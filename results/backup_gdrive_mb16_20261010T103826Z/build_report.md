# GDrive MB16 fixture-root build

MB16 moves the fixture base, HOME, native applets, AppleScript sources and stub wrappers beneath a separate fixture root. The default is a fresh `tempfile.mkdtemp(prefix="memit_gdrive_native_", dir="/private/tmp")`. An explicit `--fixture-root` must already exist, be empty, and resolve outside `/Volumes`; validation finishes before production imports, compilation or launching.

Evidence remains in this receipt's `native_<case>_<UTC>/` directory. Case closeout copies the requested logs, counter, receipt, heartbeat, failure journal and complete recoveries archive into `fixture_copy/`, retaining their paths relative to the fixture base. Missing optional files are omitted. The fixture itself is retained for host inspection. Summary records `fixture_root`, the interpreter and real wrapper paths. On failed or timed-out `open`, the helper records the exact command and saves the applet's process tree before case cleanup. Snapshots preserve PID, PPID, state, elapsed time and complete command paths; an unavailable inspection or missing applet is explicit. Allocation-pause failure snapshots precede release of that pause.

The 20-second ordinary `open` timeout and original crash-path deadlines are unchanged; no retries or skipped cases were added. All 18 original assertion nodes/calls and the production-source SHA-256 block match MB14's AST exactly.

## Verification

```sh
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb16_20261010T103826Z/test_host_launcher_checks_mb16.py -v
```

**21 tests passed; 0 errors; 0 failures; 0 skips.** `GREEN.log` contains the final run. `RED_index.json` maps every test to its saved behavioral RED log (21 assertion failures, no test errors). The first RED baseline mechanically exposes MB14 behavior through small functions: evidence-local fixtures, no fixture-copy operation, no failure snapshot. `RED_helper_baseline.py` preserves that baseline; `RED_helper_followup_baseline.py` preserves the later baseline for the timeout-command and raised-cleanup checks. Tests intercept native subprocess boundaries; no applet was compiled or launched.

`protected_before.json` was written before the first helper/test edit. `protected_after.json` is identical: **8/8 production files and 88/88 MB14 receipt files are byte-identical**, including the MB14 helper and all original native-run receipts. `verification.json` records the counts, AST checks and final helper/test hashes. Syntax checks used in-memory `compile`, with bytecode writes disabled.

## Host commands for MAESTRO

Run from `worktree-c10k-route-a`; each command creates a separate fresh fixture root and native evidence directory.

```sh
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb16_20261010T103826Z/host_launcher_checks_mb16.py manual-interleave
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb16_20261010T103826Z/host_launcher_checks_mb16.py crash-after-allocation
LLMDB_ROOT=$PWD .venv/bin/python -B results/backup_gdrive_mb16_20261010T103826Z/host_launcher_checks_mb16.py recovery
```

**UNRUN:** native host execution and the macOS privacy hypothesis. Moving the fixture does not remove every memit access: manual-interleave still dispatches the real wrapper, and `BACKUP_PYTHON` remains the memit `.venv` interpreter. A remaining hang requires examination of `process_snapshot.txt`, `failure.txt`, `commands.json` and the recorded fixture root. No production edit, commit, push, merge, app installation, launchd mutation, real rclone invocation, network call or real backup-log write was performed.

## Production SHA-256 before = after

| File | SHA-256 |
| --- | --- |
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| `tools/backup_gdrive_status.py` | `64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b` |
| `tools/launchd/MemitGdriveBackup.applescript` | `683cb5a354b0b58fc8ff012317560d595f908000bc510d4ebfdf18741d1244da` |
| `tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` |
| `tools/launchd/com.rhu.memit-backup.plist` | `44c2ffcad9837f76c0b08d34a1b40ca367c9145edf3360cad3131e1c64e29a2f` |
| `tools/launchd/com.rhu.memit-gdrive-backup.plist` | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce` |
| `tools/test_backup_gdrive.py` | `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` |
| `tools/test_backup_gdrive_addendum.py` | `74cbd8afb20f2be676e61e9e1329c3356c52031ece1e7e5aef536709b2e891f3` |

## Created-file SHA-256

These are all receipt files created before this report. `created_files_sha256.json` additionally carries the final byte hash of this report; its own detached digest is emitted by final verification rather than embedded in itself.

| File (relative to this receipt) | SHA-256 |
| --- | --- |
| `GREEN.log` | `07c4e15803787aa55425304fbaf381cac8d1297d915b148468f49c5dd156c3ff` |
| `RED_helper_baseline.py` | `82fd9ab1398656b51f745303b063352cc92f0282c9c5bd49a4c2f321637c2d3d` |
| `RED_helper_followup_baseline.py` | `9027d4164f47b150279c03539e90ebf4d638be8c864aebf98c2790892afeb760` |
| `RED_index.json` | `3fa02425b2e0cda1347219700f8e3fb808f79cd3676c4a2abe92cadfc66a3dd3` |
| `RED_test_2_default_layout_all_fixture_paths_outside_volumes.log` | `6288236299cac26b91453f882ee8ac7c373e1d6b80e684524f8b6f02be1a4bac` |
| `RED_test_2_explicit_layout_all_fixture_paths_outside_volumes.log` | `b59d55f2689ae7f46ab2db1687ae8cc629ec2824e6e9af7b88bfe2409386f6fa` |
| `RED_test_2_file_fixture_root_rejected_before_native_work.log` | `f42a8dd500bf17b98950fc084d4f60c41e09286ace2a904fe89e0d285e086dce` |
| `RED_test_2_missing_fixture_root_rejected_before_native_work.log` | `e0208a468369b5a3e3418e5441014f6a355834b41149f811026ddb56f35a57a5` |
| `RED_test_2_nonempty_fixture_root_rejected_without_modification.log` | `1a50ec08146a8e528505ee7105f99cfc5bb4abe1c23cd1936a6ca181541ba473` |
| `RED_test_2_symlink_into_volumes_rejected_after_resolution.log` | `d00766a522a46d5e08a0e3e2dfce46e6ff5dea6e29b15f85411730d75919d3d6` |
| `RED_test_2_volume_fixture_root_rejected_before_native_work.log` | `ea3b8e3d016eb00c9a074fc6de35735ad492b91397c02a1a20841102cd858c7f` |
| `RED_test_3_absent_optional_files_are_omitted.log` | `b5e13b207babb668129cf0f15408d79e382241bddb747f7155d81fd9bd5c6b5c` |
| `RED_test_3_cleanup_failure_still_copies_fixture_evidence.log` | `923c78574423a287e1b7fe56561d99493f5ab7539da5625a2427db006c10a3ac` |
| `RED_test_3_failing_case_copies_exact_bytes_and_recovery_tree.log` | `92da5d9015f3eb360d8b35c4f44da955f4ecc763975384b236796627c9900858` |
| `RED_test_3_open_timeout_remains_in_commands_receipt.log` | `fcfa3d9aab37e1ae4426e0cdf659b6736f9ed58d60f608095914476a569b2ba4` |
| `RED_test_3_passing_case_copies_exact_bytes_and_recovery_tree.log` | `c2c4e400aee5be9e2ea7ce52bb60bd613fd7b7500bd7c0f352f9a3d3f4354cf2` |
| `RED_test_3_raised_cleanup_failure_keeps_case_reviewable.log` | `7065b97f33de3ea46be2e539c785629976db4551dd8145f7a11b4c0a35d060f7` |
| `RED_test_4_crash_allocation_failure_snapshots_before_release_cleanup.log` | `ab319cd410beb2180a51471e1ce9283e9f2b6da42404a1cbe0e78d23d95ff76d` |
| `RED_test_4_denied_process_inspection_records_unavailable_reason.log` | `cf6769a228ae149d10c1b32d94bebb0328754eb11ed3a2d3416d9cb2dd7e2890` |
| `RED_test_4_missing_applet_is_explicit_without_unrelated_processes.log` | `dee0154d5ea5103174f9dce7442751477e0347b4000ff1003f44e9516f654da7` |
| `RED_test_4_open_nonzero_snapshots_before_returning_failure.log` | `2b37d26eef7d1e701fe36e4b9843f37d382b432d7a4bb68686ae13ba3f2d5998` |
| `RED_test_4_open_timeout_snapshots_without_retry_or_longer_timeout.log` | `be7e64c0bce7aaf06c69b693dabed67e79d2d223d8274f6094db7bdc28e2d2ce` |
| `RED_test_4_snapshot_filter_keeps_applet_and_all_unordered_descendants.log` | `d1bfa6053a6f4f1f91e0c1843d2983c20f8c63a921d7d09da71562f7f2c9da60` |
| `RED_test_4_snapshot_filter_matches_executable_paths_with_spaces.log` | `419d29bb0568c76158a0822cbd50611c5073f8f9a5f3f29646946b92fb245412` |
| `RED_test_4_timed_out_process_inspection_records_unavailable_reason.log` | `f31df7993fc50b3f969e7547f244e908d580510787ed79c8814fec79cd70201e` |
| `host_launcher_checks_mb16.py` | `61683c2d8f0a48def55771f48133c7037404e788cfce7805bab926af476937c9` |
| `protected_after.json` | `ab54974d67f8cdde2556b9ae724520de4bbfebbbd29d624a4a12e5403c36a2f4` |
| `protected_before.json` | `ab54974d67f8cdde2556b9ae724520de4bbfebbbd29d624a4a12e5403c36a2f4` |
| `test_host_launcher_checks_mb16.py` | `bf76ea4642e39d1eae69ef3eda3d10ebb9c97d01c3d2ca341703458272ebbd4a` |
| `verification.json` | `e1ddd9d2a602e0d92618ab188af092018b0efb54bb46fb5298a2bafe0d7d3178` |

## Handoff

Done: helper change, 21 per-test behavioral RED receipts, 21-test GREEN run, protected-file and assertion verification, and host commands. Half-applied work: none. All created/changed files are confined to `results/backup_gdrive_mb16_20261010T103826Z/`; the tables and detached manifest enumerate their exact paths and SHA-256s. Main helper: `results/backup_gdrive_mb16_20261010T103826Z/host_launcher_checks_mb16.py` (SHA-256 `61683c2d8f0a48def55771f48133c7037404e788cfce7805bab926af476937c9`). Tests: `results/backup_gdrive_mb16_20261010T103826Z/test_host_launcher_checks_mb16.py` (SHA-256 `bf76ea4642e39d1eae69ef3eda3d10ebb9c97d01c3d2ca341703458272ebbd4a`). Next step: MAESTRO runs the three host commands, inspects failure snapshots if necessary, obtains GPT-6-Astra review and handles any commit. Open risk: other memit accesses may still hang; fixture/static success is not native execution evidence.

**Binding context directive, carried forward:** watch `Context N% left` for this session and every orchestrated team session. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work, write a handoff at the end of the build report with completed/in-flight/half-applied work, exact paths and SHA-256s, next step and risks, and reply `CONTEXT HANDOFF WRITTEN`. On `Context compacted`, do the same at once. AGENTS.md also binds: before roughly 20% remains, stop new work and write the precise handoff; never approach full-window compaction; restate the directive in every successor handoff.
