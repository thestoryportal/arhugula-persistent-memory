# MB32 locked Google Drive backup release

MB34 locked-release fixture receipts are **GREEN** after the runner-only auditor repair. The new `green_success` Python 3.9.6 suite is **151 run, 133 passed, zero failures/errors, 18 skipped; exit 0**. The targeted `clearance_fix_red` reproduction is **1 run, 1 failure, zero errors/skips; exit 1**; `clearance_fix_green` is **1 run, 1 passed, zero failures/errors/skips; exit 0**. All earlier runs, including the failed `green_final` (151 run, 1 auditor failure, 18 skips; exit 1), remain untouched. All 14 MB32 release tests were RED against original product bytes; `red_verified_original` retains 14 failures, zero errors/skips; exit 1. Native compilation, app execution and full decompile comparison remain **UNVERIFIED**, with the same 18 skips listed below. No activation or production app was created.

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

Every suite run has `command.json`, `test.log`, `result.json`, `tool_completion.json`, `started_processes.jsonl`, `process_clearance.jsonl` and `process_clearance.json`. Each command and its actual exit code are preserved. The initial failed GREEN attempt is retained: a Perl literal placeholder regex did not match; a minimal probe reproduced it, and using a variable placeholder corrected it. The first full GREEN run preceded the final native script-file path correction and the extra fixture/child evidence capture; `green_final` exercised the final product bytes, but its process audit failed. MB34 reproduced that defect before changing the runner and captured fresh targeted/full GREEN receipts. Each MB34 `command.json` records the exact interpreter command, execution wrapper, cwd, resolved interpreter and SHA-256 of the runner, applet, builder, stager, wrapper, status tool, excludes and test file. The unmodified RED runner was hashed before and after reproduction; GREEN metadata is written by the runner before loading tests.

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
| `clearance_fix_red` | 1 | 1 | 0 | 0 | 1 | 5 |
| `clearance_fix_green` | 1 | 0 | 0 | 0 | 0 | 5 |
| `green_success` | 151 | 0 | 0 | 18 | 0 | 1914 |

## Process-record sizes (bytes)

| Suite run | process_clearance.json | process_clearance.jsonl | started_processes.jsonl |
|---|---:|---:|---:|
| `red_new` | 186,385 | 180,240 | 172,725 |
| `red_final` | 175,400 | 169,255 | 161,740 |
| `red_build_id` | 3,080 | 2,298 | 1,719 |
| `green_new` | 38,790 | 32,001 | 23,938 |
| `green_new_final` | 206,814 | 198,891 | 189,897 |
| `red_verified_original` | 176,009 | 169,758 | 162,155 |
| `green_full` | 6,258,233 | 6,097,317 | 5,907,241 |
| `green_final` | 6,289,204 | 6,129,514 | 5,907,726 |
| `clearance_fix_red` | 4,780 | 4,543 | 2,927 |
| `clearance_fix_green` | 4,234 | 3,555 | 2,935 |
| `green_success` | 6,262,559 | 6,105,119 | 5,908,696 |

`green_final` has approximately 6 MB per file (6,289,204 / 6,129,514 / 5,907,726 bytes). `green_success` is similar: 6,262,559 / 6,105,119 / 5,908,696 bytes. The targeted runs are much smaller, roughly 3–5 KB per file. All records are retained without truncation.


Exact MB32 RED and failed final commands (the runner creates an isolated HOME and refuses reuse of a run directory):

```sh
LLMDB_ROOT="$PWD" /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py red_verified_original LockedReleaseTest --original-launcher
```
```sh
LLMDB_ROOT="$PWD" /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py green_final all
```

The suite is invoked with `/usr/bin/python3 -B` (3.9.6); macOS resolves that shim to `/Library/Developer/CommandLineTools/usr/bin/python3`, which is also `sys.executable` used by fixture helpers. `HOME`, `LLMDB_ROOT`, `BACKUP_TEST_NO_RCLONE=1`, `PYTHONDONTWRITEBYTECODE=1`, `BACKUP_TEST_RECEIPTS` and the Python settings are recorded in each command receipt. Release/native fixture HOMEs are under `/private/tmp`, because a receipt-dir HOME in this worktree would itself be inside a git checkout. Other safe fixtures use receipt-dir HOMEs. No tests write the real `~/Library` or `~/Applications`.

Final MB34 clearance: **1,914 directly started process leaders, all reaped, every owned process group absent before containment**. There are 5 confirmed in-group heartbeat child records; none remained a live member of an owned group at audit. The targeted GREEN records no child for the synthetic runner PID. The RED retained PID 13192 as the false child, identical to its `command.json` runner PID. Both observation and final audit now exclude `os.getpid()` and require actual live membership (`kill(pid, 0)` plus `getpgid(pid)`) in a group recorded for that test. Direct-process/group detection keeps its original 0.5-second grace period and failure semantics. Child leak evidence is recorded before failed-group containment, so killing a genuine leak cannot erase its report. Only an owned group can be killed; complete group absence still covers transient shell/Perl/Python descendants. `/bin/ps` was freshly probed and sandbox-denied (UNAVAILABLE). No real rclone, Drive, launchctl, commits, pushes or merges were performed.

`green_success/fixture_artifacts/<test>/` preserves the actual fixture receipts, counters, dispatched path markers, rendered AppleScripts and release snapshots before temporary directories are cleaned. These copies are evidence only; their temporary release paths are not deployment paths. Full skip diagnostics and positive-control output are in `green_success/result.json`, `test.log` and `runner_stdout.log`. `green_final` retains its original fixture artifacts and diagnostics.

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

Shell syntax checks and scoped `git diff --check` passed; observations are in `preflight_checks.json`. MB32 counts/hashes remain in the untouched `evidence.json`; MB34 results, file sizes and scope verification are in `mb34_evidence.json`. Product bytes remain pinned. MB34 code changes are confined to `run_suite.py` and the new auditor fixture in this receipt tree; MB33 work and `tools/test_dashboard_mathlab.py` were left alone.


## MB34 auditor fixture

`test_clearance_auditor.py` loads the exact runner auditor definitions without running its CLI. It uses real local process groups, live outsider PIDs and a child that moves groups. The genuine-leak control starts a live leader and child in one owned group, confirms the child is observed, asserts the nested audit reports both PIDs and fails, and verifies both processes are reaped and the group is absent. The fixture reaps both of its direct children before probing a zombie-only group, which the sandbox otherwise denies.

| Fixture run | Tests | Failures | Errors | Skips | Exit | Nested clearance JSONL total bytes |
|---|---:|---:|---:|---:|---:|---:|
| `auditor_fixture_red` | 5 | 2 | 3 | 0 | 1 | 966 |
| `auditor_fixture_red_verified` | 5 | 5 | 0 | 0 | 1 | 1,508 |
| `auditor_fixture_green` | 5 | 0 | 0 | 0 | 0 | 1,508 |

The first fixture-authoring attempt had a missing `sys` binding and a zombie-group probe error; it is preserved. The corrected fixture was rerun against the saved pre-fix runner: **5 failures, zero errors/skips; exit 1**. Against the fixed runner it is **5 passed, zero failures/errors/skips; exit 0**, including the genuine leak control. Standalone fixture runs have per-case clearance JSONL, rather than suite-level `process_clearance.json` or `started_processes.jsonl`. Their commands, audited-runner hashes, pinned product/test hashes, fixture source snapshots and tool exit receipts are saved separately.

```sh
/usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/test_clearance_auditor.py auditor_fixture_red_verified results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/before/run_suite.py
```

```sh
/usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/test_clearance_auditor.py auditor_fixture_green results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py
```

## Context saved / MB34 completion

Done: preserved original runner and README; reproduced the synthetic-PID failure; verified five auditor fixtures RED→GREEN; captured clean targeted/full GREEN logs, hashes, source snapshots, exact interpreter commands, process records and actual exit codes. Half-applied: none. In flight: none. Status: **DRIVE RECEIPTS DONE**. The original MB32 context handoff is preserved in `before/README.mb32.md`.

Changed code paths and current SHA-256:

- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py` — `5065464f1f61e957011f361ae48d8af1a85cd52fdecdcb40710c30d125b1fe3d`; pre-fix copy `before/run_suite.py` — `268af4e2907ea54b289da7c2936aac0edac5245efae0bb57d85ca3a157454623`.
- `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/test_clearance_auditor.py` — `cdc4187c0abc4808ab55c12ceb9315c8651b05066921f9fbfef9e1947450fe58`.

Exact MB34 suite commands (cwd `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; `/usr/bin/python3`, resolving to `/Library/Developer/CommandLineTools/usr/bin/python3`):

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py clearance_fix_red StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs
```

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py clearance_fix_green StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs
```

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py green_success all
```

The targeted RED has 1 auditor failure / exit 1; targeted GREEN has 1 pass / exit 0; full GREEN has 151 run, 133 passed, zero failures/errors, 18 skips / exit 0. No failing tests remain in the accepted runs. The 18 skipped cases remain host-pending or native-unverified as listed above. Next: MAESTRO owns the separately authorized host reruns and Astra re-review before activation. No product file changed during MB34, and all earlier receipt files other than this README and the authorized runner edit were rehashed unchanged.

Binding context directive: watch "Context N% left" for this session and every orchestrated session. Start a new piece of work only at 60% left or more. At 40% left or less, or any "Context compacted", stop starting work; write a handoff at the end of this README with what is done/half-applied, exact paths and SHA-256 of changed files, failing tests and exact commands, and the next step; reply exactly "CONTEXT HANDOFF WRITTEN". Preserve this directive in every successor handoff.
