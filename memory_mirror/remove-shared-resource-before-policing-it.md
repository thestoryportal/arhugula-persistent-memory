---
name: remove-shared-resource-before-policing-it
description: When a proof/review loop can't terminate, step back to architecture — remove the contention instead of proving the policing complete (R2 → Git+Drive, 2026-10-11)
metadata:
  type: feedback
---
R2 (two Macs sharing memit) ran ~14 h and 10+ Astra NO-GOs trying to prove a complete list of every process science could start. The round-13 Sol sweep + AST tracer showed it can never close (Torch/Git/Bash internals untraceable). Fences (sandbox), run-time watch, single-file scripts and tar transfers each fixed only part. The operator cut through it: "Can the Intel Mac pull in its needed context directly from Git on demand instead?" → the initial Git+Drive concept kept memit M3-only (operator GO 2026-10-11 23:02Z, `results/compute_storage_brainstorm_20261011T054507Z/r2_redesign_operator_ruling.md`). The later adopted v4 (D-R2C-ADOPT) has the M3 push to approved Intel staging and Intel perform Drive uploads, retries and checks; Intel never accesses memit. The M3 push observes the existing check_gpu gate and stops when science starts. Design adoption is not activation authorization; activation still needs its separate approval and checks.

**Why:** policing a shared resource requires a complete model of every actor; removing the sharing removes the need for that model.

**How to apply:** when a gate loop finds "one more layer" twice in a row, ask first "can the contention be designed away?" (separate copies, pull-on-demand from the source of truth) before proposing stronger enforcement. Bring that framing to the operator early, in plain words. Related: [[intel-exists-to-offload-the-m3]]; [[sol-for-sweeps-astra-for-gates]] (Claude auto-memory, not memory_mirror/).
