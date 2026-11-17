---
name: api-calls-via-warp-only
description: All requests from this server to OpenRouter/Groq must go through the WARP proxy; the real server IP must never reach an API provider
metadata:
  type: feedback
---

Every request from this server to an AI provider (OpenRouter, Groq, or any other API) goes through a WARP SOCKS proxy, never directly, so the server's real IP is not exposed.

**Why:** the user reminded me of this twice (2026-11-15) while building the playground AI relay.

**How to apply:** the relay (`11th-grade/ai-proxy/app.py`) uses only the WARP SOCKS endpoints in `config.json` (127.0.0.1:4290, 4291), `trust_env=False`, and the systemd unit allows loopback only (`IPAddressAllow=localhost`), so a direct connection fails. Check with the sandbox test in `ai-proxy/` (direct blocked, via WARP 200/401). Never call a provider API from browser code or from a test script without the proxy. The student's browser calls only the site relay (teacher.arashnm80.ir/api/ai/ask).
