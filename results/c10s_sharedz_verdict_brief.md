# Codex brief — D-C10s-sharedz verdict pass (step 1 rerun under A2 v2)

Review only: no model, no GPU (the location control is running), edit nothing but your output file **`results/c10s_sharedz_codex_verdict.md`**, `/usr/bin/git`. Then say DONE.

## The run
`results/c10s_sharedz_r2/` (`inertness.json`, `run.json`, `inject.json`), logs `results/c10s_sharedz_logs/r2_inertness.log` and `r2_arms_first.log`; source at commit `1169794` (A2 v2, your round-2 PROCEED `results/c10s_sharedz_codex_a2_review_round2.md`). Reader: `.venv/bin/python -B experiments/track_c/c10s_sharedz_read.py results/c10s_sharedz_r2` (model-free; you may run it). Prereg: `docs/C10S_SHARED_Z_PREREG.md` (§0, §2 cell 1, §3, §7 A2).

Printed by the reader: inertness ALL INERT ((iii) and (iv) parity 0.0; engine 7-row vs 19-row distance 0.0977 recorded); cell 1 canonical 51/72, shared 69/72, gain 18 (net by template 4/9/5, 12 subjects); fit min 0.8437 with 18 underfit (subject, frame) entries across 7 subjects (CANON included for 5 of them); clamp hits 24/24, mean steps 24.0; control c T1 additive canonical 5 vs shared 24, T2 4 vs 24 (absolute 13 vs 23); noise twin gain 3, 17/72 pairs disagree. Outcome **UNDERFIT** → write arm not run.

## Questions
1. **Validity.** Is the run valid under the prereg, A2 and the provenance rules (source hashes, identity, inertness binding, OUT_DIR)? Is UNDERFIT the correctly applied label, given the precedence UNDERFIT > NOISE-NON-DISCRIMINATING > screen?
2. **What may be recorded.** The prereg says UNDERFIT means "inconclusive under this solve budget; nothing is concluded about frames". Which of the cell-1 numbers may go in CORPUS/51 as recorded observations, with what qualifiers? Consider: the 69/72 is an injection into the unedited model (CORPUS/46 F-D1: injection performance depends on the surrounding model), the shared z is underfit, the screen would otherwise have passed, T1 shares "government" with held-out Q3 (the Q3 net gain is 5), and the noise twin's 17/72 discordance.
3. **The underfit itself.** All 24 solves ran the full 25-step budget and hit the clamp; 5 subjects underfit even on CANON. What does the record say about why (budget vs the clamp radius vs the frames), and what would a follow-up arm need to change? Name it as a candidate only; do not design it fully.
4. **Next per the prereg.** §3 says an UNDERFIT moves the sequence to step 2. Do you agree, or does the record justify a pre-registered budget/clamp follow-up of step 1 first? Give a recommendation with reasons.

Format: header (reviewer, model, effort, date), **Verdict: label CONFIRMED / label WRONG (and why)**, numbered items with file:line, the exact wording you would put in CORPUS/51 for the observations, and the recommendation.
