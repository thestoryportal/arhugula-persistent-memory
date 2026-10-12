# CAB — Codex context layer audit, 2026-10-12 UTC

Read-only audit for MAESTRO. Only this report was written. No science, project Python, network, model launch, Git mutation, backup, tmux mutation, credential use or context-save workflow was run. Static configuration is not proof of MCP startup, authentication or hook enforcement.

G = /Users/robertrhu/.codex. M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory (main checkout). Unprefixed paths identify the assigned worktree. Global AGENTS is actually 145 lines, versus the brief's 144; worktree AGENTS is 162 and main AGENTS 145. Bytes are UTF-8 source-span sizes including line endings; they are not necessarily removal savings.

Evidence receipts:

- C1: pwd; git rev-parse --show-toplevel; git branch --show-current returned the assigned worktree and worktree-c10k-route-a. git -C /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory branch --show-current returned master.
- C2: /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B - probes used Path(path).exists(), is_symlink(), resolve(), os.environ.get("LLMDB_ROOT") and shutil.which(). /workspace is absent. LLMDB_ROOT names M. hf_cache and covariance_caches are symlinks into memit; project Python resolves to cpython-3.11.16. CORPUS numbered glob has 62 files, 00–61. /opt/homebrew/bin/node resolves to Cellar/node/26.8.2/bin/node, and /opt/homebrew/bin/npx exists. setsid does not resolve. Legacy paths and project trust paths were individually checked below.
- C3: Same read-only Python runner extracted G/config.toml:133 PATH and called shutil.which("npx", path=rawpath) and shutil.which("node", path=rawpath): both None. PATH omits /opt/homebrew/bin. Duplicates: RTK shim x2, libpq x2, user bin x2, local bin x2, volta x3, /usr/local/sbin x2. First-occurrence-preserving deduplication savings are computed below; executable resolution is the functional issue.
- C4: /opt/homebrew/bin/rtk proxy diff -u M/AGENTS.md AGENTS.md returned 1, expected differences. Python difflib.SequenceMatcher(..., autojunk=False) found all 18 edit blocks, listed below. No synchronization performed.
- C5: Read G/models_cache.json and extracted only slugs/efforts: gpt-6-astra, gpt-6.1-sol, gpt-5.6-sol and gpt-5.5 all listed. First three allow high/max/ultra; gpt-5.5 high/xhigh. Cached availability is not live account verification; older does not mean invalid.
- C6: git log -4 --oneline -- AGENTS.md .codex/config.toml CORPUS/AGENTS.md experiments/AGENTS.md returned 2b31a5fe, b19e4377, f69a9a5f, 6cbb10cf. Prior README.md, APPLIED.md and astra_review.md in results/memory_audit_20261010/ were read.

## Passage findings

| item (file:line-range or note filename) | bytes | verdict(s) | evidence (file:line or command) | proposed action | replacement text (only when item should stay, at most 200 characters) |
|---|---:|---|---|---|---|
| G/AGENTS.md:1-1 | 32 | KEEP | G/RTK.md exists, 482 bytes; /opt/homebrew/bin/rtk exists (C2). | keep | |
| G/AGENTS.md:3-24 | 1904 | KEEP | AGENTS.md:14 and CLAUDE.md:15 agree on scoped action, grounded recommendations and scarce operator questions. | keep | |
| G/AGENTS.md:26-54 | 1143 | KEEP | Simplicity/surgical-change conventions agree with AGENTS.md:14-15 preserving neighboring work. | keep | |
| G/AGENTS.md:56-63 | 1182 | KEEP | Distinct type/effect conventions; one authority agrees with DISCIPLINE.md:48. | keep | |
| G/AGENTS.md:64-64 | 299 | AMBIGUOUS | Quote: mechanics needing “if / when / skip / only” implies leaked variability. Reading A: simplify pure logic; B: remove safety guards. CLAUDE.md:15,30,38 requires conditional authority/admission/HALT. | fix-text (limit heuristic to pure domain logic) | Prefer data-driven pure logic; preserve explicit permission, admission, validation and HALT guards at effect boundaries. |
| G/AGENTS.md:66-66 | 155 | BLOAT | G/AGENTS.md:66 says an inline tagging discipline is intentionally not adopted; no current rule results. Entire measured span can be cut. | retire | |
| G/AGENTS.md:68-85 | 1266 | KEEP | AGENTS.md:13-16,103 and CLAUDE.md:26 require test-first evidence, independent review and handoff readiness. | keep | |
| G/AGENTS.md:87-95 | 2176 | KEEP | CLAUDE.md:30-40 and AGENTS.md:15,100 require empirical evidence and explicit failures. Positive controls/cache clearing remain subject to authorized scope at AGENTS.md:14. | keep | |
| G/AGENTS.md:97-99 | 233 | AMBIGUOUS | G/AGENTS.md:99 names Read/Glob/Grep/Explore, absent as named tools in the current harness tool schema; exec_command/collaboration are available. Reading A: any reader; B: wait for nonexistent names. | fix-text (name capabilities) | After a denial, use permitted read-only capabilities; report the restriction and avoid repeating the denied action. |
| G/AGENTS.md:101-109 | 784 | NONFACTUAL | :103 says no conversation carries over. Current collaboration.spawn_agent schema defaults fork_turns to all; none suppresses inheritance. :108 artifact verification remains sound. | fix-text (make inheritance host-dependent) | Inheritance depends on fork_turns and the host. Include scope and acceptance criteria explicitly; verify the produced artifact yourself. |
| G/AGENTS.md:111-113 | 321 | KEEP | C1 verifies both checkouts; CLAUDE.md:52 requires isolated integration worktree. | keep | |
| G/AGENTS.md:115-117 | 483 | AMBIGUOUS | “not ... more than the current CI branch” and “gh-down CI parity” lack scope/definition. Reading A: one active candidate; B: delete other branches. AGENTS.md:14,17 forbids builder deletion/merge. | fix-text (retain exact-head green CI; remove undefined policy) | Require green CI for the exact candidate head. Preserve other branches; follow repo merge-gate and role-specific mutation authority. |
| G/AGENTS.md:119-125 | 581 | KEEP | PEP668/fallback dependency advice and deterministic edits agree with AGENTS.md:71 and CLAUDE.md:62; no dependency action was authorized in CAB. | keep | |
| G/AGENTS.md:127-129 | 503 | KEEP | :129 distinguishes concise narration from full deliverables; matches audit evidence requirements. | keep | |
| G/AGENTS.md:131-133 | 503 | AMBIGUOUS | “MEMORY.md” could mean project/live index or every registry with that basename. DISCIPLINE.md:52 names memory_mirror; current harness memory policy forbids direct edits to G/memories. | fix-text (name memory system and write authority) | Apply the 24,400-byte cap to the project index and its live mirror. Follow each memory system's write authority; do not trim unrelated registries. |
| G/AGENTS.md:135-137 | 292 | AMBIGUOUS | “Save ... into context ... before proceeding” could mean authorized report or mandatory memory mutation. AGENTS.md:14 and CAB brief allow only this report. | fix-text (scope recording) | Record useful learnings in the authorized task artifact. Update durable memory only when task scope and memory policy authorize it. |
| G/AGENTS.md:139-141 | 146 | CONFLICT | Mandatory context-save conflicts with AGENTS.md:14 and one-file CAB scope. Installed context-save SKILL.md:26-29 mutates session files; :250-284 can change/commit CLAUDE.md. | fix-text (honor authorized destination) | At completion/context gates, preserve a handoff in the authorized destination; run context-save only within the task's permitted write scope. |
| G/AGENTS.md:143-145 | 267 | KEEP | Summary of :18,43-54,85; no competing operational threshold. | keep | |
| AGENTS.md:1-3 | 564 | KEEP | CLAUDE.md:10-14 and DISCIPLINE.md:106-109 confirm shared authority and Codex-specific adaptation. | keep | |
| AGENTS.md:5-9 | 857 | STALE | :7 uses 60%/40%; CLAUDE.md:18 repeats it. memory_mirror/context-management-every-session.md:22 adds 45% early-stop with long steps pending; current CAB brief requires stop on MAESTRO's 45% message. | fix-text (carry current stop margin) | New work only at >=60% left. Stop/write handoff at <=45%; successor by <=40% or after compaction. MAESTRO monitors sessions lacking a visible meter. |
| AGENTS.md:11-17 | 1630 | KEEP | CLAUDE.md:16-17,52 agrees on Astra, RED/GREEN, scoped edits, no builder Git/PR mutation and exact completion tokens. | keep | |
| AGENTS.md:19-19 | 2302 | DUPLICATE | Identical full cooperative paragraph at CLAUDE.md:54; origin results/git_automation_fix3_mb13_20261010T092614.133488Z/build_report.md:23. Preserve all obligations. | merge-into CLAUDE.md:50-54 (retain prohibition and mandatory read pointer) | Builders never push, merge or mutate PRs/CI. MAESTRO alone merges through the gate; read CLAUDE.md Merging and its full cooperative rule before gate work. |
| AGENTS.md:21-21 | 247 | KEEP | C2 env points at main; closeout_check.py:25, render_state.py:16, engine_fingerprint.py:31 prefer env; git_hooks/pre-commit:12-13 invokes the first two. | keep | |
| AGENTS.md:23-24 | 671 | KEEP | DISCIPLINE.md:7-22,59-92 defines goal/protocol; :106-109 binds both hosts. | keep | |
| AGENTS.md:27-40 | 914 | DUPLICATE | Contract/mechanism distinction overlaps DISCIPLINE.md:82-92; fallback prohibition at :13-20. Safety distinction stays. | merge-into DISCIPLINE.md (retain Codex pointer) | Skills specify gates, not independent evidence. Honor DISCIPLINE.md: side-store mitigation cannot close an unaccepted in-weight F1 requirement. |
| AGENTS.md:42-43 | 314 | KEEP | CLAUDE.md:3 and governing spec pointer agree on concise program identity. | keep | |
| AGENTS.md:45-53 | 963 | CONFLICT | “Read first (in this order)” omits bootstrap/e2e map; DISCIPLINE.md:29-30 orders those and CLAUDE.md:12-14 requires them. | merge-into DISCIPLINE.md:24-44 | Follow DISCIPLINE.md read triggers, including bootstrap and the full end-to-end map before experiment, hypothesis or decision work. |
| AGENTS.md:55-67 | 894 | MISLEADING | C2: external_prior_art/larql, external_prior_art/BetaEdit, llama_cpp_src, b3_edited_qwen3b and b3_q4km.vindex absent. Map presents them as infrastructure; :46 names README repo-map home. | merge-into README.md (label historical/optional assets there) | Use README.md for the current repository map. Verify optional or recovered infrastructure paths before relying on them. |
| AGENTS.md:69-70 | 368 | KEEP | EXPERIMENT_RUNBOOK.md:91 explicitly names M3/48GB/MPS and deployment target; R2 adoption:11 activates nothing. | keep | |
| AGENTS.md:71-71 | 350 | KEEP | pyvenv.cfg gives 3.11; .venv/lib/python3.11/site-packages/torch-2.8.0.dist-info/METADATA:3 and transformers-4.51.0.dist-info/METADATA:3 confirm pins. No project Python executed. | keep | |
| AGENTS.md:72-72 | 660 | KEEP | C2 verifies symlinks, vendored engine and LLMDB_ROOT=main; :21 prevents wrong-root effects. | keep | |
| AGENTS.md:73-75 | 348 | CONFLICT | “No-GPU sanity” b3_verdict.py:80-86 opens canonical b3_quant_survival_result.json with w, forbidden at AGENTS.md:95. C2 runner loads model; neither is authorized as CAB smoke. | fix-text (replace generic smoke command) | Use REPRODUCIBILITY.md under the named science brief. Existing B3 verdict runner writes a canonical result; it is not a read-only sanity check. |
| AGENTS.md:76-76 | 537 | KEEP | CLAUDE.md:30 repeats admission restrictions; C2 finds no setsid. Launch advice remains subject to :14 scope. | keep | |
| AGENTS.md:78-82 | 894 | AMBIGUOUS | “after any structural change” can mean immediate science or scope-gated evidence. :14 requires authority; C invokes model-loading C2 and canonical-writing B3. | fix-text (preserve gates and explicit admission) | Structural edits require applicable A/B/C evidence. Run C only under admitted science authority with safe outputs; otherwise report C UNVERIFIED. |
| AGENTS.md:83-87 | 632 | KEEP | Preregistration matches CLAUDE.md:16; naming/status conventions fit actual experiments/track_c hierarchy. Nested flat-path naming is the outlier. | keep | |
| AGENTS.md:88-88 | 246 | DUPLICATE | Detailed template lives at CORPUS/AGENTS.md:11-22. | merge-into CORPUS/AGENTS.md:11-22 | Follow CORPUS/AGENTS.md for finding structure: preregistration, verdict, caveats, Decision-ID and next-step fork. |
| AGENTS.md:89-90 | 289 | KEEP | Fail-closed env agrees with :21 and CLAUDE.md:30; nested fallback must not supersede it. | keep | |
| AGENTS.md:92-96 | 1090 | KEEP | CLAUDE.md:31,34,38-40,60 preserves inertness/HALT/locked evidence. Prior astra_review.md:15-17 confirms namespacing remains caller-enforced. Intentional safety anchor. | keep | |
| AGENTS.md:97-97 | 565 | MISLEADING | Valid reserve/deletion rules omit adopted transfer authority: r2_redesign_operator_adoption.md:5,11; runbook:1254 requires v4 staging and distinct activation/protection gates. | fix-text (add adopted architecture pointer) | Keep budget +20 GiB and exact deletion approval. Use adopted R2 Git+Drive v4 host roles and transfer gates; adoption permits no activation. |
| AGENTS.md:98-100 | 646 | KEEP | CLAUDE.md:33-40,60,62 preserves frozen infra, persistence verification and evidence/inference boundary. | keep | |
| AGENTS.md:102-103 | 868 | MISLEADING | Thin closeout list omits provenance/V&V and generated-source edits at DISCIPLINE.md:49-50; CLAUDE.md:44 delegates full set there. Mechanical gate remains correct. | merge-into DISCIPLINE.md:46-55 (retain gate/rerun rule) | Follow DISCIPLINE.md §1.1 fully; closeout_check must be ALL GREEN. Compromised science needs a reviewed fix and fresh authorized rerun. |
| AGENTS.md:105-110 | 1378 | KEEP | CLAUDE.md:16 requires Astra high/no-graft; DISCIPLINE.md:82 differentiates lead families, :52 identifies memory home. | keep | |
| AGENTS.md:112-114 | 909 | DUPLICATE | CLAUDE.md:70-72 and DISCIPLINE.md:94-104 cover opt-in bounded/STAGING harness, distinct from standing delegation at CLAUDE:22. | merge-into AUTONOMY.md (retain pointer and hard boundary) | Autonomy harness is opt-in, operator-launched and STAGING-only; follow AUTONOMY.md and DISCIPLINE.md §3.1. Standing delegation is separate authority. |
| AGENTS.md:115-115 | 264 | NONFACTUAL | Says hooks enforce STAGING; .codex/hooks.json:4,6,8,10 executes absent /workspace scripts (C2). Prior APPLIED.md:200,254 left this unresolved. | fix-text (remove unsupported enforcement claim) | STAGING-only remains mandatory. Project hooks target absent /workspace paths; enforcement is unverified until paths and runtime behavior are qualified. |
| AGENTS.md:116-118 | 794 | KEEP | tools/autonomy_mission.json:2 explicitly marks c2band STALE/DONE; CLAUDE.md:72 requires re-pointing. No launch attempted. | keep | |
| AGENTS.md:120-121 | 237 | KEEP | CLAUDE.md:66 agrees that generated runbook, checkpoint and CORPUS supply current position. | keep | |
| AGENTS.md:123-130 | 792 | STALE | Node24 at :127 contradicted by C2 Node26.8.2 symlink. Perplexity configured at G/config:194-199 but npx unresolved under its PATH (C3). | move-to a research-tools runbook (retain availability/credential pointer) | Verify configured research tools and executable paths before use. Credentials stay per-user; configured does not mean operational. |
| AGENTS.md:132-133 | 387 | KEEP | memory_mirror/notebooklm-via-browser-harness.md:8,12 records failed auth on 2026-10-10 and requires rechecking after updates. Last-verified evidence, no fresh live assertion here. | keep | |
| AGENTS.md:135-140 | 1199 | AMBIGUOUS | “READY (key required)” could mean installed/configured or merely installable. Neither config has InfraNodus; DISCIPLINE.md:41 says not connected by default. Node24 also stale (C2). | move-to a research-tools runbook (retain availability pointer) | InfraNodus is optional, requiring configured MCP access and operator credentials. Verify the live tool list before relying on it. |
| AGENTS.md:141-144 | 759 | KEEP | DISCIPLINE.md:41,91 requires leads/register/falsification; runbook:91 confirms single M3 science host. Intel support is no extra local LLM science. | keep | |
| AGENTS.md:146-155 | 1272 | DUPLICATE | DISCIPLINE.md:90,92 and :62-72 specify refutation, bounded fan-out and proposer/documenter separation; :147 adds historical 130-repo example. | move-to a team-workflow runbook (retain bounds/independence pointer) | Follow DISCIPLINE.md for bounded refutation and role separation. Parallelize authorized analysis; serialize M3 science compute. |
| AGENTS.md:157-162 | 895 | KEEP | CLAUDE.md:17,52 and DISCIPLINE.md:92 agree on worktrees, MAESTRO mutations, weak same-family independence and bounded role separation. C1 confirms Git. | keep | |
| M/AGENTS.md:1-51 | 4339 | DUPLICATE, STALE | Shared passages match worktree equivalents. Exceptions: M:33 ends index at20 (CORPUS61 exists, C2); M lacks W:5-21 team/context/root-isolation insertion. | fix-text (reconcile from current authority; no blind overwrite) | Align main's Codex guide with current team/context authority; use CORPUS/README.md for the moving index. |
| M/AGENTS.md:52-54 | 799 | STALE, CONFLICT | Says 4090/CUDA/Intel/export workspace; runbook:91 and W:70-72 say M3/MPS/local. Prior astra_review.md:23-25 closed Intel-target item in W; M retains it. | fix-text (port current platform/root guidance) | Science and deployment: M3 Pro, 48 GB, MPS. Intel is support only. In worktrees use LLMDB_ROOT=$PWD and project .venv. |
| M/AGENTS.md:55-65 | 1368 | STALE, CONFLICT | Bare python/setsid/workspace vs W:74-83 macOS/root-bound interpreter; C2 workspace absent. B3 output is unsafe at b3_verdict.py:86. | fix-text (align admitted reproducibility) | Use current REPRODUCIBILITY.md under admitted scope with LLMDB_ROOT=$PWD, project .venv and safe output paths. |
| M/AGENTS.md:67-81 | 2600 | STALE, CONFLICT | M:72 silent fallback vs W:90; M:80 current-FUSE assertion vs CLAUDE:62 historical; lacks W:97 storage duty. Other safety rules agree and stay. | fix-text (align root, storage and FS caveat) | Require LLMDB_ROOT explicitly; retain inertness, halt and storage duties. Historical FUSE reverts justify persistence checks, not a current workspace assumption. |
| M/AGENTS.md:83-84 | 570 | CONFLICT | Completion lacks binding mechanical gate; W:103 and CLAUDE:44 require ALL GREEN/fresh rerun. | fix-text (carry canonical closeout pointer) | Follow DISCIPLINE.md §1.1; closeout_check must be ALL GREEN. Halted science requires fresh authorized rerun after a reviewed fix. |
| M/AGENTS.md:86-90 | 891 | MISLEADING | Generic advisor text omits W:106 binding Astra high/no-graft and :107 MAESTRO-brief distinction; CLAUDE:16-17 is current. | fix-text (carry review-role distinction) | MAESTRO runs Astra high at promote gates with graft disabled. Codex-led work uses Claude advisory review; helper review cannot replace Astra. |
| M/AGENTS.md:92-98 | 1712 | STALE | M:96 says currently c2band; tools/autonomy_mission.json:2 says stale/done, W:116 warns. M:93 omits standing-delegation distinction at CLAUDE:22,72. | fix-text (align harness/mission boundary) | Harness is opt-in and STAGING-only, separate from standing delegation. Re-point its stale mission to an approved live falsifier before launch. |
| M/AGENTS.md:100-101 | 475 | STALE | Hand-copies B3/E3/band next choices; W:121 removed them; CORPUS21 exists (C2), and CLAUDE:66 prohibits copied state. | fix-text (retain only authority pointers) | Current work comes from runbook §0.3, checkpoint and hypothesis register; do not duplicate next-action state here. |
| M/AGENTS.md:103-124 | 3269 | STALE | M:104 pod setup vs lost-pod runbook:91. M:112-115 CLI/cookie instructions vs W:132-133 and notebooklm-via-browser-harness.md:8-12 signed-in-browser/no-cookie rule. | fix-text (replace historical tool setup) | Use the research-tools runbook and verify availability. NotebookLM uses the already signed-in browser; do not extract credentials or cookies. |
| M/AGENTS.md:125-137 | 1550 | STALE, DUPLICATE | M:126 single4090 vs W:144/runbook:91 M3. Remaining fan-out examples duplicate DISCIPLINE:92. | move-to a team-workflow runbook (retain current compute anchor) | Parallel analysis, serialized M3 science compute; Intel support has no local LLM execution authority. |
| M/AGENTS.md:139-139 | 426 | NONFACTUAL | Says not Git-initialized/run git init. C1 main branch is master; W:157 correctly names worktrees and MAESTRO authority. | fix-text (remove git-init instruction) | Repo is Git-initialized. Use authorized isolated worktrees; MAESTRO alone commits, pushes and merges through the gate. |
| M/AGENTS.md:141-145 | 505 | DUPLICATE | M:143 repeats M:126 serialization; W removed it. Independence/bounds/roles remain W:160-162 and DISCIPLINE:92. | merge-into DISCIPLINE.md:92 (retain Codex pointer) | Honor bounded refutation, proposer/documenter separation and serialized M3 science compute in DISCIPLINE.md. |
| CORPUS/AGENTS.md:1-3 | 222 | KEEP | CLAUDE.md:12,66 identifies evidence authority; append-only at AGENTS:95. | keep | |
| CORPUS/AGENTS.md:5-6 | 128 | STALE | “currently through20” contradicted by CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md:1 and C2 numbered enumeration. | fix-text (remove moving number; retain next-number rule) | New findings use the next unused number. Consult CORPUS/README.md; never renumber or rewrite locked findings. |
| CORPUS/AGENTS.md:7-9 | 666 | KEEP | CLAUDE:26,31,66 and AGENTS:95,100 preserve reversal accounting/caveats/provenance. | keep | |
| CORPUS/AGENTS.md:11-22 | 624 | KEEP | AGENTS:88 delegates template here; fixed14-20 examples are examples, not current frontier claims. | keep | |
| CORPUS/AGENTS.md:24-29 | 529 | CONFLICT | :27 directs updating runbook §0.3 without generated JSON; CLAUDE:11 forbids edits in generated markers. DISCIPLINE:49-50 supplies missing trackers/gate. Relative docs/MEMORY paths unclear. | merge-into DISCIPLINE.md:46-55 | Follow DISCIPLINE.md §1.1 fully. Edit docs/program_state.json for generated state, then require ALL GREEN from closeout_check. |
| CORPUS/AGENTS.md:30-30 | 137 | STALE | Current network-FS assertion vs CLAUDE:62 pod history/local recurrence UNVERIFIED. Persistence check stays. | fix-text (historical attribution) | Write large canonical docs via shell/Python; verify after an intervening operation. Known reverts occurred on the lost RunPod FUSE volume. |
| CORPUS/AGENTS.md:32-33 | 389 | STALE | Index ends C2/20; C2 finds21-61. :33 itself names README as read-order home. | merge-into CORPUS/README.md | Use CORPUS/README.md for the evidence index and COUNCIL_PROTOCOL.md for review rules. |
| experiments/AGENTS.md:1-6 | 654 | MISLEADING | Track map ends track_c at c2/c2b, omitting current C10 recorded in CORPUS61; :3 declares local specificity, magnifying later stale overrides. | merge-into README.md (retain scoped-rule anchor) | Apply scoped experiment rules with root guardrails; use README.md and registry for the current track map. |
| experiments/AGENTS.md:8-9 | 194 | CONFLICT | Export workspace vs root AGENTS:21,72 and CLAUDE:30; C2 workspace absent. | fix-text (bind worktree) | Run from the authorized root with LLMDB_ROOT=$PWD; use project .venv for admitted project work. |
| experiments/AGENTS.md:10-11 | 451 | KEEP | C2 verifies configs directories/probe file. Prior astra_review.md:15-17 confirms caller-enforced RESULT_TAG. | keep | |
| experiments/AGENTS.md:12-12 | 109 | STALE | setsid/bare Python vs AGENTS:76 macOS nohup/project interpreter; C2 setsid unresolved. | fix-text (platform/scoped launch) | Authorized detached macOS work uses nohup, project .venv, LLMDB_ROOT=$PWD and namespaced output; respect admission and disk budget. |
| experiments/AGENTS.md:14-15 | 279 | CONFLICT | Says advisor -> Codex subagent/review; AGENTS:106-107 and CLAUDE:16 distinguish binding Astra from Codex-led Claude advisor. | fix-text (current independent-review route) | Pre-register before coding/running. Codex-led criteria use Claude advice; MAESTRO supplies binding Astra-high promote review. Helpers cannot substitute. |
| experiments/AGENTS.md:16-16 | 233 | CONFLICT | Silent workspace fallback vs root AGENTS:90 required env and :21 isolation. | fix-text (explicit root) | Use os.environ["LLMDB_ROOT"] with LLMDB_ROOT=$PWD; derive engine and HF paths from that explicit root. |
| experiments/AGENTS.md:17-17 | 124 | CONFLICT | Flat experiments/<track><n> conflicts root AGENTS:86 hierarchy and experiments/track_c/c2_key_collinearity.py. | fix-text (correct hierarchy) | Name runners experiments/<track>/<track><n>_<slug>.py; namespace result/log paths and verify destinations before dispatch. |
| experiments/AGENTS.md:18-18 | 170 | AMBIGUOUS | Hardcoded delta<0.05 could mean universal tolerance or example. CLAUDE:31 binds specified checks; runbook:89 records INERT with locality delta0.23. | fix-text (frozen metric-specific criteria) | Run LAW#5 against frozen metric-specific inertness criteria before trusting science; unmet criteria mean HALT. |
| experiments/AGENTS.md:19-19 | 181 | AMBIGUOUS | “If ... must patch” could authorize engine edit or mean halted proposal; CLAUDE:34/root AGENTS:93 says unmodified, :14 restricts edits to brief. | fix-text (require exception authority) | Engine stays unmodified on the science path. Report any proposed exception for explicit authority; isolate it and prove LAW#5 before promotion. |
| experiments/AGENTS.md:21-24 | 253 | KEEP | Root AGENTS:95,98 agrees on archive freeze/output protection/no hardcoding; :24 internally conflicts with :9,16, addressed above. | keep | |
| G/config.toml:1-6 | 141 | KEEP | Astra/high matches CLAUDE:16; approval preference does not override current managed never-approval policy. Builders need explicit role selection. | keep | |
| G/config.toml:7-7 | 249 | KEEP | C2 notification binary and voice-notify.sh exist. No notification sent or inferred authority to message others. | keep | |
| G/config.toml:9-55 | 1008 | AMBIGUOUS | lean/full selects valid gpt-5.6-sol (C5); program builders gpt-6.1-sol/max at model-and-compute-allocation.md:12. Personal profile intent/frequency unknown. | operator-decision (retain intentional personal profiles or add program-role profiles) | |
| G/config.toml:57-62 | 159 | STALE | C2 story-portal exists, seo-growth-engine absent. Dormant trust entry is not runtime-action proof. | operator-decision (retire absent-project trust if no longer needed) | |
| G/config.toml:63-64 | 39 | AMBIGUOUS | Root / trust intent/inheritance not demonstrated; narrow entries at :78-85 exist. Scope still constrained by AGENTS:14. | operator-decision (confirm purpose and effective scope of root trust) | |
| G/config.toml:66-85 | 583 | STALE | C2 indydevdan-harness-research and agent-deployment-framework absent; arhugula/marimo/arhugula-v2/home/main exist. | operator-decision (retire only confirmed obsolete trust entries) | |
| G/config.toml:87-130 | 841 | KEEP | Explicit plugin switches and profile overrides :26-55 explain differing catalogs; not credential/activation evidence. Catalogs visible in current harness. | keep | |
| G/config.toml:132-138 | 1386 | MISLEADING | PATH excludes installed Homebrew node/npx; command resolution fails (C3), Perplexity uses bare npx at :195. Exact repeated PATH entries are redundant. | fix-text (repair resolution and exact duplicates) | Include /opt/homebrew/bin in intended MCP/shell PATH; deduplicate exact repeats preserving order, then verify command resolution. |
| G/config.toml:139-147 | 437 | KEEP | :140 includes context-remaining/context-used. NUX counters are UI history; model slugs valid in cache (C5), not role authority. | keep | |
| G/config.toml:149-158 | 369 | KEEP | Marketplace locations are parsed loader state, not prompt prose. No operational-freshness claim or proposed deletion from dates alone. | keep | |
| G/config.toml:159-166 | 159 | KEEP | Hooks/memories switches express intent; actual managed capabilities/authority govern this session, not inferred enforcement. | keep | |
| G/config.toml:168-185 | 1161 | UNREACHABLE | C2 /Applications/Codex.app and user-Applications variant absent; configured node_repl binary/module paths therefore absent. This does not prove all managed browser backends unavailable. | fix-text (resolve installed runtime through managed setup) | Reconcile node_repl paths with installed runtime and verify startup; retain browser preferences with a working backend. |
| G/config.toml:186-189 | 175 | KEEP | C2 Pencil MCP binary exists. Startup/auth not exercised; static path evidence only. | keep | |
| G/config.toml:190-192 | 53 | CONFLICT | Global graft MCP lacks enabled=false; root AGENTS:106 and CLAUDE:16 require disabled graft. Exact review command supplies override; naked/profile launches do not. | fix-text (explicit program-role disable/override) | Program launches must disable graft explicitly. Binding review already passes mcp_servers.graft.enabled=false; do not rely on personal defaults. |
| G/config.toml:194-199 | 191 | MISLEADING | Bare npx at :195 unresolved under configured PATH (C3), despite installed binary (C2). Key name at :199 only; value never copied. Startup untested. | fix-text (repair command resolution; retain per-user credential) | Use a resolvable npx command; verify authorized MCP startup. Keep PERPLEXITY_API_KEY per-user and do not duplicate credential material. |
| G/config.toml:201-283 | 4588 | KEEP | Migration notices/trusted hook hashes are machine-owned state. arhugula-v2 trust records do not prove worktree hooks execute; project keys differ at P:32-42. | keep | |
| G/config.toml:284-292 | 216 | KEEP | Desktop settings/disabled Figma are explicit preferences; no required-capability contradiction found. | keep | |
| .codex/config.toml:1-3 | 165 | AMBIGUOUS | .codex/config.toml:2 fallback names could be misread as concatenation of AGENTS/DISCIPLINE/CLAUDE; all exist. Cap permits current root/nested docs; runtime discovery not traced. | fix-text (clarify fallback versus mandatory reads) | Fallback names select alternate project guidance, not all listed files. AGENTS.md separately requires reading DISCIPLINE.md. |
| .codex/config.toml:6-10 | 337 | STALE, CONFLICT | Project gpt-5.5/default claim vs CLAUDE:16 explicitly replacing it with Astra/high; builders gpt-6.1-sol/max at allocation note:12. G:2 Astra default can be masked by trusted project default absent explicit model. | operator-decision (remove obsolete override or define intentional role profiles) | |
| .codex/config.toml:11-15 | 86 | KEEP | Personality/approval/hooks switches are intended settings, not runtime hook acceptance or managed-policy overrides. | keep | |
| .codex/config.toml:17-21 | 307 | STALE, UNREACHABLE | Workspace trust/launch/bashrc comments conflict C1 local worktree and C2 workspace absent. G:84-85 trusts current main. | fix-text (replace pod-root launch/trust instructions) | Launch from the authorized local repo/worktree. Trust current project roots explicitly; /workspace is a lost pod-era path. |
| .codex/config.toml:23-28 | 419 | KEEP | :24 includes context-remaining. gpt-5.5 NUX is UI history, distinct from stale selection at :9. | keep | |
| .codex/config.toml:30-42 | 621 | STALE, UNREACHABLE | Four trust keys refer absent workspace hooks; .codex/hooks.json:4-10 also names absent scripts (C2). Prior APPLIED:200,254 left unresolved. | fix-text (qualify current paths and regenerate trust receipts) | Requalify local project hooks and trust receipts for their actual paths. Old workspace trust records prove no present enforcement. |
| .codex/config.toml:44-53 | 668 | HISTORICAL, MISLEADING | Disabled wrapper is correct (prior README:29, C6 6cbb10cf); “give Codex Perplexity again” stale because global :194-199 already configures server/key. | fix-text (retain short retirement record) | Pod wrapper retired 2026-10-10 (6cbb10cf). Global Perplexity is configured; verify resolution/startup rather than add it again. |

## Cross-source findings

1. Main/worktree split: main:52-64,72,84,96,101,112-115,126,139 conflicts with worktree:70-90,103,106-107,116,121,132-144,157. Worktree is newer and corroborated by CLAUDE:16-18,30,44,52 and runbook:91, but still needs this report's threshold/command/nested fixes. Main lacks Team/context insertion. Do not blindly copy either version.
2. Closed-item regression in effective main guidance: prior astra_review:23-25 identified Intel deployment; C6 f69a9a5f records worktree fix and W:70 is correct. M:52 still wrong. This is cross-checkout coverage failure, not proof the worktree fix reverted. Disabled Perplexity wrapper retirement remains preserved at project config:44-49. Hook paths were outside prior applied scope (APPLIED:200,254): outstanding, not closed-item regression.
3. Nested specificity: experiments:3,9,12,15-19 can override correct root:21,71,76,86,90,93,106-107 and CLAUDE:16,30,34. CORPUS:27 conflicts generated-state handling at CLAUDE:11 and full closeout at DISCIPLINE:49-50. Preserve all safety gates while fixing specificity collisions.
4. Threshold copies: W:7, CLAUDE:18 and checkpoint:4 agree 60%/40%; context-management-every-session:22 adds 45% with long steps pending; this brief mandates 45% stop message. Reconcile explicitly across both hosts. Checkpoint:10 still says ~20% inside a dated live-handoff block, a cross-lane historical hazard.
5. Model precedence/roles: global:2-3 Astra/high; project:9-10 gpt-5.5/high. Trusted project settings can mask global absent explicit -m/--model. CLAUDE:16 and allocation note:12 explicitly select Astra/high and builder gpt-6.1-sol/max. lean/full selects valid older gpt-5.6-sol; changing intentional personal profiles needs operator choice. No runtime launch made to assert all existing sessions' effective settings.
6. Smoke-command safety: root:74,82 invokes b3_verdict.py:80-86 writing canonical output forbidden at root:95. Structural trigger root:79 conflicts scoped no-real-run authority at :14 and admission CLAUDE:30. Preserve required reproduction evidence; do not imply new execution authority.
7. Hook enforcement overclaim: root:115 says enforced, project config:32-42 and hooks.json:4-10 point at absent workspace. C2 verifies absence; hooks=true proves intent, not invocation. Requalification is required; removing safety controls is not a byte-saving proposal.
8. Full merge-contract duplication: root:19 and CLAUDE:54 identical. Keep one complete authority and Codex's prohibition/read pointer; compare every obligation before hygiene. Root:45-53 and CORPUS:24-29 should delegate to DISCIPLINE:24-55, not maintain competing routing/closeout lists. Fan-out root:146-155 repeats DISCIPLINE:92; retain independence, bounds and serialization.
9. Global save/inheritance assumptions: G/AGENTS:137,141 conflicts CAB one-file scope/root:14. Installed context-save skill:26-29,250-284 has mutations/commits; availability is not authorization. Global:103 conflicts this harness's fork_turns=all default; explicit requirements and artifact review stay mandatory.
10. Storage routing: root:97 and CLAUDE:58-61 retain valid tiers/reserve/deletion boundaries. R2 adoption record:5,11 and runbook:1254 add M3-only memit, Intel-local staging/upload and separate activation/protection gates. Add thin v4 pointer; adoption is not commissioning/transfer/deletion authority.
11. MCP availability: global:195 npx cannot resolve under global:133 PATH, despite installed Homebrew binary. Global:169 node_repl command path absent; managed backends may be independent, so do not claim all browser tools unavailable. Global graft:190-192 conflicts no-graft role policy W:106/CLAUDE:16; exact review command overrides it.

### Complete main/worktree diff inventory

All 18 C4 edit blocks follow. Unchanged passages have their worktree assessment, subject to master exceptions in the findings table.

| main range | worktree range | change |
|---|---|---|
| insertion after3 | 4-21 | Context, Team, merge rule and root-binding added. |
| 33 | 51 | Moving 00-20 index removed. |
| 52-54 | 70-72 | Platform, interpreter and current root corrected. |
| 56-58 | 74-76 | Bare Python/setsid replaced; scope/output hazard remains. |
| 61-64 | 79-82 | Reproduction commands root-bound; C admission hazard remains. |
| 72 | 90 | Silent fallback replaced by required env. |
| insertion after78 | 97 | Storage budget/reserve/deletion authority added. |
| 80 | 99 | FUSE hazard scoped as pod history/local UNVERIFIED. |
| 84 | 103 | ALL GREEN gate/fresh rerun added. |
| 87 | 106-107 | Binding Astra/no-graft and lead-family distinction added. |
| 93 | 113 | Harness distinguished from standing delegation. |
| 96 | 116 | Bundled mission explicitly stale. |
| 101 | 121 | Moving next-action narrative removed. |
| 104 | 124 | Pod tool location -> Mac. |
| 112-115 | 132-133 | NotebookLM CLI/cookies -> signed-in browser. |
| 126 | 144 | 4090 -> M3 unified-memory serialization. |
| 139 | 157 | False git-init -> existing worktree/MAESTRO authority. |
| 143 | removed | Repeated serialization removed; retained W:144. |

## Load cost

Approximate textual tokens = UTF-8 bytes/4 rounded up; not tokenizer measurements. Configs are parsed settings, not automatically concatenated prompt prose. Their derived MCP/plugin/instruction catalogs and hook-output cost remain unmeasured.

This CAB instruction packet visibly supplied global and worktree-root AGENTS content. Nested content was absent until read. Installed OpenAI Docs local reference G/skills/.system/openai-docs/references/codex-self-knowledge.md:52-54 describes nested guidance as subtree-specific and project config as trusted-repository settings; experiments:3 declares local specificity. Expected root-to-cwd discovery would select the worktree root guide and additionally the scoped guide for a cwd below CORPUS/experiments. This is an inference from the local scoped-guidance contract, not an observed startup receipt. **Exact host startup discovery was not runtime-probed**: no CLI model launch was permitted/performed. Cat does not prove automatic injection, and root sessions are not proven to reload a nested guide merely because they edit there. Until verified, explicitly include applicable scoped rules in briefs. Fallback config:2 does not mean all named files concatenate. No AGENTS.override.md found at global/root/two nested locations (C2). C1 verifies the distinct Git worktree root; discovery is expected to stop there. Do not count main's file as loaded merely because it is a physical ancestor; no such additional injection was observed in CAB.

| audited file / dependency | bytes | approximate textual tokens | loading and sessions |
|---|---:|---:|---|
| G/AGENTS.md | 12,286 | ~3,072 | Codex builder/Astra global guidance; supplied CAB packet. Claude only if explicitly read/copied. |
| AGENTS.md | 25,757 | ~6,440 | Codex builder/Astra at this worktree root; supplied CAB packet. Claude workflow references it; auto-inclusion not demonstrated. |
| M/AGENTS.md | 18,512 | ~4,628 | Codex launched in main; separate from worktree load, not additive by physical ancestry. |
| CORPUS/AGENTS.md | 2,699 | ~675 | Subtree cwd discovery or explicit scoped read/brief; root CAB read during audit. No Claude auto-load demonstrated. |
| experiments/AGENTS.md | 2,651 | ~663 | Subtree cwd discovery or explicit scoped read/brief; root CAB read during audit. No Claude auto-load demonstrated. |
| G/config.toml | 11,764 | ~2,941 | Parsed Codex global settings: 0 proven raw prompt bytes; derived context cost unknown. Claude does not parse as Codex config. |
| .codex/config.toml | 2,609 | ~653 | Trusted-project Codex settings: 0 proven raw prompt bytes; policy/profile/CLI precedence matters. No Claude raw loading. |
| G/RTK.md | 482 | ~121 | Global:1 points here; CAB read it explicitly. Automatic @ expansion unverified. |
| DISCIPLINE.md | 22,575 | ~5,644 | Explicit mandatory read via root:23-24 and CLAUDE:10 for both; added fetch cost, not proven auto-concatenation. |

Load totals, source hashes and verdict counts are computed below from the audited bytes. No hygiene applied. FORMAT is zero because these AGENTS/config files do not use memory-note frontmatter.

Global + worktree root: **38,043 bytes (~9,511 tokens)**. Global + main: 30,798 (~7,700). CORPUS adds 2,699 (~675); experiments adds 2,651 (~663), independent subtrees, not mandatory joint loading. Mandatory DISCIPLINE adds 22,575 (~5,644), giving worktree guidance 60,618 bytes (~15,155) before task/evidence/checkpoint/tool catalogs. Cap 131,072 does not request filling it; no savings claimed for lowering it alone.

C3 exact duplicate PATH-value bytes removable preserving first occurrence: 210; excludes key/quote overhead.

Snapshot SHA-256 (no credential contents reproduced):

- G/AGENTS.md: da3841a5356b280c6bb1f601acf5a1bf2402076ca43feb054659446ab4fe00a1
- AGENTS.md: d615226e1c57db676d8f8404af2082904e57a5006062f242926d398806dbe4e0
- M/AGENTS.md: 85c8aa07b4f7dee66fb16f363e785bf03f1fbcfe6a38c27230c85dfb52793c91
- CORPUS/AGENTS.md: 312877b0f8c17a38cb13c75098d1733346525a37e8544b5f0ee278bb3d6c2c42
- experiments/AGENTS.md: a76aa55838a5a79e8438eb40bf59289b91d168dfc0d5b161e8a1c495fdfec27e
- G/config.toml: e7c31e19916e2d1f82be108540a0d00ced0faa75162ed28b6cb51db739fac491
- .codex/config.toml: 5e46daf3e93627a0436a8e88132f17c1248579516acaa8133a03ea9361ec80a0

## Verdict counts

105 rows; two-verdict rows count in both labels.

| verdict | count |
|---|---:|
| KEEP | 45 |
| BLOAT | 1 |
| CONFLICT | 14 |
| DUPLICATE | 8 |
| NONFACTUAL | 3 |
| STALE | 19 |
| AMBIGUOUS | 12 |
| MISLEADING | 8 |
| HISTORICAL | 1 |
| UNREACHABLE | 3 |
| FORMAT | 0 |

No hygiene applied. Priority follow-up: align root/nested/main authority, qualify hooks, correct model/root defaults and remove unsafe implied smoke-run authority. Keep LAWs, halt, storage tiers/reserves, merge gate and operator holds intact.

Lines: 219
