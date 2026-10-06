---
name: corpus44-rho-is-remaining-residual
description: CORPUS/44's ρ_c (0.028) is the fraction of the canonical residual that REMAINS after the band write in step 0's reconstruction, not the fraction realised; the "3 % realised" reading was reversed and corrected 2026-10-06.
metadata:
  type: project
---

**Fact.** `experiments/track_c/c10l_covgeom_step0.py:74–75` defines `rel = ‖dW·K − R‖/‖R‖` and `:134` defines `rho_c_band = ‖z − cur_after‖/‖z − cur_before‖` — remaining-residual ratios. R0 (the harness recipe) leaves 2.8 % of the canonical residual norm at the z-layer keyed position in the float64 offline reconstruction (R1, P := I, leaves 0.8 % and does not behave better); ≈ 23 % remains on paraphrase prompts under a proxy CORPUS/44 marks uninformative (Spearman −0.12). CORPUS/44 F-A3 said "the weight edit realises the same z to 3 %": reversed. Corrected append-only on 2026-10-06 after an advisor pass and a Codex pass (`results/c10l_covgeom_rho_correction_2026-10-06.md`); token re-stamped to ⟨D-C10l-covgeom@af2e38f7⟩; no label changed.

**Why it matters.** The "realisation account" (the write cannot install the target at the keyed position) loses its canonical-position premise; the live accounts are the edit's collateral change (CORPUS/46 F-D1: a z carrying 51/72 pre-edit carries 23/72 injected into the edited model) and the key-side difference under paraphrase. The research pass's ranking criterion 3 and its steps 6–7 (I-1/I-2, H-3 direct ΔW) were motivated by the reversed reading.

**How to apply.** Never write "X % realised" from ρ_c; write "X % remains". Before scheduling steps 6–7, re-argue their rationale with the operator. The next harness run that solves z records the in-harness ratio for A1, A2 and A7 (D-C10s-sharedz amendment A1); read equal small ratios as "this scalar does not explain the gap", not as "realisation is irrelevant". Trap: an offline reconstruction's ratio is not a behavioural-run measurement (F-A4: cross-process ΔW variation up to 4.35 %).
