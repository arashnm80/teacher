#!/usr/bin/env python3
"""Build the offline bilingual site.

Persian lesson text is sliced from converted-markdown-book/ using outline.py.
English lesson text is the matching file in sections/en/. Both are written
into each HTML page so the folder still works with no internet. See
REQUIREMENTS.md.
"""

from __future__ import annotations

import gzip
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import zipfile
from pathlib import Path

import markdown

from outline import MODULES, SECTIONS

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "converted-markdown-book"
SITE = ROOT / "site"
WEB = ROOT / "web"
EN_DIR = ROOT / "sections" / "en"
FA_DIR = ROOT / "sections" / "fa"

PAGE_RE = re.compile(r"^<!-- page (\d+) -->\s*$", re.M)
TAG_RE = re.compile(r"(<[^>]+>)")
# An English run inside Persian text: from a Latin letter to the last Latin
# letter, digit, or closing mark before the next Persian word.
LATIN_RE = re.compile(
    r"[\"“]?[A-Za-z][A-Za-z0-9_.\-+#/:\\'\"“”’()\[\]{}=;,!?@$%*\s]*[A-Za-z0-9)\]}\"”’!?%]|[\"“]?[A-Za-z]"
)
ARABIC_RE = re.compile(
    r"[؀-ۿ](?:[؀-ۿ‌ً-ْ]|[ \t])+[؀-ۿ]|[؀-ۿ]{2,}"
)
ENTITY_RE = re.compile(r"(&[A-Za-z]+;|&#\d+;|&#x[0-9A-Fa-f]+;)")
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rel(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent).replace(os.sep, "/")


def pages_in(text: str) -> dict[int, str]:
    """Split a converted chapter at its «<!-- page N -->» markers."""
    matches = list(PAGE_RE.finditer(text))
    if not matches:
        raise SystemExit("a chapter file has no page markers")
    found: dict[int, str] = {}
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        found[number] = text[match.start() : end].strip()
    return found


RUBRIC_RE = re.compile(r"^## ارزشیابی شایستگی", re.M)


def drop_rubric(text: str) -> str:
    """Keep the «ارزشیابی شایستگی» heading and its standard; drop the
    scoring rubric that follows (REQUIREMENTS: not part of the site)."""
    match = RUBRIC_RE.search(text)
    if not match:
        return text
    head, rest = text[: match.start()], text[match.start() :]
    kept = []
    for block in re.split(r"\n\s*\n", rest):
        stripped = block.strip()
        if stripped.startswith(("![", "|", "> **پانویس")) or (kept and stripped.startswith("<!-- page")):
            break
        kept.append(block)
    return head + "\n\n".join(kept).rstrip() + "\n"


def section_markdown(section: dict) -> str:
    text = (BOOK / section["file"]).read_text(encoding="utf-8")
    found = pages_in(text)
    parts = []
    for number in range(section["start"], section["end"] + 1):
        if number not in found:
            raise SystemExit(f"{section['id']} is missing book page {number}")
        parts.append(found[number])
    return drop_rubric("\n\n".join(parts).strip() + "\n")


def export_fa() -> None:
    FA_DIR.mkdir(parents=True, exist_ok=True)
    for section in SECTIONS:
        if section.get("custom") or section["id"] == "toc":
            continue
        (FA_DIR / f"{section['id']}.md").write_text(
            section_markdown(section), encoding="utf-8"
        )


CALLOUT_KINDS = {
    "نکته": "note", "توجه": "note", "note": "note",
    "فعالیت": "activity", "activity": "activity",
    "کنجکاوی": "curiosity", "curiosity": "curiosity", "try this": "curiosity",
    "کار کارگاهی": "workshop", "workshop": "workshop",
    "مثال": "example", "example": "example",
    "بیشتر بدانید": "more", "learn more": "more",
    "پروژه": "project", "project": "project",
    "پانویس": "footnote", "footnote": "footnote", "footnotes": "footnote",
}
CALLOUT_OPEN_RE = re.compile(r"<blockquote>\s*<p><strong>([^<]{1,40})</strong></p>", re.S)


def callout_kind(label: str) -> str:
    key = label.strip().lower()
    key = re.sub(r"\s*\((ادامه|continued)\)$", "", key)
    return CALLOUT_KINDS.get(key, "note")


def box_callouts(body: str) -> str:
    """«> **نکته**» blockquotes become tinted boxes like the book's."""
    out: list[str] = []
    stack: list[bool] = []
    pos = 0
    for match in re.finditer(r"<blockquote>|</blockquote>", body):
        out.append(body[pos : match.start()])
        pos = match.end()
        if match.group(0) == "<blockquote>":
            labelled = CALLOUT_OPEN_RE.match(body, match.start())
            if labelled:
                label = labelled.group(1).strip()
                kind = callout_kind(label)
                cont = " continued" if re.search(r"\((ادامه|continued)\)$", label) else ""
                out.append(f'<aside class="callout {kind}{cont}"><p class="callout-label">{label}</p>')
                pos = labelled.end()
                stack.append(True)
            else:
                out.append("<blockquote>")
                stack.append(False)
        else:
            out.append("</aside>" if (stack.pop() if stack else False) else "</blockquote>")
    out.append(body[pos:])
    return "".join(out)


FIGURE_RE = re.compile(
    r"<p>(<img\b[^>]*>)\s*(?:<br\s*/?>\s*)?<em>((?:شکل|Figure)[^<]*)</em>([^<]*)</p>"
)
TABLE_CAP_RE = re.compile(r"<p><em>((?:جدول|Table|شکل|Figure)\s[^<]*)</em></p>")


QUOTED_FENCE_RE = re.compile(r"^((?:> ?)+)```[^\n]*\n(.*?)^\1```[ \t]*$", re.M | re.S)


def quoted_fences(text: str) -> str:
    """Python-Markdown cannot see a ``` fence inside «> » quotes; turn it
    into an indented code block, which it does read there."""

    def repl(match: re.Match[str]) -> str:
        prefix = match.group(1).rstrip() + " "
        body = []
        for line in match.group(2).rstrip("\n").split("\n"):
            stripped = line[len(match.group(1)):] if line.startswith(match.group(1)) else line.lstrip("> ")
            body.append(prefix + "    " + stripped)
        return prefix.rstrip() + "\n" + "\n".join(body) + "\n" + prefix.rstrip()

    return QUOTED_FENCE_RE.sub(repl, text)


def render_markdown(text: str, image_prefix: str, lang: str) -> str:
    def page_mark(match: re.Match[str]) -> str:
        number = match.group(1)
        label = f"صفحه {number.translate(FA_DIGITS)}" if lang == "fa" else f"Page {number}"
        return f'\n<p class="page-mark">{label}</p>\n'

    text = PAGE_RE.sub(page_mark, text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = quoted_fences(text)
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])
    body = converter.convert(text)

    def image(match: re.Match[str]) -> str:
        name = match.group(1).split("/")[-1]
        return f'src="{image_prefix}/{name}" loading="lazy"'

    body = re.sub(r'src="(?:\.\./)*images/([^"]+)"', image, body)
    body = FIGURE_RE.sub(
        lambda m: f'<figure class="shot">{m.group(1)}<figcaption>{m.group(2)}{m.group(3)}</figcaption></figure>',
        body,
    )
    body = re.sub(r"<p>(<img\b[^>]*>)</p>", r'<figure class="shot">\1</figure>', body)
    body = TABLE_CAP_RE.sub(r'<p class="table-cap">\1</p>', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = body.replace("<pre>", '<div class="code-wrap" dir="ltr"><pre>').replace(
        "</pre>", "</pre></div>"
    )
    return box_callouts(body)


def isolate_bidi(fragment: str, lang: str) -> str:
    """Keep mixed Persian/English lines in reading order: every English run
    in Persian text (and every Persian run in English text) is isolated."""
    parts = TAG_RE.split(fragment)
    out: list[str] = []
    skip = 0
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<pre", "<code", "<script", "<bdi", "<style")):
                skip += 1
            elif low.startswith(("</pre", "</code", "</script", "</bdi", "</style")):
                skip = max(0, skip - 1)
            out.append(part)
            continue
        if skip or not part:
            out.append(part)
            continue
        pattern = LATIN_RE if lang == "fa" else ARABIC_RE
        direction = "ltr" if lang == "fa" else "rtl"

        def wrap(piece: str, pattern: re.Pattern[str] = pattern, direction: str = direction) -> str:
            def one(match: re.Match[str]) -> str:
                run = match.group(0)
                body = run.rstrip()
                tail = run[len(body):]
                # A closing bracket whose opener is outside the run stays
                # outside, so «(syntax)» keeps both brackets together.
                pairs = {")": "(", "]": "[", "}": "{"}
                while body and body[-1] in pairs and body.count(body[-1]) > body.count(pairs[body[-1]]):
                    tail = body[-1] + tail
                    body = body[:-1].rstrip()
                if not body:
                    return run
                return f'<bdi dir="{direction}">{body}</bdi>{tail}'

            return pattern.sub(one, piece)

        # Entities (&lt; &amp; ...) must not be split by the English pattern.
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



# Sections of the «مطالب مفید» page: the sidebar lists them (its own contents).
LINK_SECTIONS = [
    ("software", "نرم‌افزارهای لازم", "Get the software"),
    ("videos", "ویدیوهای جالب درباره پایتون", "Fun Python videos"),
    ("last-period", "برای زنگ چهارم", "For the last period"),
]


def materials_nav() -> list[str]:
    rows = "".join(
        f'<a href="#{anchor}" data-fa="{esc(fa)}" data-en="{esc(en)}">{esc(fa)}</a>'
        for anchor, fa, en in LINK_SECTIONS
    )
    return [
        '<details class="toc" open><summary class="nav-toggle" aria-label="فهرست">'
        '<span class="burger" aria-hidden="true"></span>'
        '<span class="label" data-fa="فهرست این بخش" data-en="In this section">فهرست این بخش</span>'
        '</summary><nav id="lesson-nav" class="side" aria-label="contents">',
        f'<p class="mod" data-fa="فراتر از کتاب" data-en="Beyond the book">فراتر از کتاب</p>',
        f"{rows}</nav></details>",
    ]

ASSET_V = "24"


def is_book_page(page_path: Path) -> bool:
    """Textbook pages (lessons, contents, materials) get the language switch."""
    return page_path.relative_to(SITE).parts[:1] == ("book",)


def site_header(root: str, active: str, lang: bool) -> str:
    """The one header every page uses. root: prefix to the site root; active: current section."""

    def tab(key: str, href: str, fa: str, en: str) -> str:
        current = ' aria-current="page"' if key == active else ""
        return f'<a href="{root}{href}"{current} data-fa="{fa}" data-en="{en}">{fa}</a>'

    tabs = (
        tab("lessons", "book/toc.html", "درس‌ها", "Lessons")
        + tab("playground", "playground/index.html", "زمین بازی", "Playground")
        + tab("materials", "book/links.html", "مطالب مفید", "Useful materials")
    )
    toggle = (
        '<button type="button" id="lang-toggle" class="lang-toggle" dir="ltr" data-lang="fa" aria-label="تغییر زبان">'
        '<span data-opt="fa">فا</span><span data-opt="en">EN</span></button>'
        if lang
        else ""
    )
    return (
        '<header class="top">'
        f'<a class="brand" href="{root}index.html"><span data-fa="طراح سایت" data-en="Site Design">طراح سایت</span>'
        '<small data-fa="پایه یازدهم" data-en="Grade 11">پایه یازدهم</small></a>'
        f'<nav class="sections" aria-label="بخش‌های سایت">{tabs}</nav>'
        '<div class="search-wrap" role="search"><input id="q" type="search" autocomplete="off" data-lpignore="true" data-1p-ignore data-bwignore="true" data-form-type="other" '
        'data-fa-placeholder="جستجو در درس‌ها" data-en-placeholder="Search lessons" '
        'placeholder="جستجو در درس‌ها" aria-label="جستجو در درس‌ها">'
        '<div id="search-results" class="search-results" hidden></div></div>'
        '<div class="top-actions">'
        f'<a class="btn primary sm download-link" href="{root}grade11-offline.zip?v=6" '
        'data-fa="دانلود کل سایت" data-en="Download the whole site">دانلود کل سایت</a>'
        f"{toggle}</div></header>"
    )


def site_footer(root: str) -> str:
    """The one footer every page uses."""
    return (
        '<footer class="site-foot">'
        '<p><strong data-fa="طراح سایت" data-en="Site Design">طراح سایت</strong> · '
        '<span data-fa="پایه یازدهم" data-en="Grade 11">پایه یازدهم</span></p>'
        '<nav aria-label="پیوندهای سایت">'
        f'<a href="{root}index.html" data-fa="صفحه اصلی" data-en="Home">صفحه اصلی</a>'
        f'<a href="{root}book/toc.html" data-fa="درس‌ها" data-en="Lessons">درس‌ها</a>'
        f'<a href="{root}playground/index.html" data-fa="زمین بازی" data-en="Playground">زمین بازی</a>'
        f'<a href="{root}book/links.html" data-fa="مطالب مفید" data-en="Useful materials">مطالب مفید</a>'
        "</nav>"
        f'<a class="btn ghost sm download-link" href="{root}grade11-offline.zip?v=6" '
        'data-fa="دانلود برای آفلاین" data-en="Download for offline use">دانلود برای آفلاین</a>'
        "</footer>"
    )


def lesson_nav(page_path: Path, pages: list[dict]) -> list[str]:
    """The sidebar of a textbook page: every lesson, grouped by module and unit."""
    nav = [
        '<details class="toc" open>',
        '<summary class="nav-toggle" aria-label="فهرست درس‌ها">'
        '<span class="burger" aria-hidden="true"></span>'
        '<span class="label" data-fa="فهرست درس‌ها" data-en="Lessons">فهرست درس‌ها</span>'
        "</summary>",
        '<nav id="lesson-nav" class="side" aria-label="lessons">',
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
    return nav


def chrome(page_path: Path, title_fa: str, title_en: str, pages: list[dict], body: str,
           show_nav: bool = True, side_items: bool = False) -> str:
    def asset(name: str) -> str:
        return rel(page_path, SITE / "assets" / name) + f"?v={ASSET_V}"

    home = rel(page_path, SITE / "index.html")
    root = "" if home == "index.html" else home[: -len("index.html")]
    if page_path == SITE / "book" / "links.html":
        active = "materials"
    elif is_book_page(page_path):
        active = "lessons"
    else:
        active = ""
    if side_items:
        nav = materials_nav()
    elif show_nav:
        nav = lesson_nav(page_path, pages)
    else:
        nav = []
    layout_class = "layout has-side" if nav else "layout"
    lang = is_book_page(page_path)
    favicon = rel(page_path, SITE / "assets" / "favicon.svg")
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title data-fa="{esc(title_fa)}" data-en="{esc(title_en)}">{esc(title_fa)}</title>
  <link rel="icon" href="{favicon}">
  <script>if (location.protocol === "file:") document.documentElement.classList.add("is-offline");</script>
  <link rel="stylesheet" href="{asset('shared.css')}">
  <link rel="stylesheet" href="{asset('style.css')}">
</head>
<body data-root="{root}">
  {site_header(root, active, lang)}
  <div class="{layout_class}">
    {''.join(nav)}
    <div class="main">
      {body}
    </div>
  </div>
  {site_footer(root)}
  <script src="{asset('search-index.js')}"></script>
  <script src="{asset('search.js')}"></script>
  <script src="{asset('guard.js')}"></script>
  <script src="{asset('app.js')}"></script>
</body>
</html>
"""


def home_body(pages: list[dict], here: Path) -> str:
    """Landing page: the book, then how to use it offline. No module list here."""
    package = rel(here, SITE / "grade11-offline.zip") + "?v=5"
    hub = rel(here, SITE / "book" / "index.html")
    return f"""
      <header class="page-head">
        <p class="kicker" data-fa="کتاب درسی هنرستان · پایه یازدهم" data-en="Vocational textbook · Grade 11">کتاب درسی هنرستان · پایه یازدهم</p>
        <h1 data-fa="درس‌های پایه یازدهم" data-en="Grade 11 lessons">درس‌های پایه یازدهم</h1>
        <p class="lede" data-fa="درس‌ها، تمرین‌ها و مطالب مفید هنرستان در یک جا هستند. آنلاین بخوانید، یا فایل آفلاین را برای کلاس بدون اینترنت دانلود کنید." data-en="Lessons, practice, and useful materials in one place. Read online, or download the offline copy for a class with no internet.">درس‌ها، تمرین‌ها و مطالب مفید هنرستان در یک جا هستند. آنلاین بخوانید، یا فایل آفلاین را برای کلاس بدون اینترنت دانلود کنید.</p>
      </header>

      <h2 class="section-h" data-fa="کتاب" data-en="Book">کتاب</h2>
      <a class="card is-link course" href="{hub}">
        <span class="chip" data-fa="کتاب درسی" data-en="Textbook">کتاب درسی</span>
        <h3 class="card-title" data-fa="طراح سایت" data-en="Site Design">طراح سایت</h3>
        <p class="card-text" data-fa="پایه یازدهم، رشته شبکه و نرم‌افزار رایانه. پنج پودمان، هر کدام با درس، تمرین و مطالب مفید." data-en="Grade 11, networking and software. Five modules, each with lessons, practice, and useful materials.">پایه یازدهم، رشته شبکه و نرم‌افزار رایانه. پنج پودمان، هر کدام با درس، تمرین و مطالب مفید.</p>
        <span class="card-cta" data-fa="ورود به کتاب" data-en="Enter the book">ورود به کتاب</span>
      </a>

      <h2 class="section-h" data-fa="استفاده بدون اینترنت" data-en="Offline use">استفاده بدون اینترنت</h2>
      <div class="step-grid">
        <div class="card step">
          <span class="num">۱</span>
          <h3 class="card-title" data-fa="کپی یا دانلود" data-en="Copy or download">کپی یا دانلود</h3>
          <p class="card-text" data-fa="پوشه را کپی کنید، یا از دکمه بالای صفحه فایل فشرده را بگیرید و باز کنید." data-en="Copy the folder, or download the zip with the button above and unpack it.">پوشه را کپی کنید، یا از دکمه بالای صفحه فایل فشرده را بگیرید و باز کنید.</p>
        </div>
        <div class="card step">
          <span class="num">۲</span>
          <h3 class="card-title" data-fa="باز کردن درس‌ها" data-en="Open the lessons">باز کردن درس‌ها</h3>
          <p class="card-text" data-fa="فایل index.html را با دوبار کلیک باز کنید." data-en="Double-click index.html.">فایل index.html را با دوبار کلیک باز کنید.</p>
        </div>
        <div class="card step">
          <span class="num">۳</span>
          <h3 class="card-title" data-fa="باز کردن زمین بازی" data-en="Open the playground">باز کردن زمین بازی</h3>
          <p class="card-text" data-fa="فایل شروع.bat را با دوبار کلیک اجرا کنید. به اینترنت نیاز ندارد." data-en="Double-click شروع.bat. It needs no internet.">فایل شروع.bat را با دوبار کلیک اجرا کنید. به اینترنت نیاز ندارد.</p>
        </div>
      </div>

      <div class="card banner">
        <div>
          <p class="card-title" data-fa="دانلود کل سایت برای استفاده آفلاین" data-en="Download the whole site for offline use">دانلود کل سایت برای استفاده آفلاین</p>
          <p class="card-text" data-fa="فایل فشرده را یک بار دانلود کنید؛ درس‌ها و زمین بازی هر دو داخل آن است." data-en="Download the zip once; the lessons and the playground are both inside.">فایل فشرده را یک بار دانلود کنید؛ درس‌ها و زمین بازی هر دو داخل آن است.</p>
        </div>
        <a class="btn primary download-link" href="{package}" data-fa="دانلود" data-en="Download">دانلود</a>
      </div>
    """


def hub_body(here: Path) -> str:
    """Book entry: lessons, playground, and useful materials."""
    toc = rel(here, SITE / "book" / "toc.html")
    links = rel(here, SITE / "book" / "links.html")
    playground = rel(here, SITE / "playground" / "index.html")
    zip_href = playground_zip_href(rel(here, SITE / "images"))
    return f"""
      <header class="page-head">
        <p class="kicker" data-fa="کتاب درسی · پایه یازدهم" data-en="Textbook · Grade 11">کتاب درسی · پایه یازدهم</p>
        <h1 data-fa="طراح سایت" data-en="Site Design">طراح سایت</h1>
        <p class="lede" data-fa="از اینجا به درس‌ها، زمین بازی پایتون یا مطالب مفید بروید." data-en="From here, go to the lessons, the Python playground, or the useful materials.">از اینجا به درس‌ها، زمین بازی پایتون یا مطالب مفید بروید.</p>
      </header>

      <div class="option-grid">
        <a class="card is-link option" href="{toc}">
          <span class="num">۱</span>
          <h2 class="card-title" data-fa="درس‌ها" data-en="Lessons">درس‌ها</h2>
          <p class="card-text" data-fa="فهرست کتاب: همه درس‌های پنج پودمان." data-en="Contents: every lesson in the five modules.">فهرست کتاب: همه درس‌های پنج پودمان.</p>
          <span class="card-cta" data-fa="باز کردن فهرست" data-en="Open the contents">باز کردن فهرست</span>
        </a>
        <article class="card option">
          <span class="num">۲</span>
          <h2 class="card-title" data-fa="زمین بازی پایتون" data-en="Python playground">زمین بازی پایتون</h2>
          <p class="card-text" data-fa="تمرین با تست، راهنما و مقایسه خروجی." data-en="Practice with tests, hints, and output comparison.">تمرین با تست، راهنما و مقایسه خروجی.</p>
          <div class="btn-row">
            <a class="btn primary sm" href="{playground}" data-fa="باز کردن آنلاین" data-en="Open online">باز کردن آنلاین</a>
            <a class="btn secondary sm download-link" href="{zip_href}" data-fa="دانلود کل سایت" data-en="Download the whole site">دانلود کل سایت</a>
          </div>
          <p class="card-text note" data-fa="زمین بازی در همین فایل فشرده‌ی کل سایت است. برای کلاس بدون اینترنت، یک بار دانلود کنید و شروع.bat را اجرا کنید." data-en="The playground is in the same whole-site zip. For a class with no internet, download the zip once and run شروع.bat.">زمین بازی در همین فایل فشرده‌ی کل سایت است. برای کلاس بدون اینترنت، یک بار دانلود کنید و شروع.bat را اجرا کنید.</p>
        </article>
        <a class="card is-link option" href="{links}">
          <span class="num">۳</span>
          <h2 class="card-title" data-fa="مطالب مفید" data-en="Useful materials">مطالب مفید</h2>
          <p class="card-text" data-fa="نرم‌افزار لازم، ویدیوهای جالب و بازی «تکامل اعتماد»." data-en="Software you need, fun videos, and the Evolution of Trust game.">نرم‌افزار لازم، ویدیوهای جالب و بازی «تکامل اعتماد».</p>
          <span class="card-cta" data-fa="باز کردن" data-en="Open">باز کردن</span>
        </a>
      </div>
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


# A living page of tools and videos, not book text. Thumbnails are
# downloaded once into extra-images/ so the page works offline.
LINK_SOFTWARE = [
    ("Py", "دانلود پایتون", "Download Python",
     "نصب‌کننده رسمی پایتون برای ویندوز و مک.",
     "Official Python installer for Windows and Mac.",
     "https://www.python.org/downloads/"),
    ("VS", "دانلود وی‌اس‌کد", "Download VS Code",
     "ویرایشگر کدی که در کتاب با آن کار می‌کنیم.",
     "The code editor used in the book.",
     "https://code.visualstudio.com/"),
    ("Pd", "پایدروید ۳ برای اندروید", "Pydroid 3 for Android",
     "پایتون روی گوشی؛ برای تمرین بدون رایانه.",
     "Python on your phone; practice without a computer.",
     "https://play.google.com/store/apps/details?id=ru.iiec.pydroid3"),
]
LINK_VIDEOS = [
    ("yt_qQXXI5QFUfw.jpg", "https://www.youtube.com/watch?v=qQXXI5QFUfw",
     "پرکاربردترین زبان‌های برنامه‌نویسی از ۱۹۶۵ تا ۲۰۲۲",
     "Most-used programming languages, 1965 to 2022"),
    ("yt_3PcIJKd1PKU.jpg", "https://www.youtube.com/watch?v=3PcIJKd1PKU",
     "مقایسه تعداد خطوط، مدت ساخت و مدت اجرای یک کار یکسان با ۳ زبان مختلف",
     "Same task in 3 languages: lines, build time, and run time compared"),
    ("yt__-KjEgCLQFw.jpg", "https://www.youtube.com/watch?v=_-KjEgCLQFw",
     "بازی مار در ۶۰ خط و ۵ دقیقه با پایتون",
     "Snake game in 60 lines and 5 minutes with Python"),
    ("yt_7kGNs5R-AM8.jpg", "https://www.youtube.com/watch?v=7kGNs5R-AM8",
     "بازی تتریس (خانه‌سازی) در ۱۸۰ خط و ۹ دقیقه با پایتون",
     "Tetris in 180 lines and 9 minutes with Python"),
    ("", "https://www.youtube.com/watch?v=DEFmxPMdBqmU",
     "این پیوند در یوتیوب باز نشد؛ شاید حذف یا خصوصی شده باشد",
     "This link did not open on YouTube; it may be deleted or private"),
]


def links_html(prefix: str) -> str:
    cards = []
    for badge, fa, en, dfa, den, href in LINK_SOFTWARE:
        cards.append(
            f'<div class="link-card"><span class="badge">{esc(badge)}</span>'
            f'<div><h3 data-fa="{esc(fa)}" data-en="{esc(en)}">{esc(fa)}</h3>'
            f'<p data-fa="{esc(dfa)}" data-en="{esc(den)}">{esc(dfa)}</p>'
            f'<a href="{esc(href)}" data-fa="دانلود" data-en="Download">دانلود</a>'
            "</div></div>"
        )
    videos = []
    for thumb, href, fa, en in LINK_VIDEOS:
        if thumb:
            shot = f'<img src="{prefix}/{thumb}" alt="" loading="lazy">'
        else:
            shot = '<span class="no-thumb" aria-hidden="true">▶</span>'
        videos.append(
            f'<div class="link-card video"><a class="shot-link" href="{esc(href)}">{shot}</a>'
            f'<div><p class="video-title" data-fa="{esc(fa)}" data-en="{esc(en)}">{esc(fa)}</p>'
            f'<a href="{esc(href)}" data-fa="تماشا در یوتیوب" data-en="Watch on YouTube">تماشا در یوتیوب</a>'
            "</div></div>"
        )
    return (
        '<h2 class="section-h" id="software" data-fa="نرم‌افزارهای لازم" data-en="Get the software">نرم‌افزارهای لازم</h2>'
        f'<div class="link-grid">{"".join(cards)}</div>'
        '<h2 class="section-h" id="videos" data-fa="ویدیوهای جالب درباره پایتون" data-en="Fun Python videos">ویدیوهای جالب درباره پایتون</h2>'
        f'<p class="link-note" data-fa="تماشای ویدیوها اینترنت می‌خواهد؛ خود صفحه بدون اینترنت هم باز می‌شود." data-en="Watching the videos needs internet; the page itself opens offline too.">تماشای ویدیوها اینترنت می‌خواهد؛ خود صفحه بدون اینترنت هم باز می‌شود.</p>'
        f'<div class="link-grid">{"".join(videos)}</div>'
        '<h2 class="section-h" id="last-period" data-fa="برای زنگ چهارم" data-en="For the last period">برای زنگ چهارم</h2>'
        '<div class="link-grid">'
        '<div class="link-card"><span class="badge">تمرین</span><div>'
        '<h3 data-fa="زمین بازی پایتون" data-en="Python playground">زمین بازی پایتون</h3>'
        '<p data-fa="تمرین پودمان ۱ با تست، راهنمایی و مقایسه خروجی. آنلاین باز کنید؛ در کلاس بدون اینترنت zip را بگیرید و شروع.bat را اجرا کنید." '
        'data-en="Module 1 practice with tests, hints, and diffs. Open it online; in the lab with no internet, unzip and run شروع.bat.">'
        'تمرین پودمان ۱ با تست، راهنمایی و مقایسه خروجی. آنلاین باز کنید؛ در کلاس بدون اینترنت zip را بگیرید و شروع.bat را اجرا کنید.</p>'
        f'<a href="{esc(playground_online_href(prefix))}" data-fa="باز کردن آنلاین" data-en="Open online">باز کردن آنلاین</a> '
        f'<a href="{esc(playground_zip_href(prefix))}" data-fa="دانلود نسخه آفلاین" data-en="Download the offline copy">دانلود نسخه آفلاین</a>'
        '</div></div>'
        '<div class="link-card"><span class="badge">بازی</span><div>'
        '<h3 data-fa="تکامل اعتماد" data-en="The Evolution of Trust">تکامل اعتماد</h3>'
        '<p data-fa="نظریه بازی. فایل فشرده را باز کنید و index.html را اجرا کنید. خود بازی اینترنت نمی‌خواهد." '
        'data-en="Game theory. Unzip it and open index.html. The game itself needs no internet.">'
        'نظریه بازی. فایل فشرده را باز کنید و index.html را اجرا کنید. خود بازی اینترنت نمی‌خواهد.</p>'
        f'<a href="{esc(trust_zip_href(prefix))}" data-fa="دانلود نسخه آفلاین" data-en="Download the offline copy">دانلود نسخه آفلاین</a>'
        '</div></div></div>'
        '<p class="link-note" data-fa="این فهرست در طول ترم بیشتر می‌شود." data-en="This list grows during the term.">این فهرست در طول ترم بیشتر می‌شود.</p>'
    )


def trust_zip_href(prefix: str) -> str:
    root = prefix[: -len("images")] if prefix.endswith("images") else ""
    return root + "evolution-of-trust-offline.zip?v=4"


def playground_online_href(prefix: str) -> str:
    root = prefix[: -len("images")] if prefix.endswith("images") else ""
    return root + "playground/"


def playground_zip_href(prefix: str) -> str:
    root = prefix[: -len("images")] if prefix.endswith("images") else ""
    return root + "grade11-offline.zip?v=6"


def links_text(lang: str) -> str:
    if lang == "fa":
        bits = [row[1] for row in LINK_SOFTWARE] + [row[2] for row in LINK_VIDEOS]
        bits.append("زمین بازی پایتون")
        bits.append("تکامل اعتماد")
    else:
        bits = [row[2] for row in LINK_SOFTWARE] + [row[3] for row in LINK_VIDEOS]
        bits.append("Python playground")
        bits.append("The Evolution of Trust")
    return " ".join(bits)


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
      <aside class="card extra">
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


EXTRA_IMAGES = ROOT / "extra-images"


def link_images() -> int:
    target = SITE / "images"
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for source in (BOOK / "images", EXTRA_IMAGES):
        if not source.is_dir():
            continue
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


# The tutorials (آموزش) are not shipped in the offline copy: like the website, it gets them after a
# sign-in (the accounts service sends them) and keeps them on the device.
OFFLINE_GUIDE_FIELDS = ("guide", "guideTitle", "solutions", "mistakes")
OFFLINE_ROOT = "grade11-site"


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_zip() -> None:
    """The offline copy: a zip of the whole site, plus offline-manifest.json.

    The manifest lists every file with its hash. The copy's launcher compares it with the one on the
    website to find out what changed, and downloads only those files. Files that are the same as on
    the website are fetched from their normal address; the few that differ in the offline copy (the
    playground page and the questions file) are published under offline-files/.
    """
    target = SITE / "grade11-offline.zip"
    temporary = ROOT / ".grade11-offline.zip"
    if temporary.exists():
        temporary.unlink()
    published = SITE / "offline-files"
    if published.exists():
        shutil.rmtree(published)
    files: dict[str, dict] = {}

    def publish_variant(archive: zipfile.ZipFile, rel: str, data: bytes) -> None:
        out = published / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        archive.writestr(f"{OFFLINE_ROOT}/{rel}", data)
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "url": f"offline-files/{rel}"}

    with zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as archive:
        for path in sorted(SITE.rglob("*")):
            if not path.is_file() or path.suffix == ".zip":
                continue
            rel = path.relative_to(SITE)
            if rel.parts[0] in ("admin", "offline-files") or rel.as_posix() == "offline-manifest.json":
                continue  # the panel exists only online; the other two are made here
            if rel.as_posix() == "playground/index.html":
                # The offline copy checks answers on the device; it signs in to send them (sync).
                page = path.read_text(encoding="utf-8").replace(
                    '<meta name="pg-mode" content="online">',
                    '<meta name="pg-mode" content="offline">',
                )
                publish_variant(archive, rel.as_posix(), page.encode("utf-8"))
                continue
            archive.write(path, f"{OFFLINE_ROOT}/{rel.as_posix()}")
            files[rel.as_posix()] = {"sha256": file_digest(path), "size": path.stat().st_size, "url": rel.as_posix()}
        # The questions without their tutorials: the same view of the questions as the website's.
        problems = json.loads((ROOT / "playground" / "app" / "data" / "problems.json").read_text(encoding="utf-8"))
        public = [{k: v for k, v in q.items() if k not in OFFLINE_GUIDE_FIELDS} for q in problems]
        publish_variant(
            archive, "playground/data/problems.json",
            json.dumps(public, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        )
        ordered = dict(sorted(files.items()))
        version = hashlib.sha256(
            "\n".join(f"{name}\t{info['sha256']}" for name, info in ordered.items()).encode("utf-8")
        ).hexdigest()[:12]
        manifest = json.dumps(
            {"format": 1, "version": version,
             "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "files": ordered},
            ensure_ascii=False, indent=1,
        ).encode("utf-8")
        archive.writestr(f"{OFFLINE_ROOT}/offline-manifest.json", manifest)
    (SITE / "offline-manifest.json").write_bytes(manifest)
    shutil.move(temporary, target)


def publish_playground() -> None:
    src = ROOT / "playground" / "app"
    dst = SITE / "playground"
    if not src.is_dir():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    # The online site does not publish the questions file: it holds the solutions, and the
    # server releases each solution only to a student who has passed the question.
    (dst / "data" / "problems.json").unlink(missing_ok=True)
    split_engine_parts(dst / "vendor" / "pyodide")
    index = dst / "index.html"
    page = index.read_text(encoding="utf-8")
    if "<!--SITE-HEADER-->" not in page or "<!--SITE-FOOTER-->" not in page:
        raise SystemExit("playground/app/index.html needs the SITE-HEADER and SITE-FOOTER placeholders")
    page = page.replace("<!--SITE-HEADER-->", site_header("../", "playground", lang=False))
    page = page.replace("<!--SITE-FOOTER-->", site_footer("../"))
    index.write_text(page, encoding="utf-8")


ENGINE_PART_FILES = {
    "pyodide.asm.wasm": "application/wasm",
    "pyodide.asm.js": "text/javascript",
    "python_stdlib.zip": "application/zip",
    "pyodide-lock.json": "application/json",
}
ENGINE_PART_SIZE = 256 * 1024


def split_engine_parts(engine_dir: Path) -> None:
    """Gzip + split big engine files so the online playground can resume
    downloads over flaky links (see playground/app/js/enginefetch.js)."""
    if not engine_dir.is_dir():
        return
    out = engine_dir / "chunks"
    out.mkdir(exist_ok=True)
    files = []
    for name, mime in ENGINE_PART_FILES.items():
        raw = (engine_dir / name).read_bytes()
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        tag = hashlib.sha256(raw).hexdigest()[:12]
        parts = []
        for i in range(0, len(packed), ENGINE_PART_SIZE):
            blob = packed[i : i + ENGINE_PART_SIZE]
            part = f"{name}.{tag}.{i // ENGINE_PART_SIZE:03d}.bin"
            (out / part).write_bytes(blob)
            parts.append({"name": part, "size": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
        files.append({"name": name, "type": mime, "size": len(raw), "parts": parts})
    (out / "manifest.json").write_text(json.dumps({"files": files}, indent=1), encoding="utf-8")


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
    shutil.copy2(WEB / "shared.css", SITE / "assets" / "shared.css")
    shutil.copy2(WEB / "search.js", SITE / "assets" / "search.js")
    shutil.copy2(WEB / "guard.js", SITE / "assets" / "guard.js")
    shutil.copy2(WEB / "app.js", SITE / "assets" / "app.js")
    shutil.copytree(WEB / "admin", SITE / "admin")
    fonts_src = WEB / "fonts"
    if fonts_src.is_dir():
        shutil.copytree(fonts_src, SITE / "assets" / "fonts")
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
        elif item.get("custom") == "links":
            fa_html = en_html = links_html(prefix)
        else:
            fa_html = isolate_bidi(render_markdown(section_markdown(item), prefix, "fa"), "fa")
            en_html = isolate_bidi(render_markdown(english_markdown(item), prefix, "en"), "en")
        title = (
            '<header class="page-head">'
            f'<p class="kicker" data-fa="{esc(item["module_fa"])}" data-en="{esc(item["module_en"])}">{esc(item["module_fa"])}</p>'
            f'<h1 data-fa="{esc(item["fa"])}" data-en="{esc(item["en"])}">{esc(item["fa"])}</h1>'
            "</header>"
        )
        # The materials page is a set of cards already; it does not sit in one more card.
        article_class = "lesson no-copy" if item.get("custom") == "links" else "card lesson no-copy"
        body = (
            title
            + f'<article class="{article_class}" lang="fa" dir="rtl" data-lang-block="fa">{fa_html}</article>'
            + f'<article class="{article_class}" lang="en" dir="ltr" data-lang-block="en" hidden>{en_html}</article>'
            + extra_block(item)
            + pager(item["out"], pages, index)
        )
        item["out"].parent.mkdir(parents=True, exist_ok=True)
        item["out"].write_text(
            chrome(item["out"], item["fa"], item["en"], pages, body, side_items=item.get("custom") == "links"),
            encoding="utf-8",
        )
        search.append(
            {
                "href": rel(SITE / "index.html", item["out"]),
                "titleFa": item["fa"],
                "titleEn": item["en"],
                "textFa": links_text("fa") if item.get("custom") == "links" else (" ".join(row[1] for row in CONTENTS) if item["id"] == "toc" else plain_text(fa_html)),
                "textEn": links_text("en") if item.get("custom") == "links" else (" ".join(row[2] for row in CONTENTS) if item["id"] == "toc" else plain_text(en_html)),
            }
        )
        guard(item["out"])

    index_path = SITE / "index.html"
    index_path.write_text(
        chrome(index_path, "طراح سایت", "Site Design", pages, home_body(pages, index_path), show_nav=False),
        encoding="utf-8",
    )
    guard(index_path)

    hub_path = SITE / "book" / "index.html"
    hub_path.parent.mkdir(parents=True, exist_ok=True)
    hub_path.write_text(
        chrome(hub_path, "طراح سایت", "Site Design", pages, hub_body(hub_path), show_nav=False),
        encoding="utf-8",
    )
    guard(hub_path)
    search.append(
        {
            "href": rel(index_path, hub_path),
            "titleFa": "طراح سایت",
            "titleEn": "Site Design",
            "textFa": "درس‌ها فهرست کتاب زمین بازی پایتون مطالب مفید",
            "textEn": "Lessons contents Python playground useful materials",
        }
    )

    payload = json.dumps(search, ensure_ascii=False).replace("<", "\\u003c")
    (SITE / "assets" / "search-index.js").write_text(
        "window.BOOK_SEARCH = " + payload + ";\n",
        encoding="utf-8",
    )
    (SITE / "README.md").write_text(
        """# طراح سایت — نسخه آفلاین کلاس

کل همین پوشه را به رایانه کلاس کپی کنید و `index.html` را با دوبار کلیک باز کنید. اینترنت لازم نیست.

فایل `grade11-offline.zip` برای دانلود از سایت است. داخل خودِ فایل فشرده نیست، تا دانش‌آموز بعد از باز کردن، یک پوشه ساده داشته باشد.

تمرین‌ها و بازی‌های جدا (`/playground/` آنلاین، `teacher-playground-offline.zip`، `evolution-of-trust-offline.zip`) هم روی سایت عمومی در صفحه «پیوندهای مفید» هستند؛ داخل این zip کتاب نیستند.

# Site Design — offline classroom copy

Copy this whole folder onto a lab PC and double-click `index.html`. No internet is required.

`grade11-offline.zip` is the download offered on the public site. It is not packed inside itself.

The online playground (`/playground/`) and separate lab zips (`teacher-playground-offline.zip`, `evolution-of-trust-offline.zip`) are on the public Useful-links page; they are not inside this textbook zip.
""",
        encoding="utf-8",
    )
    trust_zip = ROOT / "extras" / "evolution-of-trust-offline.zip"
    if trust_zip.is_file():
        shutil.copy2(trust_zip, SITE / "evolution-of-trust-offline.zip")
    shutil.copy2(ROOT / "offline" / "شروع.bat", SITE / "شروع.bat")
    (SITE / "README.md").write_text('# طراح سایت — نسخه\u200cی کامل آفلاین\n\nاین فایل فشرده کل سایت است: درس\u200cها و زمین بازی. یک بار دانلود کنید؛ دیگر لازم نیست چیزی را دوباره بگیرید.\n\n- درس\u200cها: فایل `index.html` را با دوبار کلیک باز کنید.\n- زمین بازی: فایل `شروع.bat` را با دوبار کلیک اجرا کنید (Python 3 با tkinter لازم است). پیشرفت شما در همین نشانی محلی ذخیره می\u200cماند؛ همیشه با همین فایل باز کنید.\n\n# Site Design — full offline copy\n\nOne zip holds the whole site: lessons and playground. Download once.\n\n- Lessons: double-click `index.html`.\n- Playground: double-click `شروع.bat` (needs Python 3 with tkinter). Progress is kept at the same local address, so always start it the same way.\n', encoding="utf-8")
    publish_playground()
    write_zip()
    print(f"pages {len(pages) + 1} images {images}")


if __name__ == "__main__":
    main()
