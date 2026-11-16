# Playground expansion: 30 → 50 problems (started 2026-11-15)

## User request (verbatim criteria)
- Increase problems from 30 to 50.
- Every question understandable for students who started Python recently.
- Some questions: multiple different solutions (provide them).
- Answers as simple step-by-step (قدم‌به‌قدم).
- Persian comments on lines/sections of code.
- Persian explanation for each answer (one or a few paragraphs).
- Only use concepts already taught in the book.
- Goal: students get help and understand concepts.
- AFTER this: return to the website-lesson refining work (T8 onward in grade11-rebuild-tasks.md).

## Scope decision: "taught in the book"
Playground = module 1 (units 1–2) + the built-in functions table + modules
`math` (import, math.sqrt, from math import), `random`, `datetime`.
NOT taught in module 1 (do not use): try/except, lambda, enumerate, zip,
dict .items()/.keys()/.values()/.get(), iterating a dict with for, set(),
list(), dict(), tuple(), None / is None, slicing [a:b] / [::-1], negative
indexes, list.reverse(), .sort(), .count(), .index(), .join(), .strip(),
.replace(), isdigit(), +=, -=, //=, %=, print(*lst), & | on sets, f-strings,
math.floor/ceil/pi, conditional expression (x if c else y), `not in`,
tuple unpacking `a, b = t`, json, pathlib, classes.
Allowed: input/int/float/str/print(…, end=) (book text), len, range (with step),
min, max, sum, abs, round, pow, sorted (incl. reverse=), type, bool, split(),
lower(), upper(), append, insert, remove, pop(), clear(), del (lists), `in`,
and/or/not, elif, break, continue, while True + break, def/return, `_` as
unused loop variable, `**`, `//`, `%`.

## Pipeline (source of truth = authoring files, NOT problems.json)
- Sources: `11th-grade/playground-authoring/content_*.py` (one dict per problem).
- Build: `python3 11th-grade/playground-authoring/build.py` → writes
  `playground/app/data/problems.json` (guides generated from `solutions`).
- Check: `build.py` runs `check.py`: every solution passes all tests,
  constraints, banned-token list, Persian comments, Persian explanation.
- Then: rebuild offline zip `11th-grade/extras/teacher-playground-offline.zip`
  (prefix `teacher-playground/`, same file set as playground/), bump
  `playground_zip_href` `?v=` in build_site.py, then
  `python3 build_site.py && bash deploy.sh` (or `.claude/rebuild.sh`).
- Redeploy after each batch (content_a … content_e).

## Status (update as you go)
| batch | problems | status |
|---|---|---|
| a | p01–p10 rewritten (Persian comments, Persian steps + explanations, 2 solutions each) | done, deployed v12 |
| b | p11–p20 rewritten; untaught parts removed (//=, [::-1], print(*), None, set()) | done |
| c | p21–p30 rewritten; p23 signature changed; p29/p30 use math.sqrt + round | done |
| d | NEW p31–p40 | done |
| e | NEW p41–p50 + concepts strings, builtins | done, deployed v13 |
| checks | 50/50 problems: every solution passes all tests + constraints + banned list + Persian comments per section; 47 have 2+ solutions (p21, p28, p41 have one) | done |
| then | return to lesson refining (T8…) | NEXT |

## How to publish the playground (after any edit)
1. Edit `11th-grade/playground-authoring/content_*.py` (NOT problems.json).
2. `cd 11th-grade/playground-authoring && python3 build.py` (checks; must print "wrote 50 problems").
3. `python3 pack.py` → bumps the `?v=` cache version, rebuilds
   `extras/teacher-playground-offline.zip`, runs build_site.py and deploy.sh.
4. Verify: `curl …/playground/data/problems.json?v=N` shows 50 problems.

## Files
- `playground-authoring/base/problems-30.json` — original 30 (never edit; build starts from it).
- `playground-authoring/check.py` — checker (tests, constraints, banned list, Persian comments).
- `playground-authoring/build.py` — merges content, generates guides, checks, writes JSON.
- `playground-authoring/pack.py` — version bump, zip, site build, deploy.
- `playground-authoring/content_a.py … content_e.py` — the content (ITEMS, CONCEPTS).

## Resume notes
- Known untaught items in the ORIGINAL 30 (to fix in batches b/c):
  p15 `//=`; p17 `[::-1]`, `print(*…)`; p18 `print(*…)`; p19 `None`/`is`;
  p20 `set()`; p21 set comprehension and `&`; p22 iterating dict; p23
  `.items()` (signature changes to grade_book(names, scores));
  p29 floor/ceil (rewritten to math.sqrt + round); p30 math.pi (rewritten to
  distance with math.sqrt); p10/p15 `+=`.
