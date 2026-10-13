FIX-FIRST

**BLOCKING — N2’s insertion is verbatim, but contradictory wording remains at [D:38](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md:38).** It says a refused drift rerun counts, then unconditionally says “It is not a §9(c) refusal.” It also sends every first REFUSED/INTERRUPTED record to the operator, whereas §9(c) permits one rerun.

Replace:

> A record that was REFUSED, INTERRUPTED or STOP stays under §9(c) and returns to the operator, whatever changes afterward.

with:

> A prior REFUSED or INTERRUPTED record remains subject to §9(c)’s one-rerun allowance and cumulative refusal count; identity changes neither reset that count nor grant a drift replacement. A prior STOP returns to the operator regardless of later changes.

Replace:

> It is not a §9(c) refusal, and it does not use up §9(c)’s one re-run.

with:

> Identity drift itself is not a §9(c) refusal and does not consume its one-rerun allowance. The replacement benchmark’s outcome remains subject to §9(c): REFUSED or INTERRUPTED increments the cumulative refusal count, and STOP returns to the operator.

Brief notes:

- **Other five blockers resolved:** Astra 1 at D:5/B:62; Astra 2 at B:265; Astra 3 at B:309/391; Astra 4 at D:84/B:289; N1 at B:5/35. N1’s P3 extension is appropriately stricter. Superseded-wording search found no other substantive conflict.
- Lens placement, warm-up, `benchmark_module()` seam and full stage-3 command introduce no new prereg contradiction. **The lead’s Cost change at D:100 is acceptable.** Fold-map R11 remains stale about where authorization/time is recorded.
- Declined A-1/A-7/A-8 are acceptable within the stated controlled-workflow and visualization scope. A-9 remains required before appending §9.1; A-10’s sequencing disposition is acceptable.
- Non-blocking: B:324 should explicitly fail if its bounded wait expires without `t_attempt` or T finishing; otherwise delayed scheduling can still satisfy `T.is_alive()`.
- The cited budget row has moved: **D-C10z-budget is currently EXPERIMENT_RUNBOOK.md:367**, not :365. Prereg SHA remains `e2d7fa10…eca50`. No Python or GPU execution.

🌱 graft reported ~94,868 tokens saved (~$0.06), 1 call.

