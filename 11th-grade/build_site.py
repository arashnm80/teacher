#!/usr/bin/env python3
"""Build the offline bilingual site.

Persian lesson text is sliced from converted-markdown-book/ using outline.py.
English lesson text is the matching file in sections/en/. Both are written
into each HTML page so the folder still works with no internet. See
REQUIREMENTS.md.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import zipfile
from pathlib import Path

import markdown

from outline import MODULES, SECTIONS
from repair_markdown import repair_markdown

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "converted-markdown-book"
SITE = ROOT / "site"
WEB = ROOT / "web"
EN_DIR = ROOT / "sections" / "en"
FA_DIR = ROOT / "sections" / "fa"

PAGE_RE = re.compile(r"^\*\*صفحه\s*([۰-۹0-9]+)\*\*\s*$", re.M)
TAG_RE = re.compile(r"(<[^>]+>)")
LATIN_RE = re.compile(
    r"(?<![\w/])(?:\([A-Za-z0-9][^()\n]{0,80}\)|[A-Za-z][A-Za-z0-9_+#./:\\-]*)"
)
ARABIC_RE = re.compile(
    r"[\u0600-\u06FF](?:[\u0600-\u06FF\u200c\u064b-\u0652]|[ \t])+[\u0600-\u06FF]|[\u0600-\u06FF]{2,}"
)
ENTITY_RE = re.compile(r"(&[A-Za-z]+;|&#\d+;|&#x[0-9A-Fa-f]+;)")
PAGE_MARK_RE = re.compile(
    r"<p><strong>((?:صفحه|Page)\s+[^<]+)</strong></p>"
)
FIGURE_RE = re.compile(
    r"<p>(<img\b[^>]*>)\s*</p>\s*<p><strong>((?:شکل|Figure|تصویر)[^<]*)</strong></p>",
    re.I,
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rel(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent).replace(os.sep, "/")


def page_number(raw: str) -> int:
    return int(raw.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")))


def pages_in(text: str) -> dict[int, str]:
    matches = list(PAGE_RE.finditer(text))
    if not matches:
        raise SystemExit("a lesson file has no صفحه markers")
    found: dict[int, str] = {}
    preamble = text[: matches[0].start()].strip()
    for index, match in enumerate(matches):
        number = page_number(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = text[match.start() : end].strip()
        if index == 0 and preamble:
            chunk = preamble + "\n\n" + chunk
        found[number] = chunk
    return found


def section_markdown(section: dict) -> str:
    text = (BOOK / section["file"]).read_text(encoding="utf-8")
    found = pages_in(text)
    parts = []
    for number in range(section["start"], section["end"] + 1):
        if number not in found:
            raise SystemExit(f"{section['id']} is missing book page {number}")
        parts.append(found[number])
    return "\n\n".join(parts).strip() + "\n"


def export_fa() -> None:
    FA_DIR.mkdir(parents=True, exist_ok=True)
    for section in SECTIONS:
        (FA_DIR / f"{section['id']}.md").write_text(
            section_markdown(section), encoding="utf-8"
        )


def render_markdown(text: str, image_prefix: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "toc"])
    body = converter.convert(text)

    def image(match: re.Match[str]) -> str:
        name = match.group(1).split("/")[-1]
        return f'src="{image_prefix}/{name}"'

    body = re.sub(r'src="(?:\.\./)*images/([^"]+)"', image, body)
    body = PAGE_MARK_RE.sub(r'<p class="page-mark">\1</p>', body)
    body = FIGURE_RE.sub(
        r'<figure class="shot">\1<figcaption>\2</figcaption></figure>',
        body,
    )
    body = body.replace("<pre>", '<div class="code-wrap" dir="ltr"><pre>').replace(
        "</pre>", "</pre></div>"
    )
    return box_callouts(body)


# The book prints کنجکاوی / پروژه / نکته / فعالیت as tinted side boxes.
# Their markdown is an h3 followed by the box content, so wrap that range
# in an aside with its own background color.
CALLOUT_KINDS = (
    ("curiosity", ("کنجکاوی", "try this")),
    ("project", ("پروژه", "project")),
    ("note", ("نکته", "note")),
    ("activity", ("فعالیت", "activity")),
)
# "Quiz game project" is a book callout even though the keyword comes last.
CALLOUT_TAIL = {"quiz game project"}
CALLOUT_END_RE = re.compile(r"<(?:h[123][ >]|hr[ >])", re.I)


def box_callouts(body: str) -> str:
    out: list[str] = []
    pos = 0
    for match in re.finditer(r"<h3\b[^>]*>(.*?)</h3>", body, re.S):
        title = re.sub(r"<[^>]+>", "", match.group(1)).strip().lower()
        kind = ""
        for name, keys in CALLOUT_KINDS:
            if title.startswith(keys) or (name == "project" and title in CALLOUT_TAIL):
                kind = name
                break
        if not kind:
            continue
        end = CALLOUT_END_RE.search(body, match.end())
        stop = end.start() if end else len(body)
        out.append(body[pos : match.start()])
        out.append(
            f'<aside class="callout {kind}">{body[match.start() : stop]}</aside>'
        )
        pos = stop
    out.append(body[pos:])
    return "".join(out)


def isolate_bidi(fragment: str, lang: str) -> str:
    """Keep mixed Persian/English lines in reading order."""
    parts = TAG_RE.split(fragment)
    out: list[str] = []
    skip = 0
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<pre", "<code", "<script")):
                skip += 1
            elif low.startswith(("</pre", "</code", "</script")):
                skip = max(0, skip - 1)
            out.append(part)
            continue
        if skip or not part:
            out.append(part)
            continue
        pattern = LATIN_RE if lang == "fa" else ARABIC_RE
        direction = "ltr" if lang == "fa" else "rtl"

        def wrap(piece: str, pattern: re.Pattern[str] = pattern, direction: str = direction) -> str:
            return pattern.sub(
                lambda match: f'<bdi dir="{direction}">{match.group(0)}</bdi>',
                piece,
            )

        pieces = ENTITY_RE.split(part)
        out.append("".join(wrap(piece) if index % 2 == 0 else piece for index, piece in enumerate(pieces)))
    return "".join(out)


def module_by_id(module_id: str) -> dict:
    for module in MODULES:
        if module["id"] == module_id:
            return module
    raise SystemExit(f"unknown module {module_id}")


def flatten() -> list[dict]:
    pages = []
    for section in SECTIONS:
        module = module_by_id(section["module"])
        pages.append(
            {
                **section,
                "out": SITE / "book" / f"{section['id']}.html",
                "module_fa": module["fa"],
                "module_en": module["en"],
                "blurb_fa": module["blurb_fa"],
                "blurb_en": module["blurb_en"],
                "home": module["home"],
            }
        )
    return pages


def chrome(page_path: Path, title_fa: str, title_en: str, pages: list[dict], body: str) -> str:
    assets = rel(page_path, SITE / "assets" / "style.css") + "?v=6"
    script = rel(page_path, SITE / "assets" / "app.js") + "?v=6"
    search = rel(page_path, SITE / "assets" / "search-index.js") + "?v=6"
    home = rel(page_path, SITE / "index.html")
    favicon = rel(page_path, SITE / "assets" / "favicon.svg")
    package = rel(page_path, SITE / "grade11-offline.zip") + "?v=2"
    to_home = rel(page_path, SITE / "index.html")
    root = "" if to_home == "index.html" else to_home[: -len("index.html")]

    nav = [
        '<details class="toc" open>',
        '<summary><span data-fa="فهرست درس‌ها" data-en="Lesson list">فهرست درس‌ها</span></summary>',
        '<nav class="side" aria-label="lessons">',
    ]
    last_module = None
    last_unit = None
    for item in pages:
        if item["module_fa"] != last_module:
            nav.append(
                f'<p class="mod" data-fa="{esc(item["module_fa"])}" data-en="{esc(item["module_en"])}">'
                f"{esc(item['module_fa'])}</p>"
            )
            last_module = item["module_fa"]
            last_unit = None
        if item["unit_fa"] != last_unit:
            nav.append(
                f'<p class="unit" data-fa="{esc(item["unit_fa"])}" data-en="{esc(item["unit_en"])}">'
                f"{esc(item['unit_fa'])}</p>"
            )
            last_unit = item["unit_fa"]
        href = rel(page_path, item["out"])
        current = " current" if item["out"] == page_path else ""
        nav.append(
            f'<a class="{current.strip()}" href="{href}" '
            f'data-fa="{esc(item["fa"])}" data-en="{esc(item["en"])}">'
            f"{esc(item['fa'])}</a>"
        )
    nav.append("</nav></details>")

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title data-fa="{esc(title_fa)}" data-en="{esc(title_en)}">{esc(title_fa)}</title>
  <link rel="icon" href="{favicon}">
  <link rel="stylesheet" href="{assets}">
</head>
<body data-root="{root}">
  <header class="top">
    <a class="brand" href="{home}">
      <span data-fa="طراح سایت" data-en="Site Design">طراح سایت</span>
      <small data-fa="پایه یازدهم" data-en="Grade 11">پایه یازدهم</small>
    </a>
    <div class="search-wrap">
      <input id="q" type="search" autocomplete="off"
        data-fa-placeholder="جستجو در درس‌ها" data-en-placeholder="Search lessons"
        placeholder="جستجو در درس‌ها">
      <div id="results" class="results" hidden></div>
    </div>
    <a class="download" href="{package}" data-fa="دانلود کل سایت" data-en="Download the whole site">دانلود کل سایت</a>
    <button type="button" id="lang-toggle" class="lang-toggle" dir="ltr" data-lang="fa"
      aria-label="تغییر زبان">
      <span data-opt="fa">فا</span>
      <span data-opt="en">EN</span>
    </button>
  </header>
  <div class="layout">
    {''.join(nav)}
    <div class="main">
      {body}
    </div>
  </div>
  <script src="{search}"></script>
  <script src="{script}"></script>
</body>
</html>
"""


def home_body(pages: list[dict], here: Path) -> str:
    package = rel(here, SITE / "grade11-offline.zip") + "?v=2"
    cards = []
    seen = set()
    number = 0
    for item in pages:
        if not item["home"] or item["module"] in seen:
            continue
        seen.add(item["module"])
        number += 1
        href = rel(here, item["out"])
        cards.append(
            f'''<a class="card" href="{href}">
              <span class="num">{number}</span>
              <h2 data-fa="{esc(item["module_fa"])}" data-en="{esc(item["module_en"])}">{esc(item["module_fa"])}</h2>
              <p data-fa="{esc(item["blurb_fa"])}" data-en="{esc(item["blurb_en"])}">{esc(item["blurb_fa"])}</p>
            </a>'''
        )
    fa = """
      <p class="kicker">کتاب درسی هنرستان</p>
      <h1>طراح سایت</h1>
      <p class="lede">پایه یازدهم، رشته شبکه و نرم‌افزار رایانه. متن کتاب به فارسی و انگلیسی در همین پوشه است. اینترنت لازم نیست.</p>
      <div class="steps">
        <div><strong>۱. کپی یا دانلود</strong>پوشه را کپی کنید، یا از دکمه بالای صفحه فایل فشرده را بگیرید و باز کنید.</div>
        <div><strong>۲. باز کردن</strong>فایل index.html را با دوبار کلیک باز کنید.</div>
        <div><strong>۳. زبان</strong>دکمه فا / EN را از هر جای آن بزنید تا همه متن عوض شود.</div>
      </div>
    """
    en = """
      <p class="kicker">Vocational textbook</p>
      <h1>Site Design</h1>
      <p class="lede">Grade 11, computer networking and software. The book is here in Persian and English. No internet is required to read it.</p>
      <div class="steps">
        <div><strong>1. Copy or download</strong>Copy the folder, or use the button above to download the zip and unpack it.</div>
        <div><strong>2. Open</strong>Double-click index.html.</div>
        <div><strong>3. Language</strong>Click the فا / EN control anywhere on it. The whole page switches.</div>
      </div>
    """
    return f"""
      <section class="hero">
        <div data-lang-block="fa">{fa}</div>
        <div data-lang-block="en" hidden>{en}</div>
        <a class="download-banner" href="{package}">
          <strong data-fa="دانلود کل سایت برای استفاده آفلاین" data-en="Download the whole site for offline use">دانلود کل سایت برای استفاده آفلاین</strong>
          <span data-fa="فایل فشرده را باز کنید و index.html را اجرا کنید. بعد از آن اینترنت و فیلترشکن لازم نیست." data-en="Unzip the file and open index.html. After that, the pages work with no internet and no VPN.">فایل فشرده را باز کنید و index.html را اجرا کنید. بعد از آن اینترنت و فیلترشکن لازم نیست.</span>
        </a>
        <div class="grid">{''.join(cards)}</div>
      </section>
    """


def pager_link(page_path: Path, item: dict, rel_name: str, word_fa: str, word_en: str) -> str:
    return (
        f'<a rel="{rel_name}" class="{rel_name}" href="{rel(page_path, item["out"])}">'
        f'<span class="pager-word" data-fa="{esc(word_fa)}" data-en="{esc(word_en)}">{esc(word_fa)}</span>'
        f'<span class="pager-name" data-fa="{esc(item["fa"])}" data-en="{esc(item["en"])}">{esc(item["fa"])}</span>'
        f"</a>"
    )


def pager(page_path: Path, pages: list[dict], index: int) -> str:
    parts = ['<nav class="pager">']
    if index > 0:
        parts.append(pager_link(page_path, pages[index - 1], "prev", "قبلی", "Previous"))
    else:
        parts.append("<span></span>")
    if index + 1 < len(pages):
        parts.append(pager_link(page_path, pages[index + 1], "next", "بعدی", "Next"))
    parts.append("</nav>")
    return "".join(parts)


# The printed contents page is a dotted leader line. Those lines fall apart
# once Persian, English, and the page number share one paragraph.
CONTENTS = [
    ("module", "پودمان اول: برنامه‌نویسی پایتون", "Module 1: Python programming", "1", "p1-intro"),
    ("unit", "واحد یادگیری ۱. مدل‌سازی داده", "Unit 1. Data modeling", "2", "p1-python"),
    ("unit", "واحد یادگیری ۲. کار با توابع و ماژول‌ها", "Unit 2. Working with functions and modules", "48", "p1-sets"),
    ("module", "پودمان دوم: طراحی صفحات وب ایستا", "Module 2: Designing static web pages", "83", "p2-intro"),
    ("unit", "واحد یادگیری ۱. طراحی ساختار صفحات وب با HTML", "Unit 1. Designing web page structure with HTML", "84", "p2-web"),
    ("unit", "واحد یادگیری ۲. طراحی ظاهر صفحات وب با CSS", "Unit 2. Designing web page appearance with CSS", "116", "p2-css-start"),
    ("module", "پودمان سوم: تولید صفحات وب تعاملی", "Module 3: Producing interactive web pages", "145", "p3-intro"),
    ("unit", "واحد یادگیری ۱. توسعه صفحات وب تعاملی با بوت‌استرپ", "Unit 1. Developing interactive pages with Bootstrap", "146", "p3-bs-start"),
    ("unit", "واحد یادگیری ۲. طراحی صفحات وب تعاملی با جاوااسکریپت", "Unit 2. Designing interactive pages with JavaScript", "192", "p3-js-start"),
    ("module", "پودمان چهارم: توسعه وب پایتون", "Module 4: Python web development", "233", "p4-intro"),
    ("unit", "واحد یادگیری ۱. تولید برنامه شیءگرا", "Unit 1. Producing an object-oriented program", "234", "p4-idea"),
    ("unit", "واحد یادگیری ۲. توسعه برنامه شیءگرا", "Unit 2. Developing an object-oriented program", "254", "p4-files"),
    ("module", "پودمان پنجم: برنامه‌نویسی جنگو", "Module 5: Django programming", "275", "p5-intro"),
    ("unit", "واحد یادگیری ۱. ایجاد وب‌اپلیکیشن", "Unit 1. Creating a web application", "276", "p5-what"),
    ("unit", "واحد یادگیری ۲. توسعه وب‌اپلیکیشن", "Unit 2. Developing a web application", "295", "p5-model"),
    ("module", "منابع", "References", "330", "refs"),
]


def contents_html() -> str:
    rows = []
    for kind, fa, en, page, target in CONTENTS:
        rows.append(
            f'<li class="{kind}"><a href="{esc(target)}.html">'
            f'<span class="label" data-fa="{esc(fa)}" data-en="{esc(en)}">{esc(fa)}</span>'
            f'<span class="page">{esc(page)}</span>'
            f"</a></li>"
        )
    return f'<ol class="contents">{"".join(rows)}</ol>'


def extra_block(section: dict) -> str:
    items = []
    for fa, en in zip(section["ex_fa"], section["ex_en"]):
        items.append(
            f'<li data-fa="{esc(fa)}" data-en="{esc(en)}">{esc(fa)}</li>'
        )
    if not items and not section["link"]:
        return ""
    links = ""
    if section["link"]:
        href, label_fa, label_en = section["link"]
        links = (
            f'<h2 data-fa="پیوند مفید" data-en="Useful link">پیوند مفید</h2>'
            f'<ul><li><a href="{esc(href)}" data-fa="{esc(label_fa)}" data-en="{esc(label_en)}">{esc(label_fa)}</a></li></ul>'
        )
    return f"""
      <aside class="extra">
        <h2 data-fa="تمرین این بخش" data-en="Exercises for this section">تمرین این بخش</h2>
        <p class="extra-note" data-fa="این تمرین‌ها و پیوندها اضافه بر متن کتاب‌اند." data-en="These exercises and links are in addition to the book.">این تمرین‌ها و پیوندها اضافه بر متن کتاب‌اند.</p>
        <ol>{''.join(items)}</ol>
        {links}
      </aside>
    """


def plain_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def link_images() -> int:
    source = BOOK / "images"
    target = SITE / "images"
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in sorted(source.iterdir()):
        if not src.is_file():
            continue
        dest = target / src.name
        try:
            os.link(src, dest)
        except OSError:
            shutil.copy2(src, dest)
        count += 1
    return count


def guard(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    if re.search(r"<script[^>]+src=['\"]https?:", text, re.I):
        raise SystemExit(f"remote script in {html_path}")
    if re.search(r"<link[^>]+href=['\"]https?:", text, re.I):
        raise SystemExit(f"remote stylesheet in {html_path}")
    for match in re.finditer(r'<img[^>]+src="([^"]+)"', text):
        src = match.group(1)
        if src.startswith(("http://", "https://", "data:")):
            raise SystemExit(f"remote image in {html_path}: {src}")
        target = (html_path.parent / src).resolve()
        if not target.is_file():
            raise SystemExit(f"missing image {src} from {html_path}")


def write_zip() -> None:
    target = SITE / "grade11-offline.zip"
    temporary = ROOT / ".grade11-offline.zip"
    if temporary.exists():
        temporary.unlink()
    with zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as archive:
        for path in sorted(SITE.rglob("*")):
            if not path.is_file() or path.suffix == ".zip":
                continue
            arcname = Path("grade11-site") / path.relative_to(SITE)
            archive.write(path, arcname.as_posix())
    shutil.move(temporary, target)


def english_markdown(section: dict) -> str:
    path = EN_DIR / f"{section['id']}.md"
    if not path.is_file():
        raise SystemExit(f"missing English transcription: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    pages = flatten()
    export_fa()
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    shutil.copy2(WEB / "style.css", SITE / "assets" / "style.css")
    shutil.copy2(WEB / "app.js", SITE / "assets" / "app.js")
    (SITE / "assets" / "favicon.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0c2f2c"/>
  <rect x="6" y="8" width="20" height="14" rx="2" fill="#f4faf8"/>
  <path d="M10 26h12" stroke="#f4faf8" stroke-width="2"/>
</svg>
""",
        encoding="utf-8",
    )
    images = link_images()

    search = []
    for index, item in enumerate(pages):
        prefix = rel(item["out"], SITE / "images")
        if item["id"] == "toc":
            fa_html = en_html = contents_html()
        else:
            fa_html = isolate_bidi(render_markdown(repair_markdown(section_markdown(item), "fa"), prefix), "fa")
            en_html = isolate_bidi(render_markdown(repair_markdown(english_markdown(item), "en"), prefix), "en")
        title = (
            f'<h1 class="section-title" data-fa="{esc(item["fa"])}" data-en="{esc(item["en"])}">'
            f"{esc(item['fa'])}</h1>"
        )
        body = (
            title
            + f'<article class="lesson" lang="fa" dir="rtl" data-lang-block="fa">{fa_html}</article>'
            + f'<article class="lesson" lang="en" dir="ltr" data-lang-block="en" hidden>{en_html}</article>'
            + extra_block(item)
            + pager(item["out"], pages, index)
        )
        item["out"].parent.mkdir(parents=True, exist_ok=True)
        item["out"].write_text(
            chrome(item["out"], item["fa"], item["en"], pages, body),
            encoding="utf-8",
        )
        search.append(
            {
                "href": rel(SITE / "index.html", item["out"]),
                "titleFa": item["fa"],
                "titleEn": item["en"],
                "textFa": " ".join(row[1] for row in CONTENTS) if item["id"] == "toc" else plain_text(fa_html),
                "textEn": " ".join(row[2] for row in CONTENTS) if item["id"] == "toc" else plain_text(en_html),
            }
        )
        guard(item["out"])

    index_path = SITE / "index.html"
    index_path.write_text(
        chrome(index_path, "طراح سایت", "Site Design", pages, home_body(pages, index_path)),
        encoding="utf-8",
    )
    guard(index_path)

    payload = json.dumps(search, ensure_ascii=False).replace("<", "\\u003c")
    (SITE / "assets" / "search-index.js").write_text(
        "window.BOOK_SEARCH = " + payload + ";\n",
        encoding="utf-8",
    )
    (SITE / "README.md").write_text(
        """# طراح سایت — نسخه آفلاین کلاس

کل همین پوشه را به رایانه کلاس کپی کنید و `index.html` را با دوبار کلیک باز کنید. اینترنت لازم نیست.

فایل `grade11-offline.zip` برای دانلود از سایت است. داخل خودِ فایل فشرده نیست، تا دانش‌آموز بعد از باز کردن، یک پوشه ساده داشته باشد.

# Site Design — offline classroom copy

Copy this whole folder onto a lab PC and double-click `index.html`. No internet is required.

`grade11-offline.zip` is the download offered on the public site. It is not packed inside itself.
""",
        encoding="utf-8",
    )
    write_zip()
    print(f"pages {len(pages) + 1} images {images}")


if __name__ == "__main__":
    main()
