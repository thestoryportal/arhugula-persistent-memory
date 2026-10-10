# Drive backup — host verification by MAESTRO4, 2026-10-10

These are host-side runs that Codex cannot do (its sandbox has no network).

## 1. Drive self-tests: PASS
- `tools/test_backup_gdrive.py --drive`: PASS. Receipts are in `results/backup_gdrive_drive_20261010T071708Z/`, stdout in `drive_selftest_stdout.json`.
  - Three tiny syncs ran against real Drive. They created, modified and deleted files, and the replaced and deleted files were archived to `_selftest/.deleted/<stamp>/`.
  - The lock, unmounted-volume and empty-source refusals all fired.
  - `_selftest/` was purged afterward.
- `tools/test_backup_gdrive_addendum.py --archive-drive`: PASS (`results/backup_gdrive_archive_20261010T072051Z/`). It copied a file, verified the download and its SHA, and the source was preserved and the remote cleaned up.
- Upload rate: a 200 MB probe took 172.1 s, i.e. **1.16 MB/s**.
- Real-source dry run: **40,412 files / 287,080,274,442 bytes** to transfer. At the measured rate, the first full upload is about **247,000 s, roughly 69 h (~2.9 days)**. That is payload rate only; per-file API overhead is not included.

## 2. Plain launchd→bash cannot read the source volume
A throwaway agent `com.rhu.tcc-probe` was bootstrapped, kickstarted and booted out (plist and output are in this directory). `/bin/bash`, started by launchd, got `ls: /Volumes/memit/llm-database-poc-mirror: Operation not permitted`, and a file read failed the same way.

So `tools/launchd/com.rhu.memit-gdrive-backup.plist` as built, which runs `/bin/bash` directly, would fail on every run. Removable-volume access has to come through an app the operator grants, as with the old `~/Applications/MemitBackup.app`.

## 3. The old backup has been silently hung since 2026-10-09 17:56 local
- `~/Backups/memit/backup.launchd.log` was last written at 17:56. That was the rsync exit-24 "FATAL".
- `launchctl print` reports `runs = 5, last exit code = 0`.
- The unified log shows the applet (pid 19469) started at 17:56:13 and terminated at 23:39:53.

The old applet's body is a bare `do shell script "…backup_mirror.sh …"` (decompiled from `MemitBackup.app`). When the shell script exits nonzero, AppleScript raises an error, and an applet shows that error as a **modal dialog**. `open -W` then waits on the dialog, and launchd will not start the next interval while the job is still running.

The result is hours of no backups, with launchd still reporting exit 0. A replacement applet must never be able to show a dialog. Health has to be judged from the heartbeat and status tool, not from launchd's exit code.

## 4. Activation is gated on PR #21 merging
The plist points at the main checkout (`master`), and `tools/backup_gdrive.sh` is not on `master` yet (`git cat-file -e master:tools/backup_gdrive.sh` fails). The order is:
1. Build and Astra-review the fixes.
2. First gated merge.
3. Update the main checkout.
4. Install the applet; the operator grants Removable Volumes once.
5. Load the job and `launchctl kickstart` it, with heartbeat evidence.
6. Retire the old job.

## Astra r1
NO-GO, with 3 P1 findings and 1 P2 (`astra_r1_verdict.md`). Each P1 was checked against the code at `tools/backup_gdrive.sh:17,76,100,115` and holds.
