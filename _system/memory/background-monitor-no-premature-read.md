---
name: background-monitor-no-premature-read
description: "RETIRED 2026-10-10 — merged into never-idle-arm-completion-watch; do not act on this note"
metadata:
  type: reference
---
RETIRED 2026-10-10 by the memory audit (results/memory_audit_20261010/). Merged into [[never-idle-arm-completion-watch]] (the one still-true rule: never Read a background task's output before its notification; foreground sleep is blocked, use Monitor). Full prior text: `git show fd77f7e:memory_mirror/background-monitor-no-premature-read.md`.
