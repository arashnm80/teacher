"""Tests for the revision rules in build.py: progress is kept unless a question has a major edit.

Run with:  python3 test_revisions.py
The build's history file and published file are replaced by temporary copies in each test.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402


def question(pid, **extra):
    base = {
        "id": pid, "mode": "stdio", "title": f"مسئله {pid}", "statement": "متن",
        "tests": [{"stdin": "Ali\n", "stdout": "Hello, Ali\n"}],
        "hints": ["سرنخ"], "guide": "راهنما", "starter": "x = input()",
    }
    base.update(extra)
    return base


class RevisionRulesTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="rev-test-"))
        self._saved = (build.REVISIONS_FILE, build.OUT)
        build.REVISIONS_FILE = self.dir / "revisions.json"
        build.OUT = self.dir / "published.json"

    def tearDown(self):
        build.REVISIONS_FILE, build.OUT = self._saved

    def publish(self, problems):
        """Write the current history and the published file, as a real build does."""
        history, _ = build.reconcile_revisions(copy.deepcopy(problems), [])
        build.REVISIONS_FILE.write_text(json.dumps(history), encoding="utf-8")
        published = copy.deepcopy(problems)
        for p in published.values():
            p.pop("solutions", None)
        build.OUT.write_text(json.dumps(list(published.values())), encoding="utf-8")

    def reconcile(self, problems, bump=()):
        history, notes = build.reconcile_revisions(problems, list(bump))
        build.REVISIONS_FILE.write_text(json.dumps(history), encoding="utf-8")
        return notes

    def test_new_questions_start_at_revision_one(self):
        problems = {"p01": question("p01")}
        notes = self.reconcile(problems)
        self.assertEqual(problems["p01"]["revision"], 1)
        self.assertIn("new question", notes[0])

    def test_wording_hints_guides_and_starter_never_bump(self):
        problems = {"p01": question("p01"), "p02": question("p02")}
        self.publish(problems)
        edited = copy.deepcopy(problems)
        edited["p01"].update({"title": "عنوان دیگر", "statement": "صورت مسئله با کلمات دیگر",
                              "hints": ["سرنخ تازه", "سرنخ دوم"], "guide": "راهنمای نو",
                              "starter": "print('hi')", "difficulty": 4})
        self.reconcile(edited)
        self.assertEqual(edited["p01"]["revision"], 1)
        self.assertEqual(edited["p02"]["revision"], 1)

    def test_changed_tests_are_a_major_edit(self):
        problems = {"p01": question("p01")}
        self.publish(problems)
        edited = copy.deepcopy(problems)
        edited["p01"]["tests"].append({"stdin": "Sara\n", "stdout": "Hello, Sara\n"})
        notes = self.reconcile(edited)
        self.assertEqual(edited["p01"]["revision"], 2)
        self.assertIn("major edit", notes[0])

    def test_changed_mode_function_name_or_constraints_are_major_edits(self):
        base = {"p01": question("p01", mode="function", functionName="square",
                                tests=[{"call": {"args": [2], "expected": 4}}])}
        for change in ({"functionName": "cube"}, {"mode": "stdio"}, {"constraints": {"require": ["for"]}}):
            with self.subTest(change=change):
                if build.REVISIONS_FILE.exists():
                    build.REVISIONS_FILE.unlink()  # each case starts from its own history
                self.publish(base)
                edited = copy.deepcopy(base)
                edited["p01"].update(change)
                self.reconcile(edited)
                self.assertEqual(edited["p01"]["revision"], 2)

    def test_manual_bump_forces_a_new_revision(self):
        problems = {"p01": question("p01")}
        self.publish(problems)
        same = copy.deepcopy(problems)
        self.reconcile(same, bump=["p01"])
        self.assertEqual(same["p01"]["revision"], 2)

    def test_bump_of_an_unknown_question_is_refused(self):
        with self.assertRaises(SystemExit):
            self.reconcile({"p01": question("p01")}, bump=["p99"])

    def test_adding_questions_in_the_middle_or_at_the_end_keeps_the_others(self):
        problems = {"p01": question("p01"), "p02": question("p02"), "p03": question("p03")}
        self.publish(problems)
        grown = {"p01": question("p01"), "p015": question("p015"), "p02": question("p02"),
                 "p03": question("p03"), "p104": question("p104")}
        self.reconcile(grown)
        self.assertEqual({k: v["revision"] for k, v in grown.items()},
                         {"p01": 1, "p015": 1, "p02": 1, "p03": 1, "p104": 1})

    def test_removed_question_keeps_history_and_returns_with_its_revision(self):
        problems = {"p01": question("p01"), "p02": question("p02", tests=[{"stdin": "", "stdout": "a\n"}])}
        self.publish(problems)
        self.reconcile({"p01": question("p01")})
        history = json.loads(build.REVISIONS_FILE.read_text(encoding="utf-8"))
        self.assertIn("p02", history, "history never forgets a question")
        returned = {"p01": question("p01"), "p02": question("p02", tests=[{"stdin": "", "stdout": "a\n"}])}
        self.reconcile(returned)
        self.assertEqual(returned["p02"]["revision"], 1, "the same question comes back with its progress")

    def test_removed_question_returning_with_different_tests_is_a_major_edit(self):
        problems = {"p02": question("p02")}
        self.publish(problems)
        self.reconcile({})
        changed = {"p02": question("p02", tests=[{"stdin": "", "stdout": "other\n"}])}
        self.reconcile(changed)
        self.assertEqual(changed["p02"]["revision"], 2)

    def test_first_run_starts_from_the_published_file(self):
        published = [dict(question("p01"), revision=4), dict(question("p02"), revision=2)]
        build.OUT.write_text(json.dumps(published), encoding="utf-8")
        if build.REVISIONS_FILE.exists():
            build.REVISIONS_FILE.unlink()
        problems = {"p01": question("p01"), "p02": question("p02")}
        self.reconcile(problems)
        self.assertEqual(problems["p01"]["revision"], 4)
        self.assertEqual(problems["p02"]["revision"], 2)

    def test_fingerprint_ignores_fields_outside_the_contract(self):
        a = question("p01")
        b = copy.deepcopy(a)
        b.update({"title": "x", "hints": [], "guide": "y", "difficulty": 5, "number": 99})
        self.assertEqual(build.fingerprint(a), build.fingerprint(b))
        b["tests"][0]["stdout"] = "changed\n"
        self.assertNotEqual(build.fingerprint(a), build.fingerprint(b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
