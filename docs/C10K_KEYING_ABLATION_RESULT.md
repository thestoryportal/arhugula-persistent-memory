# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3; two advisor rounds). Records `results/c10k_keying_ablation/K{1..4}.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`; LAW#5 parity check made knob-independent after K2's first pass halted "NOT INERT" by construction — `K2_firstpass_parity_halt.json`). Chain `tools/c10k_keying_ablation_chain.sh`, K2 rerun `tools/c10k_keying_ablation_rerun_k2k4.sh`._

## 1. Reading (prereg v3 §3 precedence): **INVALID-LAST-TOKEN-CELLS (no keying reading; the last-token write does not land)**

both last-token cells fail the canon ≥ 90 validity rule: the write does not land (canon < 90 at ridge weight 5000 with the engine's KL prompt). Gate: K1 A1 95.8 / A2 97.2 vs R0 94.4 / 98.6 → **PASS**; LAW#5 INERT in every cell (K2 after the parity fix). Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.

## 2. Results (EVIDENCE-SHOWS)

| cell | key locus | templates | A1 canon | A1 para_full | A1 para_any | A1 described-as JS | A2 canon | A2 para_full | A2 described-as JS | A1 rel. Δ‖W‖ L4…L8 | validity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | subject | on | 100.0 | **95.8** | 100.0 | 90.06 | 100.0 | **97.2** | 92.48 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K2 | subject | off | 100.0 | **91.7** | 100.0 | 91.78 | 100.0 | **88.9** | 91.97 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K3 | last | on | 29.2 | **0.0** | 0.0 | 99.82 | 4.2 | **0.0** | 99.9 | 0.10 / 0.08 / 0.10 / 0.25 / 0.42 | INVALID (canon < 90) |
| K4 | last | off | 25.0 | **0.0** | 0.0 | 99.81 | 8.3 | **0.0** | 99.84 | 0.11 / 0.09 / 0.13 / 0.29 / 0.48 | INVALID (canon < 90) |

`para_any` = fraction of the 24 subjects with at least one paraphrase correct (the per-subject ≥ 2/3 count is not stored by this harness). Δ‖W‖ is the engine's own per-layer relative update norm for the A1 edit.

## 3. What the table says

- **Keying at the prompt's final token in the program's engine, the write does not land (EVIDENCE-SHOWS).** With the identical engine, covariance, ridge weight (5000), band, z-objective and dtype as K1, K3/K4 fit the trained prompt on only 29.2 % (7/24) / 25.0 % (6/24) of A1 items (K1: 100.0 %) and 4.2 % (1/24) / 8.3 % (2/24) of A2; the described-as JS stays at 99.8 because little readable change was written, not as independent evidence of locality. **Where it fails is not yet separated (I-INFER, two candidates):** (a) the solve — the Route A ridge diagnostic (`results/c10k_route_a/memit_ridge_diag.json`) puts last-token keys 17–180× under the covariance ridge, a geometric argument tested behaviourally here at one ridge weight only; (b) the z-objective — in K3/K4 the engine's KL prompt (`"<country> is the city of is a"`) is keyed at the same final `" of"` in a near-identical context to the rewriting prompt, so one delta must change the next token for the edit and leave it unchanged for the KL prompt, a conflict K1 does not have. §3b (z-probe) separates these. The per-layer Δ‖W‖ (larger than K1's at L7–L8) says the solve wrote *something*; it is not a measure of what reached the keyed token.
- **Therefore the cells cannot separate "keying prevents generalisation" from "keying prevents writing", and the pre-registered SUFFICIENT reading is not reached.** By the precedence order both last-token cells are INVALID; no rule is written from them.
- **The missing cell is plain MEMIT with last-token keying at a small ridge weight (and a non-colliding KL prompt)**: if canonical fit climbs to ≥ 90 as the weight falls, the ridge mechanism is confirmed behaviourally and the cell becomes a valid K3 whose paraphrase score answers the prereg's question; it is cheaper and closer to the question than the covariance-corpus knob and is pre-registered next (§4). Note also that Route A's AlphaEdit_ARE changed two things at once (null-space projector and 1000× smaller ridge), and the projector removes preserved-knowledge directions that paraphrases may ride on, so Route A's 0/72 has an alternative cause unrelated to keying. **The complementary half in Route A:** when a null-space projector and a 1000× smaller ridge force the last-token write in (AlphaEdit_ARE, L2 = 0.01), the trained prompt fits 24/24 and paraphrases still score 0/72 (`docs/C10K_ROUTEA_RESULT.md` §3.2, F3). Taken together (I-INFER): a write keyed at the prompt's last token either cannot be placed under a covariance ridge, or, when placed, is read only from the trained prompt. Neither experiment alone makes F3 causal; the two together leave no observed configuration in which a last-token-keyed write generalises, and one (K1) in which a subject-keyed write does, on the same subjects, paraphrases and engine.
- **Templates (K2; `described-as JS` = the described-as probe's Jensen–Shannon locality score used throughout c10e, higher = less change) (K2 valid: 91.7 / 88.9).** Subject-keyed writes without context templates still generalise (91.7 ≥ 80), so templates are not necessary for ≥ 80 % paraphrase scores with subject keying at N = 24; they still account for about 4–8 points (A1 95.8 → 91.7, A2 97.2 → 88.9). Whether the key locus carries generalisation cannot be read from this run (K3/K4 INVALID). Full-precision Δ‖W‖ differ between K1 and K2 at every layer (e.g. L4 15.874 vs 15.889), so the knob changed the key computation.

### 3b. z-probe (advisor item 2; results appended after the run)

`experiments/track_c/c10k_keying_ablation_zprobe.py` runs the engine's unmodified `compute_z` on 3 subjects in K1 style and K3 style with the engine's own templates and records the final target probability at the keyed token, the loss path and the KL term. **Reading, fixed before the run:** if K3-style target probability at the last step is ≥ 0.9 (as K1's), the z-objective reaches the target and the failure is in the solve (ridge); if it stays well below K1's, the KL-prompt conflict (or the key position) blocks the target vector itself and the ridge attribution is withdrawn.

_Results (`results/c10k_keying_ablation/zprobe.json`):_

| style | subject | steps | target prob (final) | loss final (nll + kl) | ‖z‖ |
|---|---|---|---|---|---|
| K1 | Zorbland | 12 | 0.986 | 0.050 (0.014 + 0.030) | 80.9 |
| K1 | Quaxil | 25 | 0.994 | 0.058 (0.006 + 0.046) | 85.6 |
| K1 | Plurnak | 21 | 0.997 | 0.048 (0.003 + 0.040) | 83.3 |
| K3 | Zorbland | 20 | 0.983 | 0.045 (0.017 + 0.022) | 66.8 |
| K3 | Quaxil | 16 | 0.988 | 0.046 (0.012 + 0.026) | 66.6 |
| K3 | Plurnak | 11 | 0.993 | 0.031 (0.007 + 0.017) | 63.5 |

**Reading:** K3-style `compute_z` reaches the target at the keyed `" of"` token (final target probability ≥ 0.983; K1-style ≥ 0.986) with a KL term of the same size as K1's. The z-objective is not where the K3/K4 write is lost; the KL-prompt conflict is excluded as the cause. **The loss is at the solve, which supports the ridge mechanism and licenses the next cell: the same last-token cells at a small ridge weight, plain MEMIT, no projector (prereg v3 §6 amendment).** (‖z‖ is smaller in K3 style, 63–67 vs 81–86, consistent with the last-token residual being a smaller target than the subject-token one.)

## 4. Scope, limitations, what changes

- 3B base, fp16, N = 24, 1 seed; one engine; one ridge weight (5000). The declared KL-prompt difference in K3/K4 is a live candidate cause (§3), not excluded by the untouched locality score (an unchanged locality is what a winning KL term would produce).
- **Changes:** the memory_mirror rule ("read the keying locus against the generalisation criterion before porting") stays **conditional** — supported, not proven causal. Option (ii) (subject-keyed per-token hybrid) keeps its rationale by the combined picture but gains no new evidence. New EVIDENCE-SHOWS: **in the program's engine at ridge weight 5000, a last-token-keyed write does not land (canon < 90)**; the mechanism (ridge vs KL conflict) is I-INFER until §3b and the small-weight cell resolve it. **Next pre-registration, in order:** the small-ridge-weight last-token cell (K3′), then the covariance-corpus knob (Moir, `docs/PRIOR_ART_SWEEP_2026-10-04.md` §3.4).
- C10 (A7) is untouched by this run, as pre-registered.

## 5. Advisor and close-out

Advisor on this result: `logs/claude_c10k_keying_ablation_result_review.md`. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
