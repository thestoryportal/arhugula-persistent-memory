# Gap Session 5 Summary — State Consistency + Warden

**Session:** GS5 (Gap Schedule v3)
**Primary skills:** State Consistency Theorist (primary), Warden (co-owner)
**Baseline:** v1.1 integrated spec
**Prerequisite for:** GS6 (GAP-23, Genesis reset ceremony)

---

## Scope

Discharges the A1-REVISED and A8 amendment obligations from the post-GS3 council checkpoint, and resolves GAPs 21, 24, and 25. GAP-21 resolution unblocks GS6.

---

## Amendments Applied

### A1-REVISED — Bounded Compensation Under READ_ONLY

Resolves INCON-1, D-CRC-3, C-CRC-3.

**§11.8.1.1 — Bounded Compensation Under READ_ONLY (NEW)**

While the circuit is tripped (READ_ONLY mode), the TC retains compensating-transaction authority per §11.7 for completing in-flight 2PC operations. This authority is bounded to reversal-only semantics:

(a) A compensation write MUST produce exactly the inverse of a specifically identified prior committed operation, referenced by Ledger entry ID.

(b) A compensation write that would produce any weight change beyond the reversal of the prior committed operation MUST be rejected and treated as a TC fault, triggering an additional circuit trip event (category: CONSISTENCY, subtype: `BOUNDED_COMPENSATION_VIOLATION`).

(c) The TC verifies the proposed compensation patch against the target entry's `content_delta` before issuing the write token. If the patch's semantic effect cannot be verified as the strict inverse of `target_entry.content_delta`, the write is rejected.

(d) Rejected compensation attempts produce a `COMPENSATION_REJECTED` entry (SECURITY, synchronous) recording: `target_entry_id`, `rejection_reason`, `proposed_patch_hash`.

(e) No other write path is available under READ_ONLY mode, including W3 emergency escalation. The only writes permissible are (i) bounded compensation per this section, and (ii) `CIRCUIT_RESET` via W1 after the reset ceremony completes.

**Warden confirmation:** The bounded path does not create a write surface under READ_ONLY. Compensation is strictly the inverse of an already-committed, already-audited state transition; no new information can enter parametric memory via this path. Violation attempts are themselves observable SECURITY-category events that force a second trip, guaranteeing that any attempted escape is louder than the original fault.

---

### A8 — Cross-Category Rationale Annotation (Appendix C preamble)

**Circuit Breaker Workflow — Cross-Category Rationale (NEW preamble block):**

Entries associated with the circuit breaker lifecycle span CONSISTENCY, GOVERNANCE, and SECURITY categories by design. This is not a taxonomy inconsistency; each category carries distinct audit semantics that the workflow requires simultaneously.

- **CONSISTENCY** entries record machine-detected state conditions (trip triggers, divergence detection, reconciliation results). Produced by the TC without operator involvement; describe the system's internal integrity posture.
- **GOVERNANCE** entries record human-authorized state transitions that change what the system will accept next (`CIRCUIT_RESET`, `CIRCUIT_RESET_ATTEMPT`, `DEPENDENCY_HOLD_RELEASED_SIGNED`, `SCOPE_RECONCILIATION_COMPLETE`). Require valid `operator_signature` (for operator-initiated ceremonies) or represent a TC/Orchestrator-signed state transition. Follow the signed ceremony pattern where applicable.
- **SECURITY** entries record rejected attempts at governance-category operations and bounded-authority violations (`CIRCUIT_RESET_REJECTED`, `HOLD_RELEASE_REJECTED`, `COMPENSATION_REJECTED`, `CIRCUIT_RESET_ATTEMPT_ABANDONED`, `SCOPE_RECONCILIATION_FAILED`). A rejected governance operation is a trust-boundary event worth independent forensic surfacing.

Audit reconstruction of a circuit-breaker incident requires joining across all three categories by `target_trip_entry_id`, `target_hold_entry_id`, `ceremony_id`, or `target_attempt_id`. These foreign-key-style references are contract, not convention.

---

## Gaps Resolved

### GAP-21 — RESOLVED

**Interface contract IC-HOLD-RELEASE-SIGNED-1 ratified** as proposed in GS3.

**`release_reason` enum — DECIDED:**

| Value | Meaning |
|---|---|
| `TIMEOUT_NO_RETRY` | PREPARED-state timeout with no retry planned; operator accepts Hold release. |
| `GENESIS_RESET_PREPARATION` | Hold released as part of clearing state for a Genesis reset ceremony. Reserved for GS6 / GAP-23 consumption. |
| `OPERATOR_OVERRIDE` | Other operational justification. **MUST** include non-empty `justification_text` field. |

**Appendix C additions (v1.2):**

```
DEPENDENCY_HOLD_RELEASED_SIGNED (GOVERNANCE, synchronous)
  Fields: target_hold_entry_id, operator_id, operator_signature,
          release_reason ∈ {TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION |
                            OPERATOR_OVERRIDE},
          justification_text (required iff release_reason = OPERATOR_OVERRIDE)
  Written by: TC, after independent operator_signature verification.
  Effect: Hold terminated; recorded as operator-authorized release. Distinct
          from automatic DEPENDENCY_HOLD_RELEASED (LIFECYCLE) emitted on
          successful commit.

HOLD_RELEASE_REJECTED (SECURITY, synchronous)
  Fields: target_hold_entry_id, operator_id,
          rejection_reason ∈ {SIGNATURE_INVALID | OPERATOR_NOT_AUTHORIZED |
                              RELEASE_REASON_INVALID | MISSING_JUSTIFICATION |
                              TARGET_HOLD_NOT_FOUND |
                              TARGET_HOLD_ALREADY_RELEASED}
  Written by: TC on signature or precondition failure.
  Effect: Hold remains active; operator receives rejection with reason.
```

**Downstream:** GAP-21 resolution unblocks GAP-23 (Genesis reset ceremony, GS6). `GENESIS_RESET_PREPARATION` is now a reserved `release_reason` value awaiting ceremony definition.

---

### GAP-24 — RESOLVED

**Classification:** A stalled, overloaded, or temporarily unreachable Orchestrator during a reset ceremony, **absent indicators of compromise**, is an **operational failure**, not an integrity violation. W3 escalation is NOT authorized for this condition. Attempted W3 invocation to propagate a reset under Orchestrator degradation is itself a Warden-observable event.

**Rationale:** W3 is restricted per §16.2 to `INTEGRITY_VIOLATION_EMERGENCY` with a rate ceiling of one entry per minute per component. Stalling, overload, and transient unreachability do not constitute evidence of compromise. Over-invoking W3 would dilute its emergency-only semantics and habituate operators to last-resort escalation. The system remains in READ_ONLY mode during the failure window — no weight mutations accrue, and bounded compensation (per A1-REVISED) is the only write surface, sealed to reversal-only.

**§11.8.1.2 — Reset Ceremony Under Orchestrator Degradation (NEW)**

(a) Degradation absent compromise indicators is classified as operational failure. W3 not authorized.

(b) On W1 unavailability during a signed reset ceremony, the TC writes `CIRCUIT_RESET_ATTEMPT` (GOVERNANCE, synchronous) recording `target_trip_entry_id`, `operator_id`, `operator_signature`, `preconditions_verified`, `ceremony_id`. This entry is a distinct audit record and does NOT flip circuit state.

(c) On Orchestrator restoration, the TC confirms acknowledgment of the pending attempt and writes `CIRCUIT_RESET` (with `source_attempt_id` back-reference). Circuit state flips at `CIRCUIT_RESET`, not at `CIRCUIT_RESET_ATTEMPT`.

(d) If the Orchestrator does not recover within an operator-configurable retry window (numeric default deferred, see Deferred Gaps), the TC writes `CIRCUIT_RESET_ATTEMPT_ABANDONED` (SECURITY, synchronous). The ceremony is invalidated; operator must re-sign a fresh ceremony to retry.

(e) **Hard availability requirement.** The TC's Ledger-write capability MUST remain functional whenever the TC is functional and the Ledger substrate is reachable. The Ledger-write path is independent of W1 weight-write availability. This is promoted from architectural assumption to explicit invariant.

(f) If Orchestrator degradation is accompanied by any indicator of compromise (signature mismatches attributed to the Orchestrator, unauthorized scope changes detected by the Gate, or W3 rate exceedance from any component), classification escalates to `INTEGRITY_VIOLATION_EMERGENCY` and W3 becomes available per §16.2 — **for integrity response, not for completing the paused reset ceremony**. The paused ceremony is discarded; a fresh ceremony must follow post-incident reconciliation.

**Appendix C additions (v1.2):**

```
CIRCUIT_RESET_ATTEMPT (GOVERNANCE, synchronous)
  Fields: target_trip_entry_id, operator_id, operator_signature,
          preconditions_verified, ceremony_id
  Written by: TC via direct Ledger-write (W1-independent).
  Note: Records ceremony initiation under W1 unavailability. Does NOT flip
        circuit state. Resolved by subsequent CIRCUIT_RESET (success) or
        CIRCUIT_RESET_ATTEMPT_ABANDONED (timeout/cancel).

CIRCUIT_RESET_ATTEMPT_ABANDONED (SECURITY, synchronous)
  Fields: target_attempt_id,
          abandonment_reason ∈ {W1_UNAVAILABLE_TIMEOUT | OPERATOR_CANCELLED |
                                CEREMONY_STALE}
  Written by: TC.
  Effect: Ceremony invalidated; circuit remains tripped; re-signing required.

COMPENSATION_REJECTED (SECURITY, synchronous)  [introduced by A1-REVISED]
  Fields: target_entry_id, rejection_reason, proposed_patch_hash
  Written by: TC.
  Effect: Triggers additional circuit trip event
          (subtype: BOUNDED_COMPENSATION_VIOLATION).
```

---

### GAP-25 — RESOLVED

**Reconciliation decision:** Automatic replay on Orchestrator restart. The Ledger is the authoritative source of scope state; the in-memory scope registry is a derived view. A `SCOPE_UPDATED` entry persisted in the Ledger but not reflected in the registry is a **known reconciliation condition**, not a diverged state — unless replay itself fails, in which case it IS a DIVERGED_STATE trigger.

**§10.9.1 — Scope Registry Reconciliation on Orchestrator Restart (NEW)**

(a) On every Orchestrator start or restart, the Orchestrator MUST enter `SCOPE_RECONCILIATION` state and is prohibited from issuing write tokens until reconciliation completes.

(b) The Orchestrator loads the Ledger's `SCOPE_UPDATED` history from the most recent registry checkpoint forward (or from genesis if no checkpoint exists) and rebuilds the in-memory registry chronologically.

(c) Each replayed entry produces a `SCOPE_REPLAY_APPLIED` Ledger entry (LIFECYCLE, asynchronous) recording `source_scope_updated_entry_id` and the resulting registry version.

(d) On completion, the Orchestrator writes `SCOPE_RECONCILIATION_COMPLETE` (GOVERNANCE, synchronous) with `final_registry_version` and the list of replayed entry IDs. The TC does NOT permit write-token issuance until this entry is observed. Absence of `SCOPE_RECONCILIATION_COMPLETE` after an Orchestrator restart is treated as `DIVERGED_STATE` per §11.8.

(e) If replay encounters an unapplicable entry (schema mismatch, unresolvable scope reference, cryptographic mismatch), the Orchestrator HALTS reconciliation and writes `SCOPE_RECONCILIATION_FAILED` (SECURITY, synchronous). This **IS** a `DIVERGED_STATE` trigger and trips the circuit.

(f) **Authority invariant.** A `SCOPE_UPDATED` entry persisted in the Ledger is authoritative: if registry and Ledger disagree about current scope, **the Ledger wins**. The registry is a derived view. This aligns with the uniform Ledger-authoritative pattern already applied to circuit state and Hold state.

**§10.9.2 — Scope Propagation Bound (NEW)** — OQ-S-GAP24-1 partially closed

(a) Each Orchestrator deployment MUST declare a `max_scope_propagation_lag_ms` parameter. Absence is a deployment configuration error and MUST block system startup.

(b) The TC monitors observed propagation lag per `SCOPE_UPDATED` entry: the delta between `SCOPE_UPDATED` write-timestamp and the next confirmed registry-version observation from the Orchestrator.

(c) The spec does NOT fix a universal numeric bound. The bound is a deployment-tier parameter; fixing a universal number without measurement data would be premature and would encode an unverified performance assumption into the spec.

(d) **Single breach:** `SCOPE_PROPAGATION_DEGRADED` (CONSISTENCY, asynchronous) — observability only, does NOT trip the circuit.

(e) **Sustained breach** (3 consecutive breaches within an operator-configured rolling window): `SCOPE_PROPAGATION_SUSTAINED_DEGRADATION` (CONSISTENCY, synchronous) — IS a circuit-breaker trip trigger under D48.

**OQ-S-GAP24-1: PARTIALLY CLOSED** — semantic contract fully specified; numeric default deferred to deployment configuration with mandatory observability and sustained-breach trip.

**OQ-S-GAP24-2: CLOSED** — restart reconciliation protocol fully specified in §10.9.1.

**Appendix C additions (v1.2):**

```
SCOPE_REPLAY_APPLIED (LIFECYCLE, asynchronous)
  Fields: source_scope_updated_entry_id, resulting_registry_version
  Written by: Orchestrator during reconciliation.

SCOPE_RECONCILIATION_COMPLETE (GOVERNANCE, synchronous)
  Fields: final_registry_version, replayed_entry_ids (list),
          reconciliation_duration_ms
  Written by: Orchestrator at reconciliation completion.
  Effect: TC permits resumption of write-token issuance for this Orchestrator.

SCOPE_RECONCILIATION_FAILED (SECURITY, synchronous)
  Fields: source_scope_updated_entry_id,
          failure_reason ∈ {SCHEMA_MISMATCH | SCOPE_UNRESOLVED |
                            CRYPTOGRAPHIC_MISMATCH},
          partial_registry_version
  Written by: Orchestrator.
  Effect: DIVERGED_STATE trigger per §11.8; circuit trips.

SCOPE_PROPAGATION_DEGRADED (CONSISTENCY, asynchronous)
  Fields: source_scope_updated_entry_id, measured_lag_ms, configured_max_ms
  Written by: TC.

SCOPE_PROPAGATION_SUSTAINED_DEGRADATION (CONSISTENCY, synchronous)
  Fields: degraded_entry_ids (list), rolling_window_ms, configured_max_ms
  Written by: TC.
  Effect: Circuit-breaker trip trigger under D48.
```

---

## Cross-Domain Integrations

**Ledger substrate as hard availability invariant.** §11.8.1.2(e) promotes "TC Ledger-write capability is independent of W1" from an architectural assumption to an explicit availability requirement. Warden concurs: this is a trust-boundary invariant, not merely a reliability target. Deployment tooling must enforce.

**Authority hierarchy for scope state uniform with prior invariants.** GAP-25 establishes Ledger > registry. This aligns with the existing pattern (Ledger authoritative for circuit state, Hold state, PREPARED-state metadata). State Consistency Theorist confirms this is a uniform project invariant, not a GAP-25 novelty — the resolution clarifies an existing principle for a new state surface.

**W3 sealed against liveness escalation.** GAP-24 explicitly forbids W3 for propagating a reset under Orchestrator degradation. W3 responds to integrity emergencies, not liveness failures. This narrows W3 authority in a way that protects its scarce-signal semantics.

**A1-REVISED + GAP-24 jointly close READ_ONLY.** Under the circuit-tripped state, the complete write surface is now: (i) reversal-only compensation, with overshoot producing a second trip; (ii) `CIRCUIT_RESET_ATTEMPT` / `CIRCUIT_RESET` via W1 after operator-signed ceremony; (iii) Ledger-only audit entries via the W1-independent Ledger path. No other writes permitted. No W3.

---

## GAPS RESOLVED

- **GAP-21** — IC-HOLD-RELEASE-SIGNED-1 ratified; `release_reason` enum = `{TIMEOUT_NO_RETRY, GENESIS_RESET_PREPARATION, OPERATOR_OVERRIDE}`; `DEPENDENCY_HOLD_RELEASED_SIGNED` added to GOVERNANCE; `HOLD_RELEASE_REJECTED` added to SECURITY. **Unblocks GS6 / GAP-23.**
- **GAP-24** — Stalled Orchestrator classified as operational failure; W3 not authorized; `CIRCUIT_RESET_ATTEMPT` (GOVERNANCE) and `CIRCUIT_RESET_ATTEMPT_ABANDONED` (SECURITY) added; TC Ledger-write availability declared W1-independent as hard requirement; compromise-indicator escalation path specified.
- **GAP-25** — Automatic replay on Orchestrator restart; Ledger authoritative for scope; `SCOPE_RECONCILIATION_FAILED` is a DIVERGED_STATE trigger; `SCOPE_RECONCILIATION_COMPLETE` required before TC permits write-token resumption; `SCOPE_PROPAGATION_SUSTAINED_DEGRADATION` is a D48 trip trigger.
- **OQ-S-GAP24-2** — fully closed by §10.9.1.

## GAPS PARTIALLY RESOLVED

- **OQ-S-GAP24-1** — semantic contract and observability contract closed; numeric `max_scope_propagation_lag_ms` default deferred to deployment configuration, with mandatory presence enforced at system startup.

## GAPS DEFERRED

- **Retry-window numeric default for `CIRCUIT_RESET_ATTEMPT_ABANDONED` timeout** (§11.8.1.2(d)). Specified as operator-configurable; numeric default not fixed in spec. Deferred to operator playbook work — not an architectural gap.
- **Registry checkpoint format and cadence** (§10.9.1(b)). Implementation-level; deferred.

## NEW GAPS SURFACED

- **GAP-26 (LOW, State Consistency Theorist).** Recursive-fault semantics: if the target trip of a `CIRCUIT_RESET` is itself a `BOUNDED_COMPENSATION_VIOLATION` (TC faulted during compensation), operator signing a reset re-enters a system whose last fault was the TC violating its own bounded authority. Whether this requires a stricter reset ceremony, an additional verification step, or a Warden-specific sign-off is unspecified. Defer to GS7 or later.
- **GAP-27 (LOW, State Consistency Theorist, Warden).** Scope reconciliation §10.9.1 does not specify behavior if two Orchestrators (HA pair) attempt concurrent reconciliation of overlapping `SCOPE_UPDATED` ranges. HA topology is out of scope for v1.1. Defer to a future HA spec track.

## NEW TENSIONS SURFACED

- **T-GS5-1 (resolved in session).** Ledger-authoritative scope (GAP-25) vs. Gate-enforces-from-registry. Resolution: bounded propagation window with sustained-breach trip. Not a persistent tension; documented as normal operating behavior, observable via `SCOPE_PROPAGATION_DEGRADED`.
- **T-GS5-2 (resolved in session).** W3-as-last-resort (Warden) vs. system-liveness-during-ceremony (State Consistency). Resolution: W3 sealed for liveness failures; operational retry path via `CIRCUIT_RESET_ATTEMPT` + `CIRCUIT_RESET_ATTEMPT_ABANDONED` preserves audit completeness without W3 escalation. Compromise-indicator escalation path separately preserved.

## ARTIFACTS UPDATED

- **§11.8.1.1** (new) — Bounded Compensation Under READ_ONLY (A1-REVISED).
- **§11.8.1.2** (new) — Reset Ceremony Under Orchestrator Degradation (GAP-24).
- **§10.9.1** (new) — Scope Registry Reconciliation on Orchestrator Restart (GAP-25).
- **§10.9.2** (new) — Scope Propagation Bound (GAP-25).
- **Appendix C preamble** — Circuit Breaker Workflow: Cross-Category Rationale (A8).
- **Appendix C** — 10 new entries: `DEPENDENCY_HOLD_RELEASED_SIGNED`, `HOLD_RELEASE_REJECTED`, `COMPENSATION_REJECTED`, `CIRCUIT_RESET_ATTEMPT`, `CIRCUIT_RESET_ATTEMPT_ABANDONED`, `SCOPE_REPLAY_APPLIED`, `SCOPE_RECONCILIATION_COMPLETE`, `SCOPE_RECONCILIATION_FAILED`, `SCOPE_PROPAGATION_DEGRADED`, `SCOPE_PROPAGATION_SUSTAINED_DEGRADATION`.

## BASELINE PROMOTION

Changes aggregate to a spec version bump: **v1.1 → v1.2 pending integration pass.** Integration work is mechanical (no further cross-domain decisions required from this session).

## NEXT SESSION

**GS6 — GAP-23 (Genesis reset ceremony).** GAP-21 resolution unblocks. GS6 will consume `DEPENDENCY_HOLD_RELEASED_SIGNED` with `release_reason = GENESIS_RESET_PREPARATION` as the ceremony's Hold-clearing mechanism.
