# LLM-as-Database — End-to-End Production Framework (spec ground-truth snapshot)

**Snapshot date:** 2026-06-21. **Source:** `research_and_specs/llm-as-database-v1_2-integrated-spec.md` (v1.2 integrated), read end-to-end; section refs inline. **Purpose:** a clean, faithful picture of *how the spec prescribes the system be implemented and how memory is managed in production*, to ground forward work. **§A–§I = what the SPEC prescribes** (faithful). **§J = our empirical overlay** (what we've proven / amended / found open against it — pointers, not restated). De-dup discipline: this is the e2e narrative; per-result detail lives in `CORPUS/` + `docs/SPEC_EXPERIMENT_OVERLAY.md`.

---

## §A — The paradigm (§1)
A multi-agent development harness that treats an LLM's **FFN as a physically queryable + editable graph database.** The shift is from **in-context learning** (RAG, transient context) to **in-weight learning**: validated agent outputs are *compiled into the model's weights* (via MEMIT) so subsequent agents **natively "know" the project state without prompt reconstruction.** State lives in **two parallel mediums**: a **Git repo** (deterministic syntactic state) and a **versioned parametric overlay** — the **`.vindex` layer** (semantic state physically encoded in weights).

## §B — The six coordinated layers (§3), under one Orchestrator control plane (§12)
| Layer | Concern | Key components |
|---|---|---|
| **Schema** (§7) | what the graph can represent | entity taxonomy, relation families, Genesis tiers |
| **Write Engine** (§8) | how facts enter weights | **MEMIT**, `.vindex` overlays, `.larql` patches, drift tracking |
| **Validation** (§9) | are outputs correct *before* commit | Reflexion/actor-critic, TGA cascade, Meta-Validator |
| **Security** (§10) | who may write, and how | Patch Authorization Gate, single-use tokens, Write Scope Definitions, audit |
| **State Consistency** (§11) | do both mediums agree | 2PC, Transaction Controller, Pruning Agent, **State Ledger** |
| **Orchestration** (§12) | coordinate everything | Orchestrator, review queues, lock/hold registry |

**Authoritative-medium rule (§11.2):** Git is authoritative for `structural_entity` knowledge; **`.vindex` is authoritative for Genesis-Layer-4 `domain_concept` + `constraint_rule`.** Every `.larql` patch declares `CONTENT_CLASSIFICATION ∈ {structural, layer4_domain}`; `mixed` is rejected.

## §C — The WRITE path, end to end (§9–§11)
The **atomic transaction unit** is the **task-completion package** `{module_code, test_suite, .larql_patch, declared_dependencies}` — commits together or not at all (§11.4). Flow:

1. **Orchestrator** decomposes the task, acquires a **Write Lock** on the target region, invokes agents.
2. **TGA** authors tests; **Coder** implements + drafts the `.larql` patch. **No reasoning agent ever holds write access to both mediums.**
3. **Validation Layer** (§9): actor-critic independence + Validator's 4-level cost-stratified cascade + Meta-Validator. **Everything is *behaviorally verified*, not vouched for.** `code_pass_patch_fail` is a hard rejection.
4. **Patch Authorization Gate** (§10.2): Identity → Scope → Integrity checks; verifies the single-use **invocation-scoped token** (signed by the Orchestrator key) + the patch's classification + scope.
5. **Commit Executor** (§9.10, §11.5) — the **sole** two-medium writer, a deterministic non-reasoning chokepoint; **write concurrency capped at 1** via a FIFO queue (fan-out happens above the queue, strict serialization at it).
6. **Two-Phase Commit (§11.5):** **Phase 1 Prepare** → `PREPARED` ledger entry + session lock. **Phase 2 Commit, fixed order: (1) Git push FIRST, (2) `.vindex` mount SECOND** → `COMMITTED` ledger entry with overlay hash. Ordering forces failures into the *recoverable* "Git-ahead" mode, never "weights-ahead." Missing `PREPARED` = a ledger-bypass security incident.

## §D — Two operating modes + the `.vindex` tier stack (§8.3–§8.4)
- **Genesis Mode** — a **single atomic batch compile** that mints the initial tier stack (§7.7, §11.6). Partial Genesis is not a valid state.
- **Incremental Mode** — smaller patches buffered via an L1 Cache, then MEMIT-compiled as **per-commit overlays.**

```
.vindex/
  genesis_schema.vindex       ← L1 Genesis (frozen post-mint)
  genesis_domain.vindex       ← L2 Genesis (frozen)
  genesis_constraints.vindex  ← L3 Genesis (elevated-review changes only)
  genesis_knowledge.vindex    ← L4 Genesis (updatable via standard pipeline)
  incremental_NNNN.vindex     ← per-commit overlays   ← these ACCUMULATE
```
Each fact carries a two-number importance model: `declared_importance ∈ {CORE, SUPPORTING, INCIDENTAL}` (§8.6) — drives probe sampling + priority.

## §E — ⭐ MEMORY MANAGEMENT in production (the core lifecycle) (§8.7–§8.10, §11.12–§11.14)
This is how the parametric store stays healthy over a project's life. **Incremental overlays accumulate; drift is tracked relative to the last anchor; compaction periodically re-batches everything back to a clean anchor.**

**1. Drift tracking (§8.7).** The Write Engine exposes a `drift_state` object to the Transaction Controller, **reset to zero at every anchor event** (= a successful Genesis compile *or* a successful compaction). Fields: `edge_count_since_anchor`, `drift_tier ∈ {NOMINAL, WARNING, HARD, CRITICAL}`, `anchor_event_id`, `overlay_file_count`, `p95_latency_ratio`. The TC **reads `drift_state` before issuing any write token.**
- **WARNING** at **1,500 edges since anchor** → schedule compaction at next idle window.
- **HARD** at **8,000 edges since anchor** → **writes suspended** until compaction completes.
- *(All threshold values are explicitly provisional — OQ-W1.)*

**2. Compaction = the heal (§11.14, §8.10).** **A full MEMIT re-run on all active `.larql` patches** (delta composition is rejected on correctness grounds). Triggers: drift WARNING/HARD · every **30 days** since last anchor · `overlay_file_count ≥ 50` · `p95_latency_ratio ≥ 2.0` (inference latency at 2× baseline) · manual. It **resets the anchor → drift to zero.** Genesis tiers are **never** compacted. Compaction is a **single atomic 2PC event** and is **gated by a `CompactionProbeReport`**: **CORE-edge pass rate MUST = 1.0 (any CORE regression aborts compaction)**; SUPPORTING ≥95%; INCIDENTAL ≥80%; abort → keep existing overlays + `COMPACTION_ABORTED` ledger entry.

**3. Archive (§8.10).** Patches are `active` (feed the latest anchor / later overlays) → `superseded` (pre-anchor; content embedded in the compacted overlay; moved to sealed bundles) → `retained-for-audit` (ledger record permanent). Structural superseded: 90-day retention; Layer4_domain: project-lifetime cold storage.

**4. Pruning Agent (§11.12) — deletion + staleness GC.** Flows through standard 2PC (no fast-path). Restricted to Structural + Knowledge edges; **cannot touch Genesis L1–L3; cannot delete edges < 24h old or under active Dependency Hold.** Triggers: every 50 commits / 24h, on source-file deletion / function rename / out-of-band commit, manual. **Backpressure:** edges > 24h = `stale_urgent`; at **1,000 stale_urgent, writes suspended** until Pruning completes. Also runs an `external_source_audit` over Layer-4 facts with external provenance (staleness → *advisory*, not deletion).

**5. Out-of-band Git reconciliation (§11.13).** Humans/tools may commit to Git outside the pipeline; Pruning detects these and generates **catch-up patches flagged `requires_human_review` — no auto-compile** → Reconciliation Review Queue.

**6. Concurrency safety for memory ops (§11.9).** **Write Lock** (60-min TTL, concurrent-write prevention) vs **Dependency Hold** (72-h TTL, protects edges a long task is *reading* from Pruning). Distinct lifecycles across escalation (§11.10).

## §F — Post-write verification (§8.9)
Two-level mandatory probe on every write: **L1 Storage probe** (`SELECT` read-back confirms the edge was written — all writes) + **L2 Behavioral probe** (a generation test confirms the fact *fires* in inference — CORE/SUPPORTING). **`storage-pass / behavior-fail` is a named, non-collapsed failure mode** (recorded `write_outcome = behavior_fail`). L2 uses a 3-member probe family (Generation / Assertion / Constraint) under the Semantic Assertion Criterion (§21); the ε pass-threshold is a calibrated quantity (§22).

## §G — The READ / query path (§7, §8.9, §11.2–11.3)
- **Primary read = inference over the compiled model** — agents "natively know" the state (the paradigm payoff).
- **Structured reads:** L1 `SELECT` read-back; **bidirectional traversal / reverse lookup required — every edge reverse-lookable, no write-only edges** (D4, §7.6); relation-family queries; tags enable query-views without separate stores.
- **Consistency on read (§11.3):** **strong consistency globally; reads BLOCK against `.vindex` during the mount window; no stale-read fallback.**
- *(Note: the spec defines read **requirements** — exact lookup, reverse, traversal, aggregation/negation as the read-contract surface — but does not ship a single formal query-language section; the richer read contract is the least-specified production surface. This is our CP2/E3 gap, §J.)*

## §H — Governance, consistency & failure handling (§10–§12)
- **Strong consistency**, write-concurrency = 1, Git-first 2PC ordering (§C).
- **Transaction Controller (§11.7)** is the *sole* compensation authority (no agent self-compensates): structural patches auto-revert Git after 3 failed `.vindex` mounts; layer4_domain retries `.vindex` 5× and Git-revert needs human confirmation.
- **Circuit breaker → READ_ONLY mode (§11.8):** on any trip, inference/query continue, **write-token issuance is suspended**; resumption requires a signed reset ceremony.
- **PREPARED-state timeouts (§11.5.1):** incremental 2h (→ rollback + `AWAITING_OPERATOR_RETRY`); Genesis no-default (breaker trips, forensic state preserved).
- **State Ledger (§11.15, §16):** one append-only integrity-anchored log unifying security/consistency/validation/governance/lifecycle events, audit-category tagged.
- **CeremonyToken / Patch Authorization (§20, §10):** single-use invocation-scoped tokens signed against the Orchestrator key anchor; a stolen token is useless unless every anchored document is unchanged in its TTL.
- **Three orchestration path options (§12.3)** (concurrency model) are deferred to the operator.

## §I — Deployment realization
The spec's deployment = **the model with mounted `.vindex` serves inference** (state is in-weight, zero added retrieval step). The **physical realization our program validated** = **edit offline on GPU → COMPILE → serve on CPU** (D-SCOPE-1; the Genesis/batch-rebuild model), with the compiled store quantized (Q4_K_M) and served on commodity CPU. *(The CPU-serve realization is partly our finding, §J / `CORPUS/17,18`.)*

---

## §J — Our empirical overlay (what's PROVEN / AMENDED / OPEN against this spec)
Detail + per-result pointers in **`docs/SPEC_EXPERIMENT_OVERLAY.md`** (spec-section ↔ experiment map) and `CORPUS/`. Headlines:
- **PROVEN-FOR-SCOPE (3B / N≤100 / batch):** the data-path spine — Genesis batch compile is corruption-clean (A1), survives real Q4_K_M (B3/CORPUS-17), serves edited facts on CPU (E1/CORPUS-18).
- **AMENDED — §8.7 drift contract:** the spec's **count-only** `edge_count_since_anchor` is the *wrong predictor* — corruption is **relation-concentration- and edit-order-dominated** → our **concentration-aware `k≤1` amendment** (D1/B1/D-D1-2). Model-general (3B+7B); numeric cross-model transfer (OQ-W1) **OPEN**.
- **DECIDED — architecture (B3/D-B3N-1):** in-weight is **not contractually required**; the spec's compaction-bounded hybrid is in-weight-viable under **3 conditions** (concentration-aware §8.7 · compaction-before-the-envelope · **compaction-at-scale cleanliness**).
- **OPEN / live (the forward work):**
  - **Condition 3 (compaction-at-scale):** the engine does a *single joint solve* (no real sub-batching — the "2,000 cap" is a spec prescription, §8/§10.4). D20 (running) shows the spec's *prescribed* sub-batching **reintroduces corruption (robust by ~10 sub-batches)** → **§E compaction cannot be assumed to fully heal at scale.** The single-solve-at-true-scale question is gated on a larger stimulus pool.
  - **The READ contract (§G / CP2):** triple-readback + 5 query families + violates-rejection — **largely unspecified + untested; the biggest determination gap.**
  - **Governance (§H / CP1–G3):** prototyped (design-viable), **not empirically proven.**
  - **7B numeric transfer; large-N vs the spec's edit caps.**

**One-line ground truth:** *the spec is a Git+parametric dual-medium harness whose memory is managed by accumulate-overlays → track-drift → compact-back-to-a-clean-anchor (with Pruning GC + behavioral-probe gates); our evidence proves the batch write/deploy spine at small scale, requires the drift trigger be concentration-aware, and shows the compaction self-heal is unsafe once it sub-batches — while the read/query contract and at-scale behavior remain the open frontier toward F1.*
