# LLM as Database: Agent Harness Architecture
## Gap Session Schedule v3.0

> **Supersedes:** `gap-session-schedule-v2.md`
> **Source backlog:** `gap-backlog-v3.md` (28 gaps, 2 active tensions T13/T15, post-GS4)
> **Produced by:** Framework Spec Writer (framework-spec-writer skill)
> **Specialist provenance:** Framework Council (cross-domain scheduling analysis)
> **Basis:** Gap Sessions 1–4 completed; Framework Council Review Checkpoint post-GS4;
>   GAP-26 resolved (D92–D96); T14 resolved; GAP-27 unblocked; GAP-28 partially closed;
>   INCON-3 surfaced (Amendment A9 required); T15 introduced
> **Status:** Draft — pending operator ratification before GS5 begins
> **Total arc:** 10 sessions (GS1–GS10) — 4 completed, 6 remaining

---

## What Changed from v2 to v3

**Completed since v2 schedule:**
- GS4 (T14 + GAP-26): T14 resolved by D92 (dual-key hierarchy mandatory). GAP-26 fully resolved
  by D92–D96 — unified CeremonyToken framework covering all four ceremony types
  (MANIFEST_RATIFICATION, HOLD_RELEASE, SCOPE_UPDATE, CIRCUIT_RESET). IC-SCOPE-AUTH-1
  ratified. IC-TC-RESET Amendment A3 populated (D96).

**Impacts on forward schedule:**

| Change | Effect on Schedule |
|---|---|
| GAP-26 resolved | GAP-27 now **unblocked** → absorb into GS7 |
| T14 resolved | GS4 stands as completed; no follow-on tension session |
| GAP-28 `scope_change_type` OQ closed (GS4 §2.3) | GAP-28 is Partial; residual absorbed into GS9 |
| INCON-3 surfaced | A9 (IC-MANIFEST-1) required before GAP-3 spec block 2a is consistent → absorb into GS7 with GAP-20 |
| T15 introduced (CAK availability vs. ceremony urgency) | v1 mitigation documented; v2 path → absorb into GS10 outline block |
| GAP-19 scope extended (OOK + CAK rotation) | No schedule change; GAP-19 remains in GS10 v2 outline |
| SCT review required before GS5 opens | GS5 must address three GS4 conditions before any other session runs |
| AG-1 closed by annotation | Per-agent rate limit scope confirmed; residual formal documentation in GS7 |
| Amendment A7b added | Appendix C additions from GS4 folded into GS7 amendment batch |

**v2 session plan disposition:**

| V2 Session | Disposition in V3 |
|---|---|
| GS5 (GAP-21, GAP-24, GAP-25 + A1) | → GS5 (unchanged pairing; SCT review from GS4 added as required opener; GAP-24 retained) |
| GS6 (GAP-22, GAP-23) | → GS6 (unchanged; blocked on GAP-21 from GS5) |
| GS7 (GAP-27) | → GS7 (expanded: + T13 + GAP-20 + INCON-3 + amendment batch) |
| GS8 (GAP-8, GAP-10) | → GS8 (unchanged) |
| GS9 (GAP-11, GAP-12, GAP-14, GAP-28) | → GS9 (unchanged; GAP-28 now partial, residual absorbed) |
| GS10 (v2 outline + contingent specs) | → GS10 (+ T15 v2 path added; GAP-15 + GAP-9 deferral confirmation added) |
| GS11, GS12 | **Collapsed into GS9 and GS10** — net session count reduced from 12 to 10 |

---

## Scheduling Methodology

### Dependency Classification (v3 update)

**Externally blocked** (cannot close through spec work — require implementation data or operator decision):
- GAP-1, GAP-2: formally deferred (D-CRC-2). No spec session can close them.
- GAP-4: requires operator orchestration path selection (A/B/C). Session produces contingent specs only.
- GAP-9, GAP-15: blocked by GAP-1. Sessions confirm formal deferral status.

**Gap-blocked** (cannot open until named gap resolves):
- GAP-23: blocked on GAP-21 (must exist in GS5 before GS6 can proceed)

**Prerequisite review before GS5** (not a gap session — SCT answers three GS4 review questions):
- SCT Condition 1: Six new + two deprecated Ledger entry types from GS4; Merkle-chain-lite
  integrity with coexisting deprecated and unified types
- SCT Condition 3: `ceremony_authorization_key_anchor` added to Tier 1 `genesis-seal.json`;
  implications for boot sequence and dual-store verification
- These answers feed directly into GAP-25 (registry reconciliation) and A10 (§13.2 amendment)

**Session-order dependencies:**
- GS5 → GS6 (GAP-23 blocked on GAP-21 from GS5)
- GS4 → GS7 (GAP-27 unblocked by GS4; T13 and GAP-20 have no upstream gap deps but belong with MEMIT cluster)
- GS5–GS9 → GS10 (contingent path specs reference trust boundary and Ledger decisions)

**No upstream gap dependency** (parallelizable after GS5 prerequisite review):
- GS7 (T13, GAP-27, GAP-20): can run in parallel with GS6
- GS8 (GAP-8, GAP-10): fully independent
- GS9 (GAP-11, GAP-12, GAP-14, GAP-28): fully independent

### Council vs. Single-Specialist Flags (v3)

| Session | Council Required? | Rationale |
|---|---|---|
| GS5 | **YES** | GAP-25 and GAP-21 each require State Consistency + Warden; A1-REVISED touches TC behavior (SCT) and reset ceremony trust boundary (Warden); SCT review of GS4 CAK model is cross-domain |
| GS6 | No | GAP-22 and GAP-23 are State Consistency domain; Warden co-review of GAP-21 already completed in GS3/GS4 |
| GS7 | **YES** | T13 is named cross-domain tension (MEMIT vs. Orchestration); GAP-20 adds Graph Data Architect; GAP-27 is Warden + SCT; amendment batch spans four domains |
| GS8 | No | GAP-8 and GAP-10 are Validation Contract Architect domain |
| GS9 | **YES** | GAP-11 requires State Consistency + MEMIT; GAP-14 requires State Consistency + Orchestration; two specialist pairings both present |
| GS10 | **YES** | Full multi-domain: GAP-4 path specs require Orchestration + Warden + SCT + MEMIT; GAP-13/GAP-17–GAP-19/T15 require Warden + Orchestration; cross-domain v2 outline |

---

## Complete Session Schedule — GS1 Through GS10

---

### ✅ GS1 — COMPLETED
**Gaps:** GAP-3 (partial)
**Primary skill:** `memit-specialist` + `graph-data-architect` | Council: No | Length: Long
**Outcome:** Gate enforcement confirmed closed. Three v2 outline spec blocks (2a, 2b, 2c). D-GAP1-A–D ratified. GAP-20 surfaced. T13 surfaced. INCON-3 later identified (A9 required — IC-MANIFEST-1 inconsistent with GS4 CeremonyToken model).

---

### ✅ GS2 — COMPLETED
**Gaps:** GAP-6, GAP-7
**Primary skill:** `state-consistency-theorist` | Council: No | Length: Medium
**Outcome:** GAP-6 resolved (D84, IC-TC-RESET — A1-REVISED outstanding). GAP-7 resolved (D85, IC-TC-TIMEOUT). GAP-21–24 surfaced.

---

### ✅ GS3 — COMPLETED
**Gaps:** GAP-5
**Primary skill:** `aisecops-specialist` | Council: No | Length: Medium
**Outcome:** GAP-5 resolved (D87, IC-SCOPE-UPDATE). GAP-25–28 surfaced. T14 surfaced. GAP-21 Warden co-review satisfied.

---

### ✅ GS4 — COMPLETED
**Gaps:** T14, GAP-26
**Primary skill:** `framework-council` (Warden + Orchestration) | Council: YES | Length: Long
**Outcome:** T14 resolved (D92 — dual-key hierarchy mandatory). GAP-26 resolved (D92–D96 — unified CeremonyToken framework, CAK physical storage contract, IC-SCOPE-AUTH-1 ratified, IC-TC-RESET A3 populated). GAP-27 unblocked. GAP-28 OQ closed. T15 introduced. INCON-3 identified. AG-1 closed by annotation. SCT review required before GS5 (3 conditions).

---

### GS5 — NEXT SESSION 🔜
**Gaps:** GAP-21, GAP-24, GAP-25 + A1-REVISED + A2-GS2 + A10 + SCT review
**Primary skill:** `framework-council` (State Consistency Theorist primary; Warden co-owner)
**Council:** YES
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**⚠️ Required first.** Three GS4 review conditions must be answered by the State Consistency
Theorist before this session opens. The SCT review answers feed directly into GAP-25 (Ledger
→ registry reconciliation) and Amendment A10 (§13.2 `genesis-seal.json` schema). Running
GS6, GS7, or any other session before GS5 risks inconsistency between the ceremony framework
and the Ledger integrity model.

**Content:**
SCT review of GS4 conditions (opener — not a separate session):
- Condition 1: Six new + two deprecated Ledger entry types from GS4 (CEREMONY_ACCEPTED,
  CEREMONY_SIGNATURE_INVALID, CEREMONY_REPLAY_REJECTED, CEREMONY_REPLAY_THRESHOLD_EXCEEDED,
  CAK_REGISTERED, CAK_COMPROMISE_DECLARED; deprecated: HOLD_RELEASE_SIGNATURE_INVALID,
  HOLD_RELEASE_REPLAY_REJECTED). Confirm Merkle-chain-lite chain integrity is preserved with
  deprecated entry types that coexist with their unified successors.
- Condition 3: `ceremony_authorization_key_anchor` added to Tier 1 `genesis-seal.json`. Define
  sequencing in the boot-time verification sequence (§13.5) — does CAK anchor verification
  become a new step? Does the dual-store comparison apply to CAK anchor the same way it applies
  to the OOK anchor?

GAP-21: Ratify IC-HOLD-RELEASE-SIGNED-1 with GS4 updates (ceremony_type: HOLD_RELEASE,
  CAK-signed per D93). Finalize `release_reason` enum. Add `DEPENDENCY_HOLD_RELEASED_SIGNED`
  (GOVERNANCE, sync) to Appendix C. Apply A7 (Appendix C additions from GS3 batch).

GAP-24: Decide whether a stalled-but-not-compromised Orchestrator during a reset ceremony
  is W3 class (INTEGRITY_VIOLATION_EMERGENCY) or operational failure (retry). Define error
  path. Specify whether a failed attempt is recorded given W1 unavailability.

GAP-25: Specify Orchestrator restart reconciliation for unprocessed `SCOPE_UPDATED` entries.
  Answer the SCT review question: DIVERGED_STATE trigger, automatic replay, or separate
  reconciliation path? Define maximum propagation lag (OQ-S-GAP24-1) if specifiable.

Amendments: A1-REVISED (§11.8.1 reversal-only bounding), A2-GS2 (§11.8.1 precondition
  check error handling), A10-§13.2 (add `ceremony_authorization_key_anchor` field).
  Apply A8-Appendix-C (cross-category circuit breaker annotation).

**Produces:** SCT review answers (GS4 Conditions 1 + 3); GAP-21 spec block; GAP-24 spec block;
GAP-25 spec block; A1-REVISED, A2, A8, A10 applied; DEPENDENCY_HOLD_RELEASED_SIGNED in
Appendix C.
**Unblocks:** GS6 (GAP-23 — Genesis Hold lifecycle requires GAP-21 first)

---

### GS6
**Gaps:** GAP-22, GAP-23
**Primary skill:** `state-consistency-theorist`
**Council:** No
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why after GS5:** GAP-23 (Genesis Hold lifecycle after timeout) is blocked on GAP-21
(signed Hold release mechanism). GAP-21 resolved in GS5. GAP-22 (`TIMED_OUT` field schema
for Genesis case) is independent of GS5 but belongs in the same session as GAP-23 because
their resolutions are coupled — GAP-22 determines what the Ledger records for a Genesis
timeout; GAP-23 determines what the TC does with active Holds after that timeout.

**Content:**
GAP-22: Choose resolution path for `TIMED_OUT` `compensation_direction` field in Genesis case:
  (a) nullable (null = circuit trip follows), (b) separate `GENESIS_TIMED_OUT` entry type,
  (c) sentinel `"CIRCUIT_TRIP"`. Update Appendix C.

GAP-23: Answer three questions: (1) Is Hold release a precondition for IC-TC-RESET? (2) Does
  CIRCUIT_RESET implicitly release Holds, or must explicit `DEPENDENCY_HOLD_RELEASED_SIGNED`
  precede it? (3) Can a new Genesis acquire a Hold while failed Genesis Hold is active? Define
  operator playbook for Genesis-timeout deadlock.

**Produces:** GAP-22 spec block (Appendix C updated); GAP-23 spec block (IC-TC-RESET
  precondition list amended); operator playbook stub.

---

### GS7
**Gaps:** T13, GAP-27, GAP-20 + Amendment batch
**Primary skill:** `framework-council` (MEMIT Specialist primary; Orchestration Comparativist +
  Graph Data Architect + Warden/SCT for amendments)
**Council:** YES
**Est. length:** Long
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✓*

*Deep Research warranted only if T13 requires current MEMIT literature on compaction fidelity
degradation rates. For pure spec reasoning, Web Search suffices.

**Why grouped:** T13 (advisory boundedness, MEMIT + Orchestration) and GAP-20 (manifest format,
MEMIT + Graph) are both GS1 completion work with MEMIT as shared domain. GAP-27 (rate limit
spec, Warden + SCT) is now unblocked by GS4 and is short enough to fold in. The full
outstanding amendment batch (A4–A9) must be applied before the next integration pass — GS7
is the natural home because its domain overlap (MEMIT + Orchestration + Graph + Warden) covers
all amendment owners. This is the highest-density session in the arc.

**Content:**
T13: MEMIT provides principled proxy for compaction fidelity degradation rate (or empirical
  basis if available). Orchestration specifies minimum operator override window and
  `LEGACY_EXTENSION_GRANTED` mechanism. Produce three-tier advisory model (Tier 1 advisory,
  Tier 2 warning, Tier 3 hard-block with override path). Ratify warning threshold N; flag
  hard-block threshold M as provisional pending GAP-1.

GAP-27: Ratify D89 (`scope_update_min_interval_seconds` in Tier 1 config, provisional default
  3,600s). Confirm per-`agent_id` rate limit scope (AG-1 implicit decision). Formally document
  multi-agent-ID spray attack surface and accepted residual risk. Add
  `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, sync) to Appendix C.

GAP-20: Resolve OQ-GAP1-1 (Architect Agent involvement in manifest authorship). Resolve
  OQ-GAP1-2 (dry-run mandatory?). Ratify IC-MANIFEST-1 amended per A9 (replace
  `ratification_signature` with `ceremony_token_id`; manifest commit gate verifies
  CEREMONY_ACCEPTED Ledger entry + manifest_hash match). Specify all fields in a manifest
  entry.

Amendment batch: A4-§14.3 (3→2 SCOPE_HASH_MISMATCH escalation), A5-§10.9 (ceremony auth
  verification), A6-§10.9 (rate limit requirement), A7-Appendix-C (GS3 batch: DEPENDENCY_
  HOLD_RELEASED_SIGNED, SCOPE_UPDATE_RATE_EXCEEDED, SCOPE_MISMATCH_ESCALATED), A7b-Appendix-C
  (GS4 batch: CEREMONY_* entries, deprecated entry markers), A9-IC-MANIFEST-1 (ceremony_token_id
  replacement). Add LEGACY_EXTENSION_GRANTED to Appendix C.

**Produces:** T13 tension resolution; GAP-3 spec blocks 2a and 2c promoted from outline to
  ratified; GAP-27 spec block; IC-MANIFEST-1 ratified (A9 applied); full amendment batch applied.

---

### GS8
**Gaps:** GAP-8, GAP-10
**Primary skill:** `validation-contract-architect`
**Council:** No
**Est. length:** Medium
**Model:** Sonnet 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** Both are Validation Contract Architect operational policy gaps with no upstream
dependency. Both concern test corpus governance and classification authority.

**Content:**
GAP-8: Resolve Tier 1 contradiction (`corpus_author_identities` mint-once but author list
  must evolve). Propose Tier 2 `corpus-author-registry/` approach. Define corpus extension
  cadence and initialization guidance.

GAP-10: Define constitutional test runtime tagging (file path convention vs. metadata tag vs.
  separate invocation). Define qualification criteria and promotion ceremony (direct addition
  to `constitutional-suite/` Tier 2 via versioned additive directory).

**Produces:** Corpus Author Registry spec block; Constitutional Test Classification + Promotion
  Ceremony spec block.

---

### GS9
**Gaps:** GAP-11, GAP-12, GAP-14, GAP-28
**Primary skill:** `framework-council` (State Consistency Theorist primary; Orchestration
  Comparativist + MEMIT Specialist secondary)
**Council:** YES
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why grouped:** GAP-11 (Layer 4 external doc provenance) requires State Consistency + MEMIT.
GAP-12 (Ledger retention) and GAP-14 (async threshold rationale) are State Consistency domain.
GAP-28 (notification obligation residual) is Orchestration. All four are operational policy
medium-priority gaps with no upstream dependencies. Grouping prevents four standalone sessions
across overlapping domain pairings.

**Content:**
GAP-11: Decide whether harness tracks external doc provenance for Layer 4 facts. Define
  provenance record structure (`external_source_uri`, `source_hash_at_write`, `hash_algorithm`,
  `write_timestamp`). Define monitoring path (Pruning Agent extension vs. separate component).
  Define Ledger entry type for staleness advisory.

GAP-12: Resolve retention governance (Tier 1 floor + Tier 3 active period?). Define archival
  storage format for forensic readability. Define project-close ceremony relationship to
  archival finality.

GAP-14: Produce rationale framework for each provisional threshold — the guarantee each serves
  and failure mode if miscalibrated. Define threshold update ceremony.

GAP-28: Ratify D91 (best-effort notification). Define whether "best-effort" needs a delivery
  guarantee spec. Accept or reject per-type notification policy as implementation-time detail.

**Produces:** Layer 4 provenance record spec block; Ledger retention governance spec block;
  async threshold rationale framework; D91 ratified.

---

### GS10
**Gaps:** GAP-4, GAP-9, GAP-13, GAP-15, GAP-17, GAP-18, GAP-19, T15
**Primary skill:** `framework-council` (full multi-domain)
**Council:** YES
**Est. length:** Medium
**Model:** Opus 4.6 | Web Search ✓ | Deep Research ✗

**Why last:** All eight items are either externally blocked (GAP-4, GAP-9, GAP-15), v2-deferred
(GAP-13, GAP-17, GAP-18, GAP-19), or a v2 tension path (T15). The session produces contingent
spec blocks and v2 outline blocks — work that requires all prior GS5–GS9 spec decisions to be
stable before conditional branches are drafted. GAP-4 path specs in particular reference the
trust boundary model (GS4/GS5), TC ceremony model (GS5/GS6), and Ledger retention model (GS9).

**Content:**
GAP-4: Three contingent path specs (Path A LangGraph, Path B SDK, Path C Hybrid), each marked
  "activates on operator selection." Per path: delegation token shape, HIL decision-return
  mechanism, 2PC TC placement, trust boundary shape, compaction scheduling trigger.

GAP-9: Confirm formal deferral (blocked by GAP-1, D-CRC-2). Record behavioral probe
  generalization as implementation-phase deliverable.

GAP-13: v2 outline block — properties a secondary LLM reviewer must satisfy to act as Genesis
  human-review proxy; trust level; authorization mechanism. v1 boundary: human review mandatory.

GAP-15: Confirm formal deferral (blocked by GAP-1). Record compaction sampling threshold
  validation as implementation-phase deliverable.

GAP-17: v2 outline block — voluntary Write Lock release ceremony requirements; inter-agent
  negotiation protocol requirements. v1 consistency guarantees that must be preserved.

GAP-18: v2 outline block — distributed Ledger consistency model requirements; Merkle-chain-lite
  replication viability; leader-election requirements.

GAP-19: v2 outline block — key rotation dependency map: every component binding on OOK or CAK,
  and what each requires from a rotation event.

T15: v2 resolution path — document OQ-S-CAK-1 (CAK rotation) + OQ-S-CAK-2 (m-of-n signing)
  as the v2 path for resolving CAK availability risk. Confirm v1 mitigation (backup custodian
  operational requirement) is sufficient to close T15 as a v1 Phase 2 blocker. Apply A11
  (deployment guidance clarification).

**Produces:** Three contingent path specs (GAP-4); five v2 outline blocks (GAP-13, GAP-17,
  GAP-18, GAP-19, T15); formal deferral records (GAP-9, GAP-15); A11 applied.

---

## Summary Table — All 10 Sessions

| Session | Status | Gaps | Primary Skill | Council | Est. Length |
|---|---|---|---|---|---|
| GS1 | ✅ Complete | GAP-3 | `memit-specialist` + `graph-data-architect` | No | Long |
| GS2 | ✅ Complete | GAP-6, GAP-7 | `state-consistency-theorist` | No | Medium |
| GS3 | ✅ Complete | GAP-5 | `aisecops-specialist` | No | Medium |
| GS4 | ✅ Complete | T14, GAP-26 | `framework-council` (Warden + Orchestration) | **YES** | Long |
| GS5 | 🔜 Next | GAP-21, GAP-24, GAP-25 + A-batch + SCT review | `framework-council` (SCT + Warden) | **YES** | Long |
| GS6 | — | GAP-22, GAP-23 | `state-consistency-theorist` | No | Medium |
| GS7 | — | T13, GAP-27, GAP-20 + amendment batch | `framework-council` (MEMIT + Orchestration + Graph) | **YES** | Long |
| GS8 | — | GAP-8, GAP-10 | `validation-contract-architect` | No | Medium |
| GS9 | — | GAP-11, GAP-12, GAP-14, GAP-28 | `framework-council` (SCT + Orchestration + MEMIT) | **YES** | Medium |
| GS10 | — | GAP-4, GAP-9, GAP-13, GAP-15, GAP-17–19, T15 | `framework-council` (full multi-domain) | **YES** | Medium |

**Totals:** 4 completed · 6 remaining · 5 council sessions · 1 single-specialist session

---

## Gap Disposition Table — All 28 Gaps + Active Tensions

| ID | Priority | Status | Assigned Session | Note |
|---|---|---|---|---|
| GAP-1 | 🔴 Critical | Formally deferred (implementation) | GS10 (record only) | D-CRC-2; OQ-W1 |
| GAP-2 | 🔴 Critical | Formally deferred (implementation) | GS10 (record only) | D-CRC-2; OQ-W2 |
| GAP-3 | 🔴 Critical | 🔶 Partial (GS1; INCON-3 adds A9) | GS7 completes 2a/2c | GAP-20 dependency |
| GAP-4 | 🟠 High | Open — externally blocked | GS10 (contingent path specs) | Operator path selection |
| GAP-5 | 🟠 High | ✅ Resolved (GS3) | — | D87 / IC-SCOPE-UPDATE |
| GAP-6 | 🟠 High | ✅ Resolved (GS2); A1-REVISED outstanding | GS5 (A1 applied) | D84 / IC-TC-RESET |
| GAP-7 | 🟠 High | ✅ Resolved (GS2) | — | D85 / IC-TC-TIMEOUT |
| GAP-8 | 🟠 High | Open | GS8 | OQ-V5 |
| GAP-9 | 🟡 Medium | Blocked by GAP-1 | GS10 (deferral confirmation) | OQ-W8 |
| GAP-10 | 🟡 Medium | Open | GS8 | OQ-V1 |
| GAP-11 | 🟡 Medium | Open | GS9 | OQ-SC2 |
| GAP-12 | 🟡 Medium | Open | GS9 | OQ-SL1 |
| GAP-13 | 🟡 Medium | Open — v2 outline | GS10 | OQ-S5 |
| GAP-14 | 🟡 Medium | Open | GS9 | T5/T11 thresholds |
| GAP-15 | 🟡 Medium | Blocked by GAP-1 | GS10 (deferral confirmation) | OQ-OC3 |
| GAP-16 | 🟢 Low | Accepted — deployment-specific | — | OQ-S8 |
| GAP-17 | 🟢 Low | Deferred to v2 | GS10 (v2 outline) | OQ-CW1 |
| GAP-18 | 🟢 Low | Deferred to v2 | GS10 (v2 outline) | OQ-SL2 |
| GAP-19 | 🟢 Low | Deferred to v2 (scope extended GS4) | GS10 (v2 outline) | OOK + CAK rotation |
| GAP-20 | 🟠 High | Open (INCON-3: A9 required) | GS7 | Blocks GAP-3 2a/2c |
| GAP-21 | 🟠 High | Open (GS4 ceremony model integrated; Appendix C outstanding) | GS5 | Blocks GAP-23 |
| GAP-22 | 🟠 High | Open | GS6 | — |
| GAP-23 | 🟠 High | Blocked (GAP-21) | GS6 (after GS5) | Genesis Hold lifecycle |
| GAP-24 | 🟡 Medium | Open | GS5 | Degraded Orchestrator |
| GAP-25 | 🟠 High | Open (SCT review from GS4 feeds) | GS5 | D87 trust guarantee |
| GAP-26 | 🟠 High | ✅ Resolved (GS4 / D92–D96) | — | CeremonyToken framework |
| GAP-27 | 🟠 High | 🟢 Unblocked (GS4) | GS7 | Rate limit spec |
| GAP-28 | 🟡 Medium | 🔶 Partial (GS4 OQ closed) | GS9 | Notification residual |
| T13 | — Tension | 🔴 Open — session required | GS7 | Advisory boundedness |
| T14 | — Tension | ✅ Resolved (GS4 / D92) | — | Dual-key hierarchy |
| T15 | — Tension | 🟡 Partial — v1 mitigation documented | GS10 (v2 path) | CAK availability |

---

## Session Dependency Diagram

```
GS1 ✅ → T13 + GAP-20 (GS1 completion) ──► GS7
GS2 ✅ → GAP-21–24 surfaced ──► GS5 (GAP-21, GAP-24, GAP-25) + GS6 (GAP-22, GAP-23)
GS3 ✅ → GAP-25–28 surfaced ──► GS5 (GAP-25) + GS7 (GAP-27 via GS4 unblock)
GS4 ✅ → GAP-26 resolved; GAP-27 unblocked; T14 resolved; T15 + INCON-3 introduced
          └──► GS5 (SCT review conditions 1+3 required before opening)
          └──► GS7 (GAP-27 unblocked; INCON-3/A9 folded into GAP-20 session)

GS5 (required first — SCT review + GAP-21, GAP-24, GAP-25 + A-batch)
    └──► unblocks ──► GS6 (GAP-23 — Genesis Hold lifecycle; requires GAP-21)

GS6 (GAP-22, GAP-23) — after GS5

GS7 (T13, GAP-27, GAP-20 + amendments) — no upstream gap dep (runs parallel with GS6)

GS8 (GAP-8, GAP-10) — independent; any order relative to GS6/GS7

GS9 (GAP-11, GAP-12, GAP-14, GAP-28) — independent

GS5 + GS6 + GS7 + GS8 + GS9 ──► GS10 (final — contingent specs + v2 outlines reference
                                          prior session decisions; preferred order: run last)
```

**Critical path:** GS5 → GS6 (sequential, TC cluster)
**Parallelizable:** GS7, GS8, GS9 (concurrent with each other and with GS6 if capacity allows)
**Final:** GS10 (references all prior work)

---

## Amendment Obligations — Pre-Integration Checklist (v3 update)

| Ref | Section | Amendment | Assigned | Status |
|-----|---------|-----------|----------|--------|
| A1-REVISED | §11.8.1 | TC compensation bounded to reversal-only (C-CRC-3) | GS5 | ⚠️ Outstanding |
| A2-GS2 | §11.8.1 | Precondition check error handling | GS5 | ⚠️ Outstanding |
| A3-IC-TC-RESET | IC-TC-RESET | CeremonyToken/CAK requirement | GS4 → GS5 (verify) | ✅ Populated (D96) |
| A4-§14.3 | §14.3 | 3→2 SCOPE_HASH_MISMATCH escalation (D88) | GS7 | ⚠️ Outstanding |
| A5-§10.9 | §10.9 | Ceremony authorization verification (D90, D93) | GS7 | ⚠️ Outstanding |
| A6-§10.9 | §10.9 | Rate limit requirement (D89) | GS7 | ⚠️ Outstanding |
| A7-Appendix-C | Appendix C | GS3 batch additions | GS7 | ⚠️ Outstanding |
| A7b-Appendix-C | Appendix C | GS4 batch: CEREMONY_* entries, deprecated markers | GS7 | ⚠️ Outstanding |
| A8-Appendix-C | Appendix C | Circuit breaker cross-category annotation | GS5 | ⚠️ Outstanding |
| A9-IC-MANIFEST-1 | IC-MANIFEST-1 | Replace `ratification_signature` with `ceremony_token_id` (INCON-3) | GS7 | 🟠 Required |
| A10-§13.2 | §13.2 `genesis-seal.json` | Add `ceremony_authorization_key_anchor` field (D92, D94) | GS5 (after SCT review) | ⚠️ Pending SCT confirmation |
| A11-deployment | Deployment guidance | v1 CAK backup custodian clarification (T15 mitigation) | GS10 | ⚠️ Outstanding |

---

*Gap Session Schedule v3.0 — 10 sessions total (GS1–GS10) · Supersedes gap-session-schedule-v2.md*
*Sources: gap-backlog-v3.md · gap-backlog-v2.md · council-review-checkpoint-post-gs3.md*
*gap-session-schedule-v2.md · llm-as-database-v1_1-integrated-spec.md*
