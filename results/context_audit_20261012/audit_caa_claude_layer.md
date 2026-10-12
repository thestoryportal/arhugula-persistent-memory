# CAA — Claude always-loaded layer audit (2026-10-12 UTC)

Read-only snapshot; only this report was written. Repo tools, hooks, science, network, backup, cleanup and Git mutation were not run. No credential values are reproduced. Bytes are UTF-8 source-span bytes including line terminators unless marked as injected payload; approximate tokens = bytes / 4, not tokenizer measurements. Rows may overlap; do not sum row bytes as a total load.

Paths: `G` = `/Users/robertrhu/.claude/CLAUDE.md`; `T` = `/Users/robertrhu/.claude/RTK.md`; `R` = worktree `CLAUDE.md`; `M` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/CLAUDE.md`; `AM` = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory`; `HC` = `/Users/robertrhu/.local/share/mise/installs/node/24.21.0/lib/node_modules/@nanonets/graft/dist/claude`; `LR` = `/Users/robertrhu/.claude/plugins/cache/promptctl/laws/0.24.1/hooks/scripts/skill-router.sh`.

Loader evidence: `TR` = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-c10k-route-a/99001b45-b0df-4ee3-bf2a-023a834c6bf3.jsonl`, line 27 (instructions attachment: G/User, T/User, R/Project, AM/MEMORY.md/AutoMem), line 4 (requested worktree cwd), lines 6/21/22 (hook injections). `SA` = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-c10k-route-a/fd1c485f-c55e-4158-9e81-7b6f7fae3e5d/subagents/agent-a64a54196ace8fc29.jsonl`, line 7 (subagent also loads G/T/R/AM). These are transcript records, not inferred loader behavior. `PJ` = the parent directory of TR.

Evidence aliases: `runbook` = `EXPERIMENT_RUNBOOK.md`; `brief.md` = `results/context_audit_20261012/brief.md`; `APPLIED.md` = `results/memory_audit_20261010/APPLIED.md`; `adoption receipt` = `results/compute_storage_brainstorm_20261011T054507Z/r2_redesign_operator_adoption.md`; `v4` / `adopted v4` = the sibling `r2_git_drive_redesign_v4.md`; `r2q_maestro_acceptance.md` and `r2t_maestro_acceptance.md` are also siblings there; `figma_mcp_setup_report.md` = `results/dashboard_integration_review_20261011/figma_mcp_setup_report.md`; `SK1 report` = `results/skills_pipeline_survey_20261012/skills_pipeline_survey.md`; `plugin hooks.json` = `/Users/robertrhu/.claude/plugins/cache/promptctl/laws/0.24.1/hooks/hooks.json`; unqualified `settings.json` in hook evidence means `/Users/robertrhu/.claude/settings.json`. Source-spans are complete policy paragraphs; proposed replacement snippets apply only to the cited defective text, retaining uncited surrounding rules.

The requested worktree-hash memory directory does not exist. AM is the fallback selected by the brief and the actual latest sampled AutoMem attachment. The older bank `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/` also exists and is loaded by an older sampled subagent (`PJ/ef74c20d-d259-4cb7-9e93-31d8d916f184/subagents/agent-aef8fd93066c07495.jsonl:7`). Directory names alone therefore do not establish current loading. Initial census was MEMORY.md + 21 notes; MAESTRO added atomic-units-parallel-worktree-lanes.md and index line 20 during this audit; the final snapshot audits all 22 notes.

| item (file:line-range or note filename) | bytes | verdict(s) | evidence (file:line or command) | proposed action | replacement text (only when item stays; <=200 characters) |
|---|---:|---|---|---|---|
| G:1-7 | 231 | KEEP | T:1-29; TR:27 records both imported files. | keep |  |
| G:9-24 | 1681 | KEEP | R:15 assigns personal decisions to operator; evidence-first advice is compatible. | keep |  |
| G:26-36 | 418 | KEEP | R:26 preserves correctness gates; no added implementation scope. | keep |  |
| G:38-54 | 724 | KEEP | R:17 builder allowlists and verification; no adjacent cleanup authorization. | keep |  |
| G:56-66 | 1637 | AMBIGUOUS | G:64 says "If describing the mechanics needs if / when / skip / only"; R:31-32,40,61 require conditional safety gates. Reading A: pure data modelling advice; B: remove boundary guards. | fix-text (limit variability advice to pure domain modelling) | Prefer data modelling over incidental branches in pure logic; preserve explicit admission, authorization and correctness guards at effect boundaries. |
| G:68-85 | 1266 | KEEP | R:16,26,44 require preregistration, independent review and empirical close-out. | keep |  |
| G:87-96 | 2492 | KEEP | R:33 requires source reads; R:26 refuses inference past unmet gates. Cache removal remains subject to deletion scope. | keep |  |
| G:98-100 | 430 | KEEP | AM/maestro-hash-pin-edits-go-to-builders.md:11-15 records refusal and explicit operator authorization before delegation. | keep |  |
| G:102-110 | 783 | NONFACTUAL | G:104 says "no CLAUDE.md" carries over; SA:7 explicitly loads G, T and R into a Claude subagent. Requirements still need explicit prompts. | fix-text (distinguish conversation inheritance from loaded guidance) | Subagents may receive global and project instructions. Put task scope, user requirements and acceptance criteria explicitly in each delegation prompt. |
| G:112-114 | 321 | KEEP | Session-start commands: git rev-parse --show-toplevel; git branch --show-current => requested worktree, worktree-c10k-route-a. | keep |  |
| G:116-118 | 843 | CONFLICT | G:118 permits no branches beyond the CI branch; tools/git_merge_gate.py:188-195 allows master, live worktree branches and PR head. The repo gate is current. | fix-text (defer branch hygiene to the project merge gate) | Require successful CI on the exact candidate head and post-merge SHA. Follow the project merge gate and its allowed-branch inventory. |
| G:120-124 | 712 | KEEP | R:17 delegates authorized runs; .venv interpreter rule matches AGENTS.md Environment. Audit-specific prohibitions override examples. | keep |  |
| G:126-130 | 597 | KEEP | R:62 requires deterministic canonical edits and persistence checks; YAML parse checks are conditional on editing YAML. | keep |  |
| G:132-134 | 503 | KEEP | Deliverable-length exception matches brief.md:33-37; running commentary stays compact. | keep |  |
| G:136-138 | 353 | AMBIGUOUS, STALE | "MEMORY.md" has no path; AM/MEMORY.md is now 3277 B, with 21123 B below the stated cap. "headroom is nearly exhausted" is false for this loaded index. | fix-text (name capped file and measure instead of asserting headroom) | Before editing the governed MEMORY.md index, identify its absolute path and measure bytes; respect its applicable cap without overwriting a fuller memory index. |
| G:140-142 | 317 | CONFLICT | Unconditional "save any learnings" and /context-save writes conflict with results/context_audit_20261012/brief.md:12,43 (only report may change). | fix-text (scope session saves to authorized destinations) | At gates, preserve context in the authorized report or handoff. Run /context-save only when its writes are within the session allowlist. |
| G:144-146 | 267 | KEEP | Closing explanation of principles; no additional authority or mutable state. | keep |  |
| G:147-149 | 226 | KEEP | Read-only Path.exists probe: ~/.claude/skills/graphify/SKILL.md exists. Explicit /graphify trigger only; not invoked here. | keep |  |
| T:1-22 | 746 | KEEP | ~/.claude/settings.json:23-27 configures rtk hook claude. Savings percentage is a product estimate, not verified savings in this audit. | keep |  |
| T:24-29 | 217 | AMBIGUOUS | T:26 "All other commands" and :29 "full command reference"; settings.json:23-27 matches Bash only, while G:1 imports T and G has no command reference. | fix-text (describe supported Bash rewriting and correct reference) | The Bash hook rewrites supported shell commands. Use rtk proxy for unfiltered evidence; verify unsupported commands rather than assuming every command is rewritten. |
| R:1-7 | 886 | KEEP | EXPERIMENT_RUNBOOK.md:89,91 names M3 science/deployment; current worktree lead/team role matches the dispatched brief. | keep |  |
| R:9-14 | 1478 | KEEP | DISCIPLINE.md:29-34 defines context triggers; runbook:45 and adoption receipt:11 preserve design-only status. | keep |  |
| R:15-15 | 654 | AMBIGUOUS | "Infra ... is pre-approved when needed" vs R:61 exact deletion approval and adoption receipt:11 separate activation GO. Reading A: scoped routine prep; B: any download/activation. | fix-text (bound infra pre-approval to existing scope) | Routine infrastructure work is pre-approved only within the active brief; frozen amendments, activation, storage/spend forks, deletions and credentials remain operator-gated. |
| R:16-16 | 868 | KEEP | git log -- CLAUDE.md:145bd3ff and results/memory_audit_20261010/astra_review.md:11-13 require binding Astra-high review; command explicitly disables graft. | keep |  |
| R:17-17 | 996 | KEEP, BLOAT | Keep team/no-commit/merge/watch rules. Narrative beginning "When you catch yourself" repeats memory_mirror/never-idle-arm-completion-watch.md; its exact substring is quantified below. | fix-text (replace idle-incident story with its existing pointer) | See memory_mirror/never-idle-arm-completion-watch.md for the idle incident; retain surrounding dispatch, verification, commit/push, merge, watcher and milestone-push rules. |
| R:18-18 | 642 | CONFLICT, STALE | R says stop only at <=40%; brief.md:30 says stop at 45%, successor <=40%; AM/sol-builders-blind-to-context.md:7-11 requires watcher-delivered stop. Memento absent in settings.json:110-115. | fix-text (state watcher and disabled-hook fallback) | New Codex work requires >=60% left; MAESTRO sends stop at 45%, successor by <=40% or compaction. Claude measures transcript usage and resets by 300k; Memento hook is disabled. |
| R:19-26 | 1081 | KEEP | Prime directive and authorized delegation are consistent; adoption receipt:11 does not authorize implementation or activation. | keep |  |
| R:28-30 | 1227 | KEEP | tools/engine_fingerprint.py:31-47 pins d941a9fb; SHA-256 of current memit_main.py = d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; .claude/settings.json:85 exports main root. | keep |  |
| R:31-33 | 1017 | KEEP | Determinism, baseline and source-read gates retained. Their empirical checks are prereg-dependent; no science was run for this document audit. | keep |  |
| R:34-34 | 375 | AMBIGUOUS | "MEMIT engine, LARQL, and git stay UNMODIFIED" vs R:17 explicitly requires commits. Reading A: vendored implementation sources; B: the Git checkout must never change. | fix-text (identify protected implementations) | Keep the pinned science-path MEMIT/LARQL implementations and Git tool implementation unchanged; authorized repository commits follow MAESTRO verification and the merge gate. |
| R:36-40 | 1222 | KEEP | Rerun scope and single-attempt approval preserved; AM/one-shot-run-needs-real-scale-dry-run.md:8 records a spent attempt. No historical result reopened. | keep |  |
| R:42-44 | 830 | DUPLICATE, MISLEADING | Full tracker list duplicates DISCIPLINE.md:49; tools/closeout_check.py:249-265 checks another memory dir and treats mirror drift as advisory. ALL GREEN does not prove current AutoMem is mirrored. | merge-into DISCIPLINE.md §1.1 (keep short binding gate here) | Run LLMDB_ROOT=$PWD python3 tools/closeout_check.py <D-ID>; require ALL GREEN and verify the actual loaded memory directory separately. Tracker protocol: DISCIPLINE.md §1.1. |
| R:46-48 | 281 | KEEP | Decision-ID + reasoning remains distinct from experiment detail and operator permission. | keep |  |
| R:50-54 | 3125 | KEEP | R:54 matches results/git_automation_fix3_mb13_20261010T092614.133488Z/build_report.md:23. Preserve full cooperative rule, including external-writer suspension and post-merge failure semantics. | keep |  |
| R:56-58 | 725 | KEEP | EXPERIMENT_RUNBOOK.md:274-278 establishes Git/hot memit/Drive tiers; adoption receipt:5,11 assigns Intel upload but no activation. | keep |  |
| R:59-59 | 752 | KEEP, BLOAT | Safety tail beginning "Instead:" matches runbook:275-277. Incident/temptation preamble duplicates runbook:273; bytes quantified below. | fix-text (cut incident preamble; retain every budget/approval requirement) | State disk budgets; require free >= projected writes + 20 GiB; archive irreplaceable bulk to Drive with committed hashes; delete regenerable bulk only after exact operator approval. |
| R:60-62 | 1191 | KEEP | Protected paths, exact deletion approval and persistence checks remain; .claude/settings.json:15-71 enforces path protections; local-FS recurrence is correctly UNVERIFIED. | keep |  |
| R:64-72 | 1541 | KEEP | State pointers avoid restatement; tools/autonomy_mission.json and AUTONOMY.md are present; appendix distinguishes opt-in harness from standing delegation. | keep |  |
| M:1-15 | 2476 | STALE | diff -u <main>/CLAUDE.md CLAUDE.md exit 1: worktree adds orchestrator/remote-operator language, worktree tool prefix and HIL scope. git log gives main 6f2aebf2 (Oct 3), worktree 2b31a5fe (Oct 10). | fix-text (reconcile current worktree authority onto master after review) | Use the current orchestrated operating model and explicit worktree tool root; retain current operator gates. |
| M:16-20 | 723 | CONFLICT, STALE | M:16 says gpt-5.5; R:16 says gpt-6-astra high. M lacks R:17-18 supervision/context requirements and conflates standing delegation with the opt-in harness. | fix-text (reviewer, orchestration and context paragraphs) | Binding promote reviewer: GPT-6-Astra high. Builders: GPT-6.1-Sol. Apply current watcher/context rules and distinguish standing delegation from the opt-in harness. |
| M:22-32 | 2252 | CONFLICT, STALE | M:28 pins e6ac7e18; R:30 and tools/engine_fingerprint.py:19-22,34 supersede it with d941a9fb; other correctness gates remain valid. | fix-text (fingerprint and worktree root) | Use LLMDB_ROOT=$PWD and the current fingerprint in tools/engine_fingerprint.py; retain all baseline, determinism, source-read and inertness gates. |
| M:34-45 | 1760 | STALE | M lacks R:40 rerun-never-read-around rule and R:50-54 merge coordination; closeout command lacks worktree prefix. Keep one-fix/halt and decision rules. | fix-text (restore current rerun, merge and closeout instructions) | Use the current rerun/halt policy, worktree-prefixed closeout and MAESTRO-only cooperative merge gate. |
| M:47-52 | 1369 | CONFLICT, STALE | M:49 calls internal SSD durable archive; runbook:276 forbids it. M:51 suggests standing deletion clearance; R:61 and adopted v4:56 require exact approval. M:52 misattributes pod FUSE history to current FS. | fix-text (three tiers, exact deletion approval, qualify FS history) | Git holds records, memit is hot storage, Drive archives bulk. Exact deletion approval remains required. Edit reversion occurred on pod FUSE; local recurrence is unverified. |
| M:54-62 | 1510 | KEEP | State pointers and opt-in harness semantics remain valid; appendix heading needs the operating-model reconciliation above. | keep |  |
| AM/MEMORY.md:1-12 | 1854 | KEEP | Every Markdown index destination exists in AM; compact behavioral hooks, not pasted result tables. | keep |  |
| AM/MEMORY.md:13-13 | 210 | STALE | Index says "no Figma yet"; AM/labviz-wireframe-before-spec-approval.md:11 and figma_mcp_setup_report.md:3,35 show configured OAuth/tool discovery, disabled pending identity validation. | fix-text (distinguish configured from validated) | Wireframes precede operator build approval; Pencil available, Figma configured but disabled pending validated identity. See the setup receipt. |
| AM/MEMORY.md:14-20 | 1213 | KEEP | 45% watcher rule matches brief.md:30; R2 adoption receipt:5,11 agrees on design-only Git/Drive/M3 push; new atomic-units note appeared during this audit. | keep |  |
| AM/atomic-units-parallel-worktree-lanes.md:1-15 | 1449 | KEEP | TR:686 records this note written by the worktree session; results/skills_pipeline_survey_20261012/skills_pipeline_survey.md:98,104 requires bounded disjoint lanes. Operator correction recorded at note:11. | keep |  |
| AM/codex-session-can-type-into-maestro-pane.md:1-13 | 1251 | KEEP | Note:11-13 distinguishes agent delivery from operator authority; preserves R:15 operator gates. Origin transcript exists under PJ/f50ff08b-a916-4dd1-bbd1-d8ca33d26441.jsonl. | keep |  |
| AM/commit-verified-bytes-before-successor.md:1-15 | 1258 | KEEP | results/compute_storage_brainstorm_20261011T054507Z/r2t_maestro_acceptance.md:5,80 records c4a39020 versus committed 8d6ab32f and rerun addendum. | keep |  |
| AM/dry-admission-probe-before-one-shot.md:1-12 | 1460 | KEEP | tools/mathlab_admit.py:69-73 implements read-only probe separate from emitting CLI path at :122; run-specific authorization still applies. Related notes are in memory_mirror, not AM. | keep |  |
| AM/gdrive-rclone-remote.md:1-21 | 1809 | DUPLICATE, UNREACHABLE | Same topic has different bytes in memory_mirror/gdrive-rclone-remote.md; AM:21 [[storage-archival-policy]] exists in neither AM nor memory_mirror. runbook:272-279 is the actual home. | merge-into memory_mirror/gdrive-rclone-remote.md (reconcile dated OAuth lessons; replace missing link) |  |
| AM/infra-closeout-template-d-hw-2.md:1-11 | 1271 | KEEP | runbook:45 records the same eight R2 IDs and design-only adoption; closeout tool:27-40 defines tracker set. Gate success remains separate from memory-sync coverage. | keep |  |
| AM/intel-exists-to-offload-the-m3.md:1-15 | 1368 | KEEP | Adoption receipt:5,11 assigns M3-initiated push, Intel upload, and no activation; adopted v4:11-15 prohibits Intel access to memit. | keep |  |
| AM/interactive-codex-brainstorm-sessions.md:1-12 | 1341 | KEEP | Named LabViz brief exists; user-present workflow differs from builder mode. Context-related links resolve in memory_mirror; exact launcher is historical example, subject to active session permissions. | keep |  |
| AM/labviz-wireframe-before-spec-approval.md:1-11 | 2040 | KEEP | figma_mcp_setup_report.md:3,35 confirms configured but disabled/identity-unvalidated state; note:11 preserves build hold and tool-status caveats. | keep |  |
| AM/m3-hosts-the-team-no-routine-reboots.md:1-11 | 1513 | KEEP | Adoption receipt:5 and v4:19-24 select observe-and-stop; note:7 labels intermediate activity accounts as superseded history, not current instruction. | keep |  |
| AM/maestro-hash-pin-edits-go-to-builders.md:1-15 | 1236 | KEEP | Note:11-15 explicitly rejects bypass by delegation after denial and requires operator choice; consistent with G:100. Origin transcript PJ/c1346b96-3a9c-4dcf-99dd-264e9c4fad09.jsonl exists. | keep |  |
| AM/merge-gate-first-use-learnings.md:1-14 | 1297 | AMBIGUOUS | Note:8 historical handoff approval was rejected; :14 generalizes to ask before every --apply. R:52 requires operator reservation, not revocation of already-direct approval. Reading A: ensure direct approval; B: repeat approval every time. | fix-text (retain refusal lesson without blanket reapproval) | Before --apply, verify direct operator approval and the cooperative reservation; if approval review rejects the action, stop and obtain the required direct ruling. |
| AM/one-shot-run-needs-real-scale-dry-run.md:1-12 | 1187 | KEEP | Distinct output-budget boundary lesson; note:8 limits evidence to R1J and preserves spent-attempt ruling; related rerun authority is R:40. | keep |  |
| AM/readonly-check-runs-in-maestro-shell.md:1-13 | 1943 | KEEP | r2q_maestro_acceptance.md:3,13 confirms nested-sandbox denial, host proof and write positive control. Broad title should be read with this macOS/Codex observation scope. | keep |  |
| AM/remove-shared-resource-before-policing-it.md:1-11 | 1453 | MISLEADING | Note:7 "only rule left" omits adopted v4:12-17 source pinning/verification/no reverse route and :56-60 deletion/offload protection. It means removal of shared-disk process-list proof, not removal of remaining gates. | fix-text (limit only-rule wording; point at full adopted design) | Removing Intel access to memit eliminates the shared-disk process-enumeration problem. The adopted v4 retains source verification, admission, storage and exact deletion gates. |
| AM/rerun-builder-tests-host-tmpdir.md:1-11 | 1545 | KEEP | Environment-specific rerun lesson survives prior audit APPLIED.md:246. Does not turn local sandbox GREEN into host/Linux acceptance; no suites rerun in audit. | keep |  |
| AM/sealed-allowance-two-drift-windows.md:1-15 | 1323 | HISTORICAL, KEEP | Note:11 identifies R1N v11/r13 historical bounds, not live clearance; R2 adoption receipt:11 grants no host activation. Keep general W1/W2 sizing lesson, never dispatch from these numbers. | keep |  |
| AM/sol-builders-blind-to-context.md:1-11 | 1026 | KEEP | brief.md:30,50 requires 45% MAESTRO stop; note:7 records three builders reporting invisible exact percentage. Matches this lane interface. | keep |  |
| AM/sol-for-sweeps-astra-for-gates.md:1-11 | 1355 | KEEP | R:16 retains binding Astra gate; note:3,11 allocates sweeps to Sol high, and SK1 report:98 uses Sol bounded units with Astra promotion. | keep |  |
| AM/stale-predecessor-watchers-steal-events.md:1-11 | 1103 | AMBIGUOUS | Note:11 says "kill any copy started before"; R:17 requires monitoring every in-flight task. Reading A: duplicate for the transferred task; B: another valid task watcher matching a broad name. Shared .state/session identity is the discriminator. | fix-text (bind cleanup to duplicate task and ownership) | On takeover, identify duplicate watchers for the same task, pane and state file; retire only confirmed predecessor copies while preserving monitors for other in-flight work. |
| AM/stop-open-ended-builder-self-audits.md:1-11 | 1381 | KEEP | Note:7,11 explicitly names incomplete checks as unverified and preserves Astra review; brief.md:46 forbids length-only stale claims. No request to weaken gate. | keep |  |
| AM/timed-chain-prebuild-gate-checker.md:1-14 | 2090 | HISTORICAL, KEEP | Note:11 records DEFECTIVE review after fast run and preserves reservation/full-census/Astra requirements. :7 timings and 870 s are R1-specific history, not commissioning authority. | keep |  |
| ~/.claude/settings.json:73-91; HC/format.js:186-204 | 3143 | CONFLICT | R:16 forbids graft tools/CLI; settings.json:78,89 still invokes them through hooks; TR:6 proves full orientation/upgrade injection. memory_mirror/graft-disabled-audit-2026-10-08.md records earlier disable intent. | operator-decision (disable repo-specific graft hook execution/injection; keep unrelated repositories separate) |  |
| ~/.claude/settings.json:73-80; HC/format.js:139-145 | 165 | CONFLICT | TR:22 injects "Run graft ask ... before grepping" despite R:16 prohibition; HC/hooks.js:473-479 performs hook-side retrieval before returning text. | operator-decision (apply same repo-specific hook suppression) |  |
| LR:47-49; plugin hooks.json:4-19 | 340 | KEEP | settings.json:114 enables laws; TR:6 records medium routing at SessionStart. Does not authorize implementation beyond the brief. | keep |  |
| LR:39-49,166-171; plugin hooks.json:14-21 | 951 | BLOAT, DUPLICATE | TR:21 repeats 340 B routing plus 610 B engagement prose. G:58-64 already states code devices; G:134 asks compact narration; abstract engagement repeats each user message. Preserve medium routing while removing repeated philosophy. | fix-text (retain 340 B routing; replace 610 B engagement with concise instruction) | Apply the relevant craft rules to this request; explain only decisions that affect the outcome. |
| LR:232-235; plugin hooks.json:24-31 | 0 observed; 515 template | CONFLICT | Conditional denial says dispatch a fresh subagent or /clear; R:18 requires durable context handoff and brief.md:50 requires CAA handoff. A craft conflict cannot authorize clearing the audit or widening delegation. | fix-text (preserve compatibility guard and scoped handoff) | If crafts conflict, preserve a handoff and use a separately authorized session; do not clear context or delegate outside the active brief. |
| ~/.claude/settings.json:23-27 (rtk) | 0 | KEEP | Bash rewrite hook, not configured SessionStart/UserPromptSubmit guidance. TR:6,21-22 sampled prompt payloads contain laws/graft only; actual rtk runtime output was not executed. | keep |  |
| ~/.claude/settings.json:34-39; ~/.claude/hooks/voice-stop.sh:1-9 | 0 | KEEP | Stop speech hook emits no additionalContext text; executes speech separately. Zero instruction payload by source inspection; hook not run. | keep |  |
| ~/.claude/settings.json:94-101; ~/.claude/hooks/herdr-agent-state.sh:20-100 | 0 | KEEP | Session-registration hook sends pane/session state over socket and emits no prompt text; source inspected, never executed. | keep |  |
| AM notes absent/different in mirror (overlaps note rows) | 16281 | MISLEADING | tools/closeout_check.py:252-261 defaults to the older mirror-root bank; current AutoMem is AM (TR:27). 11 notes absent, 1 different; prior APPLIED.md:244 asserted only the older bank mirrored. | fix-text (document/load current bank and check it explicitly; reconcile mirrors only after approval) | Determine the AutoMem directory from the live instructions attachment; compare that bank with memory_mirror using explicit LLMDB_LIVE_MEMORY. |

## Cross-source findings

1. **Master/worktree authority collision.** Executed `diff -u /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/CLAUDE.md CLAUDE.md` (exit 1 = differences). Every differing passage is covered in the M rows: lead/team role, remote operator, explicit tool root, HIL scope, Astra reviewer, watcher/context management, standing delegation, amended fingerprint/admission, fresh rerun rule, closeout root, full merging section, three storage tiers, exact deletion approval, qualified FUSE history and appendix heading. Worktree is current for these rules: `git log -3 --format='%h %ad %s' --date=iso-strict -- CLAUDE.md` resolves 2b31a5fe/Oct10; main log resolves 6f2aebf2/Oct3; current engine digest and runbook:276 independently confirm the critical differences. Do not overwrite either checkout blindly; integrate approved current passages through MAESTRO.

2. **Hooks contradict disabled graft.** R:16 says do not use graft and ignore leftover hook text. Global settings:78,89 still runs the prompt and session-start hooks; HC/hooks.js:473-479 does retrieval before the agent can ignore text. TR:6/22 proves contradictory text reaches Claude. Existing disable intent in memory_mirror/graft-disabled-audit-2026-10-08.md is insufficient to suppress global hooks. This is a surviving cross-layer configuration gap, not a claim that the previous memory-only audit edited hooks.

3. **Context threshold/enforcement collision.** R:18 and SESSION_CHECKPOINT.md:4 still say stop <=40%; AM/sol-builders-blind-to-context.md:11 and current brief.md:30,50 require 45% stop with watcher and successor <=40%. The 300k configured ceiling is verified by main `.promptctl/memento.conf:1`; global settings.json:110-115 does not enable Memento, so its cached Stop hook (`memento/0.7.0/hooks/hooks.json:4-9`) is not active through that plugin. Retain transcript measurement and explicit reset fallback; do not rely on a hook firing. memory_mirror/context-management-every-session.md:18,22 already records both gap and early-stop rationale.

4. **Loaded memory and mirrored memory have different homes.** R:66 points to memory_mirror/MEMORY.md; TR:27 loads AM/MEMORY.md; tools/closeout_check.py:252-253 compares the older bank. Current AM-only notes: atomic-units-parallel-worktree-lanes.md, codex-session-can-type-into-maestro-pane.md, commit-verified-bytes-before-successor.md, interactive-codex-brainstorm-sessions.md, maestro-hash-pin-edits-go-to-builders.md, one-shot-run-needs-real-scale-dry-run.md, readonly-check-runs-in-maestro-shell.md, sealed-allowance-two-drift-windows.md, sol-builders-blind-to-context.md, sol-for-sweeps-astra-for-gates.md, stale-predecessor-watchers-steal-events.md. Different counterpart: gdrive-rclone-remote.md. The prior audit APPLIED.md:244-248 synchronized the older bank, not this current bank; this is a newly exposed coverage gap rather than re-reporting its closed items as unfixed. Use explicit current-loader evidence and directory-specific synchronization; never copy this thin index over the full mirror index.

5. **Subagent isolation is overstated.** G:104 denies carried CLAUDE.md; SA:7 contains both global and project instruction files. Preserve explicit requirements in prompts (G:106-109), but revise the false blanket claim. AutoMem selection has also varied across sampled subagents; never assume every lane reads the same bank.

6. **Git hygiene and repeated approval.** G:118 demands a single CI branch, while tools/git_merge_gate.py:188-195 and AM/merge-gate-first-use-learnings.md:9 allow master/live worktree branches/PR head. Gate semantics are current; do not remove live worktrees to satisfy global prose. AM merge note:8,14 also turns one handoff-approval rejection into a blanket fresh-approval requirement; preserve refusal handling and current cooperative reservations without assuming already-direct approval has expired.

7. **Duplicate state versus useful reinforcement.** R:44 copies DISCIPLINE.md:49 tracker list; keep the mandatory gate in R and consolidate list maintenance in DISCIPLINE. R:17 watcher story repeats its memory note; the exact incident substring beginning "When you catch yourself" and ending before "Send a phone push" is 183 B. R:59 preamble before "Instead:" is 446 B and repeats runbook:273; cut only that narrative, keeping every budget, archival, retention and deletion condition. The full cooperative rule R:54 is deliberate safety reinforcement and stays.

8. **Broken/implicit memory links.** AM/gdrive-rclone-remote.md:21 points to storage-archival-policy, absent in both AM and memory_mirror. Other links absent from AM do exist in memory_mirror (probe, brainstorm, LabViz, one-shot, readonly, tempdir, watcher and audit notes). They need explicit repository paths or a documented resolver; absence in AM alone is not evidence they are globally missing. All 22 audited note frontmatters contain nonempty name, description and metadata.type; no FORMAT failure found.

9. **R2 must remain design-only.** AM/remove-shared-resource-before-policing-it.md:7 says "only rule left"; adopted v4:12-17,56-60 still imposes source identity, no reverse route, exact deletion approval and verified offload. Adoption receipt:11 is current: nothing built, commissioned or switched on. Keep Intel offload and no-routine-reboot lessons without treating them as activation clearance.

10. **Session saving must respect the lane.** G:142 unconditionally asks a save; brief.md:12,43 restricts writes to the report. Save recommendations must explicitly respect the active allowlist. No context-save workflow or memory mutation was executed here.

## Injected text (text only, no hook code)

Actual sampled SessionStart graft payload, including cached upgrade notice and capped map (TR:6; 3143 B):

> ⬆ graft 0.18.0 → 0.21.1 available: run `npm i -g @nanonets/graft@latest` (restart your agent after).
>
> [graft] This repo is indexed by graft. To find, understand, or change code, reach for graft first; it answers from a prebuilt graph with exact file:line, faster than grep/read. Pick the ONE tool that fits and act on its answer. Most tasks need a single call. If one isn't enough, switch to the tool that fits the next need; don't call the same tool again and again or re-ask a question reworded:
>   • graft ask "<task>" --source: locate + understand. Ranked nodes with the code inlined at each file:line (the ≤8-line crux; add --full for the whole span). The default for "how does X work" / "where is Y".
>   • graft grep "<literal>": exhaustive find. Every occurrence, grouped by enclosing symbol; use when you need them ALL (ask is ranked top-N and misses instances).
>   • graft skeleton <file>: a file's whole API in ~200 tokens, every signature + span, ~10x cheaper than reading the file.
>   • graft callers <sym> [--direction out] [--depth N|all]: exact edges. Who calls it (default), what it calls (--direction out), or the full blast radius (--depth 2, or --depth all for every connected source). Run before you change a symbol.
>   • graft map: orientation for an unfamiliar repo, directory clusters, hubs, hotspots. map alone is the answer; don't then skeleton every subsystem it names.
>   In a monorepo, add --in <path>/ to ask/grep/callers to scope to one sub-project; hits are labeled [scope/].
>   Already know the file or symbol to change? Go straight to it: graft grep "<symbol>", read the span, edit. Save ask for when you don't yet know where the code lives.
>   Refactor, rename, or multi-file change? Run graft callers <sym> --depth all FIRST to map every connected file; editing the primary file and stopping is the classic miss (platform siblings, a new file to extract).
> Each tool opens its output with a "[graft] tokens saved ≈ N" line, sometimes with its dollar value; when you used graft this turn, close your reply with a one-line tally of the total saved, dollars included when given (e.g. 🌱 graft saved ~12k tokens (~$0.04) this turn, 3 calls). Never price tokens yourself; never pipe graft through head/tail — it is already capped, and clipping drops that line.
>
> repo map (graft/INDEX.md):
> # graft — repo map
>
> Small markdown nodes summarising this repo. `grep` any term, symbol, or
> filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
> `file:line`; open a source file only to edit the named span.
>
> The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
> `graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
> as the `graft` CLI everywhere else. Edges — who calls what — live only in the
> graph, not in these files: `graft callers <symbol>` is the only way to read them.
>
> ## Files
>
> 1264 per-file wiring cards mirror the source tree under `graft/` (993 carry extracted symbols). They are deliberately not enumerated here —
> `grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.

Actual laws routing and engagement (TR:21; 951 B per user message):

> Before substantive work, identify the medium of your primary deliverable and load the skill that matches: Skill(laws:code); Skill(laws:prompt); Skill(laws:prose). Compatible crafts may share a session, but laws:code and laws:prompt corrupt each other's work when stacked and cannot both be loaded - the guard refuses the conflicting second. For the following request, please consider the laws and devices of your craft and directly consider how you will apply them to achieve the highest quality expression of your work.  You can improve your results substantially by expressing this directly in the chat.  Engaging with the laws and devices is a must.  Although it may seem tedious to repeatedly derive these concrete details from the abstract concepts, that engagement is absolutely critical for achieving your highest quality expression.  This is not a checklist to satisfy; this is a philosophy for maximizing successful achievement of your goals.

Actual weak-match graft prompt (TR:22; 165 B; capped to two weak nudges/session by HC/format.js:135-145):

> [graft] no strong match for this prompt (name-field match 0.00) — the graph has more than this probe found. Run `graft ask "<your task>" --source` before grepping.

The strong-match variant starts with the following text; variable hit pointers/snippets follow (HC/format.js:76-94):

> [graft] starting points for this task: pull the code inline with `graft ask "<what you need>" --source`, trace impact with `graft callers <symbol>`, or search with `graft grep "<literal>"`:

The conditional laws incompatibility denial (LR:234) additionally says:

> To do laws:$craft work, dispatch a fresh subagent seeded with only that skill and keep just its answer; do not load it here. If this whole session's job has genuinely become laws:$craft, run /clear first, then load it clean.

Voice and herdr inject no instruction text by source inspection. RTK is a Bash rewrite hook; it was not run, and zero prompt-context bytes were observed in the sampled SessionStart/UserPromptSubmit records. Global settings also configures graft post-edit/tool-savings/Stop; these are event-specific, not every-user-message prompt payloads. No hooks were executed to manufacture evidence.

## Load cost

Claude loader is demonstrated by TR:27 and SA:7. Native Codex builders/Astra do not automatically load these Claude user files or run Claude hooks merely because the files exist; in this lane the user explicitly supplied AGENTS.md, which points to R as authority. Codex/Astra read R/memory_mirror only when their governing brief or read-trigger instructs them to. The quoted Codex graft injection in this session proves a separate steering channel exists, not that Claude settings are its loader. Exact Codex provider loading is outside CAA; no automatic cross-provider claim is made.

| audited file | bytes if fully read | approximate tokens | sessions and load evidence |
|---|---:|---:|---|
| G | 13817 | 3,454 | Claude main + subagent, TR:27/SA:7; no native Codex/Astra auto-load shown |
| T | 964 | 241 | Claude import G:1; TR:27/SA:7 |
| R | 18899 | 4,725 | Claude worktree Project, TR:27/SA:7; Codex/Astra explicit brief/manual read |
| M | 10094 | 2,524 | Claude sessions rooted on main, project-anchor scope; not in sampled worktree TR |
| AM/MEMORY.md | 3277 | 819 | Claude AutoMem, TR:27/SA:7; note bodies not automatically concatenated |
| AM/atomic-units-parallel-worktree-lanes.md | 1449 | 362 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/codex-session-can-type-into-maestro-pane.md | 1251 | 313 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/commit-verified-bytes-before-successor.md | 1258 | 314 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/dry-admission-probe-before-one-shot.md | 1460 | 365 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/gdrive-rclone-remote.md | 1809 | 452 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/infra-closeout-template-d-hw-2.md | 1271 | 318 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/intel-exists-to-offload-the-m3.md | 1368 | 342 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/interactive-codex-brainstorm-sessions.md | 1341 | 335 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/labviz-wireframe-before-spec-approval.md | 2040 | 510 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/m3-hosts-the-team-no-routine-reboots.md | 1513 | 378 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/maestro-hash-pin-edits-go-to-builders.md | 1236 | 309 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/merge-gate-first-use-learnings.md | 1297 | 324 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/one-shot-run-needs-real-scale-dry-run.md | 1187 | 297 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/readonly-check-runs-in-maestro-shell.md | 1943 | 486 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/remove-shared-resource-before-policing-it.md | 1453 | 363 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/rerun-builder-tests-host-tmpdir.md | 1545 | 386 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/sealed-allowance-two-drift-windows.md | 1323 | 331 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/sol-builders-blind-to-context.md | 1026 | 256 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/sol-for-sweeps-astra-for-gates.md | 1355 | 339 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/stale-predecessor-watchers-steal-events.md | 1103 | 276 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/stop-open-ended-builder-self-audits.md | 1381 | 345 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| AM/timed-chain-prebuild-gate-checker.md | 2090 | 522 | Claude on recall/read; 0 automatic body bytes in TR:27; Codex/Astra only explicit read |
| global settings.json | 5353 | 1,338 if read manually | Configuration parsed by Claude, not injected wholesale; only hook outputs count |
| graft hook wrapper | 2781 | 695 if read manually | Executable, not prompt text |
| HC/hooks.js | 22792 | 5,698 if read manually | Executable, not prompt text |
| HC/format.js | 12508 | 3,127 if read manually | Executable; emitted portions above count |
| LR skill-router.sh | 13302 | 3,326 if read manually | Executable; emitted strings above count |
| laws hooks.json | 1142 | 286 if read manually | Configuration, 0 wholesale prompt bytes |
| voice-stop.sh | 425 | 106 if read manually | Executable, 0 instruction bytes |
| herdr-agent-state.sh | 3070 | 768 if read manually | Executable, 0 instruction bytes |

Current four-file Claude worktree anchor cost: **36,957 B (~9,239 tokens)**. Sample TR loaded the pre-addition AM index (3,079 B without terminal newline); current source index is 3,277 B. The 22 note bodies total **31,699 B (~7,925 tokens)** only if all are explicitly read; do not add them to every-turn baseline. Main anchor is 10,094 B versus worktree 18,899 B (difference 8,805 B).

Observed initial hook text: **3,483 B** (3,143 graft + 340 laws routing; ~871 tokens). Every substantive user message gets **951 B** laws text (~238 tokens); sampled weak-match graft adds **165 B** (~41 tokens). Repeated routing accounts for 340 B of the 951 B. Strong-match graft size is variable and capped to three hits, with novelty suppression; source-state/upgrade banners may vary. File anchor content persists in context and can be cached; it is not freshly appended each turn. Hook payloads are appended at their events; this audit makes no dollar-cost claim.

Source limits: no live hooks, gate suites, host observation, OAuth refresh or science ran. Historical incident timing/counts are retained as dated reports, not re-certified acceptance. Main/master and current engine claims were independently checked by read-only Git and byte hashing. Snapshot churn was limited to the new atomic-units note/index addition observed above.

## Verdict counts

78 rows; dual verdicts counted separately: KEEP 53 · BLOAT 3 · CONFLICT 9 · DUPLICATE 3 · NONFACTUAL 1 · STALE 8 · AMBIGUOUS 7 · MISLEADING 3 · HISTORICAL 2 · UNREACHABLE 1 · FORMAT 0.

Lines: 220
