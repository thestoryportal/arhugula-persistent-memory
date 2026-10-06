FIX-FIRST

Single most important next thing: revise v2 before implementation so the stacked result is scoped by the second write itself: bind/report `||ΔW2|| / ||ΔW1||` for pass S, and explicitly state that S-sham is a near-no-op seam control, not a magnitude-matched “two edits vs new target” control.

Issues, in priority order:

1. The sham is useful but under-controls the causal claim. A second in-place edit aimed back at `z_pre` is a good no-op/seam control because pass S-sham should have small residual after the first edit, but that also means it does not match pass S’s second-write energy. If S improves and S-sham is inert, the result still may be “new target plus larger second write,” not cleanly “new target.” The prereg currently uses S-sham thresholds of ±5/72 and `ΔW2 ≤ 0.25 × ΔW1`, but pass S only gets a total-write qualifier at `>2.0`, which could hide a large second edit below 2× total. `docs/C10Q_STACKED_SOLVE_PREREG.md:29`, `docs/C10Q_STACKED_SOLVE_PREREG.md:38`.

2. Prefer a second-write qualifier over the 2.0 total cap. For two stacked edits, total ratio is blunt; `ΔW2/ΔW1` is the direct confound. Prior C10p already showed a 1.31 total ratio with locality cost and per-layer ratios up to 1.57, so “under 2.0” is not automatically benign. `CORPUS/49_C10P_TWOPASS_SOLVE.md:18`, `CORPUS/49_C10P_TWOPASS_SOLVE.md:23`.

3. Sequential setting is intended, but the prereg should name the projector/covariance confound. `my_edit` recomputes keys on the current model and then appends `K Kᵀ` to the arm cache, so using the first edit’s cache for the second edit matches sequential editing. But `P` is computed once before arm edits from the covariance SVD, then reused, so this is “edited-model keys plus accumulated request cache under a base-covariance null-space projector,” not a fully re-estimated edited-model projector. `experiments/track_c/c10e_bandknob.py:166`, `experiments/track_c/c10e_bandknob.py:181`, `experiments/track_c/c10e_bandknob.py:218`, `experiments/track_c/c10e_bandknob.py:454`.

4. The solve-state handle is acceptable under LAW#5 only if default inertness is made explicit in implementation review. The current harness already runs LAW#5 before each recipe, and hooks run only while the edit is applied before restore. That supports the seam, but the prereg should require the implementation review to show the handle is read-only by default and does not alter no-hook output. `experiments/track_c/c10e_bandknob.py:411`, `experiments/track_c/c10e_bandknob.py:488`, `EXPERIMENT_RUNBOOK.md:177`.

5. §4 mostly has the right non-claims, but add two more. Say: “S-sham inactive does not prove the gain is target-specific under matched write magnitude,” and “LEAD/PARTIAL is a harness-side mechanism lead only, not §8.9 contract closure.” The latter matters because the spec’s write contract is behavioral post-write readback, and C10q is only one write-path mechanism arm against that surface. `docs/C10Q_STACKED_SOLVE_PREREG.md:42`, `docs/SPEC_E2E_GROUND_TRUTH.md:64`, `CORPUS/48_C10O_MAGNITUDE_DIRECTION.md:32`.

Cheapest overturning test: keep S-sham, but add or at least pre-register a matched-energy negative control if runtime allows: second edit with `||residual||` matched to S but with target directions permuted across subjects or otherwise semantically wrong. If that also improves, “new target” is overturned; if it does not, S becomes much cleaner.

Drift check: this does advance F1 indirectly because C10 is an open write-path/blocking condition, but any positive result must remain “lead, not closure.” The prereg already says LEAD is not an F1 change; keep that hard boundary. `docs/C10Q_STACKED_SOLVE_PREREG.md:40`, `docs/C10Q_STACKED_SOLVE_PREREG.md:44`.

graft saved ~4,919 tokens this turn.