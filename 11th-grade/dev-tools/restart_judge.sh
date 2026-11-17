#!/bin/bash
# Start (or restart) a TEST judge on a socket in a work folder. Stops the old one by PID file only.
# Never use pkill -f on "judge.py" or "app.py serve": it would also hit the production services.
# Work folder: TEACHER_TEST_DIR (default /tmp/teacher-test).
set -u
WORK=${TEACHER_TEST_DIR:-/tmp/teacher-test}
HERE=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$WORK/judge"
[ -f "$WORK/judge/judge.pid" ] && kill "$(cat "$WORK/judge/judge.pid")" 2>/dev/null
sleep 1
cd "$HERE/judge-server" || exit 1
TJ_SOCKET="$WORK/judge/judge.sock" TJ_SLOTS=${TJ_SLOTS:-3} nohup python3 judge.py serve > "$WORK/judge/judge.log" 2>&1 &
echo $! > "$WORK/judge/judge.pid"
sleep 1.5
echo "test judge: socket $WORK/judge/judge.sock (pid $(cat "$WORK/judge/judge.pid"))"
