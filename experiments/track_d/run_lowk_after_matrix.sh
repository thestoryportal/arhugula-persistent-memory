#!/bin/bash
set -u; cd /workspace
export LLMDB_ROOT=/workspace OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "[lowk-launch] waiting for MATRIX_DONE..."
for i in $(seq 1 240); do grep -q "MATRIX_DONE" logs/d1_matrix_orch.log 2>/dev/null && break; sleep 20; done
for i in $(seq 1 120); do U=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits); [ "$U" -lt 2000 ] && break; sleep 10; done
echo "[lowk-launch] launching low-k randomized-order (seed3, 12 orders)"
MODE=lowk MODEL=3b DETERMINISTIC=0 SEED=3 N_ORDERS=12 LOWK_GRID=4,6,8,10,12,14 \
  python3.11 -u experiments/track_d/d1_threshold_instrument.py > logs/d1_lowk_3b_s3.log 2>&1
echo "[lowk-launch] lowk exit=$? ; LOWK_LAUNCH_DONE"
