"""Offline tests for the relay (no network). Run with the service venv:

    /opt/teacher-ai/venv/bin/python /root/Storage/teacher/11th-grade/ai-proxy/test_app.py
"""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
CFG = {
    "port": 8787,
    "max_tokens": 50,
    "attempt_timeout_seconds": 5,
    "total_budget_seconds": 60,
    "referer": "https://example.invalid/",
    "warp_proxies": ["socks5://127.0.0.1:1", "socks5://127.0.0.1:2"],
    "rate": {"seconds": 60, "per_key": 1000, "per_ip": 1000},
    "providers": {
        "openrouter": {
            "label": "OpenRouter",
            "url": "https://or.invalid/chat",
            "key_pattern": "^sk-or-[A-Za-z0-9_\\-]{8,250}$",
            "headers": {"X-Title": "t"},
            "models": ["m1", "m2", "m3"],
        },
        "groq": {
            "label": "Groq",
            "url": "https://groq.invalid/chat",
            "key_pattern": "^gsk_[A-Za-z0-9_\\-]{8,250}$",
            "headers": {},
            "models": ["g1", "g2"],
        },
    },
}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
    json.dump(CFG, tmp)
os.environ["TEACHER_AI_CONFIG"] = tmp.name
spec = importlib.util.spec_from_file_location("app", HERE / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
os.unlink(tmp.name)

OR_KEY = "sk-or-v1-abcdefgh"
GROQ_KEY = "gsk_abcdefgh1234"


def reply(text):
    return lambda req: httpx.Response(200, json={"choices": [{"message": {"content": text}}]})


def status(code):
    return lambda req: httpx.Response(code, json={"error": {"message": "x"}})


def down(req):
    raise httpx.ConnectError("refused", request=req)


def slow(req):
    raise httpx.ReadTimeout("slow", request=req)


def use(script, proxies=1):
    """Route each request by its model name; returns the list of models called."""
    calls = []

    def handler(req):
        model = json.loads(req.content)["model"]
        calls.append(model)
        return script.get(model, status(404))(req)

    app.CLIENTS = [(f"mock{i}", httpx.Client(transport=httpx.MockTransport(handler))) for i in range(proxies)]
    return calls


MSGS = app.build_messages({"action": "explain_problem", "problem": {"title": "t", "statement": "s"}})


class AskTests(unittest.TestCase):
    def test_success_reports_model_and_provider(self):
        use({"m1": reply("  سلام  ")})
        self.assertEqual(app.ask("openrouter", OR_KEY, MSGS), (200, {"answer": "سلام", "model": "m1", "provider": "openrouter"}))

    def test_key_is_sent_as_bearer_and_extra_headers_are_kept(self):
        seen = {}

        def handler(req):
            seen["auth"] = req.headers["authorization"]
            seen["title"] = req.headers.get("x-title")
            return reply("ok")(req)

        app.CLIENTS = [("mock", httpx.Client(transport=httpx.MockTransport(handler)))]
        app.ask("openrouter", OR_KEY, MSGS)
        self.assertEqual(seen["auth"], "Bearer " + OR_KEY)
        self.assertEqual(seen["title"], "t")

    def test_key_error_stops_at_once(self):
        calls = use({"m1": status(401), "m2": reply("never")})
        status_code, data = app.ask("openrouter", OR_KEY, MSGS)
        self.assertEqual(status_code, 401)
        self.assertIn("error", data)
        self.assertEqual(calls, ["m1"])

    def test_busy_model_falls_back_to_next(self):
        calls = use({"m1": status(429), "m2": reply("second")})
        self.assertEqual(app.ask("openrouter", OR_KEY, MSGS)[1]["model"], "m2")
        self.assertEqual(calls, ["m1", "m2"])

    def test_empty_answer_falls_back(self):
        use({"m1": reply("   "), "m2": reply("x")})
        self.assertEqual(app.ask("openrouter", OR_KEY, MSGS)[1]["answer"], "x")

    def test_timeout_falls_back(self):
        use({"m1": slow, "m2": reply("after timeout")})
        self.assertEqual(app.ask("openrouter", OR_KEY, MSGS)[1]["answer"], "after timeout")

    def test_all_busy_says_so(self):
        use({"m1": status(429), "m2": status(429), "m3": status(429)})
        status_code, data = app.ask("openrouter", OR_KEY, MSGS)
        self.assertEqual(status_code, 429)
        self.assertIn("پر هستند", data["error"])

    def test_all_missing_is_502(self):
        use({})
        self.assertEqual(app.ask("openrouter", OR_KEY, MSGS)[0], 502)

    def test_warp_down_does_not_try_other_models(self):
        calls = use({"m1": down, "m2": reply("never")}, proxies=2)
        status_code, data = app.ask("openrouter", OR_KEY, MSGS)
        self.assertEqual(status_code, 503)
        self.assertEqual(calls, ["m1", "m1"])  # one attempt per WARP proxy, then stop

    def test_groq_uses_its_own_models_in_order(self):
        calls = use({"g1": status(404), "g2": reply("groq answer")})
        self.assertEqual(app.ask("groq", GROQ_KEY, MSGS)[1], {"answer": "groq answer", "model": "g2", "provider": "groq"})
        self.assertEqual(calls, ["g1", "g2"])


class PromptTests(unittest.TestCase):
    PROBLEM = {
        "title": "جمع دو عدد",
        "topic": "نوع داده",
        "statement": "دو عدد بخوانید و جمع را چاپ کنید.",
        "mode": "stdio",
        "samples": [{"stdin": "1\n2\n", "stdout": "3\n"}],
    }

    def test_each_action_has_its_own_instruction(self):
        texts = {
            action: app.build_messages({"action": action, "problem": self.PROBLEM})[0]["content"]
            for action in app.ACTIONS
        }
        self.assertEqual(len(set(texts.values())), 3)
        for action, text in texts.items():
            self.assertIn(app.ACTIONS[action], text)

    def test_unknown_action_is_refused(self):
        with self.assertRaises(ValueError):
            app.build_messages({"action": "write_any_code", "problem": self.PROBLEM})

    def test_sample_io_sends_the_official_samples(self):
        user = app.build_messages({"action": "sample_io", "problem": self.PROBLEM})[1]["content"]
        self.assertIn("نمونه‌های رسمی", user)
        self.assertIn("'1\\n2\\n'", user)

    def test_review_sends_code_and_the_failed_test(self):
        payload = {
            "action": "review_answer",
            "problem": self.PROBLEM,
            "code": "print(1 + 2)",
            "failure": {"kind": "stdio", "index": "2", "stdin": "5\n1\n", "expected": "6", "actual": "51", "message": ""},
        }
        user = app.build_messages(payload)[1]["content"]
        self.assertIn("print(1 + 2)", user)
        self.assertIn("شماره آزمون: 2", user)
        self.assertIn("خروجی دانش‌آموز: 51", user)

    def test_review_without_code_says_so(self):
        user = app.build_messages({"action": "review_answer", "problem": self.PROBLEM, "code": "  "})[1]["content"]
        self.assertIn("هنوز کدی نوشته نشده است", user)

    def test_long_values_are_cut(self):
        problem = dict(self.PROBLEM, title="ت" * 500)
        user = app.build_messages({"action": "explain_problem", "problem": problem})[1]["content"]
        self.assertIn("کوتاه شد", user)


class EnglishTests(unittest.TestCase):
    PROBLEM = {"title": "Sum", "topic": "Data types", "statement": "Read two numbers.", "mode": "stdio",
               "samples": [{"stdin": "1\n2\n", "stdout": "3\n"}]}

    def messages(self, action, **extra):
        return app.build_messages({"action": action, "problem": self.PROBLEM, "lang": "en", **extra})

    def test_the_prompt_asks_for_english(self):
        for action in app.ACTIONS:
            system = self.messages(action)[0]["content"]
            self.assertIn("English", system)
            self.assertNotRegex(system, r"[\u0600-\u06FF]")

    def test_the_user_text_is_english(self):
        user = self.messages("sample_io")[1]["content"]
        self.assertIn("Problem statement:", user)
        self.assertIn("The official samples", user)
        self.assertNotRegex(user, r"[\u0600-\u06FF]")

    def test_review_in_english(self):
        user = self.messages("review_answer", code="print(1)", failure={"kind": "stdio", "index": 2, "stdin": "5",
                                                                        "expected": "6", "actual": "51", "message": ""})[1]["content"]
        self.assertIn("The student's code:", user)
        self.assertIn("Test number: 2", user)
        self.assertNotRegex(user, r"[\u0600-\u06FF]")
        empty = self.messages("review_answer", code=" ")[1]["content"]
        self.assertIn("no code has been written yet", empty)

    def test_without_a_language_it_is_persian(self):
        system = app.build_messages({"action": "explain_problem", "problem": self.PROBLEM})[0]["content"]
        self.assertIn("فارسی", system)
        self.assertEqual(app.language({"lang": "de"}), "fa")
        self.assertEqual(app.language({"lang": "en"}), "en")

    def test_every_persian_error_has_an_english_text(self):
        for fa, en in app.EN_ERRORS.items():
            self.assertRegex(fa, r"[\u0600-\u06FF]")
            self.assertNotRegex(en, r"[\u0600-\u06FF]")


if __name__ == "__main__":
    unittest.main(verbosity=1)
