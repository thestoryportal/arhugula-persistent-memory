# CPS — preservation sweep
Snapshot: 2026-10-12T01:55:25.387093+00:00; W HEAD `9d71809cae83b7b4c9bb1115b792e97dda447b6e`; shared worktree changed during inspection. Read-only audit; only this report written; no commits or activation.
W = this worktree; M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory; H = /Users/robertrhu; A = results/context_audit_20261012.
B = results/compute_storage_brainstorm_20261011T054507Z; S1 = W/memory_mirror; S2 = H/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory; S3 = H/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory.
GA = H/.codex/AGENTS.md; CM = H/.codex/memories; HF = H/.claude/memento/handoffs; PS = docs/program_state.json; RB = EXPERIMENT_RUNBOOK.md. All unprefixed paths are in W. Citation aliases expand to exact paths.
Correction to the brief’s background: local M/master is Oct 4; locally cached origin/master contains the Oct 10 cleanup. A/ROOT_CAUSE.md:8 now distinguishes them. No fetch/network was performed. Every M/file citation below describes that stale local folder, never upstream master content.
Master content was checked with `git show origin/master:<path>`: origin/master:CLAUDE.md:16,30,52,61 already preserves Astra review, the current engine pin, the merge gate and exact deletion approval; origin/master:DISCIPLINE.md:88 already removes the iteration cap. The newer context policy is still absent there (origin/master:CLAUDE.md:18 and origin/master:AGENTS.md:7 retain ~20%).

## 1. R2 — finding-by-finding attribution

Unit = one numbered blocking/required-condition F finding, including commissioning conditions and the correctly retained r2c_r2 F5 freeze condition. Repeated findings count again when they prolong a later round; required-change/closure tables do not count again.
Classes: (a) intrinsic to sharing one drive between two machines under the retained exclusion contract; (b) demonstrated dropped decision or stale/missing/conflicting instruction; (c) other design, implementation, test or schema defect. (b) identifies a textual propagation/application defect; it does not prove the Oct 10 cleanup caused it.
All 14 B/astra_r2*verdict.md files were read, including both requirements rounds and both later redesign reviews: 10 NO-GO (r2f–r2o), 4 GO-WITH-CONDITIONS. Original sharing and later M3-local redesign findings are included, not silently conflated.

| Verdict / finding | Class | Finding and attribution | Evidence |
|---|---|---|---|
| r2c F3 | (a) | 15 inherited T/U/V controls require containment, durable ownership, closure and recovery; implementation absent. | B/astra_r2c_verdict.md:11 |
| r2c F4 | (c) | Acceptance omits duplicate registration, expiry, reboot/remount, independent invalidation and real admission compatibility. | B/astra_r2c_verdict.md:33 |
| r2c F5 | (c) | Release test is temporally ambiguous; post-release delayed dispatch must also be excluded. | B/astra_r2c_verdict.md:45 |
| r2c F6 | (c) | Selected mechanisms and separate freeze/commissioning/acceptance gates remain incomplete. | B/astra_r2c_verdict.md:47 |
| r2c_r2 F5 | (c) | Requirements corrections accepted; original implementation freeze remains OPEN, correctly withholding dispatch. | B/astra_r2c_r2_verdict.md:26 |
| r2d1 F1 | (b) | HW1 choice 7 dropped: RD:115 says recovery optional despite decisions_log.md:95–101,191. Builder source: codexr2d_brief.txt:18,24; reviewer: astra_r2d1_packet.md:18. | B/astra_r2d1_verdict.md:5 |
| r2d1 F2 | (c) | UID emptiness can miss fork/exit churn in the later M3-local redesign; this remains a local observation defect after two-Mac sharing is removed. | B/astra_r2d1_verdict.md:7 |
| r2d1 F3 | (c) | Writable trusted files can move activity across UIDs in the later M3-local redesign; this is not intrinsic to two machines sharing memit. | B/astra_r2d1_verdict.md:11 |
| r2d1 F4 | (c) | One passing maximum workload does not establish a budget bound for all admitted inputs/retries/cache states. | B/astra_r2d1_verdict.md:17 |
| r2d1 F5 | (c) | Adoption and operational acceptance conflated, creating a circular gate. | B/astra_r2d1_verdict.md:40 |
| r2d2 F1 | (c) | Concurrent Python maintenance probes block the unchanged science gate; lifetime is not bounded by existing code. | B/astra_r2d2_verdict.md:7 |
| r2d2 F2 | (b) | RD3:22,24,29,53–57 extends answer 6 copy-overlap permission to cleanup/retrieval; narrower source is r2_redesign_operator_r8_answers.md:16–17,23, supplied in astra_r2d2_packet.md:9,16. | B/astra_r2d2_verdict.md:9 |
| r2f F1 | (c) | Owner/session assignments, literal entrypoints/profiles, receipt grammar and hashes remain deferred. | B/astra_r2f_verdict.md:7 |
| r2f F2 | (c) | Suspended executor must consume its allowance before it can execute: startup deadlock. | B/astra_r2f_verdict.md:23 |
| r2f F3 | (a) | Recovery observer requires registration by the dead/stuck coordinator it must independently fence. | B/astra_r2f_verdict.md:25 |
| r2f F4 | (c) | Grant/clearance, approval, observation, profile and successful-response schemas missing. | B/astra_r2f_verdict.md:27 |
| r2f F5 | (b) | Wrong source instruction: freeze_v1:18 read nonexistent integration_plan ranges and no replacement; integration_plan.md:89 names integration_r5_completion_table.md; contract already cited that successor. | B/astra_r2f_verdict.md:37 |
| r2g F1 | (a) | Shared-storage entrypoint completeness remains unproved: missing MathLab children and false CUDA retirement exclusions. | B/astra_r2g_verdict.md:7 |
| r2g F2 | (a) | Recovery dependencies/storage share the authority root whose failure they must survive; sandbox permissions also conflict. | B/astra_r2g_verdict.md:18 |
| r2g F3 | (c) | Invocation profile hashes contain their own required hash value; profiles cannot be ordinarily constructed. | B/astra_r2g_verdict.md:26 |
| r2g F4 | (c) | Initialization cannot represent no previous writer or unknown prior history without fabricated identities. | B/astra_r2g_verdict.md:36 |
| r2g F5 | (c) | Structural checker misses malformed schema shapes, coordinated interface omission and construction instances. | B/astra_r2g_verdict.md:42 |
| r2h F1 | (a) | Tokenizer entrypoints and closed environments/dependency identities still missing from shared-storage coverage. | B/astra_r2h_verdict.md:7 |
| r2h F2 | (c) | Science launch-ID binding has no consistent selected immutable source; example does not follow frozen template. | B/astra_r2h_verdict.md:18 |
| r2h F3 | (c) | Checker equates observed precommit revision with resulting committed revision; impossible clearance construction accepted. | B/astra_r2h_verdict.md:24 |
| r2h F4 | (c) | Bindings not dereferenced/rerendered semantically; omitted mandatory references remove their own validation. | B/astra_r2h_verdict.md:36 |
| r2i F1 | (c) | Production payload and synthetic guard disagree about LaunchProfile.invocation ownership/composition. | B/astra_r2i_verdict.md:7 |
| r2i F2 | (c) | TOP_LEVEL no-op admission exposes inner P2 launcher without its required outer gate/coordinator. | B/astra_r2i_verdict.md:15 |
| r2i F3 | (c) | Unsandboxed-science exemption conflicts with Process schemas and permits non-science roles/capabilities. | B/astra_r2i_verdict.md:23 |
| r2i F4 | (a) | Imported P3 Git children omitted; ordinary unchanged spawns lack the required pre-release enrollment mechanism. | B/astra_r2i_verdict.md:34 |
| r2i F5 | (b) | DS invents activity from basename absence and misidentifies AutoResearch Arm R as C10W; actual ruling: results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18; reviewer inspected DS and queue. | B/astra_r2i_verdict.md:48 |
| r2i F6 | (c) | QUERY observation coherence and mandatory-reference completeness escape semantic checks. | B/astra_r2i_verdict.md:58 |
| r2j F1 | (b) | D3/DR:28–34 and freeze_v5:209,260–263 claim recipe declaration satisfies unchanged contract:87,115–117 process registration; reviewer read both. Conflicting new instruction, not proof a memory was overwritten. | B/astra_r2j_verdict.md:7 |
| r2j F2 | (c) | Guard invocation omits its mandatory sandbox while sandbox forbids its assigned admission/payload execution. | B/astra_r2j_verdict.md:15 |
| r2j F3 | (c) | Direct P2 evaluator/trainer still TOP_LEVEL with no-op admission, bypassing required outer obligations. | B/astra_r2j_verdict.md:23 |
| r2j F4 | (c) | Aggregate admission receipt needs 35 hashes but schema allows only 32; individual binding GREEN misses it. | B/astra_r2j_verdict.md:31 |
| r2j F5 | (c) | Refusal variants omit required operands/arity; real source-valid invocation does not match the frozen refusal. | B/astra_r2j_verdict.md:39 |
| r2j F6 | (c) | Locally valid bindings can use different launch contexts in one production tree. | B/astra_r2j_verdict.md:47 |
| r2k F1 | (b) | P3 labels admission/fingerprint helpers A1 science descendants, conflicting with r2_round8_decisions.md:13–17 (roots/all non-science retain pre-release registration); reviewer read D8 and F6. | B/astra_r2k_verdict.md:5 |
| r2k F2 | (c) | Direct P1/P3 evaluation no-ops omit caller guard_phase_projection and its live phase-budget check. | B/astra_r2k_verdict.md:13 |
| r2k F3 | (c) | Delegation hashes can reference another launch despite local binding/context labels passing. | B/astra_r2k_verdict.md:23 |
| r2l F1 | (b) | A1 leakage persists through imported verifier/Git admission branches; D9:9 excludes every admission-spawned process, but P4 labels them SCIENCE/A1; reviewer traced D9, freeze and source. | B/astra_r2l_verdict.md:5 |
| r2m F1 | (c) | P2 argv does not guarantee P2 certificate: loaded P3 certificate can spawn unrepresented Git descendants before rejection. | B/astra_r2m_verdict.md:5 |
| r2n F1 | (c) | Seven disk-selected linked records trigger seven Git probes before six-unit validation; six-recipe fixture is incomplete. | B/astra_r2n_verdict.md:5 |
| r2n F2 | (c) | Verifier and phase_trains independently load adapter operands; their union need not fit one six-recipe set. | B/astra_r2n_verdict.md:13 |
| r2o F1 | (c) | p1-project has children=[] although verifier runs before its stage branch; no independent missing-child check. | B/astra_r2o_verdict.md:5 |
| r2o F2 | (c) | Certificate-selected replication coverage omitted on science P1/P2 origins; D15 item 6 was present in packet, so missing recall is unproved. | B/astra_r2o_verdict.md:13 |
| r2o F5 | (b) | freeze_v10.md:317 retains K5/P3/r2s_report, contradicting :330,359 K9/current packet; reviewer packet astra_r2o_packet.md:21 explicitly disclosed stale instruction. | B/astra_r2o_verdict.md:47 |

Counts: **48 numbered blocking/conditional findings: (a) 6, (b) 8, (c) 34**; these are review-occurrences, not independent root causes.
Nonblocking findings excluded explicitly: r2c F1/F2/F7; r2c_r2 F1–F4; r2d1 F6; r2d2 F3–F5; r2f F6; r2g F6; r2h F5; r2i F7; r2j F7; r2k F4; r2l F2–F4; r2m F2–F4; r2n F3–F5; r2o F3/F4/F6. Their native/commissioning qualifications remain intact.
**Verdict on the operator’s hypothesis:** preservation/propagation failures demonstrably added work (8 class-b occurrences), especially the repeated A1 boundary error and missing recovery choice. But the evidence does **not** support the stronger claim that stale local-checkout/cache/config instructions caused the original shared-drive impasse: the reviewed packets generally supplied the relevant decisions, and the terminal completeness problem survives correct instructions. The sweep/tracer record identifies 1,302 unresolved callees and 94 boundaries (B/r2_redesign_operator_ruling.md:3); replacing shared access was an operator scope change, not a recovered forgotten earlier instruction. HW1 choice 7 and r2d2 overlap expansion are later redesign defects, so neither explains the preceding ten NO-GOs. Class-b findings show local instruction loss/conflict, not a traced builder/reviewer reading stale M/S2/CM bytes.

## 2. Operator rulings not consistently preserved

Rows identify surviving authority plus a specific stale or missing reader path; “missing” means recall/propagation gap, not erased evidence. A scoped choice need not be duplicated into every global/scoped guide if its authoritative route is intact. Historical permissions do not override a later hold or this sweep’s restrictions.

| Date / short verbatim words | Correctly held | Missing or contradicted reader path | Wrong action a session could take |
|---|---|---|---|
| 10-04 “not on rented servers” | S1/local-only-no-rented-compute.md:8; AGENTS.md:70 | M/AGENTS.md:52,126 still 4090/Intel; SESSION_BOOTSTRAP.md:100 remote GPU | Plan CUDA/rented compute or obsolete deployment. |
| 10-06 “gpt-sol-6.1 max” | S1/model-and-compute-allocation.md:8,12; CLAUDE.md:16 requires Astra-high gates | M/CLAUDE.md:16 gpt-5.5; .codex/config.toml:9 gpt-5.5; S2/MEMORY.md:38 fallback | Launch wrong builder/reviewer, or treat advisory fallback as binding review. |
| 10-06 “not very useful really for observability” | S1/model-and-compute-allocation.md:12 interactive tmux builders | GA has no program-role/interactive-builder rule; scoped experiments/AGENTS.md:15 obsolete review route | Use headless builder/default review without required observability/roles. |
| 10-06 “until the human interrupts you, period” | DISCIPLINE.md:88; RB:367; docs/AUTORESEARCH.md:3–5 | M/DISCIPLINE.md:87 caps at 12; M:42 points at obsolete skill | Stop adopted optimizer at an invented iteration cap. |
| 10-06 “Don't bring those types of questions to me please” | S1/operator-decision-scope.md:8,12; CLAUDE.md:15 | S3 has no operator-decision-scope note; M/AGENTS.md lacks team role contract | Escalate routine method/word-list decisions instead of resolving them. |
| 10-06 “clear, understandable and concise” | S1/plain-language-to-operator.md:8; S2 same note | S3 lacks that standing note; GA lacks program-specific phone/recommendation-first route | Send jargon/large command dumps or reopen settled choices. |
| 10-06 “plain description … top of the repo's README” [memory paraphrase, not recovered direct quote] | S1/readme-plain-words-summary.md:8,12; DISCIPLINE.md:52 | M/DISCIPLINE.md §1.1 has no plain-language progress-push obligation; S3 lacks note | Push progress without refreshing operator-facing README. |
| 10-06 “Continue through the night” | S1/operator-overnight-autonomy-2026-10-06.md:8; CLAUDE.md:22 with exceptions | M/CLAUDE.md lacks current delegation; S3 lacks note; S1:20 still older merge/budget wording | Idle unnecessarily or treat blanket initiative as overriding current run/scope gates. |
| 10-07 “And push it all” | RB:391; CLAUDE.md:17; S1/commit-forward-work-without-asking.md:8,13 | S3 no standing push note; GA generic completion/save rules have no MAESTRO/builder distinction | Leave verified MAESTRO work local, or let a builder commit/push outside brief. |
| 10-07 “historically on all of the models we have tested” | RB:397; S1/lab-view-and-live-telemetry.md; later LabViz choices map | M and older scoped guides do not route to the newer LabViz plan/hold; S3 lacks telemetry note | Narrow visualization to current C10 slice or confuse historical data with new replay permission. |
| 10-08 “never allow an experiment … not be rerun” | RB:412; CLAUDE.md:40; S1/rerun-never-patch.md:8–11 | M/AGENTS.md:84 omits fresh-process rerun; S1 note lacks spent-attempt authorization qualification | Read around a compromised run, or rerun a spent single attempt without fresh GO. |
| 10-08 “Any experiment, as needed” | RB:415; S1/operator-overnight-autonomy-2026-10-06.md:14 | Same note:20 and current CLAUDE.md:15,22 retain frozen-cap/operator exceptions; no explicit resolution in S3/GA | Either block measured authorized budget work or overextend it to a frozen/spend fork. SOURCE CONFLICT stays OPEN. |
| 10-08 “not comfortable giving permission for my entire Mac internal drive” | S1/backup-via-memitbackup-app.md:11; S2 same; RB:438 | S3 lacks narrow-access/FDA refusal note; M/CLAUDE.md:49 still bare launchd/internal archive route | Request Full Disk Access or trust an unqualified launchd backup recipe. |
| 10-08 “I approve the use of InfraNodus for all work now and forever” | S1/infranodus-standing-approval.md:7,11; S2 same | S3 lacks note; root AGENTS.md research-tool section only describes optional credentials | Ask again for the already granted prose scope; this does not waive missing credentials or an actual denial. |
| 10-09 “This context directive must be made durable through any and all handoffs” | AGENTS.md:6–8; S1/context-management-every-session.md:8 | M lacks directive; origin/master:AGENTS.md:7 still ~20%; S2/MEMORY.md:1 ~20%; GA:141 unconditional context-save | Stop too late or write unauthorized save artifacts instead of the scoped handoff. |
| 10-10 “raise the maestro context ceiling to 300k, instead of 180k” | S1/context-management-every-session.md:20–22; CLAUDE.md:18 | S1:13 says wait for hook, contradicted by :18 inactive plugin; S3 lacks ceiling note; origin/master old threshold | Wait for a hook that never fires, or reset against an old ceiling. |
| 10-11 watcher-delivered 45% stop [observed operating rule, not a recovered operator quote] | S3/sol-builders-blind-to-context.md:7–11; current sweep brief last section | Root AGENTS.md:7 assumes visible gauge/40%; S1/S2 lack this note; CM records some task-specific 45% handoffs only | Expect a blind builder to self-stop; omit MAESTRO watcher/message. |
| 10-09 “Giddy up…orchestrate the work” | S1/never-idle-arm-completion-watch.md:8; CLAUDE.md:17 | Same note:16 old <25% alert; old token-anchoring sibling unindexed; S3 stale-watcher lesson absent S1/S2 | Miss completion/context events or trust an echoed reply token. |
| 10-09 storage policy: no internal-SSD warehouse [recorded ruling] | CLAUDE.md:58–59; RB §3.3a; S1/backup-via-memitbackup-app.md:9 | M/CLAUDE.md:49 explicitly calls internal SSD durable archive | Park irreplaceable bulk internally and call it protected. |
| 10-10 “ask my permission for you to run it yourself” | S1/approved-deletes-ask-then-rmtree.md:10–12; CLAUDE.md:61 | M/CLAUDE.md:51 stale reclaim carve-out; S3 lacks deletion note | Delete an eligible path without exact current path/size/method approval. |
| 10-10 first gated merge GO [handoff-reported operator choice] | HF/maestro9_takeover_20261010.md:31–32; CLAUDE.md:50–54; origin/master same gate | S1/S2 commit-forward-work-without-asking.md:13 says operator merges; overnight note:20 never merge; M lacks gate | Bypass cooperative reservation/gate or refuse a legitimately authorized MAESTRO merge. |
| 10-10 “Turn on, keep fixing” → later wait for fixed build [superseded] | HF/maestro8_takeover_20261010.md:33; maestro9_takeover_20261010.md:40; RB:440 | Old handoff still grants activation; M archive recipe and broad standing notes omit amendment | Activate the superseded defective build. Later activation approvals remain separate. |
| 10-10 “Yes, run it once” | HF/maestro23_takeover_20261010.md:13; PS:12 says authorization consumed | SESSION_CHECKPOINT.md:53 NOT RUN; generic rerun note lacks single-use caveat | Run NEW-1 a second time from stale startup state. |
| 10-10 “C10Y should be defered” | RB:431; S1/c10y-deferred-behind-drive-backup.md:8; PS retest/Drive queue | S2/S3 lack deferred note; old PS:15 still routes to C10Y calibration; S1 description implies backup alone unblocks | Remove C10Y permanently or resume terminal calibration without reclaim/review/fresh GO. |
| 10-11 “Approve, with minted token” | RB:432; results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18; PS:374–375 | R2 DS claimed Arm R=C10W (B/astra_r2i_verdict.md:48–56); S1/S2/S3 have no standalone re-test ruling note | Plan the wrong Arm R, or mistake planning approval for a run GO. |
| 10-11 “dynamically updated so it is never stale” | S1/work-queue-tab-keep-current.md:8; PS/work_queue | S2 same-name note lacks later maintenance extensions (byte comparison); PS:50 still repeats corrected no-merge claim | Show a stale queue or overwrite predecessor notes/dependencies on a queue patch. |
| 10-11 “I approve this session's design” | B/decisions_log.md:181–183; RB:458; PS:14 | M/root guides and S2 lack D-HW-2 integration/current role note; PS:13 still Neo4j on M3 | Build obsolete same-host engine or dispatch affected work without cross-cutting reconciliation. |
| 10-11 HW1 choice 7 “A” | B/decisions_log.md:99–101,191; redesign v4 preserves recovery | B/r2_git_drive_redesign_v1.md:115 made recovery optional; S1/S2/S3 have no choice-7 note | Drop seven-daily/four-weekly restore history and old-version recovery. |
| 10-11 “Before beginning building work … please wait” | HF/maestro45_takeover_20261011.md:7; PS:284–285 | M startup/older broad LabViz build rulings lack hold; S2 lacks wireframe/hold note | Start dashboard/LabViz BUILD from earlier blanket approval. |
| 10-11 “I will review the report first” | HF/maestro47_takeover_20261011.md:8; successor HF/20261012T002451Z-56625.md:2 | PS needs_from_you asks for choices with blocked_by=[]; its historical note DOES preserve the review-first condition; no standalone recall note | Ask SUMMARY adoption questions before the operator says review is complete. |
| 10-11 “other domains … one by one” | HF/maestro48_takeover_20261011.md:9; S3/interactive-codex-brainstorm-sessions.md:8 | S1/S2/GA lack brainstorm-session contract | Replace operator-driven discussion with a builder-style task or move domains prematurely. |
| 10-11 “Once Astra approves the spec … static wireframe” | S1/S3/labviz-wireframe-before-spec-approval.md:7,11 | S2 missing note; S3/MEMORY.md:13 still no Figma yet although note:11 records configured/sign-in | Skip visual review before approval/build or reopen solved tool setup. |
| 10-11 “will do just as good … cost much less” | HF/maestro60_takeover_20261011.md:22; S3/sol-for-sweeps-astra-for-gates.md:7–11 | S1/S2/GA missing sweep-role/loop-escalation instruction; CM no dedicated note | Spend Astra on repeated sweeps instead of Sol sweep/tracer, then binding gate. |
| 10-11 “Can the Intel Mac pull … directly from Git” | B/r2_redesign_operator_ruling.md:5–11; S1/S3/remove-shared-resource-before-policing-it.md:7 | S2 missing note; old integration/profile artifacts retained without universal reader tombstone; PS:14 second-memit-copy wording | Resume retired shared-memit R2 freeze or give Intel a memit route. |
| 10-11 “never maxed and stops science mid stream” | B/r2_redesign_operator_ruling.md:9–11; adopted v4 S1–S12 | S1 removal note:7 compresses to proactive storage without numeric acceptance; S2 absent; M only old archive/cap recipe | Treat monitoring or one passing sample as a guarantee; ignore peak/support-writer bounds. |
| 10-11 “The whole point of the Intel is to offload work like uploading” | B/r2_redesign_operator_r8_answers.md:8,16,22; S1/S3/intel-exists-to-offload-the-m3.md:11 | S2 absent; S1/S3 removal note:7 still M3-only backup/science exclusion shorthand | Put slow Drive upload on M3 or incorrectly prohibit approved M3-initiated source-read push. |
| 10-11 account question “No”; copy-overlap question “Yes (Recommended)” | B/r2_redesign_operator_r8_answers.md:9,17,23; adopted v4 | Older redesign v1/v2 require UIDs; v3 generalized overlap to destructive maintenance (astra_r2d2 F2) | Commission rejected accounts or apply accepted copy risk to cleanup/restore. |
| 10-11 “Adopt (Recommended)” | B/r2_redesign_operator_adoption.md:9–11; RB:475; PS:5 | Older Gate-1/commissioning language and broad standing approval lack explicit v4 replacement; S2 no adoption note | Treat adoption as activation or continue a canceled original R2 round. |
| 10-12 “Update the plan” | PS:230–231; HF/20261012T002451Z-56625.md:2; LabViz settled-choice ledger | Old Oct 7 LabViz build-all rulings remain in startup history; S2 lacks new wireframe/hold sequence | Implement UI while only v3 writing/review is authorized. |
| 10-12 “VERY atomic … their own worktrees” | S3/atomic-units-parallel-worktree-lanes.md:11–15 | S1/S2/GA absent; S1/parallel-builders-name-each-others-files.md:8–12 still shared-tree mitigation | Dispatch long overlapping builders instead of small isolated units. |
| 10-12 “Fix absolutely everything” [queue-recorded quote] | PS:50–51 specifies context hygiene then stop; S3/context-hygiene-must-reach-every-store.md:11–15 | PS still lists other ready/running work without per-item hygiene pause; generic standing-autonomy notes omit latest hold | Resume science/activation/build work before context cleanup and operator stop. |
Dates without year are 2026. Bracketed entries are source-labelled paraphrases/observations where the operator’s exact words were not recovered; they are not presented as direct quotes. The 144 settled LabViz choices are preserved in a Git choices map (PS:231), not 144 erased directives; scoped HW choices/conditional trials remain in B/decisions_log.md. Missing generic-anchor duplication is not itself a defect when the task packet routes to those sources.

## 3. Lessons present in only one store

Census: stdlib pathlib glob("*.md") + filename set differences + SHA-256 of same-name bytes, all three stores read successfully. S1=202 files, S2=125, S3=24; **68 S1-only (36 retired, 31 other notes, 1 historical checkpoint), 0 S2-only, 12 S3-only**. Earlier A/SYNTHESIS.md:40,55–57 counted 11 S3-only; new context-hygiene note makes 12.
Visibility for EVERY row: Codex builders and Astra **can read the named path explicitly** under this host’s read permissions; neither is guaranteed to receive its body. I = S1 index supplies a discovery pointer; U = no S1 index pointer, requires file search/explicit packet; S = active Claude S3 recall/index, outside Git and not a Codex/Astra default attachment. All three codes mean C/A manual access possible, automatic recall unproved. Retired notes are preserved tombstones, not lessons to reactivate.

| Sole store / exact note evidence | Recall route / state |
|---|---|
| S1/SESSION_CHECKPOINT.md:1 | U; historical checkpoint |
| S1/anyedit-clearing-c10-would-close-tested-write-serve-scope.md:3 | U; retired |
| S1/anyedit-connectedpapers-adds-diagnostics-not-plan-change.md:3 | U; retired |
| S1/anyedit-default-window-collapses-c10-a7.md:3 | U; retired |
| S1/anyedit-gate-upgraded-by-muke-coin-suit.md:3 | U; retired |
| S1/anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md:3 | U; retired |
| S1/anyedit-local-transplant-controls-fail-before-a7.md:3 | U; retired |
| S1/anyedit-precommit-triage-proceed-but-viability-gated.md:3 | U; retired |
| S1/anyedit-token-alignment-gate-prevents-false-rescue.md:3 | U; retired |
| S1/ask-astra-automatic-before-operator-chore.md:3 | I; lesson retained |
| S1/autonomy-drifts-from-kickoff-scope.md:3 | U; lesson retained |
| S1/autoresearch-is-not-a-faithfulness-gate.md:3 | U; retired |
| S1/background-monitor-no-premature-read.md:3 | U; retired |
| S1/c10-band-knobs-failed-for-hard-coined-values.md:3 | U; retired |
| S1/c10-edit-collateral-breaks-injected-target.md:3 | U; lesson retained |
| S1/c10-edit-rotates-required-target-direction.md:3 | U; lesson retained |
| S1/c10-layerpick-null.md:3 | U; lesson retained |
| S1/c10-secondkey-null-large-write.md:3 | U; lesson retained |
| S1/c10-sharedz-underfit.md:3 | U; lesson retained |
| S1/c10-solvefeas-underfit-at-50.md:3 | U; retired |
| S1/c10-stacked-solve-tradeoff.md:3 | U; lesson retained |
| S1/c10-status-and-session-b-residual-test.md:3 | U; retired |
| S1/c10-twopass-solve-null-at-margin.md:3 | U; lesson retained |
| S1/c10y-deferred-behind-drive-backup.md:3 | I; lesson retained |
| S1/canonical-fit-is-not-c10-rescue.md:3 | U; retired |
| S1/check-for-running-duplicate-before-launch.md:3 | I; lesson retained |
| S1/codex-brief-handoff-file-narrow-reads.md:3 | I; lesson retained |
| S1/codex-chatgpt-oauth-model-slug.md:3 | U; retired |
| S1/codex-hook-trust-prompt-at-launch.md:3 | I; lesson retained |
| S1/codex-review-embed-evidence-and-effort.md:3 | U; retired |
| S1/codex-watch-anchor-replies-read-context-from-rollout.md:3 | I; lesson retained |
| S1/codex-watch-anchor-tokens-read-context-from-rollout.md:3 | U; lesson retained |
| S1/codex-web-review-lanes.md:3 | I; lesson retained |
| S1/cross-process-contracts-one-enforcer.md:3 | I; lesson retained |
| S1/decision-id-check-before-assigning.md:3 | I; lesson retained |
| S1/deployment-target-intel-cpu.md:3 | U; retired |
| S1/e2e-ground-truth-situate-on-the-map.md:3 | U; retired |
| S1/exhaust-options-before-blocked.md:3 | U; lesson retained |
| S1/experiment-gate-before-next-science-arc.md:3 | U; retired |
| S1/gemma4-rung4-candidate.md:3 | U; retired |
| S1/importing-external-files-traps.md:3 | I; lesson retained |
| S1/in-weight-vs-sidestore-f1-question.md:3 | U; retired |
| S1/intel-mac-node-access.md:3 | I; lesson retained |
| S1/larql-the-mechanism-prior-art.md:3 | U; retired |
| S1/local-only-hardware-rule.md:3 | U; retired |
| S1/memit-cov-inversion-not-a-hang.md:3 | U; retired |
| S1/molab-migration-assessment.md:3 | U; retired |
| S1/native-applet-removable-volumes-prompt.md:3 | I; lesson retained |
| S1/neuraldb-scr-keep-side-store-pressure-live.md:3 | U; retired |
| S1/notebooklm-install-and-notebook-ids.md:3 | U; retired |
| S1/operator-profile-llm-as-database.md:3 | U; retired |
| S1/operator-scaffolding-phase-tooling.md:3 | U; retired |
| S1/parallel-builders-name-each-others-files.md:3 | I; lesson retained |
| S1/perplexity-c10h-reranks-anyedit-failure-geometry-first.md:3 | U; lesson retained |
| S1/perplexity-mcp-restore-from-pod-restore.md:3 | U; retired |
| S1/pod-restart-wipes-system-python-ml-stack.md:3 | U; retired |
| S1/q4km-quantization-survival-pass.md:3 | U; lesson retained |
| S1/read-handoff-before-launching-successor.md:3 | I; lesson retained |
| S1/record-provenance-per-test-run.md:3 | I; lesson retained |
| S1/repo-reorganized-llmdb-root.md:3 | U; retired |
| S1/research-pass-2026-10-06-sequence.md:3 | U; retired |
| S1/runpod-dashboard-vs-pod-metrics.md:3 | U; retired |
| S1/runpod-durable-experiment-launch.md:3 | U; retired |
| S1/runpod-session-disconnect-cause.md:3 | U; retired |
| S1/sandbox-green-is-not-host-green.md:3 | I; lesson retained |
| S1/scope-gate-batch-is-deployment-model.md:3 | U; lesson retained |
| S1/trim-builder-reading-lists.md:3 | I; lesson retained |
| S1/wide-intermediate-7b-editing-vram.md:3 | U; lesson retained |
| S3/atomic-units-parallel-worktree-lanes.md:3 | S; lesson retained |
| S3/codex-session-can-type-into-maestro-pane.md:3 | S; lesson retained |
| S3/commit-verified-bytes-before-successor.md:3 | S; lesson retained |
| S3/context-hygiene-must-reach-every-store.md:3 | S; lesson retained |
| S3/interactive-codex-brainstorm-sessions.md:3 | S; lesson retained |
| S3/maestro-hash-pin-edits-go-to-builders.md:3 | S; lesson retained |
| S3/one-shot-run-needs-real-scale-dry-run.md:3 | S; lesson retained |
| S3/readonly-check-runs-in-maestro-shell.md:3 | S; lesson retained |
| S3/sealed-allowance-two-drift-windows.md:3 | S; lesson retained |
| S3/sol-builders-blind-to-context.md:3 | S; lesson retained |
| S3/sol-for-sweeps-astra-for-gates.md:3 | S; lesson retained |
| S3/stale-predecessor-watchers-steal-events.md:3 | S; lesson retained |

Same-name collisions: MEMORY.md (all differ), gdrive-rclone-remote.md (S3 differs), graft-disabled-audit-2026-10-08.md and work-queue-tab-keep-current.md (S2 lacks S1 extensions). The census compared content, not mtimes; distinct role indexes must not be blindly overwritten.
S3-only lessons cover atomic worktrees, pane-message authority, verified-byte-before-successor commits, all-store hygiene, interactive brainstorms, frozen-pin fixes/denials, real-scale one-shot tests, host-shell sandbox proof, two budget drift windows, blind-builder context, Sol sweeps/Astra gates and stale watchers. Twelve filesystem-readable notes are not twelve guaranteed recalled rules.
CM is separate personal memory, not a fourth program mirror: CM/MEMORY.md:3–4 preserves R2 static/host boundaries; historical generated memories retain some ~20% recipes. No dedicated atomic-unit/Sol-sweep/300k rule was found by the exact-phrase scan across 171 CM Markdown files; absence of those phrases alone cannot prove semantic absence. This audit neither edits nor exports CM.

## 4. Other loss paths and uncommitted decisions

Git evidence: `git log -1 --format="%H %cI" master` → 557a58bc5384829b3506374d0495b2816c658fac, Oct 4; same command for origin/master → 5ccbb836abcb7d0534d6601d502f760f79bf8d85, Oct 10. `git merge-base --is-ancestor 6aa22ab5 origin/master` → rc 0: cleanup reached cached upstream. MAESTRO’s correction reports 511 commits unique to this branch and 3 unique to origin/master at its snapshot. My earlier observations were 512→514; the correction check at HEAD 8c107cdb257aca7ac943c514321304cd1f43b624 returned 516 and 3 using `git rev-list --count origin/master..HEAD` and `git rev-list --count HEAD..origin/master`. These are concurrent snapshot counts, not conflicting master identities. No fetch was performed; GitHub-now state is operator-reported, cached content is locally verified.
`git worktree list --porcelain` enumerated seven entries; `git -C <each path> status --porcelain=v1` succeeded for all, with no mutation:

| Worktree (suffix relative to M unless absolute) | Observed status before report | Decision exposure |
|---|---|---|
| M (master) | 4 untracked: .claude/worktrees/, .ignore, .promptctl/, c10l_mint_edited_qwen3b_N/ | Local main instructions stale; untracked config/model directory not automatically preserved by Git. |
| H/.local/share/openresearch/worktrees/0a1375d4-8f79-44be-bea6-2a27f6658761/chat_3cd2ad17-33c5-4752-b9e0-9259bc163220 | clean; detached c50a546a | No observed uncommitted decision. |
| Same OpenResearch parent/chat_73a1fdb0-4a98-49ce-9f9d-c16222391e61 | only .ignore untracked; detached ea36597d | Config only; no observed new ruling. |
| Same OpenResearch parent/chat_8376051e-0cc1-4c9c-94f6-eb257a489254 | only .ignore untracked; research-pass/2026-10-06 at 900aa8ed | Config only; old startup authority. |
| .claude/worktrees/backup-gdrive-r13-cand-20261011T034947Z | clean; backup-gdrive-r12 at e76db678 | No observed uncommitted decision. |
| .claude/worktrees/c10k-route-a (W) | 3 modified tracked paths; 246 untracked status entries | See exact decision-bearing paths below; counts precede this report and may change concurrently. |
| .claude/worktrees/merge-int-20261010 | clean; detached bac4fbe0 | Historical integration snapshot, not current team authority. |

W tracked changes: B/drive_intel_dedup_layout_v2.md:58,116,153 restore exclusive incoming-part creation and baseline/inertness requirements; results/drive_activation_intel_20261012/activation_plan_intel_v1.md:120–136,180–189 holds new Intel coverage/configuration safeguards; tools/test_dashboard_mathlab.py has 135 insertions/2 deletions (`git diff --stat`). The first two hold reviewed-design repair decisions; the test file is parallel work, not this sweep’s change. This sweep neither committed nor altered those paths; another session may commit them after the recorded status snapshot.
W untracked decision-bearing material: A/hygiene/PLAN.md, LANES.md, host_apply.md and 33 briefs are an in-flight preservation plan; results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/context_checkpoint.md:58,60 still carries the historical ~20% handoff; design_review.md and before/mb12_before/mb15_scope_* snapshots preserve past scope/review decisions. results/labviz_codex_brief.md and implementation reports are untracked older task contracts. These are at risk of omission from a fresh checkout, not evidence they were deleted.
**Handoff/queue routing risk, not erased decisions:** “review report before questions” survives HF/maestro47_takeover_20261011.md:8 AND PS’s 14:12Z historical note; the active needs_from_you still prompts choices with blocked_by=[]. The later hygiene-only hold survives PS:50 while other items advertise ready/running. These conditions reached durable files; their current display/enforcement is weaker than their historical prose. No erased, uniquely chat-only operator ruling was established.
**A live propagation regression:** PS:50 still says “master has had no merge since Oct 4,” contradicted by corrected A/ROOT_CAUSE.md:8 and cached origin/master. S3/context-hygiene-must-reach-every-store.md:11 says compare origin/master, but its merge timestamp/count also lag current receipts. Correct source facts did not automatically update queue/index summaries.
**Preservation mechanisms do not cover every store:** S1/memory-paths-and-mirror-discipline.md:8–16 describes two stores; tools/closeout_check.py:252–276 defaults to S2 and treats memory issues as WARN, while sampled Claude attachments selected S3 (A/SYNTHESIS.md:23,40). .codex/hooks.json:4–10 still names absent /workspace scripts. H/.claude/settings.json:78,89 emits graft instructions despite CLAUDE.md:16. GA:141 unconditional context-save can violate a one-file brief. These are static reader/enforcement defects, not tested live hook failures.
No sync, cleanup, host test, runtime proof or corrective write was authorized here. At MAESTRO’s 45% message or any compaction: stop new work, preserve done/in-flight/remaining paths and this rule in A/cps_handoff.md, reply CPS HANDOFF; start new work only at ≥60%, successor by ≤40%. No such message/compaction occurred during this sweep.

## 5. Plain summary

The missing and conflicting instructions added work to R2, but the evidence does not show they caused its central shared-drive problem. The research records and Oct 10 cleanup survived; the main checkout, newer rule copies and recall routes diverged. Twelve recent lessons exist only in Claude’s active memory bank, and 68 files exist only in Git memory, including deliberately retired notes. The immediate risks are stale run permissions, late handoffs, wrong review roles and missing build/activation holds; some repairs are still uncommitted parallel work. This report preserves the evidence and changes no rules or permissions.


## 6. Origin of the exact-match rule (follow-up)

- Earlier safety need: a surviving science child could outlive its reservation; incomplete ownership could hide helpers. R2 required transfer ownership including descendants, and R2C explicitly carried registration-before-release from those reviews (results/research_engine_phase1_20261011/astra_spec_r4_verdict.md:28; results/research_engine_phase1_20261011/astra_spec_r5_verdict.md:35–49; B/astra_r1_verdict.md:24; B/r2c_report.md:6).
- First R2 contract source: v1 required enumeration, exact executable/argument identities and independent whole-population accounting; A16 required observed and accounted populations to agree. These are process/closure obligations, not root-time recipe registration (B/shared_disk_clearance_contract_v1.md:113–117,146; retained at B/shared_disk_clearance_contract_v1_1.md:87–89,115–117).
- First literal exact-profile comparison in the implementation lineage: freeze v1 selected a suspended-spawn broker, full-population ledger comparison and executable/argv exact equality against reviewed role profiles; D3 later cited the inherited v4 comparison (B/shared_disk_clearance_freeze_v1.md:129–132; B/shared_disk_clearance_freeze_v4.md:242; B/r2_round7_decisions.md:31).
- D3's science recipe rule was MAESTRO52's selection, responding to Astra R4's missing transitive Git children and pre-execution registration problem: declare every descendant recipe at root admission, then match observed children exactly while preserving unchanged science spawns (B/astra_r2i_verdict.md:34–46,85; B/r2_round7_decisions.md:26–34).
- Actual builder/reviewer inputs propagated that choice: the builder was ordered to treat D3 as binding; the review packet asked whether it satisfied the contract. Astra rejected it because recipes lack future PID/start/parent identities and later matching cannot prevent an already executed child (B/codexr2q_brief.txt:6–7,16; B/astra_r2j_packet.md:13,26; B/astra_r2j_verdict.md:7–13).
- Later A1, explicitly approved by the operator, relaxed only science-descendant pre-release identity registration; it retained advance recipe declaration, exact matching, uncertainty keeping exclusion, whole-population accounting and full registration for roots/non-science helpers. It is an amendment, not the origin (B/r2_round8_decisions.md:9–19,23).
- Stale/over-broad GPU-note causation: **unproved**. The note concerns pending-stage compute admission/exemptions; the documented inputs instead trace to closure findings, the live contract and D3. The breadth is explicit in C9/D3, but those sources do not establish that exact recipes were the only possible safety mechanism (S1/gpu-gate-refuses-any-venv-python.md:10–12; B/r2c_report.md:6; B/codexr2q_brief.txt:4–7,16; B/shared_disk_clearance_contract_v1_1.md:119).
- M3 copy source folder: **not frozen in the examined record**; the freeze requires exact paths in a unit profile but does not select bare main, this worktree or the whole volume. The settled access-path audit remains the reference (B/shared_disk_clearance_freeze_v11.md:37; A/operator_hypothesis_worktree_vs_main.md:10).
The team chose a drive-safety rule that it could not prove covered every helper program; an old GPU note is not a proven cause (B/r2_round7_decisions.md:28–31; B/r2_sweep_report.md:72–80; B/codexr2q_brief.txt:6–7,16).

Lines: 250
