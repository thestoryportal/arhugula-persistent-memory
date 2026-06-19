#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 HF_HOME=$LLMDB_ROOT/hf_cache
echo "waiting for gemma vindex pull..."
n=0; until ! pgrep -x larql >/dev/null; do sleep 20; n=$((n+1)); [ $n -ge 90 ] && { echo "PULL TIMEOUT"; break; }; done
echo "=== pull done; cached vindexes ==="
target/release/larql list 2>&1 | tail -6
NAME=$(target/release/larql list 2>/dev/null | grep -ioE 'gemma[a-z0-9._-]*' | head -1)
echo "gemma vindex name: ${NAME:-?}"
echo "=== READ (clean generation): expect Paris ==="
timeout 400 target/release/larql run "$NAME" "The capital of France is" 2>&1 | tail -6
echo "=== ROUND-TRIP: INFER -> INSERT France capital->Berlin -> INFER (one session) ==="
timeout 500 target/release/larql lql "USE \"$NAME\"; INFER \"The capital of France is\" TOP 5; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\"); INFER \"The capital of France is\" TOP 5;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -30
echo "GEMMA_ROUNDTRIP_DONE"
