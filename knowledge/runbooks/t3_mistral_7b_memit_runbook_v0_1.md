# T.3-α-MISTRAL Runbook — Mistral-7B-v0.3 (base) under MEMIT — v0.1

**Status:** DECLARATIVE (authored S2.29 micro-pass; pod-side execution same session)
**Iteration:** v0.1 first authoring (NEW runbook; not a revision)
**Engine:** MEMIT (canonical engine per `memit-patches-canonical v2.5`)
**Target model:** `mistralai/Mistral-7B-v0.3` (base, NOT Instruct; fp16)
**Axis:** Axis 10 candidate — **first cross-architecture axis** (T.3; re-scoped into WS1 per D-S228-T3-RESCOPE-1)
**Direct structural template:** `t1_alt_model_3b_memit_runbook v0.1` (closest sibling; model-swap inheritance)
**Basis:** S2.29 kickoff; S2.28 close carry-forward; `framework_finding v1.3` §2.4 config idiom + §6 forward; `t_branch v1.2` §6'' T.3 methodology lock; `cross_architecture_axis_scoping_note` §4.1
**Specialist provenance:** memit-specialist (primary; engine + patch + cov-cache + dispatch + the architecture-port adaptations), framework-spec-writer (inheritance map + routing matrix + integrity), state-consistency-theorist (light; determinism chain bootstrap + NV inventory + manifest)
**Persistence:** `/mnt/user-data/outputs/t3_mistral_7b_memit_runbook_v0_1.md`

---

## Part 0 — Orientation

### 0.1 What this runbook is

This runbook executes **T.3-α-MISTRAL**: running the MEMIT write engine against `mistralai/Mistral-7B-v0.3` (the base, non-instruct model) at the canonical hyperparameters and corpus that produced the nine-axis architectural-invariant ceiling on the Llama family. It is a NEW runbook authored by structural inheritance from `t1_alt_model_3b_memit_runbook v0.1` (the closest sibling — same MEMIT engine, same corpus, same trial protocol, model swapped), with the base model swapped from a Llama-family model to a **non-Llama architecture (Mistral)** and the covariance caches re-authored from scratch.

The `α` suffix marks the **first cross-architecture arm**. T.3 is the only remaining axis that can change the *class* of the finding. Every prior axis (1–9) varied something *inside* the Llama-family / MEMIT-mechanism box: hyperparameters, corpus, target, probe locus, layer-set, write-engine (ROME), model scale (8B→3B), and layer band ([2–6]→[4–8]). All nine reproduced the same ceiling. T.3-α is the first axis that varies the **base architecture family**.

### 0.2 The one question this runbook answers, for the operator learning the system

A useful mental model carried from the 3B runbook: MEMIT optimizes an internal vector (the `z` / `v` vector) to drive a new fact into a band of MLP layers. On every Llama model tested — 8B and 3B, across both contested layer bands — that optimizer made enormous *internal* progress (tens of thousands of times improvement in the quantity it minimizes) while the externally-observable consistency probe — "does the model now say the new fact when asked?" — registered a three-to-six-orders-of-magnitude miss against the 0.5 acceptance band. Nine independent perturbations all reproduced this **internal-vs-external split**. That split is the ceiling's defining signature.

T.3-α asks one question: **does that signature reproduce on a non-Llama architecture?** The answer changes what the ceiling *is*:

- **(L) Llama-family-specific** — if Mistral CLEARS (consistency PASS where Llama failed), the ceiling is something about base Llama's representation geometry. The within-regime per-layer sweep on Llama re-activates immediately as a "what's different between the architectures" probe.
- **(G) base-decoder-LM-general** — if Mistral reproduces the `0/5` with the same internal-vs-external split, the ceiling is a property of MEMIT-class in-weight editing on base (non-instruct) autoregressive decoder LMs at canonical hparams, of which Llama is one instance. This is the portable, framework-level result about the write layer — and it routes to the Qwen-7B confirmation arm.

This is **OQ-V12-T-BRANCH-4**, the class-changing read. The primary instrument for it is the dispatch log's internal-vs-external split (§Cell 9 / §Cell 13), not the bare consistency number.

### 0.3 Why Mistral is structurally CLOSER to the 8B canonical than the 3B arm was

A counter-intuitive but load-bearing fact for this port. The 3B arm (Axis 8) required two structural overrides away from the 8B canonical config (a shrunk `v_loss_layer` and a *tied*-embedding `lm_head_module`). Mistral-7B-v0.3 base requires neither of those: it has the **same layer count (32), same hidden size (4096), same intermediate size (14336), and UNTIED embeddings** as Llama-3.1-8B. The MEMIT config's structural fields therefore mostly match the 8B canonical *as-is*. The genuine cross-architecture deltas are narrower and different in kind:

1. **The tokenizer is entirely different.** Mistral uses a SentencePiece tokenizer with `vocab_size ≈ 32768` (v0.3) vs Llama-3's 128256-entry BPE vocab. **Every probe token ID and every target token ID must be re-resolved from scratch** — none of the Llama token IDs (`guitar=17418`, `piano=27374`, etc.) are valid on Mistral. This is the single largest correctness surface in the port (Cell 5 / Cell 6).
2. **The pad-token convention differs.** The Llama Pad-Token patch set `pad_token_id = 128001`. Mistral's tokenizer has no distinct pad token; the community convention (EasyEdit) is `pad_token_id = eos_token_id = 2`. The Pad-Token patch **re-derives** for Mistral (§3.2).
3. **The config attribute names are the unified HF-2.0 schema** (`hidden_size`, `max_position_embeddings`) — which is exactly what **P-4 already handles**; P-4 lists Mistral as a **Required** family (`memit-patches v2.5` §3.5.2). No new patch content; P-4 applies as written.
4. **The module-path templates** (`rewrite_module_tmp`, `mlp_module_tmp`, `layer_module_tmp`) are *expected* to be string-identical to Llama (`model.layers.{}.mlp.down_proj` etc.) because `MistralForCausalLM` is a standard HF gated-MLP decoder, but this is the **highest-risk delta** and is verified empirically by `named_parameters()` at Cell 1.5, never assumed (C-S227-3 discipline).

The net effect: the Mistral port has FEWER hparam-structural overrides than the 3B port, but a LARGER tokenizer-resolution surface. The runbook front-loads the tokenizer re-resolution and the module-path verification accordingly.

### 0.4 Three outcomes, and how the verdict routes

Three outcomes are possible at the Cell 13 gate, and the verdict routes the next session (see §IX):

- **CLEAR (PASS)** — Mistral clears the consistency band where every Llama model could not. The ceiling is **(L) Llama-family-specific**. Major reframe: the within-regime per-layer sweep on Llama re-activates as the "what's different" probe; the framework write-layer claim narrows to Llama. Low prior given nine axes, but this is the one outcome that re-opens the design space.
- **0/5 with signature reproduced (FAIL-with-installation)** — the edit dispatches and runs; the same internal-vs-external split reproduces (`compute_z` drives the internal objective hard; the external probe registers nothing; top-1 never becomes the target). The ceiling is **(G) base-decoder-LM-general**. Routes to the **Qwen-7B confirmation arm** (second non-Llama family, near-decisive for G).
- **FAIL-at-environment** — the cov-cache compute or edit dispatch hits a resource wall before producing a verdict. Unexpected (Mistral-7B fp16 ≈ 14.5 GiB weights; projected ~17–19 GiB peak under MEMIT vs the 24 GiB ceiling — tighter than the 3B arm but fits). Routes to triage (precision relaxation or scope reduction).

### 0.5 Two-surface execution discipline (carried verbatim from S2.24 §9)

Every cell is annotated with its execution surface:

- **Surface A** — pod terminal (SSH). OS-level commands, repo clone, dependency install, patch application, file-system operations, covariance computation launches.
- **Surface B** — JupyterLab notebook on the pod. Model load, probe-panel capture, MEMIT edit dispatch, verdict computation, JSON writes.

Cells spanning both are annotated `[Surface A → B]` with the handoff marked inline. Operator-guidance register (S2.24 §9, carried verbatim): zero-ML-background, one cell at a time; each cell states WHAT it does, WHY, and the expected healthy output BEFORE the operator runs it; a null result (`0/5` with signature) is framed as **signal, not failure** — it is the load-bearing scientific outcome this session is built to detect. Claude makes all calls and proceeds; only irreversible operations (the model pull + license accept, the ~45-min cov compute launch, any NV-destructive op) are surfaced for explicit confirmation before dispatch.

### 0.6 Block structure

```
═══════════════════════════════════════════════════════════════════
  BLOCK A — Pre-flight (Cells 0–8)
     Pod bring-up + deps, engine clone + snapshot, Mistral module
     introspection (HIGHEST-RISK port check), patch application
     (P-4 Required; Pad-Token RE-DERIVED), cov-cache entry gate,
     MEMIT hparam config (Mistral structural fields + EasyEdit
     reference band), baseline PRODUCE (Checkpoint #1 on Mistral —
     fresh determinism chain), token re-resolution + allowlist,
     pre-edit panel, FRESH covariance computation

  BLOCK B — Dispatch + verdict (Cells 9–13)
     MEMIT joint-overlay edit at the reference band, verdict surface,
     Copy-Unmount, per-trial JSON, Cell 13 3-route gate (EXTENDED
     with T.3-α cross-architecture routing matrix)

  BLOCK C — Confirmatory pass (Cells 14–17) [verdict-conditional]
     Route-A discipline: single confirmatory dispatch when 0/5 is
     established; Route B 15-trial only if Mistral approaches the band

  BLOCK-END (Cells 18–20)
     Cov-cache integrity gate, NV inventory, manifest extension
═══════════════════════════════════════════════════════════════════
```

### 0.7 Engine-class note for the operator

MEMIT on Mistral behaves identically in mechanism to MEMIT on Llama — the engine code is byte-identical; only the model it operates on changes. Two engine-class properties carry forward unchanged:

1. **MEMIT consumes covariance caches.** MEMIT's least-squares update needs a per-layer second-moment statistic (`mom2`) computed over a Wikipedia corpus. The Llama caches on NV are keyed on the Llama architecture and are **useless for Mistral** (different `hidden_size`-keyed paths and a different model). Cell 8 computes these fresh for Mistral — the single most expensive cell (~45–75 min for the 5-layer band; Mistral's `intermediate_size=14336` matches 8B, so per-layer cache size ≈ the 8B caches, larger than the 3B arm's).
2. **MEMIT modifies weights in place; Copy-Unmount applies.** MEMIT's joint-overlay edit is reversed by the bit-exact Copy-Unmount mechanism validated across 5 layer-ranges on Llama. This runbook inherits Copy-Unmount; a successful Mistral unmount at `drift=0.00e+00` would be the **6th validated config** (and the first on a non-Llama architecture — a meaningful determinism-discipline extension).

---

## Part I — Inheritance Map

### 1.1 Inheritance lineage

```
═══════════════════════════════════════════════════════════════════
        stage_1_sect_runbook v1.7   (root MEMIT-side runbook)
                  │
                  │  model swap 8B → 3B  (Axis 8)
                  ▼
        t1_alt_model_3b_memit_runbook v0.1   (DIRECT structural template)
                  │
                  │  model swap Llama-3.2-3B → Mistral-7B-v0.3
                  │  (cross-architecture; Axis 10 candidate)
                  ▼
        t3_mistral_7b_memit_runbook v0.1   ◄── (this artifact)
═══════════════════════════════════════════════════════════════════

Sibling references (NOT load-bearing for authoring):
  - t1_alt_model_3b_memit_akd_runbook v0.1   (AKD instrument — Cell P1 source IF AKD pre-flight added)
  - t1_band_4_8_runbook v0.1                  (band [4–8] single-variable pattern — band already adopted here)
  - t2_rome_runbook v0.2                      (ROME-side; eliminated S2.18; forensic record)
```

### 1.2 Direct-inheritance surfaces

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition | `t1_alt_model_3b_memit_runbook v0.1` Part IV–VII | verbatim with §1.4 substitutions |
| Patch application discipline | `memit-patches-canonical v2.5` §6–§7 | verbatim (Pad-Token RE-DERIVED; see §3.2) |
| Constraint registry | `memit-patches-canonical v2.5` §3 + §10 | verbatim |
| Verdict surface taxonomy | `t1_alt_model_3b_memit_runbook v0.1` Cell 10 / `stage_1_sect_runbook v1.7` §7 | verbatim |
| Trial protocol | IC-S24-4 (5 facts × 3 replicates; Route-A single-dispatch) | verbatim |
| Acceptance bands | 0.5 cons / 0.05 gen / 0.05 spec / 1e-4 unmount | verbatim (model-agnostic) |
| Verdict-integrity subset | D-S215D2-VERDICT-INTEGRITY-1 {cfb-v3-001/002/005} | verbatim |
| Copy-Unmount mechanism | `memit-patches-canonical v2.5` (IC-S23-4) | verbatim (APPLICABLE under MEMIT; in-place weight restore is architecture-agnostic) |
| Forward routing matrix | `t1_alt_model_3b_memit_runbook v0.1` §IX | EXTENDED (T.3-α cross-architecture routing per §IX) |

### 1.3 Cell delta map

| Cell | Delta class | Notes |
|---|---|---|
| 0 | structural inheritance verbatim | OS preamble + dependency install; Mistral SentencePiece dep (`sentencepiece`) load-bearing |
| 1 | structural inheritance | MEMIT engine clone + snapshot at canonical SHA (same engine as Llama arms) |
| 1.5 | RE-AUTHORED — Mistral module introspection | **HIGHEST-RISK port check**: verify `model.layers.{}.mlp.down_proj` exists on `MistralForCausalLM` via `named_parameters()`; verify `lm_head.weight` PRESENT (untied) |
| 2 | structural inheritance + Pad-Token RE-DERIVATION | P-4 Required (Mistral family); Pad-Token re-derived to `eos_token_id` (§3.2) |
| 3 | APPLICABLE — cov-cache entry gate | expect `mistral_7b_v0_3` cov dir ABSENT at first execution |
| 4 | RE-AUTHORED — Mistral structural fields + reference band | `v_loss_layer=31`, `lm_head_module=lm_head` (UNTIED — 8B-form not 3B-form), band `[4,5,6,7,8]` (EasyEdit reference per OQ-V12-T-BRANCH-3) |
| 5 | INVERTED — baseline PRODUCER (Checkpoint #1 on Mistral) | PRODUCES `mistral_7b_v0_3_baselines.json`; FIRST determinism checkpoint in a fresh Mistral chain (no prior baseline to consume) |
| 6 | RE-AUTHORED — token re-resolution against Mistral tokenizer | ALL target/probe token IDs re-resolved; multi-token classification re-run from scratch (harp proxy re-checked) |
| 7 | structural inheritance | pre-edit baseline against current Mistral state |
| 8 | RE-AUTHORED — fresh Mistral cov computation | `/workspace/covariance_caches/mistral_7b_v0_3/`; ~45–75 min for `[4..8]` |
| 9–12 | structural inheritance | MEMIT edit dispatch + verdict surface + Copy-Unmount + JSON |
| 13 | EXTENDED — T.3-α cross-architecture routing matrix | 3-route gate + §IX routing; internal-vs-external signature is the PRIMARY read |
| 14–17 | declarative inheritance | Block C (Route-A single confirmatory dispatch default) |
| 18 | APPLICABLE — cov-cache integrity gate | verifies fresh Mistral computation post-Cell-8 |
| 19–20 | structural inheritance | NV inventory + manifest extension |

### 1.4 Substring substitutions for verbatim cells

| Substitution | Pattern |
|---|---|
| Model name | `meta-llama/Llama-3.2-3B` → `mistralai/Mistral-7B-v0.3` |
| Revision SHA | pinned at Cell 1 entry (OQ-V12-T-BRANCH-1; resolve against the HF model card at session entry; recorded in Cell 20 manifest) |
| Baseline path | `llama_3_2_3b_baselines.json` → `mistral_7b_v0_3_baselines.json` |
| Output paths | `t1_alt_model_3b_memit_*` → `t3_mistral_7b_memit_*` |
| Cov cache path | `/workspace/covariance_caches/llama_3_2_3b/...` → `/workspace/covariance_caches/mistral_7b_v0_3/...` |
| Layer paths | `model.layers.{2..6}.mlp.down_proj` → `model.layers.{4..8}.mlp.down_proj` (reference band) |
| Layer band | `[2,3,4,5,6]` → `[4,5,6,7,8]` (EasyEdit reference; Axis-9-validated equivalent) |
| `v_loss_layer` | `27` → `31` (n_layers−1 = 32−1) |
| `lm_head_module` | `model.embed_tokens` (3B tied) → `lm_head` (Mistral UNTIED) |
| `pad_token_id` | `128001` → `2` (Mistral eos) |

---

## Part II — Architecture Swap Reference (Llama-3.2-3B → Mistral-7B-v0.3)

### 2.1 Architecture comparison (three-way, with the 8B canonical for context)

| Property | Llama-3.1-8B (canonical) | Llama-3.2-3B (Axis 8) | **Mistral-7B-v0.3 (T.3-α)** |
|---|---|---|---|
| `model_type` | `llama` | `llama` | **`mistral`** |
| HF class | `LlamaForCausalLM` | `LlamaForCausalLM` | **`MistralForCausalLM`** |
| Hidden size | 4096 | 3072 | **4096** |
| Intermediate size | 14336 | 8192 | **14336** |
| Decoder layers (`n_layers`) | 32 | 28 | **32** |
| `v_loss_layer` (= n−1) | 31 | 27 | **31** |
| `tie_word_embeddings` | False | **True** | **False** |
| `lm_head_module` | `lm_head` | `model.embed_tokens` | **`lm_head`** |
| `down_proj` shape | `Linear(14336, 4096)` | `Linear(8192, 3072)` | **`Linear(14336, 4096)`** |
| fp16 weight footprint | 16.06 GiB | 6.42 GiB | **~14.5 GiB** |
| Tokenizer | Llama-3 BPE | Llama-3 BPE | **Mistral SentencePiece (v3)** |
| `vocab_size` | 128256 | 128256 | **32768** |
| `pad_token_id` convention | 128001 | 128001 | **2 (= eos)** |
| `max_position_embeddings` | 131072 | 131072 | **32768** |

**Reading of the table.** The Mistral column is structurally nearer the 8B canonical column than the 3B column is, on every field except the bottom four (tokenizer, vocab, pad convention, context window). The MEMIT *hparam-structural* port is therefore lighter than the 3B port; the *tokenizer* port is heavier.

### 2.2 MEMIT edit-site validity on Mistral

MEMIT reference band for the Mistral/Llama-7B architecture per EasyEdit (arXiv 2308.07269 Table 4): `[4, 5, 6, 7, 8]`, value-loss layer `model.layers.31`, target module `model.layers.{}.mlp.down_proj`. Per the §6''.1 methodology lock (OQ-V12-T-BRANCH-3): **adopt the engine's reference band for the target architecture; do NOT re-sweep.** Axis 9 (S2.27) established that the `[4–8]` band is empirically equivalent to the `[2–6]` canonical band on Llama (`delta_vs_2_6_floor ≈ 0`), so adopting `[4–8]` for Mistral keeps the result interpretively clean — it is a band already confirmed non-load-bearing.

| Layer | Mistral validity (`0 ≤ idx < 32`) | Relative depth (Mistral) | Memo |
|---|---|---|---|
| L4 | VALID | 12.5% | band entry (EasyEdit MEMIT critical-range start) |
| L5 | VALID | 15.6% | ROME single-layer site (EasyEdit) |
| L6 | VALID | 18.8% | |
| L7 | VALID | 21.9% | |
| L8 | VALID | 25.0% | band exit (MLP/hidden severance disparity collapses after L8 per EasyEdit) |

`C-S229-4` asserts the bound `0 ≤ idx < 32` for every index in `[4..8]` at Cell 4 entry.

### 2.3 VRAM projection (RTX 4090 24 GiB)

```
═══════════════════════════════════════════════════════════════════
  Component                                       VRAM cost
  ─────────────────────────────────────────────────────────
  Model weights (fp16, 7.25B)                     ~14.5 GiB
  Activations + gradient accumulation (5-layer)   ~3–4  GiB
  mom2 inverse + workspace                        ~1–2  GiB
  cuBLAS + workspace                              0.50  GiB
  ─────────────────────────────────────────────────────────
  Total under MEMIT canonical hparams:            ~19–21 GiB
  RTX 4090 ceiling:                               24.00 GiB
  HEADROOM:                                       3–5 GiB   ← fits, but TIGHTER than 3B/8B
═══════════════════════════════════════════════════════════════════
```

Provenance: Mistral-7B fp16 weights (~14.5 GiB) sit between the 3B (6.42) and 8B (16.06) footprints. The MEMIT joint-overlay at L4-L8 on 8B ran at ~14 GiB peak (S2.15-D2 reference) on a 16 GiB-weight model; Mistral's lighter weights but identical `intermediate_size` put the projected peak at ~19–21 GiB. **Headroom is tighter than any prior arm** — `OQ-S229-VRAM-1` confirms empirically at Cell 8/9. Mitigation if exceeded: the cov compute (Cell 8) is the larger consumer and runs without the edit-time activation retention, so an OOM is more likely at edit dispatch (Cell 9); fall-back is single-layer scope or fp16 cov-only relaxation (§IX FAIL-at-environment route).

---

## Part III — Patch Inheritance

### 3.1 Patch applicability matrix

| Patch | Mistral-7B applicability | Defect class | Provenance |
|---|---|---|---|
| P-1 (`.upstream_pristine` + parent_module substitution) | APPLICABLE | Universal HF transformer with numeric submodule indices | `memit-patches v2.5` §2 |
| P-2 (fp16 cdist; cov-compute backward) | APPLICABLE | Universal fp16-loaded model | `memit-patches v2.5` §2 |
| P-3' + Device-Map | NOT APPLICABLE — single-GPU RTX 4090 dispatch; no multi-GPU sharding | `memit-patches v2.5` §3 / §5 |
| **P-4 (config-attribute compat for non-GPT-2-family)** | **APPLICABLE — REQUIRED** (Mistral is explicitly listed Required in §3.5.2) | `n_embd`/`n_positions` → `hidden_size`/`max_position_embeddings` getattr-fallback | `memit-patches v2.5` §3.5 |
| P-5 (dataset-loader modernization) | APPLICABLE — corpus-side, model-agnostic | `memit-patches v2.5` §3.6 |
| P-6 (`size_suffix` f-string `_t100_` segment) | APPLICABLE — cache-filename-side, model-agnostic | `memit-patches v2.5` §3.7 |
| P-7 (`batch_tokens` propagation to `layer_stats`) | APPLICABLE — load-bearing (Mistral `max_position_embeddings=32768` >> 8192 threshold; same regime as 8B) | `memit-patches v2.5` §3.8 |
| **Pad-Token** | **APPLICABLE — RE-DERIVED** (Mistral has no distinct pad token; set to `eos_token_id=2`) | tokenizer attribute | `memit-patches v2.5` §4 + §3.2 below |
| Copy-Unmount | APPLICABLE — in-place weight restore is architecture-agnostic; 6th validated config if `drift=0.00e+00` | IC-S23-4 |

**Patches NOT applicable** (GRACE-side, S2.22): P-1-GRACE / P-2-GRACE / F-2 (CONFIGURATION_LAYER) / GRACE adapter-detach unmount.

**Key port observation.** P-4 — the patch that resolves `AttributeError: 'LlamaConfig' object has no attribute 'n_embd'` by routing to the unified HF-2.0 config schema — is the patch that makes the engine work on *any* non-GPT-2-family model. `memit-patches v2.5` §3.5.2 already lists **Mistral family as Required**, and §3.5.5 names Mistral explicitly in the rationale. P-4 is therefore not a re-derivation; it applies verbatim and is the structural reason the MEMIT engine runs on Mistral without code change beyond the patch set that already runs on Llama.

### 3.2 Pad-Token RE-DERIVATION for Mistral (the one patch that changes content)

The Llama Pad-Token patch (`memit-patches v2.5` §4) set `tokenizer.pad_token_id = 128001` (a dedicated Llama-3 reserved token). Mistral's SentencePiece tokenizer has no distinct pad token. The community-standard convention — EasyEdit's own Mistral handling (`editor.py`: `self.tok.pad_token_id = self.tok.eos_token_id` for any `mistral` model) — sets the pad token to the EOS token. Mistral-7B-v0.3 base has `eos_token_id = 2`.

**Re-derived Pad-Token form for Mistral:**
```
tokenizer.pad_token_id = tokenizer.eos_token_id   # = 2 for Mistral-7B-v0.3
```

This is functionally equivalent to the Llama patch's purpose (give MEMIT's batched tokenization a valid pad id so padded-batch forward passes don't raise) but uses Mistral's convention. The patch is applied at Cell 2 and verified by asserting `tokenizer.pad_token_id == tokenizer.eos_token_id == 2` (`C-S229-PADTOKEN-1`). `per_variant_notes` in §4.4 of the canonical anticipated exactly this branch ("Otherwise leave as-is" / per-family handling).

### 3.3 P-7 note for Mistral (operator-facing)

P-7 propagates `batch_tokens=100` into MEMIT's edit-time `get_cov` → `layer_stats` chain so the covariance cache filenames carry the `_t100_` segment and the edit-time lookup hits. Mistral's `max_position_embeddings = 32768` is far above the `8192` threshold — same regime as Llama-3.1-8B — so P-7 is **load-bearing**: without it the edit-time lookup constructs filenames lacking `_t100_`, misses the Cell 8 caches, and falls back to a full-`npos` local compute that OOMs (especially likely given the tighter Mistral VRAM headroom, §2.3). `D-S229-PATCH-INHERITANCE-1` records that all MEMIT patches inherit per `memit-patches v2.5` and the engine source is byte-identical to the Llama baseline (verified via patch-site line numbers at Cell 1.0).

### 3.4 Process constraints (carry-forward)

`C-S25-15` / `C-S26-1` / `C-S26-2` / `C-S26-3` / `C-S28-1` carry forward verbatim from `memit-patches v2.5`. The R1.1 / R1.2 / R1.3 cell-level gates apply; R1.3 (canonical dry-run gate) absorbs into the post-compute verification gate (`C-S229-3`) at Cell 8 close, as in the 3B arm.

---

## Part IV — BLOCK A: Pre-flight

### Cell 0 — Pod bring-up + dependency install  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Bring the pod to a known dependency state. Carries the S2.24 lesson (`OQ-S222-CELL0-DEPS-1`): fresh pod images require explicit installation; do not assume preinstalled deps.

**WHAT / WHY (operator-facing):** This cell confirms the GPU is the expected RTX 4090, confirms the Network Volume is mounted, and installs the Python packages the engine needs. Mistral's tokenizer is SentencePiece-based, so `sentencepiece` is load-bearing here in a way it was incidental on Llama — without it the tokenizer load at Cell 5 fails.

**Cell body (operator reading order):**
1. Confirm pod identity + GPU: `nvidia-smi` (expect single RTX 4090, 24 GiB). **Expected healthy output:** one GPU line, 24576 MiB total, ~0 MiB used.
2. Confirm NV mount: `ls /workspace` (expect existing `covariance_caches/`, `architecture_profile/`, `session_logs/`).
3. Install pinned dependencies (Surface A; explicit):
   - `transformers` (engine-compatible pin per `memit-patches v2.5` engine SHA; Mistral support is present in all transformers ≥ 4.34, so the canonical pin already covers it)
   - `accelerate`, `hydra-core`, `pyyaml`, **`sentencepiece`** (load-bearing for the Mistral tokenizer), `protobuf` (SentencePiece dependency)
   - any MEMIT-specific deps surfaced at Cell 1.5 introspection (re-run install if introspection reveals a gap).
4. Print acceptance string: `CELL0_DEPS_OK <transformers_version> <accelerate_version> sentencepiece=<version>`.

**Halt conditions:**
- GPU is not RTX 4090 24 GiB → halt (VRAM projection §2.3 invalid; the Mistral headroom is already tight — a smaller GPU does not fit).
- NV mount absent → halt (no durable tier).
- Dependency install fails (esp. `sentencepiece`) → halt; triage before Cell 1.

---

### Cell 1 — MEMIT engine clone + NV snapshot  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Clone the canonical MEMIT engine at its pinned SHA and snapshot the source to NV. The engine is the SAME engine run on every Llama arm — byte-identical. Absorbs `OQ-S222-CELL1-2` (snapshot source to a content-addressed NV path at first clone).

**WHAT / WHY (operator-facing):** We are NOT cloning anything Mistral-specific. The whole point of the cross-architecture test is that the engine is unchanged; only the model it operates on differs. This cell clones that unchanged engine and proves (Cell 1.0) it is byte-identical to what ran on Llama, so any result difference is attributable to the model, not engine drift.

**Cell body (operator reading order):**
1. Resolve and pin the target model HF revision SHA (`OQ-V12-T-BRANCH-1`): record the current `mistralai/Mistral-7B-v0.3` base revision commit SHA from the HF model card at session entry; print `MISTRAL_MODEL_SHA <sha>`. (License/gating: accept the Mistral model license on HF for this account before the pull — separate acceptance from any Llama gating per §6''.2.)
2. Clone the canonical MEMIT engine repo (forked, pinned per `memit-patches v2.5` §9 anchor SHA).
3. Record the engine SHA (`C-S229-1`): print `MEMIT_ENGINE_SHA <sha>`; carried into the Cell 20 manifest.
4. **Cell 1.0 byte-identity check (`D-S229-PATCH-INHERITANCE-1`):** verify the engine source is byte-identical to the Llama baseline at the patch-site line numbers in `memit-patches v2.5` (P-1/P-2/P-4/P-5/P-6/P-7 anchor lines). Print per-patch-site match/mismatch. Any mismatch → halt.
5. **Engine source snapshot (`C-S229-2`):** copy the clean engine source to `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` BEFORE any patch. Print `ENGINE_SNAPSHOT_OK <path>`.

**Halt conditions:**
- Clone fails (network / auth) → halt.
- Mistral license not accepted (model pull at Cell 5 will 401) → surface to operator; halt until accepted.
- Cell 1.0 byte-identity mismatch at any patch site → halt; reconcile patch line numbers against the actual SHA.

---

### Cell 1.5 — Mistral module introspection (RE-AUTHORED — HIGHEST-RISK PORT CHECK)  [Surface B]

**Specialist:** memit-specialist
**Purpose:** RE-AUTHORED for the Mistral architecture. This is the **highest-risk delta in the entire port** (per §6''.2 / OQ-V12-T-BRANCH-2). The MEMIT hparams reference module paths by string template (`rewrite_module_tmp = 'model.layers.{}.mlp.down_proj'`, etc.). If `MistralForCausalLM` names its MLP down-projection differently from `LlamaForCausalLM`, the edit silently targets the wrong (or a non-existent) module. This cell verifies the actual named modules BEFORE any config is built.

**WHAT / WHY (operator-facing):** Mistral and Llama are both standard HF decoder transformers and are *expected* to use identical module names — but "expected" is not "verified." This cell loads the model's parameter name list and confirms the exact strings MEMIT will format into exist. It also confirms `lm_head.weight` is a real, untied parameter (it is, for Mistral) — the inverse of the 3B case, where `lm_head.weight` was absent (tied) and forced the `model.embed_tokens` override. Getting this wrong is the single most likely cause of a spurious or misleading result.

**Cell body (operator reading order):**
1. Load `mistralai/Mistral-7B-v0.3` at the pinned SHA, fp16 (first model load; ~14.5 GiB — confirm it fits, ~0 MiB → ~15 GiB on `nvidia-smi`).
2. Enumerate `model.named_parameters()` and assert the presence of, for a representative layer in the reference band (e.g., L5):
   - `model.layers.5.mlp.down_proj.weight` (the MEMIT `rewrite_module_tmp` target) — **shape must be `[4096, 14336]`** (the `down_proj` weight is `out_features × in_features = hidden × intermediate`).
   - `model.layers.5.mlp` (the `mlp_module_tmp` target).
   - `model.layers.5` (the `layer_module_tmp` target).
   - `model.layers.31` (the `v_loss_layer` target, n−1).
3. **Untied-embedding verification (`C-S229-LMHEAD-1`, the inverse of the 3B check):** assert `lm_head.weight` IS PRESENT in `named_parameters()` (Mistral `tie_word_embeddings=False`). This confirms `lm_head_module='lm_head'` is the correct config field — the 8B-canonical form, NOT the 3B tied `model.embed_tokens` override. If `lm_head.weight` is unexpectedly absent (would indicate a tied-embedding Mistral variant), fall back to the tied-embedding adaptation per `D-S227-LMHEAD-1` and re-derive `lm_head_module`.
4. Confirm the engine's MEMIT package surface (`memit_main`, `rome/layer_stats`, `util/nethook`) resolves as on Llama (engine unchanged).
5. Print `MISTRAL_MODULE_INTROSPECT_OK` with: the 4 resolved module-path strings, the `down_proj` weight shape, and `lm_head_untied=True`.

**Halt conditions:**
- Any of the 4 module-path templates does not resolve to a real named module → halt (module-name mismatch; the MEMIT module-path templates require Mistral-specific re-derivation before any edit — do NOT proceed on assumed paths).
- `down_proj.weight` shape ≠ `[4096, 14336]` → halt (architecture mismatch vs the config the runbook was authored against).
- `lm_head.weight` absent → branch to tied-embedding adaptation (do not halt; re-derive `lm_head_module` per §2.4 of framework_finding v1.3 and re-run).

---

### Cell 2 — MEMIT patch application (+ Pad-Token RE-DERIVATION)  [Surface A → B]

**Specialist:** memit-specialist
**Purpose:** Apply the MEMIT patch set per `memit-patches v2.5` §6–§7 and report patch state. Pad-Token is RE-DERIVED for Mistral (§3.2).

**WHAT / WHY (operator-facing):** These patches make the GPT-J-authored MEMIT engine run correctly on a modern HF model. P-4 is the load-bearing one for cross-architecture: it routes the engine's old `n_embd`/`n_positions` config lookups to the modern `hidden_size`/`max_position_embeddings` that Mistral uses — exactly as it does for Llama. The one patch that changes content for Mistral is Pad-Token, set to the EOS token per Mistral convention.

**Cell body (operator reading order):**
1. Apply patches in canonical order: P-1, P-2, P-4, P-5, P-6, P-7, **Pad-Token (re-derived: `pad_token_id = eos_token_id = 2`)**. (P-3' and Device-Map are NOT applied — single-GPU RTX 4090 per §3.1.)
2. Each patch prints `PATCH <id> APPLIED`. P-7 requires BOTH post-state markers present; partial-marker → halt. **P-4 must report APPLIED at all four sites** (`compute_z.py`, `compute_v.py`, `layer_stats.py` ×2) — P-4 is the patch most likely to matter for a non-Llama model, so its application is verified explicitly.
3. **Pad-Token verification (`C-S229-PADTOKEN-1`):** assert `tokenizer.pad_token_id == tokenizer.eos_token_id == 2`. Print `PADTOKEN_MISTRAL_OK pad=eos=2`.
4. Construct the patch-state record matching `memit-patches v2.5` §8 schema. `patches_required_but_not_applied` MUST be empty.
5. Print `CELL2_PATCH_STATE_OK` with the full `patches_applied` dict.

**Halt conditions:**
- Any patch reports a partial-marker state → halt (reconcile per §3.8.7).
- P-4 NOT applied at all four sites → halt (the engine will raise `AttributeError` on Mistral's config at first `compute_z`).
- `patches_required_but_not_applied` non-empty → halt.
- Pad-Token assertion fails (`pad_token_id != 2`) → halt (batched tokenization will misbehave).

---

### Cell 3 — Covariance-cache entry gate  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Check whether any `mistral_7b_v0_3` covariance caches already exist at NV. At first T.3-α execution, NONE exist — this cell confirms absence and sets the expectation that Cell 8 computes fresh.

**Cell body (operator reading order):**
1. List `/workspace/covariance_caches/mistral_7b_v0_3/.../wikipedia_stats/` (expect: absent or empty at first execution).
2. If absent/empty → print `COV_CACHE_MISTRAL_ABSENT — Cell 8 will compute fresh` and set `cov_cache_compute_required = True`.
3. If present (re-execution) → verify per-layer file size + checksum against the Cell 8 provenance record; print `COV_CACHE_MISTRAL_PRESENT — integrity {OK|MISMATCH}`. On MISMATCH → halt.

**Halt conditions:**
- Present-but-corrupt cov cache (checksum mismatch) → halt.

---

### Cell 4 — MEMIT hyperparameter config (RE-AUTHORED — Mistral structural fields)  [Surface B]

**Specialist:** memit-specialist
**Purpose:** RE-AUTHORED for Mistral. Build the MEMIT hparams by the scale-variant config idiom (`framework_finding v1.3` §2.4, generalized to cross-architecture per §6''.1): **load the 8B-canonical MEMIT JSON, override only the architecture-structural fields.** For Mistral those overrides are fewer than the 3B arm (untied embeddings, same dims, same layer count) plus the reference-band adoption.

**WHAT / WHY (operator-facing):** The config tuning knobs (`v_lr`, `mom2_update_weight`, grad steps) carry forward UNCHANGED from the configuration validated across all nine Llama axes — we are explicitly NOT re-tuning, because re-tuning would conflate an architecture difference with a hparam difference and destroy the single-variable interpretation. Only the fields forced by the architecture change (layer count, embedding tying, the edit band) are overridden.

**Cell body (operator reading order):**
1. Load the reference MEMIT JSON (8B-canonical) and apply the architecture-structural overrides:

| Hparam | Value | Override class | Provenance |
|---|---|---|---|
| MEMIT layer set | `[4, 5, 6, 7, 8]` | **OVERRIDE — reference band** | EasyEdit MEMIT critical-range for Llama/Mistral-7B (arXiv 2308.07269 Table 4); OQ-V12-T-BRANCH-3; Axis-9-validated equivalent to `[2–6]` |
| `v_loss_layer` | `31` | **OVERRIDE — structural** (n−1 = 32−1) | §2.1; same value as 8B by layer-count coincidence |
| `lm_head_module` | `lm_head` | **OVERRIDE — structural** (untied; reverts 3B's tied override back to 8B form) | C-S229-LMHEAD-1 (Cell 1.5 verified untied) |
| `mom2_update_weight` | 15000 | INHERIT (tuning knob; NOT re-tuned) | S2.10 PASS configuration |
| `v_lr` | 0.5 | INHERIT | S2.10 PASS configuration |
| `v_num_grad_steps` | 25 | INHERIT | S2.10 PASS configuration |
| `kl_factor` | 0.0625 | INHERIT | canonical |
| `rewrite_module_tmp` | `model.layers.{}.mlp.down_proj` | INHERIT (verified at Cell 1.5) | §2.1 |
| `mlp_module_tmp` | `model.layers.{}.mlp` | INHERIT (verified) | §2.1 |
| `layer_module_tmp` | `model.layers.{}` | INHERIT (verified) | §2.1 |
| `mom2_dataset` / `mom2_n_samples` / `mom2_dtype` | `wikipedia` / 100000 / `float32` | INHERIT | canonical envelope |
| Edit dispatch | joint-overlay 5-fact | INHERIT | S2.14-D D.3 protocol |

2. **`C-S229-4` bound assertion:** assert every index in `[4..8]` satisfies `0 ≤ idx < n_layer = 32`. Print `LAYER_BOUND_OK [4..8] < 32`.
3. **Full-field diff record (`C-S229-2-DIFF`):** print the complete `MEMITHyperParams` and annotate each field INHERIT vs OVERRIDE, so the single-variable claim (architecture-only) is auditable at the field level. The ONLY tuning-knob value that differs from the 8B canonical is `layers` (the reference band) — and that band is Axis-9-validated as equivalent.
4. Print `CELL4_HPARAM_OK` with the full config + the INHERIT/OVERRIDE annotation map.

**Open question carried:** `OQ-S229-1` — whether `mom2_update_weight=15000` (the Llama PASS value) is correctly calibrated at Mistral scale, or requires re-tuning. PROVISIONAL inheritance; not resolved at authoring (resolving it is out of scope for the single-variable architecture port — re-tuning is a deeper arm).

**Halt conditions:**
- Layer bound assertion fails → halt (config error).
- `lm_head_module` set to a value Cell 1.5 did not verify present → halt (config/introspection inconsistency).

---

### Cell 5 — Baseline PRODUCE (Checkpoint #1 on Mistral — fresh determinism chain)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** PRODUCES `mistral_7b_v0_3_baselines.json` — the FIRST determinism checkpoint in a fresh Mistral chain. Unlike the 3B Cell 5 (which CONSUMED a GRACE-produced baseline), there is no prior Mistral baseline to consume; this cell establishes Checkpoint #1 (§6''.3: "establish a fresh determinism chain per new model"). The baseline is engine-agnostic (captures untouched-model forward-pass state at the pinned SHA) and is the producer artifact a future Mistral re-run (or the Qwen confirmation arm's analog) would consume.

**WHAT / WHY (operator-facing):** Before editing anything, we record exactly what the untouched Mistral model predicts on all 38 probes. This is the "before" picture. Two jobs: (1) it is the reference for every "did the edit change this?" comparison later; (2) re-running it on a fresh load and getting bit-identical numbers is how we prove the model loads deterministically — the foundation that lets us attribute any later difference to the edit, not to load noise.

**Cell body (operator reading order):**
1. Load `mistralai/Mistral-7B-v0.3` at the pinned SHA, fp16 (reuse the Cell 1.5 load if still resident).
2. Capture the 38-probe panel pre-edit (5 facts × {3 consistency + 3 generalization + 1 unmount} + 3 shared specificity): for each probe record `top_1_token_id`, `p_top_1_pre`, `top_5`, and (consistency/unmount) `p_target_new_pre` / `p_target_true_pre`. **Prompts are held verbatim from probe-set-v3** (the prompt STRINGS are model-agnostic; only the token IDs differ — those are resolved in Cell 6).
3. Capture per-fact `target_true` = the model's natural top-1 at the canonical prompt `{subject} plays the instrument of`, and its probability. (On Mistral this is re-captured fresh — the Llama ` his`/` her` top-1s are NOT assumed; Mistral's natural completion may differ.)
4. **Determinism self-check (Checkpoint #1, `C-S229-CHECKPOINT-1`):** capture the panel TWICE on the same loaded model; assert bit-exact agreement (`drift = 0.00e+00` across all 38 probes, 0 top-1 mismatches). This is the within-session determinism floor; a fresh-reload cross-session gate is established when a later session consumes this baseline.
5. Write `mistral_7b_v0_3_baselines.json` to NV with: model SHA, `n_layer=32`, `hidden_size=4096`, `intermediate_size=14336`, per-fact target/true captures, per-probe panel, `pad_token_id=2`.
6. Print `CHECKPOINT_1_MISTRAL_OK drift_max=<value>` and `CELL5_BASELINE_PRODUCED <path>`.

**Halt conditions:**
- Within-session determinism self-check fails (`drift > 0`) → halt (nondeterministic load; cannot establish a clean baseline — triage before any edit).
- Model load OOM (~14.5 GiB should fit with margin pre-edit) → halt (environment).

---

### Cell 6 — Token re-resolution + MULTI_TOKEN_ALLOWLIST (RE-AUTHORED — Mistral tokenizer)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** RE-AUTHORED. This is the LARGEST correctness surface in the port. NONE of the Llama token IDs are valid on Mistral's SentencePiece vocab. Re-resolve every target_new token ID against the Mistral tokenizer and re-run the multi-token classification from scratch. The harp first-token-proxy must be re-evaluated against the new vocab (`D-S215D2-CFB-V3-004-PROXY-1` re-checked, §6''.2).

**WHAT / WHY (operator-facing):** A "token" is a chunk of text the model reads as one unit. Different tokenizers chop words differently. On Llama, `guitar` was one token (id 17418). On Mistral, `guitar` might be one token with a totally different id, or it might be split into pieces (`gu` + `itar`). MEMIT's consistency check measures the probability of the target token(s); if we used Llama's ids on Mistral we'd be measuring the wrong thing entirely. This cell re-resolves all five targets and classifies each as single-token (clean) or multi-token (needs the first-token-proxy treatment).

**Cell body (operator reading order):**
1. For each fact, tokenize `target_new` with a leading space against the Mistral tokenizer (matching the `{subject} plays the instrument of ___` continuation form) and record the full token-id list:
   - cfb-v3-001 `guitar` → Mistral ids `[?]` → classify STRICT_SINGLE_TOKEN if length 1, else MULTI_TOKEN
   - cfb-v3-002 `piano` → Mistral ids `[?]`
   - cfb-v3-003 `violin` → Mistral ids `[?]`
   - cfb-v3-004 `harp` → Mistral ids `[?]` (was `[4960, 79]` multi-token on Llama; re-check — Mistral's 32k SentencePiece vocab may tokenize `harp` differently, possibly single-token)
   - cfb-v3-005 `flute` → Mistral ids `[?]`
   
   **Authoring note:** the exact Mistral ids cannot be authored offline (they depend on the live tokenizer); the cell resolves them at execution and prints them. The classification logic and the allowlist gate are fully specified below; only the literal id integers are execution-resolved. This is the one place where a literal value is necessarily execution-time (a tokenizer query), not a placeholder for operator judgment.
2. **Build `MULTI_TOKEN_ALLOWLIST` fresh from the Mistral classification** (do NOT inherit the Llama `{"cfb-v3-004"}` allowlist — it was specific to the Llama tokenization of `harp`). Any fact tokenizing multi-token on Mistral is added to the Mistral allowlist with `verdict_class = ALLOWLIST_FIRST_TOKEN_PROXY` and `re_evaluate_at_trial_0 = True`; its first token id is the proxy.
3. **SUBSET hard gate (`D-S217-2` discipline):** assert the Mistral allowlist covers every fact whose `verdict_class == MULTI_TOKEN`. Any multi-token fact absent from the allowlist → `MULTI_TOKEN_FAIL` (session-level HARD halt) until added AND its first-token-proxy is confirmed acceptable.
4. **Harp-proxy re-evaluation note (`OQ-S229-HARP-1`):** if `harp` is single-token on Mistral (plausible given SentencePiece), the cfb-v3-004 first-token-proxy mechanism is INAPPLICABLE on Mistral and the fact becomes STRICT — a cleaner read than Llama. If still multi-token, re-derive the proxy. Record the disposition either way.
5. Write `fact_verdicts` (Mistral-resolved) as the single-source record for Cell 8 + Cell 9 (`D-S217-2` cross-cell single-source contract).
6. Print `CELL6_TOKEN_VERIFY_OK` with the per-fact Mistral token-id list + verdict_class map + the freshly-built allowlist.

**Halt conditions:**
- `MULTI_TOKEN_FAIL` (a non-allowlisted fact tokenizes multi-token) → session-level HARD halt; add to allowlist AND verify first-token-proxy acceptable.
- A target_new fails to tokenize / produces an empty id list → halt (corpus/tokenizer incompatibility; investigate before edit).

---

### Cell 7 — Pre-edit baseline panel  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Capture the pre-edit probe panel against the current (just-loaded, unedited) Mistral state, using the Mistral-resolved token ids from Cell 6. Cross-checks Cell 5's producer baseline.

**Cell body (operator reading order):**
1. For each of the 38 probes, capture pre-edit: `top_1_token_id`, `p_top_1_pre`, and (consistency) `p_target_new_pre` using the **Mistral** target ids; (unmount) `p_target_true_pre`.
2. For any ALLOWLIST_FIRST_TOKEN_PROXY fact, capture first-token-proxy P (the Mistral first-token id from Cell 6).
3. Cross-check Cell 7 vs Cell 5 panel (both pre-edit on the same load → agree to FP16 noise). Print `CELL7_BASELINE_OK` + any probe whose Cell 7 vs Cell 5 drift exceeds `1e-5` (informational unless Cell 5 passed and Cell 7 diverges → within-session nondeterminism halt).

**Halt conditions:**
- Intra-session Cell 7 vs Cell 5 divergence `> 1e-5` → halt (within-session nondeterminism).

---

### Cell 8 — Fresh covariance computation (RE-AUTHORED — Mistral)  [Surface A → B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** RE-AUTHORED for Mistral. Compute the per-layer `mom2` covariance statistics for Mistral-7B-v0.3 from scratch over the canonical Wikipedia corpus, for the reference band `[4..8]`. Llama caches are INAPPLICABLE (different model, different keyed paths). Single most expensive cell (~45–75 min for the band; `OQ-S229-COV-TIME-1`).

**WHAT / WHY (operator-facing):** MEMIT's edit math needs a statistical summary (a covariance matrix) of how each target MLP layer behaves across a big text corpus — it uses this to make the edit while disturbing existing knowledge as little as possible. That summary is model-specific and must be computed once per model. This is the long cell; it runs unattended. Mistral's intermediate size matches the 8B model, so each layer's cache is roughly the 8B cache size (~0.8–1.0 GiB/layer), larger than the 3B caches.

**Cell body (operator reading order):**
1. Confirm `cov_cache_compute_required = True` from Cell 3.
2. Confirm P-5 (dataset loader), P-6 (`_t100_` filename segment), P-7 (`batch_tokens` dispatch) reported `true` from Cell 2 — fresh computation depends on all three. Corpus substrate is the post-P-5 `20231101.en` Wikipedia (`C-S25-15`).
3. For each layer in `[4, 5, 6, 7, 8]`, compute `mom2` over the Wikipedia corpus with `batch_tokens=100` (P-7 dispatch). Anticipated per-layer wall-time ~9–15 min (`OQ-S229-COV-TIME-1`); total ~45–75 min for the 5-layer band.
4. Write each cache to `/workspace/covariance_caches/mistral_7b_v0_3/.../wikipedia_stats/` with the canonical post-P-6 filename form (`_t100_` segment present; the path is keyed on the Mistral module name `model.layers.{N}.mlp.down_proj` and the `float32_mom2_t100_100000` envelope).
5. **`C-S229-3` provenance gate:** per-layer file size + checksum; per-layer cache anticipated ~0.8–1.0 GiB (Mistral `intermediate_size=14336` × float32 mom2 — matches 8B). Print `COV_COMPUTE_OK <layer> size=<bytes> sha=<checksum>` per layer. Total NV addition ~4–5 GiB for L4-L8.
6. **R1.3 absorption (post-compute verification gate):** re-list the cache directory; confirm five caches present with `_t100_` segment and non-zero size. Print `CELL8_COV_FRESH_OK 5/5`.

**Halt conditions:**
- P-5 / P-6 / P-7 not reported `true` → halt.
- A layer cache writes with zero size or absent `_t100_` segment → halt (filename construction regression; P-6/P-7 reconcile).
- `COV_COMPUTE_OK` count `< 5` → halt.
- Cov-compute OOM (less likely than edit-dispatch OOM given no activation retention; but Mistral weights are larger than 3B) → halt; route to FAIL-at-environment triage.

---

## Part V — BLOCK B: Dispatch + verdict

### Cell 9 — MEMIT joint-overlay edit dispatch  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Dispatch the MEMIT joint-overlay 5-fact edit at `[4..8]` and capture the post-edit panel. This is the cell that produces the class-changing read: the dispatch log's internal-vs-external split (`OQ-V12-T-BRANCH-4`).

**WHAT / WHY (operator-facing):** This is the actual edit. MEMIT will try to write all five "plays the instrument of X" facts into the model's weights at once. Watch two things in the log: (a) the INTERNAL objective — `compute_z` reports an average-probability per fact that it drives upward over 25 steps; on Llama this climbed tens of thousands of times. (b) the EXTERNAL probe — after the edit, does the model actually say the new instrument when asked? On every Llama model, (a) succeeded and (b) failed by orders of magnitude. The whole session hinges on whether that same split appears on Mistral.

**Cell body (operator reading order):**
1. Pre-edit probe panel (inherited from Cell 7 state).
2. **Capture the per-fact internal objective trace** from the dispatch log: `compute_z` start→end avg-prob per fact, and the gain ratio. This is the load-bearing diagnostic — record it explicitly, not just the final consistency number.
3. **MEMIT batched edit dispatch:** 5-fact joint overlay at `[4..8]`, consuming the fresh Mistral cov caches from Cell 8 (P-7 makes them edit-time visible). Log should show `Rewrite layer is 8` (top of band) and `Tying optimization objective to 31` — both correct for Mistral; if either reports a different value, the config (Cell 4) did not propagate — halt.
4. Post-edit probe panel capture (38 probes, Mistral ids).
5. **RE-EVALUATE gate at trial 0** (any ALLOWLIST_FIRST_TOKEN_PROXY fact from Cell 6): capture BOTH first-token-proxy P and full-sequence P; retire-or-ratify the proxy.
6. Print the post-edit consistency surface per fact: `p_target_new_post` + `top_1_post` for each consistency probe, AND the internal-vs-external summary (`internal_gain` vs `external_p_target_new` vs `top_1_moved`).

**Halt conditions:**
- Edit dispatch OOM → halt (FAIL at environment; PLAUSIBLE given tight Mistral headroom §2.3 — route to Cell 13 environment triage; mitigation is single-layer scope or precision relaxation).
- Cov-cache lookup miss at edit time (filename `_t100_` mismatch) → halt (P-7 dispatch regression).
- `Rewrite layer` ≠ 8 or `loss layer` ≠ 31 in the dispatch log → halt (Cell 4 config did not propagate).

---

### Cell 10 — Verdict surface aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the post-edit panel into the per-fact consistency / generalization / specificity verdict surface. Inherited UNCHANGED from the 3B Cell 10 semantics.

**Cell body (operator reading order):**
1. Per-fact consistency: all 3 cons probes PASS the predicate (`post-edit P(target_new) > 0.5 AND top-1 == target_new`, Mistral ids).
2. Per-fact generalization: all 3 gen probes PASS (`abs(p_top_1_post − p_top_1_pre) < 0.05`).
3. Specificity: 3 shared-spec probes PASS post-edit drift predicate.
4. Aggregate per `OQ-S212A-2` closure: `≥3 of 5 facts at ≥2/3 trials each` PASSES the consistency aggregate. (Single-dispatch Block B uses the trial-0 surface as the dry-run signal.)
5. **Record the internal-vs-external split explicitly** (the class-changing read): for each fact, `internal_gain` (compute_z start→end) × `external_p_target_new` × `top_1_moved?`. A reproduced split (huge internal gain, negligible external, top-1 unmoved) = signature reproduced = ceiling is base-decoder-LM-general.
6. Print `CELL10_VERDICT_SURFACE` with per-fact consistency PASS-rate + the internal-vs-external table.

**Halt conditions:** none (verdict surface is diagnostic input to Cell 13).

---

### Cell 11 — Copy-Unmount + post-unmount panel  [Surface B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Reverse the MEMIT joint-overlay edit via bit-exact Copy-Unmount and capture the post-unmount panel. APPLICABLE under MEMIT; a clean Mistral unmount is the **6th validated Copy-Unmount config and the first on a non-Llama architecture**.

**Cell body (operator reading order):**
1. Copy-Unmount: restore the L4-L8 `down_proj` weights from the pre-edit copy (bit-exact).
2. Post-unmount probe panel capture (38 probes, Mistral ids).
3. **IC-S23-4 HARD gate (per unmount probe):** `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4`. The unmount probe is the canonical prompt; `target_true` is Mistral's natural top-1 captured at Cell 5/7 (re-captured fresh on Mistral; NOT assumed to be ` his`/` her`).
4. Print `CELL11_UNMOUNT_OK drift_max=<value>` per fact. A `0.00e+00` result extends the Copy-Unmount validation to its 6th config (first non-Llama).

**Halt conditions:**
- IC-S23-4 unmount band exceeded (`drift ≥ 1e-4`) → halt (Copy-Unmount regression on Mistral; investigate the in-place restore at Mistral module paths).

---

### Cell 12 — Per-trial JSON write  [Surface B]

**Specialist:** state-consistency-theorist
**Purpose:** Persist the per-trial verdict record to NV. Inherited from the 3B Cell 12 with the proxy-annotation schema extension for any Mistral multi-token fact.

**Cell body (operator reading order):**
1. Write per-trial JSON to `/workspace/t3_mistral_7b_memit_*/` with: pre-edit / post-edit / post-unmount panels, per-fact verdict, the internal-vs-external trace, and (for any proxy fact) the `proxy_annotation` field (`verdict_class + primary_token_id + full_token_ids + proxy_disposition`).
2. Print `CELL12_JSON_WRITE_OK <path>`.

**Halt conditions:**
- Write failure (NV full / permission) → halt.

---

### Cell 13 — Verdict gate (3-route, EXTENDED with T.3-α cross-architecture routing)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + framework-spec-writer
**Purpose:** EXTENDED for T.3-α. The 3-route gate is preserved; routing consequences are extended with the cross-architecture matrix (§IX). Cell 13 reads the Cell 10 verdict surface + the internal-vs-external split + Cell 11 unmount status and routes Block C. **The PRIMARY read is the signature, not the bare consistency number** (per §6''.3: "A clean signature reproduction on Mistral/Qwen = ceiling is base-decoder-LM-general").

**Cell body (operator reading order):**
1. Read the Cell 10 per-fact consistency PASS-rate, the internal-vs-external table, and Cell 11 unmount status.
2. Apply the 3-route gate:
   - **Route A (HALT / single-confirmatory):** consistency surface shows the Llama-class miss pattern (post-edit `P(target_new)` orders of magnitude below 0.5 on all 5 facts) AND the internal-vs-external split is reproduced (huge internal gain, negligible external, top-1 unmoved). The dry-run reproduces the architectural-invariant pathology **on a non-Llama architecture**. Verdict trends toward `0/5 signature-reproduced` → **ceiling is base-decoder-LM-general (G)**. Block C is a single confirmatory pass per Route-A discipline.
   - **Route B (15-trial):** consistency clears or approaches the band for `≥3 of 5` facts. **This is the class-changing surprise** — Mistral CLEARS where Llama failed. Run the full Block C 15-trial loop to establish the PASS aggregate with replicates. Verdict trends toward `CLEAR` → **ceiling is Llama-family-specific (L)**; re-activates the within-regime per-layer sweep on Llama as the "what's different" probe.
   - **Route C (3-trial preview):** ambiguous surface (partial clearance; 1–2 facts near band). Run a reduced preview before committing.
3. Print `CELL13_ROUTE <A|B|C>` with rationale: per-fact PASS-rate, which facts cleared, AND the internal-vs-external verdict (`signature_reproduced: True|False`).

**`OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1` resolution gate.** Reconcile the runbook generalization predicate vs the `probe-set-v3.yaml` §126 predicate before the verdict is final (carried from the 3B arm; close at session entry).

**Halt conditions:**
- Route A → Block C runs at most one confirmatory pass.
- Calibration-criteria mismatch unresolved → halt ratification until reconciled.

---

## Part VI — BLOCK C: Confirmatory pass (verdict-conditional)

Block C is conditional on the Cell 13 route. It inherits the 3B Block C bodies declaratively. **Default expectation under Route-A discipline (D-S224-BLOCKC-SKIP-1):** a single confirmatory dispatch suffices for a `0/5` surface; the full 15-trial loop runs ONLY if Mistral approaches the band (Route B/C).

### Cell 14 — Trial matrix definition  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Define the trial matrix. 5 facts × {route-conditional replicates} (IC-S24-4 protocol).

**Cell body (operator reading order):**
1. Build `fact_memit_requests` referencing the same fact_id set as Cell 6 (`D-S217-2` SUBSET hard gate: Cell 6 verdict set ⊇ Cell 14 trial set ⊇ Mistral allowlist).
2. Route-conditional trial count:
   - Route A: ≤1 confirmatory replicate per fact (single confirmatory dispatch; Route-A discipline).
   - Route B: 3 replicates per fact (15 trials).
   - Route C: 1 replicate per fact (5 trials preview).
3. Print `CELL14_TRIAL_MATRIX <route> <n_trials>`.

**Halt conditions:**
- SUBSET gate fails → halt.

---

### Cell 15 — Trial loop body  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Execute the trial loop. Each trial: pre-edit panel → MEMIT edit (5-fact joint overlay at `[4..8]`) → post-edit panel → Copy-Unmount → post-unmount panel → IC-S23-4 HARD gate → per-trial JSON. Inherits the 3B Cell 15 body including the RE-EVALUATE gate at trial 0 for any proxy fact.

**Cell body (operator reading order):**
1. For each trial in the matrix:
   - pre-edit probe panel (Mistral ids).
   - MEMIT batched edit dispatch (inherited hparams; fresh Mistral cov caches); capture the internal objective trace each trial.
   - post-edit probe panel.
   - RE-EVALUATE gate at trial 0 (proxy facts only): both first-token-proxy and full-sequence P; retire-or-ratify.
   - Copy-Unmount + post-unmount panel + IC-S23-4 HARD gate (drift `< 1e-4`).
   - per-trial verdict + JSON write.
2. **STRICT-fact determinism:** for STRICT facts, the loop body is logically identical to the 3B inheritance; cross-session bit-exact determinism (D-S217-4 / D-S218-7 discipline) is preserved per Mistral Checkpoint #1.
3. Print `CELL15_TRIAL <id> verdict=<...> internal_gain=<...> external_p=<...>` per trial.

**Halt conditions:**
- IC-S23-4 unmount band exceeded at any trial → halt.
- Edit dispatch OOM at any trial → halt (FAIL at environment).

---

### Cell 16 — Per-fact verdict aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate per-trial verdicts into per-fact verdicts. Inherited from the 3B Cell 16 verbatim.

**Cell body (operator reading order):**
1. Per-fact consistency PASS-rate across replicates.
2. Aggregate per `OQ-S212A-2` closure: `≥3 of 5` facts at `≥2/3` trials each PASSES the consistency aggregate.
3. Print `CELL16_AGGREGATE consistency_pass_facts=<n>/5 signature_reproduced=<bool>`.

**Halt conditions:** none.

---

### Cell 17 — Generalization + specificity + unmount aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the non-consistency surfaces. Inherited from the 3B Cell 17 verbatim.

**Cell body (operator reading order):**
1. Generalization mean drift across gen probes.
2. Specificity mean drift across shared-spec probes (post-edit + post-unmount).
3. Unmount HARD-gate status (all trials must pass IC-S23-4).
4. Print `CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>`.

**Halt conditions:**
- Any trial's unmount HARD-gate FAIL → already halted at Cell 15; surfaced here for the record.

---

## Part VII — BLOCK-END

### Cell 18 — Covariance-cache integrity gate (post-compute)  [Surface A]

**Specialist:** state-consistency-theorist + memit-specialist
**Purpose:** Verify the fresh Mistral cov caches written at Cell 8 are intact and bit-exact-preserved across the session (MEMIT does not modify cov caches; post-session checksums must match Cell 8).

**Cell body (operator reading order):**
1. Re-checksum each `mistral_7b_v0_3` cov cache.
2. Compare against the Cell 8 `C-S229-3` provenance record (per-layer size + checksum).
3. Print `CELL18_COV_INTEGRITY_OK 5/5 sha_match=True` or the mismatch list.

**Halt conditions:**
- Checksum mismatch → halt (cov cache corrupted mid-session).

---

### Cell 19 — NV inventory  [Surface A]

**Specialist:** state-consistency-theorist
**Purpose:** Inventory the NV outputs produced this session.

**Cell body (operator reading order):**
1. List session outputs: `/workspace/t3_mistral_7b_memit_*/`, fresh Mistral cov caches, engine snapshot, per-trial JSONs, `mistral_7b_v0_3_baselines.json`, session log.
2. Report NV free space (cov caches added ~4–5 GiB + Mistral model cache ~15 GiB if pulled to NV; confirm against 300 GiB capacity).
3. Print `CELL19_NV_INVENTORY_OK` with the output manifest.

**Halt conditions:**
- NV near-full → halt; prune working tier per two-tier discipline (D-S210-6).

---

### Cell 20 — Reproducibility manifest extension  [Surface A → B]

**Specialist:** state-consistency-theorist + memit-specialist
**Purpose:** Extend the reproducibility manifest with the S2.29 T.3-α-MISTRAL entry.

**Cell body (operator reading order):**
1. Append the S2.29 entry to `reproducibility_manifest.json`: Mistral model SHA, MEMIT engine SHA (`C-S229-1`), patch-state dict (Cell 2, incl. re-derived Pad-Token), cov-cache provenance (Cell 8), Checkpoint #1 drift (Cell 5), Mistral token-id resolution map (Cell 6), verdict aggregate (Cell 16/17), Cell 13 route, `signature_reproduced` flag.
2. Record the engine source snapshot path (`C-S229-2`).
3. Print `CELL20_MANIFEST_OK <entry_id>`.

**Halt conditions:**
- Manifest write failure → halt.

---

## Part VIII — Halt-condition cross-index

| Cell | Condition | Class | Action |
|---|---|---|---|
| 0 | GPU not RTX 4090 / NV absent / dep install fail (esp. sentencepiece) | Session HARD | halt; re-scope |
| 1 | Clone fail / byte-identity mismatch / Mistral license not accepted | Session HARD | halt; reconcile |
| 1.5 | Module-path template unresolved / down_proj shape wrong / lm_head tied-when-expected-untied | Session HARD (paths) / BRANCH (tied) | halt and re-derive module paths; OR branch to tied-embedding adaptation |
| 2 | Partial-marker patch / P-4 not at 4 sites / Pad-Token ≠ 2 / required-not-applied | Session HARD | halt; reconcile §3.8.7 / §3.2 |
| 3 | Present-but-corrupt cov cache | Session HARD | halt |
| 4 | Layer bound assertion fail / lm_head_module unverified | Session HARD | halt; config error |
| 5 | Within-session determinism self-check fail / model load OOM | Session HARD | halt; nondeterminism or environment |
| 6 | MULTI_TOKEN_FAIL (non-allowlisted) / target fails to tokenize | Session HARD | halt; allowlist + proxy or investigate |
| 7 | Cell 7 vs Cell 5 divergence > 1e-5 | Session HARD | halt; within-session nondeterminism |
| 8 | P-5/6/7 not true / zero-size cache / count < 5 / cov OOM | Session HARD | halt; prerequisites or environment |
| 9 | Edit OOM / cov lookup miss / Rewrite layer ≠ 8 or loss layer ≠ 31 | Session HARD | halt; environment, P-7 regression, or config non-propagation |
| 11 / 15 | IC-S23-4 unmount band exceeded | Trial HARD | halt; Copy-Unmount regression on Mistral |
| 13 | Calibration-criteria mismatch unresolved | Verdict HARD | halt ratification until reconciled |
| 14 | SUBSET gate fail | Session HARD | halt |
| 18 | Cov-cache checksum mismatch | Session HARD | halt; corruption |
| 19 | NV near-full | Session HARD | halt; prune working tier |
| 20 | Manifest write fail | Session HARD | halt |

---

## Part IX — Forward Routing Matrix — S2.29 Cell 13 → S2.30

```
═══════════════════════════════════════════════════════════════════
  S2.29 Cell 13 / Cell 16 verdict → S2.30 routing:

  CLEAR (consistency aggregate PASSES; ≥3 of 5 facts at ≥2/3 trials;
        Mistral clears where every Llama model failed):
    └── CLASS-CHANGING SURPRISE. Ceiling is LLAMA-FAMILY-SPECIFIC (L).
        framework_finding v1.4 amendment scope: the nine-axis ceiling
        is a Llama-family-representation-geometry property, NOT a
        base-decoder-LM-general property. The "LLM-as-database" write
        layer is editable on Mistral — re-opens the search for an
        editable base model.
    └── S2.30 = within-regime per-layer sweep on Llama RE-ACTIVATED
        (D-V12-T-BRANCH-3 conditional re-activation) as the
        "what's different between Llama and Mistral" probe.
        (Low prior given 9 axes, but the one outcome that re-opens
        the design space.)

  0/5 SIGNATURE-REPRODUCED (edit dispatches + runs; internal-vs-external
        split reproduced — huge internal gain, negligible external,
        top-1 unmoved — on a non-Llama architecture):
    └── Ceiling is BASE-DECODER-LM-GENERAL (G). framework_finding v1.4
        amendment scope: Axis 10 (first cross-architecture axis);
        promotes the ceiling from "config-independent MEMIT-on-base-
        Llama" to "config-independent MEMIT-on-base-decoder-LM" —
        the portable, framework-level write-layer result.
    └── S2.30 = T.3-β QWEN authoring + execution (second non-Llama
        family; near-decisive for G; reuses this T.3 scaffold).

  FAIL-at-environment (cov-cache compute OR edit dispatch OOM —
        plausible given tight Mistral headroom §2.3 ~19–21 GiB peak):
    └── NOT a scientific verdict. Mitigation in priority order:
        (1) single-layer scope (L5 only — EasyEdit ROME site);
        (2) fp16 cov relaxation; (3) deeper-arm: gradient-checkpointed
        dispatch. Re-attempt before any model-family conclusion.
    └── S2.30 = halt for triage; re-attempt T.3-α with mitigation.
═══════════════════════════════════════════════════════════════════
```

The three outcomes are mutually exclusive and exhaustive at the Cell 13 gate. Mapping from Cell 13 route to verdict class: Route A (signature reproduced) → `0/5 SIGNATURE-REPRODUCED` → (G) → Qwen arm; Route B PASS-aggregate → `CLEAR` → (L) → per-layer sweep re-activated; Route B/C non-PASS → `0/5 SIGNATURE-REPRODUCED`; any OOM at Cell 8/9/15 → `FAIL-at-environment`.

**Decision matrix restated (S2.29 kickoff):** Mistral `0/5` + signature reproduced → ceiling is base-decoder-LM-general (not Llama-specific) → Qwen-7B confirmation arm. Mistral CLEARS → ceiling is Llama-family-specific → within-regime per-layer sweep re-activated as the "what's different" probe.

---

## Part X — Open Questions

### 10.1 OQs anticipated to OPEN at S2.29

| ID | Statement | Status | Closes when |
|---|---|---|---|
| OQ-S229-1 | `mom2_update_weight=15000` (Llama PASS value) calibration on Mistral: same value, OR requires re-tuning at a different architecture? PROVISIONAL inheritance; re-tuning is out of scope for the single-variable port | Open | deeper-arm only (not this session) |
| OQ-S229-COV-TIME-1 | Mistral-7B layer_stats Wikipedia covariance per-layer wall-time on RTX 4090 fp16 (anticipates ~9–15 min/layer; informational anchor) | Open | Cell 8 execution |
| OQ-S229-VRAM-1 | Joint-overlay 5-fact dispatch peak VRAM on Mistral-7B at canonical hparams: empirical confirmation of §2.3 projection (~19–21 GiB; TIGHTEST headroom of any arm) | Open | Cell 9/15 execution |
| OQ-S229-HARP-1 | Does `harp` tokenize single-token on Mistral's SentencePiece vocab (cleaner STRICT read) or multi-token (proxy required)? | Open | Cell 6 token re-resolution |
| OQ-S229-MISTRAL-TOP1-1 | Mistral's natural top-1 at `{subject} plays the instrument of` — same ` his`/` her` class as Llama, or different? (affects target_true / unmount probe) | Open | Cell 5 baseline capture |

### 10.2 OQs carried forward / absorbed

| ID | Disposition at this runbook |
|---|---|
| OQ-V12-T-BRANCH-1 | RESOLVED at Cell 1 — Mistral-7B-v0.3 base, HF revision SHA pinned at session entry |
| OQ-V12-T-BRANCH-2 | RESOLVED at Cell 1.5 — architecture-structural field set derived via `named_parameters()` (untied lm_head; module paths verified; n_layers=32 → v_loss_layer=31) |
| OQ-V12-T-BRANCH-3 | RESOLVED at Cell 4 — reference band `[4..8]` adopted (EasyEdit MEMIT critical-range; Axis-9-validated equivalent); no re-sweep |
| OQ-V12-T-BRANCH-4 | PRIMARY READ this session — internal-vs-external signature reproduction (Cell 9/10/13); the class-changing question |
| OQ-V12-T-BRANCH-5 | CONDITIONAL — resolved only on a surprising CLEAR (re-activates per-layer sweep + dispatch-mode arms) |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | CARRIED — resolve before Cell 10/13 verdict (§Cell 13 gate) |
| OQ-S222-CELL1-2 / CELL0-DEPS-1 / SURFACE-LABELING-1 / CELL-EXEC-VERIFICATION-1 | ABSORBED (Cell 1 snapshot / Cell 0 explicit install / per-cell surface annotation / acceptance strings) |

---

## Part XI — Decision + Constraint Registry

### 11.1 Decisions (this runbook)

| ID | Statement |
|---|---|
| D-S229-Q1-1 | Runbook structural inheritance from `t1_alt_model_3b_memit_runbook v0.1` with §1.4 cross-architecture substitutions; corpus / probe-strings / trial protocol / acceptance bands held verbatim |
| D-S229-Q2-1 | Cell 5 PRODUCES Mistral Checkpoint #1 (fresh determinism chain; no prior baseline to consume — unlike the 3B Cell 5 which consumed a GRACE baseline) |
| D-S229-Q3-1 | Reference band `[4,5,6,7,8]` adopted from EasyEdit MEMIT critical-range (OQ-V12-T-BRANCH-3); Axis-9 establishes band non-load-bearing → interpretively clean |
| D-S229-Q4-1 | Cell 8 RE-AUTHORED — fresh Mistral cov computation at `[4..8]`; ~45–75 min; ~4–5 GiB NV |
| D-S229-LMHEAD-1 | `lm_head_module = 'lm_head'` (UNTIED; reverts the 3B tied `model.embed_tokens` override to the 8B-canonical form); verified untied at Cell 1.5 (`C-S229-LMHEAD-1`); the INVERSE of the 3B tied-embedding adaptation |
| D-S229-PADTOKEN-1 | Pad-Token RE-DERIVED to `eos_token_id=2` per Mistral convention (EasyEdit handling); the one patch with changed content vs the Llama canonical |
| D-S229-PATCH-INHERITANCE-1 | All MEMIT patches per `memit-patches v2.5` inherited; P-4 (Mistral=Required) is the structural reason the engine runs unchanged; engine source byte-identical to Llama baseline (verified Cell 1.0) |
| D-S229-TOKEN-RERESOLVE-1 | ALL probe + target token IDs re-resolved against the Mistral tokenizer (Cell 6); the Llama allowlist `{cfb-v3-004}` NOT inherited — Mistral allowlist built fresh from Mistral classification |
| D-S229-BLOCKC-SKIP-1 | Route-A discipline (single confirmatory dispatch for a 0/5 surface) inherited (D-S224-BLOCKC-SKIP-1); full 15-trial only on Route B/C |

### 11.2 Constraints (this runbook)

| ID | Statement |
|---|---|
| C-S229-1 | MEMIT engine SHA pinning at Cell 1 entry; documented in Cell 20 manifest |
| C-S229-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` post-Cell-1 |
| C-S229-3 | Cov-cache fresh-computation gate at Cell 8: per-layer file size + checksum per S2.15-D2 PROVENANCE protocol |
| C-S229-4 | Layer-set bound assertion at Cell 4: all of `[4..8]` within `0 ≤ idx < n_layer = 32` |
| C-S229-5 | Per-cell explicit Surface annotation (A vs B) |
| C-S229-LMHEAD-1 | `lm_head.weight` PRESENT (untied) verified at Cell 1.5 via `named_parameters()` before `lm_head_module='lm_head'` is set (the C-S227-3 discipline, inverted for the untied case) |
| C-S229-PADTOKEN-1 | `tokenizer.pad_token_id == tokenizer.eos_token_id == 2` asserted at Cell 2 |
| C-S229-MODULE-1 | All four MEMIT module-path templates (`rewrite`/`mlp`/`layer`/`v_loss`) resolve to real named modules on `MistralForCausalLM`, asserted at Cell 1.5 before any config build |

### 11.3 Inherited carry-forward anchors (NOT re-numbered)

| Anchor | Source | Disposition |
|---|---|---|
| IC-S23-4 | unmount band HARD gate | APPLICABLE at Cell 11 / Cell 15 (6th validated config if 0.00e+00; first non-Llama) |
| IC-S24-4 | 5×3 trial protocol | APPLICABLE at Cell 14 (Route-conditional) |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} subset | APPLICABLE (verdict integrity binding) |
| D-S217-2 | Cell 6 ↔ Cell 14 single-source SUBSET | APPLICABLE at Cell 6 / Cell 14 |
| D-S217-4 / D-S218-7 | cross-session bit-exact determinism | APPLICABLE (STRICT facts) at Cell 15 |
| D-V12-MULTITOKEN-1 | MULTI_TOKEN_ALLOWLIST absorption | APPLICABLE at Cell 6 / 7 / 9 / 15 (Mistral-rebuilt allowlist) |
| C-S25-15 | substrate-shift (`20231101.en`) | APPLICABLE at Cell 8 |
| C-S26-1 / C-S26-2 | cache-dispatch symmetry (P-7) | APPLICABLE at Cell 8 / 9 |
| D-S227-HPARAM-IDIOM-1 | scale-variant config idiom | APPLICABLE at Cell 4 (generalized to cross-architecture) |
| D-S227-LMHEAD-1 | tied-embedding dispatch-failure discipline | APPLICABLE at Cell 1.5 as the INVERSE check (untied confirmed) |

---

## Part XII — Non-Goals

This runbook v0.1 does NOT:

1. **Re-tune MEMIT hyperparameters for Mistral.** The Llama-validated tuning knobs are inherited verbatim (`D-S229-Q1-1`); re-tuning would conflate architecture with hparam and is a deeper arm (`OQ-S229-1`), not this single-variable port.
2. **Re-sweep the layer band.** Axis 9 established band non-load-bearing; the EasyEdit reference `[4..8]` is adopted (`D-S229-Q3-1`).
3. **Modify `memit-patches-canonical v2.5`.** All patches inherited; Pad-Token re-derivation is a per-variant application of the existing patch (§4.4 anticipated branch), not a canonical modification.
4. **Modify `t1_alt_model_3b_memit_runbook v0.1` or `stage_1_sect_runbook v1.7`.** This is a NEW sibling runbook.
5. **Author the v1.4 framework_finding amendment.** v1.4 is a separate deliverable conditional on the S2.29 verdict.
6. **Select or author the Qwen-7B arm.** Deferred to S2.30 routing IF the verdict is `0/5 signature-reproduced` (G).
7. **Convene the Council.** Proven port pattern, not an open design problem (per kickoff specialist routing — no Council).
8. **Consume GRACE-side artifacts.** INAPPLICABLE for MEMIT-side authoring.
9. **Author runtime implementation code.** Cell bodies are operator-reading-order specifications + acceptance-string contracts; code execution is pod-side.

---

## Part XIII — Reference Appendices

### 13.1 Cell → Surface → Specialist index

| Cell | Surface | Primary specialist | Delta class |
|---|---|---|---|
| 0 | A | memit + state-consistency | verbatim + dep-install (sentencepiece) |
| 1 | A | memit | inheritance (clone + snapshot + SHA pin) |
| 1.5 | B | memit | RE-AUTHORED (Mistral module introspect — highest risk) |
| 2 | A → B | memit | inheritance + Pad-Token re-derivation |
| 3 | A | memit + state-consistency | APPLICABLE (cov entry gate) |
| 4 | B | memit | RE-AUTHORED (structural fields + reference band) |
| 5 | B | validation + memit + state-consistency | INVERTED (producer; Checkpoint #1) |
| 6 | B | validation + memit | RE-AUTHORED (token re-resolution) |
| 7 | B | validation + memit | inheritance |
| 8 | A → B | memit + state-consistency | RE-AUTHORED (fresh Mistral cov) |
| 9 | B | validation + memit + state-consistency | inheritance (internal-vs-external trace foregrounded) |
| 10 | B | validation | inheritance (+ signature table) |
| 11 | B | memit + state-consistency | inheritance (6th Copy-Unmount config) |
| 12 | B | state-consistency | inheritance |
| 13 | B | validation + memit + framework-spec | EXTENDED (cross-architecture routing) |
| 14 | B | validation + memit | inheritance |
| 15 | B | validation + memit + state-consistency | declarative |
| 16 | B | validation | inheritance |
| 17 | B | validation | inheritance |
| 18 | A | state-consistency + memit | APPLICABLE (cov integrity) |
| 19 | A | state-consistency | inheritance |
| 20 | A → B | state-consistency + memit | inheritance |

### 13.2 Per-fact target reference (token IDs RE-RESOLVED at Cell 6 against Mistral tokenizer)

| Fact | Subject | target_new | Llama-3.2-3B id (REFERENCE ONLY — NOT valid on Mistral) | Mistral id | Class |
|---|---|---|---|---|---|
| cfb-v3-001 | Bo Jackson | guitar | `[17418]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-002 | Tiger Woods | piano | `[27374]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-003 | Deion Sanders | violin | `[63137]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-004 | Hakeem Olajuwon | harp | `[4960, 79]` (multi on Llama) | resolve @ Cell 6 (OQ-S229-HARP-1) | resolve @ Cell 6 |
| cfb-v3-005 | Lindsey Vonn | flute | `[96812]` | resolve @ Cell 6 | resolve @ Cell 6 |

Canonical prompt form: `{subject} plays the instrument of` (model-agnostic string; held verbatim from cfb-v3). The Llama ids are shown ONLY to document that they are deliberately discarded — the Mistral ids are the live values, resolved at Cell 6. This is the only table in the runbook with execution-resolved literals, by necessity (a tokenizer query); the resolution logic and gates are fully specified at Cell 6.

### 13.3 Architecture-structural field derivation (the port adaptations, fully derived at authoring)

| Field | Source of value | Mistral-7B-v0.3 value | Derivation |
|---|---|---|---|
| `n_layers` | model config | 32 | HF config `num_hidden_layers` |
| `v_loss_layer` | n_layers − 1 | 31 | structural (same as 8B by coincidence) |
| `tie_word_embeddings` | model config | False | HF config; → lm_head untied |
| `lm_head_module` | tie check | `lm_head` | untied → 8B-canonical form (NOT 3B tied override) |
| `hidden_size` | model config | 4096 | = 8B |
| `intermediate_size` | model config | 14336 | = 8B |
| `rewrite_module_tmp` | named_parameters | `model.layers.{}.mlp.down_proj` | verified @ Cell 1.5 |
| `mlp_module_tmp` | named_parameters | `model.layers.{}.mlp` | verified @ Cell 1.5 |
| `layer_module_tmp` | named_parameters | `model.layers.{}` | verified @ Cell 1.5 |
| layer band | EasyEdit reference | `[4,5,6,7,8]` | arXiv 2308.07269 Table 4; OQ-V12-T-BRANCH-3 |
| `pad_token_id` | Mistral convention | 2 (= eos) | EasyEdit Mistral handling; re-derived Pad-Token |
| `vocab_size` | model config | 32768 | → all token IDs re-resolved (Cell 6) |
| P-4 applicability | family | Required | `memit-patches v2.5` §3.5.2 (Mistral listed Required) |

### 13.4 Acceptance-string index (for execution verification)

```
CELL0_DEPS_OK <transformers_version> <accelerate_version> sentencepiece=<version>
MISTRAL_MODEL_SHA <sha>
MEMIT_ENGINE_SHA <sha>
ENGINE_SNAPSHOT_OK <path>
MISTRAL_MODULE_INTROSPECT_OK <4 paths> down_proj_shape=[4096,14336] lm_head_untied=True
PATCH <id> APPLIED   (per patch; P-4 ×4 sites)
PADTOKEN_MISTRAL_OK pad=eos=2
CELL2_PATCH_STATE_OK <patches_applied dict>
COV_CACHE_MISTRAL_ABSENT | COV_CACHE_MISTRAL_PRESENT — integrity {OK|MISMATCH}
LAYER_BOUND_OK [4..8] < 32
CELL4_HPARAM_OK <config + INHERIT/OVERRIDE map>
CHECKPOINT_1_MISTRAL_OK drift_max=<value>
CELL5_BASELINE_PRODUCED <path>
CELL6_TOKEN_VERIFY_OK <per-fact Mistral ids + verdict_class map + allowlist>
CELL7_BASELINE_OK
COV_COMPUTE_OK <layer> size=<bytes> sha=<checksum>   (per layer)
CELL8_COV_FRESH_OK 5/5
CELL10_VERDICT_SURFACE <per-fact pass-rate + internal-vs-external table>
CELL11_UNMOUNT_OK drift_max=<value>   (per fact)
CELL12_JSON_WRITE_OK <path>
CELL13_ROUTE <A|B|C> signature_reproduced=<bool>
CELL14_TRIAL_MATRIX <route> <n_trials>
CELL15_TRIAL <id> verdict=<...> internal_gain=<...> external_p=<...>   (per trial)
CELL16_AGGREGATE consistency_pass_facts=<n>/5 signature_reproduced=<bool>
CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>
CELL18_COV_INTEGRITY_OK 5/5 sha_match=True
CELL19_NV_INVENTORY_OK <manifest>
CELL20_MANIFEST_OK <entry_id>
```

---

**Runbook v0.1 status:** DECLARATIVE — READY FOR S2.29 EXECUTION
**Persistence:** `/mnt/user-data/outputs/t3_mistral_7b_memit_runbook_v0_1.md`

*End of t3_mistral_7b_memit_runbook v0.1 — MEMIT on Mistral-7B-v0.3 base × cfb-v3 × canonical hparams × EasyEdit reference band; first cross-architecture axis (T.3-α); single-variable architecture port; internal-vs-external signature reproduction as the primary read (OQ-V12-T-BRANCH-4, the class-changing question); single confirmatory dispatch (Route-A discipline).*
