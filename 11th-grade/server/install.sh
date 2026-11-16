#!/usr/bin/env bash
# Install or update the origin guard (run as root; safe to run again).
# This changes live firewall rules (ports 80 and 443) and the nginx config.
# Rollback: see server/README.md.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
install -m 0755 "$SRC/cloudflare-web-guard.sh" /usr/local/sbin/cloudflare-web-guard.sh
install -m 0644 "$SRC/cloudflare-web-guard.service" /etc/systemd/system/cloudflare-web-guard.service
install -m 0644 "$SRC/cloudflare-web-guard.timer" /etc/systemd/system/cloudflare-web-guard.timer
systemctl daemon-reload
/usr/local/sbin/cloudflare-web-guard.sh
systemctl enable cloudflare-web-guard.service >/dev/null   # re-applies the rules at boot
systemctl enable --now cloudflare-web-guard.timer >/dev/null
echo "installed; timer: $(systemctl is-active cloudflare-web-guard.timer)"
