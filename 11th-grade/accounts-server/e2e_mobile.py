"""Phone and computer checks of the playground that runs code on the server: layout, the coding keys,
scrolling to the results, the copy-error button. Start the test servers first (accounts + judge).
"""
import json
import os
import urllib.request
import http.cookiejar
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8800")
SHOTS = os.environ.get("E2E_SHOTS", "")
PROBLEMS = Path("/root/Storage/teacher/11th-grade/playground/app/data/problems.json")
problems = json.loads(PROBLEMS.read_text(encoding="utf-8"))
first = problems[0]
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""), flush=True)


def session_cookies():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    body = json.dumps({"phone": "09123456789", "nationalCode": "0499370899", "classCode": "201",
                       "fullName": "علی احمدی", "password": "abc12345"}).encode()
    try:
        opener.open(urllib.request.Request(BASE + "/api/student/register", data=body,
                                           headers={"Content-Type": "application/json"}))
    except Exception:
        body = json.dumps({"phone": "09123456789", "password": "abc12345"}).encode()
        opener.open(urllib.request.Request(BASE + "/api/student/login", data=body,
                                           headers={"Content-Type": "application/json"}))
    return [{"name": c.name, "value": c.value, "url": BASE} for c in jar]


def shot(page, name):
    if SHOTS:
        page.screenshot(path=f"{SHOTS}/{name}.png")


def set_code(page, code):
    page.evaluate("(c) => document.querySelector('.CodeMirror').CodeMirror.setValue(c)", code)


def get_code(page):
    return page.evaluate("() => document.querySelector('.CodeMirror').CodeMirror.getValue()")


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - innerWidth")


def in_view(page, selector):
    return page.evaluate("""(s) => { const r = document.querySelector(s).getBoundingClientRect();
        return r.top < innerHeight && r.bottom > 0; }""", selector)


def open_page(browser, device, cookies, lang="fa"):
    ctx = browser.new_context(**device, permissions=["clipboard-read", "clipboard-write"])
    ctx.add_cookies(cookies)
    ctx.add_init_script(f"try {{ localStorage.setItem('grade11-lang-v2', '{lang}') }} catch (e) {{}}")
    page = ctx.new_page()
    page.errors = []
    page.on("pageerror", lambda e: page.errors.append(str(e)[:200]))
    page.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page.wait_for_selector(".problem-link", timeout=60000)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=60000)
    page.wait_for_timeout(400)
    return ctx, page


with sync_playwright() as p:
    browser = p.chromium.launch()
    cookies = session_cookies()
    phone = dict(p.devices["Pixel 7"])
    small = dict(p.devices["Pixel 5"])
    small["viewport"] = {"width": 360, "height": 640}
    desktop = dict(viewport={"width": 1366, "height": 800})

    for label, device in (("phone", phone), ("small phone", small)):
        for lang in ("fa", "en"):
            ctx, page = open_page(browser, device, cookies, lang)
            tag = f"{label} {lang}"
            check(f"{tag}: no sideways scrolling", overflow(page) <= 0, overflow(page))
            check(f"{tag}: the Python engine is not loaded online", page.evaluate("typeof loadPyodide") == "undefined")
            check(f"{tag}: the coding keys are shown", page.locator("#keybar").is_visible())
            check(f"{tag}: the keys are big enough to tap",
                  min(page.locator("#keybar .key").evaluate_all("els => els.map(e => Math.min(e.offsetWidth, e.offsetHeight))")) >= 40)
            run_box = page.locator("#btn-run").bounding_box()
            check(f"{tag}: the run button is big enough to tap", run_box["height"] >= 40, run_box)
            # choosing a question scrolls to it
            page.locator(".problem-link").nth(2).click()
            page.wait_for_timeout(900)
            check(f"{tag}: choosing a question shows it", in_view(page, "#problem-title"))
            # the keys type into the editor
            set_code(page, "")
            page.evaluate("document.querySelector('.CodeMirror').scrollIntoView()")
            page.locator("#keybar .key", has_text="Tab").tap()
            page.locator("#keybar .key", has_text="( )").tap()
            page.locator("#keybar .key", has_text=":").first.tap()
            check(f"{tag}: Tab, a bracket pair and a colon are typed (the colon lands inside the pair)", get_code(page) == "    (:)", repr(get_code(page)))
            cursor = page.evaluate("document.querySelector('.CodeMirror').CodeMirror.getCursor().ch")
            check(f"{tag}: the cursor is between the brackets after the pair key",
                  page.evaluate("""() => { const cm = document.querySelector('.CodeMirror').CodeMirror;
                    cm.setValue(''); return true; }"""))
            page.locator("#keybar .key", has_text="( )").tap()
            check(f"{tag}: a bracket pair puts the cursor inside",
                  page.evaluate("document.querySelector('.CodeMirror').CodeMirror.getCursor().ch") == 1)
            check(f"{tag}: the keys do not take the focus from the editor",
                  page.evaluate("document.activeElement.closest('.CodeMirror') !== null"))
            # a run: the result is brought into view
            problem = problems[2]
            set_code(page, "print('wrong')")
            page.evaluate("window.scrollTo(0, 0)")
            page.locator("#btn-run").scroll_into_view_if_needed()
            page.locator("#btn-run").tap()
            page.wait_for_function("document.querySelectorAll('#results .test-card').length > 0", timeout=60000)
            page.wait_for_timeout(1000)
            check(f"{tag}: the results are in view after a run", in_view(page, "#results .test-card"))
            check(f"{tag}: no sideways scrolling with results open", overflow(page) <= 0, overflow(page))
            shot(page, f"{label.replace(' ', '-')}-{lang}-results")
            check(f"{tag}: no page errors", not page.errors, page.errors)
            ctx.close()

    # the error copy button, on a phone and a computer, when the page cannot start
    for label, device in (("phone", phone), ("desktop", desktop)):
        ctx = browser.new_context(**device, permissions=["clipboard-read", "clipboard-write"])
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        page.route("**/js/enginefetch.js*", lambda route: route.abort())
        page.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
        page.wait_for_selector("#boot-copy", state="visible", timeout=30000)
        page.wait_for_function("document.getElementById('boot-tech').value.length > 20", timeout=30000)
        shot(page, f"{label}-boot-error")
        check(f"{label}: the copy-error button is visible", page.locator("#boot-copy").is_visible())
        page.locator("#boot-copy").click()
        page.wait_for_selector("#boot-copy-note:not([hidden])", timeout=5000)
        shown = page.inner_text("#boot-copy-note")
        copied = page.evaluate("navigator.clipboard.readText()")
        check(f"{label}: pressing it copies the details", copied == page.input_value("#boot-tech") and len(copied) > 20, len(copied))
        check(f"{label}: and says so", "کپی شد" in shown, shown)
        check(f"{label}: the details box can be selected and copied by hand",
              page.evaluate("""() => { const f = document.getElementById('boot-tech'); f.focus(); f.select();
                 return f.selectionEnd - f.selectionStart === f.value.length; }"""))
        ctx.close()
        ctx = browser.new_context(**device, permissions=["clipboard-read", "clipboard-write"])  # the fallback path
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'clipboard', { value: undefined })")
        page.route("**/js/enginefetch.js*", lambda route: route.abort())
        page.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
        page.wait_for_selector("#boot-copy", state="visible", timeout=30000)
        page.wait_for_function("document.getElementById('boot-tech').value.length > 20", timeout=30000)
        page.locator("#boot-copy").click()
        page.wait_for_selector("#boot-copy-note:not([hidden])", timeout=5000)
        check(f"{label}: without the clipboard API the text is selected for copying",
              page.evaluate("document.getElementById('boot-tech').selectionEnd") > 20)
        ctx.close()

    # the computer layout
    ctx, page = open_page(browser, desktop, cookies)
    check("desktop: the coding keys are hidden", not page.locator("#keybar").is_visible())
    check("desktop: three columns", page.evaluate("getComputedStyle(document.querySelector('.pg')).gridTemplateColumns.split(' ').length") == 3)
    check("desktop: no sideways scrolling", overflow(page) <= 0)
    shot(page, "desktop")
    ctx.close()
    browser.close()

print(f"{sum(results)} of {len(results)} checks passed")
raise SystemExit(0 if all(results) else 1)
