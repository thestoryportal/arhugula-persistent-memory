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

**Rule:** on the fixed grid `[10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]`, take the **largest** L2 whose mean realised fraction is ≥ 0.85 at **every** band layer on **both** control arms. Largest, so the departure from upstream's ridge is the smallest that lets the solve do what the z-optimisation asked for; 0.85, because the residual is spread over five layers and a per-layer shortfall compounds. The rule uses only the calibration quantity above; no edit outcome enters. Values passing: `[0.01, 0.003, 0.001]` → **L2 = 0.01**.

Change: `configs/hparams/anyedit_alphaedit_are_qwen25_3b.json` `"L2": 10` → `"L2": 0.01`. Nothing else: the module, projector, thresholds, windows, dtype and device are unchanged. `memit_ARE` (R3) has no L2 (its ridge is `mom2_update_weight · cov`, which is scale-matched to the keys by construction) and is unchanged.

**What the rerun must show (same gate, pre-registered in the parent):** R1 A1 and A2 `para_full ≥ 80` both. The locality bounds (real-country ≥ 11/12, JS ≥ 95; stock item unchanged) now carry real weight: a 1000× smaller ridge is exactly the regime where the null-space projector and the `Kp` preservation term must do the protecting, and the Amendment 1 controls say L8 does not protect last-token keys. A rerun that passes the controls but breaks a locality bound is recorded as such, not as recovered.

**Anchor:** the D5 device anchor is re-run under the new L2 before the controls (cheap; the solve is now in a different conditioning regime). R0 is not re-run (it does not depend on L2).

## 4. Scope of claims

Every result from here carries `L2=0.01 (Amendment 3)` in its scope string. A PASS-LEAD remains a mechanism lead for *this port with a rescaled ridge*; the official AnyEdit setting on this model is now known to be non-functional at L2 = 10 (a finding in its own right, scoped to the 3B base model and these keys). A FAIL remains scoped to this port and these three amendments.

## 5. Advisor

`tools/claude_advisor.sh` on this amendment before the rerun: `logs/claude_c10k_route_a_amendment3_review.md`.
