# Accounts, progress and the teacher's panel

The online playground (`teacher.arashnm80.ir/playground/`) asks students to sign up with their
phone number, national code, full Persian name and a password. Their progress is kept on the
server, and the teacher sees it in the panel at `teacher.arashnm80.ir/admin/`.

The offline copy (`grade11-offline.zip`) has no accounts. It keeps working as before, with the
progress in the browser.

## Parts

| Part | Where | What it does |
| --- | --- | --- |
| Accounts service | `accounts-server/app.py` | Students, sessions, progress, guides, the admin API. Python standard library only; SQLite database. |
| Playground (online) | `playground/app/js/account.js`, `app.js` | Sign-in dialog, progress sync, the guide and the assistant from the start. |
| Teacher's panel | `web/admin/` | Login, student list and search, progress and attempts with code, reset password, enable/disable, CSV, report of actions. |
| Questions and revisions | `playground-authoring/build.py`, `revisions.json` | Each question has an id and a revision. Progress belongs to the id. |
| Server setup | `accounts-server/deploy/` | systemd unit, Nginx rules, installer. |

## Install (once, on the server)

```bash
sudo bash accounts-server/deploy/install.sh
sudo -u teacher-accounts env TA_DB=/var/lib/teacher-accounts/accounts.db \
    python3 /opt/teacher-accounts/app.py set-admin-password
```

The second command asks for the admin password twice. It is stored only as a hash. Choose at
least 12 characters. The panel does not work until this is done.

Back up `/var/lib/teacher-accounts/accounts.db` regularly. It holds every student's progress.

## Publishing changes

```bash
python3 build_site.py     # the website, the offline zip and the panel
bash deploy.sh            # publishes them and, when the service exists, updates the questions file
```

`deploy.sh` copies `playground/app/data/problems.json` to the server and restarts the service.
Sessions are stored in the database, so students stay signed in across the restart.

## Questions: adding, editing, and what resets progress

Progress belongs to a question's **id** (`p01`, `p02`, ...), never to its position. So:

* **Adding a question** (in the middle or at the end): give it a new id, add its tier in
  `tiers.json`, run `python3 playground-authoring/build.py`. Every other question keeps its
  progress. Numbers shown to students change, but progress does not.
* **Editing wording, hints, guides, starter code or the difficulty**: nothing resets. The
  build does not count these as changes.
* **Editing what a correct answer must satisfy** (the tests, the mode, the function name or the
  constraints): the build gives the question a new revision automatically. For that question
  only, every student starts again: the solved mark and the hints go, while the attempts, the
  code and the teacher's flags stay.
* **A change the build cannot see** (for example the meaning of the statement changed but the
  tests did not): run `python3 playground-authoring/build.py --bump p12`. This forces a new
  revision for that question.
* **Removing a question**: its history stays in `revisions.json`. Never reuse an id for a
  different question. If a removed id comes back with the same tests, its progress returns.

`python3 playground-authoring/test_revisions.py` checks these rules.

## How students use it

* **Sign up**: phone number (09...), national code (checked with the national check digit),
  full name in Persian with at least two words, and a password of at least 8 characters with a
  letter and a digit.
* **Sign in**: phone and password. Eight wrong passwords in a row lock the account for 15 minutes.
  Sign-in attempts from one address are rate-limited too.
* **Forgot the password**: the student asks the teacher. In the panel the teacher presses
  *reset password*. The next time the student signs in, the dialog asks for the national code and
  a new password. No SMS or email is used.
* **One browser at a time**: signing in on a second browser signs out the first.

## The teacher's panel

Open `teacher.arashnm80.ir/admin/` and sign in with the admin password.

* **Students**: list and search by name, phone or national code. Each row shows how many
  questions are passed, the number of runs and how many runs are flagged.
* **A student**: each question with its state, number of runs, revision and flags, and the last
  code. Then the recent runs, with their code.
* **Reset password**, **disable/enable account**.
* **CSV**: opens in a spreadsheet program.
* **Report of actions**: sign-ins, resets, disables, and the revision resets.

### Flags

* *Text without typing*: text appeared in the editor without being typed. The editor blocks
  pasting, so this should not happen.
* *Code without typing*: a long program appeared without any typed key.
* *Pass very quickly*: a long program passed within a minute of first opening the question.

Flags do not block anything. They are for the teacher to look at.

## What the security measures do

* Passwords are stored as scrypt hashes. Nothing readable is kept in the database.
* Sessions are random tokens, stored as hashes, in cookies that JavaScript cannot read
  (`HttpOnly`, `Secure`, `SameSite=Strict`). One session per student.
* Every write checks the request's origin and its JSON type; cross-site forms are refused.
* Rate limits on sign-up, sign-in, reset, saving code and runs, kept in the database.
* Account lock after eight wrong passwords, for 15 minutes.
* The solved mark is computed by the server from the number of tests. A browser cannot send a
  pass for a question with a different number of tests, or for an old revision.
* Guides and solutions are sent only to a student who has passed that question. The file of
  questions the server holds is not published on the website.
* The panel uses a strict content policy, is not indexed, and shows every value as plain text.
* The service listens only on `127.0.0.1` and accepts connections only from this machine.

## Known limits (be aware)

* **Checking happens in the student's browser**, as you asked. A student who knows how to use
  the browser's developer tools can still change what their browser reports. The server keeps
  the code of every run, so the teacher can compare a suspicious pass with the code, and the
  flags point to the likely cases. Only server-side checking would close this completely.
* The expected outputs of the questions must be in the browser to be checked there. A student
  who looks for them in the developer tools can see them. The hidden tests are not shown on the
  page, and the guides are kept back until a pass.
* The copy blocking on the site is a deterrent, not a lock. Screenshots and developer tools
  still work.
* The offline copy contains everything, as before, by design.


## The offline copy (/api/offline/*)

The offline copy is a page on the student's own computer, so it cannot share the website's cookies. It signs in with a bearer token (`Authorization: Bearer ...`), kept apart from the website's sessions (`sessions.kind`). The routes answer cross-site requests (CORS) and are rate limited like the student routes (nginx, `^~ /api/offline/`).

| Route | What it does |
| --- | --- |
| `POST register`, `login`, `complete-reset` | Same as the website's, but the answer carries `token` and no cookie is set. |
| `POST logout` | Ends the token. |
| `GET me` | The student, progress, class schedule, the current revision of every question, `guidesVersion`, `serverTime`. |
| `POST sync` | Up to 100 results (`problemId`, `revision`, `code`, `passed`, `total`, `blocked`, `typed`, `inserted`, `clientAt`). Each goes through the same attempt code as the website; a bad one is refused alone. Answers like `me`. |
| `GET guides` | Every tutorial, for a signed-in student. The offline copy keeps them on the device. |

The deadline is decided by this server's clock when a result arrives, never by the device's clock; the device's reported time is kept in `attempts.client_at` for the teacher to see.

Updating the offline copy does not use this service: the launcher compares `offline-manifest.json` with the website's (see `playground/app/updater.py`).
