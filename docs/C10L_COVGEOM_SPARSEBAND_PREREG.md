# Pre-registration (v2) — (ii-c) opener: solve geometry (I-8) and sparse layer set (I-9a) on the program's C10 harness (D-C10l-covgeom)

**Date:** 2026-10-05 (v1 → advisor FIX-FIRST, `results/c10l_covgeom/advisor_v1.md`; v2 = this file, items folded in §0). **Status: v2 — frozen for the next session; nothing has run.** **Decision-ID:** `D-C10l-covgeom`. **E2e-map cell:** §8.9 write/firing (multi-token CORE values); F1 condition **C10**. **Class:** falsifier (can fail). **Model:** Qwen/Qwen2.5-3B @ `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`, fp16, MPS (D-HW-1; D-C10k-rulings-2). **Harness:** `experiments/track_c/c10e_bandknob.py` (P-8 device-neutral; produced CORPUS/37–39 and the CORPUS/43 K-cells), `.venv` python, `LLMDB_ROOT` = this worktree. Notation: a *band* is written `4–8`; a *layer set* is written `{4, 8}`.

## 0. v1 → v2 (advisor items and their disposition)

| # | advisor item | disposition in v2 |
|---|---|---|
| 0 | establish the A7 z-ceiling by z-injection before anything else | **adopted as step −1 (P6)**: patch `zs` into the residual stream at layer 8, subject-last token, on the 24 `CANON` and 72 `PTEST` prompts; greedy-decode; score `canon_full`/`para_full`. `c10d_zprobe.py` measured only the `compute_z` objective's own probability (0.98–0.99), not decoding after injection, so this is new. If the injected ceiling on paraphrases is < 30/72, no solve aimed at `zs` can reach LEAD and the bottleneck is the target (I-1 territory); the prereg then records that and the arms still run once, for the record, but cannot be read as a solve result |
| 1 | A7 mostly fails on the canonical prompt (CORPUS/39: `canon_full` 7/24, `para_full` 15/72), so RoSE's generalisation mechanism targets the smaller gap | **confirmed and adopted**: `ρ_c` (canonical realisation) is a read readout beside `ρ_p`; H-I8 is restated as two sub-claims, realisation (H-I8a) and transfer (H-I8b), read separately |
| 2 | step 0 must be sequential: the harness updates in place and recomputes keys and `cur` per layer | **confirmed** (`c10e_bandknob.py:170–199`: `compute_ks` and `get_module_input_output_at_words` are called inside the layer loop after the previous layer's in-place update). Step 0 is sequential on an in-memory model with snapshot/restore of the five `down_proj` weights; nothing persists |
| 3 | R0 may be mis-transcribed; P is on both sides | **confirmed**: `A = P·(K Kᵀ + cache) + L2·I`, `B = P·K·Rᵀ`, `ΔW = solve(A, B)ᵀ` (`c10e_bandknob.py:188–190`), so `ΔW = R Kᵀ P A⁻ᵀ`; `cache` is zeros in a single-batch run (`cache_c` initialised to zeros, added to only after all layers). v2 writes the solve in that form for all regularisers |
| 4 | key dimension is 11008, not 2048 | **confirmed** (`intermediate_size: 11008`; cache files are 484.7 MB = 11008² × 4 B). Cost line and λ′ = 5000·tr(C)/11008 corrected |
| 5 | `ρ_p` unvalidated and possibly degenerate; step 0 must not decide queue order | **adopted**: arm B runs regardless; step 0 explains, it does not gate. Template-key cosines to `K_c` reported per `PTEST` template; per-subject `ρ_p` under R0 is correlated with per-subject `para_full` from arm A and the correlation is reported |
| 6 | arm C mixes sparsity, layer count and residual share; notation collision | **adopted**: control arm C′ `{7, 8}` (contiguous two-layer, z at 8) added; notation fixed throughout |
| 7 | locality axes cannot see what the projector protects | **adopted**: axis L3 = 50 unedited real capitals from `configs/screens/g6_screen_qwen3b_v2.json` (78 selected; the 50 not used as A1/A2 values), top-1 agreement with the pre-edit model (binding: ≥ 48/50) and mean next-token KL (reported); plus a 20-sentence generic-text perplexity slice (reported) |
| 8 | fingerprint conflicts with CLAUDE.md | **reconciled**: `tools/engine_fingerprint.py:13–22, 34` records `5c0c706a` (pod era) → `e6ac7e18` (P-8, 2026-10-03) → **`d941a9fb` (P-8 amended 2026-10-04; supersedes e6ac7e18 before any result ran under it)**; `docs/program_state.json` next_actions[0] cites `d941a9fb`. **CLAUDE.md line 28 is stale** (cites `e6ac7e18`); flagged to the operator, not edited here |
| 9 | arm B's validity argument must be explicit; "bit-level on CPU" is wrong for MPS fp16 | **adopted** (P3 rewritten) |
| 10 | text fixes (LEAD sentence, typo, envelope rule, clustering) | **adopted**: envelope = observed values ± 3/72 → A7 `para_full` ∈ [11, 18]/72 and `canon_full` ∈ [5, 10]/24; LEAD = ≥ 30/72, double the observed baseline; 72 items are 24 subjects × 3 paraphrases, subject-clustered, one seed |

## 1. Question

Two one-knob changes in *what the harness solves*, engine unmodified:

- **H-I8 (solve geometry, P := I).** The harness solves `A = P·(K Kᵀ + cache) + 1.0·I`, `B = P·K·Rᵀ`, where `P` projects onto the null space of the layer covariance (σ < 0.005). RoSE ("Beyond the Covariance Trap", arXiv 2603.15518 §3–4) argues that routing same-subject edits through the covariance geometry collapses generalisation across prompt variations and replaces the covariance with the identity, ΔW = R Kᵀ (I + K Kᵀ)⁻¹, which is this harness with `P := I`. Two sub-claims, read separately: **H-I8a** the projector removes directions the canonical edit needs (CORPUS/39: 17/24 A7 edits miss on the canonical prompt) — readout `ρ_c` and `canon_full`; **H-I8b** the projector starves transfer to paraphrase keys (the remaining gap, 15/72 vs 7/24·3 ≈ 21/72 expected if transfer were perfect) — readout `ρ_p` and `para_full`. The S-3 rule (arc §5) predicts both at a locality cost.
- **H-I9a (sparse layer set).** BLUE (arXiv 2502.03748 Thm 4.1, §4.3): the error of spreading one residual evenly over a band grows with the spread; two layers suffice. On harness semantics (`c10e_bandknob.py:170–199`, mirroring `memit_main.py:152–205`): `layers = [4, 8]` computes z at 8, gives half the residual to 4 and the remainder to 8 — a **sparse set**, not BLUE proper (I-9b, science path). The band sweeps CORPUS/37–39 varied `4–8`, `8–12`, `4–12`, `4–12 ∪ 18–22`, never a non-contiguous set and never a two-layer set.

## 2. Premise checks (blocking; all recorded in the result JSON before any arm)

- **P1 — the solve that produced the A7 numbers** (`c10e_bandknob.py:146–199`): AlphaEdit-style as above; `hp.mom2_update_weight` is not used by `my_edit` (it enters only the engine call in the LAW#5 parity gate). Consequence recorded in the arc doc §12: CORPUS/39 `lowcov2500 4–12` is a `band412` replicate (CORPUS/38), not a covariance-weight data point.
- **P2 — fingerprint and LAW#3.** `python3 tools/engine_fingerprint.py` PASS with `d941a9fb…` and `_cov_cpu == 3`. Then arm A (the harness's baseline recipe) reproduces CORPUS/39 `4–8`: A1 `para_full` ≥ 68/72, A2 ≥ 68/72, A7 `canon_full` ∈ [5, 10]/24, A7 `para_full` ∈ [11, 18]/72, A7 `para_first` ∈ [48, 62]/72 (observed 56/72). Miss → HALT (harness fault).
- **P3 — the knob's inertness and arm B's validity.** New env knob `C10_PROJECTOR ∈ {nullspace, identity}`, default `nullspace`. Validity rests on two things only: (a) with the default, `delta_norms` per layer match a pre-knob run to the device's float tolerance (MPS fp16 forward; CPU float32 solve: relative difference < 1e-4), and the LAW#5 parity gate (`|Δexpr| < 0.05`, `|Δloc| < 3`, `c10e_bandknob.py:270–300`) passes; (b) a `cat -n` read of the `identity` branch showing it sets `P = I` and nothing else. Arm B departs from the engine by design; it is a pre-registered science arm, not a harness change, and is never run through the parity gate.
- **P4 — tokenisation declaration** (arXiv 2609.29045). `full_seq_match` (`c10e_bandknob.py:236`) compares greedy ids with `tok(" " + value)` ids. Binding metric = id match (comparable with CORPUS/35–39). A same-string recall through a different tokenisation is a miss on the binding metric and is reported separately as `para_full_string`.
- **P5 — environment and provenance.** `.venv` python; covariance caches for layers 4–12 present (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.{4..12}.mlp.down_proj_float32_mom2_t100_100000.npz`); the SHA-256 of every cache file used is written to the result JSON; `DECISION_ID`, `PREREG`, `OUT` set on every run.
- **P6 — z-injection ceiling (step −1).** On the fp16 model, for each of the 24 A7 requests compute `zs` with the harness's `compute_z` at layer 8; patch it into the residual stream output of layer 8 at the subject-last token (forward hook; no weight change) and greedy-decode `len(target)` tokens on `CANON` and on each `PTEST` prompt. Report `canon_full_inj` (/24) and `para_full_inj` (/72). **Reading:** `para_full_inj` < 30/72 → the target itself cannot carry LEAD; arms still run once for the record but §5 readings are suffixed "under a sub-LEAD target ceiling" and the next queue item becomes I-1. `para_full_inj` ≥ 30/72 → the ceiling admits LEAD; proceed normally. Also report `para_full_inj` per `PTEST` template.

## 3. Step 0 — offline solve-geometry reconstruction (explanatory; does not gate; sequential; no persistence)

Model in memory, snapshot of the five `down_proj` weights taken (`snap()`/`restore()` as in the harness). For each regulariser, run the harness's own layer loop with the solve replaced, applying each layer's `ΔW` in place so that layer i+1's keys and `cur` are what the harness would see, then restore. Nothing is scored behaviourally in step 0; readouts are algebraic.

**Regularisers (same requests, same `compute_z` targets):** (R0) `A = P(K Kᵀ) + I`, `B = P K Rᵀ` — the harness; (R1) `P := I` — RoSE/IGA; (R2) `A = K Kᵀ + 5000·C`, `B = K Rᵀ` — the engine's MEMIT ridge, reference only; (R3) `A = K Kᵀ + λ′ I`, λ′ = 5000·tr(C)/11008 — trace-matched identity, reference only. `K` is 11008 × 24 per layer; solves are 11008 × 11008 in float64 on CPU (≈ 1 GB each); `P` needs one eigendecomposition per layer (cached across regularisers).

**Readouts, per layer and summed over the band, for R0 and R1 (R2/R3 reported):**
- `ρ_c = ‖ΔW K_c − R‖_F / ‖R‖_F` on the canonical keys (H-I8a);
- `ρ_p = ‖ΔW K_p − R_p‖_F / ‖R_p‖_F` on the 72 paraphrase subject-last keys, `R_p = zs − cur_p` (H-I8b); **validity of the proxy:** cosine of each template's keys to `K_c` (a template whose keys equal `K_c` is degenerate and is excluded from `ρ_p`); per-subject `ρ_p` under R0 correlated (Spearman) with per-subject arm-A `para_full` — reported, and if |ρ| < 0.3 the proxy is marked uninformative;
- `π = ‖ΔW K_ctrl‖_F / ‖ΔW K_c‖_F` on the 50 L3 real-capital subject-last keys and the 24 `described as` keys;
- `‖ΔW‖_F` and the share of `‖ΔW‖²_F` inside the null space of `C`.

**Reading (explanatory):** R1 lowers `ρ_c` by ≥ 20 % → H-I8a mechanism present; R1 lowers `ρ_p` by ≥ 20 % → H-I8b mechanism present; `π_R1 / π_R0` is the predicted locality cost. These predictions are written down before arm B runs and compared with arm B afterwards; a prediction that fails is itself a finding about the proxy. Output `results/c10l_covgeom/step0_offline.json`; script `experiments/track_c/c10l_covgeom_step0.py` (new, harness-side, imports the harness primitives after a `cat -n` read of lines 146–199).

## 4. Behavioural arms (harness; arms A1 / A2 / A7 in every run; N = 24; one seed; fp16)

| arm | hparams | change | specified by |
|---|---|---|---|
| **A** baseline | `qwen25_3b_memit_hparams.json`, band `4–8` | none | P2 reproduction |
| **B** I-8 | same | `P := I` in `my_edit` | `C10_PROJECTOR=identity` |
| **C** I-9a | `qwen25_3b_memit_hparams_set48.json` = baseline with `"layers": [4, 8]` | set `{4, 8}`: half the residual at 4, remainder at 8, z at 8 | `HPARAMS=` |
| **C′** control | `qwen25_3b_memit_hparams_set78.json` = `"layers": [7, 8]` | contiguous two-layer set, z at 8 | `HPARAMS=` |
| D | set `{4, 8}` + `P := I` | both | only if §5 allows (single-factor results first) |

**Metrics per arm (exact counts):** A1/A2/A7 `canon_full` (/24), `para_full` (/72, **binding on A7**), `para_first` (/72), `tf_pertok_cont`, `locality_described_as` (harness JS score); **locality axes:** L1 = top-1 flips to any edited value on the 12 real-country `CANON` prompts of CORPUS/43 F-A3 (/12); L2 = `delta_norms` per layer and cache SHAs; **L3 = top-1 agreement with the pre-edit model on 50 unedited real capitals (/50, binding ≥ 48) and mean next-token KL on them (reported), plus mean perplexity on 20 generic sentences (reported)**; `para_full_string` (P4).

## 5. Pre-registered readings (candidate arm vs arm A from the same run; first match wins)

- **INVALID:** arm A outside the P2 envelope; or candidate A1 or A2 `para_full` < 58/72; or L3 < 48/50 (the candidate damaged unrelated knowledge; a C10 number cannot be read from it, only the TRADEOFF line below).
- **PASS:** A7 `para_full` ≥ 61/72 (≈ 85 %, CORPUS/36's gate) with L1 ≤ baseline + 1, `locality_described_as` ≥ baseline − 3, L3 ≥ 48/50. → promote: CORPUS entry after advisor + gpt-5.5 cross-family.
- **LEAD:** A7 `para_full` ≥ 30/72 (double the observed baseline) with the same locality conditions. → ingredient real but insufficient alone; D and I-1/I-2 queue on top of it.
- **TRADEOFF:** A7 `para_full` ≥ 30/72 but a locality condition fails (L1, `described_as`, or L3). → report the exchange rate Δ`para_full` per Δ(each locality axis) beside LyapLock Table 2 (≈ 3–4 : 1); not a rescue; D not run.
- **REALISATION-ONLY:** A7 `canon_full` ≥ 15/24 (double) but `para_full` < 30/72. → H-I8a supported, H-I8b not; the transfer wall stands; pairs with I-1.
- **NULL:** none of the above. **Flat gain with a worse locality axis is NULL with a locality cost, not neutral.**
- **Arm C vs C′:** a LEAD on C is credited to the *spread* (BLUE's argument) only if C′ does not also reach LEAD; if both do, the credit is "two layers", not "boundary layers".

All counts are over the same 72 subject-clustered items as CORPUS/36–39; the within-run contrast is what is read.

## 6. What this does not test

I-9b (BLUE proper), I-1 (OverTone), I-2 (forward replay) — science path. The engine-path λC → λ′I variant (deferred). C1 scale. Deployment (B3 gate at promotion). Multiple seeds and other models (D-C10k-rulings-2).

## 7. Cost, order, provenance, halt

Order: P1–P5 → P6 (step −1, ≈ 15 min) → step 0 (≈ 30–45 min, CPU float64 solves) → arm A → arm B → arm C → arm C′ → D only if §5 allows. Each behavioural arm ≈ 20–25 min (CORPUS/39 timing). Results under `results/c10l_covgeom/`; the advisor's v1 review is archived there. Halt discipline: one speculative fix after a `cat -n` read, then HALT with `architecture_profile/sNNN_halt_diagnostic.json` and a checkpoint note.

## 8. Reviews

v1 advisor → FIX-FIRST (§0). v2 is frozen for the run; any further change before the run is an amendment with its own advisor pass. gpt-5.5 cross-family at the promote gate only.
