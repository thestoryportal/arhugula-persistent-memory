# MAESTRO5 host verification of MB8 (2026-10-10T08:48:18Z)

- `shasum -c SHA256SUMS.txt`: all OK (code, tests, report, host helper match the build).
- Full acceptance on host: `.venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive` → **72 OK, 0 skipped** (106 s). The two sandbox-UNVERIFIED launcher tests run natively here.
- `tools.test_backup_gdrive_addendum.LauncherTest` → 3 OK (real osacompile + manifest; launchd waits for background applet; nonzero script caught promptly with no dialog).
- Astra r2 finding 9 — real app bundles through `/usr/bin/open -W -g` (host_launcher_checks.py, receipts in host_<case>_*/):
  - long (3 s stub): PASS, open -W held 3.61 s and returned after the stub finished, receipt exit 0.
  - exit75 (live owner): PASS, 0.48 s, receipt exit 75, owner heartbeat byte-identical, status incomplete (not failed).
  - absent (/Volumes/memit-mb8-absent-…): PASS, 0.49 s, receipt exit 127, status "failed backup launch" over a seeded fresh success.
  - writefail (receipt dir 0555): PASS, 0.47 s, prior receipt preserved, no temp leak, no dialog.
- Not covered here (activation steps): production TCC Removable Volumes grant; real launchd load/kickstart.
