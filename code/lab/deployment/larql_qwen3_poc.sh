#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 RAYON_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
echo "=== STEP 1: pull Qwen3-0.6B (ungated) ==="
target/release/larql model pull Qwen/Qwen3-0.6B 2>&1 | tail -4
SNAP=$(find $LLMDB_ROOT/hf_cache/hub/models--Qwen--Qwen3-0.6B/snapshots -maxdepth 1 -mindepth 1 -type d 2>/dev/null | head -1)
echo "snapshot: $SNAP"
[ -z "$SNAP" ] && { echo "PULL FAILED"; exit 1; }
echo "=== STEP 2: stage on tmpfs ==="
rm -rf /dev/shm/qwen3_model /dev/shm/qwen3.vindex; mkdir -p /dev/shm/qwen3_model
cp -rL "$SNAP"/. /dev/shm/qwen3_model/ && du -sh /dev/shm/qwen3_model
grep -oE '"(model_type|architectures)"[^,]*' /dev/shm/qwen3_model/config.json | head
echo "=== STEP 3: extract --level all (thread-capped) ==="
target/release/larql convert safetensors-to-vindex --output /dev/shm/qwen3.vindex --level all --f16 /dev/shm/qwen3_model 2>&1 | tail -4
echo "=== manifest: qk_norm / bias present? ==="
echo "qk_norm entries: $(grep -oc 'q_norm\|k_norm' /dev/shm/qwen3.vindex/weight_manifest.json 2>/dev/null)"
echo "bias entries: $(grep -oc bias /dev/shm/qwen3.vindex/weight_manifest.json 2>/dev/null)"
echo "=== STEP 4: POSITIVE CONTROL — run, expect Paris ==="
timeout 200 target/release/larql run /dev/shm/qwen3.vindex "The capital of France is" 2>&1 | tail -8
echo "=== INFER TOP 5 ==="
timeout 150 target/release/larql lql 'USE "/dev/shm/qwen3.vindex"; INFER "The capital of France is" TOP 5;' 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -12
echo "QWEN3_POC_DONE"
