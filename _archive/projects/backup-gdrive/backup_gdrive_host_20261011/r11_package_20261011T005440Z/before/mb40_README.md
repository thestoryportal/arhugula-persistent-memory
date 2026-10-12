# MB39 → MB40 handoff — incomplete Drive r11 package

MAESTRO instructed MB39 to stop after the in-flight suite at 49% context left. That suite has finished. No further fix or suite was started. This package is **not ready for MAESTRO's host runs or Astra r11**.

Receipt: `results/backup_gdrive_host_20261011/r11_package_20261011T005440Z/` (all relative paths below are within this receipt unless explicitly rooted). Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch `worktree-c10k-route-a`; launch HEAD `feb9ac4b60874594a31a2e16bd11a265bb591ec3`. No commits, pushes, remote operations, native execution, launchd actions, real HOME writes or process kills outside owned groups occurred. MAESTRO's `tools/closeout_check.py` and `tools/test_closeout_check.py` are excluded from all inventories of source hashes and from edits.

## Saved evidence

| Run | Counts / result | Complete log and exit |
|---|---|---|
| E initial harness attempt | 1 test, 4 subcase failures caused by incorrectly retained production shell scaffolding; INVALID as leak evidence | `e_red/stderr.txt`, `e_red/exit_code.txt` = 1 |
| E valid RED | 1 test, exactly 2 failing subcases: `generationShell` and `receiptShell`, parent HOME absent, Perl prints `UNSET`; sentinel parent passes | `e_red_valid/stderr.txt`, `e_red_valid/exit_code.txt` = 1 |
| E GREEN | 1 test passes; all four property/parent subcases pass; 0 skips | `e_green/stderr.txt`, `e_green/exit_code.txt` = 0 |
| Package initial RED | 33 tests, 13 failures, 18 errors, 2 passes; negative fixtures expose unsafe acceptance; missing runners/docs/pins account for errors | `package_red/stderr.txt`, `package_red/exit_code.txt` = 1 |
| Sandbox runner first attempt | No tests run; denied `/bin/ps` spawn raised PermissionError; inventories identical; implementation attempt preserved | `sandbox_non_native/result.json`, `sandbox_non_native/exit_code.txt` = 1 |
| Sandbox non-native suite | **151 run, 13 failures, 2 errors, 14 skipped**, 246.332 seconds; not GREEN | `sandbox_non_native_v2/test.log:325`, `sandbox_non_native_v2/result.json`, `sandbox_non_native_v2/exit_code.txt` = 1 |

The outer one-off driver for `e_red_valid` also exited 1 because its check for the substring `Error` mistakenly matched the expected `AssertionError` text. The unittest result is the valid RED above; its full stdout/stderr and child exit are saved. The valid RED source was copied separately before applying GREEN. Do not cite the initial four-failure attempt as proof of E.

The final sandbox suite reports `all_owned_groups_exited=true` and `real_inventory_identical=true`. Before/after inventory SHA-256 is `36154be89f79a57194f1ed7cd50f3772cd847d5a5ab6eae24c55cc4def09b0c9` for both files. `/bin/ps` was observed UNAVAILABLE through denied execution: saved exit 126 in `sandbox_non_native_v2/ps.exit_code.txt`, with actual error in `ps.stderr.txt`. Python was `/usr/bin/python3` 3.9.6; Apple's launcher reports `/Library/Developer/CommandLineTools/usr/bin/python3` as `sys.executable`. Sandbox niceness is **10**, not host niceness 0. Native tests were not run. The suite runner saved each invocation in `command.json`, source hashes, child argv and per-test group-clearance records.

The thousand-refusal positive control completed 1,000 invocations in 133.371 seconds with 3 files, 1 refusal file, 1,851 bytes. This narrow control passed; it does not make the full suite GREEN.

### Every skip / exclusion

Four native tests were excluded explicitly in `sandbox_non_native_v2/native_not_run.json`: `LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`, `LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest`, `LockedReleaseTest.test_compiled_app_full_source_equals_saved_source`, and `LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change`. The full addendum now has 155 tests (154 original plus one E probe). The requested base ten were not run in the sandbox because they require real rclone.

The 14 skips below are saved individually in `sandbox_non_native_v2/result.json`; all have reason `HOST-PENDING: real rclone forbidden by MB14 brief`:

| Class | Skipped case |
|---|---|
| ArchiveTest | test_corrupt_remote_download_check_does_not_create_receipt |
| ArchiveTest | test_differing_remote_is_immutable_and_preserves_prior_manifest |
| ArchiveTest | test_manifest_write_failure_is_loud |
| ArchiveTest | test_real_copy_download_check_and_sha_receipt_never_delete_source |
| ArchiveTest | test_source_drift_after_check_does_not_create_receipt |
| HeartbeatTest | test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries |
| HeartbeatTest | test_exit_publication_failure_is_loud_and_preserves_original_failure |
| HeartbeatTest | test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept |
| HeartbeatTest | test_native_nonregular_skip_is_recorded_as_warning |
| HeartbeatTest | test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night |
| HeartbeatTest | test_real_queued_source_vanish_is_warning_and_keeps_raw_exit |
| HeartbeatTest | test_real_sync_publishes_actual_bytes_and_completed_success |
| HeartbeatTest | test_remote_global_overrides_refuse_without_dispatch |
| HeartbeatTest | test_start_publication_failure_invalidates_previous_success |

### Final sandbox failures, all in LockedReleaseTest

The suite has 13 failures in: `test_builder_compares_fresh_saved_compile_with_newline_growth`, `test_builder_rejects_empty_canonical_decompile`, `test_changed_excludes_byte_refuses`, `test_changed_manifest_byte_refuses`, `test_changed_status_byte_refuses`, `test_changed_wrapper_byte_refuses`, `test_checkout_pull_cannot_change_dispatch`, `test_dirty_checkout_stages_commit_bytes`, `test_existing_release_id_refused_without_overwrite`, `test_extra_file_refuses`, `test_good_release_dispatches_release_path`, `test_missing_file_refuses`, and `test_rendered_source_stamps_release_and_all_four_hashes`. The 2 errors are `test_builder_rejects_app_decompile_byte_mismatch` subcases `extra_newline` and `changed_byte` (missing decompile artifacts after failed staging). Exact tracebacks start at `sandbox_non_native_v2/test.log:153`.

EVIDENCE-SHOWS: staging rejected these paths with `Release must be outside every git checkout: <this worktree>`. I-INFER: the new runner's global TemporaryDirectory remap put locked-release fixtures beneath its HOME inside the repo, violating the production guard. There is no established production defect. **Do not weaken the production guard, add retries or alter the frozen runner.**

## Criterion table — tests first, current status

The preregistered list is `test_list.md`; test code is `test_package.py`. The original addendum was copied before editing. Package implementation began only after saved RED. GREEN below means actually observed, not an expected result.

| Criterion | Test/check | RED | GREEN / remaining |
|---|---|---|---|
| 2.1 | CheckTemplateTest | package RED: absent runner | `run_local_check.py` implemented; untested; plan missing |
| 2.2 | 11 VerifyCheckTest cases | package RED: naive verifier accepted bad fixtures | verifier implemented; no GREEN run yet |
| 2.3 | local→local four-case runner | test/template written first | host UNRUN; runner implemented, unverified |
| 2.4 | PlanCriteriaTest.test_2_4_checkpoint | package RED: absent plan | plan missing |
| 3.1 | 3 RunnerContractTest cases; exact 22 host tests | package RED: absent runner | runner implemented; host UNRUN; sandbox runner has fixture-path failure |
| 3.2 | PinsTest and shasum -c | package RED: absent pins | pins missing; old pins preserved |
| 3.3 | ErratumTest | package RED: absent erratum | erratum missing; current sleep line 483, parse line 470 |
| 4.1 | PlanCriteriaTest.test_4_1_fresh_history | package RED: absent plan | plan missing; inventory collected by sandbox envelope, but no operational choice finalized |
| 4.2 | PlanCriteriaTest.test_4_2_deployed_tool | package RED: absent plan | plan missing |
| 4.3 | PlanCriteriaTest.test_4_3_deadline_and_progress | package RED: absent plan | plan missing |
| 4.4 | PlanCriteriaTest.test_4_4_failure_branch | package RED: absent plan | plan missing |
| 4.5 | PlanCriteriaTest.test_4_5_assertions | package RED: absent plan | plan missing |
| 4.6 | PlanCriteriaTest.test_4_6_orphans | package RED: absent plan | plan missing; no host PID check performed |
| 4.7 | PlanCriteriaTest.test_4_7_retirement | package RED: absent plan | plan missing |
| 5.1 | 5 CheckPlanTest cases | package RED: naive checker missed hazards | checker implemented; needs own captured RED on v1 and GREEN on v2 |
| 5.2 | PlanCriteriaTest.test_5_2_build_and_schedule | package RED: absent plan | plan missing |
| 5.3 | PlanCriteriaTest.test_5_3_order_and_stop | package RED: absent plan | plan missing |
| E.1 | LauncherHomeExportTest | valid RED: two UNSET failures | 1 test GREEN, four passing subcases |
| E.2 | shared isolate_failing_launcher_home helper | same valid RED | export HOME fixed; GREEN above |
| E.3 | strengthened existing native failing-wrapper case | assertion added after E RED | fixture receipt/counter/unresolved assertions added; native UNRUN |
| E.4 | inventory envelope | no native run before E GREEN | host UNRUN; sandbox inventory identity verified |

## Files and hashes

Only the existing `tools/test_backup_gdrive_addendum.py` was edited: before SHA-256 `f9547a3f58870881a5d78b8e2fd829a24e432979885c199865e837cfa871ab34`; after SHA-256 `3ff28cb712e97941476c1730928ff720f9a0dbcb2d8ba29344647ea8904501f8`. Diff: 49 insertions, 7 deletions, entirely E helper/probe/native positive control. Its untouched original is `before/tools/test_backup_gdrive_addendum.py`. The valid RED snapshot is `before/tools/test_backup_gdrive_addendum_red_valid.py`; it is replayable without reverting the live test file.

All new files have an absent before-state. Initial naive verifier/checker and first test bytes are preserved in `before/`; the initial runner revision is `before/run_py39_coverage_v1.py`. Every starting production/base/old-pin hash is in `before_sha256.txt`; current production/base/test/old-pin/frozen-runner and all package implementation hashes are in `handoff_sha256.txt`. Seven production files, base tests, old pins and frozen runner remain unchanged.

| New implementation | Current SHA-256 |
|---|---|
| test_list.md | a66bf2e140cea00d9a634b5f2a4991b15a867b41f347ae751026ccc8282c0601 |
| test_package.py | 9aa0a31ebb5e4a3f25c5714930640b32cf2de5a277e34ff37dccbbb3dbe898d0 |
| verify_check.py | a7126bd62cf127c757873f348db745b981fae9603246a5afff604736c8fc49e5 |
| check_plan.py | fb56acf06fe1f7d69e3321577762c61b0575c4d64f62522dcd94a4d8f64d50c4 |
| real_inventory.py | d68c62f12c60aa8152ed8f37c26b8bdf920c1235b79765473797c47f39e7a56f |
| run_py39_coverage.py | 164b353b620ad8b7b2baaf43e3f61877953fc0fc3fe28072bc69b32b790fa003 |
| run_local_check.py | d2c93d25c4d169447c08a003765f2bb1aee04e60da1a94d2fc60af75d1eb0059 |

Suite log SHA-256: `9a37fee9521d391b7a4911463caa315796b8bd3d8c5ed0c49a792f3ffae03ab1`; suite result SHA-256: `0b71e9ef9976dfa03cd313f6a07cf0dcf705b1075526d7bafe2c38936fd9d8fa`. E valid RED log SHA-256: `6532b838095eb8892b5d165a41b6bd54109ba74684acd1c0aab69fcc4b3cd59e`; E GREEN log SHA-256: `7b0928400e722e129793c2cc4372304c206a8425180018fcfb94e2ba5abf4661`.

Observed receipt allocation was 13,488 KiB after suite completion (budget <200 MB). The finalizer lists files over 1,000,000 bytes with size and hash in `bulk_not_in_git_sha256.json`. No prior receipt was edited. New package files are uncommitted.

## Astra r11 map — incomplete, do not submit yet

| r10 item | Current evidence / gap |
|---|---|
| 1 | Read-only confirmed locked-release inputs: `tools/launchd/stage_gdrive_release.sh:10`, `tools/launchd/MemitGdriveBackup.applescript:4`; original host GREEN is the brief's `results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/cmpfix_green/result.json` (154 run, 14 skips). Seven-file scope remains to be stated in plan v2 and re-reviewed. Current sandbox suite is FAIL. |
| 2 | `test_package.py:27` negative receipt cases; implemented `verify_check.py:9` and `run_local_check.py:19`; no final plan, verifier GREEN or local rclone fixture evidence. |
| 3 | `run_py39_coverage.py:27` selects 10+9+3; `:39` host validation; all host evidence UNRUN. Pins/erratum absent. |
| 4 | `real_inventory.py:9` and actual sandbox before/after receipts; operational plan absent. No recovery or native activation performed. |
| 5 | `test_package.py:80` checker tests; `check_plan.py:9` implementation; v1 command RED and v2 GREEN still needed. |
| E | `tools/test_backup_gdrive_addendum.py:32` shared helper, `:43` non-native probe; `e_red_valid/stderr.txt:3` RED; `e_green/stderr.txt:1` GREEN. Native positive-control assertions added, host UNRUN. |

Current line references for the erratum: `tools/test_backup_gdrive_addendum.py:470` unguarded `json.loads`, `:483` `time.sleep(0.01)`. Astra's ruling still binds: normal status publication is atomic (`tools/backup_gdrive_status.py:228–235`), so malformed input can raise but partial-write JSON is not an established race. Historical full test hashes confirmed by git object reads: old pins `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e`; a091aec `b764938802edf101be01493d24012a586076ca9f00bbfba2193c70336e54fdf1`; a19749d `6eba5860e1fbb0c562af9a4241f8acf6f50d966d05b3d0e8ac66ec35e14e7d2c`; d1a7154/start `f9547a3f58870881a5d78b8e2fd829a24e432979885c199865e837cfa871ab34`; E after hash above. `01147aaa` also contains f9547a3f; do not use it as the first lineage entry. The committed old pin file stays untouched with SHA-256 `b24014eaffb19434922a67790bbe54753253f5461686b473779a03259bae6d68`.

No real rclone calls occurred except allowed `version` and `check --help`. Installed rclone is v1.75.2. Its help confirms report sigils and download/one-way behavior. The verifier's terminal-log parser was based on primary source https://raw.githubusercontent.com/rclone/rclone/v1.75.2/fs/operations/check.go (reportResults at lines 227–247): nonzero unchecked-hash count is reported explicitly; a matching sigil alone does not prove a hash was checked. Host fixture must verify that actual output shape. The next session should capture the allowed help output into this receipt; this session only read it through the tool.

## Handoff — single next step for MB40

**Single next step: diagnose and fix the new runner's fixture placement, with a cheap isolated locked-release positive control, preserving this failing suite and leaving all seven production files and the frozen runner untouched.** The global temporary-directory remap currently makes production release staging correctly refuse paths under the checkout. Do not start another full suite until that positive control reaches the real staging path.

Done: authority/pins checked, test list written, E shared transform extracted, valid RED saved, export fixed, non-native E GREEN saved, native fixture positive control added, package tests RED saved, candidate verifier/checker/inventory/host runners written, full sandbox attempt completed and receipts preserved. No command is in flight; unified exec session 79514 exited 1. Half-done: runner correctness, all package GREENs and plan/pin/erratum/host-command deliverables.

Remaining after that next step: complete plan v2 written for release-dir deployment, pin set v2 and erratum; run verifier/checker/runner contract GREEN tests; capture checker RED on preserved v1; produce exact niceness-0 host commands for E RED/GREEN, the 22-case runner, the four local-content fixtures, inventory-wrapped frozen runner under fresh labels, checker RED/GREEN and shasum -c; rerun all sandbox-runnable GREENs; state final pin count and every skip; refresh hashes/bulk list and this README. Never claim host passes without MAESTRO's receipts. The final ready token is forbidden until every sandbox-runnable GREEN passes.

Open risks: runner candidates have no package GREEN yet; new full suite is FAIL; activation plan/pins/erratum do not exist; real-history branch needs a new inventory plus operator no-lost-history confirmation; native artifacts/home isolation remain UNVERIFIED; the immutable deployment change has not been reviewed by Astra. All old GO/STOP conditions and the r10 verbatim order still need to be carried into plan v2. No authorization to execute that plan is granted here.

**CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch “Context N% left”. Start a new piece of work only at >=60% left. At <=40% left, or on any “Context compacted”, stop starting work, append a handoff to README (done / half-done, exact paths, SHA-256s, test state, single next step), and reply “MB39 HANDOFF”. Restate this directive in any successor handoff and for every team session. MAESTRO's explicit stop-after-suite instruction at 49% takes effect now.**

PYTHON QUIET persists: on “HOLD PYTHON”, finish the current command and start no Python or tests until “RESUME PYTHON”. Scope persists: only the E portion of tools/test_backup_gdrive_addendum.py, this receipt, and mktemp dirs may be written; stop if any other pinned input changes. MAESTRO owns trackers/dashboard/MathLab/NEW1/closeout work. Do not touch or hash those files.
