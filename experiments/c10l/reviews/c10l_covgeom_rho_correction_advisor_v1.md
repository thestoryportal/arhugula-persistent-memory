# Advisor review v1 — proposed ρ_c correction to CORPUS/44 (2026-10-06)

**Verdict: FIX-FIRST.** The reversal is real and the correction's direction is right; the append text and the propagation list need fixes before the CORPUS gate.

**Single most important thing.** "≈ 97 % installed" is a bound from one offline reconstruction, not a measurement of the edit that scored 7/24. Reword to "2.8 % of the canonical residual remains in norm, in step 0's reconstruction", and add the missing control: record `‖z − cur_after‖/‖z − cur_before‖` inside the harness run itself (`experiments/track_c/c10e_bandknob.py:197–217` reads `cur` once and never re-reads it after the band). Until that exists for a behavioural run, "the edit installs the target at the keyed position" is the reconstruction's claim, not the run's.

## Issues, priority order

1. **(a) Reading — correct, with caveats the note omits.** `rel = ‖dW·K − R‖/‖R‖` (`c10l_covgeom_step0.py:74–75`) and `rho_c_band = ‖zs − cur1_c‖/‖zs − cur0_c‖` (`:132–134`) are remaining-residual ratios; R0 band 0.0282, R1 0.0080 (`step0_offline.json` `regularisers.R0.band`, `.R1.band`). The pre-registration defined it this way (`docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:44`, `:49` "R1 lowers ρ_c → mechanism present") and the JSON's `H-I8a_mechanism_present: True` reads it correctly — CORPUS/44:31 misread its own prereg; say so, it is the strongest support. Caveat 1, cross-process: step 0 has its own context-template draw (F-A4, `CORPUS/44:32`, delta_norms vary up to 4.35 %); arm A's ρ_c was never measured. Caveat 2, precision: `f32_vs_f64_rel` is 3e-5–7e-5 per layer (R0 `per_layer`) and both paths cast to fp16 (`step0.py:128–130`, `c10e_bandknob.py:217`), so F-A5 H3 is effectively answered — state it instead of leaving H3 silently alive.

2. **(d) "≈ 97 % installed in norm" over-states.** The ratio is of residual norms, not a projection; by the triangle inequality `‖cur_after − cur_before‖/‖z − cur_before‖` lies in [0.972, 1.028] and may overshoot. Write "2.8 % remains in norm" or give the interval. "R1 behaves worse (canon 7 → 4)": the canon envelope is [5, 10]/24 (`CORPUS/44:39`); "does not behave better" is what is licensed.

3. **(c) I-INFER leaks into the append.** The §"implications" block is labelled and excluded, but the append's last sentence ("not a canonical-position realisation shortfall; H1 and the key-side difference remain live") is untagged inference; CORPUS/44 tags every such clause (`:33`). Tag it, and say H2 was routed to the H1 bucket by `CORPUS/46:30` rather than dropping H2 unmentioned.

4. **(e) Propagation list incomplete; one claim false.** The note (:27) says the ledgers carry "NULL ×3 only". They carry the reversed sentence verbatim — "step 0 realises z to 3 % at the keyed position, so the P6-vs-edit gap points at the edit's collateral effect" — at `CORPUS/00_MASTER_EVIDENCE.md:233`, `CORPUS/03_STATUS_LEDGER.md:140`, `EXPERIMENT_RUNBOOK.md:849` (§13), `docs/HYPOTHESIS_REGISTER_2026-06-18.md:341`. Also missing: `recommended_sequence.md:26–27` (steps 6–7 "aimed at the '3 percent installed' finding"), `prereg_stubs.md:74, :78`, `docs/C10V_LAYERPICK_PREREG.md:34`. `docs/EVIDENCE_INDEX.md` not found at that path; auto-memory outside this directory: UNVERIFIABLE.

5. **(b) Labels.** None change: F-A3's behavioural clause (49/72 vs 13/72) stands, only its mechanistic clause is withdrawn; CORPUS/47–50 cite CORPUS/44 by count or "no label change" (`CORPUS/47:6`, `48:6`, `49:6`, `50:6`); F-D1 (`CORPUS/46:30`) is independent. Correct. Add the inverted consequence explicitly: the ledger's conclusion ("points at the collateral effect") is *better* supported under the right reading, so the fold is not a retraction of H1.

6. **Overturning test.** The in-harness ρ_c readout above, plus one A1 line (A1 ρ_c never measured, `results/c10v_layerpick_advisor_v1.md:23`): if A1 and A7 both leave ≈ 3 %, realisation-in-norm says nothing about the wall.

7. **Drift.** Bookkeeping on a live C10 falsifier; it changes the ranking rationale of sequence steps 6–7 (`recommended_sequence.md:13`) and the operator must see it before they are scheduled. No F1 bearing.
