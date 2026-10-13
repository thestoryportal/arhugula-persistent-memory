# LLM as Database: Agent Harness Architecture
## Gap Session Schedule v2.0 — Merged

> **Supersedes:** `gap-session-schedule-v1.md`
> **Source backlogs:** `gap-backlog-v1.md` (19 gaps) → `gap-backlog-v2.md` (28 gaps + 2 tensions)
> **Produced by:** Framework Spec Writer (framework-spec-writer skill)
> **Specialist provenance:** Framework Council (cross-domain scheduling analysis)
> **Basis:** Gap Sessions 1–3 completed; Council Review Checkpoint post-GS3;
>   canonical GAP IDs established in gap-backlog-v2.md (D-CRC-1)
> **Status:** Draft — pending operator ratification before GS4 begins
> **Total arc:** 12 sessions (GS1–GS12) — 3 completed, 9 remaining

---

## What Changed from v1 to v2

The v1 schedule projected 8 sessions covering 19 gaps. Three sessions have since been executed
(GS1–GS3). Each session both resolved gaps and introduced new ones — net effect: 28 gaps + 2
open tensions requiring scheduling, with the v2 forward arc spanning 9 further sessions.

**Gaps resolved since v1 schedule was written:**
- GAP-5 (GS3): Write Scope Definition update ceremony — resolved via D87, IC-SCOPE-UPDATE
- GAP-6 (GS2): Circuit breaker reset authority — resolved via D84, IC-TC-RESET (A1 amendment pending)
- GAP-7 (GS2): PREPARED-state timeout — resolved via D85, IC-TC-TIMEOUT

**Gaps formally deferred to implementation phase:**
- GAP-1, GAP-2: empirical thresholds and MEMIT architecture compatibility — cannot be resolved
  through spec work. Council decision D-CRC-2.

**Gaps accepted as deployment-specific / v2-deferred (no session needed, require v2 outline):**
- GAP-16 (notification channels): accepted as deployment-specific
- GAP-17, GAP-18, GAP-19: confirmed v2-deferred; outline session required

**New gaps introduced by GS1–GS3:**
- GAP-20 (GS1): `larql_migration_manifest` format unspecified
- GAP-21 (GS2): `DEPENDENCY_HOLD_RELEASED_SIGNED` missing from Appendix C
- GAP-22 (GS2): `TIMED_OUT` entry schema invalid for Genesis case
- GAP-23 (GS2): Genesis Hold lifecycle after timeout — potential deadlock
- GAP-24 (GS2): Degraded Orchestrator during reset ceremony — no error path
- GAP-25 (GS3): Ledger → in-memory registry reconciliation on Orchestrator restart
- GAP-26 (GS3): Ceremony authorization key model unspecified
- GAP-27 (GS3): No rate limit on `SCOPE_UPDATED` events — denial-of-service surface
- GAP-28 (GS3): Orchestrator proactive notification obligation unspecified

**New cross-domain tensions promoted to tension map:**
- T13: Advisory Boundedness vs. Operational Flexibility (MEMIT + Orchestration) — requires session
- T14: Single-Key vs. Dual-Key for Ceremony Authorization (Warden + Orchestration) — blocks GAP-26

**Amendment obligations from GS2–GS3 + council checkpoint:**
- A1-REVISED: §11.8.1 — TC compensation bounded to reversal-only (D-CRC-3, C-CRC-3)
- A2-GS2: §11.8.1 — Precondition check error handling
- A3-IC-TC-RESET: Placeholder for GAP-26 ceremony authorization dependency (C-CRC-2)
- A4–A8: Various Appendix C and §10.9 amendments — all targeting GS5

**V1 session plan disposition:**

| V1 Planned Session | Disposition in V2 Schedule |
|---|---|
| V1 S1 (GAP-3) | → GS1 ✅ Completed (partial) |
| V1 S2 (GAP-6, GAP-7) | → GS2 ✅ Completed (both resolved) |
| V1 S3 (GAP-5) | → GS3 ✅ Completed (resolved) |
| V1 S4 (GAP-8, GAP-10) | → GS9 (unchanged pairing) |
| V1 S5 (GAP-9, GAP-11, GAP-15) | → GS10 (GAP-9 + GAP-11); GAP-15 deferred pending GAP-1 |
| V1 S6 (GAP-12, GAP-14) | → GS11 (+ GAP-28 added) |
| V1 S7 (GAP-1, GAP-2, GAP-4) | GAP-1, GAP-2 formally deferred; GAP-4 → GS12 |
| V1 S8 (v2 outline: GAP-13, GAP-16–19) | → GS12 (GAP-16 removed as accepted deployment-specific) |

---

## Scheduling Methodology

### Dependency Classification

**Externally blocked** (cannot close through spec work alone):
- GAP-1, GAP-2: require implementation-phase empirical data. Formally deferred (D-CRC-2).
- GAP-4: requires operator selection of orchestration path (A/B/C). Session produces
  contingent specs only.
- GAP-15: blocked by GAP-1 deferral. Session confirms deferral and records status.

**Gap-blocked** (cannot open until named gap is resolved):
- GAP-27: blocked by GAP-26 (must resolve ceremony authorization model first)
- GAP-23: blocked by GAP-21 (signed Hold release mechanism must exist before Genesis reset sequencing)

**Session-order dependencies** (must be scheduled after a prior session, but not blocked on that session's full closure — can begin once the relevant spec decision is made):
- GAP-6 was prerequisite for A1 amendment work in GS5
- GAP-21 resolution in GS5 is prerequisite for GAP-23 in GS6

**No spec-level blocker** (can schedule in any order relative to each other):
T14, GAP-26, GAP-21, GAP-24, GAP-25, A1 amendment, GAP-22, T13, GAP-20, GAP-8, GAP-9,
GAP-10, GAP-11, GAP-12, GAP-13, GAP-14, GAP-28

### Council vs. Single-Specialist Flags

Per the iteration guide Step 2.2: any session requiring 2+ specialists invokes the
`framework-council` skill. Single-specialist sessions use the relevant individual skill.

| Session | Council Required? | Rationale |
|---|---|---|
| GS4 | YES | T14 is a named cross-domain tension; D-CRC-4 requires unified ceremony framework covering all three ceremony types — cannot be specced by one domain |
| GS5 | YES | GAP-25 and GAP-21 each require State Consistency + Warden; A1 amendment touches TC behavior (State Consistency) and the reset ceremony trust boundary (Warden) |
| GS6 | No | GAP-22 and GAP-23 are State Consistency Theorist domain; Warden confirmed GAP-21 trust boundary already satisfied in GS3 |
| GS7 | YES | GAP-27 is Warden primary (rate limit design, per-agent vs. global authorization model) + State Consistency Theorist (Ledger entry type, `SCOPE_UPDATE_RATE_EXCEEDED` placement) |
| GS8 | YES | T13 is a named cross-domain tension (MEMIT vs. Orchestration); GAP-20 adds Graph Data Architect — three-specialist session |
| GS9 | No | GAP-8 and GAP-10 are Validation Contract Architect domain |
| GS10 | YES | GAP-9 crosses Validation + MEMIT; GAP-11 crosses State Consistency + MEMIT — two pairings, MEMIT shared across both |
| GS11 | YES | GAP-14 is State Consistency + Orchestration; GAP-28 is Orchestration — two-specialist minimum |
| GS12 | YES | GAP-4 path specs require Orchestration + Warden + State Consistency + MEMIT — four domains |

---

## Complete Session Schedule — GS1 Through GS12

---

### ✅ GS1 — COMPLETED
**Gaps:** GAP-3
**Primary skill:** `memit-specialist` + `graph-data-architect`
**Council:** No (two-specialist)
**Est. length:** Long → Actual: Long
**Outcome:** GAP-3 partial — Gate enforcement confirmed closed; three v2 outline spec blocks
produced; GAP-20 surfaced (manifest format unspecified); T13 surfaced (advisory boundedness).
D-GAP1-A through D-GAP1-D ratified.

---

### ✅ GS2 — COMPLETED
**Gaps:** GAP-6, GAP-7
**Primary skill:** `state-consistency-theorist`
**Council:** No (single specialist)
**Est. length:** Medium → Actual: Medium
**Outcome:** GAP-6 resolved (D84, IC-TC-RESET — A1 amendment required per INCON-1).
GAP-7 resolved (D85, IC-TC-TIMEOUT). Four new gaps introduced: GAP-21–24.

---

### ✅ GS3 — COMPLETED
**Gaps:** GAP-5
**Primary skill:** `aisecops-specialist`
**Council:** No (two-specialist with MEMIT input)
**Est. length:** Medium → Actual: Medium
**Outcome:** GAP-5 resolved (D87, IC-SCOPE-UPDATE). Four new gaps introduced: GAP-25–28.
T14 surfaced (ceremony key model). GAP-21 Warden co-review satisfied.

---

### GS4 — NEXT SESSION
**Gaps:** T14, GAP-26
**Primary skill:** `framework-council` (Warden primary; Orchestration Comparativist required)
**Council:** YES — cross-domain tension session
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why first:** T14 (single-key vs. dual-key for ceremony authorization) is the root dependency
for GAP-26 (ceremony authorization model), which in turn blocks GAP-27. T14 is also the
core question behind OQ-S-GAP26-3. This is the highest-priority unblocked session — resolving
it cascades relief down to GAP-27 and clears the ceremony authorization ambiguity that
C-CRC-2 has flagged as a placeholder dependency in IC-TC-RESET.

D-CRC-4 constraint: GAP-26 resolution MUST define a unified ceremony authorization framework
covering all three ceremony types from GS1–3 — manifest ratification, Hold release, and scope
update ceremony. A ceremony-type-specific model that does not generalize is a spec violation.

**Content:**

*T14 — Single-Key vs. Dual-Key Ceremony Authorization:*
- Resolve the core question (OQ-S-GAP26-3): must the ceremony authorization key be separate
  from the Orchestrator's first-boot signing key (§10.5)?
- Warden position: separate key required — a compromised Orchestrator must not authorize its
  own governance ceremonies.
- Orchestration position: separate key creates operational overhead — physical location,
  rotation, out-of-band management must be specified.
- Resolution must satisfy both: define a key hierarchy where the Orchestrator key covers
  operational writes and a human-held ceremony key covers governance ceremonies. Define the
  physical storage contract for the ceremony key (OQ-S-GAP26-1).

*GAP-26 — Ceremony Authorization Model:*
- Specify which entity or entities may initiate a scope update ceremony.
- Specify the Gate's verification procedure for confirming authorized ceremony initiation
  (not just a structurally valid signature).
- Specify the relationship between the ceremony authorization key and the Orchestrator signing
  key (resolved by T14 above).
- Produce a unified authorization framework applicable to all three ceremony types (D-CRC-4).
- Specify retention policy and rotation cadence for ceremony key material (OQ-S-GAP26-2).
- Produce IC-SCOPE-AUTH-1 as a ratified contract.

**Produces:**
- T14 tension resolution entry
- Spec block: Ceremony Authorization Key Model (unified — covering manifest ratification,
  Hold release, scope update ceremony)
- Spec block: GAP-26 — Ceremony Authorization Model (includes physical storage contract)
- Interface contract: IC-SCOPE-AUTH-1 (ratified)
- Placeholder amendment A3-IC-TC-RESET satisfied or upgraded to full spec
- Open question dispositions: OQ-S-GAP26-1, OQ-S-GAP26-2, OQ-S-GAP26-3

**Unblocks:** GAP-27 (rate limit design requires knowing the authorization entity model)

---

### GS5
**Gaps:** GAP-21, GAP-24, GAP-25 + A1 amendment revision
**Primary skill:** `framework-council` (State Consistency Theorist primary; Warden co-owner)
**Council:** YES — two-specialist session
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why second:** GAP-21 (signed Hold release Ledger entry) has no upstream gap dependency — the
only blocker is a policy decision on the `release_reason` enum. GAP-24 (degraded Orchestrator
during reset) and GAP-25 (Ledger → in-memory reconciliation on restart) are both Warden +
State Consistency and are thematically connected: all three concern what happens at the edges
of the TC ceremony model. Resolving them together prevents three separate passes through the
same ceremony trust boundary. GAP-21 resolution in this session also unblocks GS6 (GAP-23).

The A1 amendment revision (INCON-1 + C-CRC-3) is Warden + State Consistency and belongs in
this session — it strengthens the TC compensation bound in §11.8.1. A8 (Appendix C cross-
category annotation for circuit breaker workflow entries) can also be resolved here.

**Content:**

*A1 Amendment Revision — §11.8.1:*
- Apply C-CRC-3 bounding language: "A compensation write that would produce any weight change
  beyond the reversal of the prior committed operation MUST be rejected and treated as a TC
  fault, triggering an additional circuit trip event."
- Warden co-signs the amendment — confirm the bounded compensation path does not create a
  new write surface under READ_ONLY mode.
- Apply A8: add cross-category rationale annotation for circuit breaker workflow entries in
  Appendix C (GS2 T-NEW-1 finding).

*GAP-21 — `DEPENDENCY_HOLD_RELEASED_SIGNED` Ledger Entry:*
- Ratify IC-HOLD-RELEASE-SIGNED-1 (proposed in GS3): entry type GOVERNANCE, synchronous;
  TC verifies `operator_signature` before writing; `release_reason` enum
  `{TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE}`.
- Add companion entry `HOLD_RELEASE_REJECTED` (SECURITY, synchronous) to Appendix C.
- Add to Appendix C via A7 amendment.

*GAP-24 — Degraded Orchestrator During Reset Ceremony:*
- Decide: is a stalled/overloaded (not compromised) Orchestrator during reset an integrity
  violation (W3 path) or an operational failure (retry permitted)?
- Define the error path for "TC verified preconditions, operator signed, W1 write unavailable."
- Specify whether a failed reset attempt produces a Ledger entry (if W1 is unavailable, no
  entry is possible via W1 — does W3 apply? Does the spec need a `RESET_ATTEMPT_FAILED`
  advisory entry via a limited path?).

*GAP-25 — Ledger → In-Memory Registry Reconciliation on Restart:*
- Specify the maximum allowed propagation lag between `SCOPE_UPDATED` Ledger write and
  registry update (OQ-S-GAP24-1).
- Specify procedure for detecting and replaying unprocessed `SCOPE_UPDATED` entries on
  Orchestrator restart (OQ-S-GAP24-2).
- Resolve the State Consistency question: is an unprocessed `SCOPE_UPDATED` entry a
  `DIVERGED_STATE` condition, an automatic replay, or a separate reconciliation path?

**Produces:**
- A1 amendment (revised, bounded) — §11.8.1 update
- A8 amendment — Appendix C cross-category annotation
- Spec block: `DEPENDENCY_HOLD_RELEASED_SIGNED` + `HOLD_RELEASE_REJECTED` (Appendix C)
- Spec block: GAP-24 — Reset Ceremony Degraded-Orchestrator Error Path
- Spec block: GAP-25 — Orchestrator Restart Registry Reconciliation Protocol
- IC-HOLD-RELEASE-SIGNED-1 ratified
- Open question dispositions: OQ-S-GAP24-1, OQ-S-GAP24-2

**Unblocks:** GAP-23 (Genesis Hold lifecycle — requires signed Hold release mechanism)

---

### GS6
**Gaps:** GAP-22, GAP-23
**Primary skill:** `state-consistency-theorist`
**Council:** No — single-specialist session
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why third in TC cluster:** GAP-22 (`TIMED_OUT` field schema for Genesis case) is a
self-contained internal decision. GAP-23 (Genesis Hold lifecycle after timeout circuit trip)
was blocked by GAP-21 in GS5 — now unblocked. These two are tightly coupled: GAP-22
determines the semantics of the `TIMED_OUT` Ledger entry in the Genesis case; GAP-23
determines what the TC does with active Holds during the Genesis reset ceremony that follows.
Speccing them together prevents the `TIMED_OUT` entry definition from being inconsistent
with the Hold release sequencing.

**Content:**

*GAP-22 — `TIMED_OUT` Entry Schema for Genesis Case:*
- Select resolution path: (a) `compensation_direction` nullable — null = "circuit trip follows,
  no compensation"; (b) separate `GENESIS_TIMED_OUT` entry type; (c) sentinel value
  `compensation_direction: "CIRCUIT_TRIP"`.
- Rationale: (b) is semantically cleanest and avoids nullable field conventions that would need
  documenting across audit tools; (a) is minimal; (c) is a convention-heavy workaround. Spec
  the chosen path and update Appendix C.
- Confirm `GENESIS_TIMED_OUT` (if chosen) is CONSISTENCY category, synchronous, carries
  full forensic evidence payload.

*GAP-23 — Genesis Hold Lifecycle After Timeout:*
- Resolve three open questions:
  1. Is Hold release a precondition for the IC-TC-RESET signed ceremony? → Propose: yes,
     the `release_reason: GENESIS_RESET_PREPARATION` value from GAP-21 exists precisely
     for this scenario. Amend IC-TC-RESET to list this as a precondition for Genesis timeout
     trips.
  2. Does `CIRCUIT_RESET` implicitly release all active Holds from the failed transaction?
     → Propose: no implicit release; explicit `DEPENDENCY_HOLD_RELEASED_SIGNED` with
     `release_reason: GENESIS_RESET_PREPARATION` must precede or accompany `CIRCUIT_RESET`.
  3. Can a new Genesis acquire a Hold while the failed Genesis's Hold is active? → No; the
     Pruning pre-check (§17.6) blocks any new Hold on held edges. Define the explicit rule
     for the Genesis-re-initiation case.
- Define the operator playbook for the deadlock scenario: failed Genesis Hold active → circuit
  breaker tripped → new Genesis cannot start. Sequence: sign Hold release → verify
  `HOLD_RELEASE_REJECTED` not returned → proceed to IC-TC-RESET ceremony.

**Produces:**
- Spec block: `TIMED_OUT` / `GENESIS_TIMED_OUT` entry schema (Appendix C update)
- Spec block: GAP-23 — Genesis Hold Lifecycle and Reset Ceremony Sequencing
- Amendment to IC-TC-RESET adding Hold release as precondition for Genesis timeout trips
- Operator playbook stub for Genesis-timeout deadlock scenario
- Open question dispositions: GAP-22 resolution path selection, GAP-23 sequencing

---

### GS7
**Gaps:** GAP-27
**Primary skill:** `framework-council` (Warden primary; State Consistency Theorist Ledger entry co-owner)
**Council:** YES — two-specialist session
**Est. length:** Short
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why after GS4:** GAP-27 (rate limit on `SCOPE_UPDATED` events) was blocked by GAP-26 (GS4).
Now unblocked. The rate limit design requires knowing the authorization entity model — per-agent
rate limits require knowing what "agent" means in the ceremony authorization framework resolved
in GS4. The D89 provisional resolution (`scope_update_min_interval_seconds` in Tier 1 config,
default 3,600 seconds) needs ratification. The per-agent vs. global scope question
(OQ-S-GAP27-1) is the key remaining decision.

**Content:**

*GAP-27 — Scope Update Ceremony Rate Limit:*
- Ratify D89: `scope_update_min_interval_seconds` as Tier 1 config field with default 3,600s.
- Resolve OQ-S-GAP27-1: per-`agent_id` vs. global rate limit scope.
  - Global: prevents ceremony flooding; blocks all agents if any ceremony is rate-limited.
  - Per-agent: bypassed by multi-agent-ID spray attacks (an attacker registering many agent
    IDs to circumvent per-agent limits). With the ceremony authorization key model from GS4,
    the relevant entity is the *ceremony initiator* (human operator with ceremony key), not the
    agent being updated. Rate limiting on ceremony initiator is more robust.
  - Proposed resolution: rate limit applies per ceremony initiator identity (not per `agent_id`
    and not globally), with global fallback if ceremony initiator identity is absent. Confirm
    with Warden.
- Add `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, synchronous) to Appendix C (A7 amendment
  subset — this entry type was flagged but not yet added).
- Apply A4: reduce consecutive `SCOPE_HASH_MISMATCH` escalation threshold from 3 to 2
  (D88 from GS3 checkpoint).
- Resolve OQ-S-GAP28-1 (carried from GAP-28): should `SCOPE_UPDATED` carry
  `scope_change_type: EXPANDING | NARROWING | RESTRUCTURING`? Flag disposition here or
  defer to GS11 with GAP-28.

**Produces:**
- D89 ratified (or revised): rate limit spec
- Spec block: `SCOPE_UPDATE_RATE_EXCEEDED` (Appendix C)
- A4 amendment applied — §14.3 escalation threshold update
- Open question disposition: OQ-S-GAP27-1

---

### GS8
**Gaps:** T13, GAP-20
**Primary skill:** `framework-council` (MEMIT Specialist primary; Orchestration Comparativist + Graph Data Architect required)
**Council:** YES — three-specialist cross-domain tension session
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✓*

*Deep Research warranted only if the MEMIT compaction fidelity degradation question (OQ-GAP1-4)
requires current research on edit accumulation and catastrophic forgetting rates. For the pure
operational-flexibility spec reasoning, Web Search suffices.

**Why after GS1 but can run anytime (no upstream gap dependency):** T13 (advisory boundedness
vs. operational flexibility) was surfaced in GS1 and requires MEMIT + Orchestration to resolve
the hard-block threshold for `LARQL_VERSION_LEGACY` accumulation (OQ-GAP1-3 / GAP-3 spec
block 2c). GAP-20 (`larql_migration_manifest` format) is MEMIT + Graph and also traces back
to GS1's output. Combining them makes this session the GS1 completion pass — closing the
two items GS1 explicitly left open.

**Content:**

*T13 — Advisory Boundedness vs. Operational Flexibility:*
- MEMIT Specialist: provide empirical basis or principled proxy for compaction fidelity
  degradation rate as a function of `LARQL_VERSION_LEGACY` patch accumulation. If empirical
  data is not available, define a conservative proxy — e.g., degradation risk increases
  proportionally with the ratio of legacy patches to total active patches.
- Orchestration Comparativist: specify minimum operator override window — what is the minimum
  acceptable notice period before a Tier 3 hard-block takes effect? Specify the
  `LEGACY_EXTENSION_GRANTED` mechanism (OQ-GAP1-3): what does the operator sign, what does
  the Gate check, and what is the maximum extension duration?
- Resolve: define the three-tier advisory model (Tier 1: `LARQL_VERSION_LEGACY` advisory
  async entry; Tier 2: warning Ledger entry at N patches; Tier 3: hard-block at M patches
  with `LEGACY_EXTENSION_GRANTED` as the override path). Ratify the threshold for N and M,
  noting that M is provisional pending GAP-1 empirical data.

*GAP-20 — `larql_migration_manifest` Format (IC-MANIFEST-1 Ratification):*
- Resolve OQ-GAP1-1: can the Architect Agent participate in manifest authorship (with human
  ratification), or is it fully outside the agent authorization model? Note that the Architect
  Agent holds the highest agent privilege class — the question is whether manifest authorship
  is an agent-class operation (subject to standard gate + token model) or a human-only
  governance operation (subject to Tier 1 update ceremony).
- Resolve OQ-GAP1-2: is a test compaction ("manifest dry-run") on a sample of legacy patches
  mandatory before manifest ratification? Specify the dry-run protocol if yes.
- Ratify IC-MANIFEST-1: specify all fields in a manifest entry — translation rule structure,
  how bucket decisions are expressed, `bucket_map` field definition. Note that bucket boundary
  thresholds (GAP-3 residual (a)) remain provisional pending GAP-1 empirical data.
- Apply A5 and A6 amendments to §10.9 (ceremony authorization verification, rate limit
  requirement) if not already applied in GS5/GS7.

**Produces:**
- T13 tension resolution entry
- Spec block: Three-Tier `LARQL_VERSION_LEGACY` Advisory Model (Tiers 1–3 defined;
  hard-block threshold M provisional pending GAP-1)
- `LEGACY_EXTENSION_GRANTED` Ledger entry type + spec
- IC-MANIFEST-1 ratified — `larql_migration_manifest` field definitions
- GAP-3 spec blocks 2a and 2c — updated and promoted from outline to ratified
- Open question dispositions: OQ-GAP1-1, OQ-GAP1-2, OQ-GAP1-3

---

### GS9
**Gaps:** GAP-8, GAP-10
**Primary skill:** `validation-contract-architect`
**Council:** No — single-specialist session
**Est. length:** Medium
**Model:** Sonnet 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** Both are Validation Contract Architect operational policy gaps with no
upstream dependency. They share a concern: corpus governance and test authority. Resolving
them together produces a coherent sealed corpus governance model — who can write tests, how
tests are classified, and how tests are promoted to constitutional status.

**Content:**

*GAP-8 — Corpus Authorship Policy:*
- Resolve the Tier 1 contradiction: `corpus_author_identities` is a mint-once Tier 1 field,
  but operators need to add or remove authorized authors over the project lifetime. Proposed
  resolution: Tier 1 contains the bootstrapping identity only; a Tier 2 sealed artifact
  (`corpus-author-registry/`) carries the live author list with versioned additive directories
  and signed manifests. Tier 1 `corpus_author_identities` is re-interpreted as the bootstrapping
  authority that may sign the first Tier 2 manifest.
- Define corpus extension cadence: is the 90-day staleness flag (§13.3) the only cadence
  signal, or should the spec set a minimum mandatory extension requirement? Propose: staleness
  flag is the only signal; cadence is operator-owned. Confirm or revise.
- Define minimum viable corpus guidance for initial deployment: before the first 50 commits,
  what is the minimum corpus initialization expectation?

*GAP-10 — Constitutional Test Classification:*
- Define the runtime tagging mechanism: how does the Validator know at runtime that a given
  test belongs to the `constitutional-suite/` Tier 2 artifact vs. a task-generated test?
  Proposed: file path convention — tests within `constitutional-suite/` are constitutional by
  location; Validator has persistent read access and uses the path prefix as the tag. No
  runtime metadata field required.
- Define constitutional qualification criteria: what properties must a test have to be
  eligible for promotion? Proposed: (a) asserts a framework-level invariant not specific to
  any single task; (b) passes against a known-good model state snapshot; (c) authored by an
  identity in the corpus author registry (resolved above).
- Define the promotion ceremony: direct operator addition to the `constitutional-suite/`
  Tier 2 artifact via the standard versioned additive directory pattern. No separate
  nomination workflow — the Tier 2 signed update ceremony is the ceremony.

**Produces:**
- Spec block: Corpus Author Registry — Tier 2 approach (resolves Tier 1 contradiction)
- Spec block: Constitutional Test Classification — Runtime Tagging and Promotion Ceremony
- Open question dispositions: OQ-V5 (residuals), OQ-V1

---

### GS10
**Gaps:** GAP-9, GAP-11
**Primary skill:** `framework-council` (MEMIT Specialist primary; Validation Contract Architect
+ State Consistency Theorist secondary)
**Council:** YES — two-to-three specialist session
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** GAP-9 (behavioral probe generalization for non-code domains) crosses Validation
+ MEMIT. GAP-11 (Layer 4 external documentation unavailability) crosses State Consistency +
MEMIT. MEMIT is the shared domain — both gaps concern what the write engine can verify about
facts it has written. The domain-agnostic probe protocol (GAP-9) and the external provenance
tracking model (GAP-11) are related: if the L2 probe is generalized, it directly informs
whether a provenance-check failure on an external source can be detected via inference.

**Content:**

*GAP-9 — Behavioral Probe Generalization:*
- Define a domain-agnostic L2 inference probe protocol. The code-domain framing
  ("generation test confirms the fact fires correctly in inference") needs a domain-general
  equivalent. Candidate options:
  - (a) Forced-choice probe: model selects the correct answer to a templated factual question
    about the written edge from a candidate set. Probe template is authored at write time.
  - (b) Generative consistency probe: model generates a free-text response to a prompt;
    Validator checks for presence of the written fact using a deterministic assertion against
    the response.
  - (c) Probability distribution probe: model's softmax distribution on a token completion
    task has expected argmax at the written fact's canonical form.
- Resolve the actor-critic independence question: who authors the probe template? If the
  Coder Agent authors it, this violates the spirit of D32. Proposed: probe template is
  authored by the TGA as part of the test-generation phase, treating the probe template as
  a test artifact under the same independence constraints.
- Define "probe passes" in domain-general terms.

*GAP-11 — Layer 4 External Documentation Provenance:*
- Decide whether the harness tracks external document provenance for Layer 4 facts.
  Proposed: yes, with lightweight URL pinning + content hash at write time, stored as
  metadata in the `.larql` patch and in the Ledger entry.
- Define the provenance record structure: `external_source_id` (URI), `source_hash_at_write`
  (content hash), `hash_algorithm`, `write_timestamp`. Stored as optional fields in the
  `.larql` patch header — mandatory for Layer 4 domain patches that cite external sources.
- Define what happens when a provenance check fails: staleness advisory Ledger entry
  (`EXTERNAL_SOURCE_STALE`, CONSISTENCY, async); no automatic compensation. Human review flag.
- Define whether provenance monitoring is a Pruning Agent extension (Pruning Agent checks
  pinned hashes periodically) or a separate monitoring component. Proposed: Pruning Agent
  extension; monitoring cadence matches Pruning trigger schedule (§11.12).

**Produces:**
- Spec block: Domain-Agnostic L2 Inference Probe Protocol
- Spec block: Layer 4 External Document Provenance Record
- `EXTERNAL_SOURCE_STALE` Ledger entry type (Appendix C)
- Open question dispositions: OQ-W8, OQ-SC2

---

### GS11
**Gaps:** GAP-12, GAP-14, GAP-28
**Primary skill:** `framework-council` (State Consistency Theorist primary;
Orchestration Comparativist secondary for GAP-14 and GAP-28)
**Council:** YES — two-specialist session
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** GAP-12 (Ledger retention policy) and GAP-14 (async threshold suite rationale
framework) are both State Consistency Theorist domain and both concern Ledger operational
policy — one for how long entries are kept, the other for how frequently the chain is verified.
GAP-28 (Orchestrator proactive notification obligation, with proposed D91 resolution) is
Orchestration-primary but shares the scope update context established in GS4–GS7 and requires
minimal session time if D91 is accepted as written.

**Content:**

*GAP-12 — Ledger Retention Policy:*
- Define the retention policy governance model: is retention period a Tier 1 immutable value
  (set at first boot, never changed) or a Tier 3 anchored Git config value (changeable via
  Git commit + Ledger entry)? Note the tension: longer retention periods are a forensic
  benefit; immutability prevents policy downgrade attacks. Proposed: Tier 1 immutable for the
  minimum retention floor; Tier 3 for the active retention period, subject to the constraint
  that it cannot be shorter than the Tier 1 floor.
- Define the archival storage format beyond "compressed, manifest-sealed bundles" — sufficient
  for forensic readability across multi-year horizons. Specify: format identifier, compression
  algorithm, manifest schema, integrity hash type, and restore procedure.
- Define the project-close ceremony if one is required: does `PROJECT_CLOSED` seal the final
  epoch, make the Ledger read-only, and trigger archival? Specify the ceremony and the Ledger
  entry (LIFECYCLE, synchronous).

*GAP-14 — Async Threshold Suite Rationale Framework:*
- Produce a rationale framework for each provisional threshold — not new values (empirical
  data unavailable), but the guarantee each threshold serves and the failure mode each
  prevents. For each:
  - WAL flush cadence: maximum data-loss window this cadence bounds.
  - Light verification interval (every 100 entries): corruption-detection window for the
    Merkle-chain-lite model.
  - Full verification interval (10,000 entries / 24h): audit-completeness guarantee and
    cost-model justification for the 24-hour fallback.
  - Reconciliation backlog thresholds (10/7d warning; 50/30d critical): SLA proxy definition.
- Define the threshold update ceremony: what Ledger entry records a threshold change? Who has
  authority? Is `scope_update_min_interval_seconds` the precedent for threshold governance?

*GAP-28 — Orchestrator Proactive Notification Obligation:*
- Ratify or revise D91: Orchestrator notifies agents listed in `affected_agent_ids` as a
  best-effort operation; agents must not rely on proactive notification for safety-critical
  behavior (Gate rejection is the authoritative enforcement mechanism).
- Resolve OQ-S-GAP28-1 (carried from GS7 if deferred): should `SCOPE_UPDATED` carry
  `scope_change_type: EXPANDING | NARROWING | RESTRUCTURING`? If yes, define per-type
  notification policy. If no, mark as out-of-scope.

**Produces:**
- Spec block: Ledger Retention Policy Governance Model
- Spec block: Project-Close Ceremony (if warranted)
- Spec block: Async Threshold Suite Rationale Framework (values remain provisional)
- D91 ratified (or revised): proactive notification
- Open question dispositions: OQ-SL1, T5/T11 threshold framework, OQ-S-GAP28-1

---

### GS12
**Gaps:** GAP-4, GAP-13, GAP-15 (status confirmation), GAP-17, GAP-18, GAP-19
**Primary skill:** `framework-council` (full multi-domain — Orchestration, Warden,
State Consistency, MEMIT all required)
**Council:** YES — full multi-domain session
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why last:** This is the v2 planning and contingent-spec session. It produces outline spec
blocks and contingent path specs, not closures. All six gaps here are either externally blocked
(GAP-4, GAP-15) or v2-deferred (GAP-13, GAP-17, GAP-18, GAP-19). The session is scheduled
last so that the full GS4–GS11 spec work is stable before contingent specs are drafted —
the GAP-4 path specs in particular must reference the trust boundary model (GS4), the TC
ceremony model (GS5–GS6), and the Ledger retention model (GS11) without contradiction.

**Content:**

*GAP-4 — Three Contingent Path Specs (operator path selection externally blocked):*
- Produce three conditional spec blocks, each marked "activates on operator selection of
  Path [X]":
  - Path A (LangGraph alone): subgraph delegation token shape; HIL decision delivery within
    LangGraph's concurrency model; 2PC TC placement within a LangGraph execution graph.
  - Path B (Claude Agent SDK alone): nested sub-agent delegation token shape; HIL delivery
    via SDK callback or interrupt; sub-agent write scope inheritance model.
  - Path C (Hybrid): delegation token handoff at the LangGraph ↔ SDK boundary; HIL delivery
    in a mixed concurrency model; scope inheritance when an SDK sub-agent is spawned from a
    LangGraph node.
- Warden: for each path, specify where token verification happens and what the trust boundary
  shape looks like.
- State Consistency: for each path, specify where the 2PC TC lives and how compaction
  scheduling is triggered within that path's event loop.

*GAP-13 — Genesis Automation (v2 outline):*
- Define what v2 must specify: properties a secondary LLM reviewer must satisfy to act as
  a human-review proxy for Genesis authorization; minimum trust level; authorization mechanism
  (agent YAML? separate Write Scope Definition?).
- What v1 leaves as the boundary: human review is mandatory in v1. The proxy concept is v2
  only. v2 must not remove the principle that Genesis authorization requires a trusted
  non-Orchestrator party.

*GAP-15 — Compaction Sample Size (status confirmation):*
- Confirm formal deferral to implementation phase (blocked by GAP-1, which is deferred by
  D-CRC-2). Record the threshold validation framework as the pending deliverable: the 10%
  sample rate and SUPPORTING/INCIDENTAL abort thresholds remain provisional pending
  OQ-W1 empirical data. No spec session can close this gap.

*GAP-17, GAP-18, GAP-19 — v2 Outline Blocks:*
- GAP-17 (voluntary lock release): define v2 requirements for voluntary Write Lock release
  ceremony and inter-agent write region negotiation protocol.
- GAP-18 (multi-machine Ledger replication): define consistency model requirements for a
  distributed Ledger; flag Merkle-chain-lite as single-machine-only; define leader-election
  requirements.
- GAP-19 (Orchestrator key rotation): define what a key rotation event must guarantee for
  active token validity, in-flight operations, public-key re-anchoring, and all components
  that bind on the Orchestrator key.

**Produces:**
- Three conditional spec blocks: Path A, Path B, Path C (all marked "activates on operator
  selection")
- GAP-13, GAP-17, GAP-18, GAP-19: four v2 outline spec blocks
- GAP-15: formal deferral record with threshold validation framework reference
- GAP-4: contingent interface contract stubs for each path (marked provisional until path
  is selected)

---

## Summary Table — All 12 Sessions

| Session | Status | Gaps | Primary Skill(s) | Council | Est. Length |
|---|---|---|---|---|---|
| GS1 | ✅ Complete | GAP-3 | `memit-specialist` + `graph-data-architect` | No | Long |
| GS2 | ✅ Complete | GAP-6, GAP-7 | `state-consistency-theorist` | No | Medium |
| GS3 | ✅ Complete | GAP-5 | `aisecops-specialist` | No | Medium |
| GS4 | 🔜 Next | T14, GAP-26 | `framework-council` (Warden + Orchestration) | **YES** | Long |
| GS5 | — | GAP-21, GAP-24, GAP-25, A1 | `framework-council` (State Consistency + Warden) | **YES** | Long |
| GS6 | — | GAP-22, GAP-23 | `state-consistency-theorist` | No | Medium |
| GS7 | — | GAP-27 | `framework-council` (Warden + State Consistency) | **YES** | Short |
| GS8 | — | T13, GAP-20 | `framework-council` (MEMIT + Orchestration + Graph) | **YES** | Long |
| GS9 | — | GAP-8, GAP-10 | `validation-contract-architect` | No | Medium |
| GS10 | — | GAP-9, GAP-11 | `framework-council` (MEMIT + Validation + State Consistency) | **YES** | Medium |
| GS11 | — | GAP-12, GAP-14, GAP-28 | `framework-council` (State Consistency + Orchestration) | **YES** | Medium |
| GS12 | — | GAP-4, GAP-13, GAP-15, GAP-17, GAP-18, GAP-19 | `framework-council` (full multi-domain) | **YES** | Medium |

**Totals:** 3 completed · 9 remaining · 7 council sessions · 2 single-specialist sessions

---

## Gap Disposition Table — All 28 Gaps + 2 Tensions

| ID | Priority | Status | Assigned Session | Note |
|---|---|---|---|---|
| GAP-1 | 🔴 Critical | Formally deferred — implementation phase | GS12 (status record only) | D-CRC-2; OQ-W1 |
| GAP-2 | 🔴 Critical | Formally deferred — implementation phase | GS12 (status record only) | D-CRC-2; OQ-W2 |
| GAP-3 | 🔴 Critical | 🔶 Partial (GS1) | GS8 completes 2a/2c; GS12 closes 2b/2d | GAP-20 blocks 2a/2c |
| GAP-4 | 🟠 High | Open — externally blocked | GS12 (contingent path specs) | Operator path selection |
| GAP-5 | 🟠 High | ✅ Resolved (GS3) | — | D87 / IC-SCOPE-UPDATE |
| GAP-6 | 🟠 High | ✅ Resolved (GS2) | GS5 (A1 amendment) | D84 / IC-TC-RESET; A1 required |
| GAP-7 | 🟠 High | ✅ Resolved (GS2) | — | D85 / IC-TC-TIMEOUT |
| GAP-8 | 🟠 High | Open | GS9 | OQ-V5 |
| GAP-9 | 🟡 Medium | Open | GS10 | OQ-W8 |
| GAP-10 | 🟡 Medium | Open | GS9 | OQ-V1 |
| GAP-11 | 🟡 Medium | Open | GS10 | OQ-SC2 |
| GAP-12 | 🟡 Medium | Open | GS11 | OQ-SL1 |
| GAP-13 | 🟡 Medium | Open — v2 outline | GS12 | OQ-S5 |
| GAP-14 | 🟡 Medium | Open | GS11 | T5/T11 thresholds |
| GAP-15 | 🟡 Medium | Open — blocked by GAP-1 | GS12 (deferral confirmation) | OQ-OC3 |
| GAP-16 | 🟢 Low | Accepted — deployment-specific | — | OQ-S8 |
| GAP-17 | 🟢 Low | Deferred to v2 | GS12 (v2 outline) | OQ-CW1 |
| GAP-18 | 🟢 Low | Deferred to v2 | GS12 (v2 outline) | OQ-SL2 |
| GAP-19 | 🟢 Low | Deferred to v2 | GS12 (v2 outline) | Key rotation |
| GAP-20 | 🟠 High | Open | GS8 | Blocks GAP-3 spec blocks 2a/2c |
| GAP-21 | 🟠 High | Open | GS5 | Blocks GAP-23 |
| GAP-22 | 🟠 High | Open | GS6 | — |
| GAP-23 | 🟠 High | Blocked (GAP-21) | GS6 (after GS5) | Genesis Hold lifecycle |
| GAP-24 | 🟡 Medium | Open | GS5 | Degraded Orchestrator |
| GAP-25 | 🟠 High | Open | GS5 | D87 trust boundary gap |
| GAP-26 | 🟠 High | Open — blocked by T14 | GS4 | Ceremony authorization |
| GAP-27 | 🟠 High | Blocked (GAP-26) | GS7 (after GS4) | Rate limit design |
| GAP-28 | 🟡 Medium | Open | GS11 | D91 proposed; ratification needed |
| T13 | — Tension | Open — session required | GS8 | Advisory boundedness |
| T14 | — Tension | Open — session required | GS4 | Blocks GAP-26 |

---

## Session Dependency Diagram

```
GS1 ✅ (GAP-3 partial; T13 surfaced; GAP-20 surfaced)
    └──► informs ──► GS8 (T13 + GAP-20 — GS1 completion pass)

GS2 ✅ (GAP-6, GAP-7 resolved; GAP-21–24 surfaced)
GS3 ✅ (GAP-5 resolved; GAP-25–28 surfaced; T14 surfaced)
    └──► GS3 T14 ──► GS4 (T14 + GAP-26 — must be first)

GS4 (T14, GAP-26) — no upstream dependency
    └──► unblocks ──► GS7 (GAP-27 — rate limit now specifiable)

GS5 (GAP-21, GAP-24, GAP-25, A1) — no upstream gap dependency
    └──► unblocks ──► GS6 (GAP-23 — Genesis Hold lifecycle; requires GAP-21 first)

GS6 (GAP-22, GAP-23) — after GS5

GS7 (GAP-27) — after GS4

GS8 (T13, GAP-20) — no upstream gap dependency (informs GS1 completion)
    └──► completes GAP-3 spec blocks 2a/2c
    └──► LEGACY_EXTENSION_GRANTED mechanism available for GS12 contingent specs

GS9 (GAP-8, GAP-10) — no upstream gap dependency
GS10 (GAP-9, GAP-11) — no upstream gap dependency
GS11 (GAP-12, GAP-14, GAP-28) — no upstream gap dependency
    [GS11 Ledger retention model informs GS12 contingent path specs — preferred sequencing
     but not a hard dependency]

GS12 (GAP-4, GAP-13, GAP-15, GAP-17–19) — scheduled last; references GS4–GS11 spec output
    [produces contingent path specs and v2 outline blocks — does not block any other session]
```

**Minimum critical path (to close all High-priority open gaps):**
GS4 → GS5 → GS6 → GS7 (all TC/ceremony cluster) + GS8 (larql versioning cluster) + GS9–GS11 (remaining policy gaps, parallelizable in principle)

---

## Amendment Obligations — Pre-Integration Checklist

The following amendments are required before the next v1.x spec integration pass. Session assignments shown.

| Ref | Section | Amendment | Assigned |
|---|---|---|---|
| A1-REVISED | §11.8.1 | TC compensation bounded to reversal-only (C-CRC-3) | GS5 |
| A2-GS2 | §11.8.1 | Precondition check error handling | GS5 |
| A3-IC-TC-RESET | IC-TC-RESET | Placeholder → full ceremony auth key spec | GS4 → GS5 |
| A4-§14.3 | §14.3 | 3 consecutive → 2 consecutive `SCOPE_HASH_MISMATCH` (D88) | GS7 |
| A5-§10.9 | §10.9 | Ceremony authorization verification requirement (D90) | GS8 |
| A6-§10.9 | §10.9 | Rate limit requirement (D89) | GS7 |
| A7-Appendix-C | Appendix C | Add: `DEPENDENCY_HOLD_RELEASED_SIGNED`, `HOLD_RELEASE_REJECTED`, `SCOPE_UPDATE_RATE_EXCEEDED`, `SCOPE_MISMATCH_ESCALATED` | GS5 + GS7 |
| A8-Appendix-C | Appendix C | Cross-category rationale annotation for circuit breaker workflow entries | GS5 |

---

*Gap Session Schedule v2.0 — 12 sessions total (GS1–GS12) · Supersedes gap-session-schedule-v1.md*
*Sources: gap-backlog-v1.md · gap-backlog-v2.md · council-review-checkpoint-post-gs3.md*
*gap-session-schedule-v1.md · llm-as-database-v1_1-integrated-spec.md*
