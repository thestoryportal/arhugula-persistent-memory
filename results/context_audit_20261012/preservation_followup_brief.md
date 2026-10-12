# codexcps2 — preservation follow-up: where R2's exact-match rule came from

You are a read-only successor to codexcps, which stopped at its context limit. Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` (W). `B` = `results/compute_storage_brainstorm_20261011T054507Z`. `A` = `results/context_audit_20261012`.

## Why this matters
The operator asked whether a context-preservation failure caused R2 (the two-Mac shared-drive design) to fail. Their recollection: "both Macs pull from the memit drive but the requirement was that they had to match in some particular way." That is the exact-match rule at `B/r2_round7_decisions.md:28–34` (D3): every child process of a science run is registered ahead of time and observed processes must match that list exactly. R2 stalled because the list could never be completed (`B/r2_sweep_report.md:72–80`). The operator wants to know whether that requirement came from a real need or from a stale, conflicting or over-broad instruction.

## Read first (only these, then targeted spans)
1. `A/cps_handoff.md`: your predecessor's done/in-progress/remaining list. Its "Remaining" steps 3–5 are your task.
2. `A/operator_hypothesis_worktree_vs_main.md`: settled evidence. Cite it; do not re-derive it.
3. `A/PRESERVATION.md` §1 (lines 8–67) and its last line.

## Already settled — do not reopen
- The Intel had no memit access in the R2 design; only the M3 executor touched memit (`B/shared_disk_clearance_freeze_v11.md:27,34,37`; `B/shared_disk_clearance_contract_v1_1.md:24–26`; operator HW1 choice 2 "Separate copies" at `B/decisions_log.md:47–53`).
- R2 attribution counts: 48 findings, a6/b8/c34 (PRESERVATION.md:65).

## Your task
1. Trace the exact-match rule backward to its first source: the earliest design text, Astra finding, operator ruling or instruction file that demanded exact registration/matching of descendants. Keep three things distinct: the original contract's population/closure obligations (`B/shared_disk_clearance_contract_v1_1.md`), D3's recipe declaration (`B/r2_round7_decisions.md:28–34`), and the later A1 amendment (`B/r2_round8_decisions.md:9–19`). A later date is not an origin.
2. Decide whether a stale or over-broad instruction drove it. The candidate named so far is the GPU-gate note `memory_mirror/gpu-gate-refuses-any-venv-python.md` (SYNTHESIS unit N16 under group F12, `A/SYNTHESIS.md:108`). Causation needs a builder or reviewer input (brief, packet or verdict, with file:line) that actually used such a note. With no such input, write "unproved" and say what the rule followed from instead.
3. Only if you meet it on the way: any frozen profile naming the folder the M3 executor would copy from (bare main folder, this worktree, or whole volume). Do not search for this exhaustively; report "not frozen" when no frozen profile names it.

## Output
Append one section to `A/PRESERVATION.md`, titled `## 6. Origin of the exact-match rule (follow-up)`, at most 13 lines, so the file stays at or under 250 lines. Every claim carries file:line. End the section with one plain-language sentence an operator can read without jargon. Update the final `Lines:` value. Edit no other file.

Bad section 6 lines, for calibration:
- "The rule arose from careful safety design." No file:line, so it is not evidence.
- "Stale GPU-gate notes drove the rule." This names no input that used them, so it asserts causation without showing it.
- A re-tally of the 48 findings, or a restated point from the hypothesis file. Those are already settled.

## Limits
Read-only apart from that one append. No commits, network, graft, rclone, SSH, transfers, deletions or project Python. `/usr/bin/python3 -B` and stdlib reads are fine. Other sessions are writing in this worktree: touch only your section.

## Context directive (binding; restate it in any handoff)
Manage your context for every handoff. You cannot see your own percentage, so MAESTRO's watcher will send a stop at 45% left. On that message, or on any context compaction: start no new searches; write done/in-progress/remaining work, exact paths and open risks to `A/cps2_handoff.md`; reply `CPS2 HANDOFF`. New work starts only at ≥60% left; a successor takes over by ≤40%.

## Reply
Finish with exactly one of: `CPS2 READY A/PRESERVATION.md`, `CPS2 BLOCKED <reason>`, `CPS2 HANDOFF`.
