# SK1 — Design → PRD/spec → plan → atomic units survey

Status: SURVEY COMPLETE; pipeline and trial PROPOSED. Read-only survey on 2026-10-11; output name follows the brief's 20261012 convention. No workflow, skill script, installation, build, review service or activation was run.

The missing link is an explicit, checked translation between artifacts, rather than another whole-document review. We already have design-to-PRD traceability and atomic-decomposition contracts, but some are nested synced assets with unresolved loader status and flattened references. Adopt those contracts through explicit reads; keep MAESTRO's verification and Astra's promote gates.

## 1. Inventory

Paths below are exact after expanding these aliases; `:N` cites 1-based source lines. Braces enumerate separate paths, not a new directory.

- C = `/Users/robertrhu/.claude/skills`; D = `/Users/robertrhu/.codex/skills`; A = `/Users/robertrhu/.agents/skills`.
- N = `/Users/robertrhu/.codex/superpowers/skills`; P = `/Users/robertrhu/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills`.
- S = `C/synced/64b41406-d159-4623-870b-4d98e20857d0_3e2ca3e4-6f17-4aae-b6ef-6c82f5b79038`.
- V = `/Users/robertrhu/Projects/arhugula-v1`; K = `/Users/robertrhu/.claude/plugins/cache/promptctl/laws/0.24.1`.
- R = this research worktree, `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`.

**Loaded? evidence keys (availability is different from invocation):**

- **D1 YES, advertised to this Codex session:** the injected `Available skills` catalog names the D/gstack, A/shared and R/advisor paths shown below. This is direct loader evidence; it does not mean their bodies have already been invoked. No explicit per-skill enable list was found in `~/.codex/config.toml`.
- **D2 YES, advertised native Superpowers:** the same live catalog names A/superpowers paths; that directory is a symlink to N. Verified discovery convention: `~/.codex/superpowers/.codex/INSTALL.md:3,18-29` describes native discovery through that symlink and restart.
- **D3 YES, advertised plugin Superpowers:** live catalog names P paths; `~/.codex/config.toml:111-112` explicitly enables `superpowers@openai-curated`. D2 and D3 coexist; they are different bytes.
- **C0 UNKNOWN in MAESTRO's runtime:** valid personal-root SKILL.md exists and was read, but this Codex session cannot see MAESTRO's injected skill catalog. `~/.claude/settings.json:110-115` lists plugins, not these individual skills; `:163` is a sandbox write allowance, **not** a loader declaration. Do not promote filesystem presence to YES.
- **C1 UNKNOWN nested synced discovery:** S contains SKILL.md files, outside Codex's advertised catalog; no active loader entry for S was found. Explicitly reading the exact skill and its resources is usable now, without claiming a native slash command exists.
- **C2 CONFIGURED; runtime UNKNOWN:** `~/.claude/settings.json:114` enables laws; `K/.claude-plugin/plugin.json:2-3` identifies laws 0.24.1. Installation also recorded in `~/.claude/plugins/installed_plugins.json:78`. No live Claude invocation was tested.
- **X NO here:** foreign project/agent, missing SKILL.md, or absent directory; the exact path/probe below supplies evidence. Manual reading can still use a foreign contract.

| Skill | Agent | Path / content evidence | Stage | Input → output artifact | Loaded? evidence | Fit to this team |
|---|---|---|---|---|---|---|
| brainstorming | both | C/brainstorming/SKILL.md:12-14,89-131; N/brainstorming/SKILL.md:96-134; P/brainstorming/SKILL.md:226-265 | design | idea/context → approved design .md | Claude UNKNOWN C0; Codex YES D2/D3 | Good boundaries; MAESTRO owns approval/commits; do not reopen settled choices. |
| office-hours | both | C/office-hours/SKILL.md:872,1654; D/gstack-office-hours/SKILL.md:3; C/gstack/office-hours/sections/design-and-handoff.md:20 | design | problem dialogue → design .md in ~/.gstack/projects | Claude UNKNOWN C0; Codex YES D1 | Product framing useful early; copy the approved artifact into git through MAESTRO. |
| prd-author | Claude | S/prd-author/SKILL.md:28-78; S/prd-author/prd-template.md:51-78 | PRD | filed design/ADRs → observable requirements, acceptance, traceability matrix | UNKNOWN C1; Codex not advertised | Best design→PRD contract; phase/V3 assumptions and reference paths require explicit adaptation. |
| prd-to-agentic-spec | Claude | C/prd-to-agentic-spec/SKILL.md:12-28,129-216,295-310 | spec | PRD → single spec .md + optional gaps .md | UNKNOWN C0; Codex not advertised | Explicit paths, dependencies and input→output validation; gaps may not authorize execution. |
| prd-to-agentic-spec-workspace | Claude | C/prd-to-agentic-spec-workspace (directory probe: iteration-1…4; no SKILL.md) | spec evaluation workspace | evaluation inputs → saved trial outputs | NO X: no skill entrypoint | Evaluation artifacts, not a second callable skill. |
| prd-to-engineering-spec | both | C/prd-to-engineering-spec/SKILL.md → A/prd-to-engineering-spec/SKILL.md:36-49,132-154,254-355 | PRD/spec/plan | complete PRD → requirements, multi-file specs, tests, task breakdown | Claude UNKNOWN C0; Codex YES D1 | Strong seven-lens completeness; heavier multi-document output and interactive choices. |
| spec-writer | Claude | S/spec-writer/SKILL.md:8-31,37-40,250-255 | spec integration | council envelopes/voices → spec artifacts, ledgers, transition delta | UNKNOWN C1; Codex not advertised | Preserves unresolved tensions; cannot invent the missing design or implementation plan. |
| framework-spec-writer | Claude | S/framework-spec-writer/SKILL.md:10-37,55-80,237-254 | spec | framework decisions → typed spec blocks/interfaces/integrated spec | UNKNOWN C1; Codex not advertised | Existing IDs are useful; /mnt/user-data and project-KB delivery are foreign to git authority. |
| validation-contract-architect | Claude | S/validation-contract-architect/SKILL.md:12-16,24-40,44-80 | design/spec validation | validation questions → proof/limits, input/output, failure/exit contracts | UNKNOWN C1; Codex not advertised | Good for difficult validation contracts; carries another harness's .larql/Warden decisions. |
| laws:application-spec | Claude | K/skills/application-spec/SKILL.md:1-25; references/craft.md:9-29 | behavioral spec | observable running application → clean-room appspec/ files | CONFIGURED C2; Codex not advertised | Appropriate for black-box reimplementation; deliberately excludes our internal file/signature design. |
| spec / gstack-spec | both | C/spec/SKILL.md:800-818,1091; D/gstack-spec/SKILL.md:1080,1897 | PRD/spec | vague intent → reviewed GitHub issue + local archive + optional spawned executor | Claude UNKNOWN C0; Codex YES D1 | Issue filing/spawn/default execution are outside builder authority; poor default here. |
| create-implementation-plan | both | C/create-implementation-plan/SKILL.md → A/create-implementation-plan/SKILL.md:10-42,44-66,85-153 | plan/atomic units | requirements → structured /plan/ Markdown, REQ/TASK IDs | Claude UNKNOWN C0; Codex YES D1 | Parallel tasks and explicit dependencies; template lacks per-unit file ownership and numbered test receipts. |
| implementation-planner | Claude | S/implementation-planner/SKILL.md:28-83,106-115; implementation-plan-template.md:60-100 | plan/atomic units | cleared spec → units, DAG, contract coverage, integration units | UNKNOWN C1; Codex not advertised | Strongest decomposition law; logical filenames must become exact paths before dispatch. |
| writing-plans | both | C/writing-plans/SKILL.md:36-52,79-125; N/writing-plans/SKILL.md:38-43,98-120; P/writing-plans/SKILL.md:34-50,92-175 | plan/atomic briefs | bounded spec → tasks with files, interfaces, failing tests, commands | Claude UNKNOWN C0; Codex YES D2/D3 | P is leaner and includes review focus; replace worker commit and execution-choice defaults. |
| scout (skill) | Claude | V/.claude/skills/scout/SKILL.md:33-80 | atomic units | spec → JSON units, artifacts, dependencies, risk, critical path | NO here X: V project scope, not R; global C/scout absent | Real downstream decomposition contract found; session-sized criterion exceeds our ~8-minute target. |
| architect (agent, not skill) | Claude | V/.claude/agents/architect.md:2-24,28-43,54-80 | plan | scout JSON + spec/pattern source → read-only textual implementation plan | NO here X: V project scope; R/.claude/agents absent | Exact paths/tests and parallel groups; MAESTRO must persist text and replace foreign source snapshots. |
| project-workflow-analysis-blueprint-generator | both | C/project-workflow-analysis-blueprint-generator/SKILL.md → A/project-workflow-analysis-blueprint-generator/SKILL.md:36-80,223-293 | design/context analysis | existing code flows → workflow descriptions/implementation templates | Claude UNKNOWN C0; Codex YES D1 | Documents existing patterns; not a requirements or dispatch authority. |
| icm-workspace | Claude | C/icm-workspace/SKILL.md:19-53,55-72,85-127 | execution/context routing | genuine ICM stage contracts → staged workspace/lint report | UNKNOWN C0; Codex not advertised | Useful scoped-input idea; explicitly forbids converting ordinary repo governance into ICM. |
| icm-workspace-workspace | Claude | C/icm-workspace-workspace (directory probe: no SKILL.md) | skill evaluation | evaluation cases → evaluation workspace | NO X: no entrypoint | Not a pipeline skill. |
| dispatching-parallel-agents | Codex | N/dispatching-parallel-agents/SKILL.md:10-14,49-79; P/dispatching-parallel-agents/SKILL.md:49-77 | dispatch | independent problems + constrained prompts → parallel returns + integration | YES D2/D3; C entrypoint absent | Closest dispatch contract; MAESTRO applies it to tmux units with disjoint files and resource limits. |
| subagent-driven-development | Codex | N/subagent-driven-development/SKILL.md; P/subagent-driven-development/SKILL.md:188,273-284,337 | execution/review | plan → task implementer/reviewer loop and branch review | YES D2/D3; C entrypoint absent | P forbids parallel implementers, assumes commits and discourages reviewer test reruns; unsuitable unchanged. |
| executing-plans | Codex | N/executing-plans/SKILL.md:18-37,65-70; P/executing-plans/SKILL.md | execution | plan → executed tasks, verification, finishing handoff | YES D2/D3; C entrypoint absent | Execute one authorized brief only; suppress all-plan scope and branch-finishing chain. |
| autoplan | both | C/autoplan/SKILL.md:5,28; D/gstack-autoplan/SKILL.md:893-913,957,1628-1690 | review/plan aggregation | plan → CEO→design→eng→DX findings, decisions, aggregated tasks | Claude UNKNOWN C0; Codex YES D1 | Auto-decisions, four reviews and external artifacts are costly; cannot decide operator-only forks or replace Astra. |
| plan-eng-review | both | C/plan-eng-review/SKILL.md:808,1050; C/gstack/plan-eng-review/sections/review-sections.md:558-585; D/gstack-plan-eng-review/SKILL.md:1377-1445 | plan review | plan → architecture/test/failure review + implementation task Markdown/JSONL | Claude UNKNOWN C0; Codex YES D1 | Best gstack review for this team; JSONL tasks still need acceptance/file/context fields. |
| plan-ceo-review | both | C/plan-ceo-review/SKILL.md:869-876; D/gstack-plan-ceo-review/SKILL.md:831-838 | design/plan review | plan → scope/strategy decisions and reviewed plan | Claude UNKNOWN C0; Codex YES D1 | HOLD SCOPE fits; expansion modes must not amend frozen research authority. |
| plan-design-review | both | C/plan-design-review/SKILL.md:841,1138-1159,1479; D/gstack-plan-design-review/SKILL.md:830,1120-1141,1547 | design review | UI plan → scored dimensions, revised plan, implementation tasks | Claude UNKNOWN C0; Codex YES D1 | Useful for LabViz later; default mockups cannot override its drawing/build hold. |
| plan-devex-review | both | C/plan-devex-review/SKILL.md:847-882; D/gstack-plan-devex-review/SKILL.md:832-887 | design/plan review | developer journeys → DX findings and revised plan/tasks | Claude UNKNOWN C0; Codex YES D1 | Target onboarding/operator friction only; avoid unrelated competitive research. |
| lane-integrator | Claude | S/lane-integrator/SKILL.md:16-31,54-80,83-99,144-165 | integration/review | research lane returns → packet + structured research record | UNKNOWN C1; Codex not advertised | Legal-research role, not code merge integration; retain the lesson that stop states cannot become success. |
| advisor-review | Codex | R/.codex/skills/advisor-review/SKILL.md:3-8,55-70 | review | evidence packet → adversarial verdict + prioritized issues | YES D1; R/.claude/skills absent | Use evidence/independence contract; MAESTRO's binding reviewer remains Astra, not the Codex-led Claude default. |
| voice-discussion, voice-gates, voice-off, voice-status (prompts) | Codex | /Users/robertrhu/.codex/prompts/voice-{discussion,gates,off,status}.md:1-4 | communication only | invocation → voice-mode shell command | UNKNOWN: files exist; no prompt loader proof in config or live skill catalog | No design, planning or atomic-unit behavior. Do not run them for this survey. |

**Search completeness and location findings:** R/.claude/skills and R/.claude/agents are absent; R/.codex/skills contains advisor-review. The six requested “anthropic-skills” names are all present at S; a directory literally named `anthropic-skills` was not found in the scanned home/memit trees. `~/.claude/plugins/marketplaces/anthropic-agent-skills` is also present, but marketplace presence is not activation (`~/.claude/settings.json:135-138`).

Plugin-cache SKILL.md keyword scan (`implementation plan|atomic|work unit|task decomposition|PRD`) returned no matching entrypoints; application-spec was inspected separately as requested. The cache contains laws, skill-creator and frontend-design entrypoints, not a discovered competing atomic-build pipeline.

Scout is **not missing as functionality**: V/.claude/skills/scout/SKILL.md defines the expected JSON decomposition. Architect is defined at V/.claude/agents/architect.md and routed by V/.claude/commands/architect.md:2-12. No matching Scout agent definition was found in R or the global Claude agents directory. V/.pi/agents/scout.md:1-6 is a generic Pi reconnaissance agent, not that JSON contract. Other same-name example agents found on disk are not proof of this pipeline's loading.

Metadata search covered `/Users/robertrhu` and `/Volumes/memit`, pruning package/cache-heavy subtrees. It reported permission-denied system/Photos/Trash directories; absence findings are scoped to searchable locations, not an exhaustive proof about every protected byte on the Mac. The ADF root hardcoded at C/prd-to-agentic-spec/SKILL.md:121 (`~/Projects/agent-deployment-framework`) is absent.

## 2. Duplicates and overlaps

- **Design:** brainstorming and office-hours both shape an idea. Prefer brainstorming's component boundaries and explicit design approval for this fixed-scope research team; office-hours is stronger for unsettled product demand, which is not this task.
- **PRD:** prd-author is the strongest match to the requested direction: design first, observable requirements second, each traced to a design commitment (S/prd-author/SKILL.md:28-65). The other PRD converters assume the PRD already exists. `prd-writing-guide` and `ai-agent-prd`, referenced by engineering-spec, are absent at the probed global roots.
- **Spec:** prefer prd-to-agentic-spec for a small engineering slice: one spec, exact artifacts, concrete validation, explicit gaps. Engineering-spec is stronger for a full migration/replicability dossier, but its many outputs increase integration burden. Spec-writer/framework-spec-writer preserve council/framework provenance; neither is a general decomposition engine. Application-spec's clean-room guarantee conflicts with an internal build spec.
- **Plan:** implementation-planner is strongest for contract coverage, acyclic dependencies and independent rollback/test boundaries. create-implementation-plan has better machine-oriented formatting, but weaker unit-local acceptance detail. Scout supplies usable JSON; architect supplies exact paths; both are foreign-project scoped.
- **Atomic briefs:** prefer P/writing-plans over C and N copies: P:140-175 specifies signatures/test assertions rather than entire routine function bodies, adds review focus and checks plan proportion. C:130-140 demands complete code, encouraging the giant plans we want to avoid. These copies are not interchangeable.
- **Review/dispatch:** plan-eng-review gives relevant architecture/testing checks; autoplan aggregates four review stages and dual voices, rather than solving our unit-size problem. SDD is intentionally serial; dispatching-parallel-agents permits independent domains. Neither supplies MAESTRO's current promote authority.

## 3. Gaps and incompatible defaults

1. **No ready-made team packet:** none of the surveyed skills guarantees an ~8-minute complete RED→GREEN unit, numbered prereg tests, exclusive file ownership, raw receipts, exact reply token and ≥60%/45% context handling together. This must be the MAESTRO brief contract, not a new worker's discretion.
2. **Synced portability:** S/prd-author/SKILL.md:52,76,80 and S/implementation-planner/SKILL.md:77-85 reference `references/...`. Those directories are absent; the named templates/protocols exist beside SKILL.md. Their V3/phase-clearance assumptions are from another workflow (both SKILL.md:10,18-22). Use explicit root-level resource paths and map gates honestly; never claim P3/P5/P6 clearance happened here.
3. **Gap handling:** agentic-spec's non-blocking draft gaps (:26-28) suit authoring, not execution. Any unknown that affects an acceptance test, interface, permission or resource bound blocks that unit until resolved in the owning upstream artifact. Do not manufacture a quota of gaps from :58.
4. **Worker side effects:** brainstorming and writing-plans instruct commits; gstack-spec files issues and may spawn execution; gstack preambles can write configuration, checkpoints, telemetry and external artifacts. Execution skills chain to branch finishing. Override these in the authorized brief; builders never commit/push/merge or run live/native/network/science actions without specific authority (R/CLAUDE.md:15-18,50-58).
5. **Verification mismatch:** P/subagent-driven-development/SKILL.md:337 discourages reviewer reruns. Our MAESTRO reruns remain binding. Same-family task reviewers are advisory; the promote gate is Astra at high effort (R/CLAUDE.md:16-17), regardless of a skill's generic “review clean” result.
6. **Dispatch and reconciliation:** N/P dispatch skills do not provide tmux supervision, full contract coverage or science-priority admission. File-disjoint workers can still share memory/disk or an unfrozen interface. Require dependency/ownership checks before fan-out, then one explicit integration unit with cross-boundary tests. Do not use lane-integrator's legal workflow as a code integration authority.
7. **Loading remains partly unproven:** Codex catalog advertisement is verified; Claude's actual session advertisement is not. `~/.codex/config.toml:159-166` has no explicit `multi_agent` entry; this survey session nevertheless exposes collaboration tools. Tool availability and dispatch authorization are separate; do not infer either from a skill file.

## 4. Recommended pipeline — PROPOSED

Exactly one selected skill per stage below. “Use” means an explicit read of the cited contract; it does not authorize its bundled scripts or foreign side effects. MAESTRO's prompt overrides are recorded in the packet, without modifying installed skills. All artifacts listed are proposed git records; **MAESTRO alone** verifies and commits them.

| Stage | One selected skill | Who runs it | Artifact left in git | Gate |
|---|---|---|---|---|
| Design | C/brainstorming/SKILL.md | MAESTRO with operator for genuine choices | design.md + stable decision/source IDs | MAESTRO reconciles settled authority; Astra reviews promotion; operator settles their forks. |
| PRD | S/prd-author/SKILL.md | MAESTRO; a Sol writer may draft one bounded requirement group | prd_v1.md + design→REQ coverage in that file | MAESTRO checks every requirement against design; Astra gates PRD promotion. |
| Engineering spec | C/prd-to-agentic-spec/SKILL.md | Sol writer per bounded component; MAESTRO integrates | spec_v1.md + gaps_v1.md when needed | MAESTRO resolves source conflicts/required gaps; Astra gates spec/interface freeze. |
| Dependency plan | S/implementation-planner/SKILL.md | MAESTRO; Sol may draft one contract group | plan_v1.md with unit DAG and SPEC→UNIT matrix | MAESTRO checks complete coverage/acyclicity; Astra gates plan promotion. |
| Atomic unit briefs | P/writing-plans/SKILL.md | MAESTRO, with a Sol writer for bounded packet preparation | units/Uxx_prompt.md + units/index.md | MAESTRO resolves exact paths/interfaces, preregisters numbered tests; Astra gates each promoted packet. |
| Execution/dispatch | P/dispatching-parallel-agents/SKILL.md | MAESTRO dispatches; one Sol builder per prompt | named code/tests, Uxx_report.md, RED/GREEN logs and hashes | MAESTRO reruns prescribed tests and checks scope; Astra gates each unit and integration promotion. |
| Promote review | R/.codex/skills/advisor-review/SKILL.md | MAESTRO prepares packet; Astra is binding reviewer | review_packet.md + astra_verdict.md beside each subject | Use Claude-led→GPT independence clause (:69-70); current CLAUDE.md Astra command/model supersedes stale examples. |

**Brief contract and sizing (PROPOSED):**

- A unit means one coherent observable change, its own failing tests, implementation, GREEN verification and receipt report within **at most ~8 minutes total builder work**, including essential reading. It is not one 2–5-minute step repeated five times. Pilot estimates from actual completion times; split before dispatch if reading/test time alone consumes the budget. Do not lower tests or acceptance to meet a time estimate.
- One builder, one prompt file, one exact allowlist covering production/test/report/log files; protected file hashes before/after. Dependent shared interfaces are frozen in a predecessor unit. Concurrent allowlists must be pairwise disjoint; a shared canonical document gets one integrator owner rather than parallel section editing.
- Every prompt contains source hashes and small cited spans; stable REQ/SPEC IDs; exact input/output signatures; numbered acceptance tests with expected values/labels; saved behavioral RED; GREEN command/expected count; boundary/round-trip/HALT cases where applicable; forbidden effects; receipt paths and exact finish token. A missing import alone does not demonstrate a behavioral RED.
- MAESTRO copies the already-approved constraints into the prompt. Avoid making each worker re-read the 1,178-line spec or rediscover neighboring contracts. Preserve source traceability so small packets cannot silently relax requirements. Documentation units use numbered content/coverage checks; runnable implementations use behavioral tests.
- Start a new unit only at ≥60% context left. At MAESTRO's ≤45% message or any compaction, stop new work, write the designated handoff with done/in-flight/paths/next action/risks and this context rule, and use a fresh successor. This brief's 45% stop point takes precedence over older 40% text (R/memory_mirror/context-management-every-session.md:14,20-22).
- MAESTRO verifies raw artifacts and reruns tests before committing verified bytes. Astra reviews the current packet/bytes at every promote gate; fixes require renewed affected checks. A final integration unit exercises real producer→consumer boundaries and accounts for every contract. Local fixtures, host acceptance and scientific conclusions remain separate.

## 5. First trial — the Drive switch-on plan, planning only

**Choose (a).** `results/drive_activation_intel_20261012/activation_plan_intel_v1.md` already exists, is bounded at 245 lines and has A1–A8/I2/I3 coverage (:218-245). Its ordered gates and Test lines (:18-34) make a compact pilot of traceability and packet sizing. Its status is PROPOSED/UNEXECUTED (:12); deriving artifacts cannot open commissioning.

**Do not choose (b) yet:** `results/research_engine_phase1_20261011/phase1_intel_build_plan_v1.md` was absent at the last probe; do not invent its contents. **(c) is second:** `results/dashboard_integration_review_20261011/labviz_spec_v3_ledger.md:3,7,15` is a reconciliation ledger against a 1,178-line predecessor, with explicit build hold; its conflicts/open items need reconciliation before freezing implementation units. Planning is permitted; drawings/building stay held.

Snapshot pins (the documents are in flight; re-pin before the trial):

| Input | Lines | SHA-256 / status |
|---|---:|---|
| Drive activation plan above | 245 | `2de4a4400df60ce28d6c3230b2be9adbfe803a8ff9a2427c5ce818c0d7608075` |
| Intel research-engine build plan above | — | ABSENT, not assessed |
| LabViz ledger above | 238 | `d869609b18987d4403f1ca415f1c20ccf0e45057fdf83227fefdc8eb946f38ac` |

**Concrete artifact chain, all PROPOSED:** keep the existing Drive plan untouched. MAESTRO reads its adopted-design citations as authority, then explicitly uses prd-author and its root-level prd-template.md to produce `results/drive_activation_intel_20261012/pipeline_trial/prd_v1.md`. REQ rows describe observable refusal, source consistency, bounded staging, science yielding and receipts, each citing the existing A/I/V4 source ID and section; unresolved operator choices remain unresolved.

Next, agentic-spec produces `pipeline_trial/spec_v1.md` and, when needed, `pipeline_trial/gaps_v1.md`. Each component records exact inputs/outputs, failure labels, permission boundaries, artifacts and concrete validation. Override the skill's absent ADF map; do not derive new transfer limits or permission from examples. MAESTRO/Astra freeze these contracts before a planner emits `pipeline_trial/plan_v1.md` and the atomic briefs.

**Unit-list format:** `ID | REQ/SPEC source+section | one deliverable | exact allowed files | consumes→produces | dependencies | numbered acceptance checks | RED/GREEN commands+expected results | estimated total minutes | forbidden effects | receipt paths | review/authority status`. Store full unit blocks in units/Uxx_prompt.md and the DAG/coverage index in units/index.md. Estimated paths/minutes are proposals until MAESTRO resolves and freezes them.

Illustrative first planning wave (each one prompt, ≤8-minute target; no implementation implied):

| Unit | Disjoint proposed output | Numbered acceptance checks | Dependency |
|---|---|---|---|
| D01 gate requirements | pipeline_trial/slices/gates_prd.md | 1. REVIEW→CHOICES→GO→COMMISSION preserved; 2. approval/choice alone never starts actions; 3. every requirement cites A6/source :18-34 | Frozen source set |
| D02 capture requirements | pipeline_trial/slices/capture_prd.md | 1. source inventory unknowns visible; 2. immutable/live/source-change/catch-up semantics preserved; 3. no deletion or new numeric bound | Frozen source set |
| D03 receipt requirements | pipeline_trial/slices/receipts_prd.md | 1. generation/history/readback requirements retained; 2. local fixtures cannot qualify Intel/Drive; 3. STOP preserves evidence | Frozen source set |
| D04 integration and coverage | pipeline_trial/prd_v1.md | 1. A1–A8 and I2/I3 each mapped; 2. cross-slice terms match; 3. choices/gaps and activation hold retained | D01–D03 |

After PRD/spec/plan gates, candidate build packets can separately cover a pure gate evaluator, capture-record validator and receipt validator, then one integration unit. **These are candidate boundaries, not approved features:** retain only contracts requiring new code after MAESTRO checks existing implementation. Exact code/test paths and numbered behavioral assertions must be resolved in the spec/brief; do not dispatch vague validators from this survey.

MAESTRO reruns the planning checks; Astra reviews the integrated PRD, then spec/plan and promoted packets. Native/host/Drive commissioning remains behind the original Astra review, exactly three operator choices and separate operator GO (`activation_plan_intel_v1.md:18-40`). Nothing in this pilot supplies that GO.

**Trial acceptance:** complete design→REQ→SPEC→UNIT coverage; zero conflicting parallel file ownership; no unresolved execution-critical gap in a dispatchable unit; actual builder durations recorded against the ~8-minute target; MAESTRO verification and Astra verdict persisted at each promotion. Any budget overrun yields a smaller successor unit, not a reduced contract.

## 6. Phone-readable recommendation

We already have skills that turn design decisions into requirements and break a spec into small, testable jobs, but several are sitting in a synced folder rather than a proven active pipeline. What was missing was the checked handoff from each requirement to one short builder brief, with clear file ownership and its own tests. Try this on the Drive plan first, while keeping MAESTRO verification, Astra review and the separate activation approval.

## Scope and handoff record

Only this report was created by SK1. The worktree was already dirty at entry (including tools/test_dashboard_mathlab.py and unrelated untracked artifacts); “only the new file” must mean SK1's delta, not a clean global status. No unrelated bytes were edited, no commits/installs/skill edits were performed. Concurrent document drift was observed in the LabViz ledger and is why snapshot hashes are recorded.

Next step: MAESTRO/Astra review this PROPOSED pipeline, then issue a separate bounded planning-only trial brief. Preserve the original source authorities and operator holds. Context directive for successors: new work only at ≥60% left; at MAESTRO's 45% message or any compaction, stop starting work, save a precise handoff with paths/status/risks/next action and restate this directive. This report is the permitted durable session record; no separate context-save artifacts were written.

Verification: sections 1–6 present; 30 inventory rows each have a path and loader-status evidence; section 4 has exactly seven stages with one skill each. Aliased file citations were checked for existence and line bounds. The tracked-diff SHA-256 remained `2ea631fdfea12f18955f3bc968d0774be732db96267108ccc0522e4aac1eaf3c`, identical to entry; global untracked status changed concurrently, so a globally clean status is not claimed. Final line count: 155.
