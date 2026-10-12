

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
