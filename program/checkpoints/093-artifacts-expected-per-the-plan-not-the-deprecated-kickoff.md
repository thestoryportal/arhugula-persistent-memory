## ARTIFACTS EXPECTED (per the PLAN, not the deprecated kickoff)
Phase 0: `s241_gatecal_gptj.json`, `s241_gatecal_qwen.json`. Program deliverables per plan §Artifacts: `s242_baseline_failure.json` (Phase 1) · `s243_relation_keying.json` (Phase 2) · `s244_entity_nullspace.json` (Phase 3) · `s24X_grace_existence.json` (cond.) · framework_finding v1.10 (metric+baseline) → v1.11 (workarounds) → v1.12 (verdict) · `write_engine_viability_determination_report.md` (Phase 4 verdict).

# LATEST SESSION HANDOFF - 2026-06-27 C10h closeout

- **D-C10h-anyedit-pilot ⟨D-C10h-anyedit-pilot@6413cc67⟩ (CORPUS/40) - C10 AnyEdit small-window pilot DONE = TRADEOFF_NOT_CLEAN_RESCUE.** local AnyEdit-style ARE small-window pilot (`window_size=1`) passes token-alignment and no-op gates but is NOT a clean C10 rescue: baseline A1/A2 held-out `para_full` 93.1/97.2 collapse to 0.0/0.0, and hard A7 `para_full` worsens 12.5 (9/72) to 1.4 (1/72). Scoped to this local fixed small-window transplant; upstream AnyEdit/AnyEdit++/muKE remain un-falsified. C10 remains open; F1 unchanged.
- Artifacts: `docs/C10_ANYEDIT_PILOT_PREREG.md`, `experiments/track_c/c10h_anyedit_pilot.py`, `results/c10h_anyedit_pilot.json`, `logs/c10h_anyedit_pilot.log`. Next diagnostic if continuing: A1/A2-only `window_size=50` or upstream-equivalent dependency/window behavior; require >=80% controls before A7.
