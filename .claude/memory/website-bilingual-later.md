---
name: website-bilingual-later
description: "The whole website (lessons, playground, admin panel, book, assistant) is bilingual Persian/English since 2026-11-16; how it is built and where English texts live"
metadata:
  node_type: memory
  type: project
  modified: 2026-11-16T20:54:02.913Z
---

Done and deployed on 2026-11-16 (owner: "make the whole website bilingual"). Persian is the default,
the choice is stored in localStorage `grade11-lang-v2` (shared by lessons, playground, admin).

How it is built:
- Static page text: `data-fa`/`data-en` (+ `-placeholder`, `-aria`) attributes. Script texts: `define()` / `t()` in
  `playground/app/js/i18n.js`; the admin panel has its own small `x(fa, en)` in `web/admin/admin.js`.
- Question texts: `playground-authoring/en/chunk-NN.json` (title, statement, hints, solution steps/explanations,
  mistakes, plus a `_comments` map for code comments), topics in `en/topics.json`, topic tutorials in
  `base/concepts-en.json`. `build.py` merges them into problems.json as `en` (public) and `guideEn` (kept back
  with the tutorial, in GUIDE_FIELDS and OFFLINE_GUIDE_FIELDS). A new or changed question needs its English chunk
  entry, or the build reports it as untranslated.
- Book: `english.py` translation memory `sections/translations-en.json` (key = hash of the Persian piece);
  `python3 english.py pending` lists what is untranslated (0 now).
- Class series texts: `en` object per pack in `accounts-server/schedule.json` (title, markdown) + English date from
  `teacher_schedule.english_text`.
- Assistant relay: `lang` in the payload picks English prompts and errors (`ai-proxy/app.py`).
- Test: `accounts-server/e2e_lang.py` (33 checks, needs the test servers; see the restart helper note in
  [[kill-test-servers-by-pid]]).

**Why:** the owner wants the English-speaking audience served too.

**How to apply:** when adding a question, tutorial, schedule pack, UI text or book section, add its English twin in
the same change and re-run `e2e_lang.py`. Known mismatch left for the owner: Persian titles of problems 95 and 96
("کف و سقف با math", "مساحت دایره") do not match what they ask (square root, distance); English titles say what is asked.
