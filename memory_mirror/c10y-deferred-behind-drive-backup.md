---
name: c10y-deferred-behind-drive-backup
description: "Operator 2026-10-10: C10Y is DEFERRED (not shelved/removed); it unblocks once the Drive backup frees memit space"
metadata:
  type: project
---

Operator ruling D-C10r-rulings-16 (2026-10-10 ~23:40Z, `results/c10y_precast_diag/operator_ruling_defer_20261010.md`): "C10Y should be defered, not completely taken out of the possible experiments. We first need to complete the drive backup to ensure enough space is made available for it." Supersedes D-C10r-rulings-15's "SHELVED".

**Why:** the pre-cast needs ~273 GiB free and memit has ~80 GiB; the operator wants space made by moving bulk to Google Drive, not by dropping the experiment.

**How to apply:** never describe C10Y as shelved or removed. Treat the Drive backup (locked release → host tests → Astra r11 → activation → verified mirror) as a prerequisite on the C10 path, and when it completes, propose the C10Y space plan to the operator. C10Y's frozen criteria and the terminal calibration-4 halt are unchanged; a new attempt needs fresh authorization. Related: [[gdrive-rclone-remote]].
