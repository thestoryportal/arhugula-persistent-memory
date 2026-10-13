# GPT-6-Astra (high) — re-review r5: Google Drive backup (launcher + status)

Read-only. Worktree = current dir. Your r4 verdict (`results/backup_gdrive_host_20261010/astra_r4_verdict.md`) was NO-GO on: P1, an exit-75 refusal receipt exempted the whole outstanding counter and so hid a failure recorded only by the counter (your manual-interleave schedule); P2, a missing/corrupt counter published null-generation evidence that allocation and status then rejected forever, a recovery trap. Findings 2 and 4 were clean; 5 restated activation.

The fix is MB14, uncommitted in the working tree: `git diff HEAD -- tools/backup_gdrive_status.py tools/launchd/MemitGdriveBackup.applescript tools/test_backup_gdrive_addendum.py`. Read the section "MB14 Astra r4 findings 1 (P1) and 3 (P2) build and verification" at `results/backup_gdrive_build_report.md:481` onward (including its recovery command, `tools/backup_gdrive_status.py recover --generation-floor N`), and the receipts in `results/backup_gdrive_mb14_20261010T095752Z/`. Source SHA-256 at review time: `results/backup_gdrive_mb16_20261010T103826Z/host_runs_maestro14/sources_sha256.txt` (backup_gdrive.sh 36647860…, backup_gdrive_status.py 64d59eab…, MemitGdriveBackup.applescript 683cb5a3…, test_backup_gdrive_addendum.py 74cbd8af…). Verify them first; a mismatch means stop.

## My host evidence, which you cannot reproduce

- Full acceptance on the host, no fixture restrictions, real rclone against local temp destinations only: `tools.test_backup_gdrive_addendum tools.test_backup_gdrive` ran **104 tests OK, 0 skipped**, 17:50–17:51Z (`results/backup_gdrive_mb16_20261010T103826Z/host_runs_maestro14/full_acceptance.{log,meta}`). The 16 tests MB14 left host-pending (14 real-rclone, 2 native) ran in it.
- Native app bundles through `/usr/bin/open -W -g`, with MB16's rebuilt helper (fixtures under `/private/tmp`, outside `/Volumes`; `results/backup_gdrive_mb16_20261010T103826Z/build_report.md`): crash-after-allocation PASS and recovery PASS at 10:51Z (`host_runs_maestro12/`); manual-interleave rc=1 at 10:51Z, then PASS on unchanged sources at 17:42Z (`host_runs_maestro13/`, `native_manual-interleave_20261010T174248.434344Z/`).
- The manual-interleave failure was the per-app **Removable Volumes** privacy prompt: each newly built applet that runs the wrapper on the `memit` volume blocks until the operator clicks Allow. The stuck process tree after Allow is in `host_runs_maestro12/native2_tree_after_allow_maestro13.txt`; the wrapper opened `tools/backup_gdrive.sh` immediately after Allow. Note: `memory_mirror/native-applet-removable-volumes-prompt.md`.
- Side effect, `host_runs_maestro13/mb14_counter_drift_maestro14.md`: two MB14 fixture applets from ~10:28Z, each with HOME embedded in its receipt fixture, evidently ran their wrapper once more hours later, when an Allow was clicked (counters 10→11 at 16:15Z and 17:20Z). I restored the receipt bytes; the drift is recorded there.

## Check against the code (cite file:line)

1. r4 P1 closed: replay your exact schedule (completed 10; both failure sinks unwritable; absent-wrapper launch 11; restore receipt writability; manual backup running; applet 12 refuses with 75; manual completes). Status must be unhealthy for 11. Also: two refusals in a row; a refusal followed by a successful applet 13. A manual run must never acknowledge an applet failure.
2. r4 P2 closed: from a missing/corrupt counter and null-generation evidence, does `recover --generation-floor N` restore service without erasing or reinterpreting the ambiguous evidence, never lower the floor, and refuse an N below anything observed? Can an operator use it to make an unacknowledged failure read healthy?
3. No regression in r4 findings 2 and 4: generation (not wall-clock) ordering; exit 75 never marks an active owner failed; status never writes `last_run.json`; no applet path can show a dialog; `open -W -g` waits; bounded storage; ownership, `--retries 1`, `--bwlimit '08:00,512k 23:00,off'`, excludes.
4. The Removable Volumes prompt in production. The production applet runs the wrapper on `memit`, so its first launch blocks until Allow. While it is blocked: what does status report, does launchd's `open -W -g` hold the job, and do later scheduled launches pile up or refuse? If an applet launch is released hours late (as the MB14 fixtures were), can its late generation or receipt corrupt ordering, hide a failure, or acknowledge one?
5. Anything else that blocks activation. Restate the ordered activation checklist, placing the operator's one-time Allow for the production applet in its correct position relative to counter provisioning, the first invocation, and loading the plist.

## Output

Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, or generic advice with no named failing input.
