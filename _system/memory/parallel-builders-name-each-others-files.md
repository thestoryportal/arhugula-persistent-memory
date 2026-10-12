---
name: parallel-builders-name-each-others-files
description: When two Codex builders share one worktree, each brief must list the files the other is authorized to change, or a hash-protection check raises a false STOP
metadata:
  type: feedback
---
When two builders work in the same worktree at once, each brief names the other's write scope (exact files and receipt dirs), says those edits are authorized, and tells it not to hash them as protected or STOP over them.

**Why:** 2026-10-10, MB18 (NEW-1) hashed the Drive-backup files as "protected", saw MB20's authorized edits to them, and raised a STOP; MAESTRO15 had to reconcile the drift by hand (`results/mathlab_staging/new1_construction_diag_investigate_20261010T174911.191674Z/maestro15_drift_reconciliation.md`).

**How to apply:** in each brief's `<boundaries>`, add one paragraph: "Another builder, <name>, is working on <area> in this worktree. Its files are <list>. Those edits are authorized; do not touch them, and do not STOP over their changing." MB21 (Drive) and MB22 (dashboard) briefs were the first written this way. See [[context-management-every-session]] and [[test-first-one-round-builds]].
