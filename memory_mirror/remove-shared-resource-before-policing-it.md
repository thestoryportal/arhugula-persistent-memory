---
name: remove-shared-resource-before-policing-it
description: When a proof/review loop can't terminate, step back to architecture — remove the contention instead of proving the policing complete (R2 → Git+Drive, 2026-10-11)
metadata:
  type: feedback
---
R2 (two Macs sharing memit) ran ~14 h and 10+ Astra NO-GOs trying to prove a complete list of every process science could start. The round-13 Sol sweep + AST tracer showed it can never close (Torch/Git/Bash internals untraceable). Fences (sandbox), run-time watch, single-file scripts and tar transfers each fixed only part. The operator cut through it: "Can the Intel Mac pull in its needed context directly from Git on demand instead?" → Intel reads records from Git and bulk from Google Drive; memit is M3-only; the only rule left is M3-local backup/science mutual exclusion plus proactive storage management (operator GO 2026-10-11 23:02Z, `results/compute_storage_brainstorm_20261011T054507Z/r2_redesign_operator_ruling.md`).

**Why:** policing a shared resource requires a complete model of every actor; removing the sharing removes the need for that model.

**How to apply:** when a gate loop finds "one more layer" twice in a row, ask first "can the contention be designed away?" (separate copies, pull-on-demand from the source of truth) before proposing stronger enforcement. Bring that framing to the operator early, in plain words. Related: [[sol-for-sweeps-astra-for-gates]].
