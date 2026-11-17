---
name: kill-test-servers-by-pid
description: "never pkill -f \"app.py serve\" — it also kills the production teacher-accounts service; stop test servers by PID file"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-16T20:19:05.329Z
---

Stop local test servers only by their PID (e.g. `kill $(cat .../server.pid)`), never with `pkill -f "app.py serve"` or similar patterns.

**Why:** On 2026-11-16 `pkill -f "app.py serve"` also matched the production `/opt/teacher-accounts/app.py serve` (systemd unit `teacher-accounts`), which stopped for ~10 s until I ran `systemctl start teacher-accounts`. Students' sessions survived (stored in DB), but it was live traffic.

**How to apply:** Before killing, list with `ps aux | grep` and check the script path/port; test servers run from `accounts-server/` on port 8800, production runs `/opt/teacher-accounts/app.py` on 8790. After any accidental stop: `systemctl is-active teacher-accounts`. See also [[stay-in-storage-root]].
