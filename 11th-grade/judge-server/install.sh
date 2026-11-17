#!/bin/bash
# Installs the judge on this machine (run as root): the service user, the sandbox image, the
# systemd unit. Run it BEFORE publishing the accounts service that uses it.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

getent group teacher-accounts >/dev/null || groupadd --system teacher-accounts
id teacher-judge >/dev/null 2>&1 || useradd --system --home /var/lib/teacher-judge --shell /usr/sbin/nologin \
  -g teacher-accounts -G docker teacher-judge
install -d -m 0755 /opt/teacher-judge
install -m 0644 "$HERE/judge.py" /opt/teacher-judge/judge.py
"$HERE/build_image.sh"
install -m 0644 "$HERE/teacher-judge.service" /etc/systemd/system/teacher-judge.service
systemctl daemon-reload
systemctl enable teacher-judge
systemctl restart teacher-judge
sleep 2
systemctl is-active teacher-judge
python3 - <<'PY'
import json, socket
s = socket.socket(socket.AF_UNIX); s.settimeout(30); s.connect("/run/teacher-judge/judge.sock")
s.sendall(json.dumps({"mode": "stdio", "source": "print(int(input()) * 2)", "tests": [{"stdin": "21\n"}]}).encode() + b"\n")
out = json.loads(s.makefile().readline())
assert out["ok"] and out["results"][0]["stdout"] == "42\n", out
print("the judge answered: 21 * 2 =", out["results"][0]["stdout"].strip())
PY
