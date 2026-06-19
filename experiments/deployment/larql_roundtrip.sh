#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 RAYON_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
echo "waiting for inference convert..."
n=0; until ! pgrep -x larql >/dev/null; do sleep 20; n=$((n+1)); [ $n -ge 90 ] && { echo "TIMEOUT 30min"; break; }; done
echo "=== inference vindex ready? ==="
ls /dev/shm/qwen05_inf.vindex/ 2>/dev/null | tr '\n' ' '; echo
tail -2 $LLMDB_ROOT/logs/larql_convert_inf.log
echo "=== STEP 1 — READ (INFER) the original fact ==="
timeout 200 target/release/larql lql 'USE "/dev/shm/qwen05_inf.vindex"; INFER "The capital of France is" TOP 5;' 2>&1 | tail -14
echo "=== STEP 2+3 — WRITE (INSERT France capital->Berlin) then RE-READ, one session ==="
timeout 250 target/release/larql lql 'USE "/dev/shm/qwen05_inf.vindex"; INFER "The capital of France is" TOP 3; INSERT INTO EDGES (entity, relation, target) VALUES ("France", "capital-of", "Berlin"); INFER "The capital of France is" TOP 3;' 2>&1 | tail -22
echo "ROUNDTRIP_DONE"
