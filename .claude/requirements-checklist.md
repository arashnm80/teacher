# Owner requirements and tasks (checklist)

Every new note, task or prompt from the owner is written here the same day. Open items are worked in priority order, then by how early they were given. An item is checked off only when it is done and verified. Items marked **Owner decision** need an answer from the owner before work continues.

Last updated: 2026-11-16 (Monday).

## Open, in priority order

0. [x] **Deadlines (owner, 2026-11-16, final version, both classes): deadlines are by problem number, all at 23:00 Tehran time.** Problems 1 to 10 are due Tuesday 17 Nov; 11 to 20 Wednesday 18 Nov; 21 to 30 Thursday 19 Nov; 31 to 40 Friday 20 Nov; 41 to 50 Saturday 21 Nov; 51 to 60 Sunday 22 Nov; 61 to 70 Monday 23 Nov; 71 to 80 Tuesday 24 Nov. Then 81 to 85 Wednesday 25 Nov; 86 to 90 Thursday 26 Nov; 91 to 95 Friday 27 Nov; 96 to 100 Saturday 28 Nov (the final deadline). All 100 are due before Sunday 29 Nov. Published on 2026-11-16.
   - Problem numbers are the numbers shown on the site, not the internal ids.
   - Earlier plans (Monday to Saturday for class 201, Thursday to Tuesday for class 202, the Thursday and Saturday draft, and 22:00 deadlines) are superseded. Their commits stay in the history.

1. [x] **Comprehensive tutorial (آموزش) for every question, like the earlier version: descriptive comment lines and several answers each.** (Owner, 2026-11-16.)
   - Done: 37 questions restored from the earlier teacher-playground version. Their statements and tests are unchanged, and the checker accepts every solution. Every defined solution is now shown (no hidden picks).
   - Done since: 24 more questions now have two commented answers each (batches 2 to 4: p03, p04, p09, p47, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, p61, p76, p77, p78, p79, p80, p81, p87, p95, p96). In total 61 of 100 are done.
   - Also done (batch 5): p64, p65, p66, p67, p68, p69, p70, p91. In total 69 of 100 are done.
   - Also done (batch 6): p24, p48, p83, p84, p85, p86, p88, p97. In total 77 of 100 are done.
   - Also done (batch 7): p18, p35, p62, p63, p82, p98, p99, p100. In total 85 of 100 are done.
   - Also done (batch 8): p15, p16, p17, p38, p40, p73, p74, p75. In total 93 of 100 are done.
   - Also done (batch 9): p19, p21, p23, p28, p41, p42, p50. All 100 questions now have commented answers (two or more each) that the checker accepts.
   - Published on 2026-11-16 (site and accounts service). Still for the owner: read a few tutorials in the browser and say if the wording or the level needs changing.
2. [x] **Not-cheating protocol: students must not break deadlines, and must not copy or paste answers from the AI assistant or the آموزش; they write the code by hand.** (Owner, 2026-11-16.)
   - Done: copy, cut and drag are blocked on the page, and paste into the editor is blocked (guard.js, loaded by the playground). The آموزش and the assistant open from the first question. Deadlines are decided by the server's clock.
   - Checked in the browser on 2026-11-16 (6 of 6): copy and cut from the tutorial and the assistant are blocked; paste and drop into the editor are blocked. Deadlines are decided by the server's clock (covered by the server tests).
   - Limits for the owner: a determined student can still read the page with developer tools, take a screenshot, or type from memory of the solutions; the offline copy still contains every solution in its questions file.
3. [ ] **Owner decision: the text shown for each series on the website.** The series texts are placeholders now.
4. [ ] **Owner decision: the offline zip still contains every solution.** Keep, or remove the solutions from the offline copy?
5. [ ] **Owner check: the AI assistant works in the owner's browser now (keys verified through the relay).** Consider rotating the two keys that were pasted into the chat.
6. [ ] **Owner action: delete the saved browser entry for the test student in Manage Passwords, then confirm the search box shows no suggestions.**
7. [ ] **Owner action: the live test student is still in class 200. Set class 201 or 202 if you want to see that class's view.**
8. [ ] **Lowest priority, do last: the whole website bilingual like the lessons, with Persian as the default.** The lesson site is already Persian by default. Still open: English for the playground and admin text, English content for the questions, and the book sections E1–E5. (Owner, earlier.)

9. [ ] **Owner check: the Aban dates in your message are one day behind the calendar.** You wrote Tuesday 25 Aban and Wednesday 26 Aban. Tuesday 17 Nov is 26 Aban and Wednesday 18 Nov is 27 Aban. The Azar dates you wrote match. The site uses the weekdays, so Tuesday 17 Nov shows as 26 Aban. Confirm, or tell me which day you meant.
10. [ ] **Owner check: both classes use the same deadlines.** This follows your earlier instruction "for both classes". Confirm, or give class 202 a different schedule.
11. [x] **My follow-up: run the browser end-to-end checks again.** Run on 2026-11-16 after the tutorial batches and the new deadlines: 33 of 33 passed.

## Done

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
