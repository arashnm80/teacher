"""Turn one PDF text line (glyphs in visual order) into logical order.

The book PDF stores every glyph where it is drawn. Reading a Persian line
means walking it right to left, except for runs of English words, digits,
and code, which read left to right. A run is everything from a strong
left-to-right character to the next one, as long as no Persian letter is in
between. A bracket that balances a bracket inside the run joins it, so
«IDLE (Python 3.x)» stays whole.
"""

from __future__ import annotations

import re
import unicodedata

ALEF_LIKE = set("اأإآٱ")
LAM = "ل"
OPEN, CLOSE = "([{<", ")]}>"


def is_mark(ch: str) -> bool:
    return unicodedata.category(ch) in ("Mn", "Me")


def is_arabic(ch: str) -> bool:
    if not ch:
        return False
    o = ord(ch[0])
    if 0x06F0 <= o <= 0x06F9 or 0x0660 <= o <= 0x0669:
        return False
    return (
        0x0600 <= o <= 0x06FF
        or 0x0750 <= o <= 0x077F
        or 0xFB50 <= o <= 0xFDFF
        or 0xFE70 <= o <= 0xFEFF
    )


def is_latin(ch: str) -> bool:
    return (ch.isascii() and ch.isalpha()) or ("À" <= ch <= "ɏ")


def _tokens(chars: list[dict]) -> list[dict]:
    toks: list[dict] = []
    marks: list[dict] = []
    i = 0
    n = len(chars)
    while i < n:
        c = chars[i]
        ch = c["c"]
        w = c["x1"] - c["x0"]
        nxt = chars[i + 1] if i + 1 < n else None
        # The lam-alef ligature: a zero-width alef stored next to the lam.
        if nxt and ch in ALEF_LIKE and w < 0.4 and nxt["c"] == LAM:
            toks.append(dict(nxt, t=LAM + ch, x=(nxt["x0"] + nxt["x1"]) / 2))
            i += 2
            continue
        if nxt and ch == LAM and nxt["c"] in ALEF_LIKE and nxt["x1"] - nxt["x0"] < 0.4:
            toks.append(dict(c, t=LAM + nxt["c"], x=(c["x0"] + c["x1"]) / 2))
            i += 2
            continue
        if ch in ("\u200b", "\ufeff", "\u00ad"):
            i += 1
            continue
        if is_mark(ch):
            marks.append(c)
            i += 1
            continue
        toks.append(dict(c, t=ch, x=(c["x0"] + c["x1"]) / 2))
        i += 1
    # A diacritic belongs to the Persian letter drawn under it.
    for m in marks:
        mx = (m["x0"] + m["x1"]) / 2
        letters = [t for t in toks if is_arabic(t["t"][0])]
        if not letters:
            continue
        best = min(letters, key=lambda t: abs(t["x"] - mx))
        best["t"] += m["c"]
    return toks


SUPERSCRIPTS = set("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079")


def _kind(tok: dict) -> str:
    ch = tok["t"][0]
    if ch in SUPERSCRIPTS:
        return "N"
    if is_latin(ch) or ch.isdigit():
        return "L"
    if is_arabic(ch) or ch in ("\u200c", "\u200d"):
        return "R"
    return "N"


def _ltr_base(toks: list[dict], kinds: list[str]) -> list[dict]:
    """Left-to-right line (code) holding Persian words: reverse each
    Persian run in place."""
    out = list(toks)
    n = len(toks)
    i = 0
    while i < n:
        if kinds[i] != "R":
            i += 1
            continue
        # Punctuation printed against the run's left edge ends the Persian
        # phrase («سلام دنیا!»).
        while i > 0 and kinds[i - 1] == "N" and toks[i - 1]["t"] in "!?.،:؛؟" and (i < 2 or kinds[i - 2] != "R"):
            i -= 1
        j = i
        k = i + 1
        while k < n and kinds[k] != "L":
            if kinds[k] == "R":
                j = k
            k += 1
        out[i : j + 1] = list(reversed(toks[i : j + 1]))
        i = j + 1
    for t in out:
        t["run"] = 1 if is_latin(t["t"][0]) or t["t"][0] in "<>/=\"'(){}[];:.-_#" else 0
    return out


def visual_to_logical_tokens(chars: list[dict], base: str | None = None) -> tuple[list[dict], str]:
    """Return (tokens in logical order, base direction 'R' or 'L').

    Tokens of one left-to-right run share a ``run`` number (1, 2, ...) if the
    run holds a Latin letter.
    """
    toks = _tokens(chars)
    if not toks:
        return [], "R"
    toks.sort(key=lambda t: t["x"])
    kinds = [_kind(t) for t in toks]
    if base == "L" and "R" in kinds:
        return _ltr_base(toks, kinds), "L"
    base = "R" if "R" in kinds else "L"
    forced = False
    if base == "L":
        # «<label>» or «1 <button>» printed in a Persian paragraph: the tag
        # brackets come out mirrored («>label<»), so the line is right-to-left.
        vis = "".join(t["t"] for t in toks).strip()
        if re.fullmatch(r">[^<>]*(?:>[^<>]*<[^<>]*)*<(?:\s+\d{1,2})?", vis):
            base = "R"
            forced = True
    if base == "L":
        latin = any(is_latin(t["t"][0]) for t in toks)
        for t in toks:
            t["run"] = 1 if latin else 0
        return toks, "L"
    n = len(toks)
    runs: list[list[int]] = []
    i = 0
    while i < n:
        if kinds[i] != "L":
            i += 1
            continue
        j = i
        k = i + 1
        while k < n and kinds[k] != "R":
            if kinds[k] == "L":
                j = k
            k += 1
        if forced:
            # «button<  1»: the item number is its own run.
            text = "".join(toks[x]["t"] for x in range(i, j + 1))
            m = re.search(r"\s+\d{1,2}$", text)
            if m and m.start() > 0:
                cut = i + len(text[: m.start()].rstrip())
                # tokens are single characters here
                last_letter = max(x for x in range(i, cut + 1) if kinds[x] == "L")
                runs.append([i, last_letter])
                first_digit = next(x for x in range(last_letter + 1, j + 1) if kinds[x] == "L")
                runs.append([first_digit, j])
                i = j + 1
                continue
        runs.append([i, j])
        i = j + 1
    for r in runs:
        changed = True
        while changed:
            changed = False
            text = "".join(toks[x]["t"] for x in range(r[0], r[1] + 1))
            for o, c in zip(OPEN, CLOSE):
                bal = text.count(o) - text.count(c)
                if bal > 0 and r[1] + 1 < n and toks[r[1] + 1]["t"] == c:
                    r[1] += 1
                    changed = True
                    break
                if bal < 0 and r[0] - 1 >= 0 and toks[r[0] - 1]["t"] == o:
                    r[0] -= 1
                    changed = True
                    break
    items: list[list[dict]] = []
    i = 0
    ri = 0
    run_no = 0
    while i < n:
        if ri < len(runs) and runs[ri][0] == i:
            s, e = runs[ri]
            group = toks[s : e + 1]
            if any(is_latin(t["t"][0]) for t in group):
                run_no += 1
                for t in group:
                    t["run"] = run_no
            items.append(group)
            i = e + 1
            ri += 1
        else:
            items.append([toks[i]])
            i += 1
    out: list[dict] = []
    for group in reversed(items):
        out.extend(group)
    return out, "R"


def visual_to_logical(chars: list[dict]) -> str:
    toks, _ = visual_to_logical_tokens(chars)
    return "".join(t["t"] for t in toks)
