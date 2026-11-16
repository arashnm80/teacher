"""End-to-end checks: sign-up, progress across reloads, hidden tests, the guides and the assistant from the start,
single session, the teacher's reset, the CSV export, and the offline copy (no sign-in, progress in the browser).

The online server and the offline copy must already be running (see the run notes in the scratchpad).
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

import os
BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8790")
OFFLINE = "http://127.0.0.1:8791"
PROBLEMS = Path("/root/Storage/teacher/11th-grade/playground/app/data/problems.json")
PHONE = "09123456789"
NATIONAL = "0499370899"
NAME = "علی احمدی"
PASSWORD = "abc12345"
NEW_PASSWORD = "newpass999"
ADMIN_PASSWORD = "admin-e2e-pass-123"

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""), flush=True)


problems = json.loads(PROBLEMS.read_text(encoding="utf-8"))
multi = next(p for p in problems if len(p["tests"]) >= 2 and p.get("solutions"))
simple = next(p for p in problems if p["id"] != multi["id"] and p.get("solutions"))


def set_code(page, code):
    page.evaluate("(c) => document.querySelector('.CodeMirror').CodeMirror.setValue(c)", code)


def get_code(page):
    return page.evaluate("() => document.querySelector('.CodeMirror').CodeMirror.getValue()")


def pick(page, title):
    page.locator(".problem-link", has_text=title).first.click()
    page.wait_for_timeout(400)


def wait_ready(page, timeout=240000):
    page.wait_for_timeout(300)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=timeout)


def dialog_open(page):
    return page.evaluate("() => document.getElementById('auth-dialog').open")


def run_code(page):
    page.click("#btn-run")
    page.wait_for_timeout(300)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=180000)


def register(page):
    page.click("#auth-tab-register")
    page.fill("#auth-phone", PHONE)
    page.fill("#auth-national", NATIONAL)
    page.fill("#auth-name", NAME)
    page.select_option("#auth-class", "201")
    page.fill("#auth-password", PASSWORD)
    page.fill("#auth-password2", PASSWORD)
    page.click("#auth-submit")
    page.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)


def login(page, password):
    page.fill("#auth-phone", PHONE)
    page.fill("#auth-password", password)
    page.click("#auth-submit")


def new_context(browser):
    return browser.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])


with sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []

    # ---- A: a new student signs up and works ---------------------------------------------
    ctx_a = new_context(browser)
    page_a = ctx_a.new_page()
    page_a.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page_a.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page_a.wait_for_selector("#auth-dialog[open]", timeout=120000)
    check("first visit asks for a sign-in", True)
    check("no questions are sent before sign-in", page_a.locator(".problem-link").count() == 0)
    register(page_a)
    page_a.wait_for_selector(".problem-link", timeout=240000)
    wait_ready(page_a)
    check("the student bar shows the name", NAME in page_a.inner_text("#student-name"))
    check("the run button has the new label", page_a.inner_text("#btn-run").strip() == "بررسی و تست")

    pick(page_a, multi["title"])
    concept = page_a.inner_text("#concept")
    page_a.wait_for_function("document.getElementById('concept').innerText.includes('قدم ۱')", timeout=60000)
    check("the guide is open before a pass", "قدم ۱" in page_a.inner_text("#concept"))

    set_code(page_a, "print('wrong answer')")
    run_code(page_a)
    cards = page_a.locator("#results .test-card")
    check("a failing run shows the result cards", cards.count() >= 2, f"cards={cards.count()}")
    hidden = cards.nth(1).inner_text()
    check("a hidden test shows no expected output",
          "این آزمون پنهان است" in hidden and "باید باشد" not in hidden and "مورد انتظار" not in hidden)

    set_code(page_a, multi["solutions"][0]["code"])
    run_code(page_a)
    page_a.wait_for_selector(".problem-link.done", timeout=60000)
    check("a passing run marks the question done", True)
    stored = page_a.evaluate("async () => (await (await fetch('/api/student/progress')).json()).progress")
    check("the server stored the pass", stored.get(multi["id"], {}).get("solved") is True)
    page_a.wait_for_function("document.getElementById('concept').innerText.includes('قدم ۱')", timeout=60000)
    check("the guide stays open after the pass", "قدم ۱" in page_a.inner_text("#concept"))

    page_a.reload(wait_until="domcontentloaded")
    page_a.wait_for_selector(".problem-link", timeout=240000)
    check("a reload keeps the session", not dialog_open(page_a))
    wait_ready(page_a)
    check("the solved mark survives a reload", page_a.locator(".problem-link.done").count() >= 1)
    pick(page_a, multi["title"])
    check("the last code is restored", get_code(page_a).strip() == multi["solutions"][0]["code"].strip())

    pick(page_a, simple["title"])
    check("the assistant is open before a pass", "بعد از قبول شدن" not in page_a.inner_text("#ai-hint"))
    page_a.fill("#ai-key", "sk-or-v1-abcdefgh12345678")
    page_a.click("#ai-key-save")
    check("the assistant buttons work before a pass once a key is saved",
          page_a.locator(".ai-action").first.is_enabled())

    # ---- B: a second browser takes over the account -------------------------------------
    ctx_b = new_context(browser)
    page_b = ctx_b.new_page()
    page_b.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page_b.wait_for_selector("#auth-dialog[open]", timeout=120000)
    login(page_b, PASSWORD)
    page_b.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    page_b.wait_for_selector(".problem-link", timeout=240000)
    check("a second browser signs in to the same account", True)
    pick(page_a, simple["title"])
    page_a.click("#btn-run")
    page_a.wait_for_selector("#auth-dialog[open]", timeout=120000)
    check("the first browser is signed out (one session at a time)", True)
    ctx_b.close()

    # ---- C: the teacher resets the password ---------------------------------------------
    # The panel's content policy forbids string evaluation; the test harness must evaluate nothing
    # on that page, so the policy is bypassed for this context only (the panel itself is unchanged).
    ctx_c = browser.new_context(viewport={"width": 1280, "height": 900}, bypass_csp=True)
    page_c = ctx_c.new_page()
    page_c.on("dialog", lambda d: d.accept())
    page_c.goto(BASE + "/admin/index.html", wait_until="domcontentloaded")
    page_c.wait_for_selector("#login-view:not([hidden])", timeout=60000)
    page_c.fill("#admin-password", ADMIN_PASSWORD)
    page_c.click("#login-form button[type=submit]")
    page_c.wait_for_selector("#app-view:not([hidden])", timeout=60000)
    page_c.wait_for_selector("#students button.link-button", timeout=60000)
    check("the teacher sees the student list", NAME in page_c.inner_text("#students"))
    page_c.click(f"#students button.link-button:has-text('{NAME}')")
    page_c.wait_for_selector("#detail:not([hidden])", timeout=60000)
    check("the student's progress is shown", "قبول شده" in page_c.inner_text("#detail-progress") or
          multi["title"] in page_c.inner_text("#detail-progress"))
    page_c.click("#detail-reset")
    page_c.wait_for_selector("#status:has-text('بازنشانی')", timeout=30000)
    check("the teacher resets the password", True)
    body = page_c.request.get(BASE + "/api/admin/export.csv").body()
    check("the CSV export opens with a byte-order mark", body.startswith(b"\xef\xbb\xbf"))
    check("the CSV export lists the student", NAME.encode("utf-8") in body)
    audit = page_c.request.get(BASE + "/api/admin/audit").json()
    check("the reset is in the audit log", any(e["action"] == "reset-password" for e in audit["entries"]))
    ctx_c.close()

    # ---- D: the student chooses a new password ------------------------------------------
    ctx_d = new_context(browser)
    page_d = ctx_d.new_page()
    page_d.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page_d.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page_d.wait_for_selector("#auth-dialog[open]", timeout=120000)
    login(page_d, PASSWORD)
    page_d.wait_for_function("document.getElementById('auth-title').textContent.includes('انتخاب رمز تازه')",
                             timeout=60000)
    check("after a reset the sign-in asks for a new password", True)
    page_d.fill("#auth-national", NATIONAL)
    page_d.fill("#auth-password", NEW_PASSWORD)
    page_d.fill("#auth-password2", NEW_PASSWORD)
    page_d.click("#auth-submit")
    page_d.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    page_d.wait_for_selector(".problem-link", timeout=240000)
    check("the student is in with the new password", True)
    check("the progress is still there after the reset of the password",
          page_d.locator(".problem-link.done").count() >= 1)
    page_d.click("#student-logout")
    page_d.wait_for_selector("#auth-dialog[open]", timeout=120000)
    login(page_d, NEW_PASSWORD)
    page_d.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    check("the new password works after a sign-out", True)
    ctx_d.close()

    # ---- E: the offline copy keeps working as before ------------------------------------
    ctx_f = new_context(browser)
    page_f = ctx_f.new_page()
    page_f.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page_f.goto(OFFLINE + "/playground/index.html", wait_until="domcontentloaded")
    page_f.wait_for_selector(".problem-link", timeout=240000)
    check("the offline copy asks for no sign-in", not dialog_open(page_f))
    check("the offline copy has the new run label", page_f.inner_text("#btn-run").strip() == "بررسی و تست")
    wait_ready(page_f)
    pick(page_f, simple["title"])
    set_code(page_f, simple["solutions"][0]["code"])
    run_code(page_f)
    page_f.wait_for_selector(".problem-link.done", timeout=60000)
    page_f.reload(wait_until="domcontentloaded")
    page_f.wait_for_selector(".problem-link", timeout=240000)
    wait_ready(page_f)
    check("the offline copy keeps its progress in the browser", page_f.locator(".problem-link.done").count() >= 1)
    pick(page_f, multi["title"])
    check("the offline copy has no tutorial until a sign-in (like the website)", "قدم ۱" not in page_f.inner_text("#concept"))
    set_code(page_f, "print('wrong')")
    run_code(page_f)
    offline_cards = page_f.locator("#results .test-card")
    check("the offline copy hides the expected output of hidden tests, like the website",
          offline_cards.count() >= 2 and "این آزمون پنهان است" in offline_cards.nth(1).inner_text()
          and "باید باشد" not in offline_cards.nth(1).inner_text())
    ctx_f.close()

    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()

print(f"{sum(results)} of {len(results)} checks passed", flush=True)
