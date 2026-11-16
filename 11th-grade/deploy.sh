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
# SKIP_OFFLINE=1 publishes the site without the offline zip and its update files, for the time
# when the new offline copy is not ready; whatever is already live stays.
EXCLUDES=()
if [[ "${SKIP_OFFLINE:-}" == "1" ]]; then
  EXCLUDES=(--exclude grade11-offline.zip --exclude offline-manifest.json --exclude 'offline-files/')
fi
rsync -a --delete "${EXCLUDES[@]}" site/ /var/www/teacher.arashnm80.ir/
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
