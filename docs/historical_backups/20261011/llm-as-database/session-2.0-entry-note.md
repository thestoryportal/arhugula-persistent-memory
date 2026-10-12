# Session 2.0 Entry Note — Target Model Commitment

> **Workstream:** 1 — Empirical POC Scoping (post-v1.2 sealed spec)
> **Session:** 2.0 — Target Model Commitment
> **Position in arc:** Opens after Session 1.7 (Workstream 1 closing synthesis); precedes Stage 0 corpus authorship and Stage 1 (MEMIT-COMPAT-PROTO-1) execution.
> **Primary skill:** `memit-specialist`
> **Closes:** OQ-WS1-1 (target model commitment, inherited from Session 1.1)

---

## Curation Notice — Read Before Beginning

The project knowledge base has been deliberately curated for this session. Four downstream calibration protocols have been removed from the active KB:

- `memit-drift-proto-1.md` (Stage 2 — drift / capacity)
- `epsilon-calib-proto-1.md` (Stage 3a — ε / M / bucket calibration)
- `compaction-probe-calib-proto-1.md` (Stage 3b — compaction probe sampling)
- `judge-calib-proto-1.md` (Stage 3c — judge-model threshold)

These were removed because they consume the target model commitment rather than inform it. If you find yourself reaching for downstream criteria — drift sweep ranges, ε cell counts, compaction corpus size, judge-model latency budgets — to evaluate a candidate, that is a signal you have left the session's scope. Stay upstream.

The only criteria that apply in this session are SC-1..SC-9 from `memit-compat-proto-1.md` §1. They are repeated in the prompt below for convenience but the canonical source is the protocol document in the KB.

`judge-calib-proto-1.md` in particular has been removed because it carries SC-style judge-model selection criteria that are similar in shape to but distinct from SC-1..SC-9. If a question about the judge model arises, defer it — judge selection is a downstream session that runs after target commitment.

## Active KB Documents (7)

The following remain in the project KB and are the intended context for this session:

| Document | Role in this session |
|---|---|
| `memit-compat-proto-1.md` | **Primary input.** Source of SC-1..SC-9 selection criteria. |
| `llm-as-database-agent-harness-framework.md` | Paradigm grounding. Anchors SC-6 literature search. |
| `llm-as-database-v1_2-integrated-spec.md` | Appendix A deployment preconditions; A11 break-glass custodian rule; §22.8 cross-model non-portability. |
| `write-engine-poc-scope.md` | Establishes why target commitment matters and what it gates. |
| `poc-execution-plan-and-spec-revision-rule.md` | Workstream 1 closing synthesis; staging context. |
| `tension-map-v5.md` | Cross-reference. Pre-T2 (Write Volume vs. Edit Locality) is the only directly relevant tension. |
| `gap-backlog-v5.md` | Cross-reference. GAP-1 (empirical thresholds) and GAP-2 (MEMIT architecture compatibility) are the relevant gap entries. |

## Tools Expected in This Session

- **Web search** — required for SC-6 (documented MEMIT precedent) and current model release status.
- **Web fetch** — required for license text retrieval (SC-9), MEMIT paper / repo retrieval (SC-6), and the candidate catalog site provided in the prompt.
- **Past conversation search** — use on first turn if any model name appearing in prior chats comes up. The skill includes this tool by default.
- **Deep Research** — recommended if the operator wants a thorough survey before commitment; not required for v1 candidate field.

Tools that do NOT apply: image search, maps, weather, calendar, email, drive, recipes, places.

## Output Discipline

The session output is a **recommendation**, not a commitment. The operator commits in a follow-up. Do not commit on the operator's behalf. Do not extend into Stage 0 corpus drafting in this session, even if the operator commits inline — Stage 0 is its own session with its own KB curation.

---

*Entry note ends. The fresh session prompt follows in `session-2.0-prompt.md`.*
