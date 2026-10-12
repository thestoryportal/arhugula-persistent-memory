---
status: ready-for-maestro-host-run
branch: worktree-c10k-route-a
files_modified:
  - tools/dashboard_queue.py
  - tools/test_dashboard_queue.py
  - tools/dashboard_queue_tab.sh
  - tools/team_dashboard.sh
---

# Q1 saved context

Done: typed queue parser, pure renderer, per-tick live detection, five-second resilient loop, idempotent tab launcher, exact team integration, host runner. All 15 tests GREEN with prior RED evidence. Report and source SHA-256s: README.md and after_sha256.json beside this note. Final logs: green.log, green.exit. Original criterion bodies are unchanged.

Decisions: bind the read-only source to the script's checkout to avoid inherited LLMDB_ROOT=main; use explicit default tmux socket; fresh observations with visible denial/parse errors; shared pure BUSY_RE and cell_width only; no cached live pane reader. No live mutation, science, .venv, commit, push or staging.

Remaining: MAESTRO runs `bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh'`, reviews its receipt outputs, then installs the queue tab. Actual host tmux lifecycle and GPU admission are UNVERIFIED. Existing q1check servers cause refusal, and unrelated GPU blockers can legitimately keep admission closed.

Context directive (binding, operator 2026-10-10): watch “Context N% left.” Start a new piece of work only at >=60% left. At <=40% left, or on any “Context compacted,” stop starting work, append a handoff into README.md with done/half-done, exact paths, SHA-256s, test state and a single next step, and reply “Q1 HANDOFF.” Every handoff restates this directive.
