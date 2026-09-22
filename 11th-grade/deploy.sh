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
echo "published https://teacher.arashnm80.ir"
