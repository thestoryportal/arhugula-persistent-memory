# MB21 host verification — MAESTRO18, 2026-10-10 ~19:33–19:50Z

Sources re-hashed against MB21's final table before running (all match): backup_gdrive_status.py 10632286…, MemitGdriveBackup.applescript 80c7b712…, test_backup_gdrive_addendum.py da2389f2…, backup_gdrive.sh 36647860… (unchanged), host_launcher_checks_mb21.py e6e8a21e…, build report 2d9d23c5….

- `acceptance.log`: `tools.test_backup_gdrive_addendum` with real local rclone (BACKUP_TEST_NO_RCLONE=0), local temp destinations only: **109 OK, 0 skipped**, exit 0 (r6 had 103; MB21 adds 6 net, 2 more renamed/reversed). Real-path inventory `real_paths_before.json` / `real_paths_after.json` byte-identical (cmp).
- `base_module.log`: `tools.test_backup_gdrive`: **10 OK**. Total 119 OK, 0 skipped.
- Native applets via MB21's helper, fixtures under /private/tmp: crash-after-allocation, recovery, unresolved-compaction and the new compaction-boundary **PASS**. manual-interleave run 1 **FAILED** (`Native_2.app` `open -W -g` timed out at 20 s on the per-app Removable Volumes prompt, `native_manual-interleave_run1_FAIL_prompt.log`), then **PASSED** on unchanged sources after the operator clicked Allow (`native_manual-interleave.log`), as in MB20's r6 round. Run 1's blocked fixture applet (pids 36233/36258/37109, /private/tmp/memit_gdrive_native_yqxs6z_9) stayed alive afterwards.
