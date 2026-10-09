---
name: backup-via-memitbackup-app
description: The 6-hourly durable backup runs through ~/Applications/MemitBackup.app (Removable Volumes grant only); never ask for Full Disk Access on /bin/bash
metadata:
  type: project
---
Since 2026-10-08 the launchd job com.rhu.memit-backup runs `/usr/bin/open -W -g ~/Applications/MemitBackup.app`, a single-purpose AppleScript applet (id org.thestoryportal.memitbackup, ad-hoc signed) that only runs ~/Backups/memit/bin/backup_mirror.sh. It holds only macOS's "Removable Volumes" grant. Before that, /bin/bash under launchd was blocked by TCC from Oct 4 (silent failures; "Operation not permitted").

**Why:** the operator declined Full Disk Access ("not comfortable giving permission for my entire Mac internal drive"); the narrow app grant does the job.

**How to apply:** if the backup log shows Operation not permitted, check the app's grant (System Settings → Privacy & Security → Files and Folders), not FDA. Rebuilding/re-signing the app may reset its grant — the operator must click Allow again. Keep ~/Backups/memit/bin/backup_mirror.sh in sync with tools/backup_mirror.sh.
