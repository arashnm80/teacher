#!/bin/bash
# Serve a fresh copy of the OFFLINE zip (site/grade11-offline.zip, made by build_site.py) on port 8791,
# the way the e2e_lang / e2e_online / e2e_offline_sync checks expect it. Stops the old one by PID file only.
set -eu
WORK=${TEACHER_TEST_DIR:-/tmp/teacher-test}
HERE=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$WORK/offline"
[ -f "$WORK/offline.pid" ] && kill "$(cat "$WORK/offline.pid")" 2>/dev/null || true
sleep 1
rm -rf "$WORK/offline" && mkdir -p "$WORK/offline"
python3 -c "import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$HERE/site/grade11-offline.zip" "$WORK/offline"
cd "$WORK/offline/grade11-site"
nohup python3 -m http.server 8791 --bind 127.0.0.1 > "$WORK/offline.log" 2>&1 &
echo $! > "$WORK/offline.pid"
sleep 1
echo "offline copy: http://127.0.0.1:8791/playground/index.html (pid $(cat "$WORK/offline.pid"))"
