# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3; two advisor rounds). Records `results/c10k_keying_ablation/K{1..4}.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`; LAW#5 parity check made knob-independent after K2's first pass halted "NOT INERT" by construction — `K2_firstpass_parity_halt.json`). Chain `tools/c10k_keying_ablation_chain.sh`, K2 rerun `tools/c10k_keying_ablation_rerun_k2k4.sh`._

## 1. Reading (prereg v3 §3 precedence): **INVALID-LAST-TOKEN-CELLS (no keying reading; writability finding)**

both last-token cells fail the canon ≥ 90 validity rule: the write does not land under the covariance ridge. Gate: K1 A1 95.8 / A2 97.2 vs R0 94.4 / 98.6 → **PASS**; LAW#5 INERT in every cell (K2 after the parity fix). Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.

## 2. Results (EVIDENCE-SHOWS)

| cell | key locus | templates | A1 canon | A1 para_full | A1 para_any | A1 described-as JS | A2 canon | A2 para_full | A2 described-as JS | A1 rel. Δ‖W‖ L4…L8 | validity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | subject | on | 100.0 | **95.8** | 100.0 | 90.06 | 100.0 | **97.2** | 92.48 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K2 | subject | off | 100.0 | **91.7** | 100.0 | 91.78 | 100.0 | **88.9** | 91.97 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K3 | last | on | 29.2 | **0.0** | 0.0 | 99.82 | 4.2 | **0.0** | 99.9 | 0.10 / 0.08 / 0.10 / 0.25 / 0.42 | INVALID (canon < 90) |
| K4 | last | off | 25.0 | **0.0** | 0.0 | 99.81 | 8.3 | **0.0** | 99.84 | 0.11 / 0.09 / 0.13 / 0.29 / 0.48 | INVALID (canon < 90) |

`para_any` = fraction of the 24 subjects with at least one paraphrase correct (the per-subject ≥ 2/3 count is not stored by this harness). Δ‖W‖ is the engine's own per-layer relative update norm for the A1 edit.

## 3. What the table says

- **Keying at the prompt's final token in the program's engine does not write at all.** With the identical engine, covariance, ridge weight (5000), band, z-objective and dtype as K1, K3/K4 fit the trained prompt on only 29.2 % / 25.0 % of A1 items (K1: 100.0 %) and 4.2 % / 8.3 % of A2, with locality untouched (99.82 / 99.81 vs K1 90.06). The update is not small (relative Δ‖W‖ up to 0.42 at L8) but it does not reach the trained prompt. This is the behavioural face of the Route A ridge diagnostic (`results/c10k_route_a/memit_ridge_diag.json`): last-token keys lie 17–180× under the covariance ridge at every band layer, so a MEMIT-style solve cannot place a readable write there at either ridge weight.
- **Therefore the cells cannot separate "keying prevents generalisation" from "keying prevents writing", and the pre-registered SUFFICIENT reading is not reached.** By the precedence order both last-token cells are INVALID; no rule is written from them.
- **The complementary half already exists in Route A:** when a null-space projector and a 1000× smaller ridge force the last-token write in (AlphaEdit_ARE, L2 = 0.01), the trained prompt fits 24/24 and paraphrases still score 0/72 (`docs/C10K_ROUTEA_RESULT.md` §3.2, F3). Taken together (I-INFER): a write keyed at the prompt's last token either cannot be placed under a covariance ridge, or, when placed, is read only from the trained prompt. Neither experiment alone makes F3 causal; the two together leave no observed configuration in which a last-token-keyed write generalises, and one (K1) in which a subject-keyed write does, on the same subjects, paraphrases and engine.
- **Templates (K2 valid: 91.7 / 88.9).** Subject-keyed writes without context templates still generalise (91.7 ≥ 80), so templates are not what carries paraphrase generalisation in this engine; whether the key locus is cannot be read from this run (K3/K4 INVALID).

## 4. Scope, limitations, what changes

- 3B base, fp16, N = 24, 1 seed; one engine; the declared KL-prompt difference in K3/K4 (`"<country> is the city of is a"`, keyed at `" of"`) is present but cannot explain a canonical fit of 25–29 % (the KL term regularises locality, and locality is untouched).
- **Changes:** the memory_mirror rule ("read the keying locus against the generalisation criterion before porting") stays **conditional** — supported, not proven causal. Option (ii) (subject-keyed per-token hybrid) keeps its rationale by the combined picture but gains no new evidence. New EVIDENCE-SHOWS for the ridge line: **last-token keys are not writable under the Wikipedia covariance ridge in the program's engine**, which is the local reason to pre-register the covariance-corpus knob (Moir, `docs/PRIOR_ART_SWEEP_2026-10-04.md` §3.4) before any further keying experiment.
- C10 (A7) is untouched by this run, as pre-registered.

## 5. Advisor and close-out

Advisor on this result: `logs/claude_c10k_keying_ablation_result_review.md`. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
