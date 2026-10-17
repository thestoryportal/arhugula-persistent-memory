# Close-out rule
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

Operator, 2026-10-16, verbatim: "any upgrades, updates, feature adds to code are closed with these context updates where they are relevant in all related/relevant documents."

A change to any workflow tool or to the skill (a MAESTRO step, a ticket that changes a gate, a new allow rule, a new ledger event) is not closed until all four are current:
1. this guide (`_system/governance/TICKETS.md` and `_system/governance/tickets/`), and every other governance file that describes the changed part;
2. the CLAUDE.md routing row that reaches `TICKETS.md` (then regenerate the twins AGENTS.md and routing.md);
3. the skill (S/SKILL.md, S/references/worker.md, S/references/reviewer.md) where it describes the changed part;
4. the related memory files in MEM (listed in `TICKETS.md` § Pointers), updated in place, then targeted hygiene on the files the work touched.

Record the doc updates in the step's ledger row (the Step 325 install row says "docs pending: TICKETS.md (exit 5, tests row, test-edit-allow.json)"; that row stays open until they are written).

The tool works, the suite is green, and you will think *"docs after the next step; the code is the source of truth."* The code is the truth for the code. For the next session, the truth is what routing reaches: a feature that lives only in a script comment or a handoff is invisible to a successor that reads CLAUDE.md first, and it re-learns the trap at full price. "Ship small, document later" is right for a feature behind a flag; it is wrong here, because this workflow is run by agents who know only what the docs tell them. The memory drift in [G12] is what "later" looks like.

