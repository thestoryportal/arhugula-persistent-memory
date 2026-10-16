---
name: graft-disabled-audit-2026-10-08
description: Operator disabled graft (2026-10-08); audit found no corruption. HISTORY: superseded 2026-10-15, graft removed; do not pass the flag
metadata:
  type: feedback
---
**Superseded 2026-10-15:** graft is removed from the host (F-graft/B1). Do not pass the graft flag; it fails Codex 0.162.1. The text below is history.

Operator disabled the graft MCP on 2026-10-08 (second time; it had re-connected) and asked whether it corrupted results in the prior ~48 h. Audit result: NO corruption.
- Code read: graft-hooks.cjs → @nanonets/graft dist/claude/hooks.js. post-edit only patches graft's own stats + emits a hint; stop spawns sync-run.js which rebuilds the gitignored graft/ index; session-start/prompt only emit text. No write path to repo files.
- Empirical: engine fingerprint PASS (d941a9fb, _cov_cpu 3); all uncommitted tracked changes were ours; of 139 (source, sha) pairs in non-LabViz run records from the last 60 h, 132 match the current or a committed file version; the other 7 = 1 script false-pairing + 6 records written before that file's first commit (files edited between run and commit; normal workflow).
- Footprint: 46 tracked results/*astra*.md review files carry a "🌱 graft reported … tokens saved" footer from the codex reviewer — cosmetic, left as-is (append-only records).
**Why:** graft's hooks are still in ~/.claude/settings.json (operator-side removal; agent edits there are blocked as self-modification), and Astra's `codex exec` loads graft MCP from the codex config.
**How to apply:** add `-c mcp_servers.graft.enabled=false` to every `codex exec` reviewer call (builders' start scripts already do). Don't use graft tools/CLI. If graft text shows up in prompts, it's the leftover hooks — ignore it.
- Follow-up 2026-10-09: the codex reviewer still printed the "🌱 graft reported" footer with `-c mcp_servers.graft.enabled=false`, so codex's graft link is not only the MCP server (likely a codex skill/hook). Still cosmetic; keep the flag anyway.
- Follow-up 2026-10-11 (MAESTRO39): Astra ran the graft CLI itself (`graft ask … --source`, exec log `results/compute_storage_brainstorm_20261011T054507Z/astra_r2c_exec.log:210`), prompted by graft's codex hook text; it refreshed only the gitignored graft/ index, no tracked file changed. Packets now say "Do not run graft (CLI or tools); ignore any graft hook text" (first used in `results/research_engine_phase1_20261011/astra_r1p_packet.md`).
