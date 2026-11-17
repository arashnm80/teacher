---
name: no-hard-refresh
description: "Students must always get the latest site without Ctrl+Shift+R: build_site.py stamps every js/css/json address with a content-based build id"
metadata:
  type: feedback
---

Owner (2026-11-17): updates must reach students on a normal visit. Cloudflare in front of the site overrides browser cache of js/css to 4 hours, whatever nginx sends, so only a changing URL helps.

**Why:** hand-bumped `?v=N` numbers drifted (admin had v=23, lessons v=24) and stale scripts stayed for hours.

**How to apply:** never bump `?v=` by hand; `stamp_versions()` in `build_site.py` rewrites them all at build time. New asset types or new directories must be covered by its `VERSIONED`/`STAMPED_TYPES` patterns. HTML pages stay `no-cache`.
