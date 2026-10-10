# MB7 git automation fix build

Status: **BUILD DONE; GATED on binding Astra GO.** Authority: MAESTRO5 brief and the unchanged NO-GO verdict at `results/git_automation_build_20261010T064202.457112Z/astra_binding_verdict.md`, findings 1–2. MB7 made no commit/push/merge or hygiene/merge apply against the real repo. No model, torch, MPS, .venv, or science job launched.

## Changes and evidence

- `git_hygiene --apply` keeps every worktree. Eligible worktrees are `manual_removal_candidates` with path, branch, head SHA and size; stderr labels them as manual candidates. Production command receipts assert that neither worktree removal nor pruning dispatches. Local/remote merged branches with no worktree still delete under the existing guards.
- Both real-repo fixture races execute their writer **after** the second completed real worktree inspection. Before the fix, this is the last inspection before removal; after the fix, it is the final overall inspection. The tests assert that the writer fired and no later inspection of that worktree occurred. The ignored packet survives; the new detached commit remains reachable from worktree HEAD and the combined reflogs.
- Exact-head CI is re-read after ready(), the final hygiene inventory, and final stable() call, immediately before merge dispatch. Pending, failed, absent and differently-headed evidence refuse without merging. The final CI evidence is retained in the report.
- After dispatch succeeds, `merged=true` persists. The returned commit's first parent is read through the bounded commit-object adapter and must match the recorded base. A mismatch reports `MERGED_ON_MOVED_BASE`; CI failure/timeout, moved master, parent-read failure and post-hygiene failure report `MERGED_WITH_FAILURE`, keeping `merge_sha`. The CLI also distinguishes the merged outcome. Clean completion is `MERGED`; pre-merge refusal is `REFUSED`; read-only success is `DRY_RUN_PASS`.
- All three dashboard timestamps use `birthtime_or_mtime()` and `getattr(st, "st_birthtime", st.st_mtime)`. Real run_rows() and complete render() tests exercise missing-birthtime stat results, including sorting and completed-run timing. Native-birthtime controls retain 65-second durations; fallback controls complete with zero-second durations.

## Test-first receipts

**19/19 regressions saved RED, then 19/19 GREEN:** 18 new tests and one revised worktree-policy test. The old automatic-removal expectation contradicted the required interim policy; the revised test strengthens preservation, exact candidate metadata, attached refs, size, idempotence and executed-command assertions. Other existing tests/assertions remain intact. `regression_receipts.json` links each test to its separate RED/GREEN log; RED2 preserves corrected RED runs for the timestamp tests and differently-headed CI schedule. Initial logs remain available.

| Acceptance command | Result | Receipt |
| --- | --- | --- |
| `LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v` | 74 PASS, exit 0, 46.555 s | `green_git_automation.log` |
| `LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector` | 80 PASS, exit 0, 2.461 s | `green_model_free.log` |

The three model-free counts are **13 + 27 + 40**. Commands ran raw under an RTK proxy shell, foreground, with TMPDIR confined to this receipt's fixtures directory. Local `/usr/bin/python3` is **3.9.6** on macOS; CI remains Ubuntu 24.04 / Python 3.11. **Ubuntu is UNVERIFIED until the live rerun.** Existing dashboard unclosed-file ResourceWarnings appear in RED native controls and acceptance logs (8 in automation, 31 in model-free); unrelated file-handling code was left untouched. Scoped `git diff --check` passes (`diff_check.log`).

## Workflow and residual race

`.github/workflows/ci.yml:3–7` has push/master and pull_request/master with no `types`. GitHub defaults pull_request to opened, synchronize and reopened; ready_for_review is excluded. Therefore gh pr ready does not create a new CI run on the same head for this workflow, and the final read refuses pending evidence immediately. The workflow, runner and detector inclusion are unchanged. Source: [GitHub event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request).

Client-side checks narrow the window but do not close it: checks or master can change between the final read and merge dispatch, and parent/post-merge checks detect failure after a merge without undoing it. The remaining premise is that **MAESTRO is the only merger and the only writer to master**. Server-side enforcement is unavailable: MAESTRO5 checked the private/free-plan repository at 2026-10-10 08:15Z and received 403 “Upgrade to GitHub Pro” for branch protection and rulesets. This build neither adds nor calls those APIs; the operator rules on any spend. Binding Astra re-review and writer coordination remain required before merging.

The exact-commit parent endpoint is documented in [GitHub's Git commit API](https://docs.github.com/en/rest/git/commits#get-a-commit-object). A read-only live probe failed with a network error (`parent_api_probe.log`); live adapter behavior remains UNVERIFIED. Fixture tests cover valid, wrong-SHA, missing and malformed parent JSON.

## SHA-256 and scope

| Changed file | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `tests/test_git_automation.py` | `a15b02c79d2c7b26e011a0dc0f28c4a07fef7d623161d5836ecde0867938f9da` | `5187fc993491be5c9504d8a21b88afbfa4cc3655919746aacb9bbb983027b35c` |
| `tools/dashboard_experiment.py` | `40e6dd310446935e660ec81aea2aa8d0655b4218de320abff2737e224cb0d772` | `96d0e142f90020f63d1381c39dedcf5cd0cea14620ffce5f6d93b0aac5b62052` |
| `tools/git_hygiene.py` | `2f54d6e062ce077897bb231526b635df5645acda7e34714e3470c4263d70821c` | `1980929aadb716d85a9766dec18d57c96891c12854e24864941691a3f2c5d544` |
| `tools/git_merge_gate.py` | `c0abaa33a17d7db6c01f5723a6669a60e9bd57bd57b00a673cd09f62161f2984` | `8e1ea0caae4e5bbb3b17a4927b7ce9c463f1e380508f154ad1874474994199c7` |

`before_manifest.json` and `after_manifest.json` include byte counts and protected-file snapshots; `before/`, `after/` and `changes.diff` preserve reviewable source evidence. MB7 source edits are exactly these four files. The workflow, binding verdict, AGENTS.md, CLAUDE.md, runbook and tools/test_dashboard_mathlab.py hashes remain unchanged. Concurrent protected-file drift was observed in `tests/test_new1_construction_diag.py`, `tools/backup_gdrive.sh`, `tools/backup_gdrive_status.py`, `tools/launchd/MemitGdriveBackup.applescript`; those files were not edited or reverted by MB7. Other sessions' work remains present. Full status snapshots are `git_status_before.txt` and `git_status_after.txt`. HEAD advanced concurrently from `1ba14c753a85768bd2dd356d3ad3b17348c6e13b` to `5620b948ea6f88d6efcb352ebce32d8cadfef816` for a NEW-1 review-receipt commit (`head_drift.log`); the branch/root did not switch and all four owned source hashes still match the tested snapshot.

Session context, remaining gates and the binding context directive are saved in `context_save.md`. Evidence here is local CPU/fixture evidence, not live GitHub/Ubuntu or scientific execution.
