## 11. State Consistency Layer

### 11.1 Purpose

The Git repository and the `.vindex` overlay must tell the same story, and the system must have a defined answer for every failure mode where they could diverge. This layer specifies which medium is authoritative for which content class, how writes are coordinated across both, and how drift is detected and healed.

### 11.2 Content-Scoped Authoritative Medium (D42)

- **Git authoritative** for `structural_entity` knowledge.
- **`.vindex` authoritative** for Genesis Layer 4 `domain_concept` and `constraint_rule` knowledge.

Every `.larql` patch carries a mandatory `CONTENT_CLASSIFICATION` directive: `structural` | `layer4_domain` (C-SC3, IC-SC1). Value `mixed` is rejected pre-commit (C-SC4). The `CONTENT_CLASSIFICATION_MIXED` rejection (IC-GATE-9) carries split guidance directing the Coder Agent to resubmit as distinct single-classification patches. The split is driven by Gate's triple-level classification check, not the Coder's declared directive. This preserves the authoritative-medium assignment per D42.

### 11.3 Strong Consistency Model (D43)

Strong consistency globally. Reads block against `.vindex` during the mount window. No stale-read fallback. Write concurrency capped at 1 via the Commit Executor FIFO queue (C-CW1). Fan-out occurs above the queue; strict serialization at the queue.

### 11.4 Atomic Transaction Unit (D44, extended T8)

The atomic transaction is the **task-completion package** (C-TPC1):
```
{
  module_code,
  test_suite,
  .larql_patch,
  declared_dependencies    ← added T8
}
```

These commit together or not at all.

### 11.5 Two-Phase Commit Protocol

**Phase 1 — Prepare:**
- Commit Executor receives verified package from Orchestrator (IC-TPC1).
- Writes `PREPARED` Ledger entry with package hash and classification.
- Admits package into the 2PC window; holds session-scoped lock (C-TPC5).

**Phase 2 — Commit (ordering fixed per D46 / C-TPC3):**
1. **Git push first.**
2. **`.vindex` mount second.**

Ordering constrains failure modes to Git-ahead (easier to recover via compensation) rather than Weights-ahead (harder).

On success: writes `COMMITTED` Ledger entry with overlay hash.

Every 2PC produces `PREPARED` and `COMMITTED` entries. Missing `PREPARED` is a Ledger-bypass security incident (C-TPC4).

**§11.5.1 — PREPARED-State Timeout Behavior (D85)**

Two configurable timeout values apply (both stored in Tier 1 config):
`incremental_prepared_timeout` (default 2 hours) for all non-Genesis transactions, and `genesis_prepared_timeout` (no default; Gate blocks Genesis initiation if absent, C-GATE-2) for Genesis compiles.

Incremental timeout: TC executes Phase 1 rollback, releases Write Lock, sets task to `AWAITING_OPERATOR_RETRY`. Dependency Hold persists through timeout — the Hold MUST NOT be released automatically on timeout; it persists until successful commit on retry or explicit operator-signed Hold release. Retry requires fresh token (infrastructure failure class per D67 — no retry budget consumed). Three consecutive timeouts on the same task → human review queue escalation, flagged `repeated_timeout`.

Genesis timeout: circuit breaker trips immediately (`DIVERGED_STATE` type per IC-TC-RESET). No auto-compensation — partial compile state is preserved as forensic evidence. Operator MUST run full model integrity check against the pre-Genesis `IMMUTABLE_ANCHOR` baseline before the reset ceremony may proceed (IC-TC-TIMEOUT).

### 11.6 Genesis as Single Atomic 2PC (D45, C-TPC2)

Genesis compile is a single atomic 2PC event across all tier files L1–L4. Partial Genesis is not a valid state. Architect Agent's internal sub-batching (T6) is transparent to the Ledger.

### 11.7 Transaction Controller — Compensation Authority (D47, C-TC1)

Sole compensating-transaction authority. No agent, including the Commit Executor, self-compensates. Compensation direction determined by `CONTENT_CLASSIFICATION` (C-TC2):

- **Structural patches:** auto-revert Git on persistent `.vindex` failure (3 mount retries, then revert).
- **Layer4_domain patches:** retry `.vindex` up to 5x; Git revert requires human confirmation.

All compensating transactions logged to the Ledger (C-TC4).

### 11.8 Circuit Breaker (D48, C-TC3, extended by GS10–GS11)

Thresholds:
- 3 consecutive 2PC failures in one task → trip (`CONSECUTIVE_FAILURE`).
- 5 consecutive 2PC failures across any tasks in a 10-minute window → trip (`CROSS_TASK_FAILURE`).
- Diverged state → immediate trip, no auto-repair (C-TC5) (`DIVERGED_STATE`).
- Genesis-timeout-without-trip pairing failure (`GENESIS_TIMEOUT_TRIP_MISSING`, C-GTO-1/2, IC-MON-GTOTM).
- Aggregate `SCOPE_HASH_MISMATCH` threshold breach (§14.3, IC-AGG-COUNTER).

On trip: systemwide write suspension (READ_ONLY mode — see §11.8.1). Write resumption requires the signed reset ceremony (IC-TC-RESET). Trip reason is recorded on every `CIRCUIT_TRIPPED` Ledger entry with a **cross-category rationale annotation** (A8 — every `CIRCUIT_TRIPPED` records whether the originating signal was INTEGRITY, CONSISTENCY, or SECURITY category, so the reset ceremony has the provenance context needed for the right precondition branch).

Abort authority (human interrupt of PREPARED transaction): exists via signed abort request to Orchestrator, always routes through Transaction Controller compensation path, never process-kill (OQ-TPC2 resolved D74). Post-commit abort is rejected.

**State machine (extended GS10):** The TC operates under a six-state machine (GAP-58 / GS10 — state lifecycle integration):

| State | Entry | Exit |
|---|---|---|
| `WRITE_ENABLED` | Boot after successful verification; `CIRCUIT_RESET` completion. | Any trip condition → `CIRCUIT_TRIPPED`. Burst-limit breach → `BURST_SUSPENDED`. Double-compromise → `TRUST_ROOT_LOST`. |
| `CIRCUIT_TRIPPED` | Any trip condition. | IC-TC-RESET ceremony (A3 CAK-authorized) → `WRITE_ENABLED`. |
| `READ_ONLY` | Synonym for `CIRCUIT_TRIPPED` operational surface; inference/query proceed. | As `CIRCUIT_TRIPPED`. |
| `BURST_SUSPENDED` | Per-CAK burst limit breach (N=5 / 10min, GAP-41, IC-CAKB-1). | 60-minute auto-clear OR Tier 1 explicit-clear ceremony. Transitions to `WRITE_ENABLED`. |
| `TRUST_ROOT_LOST` | Double-compromise detected (primary CAK and break-glass channel both suspect). Terminal in v1.2. | No automatic exit. Operator recovery requires full genesis reseal procedure (v2 scope). |
| `HALTED` | Reserved for `CONSTITUTIONAL_FAILURE` weak-check advisory (§25). Not auto-entered in v1.2; advisory-only. | N/A (v1.2). |

**BURST_SUSPENDED interaction with circuit reset:** a harness in `BURST_SUSPENDED` rejects IC-TC-RESET ceremonies with `CIRCUIT_RESET_REJECTED_BURST_STATE` until the burst window clears (GAP-58 resolution). Burst-suspension and circuit-trip are orthogonal states; clearing one does not clear the other.

**TRUST_ROOT_LOST is terminal:** a harness in `TRUST_ROOT_LOST` processes no ceremony types and issues no tokens. Only read-query inference proceeds. See §23.3 break-glass.

### 11.8.1 READ_ONLY Mode and Write Resumption Ceremony (D84, revised A1-REVISED + A2 + GAP-35 + GAP-37)

On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human action. Inference, query, and read operations proceed normally; write token issuance is suspended. Consistency Status API state transitions to `CIRCUIT_TRIPPED` (§12.5).

**Consumed tokens proceed to natural outcome (GAP-35).** Tokens that the Gate has already admitted (status: `CONSUMED`) are not invalidated by circuit trip. Their owning transactions proceed through their natural PREPARED → COMMITTED or PREPARED → ABORTED lifecycle under TC supervision. New tokens are not issued in READ_ONLY.

**Governance-category write carve-out (GAP-37, IC-GCO-1 — closes T-SC-W-2).** Governance-category Ledger entries written as part of the signed reset ceremony itself proceed regardless of `CIRCUIT_TRIPPED` state. This is a narrow carve-out: only entries whose `audit_category: GOVERNANCE` and whose ceremony_token_id binds them to the active IC-TC-RESET invocation are permitted. Token-mediated writes (Coder/Architect/Pruning output) remain suspended. This carve-out is a W3 cross-reference (§16.2) — the emergency-writer tier is the only writer that can emit during `CIRCUIT_TRIPPED`, and only for the reset ceremony's own Ledger entries.

**Write resumption requires a signed reset ceremony (IC-TC-RESET, A3 — CeremonyToken / CAK-authorized).** The TC independently verifies preconditions before accepting any reset request — human attestation alone is not sufficient.

**Admission order for IC-TC-RESET:**

1. **Precondition branch selection** by trip reason (cross-category annotation, A8):
   - `CONSECUTIVE_FAILURE` or `CROSS_TASK_FAILURE`: compensation is `COMPLETED` and current overlay hash matches the Ledger's most recent `COMMITTED` entry.
   - `DIVERGED_STATE`: a `RECONCILIATION_COMPLETE` Ledger entry with `result: "CONSISTENT"` timestamped after the trip.
   - `GENESIS_TIMEOUT_TRIP_MISSING`: a matching paired trip entry must exist (C-GTO-2).
   - Genesis-trip Hold release (A12): if the trip occurred during Genesis and any Dependency Holds remain active from the pre-trip epoch, a paired `HOLD_RELEASE` ceremony must have resolved those Holds before IC-TC-RESET can admit.
2. **CeremonyToken verification** against `ceremony_authorization_key_anchor` (§13.2, §20). ceremony_type discriminator must equal `CIRCUIT_RESET`.
3. **Precondition check** — if any branch precondition fails, the TC rejects with `CIRCUIT_RESET_REJECTED` (A2), emitting a Ledger entry that names the unmet precondition. The submitted CeremonyToken is **not** consumed by a precondition-check rejection (GAP-35 — consumed tokens proceed to natural outcome; but a precondition-rejected token is not consumed because the ceremony never admitted).
4. **CAK verification** — signature validity over the reset envelope.
5. **`CIRCUIT_RESET` Ledger write** (GOVERNANCE, synchronous) → state transitions to `WRITE_ENABLED`.

Reset via the W3 emergency Ledger path is not permitted as a substitute for the signed ceremony. The signed ceremony is the exclusive mechanism for write resumption. (The W3 governance carve-out above permits W3 writes of the ceremony's own Ledger entries, not W3 writes as reset.)

### 11.8.1.1 Bounded Compensation Under READ_ONLY (A1-REVISED; C-CRC-3)

Transaction Controller compensation during READ_ONLY is **bounded to reversal-only** operations. The TC MUST NOT perform forward progress, speculative reapplication, or any compensation whose effect is to advance state beyond the last `COMMITTED` entry. Permitted compensation operations:

- **Git revert** of the failed transaction's staged commit (Structural content classification).
- **`.vindex` overlay rollback** to the pre-PREPARED tier state.
- **Ledger annotation** via `ABORTED` entry + `COMPENSATION_COMPLETED` entry.

Prohibited during READ_ONLY:

- Retry of the failed transaction (retries are a pre-trip construct; after trip, the transaction is terminal).
- Any `COMMITTED` entry emission for the failed transaction's content.
- Any overlay write beyond rollback to the trip-time `anchor_hash`.

Violation of the reversal-only bound produces `BOUNDED_COMPENSATION_VIOLATION` (INTEGRITY, sync, W1). Standard IC-TC-RESET applies to resume from such a trip; the forensic record carries `trip_reason: TC_COMPENSATION_OVER_SCOPE` (GAP-43 / GS11).

### 11.8.1.2 Reset Ceremony Under Orchestrator Degradation (GAP-24 / v3 GS5)

If the Orchestrator process is degraded — unable to route ceremony envelopes, crash-looped, or in an unresponsive control-plane state — the TC accepts IC-TC-RESET envelopes submitted via a **direct-to-TC channel** bypassing the Orchestrator's normal ceremony router. This is a narrow, operator-invoked pathway:

- Operator invokes the `tc_direct_reset` tool against the live TC process.
- The envelope is still a CeremonyToken structurally identical to the Orchestrator-routed form (§20), including full CAK signature and replay-rejection binding.
- The TC performs the full IC-TC-RESET admission order (§11.8.1) independent of the Orchestrator's routing state.
- The resulting `CIRCUIT_RESET` Ledger entry carries an `operator_routing_override: true` flag and a `degradation_reason` field authored by the operator.
- On successful reset, the Orchestrator is **not** automatically restarted; recovery of the Orchestrator control plane is a separate operational step.

This pathway exists to prevent an Orchestrator failure from creating an unrecoverable `CIRCUIT_TRIPPED` lockout. The CAK-verification requirement means the Orchestrator's control-plane state is not a security dependency of the reset ceremony itself. Tier 1 CAK anchor is the single root of trust for admission.

### 11.9 The Lock / Hold Split (T8)

Two distinct Orchestrator-managed concepts:

**Write Lock** — concurrent write prevention only:
- Acquired at task declaration (D59, C-CW3).
- 60-minute TTL with auto-release (D60, C-CW5).
- Blocks other agents from writing to the declared region.
- Released on task completion, abort, or TTL expiry.

**Dependency Hold** — dependency preservation across long-escalation tasks:
- Placed on specific edges the task is *reading* (its dependency set).
- 72-hour TTL, renewable on escalation events.
- Blocks Pruning on held edges only.
- Does not block other agents from acquiring Write Locks or writing novel facts.
- Released on task completion, abort, or TTL expiry.

Commit-time collision after declaration-time lock is a security incident (D61).

### 11.10 Escalation Phase Lock/Hold Behavior (T8)

| Escalation Step | Write Lock | Dependency Hold |
|---|---|---|
| Parent → Subtask Decomposition | Released if expired / transferred if within TTL | **Transferred** to subtasks, scoped per subtask |
| Peer Agent Review | **Renewed** (fresh 60 min) | **Renewed** (fresh 72 hrs) |
| Human Escalation Queue | **Released** | **Maintained**, auto-renewed while in `IN_HUMAN_QUEUE` |
| Logged Suspension | Released | Released |

**Task resume re-verification protocol:** when an escalated task resumes, Orchestrator compares current state of all held edges against the escalation-entry snapshot. `context_stale` (edge changed) → task repackaged with current state. `context_lost` (hold expired before resume) → task may be re-escalated with `dependency_reconstruction_required`.

### 11.11 Dependency Set Identification (T8)

Hybrid declaration model:
- Coder Agent declares initial dependency set as part of task-completion package (`declared_dependencies` field).
- Orchestrator extends the Dependency Hold automatically on observed reads (Agent Runtime Wrapper mediates all reads).

Sanity cap: no more than 10% of project edge count per task declaration. Soft cap, escalates to human review on exceedance.

### 11.12 Pruning Agent (D53–D57, extended T8, T10, GAP-11, T-PM-vs-PA)

- Pruning writes flow through the standard 2PC path. No fast-path (D53, C-PA1).
- Restricted to Structural and Knowledge family edges only (D54, C-PA2).
- Cannot touch Genesis tiers L1–L3 (C-PA3).
- Cannot delete edges younger than 24 hours (D56, C-PA5).
- **Cannot delete edges under active Dependency Hold** (T8, IC-PA7).

**Trigger conditions (D57):** every 50 commits or 24 hours; on source file deletion; on function rename detection; on out-of-band commit; on Session 4 D37 gap record followup; manual trigger.

**Backpressure (D55):** 24-hour staleness window; edges older than 24h classified `stale_urgent`. At 1,000 `stale_urgent`, writes suspended until Pruning completes.

**External source audit (GAP-11 / v3 GS9 — see §26).** The Pruning Agent runs a dedicated `external_source_audit` sub-routine over Layer 4 facts with external document provenance. For each Layer 4 fact carrying a provenance block, the sub-routine checks the referenced external document's declared staleness signals (fetch timestamp, content hash, publisher-declared version). Staleness does not trigger deletion — it produces an advisory entry on the Reconciliation Review Queue. Classification: advisory-only; operator acknowledgment required to resolve.

**Merged advisory queue policy (T-PM-vs-PA / GS11 — IC-REVIEW-QUEUE amended).** External-provenance staleness advisories merge into the existing review queue item for the same `edge_id`, rather than creating a separate queue item. CORE-importance facts with STALE or UNAVAILABLE external-document provenance receive priority elevation in the merged item. Both advisory reasons (Pruning's staleness signal and Provenance Monitor's external-document signal) MUST be acknowledged before the merged item can be resolved. Tension T-PM-vs-PA is closed by this policy.

### 11.13 Out-of-Band Git Reconciliation (D52, T10)

Humans or external tools may commit to Git outside the harness pipeline. Pruning Agent detects these and generates catch-up patches flagged `requires_human_review`. **No auto-compile.**

Catch-up patches route to the Reconciliation Review Queue (T10 IC-PA8, IC-OR10) — see §15.

### 11.14 Overlay Compaction (D62–D66, revised T9, extended D83, D86)

**Strategy:** full MEMIT re-run on active `.larql` patches. Delta composition is rejected on correctness grounds.

**Triggers (revised T9):** Compaction trigger evaluation uses the `drift_state` object exposed by the Write Engine (IC-WE-1, D83). Trigger conditions:
- Drift tier `WARNING` (edge count reaches warning threshold since last anchor): schedule at next idle window.
- Drift tier `HARD` (edge count reaches hard trigger): immediate, blocking writes.
- Time-based scheduler: every 30 days since last anchor.
- `drift_state.overlay_file_count` ≥ 50: schedule.
- `drift_state.p95_latency_ratio` ≥ 2.0 (p95 inference latency at 2× baseline): schedule.
- Manual.

All drift threshold values are provisional pending empirical validation (OQ-W1).

**Verification (D66, extended D86):** Behavioral Probe returns a structured `CompactionProbeReport` to the TC before Phase 2 commit (IC-OC-PROBE). Sampling: 100% of CORE edges (full), ≥20% of SUPPORTING edges (stratified, floor 5 probes), 10% of INCIDENTAL edges (stratified, floor 3 probes). Random seed logged for reproducibility. Abort thresholds: CORE pass rate MUST equal 1.0 (C-OC3 — any CORE failure is an immediate compaction abort); SUPPORTING ≥95%; INCIDENTAL ≥80%. Abort → existing overlays retained, `COMPACTION_ABORTED` Ledger entry with serialized `CompactionProbeReport` as payload. CORE failures individually listed; SUPPORTING and INCIDENTAL failures summary-logged unless ≤10 IDs.

Probe infrastructure failure → `COMPACTION_PROBE_FAILED` entry (distinct from `COMPACTION_ABORTED`). Both are distinguishable in the Ledger for operator diagnostics. All SUPPORTING and INCIDENTAL thresholds and sampling rates are provisional pending OQ-OC3 / OQ-W1 calibration. The CORE 1.0 threshold and C-OC3 are not provisional.

Genesis tiers never compacted (C-OC1). Compaction is a single atomic 2PC event (C-OC2).

### 11.15 State Ledger as the Unified Substrate

**The Ledger unifies what was previously specced as separate audit trail and State Ledger artifacts (T11).** All integrity-anchored event records — security, consistency, validation, governance, lifecycle — land in one log with audit-category tagging. See §16 for the full Ledger specification.

