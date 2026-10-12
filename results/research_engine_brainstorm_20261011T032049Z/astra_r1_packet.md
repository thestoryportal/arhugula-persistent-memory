# Astra review r1 — research-engine design (before any phase-1 build brief)

You are the program's independent cross-family reviewer. Work read-only. Do not edit, create or run anything except read/search commands.

## Context

This repo is the "LLM-as-Database" research program: it tests whether a spec for storing facts in model weights (MEMIT-style edits) is buildable (the "F1 determination"). Its governance lives in `CLAUDE.md`, `DISCIPLINE.md`, `EXPERIMENT_RUNBOOK.md` §0.3, `CORPUS/`, `docs/program_state.json`, `docs/AUTORESEARCH.md`, `docs/MATHLAB_STEP4_PREREG.md`, and `tools/closeout_check.py`.

The operator and a brainstorming agent designed a "research engine": an ontology over the program's records plus two rebuildable query copies (DuckDB for measurements, Neo4j for connections), agent tools, LabViz views, and adapters to MathLab, InfraNodus and AutoResearch. The operator approved the written design at 2026-10-11 04:23:51 UTC.

- Design: `results/research_engine_brainstorm_20261011T032049Z/design.md` (sha256 aa09563f092b6da8e01f900339720ee5cb46397cd3f5b98649f949de728dc6df)
- Operator's exact decisions: `results/research_engine_brainstorm_20261011T032049Z/decisions_log.md`
- The designer's self-review: `results/research_engine_brainstorm_20261011T032049Z/review_notes.md`

Nothing has been built. MAESTRO (the orchestrator) will next write a narrow phase-1 build brief (design.md lines 227–239). This review decides whether the design is sound enough to brief from, and what that brief must contain.

## Scope

The operator's choices are settled and are theirs to make: the three goals, DuckDB + Neo4j with Git as authority, agents as first-class users, the HIL rule for experiments and resource contention, guided AutoResearch mode as a new reviewed capability, and the five phases. Do not argue for different choices. Do flag a choice only if it, as written, conflicts with a binding repo rule or makes a stated acceptance check impossible to meet.

Review for:

1. **Conflicts with binding repo rules.** Anything in the design that would let work bypass or weaken: the close-out gate, Astra promote gates, frozen preregistrations, storage discipline (CLAUDE.md "Storage discipline"), the AutoResearch isolation contract, the MathLab step-4 stop, or operator-only decisions (deletions, spend, frozen-prereg amendments).
2. **Authority model gaps.** Places where agent operations (stage closeouts, request approvals, submit links, resume work) could turn into execution or record changes without the stated approval, or where "existing manager covers this workload" is undefined enough to be abused.
3. **Phase-1 testability.** Whether the phase-1 acceptance checks (design.md:233, :239) can actually fail, who produces the "independent expected answers", and what would count as a phase-1 failure.
4. **Internal contradictions or unbuildable statements**, including the two-database generation/manifest scheme (design.md:119).
5. **Missing items for the phase-1 brief** beyond the list at design.md:262–270.

## Deliverable

Write your verdict as Markdown to stdout (it is saved as the output file). Exactly this shape:

```
# Astra r1 verdict — research-engine design
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## Findings
F1. [severity: blocking|condition|note] <one-sentence defect>. Evidence: design.md:<line> vs <repo file>:<line>. Consequence: <what goes wrong>.
...
## Conditions for the phase-1 brief
C1. <a requirement the brief must contain, stated so MAESTRO can check it was met>
...
## What I checked and did not check
```

Each finding cites a design.md line and, where it claims a conflict, the repo file and line you read. A finding you could not ground in a read source is labelled `note` and says so.

Do NOT produce findings like: "Consider adding more tests", "Neo4j may be overkill; DuckDB alone could suffice", "Ensure security best practices are followed", or a rewritten design. The first and third cannot be checked; the second re-argues a settled operator choice; the fourth is not a review.
