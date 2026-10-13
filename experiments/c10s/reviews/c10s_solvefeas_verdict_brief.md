# Codex brief — D-C10s-solvefeas verdict pass

Review only: no model, no GPU; edit nothing but **`results/c10s_solvefeas_codex_verdict.md`**; `/usr/bin/git`. Then say DONE.

## The run
Prereg `docs/C10S_SOLVEFEAS_PREREG.md` v2 (advisor v1 FIX-FIRST folded; implementation by Codex, advisor implementation review FIX-FIRST with one BLOCKING fixed at commit `400f051`). Records `results/c10s_solvefeas/{inertness,run,inject}.json`, logs `results/c10s_solvefeas_logs/{inertness,arms_first}.log`. Reader: `LLMDB_ROOT=<worktree> C10S_ARM=solvefeas .venv/bin/python -B experiments/track_c/c10s_sharedz_read.py results/c10s_solvefeas` (model-free).

Printed: inertness ALL INERT (parity 0.0; engine 7- vs 19-row distance 0.2223 at 50 steps); cell 1 canonical 54/72, shared 72/72, gain 18 (5/10/3 by template, 15 subjects); fit min 0.9712, two entries below 0.98 (Plurnak T2 0.9712, evaluation 25 0.9773; Vorlex T2 0.9758, evaluation 25 0.9647), both **objective-stopped**; mean steps 37.83; clamp hits 24/24; evaluation-25 shared-z injection 70/72 (record only); noise twin gain 2, 14/72 pairs differ; control c T1 3–4 vs 24, T2 5/11 vs 24; 50-step positive control True; outcome **UNDERFIT-AT-50**.

## Questions
1. Validity under the prereg and the provenance rules (source identity `400f051`, settings binding, arm selector, inertness binding, budget positive control). Is UNDERFIT-AT-50, qualified objective-stopped, the correct label?
2. What may be recorded in CORPUS/52, with which qualifiers? The two objective-stopped entries say the engine's averaged stopping rule (total loss < 0.05) ended the solve before every frame reached 0.98. What does that mean for the 0.98 per-frame bar against the frozen verbatim stopping rule? Plurnak fell from 0.977 at evaluation 25 to 0.971 at the stop. The injection numbers (72/72, and evaluation-25 70/72) are unedited-model observations; CORPUS/46 F-D1 applies. The template draw differs from CORPUS/51's.
3. Compare with CORPUS/51 honestly: what does going from 18 underfit entries at 25 to 2 at 50 (different template draws, but the same-run evaluation-25 snapshot shows 0.925 min → 0.971) say about explanation (a), and what remains for (b)/(c)?
4. Next: the prereg routes to step 2. Do you agree? Name any candidate that the record now motivates (for example, a stopping rule that requires each frame's fit, which would be a deliberate departure from the engine's verbatim rule and its own hypothesis), as a candidate only.
5. Exact proposed CORPUS/52 wording.

Format: header (reviewer, model, effort, date), **Verdict: label CONFIRMED / WRONG**, numbered items with file:line, the CORPUS/52 wording, the recommendation.
