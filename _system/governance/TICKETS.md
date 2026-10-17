# TICKETS — the atomic-ticket workflow, from an approved plan to merged master
Job: how one approved plan becomes many atomic tickets that fresh builders implement in parallel lanes and that ship, train and land without hand work; which tool owns each stage; the traps each stage has already sprung; the gaps still open.
Routed from the root CLAUDE.md (twin: AGENTS.md). Written 2026-10-16 from the sweep `L/w1opt/staged/tickets-doc/INVENTORY.md` (the audit, one row per component; this guide is for the moment of decision). The guide (this router plus `tickets/*.md`) is the registry of every tag (`[R12]`, `[G7]`): a tag is defined by the rule or gap it is attached to, found with the grep under "Where to read next". INVENTORY.md is only the frozen sweep evidence for R1-R53 and G1-G20; later tags exist only in the guide.

This file is the router. It holds the goal, the belt and where to read next. Every rule lives in one file under `_system/governance/tickets/`.
Read `tickets/00-roots-and-roles.md` once per session (it defines the roots L, M, S, W, TD, MEM, HO and who does what), then only the file for your stage or moment.

## The goal

Operator, 2026-10-16, verbatim: "The goal of all of this work is that Atomic tickets complete end to end in no more than 15 minutes."

- Measure every ticket from its `dispatch` row to its `merged` row and report the minutes against 15, in every estimate and every report. A ticket over 15 gets its cause written down (`tickets/ledger-and-metrics.md`), because an overrun with no named cause comes back on the next ticket.
- Merges land in one `train.sh` CI cycle for all ready PRs. Never estimate, plan or run merges one after another: ten PRs that reach `ready` together land in one candidate, one CI run, one gate call (train.sh:2-5). The sentence *"T319 lands, then T320, then..."* prices the train at ten times its real cost, and the plan built on it is wrong before it starts.

## The belt

Picture the workflow as one conveyor belt: plan → cut → lane → brief → build → ship → train → land → release. Each station is a script, and each script leaves marks that the next station reads: a ledger row, a `verdict.sha` written before the review, a ready marker, a lock dir, a recorded merge-base, an allow file with a reason in it.

A step done by hand takes the ticket off the belt. A `git commit` in a lane, a `gh pr merge`, a `cp` over a live tool, a verdict file edited after the fact: each one skips the station that writes the marks. The next station then either refuses, which is the cheap outcome, or trusts a mark that no longer describes the ticket, which is the expensive one: a GO reused for code nobody reviewed, a cleanup that never ran, a merge on master with no name on it. None of these raise an alarm. They surface days later as a mystery that the next session spends hours on.

So at every stage, ask first: *which station owns this, and am I about to do its job by hand?* The answer is almost always "a script owns it; run the script."

## Where to read next

| Stage | File | Station | Reads → writes |
|---|---|---|---|
| 1 Plan | `tickets/01-plan.md` | MAESTRO by hand; the operator approves | operator approval → `TD/PLAN.md` |
| 2 Cut | `tickets/02-cut.md` | `tickets.py cut --base` | `TD/PLAN.md`, base checkout → `TD/tickets/<T>.json` |
| 3 Lanes | `tickets/03-lanes.md` | `mklane.sh` | ticket → lane `tk-<T>`, `dispatch` row |
| 4 Briefs | `tickets/04-briefs.md` | MAESTRO, from `L/w1opt/brief-template.md` | ticket, template → `TD/brief-<T>.md` |
| 5 Build | `tickets/05-build.md` | builder (`S/references/worker.md`); MAESTRO verifies | brief, lane → lane edits, `verified` row |
| 6 Fix rounds | `tickets/06-fix-rounds.md` | MAESTRO ruling; a fresh fixer per round | review files → `RULING.md`, `TD/brief-<T>-fix<n>.md` |
| 7 Ship | `tickets/07-ship.md` | `ship.sh` (cwd M, background) | lane, ticket, SPECREF/SEAM → PR, `TD/reviews/<T>/`, ready marker |
| 8 Train | `tickets/08-train.md` | `train.sh` (cwd M, background) | ready markers → merged PRs, cleanup rows |
| 9 Land | `tickets/09-land.md` | the merge gate; `L/land.sh` with TRAIN=0 | PR → master |
| 10 Release | `tickets/10-release.md` | train.sh or ship.sh cleanup; hygiene | merged PR → lane and branch removed |
| 11 MAESTRO steps | `tickets/11-maestro-steps.md` | `install_staged.sh` (5b by hand) | staged `.new` → live tool, `install` row |

| Moment | File |
|---|---|
| Once per session, before any stage: roots and names, who does what (old § Roots and names, § Who does what) | `tickets/00-roots-and-roles.md` |
| Setting a variable for a test or a one-off (old § Environment overrides) | `tickets/env-overrides.md` |
| A ledger row, METRICS.md, counting landed tickets, the dashboard tab (old § Ledger and metrics) | `tickets/ledger-and-metrics.md` |
| Disk floor, a permission prompt, a session reset, watchers, zsh traps (old § Disk, permissions, sessions) | `tickets/disk-permissions-sessions.md` |
| Closing any change to a tool, the skill or a rule (old § Close-out rule) | `tickets/close-out.md` |
| A known defect or open gap (old § Known gaps) | `tickets/gaps.md` |
| Running the trace check, or a new path a script names (old § Path index) | `tickets/path-index.md` |
| The generic method: plan format, cut, ready, close (the skill; this guide adds the house stations) | `/atomic-ticketizer` (Claude) or `$atomic-ticketizer` (Codex), `S/SKILL.md` |

A tag cited elsewhere lives where its rule or gap lives: `grep -n '\[R<n>\]' _system/governance/tickets/*.md`.

## Pointers (rules that live elsewhere)

- Merging, the gate, and the cooperative rule: `_system/governance/MERGING.md`.
- Context management for MAESTRO and every team session: `_system/governance/OPERATING-MODEL.md` § Context management.
- Bulk writes, downloads, deletions: `_system/governance/STORAGE.md`.
- Halt discipline and correctness gates: `_system/governance/DISCIPLINE.md`.
- Codex builders and tools: `_system/governance/CODEX.md`.
- Memory that holds this workflow's lessons (update in place, never append a duplicate): MEM/lean-ticket-lane-traps.md, MEM/lean-tools-ship-and-cut-base.md, MEM/atomic-units-parallel-worktree-lanes.md, MEM/workflow-change-closes-with-doc-updates.md, MEM/icm21-part2-and-workflow-approvals.md, MEM/check-gpu-counts-team-pythons.md, MEM/fix-lane-evidence-fills-memit.md, MEM/merge-gate-first-use-learnings.md, MEM/build-gate-allow-rules.md, MEM/atomic-unit-builder-lifecycle.md, MEM/rerun-builder-tests-host-tmpdir.md, MEM/review-substitution-is-exception.md, MEM/one-shot-run-needs-real-scale-dry-run.md.
- Handoffs: HO/HANDOFF-STEP70.md is the latest (it supersedes HO/HANDOFF-STEP69.md and HO/HANDOFF-STEP68.md; STEP50-67 before them). A handoff carries a session's state; a rule found in one belongs in this guide or in memory, where the next session will look.
- Wave-1 filesystem rulings: `L/part2/extra-fd-binding.md` and `L/part2/reviews/<T>/RULING.md` (for example `L/part2/reviews/T201/RULING.md`).

## Recap

- The goal: every ticket dispatch to merged in 15 minutes; all ready PRs land in one train, never serially.
- The belt: plan (frozen-suite check, size rule) → `tickets.py cut --base` → `mklane.sh` → brief from `L/w1opt/brief-template.md` → builder (worker.md, revert check) → MAESTRO verifies → `ship.sh` (1a guard mutants, 1b test-file edits, close, pre-review, Astra under admission, ready marker) → `train.sh` from cwd M (batch gate, cleanup, hygiene) → ledger and METRICS.md.
- Hand work drops the ticket off the belt: no hand commit (re-ship), no hand merge (the gate), no `cp` over a tool (install_staged.sh), no edit to a pinned review file (a new note).
- Allow files and rulings are MAESTRO's alone, each with its reason.
- A tool change closes only when this guide, the routing row, the skill and the memory say what is now true.
