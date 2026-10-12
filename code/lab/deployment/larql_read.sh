#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export HF_HOME=$LLMDB_ROOT/hf_cache
echo "waiting for convert to finish..."
n=0; until ! pgrep -x larql >/dev/null; do sleep 15; n=$((n+1)); [ $n -ge 48 ] && { echo "TIMEOUT 12min"; break; }; done
echo "=== convert done? vindex contents ==="
ls -la /dev/shm/qwen05.vindex/ 2>/dev/null | awk '{print $5,$NF}'
tail -3 $LLMDB_ROOT/logs/larql_convert2.log
echo "=== register vindex (link) ==="
target/release/larql link /dev/shm/qwen05.vindex 2>&1 | tail -3
echo "=== list ==="
target/release/larql list 2>&1 | tail -8
echo "=== READ A: LQL WALK (semantic graph read) ==="
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 timeout 150 target/release/larql lql 'USE "/dev/shm/qwen05.vindex"; WALK "The capital of France is" TOP 5;' 2>&1 | tail -15
echo "=== READ B: DESCRIBE ==="
OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 timeout 120 target/release/larql lql 'USE "/dev/shm/qwen05.vindex"; DESCRIBE "Paris";' 2>&1 | tail -12
echo "T24_READ_DONE"
