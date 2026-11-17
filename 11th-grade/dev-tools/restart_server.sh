#!/bin/bash
# Start (or restart) the TEST accounts server on port 8800 with a FRESH database.
# Needs restart_judge.sh to have run first. Stops the old one by PID file only (never pkill -f).
# Admin password of the test database: admin-e2e-pass-123 (the one the e2e_*.py files use).
set -u
WORK=${TEACHER_TEST_DIR:-/tmp/teacher-test}
HERE=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$WORK/server"
[ -f "$WORK/server/server.pid" ] && kill "$(cat "$WORK/server/server.pid")" 2>/dev/null
sleep 1
rm -f "$WORK"/server/accounts.db*
cd "$HERE/accounts-server" || exit 1
export TA_JUDGE_SOCKET="$WORK/judge/judge.sock" TA_COOKIE_SECURE=0 TA_PORT=8800 TA_HOST=127.0.0.1
export TA_SCHEDULE="$PWD/schedule.json" TA_ORIGIN=http://127.0.0.1:8800
export TA_STATIC="$HERE/site" TA_PROBLEMS="$HERE/playground/app/data/problems.json" TA_DB="$WORK/server/accounts.db"
nohup python3 app.py serve > "$WORK/server/server.log" 2>&1 &
echo $! > "$WORK/server/server.pid"
sleep 2
python3 -c "import app; app.store_admin_password('admin-e2e-pass-123')"
echo "test server: http://127.0.0.1:8800 (pid $(cat "$WORK/server/server.pid"))"
