#!/usr/bin/env python3
"""Put extracted lesson markdown back into readable paragraphs.

The PDF extractor often drops diagram labels (list, str, float, box1, …)
between the words of a sentence, and it fences prose as code. This pass
repairs that structure. It does not rewrite the lesson. Real code stays
in fences.
"""

from __future__ import annotations

import re

ARABIC = re.compile(r"[\u0600-\u06FF]")
FENCE_RE = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.M | re.S)
CHIP_LINE = re.compile(r"^`([^`\n]+)`[ \t]*$")
CODE_MARK = re.compile(
    r"[=;{}<>\[\]]|^\s*(def |class |import |from |return |const |let |var |function |print\(|if |for |while )"
)
TOKEN_FIX = {
    "folat": "float",
    "felx": "flex",
    "felx-direction": "flex-direction",
    "felx-wrap": "flex-wrap",
    "disply": "display",
    "f loat": "float",
}
# Labels printed on a figure. The figure image already shows them.
FIGURE_LABELS = {
    "list", "str", "int", "set", "float", "tuple", "dict", "bool",
    "box1", "box2", "box3", "f loat",
}
# Persian glosses that were copied into the English transcription.
EN_GLOSS = {
    "گرد کردن عدد اعشاری": "rounds a decimal number",
    "محاسبه توان": "calculates a power",
    "بزرگ‌ترین عدد": "the largest number",
    "بزرگترین عدد": "the largest number",
    "کوچک‌ترین عدد": "the smallest number",
    "کوچکترین عدد": "the smallest number",
    "جمع چند عدد": "the sum of several numbers",
    "تبدیل به عدد صحیح": "converts to an integer",
    "تبدیل به عدد اعشاری": "converts to a floating-point number",
    "محاسبه قدرمطلق عدد": "calculates the absolute value of a number",
    "بنویسید": "write it",
}


def _fix_token(token: str) -> str:
    return TOKEN_FIX.get(token.strip(), token.strip())


def _is_figure_label(token: str) -> bool:
    return _fix_token(token).lower() in FIGURE_LABELS or token.strip().lower() in FIGURE_LABELS


def _looks_like_code(line: str) -> bool:
    stripped = line.strip()
    if CODE_MARK.search(stripped):
        return True
    return bool(re.match(r"^[:;]\s*[A-Za-z_]", stripped))


def _persian_outside_quotes(line: str) -> bool:
    stripped = re.sub(r"(['\"]).*?\1", "", line)
    return bool(ARABIC.search(stripped))


def _ends_sentence(text: str) -> bool:
    plain = re.sub(r"`[^`]*`", "", text).rstrip()
    return plain.endswith((".", "؟", "!", "؛", "…", ":", "»"))


def _is_structural(text: str) -> bool:
    s = text.strip()
    return (
        not s
        or s.startswith("#")
        or s.startswith("![")
        or s.startswith("**")
        or s.startswith("---")
        or s.startswith("<!--")
        or s.startswith("|")
        or s.startswith("- ")
        or s.startswith("* ")
        or bool(re.match(r"^\d+\s", s))
    )


def _translate_gloss(text: str, lang: str) -> str:
    if lang != "en":
        return text
    for fa, en in EN_GLOSS.items():
        text = text.replace(fa, en)
    text = ARABIC.sub("", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def _normalize_code_line(line: str) -> str:
    fixed = re.sub(r"^;(\s*)(?=[A-Za-z_-])", "", line.rstrip())
    if line.strip().startswith(";") and not fixed.rstrip().endswith(";"):
        fixed = fixed.rstrip() + ";"
    return fixed


def _code_statements(fragment: str) -> list[str]:
    parts = [p.strip().rstrip(",") for p in re.split(r"\s*,\s*(?=[A-Za-z_])", fragment) if p.strip()]
    return parts or [fragment.strip()]


def _split_fence(body: str, lang: str) -> list[tuple[str, str]]:
    """Return blocks: ('code', text) ('prose', text) ('chip', token)."""
    lines = [line for line in body.splitlines() if line.strip()]
    if not lines:
        return []
    if all(_is_figure_label(line.strip("`")) for line in lines):
        return [("chip", _fix_token(line.strip("`"))) for line in lines]
    if all(not _persian_outside_quotes(line) and _looks_like_code(line) for line in lines):
        return [("code", "\n".join(_normalize_code_line(line) for line in lines))]
    if not any(_persian_outside_quotes(line) or _looks_like_code(line) for line in lines):
        if all(" " not in line.strip() and len(line.strip()) < 40 for line in lines):
            return [("chip", _fix_token(line.strip("`"))) for line in lines]
        prose_lines: list[str] = []
        for line in lines:
            piece = line.strip()
            if piece.startswith(".") and prose_lines:
                prose_lines[-1] = prose_lines[-1].rstrip() + "."
                piece = piece[1:].lstrip()
            if piece:
                prose_lines.append(piece)
        prose = _translate_gloss(" ".join(prose_lines), lang)
        return [("prose", prose)] if prose else []

    out: list[tuple[str, str]] = []
    prose_bits: list[str] = []
    code_bits: list[str] = []

    def flush_prose() -> None:
        if prose_bits:
            prose = _translate_gloss(" ".join(prose_bits), lang)
            prose_bits.clear()
            if prose:
                out.append(("prose", prose))

    def flush_code() -> None:
        if code_bits:
            out.append(("code", "\n".join(code_bits)))
            code_bits.clear()

    for line in lines:
        if _persian_outside_quotes(line):
            flush_code()
            code_match = re.search(
                r"((?:[A-Za-z_][\w.]*\s*=\s*\S.*)|(?:[Pp]rint\s*\(.*\))\s*)$",
                line,
            )
            if code_match and ARABIC.search(line[: code_match.start()]):
                prose_bits.append(line[: code_match.start()].strip(" ،"))
                flush_prose()
                code_bits.extend(_code_statements(code_match.group(1)))
                flush_code()
                continue
            prose_bits.append(line.strip())
            continue
        if _looks_like_code(line):
            flush_prose()
            code_bits.append(_normalize_code_line(line))
            continue
        flush_code()
        prose_bits.append(line.strip())
    flush_code()
    flush_prose()
    return out


def _parse(text: str, lang: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            body = "\n".join(lines[i + 1 : j])
            blocks.extend(
                ("text", value) if kind == "prose" else (kind, value)
                for kind, value in _split_fence(body, lang)
            )
            i = j + 1 if j < len(lines) else j
            continue
        line = lines[i]
        chip = CHIP_LINE.match(line.strip())
        if chip and _is_figure_label(chip.group(1)):
            blocks.append(("chip", _fix_token(chip.group(1))))
        elif chip and len(chip.group(1)) < 28 and " " not in chip.group(1).strip() and not _looks_like_code(chip.group(1)):
            blocks.append(("chip", _fix_token(chip.group(1))))
        else:
            kind = "blank" if not line.strip() else "text"
            blocks.append((kind, line))
        i += 1
    return blocks


def _join_inline_codes(line: str) -> str:
    def once(current: str) -> str:
        def repl(match: re.Match[str]) -> str:
            left, right = match.group(1), match.group(2)
            if len(left) > 24 or len(right) > 24:
                return match.group(0)
            sep = "" if left[-1] in "+-./" or right[0] in "+-./" else " "
            return f"`{left}{sep}{right}`"

        return re.sub(r"`([^`\n]+)`[ \t]+`([^`\n]+)`", repl, current)

    current = line
    for _ in range(6):
        nxt = once(current)
        if nxt == current:
            return current
        current = nxt
    return current


def _fix_call_parens(line: str) -> str:
    # `)(`int` is the visual-order form of int(). Leave real calls alone.
    line = re.sub(
        r"\)\(`([A-Za-z_][\w.]*)`(?!\()",
        lambda m: f"`{m.group(1)}()`",
        line,
    )
    line = re.sub(r"`([A-Za-z_][\w.]*)`\(\)", lambda m: f"`{m.group(1)}()`", line)
    return line


def _smash_function_rows(line: str, lang: str) -> str:
    """name()description print(name(...)) was extracted as one line."""

    def repl(match: re.Match[str]) -> str:
        name, desc, args = match.group(1), match.group(2).strip(" :،.-"), match.group(3)
        desc = _translate_gloss(desc, lang)
        example = f"print({name}({args}))"
        if not desc:
            return f"`{example}`"
        return f"`{name}()` — {desc}\n\n`{example}`"

    line = re.sub(
        r"`([A-Za-z_][\w]*)`?\(\)`?\s*([^`]+?)`[Pp]rint`\(`\1`\(([^)]*)\)\)",
        repl,
        line,
    )
    def gloss(match: re.Match[str]) -> str:
        desc = match.group(2).strip(" :،.-")
        if desc.startswith("—"):
            return match.group(0)
        return f"`{match.group(1)}()` — {_translate_gloss(desc, lang)}"

    return re.sub(r"^`?([A-Za-z_][\w]*)`?\(\)`?\s*([^`]+)$", gloss, line)


def _attach_continuations(blocks: list[tuple[str, str]], lang: str) -> list[tuple[str, str]]:
    """Glue a short tail, such as «بنویسید.», back onto the sentence it finishes.

    A figure or a blank line may sit between the two halves. The figure stays
    where it is; the tail moves up to the unfinished line.
    """
    out: list[tuple[str, str]] = []
    index = 0
    while index < len(blocks):
        kind, value = blocks[index]
        if (
            kind != "text"
            or _is_structural(value)
            or _ends_sentence(value)
            or len(value.strip()) < 40
            or re.match(r"https?://\S+$", value.strip())
        ):
            out.append((kind, value))
            index += 1
            continue
        gap: list[tuple[str, str]] = []
        cursor = index + 1
        while cursor < len(blocks) and _can_skip(blocks[cursor]):
            gap.append(blocks[cursor])
            cursor += 1
        if cursor < len(blocks) and _is_tail(blocks[cursor][1]):
            tail = blocks[cursor][1].strip()
            if lang == "en" and tail.strip(" .") == "write it":
                base = value.rstrip()
                out.append(("text", base if base.endswith(".") else base + "."))
            else:
                out.append(("text", value.rstrip() + " " + tail))
            out.extend(gap)
            index = cursor + 1
            continue
        out.append((kind, value))
        index += 1
    return out


def _can_skip(block: tuple[str, str]) -> bool:
    kind, value = block
    if kind in {"blank", "chip"}:
        return True
    return kind == "text" and (_is_structural(value) or value.strip().startswith("!["))


def _fix_project_labels(lines: list[str], lang: str) -> list[str]:
    """The book's «پروژه» callout extracted as an orphan label.

    In Persian it sits alone on its line just above «پروژه آشپزباشی:».
    In English it glued itself to the end of the previous question and the
    title kept a stray leading colon (visual order). Merge each case into
    one real heading so the project is visible like every کنجکاوی/نکته box.
    """
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if lang == "fa" and stripped == "پروژه":
            out.append("### پروژهPLACEHOLDER")
            continue
        if lang == "en" and not stripped.startswith("#"):
            tail = re.sub(r"\s+Project\s*$", "", line.rstrip())
            if tail != line.rstrip():
                out.append(tail)
                out.append("### ProjectPLACEHOLDER")
                continue
        out.append(line)
    merged: list[str] = []
    for line in out:
        if line.strip() in {"### پروژهPLACEHOLDER", "### ProjectPLACEHOLDER"}:
            merged.append(line)
            continue
        if line.strip() == "" and merged and merged[-1].strip() in {
            "### پروژهPLACEHOLDER", "### ProjectPLACEHOLDER",
        }:
            merged.append(line)
            continue
        if (
            line.strip()
            and not _is_structural(line)
            and [m for m in merged if m.strip()]
            and [m for m in merged if m.strip()][-1].strip()
            in {"### پروژهPLACEHOLDER", "### ProjectPLACEHOLDER"}
        ):
            while merged and not merged[-1].strip():
                merged.pop()
            merged.pop()
            title = line.strip()
            if lang == "fa":
                title = re.sub(r"^پروژه\s*", "", title).rstrip(":").strip()
                merged.append(f"### پروژه: {title}" if title else "### پروژه")
            else:
                title = re.sub(r"^:?\s*", "", title)
                title = re.sub(r"^Project\s*", "", title, flags=re.I).rstrip(":").strip()
                title = re.sub(r"\s+project$", "", title, flags=re.I).strip()
                merged.append(f"### Project: {title}" if title else "### Project")
            continue
        merged.append(line)
    return [
        "### پروژه" if line.strip() == "### پروژهPLACEHOLDER"
        else "### Project" if line.strip() == "### ProjectPLACEHOLDER"
        else line
        for line in merged
    ]


def _is_tail(value: str) -> bool:
    tail = value.strip()
    if not tail or _is_structural(tail) or tail.startswith(("`", "!", "#", "http")):
        return False
    if tail.startswith(("مثال", "Example", "Figure", "شکل")):
        return False
    if _looks_like_code(tail) or re.fullmatch(r"\d+(?:\.\d+)?", tail):
        return False
    if ":" in tail:
        return False
    if re.fullmatch(r"[=<>+\-*/]+", tail):
        return False
    # Only a real leftover fragment, not the next cell of a broken table.
    if tail.startswith(("می‌", "می", "یا ", "or ", "to ", "of ", "and ")):
        return len(tail) <= 80
    return len(tail) <= 18


def repair_markdown(text: str, lang: str) -> str:
    current = text
    for _ in range(4):
        nxt = _repair_once(current, lang)
        if nxt == current:
            return current
        current = nxt
    return current


def _repair_once(text: str, lang: str) -> str:
    text = "\n".join(_fix_project_labels(text.splitlines(), lang)) + "\n"
    blocks = _parse(text, lang)
    merged: list[tuple[str, str]] = []
    i = 0
    while i < len(blocks):
        kind, value = blocks[i]
        if kind != "chip":
            merged.append((kind, value))
            i += 1
            continue
        j = i
        chips: list[str] = []
        while j < len(blocks) and blocks[j][0] in {"chip", "blank"}:
            if blocks[j][0] == "chip":
                chips.append(blocks[j][1])
            j += 1
        prev = merged[-1] if merged else None
        nxt = blocks[j] if j < len(blocks) else None
        interrupts = (
            prev
            and prev[0] == "text"
            and not _is_structural(prev[1])
            and not _ends_sentence(prev[1])
            and len(prev[1].strip()) >= 40
            and nxt
            and nxt[0] == "text"
            and not _is_structural(nxt[1])
        )
        if interrupts:
            # The labels were sitting in the middle of one sentence.
            i = j
            continue
        if chips and all(_is_figure_label(chip) for chip in chips):
            i = j
            continue
        separator = "، " if lang == "fa" else ", "
        if len(chips) >= 2:
            merged.append(("text", separator.join(f"`{chip}`" for chip in chips)))
        elif chips:
            merged.append(("text", f"`{chips[0]}`"))
        i = j

    merged = _attach_continuations(merged, lang)

    # Join a long line to the next line when figure labels used to split them
    # and the first line is still unfinished. A second pass catches that
    # because the chips are already gone, so the two halves are neighbors
    # only if nothing else stood between them. Re-scan raw blocks for pairs
    # that had only chips between them.
    joined_text = _render(merged)
    return _post(joined_text, lang, blocks)


def _pairs_split_by_chips(blocks: list[tuple[str, str]]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    last_text: str | None = None
    pending = False
    for kind, value in blocks:
        if kind == "chip":
            if last_text is not None:
                pending = True
            continue
        if kind == "blank":
            continue
        if kind == "text" and not _is_structural(value):
            if (
                pending
                and last_text is not None
                and not _ends_sentence(last_text)
                and len(last_text.strip()) >= 40
                and not re.match(r"https?://\S+$", last_text.strip())
                and _is_tail(value)
            ):
                pairs.add((last_text, value))
            last_text = value
            pending = False
        else:
            last_text = None
            pending = False
    return pairs


def _post(text: str, lang: str, original_blocks: list[tuple[str, str]]) -> str:
    pairs = _pairs_split_by_chips(original_blocks)
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines):
            # Allow a blank line between the two halves.
            nxt_i = i + 1
            if lines[nxt_i].strip() == "" and nxt_i + 1 < len(lines):
                nxt_i += 1
            if (lines[i], lines[nxt_i]) in pairs:
                out.append(lines[i].rstrip() + " " + lines[nxt_i].lstrip())
                i = nxt_i + 1
                continue
        out.append(lines[i])
        i += 1
    text = "\n".join(out)
    fixed_lines = []
    for line in text.splitlines():
        if line.startswith("```"):
            fixed_lines.append(line)
            continue
        assign = re.match(r"^`([A-Za-z_][\w]*)`\s*=\s*(\S.*?)\s*$", line)
        if assign:
            fixed_lines.extend(["```", f"{assign.group(1)} = {assign.group(2)}", "```"])
            continue
        line = _smash_function_rows(line, lang)
        line = _fix_call_parens(line)
        line = _join_inline_codes(line)
        line = re.sub(r"`([^`\n]+)`", lambda m: f"`{_fix_token(m.group(1))}`", line)
        fixed_lines.append(line)
    text = "\n".join(fixed_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text.endswith("\n"):
        text += "\n"
    return text


def _render(blocks: list[tuple[str, str]]) -> str:
    lines: list[str] = []
    for kind, value in blocks:
        if kind == "blank":
            lines.append("")
        elif kind == "code":
            lines.extend(["```", value, "```"])
        else:
            lines.append(value)
    return "\n".join(lines) + "\n"
