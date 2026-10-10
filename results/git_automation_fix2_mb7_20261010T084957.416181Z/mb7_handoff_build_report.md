# MB7 Task 2 context handoff — NOT DONE

Stopped starting work at the approximately 20% context threshold, per the binding directive. **13 new regressions have saved RED. Production fixes, GREEN and full acceptance remain UNRUN.** Do not emit the completion token yet.

## Authority and exact paths

- Brief: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb7_task2_prompt.txt` (read in full).
- Binding NO-GO r2: `results/git_automation_build_20261010T064202.457112Z/astra_binding_r2_verdict.md` (read in full). Task 1 findings 1, 2, 5 are closed; leave those fixes intact.
- Repo/worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`; HEAD at Task 2 start `af8b5da3da3d5b94a75c0d0eac886dde2d9879b4`. Verify current HEAD/branch before resuming; another builder/coordinator is active.
- This receipt: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/git_automation_fix2_mb7_20261010T084957.416181Z`.
- Task 1 is committed at `19fac9c`; MAESTRO reports exact-head Linux run `38038772117` passed. That validates Task 1, not these unimplemented changes.

## Completed and in flight

Only `tests/test_git_automation.py` has changed. Added contextmanager import, FakeGh run_attempt / check id / updated_at metadata, and a validated-response-shaped return value from FakeGh.merge (production still ignores it). Added 13 tests: lock-exit OSError; lock-exit ValueError through main; first post-merge PR query failure; older pending same-SHA run; increased run_attempt during final inventory; rerun between final read and merge; new head check/status; changed updated_at/conclusion; REST merge response/command; invalid REST merge shapes; evidence adapter metadata/full inventories. All 13 ran individually against unchanged production and failed as expected. Read `RED/index.json` and separate logs. The evidence-adapter regression errors on the old adapter consuming the proposed REST JSON shape; the other regressions fail assertions reproducing the r2 defects.

Receipt-local `run_regressions.py` was copied from Task 1. It compares test names with `before/tests/test_git_automation.py`, runs raw system Python per case, sets TMPDIR to this receipt's fixtures, and saves logs. `test_plan.md` records the acceptance plan before implementation. No tests were deleted or weakened. The existing 74 tests are preserved; after the 13 additions the full automation suite should contain 87 tests (UNRUN).

**No process remains running.** RED runner completed with exit 0, meaning 13 expected failures and no unexpected results. No production file was edited. No real git/gh mutation API, model/GPU/.venv job, commit, push, merge, or apply against the real repo was run.

## Proposed minimal implementation — not yet written

1. `tools/git_hygiene.py`, `Gh.merge`: replace gh pr merge with `self.json(['api','-X','PUT',f'repos/{self.repository}/pulls/{number}/merge','-f','merge_method=merge','-f','sha='+sha])`. Require a dict, merged **is True**, and a string matching 40 lowercase hex; otherwise raise Refusal. Return the validated `{merged: True, sha: ...}` response. Capture report merged/SHA immediately from that return, before gh.pr/first_parent/master/evidence queries. Keep merge-only strategy and exact-head sha parameter. Test adapter command and response against mocks only; real merge API is forbidden.
2. Use ONE report object through gate() and main(). Suggested small constructor plus error-recording helper; main creates the report before try and passes it into gate via an optional report argument. Never replace it on exception. Every exception path sets ok=false; after merged=true preserve merge_sha and MERGED_WITH_FAILURE (retain the specific MERGED_ON_MOVED_BASE status where applicable). Catch ordinary Exception at the diagnostic boundaries so lock-exit ValueError/RuntimeError cannot escape and erase the report. Record each error explicitly.
3. Finalize success only **after** the with-lock statement has exited successfully. Current assignments at the bottom of the with body cause OSError exit to retain ok=true. Remove those assignments from the critical section; after it completes without errors assign ok=true/status MERGED (or DRY_RUN_PASS). Early refusal returns still exit the context and must be covered by the same report-preserving outer catch. Existing named checks stay unchanged to retain the current exact-check-set test.
4. Workflow data currently comes from gh run list, whose selected JSON omits run_attempt/updated_at. Use a bounded read-only REST actions/runs query with `head_sha`, `per_page=100`, plus master/push filters for post-merge master CI. Map id/head_sha/head_branch/event/name/status/conclusion/html_url to the current evidence keys and retain run_attempt/updated_at. Keep the existing 100-row fail-closed cap. Native success proof can retain filter=latest, but add a separate filter=all check-run inventory and retain all raw commit statuses as `all_check_runs` / `all_statuses` for the audit. This gives complete tracking without making historical status failures the current-status authority. Update the existing absent-check adapter fixture JSON sequence to the new documented response shapes without weakening its assertions. The new adapter fixture supplies five responses: PR checks, workflow_runs, latest checks, all checks, statuses.
5. In ci_state(), reject every workflow run that is not completed/successful, before reducing to latest workflow/event/branch. Name the run id in the reason. This catches the older pending run that latest-id selection currently hides. Keep all Task 1 exact-SHA/native-link checks.
6. Pure snapshot/difference helpers should compare workflow runs by databaseId, native check runs by id, and statuses by id; retain name/context and fields run_attempt, status/state, conclusion, updated_at. Prefer the complete inventories when present, falling back to existing fake evidence for tests. Name added/removed ids and changed fields in errors. Reject any higher run_attempt at the final read versus the last successful earlier CI sample; rejecting any changed snapshot at that boundary is consistent with the cooperative rule. Save final evidence as now.
7. After capture and post-merge PR/parent validation, re-read the head's evidence (post=False) and compare against the final pre-merge snapshot. Any new/changed run/check/status => MERGED_WITH_FAILURE, keep exact merge SHA, identify the difference and explicitly say detection **does not undo the merge**. Save audit evidence/differences in the same report. The critical rerun test starts the rerun inside FakeGh.merge, after the final evidence read; master/post-merge CI remains successful, so only the new audit can make it non-PASS.

The report should include this exact cooperative rule paragraph for MAESTRO to adopt (MB7 must not edit CLAUDE.md/AGENTS.md):

> While the merge gate holds git_automation.lock, no actor may push master, change the PR head, edit or close/reopen the PR, rerun CI, or create/update check runs or commit statuses for the candidate head. Previously triggered runs must finish successfully before the final admission read. MAESTRO is the only merger and writer to master, and every actor with permission to perform these actions must honor this critical section until the gate releases its lock. Post-merge detection of a violation reports failure and does not undo the merge.

Primary docs were read through web tools, with no mutation API execution: https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request and https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository . Cite those in the final build report if describing API contracts. Runtime behavior of the new REST adapter remains UNVERIFIED until an authorized live use. Do not call protection/ruleset APIs.

## Exact next step and verification

Implement the above inside only tools/git_hygiene.py / tools/git_merge_gate.py and the owned test file. Then run:

```sh
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S results/git_automation_fix2_mb7_20261010T084957.416181Z/run_regressions.py GREEN
export TMPDIR="$PWD/results/git_automation_fix2_mb7_20261010T084957.416181Z/fixtures"
export PATH="/opt/homebrew/bin:$PATH"
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector
```

Save raw full acceptance logs and exit codes in this receipt; expected 87 and 80 tests, but report actual counts. Every further new test needs its own saved RED before production changes for that behavior. Finish before/after SHA-256, diff, short build report, and context-save. Only when complete reply `GITAUTO FIX2 BUILD DONE` with counts. No merge until binding Astra GO. System Python is 3.9.6; Task 2 Ubuntu/Python 3.11 remains UNVERIFIED until the new live rerun.

## SHA-256 at handoff

| Allowed file | Before | Handoff snapshot |
| --- | --- | --- |
| `tools/git_hygiene.py` | `1980929aadb716d85a9766dec18d57c96891c12854e24864941691a3f2c5d544` | `1980929aadb716d85a9766dec18d57c96891c12854e24864941691a3f2c5d544` |
| `tools/git_merge_gate.py` | `8e1ea0caae4e5bbb3b17a4927b7ce9c463f1e380508f154ad1874474994199c7` | `8e1ea0caae4e5bbb3b17a4927b7ce9c463f1e380508f154ad1874474994199c7` |
| `tests/test_git_automation.py` | `5187fc993491be5c9504d8a21b88afbfa4cc3655919746aacb9bbb983027b35c` | `d08234668b1642028845eb71c053dcacd6fed5cfef1874f5b4988c5718359128` |

`before_manifest.json`, `handoff_manifest.json`, `handoff_snapshot/`, `changes_at_handoff.diff`, and status snapshots preserve the exact unfinished state. Do not mistake the handoff snapshot for a GREEN implementation.

## Binding context directive — restate in every successor handoff

Operator: “Do not forget to manage context usage for yours and every team session you are orchestrating.” / “This context directive must be made durable through any and all handoffs.” Watch Context N% left. At roughly 20%, stop starting work, write a handoff into the task report with done/in-flight work, exact paths, next step and risks, and notify MAESTRO to start a fresh successor. Never approach full-window compaction. Every successor handoff restates this directive.

## Scope and open risks

No edits to .github/, CLAUDE.md, AGENTS.md, memory_mirror/, backup_gdrive*, tools/launchd/, tools/new1_*, tests/test_new1_*, results/mathlab_staging/, or tools/test_dashboard_mathlab.py. Do not use graft. Another builder owns backup/launchd and NEW-1 work; preserve all concurrent changes. Do not commit/push/merge, call real merge/ready/rerun APIs, delete outside receipts, or apply the real gate/hygiene. Keep tests short and foreground; no .venv/native/science jobs. If GPU-LIVE arrives, finish the current command and run no Python until GPU-CLEAR. No server-side protection enforcement is available; operator rules on spend.
