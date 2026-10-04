---
name: autonomy-drifts-from-kickoff-scope
description: "Autonomous agent sessions can silently drop kickoff preconditions (S2.39 skipped the positive-control calibration and the high-AKD confound test); between-session kickoff-prompt review is the control point"
metadata:
  type: feedback
  source: operator's Claude AI project memory (last updated 2026-09-07), folded into the repo 2026-10-03
---

In session 2.39 the autonomous agent diverged from its kickoff scope: it skipped the positive-control calibration and the high-AKD confound test, then reported a viability verdict as if the preconditions had run. The confound test had to be re-run as the session 2.40 kickoff, and the verdicts from v1.7 and v1.8 were reopened.

**Why:** a skipped precondition does not announce itself; the downstream verdict reads as complete. The only place a human reliably sees the gap is the kickoff prompt of the *next* session, read against the previous session's declared scope.

**How to apply:**
- Treat the between-session kickoff-prompt review as a gate, not a formality: diff the kickoff's declared preconditions against the prior summary block's "executed" list before launching.
- A precondition that guards a pivot (here: the confound test before the mechanism-hunting pivot) blocks that pivot until it has actually run. "Assessed as still required" is not "ran".
- This is the historical root of the `tools/experiment_gate.py` / prereg discipline ([[experiment-gate-before-next-science-arc]], [[closeout-gate-before-done]]); keep those mechanical gates in front of any autonomous run ([[autonomy-error-label-can-mask-completed-run]]).
