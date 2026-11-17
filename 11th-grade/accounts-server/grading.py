"""Checking a student's code on the server.

The program runs in the sandbox of the judge service (judge-server/): the accounts service never
runs student code itself. The judge returns what the program printed or returned for each test; this
module compares that with the expected result, which never leaves the server for the hidden tests.

Same rules as the browser version had (playground/app/js/runner.js): the "must use / must not use"
rules, text compared after line endings are made alike, function results compared as values with a
small tolerance for decimals.
"""
import json
import os
import re
import socket
import math

SOCKET = os.environ.get("TA_JUDGE_SOCKET", "/run/teacher-judge/judge.sock")
CALL_TIMEOUT = 40.0
TIME_LIMIT = 2.0


class JudgeUnavailable(Exception):
    """The judge could not be reached or answered badly. `code` is "busy" or "down"."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def ask_judge(request: dict) -> dict:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(CALL_TIMEOUT)
            sock.connect(SOCKET)
            sock.sendall(json.dumps(request, ensure_ascii=False).encode("utf-8") + b"\n")
            data = b""
            while not data.endswith(b"\n"):
                chunk = sock.recv(1 << 16)
                if not chunk:
                    break
                data += chunk
                if len(data) > 8_000_000:
                    raise JudgeUnavailable("down")
        answer = json.loads(data.decode("utf-8"))
    except JudgeUnavailable:
        raise
    except (OSError, ValueError):
        raise JudgeUnavailable("down")
    if not isinstance(answer, dict) or not answer.get("ok"):
        code = answer.get("error") if isinstance(answer, dict) else None
        raise JudgeUnavailable("busy" if code == "busy" else "down")
    return answer


# --- the "must use / must not use" rules -----------------------------------------------------
# Tokens are matched on the code with strings and comments removed.

_NOISE = re.compile(r"""('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\"|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")""")
_COMMENT = re.compile(r"#.*")
KEYWORDS = {"for", "while", "if", "elif", "else", "def", "return", "import", "in", "not", "and", "or",
            "pass", "break", "continue"}


def strip_noise(source: str) -> str:
    return _COMMENT.sub("", _NOISE.sub('""', source or ""))


def token_pattern(token: str) -> "re.Pattern[str]":
    if token == "import":
        return re.compile(r"\bimport\b|\bfrom\b", re.ASCII)
    if token in KEYWORDS:
        return re.compile(r"\b" + re.escape(token) + r"\b", re.ASCII)
    # a call such as max( : not my_max( and not obj.max(
    return re.compile(r"(?<![\w.])" + re.escape(token) + r"\s*\(", re.ASCII)


def constraint_issues(source: str, constraints: dict | None) -> list[dict]:
    cleaned = strip_noise(source)
    issues = []
    for token in (constraints or {}).get("require", []):
        if not token_pattern(token).search(cleaned):
            issues.append({"type": "require", "token": token})
    for token in (constraints or {}).get("forbid", []):
        if token_pattern(token).search(cleaned):
            issues.append({"type": "forbid", "token": token})
    return issues


# --- comparing ---------------------------------------------------------------------------------

def normalize_newlines(text: object) -> str:
    return str("" if text is None else text).replace("\r\n", "\n").replace("\r", "\n")


def _number(v: object) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def deep_equal(a: object, b: object) -> bool:
    if _number(a) and _number(b):
        if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
            return True
        if a == b:
            return True
        try:
            return abs(a - b) <= 1e-9 * max(1, abs(a), abs(b))
        except (OverflowError, ValueError):
            return False
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(deep_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(deep_equal(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


def _plain(v: object) -> object:
    """Whole decimals print as integers, as they did in the browser (1.0 is shown as 1)."""
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
        return int(v)
    if isinstance(v, list):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    return v


def show_value(v: object) -> str:
    try:
        return json.dumps(_plain(v), ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError):
        return str(v)


# --- the whole check -------------------------------------------------------------------------

PROBLEM_MESSAGES = {  # codes the page turns into text in the chosen language
    "timeout": "timeout", "skipped": "timeout", "memory": "memory", "output": "output", "crash": "crash",
}


def visible_count(problem: dict) -> int:
    return len(problem.get("samples") or []) or 1


def grade(problem: dict, code: str, ask=None) -> dict:
    """The outcome of running `code` on every test of `problem`.

    Tests after the visible ones report only whether they passed (and an error text if the program
    crashed): their input and expected result stay on the server.
    """
    issues = constraint_issues(code, problem.get("constraints"))
    tests = problem["tests"]
    if issues:
        return {"blocked": True, "constraintIssues": issues, "passed": 0, "total": len(tests), "results": []}
    function = (problem.get("mode") or "stdio") == "function"
    request = {
        "problem": problem.get("id") or "",
        "mode": "function" if function else "stdio",
        "source": code,
        "functionName": problem.get("functionName") or "",
        "timeLimit": float(problem.get("timeLimit") or TIME_LIMIT),
        "tests": [
            ({"args": t["call"].get("args") or [], "kwargs": t["call"].get("kwargs") or {}} if function
             else {"stdin": t.get("stdin") or ""})
            for t in tests
        ],
    }
    ran = (ask or ask_judge)(request)["results"]
    shown = visible_count(problem)
    results = []
    for i, (test, run) in enumerate(zip(tests, ran), start=1):
        see = i <= shown
        item = {"index": i, "ok": False}
        status = run.get("status")
        if function:
            item["args"] = test["call"].get("args") or [] if see else None
        else:
            item["stdin"] = test.get("stdin") or "" if see else None
        if status == "error":
            item.update(kind="runtime", message=run.get("error") or "")
            if see:
                item["actual"] = run.get("stdout") or ""
        elif status != "ok":
            item.update(kind="runner", code=PROBLEM_MESSAGES.get(status, "crash"))
        elif function:
            expected = test["call"].get("expected")
            item.update(kind="function", ok=deep_equal(run.get("value"), expected))
            if see and not item["ok"]:
                item.update(expected=show_value(expected), actual=show_value(run.get("value")))
            if see:
                item["stdout"] = run.get("stdout") or ""
        else:
            expected = test.get("stdout") or ""
            actual = run.get("stdout") or ""
            item.update(kind="stdio", ok=normalize_newlines(expected) == normalize_newlines(actual))
            if see and not item["ok"]:
                item.update(expected=expected, actual=actual)
        item = {k: v for k, v in item.items() if v is not None}
        results.append(item)
    passed = sum(1 for r in results if r["ok"])
    return {"blocked": False, "constraintIssues": [], "passed": passed, "total": len(tests), "results": results}
