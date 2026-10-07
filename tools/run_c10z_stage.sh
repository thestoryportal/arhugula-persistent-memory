#!/bin/bash
# D-C10z-astra: one externally requested stage per invocation; no shell stage chain.
STAGE="${1-}"
case "$STAGE" in 0|1|2|3) ;; *) echo 'usage: run_c10z_stage.sh <0|1|2|3>' >&2; exit 2 ;; esac
[ "$#" -eq 1 ] || { echo 'exactly one stage argument required' >&2; exit 2; }
W="$(cd "$(dirname "$0")/.." && pwd)" || exit 2
export LLMDB_ROOT="$W" PYTHONUNBUFFERED=1
cd "$W" || exit 2
OUT_DIR="${C10Z_OUT_DIR:-$W/results/c10z_astra}"
export C10Z_OUT_DIR="$OUT_DIR"
mkdir -p "$OUT_DIR/logs" || exit 2
LOG="$OUT_DIR/logs/stage_$STAGE.log"
[ ! -e "$LOG" ] || { echo "refusing existing stage log: $LOG" >&2; exit 2; }
"$W/.venv/bin/python" -B "$W/experiments/track_c/c10z_astra_arms.py" "$STAGE" > "$LOG" 2>&1
rc=$?
echo "STAGE_EXIT=$rc" >> "$LOG"
exit "$rc"
