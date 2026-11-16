#!/bin/bash
# Rebuild everything from the PDF and publish. Stops (and does NOT deploy)
# if any step fails, so the live site stays on the last good version.
# Usage: bash /root/Storage/teacher/.claude/rebuild.sh
set -euo pipefail
cd /root/Storage/teacher/11th-grade
VENV=/root/Storage/teacher/.claude/venv
if [[ ! -x $VENV/bin/python ]]; then
  python3 -m venv "$VENV" && "$VENV/bin/pip" install -q pymupdf
fi
"$VENV/bin/python" convert_book.py > /tmp/convert.log
grep "book_fixes" /tmp/convert.log >&2 || true
grep -q . converted-markdown-book/01-poodman-1-python/01-data-modeling.md
python3 english.py build | tail -1
python3 build_site.py | tail -1
test -f site/index.html && test -f site/book/p1-python.html
bash deploy.sh
