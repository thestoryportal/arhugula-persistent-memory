---
name: c10y-deferred-behind-drive-backup
description: "Operator 2026-10-10: C10Y is DEFERRED (not shelved/removed); verified Drive copy, approved reclaim and fresh run authorization are separate prerequisites"
metadata:
  type: project
---

Operator ruling D-C10r-rulings-17 (ID corrected by MAESTRO28; 6fb1e49 mislabelled it -16, which is the 09:50Z Drive go-live ruling) (2026-10-10 ~23:40Z, `results/c10y_precast_diag/operator_ruling_defer_20261010.md`): "C10Y should be defered, not completely taken out of the possible experiments. We first need to complete the drive backup to ensure enough space is made available for it." Supersedes D-C10r-rulings-15's "SHELVED".

**Why:** the pre-cast needs ~273 GiB free and memit has ~80 GiB; the operator wants space made by moving bulk to Google Drive, not by dropping the experiment.

**How to apply:** never describe C10Y as shelved or removed. Treat a verified Drive copy under the adopted R2 design, separately approved reclaim, and the full C10Y free-disk floor as prerequisites; then propose the C10Y space plan to the operator. Backup verification does not itself free space or authorize activation or a run. C10Y's frozen criteria and the terminal calibration-4 halt are unchanged; a new attempt needs fresh authorization. Related: [[gdrive-rclone-remote]].
