# LLM as Database: Agent Harness Architecture
## v1.2 Integrated Specification

> **Version:** 1.2
> **Iteration:** v1.1 baseline + Phase 2 gap resolutions (GS1–GS13, including parallel v2/v3
> gap-session tracks) + fourteen ratified amendments (A1-REVISED, A2–A14).
> **Status:** Draft — pending operator ratification. All Critical/High gaps resolved or
> explicitly deferred with OQ anchors. Two tensions remain (T15 partial; T16 v2-scope).
> **Supersedes:** `llm-as-database-v1_1-integrated-spec.md`
> **Scope:** Single-machine reference implementation specification.
> **Basis:** v1.1 seven-session Council synthesis + thirteen Phase 2 gap sessions resolving
> 52 of 60 tracked gaps (`gap-backlog-v5.md`) and closing 23 of 25 tracked tensions
> (`tension-map-v5.md`). The v2 spec is self-contained; reading v1.1 is not required.
> **Reference Framework Document:** `llm-as-database-agent-harness-framework.md`
> (Chris Hay larql / V-Index paradigm + MEMIT literature).
> **Resolution record:** `gap-backlog-v5.md`, `tension-map-v5.md`, session summaries
> `gap-session-[N]-summary.md` for N ∈ {4–13}.
> **Note on version naming:** v1.2 closes all v1.1 outstanding amendments (A1–A14) in-place.
> No appendix-style amendment patches carry over. v2 scope — distributed trust, OOK/CAK
> rotation, multi-machine Ledger replication, voluntary Write Lock release, Genesis automation
> proxy, T15 m-of-n CAK availability, T16 batch Hold release — is outlined in §19.
> **Known D-number collision range:** D89–D103 were locally assigned across parallel
> v1/v2/v3 session tracks. Citation style is session-reference + content-description to
> disambiguate. See Appendix H for the collision register.

---

## Table of Contents

**Part I — Framework Overview**
1. Purpose and Paradigm
2. Architectural Summary
3. The Six Coordinated Layers

**Part II — Trust Boundary Scope**
4. Category 1: In-Scope Threats (Defended by Spec Mechanisms)
5. Category 2: Out-of-Scope Operational Assumptions
6. Category 3: Deferred to v2

**Part III — The Six Layers**
7. Schema Layer
8. Write Engine Layer
9. Validation Layer
10. Security Layer
11. State Consistency Layer
12. Orchestration Layer

**Part IV — Cross-Cutting Concerns**
13. Configuration Governance — The Three-Tier `.harness/` Model
14. Token and Authorization Lifecycle
15. Review Pathways — Two-Queue Model
16. The Unified Ledger
17. Concurrency Control — Lock vs. Hold

**Part V — Open Questions and v2 Roadmap**
18. Remaining Open Questions
19. v2 Scope Targets

**Part VI — Cross-Cutting Protocols (v1.2 additions)**
20. Ceremony Authorization — Unified CeremonyToken Model
21. L2 Probe Family and Semantic Assertion Criterion
22. `larql_fidelity_calibration` Protocol
23. CAK Bootstrap, Burst Limit, and Break-Glass
24. Corpus Author Registry Expiry Enforcement
25. Q5 Weak-Check / Constitutional-Failure Invariant
26. External Document Provenance for Layer 4 Facts
27. Ledger Retention Policy

**Part VII — Reference Appendices**
- A. Deployment Preconditions
- B. Interface Contract Index
- C. Ledger Entry Type Catalog
- D. Directory Layout
- E. Sealed Corpora Inventory
- F. Tension Map Summary (v2 State)
- G. Amendment Application Record (A1-REVISED, A2–A14)
- H. D-Number Collision Register (D89–D103)
- I. Inconsistency Flag List (INCON-N)

---

═══════════════════════════════════════════════════
# PART I — FRAMEWORK OVERVIEW
═══════════════════════════════════════════════════

## 1. Purpose and Paradigm

This specification defines a multi-agent development harness that treats a Large Language Model's Feed Forward Network (FFN) as a physically queryable and editable graph database. The system coordinates agent workflows across two parallel state mediums — a Git repository (deterministic syntactic state) and a versioned parametric overlay (the `.vindex` layer, representing semantic state physically encoded in model weights via the MEMIT algorithm).

The paradigm shift is from **in-context learning** (retrieval-augmented generation, transient context windows) to **in-weight learning** (permanent, zero-latency semantic memory physically wired into model pathways). Agent outputs that pass validation are not merely committed to a repository — they are compiled into the model itself, such that subsequent agents natively "know" the project's architectural state without requiring prompt reconstruction.

The harness is a specification framework, not an implementation. It defines:
- What components exist and what each must guarantee.
- How components interface with one another (the Interface Contract catalog in Appendix B).
- What threats the system defends against and what it assumes about its deployment environment (Part II).
- Which questions remain empirical or operational and are deliberately left open (Part V).

## 2. Architectural Summary

The harness is organized as six coordinated layers operating under a single Orchestrator-mediated control plane. A task flows through the system as follows:

```
  Human / External Input
         │
         ▼
  ┌──────────────────────────────────────────────────────────┐
  │                     ORCHESTRATOR                          │
  │   (task decomposition, agent invocation, lock/hold        │
  │    management, ledger writes, review queue routing)       │
  └──────────────────────────────────────────────────────────┘
         │                                         ▲
         │                                         │
         ▼                                         │
  ┌────────────────────┐    ┌──────────────────────────────┐
  │  TGA               │    │  Validator (+ Meta-Validator) │
  │  (test authorship) │────▶  (correctness cascade)        │
  └────────────────────┘    └──────────────────────────────┘
         │                                         │
         ▼                                         │
  ┌────────────────────┐                          │
  │  Coder Agent       │──────────────────────────┘
  │  (implementation + │         signed pass
  │   .larql drafting) │         ▼
  └────────────────────┘    ┌──────────────────────────────┐
                            │  Commit Executor              │
                            │  (sole two-medium writer)     │
                            └──────────────────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │  Patch Authorization Gate             │
                   │  (Identity → Scope → Integrity)       │
                   └───────────────────────────────────────┘
                                       │
                 ┌─────────────────────┴──────────────────┐
                 ▼                                         ▼
         ┌───────────────┐                      ┌─────────────────┐
         │  Git          │                      │  MEMIT Write    │
         │  (syntactic   │                      │  Engine         │
         │   state)      │                      │  (→ .vindex)    │
         └───────────────┘                      └─────────────────┘
                 │                                         │
                 └─────────────────┬───────────────────────┘
                                   │
                           ┌───────▼───────┐
                           │ State Ledger  │
                           │ (unified      │
                           │  integrity    │
                           │  + audit)     │
                           └───────────────┘
```

## 3. The Six Coordinated Layers

| Layer | Primary Concern | Key Components |
|---|---|---|
| Schema | What the graph can represent | Entity taxonomy, relation families, Genesis tiers |
| Write Engine | How facts enter model weights | MEMIT, `.vindex` overlays, `.larql` patches, drift tracking |
| Validation | Whether outputs are correct before commit | Reflexion loop, TGA cascade, Meta-Validator |
| Security | Who is authorized to write and how | Gate, tokens, Write Scope Definitions, audit trail |
| State Consistency | Whether both mediums agree | 2PC, Transaction Controller, Pruning Agent, Ledger |
| Orchestration | How all components are coordinated | Orchestrator, review queues, lock/hold registry |

**v1.2 cross-cutting additions (Part VI):** Eight protocols cut across multiple layers — Ceremony Authorization (§20), L2 Probe Family (§21), `larql_fidelity_calibration` (§22), CAK Bootstrap / Burst / Break-Glass (§23), Corpus Author Expiry (§24), Q5 Weak-Check (§25), External Document Provenance (§26), and Ledger Retention (§27). These are first-class spec content, not addenda. Layer sections cross-reference them where relevant.

---

═══════════════════════════════════════════════════
# PART II — TRUST BOUNDARY SCOPE
═══════════════════════════════════════════════════

## 4. Category 1: In-Scope Threats (Defended by Spec Mechanisms)

- Unauthorized writes to `.vindex` (Gate + token model).
- Agent overreach beyond declared Write Scope (Gate scope check).
- Prompt injection via external content (two-layer sequential defense, D38).
- Replay attacks on signed artifacts (single-use token model, Ledger consumption record).
- State divergence between Git and `.vindex` (2PC + Transaction Controller).
- Silent discard of agent failures (four-step escalation cascade, C28).
- Validator corruption or overreach (actor-critic independence, D32–D33).
- Tampered configuration artifacts (three-tier `.harness/` model, boot-time verification).
- Replay of stale `.larql` patches across schema version boundaries (C-GATE-1, IC-GATE-8).
- Unauthorized corpus authorship (C-GOC4, IC-CORPUS-AUTH; expiry enforcement §24).
- Retention policy shortening to destroy forensic evidence (C-SL2, IC-LDG-RETAIN; retention policy §27).
- Unauthorized ceremony replay or cross-ceremony token substitution (§20 unified CeremonyToken, IC-SCOPE-AUTH-1).
- Compromised operator root key at bootstrap (dual-root signing, C-BOOT-5, IC-BOOT-1, §23.1).
- CAK burst-signing attacks (per-CAK burst limit N=5/10min, `BURST_SUSPENDED`, IC-CAKB-1, §23.2).
- Primary-CAK compromise requiring rapid replacement (break-glass M≥3 quorum, `TRUST_ROOT_LOST` terminal state, IC-BG-1, §23.3).
- Low-signal scope-mismatch events aggregating into policy drift (aggregate `SCOPE_HASH_MISMATCH` detection, IC-AGG-COUNTER, §14.3).
- Stale or fabricated Layer 4 external documents (mandatory provenance block, advisory staleness, §26).
- Manifest-lattice incompleteness at ratification (IC-MANIFEST-1 Check 8).
- Pre-boot hook tampering (Tier 2 sealed `hook-registry/v1`, IC-HOOK-BOOT, `HOOK_INTEGRITY_VIOLATION`).
- Rate-limit / retention-window boot misconfiguration (`RATE_LIMIT_RETENTION_CONFLICT` boot check, IC-BOOT-RLRF).
- Genesis initiation during active Hold (`GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE`, `GENESIS_INITIATION_ABUSE_PATTERN`, IC-GIB-1).
- Genesis timeout/trip pairing failure (`GENESIS_TIMEOUT_TRIP_MISSING`, C-GTO-1/2, IC-MON-GTOTM).
- Hold-release without operator-cited precursor (`HOLD_RELEASE_REASON_UNWARRANTED`, IC-REL-PRECURSOR).
- Constitutional-invariant drift at runtime (Q5 weak-check, `CONSTITUTIONAL_FAILURE` with invariant_statement + failure_assertion_message, C-CONSTITUTIONAL-Q5, §25).

## 5. Category 2: Out-of-Scope Operational Assumptions

- Physical security of the host machine.
- Integrity of the base model file at installation (operator responsibility).
- Network security for external content ingestion (operator-controlled).
- Notification infrastructure for integrity violations (OQ-S8 — deployment-specific).
- Backup strategy for `<harness_root>/` (operator responsibility).
- Physical-access provision for break-glass CAK rotation (C-BG-4; operator pre-arranges custodians; see Appendix A).
- `.dry-run-store/` content-level immutability before executor signing (T-S-RP-1 accepted for v1; metadata-only Warden audit per IC-DRS-1; content-addressed storage v2-flagged).
- Worst-case legitimate Genesis event-count modeling against the N=5/10min burst limit (GAP-56 — empirical validation scoped to pre-ship).
- Operator workflow for break-glass custodian pre-arrangement (T-W-BG-1 accepted design tradeoff; deliberate friction is the security property).

## 6. Category 3: Deferred to v2

- Full PKI: mass revocation lists, Orchestrator key rotation, multi-Orchestrator trust.
- OOK and CAK key rotation ceremonies with full dependency map (GAP-19).
- Delegation tokens for nested sub-agent invocations (Path B/C nested cases).
- Pre-receive Git hooks (prevent-at-write for Tier 3 config).
- Multi-machine harness with Ledger replication and distributed consensus (GAP-18).
- Voluntary Write Lock release and inter-agent negotiation (GAP-17, OQ-CW1).
- Genesis automation proxy (secondary LLM reviewer as human-review substitute, GAP-13). Human review remains mandatory in v1.2.
- Genesis security model for fully automated pipelines (OQ-S5).
- Peer agent review delegation token design (GAP-20 — agent-to-agent trust model).
- `.larql` schema version migration path authorship and deprecation ceremony (OQ-W6 residual).
- T15 m-of-n CAK availability path (OQ-S-CAK-2; break-glass per §23.3 partially addresses OQ-S-CAK-1 for v1.2).
- T16 ceremony-scope narrowness: batch Genesis Hold release and multi-Hold ceremony scoping.
- Batch Genesis Hold release ceremony (T16 outline — per-Hold model remains v1.2 path).
- GAP-32 further scope-update rate-limit policy evolution.
- Sampled-verification for Ledger chains exceeding 10M entries (GAP-59 — design deferred per GAP-53 documentation threshold).
- Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60 — per GAP-52 open question).
- Empirical threshold calibration outputs: drift thresholds, MEMIT sub-batch ceiling, ε coefficient, M in T13 three-tier model (GAP-1, GAP-2; protocol structure in §22 is ratified, numeric outputs are implementation-phase).
- Stale Layer 4 fact reconciliation workflow (OQ-SC3 — implementation-time decision per v3 GS13 disposition).
- TGA split into TGA-Test / TGA-Probe (T-TGA-load v2-reconsider flag; activates only if v1.2 operation surfaces concrete failure-mode evidence).
- Path-conditional deployment architecture for GAP-4 Path A (LangGraph), Path B (SDK), Path C (Hybrid) — activates on operator selection of a path (GAP-56/57/58 preconditions).
- Aggregate-detection entry type convention (GAP-55 — formal framework convention for always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item; post-v1 integration pass).

---

═══════════════════════════════════════════════════
# PART III — THE SIX LAYERS
═══════════════════════════════════════════════════

## 7. Schema Layer

### 7.1 Schema/Code Partition

The schema defines what the graph can represent. The LLM stores **semantics** — relationships, dependencies, rules, knowledge. Git stores **syntax** — literal code, file contents, exact strings. This partition is a hard architectural boundary (D1). The LLM provides the map; Git provides the territory.

### 7.2 Entity Taxonomy

Five fixed base entity types (D3). Maximum five is a constitutional constraint (C1):
- `structural_entity` — files, modules, classes, functions.
- `domain_concept` — knowledge facts, named entities from the problem domain.
- `constraint_rule` — architectural rules, must-follow patterns.
- `process` — workflows, pipelines, execution sequences.
- `version_artifact` — *removed as an FFN base type* (closed via D17). Version metadata lives in the State Ledger, not the graph.

Domain extensions are declared as **subtypes** during Genesis Layer 2.

### 7.3 Relation Families

Five relation families (D6):
- **Structural** — `contains`, `defined_in`, `depends_on`, `imports`.
- **Knowledge** — `describes`, `associated_with`, `derived_from`.
- **Constraint** — `must_precede`, `must_not_contain`, `requires`.
- **Taxonomy** — `is_a`, `subtype_of`.
- **Namespace** — `scoped_to`, `belongs_to`.

The `contains`/`defined_in` pair is specified as **one canonical directed edge** (`defined_in`, child→parent). The write engine auto-generates the reverse; agents declare the canonical direction only (D16, closes OQ4).

### 7.4 Knowledge Namespaces

Two mandatory namespaces (D2):
- **Domain Knowledge** — portable across projects, `scoped_to = "domain"`.
- **Project Knowledge** — project-specific, `scoped_to = project_id`.

Different pruning rules and different write authorization levels apply per namespace.

### 7.5 Polysemantic Discipline

- All entity names must be compositionally unambiguous (C2).
- `target` is reserved in the triple model and prohibited as an entity name (C3).
- Untyped entities are schema violations (C4).
- Undeclared relation labels in `.larql` patches are schema violations (C5), rejected by the Validator before MEMIT.
- Semantic descriptions are metadata on entity nodes, never graph edges (D5).

### 7.6 Traversal and Ephemeral Relations

Bidirectional traversal is required (D4). Every edge supports reverse lookup; no write-only edges.

The `violates` relation is **ephemeral only** (D7) — never written to `.vindex`. The write engine hard-rejects any `.larql` patch containing `violates` (C6, C9).

### 7.7 Project Genesis (Four Layers)

Genesis organizes the initial knowledge compile into four layers (D9):
- **L1 — Schema Constitution** (framework-generated, write-once).
- **L2 — Domain Extension Declarations** (Architect Agent, write-once).
- **L3 — Project Constitutional Constraints** (Architect Agent, elevated review required).
- **L4 — Foundational Domain Knowledge** (Architect Agent, updatable via standard pipeline).

Genesis L1–L2 require schema migration to modify (C7). The scope test: *"Is the harness broken without this fact?"* If no, it does not belong in Genesis (D10).

### 7.8 Deletion Authority

Pruning Agent may delete Structural and Knowledge family edges only (D8, D54). Constraint and Taxonomy relations require privileged orchestrator-level deletion.

## 8. Write Engine Layer

### 8.1 Purpose

The write engine compiles `.larql` patches into physical modifications of FFN pathways via the MEMIT algorithm. All writes are overlay-based; the base model is permanently frozen (D11, C8).

### 8.2 MEMIT as the Designated Engine

MEMIT is the designated write engine (D12). ROME, GRACE, and full fine-tuning are explicitly excluded. MEMIT targets middle-to-late FFN layers (L15–L25 for a 32-layer model; C15). Early syntax layers are off-limits for semantic injection.

Two mandatory safeguards (D20):
- **Orthogonal projection** — new fact vectors are computed orthogonally to existing feature vectors, preventing polysemantic cluster corruption.
- **Covariance balancer** — scales injection strength relative to existing neighborhood covariance.

### 8.3 Two Operating Modes (D13)

- **Genesis Mode** — batch compile, mints the initial `.vindex` tier stack.
- **Incremental Mode** — smaller patches buffered via an L1 Cache before MEMIT compile.

### 8.4 The `.vindex` Tier Stack (D14)

```
.vindex/
  genesis_schema.vindex        ← L1 Genesis (frozen post-mint)
  genesis_domain.vindex        ← L2 Genesis (frozen post-mint)
  genesis_constraints.vindex   ← L3 Genesis (elevated-review changes only)
  genesis_knowledge.vindex     ← L4 Genesis (updatable via standard pipeline)
  incremental_NNNN.vindex      ← per-commit overlays
```

Tiered for independent rollback.

### 8.5 The `.larql` Canonical Format (D15, extended by T1, IC-SC1, D81, D90)

Four required sections, bracketed by `BEGIN TRANSACTION` / `COMMIT`:

1. **Entity Registration** — new entity nodes with base type tags.
2. **Edge Declarations** — edges with `declared_importance` enum (see 8.6).
3. **Deletions** — explicit `DELETE FROM EDGES` / `DELETE FROM ENTITIES` operations.
4. **Compiler Directives** — `TIER`, `CONTENT_CLASSIFICATION`, `ORTHOGONAL_PROJECTION`, `SET TARGET_LAYERS`.

Mandatory directives:
- `TIER` in every patch (C11).
- `CONTENT_CLASSIFICATION ∈ {structural, layer4_domain}` in every patch (C-SC3). Value `mixed` rejected pre-commit (C-SC4). When a patch contains triples spanning multiple classification tiers (detectable at Gate via triple-level `edge_category` check against the Tier 1 config `classification_tier_mapping`), Gate returns `CONTENT_CLASSIFICATION_MIXED` with a structured `split_guidance` payload specifying which triple IDs belong to each classification tier (D90, IC-GATE-9). The Coder Agent resubmits as N separate single-classification patches. Gate classification is authoritative; the Coder's declared patch-level directive is informational only.

Every patch MUST carry a `larql_syntax_version` header field declaring the `.larql` syntax version under which it was authored (D81, C-GATE-1). Current version: `"1.1"` (incorporating the T1 two-number importance model). The Gate's version pre-check (§10.2 pre-check #8) enforces this field. Compaction re-run parsing of superseded patches across version boundaries requires the versioned patch parser and `larql_migration_manifest` declared in Tier 1 config (D82).

### 8.6 Importance and Attention Weight — Two-Number Model (T1)

The agent-authored `attention_weight` field from the original `.larql` format is **split into two separate concepts**:

- **`declared_importance`** — agent-authored enum with three values: `CORE`, `SUPPORTING`, `INCIDENTAL`. Reference mapping: 0.9 / 0.7 / 0.4. Used pre-commit by the Validator to gate verification intensity.
- **`attention_weight`** — engine-computed during MEMIT compile, based on covariance balancer math. Not authored by the agent. Emitted into the State Ledger entry for audit and post-compile analysis.

A **divergence check** runs post-compile: if `declared_importance = CORE` yields engine-computed `attention_weight < 0.5`, or `declared_importance = INCIDENTAL` yields `> 0.9`, the Validator flags the write as a soft signal for review. Not a hard rejection.

### 8.7 Drift-from-Anchor Thresholds (T6)

Drift is measured relative to the most recent **anchor event**, not as total cumulative edges. Anchor events:
- Successful Genesis compile.
- Successful overlay compaction.

After an anchor event, drift resets to zero.

- **Drift warning:** 1,500 edges since last anchor → schedule compaction at next idle window.
- **Drift hard trigger:** 8,000 edges since last anchor → writes suspended until compaction completes.

Deletions count toward drift the same as additions (absolute edge changes).

All thresholds are provisional pending empirical validation against target model (OQ-W1 remains open).

The Write Engine exposes a queryable `drift_state` object to the Transaction Controller, updated after each `COMMITTED` Ledger entry and reset to baseline after each `ANCHOR_ESTABLISHED` event (D83, IC-WE-1). Fields: `edge_count_since_anchor`, `drift_tier` (enum `NOMINAL | WARNING | HARD | CRITICAL`), `anchor_event_id`, `overlay_file_count`, and `p95_latency_ratio`. The TC reads `drift_state` before issuing any new write token; tier-to-action mapping is specified in IC-WE-1. Tier boundary values are sourced from Tier 1 config; all values remain provisional (OQ-W1).

The drift counter MUST reconcile with the Ledger-computed edge count within 5% tolerance. Divergence exceeding this threshold triggers `INTEGRITY_VIOLATION` and write suspension (C-WE-1).

### 8.8 Architect Capacity Model (T6)

Two-ceiling model:
- **Hard security cap (per-patch):** Architect 10,000 edges, Coder 500 edges (100 when external content flagged), Pruning unbounded-in-principle but family-scope restricted.
- **MEMIT recommended batch size:** 2,000 edges. Patches exceeding this are sub-batched internally by the write engine. Sub-batching is transparent to the ledger — a 10K Architect patch remains one atomic 2PC event (preserves C-TPC2).

All Coder caps are per-patch (not per-session or per-task).

### 8.9 Post-Write Verification (D18)

Two-level mandatory probe:
- **L1 — Storage probe** (mandatory for all writes): `SELECT` read-back confirms the edge was written.
- **L2 — Behavioral probe** (mandatory for `declared_importance ∈ {CORE, SUPPORTING}`): generation test confirms the fact fires correctly in inference.

**Storage-pass / behavior-fail** is a named failure mode (D19, D30). Recorded as `write_outcome = "behavior_fail"` in the Ledger — explicitly not collapsed into success.

Compaction verification uses a distinct probe class (`probe_type: "COMPACTION_REGRESSION"`) that tests whether *previously encoded facts survived a recompile*, not whether a new fact was accepted. This probe is defined in IC-OC-PROBE and produces a `CompactionProbeReport` rather than the per-edge storage/behavioral probe signals of L1/L2.

**L2 probe family (§21):** L2 behavioral probes are authored from a three-member domain-agnostic probe family — Generation probe, Assertion probe, Constraint probe — subject to the Semantic Assertion Criterion with three judgment methods. Full protocol in §21. TGA is the authorship authority (v2 GS10 — GAP-9 resolution).

**Post-write fidelity calibration (§22):** The ε coefficient used in behavioral-probe pass thresholds is itself a measured quantity, produced by the `larql_fidelity_calibration` protocol per-transform-class. Protocol structure is ratified in §22; numeric ε outputs are implementation-phase per OQ-W1 (v2 GS8 — D-GS8-A; GAP-48 probe-set versioning open).

### 8.10 Anchor-Superseded Archive (T9)

`.larql` patches exist in three states:
- **Active** — feeds into the most recent anchor or subsequent incremental overlays. Retained in `.larql-archive/active/`.
- **Superseded** — earlier than the most recent anchor. Content embedded in that anchor's compacted overlay. Moved to `.larql-archive/superseded/{epoch_bundle_N}/` as compressed, manifest-sealed bundles.
- **Retained-for-audit** — ledger record (hash, metadata, classification, timestamp, issuing agent, outcome) is permanent regardless of archive state.

**Classification-differentiated retention:**
- Structural-classified superseded patches: **90-day default** retention.
- Layer4_domain-classified superseded patches: **project-lifetime** retention in cold storage.

Compaction is a full MEMIT re-run on archived patches (D62, closes OQ-W10). Delta composition is rejected — it would skip the mandatory mathematical safeguards. Time-based compaction scheduling: every 30 days since the last anchor, triggered during idle windows.

Compaction re-run MUST parse all active `.larql` patches through the versioned patch parser. Patches carrying a `larql_syntax_version` below the current version are translated via the `larql_migration_manifest` before passing to MEMIT compile. Translation failure aborts compaction (D82). The migration manifest is a Tier 1 config artifact; it is updated at the same time as `current_larql_version` whenever a `.larql` syntax version advance occurs.

## 9. Validation Layer

### 9.1 Purpose

Every output that reaches the Commit Executor must be proven correct, not semantically vouched for. The Validation Layer ensures that code, tests, and `.larql` patches are *behaviorally verified* before any parametric state change occurs.

### 9.2 Actor-Critic Independence

Two hard independence rules:
- **The Coder Agent does not author its own tests** (D32, C23). The Test-Generation Agent (TGA) is a separate actor.
- **TGA reads the task specification only, never the Coder Agent's code before writing tests** (D33, C24). Independence is enforced by sequencing, not policy alone.

These rules extend to human reviewers: a reviewer who `modify_patch`es a catch-up or escalated patch cannot bypass the Validator — the modified patch re-enters the standard cascade (T10 IC-OR14).

### 9.3 Validator Four-Level Cost-Stratified Cascade (D34)

Per `.larql` patch verification:
- **L1 — Static analysis** — all patches, mandatory (syntax, schema conformance, vocabulary check, `larql_syntax_version` conformance per IC-GATE-8).
- **L2 — Inference probe** — edges with `declared_importance ∈ {CORE, SUPPORTING}`, mandatory (behavioral probe).
- **L3 — Cross-agent review** — conditional: `declared_importance = CORE` or Genesis-adjacent tier.
- **L4 — Human spot-check** — periodic audit, not a per-patch gate.

### 9.4 TGA Four-Layer Validation Cascade (T2)

The TGA itself is gated to prevent silent corruption of the correctness floor:

- **L1 — Structural check** (all outputs, mandatory). Static analysis: ≥2 assertions per test, no bare `pass` or `assert True` bodies, every assertion references spec-declared symbols, test count scales with spec complexity.
- **L2 — Stub probe** (all outputs, mandatory). TGA tests run against an empty stub implementation. Any substantive test that passes against stub is a false-positive gate; TGA is re-invoked.
- **L3 — Dual-TGA** (`declared_importance = CORE` tasks only). Two independent TGA invocations on the same spec; only behaviors asserted by both count as active gates.
- **L4 — Meta-TGA** (periodic, every 50 commits or weekly). Held-out `(spec, gold_test_set)` corpus per the Sealed Corpus pattern. TGA Health Score thresholds mirror Meta-Validator's: ≥95% no action, 85–94% warning and 48-hour review, <85% immediate suspension. Corpus authorship requirements and minimum viable corpus size (20 cases) are defined in IC-CORPUS-AUTH and §13.3 (D88). Health Score is `NOT_COMPUTED` when corpus is below 20 cases.

L1 + L2 failures do not consume Coder Agent retry budget — they are upstream infrastructure failures (consistent with D67).

### 9.5 Failure Classification and Retry Limits (D36)

Tiered retry limits:
- **Tier 1 — Syntactic / formatting:** max 2 retries.
- **Tier 2 — Logic / test failure:** max 3 retries.
- **Tier 3 — Architectural / schema violation:** max 1 retry, then immediate escalation.

**Hard cap: 5 retry events per task across all tiers** (C27). 2PC infrastructure failures do not consume this budget (D67).

Constitutional test suite failures are treated as Tier 3 regardless of the error's surface appearance (C25).

### 9.6 Failure Escalation Cascade (D37)

Four-step, in order:
1. **Task decomposition** — Orchestrator splits task into narrower subtasks, each with fresh retry budget (OQ-V2 resolved D73). Aggregate 5-event cap preserved across subtasks.
2. **Peer agent review** — second independent Coder receives full retry history and attempts task fresh. Tokenization of the peer review agent uses the standard Orchestrator ceremony; agent-to-agent trust model is deferred to v2 (GAP-20).
3. **Human escalation queue** — full package routed to the Correctness Review Queue with task spec, retry history, decomposition log, failure tier, consistency status.
4. **Logged suspension** — task suspended, named gap record written to the Ledger, `.vindex` not patched. Silent discard is prohibited at every step (C28).

### 9.7 `code_pass_patch_fail` — Hard Rejection (D35, C26)

The Validator may reject a `.larql` patch independently of code. `code_pass_patch_fail` is a named failure mode: neither output is committed when the patch fails, even if code is correct. Both must pass or neither is committed. This preserves the atomic transaction unit (C-TPC1).

### 9.8 Prompt Injection Defense — Two-Layer Sequential (D38)

- **Authorization Gate** owns *structural* inspection: field lengths, control characters, escape sequences, pattern-based. No NL parsing.
- **Validator** owns *semantic* content inspection: instruction-like language in free-text fields, override-pattern entity names.

Injection suspect events are never offered a retry (C29). Always hard rejection plus human review flag, regardless of injection confidence level.

### 9.9 Validator Has No Write Authority (D39)

Validator outputs are signed signals only, classified as orchestration communications. They pass through the Orchestrator's verification layer before the Commit Executor is spawned (IC21, IC22).

### 9.10 The Commit Executor Pattern (D40, C30)

Single-file, deterministic, non-reasoning agent. **Sole component with simultaneous write access to both Git and the MEMIT write engine.** No reasoning agent holds this access. The Commit Executor is the exclusive chokepoint for dual-medium writes (C-OR2, C-OR6).

### 9.11 Meta-Validator (D41)

Runs every 50 commits or weekly, whichever first. Evaluated against a held-out human-authored suite per the Sealed Corpus pattern. Corpus authorship requirements and minimum viable corpus size (20 cases) are defined in IC-CORPUS-AUTH and §13.3 (D88). Health Score is `NOT_COMPUTED` when corpus is below 20 cases. Validator Health Score thresholds:
- **≥ 95%:** no action.
- **85–94%:** warning flag, human review within 48 hours.
- **< 85%:** Validator suspended, immediate human review, recent passes audited.

## 10. Security Layer

### 10.1 Purpose

Every write is authorized, verified, auditable, and bounded by the least privilege necessary. The Security Layer establishes and enforces the trust boundaries across which agents, humans, and system components communicate.

### 10.2 The Patch Authorization Gate (D22, C16, extended D81, D90)

Mandatory and exclusive. No `.larql` patch reaches the write engine without passing all checks in sequence:

**Pre-checks (T5, T7, D81):**
1. Token signature valid (verified against Orchestrator public key from dual-store anchor).
2. Token not expired (invocation tokens: 10-minute TTL; schema migration tokens: 10-minute admission-time TTL).
3. Token not previously consumed (Ledger lookup).
4. `write_scope_hash` matches current Write Scope Definition version.
5. `expected_yaml_hash` matches current Agent YAML version. Content classification pre-check: if the patch contains triples spanning multiple classification tiers, Gate returns `CONTENT_CLASSIFICATION_MIXED` with `split_guidance` payload (D90, IC-GATE-9).
6. Scope lock reference (if present) is still valid.
7. Agent not in `suspended_agents` set.
8. `larql_syntax_version` present and within supported range (D81, C-GATE-1). Absent or below `min_supported_larql_version` → `VERSION_REJECTED` (hard rejection, no retry budget consumed). Above `current_larql_version` → `VERSION_UNSUPPORTED` (hard rejection, operator alert set). Between minimum and current → `LARQL_VERSION_LEGACY` advisory entry written (async), patch proceeds (D82).

**Core checks (D22–D23):**
9. **Identity** — agent token signature verification.
10. **Scope** — entity base type + relation family + tier target within agent's declared Write Scope Definition.
11. **Integrity** — patch hash matches agent-declared hash.

Failure at any check is hard rejection; partial write is prohibited. Direct filesystem writes to `.vindex` bypass the gate and are treated as security violations (C16).

### 10.3 Scoped Agent Roles (D25, extended by T2)

Four write-authorized agent roles:

| Agent | Types | Tiers | Edge Cap | External Content |
|---|---|---|---|---|
| Architect | All types/families | All Genesis tiers (with schema migration token) | 10,000/patch | HIGH RISK flag |
| Coder | `structural_entity` only | Structural + Knowledge families, incremental tier only | 500/patch (→100 with external content) | Capped |
| Pruning | `structural_entity` + `domain_concept` | Structural + Knowledge only, DELETE authorized | No numeric cap | None processed |
| TGA | None on `.vindex` (gatekeeper-data-producer) | n/a | n/a | Task spec only, no external |

TGA writes tests as part of the atomic task-completion package but never authors `.larql` patches. Architect is the only agent authorized to target Genesis tiers; all other agents are hard-rejected at the Scope check for any L1–L3 tier target (C19).

### 10.4 Invocation-Scoped Single-Use Tokens (T5)

Structure (nine fields):
- `token_id` — unique identifier for Ledger matching.
- `agent_id` — matches Write Scope Definition.
- `invocation_id` — specific invocation scope.
- `task_id` — for lineage tracking (IC-OR9).
- `scope_lock_ref` — lock ID if applicable.
- `write_scope_hash` — Write Scope Definition version at issuance.
- `expected_yaml_hash` — Agent YAML version at issuance.
- `issued_at`, `expires_at` — 10-minute TTL.
- `signature` — Orchestrator-signed.

**Token is not a standalone credential.** It is a *witness* to the state of the entire governance layer at the moment of issuance. An attacker stealing a token must also keep every anchored document unchanged within the TTL window.

### 10.5 Orchestrator Signing Key (T5)

Generated at first boot. Private half stored at `<harness_root>/.orchestrator-key/` with strict filesystem permissions. Public half dual-stored: primary in State Ledger as `ORCHESTRATOR_KEY_ANCHOR` (immutable), secondary at `<repo_root>/.harness/orchestrator-key-anchor.json` (Git-committed). Boot-time hash comparison required; mismatch suspends boot.

Key rotation is v2 (Category 3).

### 10.6 Genesis Security Protocol (D26)

Three-step:
1. **Human review** of Architect Agent output patch before write engine execution (mandatory in v1; OQ-S5 fully-automated variant is v2).
2. **Schema migration authorization token** — one-time-use, cryptographically bound to patch hash, 10-minute admission-time TTL (T7, revised from D27's original 30 minutes). Validated at Phase 1 admission; compile proceeds independent of token state thereafter.
3. **Post-Genesis snapshot integrity seal** — `genesis.vindex` hash stored as `IMMUTABLE_ANCHOR` Ledger entry. Project-lifetime rollback anchor.

### 10.7 Agent Suspension — Token Revocation Mechanism (T5, closes OQ-S2)

Bulk revocation via in-memory `suspended_agents` set on the Orchestrator. Suspension triggers:
- Three consecutive scope failures from same agent in one session (D31).
- Meta-Validator or Meta-TGA Health Score below 85%.
- Warden-initiated manual suspension for integrity events (C22).

Suspended agents cannot be issued new tokens; existing tokens rejected at Gate with `TOKEN_AGENT_SUSPENDED`. Clearing suspension requires explicit human action with Ledger entry.

Full PKI (mass revocation lists, delegation chains, multi-Orchestrator trust) is v2.

### 10.8 Write Scope Definitions as Tier 2 Sealed Artifacts (D24, T4)

Stored at `<harness_root>/.sealed-corpora/write-scope-definitions/` per the Sealed Corpus pattern. Updates via versioned additive directories with human-signed manifest. Not modifiable by any agent at runtime (C17).

### 10.9 Agent YAML ↔ Write Scope Definition Binding (T4, extended D87)

**Write Scope Definition is the source of truth.** Agent YAML is the operational document, structurally subordinate. Binding enforced at invocation time:

- Orchestrator computes YAML hash, compares against `expected_yaml_hash` field in Write Scope Definition.
- Mismatch → Orchestrator refuses invocation, `YAML_BINDING_FAIL` Ledger entry.

Update ceremony scales with blast radius:
- Trivial operational tweaks (temperature, non-prompt parameters): Git commit + `CONFIG_UPDATE` Ledger entry only.
- Changes affecting prompt content or allowed tools: Git commit + Write Scope Definition update (signed ceremony) + `expected_yaml_hash` update.

**Scope Update Ceremony (D87, extended by §20 Ceremony Authorization)**

Write Scope Definition updates are accepted mid-flight — no drain of in-flight invocations is required. An update MUST produce a `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous) before the Orchestrator's in-memory scope registry is updated. The entry carries `previous_scope_hash`, `new_scope_hash`, `ceremony_token_id` (A9 — replaces the v1.1 `ratification_signature` / `operator_signature` field), and `affected_agent_ids`.

**Ceremony authorization (A5, A6 — applied):** SCOPE_UPDATE ceremonies are now authorized via the unified CeremonyToken model (§20, IC-SCOPE-AUTH-1). The Orchestrator enforces the following admission order for every SCOPE_UPDATE submission (order is normative):

1. **Rate-limit check** against `scope_update_min_interval_seconds` (per-initiator primary; per-affected-agent-id secondary) — per Tier 3 `rate-limits.json` (GAP-27 resolution). If the rate limit is breached, the ceremony is rejected with `SCOPE_UPDATE_RATE_LIMITED` **before** any signature verification is performed (A6). This ordering eliminates a signature-oracle attack surface.
2. **CeremonyToken envelope verification** — structural validity, ceremony_type discriminator must equal `SCOPE_UPDATE`, non-replay check against Ledger.
3. **Ceremony authorization verification against CAK** — signature over the ceremony envelope is verified against the current `ceremony_authorization_key_anchor` (§13.2, A10). Verification failure is logged as `CEREMONY_AUTH_INVALID` and the ceremony is rejected. CAK verification precedes SCOPE_UPDATED Ledger write (A5); no SCOPE_UPDATED entry is produced by a failed authorization.
4. **Precondition checks** — manifest-lattice completeness, affected-agent-id validity, scope hash predecessor consistency.
5. **SCOPE_UPDATED write** — Ledger entry synchronous; in-memory registry update follows.

Any in-flight token whose `write_scope_hash` predates the update will fail at Gate pre-check step 4 with error code `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure). The error payload includes `current_scope_hash` and `scope_updated_at`, enabling the Orchestrator to issue a corrected token without consuming the agent's retry budget. Active PREPARED transactions are not interrupted; scope changes are forward-only.

### 10.9.1 Scope Registry Reconciliation on Orchestrator Restart (GAP-25 / v3 GS5)

On Orchestrator restart, the in-memory scope registry MUST be reconciled against the Ledger's `SCOPE_UPDATED` entry chain before any token issuance resumes. The reconciliation procedure (IC-SCOPE-RECONCILE):

1. Read Ledger from boot back to the most recent `SCOPE_ANCHOR` entry (or genesis if none).
2. Replay all `SCOPE_UPDATED` entries in causal order, reconstructing the affected-agent → scope-hash map.
3. Verify the reconstructed head `new_scope_hash` matches the current Write Scope Definition's computed hash.
4. On match: mark scope registry `RECONCILED`; token issuance resumes.
5. On mismatch: emit `SCOPE_REGISTRY_DIVERGED` (INTEGRITY, sync, W1) with the reconstructed-head and computed-head hashes; Orchestrator enters `READ_ONLY`. Manual operator intervention required.

No SCOPE_UPDATE ceremonies are accepted until reconciliation completes. In-flight transactions from the pre-restart epoch do not resume — their tokens have been revoked by the restart event.

### 10.9.2 Scope Propagation Bound (GAP-38 related)

Every SCOPE_UPDATED event must propagate to all active token-issuing paths within a 5-second ceiling from Ledger-write-acknowledgment. Propagation is measured as the interval between `SCOPE_UPDATED.ledger_write_ack` and the Orchestrator's last-touched in-memory registry timestamp for `new_scope_hash`.

If propagation exceeds the ceiling, `DIVERGED_STATE` is emitted (CONSISTENCY, sync, W1). DIVERGED_STATE is an Orchestrator-local integrity signal: it triggers an immediate scope-registry self-check and, if the self-check fails, escalates to READ_ONLY via the standard circuit breaker (§11.8).

The 5-second ceiling is a hard invariant of the scope-propagation subsystem; it is not configurable. Ceiling breach must not be silent: either the registry catches up (returning to nominal), or DIVERGED_STATE fires.

### 10.10 Three Consecutive Failure Rule (D31)

Three consecutive scope failures from the same agent in one session: agent suspended, human review flag raised. Integrity failures are always escalated regardless of count (C22).

## 11. State Consistency Layer

### 11.1 Purpose

The Git repository and the `.vindex` overlay must tell the same story, and the system must have a defined answer for every failure mode where they could diverge. This layer specifies which medium is authoritative for which content class, how writes are coordinated across both, and how drift is detected and healed.

### 11.2 Content-Scoped Authoritative Medium (D42)

- **Git authoritative** for `structural_entity` knowledge.
- **`.vindex` authoritative** for Genesis Layer 4 `domain_concept` and `constraint_rule` knowledge.

Every `.larql` patch carries a mandatory `CONTENT_CLASSIFICATION` directive: `structural` | `layer4_domain` (C-SC3, IC-SC1). Value `mixed` is rejected pre-commit (C-SC4). The `CONTENT_CLASSIFICATION_MIXED` rejection (IC-GATE-9) carries split guidance directing the Coder Agent to resubmit as distinct single-classification patches. The split is driven by Gate's triple-level classification check, not the Coder's declared directive. This preserves the authoritative-medium assignment per D42.

### 11.3 Strong Consistency Model (D43)

Strong consistency globally. Reads block against `.vindex` during the mount window. No stale-read fallback. Write concurrency capped at 1 via the Commit Executor FIFO queue (C-CW1). Fan-out occurs above the queue; strict serialization at the queue.

### 11.4 Atomic Transaction Unit (D44, extended T8)

The atomic transaction is the **task-completion package** (C-TPC1):
```
{
  module_code,
  test_suite,
  .larql_patch,
  declared_dependencies    ← added T8
}
```

These commit together or not at all.

### 11.5 Two-Phase Commit Protocol

**Phase 1 — Prepare:**
- Commit Executor receives verified package from Orchestrator (IC-TPC1).
- Writes `PREPARED` Ledger entry with package hash and classification.
- Admits package into the 2PC window; holds session-scoped lock (C-TPC5).

**Phase 2 — Commit (ordering fixed per D46 / C-TPC3):**
1. **Git push first.**
2. **`.vindex` mount second.**

Ordering constrains failure modes to Git-ahead (easier to recover via compensation) rather than Weights-ahead (harder).

On success: writes `COMMITTED` Ledger entry with overlay hash.

Every 2PC produces `PREPARED` and `COMMITTED` entries. Missing `PREPARED` is a Ledger-bypass security incident (C-TPC4).

**§11.5.1 — PREPARED-State Timeout Behavior (D85)**

Two configurable timeout values apply (both stored in Tier 1 config):
`incremental_prepared_timeout` (default 2 hours) for all non-Genesis transactions, and `genesis_prepared_timeout` (no default; Gate blocks Genesis initiation if absent, C-GATE-2) for Genesis compiles.

Incremental timeout: TC executes Phase 1 rollback, releases Write Lock, sets task to `AWAITING_OPERATOR_RETRY`. Dependency Hold persists through timeout — the Hold MUST NOT be released automatically on timeout; it persists until successful commit on retry or explicit operator-signed Hold release. Retry requires fresh token (infrastructure failure class per D67 — no retry budget consumed). Three consecutive timeouts on the same task → human review queue escalation, flagged `repeated_timeout`.

Genesis timeout: circuit breaker trips immediately (`DIVERGED_STATE` type per IC-TC-RESET). No auto-compensation — partial compile state is preserved as forensic evidence. Operator MUST run full model integrity check against the pre-Genesis `IMMUTABLE_ANCHOR` baseline before the reset ceremony may proceed (IC-TC-TIMEOUT).

### 11.6 Genesis as Single Atomic 2PC (D45, C-TPC2)

Genesis compile is a single atomic 2PC event across all tier files L1–L4. Partial Genesis is not a valid state. Architect Agent's internal sub-batching (T6) is transparent to the Ledger.

### 11.7 Transaction Controller — Compensation Authority (D47, C-TC1)

Sole compensating-transaction authority. No agent, including the Commit Executor, self-compensates. Compensation direction determined by `CONTENT_CLASSIFICATION` (C-TC2):

- **Structural patches:** auto-revert Git on persistent `.vindex` failure (3 mount retries, then revert).
- **Layer4_domain patches:** retry `.vindex` up to 5x; Git revert requires human confirmation.

All compensating transactions logged to the Ledger (C-TC4).

### 11.8 Circuit Breaker (D48, C-TC3, extended by GS10–GS11)

Thresholds:
- 3 consecutive 2PC failures in one task → trip (`CONSECUTIVE_FAILURE`).
- 5 consecutive 2PC failures across any tasks in a 10-minute window → trip (`CROSS_TASK_FAILURE`).
- Diverged state → immediate trip, no auto-repair (C-TC5) (`DIVERGED_STATE`).
- Genesis-timeout-without-trip pairing failure (`GENESIS_TIMEOUT_TRIP_MISSING`, C-GTO-1/2, IC-MON-GTOTM).
- Aggregate `SCOPE_HASH_MISMATCH` threshold breach (§14.3, IC-AGG-COUNTER).

On trip: systemwide write suspension (READ_ONLY mode — see §11.8.1). Write resumption requires the signed reset ceremony (IC-TC-RESET). Trip reason is recorded on every `CIRCUIT_TRIPPED` Ledger entry with a **cross-category rationale annotation** (A8 — every `CIRCUIT_TRIPPED` records whether the originating signal was INTEGRITY, CONSISTENCY, or SECURITY category, so the reset ceremony has the provenance context needed for the right precondition branch).

Abort authority (human interrupt of PREPARED transaction): exists via signed abort request to Orchestrator, always routes through Transaction Controller compensation path, never process-kill (OQ-TPC2 resolved D74). Post-commit abort is rejected.

**State machine (extended GS10):** The TC operates under a six-state machine (GAP-58 / GS10 — state lifecycle integration):

| State | Entry | Exit |
|---|---|---|
| `WRITE_ENABLED` | Boot after successful verification; `CIRCUIT_RESET` completion. | Any trip condition → `CIRCUIT_TRIPPED`. Burst-limit breach → `BURST_SUSPENDED`. Double-compromise → `TRUST_ROOT_LOST`. |
| `CIRCUIT_TRIPPED` | Any trip condition. | IC-TC-RESET ceremony (A3 CAK-authorized) → `WRITE_ENABLED`. |
| `READ_ONLY` | Synonym for `CIRCUIT_TRIPPED` operational surface; inference/query proceed. | As `CIRCUIT_TRIPPED`. |
| `BURST_SUSPENDED` | Per-CAK burst limit breach (N=5 / 10min, GAP-41, IC-CAKB-1). | 60-minute auto-clear OR Tier 1 explicit-clear ceremony. Transitions to `WRITE_ENABLED`. |
| `TRUST_ROOT_LOST` | Double-compromise detected (primary CAK and break-glass channel both suspect). Terminal in v1.2. | No automatic exit. Operator recovery requires full genesis reseal procedure (v2 scope). |
| `HALTED` | Reserved for `CONSTITUTIONAL_FAILURE` weak-check advisory (§25). Not auto-entered in v1.2; advisory-only. | N/A (v1.2). |

**BURST_SUSPENDED interaction with circuit reset:** a harness in `BURST_SUSPENDED` rejects IC-TC-RESET ceremonies with `CIRCUIT_RESET_REJECTED_BURST_STATE` until the burst window clears (GAP-58 resolution). Burst-suspension and circuit-trip are orthogonal states; clearing one does not clear the other.

**TRUST_ROOT_LOST is terminal:** a harness in `TRUST_ROOT_LOST` processes no ceremony types and issues no tokens. Only read-query inference proceeds. See §23.3 break-glass.

### 11.8.1 READ_ONLY Mode and Write Resumption Ceremony (D84, revised A1-REVISED + A2 + GAP-35 + GAP-37)

On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human action. Inference, query, and read operations proceed normally; write token issuance is suspended. Consistency Status API state transitions to `CIRCUIT_TRIPPED` (§12.5).

**Consumed tokens proceed to natural outcome (GAP-35).** Tokens that the Gate has already admitted (status: `CONSUMED`) are not invalidated by circuit trip. Their owning transactions proceed through their natural PREPARED → COMMITTED or PREPARED → ABORTED lifecycle under TC supervision. New tokens are not issued in READ_ONLY.

**Governance-category write carve-out (GAP-37, IC-GCO-1 — closes T-SC-W-2).** Governance-category Ledger entries written as part of the signed reset ceremony itself proceed regardless of `CIRCUIT_TRIPPED` state. This is a narrow carve-out: only entries whose `audit_category: GOVERNANCE` and whose ceremony_token_id binds them to the active IC-TC-RESET invocation are permitted. Token-mediated writes (Coder/Architect/Pruning output) remain suspended. This carve-out is a W3 cross-reference (§16.2) — the emergency-writer tier is the only writer that can emit during `CIRCUIT_TRIPPED`, and only for the reset ceremony's own Ledger entries.

**Write resumption requires a signed reset ceremony (IC-TC-RESET, A3 — CeremonyToken / CAK-authorized).** The TC independently verifies preconditions before accepting any reset request — human attestation alone is not sufficient.

**Admission order for IC-TC-RESET:**

1. **Precondition branch selection** by trip reason (cross-category annotation, A8):
   - `CONSECUTIVE_FAILURE` or `CROSS_TASK_FAILURE`: compensation is `COMPLETED` and current overlay hash matches the Ledger's most recent `COMMITTED` entry.
   - `DIVERGED_STATE`: a `RECONCILIATION_COMPLETE` Ledger entry with `result: "CONSISTENT"` timestamped after the trip.
   - `GENESIS_TIMEOUT_TRIP_MISSING`: a matching paired trip entry must exist (C-GTO-2).
   - Genesis-trip Hold release (A12): if the trip occurred during Genesis and any Dependency Holds remain active from the pre-trip epoch, a paired `HOLD_RELEASE` ceremony must have resolved those Holds before IC-TC-RESET can admit.
2. **CeremonyToken verification** against `ceremony_authorization_key_anchor` (§13.2, §20). ceremony_type discriminator must equal `CIRCUIT_RESET`.
3. **Precondition check** — if any branch precondition fails, the TC rejects with `CIRCUIT_RESET_REJECTED` (A2), emitting a Ledger entry that names the unmet precondition. The submitted CeremonyToken is **not** consumed by a precondition-check rejection (GAP-35 — consumed tokens proceed to natural outcome; but a precondition-rejected token is not consumed because the ceremony never admitted).
4. **CAK verification** — signature validity over the reset envelope.
5. **`CIRCUIT_RESET` Ledger write** (GOVERNANCE, synchronous) → state transitions to `WRITE_ENABLED`.

Reset via the W3 emergency Ledger path is not permitted as a substitute for the signed ceremony. The signed ceremony is the exclusive mechanism for write resumption. (The W3 governance carve-out above permits W3 writes of the ceremony's own Ledger entries, not W3 writes as reset.)

### 11.8.1.1 Bounded Compensation Under READ_ONLY (A1-REVISED; C-CRC-3)

Transaction Controller compensation during READ_ONLY is **bounded to reversal-only** operations. The TC MUST NOT perform forward progress, speculative reapplication, or any compensation whose effect is to advance state beyond the last `COMMITTED` entry. Permitted compensation operations:

- **Git revert** of the failed transaction's staged commit (Structural content classification).
- **`.vindex` overlay rollback** to the pre-PREPARED tier state.
- **Ledger annotation** via `ABORTED` entry + `COMPENSATION_COMPLETED` entry.

Prohibited during READ_ONLY:

- Retry of the failed transaction (retries are a pre-trip construct; after trip, the transaction is terminal).
- Any `COMMITTED` entry emission for the failed transaction's content.
- Any overlay write beyond rollback to the trip-time `anchor_hash`.

Violation of the reversal-only bound produces `BOUNDED_COMPENSATION_VIOLATION` (INTEGRITY, sync, W1). Standard IC-TC-RESET applies to resume from such a trip; the forensic record carries `trip_reason: TC_COMPENSATION_OVER_SCOPE` (GAP-43 / GS11).

### 11.8.1.2 Reset Ceremony Under Orchestrator Degradation (GAP-24 / v3 GS5)

If the Orchestrator process is degraded — unable to route ceremony envelopes, crash-looped, or in an unresponsive control-plane state — the TC accepts IC-TC-RESET envelopes submitted via a **direct-to-TC channel** bypassing the Orchestrator's normal ceremony router. This is a narrow, operator-invoked pathway:

- Operator invokes the `tc_direct_reset` tool against the live TC process.
- The envelope is still a CeremonyToken structurally identical to the Orchestrator-routed form (§20), including full CAK signature and replay-rejection binding.
- The TC performs the full IC-TC-RESET admission order (§11.8.1) independent of the Orchestrator's routing state.
- The resulting `CIRCUIT_RESET` Ledger entry carries an `operator_routing_override: true` flag and a `degradation_reason` field authored by the operator.
- On successful reset, the Orchestrator is **not** automatically restarted; recovery of the Orchestrator control plane is a separate operational step.

This pathway exists to prevent an Orchestrator failure from creating an unrecoverable `CIRCUIT_TRIPPED` lockout. The CAK-verification requirement means the Orchestrator's control-plane state is not a security dependency of the reset ceremony itself. Tier 1 CAK anchor is the single root of trust for admission.

### 11.9 The Lock / Hold Split (T8)

Two distinct Orchestrator-managed concepts:

**Write Lock** — concurrent write prevention only:
- Acquired at task declaration (D59, C-CW3).
- 60-minute TTL with auto-release (D60, C-CW5).
- Blocks other agents from writing to the declared region.
- Released on task completion, abort, or TTL expiry.

**Dependency Hold** — dependency preservation across long-escalation tasks:
- Placed on specific edges the task is *reading* (its dependency set).
- 72-hour TTL, renewable on escalation events.
- Blocks Pruning on held edges only.
- Does not block other agents from acquiring Write Locks or writing novel facts.
- Released on task completion, abort, or TTL expiry.

Commit-time collision after declaration-time lock is a security incident (D61).

### 11.10 Escalation Phase Lock/Hold Behavior (T8)

| Escalation Step | Write Lock | Dependency Hold |
|---|---|---|
| Parent → Subtask Decomposition | Released if expired / transferred if within TTL | **Transferred** to subtasks, scoped per subtask |
| Peer Agent Review | **Renewed** (fresh 60 min) | **Renewed** (fresh 72 hrs) |
| Human Escalation Queue | **Released** | **Maintained**, auto-renewed while in `IN_HUMAN_QUEUE` |
| Logged Suspension | Released | Released |

**Task resume re-verification protocol:** when an escalated task resumes, Orchestrator compares current state of all held edges against the escalation-entry snapshot. `context_stale` (edge changed) → task repackaged with current state. `context_lost` (hold expired before resume) → task may be re-escalated with `dependency_reconstruction_required`.

### 11.11 Dependency Set Identification (T8)

Hybrid declaration model:
- Coder Agent declares initial dependency set as part of task-completion package (`declared_dependencies` field).
- Orchestrator extends the Dependency Hold automatically on observed reads (Agent Runtime Wrapper mediates all reads).

Sanity cap: no more than 10% of project edge count per task declaration. Soft cap, escalates to human review on exceedance.

### 11.12 Pruning Agent (D53–D57, extended T8, T10, GAP-11, T-PM-vs-PA)

- Pruning writes flow through the standard 2PC path. No fast-path (D53, C-PA1).
- Restricted to Structural and Knowledge family edges only (D54, C-PA2).
- Cannot touch Genesis tiers L1–L3 (C-PA3).
- Cannot delete edges younger than 24 hours (D56, C-PA5).
- **Cannot delete edges under active Dependency Hold** (T8, IC-PA7).

**Trigger conditions (D57):** every 50 commits or 24 hours; on source file deletion; on function rename detection; on out-of-band commit; on Session 4 D37 gap record followup; manual trigger.

**Backpressure (D55):** 24-hour staleness window; edges older than 24h classified `stale_urgent`. At 1,000 `stale_urgent`, writes suspended until Pruning completes.

**External source audit (GAP-11 / v3 GS9 — see §26).** The Pruning Agent runs a dedicated `external_source_audit` sub-routine over Layer 4 facts with external document provenance. For each Layer 4 fact carrying a provenance block, the sub-routine checks the referenced external document's declared staleness signals (fetch timestamp, content hash, publisher-declared version). Staleness does not trigger deletion — it produces an advisory entry on the Reconciliation Review Queue. Classification: advisory-only; operator acknowledgment required to resolve.

**Merged advisory queue policy (T-PM-vs-PA / GS11 — IC-REVIEW-QUEUE amended).** External-provenance staleness advisories merge into the existing review queue item for the same `edge_id`, rather than creating a separate queue item. CORE-importance facts with STALE or UNAVAILABLE external-document provenance receive priority elevation in the merged item. Both advisory reasons (Pruning's staleness signal and Provenance Monitor's external-document signal) MUST be acknowledged before the merged item can be resolved. Tension T-PM-vs-PA is closed by this policy.

### 11.13 Out-of-Band Git Reconciliation (D52, T10)

Humans or external tools may commit to Git outside the harness pipeline. Pruning Agent detects these and generates catch-up patches flagged `requires_human_review`. **No auto-compile.**

Catch-up patches route to the Reconciliation Review Queue (T10 IC-PA8, IC-OR10) — see §15.

### 11.14 Overlay Compaction (D62–D66, revised T9, extended D83, D86)

**Strategy:** full MEMIT re-run on active `.larql` patches. Delta composition is rejected on correctness grounds.

**Triggers (revised T9):** Compaction trigger evaluation uses the `drift_state` object exposed by the Write Engine (IC-WE-1, D83). Trigger conditions:
- Drift tier `WARNING` (edge count reaches warning threshold since last anchor): schedule at next idle window.
- Drift tier `HARD` (edge count reaches hard trigger): immediate, blocking writes.
- Time-based scheduler: every 30 days since last anchor.
- `drift_state.overlay_file_count` ≥ 50: schedule.
- `drift_state.p95_latency_ratio` ≥ 2.0 (p95 inference latency at 2× baseline): schedule.
- Manual.

All drift threshold values are provisional pending empirical validation (OQ-W1).

**Verification (D66, extended D86):** Behavioral Probe returns a structured `CompactionProbeReport` to the TC before Phase 2 commit (IC-OC-PROBE). Sampling: 100% of CORE edges (full), ≥20% of SUPPORTING edges (stratified, floor 5 probes), 10% of INCIDENTAL edges (stratified, floor 3 probes). Random seed logged for reproducibility. Abort thresholds: CORE pass rate MUST equal 1.0 (C-OC3 — any CORE failure is an immediate compaction abort); SUPPORTING ≥95%; INCIDENTAL ≥80%. Abort → existing overlays retained, `COMPACTION_ABORTED` Ledger entry with serialized `CompactionProbeReport` as payload. CORE failures individually listed; SUPPORTING and INCIDENTAL failures summary-logged unless ≤10 IDs.

Probe infrastructure failure → `COMPACTION_PROBE_FAILED` entry (distinct from `COMPACTION_ABORTED`). Both are distinguishable in the Ledger for operator diagnostics. All SUPPORTING and INCIDENTAL thresholds and sampling rates are provisional pending OQ-OC3 / OQ-W1 calibration. The CORE 1.0 threshold and C-OC3 are not provisional.

Genesis tiers never compacted (C-OC1). Compaction is a single atomic 2PC event (C-OC2).

### 11.15 State Ledger as the Unified Substrate

**The Ledger unifies what was previously specced as separate audit trail and State Ledger artifacts (T11).** All integrity-anchored event records — security, consistency, validation, governance, lifecycle — land in one log with audit-category tagging. See §16 for the full Ledger specification.

## 12. Orchestration Layer

### 12.1 Purpose

The Orchestrator is the single control point for all component coordination. Every agent invocation, every Ledger write, every queue transition, every configuration read is mediated through it. Components do not communicate peer-to-peer; all flow converges at the Orchestrator.

### 12.2 Core Non-Negotiables (C-OR1 to C-OR6)

- Must satisfy the eight non-negotiable requirements from the Session 6 matrix (control flow, state, heterogeneous steps, 2PC, HIL, observability, concurrency, extensibility).
- The write path (Patch Authorization Gate → Commit Executor → MEMIT → Git) must be deterministic, non-reasoning code. LLM-based agents never hold simultaneous write access to both state mediums.
- Agent identity and runtime framework isolated behind a single invocation wrapper (IC-OR5). Swapping agent runtime must not require re-speccing graph structure or orchestration plumbing.
- Scope Lock Registry, State Ledger, and Audit category views are Orchestrator-owned. Agents never read or write them directly.
- Aggregate retry budget preserved across task decomposition (C-OR5).
- Commit Executor FIFO queue serialization is the exclusive chokepoint (C-OR6). Fan-out above; strict serialization at the queue.

### 12.3 Three Path Options (D72 — Deferred to Operator)

Three architecturally complete paths for operator selection:
- **Path A** — LangGraph alone.
- **Path B** — Claude Agent SDK alone.
- **Path C** — Hybrid (LangGraph + SDK).

No path is recommended in this spec. All three are comparable; selection is operational policy. Regardless of path, the 2PC Transaction Controller and the Merkle-chain State Ledger are custom components — no evaluated candidate ships them natively (D80).

Eliminated from consideration:
- **Pi** (D69): correctly categorized as an agent runtime, not an orchestrator. Fails non-negotiables 1, 5, 6, 7.
- **n8n** (D70): execution model (HTTP/function-call nodes) mismatched with multi-minute GPU-bound MEMIT compile as first-class step.
- **OpenClaw + Lobster** (D71): chat-gateway-first architecture wrong deployment shape for a pure dev harness. Viable but not advantaged vs. LangGraph.

### 12.4 Scope Lock and Hold Registry (IC-CW1, IC-OR4, extended T8)

Orchestrator-owned. Agents query via API; direct registry manipulation is integrity violation (OQ-CW2 resolved D78).

Unified typed registry: `write_lock` | `dependency_hold` entries. See §17 for full concurrency model.

### 12.5 Consistency Status API (D75, extended T10 IC-OR12)

Exposes real-time consistency status to agents via Orchestrator-mediated API only (OQ-TC3 resolved D75). Six states:
- `NORMAL`
- `COMPACTION_IN_PROGRESS`
- `CIRCUIT_TRIPPED` — systemwide write suspension. READ_ONLY mode is active: inference and query operations proceed; write token issuance is suspended. Enters this state automatically on TC circuit-breaker trip. Exits only via IC-TC-RESET signed ceremony (D84).
- `DIVERGED`
- `GENESIS_LOCKED`
- `RECONCILIATION_BACKLOG` *(added T10)*

Agents must check status before task acceptance.

### 12.6 Task Lineage Ledger (IC-OR9)

`TASK_DECOMPOSED` entries link subtask IDs to original task ID. Aggregate retry count tracked across subtasks. Enables reconstruction of escalation trees for post-hoc review.

### 12.7 Review Queue Management (T10)

Orchestrator maintains two named review queues with distinct semantics. See §15.

### 12.8 Idle-Window Detection (D79, closes OQ-OC1)

Orchestrator-internal. Heuristic: queue depth 0 + active locks 0 + no `PREPARED` 2PC for N minutes (default 30). Not exposed to agents. Used to schedule compaction and other background operations.

### 12.9 Path Classification (D76, extended T4)

Path classification stored at `.harness/path-classification.json` (Tier 3 Anchored Git Config). Git-committed, per-project. Harness ships default baseline. Classification drives 2PC compensation direction:
- `parametric_required` — default (safe failure).
- `parametric_none` — cannot be self-declared by agents (C-GOC3).
- `parametric_deferred` — delayed reconciliation via Pruning catch-up.

---

═══════════════════════════════════════════════════
# PART IV — CROSS-CUTTING CONCERNS
═══════════════════════════════════════════════════

## 13. Configuration Governance — The Three-Tier `.harness/` Model (T4)

### 13.1 Core Rule

Integrity-critical artifacts are classified by trust tier, not by artifact type. Three tiers with distinct integrity mechanisms:

### 13.2 Tier 1 — Immutable Anchor

Mint-once, verify-forever. Trust root.

**Artifacts:**
- `genesis-seal.json` — includes `current_larql_version`, `min_supported_larql_version`, `larql_migration_manifest`, `corpus_author_bootstrap_identity` (GAP-8 / v3 GS8 — replaces the v1.1 `corpus_author_identities` array; the evolving full list now lives in the `corpus-author-registry/` Tier 2 sealed corpus; the Tier 1 field records only the bootstrap identity that seeded the registry), `incremental_prepared_timeout`, `genesis_prepared_timeout` (no default; must be set before Genesis initiation per C-GATE-2), `ceremony_authorization_key_anchor` (A10 — public-key anchor against which every CeremonyToken envelope signature is verified, per §20 / IC-SCOPE-AUTH-1), `scope_mismatch_aggregate_threshold_n` and `scope_mismatch_aggregate_window_seconds` (GAP-38 / GS12 — see §14.3), and the genesis hash fields.
- `orchestrator-key-anchor.json` (public half of Orchestrator signing key)
- `break-glass-anchor.json` (A11-related; second Tier 1 anchor used by the break-glass channel, §23.3 / IC-BG-1).

**Write model:** produced once during bootstrap. Never modified by runtime. CAK rotation is v2 (GAP-19).

**Integrity:** dual-stored (`.state-ledger/` primary + `<repo_root>/.harness/` secondary). Boot-time hash comparison. Mismatch suspends boot.

### 13.3 Tier 2 — Sealed Artifacts

Evolving human-authored integrity-critical artifacts. Signed-append model.

**Artifacts (v1.2 — seven sealed corpora):**
- `meta-validator-suite/` — Validator held-out corpus.
- `meta-tga-corpus/` — TGA held-out corpus.
- `constitutional-suite/` — Constitutional test suite (promoted from S4 D32).
- `write-scope-definitions/` — Per-agent write authority definitions.
- `reconciliation-reviewers/` — Authorized reviewers for Reconciliation Review Queue.
- `corpus-author-registry/` — **Sixth sealed corpus (GAP-8 / v3 GS8).** Authoritative list of identities authorized to submit cases to Meta-Validator and Meta-TGA corpora. Supersedes the v1.1 Tier 1 `corpus_author_identities` array. Per-author fields include `author_id`, `key_fingerprint`, `authorized_corpora` (subset of `{meta-validator-suite, meta-tga-corpus, constitutional-suite}`), `expires_at`, and `bootstrap_link` (references the Tier 1 `corpus_author_bootstrap_identity` for the registry's initial identity). Expiry enforcement per §24.
- `hook-registry/v1` — **Seventh sealed corpus (GAP-54 / GS11).** Authoritative record of permitted boot-time and runtime hook binary hashes. Every hook binary loaded by the harness is hash-matched against this registry at boot. Mismatch produces `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) and suspends boot. See IC-HOOK-BOOT.

**Write model:** versioned additive directories (`v1/`, `v2/`, ... `vN/`). Each version signed by operator key. `manifest.json` tracks current active version and signatures.

**Integrity:** dual-store hash (`.sealed-corpora/<n>/manifest.json` + `SEALED_CORPUS_UPDATE` Ledger entry). Boot-time verification.

**Access:**
- Meta-* corpora: time-bounded capability access during Meta-* runs only. Never exposed to normal Validator or TGA operation.
- Constitutional suite: Validator has persistent read access during normal operation.
- Write Scope Definitions: Authorization Gate has persistent read access during normal operation.
- Reconciliation reviewers: Gate reads when verifying `reconciliation_reviewer_id`.
- Corpus author registry: consulted by IC-SL7 token issuance path and by Meta-* case-submission ingress (§24).
- Hook registry: consulted by boot sequence (IC-HOOK-BOOT) and by any hook-reload ceremony.

**Per-case audit reporting mandatory** for Meta-* runs (T3 closure of OQ-V5). Aggregate-only reporting is forbidden.

**Corpus Authorship Model (D88, IC-CORPUS-AUTH, extended IC-SL7 + §24)**

Corpus authorship is a restricted operator role (C-GOC4). Only identities listed in the active `corpus-author-registry/vN/` sealed corpus may submit cases. No agent identity MUST appear in the registry. Authorization is verified at two points (§24 expiry enforcement):

1. **Submission ingress** — the Orchestrator verifies author identity + `expires_at` predicate at submission time (A12-IC-CORPUS-AUTH — closes the v1.1 gap where expiry was checked only at token issuance).
2. **IC-SL7 token issuance** — the Orchestrator re-verifies expiry at Meta-* run initiation and includes a `contains_expired_author_cases` response field in the IC-SL7 envelope (A13-IC-SL7).

Case formats are formally defined:

- *Meta-Validator case format:* `{ id, prompt, expected_assertion_set: [{ type, value }...], expected_pass }`
- *Meta-TGA case format:* `{ id, specification_fragment, gold_test_set: [{ test_name, assertion_count (≥2), asserts_symbols }...] }`

Minimum viable corpus: 20 cases before any Meta-* run produces a meaningful Health Score. Below minimum, the `health_score` field is `NOT_COMPUTED` — not zero, which would be indistinguishable from a failed run. A corpus staleness flag (`corpus_staleness_flag: true`) is set on the health record if no case has been added in 90 days. Cadence is operator-owned policy, not enforced by this spec.

### 13.4 Tier 3 — Anchored Git Config

Git-committed operational configuration with integrity anchoring.

**Artifacts:**
- `path-classification.json`
- `agent-yamls/*.yaml`
- `genesis-seal.json` (secondary copy of Tier 1)
- `orchestrator-key-anchor.json` (secondary copy of Tier 1)
- `rate-limits.json` — carries `scope_update_min_interval_seconds` (per-initiator primary + per-affected-agent-id secondary; GAP-27 resolution) and related per-CAK / per-ceremony-type rate parameters. See §10.9 admission order and §14.3.

**GAP-27 Tier placement note:** `scope_update_min_interval_seconds` was resolved to Tier 3 placement in `rate-limits.json`. A separate open item remains for whether certain rate parameters that also participate in boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation should migrate to Tier 1; this Tier conflict is deferred to GS13 disposition (OQ-CFG-TIER).

**Write model:** modified via Git commit. Git commit-hook writes `CONFIG_UPDATE` Ledger entry with filename, new hash, Git commit hash.

**Integrity:** Ledger anchor + boot-time hash verification. Boot-time mismatch between current file hash and most recent `CONFIG_UPDATE` entry produces `CONFIG_INTEGRITY_FAIL` and suspends writes.

**Enforcement mode:** detect-at-boot, not prevent-at-write. Stronger enforcement (pre-receive server-side hook) is v2.

### 13.5 Boot-Time Verification Sequence (T4, extended T5, T11, GS5 v3, GAP-46, GAP-54)

Fail-closed. Any step failing suspends writes and produces an integrity-violation event.

1. State Ledger Merkle chain verification from Genesis Seal forward.
2. Genesis Seal dual-store comparison.
3. **Orchestrator key anchor dual-store comparison** (T5).
3a. **CAK anchor semantic verification (v3 GS5 — locally labeled D99/D100 in GS5 v3; see Appendix H collision register).** The `ceremony_authorization_key_anchor` field in `genesis-seal.json` is not merely hash-compared — its public-key material is parsed, the key type (algorithm identifier) is verified against the permitted-algorithm set in the harness release manifest, and the break-glass anchor (`break-glass-anchor.json`) is verified to be structurally independent (distinct public-key material, distinct algorithm-parameter tuple). Failure: `CAK_ANCHOR_SEMANTIC_INVALID` (SECURITY, sync, W1) suspends boot.
4. Sealed corpus manifest verification (for each Tier 2 artifact — seven corpora in v1.2, including `corpus-author-registry/` and `hook-registry/v1`).
4a. **Hook binary integrity check (GAP-54 / GS11 — IC-HOOK-BOOT).** Every hook binary loaded from `hook-registry/v1/` has its current filesystem hash matched against the registry-declared hash. Mismatch: `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) suspends boot.
5. Anchored Git config verification (for each Tier 3 artifact, including `rate-limits.json`).
5a. **Rate-limit / retention-window consistency check (GAP-46 / GS11 — IC-BOOT-RLRF).** TC verifies that `scope_update_min_interval_seconds` (both per-initiator and per-affected-agent) is strictly less than the minimum retention window for `SCOPE_UPDATED` Ledger entries. The check also verifies equivalent relationships for every rate-limited ceremony type against its corresponding Ledger retention floor. Failure: `RATE_LIMIT_RETENTION_CONFLICT` (SECURITY, sync, W1) suspends boot.
6. Agent YAML ↔ Write Scope Definition binding verification.
7. Periodic integrity verification cadence established (T11).

All pass → writes enabled. Any fail → writes suspended, `<TIER>_INTEGRITY_FAIL` (or the named-failure entry as listed above) produced, human review required.

## 14. Token and Authorization Lifecycle (T5, T7)

### 14.1 Unified Token Model

Two token types share the same admission-time-validation pattern:

**Invocation Token (T5):**
- Issued per agent invocation by Orchestrator.
- 10-minute TTL, single-use.
- Consumed at Authorization Gate on patch submission.

**Schema Migration Token (T7, revised D27):**
- Issued when human authorization gesture completes (Genesis or L1–L3 modification).
- 10-minute admission-time TTL.
- Consumed at 2PC Phase 1 admission. Compile proceeds independent of subsequent token state.

Both tokens carry hashes binding them to the full governance state at issuance time (Write Scope Definition version, Agent YAML version). Stealing a token is insufficient if any bound document changes within the TTL window.

### 14.2 Token Lifecycle Ledger Entries

Each token produces a paired issuance/outcome record in the Ledger. Every `*_ISSUED` resolves to exactly one of `CONSUMED`, `REJECTED`, or `EXPIRED_UNUSED`. Unresolved tokens past the reconciliation window are an integrity signal.

### 14.3 Failure Mode Interaction with Retry Budget

- **Token expiry before Gate consumption** — infrastructure failure class. Fresh token issued; retry budget not consumed.
- **Hash mismatch (mid-flight governance update)** — infrastructure failure class. Agent re-reads current state; retry budget not consumed.
- **Double-consumption** — security incident. Agent suspended; retry budget not consumed (task aborted, not retried).
- **Signature failure** — security incident. Agent suspended; retry budget not consumed.
- **Scope hash mismatch (`SCOPE_HASH_MISMATCH`)** — infrastructure failure class (D87). Gate returns structured payload including `current_scope_hash` and `scope_updated_at`. Orchestrator MUST re-issue token against current scope hash — NOT the stale hash. Retry budget not consumed. Distinguished from generic hash-mismatch by the `SCOPE_HASH_MISMATCH` error code. **Two consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation (A4 — threshold lowered from 3 in v1.1 to 2 in v1.2)** → Orchestrator emits `SCOPE_MISMATCH_ESCALATED` (SECURITY, sync, W1) and routes the invocation to human review queue. The lowered threshold reflects the Warden's concern that three-attempt repetition provided a narrow oracle window.

**Aggregate `SCOPE_HASH_MISMATCH` detection (GAP-38 / GS12 — IC-AGG-COUNTER, IC-AGG-ALERT-LINK).**

Per-invocation escalation (above) catches narrow loops; a per-Orchestrator-instance aggregate counter catches low-signal-rate distributed attacks.

- **Aggregate threshold:** `scope_mismatch_aggregate_threshold_n` (default N=10) within a sliding window of `scope_mismatch_aggregate_window_seconds` (default M=60). Both parameters are Tier 1 config (`genesis-seal.json`).
- **Scope:** per-Orchestrator-instance global; counts across all invocations and all agents.
- **Alert path (IC-AGG-ALERT-LINK):** on threshold breach, emit `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1) and cross-link to a newly-created review queue item. The cross-link carries the list of contributing invocation IDs and their source agents.
- **Counter behavior (IC-AGG-COUNTER):** counter increments on each `SCOPE_HASH_MISMATCH` regardless of per-invocation re-issue outcome. Counter is **not reset** by review-queue acknowledgment. Cooldown after alert: equal to the sliding window (M seconds); during cooldown the counter continues to accumulate but suppresses duplicate alerts.
- **Failure behavior:** alert is advisory at the aggregate level. It does not directly trip the circuit breaker — but if the Warden's operator-defined escalation policy maps `SCOPE_MISMATCH_AGGREGATE_ALERT` to circuit trip, the breaker's existing cross-category machinery (§11.8, A8) applies.

Both the per-invocation and aggregate thresholds are parameters the operator may tune. Both are Tier 1 — their modification is a Genesis Seal change.

### 14.4 Orchestrator-Signed as the Unifying Authority

Invocation tokens, schema migration tokens, and Ledger write authorization all route through the Orchestrator. The Orchestrator's signing key is the single cryptographic anchor that ties together agent identity, write authorization, and integrity-anchored record-keeping.

## 15. Review Pathways — Two-Queue Model (T10)

### 15.1 Two Distinct Review Types

**Correctness Review Queue** — populated by Reflexion escalation (D37 Step 3).
- Reviewer question: *"Is this agent output acceptable?"*
- Contains: task spec, retry history, decomposition log, failure tier, consistency status.
- Decisions: `approve_as_is` | `reject` | `re_route_for_further_work`.
- **Default on neglect:** task times out into logged suspension (D37 Step 4). Work is lost; no state changes.

**Reconciliation Review Queue** — populated by Pruning Agent catch-up patches with `requires_human_review` flag, by `external_source_audit` advisory entries (§26), and by cross-links from `SCOPE_MISMATCH_AGGREGATE_ALERT` (§14.3).
- Reviewer question: *"Should we update parametric memory to match out-of-band state change or external-document change?"*
- Contains: out-of-band Git commit hash and diff (for Pruning entries), external-document provenance staleness or unavailability signal (for provenance entries), contributing-invocation list (for aggregate-alert cross-links), proposed catch-up `.larql` patch where applicable, classification rationale, age, advisory-reason(s).
- Decisions: `approve_patch` | `reject_patch` | `modify_patch` | `defer_with_reason` | `acknowledge_advisory` (for advisory-only entries).
- **Default on neglect:** no silent default. Items accumulate; backlog signals escalate via Ledger and Consistency Status API.

**Merged queue policy (T-PM-vs-PA / GS11 — IC-REVIEW-QUEUE amended):** when multiple advisory reasons target the same `edge_id`, they merge into a single queue item rather than creating separate items. CORE-importance facts with STALE or UNAVAILABLE external-document provenance receive priority elevation in the merged item. Both advisory reasons MUST be acknowledged before the merged item can resolve. This replaces the v1.1 one-item-per-signal model.

### 15.2 Backlog Signals (Reconciliation Queue)

Tiered:
- ≤ 10 items, all < 7 days old: `NORMAL` state.
- > 10 items OR any > 7 days: `RECONCILIATION_BACKLOG_WARNING` Ledger entry; Consistency Status surfaces flag but state remains `NORMAL`.
- > 50 items OR any > 30 days: `RECONCILIATION_BACKLOG_CRITICAL` Ledger entry; Consistency Status state becomes `RECONCILIATION_BACKLOG`.
- `stale_urgent` edge count > 1,000 (D55): write suspension triggers independently.

### 15.3 Reviewer Authority

Reconciliation reviewers are a named subset in the Tier 2 sealed corpus `reconciliation-reviewers/`. Reviewer identity recorded in decisions and stamped into `.larql` patch metadata (`reconciliation_reviewer_id` field).

### 15.4 `modify_patch` Semantics

Reviewer-modified patches re-enter the standard pipeline as new submissions. Validator cascade (9.3) runs on the modified patch. Validator rejection returns the item to the queue with feedback attached. This preserves Validator independence when humans are in the authoring seat.

### 15.5 Dependency Hold Interaction

Catch-up patches respect Dependency Holds. Held edges excluded from patch delete operations. Conflicts (out-of-band change conflicts with held edge) flagged `dependency_conflict` — reviewer must explicitly resolve (wait for task resolution, or document explicit hold release).

## 16. The Unified Ledger (T11)

### 16.1 Consolidation

The State Ledger and the previously-separate audit trail (D28) are **one artifact**. D28's intent is preserved; "audit trail" becomes an organizational lens on the Ledger via the `audit_category` entry field, not a separate store.

**Location:** `<harness_root>/.state-ledger/ledger.jsonl`. Append-only. Merkle-chain-lite integrity (D50). Outside Git and outside `.vindex`.

### 16.2 Three-Tier Writer Model (extended by GAP-29b / GS10 — W3 scope consolidation)

**Tier W1 — Orchestrator-mediated writes** (default for all component writes):
All components route writes through the Orchestrator, which verifies component identity, validates entry schema, assigns Merkle predecessor hash, and appends.

Writers under W1: Authorization Gate, Commit Executor, Meta-Validator, Meta-TGA, Validator, Pruning Agent, Transaction Controller, Human Review writers, Config Update Hook.

**Tier W2 — Bootstrap writes** (one-time):
During initial bootstrap sequence only. Writes Genesis Seal, Orchestrator Key Anchor, CAK anchor, break-glass anchor, `PROJECT_INITIATED` (retention policy declaration), and initial chain anchor. After bootstrap completes, bootstrap writer is retired; any subsequent bootstrap-class entry attempt is an integrity violation.

**Tier W3 — Emergency Escalation Path** (narrow, consolidated GAP-29b / GS10):

W3 is an **exceptional** write path: it bypasses Orchestrator mediation and is limited by policy to a small, ratified entry-type set. In v1.1 the only W3 entry type was `INTEGRITY_VIOLATION_EMERGENCY`. Subsequent gap resolutions added three further ratified carve-outs. The consolidated v1.2 W3 scope policy is given by **C-W3-1** (two admission criteria, both must hold) and **IC-W3-POLICY-1** (the consolidated admission contract).

**C-W3-1 — W3 admission criteria (both required):**

1. **Originator criterion:** the writer MUST be one of Gate, Transaction Controller, Boot-verifier, or (for ceremony-carve-out entries only) the ceremony-mediating code path executing an IC-SCOPE-AUTH-1-authorized ceremony. No other component may emit a W3 entry.
2. **Entry-type criterion:** the entry type MUST be on the ratified W3 carve-out list (below). No new entry types are added to W3 without amendment.

**IC-W3-POLICY-1 — ratified W3 carve-out list:**

| Entry Type | Carve-out Rationale | Source |
|---|---|---|
| `INTEGRITY_VIOLATION_EMERGENCY` | Original W3 scope — log compromised-Orchestrator scenarios where the normal W1 path is the problem. | v1.1 baseline. |
| Governance ceremony entries emitted during `CIRCUIT_TRIPPED` | The IC-TC-RESET ceremony itself must emit Ledger entries, but the Orchestrator's normal mediation path is suspended by the trip. Narrow carve-out: only entries whose `audit_category: GOVERNANCE` and whose `ceremony_token_id` binds them to the active ceremony. | GAP-37 / GS10 — closes T-SC-W-2, IC-GCO-1. |
| `TRUST_ROOT_LOST` entry | Emitted by the boot-verifier when both primary CAK and break-glass channel are compromise-suspect. Cannot route through Orchestrator because Orchestrator trust is itself lost. | GAP-42 / GS10 — IC-BG-1. |
| `BURST_SUSPENDED` entry | Emitted by the CAK enforcement path when per-CAK burst limit is breached; originator is Gate or TC, not Orchestrator. | GAP-41 / GS10 — IC-CAKB-1. |

Each W3 carve-out is subject to:
- Maximum 1 entry per minute per originator per entry type (rate limit).
- Strict schema enforcement — W3 entries use the same schema as their W1 equivalents; only the writer tier differs.
- Immediate write suspension on emission (except for the reset-ceremony carve-out, which by definition operates during write suspension).
- Forced human investigation via review queue cross-link.

Any W3 emission that does not meet C-W3-1 is itself a `W3_SCOPE_VIOLATION` (INTEGRITY, sync, W1) — detected at Ledger append by the Merkle-chain validator.

Aggregate-detection entry types (e.g., `GENESIS_INITIATION_ABUSE_PATTERN` from GAP-44) are **not** W3-eligible per C-W3-1 — they route through W1 because the Orchestrator remains trusted in those scenarios. The general framework convention for aggregate-detection entries (always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item) is GAP-55, deferred to post-v1 integration pass.

### 16.3 Write Mode Classification

**Synchronous (blocking)** — entries that must complete before the triggering operation proceeds:
- `TOKEN_CONSUMED` at Gate admission.
- `PREPARED` at 2PC Phase 1.
- `COMMITTED` at 2PC Phase 2.
- `COMPENSATED` entries.
- All `INTEGRITY_VIOLATION` entries.
- `CIRCUIT_TRIPPED`, `CIRCUIT_RESET`, `CIRCUIT_RESET_REJECTED`.
- `TIMED_OUT`, `RECONCILIATION_COMPLETE`.
- `SCOPE_UPDATED`, `SCOPE_UPDATE_REJECTED`.
- `RETENTION_OVERRIDE_REJECTED`.
- `PROJECT_INITIATED`, `PROJECT_CLOSED`.
- `VERSION_REJECTED`, `VERSION_UNSUPPORTED`.
- `CORPUS_WRITE_REJECTED` (UNAUTHORIZED_AUTHOR reason).
- `COMPACTION_ABORTED`, `COMPACTION_PROBE_FAILED`.

**Asynchronous (durable queue)** — observation entries:
- Meta-Validator / Meta-TGA health records.
- Sealed Corpus access records.
- Config update notifications.
- `LARQL_VERSION_LEGACY` (advisory).
- `CORPUS_CASE_ADDED`.
- `COMPACTION_CORPUS_SMALL` (advisory).
- `CONTENT_SPLIT_LOOP` (advisory).

Async writes go through WAL (`<harness_root>/.state-ledger/wal/`) before acknowledgment. WAL replays on crash. Ordering preserved within the queue; Merkle-chain order remains consistent.

### 16.4 Integrity Verification Cadence

- **Boot-time:** full chain walk from Genesis Seal forward (unchanged from D50).
- **Light verification:** every 100 entries appended. Verifies last ~10 entries. Cheap; catches immediate corruption.
- **Full verification:** every 10,000 entries OR 24 hours, whichever first. Walks entire chain.

Chain-break detection during any verification triggers immediate write suspension.

**Entry-count bounds for full verification (GAP-53 / GS11).**

Full chain verification is a linear-time operation in Ledger entry count. Operating envelope on reference hardware:

- **Typical project range:** 100K–1M entries. Full verification is routinely tractable.
- **Upper operating bound:** 10M entries marks the infeasibility threshold on reference hardware — full verification at this scale is not practical inside the 24-hour cadence.

Projects approaching or exceeding 10M entries require a sampled-verification strategy. The sampled-verification design (coverage guarantee, sampling distribution, integration with the C-GTO-2 pairing-check) is flagged for v2 (GAP-59). In v1.2, operators whose projects approach 10M entries must either rotate to a fresh epoch (via project close + re-initiation) or adjust the verification cadence (operational policy; not a spec-enforced knob).

### 16.5 Tiered Read-Access Model (closes OQ-S7, OQ-SL3)

- **Orchestrator:** direct read access.
- **Humans:** mediated access via Orchestrator-provided query API. Filtering by entry type, timestamp, audit category, correlation ID.
- **Agents:** restricted to entries where `agent_id` matches their own identity. Cross-agent audit visibility requires human-level access.
- **Filesystem-level access:** restricted to Orchestrator, Boot-verifier, and Retention Manager. Enforced via filesystem permissions.

### 16.6 Audit Category Tags

Every entry carries an `audit_category` field. Initial enumeration:
- `SECURITY` — Gate interactions, token events, integrity violations.
- `CONSISTENCY` — 2PC phases, rollback, chain events.
- `VALIDATION` — Meta-Validator, Meta-TGA, Reflexion outcomes.
- `GOVERNANCE` — Config updates, sealed corpus events, reviewer decisions.
- `LIFECYCLE` — Locks, holds, scheduling, archival, project lifecycle.

Tags enable query-based views without requiring separate stores. Enumeration is extensible.

### 16.7 Ledger Epoch Archival and Retention Policy Interface (T11, D89)

Ledger entries older than the most recent `ANCHOR_ESTABLISHED` event are eligible for cold-storage archival at `<harness_root>/.state-ledger/archive/{epoch_bundle_N}/`. Parallels T9 compaction-epoch bundling.

**Retention policy (IC-LDG-RETAIN):**
Retention policy is declared at bootstrap via `PROJECT_INITIATED` (LIFECYCLE, W2 bootstrap writer, immutable post-mint). Default if not specified: PROJECT_LIFETIME. Retention is immutable-downward (C-SL2): once configured, it MUST NOT be shortened. Extensions (longer retention) are permitted via `RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE, signed ceremony). The Ledger layer blocks any shortening attempt regardless of operator key validity.

**Unconditional invariant:** Epochs containing any `INTEGRITY_VIOLATION` entry are retained INDEFINITELY, regardless of configured retention policy and regardless of any operator override attempt.

**Project close:** `PROJECT_CLOSED` (LIFECYCLE, signed ceremony) seals the final epoch and makes the Ledger read-only. Archival format: gzip bundles with operator-signed SHA-256 manifest, format version `"1.0"`. `PROJECT_CLOSED` is write-final — Ledger is read-only even if archival is pending (cold storage unavailable). Archival retried with exponential backoff when storage becomes available.

Archival preserves full entry content, Merkle linkage, and integrity hash manifest. Archived epochs are verifiable; on-demand restore is supported for forensic investigation.

### 16.8 Complete Ledger Entry Type Catalog

See Appendix C. The v1.2 catalog includes all v1.1 entry types plus 50+ additions from GS1–GS13 (new ceremony-related, bootstrap, burst-state, break-glass, scope-mismatch aggregate, external-provenance, retention, hook-integrity, Q5 weak-check, and corpus-expiry types). Two v1.1 entry types are marked deprecated per A7b: `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` — both subsumed by the unified CeremonyToken model (§20 / IC-SCOPE-AUTH-1).

## 17. Concurrency Control — Lock vs. Hold (T8)

### 17.1 Separation of Concerns

The original scope lock (D59/D60) was conflating three concerns. The lock/hold split cleanly separates them:

| Concern | Mechanism | TTL | Purpose |
|---|---|---|---|
| Concurrent write prevention | Write Lock | 60 min | Throughput / sequencing |
| Dependency preservation | Dependency Hold | 72 hr renewable | Correctness across escalation |
| Pruning exclusion | Dependency Hold (subset) | 72 hr renewable | Prevent GC of in-use edges |

### 17.2 Write Lock — Unchanged D59/D60

- Acquired at task declaration.
- 60-minute TTL, auto-release.
- Blocks *other agents* from writing to region.
- Scope: the declared write region.
- Conflicts resolved at assignment, not commit (C-CW4).

### 17.3 Dependency Hold — New (T8)

- Placed on specific edges the task is *reading*.
- 72-hour TTL, renewable on escalation events (Peer Agent review, Human Queue residency).
- Blocks *Pruning operations only*.
- Does not block other Write Locks or overwrites by other agents.
- Released on task completion, abort, or TTL expiry.
- PREPARED-state timeout does NOT automatically release the Hold (D85). Hold persists until successful commit on retry or operator-signed Hold release (GOVERNANCE category, signed ceremony).

### 17.4 Task Resume Re-Verification

On escalated task resumption:
1. Orchestrator reads current state of held edges.
2. Compares against escalation-entry snapshot.
3. **Unchanged:** task resumes with original context.
4. **Changed:** `context_stale` — task repackaged with current state, reassigned fresh.
5. **Hold expired:** `context_lost` — may require `dependency_reconstruction_required` escalation.

### 17.5 Interaction with 24-Hour Pruning Floor

Stratified rule:
- Edge age < 24 hours: never prunable (D56 floor).
- Edge age ≥ 24 hours AND under active Dependency Hold: not prunable while held.
- Edge age ≥ 24 hours AND no active holds: prunable per normal D54–D57.

### 17.6 Pruning Pre-Check

Before patch submission, Pruning Agent queries Orchestrator for Hold state on target edges (IC-PA7). Held edges excluded. If exclusion drops patch below meaningful size, Pruning logs deferral and reschedules. Excluded edges accumulate in `stale_urgent` count but flagged `held_not_prunable`.

---

═══════════════════════════════════════════════════
# PART V — OPEN QUESTIONS AND v2 ROADMAP
═══════════════════════════════════════════════════

## 18. Remaining Open Questions

### 18.1 Empirical / Post-Deployment Tuning

- **OQ-W1** — Cumulative edit volume degradation threshold (model-specific). All drift numbers (1,500 / 8,000 / 2,000 sub-batch) are provisional. The drift state interface shape is specced (IC-WE-1, D83); threshold values remain OQ-W1. Blocks OQ-OC3 calibration. Superset of GAP-1.
- **OQ-W2** — MEMIT/target model architecture compatibility verification.
- **OQ-W8** — Behavioral probe generalization beyond code domains. **PARTIALLY CLOSED** by §21 (L2 Probe Family — three sub-types, Semantic Assertion Criterion, three judgment methods, TGA authorship; GAP-9 / v2 GS10). Residual: threshold calibration per probe sub-type.
- **OQ-W-CALIB-1** — Numeric ε outputs of the `larql_fidelity_calibration` protocol (§22). Protocol structure is ratified (D-GS8-A); per-transform-class ε values, bucket boundaries for non-default BUCKET transforms, and derived M thresholds are implementation-phase. GAP-1, GAP-2, GAP-48 all roll up here.
- **OQ-W-PROBE-VERSION** — Probe set versioning for ε calibration. Probe-set evolution across Genesis updates is unspecified; if the probe set changes, historical ε values lose comparability (GAP-48 — GS13 scope).
- **OQ-V-JUDGE-THRESHOLD** — Threshold calibration for `judgment_method: judge_model_classification` in §21 probes — per-probe, per-domain, or global default (GAP-9 residual).
- **OQ-V-SELF-REF** — Self-referential probing: handling probes whose judge model is itself subject to `.vindex` writes (GAP-49 — GS13 scope).
- **OQ-OC3** — Compaction verification sampling calibration (failure report format and abort thresholds specced by D86, IC-OC-PROBE; sampling rates for SUPPORTING and INCIDENTAL tiers remain provisional pending OQ-W1 resolution).
- **OQ-CAKB-BURST** — Per-CAK burst-limit empirical validation. N=5 / 10-min is provisional; legitimate Genesis sequences under rapid-recovery debugging may exceed this (GAP-56 — GS13 scope; pre-ship modeling required).
- **T5 / T11** thresholds — async WAL flush cadence, verification intervals, backlog thresholds — starting heuristics.

### 18.2 Operational Policy

- **OQ-S5** — Minimum viable Genesis security for fully automated pipelines (v1 requires human review; full automation is v2 or operator policy).
- **OQ-S8** — Notification channels for integrity violations (email, Slack, logging — not spec).
- **OQ-V1** — Constitutional test failures as Tier 3 classification (policy). Mechanism (constitutional suite in Tier 2 sealed corpus) is specced; runtime tagging and promotion ceremony are not. **PARTIALLY CLOSED** by §25 (Q5 Weak-Check `CONSTITUTIONAL_FAILURE` with invariant_statement + failure_assertion_message field pair, A14).
- **OQ-V5** — PARTIALLY CLOSED by D88 (IC-CORPUS-AUTH), §24 expiry enforcement, and the `corpus-author-registry/` Tier 2 sealed corpus (GAP-8). Corpus extension cadence and authorship rotation policy remain operator-owned.
- **OQ-SC2** — Layer 4 recovery when originating external document unavailable. **PARTIALLY CLOSED** by §26 external document provenance (mandatory provenance block, advisory staleness, external_source_audit, IC-EXT-PROV1/2). Residual: stale-fact reconciliation workflow (OQ-SC3).
- **OQ-SC3** — Stale Layer 4 fact reconciliation workflow. Open; implementation-time decision per GS13 disposition.
- **OQ-W6** — PARTIALLY CLOSED at Gate enforcement layer (D81, D82, IC-GATE-8). Gate version pre-check (#8) and compaction versioned parser are specced. Remaining deferred to v2: migration path authorship, deprecation ceremony for old versions, multi-version team deployment.
- **OQ-CFG-TIER** — Tier placement conflict for rate-limit parameters participating in boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation. GAP-27 placed `scope_update_min_interval_seconds` at Tier 3; whether boot-participating parameters should migrate to Tier 1 is deferred (GS13 disposition).

### 18.3 Deferred to v2

- **OQ-CW1** — Voluntary scope-lock / Write Lock release and inter-agent negotiation (GAP-17).
- **OQ-SL2** — Multi-machine harness Ledger replication (GAP-18).
- **OQ-W6 (residual)** — `.larql` schema version migration path authorship, deprecation ceremony, multi-version team deployment.
- **OQ-GENESIS-AUTO** — Genesis automation (secondary LLM reviewer as human-review proxy) (GAP-13).
- **OQ-KEY-ROTATION** — OOK and CAK key rotation ceremonies with full dependency map (GAP-19). CAK rotation is a v2 deliverable; §23.3 break-glass is the v1.2 emergency substitute.
- **OQ-S-CAK-2** — T15 m-of-n CAK availability path (T15 v2; GAP-42 break-glass partially addresses OQ-S-CAK-1 in v1.2).
- **OQ-BATCH-HOLD** — T16 batch Genesis Hold release and multi-Hold ceremony scoping. Per-Hold model is the v1.2 path.
- **OQ-RATE-POLICY-EVOL** — Further scope-update rate-limit policy evolution beyond GAP-27 resolution (GAP-32).
- **OQ-SAMPLED-VERIFY** — Sampled-verification design for Ledger chains exceeding 10M entries (GAP-59; per GAP-53 documentation threshold).
- **OQ-RETIRED-KEY-META** — Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60).
- **OQ-AGG-CONVENTION** — Formal framework convention for aggregate-detection entry types (always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item) (GAP-55; post-v1 integration pass).
- **OQ-PATH-DEPLOY** — Path-conditional deployment architecture for GAP-4 Path A/B/C, accounting for GAP-56 burst-limit density, GAP-57 per-operator binary, GAP-58 state-machine completeness per path. Activates on operator path selection.
- **OQ-TGA-SPLIT** — T-TGA-load v2-reconsider: TGA split into TGA-Test / TGA-Probe if v1.2 operation surfaces concrete failure-mode evidence.
- **OQ-DRS-CAS** — Content-addressed immutable storage for `.dry-run-store/` (T-S-RP-1 v2-flag; replaces metadata-only Warden audit with content-level immutability).

### 18.4 Closed in Integration

Closed during Session 7 synthesis (v1.0 → v1.1):
- **OQ-W5** — `attention_weight` authority (T1: two-number split model).
- **OQ-V2** — Retry budget reset per subtask (D73: fresh per subtask, aggregate cap preserved).
- **OQ-V3** — TGA test validation (T2: four-layer cascade).
- **OQ-S1** — Prompt injection ownership (D38: two-layer sequential).
- **OQ-S2** — Token revocation (T5: agent-suspension-flag model).
- **OQ-S3** — Validator write authority (D39: no authority, Commit Executor pattern).
- **OQ-S6** — Genesis seal storage (D49: dual-store).
- **OQ-S7** — Audit queryability (T11: tiered read-access).
- **OQ-SL3** — Agent ledger access (T11: restricted to own-identity).
- **OQ-TC2** — Infrastructure failures vs. retry budget (D67: independent).
- **OQ-TC3** — Consistency status exposure (D75: Orchestrator-mediated API).
- **OQ-GOC1** — Path classification storage (D76: Tier 3 Anchored Git Config).
- **OQ-CW2** — Lock visibility (D78: Orchestrator-mediated only).
- **OQ-OC1** — Idle-window detection (D79: Orchestrator-internal heuristic).
- **OQ-TPC2** — Human abort authority (D74: compensation path, no process-kill).
- **OQ-W10** — Compaction strategy (D62: full MEMIT re-run mandated).

Closed during IC Review Session (v1.1):
- **OQ-TC1** — Circuit breaker reset authority (D84: signed ceremony with independent TC precondition verification; IC-TC-RESET). READ_ONLY automatic on trip; write resumption via ceremony only.
- **OQ-TPC1** — PREPARED-state timeout value (D85: two-value model — `incremental_prepared_timeout` default 2 hours; `genesis_prepared_timeout` no default, Gate-blocked if absent; IC-TC-TIMEOUT).
- **OQ-S4** — Scope version management across long-running projects (D87: mid-flight update model; `SCOPE_HASH_MISMATCH` error code defined; superseded by §20 CeremonyToken model).
- **OQ-SL1** — Full Ledger retention policy (D89: immutable-downward model; `PROJECT_CLOSED` ceremony; archival format versioned `"1.0"`; IC-LDG-RETAIN; extended by §27).

Closed during Phase 2 gap sessions (v1.1 → v1.2):
- **OQ-S-CAK-1** — CAK availability when primary CAK compromised — PARTIALLY CLOSED by §23.3 break-glass (GAP-42 / GS10). Residual m-of-n variant is OQ-S-CAK-2 (v2).
- **OQ-V9** — Validator nomination-time attestation for constitutional tests — CLOSED by GAP-39 / GS12 (nomination-time declarative attestation + dry-run sufficient for v1.2; IC-CLK-META, IC-CLK-SANDBOX, IC-NOM-DRYRUN).
- **T-S4-N1 / T-S7-N1** — Rotation registry ordering + rate-limit derived-vs-primary state — CLOSED by GAP-46 / GS11 (IC-CAK-IDENTITY, IC-BOOT-RLRF).
- **T-SC-W-2** — Write suspension vs. governance-ceremony write — CLOSED by GAP-37 / GS10 (IC-GCO-1).
- **T-PM-vs-PA** — Provenance Monitor vs. Pruning Agent advisory queue priority — CLOSED by GS11 merge policy (IC-REVIEW-QUEUE amended).
- **T-TGA-load** — TGA authority concentration — CLOSED (Accepted) by GS12; v2-reconsider flag set.

## 19. v2 Scope Targets

v2 is additive, not corrective. The v1.2 design does not prevent any v2 feature; it simply does not include them. All deferrals are anchored to a GAP or OQ identifier for traceability.

**Distributed trust:**
- Multi-machine harness with Ledger replication and distributed consensus (GAP-18).
- Cross-machine token federation.
- Multi-operator (quorum) Tier 2 signing.
- Remote attestation.

**Key lifecycle management:**
- OOK and CAK key rotation ceremonies with full dependency map (GAP-19). In v1.2 the §23.3 break-glass channel is the sole CAK-replacement mechanism.
- Operator signing key rotation and revocation (full PKI).
- Orchestrator key rotation.
- Cross-project key sharing policies.
- Delegation tokens for nested sub-agent invocations.
- CAK availability m-of-n path (OQ-S-CAK-2 / T15 v2).
- Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60).

**Agent-to-agent trust:**
- Peer agent review delegation token design (GAP-20 — authorization model for D37 Step 2 escalation second Coder Agent).

**Ceremony scope extensions:**
- Batch Genesis Hold release and multi-Hold ceremony scoping (T16).
- Voluntary Write Lock release and inter-agent negotiation (GAP-17, OQ-CW1).
- Further scope-update rate-limit policy evolution (GAP-32).

**Formal enforcement upgrades:**
- Pre-receive Git hooks (prevent-at-write for Tier 3).
- Stronger sandbox attestation.
- Hardware-backed key storage (TPM, HSM).

**Verification scale:**
- Sampled-verification design for Ledger chains exceeding 10M entries (GAP-59 / GAP-53).

**Validation architecture:**
- TGA split into TGA-Test / TGA-Probe (T-TGA-load v2-reconsider; activates only on v1.2 operational evidence).
- Self-referential probing: probes whose judge model is itself subject to `.vindex` writes (GAP-49).

**Archival extensions:**
- External cold-storage export for `.larql` and Ledger archives.
- Project-to-project trust transfer for shared sealed corpora.
- Content-addressed immutable storage for `.dry-run-store/` (T-S-RP-1 v2-flag).

**Automation extensions:**
- Genesis automation — secondary LLM reviewer as human-review proxy (OQ-S5 / GAP-13).

**Schema versioning extensions:**
- OQ-W6 residual — `.larql` schema version migration path authorship, deprecation ceremony, multi-version team deployment.

**Observability conventions:**
- Aggregate-detection entry type convention (GAP-55; post-v1 integration pass).

**Deployment architecture:**
- Path-conditional deployment for GAP-4 Path A (LangGraph), Path B (SDK), Path C (Hybrid), incorporating GAP-56 burst-limit density validation, GAP-57 per-operator binary distribution, GAP-58 state-machine completeness per path (OQ-PATH-DEPLOY).

---

═══════════════════════════════════════════════════
# PART VI — CROSS-CUTTING PROTOCOLS (v1.2 Additions)
═══════════════════════════════════════════════════

## 20. Ceremony Authorization — Unified CeremonyToken Model

### 20.1 Purpose

Every GOVERNANCE-class ceremony in the harness — manifest ratification, Dependency Hold release, scope update, circuit reset, schema extension, retention extension, project close, corpus manifest signing, and ceremony-key rotation — is authorized through a single umbrella Interface Contract: **IC-SCOPE-AUTH-1** (v2 GS4 — ratified; supersedes the v1.1 single-ceremony `IC-SCOPE-UPDATE` authorization model). The CeremonyToken envelope is the unified shape; specialized ICs delegate authorization to IC-SCOPE-AUTH-1 and specify only their ceremony-type-specific `ceremony_payload` bodies.

### 20.2 Root of Trust

The single root is the **Ceremony Authorization Key (CAK)** — public half anchored at `ceremony_authorization_key_anchor` in Tier 1 `genesis-seal.json` (A10, §13.2). The private half is operator-held, offline, HSM-preferred. The CAK is structurally distinct from the Orchestrator signing key (`ORCHESTRATOR_KEY_ANCHOR`) — no ceremony envelope with `key_ref == ORCHESTRATOR_KEY_ANCHOR` is ever accepted.

The break-glass anchor (`break_glass_key_anchor`, §23.3) is a second, distinct Tier 1 anchor authorized for one and only one ceremony type: `CAK_ROTATION_EMERGENCY`.

### 20.3 IC-SCOPE-AUTH-1 — Ceremony Authorization Interface Contract

**From:** Human operator (holder of CAK).
**To:** Every ceremony verifier in the harness — Gate (scope update), Transaction Controller (circuit reset), Hold Registry (Dependency Hold / Genesis Hold release), Migration Manifest Verifier, Schema Extension Ceremony handler, Retention Extension / Project Close handler, Corpus Manifest Verifier, Ceremony Key Rotation handler.

**Common envelope:**

```
{
  ceremony_type: "SCOPE_UPDATE" | "HOLD_RELEASE" | "MANIFEST_RATIFY"
               | "CIRCUIT_RESET" | "SCHEMA_EXTENSION"
               | "RETENTION_EXTEND" | "PROJECT_CLOSE"
               | "CORPUS_MANIFEST_SIGN" | "CEREMONY_KEY_ROTATION"
               | "CALIBRATION_RATIFICATION" | "RETENTION_PRUNING"
               | "CAK_ROTATION_EMERGENCY" | "CAK_BURST_CLEARED",
  ceremony_id:            UUID,
  ceremony_payload:       { ... },   // type-specific body, owned by the specialized IC
  operator_id:            <stable external id, GAP-46>,
  timestamp:              <ISO-8601, wall-clock>,
  operator_signature:     <signature over the canonical envelope bytes>,
  key_ref:                <MUST equal CEREMONY_KEY_ANCHOR>
}
```

**Verifier preconditions (uniform, non-delegable):**

1. `key_ref` MUST equal the current active `ceremony_authorization_key_anchor`.
2. `key_ref` MUST NOT equal `ORCHESTRATOR_KEY_ANCHOR`. Structural exclusion — checked before signature validation and before any ceremony-type-specific logic.
3. Signature valid against the public half at `key_ref`.
4. Timestamp within 60s of verifier's wall-clock (replay protection).
5. `key_ref` not in the revoked/rotated list (rotation-registry lookup; v1.2 rotation is via the break-glass `CAK_ROTATION_EMERGENCY` path only).
6. Ceremony-type-specific preconditions delegated to the specialized IC.

**Failure behaviors (SECURITY, synchronous, W1 — all escalate to Warden):**

| Condition | Emitted Entry |
|---|---|
| `key_ref == ORCHESTRATOR_KEY_ANCHOR` | `CEREMONY_AUTH_WRONG_KEY` (CRITICAL — Orchestrator attempted self-authorization) |
| Signature invalid | `CEREMONY_AUTH_SIGNATURE_INVALID` |
| Stale timestamp | `CEREMONY_AUTH_REPLAY_REJECTED` |
| `key_ref` in revoked list | `CEREMONY_AUTH_KEY_EXPIRED` |
| Unknown `key_ref` | `CEREMONY_AUTH_KEY_UNKNOWN` |
| Missing required envelope field | `CEREMONY_AUTH_MALFORMED` |

### 20.4 Specialized IC Delegation

All existing and future GOVERNANCE-class ICs delegate authorization to IC-SCOPE-AUTH-1 and specify only their `ceremony_payload` body and type-specific preconditions:

- **IC-TC-RESET** (A3 — §11.8.1): payload body for `CIRCUIT_RESET`; preconditions branch by trip reason.
- **IC-HOLD-RELEASE**: payload body `{ hold_id, hold_type, release_reason_code }`; preconditions include HELD-state verification by Hold Registry. Supersedes v1.1 `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` entries (both deprecated per A7b — they collapse into IC-SCOPE-AUTH-1's uniform failure set).
- **IC-SCOPE-UPDATE** (A5/A6/A9 — §10.9): payload body carries scope-hash predecessor and affected agent IDs; admission order includes rate-limit → envelope check → CAK verification → precondition checks.
- **IC-SCHEMA-EXTEND, IC-LDG-RETAIN (§27), IC-SL8**: delegate authorization; payload bodies per specialized IC.
- **Manifest ratification IC** (IC-MANIFEST-1, Check 8 from GAP-29a): delegates authorization; payload body carries manifest lattice completeness evidence.
- **CALIBRATION_RATIFICATION** (§22): payload body carries `epsilon_calibration_report` artifact.
- **RETENTION_PRUNING** (GAP-47 / GS10, IC-RP-1): payload body names the `artifact_retention_manager` role and retention-boundary operation.
- **CAK_ROTATION_EMERGENCY / CAK_BURST_CLEARED** (§23): payload bodies per §23.

### 20.5 Cross-Cutting Implications

IC-SCOPE-AUTH-1 changes the structure of every GOVERNANCE and SECURITY Ledger entry that previously carried a standalone `operator_signature` field. The envelope now wraps these: `operator_signature` appears as a nested field of the envelope, alongside `ceremony_type`, `ceremony_id`, and `key_ref`. Appendix C reflects the updated entry schemas.

### 20.6 Non-Goals

IC-SCOPE-AUTH-1 does not govern:
- Non-ceremony authentication (e.g., agent identity verification at invocation-time uses the Orchestrator signing key, not CAK).
- Automatic CAK rotation — v1.2 rotation is only via break-glass `CAK_ROTATION_EMERGENCY` (§23.3). Scheduled rotation is v2 (GAP-19).

---

## 21. L2 Probe Family and Semantic Assertion Criterion

### 21.1 Purpose

L2 behavioral probes (§8.9 — mandatory for `declared_importance ∈ {CORE, SUPPORTING}`) are generalized from the code-domain-only "generation test" of v1.1 into a domain-agnostic three-member probe family, each producing the same deterministic binary pass/fail outcome required by the Ledger schema (`write_outcome ∈ {success, behavior_fail}`). Source: GAP-9 / v2 GS10.

### 21.2 The Three Probe Sub-Types

**Generation probe** (code-domain edges, `function` / `module` entity types):
Prompt elicits code generation or completion; pass condition is execution-based (test harness returns green). This is the existing §8.9 behavior, preserved verbatim as one member of the family.

**Assertion probe** (non-code `domain_concept` edges asserting positive facts — legal constraints, architectural invariants, business rules stated affirmatively):
Prompt elicits a response in a context where the fact should fire; pass condition is that the response contains the target assertion, verified by one of the three judgment methods (§21.4).

**Constraint probe** (non-code edges asserting prohibitions or invariants — "X must not Y", "Z is required before W"):
Prompt presents an adversarial scenario that would violate the constraint; pass condition is that the response refuses, flags, or correctly applies the constraint.

All three sub-types share the same Ledger contract: binary outcome at probe evaluation time, `write_outcome ∈ {success, behavior_fail}`, storage-pass / behavior-fail never collapsed into success.

### 21.3 Probe Authorship Authority

Probe templates are authored by the **Test Generator Agent (TGA)** as a sub-class of test artifact. This preserves D32–D33 actor-critic independence without a new component and without an independence exemption. TGA's mandate extends:

- From the task specification, emit (i) executable tests for code artifacts, (ii) probe templates for non-code artifacts, (iii) both when a write crosses domains.
- The Coder Agent / Architect Agent writes the `.larql` patch without visibility into either tests or probes.

Option (b) — granting the writing agent an independence exemption — is rejected as puncturing the central invariant. Option (c) — a separate probe-template component — is rejected as requiring a justification TGA already satisfies. The T-TGA-load tension (TGA authority concentration) was Accepted for v1 (GS12) under this allocation.

### 21.4 Semantic Assertion Criterion

Given probe template:

```
P = (elicitation_prompt, target_assertion, judgment_method, threshold)
```

the probe passes iff the model's response to `elicitation_prompt`, evaluated by `judgment_method`, registers `target_assertion` at or above `threshold`. The three permitted judgment methods:

- **`exact_substring`** — target_assertion is a string; pass iff the response contains it (case-sensitive by default; case-insensitive if the template declares so).
- **`structured_field_match`** — target_assertion is a structured object (JSON); the response is parsed against an expected schema and field values; pass iff all required fields match.
- **`judge_model_classification`** — target_assertion is a natural-language specification of the expected content; a designated judge model classifies the response at a declared confidence threshold. Binary classifier output.

For `judge_model_classification`, the judge model, judge prompt, and threshold are part of the probe template and are **versioned and frozen at probe template commit**. A probe's judgment dependencies are immutable once committed — preventing silent drift in what "pass" means.

### 21.5 Spec Block — L2 Probe Family

**What it must do:** Provide a domain-general behavioral verification gate for edges with `declared_importance ∈ {CORE, SUPPORTING}`. Produce a deterministic binary outcome recorded as `write_outcome` in the Ledger.

**Hard constraints:**
- Every L2 probe has exactly three components: `elicitation_prompt`, `expected_behavior_predicate`, `judgment_method`.
- Probe outcome is binary; storage-pass / behavior-fail is a distinct Ledger state, never collapsed into success (preserves §8.9).
- Probe sub-type is declared in the probe template: `{generation | assertion | constraint}`.
- Judge-model dependencies (when `judgment_method = judge_model_classification`) are pinned to specific model versions and frozen at probe template commit.
- Probe templates are TGA-authored.

**Tradeoffs decided:**
- Binary rather than graded outcome — preserves Ledger schema and clean Reflexion-loop semantics; cost is loss of fine-grained confidence for borderline assertion probes.
- Judge-model classification permitted despite introducing a second model — without it, non-trivial non-code facts have no machine-checkable criterion. Mitigated by freezing judge-model and prompt at template commit.
- TGA-authored probes over a separate probe-template component — preserves D32–D33 without new machinery; T-TGA-load concentration Accepted.

**Open questions (deferred):**
- Threshold calibration for `judge_model_classification`: per-probe, per-domain, or global default (OQ-V-JUDGE-THRESHOLD; GAP-9 residual).
- Self-referential probing — handling probes whose judge model is itself subject to `.vindex` writes (OQ-V-SELF-REF; GAP-49 → GS13).

**Interface contract (probe template shape):**

```
probe_template := {
  probe_id,
  probe_sub_type       ∈ {generation, assertion, constraint},
  elicitation_prompt,
  expected_behavior_predicate,
  judgment_method      ∈ {exact_substring, structured_field_match,
                          judge_model_classification},
  judgment_config      (judge_model_id, judge_prompt, threshold — when applicable),
  authored_by          : tga_agent_id,
  template_hash
}
```

### 21.6 Non-Goals

§21 does not specify:
- The calibration of judge-model thresholds (OQ-V-JUDGE-THRESHOLD).
- Probe-template refactoring ceremonies (v2 — tied to TGA-split reconsideration).
- Probe outcomes for edges with `declared_importance = INCIDENTAL` — these are not L2-probed.

---

## 22. `larql_fidelity_calibration` Protocol

### 22.1 Purpose

Several T13 thresholds and IC-MANIFEST-1 bucket-map boundaries depend on a per-transform-class fidelity coefficient ε that cannot be set a priori. The `larql_fidelity_calibration` protocol (D-GS8-A, v2 GS8) defines the measurement procedure that produces an `epsilon_calibration_report` artifact consumable by the genesis-seal update ceremony. Protocol structure is ratified; numeric ε outputs are implementation-phase per OQ-W1 / OQ-W-CALIB-1 / GAP-1 / GAP-2 / GAP-48.

### 22.2 Preconditions

- At least one full `current_larql_version` increment has occurred, producing a non-empty migration manifest with at least one RENAME, one BUCKET, and one COMPUTE transform type populated.
- A reference patch corpus representative of production agent output exists (minimum 200 patches per transform class per version hop measured).

### 22.3 Procedure (per transform class, per version hop)

1. Select reference patches at `source_version`. Compile through MEMIT to produce baseline parametric encoding; record per-patch retrieval fidelity via canonical probe set (probe set defined at Genesis; versioning per OQ-W-PROBE-VERSION / GAP-48).
2. Apply migration manifest translation to the same reference patches. Compile the translated patches through MEMIT. Record per-patch retrieval fidelity via the same probe set.
3. Compute per-patch fidelity delta. Aggregate mean, p50, p95, p99 across the class-hop combination.
4. The class-hop ε value = p95 of fidelity delta. (p95 chosen over mean to bound worst-case compaction batches.)

### 22.4 Output Artifact — `epsilon_calibration_report`

Required fields:
- Per transform class (RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT): per-hop ε values.
- Corpus statistics (patch count per class-hop).
- `calibrated_against_probe_set_version` field — records the canonical probe-set version the calibration was run against (D-GS8-A / GAP-48 resolution). Historical ε values are comparable only within a single probe-set-version epoch.
- Compaction tolerance assumption used for M derivation (provisional default: `Δfidelity_max = 0.05`; ratified at calibration time).
- Timestamp and signing CAK.

### 22.5 Ratification Path

The calibration artifact is submitted via a `CALIBRATION_RATIFICATION` ceremony (ceremony_type per §20 / IC-SCOPE-AUTH-1). On acceptance, Tier 1 `genesis-seal.json` fields `larql_epsilon_table`, `compaction_tolerance`, and derived M values are populated, and the provisional flags on T13 thresholds and IC-MANIFEST-1 `bucket_map` are cleared in the spec's next integrated iteration.

### 22.6 Bucket Boundary Determination (D-GS8-B)

Bucket boundaries for any BUCKET transform class are calibrated by the same protocol, producing a per-transform-class optimal boundary table rather than a fixed global default. The GS7 illustrative values (0.33 / 0.66) are retained as provisional illustrative defaults for the `attention_weight → declared_importance` bucket only; other BUCKET transforms ratify their own boundaries at calibration time.

### 22.7 Interface Contract Delta

`IC-MANIFEST-1` `bucket_map` field description:
- Boundaries remain PROVISIONAL until a `CALIBRATION_RATIFICATION` ceremony is accepted for the transform class the bucket serves.
- Manifest entries authored prior to first calibration carry `calibration_state: UNCALIBRATED` and flag accordingly in dry-run reports (non-blocking; advisory only until first calibration lands).

### 22.8 Non-Goals

§22 does not specify:
- Numeric ε values, M values, or bucket boundaries — implementation-phase per OQ-W-CALIB-1.
- Automated re-calibration triggers — operator-owned cadence.
- Cross-model ε transfer — a calibration is per-deployment, not portable.

---

## 23. CAK Bootstrap, Burst Limit, and Break-Glass

### 23.1 CAK Bootstrap Tool (GAP-40 / GS10 — IC-BOOT-1)

**Purpose:** A pre-harness operator tool that mint-once writes `ceremony_authorization_key_anchor` (and `break_glass_key_anchor`, §23.3) into `genesis-seal.json`, establishing the CAK trust-chain root before the harness starts. The harness cannot produce this artifact (circular trust); the tool is the trust-chain seed.

**Hard constraints:**

- **C-BOOT-1 (Identity Separation):** Tool runs under operator credentials in a process identity distinct from any harness-owned identity. No shared filesystem user, group, or capability set with harness runtime.
- **C-BOOT-2 (Input):** Accepts operator-generated public key material (CAK public half, break-glass public half) from an operator-controlled HSM or key ceremony. Private halves never enter tool memory.
- **C-BOOT-3 (Atomic Write):** `genesis-seal.json` written via temp-file + fsync + rename, followed by post-write SHA-256 verification. Mismatch aborts boot preparation.
- **C-BOOT-4 (Boot Manifest):** Tool emits signed `boot_manifest.json` containing `genesis_seal_hash`, `operator_root_signature`, `tool_version`, `tool_binary_hash`, `timestamp`. Signed with operator root key (offline, out-of-band).
- **C-BOOT-5 (First-Boot Verification):** At first boot, harness verifies `boot_manifest` signature against a **compile-time-embedded** `operator_root_public_key`, verifies `genesis_seal_hash` matches actual file SHA-256, verifies `tool_binary_hash` against independently published release hash. Any mismatch refuses boot with `GENESIS_SEAL_UNVERIFIED` (SECURITY, via W3 boot-verifier path).
- **C-BOOT-6 (Distribution):** Distributed as a signed release artifact alongside the harness but from a **distinct signing authority chain** (operator root, not harness release key). Two independent trust roots converging at first boot.
- **C-BOOT-7 (Re-use Prohibition):** Tool refuses to overwrite an existing `genesis-seal.json`. Re-mint requires explicit operator teardown of the prior harness instance.

**Tradeoffs decided:**
- **Dual-root signing model** accepted — reduces single-vendor compromise risk at cost of operator setup complexity.
- **Per-operator harness binary** via compile-time-embedded operator root public key — harness binary is not a universal artifact. Accepted as the price of closing the bootstrap-trust gap. Implications for release / reproducible builds are GAP-57 (GS13 scope, OQ-PATH-DEPLOY).
- **Mint-once** — rejected automated re-mint paths as reintroducing the circular-trust problem.

**Open questions (deferred):**
- Operator key-ceremony internal spec — operator-domain policy, out of scope for v1 harness spec.
- Tool upgrade path on operator root rotation — v2.

**Interface contract:** **IC-BOOT-1** — as specified. Resolves T-S4-N2 (bootstrap-tool trust asymmetry).

### 23.2 Per-CAK Ceremony Burst Limit (GAP-41 / GS10 — IC-CAKB-1)

**Purpose:** Cap rapid ceremony issuance from a single CAK identity to bound blast radius of a briefly-exposed CAK before operator detection and rotation.

**Hard constraints:**
- **C-CAKB-1 (Window):** 10 minutes, rolling per CAK fingerprint.
- **C-CAKB-2 (Limit):** 5 ceremonies of any type per CAK per 10-minute window.
- **C-CAKB-3 (Breach Behavior):** 6th ceremony REJECTED (not delayed). Emits `CAK_CEREMONY_BURST_EXCEEDED` (SECURITY, synchronous, W1). Payload: `cak_fingerprint`, `ceremony_count_in_window`, `window_start`, `rejected_ceremony_type`.
- **C-CAKB-4 (Effect):** Breach places the CAK into `BURST_SUSPENDED` state — no further ceremonies accepted for 60 minutes OR until an explicit `CAK_BURST_CLEARED` ceremony signed by a **different** CAK with Tier 1 authority.
- **C-CAKB-5 (Orthogonality):** Independent of per-ceremony-type limits (GAP-27) and `CIRCUIT_RESET_REJECTED` rate limit (GAP-36, IC-CRR-1). Burst check applies first; if burst exceeded, per-type limit is not consulted.
- **C-CAKB-6 (Break-Glass Exemption):** Break-glass CAK is exempt — its use is already out-of-band quorum-gated (§23.3).
- **C-CAKB-7 (Interaction with Circuit Trip):** A harness in `BURST_SUSPENDED` rejects IC-TC-RESET ceremonies with `CIRCUIT_RESET_REJECTED_BURST_STATE` until burst window clears (GAP-58 resolution, §11.8).

**Tradeoffs decided:**
- **Rejection over delay** — delay creates a timing side-channel and complicates state.
- **60-minute auto-clear with explicit-clear path** — operator detection window with legitimate-burst escape hatch.
- **SECURITY category** — burst is attacker-characteristic; false-positive cost (operator re-clear) is low.
- **N=5, M=10min** — permits legitimate concurrent Genesis orchestration while flagging attack-rate usage. Subject to empirical validation per GAP-56 (OQ-CAKB-BURST).

**Open questions (deferred):**
- Worst-case legitimate Genesis-sequence modeling (GAP-56 / GS13).
- Per-CAK window persistence across harness restart — provisionally in-memory; revisit.

**Interface contract:** **IC-CAKB-1** — as specified. Layers with GAP-27 (per-ceremony rate limit) and GAP-38 (aggregate SCOPE_HASH_MISMATCH).

### 23.3 Break-Glass Emergency Channel (GAP-42 / GS10 — IC-BG-1)

**Purpose:** A last-resort recovery path when the primary CAK is declared compromised (`CAK_COMPROMISE_DECLARED`) and normal ceremony issuance is blocked. Must not itself become a parallel compromise vector.

**Hard constraints:**

- **C-BG-1 (Anchor):** Second Tier 1 key anchor `break_glass_key_anchor` written into `genesis-seal.json` at first-boot by the CAK bootstrap tool (extends IC-BOOT-1 scope by one field). Public half only; private half held offline under operator quorum.
- **C-BG-2 (Activation Prerequisite):** Break-glass use requires BOTH (a) a prior `CAK_COMPROMISE_DECLARED` Ledger entry AND (b) a quorum-signed `BREAK_GLASS_ACTIVATION` ceremony — M-of-N operator signatures, **M ≥ 3**, N operator-defined at bootstrap.
- **C-BG-3 (Single-Purpose Envelope):** Break-glass key can ONLY sign entries of ceremony_type `CAK_ROTATION_EMERGENCY`, which replaces the primary CAK anchor with a new operator-provided public key. No general-purpose ceremonies.
- **C-BG-4 (Out-of-Band Injection):** `BREAK_GLASS_ACTIVATION` injected via a dedicated out-of-band path requiring **physical operator access** to the harness host (not over network APIs). Prevents remote exploitation even if break-glass private material is exposed. See Appendix A deployment preconditions.
- **C-BG-5 (Parallel-Compromise Prevention):**
  - Separate HSM from primary CAK (distinct vendor if operator policy permits).
  - M-of-N across distinct operator identities (no single-human access to M signatures).
  - Physical-access requirement (C-BG-4).
  - Emits `BREAK_GLASS_ACTIVATED` (SECURITY, sync, dedicated W1 path, not W3) — alerts regardless of CAK state.
- **C-BG-6 (Post-Activation):** After successful `CAK_ROTATION_EMERGENCY`, break-glass key remains active; operator SHOULD rotate it via a second break-glass ceremony at convenience. New primary CAK resumes normal ceremony authority immediately.
- **C-BG-7 (No Freeze Bypass / TRUST_ROOT_LOST):** If break-glass itself is compromised (detected via anomalous `BREAK_GLASS_ACTIVATION` attempt), harness enters `TRUST_ROOT_LOST` terminal state — both CAK and break-glass blocked. Recovery requires full Genesis re-initialization. **No v1.2 third-tier recovery.**

**Tradeoffs decided:**
- **Single-purpose key** (rotation only) — minimizes blast radius if break-glass itself is compromised.
- **Physical-access requirement** — highest friction; break-glass is definitionally rare, friction acceptable. Creates T-W-BG-1 (Accepted design tradeoff, GS10).
- **M ≥ 3 floor** — single-operator break-glass compromise cannot activate it alone.
- **TRUST_ROOT_LOST as terminal** — no third-tier recovery avoids infinite regress of trust anchors; Genesis re-init is the recovery plan for double compromise.

**Open questions (deferred):**
- Exact M, N defaults — operator-configurable at bootstrap; M ≥ 3 hard floor only.
- Whether `CAK_ROTATION_EMERGENCY` re-triggers reconciliation to verify post-rotation state integrity — lean yes (see GS11 residual).

**Interface contract:** **IC-BG-1** — as specified. Partially closes OQ-S-CAK-1 (GAP-19 v2 residual). Extends IC-BOOT-1 by adding `break_glass_key_anchor` to `genesis-seal.json` schema. The m-of-n availability variant (OQ-S-CAK-2 / T15 v2) is not addressed in v1.2.

### 23.4 Non-Goals

§23 does not specify:
- CAK scheduled rotation (GAP-19 / v2).
- Operator-internal key ceremony procedures (operator policy).
- Custodian pre-arrangement workflow (Appendix A deployment precondition; T-W-BG-1 accepted friction).

---

## 24. Corpus Author Registry Expiry Enforcement

### 24.1 Purpose

The `corpus-author-registry/` Tier 2 sealed corpus (§13.3; GAP-8) admits an optional `expires_at` field per author record. §24 specifies where expiry is checked, how it is enforced, and what happens to Meta-* runs whose corpus still contains cases authored by an expired identity. Source: GAP-8 residual + v2 GS9 D99.

### 24.2 Two-Point Enforcement Model

Expiry is enforced at two discrete surfaces. Mid-run revocation is explicitly **not** performed — a Meta-* run that begins before a key's expiry crosses completes in an advisory posture rather than being aborted.

**Point 1 — Corpus case submission ingress (Warden-owned, A12-IC-CORPUS-AUTH).**
When an author submits a new corpus case, the Warden verifies that the submitting identity's `expires_at` is either absent or strictly greater than `now()`. An expired identity cannot submit. This is the authoritative enforcement surface for future-case admission. Rejection emits `CORPUS_WRITE_REJECTED` with reason `AUTHOR_EXPIRED`.

**Point 2 — IC-SL7 Meta-* token issuance (A13-IC-SL7).**
When the Transaction Controller requests an IC-SL7 corpus-access token for a scheduled Meta-* run, the Corpus Seal Registry verifies that every author whose cases are in the active corpus version either has no `expires_at` or has not yet crossed it. If any author has expired *and* their cases remain in the active corpus version:

- The IC-SL7 token is still issued (no run abortion).
- The IC-SL7 response carries a `contains_expired_author_cases: true` field.
- The Meta-* run completes in advisory posture; the Ledger result record carries an `EXPIRED_AUTHOR_PRESENT` advisory flag alongside the Health Score.

No new Ledger entry type is introduced for the advisory signal — it is an additive flag on the existing Meta-* result record.

### 24.3 Spec Block — Corpus Author Registry Expiry

**What it must enforce:** Expired corpus author identities cannot submit new cases. Runs whose existing corpus contains expired-author cases complete with an advisory flag rather than being revoked.

**Hard constraints:**
- **C-CORPUS-EXP1:** Expired author identity MUST NOT be accepted at corpus case submission ingress (Point 1).
- **C-CORPUS-EXP2:** Meta-* runs encountering expired-author cases in the active corpus version MUST complete with the `EXPIRED_AUTHOR_PRESENT` flag and MUST NOT be revoked mid-run (Point 2).

**Tradeoffs decided:**
- Advisory-only at Point 2 over mid-run abort — consistent with the harness pattern that Meta-* integrity is operator-observed, not operator-blocking.
- Two-point enforcement over single-point — Point 1 alone would leave previously-admitted cases unobserved; Point 2 alone would admit new cases from expired authors.

**Open questions (deferred):**
- Corpus version cadence for removing cases authored by expired identities — operator policy, parallel to general corpus extension cadence (OQ-V5 residual).

**Interface contract amendments:**
- **A12-IC-CORPUS-AUTH** — `expires_at` predicate added at submission ingress.
- **A13-IC-SL7** — `contains_expired_author_cases` response field + `EXPIRED_AUTHOR_PRESENT` advisory flag propagation.

### 24.4 Non-Goals

§24 does not specify:
- Expiry notification / pre-expiry warning mechanisms (operator-owned alerting).
- Automatic case-removal ceremonies when an author expires (operator discretion via normal corpus versioning).

---

## 25. Q5 Weak-Check / Constitutional-Failure Invariant

### 25.1 Purpose

Qualification criterion Q5 for constitutional-test promotion (GAP-10; v2 GS8 D97) requires that failures of constitutional tests map to a claimed `invariant_statement` field on the test metadata. Structural verification of natural-language assertion messages against such a claim is brittle as a blocking gate — too-strict parsers reject legitimate failures; too-lenient parsers provide no signal. §25 specifies the **weak-check pattern**: Ledger-logged co-record, no runtime block. Source: v2 GS9 D100; amendment A14.

### 25.2 The Weak-Check Pattern

When a constitutional test fails, the Validator emits a `CONSTITUTIONAL_FAILURE` Ledger entry (pre-existing in Appendix C per A7b) with a **new field pair** (A14):

- **`invariant_statement`** — copied from the test's metadata (authoritative source).
- **`failure_assertion_message`** — captured verbatim from the test's runtime output.

The Validator does **not** compare these two fields at runtime. The entry is a co-record: both fields are present in the Ledger, available for operator audit query. Divergence between the two is a signal the operator chooses to surface — not a runtime block.

This preserves the central invariant of the validation architecture (no runtime-gated natural-language parsing) while providing the data substrate for a future promotion to blocking-gate classification if the operational signal is ever deemed sufficient.

### 25.3 Spec Block — Constitutional-Failure Invariant

**What it must record:** Every constitutional-test failure produces a Ledger entry whose content includes both the test-metadata invariant claim and the runtime failure message, side-by-side.

**Hard constraints:**
- **C-CONSTITUTIONAL-Q5:** `CONSTITUTIONAL_FAILURE` Ledger entry MUST include both `invariant_statement` (from test metadata) and `failure_assertion_message` (captured verbatim from runtime). Neither field is optional; a write attempting to emit one without the other is rejected by the Validator as an implementation bug.
- No runtime comparison of the two fields is performed by any automated path. Comparison is an operator-initiated audit query.
- The two fields carry separate integrity guarantees: `invariant_statement` is a deterministic copy of test metadata at the time of the failing test run; `failure_assertion_message` is the verbatim runtime output from the test harness.

**Tradeoffs decided:**
- Weak-check pattern over blocking-gate check — preserves Reflexion-loop semantics and avoids brittleness.
- Same Ledger entry type (`CONSTITUTIONAL_FAILURE`) as a field pair, over introducing a new entry type — minimal surface change; entry type already exists.

**Open questions (deferred):**
- **OQ-V10** — Whether the spec should mandate a minimum operator audit-query suite (distinct from the constitutional test suite) to surface Q5 divergences. The weak-check pattern presumes operator tooling; if no query ever runs, Q5 degradation is logged but never observed. Low priority; v2 scope.

**Interface contract amendment:**
- **A14-Appendix-C-CONSTITUTIONAL_FAILURE** — field pair added to the entry type schema.

### 25.4 Non-Goals

§25 does not specify:
- Operator audit-query tooling (OQ-V10; operator-owned).
- Promotion of the weak-check to a blocking gate — the field pair is the substrate if future analysis warrants promotion, but the promotion itself is out of scope for v1.2.

---

## 26. External Document Provenance for Layer 4 Facts

### 26.1 Purpose

Layer 4 facts sourced from external documents (documentation sites, standards bodies, API references) require a provenance record binding the fact to a hash-pinned snapshot of its source at write time. §26 specifies the mandatory provenance block, the three-state staleness model, and the `external_source_audit` sub-routine on the Pruning Agent. Source: GAP-11 / v3 GS9 D101/D102.

### 26.2 Mandatory Provenance Block

Every Layer 4 fact written from an external source carries an `external_provenance` block in its patch metadata. Absence of this block for a Layer 4 external fact is a compile-time rejection: the Write Engine emits `LAYER4_MISSING_PROVENANCE` (UNRECOVERABLE at patch level; C-EXT-PROV1).

**Provenance block fields:**

| Field | Type | Required | Purpose |
|---|---|---|---|
| `source_uri` | URI | yes | Canonical location of the external document. |
| `source_hash_at_write` | hex (SHA-256) | yes | Hash of document content at write time. |
| `source_fetch_timestamp` | ISO-8601 UTC | yes | When the content was fetched. |
| `content_length_bytes` | integer | yes | Detects truncation vs. change later. |
| `etag` | string | optional | Populated if server returned one. |
| `archive_uri` | string (URI) | optional | Best-effort archive.org / IPFS pin. |
| `refetch_policy` | enum | yes | `pruning_cadence` \| `hourly` \| `never`. |

On patch commit, an `EXTERNAL_PROVENANCE_RECORDED` Ledger entry (CONSISTENCY, async) is emitted, replicating the patch metadata plus `patch_id`, `fact_triple_hash`, `ledger_seq`. The Ledger entry is the audit anchor; the patch metadata is the operational record consulted by the monitoring path.

### 26.3 Three-State Staleness Model — Advisory Only

Staleness is **advisory at detection time**, never blocking. The harness does not block writes or queries on external staleness (C-EXT-PROV2).

| State | Meaning | Ledger entry |
|---|---|---|
| `FRESH` | Last refetch hash matches `source_hash_at_write` | none (silent success) |
| `STALE` | Source reachable, hash differs from `source_hash_at_write` | `EXTERNAL_PROVENANCE_STALE` (async) |
| `UNAVAILABLE` | Source unreachable (404, DNS fail, timeout) | `EXTERNAL_PROVENANCE_UNAVAILABLE` (async) |

Both non-FRESH states emit CONSISTENCY-category entries and mark the underlying fact with an advisory `provenance_flag ∈ {STALE, UNAVAILABLE}` visible in query results. CORE-importance facts sourced externally additionally raise a `REQUIRES_HUMAN_REVIEW` signal on first detection, matching the pattern used by out-of-band Git reconciliation (§11.13) and merged through the Reconciliation Review Queue (§15.1, T-PM-vs-PA policy).

Rationale: Network flaps and benign upstream edits (whitespace changes, CDN variance) are routine. Hard-blocking on external staleness would wedge the harness on conditions outside operator control. The advisory pattern preserves auditability without creating a DoS vector against the harness via external source manipulation.

### 26.4 Monitoring — Pruning Agent `external_source_audit` Sub-Routine

The monitoring responsibility is placed on the Pruning Agent as a new sub-routine. No new component is introduced.

**Cadence:**
- Default: aligned with Pruning cadence (every 50 commits or 24 hours; §11.12).
- Per-fact override via `refetch_policy` field: `hourly` for fast-moving sources, `never` for sources intentionally pinned at a snapshot.

**Failure isolation (C-EXT-PROV3):** If N consecutive audit passes fail to reach the network (default N=5, configurable), the Pruning Agent suspends further external-audit work — but **not** Git-side pruning — and emits `EXTERNAL_AUDIT_SUSPENDED` (CONSISTENCY, async). This prevents log-flooding under sustained network partition.

### 26.5 Spec Block — External Document Provenance

**What it must do:**
- Bind every Layer 4 fact written from an external source to a hash-pinned snapshot of that source at write time.
- Detect source drift (content change) and source loss (unreachability) on a scheduled cadence, emitting advisory Ledger entries without blocking writes or queries.

**What it explicitly does NOT do:**
- Auto-retract or auto-rewrite facts when their source changes. Staleness is surfaced; reconciliation is a separate human- or Coder-Agent-driven action.
- Guarantee fetch fidelity for sources that serve non-deterministic content (dynamic pages, auth-gated resources). Such sources should be snapshotted to an `archive_uri` before provenance recording.

**Hard constraints:**
- **C-EXT-PROV1:** Layer 4 external facts without `external_provenance` block in the patch metadata cannot be compiled. Write engine rejects.
- **C-EXT-PROV2:** Staleness detection MUST be advisory. No code path promotes STALE or UNAVAILABLE to a blocking state automatically.
- **C-EXT-PROV3:** Pruning Agent audit sub-routine failures MUST NOT propagate to Git-side pruning. Isolation is explicit.

**Tradeoffs decided:**
- Advisory-only over hard-blocking (§26.3 rationale).
- Extended Pruning Agent over new dedicated component (§26.4 rationale).
- SHA-256 as sole hash algorithm for v1.2; field is enum-typed for future agility (BLAKE3 etc.) without schema migration.

**Open questions (deferred):**
- **OQ-SC3** — Reconciliation workflow for STALE Layer 4 facts once detected. Currently the fact stays in `.vindex` with an advisory flag; whether a Coder Agent auto-proposes a refresh patch or whether operator approval is required first is unspecified. Implementation-time decision per GS13 disposition.

**Interface contracts:**

```
IC-EXT-PROV1 — Write engine → patch validation
  From: Layer 4 .larql patch submitted to write engine
  To:   MEMIT compilation path
  What A exposes: external_provenance block present and well-formed.
  Failure behavior: LAYER4_MISSING_PROVENANCE (UNRECOVERABLE at patch level).

IC-EXT-PROV2 — Pruning Agent audit → State Ledger
  From: Pruning Agent external_source_audit sub-routine
  To:   State Ledger CONSISTENCY stream
  What A exposes: EXTERNAL_PROVENANCE_STALE or EXTERNAL_PROVENANCE_UNAVAILABLE
    entries keyed by fact_triple_hash + source_uri.
  Conditions: Refetch performed; hash compared; non-FRESH outcome reached.
  Failure behavior: EXTERNAL_AUDIT_SUSPENDED after N consecutive network
    failures (N configurable, default 5).
```

### 26.6 Non-Goals

§26 does not specify:
- Archive-URI population strategy (operator chooses archive.org, IPFS pin, or none).
- Reconciliation workflow for STALE facts (OQ-SC3 deferred).
- Per-source auth credential handling (out of scope; authoritative sources should be public or snapshotted).

---

## 27. Ledger Retention Policy

### 27.1 Purpose

Ledger retention policy governs how long each entry persists, how archival is structured, and how PROJECT_CLOSED interacts with archival I/O. §27 specifies a two-tier governance model (Tier 1 floor + Tier 3 active window), a canonical archive format `ledger-archive/v1`, and an async-archival PROJECT_CLOSED ceremony. Extends and supersedes the v1.1 IC-LDG-RETAIN block (D89). Source: GAP-12 / v3 GS9 D103/D104/D105.

### 27.2 Two-Tier Retention Governance (D103)

Two-tier retention: Tier 1 declares the immutable minimum floor; Tier 3 declares the active-in-hot-storage period.

| Parameter | Tier | Default | Constraint |
|---|---|---|---|
| `ledger_retention_floor` | Tier 1 | 7 years | Minimum total retention; cannot be reduced (C-RETENTION1). |
| `ledger_active_period` | Tier 3 | 90 days | Hot-storage window; operator-tunable. |
| `ledger_archive_period` | derived | floor − active | Must be ≥ 0; archive storage holds. |

**C-SL2 interaction (immutable-downward preserved):**
- `ledger_retention_floor` is immutable once set at Genesis. It may be *extended* by the `LEDGER_RETENTION_EXTENDED` ceremony (§27.4) but never shortened.
- `ledger_active_period` is operator-tunable downward to a minimum of **30 days** (Tier 1 floor on a Tier 3 value; C-RETENTION2). Attempts to reduce below 30 days are rejected by the Transaction Controller.
- `ledger_archive_period` is not directly configured; it is derived to satisfy `active + archive ≥ floor`. Reducing `active_period` extends `archive_period` for the same total.

Rationale: Seven years mirrors standard financial / legal audit retention floors and gives a defensible forensic window for the full lifecycle of a typical project. Ninety days active reflects the practical operational-debugging query window without forcing hot-storage costs on old entries.

### 27.3 Archival Format — `ledger-archive/v1` (D104)

Canonical archive format for v1.2. Versioned identifier permits future evolution without breaking restore paths.

```
Format identifier:     ledger-archive/v1
Compression:           zstd (level 19, long mode enabled)
Per-entry integrity:   SHA-256 (matches hot-Ledger algorithm)
Archive integrity:     Merkle root over all entries in archive batch
Chain-link anchors:    chain_hash_at_start + chain_hash_at_end bind archive
                       to the hot Ledger at batch boundaries
```

**Manifest schema (`archive-manifest.json`, sibling to compressed payload):**

| Field | Type | Notes |
|---|---|---|
| `archive_id` | UUID | Unique per archive batch. |
| `format_version` | string | `ledger-archive/v1`. |
| `start_ledger_seq` | integer | First entry in archive. |
| `end_ledger_seq` | integer | Last entry in archive. |
| `start_timestamp` | ISO-8601 UTC | First entry time. |
| `end_timestamp` | ISO-8601 UTC | Last entry time. |
| `entry_count` | integer | For restore verification. |
| `chain_hash_at_start` | hex | Hash of entry at `start_ledger_seq − 1`. |
| `chain_hash_at_end` | hex | Hash of entry at `end_ledger_seq`. |
| `archive_merkle_root` | hex | Merkle root over archived entries. |
| `compression_algo` | string | `zstd`. |
| `compression_params` | string | `level=19;long=27`. |
| `payload_sha256` | hex | Hash of the compressed payload file. |
| `manifest_sha256` | hex | Self-hash excluding this field. |
| `signer_identity` | string | Operator identity signing archive. |
| `signer_public_key_material` | blob | Public key material, bound to the manifest (GAP-52 / GS11 resolution — `ARCHIVE_KEY_SEALED` Ledger entry emitted at seal time; Genesis Seal cross-check at restore). |
| `signature` | string | Signature over manifest (excluding `signature` field). |

**Restore procedure:**
1. Verify `manifest_sha256` self-consistency.
2. Verify operator signature against trusted identity registry; cross-check `signer_public_key_material` against Genesis Seal archive-key record.
3. Verify `payload_sha256` against compressed payload file.
4. Decompress payload.
5. Verify `archive_merkle_root` against decompressed entries.
6. Verify `chain_hash_at_start` links to hot-Ledger entry (`end_seq − 1`) — confirms archive is contiguous with hot Ledger.
7. Expose restored range as read-only query layer appended to hot Ledger.

Merkle-chain-lite integrity extends across archive boundaries: a chain verification pass reads the manifest's `chain_hash_at_end` to continue verification into the next archive segment or into hot Ledger, **without requiring decompression** — the chain is verifiable against anchors alone.

### 27.4 PROJECT_CLOSED Ceremony Relationship (D105)

`PROJECT_CLOSED` (LIFECYCLE, signed — delegates to IC-SCOPE-AUTH-1 ceremony_type `PROJECT_CLOSE`) is synchronous and triggers — but does not depend on — final archival (C-RETENTION4).

**Sequence:**
1. `PROJECT_CLOSED` entry committed to Ledger synchronously. Harness enters `CLOSED` state — no new agent tokens issued, no new writes accepted.
2. `FINAL_STATE_SNAPSHOT` entry emitted, paired atomically with `PROJECT_CLOSED`, carrying the Ledger chain tip hash and the `.vindex` snapshot hash at close. (IC-RETENTION1 contract: atomic pair; either both commit or neither commits.)
3. Archive ceremony dispatched **asynchronously**:
   - If archive storage is available and writable: archive batch produced per §27.3, manifest signed, `PROJECT_ARCHIVED` Ledger entry emitted.
   - If archive storage is unavailable: `PROJECT_ARCHIVE_PENDING` entry emitted instead, with SLA clock started (default 30 days to resolve).
4. Expiry of SLA without `PROJECT_ARCHIVED` emission raises `PROJECT_ARCHIVE_SLA_BREACHED` (LIFECYCLE, sync, W1) — an operational incident requiring operator intervention. It does not alter the Ledger state of the project (which remains `CLOSED`) but flags the archival gap in any subsequent audit.

Rationale: Decoupling `PROJECT_CLOSED` (which must succeed atomically as a forensic anchor) from archival I/O (which can fail for storage reasons outside harness control) preserves closing-ceremony atomicity without fabricating a success signal for archival that may not have occurred.

### 27.5 Retention Update Ceremonies

**Floor extension (immutable-downward preserved):**
`LEDGER_RETENTION_EXTENDED` ceremony (IC-SCOPE-AUTH-1 ceremony_type `RETENTION_EXTEND`), Tier 1 authority signer (CAK), carries `new_floor_years > old_floor_years`. Attempts to reduce the floor are rejected at entry-construction time — the ceremony is structurally incapable of expressing a reduction.

**Active-period changes:**
`LEDGER_ACTIVE_PERIOD_UPDATED`, Tier 3 authority (operator), carries new value ≥ 30-day floor. Reduction permitted within floor.

### 27.6 Spec Block — Ledger Retention

**What it must guarantee:**
- No Ledger entry is deleted or made unreadable within the Tier 1 retention floor, regardless of operator configuration.
- Archived entries remain chain-verifiable against the hot Ledger Merkle chain via manifest anchors.
- Project close produces a synchronous forensic anchor even when archival storage is temporarily unavailable.

**What it explicitly does NOT guarantee:**
- Uninterrupted query latency for archived entries. Restore can require decompression and signature verification — a read-time cost.
- Archival storage medium availability. External dependency, monitored via SLA mechanism but not guaranteed by the harness.

**Hard constraints:**
- **C-RETENTION1:** `ledger_retention_floor` is monotonically non-decreasing from Genesis onward.
- **C-RETENTION2:** `ledger_active_period ≥ 30 days`.
- **C-RETENTION3:** Archive manifests MUST link chain hashes across archive boundaries for end-to-end Merkle verifiability.
- **C-RETENTION4:** PROJECT_CLOSED Ledger write MUST NOT block on archive I/O.

**Tradeoffs decided:**
- Single canonical archive format (zstd + SHA-256 + Merkle) over per-project format negotiation — forensic readability over compression tuning.
- Seven-year floor as default, operator may only extend — short-project operators bear the cost; long-lived projects are the common case.
- Async archival with SLA-tracked pending state over synchronous archival — preserves closing-ceremony atomicity.

**Open questions (deferred):**
- OQ-SL1 is **closed** by this spec block.
- GAP-60 (retired-key revocation metadata: retired-clean vs. retired-compromised classification for archive signing keys) deferred to v2.

**Interface contracts:**

```
IC-RETENTION1 — PROJECT_CLOSED → final snapshot
  From: Transaction Controller at project-close ceremony
  To:   State Ledger LIFECYCLE stream
  What A exposes: Synchronous PROJECT_CLOSED + FINAL_STATE_SNAPSHOT pair;
    chain tip hash; .vindex snapshot hash.
  Failure behavior: Ceremony atomic — both succeed or neither commits.

IC-RETENTION2 — Archive manifest → restore path
  From: Completed archive batch
  To:   Any future restore invocation
  What A exposes: Signed manifest with Merkle root, chain-link anchors,
    payload hash; compressed payload.
  Conditions: All archive verification steps pass (§27.3 sequence 1–7).
  Failure behavior: RESTORE_MANIFEST_INVALID or RESTORE_CHAIN_BREAK.
```

### 27.7 Non-Goals

§27 does not specify:
- External cold-storage export format (v2 — separate from archive format).
- Cross-project archive sharing policies (v2).
- Retired-key revocation metadata (GAP-60; v2-deferred).

---

═══════════════════════════════════════════════════
# PART VII — REFERENCE APPENDICES
═══════════════════════════════════════════════════

## Appendix A — Deployment Preconditions

Environmental contracts the harness assumes from its deployment context.

**Base preconditions (carried from v1.1):**
- Single machine, single OS user owning the harness process.
- Filesystem supports POSIX permissions; `<harness_root>/` readable only by harness user.
- Git binary installed and trusted (standard OS package).
- Docker or E2B runtime available for sandbox execution.
- Base model file present at configured location with known hash (provenance verified at install, not runtime).
- Initial Orchestrator signing key generated or imported before first boot.
- `genesis_prepared_timeout` set in Tier 1 config before Genesis initiation (C-GATE-2).
- Network connectivity for external content ingestion (Architect Agent) is operator-controlled.
- Backup strategy for `<harness_root>/` is operator responsibility.

**v1.2 preconditions — CAK trust chain:**
- Operator root key pair generated offline before first boot; public half embedded in the distributed harness binary at compile time (C-BOOT-5; GAP-57 implication — harness binaries are per-operator, not universal).
- CAK public half generated by operator HSM or equivalent key ceremony, available to the CAK bootstrap tool before first boot.
- CAK private half held offline (HSM-preferred) under operator control. Private half never enters tool memory (C-BOOT-2).
- CAK bootstrap tool distributed via a signing authority chain distinct from the harness release key (C-BOOT-6 — two independent trust roots converging at first boot).
- **A11 — v1 CAK backup custodian pre-arrangement.** Operator MUST pre-arrange break-glass custodians BEFORE declaring the harness operational. M ≥ 3 custodians, identities documented outside the harness, physical-access provisions in place for §23.3 / C-BG-4. This is not an optional step — the break-glass channel is unreachable without pre-arranged custodians, and CAK compromise after deployment without pre-arranged custodians results in `TRUST_ROOT_LOST` terminal state with no recovery path short of Genesis re-initialization.

**v1.2 preconditions — break-glass channel:**
- Break-glass public key material available before first boot; private half held offline in HSMs distinct from the primary CAK HSM, distributed among M ≥ 3 operator identities per operator policy.
- Physical-access provision for the harness host by operator identities holding break-glass keys (C-BG-4). "Physical access" means out-of-band injection path that is not a network API — the exact implementation (serial console, physically-present USB, etc.) is operator-owned.
- Operator acceptance of T-W-BG-1: break-glass friction is a deliberate security property. Rapid incident response is incompatible with the break-glass channel's design; operators who need rapid CAK replacement must plan around this ceiling.

**v1.2 preconditions — operational storage:**
- `.dry-run-store/` is operator-owned (GAP-33, T-S-RP-1 accepted for v1). Metadata-only Warden audit applies per IC-DRS-1. Operators accepting this trust model must plan for v2 migration to content-addressed immutable storage if content-level immutability becomes a requirement.
- `.ledger-archive/` storage availability at project close (IC-RETENTION2). If storage is unavailable, `PROJECT_ARCHIVE_PENDING` is emitted; the 30-day default SLA to resolve is operator-tracked.

**v1.2 preconditions — network and sources:**
- External document sources for Layer 4 facts SHOULD be public or operator-snapshotted. Auth-gated or non-deterministic sources require `archive_uri` population to achieve provenance (§26.2).

**v1.2 preconditions — path selection:**
- GAP-4 path selection (A / B / C) is deferred to the operator. Path-conditional deployment implications (GAP-56 burst-limit density, GAP-57 per-operator binary, GAP-58 state-machine completeness per path) are operator-evaluated before selection. Activates OQ-PATH-DEPLOY on selection.

## Appendix B — Interface Contract Index

Canonical list of inter-component contracts. Cross-references to session of origin.

### From Session 1 (Schema)
- **IC1** — Write Engine receives base-type tag + relation-family tag; enforces `violates` hard rejection.
- **IC2** — Validator receives declared vocabulary; rejects undeclared types or relations.
- **IC3** — Pruning Agent receives deletion policy + namespace flag; restricted to Structural/Knowledge families.
- **IC4** — Orchestrator receives query results with `coverage_quality` flag; empty results route to documentation ingestion.

### From Session 2 (Write Engine)
- **IC5** — Write Engine ← Validator: pre-validated `.larql` patch.
- **IC6** — Write Engine → State Ledger: overlay filename + hash post-compile.
- **IC7** — Write Engine → Orchestrator: write result signal.
- **IC8** — Write Engine ← Orchestrator (Genesis): schema migration token (revised T7).
- **IC9** — Behavioral Probe → Orchestrator: probe result with expected and actual signals.

### From Session 3 (Security)
- **IC10** — Gate ← Agent: signed `.larql` patch + identity token (extended T5).
- **IC11** — Gate → Validator: verified patch (identity, scope, integrity confirmed).
- **IC12** — Gate → Orchestrator: rejection signal (extended with T5 reason codes).
- **IC13** — Gate → Ledger: evaluation record (every interaction).
- **IC14** — Orchestrator → Write Engine: schema migration token (revised T7, admission-time).
- **IC15** — Write Engine → Ledger: pre-write + post-write hashes + outcome.
- **IC16** — Post-Genesis Seal → Ledger: `IMMUTABLE_ANCHOR` entry.

### From Session 4 (Validation)
- **IC17** — TGA ← Orchestrator: task spec + schema vocabulary.
- **IC18** — Sandbox → Verbal Feedback Generator: execution result.
- **IC19** — Verbal Feedback Generator → Coder: structured failure report.
- **IC20** — Patch Validator → Orchestrator: patch verdict.
- **IC21** — Validator → Orchestrator: signed pass/fail signal (verified before Commit Executor spawn).
- **IC22** — Orchestrator → Commit Executor: verified signal + gate-cleared patch + code payload.
- **IC23** — Commit Executor → Transaction Controller: 2PC initiation.
- **IC24** — Meta-Validator → Ledger: health record (extended T3 per-case; v1.1: includes `corpus_staleness_flag` and `corpus_size_at_run` fields; `health_score` field is `NOT_COMPUTED` when corpus < 20 cases).

### From Session 5 (State Consistency)
- **IC-SC1** — `.larql` schema: `CONTENT_CLASSIFICATION` mandatory.
- **IC-SC2** — Gate → Write Engine: classification tag unmodified.
- **IC-SC3** — Transaction Controller ← Ledger: classification readable for rollback direction.
- **IC-TPC1** — Commit Executor ← Orchestrator: verified package + classification.
- **IC-TPC2** — Commit Executor → Ledger: `PREPARED` / `COMMITTED` entries.
- **IC-TPC3** — Commit Executor → MEMIT: compile request returns `{success, overlay_filepath, overlay_hash}`.
- **IC-TPC4** — Commit Executor → Transaction Controller: failure signal at phase boundary.
- **IC-TC1** — Transaction Controller ← Commit Executor: 2PC step outcomes.
- **IC-TC4** — Transaction Controller → Ledger: compensation records.
- **IC-TC5** — Transaction Controller → Orchestrator: circuit-breaker trip signal.
- **IC-TC6** — Transaction Controller → MEMIT: mount retry signal.
- **IC-SL1** — Ledger ← Commit Executor: `PREPARED` / `COMMITTED`.
- **IC-SL2** — Ledger ← Transaction Controller: `COMPENSATED` / `FAILED`.
- **IC-SL3** — Ledger ← Bootstrap (Genesis): `IMMUTABLE_ANCHOR`.
- **IC-SL4** — Ledger → Rollback Coordinator: commit-to-snapshot lookup.
- **IC-SL6** — Ledger → Audit: integrity-violation events.
- **IC-GOC1** — Commit Executor → Ledger: classification mandatory on entries.
- **IC-GOC2** — Pruning → Commit Executor: catch-up patch with `requires_human_review`.
- **IC-PA3** — Pruning ← Audit: gap record read access.
- **IC-PA4** — Pruning → Gate: deletions via standard write path.
- **IC-PA6** — Pruning → Orchestrator: `stale_urgent` count signal.
- **IC-CW1** — Orchestrator → Scope Lock Registry: task declarations produce lock entries.
- **IC-CW2** — Orchestrator → Coder: task assignment with declared-and-locked scope.
- **IC-CW3** — Commit Executor ← Orchestrator: verified signal carries scope lock reference.
- **IC-OC1** — Transaction Controller → Commit Executor: compaction trigger, drain signal.
- **IC-OC2** — Transaction Controller → MEMIT: Genesis-Mode recompile request.
- **IC-OC4** — MEMIT → Behavioral Probe: verification request on compacted overlay.
- **IC-OC5** — Transaction Controller → Ledger: compaction lifecycle entries.

### From Session 6 (Orchestration)
- **IC-OR1** — Orchestrator → Validator: pass/fail signal verification.
- **IC-OR2** — Orchestrator → Commit Executor: verified package + classification + lock ref + retry state.
- **IC-OR3** — Orchestrator → Ledger: sole write authority (all ledger writes routed).
- **IC-OR4** — Orchestrator → Scope Lock Registry: exclusive read/write.
- **IC-OR5** — Orchestrator → Agent Runtime Wrapper: `agent_invoke(agent_name, input, allowed_tools)`.
- **IC-OR6** — Orchestrator → Human Review Queue: pause workflow with full package.
- **IC-OR7** — Orchestrator → Consistency Status API (six-state enum per T10).
- **IC-OR8** — Human → Orchestrator: signed abort request.
- **IC-OR9** — Orchestrator → Task Lineage Ledger: `TASK_DECOMPOSED` entries.

### From Session 7 (Integration)
- **IC-V-TGA1** — TGA output → Stub Probe → Pass/Fail before Coder invoked (T2).
- **IC-V-TGA2** — Meta-TGA → Ledger: health record parallel to IC24; v1.1 extended per IC-CORPUS-AUTH (T2).
- **IC-SL7** — Ledger ← Bootstrap: `SEALED_CORPUS_INTEGRITY_FAIL` on dual-store mismatch (T3).
- **IC-SL8** — Ledger ← Orchestrator: `SEALED_CORPUS_ACCESS` at Meta-* scheduling (T3).
- **IC-SL9** — Ledger ← Manifest Update Handler: `SEALED_CORPUS_UPDATE` on signed extension (T3).
- **IC-CFG1** — Git commit-hook → Ledger: `CONFIG_UPDATE` on `.harness/` file changes (T4).
- **IC-CFG2** — Bootstrap → Ledger: `CONFIG_INTEGRITY_FAIL` on boot-time mismatch (T4).
- **IC-CFG3** — Orchestrator → WSD + YAML: hash binding check at invocation; `YAML_BINDING_FAIL` on mismatch (T4).
- **IC-MEMIT-3** — Write Engine → Ledger: `ANCHOR_ESTABLISHED` flag on qualifying entries (T6).
- **IC-PA7** — Pruning → Orchestrator: Hold-state query returning `held | not_held` per edge (T8).
- **IC-PA8** — Pruning → Orchestrator: catch-up patch submission with `requires_human_review` (T10).
- **IC-OR10** — Orchestrator → Reconciliation Review Queue (T10).
- **IC-OR11** — Orchestrator → Ledger: backlog warning / critical entries (T10).
- **IC-OR12** — Orchestrator → Consistency Status: `RECONCILIATION_BACKLOG` state (T10).
- **IC-OR13** — Reconciliation Reviewer → Gate: reviewer-signed catch-up patch (T10).
- **IC-OR14** — Reviewer `modify_patch` output → Validator: modified patches re-enter cascade (T10).
- **IC-OC6** — Write Engine → Compaction Bundler: patch set consumed (T9).
- **IC-OC7** — Compaction Bundler → Ledger: `COMPACTION_BUNDLE_SEALED` (T9).
- **IC-OC8** — Retention Manager → Ledger: `SUPERSEDED_BUNDLE_EXPIRED` (T9).
- **IC-LDG1** — Component → Orchestrator: ledger write request (T11).
- **IC-LDG2** — Orchestrator → Ledger: authenticated append with chain hash (T11).
- **IC-LDG3** — Gate / TC / Boot-verifier → Ledger: emergency write path (T11).
- **IC-LDG4** — Orchestrator → Query API: tiered read access (T11).
- **IC-LDG5** — Retention Manager → Ledger: epoch archival ops (T11).

### From IC Review Session (v1.1 — D81–D90)
- **IC-GATE-8** — Gate pre-check #8: `larql_syntax_version` header validation. Rejects absent, below-minimum, and forward-version patches with distinct error codes (`VERSION_REJECTED`, `VERSION_UNSUPPORTED`). Advisory path (`LARQL_VERSION_LEGACY`) for legacy-but-supported versions. Compaction re-run requires versioned parser and `larql_migration_manifest` in Tier 1 config (D81, D82, C-GATE-1).
- **IC-WE-1** — Write Engine → Transaction Controller: `drift_state` object. Fields: `edge_count_since_anchor`, `drift_tier` (NOMINAL/WARNING/HARD/CRITICAL), `anchor_event_id`, `overlay_file_count`, `p95_latency_ratio`. Read before every write token issuance; drift counter reconciled every 100 COMMITTED entries within 5% tolerance (D83, C-WE-1).
- **IC-TC-RESET** — Human Operator → Transaction Controller: signed circuit breaker reset ceremony. TC independently verifies preconditions before accepting. Automatic READ_ONLY on trip; write resumption via signed ceremony only. W3 path excluded from reset authority (D84).
- **IC-TC-TIMEOUT** — Transaction Controller timeout monitor → Write Engine + Orchestrator: two-value timeout model (`incremental_prepared_timeout` default 2h; `genesis_prepared_timeout` operator-set mandatory, C-GATE-2). Incremental timeout → Phase 1 rollback, Hold persists, retry as infrastructure failure. Genesis timeout → circuit breaker trips (DIVERGED_STATE), no auto-compensation (D85).
- **IC-OC-PROBE** — Behavioral Probe (compaction) → Transaction Controller: `CompactionProbeReport` struct. Stratified sampling (CORE 100%; SUPPORTING ≥20% floor; INCIDENTAL 10%); abort thresholds CORE 1.0 (C-OC3) / SUPPORTING 0.95 / INCIDENTAL 0.80. Random seed logged. Sampling rates provisional (OQ-OC3) (D86).
- **IC-SCOPE-UPDATE** — Orchestrator + Gate: Write Scope Definition update ceremony. Mid-flight updates accepted (no drain). Gate returns `SCOPE_HASH_MISMATCH` (not generic) with current scope hash. Active PREPARED transactions not interrupted. Scope changes forward-only (D87).
- **IC-CORPUS-AUTH** — Corpus Author → Sealed Corpus (Meta-Validator / Meta-TGA): role-restricted submission (C-GOC4) with format validation. Minimum 20 cases for valid Health Score. Staleness flag at 90 days. Case formats defined (D88).
- **IC-LDG-RETAIN** — Operator → Ledger: retention lifecycle interface. `PROJECT_INITIATED` (W2 bootstrap, immutable), `PROJECT_CLOSED` (write-final ceremony), `RETENTION_OVERRIDE_EXTENDED` (extensions only). Retention immutable-downward (C-SL2). INTEGRITY_VIOLATION epochs unconditionally indefinite. Archival format versioned `"1.0"` (D89).
- **IC-GATE-9** — Gate → Orchestrator → Coder Agent: `CONTENT_CLASSIFICATION_MIXED` structured rejection with `split_guidance` payload. Gate triple-level classification is authoritative over Coder declarations. `complexity_flag` set when > 5 sub-patches required → human review escalation. Loop detection at 3 equivalent re-rejections (D90).

### From Phase 2 Gap Sessions (v1.1 → v1.2)

*Grouped by originating gap session. Every contract below is a ratified addition or amendment. Deprecated / superseded v1.1 contracts are listed at the end.*

**Ceremony Authorization (v2 GS4 — GAP-26):**
- **IC-SCOPE-AUTH-1** — NEW umbrella authorization contract for all GOVERNANCE-class ceremonies. Common CeremonyToken envelope (ceremony_type / ceremony_id / ceremony_payload / key_ref = CAK). Non-delegable uniform preconditions. See §20.3.
- **IC-TC-RESET** — AMENDED (A3). Reset ceremony authorization key is the CAK per IC-SCOPE-AUTH-1. Genesis-trip Hold-release precondition branch added (A12). CAK-authorization requirement is necessary-but-not-sufficient; TC independent precondition verification unchanged.
- **IC-HOLD-RELEASE** — DELEGATION UPDATE. Authorization layer delegates to IC-SCOPE-AUTH-1. Payload body retained: `hold_id`, `hold_type`, `release_reason_code`.
- **IC-SCOPE-UPDATE** — DELEGATION UPDATE (A5, A6, A9). Payload body retained; admission order specifies rate-limit precedes signature verification. `ceremony_token_id` replaces prior standalone `ratification_signature` / `operator_signature` field.
- **IC-SCHEMA-EXTEND, IC-LDG-RETAIN, IC-SL8** — DELEGATION UPDATE. All delegate authorization to IC-SCOPE-AUTH-1.
- **IC-MANIFEST-1** — AMENDED. Ceremony authorization delegates to IC-SCOPE-AUTH-1; `bucket_map` provisional-flag semantics per §22; Check 8 added (manifest-lattice completeness, GAP-29a).

**Scope Registry (v3 GS5; GS12):**
- **IC-SCOPE-RECONCILE** — NEW. Orchestrator-restart scope-registry reconciliation against Ledger `SCOPE_UPDATED` chain. §10.9.1.
- **IC-AGG-COUNTER** — NEW. Per-Orchestrator-instance aggregate `SCOPE_HASH_MISMATCH` counter behavior (no reset on review; cooldown = M seconds). §14.3, GAP-38.
- **IC-AGG-ALERT-LINK** — NEW. Aggregate-alert → review queue cross-link format, including contributing-invocation list and source agents. §14.3.

**Transaction Controller / State Machine (GS10–GS12):**
- **IC-GCO-1** — NEW. Governance-category write carve-out under `CIRCUIT_TRIPPED` — narrow scope restricted to IC-TC-RESET ceremony entries via ceremony_token_id binding. Closes T-SC-W-2. §11.8.1, GAP-37.
- **IC-CRR-1** — NEW. `CIRCUIT_RESET_REJECTED` rate limit: N=5 / M=60min, advisory + operator alert. GAP-36.
- **IC-TC-PRECURSOR-QUERY** — NEW. TC → Ledger precursor-lookup on Hold-release ceremony admission: coverage + audit-window check. GAP-31.
- **IC-REL-PRECURSOR** — NEW. `HOLD_RELEASE_REASON_UNWARRANTED` emission when operator-cited precursor fails Hold-coverage or audit-window check. SECURITY, sync, W1 (not W3 per C-W3-1). GAP-31.
- **IC-PREPARE-SCOPE** — NEW. `governing_scope_hash` field added to PREPARED and COMMITTED entries (captured at PREPARE, preserved at COMMIT, nullable for pre-amendment entries). GAP-34.
- **IC-MON-GTOTM** — NEW. Monitor pairing-check: `GENESIS_TIMEOUT_TRIP_MISSING` on unpaired genesis-timeout. CONSISTENCY, async, W1. C-GTO-1 / C-GTO-2. GAP-30.

**Dry-Run Store (v2 GS8; GS10):**
- **IC-DRS-1** — NEW. Operator-owned `.dry-run-store/` at `<harness_root>/.dry-run-store/`; 37-day minimum retention; metadata-only Warden audit; manifest-hash anchor in Ledger. GAP-33; T-S-RP-1 accepted.
- **IC-DRYRUN-1** — NEW (v2 GS8). `dry_run_report` artifact shape for IC-MANIFEST-1 Check #5/#6 (dry-run artifact freshness + hash binding).

**Unified Ledger W3 (GS10):**
- **IC-W3-POLICY-1** — NEW. W3 admission consolidation per C-W3-1 two-admission-criteria. Four ratified carve-outs: `INTEGRITY_VIOLATION_EMERGENCY`, governance-ceremony entries under trip, `TRUST_ROOT_LOST`, `BURST_SUSPENDED`. GAP-29b. §16.2.
- **IC-MANIFEST-1** Check 8 — AMENDED. Manifest-lattice completeness verification at ratification; `MANIFEST_LATTICE_INCOMPLETE` emitted on failure (SECURITY, sync). GAP-29a.

**CAK Bootstrap / Burst / Break-Glass (GS10):**
- **IC-BOOT-1** — NEW. CAK bootstrap tool interface. Dual-root signing (operator root + harness release key); atomic write; signed boot manifest; refuse-boot on verification failure. C-BOOT-1 through C-BOOT-7. GAP-40. §23.1.
- **IC-CAKB-1** — NEW. Per-CAK burst limit N=5 / 10min; `BURST_SUSPENDED` state; 60-min auto-clear or Tier 1 explicit clear; orthogonal to GAP-27 and GAP-36. GAP-41. §23.2.
- **IC-BG-1** — NEW. Break-glass channel: second Tier 1 anchor (`break_glass_key_anchor`), M ≥ 3 quorum, physical-access injection, single-purpose `CAK_ROTATION_EMERGENCY`, `TRUST_ROOT_LOST` terminal double-compromise state. Partially closes OQ-S-CAK-1. GAP-42. §23.3.

**Genesis Initiation / Hold Interaction (GS10; GS11):**
- **IC-GIB-1** — NEW. `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` (INTEGRITY, sync, W1) + `GENESIS_INITIATION_ABUSE_PATTERN` (SECURITY, aggregate, ≥ 3 in 60min). Neither W3-eligible per C-W3-1. GAP-44.
- **IC-RP-1** — NEW. `RETENTION_PRUNING` ceremony type + `artifact_retention_manager` role. GAP-47.

**Rotation Registry / Boot-Time Validation (GS11):**
- **IC-CAK-IDENTITY** — NEW. Stable external `operator_id` bound at first-boot CAK registration; carried unchanged across rotation. Closes T-S4-N1. GAP-46.
- **IC-BOOT-RLRF** — NEW. Boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation: per-initiator and per-agent rate-limit intervals strictly less than corresponding Ledger-entry minimum retention windows. Closes T-S7-N1. §13.5 step 5a. GAP-46.
- **IC-HOOK-BOOT** — NEW. Boot-time hook binary hash verification against Tier 2 `hook-registry/v1`. `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) on mismatch. §13.5 step 4a. GAP-54.

**Constitutional Tests / Sandbox (GS12):**
- **IC-CLK-META** — NEW. `clock_stub_required` flag required on every constitutional test nomination. Declarative attestation. GAP-39.
- **IC-CLK-SANDBOX** — NEW. Sandbox synthetic-clock injection mandatory when `clock_stub_required=true`; missing injection → `SANDBOX_CONFIG_ERROR` (not test failure). GAP-39.
- **IC-NOM-DRYRUN** — NEW. Nomination-time declarative attestation + dry-run sufficient for v1.2 Q-gate evidence (closes OQ-V9). GAP-39.

**External Document Provenance (v3 GS9 — GAP-11):**
- **IC-EXT-PROV1** — NEW. Write engine patch validation: `external_provenance` block required for Layer 4 external facts; absence → `LAYER4_MISSING_PROVENANCE` (UNRECOVERABLE). §26.5.
- **IC-EXT-PROV2** — NEW. Pruning Agent `external_source_audit` → Ledger: `EXTERNAL_PROVENANCE_STALE` / `EXTERNAL_PROVENANCE_UNAVAILABLE` advisory (CONSISTENCY, async). `EXTERNAL_AUDIT_SUSPENDED` on N consecutive network failures (default N=5). §26.5.

**Ledger Retention (v3 GS9 — GAP-12):**
- **IC-RETENTION1** — NEW. PROJECT_CLOSED + FINAL_STATE_SNAPSHOT paired atomic commit. §27.4, §27.6.
- **IC-RETENTION2** — NEW. Archive-manifest restore path: seven-step verification (manifest self-hash → signer identity → payload hash → decompress → Merkle root → chain-link continuity → expose as read-only query layer). §27.3, §27.6.

**Review Queue (GS11 — T-PM-vs-PA):**
- **IC-REVIEW-QUEUE (amended)** — Merged-queue policy: external-provenance advisories merge into the existing review queue item for the same `edge_id`. CORE-importance facts with STALE or UNAVAILABLE provenance receive priority elevation; both advisory reasons must be acknowledged. §15.1.

**Corpus Authorship (GS8; v2 GS9):**
- **IC-CORPUS-AUTH (amended A12)** — `expires_at` predicate at submission ingress. §24.2.
- **IC-SL7 (amended A13)** — `contains_expired_author_cases` response field; `EXPIRED_AUTHOR_PRESENT` advisory flag on Meta-* Ledger result record. §24.2.
- **IC-SL8** — corpus manifest signing; delegates authorization to IC-SCOPE-AUTH-1.

**Deprecated / Superseded in v1.2:**
- **IC-SCOPE-UPDATE (v1.1 standalone authorization form)** — superseded by IC-SCOPE-AUTH-1 delegation. `operator_signature` field no longer standalone; now nested within CeremonyToken envelope.
- **`HOLD_RELEASE_SIGNATURE_INVALID`, `HOLD_RELEASE_REPLAY_REJECTED`** (Ledger entry types; A7b) — deprecated. Both collapse into the uniform IC-SCOPE-AUTH-1 failure set (`CEREMONY_AUTH_SIGNATURE_INVALID`, `CEREMONY_AUTH_REPLAY_REJECTED`).

## Appendix C — Ledger Entry Type Catalog

Organized by audit category tag. v1.2 additions are marked `v1.2`. v1.0 and v1.1 entries are preserved verbatim from the v1.1 baseline; dispositions (DEPRECATED per A7b, AMENDED per A8 or A14) are attached inline.

**Category mapping note:** The catalog's audit categories — SECURITY, CONSISTENCY, VALIDATION, GOVERNANCE, LIFECYCLE — are the tags used by the Unified Ledger (§16). Every entry carries exactly one category tag. Writes under the W1 / W2 / W3 admission policy (§16.2, IC-W3-POLICY-1) reference this tag at admission time — carve-outs under `CIRCUIT_TRIPPED` are narrowed by category (IC-GCO-1) and the W3 emergency path (IC-LDG3) is restricted to the four ratified carve-outs documented at §16.2.

### SECURITY category

**v1.0 / v1.1 (preserved):**
- `TOKEN_ISSUED`, `TOKEN_CONSUMED`, `TOKEN_REJECTED`, `TOKEN_ABANDONED`
- `SCHEMA_MIGRATION_TOKEN_ISSUED`, `_CONSUMED`, `_REJECTED`, `_EXPIRED_UNUSED`
- `AGENT_SUSPENDED`, `AGENT_UNSUSPENDED`
- `ORCHESTRATOR_KEY_ANCHOR`
- `INTEGRITY_VIOLATION`, `INTEGRITY_VIOLATION_EMERGENCY`
- `YAML_BINDING_FAIL`, `CONFIG_INTEGRITY_FAIL`
- `SEALED_CORPUS_INTEGRITY_FAIL`
- `LARQL_VERSION_LEGACY` *(async advisory — legacy .larql syntax version, still within supported range; v1.1)*
- `VERSION_REJECTED` *(sync — Gate pre-check #8 hard rejection: absent or below-minimum version; v1.1)*
- `VERSION_UNSUPPORTED` *(sync — Gate pre-check #8: patch declares version above current; v1.1)*
- `SCOPE_UPDATE_REJECTED` *(sync — unsigned or invalid Write Scope Definition update attempt; v1.1)*
- `CORPUS_WRITE_REJECTED` *(sync for UNAUTHORIZED_AUTHOR reason; GOVERNANCE category for FORMAT_VIOLATION or DUPLICATE_CASE_ID; v1.1. **v1.2 AMEND:** adds `AUTHOR_EXPIRED` reason code per §24.2 / A12.)*
- `RETENTION_OVERRIDE_REJECTED` *(sync — retention shortening attempt blocked; v1.1)*
- `CONTENT_SPLIT_LOOP` *(async advisory — Coder Agent repeatedly resubmitting mixed-classification patches; v1.1)*
- `CIRCUIT_RESET_REJECTED` *(sync — failed reset ceremony attempt; v1.1; field amended per A2 — structured precondition-unmet reason code required; non-consumed CeremonyToken per GAP-35.)*

**v1.2 additions — Unified CeremonyToken failure set (GS4 / IC-SCOPE-AUTH-1):**
- `CEREMONY_AUTH_SIGNATURE_INVALID` *(sync, W1 — signature on CeremonyToken envelope fails verification against the current CAK anchor; §20.4 admission check 3.)*
- `CEREMONY_AUTH_REPLAY_REJECTED` *(sync, W1 — ceremony_id observed in prior Ledger entry; replay protection; §20.4 admission check 4.)*
- `CEREMONY_AUTH_KEY_EXPIRED` *(sync, W1 — CAK key material past expiration timestamp at verification time.)*
- `CEREMONY_AUTH_KEY_UNKNOWN` *(sync, W1 — `key_ref` resolves to no anchor in Tier 1.)*
- `CEREMONY_AUTH_WRONG_KEY` *(sync, W1 — ceremony signed by OOK or other key rather than CAK; dual-key invariant violation.)*
- `CEREMONY_AUTH_MALFORMED` *(sync, W1 — envelope fails structural validation.)*
- `CEREMONY_REJECTED_BURST_SUSPENDED` *(sync, W1 — ceremony received while CAK in BURST_SUSPENDED state per IC-CAKB-1 / §23.2.)*
- `CEREMONY_REJECTED_CIRCUIT_TRIPPED` *(sync, W1 — ceremony received under CIRCUIT_TRIPPED outside the IC-GCO-1 carve-out.)*
- `CEREMONY_REJECTED_TRUST_ROOT_LOST` *(sync, W1 — ceremony received after TRUST_ROOT_LOST entered; see §23.3.)*
- `CEREMONY_REJECTED_MULTI_CAUSE` *(sync, W1 — multiple rejection conditions simultaneous; carries ordered cause list for forensic clarity.)*

**v1.2 additions — CAK lifecycle (GS10 / §23.1):**
- `CAK_REGISTERED` *(sync, W2 bootstrap — first-boot CAK anchor record; fields: `operator_id`, `cak_public_key`, `anchor_hash`, `boot_manifest_ref`.)*
- `CAK_COMPROMISE_DECLARED` *(sync, W1 — operator declaration via standard ceremony path; triggers defensive posture.)*
- `CAK_COMPROMISED_AT_BOOT` *(sync, W1 — boot-time detection of tamper or anchor mismatch; triggers boot-suspend.)*
- `COMPROMISED_AT_BOOT` *(sync, W1 — generic boot-time compromise detection, distinct from CAK-specific variant above.)*

**v1.2 additions — Burst limit (GS10 / §23.2 / IC-CAKB-1):**
- `BURST_SUSPENDED` *(sync, W1 — CAK entered BURST_SUSPENDED state after exceeding N=5 ceremonies per 10-minute window.)*
- `CAK_BURST_LIMIT_EXCEEDED` *(sync, W1 — triggering event for BURST_SUSPENDED; same window boundary.)*
- `CAK_CEREMONY_BURST_EXCEEDED` *(alias — GS10 co-usage; identical semantics to CAK_BURST_LIMIT_EXCEEDED. [COUNCIL-FLAG: two names appear across GS10 source; recommend canonical spelling `CAK_BURST_LIMIT_EXCEEDED` and treat alias as dropped in final docs.])*
- `CAK_BURST_AUTO_CLEARED` *(async — 60-minute automatic clear of BURST_SUSPENDED state.)*
- `CAK_BURST_CLEARED` *(sync, W1 — Tier 1 explicit-clear ceremony; distinct from auto-clear.)*
- `RESET_WOULD_EXTEND_BURST` *(sync, W1 — advisory-path reset attempt that would re-start the burst window without clearing; rejected.)*

**v1.2 additions — Circuit reset rate (GS10 / IC-CRR-1 / GAP-36):**
- `CIRCUIT_RESET_REJECTED_RATE_EXCEEDED` *(sync, W1 — rate-limit breach N=5 / M=60min; advisory + operator alert.)*

**v1.2 additions — Genesis initiation (GS10 / IC-GIB-1 / GAP-44):**
- `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` *(sync, W1 — genesis initiation attempted while a Dependency Hold remains active from the pre-trip epoch.)*
- `GENESIS_INITIATION_ABUSE_PATTERN` *(aggregate — ≥ 3 blocked initiations in 60 minutes; not W3-eligible per C-W3-1.)*

**v1.2 additions — Hook registry (GS11 / IC-HOOK-BOOT / GAP-54):**
- `HOOK_INTEGRITY_VIOLATION` *(sync, W1 — boot-time hook binary hash mismatch against Tier 2 `hook-registry/v1`.)*

**v1.2 additions — Boot-time rate-limit / retention validation (GS11 / IC-BOOT-RLRF / GAP-46):**
- `RATE_LIMIT_RETENTION_CONFLICT` *(sync, W1 — per-initiator or per-agent rate-limit interval is not strictly less than the minimum retention window for its associated Ledger entry type. Closes T-S7-N1.)*

**v1.2 additions — Scope mismatch aggregate (GS12 / GAP-38):**
- `SCOPE_MISMATCH_AGGREGATE_ALERT` *(sync, W1 — aggregate threshold breached: N mismatches within window M, per Tier 1 `scope_mismatch_aggregate_threshold_n` and `_window_seconds`. Includes contributing-invocation list per IC-AGG-ALERT-LINK.)*
- `SCOPE_MISMATCH_ESCALATED` *(sync, W1 — per-invocation escalation after 2 consecutive `SCOPE_HASH_MISMATCH` errors per A4; routes to human review.)*
- `SCOPE_UPDATE_RATE_EXCEEDED` *(sync, W1 — per-`agent_id` rate-limit breach under `scope_update_min_interval_seconds`; check precedes signature verification per A6 / GS7 GAP-27 / D89.)*
- `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` *(alias — GS10 variant spelling; identical semantics. [COUNCIL-FLAG: two names across source; recommend canonical `SCOPE_UPDATE_RATE_EXCEEDED`.])*

**v1.2 additions — Trust root lost (GS10 / §23.3 / IC-BG-1):**
- `TRUST_ROOT_LOST` *(sync, W1 — terminal double-compromise state declaration; both CAK and break-glass keys compromised. Harness refuses further ceremony acceptance.)*
- `TRUST_ROOT_LOST_ENTERED` *(alias / state-entry marker — may be paired with declaration entry for audit clarity.)*

**v1.2 additions — Reconciliation path (GS5 v3 / IC-SCOPE-RECONCILE):**
- `LEDGER_SIGNATURE_REVERIFICATION_FAILED` *(sync, W3 — tampering detection during post-boot scope-registry reconciliation. Routes through the SECURITY W3 emergency carve-out.)*
- `ORCHESTRATOR_UNAVAILABILITY_ESCALATED` *(sync, W3 — GS5 v3 D102 / IC-TC-RESET-DEGRADED: extended Orchestrator outage during reset ceremony. Narrow W3 carve-out; not W1. C-TC-RESET-DEG-1 through C-TC-RESET-DEG-3.)*

**v1.2 additions — Schema deprecation (GS5 v3 / D98):**
- `SCHEMA_DEPRECATION_ENACTED` *(sync, W1 — records deprecated-type → unified-successor map; historical deprecated entries remain chain-valid per C-DEPREC-1.)*
- `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF` *(sync, W1 — post-cutoff write of a deprecated type; integrity violation per C-DEPREC-2.)*

**v1.2 additions — External document provenance (§26 / GS9 v3 / GAP-11):**
- `LAYER4_MISSING_PROVENANCE` *(sync, W1 — Layer 4 external-source fact submitted without `external_provenance` block; UNRECOVERABLE at patch level per C-EXT-PROV1 / IC-EXT-PROV1.)*

**v1.2 additions — Bounded compensation violation (§11.8.1.1 / A1-REVISED):**
- `BOUNDED_COMPENSATION_VIOLATION` *(sync, W1 — compensation-under-READ_ONLY exceeded its bound per C-CRC-3; carries bound-type and observed-excess fields.)*

**v1.2 additions — Archive-key compromise / mismatch (GS11 / GAP-52):**
- `ARCHIVE_KEY_MATERIAL_MISMATCH` *(sync, W1 — restore-time mismatch between archive-manifest `signer_public_key_material` and Genesis Seal `ARCHIVE_KEY_SEALED` record.)*

### CONSISTENCY category

**v1.0 / v1.1 (preserved):**
- `PREPARED`, `COMMITTED`, `COMPENSATED`, `FAILED`
- `IMMUTABLE_ANCHOR`
- `ANCHOR_ESTABLISHED` (flag on qualifying `COMMITTED` entries)
- `COMPACTION_BEGIN`, `COMPACTION_BOUNDARY`, `COMPACTION_ABORT`
- `COMPACTION_BUNDLE_SEALED`, `SUPERSEDED_BUNDLE_EXPIRED`
- `LEDGER_EPOCH_ARCHIVED`
- `CHAIN_VERIFICATION_RESULT`
- `DEPENDENCY_CONFLICT_FLAGGED`
- `TIMED_OUT` *(sync — PREPARED-state timeout; fields: transaction_id, compensation_direction, trigger; v1.1)*
- `CIRCUIT_TRIPPED` *(sync — circuit breaker trip event; fields: `trip_type {CONSECUTIVE_FAILURE | CROSS_TASK_FAILURE | DIVERGED_STATE}`, `triggering_transaction_id`; v1.1. **v1.2 AMEND per A8:** adds `originating_category` field recording whether the signal that triggered the trip was INTEGRITY, CONSISTENCY, or SECURITY. Reset ceremony (IC-TC-RESET) selects its precondition branch using this annotation.)*
- `RECONCILIATION_COMPLETE` *(sync — full reconciliation run result; field: result {CONSISTENT | DIVERGED}; v1.1)*
- `COMPACTION_ABORTED` *(sync — compaction verification failure; payload: serialized CompactionProbeReport; v1.1)*
- `COMPACTION_PROBE_FAILED` *(sync — Behavioral Probe infrastructure failure during compaction, distinct from COMPACTION_ABORTED; v1.1)*
- `COMPACTION_CORPUS_SMALL` *(async advisory — probe corpus below sampling floor; v1.1)*

**v1.2 additions — Genesis-timeout pairing (GS10 / IC-MON-GTOTM / GAP-30):**
- `GENESIS_TIMED_OUT` *(sync — Genesis initiation exceeded `genesis_prepared_timeout`; triggers circuit-breaker trip in DIVERGED_STATE mode per IC-TC-TIMEOUT.)*
- `GENESIS_TIMEOUT_TRIP_MISSING` *(async, W1 — monitor-pairing check: `GENESIS_TIMED_OUT` observed without paired `CIRCUIT_TRIPPED` within bounded window; C-GTO-1 / C-GTO-2.)*

**v1.2 additions — Hold release / precursor (GS10 / GS11 / GAP-31 / IC-TC-PRECURSOR-QUERY):**
- `DEPENDENCY_HOLD_RELEASE_SIGNED` *(sync — CAK-signed Hold-release ceremony committed; GS5 v3 GAP-21 / D101.)*
- `DEPENDENCY_HOLD_RELEASED_SIGNED` *(alias — GS5/GS10 co-spellings. [COUNCIL-FLAG: both appear in source; recommend canonical `DEPENDENCY_HOLD_RELEASE_SIGNED`.])*
- `HOLD_RELEASE_REASON_UNWARRANTED` *(sync, W1 — operator-cited precursor fails Hold-coverage or audit-window check at admission time; IC-REL-PRECURSOR. W1 per C-W3-1, not W3.)*

**v1.2 additions — Manifest lattice completeness (GS10 / GAP-29a / IC-MANIFEST-1 Check 8):**
- `MANIFEST_LATTICE_INCOMPLETE` *(sync, W1 — manifest-lattice completeness verification failed at ratification.)*
- `MANIFEST_COMMIT_REJECTED` *(sync — pre-commit rejection at manifest submission; GS7 v3 / GAP-20.)*
- `MANIFEST_RATIFICATION` *(sync — successful manifest ratification ceremony; GS7 v3 / GAP-20. [COUNCIL-FLAG: verify placement — this may fit GOVERNANCE more naturally since it is a signed operator ceremony outcome. Kept in CONSISTENCY here pending clarification.])*

**v1.2 additions — Preserved scope binding on 2PC (GS10 / IC-PREPARE-SCOPE / GAP-34):**
- (Field addition, not new entry type) `PREPARED` and `COMMITTED` entries now carry `governing_scope_hash` field, captured at PREPARE and preserved at COMMIT. Nullable for pre-amendment entries.

**v1.2 additions — External document provenance (§26 / IC-EXT-PROV2):**
- `EXTERNAL_PROVENANCE_RECORDED` *(async — Layer 4 external-source patch commit replicating provenance metadata; fields include `patch_id`, `fact_triple_hash`, `ledger_seq`.)*
- `EXTERNAL_PROVENANCE_STALE` *(async advisory — Pruning Agent audit detected source-hash drift.)*
- `EXTERNAL_PROVENANCE_UNAVAILABLE` *(async advisory — Pruning Agent audit could not reach source.)*
- `EXTERNAL_AUDIT_SUSPENDED` *(async — N consecutive network failures in the audit sub-routine; audit paused while Git-side pruning continues per C-EXT-PROV3.)*

**v1.2 additions — Dry-run store (GS8 v2 / GS10 / IC-DRS-1 / IC-DRYRUN-1):**
- `DRY_RUN_ARTIFACT_STORED` *(async — operator-owned `.dry-run-store/` manifest-hash anchor written to Ledger.)*
- `DRY_RUN_ARTIFACT_PRUNED` *(async — retention-driven pruning of dry-run artifact after 37-day minimum.)*
- `DRY_RUN_STALE` *(sync — dry-run artifact older than freshness policy when referenced.)*
- `DRY_RUN_CORPUS_DRIFTED` *(sync — corpus state at dry-run differs from corpus state at submission.)*
- `DRY_RUN_SIGNATURE_INVALID` *(sync — executor signature on dry-run report fails verification.)*
- `DRY_RUN_TIME_CEILING_EXCEEDED` *(sync — time between dry-run and referencing ceremony exceeds ceiling.)*

**v1.2 additions — Write Lock lifecycle (GS10 / GS12 partial):**
- `WRITE_LOCK_VOLUNTARY_RELEASED` *(sync — v2-scope hint; v1.2 records event only for future-proofing. [COUNCIL-FLAG: v2 scope item per §19 — included for forensic completeness if emitted by operator tooling; no v1 code path produces this entry.])*
- `VOLUNTARY_WRITE_LOCK_RELEASE` *(alias form.)*
- `WRITE_LOCK_ABANDONED` *(sync — lock-holder agent abandoned scope; normal liveness recovery.)*

### VALIDATION category

**v1.0 / v1.1 (preserved):**
- Meta-Validator health records *(per-case; v1.1: `health_score` field is `NOT_COMPUTED` when corpus < 20 cases; includes `corpus_staleness_flag` and `corpus_size_at_run`.)*
- Meta-TGA health records *(per-case; same v1.1 extensions as Meta-Validator.)*
- Task gap records *(D37 Step 4.)*
- `CONSTITUTIONAL_FAILURE` *(v1.1 — constitutional test failure. **v1.2 AMEND per A14:** entry now carries a mandatory field pair — `invariant_statement` (copied from test metadata) + `failure_assertion_message` (captured verbatim from runtime). Both fields REQUIRED. No runtime comparison. §25 weak-check pattern.)*

**v1.2 additions — Sandbox / synthetic clock (GS12 / IC-CLK-SANDBOX / GAP-39):**
- `SANDBOX_CONFIG_ERROR` *(sync — constitutional test with `clock_stub_required=true` submitted to a sandbox configuration missing synthetic-clock injection; treated as a configuration error, NOT a test failure.)*

**v1.2 additions — Frozen judge model (GS12 / §21 L2 probe family):**
- `FROZEN_JUDGE_MODEL_BOOTSTRAPPED` *(sync — initial pin of frozen judge model at first boot.)*
- `FROZEN_JUDGE_MODEL_DRIFT_DETECTED` *(async — empirical drift observed against the frozen reference.)*
- `FROZEN_JUDGE_MODEL_WRITE_ATTEMPTED` *(sync, W1 — any attempted write path targeting the frozen judge model; structurally forbidden.)*

**v1.2 additions — Corpus init / staleness (GS8 v3 / D94 / D95):**
- `CORPUS_INIT_STATE` *(sync — Day-0 corpus initialization marker; emitted after the five preconditions pass.)*
- `HEALTH_SCORE_STALE` *(async advisory — corpus older than 180-day enforced floor; Meta-* result records emit companion `corpus_staleness_flag`.)*

**v1.2 additions — Forensic capture (GS10 / GS11):**
- `LEDGER_FORENSIC_EVIDENCE_CAPTURE` *(sync — point-in-time forensic snapshot reference committed to Ledger during incident response.)*
- `VINDEX_FORENSIC_SNAPSHOT_REF` *(sync — `.vindex` overlay snapshot hash paired with forensic-capture entry.)*

### GOVERNANCE category

**v1.0 / v1.1 (preserved):**
- `CONFIG_UPDATE`
- `SEALED_CORPUS_UPDATE`, `SEALED_CORPUS_ACCESS`
- `RECONCILIATION_REVIEW_DECISION`
- `RECONCILIATION_BACKLOG_WARNING`, `RECONCILIATION_BACKLOG_CRITICAL`
- `CIRCUIT_RESET` *(sync — successful circuit breaker write resumption; fields: target_trip_entry_id, operator_id, preconditions_verified; GOVERNANCE category; v1.1. **v1.2:** authorized via CeremonyToken / IC-SCOPE-AUTH-1 per A3.)*
- `SCOPE_UPDATED` *(sync — Write Scope Definition updated; v1.1 fields: previous_scope_hash, new_scope_hash, operator_signature, affected_agent_ids. **v1.2 AMEND per A9:** `ceremony_token_id` replaces standalone `operator_signature` field.)*
- `CORPUS_CASE_ADDED` *(async — corpus case successfully appended; fields: case_id, author_id, corpus_target, new_corpus_size; v1.1)*
- `RETENTION_OVERRIDE_EXTENDED` *(sync — retention period extended; operator-signed; v1.1. v1.2: delegates authorization to IC-SCOPE-AUTH-1 / ceremony_type `RETENTION_EXTEND`. See also `LEDGER_RETENTION_EXTENDED` below.)*

**v1.2 additions — Unified ceremony lifecycle (GS4 / IC-SCOPE-AUTH-1):**
- `CEREMONY_ACCEPTED` *(sync — CeremonyToken admitted; common success marker across all GOVERNANCE-class ceremonies.)*
- `CEREMONY_KEY_ANCHOR` *(sync, W2 bootstrap — initial CAK anchor record; parallel to `ORCHESTRATOR_KEY_ANCHOR`.)*
- `CEREMONY_KEY_ROTATION_COMPLETE` *(sync — successful CAK rotation ceremony; carries previous_key_ref and successor anchor.)*
- `CEREMONY_KEY_ROTATION_OVERDUE` *(sync — 365-day rotation ceiling reached without rotation.)*
- `CEREMONY_KEY_STALE` *(sync — 450-day degraded-mode threshold reached; ceremonies still accepted but each emits this entry.)*
- `CEREMONY_KEY_COMPROMISE_DECLARED` *(sync, W1 — operator declaration via ceremony; triggers defensive posture. Parallel to `CAK_COMPROMISE_DECLARED`.)*
- `CEREMONY_REPLAY_REJECTED` *(deprecated alias — see `CEREMONY_AUTH_REPLAY_REJECTED` in SECURITY; retained for transitional compat.)*
- `CEREMONY_SIGNATURE_INVALID` *(deprecated alias — see `CEREMONY_AUTH_SIGNATURE_INVALID` in SECURITY; retained for transitional compat.)*

**v1.2 additions — Scope-update aggregate advisories (GS12 / GAP-38):**
- `SCOPE_UPDATE_ACCEPTED` *(sync — ceremony admitted successfully; GS5 v3 companion to `SCOPE_UPDATED`.)*
- `SCOPE_UPDATE_AGGREGATE_ADVISORY` *(async — aggregate-volume advisory under threshold.)*
- `SCOPE_UPDATE_AGGREGATE_WARNING` *(sync — aggregate volume approaching `SCOPE_MISMATCH_AGGREGATE_ALERT` threshold.)*

**v1.2 additions — Calibration (§22 / GS7 v3 / GS8 v2):**
- `CALIBRATION_RATIFICATION` *(sync — `larql_fidelity_calibration` artifact ratified via CeremonyToken; new ceremony type.)*

**v1.2 additions — Retention (§27):**
- `LEDGER_RETENTION_EXTENDED` *(sync — Tier 1 authority CAK-signed ceremony; `new_floor_years > old_floor_years` required by construction. Ceremony-type `RETENTION_EXTEND` under IC-SCOPE-AUTH-1.)*
- `LEDGER_ACTIVE_PERIOD_UPDATED` *(sync — Tier 3 operator ceremony updating hot-storage window; reduction permitted within 30-day floor.)*
- `PROJECT_ARCHIVED` *(sync — async-dispatched archive ceremony completed; pairs with manifest per IC-RETENTION2.)*
- `PROJECT_ARCHIVE_PENDING` *(sync — PROJECT_CLOSED committed but archival I/O unavailable; 30-day SLA clock started.)*
- `ARCHIVE_KEY_SEALED` *(sync — archive-signing key material sealed at Genesis Seal during initial setup; cross-check anchor for restore path per GAP-52.)*

**v1.2 additions — Retention pruning (GS10 / IC-RP-1 / GAP-47):**
- `RETENTION_PRUNING` *(sync — retention-pruning ceremony under `artifact_retention_manager` role; new ceremony type.)*

**v1.2 additions — Legacy extension grant (GS7 v3 / GAP-20):**
- `LEGACY_EXTENSION_GRANTED` *(sync — operator grant extending legacy-larql-version support window; Tier 3 governance decision.)*

**v1.2 additions — Stale-fact refresh (GS13 / IC-SFR-1 / OQ-SC3 resolution):**
- `STALE_FACT_REFRESH_REQUESTED` *(sync — Pruning Agent initiates refresh ceremony upon detecting `EXTERNAL_PROVENANCE_STALE`. CORE-tier facts automatically attach `REQUIRES_HUMAN_REVIEW` flag per C-SFR-4.)*
- `STALE_FACT_REFRESH_APPROVED` *(sync — operator approval via Reconciliation Review Queue; dispatches Coder Agent with refresh scope.)*
- `STALE_FACT_REFRESH_REJECTED` *(sync — operator declines refresh; fact remains STALE with advisory flag per D101.)*
- `STALE_FACT_REFRESH_DEFERRED` *(sync — operator defers decision with reason; no action taken; fact remains STALE.)*

**v1.2 additions — Operator identity / recovery (GS11 / IC-CAK-IDENTITY):**
- `OPERATOR_IDENTITY_REGISTERED` *(sync — stable external `operator_id` bound at first-boot CAK registration; carried unchanged across rotation. Closes T-S4-N1.)*
- `OPERATOR_RECOVERY_ACTION_LOGGED` *(sync — recovery-ceremony metadata record for post-incident audit.)*

**v1.2 additions — Genesis review (GS7 v3):**
- `GENESIS_REVIEW_DECISION_AI` *(sync — Architect Agent's drafted manifest review outcome; non-authoritative informational record, does not grant ratification authority per D-GAP1-B.)*

**v1.2 additions — Break-glass (GS10 / §23.3 / IC-BG-1):**
- `BREAK_GLASS_ACTIVATED` *(sync, W1 — break-glass channel single-purpose `CAK_ROTATION_EMERGENCY` ceremony committed via the second Tier 1 anchor and M ≥ 3 quorum.)*
- `CAK_ROTATION_EMERGENCY` *(sync — completion record of the emergency CAK rotation; pair with `BREAK_GLASS_ACTIVATED`.)*

**v1.2 additions — OOK lifecycle (GS11 / GS12):**
- `OOK_ROTATED` *(sync — Orchestrator Operator Key rotation completion. [COUNCIL-FLAG: source material shows this emitted from both GOVERNANCE and LIFECYCLE contexts; placed in GOVERNANCE here to pair with the CAK-rotation entries; if implementation treats it as pure lifecycle, move to LIFECYCLE category.])*

### LIFECYCLE category

**v1.0 / v1.1 (preserved):**
- `TASK_DECOMPOSED`
- `DEPENDENCY_HOLD_PLACED`, `_RENEWED`, `_RELEASED`, `_EXPIRED_UNCLAIMED`
- Scope Lock entries
- Compaction scheduling events
- `PROJECT_INITIATED` *(sync, W2 bootstrap — retention policy declaration, mint-once; fields: default_retention_policy, operator_signature; v1.1)*
- `PROJECT_CLOSED` *(sync — final epoch sealed, Ledger made read-only; v1.1 fields: operator_signature, final_epoch_id, archival_status {COMPLETE | PENDING}. **v1.2 AMEND per §27.4:** authorization delegated to IC-SCOPE-AUTH-1 ceremony_type `PROJECT_CLOSE`; paired atomically with `FINAL_STATE_SNAPSHOT` per IC-RETENTION1; archival dispatched asynchronously — `archival_status=COMPLETE` or `PENDING` reflects archive-ceremony outcome only after async completion, not at the moment of PROJECT_CLOSED commit.)*

**v1.2 additions — Final state snapshot (§27.4 / IC-RETENTION1):**
- `FINAL_STATE_SNAPSHOT` *(sync — carries Ledger chain tip hash and `.vindex` snapshot hash at close; atomic pair with `PROJECT_CLOSED`.)*

**v1.2 additions — Archive SLA (§27.4):**
- `PROJECT_ARCHIVE_SLA_BREACHED` *(sync, W1 — 30-day default SLA for resolving `PROJECT_ARCHIVE_PENDING` expired without `PROJECT_ARCHIVED` emission. [COUNCIL-FLAG: §27.4 text places this as LIFECYCLE sync W1; if the intended semantic is a governance/operational-incident record, consider GOVERNANCE category. Kept as LIFECYCLE per §27.4 verbatim.])*

**v1.2 additions — Genesis initiation ceremony (GS10):**
- `GENESIS_INITIATION` *(sync — Genesis initiation ceremony committed; distinct from Genesis Seal event.)*

**v1.2 additions — Expired-author advisory flag (§24.2 / A13):**
- `EXPIRED_AUTHOR_PRESENT` *(flag on Meta-* Ledger result record — not a standalone entry type. Additive to existing Meta-* health-record entries per A13.)*

### Deprecated in v1.2 (per A7b — unified-failure-set collapse)

The following v1.1 entry types are DEPRECATED and replaced by their unified-CeremonyToken counterparts in the SECURITY category. Historical entries of these types remain chain-valid forever (C-DEPREC-1). Post-cutoff writes are integrity violations per C-DEPREC-2 and emit `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF`. Audit tools map deprecated entries to unified successors per C-DEPREC-3.

- `HOLD_RELEASE_SIGNATURE_INVALID` *(DEPRECATED; successor: `CEREMONY_AUTH_SIGNATURE_INVALID`.)*
- `HOLD_RELEASE_REPLAY_REJECTED` *(DEPRECATED; successor: `CEREMONY_AUTH_REPLAY_REJECTED`.)*

### Catalog scope notes

- **Running total:** The v1.2 catalog contains all v1.1 entries plus 50+ v1.2 additions spanning CeremonyToken failure modes (10), CAK lifecycle and burst state (8), hook / rate-limit / archive-key integrity (4), genesis-initiation blocking (2), scope-mismatch aggregate and rate (5), trust-root-lost (2), reconciliation-path failures (2), dry-run artifact lifecycle (6), manifest lattice and commit (3), provenance and staleness (4 + 4 refresh), retention governance (5), break-glass (2), deprecation machinery (2), calibration and legacy extension (2), and several miscellaneous operator / forensic entries.
- **Alias register.** Several entries have variant spellings across session sources (`DEPENDENCY_HOLD_RELEASE_SIGNED` vs. `DEPENDENCY_HOLD_RELEASED_SIGNED`; `CAK_BURST_LIMIT_EXCEEDED` vs. `CAK_CEREMONY_BURST_EXCEEDED`; `SCOPE_UPDATE_RATE_EXCEEDED` vs. `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED`). Aliases are marked inline with [COUNCIL-FLAG] and recommended canonical names are noted. Implementation should pick one per pair and retire the other; aliases are documentation-only, not separate types.
- **Not catalogued here:** per-entry field schemas (JSON-schema-level). Those are documented inline with the interface contracts in Appendix B or in the source gap-session summaries. This catalog enumerates entry TYPES and their category placement only.

## Appendix D — Directory Layout

```
<harness_root>/                         # Machine-local, NOT Git-tracked
  .state-ledger/
    ledger.jsonl                        # Merkle-chain Unified Ledger
    wal/                                # Async write-ahead log
    archive/{epoch_bundle_N}/           # v1.1 Ledger epoch cold storage
  .ledger-archive/                      # v1.2 addition — canonical archive per IC-RETENTION2
    {archive_id}/
      archive-manifest.json             # signed manifest (ledger-archive/v1)
      payload.zst                       # zstd-compressed Ledger entries
  .sealed-corpora/                      # Tier 2 — human-signed sealed artifacts
    meta-validator-suite/
      manifest.json
      v1/ v2/ ... vN/
    meta-tga-corpus/
      manifest.json
      v1/ v2/ ... vN/
    constitutional-suite/
      manifest.json
      v1/ v2/ ... vN/
    write-scope-definitions/
      manifest.json
      v1/ v2/ ... vN/
    reconciliation-reviewers/
      manifest.json
      v1/ v2/ ... vN/
    corpus-author-registry/             # v1.2 addition (GAP-8 / v3 GS8)
      manifest.json
      v1/ v2/ ... vN/
    hook-registry/                      # v1.2 addition (GAP-54 / GS11)
      v1/
        manifest.json                   # per-hook binary hash registry
  .orchestrator-key/                    # Private key material (permission-protected)
  .dry-run-store/                       # v1.2 addition (GAP-33) — operator-owned
    {dry_run_id}/
      report.json                       # dry-run artifact; 37-day min retention
  .larql-archive/
    active/                             # Active .larql patches
    superseded/{epoch_bundle_N}/        # Compaction-epoch bundles

<repo_root>/                            # Git-tracked project repository
  .harness/                             # Tier 3 — Anchored Git Config
    genesis-seal.json                   # Tier 1 secondary copy
                                        #   (includes ceremony_authorization_key_anchor,
                                        #   break_glass_key_anchor,
                                        #   corpus_author_bootstrap_identity,
                                        #   larql_epsilon_table, ledger_retention_floor,
                                        #   scope_mismatch_aggregate_threshold_n,
                                        #   scope_mismatch_aggregate_window_seconds)
    orchestrator-key-anchor.json        # Tier 1 secondary copy (public half)
    path-classification.json
    rate-limits.json                    # v1.2 addition (GAP-27)
                                        #   scope_update_min_interval_seconds
                                        #   per-CAK and per-ceremony-type rate params
                                        #   ledger_active_period (≥ 30d)
    larql-migration-manifest.json       # Tier 1-governed; referenced by genesis-seal
    agent-yamls/
      architect.yaml
      coder.yaml
      pruning.yaml
      tga.yaml
      validator.yaml
  src/
  tests/
  ...

<harness_release>/                      # v1.2 addition — per-operator compiled binary
  harness.bin                           # embeds operator_root_public_key (C-BOOT-5)
  boot_manifest.json                    # signed by operator root key (IC-BOOT-1)
```

Notes:
- `.vindex/` is an internal-to-harness layout managed by the Write Engine (not shown — see §8.4).
- `corpus-author-registry/` and `hook-registry/v1/` are the sixth and seventh Tier 2 sealed corpora (Appendix E).
- `.dry-run-store/` is operator-owned per T-S-RP-1; Warden audit is metadata-only (IC-DRS-1).
- `.ledger-archive/` supersedes `.state-ledger/archive/` as the canonical archive location for v1.2 (IC-RETENTION2). Operators upgrading from v1.1 retain the legacy path read-compatibility but all new archives land at `.ledger-archive/`.
- Per-operator harness binary distribution (GAP-57 / OQ-PATH-DEPLOY) is an operator-side concern; v1.2 documents the precondition but does not prescribe distribution mechanics.

## Appendix E — Sealed Corpora Inventory

Seven Tier 2 sealed corpora in v1.2 (five from v1.1 + `corpus-author-registry/` GAP-8 + `hook-registry/v1/` GAP-54):

| Corpus | Purpose | Access Pattern | Minimum Viable Size | Retention |
|---|---|---|---|---|
| `meta-validator-suite/` | Held-out cases for Meta-Validator | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `meta-tga-corpus/` | Held-out `(spec, gold_tests)` for Meta-TGA | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `constitutional-suite/` | Architectural invariant tests | Validator persistent read | No minimum specced | Permanent additive versioning |
| `write-scope-definitions/` | Per-agent write authority | Authorization Gate persistent read | n/a | Permanent additive versioning |
| `reconciliation-reviewers/` | Authorized reviewer list for Reconciliation Queue | Gate read on reviewer verification | n/a | Permanent additive versioning |
| `corpus-author-registry/` | Authoritative list of identities authorized to submit cases to Meta-* corpora (GAP-8) | IC-SL7 token issuance; §24 submission ingress; boot-time verification | ≥ 1 identity (the bootstrap identity from `corpus_author_bootstrap_identity`) | Permanent additive versioning |
| `hook-registry/v1/` | Boot-time + runtime hook binary hash registry (GAP-54) | Boot sequence IC-HOOK-BOOT; any hook-reload ceremony | No minimum specced | Permanent additive versioning |

All seven follow identical storage, signing, dual-store, and boot-verification mechanics.

## Appendix F — Tension Map Summary (v2 State)

Summary of the cross-domain tension register as of v1.2 sealing. Pulled verbatim from `tension-map-v5.md`. All 25 tension IDs are listed with their current disposition. 23 of 25 are ✅ Resolved or 📋 Accepted; 2 remain (T15 partial; T16 v2-deferred) and are the sole reason the spec carries an "all tensions accounted for" rather than "all tensions closed" status line.

### Resolution notation

- ✅ **Resolved** — addressed by a ratified decision, interface contract, or spec block. No further action pending.
- 📋 **Accepted** — acknowledged as a design tradeoff or operator-owned concern; no spec-level remediation. Documented for operator awareness.
- 🔶 **Partial** — v1 mitigation in place; full resolution deferred to v2.
- 🔴 **v2** — v1 outlines only; resolution is v2 scope.

### Full map

| ID | Name | Specialists | Status | Where resolved |
|----|------|-------------|--------|----------------|
| T1–T12 | Session 7 integration tensions | Various | ✅ Resolved | v1.1 spec, preserved in v1.2 |
| T13 | Advisory Boundedness vs. Operational Flexibility | MEMIT + Orchestration | ✅ Resolved | GS7 v3 |
| T14 | Single-Key vs. Dual-Key for Ceremony Authorization | Warden + Orchestration | ✅ Resolved | GS4 v2/v3 (D-GAP4-A, IC-SCOPE-AUTH-1) |
| T15 | CAK Availability vs. Ceremony Urgency | Warden + Orchestration | 🔶 Partial | GS13 v2 path; A11 v1 deployment guidance; GAP-42 break-glass partial mitigation |
| T16 | Ceremony-Scope Narrowness vs. Operational Batching | Warden + SCT | 🔴 v2 | GS13 outline; per-Hold path v1-specced |
| T-SC-W-1 | Audit Category vs. Lifecycle for Hold Release | SCT + Warden | ✅ Resolved | GS5 v3 |
| T-SC-W-2 | Write Suspension vs. Governance-Ceremony Write | SCT + Warden | ✅ Resolved | GS10 (§11.8.1, IC-GCO-1) |
| T-S3-N1 | Ledger Ordering Underpins D87 | Warden + SCT | ✅ Resolved | GS5 v3 |
| T-S3-N2 | Push-Based Invalidation Channel | Warden + Orchestration | ✅ Resolved | GS9 v3 (D111) |
| T-S4-1 | Audit Completeness Under Roster Indirection | Warden + Validation | 📋 Absorbed | — |
| T-S4-2 | Roster State at Snapshot Boundaries | SCT + Validation | ✅ Resolved | — |
| T-S4-3 | Two-Signature Ceremony Latency for Promotion | Orchestration + Validation | 📋 v2 concern | — |
| T-Candidate-GS7 | Dry-Run Freshness vs. Authorship Lifecycle | MEMIT + Graph | ✅ Resolved | D-GS8-D |
| T13-v1-GS1 | Manifest Signing Ownership (local) | MEMIT + Warden | ✅ Resolved | GS7 v3 |
| T14-v1-GS1 | Deprecation Timing vs. Compaction Cadence (local) | MEMIT + SCT | ✅ Resolved | GS7 v3 |
| T-S4-N1 | Rotation Registry Ordering | Warden + SCT | ✅ Resolved | GS11 (IC-CAK-IDENTITY) |
| T-S4-N2 | Bootstrap-Tool Trust Asymmetry | Warden + Orchestration | 📋 Acknowledged | GAP-40 resolved; residual accepted |
| T-S7-N1 | Rate-Limit State Derived vs. Primary | Warden + SCT | ✅ Resolved | GS11 (IC-BOOT-RLRF, §13.5 step 5a) |
| T-PM-vs-PA | Provenance Monitor vs. Pruning Agent Advisory | SCT + Warden | ✅ Resolved | GS11 (IC-REVIEW-QUEUE amended, §15.1) |
| T-TGA-load | TGA Authority Concentration | Validation | ✅ Accepted for v1 | GS12 (D32/D33 acknowledged; v2-reconsider flagged) |
| T-BT | Bounded Tunability Latent Tension | Various | 📋 v2 planning | — |
| T-NOTIFY-LOSS | Notification Loss Failure Mode | SCT + Orchestration | 📋 Accepted tradeoff | D111 one-attempt-before-TTL boundary |
| T-v2GS6-CEREMONY-DECOMP | Ceremony Atomicity vs. Decomposition | SCT + Warden | 📋 Framework axis | — |
| T-W-BG-1 | Break-Glass Friction vs. Incident Urgency | Warden | 📋 Accepted | GS10 — deliberate security property; A11 precondition |
| T-S-RP-1 | Dry-Run Store Ownership vs. Warden Immutability | Warden + SCT | 📋 Accepted for v1 | GS10 — IC-DRS-1 metadata-only audit; v2-flagged |

### Tensions requiring action beyond v1.2

Two remain:

**T15 (CAK Availability vs. Ceremony Urgency).** Partial in v1.2: A11 deployment-precondition text requires operators to pre-arrange break-glass custodians before declaring harness operational. GAP-42 (break-glass channel) provides a v1 mitigation path for the full CAK-loss scenario. Full resolution (m-of-n CAK with operational-latency budget) is v2 scope per OQ-S-CAK-2.

**T16 (Ceremony-Scope Narrowness vs. Operational Batching).** v2-scope. v1.2 ships with per-Hold ceremony scope. Batch-release path (GS13 outline) is documented but not specced. No v1.2 operator action required; operators accepting per-Hold-ceremony operational cost are fully supported.

All other tensions are either resolved (✅), accepted by explicit design decision (📋), or absorbed into later architecture (✅ / 📋 absorbed). No High-priority tension remains unaddressed in the v1.2 cross-domain register.

---

## Appendix G — Amendment Application Record (A1-REVISED, A2–A14)

Record of every ratified amendment applied in v1.2. Each amendment carries a section pointer to where it is applied in the spec body, the session in which it was ratified, and a one-line summary of the amendment's effect.

| Amendment | Ratified in | Applied at | Summary of effect |
|---|---|---|---|
| **A1-REVISED** | GS10 | §11.8.1.1 (new subsection); C-CRC-3 | Bounded compensation under READ_ONLY mode — the original A1 compensation-suspension rule is amended to permit narrowly-bounded compensation writes during READ_ONLY, with the bound defined by C-CRC-3. Resolves the v1.1 deadlock where a transaction held under CIRCUIT_TRIPPED could not compensate and could not abort. `BOUNDED_COMPENSATION_VIOLATION` Ledger entry added when the bound is exceeded. |
| **A2** | GS10 | §11.8.1 (revised text); GAP-35 | `CIRCUIT_RESET_REJECTED` field semantics clarified — structured precondition-unmet reason code required. Non-consumed CeremonyToken invariant: a token rejected at precondition check is NOT consumed (the ceremony never admitted), distinct from a token that admits and then fails. |
| **A3** | GS4 v2; finalized GS10 | §11.8.1 (IC-TC-RESET); §14.x (ceremony authorization); §20 | IC-TC-RESET placeholder populated. Reset ceremony is CAK-authorized via IC-SCOPE-AUTH-1 (CeremonyToken envelope). CAK-authorization is necessary-but-not-sufficient — the Transaction Controller's independent precondition verification remains. |
| **A4** | GS12 | §14.3 (SCOPE_HASH_MISMATCH handling) | Per-invocation `SCOPE_HASH_MISMATCH` escalation threshold lowered from 3 consecutive errors (v1.1) to **2 consecutive errors** (v1.2). Addresses Warden concern that a three-attempt oracle window was too permissive. `SCOPE_MISMATCH_ESCALATED` Ledger entry added. |
| **A5** | GS4 v2 | §10.9; IC-SCOPE-UPDATE | CAK verification precedes SCOPE_UPDATED Ledger write. No SCOPE_UPDATED entry is produced by a failed authorization. Orders the write side of the ceremony admission chain. |
| **A6** | GS4 v2; finalized GS7 v3 | §10.9; IC-SCOPE-UPDATE admission order; GAP-27 / D89 (scope_update_min_interval_seconds) | Rate-limit check precedes signature verification. Eliminates signature-oracle attack surface — an attacker cannot force expensive crypto work simply by sending ceremony requests faster than the rate window. Applies to all ceremony types under IC-SCOPE-AUTH-1. |
| **A7** | GS5 v3 / GS10 | Appendix C — deprecated-entries block | Schema deprecation machinery introduced. Historical deprecated entries remain chain-valid forever (C-DEPREC-1); post-cutoff writes are integrity violations (C-DEPREC-2); audit tools map deprecated entries to unified successors (C-DEPREC-3). `SCHEMA_DEPRECATION_ENACTED` and `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF` entries added. |
| **A7b** | GS5 v3 / GS10 | Appendix C — deprecation markers on `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` | Two specific v1.1 entry types deprecated and replaced by unified CeremonyToken failure-set entries (`CEREMONY_AUTH_SIGNATURE_INVALID`, `CEREMONY_AUTH_REPLAY_REJECTED`). Concrete application of A7's deprecation machinery. |
| **A8** | GS10 | §11.8 (circuit-breaker trip); Appendix C `CIRCUIT_TRIPPED` entry amendment | Cross-category trip-reason annotation. Every `CIRCUIT_TRIPPED` entry now records `originating_category ∈ {INTEGRITY, CONSISTENCY, SECURITY}` so that the reset ceremony (IC-TC-RESET) can select its precondition branch from the correct provenance context. Resolves the v1.1 ambiguity where trip provenance was inferable but not attested. |
| **A9** | GS4 v2 | §10.9; IC-SCOPE-UPDATE payload | `ceremony_token_id` field replaces the v1.1 standalone `operator_signature` field on SCOPE_UPDATED entries. Signatures are nested within the CeremonyToken envelope (IC-SCOPE-AUTH-1) rather than flat fields on the domain entry. |
| **A10** | GS4 v2 | §13.2 (genesis-seal.json); §20.3 (CAK anchor) | `ceremony_authorization_key_anchor` added to Tier 1 `genesis-seal.json`. This is the public-key anchor against which every CeremonyToken envelope signature is verified. Mint-once at Genesis. A separate `break_glass_key_anchor` is added as the second Tier 1 anchor per §23.3. |
| **A11** | GS10 / GS13 | Appendix A — Deployment Preconditions | v1 CAK backup-custodian pre-arrangement requirement. Operator MUST pre-arrange M ≥ 3 break-glass custodians BEFORE declaring the harness operational. Without pre-arranged custodians, a post-deployment CAK compromise has no recovery path short of Genesis re-initialization. Partial mitigation for T15; full resolution v2. |
| **A12** | GS9 v2 | §24.2 (Point 1); IC-CORPUS-AUTH amendment | `expires_at` predicate added to corpus author registry at submission ingress. An expired author identity cannot submit new cases. `CORPUS_WRITE_REJECTED` with reason code `AUTHOR_EXPIRED` is the enforcement record. |
| **A13** | GS9 v2 | §24.2 (Point 2); IC-SL7 amendment | `contains_expired_author_cases` response field added to IC-SL7 Meta-* token issuance. When the active corpus contains cases authored by an expired identity, the token is still issued but the Meta-* run completes in advisory posture with the `EXPIRED_AUTHOR_PRESENT` flag on the Ledger result record. No mid-run revocation. |
| **A14** | GS9 v2 / GS8 v3 residual | §25.2; Appendix C `CONSTITUTIONAL_FAILURE` amendment | Q5 weak-check field pair. Every `CONSTITUTIONAL_FAILURE` entry now carries both `invariant_statement` (from test metadata) and `failure_assertion_message` (captured verbatim from runtime). Fields are co-recorded, not compared at runtime. Operator audit query surfaces divergences. Preserves determinism requirement of D97 Q5. |

### Amendment ordering and precedence

Amendments apply in declaration order unless an amendment explicitly supersedes a prior one. A1 → A1-REVISED is the only supersession in the v1.2 set: A1 (v1.1 original) is fully replaced by A1-REVISED per GS10. A2 through A14 are strictly additive to their respective anchor sections.

No amendment in v1.2 reverses a v1.1 decision or removes a v1.1 interface contract. All v1.2 amendments are either additive or clarifying. Two v1.1 Ledger entry types are deprecated under A7b; deprecation is additive (historical entries remain chain-valid) and is the only "removal" in v1.2.

### Amendment ratification provenance

- **GS4 v2:** A3 (initial), A5, A6 (initial), A9, A10. IC-SCOPE-AUTH-1 infrastructure.
- **GS5 v3:** A7, A7b (initial — deprecation machinery).
- **GS7 v3:** A6 (finalized with GAP-27 / D89).
- **GS9 v2:** A12, A13, A14.
- **GS10:** A1-REVISED, A2, A3 (finalized), A7/A7b (finalized with migration tooling), A8, A11 (initial).
- **GS11:** (no new amendments; ratification and integration session.)
- **GS12:** A4.
- **GS13:** A11 (finalized as Appendix A precondition text).

---

## Appendix H — D-Number Collision Register (D89–D103)

Parallel v1 / v2 / v3 gap-session tracks assigned D-numbers independently for local decisions, producing collisions in the D89–D103 range. This appendix registers every such D-number so that downstream readers can disambiguate. v1.2 citation style for any D-number in this range uses **session reference + content description** rather than bare D-number to eliminate ambiguity.

### Convention

- **Baseline v1.1:** D1 through D80 were assigned during the seven-session Council arc (Schema through Integration) and are unique by construction.
- **v1.1 IC Review Session:** D81 through D90 were assigned during the v1.1 Interface Contract Review; these are authoritative v1.1 decisions.
- **Phase 2 gap sessions:** GS4 through GS13 on parallel v2 and v3 tracks reused the D89+ range for local decisions before the collision pattern was detected. The register below records every local assignment.

### Register

| D-Number | Source | Content Summary | Disambiguation Key |
|---|---|---|---|
| **D81** | v1.1 IC Review | Gate pre-check #8 — `larql_syntax_version` header validation. IC-GATE-8, C-GATE-1. | `v1.1-D81 — Gate version check` |
| **D82** | v1.1 IC Review | Versioning semantics — forward/backward/legacy policy. | `v1.1-D82 — versioning semantics` |
| **D83** | v1.1 IC Review | Write Engine drift_state object. IC-WE-1, C-WE-1. | `v1.1-D83 — IC-WE-1 drift state` |
| **D84** | v1.1 IC Review | Circuit breaker reset ceremony. IC-TC-RESET. | `v1.1-D84 — IC-TC-RESET baseline` |
| **D85** | v1.1 IC Review | Two-value timeout model. IC-TC-TIMEOUT, C-GATE-2. | `v1.1-D85 — IC-TC-TIMEOUT` |
| **D86** | v1.1 IC Review | Compaction probe stratified sampling. IC-OC-PROBE, C-OC3. | `v1.1-D86 — IC-OC-PROBE` |
| **D87** | v1.1 IC Review | Scope update ceremony. IC-SCOPE-UPDATE baseline. | `v1.1-D87 — IC-SCOPE-UPDATE baseline` |
| **D88** | v1.1 IC Review | Corpus author interface. IC-CORPUS-AUTH baseline. | `v1.1-D88 — IC-CORPUS-AUTH baseline` |
| **D89** *(v1.1)* | v1.1 IC Review | Retention lifecycle — IC-LDG-RETAIN baseline. Archival format "1.0". | `v1.1-D89 — IC-LDG-RETAIN baseline` |
| **D89** *(v3 GS7)* | GAP-27 ratification (GS7 v3) | `scope_update_min_interval_seconds` Tier 1 field; rate-limit-precedes-signature ordering. | `GS7-v3-D89 — SCOPE_UPDATED rate limit` |
| **D90** *(v1.1)* | v1.1 IC Review | Content classification mixed — IC-GATE-9 structured rejection with split_guidance. | `v1.1-D90 — IC-GATE-9` |
| **D90** *(GS3 reference in GS4 v2)* | GS3 / GS4 v2 | Scope update ceremony internal reference (per GS4 v2 §"Ceremony types in unified scope"). | `GS4-v2-D90-ref — scope update ceremony` |
| **D91** | GS3 (origin) / ratified GS9 v3 as D111 | Best-effort scope-update notification; at-least-one-attempt-before-TTL. Final TTL = 60s (Tier 3, 10s Tier 1 floor). Agent responsibility reaffirmed — notification is a performance hint, not a safety mechanism. | `GS9-v3-D111 — D91 ratification (scope notification TTL)` |
| **D92** | GS4 CeremonyToken model (informal attribution via GS8 v2) | Component of the CeremonyToken model (envelope structure — precise scoping per GS8 v2 reference "D92–D96 CeremonyToken model"). [COUNCIL-FLAG: D92 is not labeled as a formal decision in GS4 v2; attribution is indirect via downstream citation. Session reference + content description is the authoritative disambiguator.] | `GS4-v2-CeremonyToken-envelope (informal D92)` |
| **D93** *(v3 GS8)* | GS8 v3 | Corpus author registry adopted — Tier 2 `corpus-author-registry/`; Tier 1 narrowed to `corpus_author_bootstrap_identity`. | `GS8-v3-D93 — corpus-author-registry` |
| **D94** | GS8 v3 | Meta-* corpus extension cadence — 90-day advisory / 180-day enforced (`HEALTH_SCORE_STALE`). | `GS8-v3-D94 — corpus cadence tiers` |
| **D95** | GS8 v3 | Five Day-0 deployment preconditions for corpus initialization; `CORPUS_INIT_STATE` Ledger entry. | `GS8-v3-D95 — corpus init preconditions` |
| **D96** | GS8 v3 | Dual-signal constitutional test tagging (directory + module markers). | `GS8-v3-D96 — constitutional test tagging` |
| **D97** | GS8 v3 | Five qualification criteria Q1–Q5 for constitutional test promotion. | `GS8-v3-D97 — Q1–Q5 qualification` |
| **D98** *(v3 GS8)* | GS8 v3 | Constitutional test promotion via standard Tier 2 versioned additive pattern; single-operator signature in v1.1; qualification attestation block. | `GS8-v3-D98 — promotion ceremony` |
| **D98** *(v3 GS5)* | GS5 v3 | `SCHEMA_DEPRECATION_ENACTED` Ledger entry + C-DEPREC-1/2/3. A7 application. | `GS5-v3-D98 — schema deprecation machinery` |
| **D99** *(v2 GS9)* | GS9 v2 | Corpus author registry expiry — two-point enforcement; no mid-run revocation. GAP-8 residual close. | `GS9-v2-D99 — corpus author expiry` |
| **D99** *(v3 GS9)* | GS9 v3 | Layer 4 external document provenance tracking — mandatory `external_provenance` block. GAP-11 core decision. | `GS9-v3-D99 — external provenance tracking` |
| **D100** *(v2 GS9)* | GS9 v2 | Q5 weak-check — `CONSTITUTIONAL_FAILURE` field pair (`invariant_statement` + `failure_assertion_message`). A14. | `GS9-v2-D100 — Q5 weak-check` |
| **D100** *(v3 GS9)* | GS9 v3 | Provenance-record storage: two locations (patch metadata + Ledger entry `EXTERNAL_PROVENANCE_RECORDED`). | `GS9-v3-D100 — provenance storage` |
| **D101** *(v3 GS5)* | GS5 v3 | `DEPENDENCY_HOLD_RELEASED_SIGNED` formalized as GOVERNANCE/sync Appendix C entry with CeremonyToken integration. release_reason enum finalized as 4-value closed set. GAP-21. | `GS5-v3-D101 — HOLD_RELEASE_SIGNED formalization` |
| **D101** *(v3 GS9)* | GS9 v3 | Staleness is advisory, never blocking, at detection time. Three-state model FRESH/STALE/UNAVAILABLE. No auto-rewrite of Layer 4 facts. | `GS9-v3-D101 — staleness advisory` |
| **D102** *(v3 GS5)* | GS5 v3 | Degraded Orchestrator during reset ceremony — stratified response; narrow W3 carve-out; IC-TC-RESET-DEGRADED. GAP-24. | `GS5-v3-D102 — orchestrator degraded reset` |
| **D102** *(v3 GS9)* | GS9 v3 | Pruning Agent `external_source_audit` sub-routine. Cadence, per-fact override, `EXTERNAL_AUDIT_SUSPENDED` isolation. | `GS9-v3-D102 — pruning audit sub-routine` |
| **D103** *(v3 GS5)* | GS5 v3 | Scope Registry Reconciliation path — post-boot Orchestrator phase; signature reverification against current CAK anchor. IC-SCOPE-RECONCILE. GAP-25. | `GS5-v3-D103 — scope reconciliation` |
| **D103** *(v3 GS9)* | GS9 v3 | Two-tier Ledger retention governance — Tier 1 `ledger_retention_floor` (immutable-downward, 7y default) + Tier 3 `ledger_active_period` (90d default, 30d floor). | `GS9-v3-D103 — retention tiers` |

### Beyond the collision range

D104–D111 are unique to GS9 v3 and do not collide with parallel-track assignments. They are listed for completeness of the retention / consistency-parameters cluster:

| D-Number | Source | Content Summary |
|---|---|---|
| **D104** | GS9 v3 | Archive format `ledger-archive/v1` — zstd compression, SHA-256 per-entry, Merkle root, chain-link anchors. GAP-12. |
| **D105** | GS9 v3 | `PROJECT_CLOSED` synchronous + async archival; `FINAL_STATE_SNAPSHOT` atomic pair; `PROJECT_ARCHIVE_PENDING` / `PROJECT_ARCHIVED` / `PROJECT_ARCHIVE_SLA_BREACHED`. IC-RETENTION1. |
| **D106** | GS9 v3 | WAL flush policy — two-mode, keyed to fact importance class. GAP-14 core. |
| **D107** | GS9 v3 | Light Ledger chain verification at every 100 entries (retained from v1.1). |
| **D108** | GS9 v3 | Full Ledger chain verification at 10,000 entries OR 24 hours; audit-mode. |
| **D109** | GS9 v3 | Async threshold out-of-band sync SLA made explicit. |
| **D110** | GS9 v3 | All thresholds in this cluster are Tier 3 tunable with Tier 1 floor. |
| **D111** | GS9 v3 | D91 ratified final — scope-update notification at-least-one-attempt-before-TTL; 60s default TTL; Tier 3 tunable / 10s Tier 1 floor. |

### Citation guidance for downstream documents

When citing any D-number in the D89–D103 collision range, use one of the following forms:

1. **Session-qualified:** `GS9-v3-D99` or `GS9-v2-D99` — unambiguous.
2. **Content-qualified:** `D99 (external provenance tracking)` or `D99 (corpus author expiry)` — unambiguous.
3. **Both:** `GS9-v3-D99 (external provenance tracking)` — unambiguous and redundantly safe.

Avoid bare `D99`, `D100`, `D101`, `D102`, `D103`, `D90`, `D89` in cross-document references. Within a single session summary, bare D-numbers are fine because the session context resolves ambiguity.

---

## Appendix I — Inconsistency Flag List (INCON-N)

This appendix records any inconsistencies detected during final v1.2 spec assembly that were not resolved during the gap-session arc. Each flag is a candidate for a targeted follow-on session. Absence of a flag in this list indicates the corresponding area was either resolved inline or not detected during assembly.

### Status: **ASSEMBLY CLEAN WITH ADVISORY NOTES**

No blocking inconsistencies were identified during v1.2 assembly. Four advisory notes are recorded below for operator and future-council awareness. None of the advisories alters a ratified decision, constraint, or interface contract — each is a cosmetic or documentation-hygiene concern raised by cross-referencing session sources.

### Advisory notes

**INCON-v12-A01 — Ledger entry name aliases across sources.**
Three entry-type pairs exist with variant spellings in session summaries:
- `DEPENDENCY_HOLD_RELEASE_SIGNED` vs. `DEPENDENCY_HOLD_RELEASED_SIGNED` (GS5 v3 / GS10 co-usage)
- `CAK_BURST_LIMIT_EXCEEDED` vs. `CAK_CEREMONY_BURST_EXCEEDED` (GS10 co-usage)
- `SCOPE_UPDATE_RATE_EXCEEDED` vs. `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` (GS7 v3 / GS10 co-usage)

**Disposition:** Appendix C records both forms with [COUNCIL-FLAG] markers and names the recommended canonical form for each pair. Implementation should pick one per pair and treat the other as not emitted. Advisory only; does not affect correctness, Ledger integrity, or any ratified contract.

**INCON-v12-A02 — `MANIFEST_RATIFICATION` category placement.**
§Appendix C places `MANIFEST_RATIFICATION` in the CONSISTENCY category for narrative grouping with `MANIFEST_COMMIT_REJECTED` and `MANIFEST_LATTICE_INCOMPLETE`. However, a signed operator ceremony outcome arguably fits GOVERNANCE more naturally (it is a ceremony record, not a consistency event).

**Disposition:** Flagged inline at Appendix C. Either placement is defensible; implementation will pick one at the point of emitter wiring. Advisory only.

**INCON-v12-A03 — `OOK_ROTATED` category placement.**
Source material (GS11, GS12) shows `OOK_ROTATED` emitted under contexts consistent with both GOVERNANCE (paired with CAK-rotation entries under operator ceremony) and LIFECYCLE (as a key-rotation lifecycle marker).

**Disposition:** Appendix C places it in GOVERNANCE to pair with the CAK-rotation family. If implementation treats it as pure key-lifecycle, relocate to LIFECYCLE. Advisory only.

**INCON-v12-A04 — `WRITE_LOCK_VOLUNTARY_RELEASED` v2-scope drift.**
The `voluntary write-lock release` path is explicitly listed in §19 v2 scope. The corresponding Ledger entry type was introduced in GS10 / GS12 partial discussion. Appendix C records the entry type with a [COUNCIL-FLAG] noting that no v1 code path emits it; it is present solely for forensic completeness if operator tooling ever produces it.

**Disposition:** Kept in catalog with flag; retired from v1.2 emitter surface; documented for v2 re-integration.

### Resolution path

None of INCON-v12-A01 through A04 requires a follow-on gap session. All four are documentation-hygiene concerns or forward-compat placeholders that implementation teams will resolve at the emitter-wiring step. The spec is consistent on all load-bearing contracts (authorization, state consistency, validation, retention, provenance).

**Overall v1.2 assembly status: CLEAN.** No unresolved blocking inconsistency. Spec is ready to seal pending only the standard operator ratification step.

---

## Closing Notes

This v1.2 specification closes the v1.1 → v1.2 iteration. v1.1 is preserved in full: every v1.1 decision, constraint, and interface contract carries forward unless explicitly marked DEPRECATED or AMENDED in this document. The v1.2 delta resolves 52 of 60 tracked gaps across the thirteen Phase 2 gap sessions (see `gap-backlog-v5.md`), closes 23 of 25 cross-domain tensions (see Appendix F), and applies fourteen ratified amendments (A1-REVISED, A2–A14; see Appendix G).

**What this spec does:**
- Defines every component and every interface between components at the single-machine reference-implementation level.
- Establishes the unified CeremonyToken authorization model (IC-SCOPE-AUTH-1) as the sole authority chain for every GOVERNANCE-class ceremony.
- Binds the Ledger, the `.vindex` overlay, and the Git repository via the State Ledger and the two-phase commit protocol, extended by the v1.2 bounded-compensation machinery (A1-REVISED).
- Specifies every operator-observable state change via the Ledger entry catalog (Appendix C), including the 50+ v1.2 additions for ceremonies, burst states, bootstrap verification, provenance, and retention.
- Documents every ratified amendment with a section pointer (Appendix G) and registers every D-number collision across parallel session tracks (Appendix H).
- Enumerates two remaining tensions (T15 partial, T16 v2-deferred) and the full open-question register (§18) with explicit dispositions for each.

**What this spec does NOT do:**
- Prescribe implementation language, framework, or runtime details.
- Select an orchestration path (A/B/C) — operator-decided per §19 and Appendix A.
- Specify values for thresholds marked provisional in §18 / GAP-1.
- Address multi-machine or distributed-trust scenarios — v2 scope (§19; T15/T16; GAP-18).
- Define the content-addressed immutable dry-run store (T-S-RP-1; v2 scope).
- Define the m-of-n CAK operational availability path (T15 full resolution; OQ-S-CAK-2; v2).

**Open gaps carrying into v2:**
- GAP-1 (empirical thresholds), GAP-2 (MEMIT architecture compatibility), GAP-3 (v2 migration path), GAP-4 (orchestration path selection), GAP-18 (multi-machine Ledger replication), remaining medium/low-priority GAP-XX items — see `gap-backlog-v5.md` for the full register.

**Carry-forward conditions:**
- v1.2 is structurally self-contained. Reading v1.1 is not required; every v1.1 decision referenced in v1.2 text appears inline or is explicitly pointed to.
- The `llm-as-database-agent-harness-framework.md` background remains the reference for the paradigm (larql, V-Index, MEMIT literature basis) and is not superseded by this spec.
- Deprecated v1.1 Ledger entry types (`HOLD_RELEASE_SIGNATURE_INVALID`, `HOLD_RELEASE_REPLAY_REJECTED`) remain chain-valid in historical Ledgers per C-DEPREC-1. Migration tooling per A7 is required for any operator who needs aggregate reporting that spans the deprecation cutoff.

**Status:** Ready for operator ratification and implementation planning. No targeted follow-on session is required for v1.2 sealing based on the assembly findings (see Appendix I). v2 extends this baseline additively.

*— End of v1.2 Integrated Specification —*
