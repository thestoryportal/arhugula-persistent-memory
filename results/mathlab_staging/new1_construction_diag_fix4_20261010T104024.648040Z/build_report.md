# NEW1 FIX4 — MB17 build report

**NEW1 FIX4 STOPPED — sandbox repeatability acceptance failed.** Six new regressions have behavioral RED→GREEN evidence; all 182 existing methods remain. The corrected stalled-launch test passed **20/20 consecutive fresh-process solo runs**. The first required full-suite run completed **188 methods: 182 passed, 6 failed**, exit **1**, with a ResourceWarning. The driver stopped; required full runs 2–3 were not restarted or replaced. This candidate is not accepted and has no launch approval.

MAESTRO11 verifies and commits; GPT-6-Astra reviews. No commit, push, merge, real diagnostic, model/GPU launch, real admission, real numerical input read/rehash or repository artifact deletion was performed. The diagnostic authorization remains unchanged. Receipt budget: 8 MiB; initial free space was **86,346,117,120 bytes**, exceeding that budget plus 20 GiB. Current receipt byte accounting and the final inventory are in `release_manifest.json`.

## Abrupt-exit attribution before implementation (criterion 3)

`observe_abrupt.py` ran the unchanged failing solo schedule from an external process, preserving actual `os._exit` calls. It captured an occurrence on **attempt 1**, below the 200-attempt stop limit. `capture_001.log`, `capture_001.jsonl` and `capture_index.json` preserve exit status 2, absent unittest completion, PID/role, caller stacks, exception history, original deadline remaining and owned PID/proof/descriptor state. Lifecycle source remained SHA **14329bd0daa00bb109010464c26988b5014c6b6e9b92e39152028a9af7033cbe** throughout capture and deterministic replay.

| Role / PID | Observed cause and exit site | Ownership / deadline observation |
|---|---|---|
| Guardian **85274**, owned worker **85275** | `PermissionError(1, 'Operation not permitted')` at old `kill_worker:279`, propagated through `watchdog:340/346` and `OwnedWorker.start:381` into the inherited supervisor. Both inherited cleanup attempts then raised `OSError(9, 'Bad file descriptor')`. Actual `_exit(2)` caller: old `supervise:612`. | Guardian's inherited owner had guardian PID 0, no worker/proof and partly closed channels. Approximately **0.7415 s** remained. This PID was the guardian, not the actual parent. |
| Actual parent **85239** | Primary `STOPPED-LAUNCH: worker creation/registration exceeded launch bound`. Both cleanup attempts raised `INVALID-CLEANUP: guardian exit lacks worker reaping proof`. Actual `_exit(2)` caller: old `supervise:612`. | Guardian exit 2 had been collected; worker PID 85275 was registered, worker proof absent, owned descriptor slots all closed, no streams remained. Approximately **0.7400 s** remained. |

This attributes the newly captured occurrence only. Historical MB15 runs 06 and 18 remain unattributed. The captured trace does not supply the worker's historical exit status or establish why group signalling returned EPERM; no such claim is made.

`deterministic_before/trace.jsonl`, `red.log` and `receipt.json` then forced the captured guardian group-signalling refusal in the same stalled-launch fixture with unchanged lifecycle source. Both guardian and actual parent again reached old `supervise:612`, without unittest completion. Before implementation, the dedicated criterion-3 regression in `red_c3_deterministic/` reproduced that chain with a controlled live pre-release worker. These saved schedules precede the lifecycle edit. Instrumentation logs exceptions and exit callers but invokes the real native exit, without converting it into a return or exception.

## Change and scope

- `kill_worker` now falls back from ProcessLookupError or PermissionError on group signalling to SIGKILL of the already-owned PID. A refused direct PID signal still raises; signal return alone never proves reaping. Kill attempts retain the guardian's actual wait status.
- Guardian signal/session setup now executes inside its existing protected lifecycle, so a setup failure can report the true no-worker-created failure. The raw-fork child branch has an unconditional `_exit(2)` boundary around `watchdog`; setup/final-send exceptions or a returning guardian cannot unwind into inherited supervisor/unittest code.
- The stalled-launch test retains STOPPED-LAUNCH, the **.3 s** bound, **.05 s** launch/cleanup fixture bounds and absent arithmetic marker. The overstrict kills==1 assertion is replaced with worker-proof identity, real guardian/worker OS checks and stream/descriptor closure before fixture teardown. Controlled schedules separately assert (0,2), (1,-9) and (1,2), with no global biconditional.
- The external regression fixture records ownership immediately after the real supervisor returns and before result-file reads or fixture teardown. It counts successful real worker/guardian waitpid collections, probes worker absence, verifies guardian waitpid is already consumed and checks all owned descriptors/streams closed. Exit-between-wait-and-kill uses native waitid(WNOWAIT) only to observe a real exited worker without consuming its waitpid status. Fixture workers are bounded synthetic processes and never reach real arithmetic.
- Construction source and its existing pin test receive the necessary identity-source SHA update. The scope receives an additive **Scope revision — FIX4**, followed by an explicit verification-stop appendix; the initial **107,748 bytes** remain an exact prefix. The tested pre-stop scope SHA is **4e33c59495837e1f6753985cda27d7ef79a51f1e4b2f5724f0396146f754b8c8**. The final scope SHA below adds stop documentation only.

`supervise` is byte-identical to entry, including all three emergency exit bodies, the existing bounded cleanup fallback, timer handling and terminal error recording. No emergency exit was deleted or softened; no retries or caps were added/increased. All other identity functions/class methods are byte-identical except kill_worker/watchdog/OwnedWorker.start. Construction source differs only by its necessary identity pin. Scientific functions, inputs, projector gate, scalar output schema, four constructions and authorization remain unchanged.

## Per-criterion behavioral evidence

All six individual REDs completed a unittest method and failed behaviorally before the implementing change. PID-tagged external records are saved alongside each log. The dedicated C3 deterministic RED additionally proves the captured trigger independent of the removed kill assertion.

| New method | RED | GREEN |
|---|---|---|
| `test_fix4_c1_already_exited_is_reaped_without_a_signal_before_return` | `red_fix4/001.log` — Legacy kills==1 assertion failed with legitimate kills 0/code 2. | `green_fix4/001.log` — (0,2); real worker/guardian reaped once; OS absence and closure at supervisor return. |
| `test_fix4_c1_live_worker_is_killed_and_reaped_before_return` | `red_fix4/002.log` — Forced captured group refusal caused guardian escape and parent native exit 2. | `green_fix4/002.log` — (1,-9); worker observed live before guardian termination; ownership closed before return. |
| `test_fix4_c1_exit_between_wait_and_kill_retains_actual_exit_status` | `red_fix4/003.log` — After WNOHANG observed live, WNOWAIT observed worker exit; group refusal escaped. | `green_fix4/003.log` — (1,2); actual exited status retained after a real attempted termination; one real reap per PID. |
| `test_fix4_c2_guardian_setup_exception_cannot_unwind_into_supervisor` | `red_fix4/004.log` — Setup exception reached PID-tagged inherited-supervisor sentinels. | `green_fix4/004.log` — Guardian native exit 2 inside child lifecycle; explicit no-worker failure proof; parent failure return. |
| `test_fix4_c2_final_send_exception_retains_reaping_and_child_boundary` | `red_fix4/005.log` — Final receipt send exception reached inherited-supervisor sentinels. | `green_fix4/005.log` — Actual worker reaped once before send failure; child remains contained; parent missing-proof fail-stop 2. |
| `test_fix4_c3_captured_exit_schedule_returns_but_true_failures_fail_stop` | `red_fix4/006.log` — Dedicated deterministic RED retained parent supervise:612 after signalling refusal. | `green_fix4/006.log` — Ordinary STOPPED-LAUNCH returns with ownership and unittest completion; genuine proof/output failures retain native fail-stops. |

The C3 GREEN contains separate externally observed missing-reaping-proof and terminal-output/stderr failures. Each preserves native parent exit **2**, a captured emergency exit caller and exception/deadline evidence, no successful ownership return and no unittest completion. C2's final-send GREEN demonstrates actual worker reaping before the receipt fails and no child escape into the inherited supervisor. Successful ordinary cleanup remains externally distinguishable by a Python return, complete ownership snapshot and completed unittest.

Two harness issues are retained and excluded from behavioral RED or acceptance evidence: an f-string parse failure before any tests executed, corrected before RED capture, and `green_fix4_first/001.log`, which mistakenly classified signal-0 OS ownership probes as termination attempts. The observer event label was corrected; production did not change for that failure. `red_fix4/index.json` initially flagged the text `error::ResourceWarning` in failed assertion metadata as a warning. Its original bytes remain preserved; the audit rescanned actual warning lines and found no ResourceWarning in those six REDs. The required full-run warning below is real and disqualifying.

## Acceptance results and unresolved failure

Method inventory: **66 construction + 27 identity + 34 geometry + 61 supervisor = 188**. All **182 entry methods** remain; **180 are byte-identical**, with only the named stalled-launch assertion and identity pin test changed. No identity/geometry/supervisor test source was edited. New methods: 3 criterion 1, 2 criterion 2, 1 criterion 3.

`sandbox_solo_20/index.json` binds all 20 saved solo logs, source/test hashes, command, exit status, complete one-test results and warning scans. Every run exited 0 and completed OK. No selective restart occurred.

`sandbox_full_3/001.log` / `index.json` record the first required full command, **Ran 188 tests in 34.615 s / FAILED (failures=6)**, native exit 1, approximately **34.800 s** wall time. The six failures were:

- `tests.test_new1_supervisor.SupervisorTests.test_blocked_halt_persistence_cannot_extend_total_deadline`
- `tests.test_new1_supervisor.SupervisorTests.test_blocking_admission_is_interrupted_by_whole_run_deadline`
- `tests.test_new1_supervisor.SupervisorTests.test_cell_alarm_interrupts_blocked_persistence_inside_total_cap`
- `tests.test_new1_supervisor.SupervisorTests.test_supervisor_cell_deadline_interrupts_a_blocked_resource_probe`
- `tests.test_new1_supervisor.SupervisorTests.test_watchdog_enforces_during_blocked_persistence`
- `tests.test_new1_supervisor.SupervisorTests.test_watchdog_refuses_memory_drop_during_blocking_admission`

Observed mismatches include elapsed **2.0103 s versus <.3 s**, **1.0123 s versus <.2 s**, **.2811 s versus <.2 s**, INVALID-ADMISSION instead of STOPPED-DEADLINE, STOPPED-DEADLINE instead of STOPPED-RESOURCE, and INVALID-WORKER instead of STOPPED-RESOURCE. The log also reports `ResourceWarning: subprocess 25689 is still running` from Popen.__del__. All six new FIX4 methods passed within that run, but full-suite acceptance failed.

The failing deadline fixture passed in a separate fresh-process solo control (`supervisor_solo_control.log/json`). A diagnostic-only run of the complete sequence under `observe_suite_state.py` reported **188 passing methods** (`suite_state.log`, `suite_state_result.json`). Its **376 before/after samples** (`suite_state.json`) recorded empty main-thread signal masks, default SIGALRM handlers and inactive timers. That observation rules out a persistent main-thread mask/handler/timer leak at those boundaries, not all possible interference. The timing/signal mechanism remains unresolved. Protected source/test hashes remained identical; this does not establish whether the first failure predates FIX4 or is caused by the candidate.

The diagnostic PASS does not replace the failed required run. Required full runs 2–3 remain **UNRUN** after the fail-stop, and the accepted required full-run count is **0/3**. Discarding the failed run or starting a fresh success count on the same unchanged candidate would violate the no-selective-restart contract. No unrelated protected-file fix or cap relaxation was attempted. MB17 therefore stops without a DONE claim.

The exact failing full command was:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest tests.test_new1_construction_diag tests.test_new1_identity_diag tests.test_new1_geometry tests.test_new1_supervisor -v
```

The exact corrected solo command was:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once -v
```

## Static audit, receipts and pins

`audit_release.py`, `audit_release.log/json` and `audit_command.json` report **STATIC-PASS / ACCEPTANCE-FAIL**, exit **1**. The auditor retains the failure gate; it does not relabel the failed repetition as PASS. It verifies the allowed lifecycle diff, byte-identical supervisor/Output/scientific/helper bodies, constant/source/input assignments, construction-only pin change, all existing methods, scope prefix, current source pins and historical source, protected files, prior receipts, REDs/GREENs, every repetition log/hash and the exact unexecuted launch command. It imports no torch/numpy/transformers/safetensors, runs no admission and reads no numerical input.

**19 protected files** and **181 pre-existing receipt files** match entry hashes. This includes dashboard, Drive-backup and launchd exclusions as inventoried in baseline.json. Concurrent unrelated work was preserved. A scoped diff against MB17's actual entry snapshots is saved in `mb17_changed.diff`; the broader git HEAD diff contains prior builders' work and is not MB17's change inventory.

| Changed existing file | Final SHA-256 |
|---|---|
| `tools/new1_identity_diag.py` | `1161503c55346fb5d47bbed462ec3de3b17698b0b94752dfef4d7bf4d0e2ff8a` |
| `tools/new1_construction_diag.py` | `b1db5aa9ab2d6914c3f4b3601f0164a9c78686c443ebdaa3445f9ea9d0d391a4` |
| `tests/test_new1_construction_diag.py` | `c80e08c5b36ffb9e5c83a2a47d9fdf28b223fb9e7e5d47a003893b681cbf69d4` |
| `results/mathlab_staging/new1_construction_diag_scope.md` | `77f3086cac50de8ba5896e5d7e4e4d5a3661ec43d136fa8c1a2cab53d1f8c607` |

`release_manifest.json` binds these hashes, the unchanged protected inventory, current source/input pin dictionaries, audit/acceptance states and SHA-256/byte counts of every fresh receipt except itself. Before hashes/copies are in `baseline.json` and `before_*`. New receipts were absent at entry. `launch_command.txt` is generated from the unchanged source launch-command function with the final scope and construction-source hashes, read back exactly and **not executed**. It is a review artifact, not launch approval. The nice increment, environment, source/input checks, namespace, output contract and authorization remain the existing launch contract.

## Exact MAESTRO host repetition commands — UNRUN

Run from the branch worktree only after review of this stopped candidate. The recorder creates fresh directories, invokes the exact fresh-process unittest commands with -B, PYTHONDONTWRITEBYTECODE=1 and -W error::ResourceWarning, preserves every log/status/source hash, rejects incomplete counts/warnings/timeouts/ignored exceptions and stops on the first failure. Existing directory reuse refuses; no selective restarting is authorized.

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/run_checks.py solo --count 100 --label host_solo_100
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/run_checks.py full --count 10 --label host_full_10

```

These commands request **100 solo + 10 full-suite** host runs. None were run by MB17. Sandbox and host repetition are practical thresholds, not proofs of non-flakiness; deterministic schedule coverage remains essential.

## Handoff to MAESTRO11 / Astra

Completed: criterion-3 capture and deterministic unchanged-source replay; six numbered RED→GREEN regressions; minimal lifecycle containment/signalling correction; immediate ownership checks; all 182 existing methods retained; scope prefix and protected/prior receipts preserved; 20 consecutive solo pre-checks; all evidence, audit, final pins and unexecuted launch command refreshed. No source edit is half-applied.

Open: first required full-suite run failed six existing deadline/resource methods and emitted a ResourceWarning. The diagnostic-only full PASS does not clear that failure. Further required sandbox repetitions, host 100/10 repetition and binding Astra acceptance remain unestablished. No real scientific/GPU/model/admission work or commit/merge is permitted by this packet.

Exact changed paths and SHA-256 values are the table above and release_manifest.json. The exact failing command and six method IDs are above; saved failure evidence is `sandbox_full_3/001.log`. Next step: MAESTRO11/Astra review that failure and the signal-state controls, determine the minimal authorized investigation/fix if one is necessary, then qualify an explicitly reviewed candidate with all failures retained. Do not overwrite or read around the failed batch or treat the written launch command as approval.

**Binding context directive, restated:** watch Context N% left. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a handoff at the end of build_report.md with completed/half-applied work, exact changed paths and SHA-256 values, failing tests/exact commands and next step, then reply **CONTEXT HANDOFF WRITTEN**. If context is compacted, do so immediately. Restate this directive in every handoff.
