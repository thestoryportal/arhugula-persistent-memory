---
name: disk-budget-before-dispatch
description: Every dispatch waits for free disk ≥ projected writes + 20 GiB; every scope states a disk budget; storage policy is runbook §3.3a (gdrive archive)
metadata:
  type: project
---

2026-10-09 ~17:43 MDT: C10Y pre-cast diagnostic (results/c10y_precast_diag/20261009T225619Z, INCONCLUSIVE timeout) persisted 131 float64 operand packets = 105 GB (+12 MB records) → memit 419 GiB at 100% (32 MiB free). ASTRA attempt 4 then started and died in 59 s (infra; Astra RELAUNCH-OK, failed dir archived as results/c10z_astra_attempt4_infrafail_20261009T234321Z). A full pre-cast run (both arms) would need >200 GB.

**Why:** persist-before-gate designs save every operand; scopes budgeted time and RAM but never disk. The queue chain checked the GPU gate, not free space.

**How to apply:** (1) every queue chain / launcher waits for an explicit free-disk floor (≥ 20 GiB plus the job's projected writes) before dispatch; (2) every new scope/prereg states a disk budget (bytes per packet × count) next to time and memory; (3) for reclaim deletions follow [[approved-deletes-ask-then-rmtree]] (regenerable bulk: autonomous under the 2026-10-15 ruling; anything else: per-path AskUserQuestion, then python shutil.rmtree); never re-issue a refused command in variant forms. Related: [[gpu-gate-refuses-any-venv-python]], [[never-idle-arm-completion-watch]].

**Storage policy:** runbook §3.3a (operator, 2026-10-09, BINDING) is the single source: internal SSD is NOT an archive tier; Google Drive via rclone is the archive tier (remote `gdrive:` authorized 2026-10-10, [[gdrive-rclone-remote]]); regenerable bulk is purged after its reading is confirmed, keeping per-file SHA-256 + sizes in git; the internal-SSD mirror is being replaced by a Drive backup ([[backup-via-memitbackup-app]]).
