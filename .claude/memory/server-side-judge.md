---
name: server-side-judge
description: "Since 2026-11-17 students' Python runs on the server in a Docker sandbox (teacher-judge), not in their browser; offline copy still runs locally"
metadata:
  type: project
---

Online playground sends only code to `/api/student/attempt`; `accounts-server/grading.py` asks the judge
(`judge-server/judge.py`, systemd `teacher-judge`, Unix socket `/run/teacher-judge/judge.sock`, image
`teacher-judge:current` built by `judge-server/build_image.sh` from the host Python) and compares with the
expected outputs. Hidden tests never reach the browser. The offline zip still uses Pyodide on the device and
its sync still trusts the client's passed count.

**Why:** many students could not load the Pyodide download; also stops forged results.

**How to apply:** after changing `runner.py`/`child.py` run `judge-server/install.sh`; changing `grading.py`
needs `deploy.sh`. Tests: `judge-server/test_judge.py` (41 attacks), `accounts-server/test_accounts.py`,
`test_grading.py`, `e2e_mobile.py` (needs the test servers: scratchpad `restart_judge.sh` then `restart_server.sh`).
A live check with a throwaway student needs a browser User-Agent (Cloudflare blocks urllib) and the rows
(student, progress, attempts, sessions, audit) must be deleted afterwards. See [[kill-test-servers-by-pid]].
