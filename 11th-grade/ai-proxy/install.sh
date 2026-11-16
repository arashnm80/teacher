#!/usr/bin/env bash
# Install or update the AI relay on this server. Run as root; safe to run again.
# It does not touch nginx. The one-time nginx include is described in README.md.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
APP=/opt/teacher-ai

if ! id -u teacher-ai >/dev/null 2>&1; then
  useradd --system --home-dir "$APP" --shell /usr/sbin/nologin teacher-ai
fi
install -d -m 0755 "$APP"
if [ ! -x "$APP/venv/bin/python" ]; then
  python3 -m venv "$APP/venv"
fi
"$APP/venv/bin/pip" install --quiet "httpx>=0.27" "socksio>=1.0"
install -m 0644 "$SRC/app.py" "$APP/app.py"
install -m 0644 "$SRC/config.json" "$APP/config.json"
install -m 0644 "$SRC/teacher-ai.service" /etc/systemd/system/teacher-ai.service
systemctl daemon-reload
systemctl enable teacher-ai >/dev/null
systemctl restart teacher-ai
sleep 2
systemctl --no-pager --lines=3 status teacher-ai || true
