#!/usr/bin/env python3
"""Convert the grade-11 website-design textbook PDF into markdown files.

The InDesign PDF stores Persian in visual order and encodes the lam-alef
ligature backwards (اطالعات instead of اطلاعات). This script rebuilds reading
order, fixes that ligature, and saves the book's figure screenshots.
"""

from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path

import pymupdf

PDF_PATH = Path(
    "/root/Storage/teacher/11th-grade/original-reference/11th-grade-programming-book.pdf"
)
OUT_DIR = Path("/root/Storage/teacher/11th-grade/converted-markdown-book")

ALEF_LIKE = set("اأإآٱ")
LAM = "ل"
HAIR = "\u200a"
ZWNJ = "\u200c"

# ASCII punctuation that belongs to an embedded English/code run.
ASCII_PUNCT = set(".,;:!?()[]{}<>+-=*/\\_'\"#@$%^&|~`")

CALLOUTS = {
    "نکته",
    "فعالیت",
    "مثال",
    "کنجکاوی",
    "بیشتر بدانید",
    "کار کارگاهی",
    "استاندارد عملکرد",
    "ارزشیابی",
    "ارزشيابي",
    "توضیحات کدها",
    "توضیحات",
    "کاربرد",
    "مراحل کار",
}

MODULE_DIRS = [
    "01-poodman-1-python",
    "02-poodman-2-static-web",
    "03-poodman-3-interactive-web",
    "04-poodman-4-python-oop",
    "05-poodman-5-django",
]
UNIT_SLUGS = [
    ["01-data-modeling", "02-functions-and-modules"],
    ["01-html", "02-css"],
    ["01-bootstrap", "02-javascript"],
    ["01-object-oriented", "02-object-oriented-development"],
    ["01-create-web-app", "02-develop-web-app"],
]

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def is_arabic_letter(ch: str) -> bool:
    return len(ch) == 1 and unicodedata.category(ch) == "Lo" and "\u0600" <= ch <= "\u06ff"


def is_strong_ltr(ch: str) -> bool:
    if len(ch) != 1:
        return False
    if ch.isascii() and ch.isalnum():
        return True
    return "\u06f0" <= ch <= "\u06f9"  # Persian digits


def is_strong_rtl(ch: str) -> bool:
    if len(ch) != 1:
        return False
    o = ord(ch)
    if ch in (HAIR, ZWNJ, "\u200d", "\u0640"):
        return True
    if 0x0600 <= o <= 0x06FF or 0x0750 <= o <= 0x077F:
        return not is_strong_ltr(ch)
    if 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF:
        return True
    return False


def is_ligature_alef(char: dict) -> bool:
    bb = char["bbox"]
    return char["c"] in ALEF_LIKE and abs(bb[2] - bb[0]) < 0.4


def fix_ligatures(chars: list[dict]) -> list[dict]:
    """Turn a zero-width alef + lam pair into logical lam-alef at the lam's x."""
    out = []
    i = 0
    while i < len(chars):
        c = chars[i]
        nxt = chars[i + 1] if i + 1 < len(chars) else None
        if nxt and is_ligature_alef(c) and nxt["c"] == LAM:
            out.append({"text": LAM + c["c"], "x": nxt["origin"][0]})
            i += 2
            continue
        if nxt and c["c"] == LAM and is_ligature_alef(nxt):
            out.append({"text": LAM + nxt["c"], "x": c["origin"][0]})
            i += 2
            continue
        ch = c["c"]
        if ch in ("\u200b", "\ufeff", "\u00ad"):
            i += 1
            continue
        out.append({"text": ch, "x": c["origin"][0]})
        i += 1
    return out


def _reverse_inner_ltr(island: list[str]) -> list[str]:
    """Reverse English words in place and leave parentheses where they are."""
    n = len(island)
    kind = []
    for ch in island:
        if is_strong_ltr(ch):
            kind.append("L")
        elif ch in "()":
            kind.append("P")
        else:
            kind.append("N")
    out: list[str] = []
    i = 0
    while i < n:
        if kind[i] != "L":
            out.append(island[i])
            i += 1
            continue
        j = i
        while j < n and kind[j] != "P":
            if kind[j] == "N":
                k = j
                while k < n and kind[k] == "N":
                    k += 1
                if k < n and kind[k] == "L":
                    j = k
                    continue
                # Keep «.py» and «_blank» with the word.
                if j < n and island[j] in "._":
                    j += 1
                break
            j += 1
        prefix: list[str] = []
        if out and out[-1] == ":" and j - i <= 2:
            prefix.append(out.pop())
        out.extend(reversed(prefix + island[i:j]))
        i = j
    return out


def restore_ltr(text: str) -> str:
    """Text is in right-to-left order. Put embedded English and code back."""
    chars = list(text)
    n = len(chars)
    rtl = [is_strong_rtl(ch) for ch in chars]
    out: list[str] = []
    i = 0
    while i < n:
        if rtl[i]:
            out.append(chars[i])
            i += 1
            continue
        j = i
        while j < n and not rtl[j]:
            j += 1
        island = chars[i:j]
        if not any(is_strong_ltr(ch) for ch in island):
            out.extend(island)
            i = j
            continue
        core = "".join(island).strip()
        leading = len(island) - len("".join(island).lstrip())
        trailing = len(island) - len("".join(island).rstrip())
        # A whole English phrase that was stored backwards, including its brackets.
        backwards = (
            core.startswith(")")
            or (core.startswith(">") and core.endswith("<"))
            or "ptth" in core  # a reversed http/https URL
        )
        if backwards:
            restored = list(reversed(core))
        else:
            restored = _reverse_inner_ltr(list(core))
        out.extend(island[:leading])
        out.extend(restored)
        out.extend(island[len(island) - trailing :] if trailing else [])
        i = j
    return fix_mirrored_parens("".join(out))


def fix_mirrored_parens(text: str) -> str:
    """Markdown has no bidi mirroring, so show the parentheses a reader expects."""
    text = re.sub(
        r"\)([A-Za-z][A-Za-z0-9_ .+\-]*)\(",
        lambda m: "(" + m.group(1).strip() + ")",
        text,
    )
    text = re.sub(
        r">(/?[A-Za-z][A-Za-z0-9]*)<",
        lambda m: "<" + m.group(1) + ">",
        text,
    )
    return text


def normalize_persian(text: str) -> str:
    chars = list(text)
    out: list[str] = []
    for i, ch in enumerate(chars):
        if ch == HAIR:
            prev = chars[i - 1] if i else ""
            nxt = chars[i + 1] if i + 1 < len(chars) else ""
            if is_arabic_letter(prev) and is_arabic_letter(nxt):
                out.append(ZWNJ)
            continue
        if ch == "\u0640":  # tatweel used to justify lines
            continue
        if ch == "\u064a":  # Arabic yeh -> Persian
            ch = "\u06cc"
        elif ch == "\u0643":  # Arabic kaf -> Persian
            ch = "\u06a9"
        out.append(ch)
    text = "".join(out)
    if any("\ufb50" <= ch <= "\ufeff" for ch in text):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\u064a", "\u06cc").replace("\u0643", "\u06a9")
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(rf"{ZWNJ}{{2,}}", ZWNJ, text)
    return text.strip()


def line_to_text(line: dict) -> str:
    chars = []
    for span in line["spans"]:
        chars.extend(span["chars"])
    if not chars:
        return ""
    tokens = fix_ligatures(chars)
    tokens.sort(key=lambda t: -t["x"])
    raw = "".join(t["text"] for t in tokens)
    return normalize_persian(restore_ltr(raw))


def span_style(line: dict) -> tuple[float, str]:
    if not line["spans"]:
        return 0.0, ""
    span = line["spans"][0]
    return float(span.get("size") or 0), span.get("font") or ""


def heading_level(text: str, size: float, font: str) -> int:
    t = text.strip().rstrip(":：")
    if size >= 24 and "پودمان" in text:
        return 1
    if size >= 22:
        return 2
    if size >= 16 and ("واحد یادگیری" in text or "Titr" in font):
        return 2
    if "Titr" in font and size >= 13.5 and len(text) <= 100:
        return 3
    if t in CALLOUTS and len(text) <= 40:
        return 3
    return 0


def is_running_header(text: str, y0: float, size: float) -> bool:
    return y0 < 105 and size <= 15 and text.startswith("پودمان") and ":" in text


def is_page_number(text: str, y0: float) -> bool:
    return y0 > 690 and bool(re.fullmatch(r"[0-9۰-۹]{1,3}", text.strip()))


def is_code_line(text: str) -> bool:
    if len(text) < 6:
        return False
    # Dotted leaders in the table of contents are not code.
    if text.count(".") + text.count("…") > len(text) * 0.25:
        return False
    letters = sum(1 for ch in text if ch.isascii() and ch.isalpha())
    code = sum(1 for ch in text if ch.isascii() and not ch.isspace())
    return letters >= 4 and code / len(text) > 0.55


def mostly_ascii(text: str) -> bool:
    if not text.strip():
        return False
    ascii_chars = sum(1 for ch in text if ch.isascii() and not ch.isspace())
    return ascii_chars / len(text.strip()) > 0.7


def ends_sentence(text: str) -> bool:
    return text.rstrip().endswith((".", "؟", "!", ":", "؛", "…"))


def is_list_start(text: str) -> bool:
    return bool(re.match(r"^[\d۰-۹]+([.)]|[.)]\s|\s+\S)", text))


def protect_inline(text: str) -> str:
    """Backtick Latin tokens so underscores do not start Markdown emphasis."""

    def repl(match: re.Match[str]) -> str:
        token = match.group(0)
        if re.search(r"[A-Za-z]", token):
            return f"`{token}`"
        return token

    return re.sub(r"[A-Za-z0-9_./\\:+#@$%^*=<>\-\[\]'\"|]+", repl, text)


def fa_num(value: str) -> str:
    return value.translate(FA_DIGITS)


def keep_image(bbox: tuple[float, float, float, float]) -> bool:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    if w > 540 and h > 680:
        return False
    # Drop the small نکته / فعالیت badges. Keep code strips, which are wide.
    if w >= 85 or h >= 55:
        return True
    return False


def extract_page(doc: pymupdf.Document, index: int, image_dir: Path) -> list[dict]:
    page = doc[index]
    raw = page.get_text("rawdict")
    items: list[dict] = []

    for block in raw["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            text = line_to_text(line)
            if not text:
                continue
            size, font = span_style(line)
            bb = line["bbox"]
            items.append(
                {
                    "kind": "text",
                    "text": text,
                    "size": size,
                    "font": font,
                    "x0": bb[0],
                    "y0": bb[1],
                    "x1": bb[2],
                    "y1": bb[3],
                    "level": heading_level(text, size, font),
                }
            )

    image_i = 0
    seen_boxes: list[tuple[float, float, float, float]] = []
    for info in page.get_image_info(xrefs=True):
        bb = tuple(info["bbox"])
        if not keep_image(bb):
            continue
        if any(abs(bb[0] - o[0]) < 2 and abs(bb[1] - o[1]) < 2 and abs(bb[2] - o[2]) < 2 for o in seen_boxes):
            continue
        seen_boxes.append(bb)
        clip = pymupdf.Rect(bb) & page.rect
        if clip.is_empty or clip.width < 8 or clip.height < 8:
            continue
        image_i += 1
        name = f"p{index + 1:03d}-{image_i:02d}.png"
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip, alpha=False)
        pix.save(image_dir / name)
        items.append(
            {
                "kind": "image",
                "text": "",
                "path": f"images/{name}",
                "x0": bb[0],
                "y0": bb[1],
                "x1": bb[2],
                "y1": bb[3],
                "level": 0,
                "size": 0,
                "font": "",
            }
        )

    items.sort(key=lambda it: (round(it["y0"], 0), -it["x0"]))
    return items


def page_to_markdown(items: list[dict], pdf_page: int) -> list[str]:
    book_page = ""
    body = []
    for item in items:
        if item["kind"] == "text" and is_page_number(item["text"], item["y0"]):
            book_page = item["text"]
            continue
        if item["kind"] == "text" and is_running_header(item["text"], item["y0"], item["size"]):
            continue
        body.append(item)

    if not book_page:
        # Content pages of this PDF are 6 pages ahead of the printed number.
        if pdf_page > 6:
            book_page = str(pdf_page - 6)

    lines: list[str] = []
    label = fa_num(book_page or str(pdf_page))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"<!-- pdf-page: {pdf_page} | book-page: {book_page or '?'} -->")
    lines.append("")
    lines.append(f"**صفحه {label}**")
    lines.append("")

    # Join wrapped body lines into paragraphs, then emit.
    texts = [it for it in body if it["kind"] == "text"]

    def is_side_image(image: dict) -> bool:
        for text in texts:
            if text["y1"] < image["y0"] - 4 or text["y0"] > image["y1"] + 4:
                continue
            if text["x0"] >= image["x1"] - 15 or text["x1"] <= image["x0"] + 15:
                return True
        return False

    paragraphs: list[dict] = []
    held_images: list[dict] = []
    for item in body:
        if item["kind"] == "image":
            if is_side_image(item):
                held_images.append(item)
                continue
            paragraphs.extend(held_images)
            held_images = []
            paragraphs.append(item)
            continue
        if item["level"] or item["size"] >= 16:
            paragraphs.extend(held_images)
            held_images = []
            paragraphs.append(item)
            continue
        prev = paragraphs[-1] if paragraphs else None
        same_block = prev and (
            abs(prev["x1"] - item["x1"]) < 30 or abs(prev["x0"] - item["x0"]) < 30
        )
        can_join = (
            prev
            and prev["kind"] == "text"
            and not prev["level"]
            and prev["size"] < 16
            and not is_code_line(prev["text"])
            and not is_code_line(item["text"])
            and not mostly_ascii(prev["text"])
            and not mostly_ascii(item["text"])
            and not ends_sentence(prev["text"])
            and not is_list_start(item["text"])
            and same_block
            and item["y0"] - prev["y1"] < 12
            and abs(prev["size"] - item["size"]) < 2.5
        )
        if can_join:
            joiner = ""
            if prev["text"].endswith(ZWNJ) or item["text"].startswith(ZWNJ):
                joiner = ""
            elif prev["text"].endswith("-"):
                joiner = ""
            else:
                joiner = " "
            prev["text"] = prev["text"] + joiner + item["text"]
            prev["y1"] = max(prev["y1"], item["y1"])
            prev["x1"] = max(prev["x1"], item["x1"])
            prev["x0"] = min(prev["x0"], item["x0"])
            continue
        paragraphs.extend(held_images)
        held_images = []
        paragraphs.append(item)
    paragraphs.extend(held_images)

    # Attach the following شکل/جدول caption as image alt text.
    for i, item in enumerate(paragraphs):
        if item["kind"] != "image":
            continue
        alt = "تصویر کتاب"
        if i + 1 < len(paragraphs) and paragraphs[i + 1]["kind"] == "text":
            nxt = paragraphs[i + 1]["text"].strip()
            if re.match(r"^(شکل|جدول)\s*[0-9۰-۹]+", nxt):
                alt = nxt
        item["alt"] = alt

    code_buf: list[str] = []

    def flush_code() -> None:
        if not code_buf:
            return
        lines.append("```")
        lines.extend(code_buf)
        lines.append("```")
        lines.append("")
        code_buf.clear()

    for item in paragraphs:
        if item["kind"] == "image":
            flush_code()
            rel = item["path"]
            # Markdown files live in subfolders; front matter is at the root.
            lines.append(f"![{item['alt']}]({rel})")
            lines.append("")
            continue
        text = item["text"].strip()
        if not text:
            continue
        if item["level"]:
            flush_code()
            lines.append(f"{'#' * item['level']} {text}")
            lines.append("")
            continue
        if is_code_line(text):
            code_buf.append(text)
            continue
        flush_code()
        if re.match(r"^(شکل|جدول)\s*[0-9۰-۹]+$", text):
            lines.append(f"**{text}**")
            lines.append("")
            continue
        lines.append(protect_inline(text))
        lines.append("")

    flush_code()
    return lines


def rel_image_path(md_rel: str, image_path: str) -> str:
    """image_path is 'images/foo.png'. md_rel is the markdown path under OUT_DIR."""
    depth = md_rel.count("/")
    return ("../" * depth) + image_path


class Writer:
    def __init__(self) -> None:
        self.files: dict[str, list[str]] = {}
        self.order: list[str] = []
        self.current = "00-front-matter.md"
        self.module_i = -1
        self.unit_i = -1
        self.seen_toc = False
        self.titles: dict[str, str] = {}
        self._touch(self.current, "شناسنامه و مقدمه کتاب")

    def _touch(self, path: str, title: str) -> None:
        if path not in self.files:
            self.files[path] = [f"# {title}", ""]
            self.order.append(path)
            self.titles[path] = title

    def _switch(self, path: str, title: str) -> None:
        self._touch(path, title)
        self.current = path

    def add_page(self, pdf_page: int, md_lines: list[str], plain_for_split: list[dict]) -> None:
        for item in plain_for_split:
            if item["kind"] != "text":
                continue
            text = item["text"].strip()
            if not self.seen_toc and text == "فهرست" and item["y0"] < 200:
                self.seen_toc = True
                self._switch("00-toc.md", "فهرست")
            if item["level"] == 1 and "پودمان" in text and item["size"] >= 24:
                self.module_i += 1
                self.unit_i = -1
                folder = MODULE_DIRS[self.module_i] if self.module_i < len(MODULE_DIRS) else f"0{self.module_i + 1}-poodman"
                self._switch(f"{folder}/00-intro.md", text)
            elif item.get("level") == 2 and self.current in self.titles and self.titles[self.current].startswith("واحد یادگیری") and "واحد یادگیری" not in text and "پودمان" not in text:
                self.titles[self.current] = text
                self.files[self.current][0] = f"# {text}"
            elif "واحد یادگیری" in text and item["size"] >= 16:
                self.unit_i += 1
                folder = MODULE_DIRS[self.module_i] if 0 <= self.module_i < len(MODULE_DIRS) else "99-extra"
                slugs = UNIT_SLUGS[self.module_i] if 0 <= self.module_i < len(UNIT_SLUGS) else []
                slug = slugs[self.unit_i] if self.unit_i < len(slugs) else f"{self.unit_i + 1:02d}-unit"
                # Title is completed by the next large heading; start with this line.
                self._switch(f"{folder}/{slug}.md", text)
            elif text in ("منابع", "منابع:") and item["size"] >= 14 and pdf_page > 300:
                self._switch("06-references.md", "منابع")

        bucket = self.files[self.current]
        depth = self.current.count("/")
        prefix = "../" * depth
        for line in md_lines:
            if line.startswith("![") and "](images/" in line:
                line = line.replace("](images/", f"]({prefix}images/")
            bucket.append(line)

    def write(self) -> None:
        for rel, lines in self.files.items():
            path = OUT_DIR / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            # Drop a trailing pile of blank lines.
            text = "\n".join(lines).rstrip() + "\n"
            path.write_text(text, encoding="utf-8")


def write_readme(writer: Writer, page_count: int, image_count: int) -> None:
    rows = []
    for rel in writer.order:
        title = writer.titles.get(rel, rel)
        rows.append(f"- [{title}]({rel})")
    body = f"""# کتاب طراح سایت — پایه یازدهم

متن کتاب درسی «طراح سایت» (رشته شبکه و نرم‌افزار رایانه، پایه یازدهم) که از PDF به مارک‌داون تبدیل شده است.

- منبع: `original-reference/11th-grade-programming-book.pdf`
- تعداد صفحه‌های PDF: {page_count}
- تعداد تصویرهای استخراج‌شده: {image_count}

هر فایل درس، متن را به ترتیب کتاب دارد و بالای هر صفحه شمارهٔ صفحهٔ چاپی آمده است. شکل‌ها و نمونه کدهایی که در کتاب به‌صورت تصویر چاپ شده‌اند، همین‌جا کنار متن قرار گرفته‌اند.

## فایل‌ها

{chr(10).join(rows)}

## نکتهٔ تبدیل

در PDF این کتاب، ترکیب «لا» جابه‌جا ذخیره شده بود (مثلاً «اطالعات» به‌جای «اطلاعات») و ترتیب حروف فارسی هم برعکس بود. متن این پوشه آن را به فارسی خوانا برگردانده است. نمونه کدهای داخل محیط برنامه‌نویسی تصویر هستند، چون در خود کتاب به‌صورت عکس چاپ شده‌اند.
"""
    (OUT_DIR / "README.md").write_text(body, encoding="utf-8")


def self_test() -> None:
    assert restore_ltr("s + lrtc") == "ctrl + s"
    assert restore_ltr("yp.olleh_10gorp") == "prog01_hello.py"
    assert restore_ltr(":D") == "D:"
    assert restore_ltr(")x.3 nohtyP( ELDI") == "IDLE (Python 3.x)", restore_ltr(")x.3 nohtyP( ELDI")
    assert restore_ltr("(xatnys)") == "(syntax)"
    assert restore_ltr("(شکل 2).") == "(شکل 2)."
    assert restore_ltr("(پنجره llehS ELDI)") == "(پنجره IDLE Shell)"
    assert restore_ltr(">a<") == "<a>"
    assert restore_ltr("knalb_") == "_blank"
    assert restore_ltr("/moc.tcejorpognajd.scod//:sptth") == "https://docs.djangoproject.com/"
    sample = normalize_persian("می\u200aکند داده\u200aها")
    assert sample == "می‌کند داده‌ها", sample
    assert normalize_persian("تــعاملی") == "تعاملی"


def main() -> None:
    self_test()
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    image_dir = OUT_DIR / "images"
    image_dir.mkdir(parents=True)

    doc = pymupdf.open(PDF_PATH)
    writer = Writer()
    image_count = 0
    for index in range(doc.page_count):
        items = extract_page(doc, index, image_dir)
        image_count += sum(1 for it in items if it["kind"] == "image")
        md_lines = page_to_markdown(items, index + 1)
        writer.add_page(index + 1, md_lines, items)
        if (index + 1) % 20 == 0 or index + 1 == doc.page_count:
            print(f"page {index + 1}/{doc.page_count}", flush=True)

    writer.write()
    write_readme(writer, doc.page_count, image_count)
    print("files", len(writer.order))
    print("images", image_count)
    for rel in writer.order:
        print(" ", rel)


if __name__ == "__main__":
    main()
