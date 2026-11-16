# AI helper relay (teacher.arashnm80.ir/api/ai/)

The playground's AI helper sends a student's question to OpenRouter through
this server. Requests leave this machine only through the WARP SOCKS proxies
in `config.json`. The students' devices never contact OpenRouter.

## Files

| File | Where it goes |
| --- | --- |
| `app.py`, `config.json` | `/opt/teacher-ai/` (by `install.sh`) |
| `teacher-ai.service` | `/etc/systemd/system/` (by `install.sh`) |
| `nginx-teacher-ai.conf` | `/etc/nginx/snippets/teacher-ai.conf` (one-time, below) |
| `nginx-ratelimit.conf` | `/etc/nginx/conf.d/teacher-ai-ratelimit.conf` (one-time, below) |

## Install or update

    sudo bash /root/Storage/teacher/11th-grade/ai-proxy/install.sh

## One-time nginx include

1. Copy the two nginx files to the paths above.
2. In `/etc/nginx/sites-available/teacher.arashnm80.ir`, inside the `listen 443`
   server block, add the line `include /etc/nginx/snippets/teacher-ai.conf;`.
3. `nginx -t && systemctl reload nginx`

## Rules

- Egress: only the WARP SOCKS proxies in `config.json`. systemd allows
  loopback only (`IPAddressAllow=localhost`), so a direct connection fails.
- Keys: a student's OpenRouter key arrives in `X-OpenRouter-Key`. It is used
  for one request, never stored, never logged.
- Prompts: built on the server from a few fields (problem, code, failing test).
  The endpoint cannot be used to send arbitrary prompts.
- Limits: per IP (nginx `limit_req`, 60/min, burst 40) and per key (40 per 10 min).
