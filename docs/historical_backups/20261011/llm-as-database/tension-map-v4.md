# LLM as Database: Agent Harness Architecture
## Tension Map v4.0

> **Supersedes:** `tension-map-v1.md` (and any v2/v3 tension map if produced)
> **Source sessions:** v1 GS1–GS4, v3 GS5–GS9, v2/v3 GS4
> **Scope:** All cross-domain tensions — those resolved in v1.1 synthesis (T1–T12),
>   those from gap-backlog-v2/v3 (T13–T15), and tensions surfaced in completed gap sessions
> **Next required:** GS10 (full council) to review and potentially add new tensions

---

## Status Labels

| Status | Meaning |
|--------|---------|
| ✅ **Resolved** | Both domains agreed; spec block produced |
| 🔶 **Partial** | One domain agreed or partial mitigation in place; v2 resolution required |
| 🔴 **Open** | Active tension requiring a gap session |
| 📋 **Acknowledged** | Surfaced and understood; accepted as design tradeoff |

---

## T1–T12 — Session 7 Integration Tensions

*(These tensions were resolved in the original seven-session spec arc and are carried forward for traceability. They are not repeated in full here — see `llm-as-database-v1_1-integrated-spec.md` §Appendix F for details.)*

| ID | Name | Status | Resolution |
|----|------|--------|------------|
| T1 | attention_weight two-number split | ✅ Resolved | D81: declared_importance + engine-computed attention_weight |
| T2 | TGA four-layer cascade | ✅ Resolved | D82: Stub probe + Dual-TGA + Meta-TGA |
| T3 | Meta-Validator per-case audit | ✅ Resolved | IC-SL8: per-case mandatory, aggregate forbidden |
| T4 | Three-tier .harness/ model | ✅ Resolved | Tier 1/2/3 model with distinct integrity mechanisms |
| T5 | Scope hash binding in tokens | ✅ Resolved | write_scope_hash + expected_yaml_hash in invocation token |
| T6 | Drift-from-anchor semantics | ✅ Resolved | Anchor-relative drift; drift_state object; D83 |
| T7 | Schema migration token timing | ✅ Resolved | Admission-time TTL; compile independent of subsequent token state |
| T8 | Lock/Hold split | ✅ Resolved | Write Lock (concurrent write prevention) + Dependency Hold (correctness across escalation) |
| T9 | Compaction epoch bundling | ✅ Resolved | Full MEMIT re-run; delta composition rejected; epoch archive |
| T10 | Two-queue review model | ✅ Resolved | Correctness Queue + Reconciliation Queue with distinct semantics |
| T11 | Unified State Ledger | ✅ Resolved | Single append-only JSONL ledger; audit_category tags |
| T12 | CONTENT_CLASSIFICATION_MIXED rejection | ✅ Resolved | D90: Gate triple-level classification authoritative; split_guidance payload |

---

## T13 — Advisory Boundedness vs. Operational Flexibility

**Specialists:** MEMIT Specialist vs. Orchestration Comparativist
**Status:** ✅ **Resolved** — GS7 v3

**Core conflict:** `LARQL_VERSION_LEGACY` accumulation must be bounded (MEMIT: unbounded accumulation degrades compaction fidelity via approximation error). Teams in active development cannot be hard-blocked mid-sprint (Orchestration: enforcement must be predictable with operator override).

**Resolution (GS7 v3):**
- MEMIT provided principled proxy: `Δfidelity ≈ r × h_avg × ε` (ratio of legacy patches × average hop distance × per-hop error coefficient).
- Three-tier model ratified: Tier 1 (LARQL_VERSION_LEGACY async advisory); Tier 2 (warning at r≥0.10 OR count≥25, 72h minimum before Tier 3); Tier 3 (hard-block at r≥0.25 OR count≥75 with 72h elapsed since Tier 2). Tier 3 thresholds **provisional pending GAP-1 empirical calibration of ε**.
- Override path: LEGACY_EXTENSION ceremony (CeremonyToken, CAK-signed, ceremony_type: LEGACY_EXTENSION); max 30-day single extension; max 2 extensions per rolling 90-day window.
- 72-hour notice window: fits between "overnight" and "sprint cycle."

**New Ledger types:** LARQL_VERSION_LEGACY_WARNING (SECURITY, sync), LARQL_VERSION_HARD_BLOCKED (SECURITY, sync), LEGACY_EXTENSION_GRANTED (GOVERNANCE, sync).

**Residual (provisional):** Hard-block threshold M remains provisional pending GAP-1. Per-version-gap weighting of ratio r deferred to GAP-1.

---

## T14 — Single-Key vs. Dual-Key for Ceremony Authorization

**Specialists:** Warden vs. Orchestration Comparativist
**Status:** ✅ **Resolved** — GS4 v2/v3 (D92)

**Core conflict:** Warden required separate ceremony authorization key (compromised Orchestrator must not self-authorize governance ceremonies). Orchestration noted operational overhead (out-of-band key management, physical security, availability).

**Resolution:** Dual-key hierarchy mandatory. OOK (Orchestrator Operational Key) for token-mediated writes; CAK (Ceremony Authorization Key) for all governance ceremonies. Security argument: OOK private key is on filesystem by design; single key would allow any agent with filesystem read to self-authorize scope expansions. Operational argument accepted: ceremony frequency (≤once/hour for scope updates; less frequent for others) makes hardware security token overhead acceptable.

**CAK storage (D94):** Hardware security token preferred; encrypted offline media acceptable; filesystem prohibited (C-CAK-1). `ceremony_authorization_key_anchor` field in Tier 1 `genesis-seal.json` (Amendment A10, applied GS5 v3). Boot-time verification step 3a added to §13.5 (GS5 v3).

---

## T15 — CAK Availability vs. Ceremony Urgency

**Specialists:** Warden vs. Orchestration Comparativist
**Status:** 🔶 **Partial** — v1 mitigation documented (gap-backlog-v3.md); v2 resolution pending GS10

**Core conflict:** D92 requires CAK to be human-held on hardware security token or encrypted offline media, physically separate from all networked systems. Unplanned ceremonies (circuit reset after incident) may require CAK access when the primary CAK custodian is unavailable or when CAK has been declared compromised (`CAK_COMPROMISE_DECLARED` written — all ceremonies blocked, no v1 rotation path).

**v1 mitigation (operational, not specced):** First-boot CAK registration ceremony must designate at minimum one backup custodian — a second person with physical access to the same CAK storage medium. v1 supports exactly one registered CAK anchor in `genesis-seal.json`; "backup custodian" is a second person with the same key, not a second registered key (Amendment A11, pending GS10).

**v2 resolution path:** OQ-S-CAK-1 (rotation ceremony design, accounting for mint-once Tier 1 `ceremony_authorization_key_anchor` and §13.5 step 3a interactions) + OQ-S-CAK-2 (m-of-n signing for multiple registered CAK principals).

---

## T16 — Ceremony-Scope Narrowness vs. Operational Batching

**Specialists:** Warden vs. State Consistency Theorist
**Status:** 🔴 **Open** — GS6 v3, related to GAP-32

**Core conflict:** When a failed Genesis held N edges, the operator must sign N separate DEPENDENCY_HOLD_RELEASED_SIGNED ceremonies (one per Hold). Warden's architectural preference: one-authorization-one-ceremony — narrow scope, individually auditable. SCT's operational concern: N scales with Genesis read-scope (potentially hundreds of edges), making per-Hold signing operationally burdensome.

**Proposed resolution direction (GS6 v3):** `ceremony_type: GENESIS_HOLD_RELEASE_BATCH` covering all `affected_hold_ids` in a single CAK signature — deferred to v2. Per-Hold path is specced and workable for v1. This is not a v1 Phase 2 blocker.

**v2 requirement:** Batch ceremony design must preserve Warden's audit requirement (each Hold release must be individually traceable in the audit trail) while permitting a single CAK signing event.

---

## T-SC-W-1 — Audit Category vs. Lifecycle Event for Hold Release

**Specialists:** State Consistency Theorist vs. Warden
**Status:** ✅ **Resolved** — GS5 v3

**Conflict:** Operator-signed Hold release is simultaneously a lifecycle state change (registry-level Hold state) and a governance ceremony (signed, audit-traceable operator action). Which audit_category tag governs?

**Resolution (GS5 v3):** `DEPENDENCY_HOLD_RELEASED_SIGNED` placed in GOVERNANCE category (synchronous). `HOLD_RELEASE_REJECTED` (equivalent failure) placed in SECURITY category. The existing LIFECYCLE `DEPENDENCY_HOLD_RELEASED` (automatic release) is distinct and retained for automatic-release events. Three entry types coexist in the Ledger — each covering a distinct release path.

---

## T-SC-W-2 — Write Suspension Scope vs. Governance-Ceremony Write Path

**Specialists:** State Consistency Theorist vs. Warden
**Status:** 🔶 **Partial** — A1-REVISED addresses bounding; explicit carve-out language pending (GAP-37)

**Conflict:** CIRCUIT_TRIPPED suspends "write token issuance." But CIRCUIT_RESET (the exit mechanism) is a W1 Ledger write occurring while in CIRCUIT_TRIPPED state. Without an explicit carve-out, the exit mechanism is definitionally blocked by the state it must exit.

**Partial resolution (GS5 v3 A1-REVISED):** TC compensation bounded to reversal-only. The implied invariant — governance-category W1 writes proceed during CIRCUIT_TRIPPED while token-mediated writes do not — is now operative in practice. However, the explicit statement in §11.8.1 ("governance-category W1 writes proceed during CIRCUIT_TRIPPED; token-mediated writes do not") has not been confirmed as added to the spec text.

**Remaining:** GAP-37 — confirm the explicit carve-out language is in §11.8.1.

---

## T-S3-N1 — Warden ↔ SCT: Ledger Ordering Underpins D87

**Specialists:** Warden vs. State Consistency Theorist
**Status:** ✅ **Resolved** — GS5 v3 (D103/IC-SCOPE-RECONCILE)

**Conflict:** D87's airtightness (SCOPE_UPDATED before registry update) depends on Ledger write ordering semantics that the Warden cannot specify unilaterally. A race exists if SCOPE_UPDATED and affected commit entries can interleave.

**Resolution (GS5 v3):** IC-SCOPE-RECONCILE specifies the Orchestrator startup reconciliation protocol for unprocessed SCOPE_UPDATED entries. 5-second propagation-lag ceiling (OQ-S-GAP24-1). DIVERGED_STATE triggered on reconciliation application failure. The ordering dependency is explicit: SCOPE_UPDATED write must complete before registry update; gap during crash is addressed by the reconciliation startup phase.

---

## T-S3-N2 — Warden ↔ Orchestration: Push-Based Invalidation Channel

**Specialists:** Warden vs. Orchestration Comparativist
**Status:** ✅ **Resolved** — GS9 v3 (D111/GAP-28)

**Conflict:** Whether the Orchestrator needs a push channel for scope invalidation. Warden's recommendation: reactive discovery (Gate rejection) is authoritative; proactive push is optional optimization.

**Resolution (GS9 v3):** D111 ratified. At-least-one-attempt-before-TTL boundary for proactive notification (60s default TTL, 10s Tier 1 floor). Agents MUST NOT rely on proactive notification for safety-critical operations — Gate rejection is authoritative. Push is confirmed as optimization, not requirement. `SCOPE_UPDATED` Ledger entry carries `affected_agent_ids` and `scope_change_type` (per GS4) for Orchestrator-side per-type notification policy.

---

## T-S4-1 — Warden / Validation: Audit Completeness Under Roster Indirection

**Specialists:** Warden vs. Validation Contract Architect
**Status:** 📋 **Acknowledged** — scope accepted, monitoring deferred

**Conflict:** IC-SL9 amendment (per-case `delegation_entry_id` in audit entries) extends Warden per-access verification scope to include the `corpus-author-registry/` append-only log. Does audit completeness now require the Warden to audit the roster's log on the same cadence as corpus manifest verification?

**Position (GS4 v1, reinforced by GS8 v3):** Yes — the roster log is an audit-relevant object. However, GS8 v3 resolved this structurally: `corpus-author-registry/` is a Tier 2 sealed artifact with standard Sealed Corpus pattern governance (Warden already governs via IC-SL7/IC-SL8). Roster log verification is naturally included in the existing sealed corpus verification cadence. No new verification mechanism required — absorbed into existing Warden scope.

---

## T-S4-2 — SCT / Validation: Roster State at Snapshot Boundaries

**Specialists:** State Consistency Theorist vs. Validation Contract Architect
**Status:** ✅ **Resolved** — GS4 v1 (design recommendation accepted, GS8 v3 reinforced)

**Conflict:** If a rollback to an earlier `CANONICAL_SNAPSHOT` occurs, does the `corpus-author-registry/` also roll back (reverting recent delegations/revocations)?

**Resolution:** Roster is snapshot-invariant (append-only log is not rolled back). Rationale: rolling back authorization records would undo legitimate revocations and reintroduce compromised identities, violating security monotonicity. The roster is an authorization log, not system state. This aligns with GS8 v3's treatment of `corpus-author-registry/` as a Tier 2 sealed artifact outside the Git/`.vindex` consistency boundary.

---

## T-S4-3 — Orchestration / Validation: Two-Signature Ceremony Latency for Promotion

**Specialists:** Orchestration Comparativist vs. Validation Contract Architect
**Status:** 🔴 **Open** — surfaced GS4 v1; not addressed in any subsequent session

**Conflict:** D98 (GS8 v3) requires a two-signature ceremony for every constitutional test promotion (nominator + distinct reviewer). As the constitutional suite grows, this creates a coordination bottleneck. Alternative — batch promotions where one reviewer signs N nominations simultaneously — reduces latency but weakens per-test independence of review.

**Current position (GS4 v1):** Orchestration asked whether the orchestration layer needs a ceremony-coordination primitive (nomination queue, review workflow) or whether ceremony coordination is out of orchestration scope. This question remains unanswered. GS8 v3 accepted single-operator signing (not two-signature) for v1.1 with multi-operator quorum deferred to v2.

**v2 relevance:** When multi-operator quorum is implemented (§19 roadmap), the coordination primitive question re-emerges. Flag for v2 orchestration spec.

---

## T-Candidate-GS7 — Dry-Run Freshness vs. Manifest Authorship Lifecycle

**Specialists:** MEMIT Specialist vs. Graph Data Architect (implied)
**Status:** 📋 **Acknowledged** — flagged in GS7 v3 for future review

**Conflict:** The 7-day freshness window on `dry_run_artifact_hash` (IC-MANIFEST-1 commit gate check 7) can conflict with longer manifest authorship cycles. If Architect Agent drafting + human review extends beyond 7 days, the dry-run must be re-run before ratification. This may be acceptable operational cost or may need tuning.

**Current position:** Accepted at 7 days (provisional) pending operational experience. If multi-week review cycles prove common, the freshness window should be tunable as a Tier 3 config value. No spec change required yet.

**GAP-33 dependency:** The dry-run artifact storage spec (GAP-33) must define storage retention that ensures dry-run artifacts remain accessible for at least the freshness window duration.

---

## T13-v1-GS1 (Local Tension, Session-Internal) — Manifest Signing Ownership

**Specialists:** MEMIT Specialist vs. AISecOps Specialist (GS1 v1 local framing)
**Status:** ✅ **Resolved** — GS7 v3 (structural resolution via IC-MANIFEST-1 + CeremonyToken model)

**Conflict (GS1 v1):** The `larql_migration_manifest` is a schema artifact (MEMIT + Graph Data Architect) that is simultaneously a trust-boundary artifact (Warden). Which domain is canonical owner of manifest content authorship vs. signing authority?

**Resolution (GS7 v3):** Clean split established — schema owner (Architect Agent via standard token/gate model) is the canonical **content author** (proposes manifest entries, may draft content); Warden (via CAK-signed MANIFEST_RATIFICATION CeremonyToken, D93) is the canonical **signing authority**. Commit gate verification (7 checks) closes the boundary.

---

## T14-v1-GS1 (Local Tension, Session-Internal) — Deprecation Timing vs. Compaction Cadence

**Specialists:** MEMIT Specialist vs. State Consistency Theorist (GS1 v1 local framing)
**Status:** ✅ **Resolved** — GS7 v3 (three-tier advisory model resolves)

**Conflict (GS1 v1):** Deprecation cutoffs depend on drainage of active patches at the deprecated version. Drainage is driven by compaction cycles (SCT-owned cadence). If the two domains select independent cadences — deprecation on calendar, compaction on drift thresholds — the drainage-before-cutoff invariant can be violated silently.

**Resolution (GS7 v3):** Tier 3 hard-block is ratio-based and compaction-cycle-aware (r = ratio of legacy patches to total active patches at compaction time). Tier 2 warning gives 72 hours minimum before hard-block. The ratio metric is computed at compaction evaluation time, not on a calendar, so the coupling between deprecation timing and compaction cadence is inherent in the metric design. SCT owns the compaction cadence; MEMIT consumes the ratio computed against that cadence.

---

## Tension Map — Summary Table

| ID | Name | Specialists | Status |
|----|------|-------------|--------|
| T1–T12 | Session 7 integration tensions | Various | ✅ All resolved (v1.1 spec) |
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | ✅ Resolved (GS7 v3) |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | ✅ Resolved (GS4 v2/v3) |
| T15 | CAK Availability vs. Ceremony Urgency | Warden + Orchestration | 🔶 Partial — v2 required |
| T16 | Ceremony-Scope Narrowness vs. Operational Batching | Warden + SCT | 🔴 Open (GS6 v3) |
| T-SC-W-1 | Audit Category vs. Lifecycle for Hold Release | SCT + Warden | ✅ Resolved (GS5 v3) |
| T-SC-W-2 | Write Suspension vs. Governance-Ceremony Write | SCT + Warden | 🔶 Partial — GAP-37 pending |
| T-S3-N1 | Ledger Ordering Underpins D87 | Warden + SCT | ✅ Resolved (GS5 v3) |
| T-S3-N2 | Push-Based Invalidation Channel | Warden + Orchestration | ✅ Resolved (GS9 v3) |
| T-S4-1 | Audit Completeness Under Roster Indirection | Warden + Validation | 📋 Absorbed into existing scope |
| T-S4-2 | Roster State at Snapshot Boundaries | SCT + Validation | ✅ Resolved (design accepted) |
| T-S4-3 | Two-Signature Ceremony Latency for Promotion | Orchestration + Validation | 🔴 Open — v2 relevance |
| T-Candidate-GS7 | Dry-Run Freshness vs. Authorship Lifecycle | MEMIT + Graph | 📋 Acknowledged; monitor |
| T13-v1-GS1 | Manifest Signing Ownership (session-local) | MEMIT + Warden | ✅ Resolved by GS7 v3 structure |
| T14-v1-GS1 | Deprecation Timing vs. Compaction Cadence (local) | MEMIT + SCT | ✅ Resolved by GS7 v3 model |

---

## Additional Tensions from v2 Schedule Sessions

---

### T-S4-N1 — Warden ↔ State Consistency Theorist: Rotation Registry Ordering
**Source:** v2 GS4 | **Status:** 🔴 Open (High priority)

When a `CEREMONY_KEY_ROTATION_COMPLETE` event rotates the CAK, the outgoing key governs ceremonies initiated before the event and the successor governs ceremonies initiated after. This requires the same Ledger barrier contract as T-S3-N1 (SCOPE_UPDATED ordering), generalized to all anchor-versioning ceremonies. The barrier problem is now a framework-level concern, not specific to scope updates.

**Resolution path:** Uniform Ledger-barrier contract covering all anchor-versioning ceremonies (SCOPE_UPDATED, CEREMONY_KEY_ROTATION_COMPLETE, and any future anchor-mutating ceremony). Add to §14.3 or equivalent: rate-limit and ceremony-ordering windows MUST be strictly shorter than the minimum retention window for the governing entry type. Boot-time validation: if configured window exceeds retention floor, suspend boot with `RATE_LIMIT_RETENTION_CONFLICT`. **Relates to:** T-S3-N1 (resolved), GAP-46, GAP-19.

---

### T-S4-N2 — Warden ↔ Orchestration: Bootstrap-Tool Trust Asymmetry
**Source:** v2 GS4 | **Status:** 📋 Acknowledged — resolution path defined, full spec deferred to GAP-40

The bootstrap tool (GAP-40) runs with operator identity outside the harness and writes the harness's root trust anchor. This inverts the normal trust direction. Orchestration: the tool must be distributable, versionable, auditable. Warden: the tool must not become a supply-chain attack vector — a compromised bootstrap tool can inscribe an attacker-controlled CAK, undetectable by subsequent mechanisms.

**Resolution path (documented, not yet specced):** Signed bootstrap-tool distribution + out-of-band tool integrity verification by operator before first-boot. Full spec deferred to GAP-40 resolution.

---

### T-S7-N1 — Warden ↔ State Consistency Theorist: Rate-Limit State as Derived vs. Primary
**Source:** v2 GS7 | **Status:** 🔴 Open (High priority)

Per-initiator rate-limit windows are derived from Ledger replay (elapsed time since most recent `SCOPE_UPDATED`). If that entry is compacted or archived between window checks, the rate-limit window resets — giving an operator a fresh budget after compaction even within the window. Warden: rate-limit state cannot depend on retention boundaries.

**Resolution path (v2 GS7 proposed):** Add requirement that `scope_update_min_interval_seconds` (per-initiator and per-agent) MUST be strictly less than the minimum retention window for `SCOPE_UPDATED` Ledger entries. Boot-time validation: if configured interval exceeds retention floor, suspend boot with `RATE_LIMIT_RETENTION_CONFLICT`. This is additive to §14.3 or §16.7. **Priority: High — operational correctness.**

---

### T-PM-vs-PA — Provenance Monitor ↔ Pruning Agent: Advisory Queue Priority
**Source:** v2 GS10 | **Status:** 🔶 Partial — v3 GS9 resolved GAP-11 with Pruning Agent extension (not separate Provenance Monitor); tension partially moot but not fully resolved

v2 GS10 introduced a separate Provenance Monitor component. v3 GS9 (authoritative, ran later) resolved GAP-11 using a Pruning Agent extension instead. Under the v3 GS9 resolution, a single edge can accumulate advisories from both the Pruning Agent's Git-side staleness detection and the Pruning Agent's external-source audit sub-routine, without a defined merge/priority order in the human review queue.

**Remaining question:** When a single edge has both a `REQUIRES_HUMAN_REVIEW` (Git-side) and `EXTERNAL_PROVENANCE_STALE` (external-source) advisory, does the review queue present them as a single consolidated item or two separate items? Ownership: State Consistency Theorist (queue semantics) + Warden (review-path integrity). **Candidate for GS11.**

---

### T-TGA-load — TGA Authority Concentration
**Source:** v2 GS10 | **Status:** 🔴 Open (Medium priority)

v2 GS10 assigned probe template authorship to TGA (three sub-types), on top of its existing executable test-generation mandate. The Actor-Critic independence guarantee (D32–D33) concentrates all verification-artifact generation in a single role: executable tests, probe templates, and the only agent permitted to read task specifications for verification purposes. This creates a single-point-of-failure concern: a compromised or failing TGA simultaneously degrades test quality, probe quality, and all downstream verification signal.

**Resolution path:** Not resolved in any session. Options: (a) accept as design constraint (actor-critic independence requires concentration); (b) split into TGA-Test and TGA-Probe as separate agent roles. **GS12 or GS13 triage.**

---

### T-BT — Bounded Tunability Latent Tension
**Source:** v2 GS11 | **Status:** 📋 Acknowledged — v2 design decision required

The "bounded tunability" pattern (Tier 1 immutable bounds + Tier 3 tunable values) is now applied to both retention (no-shortening path / extensions) and async thresholds (Tier 1 min floors / Tier 3 values). If an operator discovers that a Tier 1 bound was set too tightly at bootstrap, there is no recovery path within the current spec. A rare, high-ceremony "bound revision" path (distinct from normal tuning) may be required.

**v2 planning item.** Not a v1 Phase 2 blocker — the current spec prevents this scenario from being dangerous by making bounds conservative.

---

### T-NOTIFY-LOSS — Notification Loss Failure Mode
**Source:** v2 GS11 | **Status:** 📋 Acknowledged — accepted tradeoff

GAP-28's single-attempt-no-retry notification decision (D111) creates a narrow window where an agent's in-flight work is wasted because a notification was lost and the agent continued until Gate rejection. This is intentional (prevents notification-delivery ambiguity) but creates a failure mode where long-running tool calls from an affected agent cannot be preemptively aborted.

**Accepted as design tradeoff.** Gate rejection is the authoritative signal; notification is optimization only (C-NOTIFY3). No spec change warranted.

---

### T-v2GS6-CEREMONY-DECOMP — Ceremony Atomicity vs. Ceremony Decomposition
**Source:** v2 GS6 (local "T13") | **Status:** 📋 Acknowledged — framework-level design axis

GAP-23 resolved in favor of decomposed ceremonies (Hold release separate from circuit reset) for forensic clarity. A future refactor aimed at reducing operator burden (fewer ceremonies) could reintroduce pressure to make `CIRCUIT_RESET` implicitly release Holds — exactly the pattern GAP-23 rejected. The tension between auditability (many narrow ceremonies) and operator ergonomics (fewer consolidated ceremonies) is a framework-level axis that will recur in any future multi-ceremony recovery design.

**Not a v1 blocker.** Owners: State Consistency Theorist + Warden. Related to T16 (Ceremony-Scope Narrowness), GAP-32 (batch Hold release).

---

## Tension Map — Full Summary Table

| ID | Name | Specialists | Status |
|----|------|-------------|--------|
| T1–T12 | Session 7 integration tensions | Various | ✅ All resolved (v1.1 spec) |
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | ✅ Resolved (GS7 v3) |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | ✅ Resolved (GS4 v2/v3) |
| T15 | CAK Availability vs. Ceremony Urgency | Warden + Orchestration | 🔶 Partial — v2 required |
| T16 | Ceremony-Scope Narrowness vs. Operational Batching | Warden + SCT | 🔴 Open (GS6 v3) |
| T-SC-W-1 | Audit Category vs. Lifecycle for Hold Release | SCT + Warden | ✅ Resolved (GS5 v3) |
| T-SC-W-2 | Write Suspension vs. Governance-Ceremony Write | SCT + Warden | 🔶 Partial — GAP-37 |
| T-S3-N1 | Ledger Ordering Underpins D87 | Warden + SCT | ✅ Resolved (GS5 v3) |
| T-S3-N2 | Push-Based Invalidation Channel | Warden + Orchestration | ✅ Resolved (GS9 v3) |
| T-S4-1 | Audit Completeness Under Roster Indirection | Warden + Validation | 📋 Absorbed |
| T-S4-2 | Roster State at Snapshot Boundaries | SCT + Validation | ✅ Resolved |
| T-S4-3 | Two-Signature Ceremony Latency for Promotion | Orchestration + Validation | 🔴 Open — v2 |
| T-Candidate-GS7 | Dry-Run Freshness vs. Authorship Lifecycle | MEMIT + Graph | ✅ Resolved (D-GS8-D v2 GS8) |
| T13-v1-GS1 | Manifest Signing Ownership (local) | MEMIT + Warden | ✅ Resolved (GS7 v3) |
| T14-v1-GS1 | Deprecation Timing vs. Compaction Cadence (local) | MEMIT + SCT | ✅ Resolved (GS7 v3) |
| T-S4-N1 | Rotation Registry Ordering | Warden + SCT | 🔴 Open (High) — v2 GS4 |
| T-S4-N2 | Bootstrap-Tool Trust Asymmetry | Warden + Orchestration | 📋 Ack. — GAP-40 |
| T-S7-N1 | Rate-Limit State Derived vs. Primary | Warden + SCT | 🔴 Open (High) — v2 GS7 |
| T-PM-vs-PA | Provenance Monitor vs. Pruning Agent Advisory | SCT + Warden | 🔶 Partial — GS11 |
| T-TGA-load | TGA Authority Concentration | Validation | 🔴 Open (Med) — v2 GS10 |
| T-BT | Bounded Tunability Latent Tension | Various | 📋 Ack. — v2 planning |
| T-NOTIFY-LOSS | Notification Loss Failure Mode | SCT + Orchestration | 📋 Accepted tradeoff |
| T-v2GS6-CEREMONY-DECOMP | Ceremony Atomicity vs. Decomposition | SCT + Warden | 📋 Ack. — framework axis |

---

## Tensions Requiring Action Before Phase 2 Can Close

1. **T15 (CAK Availability)** — GS13 v2 outline + Amendment A11.
2. **T16 (Ceremony-Scope Narrowness)** — GS13 v2 outline for GAP-32.
3. **T-SC-W-2 (Write Suspension vs. Governance Write)** — GAP-37, GS10.
4. **T-S4-N1 (Rotation Registry Ordering)** — add explicit boot-time validation requirement; GS11 or integration pass.
5. **T-S7-N1 (Rate-Limit State Derived vs. Primary)** — add `RATE_LIMIT_RETENTION_CONFLICT` boot check; GS11.
6. **T-TGA-load (TGA Authority Concentration)** — triage in GS12 or GS13; v1 vs. v2 decision.
7. **T-S4-3 (Promotion Ceremony Latency)** — accepted for v1.1; flag for v2 orchestration spec.

---

*Tension Map v4.0 (amended post-v2 schedule reconciliation) — 23 tension IDs tracked*
*Supersedes tension-map-v1.md (and any subsequent maps)*
*Sources: v1 GS1–GS4, v2 GS4–GS11, v3 GS5–GS9, v2/v3 GS4, llm-as-database-v1_1-integrated-spec.md §Appendix F*
