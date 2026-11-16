"""Tests for the accounts service: validation, sign-up, login, sessions, progress, revisions,
guides, admin and abuse.

Run with:  python3 test_accounts.py
Each test starts from an empty student list and the base question file; the server runs in
this process on a free port.
"""
import copy
import http.client
import json
import os
import sqlite3
import sys
import tempfile
import threading
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TMP = tempfile.mkdtemp(prefix="ta-test-")
FIXTURE = [
    {
        "id": "p01", "number": 1, "title": "سلام", "mode": "stdio", "revision": 1,
        "tests": [{"stdin": "Ali\n", "stdout": "Hello, Ali\n"}, {"stdin": "Sara\n", "stdout": "Hello, Sara\n"}],
        "samples": [{"stdin": "Ali\n", "stdout": "Hello, Ali\n"}],
        "guide": "SECRET-GUIDE-TEXT", "guideTitle": "راهنما", "solutions": [{"code": "SECRET-SOLUTION"}],
        "mistakes": ["SECRET-MISTAKE"], "hints": ["نام را بخوان"], "starter": "name = input()",
    },
    {
        "id": "p02", "number": 2, "title": "تابع", "mode": "function", "revision": 1, "functionName": "square",
        "tests": [{"call": {"args": [2], "expected": 4}}, {"call": {"args": [3], "expected": 9}},
                  {"call": {"args": [0], "expected": 0}}],
        "samples": [{"call": {"args": [2], "expected": 4}}], "guide": "SECRET-GUIDE-2",
    },
]
os.environ.update({
    "TA_DB": os.path.join(TMP, "accounts.db"),
    "TA_PROBLEMS": os.path.join(TMP, "problems.json"),
    "TA_ORIGIN": "https://teacher.example.test",
    "TA_COOKIE_SECURE": "0",
})
sys.path.insert(0, str(HERE))
import app as ta  # noqa: E402

PHONE = "09123456789"
NATIONAL = "0499370899"  # passes the national code check digit
OTHER_PHONE = "09351234567"
OTHER_NATIONAL = "1234567891"  # also passes the check digit
NAME = "علی احمدی"
OTHER_NAME = "سارا محمدی"
PASSWORD = "abc12345"
ADMIN_PASSWORD = "admin-password-123"
ORIGIN = "https://teacher.example.test"


def base_fixture():
    return copy.deepcopy(FIXTURE)


def use_problems(problems):
    Path(os.environ["TA_PROBLEMS"]).write_text(json.dumps(problems, ensure_ascii=False), encoding="utf-8")
    ta.load_problems()


def call(port, method, path, body=None, cookie=None, origin=None, raw=None, content_type="application/json"):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
    headers = {}
    if cookie:
        headers["Cookie"] = cookie
    if origin:
        headers["Origin"] = origin
    data = None
    if raw is not None:
        data = raw
        headers["Content-Type"] = content_type
    elif body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    conn.request(method, path, body=data, headers=headers)
    resp = conn.getresponse()
    payload = resp.read()
    set_cookies = resp.msg.get_all("Set-Cookie") or []
    ctype = resp.getheader("Content-Type", "")
    conn.close()
    parsed = json.loads(payload.decode("utf-8")) if ctype.startswith("application/json") else payload
    return resp.status, parsed, set_cookies, resp


def cookie_value(set_cookies, name):
    for item in set_cookies:
        if item.startswith(name + "="):
            value = item.split(";")[0].split("=", 1)[1]
            return f"{name}={value}" if value else None
    return None


class Base(unittest.TestCase):
    port = 0
    httpd = None

    @classmethod
    def setUpClass(cls):
        db = ta.connect()
        ta.init_db(db)
        db.close()
        ta.store_admin_password(ADMIN_PASSWORD)
        cls.httpd = ta.ThreadingHTTPServer(("127.0.0.1", 0), ta.Handler)
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def setUp(self):
        use_problems(base_fixture())
        db = ta.connect()
        with ta.transaction(db):
            for table in ("students", "sessions", "progress", "attempts", "hits", "admin_sessions", "audit"):
                db.execute(f"DELETE FROM {table}")
            db.execute("UPDATE admin SET failed_logins = 0, locked_until = NULL")
        db.close()

    def register(self, phone=PHONE, national=NATIONAL, name=NAME, password=PASSWORD):
        status, body, cookies, _ = call(self.port, "POST", "/api/student/register",
                                        {"phone": phone, "nationalCode": national, "classCode": "201", "fullName": name,
                                         "password": password})
        self.assertEqual(status, 201, body)
        return cookie_value(cookies, ta.STUDENT_COOKIE)

    def login(self, phone=PHONE, password=PASSWORD):
        status, body, cookies, _ = call(self.port, "POST", "/api/student/login",
                                        {"phone": phone, "password": password})
        return status, body, cookie_value(cookies, ta.STUDENT_COOKIE)

    def admin_cookie(self):
        status, body, cookies, _ = call(self.port, "POST", "/api/admin/login", {"password": ADMIN_PASSWORD})
        self.assertEqual(status, 200, body)
        return cookie_value(cookies, ta.ADMIN_COOKIE)

    def db(self):
        return sqlite3.connect(os.environ["TA_DB"])


class ValidationTests(unittest.TestCase):
    def test_national_code(self):
        self.assertEqual(ta.clean_national_code("0499370899"), "0499370899")
        self.assertIsNone(ta.clean_national_code("0499370898"))
        self.assertIsNone(ta.clean_national_code("1111111111"))
        self.assertIsNone(ta.clean_national_code("123"))
        self.assertEqual(ta.clean_national_code("۰۴۹۹۳۷۰۸۹۹"), "0499370899")

    def test_phone(self):
        self.assertEqual(ta.clean_phone("09123456789"), "09123456789")
        self.assertEqual(ta.clean_phone("+989123456789"), "09123456789")
        self.assertEqual(ta.clean_phone("۰۹۱۲۳۴۵۶۷۸۹"), "09123456789")
        self.assertIsNone(ta.clean_phone("0912345678"))
        self.assertIsNone(ta.clean_phone("08123456789"))
        self.assertIsNone(ta.clean_phone("09123456789; DROP TABLE students"))

    def test_name_must_be_persian_with_two_words(self):
        self.assertEqual(ta.clean_full_name("علی احمدی"), "علی احمدی")
        self.assertEqual(ta.clean_full_name("علی   احمدی"), "علی احمدی")
        self.assertEqual(ta.clean_full_name("علي احمدي"), "علی احمدی")
        self.assertIsNone(ta.clean_full_name("Ali Ahmadi"))
        self.assertIsNone(ta.clean_full_name("علی"))
        self.assertIsNone(ta.clean_full_name("<script>alert(1)</script>"))
        self.assertIsNone(ta.clean_full_name("علی ۱۲"))
        self.assertIsNone(ta.clean_full_name("علی احمدی؟"))

    def test_password_policy(self):
        self.assertEqual(ta.password_problem("short1", PHONE, NATIONAL), "password_length")
        self.assertEqual(ta.password_problem("abcdefgh", PHONE, NATIONAL), "password_mix")
        self.assertEqual(ta.password_problem("12345678", PHONE, NATIONAL), "password_mix")
        self.assertIsNone(ta.password_problem("abc12345", PHONE, NATIONAL))

    def test_scrypt_round_trip(self):
        stored = ta.hash_password("abc12345")
        self.assertTrue(stored.startswith("scrypt$"))
        self.assertTrue(ta.verify_password("abc12345", stored))
        self.assertFalse(ta.verify_password("abc12346", stored))
        self.assertFalse(ta.verify_password("abc12345", None))


class SignUpAndLoginTests(Base):
    def test_register_sets_session_and_returns_masked_details(self):
        cookie = self.register()
        self.assertIsNotNone(cookie)
        status, body, _, _ = call(self.port, "GET", "/api/student/me", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(body["student"]["fullName"], NAME)
        self.assertNotIn(NATIONAL, json.dumps(body, ensure_ascii=False))
        self.assertNotIn("abc12345", json.dumps(body))
        status, _, _, _ = call(self.port, "GET", "/api/student/me")
        self.assertEqual(status, 401)

    def test_class_must_be_201_or_202(self):
        base = {"phone": PHONE, "nationalCode": NATIONAL, "fullName": NAME, "password": PASSWORD}
        for bad in (None, "203", "2O1", ""):
            body = dict(base, classCode=bad) if bad is not None else dict(base)
            status, response, _, _ = call(self.port, "POST", "/api/student/register", body)
            self.assertEqual(status, 400, bad)
            self.assertEqual(response["error"], "class_invalid")
        status, response, _, _ = call(self.port, "POST", "/api/student/register", dict(base, classCode="۲۰۲"))
        self.assertEqual(status, 201)
        self.assertEqual(response["student"]["id"] > 0, True)

    def test_class_reaches_the_panel_and_the_export(self):
        self.register()
        admin = self.admin_cookie()
        status, body, _, _ = call(self.port, "GET", "/api/admin/students", cookie=admin)
        self.assertEqual(body["students"][0]["classCode"], "201")
        status, raw, _, _ = call(self.port, "GET", "/api/admin/export.csv", cookie=admin)
        self.assertIn("کلاس".encode("utf-8"), raw)

    def test_duplicate_phone_or_national_code_is_refused(self):
        self.register()
        status, body, _, _ = call(self.port, "POST", "/api/student/register", {
            "phone": PHONE, "nationalCode": NATIONAL, "classCode": "201", "fullName": NAME, "password": PASSWORD})
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "exists")
        status, body, _, _ = call(self.port, "POST", "/api/student/register", {
            "phone": "09999999999", "nationalCode": NATIONAL, "classCode": "201", "fullName": NAME, "password": PASSWORD})
        self.assertEqual(status, 409)

    def test_invalid_fields_get_specific_errors(self):
        cases = [
            ({"phone": "0912", "nationalCode": NATIONAL, "classCode": "201", "fullName": NAME, "password": PASSWORD}, "phone_invalid"),
            ({"phone": PHONE, "nationalCode": "1234567890", "classCode": "201", "fullName": NAME, "password": PASSWORD},
             "national_code_invalid"),
            ({"phone": PHONE, "nationalCode": NATIONAL, "classCode": "201", "fullName": "Ali Ahmadi", "password": PASSWORD},
             "name_invalid"),
            ({"phone": PHONE, "nationalCode": NATIONAL, "classCode": "201", "fullName": NAME, "password": "abcdefgh"},
             "password_mix"),
        ]
        for body, code in cases:
            status, response, _, _ = call(self.port, "POST", "/api/student/register", body)
            self.assertEqual(status, 400, body)
            self.assertEqual(response["error"], code)

    def test_login_wrong_password_then_lock_then_expiry(self):
        self.register()
        for _ in range(ta.MAX_FAILURES):
            status, body, _ = self.login(password="wrong-pass-1")
            self.assertEqual(status, 401)
        status, body, _ = self.login()
        self.assertEqual(status, 423, "the right password is refused while the account is locked")
        self.assertIn("retryAfter", body)
        db = self.db()
        db.execute("UPDATE students SET locked_until = '2000-01-01T00:00:00Z'")
        db.commit()
        db.close()
        status, _, cookie = self.login()
        self.assertEqual(status, 200)
        self.assertIsNotNone(cookie)

    def test_one_session_per_student(self):
        first = self.register()
        status, _, second = self.login()
        self.assertEqual(status, 200)
        status, _, _, _ = call(self.port, "GET", "/api/student/me", cookie=first)
        self.assertEqual(status, 401, "the earlier browser is signed out")
        status, _, _, _ = call(self.port, "GET", "/api/student/me", cookie=second)
        self.assertEqual(status, 200)

    def test_logout_ends_the_session(self):
        cookie = self.register()
        status, _, _, _ = call(self.port, "POST", "/api/student/logout", {}, cookie=cookie)
        self.assertEqual(status, 200)
        status, _, _, _ = call(self.port, "GET", "/api/student/me", cookie=cookie)
        self.assertEqual(status, 401)

    def test_change_password_keeps_current_session_and_ends_others(self):
        cookie = self.register()
        _, _, other = self.login()
        status, body, _, _ = call(self.port, "POST", "/api/student/change-password",
                                  {"currentPassword": PASSWORD, "newPassword": "newpass999"}, cookie=other)
        self.assertEqual(status, 200, body)
        status, _, _, _ = call(self.port, "GET", "/api/student/me", cookie=cookie)
        self.assertEqual(status, 401)
        self.assertEqual(self.login(password="newpass999")[0], 200)

    def test_reset_by_teacher_then_student_chooses_password(self):
        cookie = self.register()
        admin = self.admin_cookie()
        status, _, _, _ = call(self.port, "GET", "/api/admin/students", cookie=admin)
        self.assertEqual(status, 200)
        sid = self.db().execute("SELECT id FROM students").fetchone()[0]
        status, _, _, _ = call(self.port, "POST", f"/api/admin/students/{sid}/reset-password", {}, cookie=admin)
        self.assertEqual(status, 200)
        status, _, _, _ = call(self.port, "GET", "/api/student/me", cookie=cookie)
        self.assertEqual(status, 401, "the old session ends with the reset")
        status, body, _ = self.login()
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "reset_required")
        status, body, _, _ = call(self.port, "POST", "/api/student/complete-reset", {
            "phone": PHONE, "nationalCode": "0499370890", "newPassword": "newpass999"})
        self.assertEqual(status, 401, "a wrong national code does not reset")
        status, body, cookies, _ = call(self.port, "POST", "/api/student/complete-reset", {
            "phone": PHONE, "nationalCode": NATIONAL, "newPassword": "newpass999"})
        self.assertEqual(status, 200, body)
        self.assertIsNotNone(cookie_value(cookies, ta.STUDENT_COOKIE))
        self.assertEqual(self.login(password=PASSWORD)[0], 401, "the old password no longer works")
        self.assertEqual(self.login(password="newpass999")[0], 200)

    def test_disable_blocks_login_and_enable_restores(self):
        self.register()
        admin = self.admin_cookie()
        sid = self.db().execute("SELECT id FROM students").fetchone()[0]
        call(self.port, "POST", f"/api/admin/students/{sid}/disable", {}, cookie=admin)
        status, body, _ = self.login()
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "disabled")
        call(self.port, "POST", f"/api/admin/students/{sid}/enable", {}, cookie=admin)
        self.assertEqual(self.login()[0], 200)


class ProgressTests(Base):
    def setUp(self):
        super().setUp()
        self.cookie = self.register()

    def attempt(self, problem, passed, total, code="print('x')", revision=1, **extra):
        body = {"problemId": problem, "code": code, "passed": passed, "total": total, "revision": revision, **extra}
        return call(self.port, "POST", "/api/student/attempt", body, cookie=self.cookie)

    def test_problems_and_progress_need_a_session(self):
        status, _, _, _ = call(self.port, "GET", "/api/student/problems")
        self.assertEqual(status, 401)
        status, _, _, _ = call(self.port, "GET", "/api/student/progress")
        self.assertEqual(status, 401)
        status, body, _, resp = call(self.port, "GET", "/api/student/problems", cookie=self.cookie)
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 2)
        self.assertEqual(resp.getheader("Cache-Control"), "no-store")

    def test_solved_is_computed_by_the_server(self):
        status, body, _, _ = self.attempt("p01", 2, 2)
        self.assertEqual(status, 200)
        self.assertTrue(body["solved"])
        status, body, _, _ = self.attempt("p02", 2, 3)
        self.assertFalse(body["solved"])
        status, body, _, _ = self.attempt("p02", 3, 3, blocked=True)
        self.assertFalse(body["solvedNow"], "a blocked run cannot pass")

    def test_claims_that_do_not_fit_the_problem_are_refused(self):
        status, body, _, _ = self.attempt("p02", 1, 1)
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "total_mismatch")
        status, body, _, _ = self.attempt("p02", 5, 3)
        self.assertEqual(status, 400)
        status, body, _, _ = call(self.port, "POST", "/api/student/attempt",
                                  {"problemId": "p99", "code": "x", "passed": 1, "total": 1, "revision": 1},
                                  cookie=self.cookie)
        self.assertEqual(body["error"], "unknown_problem")
        status, body, _, _ = self.attempt("p01", 2, 2, code="x" * (ta.MAX_CODE + 1))
        self.assertEqual(body["error"], "code_too_long")

    def test_progress_is_private_to_each_student(self):
        self.attempt("p01", 2, 2, code="print('Hello')")
        status, body, _, _ = call(self.port, "GET", "/api/student/progress", cookie=self.cookie)
        self.assertTrue(body["progress"]["p01"]["solved"])
        self.assertEqual(body["progress"]["p01"]["lastCode"], "print('Hello')")
        call(self.port, "POST", "/api/student/logout", {}, cookie=self.cookie)
        other = self.register(phone=OTHER_PHONE, national=OTHER_NATIONAL, name=OTHER_NAME)
        status, body, _, _ = call(self.port, "GET", "/api/student/progress", cookie=other)
        self.assertEqual(body["progress"], {})

    def test_flags_for_inserted_text_and_pasted_solutions(self):
        status, body, _, _ = self.attempt("p01", 2, 2, code="print('a')\n" * 12, typed=5, inserted=40)
        self.assertIn("inserted", body["flags"])
        status, body, _, _ = self.attempt("p02", 1, 3, code="def square(x):\n    return x * x\n" * 3, typed=0)
        self.assertIn("no_typing", body["flags"])

    def test_draft_keeps_code_and_hint_level(self):
        status, _, _, _ = call(self.port, "POST", "/api/student/draft", {
            "problemId": "p02", "code": "def f(x):\n    return x * x\n", "hintLevel": 1, "typed": 20, "inserted": 0,
            "revision": 1}, cookie=self.cookie)
        self.assertEqual(status, 200)
        status, body, _, _ = call(self.port, "GET", "/api/student/progress", cookie=self.cookie)
        self.assertEqual(body["progress"]["p02"]["lastCode"], "def f(x):\n    return x * x\n")
        self.assertEqual(body["progress"]["p02"]["hintLevel"], 1)
        self.assertFalse(body["progress"]["p02"]["solved"])

    def test_draft_refuses_unknown_problems_and_bad_numbers(self):
        status, body, _, _ = call(self.port, "POST", "/api/student/draft",
                                  {"problemId": "p01; DROP", "code": "x"}, cookie=self.cookie)
        self.assertEqual(status, 400)
        status, body, _, _ = call(self.port, "POST", "/api/student/draft",
                                  {"problemId": "p01", "code": "x", "typed": "many"}, cookie=self.cookie)
        self.assertEqual(body["error"], "bad_number")


class RevisionTests(Base):
    """Progress belongs to a question's id. Only a new revision (a major edit) starts it again."""

    def setUp(self):
        super().setUp()
        self.cookie = self.register()

    def solve(self, pid, total, revision):
        status, body, _, _ = call(self.port, "POST", "/api/student/attempt", {
            "problemId": pid, "code": "print(1)", "passed": total, "total": total, "revision": revision},
            cookie=self.cookie)
        return status, body

    def progress(self):
        status, body, _, _ = call(self.port, "GET", "/api/student/progress", cookie=self.cookie)
        self.assertEqual(status, 200)
        return body["progress"]

    def listed(self):
        status, body, _, _ = call(self.port, "GET", "/api/student/problems", cookie=self.cookie)
        return [p["id"] for p in body]

    def test_questions_added_in_the_middle_and_at_the_end_keep_progress(self):
        self.assertTrue(self.solve("p01", 2, 1)[1]["solved"])
        middle = {"id": "p015", "number": 2, "title": "جدید", "mode": "stdio", "revision": 1,
                  "tests": [{"stdin": "", "stdout": "x\n"}]}
        end = {"id": "p103", "number": 9, "title": "پایان", "mode": "stdio", "revision": 1,
               "tests": [{"stdin": "", "stdout": "y\n"}]}
        problems = base_fixture()
        use_problems([problems[0], middle, problems[1], end])
        self.assertEqual(self.listed(), ["p01", "p015", "p02", "p103"])
        progress = self.progress()
        self.assertTrue(progress["p01"]["solved"], "the solved question keeps its mark")
        self.assertNotIn("p015", progress)
        self.assertTrue(self.solve("p02", 3, 1)[1]["solved"], "old questions still accept answers")
        self.assertTrue(self.solve("p103", 1, 1)[1]["solved"], "new questions work at once")

    def test_minor_edits_keep_progress(self):
        self.solve("p01", 2, 1)
        problems = base_fixture()
        problems[0].update({"title": "سلام به همه", "guide": "متن تازه", "hints": ["سرنخ تازه"],
                            "starter": "print()", "statement": "متن دیگر"})
        use_problems(problems)
        progress = self.progress()
        self.assertTrue(progress["p01"]["solved"])
        self.assertEqual(progress["p01"]["revision"], 1)

    def test_major_edit_resets_only_that_question(self):
        self.solve("p01", 2, 1)
        self.solve("p02", 3, 1)
        problems = base_fixture()
        problems[0]["tests"].append({"stdin": "Reza\n", "stdout": "Hello, Reza\n"})
        problems[0]["revision"] = 2
        use_problems(problems)
        progress = self.progress()
        self.assertFalse(progress["p01"]["solved"], "the changed question starts again")
        self.assertEqual(progress["p01"]["revision"], 2)
        self.assertTrue(progress["p02"]["solved"], "the other question keeps its mark")
        self.assertEqual(progress["p02"]["revision"], 1)
        history = self.db().execute("SELECT COUNT(*) FROM attempts WHERE problem_id = 'p01'").fetchone()[0]
        self.assertEqual(history, 1, "the earlier attempt stays in the history for the teacher")

    def test_attempts_for_an_old_revision_are_refused(self):
        self.solve("p01", 2, 1)
        problems = base_fixture()
        problems[0]["tests"].append({"stdin": "Reza\n", "stdout": "Hello, Reza\n"})
        problems[0]["revision"] = 2
        use_problems(problems)
        status, body = self.solve("p01", 3, 1)
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "problem_updated")
        status, body = self.solve("p01", 3, 2)
        self.assertEqual(status, 200)
        self.assertTrue(body["solved"])

    def test_code_is_kept_across_a_major_edit(self):
        call(self.port, "POST", "/api/student/draft", {
            "problemId": "p01", "code": "name = input()\n", "revision": 1}, cookie=self.cookie)
        problems = base_fixture()
        problems[0]["revision"] = 2
        use_problems(problems)
        progress = self.progress()
        self.assertEqual(progress["p01"]["lastCode"], "name = input()\n")

    def test_removed_question_keeps_its_progress_and_returns_with_it(self):
        self.solve("p02", 3, 1)
        use_problems([base_fixture()[0]])
        self.assertTrue(self.progress()["p02"]["solved"], "the row stays while the question is away")
        use_problems(base_fixture())
        self.assertTrue(self.progress()["p02"]["solved"], "and it counts again when the question returns")

    def test_guide_is_released_only_after_a_pass_and_locked_again_after_a_major_edit(self):
        status, raw, _, _ = call(self.port, "GET", "/api/student/problems", cookie=self.cookie)
        self.assertNotIn(b"SECRET", json.dumps(raw).encode("utf-8"))
        status, body, _, _ = call(self.port, "GET", "/api/student/problems", cookie=self.cookie)
        self.assertFalse(any("guide" in p or "solutions" in p or "mistakes" in p for p in body))
        status, body, _, _ = call(self.port, "GET", "/api/student/guide?problemId=p01", cookie=self.cookie)
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "locked")
        self.solve("p01", 2, 1)
        status, body, _, _ = call(self.port, "GET", "/api/student/guide?problemId=p01", cookie=self.cookie)
        self.assertEqual(status, 200)
        self.assertEqual(body["guide"], "SECRET-GUIDE-TEXT")
        self.assertEqual(body["solutions"], [{"code": "SECRET-SOLUTION"}])
        problems = base_fixture()
        problems[0]["tests"].append({"stdin": "Reza\n", "stdout": "Hello, Reza\n"})
        problems[0]["revision"] = 2
        use_problems(problems)
        status, body, _, _ = call(self.port, "GET", "/api/student/guide?problemId=p01", cookie=self.cookie)
        self.assertEqual(status, 403, "after a major edit the guide waits for a new pass")


class TransportTests(Base):
    def test_cross_site_writes_are_refused(self):
        status, body, _, _ = call(self.port, "POST", "/api/student/login",
                                  {"phone": PHONE, "password": PASSWORD}, origin="https://evil.example")
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "bad_origin")
        status, body, _, _ = call(self.port, "POST", "/api/student/login", origin=ORIGIN,
                                  raw=b"phone=09123456789", content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, 415)

    def test_bad_json_and_huge_bodies_are_refused(self):
        status, body, _, _ = call(self.port, "POST", "/api/student/login", raw=b"{not json")
        self.assertEqual(status, 400)
        status, body, _, _ = call(self.port, "POST", "/api/student/login", raw=b"[]")
        self.assertEqual(status, 400)
        status, body, _, _ = call(self.port, "POST", "/api/student/login", raw=b"{" + b"a" * (ta.MAX_BODY + 1))
        self.assertEqual(status, 413)

    def test_cookies_are_http_only_and_strict(self):
        self.register()
        _, _, cookies, _ = call(self.port, "POST", "/api/student/login", {"phone": PHONE, "password": PASSWORD})
        cookie = [c for c in cookies if c.startswith(ta.STUDENT_COOKIE)][0]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Strict", cookie)
        self.assertIn("Path=/", cookie)
        ta.CONFIG["secure_cookies"] = True
        try:
            self.assertIn("Secure", ta.cookie_header("x", "y", 10, "/"))
        finally:
            ta.CONFIG["secure_cookies"] = False

    def test_rate_limit_on_registration(self):
        for _ in range(10):
            status, _, _, _ = call(self.port, "POST", "/api/student/register", {"phone": "1"})
            self.assertEqual(status, 400)
        status, body, _, _ = call(self.port, "POST", "/api/student/register", {"phone": "1"})
        self.assertEqual(status, 429)

    def test_unknown_paths_and_methods(self):
        self.assertEqual(call(self.port, "GET", "/api/nothing")[0], 404)
        self.assertEqual(call(self.port, "PUT", "/api/student/login", {})[0], 405)
        self.assertEqual(call(self.port, "GET", "/index.html")[0], 404)
        self.assertEqual(call(self.port, "GET", "/playground/data/problems.json")[0], 404)


class AdminTests(Base):
    def test_admin_api_needs_the_admin_cookie(self):
        self.assertEqual(call(self.port, "GET", "/api/admin/students")[0], 401)
        cookie = self.register()
        self.assertEqual(call(self.port, "GET", "/api/admin/students", cookie=cookie)[0], 401,
                         "a student session is not an admin session")

    def test_admin_lock_after_wrong_passwords(self):
        for _ in range(ta.ADMIN_MAX_FAILURES):
            status, _, _, _ = call(self.port, "POST", "/api/admin/login", {"password": "not-the-password"})
            self.assertEqual(status, 401)
        status, body, _, _ = call(self.port, "POST", "/api/admin/login", {"password": ADMIN_PASSWORD})
        self.assertEqual(status, 423)

    def test_list_detail_and_export(self):
        cookie = self.register()
        call(self.port, "POST", "/api/student/attempt",
             {"problemId": "p01", "code": "print('Hello, Ali')", "passed": 2, "total": 2, "revision": 1},
             cookie=cookie)
        admin = self.admin_cookie()
        status, body, _, _ = call(self.port, "GET", "/api/admin/students", cookie=admin)
        self.assertEqual(status, 200)
        row = body["students"][0]
        self.assertEqual(row["fullName"], NAME)
        self.assertEqual(row["solved"], 1)
        self.assertEqual(row["nationalCode"], NATIONAL)
        sid = row["id"]
        status, detail, _, _ = call(self.port, "GET", f"/api/admin/students/{sid}", cookie=admin)
        self.assertEqual(detail["attempts"][0]["code"], "print('Hello, Ali')")
        self.assertEqual(detail["attempts"][0]["revision"], 1)
        self.assertEqual(detail["progress"][0]["problemId"], "p01")
        status, _, _, _ = call(self.port, "GET", "/api/admin/students/999", cookie=admin)
        self.assertEqual(status, 404)
        status, raw, _, resp = call(self.port, "GET", "/api/admin/export.csv", cookie=admin)
        self.assertTrue(raw.startswith("﻿".encode("utf-8")))
        self.assertIn(NAME.encode("utf-8"), raw)
        self.assertIn("attachment", resp.getheader("Content-Disposition"))
        status, audit, _, _ = call(self.port, "GET", "/api/admin/audit", cookie=admin)
        self.assertIn("login", [e["action"] for e in audit["entries"]])

    def test_search_is_parameterised(self):
        self.register()
        admin = self.admin_cookie()
        status, body, _, _ = call(self.port, "GET",
                                  "/api/admin/students?q=" + "%27%20OR%201%3D1%20--", cookie=admin)
        self.assertEqual(status, 200)
        self.assertEqual(body["students"], [])
        status, body, _, _ = call(self.port, "GET", "/api/admin/students?q=" + "%25", cookie=admin)
        self.assertEqual(status, 200)
        self.assertEqual(self.db().execute("SELECT COUNT(*) FROM students").fetchone()[0], 1)

    def test_csv_cannot_run_formulas(self):
        self.assertEqual(ta.csv_safe("=HYPERLINK()"), "'=HYPERLINK()")
        self.assertEqual(ta.csv_safe("علی"), "علی")

    def test_passwords_are_not_stored_in_plain_text(self):
        self.register()
        self.login()
        with open(os.environ["TA_DB"], "rb") as handle:
            raw = handle.read()
        self.assertNotIn(PASSWORD.encode(), raw)
        self.assertNotIn(ADMIN_PASSWORD.encode(), raw)
        stored = self.db().execute("SELECT password_hash FROM students").fetchone()[0]
        self.assertTrue(stored.startswith("scrypt$"))


class JalaliTests(unittest.TestCase):
    def test_known_dates(self):
        from datetime import date
        from teacher_schedule import gregorian_to_jalali, jalali_plain, parse_tehran
        self.assertEqual(gregorian_to_jalali(date(2024, 3, 20)), (1403, 1, 1))
        self.assertEqual(gregorian_to_jalali(date(2025, 3, 21)), (1404, 1, 1))
        self.assertEqual(gregorian_to_jalali(date(2026, 11, 21)), (1405, 8, 30))
        # 22:00 Tehran is 18:30 UTC (Tehran has no daylight saving time)
        self.assertEqual(parse_tehran("2026-11-16T22:00").strftime("%H:%M"), "18:30")
        self.assertEqual(jalali_plain(parse_tehran("2026-11-21T22:00")), "1405/08/30 22:00")


class ScheduleTests(Base):
    """Deadlines per class: a first pass counts only if it came on or before the deadline."""

    def setUp(self):
        super().setUp()
        schedule = {"classes": {"201": {"packs": [
            {"id": "open", "title": "باز", "until": "2099-01-01T00:00", "problems": ["p01"],
             "markdown": "### باز"},
            {"id": "closed", "title": "سری", "until": "2000-01-01T00:00", "problems": ["p02"]},
        ]}}}
        path = Path(TMP) / "schedule.json"
        path.write_text(json.dumps(schedule, ensure_ascii=False), encoding="utf-8")
        ta.CONFIG["schedule"] = path
        ta.load_schedule()
        self.cookie = self.register()

    def attempt(self, cookie, pid, passed, total, code="print('ok')", revision=1):
        return call(self.port, "POST", "/api/student/attempt", {
            "problemId": pid, "code": code, "passed": passed, "total": total, "revision": revision},
            cookie=cookie)

    def test_pass_before_deadline_is_scored_and_after_is_not(self):
        status, body, _, _ = self.attempt(self.cookie, "p01", 2, 2)
        self.assertTrue(body["scored"])
        status, body, _, _ = self.attempt(self.cookie, "p02", 3, 3)
        self.assertTrue(body["solved"])
        self.assertFalse(body["scored"], "after the deadline the pass is practice only")
        progress = call(self.port, "GET", "/api/student/progress", cookie=self.cookie)[1]["progress"]
        self.assertTrue(progress["p01"]["scored"])
        self.assertFalse(progress["p02"]["scored"])
        self.assertTrue(progress["p02"]["solved"], "the question stays open for practice")
        self.assertIn("deadlineText", progress["p01"])

    def test_submission_log_shows_percent_class_time_and_code(self):
        self.attempt(self.cookie, "p01", 1, 2, code="print('half')")
        admin = self.admin_cookie()
        subs = call(self.port, "GET", "/api/admin/submissions", cookie=admin)[1]["submissions"]
        self.assertEqual(subs[0]["percent"], 50.0)
        self.assertEqual(subs[0]["class"], "201")
        self.assertEqual(subs[0]["code"], "print('half')")
        self.assertTrue(subs[0]["onTime"])
        self.assertTrue(subs[0]["at"].endswith("Z"))
        filtered = call(self.port, "GET", "/api/admin/submissions?class=202", cookie=admin)[1]["submissions"]
        self.assertEqual(filtered, [])
        raw = call(self.port, "GET", "/api/admin/submissions.csv", cookie=admin)[1]
        import re
        self.assertTrue(re.search(rb"\d{4}/\d{2}/\d{2} \d{2}:\d{2}", raw))
        self.assertIn(b"print('half')", raw)

    def test_students_see_their_packs_and_the_panel_sees_all(self):
        status, body, _, _ = call(self.port, "GET", "/api/student/schedule", cookie=self.cookie)
        self.assertEqual(body["classCode"], "201")
        self.assertEqual([pk["id"] for pk in body["packs"]], ["closed", "open"])
        self.assertEqual(body["packs"][1]["questions"][0]["id"], "p01")
        admin = self.admin_cookie()
        status, body, _, _ = call(self.port, "GET", "/api/admin/schedule", cookie=admin)
        self.assertIn("201", body["classes"])
        self.attempt(self.cookie, "p01", 2, 2)
        listed = call(self.port, "GET", "/api/admin/students", cookie=admin)[1]["students"][0]
        self.assertEqual(listed["scored"], 1)

    def test_a_class_without_a_schedule_only_practises(self):
        status, _, cookies, _ = call(self.port, "POST", "/api/student/register", {
            "phone": OTHER_PHONE, "nationalCode": OTHER_NATIONAL, "classCode": "202",
            "fullName": OTHER_NAME, "password": "sara1234"})
        self.assertEqual(status, 201)
        other = cookie_value(cookies, ta.STUDENT_COOKIE)
        body = self.attempt(other, "p01", 2, 2)[1]
        self.assertTrue(body["solved"])
        self.assertFalse(body["scored"])

    def test_schedule_file_must_match_the_questions(self):
        with self.assertRaises(ValueError):
            ta.Schedule if False else __import__("teacher_schedule").Schedule(
                {"classes": {"201": {"packs": [{"id": "x", "title": "x", "until": "2099-01-01T00:00",
                                               "problems": ["p99"]}]}}}, {"p01"})
        with self.assertRaises(ValueError):
            __import__("teacher_schedule").Schedule(
                {"classes": {"201": {"packs": [
                    {"id": "a", "title": "a", "until": "2099-01-01T00:00", "problems": ["p01"]},
                    {"id": "b", "title": "b", "until": "2099-01-01T00:00", "problems": ["p01"]}]}}}, {"p01"})


class ClassChangeTests(Base):
    """The teacher moves a student to the other class (201 or 202); the change is recorded."""

    def test_teacher_changes_the_class_and_it_is_recorded(self):
        cookie = self.register()
        admin = self.admin_cookie()
        sid = self.db().execute("SELECT id FROM students").fetchone()[0]
        status, body, _, _ = call(self.port, "POST", f"/api/admin/students/{sid}/class",
                                  {"classCode": "202"}, cookie=admin)
        self.assertEqual(status, 200, body)
        self.assertEqual(call(self.port, "GET", "/api/student/schedule", cookie=cookie)[1]["classCode"], "202")
        listed = call(self.port, "GET", "/api/admin/students", cookie=admin)[1]["students"][0]
        self.assertEqual(listed["classCode"], "202")
        audit = call(self.port, "GET", "/api/admin/audit", cookie=admin)[1]["entries"]
        self.assertTrue(any(e["action"] == "class-change" and "201 -> 202" in e["target"] for e in audit))

    def test_only_201_or_202_is_accepted(self):
        self.register()
        admin = self.admin_cookie()
        sid = self.db().execute("SELECT id FROM students").fetchone()[0]
        for bad in ("200", "203", "", None):
            status, body, _, _ = call(self.port, "POST", f"/api/admin/students/{sid}/class",
                                      {"classCode": bad}, cookie=admin)
            self.assertEqual(status, 400, bad)
            self.assertEqual(body["error"], "class_invalid")

    def test_class_change_needs_the_admin(self):
        cookie = self.register()
        sid = self.db().execute("SELECT id FROM students").fetchone()[0]
        status, _, _, _ = call(self.port, "POST", f"/api/admin/students/{sid}/class",
                               {"classCode": "202"}, cookie=cookie)
        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main(verbosity=2)
