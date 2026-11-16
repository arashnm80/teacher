#!/usr/bin/env python3
"""Accounts, progress and the teacher's admin API for the online playground.

Students sign up with phone number, national code, Persian full name and a password.
Their progress is kept here, and the admin panel shows it to the teacher.

Answers are checked in the student's own browser, where the playground runs Python. This
server stores what the browser reports, and checks what it can: the number of tests of each
problem, the solved flag (computed here, never taken from the browser), the typed and the
inserted characters, and rate limits. One session is allowed per student at a time.

Progress belongs to a question's id, not to its place in the list, so questions can be added
anywhere. Each question has a revision that the build raises only for a major edit (see
playground-authoring/build.py). When the revision changes, the solved mark and the hints of
that question start again for every student; attempts, code and the teacher's flags stay.

Solution material (guides and solutions) is sent only to a student who has solved the question.

    python3 app.py serve                  listen on TA_HOST:TA_PORT (default 127.0.0.1:8790)
    python3 app.py set-admin-password     asks twice; keeps only a scrypt hash in the database

Environment: TA_DB (database file), TA_PROBLEMS (problems.json), TA_ORIGIN (the public
address, checked on every write), TA_COOKIE_SECURE (1 on the public site, 0 for local tests),
TA_STATIC (local tests only: serve a site folder from the same address).
"""
from __future__ import annotations

import base64
import csv
import getpass
import hashlib
import hmac
import io
import json
import logging
import os
import re
import secrets
import sqlite3
import sys
import threading
import time
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from teacher_schedule import Schedule, jalali_plain, jalali_text, stamp_utc  # noqa: E402

CONFIG = {
    "host": os.environ.get("TA_HOST", "127.0.0.1"),
    "port": int(os.environ.get("TA_PORT", "8790")),
    "db": Path(os.environ.get("TA_DB", "/var/lib/teacher-accounts/accounts.db")),
    "problems": Path(os.environ.get("TA_PROBLEMS", "/opt/teacher-accounts/data/problems.json")),
    "origin": os.environ.get("TA_ORIGIN", "https://teacher.arashnm80.ir"),
    "secure_cookies": os.environ.get("TA_COOKIE_SECURE", "1") == "1",
    "static": os.environ.get("TA_STATIC", ""),
    "schedule": Path(os.environ.get("TA_SCHEDULE", "/opt/teacher-accounts/schedule.json")),
}

log = logging.getLogger("teacher-accounts")

STUDENT_COOKIE = "ta_student"
ADMIN_COOKIE = "ta_admin"
ADMIN_PATH = "/api/admin"
STUDENT_SESSION = timedelta(days=30)
ADMIN_SESSION = timedelta(hours=8)
MAX_FAILURES = 8  # wrong passwords or national codes in a row before the lock
ADMIN_MAX_FAILURES = 5
LOCK_FOR = timedelta(minutes=15)
PASSWORD_MIN, PASSWORD_MAX = 8, 128
MAX_BODY = 64 * 1024
OFFLINE_MAX_BODY = 1024 * 1024  # a batch of results from the offline copy, with their code
MAX_CODE = 30_000
ADMIN_PASSWORD_MIN = 12
QUICK_PASS_SECONDS = 60  # a first pass this soon after the first look is flagged (long code only)
QUICK_PASS_CODE = 120
GUIDE_FIELDS = ("guide", "guideTitle", "solutions", "mistakes")

INVALID_MESSAGE = "شماره موبایل یا رمز درست نیست."
LOCKED_MESSAGE = "چند بار رمز اشتباه وارد شده است. ۱۵ دقیقه صبر کن و دوباره امتحان کن."
DUPLICATE_MESSAGE = (
    "این شماره موبایل یا کد ملی قبلاً ثبت شده است. اگر حساب خودت است، با همان رمز وارد شو. "
    "اگر رمزت را گم کرده‌ای، از معلم بخواه آن را بازنشانی کند."
)
PASSWORD_MESSAGES = {
    "password_length": "رمز باید بین ۸ تا ۱۲۸ نویسه باشد.",
    "password_mix": "رمز باید هم حرف و هم عدد داشته باشد.",
    "password_weak": "رمز نباید همان شماره موبایل یا کد ملی باشد.",
}
STALE_MESSAGE = "این مسئله به‌روز شده است. صفحه را دوباره باز کن تا نسخه‌ی تازه را ببینی."

DIGIT_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "0123456789" * 2)
PERSIAN_NAME = re.compile(r"[ء-غف-يٱ-ۓە‌‍ ]+")
PASSWORD_LETTER = re.compile(r"[A-Za-zء-غف-يٱ-ۓ]")
PASSWORD_DIGIT = re.compile(r"[0-9]")

# Loaded at start-up from problems.json.
PROBLEMS_BYTES = b""  # the full file: admin only
PROBLEMS_PUBLIC_BYTES = b""  # what a signed-in student receives: no solution material
PROBLEM_META: dict[str, dict] = {}  # id -> total tests, current revision, title, number, samples
GUIDES: dict[str, dict] = {}  # id -> the solution material, released after a pass
SCHEDULE: Schedule | None = None  # class packs and deadlines (teacher_schedule.py)
_DUMMY_HASH: str | None = None
_counter_lock = threading.Lock()
_request_count = 0


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, **extra):
        super().__init__(code)
        self.status, self.code, self.message, self.extra = status, code, message, extra


class Raw:
    """A non-JSON response: the problems file, or the CSV export."""

    def __init__(self, body: bytes, content_type: str, filename: str = ""):
        self.body, self.content_type, self.filename = body, content_type, filename


# --- time and text ------------------------------------------------------------------------

def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_stamp(text: str | None) -> datetime | None:
    if not text:
        return None
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def clean_phone(raw: object) -> str | None:
    text = str(raw or "").translate(DIGIT_MAP)
    text = re.sub(r"[\s.()\-]", "", text)
    if text.startswith("+98"):
        text = "0" + text[3:]
    elif text.startswith("0098"):
        text = "0" + text[4:]
    return text if re.fullmatch(r"09\d{9}", text) else None


def clean_national_code(raw: object) -> str | None:
    text = re.sub(r"[\s\-]", "", str(raw or "").translate(DIGIT_MAP))
    if not re.fullmatch(r"\d{10}", text) or len(set(text)) == 1:
        return None
    total = sum(int(text[i]) * (10 - i) for i in range(9))
    rest = total % 11
    check = int(text[9])
    return text if (check == rest if rest < 2 else check == 11 - rest) else None


CLASSES = ("201", "202")


def clean_class(raw: object) -> str | None:
    text = str(raw or "").translate(DIGIT_MAP).strip()
    return text if text in CLASSES else None


def clean_full_name(raw: object) -> str | None:
    text = unicodedata.normalize("NFC", str(raw or ""))
    text = re.sub(r"[ً-ٰٟ]", "", text)  # vowel marks
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"[ \t]+", " ", text).strip()
    if not 5 <= len(text) <= 60 or not PERSIAN_NAME.fullmatch(text):
        return None
    words = [w for w in text.split(" ") if w.strip("‌‍")]
    return text if len(words) >= 2 else None


def normalize_search(raw: str) -> str:
    return raw.translate(DIGIT_MAP).strip()[:60]


def escape_like(text: str) -> str:
    return re.sub(r"([\\%_])", r"\\\1", text)


def password_problem(password: object, phone: str, national: str) -> str | None:
    if not isinstance(password, str) or not PASSWORD_MIN <= len(password) <= PASSWORD_MAX:
        return "password_length"
    if not PASSWORD_DIGIT.search(password) or not PASSWORD_LETTER.search(password):
        return "password_mix"
    if password in (phone, national):
        return "password_weak"
    return None


# --- passwords and tokens -----------------------------------------------------------------

def _scrypt(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
    return hashlib.scrypt(password, salt=salt, n=n, r=r, p=p, maxmem=64 * 1024 * 1024, dklen=length)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = _scrypt(password.encode("utf-8"), salt, 2**14, 8, 1, 32)
    return f"scrypt$16384$8$1${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(password: str, stored: str | None) -> bool:
    if not stored:
        _scrypt(b"nothing", b"0" * 16, 2**14, 8, 1, 32)  # same cost for unknown accounts
        return False
    try:
        scheme, n, r, p, salt_b64, digest_b64 = stored.split("$")
        if scheme != "scrypt":
            return False
        expected = base64.b64decode(digest_b64)
        digest = _scrypt(password.encode("utf-8"), base64.b64decode(salt_b64), int(n), int(r), int(p), len(expected))
        return hmac.compare_digest(digest, expected)
    except (ValueError, TypeError):
        return False


def dummy_hash() -> str:
    global _DUMMY_HASH
    if _DUMMY_HASH is None:
        _DUMMY_HASH = hash_password("unused-dummy-password-1")
    return _DUMMY_HASH


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def cookie_header(name: str, value: str, max_age: int, path: str) -> str:
    parts = [f"{name}={value}", f"Path={path}", "HttpOnly", "SameSite=Strict", f"Max-Age={max_age}"]
    if CONFIG["secure_cookies"]:
        parts.append("Secure")
    return "; ".join(parts)


def parse_cookies(raw: str) -> dict[str, str]:
    out = {}
    for part in raw.split(";"):
        name, sep, value = part.strip().partition("=")
        if sep and name:
            out[name] = value
    return out


# --- database -----------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL UNIQUE,
    national_code TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    class_code TEXT,
    password_hash TEXT,
    needs_password INTEGER NOT NULL DEFAULT 0,
    disabled INTEGER NOT NULL DEFAULT 0,
    failed_logins INTEGER NOT NULL DEFAULT 0,
    locked_until TEXT,
    created_at TEXT NOT NULL,
    last_login_at TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'web'
);
CREATE INDEX IF NOT EXISTS sessions_student ON sessions(student_id);
CREATE TABLE IF NOT EXISTS progress (
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    problem_id TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    solved INTEGER NOT NULL DEFAULT 0,
    solved_at TEXT,
    best_passed INTEGER NOT NULL DEFAULT 0,
    total INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_code TEXT,
    last_passed INTEGER,
    first_seen_at TEXT,
    updated_at TEXT,
    hint_level INTEGER NOT NULL DEFAULT 0,
    typed_total INTEGER NOT NULL DEFAULT 0,
    inserted_total INTEGER NOT NULL DEFAULT 0,
    flags TEXT NOT NULL DEFAULT '[]',
    PRIMARY KEY (student_id, problem_id)
);
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    problem_id TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    code TEXT NOT NULL,
    passed INTEGER NOT NULL,
    total INTEGER NOT NULL,
    solved INTEGER NOT NULL,
    typed INTEGER NOT NULL,
    inserted INTEGER NOT NULL,
    flags TEXT NOT NULL DEFAULT '[]',
    client_at TEXT
);
CREATE INDEX IF NOT EXISTS attempts_student ON attempts(student_id, id);
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    password_hash TEXT NOT NULL,
    failed_logins INTEGER NOT NULL DEFAULT 0,
    locked_until TEXT,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS admin_sessions (
    token_hash TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    at TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    ip TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS hits (
    key TEXT NOT NULL,
    at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS hits_key ON hits(key, at);
"""

UPSERT_PROGRESS = """
INSERT INTO progress (student_id, problem_id, revision, solved, solved_at, best_passed, total,
                      attempts, last_code, last_passed, first_seen_at, updated_at, typed_total,
                      inserted_total, flags)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (student_id, problem_id) DO UPDATE SET
    revision = excluded.revision,
    solved = MAX(progress.solved, excluded.solved),
    solved_at = COALESCE(progress.solved_at, excluded.solved_at),
    best_passed = MAX(progress.best_passed, excluded.best_passed),
    total = excluded.total,
    attempts = progress.attempts + excluded.attempts,
    last_code = excluded.last_code,
    last_passed = COALESCE(excluded.last_passed, progress.last_passed),
    first_seen_at = COALESCE(progress.first_seen_at, excluded.first_seen_at),
    updated_at = excluded.updated_at,
    typed_total = MAX(progress.typed_total, excluded.typed_total),
    inserted_total = MAX(progress.inserted_total, excluded.inserted_total),
    flags = excluded.flags
"""

# A new revision starts the question again: the solved mark and the hints go; code, attempts,
# flags and the typing counts stay, because the teacher needs them.
RESET_FOR_REVISION = """
UPDATE progress SET revision = ?, solved = 0, solved_at = NULL, best_passed = 0, last_passed = NULL,
                    hint_level = 0, first_seen_at = NULL
WHERE student_id = ? AND problem_id = ?
"""


def connect() -> sqlite3.Connection:
    db = sqlite3.connect(str(CONFIG["db"]), timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    return db


@contextmanager
def transaction(db: sqlite3.Connection):
    db.execute("BEGIN IMMEDIATE")
    try:
        yield db
    except BaseException:
        db.execute("ROLLBACK")
        raise
    else:
        db.execute("COMMIT")


def init_db(db: sqlite3.Connection) -> None:
    db.executescript(SCHEMA)
    # Databases made before the class field existed get the column.
    columns = {row["name"] for row in db.execute("PRAGMA table_info(students)").fetchall()}
    if "class_code" not in columns:
        db.execute("ALTER TABLE students ADD COLUMN class_code TEXT")
    # The offline copy signs in with a token: its sessions are kept apart from the website's.
    if "kind" not in {row["name"] for row in db.execute("PRAGMA table_info(sessions)").fetchall()}:
        db.execute("ALTER TABLE sessions ADD COLUMN kind TEXT NOT NULL DEFAULT 'web'")
    # Results sent later from the offline copy keep the time the student's device reported.
    if "client_at" not in {row["name"] for row in db.execute("PRAGMA table_info(attempts)").fetchall()}:
        db.execute("ALTER TABLE attempts ADD COLUMN client_at TEXT")


def audit(db: sqlite3.Connection, actor: str, action: str, target: object = "", ip: str = "") -> None:
    db.execute(
        "INSERT INTO audit (at, actor, action, target, ip) VALUES (?, ?, ?, ?, ?)",
        (stamp(now()), actor, action, str(target)[:120], ip[:64]),
    )


def limited(req: "Request", key: str, limit: int, window: int) -> None:
    """A sliding-window rate limit kept in the database, so it survives a restart."""
    current = time.time()
    with transaction(req.db):
        req.db.execute("DELETE FROM hits WHERE key = ? AND at < ?", (key, current - window))
        (count,) = req.db.execute("SELECT COUNT(*) FROM hits WHERE key = ?", (key,)).fetchone()
        if count >= limit:
            raise ApiError(429, "rate_limited", "تعداد تلاش‌ها زیاد است. کمی بعد دوباره امتحان کن.")
        req.db.execute("INSERT INTO hits (key, at) VALUES (?, ?)", (key, current))


def maintenance() -> None:
    global _request_count
    with _counter_lock:
        _request_count += 1
        due = _request_count % 200 == 0
    if not due:
        return
    db = connect()
    try:
        with transaction(db):
            t = stamp(now())
            db.execute("DELETE FROM sessions WHERE expires_at <= ?", (t,))
            db.execute("DELETE FROM admin_sessions WHERE expires_at <= ?", (t,))
            db.execute("DELETE FROM hits WHERE at < ?", (time.time() - 86400,))
    finally:
        db.close()


# --- problems -----------------------------------------------------------------------------

def load_problems() -> None:
    global PROBLEMS_BYTES, PROBLEMS_PUBLIC_BYTES
    raw = CONFIG["problems"].read_bytes()
    data = json.loads(raw.decode("utf-8"))
    PROBLEMS_BYTES = raw
    PROBLEMS_PUBLIC_BYTES = json.dumps(
        [{k: v for k, v in p.items() if k not in GUIDE_FIELDS} for p in data],
        ensure_ascii=False,
    ).encode("utf-8")
    PROBLEM_META.clear()
    GUIDES.clear()
    for p in data:
        PROBLEM_META[p["id"]] = {
            "total": len(p["tests"]),
            "revision": int(p.get("revision", 1)),
            "title": p.get("title", ""),
            "number": p.get("number", 0),
            "samples": len(p.get("samples") or []),
        }
        GUIDES[p["id"]] = {k: p[k] for k in GUIDE_FIELDS if k in p}


def clean_problem(value: object) -> str:
    if not isinstance(value, str) or value not in PROBLEM_META:
        raise ApiError(400, "unknown_problem", "این مسئله پیدا نشد.")
    return value


def clean_code(value: object) -> str:
    if not isinstance(value, str):
        raise ApiError(400, "bad_code", "کد باید متن باشد.")
    if len(value) > MAX_CODE:
        raise ApiError(400, "code_too_long", "کد خیلی طولانی است.")
    return value


def as_int(value: object, low: int, high: int, default: int | None = None) -> int:
    if value is None and default is not None:
        return default
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ApiError(400, "bad_number", "عدد نامعتبر است.")
    number = int(value)
    if not low <= number <= high:
        raise ApiError(400, "bad_number", "عدد خارج از محدوده است.")
    return number


def merge_flags(previous: list, typed_total: int, inserted_total: int, code: str,
                first_solve: bool, first_seen: str | None) -> list:
    flags = set(previous)
    if inserted_total > 0:
        flags.add("inserted")  # text appeared in the editor without being typed
    if typed_total == 0 and len(code.strip()) >= 30:
        flags.add("no_typing")
    if first_solve and first_seen and len(code) >= QUICK_PASS_CODE:
        age = (now() - parse_stamp(first_seen)).total_seconds()
        if age < QUICK_PASS_SECONDS:
            flags.add("quick_pass")
    return sorted(flags)


def sync_revisions(db: sqlite3.Connection, sid: int) -> None:
    """Start again the questions whose revision changed (a major edit). Questions that are not
    in the current file keep their rows: they come back with the progress if the id returns."""
    rows = db.execute("SELECT problem_id, revision FROM progress WHERE student_id = ?", (sid,)).fetchall()
    for row in rows:
        meta = PROBLEM_META.get(row["problem_id"])
        if meta is None or row["revision"] == meta["revision"]:
            continue
        db.execute(RESET_FOR_REVISION, (meta["revision"], sid, row["problem_id"]))
        audit(db, f"student:{sid}", "revision-reset", row["problem_id"])


# --- students -----------------------------------------------------------------------------

def get_student(db: sqlite3.Connection, sid: int) -> sqlite3.Row | None:
    return db.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()


def mask_phone(phone: str) -> str:
    return phone[:4] + "•••••" + phone[-2:]


def student_view(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "fullName": row["full_name"],
        "classCode": row["class_code"] or "",
        "phone": mask_phone(row["phone"]),
        "nationalCode": "••••••" + row["national_code"][-4:],
    }


def is_locked(row: sqlite3.Row) -> int:
    until = parse_stamp(row["locked_until"])
    if until and until > now():
        return max(1, int((until - now()).total_seconds()))
    return 0


def start_student_session(db: sqlite3.Connection, sid: int, kind: str = "web") -> str:
    token = secrets.token_urlsafe(32)
    db.execute("DELETE FROM sessions WHERE student_id = ? AND kind = ?", (sid, kind))  # one at a time
    db.execute(
        "INSERT INTO sessions (token_hash, student_id, created_at, expires_at, kind) VALUES (?, ?, ?, ?, ?)",
        (token_digest(token), sid, stamp(now()), stamp(now() + STUDENT_SESSION), kind),
    )
    return token


def open_session(req: "Request", sid: int) -> tuple[dict, list[str]]:
    """The website gets a cookie; the offline copy gets a token in the answer (no cookies cross sites)."""
    if req.offline:
        return {"token": start_student_session(req.db, sid, "offline")}, []
    token = start_student_session(req.db, sid, "web")
    return {}, [cookie_header(STUDENT_COOKIE, token, int(STUDENT_SESSION.total_seconds()), "/")]


def record_failure(db: sqlite3.Connection, sid: int) -> None:
    with transaction(db):
        (failures,) = db.execute("SELECT failed_logins FROM students WHERE id = ?", (sid,)).fetchone()
        failures += 1
        if failures >= MAX_FAILURES:
            db.execute(
                "UPDATE students SET failed_logins = 0, locked_until = ? WHERE id = ?",
                (stamp(now() + LOCK_FOR), sid),
            )
        else:
            db.execute("UPDATE students SET failed_logins = ? WHERE id = ?", (failures, sid))


def register(req: "Request"):
    limited(req, f"register:{req.ip}", 10, 3600)
    phone = clean_phone(req.body.get("phone"))
    if phone is None:
        raise ApiError(400, "phone_invalid", "شماره موبایل معتبر نیست. مثل 09123456789 بنویس.")
    national = clean_national_code(req.body.get("nationalCode"))
    if national is None:
        raise ApiError(400, "national_code_invalid", "کد ملی معتبر نیست. ده رقم را دوباره بررسی کن.")
    name = clean_full_name(req.body.get("fullName"))
    if name is None:
        raise ApiError(400, "name_invalid", "نام و نام خانوادگی را با حروف فارسی و حداقل دو کلمه بنویس.")
    class_code = clean_class(req.body.get("classCode"))
    if class_code is None:
        raise ApiError(400, "class_invalid", "کلاس را انتخاب کن: ۲۰۱ یا ۲۰۲.")
    password = req.body.get("password")
    problem = password_problem(password, phone, national)
    if problem:
        raise ApiError(400, problem, PASSWORD_MESSAGES[problem])
    try:
        with transaction(req.db):
            clash = req.db.execute(
                "SELECT 1 FROM students WHERE phone = ? OR national_code = ?", (phone, national)
            ).fetchone()
            if clash:
                raise ApiError(409, "exists", DUPLICATE_MESSAGE)
            sid = req.db.execute(
                "INSERT INTO students (phone, national_code, full_name, class_code, password_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (phone, national, name, class_code, hash_password(password), stamp(now())),
            ).lastrowid
            audit(req.db, f"student:{sid}", "register", sid, req.ip)
            extra, cookies = open_session(req, sid)
    except sqlite3.IntegrityError:
        raise ApiError(409, "exists", DUPLICATE_MESSAGE)
    return 201, {"student": student_view(get_student(req.db, sid)), **extra}, cookies


def login(req: "Request"):
    limited(req, f"login:{req.ip}", 40, 900)
    phone = clean_phone(req.body.get("phone")) or ""
    password = req.body.get("password") if isinstance(req.body.get("password"), str) else ""
    row = req.db.execute("SELECT * FROM students WHERE phone = ?", (phone,)).fetchone() if phone else None
    if row is None:
        verify_password(password, dummy_hash())
        raise ApiError(401, "invalid", INVALID_MESSAGE)
    left = is_locked(row)
    if left:
        raise ApiError(423, "locked", LOCKED_MESSAGE, retryAfter=left)
    if row["needs_password"]:
        raise ApiError(403, "reset_required",
                       "رمزت را معلم بازنشانی کرده است. با همین شماره و کد ملی، رمز جدید انتخاب کن.")
    if not verify_password(password, row["password_hash"]):
        record_failure(req.db, row["id"])
        raise ApiError(401, "invalid", INVALID_MESSAGE)
    if row["disabled"]:
        raise ApiError(403, "disabled", "این حساب غیرفعال شده است. با معلم صحبت کن.")
    with transaction(req.db):
        req.db.execute(
            "UPDATE students SET failed_logins = 0, locked_until = NULL, last_login_at = ? WHERE id = ?",
            (stamp(now()), row["id"]),
        )
        extra, cookies = open_session(req, row["id"])
        audit(req.db, f"student:{row['id']}", "login-offline" if req.offline else "login", row["id"], req.ip)
    return 200, {"student": student_view(get_student(req.db, row["id"])), **extra}, cookies


def complete_reset(req: "Request"):
    limited(req, f"reset:{req.ip}", 20, 900)
    phone = clean_phone(req.body.get("phone")) or ""
    national = clean_national_code(req.body.get("nationalCode")) or ""
    password = req.body.get("newPassword")
    row = req.db.execute("SELECT * FROM students WHERE phone = ?", (phone,)).fetchone() if phone else None
    if row is None or not row["needs_password"] or row["disabled"]:
        verify_password("", dummy_hash())
        raise ApiError(401, "invalid", INVALID_MESSAGE)
    left = is_locked(row)
    if left:
        raise ApiError(423, "locked", LOCKED_MESSAGE, retryAfter=left)
    if national != row["national_code"]:
        record_failure(req.db, row["id"])
        raise ApiError(401, "invalid", INVALID_MESSAGE)
    problem = password_problem(password, phone, national)
    if problem:
        raise ApiError(400, problem, PASSWORD_MESSAGES[problem])
    with transaction(req.db):
        req.db.execute(
            "UPDATE students SET password_hash = ?, needs_password = 0, failed_logins = 0, "
            "locked_until = NULL, last_login_at = ? WHERE id = ?",
            (hash_password(password), stamp(now()), row["id"]),
        )
        extra, cookies = open_session(req, row["id"])
        audit(req.db, f"student:{row['id']}", "password-set", row["id"], req.ip)
    return 200, {"student": student_view(get_student(req.db, row["id"])), **extra}, cookies


def logout(req: "Request"):
    token = req.token()
    if token:
        with transaction(req.db):
            req.db.execute("DELETE FROM sessions WHERE token_hash = ?", (token_digest(token),))
    return 200, {"ok": True}, ([] if req.offline else [cookie_header(STUDENT_COOKIE, "", 0, "/")])


def me(req: "Request"):
    return 200, {"student": student_view(req.require_student())}, []


def change_password(req: "Request"):
    student = req.require_student()
    limited(req, f"change:{student['id']}", 10, 3600)
    current = req.body.get("currentPassword") if isinstance(req.body.get("currentPassword"), str) else ""
    if not verify_password(current, student["password_hash"]):
        record_failure(req.db, student["id"])
        raise ApiError(401, "invalid", "رمز فعلی درست نیست.")
    new = req.body.get("newPassword")
    problem = password_problem(new, student["phone"], student["national_code"])
    if problem:
        raise ApiError(400, problem, PASSWORD_MESSAGES[problem])
    keep = token_digest(req.cookie(STUDENT_COOKIE) or "")
    with transaction(req.db):
        req.db.execute("UPDATE students SET password_hash = ? WHERE id = ?", (hash_password(new), student["id"]))
        req.db.execute("DELETE FROM sessions WHERE student_id = ? AND token_hash <> ?", (student["id"], keep))
        audit(req.db, f"student:{student['id']}", "password-changed", student["id"], req.ip)
    return 200, {"ok": True}, []


# --- progress -----------------------------------------------------------------------------

def load_schedule() -> None:
    global SCHEDULE
    SCHEDULE = Schedule.load(CONFIG["schedule"], set(PROBLEM_META))


# A first pass counts for the score only if it came on or before the question's deadline.
def scored_pass(class_code: str | None, problem_id: str, solved: bool, solved_at: str | None) -> bool:
    return bool(solved and solved_at and SCHEDULE is not None
                and SCHEDULE.is_scored(class_code, problem_id, parse_stamp(solved_at)))


def scored_counts(db: sqlite3.Connection, sid: int | None = None) -> dict[int, int]:
    query = ("SELECT p.student_id, p.problem_id, p.solved_at, s.class_code FROM progress p "
             "JOIN students s ON s.id = p.student_id WHERE p.solved = 1")
    rows = db.execute(query + (" AND p.student_id = ?" if sid is not None else ""),
                      ((sid,) if sid is not None else ())).fetchall()
    counts: dict[int, int] = {}
    for r in rows:
        if scored_pass(r["class_code"], r["problem_id"], True, r["solved_at"]):
            counts[r["student_id"]] = counts.get(r["student_id"], 0) + 1
    return counts


def progress_view(row: sqlite3.Row, class_code: str | None = None) -> dict:
    deadline = SCHEDULE.deadline(class_code, row["problem_id"]) if SCHEDULE else None
    return {
        "revision": row["revision"],
        "solved": bool(row["solved"]),
        "at": row["solved_at"],
        "scored": scored_pass(class_code, row["problem_id"], bool(row["solved"]), row["solved_at"]),
        "deadline": stamp_utc(deadline) if deadline else None,
        "deadlineText": jalali_text(deadline),
        "bestPassed": row["best_passed"],
        "total": row["total"],
        "attempts": row["attempts"],
        "lastCode": row["last_code"] or "",
        "lastPassed": row["last_passed"],
        "hintLevel": row["hint_level"],
        "flags": json.loads(row["flags"] or "[]"),
    }


def student_problems(req: "Request"):
    req.require_student()
    return 200, Raw(PROBLEMS_PUBLIC_BYTES, "application/json; charset=utf-8"), []


def student_guide(req: "Request"):
    """The آموزش of a question: open to every signed-in student from the start. Students write
    the code themselves from it; copying and pasting are blocked in the browser."""
    req.require_student()
    pid = clean_problem(req.query.get("problemId", [""])[0])
    return 200, GUIDES.get(pid, {}), []


def student_progress(req: "Request"):
    student = req.require_student()
    with transaction(req.db):
        sync_revisions(req.db, student["id"])
        rows = req.db.execute("SELECT * FROM progress WHERE student_id = ?", (student["id"],)).fetchall()
    cls = student["class_code"]
    return 200, {"progress": {r["problem_id"]: progress_view(r, cls) for r in rows}}, []


def student_schedule(req: "Request"):
    student = req.require_student()
    cls = student["class_code"]
    packs = SCHEDULE.public_packs(cls, PROBLEM_META) if SCHEDULE else []
    return 200, {"classCode": cls or "", "packs": packs}, []


def admin_schedule(req: "Request"):
    req.require_admin()
    classes = {cls: SCHEDULE.public_packs(cls, PROBLEM_META) for cls in SCHEDULE.classes()} if SCHEDULE else {}
    return 200, {"classes": classes}, []


def submission_view(r: sqlite3.Row) -> dict:
    meta = PROBLEM_META.get(r["problem_id"], {})
    total = r["total"]
    deadline = SCHEDULE.deadline(r["class_code"], r["problem_id"]) if SCHEDULE else None
    return {
        "id": r["id"],
        "at": r["created_at"],
        "class": r["class_code"] or "",
        "studentId": r["student_id"],
        "studentName": r["full_name"],
        "problemId": r["problem_id"],
        "number": meta.get("number", 0),
        "title": meta.get("title", ""),
        "passed": r["passed"],
        "total": total,
        "percent": round(r["passed"] * 100 / total, 1) if total else 0,
        "solved": bool(r["solved"]),
        "onTime": bool(deadline and parse_stamp(r["created_at"]) <= deadline),
        "deadline": stamp_utc(deadline) if deadline else None,
        "code": r["code"],
    }


SUBMISSION_SQL = '''SELECT a.*, s.full_name, s.class_code FROM attempts a
    JOIN students s ON s.id = a.student_id
    WHERE (? = '' OR s.class_code = ?) AND (? = '' OR s.full_name LIKE ? ESCAPE '\\')
    ORDER BY a.id DESC'''


def _submission_filters(req: "Request"):
    cls = (req.query.get("class", [""])[0] or "").strip()[:3]
    query = normalize_search(req.query.get("q", [""])[0])
    return cls, query, f"%{escape_like(query)}%"


def admin_submissions(req: "Request"):
    req.require_admin()
    cls, query, like = _submission_filters(req)
    rows = req.db.execute(SUBMISSION_SQL + " LIMIT 500", (cls, cls, query, like)).fetchall()
    return 200, {"submissions": [submission_view(r) for r in rows]}, []


def admin_submissions_csv(req: "Request"):
    req.require_admin()
    cls, query, like = _submission_filters(req)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["زمان ثبت (تهران، جلالی)", "کلاس", "نام و نام خانوادگی", "شماره مسئله", "مسئله",
                     "درصد آزمون‌های درست", "در مهلت", "کد"])
    for r in req.db.execute(SUBMISSION_SQL, (cls, cls, query, like)).fetchall():
        v = submission_view(r)
        writer.writerow([jalali_plain(parse_stamp(v["at"])), v["class"], csv_safe(v["studentName"]),
                         v["number"], csv_safe(v["title"]), v["percent"], "بله" if v["onTime"] else "خیر",
                         csv_safe(v["code"])])
    body = ("\ufeff" + buffer.getvalue()).encode("utf-8")
    return 200, Raw(body, "text/csv; charset=utf-8", "submissions.csv"), []


def record_draft(req: "Request", student: sqlite3.Row, body: dict) -> dict:
    pid = clean_problem(body.get("problemId"))
    code = clean_code(body.get("code"))
    hint = as_int(body.get("hintLevel"), 0, 20, 0)
    typed = as_int(body.get("typed"), 0, 10_000_000, 0)
    inserted = as_int(body.get("inserted"), 0, 10_000_000, 0)
    sid = student["id"]
    with transaction(req.db):
        sync_revisions(req.db, sid)
        prog = req.db.execute("SELECT * FROM progress WHERE student_id = ? AND problem_id = ?", (sid, pid)).fetchone()
        typed_total = max(typed, prog["typed_total"] if prog else 0)
        inserted_total = max(inserted, prog["inserted_total"] if prog else 0)
        first_seen = (prog["first_seen_at"] if prog else None) or stamp(now())
        flags = merge_flags(json.loads(prog["flags"]) if prog else [], typed_total, inserted_total, code,
                            False, first_seen)
        req.db.execute(UPSERT_PROGRESS, (
            sid, pid, PROBLEM_META[pid]["revision"], 0, None, prog["best_passed"] if prog else 0,
            PROBLEM_META[pid]["total"], 0, code, None, first_seen, stamp(now()),
            typed_total, inserted_total, json.dumps(flags),
        ))
        req.db.execute("UPDATE progress SET hint_level = MAX(hint_level, ?) WHERE student_id = ? AND problem_id = ?",
                       (hint, sid, pid))
    return {"saved": True}


def student_draft(req: "Request"):
    student = req.require_student()
    limited(req, f"draft:{student['id']}", 1500, 3600)
    return 200, record_draft(req, student, req.body), []


def record_attempt(req: "Request", student: sqlite3.Row, body: dict, client_at: str | None = None) -> dict:
    sid = student["id"]
    pid = clean_problem(body.get("problemId"))
    code = clean_code(body.get("code"))
    meta = PROBLEM_META[pid]
    revision = as_int(body.get("revision"), 1, 10_000)
    if revision != meta["revision"]:
        raise ApiError(409, "problem_updated", STALE_MESSAGE)
    total = as_int(body.get("total"), 0, 1000)
    if total != meta["total"]:
        raise ApiError(400, "total_mismatch", "تعداد آزمون‌ها با نسخه‌ی این مسئله نمی‌خواند. صفحه را دوباره باز کن.")
    blocked = body.get("blocked") is True
    passed = 0 if blocked else as_int(body.get("passed"), 0, total)
    typed = as_int(body.get("typed"), 0, 10_000_000, 0)
    inserted = as_int(body.get("inserted"), 0, 10_000_000, 0)
    solved_now = (not blocked) and total > 0 and passed == total
    with transaction(req.db):
        sync_revisions(req.db, sid)
        prog = req.db.execute("SELECT * FROM progress WHERE student_id = ? AND problem_id = ?", (sid, pid)).fetchone()
        was_solved = bool(prog["solved"]) if prog else False
        first_seen = (prog["first_seen_at"] if prog else None) or stamp(now())
        typed_total = max(typed, prog["typed_total"] if prog else 0)
        inserted_total = max(inserted, prog["inserted_total"] if prog else 0)
        flags = merge_flags(json.loads(prog["flags"]) if prog else [], typed_total, inserted_total, code,
                            solved_now and not was_solved, first_seen)
        req.db.execute(
            "INSERT INTO attempts (student_id, problem_id, revision, created_at, code, passed, total, solved, "
            "typed, inserted, flags, client_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (sid, pid, meta["revision"], stamp(now()), code, passed, total, int(solved_now), typed, inserted,
             json.dumps(flags), client_at),
        )
        req.db.execute(UPSERT_PROGRESS, (
            sid, pid, meta["revision"], int(solved_now), stamp(now()) if solved_now else None, passed, total, 1,
            code, passed, first_seen, stamp(now()), typed_total, inserted_total, json.dumps(flags),
        ))
        solved = req.db.execute("SELECT solved FROM progress WHERE student_id = ? AND problem_id = ?",
                                (sid, pid)).fetchone()["solved"]
    scored = scored_pass(student["class_code"], pid, bool(solved), prog["solved_at"] if prog and prog["solved"] else None)
    if solved_now and not was_solved:
        scored = scored_pass(student["class_code"], pid, True, stamp(now()))
    return {"problemId": pid, "solvedNow": solved_now, "solved": bool(solved), "passed": passed, "total": total,
            "flags": flags, "scored": scored}


def student_attempt(req: "Request"):
    student = req.require_student()
    limited(req, f"attempt:{student['id']}", 300, 3600)
    return 200, record_attempt(req, student, req.body), []


# --- the offline copy ---------------------------------------------------------------------
# The offline copy is a page on the student's own computer. It signs in with a token, keeps its
# results in a queue, and sends them here whenever there is internet. The deadline is decided by
# this server's clock at the moment a result arrives: a result counts when it reaches us in time.

SYNC_MAX = 100
CLIENT_TIME = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d(\.\d{1,6})?)?Z?$")


def clean_client_time(value: object) -> str | None:
    return value if isinstance(value, str) and CLIENT_TIME.match(value) else None


def offline_state(req: "Request", student: sqlite3.Row) -> dict:
    cls = student["class_code"]
    with transaction(req.db):
        sync_revisions(req.db, student["id"])
        rows = req.db.execute("SELECT * FROM progress WHERE student_id = ?", (student["id"],)).fetchall()
    return {
        "student": student_view(student),
        "classCode": cls or "",
        "progress": {r["problem_id"]: progress_view(r, cls) for r in rows},
        "packs": SCHEDULE.public_packs(cls, PROBLEM_META) if SCHEDULE else [],
        "revisions": {pid: meta["revision"] for pid, meta in PROBLEM_META.items()},
        "serverTime": stamp(now()),
    }


def offline_me(req: "Request"):
    return 200, offline_state(req, req.require_student()), []


def offline_sync(req: "Request"):
    student = req.require_student()
    limited(req, f"sync:{student['id']}", 60, 3600)
    items = req.body.get("results")
    if not isinstance(items, list) or len(items) > SYNC_MAX:
        raise ApiError(400, "bad_results", "فهرست نتیجه‌ها معتبر نیست.")
    outcomes = []
    for item in items:
        pid_text = str(item.get("problemId"))[:20] if isinstance(item, dict) else ""
        try:
            if not isinstance(item, dict):
                raise ApiError(400, "bad_results", "فهرست نتیجه‌ها معتبر نیست.")
            outcomes.append({"ok": True, **record_attempt(req, student, item, clean_client_time(item.get("clientAt")))})
        except ApiError as err:
            outcomes.append({"ok": False, "problemId": pid_text, "error": err.code, "message": err.message})
    return 200, {"results": outcomes, **offline_state(req, student)}, []



# --- admin --------------------------------------------------------------------------------

def store_admin_password(password: str) -> None:
    db = connect()
    try:
        init_db(db)
        with transaction(db):
            db.execute(
                "INSERT INTO admin (id, password_hash, failed_logins, locked_until, updated_at) "
                "VALUES (1, ?, 0, NULL, ?) ON CONFLICT (id) DO UPDATE SET password_hash = excluded.password_hash, "
                "failed_logins = 0, locked_until = NULL, updated_at = excluded.updated_at",
                (hash_password(password), stamp(now())),
            )
            db.execute("DELETE FROM admin_sessions")
    finally:
        db.close()


def admin_login(req: "Request"):
    limited(req, f"admin:{req.ip}", 10, 900)
    row = req.db.execute("SELECT * FROM admin WHERE id = 1").fetchone()
    if row is None:
        raise ApiError(503, "not_configured", "رمز مدیر هنوز تعیین نشده است.")
    left = is_locked(row)
    if left:
        raise ApiError(423, "locked", LOCKED_MESSAGE, retryAfter=left)
    password = req.body.get("password") if isinstance(req.body.get("password"), str) else ""
    if not verify_password(password, row["password_hash"]):
        with transaction(req.db):
            fails = row["failed_logins"] + 1
            locked = stamp(now() + LOCK_FOR) if fails >= ADMIN_MAX_FAILURES else None
            req.db.execute("UPDATE admin SET failed_logins = ?, locked_until = ? WHERE id = 1",
                           (0 if locked else fails, locked))
            audit(req.db, "admin", "login-failed", "", req.ip)
        raise ApiError(401, "invalid", "رمز اشتباه است.")
    token = secrets.token_urlsafe(32)
    with transaction(req.db):
        req.db.execute("UPDATE admin SET failed_logins = 0, locked_until = NULL WHERE id = 1")
        req.db.execute("INSERT INTO admin_sessions (token_hash, created_at, expires_at) VALUES (?, ?, ?)",
                       (token_digest(token), stamp(now()), stamp(now() + ADMIN_SESSION)))
        audit(req.db, "admin", "login", "", req.ip)
    cookie = cookie_header(ADMIN_COOKIE, token, int(ADMIN_SESSION.total_seconds()), ADMIN_PATH)
    return 200, {"ok": True}, [cookie]


def admin_logout(req: "Request"):
    token = req.cookie(ADMIN_COOKIE)
    if token:
        with transaction(req.db):
            req.db.execute("DELETE FROM admin_sessions WHERE token_hash = ?", (token_digest(token),))
    return 200, {"ok": True}, [cookie_header(ADMIN_COOKIE, "", 0, ADMIN_PATH)]


def admin_session(req: "Request"):
    req.require_admin()
    return 200, {"ok": True}, []


def student_row_view(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "fullName": row["full_name"],
        "classCode": row["class_code"] or "",
        "phone": row["phone"],
        "nationalCode": row["national_code"],
        "createdAt": row["created_at"],
        "lastLoginAt": row["last_login_at"],
        "needsPassword": bool(row["needs_password"]),
        "disabled": bool(row["disabled"]),
        "locked": bool(is_locked(row)),
        "solved": row["solved"],
        "attempts": row["attempts"],
        "flagged": row["flagged"],
    }


SUMMARY_SQL = """SELECT s.*,
     (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id AND p.solved = 1) AS solved,
     (SELECT COUNT(*) FROM attempts a WHERE a.student_id = s.id) AS attempts,
     (SELECT COUNT(*) FROM progress p WHERE p.student_id = s.id AND p.flags <> '[]') AS flagged
   FROM students s"""


def admin_students(req: "Request"):
    req.require_admin()
    query = normalize_search(req.query.get("q", [""])[0])
    like = f"%{escape_like(query)}%"
    rows = req.db.execute(
        SUMMARY_SQL + """ WHERE ? = '' OR s.full_name LIKE ? ESCAPE '\\' OR s.phone LIKE ? ESCAPE '\\'
                 OR s.national_code LIKE ? ESCAPE '\\'
           ORDER BY s.full_name, s.id LIMIT 1000""",
        (query, like, like, like),
    ).fetchall()
    scored = scored_counts(req.db)
    views = []
    for r in rows:
        view = student_row_view(r)
        view["scored"] = scored.get(r["id"], 0)
        views.append(view)
    return 200, {"students": views, "problemCount": len(PROBLEM_META)}, []


def admin_student_detail(req: "Request", sid: int):
    req.require_admin()
    with transaction(req.db):
        sync_revisions(req.db, sid)
    row = req.db.execute(SUMMARY_SQL + " WHERE s.id = ?", (sid,)).fetchone()
    if row is None:
        raise ApiError(404, "not_found", "این دانش‌آموز پیدا نشد.")
    progress = []
    for r in req.db.execute("SELECT * FROM progress WHERE student_id = ?", (sid,)).fetchall():
        meta = PROBLEM_META.get(r["problem_id"], {})
        item = progress_view(r, row["class_code"])
        item.update({"problemId": r["problem_id"], "number": meta.get("number", 0),
                     "title": meta.get("title", "") or "(این مسئله از فهرست حذف شده است)"})
        progress.append(item)
    progress.sort(key=lambda item: item["number"])
    attempts = [
        {
            "id": a["id"], "problemId": a["problem_id"], "revision": a["revision"], "at": a["created_at"],
            "passed": a["passed"], "total": a["total"], "solved": bool(a["solved"]),
            "typed": a["typed"], "inserted": a["inserted"], "flags": json.loads(a["flags"] or "[]"),
            "code": a["code"], "percent": round(a["passed"] * 100 / a["total"], 1) if a["total"] else 0,
            "onTime": bool(SCHEDULE and SCHEDULE.is_scored(row["class_code"], a["problem_id"],
                                                          parse_stamp(a["created_at"]))),
        }
        for a in req.db.execute(
            "SELECT * FROM attempts WHERE student_id = ? ORDER BY id DESC LIMIT 60", (sid,)).fetchall()
    ]
    view = student_row_view(row)
    view["scored"] = scored_counts(req.db, sid).get(sid, 0)
    return 200, {"student": view, "progress": progress, "attempts": attempts,
                 "problemCount": len(PROBLEM_META)}, []


def admin_reset_password(req: "Request", sid: int):
    req.require_admin()
    with transaction(req.db):
        if get_student(req.db, sid) is None:
            raise ApiError(404, "not_found", "این دانش‌آموز پیدا نشد.")
        req.db.execute(
            "UPDATE students SET password_hash = NULL, needs_password = 1, failed_logins = 0, locked_until = NULL "
            "WHERE id = ?", (sid,))
        req.db.execute("DELETE FROM sessions WHERE student_id = ?", (sid,))
        audit(req.db, "admin", "reset-password", sid, req.ip)
    return 200, {"ok": True}, []


def admin_change_class(req: "Request", sid: int):
    req.require_admin()
    code = clean_class(req.body.get("classCode"))
    if code is None:
        raise ApiError(400, "class_invalid", "کلاس را ۲۰۱ یا ۲۰۲ بگذار.")
    with transaction(req.db):
        row = get_student(req.db, sid)
        if row is None:
            raise ApiError(404, "not_found", "این دانش‌آموز پیدا نشد.")
        req.db.execute("UPDATE students SET class_code = ? WHERE id = ?", (code, sid))
        audit(req.db, "admin", "class-change", f"{sid}: {row['class_code'] or '-'} -> {code}", req.ip)
    return 200, {"ok": True, "classCode": code}, []


def admin_set_disabled(req: "Request", sid: int, disabled: bool):
    req.require_admin()
    with transaction(req.db):
        if get_student(req.db, sid) is None:
            raise ApiError(404, "not_found", "این دانش‌آموز پیدا نشد.")
        req.db.execute("UPDATE students SET disabled = ? WHERE id = ?", (int(disabled), sid))
        if disabled:
            req.db.execute("DELETE FROM sessions WHERE student_id = ?", (sid,))
        audit(req.db, "admin", "disable" if disabled else "enable", sid, req.ip)
    return 200, {"ok": True}, []


def csv_safe(value: object) -> str:
    text = str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def admin_export(req: "Request"):
    req.require_admin()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["شناسه", "نام و نام خانوادگی", "کلاس", "شماره موبایل", "کد ملی",
                     "مسئله‌های قبول‌شده", "تعداد ثبت‌ها", "کد نیازمند بررسی", "تاریخ ثبت‌نام", "آخرین ورود"])
    total = len(PROBLEM_META)
    for row in req.db.execute(SUMMARY_SQL + " ORDER BY s.id").fetchall():
        writer.writerow([row["id"], csv_safe(row["full_name"]), row["class_code"] or "", row["phone"], row["national_code"],
                         f"{row['solved']} از {total}", row["attempts"], row["flagged"],
                         row["created_at"], row["last_login_at"] or ""])
    body = ("﻿" + buffer.getvalue()).encode("utf-8")
    return 200, Raw(body, "text/csv; charset=utf-8", "students.csv"), []


def admin_audit(req: "Request"):
    req.require_admin()
    rows = req.db.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 200").fetchall()
    return 200, {"entries": [
        {"at": r["at"], "actor": r["actor"], "action": r["action"], "target": r["target"]} for r in rows
    ]}, []


def admin_problems(req: "Request"):
    req.require_admin()
    return 200, Raw(PROBLEMS_BYTES, "application/json; charset=utf-8"), []


# --- request plumbing ---------------------------------------------------------------------

class Request:
    def __init__(self, handler, method: str, query: str, body: dict, db: sqlite3.Connection):
        self.handler = handler
        self.method = method
        self.query = parse_qs(query)
        self.body = body
        self.db = db
        self.ip = client_ip(handler)
        self.cookies = parse_cookies(handler.headers.get("Cookie", ""))
        self.offline = urlsplit(handler.path).path.startswith("/api/offline/")

    def cookie(self, name: str) -> str | None:
        return self.cookies.get(name)

    def token(self) -> str | None:
        """The website sends a cookie; the offline copy sends 'Authorization: Bearer <token>'."""
        if self.offline:
            header = self.handler.headers.get("Authorization", "")
            return header[7:].strip() or None if header[:7].lower() == "bearer " else None
        return self.cookie(STUDENT_COOKIE)

    def student(self) -> sqlite3.Row | None:
        token = self.token()
        if not token:
            return None
        row = self.db.execute(
            "SELECT s.* FROM sessions se JOIN students s ON s.id = se.student_id "
            "WHERE se.token_hash = ? AND se.kind = ? AND se.expires_at > ?",
            (token_digest(token), "offline" if self.offline else "web", stamp(now())),
        ).fetchone()
        if row is None or row["disabled"]:
            return None
        return row

    def require_student(self) -> sqlite3.Row:
        row = self.student()
        if row is None:
            raise ApiError(401, "login_required", "برای ادامه وارد شو.")
        return row

    def require_admin(self) -> None:
        token = self.cookie(ADMIN_COOKIE)
        ok = token and self.db.execute(
            "SELECT 1 FROM admin_sessions WHERE token_hash = ? AND expires_at > ?",
            (token_digest(token), stamp(now())),
        ).fetchone()
        if not ok:
            raise ApiError(401, "admin_required", "برای ورود به پنل، رمز مدیر را وارد کن.")


def client_ip(handler) -> str:
    peer = handler.client_address[0]
    if peer in ("127.0.0.1", "::1"):  # the public site reaches us through nginx on this machine
        forwarded = handler.headers.get("CF-Connecting-IP") or handler.headers.get("X-Real-IP")
        if forwarded:
            return forwarded.strip()[:64]
    return peer


ROUTES: list[tuple[str, re.Pattern, object]] = []


def route(method: str, pattern: str, func) -> None:
    ROUTES.append((method, re.compile(pattern + r"\Z"), func))


route("POST", "/api/student/register", register)
route("POST", "/api/student/login", login)
route("POST", "/api/student/complete-reset", complete_reset)
route("POST", "/api/student/logout", logout)
route("GET", "/api/student/me", me)
route("POST", "/api/student/change-password", change_password)
route("GET", "/api/student/problems", student_problems)
route("GET", "/api/student/guide", student_guide)
route("GET", "/api/student/progress", student_progress)
route("POST", "/api/student/draft", student_draft)
route("POST", "/api/student/attempt", student_attempt)
route("POST", "/api/admin/login", admin_login)
route("POST", "/api/admin/logout", admin_logout)
route("GET", "/api/admin/session", admin_session)
route("GET", "/api/admin/students", admin_students)
route("GET", r"/api/admin/students/(\d+)", lambda req, sid: admin_student_detail(req, int(sid)))
route("POST", r"/api/admin/students/(\d+)/reset-password", lambda req, sid: admin_reset_password(req, int(sid)))
route("POST", r"/api/admin/students/(\d+)/disable", lambda req, sid: admin_set_disabled(req, int(sid), True))
route("POST", r"/api/admin/students/(\d+)/enable", lambda req, sid: admin_set_disabled(req, int(sid), False))
route("POST", r"/api/admin/students/(\d+)/class", lambda req, sid: admin_change_class(req, int(sid)))
route("GET", "/api/admin/export.csv", admin_export)
route("GET", "/api/admin/audit", admin_audit)
route("GET", "/api/admin/problems", admin_problems)
route("GET", "/api/student/schedule", student_schedule)
route("POST", "/api/offline/register", register)
route("POST", "/api/offline/login", login)
route("POST", "/api/offline/complete-reset", complete_reset)
route("POST", "/api/offline/logout", logout)
route("GET", "/api/offline/me", offline_me)
route("POST", "/api/offline/sync", offline_sync)
route("GET", "/api/admin/schedule", admin_schedule)
route("GET", "/api/admin/submissions", admin_submissions)
route("GET", "/api/admin/submissions.csv", admin_submissions_csv)


def match_route(method: str, path: str):
    for route_method, pattern, func in ROUTES:
        if route_method != method:
            continue
        found = pattern.match(path)
        if found:
            return func, found.groups()
    return None


def allowed_origins() -> set[str]:
    origins = {CONFIG["origin"]}
    if CONFIG["static"]:  # local tests: the page is served from this same machine
        port = CONFIG["port"]
        origins |= {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
    return origins


class Handler(SimpleHTTPRequestHandler):
    server_version = "teacher-accounts"
    sys_version = ""

    def log_message(self, format, *args):  # paths only: never bodies, cookies or query strings
        status = args[1] if len(args) > 1 else ""
        log.info("%s %s %s", self.command, urlsplit(self.path).path, status)

    cors = False  # the offline routes answer pages on the student's own computer

    def do_GET(self):
        self.dispatch("GET")

    def do_OPTIONS(self):
        path = unquote(urlsplit(self.path).path)
        if path.startswith("/api/offline/"):
            self.cors = True
            return self.send_result(204, {}, [])
        self.send_result(405, {"error": "method_not_allowed", "message": "این درخواست مجاز نیست."}, [])

    def do_POST(self):
        self.dispatch("POST")

    def do_PUT(self):
        self.send_result(405, {"error": "method_not_allowed", "message": "این درخواست مجاز نیست."}, [])

    do_DELETE = do_PUT
    do_PATCH = do_PUT

    def dispatch(self, method: str) -> None:
        parts = urlsplit(self.path)
        path = unquote(parts.path)
        self.cors = path.startswith("/api/offline/")
        if not path.startswith("/api/"):
            if method == "GET" and CONFIG["static"]:
                return SimpleHTTPRequestHandler.do_GET(self)
            return self.send_result(404, {"error": "not_found", "message": "نشانی پیدا نشد."}, [])
        found = match_route(method, path)
        if found is None:
            return self.send_result(404, {"error": "not_found", "message": "نشانی پیدا نشد."}, [])
        func, params = found
        try:
            if method == "POST":
                origin = self.headers.get("Origin")
                if not self.cors and origin is not None and origin not in allowed_origins():
                    raise ApiError(403, "bad_origin", "این درخواست از همین سایت نیامده است.")
                body = self.read_body()
            else:
                body = {}
            db = connect()
            try:
                req = Request(self, method, parts.query, body, db)
                status, payload, cookies = func(req, *params)
            finally:
                db.close()
            maintenance()
            self.send_result(status, payload, cookies)
        except ApiError as err:
            self.send_result(err.status, {"error": err.code, "message": err.message, **err.extra}, [])
        except Exception:
            log.exception("request failed: %s %s", method, path)
            self.send_result(500, {"error": "server_error", "message": "خطای سرور. دوباره تلاش کن."}, [])

    def read_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            raise ApiError(400, "bad_length", "درخواست نامعتبر است.")
        if length == 0:
            return {}
        if length > (OFFLINE_MAX_BODY if self.cors else MAX_BODY):
            raise ApiError(413, "too_large", "درخواست خیلی بزرگ است.")
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype != "application/json":
            raise ApiError(415, "unsupported_media", "درخواست باید JSON باشد.")
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ApiError(400, "bad_json", "درخواست نامعتبر است.")
        if not isinstance(data, dict):
            raise ApiError(400, "bad_json", "درخواست نامعتبر است.")
        return data

    def send_result(self, status: int, payload, cookies: list[str]) -> None:
        extra: list[tuple[str, str]] = []
        if isinstance(payload, Raw):
            body, ctype = payload.body, payload.content_type
            if payload.filename:
                extra.append(("Content-Disposition", f'attachment; filename="{payload.filename}"'))
        else:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            ctype = "application/json; charset=utf-8"
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        for name, value in extra:
            self.send_header(name, value)
        for cookie in cookies:
            self.send_header("Set-Cookie", cookie)
        if self.cors:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()
        if status != 204:
            self.wfile.write(body)


def serve() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_problems()
    load_schedule()
    db = connect()
    try:
        init_db(db)
    finally:
        db.close()
    handler = partial(Handler, directory=CONFIG["static"]) if CONFIG["static"] else Handler
    server = ThreadingHTTPServer((CONFIG["host"], CONFIG["port"]), handler)
    log.info("listening on %s:%d (%d problems)", CONFIG["host"], CONFIG["port"], len(PROBLEM_META))
    server.serve_forever()


def set_admin_password() -> int:
    first = getpass.getpass("New admin password (at least 12 characters): ")
    second = getpass.getpass("Repeat the password: ")
    if first != second:
        print("The two passwords differ. Nothing was saved.", file=sys.stderr)
        return 1
    if not ADMIN_PASSWORD_MIN <= len(first) <= 256:
        print(f"Use {ADMIN_PASSWORD_MIN} to 256 characters. Nothing was saved.", file=sys.stderr)
        return 1
    store_admin_password(first)
    print("Admin password saved. Existing admin sessions were ended.")
    return 0


def main(argv: list[str]) -> int:
    command = argv[1] if len(argv) > 1 else "serve"
    if command == "serve":
        serve()
        return 0
    if command == "set-admin-password":
        return set_admin_password()
    print("usage: app.py serve | set-admin-password", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
