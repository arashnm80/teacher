"""Language switch in the playground: English draws the whole interface in English and left-to-right,
Persian brings it back, the choice is remembered, and a result on the screen stays through the switch.

Needs the online test server (E2E_BASE) and the offline copy (E2E_OFFLINE)."""
import json
import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8800")
OFFLINE = os.environ.get("E2E_OFFLINE", "http://127.0.0.1:8791")
results = []
PROBLEMS = json.loads(Path("/root/Storage/teacher/11th-grade/playground/app/data/problems.json").read_text(encoding="utf-8"))
import random


def national_code():
    """A random ten-digit national code with a correct check digit."""
    digits = [random.randint(0, 9) for _ in range(9)]
    if len(set(digits)) == 1:
        digits[0] = (digits[0] + 1) % 10
    total = sum(d * (10 - i) for i, d in enumerate(digits)) % 11
    return "".join(map(str, digits)) + str(total if total < 2 else 11 - total)


PHONE = "0912" + str(random.randint(1000000, 9999999))
NATIONAL = national_code()
PERSIAN = re.compile(r"[؀-ۿ]")
# Parts that hold the student's own data or code (not texts of the site).
CONTENT = ("#student-name, #auth-name, .CodeMirror, .lang-toggle, #results pre, #results .diff-block, #ai-answer, "
           "#ai-dialog-body, .link-button, .admin-code, #detail-name, #sub-rows td:nth-child(3), #sub-rows td:nth-child(4), "
           "#detail-progress td:first-child")

def check(name, ok, detail=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""), flush=True)


def persian_chrome(page):
    """Visible text nodes with Persian letters outside the content parts."""
    return page.evaluate(
        """(content) => {
          const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT']);
          const out = [];
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) {
            const node = walker.currentNode;
            const text = node.textContent.trim();
            if (!text || !/[\\u0600-\\u06FF]/.test(text)) continue;
            if (text.includes('سلام')) continue; // question 64 asks for the Persian word itself
            const el = node.parentElement;
            if (!el || skip.has(el.tagName) || el.closest(content)) continue;
            let hidden = false;
            for (let e = el; e; e = e.parentElement) {
              if (e.hidden || getComputedStyle(e).display === 'none') { hidden = true; break; }
            }
            if (hidden) continue;
            out.push(text.slice(0, 70));
          }
          return out;
        }""",
        CONTENT,
    )


def attrs_persian(page):
    return page.evaluate(
        """() => {
          const out = [];
          for (const el of document.querySelectorAll('[placeholder],[title],[aria-label]')) {
            for (const a of ['placeholder', 'title', 'aria-label']) {
              const v = el.getAttribute(a);
              if (v && /[\\u0600-\\u06FF]/.test(v) && !el.closest('.remain, #problem-list')) out.push(a + ': ' + v.slice(0, 60));
            }
          }
          return out;
        }"""
    )


def set_code(page, code):
    page.evaluate("(c) => document.querySelector('.CodeMirror').CodeMirror.setValue(c)", code)


def run_code(page):
    page.click("#btn-run")
    page.wait_for_timeout(300)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=180000)


def lang_state(page):
    return page.evaluate("() => [document.documentElement.lang, document.documentElement.dir]")


with sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []

    # ---- online ------------------------------------------------------------------------
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page.wait_for_selector("#auth-dialog[open]", timeout=120000)
    check("the first visit is Persian and right-to-left", lang_state(page) == ["fa", "rtl"], str(lang_state(page)))

    page.click("#auth-dialog [data-lang-toggle]")  # the header is under the modal window
    page.wait_for_timeout(300)
    check("the switch makes the page English and left-to-right", lang_state(page) == ["en", "ltr"], str(lang_state(page)))
    bad = persian_chrome(page) + attrs_persian(page)
    check("the sign-in dialog has no Persian left", not bad, " | ".join(bad[:6]))
    check("the sign-in title is English", re.search(r"[A-Za-z]{4}", page.inner_text("#auth-title")) is not None,
          page.inner_text("#auth-title"))

    page.click("#auth-tab-register")
    page.fill("#auth-phone", PHONE)
    page.fill("#auth-national", NATIONAL)
    page.fill("#auth-name", "علی احمدی")
    page.select_option("#auth-class", "201")
    page.fill("#auth-password", "abc12345")
    page.fill("#auth-password2", "abc12345")
    page.click("#auth-submit")
    page.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    page.wait_for_selector(".problem-link", timeout=240000)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=240000)
    check("the choice survives the sign-in", lang_state(page) == ["en", "ltr"])
    check("the run button is English", page.inner_text("#btn-run").strip() == "Check and test", page.inner_text("#btn-run"))
    bad = persian_chrome(page) + attrs_persian(page)
    check("the main page has no Persian chrome", not bad, " | ".join(bad[:10]))
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-main.png")

    page.locator(".problem-link").first.click()
    page.wait_for_timeout(500)
    set_code(page, "print('wrong answer')")
    run_code(page)
    results_text = page.inner_text("#results")
    check("the results are English", "Test 1" in results_text and "Failed" in results_text, results_text[:120])
    bad = persian_chrome(page) + attrs_persian(page)
    check("the page after a run has no Persian chrome", not bad, " | ".join(bad[:10]))
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-results.png")

    first = PROBLEMS[0]
    check("the problem is in English", page.inner_text("#problem-title").strip().endswith(first["en"]["title"]),
          page.inner_text("#problem-title"))
    bad = persian_chrome(page)
    check("the problem page has no Persian at all", not bad, " | ".join(bad[:8]))
    page.click('.tab[data-tab="hints"]')
    page.click("#btn-hint")
    check("the hint is English", first["en"]["hints"][0][:20] in page.inner_text("#hint-list"), page.inner_text("#hint-list")[:80])
    set_code(page, first["solutions"][0]["code"])
    run_code(page)
    page.wait_for_selector(".problem-link.done", timeout=60000)
    page.click('.tab[data-tab="concept"]')
    page.wait_for_function("document.getElementById('concept').innerText.includes('Step 1')", timeout=60000)
    tutorial = page.inner_text("#concept")
    check("after a pass the tutorial is in English", "Method 1" in tutorial and "Step 1" in tutorial, tutorial[:80])
    bad = persian_chrome(page)
    check("the tutorial has no Persian", not bad, " | ".join(bad[:5]))
    page.click('.tab[data-tab="results"]')
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-tutorial.png")
    page.click("#lang-toggle")
    page.wait_for_timeout(500)
    check("back to Persian and right-to-left", lang_state(page) == ["fa", "rtl"], str(lang_state(page)))
    check("the run button is Persian again", page.inner_text("#btn-run").strip() == "بررسی و تست", page.inner_text("#btn-run"))
    check("a result on the screen stays through the switch", page.locator("#results .test-card").count() >= 1)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_selector(".problem-link", timeout=240000)
    check("the Persian choice is remembered", lang_state(page) == ["fa", "rtl"])
    page.click("#lang-toggle")
    page.reload(wait_until="domcontentloaded")
    page.wait_for_selector(".problem-link", timeout=240000)
    check("the English choice is remembered", lang_state(page) == ["en", "ltr"])
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=240000)
    page.click("#btn-progress")
    page.wait_for_selector("#progress-dialog[open]", timeout=10000)
    bad = persian_chrome(page)
    check("the progress window is English", not bad and "problems solved" in page.inner_text("#progress-summary"),
          " | ".join(bad[:6]) + " / " + page.inner_text("#progress-summary"))
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-progress.png")
    ctx.close()

    # ---- offline -----------------------------------------------------------------------
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page.add_init_script("try { localStorage.setItem('grade11-lang-v2', 'en'); } catch (e) {}")
    page.goto(OFFLINE + "/playground/index.html", wait_until="domcontentloaded")
    page.wait_for_selector(".problem-link", timeout=240000)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=240000)
    check("the offline copy opens in English", lang_state(page) == ["en", "ltr"])
    bad = persian_chrome(page) + attrs_persian(page)
    check("the offline copy has no Persian chrome", not bad, " | ".join(bad[:10]))
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-offline.png")
    ctx.close()

    # ---- the teacher's panel -------------------------------------------------------------
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, bypass_csp=True)
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page.goto(BASE + "/admin/index.html", wait_until="domcontentloaded")
    page.wait_for_selector("#login-view:not([hidden])", timeout=60000)
    check("the panel starts in Persian", lang_state(page) == ["fa", "rtl"])
    page.click("#lang-toggle")
    check("the panel switches to English", lang_state(page) == ["en", "ltr"], str(lang_state(page)))
    bad = persian_chrome(page) + attrs_persian(page)
    check("the panel's sign-in has no Persian left", not bad, " | ".join(bad[:6]))
    page.fill("#admin-password", "admin-e2e-pass-123")
    page.click("#login-form button[type=submit]")
    page.wait_for_selector("#app-view:not([hidden])", timeout=60000)
    page.wait_for_selector("#students button.link-button", timeout=60000)
    bad = persian_chrome(page) + attrs_persian(page)
    check("the student list has no Persian chrome", not bad, " | ".join(bad[:8]))
    check("the count is in English", "students" in page.inner_text("#status"), page.inner_text("#status"))
    page.click("#students button.link-button")
    page.wait_for_selector("#detail:not([hidden])", timeout=60000)
    bad = persian_chrome(page)
    check("a student's page has no Persian chrome", not bad, " | ".join(bad[:8]))
    for tab in ("submissions", "schedule", "audit"):
        page.click(f"#tab-{tab}")
        page.wait_for_timeout(600)
        bad = persian_chrome(page) + attrs_persian(page)
        check(f"the {tab} part has no Persian chrome", not bad, " | ".join(bad[:6]))
    page.screenshot(path=os.environ.get("E2E_SHOTS", "/tmp") + "/lang-en-admin.png")
    page.click("#lang-toggle")
    check("the panel goes back to Persian", lang_state(page) == ["fa", "rtl"])
    ctx.close()

    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()

print(f"{sum(results)} of {len(results)} checks passed", flush=True)
