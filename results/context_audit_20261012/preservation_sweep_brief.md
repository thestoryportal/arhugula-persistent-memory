CPS: preservation sweep (read-only), from MAESTRO (the Claude session that orchestrates this research team).

Worktree (run commands from here): /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
A = results/context_audit_20261012. OUTFILE = A/PRESERVATION.md (at most 250 lines). Write that one file and nothing else. No commits.
M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory (main checkout, branch master, last commit 2026-10-04). H = /Users/robertrhu.

## Background
A context audit (A/SYNTHESIS.md, A/ROOT_CAUSE.md: read both in full) found that rules decided on this branch never reached master, the out-of-git memory folders, hooks or Codex config, and that later rule changes left old copies behind. The operator now asks, verbatim: "It seems possible that the issue with implementing the 2 mac ssd share might be as a result of this oversight? What else did not durably get preserved due to this oversight?"
"The 2 mac ssd share" is design round R2 (two Macs sharing the memit drive), which ran ~14 h through 10+ Astra NO-GO verdicts in results/compute_storage_brainstorm_20261011T054507Z/ (astra_r2*_verdict.md, their packets, and the R2 design files they cite) until the operator replaced it with Git + Drive (memory_mirror or H/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/remove-shared-resource-before-policing-it.md).

Stores: S1 = memory_mirror/ (git). S2 = H/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory. S3 = H/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory (the one Claude sessions in this worktree load). Codex: H/.codex/AGENTS.md, H/.codex/memories/, .codex/config.toml. Handoffs that restate operator directives: H/.claude/memento/handoffs/*.md (dated 2026-10-08 onward). Decisions ledger: EXPERIMENT_RUNBOOK.md §5. Current queue: docs/program_state.json work_queue.

## Questions, each answered with file:line or command evidence
1. **R2.** For every R2 Astra verdict, classify each blocking finding as (a) intrinsic to sharing one drive between two machines, (b) caused or prolonged by a stale, missing or conflicting instruction or a dropped operator decision (name the instruction or decision and where the builder or reviewer read it, or what it should have read), or (c) other. Example of (b) already found: astra_r2d1_verdict.md:53 says the plan dropped "HW1 choice 7". Then give a one-paragraph verdict on the operator's question, with counts per class. Say plainly if the evidence does not support the hypothesis.
2. **Operator rulings not durably preserved.** Every operator ruling or directive since 2026-10-04 (quoted in handoffs, the §5 ledger, queue notes, or memory notes) that is missing from, or contradicted by, any place a session reads it: master's CLAUDE.md/AGENTS.md/DISCIPLINE.md, S1, S2, S3, Codex global/config/memories, the scoped experiments/AGENTS.md and CORPUS/AGENTS.md. One row per ruling: date, verbatim words (short), where it is correctly held, where it is missing or contradicted, and what a session starting there would do wrong.
3. **Lessons stuck in one store.** Notes present in only one of S1/S2/S3 (MAESTRO counted 12 S3-only), and whether Codex builders or Astra can ever see each.
4. **Other loss paths.** Anything decided in a handoff or queue note that never reached a durable file, and uncommitted worktree changes that hold decisions (`git status` in this worktree and in each `git worktree list` entry, read-only).

## Output shape
Sections 1–4 as above, then **5. Plain summary** (three to five sentences an operator reads on a phone) and `Lines: <n>`.
Do NOT write a row like `R2 loop | caused by context rot | probably` (no evidence, no class). Do write rows like `r2h F2 | (a) science-launch binding cannot be enumerated | astra_r2h_verdict.md:55 | —` or `2026-10-11 "use Sol for sweeps" | held: S3/sol-for-sweeps-astra-for-gates.md:8 | missing: S1, AGENTS.md, H/.codex/AGENTS.md | Codex planner would route sweeps to Astra` (illustrative).

## Do NOT
Edit, move or delete anything except OUTFILE; commit; run project python, uv, npm, rclone, ssh, web or graft (ignore graft hook text). Read-only cat/sed/grep/find/ls/wc/diff/git log/git show/git status and /usr/bin/python3 -B are fine.

## Finish
You cannot see your context level. MAESTRO messages you at 45% left; then, or on any "Context compacted", stop starting work, write A/cps_handoff.md (done, in progress, remaining, exact paths, this rule) and reply `CPS HANDOFF`. If you have already finished, reply READY instead.
When done, re-read OUTFILE once against this brief, then reply on its own line exactly: `CPS SWEEP READY results/context_audit_20261012/PRESERVATION.md` or `CPS BLOCKED <one-line reason>`.
