# MAESTRO16 host verification of MB20 (2026-10-10, 18:21–19:05Z)

Sources at run time: backup_gdrive_status.py a4d3978b…, MemitGdriveBackup.applescript 31566aca…, test_backup_gdrive_addendum.py 6bca5cd7…, backup_gdrive.sh 36647860… (all 41 entries of ../hashes_final.json re-verified on disk).

- `scoped_r5_9tests.log`: the 9 new R5 tests rerun by MAESTRO16, 9 OK.
- `acceptance.log`: full `tools.test_backup_gdrive_addendum`, real local rclone, no restrictions: 103 OK, 0 skipped (94 MB14 tests + 9 new; none removed).
- `acceptance_base.log`: `tools.test_backup_gdrive`: 10 OK, 0 skipped. Together 113 OK, matching the r5 standard (r5's 104 = 94 + 10).
- `real_paths_*.json`: real HOME log glob, the Applications app and LaunchAgents, before/after each module; all four files byte-identical (21 entries).
- `native/`: MB20 helper cases. crash-after-allocation, recovery, unresolved-compaction PASS first time. manual-interleave first run FAIL: `open -W -g Native_2.app` timed out at 20 s, blocked on the per-app Removable Volumes prompt (same signature as r5). Operator clicked Allow; rerun on unchanged sources PASS (`manual-interleave_rerun_after_allow.log`). The first run's Native_2 applet (pid 32906, fixture under /private/tmp) stayed blocked afterwards.
