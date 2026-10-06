# 49 — Two-pass solve: NULL with a directional gain (+8/72), a larger write (total ΔW ×1.31) and a described_as gate miss (−3.08 against 3.0); the injection-found direction does not survive as a fresh weight edit at the pre-registered margin

_Result 2026-10-05. Decision-ID D-C10p-twopass ⟨D-C10p-twopass@12f87dc3⟩. Pre-registered `docs/C10P_TWOPASS_SOLVE_PREREG.md` (v2 frozen after the Codex gpt-5.5 design pass; implementation pass; verdict pass before this entry — `results/c10p_twopass_advisor_{v1,impl,verdict}.md`). Records `results/c10p_twopass/{run,pass1,pass2,pass3}.json`, `logs_c10p_chain.log` (readout), `logs_run.log`. Driver `experiments/track_c/c10p_twopass_arms.py`; reader `c10p_twopass_read.py`; harness seam `Z_OVERRIDE` in `experiments/track_c/c10e_bandknob.py` (default `None`, bypassed inside the LAW#5 parity check, consumption audited). Engine unmodified (fingerprint d941a9fb stored in full; LAW#5 INERT in all three passes, |Δexpr| ≤ 0.0012). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@af2e38f7⟩ run 1 arm A. Lineage: CORPUS/48 routing (D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩: DIRECTION), CORPUS/47 (D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩), CORPUS/46 (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩). Rulings: D-C10k-rulings-1 (strict held-out-paraphrase full-sequence bar binds), D-C10k-rulings-2, D-C10l-rulings-2._

## Claim class
**Pre-registered mechanism arm on the program's C10 harness — Qwen2.5-3B fp16 MPS, band 4–8, N = 24, one process, three full harness passes (baseline, sham, two-pass), arms A1 + A2 + A7 with the S-3 axes and a same-frame fictional probe. Read against the §8.9 bar strictly by §3. No label in CORPUS/44–48 changes; no bearing on the F1 label. C10 stays OPEN/BLOCKING.**

## VERDICT — NULL (gain 8/72 < 10), with the effect stated: +8 held-out, canon 7 → 12, total ΔW ×1.31, described_as −3.08

Validity all GREEN: fingerprint; LAW#5 ×3; pass-1 controls A1 72, A2 71; A7 edit-only 13/72 ∈ [5, 18], canon 7 ∈ [5, 10]; **sham inert** (pass 2 identical to pass 1 on every readout and every per-layer ΔW, deviation 0.000); override consumed 0 / 1 / 1 times; rotated population 18/24 (re-solve geometry: mean cosine 0.872, mean displacement 0.56).

| pass | canon /24 | held-out /72 | first | string | A1 | A2 | L1 /12 | same-frame fictional /6 (pre-edit 1) | described_as | L3 /30 | ppl post | ΔW L4..L8 (total) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 baseline (engine targets) | 7 | 13 | 59 | 13 | 72 | 71 | 0 | 1 | 88.18 | 30 | 21.63 | 15.8 / 12.1 / 12.0 / 20.2 / 27.8 (88.0) |
| 2 sham (fresh edit aimed at `z_pre`) | 7 | 13 | 59 | 13 | 72 | 71 | 0 | 1 | 88.18 | 30 | 21.63 | identical to pass 1 |
| **3 two-pass (fresh edit aimed at `z_post`)** | **12** | **21** | 60 | 21 | 72 | 71 | 0 | 1 | **85.10** | 30 | 21.67 | 24.9 / 17.8 / 16.0 / 24.8 / 31.7 (**115.2**) |

Locality gates for pass 3: A1, A2, L1, L3, perplexity (+0.04 ≤ 0.5) and the same-frame fictional probe hold; **`described_as` 85.10 misses 88.18 − 3 = 85.18 by 0.08**. ΔW ratio pass 3 / pass 1: total 1.31 (under the 1.5 cap for the LARGE-WRITE qualifier); per layer 1.57 / 1.47 / 1.33 / 1.23 / 1.14 (the cap is on the total). **Binding:** pass 3 held-out 21/72 (string readout 21) against 13 → gain 8 < 10 → **NULL**. LEAD needed ≥ 30; PARTIAL or TRADEOFF needed gain ≥ 10.

## Findings (scoped: one process; N = 24; one model)

- **F-T1 (EVIDENCE-SHOWS).** A fresh edit aimed at the target re-solved on the once-edited model does not transfer materially better on this harness: 21/72 held-out against 13/72 (gain 8, under the pre-registered 10), canon 7 → 12. CORPUS/48's DIRECTION routing is **not borne out at the pre-registered margin for the fresh two-pass weight edit**; the injection finding itself stands (a weight edit is a different intervention, CORPUS/44 F-A3). The stacked variant is untested (prereg §2.4).
- **F-T2 (EVIDENCE-SHOWS).** The two-pass write is 31 % larger in total (1.57× at layer 4 tapering to 1.14× at layer 8) and costs 3.08 points of `described_as`; the other locality axes and the controls held within their gates (perplexity +0.04). Had the gain cleared 10, the label would have been TRADEOFF on that axis.
- **F-T3 (EVIDENCE-SHOWS, method).** On this harness path the `Z_OVERRIDE` seam can aim the A7 edit at supplied z vectors with inertness shown: the sham pass reproduces the baseline to the last digit on every readout and every per-layer ΔW, with the override audited as consumed exactly once per pass and never inside the LAW#5 parity check.
- **F-T4 (I-INFER; register only).** The 13 → 21 move sits above the identical-baseline envelope's top (18) and comes with canon 7 → 12, so the re-solved target does something as a weight edit — not enough, and with a larger write. Hypotheses, not run: (a) one re-solve is not a fixed point (iterate on the twice-edited model, write size capped); (b) the stacked variant; (c) any band-4–8 edit reintroduces the collateral change at non-keyed positions regardless of target (CORPUS/46 H1), which is the engine-path arms' question.

## What this changes

- **By the prereg's NULL consequence, the next arms are I-1 OverTone / I-2 forward replay on the engine path** (LAW#5 discipline; CORPUS/46's queue). The iterated re-solve and the stacked variant (F-T4 a/b) are logged in the register as cheaper harness-side alternatives; choosing them ahead of I-1 / I-2 would be an operator decision, not the pre-registered branch.
- The harness gains a reusable, audited seam for aiming edits at supplied targets (F-T3), scoped to this path.
- Not written here, by the advisor's instruction: "the direction reading was wrong"; "any supplied target"; "unchanged" for axes that moved within gates; any CORPUS/44–48 label change; contract evidence; F1 change. C10 OPEN/BLOCKING.
- Limitations: one process; N = 24; one model (D-C10k-rulings-2); fp16 MPS; the described_as miss is 0.08 on a 3.0 gate and the gain 8 on a 10 margin — both inside the per-process spread, so neither is a strong signal either way.
