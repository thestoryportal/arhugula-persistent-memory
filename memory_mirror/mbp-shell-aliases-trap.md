---
name: mbp-shell-aliases-trap
description: "On Robert's M3 Pro, du/cat/ls/grep/find are aliased or wrapped (dust, bat, eza, rtk); use `command <tool>` or absolute paths in scripts"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-03T23:55:41.082Z
---

On this Mac, `du` is aliased to dust, `cat` to `bat --paging=never`, `ls` to eza, and `grep`/`find` are shell functions (rtk wrappers). Verified 2026-10-03 with `type`. Robert's own project memory lists the same quirks and adds that rsync over direct TCP needs the `-e` flag.

**Why:** `du -sh */ | sort -h` printed dust's help text instead of sizes; parsed output from these commands will be wrong or empty.

**How to apply:** prefix with `command ` (e.g. `command du -sh`) or use `/usr/bin/du`, `/bin/cat`; expect `rg`/`fd`/`dust`/`bat` to be on PATH via Homebrew. See [[llm-db-local-migration-gaps]].
