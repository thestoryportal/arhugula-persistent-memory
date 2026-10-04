# C10K Route A — ported official AnyEdit on the M3 Pro: HALTED — CONTROLS_NOT_RECOVERED

_Result 2026-10-04. Decision-ID `D-C10k-route-a`. Pre-registered in `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (commit `ceeaff8`) with Amendments 1 (`docs/C10K_ROUTEA_AMENDMENT_1_PER_LAYER_THRESHOLD.md`), 2 (`docs/C10K_ROUTEA_AMENDMENT_2_FP32_MPS.md`) and 3 (`docs/C10K_ROUTEA_AMENDMENT_3_L2_RESCALE.md`), each advisor-reviewed and committed before the run it governs. Successor to CORPUS/41 (Stage 0 halt; operator chose Route A). Records under `results/c10k_route_a/`; logs under `logs/c10k_route_a_*`, `logs/route_a_chain*.log`. Halt record: `architecture_profile/c10k_route_a_halt_diagnostic.json`._

## 1. Verdict

**HALTED — `CONTROLS_NOT_RECOVERED`** (prereg §3/§4): the A1/A2 control arms did not reach `para_full ≥ 80` under the ported `AlphaEdit_ARE` at upstream's hyperparameters, nor after the one localized fix the prereg allows (Amendment 3, ridge rescale). No A7 interpretation is licensed; A7 and the `memit_ARE` arm were run diagnostic-only. **Scope of the negative, no wider than the port:** Qwen2.5-3B base, fp32 on MPS, the official `jianghoucheng/AnyEdit@057a77f1` modules under the declared deviations D1–D8 + A1–A3, N = 24 fictional subjects, 1 seed, the program's held-out-paraphrase criterion. AnyEdit is **not** falsified; its own benchmarks do not measure this criterion (§5).

## 2. Chain of evidence (every gate in prereg order)

| step | result | artifact |
|---|---|---|
| Stage 0 (CORPUS/41) | official code cannot run on MPS; operator chose Route A (device-port deviation) | `docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md` |
| D1 port | 15 device substitutions, diff reviewed device-only | `logs/c10k_route_a_port.diff` |
| Token alignment | 72/72 | `results/c10k_route_a/alignment.json` |
| Projector gate v2 (Amendment 1; per-layer thresholds 0.01/0.02/0.02/0.02/0.03; fp32 keys) | PASS all bounds; held-out and ARE-window survival; key parity cos ≥ 0.99998 | `projector_gate_v2.json`, `projector_gate_v2_controls.json` |
| Interference control | protective at L4–L7 and on ARE keys; **non-protective at L8 for A1 last-token keys (1.03)** | `projector_gate_v2_controls.json` |
| D5 anchor (Amendment 2, MPS fp32 vs CPU fp32) | same top-1 3/3; norm ratios 1.36 / 1.23 / 1.12 / 1.01 / 1.00 (L2 = 10) and 1.00 / 1.03 / 1.10 / 1.07 / 1.04 (L2 = 0.01) | `anchor_L2-10.json`, `anchor.json` |
| R0 LAW#3 baseline (fp16, c10e) | A1 94.4 / A2 98.6 / A7 13.9 (known 93.1 / 97.2 / 12.5); LAW#5 |Δexpr| 0.0014 INERT | `R0_baseline.json`, `logs/c10k_route_a_R0_baseline.log` |
| R1 controls at upstream L2 = 10 | **FAIL** (table §3.1) | `R1_w1_*_L2-10.json` |
| Amendment 3 (one fix: L2 10 → 0.01 by calibration rule; back-test; pre-run prediction) | prediction: canonical recovers, paraphrase gate fails | `solve_gain_diag.json`, `solve_backtest.json` |
| R1 controls at L2 = 0.01 | **FAIL as predicted** (table §3.2); locality breached | `R1_w1_*.json` |
| A7, memit_ARE | diagnostic-only (§3.2) | `R1_w1_A7_coined_coined.json`, `R3_w1_A1_single.json` |

## 3. Results (EVIDENCE-SHOWS)

### 3.1 R1 controls at upstream's hyperparameters (L2 = 10)

| arm | canon_full | para_full | items ≥2/3 | real-country top-1 (≥11/12) | real JS (≥95) | described-as JS (≥95) | generic NLL Δ (nats) | stock item unchanged | band-norm ratio L4…L8 |
|---|---|---|---|---|---|---|---|---|---|
| A1_single | 11/24 | 0/72 | 0 | 11/12 | 93.21 | 99.84 | n/r | yes | 1.00 / 0.96 / 1.00 / 1.01 / 1.08 |
| A2_coherent2 | 1/24 | 0/72 | 0 | 12/12 | 98.68 | 99.87 | n/r | yes | 1.01 / 1.01 / 1.01 / 1.01 / 1.05 |

The z-optimisation converges (loss 0.009, target probability 0.99) and the per-layer solve delivers update norms 4.2 / 4.9 / 7.5 / 20 / 51 against residuals ≈ 100; z error falls only 98 → 87 across the band. Locality is intact because almost nothing was written.

### 3.2 R1 controls and diagnostics after the one allowed fix (L2 = 0.01)

| arm | canon_full | para_full | items ≥2/3 | real-country top-1 (≥11/12) | real JS (≥95) | described-as JS (≥95) | generic NLL Δ (nats) | stock item unchanged | band-norm ratio L4…L8 |
|---|---|---|---|---|---|---|---|---|---|
| A1_single | 24/24 | 0/72 | 0 | 10/12 | 84.78 | 87.02 | 0.25861 | NO | 3.60 / 1.04 / 1.00 / 1.00 / 1.00 |
| A2_coherent2 | 24/24 | 0/72 | 0 | 12/12 | 83.72 | 82.98 | 0.35221 | NO | 3.63 / 1.06 / 1.01 / 1.01 / 1.01 |
| A7_coined_coined (diagnostic-only) | 24/24 | 0/72 | 0 | 9/12 | 54.2 | 69.28 | 0.76242 | NO | 4.94 / 1.12 / 1.02 / 1.02 / 1.01 |
| memit_ARE A1_single (R3, diagnostic-only) | 2/24 | 0/72 | 0 | 12/12 | 99.01 | 99.94 | 0.00118 | yes | 6844.31 / 655.50 / 591.48 / 3564.69 / 13.10 |

**R3 memit_ARE (upstream `mom2_update_weight = 15000` covariance ridge, no projector, no L2), A1 diagnostic-only:** canon 2/24, para 0/72, real-country 12/12, described-as JS 99.94, generic NLL Δ 0.00118, **band-norm ratios 6844 / 656 / 591 / 3565 / 13**. The solve is numerically degenerate on this model (F6): per-layer update norms 573,880 / 71,567 / 70,918 / 411,066 / 1,561 against weight norms ≈ 100, while the z error barely moves (98 → 91) and behaviour is unchanged. The normalised covariance has eigenvalues down to 1.6e-7 (L4) … 2e-9 (L5–L8) with 1,583–8,645 directions below 0.005, so `15000·C` vanishes in thousands of directions and the update is dumped where no real input looks. The AlphaEdit null-space projector is exactly what makes the AlphaEdit_ARE solve well-posed by comparison. Not rescaled (the one fix was spent); magnitude/conditioning evidence, not keying evidence.

### 3.3 Why (back-test and gain diagnostic, Amendment 3 §2/§6)

| L2 | final z error (from 98.1) | realised fraction L4…L8 | fp32/fp64 solve rel. diff (max) | hidden transfer canonical / paraphrase |
|---|---|---|---|---|
| 10 | 65.935 | 0.17 / 0.14 / 0.12 / 0.17 / 0.28 | 7.1e-05 | 0.40 / 0.018 |
| 0.03 | 0.006 | 0.76 / 0.99 / 1.00 / 1.00 / 1.00 | 1.9e-02 | 1.00 / 0.008 |
| 0.01 | 0.002 | 0.89 / 1.00 / 1.00 / 1.00 / 1.00 | 5.7e-02 | 1.00 / 0.009 |

At L2 = 10 the solve realises 5–13 % of each residual because the projected key energy on this model (7–33) is the same order as the ridge. Rescaling restores the canonical fit completely (final z error 0.002; every arm 24/24 on the trained prompt) and leaves paraphrase hidden-state transfer at 0.8–1.8 %, with no item above 50 %, at every ridge value including upstream's. The edit is keyed at the last prompt token (`compute_z.py:91`); the paraphrases end on other tokens and never read it.

### 3.4 Projector and key-dtype gates (Amendment 1 v2, Amendment 2)

| layer | th | protection | A1 survival | held-out | ARE-window | interference ratio A1 / ARE | fp16-vs-fp32 key cos |
|---|---|---|---|---|---|---|---|
| L4 | 0.01 | 0.419 | 0.436 | 0.433 | 0.376 | 0.2256 / 0.2839 | 0.999993 |
| L5 | 0.02 | 0.432 | 0.473 | 0.471 | 0.458 | 0.2423 / 0.3525 | 0.999994 |
| L6 | 0.02 | 0.431 | 0.358 | 0.353 | 0.434 | 0.4886 / 0.5508 | 0.999988 |
| L7 | 0.02 | 0.421 | 0.343 | 0.336 | 0.497 | 0.4709 / 0.4719 | 0.999995 |
| L8 | 0.03 | 0.451 | 0.242 | 0.247 | 0.563 | 1.0305 / 0.3784 | 0.999996 |


## 4. Findings that survive the halt (promotable within scope; each labelled)

- **F1 (EVIDENCE-SHOWS).** On Qwen2.5-3B base, AlphaEdit's null-space projection at the pre-registered thresholds removes 56–76 % of edit-key norm at L4–L8 (survival 0.44 / 0.47 / 0.36 / 0.34 / 0.24) and is non-protective at L8 for last-token keys (interference ratio 1.03).
- **F2 (EVIDENCE-SHOWS).** Upstream's ridge `L2 = 10` is non-functional on this model with this projector: the solve realises 5–13 % of the residual; the value is an absolute number in activation units tuned on 7B/8B Instruct keys.
- **F3 (EVIDENCE-SHOWS).** Last-prompt-token keying gives ~0 hidden-state transfer to paraphrases for single- and two-token answers on this model, independent of the ridge; behaviourally 0/72 paraphrase hits on every arm while the trained prompt reaches 24/24.
- **F4 (EVIDENCE-SHOWS).** Restoring the write magnitude (L2 = 0.01) costs locality: generic NLL +0.25861 / +0.35221 / +0.76242 nats (A1/A2/A7), real-country 10/12 / 12/12 / 9/12, described-as JS 87.02 / 82.98 / 69.28, stock item changed on every arm; the L4 band norm grows 3.6× (the attention-sink key dominates L4's preservation term).
- **F6 (EVIDENCE-SHOWS).** `memit_ARE` at upstream's `mom2_update_weight = 15000` is numerically degenerate on this model: update norms up to 5.7e5 placed in the covariance's null space (eigenvalue floor 1e-7–1e-9; thousands of directions below 0.005) with no behavioural effect (canon 2/24, locality intact). The covariance ridge, like the L2 ridge, is an absolute quantity that does not transfer across models; here it fails in the opposite direction.
- **F5 (I-INFER, prior-art frame).** F3 is the editing-lineage face of the recall-lineage result that relations are decoded linearly from the **subject's last token** (Hernandez et al. ICLR 2024, `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`); AnyEdit/AnyEdit++ key at the written context's positions (`docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`) and score BLEU on the trained prompt, which is the program's canonical read, not its paraphrase criterion.

## 5. What this does and does not change

- **C10 stays OPEN / BLOCKING.** The AnyEdit-port route on local hardware is **HALTED at the controls**; it is not "spent" in the prereg's sense (that clause attaches to a FAIL after passing controls), but the mechanism in F3 says a faithful port cannot pass the program's paraphrase gate on this stimulus design at any ridge, so re-running the port with more tuning is not a live option.
- **Not a claim about AnyEdit's own benchmarks.** Their metrics (BLEU/BERTScore on the edited prompt) correspond to the canonical read, which this port achieves at 100 %.
- **Forward options (operator's call; recommendation first):** (i) pre-register the **LRE-faithfulness admission test** (`docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` §2.3): cheap, local, and the first candidate that predicts the value-class split rather than tuning around it; read Christ 2025, Choe 2025 and "Keys to Robust Edits" (2024) first. (ii) A **subject-keyed per-token hybrid** (MEMIT keying at the subject token for generalisation, AnyEdit-style per-window targets for long values): a re-implementation, not a port, and only worth building if (i) says the target relations are linearly decodable. (iii) **Accept-bounded** with project-coined multi-word values routed to the index/side-store (Route C), a Layer-6 lifecycle decision on the e2e map.

## 6. Scope and limitations

3B base, fp32 on MPS, N = 24, 1 seed; covariance accumulated from fp16 activations (D4-b; fp32 gate reproduced to 0.001); fp32 solve error up to 5.7 % at L2 = 0.01 (declared, Amendment 3 §6c); the standalone stock-item arm was killed (exit 137, memory) at fp32 with one window per token on a 100-token answer, so stock-item locality is taken from the in-arm probe only; R0 is fp16 (cross-dtype, labelled; each fp32 arm carries its own pre-edit reference, 0/24 everywhere). NOT promotable beyond this scope.

## 7. Advisor and close-out

Advisor reviews: Amendment 1 (`logs/claude_c10k_route_a_amendment1_review.md`, `_v2_review.md`), Amendment 2 (`_amendment2_review.md`), Amendment 3 (`_amendment3_review.md`), this result (`logs/claude_c10k_route_a_result_review.md`). CORPUS entry: `CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md`. Close-out gate: `tools/closeout_check.py D-C10k-route-a`.
