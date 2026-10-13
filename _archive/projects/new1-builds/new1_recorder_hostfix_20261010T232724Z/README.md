# MB36 NEW1 recorder — READY FOR MAESTRO HOST RUN

**Sandbox GREEN: 23/23 tests. Host dispatch tests: 0 run, 19 pending.** This is a fixture-run handoff, not acceptance for the sole real invocation. MAESTRO28 succeeds MAESTRO27; the expected tracker-only HEAD transition from `02b44af91330c78f91f48b6c8e4071244411e90d` to `436c507353af33179ea73b3ba3b9324512089959` does not stop this task. A later observed HEAD `8e44cafc0439b1cad150f8666532200e489e1667` also touches only tracker/planning files (`concurrent_head.log`); the worktree/branch and source hashes remain unchanged.

Authority: MAESTRO's MB36 request and MB33's design/T1–T11 requirements in `../new1_recorder_build_20261010T225651Z/README.md`. All original requirements and six Open findings remain in force. Host evidence: `../new1_recorder_build_20261010T225651Z/maestro_green_01/test.log`, 34 tests, 9 FAIL + 5 ERROR + 20 successful (15 pure, five early refusal tests). Every traceback was read.

## Fix and causal evidence

`tools/new1_dispatch.sh` has two narrow edits:

1. `utc()` uses the existing macOS `/bin/date` rather than absent `/usr/bin/date`. No Python timestamp process was introduced.
2. Check 2f assigns `df_rows` before expanding `df_fields`, strips the retained final newline before selecting the last row, and refuses an observation without both header and data. The original numeric checks, 22,020,096-KiB minimum, raise-only override and explicit refusal receipts remain.

`save_check` records stdout, then stderr, leaving **stderr** in `REPLY`. Check 2f already explicitly reloads `2f.stdout`; that reload was correct and stays unchanged. The actual crash is zsh argument evaluation: both right-hand sides in the old single `typeset` are expanded before the first assignment, so `df_rows[-1]` is unset. An isolated shell probe reproduced that exception. A second probe showed that the real file reader retains df's terminal newline, creating an empty final array row; splitting declarations alone would still reject valid space. Both defects are caught by the added tests, including real `/bin/df` output.

The bad date path corrupts names to `new1_dispatch_.<fraction>Z`. This alone does not explain missing refusal files: the five earlier host refusal tests still found their directories. The 2f crash explains why later checks never persist their refusal/dispatch receipts. For cases whose traceback shows only the missing file or wrong exit, that common cause is a source-order inference, not a newly observed host execution.

### Every host failure → cause → fix

Cause **A**: nonexistent date path and malformed timestamp (observed in captured FAIL output). Cause **B**: check-2f unset-array expansion, before invocation, observed in captured FAIL output and reproduced in sandbox. Fix **AB**: the two edits above, including the trailing-newline correction. All rows remain **host GREEN UNRUN**.

| Host test | Failure in host log | Cause and fix |
|---|---|---|
| `test_T10_unreaped_group_blocks_compute` | Missing dispatch receipt; stderr includes A/B | AB; restore progress to fixture launch/reporting, preserve disposition blocking |
| `test_T11_endorsed_argv_cwd_env` | Exit 1 rather than 0; stderr includes A/B | AB; endorsed exec bytes remain identical |
| `test_T1_observed_recorder_line_not_blocker` | Exit 1 rather than 0; stderr includes A/B | AB; recorder still shell-only while supervisor lives |
| `test_T2_happy_path` | Exit 1 rather than 0; stderr includes A/B | AB; PID/niceness/group assertions unchanged |
| `test_T3_f_stricter_disk_floor` | Missing `refused_before_invocation.json` | B inferred from reaching 2f; AB lets the strict-floor refusal persist |
| `test_T3_g_fingerprint_failure` | Missing refusal receipt | B inferred before 2g; AB preserves fingerprint failure refusal |
| `test_T3_h_dry_probe_refusal` | Missing refusal receipt | B inferred before 2h; AB preserves dry-probe refusal |
| `test_T3_i_hash_changed_after_first_check` | Missing refusal receipt | B inferred before 2i; AB preserves the second hash check |
| `test_T5_worker_nice_three_requests_supervisor_sigint` | Missing dispatch receipt; stderr includes A/B | AB; SIGINT/mismatch logic and assertions unchanged |
| `test_T6_deadline_no_halted_event` | Exit 1 rather than 3 | B inferred from the same pre-invocation path; AB; deadline accounting unchanged |
| `test_T7_resource_halted_event` | Exit 1 rather than 3 | B inferred from the same path; AB; resource accounting unchanged |
| `test_T8_internal_admission_refused` | Exit 1 rather than 3 | B inferred from the same path; AB; invocation consumption boundary unchanged |
| `test_T9_third_abort_reached` | Exit 1 rather than 3 | B inferred from the same path; AB; abort union/third-abort rule unchanged |
| `test_disk_floor_cannot_be_lowered` | Missing refusal receipt | B inferred at 2f; AB; lower floors still refuse |

No separate defect is established by these tracebacks after the common pre-invocation crash. Host testing may reveal additional failures; this receipt makes no claim that the 19 process tests pass.

## Tests and sandbox evidence

**No existing test was corrected, deleted, skipped or weakened.** `verify_hostfix.py` compares the AST of every original test and helper against the before copy: all 34 tests and their existing helpers are identical. `tools/new1_dispatch_report.py` is byte-for-byte unchanged. Eight new methods were added to `PureTests`:

| New test | Contract exercised |
|---|---|
| `test_recorder_absolute_executables_exist` | Every literal executable path under an absolute bin/sbin path exists and is executable; includes the shell shebang |
| `test_recorder_utc_has_complete_timestamp` | Actual `utc()` emits complete ISO UTC with no stderr |
| `test_recorder_disk_reads_real_df_stdout` | Actual 2f/check/file-reader code consumes real Mac `/bin/df` output |
| `test_recorder_disk_exact_floor_with_trailing_newline` | Exactly 22,020,096 KiB passes with the normal terminal newline |
| `test_recorder_disk_shortage_refuses` | 22,020,095 KiB refuses and persists an unconsumed-authorization receipt |
| `test_recorder_disk_invalid_observation_refuses` | Empty, header-only and nonnumeric observations refuse with receipts |
| `test_recorder_disk_invalid_or_lowered_floor_refuses` | Invalid and lowered floors refuse |
| `test_recorder_disk_raised_floor_refuses` | Unaffordable raised floor refuses |

These shell component checks extract and execute the actual recorder prefix/functions/2f section in `/private/tmp/new1-shell-check-*`. Controlled input cases replace only the external df observation with `/bin/cat` of a declared fixture; the real-df case makes no substitution. They do not invoke admission, ps, supervisor or worker. The test process ends after the bounded component checks; no Python poller was added to production.

| Evidence directory/file | Result |
|---|---|
| `sandbox_red_pure/test.log` | 23 tests with original recorder and added tests, exit 1: original 15 pass; all eight new methods fail, 11 failure records including subtests, zero errors |
| `sandbox_green_pure/test.log` | 23/23 PASS, zero failures/errors, exit 0 |
| `sandbox_red_pure/command.json`, `sandbox_green_pure/command.json` | Exact suite command/cwd/interpreter/SHA-256, interpreter binary hash, source snapshots and generated shell source bytes |
| `command.json` | Final GREEN command plus all source/test/generated-shell hashes, wrapper command, verification command/source and counts |
| `verification.log` | Final verification exit 0; source/scope summary |
| `checks.json` | 34 original tests unchanged; reporter and endorsed exec identical; 10 protected files and 143 tracked engine entries unchanged |
| `executable_paths.log`, `.stderr`, `.command.json` | Exact `ls -l` of every absolute recorder tool plus resolved Python/git; exit 0, empty stderr |
| `shell_syntax.log`, `.stderr`, `.command.json` | `/bin/zsh -n` exit 0; Python sources also compiled without execution/cache writes |
| `before/`, `before.sha256`, `final_sources.sha256` | Original three files saved before any edit; final source hashes |
| `sandbox_process_probe.json` | `/bin/ps` launch raised PermissionError; host process observation UNAVAILABLE |

Exact sandbox runner commands, issued separately from the worktree root:

```sh
LLMDB_ROOT=$PWD /usr/bin/python3 -B results/mathlab_staging/new1_recorder_build_20261010T225651Z/record_test_run.py results/mathlab_staging/new1_recorder_hostfix_20261010T232724Z/sandbox_red_pure "$PWD" red --pure
LLMDB_ROOT=$PWD /usr/bin/python3 -B results/mathlab_staging/new1_recorder_build_20261010T225651Z/record_test_run.py results/mathlab_staging/new1_recorder_hostfix_20261010T232724Z/sandbox_green_pure "$PWD" green --pure
LLMDB_ROOT=$PWD /usr/bin/python3 -B results/mathlab_staging/new1_recorder_hostfix_20261010T232724Z/verify_hostfix.py
```

The suite subprocess's recorded interpreter is `/Library/Developer/CommandLineTools/usr/bin/python3`; the provenance wrapper was invoked with `/usr/bin/python3`. `own_niceness` is null: no numeric host niceness or process-clearance claim is made. No host dispatch test was run here, including the early prechecks. Evidence files are small; no bulk-write job ran.

## Absolute tools verified with ls -l

All 16 literal tool paths exist with executable permission:

```text
/bin/cat
/bin/cp
/bin/date
/bin/df
/bin/mkdir
/bin/mv
/bin/ps
/bin/rmdir
/bin/sleep
/bin/zsh
/usr/bin/awk
/usr/bin/env
/usr/bin/plutil
/usr/bin/python3
/usr/bin/shasum
/usr/bin/tr
```

Also verified: `/usr/bin/git` (the resolution of the recorder's `git` command) and `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python` (the recorder's `$ROOT`/`$PWD` expansion). The latter resolves to the existing uv-managed Python executable. Filesystem existence of `/bin/ps` does not assert sandbox execution permission. The initial `ls -l /usr/bin/date` reported no such file; the new executable-path regression fails on that original path in RED.

## Exact next host commands — MAESTRO28

Run **separately** from the operator's process-visible **niceness-0** shell. The runner still verifies its own niceness exactly 0 and refuses if observation fails. Fresh labels `maestro_red_02`, `maestro_green_02` were absent at handoff. Do not let expected RED exit 1 prevent the independent GREEN command.

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
LLMDB_ROOT=$PWD results/mathlab_staging/new1_recorder_build_20261010T225651Z/run_tests.sh maestro_red_02 red
LLMDB_ROOT=$PWD results/mathlab_staging/new1_recorder_build_20261010T225651Z/run_tests.sh maestro_green_02 green
```

RED uses the **unchanged existing runner** to copy the updated test file, gate and event reader into an exclusive mktemp root and omit both recorder implementation files. It is expected to fail all 42 tests for missing implementation, without editing the worktree back and forth. GREEN runs all **42 tests (23 pure/component + 19 dispatch)**. Review both runs' exact command/source hashes, process snapshots, cleanup assertions and exit records. If a label is already used, choose fresh labels. No real supervisor/worker is part of this fixture suite.

Runner pins, unchanged:

```text
a5ea1834515cf33cee18a22ff7807d87b40f050dcb399b4666a339fcee5fe860  ../new1_recorder_build_20261010T225651Z/run_tests.sh
8870f60985c94f1846c6fc820e5aeae1cb5c33a9c184255dc141962c418df2d5  ../new1_recorder_build_20261010T225651Z/record_test_run.py
```

## Original Open findings — retained, outside this Mac failure fix

The six findings in MB33's README are still **OPEN**: INCOMPLETE may return shell success; nonzero/malformed supervisor niceness is not stopped promptly; timeout receipt/history schema mismatch; earlier stdout abort evidence can be lost; conflicting terminal history may disagree with canonical fold; fixture emergency cleanup lacks post-kill disappearance proof. This task neither fixes nor dismisses them. They must be resolved before acceptance for the real sole invocation. Host fixture GREEN would not close them or authorize production.

## Final SHA-256 and scope

```text
287aa59fe283168eeaee961e64db951070e35850a8f38e29bf24dbf2f862cd9a  tools/new1_dispatch.sh
955079238e533b6609d5c98454155b83adeac1ce0b9e3070e0da91f4f0c005fe  tools/new1_dispatch_report.py
c3de58e98c6c5a1c670e99e2f38bdd161757f796d09d2c973852b416b04c29bd  tests/test_new1_dispatch.py
```

The reporter is listed for completeness and remains unchanged. The full recorder comparison allows only the date-path and 2f parsing edits; therefore all prechecks, own-niceness-0 rule, one-use authorization, consumption boundary, env/argv and production exec bytes are preserved. `endorsed_exec.before.txt`/`.after.txt` are identical. The engine manifest verifies 131 regular file hashes and 12 symlink targets; symlink target content is outside that tracked-entry comparison.

No real supervisor/worker/model/GPU/MPS run, authorization consumption, commit, canonical tracker edit or write under real `results/mathlab_staging/runs/` occurred. MB35's files and existing dashboard changes were left untouched. The operator-authorized tracker-only HEAD change is recorded in `checks.json`.

## Handoff and saved context

Done: both narrowly scoped shell fixes; eight added regressions; saved before copies; sandbox RED/GREEN; executable-path, original-test, protected-scope, engine and endorsed-command checks; provenance and host instructions. Half-applied edits: none. In-flight task-owned processes: none. Exact changed paths/hashes and failing historical/RED commands are above; no final sandbox failure remains. Still pending: MAESTRO28's host RED then GREEN and review of resulting 19 dispatch outcomes. Risks: host runtime behavior remains unverified and the six original Open findings remain. Next step: execute the two host commands above; do not run production. `context_saved.md` preserves the session state within the authorized receipt directory.

Binding context directive: watch `Context N% left` for this session and every orchestrated team session. Start a new piece of work only at >=60% left. At <=40% left or any `Context compacted`, stop starting work immediately; write a handoff at the end of the README with what is done/half-applied/in-flight, exact changed file paths/SHA-256, failing tests with exact commands, next step and open risks, then reply exactly `CONTEXT HANDOFF WRITTEN`. Every successor handoff must restate this directive.
