# Gap Session 5 (MEMIT-focus) — Summary

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** Gap resolution session (write-engine cluster)
**Primary voice:** MEMIT Specialist
**Secondary voices:** Validation Contract Architect (GAP-9 probe authoring independence), State Consistency Theorist (GAP-11 Pruning Agent extension)
**Targets:** GAP-9 (behavioral probe generalization), GAP-11 (Layer 4 external document provenance), GAP-15 residual (stratification key)
**Baseline:** v1.1 integrated spec
**Status on exit:** GAP-9 resolved; GAP-11 resolved; GAP-15 residual resolved; two new open questions surfaced; no new cross-domain tensions

---

## 0. Framing

The three gaps share a common shape from the write engine's angle: each leaves under-specified a *structural contract* that compile must enforce before touching weights. GS5M's working principle: the write engine's role is narrow — reject malformed inputs before any weight write, stay deterministic once inputs are accepted. This pushes every policy decision (what a valid probe looks like, what provenance must include, what stratification is sufficient) upstream into patch metadata and the Validation Layer.

The three resolutions share three moves: (a) make the structural requirement *mandatory in patch metadata*, (b) enforce *presence-and-shape-only* at compile (no semantic judgment, no live network calls), (c) push semantic evaluation to the Validator or the Pruning Agent as appropriate.

---

## 1. GAP-9 Resolution — Behavioral Probe Generalization

### 1.1 Three-Mode Probe Protocol

Behavioral probes are decoupled from code execution. A probe is a structured `(prompt, expected, mode, tolerance)` tuple. Three modes are defined:

| Mode | "Passes" means | Default use |
|---|---|---|
| `templated_recall` | Generated tokens contain target (or declared alias) within token budget | SUPPORTING atomic facts |
| `forced_choice` | argmax probability on correct target given ≥2 distractors | Ambiguous-generation cases; constraint-encoding facts |
| `generation_consistency` | Declared `consistency_check` (regex / exact-match / LLM judge) returns PASS on open-ended generation | CORE two-probe second pass |

**Default importance-to-mode mapping:**
- CORE → `forced_choice` required + `generation_consistency` required (two-probe gate)
- SUPPORTING → `templated_recall` OR `forced_choice` (one required)
- INCIDENTAL → no behavioral probe (L1 storage probe only)

### 1.2 Probe Authoring Split (preserves D32–D33)

- Coder Agent authors the `probe_template` block as part of the `.larql` patch.
- Validator independently generates ≥2 additional distractors for `forced_choice` mode (Coder distractors are a lower bound).
- Validator reviews template for adversarial degenerate cases (trivially-passing templates, self-referential prompts, empty consistency_check). DEGENERATE verdict → patch rejected at Validation (not compile).

### 1.3 Compile-Time Structural Enforcement

MEMIT enforces only structural correctness:
- CORE edge with missing `probe_template` → compile rejected.
- `templated_recall` with empty `expected` → compile rejected.
- `forced_choice` with <2 `distractors` → compile rejected.
- `generation_consistency` with missing `consistency_check` → compile rejected.

Probe *quality* is Validator scope, not MEMIT.

### 1.4 New Decisions (GAP-9)

- **D-GS5M-1:** Three-mode probe protocol (`templated_recall`, `forced_choice`, `generation_consistency`) declared per-edge in patch metadata.
- **D-GS5M-2:** Coder authors probe; Validator independently generates adversarial distractors and reviews for degenerate templates. Actor-critic independence preserved.
- **D-GS5M-3:** CORE edges require two-probe gate (`forced_choice` + `generation_consistency`); either failure aborts the write.

### 1.5 New Constraints (GAP-9)

- **C-PROBE-GEN-1:** Every CORE edge MUST declare `probe_template` in patch metadata. Compile rejects without.
- **C-PROBE-GEN-2:** Probe template authorship and probe outcome evaluation MUST be performed by independent agent instances.
- **C-PROBE-GEN-3:** Mode-specific structural requirements enforced at compile (non-empty `expected` for recall; ≥2 `distractors` for forced_choice; `consistency_check` block for generation_consistency).
- **C-PROBE-GEN-4:** CORE edges MUST pass both `forced_choice` AND `generation_consistency` probes.

### 1.6 New Interface Contracts (GAP-9)

- **IC-WE-PROBE-SCHEMA** — Write Engine pre-compile structural validation of `probe_template` block. Malformed → `PROBE_TEMPLATE_MALFORMED` (INTEGRITY, sync); Phase 1 rollback.
- **IC-VAL-PROBE-REVIEW** — Validator per-edge `probe_review_verdict ∈ {OK, DEGENERATE, AMBIGUOUS}`. DEGENERATE rejects patch at Validation; AMBIGUOUS returned to Coder for one retry.

---

## 2. GAP-11 Resolution — Layer 4 External Document Provenance

### 2.1 Mandatory Hash-Pinning in Patch Metadata

`external_provenance` block in `.larql` patch metadata (required whenever Layer 4 edge has `external_source_id` set):

| Field | Type | Req | Notes |
|---|---|---|---|
| `source_uri` | URI string | yes | HTTPS / IPFS / archive pin |
| `source_hash_at_write` | SHA-256 hex | yes | Hash of fetched content at write time |
| `hash_algorithm` | enum | yes | `SHA-256` (v1) |
| `fetch_timestamp_utc` | ISO-8601 | yes | Time of fetch, not patch commit |
| `fetch_method` | enum | yes | `http_get` / `api_call` / `archive_fetch` |
| `content_length_bytes` | integer | yes | Detects truncation vs. content change |
| `extracted_fact_span` | `{start, end}` | no | Offsets into source, aids reconciliation |
| `archive_uri` | URI string | no | Best-effort archive.org / IPFS pin |
| `refetch_policy` | enum | yes | `pruning_cadence` / `hourly` / `never` |

**Ledger mirror:** `EXTERNAL_PROVENANCE_RECORDED` (CONSISTENCY, async) at patch commit. Replicates patch metadata plus `patch_id`, `edge_triple_hash`, `ledger_seq`.

**MEMIT compile enforcement:** presence + structural correctness + hash algorithm allowlist + URI scheme allowlist. **No live refetch at compile time** — determinism preserved.

### 2.2 Three-State Advisory Staleness

| State | Condition | Ledger | Edge flag |
|---|---|---|---|
| `FRESH` | Refetch hash = `source_hash_at_write` | silent | none |
| `STALE` | Source reachable, hash differs | `EXTERNAL_PROVENANCE_STALE` | `provenance_flag: STALE` |
| `UNAVAILABLE` | Source unreachable | `EXTERNAL_PROVENANCE_UNAVAILABLE` | `provenance_flag: UNAVAILABLE` |

CORE-importance external facts: first transition out of FRESH raises `REQUIRES_HUMAN_REVIEW` (parallel to §11.13 out-of-band Git reconciliation pattern).

**Advisory-only rationale:** hard-blocking on external staleness creates a DoS vector (anyone controlling a cached external source can wedge the harness) and produces false-positive wedging on routine network flaps and whitespace-only source edits.

### 2.3 Monitoring via Pruning Agent Sub-Routine

**Pruning Agent gains an `external_source_audit` sub-routine. No new component.**

- Cadence: default aligned with Pruning Agent cadence (every 50 commits or 24h); per-fact override via `refetch_policy`.
- Failure isolation: external-audit failures MUST NOT cascade to Git-side pruning. On N consecutive network failures, suspend external-audit only; emit rate-limited `EXTERNAL_AUDIT_SUSPENDED`.

### 2.4 New Decisions (GAP-11)

- **D-GS5M-4:** Mandatory `external_provenance` block in patch metadata for Layer 4 external facts. Compile rejects without. Ledger mirror at commit via `EXTERNAL_PROVENANCE_RECORDED`.
- **D-GS5M-5:** Three-state advisory staleness enum (FRESH / STALE / UNAVAILABLE). CORE external facts raise `REQUIRES_HUMAN_REVIEW` on first non-FRESH detection.
- **D-GS5M-6:** Pruning Agent extended with `external_source_audit` sub-routine. No new component. External-audit failures isolated from Git-side pruning operation.

### 2.5 New Constraints (GAP-11)

- **C-EXT-PROV-1:** Layer 4 external facts without structurally valid `external_provenance` MUST be rejected at compile.
- **C-EXT-PROV-2:** Staleness detection MUST be advisory. No automatic promotion of STALE/UNAVAILABLE to a blocking state.
- **C-EXT-PROV-3:** External-audit sub-routine failures MUST be isolated from Git-side Pruning Agent operation.
- **C-EXT-PROV-4:** CORE-importance Layer 4 external facts MUST raise `REQUIRES_HUMAN_REVIEW` on first transition out of FRESH.

### 2.6 New Interface Contracts (GAP-11)

- **IC-WE-EXT-PROV** — Write Engine Layer 4 provenance validation. Missing/malformed → `EXTERNAL_PROVENANCE_MALFORMED` (INTEGRITY, sync); Phase 1 rollback.
- **IC-PA-EXT-AUDIT** — Pruning Agent `external_source_audit` → State Ledger. Per-edge staleness verdict + rate-limited `EXTERNAL_AUDIT_SUSPENDED` emission on network partition.

### 2.7 New Ledger Entry Types (GAP-11)

- `EXTERNAL_PROVENANCE_RECORDED` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_STALE` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_UNAVAILABLE` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_MALFORMED` (INTEGRITY, sync)
- `EXTERNAL_AUDIT_SUSPENDED` (CONSISTENCY, async, rate-limited)

---

## 3. GAP-15 Residual Resolution — Stratification Key

### 3.1 Joint Stratification Rule

§11.14 said "stratified" without naming the key. Now specified: **joint stratification by `declared_importance` band + `namespace` (primary) + `age_bucket` (secondary).**

**Why namespace primary:** guards against the failure mode where a dominant namespace crowds out sparse namespaces from the sample, leaving them blind to post-compile regression. MEMIT's locality guarantees degrade non-uniformly; sparse-namespace blind spots are a real and known risk.

**Why age_bucket secondary:** post-compile interference concentrates in recently-written edges.

### 3.2 Sampling Algorithm

For each importance band ∈ {SUPPORTING, INCIDENTAL}:

1. Compute `n_band` from §11.14 base rates (SUPPORTING 20% floor 5; INCIDENTAL 10% floor 3).
2. **Namespace pass:** partition edges by namespace; allocate per-namespace quota proportional to partition size; **floor 1 per non-empty namespace** (no-blind-spots invariant).
3. **Age pass:** within each namespace quota, allocate 40% from `<7d`, 40% from `7–30d`, 20% from `>30d`. Empty-bucket redistribution proportional to adjacent non-empty buckets.
4. **Exhaustive-small-namespace rule:** if a namespace has fewer edges than its allocated quota, sample exhaustively.
5. Random seed drawn from compile-epoch hash; logged in `CompactionProbeReport`.

### 3.3 New Decisions (GAP-15 residual)

- **D-GS5M-7:** §11.14 SUPPORTING and INCIDENTAL stratification is jointly keyed on `declared_importance` band + `namespace` (primary) + `age_bucket` (secondary), with floor-1-per-namespace and fixed {<7d, 7–30d, >30d} age buckets.

### 3.4 New Constraints (GAP-15 residual)

- **C-OC3-STRAT-1:** SUPPORTING and INCIDENTAL stratified sampling MUST use joint stratification (band + namespace + age_bucket).
- **C-OC3-STRAT-2:** Every non-empty namespace within an importance band MUST receive at least one probe (no-blind-spots invariant). Actual sample may exceed base rate in deployments with many small namespaces; this is intended.
- **C-OC3-STRAT-3:** Random seed MUST be logged in `CompactionProbeReport`. Same seed MUST reproduce the same sample set.
- **C-OC3-STRAT-4:** Age bucket boundaries {<7d, 7–30d, >30d} are Tier 1 (immutable-downward); changes require a CEREMONY-style Ledger entry.

### 3.5 New Interface Contracts (GAP-15 residual)

- **IC-OC-STRAT** — Compaction Orchestrator → Behavioral Probe sampling plan. Plan is deterministic from overlay state + seed. Plan serialized into `CompactionProbeReport` pre-execution section. Probe executor cannot override plan. Plan computation failure → `COMPACTION_PROBE_FAILED`; existing overlays retained.

---

## 4. Cross-Domain Tension Check

| Domain | Tension surfaced? |
|---|---|
| MEMIT Specialist | Owned — all three resolutions. |
| Graph Data Architect | No — schema untouched. Provenance is metadata on the patch, not the triple. Probe template is metadata, not an edge-level attribute. |
| Warden | No new trust boundary. `external_provenance` block is signed as part of patch signing; no new signer registry changes. |
| Validation Contract Architect | Minor-additive — Validator gains probe template review responsibility and adversarial distractor generation. Preserves D32–D33 independence. |
| State Consistency Theorist | Minor-additive — Pruning Agent scope extended. No new component. Git-side and external-audit isolation is explicit. |
| Orchestration Comparativist | No — no new orchestration surfaces or new coordination points. |

No new cross-domain conflicts surfaced. All new infrastructure reuses existing patterns (patch metadata, Pruning Agent cadence, advisory Ledger emission).

---

## 5. Gap Session Summary Block

**GAPS RESOLVED:**

- **GAP-9** — Behavioral probe generalization fully specced. Three-mode protocol (templated_recall, forced_choice, generation_consistency) declared per-edge in patch metadata (D-GS5M-1). Coder-authored + Validator-reviewed split preserves actor-critic independence (D-GS5M-2). CORE two-probe gate ratified (D-GS5M-3). Compile enforces structural presence; Validator enforces template quality.
- **GAP-11** — Layer 4 external document provenance fully specced. Mandatory hash-pinned `external_provenance` block (D-GS5M-4). Three-state advisory staleness enum with CORE-only REQUIRES_HUMAN_REVIEW escalation (D-GS5M-5). Pruning Agent extended via `external_source_audit` sub-routine (D-GS5M-6). Compile is presence-and-shape-only; no live refetch.
- **GAP-15 residual** — §11.14 stratification key fully specified. Joint stratification on `declared_importance` + `namespace` (primary) + `age_bucket` (secondary), with floor-1-per-namespace no-blind-spots invariant and fixed Tier 1 age bucket boundaries (D-GS5M-7).

**GAPS PARTIALLY RESOLVED:**
- None. All three targets fully resolved.

**GAPS DEFERRED:**
- None from GS5M scope.

**NEW GAPS SURFACED:**
- **OQ-VC-PROBE-1 (new)** — Adversarial probe template review heuristics. What exactly constitutes a "trivially-passing" template beyond the three degenerate cases named (empty expected, self-referential prompt, empty consistency_check)? Deferred to Validation Contract Architect. Medium priority.
- **OQ-W9 (new)** — Provenance for Layer 4 facts extracted from multi-source synthesis. When a model reads 3 documents and synthesizes a fact, which source gets hash-pinned? Current spec assumes single-source extraction. Deferred. Low-medium priority.

**NEW TENSIONS SURFACED:**
- None. Cross-domain check clean (§4).

**NEW DECISIONS (for v1.2 spec update):**

- D-GS5M-1 — Three-mode probe protocol declared per-edge in patch metadata.
- D-GS5M-2 — Coder-authored probe + Validator adversarial review; actor-critic independence preserved.
- D-GS5M-3 — CORE edges require two-probe gate (forced_choice + generation_consistency).
- D-GS5M-4 — Mandatory `external_provenance` block for Layer 4 external facts; compile rejects without.
- D-GS5M-5 — Three-state advisory staleness enum (FRESH/STALE/UNAVAILABLE); CORE escalates REQUIRES_HUMAN_REVIEW on first non-FRESH.
- D-GS5M-6 — Pruning Agent gains `external_source_audit` sub-routine; failures isolated from Git-side pruning.
- D-GS5M-7 — §11.14 stratification jointly keyed on band + namespace (primary) + age_bucket (secondary); floor-1-per-namespace invariant; age buckets fixed Tier 1.

**NEW CONSTRAINTS:**

- C-PROBE-GEN-1 through C-PROBE-GEN-4 (probe template mandatoriness, actor-critic independence, mode-specific structural requirements, CORE two-probe gate).
- C-EXT-PROV-1 through C-EXT-PROV-4 (provenance mandatoriness, advisory-only staleness, Git-pruning isolation, CORE REQUIRES_HUMAN_REVIEW escalation).
- C-OC3-STRAT-1 through C-OC3-STRAT-4 (stratification key, no-blind-spots, reproducibility, age bucket Tier 1).

**NEW INTERFACE CONTRACTS:**

- IC-WE-PROBE-SCHEMA — Write Engine probe_template structural validation.
- IC-VAL-PROBE-REVIEW — Validator probe template review and distractor generation.
- IC-WE-EXT-PROV — Write Engine Layer 4 provenance validation.
- IC-PA-EXT-AUDIT — Pruning Agent external_source_audit → State Ledger.
- IC-OC-STRAT — Compaction Orchestrator → Behavioral Probe sampling plan.

**NEW LEDGER ENTRY TYPES:**

- `PROBE_TEMPLATE_MALFORMED` (INTEGRITY, sync)
- `EXTERNAL_PROVENANCE_RECORDED` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_STALE` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_UNAVAILABLE` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_MALFORMED` (INTEGRITY, sync)
- `EXTERNAL_AUDIT_SUSPENDED` (CONSISTENCY, async, rate-limited)

---

**Session exit posture:** Three write-engine-centered gaps closed with spec language. Two new open questions surfaced, both medium-or-lower priority and non-blocking. v1.1 integrated spec gains seven new decisions (D-GS5M-1 through D-GS5M-7), twelve constraints across three clusters, five interface contracts, and six Ledger entry types. No cross-domain tensions. Ready for absorption into v1.2 integrated spec. Merge-time renumbering of D-GS5M-N into canonical D-series is expected.

**Merge-time note for spec integrator:** If GS9 (SCT-led) has also resolved GAP-11 in a separate thread, the two resolutions are structurally compatible — both adopt mandatory provenance, three-state advisory staleness, and Pruning Agent sub-routine extension. Cross-check field names and Ledger entry type names for exact consistency before merge; the patterns are aligned but the lexical choices may differ by session.
