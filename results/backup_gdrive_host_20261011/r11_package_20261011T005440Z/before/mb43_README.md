# MB42 HANDOFF — host correction GREEN; package refresh pending

## Single next step

**Finish the package refresh in this existing receipt, then provide all nine fresh host commands to MAESTRO.** The one-round code correction and focused tests are finished; no command is in flight. Do not run the existing host_commands.sh: every old r11_* label has already been used. Use the proposed fresh prefix r11_hostfix1_* for all nine actions, preflights and pins, plus the frozen inner *_all label; check that each chosen path is absent. Copy before further edits. Update the affected pins (three edited source files, plus host docs/script/plan if amended; add the new regression source), docs/README/bulk manifests, run all relevant sandbox GREENs with isolated HOME and /usr/bin/python3 -B, then final pin and README/manifests checks. The package mode now includes test_hostfix_mb42, so its expected full package count is **55** (39 existing + 16 new), subject to the actual raw GREEN. A full package run before repinning will fail PinsTest correctly. No further implementation change is known to be needed.

Pins_v2 still describe the pre-host-correction bytes; they are **STALE**, not final GREEN. Full package/sandbox/checker reruns, fresh host dispatch labels, activation-plan semantics note, bulk refresh and final package seal remain half-done. Ready token forbidden until complete. Preserve every old host/native/raw log and previous manifests; use new receipts/labels rather than overwriting. The original host run's results are immutable evidence, not GREEN on the new code.

## Done / exact evidence

- Before edits, all 27 pins and all 385 MB42 manifest entries passed under commands/mb42_hostfix1_entry_pins and commands/mb42_hostfix1_entry_manifest. Existing-file copies are before/mb42_hostfix1_<filename>; the baseline/host-evidence hashes are mb42_hostfix1_entry_snapshot.json.
- Root-cause RED: commands/mb42_hostfix1_causes_red/stderr.txt:1-79, 11 tests, **5 behavioral failures, 0 errors**, exit 1. Four failures replay the actual host DEBUG --error/error.txt contamination; the fifth executes the actual runner and observes HOME under /Volumes/memit.
- Complete RED: commands/mb42_hostfix1_full_red/stderr.txt:1-111, **16 run, 9 failures, 1 error**, exit 1. Four added failures are missing physical-proof helpers; the error is the real run_local_check.py receipt-vs-HOME containment rejection. Do not describe all ten as behavioral assertion failures.
- Focused GREEN: commands/mb42_hostfix1_focused_green/stderr.txt:1-21, **16 pass**, no failures/errors/skips, exit 0. Replays clean/excluded/symlink PASS, corruption FAIL naming alpha.txt; NOTICE-only PASS; true severity/read/unchecked errors still FAIL; actual sandbox runner placement; local-check evidence/content separation; recorded host APFS disjoint/shared/unknown identities and actual df mount resolution.
- Existing controls GREEN: commands/mb42_hostfix1_existing_controls_green/stderr.txt:1-25, **20 pass**, no failures/errors/skips, exit 0: all 11 verifier controls, eight checker tests and exact check template.
- Seven production files, both base/addendum test sources, frozen runner and old pin set remain byte-identical. mb42_hostfix1_stop_state.json records protected hashes/current source hashes and pending state. All failed host coverage/fixture receipts and MAESTRO's native diskutil probe were rehashed and preserved.
- Current allocation by file lengths is 31836992 bytes (<200 MB); new host/bulk files require the pending bulk manifest refresh. No native/real-rclone/Drive/activation command, real HOME write, unowned kill, deletion or git mutation was executed.

## Current fix and flush caveats

run_py39_coverage.py now keeps evidence in this receipt and allocates a fresh owned /private/tmp/drive_r11_<label>_*/ runtime containing HOME/fixtures/TMPDIR. Host coverage and fixture modes first run saved df -P observations, resolve each path to its mount point, then call diskutil info -plist on the mount points. APFSPhysicalStores are reduced to physical whole disks; unknown or intersecting sets STOP. ParentWholeDisk alone is deliberately insufficient: source memit is virtual disk6 over physical disk4s3; Data is virtual disk3 over physical disk0s2. Another external partition such as disk4s1 must be refused. The current parser requires evidenced APFS physical stores and fails closed for unsupported/missing identities.

MAESTRO's authoritative host probe is host_diskutil_probe_maestro31/README.txt:1-5 plus the three successful plists. /private/tmp is not a diskutil mount point (rc 1); df resolves it to /System/Volumes/Data. Probe hashes are mb42_hostfix1_diskutil_inputs.json. Sandbox diskutil was actually probed and cannot use DiskManagement; actual new runtime physical positive control is still **host UNRUN**, despite replayed native data passing.

verify_check.py now matches severity only at a log-line prefix, preserving ERROR/CRITICAL/FATAL and read/unchecked/report failures. The three recorded clean host cases falsely failed because the DEBUG argv included --error and error.txt; removing only that line made the missing-config NOTICE pass before the fix. The raw logs/reports are never altered; tests replay them in owned /private/tmp fixtures.

run_local_check.py now validates its output below this receipt and isolated HOME below /private/tmp, so the separate content/evidence roots are legal. Production's same-source-volume destination guard is untouched. .deleted/rclone.pid/timeout/start-success failures occur after the refused dispatch; no separate policy fix was made. Their shared cause is **I-INFER** until the fresh exact 22 host run passes.

The original host run at maestro_host_20261011T015745Z/rcs.txt passed E RED as expected, E GREEN 4/4, frozen 155/0 failures/14 skips, package/checker/pins; coverage failed 22 run/13 failures and fixture failed three clean cases. These are pre-fix host results. All nine actions must be rerun under fresh labels after the package refresh, including the seven previously passing actions.

## Current source identities

| File | Before SHA-256 | Current SHA-256 |
|---|---|---|
| run_py39_coverage.py | d5a7094de35b528d423c47962a66bde9ea52b69f538007c28c5c49223a65965b | f66dec5193003aeec02ce72a22760597c1beb685f00b8a7580c73aceec4bf41b |
| verify_check.py | a7126bd62cf127c757873f348db745b981fae9603246a5afff604736c8fc49e5 | 5b4748c501d3d5f416a689978a8052d3d2a3390a5d0439b313f4285ab8a1fbfc |
| run_local_check.py | d2c93d25c4d169447c08a003765f2bb1aee04e60da1a94d2fc60af75d1eb0059 | 0c9045c7635919f61ca91792c8ed756074ebb1a8fcfcabfdbd66980102131a75 |
| test_hostfix_mb42.py | ABSENT | c8f246b419009dd0bb5d13250e00fd19392e1300872e269a9e0e2284647807bf |

## Binding continuation directives

CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch Context N% left. Start a new piece only at >=60% left. At <=40% or any compaction, stop starting work; append done/half-done/in-flight exact paths, SHA-256s, test state and one single next step to README, restate this directive and reply MB42 HANDOFF. MAESTRO additionally reported this session at 50% and ordered completion of the current fix/tests, then a handoff if under 45% instead of starting the full package refresh. This session stops after the completed fix/tests; no refresh is started. Every successor/team session inherits the directive.

PYTHON QUIET: HOLD PYTHON means finish the current command and start no Python/tests until RESUME PYTHON. Production/base/addendum/frozen runner/old pins are read-only. No remote rclone, native applets, launchctl, activation, real HOME writes, unowned kills or git mutation. Preserve the exact original exclusions, including all Q1 dashboard_queue/team_dashboard files/results and MAESTRO docs/program_state.json and closeout files. Unexpected protected drift → STOP. Ready token only when every authorized sandbox-runnable GREEN and package refresh passes.

## Preserved prior package report — pre-host-correction bytes

The prior report below is historical; its final-byte/readiness/pin/UNRUN claims do not describe the current host-correction state above.

# MB42 — Drive r11 package ready for MAESTRO host runs

Prepared in the existing receipt, with every final sandbox-runnable GREEN passed. This is **package readiness**, not host GREEN, Astra GO, backup activation or full-content acceptance. Host/native/real-rclone fixtures and all operational GO rows remain UNRUN.

Worktree/branch: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, `worktree-c10k-route-a`; MB42 observed HEAD `aa4d9572dde6ab29e73d8ee6312c140beed8a27a`. MB40 handoff preserved at `before/mb41_README.md`; MB39 handoff at `before/mb40_README.md`. MB42 reverified all **339/339** MB41 handoff manifest entries and **27/27** pins at entry (commands/mb42_entry_manifest and commands/mb42_entry_pins); all eleven protected inputs remain unchanged. Trust raw logs/hashes over prose.

## Single next step

MAESTRO runs the exact individual commands in **host_commands.md**, at niceness 0, inspecting each saved output/pass rule before advancing. Begin with E RED/GREEN, then exact 22 coverage and four local-content fixtures, then frozen suite/package/checker/pins. Submit the immutable release change plus host receipts to Astra r11. No activation row runs before that review and its marked GO. Do not reuse existing run labels.

## MB42 final closeout — criteria 3.1 and 3.2

Only the nine outer dispatch examples in host_commands.md:8-16 were changed to set LLMDB_ROOT=$PWD explicitly. The underlying host script, runner, plan, checker, verifier, E-only test change and production inputs are unchanged. Every changed existing file has a rehashed before/mb42_* copy.

| Check | RED | GREEN |
|---|---|---|
| Nine host examples set the worktree root | commands/mb42_host_root_red/stderr.txt:1-22: 1 test, 1 behavioral failure, exit 1 | commands/mb42_host_root_green/stderr.txt:1-6: 1 pass, exit 0 |
| Final isolated PinsTest | Inherited missing-deliverable behavioral RED remains preserved | commands/mb42_pins_test_green/stderr.txt:1-6: 1 pass, exit 0 |
| All final pin bytes | Entry 27/27 OK preserved | commands/mb42_pins_final_green/stdout.txt:1-27: 27/27 OK, exit 0 |

Fresh MB42 totals: **RED 1 run/1 failure/0 errors; GREEN 2 run/2 pass/0 skips/failures/errors**. Both tests used /usr/bin/python3 -B, BACKUP_TEST_NO_RCLONE=1 and an isolated /private/tmp HOME. No full suite was repeated for this documentation-only change. The inherited suite/package/checker GREENs below were revalidated from raw logs, exit codes and rehashed files, then combined with the fresh final PinsTest. mb42_evidence_verification.json records that reconciliation; mb42_test_list.md was saved before the regression and edit.

| MB42 changed existing file | Before SHA-256 | Final SHA-256 |
|---|---|---|
| host_commands.md | 2415ffa78e30bf06b4433428ff535d84c526337ea94d28b5c5dfb32550a16e30 | 345056a88cf0632cf8f0830761e942089b1ea8ac85d38160442a62aef932901b |
| pins_v2.json | 51e913004e7565424e3a9aa8bd082895f1b737d101296641d202d071f78fe986 | 7cd3f4f9ace315b85eee89ba40482f0e0cc37efef8c866cf6d6100e72c72284e |
| pins_v2.sha256 | b770896fcbaaefb9143bfebbdbdfc983bfdc46abcf3a1968bc9dc8175c6bbba1 | 80dbfa2a363fa800e365e289464e9d419c79edc408c35a06ab4916ff04c4079d |
| README.md | 084316e2c8cfe3c04208ab2841b396d1aab580071e1f11d291bcfd240ceab582 | final_sha256_mb42.txt (external self-hash) |

All other 335 MB41-manifest entries remain byte-identical. bulk_not_in_git_sha256.json was revalidated against every >1,000,000-byte file; all six entries remain unchanged, so its bytes were preserved. New MB42 evidence files have before=ABSENT and are listed in change_manifest_mb42.json. The final hash manifest covers current receipt evidence and all eleven protected inputs; its own derived identity/change manifests and the final-manifest-check capture directory are excluded to avoid a circular hash dependency. final_manifest_identity_mb42.json separately hashes those derived manifests and the complete final verification receipt. Current README and complete artifact hashes are in final_sha256_mb42.txt; final_manifest_identity_mb42.json holds that manifest's external SHA-256.

Exact host commands, copied from host_commands.md:6-16; all remain **UNRUN**, require niceness 0 and must run individually with their saved output/pass rules:

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
R="$PWD/results/backup_gdrive_host_20261011/r11_package_20261011T005440Z"
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" e-red
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" e-green
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" coverage
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" fixture
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" frozen
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" package
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" check-red
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" check-green
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" pins
```

## Final sandbox evidence

| Run | Observed result | Raw sink / exits |
|---|---|---|
| Inherited addendum non-native | **151 run: 137 pass, 14 real-rclone skips, 0 failures/errors**; four native cases excluded explicitly | mb41_sandbox_green/test.log:154-156; result.json; exit_code.txt=0 |
| Inherited final package + receipt helper | **39 run, 39 pass, 0 skips/failures/errors** | mb41_package_final_green/driver.stderr.txt:42-44; child/outer exits 0 |
| Final v1 checker RED | 20 findings, all six named defect categories | mb41_check_v1_final_red/driver.stdout.txt:1; child exit 1; outer exit 0 means expected RED, not plan PASS |
| Final v2 checker GREEN | `PASS []` | mb41_check_v2_final_green/driver.stdout.txt:1; child/outer exits 0 |
| Final MB42 pins | **27/27 OK** on final document bytes | commands/mb42_pins_final_green/stdout.txt:1-27; exit_code.txt=0 |
| Host command syntax | /bin/sh -n exit 0; commands not executed | commands/mb41_host_syntax_green/command.json, exit_code.txt |
| E shared transform | Four generation/receipt × absent/sentinel parent subcases pass | inherited e_green/stderr.txt:1-6; repeated in mb41_sandbox_green/test.log:78 |

All final runner results report real_inventory_identical=true and all_owned_groups_exited=true. Fresh `mb41_sandbox_green/real_after.json` is byte-identical to `mb40_staging_green/real_after.json`: real backup logs remain empty, real launch state/journal/lock and application-support release root absent. Sandbox interpreter is /usr/bin/python3 3.9.6, niceness **10**. /bin/ps was actually attempted and denied (exit 126/PermissionError), recorded in each ps_observation.json; this is UNAVAILABLE, never host clearance. No relevant stale backup/package/checker .pyc files were found by the final scoped cache probe.

## Test-first receipts and predecessor failures

| Control | RED | GREEN |
|---|---|---|
| Read-only filename data versus actual builder operation | commands/mb41_operation_red/stderr.txt:1-26: 2 run, 1 expected WRITE_MARKER false-positive failure; real builder guard passes | commands/mb41_operation_green/stderr.txt:1-14: 7 checker tests pass; inherited final 8 checker tests pass |
| Explicit content-check wakefulness and caffeinated launch GO | commands/mb41_wake_red/stderr.txt:1: 2 run, 2 failures | commands/mb41_wake_green/stderr.txt:1-26: 20 checker/plan tests pass; final package includes both controls |
| Missing pin deliverable | commands/mb41_pins_red_valid/stderr.txt:1-18: 1 run, 1 failure | final package PinsTest and 27/27 shasum GREEN |
| E conditional HOME leak | e_red_valid/stderr.txt:3-30: 1 run, exactly 2 absent-parent UNSET failures; sentinel-parent passes | e_green/stderr.txt:1-6: 1 pass; four subcases; no native run before fix |
| Staging placement | mb40_staging_red_valid/test.log:1-17: 1 run/1 guard failure | mb40_staging_green/test.log:1-6: 1 pass; current full non-native suite also passes staging |
| Capture helper | mb40_capture_red/stderr.txt:1: 2 failures while helper absent | final package log:38-39: 2 pass |
| Original package scaffolding | package_red/stderr.txt:1-35: 33 run, 13 failures, 18 missing-artifact/import errors, 2 pass | 39 final passes; preserve the distinction between scaffold errors and behavioral RED |

Invalid/failed attempts remain preserved, not reclassified: e_red (4 scaffolding failures); sandbox_non_native (no tests, denied ps); sandbox_non_native_v2 (151 run, 13 failures, 2 errors, 14 skips); mb40_staging_red (wrong whole-suite selector, interrupted/exit 130; no result.json); mb40_check_v2_green (one false-positive WRITE_MARKER, child/outer exit 1); commands/mb41_pins_red (missing-file error, replaced as evidence by the explicit assertion RED). MB39 E valid RED's outer heuristic also exited 1 because AssertionError matched its Error substring; the unittest RED remains valid. No earlier receipt, old pin set or raw failure was edited.

## Criterion table — tests → RED → final GREEN / host limitation

`package_red/stderr.txt` references are the original pre-implementation run. GREEN references below use `mb41_package_final_green/driver.stderr.txt`; presence/plan contract tests are static evidence. They do not claim the operational behavior already ran.

| Criterion | Test | RED | Final GREEN and remaining host limitation |
|---|---|---|---|
| 2.1 | test_filters_reports_and_download | package_red/stderr.txt:6 | final package log:9; Exact identical filters/default hash, --one-way, reports and --download; plan:262; help captures preserved. |
| 2.2 | test_differing_file | package_red/stderr.txt:24 | final package log:28; 11 verifier controls pass (clean plus fail-closed boundaries); final log:27-37. Real report/log shape remains host UNRUN. |
| 2.3 | test_filters_reports_and_download | package_red/stderr.txt:6 | final package log:9; Template GREEN only. Four actual local→local cases are host UNRUN; run_local_check.py and host_commands.md:26. |
| 2.4 | test_2_4_checkpoint | package_red/stderr.txt:10 | final package log:13; Plan:243-327, writers/pause/catch-up/full content/inventory/read budgets; operational GO UNEXECUTED. |
| 3.1 | test_exact_selection | package_red/stderr.txt:20 | final package log:24; Runner contract GREEN, plus source-boundary and forbidden-argv controls. Exactly 22 host tests/config/native/inventory acceptance UNRUN. |
| 3.2 | test_supersedes_lineage_and_current_bytes | package_red/stderr.txt:8 | final package log:11; 27 current pins, full preserved supersession/lineage, built-bundle future manifest; commands/mb42_pins_final_green/stdout.txt:1-27. |
| 3.3 | test_current_lines | package_red/stderr.txt:7 | final package log:10; erratum.md:3-5; current T:470 parsing/T:483 10-ms sleep; atomic publication ruling retained. |
| 4.1 | test_4_1_fresh_history | package_red/stderr.txt:11 | final package log:14; Fresh empty-history inventory identical to MB40; plan:144-188 gives exact conditional recovery output/post-state. No-lost-issued-history confirmation/GO UNRUN. |
| 4.2 | test_4_2_deployed_tool | package_red/stderr.txt:12 | final package log:15; Hash immediately precedes /usr/bin/python3 against deployed D/status, e.g. plan:158-166. Deployment/status/recovery host UNRUN. |
| 4.3 | test_4_3_deadline_and_progress | package_red/stderr.txt:13 | final package log:16; Plan:211-239: owner, child and progress independent of masked status; strictly before end+13 h. Host UNRUN. |
| 4.4 | test_4_4_failure_branch | package_red/stderr.txt:14 | final package log:17; Plan:241: diagnosed operator-approved next observed successor, lock/process clearance; recovery only damaged ordering or explicit initial bootstrap. Host UNRUN. |
| 4.5 | test_4_5_assertions | package_red/stderr.txt:15 | final package log:18; Plan:202-226 initial AC/assertions; exact check lifetimes at :274/:295 and active assertions :281/:302. Additional wake control RED→GREEN below. Host UNRUN. |
| 4.6 | test_4_6_orphans | package_red/stderr.txt:16 | final package log:19; Plan:191-200: mandatory fresh eight-PID/native fixture scan immediately before launch. Host clearance UNRUN; sandbox ps unavailable. |
| 4.7 | test_4_7_retirement | package_red/stderr.txt:17 | final package log:20; Plan:381-404: content checkpoint + fresh scheduled completion, bootout/disable/disabled map/no surviving old sync. Host UNRUN. |
| 5.1 | test_v1_all_named_defects | package_red/stderr.txt:4 | final package log:7; Final v1 CLI child exit 1/20 findings, wrapper 0 denotes expected RED; v2 child/wrapper 0 PASS []; narrow regressions below. |
| 5.2 | test_5_2_build_and_schedule | package_red/stderr.txt:18 | final package log:21; Plan:106-134 build-time full manifest/full source cmp and :341-356 enabled state/login timing. Bundle remains UNBUILT, host UNRUN. |
| 5.3 | test_5_3_order_and_stop | package_red/stderr.txt:19 | final package log:22; Plan:5-9 verbatim required order/mapping, :414-430 preserved GO/STOP, preserved c1a06ea receipt :137-142. No activation performed. |
| E.1 | LauncherHomeExportTest shared probe | e_red_valid/stderr.txt:3,17: two UNSET subcases | e_green/stderr.txt:1, full suite :78; host replay UNRUN. |
| E.2 | Shared exported transform | same behavioral RED | T:32 helper used by probe and native failing-wrapper fixture; current SHA pinned; full non-native GREEN. |
| E.3 | Native receipt/counter/unresolved artifact assertions | Original native control was not run before the fix | T:2557-2561 assertions implemented; native execution **UNRUN**. |
| E.4 | Real inventory envelope | Before/after controls captured for all valid package runs | Final sandbox inventories identical; native E/full host envelopes ready but **UNRUN**. |

## Every skip and exclusion

The current addendum has 155 tests (154 original + one E probe). Four native tests were excluded from sandbox selection; all remain host UNRUN:

- `tools.test_backup_gdrive_addendum.LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest`
- `tools.test_backup_gdrive_addendum.LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`
- `tools.test_backup_gdrive_addendum.LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change`
- `tools.test_backup_gdrive_addendum.LockedReleaseTest.test_compiled_app_full_source_equals_saved_source`

The 14 actual real-rclone skips are recorded verbatim in mb41_sandbox_green/result.json:

| Test | Reason |
|---|---|
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_corrupt_remote_download_check_does_not_create_receipt` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_differing_remote_is_immutable_and_preserves_prior_manifest` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_manifest_write_failure_is_loud` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_real_copy_download_check_and_sha_receipt_never_delete_source` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_source_drift_after_check_does_not_create_receipt` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_exit_publication_failure_is_loud_and_preserves_original_failure` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_native_nonregular_skip_is_recorded_as_warning` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_queued_source_vanish_is_warning_and_keeps_raw_exit` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_sync_publishes_actual_bytes_and_completed_success` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_remote_global_overrides_refuse_without_dispatch` | HOST-PENDING: real rclone forbidden by MB14 brief |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_start_publication_failure_invalidates_previous_success` | HOST-PENDING: real rclone forbidden by MB14 brief |

The ten base tests also require real rclone and were not part of sandbox selection; they remain host-only. Exact 22 coverage must run those ten + all nine skipped Heartbeat + all three Launcher tests with BACKUP_TEST_NO_RCLONE unset, 22 pass/0 skips. The five Archive skips remain UNVERIFIED and are not activation dependencies. Frozen host suite must run 155/0 failures/errors/14 skips with groups exited; that suite does not replace exact 22 coverage. E host GREEN is 4 pass including native artifact assertions; all host evidence is currently UNRUN.

## Scope and hashes

Seven production inputs, tools/test_backup_gdrive.py, old pins and frozen run_suite.py are unchanged. The inherited E-only tools/test_backup_gdrive_addendum.py change is also unchanged by MB41 and MB42: pre-E snapshot f9547a3f… → current 3ff28cb7…; both full hashes are below/in pins_v2.json. MAESTRO's closeout files, trackers/dashboard/MathLab/NEW1 files were not edited or hashed. No real remote rclone, write pause/content check, native execution, launchd/open, real HOME write, commit/push/merge/PR action, deletion or unowned kill occurred.

Before copies were made before each existing file's first MB41 edit. New files have before=ABSENT. `change_manifest_mb41.json` records every changed/new receipt artifact against MB40's hash manifest; `final_sha256_mb41.txt` preserves the MB41 identity; `final_sha256_mb42.txt` supplies current final report/artifact hashes. Neither file replaces pins_v2. The old 33-line pin file remains b24014eaffb19434922a67790bbe54753253f5461686b473779a03259bae6d68, preserved and superseded explicitly. Full test lineage (766509ab → b7649388 → 6eba5860 → f9547a3f → 3ff28cb7) is rehashed from old pins/actual git commit bytes in pins_v2.json.

| MB41 changed existing file | Before SHA-256 | Final SHA-256 |
|---|---|---|
| check_plan.py | fb56acf06fe1f7d69e3321577762c61b0575c4d64f62522dcd94a4d8f64d50c4 | 4bca51b5a9da521afd87d8cdbd2136ccc7e4a9e784c6e9b3155207f7a41cf8e9 |
| test_package.py | 9aa0a31ebb5e4a3f25c5714930640b32cf2de5a277e34ff37dccbbb3dbe898d0 | d75ab13decda62237c3cb189c4790736484c4474a3c537b6ada06a9615ad99d7 |
| activation_plan_v2.md | c3db5be5a8e1c1a5922ce0637b4f77fdbe2da631a2a2358e00e4952366352942 | 8204d3dc97c75968b7257b85bfe8dafe386dd09ba01d111bc36f0f85964e9d89 |
| bulk_not_in_git_sha256.json | fb637bcef35c37d6e5b6b18b1fd43adb48b9910aec95d3b7e4305d3b4c54eef2 | 52cc66bbe0e243908fbe2abfc356c11bc14eea23ea1395d34544ca9d0ed22d28 |
| README.md | 987059b4c9eaeffef60ed6c8ac313c50bfaed506d2f9edfee28dc35e2b7b16cb | final_sha256_mb42.txt (current self-hash is external) |

| New implementation/deliverable (before=ABSENT) | SHA-256 |
|---|---|
| pins_v2.sha256 | 80dbfa2a363fa800e365e289464e9d419c79edc408c35a06ab4916ff04c4079d |
| pins_v2.json | 7cd3f4f9ace315b85eee89ba40482f0e0cc37efef8c866cf6d6100e72c72284e |
| host_commands.sh | 86eb5b8d7aad22679bd96756befab8120685ff4219200bf0adfd54c9c3934d32 |
| host_commands.md | 345056a88cf0632cf8f0830761e942089b1ea8ac85d38160442a62aef932901b |
| mb41_test_list.md | d53992ef6d5ff359b103095d2828223572d2d7b138cf4e3cf283eb637a895b4d |
| context_save_mb41.md | 35613b18e973ca7d00b7a750ea6e170d3ee050b63fde40554338b8128bc20b5b |
| mb41_protected_verification.json | ad15c887e66e5890fe7233fac76ec970d480f5c29eee8d8fe071605cec63501b |

Inherited implementation identity remains: runner d5a7094d…, verifier a7126bd6…, inventory d68c62f1…, local fixture d2c93d25…, capture 3df18e30…, capture tests fe50cdd0…, erratum d6a68443…; full values and all 27 final pinned dependencies are in pins_v2.json. The source hashes in intermediate receipts identify their then-current bytes. Final checker/plan controls and package GREEN identify final bytes; the addendum suite does not import the later-edited receipt checker/plan/tests.

Receipt allocation before final reports was 33,836 KiB, below 200 MB. `bulk_not_in_git_sha256.json` lists every file >1,000,000 bytes with size/SHA-256. No bulk deletion occurred; bundle is UNBUILT and gets its own build-time manifest/full cmp/pins under plan §1.2-1.3.

## Astra r11 map

| r10 item | Evidence file:line and remaining boundary |
|---|---|
| 1 | Seven immutable deployment inputs are pinned; mb40_staging_green/test.log:1 reaches staging/dispatch; mb41_sandbox_green/test.log records all non-native LockedRelease controls; prior cmpfix_green/result.json establishes old 154/14-skip host run. Current native immutable-bundle dispatch/full cmp still needs the frozen 155 host run and Astra review. |
| 2 | activation_plan_v2.md:243-327 exact quiesce/catch-up/full-population hashing/reports/download/inventory/budgets; final package log:9,12-13,23,27-37; commands/rclone_check_help/stdout.txt; verify_check.py:9. Real fixture/report shape and remote checkpoint UNRUN. |
| 3 | run_py39_coverage.py:24 exact selection/:37 host guards/:143 measured ps/config envelope; final package log:24-26; pins_v2.json:1 supersession/lineage; commands/mb42_pins_final_green/stdout.txt:1-27; erratum.md:3-5. Exact 22 host acceptance UNRUN. |
| 4 | mb41_sandbox_green/real_after.json:1 fresh empty-history inventory; activation_plan_v2.md:144-188 conditional floor/output/post-state and deployed hashes, :191-226 clearance/AC/independent progress, :228-241 end-relative completion/retry, :381-404 retirement; final package log:14-20,23. All host operations/GO UNRUN. |
| 5 | mb41_check_v1_final_red/driver.stdout.txt:1 all v1 hazards; mb41_check_v2_final_green/driver.stdout.txt:1 PASS []; activation_plan_v2.md:5-9 order/:106-134 build integrity/:341-356 enabled-state/login/:414-430 STOP; final package log:1-8,21-22. Built bundle and activation UNRUN. |
| E | T:32 shared helper/:43 probe/:2557-2561 native assertions; e_red_valid/stderr.txt:3,17 and e_green/stderr.txt:1; mb41_sandbox_green/test.log:78. Native fixture artifacts and real-path invariance remain host UNRUN. |

## Saved context and binding next-session directives

`context_save_mb42.md` preserves this closeout via context-save, confined to the authorized receipt; MB41's note remains preserved. No command is in flight. The single next step is the MAESTRO host command sequence above. No sandbox implementation work remains; host/Drive/Astra acceptance is still open. Evidence remains scoped: static/fixture/CPU success does not establish host/Drive/scientific acceptance. Conditional no-lost-history confirmation, Astra r11, built bundle and all operational GO are still gates.

**CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch Context N% left. Start a new piece only at >=60% left. At <=40% left or any compaction, stop starting work; append done/half-done/in-flight exact paths, SHA-256s, test state and a single next step to this README, then reply with the assigned HANDOFF token. Restate this in every handoff and every team session.**

PYTHON QUIET: on HOLD PYTHON finish the current command and start no Python/tests until RESUME PYTHON. Scope: only the E portion of tools/test_backup_gdrive_addendum.py, this receipt and owned /private/tmp dirs may be written. Unexpected protected-file drift means STOP. Production/base/old pins/frozen runner are read-only; MAESTRO owns closeout and all excluded concurrent work. Ready token is forbidden unless every sandbox-runnable GREEN passes.

MB42 exclusions: do not read, hash, flag or touch Q1's tools/dashboard_queue.py, tools/test_dashboard_queue.py, tools/dashboard_queue_tab.sh, tools/team_dashboard.sh, results/dashboard_queue_build_*/, or MAESTRO's docs/program_state.json, tools/closeout_check.py and tools/test_closeout_check.py. Preserve all prior dashboard/MathLab/NEW1 and results/dashboard_audit_20261010 exclusions.

At the context threshold or any STOP, append the exact handoff and reply **MB42 HANDOFF**. The ready token is **DRIVE R11 PACKAGE READY FOR MAESTRO RUN** only after every sandbox-runnable GREEN and final manifest/README verification passes.
