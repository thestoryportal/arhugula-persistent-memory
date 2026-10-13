# Astra review — research-engine phase-1 spec, r1 (before any answer-key or builder session)

You are the program's independent cross-family reviewer. Work read-only: read and search only; do not create, edit or run anything else.

## Context
You reviewed the approved research-engine design in r1 (`results/research_engine_brainstorm_20261011T032049Z/astra_r1_verdict.md`: GO-WITH-CONDITIONS, C1-C9 for the phase-1 brief). The operator then fixed phase-1 limits (`results/research_engine_brainstorm_20261011T032049Z/operator_phase1_choices_20261011.md`: Neo4j Community via Homebrew on this Mac; <=5 GB disk on memit; <=2 GB Neo4j memory; anytime; no model/GPU). A drafting session (SPEC1) wrote the phase-1 spec:

- Subject: `results/research_engine_phase1_20261011/phase1_spec.md` (sha256 09cdd80e3a365d02969cbf559440326fb69916847f5916eba27642564307e0a0). Nothing in it has been built, installed or run.

If you pass it, MAESTRO freezes it and dispatches an answer-key author (KEY1), then you review that key, then a separate builder works test-first against it.

## Review for
1. Does each of C1-C9 hold in the spec as written (section 2's mapping table), or is a mapping nominal: the named AC cannot actually catch the failure the condition targets?
2. Are the 20 ACs binary and checkable, and could any pass while the slice is wrong?
3. Do the five proposed chains (section 4) fit their categories, given the cited CORPUS/result files? Spot-check at least two citations.
4. Specific points MAESTRO wants judged:
   a. GPU gate: the program's GPU admission gate refuses launches while any non-exempt python runs (see CLAUDE.md LAW 1 and `memory_mirror/gpu-gate-refuses-any-venv-python.md`). Phase 1 runs a `.venv-research-engine` Python 3.12 and a Java Neo4j "anytime". Does the spec need a rule for not blocking a pending gated science launch?
   b. Section 7 keeps every generation in one Neo4j Community database, separated by a `generation_id` property. Does that meet C4's immutable-generation requirement, or only by convention?
   c. The spec replaces the design's LinkML recommendation with a JSON vocabulary and uses Neo4j's HTTP API with stdlib instead of a driver. Acceptable implementation choices, or a conflict with the approved design (`results/research_engine_brainstorm_20261011T032049Z/design.md:111`)?
   d. Section 11 says "nice+10" while the main tmux server already runs at niceness 10 (`memory_mirror/background-shell-niceness-10.md`). Is the priority rule stated unambiguously?
5. Anything that conflicts with binding repo rules (CLAUDE.md storage discipline, deletion approval, close-out gate, frozen-prereg rules).

## Deliverable
Markdown to stdout, exactly this shape:
```
# Astra spec r1 verdict — research-engine phase 1
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## Findings
S1. [severity: blocking|condition|note] <one-sentence defect>. Evidence: phase1_spec.md:<line> vs <file>:<line>. Consequence: <what goes wrong>.
## Required spec changes before freeze
R1. <exact change, checkable>
## What I checked and did not check
```
Ground every finding in a line you read; an ungrounded concern is a `note` and says so.

Do NOT produce: "consider adding more tests", stylistic rewrites of the spec, re-arguments of the operator's choices (DuckDB + Neo4j, Neo4j on the Mac, the budget), or a rewritten spec.
