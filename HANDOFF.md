# Handoff: where the project stands (written 2026-11-17)

For picking the work up on another machine, or in a new Claude Code session. Read this first, then
`.claude/requirements-checklist.md` (every owner request and its state) and `.claude/memory/` (the rules and
facts the assistant carried between sessions). This repo is **public**: never put phone numbers, national
codes, passwords, API keys or the server's real address in it.

Branch: `online-playground` (43 commits ahead of `main`, nothing merged yet). Everything below is committed on it.

The assistant's own memory notes are copied in `.claude/memory/` (read them; on a new machine they can be copied into
`~/.claude/projects/<project path>/memory/` so Claude Code loads them again).

## What the project is

Teaching material for a grade-11 class («طراح سایت», networking and software). One repo, mostly under `11th-grade/`:

| Part | Folder | What it is |
| --- | --- | --- |
| The book site | `converted-markdown-book/`, `sections/`, `outline.py`, `build_site.py`, `web/` | Persian textbook plus a full English version, built into `site/`. |
| Python playground (100 problems) | `playground/app/` (front end), `playground-authoring/` (problems, tutorials, English texts, build) | Online at `/playground/`, also inside the offline zip. |
| Accounts service | `accounts-server/` | Students, sessions, progress, deadlines (series), the teacher's panel API, grading. Python standard library + SQLite. |
| Teacher's panel | `web/admin/` | `/admin/`: students, progress, attempts with code, resets, CSV. |
| Judge (sandbox) | `judge-server/` | Runs students' code in a Docker container, one process per test. |
| AI assistant relay | `ai-proxy/` | Students bring their own OpenRouter/Groq key; the relay forwards through WARP only. |
| Server guard | `server/` | Cloudflare-only ports 80/443, and the nginx site file (`nginx-site-teacher.arashnm80.ir.conf`). |
| Test helpers | `dev-tools/` | Start test judge / test server / offline copy; cache check. |

Live: https://teacher.arashnm80.ir (behind Cloudflare, served by nginx from `/var/www/teacher.arashnm80.ir`).
Three systemd services on the Helsinki server: `teacher-accounts` (port 8790), `teacher-ai` (8787), `teacher-judge`
(Unix socket `/run/teacher-judge/judge.sock`). Database: `/var/lib/teacher-accounts/accounts.db` (back it up; it holds
every student's progress).

## State at the end of this session (2026-11-17)

Everything the owner asked for is done, deployed and checked; the checklist has no open items. The requests of this
last stretch, in order:

1. **Copy-the-error button** (the box was not clickable because `guard.js` blocks copying outside form fields):
   a real button with clipboard + select fallback.
2. **Python checking moved to the server** (many students could not download the Pyodide engine). The browser sends
   only the code to `POST /api/student/attempt`; `accounts-server/grading.py` asks the judge over the Unix socket and
   compares with the expected outputs itself. The judge never sees expected outputs. Hidden tests (all but the first
   test of each problem) never leave the server; public `problems.json` has `tests: [{}, ...]`. The online page does
   not load Pyodide any more. The **offline zip still runs Python on the device** (must work without internet) and its
   sync still trusts the passed count the device reports (re-checking on the server would be separate work).
3. **Sandbox**: one Docker container per run (image `teacher-judge:current`, built from the host's Python 3.12 by
   `judge-server/build_image.sh`): no network, read-only root, no capabilities except the few the runner needs to drop
   privileges, `no-new-privileges`. Limits (owner asked for small memory, many parallel checks, 2026-11-17):
   96 MB address space per program, container 128 MB, 32 processes, half a CPU, per test 3 s CPU / 2 s wall, total
   budget 10 s, output 64 KB, file size 2 MB, container hard-killed at 20 s. Judge slots 8 at once, 60 waiting
   (`TJ_SLOTS`, `TJ_QUEUE` in `teacher-judge.service`). Per student one run at a time; rate limit 40 runs / 5 min.
   Errors the browser understands: `judge_busy`, `judge_down` (503), `run_in_progress` (429).
4. **Phone and computer**: coding-key bar under the editor on touch screens, no autocorrect, 44 px targets,
   scrolling to the chosen question and results, no sideways scroll. Not testable here: the real Android keyboard
   (Gboard suggestions).
5. **No forced reload (Ctrl+Shift+R)**: Cloudflare overrides browser caching of js/css to 4 hours whatever nginx
   sends, so the only fix is a changing address. `build_site.py: stamp_versions()` writes one content-based build id
   into every js/css/json/mjs address; never bump `?v=` by hand. nginx also revalidates `/assets/*.js|css`. A tab that
   is already open stays old until reloaded; the offline copy updates through its own notice.

Earlier in the project (all in the checklist and in git history): accounts and the teacher's panel, series and
deadlines (by problem number, all 23:00 Tehran time, last deadline Saturday 28 Nov), countdown per problem, tutorials
for all 100 problems, anti-copy measures (see below), offline copy with sign-in and sync, the whole site bilingual
(Persian default), AI relay.

## Rules from the owner (also in `.claude/memory/`)

- Every new owner note goes into `.claude/requirements-checklist.md` the same day; work by priority; check off only
  when done and verified; mention the checklist status in the final message.
- Commit as work proceeds on `online-playground`. Pushing was forbidden until 2026-11-17, when the owner asked for a
  push so they can continue from another machine.
- Students must type code by hand. Copy/cut/drag are blocked in the page and paste into the editor is blocked, but
  **never claim the solutions are fully protected**: the book text is public in `search-index.js`, and the offline zip
  contains all 100 solutions.
- Progress belongs to a question's id (p01…); only a change of the problem's contract (mode, function name, tests,
  constraints) or `playground-authoring/build.py --bump ID` starts it again. Never delete from `revisions.json`.
- All calls from this server to AI providers go through the WARP proxy (never expose the real IP).
- Stop local test servers by PID file only; `pkill -f "app.py serve"` also kills the production accounts service.
- On large jobs: a task list with time estimates, one layer across the whole book at a time.
- A new question, tutorial, schedule pack, UI text or book section needs its English twin in the same change; run
  `accounts-server/e2e_lang.py` afterwards.
- No personal data in the repo; the owner's real details are only in the live database.

## How to build, test and deploy

Needs Python 3.12, `pip install markdown`, and for browser checks `pip install playwright && playwright install chromium`.
The repo's `.claude/venv/` is ignored; make your own.

```bash
cd 11th-grade
python3 build_site.py          # site/, offline zip, offline-manifest.json, build-id stamps
bash deploy.sh                 # rsync to /var/www/..., updates and restarts the accounts service (server only)
```

After changing `judge-server/runner.py` or `child.py`: `sudo bash judge-server/install.sh`. After changing the
image recipe: `judge-server/build_image.sh`. After `accounts-server/deploy/*`: `sudo bash accounts-server/deploy/install.sh`.
Live check: `bash accounts-server/deploy/smoke_test.sh` (checks the judge and runs a program in the sandbox).

Tests (all passed at the end of this session):

```bash
python3 judge-server/test_judge.py            # 41 attack tests, needs docker + the image, ~40 s
python3 accounts-server/test_accounts.py      # 70
python3 accounts-server/test_grading.py       # 17
python3 playground-authoring/test_revisions.py ; python3 playground-authoring/test_updater.py   # 11 and 12
# browser checks need the test servers:
bash dev-tools/restart_judge.sh && bash dev-tools/restart_server.sh && bash dev-tools/restart_offline.sh
python3 accounts-server/e2e_online.py   # 33     python3 accounts-server/e2e_lang.py        # 33
python3 accounts-server/e2e_countdown.py # 7     python3 accounts-server/e2e_mobile.py      # 65
python3 accounts-server/e2e_offline_sync.py      # 29
python3 dev-tools/cache_check.py                 # a plain second visit gets the new script
```

The test server uses port 8800, the test judge a socket under `$TEACHER_TEST_DIR` (default `/tmp/teacher-test`), the
offline copy port 8791. Stop them with the `.pid` files in that folder. The helper scripts only work on a machine
that has Docker; the test judge also needs the image (`judge-server/build_image.sh`).

## Live-server facts not in git

- nginx: `server/nginx-site-teacher.arashnm80.ir.conf` (copy of `/etc/nginx/sites-enabled/teacher.arashnm80.ir`;
  certificate files stay on the server), snippets in `accounts-server/deploy/nginx-snippet.conf` and
  `ai-proxy/nginx-teacher-ai.conf`. `/api/student/` has `proxy_read_timeout 60s` because a check can take about 10 s.
- The admin password is stored only as a hash in the database (`set-admin-password` command); the owner has it.
- Live check with a throwaway student needs a browser User-Agent (Cloudflare blocks urllib's), and the student's rows
  (student, progress, attempts, sessions, audit) must be deleted afterwards.
- Docker shares the host kernel: keep the host updated. The service user `teacher-judge` is in the `docker` group,
  which is root-equivalent; that is why the socket (0660, group `teacher-accounts`) is the only way in.

## Things for the owner to decide or know

- Persian titles of problems 95 and 96 do not match what they ask (square root; distance of two points); English
  titles do. Changing a title does not reset progress.
- Students holding the old offline zip must download the new one once; after that updates come from inside.
- Offline sync trusts what the device reports. If the owner wants strict scores, offline results would have to be
  re-run on the server (the code is stored with each attempt).
- `11th-grade/REQUIREMENTS.md` (older file) mentions the server's real address (English item 11, Persian item 9); the repo is public,
  so the owner may want that line removed (and the address is in git history).
- Not yet merged: `online-playground` into `main`. Merge when the owner is happy; the live site already runs this code.
- The book/lesson site, the playground and the offline copy share one build; always `build_site.py` then `deploy.sh`.
