**INVESTIGATE. FIX4’s lifecycle correction stands provisionally; this candidate is not accepted for host qualification or the real diagnostic.**

Read-only review: all seven supplied hashes match and remained unchanged. Current HEAD is `4227e2c`, the r4-packet commit; the two supervisor files remain unchanged relative to `70a66c8`. No tests or diagnostic were launched.

**1. FIX4 satisfies the identified lifecycle correction.**

- **EPERM fallback:** `kill_worker` now attempts SIGKILL on the owned PID after either group-not-found or group-permission failure. Direct PermissionError still propagates; successful signalling does not substitute for `waitpid`. This addresses the captured trigger without inventing cleanup success (`tools/new1_identity_diag.py:278–283,294–297,346–353`).
- **Fork containment:** setup is inside the guardian’s protected lifecycle, and the raw-fork branch has an unconditional native-exit boundary. Setup or final-send exceptions cannot unwind into inherited supervisor/unittest code (`tools/new1_identity_diag.py:298–303,343–354,380–383`).
- **Stalled-launch assertions:** STOPPED-LAUNCH, `.3 s`, no arithmetic, guardian collection, worker absence, and descriptor/stream closure remain enforced. The external schedules additionally check ownership immediately after supervision returns and distinguish `(0,2)`, `(1,-9)`, and `(1,2)` correctly (`tests/test_new1_construction_diag.py:520–535,1167–1172,1211–1245`).

I found **no new defect in those three changes**. Their limit remains explicit: if direct signalling also fails, or the reaping receipt is lost, successful cleanup is unproven. The actual diagnostic parent can still fail-stop at `tools/new1_identity_diag.py:608–614`; the real entry calls that supervisor at `tools/new1_construction_diag.py:239–240`. This is not ordinary successful cleanup and must remain distinguishable.

**2. The six failures are not attributable to FIX4 yet. There are concrete interference paths to investigate.**

There is **no direct call path** from `new1_supervisor.supervise` into the changed identity lifecycle. The new observer’s un-restored monkeypatches and tracing execute in a separate subprocess, which `subprocess.run` collects (`tests/test_new1_construction_diag.py:1176–1179,1195–1202`). Guardian signal/session changes occur after fork; the parent’s mask restoration remains unchanged (`tools/new1_identity_diag.py:374–391`). I found no FIX4 installation of a parent SIGCHLD handler or new parent thread.

That does **not** establish absence of indirect interference:

- **A concrete unreaped-child path exists in the unchanged supervisor.** After signalling the worker, cleanup evaluates `controller.remaining()` **before** entering the block containing `process.wait()`. An exhausted deadline therefore skips collection and returns through the closeout-error handler (`tools/new1_supervisor.py:411–428`). This fits the late warning, though PID **25689’s creation site is not established** by that log.
- **The warning does not prove the process was still executing.** This interpreter’s `Popen.__del__` warns when cached `returncode is None`, before polling. With warnings promoted to errors, that warning can interrupt the destructor before its subsequent poll (`…/cpython-3.11.16-macos-aarch64-none/lib/python3.11/subprocess.py:1120–1133`). It proves missing collection/status knowledge, not a surviving process group.
- **That late warning cannot explain the earlier failures by itself.** The blocked-halt and blocked-admission failures occur first and need no dispatched worker. Their fixtures inject two-second sleeps; the cell-persistence fixture injects one second (`tests/test_new1_supervisor.py:285–294,118–129,671–686`). The observed near-full sleeps warrant investigating ineffective or delayed alarm handling, not merely a small timing-margin miss.
- **Shared-process numerical initialization is a plausible confound.** Earlier suites import torch and set its thread count in the unittest parent (`tests/test_new1_construction_diag.py:19–24`; `tests/test_new1_identity_diag.py:18–25`). Native-thread state and signal delivery are hypotheses to test, not established causes.
- **Boundary snapshots are insufficient.** The observer records only the calling thread’s mask, Python SIGALRM handler, and timer at test boundaries—and writes JSON at every boundary. Its passing run cannot establish the failing run’s state, in-test delivery, native-thread state, or absence of child/fd residue (`R/observe_suite_state.py:14–24`).

Here, `R` is `results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/`.

**3. Minimal investigation authorized for the builder, in order**

1. **Capture provenance and failure state without changing candidate code.**  
   Use fresh scratch/receipt namespaces. Record loaded module paths/hashes, interpreter, environment, test order, and PID creation/collection. Observe alarm arm/fire times and pending signals around the six failing fixtures; record owned children/groups, descriptors, and native-thread state. Capture state **before** any fixture cleanup. Preserve real signal/exit behavior.  
   **PASS reading:** a failure has attributable alarm and ownership evidence. **FAIL/inconclusive:** another clean run with boundary snapshots alone. Do not count investigative passes toward acceptance.

2. **Run the pre-FIX4 four-suite baseline in scratch.**  
   **Yes:** restore the saved source, construction-test, and scope copies into a separate scratch tree, retaining the unchanged dependency/test files. Verify imports resolve there; never restore over the candidate. Expect **182**, not 188, methods.  
   Run **one initially; at most three fresh-process attempts**, stopping when a target supervisor failure is reproduced. If an old lifecycle abrupt exit prevents reaching the supervisor suite, stop and record that baseline as censored; use the isolated controls below rather than skipping the offending test.  
   **PASS-for-attribution:** the same supervisor symptom on pre-FIX4 proves FIX4 is unnecessary for that symptom. **FAIL/inconclusive:** three clean runs do not prove absence of a pre-existing intermittent failure. A baseline failure alone does not exonerate every FIX4 interaction.

3. **Separate process-state effects from lifecycle effects.**  
   In fresh processes, compare the supervisor suite alone with the same suite after the preceding numerical initialization, then after the FIX4 lifecycle fixtures. Start with one run per condition; use at most three per unresolved comparison, preserving every result. Add a bounded synthetic check of the **actual construction parent’s** blocked-preflight/monitor/cleanup path under the implicated condition.  
   **PASS-for-isolation:** a specific test-parent state explains the failure, ownership is clean, and the production-shaped parent passes the corresponding control. **FAIL:** leaked ownership, failed deadlines, or missing proof on the production-shaped path requires a production fix and r5 review. No cap increases, warning suppression, or outcome relaxation.

4. **Return for r5 with the mechanism and proposed qualification plan.**  
   A test-only cleanup or process-isolation change is acceptable **only after step 3 establishes why it is correct**. Cleanup must not repair ownership before assertions inspect it. Running supervisor tests separately merely to obtain green would hide the question.  
   **PASS reading:** a reproducible distinction supports a narrowly scoped correction. **FAIL/inconclusive:** retain STOPPED status; do not launch the host repetition batch.

Sandbox load/scheduling is **plausible, not established**. The 34.6-versus-15.4-second totals are not independent load measurements; full-length injected sleeps themselves contribute to the difference. A controlled sandbox/host comparison could support an environment-specific explanation, but host success alone cannot retrospectively identify the cause. No host repetitions are authorized by this ruling.

**4. Acceptance from here**

The failed run remains permanently recorded as a **failed acceptance attempt; the existing batch remains 0/3**. It cannot become run 1 of a later successful sequence (`R/build_report.md:53–66`; `new1_construction_diag_scope.md:550–556`).

The production bytes are **not permanently disqualified merely because this batch failed**. A demonstrated pre-existing harness/environment problem can justify retaining them, but requires r5 approval of a materially justified qualification revision—not a cosmetic hash change or “baseline failed too.” Any correction must then complete a **fresh 3/3 full sandbox batch** under the approved arrangement.

The host bar remains **100 consecutive fresh-process solo runs plus 10 consecutive fresh-process full four-suite runs**, using `R/run_checks.py`, stopping on the first failure, with complete counts, no ResourceWarnings/ignored exceptions, no abrupt exits/timeouts, and no cleanup leakage (`R/run_checks.py:38–64`; `new1_construction_diag_astra_r3.md:49–51`). Any proposed suite isolation changes that runner’s contract and must be reviewed at r5 first. Host qualification is still separate from real-run approval.

🌱 graft reported approximately 25,924 tokens saved; one successful call and one failed probe.

VERDICT: INVESTIGATE

