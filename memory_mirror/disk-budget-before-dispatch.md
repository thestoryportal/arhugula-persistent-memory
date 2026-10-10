---
name: disk-budget-before-dispatch
description: The C10Y pre-cast diagnostic wrote 110 GB and filled /Volumes/memit, killing the next GPU job; every dispatch needs a disk check and every scope a disk budget
metadata:
  type: project
---

2026-10-09 ~17:43 MDT: C10Y pre-cast diagnostic (results/c10y_precast_diag/20261009T225619Z, INCONCLUSIVE timeout) persisted 131 float64 operand packets = 105 GB (+12 MB records) → memit 419 GiB at 100% (32 MiB free). ASTRA attempt 4 then started and died in 59 s (infra; Astra RELAUNCH-OK, failed dir archived as results/c10z_astra_attempt4_infrafail_20261009T234321Z). A full pre-cast run (both arms) would need >200 GB.

**Why:** persist-before-gate designs save every operand; scopes budgeted time and RAM but never disk. The queue chain checked the GPU gate, not free space.

**How to apply:** (1) every queue chain / launcher waits for an explicit free-disk floor (≥ 20 GiB plus the job's projected writes) before dispatch; (2) every new scope/prereg states a disk budget (bytes per packet × count) next to time and memory; (3) §3.3 reclaim deletions may be refused by the Bash safety check — hand the operator literal commands, never re-issue variants. Related: [[gpu-gate-refuses-any-venv-python]], [[never-idle-arm-completion-watch]].

**Operator policy (2026-10-09, BINDING; runbook §3.3a):** internal SSD is NOT an archive tier. Remote archive = Google Drive via rclone (installed v1.75.2; OAuth remote `gdrive` pending at the Mac). Regenerable bulk is purged after its reading is confirmed, keeping per-file SHA-256 + sizes in git. Plan approved: replace the internal-SSD memit mirror with a Drive backup.
