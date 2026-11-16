#!/bin/bash
# Smoke test of the live site after publishing (read-only: it creates no accounts).
# Usage: bash accounts-server/deploy/smoke_test.sh [base-url]
set -uo pipefail
BASE="${1:-https://teacher.arashnm80.ir}"
fail=0

check() {  # check <description> <expected> <actual>
  if [[ "$2" == "$3" ]]; then
    echo "ok   $1"
  else
    echo "FAIL $1 (expected: $2, got: $3)"
    fail=1
  fi
}

code() { curl -s -o /dev/null -w "%{http_code}" "$@"; }

check "student area needs a sign-in"        401 "$(code "$BASE/api/student/me")"
check "questions need a sign-in"            401 "$(code "$BASE/api/student/problems")"
check "progress needs a sign-in"            401 "$(code "$BASE/api/student/progress")"
check "guides need a sign-in"               401 "$(code "$BASE/api/student/guide?problemId=p01")"
check "panel needs the admin password"      401 "$(code "$BASE/api/admin/session")"
check "students list needs the admin"       401 "$(code "$BASE/api/admin/students")"
check "questions file is not public"        404 "$(code "$BASE/playground/data/problems.json")"
check "playground page is served"           200 "$(code "$BASE/playground/index.html")"
check "panel page is served"                200 "$(code "$BASE/admin/index.html")"
check "offline zip is served"               200 "$(code "$BASE/grade11-offline.zip")"

page=$(curl -s "$BASE/playground/index.html")
if grep -q 'name="pg-mode" content="online"' <<<"$page"; then
  echo "ok   playground is the online build"
else
  echo "FAIL playground is not the online build"; fail=1
fi
if grep -q 'بررسی و تست' <<<"$page"; then
  echo "ok   run button has the new label"
else
  echo "FAIL run button label"; fail=1
fi

headers=$(curl -s -D - -o /dev/null "$BASE/admin/index.html")
if grep -qi '^content-security-policy:.*script-src .self' <<<"$headers"; then
  echo "ok   panel sends its content policy"
else
  echo "FAIL panel content policy header missing"; fail=1
fi
if grep -qi '^x-robots-tag: *noindex' <<<"$headers"; then
  echo "ok   panel is not indexed"
else
  echo "FAIL panel indexing header missing"; fail=1
fi

offline=$(curl -s "$BASE/grade11-offline.zip" -o /tmp/ta-smoke-offline.zip && python3 -c "
import zipfile, sys
z = zipfile.ZipFile('/tmp/ta-smoke-offline.zip')
names = z.namelist()
page = z.read('grade11-site/playground/index.html').decode('utf-8')
ok = 'grade11-site/playground/data/problems.json' in names and 'content=\"offline\"' in page and not any('/admin/' in n for n in names)
print('yes' if ok else 'no')
" 2>/dev/null)
rm -f /tmp/ta-smoke-offline.zip
check "offline zip has the questions, the offline mode and no panel" yes "${offline:-no}"

if [[ $fail -eq 0 ]]; then echo "all live checks passed"; else echo "some live checks failed"; fi
exit $fail
