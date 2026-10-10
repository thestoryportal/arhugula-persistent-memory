VERDICT: NO-GO

1. none found — `tools/git_hygiene.py:397` contains no worktree removal/pruning path; attached branches remain protected at `:282` and `:391`. Both regressions execute their writers after the last completed inspection and assert that no later inspection occurred (`tests/test_git_automation.py:235`). The ignored artifact survives (`:253`); the detached commit remains reachable through HEAD/reflogs (`:267`). Finding 1 is closed.

2. none found — the exact-head CI reread follows `ready()`, final hygiene and final `stable()`, immediately before merge dispatch (`tools/git_merge_gate.py:179`, `:183`, `:189–195`). PENDING, FAIL, absent and differently-headed evidence refuse; the corresponding schedules appear at `tests/test_git_automation.py:510–554`. This closes the earlier-read gap, subject to finding 4.

3. **Post-merge reporting still violates the requested contract.** In-memory probes against the current code reproduced:
   - Lock exit raises `OSError` after successful cleanup: `tools/git_merge_gate.py:227–230` retains `ok=True`; the CLI prints PASS and returns **0 despite the error**.
   - Lock exit raises `ValueError`: it escapes `gate()` and `main()` replaces the merged report with **REFUSED, merged=false, merge_sha=null** (`:250–251`).
   - The first post-merge PR read fails: `merged=true` survives, but `merge_sha=null` (`:195–200`).

   **Fix:** finalize success only after lock exit; preserve one report across exception boundaries; every post-merge exception must set `ok=false` and retain the merged outcome/SHA. Have the merge adapter capture and return the SHA from the successful [merge API response](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request), before subsequent queries. Add these three regressions.

4. **The stated premise is insufficient.** `.github/workflows/ci.yml:3–7` excludes `ready_for_review`, but that does not exclude manual reruns or close/reopen events. [GitHub permits reruns on the same SHA](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs?tool=cli). Schedule: final evidence passes at `tools/git_merge_gate.py:190`; another actor reruns CI; merge dispatches at `:195` while head CI is pending. My in-memory probe returned exit-0 PASS with this schedule and unchanged master.

   **Smallest control:** extend exclusive ownership to a coordinated critical section covering master writes, PR/head changes, reruns and check/status updates, from before fresh CI verification through merge completion. All relevant actors must participate; previously triggered runs must finish first. This cooperative control requires **no GitHub Pro**. “Only master writer” alone does not provide it.

5. none found — `tools/dashboard_experiment.py:131–133` retains native birthtime and falls back to mtime. All three callers use it (`:143`, `:296`, `:308`). Tests exercise real `run_rows()` and `render()` with missing/native birthtime, including duration and rendered-content assertions (`tests/test_git_automation.py:949–990`).

6. **First use, after fixes and re-review:** establish finding 4’s coordination; create an isolated detached integration worktree sharing the existing inventory; fetch and merge `origin/master` without force; run generated-state verification and both suites; push the candidate normally; obtain successful exact-head Linux CI; run hygiene `--apply`, then merge-gate `--apply`, retaining receipts. Stop on conflicts/failures; require post-merge master CI before completion (`tools/git_merge_gate.py:144`, `:213–225`). Hygiene **never removes worktrees**; retain the integration worktree until separately authorized, owner-coordinated removal.

Reviewed HEAD `19fac9c`; all four hashes matched. Full suites were not rerun here.

🌱 graft saved ~62,297 tokens (~$0.04), 1 successful call.