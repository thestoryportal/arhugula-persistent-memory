#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
W="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
export LLMDB_ROOT="$W"
if [ "$#" -ne 1 ]; then
  echo "Usage: code/apps/mathlab/run_mathlab_harvest.sh experiments/ml/runs/<admission run>/admission.json" >&2
  exit 2
fi
# MathLab instrument runs: record ml (code/state/llmdb_records.py ML_RUNS).
RUN_DIR="$W/experiments/ml/runs/harvest_$(date -u +%Y%m%dT%H%M%SZ)_$$"
mkdir -p "$W/experiments/ml/runs"
mkdir "$RUN_DIR"
if "$W/.venv/bin/python" -B "$W/code/apps/mathlab/mathlab_admit.py" --kind harvest --admission "$1" --run-dir "$RUN_DIR" --step 1 --deadline-s 3600; then
  exec "$W/.venv/bin/python" -B "$W/code/apps/mathlab/mathlab_harvest.py" --admission "$1" --run-dir "$RUN_DIR"
else
  RC=$?
  echo "Harvest refused; admission staged at $RUN_DIR/admission.json" >&2
  exit "$RC"
fi
