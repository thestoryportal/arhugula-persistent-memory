# GPT-6-Astra (high) — scope ruling r4: NEW-1 four-construction diagnostic, FIX4 STOPPED

Read-only. Worktree = current dir. Your r3 verdict (FIX4 contract) is `results/mathlab_staging/new1_construction_diag_astra_r3.md`. The operator authorized exactly one real run (`results/mathlab_staging/new1_construction_diag_authorization.md`); a defect found after launch costs it. Nothing launches until you rule, and a host repetition batch runs only on a candidate you accept.

## Candidate (uncommitted; `git diff` shows the change vs HEAD 70a66c8; all five hashes match `release_manifest.json`)
tools/new1_construction_diag.py b1db5aa9ab2d6914c3f4b3601f0164a9c78686c443ebdaa3445f9ea9d0d391a4
tools/new1_identity_diag.py 1161503c55346fb5d47bbed462ec3de3b17698b0b94752dfef4d7bf4d0e2ff8a
tests/test_new1_construction_diag.py c80e08c5b36ffb9e5c83a2a47d9fdf28b223fb9e7e5d47a003893b681cbf69d4
tests/test_new1_identity_diag.py 7a9a6d3b74fe600cb4784c5711cde6fc6c373e11743ab7538d8afc86e155c6b1
results/mathlab_staging/new1_construction_diag_scope.md 77f3086cac50de8ba5896e5d7e4e4d5a3661ec43d136fa8c1a2cab53d1f8c607

Committed and **unchanged by FIX4** (the six failing tests exercise these):
tools/new1_supervisor.py a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b
tests/test_new1_supervisor.py 33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec

Pre-FIX4 copies: `before_*.py` in the receipt dir below.

## What happened
Receipt dir: `results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/` (R). Builder report: `R/build_report.md`. Read §"Abrupt-exit attribution", §"Change and scope" and §"Acceptance results and unresolved failure".
- **Attribution (your r3 finding 2).** The abrupt exit 2 was captured on attempt 1 (`R/capture_001.*`). A guardian's group signal got EPERM at old `kill_worker:279`. The error unwound through `watchdog` / `OwnedWorker.start` into the inherited supervisor, and both guardian and parent hit old `supervise:612` `_exit(2)`. It replayed deterministically on unchanged source (`R/deterministic_before/`, `R/red_c3_deterministic/`). Historical MB15 runs 06/18 remain unattributed.
- **FIX4 change.** `kill_worker` falls back from ProcessLookupError/PermissionError on the group signal to SIGKILL of the owned PID; a refused direct signal still raises. Guardian setup moved inside the protected lifecycle. The raw-fork child has an unconditional `_exit(2)` boundary around `watchdog`. The stalled-launch test drops kills==1 for worker-proof identity and OS/descriptor checks. `supervise` is byte-identical to entry. Six new tests went RED→GREEN, and 20/20 sandbox solo runs passed (`R/sandbox_solo_20/`).
- **The failure.** Required full run 1 of 3 (`R/sandbox_full_3/001.log`): `Ran 188 tests in 34.615 s / FAILED (failures=6)`, plus `ResourceWarning: subprocess 25689 is still running` from Popen.__del__. All six failures are existing `tests.test_new1_supervisor.SupervisorTests` deadline/resource tests:
  - `test_blocked_halt_persistence_cannot_extend_total_deadline`
  - `test_blocking_admission_is_interrupted_by_whole_run_deadline`
  - `test_cell_alarm_interrupts_blocked_persistence_inside_total_cap`
  - `test_supervisor_cell_deadline_interrupts_a_blocked_resource_probe`
  - `test_watchdog_enforces_during_blocked_persistence`
  - `test_watchdog_refuses_memory_drop_during_blocking_admission`

  Mismatches: elapsed 2.0103 s vs <.3 s, 1.0123 s vs <.2 s, .2811 s vs <.2 s; INVALID-ADMISSION instead of STOPPED-DEADLINE; STOPPED-DEADLINE instead of STOPPED-RESOURCE; INVALID-WORKER instead of STOPPED-RESOURCE. The builder fail-stopped; runs 2–3 were never started.
- **Controls (diagnostic only; they do not clear the failed run).** A fresh-process solo run of one failing test passed (`R/supervisor_solo_control.*`). A full run of the same sequence under `R/observe_suite_state.py` passed 188/188 in **15.368 s** (vs 34.6 s for the failing run) (`R/suite_state.*`). Its 376 before/after samples show empty main-thread signal masks, default SIGALRM handlers and inactive timers at every test boundary.
- **Unknown.** Whether this failure predates FIX4: the four suites were never run on the `before_*.py` code in the same sandbox.

## Rule on (cite file:line)
1. **Does FIX4's lifecycle change stand?** Check the EPERM→owned-PID SIGKILL fallback, the fork containment boundary and the replaced stalled-launch assertions against r3's contract. Name any defect, and say whether it could reach the real diagnostic parent.
2. **Can FIX4 cause the six supervisor failures?** Name any path from the changed `kill_worker` / `watchdog` / `OwnedWorker.start` / fork boundary (or their tests) into a later supervisor test's timing or outcome. Candidates include a leaked or un-reaped child (the ResourceWarning names one), an orphaned process group, SIGCHLD or alarm interplay, and fd or thread residue. Or say that no such path exists in the code.
3. **Minimal authorized investigation.** Name the smallest set of steps that settles cause, in order. Answer each:
   - (a) Must the four suites run on the pre-FIX4 code (`before_*.py` restored into a scratch copy, never over the candidate) to learn whether the failure predates FIX4? How many runs?
   - (b) Is a test-only or harness-isolation fix acceptable (e.g., running `tests.test_new1_supervisor` in its own process, or tightening child reaping in the FIX4 tests)? Or does it hide a real defect the diagnostic could hit?
   - (c) Are the failures plausibly sandbox load or scheduling (34.6 s vs 15.4 s wall)? Would host runs settle that, and what host result would?
4. **Acceptance from here.** Is the failed run 1 permanently charged against this candidate (new candidate + fresh 3/3 required)? Or can an investigation outcome (e.g., pre-FIX4 code fails identically) keep it? Restate the host bar (100 solo + 10 full via `R/run_checks.py`, stop on first failure, no selective restarts) or change it.

## Verdict
End with exactly one line:
- `VERDICT: INVESTIGATE`: run the investigation in item 3, then return for r5. Give it as numbered steps, each with a pass/fail reading.
- `VERDICT: FIX5`: give the contract as numbered, testable criteria, each with a RED.
- `VERDICT: HOST-QUALIFY`: the candidate stands; proceed to the host 100/10 batch.
- `VERDICT: NO-GO`: stop iterating; say why.
