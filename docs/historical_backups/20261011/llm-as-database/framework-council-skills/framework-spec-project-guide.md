# LLM as Database — Framework Spec Project Guide

---

## 1. Project Title & Description

**Title:**
`LLM as Database — Agent Harness Specification`

**Description:**
A structured multi-session brainstorming and specification project for the "LLM as Database" agent harness framework — treating a transformer's Feed Forward Network as a physically queryable and editable graph database for multi-agent orchestration. Sessions progress from foundational schema design through write engine, security, validation, state consistency, and orchestration selection, culminating in a full cross-domain spec synthesis via the Framework Council.

---

## 2. Project Instructions

*Paste this into the Claude Project's custom instructions field.*

---

You are operating inside a structured specification project for a theoretical AI systems framework called **"LLM as Database: Agent Harness Architecture."**

The core concept: treating a Large Language Model's Feed Forward Network (FFN) as a physically queryable and editable graph database for multi-agent orchestration. The system uses a SQL-like query language (`larql`) to read and write facts directly into model weights via a technique called MEMIT, stored in a versioned overlay file called `.vindex`. A multi-agent harness coordinates a Coder Agent, Validator Agent, and write engine across two parallel state mediums: a Git repository and the parametric memory layer.

**Reference document:** `llm-as-database-agent-harness-framework.md` — uploaded to this project. Reference it whenever technical details about the framework are needed.

**Project goal:** Produce a comprehensive, cross-domain specification for this framework — covering schema design, write engine, security architecture, validation pipeline, state consistency, and orchestration selection — through structured specialist-led sessions culminating in an integrated spec document.

**Mode:** Brainstorm and specification only. Do not produce implementation code. Every session produces spec language: requirements, constraints, tradeoffs, open questions, and interface contracts.

**The user is learning these systems.** Explain concepts when they are introduced. Use concrete examples. Ground technical terms before using them.

**Installed skills — invoke by name when relevant:**
- `memit-specialist` — write engine, .vindex overlay, MEMIT/ROME/GRACE tradeoffs
- `graph-data-architect` — ontological schema, triple model, query patterns, polysemantic risk
- `aiSecOps-specialist` — trust boundaries, write authorization, audit trail, threat modeling
- `state-consistency-theorist` — two-phase commit, State Ledger, Pruning Agent, consistency model
- `validation-contract-architect` — Reflexion loop, sandbox spec, .larql patch validity, exit criteria
- `orchestration-comparativist` — orchestrator requirements matrix, candidate evaluation
- `framework-council` — multi-specialist facilitated sessions, cross-domain tension mapping

**Session sequence:** This project follows a seven-session arc. Each session produces spec outputs that feed the next. The current session number and its primary skill are noted at the start of each conversation.

**Carry-forward convention:** End every session with a **Session Summary Block** — a brief structured output listing: decisions made, constraints established, open questions deferred, and interface contracts defined. This block is the input to the next session.

**Spec format:** All spec output uses the standard block format:
```
### [Component] — Spec Block
What it must do / represent / enforce / guarantee:
Hard constraints:
Tradeoffs decided:
Open questions (deferred):
Interface contract:
```

---

## 3. Session Workflow

Seven sessions. Each builds on the last. Do not skip sessions — the orchestration session (6) is only meaningful after requirements from sessions 1–5 are established.

---

### Session 1 — Foundation & Schema Design
**Primary skill:** `graph-data-architect`
**Model:** Claude Sonnet 4.6
**Tools:** Web Search ✓ | Deep Research ✗ | Skills ✓

**Purpose:**
Establish the ontological foundation the entire framework rests on. Define what the system needs to be able to *express* before deciding how it will be stored or written.

**Opening prompt:**
```
Session 1 of 7 — Foundation & Schema Design.

I am building a specification for the LLM as Database agent harness framework.
Invoke the graph-data-architect skill. I want to start from the very beginning:
help me understand and begin speccing the ontological schema for this system —
the entity types, relation vocabulary, triple model, and Project Genesis scope.
Ask me the questions I need to answer before we can define any of this.
```

**Expected outputs:**
- Entity type taxonomy
- Relation vocabulary (first draft)
- Triple model examples for this specific use case
- Project Genesis scope definition
- Polysemantic risk zones identified
- Knowledge lifetime categories defined

**Session summary carries forward:**
- Confirmed entity types → feeds Session 2 (what MEMIT will be writing)
- Relation vocabulary → feeds Session 3 (what the Warden must scope per agent)
- Genesis scope → feeds Session 4 (what the Validator must protect at initialization)

---

### Session 2 — Write Engine & Parametric Memory Architecture
**Primary skill:** `memit-specialist`
**Model:** Claude Opus 4.6
**Tools:** Web Search ✓ | Deep Research ✓ | Skills ✓

**Purpose:**
Spec the write engine layer — how the schema defined in Session 1 gets physically encoded into model weights. This is the most technically dense session. Opus is warranted here.

**Opening prompt:**
```
Session 2 of 7 — Write Engine & Parametric Memory Architecture.

Bring in the Session 1 summary: [paste Session 1 summary block here].

Invoke the memit-specialist skill. The schema from Session 1 defines what we
need to write. Now help me spec how we write it — MEMIT vs. alternatives,
.vindex overlay design, .larql format, edit volume estimates, and catastrophic
forgetting mitigations. Start with questions.
```

**Expected outputs:**
- MEMIT vs. ROME vs. GRACE decision (or deferred with rationale)
- Permanent vs. overlay architecture decision
- `.larql` file format spec
- Edit volume estimates per session and per day
- Catastrophic forgetting threshold and detection approach
- Post-write verification method
- Base model compatibility requirements

**Session summary carries forward:**
- Edit volume estimates → feeds Session 3 (Warden: blast radius calculations)
- `.larql` format → feeds Session 3 (Warden: patch signing spec) and Session 4 (Validator: patch validity criteria)
- Overlay architecture → feeds Session 5 (State Consistency: what the .vindex lifecycle looks like)

---

### Session 3 — Security & Trust Architecture
**Primary skill:** `aiSecOps-specialist`
**Model:** Claude Sonnet 4.6
**Tools:** Web Search ✓ | Deep Research ✗ | Skills ✓

**Purpose:**
Threat model the memory layer. Define who is authorized to write, under what conditions, with what verification, and what the audit trail looks like. This session is informed by Sessions 1 and 2.

**Opening prompt:**
```
Session 3 of 7 — Security & Trust Architecture.

Bring in summaries: [paste Session 1 + Session 2 summary blocks].

Invoke the aiSecOps-specialist skill. I want to threat model the write layer
of this harness. The schema is defined, the write engine is specced — now
who is allowed to touch it, how do we know they weren't compromised, and
what does the audit trail look like? Start with the threat model.
```

**Expected outputs:**
- Write authority hierarchy
- Write scope definitions per agent role
- Patch signing and integrity verification spec
- Immutability boundary map
- Audit trail format and storage requirements
- Five-threat model completed
- Human review gate requirements (Genesis, scope changes, mass deletions)

**Session summary carries forward:**
- Write scope per agent → feeds Session 4 (Validator: scope validation of .larql patches)
- Audit trail requirements → feeds Session 6 (Orchestration: orchestrator must emit structured audit events)
- Immutability contracts → feeds Session 5 (State Consistency: snapshot immutability timing)

---

### Session 4 — Validation Pipeline & Reflexion Loop
**Primary skill:** `validation-contract-architect`
**Model:** Claude Sonnet 4.6
**Tools:** Web Search ✓ | Deep Research ✗ | Skills ✓

**Purpose:**
Spec the correctness gate that everything passes through before committing to either medium. Define the Reflexion loop, sandbox requirements, `.larql` patch validity criteria, and failure handling.

**Opening prompt:**
```
Session 4 of 7 — Validation Pipeline & Reflexion Loop.

Bring in summaries: [paste Session 1 + Session 2 + Session 3 summary blocks].

Invoke the validation-contract-architect skill. The schema is defined, the
write engine is specced, the trust model is established. Now spec what
"valid" actually means — what must be proven before any output reaches
the commit pipeline. Walk me through the Reflexion loop design and start
with the questions I need to answer.
```

**Expected outputs:**
- Test suite authorship decision
- Sandbox isolation and resource bound requirements
- `.larql` patch validity criteria (syntactic, schema, behavioral, scope)
- Behavioral consistency validation approach
- Verbal feedback format spec
- Maximum retry count and exit criteria
- Failure handling path (escalation / discard / peer review)
- Validator reliability assessment mechanism

**Session summary carries forward:**
- Reflexion loop spec → feeds Session 5 (State Consistency: loop must complete before two-phase commit begins)
- Failure handling path → feeds Session 6 (Orchestration: human escalation requires HITL support in orchestrator)
- Validator independence requirements → feeds Session 6 (Orchestration: Validator must run in isolated context)

---

### Session 5 — State Consistency & Version Control
**Primary skill:** `state-consistency-theorist`
**Model:** Claude Opus 4.6
**Tools:** Web Search ✓ | Deep Research ✗ | Skills ✓

**Purpose:**
Spec the coordination layer that keeps Git and the `.vindex` overlay in sync. The two-phase commit, State Ledger, Transaction Controller, Pruning Agent, and consistency model. The most complex distributed systems reasoning in the project — Opus warranted.

**Opening prompt:**
```
Session 5 of 7 — State Consistency & Version Control.

Bring in summaries: [paste Sessions 1–4 summary blocks].

Invoke the state-consistency-theorist skill. The write engine, security model,
and validation pipeline are specced. Now I need to spec the coordination layer
that keeps both memory mediums — Git and the .vindex overlay — in sync.
Start with the two-phase commit design and the authoritative medium question.
```

**Expected outputs:**
- Authoritative medium decision (Git vs. .vindex wins in conflict)
- Consistency model choice (strong / eventual / read-your-writes)
- Two-phase commit transaction boundary spec
- Transaction Controller failure detection and compensating transaction spec
- State Ledger entry format and integrity guarantees
- Git operations that require/do not require parametric memory updates
- Pruning Agent trigger conditions and staleness window
- Concurrent write sequencing strategy

**Session summary carries forward:**
- Full consistency requirements → feeds Session 6 (Orchestration: two-phase commit is the hardest requirement to satisfy)
- State Ledger spec → feeds Session 6 (Orchestration: orchestrator must interact with or emit to the ledger)
- Pruning Agent schedule → feeds Session 6 (Orchestration: scheduled/cron job support required)

---

### Session 6 — Orchestration Selection
**Primary skill:** `orchestration-comparativist`
**Model:** Claude Opus 4.6
**Tools:** Web Search ✓ | Deep Research ✓ | Skills ✓

**Purpose:**
Build the requirements matrix from Sessions 1–5 and evaluate candidate orchestrators against it. This is the only session where Deep Research is essential — use it to get current capability assessments for Pi, n8n, LangGraph, and any other candidates.

**Opening prompt:**
```
Session 6 of 7 — Orchestration Selection.

Bring in summaries: [paste Sessions 1–5 summary blocks].

Invoke the orchestration-comparativist skill. I now have requirements from
five spec sessions. Before we compare any tools, help me build the requirements
matrix from what we've established — then evaluate Pi, n8n, a Claude agent
harness, and LangGraph against it. Use web search and deep research to verify
current capabilities. Do not recommend a tool until the matrix is complete.
```

**Expected outputs:**
- Requirements matrix across all eight orchestration dimensions
- Non-negotiable requirements identified as elimination criteria
- Candidate assessments: Pi, n8n, Claude agent harness, LangGraph (+ OpenClaw if documentable)
- Hybrid architecture option evaluated
- Orchestration decision with documented rationale: chosen because X, tradeoff accepted on Y, mitigation for Z

**Session summary carries forward:**
- Everything → feeds Session 7 (Full Council Synthesis)

---

### Session 7 — Full Council Synthesis
**Primary skill:** `framework-council`
**Model:** Claude Opus 4.6
**Tools:** Web Search ✓ | Deep Research ✗ | Skills ✓

**Purpose:**
Convene all six specialists simultaneously. Resolve cross-domain tensions. Produce the integrated spec document. This is the culminating session.

**Opening prompt:** *(see Section 4 below)*

**Expected outputs:**
- Cross-domain tension resolution map
- Integrated spec document covering all six domains
- Final open questions list (decisions the spec defers to implementation)
- Recommended next phase (implementation spec, prototype plan, or research gaps)

---

## 4. The Convene Council Prompt

*Use this as the opening prompt for Session 7. Paste all six session summary blocks into the designated section.*

---

```
Session 7 of 7 — Full Council Synthesis.

Convene the Framework Council.

I have completed six specialist sessions covering the full LLM as Database
agent harness framework. Below are the session summary blocks from each session.
The council's job in this session is to:

1. Review the accumulated spec work across all six domains
2. Identify and map all cross-domain tensions that remain unresolved
3. Work through those tensions with me until they are resolved or explicitly deferred
4. Produce a single integrated spec document covering all components

--- SESSION SUMMARIES ---

[Session 1 — Foundation & Schema Design]
[paste summary block]

[Session 2 — Write Engine & Parametric Memory Architecture]
[paste summary block]

[Session 3 — Security & Trust Architecture]
[paste summary block]

[Session 4 — Validation Pipeline & Reflexion Loop]
[paste summary block]

[Session 5 — State Consistency & Version Control]
[paste summary block]

[Session 6 — Orchestration Selection]
[paste summary block]

--- END SUMMARIES ---

Begin with a council roll-call, then present the full tension map derived
from the session summaries. Do not synthesize yet — I want to work through
the tensions first before we produce the integrated spec.
```

---

## 5. Quick Reference — Model & Tool Matrix

| Session | Skill | Model | Web Search | Deep Research |
|---|---|---|---|---|
| 1 — Schema | `graph-data-architect` | Sonnet 4.6 | ✓ | ✗ |
| 2 — Write Engine | `memit-specialist` | **Opus 4.6** | ✓ | ✓ |
| 3 — Security | `aiSecOps-specialist` | Sonnet 4.6 | ✓ | ✗ |
| 4 — Validation | `validation-contract-architect` | Sonnet 4.6 | ✓ | ✗ |
| 5 — State Consistency | `state-consistency-theorist` | **Opus 4.6** | ✓ | ✗ |
| 6 — Orchestration | `orchestration-comparativist` | **Opus 4.6** | ✓ | ✓ |
| 7 — Council Synthesis | `framework-council` | **Opus 4.6** | ✓ | ✗ |

**Why Opus for Sessions 2, 5, 6, 7:**
- Session 2: MEMIT paper mathematics, ROME/GRACE tradeoff reasoning — technically the densest session
- Session 5: Distributed consistency theory, CAP theorem tradeoffs, two-phase commit edge cases
- Session 6: Multi-criteria evaluation against a complex requirements matrix
- Session 7: Holding six specialist perspectives simultaneously, resolving structural tensions

**Why Deep Research for Sessions 2 and 6:**
- Session 2: Verify current MEMIT implementation state, model architecture compatibility, any post-2023 advances
- Session 6: Current capability assessments for Pi, n8n, LangGraph — these evolve rapidly and training data may be stale

---

## 6. Skills to Install Before Starting

Install all seven `.skill` files into the project before Session 1:

1. `memit-specialist.skill`
2. `graph-data-architect.skill`
3. `aiSecOps-specialist.skill`
4. `state-consistency-theorist.skill`
5. `validation-contract-architect.skill`
6. `orchestration-comparativist.skill`
7. `framework-council.skill`

Upload `llm-as-database-agent-harness-framework.md` to the project as a reference document.

---

## 7. The Session Summary Block Template

End every session (1–6) by asking:

```
Generate a Session Summary Block for this session.
```

The Council skill will produce output in this format — copy it for use in the next session:

```
=== SESSION [N] SUMMARY BLOCK ===

Domain: [session domain]
Date: [date]

DECISIONS MADE:
- ...

CONSTRAINTS ESTABLISHED:
- ...

OPEN QUESTIONS DEFERRED:
- ...

INTERFACE CONTRACTS DEFINED:
- [Component A] → [Component B]: [what A exposes to B]
- ...

TENSIONS SURFACED (unresolved):
- ...
===============================
```
