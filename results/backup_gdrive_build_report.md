# Google Drive backup build — 2026-10-10 (Codex MB3)

**Code prepared; local verification PASS; Drive verification BLOCKED by sandbox DNS.** Operator authorization: MAESTRO3's prompt (saved in `backup_gdrive_build_20261010T055855Z/prompt.txt`) and runbook §3.3a. `gdrive:` exists in rclone v1.75.2; the earlier successful authorization/write probe is MAESTRO3's evidence. This session cannot resolve `www.googleapis.com`. The requested real-source dry run exited **1**, before a transfer plan was available. Drive create/modify/delete, upload rate and first-upload duration are **UNVERIFIED / UNMEASURED**. This is not full build acceptance or activation clearance.

## Delivered behavior

- `tools/backup_gdrive.sh`: exactly one rclone sync per run from `/Volumes/memit/llm-database-poc-mirror/` to `gdrive:memit-backup/llm-database-poc-mirror/`, archiving replaced/deleted destination files to sibling `gdrive:memit-backup/.deleted/<UTC-stamp>-<PID>/`. Original mounted/nonempty source checks and unchanged `backup_mirror.excludes` are retained. Symlinks use rclone `--links`; Drive stores its link representation for a later `--links` restore. Failure returns nonzero and identifies the log.
- Default log: `~/Library/Logs/memit-gdrive-backup.log`; atomic mkdir lock: `~/Library/Logs/memit-gdrive-backup.lock`. Held/unknown/stale locks refuse with a logged exit 75. **No age-based auto-expiry.** Recovery requires checking both recorded owner and rclone PID have stopped, then removing only that lock. Interruption conservatively retains it while a child may still run; completed failure/success releases it.
- Overrides: `BACKUP_SRC`, `BACKUP_DEST`, `BACKUP_EXCLUDES`, plus `BACKUP_LOG`, `BACKUP_LOCK_DIR`, `BACKUP_MOUNT_POINT`, `BACKUP_RCLONE`. Choose a destination directory below its backup parent: Drive self-test uses `_selftest/mirror`, so its sibling archive remains entirely inside `_selftest/.deleted`.
- `tools/launchd/com.rhu.memit-gdrive-backup.plist`: interval **21600 s**, RunAtLoad false, direct Bash main-checkout path, logs under `~/Library/Logs`, low-priority IO/Nice 5. No job loaded/unloaded. **Host activation is unverified:** the existing job uses MemitBackup.app's Removable Volumes grant; that grant does not establish direct Bash access. MAESTRO3 must deploy the reviewed main-checkout script and validate the new launcher's macOS access before replacing the old job.

## Evidence

`backup_gdrive_build_20261010T055855Z/` contains exact outputs and baseline/hash audit. Test command: `PYTHONDONTWRITEBYTECODE=1 python3 -B tools/test_backup_gdrive.py`. Before implementation: **8 failures** (`red.txt`, missing wrapper/log behavior). Real-rclone local backend then proved three runs (create, modify, delete), archived original/replaced content, unchanged exclude behavior, symlink preservation, held/stale lock refusal, missing/unmounted/empty-source refusal and nonzero/logged real-rclone failure. The initial link assertion was corrected after a standalone positive control showed the local backend restores native symlinks; production code was unchanged for that correction.

Secondary review found a self-test timeout race: killing only Bash could leave rclone writing while source cleanup/purge ran. A controlled child heartbeat reproduced this **RED** (`timeout_red.txt`). The runner now starts an independent process group, kills the entire group on timeout and drains/reaps before cleanup. **Final: 9 tests PASS** (`green_final.txt`); Bash/Python syntax and plist lint PASS. GPT-6/Codex-family read-only review: **PROCEED for code preparation only**, not activation/full sync (`review.txt`). No science/dashboard tests were run; this change is confined to backup tooling.

Exact real-source dry-run attempt:

```sh
/opt/homebrew/bin/rclone sync /Volumes/memit/llm-database-poc-mirror/ gdrive:memit-backup/llm-database-poc-mirror/ --backup-dir gdrive:memit-backup/.deleted/DRY-RUN/ --exclude-from tools/backup_mirror.excludes --links --dry-run --contimeout 10s --timeout 30s --retries 1 --low-level-retries 1 --use-json-log
```

`dry_run.jsonl`: DNS lookup failure; **exit 1**, no verified dry-run file count/bytes. Independent read-only local inventory (`source_inventory.json`), with identical excludes and link policy: **40,388 files / 287,160,929,446 bytes = 287.16 GB / 267.44 GiB**. These are source candidates, not the real-destination transfer plan. One runtime Unix socket is unsupported and skipped (`source_inventory.stderr`); no bulk/science file error was reported. No first-upload estimate is inferred without measured bandwidth.

## Remaining bounded host verification / handoff to MAESTRO3

Run from this worktree in a host environment with Drive DNS, after code review:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/test_backup_gdrive.py
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/test_backup_gdrive.py --drive
```

The explicit `--drive` runner creates a fresh `results/backup_gdrive_drive_<UTC>/` receipt, performs three tiny syncs into `gdrive:memit-backup/_selftest/mirror`, verifies archived bytes/exclusions and held-lock/unmounted/empty-source refusal, uploads **one 200,000,000-byte random file** into `_selftest`, measures wall time and remote size, and runs the **real source to real destination with --dry-run only**. It derives planned count/bytes from the combined dry-run changes plus a filtered source size listing. Duration = planned bytes / measured bytes-per-second; small-file/API overhead and concurrent source churn remain outside that projection. Temporary local disk budget: about 200 MB. No full backup is dispatched. After remote effects it calls `rclone purge` only on the exact authorized `gdrive:memit-backup/_selftest/` path; cleanup failure is fatal and recorded. The sandbox opt-in attempt failed its read-only preflight before any remote writes (`backup_gdrive_drive_20261010T060419Z/summary.json`), so there was no remote self-test data to clean up here.

Next: obtain the host receipt; confirm all remote checks and exact cleanup PASS; record actual dry-run transfer count/bytes, upload rate and duration here. Then MAESTRO3 reviews deployment/TCC and replaces the old launchd job. Pending host-runner information was requested; no runner was supplied during this build. Do not claim `GDRIVE BACKUP BUILD DONE` until these required measurements pass. No commits, full sync, launchd mutation, `~/Backups/memit` access or `tools/test_dashboard_mathlab.py` edit by this task. Old script/excludes/plist are unchanged.

**BINDING context directive:** Watch your own and every orchestrated team's `Context N% left`. Before approximately **20%**, stop starting new work; write a report handoff with what is done/in-flight, exact paths, next steps and open risks; tell the orchestrator to use a fresh successor. Every handoff restates this rule; never approach full-window compaction.

Primary flag references: [rclone backup-dir](https://rclone.org/docs/#backup-dir-dir), [rclone links](https://rclone.org/docs/#l-links), [sync exclusions/error behavior](https://rclone.org/commands/rclone_sync/). Empirical local and failed-Drive evidence above takes precedence over assumptions about deployment.

## Final local audit — 2026-10-10T06:15:03.566792+00:00

Protected old script, excludes, old plist and dashboard test SHA-256 values match the task baseline. Scoped `git diff --check` passes. `audit.json` records the five deliverable hashes; `git_status.txt` and `git_log.txt` preserve observed shared-worktree state.

Baseline HEAD `522929f6d7017f0e8b7b54e2d559d4135d9f99a2`; observed HEAD `cbe1ac28a23feeab952eb9f9fd4f4740b3739be0` on `worktree-c10k-route-a`. The shared HEAD advanced concurrently; this task performed no commits or mutating Git commands and preserved parallel changes. Drive validation remains BLOCKED; no additional remote effects were attempted.

## MAESTRO3 addendum — 2026-10-10T06:33:10.745313+00:00

**Addendum code prepared; 29 local behavioral tests PASS; required Drive verification remains BLOCKED by sandbox DNS.** The full instructions are saved at `backup_gdrive_addendum_20261010T061642Z/addendum.txt`. This section supersedes the earlier wrapper logging/status details. No launcher activation, full sync, operator bulk deletion, LAW-gate edit, dashboard-test edit or commit was performed.

### A. Heartbeat and loud status

`tools/backup_gdrive.sh` now atomically publishes `~/Library/Logs/memit-gdrive-backup/last_run.json` at start and exit. Fields: `start`, `end`, `exit_code`, `bytes_transferred`, `rclone_version`, run identity and log references. Publication uses a same-directory temporary file, fsync and rename. The existing wrapper log remains `~/Library/Logs/memit-gdrive-backup.log`; each rclone invocation writes a separate JSON log under `~/Library/Logs/memit-gdrive-backup/runs/`. Transferred bytes come from rclone's actual JSON accounting stats, with a final NOTICE-level stats record; absent/malformed stats remain **null / unknown**, never an invented zero. Refusals that do not dispatch record zero transferred bytes. `BACKUP_HEARTBEAT` isolates tests and can override the fixed receipt path.

`tools/backup_gdrive_status.py` defaults to that heartbeat, with `--heartbeat <path>` for tests. It returns **0 only for a completed successful run whose end is strictly less than 13 hours old**. Missing, torn/malformed, incomplete, failed, future and stale records return nonzero with one line. Token/auth error patterns in the current run log return nonzero; old auth failures do not poison recovery. Wrapper-log inode/byte-offset checks reject rotation/truncation and detect a newer `HEARTBEAT-FAILED` diagnostic if publication failed and an older successful heartbeat remains. Publication failures are logged and force nonzero while preserving an existing rclone failure exit code. SIGKILL cannot write an end receipt; its previously published start remains INCOMPLETE.

Closeout publishes the terminal receipt **before releasing the owned mkdir lock**, preventing an older success from replacing a newer active run's heartbeat. A cleanup error is republished as failed while the remaining lock still blocks dispatch. The existing mounted/nonempty/exclude/archive contract and exactly one sync are retained.

**Proposed wiring, source inspection only (no LAW gates changed):** the actual session hook `.codex/hooks/session_start.py:17–23` invokes `tools/codex_context_guard.py preflight` at line 19 and propagates hard failure. `tools/codex_context_guard.py:78–105` already prints HARD/WARN readiness facts. Add a separate status invocation in the session hook before that preflight and visibly print `BACKUP WARN: <one-line reason>` on nonzero. Once the new backup is deployed and its first successful receipt exists, a queue/launcher wrapper can refuse bulk-producing dispatch on nonzero before entering frozen admission. The existing pre-dispatch boundary is `tools/mathlab_admit.py:76–99` (`dispatch_check`), which re-probes admission at 95 and refuses at 98; the status invocation belongs in its calling launcher/queue wrapper, with explicit stderr and exit handling, rather than a change to frozen LAW/science gates. These are **proposals only**; backup health is not wired into dispatch yet, and the stopped MathLab study remains stopped.

### B. Verified archival and manifest

`tools/archive_to_gdrive.sh <file...>` admits regular files under the resolved repo root, maps each to `gdrive:memit-archive/<repo-relative path>`, copies via rclone, then runs **`rclone check --download --one-way`** before appending `sha256`, `size_bytes`, `remote_path` to `docs/ARCHIVE_MANIFEST.tsv`. SHA-256 and size are recomputed after verification; source drift refuses the receipt. Manifest appends hold a file lock and fsync. All arguments are admitted before any copy; directories, path escapes, final symlinks and TSV-breaking path names refuse. The tool **never removes local source files**. Identical remote content may be verified again; differing existing content is preserved and fails verification without a new manifest row. Overrides `ARCHIVE_ROOT`, `ARCHIVE_DEST`, `ARCHIVE_MANIFEST`, `ARCHIVE_RCLONE`, `ARCHIVE_PYTHON` support bounded tests. The default manifest contains only its header; no unverified real archive receipt was fabricated. MAESTRO3 must include this new file in the reviewed Git commit to make it git-tracked.

**Empirical collision finding:** installed rclone v1.75.2's single-file `copy --immutable --checksum` replaced differing local-backend content (`immutable_probe.json`, initial collision control RED). A separate actual-rclone probe demonstrated `--ignore-existing` preserves the original (`immutable_flags_probe.json`); the production copy now also supplies that flag. Its subsequent download check accepts matching content and rejects differing content, with the prior object and prior manifest preserved. This is the tested behavior of this installation; no claim is made that every rclone/backend has the same single-file immutable behavior. Primary semantics reference: [rclone ignore-existing](https://rclone.org/docs/#ignore-existing).

### RED / GREEN evidence and limits

Exact CPU/local commands (temporary roots only):

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B tools/test_backup_gdrive_addendum.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B tools/test_backup_gdrive.py -v
```

`backup_gdrive_addendum_20261010T061642Z/red.txt`: **18 failures before implementation**. `green_first.txt`: 17 pass plus the real collision refusal failure; corrected with the independently probed non-overwrite flag. `terminal_race_red_v2.txt`: **1 genuine RED** showing status returning fresh success during a marker-confirmed newer active sync. After serializing publication and adding the cleanup-error control, `green_final_v2.txt`: **20 PASS / 4.897 s**. `original_regression_final.txt`: **9 PASS / 7.060 s**. Syntax checks, embedded archive Python compilation and unchanged new plist lint PASS. The original slow-child fixtures now answer `version` immediately so they still test sync interruption/timeout; all backup test heartbeats are namespaced under temporary/receipt roots rather than the operator's home.

Controls cover fresh/stale/exact-13h/failed/missing/torn/future/in-flight status, current versus old auth errors, log rotation, start/exit publication failure after prior success, exit-code preservation, actual stats, unknown stats, overlap serialization, lock-cleanup failure, real copy/download/SHA receipt, remote collision/corruption, source drift, manifest write failure and path admission. No model, tensor, science or dashboard tests were needed for these backup-only changes. GPT-6/Codex-family read-only review resolved the overlap blocker and returned **PROCEED, code-only**; Drive behavior/activation remain UNVERIFIED.

The explicit tiny archive test is available as:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B tools/test_backup_gdrive_addendum.py --archive-drive
```

It creates one tiny temporary file, invokes the real archive helper into **`gdrive:memit-archive/_selftest/`**, checks its SHA/size/path manifest and local preservation, and purges **that exact remote path only** after any attempted remote effect. Its sandbox attempt exited **1** at read-only Drive preflight (`backup_gdrive_archive_20261010T062753Z/summary.json`, plus `archive_drive_attempt.txt`): DNS cannot resolve `www.googleapis.com`; **no Drive writes were attempted**, hence no purge was needed. The existing backup `--drive` runner now keeps its heartbeat in its receipt directory and retains group timeout protection. Required real-source dry-run size and measured 200 MB upload estimate remain UNMEASURED; the earlier local inventory remains **40,388 source files / 287,160,929,446 bytes**, not a destination transfer plan.

### File identity

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `1c787df5cbacc4e10939d94b3194f52ba52bb0bfd83e61779affd92745209cc8` |
| `tools/backup_gdrive_status.py` | `4e7f695cc529c101417db1f78b0050a93a0881e7129f7ce8c02446cc99581cf4` |
| `tools/archive_to_gdrive.sh` | `efcade80c90afec3b71224130b3e1b38a104164a3b7c90f5670f410e6f92475d` |
| `tools/test_backup_gdrive.py` | `0650b6c4f42624041e94c8642ff03f827a5b1de58e08662d18c69e036c995f90` |
| `tools/test_backup_gdrive_addendum.py` | `5ae76e866fa94df72f6d3b72db961875ae48e655e8854183f1f6d14e21d6caa3` |
| `docs/ARCHIVE_MANIFEST.tsv` | `c4e7c4e611c0e15f0dfbaa473bcb934ef737fbf49330c00afd9dd1ed8828cee3` |
| `tools/launchd/com.rhu.memit-gdrive-backup.plist` | `55aec0d1f7a3b7158c65f81c55363fc344be2506458c578e164a74cb337522de` |

### Current handoff

Done: heartbeat/status and archive/manifest implementation; 29 local tests; RED controls and code-only review. Receipts: `results/backup_gdrive_addendum_20261010T061642Z/`, original backup receipts `results/backup_gdrive_build_20261010T055855Z/`. In flight: none. Next: a legitimate host with Drive DNS runs both `tools/test_backup_gdrive.py --drive` and `tools/test_backup_gdrive_addendum.py --archive-drive`, verifies their exact scoped cleanup, records real dry-run count/bytes and upload-rate projection, then MAESTRO3 reviews deployment/access before any job replacement. Do not load/unload launchd, dispatch full sync, delete local bulk or change LAW gates under this build authorization. Existing host-runner inquiry remains unanswered. Backup health wiring remains a proposal; the manifest is prepared for Git but not staged/committed by this task.

**BINDING context directive:** Watch your own and every orchestrated team's `Context N% left`. Before approximately **20%**, stop starting new work; write a report handoff listing done/in-flight work, exact paths, next steps and open risks; tell the orchestrator to start a fresh successor. Every handoff restates this rule; never approach full-window compaction.


## Vanished-source correction — RED evidence and context handoff — 2026-10-10T06:47:13.920419+00:00

**INCOMPLETE: tests written first and RED; production correction has not been implemented.** MAESTRO3 reports that the internal-SSD backup's last logged run (`~/Backups/memit/backup.launchd.log:86–96`, 2026-10-09 17:56) was marked FATAL solely for rsync exit 24 after a `.git/objects/.../tmp_obj_*` source vanished, with no subsequent logged run. This is operator-provided evidence; this task did not read or modify `~/Backups/memit`.

### Measured rclone equivalent

A bounded actual-rclone v1.75.2 local control queued two temporary files with `--check-first --order-by name --transfers 1 --disable Copy --bwlimit 256k`, waited for the first destination transfer to appear, then removed only the queued temporary second source. `results/backup_gdrive_vanished_20261010T063803Z/vanished_probe.json` and `probe_rclone.jsonl` record **raw exit 1**, the intact first-file copy, `Failed to copy: failed to open source object: lstat <source>/z_vanished.bin: no such file or directory`, final stats `errors=1`, `fatalError=false`, `retryError=true`, and terminal NOTICE `Failed to sync: ...`. Rclone also reported **not deleting files/directories as there were IO errors**. This installation uses a general exit 1 for this case; rsync's 24 must not be translated into a blanket rclone success rule. [Primary rclone exit-code reference](https://rclone.org/docs/#list-of-exit-codes).

A proven vanished-source outcome must be a visible **source vanished; deletions suppressed** warning, with raw rclone exit retained. It cannot be described as an exact completed mirror. Genuine auth, permission, destination and other transfer failures must remain fatal. Do not use `--ignore-errors` or weaken rclone's deletion barrier.

Actual Unix-socket fixture creation was sandbox-denied (`socket_fixture.json`, `Operation not permitted`); this is UNVERIFIED. The new test instead uses a temporary FIFO to exercise rclone's generic `Can't transfer non file/directory` NOTICE. The earlier full source inventory independently recorded this NOTICE for one runtime socket. A regular file named `ordinary.sock` must remain included; a blanket `*.sock` filter would hide valid data.

### RED evidence

Exact command: `LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/test_backup_gdrive_addendum.py -v`. `results/backup_gdrive_vanished_20261010T063803Z/red.txt`: **27 tests / 11.566 s; 23 PASS, 4 FAIL; exit 1** on unchanged production. Seven new test methods plus helpers were added to `tools/test_backup_gdrive_addendum.py`. The four intended failures prove: `.git` temporary objects are copied; a nonregular skip is absent from heartbeat warnings; the real queued-source vanish is falsely FATAL/exit 1; and status hides a supplied warning behind “fresh successful backup.” Negative controls for mixed auth/permission/destination ENOENT, ambiguous or still-present source, missing/torn final log evidence, path escape, and raw non-1 exit already PASS. Original lock, publication-failure, auth and archive controls also PASS in this run. The earlier 29-test GREEN predates this steering and does not establish the requested correction.

Read-only GPT-6/Codex-family helper review (not Astra) agreed to this narrowly scoped RED plan (`review_red_plan.txt`). Binding MAESTRO3/Astra review is still required after implementation.

### Successor's concrete next step

1. Read both full briefs: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb3_gdrive_prompt.txt` and `codexmb3_gdrive_addendum.txt`, this report, and the measured receipt/log above. Implement warning classification in `tools/backup_gdrive.sh` / `tools/backup_gdrive_status.py`, preserving exactly one sync and terminal publication before lock release. Normalize wrapper success only for a fully verified local-source-vanish raw-exit-1 case; heartbeat must retain `rclone_exit_code=1`, structured warnings and the deletion-suppression qualification. Require a complete valid per-run JSON log, matching local source/object ENOENT, confirmed absence via `lstat` raising `FileNotFoundError`, consistent nonfatal final stats and matching terminal NOTICE. Reject traversal/mismatched/destination errors, existing or inaccessible sources, unrelated errors, malformed/truncated evidence and other exit codes. Accept the native terminal spelling `Failed to sync: ...` as well as any independently valid count-prefixed form used by synthetic controls.
2. Add a supplemental `--exclude '**/.git/objects/**/tmp_obj_*'` without editing shared `tools/backup_mirror.excludes`. Apply exactly the same filter to the explicit real-source dry-run and filtered source listing in `tools/test_backup_gdrive.py`. Preserve permanent Git objects and regular `.sock` files; record native nonregular skips as visible warnings. Prior source inventory predates this proposed filter.
3. Run the new 27-test addendum suite and original 9-test suite locally, inspect RED/GREEN receipts, syntax and protected-file hashes; get a helper review with the existing lock/publication races in scope, then MAESTRO3's binding Astra review. Append final hashes and warning semantics here. No real full backup, launcher activation, commits/staging, local bulk deletion, LAW-gate changes or dashboard-test edits. `EXPERIMENT_RUNBOOK.md` remains uncommitted for MAESTRO3's reviewed commit.
4. Required Drive tiny-sync/archive controls, real-destination dry-run and 200 MB upload measurement remain **BLOCKED by sandbox DNS / UNVERIFIED**. No host runner was supplied. Do not claim full build acceptance until those bounded host receipts pass.

### Scope and saved state

Worktree verified as `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. Baseline HEAD `a0047f4cbef8154e3931df061482db187150b069`; observed shared HEAD `6aa22ab5990cd5eae9721d1106d6f2c487a02c5b`. No commits or mutating Git operations by this task; concurrent HEAD advance is preserved. Production wrapper/status unchanged since latest baseline: **True**. Protected old mirror script/excludes/plist and dashboard test unchanged: **True**. Runbook unchanged by this steering: **True**. Latest test SHA-256: `43e5fd2830010b4697c269a6f2de81978804824302b25cdb8b5751b274acc91e`. Wrapper SHA-256: `1c787df5cbacc4e10939d94b3194f52ba52bb0bfd83e61779affd92745209cc8`; status SHA-256: `4e7f695cc529c101417db1f78b0050a93a0881e7129f7ce8c02446cc99581cf4`. Current RED process has finished; no work is in flight. Audit and context save: `results/backup_gdrive_vanished_20261010T063803Z/audit_handoff.json`, `context_saved.md`.

**BINDING context directive:** Watch your own and every orchestrated team's `Context N% left`. Before approximately **20%**, stop starting new work; write a task-report handoff listing done/in-flight work, exact paths, next steps and open risks; tell the orchestrator to start a fresh successor. Every handoff restates this rule; never approach full-window compaction. This handoff stops new work before the production correction.


## MB5 vanished-source correction — local build complete — 2026-10-10T07:06:50.820783+00:00

**Authorized Task 1 code correction DONE: 50 local tests PASS (41 addendum + 9 original), 28.425 s, exit 0.** This section supersedes the INCOMPLETE production-correction handoff above. The user's current scope delegates every Drive self-test, remote archive control, real-destination dry-run and upload-rate measurement to MAESTRO3. No Drive call or full sync was attempted in MB5. Remote correctness, transfer count/bytes, first-upload duration, deployment/TCC and launcher activation remain **UNVERIFIED**; this is local build completion, not full backup acceptance.

### Warning and deletion contract

The wrapper still dispatches exactly one sync, preserves rclone's IO-error deletion barrier, and publishes the terminal heartbeat before releasing its owned lock. It classifies the completed child log once, then passes that captured outcome into heartbeat publication; publication does not repeat the source check and silently change its meaning. A raw exit **1** becomes wrapper exit **0 with warnings** only when complete, newline-terminated, strictly valid per-run JSON proves local-source ENOENT: an exact local object/source path under the live source root, no traversal or symlink-parent escape, and current `lstat` FileNotFoundError. A vanished nested parent can qualify while the root remains live; inaccessible, existing/recreated or vanished-root sources cannot.

Every ERROR must be an independently verified source-vanish record, a native files/directories deletion-suppression diagnostic, or an accounted Attempt summary. Each attempt has its own error count. Completion requires final NOTICE stats after the final attempt, nonfatal matching error count/last error, no active transfers, both deletion-suppression diagnostics, and a matching last terminal NOTICE. Native `Failed to sync: ...` and count-prefixed `Failed to sync with N errors: ...` are admitted. Missing/torn/malformed evidence, duplicate JSON fields, NaN/Infinity, mixed auth/permission/destination errors, mismatched paths/counts, incompatible transfer-stat types and non-1 failures remain nonzero/FATAL. Raw `rclone_exit_code` is retained independently, including raw 0 when outcome classification itself fails; wrapper/heartbeat failure then remains nonzero.

Eligible raw-1 heartbeats contain structured `source_vanished` and `destination_deletions_suppressed` warnings. Wrapper logs explicitly say **source vanished; destination deletions suppressed**; fresh status returns 0 with **with warnings** and that qualification. This outcome is not an exact completed mirror. No second sync or delete pass follows it. Destination-only objects remain in place under rclone's barrier; a later successful scheduled sync may move them to the existing timestamped sibling `.deleted/` archive. Successful retries retain source-vanish warnings without claiming final deletions were suppressed. Ordinary successful runs retain archival of replacements/deletions via `--backup-dir`; excluded files are protected because no `--delete-excluded` or `--ignore-errors` is used.

Native nonregular skips are recorded as `nonregular_source_skipped`; other native WARNING messages remain visible as `rclone_warning`. The local FIFO control exercises the skip notice; actual Unix-socket creation remains UNVERIFIED from the predecessor's sandbox refusal. Regular `ordinary.sock` files remain included. Malformed stats remain null/unknown with a warning rather than reusing earlier byte totals. Warning receipt fields are validated, and path newlines are escaped so status stays one line.

### Git temporary-object filter

Installed rclone v1.75.2's actual local `lsjson` probe (`filter_probe.json`) demonstrated that `**/.git/objects/**/tmp_obj_*` alone misses direct objects and source-root `.git` paths. The wrapper retains that requested pattern and adds exactly its three narrow companion forms: `**/.git/objects/tmp_obj_*`, `/.git/objects/**/tmp_obj_*`, and `/.git/objects/tmp_obj_*`. Permanent Git objects remain included. The explicit Drive real-source dry-run and filtered source listing use the identical four forms; their network behavior is still UNVERIFIED. Shared `tools/backup_mirror.excludes` is unchanged, and the predecessor's source inventory predates these filters.

### Test-first evidence and review

All MB5 receipts are under `results/backup_gdrive_mb5_20261010T065106Z/`. `red.txt` reproduced the predecessor's **27 tests / 4 failures** before implementation. `supplemental_red.txt` recorded terminal/status/recovery controls; its initial recovered-field lookup raised a missing-feature KeyError, and the assertion was changed to `.get` before final validation. `green_first.txt` recorded 33 tests with the one genuine direct-Git-object filter failure. `boundary_red.txt`, `review_red.txt`, `status_boundary_red.txt` and `final_boundary_red.txt` preserve each subsequently reproduced parser, raw-exit, measurement, completion-stat, warning-field and missing-parent failure. No failing receipt was overwritten.

Final exact command (`green_final.txt`):

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

**50 PASS, zero failures/errors.** Real local-backend coverage includes create/modify/delete archival, symlinks/exclusions, queued source vanish retaining an existing destination-only file, native FIFO skip, byte accounting, archive download/SHA receipts and collision/corruption refusal. Synthetic adversarial controls cover strict log evidence, both terminal spellings, retry counters, inaccessible/path-escape/dangling-parent/missing-root cases, recovered warnings, malformed receipts, classifier failure, publication failures, overlap serialization, lock cleanup and whole-group timeout. Syntax/embedded archive Python, plist lint and scoped `git diff --check` PASS (`syntax.txt`, final audit below). No model, tensor, science or dashboard suite was run. GPT-family helper review is recorded separately; binding GPT-6-Astra review belongs to MAESTRO3.

### File scope and local handoff

Only the four backup wrapper/status/test files above and this report were edited; fresh evidence/context files were created in the named receipt directory. The ten protected baseline hashes match: archive helper, old mirror/excludes, both plists, dashboard test, CLAUDE.md, AGENTS.md, runbook and archive manifest (`baseline.json`, `audit.json`). The pre-existing dashboard diff was preserved. Baseline HEAD `f69a9a5faf3059b89a39603ce9dff9cb2ed92daf`; observed audit HEAD `11f61e35db4a9945546d5cd41ff2da41fe08e416`; branch remains `worktree-c10k-route-a`. Shared HEAD advances are concurrent work; MB5 performed no staging, commits, pushes, merges, file/branch/worktree deletion, launcher changes or memory_mirror edits. Local test fixture cleanup is confined to temporary roots.

Environment note: RTK was absent from PATH and was located at `/opt/homebrew/bin/rtk`. One environment-required Graft CLI attempt failed before graph execution because its Node interpreter was absent from PATH (exit 127); no graph output was used and no follow-up was attempted.

Done: warning correction, RED/GREEN receipts and scope proof. In flight: final report/context audit only. Next: MAESTRO3 performs binding Astra review, then the authorized host-only `--drive` / `--archive-drive` controls, exact scoped cleanup, real-destination dry-run and upload measurement. Existing activation/TCC review remains a separate step. Task 2 is intentionally unopened until the Task 1 completion reply.

**BINDING context directive:** Watch this session and every orchestrated team's `Context N% left`. Before approximately **20%**, stop starting new work; write a handoff into the relevant task report with done/in-flight work, exact paths, next steps and open risks; tell the orchestrator to start a fresh successor. Every handoff restates this directive; never approach full-window compaction.

Final code SHA-256:

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `d47b5cc52a06a3d9e8da4d2fccae4d1c4a54783dec705d51f4445a7532f71802` |
| `tools/backup_gdrive_status.py` | `1caa8b252ff88eaa3b4c3e5f2bfc7723f41d03d7647c52e5fd13ca3f1d3f8bb9` |
| `tools/test_backup_gdrive.py` | `9a78fd9879d3c45593268723b3d4a4df8556bfa25028eb0f60dbb13065886a62` |
| `tools/test_backup_gdrive_addendum.py` | `ca61197aef612af8b28821e82c59bec0b76744c43fbd5417498e9e325b3d15d9` |

Final helper verdict: **PROCEED, code preparation only** (`results/backup_gdrive_mb5_20261010T065106Z/helper_review.txt`). No blocking code findings remain after the reproduced corrections. Final report/audit/context receipt persisted; no work is in flight for Task 1.


## MB6 Astra r1 and launchd corrections — 2026-10-10T07:58:39.664792+00:00

**Local fix build complete for MAESTRO4 review: 64 tests run, 62 PASS, 2 UNVERIFIED/skipped; exit 0, 47.323 s.** The two skips are actual applet compilation/manifest and behavioral no-dialog verification; they are not PASS. Binding Astra r2, host compilation/no-dialog proof, installation, Removable Volumes/TCC access and actual launchd execution remain host checks. No Drive call, full backup, installation or launchd mutation occurred in MB6. Earlier Drive and launcher observations in `backup_gdrive_host_20261010/HOST_FINDINGS.md` are MAESTRO4 host evidence, not results reproduced here.

Receipts: `results/backup_gdrive_mb6_20261010T072852Z/`. Final local result: `green_final.txt` and `verification_final.json`. Test-by-test RED pointers: `tdd_index_final.json`. Exact acceptance command:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

Addendum: 54 tests (52 PASS, 2 UNVERIFIED). Original: 10 tests (10 PASS). Bash syntax, Python AST parsing, plist lint and scoped diff checks PASS (`syntax_final.json`). Only local storage, tiny fixtures and standard-library Python were used; no model, GPU, science or dashboard suite was run. Disk budget was under 20 MiB. Pre-write free-space observation: 89,665,060 KiB on memit and 207,328,024 KiB under `/private/tmp`, both exceeding the budget plus 20 GiB.

### Changes and behavioral evidence

1. **Astra 1 — history-safe retry policy.** Sync explicitly sets `--retries 1` and `--low-level-retries 10`. The native real-rclone/local regression archives a=v0, uploads v1, makes a queued second file vanish, then changes a to v2 at the first Attempt boundary. Pre-fix retries overwrote archived v0 with v1; the corrected run preserves v0 and leaves the mirror at v1 with source-vanish/deletion-suppression warnings. This is measured local-backend behavior, not a new Drive observation. RED: `red_retry_overlap.txt`; GREEN: `green_final.txt`.
2. **Astra 2 — configuration admission and false-success refusal.** Preflight rejects every inherited `RCLONE_*` variable except the `RCLONE_CONFIG` credential/config-file locator. The installed rclone's local `config dump` validates the selected effective config: exit, nonempty output, JSON and field shape; every remote `global.*` or `override.*` key refuses dispatch. Config values, including OAuth credentials, remain captured privately and are never printed. Inline/on-the-fly connection strings refuse too. Explicit false boolean flags disable dry-run, interactive mode, ignore-errors and delete-excluded; delete-after is explicit. No deletion-barrier override is enabled. Classification and status refuse dry-run/skipped-operation logs even with raw exit 0 and nonzero accounting bytes. Environment, config, connection-string, actual dispatched-argument and log/heartbeat controls have REDs.
3. **Astra 3 — authoritative heartbeat under ownership.** Acquire the mkdir lock and record its owner before publishing start. Start, child-PID refresh and terminal publication occur under that ownership; terminal publication precedes unlock. Non-owners never write `last_run.json`. Held-lock exit 75 gets a separate atomic receipt at `<heartbeat-parent>/refusals/<stamp>.json`; refusal-publication errors use `REFUSAL-RECORD-FAILED`, avoiding false poisoning of an owner's heartbeat. A live-owner test checks byte-for-byte preservation during refusal. The tightened admitted-overlap schedule pauses B at the actual shell command before lock acquisition (after start in the old wrapper), completes A, resumes B, requires B's dispatch marker and live process, then requires non-success/incomplete status. A refused contender can no longer satisfy it.
4. **Dead unfinished runs and publication failure.** Heartbeats record wrapper owner/rclone PIDs. After dispatch a start refresh records the child. Dead recorded processes yield `stale incomplete backup: owner and rclone PIDs are dead`, exit 1. Live-owner, live-child and pre-dispatch owner controls stay incomplete/non-success. No age-based lock expiry was added. A child-PID publication failure now waits/reaps and preserves a genuine raw failure before cleanup; `red_child_publication.txt` reproduces raw exit 23 previously becoming exit 1. Existing publication-failure assertions remain intact.
5. **Astra 6 — per-attempt proof.** Each Attempt boundary requires both files and directories deletion-suppression records. The retry-evidence test supplies Astra's exact negative input removing both first-attempt records, each individual record, and both final-attempt records; all remain FATAL/nonzero. The admitted-overlap test above closes the other overstated test's missing schedule.
6. **Launcher.** `tools/launchd/MemitGdriveBackup.applescript` wraps `/bin/bash /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh` in `try ... end try`, with no dialog-producing error handler. Executable `tools/launchd/build_gdrive_applet.sh <output.app>` refuses existing bundles, invokes `/usr/bin/osacompile`, and prints each regular bundle file's SHA-256. The plist invokes `/usr/bin/open -W -g /Users/robertrhu/Applications/MemitGdriveBackup.app`, retaining interval 21600 and RunAtLoad=false. Parsed plist behavior PASS. Actual applet build/manifest and no-dialog execution are **UNVERIFIED** below.
7. **Concurrent binding operator update.** During MB6 the runbook was committed with D-C10r-rulings-15: “Slower by day, full at night” means exact `--bwlimit '08:00,512k 23:00,off'`. The wrapper now passes that setting. Its added regression records the actual dispatched argv and completes a tiny real local sync; `red_upload_timetable.txt` proves its absence before the fix. The old host 69-hour payload estimate predates this timetable; no new duration or daytime rate measurement is claimed.

Primary flag references: [rclone retry semantics](https://rclone.org/docs/#retries-int), [remote global overrides](https://rclone.org/docs/#adding-global-configuration-to-a-remote), [configuration precedence](https://rclone.org/docs/#environment-variables). Local fixtures and exact host receipts bind over documentation assumptions.

### Applet boundary — UNVERIFIED, exact observations

The no-dialog test writes an exit-1 shell stub with a marker, substitutes it into the actual AppleScript, attempts compilation, and requires osascript exit 0 within 5 seconds plus the marker. Compilation prevented that execution: no successful stub invocation or prompt-free completion is claimed. The builder's bundle-manifest assertions were also not reached.

Actual source and exit-1 variant: osacompile exit 1, `:3: error: Expected end of line but found identifier. (-2741)`. Independent `do shell script "/usr/bin/true"` compilation/execution also failed: `A identifier can’t go after this identifier. (-2740)`. Basic `return "control"` compiled and executed successfully. Explicit AppleScript language and `use scripting additions` did not restore shell terminology. The independent raw Standard Additions command `osascript -e '«event sysoexec» "/usr/bin/true"'` returned exit 1:

```text
Connection Invalid error for service com.apple.hiservices-xpcservice.
Error received in message reply handler: Connection invalid
0:32: execution error: "/usr/bin/true" doesn’t understand the “«event sysoexec»” message. (-1708)
```

Exact command/stdout/stderr records, timestamps and PIDs are in `osa_probes.json`, `osa_terms_probes.json` and the two UNVERIFIED lines of `green_final.txt`. System-log inspection returned exit 64, `log: Cannot run while sandboxed` (`osa_log_probe.json`). The observed boundary is unavailable Standard Additions/HIServices in this execution context; the precise underlying denial was not observable. Parser errors alone do not skip tests: the independent service-connection failure is also required, and parser failures remain failures when that control works. No fake compiler, osascript result or bundle was substituted. MAESTRO4 must compile and run the exit-1 variant outside this sandbox before claiming no-dialog behavior or activation readiness.

### Test-first audit and file scope

All **14 new tests** and **3 tightened tests** have assertion-based RED receipts. `red_behavior.txt` covers the broad pre-fix failures; `red_retry_overlap.txt` supplies corrected native retry/admitted-overlap REDs; `red_child_publication.txt` covers reaping; `red_upload_timetable.txt` covers the late operator directive. `red.txt` was an initial test-string quoting SyntaxError and is excluded from RED proof. A first retry observation raced the native move of the original destination; a first overlap setup gave sourced Bash the wrong `$0`. Both test fixtures were corrected before production changes without reducing their outcome assertions. `green_first.txt` preserves publication-window and OSA failures; `green_publication.txt` verifies focused wrapper corrections; `green_second.txt` is the earlier 63-test run; `green_final.txt` is final acceptance after the upload timetable.

Only the seven code/test/launcher files below plus this appended report section were changed. Evidence/context files are in the named receipt directory. The excludes, old mirror, archive helper/manifest, CLAUDE.md, AGENTS.md and dashboard test baseline hashes match. The runbook hash changed concurrently in committed D-C10r-rulings-15; its working tree is clean (`scope_drift.json`). MB6 did not edit it or revert that progress. Baseline HEAD `b19a45664f0cc26548a6c93a8f85251833c46789`; observed HEAD `b0ee185fea0dec62f93519a5f23125aaa46f4f6d`; branch `worktree-c10k-route-a` remained unchanged. No Git mutation, repo file/branch/worktree deletion, dependency installation, Drive/full-backup call, launcher activation or memory_mirror edit occurred. One higher-priority environment-required graft lookup failed before execution because Node was absent from PATH; no graph output was used. Subsequent shell work used `/opt/homebrew/bin/rtk proxy`.

Final code/test SHA-256:

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `b5aece49ae0f182520aa49f0c7cac8db09768c15d5212f4985c4295d04e49be7` |
| `tools/backup_gdrive_status.py` | `f7a5d933f37a928f2c0781190c43dc56a6e9ac0726beaa0d5403ddfd8f31adcd` |
| `tools/launchd/com.rhu.memit-gdrive-backup.plist` | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce` |
| `tools/test_backup_gdrive.py` | `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` |
| `tools/test_backup_gdrive_addendum.py` | `931588de4391e1ba1ef46adc6b9a446750dbc3567b043cc0f6516e470a8103f4` |
| `tools/launchd/MemitGdriveBackup.applescript` | `000784725e5180bca488bfc75b4752551630f54c82c0874fd261605c7b83f4c4` |
| `tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` |

`audit.json` and `SHA256SUMS.txt` include final hashes for every changed file, including the report itself; its hash is external to avoid self-reference. `context_saved.md` saves state within the authorized receipt namespace rather than out-of-scope home state.

Done: scoped local corrections, all available checks, RED/GREEN/hash/scope/context receipts. In flight: none. Next: MAESTRO4 obtains binding Astra r2, builds the host applet and verifies its manifest and exit-1/no-dialog behavior, deploys reviewed main-checkout files and performs authorized Removable Volumes/launchd checks. No binding GO, Drive correctness guarantee or activation acceptance is claimed.

**BINDING context directive:** Watch this session and every orchestrated team's Context N% left. At approximately 20% remaining, stop starting work; write done/in-flight work, exact paths, next steps and risks into the task report; notify MAESTRO4 to use a fresh successor. Restate this directive in every handoff; never approach full-window compaction.


## MB8 Astra r2 findings 5 and 6 — 2026-10-10

**Local R2 fix build DONE: 72 tests run, 70 PASS, 2 UNVERIFIED/skipped, exit 0, 108.950 s.** All eight new tests have saved, assertion-based REDs. Binding Astra r3 and host launcher/activation checks remain with MAESTRO5. This infrastructure preserves the F1 evidence/storage boundary; no science run or new scientific claim.

Receipts: `results/backup_gdrive_mb8_20261010T082434Z/`. `verification_final.json` records acceptance and both 1,000-invocation timings; `tdd_index_final.json` maps each new test to RED/GREEN. Exact acceptance:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

### Finding 5: internal-disk launch receipt and read-only status

The applet embeds two shell literals. `launchShell` synchronously runs Bash against the wrapper and captures its actual exit. `receiptShell` is independently executable with `/bin/sh`: it writes `$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json`, containing schema, microsecond UTC, wrapper path, exit code or AppleScript error number. The receipt writer uses only internal `/bin` and `/usr/bin` tools: mkdir, mktemp, Perl with bundled JSON::PP/Time::HiRes/POSIX, mv and trap cleanup. It never sources, reads or executes the wrapper or any volume-hosted helper. The receipt is encoded as JSON and replaced with same-directory temp + mv, preserving quoted/backslash paths and one bounded final file. Microseconds avoid a later failure comparing older than a heartbeat written within the same second.

Wrapper nonzero exits, including 127 for an absent path and 75 for a held lock, are recorded without raising an applet shell error. AppleScript errors use the independent receipt-only path. Both that path and receipt-write errors are caught, with no dialog-producing handler. **AppleScript/app-bundle execution is UNVERIFIED** here; the shell execution evidence does not prove native applet behavior. `launch_shell.sh` and `receipt_shell.sh` are inspection copies extracted from the applet literals, not runtime dependencies.

Status reads the sibling launch receipt and never writes `last_run.json`. A strictly newer failed launch takes precedence over the last heartbeat's end (or start while incomplete); a completed newer/equal heartbeat recovers from older launcher evidence. Exit 75 remains a refusal and leaves a real active owner in flight. A success launch receipt alone cannot make an incomplete/failed backup healthy. Malformed/future receipts fail closed. Tests preserve heartbeat bytes across launch errors, receipt writes, status reads and active-owner exit-75 refusal.

`red_launch_status.txt`: seven tests fail against the original launcher/status, including fresh success + actual absent-wrapper invocation still reporting success, and no receipt for successful launches. `green_launch_status.txt`: all seven PASS after the fix. The receipt-only AppleScript-error regression executes the embedded writer with error -1708 and proves the supplied wrapper was never executed. The unwritable-directory regression executes real shell receipt logic, requires prompt nonzero, preserves the old receipt/heartbeat and leaves no temporary file. Neither regression greps AppleScript for try/on-error/mv as behavior proof.

### Finding 6: one latest refusal receipt

Non-owners atomically replace `<heartbeat-parent>/refusals/latest-refusal.json` using the existing fsync/rename recorder. One latest receipt preserves the current refusal/run identity with constant storage and needs no ring index or retention loop. Ownership, lock recovery rules, owner heartbeat, retry flags, excludes and upload timetable are unchanged. Historical files are preserved; this build performs no historical receipt deletion.

| Evidence | Actual Bash refusals | Wall seconds | Refusal files | Total heartbeat-directory files | Total bytes |
|---|---:|---:|---:|---:|---:|
| `red_refusal_stress.txt` | 1,000 | 58.003 | 1,000 | 1,002 | 512,414 |
| `green_final.txt` | 1,000 | 60.141 | 1 | 3 | 1,010 |

Both runs held the lock in a **real live wrapper**, with its dispatched child blocked on a local FIFO. The test checks the owner remains alive, its heartbeat is byte-for-byte unchanged, and status stays incomplete/in flight. RED fails at 1,000 refusal files versus the required bound of one; GREEN passes every assertion. The count was never reduced; both 1,000-run timings are below two minutes. Runs were foreground and used only local stubs/storage. All 54 existing addendum test methods are AST-identical; the original ten-test module is unchanged. No test was removed or weakened.

### MAESTRO5 host checks — UNVERIFIED, one copy-paste list

The acceptance suite again observes osacompile exit 1 at the Standard Additions command (`(-2741)`), plus an independent osascript raw-event control failing with `com.apple.hiservices-xpcservice` / `Connection invalid` / error -1708. Exact observations are in the two skipped lines of `green_final.txt`. Compilation, bundle manifest and native no-dialog completion are not claimed PASS. The plist remains `/usr/bin/open -W -g /Users/robertrhu/Applications/MemitGdriveBackup.app`, StartInterval=21600, RunAtLoad=false.

`host_launcher_checks.py` is a **prepared host-only helper, AST-checked but not executed here**. It compiles actual app bundles on the internal disk and invokes exactly `/usr/bin/open -W -g <bundle>` with no osascript substitute. Only the wrapper-path and isolated internal HOME literals vary; the applet executable body is the reviewed source. It preserves its fixtures/bundles, hashes the bundle, logs the full command and writes `host_<case>_<UTC>/commands.json` and `summary.json` alongside these receipts. It never installs into Applications or changes launchd. The absent case uses a nonexistent `/Volumes/memit-mb8-absent-.../backup_gdrive.sh` namespace, without unmounting the working volume. A timeout or failed assertion is FAILED, never a skip/PASS; a timed-out app may need host inspection.

Run outside the Codex sandbox from this worktree, before activation:

```sh
# Finding 9: open -W must stay live while the 3-second stub runs, then await its completion.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py long
# Finding 9: exit-75 stub must exit promptly and keep the live owner's status/heartbeat intact.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py exit75
# Absent volume path: open -W -g must exit promptly, write exit 127, and override seeded fresh success.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py absent
# Receipt-write refusal: the native applet must still exit promptly without an error dialog.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py writefail
# Existing native compiler/manifest and caught exit-1 checks: all three must actually PASS on the host.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.LauncherTest -v
```

Astra finding 9's TCC/activation conditions remain: the operator's initial Removable Volumes grant must complete before unattended activation and before demanding a fresh kickstart heartbeat. Host helper receipts do not grant production TCC or prove actual launchd activation. MAESTRO5 owns binding Astra r3, reviewed merge/deployment, production applet grant, authorized job checks and eventual full-copy verification; retire the old job only after verified full-copy completion. No activation GO is inferred from this build.

### Final scope and hashes

Bash/sh syntax, Python AST, parsed plist and scoped diff checks PASS (`syntax_final.json`). Disk budget was under 20 MiB; baseline free space was 91,809,222,656 B on memit and 212,276,322,304 B internally, exceeding budget + 20 GiB. No Drive/network/model/GPU call, dependency installation, commit/push/merge, Applications installation, launchd mutation or repo deletion was performed. The mirror excludes, old mirror, archive helper, CLAUDE.md, AGENTS.md, runbook, memory_mirror and dashboard test remain at baseline hashes. Other builders changed `results/mathlab_staging/new1_construction_diag_scope.md`, `tests/test_git_automation.py`, `tests/test_new1_construction_diag.py`, `tools/dashboard_experiment.py`, `tools/git_hygiene.py` and `tools/git_merge_gate.py` concurrently; their before/after hashes are recorded in `scope_drift.json` and no change was reverted. Branch and HEAD remained `worktree-c10k-route-a` / `5620b948ea6f88d6efcb352ebce32d8cadfef816` at this audit. One environment-required graft lookup failed before execution (Node absent); no graph output was used.

Final changed code/test SHA-256:

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `506ce31845bcbe812261ce128f2119f247cfe270e69b8af08e9a612207aed9ce` |
| `tools/backup_gdrive_status.py` | `f5c98ad6adb3530ac215befbfcedc94a63368a9d153186864f67823db7c40b25` |
| `tools/launchd/MemitGdriveBackup.applescript` | `ebafee3ad82a4376ec5dda0fbc823f2170c795cddd56d62f5ede730d6d5c3bab` |
| `tools/test_backup_gdrive_addendum.py` | `efa0c4e8047279bafe4dd04cfabb2b7839ff68ea012618f93b53cfd44785d985` |

The report's final SHA-256 is recorded externally in `SHA256SUMS.txt` and `audit.json` to avoid self-reference. Those receipts include hashes for all seven reviewed code/test/launcher inputs, the appended report and prepared host helper. The preexisting report bytes are preserved exactly; this section is appended.

Done: local P1/P2 corrections, exact acceptance, eight REDs, bounded-storage evidence, syntax/scope/hash audit and prepared host commands. In flight: none. Next: MAESTRO5 runs the host list and submits these exact hashes/evidence to Astra r3; activation remains host-owned. `context_saved.md` preserves decisions and this handoff within the authorized receipt namespace. Learning for the successor: pre-wrapper failure evidence must live off the source volume, and refusal history must not become an unbounded per-launch sink.

**BINDING context directive:** Watch this session and every orchestrated team's Context N% left. At approximately 20% remaining, stop starting work; write done/in-flight work, exact paths, next steps and risks into the task report; notify MAESTRO5 to use a fresh successor. Restate this directive in every handoff; never approach full-window compaction.


## MB8 Task 2 context handoff to MAESTRO6 — 2026-10-10T09:05:47.978337+00:00

**STOPPED at the explicit context gate; Task 2 is NOT built.** Before compaction, MB8 read `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb8_task2_prompt.txt`, the full `results/backup_gdrive_host_20261010/astra_r3_verdict.md`, and `results/backup_gdrive_mb8_20261010T082434Z/host_maestro5_verification.md`; inspected the implementation/tests and prior host helper; considered generation/journal designs in analysis; and created the preparation artifacts below. Baseline branch/HEAD: `worktree-c10k-route-a` / `5200f6301a5bab2c265d5477c53f93703613a615`.

After compaction, MB8 reread the Task 2 prompt and relevant source/test spans and verified worktree/branch. After the explicit stop, only state/hash verification and this documentation were performed. The first handoff writer hit a shell/Python quoting error before writing; the corrected writer verified that all baseline files were still unchanged. All seven code/test/launcher files match `baseline.json`; the report matched its saved pre-handoff bytes. **No implementation or tests were started; no changes are half-applied; no process is in flight.** No Task 2 test, Drive/network/model/GPU run, Git mutation, installation or launchd action occurred.

**Saved Task 2 REDs: none.** No Task 2 regression was written or executed. Existing `results/backup_gdrive_mb8_20261010T082434Z/red_launch_status.txt` and `results/backup_gdrive_mb8_20261010T082434Z/red_refusal_stress.txt` are historical Task 1 evidence, not R3 REDs. The progress announcement that REDs were next did not mean they had been saved.

Every file created for Task 2 so far, with exact SHA-256:

| Exact workspace-relative path | SHA-256 | State |
|---|---|---|
| `results/backup_gdrive_mb8b_20261010T085955Z/baseline.json` | `e47e718a70d99de076f4ce60a77310a9f71a978d71684b75906ed80c0ba6a122` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/results/backup_gdrive_build_report.md` | `97f8218ba173ece5e7923fc92a854da5400ca246ef6bd646114b63476c137c62` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/backup_gdrive.sh` | `506ce31845bcbe812261ce128f2119f247cfe270e69b8af08e9a612207aed9ce` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/backup_gdrive_status.py` | `f5c98ad6adb3530ac215befbfcedc94a63368a9d153186864f67823db7c40b25` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/launchd/MemitGdriveBackup.applescript` | `ebafee3ad82a4376ec5dda0fbc823f2170c795cddd56d62f5ede730d6d5c3bab` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/launchd/com.rhu.memit-gdrive-backup.plist` | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/test_backup_gdrive.py` | `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/before/tools/test_backup_gdrive_addendum.py` | `efa0c4e8047279bafe4dd04cfabb2b7839ff68ea012618f93b53cfd44785d985` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/git_status_before.txt` | `81e9429d99ebdd0d066a5c6d62f2b7c626b051ce8cf851ab2d2ce943495af5f9` | Complete preparation artifact |
| `results/backup_gdrive_mb8b_20261010T085955Z/prompt.txt` | `a580ef3a640b8a8f9f26654c28f86743cd86eafaa5ff71013f0ee2673e6168b4` | Complete preparation artifact |

The only modified preexisting file is `results/backup_gdrive_build_report.md`: this appended handoff is complete documentation, not a partial implementation. Its complete post-append SHA-256 is recorded externally in `results/backup_gdrive_mb8b_20261010T085955Z/handoff_SHA256SUMS.txt`, alongside every preparation-file digest. This checksum metadata excludes itself to avoid self-reference. Pre-handoff report SHA-256: `97f8218ba173ece5e7923fc92a854da5400ca246ef6bd646114b63476c137c62`.

**Concrete next step:** start a fresh builder session; read AGENTS.md Team mode/Context management and the Task 2 packet/verdict. First write and save REDs for finding 2: 10:00:00 success followed by 09:59:59 failure, equal timestamps with different generations, missing/corrupt/non-increasing counter, and manual execution without an applet generation. Then implement atomic internal-disk generation allocation/propagation and generation-only ordering; document the manual-run rule and the narrowly authorized change to the equal-timestamp-success assertion at `tools/test_backup_gdrive_addendum.py:120–122`. Next save REDs for finding 1's fresh success + receipt directory 0555 + absent wrapper, then implement the independent bounded journal and nested no-dialog catch. Verify/document both failure sinks unwritable. A separate generation directory to detect issued-but-unacknowledged launches was considered but is unimplemented and unverified.

Prepare a new host helper in fresh receipts for actual `open -W -g` combined absent+0555 and clock-independent ordering; revisit the old writefail healthy expectation. Native Task 2 applet/app-bundle execution remains **UNVERIFIED**. Run the packet's exact acceptance in the foreground, save every new RED and final GREEN/hash/scope evidence, append the completion report, and use `GDRIVE R3 FIX BUILD DONE` only when complete. Findings 3–5 stay closed; preserve their paths and all original scope/Do-NOT rules. No activation approval is inferred.

**BINDING context directive:** Watch your own and every orchestrated team's Context N% left. At approximately 20% remaining, stop starting work; write done/in-flight work, exact paths, next steps and risks into the task report; and notify the orchestrator to start a fresh successor. Restate this directive in every handoff; never approach full-window compaction. This session was compacted and explicitly stopped by MAESTRO6; do not resume implementation in it.


## MB11 Task 2 R3 findings 1–2 build and verification — 2026-10-10T09:26:59.752036+00:00

**Implementation is built; full acceptance is pending the explicit rclone constraint clarification.** This section supersedes MB8's unimplemented Task 2 handoff, without modifying prior sections or historical RED receipts. Worktree/branch verified as `worktree-c10k-route-a`; all seven MB8-listed code/test/launcher SHA-256 values and the post-handoff report hash matched at takeover. No half-applied code was found; MB11 chose to continue unchanged code, with no restore from HEAD. Evidence: `results/backup_gdrive_mb8b_20261010T085955Z/mb11_takeover.json`.

### Ordering and publication rules

Finding 2: the applet allocates a positive integer launch generation, atomically replacing `$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter` while holding a separate Perl `flock` lock. Allocation precedes wrapper execution, compares the counter with receipt/heartbeat/journal evidence, and refuses missing, corrupt, exhausted, non-increasing or ambiguous state. It propagates `BACKUP_LAUNCH_GENERATION` to the wrapper. Start and end heartbeat records include `launch_generation` and `launch_mode`; launch receipts include the generation. Status uses generations for ordering. A failure is acknowledged only by an equal or later **completed** heartbeat; timestamps remain display/staleness and malformed/future validation data. A successful launch receipt alone cannot clear a failed launch. Issued generations without completion remain unhealthy, independently of receipt publication.

Counter bootstrap is intentionally explicit and fail-closed: the initial counter must be provisioned as `0` exactly once in a new state directory before applet activation. **Never reset an existing counter or initialize over existing applet evidence.** Missing or ambiguous state requires operator-reviewed recovery. The host helper seeds only its own isolated fixture counter at generation 10; MB11 made no activation or installation change.

Manual-run rule: absent `BACKUP_LAUNCH_GENERATION` still runs normally and publishes `launch_generation: null`, `launch_mode: manual`. Status labels a completed manual/legacy heartbeat `manual/unsequenced`. Without applet evidence it can be healthy; it cannot acknowledge unresolved applet generations or failures. An exit-75 contender continues to preserve the owner's heartbeat and incomplete status; it never acknowledges journal failures.

The existing assertion at the former `tools/test_backup_gdrive_addendum.py:120–122` changed narrowly: equal or later wall-clock timestamps with completed generation 10 remain unhealthy against failed generation 11. Completing generation 11 clears the failure, including at the exact same timestamp. Added fixture counter/generation fields support this ordering check; timestamps no longer determine recovery.

Finding 1: receipt-publication failure appends a generation-bearing marker to `$HOME/Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl`, in a directory independent of receipts and counter state. Normal failed launch outcomes also enter this journal, preventing a later success/refusal receipt from hiding them without completion. Publication is atomic under a separate journal lock. The journal retains at most 64 markers, prioritizing the greatest failed generations and preserving ambiguous markers; writer reasons are bounded. Status refuses malformed/empty/unavailable journals and markers not acknowledged by completed generations. Embedded launch/receipt/journal code uses only `/bin` and `/usr/bin` programs and core Perl modules. The nested AppleScript catch remains; failures inside the handler are caught without dialogs.

When **both receipt and journal directories are 0555**, the launch counter still advances. The old heartbeat/receipt stay unchanged, the journal cannot publish, and status reports `unacknowledged launch generation 11: no completed heartbeat`. This closes the remaining two-sink case through independent issued-generation evidence; no false-green expectation is accepted. The old host `writefail` healthy-status expectation is replaced by an unhealthy journal expectation, even when its wrapper stub returns 0. A wrapper completion of generation 11 subsequently clears the fixture failure. Persistence against power loss is not claimed by these atomic-rename tests.

### Test-first receipts and verification

`mb11_red_index_final.json` maps **all 24 new tests plus the revised equality test (25 cases)** to saved behavioral RED logs. These were saved before each corresponding implementation change. One initial incomplete-generation schedule unexpectedly passed the old timestamp implementation; it was strengthened so the incomplete start timestamp follows the failed receipt. Its `_v2` RED is authoritative; the initial log was retained. MB8's Task 1 REDs were never replaced or re-saved.

- `mb11_GREEN_generation_round1.txt`: 23 tests passed before the final malformed-evidence boundary cases.
- `mb11_GREEN_no_rclone.txt`: **45 tests ran; 43 passed, 2 skipped, 0 failures/errors**. Includes all 25 RED-mapped cases, status regressions, shell-literal launch behavior, wrapper generation recording, 12 concurrent allocations, 80 failed-publication attempts, combined absent-wrapper/0555, and both sinks unwritable. No real rclone or network call occurred. Wrapper recording tests intentionally fail before rclone, or use a fixture stub.
- The two native AppleScript tests skipped after an independent Standard Additions positive-control probe failed with `com.apple.hiservices-xpcservice` / `Connection invalid`. The compiler's `-2741` observation does **not** prove source validity or a source defect here; native compilation and real `open -W -g` execution remain **UNVERIFIED** for MAESTRO6's host checks.
- Python AST parsing and `/bin/bash -n tools/backup_gdrive.sh` passed; `host_launcher_checks_mb11.py --help` passed. Static syntax and shell-literal evidence do not substitute for native host runs.

Exact acceptance remains pending because its existing tests execute `/opt/homebrew/bin/rclone` on temporary local fixtures, while MB11's current prompt explicitly prohibits running rclone. An asynchronous clarification requested permission for fixture-only rclone calls, with no Drive/network. No dependent acceptance run has occurred without that permission.

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

### MAESTRO6 host commands — prepared, not executed by MB11

The new helper preserves fixture/app-bundle evidence under `/private/tmp` and command/stdout/stderr/manifest/summary receipts under this receipt directory. It never installs, loads launchd, runs rclone/network, or deletes fixtures. Each case verifies healthy generation 10, performs a real `open -W -g` launch, verifies the failure and unchanged owner heartbeat, then verifies recovery only after completed generation 11. Rollback/equality cases force the emitted receipt time without changing the host clock.

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py absent-0555
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py clock-rollback
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py equal-time
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py writefail
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py both-unwritable
```

### Final code/helper SHA-256

| Changed path | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| `tools/backup_gdrive_status.py` | `614a5edb074c8427e98f4a5374ab60dac52ca68c3e9a336b3cf91c4240f03ef3` |
| `tools/launchd/MemitGdriveBackup.applescript` | `2c7b6ee22b9283d17c897a6107c4d210e42684fdf567bb1872fd41f7681afc8b` |
| `tools/test_backup_gdrive_addendum.py` | `fb0af721b29cefc07c795267655050520f249b3371eb3462757e4a0886e8fd19` |
| `results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py` | `7c3e113860a9efc2b99d6007f9ffc8ab51fdb529904a827c0b03b8fbef41a58f` |

The report's complete post-append SHA-256 and all new receipt hashes are saved in `results/backup_gdrive_mb8b_20261010T085955Z/mb11_SHA256SUMS.txt`; the report cannot embed its own complete digest. `tools/test_backup_gdrive.py`, `tools/launchd/build_gdrive_applet.sh`, and the plist remain byte-identical to MB8's baseline. No commit/push/merge, installation, launchd mutation, model/GPU run, network operation, or deletion of preexisting files occurred. `tools/test_dashboard_mathlab.py`, NEW-1 and git-automation files were left to their owners. Host verification and Astra review remain MAESTRO6's next external steps.

**BINDING context directive:** Watch "Context N% left" for this and every orchestrated team session. At **40% left or less**, stop starting work; append a handoff at the end of this report containing what is done, what is half-applied, exact paths and SHA-256 of changed files, and the next step; reply exactly `CONTEXT HANDOFF WRITTEN`. If "Context compacted" appears, do the same immediately. Restate this directive in every handoff; never continue to a mid-change compaction.


## MB11 Task 2 context handoff to MAESTRO6 — 2026-10-10T09:36:11.985528+00:00

**STOPPED at the binding context handoff gate. Do not start more build work in this session. Task 2 completion is NOT claimed:** the code and host helper are built, but exact acceptance is pending the operator's fixture-rclone clarification, and native host checks remain UNVERIFIED. No process is in flight. No code/test change is half-applied. This handoff's hashes and counts supersede the provisional MB11 section above.

**Done:** atomic, flock-serialized internal-disk generation allocation; wrapper start/end propagation; generation-only receipt/journal ordering; explicit manual/unsequenced heartbeat mode; fail-closed missing/corrupt/non-increasing/ambiguous counter handling; independent bounded 64-marker failure journal; nested no-dialog catches; combined absent-wrapper + 0555 regression and both-sinks-unwritable regression; native host helper and its command list. No commit, push, merge, installation, launchd mutation, real rclone, network or model/GPU run occurred.

A final inspection found one additional false-green: when the journal is unwritable, a failed generation 11 receipt could be replaced by a later exit-75 receipt at generation 12 without any completed heartbeat. MB11 saved a RED (`mb11_RED_test_unwritable_journal_refusal_cannot_hide_uncompleted_failure.txt`), then serialized receipt publication with allocation and preserved the unresolved failed receipt until an equal/later completed heartbeat acknowledges it. This preserves ordinary active-owner exit-75 behavior while preventing refusal receipts from clearing prior failures.

**Verification:** `mb11_red_index_final.json` now maps **25 new tests plus the revised equality regression (26 cases)** to saved REDs. `mb11_GREEN_no_rclone_final.txt` is the latest GREEN: **46 tests ran; 44 passed, 2 skipped, 0 failures/errors**. Every mapped case passed. The two native AppleScript tests skipped after the independent Standard Additions positive control also failed with `Connection invalid`; native compilation and actual `open -W -g` behavior are still UNVERIFIED. All MB8 receipts and earlier MB11 logs are retained. Do not re-save or overwrite RED logs. Do not rerun the historical construction scripts `mb11_write_applet.py` or `mb11_append_report.py`; they target earlier source/report states.

**Complete changed files, exact SHA-256:**

| Exact workspace-relative path | SHA-256 | State |
|---|---|---|
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | Complete |
| `tools/backup_gdrive_status.py` | `614a5edb074c8427e98f4a5374ab60dac52ca68c3e9a336b3cf91c4240f03ef3` | Complete |
| `tools/launchd/MemitGdriveBackup.applescript` | `446d35a6fc83c0fc84018d2fec9d2edf285588ec2fccd4fbc6d19a33f28534d1` | Complete |
| `tools/test_backup_gdrive_addendum.py` | `f19e0db1461bbfbe4e5f34300b473edd88aeb4a10d4b7e4af05f67c09a67be80` | Complete |
| `results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py` | `7c3e113860a9efc2b99d6007f9ffc8ab51fdb529904a827c0b03b8fbef41a58f` | Complete |

`results/backup_gdrive_build_report.md` contains only complete appended documentation. Its final post-handoff SHA-256 is saved externally in `results/backup_gdrive_mb8b_20261010T085955Z/mb11_handoff_SHA256SUMS.txt` (self-hash excluded). The complete receipt inventory, including report and changed-source hashes, is in `mb11_SHA256SUMS.txt`. The three remaining MB8 allowed files (`tools/test_backup_gdrive.py`, applet builder, plist) still match MB8's baseline SHA-256 exactly. Other builders' dashboard/NEW-1/git-automation work was left untouched.

**Concrete next step:** in a fresh session, verify the hashes above before editing and continue the built code; do not restore it to Task 1/HEAD. Resolve the pending asynchronous question: the user forbids rclone but the exact required acceptance suite invokes `/opt/homebrew/bin/rclone` on temporary local fixtures. No reply/authorization arrived in this session. Only after explicit authorization for those fixture-only calls, execute and save the exact acceptance command in the foreground:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

Then append acceptance counts, final hashes and native limitations. Use `GDRIVE R3 FIX BUILD DONE` with test counts only after required acceptance passes. Continue receipts in `results/backup_gdrive_mb8b_20261010T085955Z/`; preserve all historical REDs. MAESTRO6 verifies, GPT-6-Astra reviews, MAESTRO6 commits.

**MAESTRO6 host-check commands (prepared, not executed by MB11):**

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py absent-0555
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py clock-rollback
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py equal-time
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py writefail
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb8b_20261010T085955Z/host_launcher_checks_mb11.py both-unwritable
```

**Open risks/boundaries:** explicit first-activation counter provisioning is required (`0` in a fresh state directory only; never reset over applet evidence). No activation approval is inferred. Receipt/journal/boundedness proofs are shell/CPU fixtures, not native applet evidence or power-loss durability proof. Both unwritable failure sinks remain unhealthy through the independently issued counter; an exit-75 receipt cannot clear an unresolved failed receipt when journal publication fails. Full rclone-dependent acceptance and all real host helper cases remain unrun.

**BINDING context directive:** Watch "Context N% left" for your own and every orchestrated team session. At **40% left or less**, stop starting work; append a handoff at the end of this report with what is done, what is half-applied, exact paths and SHA-256 of changed files, and the next step. Reply exactly `CONTEXT HANDOFF WRITTEN`. If "Context compacted" appears, do the same immediately. Restate this directive in every handoff; do not take the tempting one-more-edit step into mid-change compaction.


## Known limits at activation — operator ruling D-C10r-rulings-16 (2026-10-10 ~09:50Z, MAESTRO8)

The operator ruled "turn on, keep fixing": build 186491a goes live with Astra r4's two residuals documented here, and a fresh builder (codexmb14, brief `~/.claude/jobs/8ac4cacf/tmp/codexmb14_prompt.txt`) fixes them in parallel. The fix replaces the live copy only after Astra GO. Verdict: `results/backup_gdrive_host_20261010/astra_r4_verdict.md`.

**Known limit 1 (r4 P1) — a refusal can hide a counter-only failure.** If a launch fails without leaving a failed receipt or journal marker, a later exit-75 refusal at the current counter makes status report healthy. Two schedules reach this. In the first, both failure sinks are unwritable, then a manual backup interleaves with an applet refusal. In the second, the process crashes after allocating a generation and before writing anything. Either way, an unwritable `~/Library/Logs` or a crash mid-launch can be reported green until the next sequenced completion. Mitigation until the fix lands: do not run manual backups while the applet job is loaded, and treat a status line naming a refusal as unconfirmed until a later sequenced completion appears.

**Known limit 2 (r4 P2) — null-generation evidence blocks allocation permanently.** If the counter file goes missing or corrupt, the applet publishes evidence with no generation. Repairing the counter does not clear it: allocation keeps refusing, and status stays unhealthy. This fails closed and loud, so no false green results, but backups stop until an operator recovery. No reviewed recovery command exists yet; codexmb14 builds one. Until then, the recovery is a reviewed manual step: move the ambiguous evidence aside (never delete it) and set the counter above every generation ever seen.

**Activation precondition found by MAESTRO8.** `~/Library/Logs/memit-gdrive-backup/launch_receipt.json` (written 2026-10-10T08:47:51Z, `wrapper_path` = a `/private/tmp/gdrive_addendum_*` fixture, no `launch_generation`) leaked from the native launcher test at 0ab0c42, which did not yet isolate `HOME`. The current test (186491a) isolates it. Left in place, this receipt would trip known limit 2 on the very first production launch. It must be preserved in this repo and moved aside before the counter is provisioned. codexmb14 must also prove that the whole suite leaves the real paths untouched.

**Amended 2026-10-10 ~10:20Z (operator, AskUserQuestion):** the install step was blocked by the session's auto-mode safety check (persistence). Offered approve / paste-commands / wait, the operator chose **wait for the fixed version**: nothing is installed until codexmb14's r4 P1+P2 fix passes Astra GO. The old internal-disk backup job stays as is. The leaked receipt is still in place and must be moved aside at activation.


## MB14 Astra r4 findings 1 (P1) and 3 (P2) build and verification — 2026-10-10T10:22:17.011897+00:00

**GDRIVE R4 FIX BUILD DONE.** This is a reviewed-build candidate for MAESTRO8 / GPT-6-Astra; installation and production replacement remain gated on review GO. The operator's live `186491a` build and its documented known limits were left in place. No commit, push, merge, Applications install, launchd write, real log write, real rclone invocation, or network call was made by MB14.

### Implemented rules and scope

P1: the applet persists `unresolved.json` beside `counter` under `counter.lock`. Its schema is `{"schema":1,"issued_generation":N,"unresolved":[[low,high],...],"recovery_barrier":null|N}`; inclusive disjoint intervals represent the unresolved generation set without enumerating large counter gaps. The issued set publishes before the counter. An interruption between those publications leaves a mismatch that refuses dispatch. An exit-75 receipt removes its own generation only. A manual completion removes no applet generation; only a completed sequenced heartbeat resolves earlier or equal generations. Resolved intervals are pruned under the lock on subsequent allocation/receipt publication; the status reader computes acknowledgement without writing state. A success receipt alone never completes a generation. The reader names the earliest unresolved generation, so both the required manual-interleave and allocation-crash schedules remain unhealthy and name **generation 11** after the generation-12 refusal.

P2: `recover` holds the same counter lock as allocation and all receipt/journal publication, including null-generation publication. It reserves a recovery barrier above the maximum of the operator's supplied floor, the counter, persisted issued state, active heartbeat/receipt/journal generations, and preserved recovery manifests. It first preserves a manifest, then publishes the barrier state, moves ambiguous evidence and the old counter into a fresh `memit-gdrive-backup-launch-state/recoveries/<UTC>/` directory, and publishes the barrier counter. Ambiguous evidence is moved byte-for-byte, never deleted; mixed journals are preserved as whole files. Interrupted publication remains fail-closed through ambiguity, a missing counter, or a state/counter mismatch. The next allocation is above the barrier. Status remains unhealthy until a completed sequenced heartbeat **strictly above** that barrier; manual completion cannot clear it. Existing unresolved ranges survive recovery. Repeated recovery remains monotonic even after a lower counter repair.

Changed code: applet, status tool, and addendum tests. `tools/backup_gdrive.sh` is unchanged (`36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8`). The build report is append-only; all earlier report bytes are preserved. MB14 did not edit main-checkout staged copies, `tools/test_dashboard_mathlab.py`, NEW-1, or git-automation files. All MB14-created fixtures and their cleanup were inside this receipt directory. `hashes_before.json` records all four existing files before the first edit; originals are preserved in `originals/`. The helper, listing script, and other receipt artifacts are newly created files with no prior content.

### Behavioral RED index and acceptance

Every new test is numbered for its criterion. All seven have behavioral RED logs saved before the change that made them pass:

| New test | Behavioral RED receipt |
| --- | --- |
| `test_1_manual_interleave_preserves_counter_only_generation_11` | `results/backup_gdrive_mb14_20261010T095752Z/RED_01_behavioral_manual_interleave.log` |
| `test_2_crash_after_allocation_then_refusal_preserves_generation_11` | `results/backup_gdrive_mb14_20261010T095752Z/RED_02_test_2_crash_after_allocation_then_refusal_preserves_generation_11.log` |
| `test_3_corrupt_unresolved_set_refuses_dispatch` | `results/backup_gdrive_mb14_20261010T095752Z/RED_03_test_3_corrupt_unresolved_set_refuses_dispatch.log` |
| `test_3_refusal_discharges_only_itself_and_completed_generations_resolve_set` | `results/backup_gdrive_mb14_20261010T095752Z/RED_04_test_3_refusal_discharges_only_itself_and_completed_generations_resolve_set.log` |
| `test_4_missing_counter_and_repeated_recovery_keep_monotonic_barriers` | `results/backup_gdrive_mb14_20261010T095752Z/RED_05_test_4_missing_counter_and_repeated_recovery_keep_monotonic_barriers.log` |
| `test_4_recovery_preserves_null_evidence_and_requires_sequenced_completion` | `results/backup_gdrive_mb14_20261010T095752Z/RED_06_test_4_recovery_preserves_null_evidence_and_requires_sequenced_completion.log` |
| `test_4_null_evidence_publication_waits_for_recovery_counter_lock` | `results/backup_gdrive_mb14_20261010T095752Z/RED_07_recovery_publication_lock.log` |

Machine-readable index: `results/backup_gdrive_mb14_20261010T095752Z/RED_index.json`. The first `RED_01_test_1_...` log failed the fixture positive control because the receipt-root destination was on `/Volumes/memit`; it is retained for history and is **not** the required P1 RED. `RED_01_behavioral_manual_interleave.log` is the corrected behavioral RED and is the indexed receipt. No-rclone fixtures use an explicit stub `fixture:` destination and stub config dump, preserving the production physical-disk refusal guard. The additional recovery-lock test was RED because null-generation publication completed while the recovery counter lock was held; it now waits for that lock.

Acceptance command (the two exports select isolated fixtures and forbid real rclone):

```sh
export BACKUP_TEST_NO_RCLONE=1
export BACKUP_TEST_RECEIPTS=$PWD/results/backup_gdrive_mb14_20261010T095752Z/fixtures
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v
```

**94 tests: 78 PASS, 16 host-pending skips, zero failures/errors; 7 new RED-to-GREEN regressions.** Evidence: `acceptance.log` (87.004 seconds), `acceptance_summary.json`, `GREEN_generation_checks.log`, `GREEN_recovery_lock.log`, and `GREEN_classifier_fixture.log`. The earlier full run is preserved as `attempt1_acceptance.log`; its classifier positive-control path needed a no-rclone fixture, now supplied without weakening its raw-exit assertion. Existing timestamp-ordering, completed-generation acknowledgement, receipt preservation, active-owner refusal and 1,000-refusal bounded-storage checks passed. Python syntax, embedded shell syntax, and changed-file whitespace checks passed. `verification.json` records the final audit.

Criterion 5 receipts: `real_paths_before.json` and `real_paths_after.json` are **byte-identical** (21 entries: 18 regular files with SHA-256, 2 directories, 1 absent path). They cover the actual HOME backup-log glob, actual Applications app, and all actual LaunchAgents. No symlink or special-file exceptions were present. The before/after observation includes names, modes, modification times, sizes and file hashes. Both listing receipts are preserved; no production write was used to test isolation.

Real-rclone tests left host-pending by name:

- `tools.test_backup_gdrive_addendum.ArchiveTest.test_corrupt_remote_download_check_does_not_create_receipt`
- `tools.test_backup_gdrive_addendum.ArchiveTest.test_differing_remote_is_immutable_and_preserves_prior_manifest`
- `tools.test_backup_gdrive_addendum.ArchiveTest.test_manifest_write_failure_is_loud`
- `tools.test_backup_gdrive_addendum.ArchiveTest.test_real_copy_download_check_and_sha_receipt_never_delete_source`
- `tools.test_backup_gdrive_addendum.ArchiveTest.test_source_drift_after_check_does_not_create_receipt`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_exit_publication_failure_is_loud_and_preserves_original_failure`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_native_nonregular_skip_is_recorded_as_warning`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_queued_source_vanish_is_warning_and_keeps_raw_exit`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_sync_publishes_actual_bytes_and_completed_success`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_remote_global_overrides_refuse_without_dispatch`
- `tools.test_backup_gdrive_addendum.HeartbeatTest.test_start_publication_failure_invalidates_previous_success`

Existing native tests left host-pending by name:

- `tools.test_backup_gdrive_addendum.LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest`
- `tools.test_backup_gdrive_addendum.LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`

Their existing positive control independently reproduced the unavailable Standard Additions XPC service in this sandbox, so native compilation/execution is **UNVERIFIED** here. Three additional native helper cases below are prepared and UNRUN; they are separate from the 94-test count. No Drive transfer, live installation, power-loss durability, or scientific execution is established by these fixture results.

### Recovery command: exact usage

After review GO, the operator can run the reviewed status tool explicitly:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N
```

Replace `N` with the operator-reviewed greatest generation ever issued/observed, including any history lost through missing or corrupt state. The command raises this floor to all greater generations it observes; it never resets to zero. For a fixture/custom heartbeat, append `--heartbeat /absolute/path/to/last_run.json`; the counter, journal and preserved recovery archive are derived from that heartbeat's log root. Without that option the command targets `$HOME/Library/Logs/memit-gdrive-backup/last_run.json`. It refuses while the sibling `memit-gdrive-backup.lock` exists and refuses an exhausted generation space. Inspect actual ownership before recovery; the command does not expire or remove ownership locks. Do not reprovision or reset a live counter as part of deploying this fix. Recovery itself never authorizes healthy status: require a later completed applet generation and confirm the read-only status command exits 0.

### Host commands for MAESTRO8

`host_launcher_checks_mb14.py` is a newly created host helper based on the MB11 isolated-launcher pattern. Every app is compiled inside its own preserved receipt fixture, every embedded HOME is redirected there, and every native invocation uses real `open -W -g`. The manual-interleave case uses the actual wrapper with a stub sync child, the crash case SIGKILLs only the exactly identified fixture applet after allocation and before receipt publication, and the recovery case uses native null evidence/allocation with an explicit fixture completed heartbeat. These are native/fixture checks, not a real backup. The helper never installs an app, writes launchd state, calls real rclone, or deletes its fixtures.

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb14_20261010T095752Z/host_launcher_checks_mb14.py manual-interleave
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb14_20261010T095752Z/host_launcher_checks_mb14.py crash-after-allocation
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb14_20261010T095752Z/host_launcher_checks_mb14.py recovery
```

To run the entire suite including real **local** rclone on the host, choose a fresh host fixture receipt root on `/private/tmp` so the existing source-physical-disk guard does not reject the local test destination. Its fixture cleanup remains inside that declared host receipt root. This command does not run a Drive self-test:

```sh
host_fixture_receipts=/private/tmp/backup_gdrive_mb14_host_$(/bin/date -u +%Y%m%dT%H%M%SZ)
/bin/mkdir "$host_fixture_receipts"
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb14_20261010T095752Z/real_path_listing.py "$host_fixture_receipts/real_paths_before.json"
LLMDB_ROOT=$PWD BACKUP_TEST_NO_RCLONE=0 BACKUP_TEST_RECEIPTS="$host_fixture_receipts" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v > "$host_fixture_receipts/acceptance.log" 2>&1
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb14_20261010T095752Z/real_path_listing.py "$host_fixture_receipts/real_paths_after.json"
cmp "$host_fixture_receipts/real_paths_before.json" "$host_fixture_receipts/real_paths_after.json"
```

Record and inspect the suite's exit code and log before any promotion; retain the host receipt root and supply its path with the review packet. Production staging/replacement follows MAESTRO8's reviewed GO process, outside MB14's build scope.

### Final SHA-256 and continuation

| File | Final SHA-256 |
| --- | --- |
| `tools/launchd/MemitGdriveBackup.applescript` | `683cb5a354b0b58fc8ff012317560d595f908000bc510d4ebfdf18741d1244da` |
| `tools/backup_gdrive_status.py` | `64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b` |
| `tools/test_backup_gdrive_addendum.py` | `74cbd8afb20f2be676e61e9e1329c3356c52031ece1e7e5aef536709b2e891f3` |
| `results/backup_gdrive_mb14_20261010T095752Z/host_launcher_checks_mb14.py` | `cd20f0651750ca2dfebef6da443efcb1b3bbb71e2d1f454e4f2ca8f5f53ca628` |
| `results/backup_gdrive_mb14_20261010T095752Z/real_path_listing.py` | `b040c2d595e4f1cdc49daee030987cbaff1e7fcdb5a36d710a7cdbf801bffca1` |

The final SHA-256 of the appended report itself is recorded in `results/backup_gdrive_mb14_20261010T095752Z/hashes_final.json`, avoiding a self-referential hash inside this report. That manifest also pins the changed code and newly created receipt files. Next step: MAESTRO8 runs the host-pending checks, supplies these exact source pins and receipts to Astra, and replaces the live copy only after review GO.

Context directive remains binding for every successor and team session: watch **Context N% left**; at **40% left or less**, stop starting work and append a handoff with completed/in-flight work, half-applied changes, exact paths and SHA-256, next step and open risks, then reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do that immediately. Restate this directive in every handoff. This build has no half-applied change; runtime/native/rclone review boundaries above remain explicit.


## MB20 Astra r5 findings 2 (P1) and 3 (P2) build and verification

**GDRIVE R5 FIX BUILD DONE — 25 PASS, 0 skipped; 9 new regressions have saved behavioral RED and GREEN.** Candidate for MAESTRO15 / GPT-6-Astra. All four MB14 start pins matched before the first edit. Activation remains blocked until re-review says GO. No commit, push, merge, Applications install, launchd mutation, real backup-log write, rclone, network call or native applet invocation was performed here. Only the three touched test classes ran.

### Rules and criterion evidence

1. Recovery parses journal lines independently, including valid records after a torn line. Every valid observed generation counts toward the maximum. Ambiguous journals are preserved in their entirety, byte-for-byte, including torn bytes. The exact corrupt-counter / absent-state / completed-10 / null-receipt / failure-100-plus-torn case refuses N=10 without mutation, then accepts N=100 and reserves barrier 101. Successful generation 12 and completion 101 remain unhealthy; sequenced completion 102 clears it. A valid 103 after the torn line also counts and produces barrier 104 with N=103.
2. Floors below observed history refuse before even creating a recovery directory or counter lock. History is checked again under the allocator lock before publication. Both valid and torn failure-100 journals have whole-tree byte/absence snapshots proving unchanged counter, unresolved state, receipt, journal, barrier and archive state on refused N=10.
3. Recovery alone remains unhealthy; manual and incomplete heartbeats do not discharge its barrier. The two touched MB14 recovery tests now meet the stricter floor rule: use floor 11 when state issued 11, and prove a repeated recovery with N=0 refuses before retrying with the prior barrier as the reviewed floor. Existing manual-interleave, allocation-crash, refusal, owner and publication-lock tests passed.
4. Persisted unresolved state is limited to **64 intervals and 2,048 bytes including the trailing newline**, using compact JSON. Exactly 64 intervals below the byte cap remain intact. On count 65 or byte overflow, all outstanding history is conservatively folded into `compaction_barrier = issued_generation`, with an empty interval list and the existing `recovery_barrier` retained. No oldest/newest subset is discarded. Later overflow advances the compacted barrier monotonically. Refusal can remove only its explicit interval and cannot discharge either barrier; manual or incomplete completion cannot clear them. A completed sequenced heartbeat at or above the compacted barrier can acknowledge it. Later unresolved intervals still need acknowledgement. The separate recovery barrier retains its strictly-above requirement. Missing optional `compaction_barrier` fields in MB14 schema-1 state remain supported.
5. Python recovery publication and both embedded Perl publishers agree at the interval boundaries. The MB16 helper was copied to `results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py` and extended with native case **unresolved-compaction**; the original is unchanged. The new case runs the 2,000-allocation fixture and then crosses the 64/65 boundary with three actual isolated applet invocations: refusal, another refusal after manual completion, and a subsequent sequenced fixture completion. It preserves unresolved-state evidence and checks sizes, barriers and health. Its default fixture root is fresh /private/tmp; explicit roots must be existing, empty and outside /Volumes. The 20-second open timeout is unchanged. **UNRUN / HOST-PENDING here**, per the host-load boundary.
6. `results/backup_gdrive_mb20_20261010T180133Z/real_paths_before.json` and `real_paths_after.json` are byte-identical: **21 entries, 18 regular files with SHA-256, 2 directories, 1 absent path**. They inventory the actual HOME backup-log glob, Applications/MemitGdriveBackup.app and all LaunchAgents before/after the final three-class sequence. The listing script only reads these paths. Tests and their cleanup used `results/backup_gdrive_mb20_20261010T180133Z/fixtures` exclusively. An initial inventory is also retained.

The 2,000-allocation test executes the complete extracted production allocation and receipt Perl programs in one process against receipt-local persistent files: odd 11..2009 allocate without completion; even 12..2010 refuse. It reads persisted state after each allocation/refusal, checks both bounds, and checks unhealthy status naming generation 11 or its compacted barrier. A manual or incomplete heartbeat and a further refusal remain unhealthy; subsequent sequenced completion makes it healthy. The GREEN harness compiles the programs once to reduce host load; only process exit and stdout are adapted for in-process execution. These are production-shell fixtures, not native execution or real backups.

### RED index and scoped verification

Machine-readable index: `results/backup_gdrive_mb20_20261010T180133Z/RED_index.json`. Every indexed RED was saved before the production change that made it pass.

| New test | Behavioral RED log in receipt directory |
| --- | --- |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_1_torn_journal_preserves_generation_and_entire_ambiguous_file` | `RED_01_test_1_torn_journal_preserves_generation_and_entire_ambiguous_file.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_1_valid_generation_after_torn_line_still_counts` | `RED_02_test_1_valid_generation_after_torn_line_still_counts.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_2_floor_below_valid_journal_is_read_only` | `RED_03_test_2_floor_below_valid_journal_is_read_only.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_2_floor_below_torn_journal_is_read_only` | `RED_04_test_2_floor_below_torn_journal_is_read_only.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_4_exact_limit_and_limit_plus_one_compaction` | `RED_05_test_4_exact_limit_and_limit_plus_one_compaction.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_4_byte_overflow_preserves_the_recovery_barrier` | `RED_06_test_4_byte_overflow_preserves_the_recovery_barrier.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_4_two_thousand_allocations_remain_bounded_and_fail_closed` | `RED_07_test_4_two_thousand_allocations_remain_bounded_and_fail_closed.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_4_compacted_barrier_cannot_be_refused_and_completion_at_barrier_clears` | `RED_08_test_4_compacted_barrier_cannot_be_refused_and_completion_at_barrier_clears.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_5_python_and_both_perl_publishers_agree_at_boundaries` | `RED_09_test_5_python_and_both_perl_publishers_agree_at_boundaries.log` |

The two `attempt1_RED_07_...` / `attempt1_RED_09_...` logs are retained but excluded. One exposed an over-greedy shell-program extractor; the other mixed an interval assertion with a missing post-fix helper call in continuing subtests. Their indexed replacements prove actual interval overflow. All nine accepted RED logs contain assertion failures and no unittest errors; production was unchanged until those corrected REDs were saved.

Exact scoped commands from the worktree root:

```sh
export BACKUP_TEST_NO_RCLONE=1
export BACKUP_TEST_RECEIPTS=$PWD/results/backup_gdrive_mb20_20261010T180133Z/fixtures
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5RecoveryTest -v
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5CompactionTest -v
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.GenerationLaunchTest -v
```

GREEN receipts under `results/backup_gdrive_mb20_20261010T180133Z`: `GREEN_R5RecoveryTest.log` (4 PASS), `GREEN_R5CompactionTest.log` (5 PASS), `GREEN_GenerationLaunchTest.log` (16 PASS). No skips. Python, embedded shell and Perl syntax checks and scoped whitespace checks passed. `verification.json` records the counts, isolation and unchanged-file checks; MB20 diffs against MB14 are saved beside it. The full suite was intentionally not run here.

### Updated recovery command and refusal behavior

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be the operator-reviewed greatest generation ever issued, including lost history, and **at least every observed generation** from the counter, issued state, heartbeat, receipt, independently parseable journal records and preserved recovery manifests. Lower floors exit nonzero with `recovery refused` / `below observed maximum` and publish or move no recovery evidence. This supersedes MB14's statement that an inadequate floor is raised automatically. A corrupt journal line does not refuse an otherwise permitted recovery: each valid line counts and the entire ambiguous file is preserved. Active ownership and exhausted generation space still refuse. Help output is retained in `recovery_help.txt`.

The heartbeat option is required for fixtures. Omitting it targets real HOME state and is an operator recovery action only after review GO. Recovery never establishes healthy status; require a completed sequenced generation strictly above its new barrier. Never provision zero over existing history.

### Exact host commands for MAESTRO15

Run the full addendum suite once on the host with real **local** rclone and preserved /private/tmp receipts. No Drive self-test is requested.

```sh
mb20_host_receipts=/private/tmp/backup_gdrive_mb20_host_$(/bin/date -u +%Y%m%dT%H%M%SZ)
/bin/mkdir "$mb20_host_receipts"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/real_path_listing.py "$mb20_host_receipts/real_paths_before.json"
LLMDB_ROOT=$PWD BACKUP_TEST_NO_RCLONE=0 BACKUP_TEST_RECEIPTS="$mb20_host_receipts" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v > "$mb20_host_receipts/acceptance.log" 2>&1
mb20_suite_exit=$?
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/real_path_listing.py "$mb20_host_receipts/real_paths_after.json"
if [ "$mb20_suite_exit" -ne 0 ]; then
    /bin/cat "$mb20_host_receipts/acceptance.log"
    exit "$mb20_suite_exit"
fi
/usr/bin/cmp "$mb20_host_receipts/real_paths_before.json" "$mb20_host_receipts/real_paths_after.json"
```

Retain and inspect acceptance.log, exit code and inventories before proceeding. All four native helper cases are HOST-PENDING / UNRUN here. The copied helper defaults to fresh local /private/tmp fixtures:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py manual-interleave
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py crash-after-allocation
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py recovery
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py unresolved-compaction
```

No new unit test requires real rclone or a native applet. Existing real-rclone tests remain host-pending (prefix `tools.test_backup_gdrive_addendum.`):

- `ArchiveTest.test_corrupt_remote_download_check_does_not_create_receipt`
- `ArchiveTest.test_differing_remote_is_immutable_and_preserves_prior_manifest`
- `ArchiveTest.test_manifest_write_failure_is_loud`
- `ArchiveTest.test_real_copy_download_check_and_sha_receipt_never_delete_source`
- `ArchiveTest.test_source_drift_after_check_does_not_create_receipt`
- `HeartbeatTest.test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries`
- `HeartbeatTest.test_exit_publication_failure_is_loud_and_preserves_original_failure`
- `HeartbeatTest.test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept`
- `HeartbeatTest.test_native_nonregular_skip_is_recorded_as_warning`
- `HeartbeatTest.test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night`
- `HeartbeatTest.test_real_queued_source_vanish_is_warning_and_keeps_raw_exit`
- `HeartbeatTest.test_real_sync_publishes_actual_bytes_and_completed_success`
- `HeartbeatTest.test_remote_global_overrides_refuse_without_dispatch`
- `HeartbeatTest.test_start_publication_failure_invalidates_previous_success`

Existing native tests remain host-pending by name:

- `tools.test_backup_gdrive_addendum.LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest`
- `tools.test_backup_gdrive_addendum.LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`

These fixtures do not establish a Drive copy, production permissions, live activation or power-loss durability. MAESTRO15 host acceptance and Astra re-review remain required.

### Start and final SHA-256 / scope

| File | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `tools/backup_gdrive_status.py` | `64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b` | `a4d3978bfc2995c78762f83c8c73152e73e8feb6cb4d8056791223249ef082c2` |
| `tools/launchd/MemitGdriveBackup.applescript` | `683cb5a354b0b58fc8ff012317560d595f908000bc510d4ebfdf18741d1244da` | `31566aca9386b8c70d822f4e9bfe2132b7bb8c86a87b46440aea6c91eec6e6d7` |
| `tools/test_backup_gdrive_addendum.py` | `74cbd8afb20f2be676e61e9e1329c3356c52031ece1e7e5aef536709b2e891f3` | `6bca5cd7751ff28c19083175dfcbe4829e7d4d80827f5db33aa58a668ba6b833` |
| `results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py` | New receipt copy; copied baseline `61683c2d8f0a48def55771f48133c7037404e788cfce7805bab926af476937c9` | `f37134a94b9692630a7853e25c7d2847da5d6b13d8df2eeec73856f4715d9efd` |
| `results/backup_gdrive_build_report.md` | `dfe3e3df2f15b4ed24767cb91bcd13db179446b4e4f70a1fdec03ce68a726976` | See `results/backup_gdrive_mb20_20261010T180133Z/hashes_final.json`, external to avoid a self-referential report hash |

The report was appended; every earlier byte remains unchanged. `hashes_before.json` records start pins; `originals/` preserves MB14 code/report. `hashes_final.json` supplies the report final SHA-256 and hashes of all newly created receipt artifacts (start: absent). The original MB16 helper is unchanged. `tools/backup_gdrive.sh` remains `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8`. No main-checkout staged copy, dashboard MathLab file, NEW-1 file or unrelated builder file was edited. MB20 fixture deletion stayed inside this receipt directory.

Session continuation: no half-applied change or in-flight test remains. Next: MAESTRO15 runs the host commands once, provides the exact source pins, RED/GREEN logs and native receipts to Astra, and keeps activation blocked until GO. Learning: preserving journal bytes alone does not preserve their ordering constraint; derive barriers from independently parsed records and refuse inadequate reviewed floors before mutation.

Context directive remains binding for every successor/team session: watch **Context N% left**. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a handoff with completed/in-flight work, half-applied changes, exact paths and SHA-256 and next step, then reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do so immediately. Restate this directive in any handoff.

## MB21 Astra r6 findings 2 (P1), 3 (P2) and 4 (P2) build and verification

**GDRIVE R6 FIX BUILD DONE — 15 PASS, 0 skipped; 8 new or reversed regressions have saved behavioral RED and GREEN.** Candidate for MAESTRO17 host verification and GPT-6-Astra re-review. Activation remains **BLOCKED** until Astra says GO. Starting branch/root were verified as `worktree-c10k-route-a` / this worktree. All four supplied MB20 source pins matched before the first edit. The archived MB14 status source also matched `64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b`.

### Criteria and evidence

1. Recovery now inspects the payloads in **all** recovery directories, including raw archived counters, archived heartbeat/receipt JSON and every independently parsed archived journal line before and after torn lines. Manifests remain validated, but their maximum does not replace payload inspection. The same `inspect_history()` implementation runs before any recovery mkdir/lock and again under the allocator lock. Archived uncertain payloads are observed without being added to the list of files moved by recovery. Every archived byte stays intact.
2. Live `refusals/latest-refusal.json` is included in both observed-maximum calculations. Its valid launch generation raises the required reviewed floor. Exit 75 publishes no failure journal or additional failure interval. The absent-state recovery keeps the existing conservative lost-history range derived from the reviewed floor; with floor 100 that range is `[[1,100]]`, and the recovery barrier is 101. No refusal-specific failure is inserted. The exact corrupt-counter / absent-state / completed-10 / null-receipt / refusal-100 input refuses floor 10 with the whole Logs tree unchanged, accepts floor 100, retains the refusal bytes and becomes healthy after sequenced completion 102. A separate injected-refusal test proves the under-lock recheck.
3. All three compaction boundaries are strict: the Python reader rejects **completed <= compaction_barrier**, and both extracted Perl `resolve_state` implementations clear only for **completed > compaction_barrier**. The old equality-clears test is reversed and renamed `test_r6_3_compacted_barrier_requires_strictly_later_completion`. The previous `test_5_python_and_both_perl_publishers_agree_at_boundaries` is extended and renamed `test_r6_3_python_and_both_perl_publishers_agree_at_boundaries` to follow the required r6 criterion numbering. It checks completed = barrier - 1, barrier and barrier + 1 for Python and both publishers, as well as the original 64/65 interval boundary. The actual extracted production-shell schedule fails odd generations 11..137 and refuses the intervening evens, then allocates 139: barrier 139 is created, completion 139 remains unhealthy and both publishers retain it; allocation/refusal 140 still cannot discharge it; completion 140 becomes healthy and both publishers clear it.
4. The seven retained tests passed with the eight new/reversed regressions. The r5 torn-journal and valid-after-torn cases still preserve all bytes, refuse inadequate floors, reserve the correct barriers and require sequenced completion above recovery. The unchanged 2,000-allocation test exercises both complete production Perl programs, preserves 64-interval / 2,048-byte bounds and keeps manual, incomplete and refused completions from clearing barriers. The byte-overflow test retains `recovery_barrier`. The applet diff is verified to contain **exactly two comparison replacements**; manual-interleave, late-generation ordering, owner handling, exit-75 publication, nested catches and launch control flow were not rewritten. `tools/backup_gdrive.sh` is unchanged, so retries, bandwidth, excludes and owner-preserving refusal behavior retain their reviewed implementation. Finding 5's remaining runtime tests are part of the full host suite below; they were not rerun locally outside the authorized touched classes.
5. MB20's helper was copied, preserving the original, to `results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py`. New native case **compaction-boundary** seeds the 64 odd intervals and uses three actual isolated applet allocation/refusal invocations: first compaction at 139, then completion equal to 139 during generation/receipt publication 140 (still unhealthy; barrier retained), then completion 140 during publication 141 (healthy; barrier cleared). It saves `unresolved_compacted.json`, `unresolved_equal.json` and `unresolved_above.json`. Default fixture roots remain fresh local `/private/tmp`; explicit roots must exist, be empty and resolve outside `/Volumes`. The 20-second `open -W -g` timeout is unchanged. All five native cases are **UNRUN / HOST-PENDING here**. Only syntax and `--help` were checked for the copied helper.
6. Real HOME inventories immediately before and after the final two-class run are byte-identical: **21 entries, 18 regular files with SHA-256, 2 directories, 1 absent path**. Both listing files have SHA-256 `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99`. The read-only MB20 inventory script was copied unchanged to `results/backup_gdrive_mb21_20261010T191747Z/real_path_listing.py`. An initial inventory is retained too. Every test fixture and cleanup used `results/backup_gdrive_mb21_20261010T191747Z/fixtures`; the actual HOME backup-log glob, Applications app and LaunchAgents were only read by the inventory script.

### Actual MB14 fixture

`results/backup_gdrive_mb21_20261010T191747Z/capture_mb14_fixture.py` ran the pinned MB14 recovery **once** on the exact requested input in a receipt-local temporary directory: failure 100 followed by `{torn`, corrupt counter, absent unresolved state, completed generation 10, null-generation receipt, floor 10. Command/exit/stdout/stderr are saved in `mb14_recovery_command.json`. Actual MB14 output had highest_seen 10 and recovery_barrier 11, while its archived journal retained failure 100. The exact archived directory names and file bytes, counter, counter lock and unresolved state are saved under `mb14_fixture/`. The regression copies this saved output layout, verifies every saved file hash, refuses floor 11 without changing any file/absence, accepts floor 100 with barrier 101, rejects completion 13 and accepts a sequenced allocation/completion 102. The original MB14 archive remains byte-identical throughout.

Machine-readable tree: `results/backup_gdrive_mb21_20261010T191747Z/mb14_fixture_tree_sha256.json`. Paths below are relative to `mb14_fixture/`:

| Path | Bytes / kind | SHA-256 |
| --- | --- | --- |
| `counter` | 3 | `25d4f2a86deb5e2574bb3210b67bb24fcc4afb19f93a7b65a057daa874a9d18e` |
| `counter.lock` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `recoveries` | directory | `directory` |
| `recoveries/20261010T192107.072565Z` | directory | `directory` |
| `recoveries/20261010T192107.072565Z/counter` | 8 | `06d0083ba740ff26c91cb17f10d15d398eea1affd3112599b429f30452b59db4` |
| `recoveries/20261010T192107.072565Z/failures.jsonl` | 68 | `5549e15ca2e08f2e074f3cb2cd88f8a7a23729f42b51071e59de1b2d724e331a` |
| `recoveries/20261010T192107.072565Z/launch_receipt.json` | 263 | `82829ede0361d5e94b9ca0843a0bcef76f5cce7c8ecfbc9b95ddb4c384af6f08` |
| `recoveries/20261010T192107.072565Z/manifest.json` | 822 | `ad1d4416f1f50a0aab6ee02854c7adc3eec0acbbbcd91a968211035c37bf9798` |
| `unresolved.json` | 88 | `d8f8aa0959759c7db247333db835e5f75867a4c99f53cfbb37fdd9c386670502` |

### RED index and scoped verification

Machine-readable index: `results/backup_gdrive_mb21_20261010T191747Z/RED_index.json`. Production status/applet/wrapper hashes were still the MB20 pins when the RED runs completed. Each touched class ran once in RED and once in GREEN; each individual RED receipt contains its corresponding complete class log, including that test's assertion failure. The eight indexed methods had behavioral failures and **no unittest errors or skips**. Seven retained tests were already passing. No full-suite or native execution, rclone invocation, network call or repeated test loop was performed by MB21.

| New or reversed test | RED receipt in this directory |
| --- | --- |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_r6_1_mb14_archive_requires_floor_100_and_completion_102` | `RED_test_r6_1_mb14_archive_requires_floor_100_and_completion_102.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_r6_1_every_archived_source_in_older_directories_counts` | `RED_test_r6_1_every_archived_source_in_older_directories_counts.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_r6_1_under_lock_rechecks_archived_journal` | `RED_test_r6_1_under_lock_rechecks_archived_journal.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_r6_2_refusal_heartbeat_raises_floor_without_a_failure` | `RED_test_r6_2_refusal_heartbeat_raises_floor_without_a_failure.log` |
| `tools.test_backup_gdrive_addendum.R5RecoveryTest.test_r6_2_under_lock_rechecks_refusal_heartbeat` | `RED_test_r6_2_under_lock_rechecks_refusal_heartbeat.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_r6_3_compacted_barrier_requires_strictly_later_completion` | `RED_test_r6_3_compacted_barrier_requires_strictly_later_completion.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_r6_3_python_and_both_perl_publishers_agree_at_boundaries` | `RED_test_r6_3_python_and_both_perl_publishers_agree_at_boundaries.log` |
| `tools.test_backup_gdrive_addendum.R5CompactionTest.test_r6_3_odd_failure_schedule_compacts_at_139` | `RED_test_r6_3_odd_failure_schedule_compacts_at_139.log` |

Exact scoped commands used by `run_scoped_tests.py` (the executable resolves to this worktree's `.venv/bin/python`):

```sh
export BACKUP_TEST_NO_RCLONE=1
export BACKUP_TEST_RECEIPTS=$PWD/results/backup_gdrive_mb21_20261010T191747Z/fixtures
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5RecoveryTest -v
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5CompactionTest -v
```

GREEN receipts: `GREEN_R5RecoveryTest.log` (**9 PASS**) and `GREEN_R5CompactionTest.log` (**6 PASS**), zero skips. `RED_commands.json` / `GREEN_commands.json` preserve exact argv, exits, counts and log hashes. `verification.json` records syntax checks, exact two-change publisher scope, protected pins, intact MB14 fixture hashes, eight RED receipts and identical real-path inventories. Python compilation without bytecode, all three embedded shell syntax checks, both entire extracted Perl syntax checks, helper/recovery CLI help and changed-line whitespace checks passed. Source diffs against the captured MB20 originals are saved beside those receipts. The full suite is intentionally host-pending; expected count after these six net-new methods is 119, subject to MAESTRO17's actual full-suite receipt.

### Recovery command, evidence list and refusal rule

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be operator-reviewed and cover every observed generation from: the current raw counter; current `unresolved.json` issued state; current heartbeat; current launch receipt; every independently parseable current failure-journal line; current `refusals/latest-refusal.json`; every preserved recovery manifest; every archived raw counter; and JSON / individually parsed JSONL payloads in **every** archived recovery directory, including archived heartbeats, receipts, refusal heartbeats and failure journals. Recognized valid generation fields include launch_generation, issued_generation, recovery_barrier, compaction_barrier, highest_seen and generation_floor. Old directory payloads count even if a newer directory has a lower maximum. Both the pre-lock scan and under-lock recheck use this complete list.

An inadequate floor exits nonzero with `recovery refused` / `below observed maximum`; a pre-lock refusal creates no directory or lock and writes/moves nothing. An injected higher archived generation or refusal after the first scan is rejected under lock without moving/publishing recovery evidence. Exit 75 is only an observed-generation source, not an unresolved backup failure. All archived bytes remain intact even when torn. Recovery still never establishes health on its own, and neither manual completion nor refusal can discharge recovery or compaction barriers. Do not omit `--heartbeat` in fixtures: the default points at real HOME and remains an operator recovery action only after GO.

### Exact host commands for MAESTRO17

Run the full addendum suite once on the host with real **local** rclone, preserving local `/private/tmp` receipts. This is not a Drive/network self-test.

```sh
mb21_host_receipts=/private/tmp/backup_gdrive_mb21_host_$(/bin/date -u +%Y%m%dT%H%M%SZ)
/bin/mkdir "$mb21_host_receipts"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/real_path_listing.py "$mb21_host_receipts/real_paths_before.json"
LLMDB_ROOT=$PWD BACKUP_TEST_NO_RCLONE=0 BACKUP_TEST_RECEIPTS="$mb21_host_receipts" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v > "$mb21_host_receipts/acceptance.log" 2>&1
mb21_suite_exit=$?
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/real_path_listing.py "$mb21_host_receipts/real_paths_after.json"
if [ "$mb21_suite_exit" -ne 0 ]; then
    /bin/cat "$mb21_host_receipts/acceptance.log"
    exit "$mb21_suite_exit"
fi
/usr/bin/cmp "$mb21_host_receipts/real_paths_before.json" "$mb21_host_receipts/real_paths_after.json"
```

Inspect acceptance.log, exit code and identical inventories before proceeding. Run **every** native helper case on local temp paths; none was run by MB21:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py manual-interleave
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py crash-after-allocation
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py recovery
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py unresolved-compaction
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py compaction-boundary
```

Provide source pins, RED/GREEN, fixture tree, isolation receipts, full-suite and five native-case evidence to GPT-6-Astra. This build establishes fixture behavior and syntax only; native privacy, real Drive copy, production activation and power-loss durability remain unverified. No commit, push, merge, Applications install, launchd mutation, real backup-log write, rclone or network call occurred here.

### Start and final SHA-256 / scope

| Changed file | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `tools/backup_gdrive_status.py` | `a4d3978bfc2995c78762f83c8c73152e73e8feb6cb4d8056791223249ef082c2` | `1063228655fb3712705b617b5da9412f5b887a40e317311fc38cedd41a5a97a0` |
| `tools/launchd/MemitGdriveBackup.applescript` | `31566aca9386b8c70d822f4e9bfe2132b7bb8c86a87b46440aea6c91eec6e6d7` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` |
| `tools/test_backup_gdrive_addendum.py` | `6bca5cd7751ff28c19083175dfcbe4829e7d4d80827f5db33aa58a668ba6b833` | `da2389f23a91c7e7db75d81a46d81bf6439f8d6a9e87d4161eaf3d7fff6359a9` |
| `results/backup_gdrive_mb21_20261010T191747Z/host_launcher_checks_mb21.py` | `New receipt copy; copied baseline f37134a94b9692630a7853e25c7d2847da5d6b13d8df2eeec73856f4715d9efd` | `e6e8a21e019759f9dfc14f6be410deb9a5100e05fa55b5d8a9545019faff995f` |
| `results/backup_gdrive_build_report.md` | `10f403d6480c2b22cd26f1a7788026b587b9a8f02db908a8a20794cd702f1b33` | See `results/backup_gdrive_mb21_20261010T191747Z/hashes_final.json` (external to avoid self-reference) |

The report is appended and every prior byte is retained. `hashes_final.json` supplies its final hash and hashes of every new receipt file (start: absent), avoiding a self-referential report hash. `hashes_before.json` and `originals/` preserve the start evidence. The copied listing script remains `2bc40d375fc4651d0d57525739083b832ed495189568d923074f193e4bed30c1`. MB14 original and both MB20 helper/listing originals remain unchanged. `tools/backup_gdrive.sh` remains `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8`; no criterion required changing it. No main-checkout staged file, dashboard file/receipt, `tools/test_dashboard_mathlab.py`, NEW-1 file or unrelated builder file was touched or hashed as protected.

Session continuation: no half-applied source change or in-flight test remains. Next: MAESTRO17 runs the host commands once, obtains Astra re-review and keeps activation blocked until GO. Learning: archived payloads retain generation authority independently of manifests; refusal generations constrain recovery floors without becoming backup failures; completion must be strictly later than a conservative compaction barrier.

Context directive remains binding for every successor/team session: watch **Context N% left**. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a handoff with completed/in-flight work, half-applied changes, exact paths and SHA-256 and next step, then reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do so immediately. Restate this directive in any handoff. Do not allow sessions to approach full-window compaction; use a fresh successor with a precise handoff.


## MB24 — Astra r7 finding 2 publication-temporary / archive scan fix (2026-10-10)

**BUILD DONE; activation remains BLOCKED pending Astra re-review GO.** Worktree `worktree-c10k-route-a`; starting MB21 commit `f22c9f2`. All four supplied start hashes matched before the first source edit. Receipts: `results/backup_gdrive_mb24_20261010T194953Z/`. MB24 ran only the new classes and the explicitly required existing `R5RecoveryTest` (including all five r6 tests); no full suite, native case, rclone, network, install, launchd mutation, commit, push or merge ran.

### Change and scope

Only `recover.inspect_history` changed in the status tool. Both pre-lock and under-lock calls enumerate every known live publication-temporary prefix in the heartbeat directory, its `refusals/` directory, the launch-state directory and the launch-journal directory, plus every file recursively below `recoveries/`. Recursive traversal includes nested manifests and nested temporary files. Heartbeat/receipt/state temporaries are JSON objects; journal temporaries are JSONL; counter temporaries are integers. `.recovery.*` is shared by the counter, unresolved-state and manifest publishers, so it accepts the writer's exact integer format or a JSON object. Temporary evidence is read only and stays at its original path with identical bytes, including after successful recovery.

Unsupported encodings (UTF-16 included), archive file formats, wholly unparseable archived JSON/JSONL, unparseable publication temporaries, non-object archived JSON, invalid generation field types and generation fields nested in objects or arrays refuse with the evidence filename. Known damaged canonical raw counters remain preserved damaged history under the existing operator-reviewed-floor contract; they are never invented into numeric generations. Existing canonical UTF-8 failure journals still retain independently valid records before and after torn lines, as required by the unchanged R5/r6 fixtures. These supported damaged-history forms are distinct from unsupported encodings/layouts. Ordinary null-generation final receipts remain preservable ambiguous evidence.

`scope_checks.json` proves byte identity outside `inspect_history`, byte identity of every existing test, unchanged applet/wrapper hashes, and copied inventory-helper identity. Consequently strict status `completed > barrier`, both Perl publishers, 64 intervals / 2,048 bytes, owner-preserving exit 75, read-only status and r4 manual-interleave code were not edited. The existing MB14 replay, refusal heartbeat and sequenced recovery-boundary tests pass here. Full-suite and native behavior beyond these targeted tests are **HOST-PENDING / not reproduced by MB24**; the MB21 host receipts remain prior host evidence. No applet/wrapper edit was needed, so requirement 4 requires no native-helper copy or new native case.

### Start and final SHA-256

| File | Start | Final |
| --- | --- | --- |
| `tools/backup_gdrive_status.py` | `1063228655fb3712705b617b5da9412f5b887a40e317311fc38cedd41a5a97a0` | `6140a7e1d0b122ee30c93bfbfb5861a99851a7dcd1788cc23a21e355deff3046` |
| `tools/test_backup_gdrive_addendum.py` | `da2389f23a91c7e7db75d81a46d81bf6439f8d6a9e87d4161eaf3d7fff6359a9` | `5e22410abde8debbefdce4810b3f455a5b62189371f715e2ed59a03f5d68806c` |
| `tools/launchd/MemitGdriveBackup.applescript` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` |
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |

The report's start SHA-256 is `2d9d23c5f5ecd449ddd9c906228efe69c723784a3c5d45a0bfa37a6b354ae454`. This section is appended only; the existing report prefix is checked byte for byte. Its final digest is in `results/backup_gdrive_mb24_20261010T194953Z/final_sha256.txt`, computed after append to avoid a self-referential report digest. Newly created receipt files start ABSENT; their final digests are in the same file (which excludes itself).

### Actual writer publication-temporary prefixes

| Prefix | Writer file:line |
| --- | --- |
| `.last_run.*` | `tools/backup_gdrive_status.py:228` |
| `.recovery.*` | `tools/backup_gdrive_status.py:277` |
| `.unresolved.*` | `tools/launchd/MemitGdriveBackup.applescript:3` |
| `.counter.*` | `tools/launchd/MemitGdriveBackup.applescript:3` |
| `.unresolved.*` | `tools/launchd/MemitGdriveBackup.applescript:6` |
| `.launch-receipt.*` | `tools/launchd/MemitGdriveBackup.applescript:6` |
| `.journal.*` | `tools/launchd/MemitGdriveBackup.applescript:6` |

These are all six distinct prefixes from the reviewed writers. `tools/backup_gdrive.sh` creates no publication temporary itself; at `:43` it invokes the status publisher, with refusal heartbeat destination selected at `:42`. Both applet state publishers create `.unresolved.*` (`:3` and `:6`). Every prefix is covered live and archived; `.last_run.*` includes both the ordinary heartbeat directory and the exact Astra refusal path `refusals/.last_run.ABC123`. `.recovery.*` has separate raw integer, state-object and manifest-object cases.

### Behavioral RED index and final GREEN

The scanner stayed at the supplied start SHA during both RED runs. `red_index.json` records each new test, every failure line, the baseline scanner hash and the unchanged new-test hash. All 16 new tests have behavioral REDs: 11 temporary tests / 54 failed subcases and 5 archive tests / 7 failed subcases; no import/runtime errors or skips. All fixtures are raw bytes, never outputs from the fixed scanner's helpers.

| New test | Saved RED log | Failure lines |
| --- | --- | --- |
| `test_r7_1_refusal_last_run_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 222, 233 |
| `test_r7_1_heartbeat_last_run_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 90, 101 |
| `test_r7_1_launch_receipt_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 134, 145 |
| `test_r7_1_journal_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 112, 123 |
| `test_r7_1_counter_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 68, 79 |
| `test_r7_1_unresolved_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 586, 597 |
| `test_r7_1_recovery_state_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 200, 211 |
| `test_r7_1_recovery_manifest_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 178, 189 |
| `test_r7_1_recovery_counter_temporary_live_and_archived_floor_pair` | `red_R7PublicationTemporaryTest.log` | 156, 167 |
| `test_r7_1_under_lock_rechecks_every_live_and_archived_temporary` | `red_R7PublicationTemporaryTest.log` | 244, 252, 260, 268, 276, 284, 292, 300, 308, 316, 324, 332, 340, 348, 356, 364, 372, 380 |
| `test_r7_1_unparseable_temporary_live_and_archived_refuses_with_filename` | `red_R7PublicationTemporaryTest.log` | 388, 399, 410, 421, 432, 443, 454, 465, 476, 487, 498, 509, 520, 531, 542, 553, 564, 575 |
| `test_r7_2_nested_manifest_requires_floor_100_and_reserves_101` | `red_R7ArchivePrecisionTest.log` | 34 |
| `test_r7_2_utf16_jsonl_refuses_unchanged_and_names_file` | `red_R7ArchivePrecisionTest.log` | 78 |
| `test_r7_2_nested_generation_refuses_unchanged_and_names_file` | `red_R7ArchivePrecisionTest.log` | 12, 23 |
| `test_r7_2_unknown_archive_format_refuses_unchanged_and_names_file` | `red_R7ArchivePrecisionTest.log` | 45 |
| `test_r7_2_unparseable_archived_json_and_jsonl_refuse_with_filename` | `red_R7ArchivePrecisionTest.log` | 56, 67 |

Final verification: **25 tests OK, 0 skipped** (16 new + 9 existing, including 5 r6). The final source uses the same named UTF-8 rejection helper for payloads and preserved counters; after that diagnostic consistency change, only these same three classes were rerun once. The earlier successful targeted receipts are preserved separately; counts below refer to the final runs, not sums of repeated runs.

| Class | Tests OK | Skips | Final receipt |
| --- | --- | --- | --- |
| `R7PublicationTemporaryTest` | 11 | 0 | `results/backup_gdrive_mb24_20261010T194953Z/green_final_R7PublicationTemporaryTest.log` |
| `R7ArchivePrecisionTest` | 5 | 0 | `results/backup_gdrive_mb24_20261010T194953Z/green_final_R7ArchivePrecisionTest.log` |
| `R5RecoveryTest` | 9 | 0 | `results/backup_gdrive_mb24_20261010T194953Z/green_final_R5RecoveryTest.log` |

Each class ran with this command, substituting the class name:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_NO_RCLONE=1 BACKUP_TEST_RECEIPTS=$PWD/results/backup_gdrive_mb24_20261010T194953Z/fixtures /opt/homebrew/bin/rtk proxy .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.<Class> -v
```

There are 18 live/archive floor pairs, each proving floor 10 refuses without any file/directory/lock mutation and floor 100 reserves counter/barrier 101 while keeping temporary/archive bytes intact. The lock regression injects each of the nine payload/location forms live and archived after the pre-lock scan (18 cases), then proves floor 10 refuses with the entire injected snapshot unchanged. Invalid-temporary coverage adds 18 live/archive cases. Archive tests cover `recoveries/old/nested/manifest.json`, multiline UTF-16 JSONL, nested generation fields in objects and arrays, unknown archive extensions and wholly unparseable JSON/JSONL.

The copied `real_path_listing.py` saved `real_paths_before_final2.json` and `real_paths_after_final2.json`; `cmp` exited 0. SHA-256 of each: `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99` (21 inventory rows). The initial and first-targeted-run before/after listings also match. Every unittest temporary root was forced below `results/backup_gdrive_mb24_20261010T194953Z/fixtures/`, including cleanup. No protected real-HOME sink was created, changed or removed.

### Recovery command, updated evidence list and refusal rule

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be operator-reviewed and cover every observed generation from the current raw counter, current unresolved issued state, current heartbeat, current launch receipt, every independently parseable current failure-journal line, current `refusals/latest-refusal.json`, **every known publication temporary in the four live writer directories listed above**, every preserved recovery manifest at any recursive depth, every archived raw counter, every archived JSON/JSONL payload and **every known archived publication temporary**. Older directories count even when newer manifests have lower maxima. Top-level generation fields include launch_generation, issued_generation, recovery_barrier, compaction_barrier, highest_seen and generation_floor. `.journal.*` is parsed line by line and `.counter.*` as an integer; `.recovery.*` supports the publisher's JSON and integer forms.

Both scans use the complete same evidence set. A floor below the observed maximum refuses nonzero with `recovery refused` / `below observed maximum`; the pre-lock refusal creates no directory or lock and changes no bytes. Unsupported temporary/archive encodings, formats or nested generation layouts refuse nonzero and name the file instead of treating it as absent. A higher temporary, archive record or refusal injected between scans refuses under lock without moving or publishing recovery evidence. Crash-left temporary bytes remain exactly in place on refusal and success. Exit 75 remains observed history, not an unresolved backup failure; recovery itself never establishes health, and manual completion/refusal cannot discharge a recovery or compaction barrier. Fixtures must keep explicit `--heartbeat`; operator recovery/activation remains blocked until re-review GO.

### Exact MAESTRO19 host commands and remaining handoff

Run from this worktree once:

```sh
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash results/backup_gdrive_mb24_20261010T194953Z/host_full_addendum_mb24.sh
```

The script below runs the full addendum suite exactly once, in a fresh local receipt root; it records real-path listings before/after even when tests fail, compares them and returns the test or inventory failure. It deliberately clears the builder-only no-rclone switch for MAESTRO's host local-fixture suite. Expected host count is MB21's 109 addendum tests + 16 new = 125, with 0 skipped; MB24 has not run it. No new native case exists because the applet and wrapper are byte-identical.

```sh
#!/bin/bash
set -eu
mb24_build_receipt=results/backup_gdrive_mb24_20261010T194953Z
mb24_host_receipt=$(/opt/homebrew/bin/rtk proxy /usr/bin/mktemp -d /private/tmp/backup_gdrive_mb24_host.XXXXXX)
/opt/homebrew/bin/rtk proxy /bin/mkdir "$mb24_host_receipt/fixtures"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb24_build_receipt/real_path_listing.py" "$mb24_host_receipt/real_paths_before.json"
if LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb24_host_receipt/fixtures" \
  /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE \
  .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v \
  > "$mb24_host_receipt/full_addendum.log" 2>&1; then
  mb24_suite_rc=0
else
  mb24_suite_rc=$?
fi
printf '%s\n' "$mb24_suite_rc" > "$mb24_host_receipt/full_suite_exit_code.txt"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb24_build_receipt/real_path_listing.py" "$mb24_host_receipt/real_paths_after.json"
if /opt/homebrew/bin/rtk proxy /usr/bin/cmp \
  "$mb24_host_receipt/real_paths_before.json" "$mb24_host_receipt/real_paths_after.json"; then
  printf 'identical\n' > "$mb24_host_receipt/inventory_comparison.txt"
else
  printf 'DIFFERENT\n' > "$mb24_host_receipt/inventory_comparison.txt"
  printf 'MB24 host inventories differ; receipts: %s\n' "$mb24_host_receipt" >&2
  exit 1
fi
printf 'MB24 host full addendum exit %s; receipts: %s\n' "$mb24_suite_rc" "$mb24_host_receipt"
exit "$mb24_suite_rc"
```

Next: MAESTRO19 runs that host command, inspects its logs/inventory equality, and submits final source hashes plus these RED/GREEN/scope receipts to Astra. Activation remains BLOCKED until re-review GO. No source change is half-applied and no targeted test remains failing.

**Binding context directive for this handoff:** watch `Context N% left` for this and every team session. Start a new piece of work only at 60% left or more; at 40% left or less stop starting work, append a handoff with done/in-flight/half-applied state, exact paths and hashes, failing test commands and next step, and reply exactly `CONTEXT HANDOFF WRITTEN`. If `Context compacted` appears, do that immediately. The AGENTS Team mode and Context management sections continue to bind; no commits, real/native runs or out-of-scope edits by the builder. Every successor handoff must restate the directive.

## MB25 — Astra r8 findings 2 and 3: current state and duplicate-key refusal (2026-10-10)

**BUILD DONE; activation remains BLOCKED until Astra re-review says GO.** Branch `worktree-c10k-route-a`; MB24 commit `dba3a2c` is an ancestor of the current checkout. All four supplied SHA-256 pins matched before any edit. Receipts: `results/backup_gdrive_mb25_20261010T202206Z/`. MAESTRO22 verifies on the host and commits; MB25 has not committed, pushed or merged.

Only `recover.inspect_history` changed in the status tool. Current `unresolved.json` now enters the same UTF-8, JSON-object, nested-generation and generation-field checks as strict scanner evidence, before the existing state-schema loader runs. Both pre-lock and under-lock scans use this path. JSON decoding rejects duplicate keys at every object depth using an object-pairs hook. A distinct duplicate-key exception is handled before the existing torn-line `except ValueError`, and is re-raised with the evidence filename. Refused evidence is never normalized or rewritten.

### Start and final SHA-256

| File | Start | Final |
| --- | --- | --- |
| `tools/backup_gdrive_status.py` | `6140a7e1d0b122ee30c93bfbfb5861a99851a7dcd1788cc23a21e355deff3046` | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` |
| `tools/test_backup_gdrive_addendum.py` | `5e22410abde8debbefdce4810b3f455a5b62189371f715e2ed59a03f5d68806c` | `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e` |
| `tools/launchd/MemitGdriveBackup.applescript` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` |
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| `results/backup_gdrive_build_report.md` | `7f198ae9f844324531e88545eece8a5128b72f41d6ece957f2618b7892e93dff` | Recorded after append in `results/backup_gdrive_mb25_20261010T202206Z/final_sha256.txt` |

The report digest is stored outside the report to avoid self-reference. Newly created receipt files start ABSENT; final digests are in the same ledger, excluding the ledger itself. `scope_checks.json` proves identical status bytes outside `inspect_history`, identical bytes for every pre-existing test and fixture, unchanged applet/wrapper, identical copied inventory helper, and unchanged new tests between RED and GREEN. The report's pre-existing prefix is preserved byte for byte and re-read after an intervening operation.

### Behavioral RED index and final GREEN

`red_index.json` records the unchanged scanner hash `6140a7e1d0b122ee30c93bfbfb5861a99851a7dcd1788cc23a21e355deff3046`, the test hash, and each failure line. All **11 new refusal tests have behavioral REDs** (18 failed subcases), with no import/runtime errors or skips. The twelfth new test is the explicitly required torn-final-JSONL preservation control: it passes on unchanged MB24 and on the final code. Its baseline GREEN is retained in the RED-phase log; no failing result is claimed for that control. All adverse payloads were written as raw bytes, including the exact Astra nested-state and duplicate-key strings, rather than dictionaries or scanner helpers.

All log names below are relative to `results/backup_gdrive_mb25_20261010T202206Z/`.

| New test | RED-phase log | Failure lines |
| --- | --- | --- |
| `test_r8_2_current_unresolved_nested_generation_pre_lock_refuses_unchanged` | `red_R8CurrentUnresolvedTest.log` | 21 |
| `test_r8_2_current_unresolved_validation_under_lock_refuses_unchanged` | `red_R8CurrentUnresolvedTest.log` | 42, 52, 62 |
| `test_r8_2_current_unresolved_non_utf8_refuses_with_filename` | `red_R8CurrentUnresolvedTest.log` | 32 |
| `test_r8_2_current_unresolved_invalid_generation_field_refuses_with_filename` | `red_R8CurrentUnresolvedTest.log` | 10 |
| `test_r8_3_archived_json_duplicate_keys_refuse_unchanged_with_filename` | `red_R8DuplicateKeysTest.log` | 18 |
| `test_r8_3_live_json_duplicate_keys_refuse_unchanged_with_filename` | `red_R8DuplicateKeysTest.log` | 107 |
| `test_r8_3_recognized_json_temporary_duplicate_keys_refuse_unchanged_with_filename` | `red_R8DuplicateKeysTest.log` | 142 |
| `test_r8_3_jsonl_duplicate_keys_refuse_instead_of_torn_line_tolerance` | `red_R8DuplicateKeysTest.log` | 94 |
| `test_r8_3_current_unresolved_duplicate_keys_refuse_unchanged_with_filename` | `red_R8DuplicateKeysTest.log` | 31 |
| `test_r8_3_duplicate_keys_under_lock_refuse_every_evidence_location_unchanged` | `red_R8DuplicateKeysTest.log` | 44, 54, 64, 74, 84 |
| `test_r8_3_nested_duplicate_keys_refuse_unchanged_with_filename` | `red_R8DuplicateKeysTest.log` | 120, 131 |
| `test_r8_3_genuinely_torn_final_jsonl_line_remains_tolerated` | `red_R8DuplicateKeysTest.log` | baseline GREEN; preservation control |

Final verification: **28 tests OK, 0 skipped**, each class run once after the scanner edit. Only the two new test classes and both expressly required R7 test classes ran; no full addendum/base suite or repeated-run loop ran.

| Class | Tests OK | Skips | GREEN log |
| --- | --- | --- | --- |
| `R8CurrentUnresolvedTest` | 4 | 0 | `green_R8CurrentUnresolvedTest.log` |
| `R8DuplicateKeysTest` | 8 | 0 | `green_R8DuplicateKeysTest.log` |
| `R7PublicationTemporaryTest` | 11 | 0 | `green_R7PublicationTemporaryTest.log` |
| `R7ArchivePrecisionTest` | 5 | 0 | `green_R7ArchivePrecisionTest.log` |

Exact per-class command, substituting only the class name:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_NO_RCLONE=1 BACKUP_TEST_RECEIPTS=$PWD/results/backup_gdrive_mb25_20261010T202206Z/fixtures /opt/homebrew/bin/rtk proxy .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.<Class> -v
```

`commands.txt` records all executed class commands and receipt destinations. The four current-state tests cover the exact nested evidence, a non-UTF-8 file, an invalid generation-field type and injection of each layout after the first scan. Duplicate-key tests cover archived `recoveries/old/x.json`, a live receipt, a recognized `.last_run.*` temporary, a canonical JSONL line, current unresolved state and nested objects/arrays. Under-lock duplication is injected at all five evidence locations. The injection fixtures precreate `counter.lock`, confirm injection happened at `flock` after the first scan, and compare the entire post-injection file/directory snapshot with the refused result. Pre-lock fixtures assert nonzero exit, the filename and no new directory or lock; every evidence byte remains identical.

The torn-line control proves independently valid generation 100 still requires floor 100, reserves counter/barrier 101, and archives the journal with its torn final line byte-identical. All 16 R7 tests remain GREEN, including every publication prefix live/archived, recursive manifests, archive format/encoding/nested-field rejection, and under-lock rescan. Existing MB14 replay/refusal-heartbeat tests, strict `completed > barrier`, 64-interval/2,048-byte bounds, owner-preserving exit 75, read-only status and r4 manual-interleave tests/code remain unchanged. Earlier behavior outside the two required R7 classes is **HOST-PENDING**, not re-executed or newly claimed by MB25.

### Real-path isolation

The helper is a byte-identical copy of `results/backup_gdrive_mb24_20261010T194953Z/real_path_listing.py`. `real_paths_before_final.json` and `real_paths_after_final.json` match; `cmp` exited 0. Both hashes are `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99` (21 inventory rows). `real_paths_before_red.json` also matches the final listing. `scope_checks.json` independently asserts all three byte identities. All unittest temporary roots and their cleanup were confined to `results/backup_gdrive_mb25_20261010T202206Z/fixtures/`; no real HOME Logs sink, Applications app or LaunchAgents path was created, modified or deleted.

### Recovery command, updated evidence list and refusal rule

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be operator-reviewed and cover the current raw counter; **all supported top-level generation fields in current `unresolved.json`**; heartbeat, launch receipt, independently parseable current failure-journal records and `refusals/latest-refusal.json`; every known publication temporary in the heartbeat, refusals, launch-state and launch-journal directories; and every recursive recovery manifest, archived raw counter, archived JSON/JSONL payload and recognized archived temporary. Fields counted are `launch_generation`, `issued_generation`, `recovery_barrier`, `compaction_barrier`, `highest_seen` and `generation_floor`. Older directories remain evidence even when newer maxima are lower. All six existing temporary prefixes and their JSON/JSONL/integer format rules remain as in MB24.

Both scans inspect that complete evidence set before recovery publication. Unsupported encoding, nested generation layout, invalid strict generation field, duplicate JSON key, unsupported archive format or unparseable strict publication refuses nonzero and names the evidence file. Current unresolved state follows the same scanner checks; duplicates in JSONL are refused rather than swallowed as torn lines. Pre-lock refusal creates no directory/lock and changes no bytes. Unsupported or higher evidence injected after the first scan refuses under lock without publishing or moving recovery evidence; all bytes and directories present at injection remain unchanged. A floor below the observed maximum still refuses with `below observed maximum`.

The supported exceptions remain damaged UTF-8 canonical raw counters and genuinely torn canonical/archived JSONL retaining independently parseable records. Temporary JSONL retains its existing stricter publication rule. Null-generation final receipts remain ambiguous evidence. Recovery reserves a barrier and does not establish health; subsequent completed generation must be strictly greater than the barrier. Manual completion/refusal cannot discharge recovery/compaction barriers, and exit 75 remains observed owner-preserving history. Preserve every refused file's raw bytes. Fixtures keep explicit `--heartbeat`; operator recovery and activation remain BLOCKED pending re-review GO.

### Exact MAESTRO22 host commands and handoff

From this worktree, run this prepared command once:

```sh
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash results/backup_gdrive_mb25_20261010T202206Z/host_full_suites_mb25.sh
```

The script is saved for review and passes `bash -n`; MB25 has not executed it. It creates one fresh `/private/tmp/backup_gdrive_mb25_host.*` receipt root, records real-path listings before and after both suites even when a suite fails, compares them, and propagates suite/inventory failures. It clears the builder-only `BACKUP_TEST_NO_RCLONE` switch for MAESTRO's host local-fixture tests. It runs these two suite commands exactly once each, with `BACKUP_TEST_RECEIPTS` set to that root's `fixtures/` directory:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb25_host_receipt/fixtures" /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb25_host_receipt/fixtures" /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE .venv/bin/python -B -m unittest tools.test_backup_gdrive -v
```

Expected host counts: **137 addendum tests OK (MB24's 125 + 12), 10 base tests OK, 0 skipped**, with identical inventories. The script validates these counts and saves full logs/exit codes. MAESTRO22 then submits final source hashes and RED/GREEN/scope receipts to GPT-6-Astra for re-review. No applet/wrapper edit or new native case was needed. No source change is half-applied and no targeted test remains failing. No native launch, install, launchd mutation, rclone or network call ran here; no deletion occurred outside this receipt directory.

**Binding context directive for this handoff:** watch `Context N% left` for this and every team session. Start a new piece of work only at 60% left or more; at 40% left or less stop starting work, append a handoff giving done/in-flight/half-applied state, exact paths and SHA-256, failing test commands and next step, then reply exactly `CONTEXT HANDOFF WRITTEN`. If `Context compacted` appears, do this immediately. AGENTS Team mode and Context management remain binding; no commits, real/native runs or out-of-scope edits by the builder. Every successor handoff must restate this directive.
