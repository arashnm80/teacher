#!/usr/bin/env python3
"""Relay for the playground's AI helper: fixed actions, two providers, free models.

Browser (a student's device, or the offline playground copy)
  -> https://teacher.arashnm80.ir/api/ai/ask     (nginx: TLS, CORS, rate limit)
  -> this process on 127.0.0.1                   (fixed prompts, limits, fallback)
  -> a WARP SOCKS proxy on this machine          (the only way out)
  -> OpenRouter or Groq (OpenAI-style chat API)

Rules kept here:
- Egress only through the WARP SOCKS proxies in config.json. Environment proxies
  are ignored. systemd allows loopback only (IPAddressAllow=localhost).
- The student's key arrives in the X-AI-Key header. It is used for the request
  and never stored or logged. Rate limits use a short hash of it.
- The prompt is one of three fixed actions, built here. The endpoint is not a
  general relay: nothing from the browser can choose a prompt or a URL.
- Models are tried in the order listed in config.json. A model-level failure
  (not found, busy, server error, timeout) moves on to the next model. A key-level
  failure (401, 403, 402) stops at once, because the next model would fail too.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx

CONFIG_PATH = Path(os.environ.get("TEACHER_AI_CONFIG", "/opt/teacher-ai/config.json"))
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
for _name, _cfg in CONFIG["providers"].items():
    _cfg["key_re"] = re.compile(_cfg["key_pattern"])

TRACE_URL = "https://www.cloudflare.com/cdn-cgi/trace"
MAX_BODY = 64 * 1024
LIMITS = {
    "title": 200,
    "topic": 100,
    "statement": 6000,
    "code": 6000,
    "samples": 3000,
    "stdin": 1500,
    "expected": 2000,
    "actual": 2000,
    "message": 2000,
    "kind": 20,
}
WARP_DOWN = "اتصال امن (WARP) برقرار نیست. بعداً دوباره امتحان کنید."

SYSTEM = """تو معلم صبور پایتون هستی. دانش‌آموز تازه پایتون را شروع کرده است.
همیشه به فارسی ساده پاسخ بده. نام‌ها و کدهای پایتون را انگلیسی بنویس و داخل بک‌تیک بگذار، مثل `input()`.
پاسخ کوتاه و مرتب باشد؛ از عنوان کوتاه یا فهرست استفاده کن."""

ACTIONS = {
    "explain_problem": (
        "مسئله را برای دانش‌آموز توضیح بده: ۱) خواسته‌ی مسئله را به زبان ساده بگو؛ "
        "۲) ورودی و خروجی را مشخص کن؛ ۳) اگر ایده‌ی حل مهم است، آن را گام‌به‌گام بگو. "
        "کد کامل حل مسئله را ننویس."
    ),
    "sample_io": (
        "سه نمونه ورودی و خروجی متفاوت برای این مسئله بنویس: یک ساده، یک معمولی، و یک حالت مرزی. "
        "خروجی هر نمونه باید دقیقاً با خواسته‌ی مسئله درست باشد. اگر مسئله تابع است، نمونه‌ها را "
        "به شکل فراخوانی تابع و مقدار برگشتی بنویس. کد حل مسئله ننویس."
    ),
    "review_answer": (
        "کد دانش‌آموز را با صورت مسئله بررسی کن. اگر آزمون رد شده داده شده، بگو خروجی دانش‌آموز "
        "با انتظار کجا فرق دارد. بگو کدام قسمت کد اشتباه است و چرا، و کدام قسمت درست است. "
        "به شماره خط اشاره کن. یک تا سه راهنمایی بده؛ برنامه‌ی کامل درست را ننویس."
    ),
}

SYSTEM_EN = """You are a patient Python teacher. The student has just started learning Python.
Always answer in simple English. Write Python names and code in English inside backticks, like `input()`.
Keep the answer short and tidy; use a short heading or a list."""

ACTIONS_EN = {
    "explain_problem": (
        "Explain the problem to the student: 1) say what the problem asks in simple words; "
        "2) point out the input and the output; 3) if the idea of the solution is important, give it step by step. "
        "Do not write the complete solution code."
    ),
    "sample_io": (
        "Write three different input and output samples for this problem: a simple one, a usual one and a boundary case. "
        "The output of each sample must be exactly right for what the problem asks. If the problem is a function, write "
        "the samples as a function call and its returned value. Do not write the solution code."
    ),
    "review_answer": (
        "Check the student's code against the problem statement. If a failed test is given, say where the student's "
        "output differs from the expected one. Say which part of the code is wrong and why, and which part is right. "
        "Point to the line number. Give one to three hints; do not write the complete correct program."
    ),
}

# Fixed English texts for the errors the relay gives (the Persian text is the key).
EN_ERRORS = {
    WARP_DOWN: "The secure connection (WARP) is not up. Try again later.",
    "این مدل خیلی دیر پاسخ داد.": "This model answered too slowly.",
    "پاسخ این مدل خوانده نشد.": "This model's answer could not be read.",
    "این مدل پاسخی نداد.": "This model gave no answer.",
    "کلید وارد شده نامعتبر است یا دسترسی ندارد.": "The key you entered is invalid or has no access.",
    "اعتبار حساب این کلید تمام شده است.": "The credit of this key's account has run out.",
    "این مدل الان پر است.": "This model is busy right now.",
    "این مدل در دسترس نیست.": "This model is not available.",
    "سرویس این مدل خطا داد.": "This model's service gave an error.",
    "هیچ‌کدام از مدل‌های این سرویس پاسخ ندادند. بعداً دوباره امتحان کنید.": "None of this service's models answered. Try again later.",
    "همه مدل‌های رایگان این سرویس الان پر هستند. چند دقیقه بعد دوباره امتحان کنید.": "All the free models of this service are busy right now. Try again in a few minutes.",
    "درخواست باید JSON باشد.": "The request must be JSON.",
    "درخواست خالی است.": "The request is empty.",
    "درخواست خیلی بزرگ است.": "The request is too big.",
    "اطلاعات درخواست کامل نیست.": "The request data is incomplete.",
    "این سرویس هوش مصنوعی پشتیبانی نمی‌شود.": "This AI service is not supported.",
    "درخواست‌ها زیاد است. چند دقیقه بعد دوباره امتحان کنید.": "There are too many requests. Try again in a few minutes.",
    "نوع درخواست پشتیبانی نمی‌شود.": "This kind of request is not supported.",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("teacher-ai")


def make_client(proxy_url: str) -> httpx.Client:
    return httpx.Client(
        proxy=proxy_url,
        trust_env=False,
        timeout=httpx.Timeout(CONFIG["attempt_timeout_seconds"], connect=15.0),
        follow_redirects=False,
    )


CLIENTS = [(url, make_client(url)) for url in CONFIG["warp_proxies"]]


class Window:
    """Sliding-window counter per name (a key hash or an IP). Keeps no secrets."""

    def __init__(self, limit: int, seconds: int) -> None:
        self.limit = limit
        self.seconds = seconds
        self.hits: dict[str, deque[float]] = {}
        self.lock = threading.Lock()

    def allow(self, name: str) -> bool:
        now = time.monotonic()
        with self.lock:
            q = self.hits.setdefault(name, deque())
            while q and now - q[0] > self.seconds:
                q.popleft()
            if len(q) >= self.limit:
                return False
            q.append(now)
            if len(self.hits) > 10000:
                self.hits = {k: v for k, v in self.hits.items() if v and now - v[-1] <= self.seconds}
            return True


PER_KEY = Window(CONFIG["rate"]["per_key"], CONFIG["rate"]["seconds"])
PER_IP = Window(CONFIG["rate"]["per_ip"], CONFIG["rate"]["seconds"])


def language(payload: object) -> str:
    """"en" when the page asked for English; anything else is Persian."""
    return "en" if isinstance(payload, dict) and payload.get("lang") == "en" else "fa"


def clip(value: object, name: str, lang: str = "fa") -> str:
    text = "" if value is None else str(value)
    limit = LIMITS[name]
    return text if len(text) <= limit else text[:limit] + (" …(cut)" if lang == "en" else " …(کوتاه شد)")


def samples_text(samples: object, lang: str = "fa") -> str:
    en = lang == "en"
    rows = []
    for i, sample in enumerate(samples if isinstance(samples, list) else [], 1):
        if not isinstance(sample, dict):
            continue
        call = sample.get("call")
        if call:
            args = ", ".join(json.dumps(a, ensure_ascii=False) for a in call.get("args") or [])
            rows.append(f"{i}) {'call' if en else 'فراخوانی'}: f({args}) → {json.dumps(call.get('expected'), ensure_ascii=False)}")
        else:
            rows.append(f"{i}) {'input' if en else 'ورودی'}: {sample.get('stdin', '')!r} | "
                        f"{'output' if en else 'خروجی'}: {sample.get('stdout', '')!r}")
        if len(rows) >= 6:
            break
    return clip("\n".join(rows) or ("(no sample recorded)" if en else "(نمونه‌ای ثبت نشده است)"), "samples", lang)


def build_messages(payload: dict) -> list[dict]:
    action = payload.get("action")
    if action not in ACTIONS:
        raise ValueError("unknown action")
    lang = language(payload)
    en = lang == "en"
    problem = payload.get("problem") or {}
    is_function = problem.get("mode") == "function"
    c = lambda value, name: clip(value, name, lang)  # noqa: E731
    if en:
        lines = [
            f"Problem: {c(problem.get('title'), 'title')}",
            f"Topic: {c(problem.get('topic'), 'topic')}",
            f"Kind of problem: {'function' if is_function else 'input and output'}",
        ]
    else:
        lines = [
            f"مسئله: {c(problem.get('title'), 'title')}",
            f"موضوع: {c(problem.get('topic'), 'topic')}",
            f"نوع مسئله: {'تابع' if is_function else 'ورودی و خروجی'}",
        ]
    if is_function and problem.get("functionName"):
        lines.append(f"{'Function name' if en else 'نام تابع'}: {c(problem.get('functionName'), 'topic')}")
    lines += ["Problem statement:" if en else "صورت مسئله:", c(problem.get("statement"), "statement")]
    if action == "sample_io":
        lines += ["", "The official samples of this problem:" if en else "نمونه‌های رسمی همین مسئله:",
                  samples_text(problem.get("samples"), lang)]
    if action == "review_answer":
        code = c(payload.get("code"), "code")
        lines += [
            "",
            "The student's code:" if en else "کد دانش‌آموز:",
            "```python",
            code if code.strip() else ("(no code has been written yet)" if en else "(هنوز کدی نوشته نشده است)"),
            "```",
        ]
        failure = payload.get("failure")
        if isinstance(failure, dict) and failure:
            if en:
                lines += [
                    "",
                    "The test that failed:",
                    f"Kind: {c(failure.get('kind'), 'kind')}",
                    f"Test number: {int(failure.get('index') or 0)}",
                    f"Input: {c(failure.get('stdin'), 'stdin')}",
                    f"Expected: {c(failure.get('expected'), 'expected')}",
                    f"The student's output: {c(failure.get('actual'), 'actual')}",
                    f"Error message: {c(failure.get('message'), 'message')}",
                ]
            else:
                lines += [
                    "",
                    "آزمونی که رد شده:",
                    f"نوع: {c(failure.get('kind'), 'kind')}",
                    f"شماره آزمون: {int(failure.get('index') or 0)}",
                    f"ورودی: {c(failure.get('stdin'), 'stdin')}",
                    f"انتظار: {c(failure.get('expected'), 'expected')}",
                    f"خروجی دانش‌آموز: {c(failure.get('actual'), 'actual')}",
                    f"پیام خطا: {c(failure.get('message'), 'message')}",
                ]
    system = (SYSTEM_EN + "\n\n" + ACTIONS_EN[action]) if en else (SYSTEM + "\n\n" + ACTIONS[action])
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n".join(lines)},
    ]


class Outcome:
    """One attempt: kind is "ok", "key" (stop), "model" (try the next model), or "warp" (stop)."""

    def __init__(self, kind: str, status: int, message: str = "", text: str = "") -> None:
        self.kind = kind
        self.status = status
        self.message = message
        self.text = text


def try_model(cfg: dict, key: str, model: str, messages: list[dict]) -> Outcome:
    body = {"model": model, "messages": messages, "max_tokens": CONFIG["max_tokens"], "temperature": 0.3}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", **cfg.get("headers", {})}
    for index, (_url, client) in enumerate(CLIENTS):
        try:
            response = client.post(cfg["url"], json=body, headers=headers)
        except httpx.TimeoutException:
            log.info("model %s timed out", model)
            return Outcome("model", 504, "این مدل خیلی دیر پاسخ داد.")
        except httpx.TransportError:
            log.info("WARP proxy %d not reachable", index)
            continue
        log.info("model %s status %d via WARP proxy %d", model, response.status_code, index)
        code = response.status_code
        if code == 200:
            try:
                content = response.json()["choices"][0]["message"]["content"]
            except (ValueError, KeyError, IndexError, TypeError):
                return Outcome("model", 502, "پاسخ این مدل خوانده نشد.")
            if isinstance(content, list):
                content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
            text = (content or "").strip()
            if not text:
                return Outcome("model", 502, "این مدل پاسخی نداد.")
            return Outcome("ok", 200, text=text)
        if code in (401, 403):
            return Outcome("key", 401, "کلید وارد شده نامعتبر است یا دسترسی ندارد.")
        if code == 402:
            return Outcome("key", 402, "اعتبار حساب این کلید تمام شده است.")
        if code == 429:
            return Outcome("model", 429, "این مدل الان پر است.")
        if code in (400, 404, 422):
            return Outcome("model", 404, "این مدل در دسترس نیست.")
        return Outcome("model", 502, "سرویس این مدل خطا داد.")
    return Outcome("warp", 503, WARP_DOWN)


def ask(provider: str, key: str, messages: list[dict]) -> tuple[int, dict]:
    cfg = CONFIG["providers"][provider]
    started = time.monotonic()
    last = Outcome("model", 502, "هیچ‌کدام از مدل‌های این سرویس پاسخ ندادند. بعداً دوباره امتحان کنید.")
    for model in cfg["models"]:
        if time.monotonic() - started > CONFIG["total_budget_seconds"] - CONFIG["attempt_timeout_seconds"]:
            break
        outcome = try_model(cfg, key, model, messages)
        if outcome.kind == "ok":
            return 200, {"answer": outcome.text, "model": model, "provider": provider}
        if outcome.kind in ("key", "warp"):
            return outcome.status, {"error": outcome.message}
        last = outcome
    if last.status == 429:
        return 429, {"error": "همه مدل‌های رایگان این سرویس الان پر هستند. چند دقیقه بعد دوباره امتحان کنید."}
    return 502, {"error": last.message}


_health = {"at": 0.0, "data": None}


def health() -> dict:
    now = time.monotonic()
    if _health["data"] is not None and now - _health["at"] < 60:
        return _health["data"]
    ok = False
    for _url, client in CLIENTS:
        try:
            text = client.get(TRACE_URL, timeout=15).text
        except httpx.HTTPError:
            continue
        if "warp=on" in text or "warp=plus" in text:
            ok = True
            break
    data = {
        "ok": ok,
        "providers": {name: {"label": cfg["label"], "models": len(cfg["models"])} for name, cfg in CONFIG["providers"].items()},
    }
    _health.update(at=now, data=data)
    return data


class Handler(BaseHTTPRequestHandler):
    server_version = "teacher-ai"
    sys_version = ""

    def log_message(self, fmt: str, *args: object) -> None:  # no bodies, no headers
        log.info("%s %s", self.command, self.path.split("?")[0])

    lang = "fa"  # set per request from the payload; errors follow it

    def send_json(self, status: int, data: dict) -> None:
        if self.lang == "en" and isinstance(data.get("error"), str):
            data = {**data, "error": EN_ERRORS.get(data["error"], data["error"])}
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path.split("?")[0] == "/api/ai/health":
            return self.send_json(200, health())
        return self.send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path.split("?")[0] != "/api/ai/ask":
            return self.send_json(404, {"error": "not found"})
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self.send_json(415, {"error": "درخواست باید JSON باشد."})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return self.send_json(400, {"error": "درخواست خالی است."})
        if length > MAX_BODY:
            return self.send_json(413, {"error": "درخواست خیلی بزرگ است."})
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self.send_json(400, {"error": "اطلاعات درخواست کامل نیست."})
        if not isinstance(payload, dict):
            return self.send_json(400, {"error": "اطلاعات درخواست کامل نیست."})
        self.lang = language(payload)
        provider = payload.get("provider")
        if provider not in CONFIG["providers"]:
            return self.send_json(400, {"error": "این سرویس هوش مصنوعی پشتیبانی نمی‌شود."})
        cfg = CONFIG["providers"][provider]
        key = (self.headers.get("X-AI-Key") or "").strip()
        if not cfg["key_re"].match(key):
            if self.lang == "en":
                return self.send_json(400, {"error": f"The {cfg['label']} key is not valid. Check the key again."})
            return self.send_json(400, {"error": f"کلید {cfg['label']} معتبر نیست. کلید را دوباره بررسی کنید."})
        ip = self.headers.get("X-Real-IP") or self.client_address[0]
        key_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        if not PER_IP.allow(ip) or not PER_KEY.allow(key_id):
            return self.send_json(429, {"error": "درخواست‌ها زیاد است. چند دقیقه بعد دوباره امتحان کنید."})
        try:
            messages = build_messages(payload)
        except (ValueError, TypeError):
            return self.send_json(400, {"error": "نوع درخواست پشتیبانی نمی‌شود."})
        status, data = ask(provider, key, messages)
        return self.send_json(status, data)


def main() -> None:
    port = int(CONFIG.get("port", 8787))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    names = ", ".join(f"{n}({len(c['models'])})" for n, c in CONFIG["providers"].items())
    log.info("listening on 127.0.0.1:%d; providers %s; %d WARP proxies", port, names, len(CLIENTS))
    server.serve_forever()


if __name__ == "__main__":
    main()
