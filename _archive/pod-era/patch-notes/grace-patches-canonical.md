# GRACE Patches Canonical

> **Document version:** v0.1 (declarative; pre-empirical)
> **Authoring session:** S2.19 = T.2 GRACE runbook v0.1 authoring (operator-side post-v0.2 codification; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5')
> **Status:** RATIFIED v0.1 — declarative; empirical absorption deferred to v0.2 codification analog session post-S2.20 (parallel to ROME v0.1 → v0.2 absorption pattern)
> **Companion artifact:** `t2_grace_runbook.md` v0.1 (parallel sibling; authored at S2.19 Block 2)
> **Sibling artifacts:** `memit-patches-canonical.md` v2.5 (preserved unmodified per D-S216-CLOSE-3); `rome-patches-canonical.md` v0.2 (preserved post-elimination as historical record + carry-forward per `t_branch_decision_document.md` v1.1 §4'.1)
> **Specialist provenance:** memit-specialist (primary; GRACE adapter mechanism specification, hparam surface derivation from GRACE paper Table 1, mechanism-orthogonality argument cross-validation); state-consistency-theorist (secondary; adapter-detach unmount mechanism specification per C-GRACE-5, covariance cache inapplicability rationale, cross-session bit-exact determinism inheritance); orchestration-comparativist (write-engine architecture comparison surface; adapter-vs-rank-1-update structural comparison codified at §12.2 mechanism-class taxonomy); graph-data-architect (light-touch; framework-spec-relevance scoring for adapter-based mechanisms); validation-contract-architect (Cell 6 / Cell 7 / Cell 9 verdict surface inheritance for runbook companion artifact); framework-spec-writer (formalization; sibling-parity discipline preservation)
> **Workstream:** WS1 (empirical execution; T.2 GRACE entry; verdict-conditional C-FAIL branch active)

---

## §0 Purpose & non-amendment declaration

This document is the **parallel canonical patches reference for the GRACE write engine** under the T.2 GRACE work pre-committed at S2.19 and forthcoming at S2.20. It is structurally analogous to `memit-patches-canonical.md` v2.5 (the MEMIT patches canonical) and `rome-patches-canonical.md` v0.2 (the ROME patches canonical) but **does not amend either**. MEMIT canonical is preserved unmodified at v2.5 per D-S216-CLOSE-3; ROME canonical is preserved unmodified at v0.2 post-elimination per `t_branch_decision_document.md` v1.1 §4'.1. Three coexisting write-engine canonicals at S2.19 close: MEMIT v2.5 (preserved; no further work scheduled) + ROME v0.2 (preserved; historical record + carry-forward) + GRACE v0.1 (active forward-target).

**Document scope.** This canonical declares:

1. The **patch inventory** for the GRACE write engine on `meta-llama/Llama-3.1-8B`, partitioned by:
   - **SOURCE_LAYER patches** inherited from MEMIT/ROME: applicable directly (engine-agnostic; reduced to `Pad-Token` at v0.1), applicable with modification (`P-1` / `P-2` retain-trace pattern; OPEN at v0.1), or inapplicable (the majority — rank-1-in-weight mechanism specifics)
   - **SOURCE_LAYER patches** authored fresh for GRACE — DEFERRED at v0.1 declarative; absorbed at v0.2 codification analog session post-S2.20 first-execution (parallel to ROME v0.1 → v0.2 P-7-ROME / P-8-ROME / P-9-ROME absorption pattern)
   - **CONFIG_LAYER patches** — DEFERRED at v0.1 declarative; whether GRACE has a `globals.yml`-equivalent or similar config-loading idiom is OPEN until first-execution
2. The **SHA pin** for the GRACE repository under which patches are valid (per D-S219-Q1-1: latest stable tip of `https://github.com/Thartvigsen/GRACE`; specific SHA recorded at v0.2 absorption post-S2.20 Block A Cell 1)
3. The **process constraints** governing the GRACE patch surface (`C-GRACE-1` through `C-GRACE-5`; parallel structure to MEMIT `C-S26-1`/`-2`/`-3` + `C-S28-1` and ROME `C-ROME-1`..`-4` + `C-S218-1`..`-5`; reduced count at v0.1 declarative; expected expansion at v0.2 absorption)
4. The **applicability verdict matrix** mapping each MEMIT/ROME patch (`P-1`, `P-2`, `P-3'`, `P-4`, `P-5`, `P-6`, `P-7`, `P-7-ROME`, `P-8-ROME`, `P-9-ROME`, `Pad-Token`, `Copy-Unmount`, `Device-Map`) to its GRACE status (declarative-at-v0.1; some entries OPEN pending first-execution)

**v0.1 declarative status.** All v0.1 verdicts in this canonical are **declared** — best-judgment predictions based on: (a) the mechanism-orthogonality argument codified in `t_branch_decision_document.md` v1.1 §4'.2 and `framework_finding_memit_ceiling_archival.md` v1.1 §4.3'.4; (b) GRACE paper architectural description (Hartvigsen et al., adapter-based mechanism with discrete key-value codebook + routing-layer dispatch); (c) shared-tokenizer / shared-base-model carry-forward from MEMIT/ROME work. v0.2 absorption post-S2.20 will replace any declarative verdict superseded by empirical record. Where the v0.1 declarative form is uncertain, entries are marked **OPEN at v0.1**; these are first-class targets for v0.2 absorption.

**Reduced inheritance scope vs. ROME v0.2 (structurally inverted partition).** GRACE adapter mechanism is structurally distinct from rank-1 in-weight write engines (MEMIT + ROME). The architectural-invariant ceiling claim per `framework_finding_memit_ceiling_archival.md` v1.1 §1' Axis 7 covers `(Llama-3.1-8B × {MEMIT, ROME} × canonical hparams)` but does **not transitively cover GRACE** because GRACE does not implement the rank-1-in-weight mechanism class. This document records the inheritance scope reduction at §1.3 (INAPPLICABLE inventory; the largest partition at v0.1) and §1.1 (APPLICABLE-DIRECTLY inventory; the smallest partition at v0.1, structurally inverted relative to ROME v0.2 where APPLICABLE-DIRECTLY was the largest with five entries). The inversion is the structural signature of the engine-class transition: when most MEMIT-inherited patches reduce to INAPPLICABLE, the patches doc shifts from "what carries over" to "what does not carry over and why."

**Mechanism-orthogonality argument (load-bearing for §1 inventory partitioning).** GRACE adapter modules add parameters to the model rather than modifying base weights in-place. Specifically:

- **Adapter mechanism.** GRACE maintains a discrete codebook of key-value pairs at a specific layer position. Each codebook entry pairs an input activation pattern (key) with an output adjustment (value). At forward pass, a routing function computes distance between current input activation and stored keys; if within a threshold (`epsilon`), the adapter dispatches the matching value as a residual addition to the layer's output; otherwise the base model's normal forward pass proceeds unmodified.
- **No in-place weight modification.** Base model parameters (`model.model.layers[N].mlp.down_proj.weight` and equivalents) are NOT modified by GRACE edits. The adapter's parameters (codebook keys, codebook values, routing-function parameters) are stored as separate added tensors associated with the routing layer.
- **No covariance projection.** GRACE does not consume `layer_stats` covariance caches. The codebook key-value pairs are derived per-edit via gradient-based optimization (typically Adam) against an edit-loss objective; no projection step against pre-computed covariance is involved.
- **No outer-product update.** The rank-1 outer-product Adam buffer mechanism (`P-9-ROME` structural site) is INAPPLICABLE — GRACE does not perform rank-1 weight updates.
- **Different unmount semantics.** Copy-Unmount (in-place tensor restore via `weights_copy[name][...] = weights_copy_originals[name]`) is INAPPLICABLE because no in-place modification occurred. GRACE unmount = remove adapter from routing layer; restore base-model forward-pass behavior (per D-S219-Q4-1; codified at C-GRACE-5).

This argument is the structural rationale for why §1.3 INAPPLICABLE partition is large at v0.1 and why §1.4 NEW patches partition is reserved for v0.2 absorption rather than declarative authoring. It is also the load-bearing rationale for T.2 GRACE entry being the next test surface post-T.2-ROME-elimination per `t_branch_decision_document.md` v1.1 §4'.2.

**Empirical anchor reference at v0.1.** No GRACE-specific empirical record exists at v0.1 authoring. The carry-forward anchors at v0.1 are inherited from S2.13-C through S2.18 at the target-model + corpus + probe-set + trial-protocol layers (per `t_branch_decision_document.md` v1.1 §6'.1 and `session_v0_2_codification_summary_block.md` §8). v0.2 absorption post-S2.20 will record GRACE-specific empirical anchors at parallel structure to ROME v0.2 §0 empirical anchor reference.

---

## §1 Patch inventory

### §1.0 Patch class taxonomy (inherited from rome v0.2 §1.0; D-V02-6 carry-forward)

v0.1 inherits the two-class patch taxonomy introduced at `rome-patches-canonical.md` v0.2 per D-V02-6:

| Patch class | Definition | Examples (canonical) | Application semantics |
|---|---|---|---|
| **SOURCE_LAYER** | Patches that modify Python source files in the GRACE repository (`grace/*.py`, supporting modules) | (DEFERRED at v0.1; expected NEW patches at v0.2 absorption post-S2.20) | Applied via in-place text substitution against post-clone source; pristine SHA preserved at `<file>.upstream_pristine` siblings (parallel to ROME v0.2 §1.1 transplant convention) |
| **CONFIG_LAYER** | Patches that modify configuration data files (`*.yml`, `*.yaml`, `*.json` in the repo) consumed at module import time | (OPEN at v0.1; whether GRACE has `globals.yml`-equivalent is empirically resolved at S2.20 Block A Cell 8 initial diagnostic) | Applied via in-place rewrite of the config file body; pristine preserved at `<file>.upstream_pristine`; consumed at first-import |

**Sibling-parity note (carry-forward from rome v0.2 §1.0).** MEMIT v2.5 has no documented CONFIG_LAYER patches; the MEMIT-side `globals.yml` was customized at the pre-S2.6 fork-work session but never codified in `memit-patches-canonical.md`. ROME v0.2 §1.6 introduced the CONFIG_LAYER class. GRACE v0.1 inherits the taxonomy declaratively; whether GRACE has a CONFIG_LAYER instance is OPEN until first-execution.

### §1.1 SOURCE_LAYER patches inherited from MEMIT/ROME — APPLICABLE DIRECTLY

These patches are **engine-agnostic** — they target files or behaviors that are model-side or tokenizer-side rather than write-engine-side. They are expected to apply directly to GRACE without modification. Inventory is reduced relative to ROME v0.2 §1.1 (which had five transplanted patches: P-1, P-2, P-4, P-5, P-6) because most of those were rank-1-in-weight mechanism-specific.

| ID | Target (file or behavior) | MEMIT canonical reference | v0.1 verdict | Rationale |
|---|---|---|---|---|
| **Pad-Token** | tokenizer-side alias (`tokenizer.pad_token = tokenizer.eos_token`) | `memit-patches-canonical.md` v2.5 §3.1 | **APPLICABLE DIRECTLY** | Engine-agnostic; tokenizer state required for any encoding operation against Llama-3.1-8B regardless of write engine. EMPIRICALLY-VALIDATED across MEMIT (S2.13-C through S2.15-D2) and ROME (S2.18). Carries forward to GRACE without re-derivation. |

**Note on inventory minimality.** §1.1 contains exactly one entry at v0.1 declarative: `Pad-Token`. Compare ROME v0.2 §1.1 (five entries: P-1, P-2, P-4, P-5, P-6 — all transplanted from MEMIT). This is the structural inversion noted in §0: under GRACE adapter mechanism, the MEMIT-inherited rank-1-in-weight patches relocate to §1.3 INAPPLICABLE; only the engine-agnostic patches remain in §1.1.

### §1.2 SOURCE_LAYER patches inherited from MEMIT/ROME — APPLICABLE WITH MODIFICATION (OPEN at v0.1)

These patches MAY apply to GRACE in modified form depending on actual GRACE codebase structure. Verdicts at v0.1 are declarative-OPEN; first-execution at S2.20 Block A Cell 2 will resolve.

| ID | Target file (MEMIT canonical) | v0.1 verdict | Resolution path |
|---|---|---|---|
| **P-1** | `util/nethook.py` retain pattern for activation traces | **OPEN at v0.1** | If GRACE adapter forward pass instruments base-model activations via `util.nethook.get_module(...)` traces (analogous to ROME `compute_u` activation capture), `P-1` retain pattern may be required. If GRACE uses standard PyTorch forward hooks or routes through its own adapter forward-pass without nethook tracing, `P-1` is INAPPLICABLE. Resolved at S2.20 Block A Cell 2 via grep-anchor inspection of `grace/*.py` for `nethook.get_module` usage. |
| **P-2** | `util/nethook.py` retain pattern keyword arguments | **OPEN at v0.1** | Co-applicable with `P-1`; if `P-1` is INAPPLICABLE then `P-2` is INAPPLICABLE; if `P-1` is APPLICABLE, `P-2` is APPLICABLE-DIRECTLY (the two patches are jointly required per MEMIT v2.5 §2.2 / ROME v0.2 §1.1). |

**OQ-S219-1 (NEW at v0.1; tracked here per kickoff §8 anticipated OQ).** The `P-1` / `P-2` retain-trace applicability question is OPEN at v0.1 declarative authoring. Closure path: empirical resolution at S2.20 Block A Cell 2 grep-anchor inspection of `grace/*.py`. v0.2 absorption codifies the verdict.

### §1.3 SOURCE_LAYER patches inherited from MEMIT/ROME — INAPPLICABLE (mechanism-orthogonal)

These patches target rank-1-in-weight mechanism specifics (covariance projection, outer-product update, precision coercion at compute_u/compute_v sites, in-place weight restore at unmount). GRACE adapter mechanism does not implement any of these; therefore all are INAPPLICABLE.

| ID | Target file / mechanism | Rationale for INAPPLICABLE under GRACE |
|---|---|---|
| **P-3'** | `rome/rome_main.py` device-map handling | INAPPLICABLE — `P-3'` is a fp16-fp32 device-placement workaround for the rank-1 outer-product matmul on RTX 4090; GRACE adapter forward pass does not perform an outer-product matmul against base-model weights. |
| **Device-Map** | model load-time device placement coercion (companion to `P-3'`) | INAPPLICABLE — GRACE adapter parameters are stored alongside the routing layer; standard `device_map="auto"` or explicit `.to(device)` placement on the base model + adapter pool is sufficient. |
| **P-4** | `compute_v.py` covariance-projection fallback nesting | INAPPLICABLE — GRACE does not invoke `compute_v` (no rank-1 update step). |
| **P-5** | `layer_stats.py` covariance computation dispatch | INAPPLICABLE — GRACE does not consume `layer_stats` covariance caches per `framework_finding_memit_ceiling_archival.md` v1.1 §4.3'.4. |
| **P-6** | `layer_stats.py` cache filename `_t100_` segment | INAPPLICABLE — co-INAPPLICABLE with `P-5`; no cache filename round-trip required for GRACE adapter mechanism. |
| **P-7** | `memit/memit_main.py:get_cov` `batch_tokens` propagation | INAPPLICABLE — GRACE does not invoke MEMIT's `get_cov` resolution chain. |
| **P-7-ROME** | `rome/compute_u.py:get_inv_cov` `batch_tokens` propagation | INAPPLICABLE — GRACE does not invoke ROME's `get_inv_cov` resolution chain (no inverse-covariance projection in adapter mechanism). |
| **P-8-ROME** | `rome/compute_u.py` `compute_u` matmul precision coercion | INAPPLICABLE — GRACE does not invoke ROME's `compute_u`; no fp32 inv_cov × fp16 cur_repr matmul site exists in adapter forward pass. |
| **P-9-ROME** | `rome/rome_main.py` outer-product Adam buffer precision coercion | INAPPLICABLE — GRACE does not perform rank-1 outer-product Adam buffer; no `fp16 left_vector @ fp32 right_vector` matmul site exists in adapter forward pass. |
| **Copy-Unmount** | in-place weight tensor restore via `weights_copy[name][...] = weights_copy_originals[name]` | INAPPLICABLE — GRACE adapter mechanism does NOT modify base weights in-place; no in-place restore is required. GRACE unmount semantics are mechanism-distinct: detach adapter from routing layer; restore base-model forward-pass behavior (per D-S219-Q4-1; codified at `C-GRACE-5` in §5). |

**INAPPLICABLE partition rationale (load-bearing for T.2 GRACE entry).** This partition documents the structural mechanism-orthogonality argument for why T.2 GRACE is the next test surface post-T.2-ROME-elimination per `t_branch_decision_document.md` v1.1 §4'.2: ten of the eleven MEMIT-or-ROME-derived patches do not apply to GRACE. The architectural-invariant ceiling claim covering `(Llama-3.1-8B × {MEMIT, ROME} × canonical hparams)` does not transitively cover GRACE because the underlying mechanism class is not implemented by GRACE. PASS at S2.20 → ceiling is rank-1-class-specific; FAIL at S2.20 → ceiling is `(model × hparams)` independent of write-engine class (per `t_branch_decision_document.md` v1.1 §5' conditional execution plan).

### §1.4 SOURCE_LAYER patches authored fresh for GRACE — DEFERRED at v0.1

S2.20 Block A Cell 2 first-execution against `meta-llama/Llama-3.1-8B` may surface latent defects in upstream `https://github.com/Thartvigsen/GRACE` at the pinned SHA that block GRACE adapter dispatch under the project's NV-resident environment. Such defects are absorbed at the v0.2 codification analog session post-S2.20 (parallel to ROME v0.1 → v0.2 P-7-ROME / P-8-ROME / P-9-ROME absorption pattern).

**v0.1 disposition: NO NEW patches authored at v0.1.** The S2.18 ROME pattern surfaced three NEW SOURCE_LAYER patches (P-7-ROME, P-8-ROME, P-9-ROME) at first-execution mid-session. v0.1 declarative does not pre-author analogous GRACE-side patches because:

1. The candidate defect surfaces from ROME (cache filename round-trip; precision coercion at `compute_u` and outer-product matmul sites) are rank-1-in-weight specific and INAPPLICABLE to GRACE adapter mechanism.
2. The candidate defect surfaces specific to adapter-based mechanism (e.g., codebook persistence across model reload; routing-layer state initialization; gradient flow through adapter pool when base-model weights are frozen; fp16 vs. fp32 mismatch at adapter-vs-base-model interface) are unknown at v0.1 — they must be surfaced empirically at S2.20.

**Anticipated NEW patch surfaces (declarative; for S2.20 operator situational awareness, NOT a declarative patch list).** Plausible NEW patch surfaces at S2.20 Block A include:

- **(a) Adapter parameter dtype coercion.** Llama-3.1-8B base model is fp16; GRACE paper Table 1 likely assumes fp32 adapter parameters. The adapter-vs-base-model interface (residual addition site) requires dtype compatibility. Plausible analog of `P-8-ROME` structural class (precision coercion at matmul / addition site).
- **(b) Llama-3.1-8B architecture-specific instrumentation.** RoPE handling, GQA attention head count, RMSNorm placement at adapter insertion point may surface adaptation requirements. Plausible analog of `P-7` structural class (architecture-specific instrumentation patch).
- **(c) Batch-dimension or sequence-length handling at codebook routing.** Routing-function evaluation against batch-major activations may require shape-handling adaptation.
- **(d) Gradient flow through frozen base model.** Adapter optimization requires gradient backflow through the adapter parameters only; base-model `requires_grad=False` may need explicit handling.

None of these is empirically anchored at v0.1; the list is informative for S2.20 Block A operator situational awareness.

### §1.5 Verification-only carry-forward (no patch application; verification gate only)

| Item | Verification gate | Cell | v0.1 status |
|---|---|---|---|
| **Llama-3.1-8B target model bit-exact identity** | `assert model.config._name_or_path == 'meta-llama/Llama-3.1-8B' and model_revision_sha == 'd04e592bb4f6aa9cfee91e2e20afa771667e1d4b'` | t2_grace_runbook v0.1 Cell 5 | INHERITED — same target model SHA across MEMIT (S2.13-C through S2.15-D2) and ROME (S2.18); 6 cross-session bit-exact determinism checkpoints |
| **Pad-Token alias verification** | `assert tokenizer.pad_token == tokenizer.eos_token` | t2_grace_runbook v0.1 Cell 5 | INHERITED — EMPIRICALLY-VALIDATED at MEMIT + ROME |
| **GRACE codebook initialization at trial entry** | `assert grace_adapter_pool.codebook_size == 0` (no cross-trial state) | t2_grace_runbook v0.1 Cell 8 (R1.3-equivalent dry-run); Cell 15 (per-trial entry) | DECLARATIVE at v0.1; empirical at S2.20 |
| **GRACE adapter routing-layer absence pre-edit** | `assert no GRACE adapter registered at routing layer` (pre-edit forward-pass = base model forward pass) | t2_grace_runbook v0.1 Cell 7 (pre-edit baseline); Cell 15 trial entry | DECLARATIVE at v0.1; empirical at S2.20 |

### §1.6 CONFIG_LAYER patches — DEFERRED at v0.1

Whether GRACE has a `globals.yml`-equivalent or other CONFIG_LAYER instance is OPEN at v0.1 declarative. Resolved at S2.20 Block A Cell 8 initial diagnostic phase.

**OQ-S219-2 (NEW at v0.1; tracked here per kickoff §8 anticipated OQ).** GRACE may have a CONFIG_LAYER analog (`globals.yml`-equivalent or similar config-loading idiom). Closure path: empirical resolution at S2.20 Block A Cell 8 initial diagnostic; if surfaced, codified at v0.2 absorption analogous to ROME v0.2 §9.

---

## §2 Reserved for v0.2 absorption (`v0_1_undocumented_findings`)

(Section reserved for `v0_1_undocumented_findings` absorption parallel to ROME v0.2 §2; populated at v0.2 codification analog session post-S2.20 first-execution. NO content at v0.1 declarative. Section number preserved for sibling-parity with rome v0.2 numbering.)

---

## §3 GRACE repository SHA pin

**Per D-S219-Q1-1 (closes OQ-V11-T-BRANCH-1):** GRACE repository pinned at the **latest stable tip** of `https://github.com/Thartvigsen/GRACE` at S2.20 Block A Cell 1 entry. Specific SHA hash recorded at S2.20 Block A Cell 1 (parallel to ROME's `0874014cd9837e4365f3e6f3c71400ef11509e04` recorded at S2.18 Block A Cell 1).

**Rationale for "latest stable tip" disposition (parallel to D-S217-Q2-1 ROME selection):**

- GRACE repository is research-code class (Hartvigsen et al. NeurIPS 2023 supplementary); no formal release tags expected.
- "Latest stable tip" is the most-current state with merged fixes; alternatives (paper supplementary release tag, or a specific historical SHA) introduce reproducibility coupling to a frozen state that may have known-but-unfixed defects.
- Bit-exact reproducibility is anchored at the SHA hash recorded at S2.20 Cell 1 — once recorded, that SHA is the canonical reference for any future GRACE re-execution (parallel to ROME's recorded SHA pattern).

**v0.2 absorption note.** The specific SHA hash will be recorded in this section at v0.2 codification analog session post-S2.20 (parallel to ROME v0.2 §3 specific SHA recording).

---

## §4 GRACE canonical hparams

### §4.1 GRACE paper Table 1 reference values

Per D-S219-Q2-1 (closes OQ-V11-T-BRANCH-2): GRACE hparam surface starts from GRACE paper Table 1 reference values + targeted Llama-3.1-8B adaptation. The GRACE paper (Hartvigsen et al., "Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors," NeurIPS 2023) reports reference hparams against GPT-2-XL and T5 architectures; Llama-3.1-8B adaptation is required because Llama architecture differs from both reference architectures (32 layers vs. GPT-2-XL 48 / T5 24; hidden dim 4096; GQA attention head count differences; RMSNorm vs. LayerNorm).

| Hparam | Paper-canonical reference (declarative) | v0.1 Llama-3.1-8B initial value | Rationale |
|---|---|---|---|
| `epsilon` (routing distance threshold) | per paper Table 1; deferred re-derivation against Llama activation magnitudes | **paper-canonical** at v0.1 declarative | Calibration corridor at S2.20 Block B Cell 9 will surface whether Llama-3.1-8B activation magnitudes require adjustment |
| `learning_rate` (adapter optimization LR) | per paper Table 1 | **paper-canonical** at v0.1 declarative | Re-evaluate at S2.20 Block B if adapter loss does not converge |
| `n_iter` (adapter optimization iterations per edit) | per paper Table 1 | **paper-canonical** at v0.1 declarative | Parallel to MEMIT/ROME `v_num_grad_steps` envelope |
| `replacement` (codebook collision-handling policy) | LRU-style per paper Table 1 | **paper-canonical** at v0.1 declarative | Affects single-fact-per-trial behavior; no cross-trial codebook state per `C-GRACE-1` makes this hparam moot for v0.1 trial-loop semantics |
| `init` (adapter initialization scheme) | "cold" per paper Table 1 (fresh codebook at edit time) | **"cold"** at v0.1 declarative | Ensures no warm-start state across trials per `C-GRACE-2` |
| `eps_expand` (codebook key-set expansion scheme) | per paper Table 1 (mechanism-specific) | **paper-canonical** at v0.1 declarative | OPEN — re-derived at S2.20 Block B if codebook expansion behavior differs from paper expectation |

**Hparam-surface caveat at v0.1.** GRACE has additional mechanism-specific hparams (codebook capacity, distance metric type, key-encoding dimension) that are GRACE-paper-Table-1 declared. Specific values are recorded against the actual repo at S2.20 Block A Cell 4 first-execution. v0.2 absorption codifies the empirical values in this section. The "paper-canonical" disposition at v0.1 is a declarative placeholder for "consume the values present in the GRACE paper Table 1 (or the equivalent default values shipped with the repository's `hparams/` directory if present)" — the specific numeric values are deferred to first-execution rather than guessed at v0.1.

### §4.2 GRACE adapter placement at Llama-3.1-8B (per D-S219-Q3-1)

Per D-S219-Q3-1 (closes OQ-V11-T-BRANCH-3): two-candidate test surface at S2.20 Block B (parallel to D-S217-Q4-1 ROME L17 + L2 pattern).

| Candidate | Layer | Rationale | Block B test ordering |
|---|---|---|---|
| **Layer-A (primary)** | **L17** (transformer-mid analog to ROME L17 paper precedent) | Adapter placement at transformer-mid mirrors GRACE paper canonical placement on GPT-2-XL (mid-network) and ROME paper L17 precedent for Llama-3.1-8B; MLP down-projection at this band aligns with the strongest factual recall signal in the residual stream (per S2.14-D D.1 mediation map: residual IE peak at L31 monotonic accumulation L15→L31; mid-network band L15-L17 catches early factual encoding) | Tested first at Cell 9 |
| **Layer-B (secondary)** | **L2** (S2.14-D D.1 MLP-output mediation peak; parallel to MEMIT canonical layer set per D-S215D2-1 and ROME L2 secondary per D-S217-Q4-1) | Adapter placement at MLP-output mediation peak band tests whether the mediation peak placement carries across mechanism class (rank-1 weight update → adapter); if Layer-A FAILS at calibration corridor, Layer-B tests the mediation-peak-placement hypothesis | Tested second at Cell 11 |

**Specific layer index at v0.1 declarative.** Layer-A primary = single layer L17 (parallel to ROME L17 single-layer placement; concrete declarative pin against the L17 cache extension recorded in NV per S2.18). Layer-B secondary = single layer L2 (parallel to ROME L2 secondary per S2.18 Cell 11).

**GRACE-paper-canonical placement (option (a) considered and not selected at Q3).** GRACE paper canonical placement for GPT-2-XL was at a specific transformer block FFN. For Llama-3.1-8B, the architectural translation requires adapting the attention-FFN block index plus the FFN sub-component (`down_proj` vs. `gate_proj` vs. `up_proj`). The Q3 selection ((b) primary L17 + (c) secondary L2) defers GRACE-paper-canonical placement until S2.20 Block B verdict surface; if both Layer-A and Layer-B FAIL the calibration corridor, Layer-C = GRACE-paper-canonical-placement-translated MAY be tested as a Block B retry candidate (recorded as a forward-conditional consideration; no formal OQ at v0.1).

### §4.3 Llama-3.1-8B-specific hparam considerations (v0.1 carry-forward)

| Consideration | v0.1 disposition | Resolution path |
|---|---|---|
| RMSNorm vs. LayerNorm at adapter insertion | GRACE paper assumed LayerNorm; Llama-3.1-8B uses RMSNorm. Adapter parameter dtype + scale must be compatible with RMSNorm output magnitude | Empirical at S2.20 Block A Cell 5 (model load) + Cell 8 (R1.3 dry-run gate) |
| GQA attention head count | Llama-3.1-8B uses GQA (8 KV heads, 32 query heads); not directly relevant to MLP-layer adapter placement but relevant if any attention-side adaptation considered (out of v0.1 scope) | Out of v0.1 scope; informational |
| Long-context `max_position_embeddings` | Llama-3.1-8B `max_position_embeddings=131072`; this was the structural site for `P-7-ROME` under ROME mechanism (cache filename `_t100_`-vs-`_t8192_` mismatch). GRACE adapter mechanism does not invoke `layer_stats` covariance caches, so no analogous site is anticipated. | INAPPLICABLE — anticipated null result |
| Adapter parameter dtype | GRACE paper Table 1 likely fp32 for adapter parameters; Llama-3.1-8B base model is fp16. Adapter-vs-base interface dtype requires verification | Empirical at S2.20 Block A Cell 8 (R1.3 dry-run gate); plausible NEW patch surface (analog of `P-8-ROME` structural class) per §1.4 anticipated NEW patch (a) |
| Multi-token target tolerance | Per D-S219-Q5-1: carry-forward first-token-proxy methodology from D-S215D2-CFB-V3-004-PROXY-1 + D-V12-MULTITOKEN-1 with `RE-EVALUATE AT TRIAL 0` flag (parallel to D-S217-Q5-1 ROME disposition) | Empirical at S2.20 Block B Cell 9 trial 0; first-token-proxy RETIRED for Cell 9 if GRACE's adapter dispatch natively handles full multi-token target_new sequence at trial 0 |

---

## §5 Process constraints

### §5.1 `C-GRACE-1` — Single-fact dispatch envelope

**Statement.** GRACE edit dispatch at S2.20 operates in single-fact-per-trial mode; the codebook is initialized fresh at trial entry and discarded at trial exit (no cross-trial codebook state). One fact per trial; one trial per per-fact entry in the trial matrix.

**Rationale.** Parallel to `C-ROME-1`. IC-S24-4 trial protocol semantics (5 facts × 3 replicates = 15 trials) require per-trial isolation for unmount band verification. GRACE's natural mode is multi-fact accumulation via codebook entries; for v0.1 this is reduced to single-fact-per-trial to preserve IC-S24-4 protocol compatibility. v0.2 absorption may surface that multi-fact accumulation is structurally awkward to disable in GRACE's dispatch path; if so, an alternative envelope (e.g., codebook-pop-per-fact) is codified at v0.2 (see OQ-S219-3).

**Verification site.** `t2_grace_runbook.md` v0.1 Cell 9 (single-edit dispatch) and Cell 15 (trial loop body — per-trial codebook reset gate).

**Status.** DECLARATIVE at v0.1; EMPIRICALLY-VALIDATED PENDING at S2.20 Block B Cell 9 first execution.

### §5.2 `C-GRACE-2` — Adapter pool initialization at trial entry

**Statement.** GRACE adapter pool is initialized fresh at each trial entry; no cross-trial adapter state is preserved. Specifically: codebook is empty; routing-layer adapter list contains zero adapters; routing-function parameters (if any) are at their post-Pad-Token / pre-edit canonical state.

**Rationale.** Parallel to `C-ROME-2` (covariance cache reuse) but mechanism-distinct: `C-ROME-2` enforced REUSE of pre-computed covariance caches across trials (cache HIT discipline); `C-GRACE-2` enforces ABSENCE of any cross-trial state. The structural difference reflects that ROME's trial-loop performance benefits from cache reuse (~hours saved on cache compute), while GRACE's trial-loop integrity requires per-trial isolation (no codebook bleed).

**Verification site.** `t2_grace_runbook.md` v0.1 Cell 15 trial loop body — per-trial entry assertion: `assert grace_adapter_pool.codebook_size == 0 and grace_adapter_pool.routing_layer_adapters == []` (or actual API-equivalent at v0.2 absorption).

**Status.** DECLARATIVE at v0.1; EMPIRICALLY-VALIDATED PENDING at S2.20 Block B Cell 9 + Cell 15.

### §5.3 `C-GRACE-3` — Dry-run gate (R1.3-equivalent)

**Statement.** Before any GRACE edit dispatch (Block B Cell 9 onward), a dry-run gate executes that smoke-loads the GRACE module against the patched repo state, instantiates an empty adapter pool, and verifies no import-time or instantiation-time errors. The dry-run uses an empty codebook; no edit is dispatched; no base-model weights are touched.

**Rationale.** Parallel to `C-ROME-3` (R1.3-equivalent dry-run gate) and MEMIT `C-S26-3`. The gate is the canonical pre-execution sanity check that all CONFIG_LAYER patches (if any) and SOURCE_LAYER patches (if any new ones authored) are in place and the GRACE module imports cleanly. Mechanism-specific specialization: GRACE dry-run uses empty-codebook adapter pool initialization + base-model forward-pass smoke-pass, NOT covariance cache resolution (which is INAPPLICABLE per §1.3).

**Verification site.** `t2_grace_runbook.md` v0.1 Cell 8 (R1.3-equivalent dry-run gate cell).

**Status.** DECLARATIVE at v0.1; EMPIRICALLY-VALIDATED PENDING at S2.20 Block A Cell 8.

### §5.4 `C-GRACE-4` — Marker post-application verification

**Statement.** After each SOURCE_LAYER or CONFIG_LAYER patch application, a uniquely identifying marker token (or assertion equivalent) MUST be present in the patched source / config; the verification step is performed before any subsequent patch application or downstream cell entry.

**Rationale.** Parallel to `C-ROME-4` / `C-S28-1` — defense-in-depth marker verification ensures patch idempotency and detects partial-application failures. For GRACE v0.1 declarative, no SOURCE_LAYER NEW patches are pre-authored, so the marker verification surface is reduced to (a) Pad-Token alias verification (tokenizer-side; canonical assertion `tokenizer.pad_token == tokenizer.eos_token`) and (b) any v0.2-absorbed NEW patches' markers (deferred). At v0.2 codification analog session, this constraint expands to cover the NEW patch markers.

**Verification site.** `t2_grace_runbook.md` v0.1 Cell 2 (patch state verification block); Cell 5 (Pad-Token alias verification).

**Status.** DECLARATIVE at v0.1; EMPIRICALLY-VALIDATED PENDING at S2.20 Block A Cells 2 + 5.

### §5.5 `C-GRACE-5` — Adapter-detach unmount mechanism

**Statement.** GRACE unmount at trial exit is performed via **adapter-detach**: the adapter is removed from the routing layer's adapter list; the base-model forward-pass behavior is restored; the adapter's parameters are released (Python garbage collection eligible). Specifically: the routing layer's `adapter_list.pop(adapter_index)` (or equivalent API per actual GRACE codebase) is invoked; post-detach, the routing layer evaluates with zero adapters and the base-model forward pass proceeds unmodified.

**Rationale.** Per D-S219-Q4-1 (closes OQ-V11-T-BRANCH-5). Adapter-detach is the cleanest unmount mechanism that preserves bit-exact base-model forward-pass behavior post-unmount. Adapter-snapshot-restore (option (c) at Q4) is considered fallback if adapter-detach produces inter-trial drift > 0 on shared-spec probes — re-evaluated at S2.20 Block B Cell 9 trial entry.

**Empirical anchor expectation.** Bit-exact forward-pass post-unmount is the load-bearing precondition for verdict integrity (parallel to IC-S23-4 `unmount drift = 0.00e+00` envelope). For GRACE, the expectation is: post-detach `model.forward(x)` produces token logits identical to pre-edit `model.forward(x)` for any shared-specificity probe, drift `0.00e+00` (fp16 base model). If drift > `1e-4` is observed at S2.20 Block B Cell 9, adapter-detach is empirically falsified; fallback to adapter-snapshot-restore (option (c)) is exercised at v0.2 absorption.

**Verification site.** `t2_grace_runbook.md` v0.1 Cell 15 trial loop body — per-trial unmount + post-unmount specificity probe drift assertion.

**Status.** DECLARATIVE at v0.1; EMPIRICALLY-VALIDATED PENDING at S2.20 Block B Cell 9.

---

## §6 Reserved for v0.2 absorption (NEW SOURCE_LAYER patch — slot 1)

(Section reserved for any NEW SOURCE_LAYER patch surfaced at S2.20 Block A first-execution; absorbed at v0.2 codification analog session post-S2.20. Parallel structure to ROME v0.2 §6 (`P-7-ROME`). NO content at v0.1 declarative. Section number preserved for sibling-parity with rome v0.2 numbering.)

---

## §7 Reserved for v0.2 absorption (NEW SOURCE_LAYER patch — slot 2)

(Section reserved; parallel to ROME v0.2 §7 (`P-8-ROME`). NO content at v0.1 declarative.)

---

## §8 Reserved for v0.2 absorption (NEW SOURCE_LAYER patch — slot 3)

(Section reserved; parallel to ROME v0.2 §8 (`P-9-ROME`). NO content at v0.1 declarative.)

---

## §9 Reserved for v0.2 absorption (CONFIG_LAYER patches)

(Section reserved for any CONFIG_LAYER patches surfaced at S2.20 Block A first-execution; absorbed at v0.2 codification analog session post-S2.20. Parallel structure to ROME v0.2 §9 (`globals.yml`). NO content at v0.1 declarative; see §1.6 OQ-S219-2 for closure path.)

---

## §10 Application order

### §10.1 v0.1 declarative application order

At v0.1 declarative the application order is reduced relative to ROME v0.2 because no NEW patches are pre-authored. The order at v0.1 is:

1. **CONFIG_LAYER patches first (if any).** None at v0.1 declarative; OPEN per §1.6. If S2.20 surfaces a CONFIG_LAYER analog (`globals.yml`-equivalent), it is applied at session-entry environment setup before any SOURCE_LAYER patch (parallel to ROME v0.2 §10.1 CONFIG_LAYER-first ordering rationale).
2. **`Pad-Token` (tokenizer-side; engine-agnostic).** Applied at model + tokenizer load time (`t2_grace_runbook.md` v0.1 Cell 5). Engine-agnostic; tokenizer state independent of GRACE source code.
3. **`P-1` / `P-2` (conditional; OPEN at v0.1).** Applied at Cell 2 patch state verification phase IF surfaced as APPLICABLE-WITH-MODIFICATION at first-execution per OQ-S219-1 resolution. INAPPLICABLE skip if GRACE adapter forward pass does not use nethook retain pattern.
4. **NEW SOURCE_LAYER patches (DEFERRED at v0.1).** None at v0.1; absorbed at v0.2 if surfaced.

### §10.2 Application order rationale

CONFIG_LAYER first ensures any config-loading idiom is satisfied before SOURCE_LAYER files import. `Pad-Token` is tokenizer-side and independent of source code; applied at model load time alongside tokenizer instantiation. `P-1` / `P-2` (conditional) are SOURCE_LAYER and applied per ROME v0.2 §10.1 pattern (in-place text substitution against post-clone source).

The rationale generalizes the ROME v0.2 application order discipline: config files must be in place before any source file referencing them is loaded; tokenizer-side patches are applied at the tokenizer instantiation site (independent of source patches); SOURCE_LAYER patches are applied in dependency order (here, `P-1` and `P-2` are jointly applied; no further inter-patch dependency at v0.1).

---

## §11 Manifest schema for `t2_grace_patch_state.json`

The patch state manifest is the canonical record of which patches have been applied to the GRACE source at a given session entry. Schema parallels ROME v0.2 §11 with reduced inventory and v0.1-declarative-status fields.

```json
{
  "manifest_schema_version": "v0.1",
  "session": "S2.X.X",
  "timestamp": "ISO-8601",
  "engine": "GRACE",
  "engine_version_sha": "<resolved at S2.20 Cell 1>",
  "target_model": "meta-llama/Llama-3.1-8B",
  "target_model_revision_sha": "d04e592bb4f6aa9cfee91e2e20afa771667e1d4b",
  "patches_applied": {
    "Pad-Token": {
      "class": "tokenizer-side",
      "status": "APPLIED",
      "verification_site": "Cell 5",
      "verification_assertion": "tokenizer.pad_token == tokenizer.eos_token"
    },
    "P-1": {
      "class": "SOURCE_LAYER",
      "target_file": "util/nethook.py",
      "status": "APPLIED|INAPPLICABLE|OPEN",
      "verification_site": "Cell 2",
      "verification_assertion": "<marker per OQ-S219-1 closure>",
      "v0_1_disposition": "OPEN"
    },
    "P-2": {
      "class": "SOURCE_LAYER",
      "target_file": "util/nethook.py",
      "status": "APPLIED|INAPPLICABLE|OPEN",
      "verification_site": "Cell 2",
      "verification_assertion": "<marker per OQ-S219-1 closure>",
      "v0_1_disposition": "OPEN"
    }
  },
  "patches_inapplicable": [
    "P-3'", "Device-Map", "P-4", "P-5", "P-6", "P-7",
    "P-7-ROME", "P-8-ROME", "P-9-ROME", "Copy-Unmount"
  ],
  "patches_deferred_to_v0_2": [
    "<NEW SOURCE_LAYER patches if surfaced at S2.20 Block A>",
    "<CONFIG_LAYER patches if surfaced at S2.20 Block A>"
  ],
  "constraints_active": [
    "C-GRACE-1", "C-GRACE-2", "C-GRACE-3", "C-GRACE-4", "C-GRACE-5"
  ],
  "decisions_active": [
    "D-S219-Q1-1", "D-S219-Q2-1", "D-S219-Q3-1", "D-S219-Q4-1", "D-S219-Q5-1"
  ]
}
```

### §11.1 Schema delta from rome v0.2

- `engine` field: `"GRACE"` (vs. ROME v0.2 `"ROME"`)
- `patches_inapplicable` list expanded to cover all rank-1-in-weight mechanism patches (10 entries; vs. ROME v0.2 which had a much shorter list since most MEMIT patches were APPLICABLE under ROME)
- `patches_deferred_to_v0_2` list NEW at v0.1 (no analog in rome v0.2 since rome v0.2 was post-absorption); v0.1 declarative status acknowledges deferred patches at the manifest layer
- `decisions_active` list NEW at v0.1; codifies the operator-resolved D-S219-Q1-1..Q5-1 ratifications at the manifest layer

---

## §12 Upstream notes — MEMIT canonical vs. ROME canonical vs. GRACE canonical relationship (v0.1)

### §12.1 Three-engine canonical coexistence

Post-S2.19 close: three write-engine canonicals coexist as parallel siblings:

- **`memit-patches-canonical.md` v2.5** — MEMIT canonical; preserved unmodified per D-S216-CLOSE-3; no further work scheduled.
- **`rome-patches-canonical.md` v0.2** — ROME canonical; preserved post-elimination as historical record + carry-forward per `t_branch_decision_document.md` v1.1 §4'.1.
- **`grace-patches-canonical.md` v0.1 (this artifact)** — GRACE canonical; active forward-target for S2.20 first-execution.

### §12.2 Mechanism-class taxonomy (v0.1 cross-canonical map)

| Mechanism class | Engine | Canonical | Status |
|---|---|---|---|
| **Rank-1 in-weight (multi-fact)** | MEMIT | `memit-patches-canonical.md` v2.5 | ELIMINATED at canonical hparams (S2.13-C through S2.15-D2 cumulative) |
| **Rank-1 in-weight (single-fact)** | ROME | `rome-patches-canonical.md` v0.2 | ELIMINATED at canonical hparams (S2.18) |
| **Adapter-based (codebook routing)** | GRACE | `grace-patches-canonical.md` v0.1 (this artifact) | ACTIVE forward-target |
| **Hypernetwork-based** | MEND | (DEFERRED; no canonical authored) | DEFERRED per `t_branch_decision_document.md` v1.1 §4'.1 |
| **Retrieval-augmented** | SERAC | (DEFERRED; no canonical authored) | DEFERRED per `t_branch_decision_document.md` v1.1 §4'.1 |

The architectural-invariant ceiling claim per `framework_finding_memit_ceiling_archival.md` v1.1 §1' covers the rank-1-in-weight class (both single-fact and multi-fact dispatch). GRACE entry tests whether the ceiling generalizes to adapter-based class. PASS = ceiling is rank-1-class-specific; FAIL = ceiling is `(model × hparams)` independent of write-engine class (per `t_branch_decision_document.md` v1.1 §5' conditional execution plan).

### §12.3 Sibling-parity discipline

All three canonicals follow parallel structural shape:

- §0 Purpose & non-amendment declaration
- §1 Patch inventory (with two-class taxonomy SOURCE_LAYER + CONFIG_LAYER per D-V02-6)
- §3 SHA pin (engine repository SHA)
- §4 Canonical hparams
- §5 Process constraints
- §6+ NEW patch detail (or reserved at v0.1 declarative)
- §10 Application order
- §11 Manifest schema
- §12 Upstream notes (this section)
- §13 Non-goals
- §14 References
- §15 Authoring metadata

Section numbering is preserved across all three canonicals to enable cross-canonical reference. Section content adapts to engine specifics; section structure is invariant.

### §12.4 Cross-canonical maintenance discipline

Future work that touches multiple canonicals (e.g., a hypothetical MEMIT v2.6 absorption of CONFIG_LAYER class retroactive to MEMIT-side `globals.yml` customization at pre-S2.6 fork-work session) MUST preserve the parallel-sibling discipline. No canonical is amended retroactively at the prompting of another canonical's authoring; cross-canonical observations are recorded at the authoring canonical's §12 upstream notes section without back-amendment.

### §12.5 Framework-spec relevance scoring (orchestration-comparativist + graph-data-architect light-touch)

Adapter-based mechanisms are structurally closer to the framework's `.vindex` overlay model than rank-1-in-weight mechanisms. Specifically:

- The `.vindex` overlay model assumes a write engine that produces a versioned overlay artifact representing the parametric memory state at a given commit. In-weight modification (MEMIT/ROME) requires the overlay to capture base-weight deltas; adapter-based (GRACE) modification produces overlay content that is naturally already separated from base weights (the adapter parameters ARE the overlay content).
- The State Ledger (mapping Git commit hashes to `.vindex` snapshot hashes) has a cleaner semantic under adapter-based mechanism: a `.vindex` snapshot hash IS the adapter pool's content hash; under in-weight mechanism, the snapshot hash must encode a delta against base weights.
- The Pruning Agent (semantic garbage collection) has a clearer surface under adapter-based mechanism: pruning = removing codebook entries from the adapter pool; under in-weight mechanism, pruning requires re-reverting the underlying weight delta.

This relevance scoring is informative for Workstream 2 (orchestration path selection) and Workstream 3 (implementation planning) regardless of S2.20 verdict; it does NOT pre-judge T.2 GRACE verdict but does record that ADAPTER-based engines have framework-spec affinity beyond the immediate ceiling-elimination question.

---

## §13 Non-goals

This canonical does NOT:

1. **Pre-author NEW SOURCE_LAYER patches at v0.1.** The S2.18 ROME pattern surfaced three NEW SOURCE_LAYER patches mid-execution. v0.1 declarative does not pre-author analogous GRACE-side patches; absorption is deferred to v0.2 codification analog session post-S2.20 (see §1.4).
2. **Pre-judge T.2 GRACE verdict.** The verdict surface at S2.20 Cell 13 verdict gate is empirical; v0.1 commits to the GRACE-as-leading-T-branch-hypothesis posture, not to GRACE PASS or FAIL.
3. **Modify `memit-patches-canonical.md` v2.5 OR `rome-patches-canonical.md` v0.2.** Sibling-parity discipline preserved per `t_branch_decision_document.md` v1.1 §4'.3 entry precondition #2.
4. **Author the T.2 GRACE runbook.** That is the scope of S2.19 Block 2 = `t2_grace_runbook.md` v0.1 (parallel sibling).
5. **Commit to specific GRACE adapter-rank, routing-threshold, memory-pool-size, learning-rate values beyond paper-canonical reference.** Targeted Llama-3.1-8B adaptation deferred to S2.20 Block B Cell 13 verdict gate; full calibration sweep out of v0.1 scope.
6. **Codify multi-fact accumulation envelope.** v0.1 declares single-fact-per-trial dispatch (`C-GRACE-1`) for IC-S24-4 trial protocol parity; multi-fact accumulation is GRACE's natural mode but is OPEN at v0.1 (re-evaluate at v0.2 if single-fact-per-trial is structurally awkward; see OQ-S219-3).
7. **Reverse the T.2 ROME elimination.** S2.18 verdict B-FAIL → T.2 ROME ELIMINATED at canonical hparams is a load-bearing empirical record; this v0.1 canonical does not propose any T.2 ROME re-execution.
8. **Foreclose T.1 / T.3 paths.** T.1 retains as fallback per `t_branch_decision_document.md` v1.1 §5' if T.2 GRACE FAILS. T.3 remains a multi-session post-WS1 redesign option if both T.2 GRACE and T.1 fail.
9. **Pre-judge framework-spec adoption of adapter-based mechanism.** §12.5 records framework-spec relevance scoring; this is informative, not normative. Adoption of any specific write engine is a Workstream 2/3 decision, not a Workstream 1 deliverable.

---

## §14 References

### §14.1 Companion artifact (concurrent S2.19 authoring)

- `t2_grace_runbook.md` v0.1 — GRACE runbook; structural parallel to `t2_rome_runbook.md` v0.2 (Block A pre-flight + Block B HC-2-equivalent dry-run + Block C trial loop; 21 cells; Cell 13 3-route verdict gate; Cell 6 `MULTI_TOKEN_ALLOWLIST` canonical absorption inheritance; Cell 15 adapter-detach unmount per `C-GRACE-5`)

### §14.2 Carry-forward canonical artifacts (preserved unmodified at S2.19)

- `memit-patches-canonical.md` v2.5 — MEMIT canonical; preserved unmodified per D-S216-CLOSE-3
- `rome-patches-canonical.md` v0.2 — ROME canonical; preserved post-elimination per `t_branch_decision_document.md` v1.1 §4'.1
- `stage_1_sect_runbook_v1_7.md` — MEMIT-side runbook (latest; `MULTI_TOKEN_ALLOWLIST` canonical absorption per D-V12-MULTITOKEN-1)
- `t2_rome_runbook.md` v0.2 — ROME-side runbook (preserved post-elimination)

### §14.3 Pre-read inputs (load-bearing)

- `t_branch_decision_document.md` v1.1 — §4'.2 GRACE selection rationale; §4'.3 GRACE entry preconditions; §6' methodology lock for T.2 GRACE
- `framework_finding_memit_ceiling_archival.md` v1.1 — §1' ceiling scope extension; §3' hypothesis-class ledger; §4.3'.4 patches carry-forward applicability for GRACE
- `session_v0_2_codification_summary_block.md` — v0.2 codification session close artifact
- `session_2_18_summary_block.md` + `session_2_18_summary_block_appendix.md` — S2.18 forensic anchor (consulted for pathology classification taxonomy carry-forward)

### §14.4 Decision IDs (S2.19)

- **D-S219-Q1-1** — GRACE SHA pin: latest stable tip of `https://github.com/Thartvigsen/GRACE` (closes OQ-V11-T-BRANCH-1)
- **D-S219-Q2-1** — GRACE canonical hparams: paper Table 1 + Llama-3.1-8B adaptation (closes OQ-V11-T-BRANCH-2)
- **D-S219-Q3-1** — GRACE adapter placement: Layer-A L17 primary + Layer-B L2 secondary (closes OQ-V11-T-BRANCH-3)
- **D-S219-Q4-1** — GRACE unmount mechanism: adapter-detach (closes OQ-V11-T-BRANCH-5)
- **D-S219-Q5-1** — Multi-token tolerance posture: first-token-proxy carry-forward + `RE-EVALUATE AT TRIAL 0` flag (closes OQ-V11-T-BRANCH-4)

### §14.5 Constraint IDs (v0.1)

- **`C-GRACE-1`** — Single-fact dispatch envelope (DECLARATIVE at v0.1)
- **`C-GRACE-2`** — Adapter pool initialization at trial entry (DECLARATIVE at v0.1)
- **`C-GRACE-3`** — Dry-run gate (R1.3-equivalent) (DECLARATIVE at v0.1)
- **`C-GRACE-4`** — Marker post-application verification (DECLARATIVE at v0.1)
- **`C-GRACE-5`** — Adapter-detach unmount mechanism (DECLARATIVE at v0.1)

### §14.6 Open questions

- **OQ-S219-1** — `P-1` / `P-2` retain-trace applicability under GRACE adapter forward pass (resolved at S2.20 Block A Cell 2)
- **OQ-S219-2** — GRACE CONFIG_LAYER analog (`globals.yml`-equivalent or similar) (resolved at S2.20 Block A Cell 8)
- **OQ-S219-3** — GRACE multi-fact dispatch semantics (single-fact-per-trial vs. adapter-accumulation) (resolved at v0.2 absorption per S2.20 Cell 15 empirical record)
- **OQ-S219-4** — GRACE Cell 3 disposition (INAPPLICABLE-DEFERRED-BY-MECHANISM vs. replace with adapter-pool initialization verification) (resolved at S2.19 Block 2 `t2_grace_runbook.md` v0.1 authoring)
- **OQ-V11-T-BRANCH-6** (carried forward from `t_branch_decision_document.md` v1.1 §8'.2) — If T.2 GRACE PASSES, what artifact captures the rank-1-in-weight-vs-adapter comparison framework finding update (resolved post-S2.20 verdict)

### §14.7 Repository references

- GRACE: `https://github.com/Thartvigsen/GRACE` (SHA pin per D-S219-Q1-1; specific SHA recorded at v0.2 absorption post-S2.20 Block A Cell 1)
- ROME (post-elimination historical reference): `https://github.com/kmeng01/rome` SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04`
- MEMIT (preserved): `https://github.com/kmeng01/memit` (SHA per `memit-patches-canonical.md` v2.5)

---

## §15 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | S2.19 = T.2 GRACE runbook v0.1 authoring (operator-side post-v0.2 codification; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5') |
| Authoring date | 2026-05-05 |
| Document version | v0.1 |
| Status | RATIFIED v0.1 — declarative; empirical absorption deferred to v0.2 codification analog session post-S2.20 |
| Supersedes | (none — first version) |
| Basis | `t_branch_decision_document.md` v1.1 §6' methodology lock for T.2 GRACE; `framework_finding_memit_ceiling_archival.md` v1.1 §4.3'.4 patches carry-forward applicability; `rome-patches-canonical.md` v0.2 structural template (15-section parallel-sibling pattern); `memit-patches-canonical.md` v2.5 sibling-parity reference; GRACE paper (Hartvigsen et al., NeurIPS 2023) Table 1 reference values (declarative anchor) |
| Specialist provenance | memit-specialist (primary; GRACE adapter mechanism specification, hparam surface derivation from GRACE paper Table 1, mechanism-orthogonality argument cross-validation); state-consistency-theorist (secondary; adapter-detach unmount mechanism specification per `C-GRACE-5`, covariance cache inapplicability rationale, cross-session bit-exact determinism inheritance); orchestration-comparativist (write-engine architecture comparison surface; adapter-vs-rank-1-update structural comparison codified at §12.2 mechanism-class taxonomy + §12.5 framework-spec relevance scoring); graph-data-architect (light-touch; framework-spec-relevance scoring for adapter-based mechanisms — adapter-based engines closer to `.vindex` overlay model than rank-1-update mechanisms); validation-contract-architect (Cell 6 / Cell 7 / Cell 9 verdict surface inheritance for runbook companion artifact); framework-spec-writer (formalization; sibling-parity discipline preservation) |
| Last updated | 2026-05-05 |

---

*End of GRACE Patches Canonical v0.1 declarative — parallel sibling to `memit-patches-canonical.md` v2.5 (preserved unmodified) and `rome-patches-canonical.md` v0.2 (preserved post-elimination); active forward-target for S2.20 first-execution; verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5'; v0.2 absorption analog session forthcoming post-S2.20 first-execution per parallel ROME v0.1 → v0.2 absorption pattern.*
