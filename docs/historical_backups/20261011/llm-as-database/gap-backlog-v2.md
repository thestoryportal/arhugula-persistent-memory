# LLM as Database: Agent Harness Architecture
## Gap Backlog v2.0

> **Source document:** `llm-as-database-v1_1-integrated-spec.md` (v1.1 Integrated Specification)
> **Session:** Framework Council — Post-Gap Sessions 1–3 Checkpoint
> **Supersedes:** `gap-backlog-v1.md`
> **Scope:** All gaps from v1 backlog, updated with GS1–GS3 closure status, plus all new gaps
> introduced in GS1–GS3 with canonical IDs established.
> **Total gaps tracked:** 28 — 3 Critical, 12 High, 7 Medium, 4 Low, 2 New Tensions (T13, T14)

---

## ⚠️ Numbering Note

Gap backlog v1 contained 19 gaps (GAP-1 through GAP-19). Gap Sessions 1–3 introduced 9 new
gaps. A naming collision occurred: Gap Session 1 labeled its new gap "GAP-21" while Gap
Session 2 independently labeled its first new gap "GAP-20" and its second "GAP-21" — two
different gaps sharing one ID. Gap Session 3 continued from Gap Session 2's numbering without
knowledge of Gap Session 1's assignment.

**This document establishes canonical IDs.** Session order is used to resolve priority
(Gap Session 1 ran before Gap Session 2 and takes the first post-backlog slot):

| Canonical ID | Was Labeled In | Source Session |
|---|---|---|
| GAP-20 | GS1 "GAP-21" | Gap Session 1 |
| GAP-21 | GS2 "GAP-20" | Gap Session 2 |
| GAP-22 | GS2 "GAP-21" | Gap Session 2 |
| GAP-23 | GS2 "GAP-22" | Gap Session 2 |
| GAP-24 | GS2 "GAP-23" | Gap Session 2 |
| GAP-25 | GS3 "GAP-24" | Gap Session 3 |
| GAP-26 | GS3 "GAP-25" | Gap Session 3 |
| GAP-27 | GS3 "GAP-26" | Gap Session 3 |
| GAP-28 | GS3 "GAP-27" | Gap Session 3 |

GS2 and GS3 session summary documents use pre-canonical numbering. They should be annotated
accordingly; their content is correct, only the IDs require mapping via this table.

---

## Priority Definitions

| Priority | Criteria |
|----------|----------|
| **Critical** | Blocks 3 or more other gaps |
| **High** | Blocks 1–2 other gaps or is a load-bearing architectural decision |
| **Medium** | Self-contained gap with no downstream spec dependencies |
| **Low** | Refinement detail; does not affect other components |

---

## Status Labels

| Status | Meaning |
|--------|---------|
| **Open** | Not yet addressed |
| **Partial** | Partially closed; residuals remain |
| **Resolved** | Fully closed; no remaining action |
| **Deferred** | Explicitly deferred with rationale |
| **Blocked** | Cannot proceed until a named dependency is resolved |

---

## 🔴 Critical — Blocks 3 or More Other Gaps

---

### GAP-1

**Domain(s):** MEMIT Specialist
**Priority:** 🔴 Critical
**Status:** Open — blocked by implementation phase

**Description:** All drift-from-anchor and compaction threshold values are provisionally
specified but empirically unvalidated (OQ-W1). Values include:
- Drift warning: 1,500 edges since last anchor (§11.14, §8.7)
- Drift hard trigger: 8,000 edges (§11.14)
- MEMIT internal sub-batch ceiling: 2,000 edges (§8.8)
- Overlay file count trigger: 50+ files (§11.14)
- p95 inference latency trigger: 2× baseline (§11.14)
- `stale_urgent` backpressure ceiling: 1,000 edges (§11.12)
- 24-hour Pruning floor (§17.5) — rationale is architectural; floor value is heuristic

**Blocked by:** Target model selection + at least one write-volume stress test against that
model's FFN architecture during the implementation phase.

**Blocks:** GAP-9 (OQ-OC3: compaction verification sample size), concrete backpressure
policy, meaningful circuit-breaker threshold rationale, any write-budget SLA spec.

**Council note (GS1-3 checkpoint):** GAP-1 feeds T13 directly — the hard-block threshold
for `LARQL_VERSION_LEGACY` accumulation (100 patches per v2 outline spec block 2c) has no
empirical basis until GAP-1 is resolved. The council recommends formal deferral of GAP-1 to
the implementation phase, with an explicit deferral rationale recorded here:

> **Formal deferral:** GAP-1 cannot be resolved through specification work alone.
> Resolution requires empirical testing against a selected target model. All threshold
> values in the current spec are explicitly marked provisional (OQ-W1). This deferral does
> not block spec work; it blocks implementation-phase calibration only.

---

### GAP-2

**Domain(s):** MEMIT Specialist
**Priority:** 🔴 Critical
**Status:** Open — blocked by implementation phase

**Description:** MEMIT's compatibility with the target model architecture has not been
verified (OQ-W2). Layer coordinates (L15–L25 for a 32-layer model), FFN width assumptions,
and architectural variant compatibility (MoE, Mamba-family, grouped-query attention) are
all unverified for the actual target model.

**Blocked by:** Explicit target model specification + MEMIT compatibility test run.

**Blocks:** Layer targeting spec correctness, edge cap justification, GAP-1 resolution,
`attention_weight` divergence check meaningfulness.

**Council note (GS1-3 checkpoint):** Same deferral rationale as GAP-1 applies.

> **Formal deferral:** GAP-2 requires empirical compatibility testing and cannot be resolved
> through specification work. Resolution requires target model selection followed by a MEMIT
> compatibility probe run. All layer coordinates are explicitly provisional.

---

### GAP-3

**Domain(s):** MEMIT Specialist, Graph Data Architect
**Priority:** 🔴 Critical
**Status:** 🔶 Partial — gate enforcement confirmed closed; three v2 residuals have outline
spec blocks; GAP-20 is a new dependency

**Description (original):** The `.larql` schema versioning strategy is deferred to v2
(OQ-W6, §18.3). Issues include: Validator handling of older-schema patches, `.larql` schema
version header field, superseded-patch archive handling during compaction, and migration path
for active patches when schema version advances.

**Gap Session 1 progress (GS1):**
- Gate enforcement layer confirmed closed (D82, pre-check #8, `larql_migration_manifest`
  in §8.10 and §13.2 form a sound enforcement chain).
- Three v2 outline spec blocks produced: migration manifest authorship ceremony (2a),
  deprecation ceremony and notice period policy (2b), `LARQL_VERSION_LEGACY` advisory window
  policy (2c).
- Decisions D-GAP1-A through D-GAP1-D ratified.
- New dependency: GAP-20 (manifest format unspecified) must be resolved before spec blocks
  2a and 2c can be fully instantiated.

**Remaining v2 residuals:**
- (a) T1 translation fidelity: bucket boundary thresholds for float-to-enum mapping
  (≥0.75 CORE / 0.50–0.74 SUPPORTING / <0.50 INCIDENTAL) deferred for v2 ratification
  (depends on GAP-1).
- (b) Compaction abort recovery for translation failure: partially outlined in 2a; recovery
  path for `COMPACTION_TRANSLATION_HEAVY` failures requires full spec.
- (c) Advisory accumulation escalation: three-tier model outlined in 2c; hard-block threshold
  (100 patches) is provisional, requires T13 resolution.
- (d) Pre-T5 sub-gap: schema extension proposal pathway for agents to propose new relation
  types remains unspecced.

**Blocks:** Complete Gate pre-check spec (§10.2), Validator L1 static analysis completeness,
compaction re-run strategy for superseded patches, v2 migration planning, T13 resolution.

---

## 🟠 High — Blocks 1–2 Gaps or Load-Bearing Architectural Decisions

---

### GAP-4

**Domain(s):** Orchestration Comparativist
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS1–3

**Description:** Orchestration path selection (Path A / B / C) is operator-decided with no
spec recommendation (D72). Downstream: (a) nested sub-agent delegation token design is
path-dependent; (b) human-in-the-loop interface mechanism is path-dependent.

**Blocked by:** Operator path selection.
**Blocks:** Delegation token v2 spec shape; HIL interface mechanism spec.

---

### GAP-5

**Domain(s):** Warden, MEMIT Specialist
**Priority:** 🟠 High
**Status:** ✅ Resolved — D87 / §10.9 / §14.3 / IC-SCOPE-UPDATE (Gap Session 3)

**Resolution summary:** `SCOPE_HASH_MISMATCH` correctly classifies scope rejections vs.
infrastructure failures. `current_scope_hash + scope_updated_at` error payload is sufficient.
PREPARED transactions use forward-only semantics. `SCOPE_UPDATED` Ledger-first ordering
prevents the race named in the original gap. Four new gaps (GAP-25 through GAP-28) are
residual seams, not reopenings.

---

### GAP-6

**Domain(s):** State Consistency Theorist
**Priority:** 🟠 High
**Status:** ✅ Resolved — D84 / §11.8.1 / IC-TC-RESET (Gap Session 2)

**Resolution summary:** READ_ONLY mode correctly defined; TC precondition verification
covers all three trip types; CIRCUIT_RESET placement in W1/W2/W3 is correct and unambiguous;
Appendix C cataloguing is complete. Amendment A1 required (TC compensation bounded to
reversal-only — council inconsistency finding). GAP-23 through GAP-24 are residual seams.

**⚠️ Council amendment required:** A1 as written in GS2 must be strengthened. The exemption
of TC compensation from write-token suspension must explicitly bound compensation to strict
reversal of the prior committed write. See Section 1 council verdict.

---

### GAP-7

**Domain(s):** State Consistency Theorist
**Priority:** 🟠 High
**Status:** ✅ Resolved — D85 / §11.5.1 / IC-TC-TIMEOUT (Gap Session 2)

**Resolution summary:** Two-value timeout model (incremental vs. Genesis) is internally
consistent. Genesis circuit-trip rationale is sound. Dependency Hold persistence through
timeout is correctly specced. GAP-22, GAP-23 are residual seams.

---

### GAP-8

**Domain(s):** Validation Contract Architect
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS1–3

**Description:** Corpus authorship policy for Meta-Validator and Meta-TGA held-out corpora
is unspecced (OQ-V5). The Meta-Validator fires every 50 commits; if corpus authorship is
not established before the first 50 commits, the first Health Score is meaningless.

**Blocked by:** Operational deployment planning.
**Blocks:** Meta-Validator and Meta-TGA operational readiness.

---

### GAP-20
*(canonical; was labeled "GAP-21" in Gap Session 1 summary)*

**Domain(s):** MEMIT Specialist, Graph Data Architect
**Priority:** 🟠 High
**Status:** Open

**Description:** The `larql_migration_manifest` is named as a Tier 1 config artifact
(§8.10, §13.2) and the versioned patch parser (D82) is specified to consume it. The format
of a manifest entry — fields, structure of translation rules, how bucket decisions are
expressed — is completely unspecified. The parser-manifest interface contract IC-MANIFEST-1
exists as a proposal only (GS1 session output) and is subject to v2 ratification.

**Proposed resolution path:** Ratify IC-MANIFEST-1 as a v1.2 patch (does not require full
v2 work). Requires resolution of the bucket boundary decision (GAP-3 residual (a)) before
the `bucket_map` field in IC-MANIFEST-1 can be fully specified.

**Blocks:** Manifest authorship ceremony spec (GAP-3 spec block 2a), compaction recovery
path spec (GAP-3 spec block 2a), bucket boundary resolution for T1 translation.

**Open questions:**
- `OQ-GAP1-1`: Should manifest authorship allow Architect Agent involvement (with human
  ratification), or is it fully outside the agent authorization model?
- `OQ-GAP1-2`: Should a test compaction ("manifest dry-run") on a sample of legacy patches
  be mandatory before manifest ratification?

---

### GAP-21
*(canonical; was labeled "GAP-20" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist, Warden
**Priority:** 🟠 High
**Status:** Open — Warden co-review satisfied (GS3); State Consistency Theorist resolution
pending

**Description:** `DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE, synchronous) is missing
from Appendix C. The existing `DEPENDENCY_HOLD_RELEASED` entry represents automatic release
on successful commit. It does not distinguish automatic release from operator-signed release.
These are fundamentally different audit events — the distinction is most forensically
significant precisely at the moment a human operator intervenes in a hung transaction.

**Warden co-review finding (GS3):** (a) The absence of a signed Hold release entry is a
trust-boundary gap — confirmed. (b) TC must independently verify `operator_signature` before
writing, per the D84 pattern — confirmed. Companion entry `HOLD_RELEASE_REJECTED` (SECURITY,
synchronous) is required.

**Proposed resolution (IC-HOLD-RELEASE-SIGNED-1, from GS3):**
```
IC-HOLD-RELEASE-SIGNED-1:
  From: TC (DEPENDENCY_HOLD_RELEASED_SIGNED writer)
  To: State Ledger
  What it exposes: DEPENDENCY_HOLD_RELEASED_SIGNED (GOVERNANCE, synchronous)
  Conditions: TC verifies operator_signature before writing; release_reason ∈
              {TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE}
  Failure behavior: Signature failure → HOLD_RELEASE_REJECTED (SECURITY, sync);
                    Hold remains active; operator receives rejection with reason
```

**Blocked by:** `release_reason` enum values policy decision.
**Blocks:** GAP-23 (Genesis reset ceremony sequencing — Hold lifecycle must be specced
before the reset ceremony can be fully sequenced).

---

### GAP-22
*(canonical; was labeled "GAP-21" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist
**Priority:** 🟠 High
**Status:** Open

**Description:** `TIMED_OUT` Ledger entry (Appendix C, CONSISTENCY category) carries a
`compensation_direction` field. For Genesis PREPARED timeouts, §11.5.1 prohibits
auto-compensation. The field has no valid value in the Genesis case; audit tools parsing
the Ledger will encounter a `TIMED_OUT` entry with a missing or meaningless field.

**Three resolution paths:**
- (a) Make `compensation_direction` nullable. Null defined as "no compensation — circuit
  trip follows."
- (b) Add `GENESIS_TIMED_OUT` entry type. Separate entry for Genesis case, without
  the field. Semantically cleaner; adds Appendix C surface area.
- (c) Sentinel value: `compensation_direction: "CIRCUIT_TRIP"`. Avoids schema changes;
  requires convention documentation.

**Blocked by:** Decision on which resolution path.
**Blocks:** Complete `TIMED_OUT` entry type definition; audit tool correctness.

---

### GAP-23
*(canonical; was labeled "GAP-22" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist
**Priority:** 🟠 High
**Status:** Blocked — depends on GAP-21 (canonical)

**Description:** After a Genesis PREPARED timeout, the circuit breaker trips and the
Dependency Hold from the failed Genesis persists (§17.3). Three questions are unanswered:

1. Is Hold release a precondition for the circuit reset ceremony? If yes, IC-TC-RESET must
   be amended.
2. Does `CIRCUIT_RESET` implicitly release all active Holds from the failed transaction?
   If yes, a `DEPENDENCY_HOLD_RELEASED_SIGNED` entry is required as part of or immediately
   after reset.
3. Can a new Genesis acquire a Hold while the failed Genesis's Hold is active?

**Latent deadlock:** System enters WRITE_ENABLED post-reset, but a new Genesis is blocked by
the unreleased old Hold — requiring further operator intervention beyond what the spec defines.

**Blocked by:** GAP-21 (canonical) — signed Hold release mechanism must exist first.
**Blocks:** Complete Genesis recovery path; fresh Genesis initiation after Genesis timeout.

---

### GAP-24
*(canonical; was labeled "GAP-23" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist, Warden
**Priority:** 🟡 Medium
*Downgraded from High: no architectural components blocked; affects operator playbook only.*

**Description:** The reset ceremony writes `CIRCUIT_RESET` via the W1 (Orchestrator-mediated)
path. If the Orchestrator is degraded — not compromised but stalled, overloaded, or
temporarily unreachable — the W1 write path is unavailable. The spec defines no error path
for "TC verified preconditions, operator signed, but W1 write path unavailable." The failure
is silent: no Ledger entry records the failed attempt.

**Warden question (unresolved):** Is a degraded Orchestrator during a reset ceremony an
integrity violation (W3 path required) or an operational failure (retry permitted)?

**Blocked by:** Policy decision on Orchestrator degradation classification.
**Blocks:** Complete reset ceremony specification; operator playbook for extended READ_ONLY.

---

### GAP-25
*(canonical; was labeled "GAP-24" in Gap Session 3 summary)*

**Domain(s):** State Consistency Theorist (primary), Warden (co-owner)
**Priority:** 🟠 High
**Status:** Open

**Description:** D87 requires `SCOPE_UPDATED` to be written to the Ledger before the
Orchestrator's in-memory scope registry is updated. Unspecified:

- Maximum allowed propagation lag between Ledger write and registry update.
- What happens if the Orchestrator crashes or stalls between writing the Ledger entry and
  updating the registry. During this window, the Ledger records a scope change the Gate is
  not enforcing.
- How a restarting Orchestrator detects and resolves a persisted `SCOPE_UPDATED` entry that
  was never reflected in the registry during the prior session.

**State Consistency Theorist review question (from GS3):** Is a `SCOPE_UPDATED` Ledger entry
not yet reflected in the registry a `DIVERGED_STATE` condition (triggering circuit breaker),
an automatic replay, or a separate reconciliation path?

**Blocked by:** State Consistency Theorist specification of Ledger → in-memory state
reconciliation behavior on Orchestrator restart.

**Open questions:**
- `OQ-S-GAP24-1` (canonical): Maximum allowed propagation lag — specifiable without
  implementation data?
- `OQ-S-GAP24-2` (canonical): Prescribed procedure for detecting and replaying unprocessed
  `SCOPE_UPDATED` entries on Orchestrator restart?

**Blocks:** Complete trust boundary guarantee for D87; complete scope update model.

---

### GAP-26
*(canonical; was labeled "GAP-25" in Gap Session 3 summary)*

**Domain(s):** Warden (primary)
**Priority:** 🟠 High
**Status:** Open — T14 (ceremony authorization key model) must be resolved first

**Description:** D90 requires scope update ceremonies to be verified against a "declared
ceremony authorization key." The ceremony authorization model is unspecified:

- Which entity or entities are permitted to initiate a scope update ceremony.
- The signing key used by the initiating entity and its relationship to the Orchestrator's
  own signing key.
- The Gate's verification procedure for confirming authorized ceremony (not just structurally
  valid signature).

Without this model, `operator_signature` is an unverified assertion. GAP-26 is blocked by
T14 — the single-key vs. dual-key tension must be resolved before the authorization model
can be specified.

**Physical storage contract for ceremony authorization key material (required fields):**
- Storage medium: Unspecced (OQ-S-GAP25-1, canonical = OQ-S-GAP26-1)
- Governance tier: Human-approved-change (operator-only key; no autonomous orchestrator
  modification)
- Retention rule: Unspecced (OQ-S-GAP25-2, canonical = OQ-S-GAP26-2)
- Write authority: Human operator only, out-of-band to the harness

**Blocked by:** T14 resolution (Warden + Orchestration Comparativist gap session required).
**Blocks:** GAP-27 (rate limit design requires knowing who can trigger ceremony); D90
implementation planning; IC-SCOPE-AUTH-1 instantiation.

**Open questions:**
- `OQ-S-GAP26-1` (canonical): Where is the operator signing key for scope update ceremonies
  stored, and under what physical storage contract?
- `OQ-S-GAP26-2` (canonical): Retention policy and rotation cadence for operator signing
  key material?
- `OQ-S-GAP26-3` (canonical): Must ceremony authorization key be separate from Orchestrator
  first-boot key (§10.5)? [Core question for T14]

---

### GAP-27
*(canonical; was labeled "GAP-26" in Gap Session 3 summary)*

**Domain(s):** Warden (primary), State Consistency Theorist (Ledger entry type co-owner)
**Priority:** 🟠 High
**Status:** Blocked — depends on GAP-26

**Description:** No rate limit on `SCOPE_UPDATED` events. Repeated scope update ceremonies —
misconfigured process or compromised operator account — exploit the infrastructure failure
classification of `SCOPE_HASH_MISMATCH` (no retry budget consumed) to keep agent tokens
permanently invalid, creating a denial-of-service against the agent's write capability.

**D89 provisional resolution:** `scope_update_min_interval_seconds` (Tier 1 operator config;
provisional default 3,600 seconds). Rate limit check precedes signature verification in
processing order. Rejection produces `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, synchronous).

**Unresolved:** Per-`agent_id` vs. global rate limit scope (OQ-S-GAP26-2, canonical =
OQ-S-GAP27-1). Global limit prevents ceremony flooding but blocks legitimate updates for
all agents if one agent's ceremony is rate-limited. Per-agent limit is bypassed by
multi-agent-ID spray attacks.

**Blocked by:** GAP-26 (ceremony authorization model — per-entity rate limiting requires
knowing what an "entity" is in the authorization model).
**Blocks:** Complete D89 specification; `scope_update_min_interval_seconds` operational
validation.

**Open question:** `OQ-S-GAP27-1` (canonical): Per-`agent_id` or global rate limit?

---

### GAP-28
*(canonical; was labeled "GAP-27" in Gap Session 3 summary)*

**Domain(s):** Orchestration Comparativist
**Priority:** 🟡 Medium
*Maintained at Medium: operational efficiency gap with no downstream security or consistency
blocker.*

**Description:** The Orchestrator's proactive notification obligation when scope updates
occur is unspecced. D87 requires agents to be listed in `affected_agent_ids`; whether the
Orchestrator must proactively notify those agents (vs. agents discovering the scope change
at Gate rejection) is undefined.

**Proposed resolution (D91 from GS3):** Orchestrator notifies agents listed in
`affected_agent_ids` as a best-effort operation; agents must not rely on proactive
notification for safety-critical behavior (Gate rejection is the authoritative enforcement).

**Open question:** `OQ-S-GAP27-1` (canonical): Should `SCOPE_UPDATED` carry
`scope_change_type: EXPANDING | NARROWING | RESTRUCTURING` to enable per-type notification
policy?

---

## 🟡 Medium — Self-Contained, No Downstream Spec Dependencies

---

### GAP-9

**Domain(s):** Validation Contract Architect, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Behavioral probe generalization for non-code deployment planning (OQ-W8).
The L2 inference probe is spec'd for code tasks. Non-code write operations (factual
knowledge injection, relation updates) may require different probe strategies.

---

### GAP-10

**Domain(s):** Validation Contract Architect
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Constitutional test classification (OQ-V1). Which test behaviors constitute
"constitutional" guarantees that override normal Reflexion loop retry logic, and which are
standard functional tests?

---

### GAP-11

**Domain(s):** State Consistency Theorist, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Layer 4 external documentation unavailability handling (OQ-SC2). When a
write operation cites external documentation that is no longer retrievable, how does the
validator handle the citation dependency?

---

### GAP-12

**Domain(s):** State Consistency Theorist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Ledger retention policy (OQ-SL1). How long are Ledger entries retained?
What is the archival mechanism for entries beyond the retention window? What is the impact
on Merkle-chain-lite integrity verification for entries in the archived segment?

---

### GAP-13

**Domain(s):** Warden, Orchestration Comparativist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Genesis automation level (OQ-S5). What is the authorized level of
Orchestrator autonomy during Genesis? Can the Orchestrator initiate Genesis compilation
unsupervised, or is human approval required at each Genesis tier boundary?

---

### GAP-14

**Domain(s):** State Consistency Theorist, Orchestration Comparativist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3

**Description:** Async threshold suite for WAL-backed Ledger writes (T5/T11 residual).
WAL flush cadence, light verification interval, full verification interval, reconciliation
backlog thresholds — all heuristic, no empirical basis.

---

### GAP-15

**Domain(s):** Validation Contract Architect, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–3; blocked by GAP-1

**Description:** Compaction verification sample size (OQ-OC3). "100% CORE + 10% random
sample of others" — sample draw procedure and failure report format from Behavioral Probe
to TC are unspecced.

**Blocked by:** GAP-1.

---

### GAP-24 (reassigned from High)
*(see entry above — downgraded to Medium)*

---

### GAP-28 (reassigned from High)
*(see entry above — downgraded to Medium)*

---

## 🟢 Low — Refinement Details, No Architectural Dependencies

---

### GAP-16

**Domain(s):** Warden, Orchestration Comparativist
**Priority:** 🟢 Low
**Status:** Accepted as implementation-time / deployment-specific

**Description:** Notification channels for integrity violations (OQ-S8). Out-of-spec by
design for single-machine reference implementation. Deployment-specific.

---

### GAP-17

**Domain(s):** Orchestration Comparativist, State Consistency Theorist
**Priority:** 🟢 Low
**Status:** Deferred to v2 (OQ-CW1)

**Description:** Voluntary scope-lock release and inter-agent negotiation. No mechanism in
v1 for an agent to release a Write Lock before TTL expiry. No negotiation for overlapping
write regions.

---

### GAP-18

**Domain(s):** State Consistency Theorist
**Priority:** 🟢 Low
**Status:** Deferred to v2 (OQ-SL2)

**Description:** Multi-machine harness Ledger replication. Out of scope for single-machine
v1 reference implementation.

---

### GAP-19

**Domain(s):** Warden
**Priority:** 🟢 Low
**Status:** Deferred to v2

**Description:** Orchestrator signing key rotation. First-boot key is not rotated in v1.
Full PKI is v2 scope.

---

## New Tensions Requiring Gap Sessions

---

### T13 — Advisory Boundedness vs. Operational Flexibility
*(Promoted from GS1 T-NEW-1)*

**Status:** Open — requires gap session
**Specialists:** MEMIT Specialist + Orchestration Comparativist
**Blocks:** v2 outline spec block 2c ratification; T13 resolution required before Phase 2
can close.

**Core conflict:** `LARQL_VERSION_LEGACY` must be a bounded transition state (MEMIT: unbounded
accumulation degrades compaction fidelity). Teams in active development cannot be hard-blocked
mid-sprint by an elapsed notice period (Orchestration: enforcement must be predictable and
override-capable).

**Resolution path:** MEMIT Specialist must provide empirical basis (or principled proxy) for
compaction fidelity degradation rate. Orchestration Comparativist must specify minimum
operator override window. `LEGACY_EXTENSION_GRANTED` (OQ-GAP1-3) is the candidate mechanism.

---

### T14 — Single-Key vs. Dual-Key for Ceremony Authorization
*(Promoted from OQ-S-GAP26-3 / GS3 implicit tension)*

**Status:** Open — requires gap session; can be combined with GAP-26 resolution
**Specialists:** Warden + Orchestration Comparativist
**Blocks:** GAP-26 resolution; D90 implementation planning.

**Core conflict:** Warden requires separate human-held ceremony authorization key (a
compromised Orchestrator must not authorize its own scope changes). Orchestration Comparativist
notes that a separate human-held key creates operational overhead — the key must be physically
secured, its location known to available operators, and its rotation managed out-of-band.

**Resolution path:** Warden must specify the minimum physical storage contract for a
separate ceremony authorization key. Orchestration Comparativist must specify acceptable
operational overhead. Candidate: a key hierarchy where Orchestrator key covers operational
writes and a separate human-held key covers governance ceremonies, with the human-held key
registered in a Tier 1 artifact at first-boot.

---

## Summary Table

| GAP | Domain(s) | Priority | Status | Blocks |
|-----|-----------|----------|--------|--------|
| GAP-1 | MEMIT | 🔴 Critical | Formally deferred (implementation) | GAP-9, backpressure, circuit-breaker rationale |
| GAP-2 | MEMIT | 🔴 Critical | Formally deferred (implementation) | GAP-1, layer targeting, edge caps |
| GAP-3 | MEMIT + Graph | 🔴 Critical | 🔶 Partial (GS1) | Gate pre-check, Validator L1, v2 migration, T13 |
| GAP-4 | Orchestration | 🟠 High | Open | Delegation token v2 shape, HIL interface |
| GAP-5 | Warden + MEMIT | 🟠 High | ✅ Resolved (GS3 / D87) | — |
| GAP-6 | State Consistency | 🟠 High | ✅ Resolved (GS2 / D84) | — (A1 amendment pending) |
| GAP-7 | State Consistency | 🟠 High | ✅ Resolved (GS2 / D85) | — |
| GAP-8 | Validation | 🟠 High | Open | Meta-Validator readiness |
| GAP-9 | Validation + MEMIT | 🟡 Medium | Open | — |
| GAP-10 | Validation | 🟡 Medium | Open | — |
| GAP-11 | State Consistency + MEMIT | 🟡 Medium | Open | — |
| GAP-12 | State Consistency | 🟡 Medium | Open | — |
| GAP-13 | Warden + Orchestration | 🟡 Medium | Open | — |
| GAP-14 | State Consistency + Orchestration | 🟡 Medium | Open | — |
| GAP-15 | Validation + MEMIT | 🟡 Medium | Open (blocked GAP-1) | — |
| GAP-16 | Warden + Orchestration | 🟢 Low | Accepted (deployment-specific) | — |
| GAP-17 | Orchestration + State Consistency | 🟢 Low | Deferred to v2 | — |
| GAP-18 | State Consistency | 🟢 Low | Deferred to v2 | — |
| GAP-19 | Warden | 🟢 Low | Deferred to v2 | — |
| GAP-20 | MEMIT + Graph | 🟠 High | Open | GAP-3 spec blocks 2a/2c |
| GAP-21 | State Consistency + Warden | 🟠 High | Open (Warden co-review ✅) | GAP-23 |
| GAP-22 | State Consistency | 🟠 High | Open | — |
| GAP-23 | State Consistency | 🟠 High | Blocked (GAP-21) | Genesis recovery path |
| GAP-24 | State Consistency + Warden | 🟡 Medium | Open | — |
| GAP-25 | State Consistency + Warden | 🟠 High | Open | D87 trust guarantee |
| GAP-26 | Warden | 🟠 High | Blocked (T14) | GAP-27, D90 planning |
| GAP-27 | Warden + State Consistency | 🟠 High | Blocked (GAP-26) | D89 completeness |
| GAP-28 | Orchestration | 🟡 Medium | Open | — |
| T13 | MEMIT + Orchestration | — (Tension) | Open — requires gap session | GAP-3 spec block 2c |
| T14 | Warden + Orchestration | — (Tension) | Open — requires gap session | GAP-26 |

---

## Recommended Gap Session Sequencing (GS4 onward)

| Session | Primary Specialists | Topics | Rationale |
|---------|---------------------|--------|-----------|
| GS4 | Warden + Orchestration Comparativist | T14, GAP-26 | T14 blocks GAP-26; GAP-26 blocks GAP-27 |
| GS5 | State Consistency + Warden | GAP-25, GAP-21, A1 amendment | Ledger reconciliation model; signed Hold release; A1 scope fix |
| GS6 | State Consistency | GAP-22, GAP-23 | Genesis Hold lifecycle; timeout field fix |
| GS7 | MEMIT + Orchestration | T13 | Advisory boundedness vs. operational flexibility |
| GS8 | Validation Contract Architect | GAP-8, GAP-10 | Meta-* corpus policy; constitutional test classification |

---

## Council Observations — Cross-Gap Patterns (Updated)

**Three patterns from v1 continue to hold:**

**Write Engine Foundation (GAP-1, GAP-2, GAP-3)** — formally deferred (GAP-1, GAP-2) or
partially closed (GAP-3). Write engine cannot be fully specced without target model selection.
All threshold values remain provisional pending empirical validation.

**Transaction Controller Completeness (GAP-6, GAP-7 resolved; GAP-21, GAP-22, GAP-23, GAP-24 open)** —
The TC's primary failure modes (circuit reset authority, PREPARED timeout) are now specced.
The Genesis-specific lifecycle (Hold through reset ceremony) and timeout field semantics remain
open. GAP-21 is the current bottleneck for GAP-23.

**Ceremony Authorization Convergence (new pattern)** — Gap Sessions 1–3 produced three
independent ceremony requirements: manifest ratification (GS1, D-GAP1-B), Hold release (GS2,
GAP-21), and scope update ceremony (GS3, D90). All three ceremonies operate under
under-specified authorization models. T14 and GAP-26 are the resolution mechanism. The council
recommends that GAP-26's resolution define a unified ceremony authorization framework
applicable to all three ceremony types, not just scope update ceremonies.

---

*Gap Backlog v2.0 — 28 gaps + 2 open tensions tracked*
*Supersedes gap-backlog-v1.md*
*Based on: gap-backlog-v1.md + Gap Session 1 + Gap Session 2 + Gap Session 3*
*Council Review Checkpoint: Post-GS3*
