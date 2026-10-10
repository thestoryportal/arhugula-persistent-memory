# GPT-6-Astra (high) — promote review: Google Drive backup build (vanished-source correction)

Read-only. Worktree = current dir, branch `worktree-c10k-route-a`. The changes are uncommitted: `git diff HEAD -- tools/backup_gdrive.sh tools/backup_gdrive_status.py tools/test_backup_gdrive.py tools/test_backup_gdrive_addendum.py`. Already committed in f70a6de and in scope: `tools/archive_to_gdrive.sh`, `tools/launchd/com.rhu.memit-gdrive-backup.plist`, `docs/ARCHIVE_MANIFEST.tsv`. Ignore `tools/test_dashboard_mathlab.py`, which is another session's WIP.

## What this replaces and why
The old job (`com.rhu.memit-backup`) rsyncs the 287 GB `/Volumes/memit/llm-database-poc-mirror/` to the Mac's internal SSD. Operator policy (EXPERIMENT_RUNBOOK.md §3.3a) says the internal SSD is not an archive; Google Drive (`gdrive:`) is the warehouse. The old job's last run (2026-10-09 17:56) logged a false FATAL because rsync exited 24 after a `.git/objects/.../tmp_obj_*` file vanished mid-run. Nothing has run since. The new job runs one `rclone sync` every 6 h, archiving replaced or deleted remote files to `gdrive:memit-backup/.deleted/<stamp>/`.

## Requirements (builder briefs, verbatim source)
- `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb3_gdrive_prompt.txt`
- `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb3_gdrive_addendum.txt`
- Vanished-source steer, from the report's "Successor's concrete next step": a vanished source is a visible warning with deletions suppressed; auth, permission, destination and other transfer failures stay fatal; no `--ignore-errors`; never weaken rclone's deletion barrier; do not edit `tools/backup_mirror.excludes`.

Builder's account and receipts: `results/backup_gdrive_build_report.md`, final section "MB5 vanished-source correction", and `results/backup_gdrive_mb5_20261010T065106Z/`. I reran `.venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive`: 50 tests, OK. A host-side Drive self-test is running separately. Do not judge Drive network behavior, which you cannot reach.

## Check
1. **Data-loss paths.** Can any input make a run delete or overwrite remote data without archiving it to `.deleted/`? Can the wrapper exit 0 or report "fresh success" when the remote is not a faithful mirror, other than the documented source-vanished warning case?
2. **Classifier soundness** (`backup_gdrive.sh` and `backup_gdrive_status.py`). Is promoting raw rclone exit 1 to wrapper exit 0 admitted ONLY for a proven local-source ENOENT? Look for a log shape, path form, or race that turns a genuine failure (auth, quota, rate limit, destination ENOENT, partial upload) into a warning.
3. **Lock and heartbeat.** Can a stale or held lock deadlock the schedule silently, i.e. refuse forever with no visible status? Can two runs overlap? Is the terminal heartbeat published before the lock is released?
4. **Excludes.** Do the four `tmp_obj_*` patterns exclude anything that is not a Git temporary object?
5. **Tests.** Does any test assert a weaker property than its name claims, or pass vacuously?
6. **Activation readiness.** The plist runs `/bin/bash` directly on the main-checkout script. Name every precondition that must hold before `launchctl load`, including the macOS removable-volume / TCC access the old job got through MemitBackup.app.

## Output
Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failure input, and the exact fix. List the activation preconditions separately at the end.

Not acceptable: findings that restate the builder's report, or "consider adding more tests" with no named failing input. If a check finds nothing, write `N. none found — <what you inspected>`.
