# Spec ↔ Experiment Overlay — the durable cross-map

**Purpose.** A single durable, legible map from **spec sections** (`research_and_specs/llm-as-database-v1_2-integrated-spec.md`) to **the experiments / decisions that bear on them**. This is the backbone of the F1 reconciliation: F1 = "for each load-bearing spec claim, what does our evidence say — validated, amended, or open?" Built 2026-06-21 on operator instruction ("spec arcs should be overlaid and associated with our experiments very durably and clearly").

**How to use.**
- **Before framing any spec question as "open"/"an operator decision"** → check here + the spec section directly (DISCIPLINE §1 SPEC-FIRST rule). The spec often pre-decides what looks open.
- **When an experiment closes** → add/update its row(s) here as part of the close-out set (DISCIPLINE §1.1). Carry a **pointer + one-line verdict**, not a restated copy (de-dup norm) — full detail lives in the cited `CORPUS/NN` / decision doc.
- **Status legend:** `VALIDATED-for-scope` (our evidence supports the spec claim within tested scope) · `AMENDED` (our evidence requires a concrete change to the spec text) · `PROTOTYPED` (self-authored contract prototype, design-viability only, not empirical) · `OPEN` (bears on F1, not yet resolved) · `PScope` = the scope qualifier (e.g. 3B / N≤100 / batch).

---

## A. The in-weight thesis & read contract (the B3 axis)

| Spec section | What it requires / claims | Our experiment(s) + Decision-ID | Finding (pointer) | Status |
|---|---|---|---|---|
| **§1 Purpose/Paradigm** (line 88–90) | The thesis: shift from in-context (RAG) to **in-weight** — agents "natively know" without prompt reconstruction; FFN as queryable+editable graph DB | **B3 necessity** `D-B3N-1`; G6.1 `D-G6-1` | In-weight is NOT *contractually* required; "native knowing" = a stated **preference**, not a tested hard requirement. Verdict = compaction-bounded hybrid is in-weight-viable under 2 conditions. `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md` | **DECIDED** (reasoned position, not a PASS) |
| **§8.9 L1 Storage probe** (line 391) | `SELECT` read-back confirms an edge was written (mandatory all writes) | metric backbone of every edit run; **CP2** (queued) | Our top-1/expression metrics are the L1 read-back instrument; clean on batch path | **VALIDATED-for-scope** (PScope 3B/N≤100); CP2 formalizes the query surface — **OPEN** |
| **§ Schema D4** reverse lookup (line 287) | Bidirectional traversal; every edge reverse-lookable; no write-only edges | **E3 / CP2** (read-contract surface) | Side-store satisfies (EV-2 KG ≥ vector-RAG on multi-hop); in-weight reverse-read **untested** as such | **OPEN** (CP2/E3) |
| **§8.9 L2 Behavioral probe** | Generation test confirms the fact fires in inference (CORE/SUPPORTING); `behavior_fail` is a named non-success | autoregressive top-1 discipline; E1 `D-E1-1` | We measure behavioral firing (not teacher-forced) — aligns with the spec's storage-pass/behavior-fail distinction; consistent with Mirage/Editing-Overfit critiques | **VALIDATED-for-scope** |

## B. The write model & drift (the D1/§8.7 arc — our richest evidence)

| Spec section | What it requires / claims | Our experiment(s) + Decision-ID | Finding (pointer) | Status |
|---|---|---|---|---|
| **§8.3 Two operating modes** | **Genesis Mode** (batch compile) + **Incremental Mode** (per-commit patches via L1 Cache → MEMIT) | A1 `D-A1-1` (batch); A0/G6.1 `D-G6-1` (incremental) | Batch ELIMINATES cross-entity corruption (100→100% N≤100); incremental/sequential corrupts held-out reads. The two modes have **materially different** corruption behavior | **VALIDATED-for-scope** (the mode distinction is real and consequential) |
| **§8.4 `.vindex` tier stack** | Frozen genesis tiers + `incremental_NNNN.vindex` per-commit overlays; tiered for independent rollback | A1, B3 `D-B3-1` (quant on the stacked store) | Stacked-overlay store survives Q4_K_M quantization + CPU serve | **VALIDATED-for-scope** |
| **⭐ §8.7 Drift-from-anchor thresholds (T6)** | Drift measured since last anchor; **count-based**: warning 1,500 / hard 8,000 edges; `drift_state` exposes `edge_count_since_anchor` | **D1** `D-D1-1`, **B1** `D-B1-2`, **D-D1-2** (numeric instrument) | **The spec's count-only variable is the WRONG predictor** — corruption is **relation-concentration- + edit-order-dominated**, not edge-count-determined. → the **§8.7 concentration-aware amendment** (`max_relation_concentration_since_anchor`, worse-of vs global count; conservative `k≤1`). Model-general (3B+7B). `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`, CORPUS/22 | **AMENDED** (operator-approved structural amendment; numeric value 3B-set, 7B-transfer OPEN) |
| **§8.7 `p95_latency_ratio`** (376/846) | Latency health signal; tolerates 2× baseline before scheduling compaction | (read-side of B3N Axis A) | No hard zero-latency SLA → undercuts any "in-weight is required for latency" claim | **VALIDATED** (as evidence the read contract is not latency-hard) |
| **§8.10 Compaction** (line 413) | Full MEMIT re-run on archived patches every ≤30 days / at drift trigger; **resets anchor to clean**; delta-composition rejected | A1 `D-A1-1`; **D20 `D-D20-1` (CORPUS/23)** | Compaction = a batch rebuild → A1 clean at N≤100 single-batch. **D20 (DIRECTIONAL, gpt-5.5-tightened):** engine does a single joint solve (the 2,000 cap is a *spec prescription*, line 384); *accumulating sequential sub-batching can reintroduce corruption even when the joint solve is clean* — order-insensitive at ~10 sub-batches (−19 to −34pp). So **"returns to clean" cannot be NAIVELY assumed once compaction sub-batches** — but **NOT proven the spec's 2,000-SIZE compaction fails:** K-vs-C confound (count vs size) open + spec sub-batch semantics unverified. *Open:* 2D N×C grid + single-solve at true scale (component 1; connects to §10.4). | **CHUNKING = DIRECTIONAL PRESSURE on condition 3 (D20, not a falsification)**; **scale + K/C disambiguation = OPEN** |
| **§8.2 Two safeguards (D20)** | Orthogonal projection + covariance balancer in the solve | AlphaEdit recipe (null-space P + cache_c); A2 sentinels `D-A2-1` | Our in-solve AlphaEdit is the D20-aligned write path; sentinels extend D20 (partial mitigation) | **VALIDATED-for-scope** |
| **§10.4 agent edit caps / MEMIT batch size** (line 384, 528) | MEMIT recommended batch size **2,000** — patches above are **sub-batched internally** (sequential); Architect 10k/patch, Coder 500 | our N≤100 scope; **⚠ feeds B3N condition 3** | We operate far below the spec's batch ceiling; **sub-batching above 2,000 = sequential solves = the corruption mechanism** → makes compaction-at-scale (§8.10 row) the sharpest open falsifier. Large-N batch/compaction cleanliness **untested** | **OPEN** (scope gap: N≤100 ≪ 2,000 sub-batch boundary; the §8.10 self-heal rests on this) |
| **OQ-W1** (drift thresholds provisional) | Spec explicitly leaves drift threshold numbers to empirical calibration | D1 / B1 / D-D1-2 | This OQ is **exactly** what the §8.7 amendment arc answers (3B set; cross-model transfer open) | **OPEN→partially answered** |

## C. Deployment / CPU serve

| Spec section | What it requires / claims | Our experiment(s) + Decision-ID | Finding (pointer) | Status |
|---|---|---|---|---|
| **Deployment thesis** (CPU serve of the in-weight store) | The edited model serves on commodity/CPU hardware | **E1** `D-E1-1`, **B3** `D-B3-1` | Q4_K_M quantization survives (edited 100% vs native 97.4%); llama.cpp CPU serves edits. LARQL `gguf-to-vindex` cannot serve Qwen2.5-3B (bias-drop, A7 causal) → model-family split | **VALIDATED-for-scope** (Claim A); LARQL ingest path **FALSIFIED** for Qwen2.5 |
| **§7.7 Project Genesis (four layers)** | Initial knowledge compile in 4 tiers (schema/domain/constraints/knowledge) | A1 Genesis path `D-A1-1` | Genesis = the batch path = clean | **VALIDATED-for-scope** |

## D. Governance substrate (contract prototypes — design-viability only)

| Spec section | What it requires | Our prototype | Status |
|---|---|---|---|
| **§11 2PC / Transaction Controller, §12 Consistency, §14 scope-mismatch, §20 CeremonyToken** | Two-medium atomic writes, circuit breaker, ledger, ceremony auth | **CP1–G3** governance prototypes | **PROTOTYPED** (self-authored — tests our own control-flow, NOT the contract empirically; [[prototype-tautology-trap]]). Not promotable as evidence. |
| **Query/read contract** (LQL, query families) | The DB read surface: triple-readback, reverse, aggregation, negation, 5 relation families | **CP2** (query-schema build-items) | **OPEN — required for F1** (L1 triple-readback + 5 query families + violates-rejection) |

---

## E. F1 readiness roll-up (what this overlay says about the north star)

- **Data-path spine** (recipe → A1 batch-clean → B3 Q4_K_M → E1 CPU-serve): **VALIDATED-for-scope** (3B / N≤100).
- **The §8.7 drift contract: AMENDED** — the spec's count-only trigger is the wrong variable; the concentration-aware amendment is the F1 deliverable from the D1/B1 arc (numeric value 3B-set; **7B transfer = next science**).
- **B3 in-weight-necessity: DECIDED** — the spec's compaction-bounded hybrid is in-weight-viable under 2 conditions (concentration-aware §8.7 + compaction cadence); side-store only for high-churn-online beyond the spec.
- **⚠ Sharpest open falsifier (advisor reconcile, 2026-06-21): compaction-at-scale cleanliness.** The §8.10 self-heal ("compaction returns to clean") is validated only at N≤100/3B single-batch, but compaction at realized drift (1,500–8,000 edges, sub-batched above MEMIT's 2,000) is sequential-solve = the corruption mechanism. **Test: does the batch/compaction path stay clean at N≥2,000? Run at or above the 7B transfer** — if it fails, the in-weight hybrid needs the side-store. (B3N condition 3; connects the §8.10 + §10.4 rows.)
- **Still OPEN / blocking F1:** **compaction-at-scale cleanliness (above)**; CP2 query contract; reverse-read in-weight (D4); the §1.1 architecture dims (auditability/governance/security/routing/cost); 7B numeric transfer (OQ-W1).

_This overlay is a living tracker. Keep it current as part of the experiment close-out set (DISCIPLINE §1.1). Pointers, not copies — full detail in the cited `CORPUS/NN` / decision docs._
