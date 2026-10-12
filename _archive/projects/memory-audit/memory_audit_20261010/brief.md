# Task: audit memory notes for an LLM research program (read-only)

Repo (git worktree, read-only for you): /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
Notes live in `memory_mirror/` (one fact per file, YAML frontmatter `name` / `description` / `metadata.type`). Its index is `memory_mirror/MEMORY.md`. These notes are read by Claude and Codex agents at session start and steer their behavior, so a stale or wrong note silently misdirects future work. Today is 2026-10-10.

The operator asked: "Run an additional audit on the current MEMORY.md to identify stale, duplicate, bloated, incorrect, misleading, etc entries."

## Your files
Audit exactly the notes listed in FILELIST (one filename per line, relative to memory_mirror/). Read each note in full.

## For each note, decide one verdict
- KEEP — accurate, current, distinct.
- STALE — describes a state that has since changed (a status, a "next step", a resume point, a pod/RunPod-era path or hardware, a tool that was replaced). Name what changed.
- INCORRECT — a factual claim contradicted by the repo now.
- MISLEADING — true in isolation but would steer an agent wrong today (e.g. an old rule superseded by a newer one).
- DUPLICATE — same fact as another note (name the other file; say which should survive).
- BLOATED — the note carries session narrative, long logs, or detail that belongs in CORPUS/runbook/checkpoint rather than a one-fact memory (give its size and what to cut).
- HISTORICAL — accurate record of a closed experiment/decision, no longer action-guiding; candidate to keep but de-index or move to an archive section.
- FORMAT — frontmatter missing/invalid (no `---` block, no `name:`/`description:`, or type not under `metadata:`).
A note can carry two verdicts (e.g. STALE+BLOATED).

## Verify, do not trust
Check each load-bearing claim against the repo: `EXPERIMENT_RUNBOOK.md` (§0.3 state, §5 decisions), `SESSION_CHECKPOINT.md` top, `CORPUS/` (numbered docs 00–61), `docs/program_state.json`, `CLAUDE.md`, `AGENTS.md`, `tools/`, `.claude/settings.json`, git log. Cite file:line or the command you ran. Context facts you may use as leads (verify before relying): the program moved from a RunPod 4090 pod (/workspace) to the operator's MacBook M3 Pro (MPS, no CUDA) on 2026-10-03 (D-HW-1); the engine is vendored at memit_dry_run/memit (fingerprint d941a9fb…); ASTRA/C10Z closed as D-C10z-a4 (CORPUS/61); MathLab STOPPED (CORPUS/60); NEW-1 is in progress (results/mathlab_staging/); Claude orchestrates Codex builders in tmux, GPT-6-Astra via `codex exec` is the binding reviewer; rclone remote `gdrive:` authorized 2026-10-10; the launchd backup still mirrors to ~/Backups/memit (Drive replacement being built).

## Output
Write a markdown table to OUTFILE with columns: `file | bytes | verdict(s) | evidence (file:line or command) | proposed action | replacement description (≤150 chars, only if the note should stay)`. Proposed action is one of: keep / fix-text (say what) / merge-into <file> / de-index (historical) / retire (stale beyond repair). Then a short "Cross-note findings" section (duplicates or contradictions spanning notes). Then reply with only: the OUTFILE path and verdict counts.

Do NOT: edit, move or delete any file (read-only audit); mark a note STALE or INCORRECT without a citation; judge a note by length alone; output prose summaries instead of the table.
Bad row (no evidence): `foo.md | 2100 | STALE | seems old | retire |`
Good row: `foo.md | 2100 | STALE | says GPU=4090; CLAUDE.md:3 says M3 Pro MPS since 2026-10-03 | fix-text: hardware line | GPU gate … on M3 Pro`
