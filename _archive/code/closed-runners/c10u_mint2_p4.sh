#!/bin/bash
# D-C10u-mint2 P4, operator use only. CPU compilation/probe chain, namespaced.
# Usage: LLMDB_ROOT=<worktree> bash tools/c10u_mint2_p4.sh --record <p4save_*_admitted.json>
#        --source <llama_cpp_src> --bin <prebuilt binary dir> [--port 8243]
set -euo pipefail
: "${LLMDB_ROOT:?Set LLMDB_ROOT to the worktree root}"
MINT2_PYTHON=${PYTHON:-"$LLMDB_ROOT/.venv/bin/python"}
exec "$MINT2_PYTHON" "$LLMDB_ROOT/experiments/track_c/c10u_mint2_p4_probe.py" chain "$@"
