"""Language switch in the playground: English draws the whole interface in English and left-to-right,
Persian brings it back, the choice is remembered, and a result on the screen stays through the switch.

Needs the online test server (E2E_BASE) and the offline copy (E2E_OFFLINE)."""
import os
import re

from playwright.sync_api import sync_playwright

BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8800")
OFFLINE = os.environ.get("E2E_OFFLINE", "http://127.0.0.1:8791")
results = []
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
# Parts that hold the problems' own texts (Persian until the English content is added) or the student's own data.
CONTENT = ("#topic-filter, #problem-list, #problem-title, #problem-topic, #statement, #concept, #hint-list, .CodeMirror, "
           "#pack-list, #student-name, #progress-list, #results .diff-block, #results pre, #lesson-link a, "
           "#auth-name, .lang-toggle, #problem-deadline, .remain, #sync-summary-last, #ai-answer, #ai-dialog-body")


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

    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()

print(f"{sum(results)} of {len(results)} checks passed", flush=True)
