# GPT-6-Astra (high) — re-review r3: Google Drive backup (launcher + status)

Read-only. Worktree = current dir. Your r2 verdict (`results/backup_gdrive_host_20261010/astra_r2_verdict.md`) was NO-GO on finding 5 (P1: the applet's `try … end try` hid pre-wrapper failures) and finding 6 (P2: refusal receipts grew without bound). Findings 1–4 were closed and 7–8 clean; finding 9 listed host checks and activation conditions.

The builder's fix is committed at 0ab0c42. Read the section "MB8 Astra r2 findings 5 and 6" at the end of `results/backup_gdrive_build_report.md`, and the receipts in `results/backup_gdrive_mb8_20261010T082434Z/` (RED/GREEN index `tdd_index_final.json`, `verification_final.json`, `host_maestro5_verification.md`, `host_<case>_*/summary.json`). Changed files: `tools/backup_gdrive.sh`, `tools/backup_gdrive_status.py`, `tools/launchd/MemitGdriveBackup.applescript`, `tools/test_backup_gdrive_addendum.py`. `git diff af8b5da 0ab0c42 -- tools` shows the exact change.

My host evidence, which you cannot reproduce: 72 tests OK with 0 skipped; the 3 LauncherTest tests run natively (real osacompile, no dialog). Real app bundles run through `/usr/bin/open -W -g`, with `host_launcher_checks.py`:
- long stub: held for 3.61 s;
- exit 75 with a live owner: 0.48 s, owner heartbeat byte-identical, status incomplete;
- absent volume path: 0.49 s, receipt exit 127, status "failed backup launch" over a seeded fresh success;
- unwritable receipt directory: 0.47 s, prior receipt preserved, no dialog.

## Check against the code (cite file:line)
1. Finding 5 closed: when /Volumes/memit is unmounted, or the wrapper is otherwise unloadable, the next launch leaves a receipt on the internal disk without loading volume-hosted code. Status then reports failure even after a fresh success. Check exit 127, AppleScript errors, and the case where the receipt write itself fails.
2. Status precedence: a newer failed launch overrides an older success; a completed newer heartbeat recovers; exit 75 never marks an active owner failed; malformed or future receipts fail closed; status never writes `last_run.json`. Look for clock-skew or same-second orderings that misclassify.
3. Finding 6 closed: one atomically replaced latest-refusal receipt; the 1,000-refusal test holds a real live owner. Ownership, lock recovery, `--retries 1`, the `--bwlimit '08:00,512k 23:00,off'` timetable and the excludes are unchanged.
4. Applet: no code path can display a dialog, including a receipt-write failure inside the error handler. The plist chain `open -W -g` still waits for the wrapper.
5. Anything else that blocks activation. Restate finding 9's activation conditions as an ordered checklist: the operator's one-time Removable Volumes grant first, then install, load and kickstart, then a fresh heartbeat; the old job is retired only after verified full-copy completion.

## Output
Under 600 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, or generic advice with no named failing input.
