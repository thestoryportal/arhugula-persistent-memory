#!/bin/bash
# D-C10w-oracle: oracle measurement, not a route. Exactly one stage per invocation.
if [ "$#" -ne 1 ]; then
    echo "HALT: usage: tools/run_c10w_stage.sh <stage>" >&2
    exit 2
fi
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)" || exit 2
WORKTREE="$(cd -- "$SCRIPT_DIR/.." && pwd)" || exit 2
if [ -n "${LLMDB_ROOT+x}" ] && [ "$LLMDB_ROOT" != "$WORKTREE" ]; then
    echo "HALT: INVALID-ENVIRONMENT: LLMDB_ROOT is not this worktree" >&2
    exit 2
fi
export LLMDB_ROOT="$WORKTREE" PYTHONUNBUFFERED=1
cd -- "$WORKTREE" || exit 2
exec "$WORKTREE/.venv/bin/python" -B "$WORKTREE/experiments/track_c/c10w_oracle_step0.py" dispatch "$1"
