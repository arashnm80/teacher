#!/usr/bin/env python3
"""Build the offline bilingual site from converted-markdown-book/.

See REQUIREMENTS.md. The site folder must open by double-clicking index.html.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "converted-markdown-book"
SITE = ROOT / "site"
WEB = ROOT / "web"

# Lesson text stays Persian. These English labels are only for the chrome.
MODULES = [
    {
        "fa": "شروع کتاب",
        "en": "Opening",
        "blurb_fa": "جلد، مجوز آزاد کتاب، و فهرست.",
        "blurb_en": "Cover, the book's free license, and the contents.",
        "lessons": [
            ("00-front-matter.md", "شناسنامه و مقدمه", "Cover and license"),
            ("00-toc.md", "فهرست", "Contents"),
        ],
    },
    {
        "fa": "پودمان ۱: برنامه‌نویسی پایتون",
        "en": "Module 1: Python programming",
        "blurb_fa": "مدل‌سازی داده، توابع و ماژول‌ها.",
        "blurb_en": "Data modeling, functions, and modules.",
        "lessons": [
            ("01-poodman-1-python/00-intro.md", "معرفی پودمان", "Module introduction"),
            ("01-poodman-1-python/01-data-modeling.md", "مدل‌سازی داده", "Data modeling"),
            ("01-poodman-1-python/02-functions-and-modules.md", "توابع و ماژول‌ها", "Functions and modules"),
        ],
    },
    {
        "fa": "پودمان ۲: صفحات وب ایستا",
        "en": "Module 2: Static web pages",
        "blurb_fa": "ساختار صفحه با HTML و ظاهر با CSS.",
        "blurb_en": "Page structure with HTML and appearance with CSS.",
        "lessons": [
            ("02-poodman-2-static-web/00-intro.md", "معرفی پودمان", "Module introduction"),
            ("02-poodman-2-static-web/01-html.md", "ساختار صفحات با HTML", "Page structure with HTML"),
            ("02-poodman-2-static-web/02-css.md", "ظاهر صفحات با CSS", "Page appearance with CSS"),
        ],
    },
    {
        "fa": "پودمان ۳: صفحات وب تعاملی",
        "en": "Module 3: Interactive web pages",
        "blurb_fa": "بوت‌استرپ و جاوااسکریپت.",
        "blurb_en": "Bootstrap and JavaScript.",
        "lessons": [
            ("03-poodman-3-interactive-web/00-intro.md", "معرفی پودمان", "Module introduction"),
            ("03-poodman-3-interactive-web/01-bootstrap.md", "صفحات تعاملی با بوت‌استرپ", "Interactive pages with Bootstrap"),
            ("03-poodman-3-interactive-web/02-javascript.md", "صفحات تعاملی با جاوااسکریپت", "Interactive pages with JavaScript"),
        ],
    },
    {
        "fa": "پودمان ۴: توسعه وب پایتون",
        "en": "Module 4: Python for the web",
        "blurb_fa": "تولید و توسعه برنامه شی‌ءگرا.",
        "blurb_en": "Building and extending object-oriented programs.",
        "lessons": [
            ("04-poodman-4-python-oop/00-intro.md", "معرفی پودمان", "Module introduction"),
            ("04-poodman-4-python-oop/01-object-oriented.md", "تولید برنامه شیءگرا", "Object-oriented programs"),
            ("04-poodman-4-python-oop/02-object-oriented-development.md", "توسعه برنامه شیءگرا", "Extending object-oriented programs"),
        ],
    },
    {
        "fa": "پودمان ۵: برنامه‌نویسی جنگو",
        "en": "Module 5: Django",
        "blurb_fa": "ایجاد و توسعه وب‌اپلیکیشن.",
        "blurb_en": "Creating and developing a web application.",
        "lessons": [
            ("05-poodman-5-django/00-intro.md", "معرفی پودمان", "Module introduction"),
            ("05-poodman-5-django/01-create-web-app.md", "ایجاد وب‌اپلیکیشن", "Creating a web app"),
            ("05-poodman-5-django/02-develop-web-app.md", "توسعه وب‌اپلیکیشن", "Developing a web app"),
        ],
    },
    {
        "fa": "پایان کتاب",
        "en": "Back of the book",
        "blurb_fa": "منابعی که کتاب معرفی کرده است.",
        "blurb_en": "Sources listed in the book.",
        "lessons": [
            ("06-references.md", "منابع", "References"),
        ],
    },
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rel(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent).replace(os.sep, "/")


def flatten() -> list[dict]:
    pages = []
    for module in MODULES:
        if module["fa"] in ("شروع کتاب", "پایان کتاب"):
            show_on_home = False
        else:
            show_on_home = True
        for src, title_fa, title_en in module["lessons"]:
            pages.append(
                {
                    "src": BOOK / src,
                    "out": SITE / "book" / Path(src).with_suffix(".html"),
                    "title_fa": title_fa,
                    "title_en": title_en,
                    "module_fa": module["fa"],
                    "module_en": module["en"],
                    "blurb_fa": module["blurb_fa"],
                    "blurb_en": module["blurb_en"],
                    "show_on_home": show_on_home,
                    "home_anchor": module["lessons"][0][0] == src and show_on_home,
                }
            )
    return pages


def render_markdown(text: str, image_prefix: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "toc"])
    body = converter.convert(text)

    def image(match: re.Match[str]) -> str:
        name = match.group(1).split("/")[-1]
        return f'src="{image_prefix}/{name}"'

    return re.sub(r'src="(?:\.\./)*images/([^"]+)"', image, body)


def chrome(page_path: Path, title_fa: str, title_en: str, pages: list[dict], body: str) -> str:
    assets = rel(page_path, SITE / "assets" / "style.css")
    script = rel(page_path, SITE / "assets" / "app.js")
    search = rel(page_path, SITE / "assets" / "search-index.js")
    home = rel(page_path, SITE / "index.html")
    favicon = rel(page_path, SITE / "assets" / "favicon.svg")
    to_home = rel(page_path, SITE / "index.html")
    root = "" if to_home == "index.html" else to_home[: -len("index.html")]

    nav = ['<nav class="side" aria-label="lessons">']
    last_module = None
    for item in pages:
        if item["module_fa"] != last_module:
            nav.append(
                f'<p class="mod" data-fa="{esc(item["module_fa"])}" data-en="{esc(item["module_en"])}">'
                f"{esc(item['module_fa'])}</p>"
            )
            last_module = item["module_fa"]
        href = rel(page_path, item["out"])
        current = " current" if item["out"] == page_path else ""
        nav.append(
            f'<a class="{current.strip()}" href="{href}" '
            f'data-fa="{esc(item["title_fa"])}" data-en="{esc(item["title_en"])}">'
            f"{esc(item['title_fa'])}</a>"
        )
    nav.append("</nav>")

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title_fa)}</title>
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
    <div class="lang" role="group" aria-label="language">
      <button type="button" data-set-lang="fa" aria-pressed="true">فا</button>
      <button type="button" data-set-lang="en" aria-pressed="false">EN</button>
    </div>
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
    cards = []
    seen = set()
    number = 0
    for item in pages:
        if not item["home_anchor"] or item["module_fa"] in seen:
            continue
        seen.add(item["module_fa"])
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
      <p class="lede">پایه یازدهم، رشته شبکه و نرم‌افزار رایانه. این پوشه را در رایانه کلاس کپی کنید و همین صفحه را باز کنید. اینترنت لازم نیست.</p>
      <div class="steps">
        <div><strong>۱. کپی</strong>کل پوشه سایت را به رایانه ببرید.</div>
        <div><strong>۲. باز کردن</strong>فایل index.html را با دوبار کلیک باز کنید.</div>
        <div><strong>۳. زبان</strong>از بالای صفحه فارسی یا انگلیسی را انتخاب کنید. متن درس همان کتاب فارسی است.</div>
      </div>
    """
    en = """
      <p class="kicker">Vocational textbook</p>
      <h1>Site Design</h1>
      <p class="lede">Grade 11, computer networking and software. Copy this folder onto a lab computer and open this page. No internet is required.</p>
      <div class="steps">
        <div><strong>1. Copy</strong>Take the whole site folder to the computer.</div>
        <div><strong>2. Open</strong>Double-click index.html.</div>
        <div><strong>3. Language</strong>Choose Persian or English at the top. Lesson text stays the official Persian book.</div>
      </div>
    """
    return f"""
      <section class="hero">
        <div data-lang-block="fa">{fa}</div>
        <div data-lang-block="en" hidden>{en}</div>
        <div class="grid">{''.join(cards)}</div>
      </section>
    """


def pager(page_path: Path, pages: list[dict], index: int) -> str:
    parts = ['<nav class="pager">']
    if index > 0:
        prev = pages[index - 1]
        parts.append(
            f'<a rel="prev" href="{rel(page_path, prev["out"])}" '
            f'data-fa="{esc(prev["title_fa"])}" data-en="{esc(prev["title_en"])}">'
            f'{esc(prev["title_fa"])}</a>'
        )
    else:
        parts.append("<span></span>")
    if index + 1 < len(pages):
        nxt = pages[index + 1]
        parts.append(
            f'<a rel="next" href="{rel(page_path, nxt["out"])}" '
            f'data-fa="{esc(nxt["title_fa"])}" data-en="{esc(nxt["title_en"])}">'
            f'{esc(nxt["title_fa"])}</a>'
        )
    parts.append("</nav>")
    return "".join(parts)


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


def main() -> None:
    pages = flatten()
    for item in pages:
        if not item["src"].is_file():
            raise SystemExit(f"missing lesson {item['src']}")

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    shutil.copy2(WEB / "style.css", SITE / "assets" / "style.css")
    shutil.copy2(WEB / "app.js", SITE / "assets" / "app.js")
    (SITE / "assets" / "favicon.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#1b3358"/>
  <rect x="6" y="8" width="20" height="14" rx="2" fill="#f6f1e7"/>
  <path d="M10 26h12" stroke="#f6f1e7" stroke-width="2"/>
</svg>
""",
        encoding="utf-8",
    )
    images = link_images()

    search = []
    for index, item in enumerate(pages):
        depth = len(item["out"].relative_to(SITE).parts) - 1
        prefix = "../" * depth + "images"
        body_html = render_markdown(item["src"].read_text(encoding="utf-8"), prefix)
        article = (
            f'<article class="lesson" lang="fa" dir="rtl">{body_html}</article>'
            + pager(item["out"], pages, index)
        )
        item["out"].parent.mkdir(parents=True, exist_ok=True)
        item["out"].write_text(
            chrome(item["out"], item["title_fa"], item["title_en"], pages, article),
            encoding="utf-8",
        )
        search.append(
            {
                "href": rel(SITE / "index.html", item["out"]),
                "titleFa": item["title_fa"],
                "titleEn": item["title_en"],
                "text": plain_text(body_html),
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

# Site Design — offline classroom copy

Copy this whole folder onto a lab PC and double-click `index.html`. No internet is required.

Lesson text is the official Persian textbook. The menus switch between Persian and English.
""",
        encoding="utf-8",
    )
    print(f"pages {len(pages) + 1} images {images}")


if __name__ == "__main__":
    main()
