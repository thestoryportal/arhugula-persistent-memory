# Gap Session 12 Summary — Aggregate Mismatch Detection & Constitutional Test Clock Injection

**Session:** GS12 of 13
**Primary skills:** aisecops-specialist (Warden), orchestration-comparativist, validation-contract-architect
**Baseline:** v1.1 integrated spec + GS1–GS11
**Gaps addressed (2):** GAP-38, GAP-39
**Tensions triaged (1):** T-TGA-load
**Sequencing note:** GAP-38 and GAP-39 are independent with no upstream dependencies on each other or on unresolved prior-session output; they are resolved in numeric order. T-TGA-load triage is addressed last as a closing item.

---

## Resolutions

### GAP-38 — Cross-Invocation Aggregate SCOPE_HASH_MISMATCH Detection — Spec Block

**What it must do / represent / enforce / guarantee:**
Detect distributed scope-hash-mismatch attack patterns that evade the per-invocation A4 rule (2 consecutive mismatches for the same invocation → human review) by spreading single mismatches across many invocations or many agents. The aggregate detector is **additive to, not a replacement for,** the per-invocation rule: both operate concurrently.

**Hard constraints:**
- **C-AGG-1 (Counter Scope):** The aggregate counter is **per-Orchestrator-instance, global across all `agent_id` values and all in-flight invocations**. This is deliberately broader than the per-invocation per-agent A4 rule — the attack pattern being detected is distribution, so the detector must aggregate across distribution axes.
- **C-AGG-2 (Threshold):** N ≥ 10 SCOPE_HASH_MISMATCH events within a sliding window of M = 60 seconds triggers the aggregate alert. **Starting values ratified as baseline.** Both N and M are Tier 1 configuration (`scope_mismatch_aggregate_threshold_n`, `scope_mismatch_aggregate_window_seconds`) and may be tuned per deployment; operators adjusting them below N=5 or above M=300s SHOULD declare rationale in deployment documentation.
- **C-AGG-3 (Sliding Window):** The counter uses a sliding time window, not a fixed tumbling window. Events age out of the count as they exceed M seconds from the current evaluation time. This prevents a trivial evasion pattern at window boundaries.
- **C-AGG-4 (Dual Alert Path):** Exceeding the aggregate threshold produces **both** (a) a Ledger entry of new type `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1), and (b) routing to the human review queue via the existing review-queue interface (IC-REVIEW-QUEUE, amended GS11). The Ledger entry provides the durable audit record; the queue routing provides the operator action path. The two are produced as a linked pair — the review-queue item carries the `alert_ledger_entry_position` of its originating Ledger entry.
- **C-AGG-5 (Alert Content):** `SCOPE_MISMATCH_AGGREGATE_ALERT` carries: `window_start_time`, `window_end_time`, `event_count`, `threshold_n_at_time_of_alert`, `threshold_m_at_time_of_alert`, `contributing_agent_ids` (deduplicated set), `contributing_invocation_ids` (deduplicated set), `contributing_event_positions` (Ledger positions of the N mismatch events that constitute the window).
- **C-AGG-6 (Counter Reset Semantics):** The counter is **not** reset on human review resolution. The counter is a pure sliding-window aggregate of observed events; review resolution closes the queue item but does not rewrite event history. Events naturally age out as they exceed M seconds. If the underlying attack pattern is ongoing, the counter will re-cross the threshold and emit a new alert — this is correct behavior (the alert is fresh evidence that the pattern persists), not a spurious re-alert.
- **C-AGG-7 (Alert Cooldown):** To prevent alert storms when the threshold is persistently exceeded, the Orchestrator applies a cooldown: after emitting `SCOPE_MISMATCH_AGGREGATE_ALERT`, a subsequent alert for the same sliding-window condition is suppressed for a minimum of M seconds (one full window). Suppressed-but-qualifying conditions increment a counter in the next emitted alert's `suppressed_requalification_count` field, so operators can see the pattern intensity even during cooldown.

**Tradeoffs decided:**
- **Global (per-Orchestrator) over per-agent aggregation** — the attack vector being defended against *is* cross-agent distribution; per-agent aggregation would be defeated by using multiple agents.
- **Sliding over tumbling window** — tumbling windows leak a trivial evasion at window boundaries (stage N−1 events just before a boundary, then N+ just after).
- **Dual path (Ledger + queue) over single path** — Ledger-only loses operator responsiveness; queue-only loses durable audit. Both are cheap; both are required.
- **Counter not reset on review resolution** — the counter measures observed world-state, not review-queue state. Tying the two would suppress legitimate re-detection of an ongoing attack while a stale review is still open.
- **Cooldown with suppressed-count carry-forward** — prevents N-per-window-per-window alert storms while preserving visibility into persistent patterns.
- **Values N=10 / M=60s ratified as starting baseline** — consistent with scope_update_min_interval (3,600s) and per-invocation A4 (2). A distributed attack would need to orchestrate ~10 mismatches per minute across agents, which substantially exceeds any plausible legitimate mismatch rate under the scope-update ceremony cadence.

**Open questions (deferred):** None for v1.1.

**Interface contract:**
- **IC-AGG-COUNTER (new):** Orchestrator maintains a sliding-window SCOPE_HASH_MISMATCH counter, updated on every occurrence of the per-invocation mismatch condition, evaluated against (N, M) after each update. Counter is in-process state; on Orchestrator restart, counter is reset to empty (by construction — no events have been observed since restart). Restart-induced reset is acceptable: the underlying mismatch events remain in the Ledger; post-restart detection resumes on fresh events.
- **IC-AGG-ALERT-LINK (new):** `SCOPE_MISMATCH_AGGREGATE_ALERT` Ledger entry and its corresponding review-queue item MUST cross-reference each other (`alert_ledger_entry_position` on the queue item; `review_queue_item_id` on the Ledger entry). Either direction of lookup is available at query time.
- **Appendix C addition:** `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1).
- **Config schema additions (Tier 1):** `scope_mismatch_aggregate_threshold_n` (default 10), `scope_mismatch_aggregate_window_seconds` (default 60), `scope_mismatch_aggregate_cooldown_seconds` (default 60, = window M).

---

### GAP-39 — Constitutional Test Clock Injection + OQ-V9 Resolution — Spec Block

**What it must do / represent / enforce / guarantee:**
Enable constitutional tests to assert time-dependent framework invariants (notably C26 corpus staleness at 180 days, and any future invariants with Ledger-cadence or time-based assertions) while preserving D97 Q5's determinism requirement. A constitutional test declares whether it depends on wall-clock behavior via a metadata flag; the Validator sandbox injects a synthetic clock whenever the flag is set; Q5 is validated at nomination time by structural evidence, not by runtime assertion-message inspection.

**Hard constraints:**
- **C-CLK-1 (Flag Requirement):** Every constitutional test MUST declare `clock_stub_required: <boolean>` in its test metadata. Absence of the flag is a nomination error — the test cannot enter review until the author attests one way or the other.
- **C-CLK-2 (Sandbox Injection — Required when Declared):** When `clock_stub_required: true`, the Validator sandbox MUST inject a synthetic clock abstraction (implementation: a clock-source facade that test code reads via the test harness's time primitive, seedable at test entry, and monotonic within a test invocation). Direct access to OS wall-clock syscalls from within such a test MUST be blocked by the sandbox.
- **C-CLK-3 (Injection Failure Is a Sandbox Config Error, Not a Test Failure):** If a test declares `clock_stub_required: true` and the sandbox cannot demonstrably inject a synthetic clock (e.g., configuration error, missing harness module, wall-clock syscall not blocked), the outcome is a **SANDBOX_CONFIG_ERROR**, distinct from a test pass or fail. A test with a config-error outcome does NOT advance in the Reflexion loop, does NOT trigger retry, and does NOT count toward pass/fail statistics. It is a halt condition requiring sandbox remediation.
- **C-CLK-4 (Flag-False Constraint):** When `clock_stub_required: false`, the test's body MUST contain no reads of wall-clock time. This is enforced at nomination review (Q5 evidence verification, below) — at runtime, the sandbox does not need to block wall-clock access for flag-false tests, but Q5 reviewer attestation is the gating mechanism.
- **C-CLK-5 (Synthetic Clock Determinism):** The synthetic clock's starting value and any in-test advancement (e.g., `clock.advance(seconds=180*86400)` primitives) MUST be fully specified within the test body. Tests MUST NOT depend on implicit default clock values — the starting epoch MUST be set explicitly. This ensures the test is reproducible across sandbox runs and across reviewer re-executions.

**Q5 Evidence Contract (D98 nomination_record extension):**
The qualification checklist entry for Q5 carries an evidence_ref whose shape depends on the `clock_stub_required` declaration:

- **Case (a) — `clock_stub_required: false`:**
  - `evidence_type`: `"no_wallclock_assertions"`
  - `evidence_text`: a short human-readable attestation, e.g. `"Test body contains no wall-clock reads. Asserts structural invariants only."`
  - `attesting_operator_id`: the nominator's stable operator ID (per GS11 IC-CAK-IDENTITY).
  - `attestation_timestamp`: nomination submission time.

- **Case (b) — `clock_stub_required: true`:**
  - `evidence_type`: `"clock_stub_verified"`
  - `evidence_text`: a short attestation, e.g. `"Test declares clock_stub_required: true. Sandbox configuration verified to inject synthetic clock at nomination-time dry-run."`
  - `sandbox_config_hash_at_verification`: SHA-256 of the sandbox configuration used for the nomination-time dry-run (binds the attestation to a specific sandbox state).
  - `nomination_dry_run_outcome`: one of `TEST_PASSED`, `TEST_FAILED`, `SANDBOX_CONFIG_ERROR` (must be `TEST_PASSED` for nomination to proceed — a failing dry-run blocks nomination regardless of intent; a config-error dry-run blocks and surfaces to sandbox operator).
  - `attesting_operator_id`: the nominator's stable operator ID.
  - `attestation_timestamp`: nomination submission time.

**OQ-V9 Resolution — Runtime structural inspection of Q5:**
**Rejected for v1.1.** Structural inspection of a failing test's assertion message to determine whether wall-clock was involved is brittle (fragile to test framework output format changes), language-specific (different test runners format messages differently), and provides no stronger guarantee than the nomination-time attestation + dry-run pair. The Q5 evidence contract above is sufficient: the flag is declarative, the sandbox's injection behavior is enforced by C-CLK-2 / C-CLK-3, and the nomination-time dry-run closes the loop on "does this test actually pass in the sandbox as configured." Runtime structural inspection adds no information that nomination-time dry-run does not already provide.

The rejection is flagged for v2 reconsideration only if future constitutional tests introduce non-clock non-determinism sources that a declarative flag cannot cover (e.g., network stubs, non-deterministic iteration order) — at that point the broader question of runtime validation may need revisiting. For v1.1, Q5 is a nomination-time-only check.

**Tradeoffs decided:**
- **Declarative flag over implicit inspection** — a flag author must make a decision and sign an attestation. Implicit inspection pushes the decision into a brittle heuristic layer.
- **Sandbox config error as distinct outcome, not test failure** — conflating config errors with test failures would pollute the Reflexion loop's retry logic (retry does not fix a sandbox misconfiguration) and would misattribute sandbox bugs to test authors.
- **Nomination-time dry-run required for flag-true tests** — costs one sandbox invocation at nomination submission but guarantees the attestation is grounded in observed behavior, not just claimed intent.
- **Nomination-time attestation over runtime inspection** — stronger evidence (bound to a specific sandbox configuration hash), simpler to implement, language-agnostic.
- **Explicit synthetic-clock starting value required (C-CLK-5)** — prevents hidden reproducibility breaks when sandbox defaults change.

**Open questions (deferred):**
- **OQ-V10 (v2):** Non-clock non-determinism sources in constitutional tests (network stubs, iteration order, memory-layout-dependent assertions). If these arise, the declarative-flag model generalizes; but the dry-run verification step may need a richer evidence schema. Not a v1.1 concern — no current constitutional test requires them.

**Interface contract:**
- **IC-CLK-META (new):** Test metadata schema (Validator-side) adds `clock_stub_required: boolean` as a required field. Tests without the field fail nomination intake.
- **IC-CLK-SANDBOX (new):** Sandbox harness exposes (a) a time-primitive facade that test code uses instead of direct OS time syscalls; (b) a sandbox-config flag that activates synthetic-clock injection; (c) a wall-clock-syscall blocker active when the flag is set; (d) a config-verification endpoint that the nomination-time dry-run invokes to confirm (a)–(c) are live before test execution.
- **IC-NOM-DRYRUN (new):** Nomination pipeline runs each candidate constitutional test once in the sandbox as configured at nomination time, captures `sandbox_config_hash` and test outcome, and records them into `nomination_record.qualification_checklist[Q5].evidence_ref`. Nomination advances only on `nomination_dry_run_outcome: TEST_PASSED`.
- **D98 nomination_record schema amendment:** `qualification_checklist[Q5].evidence_ref` gains the structured shape defined above (discriminated on `clock_stub_required`).
- **SANDBOX_CONFIG_ERROR outcome type:** added to the Validator's outcome vocabulary (distinct from PASS, FAIL, TIMEOUT).

---

### T-TGA-load — Triage Outcome

**Triage decision:** Option **(a) — Accept for v1.1, flag for v2.**

**Rationale:**
The concentration of probe template authorship (three sub-types, per v2 GS10) alongside executable test authorship and sole authority to read task specifications for verification artifacts is an intentional consequence of the actor-critic independence constraint (D32–D33): the verifier must be insulated from the actor. Splitting TGA into TGA-Test and TGA-Probe would require either (a) duplicating the task-specification reading authority (violating the skill constraint that only one agent reads the spec for verification purposes) or (b) introducing a shared intermediate representation that both sub-agents read, which merely moves the concentration point rather than removing it.

For v1.1, the concentration is governed by D32–D33 as an acknowledged design principle, not an oversight. The single-agent authorship is auditable through the Ledger and bounded by the Validator's sandbox contract.

**v2 flag recorded:** If operational experience in v1.1 surfaces specific failure modes tied to the authorship concentration (e.g., author blind spots that a split would catch, review-cadence bottlenecks), v2 SHOULD revisit the split with the benefit of observed evidence. The question to revisit is not "should we split" in the abstract but "what specific evidence from v1.1 operation argues for a split."

**Status change:** T-TGA-load closed as 📋 **Accepted for v1**, v2-reconsider flag set.

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-38 — RESOLVED.** Aggregate SCOPE_HASH_MISMATCH detector ratified: N=10, M=60s sliding window, per-Orchestrator-instance global scope, dual alert path (Ledger entry `SCOPE_MISMATCH_AGGREGATE_ALERT` SECURITY/async/W1 + review queue item cross-linked), counter not reset on review resolution, cooldown = M seconds with suppressed-requalification counter on the next emitted alert. Additive to the per-invocation A4 rule.
- **GAP-39 — RESOLVED.** Clock injection contract defined: `clock_stub_required` flag required on every constitutional test; sandbox synthetic-clock injection mandatory when flag is true; missing injection → distinct `SANDBOX_CONFIG_ERROR` outcome (not a test failure); Q5 evidence contract extended with two discriminated shapes (flag-false attestation / flag-true attestation + nomination-time dry-run + sandbox-config hash); explicit synthetic-clock starting value required (C-CLK-5). **OQ-V9 resolved:** runtime structural inspection of Q5 rejected for v1.1; nomination-time declarative attestation + dry-run is sufficient.

**GAPS PARTIALLY RESOLVED:** None.

**GAPS DEFERRED:** None from this session's allocation.

**NEW GAPS SURFACED:** None.

**NEW TENSIONS SURFACED:** None.

**TENSIONS CLOSED:**
- **T-TGA-load** → 📋 **Accepted for v1**, v2-reconsider flag set. Concentration of verification-artifact authorship in TGA ratified as a governed consequence of D32–D33 skill-constraint independence, not an oversight. v2 revisits only if v1.1 operational evidence argues for a split.

**NEW OPEN QUESTIONS (deferred to v2):**
- **OQ-V10 (v2, Validation Contract):** Non-clock non-determinism sources in constitutional tests (network, iteration order, memory layout). If any future test requires them, the declarative-flag model generalizes but the dry-run evidence schema may need extension. Not a v1.1 concern.
- **v2 flag on T-TGA-load:** Reconsider TGA-Test / TGA-Probe split if v1.1 operational experience surfaces concrete failure modes tied to the concentration.

**INTERFACE CONTRACTS DEFINED (new):**
- **IC-AGG-COUNTER** — Orchestrator-maintained sliding-window aggregate counter for cross-invocation SCOPE_HASH_MISMATCH (GAP-38).
- **IC-AGG-ALERT-LINK** — bidirectional cross-reference between `SCOPE_MISMATCH_AGGREGATE_ALERT` Ledger entry and review-queue item (GAP-38).
- **IC-CLK-META** — constitutional test metadata extension: `clock_stub_required` required field (GAP-39).
- **IC-CLK-SANDBOX** — sandbox time-primitive facade, injection flag, wall-clock-syscall blocker, config-verification endpoint (GAP-39).
- **IC-NOM-DRYRUN** — nomination-time dry-run execution, outcome capture, sandbox-config-hash binding into Q5 evidence (GAP-39).

**APPENDIX C ADDITIONS (new entry types):**
- `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1) — GAP-38.

**SCHEMA AMENDMENTS:**
- Tier 1 config: `+ scope_mismatch_aggregate_threshold_n` (default 10), `+ scope_mismatch_aggregate_window_seconds` (default 60), `+ scope_mismatch_aggregate_cooldown_seconds` (default 60). (GAP-38)
- Constitutional test metadata: `+ clock_stub_required: boolean` (required). (GAP-39)
- D98 `nomination_record.qualification_checklist[Q5].evidence_ref`: discriminated-shape structure (flag-false / flag-true branches, with sandbox-config-hash and dry-run outcome on flag-true). (GAP-39)
- Validator outcome vocabulary: `+ SANDBOX_CONFIG_ERROR` (distinct from PASS / FAIL / TIMEOUT). (GAP-39)

**DOWNSTREAM INPUTS TO GS13:**
- GS12 introduces one new Appendix C entry type (`SCOPE_MISMATCH_AGGREGATE_ALERT`) and one new outcome type (`SANDBOX_CONFIG_ERROR`). Both are W1-scope; no new W3 carve-outs. GS10's C-W3 admission criteria remain the gating policy for W3.
- T-TGA-load closure clears the last Council-flagged v1.1 tension from tension-map-v4.md's open set tied to validation/orchestration seam; GS13 inherits no residual T-TGA-load work.
- OQ-V10 is the only new v2-deferred open question from GS12 and is isolated (no v1.1 downstream implications).
- No new cross-domain conflicts introduced; GS13 inherits the tension-map state closed at the end of GS12 (which is the GS11 state minus T-TGA-load).
