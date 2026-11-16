"""Checks every playground solution before it ships.

A solution must:
- pass every test of its problem (stdio: exact stdout; function: returned value);
- satisfy the problem's constraints (require / forbid), same rule as app/js/runner.js;
- use only concepts taught in the book (BANNED list below);
- have Persian comments on its lines, Persian steps, and a Persian explanation.
"""
from __future__ import annotations

import contextlib
import io
import math
import re

PERSIAN = re.compile(r"[\u0600-\u06FF]")

KEYWORD_TOKENS = {"for", "while", "if", "elif", "else", "def", "return", "import",
                  "in", "not", "and", "or", "pass", "break", "continue"}

# Things the book does not teach in module 1 (see .claude/playground-expansion.md).
BANNED = {
    "try": r"\btry\b",
    "except": r"\bexcept\b",
    "lambda": r"\blambda\b",
    "enumerate": r"\benumerate\s*\(",
    "zip": r"\bzip\s*\(",
    "dict methods": r"\.(items|keys|values|get|setdefault|update)\s*\(",
    "set()": r"\bset\s*\(",
    "list()": r"(?<![\w.])list\s*\(",
    "dict()": r"(?<![\w.])dict\s*\(",
    "tuple()": r"(?<![\w.])tuple\s*\(",
    "None": r"\bNone\b",
    "is": r"\bis\b",
    "slice": r"\w\s*\[[^\]\n]*:[^\]\n]*\]",
    "negative index": r"\w\s*\[\s*-\s*\d",
    "reverse()": r"\.reverse\s*\(",
    "sort()": r"\.sort\s*\(",
    "count()": r"\.count\s*\(",
    "index()": r"\.index\s*\(",
    "join()": r"\.join\s*\(",
    "strip()": r"\.strip\s*\(",
    "replace()": r"\.replace\s*\(",
    "isdigit": r"\bisdigit\b",
    "floor/ceil/pi": r"\b(floor|ceil|pi)\b",
    "augmented assign": r"(\+=|-=|\*=|/=|//=|%=)",
    "star unpack": r"\(\s*\*",
    "set ops": r"\s[&|]\s",
    "f-string": r"(?<![\w])f[\"']",
    "not in": r"\bnot\s+\w+\s+in\b",
    "conditional expr": r"^(?!\s*(if|elif)\b).*\sif\b.*\belse\b",
    "del": r"\bdel\b",
    "class/self": r"\b(class|self)\b",
    "modules": r"\bimport\s+(json|pathlib|os|sys|time|turtle|copy)\b",
    "builtin ops": r"\b(map|filter|any|all|open|eval|exec)\s*\(",
    "sorted key": r"\bkey\s*=",
    "print sep/end": r"\b(sep|end)\s*=",
}


def strip_noise(src: str) -> str:
    """Remove strings (keep the quotes) and comments, like runner.js does."""
    src = re.sub(r"('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\"|'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")", '""', src)
    return re.sub(r"#.*", "", src)


def _esc(s: str) -> str:
    return re.escape(s)


def token_re(token: str):
    if token == "import":
        return re.compile(r"\bimport\b|\bfrom\b")
    if token in KEYWORD_TOKENS:
        return re.compile(r"\b%s\b" % _esc(token))
    return re.compile(r"(?<![\w.])%s\s*\(" % _esc(token))


def constraint_issues(src: str, constraints: dict | None) -> list[str]:
    c = constraints or {}
    cleaned = strip_noise(src)
    out = []
    for t in c.get("require", []):
        if not token_re(t).search(cleaned):
            out.append(f"باید «{t}» داشته باشد")
    for t in c.get("forbid", []):
        if token_re(t).search(cleaned):
            out.append(f"«{t}» ممنوع است")
    return out


def banned_hits(src: str) -> list[str]:
    cleaned = strip_noise(src)
    hits = []
    for name, pat in BANNED.items():
        if re.search(pat, cleaned, flags=re.M):
            hits.append(name)
    return hits


def _has_persian_comment(block: str) -> bool:
    return any("#" in l and PERSIAN.search(l.split("#", 1)[1]) for l in block.split("\n"))


def comment_sections(src: str) -> tuple[int, int, int]:
    """(commented sections, all sections, Persian comment lines).

    A section is a block of code separated from the next one by a blank line.
    Every section should explain itself in Persian (a comment on a line or above it).
    """
    blocks = [b for b in re.split(r"\n\s*\n", src.strip("\n")) if b.strip()]
    ok = sum(1 for b in blocks if _has_persian_comment(b))
    lines = sum(1 for l in src.split("\n") if "#" in l and PERSIAN.search(l.split("#", 1)[1]))
    return ok, len(blocks), lines


def _norm(v):
    if isinstance(v, tuple):
        return [_norm(x) for x in v]
    if isinstance(v, list):
        return [_norm(x) for x in v]
    if isinstance(v, dict):
        return {k: _norm(x) for k, x in v.items()}
    return v


def _equal(a, b) -> bool:
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k]) for k in a)
    return a == b


def run_stdio(code: str, stdin: str) -> str:
    buf = io.StringIO()
    old_in = __import__("sys").stdin
    import sys
    sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<solution>", "exec"), {"__name__": "__main__"})
    finally:
        sys.stdin = old_in
    return buf.getvalue()


def run_function(code: str, fname: str, args: list, kwargs: dict | None = None):
    ns: dict = {"__name__": "__main__"}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<solution>", "exec"), ns)
        if fname not in ns or not callable(ns[fname]):
            raise NameError(f"تابع {fname} تعریف نشده")
        return ns[fname](*args, **(kwargs or {})), buf.getvalue()


def check_solution(problem: dict, sol: dict) -> list[str]:
    errs = []
    code = sol["code"]
    try:
        compile(code, "<solution>", "exec")
    except SyntaxError as e:
        return [f"خطای نحوی: {e}"]
    errs += constraint_issues(code, problem.get("constraints"))
    hits = banned_hits(code)
    if hits:
        errs.append("مفهومی که در کتاب نیامده: " + "، ".join(hits))
    ok, sections, comment_lines = comment_sections(code)
    if ok < sections or comment_lines < 2:
        errs.append(f"توضیح فارسی: {ok} از {sections} بخش؛ هر بخش کد باید توضیح فارسی داشته باشد")
    for i, t in enumerate(problem["tests"]):
        try:
            if problem["mode"] == "stdio":
                got = run_stdio(code, t.get("stdin", ""))
                if got.replace("\r\n", "\n") != t["stdout"].replace("\r\n", "\n"):
                    errs.append(f"آزمون {i + 1}: خروجی {got!r} به جای {t['stdout']!r}")
            else:
                call = t["call"]
                val, _ = run_function(code, problem["functionName"], call.get("args", []), call.get("kwargs"))
                if not _equal(_norm(val), _norm(call["expected"])):
                    errs.append(f"آزمون {i + 1}: {val!r} به جای {call['expected']!r}")
        except Exception as e:  # noqa: BLE001 - report every failure
            errs.append(f"آزمون {i + 1}: خطا {type(e).__name__}: {e}")
            break
    return errs


REQUIRED = ["id", "number", "topic", "conceptId", "difficulty", "mode", "title",
            "statement", "starter", "hints", "samples", "tests", "guideTitle", "solutions"]


def check_problem(p: dict) -> list[str]:
    errs = []
    for k in REQUIRED:
        if k not in p:
            errs.append(f"فیلد {k} نیست")
    if errs:
        return errs
    if p["mode"] not in ("stdio", "function"):
        errs.append("mode نامعتبر")
    if p["mode"] == "function" and not p.get("functionName"):
        errs.append("functionName نیست")
    if not p["solutions"]:
        errs.append("هیچ راه‌حلی نیست")
    for s in p["solutions"]:
        for k in ("name", "steps", "code", "explain"):
            if not s.get(k):
                errs.append(f"راه‌حل «{s.get('name', '?')}»: {k} خالی است")
        if s.get("steps") and len(s["steps"]) < 2:
            errs.append(f"راه‌حل «{s['name']}»: کمتر از ۲ قدم")
        for para in s.get("explain", []):
            if not PERSIAN.search(para):
                errs.append(f"راه‌حل «{s['name']}»: توضیح باید فارسی باشد")
        errs += [f"راه‌حل «{s['name']}»: {e}" for e in check_solution(p, s)]
    return errs
