# Owner requirements and tasks (checklist)

Every new note, task or prompt from the owner is written here the same day. Open items are worked in priority order, then by how early they were given. An item is checked off only when it is done and verified. Items marked **Owner decision** need an answer from the owner before work continues.

Last updated: 2026-11-16 (Monday).

## Open, in priority order

0. [x] **HIGH PRIORITY, top of the list: show a countdown of the remaining time for each problem. (Owner, 2026-11-16.)** Shown on the problem itself (ticking) and as a compact remaining time next to each problem in the list. It uses the server's clock, not the computer's, and also works in the offline copy from its last synced schedule. Online: done and published on 2026-11-16 (browser check 7 of 7). Offline: comes with the offline sync work (item 1).
1. [x] **Offline copy = online copy, with sync and self-update. (Owner, 2026-11-16.)** Done and published on 2026-11-16 (29 browser checks, 12 updater checks, 61 server tests, a live update rehearsal and the live smoke test). The offline copy must work like the online version, but with all files downloaded and usable without internet.
   - Same features as online: sign-up and sign-in, progress, series and deadlines, the assistant, the tutorials.
   - Students can sign up and sign in inside the offline copy, and their progress is sent to the teacher whenever there is internet (the same teacher panel and reports).
   - The student must see clearly which problems were solved correctly on their device, and which of those have already reached the teacher (synced).
   - The offline copy knows the latest online version. When the teacher updates the website, the offline copy shows an update notice and can update itself.
   - Deadlines stay decided by the server's clock (a result counts when it reaches the server before the deadline); the student is told this clearly.
   - Notes for the owner: students who already have the old zip must download the new one once; after that updates come from inside (the update notice, through شروع.bat). The offline files no longer contain the tutorials or hidden expected outputs: the tutorials arrive after the first sign-in (with internet) and stay on the device. A result counts for the score when it reaches the server before the deadline.
2. [x] **Lowest priority, do last: the whole website bilingual, Persian by default. (Owner, 2026-11-16: "do that".)** The lesson site is already bilingual. Worked in stages:
   - [x] Stage 1: the playground interface (every button, message, result card, sign-in window with its own language switch, the progress window, the assistant panel, the countdown, the sync marks, the update notice, the series texts with English dates, the tutorials of the 13 topics). Checked with a browser test that no Persian is left in the interface in English (18 checks), plus the earlier suites.
   - [x] Stage 2: English texts for all 100 questions (title, topic, statement, hints) and their tutorials (steps, explanations, mistakes and the code comments; the code itself is checked to be the same as the Persian one). Files: `playground-authoring/en/`. Browser check: no Persian anywhere on a problem page, hint and tutorial in English (23 checks).
   - Note for the owner: in Persian, problem 95 is titled "کف و سقف با math" but asks for the square root, and problem 96 is titled "مساحت دایره" but asks for the distance of two points. The English titles say what is asked ("Square root with math", "Distance between two points"). The Persian titles are unchanged; say if you want them fixed too (a title change does not reset progress).
   - [x] Stage 3 (code and tests done, relay redeploy waits for the deploy step): the assistant answers in English when the page is English (English prompts, English errors; 21 relay tests).
   - [x] Stage 4: the teacher's panel (admin): its own language switch, every text in English and left-to-right (33 browser checks with the panel).
   - [x] Stage 5: the whole book in English: 1307 pieces translated (none left in Persian; four literal Persian examples inside code quotes stay as they are). Checked on pages of modules 3 and 4.

## Done

- [x] **Deadlines (owner, 2026-11-16, final version, both classes): deadlines are by problem number, all at 23:00 Tehran time.** Problems 1 to 10 are due Tuesday 17 Nov; 11 to 20 Wednesday 18 Nov; 21 to 30 Thursday 19 Nov; 31 to 40 Friday 20 Nov; 41 to 50 Saturday 21 Nov; 51 to 60 Sunday 22 Nov; 61 to 70 Monday 23 Nov; 71 to 80 Tuesday 24 Nov. Then 81 to 85 Wednesday 25 Nov; 86 to 90 Thursday 26 Nov; 91 to 95 Friday 27 Nov; 96 to 100 Saturday 28 Nov (the final deadline). All 100 are due before Sunday 29 Nov. Published on 2026-11-16.
   - Problem numbers are the numbers shown on the site, not the internal ids.
   - Earlier plans (Monday to Saturday for class 201, Thursday to Tuesday for class 202, the Thursday and Saturday draft, and 22:00 deadlines) are superseded. Their commits stay in the history.

- [x] **Comprehensive tutorial (آموزش) for every question, like the earlier version: descriptive comment lines and several answers each.** (Owner, 2026-11-16.)
   - Done: 37 questions restored from the earlier teacher-playground version. Their statements and tests are unchanged, and the checker accepts every solution. Every defined solution is now shown (no hidden picks).
   - Done since: 24 more questions now have two commented answers each (batches 2 to 4: p03, p04, p09, p47, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, p61, p76, p77, p78, p79, p80, p81, p87, p95, p96). In total 61 of 100 are done.
   - Also done (batch 5): p64, p65, p66, p67, p68, p69, p70, p91. In total 69 of 100 are done.
   - Also done (batch 6): p24, p48, p83, p84, p85, p86, p88, p97. In total 77 of 100 are done.
   - Also done (batch 7): p18, p35, p62, p63, p82, p98, p99, p100. In total 85 of 100 are done.
   - Also done (batch 8): p15, p16, p17, p38, p40, p73, p74, p75. In total 93 of 100 are done.
   - Also done (batch 9): p19, p21, p23, p28, p41, p42, p50. All 100 questions now have commented answers (two or more each) that the checker accepts.
   - Published on 2026-11-16 (site and accounts service). Still for the owner: read a few tutorials in the browser and say if the wording or the level needs changing.
- [x] **Not-cheating protocol: students must not break deadlines, and must not copy or paste answers from the AI assistant or the آموزش; they write the code by hand.** (Owner, 2026-11-16.)
   - Done: copy, cut and drag are blocked on the page, and paste into the editor is blocked (guard.js, loaded by the playground). The آموزش and the assistant open from the first question. Deadlines are decided by the server's clock.
   - Checked in the browser on 2026-11-16 (6 of 6): copy and cut from the tutorial and the assistant are blocked; paste and drop into the editor are blocked. Deadlines are decided by the server's clock (covered by the server tests).
   - Limits for the owner: a determined student can still read the page with developer tools, take a screenshot, or type from memory of the solutions; the offline copy still contains every solution in its questions file.
- [x] Both classes use the same deadlines. (Owner confirmed, 2026-11-16.)
- [x] The series text on the website is good as it is. (Owner confirmed, 2026-11-16.)
- [x] The AI assistant works in the owner's browser. (Owner confirmed, 2026-11-16.)
- [x] The saved-password problem is fixed. (Owner confirmed, 2026-11-16.)
- [x] Class 200 is gone: the live database has no class-200 student, and sign-up and the panel only allow 201 or 202. (Owner, 2026-11-16.)
- [x] The tutorials are fine so far. (Owner confirmed, 2026-11-16.)
- [x] The Aban dates and the end-to-end browser check are settled (33 of 33 on 2026-11-16).
- [x] Progress is kept when questions are added. It resets only on a major edit or a manual --bump. (Owner, earlier.)
- [x] Online sign-up and sign-in with phone number, national code, Persian full name and password. The teacher resets passwords; no SMS or email. (Owner, earlier.)
- [x] Answers are checked in the browser; the server keeps the results and recomputes passes and deadlines itself. (Owner, earlier.)
- [x] The offline version keeps working as before. (Owner, earlier.)
- [x] The run button reads "بررسی و تست". (Owner, earlier.)
- [x] Submission log: each submission with its code, time and percent of tests passed. A separate view in the teacher panel, with CSV export. (Owner, earlier.)
- [x] Class deadlines: superseded by item 0 (problem-number batches, 23:00). After a deadline the questions stay open for practice without score. (Owner, 2026-11-15 and 2026-11-16.)
- [x] Series per day, in the same pattern for both classes, with Friday included and no day holding 50 questions. Dates are Jalali and Tehran time. The word is "سری", not "بسته". (Owner, 2026-11-16.)
- [x] Sign-up asks for class 201 or 202. (Owner, earlier.)
- [x] Admin password set (given to the owner once).
- [x] Test student created in class 200.
- [x] The teacher can change a student's class in the panel. (Owner, 2026-11-15.)
- [x] The lesson site is Persian by default. (Owner, earlier.)
- [x] Button labels centred in the sign-in dialog and the admin panel. (Owner, earlier.)
- [x] Students' classes collected at sign-up. (Owner, earlier.)
- [x] Questions can be added in the middle or at the end without losing progress. (Owner, earlier.)
- [x] AI assistant available from the first question, once a key is saved. (Owner, 2026-11-16.)
- [x] AI keys accepted again; the earlier "key does not look valid" error fixed. Both keys verified through the relay on 2026-11-16.
- [x] Search box no longer offers saved accounts. (Owner, earlier.)
- [x] The progress window's close button stays visible at the bottom, so nobody has to scroll to it. (Owner, 2026-11-16.)
- [x] Class 202 six series, Thursday to Tuesday (superseded by item 0 on 2026-11-16).

## Working rules from the owner

- Every new note or task goes into this file the same day. Open items are worked in priority order, then by how early they were given. Items are checked off when done.
- Commit the needed files as the work proceeds, so the path is clear. Work is on the branch `online-playground` and is not pushed.
- Do not write personal details (phone numbers, national codes, passwords) or API keys into files in the repository.
