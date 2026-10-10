# Autonomous git automation — MB4 build report

Initial staging record, superseded by the final build acceptance below; no real merge/push/branch or worktree deletion authorized for this build. Operator-approved brief: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb4_git_prompt.txt`. NEW-1 follow-up is on hold. This infrastructure protects the repository evidence and F1 reproducibility; it is not scientific evidence.

Owned deliverables: `.github/workflows/ci.yml`, `tools/git_merge_gate.py`, `tools/git_hygiene.py`, `tests/test_git_automation.py`, this report. Detailed receipts: `results/git_automation_build_20261010T064202.457112Z`. Tests execute mutations only in temporary bare remotes/clones/worktrees under `/private/tmp`; real checkout operations remain read-only. No reset/clean/rm/force deletion/push, daemon/schedule, commits or protected-file edits.

Design: one bounded explicit invocation, default read-only hygiene; fresh remote and complete open-PR protection evidence required for apply. Checked-out branches stay protected from branch deletion; independently verified idle, clean, merged, non-default/non-PR/non-current worktrees may be removed nonforce, then their branches are reclassified. Invocation-scoped pre-push SHA guard preserves existing hooks and verifies advertised remote old OID before nonforce deletion. Apply tools share a common-dir lock. Merge gate verifies exact head SHA, all terminal successful checks and required CI workflow/job, engine fingerprint, current master included, fresh branch/worktree inventory and unchanged head/base before server-side merge; separate master push CI on merge commit precedes post-merge hygiene. Dirty unrelated WIP is permitted. No automatic conflict repair, retry or re-run.

CI candidates are actually run from `/private/tmp/git_automation_assetfree_oo3c97bs`, extracted tracked repo code/docs only; model/hf_cache/covariance_caches/results/.venv are absent. Receipts `ci_candidates.json` list each command, exit and time. CI selection and precise exclusions will be recorded after GREEN. GitHub network verification currently fails (API connection/DNS), while local remote URL and worktree refs are available; remote facts/private-plan/protection/PR state remain UNVERIFIED until a successful live read.

Root and branch verified at start; concurrent worktrees/WIP are preserved. Session tooling instructions required one repository index lookup despite the brief requesting no graft: exactly one call, ~149,666 tokens / $0.08 reported saved; no further graft use.

**BINDING context directive (operator 2026-10-09):** watch Context N% left in every root/team session; before approximately 20%, stop starting new work, write done/in-flight/exact paths/next step/open risks into this report, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; never approach full-window compaction.

## Final build acceptance — GIT AUTOMATION BUILD DONE

Recorded 2026-10-10T07:43:13.418364+00:00. **136/136 asset-free CPU tests PASS (56 automation + 80 repository); generated-state check PASS.** Final exact CI command sequence: **45.053 s** locally against the workflow **480 s / 8 min** job cap. This is measured macOS Python 3.11.16 / Apple Git 2.54.0 evidence; Linux Actions startup/runtime remains UNVERIFIED. No real commits, pushes, merges, branch deletions, worktree removals, fetches, or conflict resolutions were performed by MB4. Test mutations were confined to disposable bare remotes/clones/worktrees under /private/tmp.

### Final design and MAESTRO operating contract

`tools/git_hygiene.py` defaults to one dry run. Apply performs one origin fetch, inventories local and freshly advertised remote branches, and requires complete bounded open-PR protection evidence. MERGED means the tip is an ancestor of the reviewed origin/master. Master/remote default, attached worktree branches, and open PR heads remain protected. UNMERGED branches are reported with unique-commit count/date/remote presence and are never deleted. Unknown remote/PR/process visibility refuses admission.

Worktrees are separately eligible only when merged, fully clean (including untracked, ignored and submodule content), unlocked, non-current, non-default, non-detached, non-PR, and without any observed process cwd inside. Removal is nonforce; prune happens once only after an admitted removal. Branches are then reclassified. Per-worktree disk bytes are retained before/after; original and completed action evidence survive a later refusal. A second successful apply has no cleanup actions, although each explicit apply still performs its one fetch.

Local deletion uses `git branch -d` with a temporary invocation-only reference-transaction guard. Git supplies zero old OIDs for this deletion; the prepared hook reads the actual tip while Git holds the ref lock and compares it with the reviewed SHA. The existing configured hook is chained with its state/input and veto respected. Remote deletion uses `git push origin --delete` with a temporary pre-push guard requiring the advertised old SHA and only the requested deletion; receive-pack also compares that advertised old OID atomically. The existing pre-push hook is chained; persistent hooks/config are not rewritten. Branch rechecks refresh remote/master, PR protection, attachments and tip without repeating full branch metadata/disk scans for each branch. Five-branch fixture cleanup performs at most three full inspections.

`tools/git_merge_gate.py` is the MAESTRO merge entrypoint: OPEN same-repository PR targeting master; immutable head/base recorded; current-root engine fingerprint and committed-head engine fingerprint; current master included in the head; only master + live attached worktree branches + selected PR branch; all exact-head current checks/statuses and latest workflow runs terminal-success, including required CI/cpu linked to the actual run. No checks means not-started and bounded backoff, never green. Head/base/master/mergeability are rechecked after the final inventory immediately before server-side `gh pr merge <n> --merge --match-head-commit <sha>`. Draft ready happens only after preconditions pass. Dirty unrelated WIP does not prevent a server-side merge. Conflicts/unknown mergeability refuse for operator resolution.

After the server returns an exact-head merge commit and master points to it, master push CI is verified separately on that merge SHA, with native cpu linkage to that CI run. Only then does the gate execute one hygiene apply. A red master run or cleanup refusal exits nonzero with the recorded merge SHA; nothing automatically retries, re-runs, resolves conflicts or rolls back. A common-dir nonblocking lock serializes cooperating apply invocations. `GIT_OPTIONAL_LOCKS=0` prevents read-only status index refresh. Stdout is JSON; stderr lists checks/classifications and one final PASS/REFUSE reason.

| Bound | Frozen value |
|---|---|
| Hygiene default total deadline | 300 s |
| Merge gate default total deadline | 1200 s |
| Per CI phase wait | 480 s, also bounded by total deadline |
| Per subprocess | min(30 s, remaining deadline), then process-group termination and <=2 s reap |
| CI backoff | 1, 2, 4, 8, then at most 10 s; finite monotonic deadline |
| REST inventory pagination | At most 20 pages of 100; cap reached refuses incomplete evidence |
| Actions job | 8 min, one CPU job |

Timing CLI arguments must be finite, positive and <=1200 s; invalid inputs yield JSON plus one-line refusal before dispatch. There are no schedules, cron/launchd services, daemons, watchers, workflow chains or automatic retry loops. MAESTRO runs one hygiene apply and one merge-gate apply at arc closeout; these commands were **not executed on the real repo** in this build:

~~~sh
LLMDB_ROOT="$PWD" python3 -B -S tools/git_hygiene.py --apply
LLMDB_ROOT="$PWD" python3 -B -S tools/git_merge_gate.py 21 --apply
~~~

The only-path rule is a MAESTRO operating contract. Canonical CLAUDE/AGENTS/permission changes are MAESTRO-owned and were not edited by this builder. Client checks/locks cannot atomically prevent independent external master writes, newly opened PRs, or a process entering a worktree after observation. Server-enforced branch protection, private/free-plan/403 claims, live Actions and PR #21 state are UNVERIFIED here because GitHub access failed.

### RED / GREEN audit

| Receipt/log | Observed result |
|---|---|
| [red.json](git_automation_build_20261010T064202.457112Z/red.json) | 42 FAIL before both implementation modules existed; production absence recorded before/after |
| [green_attempt_1.json](git_automation_build_20261010T064202.457112Z/green_attempt_1.json) | 42 tests, 1 FAIL: wrong-post-master fixture moved the base before merge; fixture corrected, no production workaround |
| [red_r2.json](git_automation_build_20261010T064202.457112Z/red_r2.json) | 2 targeted tests, 1 FAIL: gh exit-1 no-checks must enter bounded not-started polling |
| [green_r2.json](git_automation_build_20261010T064202.457112Z/green_r2.json) | 45 PASS, 31.623 s |
| [red_r3.json](git_automation_build_20261010T064202.457112Z/red_r3.json) | 10 targeted cases; 22 failing assertions/subtests and 2 errors; production hashes unchanged |
| [red_r3_cli.json](git_automation_build_20261010T064202.457112Z/red_r3_cli.json) | 1 isolated CLI case, 15 failing subtests; empty temporary root, production unchanged |
| [green_r3.json](git_automation_build_20261010T064202.457112Z/green_r3.json) | 54 tests, 5 FAIL: local guard assumed nonzero hook old OID; not acceptance |
| [green_r4.json](git_automation_build_20261010T064202.457112Z/green_r4.json) | 54 PASS, 44.505 s after actual hook-interface diagnosis |
| [red_r5.json](git_automation_build_20261010T064202.457112Z/red_r5.json) | 3 cases, 5 failing subtests: wrong CI-run cpu links and unreadable/deleted lsof placeholders; real child control passed |
| [green_r5.json](git_automation_build_20261010T064202.457112Z/green_r5.json) | 56 PASS, 44.408 s |
| [assetfree_ci.json](git_automation_build_20261010T064202.457112Z/assetfree_ci.json) | State PASS; 56+80 PASS, 47.438 s; first exact workflow snapshot |
| [assetfree_ci_r2.json](git_automation_build_20261010T064202.457112Z/assetfree_ci_r2.json) | State PASS; 56+80 PASS, 45.053 s; final refreshed source snapshot |


All RED receipts retain pre/post source hashes. Initial module-absence RED, targeted regression RED and final GREEN were observed before acceptance. The initial invalid-CLI regression also performed unintended read-only inventory on the real root before validation existed; it was narrowed to a temporary empty root before implementation. No apply/merge was dispatched. Only the final dry-run snapshot proves unchanged index bytes/mtime; earlier dry runs were not qualified for optional index refresh.

The actual zero-old-OID diagnosis is [local_hook_diagnostic.json](git_automation_build_20261010T064202.457112Z/local_hook_diagnostic.json). Regressions exercise advanced remote tips before advertisement and during receive; advanced local unmerged tips; custom hook veto; dirty/ignored/submodule/in-use worktrees; complete PR pagination; absent/pending/failed/conflicting checks; moved head/base; extra merged/unmerged branches; candidate engine changes; separate red master CI; preserved WIP; dry-run immutability; idempotent cleanup; final-verification error retention; CLI deadlines; both workflow branch filters; disabled optional index locks; and bounded full inspection count.

A fresh GPT-6-Astra reviewer inspected source/receipts and closed eight findings with **PROCEED — build/fixture acceptance** in [astra_final_review.md](git_automation_build_20261010T064202.457112Z/astra_final_review.md); [astra_design_review.md](git_automation_build_20261010T064202.457112Z/astra_design_review.md) records the design review. This is a GPT-family fallback with weaker independence, not cross-family approval or a binding program ruling. Initial `claude auth status` probe returned exit 1 and `loggedIn:false`; no authenticated Claude review was claimed. Reviewer changed only its two review artifacts. The final refreshed CI snapshot retains the same four approved source hashes.

Primary references: [GitHub commit statuses](https://docs.github.com/en/rest/commits/statuses) returns status rows without a SHA field; the status URL is bound to the requested immutable SHA. [Git reference-transaction hooks](https://git-scm.com/docs/githooks) documents locked prepared transactions. [Linux lsof source](https://raw.githubusercontent.com/lsof-org/lsof/master/lib/dialects/linux/dproc.c) emits unreadable-cwd placeholders; production rejects paths that do not resolve to actual directories. The real lsof child positive control scopes only its test runner to self+child; production remains global and refuses incomplete visibility.

### CI selection and exact pins

Triggers are only push branches [master] and pull_request branches [master]. Pull-request checkout explicitly uses the PR head SHA. One ubuntu-24.04 CPU job has timeout 8 minutes, Python 3.11, thread limits 1, empty CUDA device selection and bytecode suppression. Every Python command uses -B -S, disabling all site packages; no pip dependency installation, model or GPU is needed. Git and lsof must be present.

| Selected command (each with LLMDB_ROOT=$PWD) | Final result | Why selected |
|---|---|---|
| `python3 -B -S tools/render_state.py --check` | PASS, 0.023 s | Five generated blocks checked using code/docs |
| `python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v` | 56 PASS, 43.284 s wall | Disposable Git fixtures and new safety/CI contracts |
| `python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector` | 80 PASS = 13+27+40, 1.746 s wall | Existing stdlib process/admission/dashboard regressions |

Selected candidates were actually tried individually in [ci_candidates.json](git_automation_build_20261010T064202.457112Z/ci_candidates.json). The first GPU-detector candidate failed because extraction omitted small experiment source files; it was not a model/asset failure. Adding tracked experiment code, while retaining absent large assets, yielded 40 PASS in [candidate_3_fullcode.json](git_automation_build_20261010T064202.457112Z/candidate_3_fullcode.json). The exact final workflow commands passed in [assetfree_ci_r2.json](git_automation_build_20261010T064202.457112Z/assetfree_ci_r2.json); complete logs are assetfree_ci_r2_0.log, _1.log, _2.log.

Excluded entrypoints:

- `tests/test_new1_geometry.py`, `tests/test_new1_supervisor.py`, `tests/test_new1_construction_diag.py`, `tests/test_new1_identity_diag.py`: NEW-1 follow-up is explicitly on hold and separate from this Git baseline.
- `tools/test_backup_gdrive.py`, `tools/test_backup_gdrive_addendum.py`: backup work/tests are under active MB3 ownership and outside this intake.
- `tools/test_dashboard_mathlab.py`: concurrent protected WIP; MathLab is outside this build.
- `tools/labviz/test_mathlab.py`, `tools/labviz/test_labviz.py`: separate visualization acceptance workflow, not this CPU Git baseline.
- `tools/test_dashboard_report.py`: its separate suite was not admitted as a candidate while provider sources changed concurrently; some provider paths are exercised by the selected dashboard tests.

These exclusions are scope/qualification choices, not empirical claims that every unselected suite requires models or cannot pass. Live scientific scripts, model/torch/MPS/CUDA suites, browser/Node checks and external backup/merge operations are outside CI.

The snapshot contains small tracked code/docs and the four new source files, with no model, hf_cache, covariance_caches, .venv or real results tree. Python is supplied externally from the local interpreter but -S proves no site-package dependency. Exact file identities are in assetfree_ci_r2_manifest.json. Concurrent docs/dashboard changes detected after the initial snapshot were copied only into the temporary snapshot; the full CI sequence was rerun once. assetfree_ci_r2_refreshed.json records these identities. The real current generated-state check also passed (current_state_check.json). Existing dashboard tests emit unclosed-file ResourceWarnings; these were retained, not suppressed or fixed outside scope. Final automation tests have no such warnings.

| Pin | Value |
|---|---|
| actions/checkout v4.2.2 | `11bd71901bbe5b1630ceea73d27597364c9af683` |
| actions/setup-python v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| Python CI minor / measured local | 3.11 / 3.11.16 |
| Runner | ubuntu-24.04 (live UNVERIFIED) |
| Required workflow / job | CI / cpu |
| Target branch / merge mode | master / merge commit with exact-head guard |
| Engine SHA256 / _cov_cpu sites | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` / 3 |

Action SHAs were checked against official release commit links: [checkout commit](https://github.com/actions/checkout/commit/11bd71901bbe5b1630ceea73d27597364c9af683), [setup-python commit](https://github.com/actions/setup-python/commit/a26af69be951a213d495a4c3e4e4022e16d87065).

| Final file | SHA-256 |
|---|---|
| `tools/git_hygiene.py` | `2f54d6e062ce077897bb231526b635df5645acda7e34714e3470c4263d70821c` |
| `tools/git_merge_gate.py` | `c0abaa33a17d7db6c01f5723a6669a60e9bd57bd57b00a673cd09f62161f2984` |
| `tests/test_git_automation.py` | `d658df4ca7469e1a78f1752059f493c9757177faa7477beae4af58d7db8873e1` |
| `.github/workflows/ci.yml` | `d5998af13b0cd9e0617455b12fdaf681c05429e0969f6593d9e829f5dabff33f` |


### Real read-only dry runs

Receipts: [real_hygiene_final_receipt.json](git_automation_build_20261010T064202.457112Z/real_hygiene_final_receipt.json), [real_gate_final_receipt.json](git_automation_build_20261010T064202.457112Z/real_gate_final_receipt.json); full stdout JSON and stderr logs are separately retained. [real_dry_final_snapshot.json](git_automation_build_20261010T064202.457112Z/real_dry_final_snapshot.json) proves root/branch/HEAD/refs/worktree registrations/index SHA256/index mtime unchanged over these final invocations. Recorded HEAD: `b19a45664f0cc26548a6c93a8f85251833c46789`; cached origin/master: `f6c1f421af6f183f8545739280852b245f05964a`. Later coordinator commits are separate concurrent activity.

~~~sh
LLMDB_ROOT="$PWD" python3 -B -S tools/git_hygiene.py --dry-run --timeout 180
LLMDB_ROOT="$PWD" python3 -B -S tools/git_merge_gate.py 21 --dry-run --timeout 180 --ci-wait 2
~~~

Hygiene exited **1 / REFUSE in 3.358 s**: GitHub DNS could not resolve; the open-PR API could not connect. It reported **47 branches: 34 local (31 MERGED, 3 PROTECTED), 13 cached remote (11 MERGED, 2 PROTECTED)**. Every deletion eligibility is false because remote/PR protection is unverified; actions are empty. The **31 local and 11 cached remote merged branches are conditional candidates**, not authorized deletion recommendations; open-PR/default/remote existence must first be verified. No branch with unique commits is eligible.

| Kind | Branch | Classification | Unique vs cached master | Last commit date | Tip | Protection / remote presence |
|---|---|---|---|---|---|---|
| local | `master` | PROTECTED | 0 | 2026-10-04T20:40:26-06:00 | `557a58bc5384` | default/master; checked out in worktree; remote existence UNVERIFIED |
| local | `orx/h-1-shared-value-objective-across-prompt-formats` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-10-surprisal-boundary-second-key-anyedit-under` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-11-token-level-target-reweighting-and-forward` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-12-hypernetwork-that-emits-a-fixed-lora-delta` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-13-merged-band-lora-write-trained-on-paraphras` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-14-sparse-lora-restricted-to-the-rows-the-edit` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-15-full-parameter-fine-tuning-of-the-band-on-a` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-16-preference-objective-injection-rl-or-dpo-ov` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-17-sparse-memory-layer-slots-as-the-write-site` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-18-minted-token-written-by-embedding-only-tuni` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-19-two-minted-tokens-per-value-one-per-coined` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-2-robust-key-adapter-rep` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-20-constructed-embedding-for-the-minted-row-to` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-21-qwen2-5-7b-untied-as-the-model-line-for-the` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-22-qwen3-8b-base-olmo-2-7b-pythia-6-9b-llama-3` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-23-mimo-7b-base-a-pretraining-objective-that-a` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-24-post-training-mtp-heads-on-qwen2-5-3b-itsel` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-25-llada-8b-base-or-dream-7b-as-the-diagnostic` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-26-olmo-2-7b-with-a-covariance-drawn-from-its` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-27-olmoe-1b-7b-with-the-moe-aware-closed-form` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-28-mamba-2-8b-or-falcon3-mamba-7b-with-rome-st` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-29-entity-lens-readout-at-the-keyed-position-s` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-3-direct-end-to-end-w-optimisation-over-the-ba` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-30-weight-grafting-to-localise-where-a-fine-tu` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-4-covariance-from-model-generated-text-moir` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-5-leverage-score-pivot-key-inside-the-value-ma` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-6-per-position-per-layer-value-write-with-gate` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-7-betaedit-as-the-engine-for-the-incremental-w` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-8-dynamic-per-edit-layer-selection-loki-on-the` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/h-9-subject-anchored-per-sentence-residual-with` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `orx/research-pass-2026-10-06-hypothesis-ledger-no-ru` | MERGED | 0 | 2026-10-06T11:04:32-06:00 | `95503ff4587a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| local | `research-pass/2026-10-06` | PROTECTED | 9 | 2026-10-06T12:59:41-06:00 | `900aa8edeb9c` | checked out in worktree; remote existence UNVERIFIED |
| local | `worktree-c10k-route-a` | PROTECTED | 293 | 2026-10-10T01:27:53-06:00 | `b19a45664f0c` | checked out in worktree; remote existence UNVERIFIED |
| remote | `master` | PROTECTED | 0 | 2026-10-06T20:39:23-06:00 | `f6c1f421af6f` | default/master; checked out in worktree; remote existence UNVERIFIED |
| remote | `worktree-b3-local-serving` | MERGED | 0 | 2026-10-04T02:11:40-06:00 | `e7c60264c391` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-backup-tier` | MERGED | 0 | 2026-10-03T18:43:51-06:00 | `7b15a29607c3` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-c10k-m3pro-stage0` | MERGED | 0 | 2026-10-04T02:35:35-06:00 | `a686ec8ef373` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-c10k-reduction-note` | MERGED | 0 | 2026-10-04T02:40:55-06:00 | `47f443a1092c` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-c10k-route-a` | PROTECTED | 293 | 2026-10-10T01:27:53-06:00 | `b19a45664f0c` | checked out in worktree; remote existence UNVERIFIED |
| remote | `worktree-fix-graft-leak` | MERGED | 0 | 2026-10-04T02:37:36-06:00 | `e9f624515e4f` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-ignore-symlinks` | MERGED | 0 | 2026-10-03T19:12:52-06:00 | `243582428571` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-phase2-local-machine` | MERGED | 0 | 2026-10-03T19:09:23-06:00 | `1fb61637b4de` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-phase3-mps-port` | MERGED | 0 | 2026-10-04T01:35:49-06:00 | `19b9c7abe6b3` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-plist-install-note` | MERGED | 0 | 2026-10-03T18:52:06-06:00 | `1eb81314058a` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-reconcile-claude-ai-artifacts` | MERGED | 0 | 2026-10-03T18:25:29-06:00 | `cef63f2d6750` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |
| remote | `worktree-vendor-engine` | MERGED | 0 | 2026-10-03T18:34:41-06:00 | `88a8ece3748d` | none observed; PRs UNVERIFIED; remote existence UNVERIFIED |


Protected but unmerged: research-pass/2026-10-06 local has **9** unique commits; worktree-c10k-route-a local and cached remote each have **293** unique commits at this snapshot. MAESTRO must bring unmerged-branch decisions to the operator; these branches are never deleted by hygiene.

| Worktree path | Branch / state | Bytes before -> after | Eligible | Keep reasons |
|---|---|---|---|---|
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` | `master` | 75539791872 -> 75539791872 | NO | detached/default/open-PR worktree; dirty, untracked, ignored or submodule work; process cwd in worktree; remote/PR protection unverified |
| `/Users/robertrhu/.local/share/openresearch/worktrees/0a1375d4-8f79-44be-bea6-2a27f6658761/chat_3cd2ad17-33c5-4752-b9e0-9259bc163220` | `DETACHED` | 49487872 -> 49487872 | NO | detached/default/open-PR worktree; dirty, untracked, ignored or submodule work; remote/PR protection unverified |
| `/Users/robertrhu/.local/share/openresearch/worktrees/0a1375d4-8f79-44be-bea6-2a27f6658761/chat_73a1fdb0-4a98-49ce-9f9d-c16222391e61` | `DETACHED` | 51904512 -> 51904512 | NO | detached/default/open-PR worktree; dirty, untracked, ignored or submodule work; remote/PR protection unverified |
| `/Users/robertrhu/.local/share/openresearch/worktrees/0a1375d4-8f79-44be-bea6-2a27f6658761/chat_8376051e-0cc1-4c9c-94f6-eb257a489254` | `research-pass/2026-10-06` | 51580928 -> 51580928 | NO | dirty, untracked, ignored or submodule work; unmerged branch; remote/PR protection unverified |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` | `worktree-c10k-route-a` | 43982454784 -> 43982454784 | NO | current worktree; dirty, untracked, ignored or submodule work; unmerged branch; process cwd in worktree; remote/PR protection unverified |


All five worktrees are kept. Sizes are per-path allocated bytes from du -sk; the main checkout contains the nested current worktree, so those sizes must not be added. No disk was reclaimed.

PR #21 gate exited **1 / REFUSE in 3.205 s**. PR metadata/current candidate SHA and live checks could not be read; actual admission remains UNVERIFIED. Current-root engine fingerprint is PASS; committed PR fingerprint is NOT-RUN. All nine dry-run check slots are printed:

| Gate check | Recorded status | Detail |
|---|---|---|
| branches | FAIL | hygiene evidence incomplete: git exited 128: fatal: unable to access 'https://github.com/thestoryportal/arhugula-persistent-memory/': Could not resolve host: github.com; open-PR inventory unverified: gh exited 1: error connecting to api.github.com check your internet connection or https://githubstatus.com |
| ci | NOT-RUN | prerequisite unavailable |
| fingerprint | PASS | current-root PASS; immutable candidate NOT-RUN |
| master_ci | NOT-RUN | prerequisite unavailable |
| merge | NOT-RUN | prerequisite unavailable |
| post_hygiene | NOT-RUN | prerequisite unavailable |
| pr | FAIL | gh exited 1: error connecting to api.github.com check your internet connection or https://githubstatus.com |
| ready | NOT-RUN | prerequisite unavailable |
| stable_head_base | NOT-RUN | prerequisite unavailable |


No draft-ready, merge, post-merge wait, fetch or cleanup occurred. PR-green/master-green were never inferred from absence/API failure. Live conflict/draft/private/default-branch/branch-protection facts remain UNVERIFIED; origin URL is locally verified as https://github.com/thestoryportal/arhugula-persistent-memory.

### Scope, handoff and open boundaries

scope_audit.json compares 183 protected files with the start snapshot. It records 10 concurrent differences; MB4 did not write these paths or revert them:

- `AGENTS.md`
- `EXPERIMENT_RUNBOOK.md`
- `memory_mirror/MEMORY.md`
- `memory_mirror/backup-via-memitbackup-app.md`
- `memory_mirror/c10-accept-bounded-means-hybrid-not-general-db.md`
- `memory_mirror/codex-runs-inline-from-claude-bash.md`
- `memory_mirror/commit-forward-work-without-asking.md`
- `memory_mirror/durable-artifact-path-collision.md`
- `tools/backup_gdrive.sh`
- `tools/backup_gdrive_status.py`


Allowed builder writes are the workflow, two Git tools, dedicated test file, this report, its evidence directory and its location pointer. The reviewer writes only its two review artifacts. CLAUDE.md, NEW-1 sources/prereg, protected MathLab test and unrelated file families were not edited by MB4; concurrent WIP was preserved. Baseline HEAD and subsequent coordinator HEADs are separately recorded; there is no claim the entire shared tree stayed unchanged. Every repo shell command explicitly set LLMDB_ROOT=$PWD. No model/GPU/MPS/NEW-1 run occurred.

Done: A–E implemented; RED/GREEN retained; 136 final CPU tests and generated-state check PASS; source/action/engine pins retained; two real read-only refusal receipts; eight review findings closed; full branch/worktree inventory above. In-flight builder work: none after final receipt/source validation. Exact paths: .github/workflows/ci.yml, tools/git_hygiene.py, tools/git_merge_gate.py, tests/test_git_automation.py, results/git_automation_build_report.md, results/git_automation_build_20261010T064202.457112Z/.

Next: MAESTRO folds in its canonical operating/permission rules, obtains live GitHub CI/PR evidence, reviews protected unmerged branches, and invokes the explicit tools under that policy. This build performs no real mutation and makes no server-enforcement or Linux runtime claim. Open risks: unavailable live GitHub/Actions/PR #21 acceptance, external races beyond cooperative locks, platform-wide lsof visibility, pre-existing dashboard ResourceWarnings and concurrent source/doc drift. Future admission always needs actual current exact-head and merge-SHA checks.

**BINDING context directive (operator 2026-10-09, carried through every handoff):** watch Context N% left for root and team sessions. Before approximately 20% remains, stop starting new work, write done/in-flight/exact paths/next step/open risks into the task report, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; do not approach full-window compaction. A context-save closeout checkpoint is retained locally in the evidence directory; no global memory write or git checkpoint commit is made.

Context-save closeout: [20261010T074747.363421Z_git_automation_context.md](git_automation_build_20261010T064202.457112Z/20261010T074747.363421Z_git_automation_context.md). Final evidence/source/report digests are in [final_manifest.json](git_automation_build_20261010T064202.457112Z/final_manifest.json). No runtime code changed after the final CI receipt.
