#!/usr/bin/env python3
"""Convert the grade-11 «طراح سایت» textbook PDF into markdown.

How the PDF is built (Adobe InDesign) and what this script does about it:

* Glyphs are stored in *visual* order. Each text line is rebuilt in logical
  order with a small inverse-bidi pass (``bidi.visual_to_logical``):
  Persian runs are reversed, English/number runs keep their left-to-right
  order, and a bracket that closes an English run stays with it.
* The lam-alef ligature is a zero-width alef next to a lam. It is rebuilt as
  «لا» (otherwise «اطلاعات» reads «اطالعات»).
* A hair space (U+200A) stands in for the zero-width non-joiner.
* Layout is read from the drawing layer, not guessed from text:
    - a tinted box with a dark badge in the right margin is a callout
      (نکته، فعالیت، کنجکاوی، ...);
    - a small orange square before a line is a sub-heading or a bold lead-in;
      a lighter, smaller one is a bullet; a dark-orange square holding a white
      digit is a numbered item;
    - a grid of ruled lines is a table;
    - images, frames, arrows, and the small labels printed on them are merged
      into one figure, cropped from the page as a single picture, and joined
      to its «شکل N» caption.
* Paragraphs are rebuilt from justified lines. A paragraph that runs over the
  page break is joined.

Run from anywhere (needs ``pymupdf``):  python3 convert_book.py
"""

from __future__ import annotations

import re
import shutil
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from bidi import is_arabic, visual_to_logical_tokens
from book_fixes import FIXES, IMAGE_CLIPS, IMAGE_MASKS, PAGE_OVERRIDES, REGEX_FIXES

ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "original-reference" / "11th-grade-programming-book.pdf"
OUT_DIR = ROOT / "converted-markdown-book"
IMG_DIR = OUT_DIR / "images"

HAIR = "\u200a"
ZWNJ = "\u200c"
SUPERSCRIPT = dict(zip("0123456789\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9", "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079" * 2))
ARABIC_INDIC = str.maketrans("\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669", "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9")
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
PDF_TO_BOOK_PAGE = 6  # printed page number = PDF page - 6

CALLOUT_LABELS = (
    "نکته", "فعالیت", "کنجکاوی", "بیشتر بدانید", "پروژه", "تمرین", "پرسش",
    "گفت\u200cوگو", "گفتگو", "هشدار", "کار کلاسی", "کار کارگاهی", "تحقیق", "یادآوری",
    "ایمنی", "مثال",
)

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


# ---------------------------------------------------------------- geometry

@dataclass
class Box:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def h(self) -> float:
        return self.y1 - self.y0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    def grow(self, d: float) -> "Box":
        return Box(self.x0 - d, self.y0 - d, self.x1 + d, self.y1 + d)

    def hits(self, o: "Box") -> bool:
        return self.x0 < o.x1 and o.x0 < self.x1 and self.y0 < o.y1 and o.y0 < self.y1

    def union(self, o: "Box") -> "Box":
        return Box(min(self.x0, o.x0), min(self.y0, o.y0), max(self.x1, o.x1), max(self.y1, o.y1))

    def contains_pt(self, x: float, y: float) -> bool:
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def xover(self, o: "Box") -> float:
        return max(0.0, min(self.x1, o.x1) - max(self.x0, o.x0))

    def yover(self, o: "Box") -> float:
        return max(0.0, min(self.y1, o.y1) - max(self.y0, o.y0))


def as_box(r) -> Box:
    return Box(float(r[0]), float(r[1]), float(r[2]), float(r[3]))


# ---------------------------------------------------------------- text lines

@dataclass
class Line:
    box: Box
    toks: list  # logical tokens: dict(t, bold, font, size, color)
    size: float
    font: str
    color: int
    base: str  # "R" or "L"
    used: bool = False
    marker: str = ""  # "", "head", "bullet", "num"
    raw_chars: list = field(default_factory=list)

    @property
    def text(self) -> str:
        return clean_text("".join(t["t"] for t in self.toks))

    @property
    def bold(self) -> bool:
        letters = [t for t in self.toks if not t["t"].isspace()]
        return bool(letters) and sum(t["bold"] for t in letters) >= 0.8 * len(letters)

    @property
    def latin_only(self) -> bool:
        return not any(is_arabic(t["t"][0]) for t in self.toks)


def clean_text(text: str) -> str:
    """Normalize Persian spelling artifacts of the PDF."""
    text = text.translate(ARABIC_INDIC)
    out = []
    chars = list(text)
    for i, ch in enumerate(chars):
        prev = chars[i - 1] if i else ""
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if ch == HAIR:
            # Hair space between two Persian letters is a ZWNJ; next to a
            # space it is just a gap.
            if prev and nxt and is_arabic(prev) and is_arabic(nxt):
                out.append(ZWNJ)
            elif prev and nxt and not prev.isspace() and not nxt.isspace():
                out.append(" " if not is_arabic(prev) or not is_arabic(nxt) else ZWNJ)
            continue
        if ch == "\u0640":  # tatweel: justification stretch or bullet
            if prev and nxt and prev.isascii() and nxt.isascii() and prev.isalnum() and nxt.isalnum():
                out.append("-")  # «open\u200c\u0640meteo» in a URL is a hyphen
            elif not prev or prev.isspace() or prev.isdigit() or prev in "۰۱۲۳۴۵۶۷۸۹":
                out.append("\u0640")  # a list dash, kept for the paragraph builder
            continue
        if ch == "\u064a":
            ch = "ی"
        elif ch == "\u0643":
            ch = "ک"
        elif ch == "\u00a0":
            ch = " "
        out.append(ch)
    text = "".join(out)
    if any("\ufb50" <= ch <= "\ufeff" for ch in text):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\u064a", "ی").replace("\u0643", "ک")
    text = text.replace("\u064b\u064b", "\u064b")  # doubled tanween «مثلا\u064b\u064b»
    text = re.sub("[ \u200c]+([\u2070\u00b9\u00b2\u00b3\u2074-\u2079]+)", r"\1", text)
    # «می دهد», «فایل های»: these join with a half-space (ZWNJ).
    text = re.sub(r"(?<![\u0600-\u06ff\u200c])(ن?می) (?=[\u0621-\u06cc]{2})", "\\1" + ZWNJ, text)
    text = re.sub(r"([\u0621-\u06cc]) (ها|های|هایی)(?=[\s،.):]|$)", "\\1" + ZWNJ + "\\2", text)
    text = re.sub(f"{ZWNJ}+", ZWNJ, text)
    text = re.sub(f" ?{ZWNJ} ?", lambda m: ZWNJ if m.group(0) == ZWNJ else " ", text)
    return text


def is_bold_font(font: str, flags: int) -> bool:
    return "Bold" in font or "Titr" in font or bool(flags & 16)


ROTATED: list[Box] = []


def read_lines(page: pymupdf.Page) -> list[Line]:
    raw = page.get_text(
        "rawdict",
        flags=pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_PRESERVE_LIGATURES | pymupdf.TEXT_MEDIABOX_CLIP,
    )
    frags = []
    for block in raw["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            chars = []
            for span in line["spans"]:
                bold = is_bold_font(span["font"], span["flags"])
                for c in span["chars"]:
                    chars.append(
                        {
                            "c": c["c"],
                            "x0": c["bbox"][0],
                            "x1": c["bbox"][2],
                            "y0": c["bbox"][1],
                            "y1": c["bbox"][3],
                            "bold": bold,
                            "font": span["font"],
                            "size": round(span["size"], 1),
                            "color": span["color"],
                            "base": c["origin"][1],
                        }
                    )
            if not "".join(c["c"] for c in chars).strip():
                continue
            if abs(line["dir"][1]) > 0.1:
                # Rotated text (a label inside an arrow) is part of a picture.
                ROTATED.append(as_box(line["bbox"]))
                continue
            # Split a line where an empty gap separates text of different
            # sizes (a badge label printed beside a sentence).
            xs = sorted(chars, key=lambda c: c["x0"])
            piece = [xs[0]]
            right = xs[0]["x1"]
            for c in xs[1:]:
                if c["x0"] - right > 5 and abs(c["size"] - piece[-1]["size"]) >= 1.6:
                    frags.append(_stream_order(piece, chars))
                    piece = []
                piece.append(c)
                right = max(right, c["x1"])
            frags.append(_stream_order(piece, chars))

    # Merge fragments that share a baseline and touch horizontally.
    frags.sort(key=lambda ch: (round(_baseline(ch)), -max(c["x1"] for c in ch)))
    merged: list[list[dict]] = []
    for chars in frags:
        for other in merged:
            if abs(_baseline(other) - _baseline(chars)) > 2.2:
                continue
            ox0 = min(c["x0"] for c in other)
            ox1 = max(c["x1"] for c in other)
            x0 = min(c["x0"] for c in chars)
            x1 = max(c["x1"] for c in chars)
            gap = max(x0 - ox1, ox0 - x1)
            if gap < 14 and abs(_main_size(other) - _main_size(chars)) < 1.6:
                other.extend(chars)
                break
        else:
            merged.append(list(chars))

    lines = []
    for chars in merged:
        main = _main_size(chars)
        for c in chars:
            if c["c"].isdigit() and c["size"] < main * 0.7 and main >= 11:
                c["c"] = SUPERSCRIPT.get(c["c"], c["c"])
        toks, base = visual_to_logical_tokens(chars)
        if not toks:
            continue
        box = Box(
            min(c["x0"] for c in chars if not c["c"].isspace() or True),
            min(c["y0"] for c in chars),
            max(c["x1"] for c in chars),
            max(c["y1"] for c in chars),
        )
        # Tight box over visible glyphs only.
        vis = [c for c in chars if not c["c"].isspace()]
        if vis:
            box = Box(min(c["x0"] for c in vis), min(c["y0"] for c in vis), max(c["x1"] for c in vis), max(c["y1"] for c in vis))
        main = max(vis or chars, key=lambda c: 0)  # placeholder
        sizes: dict[float, int] = {}
        fonts: dict[str, int] = {}
        colors: dict[int, int] = {}
        for c in vis:
            sizes[c["size"]] = sizes.get(c["size"], 0) + 1
            fonts[c["font"]] = fonts.get(c["font"], 0) + 1
            colors[c["color"]] = colors.get(c["color"], 0) + 1
        size = max(sizes, key=sizes.get) if sizes else 0
        font = max(fonts, key=fonts.get) if fonts else ""
        color = max(colors, key=colors.get) if colors else 0
        lines.append(Line(box, toks, size, font, color, base, raw_chars=chars))
    lines.sort(key=lambda l: (l.box.y0, -l.box.x1))
    return lines


def _stream_order(piece: list[dict], stream: list[dict]) -> list[dict]:
    ids = {id(c) for c in piece}
    return [c for c in stream if id(c) in ids]


def _baseline(chars: list[dict]) -> float:
    vis = [c for c in chars if not c["c"].isspace()] or chars
    return max(c["base"] for c in vis)


def _main_size(chars: list[dict]) -> float:
    vis = [c for c in chars if not c["c"].isspace()] or chars
    return max(c["size"] for c in vis)


# ---------------------------------------------------------------- drawings

def color_tuple(c) -> tuple:
    return tuple(round(v, 2) for v in c) if c else ()


def is_orange(fill) -> bool:
    return bool(fill) and abs(fill[0] - 0.87) < 0.05 and abs(fill[1] - 0.47) < 0.06 and abs(fill[2] - 0.25) < 0.06


def is_light_orange(fill) -> bool:
    return bool(fill) and abs(fill[0] - 0.91) < 0.05 and abs(fill[1] - 0.61) < 0.06 and abs(fill[2] - 0.43) < 0.06


def is_dark(fill) -> bool:
    return bool(fill) and max(fill) < 0.25


def is_white(fill) -> bool:
    return bool(fill) and min(fill) > 0.97


@dataclass
class Page:
    number: int  # PDF page, 1-based
    pdf: pymupdf.Page
    lines: list[Line]
    drawings: list[dict]
    images: list[Box]
    markers: list[tuple[str, Box]] = field(default_factory=list)
    cont_boxes: list[Box] = field(default_factory=list)
    badges: list[Box] = field(default_factory=list)
    callout_boxes: list[Box] = field(default_factory=list)
    tables: list[dict] = field(default_factory=list)
    open_label: str | None = None
    rotated: list[Box] = field(default_factory=list)
    figures: list[dict] = field(default_factory=list)


def load_page(doc: pymupdf.Document, index: int) -> Page:
    pdf = doc[index]
    ROTATED.clear()
    lines = read_lines(pdf)
    rotated = list(ROTATED)
    drawings = pdf.get_drawings()
    images = []
    for info in pdf.get_image_info(xrefs=True):
        b = as_box(info["bbox"])
        b = Box(max(b.x0, 0), max(b.y0, 0), min(b.x1, pdf.rect.width), min(b.y1, pdf.rect.height))
        if b.w < 3 or b.h < 3:
            continue
        images.append(b)
    page = Page(index + 1, pdf, lines, drawings, images)
    page.rotated = rotated
    return page


# ---------------------------------------------------------------- page model

HEADER_Y = 100
FOOTER_Y = 700


def drop_running_text(page: Page) -> None:
    for line in page.lines:
        t = line.text.strip()
        if line.box.y1 < HEADER_Y and line.size < 9.5 and ("پودمان" in t or line.color == 7171697):
            line.used = True
        elif line.box.y0 > FOOTER_Y and re.fullmatch(r"[0-9۰-۹]{1,3}", t):
            line.used = True


def find_markers_and_badges(page: Page) -> None:
    for d in page.drawings:
        r = as_box(d["rect"])
        fill = d.get("fill")
        if fill and is_dark(fill) and 3 < r.w < 8 and 3 < r.h < 8 and any(it[0] == "c" for it in d["items"]):
            page.markers.append(("dot", r))
        elif fill and 4 < r.w < 10.5 and 4 < r.h < 10.5 and r.x0 > 380:
            if is_light_orange(fill):
                page.markers.append(("bullet", r))
            elif is_orange(fill) and r.w < 8:
                page.markers.append(("head", r))
            elif is_orange(fill) or is_white(fill):
                page.markers.append(("num", r))
        elif fill and is_dark(fill) and r.x0 >= 400 and 35 < r.w < 65 and 14 < r.h < 32:
            # A badge is a dark tab holding a short bold label.
            if r.x0 >= 470 or any(r.contains_pt(l.box.cx, l.box.cy) and len(l.text.strip()) < 16 for l in page.lines):
                page.badges.append(r)
    # Some badges are pictures, not drawings (an icon sits under them).
    for b in page.images:
        if b.x0 >= 470 and 35 < b.w < 65 and 14 < b.h < 34:
            if not any(b.hits(o) for o in page.badges):
                page.badges.append(b)
    page.badges.sort(key=lambda b: b.y0)


def is_panel_tint(fill) -> bool:
    return bool(fill) and min(fill) > 0.5 and max(fill) < 0.995 and not is_white(fill)


def find_callout_boxes(page: Page) -> None:
    """Tinted panels: callouts with a badge, or a callout running on from
    the previous page (a panel at the top of the page with no badge)."""
    page.cont_boxes = []
    for d in page.drawings:
        r = as_box(d["rect"])
        fill = d.get("fill")
        if not is_panel_tint(fill):
            continue
        if not (r.w > 120 and r.h > 16 and r.x1 < 476 and d["items"] and d["items"][0][0] == "re" and len(d["items"]) == 1):
            continue
        if any(abs(c.x0 - r.x0) < 1 and abs(c.y0 - r.y0) < 1 and abs(c.x1 - r.x1) < 1 for c in page.callout_boxes + page.cont_boxes):
            continue
        if any(b.x0 >= r.x1 - 60 and (abs(b.y0 - r.y0) < 22 or r.y0 - 8 <= b.y0 <= r.y0 + 40) for b in page.badges):
            page.callout_boxes.append(r)
        elif r.y0 < 125 and r.w > 300:
            page.cont_boxes.append(r)


def badge_icons(page: Page) -> list[Box]:
    """Badge pictures and the icons stacked under them (bulb, «!», ...)."""
    out = []
    for b in page.images:
        if b.x0 >= 470 and b.w < 40 and b.h < 40:
            out.append(b)
        elif b.x0 >= 470 and 35 < b.w < 65 and 14 < b.h < 34:
            out.append(b)
        elif any(b.hits(bd.grow(2)) or (abs(b.cx - bd.cx) < 22 and -2 <= b.y0 - bd.y1 < 34 and b.w < 40) for bd in page.badges):
            out.append(b)
    return out


# --- tables ---------------------------------------------------------------

def find_tables(page: Page) -> None:
    segs = []  # thin ruled lines
    for d in page.drawings:
        for item in d["items"]:
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) < 0.8 and abs(p1.x - p2.x) > 8:
                    segs.append(("h", Box(min(p1.x, p2.x), p1.y, max(p1.x, p2.x), p1.y)))
                elif abs(p1.x - p2.x) < 0.8 and abs(p1.y - p2.y) > 8:
                    segs.append(("v", Box(p1.x, min(p1.y, p2.y), p1.x, max(p1.y, p2.y))))
            elif item[0] == "re" and d.get("color") is not None and not d.get("fill"):
                r = as_box(item[1])
                if r.h < 1.2 and r.w > 8:
                    segs.append(("h", Box(r.x0, r.cy, r.x1, r.cy)))
                elif r.w < 1.2 and r.h > 8:
                    segs.append(("v", Box(r.cx, r.y0, r.cx, r.y1)))
    if len(segs) < 6:
        return
    # cluster segments that touch
    groups: list[list] = []
    for kind, b in segs:
        g = Box(b.x0 - 3, b.y0 - 3, b.x1 + 3, b.y1 + 3)
        hit = [grp for grp in groups if any(g.hits(Box(o.x0 - 3, o.y0 - 3, o.x1 + 3, o.y1 + 3)) for _, o in grp)]
        if not hit:
            groups.append([(kind, b)])
        else:
            base = hit[0]
            base.append((kind, b))
            for other in hit[1:]:
                base.extend(other)
                groups.remove(other)
    for grp in groups:
        hs = [b for k, b in grp if k == "h"]
        vs = [b for k, b in grp if k == "v"]
        if len(hs) < 3 or len(vs) < 2:
            continue
        box = hs[0]
        for _, b in grp:
            box = box.union(b)
        if box.w < 80 or box.h < 30:
            continue
        ys = _cluster_vals([b.y0 for b in hs])
        xs = _cluster_vals([b.x0 for b in vs] + [box.x0, box.x1])
        page.tables.append({"box": box, "ys": ys, "xs": xs, "hs": hs, "vs": vs})


def _cluster_vals(vals: list[float], tol: float = 2.5) -> list[float]:
    vals = sorted(vals)
    out: list[float] = []
    for v in vals:
        if out and v - out[-1] < tol:
            continue
        out.append(v)
    return out


# --- figures --------------------------------------------------------------

CAPTION_RE = re.compile(r"^(شکل|جدول)\s*([0-9۰-۹]+)\s*(?:[\u0640\-–:]\s*(.*\S))?\s*$")


def is_caption(line: Line) -> bool:
    m = CAPTION_RE.match(line.text.strip())
    return bool(m) and line.size <= 12.5 and (not m.group(3) or line.bold)


def find_figures(page: Page) -> None:
    parts: list[Box] = []
    deco_icons = badge_icons(page)
    for b in page.images:
        if any(b.hits(i) and abs(b.x0 - i.x0) < 1 for i in deco_icons):
            continue
        if b.w > 500 and b.h > 600:  # full-page background
            continue
        if b.x1 < 4 or b.x0 > page.pdf.rect.width - 4:
            continue
        if b.w < 24 and b.h < 20 and any(l.box.grow(2).contains_pt(b.cx, b.cy) or (l.box.yover(b) > 0.6 * b.h and l.box.xover(b.grow(6)) > 0) for l in page.lines if l.size >= 12):
            continue  # an icon printed inside a sentence
        parts.append(b)
    table_boxes = [t["box"].grow(2) for t in page.tables]
    for d in page.drawings:
        r = as_box(d["rect"])
        fill = d.get("fill")
        if r.w < 1.5 and r.h < 1.5:
            continue
        if any(r.hits(c.grow(-1)) and r.w <= c.w + 2 and r.h <= c.h + 2 for c in page.callout_boxes):
            continue
        if any(t.x0 - 1 <= r.x0 and r.x1 <= t.x1 + 1 and t.y0 - 1 <= r.y0 and r.y1 <= t.y1 + 1 for t in table_boxes):
            continue
        if any(r.hits(b.grow(1)) and (r.x0 >= 466 or r.w < 70) for b in page.badges):
            continue
        if any(abs(r.cx - b.cx) < 22 and -2 <= r.y0 - b.y1 < 34 and r.w < 34 and r.h < 34 for b in page.badges):
            continue  # the icon under a badge
        if r.x0 >= 470 and r.w < 70:  # badges, margin icons
            continue
        if any(r.hits(m.grow(0.5)) and r.w < 12 and r.h < 12 for _, m in page.markers):
            continue
        if r.w < 12 and r.h < 12 and r.x0 > 440:
            continue
        if r.x1 < 4 or r.x0 > page.pdf.rect.width - 6:  # bleed tab
            continue
        if r.y1 < HEADER_Y and r.h < 14:  # running header bar
            continue
        if r.w > 400 and r.h < 3:  # rule under a heading / footnote separator
            continue
        if fill and r.w > 300 and r.h > 600:
            continue
        parts.append(r)
    parts.extend(page.rotated)
    # A frame or picture behind running text is a box around prose, not a figure.
    prose = [
        l for l in page.lines
        if not l.used and l.size >= 12.5 and sum(1 for t in l.toks if is_arabic(t["t"][0])) >= 8
    ]

    def wraps_prose(b: Box) -> bool:
        return sum(1 for l in prose if b.grow(1).contains_pt(l.box.cx, l.box.cy)) >= 2

    parts = [b for b in parts if not wraps_prose(b)]
    # Group parts that touch. Two groups do not merge if prose would end up
    # inside the merged picture.
    prose_all = [
        l for l in page.lines
        if not l.used and l.size >= 12 and not is_caption(l) and sum(1 for t in l.toks if is_arabic(t["t"][0])) >= 6
    ]

    def covers_prose(box: Box, comps: list[Box]) -> bool:
        for l in prose_all:
            if l.used:
                continue
            if box.contains_pt(l.box.cx, l.box.cy) and not any(c.grow(2).contains_pt(l.box.cx, l.box.cy) for c in comps):
                return True
        return False

    clusters: list[dict] = [{"box": b, "parts": [b]} for b in parts]

    def merge_pass(pad: float) -> bool:
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                a, b = clusters[i], clusters[j]
                if not any(p.grow(pad).hits(q) for p in a["parts"] for q in b["parts"]):
                    continue
                box = a["box"].union(b["box"])
                comps = a["parts"] + b["parts"]
                if covers_prose(box, comps):
                    continue
                clusters[i] = {"box": box, "parts": comps}
                clusters.pop(j)
                return True
        return False

    while merge_pass(5):
        pass
    # Small labels that sit on or next to a picture belong to it.
    for _ in range(2):
        for cl in clusters:
            for line in page.lines:
                if line.used or is_caption(line) or line.size >= 15.5:
                    continue
                if any(kind == "head" and m.y0 - 4 <= line.box.cy <= m.y1 + 4 for kind, m in page.markers):
                    continue
                lb = line.box
                inside = any(c.grow(1.5).contains_pt(lb.cx, lb.cy) for c in cl["parts"]) and lb.x0 >= cl["box"].x0 - 4 and lb.x1 <= cl["box"].x1 + 4
                small_label = (
                    any(c.grow(10).hits(lb) for c in cl["parts"])
                    and (line.size <= 10.5 or (len(line.text.strip()) <= 3 and line.bold))
                    and lb.w < 160
                )
                if inside or small_label:
                    cl["box"] = cl["box"].union(lb)
                    cl["parts"].append(lb)
                    line.used = True
                    line.marker = "figure-label"
        while merge_pass(3):
            pass
    # Thin bars and rules with no picture in them are decoration.
    clusters = [
        cl for cl in clusters
        if any(any(abs(p.x0 - im.x0) < 1 and abs(p.y0 - im.y0) < 1 for im in page.images) for p in cl["parts"])
        or (cl["box"].h >= 14 and cl["box"].w >= 14)
    ]
    groups = [cl["box"] for cl in clusters]
    groups = [g for g in groups if g.w >= 14 and g.h >= 10]
    width = page.pdf.rect.width
    keep = []
    for g in groups:
        # Margin tabs and full-bleed banners are decoration.
        if g.x1 > width - 3 and (g.x0 > 440 or g.x0 < 3):
            continue
        if g.x0 < 0 or g.x1 > width + 1:
            continue
        # An icon printed inside a sentence («از دکمه [icon] ...»).
        if g.w < 34 and g.h < 24 and any(
            l.size >= 12 and l.box.yover(g) > 0.4 * g.h and l.box.x0 - 6 <= g.cx <= l.box.x1 + 6
            for l in page.lines
        ):
            continue
        # A banner behind a module/unit title is decoration too.
        if any(l.size >= 15.5 and g.contains_pt(l.box.cx, l.box.cy) for l in page.lines):
            continue
        keep.append(g)
    page.figures = [{"box": g, "caption": None} for g in keep]


def caption_distance(cap: Box, g: Box) -> float:
    if cap.hits(g):
        return 0.0
    dx = max(0.0, cap.x0 - g.x1, g.x0 - cap.x1)
    below = cap.y0 - g.y1
    above = g.y0 - cap.y1
    if dx == 0:
        if below >= -4:
            return max(0.0, below)
        return above * 2 + 20
    if g.yover(cap) > 0:
        return dx * 0.5 + 10
    return dx + max(below, above, 0) * 1.5 + 20


def attach_captions(page: Page) -> None:
    caps = [l for l in page.lines if not l.used and is_caption(l) and l.text.strip().startswith("شکل")]
    pairs = []
    for cap in caps:
        for fig in page.figures:
            d = caption_distance(cap.box, fig["box"])
            if d < 90:
                pairs.append((d, id(cap), cap, fig))
    pairs.sort(key=lambda p: (p[0], p[1]))
    for d, _, cap, fig in pairs:
        if cap.used or fig["caption"] is not None:
            continue
        fig["caption"] = cap
        cap.used = True
        cap.marker = "caption"
    # Second chance: a caption set far to the side of its only free figure.
    for cap in caps:
        if cap.used:
            continue
        free = [f for f in page.figures if f["caption"] is None and caption_distance(cap.box, f["box"]) < 220]
        def body_between(f, cap=cap) -> bool:
            g = f["box"]
            for l in page.lines:
                if l.used or l.size < 12:
                    continue
                if g.grow(12).yover(cap.box) > 0:
                    lo, hi = min(g.x1, cap.box.x1), max(g.x0, cap.box.x0)
                    if l.box.yover(cap.box) > 0 and lo < l.box.cx < hi:
                        return True
                elif g.y1 <= l.box.cy <= cap.box.y0 and l.box.xover(g) > 0:
                    return True
            return False

        free = [f for f in free if not body_between(f)]
        if len(free) == 1:
            free[0]["caption"] = cap
            cap.used = True
            cap.marker = "caption"
    merge_figure_stacks(page)
    # A small line between a picture and its caption is part of the caption.
    for fig in page.figures:
        cap = fig["caption"]
        if cap is None:
            continue
        g = fig["box"]
        for l in page.lines:
            if l.used or l.size > 10.5:
                continue
            if g.xover(l.box) > 0 and g.y1 - 2 <= l.box.y0 and l.box.y1 <= cap.box.y0 + 2:
                l.used = True
                fig.setdefault("sub", []).append(l)


def merge_figure_stacks(page: Page) -> None:
    """Panels printed one above the other share one caption under the last."""
    body = [l for l in page.lines if not l.used and l.size >= 11.5]
    changed = True
    while changed:
        changed = False
        for fig in page.figures:
            if fig["caption"] is None:
                continue
            g = fig["box"]
            for other in page.figures:
                if other is fig or other["caption"] is not None:
                    continue
                o = other["box"]
                side_gap = o.x0 - g.x1 if o.x0 >= g.x1 - 3 else g.x0 - o.x1
                if -3 <= side_gap < 30 and o.yover(g) > 0.5 * min(o.h, g.h):
                    lo_x, hi_x = min(o.x1, g.x1), max(o.x0, g.x0)
                    if not any(l.box.x0 >= lo_x - 1 and l.box.x1 <= hi_x + 1 and l.box.yover(o) > 0 for l in body):
                        fig["box"] = g.union(o)
                        page.figures.remove(other)
                        changed = True
                        break
                gap = g.y0 - o.y1 if o.y1 <= g.y0 + 3 else o.y0 - g.y1
                if not (-3 <= gap < 16):
                    continue
                if o.xover(g) < 0.4 * min(o.w, g.w):
                    continue
                lo, hi = min(o.y1, g.y1), max(o.y0, g.y0)
                if any(l.box.y0 >= lo - 1 and l.box.y1 <= hi + 1 and l.box.xover(o.union(g)) > 0 for l in body):
                    continue
                fig["box"] = g.union(o)
                page.figures.remove(other)
                changed = True
                break
            if changed:
                break


# ---------------------------------------------------------------- inline text

CODEISH = re.compile(r"\w\(|\(\)|[\[\]{}<>=;\"'_#\\]|\w\.[A-Za-z_]|^\.\w|^@\w|^/|\w/\w")


def fix_call_parens(toks: list[dict]) -> list[dict]:
    """The book prints «print()» as «()print» in Persian lines. Put the
    parentheses back after the name."""
    out = list(toks)
    i = 0
    while i + 2 < len(out):
        a, b = out[i]["t"], out[i + 1]["t"]
        if {a, b} == {"(", ")"} and not out[i].get("run") and not out[i + 1].get("run") and out[i + 2].get("run"):
            run = out[i + 2]["run"]
            j = i + 2
            while j < len(out) and out[j].get("run") == run and (out[j]["t"].isalnum() or out[j]["t"] in "_."):
                j += 1
            name = out[i + 2 : j]
            if name and (i == 0 or not (out[i - 1]["t"].isascii() and out[i - 1]["t"].isalnum())):
                bold = name[0]["bold"]
                po = dict(out[i], t="(", run=run, bold=bold)
                pc = dict(out[i + 1], t=")", run=run, bold=bold)
                out[i:j] = name + [po, pc]
                i = j
                continue
        i += 1
    return out


CLOSERS = set(')]}"\'”!?.;:')
TAG_RE = re.compile(r"(?<![A-Za-z0-9\"'”])>([/\"”']?[A-Za-z!][^<>\u0600-\u06ff]{0,90}?)<(?![A-Za-z/!])")


def _joined(toks: list[dict]) -> tuple[str, list[int]]:
    starts, pos = [], 0
    for t in toks:
        starts.append(pos)
        pos += len(t["t"])
    return "".join(t["t"] for t in toks), starts


def _tok_at(starts: list[int], offset: int) -> int | None:
    try:
        return starts.index(offset)
    except ValueError:
        return None


def fix_mirrored_tags(toks: list[dict]) -> list[dict]:
    """«>h1/<» is how the book typed «</h1>» so that it would look right."""
    while True:
        text, starts = _joined(toks)
        for m in TAG_RE.finditer(text):
            i, j = _tok_at(starts, m.start()), _tok_at(starts, m.end())
            if i is None or (j is None and m.end() != len(text)):
                continue
            j = len(toks) if j is None else j
            inner = m.group(1)
            if inner.endswith("/"):
                new = "</" + inner[:-1].strip() + ">"
            elif inner[0] in "\"”'":
                new = "<" + inner[1:] + inner[0] + ">"
            elif inner.endswith("!") and " " in inner:
                new = "<!" + inner[:-1] + ">"
            else:
                new = "<" + inner + ">"
            ref = next((t for t in toks[i:j] if t.get("run")), toks[i])
            repl = [dict(ref, t=ch, run=ref.get("run") or -1) for ch in new]
            toks = toks[:i] + repl + toks[j:]
            break
        else:
            return toks


def _runs(toks: list[dict]) -> list[tuple[int, int]]:
    out, i = [], 0
    while i < len(toks):
        r = toks[i].get("run")
        if not r:
            i += 1
            continue
        j = i
        while j < len(toks) and toks[j].get("run") == r:
            j += 1
        out.append((i, j))
        i = j
    return out


def _unbalanced(text: str) -> bool:
    return (
        text.count("(") > text.count(")")
        or text.count("[") > text.count("]")
        or text.count('"') % 2 == 1
        or text.count("'") % 2 == 1
        or text.count("”") > text.count("“") + text.count("”") // 2 * 2 - text.count("“")
    )


def fix_stranded_closers(toks: list[dict]) -> list[dict]:
    """«)"product.pop("price» -> «product.pop("price")»: closing marks that
    the book printed on the wrong side of an English run."""
    changed = True
    while changed:
        changed = False
        for i, j in _runs(toks):
            run_text = "".join(t["t"] for t in toks[i:j])
            if not _unbalanced(run_text):
                continue
            k = i
            while k > 0:
                ch = toks[k - 1]["t"]
                if ch in CLOSERS and not toks[k - 1].get("run"):
                    k -= 1
                elif ch == " " and k - 1 > 0 and toks[k - 2]["t"] in CLOSERS and not toks[k - 2].get("run") and k < i:
                    k -= 1
                else:
                    break
            moved = toks[k:i]
            if not moved or not any(t["t"] in ')]}"\'”' for t in moved):
                continue
            r = toks[i]["run"]
            tail = [dict(t, run=r, bold=toks[i]["bold"]) for t in reversed(moved)]
            while tail and tail[0]["t"] == " ":
                tail.pop(0)
            toks = toks[:k] + toks[i:j] + tail + toks[j:]
            changed = True
            break
    return toks


def absorb_closers(toks: list[dict]) -> list[dict]:
    """A closing bracket right after an unbalanced run belongs to it."""
    for i, j in _runs(toks):
        text = "".join(t["t"] for t in toks[i:j])
        r = toks[i]["run"]
        k = j
        while k < len(toks) and not toks[k].get("run") and toks[k]["t"] in ')]"\'' and _unbalanced(text):
            toks[k] = dict(toks[k], run=r)
            text += toks[k]["t"]
            k += 1
    return toks


OPERATOR_CHARS = set("<>=!")


def isolate_operators(toks: list[dict]) -> list[dict]:
    """«=<» standing alone in a Persian sentence: the book shows it as «<=».
    Keep the order the page shows and set it apart as code, so the browser
    does not reorder or mirror it."""
    out = list(toks)
    i = 0
    while i < len(out):
        if out[i]["t"] in OPERATOR_CHARS and not out[i].get("run"):
            j = i
            while j < len(out) and out[j]["t"] in OPERATOR_CHARS and not out[j].get("run"):
                j += 1
            before = out[i - 1]["t"] if i else " "
            after = out[j]["t"] if j < len(out) else " "
            if (before.isspace() or before in "(«") and (after.isspace() or after in ")»،."):
                run = 9000 + i
                seq = [dict(t, run=run) for t in reversed(out[i:j])]
                out[i:j] = seq
            i = j
            continue
        i += 1
    return out


def render_inline(toks: list[dict]) -> str:
    """Logical tokens -> markdown with **bold** and `code`."""
    toks = [dict(t) for t in toks]
    toks = isolate_operators(toks)
    toks = fix_call_parens(toks)
    toks = fix_mirrored_tags(toks)
    toks = fix_stranded_closers(toks)
    # «<p>» / «</p>»: the brackets belong to the tag name's run.
    for i, j in _runs(toks):
        r = toks[i]["run"]
        if i > 1 and toks[i - 1]["t"] == "/" and toks[i - 2]["t"] == "<" and not toks[i - 1].get("run") and not toks[i - 2].get("run"):
            toks[i - 1]["run"] = toks[i - 2]["run"] = r
        elif i > 0 and toks[i - 1]["t"] == "<" and not toks[i - 1].get("run"):
            toks[i - 1]["run"] = r
        if j < len(toks) and toks[j]["t"] == ">" and not toks[j].get("run"):
            toks[j]["run"] = r
    toks = absorb_closers(toks)
    # A run is bold or not as a whole.
    for i, j in _runs(toks):
        letters = [t for t in toks[i:j] if t["t"].isalnum()]
        bold = bool(letters) and sum(t["bold"] for t in letters) * 2 >= len(letters)
        for t in toks[i:j]:
            t["bold"] = bold
    # Punctuation and spaces take the boldness of their neighbours.
    strong = {i for i, t in enumerate(toks) if t.get("run") or (t["t"].strip() and (t["t"][0].isalnum() or is_arabic(t["t"][0])))}
    for i, t in enumerate(toks):
        if i in strong:
            continue
        before = next((toks[k]["bold"] for k in range(i - 1, -1, -1) if k in strong), False)
        after = next((toks[k]["bold"] for k in range(i + 1, len(toks)) if k in strong), False)
        t["bold"] = before and after
    segs: list[list] = []  # [text, bold, run]
    for t in toks:
        run = t.get("run") or 0
        if segs and segs[-1][1] == t["bold"] and segs[-1][2] == run:
            segs[-1][0] += t["t"]
        else:
            segs.append([t["t"], t["bold"], run])
    out = []
    for text, bold, run in segs:
        text = clean_text(text)
        if not text:
            continue
        core = text.strip()
        lead = text[: len(text) - len(text.lstrip())]
        tail = text[len(text.rstrip()):]
        if run and (CODEISH.search(core) or re.fullmatch(r"[<>=!]+", core)) and not re.search(r"https?://|www\.", core):
            piece = code_span(core)
        else:
            if run:
                core = re.sub(r"(\w) ([,:;]) ?(\w)", r"\1\2 \3", core)
            piece = md_escape(core)
        if bold and piece:
            piece = f"**{piece}**"
        out.append(lead + piece + tail)
    text = "".join(out)
    text = re.sub(r"\*\*(\s*)\*\*", r"\1", text)
    # «**منوی واکنش‌گرا (Responsive**)»: close the bold after the bracket.
    text = re.sub(r"\*\*([^*]*\([^()*]*)\*\*\)", r"**\1)**", text)
    # «شیءMath»: a Persian word glued to the English word after it.
    parts = re.split(r"(`[^`]*`)", text)
    parts = [p if p.startswith("`") else re.sub(r"([\u0621-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc\u0629\u0624\u0626])([A-Za-z])", r"\1 \2", p) for p in parts]
    text = "".join(parts)
    # «جستجو می‌کند.گاهی»: a space after a full stop between Persian words.
    text = re.sub(r"([\u0621-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc])\.([\u0621-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc])", r"\1. \2", text)
    # «autopep8 ،Black»: the Persian comma follows the word before it.
    text = re.sub(r"(\S) ?، ?(?=\S)", r"\1، ", text)
    # «"!welcome admin"», «":your age "»: the mark ends the English phrase.
    text = re.sub(r'"([!:.…]+)([A-Za-z][^"\n`]*?)\s*"', r'"\2\1"', text)
    # «() range», «()`write_text`»: the empty brackets belong after the name.
    text = re.sub(r"\(\)\s*`(\w+)`", r"`\1()`", text)
    text = re.sub(r"(?<![\w`])\(\) ([A-Za-z_]\w*)\b", r"`\1()`", text)
    # «?(`x===s`)» -> «(`x===s`)?»
    text = re.sub(r"\?\((`[^`]+`)\)", r"(\1)?", text)
    # Python dunder names and «)(len» printed in a Persian line.
    text = re.sub(r"\\_\\_(\w+)\\_\\_", r"`__\1__`", text)
    text = re.sub(r"(?<![\w`])\)\((\w+)", r"`\1()`", text)
    # «`<body`/>» is a closing tag the book printed backwards: «`</body>`».
    text = re.sub(r"`<(\w+)`/&gt;", r"`</\1>`", text)
    # «`)pip install requests(`»: brackets printed on the wrong sides.
    text = re.sub(r"`\)([^`()]+)\(`", r"(`\1`)", text)
    # «>-- --!<» is how the book prints an HTML comment «<!-- -->».
    text = re.sub(r"(&gt;|&lt;)-- --!(&lt;|&gt;)", "`<!-- -->`", text)
    # «:D» -> «D:» (a drive letter printed in a Persian line)
    text = re.sub(r"(^|\s):([A-Z])(?=\s|$|،)", r"\1\2:", text)
    return text


def code_span(text: str) -> str:
    ticks = "``" if "`" in text else "`"
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{ticks}{pad}{text}{pad}{ticks}"


def md_escape(text: str) -> str:
    text = text.replace("\\", "\\\\")
    for ch in "`*_[]":
        text = text.replace(ch, "\\" + ch)
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


# ---------------------------------------------------------------- blocks

@dataclass
class Block:
    kind: str  # para, head2, head3, bullet, num, figure, table, code, callout, footnote, module, unit
    y: float
    x1: float = 0
    text: str = ""
    lines: list = field(default_factory=list)
    data: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    open_end: bool = False  # paragraph runs on (no final full stop)


def marker_for(page: Page, line: Line) -> str:
    for kind, m in page.markers:
        if kind == "dot":
            if m.x1 <= line.box.x0 + 3 and line.box.x0 - m.x1 < 16 and line.box.y0 - 3 <= m.cy <= line.box.y1 + 3:
                return "bullet"
            continue
        if kind == "num" and m.x0 > line.box.x1 - 12 and m.x0 < line.box.x1 + 6 and line.box.y0 - 3 <= m.cy <= line.box.y1 + 3:
            return kind
        if m.x0 > line.box.x1 - 4 and m.x0 - line.box.x1 < 14 and line.box.y0 - 3 <= m.cy <= line.box.y1 + 3:
            return kind
    return ""


def line_left_bound(page: Page, line: Line, col_left: float) -> float:
    """Left edge of the space a line can use: the column, or the right side
    of a picture, table, or caption printed beside it."""
    bound = col_left
    tall = line.box
    tall = Box(tall.x0, tall.y0 - 22, tall.x1, tall.y1 + 22)
    for fig in page.figures:
        g = fig["box"]
        if g.yover(tall) > 2 and g.x1 <= line.box.x0 + 14:
            bound = max(bound, g.x1)
    for t in page.tables:
        g = t["box"]
        if g.yover(tall) > 2 and g.x1 <= line.box.x0 + 14:
            bound = max(bound, g.x1)
    # So does any text printed to the left of the line (a code sketch).
    for other in page.lines:
        if other is not line and other.box.yover(line.box) > 4 and other.box.x1 <= line.box.x0 - 4:
            bound = max(bound, other.box.x1)
    # A caption printed beside its picture narrows the text column too.
    for fig in page.figures:
        cap = fig["caption"]
        if cap is not None and cap.box.yover(line.box) > 2 and cap.box.x1 <= line.box.x0 + 14:
            bound = max(bound, cap.box.x1)
    return bound


ENDS = (".", "؟", "?", "!", ":", "؛", "…", ")")


def lines_to_blocks(page: Page, lines: list[Line], col_left: float, col_right: float) -> list[Block]:
    """Join justified lines into paragraphs / list items / headings."""
    blocks: list[Block] = []
    cur: Block | None = None
    prev: Line | None = None
    for line in lines:
        text = line.text.strip()
        if not text:
            continue
        mk = marker_for(page, line)
        line.marker = mk or line.marker
        size = line.size
        head2 = "Titr" in line.font and 13.5 <= size < 16
        latin = line.latin_only and not re.fullmatch(r"[0-9۰-۹\W]*", text)
        starts_item = bool(
            mk
            or re.match(r"^\u0640\s*\S", text)
            or re.match(r"^[0-9۰-۹]{1,2}\s*\u0640\s*\S", text)
        )
        new = True
        punct_only = bool(re.fullmatch(r"[\W_]+", text)) and not any(is_arabic(ch) for ch in text)
        if cur is not None and prev is not None and cur.kind == "code" and (latin or punct_only or line.base == "L") and line.box.y0 - prev.box.y1 < 10 and not mk:
            cur.lines.append(line)
            prev = line
            continue
        if cur is not None and prev is not None and cur.kind in ("para", "bullet", "num", "lead") and not head2 and not starts_item and not punct_only:
            gap = line.box.y0 - prev.box.y1
            bound = line_left_bound(page, prev, col_left)
            tol = 14 if bound <= col_left + 1 else 55
            prev_full = prev.box.x0 <= bound + tol or (prev.base == "L" and prev.box.x1 >= col_right - 14)
            same_size = abs(prev.size - size) < 2.6 or (latin and not prev.latin_only) or (prev.latin_only and not latin)
            lead_in = _starts_bold(line) and (
                (not _ends_bold(prev) and prev.text.rstrip().endswith(ENDS))
                or (bool(re.match(r"\s*[^:()]{1,40}:", line.text)) and not prev.text.rstrip().endswith(":"))
            )
            # A sentence that stops at the end of a full line runs on, even
            # past the gap left by a picture printed beside it.
            if gap >= 9 and gap < 40 and prev_full and not prev.text.rstrip().endswith(ENDS) and not _starts_bold(line) and not (prev.bold or _strong(line)[:1] and _strong(line)[0]["bold"]):
                span = Box(prev.box.x0, prev.box.y1, prev.box.x1, line.box.y0)
                blocked = any(f["box"].hits(span) for f in page.figures) or any(t["box"].hits(span) for t in page.tables)
                if not blocked:
                    gap = 0
            if gap < 9 and same_size and prev_full and not lead_in and line.box.x1 > prev.box.x0:
                if not (latin and prev.latin_only and _code_like(text) and _code_like(prev.text)):
                    new = False
        if not new:
            cur.lines.append(line)
            prev = line
            continue
        if head2:
            cur = Block("head2", line.box.y0, line.box.x1, lines=[line])
        elif mk == "head":
            cur = Block("lead", line.box.y0, line.box.x1, lines=[line])
        elif mk == "num" or re.match(r"^[0-9۰-۹]{1,2}\s*\u0640\s*\S", text):
            cur = Block("num", line.box.y0, line.box.x1, lines=[line])
        elif mk == "bullet" or text.startswith("\u0640"):
            cur = Block("bullet", line.box.y0, line.box.x1, lines=[line])
        elif (latin and _code_like(text)) or (line.base == "L" and not line.latin_only) or (punct_only and re.fullmatch(r"[{}()\[\];]+", text)):
            cur = Block("code", line.box.y0, line.box.x1, lines=[line])
        else:
            cur = Block("para", line.box.y0, line.box.x1, lines=[line])
        blocks.append(cur)
        prev = line
    # merge consecutive code lines into one block
    out: list[Block] = []
    for b in blocks:
        if b.kind == "code" and out and out[-1].kind == "code" and b.y - out[-1].lines[-1].box.y1 < 12:
            out[-1].lines.extend(b.lines)
            continue
        out.append(b)
    for b in out:
        finish_block(b, col_left)
    return out


def _strong(line: Line) -> list[dict]:
    return [t for t in line.toks if t["t"].strip() and (t["t"][0].isalnum() or is_arabic(t["t"][0]))]


def _starts_bold(line: Line) -> bool:
    s = _strong(line)
    return bool(s) and s[0]["bold"] and not all(t["bold"] for t in s)


def _ends_bold(line: Line) -> bool:
    s = _strong(line)
    return bool(s) and s[-1]["bold"]


def _code_like(text: str) -> bool:
    t = text.strip()
    if re.match(r"^(/\*|//|<!--)", t) or re.search(r"\*/$|^[\w-]+\s*:\s*[^:]+;?$", t):
        return True
    if re.search(r"[(){}\[\]=;<>\"']|^\s*(def|class|for|while|if|elif|else|return|import|from|print|let|const|var|function)\b|^#|^\.|^\w+\.\w+\(", t):
        return True
    return False


def finish_block(b: Block, col_left: float) -> None:
    if b.kind == "code":
        xs = [l.box.x0 for l in b.lines]
        x_min = min(xs)
        rows = []
        for l in b.lines:
            sp = max(0, round((l.box.x0 - x_min) / (l.size * 0.5)))
            rows.append(" " * sp + clean_text("".join(t["t"] for t in l.toks)).rstrip())
        b.text = "\n".join(rows)
        return
    toks: list[dict] = []
    for i, l in enumerate(b.lines):
        lt = list(l.toks)
        # strip leading/trailing spaces of the line
        while lt and lt[0]["t"].isspace():
            lt.pop(0)
        while lt and lt[-1]["t"].isspace():
            lt.pop()
        if toks and lt:
            last = toks[-1]["t"]
            first = lt[0]["t"]
            if last.endswith(("-", ZWNJ, HAIR)) and not last.endswith(" -"):
                if last.endswith(HAIR):
                    toks[-1] = dict(toks[-1], t=last[:-1] + ZWNJ)
            else:
                toks.append({"t": " ", "bold": False})
        toks.extend(lt)
    if b.kind in ("bullet", "num"):
        while toks and (toks[0]["t"].isspace() or toks[0]["t"] in ("\u0640", "\u0640")):
            toks.pop(0)
    if b.kind == "num":
        white = [t for t in toks if t.get("color") == 0xFFFFFF and t["t"].isdigit()]
        if white:
            b.data["n"] = int("".join(t["t"] for t in white).translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")))
            toks = [t for t in toks if t not in white]
            while toks and toks[0]["t"].isspace():
                toks.pop(0)
            for t in toks:
                if t.get("run") and not any(x.get("run") == t["run"] and x["t"].isalpha() for x in toks):
                    t["run"] = 0
        digits = "" if not white else "x"
        while toks and toks[0]["t"] in "0123456789۰۱۲۳۴۵۶۷۸۹" and len(digits) < 2:
            digits += toks.pop(0)["t"]
        while toks and (toks[0]["t"].isspace() or toks[0]["t"] in ("\u0640", ".", "-", ")", "\u0640")):
            toks.pop(0)
        if digits and digits != "x":
            b.data["n"] = int(digits.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")))
        elif not digits:
            b.kind = "lead"  # a square with no number is a sub-heading
    b.data["toks"] = toks
    text = render_inline(toks).strip()
    text = re.sub(r"[ \t]{2,}", " ", text)
    b.text = text
    last = b.lines[-1]
    b.open_end = not text.rstrip("*` ").endswith(ENDS) and last.box.x0 <= col_left + 14


# ---------------------------------------------------------------- page -> blocks

def table_block(page: Page, t: dict, image_name) -> Block:
    box = t["box"]
    xs, ys = t["xs"], t["ys"]
    cells_lines = [l for l in page.lines if not l.used and box.grow(1).contains_pt(l.box.cx, l.box.cy)]
    for l in cells_lines:
        l.used = True
    nrows, ncols = len(ys) - 1, len(xs) - 1
    ok = nrows >= 1 and ncols >= 2

    def has_rule(x: float, y: float) -> bool:
        return any(abs(v.x0 - x) < 2.5 and v.y0 - 2 <= y <= v.y1 + 2 for v in t["vs"])

    # Column spans per row: a missing inner rule joins two cells.
    spans: list[list[int]] = []  # for each row, cell index -> span start
    for i in range(nrows):
        y = (ys[i] + ys[i + 1]) / 2
        start = [0] * ncols
        for c in range(1, ncols):
            start[c] = start[c - 1] if not has_rule(xs[c], y) else c
        spans.append(start)
    grid = [["" for _ in range(ncols)] for _ in range(nrows)]
    pieces = []  # (row, col, y, chars)
    for l in cells_lines:
        r = next((i for i in range(nrows) if ys[i] - 1 <= l.box.cy <= ys[i + 1] + 1), None)
        if r is None:
            ok = False
            continue
        by_col: dict[int, list] = {}
        for ch in l.raw_chars:
            cx = (ch["x0"] + ch["x1"]) / 2
            c = next((i for i in range(ncols) if xs[i] - 1 <= cx <= xs[i + 1] + 1), None)
            if c is None:
                continue
            # Text of a spanned cell goes in its right-most column (RTL).
            group = [k for k in range(ncols) if spans[r][k] == spans[r][c]]
            by_col.setdefault(max(group), []).append(ch)
        for c, chars in by_col.items():
            pieces.append((r, c, l.box.y0, chars))
    cell_parts: dict[tuple[int, int], list[tuple[str, bool]]] = {}
    for r, c, _, chars in sorted(pieces, key=lambda p: p[2]):
        toks, _ = visual_to_logical_tokens(chars)
        plain = clean_text("".join(t["t"] for t in toks)).strip()
        if not plain:
            continue
        is_code = not any(is_arabic(ch) for ch in plain) and (
            _code_like(plain) or bool(re.search(r"[A-Za-z]", plain) and re.search(r"[=+\-*/%<>!&|.:#]", plain))
        )
        txt = code_span(plain) if is_code else render_inline(toks).strip()
        cell_parts.setdefault((r, c), []).append((txt, is_code))
    code_rows = {r for (r, c), parts in cell_parts.items() if any(is_code for _, is_code in parts)}
    for (r, c), parts in cell_parts.items():
        prose = any(any(is_arabic(ch) for ch in t) for t, is_code in parts if not is_code)
        if r in code_rows and (any(is_code for _, is_code in parts) or not prose):
            grid[r][c] = "<br>".join(t for t, _ in parts)
        else:
            grid[r][c] = " ".join(t for t, _ in parts)
    title_rows = []
    keep_rows = []
    for i, row in enumerate(grid):
        if not any(cell.strip() for cell in row):
            continue
        if ncols > 1 and len(set(spans[i])) == 1:
            title_rows.append(" ".join(c for c in row if c))
            continue
        keep_rows.append(row)
    grid = keep_rows
    if not grid or len(grid) < 2:
        ok = False
    if any(len(cell) > 400 for row in grid for cell in row):
        ok = False
    # The competency rubric (ارزشیابی) is clearer as a picture.
    head_text = " ".join(c for row in grid[:2] for c in row)
    if re.search(r"ردیف|مراحل کار|نمره|استاندارد", head_text):
        ok = False
    # A rubric with many merged cells is clearer as a picture.
    merged = sum(1 for sp in spans for k in range(1, ncols) if sp[k] != k)
    if merged > nrows:
        ok = False
    b = Block("table", box.y0, box.x1, data={"box": box})
    if ok:
        # Book tables read right to left: first column is the rightmost.
        rows = [list(reversed(row)) for row in grid]
        rows[0] = [c.replace("**", "") for c in rows[0]]
        b.data["rows"] = rows
        b.data["title"] = " — ".join(title_rows)
    else:
        b.data["image"] = image_name(box)
    return b


def fix_ltr_lines(page: Page) -> None:
    """A code line like «<h1>سلام دنیا!</h1>» is printed left to right: it
    starts at the left margin with English and stops short of the right."""
    body = [l for l in page.lines if not l.used and l.size >= 11.5]
    if not body:
        return
    right = max(l.box.x1 for l in body)
    left = min(l.box.x0 for l in body)
    for l in page.lines:
        if l.used or l.base != "R" or not any(is_arabic(t["t"][0]) for t in l.toks):
            continue
        vis = sorted(l.raw_chars, key=lambda c: c["x0"])
        strong = [c for c in vis if c["c"].strip() and (c["c"].isalpha() or is_arabic(c["c"]))]
        if not strong or not strong[0]["c"].isascii():
            continue
        # The right end of a code line is code too (« </h1>», «);»).
        last = [c for c in vis if c["c"].strip()][-1]["c"]
        if not last.isascii():
            continue
        if not re.match(r"\s*[<{(\[\w.#]", "".join(c["c"] for c in vis)):
            continue
        if l.box.x1 < right - 30 and l.box.x0 <= left + 40:
            first = "".join(c["c"] for c in vis if c["c"].strip())[:1]
            if first in "<{" or re.match(r"[a-z.#]", first):
                toks, base = visual_to_logical_tokens(l.raw_chars, base="L")
                l.toks, l.base = toks, base


def page_blocks(page: Page, image_name, prev_label: str | None = None) -> list[Block]:
    drop_running_text(page)
    find_markers_and_badges(page)
    find_callout_boxes(page)
    find_tables(page)
    find_figures(page)
    attach_captions(page)

    blocks: list[Block] = []
    fix_ltr_lines(page)

    # Tables (and their «جدول N» caption, usually just above).
    for t in page.tables:
        tb = table_block(page, t, image_name)
        cap = None
        for l in page.lines:
            if l.used or not is_caption(l):
                continue
            above = -4 < t["box"].y0 - l.box.y1 < 60
            below = -4 < l.box.y0 - t["box"].y1 < 30
            if t["box"].grow(80).xover(l.box) > 0 and (above or below):
                cap = l
                break
        if cap:
            cap.used = True
            tb.data["caption"] = cap.text.strip()
            tb.y = min(tb.y, cap.box.y0)
        blocks.append(tb)

    # Figures.
    for fig in page.figures:
        g = fig["box"]
        name = image_name(g)
        cap = fig["caption"]
        blocks.append(
            Block(
                "figure",
                g.y0,
                g.x1,
                data={
                    "image": name,
                    "caption": cap.text.strip() if cap else "",
                    "sub": " ".join(l.text.strip() for l in fig.get("sub", [])),
                    "box": g,
                },
            )
        )

    # Callouts: a badge in the margin + text to its left, or a tinted panel
    # running on from the previous page.
    callout_regions = []
    for badge in page.badges:
        label_lines = [l for l in page.lines if not l.used and badge.grow(2).contains_pt(l.box.cx, l.box.cy)]
        label = " ".join(l.text.strip() for l in label_lines).strip()
        for l in label_lines:
            l.used = True
        box = next(
            (
                c for c in sorted(page.callout_boxes, key=lambda c: c.w * c.h)
                if badge.x0 >= c.x1 - 60 and (abs(badge.y0 - c.y0) < 22 or c.y0 - 8 <= badge.y0 <= c.y0 + 40)
            ),
            None,
        )
        callout_regions.append({"badge": badge, "label": label, "box": box, "cont": False})
    for c in page.cont_boxes:
        callout_regions.append({"badge": None, "label": prev_label or "", "box": c, "cont": True})

    body_lines = [l for l in page.lines if not l.used]
    col_left = min((l.box.x0 for l in body_lines if l.size >= 12 and l.box.w > 250), default=54)
    col_right = max((l.box.x1 for l in body_lines if l.size >= 12), default=472)

    def region_box(reg: dict, members: list[Line]) -> Box:
        if reg["box"] is not None:
            return reg["box"]
        badge = reg["badge"]
        left = min((l.box.x0 for l in members), default=col_left)
        y0 = min([badge.y0] + [l.box.y0 for l in members])
        y1 = max([badge.y1] + [l.box.y1 for l in members])
        return Box(left, y0, badge.x0, y1)

    # Smallest panels first, so a note inside a workshop panel is built
    # before the panel that holds it.
    order = sorted(
        range(len(callout_regions)),
        key=lambda i: (callout_regions[i]["box"].w * callout_regions[i]["box"].h) if callout_regions[i]["box"] else 0,
    )
    built: list[tuple[Box, Block]] = []
    for idx in order:
        reg = callout_regions[idx]
        if reg["box"] is not None:
            members = [l for l in page.lines if not l.used and reg["box"].grow(1.5).contains_pt(l.box.cx, l.box.cy)]
        else:
            # Unboxed note: the paragraph that starts beside the badge.
            badge = reg["badge"]
            free = [l for l in page.lines if not l.used]
            start = [l for l in free if abs(l.box.y0 - badge.y0) < 12 and l.box.x1 < badge.x0]
            members = []
            if start:
                first = min(start, key=lambda l: l.box.y0)
                members = [first]
                cursor = first
                for l in sorted(free, key=lambda l: l.box.y0):
                    if l.box.y0 <= cursor.box.y0 or l in members:
                        continue
                    if l.box.y0 - cursor.box.y1 > 7:
                        break
                    if cursor.text.rstrip().endswith(ENDS) and cursor.box.x0 > col_left + 14:
                        break
                    members.append(l)
                    cursor = l
        for l in members:
            l.used = True
        region = region_box(reg, members)
        left = region.x0 + 2
        if reg["box"] is None:
            left = min((l.box.x0 for l in members if l.size >= 12), default=region.x0 + 2)
        else:
            # Text set in from the panel edge: its margin is the x where
            # most lines start.
            starts: dict[int, int] = {}
            for l in members:
                if l.size >= 12:
                    starts[round(l.box.x0 / 3)] = starts.get(round(l.box.x0 / 3), 0) + 1
            if starts:
                common = max(starts, key=lambda k: (starts[k], -k))
                if starts[common] >= 2 and common * 3 < region.x0 + 40:
                    left = min(l.box.x0 for l in members if round(l.box.x0 / 3) == common)
        inner = lines_to_blocks(page, sorted(members, key=lambda l: (l.box.y0, -l.box.x1)), left, col_right)
        for fb in [b for b in blocks if b.kind in ("figure", "table")]:
            if region.grow(2).contains_pt(fb.data["box"].cx, fb.data["box"].cy):
                inner.append(fb)
                blocks.remove(fb)
        for rbox, child in list(built):
            if child in blocks and region.grow(2).contains_pt(rbox.cx, rbox.cy) and rbox.w * rbox.h < region.w * region.h:
                inner.append(child)
                blocks.remove(child)
        inner.sort(key=lambda b: b.y)
        label = reg["label"] or ("" if reg["cont"] else "نکته")
        x1 = reg["badge"].x0 if reg["badge"] is not None else region.x1
        blk = Block("callout", region.y0, x1, text=label, children=inner, data={"cont": reg["cont"], "box": region})
        blocks.append(blk)
        built.append((region, blk))
    # The panel that reaches the page foot carries over to the next page.
    page.open_label = None
    for region, blk in built:
        if region.y1 > 680 and (blk.data["box"].w > 300):
            page.open_label = blk.text

    # Footnotes: small text under a short rule near the page bottom.
    rest = [l for l in page.lines if not l.used]
    foot_y = None
    for d in page.drawings:
        r = as_box(d["rect"])
        if r.y0 > 430 and r.h < 2 and r.w > 60 and d.get("color") and max(d["color"]) < 0.3:
            below = [l for l in rest if l.box.y0 > r.y0 - 1]
            if below and all(l.size <= 10.5 for l in below):
                foot_y = r.y0 if foot_y is None else min(foot_y, r.y0)
    foot = [l for l in rest if foot_y is not None and l.box.y0 > foot_y - 1 and l.size <= 11.5]
    for l in foot:
        l.used = True
    if foot:
        inner = lines_to_blocks(page, foot, col_left, col_right)
        blocks.append(Block("footnote", foot_y, col_right, children=inner))

    # Headings of module / unit openers.
    for l in page.lines:
        if l.used:
            continue
        if "Titr" in l.font and l.size >= 16:
            l.used = True
            blocks.append(Block("bigtitle", l.box.y0, l.box.x1, text=l.text.strip(), data={"size": l.size, "box": l.box}))
        elif l.bold and l.size >= 20:
            l.used = True
            blocks.append(Block("bigtitle", l.box.y0, l.box.x1, text=l.text.strip(), data={"size": l.size, "box": l.box}))

    # Body text.
    rest = sorted([l for l in page.lines if not l.used], key=lambda l: (l.box.y0, -l.box.x1))
    blocks.extend(lines_to_blocks(page, rest, col_left, col_right))

    # Leftover captions (no picture found): keep them as caption text.
    for b in blocks:
        if b.kind == "para" and CAPTION_RE.match(b.text.replace("*", "").strip()):
            b.kind = "orphan-caption"

    blocks.sort(key=lambda b: (b.y, -b.x1))
    return place_side_figures(blocks)


def place_side_figures(blocks: list[Block]) -> list[Block]:
    """A figure beside a paragraph goes after that paragraph, not inside it."""
    out = list(blocks)
    for fig in [b for b in blocks if b.kind in ("figure",)]:
        g = fig.data["box"]
        for para in blocks:
            if para.kind not in ("para", "bullet", "num", "lead") or not para.lines:
                continue
            top = para.lines[0].box.y0
            bottom = para.lines[-1].box.y1
            if top < g.y0 - 2 and bottom > g.y0 + 2:
                out.remove(fig)
                out.insert(out.index(para) + 1, fig)
                break
    return out


# ---------------------------------------------------------------- markdown

def fa_num(n: int | str) -> str:
    return str(n).translate(FA_DIGITS)


def caption_text(raw: str) -> str:
    m = CAPTION_RE.match(raw.replace("*", "").strip())
    if not m:
        return raw
    head = f"{m.group(1)} {fa_num(m.group(2).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')))}"
    if not m.group(3):
        return head
    # File and function names in a caption are code.
    parts = re.split(r"([A-Za-z_][\w-]*(?:[_.][\w-]+)+)", m.group(3))
    desc = "".join(f"`{p}`" if i % 2 else md_escape(p) for i, p in enumerate(parts))
    return f"{head}: {desc}"


def emit(blocks: list[Block], depth_prefix: str) -> list[str]:
    out: list[str] = []
    for b in blocks:
        out.extend(emit_block(b, depth_prefix))
    return out


def emit_block(b: Block, prefix: str) -> list[str]:
    k = b.kind
    if k == "para":
        return [b.text, ""]
    if k == "lead":
        text = b.text
        m = re.fullmatch(r"\*\*([^*]+?)\*\*\s*[:：]?\s*", text)
        if m and len(m.group(1)) < 120:
            return [f"### {m.group(1).strip().rstrip(':').strip()}", ""]
        return [text, ""]
    if k == "head2":
        return [f"## {b.text.replace('**', '').strip()}", ""]
    if k == "bullet":
        return [f"- {b.text}", ""]
    if k == "num":
        n = b.data.get("n", 1)
        return [f"{n}. {b.text}", ""]
    if k == "code":
        return ["```", b.text, "```", ""]
    if k == "figure":
        cap = caption_text(b.data["caption"]) if b.data["caption"] else ""
        alt = cap or "تصویر کتاب"
        sub = b.data.get("sub", "")
        if sub:
            alt = f"{alt}: {sub}" if cap else sub
        lines = [f"![{alt}]({prefix}images/{b.data['image']})"]
        if cap:
            lines.append(f"*{cap}*" + (f" — {md_escape(sub)}" if sub else ""))
        return lines + [""]
    if k == "table":
        lines = []
        cap = b.data.get("caption")
        if cap:
            lines += [f"*{caption_text(cap)}*", ""]
        if "rows" in b.data:
            if b.data.get("title"):
                lines += [f"**{b.data['title'].replace('**', '').strip()}**", ""]
            rows = b.data["rows"]
            width = max(len(r) for r in rows)
            for i, row in enumerate(rows):
                row = row + [""] * (width - len(row))
                lines.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")
                if i == 0:
                    lines.append("|" + " --- |" * width)
        else:
            lines.append(f"![{caption_text(cap) if cap else 'جدول'}]({prefix}images/{b.data['image']})")
        return lines + [""]
    if k == "callout":
        inner = emit(b.children, prefix)
        label = b.text
        if b.data.get("cont"):
            label = f"{label} (ادامه)" if label else "ادامه"
        lines = [f"> **{label}**", ">"]
        for l in "\n".join(inner).split("\n"):
            lines.append(("> " + l) if l else ">")
        while lines and lines[-1] == ">":
            lines.pop()
        return lines + [""]
    if k == "footnote":
        inner = emit(b.children, prefix)
        lines = ["> **پانویس**", ">"]
        for l in "\n".join(inner).split("\n"):
            lines.append(("> " + l) if l else ">")
        while lines and lines[-1] == ">":
            lines.pop()
        return lines + [""]
    if k == "orphan-caption":
        return [f"*{caption_text(b.text)}*", ""]
    if k == "bigtitle":
        return []
    return [b.text, ""]


# ---------------------------------------------------------------- book

def merge_across_pages(prev_blocks: list[Block], blocks: list[Block]) -> None:
    """Join a paragraph that the page break cut in two (pictures at the end
    of one page or the top of the next do not stop it)."""
    if not prev_blocks or not blocks:
        return
    last = next((b for b in reversed(prev_blocks) if b.kind not in ("figure", "table")), None)
    if last is None or last.kind not in ("para", "bullet", "num", "lead") or not last.open_end:
        return
    i = 0
    while i < len(blocks) and blocks[i].kind in ("figure", "table", "bigtitle"):
        i += 1
    if i >= len(blocks) or blocks[i].kind != "para":
        return
    first = blocks[i]
    if first.text.startswith("**"):
        return  # «**مثال**: ...» opens its own paragraph
    last.text = last.text + " " + first.text
    last.open_end = first.open_end
    blocks.pop(i)


class Book:
    def __init__(self) -> None:
        self.files: dict[str, list[str]] = {}
        self.titles: dict[str, str] = {}
        self.order: list[str] = []
        self.current = "00-front-matter.md"
        self.module_i = -1
        self.unit_i = -1
        self._touch(self.current, "شناسنامه و مقدمه کتاب")

    def _touch(self, path: str, title: str) -> None:
        if path not in self.files:
            self.files[path] = [f"# {title}", ""]
            self.titles[path] = title
            self.order.append(path)

    def switch(self, path: str, title: str) -> None:
        self._touch(path, title)
        self.current = path

    def prefix(self) -> str:
        return "../" * self.current.count("/")


def module_opener(blocks: list[Block]) -> tuple[str, str] | None:
    big = [b for b in blocks if b.kind == "bigtitle"]
    pod = next((b for b in big if b.text.startswith("پودمان")), None)
    if not pod:
        return None
    rest = [b for b in big if b is not pod]
    title = rest[0].text if rest else ""
    return pod.text, title


def unit_opener(blocks: list[Block]) -> str | None:
    for b in blocks:
        if b.kind == "bigtitle" and "واحد یادگیری" in b.text:
            return b.text
    return None


ORDINALS = {"اول": 1, "دوم": 2, "سوم": 3, "چهارم": 4, "پنجم": 5}


def convert() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    IMG_DIR.mkdir(parents=True)
    doc = pymupdf.open(PDF_PATH)
    book = Book()
    prev_blocks: list[Block] = []
    image_count = 0

    for index in range(doc.page_count):
        pno = index + 1
        counter = {"n": 0}
        page = load_page(doc, index)

        def image_name(box: Box, page=page, counter=counter) -> str:
            counter["n"] += 1
            name = f"p{page.number:03d}-{counter['n']:02d}.png"
            clip = pymupdf.Rect(box.x0 - 2, box.y0 - 2, box.x1 + 2, box.y1 + 2) & page.pdf.rect
            adjust = IMAGE_CLIPS.get(name)
            if adjust:
                clip = pymupdf.Rect(clip.x0 + adjust[0], clip.y0 + adjust[1], clip.x1 + adjust[2], clip.y1 + adjust[3]) & page.pdf.rect
            pix = page.pdf.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=clip, alpha=False)
            for x0, y0, x1, y1 in IMAGE_MASKS.get(name, []):
                # set_rect uses the pixmap's own device coordinates, which start at (pix.x, pix.y).
                pix.set_rect(pymupdf.IRect(pix.x + x0, pix.y + y0, pix.x + x1, pix.y + y1), (255, 255, 255))
            pix.save(IMG_DIR / name)
            return name

        blocks = page_blocks(page, image_name, getattr(book, "open_label", None))
        book.open_label = page.open_label
        image_count += counter["n"]

        # File routing.
        if pno in (4, 5, 6):
            book.switch("00-toc.md", "فهرست")
        opener = module_opener(blocks)
        if opener and pno > 6:
            book.module_i += 1
            book.unit_i = -1
            folder = MODULE_DIRS[book.module_i]
            pod, title = opener
            book.switch(f"{folder}/00-intro.md", f"{pod}: {title}" if title else pod)
        unit = unit_opener(blocks)
        if unit and not opener:
            book.unit_i += 1
            folder = MODULE_DIRS[book.module_i]
            slug = UNIT_SLUGS[book.module_i][book.unit_i]
            title = next((b.text for b in blocks if b.kind == "head2"), "")
            # A unit opener prints «واحد یادگیری N» and then the unit title.
            big_titles = [b.text for b in blocks if b.kind == "bigtitle" and "واحد یادگیری" not in b.text]
            title = big_titles[0] if big_titles else title
            book.switch(f"{folder}/{slug}.md", title or unit)
        if pno > 300 and book.current != "06-references.md":
            if any(b.text.replace("*", "").strip().rstrip(":：").strip() == "منابع" for b in blocks if b.kind in ("head2", "para", "lead")):
                book.switch("06-references.md", "منابع")

        if getattr(book, "_last_file", None) == book.current:
            merge_across_pages(prev_blocks, blocks)
        book_page = pno - PDF_TO_BOOK_PAGE if pno > PDF_TO_BOOK_PAGE else 0
        book.pages_out = getattr(book, "pages_out", [])
        book.pages_out.append((book.current, pno, book_page, blocks))
        prev_blocks = blocks
        book._last_file = book.current
        if (pno % 25) == 0:
            print(f"page {pno}/{doc.page_count}", flush=True)

    # Emit after all merging is done.
    for path, pno, book_page, blocks in book.pages_out:
        prefix = "../" * path.count("/")
        lines = book.files[path]
        marker = f"<!-- page {book_page} -->" if book_page else f"<!-- pdf-page {pno} -->"
        lines += [marker, ""]
        if pno in PAGE_OVERRIDES:
            lines += [PAGE_OVERRIDES[pno], ""]
            continue
        unit = unit_opener(blocks)
        if unit and not module_opener(blocks):
            lines += [f"## {unit}", ""]
        lines += emit(blocks, prefix)

    fixes = {}
    for rel, old, new in FIXES:
        fixes.setdefault(rel, []).append((old, new))
    for rel, lines in book.files.items():
        path = OUT_DIR / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
        for old, new in fixes.pop(rel, []):
            if text.count(old) != 1:
                print(f"book_fixes: {rel}: found {text.count(old)}x: {old}")
            text = text.replace(old, new)
        for frel, pattern, repl in REGEX_FIXES:
            if frel == rel:
                text, n = re.subn(pattern, repl, text)
                if not n:
                    print(f"book_fixes: {rel}: pattern unused: {pattern}")
        path.write_text(text, encoding="utf-8")
    for rel, items in fixes.items():
        print(f"book_fixes: no file {rel} ({len(items)} fixes)")
    # Drop crops that no page uses (pages replaced by PAGE_OVERRIDES).
    used = set()
    for md in OUT_DIR.rglob("*.md"):
        used.update(re.findall(r"images/([\w.-]+\.png)", md.read_text(encoding="utf-8")))
    for png in IMG_DIR.iterdir():
        if png.name not in used:
            png.unlink()
            image_count -= 1
    write_readme(book, doc.page_count, image_count)
    print("files", len(book.order), "images", image_count)


def write_readme(book: Book, pages: int, images: int) -> None:
    rows = "\n".join(f"- [{book.titles[p]}]({p})" for p in book.order)
    (OUT_DIR / "README.md").write_text(
        f"""# کتاب طراح سایت — پایه یازدهم

متن کتاب درسی «طراح سایت» (رشته شبکه و نرم\u200cافزار رایانه، پایه یازدهم) که با `convert_book.py` از PDF به مارک\u200cداون تبدیل شده است.

- منبع: `original-reference/11th-grade-programming-book.pdf` ({fa_num(pages)} صفحه)
- تصویرها: {fa_num(images)} فایل در `images/`
- شماره صفحه\u0654 چاپی کتاب به\u200cصورت `<!-- page N -->` بالای هر صفحه آمده است.
- قاب\u200cهای کتاب (نکته، فعالیت، کنجکاوی و ...) به\u200cصورت نقل\u200cقولی آمده\u200cاند که سطر اول آن نام قاب است.
- هر شکل یک تصویر کامل از همان ناحیه\u0654 صفحه است و زیرنویس «شکل N» زیر آن آمده است.

## فایل\u200cها

{rows}
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    convert()
