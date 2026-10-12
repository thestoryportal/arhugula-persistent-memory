# GPT-6-Astra (high) — re-review r7: Google Drive backup (launcher + status)

Read-only. Worktree = current dir. Your r6 verdict (`results/backup_gdrive_host_20261010/astra_r6_verdict.md`) was NO-GO on: finding 2 (P1), recovery read only archived manifests, so an MB14-era recovery of failure 100 + `{torn` at floor 10 let MB20 accept floor 11 and report completion 13 healthy; finding 3 (P2), `refusals/latest-refusal.json`'s generation was missing from the observed maximum (floor 10 accepted with surviving refusal 100); finding 4 (P2), compaction cleared at `completed == barrier` in status (`:469`) and both applet Perl publishers. Findings 1 and 5 were clean; 6 restated activation.

The fix is MB21, committed at `f22c9f2`: `git diff 73f8a9b f22c9f2 -- tools/backup_gdrive_status.py tools/launchd/MemitGdriveBackup.applescript tools/test_backup_gdrive_addendum.py`. Read the section "MB21 Astra r6 findings 2 (P1), 3 (P2) and 4 (P2) build and verification" at `results/backup_gdrive_build_report.md:715` onward, and the receipts in `results/backup_gdrive_mb21_20261010T191747Z/` (`RED_index.json`, the `RED_*.log` / `GREEN_*.log`, `verification.json`, `hashes_final.json`, the captured MB14 fixture `mb14_fixture/` with `mb14_fixture_tree_sha256.json` and `mb14_recovery_command.json`). Source SHA-256 at review time: backup_gdrive.sh 36647860… (unchanged), backup_gdrive_status.py 10632286…, MemitGdriveBackup.applescript 80c7b712…, test_backup_gdrive_addendum.py da2389f2… (full values: `hashes_final.json`).

## My host evidence, which you cannot reproduce

All in `results/backup_gdrive_mb21_20261010T191747Z/host_runs_maestro18/` (README.md summarizes). Sources re-hashed first; all match MB21's final table.
- Full acceptance with real rclone against local temp destinations only: `tools.test_backup_gdrive_addendum` **109 OK** + `tools.test_backup_gdrive` **10 OK** = 119 OK, 0 skipped (r6: 103 + 10; MB21 adds 6 net, 2 more renamed/reversed). Real-path inventory byte-identical before and after.
- Native applets via `/usr/bin/open -W -g`, MB21's helper `host_launcher_checks_mb21.py`, fixtures under `/private/tmp`: crash-after-allocation, recovery, unresolved-compaction and the new compaction-boundary PASS. manual-interleave first FAILED (`Native_2.app` blocked 20 s on the per-app Removable Volumes prompt, as in r5/r6), then PASSED on unchanged sources after the operator clicked Allow.

## Check against the code (cite file:line)

1. r6 finding 2 closed: replay the captured MB14 output (`mb14_fixture/`) under MB21. `recover --generation-floor 11` must refuse with nothing mutated (counter, unresolved state, receipt, journal, every recovery dir); floor 100 must reserve barrier 101; completion 101 must not read healthy and 102 must. Is every payload in every recovery directory inspected (raw counter, heartbeat/receipt JSON, each independently parsed journal line before and after torn lines), both before any mkdir/lock and again under the allocator lock? Name any archived file, nesting or encoding that escapes the scan.
2. r6 finding 3 closed: corrupt counter, absent unresolved state, completed 10, null-generation receipt, surviving refusal generation 100 → floor 10 refuses without mutation; floor 100 succeeds. A refusal (exit 75) still never journals a failure or adds an unresolved interval. Is any other generation-bearing file the wrapper or applet writes (`tools/backup_gdrive.sh`, applet) still outside both maxima?
3. r6 finding 4 closed: `completed == compaction_barrier` is unhealthy in status and leaves the barrier in both Perl publishers; `completed == barrier + 1` clears it. Check your 11…137 / 139 schedule and the native compaction-boundary case (139 retained during publication 140, cleared at 141).
4. No regression in r6 findings 1 and 5: the r5 torn-journal case; 64-interval / 2,048-byte bounds on every write path through 2,000 alternating allocations; `recovery_barrier` retained; refusal and manual completion cannot discharge barriers; your r4 manual-interleave schedule; generation (not wall-clock) ordering; exit 75 never marks an active owner failed; status never writes `last_run.json`; no applet dialog; `open -W -g` waits; retries, bandwidth and excludes unchanged.
5. Anything else that blocks activation. Restate the ordered activation checklist from r6 §6, adjusted for MB21's evidence list (the operator-reviewed floor must cover every observed generation, including archived recovery-dir payloads and the refusal heartbeat).

## Output

Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, or generic advice with no named failing input.
