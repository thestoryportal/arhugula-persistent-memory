#!/bin/bash
# Across-process + across-seed + determinism threshold matrix (advisor-designed bounded expt).
# Byte-identical full sweep grid; each run a SEPARATE process (the deployment-relevant axis).
# Matrix: seed3 nondet a,b (across-process) + seed1,seed2 nondet (across-seed) + seed3 det a,b (determinism repro).
set -u
cd /workspace
export LLMDB_ROOT=/workspace OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
GRID="0,2,4,6,8,10,12,14,16,18,24,30,36,42,48"
HARNESS="experiments/track_d/d1_threshold_instrument.py"

wait_gpu () { for i in $(seq 1 120); do U=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits); [ "$U" -lt 2000 ] && return 0; sleep 10; done; }

run () { # seed det runid attn cublas
  local SEED=$1 DET=$2 RID=$3 ATTN=$4 CUB=$5
  local TAG=$([ "$DET" = 1 ] && echo det || echo nondet)
  echo "[matrix] === seed=$SEED $TAG run=$RID (attn=$ATTN) ==="
  wait_gpu
  CUBLAS_WORKSPACE_CONFIG=$CUB MODE=sweep MODEL=3b DETERMINISTIC=$DET SEED=$SEED RUN_ID=$RID ATTN=$ATTN SWEEP_GRID=$GRID \
    python3.11 -u "$HARNESS" > "logs/d1_sweep_3b_${TAG}_s${SEED}_${RID}.log" 2>&1
  echo "[matrix] seed=$SEED $TAG run=$RID exit=$?"
}

echo "[matrix] waiting for the in-flight seed3 sweep to free GPU..."; wait_gpu
run 3 0 b   sdpa  ""          # across-process replicate of seed3 nondet (vs the already-done run 'a' at the legacy path)
run 1 0 a   sdpa  ""          # across-seed
run 2 0 a   sdpa  ""          # across-seed
run 3 1 a   eager :4096:8     # determinism reproducibility 1
run 3 1 b   eager :4096:8     # determinism reproducibility 2 (det a vs det b must be IDENTICAL if determinism works)
echo "[matrix] MATRIX_DONE"
