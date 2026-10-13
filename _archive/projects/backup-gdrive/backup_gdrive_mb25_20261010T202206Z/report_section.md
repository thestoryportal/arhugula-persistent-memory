
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
