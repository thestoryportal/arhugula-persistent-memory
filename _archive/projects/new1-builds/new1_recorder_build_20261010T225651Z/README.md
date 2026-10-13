# MB33 NEW1 recorder — READY FOR MAESTRO FIXTURE RUN

The tests, shell recorder, stdlib reporter and external test runner are written. This is a handoff for MAESTRO's RED/GREEN fixture runs, **not full acceptance or real-launch readiness**. Six open review findings remain below; MAESTRO directed no further hardening near 49% context. No commit was made. No real supervisor or geometry worker ran, no authorization was consumed, and nothing was written under the real `results/mathlab_staging/runs/`.

## Design

`tools/new1_dispatch.sh` derives ROOT from cwd, exclusively creates its dispatch directory, checks authorization SHA single use under a shell-held mkdir lock, verifies HEAD and clean pinned paths, checks the manifest, verifies its own niceness exactly 0 with `/bin/ps`, verifies volume space >=21 GiB, waits for the fingerprint and dry admission processes to finish, snapshots existing namespaces, and rechecks hashes before recording invocation consumption. `NEW1_DISPATCH_MIN_FREE_KIB` can raise the 22,020,096-KiB floor; smaller/invalid floors refuse.

The endorsed command is launched by zsh with `BG_NICE` disabled, preserving the parent's priority rather than zsh's automatic background increment. Its argv/environment assignments are recorded before exec. During the supervisor's lifetime the recorder uses shell, ps, awk and sleep; it has no Python poller. It observes a Python worker only after nice has exec'd, records its PID/parent/group/niceness, requests supervisor-PID SIGINT on worker niceness mismatch or failed process probes, and stops waiting after 60 seconds without escalation. It captures stdout/stderr, wait status, namespace set difference, and post-exit worker/group disposition. `tools/new1_dispatch_report.py` starts after wait, uses the current authoritative stdlib event reader, reconciles outcome evidence and unions abort identities across namespaces and earlier receipts. A reported PASS without observed worker nice10/supervisor nice0/parent/group proof is INCOMPLETE and blocks subsequent compute. See Open findings for remaining limitations.

**Host facts supplied by MAESTRO27, not verified in this sandbox:** main tmux server PID 21268 and every pane, including ours, run at niceness 10; a recorder started there correctly refuses check 2e. The separate operator-started tmux server must be started at niceness 0. A launchd job runs at 0 but macOS denies it file access on `/Volumes/memit`; it is not a launch route. `/bin/ps` works outside this sandbox. Production retains `/bin/ps` and the exact own-niceness-zero requirement; no host inventory is fabricated.

## Run commands

Run these separately from the operator's process-visible niceness-0 shell. RED normally exits 1 because the implementations are absent; that expected failure must not prevent the next independent GREEN command. Labels are exclusive and must be fresh on every repetition.

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
results/mathlab_staging/new1_recorder_build_20261010T225651Z/run_tests.sh maestro_red_01 red
results/mathlab_staging/new1_recorder_build_20261010T225651Z/run_tests.sh maestro_green_01 green
```

`run_tests.sh LABEL MODE` refuses unless its own observed niceness is exactly 0. RED copies the test file (which contains all fake fixture definitions), the gate and event reader into an exclusive mktemp tree, omitting both recorder implementation files. The phrase “without the three new production files” is interpreted as omitting the two implementations while retaining the test to execute it. No worktree source is edited back and forth. GREEN runs the suite in place; all launches inside the suite still use separate fixture ROOTs and throwaway git repositories.

Each executed run writes `LABEL/test.log`, `exit_code.txt`, `runner_exit_code.txt`, `ps_before.log`, `ps_after.log`, their stderr files, own-niceness probe output, `process_clearance.json`, and `command.json`. The command record includes exact suite argv/cwd/interpreter/UID/own niceness, source hashes and preserved source bytes, including generated fixture scripts; the interpreter binary is hashed. Standard library code is supplied by that pinned interpreter. Refusals record NOT RUN rather than PASS. No full run of this wrapper was possible in this sandbox. Its syntax was checked; native launcher serialization and early failure paths were exercised by the four fixture prechecks below. Host niceness/process observation, actual worker capture, SIGINT/reap and full-wrapper behavior remain NOT RUN here.

## Evidence

| Artifact directory | Command suffix passed to `record_test_run.py` | Actual result |
|---|---|---|
| `sandbox_red_pure` | `<dir> <worktree> red --pure` | 14 tests, 14 expected absence failures, exit 1, before either implementation existed |
| `sandbox_green_pure_01` | `<dir> <worktree> green --pure` | 14/14 PASS, exit 0 |
| `sandbox_green_prechecks_01` | `<dir> <worktree> green --prechecks` | 4/4 PASS, exit 0; reused auth, wrong HEAD, dirty pinned path, bad hash |
| `sandbox_red_c1` | `<dir> <worktree> red --pure` | 15 tests, 1 failing new C1 regression, exit 1; no source rollback |
| `sandbox_green_pure_final` | `<dir> <worktree> green --pure` | 15/15 PASS, exit 0, with the final three source hashes |

Each listed log has its own `command.json` and source snapshots. The exact base command was `LLMDB_ROOT=$PWD /usr/bin/python3 -B results/mathlab_staging/new1_recorder_build_20261010T225651Z/record_test_run.py`; expanded suite commands and cwd are in those command records. The C1 regression demonstrated that PASS plus no worker observation previously produced COMPLETE; it now produces INCOMPLETE/no prediction verdict and blocks compute. The reviewer has not re-reviewed that fix. The fresh same-family read-only review is secondary input, not Astra acceptance.

The initial blocked probe is preserved in `process_clearance.json` at this receipt root. Sandbox runs intentionally have no host process-clearance claim; their individual `process_clearance.json` identifies snapshots as not taken. Direct partial checks are distinct from the full niceness-gated runner. No numeric host niceness was measured by this session.

## T1–T11 status

There are 34 planned full-suite tests: 15 pure and 19 dispatch tests. Every full process-dependent RED/GREEN run remains NOT RUN pending the above operator commands. The partial statuses below do not substitute for that acceptance.

| Criterion | Full dispatch test names | RED here | GREEN here |
|---|---|---|---|
| T1 recorder not a compute blocker | `test_T1_observed_recorder_line_not_blocker`; pure `test_T1_shell_argv_is_not_a_compute_executable` | Pure absence failure; actual line NOT RUN | Pure classifier PASS; actual process line NOT RUN |
| T2 PID, worker nice10/group, namespace, clean COMPLETE | `test_T2_happy_path` | NOT RUN | NOT RUN |
| T3 each precheck refusal b–i | `test_T3_b_reused_authorization`, `test_T3_c_wrong_head`, `test_T3_c_dirty_pinned_source`, `test_T3_d_bad_manifest_hash`, `test_T3_f_stricter_disk_floor`, `test_T3_g_fingerprint_failure`, `test_T3_h_dry_probe_refusal`, `test_T3_i_hash_changed_after_first_check`; 2e is T4 | NOT RUN | b/c/c/d PASS; e–i NOT RUN |
| T4 recorder nice1 refusal | `test_T4_nonzero_recorder_niceness` | NOT RUN | NOT RUN |
| T5 nice3 worker requests supervisor SIGINT | `test_T5_worker_nice_three_requests_supervisor_sigint` | NOT RUN | NOT RUN |
| T6 deadline stderr without halted | `test_T6_deadline_no_halted_event`; pure `test_T6_deadline_stderr_without_halt_counts_abort` | Pure absence failure; dispatch NOT RUN | Pure classifier PASS; dispatch NOT RUN |
| T7 resource halted abort | `test_T7_resource_halted_event`; pure `test_T7_resource_halt_counts_abort` | Pure absence failure; dispatch NOT RUN | Pure classifier PASS; dispatch NOT RUN |
| T8 internal admission refusal consumes authorization | `test_T8_internal_admission_refused`; pure `test_T8_admission_refusal_not_abort` | Pure absence failure; dispatch NOT RUN | Pure classification PASS; consumption/process case NOT RUN |
| T9 two prior resource halts plus deadline reaches 3 | `test_T9_third_abort_reached`; pure history union/deadline receipt tests | Pure history absence failures; total-3 dispatch NOT RUN | Pure history union PASS; total-3 dispatch NOT RUN |
| T10 surviving worker group blocks compute | `test_T10_unreaped_group_blocks_compute` | NOT RUN | NOT RUN |
| T11 exact endorsed argv/cwd/env | `test_T11_endorsed_argv_cwd_env` | NOT RUN | NOT RUN |

Additional pure cases cover missing terminal, missing/mismatched exit, invalid events, unmatched finishing, namespace anomaly, stdout abort code, and missing C1 observation. `test_disk_floor_cannot_be_lowered` is NOT RUN. No model, torch, GPU, or MPS was imported or run by these checks.

## Supervisor contract: verified current source

| Behavior relied on | Authoritative file:line |
|---|---|
| Main exclusively creates its timestamped namespace. | `tools/new1_supervisor.py:638–639` |
| Main requests a niceness increment of 10, calls supervise once, prints the outcome, and returns 0 for PASS or 3 otherwise. | `tools/new1_supervisor.py:640–648` |
| Admission is inside the run; refusal raises INVALID-ADMISSION before spawning. | `tools/new1_supervisor.py:509–519,642–645` |
| Worker launch starts a new session/process group. | `tools/new1_supervisor.py:522–533`, especially `532` |
| Retry policy counts only qualifying halted records, once per other namespace; >=3 triggers operator stop. | `tools/new1_supervisor.py:168–190`, especially `185–190` |
| SIGINT handling across construction is deferred for callable handlers; reaping masks SIGINT/SIGALRM. | `tools/new1_supervisor.py:280–310,313–323` |
| Python's default SIGINT raises KeyboardInterrupt; supervisor BaseException routing unwinds the independently bounded worker lifetime, attempts halt recording, and re-raises interrupts. This is why the recorder signals only the supervisor PID. | Python language signal behavior plus `tools/new1_supervisor.py:443–487,597–627` |
| Supervisor itself owns group signalling and direct-worker wait; failed reaping is reported. The recorder does not claim those operations always succeed. | `tools/new1_supervisor.py:330–352,458–486` |
| Deadline can raise STOPPED-DEADLINE while expired remaining time prevents halted publication and causes stderr diagnostics. | `tools/new1_supervisor.py:106–114,612–627`, especially `617–623` |
| Completed execution publishes run_finished; halted execution attempts halted. | `tools/new1_supervisor.py:592–596,618–621` |
| Terminal event types and provisional finishing; canonical NEW1 fold suppresses predictions unless PASS finished and no halt exists. | `tools/mathlab_events.py:56–58,278–303`, especially `294–303` |
| Admission scanner excludes only its own PID plus exact exemptions; Python executable names are compute blockers, and failed/empty process inventory refuses. | `tools/c10w_p2_gate.py:22–40,43–54,73–84`; admission use at `tools/mathlab_admit.py:69–73` |

Astra's C1/C3/C2 and endorsed command are `results/mathlab_staging/new1_launch_readiness_astra.md:23–29,55–89,119–126`. Its source pins matched this session's protected files.

## Open findings

These remain intentionally unfixed under MAESTRO27's context instruction. Resolve them before treating the recorder as accepted for the real sole invocation. They are static findings, not observed host failures.

1. **P1: INCOMPLETE can still return exit 0.** `tools/new1_dispatch_report.py:195–196` returns 0 whenever compute is unblocked; `tools/new1_dispatch.sh:305–307` then returns the supervisor's 0. A complete C1 observation with missing terminal or namespace ambiguity can therefore return shell success despite an INCOMPLETE receipt. Next fix/test: return nonzero for INCOMPLETE and exercise reporter main with missing terminal/ambiguous namespace.
2. **P1: malformed/nonzero supervisor niceness is not stopped promptly.** `tools/new1_dispatch.sh:234–240` only requests SIGINT for a failed ps exit; exit-zero empty/malformed/nonzero output is recorded as null/a number and allowed to continue. The final C1 check at `tools/new1_dispatch_report.py:146–166` prevents accepting a PASS, but does not supply immediate stop. Next fix/test: require actual observed supervisor nice0 while alive; test numeric mismatch and empty output.
3. **P2: timeout receipt is incompatible with abort-history schema.** `tools/new1_dispatch.sh:264–268` writes a minimal consumed/operator-required receipt lacking namespace and abort_accounting. `tools/new1_dispatch_report.py:94–112` treats it as a history error and does not recover resource/deadline evidence from its logs. Next fix/test: compatible provisional schema or post-exit reconciliation; test exact timeout shape with deadline stderr and deduplication.
4. **P2: earlier stdout abort evidence can be lost.** `tools/new1_dispatch_report.py:21–30` checks only the final stdout code for abort accounting. A STOPPED-RESOURCE line followed by other output is lost without stderr/halted evidence. Next fix/test: scan all stdout for abort names while keeping final-code reconciliation separate.
5. **P2: conflicting terminal history can disagree with canonical fold.** `tools/new1_dispatch_report.py:24–41` accepts a last run_finished(PASS) following halted(INVALID-WORKER), while `tools/mathlab_events.py:294–303` suppresses predictions whenever a halt exists. Next fix/test: reject conflicting history or consult canonical fold, using that exact event sequence.
6. **Fixture emergency-cleanup gap.** `tests/test_new1_dispatch.py:341–350` kills leaked supervisor/worker PIDs but only waits for the dispatcher afterward. It correctly fails the test, but does not prove the other killed PIDs exited before the test ends. Normal T10 release waits for disappearance at `339–340`; emergency cleanup needs the same post-kill observation while retaining failure.

Fixed finding: PASS without actual worker observation previously passed; regression RED and final 15/15 pure GREEN document the C1 patch at `tools/new1_dispatch_report.py:146–166`. Tuple and supervisor-niceness checks are in that patch; only the no-observation regression has been run.

## Final SHA-256 and protected scope

```text
6fd2876f4a29d1fe3feeb69cf461d07196c5115262845bcb76d620eac67912e5  tools/new1_dispatch.sh
955079238e533b6609d5c98454155b83adeac1ce0b9e3070e0da91f4f0c005fe  tools/new1_dispatch_report.py
3ee259d78047b44af89b108ea854ad19f37fca672535209f547eb380171e7ad7  tests/test_new1_dispatch.py
```

`final_sources.sha256` also pins the runner and provenance helper. Initial/current observed HEAD was `9f971796eb12e98ccdcd0703eaa69cb0a9d75f0c`. The nine protected source/prereg hashes passed recheck after implementation. `protected_before.sha256` and `protected_after_check.log` preserve the comparison; final checks are in `protected_final_check.log`. Concurrent unrelated changes, including MB34's named paths and `tools/test_dashboard_mathlab.py`, were left untouched. No canonical documents or existing implementation files were changed.

The first engine hash scan encountered symlinks and is preserved in `engine_initial_hash_failure.log`/`engine_before.sha256`. The corrected manifest hashes 131 regular files and separately records 12 symlink targets (143 tracked entries). Final checks compare all regular hashes and target strings. Symlink target content is outside this tracked-entry check; this task never edited the engine. Receipt artifacts are small; no bulk writes. Initial volume observation was 84,078,184 KiB free; no launch-time disk clearance is claimed.

## Context handoff

MAESTRO reported ~49% context and directed finishing the active C1 edit, stopping further hardening, and handing off for fixture runs. Done: all three source files and runner exist; 15 final pure tests and four early refusal fixtures passed; source pins checked; six findings documented. Half-applied edits: none. In-flight processes: none owned by this task. The full suite, worker niceness, actual process inventory, SIGINT behavior, reap/disposition, and runner's niceness-zero host execution are NOT RUN here. Exact changed paths/hashes are above and in `final_sources.sha256`; no known sandbox test is currently failing. Earlier expected RED failures and exact commands/source hashes are in their command.json files.

Next step: MAESTRO runs the two commands above from the separate niceness-0 shell, examines logs/provenance/clearance, and routes failures and Open findings into a fresh fix session. Do not invoke the real supervisor/geometry in the build tests. Preserve the one-use authorization and protected bytes.

Binding context directive: watch `Context N% left`; start a new piece of work only at >=60% left. At <=40% left or any `Context compacted`, stop starting work and immediately write a handoff at the end of this README with completed/in-flight work, exact changed paths/SHA-256, failing tests and exact commands, next step and risks; reply exactly `CONTEXT HANDOFF WRITTEN`. Every successor and every team session must preserve this directive through handoffs.
