# Skill Team Design Decisions
### LLM as Database — Agent Harness Specification

*This document captures the key design decisions made during the skill development session (Session 0). Reference this before modifying any skill or adding new skills to the team. Full session transcript is archived in the Skill Development project.*

---

## The Six-Skill Team

The specialist team was deliberately designed — not all initial candidates were kept, and several were refocused. Here is what was decided and why.

---

### Decision 1 — Four Skills Became Six

**Initial candidates proposed:**
1. Tensor & Model Ops Engineer (MEMIT Specialist)
2. Graph Data Architect
3. Distributed Systems Architect (Concurrency Manager)
4. AISecOps Specialist (The Warden)

**What changed:**
Two gaps were identified that none of the four skills clearly owned:

- The **Reflexion / Validation Loop** — the PyTest deterministic sandbox, Actor-Critic pattern, and Coder → Test → Fail → Fix → Retry cycle. This is the heartbeat of the harness. No proposed skill fully owned it.
- The **Orchestration Decision** — the framework explicitly leaves orchestration open (Pi, n8n, Claude harness, etc.). A skill was needed to evaluate candidates against requirements rather than advocate for any one approach.

Two skills were added: **Validation Contract Architect** and **Orchestration Comparativist**.

---

### Decision 2 — "Distributed Systems Architect" Refocused

**Original scope:** Concurrency management, distributed state, multi-agent coordination.

**Problem:** Too broad. It conflated two distinct concerns that need separate ownership:
- State synchronization between Git and the `.vindex` overlay (a consistency concern)
- General concurrency and distributed systems architecture (an implementation concern)

**Resolution:** Narrowed to **State Consistency Theorist** — scoped specifically to keeping two memory mediums in sync: the Git repository and the parametric memory layer. Orchestration-agnostic. Produces consistency guarantees and transaction boundary definitions, not implementation architecture.

---

### Decision 3 — "Pi Orchestrator Architect" Was Rejected

**Proposed at:** Initial skill design review.

**Reason rejected:** Pi as orchestrator is not a finalized decision. Building a specialist skill around Pi would bake in an architectural choice the spec is supposed to evaluate. A "Pi Architect" skill would produce Pi-flavored spec output regardless of whether Pi is the right choice.

**Resolution:** The **Orchestration Comparativist** fills this role — explicitly agnostic, evaluates all candidates (Pi, n8n, Claude agent harness, LangGraph, OpenClaw) against requirements derived from the other five skills.

**Standing rule:** If orchestration is finalized during spec work, a dedicated orchestrator implementation skill may be appropriate at that point — but not before.

---

### Decision 4 — Security and Correctness Are Separate Skills

**The risk:** The AISecOps Specialist (Warden) and the Validation Contract Architect cover adjacent territory — both gate what reaches the write engine. They could have been merged.

**Why they were kept separate:**

The Warden owns **authorization and integrity** — *who* is allowed to write, *whether the patch was tampered with*, *what the audit trail looks like*. It does not care whether the output is logically correct.

The Validation Contract Architect owns **correctness** — *whether the output is right* — before any trust question is asked. It does not care who produced the output.

The distinction matters in spec sessions: a patch can be correctly authorized (passes the Warden) but logically wrong (fails the Validator), or logically correct but unauthorized (fails the Warden, never reaches the Validator). Merging the skills would obscure this boundary.

**Standing rule:** Keep these skills' ownership scopes clean. The Warden never evaluates logical correctness. The Validator never evaluates authorization.

---

### Decision 5 — Brainstorm and Spec Only. No Implementation Code.

**All six skills share one hard constraint:** They do not produce implementation code.

They produce:
- Spec language: requirements, constraints, tradeoffs, open questions
- Interface contracts between components
- Decision rationale with explicit tradeoffs documented
- Structured open questions for deferral

**Why this constraint exists:** The framework is theoretical and the implementation approach is not yet decided. Skills that produce implementation code would make implicit choices about language, platform, and tooling that the spec process is supposed to keep open. Implementation skills can be built after orchestration and architecture decisions are finalized.

---

### Decision 6 — The Framework Council Is a Meta-Skill, Not a Seventh Specialist

The `framework-council` skill does not own a domain. It is a facilitator that:
- Embodies all six specialists as distinct voices
- Routes topics to the relevant specialist(s)
- Surfaces and holds cross-domain tensions without resolving them prematurely
- Synthesizes multi-specialist discussion into integrated spec blocks

**It is not a replacement for the individual skills.** For deep single-domain work, use the individual skill directly. Use the council when cross-domain tensions need to be explored or when a synthesis pass is needed.

**In any council session, all seven skills should be installed** — the council skill drives the session, the individual skills provide depth when the council goes deep on a specific domain.

---

## The Six Pre-Mapped Tensions

These structural tensions were identified during skill design and are baked into the council skill. They will surface in almost every council session. Do not treat them as bugs — they are the load-bearing design decisions the spec must resolve.

| ID | Tension | Specialists |
|---|---|---|
| T1 | Immutability vs. mutability window during writes | Warden vs. State Consistency Theorist |
| T2 | Write volume vs. edit locality guarantees | Graph Data Architect vs. MEMIT Specialist |
| T3 | Validator independence vs. test coverage at scale | Validation Contract Architect vs. Orchestration Comparativist |
| T4 | Audit completeness vs. write throughput | Warden vs. State Consistency Theorist + MEMIT Specialist |
| T5 | Schema stability vs. agent autonomy in patch generation | Graph Data Architect vs. Orchestration Comparativist |
| T6 | Genesis comprehensiveness vs. Genesis brittleness | Graph Data Architect vs. MEMIT Specialist |

---

## Skill Modification Rules

If a skill needs to be modified during iteration:

1. **Do not change a skill's ownership scope** without reviewing all interface contracts that reference it. Scope changes cascade.
2. **Do not merge skills** unless both ownership domains have been fully specced and the boundary between them is confirmed unnecessary.
3. **Do not add implementation guidance** to any skill body. The brainstorm/spec-only constraint applies to all six.
4. **Document the change** in `skill-refinement-log-v1.md` with rationale before reinstalling.
5. **Run a council interface contract review** after any skill modification that touches an interface contract definition.

---

## Adding New Skills

If the framework scope expands to require a new specialist:

1. Verify the new domain is not already covered by an existing skill's scope
2. Define the ownership boundary explicitly — what does this skill own that no existing skill owns?
3. Define the interface contracts with all six existing skills
4. Apply the brainstorm/spec-only constraint
5. Add the new skill's pre-mapped tensions to the council skill
6. Document the addition in this file

---

*Last updated: Session 0 — Skill Development*
*Full session transcript: archived in LLM as Database — Skill Development project*
