---
name: backup-via-memitbackup-app
description: Interim 6-hourly internal-SSD mirror runs via MemitBackup.app (Removable Volumes grant, never FDA); not an archive tier; being replaced by gdrive
metadata:
  type: project
---
Since 2026-10-08 the launchd job com.rhu.memit-backup runs `/usr/bin/open -W -g ~/Applications/MemitBackup.app`, a single-purpose AppleScript applet (id org.thestoryportal.memitbackup, ad-hoc signed) that only runs ~/Backups/memit/bin/backup_mirror.sh. It holds only macOS's "Removable Volumes" grant. Before that, /bin/bash under launchd was blocked by TCC from Oct 4 (silent failures; "Operation not permitted").

**Status (2026-10-10):** this internal-SSD mirror is an interim convenience, not an archive tier — CLAUDE.md storage discipline and runbook §3.3a make Google Drive (`gdrive:`) the warehouse, and the Drive backup (`tools/backup_gdrive.sh` + `tools/launchd/com.rhu.memit-gdrive-backup.plist`) is code-prepared but not yet activated (`results/backup_gdrive_build_report.md`). The last logged mirror run (`~/Backups/memit/backup.launchd.log`, 2026-10-09 17:56) ended `backup_mirror: FATAL: rsync failed` on a benign rsync exit 24 (a git temp object vanished mid-copy) and no later run is logged. **Root cause of the silence (MAESTRO4, 2026-10-10, `results/backup_gdrive_host_20261010/HOST_FINDINGS.md`):** the applet's bare `do shell script` turned the nonzero exit into an AppleScript error, shown as a **modal dialog**; `open -W` waited on it ~6 h and launchd starts no new interval while the job runs — yet `launchctl print` said `last exit code = 0`. Any applet launcher must wrap `do shell script` in `try … end try` and never show a dialog; judge backup health from the wrapper's heartbeat/status, never launchd's exit code. A kickstarted probe re-confirmed launchd→`/bin/bash` gets "Operation not permitted" on /Volumes/memit (2026-10-10).

**Why:** the operator declined Full Disk Access ("not comfortable giving permission for my entire Mac internal drive"); the narrow app grant does the job.

**How to apply:** if the backup log shows Operation not permitted, check the app's grant (System Settings → Privacy & Security → Files and Folders), not FDA. Rebuilding/re-signing the app may reset its grant — the operator must click Allow again. Keep ~/Backups/memit/bin/backup_mirror.sh in sync with tools/backup_mirror.sh. A new launcher (e.g. the gdrive job running bash directly) needs its own macOS access check before it replaces this one. Related: [[gdrive-rclone-remote]], [[disk-budget-before-dispatch]].
