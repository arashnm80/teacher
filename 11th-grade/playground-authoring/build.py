#!/usr/bin/env python3
"""Build playground/app/data/problems.json from the authoring sources.

    python3 build.py            # write problems.json only if every check passes
    python3 build.py --strict   # also fail if any problem still has a legacy guide

Sources: content_*.py, each defining ITEMS = {id: spec} and optional CONCEPTS = [..].
spec overrides fields of a base problem (base/problems-30.json) or defines a new one.
The guide text is generated from spec["solutions"]; nothing else is hand-written.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
import re
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check import check_problem  # noqa: E402

OUT = HERE.parent / "playground" / "app" / "data" / "problems.json"
CONCEPTS_OUT = HERE.parent / "playground" / "app" / "data" / "concepts.json"
TIERS_FILE = HERE / "tiers.json"  # difficulty 1-5 for every problem (see tiers.json notes)
TIER_LABELS = ["", "خیلی آسان", "آسان", "متوسط", "سخت", "چالشی"]
# Order inside one difficulty tier: the concepts in the order a student meets them.
CONCEPT_ORDER = ["print-input", "types-ops", "strings", "if-else", "for-loop", "while-loop",
                 "lists", "sets", "dicts", "tuples", "functions", "builtins", "modules"]
MAX_PROBLEMS = 500  # room for new questions; ids never change, so progress never moves
# Each question's revision and the fingerprint it was published with (see reconcile_revisions).
# Progress belongs to the question id. Never delete an entry from this file.
REVISIONS_FILE = HERE / "revisions.json"
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


# Which solutions to show, in order (see solution-picks.json). The beginner-friendly
# version comes first; a clever shortcut is left out even when it is shorter.
PICKS_FILE = HERE / "solution-picks.json"
SOLUTION_PICKS = json.loads(PICKS_FILE.read_text(encoding="utf-8")) if PICKS_FILE.exists() else {}


def renumber_solutions(solutions: list[dict]) -> list[dict]:
    out = []
    for number, sol in enumerate(solutions, 1):
        sol = dict(sol)
        name = sol.get("name", "")
        if name.startswith("روش"):
            sol["name"] = re.sub(r"^روش\s*[۰-۹0-9]+", "روش " + str(number).translate(FA), name, count=1)
        out.append(sol)
    return out


def make_guide(spec: dict) -> str:
    parts: list[str] = []
    if spec.get("intro"):
        parts.append(spec["intro"])
    for sol in spec["solutions"]:
        parts.append(f"**{sol['name']}**")
        steps = [f"- **قدم {str(i).translate(FA)}:** {s}" for i, s in enumerate(sol["steps"], 1)]
        parts.append("\n".join(steps))
        parts.append("```\n" + sol["code"].rstrip("\n") + "\n```")
        parts.extend(sol["explain"])
    if spec.get("mistakes"):
        parts.append("**اشتباه‌های رایج:**")
        parts.append("\n".join("- " + m for m in spec["mistakes"]))
    parts.extend(spec.get("notes", []))
    return "\n\n".join(parts) + "\n"


def first_sample(problem: dict, mode: str) -> list:
    t = problem["tests"][0]
    if mode == "stdio":
        return [{"stdin": t.get("stdin", ""), "stdout": t["stdout"]}]
    return [{"call": t["call"]}]


# Which book page teaches each concept. Checked against outline.py at build time.
LESSON_FOR_CONCEPT = {
    "print-input": "p1-cast",
    "types-ops": "p1-vars",
    "strings": "p1-vars",
    "if-else": "p1-elif",
    "for-loop": "p1-for",
    "while-loop": "p1-while",
    "lists": "p1-lists",
    "sets": "p1-sets",
    "dicts": "p1-dict",
    "tuples": "p1-tuple",
    "functions": "p1-func",
    "builtins": "p1-func-more",
    "modules": "p1-modules",
}


def attach_lessons(concepts: list[dict]) -> None:
    """Give each concept the book page (id and both titles) that teaches it."""
    import sys as _sys
    _sys.path.insert(0, str(HERE.parent))
    from outline import SECTIONS  # book outline: section ids and titles

    by_id = {s["id"]: s for s in SECTIONS}
    for concept in concepts:
        page = LESSON_FOR_CONCEPT.get(concept["id"])
        if page is None or page not in by_id:
            raise SystemExit(f"concept {concept['id']}: no book page for it (got {page!r})")
        section = by_id[page]
        concept["lesson"] = {"page": page, "fa": section["fa"], "en": section["en"]}


# What a correct answer must satisfy. A change to any of these fields is a major edit: the
# question starts again for every student. Wording, hints, guides, the starter code and the
# difficulty are not part of it, so they can change without resetting anyone's progress.
CONTRACT_FIELDS = ("mode", "functionName", "tests", "constraints")


def fingerprint(problem: dict) -> str:
    contract = {field: problem.get(field) for field in CONTRACT_FIELDS}
    text = json.dumps(contract, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def reconcile_revisions(problems: dict, bump: list[str]) -> tuple[dict, list[str]]:
    """Give each question its revision from the history in revisions.json.

    A new question starts at revision 1. A question whose contract changed, or that the
    teacher names with --bump, moves to the next revision. Every other question keeps its
    revision, so its students keep their progress. Returns the new history and what happened."""
    if REVISIONS_FILE.exists():
        history = json.loads(REVISIONS_FILE.read_text(encoding="utf-8"))
    else:
        history = {}
        if OUT.exists():  # first run: start from what is already published
            for old in json.loads(OUT.read_text(encoding="utf-8")):
                history[old["id"]] = {"revision": int(old.get("revision", 1)), "fingerprint": fingerprint(old)}
    unknown = [pid for pid in bump if pid not in problems]
    if unknown:
        raise SystemExit(f"--bump: no such question: {', '.join(unknown)}")
    notes = []
    for pid, problem in problems.items():
        current = fingerprint(problem)
        entry = history.get(pid)
        if entry is None:
            entry = {"revision": 1, "fingerprint": current}
            notes.append(f"{pid}: new question, revision 1")
        elif entry["fingerprint"] != current or pid in bump:
            reason = "--bump" if pid in bump else "tests, mode or constraints changed"
            entry = {"revision": int(entry["revision"]) + 1, "fingerprint": current}
            notes.append(f"{pid}: major edit ({reason}), revision {entry['revision']}")
        history[pid] = entry
        problem["revision"] = entry["revision"]
    return history, notes


def main() -> int:
    strict = "--strict" in sys.argv
    bump = [sys.argv[i + 1] for i, arg in enumerate(sys.argv[:-1]) if arg == "--bump"]
    base = json.loads((HERE / "base" / "problems-30.json").read_text(encoding="utf-8"))
    problems = {p["id"]: dict(p) for p in base}
    base_ids = set(problems)
    concepts = json.loads((HERE / "base" / "concepts.json").read_text(encoding="utf-8"))
    concept_ids = {c["id"] for c in concepts}

    for mod_name in sorted(m.stem for m in HERE.glob("content_*.py")):
        mod = importlib.import_module(mod_name)
        for c in getattr(mod, "CONCEPTS", []):
            if c["id"] not in concept_ids:
                concepts.append(c)
                concept_ids.add(c["id"])
        for pid, spec in mod.ITEMS.items():
            spec = copy.deepcopy(dict(spec))  # the checker runs solutions on the tests: never share them
            if pid in SOLUTION_PICKS and "solutions" in spec:
                spec["solutions"] = renumber_solutions([spec["solutions"][i] for i in SOLUTION_PICKS[pid]])
            if pid in problems:
                old = problems[pid]
                problems[pid] = {**old, **{k: v for k, v in spec.items() if k != "solutions"}}
            else:
                problems[pid] = {"id": pid, "revision": 1, **spec}
            if "solutions" in spec:
                problems[pid]["solutions"] = spec["solutions"]
                problems[pid]["guide"] = make_guide(spec)
                problems[pid]["guideTitle"] = spec["guideTitle"]
                if "samples" not in spec and ("tests" in spec or pid not in base_ids):
                    problems[pid]["samples"] = first_sample(problems[pid], problems[pid]["mode"])

    history, revision_notes = reconcile_revisions(problems, bump)
    tiers = json.loads(TIERS_FILE.read_text(encoding="utf-8"))
    if set(tiers) != set(problems):
        raise SystemExit(f"tiers.json must list exactly the problems: missing {sorted(set(problems) - set(tiers))}, extra {sorted(set(tiers) - set(problems))}")
    if len(problems) > MAX_PROBLEMS:
        raise SystemExit(f"{len(problems)} problems; the maximum is {MAX_PROBLEMS}")
    for pid, tier in tiers.items():
        if int(tier) not in range(1, 6):
            raise SystemExit(f"tiers.json: {pid} must be a tier from 1 to 5")
        problems[pid]["difficulty"] = int(tier)
    # "no constraints" is an absent key, as in the older problems (the runner reads it as {}).
    for p in problems.values():
        if p.get("constraints") is None:
            p.pop("constraints", None)
    def sort_key(pid):
        p = problems[pid]
        concept = CONCEPT_ORDER.index(p["conceptId"]) if p["conceptId"] in CONCEPT_ORDER else len(CONCEPT_ORDER)
        return (p["difficulty"], concept, int(pid[1:]))
    for number, pid in enumerate(sorted(problems, key=sort_key), 1):
        problems[pid]["number"] = number
    tier_counts = {t: sum(1 for p in problems.values() if p["difficulty"] == t) for t in range(1, 6)}
    average = sum(p["difficulty"] for p in problems.values()) / len(problems)
    print("tiers:", {TIER_LABELS[t]: n for t, n in tier_counts.items() if n}, f"average {average:.2f}")
    errors = {}
    legacy = []
    for pid, p in sorted(problems.items(), key=lambda kv: kv[1]["number"]):
        if "solutions" not in p:
            legacy.append(pid)
            continue
        errs = check_problem(copy.deepcopy(p))  # checking must not change the published data
        if errs:
            errors[pid] = errs
    for pid, errs in errors.items():
        print(f"FAIL {pid}")
        for e in errs:
            print("   -", e)
    if strict and legacy:
        errors.update({pid: ["هنوز راهنمای قدیمی است"] for pid in legacy})
        print("legacy guides:", legacy)
    if errors:
        print(f"{len(errors)} problem(s) failed; problems.json NOT written.")
        return 1

    hints_file = HERE / "hints.json"
    if hints_file.exists():
        overrides = json.loads(hints_file.read_text(encoding="utf-8"))
        for pid, tips in overrides.items():
            if pid not in problems:
                raise SystemExit(f"hints.json: unknown problem {pid}")
            if not (1 <= len(tips) <= 3) or any(not t.strip() or "```" in t for t in tips):
                raise SystemExit(f"hints.json: {pid} needs 1-3 plain tips without code fences")
            problems[pid]["hints"] = [t.strip() for t in tips]
    attach_lessons(concepts)
    english = json.loads((HERE / "base" / "concepts-en.json").read_text(encoding="utf-8"))
    for concept in concepts:
        if concept["id"] in english:
            concept["en"] = english[concept["id"]]
    ordered = [problems[k] for k in sorted(problems, key=lambda k: problems[k]["number"])]
    OUT.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CONCEPTS_OUT.write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REVISIONS_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for note in revision_notes:
        print("revision:", note)
    print(f"wrote {len(ordered)} problems, {len(concepts)} concepts; legacy guides left: {legacy or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
