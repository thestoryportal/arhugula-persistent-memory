# MB28: held-lock heartbeat diagnosis

**Verdict: (b), a race in the test. Production is not exposed to the alleged held-lock-refusal overwrite in the reproduced failures.** The owner publishes its second start heartbeat after the test takes its supposedly stable snapshot. The refused contender publishes a separate refusal receipt. All 27 failing matrix runs retain the same owner PID and run ID across the heartbeat change.

Report-only, branch `worktree-c10k-route-a`; MAESTRO25 verifies and commits. No source edits, commits, pushes, merges, network, Drive access, real rclone, or native/applet execution. MB25's unverified README was neither read nor used.

## Four required arms

Only `tools.test_backup_gdrive_addendum.HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat` ran. Every repetition has a fresh `tempfile.mkdtemp` outer HOME and the test's separate fresh fixture HOME. All use `-B`, `PYTHONDONTWRITEBYTECODE=1`, `BACKUP_TEST_NO_RCLONE=1`, and this worktree's LLMDB_ROOT. The fake rclone config branch prints `{}` and its sync branch waits for a fixture release file; it never invokes real rclone.

| Arm | Runner | Effective wrapper BACKUP_PYTHON | MB25 observer | Pass | Fail |
| --- | --- | --- | --- | ---: | ---: |
| i | `.venv/bin/python` 3.11.16 | Fixture default: `.venv/bin/python` | No | 10 | 0 |
| ii | `.venv/bin/python` 3.11.16 | `/usr/bin/python3` 3.9.6 | No | 1 | 9 |
| iii | `/usr/bin/python3` 3.9.6 | `/usr/bin/python3` 3.9.6 | No | 2 | 8 |
| iv | `/usr/bin/python3` 3.9.6 | `/usr/bin/python3` 3.9.6 | Original MB25 observer | 0 | 10 |

**40 tests: 13 pass, 27 assertion failures, 0 errors, 0 skips.** Every failure is the byte comparison at `tools/test_backup_gdrive_addendum.py:431`. Every failed snapshot changes `bytes_transferred: 0 -> null` and `rclone_pid: null -> positive PID`, without changing ownership. No interpreter exception or differing JSON meaning was observed. The 3.9 timing makes the fixed wait inadequate; the observed change follows the same heartbeat contract. Failures without the observer rule out (d) as the necessary cause. The named owner publication rules out (a). This is (b), rather than a demonstrated 3.9 semantic difference (c). Counts describe this local schedule, not general failure probabilities.

Raw evidence: [matrix.log](matrix.log), [matrix_results.json](matrix_results.json), [four_arm_counts.json](four_arm_counts.json), and every `arm_{i,ii,iii,iv}/run_{01..10}/test.log`. Each run also saves `command.json`, `runtime.json`, exact `heartbeat_before.json` / `heartbeat_after.json`, decoded `assertion.json`, and process checks. [matrix_assertion_summary.json](matrix_assertion_summary.json) covers all 40 runs.

The executed command was:

```sh
/opt/homebrew/bin/rtk proxy /bin/bash -c 'LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$1/run_matrix.py" > "$1/matrix.log" 2>&1' bash results/backup_gdrive_host_20261010/py39_heartbeat_diag_20261010T212344Z
```

[run_matrix.py](run_matrix.py) saves the exact per-run interpreter argv, cwd, and environment. [run_single.py](run_single.py) executes the original named method through unittest; the method and its wait are unchanged. Common runner-only hooks record Popen objects, capture the already-evaluated assertion bytes, and copy the fixture after owner cleanup. Arms i–iii have no PYTHONPATH observer or profile hook in the status subprocesses. The assertion snapshots are authoritative; `fixture_copy/` contains the later terminal heartbeat after owner cleanup.

**Arm ii detail:** `Fixture.setUp` at `tools/test_backup_gdrive_addendum.py:40` resets BACKUP_PYTHON to `sys.executable`, and HeartbeatTest captures that environment at `:259`. An outer variable alone would collapse ii into i. The diagnostic runner overrides captured `self.env` and `os.environ` immediately after setup for explicit-interpreter arms. Each `runtime.json` proves the effective setting. The original test's read-only health subprocess uses the runner interpreter; the wrapper's record/preflight/classify subprocesses use the table's BACKUP_PYTHON.

Arm iv uses the original receipt's `observer/` on PYTHONPATH, PY39_TRACE pointing to the new run's execution trace, and PY39_TARGET_STATUS pointing to this worktree's status tool, as `run_safe_suites.sh` sets them. `/usr/bin/python3` reports resolved executable `/Library/Developer/CommandLineTools/usr/bin/python3`, version 3.9.6.

## Actual writer and captured bytes

A failing required-arm sample is [arm_iv/run_01/test.log](arm_iv/run_01/test.log). Its [before bytes](arm_iv/run_01/heartbeat_before.json), [after bytes](arm_iv/run_01/heartbeat_after.json), and [decoded changes](arm_iv/run_01/assertion.json) show:

| Field | Before | After |
| --- | --- | --- |
| owner_pid | 3377 | 3377 |
| run_id | `20261010T212521Z-3377` | `20261010T212521Z-3377` |
| bytes_transferred | 0 | null |
| rclone_pid | null | 3396 |
| rclone_version | null | `rclone-test` |
| wrapper_log_offset | 0 | 1046 |
| end / exit_code | null / null | null / null |

The original observer's [raw execution trace](arm_iv/run_01/execution_trace.jsonl) names the executing processes and arguments; [record_writers.json](arm_iv/run_01/record_writers.json) extracts them:

| Trace line | Python PID | Parent wrapper | Publication |
| ---: | ---: | ---: | --- |
| 5 | 3388 | Owner 3377 | `last_run.json`, start, sync_started=0, child=0 |
| 13 | **3397** | **Owner 3377** | **`last_run.json`, start, sync_started=1, child=3396** |
| 16 | 3420 | Refused 3407 | `refusals/latest-refusal.json`, end, exit=75 |
| 22 | 3434 | Owner 3377 | `last_run.json`, end during cleanup after the assertion |

**Writer: owner child Python PID 3397**, executing `record` at `tools/backup_gdrive_status.py:200`, whose atomic publication is at **`:235`**. The owner dispatches it through **`tools/backup_gdrive.sh:133`** and **`:43`**. Its arguments and child PID match the after bytes. The refused wrapper is PID 3407; its Python writer 3420 targets the separate refusal path.

For direct atomic-write evidence, one supplemental invocation of the same named test used [write_audit_observer/sitecustomize.py](write_audit_observer/sitecustomize.py). It is excluded from all four counts. This observer wraps only the pinned tool's `record` call to os.replace, logs the caller line and live lock owner, saves old/new bytes, and performs the original replace. Its extra read/log overhead is not used to compare arm rates.

That invocation failed at the same assertion: [write_audit_run/test.log](write_audit_run/test.log). Event 2 of [write_audit_run/write_audit.jsonl](write_audit_run/write_audit.jsonl) directly records **Python PID 10255**, parent and lock owner **10236**, executing **`tools/backup_gdrive_status.py:235`**. At publication, `lock/owner` contains `10236 20261010T212941Z-10236`. Its actual publication bytes exactly match the assertion's snapshots:

| Bytes | Assertion snapshot | Writer snapshot | SHA-256 |
| --- | --- | --- | --- |
| Before | `write_audit_run/heartbeat_before.json` | `write_audit_run/write_10255_before.bin` | `ac5ee65f015959e3b3342ed9b91029d5146f75d750023917491a8e232d50ad66` |
| After | `write_audit_run/heartbeat_after.json` | `write_audit_run/write_10255_after.bin` | `69a5623843ce42a0a6bbcbe64db8448c49d4d3a537804c494a9a628c15e5df4d` |

Event 3 records Python PID 10280, parent refused wrapper 10266, publishing only `latest-refusal.json`, exit 75, while the lock still belongs to 10236. [diagnosis_evidence.json](diagnosis_evidence.json), [analyze_receipt.py](analyze_receipt.py), and [analysis.log](analysis.log) verify these byte matches, writer ownership, all counts, and unchanged source pins.

## Race, production impact, and proposed fix

The wrapper acquires the directory lock at `tools/backup_gdrive.sh:78`, sets LOCK_OWNED=1 at `:82`, and publishes the initial start record at `:84`. It dispatches the fixture child at `:123`, captures its PID at `:131`, writes `lock/rclone.pid` at `:132`, and publishes the second start record at `:133`. Both owner publications occur under the same held directory lock. `record` atomically replaces the target at `tools/backup_gdrive_status.py:235`; it acquires no additional lock itself.

The fake child touches `owner-dispatched` in the script constructed at `tools/test_backup_gdrive_addendum.py:416`. The test waits for that marker at `:422`, sleeps a fixed 100 ms at `:426`, then snapshots at `:427`. The child marker can exist while the owner's second Python process is still starting or publishing. In all 27 failed matrix snapshots, rclone_pid is still null: the assumed publication barrier has not been crossed. The second owner publication then completes while the contender refuses, invalidating the byte comparison at `:431`.

On refusal, mkdir fails and the wrapper exits 75 at `tools/backup_gdrive.sh:78-80`, leaving LOCK_OWNED=0. Its EXIT trap calls finish at `:67`; write_heartbeat selects `refusals/latest-refusal.json` at `:42`. The runtime writer evidence confirms that it does not publish over the owner's `last_run.json`.

The production 0-to-null transition is expected: `tools/backup_gdrive_status.py:211` records zero before dispatch and unknown transferred bytes once sync starts; `:216` records the child PID. Both start records remain incomplete (end=null, exit_code=null). This reproduced failure exposes neither a held-lock overwrite nor a false completed-success heartbeat. This conclusion concerns this failure; live Drive and native launcher behavior remain UNRUN.

**Proposed test-only fix, NOT APPLIED:** replace the fixed sleep/snapshot preparation at `tools/test_backup_gdrive_addendum.py:422-427` with bounded polling. Before taking previous, require the owner still running, the dispatch marker present, heartbeat owner_pid equal to owner.pid, and a positive published rclone_pid equal to `lock/rclone.pid`; fail clearly on timeout. The same file's `test_inflight_is_visible_and_missing_stats_are_unknown` uses a publication condition at `:304-313`, and Fixture.hold_live_owner also waits for a published child PID. Preserve the refusal, receipt, byte-equality, and health assertions. No production change is indicated by this evidence.

## Original receipt, unchanged hashes, and process clearance

Verified original commit: `a14e7720a6dce3960749868b1e0318e8b2e17313`. [mb25_raw/run_safe_suites.sh](mb25_raw/run_safe_suites.sh) records the system Python, isolated HOME, BACKUP_PYTHON, no-rclone flag, observer PYTHONPATH, and trace route. [mb25_raw/addendum_suite.log](mb25_raw/addendum_suite.log): lines 138-143 identify the test, source line 431, and bytes_transferred changing 0 to null; lines 146-148 record **134 run, 1 failure, 14 skipped**. The saved exit is 1. Raw copies include the original execution trace, scripts, and pins, without the original README.

These SHA-256s matched the original start_sha256.json before investigation, were checked before each test, and remain identical afterward:

| File | SHA-256 |
| --- | --- |
| tools/backup_gdrive_status.py | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` |
| tools/backup_gdrive.sh | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| tools/test_backup_gdrive_addendum.py | `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e` |

See [start_sha256.json](start_sha256.json), [end_sha256.json](end_sha256.json), and numbered [source_excerpts.txt](source_excerpts.txt). No tools/ or tests/ file was edited. MB27's excluded supervisor and staging paths were ignored.

**Process clearance: no process started for these test runs remains alive.** Direct Popen children were waited/reaped. Every run's started_processes.json checks its wrappers, health subprocesses, and fixture sync PID. `/bin/ps` was sandbox-denied; libproc queries were restricted to newly started runner PIDs, with a positive control seeing the runner in all 40 repetitions. Each descendants.json records descendants and their absence after runner exit. The supplemental run saves [descendant_checks.json](write_audit_run/descendant_checks.json). [final_process_checks.json](final_process_checks.json) checks recorded task-owned PIDs, including observer-discovered writers and fixture children. No process was killed. None of the eight pre-existing leaked PIDs was inspected, signaled, or changed. All backup state access stayed in the new receipt's isolated fixtures; real ~/Library/Logs/memit-gdrive-backup* state was neither read nor written.

Final receipt validation and protected-path git status are in [final_verification.log](final_verification.log); [artifact_sha256.json](artifact_sha256.json) hashes the receipt for review.
