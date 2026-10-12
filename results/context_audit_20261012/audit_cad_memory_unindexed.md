# CAD — unindexed and retired memory audit

As-of: 2026-10-12 UTC. Read-only audit of the supplied 18 unindexed entries, 41 tombstones and MEMORY.md; only this report was written. The list contains **17 memory notes plus one historical checkpoint snapshot**, not 18 ordinary notes. No science, model, backup, network or mutable tmux/git command was run.

Prior audit references below use `results/memory_audit_20261010/`. HISTORICAL + keep means **retain the current de-indexed archival status**; it is not a request to re-index. KEEP on a tombstone means retain its retirement and valid redirect. Bytes are UTF-8 item spans, including line endings; overlapping spans are not additive. Proposed actions are for a later operator-approved hygiene step.

## Findings

| item (file:line-range or note filename) | bytes | verdict(s) | evidence (file:line or command) | proposed action | replacement text (only when the item should stay, at most 200 characters) |
|---|---:|---|---|---|---|
| memory_mirror/SESSION_CHECKPOINT.md:1-531 | 132381 | HISTORICAL, BLOAT | Header dates June state at :4-24; pod relaunches :305-342 and obsolete hardware :495-517. Current authority CLAUDE.md:66; EXPERIMENT_RUNBOOK.md:41-47; tools/engine_fingerprint.py:34. Read-only line comparison: 421/432 nonempty lines also occur in root SESSION_CHECKPOINT.md. | move-to docs/session_summaries/memory_checkpoint_20260621.md |  |
| memory_mirror/autonomy-drifts-from-kickoff-scope.md:1-16 | 1646 | HISTORICAL | Prior closure APPLIED.md:39 (in results/memory_audit_20261010); precondition lesson already survives in tools/experiment_gate.py and memory_mirror/closeout-gate-before-done.md:8-12. No re-index regression. | keep |  |
| memory_mirror/c10-edit-collateral-breaks-injected-target.md:1-12 | 1510 | HISTORICAL | CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:14-18,30-33 supports counts; prescribed transport was executed in CORPUS/47_C10N_ZTRANSPORT.md:12-17. Prior de-index APPLIED.md:52. | keep |  |
| memory_mirror/c10-edit-rotates-required-target-direction.md:1-12 | 1389 | HISTORICAL | CORPUS/48_C10O_MAGNITUDE_DIRECTION.md:14-22,26-32 supports assay; the routed two-pass arm ran (CORPUS/49_C10P_TWOPASS_SOLVE.md:8-18). Prior de-index APPLIED.md:53. | keep |  |
| memory_mirror/c10-layerpick-null.md:1-12 | 1360 | HISTORICAL | CORPUS/56_C10V_LAYERPICK.md:3,9-11 supports NULL, counts and map scope. Prior de-index APPLIED.md:54. | keep |  |
| memory_mirror/c10-secondkey-null-large-write.md:1-12 | 1598 | HISTORICAL | CORPUS/53_C10T_SECONDKEY.md:1,11-17; CORPUS/56_C10V_LAYERPICK.md:3 records later executed step 4. Prior de-index APPLIED.md:57. | keep |  |
| memory_mirror/c10-sharedz-underfit.md:1-14 | 2621 | HISTORICAL | CORPUS/51_C10S_SHAREDZ.md:6,10-16; CORPUS/52_C10S_SOLVEFEAS.md:9,25-28,48-52 verifies merged follow-up and its paired 29-to-2 comparison. Prior de-index/merge APPLIED.md:58. | keep |  |
| memory_mirror/c10-stacked-solve-tradeoff.md:1-12 | 1719 | AMBIGUOUS, HISTORICAL | Description :3 says "a 1.24× write"; body :8 does not distinguish second-write from accumulated cost; CORPUS/50_C10Q_STACKED_SOLVE.md:15,19 distinguishes second/first ratio 1.24 from accumulated total 2.24. Both readings change perceived write cost. | fix-text: qualify second-write and accumulated ratios; keep de-indexed | The second write is 1.24 times the first; the accumulated write total is 2.24 times the first. This is a historical TRADEOFF, not a gain with clean locality. |
| memory_mirror/c10-twopass-solve-null-at-margin.md:1-12 | 1476 | HISTORICAL | CORPUS/49_C10P_TWOPASS_SOLVE.md:8,14-18,29 supports NULL, sham and locality; source and override consumption are documented at :3,10. Prior de-index APPLIED.md:62. | keep |  |
| memory_mirror/c10w-ceiling-oracle-result.md:1-12 | 1341 | HISTORICAL | CORPUS/57_C10W_ORACLE_FINAL.md:9,16,22-28,54-56 verifies replicated 70/72, G4/G6 and NO-GATE-CLEAN-REFERENCE. Prior de-index APPLIED.md:65. | keep |  |
| memory_mirror/c10x-enginepath-result.md:1-12 | 1933 | HISTORICAL | CORPUS/58_C10X_ENGINEPATH.md:11-14,66-70 confirms NULL and erratum INVALID-CONTROLS-UNDERFIT; Known-reader warning is retained at :8,12 for archived-output rereads. Prior de-index APPLIED.md:66. | keep |  |
| memory_mirror/codex-watch-anchor-tokens-read-context-from-rollout.md:1-16 | 1845 | DUPLICATE, MISLEADING | Old :10,16 recommends pane anchoring; surviving memory_mirror/codex-watch-anchor-replies-read-context-from-rollout.md:17 proves even anchored pane text false-matches and requires assistant rollout messages; MEMORY.md:134 indexes survivor. Read-only comparison: 11/12 nonempty old lines match survivor. | retire | RETIRED: use [[codex-watch-anchor-replies-read-context-from-rollout]]; match assistant rollout messages, not echoed pane text. |
| memory_mirror/exhaust-options-before-blocked.md:1-12 | 1550 | KEEP | Prior de-index APPLIED.md:96; durable re-search behavior is consistent with operator-profile-and-standing-directive.md:16-18 and remains reachable through codex-runs-inline-from-claude-bash.md:10. Keep de-indexed; no new route authorization inferred. | keep |  |
| memory_mirror/mbp-command-line-tools-broken.md:1-12 | 1381 | HISTORICAL | Prior de-index APPLIED.md:130; read-only /usr/sbin/pkgutil --pkg-info com.apple.pkg.CLTools_Executables returned exit 0, version 27.0.0.0.1788430756. AGENTS.md:76 retains long-job constraints. No compile/build attempted. | keep |  |
| memory_mirror/perplexity-c10h-reranks-anyedit-failure-geometry-first.md:1-24 | 1551 | HISTORICAL | CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md:8,12-16 records executed parity result; memory_mirror/method-ports-need-replication-faithfulness-gate.md:17-23 carries active-trace/easy-control lesson. Prior de-index APPLIED.md:153. | keep |  |
| memory_mirror/q4km-quantization-survival-pass.md:1-16 | 3220 | HISTORICAL | CORPUS/17_B3_QUANTIZATION_SURVIVAL.md:18-23 verifies historical retention. Its :12-14 Intel/E1/next-run language is archival: EXPERIMENT_RUNBOOK.md:87,91 records M3 serving and retired Intel target; current per-tensor lesson lives in prior-art-chrishayuk-larql-2026-10.md:14. Prior de-index APPLIED.md:167. | keep |  |
| memory_mirror/scope-gate-batch-is-deployment-model.md:1-12 | 1933 | HISTORICAL | June batch-only decision is expressly corrected in docs/B3_IN_WEIGHT_NECESSITY_DECISION.md:62,123,134; M3 target AGENTS.md:70. Prior de-index APPLIED.md:181. Its "next" quantization instruction must not be used as current queue. | keep |  |
| memory_mirror/wide-intermediate-7b-editing-vram.md:1-20 | 3024 | HISTORICAL | Current M3 scope AGENTS.md:70 and CPU solve memit_dry_run/memit/memit/memit_main.py:196-204; historical identities remain in experiments/track_b/b1_size_dose_response.py:72,100. CUDA allocations/timings are explicitly unmeasured on MPS (:8). Prior de-index APPLIED.md:194. | keep |  |
| memory_mirror/anyedit-clearing-c10-would-close-tested-write-serve-scope.md:1-7 | 685 | KEEP | `git show fd77f7e:memory_mirror/anyedit-clearing-c10-would-close-tested-write-serve-scope.md`: exit 0, 551 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-connectedpapers-adds-diagnostics-not-plan-change.md:1-7 | 643 | KEEP | `git show fd77f7e:memory_mirror/anyedit-connectedpapers-adds-diagnostics-not-plan-change.md`: exit 0, 519 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-default-window-collapses-c10-a7.md:1-7 | 625 | KEEP | `git show fd77f7e:memory_mirror/anyedit-default-window-collapses-c10-a7.md`: exit 0, 497 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-gate-upgraded-by-muke-coin-suit.md:1-7 | 619 | KEEP | `git show fd77f7e:memory_mirror/anyedit-gate-upgraded-by-muke-coin-suit.md`: exit 0, 562 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md, prior-art-anyeditpp-2026.md. | keep |  |
| memory_mirror/anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md:1-7 | 620 | KEEP | `git show fd77f7e:memory_mirror/anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md`: exit 0, 642 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-local-transplant-controls-fail-before-a7.md:1-7 | 613 | KEEP | `git show fd77f7e:memory_mirror/anyedit-local-transplant-controls-fail-before-a7.md`: exit 0, 1165 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-precommit-triage-proceed-but-viability-gated.md:1-7 | 560 | KEEP | `git show fd77f7e:memory_mirror/anyedit-precommit-triage-proceed-but-viability-gated.md`: exit 0, 607 bytes; :7 replacement(s) resolve to live notes: anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md. | keep |  |
| memory_mirror/anyedit-token-alignment-gate-prevents-false-rescue.md:1-7 | 484 | KEEP | `git show fd77f7e:memory_mirror/anyedit-token-alignment-gate-prevents-false-rescue.md`: exit 0, 640 bytes; :7 replacement(s) resolve to live notes: anyedit-noop-gate-is-not-active-edit-parity.md. | keep |  |
| memory_mirror/autoresearch-is-not-a-faithfulness-gate.md:1-7 | 496 | KEEP | `git show fd77f7e:memory_mirror/autoresearch-is-not-a-faithfulness-gate.md`: exit 0, 848 bytes; :7 replacement(s) resolve to live notes: autoresearch-editing-loop-per-fork.md. | keep |  |
| memory_mirror/background-monitor-no-premature-read.md:1-7 | 530 | KEEP | `git show fd77f7e:memory_mirror/background-monitor-no-premature-read.md`: exit 0, 1750 bytes; :7 replacement(s) resolve to live notes: never-idle-arm-completion-watch.md. | keep |  |
| memory_mirror/c10-band-knobs-failed-for-hard-coined-values.md:1-7 | 469 | KEEP | `git show fd77f7e:memory_mirror/c10-band-knobs-failed-for-hard-coined-values.md`: exit 0, 454 bytes; :7 replacement(s) resolve to live notes: c10-memit-knobs-failed-before-anyedit.md. | keep |  |
| memory_mirror/c10-solvefeas-underfit-at-50.md:1-7 | 402 | KEEP | `git show fd77f7e:memory_mirror/c10-solvefeas-underfit-at-50.md`: exit 0, 1881 bytes; :7 replacement(s) resolve to live notes: c10-sharedz-underfit.md. | keep |  |
| memory_mirror/c10-status-and-session-b-residual-test.md:1-7 | 605 | KEEP | `git show fd77f7e:memory_mirror/c10-status-and-session-b-residual-test.md`: exit 0, 4671 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. | keep |  |
| memory_mirror/c10k-route-a-resume.md:1-7 | 611 | KEEP | `git show fd77f7e:memory_mirror/c10k-route-a-resume.md`: exit 0, 21881 bytes; :7 replacement(s) resolve to live notes: seed-freezes-context-templates.md, closeout-gate-before-done.md, llmdb-root-env-points-at-main-checkout.md, test-first-one-round-builds.md. Reviewer-output race lesson is now live in codex-runs-inline-from-claude-bash.md:19 (prior Astra finding 4 closed). | keep |  |
| memory_mirror/c10z-stage1-underfit-terminal.md:1-7 | 552 | KEEP | `git show fd77f7e:memory_mirror/c10z-stage1-underfit-terminal.md`: exit 0, 436 bytes; :7 replacement(s) resolve to live notes: c10-sharedz-underfit.md. | keep |  |
| memory_mirror/canonical-fit-is-not-c10-rescue.md:1-7 | 468 | KEEP | `git show fd77f7e:memory_mirror/canonical-fit-is-not-c10-rescue.md`: exit 0, 475 bytes; :7 replacement(s) resolve to live notes: c10-memit-knobs-failed-before-anyedit.md. | keep |  |
| memory_mirror/codex-chatgpt-oauth-model-slug.md:1-7 | 558 | KEEP | `git show fd77f7e:memory_mirror/codex-chatgpt-oauth-model-slug.md`: exit 0, 1865 bytes; :7 replacement(s) resolve to live notes: model-and-compute-allocation.md. | keep |  |
| memory_mirror/codex-review-embed-evidence-and-effort.md:1-7 | 597 | KEEP | `git show fd77f7e:memory_mirror/codex-review-embed-evidence-and-effort.md`: exit 0, 1586 bytes; :7 replacement(s) resolve to live notes: codex-runs-inline-from-claude-bash.md. | keep |  |
| memory_mirror/deployment-target-intel-cpu.md:1-7 | 599 | KEEP | `git show fd77f7e:memory_mirror/deployment-target-intel-cpu.md`: exit 0, 7882 bytes; :7 replacement(s) resolve to live notes: local-only-no-rented-compute.md. | keep |  |
| memory_mirror/e2e-ground-truth-situate-on-the-map.md:1-7 | 465 | KEEP | `git show fd77f7e:memory_mirror/e2e-ground-truth-situate-on-the-map.md`: exit 0, 2217 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. | keep |  |
| memory_mirror/experiment-gate-before-next-science-arc.md:1-7 | 541 | KEEP | `git show fd77f7e:memory_mirror/experiment-gate-before-next-science-arc.md`: exit 0, 1099 bytes; :7 replacement(s) resolve to live notes: method-ports-need-replication-faithfulness-gate.md. | keep |  |
| memory_mirror/gemma4-rung4-candidate.md:1-7 | 573 | KEEP | `git show fd77f7e:memory_mirror/gemma4-rung4-candidate.md`: exit 0, 1666 bytes; :7 replacement(s) resolve to live notes: local-only-no-rented-compute.md. | keep |  |
| memory_mirror/gpu-gate-blocks-any-python.md:1-7 | 471 | KEEP | `git show fd77f7e:memory_mirror/gpu-gate-blocks-any-python.md`: exit 0, 1794 bytes; :7 replacement(s) resolve to live notes: gpu-gate-refuses-any-venv-python.md. CLAUDE.md:30 still names this retired note alongside the survivor; repair that inbound reference, not the gate. | keep |  |
| memory_mirror/in-weight-vs-sidestore-f1-question.md:1-7 | 534 | KEEP | `git show fd77f7e:memory_mirror/in-weight-vs-sidestore-f1-question.md`: exit 0, 2606 bytes; :7 replacement(s) resolve to live notes: in-weight-necessity-is-scope-keyed-hybrid.md. | keep |  |
| memory_mirror/larql-the-mechanism-prior-art.md:1-7 | 529 | KEEP | `git show fd77f7e:memory_mirror/larql-the-mechanism-prior-art.md`: exit 0, 6407 bytes; :7 replacement(s) resolve to live notes: prior-art-chrishayuk-larql-2026-10.md. | keep |  |
| memory_mirror/llm-db-local-migration-gaps.md:1-7 | 613 | KEEP | `git show fd77f7e:memory_mirror/llm-db-local-migration-gaps.md`: exit 0, 5380 bytes; :7 replacement(s) resolve to live notes: local-only-no-rented-compute.md, backup-via-memitbackup-app.md. | keep |  |
| memory_mirror/llmdb-root-points-at-main-checkout.md:1-7 | 499 | KEEP | `git show fd77f7e:memory_mirror/llmdb-root-points-at-main-checkout.md`: exit 0, 1094 bytes; :7 replacement(s) resolve to live notes: llmdb-root-env-points-at-main-checkout.md. | keep |  |
| memory_mirror/local-only-hardware-rule.md:1-7 | 478 | KEEP | `git show fd77f7e:memory_mirror/local-only-hardware-rule.md`: exit 0, 1339 bytes; :7 replacement(s) resolve to live notes: local-only-no-rented-compute.md. | keep |  |
| memory_mirror/memit-cov-inversion-not-a-hang.md:1-7 | 524 | MISLEADING | `git show fd77f7e:memory_mirror/memit-cov-inversion-not-a-hang.md`: exit 0, 1367 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. :3 says do not act, yet :7 gives still-applicable CPU-time triage. Engine CPU solve remains at memit_dry_run/memit/memit/memit_main.py:200-203; full live-note CPU-time/progress phrase scan found no live home (P3 below). | merge-into REPRODUCIBILITY.md | A quiet CPU solve can still be computing. Check CPU-time deltas with an allowed read-only observer before calling it hung; unavailable observation means UNVERIFIED. |
| memory_mirror/molab-migration-assessment.md:1-7 | 552 | KEEP | `git show fd77f7e:memory_mirror/molab-migration-assessment.md`: exit 0, 2221 bytes; :7 replacement(s) resolve to live notes: local-only-no-rented-compute.md. | keep |  |
| memory_mirror/neuraldb-scr-keep-side-store-pressure-live.md:1-7 | 499 | KEEP | `git show fd77f7e:memory_mirror/neuraldb-scr-keep-side-store-pressure-live.md`: exit 0, 471 bytes; :7 replacement(s) resolve to live notes: in-weight-necessity-is-scope-keyed-hybrid.md. | keep |  |
| memory_mirror/notebooklm-install-and-notebook-ids.md:1-7 | 471 | KEEP | `git show fd77f7e:memory_mirror/notebooklm-install-and-notebook-ids.md`: exit 0, 4942 bytes; :7 replacement(s) resolve to live notes: notebooklm-via-browser-harness.md. | keep |  |
| memory_mirror/operator-profile-llm-as-database.md:1-7 | 563 | KEEP | `git show fd77f7e:memory_mirror/operator-profile-llm-as-database.md`: exit 0, 1687 bytes; :7 replacement(s) resolve to live notes: operator-profile-and-standing-directive.md, local-only-no-rented-compute.md. | keep |  |
| memory_mirror/operator-scaffolding-phase-tooling.md:1-7 | 599 | KEEP | `git show fd77f7e:memory_mirror/operator-scaffolding-phase-tooling.md`: exit 0, 1545 bytes; :7 replacement(s) resolve to live notes: operator-overnight-autonomy-2026-10-06.md, evidence-over-scaffolding.md. | keep |  |
| memory_mirror/perplexity-mcp-restore-from-pod-restore.md:1-7 | 743 | KEEP | `git show fd77f7e:memory_mirror/perplexity-mcp-restore-from-pod-restore.md`: exit 0, 1060 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. | keep |  |
| memory_mirror/pod-restart-wipes-system-python-ml-stack.md:1-7 | 476 | KEEP | `git show fd77f7e:memory_mirror/pod-restart-wipes-system-python-ml-stack.md`: exit 0, 1876 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. | keep |  |
| memory_mirror/repo-reorganized-llmdb-root.md:1-7 | 554 | KEEP | `git show fd77f7e:memory_mirror/repo-reorganized-llmdb-root.md`: exit 0, 2402 bytes; :7 replacement(s) resolve to live notes: llmdb-root-env-points-at-main-checkout.md. | keep |  |
| memory_mirror/research-pass-2026-10-06-sequence.md:1-7 | 618 | KEEP | `git show fd77f7e:memory_mirror/research-pass-2026-10-06-sequence.md`: exit 0, 2166 bytes; :7 named repo homes checked by pathlib.Path.is_file(); see pointer notes below. Both HANDOFF.md and council_critique.md exist in results/research_pass_2026-10-06/. | keep |  |
| memory_mirror/runpod-dashboard-vs-pod-metrics.md:1-7 | 451 | KEEP | `git show fd77f7e:memory_mirror/runpod-dashboard-vs-pod-metrics.md`: exit 0, 2803 bytes; :7 replacement(s) resolve to live notes: disk-budget-before-dispatch.md. | keep |  |
| memory_mirror/runpod-durable-experiment-launch.md:1-7 | 494 | KEEP | `git show fd77f7e:memory_mirror/runpod-durable-experiment-launch.md`: exit 0, 1412 bytes; :7 replacement(s) resolve to live notes: tmux-server-hang-dashboard.md. /Users/robertrhu/.claude/CLAUDE.md:120-124 and AGENTS.md:76 preserve background/nohup launch guidance. | keep |  |
| memory_mirror/runpod-session-disconnect-cause.md:1-7 | 484 | KEEP | `git show fd77f7e:memory_mirror/runpod-session-disconnect-cause.md`: exit 0, 1701 bytes; :7 replacement(s) resolve to live notes: tmux-server-hang-dashboard.md, tmux-kill-session-exact-name.md. | keep |  |
| memory_mirror/MEMORY.md:1-154 | 22597 | KEEP | P1: 22,597 bytes, 154 lines, 142 unique links, zero missing/retired targets; hard cap /Users/robertrhu/.codex/AGENTS.md:131-133 and /Users/robertrhu/.claude/CLAUDE.md:136-138. Remaining headroom 1,803 bytes (7.39%). | keep |  |
| memory_mirror/MEMORY.md:1 | 291 | STALE, BLOAT | 280 characters / 290 bytes; prior APPLIED.md:222 recorded maximum 178 chars. Hook omits proactive 45% stop documented in context-management-every-session.md:22 and shared CAD brief; repeats detailed Memento history already at note :13,20. | fix-text: shorten hook, retain 60/45/40 thresholds and 300,000 ceiling | - [Context](context-management-every-session.md) — Codex: new work ≥60%, stop at 45%, successor ≤40% or compaction. Claude: measure usage; Memento ceiling 300,000. |
| memory_mirror/MEMORY.md:38 | 158 | MISLEADING | Hook says "perplexity_reason if Codex is down"; codex-runs-inline-from-claude-bash.md:16 explicitly says advisory only and promotion remains blocked. Prior astra_review.md:11-13 required that boundary. Body fix is present; index shorthand leaves it unclear. | fix-text: carry binding-versus-advisory boundary into hook | - [Cross-family review](codex-runs-inline-from-claude-bash.md) — Astra high binds promotion; Perplexity is advisory during auth failure. |
| memory_mirror/MEMORY.md:125 | 236 | BLOAT, DUPLICATE | 233 characters / 235 bytes; APPLIED.md:222 recorded zero lines >200. Hook repeats server/launchd detail at background-shell-niceness-10.md:9,13; preserve the pinned-launch requirement in short hook and full note. | fix-text: shorten hook without changing pinned launch or operator control | - [Background niceness](background-shell-niceness-10.md) — nice -n adds to inherited niceness; use the authorized NEW-1 server for its pinned launch. |
| memory_mirror/MEMORY.md:125-154 | 5214 | MISLEADING | Under "Results history" (:119), these 30 links include current launch, sandbox, queue, handoff and Intel operating rules. Active examples: work-queue-tab-keep-current.md and context-watcher survivor (:134). Workflow & tools (:33-52) and Traps (:53-70) are their existing homes. | fix-text: move operational hooks into Workflow & tools / Traps; retain all rules |  |
| CLAUDE.md:30 (inbound retired-memory reference) | 1150 | DUPLICATE, MISLEADING | Lists gpu-gate-refuses-any-venv-python.md and retired gpu-gate-blocks-any-python.md; tombstone :7 merged scope and -B trap into survivor, where :10-14 retains complete rule. Prior APPLIED.md:198 explains retirement because CLAUDE also cited survivor. | fix-text: remove retired note name, keep survivor and every admission requirement | Admission guidance: memory_mirror/gpu-gate-refuses-any-venv-python.md (scope, exemptions, watcher and dashboard-poll traps). |

## Cross-source findings

1. **Current watcher has a superseded sibling.** `codex-watch-anchor-tokens-read-context-from-rollout.md:10,16` recommends pane regex matching; indexed `codex-watch-anchor-replies-read-context-from-rollout.md:17` records a counterexample even for that anchored regex and scopes replies to assistant rollout messages. Retire the unindexed sibling; do not re-index it. The indexed survivor itself still contains its earlier pane instruction at :10 and a generic closing instruction at :22: keep its failed recipes explicitly historical, with :17 as the current procedure. This is a new post-October-10 collision.

2. **Historical checkpoint can impersonate the canonical one.** `memory_mirror/SESSION_CHECKPOINT.md:4-24` presents June generated state and a "start here" handoff; `CLAUDE.md:66` and `AGENTS.md:48` point to the root checkpoint and runbook. `EXPERIMENT_RUNBOOK.md:41-47` is the current generated block, while the copy still prescribes `/workspace`, gpt-5.5 and the old engine hash (:105,115,305-342,516-517). It was last changed by git commit `0b7a783c`, 2026-06-24; 421 of its 432 nonempty lines are also present in the root checkpoint. Move its 132,381 bytes out of the memory namespace into dated session history, preserving all record bytes. Its missing frontmatter is an existing checkpoint exemption, **not** a FORMAT defect (prior APPLIED.md:216).

3. **Archive labels are working; next-step verbs inside archives remain historical.** The 15 already-HISTORICAL notes stay de-indexed, as previously approved; do not re-report that de-indexing as broken. `scope-gate-batch-is-deployment-model.md:8,12` gives June batch-only scope and quantization-next language, whereas `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md:62,123,134` explicitly corrects batch-only to a conditioned compaction-bounded hybrid. `q4km-quantization-survival-pass.md:12-14` has Intel/E1-next wording, superseded by `EXPERIMENT_RUNBOOK.md:87,91` and `AGENTS.md:70`. Retrieve these as dated evidence, never as launch authority. The current Git+Drive adoption separately states nothing is switched on (`results/compute_storage_brainstorm_20261011T054507Z/r2_redesign_operator_adoption.md:5,9-11`); retirement of the science Intel target is compatible with an Intel support host.

4. **A preserved lesson is still trapped in a tombstone.** `memit-cov-inversion-not-a-hang.md:3` says do not act, while :7 tells agents to inspect CPU time before declaring a silent CPU solve hung. Current engine :200-203 still performs a CPU solve with no progress statement inside that span. P3 found this specific triage rule in no live memory note; the old text exists at `fd77f7e:memory_mirror/memit-cov-inversion-not-a-hang.md:14-18`. Move only the platform-neutral observation rule into current reproducibility guidance; keep the retired GPT-J, `/proc` and pod commands historical. This is a coverage gap, not evidence of a current hung process.

5. **Prior reviewer-output-race loss is repaired.** `results/memory_audit_20261010/astra_review.md:19-21` identified the missing lesson; current `codex-runs-inline-from-claude-bash.md:19` now requires unique reviewer output paths, including simultaneous reviews of one packet. No regression. Likewise, Astra auth-failure waiver is absent from that note :16, and the M3 deployment correction is present at `AGENTS.md:70`. The remaining review problem is the index shorthand (:38), not a renewed body waiver.

6. **Live and durable index loading are different.** `memory-paths-and-mirror-discipline.md:9-11,16` describes separate harness and mirror locations, but `tools/closeout_check.py:249-265` explicitly permits different MEMORY.md indexes and checks live-to-mirror notes only. Current default LIVE index is 17,851 bytes / 128 lines; mirror index is 22,597 bytes / 154 lines. None of these 18 entries is linked in the LIVE index either. Only c10w, c10x and the CLT note from this list physically exist in default LIVE, byte-identical. The checkpoint is not in default LIVE. Do not claim a mirror-only unindexed file is automatically loaded or that closeout GREEN proves two-way index equality.

7. **Threshold shorthand lags the early stop rule.** Index :1 and `CLAUDE.md:18` / `AGENTS.md:7` emphasize the 40% boundary, whereas `context-management-every-session.md:22` adds a 45% stop message ahead of a long pending step. The shared CAD brief sets 45% stop / 40% successor. Preserve that newer protection in the compact hook, and reconcile the other lanes' copies; do not raise thresholds to buy space. The 300,000 Memento ceiling is retained.

8. **Index structure has grown without broken links.** Prior APPLIED.md:222 reported 17,181 bytes, 112 links and max line length 178. Now: 22,597 bytes (+5,416; +31.52%), 142 unique links, zero broken/retired links, 154 lines and two lines >200 characters (280 and 233). Cap use is 92.61%, with 1,803 bytes left. Sections are Operating rules 4,282 bytes, Workflow & tools 2,749, Traps 2,433, Science lessons 5,380, Prior art 1,434 and Results history 6,027; the first context hook plus blank line accounts for the remaining 292. Many new active operational hooks (:125-154) landed under Results history. Re-home those hooks before deciding on byte cuts; retain distinct safety/science interpretation lessons.

### Exhaustive inbound references to the 41 retired filenames

P2 searched the literal slug of every listed tombstone in all four named guidance files. Hits:

- `CLAUDE.md:30`: `gpu-gate-blocks-any-python`, alongside its live survivor. This is the one active, unqualified retired-note citation; replace the redundant retired name.
- `AGENTS.md`: no listed tombstone slug found. `DISCIPLINE.md`: no listed tombstone slug found. This result is limited to the 41 supplied names.
- `EXPERIMENT_RUNBOOK.md:156,697`: `deployment-target-intel-cpu`; :135,910 `larql-the-mechanism-prior-art`; :909 `operator-scaffolding-phase-tooling`; :142,893 `pod-restart-wipes-system-python-ml-stack`; :236,248 `runpod-dashboard-vs-pod-metrics`. All nine occurrences explicitly mark the note retired/pod-era. Keep those historical labels; the E1 row :697 still has older Intel wording, consistent with the cross-source hazard above. No regression to a bare retired wikilink was found.

### Probe receipts and pointer qualification

- **P1 — structural/pointer probe:** `/usr/bin/python3 -B -` read the two supplied lists and all note/index bytes with pathlib; `re.findall(r"\]\(([^)]+)\)", index)` produced 142 unique resolving links, zero duplicate links and zero retired targets. All 58 ordinary notes/tombstones have opening/closing frontmatter with matching name, nonempty description and metadata.type. MEMORY.md and the checkpoint are excluded document types. No FORMAT defect found.
- **P2 — per-tombstone archive and inbound probes:** Python invoked `/usr/bin/git show fd77f7e:memory_mirror/<each listed tombstone>` with subprocess.run(capture_output=True); all 41 returned exit 0 and nonempty bytes. The primary table lists each exact command and byte result. For every `[[replacement]]`, pathlib verified an existing non-retired .md. Each literal slug was searched line by line in CLAUDE.md, AGENTS.md, DISCIPLINE.md and EXPERIMENT_RUNBOOK.md; the full hit inventory is above (equivalent to per-slug `grep -n`).
- **P3 — live lesson/copy probe:** pathlib fully read every non-retired memory_mirror/*.md excluding the index/checkpoint and matched `CPU time|cpu time|utime|stime|jiffies|deadlock|no progress bar|compute.*(?:hang|hung)|(?:hang|hung).*compute`. No live hit preserved CPU-time-delta triage. This scoped negative search is corroborated by the tombstone's own :7 retained advice and current CPU solve source; it is not an exhaustive absence claim across the whole repo. Default LIVE/main copies were tested with Path.exists and exact read_bytes equality, without copying.
- **Non-wikilink tombstone homes:** CORPUS number references were resolved to actual `CORPUS/NN_*.md` writeups; `docs/SPEC_EXPERIMENT_OVERLAY.md`, `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md`, `docs/EXPERIMENT_REGISTRY.md`, `docs/write_engine_viability_determination_report.md`, `research_and_specs/molab_feasibility_report.md`, `tools/experiment_gate.py`, `pyproject.toml`, `uv.lock` and both research-pass HANDOFF/council files all exist. `gemma4-rung4-candidate.md:7` explicitly describes the old `/workspace` source as gone; that intentional historical missing path is not a broken replacement. `perplexity-mcp-restore-from-pod-restore.md:7` names the retired pod path and configuration keys; no credential value was read into or copied to this report, and current external service connectivity was not tested.

## Load cost

Approximate tokens = ceil(UTF-8 bytes / 4), an accounting heuristic rather than model tokenization. Note bodies are **on-demand costs**, not automatic additions for every indexed link. No live harness transcript proving a particular Astra packet's reads was audited.

- **I (index):** Claude auto-memory loading is documented by SESSION_BOOTSTRAP.md:108; actual file location is memory-paths-and-mirror-discipline.md:9. The current default LIVE index costs 17,851 bytes (~4,463 tokens), not the mirror's 22,597. Codex builder and Astra read the durable index when following AGENTS.md:45-53 / CLAUDE.md:66; those are reading policies, not proof of automatic harness injection.
- **U (unindexed live note):** Claude, Codex builder or Astra can load it through a direct brief, surviving wikilink or targeted retrieval under DISCIPLINE.md:38. No automatic per-session body load established. HISTORICAL does not mean unreachable; e.g. local-only-no-rented-compute.md:12 links the CLT note, and codex-runs-inline-from-claude-bash.md:10 links exhaust-options.
- **T (retired redirect):** Claude, builder or Astra loads it only through an explicit/direct or surviving retired citation; the active CLAUDE.md:30 case is listed above. Never re-index tombstones.
- **S (checkpoint snapshot):** no current loader points to this mirror copy: the root path is named by AGENTS.md:48 and CLAUDE.md:66, and it is absent from default LIVE. Its entire cost applies only to an explicit read or mistaken directory-wide load.

| audited file in memory_mirror/ | bytes | approximate tokens | sessions / load route |
|---|---:|---:|---|
| SESSION_CHECKPOINT.md | 132,381 | 33,096 | S: Claude / Codex builder / Astra, conditional as above |
| autonomy-drifts-from-kickoff-scope.md | 1,646 | 412 | U: Claude / Codex builder / Astra, conditional as above |
| c10-edit-collateral-breaks-injected-target.md | 1,510 | 378 | U: Claude / Codex builder / Astra, conditional as above |
| c10-edit-rotates-required-target-direction.md | 1,389 | 348 | U: Claude / Codex builder / Astra, conditional as above |
| c10-layerpick-null.md | 1,360 | 340 | U: Claude / Codex builder / Astra, conditional as above |
| c10-secondkey-null-large-write.md | 1,598 | 400 | U: Claude / Codex builder / Astra, conditional as above |
| c10-sharedz-underfit.md | 2,621 | 656 | U: Claude / Codex builder / Astra, conditional as above |
| c10-stacked-solve-tradeoff.md | 1,719 | 430 | U: Claude / Codex builder / Astra, conditional as above |
| c10-twopass-solve-null-at-margin.md | 1,476 | 369 | U: Claude / Codex builder / Astra, conditional as above |
| c10w-ceiling-oracle-result.md | 1,341 | 336 | U: Claude / Codex builder / Astra, conditional as above |
| c10x-enginepath-result.md | 1,933 | 484 | U: Claude / Codex builder / Astra, conditional as above |
| codex-watch-anchor-tokens-read-context-from-rollout.md | 1,845 | 462 | U: Claude / Codex builder / Astra, conditional as above |
| exhaust-options-before-blocked.md | 1,550 | 388 | U: Claude / Codex builder / Astra, conditional as above |
| mbp-command-line-tools-broken.md | 1,381 | 346 | U: Claude / Codex builder / Astra, conditional as above |
| perplexity-c10h-reranks-anyedit-failure-geometry-first.md | 1,551 | 388 | U: Claude / Codex builder / Astra, conditional as above |
| q4km-quantization-survival-pass.md | 3,220 | 805 | U: Claude / Codex builder / Astra, conditional as above |
| scope-gate-batch-is-deployment-model.md | 1,933 | 484 | U: Claude / Codex builder / Astra, conditional as above |
| wide-intermediate-7b-editing-vram.md | 3,024 | 756 | U: Claude / Codex builder / Astra, conditional as above |
| anyedit-clearing-c10-would-close-tested-write-serve-scope.md | 685 | 172 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-connectedpapers-adds-diagnostics-not-plan-change.md | 643 | 161 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-default-window-collapses-c10-a7.md | 625 | 157 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-gate-upgraded-by-muke-coin-suit.md | 619 | 155 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md | 620 | 155 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-local-transplant-controls-fail-before-a7.md | 613 | 154 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-precommit-triage-proceed-but-viability-gated.md | 560 | 140 | T: Claude / Codex builder / Astra, conditional as above |
| anyedit-token-alignment-gate-prevents-false-rescue.md | 484 | 121 | T: Claude / Codex builder / Astra, conditional as above |
| autoresearch-is-not-a-faithfulness-gate.md | 496 | 124 | T: Claude / Codex builder / Astra, conditional as above |
| background-monitor-no-premature-read.md | 530 | 133 | T: Claude / Codex builder / Astra, conditional as above |
| c10-band-knobs-failed-for-hard-coined-values.md | 469 | 118 | T: Claude / Codex builder / Astra, conditional as above |
| c10-solvefeas-underfit-at-50.md | 402 | 101 | T: Claude / Codex builder / Astra, conditional as above |
| c10-status-and-session-b-residual-test.md | 605 | 152 | T: Claude / Codex builder / Astra, conditional as above |
| c10k-route-a-resume.md | 611 | 153 | T: Claude / Codex builder / Astra, conditional as above |
| c10z-stage1-underfit-terminal.md | 552 | 138 | T: Claude / Codex builder / Astra, conditional as above |
| canonical-fit-is-not-c10-rescue.md | 468 | 117 | T: Claude / Codex builder / Astra, conditional as above |
| codex-chatgpt-oauth-model-slug.md | 558 | 140 | T: Claude / Codex builder / Astra, conditional as above |
| codex-review-embed-evidence-and-effort.md | 597 | 150 | T: Claude / Codex builder / Astra, conditional as above |
| deployment-target-intel-cpu.md | 599 | 150 | T: Claude / Codex builder / Astra, conditional as above |
| e2e-ground-truth-situate-on-the-map.md | 465 | 117 | T: Claude / Codex builder / Astra, conditional as above |
| experiment-gate-before-next-science-arc.md | 541 | 136 | T: Claude / Codex builder / Astra, conditional as above |
| gemma4-rung4-candidate.md | 573 | 144 | T: Claude / Codex builder / Astra, conditional as above |
| gpu-gate-blocks-any-python.md | 471 | 118 | T: Claude / Codex builder / Astra, conditional as above |
| in-weight-vs-sidestore-f1-question.md | 534 | 134 | T: Claude / Codex builder / Astra, conditional as above |
| larql-the-mechanism-prior-art.md | 529 | 133 | T: Claude / Codex builder / Astra, conditional as above |
| llm-db-local-migration-gaps.md | 613 | 154 | T: Claude / Codex builder / Astra, conditional as above |
| llmdb-root-points-at-main-checkout.md | 499 | 125 | T: Claude / Codex builder / Astra, conditional as above |
| local-only-hardware-rule.md | 478 | 120 | T: Claude / Codex builder / Astra, conditional as above |
| memit-cov-inversion-not-a-hang.md | 524 | 131 | T: Claude / Codex builder / Astra, conditional as above |
| molab-migration-assessment.md | 552 | 138 | T: Claude / Codex builder / Astra, conditional as above |
| neuraldb-scr-keep-side-store-pressure-live.md | 499 | 125 | T: Claude / Codex builder / Astra, conditional as above |
| notebooklm-install-and-notebook-ids.md | 471 | 118 | T: Claude / Codex builder / Astra, conditional as above |
| operator-profile-llm-as-database.md | 563 | 141 | T: Claude / Codex builder / Astra, conditional as above |
| operator-scaffolding-phase-tooling.md | 599 | 150 | T: Claude / Codex builder / Astra, conditional as above |
| perplexity-mcp-restore-from-pod-restore.md | 743 | 186 | T: Claude / Codex builder / Astra, conditional as above |
| pod-restart-wipes-system-python-ml-stack.md | 476 | 119 | T: Claude / Codex builder / Astra, conditional as above |
| repo-reorganized-llmdb-root.md | 554 | 139 | T: Claude / Codex builder / Astra, conditional as above |
| research-pass-2026-10-06-sequence.md | 618 | 155 | T: Claude / Codex builder / Astra, conditional as above |
| runpod-dashboard-vs-pod-metrics.md | 451 | 113 | T: Claude / Codex builder / Astra, conditional as above |
| runpod-durable-experiment-launch.md | 494 | 124 | T: Claude / Codex builder / Astra, conditional as above |
| runpod-session-disconnect-cause.md | 484 | 121 | T: Claude / Codex builder / Astra, conditional as above |
| MEMORY.md | 22,597 | 5,650 | I: Claude / Codex builder / Astra, conditional as above |

All 60 audited files total 208,542 bytes (~52,136 tokens) if explicitly read in full; that total is not a measured normal-session load.

## Verdict counts

65 finding rows across 60 primary audited files plus one inbound guidance span. Counts include every tag on a two-verdict row; overlapping index spans are intentional.

 | verdict | rows |
|---|---:|
| KEEP | 42 |
| BLOAT | 3 |
| CONFLICT | 0 |
| DUPLICATE | 3 |
| NONFACTUAL | 0 |
| STALE | 1 |
| AMBIGUOUS | 1 |
| MISLEADING | 5 |
| HISTORICAL | 16 |
| UNREACHABLE | 0 |
| FORMAT | 0 |

No guidance was edited, copied, moved or deleted. Main-checkout differences were observed read-only and were not reconciled. Proposed corrections preserve admission, review, halt, storage and operator-approval requirements.

Lines: 204
