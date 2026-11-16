#!/usr/bin/env bash
# Hide the origin behind Cloudflare.
#  - Ports 80 and 443 accept only Cloudflare's address ranges (plus loopback and the
#    local private networks). A direct connection to this server's address is dropped.
#  - nginx takes the visitor's real address from CF-Connecting-IP, and only when the
#    connection comes from Cloudflare. Rate limits then apply per student.
# The Cloudflare lists are fetched through WARP (never directly). The last good lists
# are cached, so a boot without WARP still works. Safe to run again.
set -euo pipefail

STATE=/var/lib/cloudflare-web-guard
REALIP=/etc/nginx/conf.d/cloudflare-realip.conf
WARP_PROXIES=("127.0.0.1:4290" "127.0.0.1:4291")
mkdir -p "$STATE"

refresh() {  # $1 = v4 or v6
  local name="ips-$1" tmp="$STATE/$1.tmp" proxy
  for proxy in "${WARP_PROXIES[@]}"; do
    if curl -fsS -m 30 --socks5-hostname "$proxy" "https://www.cloudflare.com/$name" -o "$tmp" 2>/dev/null \
       && [ -s "$tmp" ] && ! grep -v -E -q '^[0-9a-fA-F:.]+/[0-9]+$' "$tmp"; then
      mv "$tmp" "$STATE/$name"
      rm -f "$tmp"
      return 0
    fi
  done
  rm -f "$tmp"
  echo "cloudflare-web-guard: WARP not reachable, using the cached $name" >&2
}
refresh v4
refresh v6

# 1) nginx: trust Cloudflare's addresses, read the real visitor address from CF-Connecting-IP.
{
  echo "# Written by cloudflare-web-guard.sh. Only Cloudflare addresses may set the visitor address."
  while read -r cidr; do echo "set_real_ip_from $cidr;"; done < "$STATE/ips-v4"
  while read -r cidr; do echo "set_real_ip_from $cidr;"; done < "$STATE/ips-v6"
  echo "real_ip_header CF-Connecting-IP;"
} > "$REALIP.new"
[ -f "$REALIP" ] && cp "$REALIP" "$REALIP.bak"
mv "$REALIP.new" "$REALIP"
if ! nginx -t >/dev/null 2>&1; then
  if [ -f "$REALIP.bak" ]; then mv "$REALIP.bak" "$REALIP"; else rm -f "$REALIP"; fi
  echo "cloudflare-web-guard: nginx test failed; previous configuration kept" >&2
  exit 1
fi
rm -f "$REALIP.bak"
systemctl reload nginx || true

# 2) firewall: web ports only from Cloudflare (plus loopback and private networks).
#    The chain is filled first and the jump into INPUT is added last, so a failure
#    part-way never leaves the ports closed without the Cloudflare rules.
apply() {  # $1 = iptables | ip6tables, $2 = list file, $3 = local networks to keep
  local ipt=$1 list=$2 chain=CF-WEB net cidr
  command -v "$ipt" >/dev/null 2>&1 || return 0
  "$ipt" -N "$chain" 2>/dev/null || true
  "$ipt" -F "$chain"
  for net in $3; do "$ipt" -A "$chain" -s "$net" -j ACCEPT; done
  while read -r cidr; do "$ipt" -A "$chain" -s "$cidr" -j ACCEPT; done < "$list"
  "$ipt" -A "$chain" -j DROP
  "$ipt" -C INPUT -p tcp -m multiport --dports 80,443 -j "$chain" 2>/dev/null \
    || "$ipt" -I INPUT 1 -p tcp -m multiport --dports 80,443 -j "$chain"
}
apply iptables "$STATE/ips-v4" "127.0.0.0/8 172.16.0.0/12"
apply ip6tables "$STATE/ips-v6" "::1/128"
echo "cloudflare-web-guard: web ports open to Cloudflare only; nginx reads CF-Connecting-IP"
