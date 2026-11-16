# Server address hidden behind Cloudflare

Structure (decided by the owner, 2026-11-15):

    user  ->  Cloudflare proxy  ->  website on this server  ->  WARP proxy  ->  AI providers

- Visitors reach the site only through Cloudflare (proxied DNS).
- This server accepts ports 80 and 443 only from Cloudflare's address ranges, so a
  direct connection to the server's address is dropped.
- nginx reads the visitor's real address from `CF-Connecting-IP` (Cloudflare only),
  so rate limits apply per student, not per Cloudflare edge.
- The AI relay calls OpenRouter and Groq only through WARP (see `11th-grade/ai-proxy/`).

## Status

- Installed on 2026-11-15 (the owner ran install.sh). The boot service and the daily timer are enabled.
- Only ports 80 and 443 are covered. Every other port is unchanged on purpose (owner decision).

## Install (after approval)

    sudo bash /root/Storage/teacher/11th-grade/server/install.sh

It installs `/usr/local/sbin/cloudflare-web-guard.sh`, a boot service, and a daily timer
that refreshes Cloudflare's lists (fetched through WARP, cached in
`/var/lib/cloudflare-web-guard/`).

## Checks after install

    iptables -S CF-WEB | tail -2              # ends with -j DROP
    grep -c set_real_ip_from /etc/nginx/conf.d/cloudflare-realip.conf
    curl -s -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0" https://teacher.arashnm80.ir/
    # direct to the server's address must now fail (drop counter goes up):
    iptables -L CF-WEB -v -n | tail -1

## Rollback

    systemctl disable --now cloudflare-web-guard.timer
    iptables -D INPUT -p tcp -m multiport --dports 80,443 -j CF-WEB 2>/dev/null
    iptables -F CF-WEB; iptables -X CF-WEB
    ip6tables -D INPUT -p tcp -m multiport --dports 80,443 -j CF-WEB 2>/dev/null
    ip6tables -F CF-WEB; ip6tables -X CF-WEB
    rm -f /etc/nginx/conf.d/cloudflare-realip.conf && nginx -t && systemctl reload nginx

## Cloudflare dashboard (not changed by these scripts)

- DNS: the `teacher` record stays proxied (orange cloud).
- SSL/TLS mode: Full (strict). The origin uses a Cloudflare Origin certificate, which
  only Cloudflare trusts.
- Optional, stronger: enable Authenticated Origin Pulls, so nginx also requires
  Cloudflare's client certificate.

## Other services (kept as they are, owner decision)

Not touched by the guard: x-ui (20967), xray (16440-16445 and 40001), squid (3128 and 9393),
2053 and 2096, and SSH (22). The NAT tables were checked: nothing redirects inbound 80 or 443
to these services. The only redirects belong to the private-router's own outbound routing.

Retired by the owner: nobelux and utility-server. Their nginx sites still exist and return 502,
because their app ports (3001 and 3002) are not running. This is expected.
