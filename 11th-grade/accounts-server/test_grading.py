"""Tests for grading.py: the rules, the comparisons and how a judge's answer becomes an outcome.

Run with:  python3 test_grading.py   (no sandbox needed: the judge is replaced by a function)
"""
import unittest

import grading as g


def judge_says(*runs):
    def ask(request):
        return {"ok": True, "results": [
            {"status": "ok", "stdout": "", "error": None, "value": None, "ms": 1, "truncated": False, **run}
            for run in runs]}
    return ask


STDIO = {"id": "q", "mode": "stdio", "samples": [{}], "constraints": None,
         "tests": [{"stdin": "a\n", "stdout": "A\n"}, {"stdin": "b\n", "stdout": "B\n"}, {"stdin": "c\n", "stdout": "C\n"}]}
FUNC = {"id": "f", "mode": "function", "functionName": "twice", "samples": [{}],
        "tests": [{"call": {"args": [2], "expected": 4}}, {"call": {"args": [0.5], "expected": 1}}]}


class Rules(unittest.TestCase):
    def issues(self, code, **rules):
        return [(i["type"], i["token"]) for i in g.constraint_issues(code, rules)]

    def test_keywords_are_whole_words(self):
        self.assertEqual(self.issues("for i in x: pass", forbid=["for"]), [("forbid", "for")])
        self.assertEqual(self.issues("format = 1", forbid=["for"]), [])
        self.assertEqual(self.issues("x = 1", require=["while"]), [("require", "while")])

    def test_calls_need_the_bracket_and_not_a_longer_name(self):
        self.assertEqual(self.issues("m = max(1, 2)", forbid=["max"]), [("forbid", "max")])
        self.assertEqual(self.issues("max = 3", forbid=["max"]), [])
        self.assertEqual(self.issues("my_max(1)", forbid=["max"]), [])
        self.assertEqual(self.issues("obj.max(1)", forbid=["max"]), [])
        self.assertEqual(self.issues("max  (1)", forbid=["max"]), [("forbid", "max")])

    def test_strings_and_comments_do_not_count(self):
        self.assertEqual(self.issues("print('for while sum(')", forbid=["for", "while", "sum"]), [])
        self.assertEqual(self.issues("x = 1  # for", forbid=["for"]), [])
        self.assertEqual(self.issues('"""for\nwhile"""\nx = 1', forbid=["for", "while"]), [])
        self.assertEqual(self.issues("for i in range(2): pass  # while", require=["for"], forbid=["while"]), [])

    def test_import_means_import_or_from(self):
        self.assertEqual(self.issues("from math import pi", forbid=["import"]), [("forbid", "import")])
        self.assertEqual(self.issues("import math", forbid=["import"]), [("forbid", "import")])
        self.assertEqual(self.issues("x = 1", forbid=["import"]), [])

    def test_no_rules(self):
        self.assertEqual(g.constraint_issues("anything", None), [])
        self.assertEqual(g.constraint_issues("anything", {}), [])


class Comparing(unittest.TestCase):
    def test_line_endings_are_made_alike(self):
        self.assertEqual(g.normalize_newlines("a\r\nb\rc\n"), "a\nb\nc\n")

    def test_numbers(self):
        self.assertTrue(g.deep_equal(1, 1.0))
        self.assertTrue(g.deep_equal(0.1 + 0.2, 0.3))
        self.assertTrue(g.deep_equal(3.141592653589793, 3.1415926535))
        self.assertFalse(g.deep_equal(3.14, 3.15))
        self.assertFalse(g.deep_equal(True, 1), "a true is not a one")
        self.assertFalse(g.deep_equal(False, 0))
        self.assertTrue(g.deep_equal(True, True))

    def test_lists_dicts_and_text(self):
        self.assertTrue(g.deep_equal([1, [2.0, "x"]], [1.0, [2, "x"]]))
        self.assertFalse(g.deep_equal([1, 2], [1, 2, 3]))
        self.assertFalse(g.deep_equal([1, 2], [2, 1]))
        self.assertTrue(g.deep_equal({"a": 1, "b": [1]}, {"b": [1], "a": 1.0}))
        self.assertFalse(g.deep_equal({"a": 1}, {"b": 1}))
        self.assertFalse(g.deep_equal("1", 1))
        self.assertTrue(g.deep_equal(None, None))
        self.assertFalse(g.deep_equal(None, 0))

    def test_values_are_shown_the_way_the_browser_showed_them(self):
        self.assertEqual(g.show_value([1.0, 2.5, "ب", {"k": 3.0}]), '[1,2.5,"ب",{"k":3}]')


class Outcomes(unittest.TestCase):
    def test_a_perfect_run(self):
        out = g.grade(STDIO, "x", ask=judge_says({"stdout": "A\n"}, {"stdout": "B\r\n"}, {"stdout": "C\n"}))
        self.assertEqual((out["passed"], out["total"], out["blocked"]), (3, 3, False))
        self.assertTrue(all(r["ok"] for r in out["results"]))

    def test_the_first_test_shows_everything_the_others_nothing(self):
        out = g.grade(STDIO, "x", ask=judge_says({"stdout": "x\n"}, {"stdout": "y\n"}, {"stdout": "C\n"}))
        first, second, third = out["results"]
        self.assertEqual((first["expected"], first["actual"], first["stdin"]), ("A\n", "x\n", "a\n"))
        self.assertEqual(set(second), {"index", "ok", "kind"})
        self.assertTrue(third["ok"])
        self.assertEqual(out["passed"], 1)

    def test_a_missing_newline_is_a_failure(self):
        out = g.grade(STDIO, "x", ask=judge_says({"stdout": "A"}, {"stdout": "B\n"}, {"stdout": "C\n"}))
        self.assertFalse(out["results"][0]["ok"])

    def test_errors_and_limits(self):
        out = g.grade(STDIO, "x", ask=judge_says(
            {"status": "error", "error": "Traceback...\nValueError: x\n", "stdout": "partial"},
            {"status": "timeout"}, {"status": "memory"}))
        first, second, third = out["results"]
        self.assertEqual((first["kind"], first["message"], first["actual"]), ("runtime", "Traceback...\nValueError: x\n", "partial"))
        self.assertEqual((second["kind"], second["code"]), ("runner", "timeout"))
        self.assertEqual(third["code"], "memory")
        self.assertEqual(out["passed"], 0)
        self.assertNotIn("actual", dict(out["results"][1]))

    def test_the_hidden_tests_do_not_tell_the_error_input(self):
        out = g.grade(STDIO, "x", ask=judge_says({"stdout": "A\n"}, {"status": "error", "error": "Boom", "stdout": "secret"}, {"stdout": "C\n"}))
        second = out["results"][1]
        self.assertEqual(second["message"], "Boom")
        self.assertNotIn("actual", second)
        self.assertNotIn("stdin", second)

    def test_function_questions(self):
        out = g.grade(FUNC, "x", ask=judge_says({"value": 4}, {"value": 1.0}))
        self.assertEqual(out["passed"], 2)
        out = g.grade(FUNC, "x", ask=judge_says({"value": 5}, {"value": 2}))
        first = out["results"][0]
        self.assertEqual((first["expected"], first["actual"], first["args"]), ("4", "5", [2]))
        self.assertEqual(set(out["results"][1]), {"index", "ok", "kind"})

    def test_what_is_sent_to_the_judge(self):
        seen = {}

        def ask(request):
            seen.update(request)
            return judge_says({"stdout": ""}, {"stdout": ""}, {"stdout": ""})(request)

        g.grade(STDIO, "print(1)", ask=ask)
        self.assertEqual(seen["tests"], [{"stdin": "a\n"}, {"stdin": "b\n"}, {"stdin": "c\n"}])
        self.assertEqual((seen["mode"], seen["source"], seen["problem"]), ("stdio", "print(1)", "q"))
        g.grade(FUNC, "def twice(x): pass", ask=lambda r: (seen.update(r), judge_says({}, {})(r))[1])
        self.assertEqual(seen["tests"], [{"args": [2], "kwargs": {}}, {"args": [0.5], "kwargs": {}}])
        self.assertEqual(seen["functionName"], "twice")

    def test_rules_stop_the_run_before_the_sandbox(self):
        problem = {**STDIO, "constraints": {"forbid": ["for"]}}

        def never(request):
            raise AssertionError("the sandbox must not be used")

        out = g.grade(problem, "for i in []: pass", ask=never)
        self.assertTrue(out["blocked"])
        self.assertEqual(out["passed"], 0)


if __name__ == "__main__":
    unittest.main()
