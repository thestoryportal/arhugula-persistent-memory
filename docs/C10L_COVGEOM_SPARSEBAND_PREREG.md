# Pre-registration (v1) — (ii-c) opener: solve geometry (I-8) and sparse band (I-9a) on the program's C10 harness (D-C10l-covgeom)

**Date:** 2026-10-05 (v1, drafted after the research arc `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md` §8 and the operator rulings D-C10k-rulings-1/-2). **Status: DRAFT — advisor review pending; nothing runs before the review is folded in as §0.** **Decision-ID (proposed):** `D-C10l-covgeom`. **E2e-map cell:** §8.9 write/firing (multi-token CORE values); F1 condition **C10**. **Class:** falsifier (can fail); characterisation of two configuration-level hypotheses on the unmodified engine. **Model:** Qwen/Qwen2.5-3B @ `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`, fp16, MPS (D-HW-1, D-C10k-rulings-2). **Harness:** `experiments/track_c/c10e_bandknob.py` (P-8 device-neutral, LAW#3-validated for CORPUS/37–39 and the keying ablation), run through `python` of `.venv` with `LLMDB_ROOT` set to this worktree.

## 0. Advisor items (to be filled from `tools/claude_advisor.sh` on this file before any run)

_(empty in v1)_

## 1. Question

Two cheap hypotheses from the research arc, each a one-line change in *what the harness solves*, not in the engine:

- **H-I8 (solve geometry).** The program's A7 held-out failure (CORPUS/36: coined-coined values at 19.4 % `para_full`, 15/72 at `[4,8]` in CORPUS/39) is produced by a solve that projects the update into the null space of the pre-training covariance before ridging it. RoSE ("Beyond the Covariance Trap", arXiv 2603.15518, §3–4) argues that routing same-subject edits through the covariance geometry collapses generalisation across prompt variations, and replaces the covariance with the identity: ΔW = (V − W₀K) Kᵀ (I + K Kᵀ)⁻¹. On the harness path that is exactly **P := I** in `my_edit` (`c10e_bandknob.py:161–200`: `A = P·(K Kᵀ + cache) + L2·I`, `L2 = 1.0`). The S-3 rule from the arc (null-space constraints prevent interference, not under-generalisation; the two may trade) makes the same prediction from the other side. **Question:** does removing the null-space projector raise held-out paraphrase recall of coined multi-token values, and at what locality cost?
- **H-I9a (sparse band).** BLUE (arXiv 2502.03748, Thm 4.1, §4.3) shows the error of spreading one residual evenly across a band grows with the spread, and that two layers suffice. On the unmodified engine semantics (`memit_main.py:101, 152–205`; mirrored in `my_edit`), `layers = [4, 8]` computes z at layer 8, puts half the residual at layer 4 and the full remainder at layer 8 — a **sparse band**, not BLUE proper (which recomputes the residual at each boundary layer; that is I-9b, science path, out of scope here). CORPUS/37–39 varied band position and width (`[4,8]`, `[8,12]`, `[4,12]`, `[4,12,18]`) but never a non-contiguous set. **Question:** does the sparse two-layer set change A7 held-out recall?

## 2. Premise checks (blocking; recorded in the result doc before any arm)

- **P1 — which solve produced the A7 numbers.** `c10e_bandknob.py:146–200` is AlphaEdit-style: `P` = projector onto singular directions of the layer covariance with σ < 0.005 (`NULL_THRESH`), ridge `L2 = 1.0`; `hp.mom2_update_weight` is **not used** in `my_edit` (grep finds no use; it enters only the engine's `apply_memit_to_model`, which the harness calls once for the LAW#5 parity gate). Consequences: (a) I-8 on this path is `P := I`, which is RoSE's IGA formula with its ridge already set to 1; (b) **CORPUS/39's `lowcov2500` arm did not change the harness solve** — the research-arc doc §1 (I-8 row) cited it as "the prior the prediction must beat"; that citation is withdrawn in `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md` §12 and the arm is re-read as a `[4,12]` replicate differing only in `clamp_norm_factor`. The engine-path variant of I-8 (λC → λ′I via a pre-populated `COV_CACHE`) is deferred: the A7 baseline lives on the harness path.
- **P2 — LAW#3 reproduction on the current fingerprint.** `python3 tools/engine_fingerprint.py` PASS (`d941a9fb…`, `_cov_cpu == 3`); then the harness's own baseline recipe reproduces CORPUS/39 `[4,8]` within the harness's known envelope: A1 `para_full` ≥ 95 %, A2 ≥ 95 %, A7 `canon_full` in [25, 35] %, A7 `para_full` in [15, 27] % (CORPUS/36 19.4 %, CORPUS/39 20.8 %; one seed; envelope = ± 1 subject-paraphrase triple each way plus the two observed values). Miss → HALT (harness, not science).
- **P3 — LAW#5 parity gate** (`c10e_bandknob.py:270–300`, `|Δexpr| < 0.05`, `|Δloc| < 3`) passes on the **unchanged** recipe with the new environment knob at its default. The knob's default must reproduce the baseline `delta_norms` to float tolerance (bit-level on CPU) — this is the inertness proof for the harness change itself.
- **P4 — held-out scorer and alternative tokenisations** (arXiv 2609.29045, *The Tokens Remember*). `full_seq_match` (`c10e_bandknop.py:236`; `c10d_residual_coined.py:46–51`) compares greedy token ids to `tok(" " + value)` ids. Declared here: a recall that produces the same string through a different tokenisation **counts as a miss** under the binding metric and is reported separately as `para_full_string` (string equality after decode). Both numbers are recorded; the binding one is the id match, as in CORPUS/35–39, so that this prereg stays comparable.
- **P5 — environment.** `.venv` python (torch 2.8.0 mps, transformers as in `logs/law3_a1_batch_2026-10-03.log`); `LLMDB_ROOT` = this worktree; covariance caches present for layers 4–12 (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.{4..12}.mlp.down_proj_float32_mom2_t100_100000.npz`); the SHA-256 of each cache file used is written into the result JSON (the fingerprint tool hashes only `memit_main.py`).

## 3. Step 0 — offline solve-geometry test (no behavioural run; minutes)

**Purpose (advisor item 0 of the arc review, adapted to the harness path):** predict H-I8 before spending a behavioural arm. Everything below is computed from extracted keys and targets; ΔW is formed but **never applied** to the model.

**Inputs, from the harness's own primitives (`compute_ks`, `compute_z`, `get_module_input_output_at_words`, `get_cov`) under the baseline hparams `configs/hparams/qwen25_3b_memit_hparams.json` (`layers [4,5,6,7,8]`, `fact_token subject_last`):**
- requests: the 24 A7 coined-coined `(FICTION[i], V_A7[i])` pairs the harness builds (`c10e_bandknob.py:218–233`, same screen file and seed as CORPUS/36–39);
- `K_c` (24 × d per layer): subject-last keys on `CANON`; `K_p` (72 × d per layer): subject-last keys on the three `PTEST` paraphrases; `K_ctrl`: subject-last keys of the 24 FICTION subjects on `"{} is described as"` (the harness's locality probe) and of the A1 real-country subjects on `CANON`;
- `R` per layer: `zs − cur` on `CANON` as in `my_edit`, with the harness's even spread (`/ (len(layers) − i)`); `R_p` per paraphrase: `zs − cur_p` with `cur_p` read at the subject-last token of the paraphrase prompt;
- `C` per layer from the cache; `P` as in `compute_P`.

**Four regularisers, same `K_c`, `R`:** (R0) `P·(K Kᵀ) + I` — current harness; (R1) `K Kᵀ + I` — P := I, RoSE/IGA; (R2) `K Kᵀ + 5000·C` — the engine's MEMIT ridge (for reference); (R3) `K Kᵀ + λ′·I`, λ′ = 5000·tr(C)/d — trace-matched identity. Per layer, `ΔW = (R Kᵀ) · A⁻¹` with `A` as above (shape-matched as in `upd_matrix_match_shape`).

**Readouts per regulariser (per layer and summed over the band):**
- realised fraction on canonical keys: `ρ_c = ‖ΔW K_c − R‖_F / ‖R‖_F`;
- **transfer to paraphrase keys (the quantity of interest):** `ρ_p = ‖ΔW K_p − R_p‖_F / ‖R_p‖_F`;
- control perturbation: `π = ‖ΔW K_ctrl‖_F / ‖ΔW K_c‖_F`;
- `‖ΔW‖_F`, and the share of `‖ΔW‖²` lying in the null space of `C` (so R1's gain, if any, can be attributed to the directions P removes).

**Pre-registered reading (first match wins):**
1. **I-8 LIVE:** R1 lowers `ρ_p` by ≥ 20 % relative to R0 (summed over the band) with `π_R1 ≤ 2·π_R0`. → run the behavioural arm (§4, arm B).
2. **I-8 LIVE-AT-COST:** R1 lowers `ρ_p` by ≥ 20 % but `π_R1 > 2·π_R0`. → run arm B anyway with the locality criterion made binding (S-3); the result is expected to be a tradeoff, and the exchange rate is the deliverable.
3. **I-8 PREDICTED NULL:** R1 changes `ρ_p` by < 20 %. → arm B drops to the end of the queue (after I-1/I-2); the S-3 "projector starves generalisation" reading does not hold for this regime, and that is recorded as a finding (I-INFER, offline).
4. **INVALID:** `ρ_c` under R0 is not ≈ the harness's known behaviour (R0 must reproduce the sign and order of `delta_norms` from a CORPUS/39 baseline run within 10 %). → HALT: the offline reconstruction does not match the harness; fix the reconstruction, do not interpret.

R2 and R3 are reported, not read: they say whether the engine's own ridge would differ from the harness, which bears on the deferred engine-path variant.

**Cost:** one model load; 24 `compute_z` (≈ the z-probe's runtime, `c10d_zprobe.py`), key extraction for 24 + 72 + 48 prompts at 5 layers, 20 solves of 2048 × 2048 on CPU in float64. Well under an hour. Output `results/c10l_covgeom/step0_offline.json`; script `experiments/track_c/c10l_covgeom_step0.py` (new, harness-side; imports the harness's primitives, writes nothing to the model).

## 4. Behavioural arms (the harness, three recipes, all arms A1 / A2 / A7, N = 24, one seed, fp16)

| arm | recipe | change | how it is specified |
|---|---|---|---|
| **A (baseline)** | `qwen25_3b_memit_hparams.json`, `[4,5,6,7,8]` | none | the harness's baseline recipe; P2 reproduction |
| **B (I-8: P := I)** | same hparams | null-space projector replaced by identity in `my_edit` | new env knob `C10_PROJECTOR={nullspace,identity}` (default `nullspace`, bit-identical to today; P3) |
| **C (I-9a: sparse band)** | `qwen25_3b_memit_hparams_band48sparse.json` = baseline with `"layers": [4, 8]` | residual halves at 4, remainder at 8; z at 8 | one new hparams file; `HPARAMS=` env as in CORPUS/39 |
| D (optional, only if both B and C are LIVE or LEAD) | sparse band + identity | both | run only if §5 says so; otherwise not run (single-factor baselines first, arc §5 S-1) |

**Metrics per arm (exact counts, as CORPUS/39 required):** A1/A2/A7 `canon_full` (/24), `para_full` (/72, **binding on A7**), `para_first`, `tf_pertok_cont`, `locality_described_as` (JS-based, /100, harness), **plus two S-3 locality axes added for this prereg:** (L1) same-frame real-country prompts: count of the 12 real-country `CANON` prompts (CORPUS/43 F-A3 set) whose top-1 flips to any edited value (/12); (L2) `delta_norms` per layer (harness) and the SHA-256 of each covariance cache used. `para_full_string` (P4) alongside.

## 5. Pre-registered readings for arms B and C (each read against arm A from the same run; first match wins)

- **INVALID:** arm A outside the P2 envelope, or A1 or A2 `para_full` < 58/72 (≈ 80 %) in the candidate arm → the candidate damaged controls; no C10 reading (CORPUS/39 rule).
- **PASS (C10 rescue on this value class):** A7 `para_full` ≥ 61/72 (≈ 85 %, the spec gate CORPUS/36 cites) **and** L1 ≤ baseline + 1 **and** `locality_described_as` ≥ baseline − 3. → promote candidate: CORPUS entry, advisor + gpt-5.5 cross-family, then the (iv)/(i) interplay.
- **LEAD:** A7 `para_full` ≥ 30/72 (≈ 42 %, double the baseline envelope's ceiling and above CORPUS/36's 2-token incoherent floor 45.8 % is not required) with the same two locality conditions. → the ingredient is real but insufficient alone; queue the combination arm D and I-1/I-2 on top of it.
- **TRADEOFF:** A7 `para_full` ≥ 30/72 but L1 > baseline + 1 or `locality_described_as` < baseline − 3. → report the exchange rate (Δ`para_full` per Δlocality) next to LyapLock Table 2's ≈ 3–4 : 1; not a rescue; combination arm not run.
- **NULL:** A7 `para_full` < 30/72. → the hypothesis is closed for this regime; next in queue.
- **Flat-gain / falling-locality** (A7 within ± 3/72 of baseline and either locality axis worse) is read as **NULL with a locality cost**, not neutral (arc §11, ZsRE pattern in LyapLock).

Thresholds are counts of the same 72 subject-paraphrase triples CORPUS/36–39 scored; one seed; the within-run contrast against arm A is what is read, the absolute level is secondary.

## 6. What this does not test

Not BLUE proper (I-9b), not the OverTone objective (I-1), not forward replay (I-2) — all science path. Not the engine-path λC → λ′I variant (deferred, P1). Not C1 scale (N = 24 only). Not deployment (no GGUF step here; B3's gate applies at promotion). One seed, one model (D-C10k-rulings-2).

## 7. Cost, order, provenance

Order: P1–P5 → step 0 → arm A → (B if step 0 says LIVE/LIVE-AT-COST, else C first) → C → D only if §5 allows. Each behavioural recipe ≈ 20–25 min on the M3 Pro (CORPUS/39 timing). `DECISION_ID=D-C10l-covgeom PREREG=docs/C10L_COVGEOM_SPARSEBAND_PREREG.md OUT=results/c10l_covgeom/<arm>.json` set for every run so the result JSON carries provenance (the keying ablation's CORPUS/43 §Provenance note). Halt discipline: one speculative fix after a `cat -n` read, then HALT with `architecture_profile/sNNN_halt_diagnostic.json`.

## 8. Advisor and cross-family

This file goes to `tools/claude_advisor.sh` before any run; its items are folded in as §0 (v2). gpt-5.5 cross-family review is required at the promote gate (PASS) only.
