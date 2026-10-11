**ACCEPT** for the current runbook. No blocking regression found.

1. **The §13 span is correct today.** `EXPERIMENT_RUNBOOK.md:848` is the final `## ` heading; no later level-2 heading exists. Lines 851–858 contain legitimate dated changelog entries before the first `### §13` heading. Including that text restores valid history. A preamble-only D-ID would also pass, but the gate’s documented contract is section presence/current fingerprint, not validation of a dated entry.

2. **Boundary limitations remain, nonblocking for this fix.** `tools/closeout_check.py:118,128` accepts heading prefixes and extends §13 to EOF. Synthetic probes confirmed that a token under a hypothetical later `## §14`, or under `## §130` without §13, satisfies the §13 check. Neither structure exists in this runbook. These limitations also existed under the old substring semantics; this fix should not be described as a general Markdown section parser.

3. **No caller dependency on the old extraction found.** `tools/git_hooks/pre-commit:13` invokes `--audit`, which exits through `tools/closeout_check.py:134–150` before section extraction. `render_state.py` only mentions the checker in its documentation; the source search found no dashboard caller relying on its spans.

4. **Tests are behavioral and sufficient for this narrow regression.** `tools/test_closeout_check.py:30–48` checks observable inclusion, exclusion, and missing-heading behavior. Independently reproduced **5/5 GREEN**, and **exactly 2/5 failures with old semantics**. Also reproduced the five real-runbook comparisons: only §13 and summaries changed, with precisely the reported exit codes. Optional coverage: retain the initial bullet-form history and exercise fingerprint status through the extracted span.

Read-only review; no files changed.

