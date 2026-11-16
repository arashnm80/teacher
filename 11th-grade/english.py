#!/usr/bin/env python3
"""English twin of every lesson section.

The Persian slice of a section (from converted-markdown-book/, cut by
outline.py) is split into translatable pieces: paragraphs, headings, list
items, captions, and table cells. Code, images, page markers, and table
layout are copied as they are. Translations live in a translation memory,
``sections/translations-en.json``, keyed by the Persian text, so a rebuild
reuses every piece that did not change.

    python3 english.py pending      # write sections/pending-en.json (untranslated pieces)
    python3 english.py merge FILE   # add {"<key>": "English"} pairs from FILE to the memory
    python3 english.py build        # write sections/en/<id>.md (fails if a piece is missing)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEMORY = ROOT / "sections" / "translations-en.json"
PENDING = ROOT / "sections" / "pending-en.json"
EN_DIR = ROOT / "sections" / "en"

ARABIC = re.compile(r"[؀-ۿ]")
FA_TO_ASCII = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

LABELS = {
    "نکته": "Note",
    "توجه": "Attention",
    "فعالیت": "Activity",
    "کنجکاوی": "Curiosity",
    "کار کارگاهی": "Workshop",
    "مثال": "Example",
    "بیشتر بدانید": "Learn more",
    "پروژه": "Project",
    "پانویس": "Footnotes",
    "ادامه": "continued",
}

CAPTION_RE = re.compile(r"^(شکل|جدول)\s*([0-9۰-۹]+)(?::\s*(.*))?$")


def key_of(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def load_memory() -> dict[str, dict]:
    if MEMORY.is_file():
        return json.loads(MEMORY.read_text(encoding="utf-8"))
    return {}


def save_memory(memory: dict[str, dict]) -> None:
    MEMORY.parent.mkdir(parents=True, exist_ok=True)
    MEMORY.write_text(
        json.dumps(dict(sorted(memory.items())), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


class Translator:
    """Walks a Persian section and either collects or fills its pieces."""

    def __init__(self, memory: dict[str, dict], collect: bool) -> None:
        self.memory = memory
        self.collect = collect
        self.pending: dict[str, str] = {}
        self.missing = 0

    def text(self, fa: str) -> str:
        fa = fa.strip()
        if not fa or not ARABIC.search(fa):
            return fa.translate(FA_TO_ASCII) if fa and not ARABIC.search(fa) else fa
        label = re.fullmatch(r"\*\*([^*]+)\*\*", fa)
        if label and label.group(1).strip() in LABELS:
            return f"**{LABELS[label.group(1).strip()]}**"
        cont = re.fullmatch(r"\*\*(.+) \(ادامه\)\*\*", fa)
        if cont and cont.group(1).strip() in LABELS:
            return f"**{LABELS[cont.group(1).strip()]} (continued)**"
        cap = CAPTION_RE.match(fa.strip("*"))
        if cap:
            word = "Figure" if cap.group(1) == "شکل" else "Table"
            head = f"{word} {cap.group(2).translate(FA_TO_ASCII)}"
            if not cap.group(3):
                return f"*{head}*" if fa.startswith("*") else head
            rest = self.text(cap.group(3))
            out = f"{head}: {rest}"
            return f"*{out}*" if fa.startswith("*") else out
        key = key_of(fa)
        hit = self.memory.get(key)
        if hit and hit.get("fa") == fa:
            return hit["en"]
        if self.collect:
            self.pending[key] = fa
        self.missing += 1
        return fa  # not translated yet: show the Persian until it is

    def block(self, lines: list[str]) -> list[str]:
        """Translate a run of markdown lines (no quote prefix)."""
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("```"):
                j = i + 1
                while j < len(lines) and not lines[j].startswith("```"):
                    j += 1
                out.extend(lines[i : j + 1])
                i = j + 1
                continue
            if line.startswith(">"):
                j = i
                inner = []
                while j < len(lines) and lines[j].startswith(">"):
                    inner.append(lines[j][2:] if lines[j].startswith("> ") else lines[j][1:])
                    j += 1
                for l in self.block(inner):
                    out.append(("> " + l) if l else ">")
                i = j
                continue
            out.append(self.line(line))
            i += 1
        return out

    def line(self, line: str) -> str:
        if not line.strip() or line.startswith("<!--"):
            return line
        m = re.match(r"^(#{1,6} )(.*)$", line)
        if m:
            return m.group(1) + self.text(m.group(2))
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
        if m:
            return f"![{self.text(m.group(1))}]({m.group(2)})"
        m = re.match(r"^(\*[^*].*?\*)( — (.*))?$", line)
        if m and CAPTION_RE.match(m.group(1).strip("*")):
            cap = self.text(m.group(1))
            return cap + (f" — {self.text(m.group(3))}" if m.group(3) else "")
        if line.startswith("|"):
            if re.fullmatch(r"\|( --- \|)+", line):
                return line
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            done = []
            for c in cells:
                parts = c.split("<br>")
                done.append("<br>".join(self.text(p) for p in parts))
            # Persian tables list the first column on the right; the
            # English table keeps the same column order.
            return "| " + " | ".join(done) + " |"
        m = re.match(r"^(- |\d+\. )(.*)$", line)
        if m:
            return m.group(1) + self.text(m.group(2))
        return self.text(line)


def sections() -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from build_site import section_markdown  # noqa: E402
    from outline import SECTIONS  # noqa: E402

    out = []
    for section in SECTIONS:
        if section.get("custom") or section["id"] == "toc":
            continue
        out.append({"id": section["id"], "en": section["en"], "fa": section_markdown(section)})
    return out


def translate_section(tr: Translator, fa_md: str) -> str:
    lines = fa_md.split("\n")
    # Title line «# ...» of the chapter file is not part of a slice.
    return "\n".join(tr.block(lines))


def cmd_pending() -> None:
    memory = load_memory()
    tr = Translator(memory, collect=True)
    order: list[str] = []
    for sec in sections():
        before = set(tr.pending)
        translate_section(tr, sec["fa"])
        order.extend(k for k in tr.pending if k not in before)
    rows = [{"key": k, "fa": tr.pending[k]} for k in dict.fromkeys(order)]
    PENDING.write_text(json.dumps(rows, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    words = sum(len(r["fa"].split()) for r in rows)
    print(f"pending pieces: {len(rows)} ({words} words) -> {PENDING}")


def cmd_merge(path: str) -> None:
    memory = load_memory()
    pending = {}
    if PENDING.is_file():
        pending = {r["key"]: r["fa"] for r in json.loads(PENDING.read_text(encoding="utf-8"))}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    added = 0
    for key, en in data.items():
        fa = pending.get(key) or memory.get(key, {}).get("fa")
        if fa is None:
            print(f"unknown key {key}")
            continue
        memory[key] = {"fa": fa, "en": en}
        added += 1
    save_memory(memory)
    print(f"merged {added}; memory has {len(memory)}")


def cmd_build() -> None:
    memory = load_memory()
    tr = Translator(memory, collect=False)
    EN_DIR.mkdir(parents=True, exist_ok=True)
    for sec in sections():
        body = translate_section(tr, sec["fa"])
        (EN_DIR / f"{sec['id']}.md").write_text(body.rstrip() + "\n", encoding="utf-8")
    print("English sections written to", EN_DIR)
    if tr.missing:
        print(f"note: {tr.missing} pieces still in Persian (run `python3 english.py pending`)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    {"pending": cmd_pending, "build": cmd_build}.get(sys.argv[1], lambda: None)() if sys.argv[1] != "merge" else cmd_merge(sys.argv[2])
