# Gap Session 3 Summary — AISecOps Specialist (GAP-5 Verification)

**Session type:** Gap resolution, verification pass
**Primary skill:** aisecops-specialist (Warden)
**Baseline spec:** v1.1 (GAP-5 closed by D87 and IC-SCOPE-UPDATE, §10.9)
**Session number:** 3 of 8 (gap schedule v3)

---

## Session scope

Verification of whether D87's mid-flight scope update model closes the GAP-5 attack surface airtight, and audit of the three-consecutive-`SCOPE_HASH_MISMATCH` escalation rule, the infrastructure-failure classification, and the sufficiency of `affected_agent_ids` for Orchestrator recovery.

---

## GAPS RESOLVED

**GAP-5 — Scope update ceremony for long-running projects**
*Status: closure verified with caveats; three follow-on refinements required.*

D87's mid-flight update model is structurally sound. The Ledger-entry-before-registry-update sequencing correctly places the durable source of truth ahead of the in-memory enforcement point, and the `SCOPE_HASH_MISMATCH` error code with structured payload gives the Orchestrator enough information to recover without consuming agent retry budget. The closure is verified on these axes:

- Mid-flight update model does not require draining in-flight invocations. Correct: drain-first would create a liveness problem for long-running projects with frequent governance updates, and forward-only scope changes mean PREPARED transactions can safely complete under the scope they were validated against.
- Infrastructure-failure classification correctly isolates `SCOPE_HASH_MISMATCH` from Coder Agent correctness failures. Retry budget is reserved for correctness retries.
- Orchestrator re-issuance against `current_scope_hash` from the error payload is the correct recovery pattern.
- Three-consecutive escalation rule does provide a safety net against Orchestrator misbehavior, though the threshold is too lenient (see refinements below).

Closure carries three refinements and one unstated assumption that requires cross-domain confirmation — captured as new gaps G-S3-N1 through G-S3-N5.

---

## GAPS PARTIALLY RESOLVED

None. GAP-5 is verified-closed; the refinements are new gaps rather than partial closures of GAP-5 itself.

---

## GAPS DEFERRED

None in this session.

---

## NEW GAPS SURFACED

### G-S3-N1 — Ledger concurrency semantics during SCOPE_UPDATED write

**Domain:** Security (Warden), State Consistency
**Description:** D87's airtightness depends on an unstated assumption that the Ledger is single-writer serialized, OR that SCOPE_UPDATED entries acquire an exclusive write barrier against commit entries for affected scopes. If neither holds, a race exists where a patch validated under OLD scope can commit with its Ledger entry interleaved after SCOPE_UPDATED, producing an audit trail where a commit appears under NEW scope that was never validated against it. The v1.1 spec implicitly assumes single-writer serialization but does not state this explicitly as a contract requirement for the Ledger.
**Blocked by:** State Consistency Theorist decision on Ledger concurrency model.
**Blocks:** Complete airtightness proof for D87; any subsequent security argument that depends on Ledger ordering.
**Priority:** High

### G-S3-N2 — PREPARED transaction scope-governance forensic gap

**Domain:** Security (Warden), State Consistency
**Description:** §10.9 permits active PREPARED transactions to proceed past a scope update without interruption. The PREPARED transaction was validated under the OLD scope and will commit under the OLD scope, but the commit Ledger entry does not currently carry a reference to which scope hash governed it. Post-update, forensic queries cannot unambiguously determine which scope governed a given commit when the commit and the SCOPE_UPDATED entry occupy adjacent Ledger positions. Fix: commit Ledger entries must carry `governing_scope_hash` field, set at PREPARE time, preserved through COMMIT.
**Blocked by:** Minor schema change to commit Ledger entry.
**Blocks:** Complete audit trail for scope transition boundaries.
**Priority:** Medium

### G-S3-N3 — Cross-invocation SCOPE_HASH_MISMATCH aggregate detection

**Domain:** Security (Warden)
**Description:** The current three-consecutive rule is scoped to a single invocation, which means an attacker can avoid tripping escalation by spreading mismatches across many invocations (trigger scope update, allow 1–2 invocations to succeed, trigger another update, repeat). A time-windowed aggregate metric is required: N SCOPE_HASH_MISMATCH events across all invocations within M seconds triggers Warden alert. Suggested starting values for specification discussion: N=10, M=60s. Aggregate metric is distinct from per-invocation threshold and is in addition to it, not a replacement.
**Blocked by:** Spec decision on aggregate threshold values and alert pathway.
**Blocks:** Complete detection model for scope-update abuse patterns.
**Priority:** Medium

### G-S3-N4 — Scope update rate limiting and burst detection

**Domain:** Security (Warden)
**Description:** Nothing in the current spec prevents rapid successive scope updates, which constitutes a governance-induced DoS vector. Even with retry budget unconsumed, wall-clock session budget and operational cost burn linearly with scope update frequency, and in-flight agents may never complete. Recommendation: introduce a ceremony-level rate limit (suggested minimum 60s between SCOPE_UPDATED events for the same scope) enforced by the Warden's ceremony signing layer upstream of the Ledger write. Additionally, burst detection: 3+ scope updates for the same scope within 300s freezes scope update authority pending human investigation.
**Blocked by:** Spec decision on rate-limit parameters and freeze protocol.
**Blocks:** Defense against governance-induced DoS; completion of scope update threat model.
**Priority:** High

### G-S3-N5 — Reactive-vs-proactive notification model ambiguity

**Domain:** Security (Warden), Orchestration
**Description:** The spec is silent on whether the Orchestrator must proactively notify agents listed in `affected_agent_ids` or whether agents discover scope updates reactively via Gate rejection. Implementations will diverge. Warden recommendation: reactive discovery is authoritative; proactive notification is OPTIONAL optimization. Spec language required:
> Agents MUST discover scope updates via Gate rejection (SCOPE_HASH_MISMATCH). The Orchestrator MAY use `affected_agent_ids` to proactively invalidate cached token state, but agents MUST NOT depend on proactive notification for correctness. The authoritative signal is Gate rejection.

`affected_agent_ids` field's primary role is forensic (post-hoc queries), not operational.
**Blocked by:** Spec decision on notification authority.
**Blocks:** Orchestrator capability requirements (affects T-S3-N2).
**Priority:** Medium

---

## NEW TENSIONS SURFACED

### T-S3-N1 — Warden ↔ State Consistency Theorist: Ledger ordering underpins D87

The D87 closure implicitly depends on Ledger write ordering and durability semantics that are in the State Consistency Theorist's domain. The Warden can specify that a barrier is required between SCOPE_UPDATED and affected commit entries, but cannot unilaterally specify the Ledger's concurrency model. Resolution of G-S3-N1 and G-S3-N2 is a joint decision.

### T-S3-N2 — Warden ↔ Orchestration Comparativist: push-based invalidation channel

Whether the Orchestrator needs a push channel for scope invalidation is an orchestration capability question. The Warden's recommendation in G-S3-N5 (reactive baseline, proactive optional) softens this tension by not making push a hard requirement, but it still factors into orchestrator evaluation — candidates that support push natively have a minor advantage for operational efficiency, though not for security correctness.

---

## REFINEMENTS TO EXISTING DECISIONS

Three refinements to v1.1 language are recommended. These are not new gaps; they are tightenings of existing text.

**R-S3-1 — Tighten escalation threshold from 3 to 2 consecutive SCOPE_HASH_MISMATCH per invocation.**
Rationale: if the Orchestrator correctly reads `current_scope_hash` from the first error payload, the first retry should always succeed. A second consecutive mismatch indicates Orchestrator bug, attack, or cache coherency failure — none of which improve with a third retry. The first mismatch logs INFO; the second logs SECURITY at escalation time. (Distinct from G-S3-N3, which concerns cross-invocation aggregation.)

**R-S3-2 — Make Ledger single-writer serialization (or equivalent barrier) an explicit contract requirement in the section describing SCOPE_UPDATED.**
Rationale: closes the race identified in G-S3-N1 by stating the assumption that D87 already depends on. Joint decision with State Consistency Theorist.

**R-S3-3 — Add `governing_scope_hash` field to commit Ledger entries, set at PREPARE time, preserved through COMMIT.**
Rationale: closes the forensic ambiguity in G-S3-N2 for PREPARED transactions that span a scope-update boundary.

---

## ⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED

**Trigger:** Conditions 1, 2, and 3 all fire.
1. Decision affects what gets recorded in the Ledger (new `governing_scope_hash` field on commit entries per R-S3-3; explicit SCOPE_UPDATED ordering contract per R-S3-2).
2. Decision affects how Ledger entries are structured (field addition, serialization contract).
3. Decision specifies governance semantics for config artifacts (scope update rate limiting per G-S3-N4 specifies when SCOPE_UPDATED may be written).

**Specific questions for State Consistency Theorist:**
- Is the Ledger currently specified as single-writer serialized, or does it permit concurrent writes with ordering? If the latter, does SCOPE_UPDATED need an exclusive barrier against commit entries for `affected_agent_ids` scope space, and what is the barrier mechanism?
- Is adding `governing_scope_hash` to commit Ledger entries consistent with the existing commit entry schema and the Ledger's append-only / immutable-downward guarantees? The field must be set at PREPARE time; does the PREPARE → COMMIT handoff preserve the field without mutation?
- For the ceremony-level rate limit in G-S3-N4: does the Ledger need a corresponding record (e.g., SCOPE_UPDATE_REJECTED entry) when a ceremony attempt is rejected for rate-limit violation, or is ceremony-level rejection outside the Ledger scope?

---

## INTERFACE CONTRACTS TOUCHED

**IC-SCOPE-UPDATE** — Referenced, not modified in this session. Three refinements (R-S3-1, R-S3-2, R-S3-3) recommend changes to v1.1 §10.9 and §14.3 text but are deferred to the integration pass where they will be reconciled against the State Consistency Theorist's Ledger spec.

No new Interface Contracts introduced.

---

## CARRY-FORWARD TO NEXT SESSION

Inputs to the next gap session:
- G-S3-N1 and G-S3-N2 require State Consistency Theorist resolution — schedule appropriately if a state-consistency-owned gap session is upcoming.
- G-S3-N4 (rate limiting) and G-S3-N3 (aggregate detection) are Warden-owned and can be resolved in a follow-on security gap session or folded into the v1.2 integration pass.
- R-S3-1 through R-S3-3 are refinement-level edits queued for integration, not blockers for subsequent gap sessions.
- T-S3-N1 should be flagged on the tension map (v2 → v3 update).
- T-S3-N2 should be folded into the orchestration-tools-requirements matrix as a soft requirement (push-based invalidation: OPTIONAL, not required).
