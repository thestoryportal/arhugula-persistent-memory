# GPT-6-Astra (high) — promote review r2: Google Drive backup fixes

Read-only. Worktree = current dir. Your r1 NO-GO: `results/backup_gdrive_host_20261010/astra_r1_verdict.md`. Host evidence: `results/backup_gdrive_host_20261010/HOST_FINDINGS.md`. That file shows launchd→bash is TCC-denied on the memit volume, and that the old applet hung on a modal error dialog while launchd reported exit 0. The builder's account is the "MB6 Astra r1 and launchd corrections" section of `results/backup_gdrive_build_report.md`, with receipts in `results/backup_gdrive_mb6_20261010T072852Z/`.

Changed files (diff against the r1 baseline: `git diff 8897e3e -- tools/backup_gdrive.sh tools/backup_gdrive_status.py tools/test_backup_gdrive.py tools/test_backup_gdrive_addendum.py tools/launchd/`):
- `tools/backup_gdrive.sh`
- `tools/backup_gdrive_status.py`
- `tools/test_backup_gdrive.py`
- `tools/test_backup_gdrive_addendum.py`
- `tools/launchd/com.rhu.memit-gdrive-backup.plist`
- new: `tools/launchd/MemitGdriveBackup.applescript`, `tools/launchd/build_gdrive_applet.sh`

On the host I reran the full suite: 64 tests OK, 0 skipped. That includes the real `osacompile` build manifest and the exit-1-stub/no-dialog behavioral test. The operator chose "slower by day, full at night", now `--bwlimit '08:00,512k 23:00,off'`. That flag is required, not a finding.

## Check
1. Did each r1 finding (1, 2, 3, 6) close, by code and by a test that fails without the fix? Cite file:line.
2. **New regressions.**
   - Can the RCLONE_* screen or the `rclone config dump` validation refuse a legitimate run forever with no visible status, or leak OAuth credentials into logs or heartbeats?
   - Can the dead-PID stale check misreport a live ~69 h run? Consider PID reuse, and a sleeping Mac.
   - Can the refusal receipts in `refusals/` grow without bound?
3. **Applet and launchd.**
   - Can the applet still block on any UI: an error, a missing `/Volumes/memit`, or the first-run TCC prompt?
   - With `open -W -g`, does a long run hold launchd's job correctly, and does a refused (exit 75) run end promptly?
4. **Activation order.** I plan: first gated merge of PR #21 → update the main checkout → build the applet into `~/Applications` → operator grants Removable Volumes once → load the plist → `launchctl kickstart` → confirm a fresh start heartbeat and status → after the first full copy, unload the old `com.rhu.memit-backup`. Name anything missing or misordered.

## Output
Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. Write `N. none found — <what you inspected>` where empty.

Not acceptable: restating the builder's report, or "add more tests" with no named failing input.
