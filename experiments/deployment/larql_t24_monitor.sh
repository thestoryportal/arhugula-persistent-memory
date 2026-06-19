#!/bin/bash
LLMDB_ROOT="${LLMDB_ROOT:-/workspace}"
cd $LLMDB_ROOT/external_prior_art/larql
PID=$(pgrep -f 'larql convert' | head -1)
if [ -n "$PID" ]; then
  u1=$(awk '{print $14}' /proc/$PID/stat); st1=$(awk '{print $15}' /proc/$PID/stat); sleep 6
  u2=$(awk '{print $14}' /proc/$PID/stat); st2=$(awk '{print $15}' /proc/$PID/stat)
  echo "PROGRESS CHECK: utime_delta=$((u2-u1)) stime_delta=$((st2-st1)) threads=$(awk '{print $20}' /proc/$PID/stat) (utime>>stime = real compute)"
fi
echo "waiting for convert..."
n=0
until ! pgrep -f 'larql convert' >/dev/null; do sleep 15; n=$((n+1)); [ $n -ge 60 ] && { echo "TIMEOUT 15min"; break; }; done
echo "=== convert ended; vindex files ==="
ls -la $LLMDB_ROOT/qwen05.vindex/ 2>/dev/null | awk '{print $5,$NF}'
tail -4 $LLMDB_ROOT/logs/larql_convert.log
echo "=== READ 1: larql run ==="
HF_HOME=$LLMDB_ROOT/hf_cache timeout 150 target/release/larql run $LLMDB_ROOT/qwen05.vindex "The capital of France is" 2>&1 | tail -12
echo "=== READ 2: LQL WALK (semantic read) ==="
HF_HOME=$LLMDB_ROOT/hf_cache timeout 120 target/release/larql lql 'USE f"{LLMDB_ROOT}/qwen05.vindex"; WALK "The capital of France is" TOP 5;' 2>&1 | tail -12
echo "T24_DONE"
