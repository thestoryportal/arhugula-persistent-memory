#!/bin/bash
# Re-run the equivalence check after the prepare.py change (REFERENCE_RUN → the fence's two-number extract).
# Keeps the previous record beside it; writes a log; runs in a tmux session so it outlives any tool timeout.
set -euo pipefail
P=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
cd "$P"
cp -n experiments/c10r/runs/autoresearch_c10_equivalence_run/autoresearch_c10_equivalence.json experiments/c10r/runs/autoresearch_c10_equivalence_run/autoresearch_c10_equivalence_2026-10-06T0815.json || true
export LLMDB_ROOT="$P"
echo "equivalence check started $(date '+%H:%M:%S')" > experiments/c10r/runs/autoresearch_c10_equivalence_run/logs/autoresearch_c10_equivalence_rerun.log
.venv/bin/python code/lab/track_c/autoresearch_c10/check_equivalence.py >> experiments/c10r/runs/autoresearch_c10_equivalence_run/logs/autoresearch_c10_equivalence_rerun.log 2>&1
echo "equivalence check exit=$? at $(date '+%H:%M:%S')" >> experiments/c10r/runs/autoresearch_c10_equivalence_run/logs/autoresearch_c10_equivalence_rerun.log
