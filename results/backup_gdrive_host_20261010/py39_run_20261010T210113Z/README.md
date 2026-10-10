**MB25 report-only Python 3.9 verification for MAESTRO25.** `record`, `classify`, `preflight` and `recover` all completed successfully under production `/usr/bin/python3` 3.9.6 in separate scratch fixtures. Both `record` phases wrote the expected heartbeat, `classify` emitted valid JSON, `preflight` completed its config validation using a scratch stub, and `recover` wrote a reserved barrier with preserved evidence. The safe addendum run has one assertion failure, recorded below. This report does not claim that suite is GREEN.

Receipt root: `results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/`. Branch: `worktree-c10k-route-a`. No file under `tools/` or `tests/` was edited. All four hashes were recorded before investigation and remain identical after the runs. No native/applet build or launch, osascript, open, launchctl, real rclone, network, Drive access, commit, push, merge or process termination ran. The operator's eight named native-process PIDs were excluded from our PID checks and left alone. MB27's files were ignored.

**Interpreter route and proof.** Both test files compile under 3.9.6, so the selected route was to run the test runner itself under `/usr/bin/python3 -B`. Addendum `Fixture.setUp` assigns `BACKUP_PYTHON=sys.executable` at `tools/test_backup_gdrive_addendum.py:39`, and status/recovery helpers also invoke `sys.executable` at `:52`, `:1213` and `:1600`. Wrapper tests select it at `:2086` and `:2120`. An inherited `BACKUP_PYTHON=/usr/bin/python3` alone would be overridden by a 3.11 runner. The base suite preserves the explicitly supplied `BACKUP_PYTHON=/usr/bin/python3`; production defaults to it at `tools/backup_gdrive.sh:11`. The intentional classifier-failure shim at addendum `:732` also delegates other operations to `/usr/bin/python3`.

Actual suite runner and executing status-tool interpreter:

```text
/Library/Developer/CommandLineTools/usr/bin/python3
3.9.6 (default, Aug 25 2026, 21:26:21) 
[Clang 21.0.0 (clang-2100.3.34.2)]
```

`/usr/bin/python3` resolves to that executable. The initial `.venv` probe was 3.11.16; it was not used for these suites or direct commands. `execution_trace.jsonl` contains 3290 `tool_version` events; every one reports 3.9.6 and `dont_write_bytecode=1`. Receipt-local `observer/sitecustomize.py` installs a read-only profile callback. When the actual status-tool function executes, it prints `sys.version` obtained from that executing frame's own globals, along with its PID, source file/line, executable and argv, into the separate trace log. It changes no tool code, inputs, stdout or stderr. Popen/temporary-cleanup observers also record task PID ownership. The observer can add timing overhead; keep that caveat with the one timing-sensitive assertion failure.

The outer suite HOME is the fresh mkdtemp `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/isolated-home-_9ccsoqn`. Addendum fixtures create additional isolated HOMEs below `results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/fixtures/`. The two base cases use their existing fresh `/private/tmp/backup_gdrive_*` roots and inherit the isolated outer HOME. Direct commands use their separate mkdtemp HOMEs listed in `direct_results.json`. All processes inherit `PYTHONDONTWRITEBYTECODE=1`; runners/direct calls use `-B`, and wrapper-invoked calls are also proven to disable bytecode writes by the inside-tool flag.

**Exact suite commands and counts.** The complete executed environment, named-test/class commands, redirections, inventory calls and exit handling are saved in `run_safe_suites.sh`. It ran once, with this command:

```sh
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/run_safe_suites.sh
```

Its base invocation selects the two held/stale-lock methods by name. Its addendum invocation selects every test class except `LauncherTest` by name. `BACKUP_TEST_NO_RCLONE=1` is set; the addendum honors it with its existing `HOST_RCLONE` decorators. The base suite does not honor it, so eight methods capable of reaching real rclone are explicitly excluded rather than run.

| Suite | Run | Passed | Failures | Errors | Skipped | Excluded | Exit | Log |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tools.test_backup_gdrive` safe methods | 2 | 2 | 0 | 0 | 0 | 8 | 0 | `base_suite.log` |
| `tools.test_backup_gdrive_addendum` safe classes | 134 | 119 | 1 | 0 | 14 | 3 | 1 | `addendum_suite.log` |

The primary addendum run took 272.510 seconds, including the 1,000-refusal stress case. No suite or individual test was rerun. Shell/Perl publisher fixtures read the applet's shell literals; they do not build or execute an applet. The whole `LauncherTest` class is omitted, including its static plist test, so no native helper is invoked.

The only suite failure is `tools.test_backup_gdrive_addendum.HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat`, assertion at `tools/test_backup_gdrive_addendum.py:431`:

```text
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_backup_gdrive_addendum.py", line 431, in test_held_lock_refusal_cannot_overwrite_owner_heartbeat
    self.assertEqual(self.heartbeat.read_bytes(), previous, "a non-owner cannot publish over the active owner")
AssertionError: b'{"b[14 chars]ed": null, "end": null, "exit_code": null, "la[790 chars]9}\n' != b'{"b[14 chars]ed": 0, "end": null, "exit_code": null, "launc[775 chars]0}\n' : a non-owner cannot publish over the active owner
```

EVIDENCE-SHOWS: the active-owner heartbeat changed from `bytes_transferred: 0` to `null` during the contender comparison; the refusal returned 75 before this assertion, and no Python 3.9 API/syntax exception appeared. I INFER: the fixture's fixed 0.1-second sleep at `:427` allowed its snapshot to precede the owner's child-PID heartbeat update. Interpreter startup and the observer may affect that window. This assertion remains unresolved; a timing cause was not established by a rerun. Proposed fixture fix, not applied: poll with the existing bounded deadline until the heartbeat's `rclone_pid` matches `lock/rclone.pid`, then take the comparison snapshot. No status-tool compatibility fix was identified or applied.

Every skip follows. Skips occur before the test body and have no traceback; the declaration file:line and exact saved skip reason are supplied instead. The reason retains the suite's existing MB14 wording although this is the MAESTRO25 verification run.

| Skipped test | File:line | Saved reason |
| --- | --- | --- |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries` | `tools/test_backup_gdrive_addendum.py:497` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_exit_publication_failure_is_loud_and_preserves_original_failure` | `tools/test_backup_gdrive_addendum.py:333` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept` | `tools/test_backup_gdrive_addendum.py:584` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_native_nonregular_skip_is_recorded_as_warning` | `tools/test_backup_gdrive_addendum.py:610` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night` | `tools/test_backup_gdrive_addendum.py:509` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_queued_source_vanish_is_warning_and_keeps_raw_exit` | `tools/test_backup_gdrive_addendum.py:549` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_real_sync_publishes_actual_bytes_and_completed_success` | `tools/test_backup_gdrive_addendum.py:276` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_remote_global_overrides_refuse_without_dispatch` | `tools/test_backup_gdrive_addendum.py:475` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.HeartbeatTest.test_start_publication_failure_invalidates_previous_success` | `tools/test_backup_gdrive_addendum.py:319` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_corrupt_remote_download_check_does_not_create_receipt` | `tools/test_backup_gdrive_addendum.py:2255` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_differing_remote_is_immutable_and_preserves_prior_manifest` | `tools/test_backup_gdrive_addendum.py:2245` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_manifest_write_failure_is_loud` | `tools/test_backup_gdrive_addendum.py:2271` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_real_copy_download_check_and_sha_receipt_never_delete_source` | `tools/test_backup_gdrive_addendum.py:2233` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |
| `tools.test_backup_gdrive_addendum.ArchiveTest.test_source_drift_after_check_does_not_create_receipt` | `tools/test_backup_gdrive_addendum.py:2263` | 'HOST-PENDING: real rclone forbidden by MB14 brief' |

Every explicit exclusion follows; none was executed, so no traceback exists.

| Excluded test | File:line | Reason |
| --- | --- | --- |
| `tools.test_backup_gdrive.BackupTest.test_three_runs_keep_old_versions_and_exclude_regenerable_files` | `tools/test_backup_gdrive.py:60` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_changing_source_between_sync_attempts_cannot_overwrite_archived_history` | `tools/test_backup_gdrive.py:85` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_empty_source_cannot_erase_existing_backup` | `tools/test_backup_gdrive.py:143` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_missing_source_refuses` | `tools/test_backup_gdrive.py:150` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_unmounted_volume_refuses` | `tools/test_backup_gdrive.py:154` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_real_rclone_failure_is_nonzero_and_logged` | `tools/test_backup_gdrive.py:158` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_interruption_retains_lock_while_child_may_still_run` | `tools/test_backup_gdrive.py:162` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive.BackupTest.test_timeout_stops_entire_sync_group_before_cleanup` | `tools/test_backup_gdrive.py:183` | Base suite lacks NO_RCLONE support; this case can invoke real /opt/homebrew/bin/rclone. |
| `tools.test_backup_gdrive_addendum.LauncherTest.test_launchd_waits_for_background_applet` | `tools/test_backup_gdrive_addendum.py:2144` | Entire LauncherTest class excluded to prevent native .app/osascript/osacompile execution; its static plist case is also excluded. |
| `tools.test_backup_gdrive_addendum.LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog` | `tools/test_backup_gdrive_addendum.py:2152` | Entire LauncherTest class excluded to prevent native .app/osascript/osacompile execution; its static plist case is also excluded. |
| `tools.test_backup_gdrive_addendum.LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest` | `tools/test_backup_gdrive_addendum.py:2184` | Entire LauncherTest class excluded to prevent native .app/osascript/osacompile execution; its static plist case is also excluded. |

**Separate direct commands.** These ran outside unittest, via the saved `run_direct_commands.py` driver. It invokes `/usr/bin/python3 -B` on the unchanged status file, captures stdout/stderr separately, checks exit status and expected output files, and validates classifier JSON before feeding it to end-record publication. Exact driver invocation:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/run_direct_commands.py
```

Actual status-tool argv and relevant environment are below. `mb25_receipt` is the absolute receipt path; the config probe environment is used only by the scratch stub. The driver's filtering removes inherited `RCLONE_*` and `BACKUP_*` variables before these commands; it reads no real credential config.

```sh
mb25_receipt="$PWD/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z"
HOME="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0" LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$mb25_receipt/observer" PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" PY39_PROBE_LOG="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/preflight_probe.txt" /usr/bin/python3 -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/backup_gdrive_status.py record --heartbeat /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/Library/Logs/memit-gdrive-backup/last_run.json --run-id py39-direct --start 2026-10-10T21:07:22.569496+00:00 --launch-generation 1 --rclone-version fixture-only --log /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/wrapper.log --run-log /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/run.jsonl --phase start --owner-pid 67718
HOME="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0" LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$mb25_receipt/observer" PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" PY39_PROBE_LOG="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/preflight_probe.txt" /usr/bin/python3 -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/backup_gdrive_status.py classify --source /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/source --run-log /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/run.jsonl --rclone-exit-code 0
HOME="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0" LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$mb25_receipt/observer" PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" PY39_PROBE_LOG="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/preflight_probe.txt" /usr/bin/python3 -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/backup_gdrive_status.py record --heartbeat /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/Library/Logs/memit-gdrive-backup/last_run.json --run-id py39-direct --start 2026-10-10T21:07:22.569496+00:00 --launch-generation 1 --rclone-version fixture-only --log /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/wrapper.log --run-log /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/run.jsonl --phase end --exit-code 0 --sync-started 1 --rclone-exit-code 0 --outcome-json '{"bytes_transferred": 7, "operations_skipped": false, "rclone_exit_code": 0, "source_vanish_only": false, "stats_status": "recorded", "warnings": []}'
HOME="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0" LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$mb25_receipt/observer" PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" PY39_PROBE_LOG="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/preflight_probe.txt" /usr/bin/python3 -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/backup_gdrive_status.py preflight --rclone /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/config-probe.sh --source /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/source --destination /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/destination
HOME="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/recovery-home-knrtsd6j" LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$mb25_receipt/observer" PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" PY39_PROBE_LOG="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/direct-home-ptlotmk0/preflight_probe.txt" /usr/bin/python3 -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/backup_gdrive_status.py recover --heartbeat /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/recovery-home-knrtsd6j/Library/Logs/memit-gdrive-backup/last_run.json --generation-floor 10
```

| Probe | Inside-tool PID | Exit | Executing function file:line | Inside-tool sys.version |
| --- | --- | --- | --- | --- |
| `record_start` | 67719 | 0 | `backup_gdrive_status.py:200` | 3.9.6 (default, Aug 25 2026, 21:26:21)  |
| `classify` | 67735 | 0 | `backup_gdrive_status.py:61` | 3.9.6 (default, Aug 25 2026, 21:26:21)  |
| `record_end` | 67758 | 0 | `backup_gdrive_status.py:200` | 3.9.6 (default, Aug 25 2026, 21:26:21)  |
| `preflight` | 67774 | 0 | `backup_gdrive_status.py:35` | 3.9.6 (default, Aug 25 2026, 21:26:21)  |
| `recover` | 67810 | 0 | `backup_gdrive_status.py:285` | 3.9.6 (default, Aug 25 2026, 21:26:21)  |

`direct/record_start.heartbeat.json` proves sequenced generation 1 with an incomplete start; `direct/record_end.heartbeat.json` proves generation 1, a completed end, exit 0 and seven transferred bytes. `direct/classify.stdout` parses as JSON with raw exit 0 and seven bytes. `direct/preflight_probe.txt` contains exactly `config dump` followed by a newline; its executable is the scratch `config-probe.sh`, not rclone. Preflight validates and returns success; it has no state-file publisher. Classify emits JSON to stdout; its captured stdout is the written artifact. Recover reserved counter/issued/barrier 11 and archived the original `corrupt` counter byte-identically; the manifest, unresolved state, counter and archived receipt/counter remain under the scratch recovery HOME. All five calls passed their independent output checks. Their stdout/stderr files, `direct_driver.log`, `direct_results.json` and the PID-matched `execution_trace.jsonl` allow this conclusion without trusting the runner version alone.

The first receipt driver failed to compile because of a generated quoting error before any status-tool command ran. It was corrected only in the receipt directory. The initial script and traceback are preserved as `run_direct_commands.initial_syntax_error.txt` and `direct_driver.initial_syntax_error.log`; this is a receipt harness error, not a production Python 3.9 incompatibility:

```text
File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/run_direct_commands.py", line 26
    stub.write_text('#!/bin/sh\n[ "$#" = 2 ] && [ "$1" = config ] && [ "$2" = dump ] || exit 43\nprintf "%s\n" "$*" >> "$PY39_PROBE_LOG"\nprintf '{"fixture":{"type":"local"}}\\n'\n')
                                                                                                                                                  ^
SyntaxError: invalid syntax
```

**Source identity and isolation.** Start SHA-256s, confirmed identical after all runs:

| File | Start SHA-256 | Final |
| --- | --- | --- |
| `tools/backup_gdrive_status.py` | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` | identical |
| `tools/backup_gdrive.sh` | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | identical |
| `tools/test_backup_gdrive.py` | `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` | identical |
| `tools/test_backup_gdrive_addendum.py` | `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e` | identical |

`start_sha256.json` and `suite_results.json` preserve these hashes. The copied inventory helper recorded identical real-HOME listings before the suites, after the suites and after all direct commands: SHA-256 `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99` for each. Thus the protected real Logs, Applications app and LaunchAgents inventory is byte-identical. `real_paths_before.json`, `real_paths_after_suites.json` and `real_paths_after_all.json` are retained.

**Process completion.** `process_check.json` records 3328 task-owned PIDs from Python starts, Popen returns, scratch sync-child PID files and the direct driver. All 3328 returned ProcessLookupError to a signal-0 liveness probe; none was alive or unavailable. A current-checker PID positive control succeeded, and checker PID 84402 was independently confirmed absent after its command returned. Signal 0 does not deliver a termination signal; no process was killed.

The requested `/bin/ps -p <our exact recorded PID list> -o pid=,ppid=,stat=,command=` was attempted and is **UNAVAILABLE**, with `PermissionError(1, 'Operation not permitted')`. `process_ps_attempt.log` preserves that denial; it is not treated as evidence of idleness. Absence is established by the separate OS liveness probes, whose full PID list and actual ps argv are in `process_check.json`. No pgrep or broad process scan was used. The operator's eight native PIDs were not queried or altered.

**Context handoff — stopped at 38% left on MAESTRO25's instruction.** No further probe, investigation or rerun was started after that instruction. This README and its existing receipts contain all available evidence.

Done: runner and status tool used `/usr/bin/python3` 3.9.6; safe base run passed 2/2 with eight rclone-capable cases excluded; safe addendum ran 134 tests, with 119 passed, one failure and 14 skips, plus three launcher-class tests excluded. Direct record-start, classify, record-end, preflight and recover calls all returned 0 and passed their output checks. Each direct call has matching inside-tool PID/function/sys.version proof in `execution_trace.jsonl`. All four source files retained their start hashes at the last verification:

- `tools/backup_gdrive_status.py`: `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` (start and last verified final identical).
- `tools/backup_gdrive.sh`: `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` (start and last verified final identical).
- `tools/test_backup_gdrive.py`: `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` (start and last verified final identical).
- `tools/test_backup_gdrive_addendum.py`: `766509ab8b1c79bc56b5f86719315c335ff87aeb051ec6b28f809aece92e434e` (start and last verified final identical).

Source changes: none. Half-applied changes: none. In-flight suites/direct jobs: none. The receipt-only driver quoting error was corrected before any direct tool call; its initial traceback remains saved. Real-HOME inventories matched before/after all runs. The PID check recorded 3,328 task-owned PIDs, all absent by signal-0 OS liveness probes with a successful current-PID positive control; none was alive or unavailable. The checker itself was then confirmed exited. No task process remains alive in the saved checks; subsequent report writes were foreground commands that completed normally. `/bin/ps` was denied and is explicitly UNAVAILABLE, not treated as evidence of idleness. No native process was queried, terminated or otherwise changed.

Open: `tools.test_backup_gdrive_addendum.HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat` failed its byte comparison at `tools/test_backup_gdrive_addendum.py:431`. The heartbeat changed from transferred bytes 0 to null. A race between the fixture's fixed sleep at `:427` and the active owner's child-PID heartbeat publication is the best current reading, **unconfirmed**. Observer/startup timing may contribute. No Python 3.9 API or syntax incompatibility was observed in the tool. The safe addendum result remains a failure; this handoff does not close it. The eight real-rclone base cases and native launcher cases remain excluded under the task boundaries. Host process-table output also remains unavailable from this sandbox.

Exact next command for a fresh successor: run only that failed case once under 3.9, without the profile observer, to check whether the same assertion fails with ordinary interpreter startup. This command has **not** been run. It creates a fresh isolated HOME and fixture root and keeps real rclone disabled; the successor must track/reap its own PIDs and retain its log. It invokes no native launcher:

```sh
mb25_next_root=$(/opt/homebrew/bin/rtk proxy /usr/bin/mktemp -d /private/tmp/gdrive_py39_handoff.XXXXXX)
/opt/homebrew/bin/rtk proxy /bin/mkdir "$mb25_next_root/home" "$mb25_next_root/fixtures"
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /usr/bin/env -u PYTHONPATH -u PY39_TRACE -u PY39_TARGET_STATUS HOME="$mb25_next_root/home" PYTHONDONTWRITEBYTECODE=1 BACKUP_PYTHON=/usr/bin/python3 BACKUP_TEST_NO_RCLONE=1 BACKUP_TEST_RECEIPTS="$mb25_next_root/fixtures" /usr/bin/python3 -B -m unittest tools.test_backup_gdrive_addendum.HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat -v > "$mb25_next_root/failing_case.log" 2>&1
```

Inspect that saved log and compare with `addendum_suite.log`; a passing rerun does not erase the primary failure or establish its cause. MAESTRO25 retains the decision on any fixture fix and production activation. Keep all changes report-only unless a new brief authorizes source edits. No source file or experiment was changed at this handoff.

**Binding context directive:** watch `Context N% left` for this and every team session. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work, append a README handoff with done/in-flight/half-applied state, exact paths and SHA-256, failing test commands and next step, then reply exactly `CONTEXT HANDOFF WRITTEN`. If `Context compacted` appears, do this immediately. AGENTS Team mode and Context management remain binding. Every successor handoff must restate this directive.
