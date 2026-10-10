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
