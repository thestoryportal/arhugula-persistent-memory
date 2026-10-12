# Gap Session 3 Summary — AISecOps Specialist
## LLM as Database: Agent Harness Architecture

> **Session:** Gap Session 3 of 8
> **Domain:** AISecOps Specialist (The Warden) — primary
> **Topic:** GAP-5 Closure Audit — Write Scope Definition Mid-Flight Update Model (D87)
> **Baseline:** v1.1 Integrated Specification
> **Supplementary:** GAP-20 Warden Co-Review (flagged by Gap Session 2)
> **Status:** Draft

---

## Session Scope

This session audited the v1.1 closure of GAP-5 (D87: mid-flight scope update model).
Five audit tasks were completed:

1. Verify the `SCOPE_UPDATED` Ledger entry → registry update sequencing is race-condition-free
2. Audit the three-consecutive `SCOPE_HASH_MISMATCH` escalation rule
3. Audit the infrastructure failure classification of `SCOPE_HASH_MISMATCH` for rate-limit
   exploit surface
4. Determine whether `affected_agent_ids` is sufficient for proactive agent notification
5. Surface any new gaps introduced by D87

Supplementary: Address the two GAP-20 Warden co-review questions from Gap Session 2.

---

## GAPS RESOLVED

### GAP-5 — Write Scope Definition Mid-Flight Update Model — VERIFIED CLOSED (with residuals)

**Resolution:** D87 / §10.9 / §14.3 / IC-SCOPE-UPDATE

The core of D87 is sound and the attack surface named in the original gap description
is closed. Specific confirmations:

- The `SCOPE_HASH_MISMATCH` error code correctly distinguishes scope rejections from generic
  infrastructure failures. Retry budget is correctly not consumed.
- The `current_scope_hash` + `scope_updated_at` error payload provides the Orchestrator
  with sufficient information to re-issue a correct token without a polling round trip.
- Active PREPARED transactions are correctly not interrupted by scope updates — forward-only
  semantics are sound for PREPARED state, which already has a committed scope at PREPARE time.
- `SCOPE_UPDATED` Ledger-first ordering prevents the specific race named in the original gap:
  the registry is never updated without a prior Ledger record.

**Residual seams (not reopenings — catalogued as new gaps GAP-24 through GAP-27):**

| Seam | Nature | New Gap |
|---|---|---|
| Ledger → registry propagation lag unspecced | Consistency hole on Orchestrator failure | GAP-24 |
| Ceremony authorization model unspecced | Trust boundary gap in `operator_signature` | GAP-25 |
| No rate limit on `SCOPE_UPDATED` events | Recovery-loop denial-of-service surface | GAP-26 |
| Orchestrator proactive notification obligation unspecced | Operational efficiency gap | GAP-27 |

---

## GAPS PARTIALLY RESOLVED

None. GAP-5 is confirmed closed at the level D87 targeted. Residual seams are new gaps,
not partial closures of GAP-5.

---

## GAPS DEFERRED

None. All session-scope items were addressed.

---

## NEW GAPS SURFACED

---

### GAP-24 — Ledger → Registry Propagation Window Unspecced

| Field | Value |
|---|---|
| **Domain(s)** | State Consistency Theorist (primary), Warden (co-owner) |
| **Priority** | 🟠 High |

**Description:** D87 requires `SCOPE_UPDATED` to be written to the Ledger before the
Orchestrator's in-memory scope registry is updated. The spec does not define:

- The maximum allowed propagation lag between Ledger write and registry update.
- What happens if the Orchestrator crashes or stalls between writing the Ledger entry and
  updating the registry. In this failure state, the Ledger records a scope update that the
  Gate is not enforcing — the Ledger is authoritative but the enforcement mechanism diverges.
- How a restarting Orchestrator detects and resolves a persisted `SCOPE_UPDATED` entry that
  was never reflected in the registry during the prior session.

**Security consequence:** During the propagation window, old-scope tokens may pass Gate
step 4 while the Ledger has already recorded a scope change. These patches are technically
authorized under the scope definition that was in effect at Gate evaluation time, but the
Ledger record may create an audit ambiguity: was the write authorized under the pre-update
or post-update scope?

**Blocked by:** State Consistency Theorist specification of Ledger → in-memory state
reconciliation behavior on Orchestrator restart.

**Blocks:** Complete trust boundary guarantee for D87; GAP-24 is a latent consistency hole
in the D87 closure that becomes a security gap only on Orchestrator failure.

---

### GAP-25 — Scope Update Ceremony Authorization Model Unspecced

| Field | Value |
|---|---|
| **Domain(s)** | Warden |
| **Priority** | 🟠 High |

**Description:** D87 specifies that scope updates require "a signed ceremony plus
`expected_yaml_hash` update" and that `SCOPE_UPDATED` carries `operator_signature`.
The spec does not define:

- Which entity or entities are permitted to initiate a scope update ceremony.
- The signing key the initiating entity uses and its relationship to the Orchestrator's
  own signing key.
- The Gate's verification procedure for confirming that the ceremony was authorized by a
  permitted entity — not merely that a structurally valid signature is present.

Without this model, `operator_signature` is an unverified assertion. The Gate cannot
distinguish a legitimately authorized ceremony from a forged or replayed one.

**Physical storage contract for ceremony authorization key material:**

| Field | Status |
|---|---|
| Storage medium | Unspecced — must be specified (OQ-S-GAP25-1) |
| Governance tier | Human-approved-change (operator-only key; no autonomous orchestrator modification) |
| Retention rule | Unspecced — must be specified (OQ-S-GAP25-2) |
| Write authority | Human operator only, out-of-band to the harness |

**Blocked by:** A decision on ceremony initiator identity hierarchy and key management model.

**Blocks:** Complete `SCOPE_UPDATED` Ledger entry trust model; GAP-26 (rate limit design
requires knowing who can trigger a ceremony before specifying how often they can do so).

**Open questions logged:**

- `OQ-S-GAP25-1`: Where is the operator signing key for scope update ceremonies stored,
  and under what physical storage contract? (Must satisfy the four-field physical storage
  contract requirement from the Warden skill.)
- `OQ-S-GAP25-2`: What is the retention policy for operator signing key material — rotation
  cadence, archival on rotation, destruction ceremony?
- `OQ-S-GAP25-3`: Can the Orchestrator's existing signing key (generated at first boot,
  §10.5) serve as the ceremony authorization key, or must scope update ceremonies use a
  separate human-held key? (The answer has implications for whether a compromised Orchestrator
  can authorize its own scope changes.)

---

### GAP-26 — No Rate Limit on `SCOPE_UPDATED` Events

| Field | Value |
|---|---|
| **Domain(s)** | Warden (primary), State Consistency Theorist (Ledger entry type co-ownership) |
| **Priority** | 🟠 High |

**Description:** The spec does not constrain the frequency at which Write Scope Definitions
may be updated. Repeated scope update ceremonies — whether caused by a misconfigured process
or a compromised operator account — exploit the infrastructure failure classification of
`SCOPE_HASH_MISMATCH` (which does not consume retry budget) to keep agent tokens permanently
invalid. This is a targeted denial-of-service against specific agent invocations that does
not trigger any existing detection mechanism.

**Required additions:**

1. `scope_update_min_interval_seconds` — operator-configurable Tier 1 config value.
   Provisional default: 3,600 seconds. MUST NOT be modifiable by the Orchestrator autonomously.
2. `SCOPE_UPDATE_RATE_EXCEEDED` — SECURITY-category Ledger entry (synchronous), written when
   a ceremony is rejected for rate violation. Required fields: `agent_id`,
   `requesting_operator_id`, `last_update_at`, `interval_elapsed_seconds`,
   `min_interval_required_seconds`.
3. Rate limit check MUST occur before signature verification in ceremony processing sequence.

**Spec block produced in session:** See `IC-SCOPE-RATE-1` below.

**Blocked by:** GAP-25 (ceremony authorization model — must know the authorized initiator
before constraining their frequency).

**Blocks:** Closure of the recovery-loop denial-of-service attack surface identified in
Audit Point 3.

**Open questions logged:**

- `OQ-S-GAP26-1`: Provisional default value of 3,600 seconds for `scope_update_min_interval_seconds`
  requires operational validation. What is the realistic frequency of legitimate scope updates
  in long-running projects?
- `OQ-S-GAP26-2`: Should the rate limit be per-`agent_id` or global across all agents?
  Per-agent limits prevent targeted attacks on individual agents; global limits prevent
  system-wide scope update flooding.

---

### GAP-27 — Orchestrator Proactive Notification Obligation Unspecced

| Field | Value |
|---|---|
| **Domain(s)** | Orchestration Comparativist (primary), Warden (secondary) |
| **Priority** | 🟡 Medium |

**Description:** When a scope-narrowing update occurs (permissions removed from a Write Scope
Definition), agents listed in `affected_agent_ids` will have their next token rejected at Gate
step 4. The spec does not define whether the Orchestrator MUST, SHOULD, or MAY proactively
notify or cancel these invocations before they complete computations and submit tokens that
will be rejected.

Gate-discovery is sufficient for correctness: no out-of-scope write executes. However, for
scope-narrowing changes, an agent may complete a full computation cycle producing a `.larql`
patch targeting entities it can no longer write to — wasting compute time and requiring
a fresh invocation.

**Scope-update type dependency:**
- Scope-expanding updates (permissions added): gate-discovery is sufficient; proactive
  notification adds no security or correctness value.
- Scope-narrowing updates (permissions removed): proactive notification prevents wasted
  computation; however it is an efficiency concern, not a trust-boundary requirement.

The `affected_agent_ids` field in `SCOPE_UPDATED` is sufficient for forensic/audit purposes.
The gap is the missing specification of what the Orchestrator is obligated to do with that
information in real time.

**Blocked by:** Orchestration path selection (GAP-4 — Path A/B/C determines the available
invocation cancellation mechanisms).

**Blocks:** Operational efficiency spec for mid-flight scope changes; long-running invocation
behavior under scope-narrowing events.

**Open questions logged:**

- `OQ-OR-GAP27-1`: Should `SCOPE_UPDATED` carry a `scope_change_type` field
  (`EXPANDING | NARROWING | RESTRUCTURING`) to enable the Orchestrator to apply different
  notification policies per update type?

---

## NEW TENSIONS SURFACED

### T-NEW-2 — Ceremony Authorization vs. Orchestrator Key Hierarchy

**Domain boundary:** Warden (ceremony authorization model) ↔ State Consistency Theorist
(Orchestrator restart and key recovery)

**Competing requirements:**

- **Warden requires:** Scope update ceremonies must be authorized by a human-held key that
  is distinct from the Orchestrator's own signing key (§10.5, first-boot generated). If the
  Orchestrator key doubles as the ceremony authorization key, a compromised Orchestrator can
  self-authorize scope changes — eliminating the human gate.
- **State Consistency Theorist implication:** If ceremony authorization requires a human-held
  key separate from the Orchestrator's key, Orchestrator restart scenarios (GAP-24) must
  specify how the restarting Orchestrator re-establishes its relationship with the ceremony
  authorization key without autonomous access to it. Restart recovery cannot be fully
  automated if ceremony authorization is locked to human key custody.

```
IC-PENDING: T-NEW-2 (Ceremony Authorization vs. Orchestrator Key Hierarchy)
Requires resolution with: Warden + State Consistency Theorist
Warden must provide: Whether ceremony authorization key must be separate from
  the Orchestrator's first-boot key, and the physical storage contract for that key.
State Consistency Theorist must provide: How Orchestrator restart re-establishes
  scope registry state when the authoritative key is human-held and the last
  SCOPE_UPDATED entry predates the restart.
Status: Open. Unresolved tension introduced by GAP-25 analysis.
```

---

## SUPPLEMENTARY: GAP-20 WARDEN CO-REVIEW (Gap Session 2 Pending Item)

**Question (a): Is the absence of a signed Hold release entry currently a trust-boundary gap?**

**Warden finding: Yes — confirmed trust-boundary gap.**

`DEPENDENCY_HOLD_RELEASED` (automatic) and an operator-signed Hold release must produce
distinct Ledger entries. An automatic Hold release is a system-internal event requiring no
human authorization. An operator-signed release is a governance act: a human overrides the
normal commit-to-release path and manually resolves a hung transaction.

An audit trail that collapses these into a single entry type fails at the moment forensic
distinction is most critical — post-incident investigation of a stalled or incorrectly
terminated transaction. The absence of `DEPENDENCY_HOLD_RELEASED_SIGNED` as a distinct
GOVERNANCE-category entry is a trust-boundary gap. GAP-20 resolution priority is confirmed
as 🟠 High.

**Question (b): Should the TC independently verify `operator_signature` before writing
`DEPENDENCY_HOLD_RELEASED_SIGNED`, per the D84 pattern?**

**Warden finding: Yes — consistent with D84 pattern.**

TC must verify the operator signature is structurally valid and corresponds to a known
operator key before writing `DEPENDENCY_HOLD_RELEASED_SIGNED`. If verification fails, TC
MUST write `HOLD_RELEASE_REJECTED` (SECURITY category, synchronous) instead of the signed
release entry. This mirrors the `CIRCUIT_RESET_REJECTED` pattern from D84 precisely.

Every governance act requiring operator authorization has a corresponding rejection entry
for failed or unverifiable authorization attempts. `HOLD_RELEASE_REJECTED` must be added
to Appendix C alongside `DEPENDENCY_HOLD_RELEASED_SIGNED`.

**Impact on GAP-20 resolution path:** The proposed `release_reason` enum
(`TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE`) is confirmed as
correctly scoped. TC signature verification is now a hard requirement before the entry is
written. Warden co-review is satisfied; GAP-20 may proceed to resolution.

---

## DECISIONS MADE

| ID | Decision |
|---|---|
| **D88** (Provisional) | `SCOPE_HASH_MISMATCH` escalation threshold reduced from **three** to **two** consecutive mismatches for the same `invocation_id`. First mismatch is expected (scope update in transit). Second mismatch confirms Orchestrator did not apply the correct hash from the error payload — this is the earliest diagnostic signal of malfunction. |
| **D89** (Provisional) | A minimum interval `scope_update_min_interval_seconds` (provisional default: 3,600 seconds) MUST be enforced between consecutive `SCOPE_UPDATED` events for the same `agent_id`. Ceremonies within the minimum interval are rejected before Ledger write. |
| **D90** (Provisional) | `operator_signature` in `SCOPE_UPDATED` is a **verified** field, not an unverified assertion. Gate / Orchestrator MUST validate the signature against a declared ceremony authorization key before writing the entry. Ceremony without a verifiable signature MUST be rejected. |
| **D91** (Provisional) | Warden confirms: `DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE, synchronous) is a required distinct Ledger entry type. `HOLD_RELEASE_REJECTED` (SECURITY, synchronous) is a required companion entry. TC MUST independently verify operator signature before writing `DEPENDENCY_HOLD_RELEASED_SIGNED`. |

*All D-IDs above are provisional, pending ratification. The last confirmed decision in the
gap session arc was D87 (v1.1 integrated spec).*

---

## CONSTRAINTS ESTABLISHED

| ID | Constraint |
|---|---|
| **C-S-GAP26-1** | `scope_update_min_interval_seconds` MUST be a Tier 1 operator config value (human-approved-change governance tier). The Orchestrator MUST NOT modify this value autonomously. |
| **C-S-GAP26-2** | Rate limit check MUST occur before signature verification in scope update ceremony processing. A rate-exceeded rejection does not require evaluating ceremony authorization. |
| **C-S-GAP25-1** | Ceremony authorization key MUST be distinct from the Orchestrator's first-boot signing key (§10.5). An Orchestrator-held key MUST NOT serve as the ceremony authorization key without explicit human-attended enrollment. |

---

## INTERFACE CONTRACTS DEFINED

```
IC-SCOPE-RATE-1:
  From: Orchestrator (ceremony processor)
  To: State Ledger
  What it exposes: SCOPE_UPDATE_RATE_EXCEEDED (SECURITY, synchronous) on rate rejection
  Conditions: Ceremony initiated within scope_update_min_interval_seconds of last
              SCOPE_UPDATED entry for the same agent_id
  Failure behavior: If Ledger write fails during rate rejection, ceremony processing
                    halts; no scope update proceeds; Orchestrator surfaces write failure
                    to ceremony initiator; no partial state is written
```

```
IC-SCOPE-AUTH-1:
  From: Scope Update Ceremony Processor
  To: Orchestrator (scope registry)
  What it exposes: Verified-signature ceremony result; registry update authorization
  Conditions: operator_signature verified against declared ceremony authorization key;
              rate limit check passed; SCOPE_UPDATED Ledger entry written successfully
  Failure behavior: Signature failure → ceremony rejected; SCOPE_UPDATED not written;
                    registry not updated; rejection payload returned to initiator
```

```
IC-HOLD-RELEASE-SIGNED-1:
  From: TC (DEPENDENCY_HOLD_RELEASED_SIGNED writer)
  To: State Ledger
  What it exposes: DEPENDENCY_HOLD_RELEASED_SIGNED (GOVERNANCE, synchronous) on
                   successful operator-signed Hold release; HOLD_RELEASE_REJECTED
                   (SECURITY, synchronous) on signature failure
  Conditions: TC verifies operator_signature against known operator key before writing;
              release_reason must be one of: TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION
              | OPERATOR_OVERRIDE
  Failure behavior: Signature verification failure → HOLD_RELEASE_REJECTED written;
                    Hold remains active; operator receives rejection with reason
```

---

## NEW LEDGER ENTRY TYPES REQUIRED

| Entry Type | Category | Mode | Producing Component |
|---|---|---|---|
| `SCOPE_UPDATE_RATE_EXCEEDED` | SECURITY | Synchronous | Orchestrator (ceremony processor) |
| `SCOPE_MISMATCH_ESCALATED` | SECURITY | Synchronous | Orchestrator (on 2nd consecutive mismatch) |
| `DEPENDENCY_HOLD_RELEASED_SIGNED` | GOVERNANCE | Synchronous | TC |
| `HOLD_RELEASE_REJECTED` | SECURITY | Synchronous | TC |

All four must be added to Appendix C of the v1.1 integrated spec.

---

## SPEC AMENDMENTS RECOMMENDED

### §14.3 Amendment — Escalation Threshold

Replace: "Three consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation →
Orchestrator escalates to human review queue."

With: "Two consecutive `SCOPE_HASH_MISMATCH` errors for the same `invocation_id` →
Orchestrator escalates to human review queue and writes `SCOPE_MISMATCH_ESCALATED`
(SECURITY, synchronous). 'Consecutive' is defined as: two Gate step-4 rejections for the
same `invocation_id` with no successful token issuance interleaved between them. (D88)"

### §10.9 Amendment — Ceremony Authorization Verification

Add after "operator_signature" field definition: "The Orchestrator MUST verify
`operator_signature` against the declared ceremony authorization key before writing the
`SCOPE_UPDATED` Ledger entry. A ceremony with an unverifiable signature MUST be rejected;
no `SCOPE_UPDATED` entry is written; no registry update occurs. (D90, C-S-GAP25-1)"

### §10.9 Amendment — Rate Limiting

Add: "A scope update ceremony MUST be rejected if the elapsed time since the previous
`SCOPE_UPDATED` entry for the same `agent_id` is less than `scope_update_min_interval_seconds`
(Tier 1 operator config; provisional default 3,600 seconds). Rejection produces a
`SCOPE_UPDATE_RATE_EXCEEDED` Ledger entry (SECURITY, synchronous). Rate limit check MUST
precede signature verification in processing order. (D89, C-S-GAP26-1, C-S-GAP26-2)"

---

## OPEN QUESTIONS CARRYING FORWARD

| ID | Question | Blocked By |
|---|---|---|
| `OQ-S-GAP24-1` | Maximum allowed propagation lag between `SCOPE_UPDATED` Ledger write and registry update — is this specifiable without implementation data? | State Consistency Theorist / GAP-24 |
| `OQ-S-GAP24-2` | On Orchestrator restart, what is the prescribed procedure for detecting and replaying unprocessed `SCOPE_UPDATED` entries from the Ledger? | GAP-24 / State Consistency Theorist |
| `OQ-S-GAP25-1` | Physical storage contract for ceremony authorization key material (storage medium + governance tier + retention rule + write authority) | GAP-25 resolution |
| `OQ-S-GAP25-2` | Retention policy and rotation cadence for operator signing key material | GAP-25 resolution |
| `OQ-S-GAP25-3` | Must ceremony authorization key be separate from Orchestrator first-boot key (§10.5)? | D90 implementation planning; T-NEW-2 |
| `OQ-S-GAP26-1` | Operational validation of `scope_update_min_interval_seconds` provisional default (3,600 seconds) | Operational experience |
| `OQ-S-GAP26-2` | Should rate limit be per-`agent_id` or global across all agents? | Operational environment and threat model |
| `OQ-S-GAP27-1` | Should `SCOPE_UPDATED` carry `scope_change_type: EXPANDING \| NARROWING \| RESTRUCTURING` to enable per-type Orchestrator notification policy? | GAP-27 / Orchestration Comparativist |
| `OQ-S-GAP3-1` (carry-forward) | If the Gate does not include a schema version check in pre-checks, does a replayed legacy-schema patch bypass Validator checks added in newer versions? | GAP-3 / GAP-25 (both address trust boundary gaps in Gate pre-check completeness) |

---

## ⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED

```
Trigger: Condition 1 — decisions affecting what is recorded in the State Ledger
         (new entry types added: SCOPE_UPDATE_RATE_EXCEEDED, SCOPE_MISMATCH_ESCALATED,
         DEPENDENCY_HOLD_RELEASED_SIGNED, HOLD_RELEASE_REJECTED)
         Condition 3 — decision C-S-GAP25-1 specifies that ceremony authorization
         key material must be stored outside Orchestrator-managed config, which
         implies a new physical storage placement that intersects config governance.

Decision that triggered it (Condition 1): D89 / D90 / D91 introduce four new
  Ledger entry types. Appendix C schema must be extended. The SCOPE_UPDATE_RATE_EXCEEDED
  entry must carry fields that reference both agent_id and operator identity — the
  State Consistency Theorist must confirm these fields do not create implicit
  foreign-key expectations that complicate Ledger append-only semantics.

Decision that triggered it (Condition 3): C-S-GAP25-1 places ceremony authorization
  key material in human-controlled storage outside the harness. The State Consistency
  Theorist must specify how Orchestrator startup reconciles the Ledger's scope update
  history with a registry that may have diverged during the prior session (GAP-24).

Specific question for State Consistency Theorist:
  (a) What is the reconciliation procedure when Orchestrator startup detects
      one or more SCOPE_UPDATED Ledger entries timestamped after the registry's
      last known state? Is this a DIVERGED_STATE condition (triggering circuit breaker),
      an automatic replay, or a separate reconciliation path?
  (b) Do the four new Ledger entry types (SCOPE_UPDATE_RATE_EXCEEDED,
      SCOPE_MISMATCH_ESCALATED, DEPENDENCY_HOLD_RELEASED_SIGNED, HOLD_RELEASE_REJECTED)
      require any additions to the Merkle-chain-lite integrity structure beyond
      standard append-only entry chaining?
```

---

## NET GAP COUNT

| | Count |
|---|---|
| Gaps entering session | 1 (GAP-5) — targeted for closure verification |
| Gaps confirmed closed | 1 (GAP-5, at D87 scope — with residuals catalogued separately) |
| New gaps surfaced | 4 (GAP-24, GAP-25, GAP-26, GAP-27) |
| Net change | +4 gaps added to backlog |

Priority breakdown of new gaps: 3 High (GAP-24, GAP-25, GAP-26), 1 Medium (GAP-27).

**Supplementary:** GAP-20 Warden co-review satisfied. GAP-20 may proceed to resolution
(GAP-22 sequencing — unblocked). `HOLD_RELEASE_REJECTED` added as required companion entry.

---

## RECOMMENDED SEQUENCING FOR GAP SESSION 4

1. **GAP-25 first** (Warden) — ceremony authorization model is a prerequisite for GAP-26
   rate limit design and partially informs T-NEW-2. The four physical storage contract fields
   for ceremony key material must be answered.
2. **GAP-24 second** (State Consistency Theorist / Warden co-owned) — Ledger → registry
   propagation model. Feeds the State Consistency Theorist review flagged above.
3. **GAP-26** follows GAP-25 (depends on ceremony authorization model for per-entity vs.
   global rate limit decision).
4. **GAP-20** (State Consistency Theorist + Warden) — Warden co-review now satisfied;
   State Consistency Theorist can proceed to close GAP-20 and unblock GAP-22.

---

*Gap Session 3 Summary — AISecOps Specialist (The Warden)*
*v1.1 baseline — 4 new gaps catalogued, 1 closure verified, GAP-20 co-review satisfied*
