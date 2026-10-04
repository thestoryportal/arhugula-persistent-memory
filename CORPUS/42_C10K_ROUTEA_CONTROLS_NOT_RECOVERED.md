# 42 — C10K Route A (ported official AnyEdit, M3 Pro): HALTED — CONTROLS_NOT_RECOVERED

_Result 2026-10-04. Decision-ID D-C10k-route-a ⟨D-C10k-route-a@3b0be47e⟩. Pre-registered: `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (`ceeaff8`) + Amendments 1–3 (each advisor-reviewed and committed before the run it governs). Full detail: `docs/C10K_ROUTEA_RESULT.md`. Halt record: `architecture_profile/c10k_route_a_halt_diagnostic.json`. Records: `results/c10k_route_a/`. Advisor reviews: `logs/claude_c10k_route_a_amendment{1,1_v2,2,3}_review.md`, `logs/claude_c10k_route_a_result_review.md`._

## Claim class
**Method-port result under declared deviations (D1–D8, A1–A3) — a scoped negative on the port's controls, NOT a falsification of AnyEdit and NOT C10 evidence (no A7 interpretation licensed).** Successor to CORPUS/41 (Stage 0 halt; operator chose Route A).

## VERDICT — HALTED — CONTROLS_NOT_RECOVERED (prereg §3 stop rule; the one allowed fix was spent)

| Finding | Value | Artifact |
|---|---|---|
| R1 controls at upstream `L2 = 10` | A1 canon 11/24, para 0/72; A2 canon 1/24, para 0/72 (gate ≥ 80 both) | `R1_w1_*_L2-10.json` |
| Why: the solve realises 5–13 % of the residual at `L2 = 10` (ridge ≈ projected key energy 7–33 on this model) | update norms 4.2/4.9/7.5/20/51 vs residual ≈ 100; back-test reproduces to the digit | `solve_gain_diag.json`, `solve_backtest.json` |
| One fix (Amendment 3): `L2 → 0.01` by calibration rule | canonical fit restored: final z error 98 → 0.002 | `solve_backtest.json` |
| R1 controls at `L2 = 0.01` | A1 canon 24/24, **para 0/72**; A2 canon 24/24, **para 0/72** → HALT | `R1_w1_*.json` |
| Mechanism: paraphrase hidden-state transfer at the z-layer | canonical 1.00; paraphrase 0.009 (L2 0.01), 0.018 (L2 10); no item ≥ 0.5 — the edit is keyed at the last prompt token (`compute_z.py:91`), which paraphrases do not share | `solve_backtest.json` |
| Locality under the rescaled ridge | real-country 10/12 / 12/12; described-as JS 87.02 / 82.98 (bound 95); generic NLL +0.25861 / +0.35221 nats; stock item changed | `R1_w1_*.json` |
| A7 diagnostic-only (`L2 = 0.01`) | canon 24/24, para 0/72; real-country 9/12, JS 69.28 | `R1_w1_A7_coined_coined.json` |
| memit_ARE A1 diagnostic-only (upstream covariance ridge 15000, no projector) | canon 2/24, para 0/72, locality intact, band-norm ratios up to 6844× (fp32) / 16049× (fp64): **over-regularised** — single-key gain 0.04–0.07 at 15000 and at the program's 5000, with or without the preservation term; last-token keys sit 17–180× under the covariance ridge; giant norms are a tail symptom (fp64 control + ridge diag) | `R3_w1_A1_single.json`, `fp64_resolve_control.json`, `memit_ridge_diag.json` |
| Projector (Amendment 1 v2, fp32 keys) | per-layer thresholds 0.01/0.02/0.02/0.02/0.03 pass protection ≤ 0.5 and survival ≥ 0.2 (A1, held-out, ARE-window); interference **non-protective at L8 for last-token keys (1.03)**; key parity cos ≥ 0.99998 | `projector_gate_v2.json`, `projector_gate_v2_controls.json` |
| D5 anchor (fp32 MPS vs CPU) | same top-1 3/3; norm ratios within [0.5, 2] at both L2 | `anchor*.json` |
| R0 LAW#3 (fp16) | A1 94.4 / A2 98.6 / A7 13.9 vs known 93.1 / 97.2 / 12.5; LAW#5 INERT | `R0_baseline.json` |

## Findings that survive the halt (scoped: Qwen2.5-3B base, fp32 MPS, this port, N = 24, 1 seed)
- **F1** AlphaEdit's null-space projection at the pre-registered thresholds removes 56–76 % of edit-key norm at L4–L8 on this model and does not protect L8 against last-token keys.
- **F2** upstream's `L2 = 10` is non-functional here (realises 5–13 % of the residual); the value is an absolute number tuned on 7B/8B Instruct key scales.
- **F3** last-prompt-token keying gives ~0 hidden-state transfer to paraphrases, independent of ridge: trained prompt 24/24, paraphrases 0/72 on every arm.
- **F4** restoring the write magnitude costs locality (NLL +0.26–0.35 nats; real-country and JS bounds breached; L4 band norm 3.6× via the attention-sink key).
- **F6** `memit_ARE` at upstream's covariance weight is over-regularised for last-token keys here (exact-arithmetic fit 2/24; single-key gain ≤ 0.07 at either weight; keys 17–180× under the ridge): the failing axis is key placement relative to the covariance geometry, the same axis as F3, not the weight alone.
- **F5 (I-INFER)** F3 is the editing-lineage face of the recall-lineage finding that relations are decoded from the **subject's last token** (Hernandez et al. ICLR 2024); AnyEdit/AnyEdit++ key inside the written context and score BLEU on the trained prompt = the program's canonical read, not its paraphrase criterion (`docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`, `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`); external support in the 2026-10-04 sweep: PRISM (subject-last-token input invariant across contexts, cos ≥ 0.97), ALOE (paraphrase failure is address-side), Suresh et al. (subject-keyed AlphaEdit on Qwen2.5-3B reaches 90–96 % paraphrase generalisation; hparams hand-derived per architecture) — `docs/PRIOR_ART_SWEEP_2026-10-04.md`. The causal attribution is tested next by `D-C10k-keying-ablation` (`docs/C10K_KEYING_ABLATION_PREREG.md` v3).

## What this does and does not change
- C10 remains **OPEN / BLOCKING**. The AnyEdit-port route on local hardware is HALTED at the controls; by F3 a faithful port cannot pass the paraphrase gate on this stimulus design at any ridge, so further port tuning is not a live option.
- AnyEdit's own claims are untouched (their metrics correspond to the canonical read this port achieves at 100 %).
- **Forward (operator's call; recommendation first):** (i) pre-register the LRE-faithfulness admission test (cheap, local; read Christ 2025, Choe 2025, "Keys to Robust Edits" first); (ii) subject-keyed per-token hybrid as a re-implementation, only if (i) says the target relations are linearly decodable; (iii) accept-bounded with coined multi-word values routed to the side-store (Route C).
