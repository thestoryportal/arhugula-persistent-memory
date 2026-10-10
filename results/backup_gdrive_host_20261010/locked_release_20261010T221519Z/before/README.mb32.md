# MB32 locked Google Drive backup release

STOPPED at the operator's 38% context gate. Final Python 3.9.6 suite: **151 run, 132 passed, 1 clearance-auditor failure, 18 skipped, zero errors; exit 1**. The earlier full GREEN was **151 run, 133 passed, 18 skipped; exit 0**. The final run's test-method assertions all passed; the recorder added one failure after a status test deliberately used the runner's own PID as a synthetic child. This is an unfixed observation-layer defect, so the final run is not accepted as GREEN. All 14 new tests were RED against original production bytes before implementation. The final test definitions were also rerun against the saved original launcher: **14 failures, zero errors/skips; exit 1**. Native compilation, app execution and full decompile comparison remain **UNVERIFIED**, with every skip listed below for MAESTRO host rerun. No activation or production app was created.

Authority: [Astra r10](../astra_r10_verdict.md), item 1 third paragraph and item 5, plus the MB32 brief. This is backup infrastructure hardening supporting durable research evidence, not scientific evidence or an F1 closure. Other r10 items belong to the later builder.

## Design and release layout

`stage_gdrive_release.sh <git-commit> <release-id> <rendered.applescript> [release-root]` resolves the commit once, extracts each of the three payload files with `/usr/bin/git show <resolved-commit>:tools/<file>`, computes the MANIFEST, and stamps the template. The three files never come from the working tree. It resolves release-root symlinks and refuses a `.git` ancestor in any checkout/worktree, including an unrelated checkout. An exclusive directory reservation refuses reuse of an existing release id. A failed staging/build is kept for inspection and requires a fresh id for another attempt.

```text
$HOME/Library/Application Support/memit-gdrive-backup/releases/<release-id>/  (0555)
  backup_gdrive.sh         (0444)
  backup_gdrive_status.py  (0444)
  backup_mirror.excludes   (0444)
  MANIFEST                (0444; SHA-256 of the preceding three named files)
```

Exactly these four entries are allowed. `build_gdrive_applet.sh <git-commit> <release-id> <output.app> [release-root]` calls the stager, canonicalizes rendered source through a temporary compiled script, then compiles the app **from the exact saved canonical source** `<output.app>.applescript`. It decompiles the bundle's `Contents/Resources/Scripts/main.scpt` into `<output.app>.decompiled.applescript` and runs `/usr/bin/cmp` over both full files. Those sidecars become read-only. The builder also prints a SHA-256 inventory of every bundle file through one checked Perl process, avoiding hidden pipeline/find-exec failures. Its interface now requires the commit and release id; MAESTRO must update activation invocations accordingly. The staged release stays outside checkouts; keep the reviewed app and its source sidecars outside pullable checkouts as well.

The compiled applet contains the absolute release wrapper path and four expected SHA-256 values (all payload files plus MANIFEST). Each run uses system `/usr/bin/perl` with Digest::SHA to hash them and check the complete entry set; `PERL5LIB` and `PERL5OPT` are cleared for this check. The gate never derives its expectations from MANIFEST at runtime. Missing, altered, unreadable, nonregular or symlink files, an extra entry, or a failed checker suppress dispatch. Receipt `integrity_failures` contains the offending filename, `expected_sha256` and `actual_sha256`; absent/unreadable objects use explicit sentinels such as `MISSING`, and extra files use expected `ABSENT`. Integrity refusals have exit code 78 and use the existing launch receipt and failure journal mechanisms. Files are read-only after staging; this is not protection against the owner deliberately changing permissions and racing a run.

## Generation choice

**Reserve the generation before the integrity check.** Every integrity refusal can then publish a sequenced failure receipt at `$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json`, with the existing independent failure journal and unresolved-generation behavior. This prevents a fresh old heartbeat from silently hiding the failed launch. Allocation failure remains fail-closed through the existing caught error boundary. Hashing still occurs before any wrapper dispatch, and a mismatch never reaches the wrapper. The wrapper and status tool remain byte-identical, including their existing generation semantics.

## New tests to requirements

All rows belong to `LockedReleaseTest` in `tools/test_backup_gdrive_addendum.py`. Shell tests obtain dispatch composition from the actual applet source and execute the same literal sequence with stamped fixture paths. Native tests load the compiled bundle's `main.scpt`. All use tiny committed fixture payloads; no real rclone or Drive.

| New test | Requirement | What is checked |
|---|---|---|
| `test_good_release_dispatches_release_path` | 1, 3, 5a | release wrapper path; generation; receipt; exact four-file layout; read-only files/directory |
| `test_changed_wrapper_byte_refuses` | 3, 5b | no dispatch; file and expected/actual SHA-256 in receipt |
| `test_changed_status_byte_refuses` | 3, 5b | no dispatch; file and expected/actual SHA-256 in receipt |
| `test_changed_excludes_byte_refuses` | 3, 5b | no dispatch; file and expected/actual SHA-256 in receipt |
| `test_changed_manifest_byte_refuses` | 3 | MANIFEST itself is also checked against a compiled stamp |
| `test_missing_file_refuses` | 3, 5c | receipt has expected digest and MISSING; generation reserved; no dispatch |
| `test_extra_file_refuses` | 3, 5c | receipt has ABSENT and the extra file digest; no dispatch |
| `test_checkout_pull_cannot_change_dispatch` | 2, 5d | change fixture checkout after staging; release bytes still dispatch |
| `test_existing_release_id_refused_without_overwrite` | 2, 5e | build refuses existing id before compiling; all original release bytes preserved |
| `test_dirty_checkout_stages_commit_bytes` | 2, 5e | dirty all three fixture files; git-show commit bytes are staged |
| `test_release_inside_another_checkout_refused` | 1 | even an unrelated git checkout is refused |
| `test_rendered_source_stamps_release_and_all_four_hashes` | 2, 3 | rendered wrapper path and all four hashes are stamped |
| `test_compiled_app_full_source_equals_saved_source` | 2, 5f | full byte equality with compiled main.scpt source; UNVERIFIED in sandbox |
| `test_compiled_app_dispatches_release_after_checkout_change` | 5a, 5d | osascript loads compiled main.scpt after checkout change; UNVERIFIED in sandbox |

The existing launcher smoke and builder tests were adapted to the new template/build interface while keeping their error-boundary and complete bundle-hash assertions.

## Runs, commands and process clearance

Every run has `command.json`, `test.log`, `result.json`, `tool_completion.json`, `started_processes.jsonl`, `process_clearance.jsonl` and `process_clearance.json`. Each command and its actual exit code are preserved. The initial failed GREEN attempt is retained: a Perl literal placeholder regex did not match; a minimal probe reproduced it, and using a variable placeholder corrected it. The first full GREEN run preceded the final native script-file path correction and the extra fixture/child evidence capture; `green_final` exercised the final bytes, but its process audit failed.

| Run | Tests | Failures | Errors | Skips | Exit | Direct processes |
|---|---:|---:|---:|---:|---:|---:|
| `red_new` | 14 | 14 | 0 | 0 | 1 | 65 |
| `red_final` | 14 | 14 | 0 | 0 | 1 | 65 |
| `red_build_id` | 1 | 1 | 0 | 0 | 1 | 5 |
| `green_new` | 14 | 13 | 0 | 0 | 1 | 71 |
| `green_new_final` | 14 | 0 | 0 | 2 | 0 | 82 |
| `red_verified_original` | 14 | 14 | 0 | 0 | 1 | 66 |
| `green_full` | 151 | 0 | 0 | 18 | 0 | 1914 |
| `green_final` | 151 | 1 | 0 | 18 | 1 | 1914 |

Exact final RED and GREEN commands (the runner creates an isolated HOME and refuses reuse of a run directory):

```sh
LLMDB_ROOT="$PWD" /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py red_verified_original LockedReleaseTest --original-launcher
```
```sh
LLMDB_ROOT="$PWD" /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py green_final all
```

The suite is invoked with `/usr/bin/python3 -B` (3.9.6); macOS resolves that shim to `/Library/Developer/CommandLineTools/usr/bin/python3`, which is also `sys.executable` used by fixture helpers. `HOME`, `LLMDB_ROOT`, `BACKUP_TEST_NO_RCLONE=1`, `PYTHONDONTWRITEBYTECODE=1`, `BACKUP_TEST_RECEIPTS` and the Python settings are recorded in each command receipt. Release/native fixture HOMEs are under `/private/tmp`, because a receipt-dir HOME in this worktree would itself be inside a git checkout. Other safe fixtures use receipt-dir HOMEs. No tests write the real `~/Library` or `~/Applications`.

Final clearance: **1914 directly started process leaders, all reaped, every owned process group absent**. The recorder contains 57 observed child records: all except one were absent at their checks. The one marked alive is PID 63963, which `command.json` identifies as the runner itself. The status test deliberately paired that PID with a dead subprocess PID; the recorder trusted that synthetic heartbeat as ownership proof. The runner then exited 1, corroborated by `tool_completion.json`. No real child leak was shown, but the child-auditor result remains failed and must be repaired/reverified. Each test uses dedicated process sessions and is failed if its leader/group remains alive after cleanup; only its own group can be killed for failed-test containment. Group absence also covers shell/Perl/Python descendants whose transient PIDs are not separately enumerated. `/bin/ps` is sandbox-denied (UNAVAILABLE, not an idle claim). Operator-owned PIDs 32906, 32913, 32914, 36233, 36258, 36259, 37109 and 65807 were never targeted. No `open`, real rclone, Drive, launchctl, commits, pushes, merges, or deletions outside receipt/temp directories were performed.

`green_final/fixture_artifacts/<test>/` preserves the actual fixture receipts, counters, dispatched path markers, rendered AppleScripts and release snapshots before temporary directories are cleaned. These copies are evidence only; their temporary release paths are not deployment paths. Full skip diagnostics and positive-control output are in `green_final/result.json` and `test.log`.

## Every skip (18)

| Test | Status / reason |
|---|---|
| `ArchiveTest.test_corrupt_remote_download_check_does_not_create_receipt` | HOST-PENDING: real rclone forbidden |
| `ArchiveTest.test_differing_remote_is_immutable_and_preserves_prior_manifest` | HOST-PENDING: real rclone forbidden |
| `ArchiveTest.test_manifest_write_failure_is_loud` | HOST-PENDING: real rclone forbidden |
| `ArchiveTest.test_real_copy_download_check_and_sha_receipt_never_delete_source` | HOST-PENDING: real rclone forbidden |
| `ArchiveTest.test_source_drift_after_check_does_not_create_receipt` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_exit_publication_failure_is_loud_and_preserves_original_failure` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_native_nonregular_skip_is_recorded_as_warning` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_real_queued_source_vanish_is_warning_and_keeps_raw_exit` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_real_sync_publishes_actual_bytes_and_completed_success` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_remote_global_overrides_refuse_without_dispatch` | HOST-PENDING: real rclone forbidden |
| `HeartbeatTest.test_start_publication_failure_invalidates_previous_success` | HOST-PENDING: real rclone forbidden |
| `LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest` | UNVERIFIED: Standard Additions XPC sandbox failure, independently confirmed |
| `LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog` | UNVERIFIED: Standard Additions XPC sandbox failure, independently confirmed |
| `LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change` | UNVERIFIED: Standard Additions XPC sandbox failure, independently confirmed |
| `LockedReleaseTest.test_compiled_app_full_source_equals_saved_source` | UNVERIFIED: Standard Additions XPC sandbox failure, independently confirmed |

The 14 HOST-PENDING real-rclone skips are required by the no-rclone scope. The four native skips independently confirm the unavailable Standard Additions XPC service with a system `osascript` positive control; host compilation/execution/source equality is not claimed. MAESTRO reruns these tests on the host with the same isolation and process-clearance runner before activation review.

## Before and after SHA-256

`before/` holds the original copies of each existing changed file. The new helper is represented by `before/tools/launchd/stage_gdrive_release.sh.ABSENT`. The recorded hashes were rechecked after intervening operations.

| Changed file | Before SHA-256 | After SHA-256 |
|---|---|---|
| `tools/launchd/MemitGdriveBackup.applescript` | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` | `4e1e79eec6dab2944bda793814dbcd0ee4f7fd56cfb07a523a128bff9e38a428` |
| `tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` | `d467ef24968d512152f2e5d8ba5cc946ff1809acd8bfefeab850ba0cc8685076` |
| `tools/launchd/stage_gdrive_release.sh` | `ABSENT` | `b157637701cf8fd55eb121468c6852a49c7b911e2df8df25505762a36d5f3b9e` |
| `tools/test_backup_gdrive_addendum.py` | `b764938802edf101be01493d24012a586076ca9f00bbfba2193c70336e54fdf1` | `6eba5860e1fbb0c562af9a4241f8acf6f50d966d05b3d0e8ac66ec35e14e7d2c` |

| Protected file (unchanged before/after) | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| `tools/backup_gdrive_status.py` | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` |
| `tools/backup_mirror.excludes` | `45bb4e2a2e4629d494b6e5ccf41dd6885133b27e329a197fc6a85bcc55e48f3f` |

Shell syntax checks and scoped `git diff --check` passed; observations are in `preflight_checks.json`. All counts and hashes above are also in `evidence.json`. No other source file was edited; MB31's NEW1 receipt tree and `tools/test_dashboard_mathlab.py` were left alone.

## Context saved / MAESTRO handoff

Done: commit-only staging, stamped per-run integrity gate, full-source comparison build, 14 test-first release tests, unchanged pinned payloads, original-byte RED logs, one full GREEN run and the final failed audit run, actual fixture receipts/source snapshots, process records and this handoff. Half-applied: no partial production edits; the receipt runner's child-observation enhancement is applied but has the false positive described above and is not accepted. In flight: none; the final runner exited 1. Implementation and tests stopped immediately on the operator's 38% context instruction; no new tests or fixes were started afterward. Context compacted while finalizing the documentation; this handoff was written immediately and no new implementation or testing was started.

Changed files and current SHA-256 (absolute paths):

- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/launchd/MemitGdriveBackup.applescript` — `4e1e79eec6dab2944bda793814dbcd0ee4f7fd56cfb07a523a128bff9e38a428`
- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/launchd/build_gdrive_applet.sh` — `d467ef24968d512152f2e5d8ba5cc946ff1809acd8bfefeab850ba0cc8685076`
- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/launchd/stage_gdrive_release.sh` — `b157637701cf8fd55eb121468c6852a49c7b911e2df8df25505762a36d5f3b9e`
- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_backup_gdrive_addendum.py` — `6eba5860e1fbb0c562af9a4241f8acf6f50d966d05b3d0e8ac66ec35e14e7d2c`

Unfinished receipt runner: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py`; SHA-256 `268af4e2907ea54b289da7c2936aac0edac5245efae0bb57d85ca3a157454623`. Evidence and report writer: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/make_report.py`. The script-file path correction is final; all source hashes match `green_final/source_sha256.json`.

Failing test: `tools.test_backup_gdrive_addendum.StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs`, added by `ClearedResult.stopTest` in the receipt runner, with synthetic child PID 63963 equal to the runner PID. Full exact failed command (cwd `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`):

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py green_final all
```

Next step for a fresh successor: reproduce the child-auditor error with a new run id, exclude the runner PID and validate actual live owned-group membership before classifying a heartbeat PID as an owned child, then rerun the targeted case and the full suite in new run directories. Preserve the failed evidence. Exact targeted reproduction command:

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py clearance_fix_red StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs
```

After that repair, use `clearance_fix_green` for the targeted GREEN and `green_success all` for full verification. Update README/evidence with their actual counts/exit codes. MAESTRO then owns the listed host reruns and Astra re-review before any separately authorized activation. Keep wrapper/status bytes pinned; do not touch MB31's receipt tree or `tools/test_dashboard_mathlab.py`. Open risks: child-auditor ownership validation unfinished; native compilation/execution/full source equality still UNVERIFIED; no activation authorization is inferred.

Report writer SHA-256: `199b61717f4fdc990522349640792d87c4b5d0f6f79a38f3ac6a68b527a2356d`.

Binding context directive: watch "Context N% left" for this session and every orchestrated session. Start a new piece of work only at 60% left or more. At 40% left or less, or any "Context compacted", stop starting work, write a handoff at the end of this README with done/half-applied work, exact paths and SHA-256 of changed files, failing tests and exact commands, and the next step; reply exactly "CONTEXT HANDOFF WRITTEN". Preserve this directive in every successor handoff.
