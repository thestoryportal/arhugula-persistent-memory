# MB14 receipt counter drift — MAESTRO14, 2026-10-10 ~17:49Z

Two committed MB14 receipt files changed in the worktree after their run (MB14 native runs were ~10:28Z):

| file (under results/backup_gdrive_mb14_20261010T095752Z/) | committed | worktree | mtime |
|---|---|---|---|
| native_manual-interleave_20261010T102801.532670Z/fixture/home/Library/Logs/memit-gdrive-backup-launch-state/counter | 10 | 11 | 16:15:35Z |
| native_crash-after-allocation_20261010T102821.705146Z/fixture/home/Library/Logs/memit-gdrive-backup-launch-state/counter | 10 | 11 | 17:20:23Z |

The third (native_recovery) is unchanged (mtime 10:28:41Z).

Reading (plausible, not proven): the MB14 fixture applets were blocked on the per-app Removable Volumes prompt (memory_mirror/native-applet-removable-volumes-prompt.md) and each ran its wrapper once when an Allow was clicked. The crash-after-allocation change lands 36 s before MAESTRO13's post-Allow snapshot (host_runs_maestro12/native2_tree_after_allow_maestro13.txt, 17:20:59Z). That snapshot lists only the MB16 Native_2 process group, so it can neither confirm nor exclude MB14 processes at 17:20:23Z. At 17:49Z no applet, osascript or backup_gdrive process is running; the only memit LaunchAgent is the pre-existing com.rhu.memit-backup.

Consequence: a native fixture applet that hits the prompt can outlive its test by hours and act later on its fixture tree. Action taken: the two counters are restored to their committed bytes (git checkout), so the MB14 receipts stay as recorded at their run. Carried to Astra r5.
