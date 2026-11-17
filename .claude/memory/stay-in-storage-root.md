---
name: stay-in-storage-root
description: Keep the shell working directory at /root/Storage; never cd into a sub-repo
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-14T20:15:19.119Z
---

The working directory should always stay /root/Storage. Inspect sub-repos with `git -C <repo>` or absolute paths instead of `cd`-ing into them.

**Why:** cd-ing into a repo (e.g. your-alfred-bot) made it the workspace dir, and the built-in safety check then blocked deleting that repo when the user asked for cleanup.

**How to apply:** In /root/Storage, use `git -C`, absolute paths, or subshells `( cd x && ... )` for per-repo commands, so the session cwd never moves.
