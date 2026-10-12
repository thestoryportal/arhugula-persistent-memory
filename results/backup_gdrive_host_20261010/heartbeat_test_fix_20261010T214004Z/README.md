# MB30 held-lock heartbeat test fix — DONE

The fixed single test passes 10/10 in all four interpreter/observer arms. The original test had 0/10 pass, 10/10 fail in arm iv. The fixed test catches a real refused-contender overwrite mutation at the unchanged full byte-equality assertion. The final safe full suite in arm iii ran 134 cases: 120 passed, 14 existing host-rclone skips, zero failures/errors (260.840 seconds; exit 0). All 18,517 recorded owned PIDs are absent. Two earlier receipt-collector failures are retained and documented below.

Only `HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat` changed in `tools/test_backup_gdrive_addendum.py`. The test polls every 10 ms for up to three seconds, requiring a running owner, the dispatch marker, the matching heartbeat owner PID, and a positive published child PID equal to `lock/rclone.pid`. The timeout fails with the unmet conditions. The snapshot and all refusal/receipt/byte-equality/health assertions follow that publication barrier unchanged.

## Frozen source and scope

`cefd5ff` is an ancestor of the initial HEAD; its test bytes match the frozen pin. See `start_git.json`, `start_sha256.json`, `candidate_sha256.json`, `final_sha256.json`, and `scope_check.json`. Every byte before and after the named test is identical to the frozen source. No backup tool was edited. Existing MB29 and dashboard modifications were left untouched.

| File | Start SHA-256 | Final SHA-256 |
|---|---|---|
| `tools/backup_gdrive_status.py` | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` |
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` |
| `tools/test_backup_gdrive_addendum.py` | `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e` | `b764938802edf101be01493d24012a586076ca9f00bbfba2193c70336e54fdf1` |

## Causal RED and mutation

`red_matrix.log` and `red_arm_iv/arm_iv/run_01` through `run_10` retain ten unmodified-test failures, one assertion failure each, zero errors/skips. `red_causal_summary.json` verifies unchanged owner PID, child PID null to the dispatched positive PID, bytes 0 to null, and separate exit-75 refusal receipts. This reproduces delayed owner publication, rather than a contender write.

`run_mutation.py` copied only the shell and byte-identical status tool into owned scratch, removed the non-owner refusal-target routing line, and patched the throwaway runner's `BACKUP` path. Both owner and contender executed the scratch shell. The fixed test reached exit 75 and failed at the preserved full heartbeat byte comparison: one test, one failure, zero errors/skips. Evidence: `mutation.patch`, `mutation_matrix.log`, `mutation_result.json`, and `mutation/arm_iii/run_01/test.log` plus before/after heartbeat bytes. The scratch tools were removed; `mutation_removed.json` confirms removal and unchanged candidate pins.

```text
AssertionError: b'{"b[14 chars]ed": 0, "end": "2026-10-10T21:41:58.865335+00:[874 chars]0}\n' != b'{"b[14 chars]ed": null, "end": null, "exit_code": null, "la[859 chars]5}\n' : a non-owner cannot publish over the active owner
```

## Fixed four-arm matrix

| Arm | Runner | Backup tool Python | Tracing observer | Pass | Fail | Errors/skips | Logs |
|---|---|---|---|---:|---:|---|---|
| i | `.venv/bin/python` | `.venv/bin/python` | No | 10 | 0 | 0/0 | `green_four_arms/arm_i/run_01` through `run_10` |
| ii | `.venv/bin/python` | `/usr/bin/python3` | No | 10 | 0 | 0/0 | `green_four_arms/arm_ii/run_01` through `run_10` |
| iii | `/usr/bin/python3` | `/usr/bin/python3` | No | 10 | 0 | 0/0 | `green_four_arms/arm_iii/run_01` through `run_10` |
| iv | `/usr/bin/python3` | `/usr/bin/python3` | MB25 sitecustomize | 10 | 0 | 0/0 | `green_four_arms/arm_iv/run_01` through `run_10` |

Each run has `test.log`, `result.json`, `runtime.json`, `command.json`, `assertion.json`, before/after heartbeat bytes, `started_processes.json`, and `descendants.json`; arm iv additionally has `execution_trace.jsonl`. Every byte comparison was identical. All 40 test outcomes are retained, without whole-test retries or new skips. Tool-version trace records in arm iv confirm Python 3.9. The copied MB28 runner overrides Fixture's captured interpreter for arm ii; otherwise Fixture would force the runner interpreter.

## Full suite and collector incident

The safe selection is exactly MB25's 13 classes, 134 cases, excluding `LauncherTest`. `BACKUP_TEST_NO_RCLONE=1` retains the existing 14 host-rclone skips. Each suite uses arm iii, no tracing observer, fresh isolated HOME and fixture roots. The full-suite runner guards native/rclone Popen commands.

The first attempted suite, `full_addendum/arm_iii/run_01/test.log`, ran all 134 cases: zero assertion failures, two receipt-collector cleanup errors, 14 skips. The collector attempted to copy the FIFO from `test_one_thousand_live_owner_refusals_have_bounded_storage` and followed the dangling symlink from `test_vanished_parent_is_warning_but_dangling_symlink_escape_is_fatal`. The second instrumented attempt, `full_addendum_symlink_capture/arm_iii/run_01/test.log`, ran 134 cases: zero assertion failures, one FIFO collector cleanup error, 14 skips. This was my receipt instrumentation mistake. No test assertion or tool was changed to address it.

The final `run_safe_addendum.py` (identical to `run_safe_addendum_no_capture.py`) retains per-test runtime, logs, byte assertions and owned-PID evidence without copying complete fixture trees. The final fresh invocation, `full_addendum_final/arm_iii/run_01/test.log`, reports **134 run, 120 passed, 14 skipped, zero failures/errors, exit 0**. Counts and class selection are saved in `full_addendum_final/arm_iii/run_01/result.json` and `suite_selection.json`; controller output is `full_addendum_final_matrix.log`. The two failed instrumentation attempts remain in place. Their collector source versions are preserved as `run_safe_addendum_before_collector_fix.py` and `run_safe_addendum_symlink_capture.py`. See `suite_collector_incident.json` and `collector_red_green.json`. The final receipt does not copy FIFO/symlink fixture trees; the requested single-test evidence retains its controlled fixture copies.

## Safety and remaining verification

No real rclone, network, Drive access, native/applet build/launch, osascript, open, launchctl, git mutation, or real `~/Library/Logs/memit-gdrive-backup*` access was performed. Each test inherits a fresh outer HOME and Fixture patches HOME again. Cleanup releases/reaps only owned fixtures. The eight specified pre-existing leaked PIDs are excluded from traversal and are never signalled.

All finished runners show no live owned processes, and every descendant-observation run passed its own-runner positive control. `verify_receipt.py` checked the exact 18,517 recorded PIDs from directly started subprocesses, fixture child PIDs, descendants and matrix controllers: **none is alive**. `final_process_clearance.json` records the PIDs and an empty alive list. Synchronous helper invocations returned and were reaped. No process from the exclusion set was queried or signalled. `acceptance.json`, `final_verification.log`, `final_sha256.json`, and `scope_check.json` contain the recomputable closeout evidence. `git diff --check -- tools/test_backup_gdrive_addendum.py` passed. Live Drive/native behavior remains UNRUN and outside this task.

## Exact controller commands

Commands ran from the worktree root. Each matrix iteration creates a fresh HOME and sets `LLMDB_ROOT` to this worktree, `BACKUP_TEST_NO_RCLONE=1`, `PYTHONDONTWRITEBYTECODE=1` and its isolated fixture root. Interpreter/observer arm overrides are recorded in each `command.json` and `runtime.json`. The fixed-arm aggregates are `green_four_arms/arm_i.log`, `arm_ii.log`, `arm_iii.log`, and `arm_iv.log`.

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/run_matrix.py red_arm_iv iv > results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/red_matrix.log 2>&1
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/run_mutation.py
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 MB30_PIN_FILE=candidate_sha256.json /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/run_matrix.py green_four_arms > results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/green_matrix.log 2>&1
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 MB30_PIN_FILE=candidate_sha256.json MB30_ITERATIONS=1 MB30_SAFE_SUITE=1 BACKUP_PYTHON=/usr/bin/python3 BACKUP_TEST_NO_RCLONE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/run_matrix.py full_addendum_final iii > results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/full_addendum_final_matrix.log 2>&1
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/verify_receipt.py > results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/final_verification.log 2>&1
```

The two prior full-suite controller commands used the same environment and `run_matrix.py` invocation, with phase arguments `full_addendum iii` and `full_addendum_symlink_capture iii` and corresponding `*_matrix.log` destinations. Source identities and all failed outcomes are retained; no outcome was replaced by a later pass. Existing output phase names refuse overwriting, so reruns require a fresh phase name/receipt and the appropriate source pins.

## Diff

```diff
--- a/tools/test_backup_gdrive_addendum.py
+++ b/tools/test_backup_gdrive_addendum.py
@@ -420,11 +420,27 @@
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
         self.addCleanup(owner.communicate, timeout=8)
         self.addCleanup(release.touch)
+        # Allow up to three seconds for the owner's post-dispatch PID publication.
         deadline = time.monotonic()+3
-        while not entered.exists() and owner.poll() is None and time.monotonic()<deadline:
+        child_pid_path = self.base/"lock/rclone.pid"
+        missing = ["post-dispatch heartbeat publication"]
+        while time.monotonic()<deadline:
+            value = json.loads(self.heartbeat.read_text()) if self.heartbeat.exists() else {}
+            child_pid = child_pid_path.read_text().strip() if child_pid_path.exists() else ""
+            published_pid = value.get("rclone_pid")
+            conditions = [
+                (owner.poll() is None, "running lock owner"),
+                (entered.exists(), "dispatch marker"),
+                (value.get("owner_pid") == owner.pid, "heartbeat owner_pid == owner.pid"),
+                (type(published_pid) is int and published_pid > 0 and child_pid.isdigit() and
+                 published_pid == int(child_pid), "positive heartbeat rclone_pid matching lock/rclone.pid"),
+            ]
+            missing = [name for reached, name in conditions if not reached]
+            if not missing:
+                break
             time.sleep(0.01)
-        self.assertTrue(entered.exists())
-        time.sleep(0.1)  # Wait for the child PID publication as well as dispatch.
+        else:
+            self.fail("three-second timeout waiting for: "+", ".join(missing))
         previous = self.heartbeat.read_bytes()
         result = self.backup()
         self.assertEqual(result.returncode, 75, result.stderr)
```
