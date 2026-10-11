# LLM as Database: Agent Harness Architecture
## v1.1 Integrated Specification

> **Version:** 1.1
> **Iteration:** v1.0 baseline + Interface Contract Review Session amendments (IC-GATE-8,
> IC-WE-1, IC-TC-RESET, IC-TC-TIMEOUT, IC-OC-PROBE, IC-SCOPE-UPDATE, IC-CORPUS-AUTH,
> IC-LDG-RETAIN, IC-GATE-9).
> **Status:** Draft — pending operator ratification of D81–D90.
> **Supersedes:** `llm-as-database-v1_0-integrated-spec.md`
> **Scope:** Single-machine reference implementation specification.
> **Basis:** Seven-session Framework Council process — six domain-specialist sessions (Schema,
> Write Engine, Security, Validation, State Consistency, Orchestration) plus a cross-domain
> synthesis session resolving twelve integration tensions — plus one Interface Contract Review
> Session addressing T3, T5, T6, T9, T11, T12 (partial and unlocatable tensions from v1.0).
> **Reference Framework Document:** `llm-as-database-agent-harness-framework.md`
> (Chris Hay larql / V-Index paradigm + MEMIT literature).
> **Amendment source:** `interface-contracts-ic-review-v1.md`
> **Note on version naming:** v1.1 is additive to v1.0. The v2 roadmap targets (§19) —
> distributed trust, key lifecycle management, formal enforcement upgrades — are not addressed
> by these amendments. v1.1 closes or partially closes GAPs 1, 3, 5, 6, 7, 8, 12, 15 and
> resolves T12.

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

**Part VI — Reference Appendices**
- A. Deployment Preconditions
- B. Interface Contract Index
- C. Ledger Entry Type Catalog
- D. Directory Layout
- E. Sealed Corpora Inventory
- F. Decision-to-Session Cross-Reference

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
- Unauthorized corpus authorship (C-GOC4, IC-CORPUS-AUTH).
- Retention policy shortening to destroy forensic evidence (C-SL2, IC-LDG-RETAIN).

## 5. Category 2: Out-of-Scope Operational Assumptions

- Physical security of the host machine.
- Integrity of the base model file at installation (operator responsibility).
- Network security for external content ingestion (operator-controlled).
- Notification infrastructure for integrity violations (OQ-S8 — deployment-specific).
- Backup strategy for `<harness_root>/` (operator responsibility).

## 6. Category 3: Deferred to v2

- Full PKI: mass revocation lists, Orchestrator key rotation, multi-Orchestrator trust.
- Delegation tokens for nested sub-agent invocations (Path B/C nested cases).
- Pre-receive Git hooks (prevent-at-write for Tier 3 config).
- Multi-machine harness with Ledger replication and distributed consensus.
- Voluntary Write Lock release and inter-agent negotiation (OQ-CW1).
- Orchestrator key rotation (OQ — v2 only).
- Genesis security model for fully automated pipelines (OQ-S5).
- Peer agent review delegation token design (GAP-20 — agent-to-agent trust model).
- `.larql` schema version migration path authorship and deprecation ceremony (OQ-W6 residual).

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

**Scope Update Ceremony (D87, IC-SCOPE-UPDATE)**

Write Scope Definition updates are accepted mid-flight — no drain of in-flight invocations is required. An update MUST produce a `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous) before the Orchestrator's in-memory scope registry is updated. The entry carries `previous_scope_hash`, `new_scope_hash`, `operator_signature`, and `affected_agent_ids`.

Any in-flight token whose `write_scope_hash` predates the update will fail at Gate pre-check step 4 with error code `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure). The error payload includes `current_scope_hash` and `scope_updated_at`, enabling the Orchestrator to issue a corrected token without consuming the agent's retry budget. Active PREPARED transactions are not interrupted; scope changes are forward-only.

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

### 11.8 Circuit Breaker (D48, C-TC3)

Thresholds:
- 3 consecutive 2PC failures in one task → trip.
- 5 consecutive 2PC failures across any tasks in a 10-minute window → trip.
- Diverged state → immediate trip, no auto-repair (C-TC5).

On trip: systemwide write suspension (READ_ONLY mode — see §11.8.1). Write resumption requires the signed reset ceremony (IC-TC-RESET).

Abort authority (human interrupt of PREPARED transaction): exists via signed abort request to Orchestrator, always routes through Transaction Controller compensation path, never process-kill (OQ-TPC2 resolved D74). Post-commit abort is rejected.

**§11.8.1 — READ_ONLY Mode and Write Resumption Ceremony (D84)**

On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human action. Inference, query, and read operations proceed normally; write token issuance is suspended. Consistency Status API state transitions to `CIRCUIT_TRIPPED` (§12.5).

Write resumption requires a signed reset ceremony (IC-TC-RESET). The TC independently verifies preconditions before accepting any reset request — human attestation alone is not sufficient. For `CONSECUTIVE_FAILURE` and `CROSS_TASK_FAILURE` trips: TC verifies compensation is `COMPLETED` and current overlay hash matches the Ledger's most recent `COMMITTED` entry. For `DIVERGED_STATE` trips: TC requires a `RECONCILIATION_COMPLETE` Ledger entry with `result: "CONSISTENT"` timestamped after the trip. All preconditions met plus valid operator signature → TC writes `CIRCUIT_RESET` (GOVERNANCE, synchronous) and enters WRITE_ENABLED state.

Reset via the W3 emergency Ledger path is not permitted. The signed ceremony is the exclusive mechanism for write resumption.

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

### 11.12 Pruning Agent (D53–D57, extended T8 and T10)

- Pruning writes flow through the standard 2PC path. No fast-path (D53, C-PA1).
- Restricted to Structural and Knowledge family edges only (D54, C-PA2).
- Cannot touch Genesis tiers L1–L3 (C-PA3).
- Cannot delete edges younger than 24 hours (D56, C-PA5).
- **Cannot delete edges under active Dependency Hold** (T8, IC-PA7).

**Trigger conditions (D57):** every 50 commits or 24 hours; on source file deletion; on function rename detection; on out-of-band commit; on Session 4 D37 gap record followup; manual trigger.

**Backpressure (D55):** 24-hour staleness window; edges older than 24h classified `stale_urgent`. At 1,000 `stale_urgent`, writes suspended until Pruning completes.

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
- `genesis-seal.json` — includes `current_larql_version`, `min_supported_larql_version`, `larql_migration_manifest`, `corpus_author_identities`, `incremental_prepared_timeout`, and `genesis_prepared_timeout` (no default; must be set before Genesis initiation per C-GATE-2) in addition to genesis hash fields.
- `orchestrator-key-anchor.json` (public half of Orchestrator signing key)

**Write model:** produced once during bootstrap. Never modified.

**Integrity:** dual-stored (`.state-ledger/` primary + `<repo_root>/.harness/` secondary). Boot-time hash comparison. Mismatch suspends boot.

### 13.3 Tier 2 — Sealed Artifacts

Evolving human-authored integrity-critical artifacts. Signed-append model.

**Artifacts:**
- `meta-validator-suite/` — Validator held-out corpus.
- `meta-tga-corpus/` — TGA held-out corpus.
- `constitutional-suite/` — Constitutional test suite (promoted from S4 D32).
- `write-scope-definitions/` — Per-agent write authority definitions.
- `reconciliation-reviewers/` — Authorized reviewers for Reconciliation Review Queue.

**Write model:** versioned additive directories (`v1/`, `v2/`, ... `vN/`). Each version signed by operator key. `manifest.json` tracks current active version and signatures.

**Integrity:** dual-store hash (`.sealed-corpora/<n>/manifest.json` + `SEALED_CORPUS_UPDATE` Ledger entry). Boot-time verification.

**Access:**
- Meta-* corpora: time-bounded capability access during Meta-* runs only. Never exposed to normal Validator or TGA operation.
- Constitutional suite: Validator has persistent read access during normal operation.
- Write Scope Definitions: Authorization Gate has persistent read access during normal operation.
- Reconciliation reviewers: Gate reads when verifying `reconciliation_reviewer_id`.

**Per-case audit reporting mandatory** for Meta-* runs (T3 closure of OQ-V5). Aggregate-only reporting is forbidden.

**Corpus Authorship Model (D88, IC-CORPUS-AUTH)**

Corpus authorship is a restricted operator role (C-GOC4). Only identities listed in `corpus_author_identities` (Tier 1 config field) may submit cases. No agent identity MUST appear in this list. Case formats are formally defined:

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

**Write model:** modified via Git commit. Git commit-hook writes `CONFIG_UPDATE` Ledger entry with filename, new hash, Git commit hash.

**Integrity:** Ledger anchor + boot-time hash verification. Boot-time mismatch between current file hash and most recent `CONFIG_UPDATE` entry produces `CONFIG_INTEGRITY_FAIL` and suspends writes.

**Enforcement mode:** detect-at-boot, not prevent-at-write. Stronger enforcement (pre-receive server-side hook) is v2.

### 13.5 Boot-Time Verification Sequence (T4, extended T5, T11)

Fail-closed. Any step failing suspends writes and produces an integrity-violation event.

1. State Ledger Merkle chain verification from Genesis Seal forward.
2. Genesis Seal dual-store comparison.
3. **Orchestrator key anchor dual-store comparison** (T5).
4. Sealed corpus manifest verification (for each Tier 2 artifact).
5. Anchored Git config verification (for each Tier 3 artifact).
6. Agent YAML ↔ Write Scope Definition binding verification.
7. Periodic integrity verification cadence established (T11).

All pass → writes enabled. Any fail → writes suspended, `<TIER>_INTEGRITY_FAIL` Ledger entry, human review required.

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
- **Scope hash mismatch (`SCOPE_HASH_MISMATCH`)** — infrastructure failure class (D87). Gate returns structured payload including `current_scope_hash` and `scope_updated_at`. Orchestrator MUST re-issue token against current scope hash — NOT the stale hash. Retry budget not consumed. Distinguished from generic hash-mismatch by the `SCOPE_HASH_MISMATCH` error code. Three consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation → Orchestrator escalates to human review queue (possible recovery loop or scope update ceremony failure).

### 14.4 Orchestrator-Signed as the Unifying Authority

Invocation tokens, schema migration tokens, and Ledger write authorization all route through the Orchestrator. The Orchestrator's signing key is the single cryptographic anchor that ties together agent identity, write authorization, and integrity-anchored record-keeping.

## 15. Review Pathways — Two-Queue Model (T10)

### 15.1 Two Distinct Review Types

**Correctness Review Queue** — populated by Reflexion escalation (D37 Step 3).
- Reviewer question: *"Is this agent output acceptable?"*
- Contains: task spec, retry history, decomposition log, failure tier, consistency status.
- Decisions: `approve_as_is` | `reject` | `re_route_for_further_work`.
- **Default on neglect:** task times out into logged suspension (D37 Step 4). Work is lost; no state changes.

**Reconciliation Review Queue** — populated by Pruning Agent catch-up patches with `requires_human_review` flag.
- Reviewer question: *"Should we update parametric memory to match out-of-band state change?"*
- Contains: out-of-band Git commit hash and diff, Pruning analysis, proposed catch-up `.larql` patch, classification rationale, age.
- Decisions: `approve_patch` | `reject_patch` | `modify_patch` | `defer_with_reason`.
- **Default on neglect:** no silent default. Items accumulate; backlog signals escalate via Ledger and Consistency Status API.

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

### 16.2 Three-Tier Writer Model

**Tier W1 — Orchestrator-mediated writes** (default for all component writes):
All components route writes through the Orchestrator, which verifies component identity, validates entry schema, assigns Merkle predecessor hash, and appends.

Writers under W1: Authorization Gate, Commit Executor, Meta-Validator, Meta-TGA, Validator, Pruning Agent, Transaction Controller, Human Review writers, Config Update Hook.

**Tier W2 — Bootstrap writes** (one-time):
During initial bootstrap sequence only. Writes Genesis Seal, Orchestrator Key Anchor, `PROJECT_INITIATED` (retention policy declaration), and initial chain anchor. After bootstrap completes, bootstrap writer is retired; any subsequent bootstrap-class entry attempt is an integrity violation.

**Tier W3 — Emergency Escalation Path** (narrow):
Gate, Transaction Controller, and Boot-verifier each hold a limited emergency-write capability restricted to a single entry type: `INTEGRITY_VIOLATION_EMERGENCY`. Bypasses Orchestrator mediation. Subject to:
- Maximum 1 entry per minute per component (rate limit).
- Strict schema enforcement.
- Immediate write suspension.
- Forced human investigation.

Purpose: log compromised-Orchestrator scenarios where normal W1 path is the problem.

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

See Appendix C.

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

- **OQ-W1** — Cumulative edit volume degradation threshold (model-specific). All drift numbers (1,500 / 8,000 / 2,000 sub-batch) are provisional. The drift state interface shape is now specced (IC-WE-1, D83); threshold values remain OQ-W1. Blocks OQ-OC3 calibration.
- **OQ-W2** — MEMIT/target model architecture compatibility verification.
- **OQ-W8** — Behavioral probe generalization beyond code domains.
- **OQ-OC3** — Compaction verification sampling calibration (failure report format and abort thresholds now specced by D86, IC-OC-PROBE; sampling rates for SUPPORTING and INCIDENTAL tiers remain provisional pending OQ-W1 resolution).
- **T5 / T11** thresholds — async WAL flush cadence, verification intervals, backlog thresholds — all starting heuristics.

### 18.2 Operational Policy

- **OQ-S5** — Minimum viable Genesis security for fully automated pipelines (v1 requires human review; full automation is v2 or operator policy).
- **OQ-S8** — Notification channels for integrity violations (email, Slack, logging — not spec).
- **OQ-V1** — Constitutional test failures as Tier 3 classification (policy). Mechanism (constitutional suite in Tier 2 sealed corpus) is specced; runtime tagging and promotion ceremony are not.
- **OQ-V5** — PARTIALLY CLOSED by D88 (IC-CORPUS-AUTH). Corpus authorship role (C-GOC4), case formats, and minimum viable corpus size (20 cases) now specced. Corpus extension cadence and authorship rotation policy remain operator-owned.
- **OQ-SC2** — Layer 4 recovery when originating external document unavailable (partially addressed by Layer4_domain project-lifetime retention; external document provenance tracking is unspecced).
- **OQ-W6** — PARTIALLY CLOSED at Gate enforcement layer (D81, D82, IC-GATE-8). Gate version pre-check (#8) and compaction versioned parser are now specced. Remaining deferred to v2: migration path authorship, deprecation ceremony for old versions, multi-version team deployment.

### 18.3 Deferred to v2

- **OQ-CW1** — Voluntary scope-lock release / inter-agent negotiation.
- **OQ-SL2** — Multi-machine harness ledger replication.
- **OQ-W6 (residual)** — `.larql` schema version migration path authorship and deprecation ceremony (Gate enforcement layer closed in v1.1).

### 18.4 Closed in Integration

Closed during Session 7 synthesis:
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
- **OQ-S4** — Scope version management across long-running projects (D87: mid-flight update model; `SCOPE_HASH_MISMATCH` error code defined; IC-SCOPE-UPDATE).
- **OQ-SL1** — Full Ledger retention policy (D89: immutable-downward model; `PROJECT_CLOSED` ceremony; archival format versioned `"1.0"`; IC-LDG-RETAIN).

## 19. v2 Scope Targets

v2 is additive, not corrective. The v1.1 design does not prevent any v2 feature; it simply does not include them.

**Distributed trust:**
- Multi-machine harness with ledger replication and distributed consensus.
- Cross-machine token federation.
- Multi-operator (quorum) Tier 2 signing.
- Remote attestation.

**Key lifecycle management:**
- Operator signing key rotation and revocation (full PKI).
- Orchestrator key rotation.
- Cross-project key sharing policies.
- Delegation tokens for nested sub-agent invocations.

**Agent-to-agent trust:**
- Peer agent review delegation token design (GAP-20 — authorization model for D37 Step 2 escalation second Coder Agent).

**Formal enforcement upgrades:**
- Pre-receive Git hooks (prevent-at-write for Tier 3).
- Stronger sandbox attestation.
- Hardware-backed key storage (TPM, HSM).

**Archival extensions:**
- External cold-storage export for `.larql` and Ledger archives.
- Project-to-project trust transfer for shared sealed corpora.

**Automation extensions:**
- OQ-S5 resolution — Genesis security model for fully automated pipelines (secondary LLM reviewer as human-review proxy).

**Schema versioning extensions:**
- OQ-W6 residual — `.larql` schema version migration path authorship, deprecation ceremony, multi-version team deployment.

---

═══════════════════════════════════════════════════
# PART VI — REFERENCE APPENDICES
═══════════════════════════════════════════════════

## Appendix A — Deployment Preconditions

Environmental contracts the harness assumes from its deployment context:

- Single machine, single OS user owning the harness process.
- Filesystem supports POSIX permissions; `<harness_root>/` readable only by harness user.
- Git binary installed and trusted (standard OS package).
- Docker or E2B runtime available for sandbox execution.
- Base model file present at configured location with known hash (provenance verified at install, not runtime).
- Initial operator signing key generated or imported before first boot.
- `genesis_prepared_timeout` set in Tier 1 config before Genesis initiation (C-GATE-2).
- Network connectivity for external content ingestion (Architect Agent) is operator-controlled.
- Backup strategy for `<harness_root>/` is operator responsibility.

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

## Appendix C — Ledger Entry Type Catalog

Organized by audit category tag.

**SECURITY category:**
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
- `CORPUS_WRITE_REJECTED` *(sync for UNAUTHORIZED_AUTHOR reason; GOVERNANCE category for FORMAT_VIOLATION or DUPLICATE_CASE_ID; v1.1)*
- `RETENTION_OVERRIDE_REJECTED` *(sync — retention shortening attempt blocked; v1.1)*
- `CONTENT_SPLIT_LOOP` *(async advisory — Coder Agent repeatedly resubmitting mixed-classification patches; v1.1)*
- `CIRCUIT_RESET_REJECTED` *(sync — failed reset ceremony attempt; v1.1)*

**CONSISTENCY category:**
- `PREPARED`, `COMMITTED`, `COMPENSATED`, `FAILED`
- `IMMUTABLE_ANCHOR`
- `ANCHOR_ESTABLISHED` (flag on qualifying `COMMITTED` entries)
- `COMPACTION_BEGIN`, `COMPACTION_BOUNDARY`, `COMPACTION_ABORT`
- `COMPACTION_BUNDLE_SEALED`, `SUPERSEDED_BUNDLE_EXPIRED`
- `LEDGER_EPOCH_ARCHIVED`
- `CHAIN_VERIFICATION_RESULT`
- `DEPENDENCY_CONFLICT_FLAGGED`
- `TIMED_OUT` *(sync — PREPARED-state timeout; fields: transaction_id, compensation_direction, trigger; v1.1)*
- `CIRCUIT_TRIPPED` *(sync — circuit breaker trip event; fields: trip_type {CONSECUTIVE_FAILURE | CROSS_TASK_FAILURE | DIVERGED_STATE}, triggering_transaction_id; v1.1)*
- `RECONCILIATION_COMPLETE` *(sync — full reconciliation run result; field: result {CONSISTENT | DIVERGED}; v1.1)*
- `COMPACTION_ABORTED` *(sync — compaction verification failure; payload: serialized CompactionProbeReport; v1.1)*
- `COMPACTION_PROBE_FAILED` *(sync — Behavioral Probe infrastructure failure during compaction, distinct from COMPACTION_ABORTED; v1.1)*
- `COMPACTION_CORPUS_SMALL` *(async advisory — probe corpus below sampling floor; v1.1)*

**VALIDATION category:**
- Meta-Validator health records (per-case; v1.1: `health_score` field is `NOT_COMPUTED` when corpus < 20 cases; includes `corpus_staleness_flag` and `corpus_size_at_run`)
- Meta-TGA health records (per-case; same v1.1 extensions as Meta-Validator)
- Task gap records (D37 Step 4)

**GOVERNANCE category:**
- `CONFIG_UPDATE`
- `SEALED_CORPUS_UPDATE`, `SEALED_CORPUS_ACCESS`
- `RECONCILIATION_REVIEW_DECISION`
- `RECONCILIATION_BACKLOG_WARNING`, `RECONCILIATION_BACKLOG_CRITICAL`
- `CIRCUIT_RESET` *(sync — successful circuit breaker write resumption; fields: target_trip_entry_id, operator_id, preconditions_verified; GOVERNANCE category; v1.1)*
- `SCOPE_UPDATED` *(sync — Write Scope Definition updated; fields: previous_scope_hash, new_scope_hash, operator_signature, affected_agent_ids; v1.1)*
- `CORPUS_CASE_ADDED` *(async — corpus case successfully appended; fields: case_id, author_id, corpus_target, new_corpus_size; v1.1)*
- `RETENTION_OVERRIDE_EXTENDED` *(sync — retention period extended; operator-signed; v1.1)*

**LIFECYCLE category:**
- `TASK_DECOMPOSED`
- `DEPENDENCY_HOLD_PLACED`, `_RENEWED`, `_RELEASED`, `_EXPIRED_UNCLAIMED`
- Scope Lock entries
- Compaction scheduling events
- `PROJECT_INITIATED` *(sync, W2 bootstrap — retention policy declaration, mint-once; fields: default_retention_policy, operator_signature; v1.1)*
- `PROJECT_CLOSED` *(sync — final epoch sealed, Ledger made read-only; fields: operator_signature, final_epoch_id, archival_status {COMPLETE | PENDING}; v1.1)*

## Appendix D — Directory Layout

```
<harness_root>/                         # Machine-local, NOT Git-tracked
  .state-ledger/
    ledger.jsonl                        # Merkle-chain Unified Ledger
    wal/                                # Async write-ahead log
    archive/{epoch_bundle_N}/           # Ledger epoch cold storage
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
  .orchestrator-key/                    # Private key material (permission-protected)
  .larql-archive/
    active/                             # Active .larql patches
    superseded/{epoch_bundle_N}/        # Compaction-epoch bundles
  .vindex/                              # Active overlay stack
    genesis_schema.vindex
    genesis_domain.vindex
    genesis_constraints.vindex
    genesis_knowledge.vindex
    incremental_NNNN.vindex

<repo_root>/                            # Git-tracked project repository
  .harness/                             # Tier 3 — Anchored Git Config
    genesis-seal.json                   # Tier 1 secondary copy
    orchestrator-key-anchor.json        # Tier 1 secondary copy (public half)
    path-classification.json
    agent-yamls/
      architect.yaml
      coder.yaml
      pruning.yaml
      tga.yaml
      validator.yaml
  src/
  tests/
  ...
```

## Appendix E — Sealed Corpora Inventory

Five Tier 2 sealed corpora in v1.1:

| Corpus | Purpose | Access Pattern | Minimum Viable Size | Retention |
|---|---|---|---|---|
| `meta-validator-suite/` | Held-out cases for Meta-Validator | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `meta-tga-corpus/` | Held-out `(spec, gold_tests)` for Meta-TGA | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `constitutional-suite/` | Architectural invariant tests | Validator persistent read | No minimum specced | Permanent additive versioning |
| `write-scope-definitions/` | Per-agent write authority | Authorization Gate persistent read | n/a | Permanent additive versioning |
| `reconciliation-reviewers/` | Authorized reviewer list for Reconciliation Queue | Gate read on reviewer verification | n/a | Permanent additive versioning |

All follow identical storage, signing, dual-store, and boot-verification mechanics.

## Appendix F — Decision-to-Session Cross-Reference

Decisions carry session-prefixed numbers for traceability:
- **D1–D10:** Session 1 (Schema)
- **D11–D21:** Session 2 (Write Engine)
- **D22–D31:** Session 3 (Security)
- **D32–D41:** Session 4 (Validation)
- **D42–D67:** Session 5 (State Consistency)
- **D68–D80:** Session 6 (Orchestration)
- **T1–T12:** Session 7 (Integration — cross-domain resolutions)
- **D81–D90:** IC Review Session (v1.1 — interface contract negotiation)

**T12 — IDENTIFIED AND RESOLVED:** `CONTENT_CLASSIFICATION_MIXED` rejection protocol (D90, IC-GATE-9). Primary tension: Warden (Gate as classification authority — security integrity of triple-level content classification enforcement) vs. Graph Data Architect (Coder Agent feedback path — how the agent learns which triples require splitting and into which classification tier). Resolved by IC-GATE-9: Gate emits structured `split_guidance`; Gate triple-level classification is authoritative over Coder declarations. Recovery path routed through Orchestrator to preserve audit trail. Previously unlocatable in spec body; now traceable to §8.5, §10.2 pre-check #5, §11.2.

Constraints: `C1–C7` (S1), `C8–C15` (S2), `C16–C22` (S3), `C23–C30` (S4), `C-SC1–C-OC2` (S5), `C-OR1–C-OR6` (S6), `C-GATE-1, C-GATE-2, C-OC3, C-SL2, C-GOC4, C-WE-1` (IC Review Session, v1.1).

Open Questions carry origin-session prefixes: `OQ1–OQ10` (S1), `OQ-W*` (S2), `OQ-S*` (S3), `OQ-V*` (S4), `OQ-SC*`, `OQ-TPC*`, `OQ-TC*`, `OQ-SL*`, `OQ-GOC*`, `OQ-PA*`, `OQ-CW*`, `OQ-OC*` (S5), `OQ-OR*` (S6).

---

## Closing Notes

This v1.1 specification extends the v1.0 baseline with nine interface contracts produced during the Post-Session 7 Interface Contract Review. All extensions are additive. No v1.0 decisions, constraints, or interface contracts have been superseded or renumbered.

**What this spec does:**
- Defines every component and every interface between components.
- Enumerates trust boundaries, separating defended threats from operationally-assumed threats and v2-deferred threats.
- Preserves traceability from every decision to its originating session and discussion.
- Identifies what remains empirical (tunable post-deployment) vs. what remains operational policy (deployment-specific) vs. what remains structurally deferred to v2.
- Closes or partially closes eight gaps from the v1.0 gap backlog (GAP-1 interface shape, GAP-3 Gate layer, GAP-5, GAP-6, GAP-7, GAP-8 partial, GAP-12, GAP-15 partial).
- Resolves T12, the previously unlocatable Session 7 tension.

**What this spec does not do:**
- Prescribe implementation language, framework, or runtime details.
- Select an orchestration path (A/B/C) — explicitly operator-decided.
- Specify values for thresholds marked provisional (OQ-W1 remains open).
- Address multi-machine or distributed-trust scenarios.
- Define the v2 scope items listed in §19.

**Open gaps not resolved in v1.1 (carrying forward):**
- GAP-1 (threshold values — empirically blocked), GAP-2 (MEMIT architecture compatibility), GAP-3 (v2 migration path), GAP-4 (orchestration path selection), GAP-8 (cadence policy), GAP-9 through GAP-19 (medium and low priority), GAP-20 (peer agent review authorization — new in v1.1).

**Status:** Ready for implementation planning and architectural review. v1.2 or v2 extends this baseline additively.

*— End of v1.1 Integrated Specification —*
