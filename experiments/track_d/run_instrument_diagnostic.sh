#!/bin/bash
# Phase-0 §8.7 instrument diagnostic orchestrator (3B). Waits for the in-flight
# b1 seeds345 run to free the GPU, then: (1) non-det 5-repeat (picks unstable k),
# (2) det 2-repeat reusing that k (CUBLAS env set; may throw -> halt diagnostic, non-fatal).
set -u
cd /workspace
export LLMDB_ROOT=/workspace OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
B1PID=359412

echo "[orch] waiting for b1 PID $B1PID + GPU to free..."
while kill -0 $B1PID 2>/dev/null; do sleep 20; done
# wait until <2GB used (model fully released)
for i in $(seq 1 60); do
  USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
  echo "[orch] gpu used=${USED}MiB"; [ "$USED" -lt 2000 ] && break; sleep 10
done

echo "[orch] === NON-DET diagnostic (picks k, 5 repeats) ==="
MODEL=3b DETERMINISTIC=0 N_REPEAT=5 SEED=3 PICK_GRID=18,24,30,36 \
  python3.11 -u experiments/track_d/d1_threshold_instrument.py > logs/d1_instr_3b_nondet.log 2>&1
NDRC=$?
echo "[orch] non-det exit=$NDRC"
if [ $NDRC -ne 0 ]; then echo "[orch] non-det FAILED; stopping (need its picked k)."; exit 1; fi

KPICK=$(python3.11 -c "import json;print(json.load(open('results/d1_instrument_variance_diagnostic_3b_nondet.json'))['k_unstable'])")
echo "[orch] picked k=$KPICK -> DET run"

echo "[orch] === DET diagnostic (k=$KPICK, 2 repeats, deterministic) ==="
CUBLAS_WORKSPACE_CONFIG=:4096:8 MODEL=3b DETERMINISTIC=1 N_REPEAT=2 SEED=3 K_PICK=$KPICK ATTN=eager \
  python3.11 -u experiments/track_d/d1_threshold_instrument.py > logs/d1_instr_3b_det.log 2>&1
echo "[orch] det exit=$? (non-fatal: a throw is the infra finding)"
echo "[orch] ALL_DONE"
