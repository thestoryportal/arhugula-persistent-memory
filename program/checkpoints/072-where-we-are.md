## WHERE WE ARE
- **Program:** Phase 0 — GATE-CAL (metric calibration). PRECONDITION that gates all later phases.
- **PHASE 0 COMPLETE — BOTH MODELS HALT (2026-06-17 02:40). GATE-CAL NOT MET. Do NOT promote to Phase 1.**
  - GPT-J `s241_gatecal_gptj.json`: null **0.110** / cf **0.386** / dest **0.394** → HALT (floor too HIGH; metric has range but no clean zero). Reproduced recovered prior run.
  - Qwen `s241_gatecal_qwen.json`: null **0.038** / cf **0.019** / dest **0.024** → HALT (INVERTED: cf & dest BELOW floor; NO dynamic range).
  - Joint HALT diagnostic: `architecture_profile/phase0_gatecal_halt_diagnostic.json` (both models + conclusion + recommended next).
  - **ROOT CAUSE (both, opposite symptoms):** fact/probe sets are NOT centrality-matched. GPT-J edits CENTRAL attributes → bleed even at null. Qwen edits a FICTIONAL peripheral attribute ('signature instrument') → total isolation → inverted band. The metric (JS on same-entity probes) is SOUND; the STIMULUS design is the defect.
  - **kl_factor ~inert on both** → §8.2 essence-KL safeguard is cross-entity, not same-entity (corroborates plan thesis).
  - **The GPT-J↔Qwen drift gap is a stimulus artifact, NOT (yet) a model-locality difference.**
- **RECOMMENDED NEXT (awaiting operator):** REDESIGN GATE-CAL stimulus — facts whose edit prompt has a CONFIDENT REAL top-1 (so null edit re-asserts a real token, not ' ____'/' the'/' He'), counterfact on a REAL central attribute, probes = OTHER real central attributes; centrality-matched across both models. Re-run; PASS = floor≈0 AND floor<cf≤dest on BOTH. Only then Phase 1.
  - Relaunch a model if needed: `cd /workspace && setsid bash -c 'cd /workspace && PYTHONUNBUFFERED=1 MODEL=<gptj|qwen> python -u s241_gatecal.py > s241_gatecal_<m>.log 2>&1' </dev/null >/dev/null 2>&1 & disown`
- **Plan:** `write_engine_viability_determination_plan.md` (the comprehensive program; supersedes single-session S2.41).
- **Active script:** `s241_gatecal.py` — calibrates same-entity-locality JS metric on GPT-J (and Qwen) via 4 conditions: NULL/identity edit (floor), COUNTERFACT (operational ref), DESTRUCTIVE (ceiling, mom2/10), kl_factor sweep (monotonicity). Emits `s241_gatecal_<model>.json` + a GATE verdict.
- **GATE-CAL pass condition:** null_floor_JS < 0.02 AND counterfact_JS > floor AND destructive_ceiling >= counterfact AND kl_factor monotone-nonincreasing. Else HALT (harness broken).

