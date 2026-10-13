# Gap Session 2 Summary — State Consistency Theorist
## LLM as Database: Agent Harness Architecture

> **Session:** Gap Session 2 of 8
> **Domain:** State Consistency Theorist (primary), Warden (co-review flagged)
> **Topic:** D84 / GAP-6 and D85 / GAP-7 Closure Verification
> **Baseline:** v1.1 Integrated Specification
> **Date:** Gap Session 2

---

## Session Scope

This session verified the v1.1 closures of GAP-6 and GAP-7 — the two High-priority
Transaction Controller completeness gaps. Both were closed in the Interface Contract Review
Session that produced v1.1 (D84 and D85 respectively). The session had four objectives:

1. Verify D84 (GAP-6) is complete: READ_ONLY mode, TC precondition verification per
   trip type, CIRCUIT_RESET placement in the W1/W2/W3 writer model, and Appendix C
   cataloguing
2. Verify D85 (GAP-7) is complete: two-value timeout model, Genesis timeout handling,
   internal consistency of the incremental vs. Genesis asymmetry
3. Surface any new tensions or gaps introduced by D84/D85 — specifically whether
   the operator-signed Hold release ceremony requires a new Ledger entry type
4. Define any residual gaps found

---

## Gaps Resolved

### GAP-6 — Circuit Breaker Reset Authority — CONFIRMED CLOSED

**Resolution:** D84 / §11.8.1 / IC-TC-RESET

The closure is complete and internally consistent. Specific confirmations:

- **READ_ONLY mode** is sufficiently defined: automatic on trip (no human action required),
  write token issuance suspended, reads and inference continue, Consistency Status API
  transitions to `CIRCUIT_TRIPPED`.
- **TC precondition verification** covers all three trip types correctly:
  - `CONSECUTIVE_FAILURE` / `CROSS_TASK_FAILURE`: compensation `COMPLETED` + overlay hash
    matches most recent `COMMITTED` entry.
  - `DIVERGED_STATE`: `RECONCILIATION_COMPLETE` with `result: 'CONSISTENT'` timestamped
    after the trip.
- **CIRCUIT_RESET placement** in W1/W2/W3 is correct. TC is a W1 writer; CIRCUIT_RESET
  is GOVERNANCE category, synchronous, Orchestrator-mediated. W3 path exclusion for reset
  is explicit and unambiguous.
- **Appendix C cataloguing** is complete: `CIRCUIT_RESET` (GOVERNANCE, sync),
  `CIRCUIT_RESET_REJECTED` (SECURITY, sync), `CIRCUIT_TRIPPED` (CONSISTENCY, sync) — all
  present with correct fields.

**Residual seam (not a reopening):** §11.8.1 does not explicitly exempt TC compensating
transactions from the write-token suspension that applies to READ_ONLY mode. Since TC
compensation is a TC-internal operation (not agent-initiated), this creates a silent
internal contradiction in the spec. One sentence resolves it (see Spec Amendments below).

---

### GAP-7 — PREPARED-State Timeout — CONFIRMED CLOSED

**Resolution:** D85 / §11.5.1 / IC-TC-TIMEOUT

The closure is complete at the policy level. Specific confirmations:

- **Two-value timeout model** is internally consistent and correctly handles the Genesis
  compile scenario from the original gap description. `genesis_prepared_timeout` has no
  default; C-GATE-2 blocks Genesis initiation if the value is absent. Operators are
  responsible for sizing to their target model and patch volume.
- **Incremental vs. Genesis asymmetry** is justified and sound:
  - *Incremental:* known-good `COMMITTED` overlay exists; rollback direction is
    unambiguous; retry is safe.
  - *Genesis:* no prior `COMMITTED` overlay to revert to; auto-compensation is undefined;
    circuit trip is the only coherent response.
- **Dependency Hold persistence** through timeout is correctly specced (§17.3): timeout
  does not release the Hold; release requires successful commit on retry or operator-signed
  ceremony.

**Residual seams (not reopenings):**
- `TIMED_OUT` Ledger entry carries a `compensation_direction` field that has no valid value
  for Genesis timeouts, where compensation is prohibited (GAP-21).
- The Dependency Hold lifecycle through the reset ceremony and into a fresh Genesis attempt
  is unspecced (GAP-22).

---

## Gaps Partially Resolved

None. Both closures are complete at the stated scope. Residual seams are catalogued as new
gaps, not as reopenings of GAP-6 or GAP-7.

---

## Gaps Deferred

None deferred in this session. All in-scope verification work completed.

---

## New Gaps Surfaced

### GAP-20 — DEPENDENCY_HOLD_RELEASED_SIGNED Entry Missing from Appendix C

**Domain:** State Consistency Theorist / Warden (co-review required)
**Priority:** 🟠 High

**Description:** §17.3 specifies that Dependency Hold release following a PREPARED-state
timeout requires an "operator-signed Hold release (GOVERNANCE category, signed ceremony)."
However, Appendix C's LIFECYCLE category lists only:

```
DEPENDENCY_HOLD_PLACED, _RENEWED, _RELEASED, _EXPIRED_UNCLAIMED
```

The `_RELEASED` entry represents automatic release on successful commit. It does not
distinguish automatic release from operator-signed release. These are fundamentally
different audit events:

- `_RELEASED` (automatic): system-internal event, no human authorization
- Operator-signed release: a governance act bypassing the normal commit-to-release path

An audit trail that cannot distinguish these two cases fails at the moment when the
distinction is most forensically significant — a human operator intervening in a hung
transaction.

**Proposed resolution:** New entry `DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE category,
synchronous), with fields: `hold_id`, `operator_id`, `operator_signature`,
`release_reason` (enum: `TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE`).

**Blocked by:** Policy decision on the `release_reason` enum values.

**Blocks:** GAP-22 (Genesis reset ceremony sequencing); complete audit trail for
PREPARED-state timeouts.

**⚑ WARDEN CO-REVIEW:** Before this entry type is ratified, the Warden must confirm:
(a) Is the absence of a signed Hold release entry currently a trust-boundary gap?
(b) Should TC independently verify `operator_signature` before writing, per the D84 pattern?

---

### GAP-21 — TIMED_OUT Entry `compensation_direction` Field Undefined for Genesis

**Domain:** State Consistency Theorist
**Priority:** 🟠 High

**Description:** `TIMED_OUT` (Appendix C, CONSISTENCY category) carries a
`compensation_direction` field. For Genesis PREPARED timeouts, §11.5.1 prohibits
auto-compensation. The field has no valid value in this case. Any deployed audit tool
parsing the Ledger will encounter a `TIMED_OUT` entry for Genesis that has either a
missing or meaningless `compensation_direction`.

**Three resolution paths:**

**(a) Make `compensation_direction` nullable.** Null is defined to mean "no compensation —
circuit trip follows." One-line schema amendment.

**(b) Add a `GENESIS_TIMED_OUT` entry type.** Separate entry for the Genesis case, without
the `compensation_direction` field. Cleaner semantically; adds Appendix C surface area.

**(c) Define a sentinel value convention.** E.g., `compensation_direction: "CIRCUIT_TRIP"`,
signaling "not applicable; circuit breaker is the resolution mechanism." Avoids schema
changes but requires convention documentation.

**Blocked by:** Decision on which resolution path to take.

**Blocks:** Complete `TIMED_OUT` entry type definition; audit tool correctness.

---

### GAP-22 — Genesis Hold Lifecycle Through Reset Ceremony Unspecced

**Domain:** State Consistency Theorist
**Priority:** 🟠 High

**Description:** After a Genesis PREPARED timeout, the circuit breaker trips and the
Dependency Hold from the failed Genesis transaction persists (§17.3). The reset ceremony
(IC-TC-RESET) defines preconditions for `DIVERGED_STATE` trips but does not address Hold
lifecycle. Three questions are unanswered:

1. **Is Hold release a precondition for the reset ceremony?** If yes, this must appear in
   IC-TC-RESET's precondition list. Currently it does not.
2. **Does `CIRCUIT_RESET` implicitly release all active Holds from the failed transaction?**
   If yes, this must be stated explicitly, and a `DEPENDENCY_HOLD_RELEASED_SIGNED` entry
   (GAP-20) must appear as part of or immediately after the reset.
3. **Can a new Genesis acquire a Hold while the failed Genesis's Hold is active?** If the
   old Hold still occupies the model parametric layer region, the new Genesis cannot acquire
   its own Hold.

**Latent deadlock scenario:** System enters WRITE_ENABLED post-reset, but a new Genesis is
blocked by the unreleased old Hold — requiring further operator intervention beyond what
the spec currently defines.

**Blocked by:** GAP-20 (the signed Hold release mechanism must exist before this sequencing
can be specced).

**Blocks:** Complete Genesis recovery path specification; fresh Genesis initiation after a
Genesis timeout event.

---

### GAP-23 — Reset Ceremony Failure Mode When Orchestrator Is Degraded

**Domain:** State Consistency Theorist / Warden (co-review required)
**Priority:** 🟡 Medium

**Description:** The reset ceremony writes `CIRCUIT_RESET` via the W1 (Orchestrator-mediated)
path. If the Orchestrator is degraded — not compromised (the W3 scenario) but degraded:
stalled, overloaded, or temporarily unreachable — the W1 write path is unavailable. The
spec defines no error path for "TC verified preconditions, operator signed, but W1 write
path unavailable." The system cannot transition from READ_ONLY to WRITE_ENABLED despite
satisfying all defined preconditions. The failure is silent from the Ledger's perspective:
no entry records the failed attempt.

**Blocked by:** Policy decision on how to classify Orchestrator degradation during a reset
ceremony: integrity violation (W3 path required) or operational failure (retry permitted).

**Blocks:** Complete reset ceremony specification; operator playbook for extended READ_ONLY
scenarios.

**⚑ WARDEN CO-REVIEW:** The Warden must confirm: is a degraded Orchestrator during a reset
ceremony an integrity violation class event (requiring W3 `INTEGRITY_VIOLATION_EMERGENCY`
logging) or an operational failure (retry after recovery)?

---

## New Tensions Surfaced

### T-NEW-1 — Circuit Breaker Workflow Cross-Category Split (documentation tension)

The circuit breaker workflow is correctly split across three Ledger categories:

| Entry | Category | Rationale |
|---|---|---|
| `CIRCUIT_TRIPPED` | CONSISTENCY | A consistency event: two mediums in problematic relationship |
| `CIRCUIT_RESET` | GOVERNANCE | A human governance act: authorized write resumption |
| `CIRCUIT_RESET_REJECTED` | SECURITY | A security signal: unauthorized or unverifiable reset attempt |
| `TIMED_OUT` | CONSISTENCY | A transaction consistency event |

The split is architecturally justified but undocumented. A future reader may reasonably
interpret it as a cataloguing error. Appendix C requires a one-line rationale annotation.

**This is a documentation tension, not a spec gap.** No new OQ required.

---

## Spec Amendments Recommended

### §11.8.1 Amendments

**A1 — TC Compensation Exemption from Write Token Suspension:**
> "TC compensating transactions initiated under READ_ONLY mode are exempt from write token
> suspension. Compensation is TC-internal and does not consume agent write tokens. The
> READ_ONLY constraint applies to agent-initiated write token issuance only."

*Closes the internal contradiction between "write token issuance suspended" and the TC's
own need to execute compensation writes.*

**A2 — Precondition Check Error Handling:**
> "Precondition check errors — system failure during verification, as distinct from
> precondition check failures where the state is known — are treated as precondition
> failures. The reset ceremony is rejected and `CIRCUIT_RESET_REJECTED` is written."

*Closes the edge case of unverifiable preconditions (e.g., overlay hash comparison fails
because the overlay is in an unreadable state).*

### Appendix C Amendments Required

| ID | Amendment | Dependency |
|---|---|---|
| C1 | Add `DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE, sync) | GAP-20 resolution + Warden co-review |
| C2 | Amend `TIMED_OUT` definition for Genesis `compensation_direction` | GAP-21 path selection |
| C3 | Add cross-category rationale annotation for circuit breaker workflow entries | T-NEW-1 — documentation only |

### Interface Contracts Requiring Amendment

| Contract | Amendment Required | Dependency |
|---|---|---|
| IC-TC-RESET | Add Hold release sequencing language | GAP-22 resolution |
| IC-TC-TIMEOUT | Note Genesis `compensation_direction` field handling | GAP-21 resolution |

---

## Net Gap Count

| | Count |
|---|---|
| Gaps entering session | 2 (GAP-6, GAP-7) — confirmed closed in v1.1 |
| Gaps resolved | 2 |
| New gaps surfaced | 4 (GAP-20, GAP-21, GAP-22, GAP-23) |
| Net change | +4 gaps added to backlog |

Priority breakdown of new gaps: 3 High (GAP-20, GAP-21, GAP-22), 1 Medium (GAP-23).
All four are residual seams from the D84/D85 closures — they are not reopenings of GAP-6
or GAP-7.

**Recommended sequencing for Gap Session 3:** GAP-20 first. It unblocks GAP-22, and its
Warden co-review requirement means it should enter the AISecOps Specialist's queue promptly.
GAP-21 can proceed in parallel (no external dependencies).

---

*Gap Session 2 Summary — State Consistency Theorist*
*v1.1 baseline — 4 new gaps catalogued, 2 closures verified*
