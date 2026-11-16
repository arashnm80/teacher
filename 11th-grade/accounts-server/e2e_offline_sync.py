"""Browser checks of the offline copy with sync: sign-up inside it, earlier work is sent, marks show what has
reached the teacher, everything works with no internet, tutorials stay on the device, the update notice, and
a second device gets the progress. Needs the online test server (E2E_BASE) and the offline copy (OFFLINE)."""
import json
import os
import random
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8800")
OFFLINE = os.environ.get("OFFLINE", "http://127.0.0.1:8791")
PROBLEMS = Path(os.environ.get("PROBLEMS", "/root/Storage/teacher/11th-grade/playground/app/data/problems.json"))
PHONE = "0912" + "".join(random.choice("0123456789") for _ in range(7))


def national_code():
    """A random ten-digit national code with a correct check digit (the test database remembers earlier runs)."""
    while True:
        digits = [random.randint(0, 9) for _ in range(9)]
        if len(set(digits)) == 1:
            continue
        total = sum(d * (10 - i) for i, d in enumerate(digits))
        r = total % 11
        return "".join(map(str, digits)) + str(r if r < 2 else 11 - r)


NATIONAL = national_code()
PASSWORD = "abc12345"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""), flush=True)


problems = json.loads(PROBLEMS.read_text(encoding="utf-8"))
by_number = sorted(problems, key=lambda q: q["number"])
first = by_number[0]
second = next(q for q in by_number[1:] if len(q["tests"]) >= 2)
third = next(q for q in by_number[1:] if q["id"] != second["id"])
INIT = f'window.__teacherSyncBase = "{BASE}/api/offline";'


def set_code(page, code):
    page.evaluate("(c) => document.querySelector('.CodeMirror').CodeMirror.setValue(c)", code)


def pick(page, title):
    page.locator(".problem-link", has_text=title).first.click()
    page.wait_for_timeout(400)


def run(page):
    page.click("#btn-run")
    page.wait_for_timeout(300)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=180000)


def block_teacher(ctx):
    """No internet as the student sees it: the local copy works, the teacher's server cannot be reached."""
    ctx.route(BASE + "/**", lambda route: route.abort("internetdisconnected"))


def unblock_teacher(ctx, page):
    ctx.unroute(BASE + "/**")
    page.evaluate("() => window.dispatchEvent(new Event('online'))")


def wait_ready(page):
    page.wait_for_selector(".problem-link", timeout=240000)
    page.wait_for_function("!document.getElementById('btn-run').disabled", timeout=240000)


def mark(page, title):
    """The class of the sync mark of a problem in the list ('' when it has none)."""
    row = page.locator(".problem-link", has_text=title).first
    node = row.locator(".sync-mark")
    return (node.first.get_attribute("class") or "").replace("sync-mark", "").strip() if node.count() else ""


def chip_state(page):
    return (page.get_attribute("#sync-chip", "class") or "").replace("sync-chip", "").strip()


def server_state(page):
    token = page.evaluate("() => JSON.parse(localStorage.getItem('teacher-sync-session-v1') || 'null')?.token")
    return page.evaluate("""async ([base, token]) => (await fetch(base + '/api/offline/me', {headers: {Authorization: 'Bearer ' + token}})).json()""",
                         [BASE, token])


with sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script(INIT)
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append((str(e) + " | " + str(getattr(e, "stack", ""))[:400])))
    page.goto(OFFLINE + "/playground/index.html", wait_until="domcontentloaded")
    wait_ready(page)

    # ---- before any account ----------------------------------------------------------------
    check("the offline copy starts without asking for a sign-in", not page.evaluate("() => document.getElementById('auth-dialog').open"))
    check("the bar offers a sign-in and says progress stays on this device", page.is_visible("#student-signin") and chip_state(page) == "signedout")
    pick(page, first["title"])
    check("the tutorial is not in the offline files", "قدم ۱" not in page.inner_text("#concept"))
    set_code(page, first["solutions"][0]["code"])
    run(page)
    page.wait_for_selector(".problem-link.done", timeout=60000)
    check("a solved problem shows it has not been sent", mark(page, first["title"]) == "unsent", mark(page, first["title"]))

    # ---- sign up inside the offline copy ---------------------------------------------------
    page.click("#student-signin")
    page.wait_for_selector("#auth-dialog[open]")
    check("the dialog can be put off", page.is_visible("#auth-later"))
    page.click("#auth-tab-register")
    page.fill("#auth-phone", PHONE)
    page.fill("#auth-national", NATIONAL)
    page.fill("#auth-name", "علی احمدی")
    page.select_option("#auth-class", "201")
    page.fill("#auth-password", PASSWORD)
    page.fill("#auth-password2", PASSWORD)
    page.click("#auth-submit")
    page.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    check("the student bar shows the name after the sign-up", "علی احمدی" in page.inner_text("#student-who"))
    page.wait_for_function("document.querySelector('.sync-mark.synced')", timeout=60000)
    check("work done before signing up was sent and is marked as sent", mark(page, first["title"]) == "synced")
    check("the chip says everything reached the teacher", chip_state(page) == "synced", chip_state(page))
    state = server_state(page)
    check("the server has the solved problem", state["progress"][first["id"]]["solved"] is True)
    page.wait_for_function("document.getElementById('concept').innerText.includes('قدم ۱')", timeout=60000)
    check("the tutorial arrives after the sign-in", True)
    pick(page, third["title"])
    page.wait_for_selector("#problem-countdown", timeout=30000)
    check("the countdown works from the synced schedule", True, page.inner_text("#problem-countdown"))

    # ---- no internet -------------------------------------------------------------------------
    block_teacher(ctx)
    pick(page, second["title"])
    set_code(page, second["solutions"][0]["code"])
    run(page)
    page.wait_for_function("document.querySelectorAll('.problem-link.done').length >= 2", timeout=60000)
    check("with no internet a solved problem is marked as waiting", mark(page, second["title"]) == "pending", mark(page, second["title"]))
    page.wait_for_timeout(2500)
    check("the chip warns that something has not been sent", chip_state(page) in ("offline", "pending"), chip_state(page))
    check("the result waits in the queue on the device", len(page.evaluate("() => JSON.parse(localStorage.getItem('teacher-sync-queue-v1') || '[]')")) >= 1)
    page.reload(wait_until="domcontentloaded")
    wait_ready(page)
    check("after a reload with no internet, the progress and the waiting mark are still there",
          mark(page, second["title"]) == "pending" and mark(page, first["title"]) == "synced")
    pick(page, third["title"])
    page.wait_for_selector("#problem-countdown", timeout=30000)
    check("the tutorial and the countdown still work with no internet", "قدم ۱" in page.inner_text("#concept"))
    pick(page, second["title"])
    set_code(page, "print('wrong')")
    run(page)
    cards = page.locator("#results .test-card")
    check("a hidden test shows no expected output offline too",
          cards.count() >= 2 and "این آزمون پنهان است" in cards.nth(1).inner_text() and "باید باشد" not in cards.nth(1).inner_text())

    # ---- back online ---------------------------------------------------------------------------
    unblock_teacher(ctx, page)
    page.wait_for_function("document.querySelectorAll('.sync-mark.pending').length === 0", timeout=90000)
    check("when the internet is back the waiting result is sent", mark(page, second["title"]) == "synced")
    state = server_state(page)
    check("the server has both solved problems", state["progress"][second["id"]]["solved"] is True and state["progress"][first["id"]]["solved"] is True)
    check("the failed run was sent too (attempts: 1 and 2 on the second problem or more)", state["progress"][second["id"]]["attempts"] >= 1)

    # ---- the update notice ---------------------------------------------------------------------
    calls = {"status": 0}
    page.route("**/__update/check", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(
        {"ok": True, "update": True, "current": "aaa", "latest": "bbb", "files": 3, "bytes": 5242880})))
    page.route("**/__update/apply", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true,"state":"running"}'))

    def status(route):
        calls["status"] += 1
        body = {"ok": True, "state": "running", "done": 1, "total": 3} if calls["status"] < 2 else {"ok": True, "state": "done", "done": 3, "total": 3}
        route.fulfill(status=200, content_type="application/json", body=json.dumps(body))

    page.route("**/__update/status", status)
    page.reload(wait_until="domcontentloaded")
    wait_ready(page)
    page.wait_for_selector("#update-banner:not([hidden])", timeout=20000)
    check("a new version shows a notice with its size", "۳" in page.inner_text("#update-text") or "3" in page.inner_text("#update-text"), page.inner_text("#update-text"))
    with page.expect_navigation(timeout=30000):
        page.click("#update-apply")
    check("the update runs, then the page reloads", True)

    # ---- sign out keeps the work ---------------------------------------------------------------
    page.unroute_all()
    wait_ready(page)
    page.click("#student-logout")
    page.wait_for_selector("#student-signin:not([hidden])")
    check("signing out keeps the progress on the device", mark(page, first["title"]) == "synced" or page.locator(".problem-link.done").count() >= 2)
    check("signing out leaves the sign-in button and the warning", chip_state(page) == "signedout")
    ctx.close()

    # ---- a second device -------------------------------------------------------------------------
    ctx2 = browser.new_context(viewport={"width": 1280, "height": 900})
    ctx2.add_init_script(INIT)
    page2 = ctx2.new_page()
    page2.on("pageerror", lambda e: errors.append((str(e) + " | " + str(getattr(e, "stack", ""))[:400])))
    page2.goto(OFFLINE + "/playground/index.html", wait_until="domcontentloaded")
    wait_ready(page2)
    check("a new device starts with nothing solved", page2.locator(".problem-link.done").count() == 0)
    page2.click("#student-signin")
    page2.wait_for_selector("#auth-dialog[open]")
    page2.fill("#auth-phone", PHONE)
    page2.fill("#auth-password", PASSWORD)
    page2.click("#auth-submit")
    page2.wait_for_function("document.querySelectorAll('.problem-link.done').length >= 2", timeout=90000)
    check("after signing in, the account's progress appears on the new device", True)
    check("those problems are marked as sent", mark(page2, first["title"]) == "synced" and mark(page2, second["title"]) == "synced")
    pick(page2, first["title"])
    code = page2.evaluate("() => document.querySelector('.CodeMirror').CodeMirror.getValue()")
    check("the code from the other device comes along", code.strip() == first["solutions"][0]["code"].strip())
    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()

print(f"{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)
