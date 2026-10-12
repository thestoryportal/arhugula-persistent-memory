# LLM as Database: Agent Harness Architecture
## Gap Backlog v3.0

> **Source document:** `llm-as-database-v1_1-integrated-spec.md` (v1.1 Integrated Specification)
> **Supersedes:** `gap-backlog-v2.md`
> **Session:** Framework Council — Post-Gap Sessions 1–4 Checkpoint
> **Scope:** All gaps from v2 backlog, updated with GS4 closure status, plus all new items
> introduced in GS4 with canonical IDs. Administrative gaps and amendment obligations
> appended.
> **Total gaps tracked:** 28 — 3 Critical, 12 High, 7 Medium, 4 Low
> **Active tensions requiring gap sessions:** T13, T15
> **Resolved tensions (this update):** T14 ✅
> **Last updated:** Framework Council Review Checkpoint, Post-GS4

---

## ⚠️ Numbering Notes

**v2 carry-forward:** Gap backlog v1 contained 19 gaps (GAP-1 through GAP-19). Gap Sessions
1–3 introduced 9 new gaps. The naming collision in v2 (GS1's "GAP-21" clashing with GS2's
"GAP-21") was resolved by D-CRC-1; canonical IDs are stable from v2 onward.

**v3 changes:** GAP-26 resolved (GS4). GAP-19 scope extended (GS4). GAP-27 unblocked (GS4).
No new GAP IDs introduced in GS4. T14 resolved. T15 added as new tension. INCON-3 surfaced
(Amendment A9 required). AG-1 closed by annotation. Total gap count is unchanged at 28.

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
| **Unblocked** | Dependency resolved; ready to schedule |

---

## 🔴 Critical — Blocks 3 or More Other Gaps

---

### GAP-1

**Domain(s):** MEMIT Specialist
**Priority:** 🔴 Critical
**Status:** Formally deferred — implementation phase

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

**Formal deferral rationale:** GAP-1 cannot be resolved through specification work alone.
Resolution requires empirical testing against a selected target model. All threshold values
in the current spec are explicitly marked provisional (OQ-W1). This deferral does not block
spec work; it blocks implementation-phase calibration only.

**Council note (Post-GS4):** GAP-1 feeds T13 directly — the hard-block threshold for
`LARQL_VERSION_LEGACY` accumulation (100 patches, v2 outline spec block 2c) has no empirical
basis until GAP-1 is resolved.

---

### GAP-2

**Domain(s):** MEMIT Specialist
**Priority:** 🔴 Critical
**Status:** Formally deferred — implementation phase

**Description:** MEMIT's compatibility with the target model architecture has not been
verified (OQ-W2). Layer coordinates (L15–L25 for a 32-layer model), FFN width assumptions,
and architectural variant compatibility (MoE, Mamba-family, grouped-query attention) are all
unverified for the actual target model.

**Blocked by:** Explicit target model specification + MEMIT compatibility test run.

**Blocks:** Layer targeting spec correctness, edge cap justification, GAP-1 resolution,
`attention_weight` divergence check meaningfulness.

**Formal deferral rationale:** GAP-2 requires empirical compatibility testing and cannot be
resolved through specification work. Resolution requires target model selection followed by a
MEMIT compatibility probe run. All layer coordinates are explicitly provisional.

---

### GAP-3

**Domain(s):** MEMIT Specialist, Graph Data Architect
**Priority:** 🔴 Critical
**Status:** 🔶 Partial — gate enforcement confirmed closed (GS1); three v2 residuals have
outline spec blocks (GS1); GAP-20 is a dependency for full instantiation

**Description (original):** The `.larql` schema versioning strategy is deferred to v2
(OQ-W6, §18.3). Issues include: Validator handling of older-schema patches, `.larql` schema
version header field, superseded-patch archive handling during compaction, and migration path
for active patches when schema version advances.

**Gap Session 1 progress:**
- Gate enforcement layer confirmed closed (D82, pre-check #8, `larql_migration_manifest` in
  §8.10 and §13.2 form a sound enforcement chain).
- Three v2 outline spec blocks produced: migration manifest authorship ceremony (2a),
  deprecation ceremony and notice period policy (2b), `LARQL_VERSION_LEGACY` advisory window
  policy (2c).
- Decisions D-GAP1-A through D-GAP1-D ratified.

**GS4 update:** The unified ceremony authorization framework (D93) specifies the manifest
ratification ceremony as `ceremony_type: MANIFEST_RATIFICATION` using the standard
CeremonyToken envelope (§2.1). Spec block 2a's human ratification step is now CAK-signed.
INCON-3 (see Amendment Obligations) requires Amendment A9 to IC-MANIFEST-1 before spec
block 2a can be considered consistent with the unified ceremony model.

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
- (e) INCON-3 resolution: IC-MANIFEST-1 `ratification_signature` field must be replaced with
  `ceremony_token_id` reference per Amendment A9.

**Blocks:** Complete Gate pre-check spec (§10.2), Validator L1 static analysis completeness,
compaction re-run strategy for superseded patches, v2 migration planning, T13 resolution.

---

## 🟠 High — Blocks 1–2 Gaps or Load-Bearing Architectural Decisions

---

### GAP-4

**Domain(s):** Orchestration Comparativist
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS1–4

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

**Resolution summary:** READ_ONLY mode correctly defined; TC precondition verification covers
all three trip types; CIRCUIT_RESET placement in W1/W2/W3 is correct and unambiguous;
Appendix C cataloguing is complete. GAP-23 through GAP-24 are residual seams.

**⚠️ Amendment A1-REVISED outstanding:** TC compensation exemption from write-token
suspension must include reversal-only bounding language (D-CRC-3, C-CRC-3). Text not yet
in integrated spec. Execution required in GS5.

**GS4 update:** Amendment A3 to IC-TC-RESET is now populated (D96). Circuit reset ceremonies
must be a `CeremonyToken` with `ceremony_type: CIRCUIT_RESET`, signed by the CAK. OOK-signed
reset tokens are rejected at verification step 3. A1-REVISED remains separately outstanding.

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
**Status:** Open — unaddressed in GS1–4

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

**GS4 update — INCON-3:** IC-MANIFEST-1's proposed `ratification_signature` field (an
operator cryptographic signature over the manifest entry hash) is inconsistent with GS4's
unified CeremonyToken model (D93). After GS4, the manifest ratification ceremony is
`ceremony_type: MANIFEST_RATIFICATION`; the operator signature is `operator_signature` in
the CeremonyToken body, not a field in the manifest entry itself. Amendment A9 is required
(see Amendment Obligations): replace `ratification_signature` in IC-MANIFEST-1 with
`ceremony_token_id: string` — the ID of the `CEREMONY_ACCEPTED` Ledger entry produced by
the manifest ratification ceremony. The manifest commit gate must verify that the referenced
Ledger entry exists and that its payload's `manifest_hash` matches the manifest being
committed.

**Proposed resolution path:** Ratify IC-MANIFEST-1 (amended per A9) as a v1.2 patch. Requires
resolution of the bucket boundary decision (GAP-3 residual (a)) before the `bucket_map` field
can be fully specified.

**Blocks:** GAP-3 spec blocks 2a and 2c full instantiation; compaction recovery path spec;
bucket boundary resolution for T1 translation.

**Open questions:**
- `OQ-GAP1-1`: Should manifest authorship allow Architect Agent involvement (with human
  ratification via CAK-signed CeremonyToken), or is the authorship phase fully outside the
  agent authorization model?
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
on successful commit. It does not distinguish automatic release from operator-signed release
— the distinction is most forensically significant precisely at the moment a human operator
intervenes in a hung transaction.

**Warden co-review finding (GS3):** (a) The absence of a signed Hold release entry is a
trust-boundary gap — confirmed. (b) TC must independently verify `operator_signature` before
writing, per the D84 pattern — confirmed. Companion entry `HOLD_RELEASE_REJECTED` (SECURITY,
synchronous) is required.

**GS4 update:** The Dependency Hold release is now specified as a governance ceremony using
`ceremony_type: HOLD_RELEASE` (D93, §2.2). IC-HOLD-RELEASE is amended: `key_ref` resolves
to `ceremony_authorization_key_anchor` (CAK). Failure events `HOLD_RELEASE_SIGNATURE_INVALID`
and `HOLD_RELEASE_REPLAY_REJECTED` are superseded by unified `CEREMONY_SIGNATURE_INVALID`
and `CEREMONY_REPLAY_REJECTED` with `ceremony_type: HOLD_RELEASE` as discriminator. The
`release_reason` enum values (TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE)
are preserved in the §2.2 payload. GAP-21 remains open because `DEPENDENCY_HOLD_RELEASED_SIGNED`
must still be added to Appendix C (the ceremony framework specifies the authorization model;
the Appendix C entry formalizes the Ledger record).

**Blocked by:** `release_reason` enum values policy decision (now partially informed by GS4
§2.2 payload definition); Appendix C amendment execution.
**Blocks:** GAP-23 (Genesis reset ceremony sequencing).

---

### GAP-22
*(canonical; was labeled "GAP-21" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS4

**Description:** `TIMED_OUT` Ledger entry (Appendix C, CONSISTENCY category) carries a
`compensation_direction` field. For Genesis PREPARED timeouts, §11.5.1 prohibits
auto-compensation. The field has no valid value in the Genesis case; audit tools parsing
the Ledger will encounter a `TIMED_OUT` entry with a missing or meaningless field.

**Three resolution paths:**
- (a) Make `compensation_direction` nullable. Null defined as "no compensation — circuit
  trip follows."
- (b) Add `GENESIS_TIMED_OUT` entry type. Separate entry for Genesis case, without the
  field. Semantically cleaner; adds Appendix C surface area.
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
   If yes, a `DEPENDENCY_HOLD_RELEASED_SIGNED` Ledger entry is required as part of or
   immediately after reset.
3. Can a new Genesis acquire a Hold while the failed Genesis's Hold is active?

**Latent deadlock:** System enters WRITE_ENABLED post-reset, but a new Genesis is blocked by
the unreleased old Hold — requiring further operator intervention beyond what the spec defines.

**GS4 note:** IC-TC-RESET Amendment A3 (D96) specifies the circuit reset ceremony
authorization (CeremonyToken, CAK-signed). It does not address Hold lifecycle sequencing,
which remains the unresolved core of this gap. GAP-23 is not reopened by GS4; it remains
blocked on GAP-21.

**Blocked by:** GAP-21 (canonical) — signed Hold release mechanism must be specced before
reset ceremony Hold sequencing can be defined.
**Blocks:** Complete Genesis recovery path; fresh Genesis initiation after Genesis timeout.

---

### GAP-25
*(canonical; was labeled "GAP-24" in Gap Session 3 summary)*

**Domain(s):** State Consistency Theorist (primary), Warden (co-owner)
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS4; SCT review from GS4 feeds directly into this gap

**Description:** D87 requires `SCOPE_UPDATED` to be written to the Ledger before the
Orchestrator's in-memory scope registry is updated. Unspecified:

- Maximum allowed propagation lag between Ledger write and registry update.
- What happens if the Orchestrator crashes or stalls between writing the Ledger entry and
  updating the registry. During this window, the Ledger records a scope change the Gate is
  not enforcing.
- How a restarting Orchestrator detects and resolves a persisted `SCOPE_UPDATED` entry that
  was never reflected in the registry during the prior session.

**GS4 update — SCT review required:** GS4's State Consistency Theorist review flag asks
specifically: (a) Is a `SCOPE_UPDATED` Ledger entry not yet reflected in the registry a
`DIVERGED_STATE` condition (triggering circuit breaker), an automatic replay, or a separate
reconciliation path? (b) Do the six new Ledger entry types from GS4 require additions to
the Merkle-chain-lite integrity structure? These SCT review questions must be answered
(required before GS5 opens) and their answers directly inform GAP-25 resolution.

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

**Domain(s):** Warden (primary), Orchestration Comparativist (secondary)
**Priority:** 🟠 High
**Status:** ✅ Resolved — D92, D93, D94, D95, D96 (Gap Session 4)

**Resolution summary:** T14 resolved by D92 (dual-key hierarchy). Unified ceremony
authorization framework (D93) covers all four ceremony types (MANIFEST_RATIFICATION,
HOLD_RELEASE, SCOPE_UPDATE, CIRCUIT_RESET) via a canonical CeremonyToken envelope.
Physical storage contract for the Ceremony Authorization Key (CAK) specified by D94
(hardware security token preferred; encrypted offline key file acceptable fallback;
filesystem storage prohibited by C-CAK-1). IC-SCOPE-AUTH-1 ratified as the unified ceremony
authorization framework interface contract (D95). IC-TC-RESET Amendment A3 populated with
CAK-based circuit reset authorization (D96). D-CRC-4 satisfied: all three ceremony types
from GS1–GS3 plus circuit reset are covered by a single verification model. OQ-S-GAP26-1
closed (D94), OQ-S-GAP26-2 partially closed (retention rule closed by D94; rotation cadence
deferred to v2, OQ-S-CAK-1), OQ-S-GAP26-3 closed (D92).

**Constraints established:** C-CAK-1 through C-CAK-5, C-CRC-4 through C-CRC-6.

**New tension introduced:** T15 (CAK Availability vs. Ceremony Urgency) — v1 mitigation
documented (backup custodian operational requirement); v2 resolution deferred (OQ-S-CAK-2).

**Ledger entry types introduced (all require Appendix C addition):**
`CEREMONY_ACCEPTED`, `CEREMONY_SIGNATURE_INVALID`, `CEREMONY_REPLAY_REJECTED`,
`CEREMONY_REPLAY_THRESHOLD_EXCEEDED`, `CAK_REGISTERED`, `CAK_COMPROMISE_DECLARED`.

**Ledger entry types deprecated (superseded by unified types):**
`HOLD_RELEASE_SIGNATURE_INVALID`, `HOLD_RELEASE_REPLAY_REJECTED`.

**Spec amendments required:**
- §13.2 `genesis-seal.json` — add `ceremony_authorization_key_anchor` field
- §10.9 Scope Update Ceremony — reference unified CeremonyToken
- Appendix C — six new entry types added; two deprecated entries marked with unified
  successors
- GAP-19 — scope extended to include CAK rotation alongside OOK rotation

**⚠️ SCT review required before GS5:** Condition 1 (six new Ledger entry types; two
deprecated; Merkle-chain-lite integrity with coexisting deprecated and unified types) and
Condition 3 (`ceremony_authorization_key_anchor` added to Tier 1 `genesis-seal.json`). Three
specific SCT questions must be answered (see GS4 summary) before GS5 opens.

---

### GAP-27
*(canonical; was labeled "GAP-26" in Gap Session 3 summary)*

**Domain(s):** Warden (primary), State Consistency Theorist (Ledger entry type co-owner)
**Priority:** 🟠 High
**Status:** 🟢 Unblocked — GAP-26 resolved (GS4); ready for GS7

**Description:** No rate limit on `SCOPE_UPDATED` events. Repeated scope update ceremonies —
misconfigured process or compromised operator account — exploit the infrastructure failure
classification of `SCOPE_HASH_MISMATCH` (no retry budget consumed) to keep agent tokens
permanently invalid, creating a denial-of-service against the agent's write capability.

**D89 provisional resolution:** `scope_update_min_interval_seconds` (Tier 1 operator config;
provisional default 3,600 seconds). Rate limit check precedes signature verification in
processing order. Rejection produces `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, synchronous).
Per-`agent_id` rate limit scope is implicit in D89's language ("for the same `agent_id`");
this is treated as the adopted scope decision (AG-1 closed by annotation — see Administrative
Gaps below).

**Unresolved (GS7 target):** Full rate limit spec completion including `scope_update_min_interval_seconds`
operational validation (OQ-S-GAP26-1 canonical = OQ-S-GAP27-2 if renumbered; not yet closed),
multi-agent-ID spray attack surface assessment, and per-agent vs. global tradeoff formal
documentation.

**GS4 update:** GAP-26 resolved. GAP-27 is now unblocked. `scope_change_type` field
(OQ-S-GAP27-1, pre-canonical) is closed — GS4 §2.3 payload adds `scope_change_type:
EXPANDING | NARROWING | RESTRUCTURING` to the SCOPE_UPDATE ceremony payload. Orchestrator
may apply per-type notification policy at its discretion. GAP-28 open question on
`scope_change_type` is therefore also closed (see GAP-28 below).

**Blocks:** Complete D89 specification; `scope_update_min_interval_seconds` operational
validation.

---

## 🟡 Medium — Self-Contained, No Downstream Spec Dependencies

---

### GAP-9

**Domain(s):** Validation Contract Architect, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4; blocked by GAP-1

**Description:** Behavioral probe generalization for non-code deployment planning (OQ-W8).
The L2 inference probe is specced for code tasks. Non-code write operations (factual
knowledge injection, relation updates) may require different probe strategies.

**Blocked by:** GAP-1.

---

### GAP-10

**Domain(s):** Validation Contract Architect
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4

**Description:** Constitutional test classification (OQ-V1). Which test behaviors constitute
"constitutional" guarantees that override normal Reflexion loop retry logic, and which are
standard functional tests?

---

### GAP-11

**Domain(s):** State Consistency Theorist, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4

**Description:** Layer 4 external documentation unavailability handling (OQ-SC2). When a
write operation cites external documentation that is no longer retrievable, how does the
Validator handle the citation dependency?

---

### GAP-12

**Domain(s):** State Consistency Theorist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4

**Description:** Ledger retention policy (OQ-SL1). How long are Ledger entries retained?
What is the archival mechanism for entries beyond the retention window? What is the impact
on Merkle-chain-lite integrity verification for entries in the archived segment?

---

### GAP-13

**Domain(s):** Warden, Orchestration Comparativist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4

**Description:** Genesis automation level (OQ-S5). What is the authorized level of
Orchestrator autonomy during Genesis? Can the Orchestrator initiate Genesis compilation
unsupervised, or is human approval required at each Genesis tier boundary?

---

### GAP-14

**Domain(s):** State Consistency Theorist, Orchestration Comparativist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4

**Description:** Async threshold suite for WAL-backed Ledger writes (T5/T11 residual). WAL
flush cadence, light verification interval, full verification interval, reconciliation backlog
thresholds — all heuristic, no empirical basis.

---

### GAP-15

**Domain(s):** Validation Contract Architect, MEMIT Specialist
**Priority:** 🟡 Medium
**Status:** Open — unaddressed in GS1–4; blocked by GAP-1

**Description:** Reflexion loop retry limit — the maximum number of Coder Agent retry
attempts before escalation — is provisional (OQ-V2). Value is currently set at 3 retries
per task. Rationale is heuristic; not calibrated to any write complexity distribution.

**Blocked by:** GAP-1 (write-volume stress testing may inform retry budget per task weight).

---

### GAP-24
*(canonical; was labeled "GAP-23" in Gap Session 2 summary)*

**Domain(s):** State Consistency Theorist, Warden
**Priority:** 🟡 Medium
*Downgraded from High in v2: no architectural components blocked; affects operator playbook
only.*
**Status:** Open — unaddressed in GS1–4

**Description:** The reset ceremony writes `CIRCUIT_RESET` via the W1 (Orchestrator-mediated)
path. If the Orchestrator is degraded — not compromised but stalled, overloaded, or
temporarily unreachable — the W1 write path is unavailable. The spec defines no error path
for "TC verified preconditions, operator signed, but W1 write path unavailable." The failure
is silent: no Ledger entry records the failed attempt.

**Warden question (unresolved):** Is a degraded Orchestrator during a reset ceremony an
integrity violation class event (W3 `INTEGRITY_VIOLATION_EMERGENCY` path) or an operational
failure (retry after recovery permitted)?

**GS4 note:** Amendment A3 (D96) populates the IC-TC-RESET ceremony authorization model.
It does not address the Orchestrator-degraded failure path, which remains open.

**Blocked by:** Policy decision on Orchestrator degradation classification.
**Blocks:** Complete reset ceremony specification; operator playbook for extended READ_ONLY.

---

### GAP-28
*(canonical; was labeled "GAP-27" in Gap Session 3 summary)*

**Domain(s):** Orchestration Comparativist
**Priority:** 🟡 Medium
**Status:** 🔶 Partial — `scope_change_type` closed (GS4); proactive notification obligation
partially specified (D91, GS3)

**Description:** The Orchestrator's proactive notification obligation when scope updates
occur was unspecced. D87 requires agents to be listed in `affected_agent_ids`; whether the
Orchestrator must proactively notify those agents (vs. agents discovering the scope change
at Gate rejection) was undefined.

**D91 partial resolution (GS3):** Orchestrator notifies agents listed in `affected_agent_ids`
as a best-effort operation; agents must not rely on proactive notification for safety-critical
behavior (Gate rejection is the authoritative enforcement mechanism).

**GS4 closure of OQ:** OQ-S-GAP28-1 (canonical) — "Should `SCOPE_UPDATED` carry
`scope_change_type: EXPANDING | NARROWING | RESTRUCTURING` to enable per-type notification
policy?" — Closed. GS4 §2.3 payload requires `scope_change_type` as a mandatory field in
the SCOPE_UPDATE CeremonyToken payload. `SCOPE_UPDATED` Ledger entry carries this field.
Orchestrator may apply per-type notification logic at its discretion.

**Remaining:** Formal documentation of the per-type notification policy design space;
whether "best-effort" notification needs a delivery guarantee specification (e.g., must
attempt once before expiry). No downstream blocks identified; may be accepted as
implementation-time detail.

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
**Status:** Deferred to v2 — scope extended (GS4)

**Description:** Key rotation for Orchestrator Operational Key (OOK) and Ceremony
Authorization Key (CAK). First-boot OOK is not rotated in v1. CAK rotation ceremony design
is not specified in v1. Full PKI (rotation ceremonies for both keys) is v2 scope.

**GS4 scope extension:** GAP-19 originally covered OOK rotation only. GS4 extended scope
to include CAK rotation alongside OOK rotation. Both keys share the v2 rotation deferral.
OQ-S-CAK-1 (v2 CAK rotation ceremony design) is the open question governing this gap.

**Open questions:**
- `OQ-S-CAK-1`: v2 CAK rotation ceremony design — procedure for replacing the
  `ceremony_authorization_key_anchor` in `genesis-seal.json` (Tier 1, mint-once) without a
  full re-genesis.
- `OQ-S-CAK-2`: Multi-operator quorum / m-of-n signing for CAK ceremonies (v2). Would
  allow multiple registered CAK principals without relying on a single human-held device.

---

## Active Tensions Requiring Gap Sessions

---

### T13 — Advisory Boundedness vs. Operational Flexibility
*(Promoted from GS1 T-NEW-1 to tension map by Post-GS3 checkpoint)*

**Status:** 🔴 Open — requires gap session
**Specialists:** MEMIT Specialist + Orchestration Comparativist
**Scheduled:** GS7 (after SCT sessions complete)
**Blocks:** v2 outline spec block 2c ratification (hard-block threshold provisional); Phase 2
exit.

**Core conflict:** `LARQL_VERSION_LEGACY` must be a bounded transition state (MEMIT: unbounded
accumulation degrades compaction fidelity). Teams in active development cannot be hard-blocked
mid-sprint by an elapsed notice period (Orchestration: enforcement must be predictable and
operator-override-capable).

**Resolution path:** MEMIT Specialist must provide empirical basis (or principled proxy) for
compaction fidelity degradation rate. Orchestration Comparativist must specify minimum
operator override window. `LEGACY_EXTENSION_GRANTED` (OQ-GAP1-3) is the candidate mechanism.
Hard-block threshold of 100 patches (v2 outline spec block 2c) is provisional pending T13
resolution and GAP-1 empirical input.

---

### T15 — CAK Availability vs. Ceremony Urgency
*(Surfaced in Gap Session 4; new to this backlog version)*

**Status:** 🟡 Partial — v1 mitigation documented; v2 resolution required
**Specialists:** Warden + Orchestration Comparativist
**Scheduled:** v2 (GS after OQ-S-CAK-1 and OQ-S-CAK-2 are scoped)

**Core conflict:** D92 requires the CAK to be human-held on a hardware security token or
encrypted offline media, physically separate from all networked systems. Unplanned ceremonies
(circuit reset following an incident) may require CAK access when the primary CAK custodian
is unavailable, or when the CAK has been declared compromised (rendering `CAK_COMPROMISE_DECLARED`
written but all ceremonies blocked with no v1 rotation path).

**v1 mitigation (operational, not specced):** First-boot registration ceremony must designate
at minimum one backup custodian — a second person with physical access to the same CAK
storage medium. This is an operational deployment requirement.

**⚠️ Deployment note:** v1 supports exactly one registered CAK anchor in
`genesis-seal.json`. A "second registered CAK" is not a v1 spec capability. The backup
custodian model is a second person with access to the same CAK medium, not a second
registered key. This distinction must be explicit in v1 deployment guidance.

**v2 resolution path:** OQ-S-CAK-1 (rotation ceremony) + OQ-S-CAK-2 (quorum signing /
m-of-n CAK principals).

---

## Resolved Tensions (Closed in GS4)

---

### T14 — Single-Key vs. Dual-Key for Ceremony Authorization ✅ Resolved
*(Promoted from OQ-S-GAP26-3 / GS3 implicit tension by Post-GS3 checkpoint)*

**Resolution:** D92 (Gap Session 4)

**Resolution summary:** Dual-key hierarchy is mandatory. The Ceremony Authorization Key
(CAK) MUST be separate from the Orchestrator Operational Key (OOK). Security argument: OOK
private key resides on the harness filesystem by design — a compromised agent with filesystem
read access could use a single-key model to self-authorize scope expansions. Operational
assessment: ceremony frequency (at most once per hour for scope updates per D89; less
frequent for manifest ratification and Genesis lifecycle events) makes human-held key
overhead acceptable. Hardware security token portability satisfies the on-call availability
requirement.

---

## Closed Administrative Gaps

---

### AG-1 — Per-`agent_id` vs. Global Rate Limit Scope — ✅ Closed by Annotation

**Description:** GS3 carried `OQ-S-GAP26-2` (pre-canonical numbering): "Should rate limit
be per-`agent_id` or global across all agents?" GS4 did not reference this OQ by number;
GS4's internal `OQ-S-GAP26-2` referred to a different question (retention/rotation cadence).

**Resolution:** GS3 D89's language "Rate limit check MUST precede signature verification
in processing order. Rejection produces `SCOPE_UPDATE_RATE_EXCEEDED`... for the same
`agent_id`" constitutes an implicit per-agent scope decision. This is treated as the adopted
scope. The per-agent vs. global tradeoff (multi-agent-ID spray attack surface) is a residual
item for GAP-27's GS7 session to formally document, not a decision requiring reversal.

**OQ status:** `OQ-S-GAP26-2` (GS3 pre-canonical) — Closed by annotation. Tracking entry
retired.

---

## Inconsistency Findings

| ID | Description | Status | Resolution Path |
|----|-------------|--------|-----------------|
| INCON-1 | GS2 Amendment A1 does not bound TC compensation to reversal-only. Creates unbounded write path under READ_ONLY mode (D-CRC-3, C-CRC-3). | ⚠️ Outstanding | A1-REVISED — §11.8.1 amendment text not yet in integrated spec. Execute in GS5. |
| INCON-2 | GAP-ID naming collision in GS1/GS2 session summaries. | ✅ Resolved | D-CRC-1; canonical IDs established in gap-backlog-v2.md; stable in v3. |
| INCON-3 | IC-MANIFEST-1 `ratification_signature` field (GS1) is inconsistent with GS4 CeremonyToken model (D93). Manifest entry self-signing conflicts with CeremonyToken-as-authorization-object model. | 🟠 Required action | Amendment A9 — replace `ratification_signature` in IC-MANIFEST-1 with `ceremony_token_id: string`. Manifest commit gate must verify referenced `CEREMONY_ACCEPTED` Ledger entry exists and `manifest_hash` matches. Address in GS1 v2 work or next GS touching GAP-20. |

---

## Amendment Obligations

*Required before v1.2 or v2 integration. Sorted by urgency.*

| Ref | Section / Target | Amendment | Status |
|-----|-----------------|-----------|--------|
| A1-REVISED | §11.8.1 | TC compensation exemption bounded to reversal-only (D-CRC-3, C-CRC-3): "A compensation write that would produce any weight change beyond the reversal of the prior committed operation MUST be rejected and treated as a TC fault, triggering an additional circuit trip event." | ⚠️ Outstanding — execute in GS5 |
| A2-GS2 | §11.8.1 | Precondition check error handling: "Precondition check errors — system failure during verification, as distinct from precondition check failures where the state is known — are treated as precondition failures. The reset ceremony is rejected and `CIRCUIT_RESET_REJECTED` is written." | Outstanding |
| A3-IC-TC-RESET | §11.8.1 IC-TC-RESET | Circuit reset ceremony must use `CeremonyToken` with `ceremony_type: CIRCUIT_RESET`, signed by CAK. OOK-signed tokens rejected at step 3. Precondition verification (D84) executes only after full five-step ceremony token verification. (D92, D93, D95, D96, C-CAK-4) | ✅ Populated — D96 (GS4) |
| A4-§14.3 | §14.3 | Replace 3 consecutive → 2 consecutive `SCOPE_HASH_MISMATCH` escalation threshold. Add `SCOPE_MISMATCH_ESCALATED` (SECURITY, synchronous) on 2nd consecutive mismatch for same `invocation_id`. (D88) | Outstanding |
| A5-§10.9 | §10.9 | Add ceremony authorization verification requirement: Orchestrator MUST verify `operator_signature` against declared ceremony authorization key (now: CAK, `ceremony_authorization_key_anchor`) before writing `SCOPE_UPDATED`. Ceremony with unverifiable signature MUST be rejected; no Ledger entry written; no registry update. (D90, C-S-GAP25-1, D93) | Outstanding |
| A6-§10.9 | §10.9 | Add rate limit requirement: scope update ceremony MUST be rejected if elapsed time since previous `SCOPE_UPDATED` for same `agent_id` is less than `scope_update_min_interval_seconds` (Tier 1; provisional default 3,600 s). Rejection produces `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, synchronous). Rate limit check precedes signature verification. (D89, C-S-GAP26-1, C-S-GAP26-2) | Outstanding |
| A7-Appendix-C | Appendix C | Add from GS3: `DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE, sync), `HOLD_RELEASE_REJECTED` (SECURITY, sync), `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, sync), `SCOPE_MISMATCH_ESCALATED` (SECURITY, sync). Add cross-category rationale annotation for circuit breaker workflow entries. | Outstanding |
| A7b-Appendix-C | Appendix C | Add from GS4: `CEREMONY_ACCEPTED` (GOVERNANCE, sync), `CEREMONY_SIGNATURE_INVALID` (SECURITY, sync), `CEREMONY_REPLAY_REJECTED` (SECURITY, sync), `CEREMONY_REPLAY_THRESHOLD_EXCEEDED` (SECURITY, sync), `CAK_REGISTERED` (GOVERNANCE, sync), `CAK_COMPROMISE_DECLARED` (SECURITY, sync). Mark `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` as deprecated, referencing unified successors. | Outstanding |
| A8-Appendix-C | Appendix C | Add cross-category rationale annotation for circuit breaker workflow entries (GS2 T-NEW-1): `CIRCUIT_TRIPPED` (CONSISTENCY — two mediums in problematic relationship), `CIRCUIT_RESET` (GOVERNANCE — human-authorized write resumption), `CIRCUIT_RESET_REJECTED` (SECURITY — unauthorized or unverifiable reset attempt). | Outstanding |
| A9-IC-MANIFEST-1 | IC-MANIFEST-1 (GS1 output, subject to v2 ratification) | Replace `ratification_signature: string` with `ceremony_token_id: string` (ID of `CEREMONY_ACCEPTED` Ledger entry for the `MANIFEST_RATIFICATION` ceremony). Add manifest commit gate requirement: gate MUST verify the referenced Ledger entry exists and its payload `manifest_hash` matches the manifest being committed. (INCON-3, D93 §2.1) | 🟠 Required — address in GS1 v2 work or next GAP-20 session |
| A10-§13.2 | §13.2 `genesis-seal.json` | Add `ceremony_authorization_key_anchor` field: CAK public key fingerprint. Tier 1, mint-once. Value set at first-boot CAK registration ceremony; immutable post-genesis. (D92, D94, C-CAK-2) | Outstanding — pending SCT review confirmation |
| A11-deployment-guidance | Deployment guidance / v1 operator notes | Clarify: v1 supports exactly one registered CAK anchor. "Backup custodian" means a second person with physical access to the same CAK storage medium — not a second registered key. Second registered CAK is not a v1 capability (v2: OQ-S-CAK-2). (T15) | Outstanding |

---

## Summary Table

| GAP | Domain(s) | Priority | Status | Blocks |
|-----|-----------|----------|--------|--------|
| GAP-1 | MEMIT | 🔴 Critical | Formally deferred (implementation) | GAP-9, backpressure, circuit-breaker rationale |
| GAP-2 | MEMIT | 🔴 Critical | Formally deferred (implementation) | GAP-1, layer targeting, edge caps |
| GAP-3 | MEMIT + Graph | 🔴 Critical | 🔶 Partial (GS1; INCON-3 adds A9 requirement) | Gate pre-check, Validator L1, v2 migration, T13 |
| GAP-4 | Orchestration | 🟠 High | Open | Delegation token v2 shape, HIL interface |
| GAP-5 | Warden + MEMIT | 🟠 High | ✅ Resolved (GS3 / D87) | — |
| GAP-6 | State Consistency | 🟠 High | ✅ Resolved (GS2 / D84); A1-REVISED outstanding | — |
| GAP-7 | State Consistency | 🟠 High | ✅ Resolved (GS2 / D85) | — |
| GAP-8 | Validation | 🟠 High | Open | Meta-Validator readiness |
| GAP-9 | Validation + MEMIT | 🟡 Medium | Open (blocked GAP-1) | — |
| GAP-10 | Validation | 🟡 Medium | Open | — |
| GAP-11 | State Consistency + MEMIT | 🟡 Medium | Open | — |
| GAP-12 | State Consistency | 🟡 Medium | Open | — |
| GAP-13 | Warden + Orchestration | 🟡 Medium | Open | — |
| GAP-14 | State Consistency + Orchestration | 🟡 Medium | Open | — |
| GAP-15 | Validation + MEMIT | 🟡 Medium | Open (blocked GAP-1) | — |
| GAP-16 | Warden + Orchestration | 🟢 Low | Accepted (deployment-specific) | — |
| GAP-17 | Orchestration + State Consistency | 🟢 Low | Deferred to v2 | — |
| GAP-18 | State Consistency | 🟢 Low | Deferred to v2 | — |
| GAP-19 | Warden | 🟢 Low | Deferred to v2 (scope extended GS4: OOK + CAK) | — |
| GAP-20 | MEMIT + Graph | 🟠 High | Open (INCON-3: A9 required) | GAP-3 spec blocks 2a/2c |
| GAP-21 | State Consistency + Warden | 🟠 High | Open (GS4 ceremony model integrated; Appendix C amendment outstanding) | GAP-23 |
| GAP-22 | State Consistency | 🟠 High | Open | — |
| GAP-23 | State Consistency | 🟠 High | Blocked (GAP-21) | Genesis recovery path |
| GAP-24 | State Consistency + Warden | 🟡 Medium | Open | — |
| GAP-25 | State Consistency + Warden | 🟠 High | Open (SCT review from GS4 feeds this gap) | D87 trust guarantee |
| GAP-26 | Warden + Orchestration | 🟠 High | ✅ **Resolved** (GS4 / D92–D96) | — |
| GAP-27 | Warden + State Consistency | 🟠 High | 🟢 **Unblocked** (GAP-26 resolved; GS7) | D89 completeness |
| GAP-28 | Orchestration | 🟡 Medium | 🔶 Partial (GS4 closed scope_change_type OQ; D91 partial) | — |
| T13 | MEMIT + Orchestration | — (Tension) | 🔴 Open — GS7 required | GAP-3 block 2c |
| T14 | Warden + Orchestration | — (Tension) | ✅ **Resolved** — D92 (GS4) | — |
| T15 | Warden + Orchestration | — (Tension) | 🟡 Partial — v1 mitigation documented; v2 required | — |

---

## Recommended Gap Session Sequencing (Updated Post-GS4)

| Session | Primary Specialists | Topics | Rationale |
|---------|---------------------|--------|-----------|
| **GS5** | State Consistency + Warden | SCT review from GS4 (Merkle chain integrity, `genesis-seal.json` schema status, `CAK_REGISTERED` first-boot sequencing); GAP-25 (Ledger → registry propagation); GAP-21 (TC timeout field / Genesis Hold lifecycle); A1-REVISED execution | **Required before any other sessions**; SCT review must complete first |
| **GS6** | State Consistency | GAP-22 (`TIMED_OUT` field for Genesis); GAP-23 (Genesis Hold lifecycle through reset ceremony) | Requires GAP-21 closure from GS5 |
| **GS7** | MEMIT + Orchestration Comparativist | T13 (advisory boundedness vs. operational flexibility); GAP-27 (rate limit spec completion, now unblocked) | Required for Phase 2 exit; GAP-27 was unblocked by GS4 |
| **GS8** | Validation Contract Architect | GAP-8 (Meta-* corpus authorship policy); GAP-10 (constitutional test classification) | Independent; can run in parallel with GS6 |
| **Amendment session** | Graph Data Architect + State Consistency | INCON-3 (Amendment A9 to IC-MANIFEST-1); GAP-20 full manifest format spec | Can fold into GS5 or GS1 v2 work; not a standalone session requirement |

---

## Phase 2 Exit Criteria — Current Status

| Criterion | Status | Notes |
|-----------|--------|-------|
| All Critical and High priority gaps resolved | ❌ Not met | GAP-3 partial; GAP-4, GAP-8, GAP-20, GAP-21, GAP-22, GAP-23, GAP-25, GAP-27 open or unblocked |
| All Medium gaps resolved or explicitly deferred with rationale | ❌ Not met | GAP-9 through GAP-15, GAP-24, GAP-28 open or partial |
| All Low gaps addressed or accepted | ✅ Met | GAP-16 accepted; GAP-17, GAP-18, GAP-19 deferred with rationale |
| Most recent council review produced no new unresolved tensions | 🔶 Partial | T15 introduced — 🟡 Partial (v1 mitigation documented; not a 🔴 Open blocker) |
| `gap-backlog-v3.md` updated with final status of all gaps | ✅ This document | Produced by Post-GS4 council review checkpoint |

**Phase 2 cannot close.** Minimum next actions: GS5 (SCT + Warden), GS6 (State Consistency),
GS7 (MEMIT + Orchestration). Progress since Post-GS3: GAP-5, GAP-6, GAP-7, GAP-26 fully
resolved; T14 resolved; GAP-27 unblocked; GAP-28 partially closed.

---

## Council Observations — Cross-Gap Patterns (Updated Post-GS4)

**Write Engine Foundation (GAP-1, GAP-2, GAP-3):** Formally deferred (GAP-1, GAP-2) or
partially closed (GAP-3). All threshold values remain provisional pending empirical validation.
GS4's INCON-3 adds Amendment A9 as a required integration task before GAP-3 spec block 2a
can be considered consistent with the unified ceremony model.

**Transaction Controller Completeness (GAP-6, GAP-7 resolved; GAP-21, GAP-22, GAP-23, GAP-24
open):** The TC's primary failure modes are specced. The Genesis-specific lifecycle (Hold
through reset ceremony) and timeout field semantics remain the current bottleneck. GAP-21
unblocks GAP-23; both are GS5/GS6 targets. GS4 strengthened the circuit reset ceremony
authorization (A3, D96) without resolving the Hold lifecycle questions.

**Ceremony Authorization Convergence (resolved at framework level, integration pending):**
T14 resolved; GAP-26 resolved; unified CeremonyToken framework established. Three integration
tasks remain: (1) A9 (IC-MANIFEST-1 reconciliation — INCON-3), (2) Appendix C additions
(A7, A7b), (3) SCT review confirmation before genesis-seal.json amendment (A10) executes.
The ceremony authorization layer is architecturally complete for v1; the integration surface
requires three targeted amendment sessions.

**Operational Risk Concentration (T15, GAP-19):** GS4 created a new operational risk cluster
around the CAK. The CAK is the sole governance authority (C-CAK-2); a compromised or
unavailable CAK with no v1 rotation path creates system halt. T15 documents the availability
risk; GAP-19's v2 scope covers the rotation protocol. Both are v2 blockers but not v1
Phase 2 blockers.

---

*Gap Backlog v3.0 — 28 gaps + 2 active tensions (T13, T15) + 1 resolved tension (T14) tracked*
*Supersedes gap-backlog-v2.md*
*Based on: gap-backlog-v2.md + Gap Session 4 + Framework Council Review Checkpoint Post-GS4*
*Council Review Checkpoint: Post-GS4*
