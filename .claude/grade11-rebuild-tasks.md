# Grade-11 book rebuild — task list and handover

Started 2026-11-14. Goal: fix the PDF → markdown → website pipeline so the
Persian book text and the site are faithful to the printed book.

## Priorities (from the user)

1. Persian version first. English translation comes last.
2. Text-only fixes (RTL/LTR order, bracket direction, punctuation) before
   everything else.
3. Work in layers across the whole book (all images, then all tables, …),
   never page by page.
4. Redeploy after every finished layer, so the live site is always usable:
   `python3 english.py build && python3 build_site.py && bash deploy.sh`
   (run from `11th-grade/`).
5. Before starting, show the task table and let the user pick IDs.

## Done so far

- `11th-grade/convert_book.py` (rewritten) + `11th-grade/bidi.py`: PDF →
  `converted-markdown-book/`. Visual→logical text order, figures cropped as
  whole pictures with captions, real markdown tables, callouts as
  `> **نکته**` blockquotes (nested and multi-page), footnotes, lists,
  paragraphs joined across lines, pictures and page breaks.
- `11th-grade/book_fixes.py`: hand fixes for places where the printed book
  itself is garbled (`FIXES`, `REGEX_FIXES`), and `PAGE_OVERRIDES` for the
  cover, licence, contents, and references pages.
- `11th-grade/build_site.py`: new markdown → HTML rendering (page marks,
  callout boxes, figures, tables, code inside callouts, bidi isolation of
  English runs). Assessment rubric (ارزشیابی) dropped from pages, per
  REQUIREMENTS. `web/style.css`: removed `unicode-bidi: plaintext` (the cause
  of Persian paragraphs shown left-to-right) and added styles for the new
  callout kinds, tables, captions.
- `11th-grade/english.py`: English twin built from a translation memory
  `sections/translations-en.json` keyed by the Persian text. Untranslated
  pieces fall back to Persian. ~1,640 of ~2,800 pieces translated
  (Modules 1–3 up to the start of JavaScript).
- Deployed to https://teacher.arashnm80.ir (last: 2026-11-14).
- Nothing committed to git yet.

## Resume here (read first)

- One command rebuilds from the PDF and deploys, and refuses to deploy if a
  step fails: `bash /root/Storage/teacher/.claude/rebuild.sh` (creates its own
  venv in `.claude/venv` on first run, ~80 s).
- Run it after every finished fix. Then tick the progress log below.
- Current job: the T series (T1–T9), in order. Fixes go into
  `11th-grade/convert_book.py` (general rules) or `11th-grade/book_fixes.py`
  (one-off places where the printed book is garbled).

## Progress log

- 2026-11-15 (playground v27): AI answers render indented ```text blocks inside numbered items as code blocks.
  List items keep their indented lines as blocks (bidi.js mdBlocks/mdList/dedentBlock); a fence left unclosed
  ends before an italic note; answer lists use Persian digits (style.css @counter-style). Tests: Node answer cases
  and the owner's sample in the browser. bidi.js v17, style.css v20.
  The private-book file opened in the IDE was not related and was not used.

- 2026-11-15 (latest, playground v26, site rebuilt and deployed):
  - PLAYGROUND, owner requests since the last note, all live:
    - Tab-out in the code editor: Tab steps past a closing ) ] } ' " next to the cursor (editor.js, tabOut).
    - Colour key: red = باید باشد ولی نیست, green = اضافه‌ی خروجی شما, in function and stdio results and at the top
      of every guide (app.js colourLegendHtml; red no longer struck through).
    - Brackets around English words: an unmatched closing bracket stays outside the LTR island (bidi.js
      latinIslandLength), so «(و بدون for)» and «زبان (Python) است» read correctly. Lessons already did this (build_site.py).
    - Markdown: bold around code (**شرط `if`**) works in AI answers, statements, hints and guides.
  - LESSONS, Poodman 1–2 (owner priority): ALL CHECKS DONE.
    - C1 code blocks: script check, no issues.
    - I1 figures: 278 crops on contact sheets. Removed two glyph-only arrows (p125-03, p132-02); trimmed edge leaks
      (p034-02, p068-02); masked a stray paragraph (p061-02). Converter: IMAGE_CLIPS and IMAGE_MASKS in book_fixes.py.
    - B1 tables (19): all compared with the printed pages. Fixed (printed errors): T01 Print→print, float(5)→5.0;
      T02 < and > meanings were swapped, != >= <= spacing; T13 box labels; T10 tools cell now one left-to-right span
      (brackets were split); T12 group row is a body row under a header. Operators and flex tables verified at 4x.
    - S1 layout: no page-level sideways overflow at 390 px on all 33 Module 1–2 pages; wide tables scroll in .table-wrap.
    - Poodman 3–5: later (owner). English twin (E1–E5): later. Git (H2): not requested.
  - Owner items, not ours: Cloudflare SSL mode (Full strict) and the proxy/DNS choice; stop the stray PM2 daemon only on
    the owner's word. pack.py now keeps the app.js cache key in step with each publish.

- 2026-11-15 (latest, deployed playground v23, site rebuilt):
  - DESIGN PASS done: one header on every page (brand, sections, search, download, EN toggle on book pages only),
    one page-head, one card/button/sidebar style, one footer; «simple yet beautiful» (light header, one teal accent,
    hairline borders). Files: web/shared.css, web/search.js, web/style.css, build_site.py, playground/app (index.html, css).
    Sidebar on screens up to 980 px is an in-flow bar that opens and closes (no overlay).
  - PLAYGROUND PROBLEMS: 100 problems (max). Tiers in playground-authoring/tiers.json (1 خیلی آسان … 5 چالشی).
    Average hardness 2.22 → 1.53 (−31%). 52 very easy, 44 easy, 3 medium, 1 hard. Order: tier, then concept
    (book order), then id. New examples p51–p100 (for: 0–9, 1–10, 20–25, 30→25, 10→1, evens, odds, steps, break,
    continue; while: count up/down, steps, doubling, break, continue; if/elif; functions; lists; strings; built-ins).
    13 old hard problems simplified in place (same ids, progress kept): p15–p19, p21–p23, p35, p38, p40, p42, p50.
    Checks: every solution passes its tests in build.py; two solutions checked in the browser.
  - MARKDOWN: bold that wraps code (**شرط `if`**) now renders in AI answers, statements, hints and guides
    (bidi.js: code spans and escapes become placeholders before emphasis). Two solution titles had raw ** (p30, p98)
    and are fixed in the authoring sources. Node tests: playground md tests; sweep of all statements = 0 leftovers.
  - LESSONS, Poodman 1–2 (owner priority):
    - C1 code blocks: checked by script (indentation, code outside blocks, fences): no issues.
    - I1 figures: all 278 crops reviewed on contact sheets. Fixed: two glyph-only arrow crops removed
      (p125-03, p132-02); edge leaks trimmed (p034-02, p068-02, IMAGE_CLIPS in book_fixes.py); stray Persian
      paragraph masked in p061-02 (IMAGE_MASKS). Rebuilt and deployed.
    - B1 tables (19): checked so far: T07, T08 (ok), T18, T19 (ok). QUEUED FIXES (printed errors, book is wrong):
      * T01 (p1-func-more, printed p75): `Print(` → `print(` in three rows (max, min, sum); float(5) output «50» → «5.0».
      * T02 (p1-if, printed p27): `<` is printed as «بزرگ‌تر از» and `>` as «کوچک‌تر از» (swapped) → swap the
        meanings; `! =` → `!=`, `> =` → `>=`, `< =` → `<=`.
      * T13 (p2-flex, printed p137): box labels garbled («box2box3», «box3box2box1») → «box1 box2 box3»,
        «box3 box2 box1» (the row and row-reverse cells).
      * STILL TO CHECK visually: T04 (p80), T06 (p134), T09 (p96), T10 (p97), T11 (p128), T12 (p130), T14–T17.
    - S1 layout: desktop and phone lesson tops checked; full check of tables/figures/callouts pages still to do.
    - Stale notes fixed later: playground-ai-links.md A2–A8 are done; REQUIREMENTS line 17 describes the old
      overlay sidebar (now a 980 px in-flow bar).
  - Owner items still open, not ours to do: Cloudflare SSL mode (Full strict) and the DNS/proxy choice; stop the stray
    PM2 daemon only on the owner's word; English translation later (E1–E5).

  - AI answer (owner, mid-turn 2026-11-15): rendered as markdown (headings, nested
    lists, tables, quotes, code, bold, italic, safe links) and a «بزرگ‌تر ببین» button
    opens the answer in a large dialog. Deployed, playground v19. Design pass continues.

  - DESIGN PASS (owner, 2026-11-15, in progress): one design system for the whole site.
    One header on every page (brand, sections tabs, search, download, language on the
    textbook pages only); one page-head pattern (kicker, title, lede); one card, button
    and sidebar style; one footer. The playground uses the same header (generated by
    build_site.py), and its progress button moves into the sidebar. Shared file:
    web/shared.css (tokens, fonts, components) and web/search.js (search for every page).

- 2026-11-15 (interrupts, all done and deployed, playground v18):
  - Landing: no module rows; book entry; sidebars only inside sections (lessons,
    playground, materials page with its own contents list).
  - One whole-site zip: `grade11-offline.zip` = lessons + playground (+ AI panel)
    + `شروع.bat` (launcher serves the site root). Separate playground zip removed.
  - AI panel on the left (always visible): 3 fixed actions, OpenRouter/Groq keys,
    loading with progress bar and 95 s timeout, cancel, clear errors. Relay
    (`11th-grade/ai-proxy/`) with real free models per provider, Persian-tested.
  - Real keys tested through the relay and in the browser (Groq answered in Persian).
  - Proxy rule verified (direct egress blocked, WARP only); memory saved.
  - Hints: 2 problem-specific tips per problem (`playground-authoring/hints.json`).
  - Button renamed to «تست و آزمون».
  - Solutions: beginner-friendly versions only (`solution-picks.json`); 10
    problems keep two easy solutions, the rest keep the easiest one.
  - Progress is never deleted on a new problem revision; backup/restore in «پیشرفت من».
  - Comments: «#» on the left, the text to its right with bidi.
  - OPEN for you: teacher.arashnm80.ir is behind Cloudflare now (REQUIREMENTS
    say no Cloudflare; Iranian access). Cloudflare also blocks Python's default
    client (1010), not browsers. Decide before the classroom use.
  - DEFERRED by the user (2026-11-15): evolution-of-trust game zip is missing from
    extras/; the links page still points to it. Not a priority; do not raise it.
  - Chat is not shared with anyone (user, 2026-11-15): key-rotation advice is not needed for sharing.
  - Cloudflare, explained to the user 2026-11-15: DNS resolves to Cloudflare; nginx
    sees Cloudflare edge IPs as visitors (rate limits are shared); 1010 blocks happen
    at Cloudflare and never reach nginx. Decision pending: DNS-only (grey cloud) per
    REQUIREMENTS, or keep proxied with CF-Connecting-IP and a bot-rule exception.

- 2026-11-15 (interrupt, done): LANDING. Home is now «درس‌های پایه یازدهم» with the
  course card (طراح سایت + its 5 module rows); new book entry `site/book/index.html`
  offers lessons (toc), playground (online + offline zip), useful materials (links).
  Built by `home_body()` / `hub_body()` in `build_site.py`; CSS block at end of
  `web/style.css`. Deployed with rebuild.sh. Links checked, no overflow at 390 px.
- 2026-11-15 (interrupt, done): PLAYGROUND RENDERING. Mixed Persian/English now
  correct: Latin runs are LTR islands in prose; Persian in code blocks is RTL
  (`cm-fa`); a Python comment is one RTL island with its «#» at the start.
  Renderer moved to `playground/app/js/bidi.js` (`mdLite`, `inlineMd`, `codeHtml`,
  `isolateLatin`). Checked: 50 problems in Node (no unisolated text), p01 in
  Chromium, live site and offline zip (served locally by شروع.bat's way). Playground v15.

- 2026-11-15: PLAYGROUND expanded 30 → 50 problems (see playground-expansion.md).
  Source is `11th-grade/playground-authoring/`; publish with `python3 pack.py`.
  Deployed v13. Back to lessons now.
- 2026-11-15: T8 done (ZWNJ rules for می/ها; heading double space fixed;
  remaining "space before punctuation" hits were false positives from the check).

- 2026-11-14: rebuild.sh added; site deployed and stable.
- T1 done: 90-sentence sample, word order correct. Added rules: bold closes
  after a bracket; space between a Persian word and a glued English word;
  fixed «import mojvle». Deployed. (Persian edits change some translation
  keys; that is expected, English is redone last.)
- T2 done: rules for «() name» -> «name()», «?(x)» -> «(x)?»; fixed
  «(.O.O.P)» and «personl_». Remaining unbalanced brackets are the book's own
  «الف)» enumerations. Deployed.
- T3 done: rules for Persian comma placement («a ،b» -> «a، b») and leading
  punctuation inside quoted English («"!x"» -> «"x!"»). Deployed.
- T4 done: standalone operators are LTR code spans in the order the book
  shows; 5 places in 01-data-modeling where the printed symbol contradicted
  its sentence corrected in book_fixes.py. Deployed.
- T5 done: file names like workshop7.html now code (CODEISH accepts a digit
  before the dot); fixed «`split()` `append()`» comma. Deployed.
- T6 done: «برنامه py.» fixed; space after a Persian full stop; file and
  function names in figure captions are code. Deployed.
- T7 done: joined the remaining split paragraphs (book_fixes, incl. one
  REGEX_FIX across a page marker); split merged comment labels in the CSS
  media-query table. Fixed a regression: the comma rule had stopped 4 older
  book_fixes from matching. rebuild.sh now prints book_fixes warnings to
  stderr; always check them. Deployed.

## How to run the converter

`convert_book.py` needs `pymupdf` (not installed system-wide). Make a venv:
`python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pymupdf` then
`/tmp/venv/bin/python convert_book.py` from `11th-grade/`. It prints any
`book_fixes` entry that no longer matches. `build_site.py` and `english.py`
run with system `python3` (needs the `markdown` package).

Translation workflow: `python3 english.py pending` writes
`sections/pending-en.json`; translate pieces into a JSON `{key: English}`;
`python3 english.py merge FILE`; then `python3 english.py build`. Changing
the Persian text of a piece changes its key, so finish Persian work first.

## Task table (pick IDs)

| # | Group | Subtask | Est. | Status |
|---|---|---|---|---|
| T1 | Persian text: direction | Spot-check ~150 sentences mixing Persian with English/code for correct word order | 30 min | done |
| T2 | Persian text: brackets | `()` `[]` `{}` `«»` mirrored or unbalanced, book-wide | 20 min | done |
| T3 | Persian text: quotes & punctuation | Misplaced `"` `'` `:` `.` `،` next to English words (e.g. `":your age "`) | 20 min | done |
| T4 | Persian text: operators | `<` `>` `<=` `!=` `==` in sentences, compared with the book page | 20 min | done |
| T5 | Persian text: inline code | Code in sentences styled as code, not reversed or split | 25 min | done |
| T6 | Persian text: Modules 4–5 | Finish scan for book-printed glitches (dunder names and `)(len` done) | 15 min | done |
| T7 | Persian text: split paragraphs | Join the last ~10 split paragraphs; split wrongly merged list items | 20 min | done |
| T8 | Persian text: spelling | ZWNJ, stray spaces, doubled diacritics, Arabic ي/ك | 10 min | done |
| T9 | Site: direction | Check live pages in a browser for RTL/LTR rendering problems | 30 min | done for Modules 1–2 (2 lost spaces fixed); Modules 3–5 glue cases left: console.log, workshop1.html, typeof(), super(), urls.py, <p>, settings.py |
| C1 | Code blocks | Indentation; no code lines left outside a block | 25 min | todo |
| I1 | Images | Spot-check ~60 figure crops for missing parts or stray text | 30 min | todo |
| B1 | Tables | Check all ~40 tables against the book (column order, merged cells) | 25 min | todo |
| S1 | Site: layout | Desktop + phone screenshots; fix layout of callouts/tables/figures | 30 min | todo |
| S2 | Site: search | Search works with the new text | 10 min | done (checked live: input, متغیر, Django, پودمان) |
| H1 | Housekeeping | Delete `repair_markdown.py`; update REQUIREMENTS/README for the new pipeline | 15 min | done (file removed; REQUIREMENTS updated) |
| H2 | Housekeeping | Commit to git | 5 min | todo |
| E1 | English | Translate rest of JavaScript (Module 3, unit 2) | 30 min | todo |
| E2 | English | Translate Module 4 | 40 min | todo |
| E3 | English | Translate Module 5 | 45 min | todo |
| E4 | English | Translate captions, table cells, labels | 20 min | todo |
| E5 | English | Terminology consistency pass | 15 min | todo |

Out of scope for this job: the playground and the Quera exercises sections.

## Latest work: playground and site publish
- AI answers: markdown subset now covers strikethrough, `_emphasis_`, tilde fences, autolinks, task boxes, escaped pipes in tables, `<br>` in cells, entities, images shown as links, LaTeX shown as text, heading underlines, and bullet and number lists kept apart. Renderer `bidi.js` v18. Checked with 39 new cases, a 4000-case safety fuzz, unchanged statement rendering, and 107 real-model answers (2 flagged; both now render).
- Clickable disclosure rows (`style.css` v21): pointer, hover tint, chevron that turns when open.
- Copy protection (asset v23, `web/guard.js`): copy, cut and drag blocked page-wide except form fields; `no-copy` on lesson articles and playground panels; paste and drop blocked in the editor. Live check 18 of 18.
- Open: the 100 solution guides are public in `/playground/data/problems.json`, and the book text is public in `/assets/search-index.js`. Decision pending from the owner.

## Accounts, progress and the teacher's panel (online playground)
- Design and owner guide: `accounts-server/README.md`. Service: `accounts-server/app.py` (stdlib, SQLite, loopback only). Tests: `accounts-server/test_accounts.py` (39), `playground-authoring/test_revisions.py` (11).
- Progress belongs to a question id. The build gives a new revision only for a contract change (tests, mode, function name, constraints) or `--bump`; the server resets only the solved mark and hints of that question. Memory: `progress-follows-question-id`.
- The build's checker used to alter published test inputs (solutions ran on shared dicts). Fixed with deep copies. p23 kept at revision 4 (a one-time decision: the change was a bug fix, not a major edit).
- Guides and solutions are released only after a pass (`/api/student/guide`); the online site does not publish `data/problems.json`; the offline zip keeps it.
- Online playground: sign-in dialog (`js/account.js`), progress and drafts on the server, hidden tests show no expected output, assistant opens after a pass, one session per student.
- Teacher's panel at `/admin/` (`web/admin/`): students, progress with code, reset password, enable/disable, CSV, report of actions.
- Status: end-to-end run passes 33 of 33 (`accounts-server/e2e_online.py`, needs a local server and the offline zip extracted). Installed on the server (`accounts-server/deploy/install.sh`), published (`build_site.py` + `deploy.sh`), live smoke test passes (`accounts-server/deploy/smoke_test.sh`). The admin password is still to be set by the owner (the panel answers 503 until then). Database file is 0600 (`UMask=0077` in the unit).
- Lesson learned on deploy: a local test server on port 8790 silently answered for the live Nginx route; check the listener (`ss -ltnp`) before trusting a smoke test.
- Known gap: the public offline zip `grade11-offline.zip` still contains all solutions (kept by design, "work as it is now"); the owner must decide about it.
- Low priority, last: bilingual website (memory `website-bilingual-later`), not started; about 245 Persian-only UI lines in the playground and panel, plus the content translation (lessons E1–E5 are still open).
- Low priority, last: make the whole website bilingual like the lessons (memory `website-bilingual-later`).
