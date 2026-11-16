#!/bin/bash
# Installs the accounts service on this machine (run as root from anywhere).
# Creates the service user, the code and data folders, the systemd unit and the nginx rules.
# The admin password is NOT set here: run the command printed at the end yourself.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"           # 11th-grade/
DEPLOY="$ROOT/accounts-server/deploy"
SITE_CONF=/etc/nginx/sites-enabled/teacher.arashnm80.ir

id teacher-accounts >/dev/null 2>&1 || useradd --system --home /var/lib/teacher-accounts --shell /usr/sbin/nologin teacher-accounts

install -d -m 0755 /opt/teacher-accounts /opt/teacher-accounts/data
install -d -m 0750 -o teacher-accounts -g teacher-accounts /var/lib/teacher-accounts
install -m 0644 "$ROOT/accounts-server/app.py" /opt/teacher-accounts/app.py
install -m 0644 "$ROOT/accounts-server/teacher_schedule.py" /opt/teacher-accounts/teacher_schedule.py
install -m 0644 "$ROOT/accounts-server/schedule.json" /opt/teacher-accounts/schedule.json
install -m 0640 -o root -g teacher-accounts "$ROOT/playground/app/data/problems.json" /opt/teacher-accounts/data/problems.json

install -m 0644 "$DEPLOY/teacher-accounts.service" /etc/systemd/system/teacher-accounts.service
install -m 0644 "$DEPLOY/nginx-zones.conf" /etc/nginx/conf.d/teacher-accounts-zones.conf
install -m 0644 "$DEPLOY/nginx-snippet.conf" /etc/nginx/snippets/teacher-accounts.conf

if ! grep -q 'snippets/teacher-accounts.conf' "$SITE_CONF"; then
  sed -i '/include \/etc\/nginx\/snippets\/teacher-ai.conf;/a\    include /etc/nginx/snippets/teacher-accounts.conf;' "$SITE_CONF"
fi

nginx -t
systemctl daemon-reload
systemctl enable teacher-accounts
systemctl restart teacher-accounts
systemctl reload nginx
echo "installed. Now set the admin password once (you will be asked twice):"
echo "  sudo -u teacher-accounts env TA_DB=/var/lib/teacher-accounts/accounts.db python3 /opt/teacher-accounts/app.py set-admin-password"
