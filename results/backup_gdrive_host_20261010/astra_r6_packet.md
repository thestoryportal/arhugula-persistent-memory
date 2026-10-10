# GPT-6-Astra (high) — re-review r6: Google Drive backup (launcher + status)

Read-only. Worktree = current dir. Your r5 verdict (`results/backup_gdrive_host_20261010/astra_r5_verdict.md`) was NO-GO on: P1, recovery discarded every parsed journal record when one line was torn and accepted a floor below the observed maximum (your case: corrupt counter, absent unresolved state, completed 10, null-generation receipt, journal with valid failure 100 then `{torn`, `recover --generation-floor 10`, then healthy at 12); P2, unresolved-interval state grew without bound (1,000 intervals after 2,000 alternating allocations). Findings 1 and 4 were clean; 5 restated activation.

The fix is MB20, committed at `6edae80`: `git diff 3a22447 6edae80 -- tools/backup_gdrive_status.py tools/launchd/MemitGdriveBackup.applescript tools/test_backup_gdrive_addendum.py`. Read the section "MB20 Astra r5 findings 2 (P1) and 3 (P2) build and verification" at `results/backup_gdrive_build_report.md:593` onward, and the receipts in `results/backup_gdrive_mb20_20261010T180133Z/` (`RED_index.json`, the nine `RED_0*.log`, `GREEN_*.log`, `verification.json`). Source SHA-256 at review time: backup_gdrive.sh 36647860…, backup_gdrive_status.py a4d3978b…, MemitGdriveBackup.applescript 31566aca…, test_backup_gdrive_addendum.py 6bca5cd7… (full list: `results/backup_gdrive_mb20_20261010T180133Z/hashes_final.json`).

## My host evidence, which you cannot reproduce

All in `results/backup_gdrive_mb20_20261010T180133Z/host_runs_maestro16/` (README.md summarizes):
- The 9 new tests rerun by me: 9 OK. Full acceptance, real rclone against local temp destinations only: `tools.test_backup_gdrive_addendum` 103 OK + `tools.test_backup_gdrive` 10 OK = **113 OK, 0 skipped** (r5's 104 was 94 + 10; the 9 new tests account for the difference, none removed). Real-path inventory (HOME backup-log glob, the Applications app, LaunchAgents) byte-identical before and after each module.
- Native applets through `/usr/bin/open -W -g`, MB20's helper `host_launcher_checks_mb20.py`, fixtures under `/private/tmp`: crash-after-allocation, recovery and the new unresolved-compaction PASS. manual-interleave first FAILED (`Native_2.app` blocked 20 s on the per-app Removable Volumes prompt, as in r5), then PASSED on unchanged sources after the operator clicked Allow. The first run's blocked applet stayed alive afterwards; its fixture HOME is under /private/tmp.

## Check against the code (cite file:line)

1. r5 P1 closed: replay your exact case. `recover --generation-floor 10` must refuse without mutating anything (counter, unresolved state, receipt, journal, barrier, archive); `--generation-floor 100` must then succeed, and generation 101 or below must not read healthy. Also: valid records after a torn line still count toward the maximum; the ambiguous journal is preserved byte-for-byte; a floor below any observed generation (counter, issued state, heartbeat, receipt, parseable journal records, preserved recovery manifests) refuses before creating a recovery directory or taking the counter lock, and is re-checked under the allocator lock. Is there any observed-generation source the floor check misses?
2. r5 P2 closed: is persisted unresolved state bounded (64 intervals, 2,048 bytes) on every write path: Python recovery publication and both embedded Perl publishers in the applet? On overflow, does compaction into `compaction_barrier = issued_generation` ever drop or acknowledge an unresolved failure, let a refusal (exit 75) or manual run clear the barrier, or lose the existing `recovery_barrier`? What clears it, and is that a sequenced completion strictly above it?
3. No regression in r5 findings 1 and 4: your r4 manual-interleave schedule; generation (not wall-clock) ordering; exit 75 never marks an active owner failed; status never writes `last_run.json`; no applet path can show a dialog; `open -W -g` waits; a late-released applet cannot acknowledge a later failure; retries, bandwidth and excludes unchanged.
4. Anything else that blocks activation. Restate the ordered activation checklist from r5 §5, adjusted for MB20's recovery rule (the operator-reviewed floor must be at least every observed generation).

## Output

Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, or generic advice with no named failing input.
