# T.3-β-QWEN Runbook — Qwen2.5-7B (base) under MEMIT — v0.1

**Status:** DECLARATIVE (authored S2.30 micro-pass; pod-side execution same session)
**Iteration:** v0.1 first authoring (NEW runbook; not a revision)
**Engine:** MEMIT (canonical engine per `memit-patches-canonical v2.5`)
**Target model:** `Qwen/Qwen2.5-7B` (base, NOT Instruct; fp16)
**Axis:** Axis 10 **confirmation arm** — second cross-architecture family (T.3-β; confirmation, NOT class-change candidate, per `t_branch v1.3` §4'''.2)
**Direct structural template:** `t3_mistral_7b_memit_runbook v0.1` (closest sibling; cross-architecture port pattern proven at S2.29)
**Basis:** S2.30 kickoff; S2.29 close carry-forward; `framework_finding v1.4` §2.4 cross-architecture idiom + §4 Qwen routing; `t_branch v1.3` §6''' methodology lock; `session_2_29_summary_block` §10 entry preconditions
**Specialist provenance:** memit-specialist (primary; engine + patch + cov-cache + dispatch + the architecture-port adaptations), framework-spec-writer (inheritance map + routing matrix + integrity), state-consistency-theorist (light; determinism chain bootstrap + NV inventory + manifest)
**Persistence:** `/mnt/user-data/outputs/t3_qwen_7b_memit_runbook_v0_1.md`

---

## Part 0 — Orientation

### 0.1 What this runbook is

This runbook executes **T.3-β-QWEN**: running the MEMIT write engine against `Qwen/Qwen2.5-7B` (the base, non-instruct model) at the canonical hyperparameters and corpus that produced the ten-axis architectural-invariant ceiling on the Llama family and Mistral. It is a NEW runbook authored by structural inheritance from `t3_mistral_7b_memit_runbook v0.1` (the closest sibling — same MEMIT engine, same corpus, same trial protocol, same cross-architecture port discipline, model swapped from Mistral to Qwen), with the base model swapped to a **second, more architecturally distinct non-Llama family (Qwen)** and the covariance caches re-authored from scratch.

The `β` suffix marks the **second cross-architecture arm** and, unlike the `α` (Mistral) arm, it is a **confirmation arm, not a class-change candidate**. T.3-α already resolved the class-changing question (OQ-V12-T-BRANCH-4): the ceiling reproduced on Mistral, promoting the finding from config-independent-MEMIT-on-base-**Llama** (L) to config-independent-MEMIT-on-base-**decoder-LM** (G). T.3-β tests the precise residual skeptic's objection: Mistral shares Llama-2's architectural lineage (RMSNorm + RoPE + gated MLP + GQA decoder block), so a critic could read Axis 10 as "generalizes within the Llama-lineage decoder shape." Qwen is the most architecturally distinct 7B base decoder family available. A `0/5` signature reproduction on Qwen converts "generalizes from Llama to a Llama-lineage cousin" into "generalizes across architecturally distinct base decoder LM families" — the strongest obtainable form of G.

### 0.2 The one question this runbook answers, for the operator learning the system

A useful mental model carried from the Mistral runbook: MEMIT optimizes an internal vector (the `z` / `v` vector) to drive a new fact into a band of MLP layers. On every base decoder LM tested so far — Llama-8B, Llama-3B, and Mistral-7B, across both contested layer bands — that optimizer made enormous *internal* progress (hundreds to thousands of times improvement in the quantity it minimizes) while the externally-observable consistency probe — "does the model now say the new fact when asked?" — registered a multi-order-of-magnitude miss against the 0.5 acceptance band. Ten independent perturbations all reproduced this **internal-vs-external split**. That split is the ceiling's defining signature.

T.3-β asks one question: **does that signature reproduce on a non-Llama-LINEAGE architecture?** The answer determines how broad G is:

- **(G confirmed, near-decisive)** — if Qwen reproduces the `0/5` with the same internal-vs-external split, the ceiling holds across architecturally-distinct base decoder LM families, not merely within the Llama lineage. This is the portable, framework-level result about the write layer at its strongest. External-validity arms (Instruct models, KnowEdit benchmark corpus) then become the frontier — none of which can change the finding's *class*, only its breadth.
- **(G narrows to Llama-lineage)** — if Qwen CLEARS (consistency PASS where Llama and Mistral failed), the ceiling is a property of the Llama-lineage decoder shape, not of base decoder LMs generally. The architecture-geometry question re-opens, and the within-regime per-layer sweep (deprioritized since S2.27) conditionally re-activates as the "what's different between the architectures" probe. Low prior given ten axes, but this is the one outcome that re-opens the design space.

This is **OQ-V13-T-BRANCH-3**, the G-confirmation read. The primary instrument for it is the dispatch log's internal-vs-external split (§Cell 9 / §Cell 13), not the bare consistency number.

### 0.3 Why Qwen is the MOST DISTINCT port of the three cross-architecture/scale arms

A load-bearing fact for interpreting this arm. The Mistral port (Axis 10) was structurally *near* the 8B canonical — same hidden size (4096), same intermediate size (14336), same layer count (32), untied embeddings — so the only genuine deltas were the tokenizer and the pad convention. **Qwen is the opposite: it differs from the Llama/Mistral canonical on nearly every structural field.** This is exactly what makes it the near-decisive confirmation:

1. **Different decoder dimensions.** Qwen2.5-7B has `hidden_size=3584` (vs 4096 on 8B/Mistral, 3072 on 3B) and `intermediate_size=18944` (vs 14336 on 8B/Mistral, 8192 on 3B). The `down_proj` weight shape is therefore `[3584, 18944]` — a shape **not seen on any prior arm**. The MEMIT covariance caches are keyed on this shape and are larger per-layer than any prior arm (`18944 × float32` second-moment).
2. **Different layer count.** Qwen2.5-7B has `num_hidden_layers=28` (vs 32 on 8B/Mistral, 28 on 3B). `v_loss_layer = n−1 = 27` — coincidentally the **same value as the 3B arm**, but for an unrelated reason (3B had 28 layers too). This is a coincidence to note, not a shared property.
3. **Untied embeddings (like 8B/Mistral, unlike 3B).** Qwen2.5-7B has `tie_word_embeddings=false`; `lm_head.weight` IS a named parameter. `lm_head_module='lm_head'` — the 8B/Mistral-canonical form, NOT the 3B tied `model.embed_tokens` override. (Note: the *smaller* Qwen2.5 variants — 0.5B/1.5B/3B — use tied embeddings; the 7B is untied. Cell 1.5 verifies this empirically rather than assuming it.)
4. **Different, larger tokenizer.** Qwen uses a BPE tokenizer with `vocab_size=152064` (vs Llama-3's 128256 BPE, Mistral's 32768 SentencePiece). Entirely disjoint vocabulary; **every probe token ID and target token ID must be re-resolved from scratch** (Cell 6). Qwen's larger vocab makes single-token targets *more* likely than on Mistral's 32k vocab — a cleaner read is plausible (re-classify fresh; OQ-S230-QWEN-FRAG-1).
5. **Different pad/eos convention.** Qwen base uses `<|endoftext|>` (id `151643`) as both bos and the natural pad token, with `<|im_end|>` (id `151645`) as eos. The Pad-Token patch re-derives to Qwen's convention (§3.2) — the one patch with model-specific content.

The net effect: the Qwen port has MORE hparam-structural overrides than the Mistral port (dims differ, layer count differs) AND a different tokenizer surface. The single-variable discipline is preserved exactly as on Mistral — **zero tuning-knob changes** — so that the only differences from the config that produced all ten prior axes are the architecture-forced structural overrides and the tokenizer re-resolution.

### 0.4 Three outcomes, and how the verdict routes

Three outcomes are possible at the Cell 13 gate, and the verdict routes the next session (see §IX):

- **CLEAR (PASS)** — Qwen clears the consistency band where Llama (×3 configs) and Mistral could not. The ceiling **narrows from G to Llama-lineage decoder LMs**. Major reframe: the within-regime per-layer sweep re-activates as the "what's different between Llama-lineage and Qwen" probe; the architecture-geometry question re-opens. Low prior given ten axes, but the one outcome that re-opens the design space.
- **0/5 with signature reproduced (FAIL-with-installation)** — the edit dispatches and runs; the same internal-vs-external split reproduces (`compute_z` drives the internal objective hard; the external probe registers nothing; top-1 never becomes the target). The ceiling is confirmed **G near-decisive** — it holds across architecturally-distinct base decoder LM families. Routes to the external-validity frontier (Instruct, KnowEdit).
- **FAIL-at-environment** — the cov-cache compute or edit dispatch hits a resource wall before producing a verdict. Qwen2.5-7B fp16 ≈ 15.2 GiB weights; projected ~20–22 GiB peak under MEMIT vs the 24 GiB ceiling — tightest headroom of any arm (the large `intermediate_size=18944` drives both the cov workspace and the edit-time activations). Routes to triage (precision relaxation or scope reduction).

### 0.5 Two-surface execution discipline (carried verbatim from S2.24 §9, via the Mistral arm)

Every cell is annotated with its execution surface:

- **Surface A** — pod terminal (SSH). OS-level commands, repo clone, dependency install, patch application, file-system operations, covariance computation launches.
- **Surface B** — JupyterLab notebook on the pod. Model load, probe-panel capture, MEMIT edit dispatch, verdict computation, JSON writes.

Cells spanning both are annotated `[Surface A → B]` with the handoff marked inline. Operator-guidance register (S2.24 §9, carried verbatim through S2.29 §9): zero-ML-background, one cell at a time; each cell states WHAT it does, WHY, and the expected healthy output BEFORE the operator runs it; a null result (`0/5` with signature) is framed as **signal, not failure** — it is the load-bearing scientific outcome this session is built to detect. Claude makes all calls and proceeds; only irreversible operations (the model pull + license accept, the cov compute launch, any NV-destructive op) are surfaced for explicit confirmation before dispatch.

### 0.6 Block structure

```
═══════════════════════════════════════════════════════════════════
  BLOCK A — Pre-flight (Cells 0–8)
     Pod bring-up + deps, engine clone + snapshot, Qwen module
     introspection (HIGHEST-RISK port check; new down_proj shape),
     patch application (P-4 Required; Pad-Token RE-DERIVED to Qwen
     convention), cov-cache entry gate, MEMIT hparam config (Qwen
     structural fields + EasyEdit reference band), baseline PRODUCE
     (Checkpoint #1 on Qwen — fresh determinism chain), token
     re-resolution + allowlist, pre-edit panel, FRESH covariance
     computation

  BLOCK B — Dispatch + verdict (Cells 9–13)
     MEMIT joint-overlay edit at the reference band, verdict surface,
     Copy-Unmount, per-trial JSON, Cell 13 3-route gate (EXTENDED
     with T.3-β cross-architecture-confirmation routing matrix)

  BLOCK C — Confirmatory pass (Cells 14–17) [verdict-conditional]
     Route-A discipline: single confirmatory dispatch when 0/5 is
     established; Route B 15-trial only if Qwen approaches the band

  BLOCK-END (Cells 18–20)
     Cov-cache integrity gate, NV inventory, manifest extension
═══════════════════════════════════════════════════════════════════
```

### 0.7 Engine-class note for the operator

MEMIT on Qwen behaves identically in mechanism to MEMIT on Llama and Mistral — the engine code is byte-identical; only the model it operates on changes. Two engine-class properties carry forward unchanged:

1. **MEMIT consumes covariance caches.** MEMIT's least-squares update needs a per-layer second-moment statistic (`mom2`) computed over a Wikipedia corpus. The Llama and Mistral caches on NV are keyed on their own architectures (different `down_proj` shapes, different models) and are **useless for Qwen**. Cell 8 computes these fresh for Qwen — the single most expensive cell. Qwen's `intermediate_size=18944` is the **largest of any arm**, so per-layer cache size is the largest seen (~1.0–1.1 GiB/layer; `18944 × float32` mom2).
2. **MEMIT modifies weights in place; Copy-Unmount applies.** MEMIT's joint-overlay edit is reversed by the bit-exact Copy-Unmount mechanism validated across 6 configs (5 Llama + Mistral). This runbook inherits Copy-Unmount; a successful Qwen unmount at `drift=0.00e+00` would be the **7th validated config** (and the second non-Llama architecture — a meaningful determinism-discipline extension to a distinct decoder family).

---

## Part I — Inheritance Map

### 1.1 Inheritance lineage

```
═══════════════════════════════════════════════════════════════════
        stage_1_sect_runbook v1.7   (root MEMIT-side runbook)
                  │
                  │  model swap 8B → 3B  (Axis 8)
                  ▼
        t1_alt_model_3b_memit_runbook v0.1
                  │
                  │  model swap Llama-3.2-3B → Mistral-7B-v0.3
                  │  (cross-architecture; Axis 10 — first instance)
                  ▼
        t3_mistral_7b_memit_runbook v0.1   (DIRECT structural template)
                  │
                  │  model swap Mistral-7B-v0.3 → Qwen2.5-7B
                  │  (cross-architecture confirmation; Axis 10 — second instance)
                  ▼
        t3_qwen_7b_memit_runbook v0.1   ◄── (this artifact)
═══════════════════════════════════════════════════════════════════

Sibling references (NOT load-bearing for authoring):
  - t1_alt_model_3b_memit_akd_runbook v0.1   (AKD instrument — Cell P1 source IF AKD pre-flight added)
  - t2_rome_runbook v0.2                      (ROME-side; eliminated S2.18; forensic record)
```

### 1.2 Direct-inheritance surfaces

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition | `t3_mistral_7b_memit_runbook v0.1` Part IV–VII | verbatim with §1.4 substitutions |
| Patch application discipline | `memit-patches-canonical v2.5` §6–§7 | verbatim (Pad-Token RE-DERIVED; see §3.2) |
| Constraint registry | `memit-patches-canonical v2.5` §3 + §10 | verbatim |
| Verdict surface taxonomy | `t3_mistral_7b_memit_runbook v0.1` Cell 10 / `stage_1_sect_runbook v1.7` §7 | verbatim |
| Trial protocol | IC-S24-4 (5 facts × 3 replicates; Route-A single-dispatch) | verbatim |
| Acceptance bands | 0.5 cons / 0.05 gen / 0.05 spec / 1e-4 unmount | verbatim (model-agnostic) |
| Verdict-integrity subset | D-S215D2-VERDICT-INTEGRITY-1 {cfb-v3-001/002/005} | verbatim (re-confirm STRICT class on Qwen tokenizer, Cell 6) |
| Copy-Unmount mechanism | `memit-patches-canonical v2.5` (IC-S23-4) | verbatim (APPLICABLE under MEMIT; in-place weight restore is architecture-agnostic) |
| Cross-architecture config idiom | `framework_finding v1.4` §2.4 (D-S229-HPARAM-IDIOM-2) | verbatim port primitive |
| Forward routing matrix | `t3_mistral_7b_memit_runbook v0.1` §IX | EXTENDED (T.3-β confirmation routing per §IX) |

### 1.3 Cell delta map

| Cell | Delta class | Notes |
|---|---|---|
| 0 | structural inheritance verbatim | OS preamble + dependency install; Qwen tokenizer is `tiktoken`/BPE-backed — `transformers>=4.37` provides it; `tokenizers` + `transformers` load-bearing (no `sentencepiece` requirement, unlike Mistral) |
| 1 | structural inheritance | MEMIT engine clone + snapshot at canonical SHA (same engine as all prior arms) |
| 1.5 | RE-AUTHORED — Qwen module introspection | **HIGHEST-RISK port check**: verify `model.layers.{}.mlp.down_proj` exists on `Qwen2ForCausalLM` via `named_parameters()`; verify `lm_head.weight` PRESENT (untied); verify `down_proj` shape `[3584, 18944]` (NEW shape) |
| 2 | structural inheritance + Pad-Token RE-DERIVATION | P-4 Required (Qwen family); Pad-Token re-derived to Qwen convention (§3.2) |
| 3 | APPLICABLE — cov-cache entry gate | expect `qwen2_5_7b` cov dir ABSENT at first execution |
| 4 | RE-AUTHORED — Qwen structural fields + reference band | `v_loss_layer=27`, `lm_head_module=lm_head` (UNTIED — 8B/Mistral-form not 3B-form), `hidden_size=3584`, `intermediate_size=18944`, band `[4,5,6,7,8]` (EasyEdit reference per OQ-V12-T-BRANCH-3) |
| 5 | INVERTED — baseline PRODUCER (Checkpoint #1 on Qwen) | PRODUCES `qwen2_5_7b_baselines.json`; FIRST determinism checkpoint in a fresh Qwen chain (no prior baseline to consume) |
| 6 | RE-AUTHORED — token re-resolution against Qwen tokenizer | ALL target/probe token IDs re-resolved; multi-token classification re-run from scratch; prefer single-token integrity-subset targets (OQ-S230-QWEN-FRAG-1) |
| 7 | structural inheritance | pre-edit baseline against current Qwen state |
| 8 | RE-AUTHORED — fresh Qwen cov computation | `/workspace/covariance_caches/qwen2_5_7b/`; ~50–80 min for `[4..8]` (largest per-layer cache of any arm) |
| 9–12 | structural inheritance | MEMIT edit dispatch + verdict surface + Copy-Unmount + JSON |
| 13 | EXTENDED — T.3-β cross-architecture-confirmation routing matrix | 3-route gate + §IX routing; internal-vs-external signature is the PRIMARY read |
| 14–17 | declarative inheritance | Block C (Route-A single confirmatory dispatch default) |
| 18 | APPLICABLE — cov-cache integrity gate | verifies fresh Qwen computation post-Cell-8 |
| 19–20 | structural inheritance | NV inventory + manifest extension |

### 1.4 Substring substitutions for verbatim cells

| Substitution | Pattern |
|---|---|
| Model name | `mistralai/Mistral-7B-v0.3` → `Qwen/Qwen2.5-7B` |
| Revision SHA | pinned at Cell 1 entry (OQ-V13-T-BRANCH-1; resolve against the HF model card at session entry; recorded in Cell 20 manifest) |
| Baseline path | `mistral_7b_v0_3_baselines.json` → `qwen2_5_7b_baselines.json` |
| Output paths | `t3_mistral_7b_memit_*` → `t3_qwen_7b_memit_*` |
| Cov cache path | `/workspace/covariance_caches/mistral_7b_v0_3/...` → `/workspace/covariance_caches/qwen2_5_7b/...` |
| Layer paths | `model.layers.{4..8}.mlp.down_proj` → `model.layers.{4..8}.mlp.down_proj` (band UNCHANGED — same reference band) |
| Layer band | `[4,5,6,7,8]` → `[4,5,6,7,8]` (UNCHANGED — EasyEdit reference; Axis-9-validated equivalent) |
| `v_loss_layer` | `31` → `27` (n_layers−1 = 28−1) |
| `hidden_size` | `4096` → `3584` |
| `intermediate_size` | `14336` → `18944` |
| `down_proj` shape | `[4096, 14336]` → `[3584, 18944]` |
| `lm_head_module` | `lm_head` → `lm_head` (UNCHANGED — both untied) |
| `pad_token_id` | `2` (Mistral eos) → `151643` (Qwen `<|endoftext|>`; §3.2) |
| `vocab_size` | `32768` → `152064` |

---

## Part II — Architecture Swap Reference (Mistral-7B-v0.3 → Qwen2.5-7B)

### 2.1 Architecture comparison (four-way, with the 8B canonical + the two prior cross-model arms for context)

| Property | Llama-3.1-8B (canonical) | Llama-3.2-3B (Axis 8) | Mistral-7B-v0.3 (Axis 10-α) | **Qwen2.5-7B (Axis 10-β)** |
|---|---|---|---|---|
| `model_type` | `llama` | `llama` | `mistral` | **`qwen2`** |
| HF class | `LlamaForCausalLM` | `LlamaForCausalLM` | `MistralForCausalLM` | **`Qwen2ForCausalLM`** |
| Hidden size | 4096 | 3072 | 4096 | **3584** |
| Intermediate size | 14336 | 8192 | 14336 | **18944** |
| Decoder layers (`n_layers`) | 32 | 28 | 32 | **28** |
| `v_loss_layer` (= n−1) | 31 | 27 | 31 | **27** |
| `tie_word_embeddings` | False | True | False | **False** |
| `lm_head_module` | `lm_head` | `model.embed_tokens` | `lm_head` | **`lm_head`** |
| `down_proj` shape | `Linear(14336, 4096)` | `Linear(8192, 3072)` | `Linear(14336, 4096)` | **`Linear(18944, 3584)`** |
| fp16 weight footprint | 16.06 GiB | 6.42 GiB | ~14.5 GiB | **~15.2 GiB** |
| Tokenizer | Llama-3 BPE | Llama-3 BPE | Mistral SentencePiece (v3) | **Qwen2 BPE (tiktoken-style)** |
| `vocab_size` | 128256 | 128256 | 32768 | **152064** |
| `pad_token_id` convention | 128001 | 128001 | 2 (= eos) | **151643 (`<|endoftext|>`)** |
| `max_position_embeddings` | 131072 | 131072 | 32768 | **32768** |
| attention | GQA | GQA | GQA (sliding-window legacy) | **GQA + QKV bias (Qwen2 distinctive)** |

**Reading of the table.** The Qwen column is the **most structurally distinct of all four** — it differs from the 8B canonical on hidden size, intermediate size, layer count, vocab, pad convention, and tokenizer family, and adds a Qwen2-distinctive attention detail (QKV bias). It shares with the 8B/Mistral canonical only the untied-embedding property and the GQA family. This is precisely why Qwen is the near-decisive confirmation: a `0/5` here cannot be attributed to shared Llama-lineage architecture shape. The `down_proj` shape `[3584, 18944]` is **new** — not seen on any prior arm — which is the single most important fact for the cov-cache and module-introspection cells.

`v_loss_layer=27` coincides numerically with the 3B arm (both 28-layer models), but this is a layer-count coincidence, not a shared property; the models are otherwise unrelated.

### 2.2 MEMIT edit-site validity on Qwen

MEMIT/ROME reference band for the Qwen2.5-7B architecture per the knowledge-editing literature (EasyEdit Qwen support; CaKE arXiv 2503.16356 §B.2 edits the early-MLP critical range — ROME at layer 5 of Qwen2.5-7B; MEMIT critical-range consistent with the early band): `[4, 5, 6, 7, 8]`, value-loss layer `model.layers.27`, target module `model.layers.{}.mlp.down_proj`. Per the §6'''.1 methodology lock (OQ-V12-T-BRANCH-3, carried to Qwen): **adopt the engine's reference band for the target architecture; do NOT re-sweep.** Axis 9 (S2.27) established that the `[4–8]` band is empirically equivalent to the `[2–6]` canonical band on Llama (`delta_vs_2_6_floor ≈ 0`), and S2.29 adopted `[4..8]` on Mistral cleanly — so adopting `[4–8]` for Qwen keeps the result interpretively clean and parity-aligned with the Mistral arm. A band already confirmed non-load-bearing across two architecture families.

| Layer | Qwen validity (`0 ≤ idx < 28`) | Relative depth (Qwen) | Memo |
|---|---|---|---|
| L4 | VALID | 14.3% | band entry (EasyEdit MEMIT critical-range start) |
| L5 | VALID | 17.9% | ROME single-layer site (CaKE Qwen2.5-7B) |
| L6 | VALID | 21.4% | |
| L7 | VALID | 25.0% | |
| L8 | VALID | 28.6% | band exit |

`C-S230-4` asserts the bound `0 ≤ idx < 28` for every index in `[4..8]` at Cell 4 entry. (Note: the band sits slightly deeper in *relative* terms than on the 32-layer models because Qwen has fewer layers; the absolute layer indices are held identical to the reference band for cross-arm parity, consistent with the band-invariance result.)

### 2.3 VRAM projection (RTX 4090 24 GiB)

```
═══════════════════════════════════════════════════════════════════
  Component                                       VRAM cost
  ─────────────────────────────────────────────────────────
  Model weights (fp16, 7.6B)                      ~15.2 GiB
  Activations + gradient accumulation (5-layer)   ~3–4  GiB
  mom2 inverse + workspace (18944-wide)           ~1.5–2.5 GiB
  cuBLAS + workspace                              0.50  GiB
  ─────────────────────────────────────────────────────────
  Total under MEMIT canonical hparams:            ~20–22 GiB
  RTX 4090 ceiling:                               24.00 GiB
  HEADROOM:                                       2–4 GiB   ← fits, but TIGHTEST of any arm
═══════════════════════════════════════════════════════════════════
```

Provenance: Qwen2.5-7B fp16 weights (~15.2 GiB) sit between Mistral (14.5) and 8B (16.06). The larger `intermediate_size=18944` (vs 14336 on Mistral/8B) inflates BOTH the mom2 workspace at cov compute AND the edit-time activation footprint relative to Mistral — so the projected peak (~20–22 GiB) is **above the Mistral arm's ~19–21 GiB** and is the **tightest headroom of any arm to date** (`OQ-S230-VRAM-1` confirms empirically at Cell 8/9). The S2.29 stale-kernel reclaim lesson (§8.3) is load-bearing here: a clean card is required before the Qwen edit. Mitigation if exceeded: the cov compute (Cell 8) is the larger memory consumer but runs without edit-time activation retention, so an OOM is more likely at edit dispatch (Cell 9); fall-back is single-layer scope (L5 only — the CaKE/EasyEdit ROME site) or fp16 cov-only relaxation (§IX FAIL-at-environment route).

---

## Part III — Patch Inheritance

### 3.1 Patch applicability matrix

| Patch | Qwen2.5-7B applicability | Defect class | Provenance |
|---|---|---|---|
| P-1 (`.upstream_pristine` + parent_module substitution) | APPLICABLE | Universal HF transformer with numeric submodule indices | `memit-patches v2.5` §2 |
| P-2 (fp16 cdist; cov-compute backward) | APPLICABLE | Universal fp16-loaded model | `memit-patches v2.5` §2 |
| P-3' + Device-Map | NOT APPLICABLE — single-GPU RTX 4090 dispatch; no multi-GPU sharding | `memit-patches v2.5` §3 / §5 |
| **P-4 (config-attribute compat for non-GPT-2-family)** | **APPLICABLE — REQUIRED** (Qwen2 uses the unified HF-2.0 config schema, identical to Mistral/Llama) | `n_embd`/`n_positions` → `hidden_size`/`max_position_embeddings` getattr-fallback | `memit-patches v2.5` §3.5 |
| P-5 (dataset-loader modernization) | APPLICABLE — corpus-side, model-agnostic | `memit-patches v2.5` §3.6 |
| P-6 (`size_suffix` f-string `_t100_` segment) | APPLICABLE — cache-filename-side, model-agnostic | `memit-patches v2.5` §3.7 |
| P-7 (`batch_tokens` propagation to `layer_stats`) | APPLICABLE — load-bearing (Qwen `max_position_embeddings=32768` >> 8192 threshold; same regime as Mistral/8B) | `memit-patches v2.5` §3.8 |
| **Pad-Token** | **APPLICABLE — RE-DERIVED** (Qwen base has no dedicated pad token; set to `<|endoftext|>` = 151643) | tokenizer attribute | `memit-patches v2.5` §4 + §3.2 below |
| Copy-Unmount | APPLICABLE — in-place weight restore is architecture-agnostic; 7th validated config if `drift=0.00e+00` | IC-S23-4 |

**Patches NOT applicable** (GRACE-side, S2.22): P-1-GRACE / P-2-GRACE / F-2 (CONFIGURATION_LAYER) / GRACE adapter-detach unmount.

**Key port observation.** P-4 — the patch that resolves `AttributeError: 'Config' object has no attribute 'n_embd'` by routing to the unified HF-2.0 config schema — is the patch that makes the engine work on *any* non-GPT-2-family model. Qwen2 uses the same `hidden_size` / `max_position_embeddings` config schema as Llama and Mistral, so P-4 applies **verbatim** — it is the structural reason the byte-identical Llama/Mistral engine runs unchanged on Qwen. `memit-patches v2.5` §3.5.2 lists the modern-HF families as Required; Qwen2 falls in the same class. (If §3.5.2 does not name Qwen explicitly, the getattr-fallback form of P-4 is family-agnostic — it triggers on the *absence* of `n_embd`, which is true for every modern-HF config including Qwen2; verify at Cell 2 that P-4 reports APPLIED at all four sites and that no `AttributeError` surfaces at first `compute_z`.)

### 3.2 Pad-Token RE-DERIVATION for Qwen (the one patch that changes content)

The Mistral Pad-Token patch (`t3_mistral_7b_memit_runbook v0.1` §3.2) set `tokenizer.pad_token_id = eos_token_id = 2`. Qwen2.5-7B base has a different convention. Qwen's special-token scheme distinguishes `<|endoftext|>` (id `151643`, used as bos and the natural document/pad delimiter) from `<|im_end|>` (id `151645`, the chat eos). For the **base** model and for MEMIT's padded-batch tokenization purpose, the community-standard convention (EasyEdit Qwen handling) is to set the pad token to `<|endoftext|>`.

**Re-derived Pad-Token form for Qwen:**
```
tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids("<|endoftext|>")   # = 151643 for Qwen2.5-7B
# equivalently, on the base model: tokenizer.pad_token = "<|endoftext|>"
```

This is functionally equivalent to the Mistral/Llama patch's purpose (give MEMIT's batched tokenization a valid pad id so padded-batch forward passes don't raise) but uses Qwen's convention. The patch is applied at Cell 2 and verified by asserting `tokenizer.pad_token_id == 151643` (`C-S230-PADTOKEN-1`). **Authoring note:** if the live tokenizer reports `pad_token_id` already set (some Qwen tokenizer revisions ship `pad_token_id=151643` pre-set), the patch is a verified no-op rather than a re-derivation — Cell 2 records which branch was taken. The assertion target (`151643`) is the same either way.

### 3.3 P-7 note for Qwen (operator-facing)

P-7 propagates `batch_tokens=100` into MEMIT's edit-time `get_cov` → `layer_stats` chain so the covariance cache filenames carry the `_t100_` segment and the edit-time lookup hits. Qwen's `max_position_embeddings = 32768` is far above the `8192` threshold — same regime as Llama-3.1-8B and Mistral — so P-7 is **load-bearing**: without it the edit-time lookup constructs filenames lacking `_t100_`, misses the Cell 8 caches, and falls back to a full-`npos` local compute that OOMs (especially likely given the tightest-of-arm Qwen VRAM headroom, §2.3). `D-S230-PATCH-INHERITANCE-1` records that all MEMIT patches inherit per `memit-patches v2.5` and the engine source is byte-identical to the Llama/Mistral baseline (verified via patch-site line numbers at Cell 1.0).

### 3.4 Process constraints (carry-forward)

`C-S25-15` / `C-S26-1` / `C-S26-2` / `C-S26-3` / `C-S28-1` carry forward verbatim from `memit-patches v2.5`. The R1.1 / R1.2 / R1.3 cell-level gates apply; R1.3 (canonical dry-run gate) absorbs into the post-compute verification gate (`C-S230-3`) at Cell 8 close, as in the Mistral arm.

---

## Part IV — BLOCK A: Pre-flight

### Cell 0 — Pod bring-up + dependency install  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Bring the pod to a known dependency state. Carries the S2.24 lesson (`OQ-S222-CELL0-DEPS-1`): fresh pod images require explicit installation; do not assume preinstalled deps. Carries the S2.29 hard lesson (`C-S229-HFHOME-1`): set `HF_HOME` to NV BEFORE any HF import.

**WHAT / WHY (operator-facing):** This cell confirms the GPU is the expected RTX 4090, confirms the Network Volume is mounted, points the HuggingFace cache at the NV (not the small container disk), and installs the Python packages the engine needs. Qwen's tokenizer is BPE/tiktoken-style and is provided natively by `transformers>=4.37` — so unlike the Mistral arm, `sentencepiece` is NOT required here; `tokenizers` (a `transformers` dependency) carries it.

**Cell body (operator reading order):**
1. **`C-S229-HFHOME-1` (HARD Cell-0 prerequisite, carried from S2.29):** export `HF_HOME=/workspace/hf_cache` and `HF_HUB_CACHE=/workspace/hf_cache/hub` BEFORE any HuggingFace import. The container disk is ~20 GiB and fills on a single 7B model pull; the model cache MUST live on NV. (S2.29 caught a 100%-full-container-disk OOM at first Mistral load from skipping this — do not repeat.)
2. Confirm pod identity + GPU: `nvidia-smi` (expect single RTX 4090, 24 GiB). **Expected healthy output:** one GPU line, 24576 MiB total, ~0 MiB used. **Stale-kernel reclaim (S2.29 §8.3):** if any idle `ipykernel` holds VRAM, `kill <pid>` to reclaim — the Qwen edit peaks at ~20–22 GiB and a clean card is mandatory (tightest headroom of any arm).
3. Confirm NV mount: `ls /workspace` (expect existing `covariance_caches/`, `architecture_profile/`, `session_logs/`, `hf_cache/`).
4. Set `TOKENIZERS_PARALLELISM=false` at the notebook top (S2.29 §8.4; silences the fork warning during cov compute; cosmetic).
5. Install pinned dependencies (Surface A; explicit):
   - `transformers` (engine-compatible pin per `memit-patches v2.5` engine SHA; Qwen2 support is present in all transformers ≥ 4.37, so the canonical pin already covers it — confirm the pin is ≥ 4.37)
   - `accelerate`, `hydra-core`, `pyyaml`, `protobuf`
   - **NOT** `sentencepiece` (Qwen does not need it — it was Mistral-specific)
   - any MEMIT-specific deps surfaced at Cell 1.5 introspection (re-run install if introspection reveals a gap).
6. Print acceptance string: `CELL0_DEPS_OK <transformers_version> <accelerate_version> hf_home=/workspace/hf_cache`.

**Halt conditions:**
- GPU is not RTX 4090 24 GiB → halt (VRAM projection §2.3 invalid; the Qwen headroom is already the tightest of any arm — a smaller GPU does not fit).
- NV mount absent → halt (no durable tier).
- `HF_HOME` not on NV → halt (container-disk OOM at Cell 1.5/5 model pull is near-certain otherwise).
- `transformers` pin < 4.37 → halt (Qwen2 architecture not registered).

---

### Cell 1 — MEMIT engine clone + NV snapshot  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Clone the canonical MEMIT engine at its pinned SHA and snapshot the source to NV. The engine is the SAME engine run on every prior arm — byte-identical. Absorbs `OQ-S222-CELL1-2` (snapshot source to a content-addressed NV path at first clone).

**WHAT / WHY (operator-facing):** We are NOT cloning anything Qwen-specific. The whole point of the cross-architecture test is that the engine is unchanged; only the model it operates on differs. This cell clones that unchanged engine and proves (Cell 1.0) it is byte-identical to what ran on Llama and Mistral, so any result difference is attributable to the model, not engine drift. (S2.29 reused the live-patched engine working tree directly, SHA 80426fd9; if that working tree is still resident on NV from the Mistral arm, this cell verifies its byte-identity rather than re-cloning — the stronger single-variable claim per D-S229-ENGINE-REUSE-1.)

**Cell body (operator reading order):**
1. Resolve and pin the target model HF revision SHA (`OQ-V13-T-BRANCH-1`): record the current `Qwen/Qwen2.5-7B` base revision commit SHA from the HF model card at session entry; print `QWEN_MODEL_SHA <sha>`. **License/gating check (§6'''.2):** Qwen2.5 ships under the Apache-2.0 license (the 7B/14B/32B/72B Qwen2.5 base models are Apache-2.0; the 3B and 72B-Instruct carry the Qwen license — the 7B base is Apache-2.0 and ungated, like Mistral, unlike Llama). Confirm ungated at session entry; if a license-acceptance gate is present on the pinned revision, accept it for this account before the pull.
2. Engine acquisition (`D-S230-ENGINE-REUSE-1`):
   - If the live-patched engine working tree from the Mistral arm is resident on NV (`/workspace/memit_dry_run/memit/`, SHA 80426fd9), verify it is present and record its SHA — REUSE it (byte-identical to all ten prior axes; stronger for the single-variable claim than a fresh clone).
   - Else clone the canonical MEMIT engine repo (forked, pinned per `memit-patches v2.5` §9 anchor SHA).
3. Record the engine SHA (`C-S230-1`): print `MEMIT_ENGINE_SHA <sha>`; carried into the Cell 20 manifest.
4. **Cell 1.0 byte-identity check (`D-S230-PATCH-INHERITANCE-1`):** verify the engine source is byte-identical to the Llama/Mistral baseline at the patch-site line numbers in `memit-patches v2.5` (P-1/P-2/P-4/P-5/P-6/P-7 anchor lines). Print per-patch-site match/mismatch. Any mismatch → halt.
5. **Engine source snapshot (`C-S230-2`):** if a clean (pre-patch) snapshot from a prior arm already exists at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/`, verify it; else copy the clean engine source there BEFORE any patch. Print `ENGINE_SNAPSHOT_OK <path>`.

**Halt conditions:**
- Clone fails (network / auth) → halt.
- Qwen license gate present and not accepted (model pull at Cell 1.5 will 401) → surface to operator; halt until accepted.
- Cell 1.0 byte-identity mismatch at any patch site → halt; reconcile patch line numbers against the actual SHA.

---

### Cell 1.5 — Qwen module introspection (RE-AUTHORED — HIGHEST-RISK PORT CHECK)  [Surface B]

**Specialist:** memit-specialist
**Purpose:** RE-AUTHORED for the Qwen architecture. This is the **highest-risk delta in the entire port** (per §6'''.2 / OQ-V13-T-BRANCH-2). The MEMIT hparams reference module paths by string template (`rewrite_module_tmp = 'model.layers.{}.mlp.down_proj'`, etc.). If `Qwen2ForCausalLM` names its MLP down-projection differently from `LlamaForCausalLM`/`MistralForCausalLM`, the edit silently targets the wrong (or a non-existent) module. AND the `down_proj` shape is NEW (`[3584, 18944]`) — this cell verifies both the path strings AND the new shape BEFORE any config is built.

**WHAT / WHY (operator-facing):** Qwen, Llama, and Mistral are all standard HF decoder transformers and are *expected* to use identical module names — but "expected" is not "verified," and Qwen is the most distinct of the three. This cell loads the model's parameter name list and confirms the exact strings MEMIT will format into exist, and that the down-projection weight has the Qwen shape. It also confirms `lm_head.weight` is a real, untied parameter (it is, for the Qwen 7B base) — the same as Mistral, the inverse of the 3B case. Getting this wrong is the single most likely cause of a spurious or misleading result.

**Cell body (operator reading order):**
1. Load `Qwen/Qwen2.5-7B` at the pinned SHA, fp16 (first model load; ~15.2 GiB — confirm it fits, ~0 MiB → ~15 GiB on `nvidia-smi`; with `HF_HOME` on NV the pull lands on the durable tier).
2. Enumerate `model.named_parameters()` and assert the presence of, for a representative layer in the reference band (e.g., L5):
   - `model.layers.5.mlp.down_proj.weight` (the MEMIT `rewrite_module_tmp` target) — **shape must be `[3584, 18944]`** (the `down_proj` weight is `out_features × in_features = hidden × intermediate = 3584 × 18944`).
   - `model.layers.5.mlp` (the `mlp_module_tmp` target).
   - `model.layers.5` (the `layer_module_tmp` target).
   - `model.layers.27` (the `v_loss_layer` target, n−1).
3. **Untied-embedding verification (`C-S230-LMHEAD-1`):** assert `lm_head.weight` IS PRESENT in `named_parameters()` (Qwen2.5-7B `tie_word_embeddings=False`). This confirms `lm_head_module='lm_head'` is the correct config field — the 8B/Mistral-canonical form, NOT the 3B tied `model.embed_tokens` override. If `lm_head.weight` is unexpectedly absent (would indicate a tied-embedding Qwen variant — true of the smaller Qwen2.5 sizes but NOT the 7B), fall back to the tied-embedding adaptation per `D-S227-LMHEAD-1` and re-derive `lm_head_module`.
4. **Qwen2-distinctive attention note (informational, non-halting):** Qwen2 attention projections carry a bias term (`q_proj.bias`, `k_proj.bias`, `v_proj.bias`) absent in Llama/Mistral. MEMIT does not touch attention modules (it edits `mlp.down_proj` only), so this is immaterial to the edit — recorded for completeness so the operator does not mistake the extra bias parameters for a problem.
5. Confirm the engine's MEMIT package surface (`memit_main`, `rome/layer_stats`, `util/nethook`) resolves as on Llama/Mistral (engine unchanged).
6. Print `QWEN_MODULE_INTROSPECT_OK` with: the 4 resolved module-path strings, the `down_proj` weight shape, and `lm_head_untied=True`.

**Halt conditions:**
- Any of the 4 module-path templates does not resolve to a real named module → halt (module-name mismatch; the MEMIT module-path templates require Qwen-specific re-derivation before any edit — do NOT proceed on assumed paths).
- `down_proj.weight` shape ≠ `[3584, 18944]` → halt (architecture mismatch vs the config the runbook was authored against — likely a wrong model variant pulled).
- `lm_head.weight` absent → branch to tied-embedding adaptation (do not halt; re-derive `lm_head_module` per §2.4 of framework_finding v1.3 and re-run).

---

### Cell 2 — MEMIT patch application (+ Pad-Token RE-DERIVATION)  [Surface A → B]

**Specialist:** memit-specialist
**Purpose:** Apply the MEMIT patch set per `memit-patches v2.5` §6–§7 and report patch state. Pad-Token is RE-DERIVED for Qwen (§3.2). (If the engine working tree was reused live-patched from the Mistral arm per Cell 1, this cell is a VERIFICATION pass — confirm patches live — not a re-apply; D-S230-PATCH-INHERITANCE-1.)

**WHAT / WHY (operator-facing):** These patches make the GPT-J-authored MEMIT engine run correctly on a modern HF model. P-4 is the load-bearing one for cross-architecture: it routes the engine's old `n_embd`/`n_positions` config lookups to the modern `hidden_size`/`max_position_embeddings` that Qwen uses — exactly as it does for Llama and Mistral. The one patch that changes content for Qwen is Pad-Token, set to `<|endoftext|>` (151643) per Qwen convention.

**Cell body (operator reading order):**
1. Apply (or verify-live) patches in canonical order: P-1, P-2, P-4, P-5, P-6, P-7, **Pad-Token (re-derived: `pad_token_id = 151643`)**. (P-3' and Device-Map are NOT applied — single-GPU RTX 4090 per §3.1.)
2. Each patch prints `PATCH <id> APPLIED` (or `PATCH <id> LIVE` if verified from a reused working tree). P-7 requires BOTH post-state markers present; partial-marker → halt. **P-4 must report APPLIED/LIVE at all four sites** (`compute_z.py`, `compute_v.py`, `layer_stats.py` ×2) — P-4 is the patch most likely to matter for a non-Llama model, so its application is verified explicitly. A smoke-check `compute_z` import that does not raise `AttributeError` on Qwen's config confirms P-4 is effective.
3. **Pad-Token verification (`C-S230-PADTOKEN-1`):** assert `tokenizer.pad_token_id == 151643`. Print `PADTOKEN_QWEN_OK pad=<|endoftext|>=151643` (and whether it was re-derived or already-set per §3.2 authoring note).
4. Construct the patch-state record matching `memit-patches v2.5` §8 schema. `patches_required_but_not_applied` MUST be empty.
5. Print `CELL2_PATCH_STATE_OK` with the full `patches_applied` dict.

**Halt conditions:**
- Any patch reports a partial-marker state → halt (reconcile per §3.8.7).
- P-4 NOT applied/live at all four sites → halt (the engine will raise `AttributeError` on Qwen's config at first `compute_z`).
- `patches_required_but_not_applied` non-empty → halt.
- Pad-Token assertion fails (`pad_token_id != 151643`) → halt (batched tokenization will misbehave).

---

### Cell 3 — Covariance-cache entry gate  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Check whether any `qwen2_5_7b` covariance caches already exist at NV. At first T.3-β execution, NONE exist — this cell confirms absence and sets the expectation that Cell 8 computes fresh.

**Cell body (operator reading order):**
1. List `/workspace/covariance_caches/qwen2_5_7b/.../wikipedia_stats/` (expect: absent or empty at first execution).
2. If absent/empty → print `COV_CACHE_QWEN_ABSENT — Cell 8 will compute fresh` and set `cov_cache_compute_required = True`.
3. If present (re-execution) → verify per-layer file size + checksum against the Cell 8 provenance record; print `COV_CACHE_QWEN_PRESENT — integrity {OK|MISMATCH}`. On MISMATCH → halt.

**Halt conditions:**
- Present-but-corrupt cov cache (checksum mismatch) → halt.

---

### Cell 4 — MEMIT hyperparameter config (RE-AUTHORED — Qwen structural fields)  [Surface B]

**Specialist:** memit-specialist
**Purpose:** RE-AUTHORED for Qwen. Build the MEMIT hparams by the cross-architecture config idiom (`framework_finding v1.4` §2.4, D-S229-HPARAM-IDIOM-2): **load the 8B-canonical MEMIT JSON, override only the architecture-structural fields, change no tuning knob, re-resolve the tokenizer.** For Qwen those structural overrides are MORE than the Mistral arm (dims differ, layer count differs) but the discipline is identical.

**WHAT / WHY (operator-facing):** The config tuning knobs (`v_lr`, `mom2_update_weight`, grad steps) carry forward UNCHANGED from the configuration validated across all ten prior axes — we are explicitly NOT re-tuning, because re-tuning would conflate an architecture difference with a hparam difference and destroy the single-variable interpretation. Only the fields forced by the architecture change (layer count, dimensions, embedding tying, the edit band) are overridden.

**Cell body (operator reading order):**
1. Load the reference MEMIT JSON (8B-canonical) and apply the architecture-structural overrides:

| Hparam | Value | Override class | Provenance |
|---|---|---|---|
| MEMIT layer set | `[4, 5, 6, 7, 8]` | **OVERRIDE — reference band** | EasyEdit/CaKE MEMIT critical-range for Qwen2.5-7B (arXiv 2503.16356 §B.2); OQ-V12-T-BRANCH-3; Axis-9-validated equivalent to `[2–6]`; parity with Mistral arm |
| `v_loss_layer` | `27` | **OVERRIDE — structural** (n−1 = 28−1) | §2.1; coincides with 3B value by layer-count, unrelated otherwise |
| `lm_head_module` | `lm_head` | **OVERRIDE — structural** (untied; 8B/Mistral form, NOT 3B tied override) | C-S230-LMHEAD-1 (Cell 1.5 verified untied) |
| `hidden_size` (if referenced by engine config) | `3584` | **OVERRIDE — structural** | §2.1; engine reads via P-4 getattr from model config |
| `intermediate_size` (if referenced) | `18944` | **OVERRIDE — structural** | §2.1 |
| `mom2_update_weight` | 15000 | INHERIT (tuning knob; NOT re-tuned) | S2.10 PASS configuration |
| `v_lr` | 0.5 | INHERIT | S2.10 PASS configuration |
| `v_num_grad_steps` | 25 | INHERIT | S2.10 PASS configuration |
| `kl_factor` | 0.0625 | INHERIT | canonical |
| `clamp_norm_factor` | 0.75 | INHERIT | canonical |
| `v_weight_decay` | 0.5 | INHERIT | canonical |
| `rewrite_module_tmp` | `model.layers.{}.mlp.down_proj` | INHERIT (verified at Cell 1.5) | §2.1 |
| `mlp_module_tmp` | `model.layers.{}.mlp` | INHERIT (verified) | §2.1 |
| `layer_module_tmp` | `model.layers.{}` | INHERIT (verified) | §2.1 |
| `ln_f_module` / `lm_head` companion fields | Qwen `model.norm` / `lm_head` | OVERRIDE — structural (verify names at Cell 1.5 if engine references them) | §2.1 |
| `mom2_dataset` / `mom2_n_samples` / `mom2_dtype` | `wikipedia` / 100000 / `float32` | INHERIT | canonical envelope |
| Edit dispatch | joint-overlay 5-fact | INHERIT | S2.14-D D.3 protocol |

2. **`C-S230-4` bound assertion:** assert every index in `[4..8]` satisfies `0 ≤ idx < n_layer = 28`. Print `LAYER_BOUND_OK [4..8] < 28`.
3. **Full-field diff record (`C-S230-2-DIFF`):** print the complete `MEMITHyperParams` and annotate each field INHERIT vs OVERRIDE, so the single-variable claim (architecture-only) is auditable at the field level. The ONLY tuning-knob value that differs from the 8B canonical is `layers` (the reference band) — and that band is Axis-9-validated as equivalent and was used cleanly on Mistral.
4. Print `CELL4_HPARAM_OK` with the full config + the INHERIT/OVERRIDE annotation map.

**Open question carried:** `OQ-S229-1` (carried) — whether `mom2_update_weight=15000` (the Llama PASS value) is correctly calibrated at the Qwen architecture, or requires re-tuning. PROVISIONAL inheritance; not resolved at authoring (resolving it is out of scope for the single-variable architecture port — re-tuning is a deeper arm).

**Halt conditions:**
- Layer bound assertion fails → halt (config error).
- `lm_head_module` set to a value Cell 1.5 did not verify present → halt (config/introspection inconsistency).

---

### Cell 5 — Baseline PRODUCE (Checkpoint #1 on Qwen — fresh determinism chain)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** PRODUCES `qwen2_5_7b_baselines.json` — the FIRST determinism checkpoint in a fresh Qwen chain. As with the Mistral Cell 5, there is no prior Qwen baseline to consume; this cell establishes Checkpoint #1 (§6'''.3: "establish a fresh determinism chain per new model"). The baseline is engine-agnostic (captures untouched-model forward-pass state at the pinned SHA) and is the producer artifact a future Qwen re-run would consume.

**WHAT / WHY (operator-facing):** Before editing anything, we record exactly what the untouched Qwen model predicts on all 38 probes. This is the "before" picture. Two jobs: (1) it is the reference for every "did the edit change this?" comparison later; (2) re-running it on a fresh load and getting bit-identical numbers is how we prove the model loads deterministically — the foundation that lets us attribute any later difference to the edit, not to load noise.

**Cell body (operator reading order):**
1. Load `Qwen/Qwen2.5-7B` at the pinned SHA, fp16 (reuse the Cell 1.5 load if still resident).
2. Capture the 38-probe panel pre-edit (5 facts × {3 consistency + 3 generalization + 1 unmount} + 3 shared specificity): for each probe record `top_1_token_id`, `p_top_1_pre`, `top_5`, and (consistency/unmount) `p_target_new_pre` / `p_target_true_pre`. **Prompts are held verbatim from probe-set-v3** (the prompt STRINGS are model-agnostic; only the token IDs differ — those are resolved in Cell 6).
3. Capture per-fact `target_true` = the model's natural top-1 at the canonical prompt `{subject} plays the instrument of`, and its probability. (On Qwen this is re-captured fresh — the Llama/Mistral natural top-1s are NOT assumed; Qwen's natural completion may differ. `OQ-S230-QWEN-TOP1-1`.)
4. **Determinism self-check (Checkpoint #1, `C-S230-CHECKPOINT-1`):** capture the panel TWICE on the same loaded model; assert bit-exact agreement (`drift = 0.00e+00` across all 38 probes, 0 top-1 mismatches). This is the within-session determinism floor; a fresh-reload cross-session gate is established when a later session consumes this baseline.
5. Write `qwen2_5_7b_baselines.json` to NV with: model SHA, `n_layer=28`, `hidden_size=3584`, `intermediate_size=18944`, per-fact target/true captures, per-probe panel, `pad_token_id=151643`.
6. Print `CHECKPOINT_1_QWEN_OK drift_max=<value>` and `CELL5_BASELINE_PRODUCED <path>`.

**Halt conditions:**
- Within-session determinism self-check fails (`drift > 0`) → halt (nondeterministic load; cannot establish a clean baseline — triage before any edit).
- Model load OOM (~15.2 GiB should fit with margin pre-edit) → halt (environment).

---

### Cell 6 — Token re-resolution + MULTI_TOKEN_ALLOWLIST (RE-AUTHORED — Qwen tokenizer)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** RE-AUTHORED. This is the LARGEST correctness surface in the port. NONE of the Llama or Mistral token IDs are valid on Qwen's BPE vocab. Re-resolve every target_new token ID against the Qwen tokenizer and re-run the multi-token classification from scratch. Prefer single-token targets for the verdict-integrity subset (`OQ-S230-QWEN-FRAG-1`). The harp / violin / flute fragmentations seen on Mistral must be re-evaluated against the new vocab.

**WHAT / WHY (operator-facing):** A "token" is a chunk of text the model reads as one unit. Different tokenizers chop words differently. On Llama, `guitar` was one token (id 17418); on Mistral, one token (id 11454, a different number). On Qwen it might be one token with yet another id, or split into pieces. MEMIT's consistency check measures the probability of the target token(s); if we used another model's ids on Qwen we'd be measuring the wrong thing entirely. This cell re-resolves all five targets and classifies each as single-token (clean) or multi-token (needs the first-token-proxy treatment). Qwen's large 152k vocab makes single-token instrument words *more* likely than Mistral's 32k — a plausibly cleaner read.

**Cell body (operator reading order):**
1. For each fact, tokenize `target_new` with a leading space against the Qwen tokenizer (matching the `{subject} plays the instrument of ___` continuation form) and record the full token-id list:
   - cfb-v3-001 `guitar` → Qwen ids `[?]` → classify STRICT_SINGLE_TOKEN if length 1, else MULTI_TOKEN
   - cfb-v3-002 `piano` → Qwen ids `[?]`
   - cfb-v3-003 `violin` → Qwen ids `[?]` (was STRICT on Llama, fragmented to 2-tok on Mistral; re-check — Qwen's large vocab may restore single-token)
   - cfb-v3-004 `harp` → Qwen ids `[?]` (2-tok on both Llama and Mistral; re-check)
   - cfb-v3-005 `flute` → Qwen ids `[?]` (was STRICT on Llama, fragmented to 2-tok on Mistral; re-check)

   **Authoring note:** the exact Qwen ids cannot be authored offline (they depend on the live tokenizer); the cell resolves them at execution and prints them. The classification logic and the allowlist gate are fully specified below; only the literal id integers are execution-resolved. This is the one place where a literal value is necessarily execution-time (a tokenizer query), not a placeholder for operator judgment.
2. **Build `MULTI_TOKEN_ALLOWLIST` fresh from the Qwen classification** (do NOT inherit the Llama `{cfb-v3-004}` or Mistral `{003, 004, 005}` allowlists — each was specific to that tokenizer). Any fact tokenizing multi-token on Qwen is added to the Qwen allowlist with `verdict_class = ALLOWLIST_FIRST_TOKEN_PROXY` and `re_evaluate_at_trial_0 = True`; its first token id is the proxy.
3. **SUBSET hard gate (`D-S217-2` discipline):** assert the Qwen allowlist covers every fact whose `verdict_class == MULTI_TOKEN`. Any multi-token fact absent from the allowlist → `MULTI_TOKEN_FAIL` (session-level HARD halt) until added AND its first-token-proxy is confirmed acceptable.
4. **Integrity-subset single-token preference (`OQ-S230-QWEN-FRAG-1`):** the verdict-integrity subset is `{cfb-v3-001/002/005}` (D-S215D2-VERDICT-INTEGRITY-1). Confirm how many of these tokenize single-token (STRICT) on Qwen. cfb-v3-001 (`guitar`) and cfb-v3-002 (`piano`) carried the load-bearing read on Mistral as STRICT; on Qwen, re-confirm at least these two are STRICT. If `flute` (005) is also single-token on Qwen (plausible given the larger vocab), the integrity subset is fully STRICT — a cleaner read than Mistral, where 005 fragmented. Record the disposition either way; the FAIL read is conservative-in-the-ceiling's-favor under fragmentation regardless (a proxy near-zero post-edit implies the whole-word near-zero).
5. Write `fact_verdicts` (Qwen-resolved) as the single-source record for Cell 8 + Cell 9 (`D-S217-2` cross-cell single-source contract).
6. Print `CELL6_TOKEN_VERIFY_OK` with the per-fact Qwen token-id list + verdict_class map + the freshly-built allowlist + the integrity-subset STRICT count.

**Halt conditions:**
- `MULTI_TOKEN_FAIL` (a non-allowlisted fact tokenizes multi-token) → session-level HARD halt; add to allowlist AND verify first-token-proxy acceptable.
- A target_new fails to tokenize / produces an empty id list → halt (corpus/tokenizer incompatibility; investigate before edit).
- ZERO of the integrity subset {001/002/005} tokenizes single-token on Qwen → halt for review (the load-bearing read would rest entirely on proxies; surface to operator before proceeding — low prior given Qwen's large vocab, but a real degradation if it occurs).

---

### Cell 7 — Pre-edit baseline panel  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Capture the pre-edit probe panel against the current (just-loaded, unedited) Qwen state, using the Qwen-resolved token ids from Cell 6. Cross-checks Cell 5's producer baseline.

**Cell body (operator reading order):**
1. For each of the 38 probes, capture pre-edit: `top_1_token_id`, `p_top_1_pre`, and (consistency) `p_target_new_pre` using the **Qwen** target ids; (unmount) `p_target_true_pre`.
2. For any ALLOWLIST_FIRST_TOKEN_PROXY fact, capture first-token-proxy P (the Qwen first-token id from Cell 6).
3. Cross-check Cell 7 vs Cell 5 panel (both pre-edit on the same load → agree to FP16 noise). Print `CELL7_BASELINE_OK` + any probe whose Cell 7 vs Cell 5 drift exceeds `1e-5` (informational unless Cell 5 passed and Cell 7 diverges → within-session nondeterminism halt).

**Halt conditions:**
- Intra-session Cell 7 vs Cell 5 divergence `> 1e-5` → halt (within-session nondeterminism).

---

### Cell 8 — Fresh covariance computation (RE-AUTHORED — Qwen)  [Surface A → B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** RE-AUTHORED for Qwen. Compute the per-layer `mom2` covariance statistics for Qwen2.5-7B from scratch over the canonical Wikipedia corpus, for the reference band `[4..8]`. Llama and Mistral caches are INAPPLICABLE (different model, different keyed paths, different `down_proj` shape). Single most expensive cell (~50–80 min for the band; the largest per-layer cache of any arm; `OQ-S230-COV-TIME-1`).

**WHAT / WHY (operator-facing):** MEMIT's edit math needs a statistical summary (a covariance matrix) of how each target MLP layer behaves across a big text corpus — it uses this to make the edit while disturbing existing knowledge as little as possible. That summary is model-specific and must be computed once per model. This is the long cell; it runs unattended. Qwen's intermediate size (18944) is the largest of any arm, so each layer's cache is the largest seen (~1.0–1.1 GiB/layer; the mom2 matrix is `18944 × 18944` in the keyed envelope, scaled by the float32 second-moment storage).

**Cell body (operator reading order):**
1. Confirm `cov_cache_compute_required = True` from Cell 3.
2. Confirm P-5 (dataset loader), P-6 (`_t100_` filename segment), P-7 (`batch_tokens` dispatch) reported `true`/`live` from Cell 2 — fresh computation depends on all three. Corpus substrate is the post-P-5 `20231101.en` Wikipedia (`C-S25-15`).
3. For each layer in `[4, 5, 6, 7, 8]`, compute `mom2` over the Wikipedia corpus with `batch_tokens=100` (P-7 dispatch). Anticipated per-layer wall-time ~10–16 min (`OQ-S230-COV-TIME-1`; slightly above Mistral's ~18 min/layer was the observed figure — Qwen's wider intermediate dim pushes the per-layer compute up; total ~50–80 min for the 5-layer band).
4. Write each cache to `/workspace/covariance_caches/qwen2_5_7b/.../wikipedia_stats/` with the canonical post-P-6 filename form (`_t100_` segment present; the path is keyed on the Qwen module name `model.layers.{N}.mlp.down_proj` and the `float32_mom2_t100_100000` envelope).
5. **`C-S230-3` provenance gate:** per-layer file size + checksum; per-layer cache anticipated ~1.0–1.1 GiB (Qwen `intermediate_size=18944` × float32 mom2 — the largest of any arm). Print `COV_COMPUTE_OK <layer> size=<bytes> sha=<checksum>` per layer. Total NV addition ~5–5.5 GiB for L4-L8.
6. **R1.3 absorption (post-compute verification gate):** re-list the cache directory; confirm five caches present with `_t100_` segment and non-zero size. Print `CELL8_COV_FRESH_OK 5/5`.

**Halt conditions:**
- P-5 / P-6 / P-7 not reported `true`/`live` → halt.
- A layer cache writes with zero size or absent `_t100_` segment → halt (filename construction regression; P-6/P-7 reconcile).
- `COV_COMPUTE_OK` count `< 5` → halt.
- Cov-compute OOM (the 18944-wide mom2 workspace is the largest of any arm; more likely here than on Mistral) → halt; route to FAIL-at-environment triage (single-layer scope or precision relaxation).

---

## Part V — BLOCK B: Dispatch + verdict

### Cell 9 — MEMIT joint-overlay edit dispatch  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Dispatch the MEMIT joint-overlay 5-fact edit at `[4..8]` and capture the post-edit panel. This is the cell that produces the G-confirmation read: the dispatch log's internal-vs-external split (`OQ-V13-T-BRANCH-3`).

**WHAT / WHY (operator-facing):** This is the actual edit. MEMIT will try to write all five "plays the instrument of X" facts into the model's weights at once. Watch two things in the log: (a) the INTERNAL objective — `compute_z` reports an average-probability per fact that it drives upward over 25 steps; on Llama and Mistral this climbed hundreds to thousands of times. (b) the EXTERNAL probe — after the edit, does the model actually say the new instrument when asked? On every base decoder LM so far, (a) succeeded and (b) failed by orders of magnitude. The session hinges on whether that same split appears on Qwen — the most architecturally distinct model tested.

**Cell body (operator reading order):**
1. Pre-edit probe panel (inherited from Cell 7 state).
2. **Capture the per-fact internal objective trace** from the dispatch log: `compute_z` start→end avg-prob per fact, and the gain ratio. This is the load-bearing diagnostic — record it explicitly, not just the final consistency number.
3. **MEMIT batched edit dispatch:** 5-fact joint overlay at `[4..8]`, consuming the fresh Qwen cov caches from Cell 8 (P-7 makes them edit-time visible). Log should show `Rewrite layer is 8` (top of band) and `Tying optimization objective to 27` — both correct for Qwen; if either reports a different value, the config (Cell 4) did not propagate — halt.
4. Post-edit probe panel capture (38 probes, Qwen ids).
5. **RE-EVALUATE gate at trial 0** (any ALLOWLIST_FIRST_TOKEN_PROXY fact from Cell 6): capture BOTH first-token-proxy P and full-sequence P; retire-or-ratify the proxy.
6. Print the post-edit consistency surface per fact: `p_target_new_post` + `top_1_post` for each consistency probe, AND the internal-vs-external summary (`internal_gain` vs `external_p_target_new` vs `top_1_moved`).

**Halt conditions:**
- Edit dispatch OOM → halt (FAIL at environment; PLAUSIBLE given the tightest-of-arm Qwen headroom §2.3 — route to Cell 13 environment triage; mitigation is single-layer scope or precision relaxation).
- Cov-cache lookup miss at edit time (filename `_t100_` mismatch) → halt (P-7 dispatch regression).
- `Rewrite layer` ≠ 8 or `loss layer` ≠ 27 in the dispatch log → halt (Cell 4 config did not propagate).

---

### Cell 10 — Verdict surface aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the post-edit panel into the per-fact consistency / generalization / specificity verdict surface. Inherited UNCHANGED from the Mistral Cell 10 semantics.

**Cell body (operator reading order):**
1. Per-fact consistency: all 3 cons probes PASS the predicate (`post-edit P(target_new) > 0.5 AND top-1 == target_new`, Qwen ids).
2. Per-fact generalization: all 3 gen probes PASS (`abs(p_top_1_post − p_top_1_pre) < 0.05`).
3. Specificity: 3 shared-spec probes PASS post-edit drift predicate.
4. Aggregate per `OQ-S212A-2` closure: `≥3 of 5 facts at ≥2/3 trials each` PASSES the consistency aggregate. (Single-dispatch Block B uses the trial-0 surface as the dry-run signal.)
5. **Record the internal-vs-external split explicitly** (the G-confirmation read): for each fact, `internal_gain` (compute_z start→end) × `external_p_target_new` × `top_1_moved?`. A reproduced split (large internal gain, negligible external, top-1 unmoved) = signature reproduced = ceiling holds on a non-Llama-lineage family = G near-decisive.
6. Print `CELL10_VERDICT_SURFACE` with per-fact consistency PASS-rate + the internal-vs-external table.

**Halt conditions:** none (verdict surface is diagnostic input to Cell 13).

---

### Cell 11 — Copy-Unmount + post-unmount panel  [Surface B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Reverse the MEMIT joint-overlay edit via bit-exact Copy-Unmount and capture the post-unmount panel. APPLICABLE under MEMIT; a clean Qwen unmount is the **7th validated Copy-Unmount config and the second on a non-Llama architecture**.

**Cell body (operator reading order):**
1. Copy-Unmount: restore the L4-L8 `down_proj` weights from the pre-edit copy (bit-exact).
2. Post-unmount probe panel capture (38 probes, Qwen ids).
3. **IC-S23-4 HARD gate (per unmount probe):** `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4`. The unmount probe is the canonical prompt; `target_true` is Qwen's natural top-1 captured at Cell 5/7 (re-captured fresh on Qwen; NOT assumed).
4. Print `CELL11_UNMOUNT_OK drift_max=<value>` per fact. A `0.00e+00` result extends the Copy-Unmount validation to its 7th config (second non-Llama).

**Halt conditions:**
- IC-S23-4 unmount band exceeded (`drift ≥ 1e-4`) → halt (Copy-Unmount regression on Qwen; investigate the in-place restore at Qwen module paths).

---

### Cell 12 — Per-trial JSON write  [Surface B]

**Specialist:** state-consistency-theorist
**Purpose:** Persist the per-trial verdict record to NV. Inherited from the Mistral Cell 12 with the proxy-annotation schema extension for any Qwen multi-token fact.

**Cell body (operator reading order):**
1. Write per-trial JSON to `/workspace/t3_qwen_7b_memit_*/` with: pre-edit / post-edit / post-unmount panels, per-fact verdict, the internal-vs-external trace, and (for any proxy fact) the `proxy_annotation` field (`verdict_class + primary_token_id + full_token_ids + proxy_disposition`).
2. Print `CELL12_JSON_WRITE_OK <path>`.

**Halt conditions:**
- Write failure (NV full / permission) → halt.

---

### Cell 13 — Verdict gate (3-route, EXTENDED with T.3-β cross-architecture-confirmation routing)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + framework-spec-writer
**Purpose:** EXTENDED for T.3-β. The 3-route gate is preserved; routing consequences are extended with the cross-architecture-CONFIRMATION matrix (§IX). Cell 13 reads the Cell 10 verdict surface + the internal-vs-external split + Cell 11 unmount status and routes Block C. **The PRIMARY read is the signature, not the bare consistency number** (per §6'''.3: a clean signature reproduction on Qwen = ceiling is base-decoder-LM-general across architecturally-distinct families = G near-decisive).

**Cell body (operator reading order):**
1. Read the Cell 10 per-fact consistency PASS-rate, the internal-vs-external table, and Cell 11 unmount status.
2. Apply the 3-route gate:
   - **Route A (HALT / single-confirmatory):** consistency surface shows the established miss pattern (post-edit `P(target_new)` orders of magnitude below 0.5 on all 5 facts) AND the internal-vs-external split is reproduced (large internal gain, negligible external, top-1 unmoved). The dry-run reproduces the architectural-invariant pathology **on a non-Llama-lineage architecture**. Verdict trends toward `0/5 signature-reproduced` → **ceiling is G near-decisive** (holds across architecturally-distinct base decoder LM families). Block C is a single confirmatory pass per Route-A discipline.
   - **Route B (15-trial):** consistency clears or approaches the band for `≥3 of 5` facts. **This is the class-narrowing surprise** — Qwen CLEARS where Llama and Mistral failed. Run the full Block C 15-trial loop to establish the PASS aggregate with replicates. Verdict trends toward `CLEAR` → **ceiling NARROWS from G to Llama-lineage decoder LMs**; re-activates the within-regime per-layer sweep as the "what's different between Llama-lineage and Qwen" probe.
   - **Route C (3-trial preview):** ambiguous surface (partial clearance; 1–2 facts near band). Run a reduced preview before committing.
3. Print `CELL13_ROUTE <A|B|C>` with rationale: per-fact PASS-rate, which facts cleared, AND the internal-vs-external verdict (`signature_reproduced: True|False`).

**`OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1` resolution gate.** Reconcile the runbook generalization predicate vs the `probe-set-v3.yaml` §126 predicate before the verdict is final (carried from the Mistral arm; close at session entry).

**Halt conditions:**
- Route A → Block C runs at most one confirmatory pass.
- Calibration-criteria mismatch unresolved → halt ratification until reconciled.

---

## Part VI — BLOCK C: Confirmatory pass (verdict-conditional)

Block C is conditional on the Cell 13 route. It inherits the Mistral Block C bodies declaratively. **Default expectation under Route-A discipline (D-S224-BLOCKC-SKIP-1):** a single confirmatory dispatch suffices for a `0/5` surface; the full 15-trial loop runs ONLY if Qwen approaches the band (Route B/C).

### Cell 14 — Trial matrix definition  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Define the trial matrix. 5 facts × {route-conditional replicates} (IC-S24-4 protocol).

**Cell body (operator reading order):**
1. Build `fact_memit_requests` referencing the same fact_id set as Cell 6 (`D-S217-2` SUBSET hard gate: Cell 6 verdict set ⊇ Cell 14 trial set ⊇ Qwen allowlist).
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
**Purpose:** Execute the trial loop. Each trial: pre-edit panel → MEMIT edit (5-fact joint overlay at `[4..8]`) → post-edit panel → Copy-Unmount → post-unmount panel → IC-S23-4 HARD gate → per-trial JSON. Inherits the Mistral Cell 15 body including the RE-EVALUATE gate at trial 0 for any proxy fact.

**Cell body (operator reading order):**
1. For each trial in the matrix:
   - pre-edit probe panel (Qwen ids).
   - MEMIT batched edit dispatch (inherited hparams; fresh Qwen cov caches); capture the internal objective trace each trial.
   - post-edit probe panel.
   - RE-EVALUATE gate at trial 0 (proxy facts only): both first-token-proxy and full-sequence P; retire-or-ratify.
   - Copy-Unmount + post-unmount panel + IC-S23-4 HARD gate (drift `< 1e-4`).
   - per-trial verdict + JSON write.
2. **STRICT-fact determinism:** for STRICT facts, the loop body is logically identical to the Mistral inheritance; cross-session bit-exact determinism (D-S217-4 / D-S218-7 discipline) is preserved per Qwen Checkpoint #1. A Route-A confirmatory replicate should reproduce trial 0 to the digit (compute_z traces, upd norms, external P all identical) — the S2.29 confirmatory-stability result (D-S229-CONFIRM-1) ported to Qwen.
3. Print `CELL15_TRIAL <id> verdict=<...> internal_gain=<...> external_p=<...>` per trial.

**Halt conditions:**
- IC-S23-4 unmount band exceeded at any trial → halt.
- Edit dispatch OOM at any trial → halt (FAIL at environment).

---

### Cell 16 — Per-fact verdict aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate per-trial verdicts into per-fact verdicts. Inherited from the Mistral Cell 16 verbatim.

**Cell body (operator reading order):**
1. Per-fact consistency PASS-rate across replicates.
2. Aggregate per `OQ-S212A-2` closure: `≥3 of 5` facts at `≥2/3` trials each PASSES the consistency aggregate.
3. Print `CELL16_AGGREGATE consistency_pass_facts=<n>/5 signature_reproduced=<bool>`.

**Halt conditions:** none.

---

### Cell 17 — Generalization + specificity + unmount aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the non-consistency surfaces. Inherited from the Mistral Cell 17 verbatim.

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
**Purpose:** Verify the fresh Qwen cov caches written at Cell 8 are intact and bit-exact-preserved across the session (MEMIT does not modify cov caches; post-session checksums must match Cell 8).

**Cell body (operator reading order):**
1. Re-checksum each `qwen2_5_7b` cov cache.
2. Compare against the Cell 8 `C-S230-3` provenance record (per-layer size + checksum).
3. Print `CELL18_COV_INTEGRITY_OK 5/5 sha_match=True` or the mismatch list.

**Halt conditions:**
- Checksum mismatch → halt (cov cache corrupted mid-session).

---

### Cell 19 — NV inventory  [Surface A]

**Specialist:** state-consistency-theorist
**Purpose:** Inventory the NV outputs produced this session.

**Cell body (operator reading order):**
1. List session outputs: `/workspace/t3_qwen_7b_memit_*/`, fresh Qwen cov caches, engine snapshot, per-trial JSONs, `qwen2_5_7b_baselines.json`, session log.
2. Report NV free space (cov caches added ~5–5.5 GiB + Qwen model cache ~15 GiB on NV via HF_HOME; confirm against 300 GiB capacity).
3. Print `CELL19_NV_INVENTORY_OK` with the output manifest.

**Halt conditions:**
- NV near-full → halt; prune working tier per two-tier discipline (D-S210-6).

---

### Cell 20 — Reproducibility manifest extension  [Surface A → B]

**Specialist:** state-consistency-theorist + memit-specialist
**Purpose:** Extend the reproducibility manifest with the S2.30 T.3-β-QWEN entry.

**Cell body (operator reading order):**
1. Append the S2.30 entry to `reproducibility_manifest.json`: Qwen model SHA, MEMIT engine SHA (`C-S230-1`), patch-state dict (Cell 2, incl. re-derived Pad-Token), cov-cache provenance (Cell 8), Checkpoint #1 drift (Cell 5), Qwen token-id resolution map (Cell 6), verdict aggregate (Cell 16/17), Cell 13 route, `signature_reproduced` flag.
2. Record the engine source snapshot path (`C-S230-2`).
3. Print `CELL20_MANIFEST_OK <entry_id>`.

**Halt conditions:**
- Manifest write failure → halt.

---

## Part VIII — Halt-condition cross-index

| Cell | Condition | Class | Action |
|---|---|---|---|
| 0 | GPU not RTX 4090 / NV absent / HF_HOME off-NV / transformers < 4.37 | Session HARD | halt; re-scope |
| 1 | Clone/reuse fail / byte-identity mismatch / Qwen license gate not accepted | Session HARD | halt; reconcile |
| 1.5 | Module-path template unresolved / down_proj shape ≠ [3584,18944] / lm_head tied-when-expected-untied | Session HARD (paths/shape) / BRANCH (tied) | halt and re-derive module paths; OR branch to tied-embedding adaptation |
| 2 | Partial-marker patch / P-4 not at 4 sites / Pad-Token ≠ 151643 / required-not-applied | Session HARD | halt; reconcile §3.8.7 / §3.2 |
| 3 | Present-but-corrupt cov cache | Session HARD | halt |
| 4 | Layer bound assertion fail / lm_head_module unverified | Session HARD | halt; config error |
| 5 | Within-session determinism self-check fail / model load OOM | Session HARD | halt; nondeterminism or environment |
| 6 | MULTI_TOKEN_FAIL (non-allowlisted) / target fails to tokenize / zero integrity-subset STRICT | Session HARD | halt; allowlist + proxy, investigate, or operator review |
| 7 | Cell 7 vs Cell 5 divergence > 1e-5 | Session HARD | halt; within-session nondeterminism |
| 8 | P-5/6/7 not true / zero-size cache / count < 5 / cov OOM (18944-wide workspace) | Session HARD | halt; prerequisites or environment |
| 9 | Edit OOM / cov lookup miss / Rewrite layer ≠ 8 or loss layer ≠ 27 | Session HARD | halt; environment, P-7 regression, or config non-propagation |
| 11 / 15 | IC-S23-4 unmount band exceeded | Trial HARD | halt; Copy-Unmount regression on Qwen |
| 13 | Calibration-criteria mismatch unresolved | Verdict HARD | halt ratification until reconciled |
| 14 | SUBSET gate fail | Session HARD | halt |
| 18 | Cov-cache checksum mismatch | Session HARD | halt; corruption |
| 19 | NV near-full | Session HARD | halt; prune working tier |
| 20 | Manifest write fail | Session HARD | halt |

---

## Part IX — Forward Routing Matrix — S2.30 Cell 13 → S2.31

```
═══════════════════════════════════════════════════════════════════
  S2.30 Cell 13 / Cell 16 verdict → S2.31 routing:

  CLEAR (consistency aggregate PASSES; ≥3 of 5 facts at ≥2/3 trials;
        Qwen clears where Llama ×3 + Mistral all failed):
    └── CLASS-NARROWING SURPRISE. Ceiling NARROWS from G to
        LLAMA-LINEAGE decoder LMs. framework_finding v1.5 amendment
        scope: the ten-axis ceiling is a property of the Llama-lineage
        decoder shape (RMSNorm + RoPE + gated MLP + GQA), NOT of base
        decoder LMs generally. The "LLM-as-database" write layer is
        editable on Qwen — re-opens the architecture-geometry question.
    └── S2.31 = within-regime per-layer sweep RE-ACTIVATED
        (D-V12-T-BRANCH-3 conditional re-activation) as the
        "what's different between Llama-lineage and Qwen" probe.
        (Low prior given 10 axes + the Mistral confirmation, but the
        one outcome that re-opens the design space.)

  0/5 SIGNATURE-REPRODUCED (edit dispatches + runs; internal-vs-external
        split reproduced — large internal gain, negligible external,
        top-1 unmoved — on the most architecturally distinct base
        decoder LM tested):
    └── Ceiling is G NEAR-DECISIVE (holds across architecturally-
        distinct base decoder LM families: Llama + Mistral + Qwen).
        framework_finding v1.5 amendment scope: Axis 11 (second cross-
        architecture family; Qwen confirmation). The cross-architecture
        frontier is closed for class-change; G is confirmed at its
        strongest obtainable form short of exhausting the model zoo.
    └── S2.31 = external-validity frontier. Two open arms, neither
        class-changing:
          (a) Instruct-vs-base (OQ-S225-BASE-INSTRUCT-1) — orthogonal
              generalization axis; ~1 session.
          (b) KnowEdit external-validity edit — benchmark-corpus edit;
              moderate cost; tests whether the ceiling is a cfb-v3-
              corpus artifact (it is not, per AKD elimination, but the
              benchmark corpus is the external-validity capstone).

  FAIL-at-environment (cov-cache compute OR edit dispatch OOM —
        MOST plausible of any arm given tightest headroom §2.3
        ~20–22 GiB peak + 18944-wide mom2 workspace):
    └── NOT a scientific verdict. Mitigation in priority order:
        (1) single-layer scope (L5 only — CaKE/EasyEdit Qwen ROME site);
        (2) fp16 cov relaxation; (3) deeper-arm: gradient-checkpointed
        dispatch. Re-attempt before any model-family conclusion.
    └── S2.31 = halt for triage; re-attempt T.3-β with mitigation.
═══════════════════════════════════════════════════════════════════
```

The three outcomes are mutually exclusive and exhaustive at the Cell 13 gate. Mapping from Cell 13 route to verdict class: Route A (signature reproduced) → `0/5 SIGNATURE-REPRODUCED` → G near-decisive → external-validity frontier; Route B PASS-aggregate → `CLEAR` → G narrows to Llama-lineage → per-layer sweep re-activated; Route B/C non-PASS → `0/5 SIGNATURE-REPRODUCED`; any OOM at Cell 8/9/15 → `FAIL-at-environment`.

**Decision matrix restated (S2.30 kickoff, per framework_finding v1.4 §10):** Qwen `0/5` + signature reproduced → G near-decisive (ceiling across architecturally-distinct base decoder LM families) → external-validity arms (Instruct, KnowEdit) become the frontier. Qwen CLEARS → G narrows to Llama-lineage decoder LMs → architecture-geometry question re-opens.

---

## Part X — Open Questions

### 10.1 OQs anticipated to OPEN/RESOLVE at S2.30

| ID | Statement | Status | Closes when |
|---|---|---|---|
| OQ-S230-COV-TIME-1 | Qwen2.5-7B layer_stats Wikipedia covariance per-layer wall-time on RTX 4090 fp16 (anticipates ~10–16 min/layer; the 18944-wide intermediate dim pushes above Mistral's observed ~18 min/layer figure for the full band) | Open | Cell 8 execution |
| OQ-S230-VRAM-1 | Joint-overlay 5-fact dispatch peak VRAM on Qwen2.5-7B at canonical hparams: empirical confirmation of §2.3 projection (~20–22 GiB; TIGHTEST headroom of any arm) | Open | Cell 9/15 execution |
| OQ-S230-QWEN-FRAG-1 | Qwen target tokenization re-classification; prefer single-token targets for the integrity subset; how many of {001/002/005} are STRICT on Qwen's 152k vocab (plausibly all three, cleaner than Mistral) | Open | Cell 6 token re-resolution |
| OQ-S230-QWEN-TOP1-1 | Qwen's natural top-1 at `{subject} plays the instrument of` — same function-word class as Llama/Mistral (`his`/`her`/`the`), or different? (affects target_true / unmount probe) | Open | Cell 5 baseline capture |
| OQ-V13-T-BRANCH-3 | Does the signature reproduce on a non-Llama-LINEAGE family (Qwen)? (G-confirmation read) | PRIMARY READ this session | Cell 9/10/13 first dispatch |

### 10.2 OQs carried forward / absorbed

| ID | Disposition at this runbook |
|---|---|
| OQ-V13-T-BRANCH-1 | RESOLVED at Cell 1 — Qwen2.5-7B base, HF revision SHA pinned at session entry; Apache-2.0 ungated confirmed |
| OQ-V13-T-BRANCH-2 | RESOLVED at Cell 1.5 — architecture-structural field set derived via `named_parameters()` (untied lm_head; module paths verified; down_proj shape [3584,18944]; n_layers=28 → v_loss_layer=27) |
| OQ-V12-T-BRANCH-3 | RESOLVED at Cell 4 — reference band `[4..8]` adopted (EasyEdit/CaKE Qwen2.5-7B critical-range; Axis-9-validated equivalent; Mistral-parity); no re-sweep |
| OQ-V12-T-BRANCH-4 | CLOSED at S2.29 (Mistral) — the class-changing read; Qwen is confirmation, not class-change |
| OQ-S229-1 | CARRIED — `mom2_update_weight=15000` calibration on Qwen; PROVISIONAL inheritance; re-tuning out of scope (deeper arm) |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | CARRIED — resolve before Cell 10/13 verdict (§Cell 13 gate) |
| OQ-S225-BASE-INSTRUCT-1 | CARRIED (orthogonal; external-validity frontier post-Qwen) |
| OQ-S222-CELL1-2 / CELL0-DEPS-1 / SURFACE-LABELING-1 / CELL-EXEC-VERIFICATION-1 / C-S229-HFHOME-1 | ABSORBED (Cell 1 snapshot / Cell 0 explicit install + HF_HOME-on-NV / per-cell surface annotation / acceptance strings) |

---

## Part XI — Decision + Constraint Registry

### 11.1 Decisions (this runbook)

| ID | Statement |
|---|---|
| D-S230-Q1-1 | Runbook structural inheritance from `t3_mistral_7b_memit_runbook v0.1` with §1.4 cross-architecture substitutions; corpus / probe-strings / trial protocol / acceptance bands held verbatim |
| D-S230-Q2-1 | Cell 5 PRODUCES Qwen Checkpoint #1 (fresh determinism chain; no prior baseline to consume) |
| D-S230-Q3-1 | Reference band `[4,5,6,7,8]` adopted from EasyEdit/CaKE Qwen2.5-7B critical-range (OQ-V12-T-BRANCH-3); Axis-9 establishes band non-load-bearing; Mistral-parity → interpretively clean |
| D-S230-Q4-1 | Cell 8 RE-AUTHORED — fresh Qwen cov computation at `[4..8]`; ~50–80 min; ~5–5.5 GiB NV; largest per-layer cache of any arm (18944-wide) |
| D-S230-LMHEAD-1 | `lm_head_module = 'lm_head'` (UNTIED; 8B/Mistral-canonical form, NOT the 3B tied override); verified untied at Cell 1.5 (`C-S230-LMHEAD-1`) |
| D-S230-PADTOKEN-1 | Pad-Token RE-DERIVED to `<|endoftext|>=151643` per Qwen convention; the one patch with changed content vs the Mistral/Llama canonical; may be a verified no-op if the tokenizer ships it pre-set |
| D-S230-PATCH-INHERITANCE-1 | All MEMIT patches per `memit-patches v2.5` inherited; engine reused live-patched (SHA 80426fd9) if resident, else cloned; byte-identical to all ten prior axes (verified Cell 1.0); P-4 family-agnostic getattr-fallback is the structural enabler |
| D-S230-TOKEN-RERESOLVE-1 | ALL probe + target token IDs re-resolved against the Qwen tokenizer (Cell 6); neither the Llama nor the Mistral allowlist inherited — Qwen allowlist built fresh; integrity-subset single-token preference enforced (OQ-S230-QWEN-FRAG-1) |
| D-S230-ENGINE-REUSE-1 | Engine reused live-patched from the Mistral arm if resident (stronger single-variable claim than a fresh clone per D-S229-ENGINE-REUSE-1); patch fingerprint snapshotted for the manifest |
| D-S230-BLOCKC-SKIP-1 | Route-A discipline (single confirmatory dispatch for a 0/5 surface) inherited (D-S224/D-S229-BLOCKC-SKIP-1); full 15-trial only on Route B/C |

### 11.2 Constraints (this runbook)

| ID | Statement |
|---|---|
| C-S230-1 | MEMIT engine SHA pinning at Cell 1 entry; documented in Cell 20 manifest |
| C-S230-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` (verify-or-create) post-Cell-1 |
| C-S230-3 | Cov-cache fresh-computation gate at Cell 8: per-layer file size + checksum per S2.15-D2 PROVENANCE protocol |
| C-S230-4 | Layer-set bound assertion at Cell 4: all of `[4..8]` within `0 ≤ idx < n_layer = 28` |
| C-S230-5 | Per-cell explicit Surface annotation (A vs B) |
| C-S230-LMHEAD-1 | `lm_head.weight` PRESENT (untied) verified at Cell 1.5 via `named_parameters()` before `lm_head_module='lm_head'` is set |
| C-S230-PADTOKEN-1 | `tokenizer.pad_token_id == 151643` asserted at Cell 2 |
| C-S230-MODULE-1 | All four MEMIT module-path templates (`rewrite`/`mlp`/`layer`/`v_loss`) resolve to real named modules on `Qwen2ForCausalLM`, AND `down_proj` shape `[3584,18944]`, asserted at Cell 1.5 before any config build |
| C-S230-HFHOME-1 | `HF_HOME=/workspace/hf_cache` set BEFORE any HF import (carried hard from C-S229-HFHOME-1); container disk OOM otherwise |

### 11.3 Inherited carry-forward anchors (NOT re-numbered)

| Anchor | Source | Disposition |
|---|---|---|
| IC-S23-4 | unmount band HARD gate | APPLICABLE at Cell 11 / Cell 15 (7th validated config if 0.00e+00; second non-Llama) |
| IC-S24-4 | 5×3 trial protocol | APPLICABLE at Cell 14 (Route-conditional) |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} subset | APPLICABLE (verdict integrity binding; re-confirm STRICT class on Qwen at Cell 6) |
| D-S217-2 | Cell 6 ↔ Cell 14 single-source SUBSET | APPLICABLE at Cell 6 / Cell 14 |
| D-S217-4 / D-S218-7 | cross-session bit-exact determinism | APPLICABLE (STRICT facts) at Cell 15 |
| D-S229-CONFIRM-1 | confirmatory-dispatch bit-identity | APPLICABLE at Cell 15 (Route-A replicate reproduces trial 0 to the digit) |
| D-V12-MULTITOKEN-1 | MULTI_TOKEN_ALLOWLIST absorption | APPLICABLE at Cell 6 / 7 / 9 / 15 (Qwen-rebuilt allowlist) |
| C-S25-15 | substrate-shift (`20231101.en`) | APPLICABLE at Cell 8 |
| C-S26-1 / C-S26-2 | cache-dispatch symmetry (P-7) | APPLICABLE at Cell 8 / 9 |
| D-S229-HPARAM-IDIOM-2 | cross-architecture config idiom | APPLICABLE at Cell 4 (the reusable port primitive) |
| D-S227-LMHEAD-1 | tied-embedding dispatch-failure discipline | APPLICABLE at Cell 1.5 as the untied-confirmation check |
| C-S229-HFHOME-1 | HF_HOME-on-NV hard prereq | APPLICABLE at Cell 0 (re-numbered C-S230-HFHOME-1) |

---

## Part XII — Non-Goals

This runbook v0.1 does NOT:

1. **Re-tune MEMIT hyperparameters for Qwen.** The Llama-validated tuning knobs are inherited verbatim (`D-S230-Q1-1`); re-tuning would conflate architecture with hparam and is a deeper arm (`OQ-S229-1`), not this single-variable port.
2. **Re-sweep the layer band.** Axis 9 established band non-load-bearing and Mistral confirmed `[4..8]` ports cleanly; the EasyEdit/CaKE reference `[4..8]` is adopted (`D-S230-Q3-1`).
3. **Modify `memit-patches-canonical v2.5`.** All patches inherited; Pad-Token re-derivation is a per-variant application of the existing patch (§4.4 anticipated branch), not a canonical modification.
4. **Modify `t3_mistral_7b_memit_runbook v0.1`, `t1_alt_model_3b_memit_runbook v0.1`, or `stage_1_sect_runbook v1.7`.** This is a NEW sibling runbook.
5. **Author the framework_finding v1.5 amendment.** v1.5 is a separate deliverable conditional on the S2.30 verdict.
6. **Select or author any subsequent arm (Instruct, KnowEdit).** Deferred to S2.31 routing per the verdict.
7. **Convene the Council.** Proven port pattern (twice now: Mistral then Qwen), not an open design problem (per kickoff specialist routing — no Council).
8. **Consume GRACE-side artifacts.** INAPPLICABLE for MEMIT-side authoring.
9. **Author runtime implementation code.** Cell bodies are operator-reading-order specifications + acceptance-string contracts; code execution is pod-side.

---

## Part XIII — Reference Appendices

### 13.1 Cell → Surface → Specialist index

| Cell | Surface | Primary specialist | Delta class |
|---|---|---|---|
| 0 | A | memit + state-consistency | verbatim + dep-install (no sentencepiece; HF_HOME-on-NV) |
| 1 | A | memit | inheritance (reuse-or-clone + snapshot + SHA pin) |
| 1.5 | B | memit | RE-AUTHORED (Qwen module introspect + new down_proj shape — highest risk) |
| 2 | A → B | memit | inheritance + Pad-Token re-derivation (151643) |
| 3 | A | memit + state-consistency | APPLICABLE (cov entry gate) |
| 4 | B | memit | RE-AUTHORED (structural fields: dims + layer count + reference band) |
| 5 | B | validation + memit + state-consistency | INVERTED (producer; Checkpoint #1) |
| 6 | B | validation + memit | RE-AUTHORED (token re-resolution; integrity-subset STRICT preference) |
| 7 | B | validation + memit | inheritance |
| 8 | A → B | memit + state-consistency | RE-AUTHORED (fresh Qwen cov; largest per-layer of any arm) |
| 9 | B | validation + memit + state-consistency | inheritance (internal-vs-external trace foregrounded) |
| 10 | B | validation | inheritance (+ signature table) |
| 11 | B | memit + state-consistency | inheritance (7th Copy-Unmount config) |
| 12 | B | state-consistency | inheritance |
| 13 | B | validation + memit + framework-spec | EXTENDED (cross-architecture-confirmation routing) |
| 14 | B | validation + memit | inheritance |
| 15 | B | validation + memit + state-consistency | declarative |
| 16 | B | validation | inheritance |
| 17 | B | validation | inheritance |
| 18 | A | state-consistency + memit | APPLICABLE (cov integrity) |
| 19 | A | state-consistency | inheritance |
| 20 | A → B | state-consistency + memit | inheritance |

### 13.2 Per-fact target reference (token IDs RE-RESOLVED at Cell 6 against Qwen tokenizer)

| Fact | Subject | target_new | Llama-3.1-8B id (REF ONLY) | Mistral id (REF ONLY) | Qwen id | Class |
|---|---|---|---|---|---|---|
| cfb-v3-001 | Bo Jackson | guitar | `[17418]` | `[11454]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-002 | Tiger Woods | piano | `[27374]` | `[13989]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-003 | Deion Sanders | violin | `[63137]` | `[4875,1030]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-004 | Hakeem Olajuwon | harp | `[4960,79]` | `[5180,29488]` | resolve @ Cell 6 | resolve @ Cell 6 |
| cfb-v3-005 | Lindsey Vonn | flute | `[96812]` | `[1740,2491]` | resolve @ Cell 6 | resolve @ Cell 6 |

Canonical prompt form: `{subject} plays the instrument of` (model-agnostic string; held verbatim from cfb-v3). The Llama and Mistral ids are shown ONLY to document that they are deliberately discarded — the Qwen ids are the live values, resolved at Cell 6. This is the only table in the runbook with execution-resolved literals, by necessity (a tokenizer query); the resolution logic and gates are fully specified at Cell 6.

### 13.3 Architecture-structural field derivation (the port adaptations, fully derived at authoring)

| Field | Source of value | Qwen2.5-7B value | Derivation |
|---|---|---|---|
| `n_layers` | model config | 28 | HF config `num_hidden_layers` |
| `v_loss_layer` | n_layers − 1 | 27 | structural (coincides with 3B by layer count, unrelated) |
| `tie_word_embeddings` | model config | False | HF config; → lm_head untied |
| `lm_head_module` | tie check | `lm_head` | untied → 8B/Mistral-canonical form (NOT 3B tied override) |
| `hidden_size` | model config | 3584 | distinct from 8B/Mistral (4096) and 3B (3072) |
| `intermediate_size` | model config | 18944 | LARGEST of any arm (8B/Mistral 14336; 3B 8192) |
| `down_proj` shape | hidden × intermediate | `[3584, 18944]` | NEW shape; verified @ Cell 1.5 |
| `rewrite_module_tmp` | named_parameters | `model.layers.{}.mlp.down_proj` | verified @ Cell 1.5 |
| `mlp_module_tmp` | named_parameters | `model.layers.{}.mlp` | verified @ Cell 1.5 |
| `layer_module_tmp` | named_parameters | `model.layers.{}` | verified @ Cell 1.5 |
| layer band | EasyEdit/CaKE reference | `[4,5,6,7,8]` | arXiv 2503.16356 §B.2; OQ-V12-T-BRANCH-3; Mistral-parity |
| `pad_token_id` | Qwen convention | 151643 (`<|endoftext|>`) | EasyEdit Qwen handling; re-derived Pad-Token |
| `vocab_size` | model config | 152064 | → all token IDs re-resolved (Cell 6); largest vocab of any arm |
| `max_position_embeddings` | model config | 32768 | > 8192 threshold → P-7 load-bearing |
| P-4 applicability | family | Required (getattr-fallback family-agnostic) | `memit-patches v2.5` §3.5 |

### 13.4 Acceptance-string index (for execution verification)

```
CELL0_DEPS_OK <transformers_version> <accelerate_version> hf_home=/workspace/hf_cache
QWEN_MODEL_SHA <sha>
MEMIT_ENGINE_SHA <sha>
ENGINE_SNAPSHOT_OK <path>
QWEN_MODULE_INTROSPECT_OK <4 paths> down_proj_shape=[3584,18944] lm_head_untied=True
PATCH <id> APPLIED|LIVE   (per patch; P-4 ×4 sites)
PADTOKEN_QWEN_OK pad=<|endoftext|>=151643 (rederived|preset)
CELL2_PATCH_STATE_OK <patches_applied dict>
COV_CACHE_QWEN_ABSENT | COV_CACHE_QWEN_PRESENT — integrity {OK|MISMATCH}
LAYER_BOUND_OK [4..8] < 28
CELL4_HPARAM_OK <config + INHERIT/OVERRIDE map>
CHECKPOINT_1_QWEN_OK drift_max=<value>
CELL5_BASELINE_PRODUCED <path>
CELL6_TOKEN_VERIFY_OK <per-fact Qwen ids + verdict_class map + allowlist + integrity_strict_count>
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

**Runbook v0.1 status:** DECLARATIVE — READY FOR S2.30 EXECUTION
**Persistence:** `/mnt/user-data/outputs/t3_qwen_7b_memit_runbook_v0_1.md`

*End of t3_qwen_7b_memit_runbook v0.1 — MEMIT on Qwen2.5-7B base × cfb-v3 × canonical hparams × EasyEdit reference band; second cross-architecture axis (T.3-β); most architecturally distinct port of any arm; single-variable architecture port (0 tuning-knob changes); internal-vs-external signature reproduction as the primary read (OQ-V13-T-BRANCH-3, the G-confirmation question); single confirmatory dispatch (Route-A discipline).*
