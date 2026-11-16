#!/bin/bash
# Publish site/ to https://teacher.arashnm80.ir
# Nginx serves /var/www/teacher.arashnm80.ir because it cannot read /root.
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f site/index.html ]]; then
  echo "site/index.html is missing. Run: python3 build_site.py" >&2
  exit 1
fi
mkdir -p /var/www/teacher.arashnm80.ir
rsync -a --delete site/ /var/www/teacher.arashnm80.ir/
# The accounts service keeps the questions file (with the solutions) for the server, and
# releases each solution only to a student who has passed the question.
if systemctl cat teacher-accounts.service >/dev/null 2>&1; then
  install -m 0640 -o root -g teacher-accounts playground/app/data/problems.json /opt/teacher-accounts/data/problems.json
  install -m 0644 accounts-server/teacher_schedule.py /opt/teacher-accounts/teacher_schedule.py
  install -m 0644 accounts-server/schedule.json /opt/teacher-accounts/schedule.json
  install -m 0644 accounts-server/app.py /opt/teacher-accounts/app.py
  systemctl restart teacher-accounts
  echo "accounts service updated with the current questions"
fi
echo "published https://teacher.arashnm80.ir"
