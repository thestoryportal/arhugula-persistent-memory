#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
W="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
export LLMDB_ROOT="$W"
if [ "$#" -lt 2 ]; then
  echo "Usage: code/apps/mathlab/run_mathlab_cpu.sh <notebook> <deadline_s> [notebook arguments]" >&2
  echo "Deadlines: m2 6540; m3 1800. Optional lead tail record: MATHLAB_ADMISSION." >&2
  exit 2
fi
NOTEBOOK="$1"; DEADLINE="$2"; shift 2
case "$NOTEBOOK:$DEADLINE" in
  code/apps/mathlab/m2_solve_repro.py:6540|"$W/code/apps/mathlab/m2_solve_repro.py:6540") STEP=2;;
  code/apps/mathlab/m3_calibration.py:1800|"$W/code/apps/mathlab/m3_calibration.py:1800") STEP=3;;
  *) echo "Refused: notebook or hard deadline differs from the preregistration" >&2; exit 3;;
esac
# MathLab instrument runs: record ml (code/state/llmdb_records.py ML_RUNS).
mkdir -p "$W/experiments/ml/runs"
RUN_DIR="$W/experiments/ml/runs/m${STEP}_$(date -u +%Y%m%dT%H%M%SZ)_$$"
mkdir "$RUN_DIR"
ADMIT_ARGS=(--kind cpu --run-dir "$RUN_DIR" --step "$STEP" --deadline-s "$DEADLINE")
if [ -n "${MATHLAB_ADMISSION:-}" ]; then ADMIT_ARGS+=(--admission "$MATHLAB_ADMISSION"); fi
if "$W/.venv/bin/python" -B "$W/code/apps/mathlab/mathlab_admit.py" "${ADMIT_ARGS[@]}"; then
  exec "$W/.venv/bin/python" -B "$W/code/apps/mathlab/mathlab_cpu_runner.py" "$NOTEBOOK" "$DEADLINE" --run-dir "$RUN_DIR" "$@"
else
  RC=$?
  echo "CPU notebook refused; admission staged at $RUN_DIR/admission.json" >&2
  exit "$RC"
fi
