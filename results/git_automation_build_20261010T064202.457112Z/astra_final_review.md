# Git automation final adversarial review

Final verdict: **PROCEED — build and fixture acceptance.** All eight review findings are closed in the final code and targeted regressions. This does **not** authorize or certify a real merge, push, branch/worktree deletion, or PR #21 admission. Real GitHub and Linux Actions behavior remain **UNVERIFIED**.

The next step is MAESTRO handoff with the exact tested files, CI suite, refusal receipts, and stated live limitations. No further implementation change is requested by this review.

Reviewer independence: GPT-family fallback with weaker independence; not a binding GPT-6-Astra or cross-family Claude signoff. This reviewer performed source/evidence inspection and wrote only its two allowed review artifacts. No real git mutation was performed by the reviewer.

## Final evidence and disposition

- `red_r5.log` records three targeted cases with five failing subtests before the final corrections; `red_r5.json` preserves the source hashes and exit 1.
- `green_r5.log` records **56 tests PASS in 44.408s**. `green_r5.json` records exit 0 and stable before/after hashes. Source inspection verifies native CPU checks are linked to the required exact-SHA CI workflow run for both PR and post-merge master checks. The mismatched-run regression fails both paths before the fix and passes afterward.
- Production `cwd_inventory` remains a global lsof scan. Absolute name fields that do not resolve to actual directories now refuse; unreadable/deleted placeholder regressions pass. The actual child-cwd positive control restricts PIDs only through its test runner wrapper, so it validates real same-user process observation without relaxing production enumeration. No claim is made that Linux-wide process visibility was empirically qualified.
- `assetfree_ci.json` and `assetfree_ci_0.log`, `assetfree_ci_1.log`, `assetfree_ci_2.log` record the exact workflow commands with **-B -S**, absent model/hf_cache/covariance_caches/.venv/results, generated-state PASS, **56 git automation tests PASS**, and **80 repository tests PASS**. Total measured local wall time is **47.438s**. The suite is `tools.test_c10w_p2_gate`, `tools.test_dashboard_live`, and `tools.test_dashboard_gpu_detector`, plus the dedicated git automation discovery suite. This is macOS Python 3.11 evidence, not a Linux Actions run or measured eight-minute cloud-runtime guarantee.
- Final read-only hygiene and PR #21 gate receipts both exit 1 on GitHub DNS/API failure, in **3.358s** and **3.205s** respectively. `real_dry_final_snapshot.json` records unchanged root, branch, HEAD, refs, worktree registrations, index SHA256, and index mtime. No cleanup or merge is admitted from unavailable evidence. The real root engine fingerprint passes; immutable live PR candidate and live CI admission remain unverified.
- The workflow uses the tested -B -S command shape, pinned actions, Python 3.11, only push-to-master and PR-to-master triggers, and an eight-minute job bound.

Final source hashes were independently re-read with `shasum -a 256` and match `assetfree_ci.json`:

| File | SHA256 |
|---|---|
| `tools/git_hygiene.py` | `2f54d6e062ce077897bb231526b635df5645acda7e34714e3470c4263d70821c` |
| `tools/git_merge_gate.py` | `c0abaa33a17d7db6c01f5723a6669a60e9bd57bd57b00a673cd09f62161f2984` |
| `tests/test_git_automation.py` | `d658df4ca7469e1a78f1752059f493c9757177faa7477beae4af58d7db8873e1` |
| `.github/workflows/ci.yml` | `d5998af13b0cd9e0617455b12fdaf681c05429e0969f6593d9e829f5dabff33f` |

The cooperative-lock limitation remains material: independent external master writes, new PRs, and processes starting after observation are not atomically excluded by this client tool. The merge path is a MAESTRO operating contract, not server-side branch protection. These are reported scope limits rather than claims of prevention.

## Historical review record — all findings below resolved

Historical verdict: **FIX-FIRST — superseded by the final PROCEED verdict above.**

This is the same GPT-family fallback reviewer used for the design review, with weaker independence. It is not a binding GPT-6-Astra or cross-family Claude signoff. No real git mutations were executed by this reviewer.

The most important next step is to add regression tests for the normal GitHub commit-status response and for a local branch changing after eligibility inspection, then correct the implementation before completion.

## Initial findings

1. `tools/git_merge_gate.py:34–36` indexes `status["sha"]`, but rows returned by the selected `/commits/{sha}/statuses` REST endpoint do not contain this field. Normal successful legacy statuses therefore cause a KeyError and false refusal. Official response shape: https://docs.github.com/en/rest/commits/statuses . Bind the response to the immutable requested SHA, validate its returned status URL or use a surrounding combined-status SHA, and add realistic nonempty status fixtures.

2. `tools/git_hygiene.py:368–369` deletes a local branch by name after a separate eligibility recheck. `git branch -d` uses its own upstream/HEAD merge test, which is not an atomic test against the approved old OID or the reviewed origin/master. A concurrent writer can advance the branch after the check. Add an invocation-scoped reference-transaction expected-old-OID guard, preserving any existing hook, plus a fixture where the new tip is upstream-merged but not master-merged.

3. `tools/git_merge_gate.py:175–183` checks head/base stability before the full hygiene scan, then merges without repeating that check. The scan can take substantial time; add the final head/base/master check after this scan immediately before merge. Test base movement during the scan.

4. `tools/git_hygiene.py:373` extracts final branches while ignoring the final inspect result errors/ok. Remote/PR/process failure in this last verification can yield a success report. Propagate final refusal and retain completed action evidence. Add a final-inspection failure regression.

5. `.github/workflows/ci.yml:4` has unrestricted push events, although the proposed design promised push-to-master and PR-to-master only. Restrict push branches to master and assert both filters structurally.

6. Set `GIT_OPTIONAL_LOCKS=0` for read-only git inspection so status cannot refresh the real index. Test the relevant invocation environment. Deadline construction currently occurs outside CLI error handling, so invalid timeout can produce traceback instead of the requested one-line refusal; validate timeout and finite bounded wait arguments.

The root has received these findings before finalizing. The initial 45 passing fixture tests (`green_r2.log`: 45 tests in 31.623s; `green_r2.json`: exit 0) do not cover these defects. The then-current candidate suite receipt showed `tools.test_dashboard_gpu_detector` failing because required small experiment source files were absent from the extraction, so final CI selection acceptance is pending a corrected asset-free run.

## Evidence already supported

The reviewed fixtures exercise real disposable Git bare remotes, clones, worktrees, pre-advertisement remote branch movement, during-receive branch movement, preserved rejecting pre-push hooks, ignored/submodule worktree content, and an actual lsof positive control. Remote deletion guard uses the advertised old OID, not only a stale local tracking ref. CI checks and separate post-merge master checks are represented independently. Full live GitHub/API acceptance is unavailable in current dry-run receipts and must remain UNVERIFIED.

## Remaining boundary

Even corrected client-side automation cannot atomically prevent independent external base writes, newly opened PRs, or a process entering a worktree after observation. Shared locks serialize cooperating MAESTRO invocations only. No server-enforced-only-path guarantee is established. Real merge, push, deletion, Linux Actions execution, and actual PR #21 admission are outside this build review evidence.

## Context handoff rule

Watch reviewer and orchestrator context remaining. Before approximately 20% remains, stop new work, append done/in-flight/exact paths/next step/open risks into the report, and notify the orchestrator for a fresh successor. Every handoff must restate this rule. Current state: full implementation and initial evidence read; corrective regressions and revised GREEN evidence pending; next action is review only changed code and new evidence, then replace this provisional verdict.

## Revision review: GREEN r4

The six original findings are now closed in the reviewed source and regressions. `green_r4.log` reports **54 tests PASS in 44.505s**; `green_r4.json` records exit 0 and equal before/after hashes for all four files. `red_r3.json` and `red_r3_cli.json` preserve the failing regressions before implementation. `green_r3.json` honestly records an intermediate exit 1; it is not acceptance evidence.

The local reference-transaction diagnostic (`local_hook_diagnostic.json`) observes all-zero old OIDs for deletion and a readable original branch SHA during `prepared`, followed by absence after `committed`. The revised guard reads the actual ref during `prepared`, while Git holds transaction locks, and preserves the pre-existing hook. Tests prove rejection of the advanced unmerged local tip and preservation of an existing hook veto. Normal deletion/idempotence passes in r4. This diagnosis supports the change without claiming Linux Git acceptance.

The source now accepts realistic legacy status rows without an invented SHA field; the SHA is checked in their status URL. Merge stability is checked after the last inventory. Final hygiene failure propagates with completed actions retained. Both workflow event filters target master. Optional index locking is disabled. Invalid/nonfinite/out-of-range CLI timing arguments produce JSON refusals without dispatch. Five merged branches are deleted with at most three full inventory/disk scans.

**Verdict remains FIX-FIRST for two newly requested edge checks:**

- Post-merge native `cpu` evidence is not linked to the exact required successful CI push run. `ci_state(..., post=True)` can accept a successful workflow named CI together with a CPU check supplied by another run. Add the same required-run linkage for native CPU evidence in the post-merge path, and a mismatched-run regression; preserve genuine zero/missing-check WAIT handling.
- `cwd_inventory` accepts every absolute `n/` field as a valid path, including Linux lsof placeholders such as `/proc/<pid>/cwd (readlink: Permission denied)`. The lsof primary source explicitly builds these names on failed cwd lookup (`lib/dialects/linux/dproc.c`, lines 883–929): https://raw.githubusercontent.com/lsof-org/lsof/master/lib/dialects/linux/dproc.c . Reject unreadable/error/deleted/nonexistent cwd entries as unknown visibility. A fixture-child positive control may use a test-only PID-scoped real lsof invocation to avoid unrelated privileged Ubuntu processes; production enumeration must stay global and fail closed. Actual Linux execution remains UNVERIFIED.

Next: review only these final changes and their test receipts. No further scope expansion or real git mutations are needed.
