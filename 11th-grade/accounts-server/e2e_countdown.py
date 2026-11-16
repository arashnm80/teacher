"""Browser check of the countdown: the open problem ticks, every unsolved problem in the list shows its
remaining time, and the time functions behave at the edges. Needs the online test server (E2E_BASE)."""
import os
import re
import sys

from playwright.sync_api import sync_playwright

BASE = os.environ.get("E2E_BASE", "http://127.0.0.1:8800")
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""), flush=True)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)[:160]))
    page.goto(BASE + "/playground/index.html", wait_until="domcontentloaded")
    page.wait_for_selector("#auth-dialog[open]", timeout=120000)
    page.click("#auth-tab-register")
    page.fill("#auth-phone", "09123456780")
    page.fill("#auth-national", "0499370899")
    page.fill("#auth-name", "علی احمدی")
    page.select_option("#auth-class", "201")
    page.fill("#auth-password", "abc12345")
    page.fill("#auth-password2", "abc12345")
    page.click("#auth-submit")
    page.wait_for_function("!document.getElementById('auth-dialog').open", timeout=60000)
    page.wait_for_selector(".problem-link", timeout=240000)
    page.locator(".problem-link").first.click()
    page.wait_for_selector("#problem-countdown", timeout=30000)
    first = page.inner_text("#problem-countdown")
    check("the open problem shows the time left", re.fullmatch(r"[۰-۹]+ روز و [۰-۹]{2}:[۰-۹]{2}:[۰-۹]{2}|[۰-۹]{2}:[۰-۹]{2}:[۰-۹]{2}", first), first)
    page.wait_for_timeout(2300)
    check("the countdown ticks every second", page.inner_text("#problem-countdown") != first)
    chips = page.locator(".problem-link .remain")
    texts = [chips.nth(i).inner_text() for i in range(chips.count())]
    shown = [t for t in texts if t.startswith("⏳")]
    check("every problem in the list shows its remaining time", len(shown) == len(texts) == 100, f"{len(shown)} of {len(texts)}")
    check("the remaining time in the list is compact", all(re.fullmatch(r"⏳ [۰-۹]+ (روز|ساعت|دقیقه)|⏳ گذشته", t) for t in shown), shown[0])
    # The time functions at their edges
    out = page.evaluate("""async () => {
        const m = await import('./js/countdown.js?v=1');
        return [m.longText(0), m.longText(-5), m.longText(90061000), m.longText(3723000), m.shortText(0),
                m.shortText(59000), m.shortText(3 * 3600000), m.shortText(2 * 86400000 + 5), m.level(0),
                m.level(2 * 3600000), m.level(5 * 3600000), m.level(30 * 3600000)];
    }""")
    check("the time functions are right at the edges", out == [
        "مهلت گذشته", "مهلت گذشته", "۱ روز و ۰۱:۰۱:۰۱", "۰۱:۰۲:۰۳", "گذشته", "۱ دقیقه", "۳ ساعت", "۲ روز",
        "late", "urgent", "soon", "ok"], str(out))
    # the server's clock wins over this computer's
    out = page.evaluate("""async () => {
        const m = await import('./js/countdown.js?v=1');
        m.setServerTime(new Date(Date.now() + 3600000).toISOString());   // the server is one hour ahead
        const ahead = m.remainingMs(new Date(Date.now() + 7200000).toISOString());
        return Math.round(ahead / 60000);
    }""")
    check("the server's clock is used (one hour ahead leaves 60 minutes of 120)", out == 60, str(out))
    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()
print(f"{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)
