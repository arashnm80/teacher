# Owner requirements and tasks (checklist)

Every new note, task or prompt from the owner is written here the same day. Open items are worked in priority order, then by how early they were given. An item is checked off only when it is done and verified. Items marked **Owner decision** need an answer from the owner before work continues.

Last updated: 2026-11-16 (Monday).

## Open, in priority order

1. [ ] **Comprehensive tutorial (آموزش) for every question, like the earlier version: descriptive comment lines and several answers each.** (Owner, 2026-11-16.)
   - Done: 37 questions restored from the earlier teacher-playground version. Their statements and tests are unchanged, and the checker accepts every solution. Every defined solution is now shown (no hidden picks).
   - Done since: 24 more questions now have two commented answers each (batches 2 to 4: p03, p04, p09, p47, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, p61, p76, p77, p78, p79, p80, p81, p87, p95, p96). In total 61 of 100 are done.
   - Also done (batch 5): p64, p65, p66, p67, p68, p69, p70, p91. In total 69 of 100 are done.
   - Also done (batch 6): p24, p48, p83, p84, p85, p86, p88, p97. In total 77 of 100 are done.
   - Also done (batch 7): p18, p35, p62, p63, p82, p98, p99, p100. In total 85 of 100 are done.
   - Left: 15 questions (the list is in the commit history; they include the ten whose statement changed since the earlier version). Each needs new commented answers and a fuller explanation, and the checker must accept them.
2. [ ] **Not-cheating protocol: students must not break deadlines, and must not copy or paste answers from the AI assistant or the آموزش; they write the code by hand.** (Owner, 2026-11-16.)
   - Done: copy, cut and drag are blocked on the page, and paste into the editor is blocked (guard.js, loaded by the playground). The آموزش and the assistant open from the first question. Deadlines are decided by the server's clock.
   - Left: check the protection end to end in the browser, and write down its limits for the owner (a determined student can still use developer tools or take a screenshot; the offline copy still contains every solution).
3. [ ] **Owner decision: the text shown for each series on the website.** The series texts are placeholders now.
4. [ ] **Owner decision: the offline zip still contains every solution.** Keep, or remove the solutions from the offline copy?
5. [ ] **Owner check: the AI assistant works in the owner's browser now (keys verified through the relay).** Consider rotating the two keys that were pasted into the chat.
6. [ ] **Owner action: delete the saved browser entry for the test student in Manage Passwords, then confirm the search box shows no suggestions.**
7. [ ] **Owner action: the live test student is still in class 200. Set class 201 or 202 if you want to see that class's view.**
8. [ ] **Lowest priority, do last: the whole website bilingual like the lessons, with Persian as the default.** The lesson site is already Persian by default. Still open: English for the playground and admin text, English content for the questions, and the book sections E1–E5. (Owner, earlier.)

## Done

- [x] Progress is kept when questions are added. It resets only on a major edit or a manual --bump. (Owner, earlier.)
- [x] Online sign-up and sign-in with phone number, national code, Persian full name and password. The teacher resets passwords; no SMS or email. (Owner, earlier.)
- [x] Answers are checked in the browser; the server keeps the results and recomputes passes and deadlines itself. (Owner, earlier.)
- [x] The offline version keeps working as before. (Owner, earlier.)
- [x] The run button reads "بررسی و تست". (Owner, earlier.)
- [x] Submission log: each submission with its code, time and percent of tests passed. A separate view in the teacher panel, with CSV export. (Owner, earlier.)
- [x] Class deadlines: class 201 (Sunday class) has six series, Monday 16 to Saturday 21 Nov, due 22:00 Tehran time; class 202 (Wednesday class) has six series, Thursday 19 to Tuesday 24 Nov, due the night before class. After a deadline the questions stay open for practice without score. (Owner, 2026-11-15 and 2026-11-16.)
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
- [x] Class 202 set to six series as in class 201, Thursday to Tuesday. (Owner, 2026-11-16.) Published on 2026-11-16.

## Working rules from the owner

- Every new note or task goes into this file the same day. Open items are worked in priority order, then by how early they were given. Items are checked off when done.
- Commit the needed files as the work proceeds, so the path is clear. Work is on the branch `online-playground` and is not pushed.
- Do not write personal details (phone numbers, national codes, passwords) or API keys into files in the repository.
