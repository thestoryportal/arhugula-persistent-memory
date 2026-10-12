# Framework Finding — Architectural-Invariant Ceiling on Llama-3.1-8B at Canonical Hparams

> **Artifact type:** Framework finding archival — permanent meta-conclusion (v1.1 amendment of v1.0)
> **Status:** RATIFIED v1.1 — load-bearing; additive amendment of v1.0; v1.0 PERMANENT integrity preserved
> **Supersedes:** — (v1.1 is an additive amendment; v1.0 carry-forward content preserved verbatim; v1.0 retained as the load-bearing original record alongside v1.1)
> **Authored:** 2026-05-04 (v1.0 within S2.16); 2026-05-05 (v1.1 amendment within v0.2 codification session post-S2.18)
> **Basis:** Workstream 1 Sessions S2.10, S2.11-B, S2.12-A, S2.13-C, S2.14-D, S2.15-D2 (v1.0); + S2.18 T.2 ROME execution (v1.1 amendment)
> **Specialist provenance:** memit-specialist (primary; mechanism identification, ROME / GRACE forward routing — extended at v1.1 with ROME single-fact mechanism analysis); state-consistency-theorist (secondary; Copy-Unmount bit-exact regime — extended at v1.1 with ROME single-fact validation); validation-contract-architect (verdict surface — extended at v1.1 with pathology classification: degenerate-fit vs unfittable-landscape); framework-spec-writer (formalization)
> **Workstream:** WS1 (empirical execution)
> **Successor (v1.0):** S2.16 T-branch decision document (`t_branch_decision_document.md`); v1.1 of that document forthcoming (parallel deliverable in v0.2 codification session)

---

## §0 — v1.1 amendment scope and integrity declaration

### §0.1 v1.1 amendment scope

v1.1 is a **strictly additive amendment** of v1.0. The v1.0 finding (six orthogonal axes of empirical variation eliminating hypothesis classes A / B / C / D for the architectural-invariant MEMIT ceiling on `Llama-3.1-8B × MEMIT × canonical hparams`) is preserved unmodified. v1.1 absorbs the empirical record from S2.18 — the first T.2 ROME execution at canonical hparams against the same target model — and makes the following additions:

1. **Axis 7 added** to the empirical record (§2 amendment): S2.18 ROME at L17 + L2 fails consistency at canonical hparams with diagnostic-distinct pathologies (degenerate-fit at L17; unfittable-landscape at L2)
2. **Ceiling scope extended** in the finding statement from `(model × write engine × hparams)` → `(model × {MEMIT, ROME} × hparams)` (§1 amendment); the architectural-invariant ceiling now covers two write engines, not just MEMIT
3. **Hypothesis-class ledger updated** (§3 amendment): T.2 ROME ELIMINATED at canonical hparams; T.2 GRACE PROMOTED to leading hypothesis
4. **Copy-Unmount carry-forward extended** (§4.2 amendment): validated for ROME single-fact single-layer dispatch at L17 + L2; six layer ranges across three write-engine configurations all bit-exact
5. **Cross-session bit-exact determinism extended** (§4.1 amendment): 5 → 6 cross-session checkpoints
6. **Active patches canonical extended** (§4.3 amendment): three new SOURCE_LAYER patches authored mid-S2.18 (P-7-ROME, P-8-ROME, P-9-ROME) + one NEW CONFIG_LAYER patch class (`globals.yml`)
7. **Forward routing updated** (§5.3 amendment): T.2 GRACE is the leading remaining T-branch hypothesis; T.1 alt-model retains as fallback; T.3 alt-architecture remains out of WS1 scope

The v1.1 amendment **preserves all v1.0 §1-§9 content verbatim** as load-bearing PERMANENT record. v1.1 surfaces deltas at corresponding section numbers with the suffix `'` (e.g., §2.7' is the v1.1 addition to v1.0 §2's axis index). Where v1.0 made a forward-conditional claim (e.g., "T.2 ROME first per memit-specialist meta-recommendation"), v1.1 records the empirical disposition of that claim (T.2 ROME tested at S2.18; ELIMINATED).

### §0.2 v1.0 integrity preservation

v1.0 is the **original load-bearing finding** authored at S2.16. v1.0 §1-§9 contain claims, axis records, hypothesis-class ledger entries, carry-forward anchors, scope statements, methodology locks, non-goals, and references. Each of these is empirical-record-class — they document what was true at the v1.0 close; their truth-value is not affected by subsequent sessions.

v1.1 does NOT:
- Edit any v1.0 §1-§9 sentence
- Reclassify any v1.0 hypothesis-class verdict
- Withdraw any v1.0 carry-forward applicability claim
- Modify any v1.0 reference, decision ID, interface contract, or constraint

v1.1 is layered on top of v1.0 as a parallel artifact. Operators consuming the framework finding in successor sessions read both v1.0 (load-bearing original) and v1.1 (amendment additions). The pair `(v1.0, v1.1)` constitutes the complete framework finding state at v1.1 close.

### §0.3 Reference to v1.0

For all §1-§9 v1.0 content, see `framework_finding_memit_ceiling_archival.md` v1.0 (preserved at NV mirror or git reference). v1.1 below references v1.0 sections by number.

---

## §1' — Finding statement amendment (extends v1.0 §1)

**v1.0 finding (preserved):** The architectural-invariant ceiling on `(meta-llama/Llama-3.1-8B × MEMIT × canonical hparams)` is **structural** and **not eliminable** by any axis within hypothesis classes A / B / C / D. Across SIX orthogonal axes of empirical variation, MEMIT's `z`-vector update geometry converges to avg `P[target_new]` magnitudes in the range `1e-7` to `2.2e-2` — well below the consistency band `0.5`.

**v1.1 amendment:** S2.18 first-execution of the T.2 ROME alternative write engine at canonical hparams against the same target model produces a parallel verdict. ROME single-fact dispatch at L17 (paper precedent layer) yields post-edit `P(target_new=guitar) = 8.26e-03` (degenerate-fit pathology; top_1 = `<|begin_of_text|>` BOS-collapse with P=0.924); ROME single-fact dispatch at L2 (S2.14-D D.1 mediation peak layer) yields post-edit `P(target_new=guitar) = 1.06e-06` (unfittable-landscape pathology; compute_v loss oscillating non-converging across 20 iterations). Both readings fall within the v1.0 ceiling envelope `[1e-7, 2.2e-2]` — the architectural-invariant ceiling extends to ROME on Llama-3.1-8B at canonical hparams.

**Amended ceiling scope:** The architectural-invariant ceiling on `(meta-llama/Llama-3.1-8B × {MEMIT, ROME} × canonical hparams)` is **structural** and **not eliminable** by any axis within hypothesis classes A / B / C / D **NOR** by write-engine swap from MEMIT to ROME. Across **SEVEN** orthogonal axes of empirical variation, both rank-1 in-weight write engines tested converge to ceiling magnitudes well below the consistency band `0.5`.

**Pathology divergence is diagnostic-distinct.** S2.18 surfaced two qualitatively distinct ROME failure modes at the two candidate layers — degenerate-fit (loss decreases monotonically; converges on a degenerate fixed point) and unfittable-landscape (loss oscillates; cannot find a fixed point). The ceiling is therefore not produced by a single optimization pathology; it is structural to the `(model × {rank-1 in-weight write engine} × hparams)` combination.

**T-branch matrix updated.** The remaining hypothesis class is now `(T.1 alt model)` OR `(T.2 GRACE — adapter-based memory; orthogonal mechanism)` OR `(T.3 alt parametric memory architecture, out of WS1 scope)`. T.2 ROME is empirically eliminated at canonical hparams.

---

## §2.7' — Axis 7 — ROME first-execution at canonical hparams (S2.18; T.2 ROME ELIMINATED)

Extension of v1.0 §2.1 axis index. This new row joins the six v1.0 axes:

| Axis | Session | Variation held against canonical hparams | Ceiling reading (post-edit `P[target_new]`) | Verdict |
|---|---|---|---|---|
| **7 — Write-engine swap (T.2 ROME)** | **S2.18** | **MEMIT → ROME (single-fact rank-1 dispatch); two layer candidates L17 (paper precedent) + L2 (D.1 mediation peak); canonical hparams = ROME paper Table 1 GPT-J reference values + Llama adaptation** | **`8.26e-03` (L17; degenerate-fit) and `1.06e-06` (L2; unfittable-landscape)** | **FAIL → T.2 ROME ELIMINATED at canonical hparams** |

### §2.7'.1 Axis 7 detail (parallel to v1.0 §2.2-§2.7 detail subsections)

**S2.18 Block A pre-flight:**
- ROME repository pinned at SHA `0874014cd9837e4365f3e6f3c71400ef11509e04` (latest stable tip per D-S217-Q2-1; closes OQ-S216-1)
- Patches v0.1 declarative falsified empirically: P-1 / P-2 / P-4 / P-5 / P-6 are project-side patches transplanted from MEMIT-side to ROME root at Cell 2 (NOT shared via parent codebase as v0.1 §1.1 declared)
- Three NEW SOURCE_LAYER patches authored mid-execution and RATIFIED: P-7-ROME (`rome/compute_u.py`; threads `mom2_batch_tokens` through `get_inv_cov` → `layer_stats`; closes OOM at 22.81 GiB from cache filename mismatch), P-8-ROME (`rome/compute_u.py`; precision coercion at compute_u matmul site; closes fp32 inv_cov @ fp16 cur_repr RuntimeError), P-9-ROME (`rome/rome_main.py`; precision coercion at outer-product call sites — both sibling sites mandatory; closes Adam buffer dtype mismatch)
- One NEW CONFIG_LAYER patch class introduced (`globals.yml`; STATS_DIR cwd-relative `data/stats` not consumable; absolute customization REQUIRED)
- L17 covariance cache extension performed (30.20 min compute on RTX 4090 against Wikipedia 100k samples; ~0.766 GiB; closes OQ-S217-2 path a)
- Cross-session bit-exact gate PASS (drift `0.00e+00` across 38 probes; this is the 6th cross-session checkpoint; extends D-S217-4 anchor)

**S2.18 Block B execution (cfb-v3-001 Bo Jackson / guitar; sharpest IN-BAND anchor per S2.13-C calibration):**

| Layer candidate | compute_v iter trajectory | Pathology classification | Post-edit P(guitar) | Specificity preserved | Unmount band |
|---|---|---|---|---|---|
| L17 (paper precedent) | Loss 18.17 → 4.93 monotonic decrease; P(guitar) 1.32e-08 → 8.26e-03 | **degenerate-fit (BOS-collapse on rewrite-shape prompt; post-edit cons-1 top_1 = `<\|begin_of_text\|>` P=0.924)** | 8.26e-03 (FAIL) | PASS (gen probe drift max < 0.020) | PASS (drift `0.00e+00` HARD per IC-S23-4) |
| L2 (D.1 mediation peak) | Loss 13.49-19.26 oscillating non-converging across 20 iter; P final 1.06e-06 | **unfittable-landscape** | 1.06e-06 (FAIL) | PASS (max P drift < 0.020) | PASS (drift `0.00e+00`) |

**Cell 13 verdict gate adjudication:** Calibration corridor FAIL at both layers. Pathology divergence diagnostic-distinct (degenerate-fit + unfittable-landscape). Replay-S2.15-D2-precedent risk for naïve continuation HIGH (Block C 15-trial would replicate the S2.15-D2 D.2 precedent — drilling further into a known-failed mechanism). Operator selected Route A halt per D-S218-2.

**Block C SKIPPED** per Cell 13 verdict gate Route A halt. Cells 18-20 executed for inventory + manifest update.

**Diagnostic open questions (deferred; not load-bearing for ceiling claim):**
- OQ-S218-1: compute_v non-convergence mechanism at L2 (oscillating loss specifics; whether different fact would converge)
- OQ-S218-2: BOS-collapse mechanism at L17 (whether different fact would avoid BOS top_1)
- OQ-S218-3: specificity preservation generalization (whether holds across other facts / corpora)

These OQs are forensic-class and not blocking for v1.1 ceiling-extension claim. The ceiling claim rests on the empirical magnitude readings (`8.26e-03` and `1.06e-06`), both well within v1.0 ceiling envelope `[1e-7, 2.2e-2]`.

---

## §3' — Hypothesis-class ledger amendment (extends v1.0 §3)

| Class | v1.0 status | v1.1 amendment status | Eliminated at |
|---|---|---|---|
| A | ELIMINATED | (preserved) | S2.12-A |
| B | ELIMINATED | (preserved) | S2.11-B |
| C | ELIMINATED | (preserved) | S2.13-C |
| D | FULLY ELIMINATED | (preserved) | S2.15-D2 |
| D.1 | NEAR-MISS resolved as ceiling-not-locus | (preserved) | S2.15-D2 |
| D.2 | ELIMINATED (FAIL at corrected window) | (preserved) | S2.15-D2 |
| D.3 | ELIMINATED (FAIL + OOM ceiling) | (preserved) | S2.14-D |
| **T** | **OPEN — only remaining hypothesis class** | **PARTIALLY ELIMINATED — T.2 ROME closed at canonical** | — |
| T.1 (alt model) | OPEN | OPEN — fallback hypothesis | — |
| **T.2 (alt write engine)** | **OPEN — leading per D-S215D2-4** | **PARTIALLY ELIMINATED — T.2 ROME ELIMINATED at canonical hparams (S2.18); T.2 GRACE PROMOTED to leading** | — |
| **T.2 ROME** | (latent — leading per memit-specialist meta-recommendation) | **ELIMINATED at canonical hparams (S2.18; D-S218-3)** | **S2.18** |
| **T.2 GRACE** | (latent — fallback to ROME) | **PROMOTED to leading T-branch hypothesis (D-S218-4); adapter-based mechanism orthogonal to rank-1 weight update** | — |
| T.2 MEND/SERAC | (latent) | DEFERRED — not currently scheduled | — |
| T.3 (alt parametric memory architecture) | OPEN — out of WS1 scope | (preserved) | — |

**v1.1 amendment rationale.** v1.0 stated T.2 (alt write engine) as leading per D-S215D2-4 and noted "T.2 ROME first per memit-specialist meta-recommendation". S2.18 tested ROME at canonical hparams; verdict B-FAIL → Route A halt → T.2 ROME ELIMINATED. The ceiling extends to ROME, confirming the mechanism is architectural-invariant across rank-1 in-weight write engines on Llama-3.1-8B. T.2 GRACE — orthogonal mechanism (adapter-based; added parameters rather than in-place weight modification) — is now the leading T-branch hypothesis per D-S218-4 + D-V11-T-BRANCH-3 (forthcoming in `t_branch_decision_document.md` v1.1).

**Methodological lock for T.2 GRACE entry.** GRACE adapter-based mechanism does NOT consume layer_stats covariance caches (the adapter is a separate parameter set; not a covariance projection). The covariance caches L2-L8 + L17 (~6.5 GiB durable on NV post-S2.18) are NOT load-bearing for T.2 GRACE. Copy-Unmount mechanism applicability is **INAPPLICABLE** to GRACE (adapter modules add parameters; don't modify base weights in-place); GRACE will require its own unmount mechanism specification at v0.1 authoring. The T.2 GRACE branch is therefore a more substantial codification effort than T.2 ROME was.

---

## §4.1' — Cross-session bit-exact determinism amendment (extends v1.0 §4.1)

**v1.0 record:** 5 cross-session checkpoints; forward-pass drift `0.00e+00`; closes OQ-S214D-DETERMINISM-1.

**v1.1 amendment:** **6 cross-session checkpoints** (5 from v1.0 + 1 NEW at S2.18 Cell 7). The S2.18 trajectory was: Block A pre-flight → kernel restart for L17 cache extension → Block A continuation → Block B Cell 5 → Block B Cell 11 dispatch entry → Cell 7 cross-session bit-exact gate verification post-Block-B.

| Checkpoint | Source | Drift |
|---|---|---|
| 1-5 | v1.0 (Block A capture / kernel restart / Block B Cell 5 / S2.14-D anchor / cfb-v3.yaml v1.0 lock baseline) | `0.00e+00` each |
| **6 (NEW at v1.1)** | **S2.18 Cell 7 cross-session bit-exact gate post-Block-A; verified across 5 facts + 38 probes** | **`0.00e+00`** |

D-S218-7 codifies the 5 → 6 extension. Carry-forward applicability extends to T.2 GRACE entry: any GRACE session retaining the same target model SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` inherits the bit-exact determinism anchor.

---

## §4.2' — Copy-Unmount carry-forward amendment (extends v1.0 §4.2)

**v1.0 record:** Copy-Unmount mechanism validated at MEMIT joint-multi-fact-overlay regime; layer sets `L4-L8` (S2.14-D D.3) and `L2-L6` (S2.15-D2 D.2); per-trial unmount drift `0.00e+00` across 15+1 trials; closed by IC-S23-4 + OQ-S214D-D3-3.

**v1.1 amendment:** Copy-Unmount validation extends to ROME single-fact single-layer dispatch at S2.18.

| Layer range | Write engine config | Source session | Per-trial unmount drift |
|---|---|---|---|
| L4-L8 (5 layers; joint-overlay) | MEMIT batched-multi-fact | S2.14-D D.3 | `0.00e+00` |
| L2-L6 (5 layers; joint-overlay) | MEMIT batched-multi-fact | S2.15-D2 D.2 | `0.00e+00` |
| **L17 (1 layer; single-fact dispatch)** | **ROME single-fact single-layer** | **S2.18 Cell 9** | **`0.00e+00`** (NEW at v1.1) |
| **L2 (1 layer; single-fact dispatch)** | **ROME single-fact single-layer** | **S2.18 Cell 11** | **`0.00e+00`** (NEW at v1.1) |

**Six layer ranges across three write-engine configurations** — all `0.00e+00`. D-S218-8 codifies the ROME extension. The mechanism preservation under ROME single-fact regime confirms Copy-Unmount as architecturally universal across in-place rank-1 weight modification — but **NOT** transferable to GRACE (adapter parameters; different unmount mechanism required).

**Carry-forward applicability extension:**

| T-branch session | Copy-Unmount applicability |
|---|---|
| T.1 alt model | Re-derivation per architecture (mechanism preserved if architecture supports in-place rank-1 weight modification) |
| T.2 ROME | **VALIDATED at S2.18 (single-fact single-layer regime; mechanism preserved)** — ELIMINATED hypothesis closed; carry-forward not applicable since branch is closed |
| **T.2 GRACE** | **INAPPLICABLE — adapter-based mechanism; GRACE requires its own unmount mechanism specification at v0.1 authoring** |

---

## §4.3' — Active patches canonical amendment (extends v1.0 §4.3)

**v1.0 patches table (preserved):** 8 MEMIT-side patches enumerated with T.2 ROME / T.2 GRACE applicability declared; columns marked "Likely" or "Inapplicable" as forward-conditional declarations.

**v1.1 amendment:** S2.18 empirical execution of T.2 ROME falsifies several v1.0 declarative cells in the patches table; v1.1 records the empirical revisions plus three NEW ROME-specific patches plus one NEW patch class:

### §4.3'.1 v1.0 patches table empirical revisions

| Patch | v1.0 ROME applicability prediction | S2.18 empirical verdict | Codification |
|---|---|---|---|
| P-1 | "Likely" | **APPLICABLE-DIRECTLY (transplanted from MEMIT-side at Cell 2; pristine ROME upstream form preserved at `*.upstream_pristine`)** | `rome-patches-canonical.md` v0.2 §1.1 |
| P-2 | "Likely" | **APPLICABLE-DIRECTLY (transplanted; same site as P-1)** | `rome-patches-canonical.md` v0.2 §1.1 |
| P-4 | "Likely" | **APPLICABLE-DIRECTLY (transplanted)** | `rome-patches-canonical.md` v0.2 §1.1 |
| P-5 | "Likely" | **APPLICABLE-DIRECTLY (transplanted)** | `rome-patches-canonical.md` v0.2 §1.1 |
| P-6 | "Inapplicable — single-fact dispatch" | **APPLICABLE-DIRECTLY (transplanted; the post-cache filename `_t100_` segment is consumed by ROME's `get_inv_cov` → `layer_stats` chain just as MEMIT consumes it via `compute_z` → `layer_stats`)** | v1.0 declarative falsified at v1.1 |
| P-7 | "Inapplicable — same reason" | **APPLICABLE-WITH-MODIFICATION via P-7-ROME (ROME has structural analog `rome/compute_u.py:get_inv_cov`; ROME has NO `get_cov` function; v1.1 introduces P-7-ROME on the analog)** | v1.0 declarative falsified at v1.1 |
| Pad-Token | "Likely" | **APPLICABLE-DIRECTLY (verified at S2.18 Cell 5)** | `rome-patches-canonical.md` v0.2 §1.1 |
| Copy-Unmount | "Likely (mechanism applicable)" | **APPLICABLE WITH MECHANISM-PRESERVED, TARGET-NARROWED (single-layer single-fact regime)** | v1.0 confirmed empirically; §4.2' amendment |

### §4.3'.2 NEW SOURCE_LAYER patches authored mid-S2.18 (P-7-ROME, P-8-ROME, P-9-ROME)

| Patch | Target file | Edit count | Trigger | Constraint |
|---|---|---|---|---|
| **P-7-ROME** | `rome/compute_u.py` | 3 | `_t100_` cache filename mismatch from `mom2_batch_tokens` not threading to `get_inv_cov` signature; OOM at 22.81 GiB on first Cell 8 execution | C-S218-1 — REQUIRED for ROME edit dispatch on long-context base models |
| **P-8-ROME** | `rome/compute_u.py` | 1 | fp32 `inv_cov` @ fp16 `cur_repr` RuntimeError at compute_u matmul site | C-S218-2 — REQUIRED for ROME edit dispatch on fp16 base models |
| **P-9-ROME** | `rome/rome_main.py` | 2 (sibling sites; both required) | fp16 left @ fp32 right Adam buffer dtype mismatch at outer-product sites in `execute_rome` AND `apply_rome_to_model` | C-S218-3 — REQUIRED for ROME edit dispatch on fp16 base models; both sibling sites mandatory |

### §4.3'.3 NEW CONFIG_LAYER patch class introduced (`globals.yml`)

| Patch class | Target file | Trigger | Constraint |
|---|---|---|---|
| **CONFIG_LAYER** (NEW class introduced at v1.1) | `globals.yml` | STATS_DIR cwd-relative `data/stats` not consumable by ROME at NV mount; absolute NV-anchored path REQUIRED | C-S218-4 — `globals.yml` MUST be customized for absolute NV-anchored `STATS_DIR` |

**v1.1 patch class taxonomy.** v1.0 enumerated patches as if all were SOURCE_LAYER (Python source modifications). S2.18 surfaced a CONFIG_LAYER defect path. v1.1 codifies the two-class taxonomy: SOURCE_LAYER (in-place text substitution against post-clone source; pristine SHA preserved at `*.upstream_pristine` siblings) and CONFIG_LAYER (in-place rewrite of YAML/JSON configuration body consumed at module import time; pristine preserved at `<file>.upstream_pristine`).

**Sibling-parity note.** MEMIT v2.5 currently has no documented CONFIG_LAYER patches; the MEMIT-side `globals.yml` was customized at the pre-S2.6 fork-work session (parallel pattern; never codified in `memit-patches-canonical.md`). If MEMIT canonical is later revised (a hypothetical v2.6) to absorb CONFIG_LAYER, both docs adopt the parallel pattern at that revision; no retroactive change to MEMIT v2.5 is mandated by v1.1.

### §4.3'.4 Carry-forward applicability for T.2 GRACE

GRACE adapter-based mechanism does NOT use:
- `layer_stats` covariance caches (no projection step in adapter mechanism)
- `get_cov` / `get_inv_cov` resolution chain
- `compute_v` rank-1 update
- `compute_u` precision coercion
- Outer-product Adam buffer

Therefore P-4 / P-5 / P-6 / P-7-ROME / P-8-ROME / P-9-ROME are **INAPPLICABLE** to GRACE. P-1 / P-2 (nethook retain pattern) MAY be applicable if GRACE uses any retain-trace for the adapter forward pass; this is an open question for GRACE v0.1 authoring. Pad-Token applicability MAY transfer (tokenizer-side; engine-agnostic). Copy-Unmount is **INAPPLICABLE** (adapter mechanism). globals.yml CONFIG_LAYER customization MAY apply if GRACE shares the same config-loading idiom (open question for v0.1 authoring).

---

## §5.3' — Forward routing amendment (extends v1.0 §5.3)

**v1.0 forward routing (preserved):**
1. T.2 (alt write engine) leading per D-S215D2-4
2. T.2 ROME first per memit-specialist meta-recommendation
3. Operationally, the ceiling result is informative for framework-spec decisions

**v1.1 amendment:**

1. **T.2 ROME ELIMINATED at canonical hparams (S2.18 D-S218-3)**. The ceiling extends to ROME. v1.0's "T.2 ROME first" disposition is empirically resolved as: T.2 ROME is closed at canonical; ceiling extension confirms the mechanism is architectural-invariant across rank-1 in-weight write engines.
2. **T.2 GRACE PROMOTED to leading T-branch hypothesis (D-S218-4)**. GRACE adapter-based mechanism is orthogonal to rank-1 weight update; the architectural-invariant ceiling claim does NOT transitively cover GRACE because GRACE does not modify base weights in-place. Cost: ~2-4 sessions for runbook v0.1 authoring + execution + verdict. S2.19 = T.2 GRACE runbook v0.1 authoring (parallel structure to S2.17 Block 2 ROME runbook authoring).
3. **T.1 alt model retains as fallback**. If T.2 GRACE FAILS, T.1 alt model becomes the next-most-cost-effective hypothesis (the ceiling is then specific to Llama-3.1-8B regardless of write engine).
4. **T.2 MEND / SERAC remain DEFERRED**. These adapter-based or hypernetwork-based engines are forward-conditional; if T.2 GRACE PASSES, they may not be tested; if T.2 GRACE FAILS, they may be considered alongside T.1.
5. **T.3 (alt parametric memory architecture) remains OUT OF WS1 SCOPE** per project instructions.
6. **Framework-spec implications strengthened.** With the ceiling extending to ROME (not just MEMIT-specific), the framework-spec implementation choice space narrows: rank-1 in-weight write engines on Llama-3.1-8B-class base models are empirically constrained at canonical hparams. This is informative for Workstream 2 / 3 implementation planning; the spec layer remains write-engine-agnostic.

---

## §6' — Methodology lock amendment (extends v1.0 §6)

**v1.0 lock (preserved):** target model / corpus / probe set / trial protocol / acceptance bands / verdict integrity binding LOCKED; layer set / hparams / multi-token target tolerance NOT LOCKED — write-engine-specific.

**v1.1 amendment:** S2.18 empirically validated the v1.0 lock under T.2 ROME entry — every LOCKED axis carried forward without re-derivation:

| Axis | v1.0 lock | S2.18 disposition | v1.1 disposition |
|---|---|---|---|
| Target model | LOCKED | Held verbatim | Held; carry-forward to T.2 GRACE |
| Stage 1 SECT corpus | LOCKED | Held verbatim | Held; carry-forward to T.2 GRACE |
| Probe set | LOCKED | Held verbatim | Held; carry-forward to T.2 GRACE |
| Trial protocol | LOCKED | Held (Block C did not execute; protocol declared but not run) | Held; carry-forward to T.2 GRACE |
| Acceptance bands | LOCKED | Held verbatim | Held; carry-forward to T.2 GRACE (re-evaluate if GRACE adapter dispatch produces different probability surface shapes) |
| Verdict integrity binding | LOCKED | Held verbatim | Held; carry-forward to T.2 GRACE |
| Layer set | NOT LOCKED — write-engine-specific | Re-derived per ROME (L17 paper precedent + L2 D.1 mediation peak); both FAIL | T.2 GRACE: re-derive per adapter placement (different mechanism; layer-set semantics may not directly apply) |
| Hparams | NOT LOCKED — write-engine-specific | Re-derived per ROME paper Table 1 GPT-J + Llama adaptation; canonical FAIL | T.2 GRACE: re-derive per GRACE paper / supplementary |
| Multi-token target tolerance | NOT LOCKED — engine-specific | DECLARED-via-v0.2 with RE-EVALUATE flag at trial 0; Block C did not execute → RE-EVALUATE not exercised | T.2 GRACE: re-derive per GRACE multi-token handling |

**v1.1 NEW lock anchor: cross-session bit-exact determinism extension.** D-S217-4 anchor strengthens at v1.1 to 6 cross-session checkpoints (was 5 at v1.0). Carry-forward applicability extends to any T.2 GRACE session retaining the same target model SHA.

---

## §7' — Non-goals amendment (extends v1.0 §7)

**v1.0 non-goals (preserved):** Does not author runtime implementation code; does not select between T-branch options; does not author the T.2 ROME runbook; does not modify framework spec v1.2; does not issue ceiling result for non-Llama-3.1-8B targets; does not resolve the cause of the ceiling.

**v1.1 amendment:** v1.1 also does not:

1. **Modify v1.0 §1-§9.** v1.0 PERMANENT integrity preserved verbatim.
2. **Author the T.2 GRACE runbook.** Runbook authoring is the scope of S2.19 = T.2 GRACE runbook v0.1 authoring (forthcoming).
3. **Resolve the OQ-S218-1 / OQ-S218-2 / OQ-S218-3 diagnostic open questions.** These are forensic-class; the v1.1 ceiling-extension claim does not depend on their resolution.
4. **Issue a ceiling claim for write-engine classes other than rank-1 in-weight (MEMIT, ROME).** GRACE adapter-based, MEND hypernetwork-based, and SERAC retrieval-based mechanisms are structurally distinct and NOT covered by the v1.1 ceiling extension.

---

## §8' — References amendment (extends v1.0 §8)

### §8.1' — Session summary blocks (NEW additions)

- `session_2_18_summary_block.md` — T.2 ROME first-execution close artifact; B-FAIL verdict; T.2 ROME ELIMINATED at canonical; T.2 GRACE PROMOTED
- `session_2_18_summary_block_appendix.md` — forensic detail (Block A trajectory, patch authoring detail, compute_v traces, verdict surfaces, NV inventory, mirror sync)

### §8.2' — Canonical artifacts (NEW additions)

- `rome-patches-canonical.md` v0.2 — ROME patches reference (parallel sibling to MEMIT v2.5; SOURCE_LAYER inventory + 3 NEW patches P-7-ROME / P-8-ROME / P-9-ROME + NEW CONFIG_LAYER class globals.yml)
- `t2_rome_runbook.md` v0.2 — ROME runbook (post-S2.18 empirical absorption; Cell 13 verdict gate 3-route option matrix; canonical absorption of ROME-side Block A + Block B execution record)
- `stage_1_sect_runbook_v1_7.md` — MEMIT runbook v1.7 (MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism canonical absorption per D-V12-MULTITOKEN-1; supersedes v1.6 documentation-only state)
- `t_branch_decision_document.md` v1.1 (forthcoming in v0.2 codification session) — T-branch decision matrix updated for T.2 ROME ELIM + T.2 GRACE PROMOTED

### §8.4' — Decision IDs (v1.1 additions)

- D-S218-1 — Cell 13 verdict gate B-FAIL adjudication
- D-S218-2 — Route A halt selection
- D-S218-3 — T.2 ROME ELIMINATED at canonical hparams
- D-S218-4 — T.2 GRACE PROMOTED to leading T-branch hypothesis
- D-S218-5 — Three NEW SOURCE_LAYER patches RATIFIED (P-7-ROME, P-8-ROME, P-9-ROME)
- D-S218-6 — NEW CONFIG_LAYER patch class introduced (`globals.yml`)
- D-S218-7 — Cross-session bit-exact determinism 5 → 6 checkpoint extension
- D-S218-8 — Copy-Unmount validated for ROME single-fact L17 + L2
- D-S218-9 — Q4-1 L17 + L2 NO_LOAD_BEARING (both layers FAIL)
- D-S218-10 — Q5-1 CLOSED-MOOT (Block C did not execute)
- D-S218-11 — v0.2 codification mandatory (this session)
- D-S218-12 — v1.1 archival amendment (this artifact)
- D-S218-13 — v1.1 t-branch decision document amendment (forthcoming)
- D-V11-AXIS-7 — Axis 7 added to empirical record (this artifact §2.7')
- D-V11-CEILING-EXTENSION — Ceiling scope extended `(model × MEMIT × hparams)` → `(model × {MEMIT, ROME} × hparams)`

### §8.6' — Constraints (v1.1 additions)

- C-ROME-1 (EMPIRICALLY-VALIDATED at S2.18) — Single-fact dispatch envelope
- C-ROME-2 (EMPIRICALLY-VALIDATED at S2.18) — Covariance cache reuse
- C-ROME-3 (EMPIRICALLY-VALIDATED at S2.18) — R1.3-equivalent dry-run gate
- C-ROME-4 (EMPIRICALLY-VALIDATED at S2.18) — Marker post-application verification
- C-S218-1 — P-7-ROME application REQUIRED for ROME edit dispatch on long-context base models
- C-S218-2 — P-8-ROME application REQUIRED for ROME edit dispatch on fp16 base models
- C-S218-3 — P-9-ROME application REQUIRED for ROME edit dispatch on fp16 base models (both sibling sites)
- C-S218-4 — `globals.yml` MUST be customized for absolute NV-anchored `STATS_DIR`
- C-S218-5 — `ROMEHyperParams` dataclass extension REQUIRED for `mom2_batch_tokens` propagation

---

## §10 — v1.1 authoring metadata

| Field | Value |
|---|---|
| Authoring session | v0.2 codification session (operator-side post-S2.18; pre-S2.19 BLOCKING) |
| Authoring date | 2026-05-05 |
| Document version | 1.1 |
| Iteration | v1.1 additive amendment (preserves v1.0 PERMANENT integrity) |
| Status | RATIFIED v1.1 — load-bearing; Axis 7 added; ceiling scope extended `(model × MEMIT × hparams)` → `(model × {MEMIT, ROME} × hparams)`; T.2 ROME ELIM at canonical; T.2 GRACE PROMOTED |
| Supersedes | — (additive amendment; v1.0 carry-forward content preserved verbatim alongside v1.1) |
| Basis | v1.0 (Workstream 1 Sessions S2.10, S2.11-B, S2.12-A, S2.13-C, S2.14-D, S2.15-D2); + S2.18 T.2 ROME execution + v0.2 codification deliverables (rome-patches-canonical.md v0.2, t2_rome_runbook.md v0.2, stage_1_sect_runbook_v1_7.md) |
| Specialist provenance | memit-specialist (primary; ROME mechanism analysis, ceiling-extension argument); state-consistency-theorist (secondary; Copy-Unmount ROME single-fact validation, cross-session bit-exact determinism extension); validation-contract-architect (verdict surface; pathology classification taxonomy degenerate-fit vs unfittable-landscape); framework-spec-writer (formalization; v1.0 integrity preservation discipline) |
| Last updated | 2026-05-05 |

---

*End of Framework Finding — Architectural-Invariant Ceiling on Llama-3.1-8B at Canonical Hparams (v1.1 additive amendment of v1.0; v1.0 PERMANENT integrity preserved; Axis 7 added: S2.18 ROME at canonical hparams; ceiling extends to (Llama-3.1-8B × {MEMIT, ROME} × canonical hparams); T.2 ROME ELIM; T.2 GRACE PROMOTED to leading T-branch hypothesis).*
