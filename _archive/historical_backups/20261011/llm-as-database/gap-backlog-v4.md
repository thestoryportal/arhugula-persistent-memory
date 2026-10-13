# LLM as Database: Agent Harness Architecture
## Gap Backlog v4.0

> **Supersedes:** `gap-backlog-v3.md`
> **Source sessions reconciled:**
>   v1 schedule: GS1 (GAP-3), GS2 (GAP-6/7), GS3 (GAP-5), GS4 (GAP-8 residual / GAP-10)
>   v3 schedule: GS5 (GAP-21/24/25 + SCT review + A-batch), GS6 (GAP-22/23),
>                GS7 (T13/GAP-27/GAP-20 + A4–A9), GS8 (GAP-8/GAP-10 final),
>                GS9 (GAP-11/12/14/28)
>   GS4 (v2/v3 schedule): T14/GAP-26 (documented in gap-backlog-v3.md)
> **Remaining:** GS10 (full council — GAP-4/9/13/15/17/18/19/T15) — NOT YET RUN
> **Status:** Post all non-council sessions across v1 and v3 schedules
> **Total gaps tracked:** 39 (original 28 + 11 new gaps surfaced in sessions)
> **Active tensions requiring sessions:** T15, T16, T-candidate-GS7 (dry-run freshness)
> **Resolved tensions:** T13 (Advisory Boundedness) ✅, T14 (Single-Key vs. Dual-Key) ✅
>
> ---
> **⚠️ Decision Numbering Collision Warning**
> Sessions across v1, v2, and v3 schedules were run non-sequentially. Each session
> assigned provisional decision IDs (D-numbers) locally without global coordination.
> Known collisions:
> - v1 GS4 assigned D89–D92 for corpus/constitutional decisions
> - v2/v3 GS4 assigned D92–D96 for CAK/CeremonyToken framework (gap-backlog-v3.md)
> - v3 GS5 assigned D97–D103; v3 GS8 assigned D93–D98; v3 GS9 assigned D99–D111
>
> Resolution policy for this backlog: gap status tracks by session reference and
> content description. D-number reconciliation is required before v1.2 spec integration.
> The v3 GS8 decisions on GAP-8/GAP-10 supersede v1 GS4 decisions on the same gaps
> (later session, more complete baseline). Where D-numbers are cited they are session-local.

---

## Status Labels

| Status | Meaning |
|--------|---------|
| ✅ **Resolved** | Fully closed; spec block produced; no remaining action |
| 🔶 **Partial** | Partially closed; residuals remain |
| 🔴 **Open** | Not yet addressed in any completed session |
| ⏳ **Deferred** | Formally deferred with rationale |
| 🔜 **Pending GS10** | Blocked on remaining council session |
| 🔒 **Accepted** | Accepted as deployment-specific / not spec-owned |

---

## 🔴 Critical — Blocks 3 or More Other Gaps

---

### GAP-1
**Domain:** MEMIT Specialist | **Priority:** 🔴 Critical | **Status:** ⏳ Formally deferred — implementation phase

All drift/compaction threshold values empirically unvalidated (OQ-W1). Drift warning 1,500 edges, hard trigger 8,000 edges, sub-batch ceiling 2,000 edges, overlay file count trigger 50, p95 latency 2×, stale_urgent ceiling 1,000 edges, 24h Pruning floor.

**Blocked by:** Target model selection + write-volume stress test. Cannot resolve through spec work.
**Blocks:** GAP-9, GAP-15 (compaction sampling), backpressure rationale, circuit-breaker threshold rationale, T13 hard-block threshold M calibration, IC-MANIFEST-1 bucket_map thresholds.

**GS7 v3 impact:** T13 ratified three-tier model with threshold M (r≥0.25, count≥75) marked **provisional pending GAP-1 empirical calibration of per-hop error coefficient ε**. IC-MANIFEST-1 bucket_map thresholds similarly provisional.

---

### GAP-2
**Domain:** MEMIT Specialist | **Priority:** 🔴 Critical | **Status:** ⏳ Formally deferred — implementation phase

MEMIT compatibility with target model architecture unverified (OQ-W2). Layer coordinates L15–L25 (32-layer model), FFN width, architecture variant (MoE, Mamba, GQA) unverified.

**Blocked by:** Target model selection + MEMIT compatibility test run.
**Blocks:** Layer targeting correctness, edge cap justification, GAP-1 resolution, attention_weight divergence check validity.

---

### GAP-3
**Domain:** MEMIT Specialist, Graph Data Architect | **Priority:** 🔴 Critical | **Status:** 🔶 Partial

Runtime chain (Gate → migration_context → MEMIT → versioned parser) verified closed (v1.1 / GS1 v1). Three v2 outline spec blocks produced (GS1 v1). IC-MANIFEST-1 ratified with A9 amendment (GS7 v3). T13 resolved and spec block 2c upgraded from outline to ratified (GS7 v3).

**GS1 v1 seam:** Manifest authorship update atomicity (`current_larql_version` can advance without manifest update — silent compile break). Addressed partially by IC-MANIFEST-1 commit gate verification in GS7.

**Remaining v2 residuals:**
- (a) T1 translation bucket thresholds — provisional pending GAP-1
- (b) Compaction abort recovery for translation failure (`COMPACTION_TRANSLATION_HEAVY`) — outlined only
- (d) Schema extension proposal pathway (agents proposing new relation types) — unspecced
- Manifest lattice completeness probe — see GAP-29 (new)

**Blocks:** v2 migration planning, complete Gate pre-check spec.

---

## 🟠 High — Blocks 1–2 Gaps or Load-Bearing Decisions

---

### GAP-4
**Domain:** Orchestration Comparativist | **Priority:** 🟠 High | **Status:** 🔜 Pending GS10

Path A/B/C selection operator-decided (D72). Delegation token design and HIL interface mechanism path-dependent.

**Blocked by:** Operator path selection. **Produces in GS10:** Three contingent spec blocks (one per path).

---

### GAP-5
**Domain:** Warden + MEMIT | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS3 v3 / D87 / IC-SCOPE-UPDATE)

Mid-flight scope update model verified closed. Residual seams catalogued as GAP-25 through GAP-28; all four now resolved (GAP-25 in GS5 v3, GAP-27 in GS7 v3, GAP-28 in GS9 v3, GAP-26 in GS4 v2/v3).

**Refinements applied from GS3 v1 session:**
- R-S3-1: SCOPE_HASH_MISMATCH escalation threshold 3→2 (applied as A4 in GS7 v3) ✅
- R-S3-2: Ledger single-writer serialization stated as explicit contract (addressed in GS5 via D103 SCOPE_RECONCILE protocol) ✅
- R-S3-3: `governing_scope_hash` field on commit Ledger entries (PREPARED→COMMIT preserving governing scope hash) — **outstanding**, not confirmed applied in any session summary. Surfaces as new gap item, see GAP-34.

---

### GAP-6
**Domain:** State Consistency Theorist | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS2 v1 / D84 / IC-TC-RESET)

Circuit breaker reset authority fully specced. READ_ONLY mode automatic; write resumption via signed CAK ceremony (A3/D96 from GS4); TC independently verifies preconditions per trip type.

**Amendments applied:**
- A1-REVISED (§11.8.1 reversal-only bounding) ✅ applied GS5 v3
- A2-GS2 (§11.8.1 precondition check error handling) ✅ applied GS5 v3
- A3/IC-TC-RESET (CAK-based ceremony authorization) ✅ applied GS4 v2/v3, confirmed GS5
- A8 (cross-category Appendix C annotation) ✅ applied GS5 v3
- A12 (Genesis-trip precondition branch) ✅ applied GS6 v3

**Residual seams from GS2 v1 — addressed:**
- NEW-GAP-SC-1 (in-flight token fate at trip): see GAP-30 (new)
- NEW-GAP-SC-2 (precondition verification infrastructure failure): A2-GS2 applied ✅
- NEW-GAP-SC-3 (rate limiting on repeated CIRCUIT_RESET_REJECTED): see GAP-31 (new)
- NEW-GAP-SC-4 (governance write carve-out during CIRCUIT_TRIPPED): A1-REVISED addresses this; explicit carve-out language status unclear — see GAP-32 (new)

---

### GAP-7
**Domain:** State Consistency Theorist | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS2 v1 / D85 / IC-TC-TIMEOUT)

Two-value PREPARED timeout model (incremental default 2h; Genesis operator-set, Gate-blocked until present). Incremental timeout: Phase 1 rollback, Hold persists, retry as infrastructure failure. Genesis timeout: circuit trip DIVERGED_STATE, forensic preservation, no auto-compensation.

---

### GAP-8
**Domain:** Validation Contract Architect | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS8 v3, superseding GS4 v1)

**GS8 v3 (definitive resolution):**
- **D93 (GS8):** `corpus_author_identities` relocated from Tier 1 to new Tier 2 sealed artifact `corpus-author-registry/`. Tier 1 retains `corpus_author_bootstrap_identity` (single-use, signs registry v1 manifest only). Six Tier 2 sealed corpora total (was 5 in v1.1).
- **D94 (GS8):** Cadence: 90-day staleness advisory → 180-day enforced `HEALTH_SCORE_STALE` (fact-based TC dispatch gating; no automatic suspension at 180d — operator 180d remediation; suspension at same path as <85% threshold if unremediated).
- **D95 (GS8):** Five Day-0 deployment preconditions (two hard blocks: bootstrap identity present, registry v1 populated; three degraded-run markers: ≥20 cases in each Meta-* corpus, ≥1 constitutional test). `CORPUS_INIT_STATE` Ledger entry at Genesis.

**ICs:** IC-CORPUS-REG1, IC-CORPUS-REG2, IC-CORPUS-CADENCE1.

**Note on D numbering:** GS4 v1 had earlier provisional D89–D91 for corpus cadence decisions; GS8 v3 decisions are authoritative as they were produced on the updated baseline.

---

### GAP-20
**Domain:** MEMIT Specialist, Graph Data Architect | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS7 v3 / IC-MANIFEST-1 ratified)

`larql_migration_manifest` format fully specified. IC-MANIFEST-1 ratified with A9 amendment (INCON-3 closed). Key decisions from GS7 v3:

- **Architect Agent authorship permitted** under standard token/gate model; ratification is CAK-signed MANIFEST_RATIFICATION CeremonyToken (not agent-controlled).
- **Dry-run mandatory:** protocol defined, acceptance criteria (zero translation failures, zero unexpected VERSION_REJECTED), 7-day freshness window on dry-run artifact hash.
- **Manifest commit gate:** seven ordered verification checks against CEREMONY_ACCEPTED Ledger entry.
- **Fields:** source_version, target_version, field_mappings (ordered, transform_type ∈ {RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT}), bucket_map (provisional thresholds pending GAP-1), ceremony_token_id, dry_run_artifact_hash.

**New gaps surfaced by resolution:** GAP-33 (dry-run artifact storage — owner: Warden + Graph Data Architect).

---

### GAP-21
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS5 v3)

`DEPENDENCY_HOLD_RELEASED_SIGNED` (GOVERNANCE, sync) formalized in Appendix C. CeremonyToken model (ceremony_type: HOLD_RELEASE, CAK-signed per GS4 D93) integrated. `release_reason` enum finalized as closed 4-value set: `{TIMEOUT_NO_RETRY, GENESIS_RESET_PREPARATION, OPERATOR_OVERRIDE, RECONCILIATION_RESUME}`. `HOLD_RELEASE_REJECTED` superseded by unified `CEREMONY_SIGNATURE_INVALID` / `CEREMONY_REPLAY_REJECTED` with ceremony_type discriminator. Unblocks GAP-23.

**Constraints:** C-HOLD-REL-1 through C-HOLD-REL-3.
**IC:** IC-HOLD-RELEASE-SIGNED-1 (now IC-HOLD-RELEASE per GS5 name).

---

### GAP-22
**Domain:** State Consistency Theorist | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS6 v3)

`TIMED_OUT` schema for Genesis case: resolution path (b) chosen. `GENESIS_TIMED_OUT` (CONSISTENCY, sync) added to Appendix C with seven fields and no `compensation_direction`. `TIMED_OUT` scope narrowed to non-Genesis transactions only (C-TIMED-OUT-1). IC-TC-GENESIS amended to use GENESIS_TIMED_OUT; category corrected to CONSISTENCY.

**Warden co-review obligation:** GENESIS_TIMED_OUT classified as CONSISTENCY (not GOVERNANCE) — pending confirmation that this is acceptable for audit queries given operator ceremony precursors live under GOVERNANCE.

---

### GAP-23
**Domain:** State Consistency Theorist | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS6 v3)

Genesis Hold lifecycle after timeout circuit trip fully specified. All three questions answered:
1. **Yes** — Hold release IS a precondition for IC-TC-RESET Genesis-trip variant (C-GEN-REC-1). Amendment A12 applied.
2. **CIRCUIT_RESET does NOT implicitly release Holds.** Strict ordering: Hold release(s) → reconciliation → reset (C-GEN-REC-2).
3. **New Genesis cannot acquire Hold** while failed Genesis Hold is active — blocked by circuit state AND Hold Registry conflict at Gate pre-check. Latent deadlock eliminated structurally.

Operator playbook (Steps 1–5) produced. `release_reason: GENESIS_RESET_PREPARATION` from GAP-21 enum is the mechanism.

**Constraints:** C-TIMED-OUT-1, C-GEN-REC-1, C-GEN-REC-2, C-GEN-REC-3.
**ICs:** IC-TC-GENESIS (amended), IC-TC-RESET (amended via A12).

---

### GAP-25
**Domain:** State Consistency Theorist (primary) + Warden | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS5 v3)

Scope Registry Reconciliation: dedicated post-boot Orchestrator startup phase, gated on §13.5 full pass. `SCOPE_UPDATED` propagation lag ceiling: 5 seconds (OQ-S-GAP24-1 closed). Durable checkpoint at `<harness_root>/.orchestrator-state/` closes OQ-S-GAP24-2. DIVERGED_STATE triggered only on reconciliation application failure; LEDGER_SIGNATURE_REVERIFICATION_FAILED via W3 on tampering detection. Signature reverification against currently-active CAK anchor.

**Constraints:** C-SCOPE-REC-1 through C-SCOPE-REC-4.
**ICs:** IC-SCOPE-RECONCILE.
**GS4 SCT Condition 3 answered (GS5):** CAK anchor inherits file-level dual-store from Genesis Seal; new semantic verification step 3a inserted in §13.5 between OOK (step 3) and sealed corpora (step 4). Sub-checks: presence, field↔Ledger reconciliation (against CAK_REGISTERED), dual-key invariant (CAK≠OOK), compromise-declared check.

---

### GAP-26
**Domain:** Warden + Orchestration | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS4 v2/v3)

Unified CeremonyToken framework (D93): four ceremony types (MANIFEST_RATIFICATION, HOLD_RELEASE, SCOPE_UPDATE, CIRCUIT_RESET). CAK physical storage contract (D94): hardware security token preferred; encrypted offline file acceptable; filesystem prohibited (C-CAK-1). IC-SCOPE-AUTH-1 ratified (D95). IC-TC-RESET A3 populated (D96) — circuit reset requires CeremonyToken ceremony_type: CIRCUIT_RESET, CAK-signed. D-CRC-4 satisfied. Constraints C-CAK-1 through C-CAK-5, C-CRC-4 through C-CRC-6.

---

### GAP-27
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟠 High | **Status:** ✅ Resolved (GS7 v3, extended by v2 GS7)

**v3 GS7:** D89 ratified. `scope_update_min_interval_seconds` (Tier 1, provisional default 3,600s), per-`agent_id` scope confirmed (AG-1). Rate limit check precedes signature verification. Multi-agent-ID spray attack residual formally documented.

**v2 GS7 extension (reconciliation required):** v2 GS7 produced a richer dual-layer rate-limit model and **placed the interval at Tier 3** (not Tier 1):
- **Primary layer (per-ceremony-initiator):** keyed on `operator_id` from CAK fingerprint. Closes the evasion vector where the same CAK targets different agent_ids to circumvent per-agent limits.
- **Secondary layer (per-affected-agent-id):** defense against per-agent starvation attacks. Both layers checked; per-initiator violation reported first.
- **Tier 3 placement:** `scope_update_min_interval_seconds` in `.harness/rate-limits.json` (new Tier 3 file). Rationale: Tier 1 is mint-once; rate limits should be operator-tunable post-bootstrap.

**Conflict:** v3 GS7 confirmed Tier 1 placement; v2 GS7 argued Tier 3 (stronger operational argument). The Tier 3 placement from v2 is architecturally sounder — Tier 1 mint-once is inappropriate for a tunable operational parameter. This conflict requires GS13 or integration-pass resolution.

**v2 GS7 open tensions from this gap:** T-S7-N1 (rate-limit state derived vs. primary — see tension map). New gaps: GAP-45 (rate-limit state durability across restart, Low), GAP-46 (ceremony_initiator_id attribution under key rotation, Medium).

---

## 🟡 Medium — Self-Contained, No Downstream Spec Dependencies

---

### GAP-9
**Domain:** Validation + MEMIT | **Priority:** 🟡 Medium | **Status:** 🔶 Partial — v2 GS10 produced resolution; v3 schedule treated as deferred; reconciliation required

**v2 GS10 resolution (applies independently of GAP-1):** L2 probe generalized to a three-member probe family: (1) **Generation probe** — model generates a response; assertion checks expected content is present; (2) **Assertion probe** — model evaluates a factual claim (true/false/unknown); criterion: correct classification at ≥ threshold; (3) **Constraint probe** — model generates a completion; assertion checks a structural/semantic constraint on the output. All three use a shared deterministic pass/fail contract: **Semantic Assertion Criterion** (SAC) — predicate over model output evaluable without running external code. Three judgment methods: string containment, embedding similarity (pinned threshold), pinned-version judge-model classification. Probe template authorship assigned to TGA as a sub-class of test artifact (preserves D32–D33 independence without exemption). "No auto-compile" scope (§11.13) extended to external source drift detection.

**v3 schedule treatment:** GS10 was projected to confirm formal deferral (blocked by GAP-1). v3 GS9 addressed GAP-11 (overlapping domain) but not GAP-9. Since v2 GS10 ran and produced a coherent resolution independent of GAP-1, the resolution stands for the domain-agnostic probe protocol. GAP-1 affects only the numeric threshold calibration for `judge_model_classification` — not the protocol structure.

**Remaining (from v2 GS10):** Threshold calibration for `judge_model_classification` (per-probe vs. per-domain vs. global) deferred. Retention policy for provenance content snapshots deferred. Handling of authenticated external sources deferred.

**GS13 role:** Confirm resolution status; record probe protocol as implementation baseline. No further spec work required for the protocol itself.

---

### GAP-10
**Domain:** Validation Contract Architect | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS8 v3, superseding GS4 v1)

**GS8 v3 (definitive resolution):**
- **D96 (GS8):** Dual-signal constitutional test tagging: directory placement in `constitutional-suite/` (primary trust boundary) AND `__constitutional__` module marker in each test file. Both required (C-CONSTITUTIONAL-DUAL). Incoherence → CONSTITUTIONAL_SUITE_MALFORMED (UNRECOVERABLE).
- **D97 (GS8):** Five qualification criteria Q1–Q5 (framework-level invariant; passes against CANONICAL_SNAPSHOT; no task-specific paths; authored by active delegation; deterministic).
- **D98 (GS8):** Promotion via standard Tier 2 versioned additive pattern with qualification attestation block in manifest. Single-operator signing for v1.1; multi-operator quorum deferred to v2 (§19 roadmap).

**ICs:** IC-CONSTITUTIONAL-1 (suite construction → Validator run), IC-CONSTITUTIONAL-2 (Tier 3 classification via C25).
**Open questions surfaced:** OQ-V7 (registry expiry enforcement), OQ-V8 (cadence differentiation Meta-V vs Meta-TGA), OQ-V9 (runtime Q5 structural validation) — all low priority.

**Note:** GS4 v1 also resolved GAP-10 (D91, D92 per that session). GS8 v3 sessions are authoritative.

---

### GAP-11
**Domain:** State Consistency + MEMIT | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS9 v3)

External document provenance for Layer 4 facts fully specced. Tracking mandatory (D99 GS9): Layer 4 fact without provenance block cannot be compiled (C-EXT-PROV1). Provenance record: 9 fields in `.larql` patch metadata + `EXTERNAL_PROVENANCE_RECORDED` Ledger entry (D100). Three-state staleness: FRESH/STALE/UNAVAILABLE, advisory-only (D101, C-EXT-PROV2); CORE facts raise REQUIRES_HUMAN_REVIEW on first detection. Monitoring: Pruning Agent `external_source_audit` sub-routine (D102, C-EXT-PROV3) — no new component. `refetch_policy` enum per-fact override.

**New OQ:** OQ-SC3 — reconciliation workflow for STALE Layer 4 facts (medium priority; candidate for GS10).
**ICs:** IC-EXT-PROV1, IC-EXT-PROV2.

---

### GAP-12
**Domain:** State Consistency | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS9 v3)

Ledger retention two-tier model (D103): Tier 1 `ledger_retention_floor` (default 7 years, immutable-downward); Tier 3 `ledger_active_period` (default 90 days, Tier 1 floor 30 days). Archive format `ledger-archive/v1` (D104): zstd level 19, SHA-256, Merkle root, chain-link anchors for cross-boundary verification. 7-step restore procedure specified. `PROJECT_CLOSED` synchronous and decoupled from archival I/O (D105): async archival with SLA-tracked `PROJECT_ARCHIVE_PENDING`; 30-day default SLA.

**Constraints:** C-RETENTION1 through C-RETENTION4.
**ICs:** IC-RETENTION1, IC-RETENTION2.
**OQ-SL1 closed.**

---

### GAP-13
**Domain:** Warden + Orchestration | **Priority:** 🟡 Medium | **Status:** 🔜 Pending GS10 (v2 outline)

Genesis automation level (OQ-S5). v1 mandates human review before write engine execution. v2 target: secondary LLM reviewer as human-review proxy.

---

### GAP-14
**Domain:** State Consistency + Orchestration | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS9 v3)

Async threshold rationale framework fully specced. Every threshold now binds to a named guarantee:
- **WAL flush (D106):** fsync-per-entry for CORE/SUPPORTING (zero-loss guarantee); group-commit for Layer 4 and async advisory (Tier 1 hard pin, not tunable).
- **Light verification 100 entries (D107):** ≤100-entry corruption-detection window.
- **Full verification 10,000 entries OR 24h (D108):** 24h audit-completeness guarantee.
- **Reconciliation backlog 10/7d warning; 50/30d critical (D109):** 7-day warn / 30-day circuit-breaker out-of-band sync SLA.
- **Threshold update ceremony (D110):** `ASYNC_THRESHOLDS_UPDATED` (CONFIG, signed); Tier 1 ordering invariants; fsync-per-entry for CORE/SUPPORTING is Tier 1 hard pin (unchangeable via ceremony).

**Constraints:** C-ASYNC1 through C-ASYNC4.
**IC:** IC-ASYNC1.
**T5/T11 thresholds: closed.**

---

### GAP-15
**Domain:** Validation + MEMIT | **Priority:** 🟡 Medium | **Status:** ⏳ Deferred; 🔜 Pending GS10 confirmation

Compaction verification sampling thresholds (OQ-OC3). SUPPORTING/INCIDENTAL sampling rates (20%, 10%) and abort thresholds (95%, 80%) provisional pending GAP-1. CORE threshold (1.0, C-OC3) is non-provisional. GS10 confirms formal deferral.

---

### GAP-24
**Domain:** State Consistency + Warden | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS5 v3)

Degraded Orchestrator during reset ceremony classified as operational failure (not W3). Stratified response: short outage — silent retry, operator CeremonyToken log is forensic artifact. Extended outage ≥ `orchestrator_unavailable_ceremony_escalation_threshold` (Tier 1, v1 default 15 minutes) → narrow W3 carve-out writing `ORCHESTRATOR_UNAVAILABILITY_ESCALATED` (SECURITY, sync).

**Constraints:** C-TC-RESET-DEG-1 through C-TC-RESET-DEG-3.
**IC:** IC-TC-RESET-DEGRADED.

---

### GAP-28
**Domain:** Orchestration | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (GS9 v3)

D91 ratified as final. Proactive notification: at-least-one-attempt-before-TTL (D111); 60s default TTL (Tier 3, 10s Tier 1 floor). Agent safety-critical operations MUST read SCOPE_UPDATED from Ledger; notification advisory only (C-NOTIFY3). Per-type notification policy (`scope_change_type` from GS4) operator-discretion; no spec-mandated differentiation.

**ICs:** IC-NOTIFY1, IC-NOTIFY2.

---

## 🟢 Low — Refinement Details

---

### GAP-16
**Domain:** Warden + Orchestration | **Priority:** 🟢 Low | **Status:** 🔒 Accepted — deployment-specific

Notification channels for integrity violations (OQ-S8). Out-of-spec by design for single-machine reference implementation.

---

### GAP-17
**Domain:** Orchestration + State Consistency | **Priority:** 🟢 Low | **Status:** 🔜 Pending GS10 (v2 outline)

Voluntary Write Lock release and inter-agent negotiation (OQ-CW1). No v1 mechanism.

---

### GAP-18
**Domain:** State Consistency | **Priority:** 🟢 Low | **Status:** 🔜 Pending GS10 (v2 outline)

Multi-machine Ledger replication (OQ-SL2). Single-machine only in v1.

---

### GAP-19
**Domain:** Warden | **Priority:** 🟢 Low | **Status:** 🔜 Pending GS10 (v2 outline, extended scope)

OOK and CAK rotation (scope extended in GS4). OQ-S-CAK-1 (v2 CAK rotation ceremony design); OQ-S-CAK-2 (m-of-n signing). CAK rotation challenge: `ceremony_authorization_key_anchor` is Tier 1 mint-once; GS5 v3 adds §13.5 step 3a interactions that rotation must account for.

---

## New Gaps Surfaced in v1 + v3 Sessions (Not in v3 Backlog)

---

### GAP-29
**Domain:** MEMIT Specialist + Warden | **Priority:** 🟠 High | **Status:** 🔴 Open
**Source:** GS1 v1 (manifest lattice completeness); GS5 v3 (W3 scope consolidation)

**Combined from two sources:**
- (GS1 v1) `larql_migration_manifest` does not require coverage of every version pair in `[min_supported_larql_version, current_larql_version]`. Missing lattice edge surfaces only at compaction time as translation failure. Natural home for completeness check: manifest authorship ceremony (now IC-MANIFEST-1) should enforce lattice completeness as a commit gate check.
- (GS5 v3) Three narrow W3 carve-outs introduced across GS4/GS5/GS6: DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF, ORCHESTRATOR_UNAVAILABILITY_ESCALATED, LEDGER_SIGNATURE_REVERIFICATION_FAILED. W3 originally single-purpose (INTEGRITY_VIOLATION_EMERGENCY only). GS6 v3 surfaces a potential fourth (HOLD_RELEASE_REASON_UNWARRANTED per GAP-31). Warden-led consolidation pass required.

**Blocked by:** Nothing. Self-contained. **Priority:** High (silent Tier 1 config error class).
**Resolution path:** (a) Add manifest lattice completeness check to IC-MANIFEST-1 commit gate (extend existing 7-check verification). (b) Warden reviews all W3 carve-outs, ratifies or restricts them in a consolidated policy document.

---

### GAP-30
**Domain:** State Consistency Theorist | **Priority:** 🟡 Medium | **Status:** 🔴 Open
**Source:** GS6 v3

`GENESIS_TIMED_OUT` → `CIRCUIT_TRIPPED` ordering monitoring. Both entries must appear in order within the sync-write window. No monitor specified for "GENESIS_TIMED_OUT with no subsequent CIRCUIT_TRIPPED." Entry type `GENESIS_TIMEOUT_TRIP_MISSING` reserved; detection path TBD.

---

### GAP-31
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟡 Medium | **Status:** 🔴 Open
**Source:** GS6 v3

Unwarranted use of `release_reason: GENESIS_RESET_PREPARATION`. If operator signs `DEPENDENCY_HOLD_RELEASED_SIGNED` with this reason but no matching `GENESIS_TIMED_OUT` exists in the audit window, TC must reject. Detection/rejection logic not yet specced. Entry type `HOLD_RELEASE_REASON_UNWARRANTED` reserved. **Warden question:** W3 eligibility for this entry type (would add a fourth W3 carve-out; ties to GAP-29 consolidation).

---

### GAP-32
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟢 Low | **Status:** 🔴 Open
**Source:** GS6 v3

Batch Genesis Hold release ceremony. If failed Genesis held N edges, operator must sign N separate HOLD_RELEASE ceremonies (operational burden scales with Genesis read-scope). Potential mitigation: `ceremony_type: GENESIS_HOLD_RELEASE_BATCH` covering all affected_hold_ids in a single CAK signature. Design tradeoff: ceremony-scope narrowness (Warden) vs. operational efficiency (SCT) — see T16. Deferred to v2.

---

### GAP-33
**Domain:** Warden + Graph Data Architect | **Priority:** 🟡 Medium | **Status:** ✅ Resolved (v2 GS8 / IC-DRYRUN-1)

Dry-run artifact storage for IC-MANIFEST-1 fully specced (v2 GS8). IC-DRYRUN-1 ratified: append-only, content-addressed, Ledger-anchored `dry_run_artifact_store`; 90-day minimum retention; access scoped to CAK-registered `dry_run_executor`. Appendix C entries: `DRY_RUN_ARTIFACT_STORED`, `DRY_RUN_ARTIFACT_PRUNED`, `DRY_RUN_SIGNATURE_INVALID`. IC-MANIFEST-1 check #7 updated to two-gate freshness: Gate A (corpus_sample_descriptor identity match, primary) + Gate B (90-day time ceiling, backstop). `DRY_RUN_STALE` deprecated; replaced by `DRY_RUN_CORPUS_DRIFTED` / `DRY_RUN_TIME_CEILING_EXCEEDED`. **Residual:** GAP-47 (pruning ceremony authority, Low).

---

### GAP-34
**Domain:** State Consistency + Warden | **Priority:** 🟡 Medium | **Status:** 🔴 Open
**Source:** GS3 v1 (R-S3-3), not confirmed applied in subsequent sessions

`governing_scope_hash` field on commit Ledger entries. PREPARED→COMMIT flow must preserve the scope hash that governed the PREPARED transaction, so post-scope-update forensic queries can determine which scope governed each commit at scope transition boundaries. Refinement R-S3-3 from GS3 v1 session recommended this; status in subsequent sessions is unconfirmed. If not yet applied, this is a Medium-priority Ledger entry schema extension.

---

### GAP-35
**Domain:** State Consistency | **Priority:** 🟢 Low | **Status:** 🔴 Open
**Source:** GS2 v1 (NEW-GAP-SC-1)

In-flight token fate at circuit-breaker trip moment. Tokens that have been consumed (`TOKEN_CONSUMED` written) but have not yet reached PREPARED are in undefined disposition when the circuit breaker trips. Three options not yet selected: (a) proceed to natural outcome, (b) force-abandon on trip (`TOKEN_ABANDONED` emitted), (c) proceed to PREPARED but cannot advance to COMMITTED.

---

### GAP-36
**Domain:** Warden | **Priority:** 🟢 Low | **Status:** 🔴 Open
**Source:** GS2 v1 (NEW-GAP-SC-3)

Rate limiting / escalation on repeated `CIRCUIT_RESET_REJECTED` attempts. Ledger-noise attack surface: no cap or escalation on repeated bad reset attempts (signature verification blocks forgery but flooding is possible). Low priority Warden policy item.

---

### GAP-37
**Domain:** Warden + State Consistency | **Priority:** 🟡 Medium | **Status:** 🔴 Open
**Source:** GS2 v1 (NEW-GAP-SC-4), partially addressed by A1-REVISED

Governance-write carve-out during CIRCUIT_TRIPPED. CIRCUIT_RESET is a W1 write occurring while "write token issuance is suspended." The exemption of governance-category ceremony writes (CIRCUIT_RESET, RETENTION_OVERRIDE_EXTENDED) from write suspension is implied but not explicitly stated in §11.8.1. A1-REVISED addressed the reversal-only bounding. The explicit carve-out language ("governance-category W1 writes proceed during CIRCUIT_TRIPPED; token-mediated writes do not") still needs to be confirmed in the spec text.

---

### GAP-38
**Domain:** Warden + Orchestration | **Priority:** 🟢 Low | **Status:** 🔴 Open
**Source:** GS3 v1 (G-S3-N3)

Cross-invocation `SCOPE_HASH_MISMATCH` aggregate detection. Current escalation (A4: 2 consecutive per invocation) is scoped to a single invocation, which an attacker can circumvent by spreading mismatches across invocations. A time-windowed aggregate metric is required: N SCOPE_HASH_MISMATCH events across all invocations within M seconds triggers Warden alert. Suggested starting values for discussion: N=10, M=60s.

---

### GAP-39
**Domain:** Validation Contract Architect | **Priority:** 🟡 Medium | **Status:** 🔴 Open
**Source:** GS4 v1 (G-S4-N3); reinforced by GS8 v3 (OQ-V9)

Constitutional test deterministic-clock dependency. D97 qualification criterion Q5 disallows "unstubbed wall-clock dependencies" (GS8 v3). But no clock injection mechanism is specified for the Validator sandbox — constitutional tests that assert timing behavior (e.g., C26 staleness transitions) need a testable clock abstraction. If no injection mechanism exists, Q5 cannot be validated deterministically, making any time-sensitive constitutional test unqualifiable.

---

## Formally Deferred to v2

| GAP | Domain | Deferred Item | Notes |
|-----|--------|---------------|-------|
| GAP-13 | Warden + Orchestration | Genesis automation — LLM reviewer proxy | GS10 produces v2 outline |
| GAP-17 | Orchestration + SCT | Voluntary lock release + inter-agent negotiation | GS10 v2 outline |
| GAP-18 | State Consistency | Multi-machine Ledger replication | GS10 v2 outline |
| GAP-19 | Warden | OOK + CAK key rotation | GS10 v2 outline; CAK rotation interactions with §13.5 step 3a are non-trivial |
| GAP-32 | SCT + Warden | Batch Genesis Hold release ceremony | See T16 |
| OQ-V7 | Validation | Registry identity expiry enforcement | Low; emerges with use cases |
| OQ-V8 | Validation | Cadence differentiation Meta-V vs Meta-TGA | Low; post-deployment empirical |

---

## Accepted as Deployment-Specific (No Session Required)

| GAP | Item |
|-----|------|
| GAP-16 | Notification channels for integrity violations |
| G-S4-N2 | Root authority quorum update path — recommended mint-once acceptance |

---


---

## Additional Gaps from v2 Schedule Sessions (GAP-40 through GAP-54)

*Surfaced in v2 GS4–GS11. Not captured in gap-backlog-v3.md or prior v4 reconciliation.*

### GAP-40
**Domain:** Orchestration Comparativist + Warden | **Priority:** 🟠 High | **Status:** 🔴 Open | **Source:** v2 GS4

First-boot CAK bootstrap tool specification. The `ceremony_authorization_key_anchor` in `genesis-seal.json` must be written mint-once by an operator-run bootstrap tool before harness first-boot (the harness cannot write its own ceremony key — circular trust). Tool must: run with operator credentials outside harness process identity; accept operator-generated public key material; write `genesis-seal.json` atomically with hash verification; emit a signed boot manifest the harness verifies at first boot. Trust model, distribution channel, and signing-authority chain are unspecified. **Blocks:** First-boot flow correctness.

### GAP-41
**Domain:** Warden | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS4

Per-CAK ceremony rate limiting. If a CAK is briefly exposed, an attacker could issue many ceremonies rapidly before detection. A per-CAK burst limit independent of per-ceremony-type limits is needed — distinct from GAP-27 (scope-update-specific) and GAP-38 (SCOPE_HASH_MISMATCH aggregate).

### GAP-42
**Domain:** Warden | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS4

Break-glass emergency channel full specification. When a CAK is declared compromised, all ceremonies are blocked with no v1 rotation path (T15). The channel is currently stubbed. Full spec required: second key? Out-of-band Ledger injection? Pre-signed envelope? Must avoid becoming a parallel compromise vector. **Related to:** GAP-19 v2 outline, T15.

### GAP-43
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟢 Low | **Status:** 🔴 Open | **Source:** v2 GS5

Recursive-fault reset semantics. If the circuit breaker tripped because of a `BOUNDED_COMPENSATION_VIOLATION`, the operator signing a reset re-enters a system whose last fault was the TC violating its own reversal-only constraint. Whether this requires a stricter reset ceremony or additional Warden sign-off is unspecified.

### GAP-44
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS6

`GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` classification review. Provisionally INTEGRITY (operational failure). But if the blocking attempt comes from a compromised agent, SECURITY classification or W3 eligibility may be warranted. **Warden co-review required.** Related to GAP-29 (W3 consolidation).

### GAP-45
**Domain:** State Consistency Theorist | **Priority:** 🟢 Low | **Status:** ⏳ v2 planning | **Source:** v2 GS7

Rate-limit state durability across Orchestrator restart. v1.1 rate-limit state is derived (Ledger replay at boot is sufficient). Becomes a gap if v2 adopts bucket-based enforcement requiring explicit durability semantics.

### GAP-46
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS7

`ceremony_initiator_id` attribution under key rotation. When CAK rotates, is `operator_id` (used in per-initiator rate limit) stable across rotation? If derived from key fingerprint, rotation resets the rate-limit window. Recommendation: operator_id is a stable external identity bound at first-boot and carried through rotation. **Requires spec confirmation.** Related to GAP-27, GAP-19.

### GAP-47
**Domain:** State Consistency Theorist + Warden | **Priority:** 🟢 Low | **Status:** 🔴 Open | **Source:** v2 GS8

Dry-run artifact store pruning ceremony authority. `DRY_RUN_ARTIFACT_PRUNED` (per IC-DRYRUN-1 / GAP-33) needs assignment as a CeremonyToken ceremony type (e.g., `RETENTION_PRUNING`). Not yet integrated into the GS4 CeremonyToken framework.

### GAP-48
**Domain:** MEMIT Specialist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS8

Probe set versioning for ε calibration. v2 GS8 D-GS8-A defines the `larql_fidelity_calibration` protocol referencing "the canonical probe set defined at Genesis." If the probe set changes across Genesis updates, historical ε values lose comparability. A probe-set versioning contract is needed. Related to GAP-1 (empirical calibration), T13.

### GAP-49
**Domain:** Validation Contract Architect + MEMIT Specialist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS10

Self-referential probing. When the judge model used by a `judge_model_classification` probe is itself subject to `.vindex` writes from the harness, probe outcomes may drift silently. No mechanism isolates judge-model state from the write stream it verifies. Related to GAP-9.

### GAP-50
**Domain:** Validation Contract Architect | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS10

TGA skill-profile divergence. v2 GS10 assigned probe template authorship to TGA (three sub-types: generation, assertion, constraint probes) in addition to existing executable test generation. Whether a single agent role covers both without quality degradation is unverified.

### GAP-51
**Domain:** State Consistency Theorist + MEMIT Specialist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS10

Provenance record lifecycle for Layer 4 re-verified facts. When a Layer 4 external-sourced fact is re-written after staleness detection, the relationship between original and successor provenance records (extend, replace, or chain) is specified narratively but not formally. Related to GAP-11, OQ-SC3.

### GAP-52
**Domain:** Warden + State Consistency Theorist | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS11

Archive key-lifecycle policy. When a bundle's signing key is retired (decadal horizon), restoration requires access to archived key material. Whether the Genesis Seal snapshot suffices across such horizons, or whether a separate key-archive ceremony is required, is unspecified. Related to GAP-19, GAP-12.

### GAP-53
**Domain:** State Consistency Theorist | **Priority:** 🟢 Low | **Status:** 🔴 Open | **Source:** v2 GS11

Ledger verification on very large chains. Full verification cost scales with chain length. On a multi-year, multi-million-entry Ledger the 24h/10K-entry full verification (D108) may become an operational bottleneck. Sampled verification with probabilistic coverage guarantee may be required.

### GAP-54
**Domain:** Warden | **Priority:** 🟡 Medium | **Status:** 🔴 Open | **Source:** v2 GS11

Pre-receive Git hook integrity. The Tier 3 config modification path depends on a pre-receive Git hook enforcing bounds and signatures on threshold updates (D110). The spec does not define how the hook itself is integrity-protected against local tampering. Related to GAP-29 (W3 consolidation).

---

## GS13 Scope (Previously GS10 — Updated)

Items requiring the final full council session:
- GAP-4: Three contingent path specs (Path A/B/C)
- GAP-9: Confirm partial resolution (v2 GS10 probe protocol); record implementation baseline
- GAP-13: v2 outline (Genesis automation proxy)
- GAP-15: Formal deferral confirmation (blocked by GAP-1)
- GAP-17: v2 outline (voluntary lock release)
- GAP-18: v2 outline (multi-machine Ledger replication)
- GAP-19: v2 outline (OOK + CAK key rotation dependency map)
- T15: v2 resolution path + Amendment A11
- OQ-SC3: Reconciliation workflow for stale Layer 4 facts
- GAP-48, GAP-49, GAP-50, GAP-51: MEMIT/Validation new gaps
- GAP-27 Tier conflict: resolve Tier 1 vs. Tier 3 placement for `scope_update_min_interval_seconds`

---

## Phase 2 Exit Criteria — Updated (Post v2 Reconciliation)

| Criterion | Status | Notes |
|-----------|--------|-------|
| All Critical + High priority gaps resolved | 🔶 Partial | GAP-4, GAP-29, GAP-40 open (High); GAP-3 partial |
| All Medium gaps resolved or deferred | 🔶 Partial | ~14 medium gaps open (GAP-30,31,34,37,39,41,42,44,46,48,49,50,51,54) |
| All Low gaps addressed | 🔶 Partial | GAP-35,36,38,43,45,47,52,53 open or v2-deferred |
| Council review with no new tensions | ❌ Not met | GS10–GS13 pending; T-S4-N1, T-S7-N1, T-TGA-load, T-BT open |
| gap-backlog-v4.md produced | ✅ This document (v2-reconciled) | |

---

## Summary Table — All 54 Gaps

| GAP | Domain | Priority | Status | Session |
|-----|--------|----------|--------|---------|
| GAP-1 | MEMIT | 🔴 Critical | ⏳ Deferred (impl.) | — |
| GAP-2 | MEMIT | 🔴 Critical | ⏳ Deferred (impl.) | — |
| GAP-3 | MEMIT + Graph | 🔴 Critical | 🔶 Partial | GS1 v1, GS7 v3 |
| GAP-4 | Orchestration | 🟠 High | 🔜 GS13 | contingent specs |
| GAP-5 | Warden + MEMIT | 🟠 High | ✅ Resolved | GS3 v3 |
| GAP-6 | SCT | 🟠 High | ✅ Resolved | GS2 v1, GS5 v3 |
| GAP-7 | SCT | 🟠 High | ✅ Resolved | GS2 v1 |
| GAP-8 | Validation | 🟠 High | ✅ Resolved | GS8 v3, GS9 v2 |
| GAP-9 | Validation + MEMIT | 🟡 Medium | 🔶 Partial (v2 GS10 protocol resolved) | GS13 confirm |
| GAP-10 | Validation | 🟡 Medium | ✅ Resolved | GS8 v3, GS9 v2 |
| GAP-11 | SCT + MEMIT | 🟡 Medium | ✅ Resolved (GS9 v3 authoritative) | GS9 v3 |
| GAP-12 | SCT | 🟡 Medium | ✅ Resolved | GS9 v3, GS11 v2 |
| GAP-13 | Warden + Orch. | 🟡 Medium | 🔜 GS13 v2 outline | — |
| GAP-14 | SCT + Orch. | 🟡 Medium | ✅ Resolved | GS9 v3, GS11 v2 |
| GAP-15 | Validation + MEMIT | 🟡 Medium | ⏳ Deferred | GS13 confirm |
| GAP-16 | Warden + Orch. | 🟢 Low | 🔒 Accepted | — |
| GAP-17 | Orch. + SCT | 🟢 Low | 🔜 GS13 v2 outline | — |
| GAP-18 | SCT | 🟢 Low | 🔜 GS13 v2 outline | — |
| GAP-19 | Warden | 🟢 Low | 🔜 GS13 v2 outline | — |
| GAP-20 | MEMIT + Graph | 🟠 High | ✅ Resolved | GS7 v3 |
| GAP-21 | SCT + Warden | 🟠 High | ✅ Resolved | GS5 v3 |
| GAP-22 | SCT | 🟠 High | ✅ Resolved | GS6 v3 |
| GAP-23 | SCT | 🟠 High | ✅ Resolved | GS6 v3 |
| GAP-24 | SCT + Warden | 🟡 Medium | ✅ Resolved | GS5 v3 |
| GAP-25 | SCT + Warden | 🟠 High | ✅ Resolved | GS5 v3 |
| GAP-26 | Warden + Orch. | 🟠 High | ✅ Resolved | GS4 v2/v3 |
| GAP-27 | Warden + SCT | 🟠 High | ✅ Resolved (Tier conflict needs GS13) | GS7 v3 + v2 |
| GAP-28 | Orch. | 🟡 Medium | ✅ Resolved | GS9 v3, GS11 v2 |
| GAP-29 | MEMIT + Warden | 🟠 High | 🔴 Open | GS10 |
| GAP-30 | SCT | 🟡 Medium | 🔴 Open | GS11 |
| GAP-31 | SCT + Warden | 🟡 Medium | 🔴 Open | GS11 |
| GAP-32 | SCT + Warden | 🟢 Low | ⏳ v2-deferred | GS13 outline |
| GAP-33 | Warden + Graph | 🟡 Medium | ✅ Resolved | v2 GS8 |
| GAP-34 | SCT + Warden | 🟡 Medium | 🔴 Open | GS11 |
| GAP-35 | SCT | 🟢 Low | 🔴 Open | GS11 |
| GAP-36 | Warden | 🟢 Low | 🔴 Open | GS10 |
| GAP-37 | Warden + SCT | 🟡 Medium | 🔴 Open | GS10 |
| GAP-38 | Warden + Orch. | 🟢 Low | 🔴 Open | GS12 |
| GAP-39 | Validation | 🟡 Medium | 🔶 Partial (OQ-V9 resolved D100) | GS12 |
| GAP-40 | Orch. + Warden | 🟠 High | 🔴 Open | GS10 |
| GAP-41 | Warden | 🟡 Medium | 🔴 Open | GS10 |
| GAP-42 | Warden | 🟡 Medium | 🔴 Open | GS10 |
| GAP-43 | SCT + Warden | 🟢 Low | 🔴 Open | GS11 |
| GAP-44 | Warden + SCT | 🟡 Medium | 🔴 Open | GS10/GS11 |
| GAP-45 | SCT | 🟢 Low | ⏳ v2 planning | — |
| GAP-46 | Warden + SCT | 🟡 Medium | 🔴 Open | GS11 |
| GAP-47 | SCT + Warden | 🟢 Low | 🔴 Open | GS10 |
| GAP-48 | MEMIT | 🟡 Medium | 🔴 Open | GS13 |
| GAP-49 | Validation + MEMIT | 🟡 Medium | 🔴 Open | GS13 |
| GAP-50 | Validation | 🟡 Medium | 🔴 Open | GS13 |
| GAP-51 | SCT + MEMIT | 🟡 Medium | 🔴 Open | GS13 |
| GAP-52 | Warden + SCT | 🟡 Medium | 🔴 Open | GS11 |
| GAP-53 | SCT | 🟢 Low | 🔴 Open | GS11 |
| GAP-54 | Warden | 🟡 Medium | 🔴 Open | GS10/GS11 |

---

*Gap Backlog v4.0 (amended post-v2 schedule reconciliation) — 54 gaps tracked*
*28 original + 11 from v1/v3 sessions + 15 from v2 sessions*
*Supersedes gap-backlog-v3.md*
*Sources: all v1 GS1–GS4, v2 GS4–GS11, v3 GS5–GS9 session summaries*
