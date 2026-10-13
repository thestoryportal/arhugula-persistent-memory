**FIX5 is warranted. The receipts establish enough mechanism to correct production mask handling; they do not identify the historical leaking instruction.** No additional investigation is required before that correction.

Read-only review completed. All five candidate hashes match; both supervisor hashes match the audited pins. Opening and closing hashes agree. No tests, diagnostics, edits, or launches were performed.

Below, `RECEIPT` and `R` mean the directories named in the request; `Audit` means `RECEIPT/investigation_report.md`, beginning at line 366.

**1. Mechanism ruling**

The production-parent mechanism is sufficiently established:

- Under imposed `[2,14]`, SIGALRM remains pending and fails to interrupt the injected blocking operation.
- Masked preflight reaches production `_exit(2)` at `tools/new1_identity_diag.py:631` after **2.016580333 s**; masked monitor reaches `:614` after **2.045951709 s**. These are lower bounds measured at the native-exit call, already exceeding `.3 s`.
- Corresponding unmasked controls return through Python in **0.110273208 s** and **0.122324792 s**.

The raw native-exit records contain the blocked mask, pending `[14]`, source location, and exception chain. Preflight exhausts work and terminal-recording budgets; monitor exhausts the reaping budgets. This supports fixing the parent’s response to a blocked enforcement mask. It does **not** establish that this explains every historical failure. See `Audit:461–468,523`; raw events `95619_000115.json:1` and `95934_000122.json:1` in their respective masked-control directories.

The fixture-leak ruling is narrower. Events `step2_baseline_03/events/77436_000276.json:1` and `77436_000277.json:1` establish `[] → [2,14]` across the unchanged identity deadline test, before fixture cleanup. They do not identify an instruction. That test calls production `I.supervise`; this is not evidence that test teardown itself introduced the mask. See [tests/test_new1_identity_diag.py:152–168](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_identity_diag.py:152).

There is nevertheless a source-supported correction target: mask mutation precedes the inner restoration protection at `I:495` and `I:510`, while final cleanup restores the mask observed at cleanup entry rather than an independently retained supervisor-entry mask (`I:635–641`). An interrupted mutation/restoration can therefore escape the intended invariant. **That is a testable vulnerability, not attribution of the recorded leak.** Python’s deferred execution of signal handlers makes interruption at Python boundaries relevant. [Python signal documentation](https://docs.python.org/3.11/library/signal.html#execution-of-python-signal-handlers).

The exact leak instruction, observer contribution, native-thread effects, and load remain open. None is necessary to establish that entering this parent with disabled enforcement is unsafe. External inheritance is also possible by contract: `exec` preserves the calling thread’s signal mask. Its occurrence in a real launch remains untested. [POSIX exec](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html).

**2. Production-fix contract — arrangement (c), both**

Implement the following two criteria, each with saved behavioral RED evidence before its production change.

1. **Restore signal state reliably across production critical sections.**

   In `tools/new1_identity_diag.py`, retain the original caller mask before mutation and establish restoration protection before the mutation can take effect. Cover deadline entry/exit, handler installation/restoration, and the same mutation pattern in `OwnedWorker` operations. Preserve unrelated blocked signals, cancellation semantics, ownership bookkeeping, and the original absolute deadline.

   A normal Python return or propagated exception must not leave supervisor-added mask bits behind, a live supervisor timer, or substituted handlers. Merely moving a `try` below the mutating call, resetting the mask in test teardown, or clearing all signals is insufficient. See [tools/new1_identity_diag.py:492–523](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_identity_diag.py:492), `:635–641`, and `:366–430`.

   **RED:** deterministically interrupt after the real mask mutation but before the current restoration protection, separately exercising the `:495` and `:510` boundaries. Capture the mask immediately after production unwinds, before any fixture repair. Assert equality with the original mask, including a case with an unrelated blocked signal. Include a schedule with an owned child and inspect reaping/channel state before cleanup. Injection must exercise the boundary; it must not simply leave the mask blocked on the test’s behalf. If the proposed schedule does not fail on unchanged production, it is not qualifying RED evidence.

   **GREEN:** those schedules restore state and retain bounded cleanup; the original identity deadline fixture also asserts signal-state preservation before teardown. Keep the full shared-process suite order.

2. **Reject an unenforceable caller mask before protected work begins.**

   Add an explicit `INVALID-ENFORCEMENT` entry check for blocked SIGALRM or SIGINT, individually or together. SIGALRM supplies deadline enforcement; SIGINT supplies the promised cancellation path. Preserve the caller’s mask and pending signals rather than silently unblocking or consuming them.

   Put the shared check in `tools/new1_identity_diag.py`; invoke it at direct `I.supervise` entry and in both diagnostic parent entry points **before their first timed file operation**. Construction main currently hashes its source and creates its directory before calling `I.supervise`, so a supervisor-only check is too late. See [tools/new1_construction_diag.py:234–240](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_construction_diag.py:234) and `tools/new1_identity_diag.py:662–668`.

   **RED:** with `[2,14]` already imposed, exercise direct supervision and actual construction main. Assert refusal before source verification, directory creation, output persistence, monitor/preflight/admission callbacks, or worker creation. The current source lacks this refusal; the existing masked-parent receipts additionally establish deadline failure. Cover SIGALRM-only and SIGINT-only cases.

   **GREEN:** direct supervision raises the named refusal; each parent main returns Python status `2` through its ordinary error path. State remains unchanged, no worker/guardian is created, and no measured result is published. The `.2 s` parent budget and `<.3 s` fixture bound remain unchanged. Rejection must not depend on the unavailable alarm or introduce synchronous artifact persistence before refusal.

This requires changes to both diagnostic scripts, both owned test files, and an additive FIX5 scope revision. Preserve the historical scope text and receipts.

The skipped `process.wait()` in **`tools/new1_supervisor.py:411–428` stays a separate ownership issue**, outside this fix. It is real static evidence, but neither warned PID is attributed to it, and construction main uses `I.supervise`, not `S.supervise`. Leave both supervisor files unchanged. A subsequent warning or ownership failure still stops qualification; it cannot be waived because this issue was scoped separately. See [tools/new1_supervisor.py:411–428](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:411).

The native exits at **`I:614` and `I:631` remain correct last-resort fail-closed behavior**: respectively, ownership cannot be confirmed and bounded terminal reporting cannot complete. They do not prove cleanup or satisfy the ordinary-return deadline. Preserve them and their existing failure controls; do not replace them with fabricated terminal success, unconditional Python return, or additional time.

**3. Qualification sequence**

All r4 investigation caps remain exhausted. The following is correction qualification in a fresh namespace, not another attempt at steps 1–3.

1. **Freeze the FIX5 contract and test inventory; save RED, implement, then save GREEN.** Bind loaded paths, source/test hashes, commands, exits, ownership observations, and every failure. Retain all existing tests and FIX4 lifecycle protections.

2. **Require actual-parent controls.** Run the unmasked blocked-preflight, blocked-monitor, and resource/cleanup cases, plus their preblocked-mask counterparts, against original construction main and corrected production supervision with science boundaries stubbed.

   Keep `.2 s` as the configured parent bound and `<.3 s` as the measured fixture requirement. Inspect ownership **before fixture cleanup**. Unmasked cases that create children require matching worker-reaping proof, guardian collection, worker/group absence, closed owned channels, and empty streams.

   For preblocked entry, the approved expected result changes specifically to **early `INVALID-ENFORCEMENT` refusal with no ownership acquired**. It need not create a result file merely to reject an invalid entry condition. This does not replace the unmasked cleanup controls or criterion 1’s interruption-with-owned-child coverage.

   Record Python return separately from native termination. An external exit code `2` alone passes neither distinction; a missing return marker or missing ownership observation fails the applicable control. Existing emergency-exit tests remain separate.

3. **Complete fresh sandbox acceptance.** Retain the scope’s **20 consecutive solo runs**, then require a **fresh 3/3 full four-suite batch** on the frozen corrected candidate. Preserve suite order and stop on the first failure. No suite isolation, warning suppression, selective restart, or relaxed deadline is approved. The 20-run prerequisite is retained from `new1_construction_diag_scope.md:537`; fresh 3/3 is required by r4:52.

   `R/run_checks.py:63` hard-codes 188. Added FIX5 methods require a reviewed, frozen expected count. Preserve the historical runner; use a FIX5 copy retaining its execution and failure-stop contract, with the explicit new count and complete hash manifest. Do not infer the expected count from successful output or remove tests to retain 188.

4. **Require one externally inherited-mask launch control before host qualification.** Name it **`fix5_inherited_mask_launch_01`**. It requires **new explicit operator authorization**; this review does not execute or assume that authorization.

   One external launcher must block `[2,14]` before exec of a fresh interpreter entering the actual construction-parent path with science stubbed. Record the mask before exec and at initial interpreter entry, without setting it again inside that interpreter. Require the same early-refusal, no-owner, state-preservation, Python-return, and timing evidence as above. Record startup time separately from the `.2 s` parent interval; do not claim an arbitrary whole-interpreter startup cap.

   This control is material to qualification of the entry placement, **not a prerequisite to implementing the fix**. Failure stops qualification; no automatic second attempt.

5. **Then retain the host bar unchanged:** **100 consecutive fresh-process solo runs plus 10 consecutive fresh-process full four-suite runs**, through the reviewed FIX5 copy of `R/run_checks.py`. Stop on the first failure; require complete expected counts, no ResourceWarnings or ignored exceptions, no unexpected native exits/timeouts, and no cleanup leakage. Real diagnostic approval remains separate. See [r4:50–54](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_astra_r4.md:50).

The host-load note does not invalidate the observed mask/pending-signal mechanism or excuse either missed deadline. It also does not isolate load as irrelevant. Record concurrent work and coordinate qualification without competing test jobs; retain the thresholds. A clean host batch cannot retrospectively identify the original cause. `RECEIPT/maestro15_drift_reconciliation.md:14–16`.

**4. Status**

The failed FIX4 batch remains **0/3 permanently**. Investigation passes contribute zero acceptance runs.

The current five-file candidate cannot survive byte-for-byte: the production restoration and entry changes, regression tests, and scope amendment are substantive requirements. FIX4’s valid lifecycle corrections should survive within the corrected files. The two supervisor files remain unchanged, with their separate ownership issue explicitly open.

🌱 graft reported approximately 40,591 tokens saved this turn; one successful call and one failed probe.

VERDICT: FIX5

