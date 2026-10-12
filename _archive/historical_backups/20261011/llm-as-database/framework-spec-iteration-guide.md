# LLM as Database — Framework Spec Iteration Guide
### Post-Session 7 Refinement Workflow

---

## How to Use This Guide

This guide picks up where the v1 spec project guide ends — after Session 7 (Full Council Synthesis) is complete and you have a first integrated spec document in hand. It defines the iterative process for refining both the **skills** and the **spec content** until the framework is implementation-ready.

Work through this guide in order. Each phase has explicit entry criteria — do not advance to the next phase until they are met.

---

## Phase 0 — Session 7 Debrief
*Complete immediately after Session 7 closes.*

This phase converts raw Session 7 output into structured inputs for the iteration loop.

### Step 0.1 — Extract the Gap Backlog

In a new session with the `framework-council` skill, submit this prompt:

```
Review the integrated spec document produced in Session 7.
Identify every location where a spec block contains any of the following:

- "to be determined" / "TBD"
- "approach not yet decided"
- An undefined interface contract
- An unresolved tension
- An open question explicitly deferred
- A decision marked as requiring implementation experience

For each gap found, produce a backlog entry in this format:

GAP-[N]:
  Domain(s): [which specialist(s) own this]
  Description: [what is undefined]
  Blocked by: [what must be true before this can be resolved]
  Blocks: [what cannot be specced until this is resolved]
  Priority: [Critical / High / Medium / Low]

Priority definitions:
  Critical — blocks 3 or more other gaps
  High — blocks 1–2 other gaps or is a load-bearing architectural decision
  Medium — self-contained gap with no downstream dependencies
  Low — refinement detail, does not affect other components

Sort by priority descending. Present the full backlog.
```

Save the output as `gap-backlog-v1.md` and upload to the project.

---

### Step 0.2 — Extract the Tension Resolution Map

In the same session, submit:

```
From Session 7, list every cross-domain tension that was:
(a) Fully resolved — state the resolution
(b) Partially resolved — state what was agreed and what remains open
(c) Unresolved / deferred — state why it was deferred

Format each as:

TENSION-[N]: [Warden] vs. [State Consistency Theorist]
Status: Resolved / Partial / Deferred
Resolution (if any): ...
Remaining open question (if partial or deferred): ...
```

Save as `tension-map-v1.md` and upload to the project.

---

### Step 0.3 — Extract the Skill Friction Log

**Project:** LLM as Database — Agent Harness Specification (same main project)
**Sessions:** Seven separate sessions — one per skill transcript
**Model:** Sonnet 4.6
**Web Search:** ✗
**Deep Research:** ✗
**Skills:** None invoked

---

#### Prerequisites

Before running Step 0.3, confirm:
- Steps 0.1 and 0.2 are complete — `gap-backlog-v1.md` and `tension-map-v1.md` are uploaded to the project
- All seven session transcripts have been exported as Markdown using the AI Chat Exporter Chrome extension and are ready to upload
- The six session summary documents are already in the project KB

If you have not yet exported session transcripts, do that first. Export each as Markdown immediately after the session closes: open the AI Chat Exporter extension, select Markdown format, save with the naming convention `transcript-session-[N]-[domain].md`. Upload all seven to the project before beginning Step 0.3.

---

#### Why Seven Separate Sessions

Each friction analysis session uploads one transcript as context and analyzes one skill's performance in depth. Analyzing all seven skills in a single session risks shallow coverage — the transcript content is dense and a single session will prioritize some skills over others. Seven focused sessions produce more specific, actionable friction entries. Each session is short (10–15 minutes) because the task is bounded.

---

#### Context for Each Session — KB vs. Direct Attachment

Every document in the project KB is automatically available in every session — you do not re-add them per session. Only the session transcript requires a manual action: attach it directly to the individual friction analysis session.

**Already in the KB — no action required per session:**
- `gap-backlog-v1.md` — uploaded in Step 0.1, available automatically
- `tension-map-v1.md` — uploaded in Step 0.2, available automatically
- All six session summary documents — uploaded during the v1 session arc, available automatically

**Attach directly to each session — one file per session:**
- The full session transcript for the session being analyzed only

Do not upload all seven transcripts to the project KB. They are large, session-specific, and would permanently inflate KB context for all future project sessions. Attach only the relevant transcript directly to each individual friction analysis conversation.

**Why gap-backlog and tension-map matter as context:**
Gaps and deferred tensions are the strongest objective signal of skill underperformance. If a gap in the backlog belongs to a skill's primary domain and that skill ran a full session on it, the skill likely missed something. The friction analysis uses these as anchors — not just the transcript — to triangulate what was missed vs. what was genuinely out of scope.

---

#### Session Map — Which Transcript for Which Skill

| Session # | Skill | Transcript File | Summary File |
|---|---|---|---|
| 1 | `graph-data-architect` | `transcript-session-1-schema.md` | `ontological-schema-llm-database-agent-framework.md` |
| 2 | `memit-specialist` | `transcript-session-2-write-engine.md` | `memit-specialist-spec-design.md` |
| 3 | `aiSecOps-specialist` | `transcript-session-3-security.md` | `threat-modeling-write-layer-access-control.md` |
| 4 | `validation-contract-architect` | `transcript-session-4-validation.md` | `validation-architecture-reflexion-loop-design.md` |
| 5 | `state-consistency-theorist` | `transcript-session-5-consistency.md` | `syncing-git-vindex-two-phase-commit.md` |
| 6 | `orchestration-comparativist` | `transcript-session-6-orchestration.md` | `orchestration-tools-requirements-matrix.md` |
| 7 | `framework-council` | `transcript-session-7-council.md` | `llm-as-database-v1.0-integrated-spec.md` |

---

#### Opening Prompt — Use for Each of the Seven Sessions

Substitute the bracketed values for each session before submitting.

```
I am conducting a post-session friction analysis for the LLM as Database
agent harness specification project. I have completed seven spec sessions
and am now auditing each specialist skill for underperformance.

This session analyzes: framework-council
Session analyzed: Session Session 7 - LLM database agent framework council synthesis    

Context documents uploaded for this session:
- Full session transcript: transcript-session-7-council.md
- Session summary: llm-as-database-v1.0-integrated-spec.md
- gap-backlog-v1.md — extracted gaps from the full spec
- tension-map-v1.md — cross-domain tensions from Session 7

Your task is to identify every instance where the framework-council skill
underperformed during Session 7. Do not invent friction — only flag
what is evidenced in the transcript or can be directly inferred from
the gap backlog and tension map.

Look for:

1. MISSED QUESTIONS — moments where the skill should have asked a
   probing question it didn't ask, evidenced by a topic that emerged 
   in the transcript or in Session 7 that this skill owned.

2. SPEC OUTPUT GAPS — spec blocks produced by this skill that are
   incomplete, vague, or that required significant revision during
   the session or in subsequent sessions.

3. MISSED CROSS-DOMAIN IMPLICATIONS — topics within this skill's domain
   that had effects on other skills' spec work, but were not
   flagged as interface contract requirements during this session.

4. FORMAT FAILURES — spec block outputs that didn't match the required
   format, were missing required fields, or that produced output the
   council had to reformat in Session 7 .

5. BACKLOG ATTRIBUTION — for every gap in gap-backlog-v1.md whose
   domain clearly belongs to framework-council, assess whether the skill
   should have resolved it sooner and failed to do so.

6. TENSION ATTRIBUTION — for every tension in tension-map-v1.md that
   was first surfaced in Session 7 rather than Session [N], assess
   whether framework-council should have surfaced it earlier.

For each friction instance found, produce an entry in this exact format:

SKILL-FRICTION-[N]:
  Skill: [skill name]
  Session: [session number and domain]
  Type: [Missed Question / Spec Output Gap / Cross-Domain Miss /
         Format Failure / Backlog Attribution / Tension Attribution]
  Evidence: [quote or reference from transcript, or gap/tension ID]
  Description: [what went wrong specifically]
  Confidence: [High / Medium]
    High = directly evidenced in transcript
    Medium = inferred from gap backlog or tension map
  Proposed fix: [specific change to the skill's SKILL.md that would
                 prevent this friction in future sessions]

Sort entries by Confidence descending, then by Type.
At the end, provide a one-paragraph summary of this skill's overall
performance pattern — what it does well and what its systematic weakness is.
```

---

#### After Each of Sessions 1–6

1. Copy the friction entries and skill performance summary to a running document
2. Number entries sequentially across all sessions (SKILL-FRICTION-1 through SKILL-FRICTION-N — do not restart numbering per skill)
3. After all seven sessions are complete, compile the full log as `skill-friction-log-v1.md`
4. Upload to the project KB

Do not upload partial friction logs between sessions — compile once, upload once, after all seven sessions are complete.

---

#### Session 7 Friction Analysis — Standalone Purpose-Built Prompt

Session 7 requires a completely different friction analysis prompt from Sessions 1–6. The `framework-council` skill has a different failure profile from the specialist skills — it fails through facilitation and synthesis quality failures, not domain content gaps. The standard specialist prompt does not apply.

**Session setup:**
- **Model:** Sonnet 4.6
- **Web Search:** ✗ | **Deep Research:** ✗ | **Skills:** None
- **Attach directly to session:** `transcript-session-7-council.md`
- **KB provides automatically:** `gap-backlog-v1.md`, `tension-map-v1.md`, `llm-as-database-v1.0-integrated-spec.md`, all six session summaries

**Session 7 friction analysis prompt:**

```
I am conducting a post-session friction analysis for the LLM as Database
agent harness specification project, specifically evaluating the
framework-council skill's performance during Session 7 — Full Council
Synthesis.

The council skill's job in Session 7 was:
1. Facilitate authentic multi-specialist discussion
2. Surface and hold cross-domain tensions without resolving prematurely
3. Route topics to the correct specialist voice(s)
4. Synthesize session work into a complete integrated spec document
5. Produce a tension resolution map

Context documents available:
- Full Session 7 transcript: transcript-session-7-council.md
- Integrated spec output: llm-as-database-v1.0-integrated-spec.md
- Gap backlog: gap-backlog-v1.md
- Tension map: tension-map-v1.md
- All six session summaries (in project KB)

Evaluate the council skill's performance across these six dimensions.
For each friction instance found, produce an entry in this format:

SKILL-FRICTION-[N]:
  Skill: framework-council
  Session: 7 — Full Council Synthesis
  Type: [see types below]
  Evidence: [quote or reference from transcript, spec, or gap/tension ID]
  Description: [what went wrong specifically]
  Confidence: [High = directly evidenced / Medium = inferred]
  Proposed fix: [specific change to the council SKILL.md]

---

DIMENSION 1 — ROUTING QUALITY
Did the council correctly identify which specialist(s) had primary stake
in each topic raised during the session? Look for:
- Topics routed to the wrong specialist voice
- Topics handled by the council narrator instead of a specialist voice
- Moments where a relevant specialist was not invited to respond
- Moments where too many specialists were brought in, diluting focus
Type label: Routing Failure

---

DIMENSION 2 — VOICE AUTHENTICITY
Were the six specialist voices rendered as genuinely distinct
perspectives, or did some converge into similar concerns? Look for:
- Specialists that echoed each other rather than providing distinct angles
- Specialists whose known domain instincts were not reflected
  (e.g., the Warden not defaulting to least privilege,
  the MEMIT Specialist not pushing back on high edit volumes)
- Moments where the council narrator voice overrode a specialist
  rather than facilitating between them
Type label: Voice Authenticity Failure

---

DIMENSION 3 — TENSION SURFACING
Did the council proactively surface cross-domain tensions, or only
acknowledge them when the user raised them? Look for:
- Tensions in tension-map-v1.md that were first raised by the user
  rather than by the council
- Pre-mapped tensions (T1–T6) that were not surfaced during Session 7
- Tensions that were named but not held open — resolved too quickly
  without adequate exploration
- New tensions that should have been caught in Session 7 but only
  appeared in the gap backlog
Type label: Tension Surfacing Failure

---

DIMENSION 4 — SYNTHESIS QUALITY
Does the integrated spec reflect a true synthesis of all six domains,
or are some domains underrepresented? Look for:
- Spec blocks in the integrated spec that are thinner than the
  corresponding session summary (regression from session to synthesis)
- Domains with fewer spec blocks than their session warranted
- Interface contracts defined during sessions that did not appear
  in the integrated spec
- TBD items that were actually resolved during sessions but not
  captured in synthesis
Type label: Synthesis Gap

---

DIMENSION 5 — PHASE DISCIPLINE
Did the council correctly manage session phases — holding exploration
open before moving to synthesis? Look for:
- Premature synthesis — producing spec output before tensions were
  adequately explored
- Exploration that ran too long without a synthesis checkpoint
- Moving to synthesis on one topic while leaving an active tension
  on another unacknowledged
- Failure to explicitly name phase transitions
Type label: Phase Discipline Failure

---

DIMENSION 6 — SPEC INTERNAL CONSISTENCY
Does the integrated spec contain internal contradictions introduced
during synthesis — not present in individual session summaries?
Look for:
- Spec blocks in different domains that make incompatible claims
  about the same component
- Interface contracts that conflict with the spec blocks they describe
- Decisions marked resolved in one domain but open in another
- Requirements from one specialist that contradict another without
  a documented resolution
Type label: Internal Inconsistency

---

After all friction entries, provide:

COUNCIL PERFORMANCE SUMMARY:
Two paragraphs. Paragraph 1: what the council did well in Session 7.
Paragraph 2: the systematic weakness pattern — what type of failure
appeared most frequently and what that suggests about the skill design.

PRIORITY FIXES:
The top 3 proposed fixes from your friction entries, ranked by impact
on future council session quality.
```

---

**Phase 0 exit criteria:**
- [ ] `gap-backlog-v1.md` complete and uploaded
- [ ] `tension-map-v1.md` complete and uploaded
- [ ] All seven session transcripts exported as Markdown and ready to attach
- [ ] Six specialist friction analysis sessions completed (Sessions 1–6)
- [ ] One council friction analysis session completed (Session 7, using council prompt)
- [ ] `skill-friction-log-v1.md` compiled from all seven sessions and uploaded
- [ ] Project custom instructions updated to reference `gap-backlog-v1.md` and `tension-map-v1.md` as active working documents

---

## Phase 1 — Skill Refinement
*Improve the skills before running gap sessions.*

Skill refinement comes before spec gap sessions for one reason: if the skills have friction points, you'll reproduce those same gaps in every future session you run. Fix the tools first.

### Step 1.1 — Triage the Skill Friction Log

Open a session in this project (no skill invoked — just Claude). Submit:

```
Review skill-friction-log-v1.md.
Group friction entries by skill.
For each skill, summarize:
- How many friction points were logged
- What pattern emerges (missing questions, weak spec format, scope confusion, etc.)
- Recommended priority for refinement (High / Medium / Low)

Present as a skill refinement priority list.
```

---

### Step 1.2 — Refine Each Skill (High Priority First)

For each skill flagged as High priority, open a **separate session** and submit:

```
I need to refine the [skill-name] skill.

Here are the friction points logged during v1 spec sessions:
[paste relevant SKILL-FRICTION entries]

Invoke the skill-creator skill. Review the current SKILL.md for [skill-name]
and propose specific edits to address each friction point. Show me before/after
for each change. Do not change the skill's ownership scope or spec output format
— only improve what it does within its domain.
```

Review the proposed changes. Approve, reject, or modify each one. Then:

```
Apply the approved changes and produce an updated SKILL.md.
```

Repackage the updated skill:
- Copy updated SKILL.md to the skill folder
- Repackage as `.skill` file
- Reinstall in the project (remove old version first)

Repeat for each skill in priority order.

---

### Step 1.3 — Tighten Interface Contracts Between Skills

After individual skill refinements, run one cross-skill pass. Open a session with the `framework-council` skill:

```
Convene the council for a brief interface contract review.

From Session 7, the following interface contracts were either undefined
or vague: [paste relevant items from tension-map-v1.md and gap-backlog-v1.md]

For each undefined contract, have the relevant specialists negotiate
a precise definition. Format output as:

INTERFACE CONTRACT:
  From: [Component A]
  To: [Component B]
  What A exposes: ...
  Conditions: ...
  Failure behavior: ...
```

Add approved interface contracts to the relevant individual skill SKILL.md files
in their "Interface contract" sections. Repackage and reinstall affected skills.

**Phase 1 exit criteria:**
- [ ] All High priority skill friction points addressed
- [ ] All Medium/Low friction points either addressed or explicitly deferred with rationale
- [ ] All undefined interface contracts from Session 7 now defined
- [ ] Updated skills reinstalled in project
- [ ] `skill-refinement-log-v1.md` created documenting changes made

---

## Phase 2 — Gap Session Arc
*Resolve spec gaps in dependency order.*

### Step 2.1 — Build the Gap Session Schedule

Open a session (no skill invoked). Submit:

```
Review gap-backlog-v1.md.

Build a gap session schedule:
1. Order gaps by dependency — gaps that are "blocked by" nothing come first
2. Group gaps that share a primary domain into the same session where possible
3. Flag any gaps that require the full council vs. a single specialist
4. Estimate the number of sessions required

Present as a numbered session schedule:
GAP SESSION [N]: Gaps [X, Y, Z] — Primary skill: [skill] — Est. length: [short/medium/long]
```

Save the schedule as `gap-session-schedule-v1.md`.

---

### Step 2.2 — Run Gap Sessions

For each gap session on the schedule, use this opening template:

```
Gap Session [N] of [total] — [Domain(s)]

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is complete. I am resolving specific
open questions from the gap backlog.

Gaps to resolve in this session:
[paste relevant GAP entries from gap-backlog-v1.md]

Relevant context from v1.1 spec:
[paste the spec blocks most relevant to these gaps]

Invoke [skill-name]. Begin with any clarifying questions you need,
then work toward a resolved spec block for each gap.
```

At the end of each gap session, generate a session summary block:

```
Generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

Save each summary as `gap-session-[N]-summary.md` and upload to project.

---

### Step 2.3 — Council Review Checkpoint

After every 3–4 gap sessions, pause and run a council review. Open a session with the `framework-council` skill:

```
Council Review Checkpoint — after Gap Sessions [N] through [M].

The following gaps have been resolved since the last council review:
[paste relevant gap session summaries]

Council tasks:
1. Verify each resolution does not introduce new cross-domain tensions
2. Check that resolved gaps are internally consistent with each other
3. Update the tension map — mark any tensions now resolved by gap work
4. Surface any new tensions introduced by the resolutions

Do not re-open resolved gaps unless a genuine inconsistency is found.
Present findings as: Verified / Tension Introduced / Inconsistency Found.
```

If tensions are introduced, add them to the gap backlog and schedule a
targeted gap session before continuing.

**Phase 2 exit criteria:**
- [ ] All Critical and High priority gaps resolved
- [ ] All Medium priority gaps resolved or explicitly deferred with rationale
- [ ] All Low priority gaps addressed or accepted as implementation-time decisions
- [ ] Most recent council review checkpoint produced no new unresolved tensions
- [ ] `gap-backlog-v2.md` updated with final status of all gaps

---

## Phase 3 — v2 Spec Synthesis
*Produce the updated integrated spec document.*

### Step 3.1 — Compile the v2 Spec

Open a session with the `framework-council` skill:

```
Full Council — v2 Spec Synthesis.

The following gap sessions have been completed since the v1 spec:
[paste all gap session summaries]

The skill friction log has been addressed. Interface contracts have been updated.

Council tasks:
1. Produce an updated integrated spec document incorporating all gap resolutions
2. Where v1 spec blocks have been superseded, replace them — do not append
3. Mark any remaining open questions explicitly as "Implementation-time decision"
4. Produce an updated tension map showing all tensions and their current status

Format: use the standard integrated spec block format from Session 7.
```

Save the output as `integrated-spec-v2.md` and upload to the project.

---

### Step 3.2 — v2 Readiness Assessment

In the same or a follow-up session with the `framework-council` skill:

```
Assess the v2 integrated spec for implementation readiness.

For each major component of the framework, answer:
1. Is the spec complete enough to begin implementation planning? Yes / No / Partially
2. If partially or no — what is the minimum additional spec work required?
3. Are there any components where the spec makes assumptions that
   should be validated by a prototype before full implementation?

Present as a readiness matrix, then a recommended next step:
- Proceed to implementation planning
- Run additional gap sessions on [specific components]
- Build a proof-of-concept for [specific component] before speccing further
```

**Phase 3 exit criteria:**
- [ ] `integrated-spec-v2.md` complete and uploaded
- [ ] Readiness assessment complete
- [ ] Decision made: proceed to implementation planning, more gap sessions, or prototype first

---

## Phase 4 — Iteration Decision Point

After Phase 3, choose one of three paths:

### Path A — Proceed to Implementation Planning
*If the readiness assessment shows all components are spec-complete.*

The spec project transitions from brainstorm/spec mode to implementation planning mode. The skills built here are no longer the primary tools — engineering planning tools take over. Archive this project as reference.

### Path B — Additional Gap Sessions
*If the readiness assessment identifies remaining gaps that can be resolved through spec work.*

Return to Phase 2. Run targeted gap sessions for the identified components. Advance to Phase 3 again when resolved.

### Path C — Prototype First
*If the readiness assessment identifies components where the spec makes assumptions that require validation.*

Build a minimal proof-of-concept for the flagged component(s). Use what you learn to close the spec gaps that require implementation experience. Return to Phase 2 with empirical findings as input.

---

## Ongoing Maintenance

Even after reaching implementation planning, maintain this project as a living reference:

**When implementation surfaces a spec conflict:**
Open a targeted session with the relevant specialist skill. Document the conflict, resolve it, and update the integrated spec. This is a Phase 2 gap session — run it the same way.

**When the framework scope expands:**
New components that fall outside the existing six domains may require new specialist skills. Return to the skill-creator workflow from Session 0 to design and build them. Update `skill-design-decisions.md` to document the addition before installing.

**When base technology changes:**
MEMIT advances, new orchestration tools emerge, new model architectures appear. Run a targeted research session with the relevant specialist and web search / deep research enabled to assess spec impact. Update affected spec blocks.

**When a new spec-writing skill is installed:**
If a dedicated spec-writing skill has been built and installed, invoke it alongside the relevant specialist skill in all gap sessions and synthesis passes. It improves output format consistency across domains and should be treated as a standing session tool from the point of installation forward. Update the model and tool guidance table below to reflect its inclusion.

**Gap session naming convention:**
Name gap session summaries descriptively rather than by number alone — e.g., `gap-session-pruning-agent-triggers.md` rather than `gap-session-07-summary.md`. Descriptive names make the KB scannable when returning after a long break.

---

## Reference — Full Document Index

### Project KB — Foundation Documents
*Uploaded before Session 1. Permanent reference — never overwritten.*

| Document | Created | Purpose |
|---|---|---|
| `llm-as-database-agent-harness-framework.md` | Session 0 | Source reference document |
| `framework-spec-project-guide.md` | Session 0 | v1 session arc and opening prompts |
| `framework-spec-iteration-guide.md` | Session 0 | This document — iteration workflow |
| `skill-design-decisions.md` | Session 0 | Skill team design rationale and modification rules |

### Project KB — v1 Session Summaries
*Uploaded immediately after each session closes. Never overwritten — permanent audit trail.*

| Document | Created | Purpose |
|---|---|---|
| `ontological-schema-llm-database-agent-framework.md` | After Session 1 | Schema design decisions and constraints |
| `memit-specialist-spec-design.md` | After Session 2 | Write engine spec and MEMIT decisions |
| `threat-modeling-write-layer-access-control.md` | After Session 3 | Security architecture and trust boundaries |
| `validation-architecture-reflexion-loop-design.md` | After Session 4 | Validation pipeline and Reflexion loop spec |
| `syncing-git-vindex-two-phase-commit.md` | After Session 5 | State consistency and two-phase commit spec |
| `orchestration-tools-requirements-matrix.md` | After Session 6 | Orchestration requirements and candidate evaluation |

### Project KB — Integrated Spec
*Uploaded after Session 7. Authoritative — supersedes individual session summaries for spec purposes, but summaries remain as audit trail.*

| Document | Created | Purpose |
|---|---|---|
| `llm-as-database-v1.0-integrated-spec.md` | After Session 7 | First full cross-domain spec — archived after v2 |

### Project KB — Iteration Working Documents
*Created and uploaded during the iteration phases below. Updated in place as work progresses.*

| Document | Created | Updated |
|---|---|---|
| `gap-backlog-v1.md` | Phase 0 | Phase 2 (status updates) |
| `tension-map-v1.md` | Phase 0 | Phase 2 checkpoints |
| `skill-friction-log-v1.md` | Phase 0 | Phase 1 only |
| `skill-refinement-log-v1.md` | Phase 1 | Phase 1 only |
| `gap-session-schedule-v1.md` | Phase 2.1 | Phase 2 only |
| `gap-session-[N]-summary.md` | Each gap session | Never (append-only) |
| `gap-backlog-v2.md` | Phase 2 (end) | Phase 2 only |
| `integrated-spec-v2.md` | Phase 3 | Phase 3+ |

### KB Management Rules

- **Never delete session summaries.** They are the audit trail for how decisions were reached. Gap sessions will reference them.
- **Never overwrite archived specs.** When v2 is uploaded, v1 remains. Label clearly with version suffix.
- **Gap session summaries are append-only.** Save each as a separate numbered file — do not consolidate into one document until Phase 3 synthesis.
- **Update this guide** whenever a new document type is introduced (e.g., a new iteration cycle produces v3 working documents). Keep the index current.
- **Project instructions require one update** when this iteration phase begins — add a line referencing `gap-backlog-v1.md` and `tension-map-v1.md` as active working documents so the council can reference them directly in gap sessions.

---

## Model & Tool Guidance — Per Phase and Step

### Why These Choices

**Opus 4.6** is warranted when the session requires holding multiple competing constraints simultaneously, resolving cross-domain tensions, or evaluating complex tradeoffs with long dependency chains. It costs more — use it deliberately.

**Sonnet 4.6** is sufficient for focused single-domain work, structured extraction tasks, skill editing, and any session where the output format is well-defined and the reasoning is bounded.

**Web Search** is enabled whenever current tool capabilities, research literature, or evolving technology landscape is relevant to the session. Disabled for pure reasoning and spec synthesis sessions — search results add noise when the work is internal consistency checking.

**Deep Research** is reserved for sessions requiring comprehensive current-state analysis of rapidly evolving tooling (orchestration platforms, MEMIT advances). Expensive and slow — use only where training data is likely stale and completeness matters.

---

### Phase 0 — Session 7 Debrief

| Step | Task | Model | Web Search | Deep Research | Skills |
|---|---|---|---|---|---|
| 0.1 | Extract gap backlog | Sonnet 4.6 | ✗ | ✗ | `framework-council` |
| 0.2 | Extract tension resolution map | Sonnet 4.6 | ✗ | ✗ | `framework-council` |
| 0.3 | Compile skill friction log | —* | ✗ | ✗ | None |

*Step 0.3 is authored by you from your own session notes — no Claude session required.

**Rationale:** All Phase 0 work is extraction and organization of existing material from Session 7 output. Sonnet handles structured extraction cleanly. No external research needed — everything required is already in the KB.

---

### Phase 1 — Skill Refinement

| Step | Task | Model | Web Search | Deep Research | Skills |
|---|---|---|---|---|---|
| 1.1 | Triage skill friction log | Sonnet 4.6 | ✗ | ✗ | None |
| 1.2 | Refine individual skills | Sonnet 4.6 | ✗ | ✗ | `skill-creator` |
| 1.3 | Interface contract negotiation | Sonnet 4.6 | ✗ | ✗ | `framework-council` |

**Rationale:** Skill editing is bounded, single-domain work — Sonnet is fully capable. No external research needed; skill refinement draws on session friction observations and the existing SKILL.md bodies. The interface contract negotiation (Step 1.3) involves multiple specialist voices but the task is well-defined — resolving already-identified vague contracts, not open-ended exploration. Sonnet is sufficient.

**Exception:** If a skill friction point involves a domain where the underlying research landscape may have shifted (e.g., MEMIT Specialist friction related to new model editing techniques), enable Web Search for that specific refinement session.

---

### Phase 2 — Gap Session Arc

#### Step 2.1 — Build the Gap Session Schedule

| Model | Web Search | Deep Research | Skills |
|---|---|---|---|
| Sonnet 4.6 | ✗ | ✗ | None |

Scheduling is a dependency-ordering and grouping task — structured reasoning on existing backlog content. No exploration or external data needed.

#### Step 2.2 — Run Gap Sessions

Gap session configuration varies by domain. Apply the row that matches the primary skill for each session:

| Primary Domain | Model | Web Search | Deep Research | Skills |
|---|---|---|---|---|
| Schema / ontology | Sonnet 4.6 | ✓ | ✗ | `graph-data-architect` |
| Write engine / MEMIT | **Opus 4.6** | ✓ | ✓* | `memit-specialist` |
| Security / trust | Sonnet 4.6 | ✓ | ✗ | `aiSecOps-specialist` |
| Validation / Reflexion loop | Sonnet 4.6 | ✓ | ✗ | `validation-contract-architect` |
| State consistency | **Opus 4.6** | ✓ | ✗ | `state-consistency-theorist` |
| Orchestration | **Opus 4.6** | ✓ | ✓ | `orchestration-comparativist` |
| Cross-domain (2+ specialists) | **Opus 4.6** | ✓ | ✗ | `framework-council` |

*Deep Research for MEMIT gap sessions only if the gap involves verifying current MEMIT implementation state or post-2023 model editing advances. For pure architectural reasoning gaps, Web Search is sufficient.

**Why Opus for write engine, state consistency, orchestration, and cross-domain:**
- Write engine gaps frequently involve multi-variable tradeoffs (edit volume vs. locality vs. forgetting) that benefit from Opus's extended reasoning
- State consistency gaps involve distributed systems edge cases with long dependency chains
- Orchestration gaps require evaluating rapidly-changing tooling against a complex requirements matrix
- Cross-domain gaps by definition require holding multiple specialist perspectives simultaneously

#### Step 2.3 — Council Review Checkpoint

| Model | Web Search | Deep Research | Skills |
|---|---|---|---|
| **Opus 4.6** | ✗ | ✗ | `framework-council` |

**Rationale:** The checkpoint's job is consistency verification across all resolved gaps simultaneously — detecting new tensions introduced by solutions. This is exactly the multi-constraint reasoning Opus handles best. No external research needed; the work is internal consistency checking against existing spec material.

---

### Phase 3 — v2 Spec Synthesis

| Step | Task | Model | Web Search | Deep Research | Skills |
|---|---|---|---|---|---|
| 3.1 | Compile v2 integrated spec | **Opus 4.6** | ✗ | ✗ | `framework-council` |
| 3.2 | Readiness assessment | **Opus 4.6** | ✗ | ✗ | `framework-council` |

**Rationale:** Both steps require holding the full six-domain spec in working context simultaneously — the largest reasoning load in the entire iteration arc. Opus is non-negotiable here. No external research; synthesis draws exclusively on KB content.

---

### Phase 4 — Ongoing Maintenance

| Task | Model | Web Search | Deep Research | Skills |
|---|---|---|---|---|
| Implementation conflict resolution | Sonnet 4.6 | ✓ | ✗ | Relevant specialist |
| New skill design | Sonnet 4.6 | ✗ | ✗ | `skill-creator` |
| Technology change assessment — MEMIT | **Opus 4.6** | ✓ | ✓ | `memit-specialist` |
| Technology change assessment — orchestration | **Opus 4.6** | ✓ | ✓ | `orchestration-comparativist` |
| Technology change assessment — other domains | Sonnet 4.6 | ✓ | ✓ | Relevant specialist |

**Rationale:** Technology change assessments for MEMIT and orchestration use Opus because changes in those domains require re-evaluating complex tradeoff matrices. Other domain changes (security standards, validation patterns) are more bounded and Sonnet handles them cleanly.

---

### Summary Matrix — Full Iteration Arc

| Phase | Step | Model | Web Search | Deep Research |
|---|---|---|---|---|
| 0 | Gap backlog extraction | Sonnet 4.6 | ✗ | ✗ |
| 0 | Tension map extraction | Sonnet 4.6 | ✗ | ✗ |
| 0 | Skill friction analysis (×7 sessions) | Sonnet 4.6 | ✗ | ✗ |
| 1 | Skill friction triage | Sonnet 4.6 | ✗ | ✗ |
| 1 | Skill refinement | Sonnet 4.6 | ✗ | ✗ |
| 1 | Interface contract negotiation | Sonnet 4.6 | ✗ | ✗ |
| 2.1 | Gap session schedule | Sonnet 4.6 | ✗ | ✗ |
| 2.2 | Gap session — schema | Sonnet 4.6 | ✓ | ✗ |
| 2.2 | Gap session — write engine | **Opus 4.6** | ✓ | ✓* |
| 2.2 | Gap session — security | Sonnet 4.6 | ✓ | ✗ |
| 2.2 | Gap session — validation | Sonnet 4.6 | ✓ | ✗ |
| 2.2 | Gap session — state consistency | **Opus 4.6** | ✓ | ✗ |
| 2.2 | Gap session — orchestration | **Opus 4.6** | ✓ | ✓ |
| 2.2 | Gap session — cross-domain | **Opus 4.6** | ✓ | ✗ |
| 2.3 | Council review checkpoint | **Opus 4.6** | ✗ | ✗ |
| 3 | v2 spec synthesis | **Opus 4.6** | ✗ | ✗ |
| 3 | Readiness assessment | **Opus 4.6** | ✗ | ✗ |
| 4 | Implementation conflict | Sonnet 4.6 | ✓ | ✗ |
| 4 | New skill design | Sonnet 4.6 | ✗ | ✗ |
| 4 | Technology change — MEMIT/orchestration | **Opus 4.6** | ✓ | ✓ |
| 4 | Technology change — other | Sonnet 4.6 | ✓ | ✓ |

*Deep Research for write engine gap sessions only when the gap involves verifying current MEMIT implementation state or post-2023 model editing advances.
