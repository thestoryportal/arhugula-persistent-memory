#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
echo "waiting for --level all extract..."
n=0; until ! pgrep -x larql >/dev/null; do sleep 20; n=$((n+1)); [ $n -ge 90 ] && { echo "TIMEOUT"; break; }; done
echo "=== vindex files ==="; ls /dev/shm/qwen05_all.vindex/ 2>/dev/null | tr '\n' ' '; echo
echo "=== BIAS in manifest now? (Qwen2.5 q/k/v_proj.bias) ==="
grep -oE 'q_proj.bias|k_proj.bias|v_proj.bias' /dev/shm/qwen05_all.vindex/weight_manifest.json 2>/dev/null | sort | uniq -c
echo "bias-total: $(grep -oc bias /dev/shm/qwen05_all.vindex/weight_manifest.json 2>/dev/null)"
echo "=== CLEAN READ: run (generation) — expect Paris ==="
timeout 250 target/release/larql run /dev/shm/qwen05_all.vindex "The capital of France is" 2>&1 | tail -8
echo "=== INFER TOP 5 ==="
timeout 200 target/release/larql lql 'USE "/dev/shm/qwen05_all.vindex"; INFER "The capital of France is" TOP 5;' 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -12
echo "QWEN_ALL_TEST_DONE"
