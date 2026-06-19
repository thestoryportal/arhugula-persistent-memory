#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
echo "=== extract vindex from OUR-edited Qwen3 weights ==="
rm -rf /dev/shm/qwen3_edited.vindex
target/release/larql convert safetensors-to-vindex --output /dev/shm/qwen3_edited.vindex --level all --f16 /dev/shm/qwen3_edited 2>&1 | tail -3
echo "=== LARQL serves the edit? run (expect Berlin for France) ==="
timeout 200 target/release/larql run /dev/shm/qwen3_edited.vindex "The capital of France is" 2>&1 | tail -6
echo "=== INFER France/Italy ==="
timeout 200 target/release/larql lql 'USE "/dev/shm/qwen3_edited.vindex"; INFER "The capital of France is" TOP 3; INFER "The capital of Italy is" TOP 3;' 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate|Inference trace' | tail -16
echo "DECOUPLE_SERVE_DONE"
