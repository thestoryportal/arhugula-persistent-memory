# Round-4 (single paragraph): C10Z §9.1 (b′4)

HARD: run no python of any kind (a live GPU run's gate refuses on any python process). Shell reads only.

In round 3 both reviewers flagged (b′4) in /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md and each supplied replacement text:
- Astra: /private/tmp/claude-501/reviews/c10z_s91_round3_astra.md (two sentence replacements)
- Advisor: /private/tmp/claude-501/reviews/c10z_s91_round3_advisor.md R3-1 (full paragraph replacement)
The lead merged them: the advisor's paragraph order, with Astra's two replacement sentences substituted for the conflicting ones ("Identity drift itself is not a §9(c) refusal…", "A prior REFUSED or INTERRUPTED record remains subject to…", "A prior STOP returns…", "The replacement benchmark's outcome remains subject to §9(c)…"). Read the merged (b′4) (grep -n "b′4" in the draft).

Check only: is the merged (b′4) internally consistent and consistent with prereg docs/C10Z_ASTRA_PREREG.md:457 (§9(c)) and EXPERIMENT_RUNBOOK.md:367 (D-C10z-budget: "A STOP, or a benchmark refused twice, returns to the operator")? Walk at least: (1) usable→drift→re-run REFUSED; (2) REFUSED→re-run usable→drift→drift re-run REFUSED; (3) usable→drift→re-run usable→drift again; (4) STOP→drift.
Output: first line PROCEED or FIX-FIRST; if FIX-FIRST, exact replacement text. Five lines max otherwise.
