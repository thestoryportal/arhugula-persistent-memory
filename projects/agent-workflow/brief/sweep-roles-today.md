# Sweep brief: roles today (output: P/drafts/inventory/roles-today.md)

Read M/projects/agent-workflow/brief/sweep-common.md first. Its roots, hard rules, evidence rules and output form apply here.

## Task
Write a factual card for every agent role and every scripted station on the ticket belt and in the session lifecycle, as each works TODAY. Scope (charter, "Decisions in force"): the ticket belt "(plan → cut → lane → brief → build → fix → ship → train → land → release) and the session lifecycle (start, handoff, reset), for build tickets like waves 1-2". Science runs are out of scope.

MAESTRO gets a short card here (trigger, model, exit, outputs). Its full task list and the rules addressed to it belong to the maestro-tasks sweep: do not list MAESTRO's tasks or rules here.

## Start list (add every other role or station you find cited; give the citation)
- Agents: operator; MAESTRO; builder (Codex or Claude, one per ticket); fixer (one per fix round); pre-review (L/tools/prereview.sh); Astra (L/tools/astra.sh); prober (S/references/prober.md and its caller in L/tools/ship.sh); deletion-probe reviewer (MEM/deletion-probe-review-staged-acceptance.md); Fable reviewer; sweep and research subagents (P/brief/); interactive Codex brainstorm sessions (MEM/interactive-codex-brainstorm-sessions.md).
- Stations: S/scripts/tickets.py; every script in L/tools/ that is not a `.bak-*` (mklane.sh, mkfixbriefs.py, verify_ticket.sh, ship.sh, combined.sh, spot.sh, train.sh, install_staged.sh, reclaim.py, prereview.sh, astra.sh, test_ship.sh, test_train.sh, ticketizer, others); L/land.sh; W/mkbrief.py; the git hook named by `core.hooksPath` (`git -C M config core.hooksPath`); M/code/agents/context_watch.py; Memento `finalize-session`; M/code/state/build_index.py and render_state.py. For every other station that a belt doc or memory file names, follow the route rule in sweep-common. A station that no ICM route reaches, or that a belt doc marks as retired, is recorded as `OFF-ROUTE` or `RETIRED`, with the citation.
- Belt docs: M/_system/governance/TICKETS.md and M/_system/governance/tickets/01-plan.md through 10-release.md, close-out.md, ledger-and-metrics.md, disk-permissions-sessions.md. Rule files for agents: S/references/worker.md, reviewer.md, prober.md; W/brief-template.md; W/brief-template-fix.md; L/tools/template-brief-builder.md; L/tools/template-brief-fix.md.

## Sections
1. `## Belt map`: one table, one row per stage (plan, cut, lane, brief, build, fix, ship, train, land, release, session start, handoff, reset). Columns: stage | acting agent(s) | station(s) | input artifact (path) | output artifact (path) | next reader | doc citation.
2. `## Role cards`: one subsection per role or station. Use these fields, one line each. Write `not recorded (grep: <command>)` when a source does not give the field:
   route (the ICM hops from M/CLAUDE.md to this role's rule file or this station's script, or `OFF-ROUTE`) | trigger (who starts it, the exact command) | job | exit (what ends it, exit codes for stations) | inputs by path | context it is given (files the harness loads for it; files it is told to read, with the line that tells it) | tools, permissions and sandbox (Codex sandbox and approval flags; Claude allow and deny rules that name it) | skills it loads or is told to load | governance files it obeys | model and effort (the flag or config line that sets them) | outputs and their reader | what is measured today (which of `passed, exit_code, duration, tokens, cost` the ledger or METRICS records for it: cite TD/ledger.tsv:1 and M/_system/governance/tickets/ledger-and-metrics.md) | positive control (for a gate: a test or fixture that shows it rejects a known-bad input, cite it; else `none found` with the grep).
3. `## Rules addressed to each non-MAESTRO role`: one table per agent role, from its rule file and brief template. Columns: rule (quote, at most 20 words) | path:line | ENFORCED or INTERPRETED | the enforcing line, if ENFORCED | surface.
4. `## Incidents (uncoded)`: per sweep-common rule 5. Sources: M/_system/governance/tickets/gaps.md, MEM/*.md "trap" lines, HO/HANDOFF-STEP70.md through the latest ("Traps found"), TD/reviews/. Cover every role you carded; at most 60 rows.

## Acceptance
Every role and station in the start list has a card, or a line in `## Missing or dead paths` that says why not. Every card field has a citation or `not recorded (grep: ...)`. Every rule row has a class and a surface.

## The trap in this sweep
Partway through, you will have read worker.md and a handoff that summarises it, and you will think "the handoff says builders get X; I'll cite that, it's faster." Stop there. The handoff is a REPORT. Open the brief template or script that hands the builder X, and cite that line. If none exists, the fact is "REPORT only", and it goes under `## Disagreements` or `## UNVERIFIED`.
