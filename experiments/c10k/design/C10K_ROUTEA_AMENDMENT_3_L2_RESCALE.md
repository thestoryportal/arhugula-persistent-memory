# Route A — Amendment 3: ridge L2 rescaled for the 3B base model (revision of deviation D3) — the one localized fix the prereg allows, pre-registered before the rerun

**Parent prereg:** `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` §3 order/stop rule: "If A1/A2 fail under R1: one localized launcher/data fix, rerun the same gate, then HALT with diagnostic." **Date:** 2026-10-04. **Trigger:** `CHAIN: HALTED - CONTROLS_NOT_RECOVERED` at 14:50 (`logs/route_a_chain.log`). **This is that one fix.** If the rerun fails the gate again, the result is `HALTED — CONTROLS_NOT_RECOVERED` and no A7 interpretation follows.

## 1. What the halted run shows (EVIDENCE-SHOWS)

`results/c10k_route_a/R1_w1_A1_single.json`, `R1_w1_A2_coherent2.json` (fp32, Amendment 2; projector `c27203012b6a`; pre-edit reference 0/24 on both arms):

| arm | canon_full | para_full | items ≥2/3 | real-country locality | described-as JS | band-norm ratio L4…L8 |
|---|---|---|---|---|---|---|
| A1_single | 45.8 (11/24) | 0.0 (0/72) | 0 | 11/12 | 99.84 | 1.001 / 0.957 / 1.002 / 1.015 / 1.083 |
| A2_coherent2 | 4.2 (1/24) | 0.0 (0/72) | 0 | 12/12 | 99.87 | 1.006 / 1.006 / 1.007 / 1.014 / 1.053 |

The module's own stdout (recorded in each result's `stdout_tail`) shows the z-optimisation converging (A1 last item: loss 0.009, target probability 0.99; "Delta norm 106, Target norm 118") and then the per-layer solve delivering almost none of it: update norms 4.2 / 4.9 / 7.5 / 20 / 51 (L4…L8) against a residual whose mean norm ("z error") only falls from 98 to 87 across the five layers. The band weights move by under 1.5 % at L4–L7. Locality is intact (the edit is too weak to harm anything). The failure is in the **magnitude** the solve produces, not in targets, keys, device, dtype, or projector (all anchored or gated above).

## 2. Mechanism (EVIDENCE-SHOWS, `experiments/track_c/c10k_route_a_solve_gain_diag.py` → `results/c10k_route_a/solve_gain_diag.json`)

The module's update is `upd = A⁻¹ P K Rᵀ` with `A = P(KKᵀ + KpKpᵀ) + L2·I` (`AlphaEdit_ARE_main.py:128-130`); the change it produces at edit key `k_e` is `R·(Kᵀ P A⁻ᵀ k_e)`, so the fraction of item e's own residual that is realised is `diag(Kᵀ P A⁻ᵀ K)`. On the exact keys the module uses (A1/A2 question+answer sequences, fp32; K = window positions, Kp = the other positions; the gate-v2 projector), per layer:

**A1_single (24 edit keys, 242 preservation keys)**

| layer | ‖k‖² | ‖Pk‖² | top eig | L2=10 | L2=3 | L2=1 | L2=0.3 | L2=0.1 | L2=0.03 | L2=0.01 | L2=0.003 | L2=0.001 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L4 | 48 | 9.1 | 231128 | 0.053 | 0.081 | 0.144 | 0.286 | 0.485 | 0.719 | 0.873 | 0.956 | 0.986 |
| L5 | 40 | 9.0 | 3690 | 0.051 | 0.077 | 0.136 | 0.274 | 0.471 | 0.709 | 0.868 | 0.954 | 0.984 |
| L6 | 78 | 10.0 | 3848 | 0.054 | 0.086 | 0.156 | 0.312 | 0.520 | 0.751 | 0.891 | 0.963 | 0.987 |
| L7 | 161 | 18.8 | 42743 | 0.095 | 0.189 | 0.349 | 0.583 | 0.781 | 0.915 | 0.969 | 0.990 | 0.997 |
| L8 | 565 | 33.0 | 18816 | 0.135 | 0.259 | 0.442 | 0.674 | 0.843 | 0.943 | 0.980 | 0.994 | 0.998 |

**A2_coherent2 (48 edit keys)**

| layer | ‖k‖² | ‖Pk‖² | top eig | L2=10 | L2=3 | L2=1 | L2=0.3 | L2=0.1 | L2=0.03 | L2=0.01 | L2=0.003 | L2=0.001 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L4 | 54 | 7.3 | 231128 | 0.175 | 0.313 | 0.446 | 0.583 | 0.712 | 0.846 | 0.931 | 0.976 | 0.992 |
| L5 | 101 | 18.7 | 3771 | 0.311 | 0.422 | 0.506 | 0.605 | 0.719 | 0.847 | 0.931 | 0.976 | 0.992 |
| L6 | 182 | 16.9 | 3944 | 0.323 | 0.435 | 0.522 | 0.628 | 0.746 | 0.870 | 0.944 | 0.981 | 0.993 |
| L7 | 257 | 25.1 | 42743 | 0.383 | 0.517 | 0.640 | 0.779 | 0.886 | 0.956 | 0.984 | 0.995 | 0.998 |
| L8 | 424 | 58.8 | 18857 | 0.444 | 0.574 | 0.696 | 0.828 | 0.918 | 0.970 | 0.990 | 0.997 | 0.999 |

At upstream's `L2 = 10` the solve realises **5–13 %** of each A1 residual: the projected key energy ‖Pk‖² on this model is 7–33, the same order as the ridge, so `L2·I` dominates `P K Kᵀ`. Upstream's 10 was tuned on Qwen2.5-7B-Instruct / Llama-3-8B-Instruct (`hparams/AlphaEdit_ARE/*.json:24`), whose key scale is not recorded; the value is not scale-free. This is the same class of issue Amendment 1 met for `nullspace_threshold` (an absolute number in activation units) and Amendment 2 §3 named.

## 3. The fix (D3 revised) — rule fixed before the rerun, calibration keys only

**Rule:** on the fixed grid `[10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]`, take the **largest** L2 whose mean realised fraction is ≥ 0.85 at **every** band layer on **both** control arms. Largest, so the departure from upstream's ridge is the smallest that lets the solve do what the z-optimisation asked for; 0.85 was chosen on a compounding argument that §6(b) shows to be wrong (shortfalls are carried forward, not compounded); the rule's outcome does not depend on it. The rule uses only the calibration quantity above; no edit outcome enters. Values passing: `[0.01, 0.003, 0.001]` → **L2 = 0.01**.

Change: `configs/hparams/anyedit_alphaedit_are_qwen25_3b.json` `"L2": 10` → `"L2": 0.01`. Nothing else: the module, projector, thresholds, windows, dtype and device are unchanged. `memit_ARE` (R3) has no L2 (its ridge is `mom2_update_weight · cov`, which is scale-matched to the keys by construction) and is unchanged.

**What the rerun must show (same gate, pre-registered in the parent):** R1 A1 and A2 `para_full ≥ 80` both. The locality bounds (real-country ≥ 11/12, JS ≥ 95; stock item unchanged) now carry real weight: a 1000× smaller ridge is exactly the regime where the null-space projector and the `Kp` preservation term must do the protecting, and the Amendment 1 controls say L8 does not protect last-token keys. A rerun that passes the controls but breaks a locality bound is recorded as such, not as recovered.

**Anchor:** the D5 device anchor is re-run under the new L2 before the controls (cheap; the solve is now in a different conditioning regime). R0 is not re-run (it does not depend on L2).

## 4. Scope of claims

Every result from here carries `L2=0.01 (Amendment 3)` in its scope string. A PASS-LEAD remains a mechanism lead for *this port with a rescaled ridge*; the official AnyEdit setting on this model is now known to be non-functional at L2 = 10 (a finding in its own right, scoped to the 3B base model and these keys). A FAIL remains scoped to this port and these three amendments.

## 5. Advisor

First review (FIX-FIRST): `logs/claude_c10k_route_a_amendment3_review.md`. Items resolved in §6–§7 below; the rerun follows this revision's commit.

## 6. Back-test of the mechanism and pre-run predictions (EVIDENCE-SHOWS, `experiments/track_c/c10k_route_a_solve_backtest.py` → `results/c10k_route_a/solve_backtest.json`; advisor FIX-FIRST items 1, 2, 4, 5, 6 of `logs/claude_c10k_route_a_amendment3_review.md`)

The ported module's layer loop (`AlphaEdit_ARE_main.py:66-140`) replayed on the 24 A1 items with the module's own `compute_z` / `compute_ks`, fp32 on MPS, weights restored after each pass; no correctness evaluation (that is the rerun).

| L2 | z error L4…L8 → final | update norm L4…L8 | realised fraction of the true residual L4…L8 (per-item mean) | fp32-MPS vs fp64-CPU solve, rel. diff L4…L8 | hidden transfer canonical | hidden transfer paraphrase |
|---|---|---|---|---|---|---|
| 10 | 98.1 / 96.2 / 94.6 / 92.8 / 87.2 → 65.935 | 4.2 / 4.9 / 7.5 / 20.3 / 50.6 | 0.17 / 0.14 / 0.12 / 0.17 / 0.28 | 7.1e-05 / 4.3e-05 / 6.4e-05 / 3.9e-05 / 1.5e-05 | 0.40 | 0.018 (max-item frac ≥ 0.5: 0.0) |
| 0.03 | 98.1 / 89.0 / 77.6 / 63.7 / 42.3 → 0.006 | 219.2 / 45.5 / 15.4 / 13.7 / 13.8 | 0.76 / 0.99 / 1.00 / 1.00 / 1.00 | 9.9e-04 / 1.5e-03 / 8.0e-03 / 1.1e-02 / 1.9e-02 | 1.00 | 0.008 (max-item frac ≥ 0.5: 0.0) |
| 0.01 | 98.1 / 87.6 / 76.6 / 62.7 / 41.8 → 0.002 | 290.0 / 33.6 / 13.8 / 13.5 / 13.5 | 0.89 / 1.00 / 1.00 / 1.00 / 1.00 | 3.7e-03 / 4.9e-03 / 2.5e-02 / 3.3e-02 / 5.7e-02 | 1.00 | 0.009 (max-item frac ≥ 0.5: 0.0) |

**(a) The diagnostic describes the module.** At L2 = 10 the replay reproduces the halted run's update norms (4.23 / 4.92 / 7.55 / 20.3 / 50.6 vs the recorded 4.2 / 4.9 / 7.5 / 20 / 51) and z-error path (98.1 → 87.2) to the last digit.

**(b) Carry-forward, not compounding (item 4).** `cur_zs` is recomputed at every layer (`AlphaEdit_ARE_main.py:108`), so a shortfall at L4 is passed to L5–L8, which then realise 100 % of what remains: final z error 0.006 (L2 = 0.03) and 0.002 (L2 = 0.01) against 65.9 at L2 = 10. §3's "compounding" rationale for the 0.85 target was wrong and is withdrawn; the rule's outcome is unchanged (any target in (0.709, 0.868] picks 0.01, and 0.03 reaches the same end state). The rule was written after the calibration table existed; no edit outcome entered it.

**(c) Precision (item 1).** The module's fp32 solve against an fp64 reference of the same system: ≤ 7e-5 at L2 = 10, up to 1.9e-2 at 0.03, up to 5.7e-2 at 0.01 (L8). Both rescaled values exceed the 2e-3 agreement D6 measured at upstream's ridge. **Declared limitation, not changed:** L2 stays at the pre-registered 0.01 (no post-hoc rule change; an fp64 or CPU solve would be a second fix and a module-numerics deviation). The realised fractions above were computed from the fp32 update actually applied, so the 5.7 % solve error is already inside the "1.00 realised / final z error 0.002" numbers: it changes the update's direction in the residual-orthogonal subspace, which is where locality damage would show, not its effect at the edit keys.

**(d) The L4 top eigenvalue is the attention-sink token (item 2).** The largest preservation key at L4 has norm 98.14 at sequence position 0 (median preservation-key norm 7.83); the same first token appears in all 24 sequences, and 24 × 98.14² ≈ 231155 is the recorded top eigenvalue (231,128). At L5–L8 the maximum is an ordinary mid-sequence token (norms 37–45). The L4 realised fraction is the only one below 1.0 at the rescaled ridges (0.76 / 0.89) and is carried forward.

**(e) Paraphrase transfer is structurally absent (item 5) — pre-run prediction.** After a full pass, the hidden state at the z-layer on the **canonical** prompt moves exactly as requested (transfer 1.00 at L2 = 0.03 and 0.01) while on the three **paraphrase** prompts it moves by 0.8–1.8 % of the requested change, with no item above 50 %, at every L2 including upstream's. The module keys the edit at the last prompt token (`compute_z.py:91`, the token "of" in the canonical template) and the paraphrases end on other tokens ("called", "is", "is"); with a single-token answer there is no answer-internal position whose key the paraphrases share. Nothing in the ridge can move this. **Prediction, recorded before the rerun:** R1 A1/A2 at L2 = 0.01 recover the canonical prompt and **fail the `para_full ≥ 80` gate**; the chain then halts as `CONTROLS_NOT_RECOVERED` with this as the mechanism. The rerun is still run, because the prediction is a hidden-space proxy and the prereg's criterion is behavioural.

**(f) Off-diagonal terms (item 6)** are included in the realised fractions above (they are computed on the true residual matrix); the per-item minimum at L2 = 0.01 is 0.83 (L4) and ≥ 0.997 elsewhere.

## 7. Remaining advisor items

- **Item 3 (projector vs ridge).** The projector's energy stripping is reported in Amendment 1 §8 and the gate tables (‖Pk‖/‖k‖ at the chosen thresholds 0.44 / 0.47 / 0.36 / 0.34 / 0.24; at upstream's 0.02 the L4 value is higher, 0.53, and L8 lower, 0.18). The ridge is still the operative cause: the back-test realises the residual fully once L2 is rescaled, with the projector unchanged. §4's sentence is narrowed: the official setting is non-functional **at L2 = 10 with the Amendment-1 thresholds, fp32 on MPS, on this 3B base model**.
- **Item 7 (locality too weak).** `run_arm` now records mean token NLL on 20 held-out Wikipedia snippets pre and post edit (`generic_nll_*`, diagnostic, not a gate).
- **Item 8 (is an hparam change a "launcher/data fix").** Recorded: the operator's standing directive accepts recommendations by default and asks that irreversible decisions be surfaced, not blocked on; this classification is surfaced in the session report. The science-path content of the change is one scalar in a config file; the module is untouched (D1).
- **Item 9 (F1 finding that survives either outcome).** Two statements go to CORPUS whichever way the rerun goes: (i) on Qwen2.5-3B base, the AlphaEdit null-space projection at the pre-registered thresholds removes 56–76 % of edit-key norm at L4–L8 (Amendment 1 §2/§8); (ii) AnyEdit's last-prompt-token keying gives ~0 hidden-state transfer to paraphrases for single-token answers on this model, independent of the ridge (§6e).
- **Anchor under the new L2 (item 1).** Re-run before the controls with the parent's criteria unchanged (same canonical top-1 on 3/3 items; per-layer update-norm ratio MPS/CPU within [0.5, 2]). Failure → HALT (`INVALID`, D5); no fp64 fallback is available because that would be a second fix.
