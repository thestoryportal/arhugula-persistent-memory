# Review brief — D-C10s-sharedz amendment A2 (design + implementation), before any GPU run

You are the cross-family reviewer for a pre-registered experiment. Review only; do not run anything that loads the model (no GPU), do not edit any file except your output file. Write your review to **`results/c10s_sharedz_codex_a2_review.md`** (model and effort in its header line), then say DONE.

## Context (read these, in order)
1. `results/c10s_sharedz_halt_analysis_2026-10-06.md` — why the first inertness run HALTED: (iii) rel 0.122, (iv) NLL Δ 0.0117 vs a frozen 1e-4; the diagnosis is fp16 batch-shape/grad-mode rounding amplified along the clamp sphere. Raw record: `results/c10s_sharedz/inertness.json` (`checks.*.solve.history`).
2. `docs/C10S_SHARED_Z_PREREG.md` §2 "Inertness", §2 cell 1 screen rule, and the new **§7 A2** (the amendment under review).
3. The implementation diff: `/usr/bin/git diff HEAD -- experiments/track_c/c10s_sharedz_read.py experiments/track_c/c10s_sharedz_inertness.py experiments/track_c/c10s_sharedz_selftest.py docs/C10S_SHARED_Z_PREREG.md`. Engine source for reference: `memit_dry_run/memit/memit/compute_z.py` (unmodified; must stay so). Driver: `experiments/track_c/c10s_sharedz_arms.py` (unchanged).
4. The model-free selftest passes: `.venv/bin/python experiments/track_c/c10s_sharedz_selftest.py` (you may run it; it loads no model).

## Questions to answer
1. **Diagnosis.** Do the recorded trajectories support "rounding, not a code-path difference"? Name any alternative explanation the records do not rule out (e.g. a plan/ordering or padding difference between the 7-row and 19-row batches).
2. **τ.** Is τ = 2 × max(s_a, s_b) the right calibration? Does s_a (the (ii) solve, bit-identical to the engine, vs the unpadded no-grad reference) measure the axis on which (iv) differs? Is the 0.05 anomaly cap sound?
3. **(iii) replacement.** Do step-0 objective equivalence + trajectory equivalence + canonical-injection equality still catch the bugs (iii) existed for (duplicate-prompt plan, mean over rows, target_init/clamp/weight-decay from prompt 0)? Is dropping the end-point gate justified? Are ±2 clamp steps and ±0.01 final NLL defensible?
4. **(iv) positive control.** Does a one-position target shift represent the bug class (iv) guards? Is "mean |Δ| ≥ 10 τ" the right bar?
5. **(vi) noise twin.** Is engine z vs `compute_z_shared([CANON]*3)` the right rounding-only twin for the cell-1 screen (same objective as the canonical z, same 19-row batch as the real shared solve)? Is "passes the screen in neither direction" the right gate? Does it belong in the inertness gate, or should it be a recorded calibration only?
6. **Implementation.** Bugs, wrong indices, wrong fields, rules that live outside the reader, anything recorded but not gated that should be (or the reverse), stale comments. Check `injects_full` uses the same calls as the driver's `injection_cell`, and that the reader's new print reads fields that the inertness record actually holds (`run.json["inertness"]`).
7. **Provenance.** The driver refuses to run if any source file's hash differs from the inertness record; confirm the edited files are in `SOURCE_FILES` and that a rerun in a new `OUT_DIR` is the correct procedure.

## Output format
Header line: reviewer, model, effort, date. Then **Verdict: PROCEED or FIX-FIRST**. Then numbered items, each with file:line, the problem, and the exact fix. Mark each item BLOCKING or ADVISORY. Disagree with the amendment where the evidence says so; do not soften. A FIX-FIRST must name what would turn it into PROCEED.
