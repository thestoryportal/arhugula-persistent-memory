# Operator decisions — research engine

This log preserves each operator decision with its date and exact words. Final written-design approval is recorded below; unselected suggestions remain proposals.

Session boundaries: design only; write only in this folder; no commits, installs, experiments, or launches.

## 2026-10-11 03:25 UTC — Include all three outcomes

Operator exact words:

> All - A, B and C

Interpretation: include choosing better experiments, trusting the research map, and discovering possible solutions in the design. No choice of tool, implementation order, or execution autonomy has been made.

## 2026-10-11 03:26 UTC — Manage follow-through

Operator exact words:

> C

Selected option: "Manage follow-through too. Prepare proposals, track approved experiments through MAESTRO, connect their results back to the research map, and suggest what comes next. A fuller research cycle, with more integration work."

Interpretation: include the complete research cycle. This does not authorize this brainstorming session to build or run anything, and does not grant the future engine permission to bypass preregistration, Astra review, MAESTRO coordination, or operator approvals.

## 2026-10-11 03:28 UTC — All human views and agents as first-class users

Operator exact words:

> A, B and C. And the engine must treat agents as first class citizens for autonomous work as well.

Interpretation: include conversation, an explorable research map, and recurring briefings. Agent access is a core requirement: structured queries, proposals, work coordination, and outcome reporting against the same research records. The autonomous authority boundary is not yet decided.

## 2026-10-11 03:32 UTC — Autonomous investigation; human approval for experiments and resource contention

Operator exact words:

> C. And any work that impacts GPU/CPU/SSD/HDD resources that block other work, ask for me to not run my own other work on my system, etc require HIL UNLESS already managed by our autonomous management systems such a gdrive back, etc.

Selected option C: agents investigate and prepare experiment proposals autonomously; each experiment waits for a separate go-ahead.

Resource rule: work that could block other work through GPU, CPU, SSD or HDD use, or require the operator to refrain from using their system, requires human approval unless an existing autonomous management system already manages that specific workload. The operator gave gdrive backup as an example.

Design interpretation: the rule applies to database rebuilds, bulk parsing, graph generation, local model use and analysis as well as science runs. Existing management coverage must be established for the requested workload; a tool being installed or the machine appearing idle does not establish an exemption. The resource exception alone does not waive the separate experiment go-ahead.

## 2026-10-11 03:32 UTC — Operator can interject into the research loop

Operator exact words:

> And of course if I surface research or ideas I am able to interject into the loop

Interpretation: accept operator-supplied papers, ideas, questions and direction changes during investigations. Preserve their origin and exact instruction, acknowledge the input, and show its effect on the plan. Input remains a lead until checked; operator direction controls priorities and scope but does not turn a claim into scientific evidence. Replanning cannot silently amend frozen experiment criteria. Explicit stop requests still stop work.

## 2026-10-11 03:38 UTC — Use DuckDB and Neo4j with the proposed division

Operator exact words:

> Both with that division

Approved division: Git is the authority for research records and checked connections; DuckDB handles measurements, comparisons and numerical summaries; Neo4j handles connections among hypotheses, claims, experiments, findings, decisions and papers; the engine combines answers with evidence pointers for humans and agents. Both databases are rebuildable views of the same dated snapshot, with stable shared IDs. Avoid duplicating all raw measurements in Neo4j. Introduce them on a small hand-checked slice before wider expansion. Resource approvals still apply.

## 2026-10-11 03:40 UTC — Approve records and trust section

Operator exact words:

> Yes

Approved section: written research vocabulary covering questions/ideas, tests/evidence, direction/history, work/responsibility; source and checked/suggested status for links; scoped measurements; distinct evidence kinds and halted/partial results; explicit indexing coverage. This is section approval, not final approval of design.md.

## 2026-10-11 03:50 UTC — Approve MathLab and InfraNodus roles; request AutoResearch and LabViz integration

Operator exact words:

> It does fit my intent. Additionally, how might the AutoResearch feature fit into the research engine stack and loop? Also, integration with the existing LabViz dashboard?

Approved: integrate MathLab as an independently gated analysis workbench; use InfraNodus as a source of candidate connections, with actual value checked against a baseline. Preserve current MathLab stop and resource permissions. AutoResearch and LabViz roles are requested for exploration and are not yet approved.

## 2026-10-11 04:00 UTC — Approve LabViz integration; clarify AutoResearch routing

Operator exact words:

> LabViz integrations approved. One clarification about AutoResearch: so the engine would never send possible experiments to it to test? Even after an experiment is run through the scientific loop? How would the loop determine when to invoke AutoResearch?

Approved: LabViz as the shared human workspace, preserving existing evidence views and rules, adding connected research, proposals, conversation/briefings, operator inputs and analysis links. AutoResearch invocation and future mission routing require clarification; no blanket approval of those policies is inferred.

## 2026-10-11 04:06 UTC — Guided AutoResearch mode and autonomous agent access across all features

Operator exact words:

> I choose A. One more clarification/requirement: all of this must treat agents as first class citizens so they are able to work autonomously with all features.

Approved AutoResearch policy: preserve the existing isolated optimizer and add a separately reviewed guided search mode for future missions, accepting approved seed ideas/starting recipes. Search outcomes remain candidates for independent scientific confirmation.

Agent requirement: agents can work autonomously with every feature through direct structured interfaces, shared records and resumable tasks. This adds full feature access; it does not revoke the earlier chosen autonomy C, separate experiment go-ahead, resource-contention HIL rule or scientific gates. Work requiring those permissions waits for valid authorization. No approval to change the existing optimizer or execute a new mission in this design-only session is inferred.

## 2026-10-11 04:08 UTC — Approve agent workflow

Operator exact words:

> Yes

Approved: direct agent interfaces across every feature; shared records and rules; scoped, source-linked, checkpointed tasks; duplicate-request protection; independently authorized work while awaiting approval; resume only against valid approvals/inputs; isolated and separately reviewed guided AutoResearch; acknowledged operator interjections. This approves the workflow section, not final approval of design.md.

## 2026-10-11 04:10 UTC — Approve phases and first test slice

Operator exact words:

> Yes

Approved: five phases covering the small checked dual-database/agent slice, full-program coverage, shared human/agent workflow, discovery/analysis integrations and approved follow-through. Each expansion has checkable acceptance. First brief: vocabulary, roughly five independently checked evidence chains, both rebuildable database views and a minimal structured agent interface, under an approved resource budget with no model experiment. This is phase/section approval; review of the final written design remains pending.

## 2026-10-11 04:23:51 UTC — Final written-design approval

Operator exact words:

> Approved

Approved: the written design.md linked by BRAIN2 for handoff to MAESTRO. Final approval completes the brainstorming session; it does not authorize this session to implement, install, provision, launch or run experiments. MAESTRO owns the next independent review, build brief and commits. BRAIN2 changed approval metadata only, with no substantive design changes.
