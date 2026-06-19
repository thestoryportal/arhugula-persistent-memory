#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
echo "=== IN-WEIGHT path: INSERT MODE=COMPOSE (L1/arch-A) -> COMPACT MAJOR (MEMIT into weights) -> INFER ==="
echo "(want: France model_top1 itself -> Berlin [WEIGHT edit, not knn_override]; Italy=Rome, Spain=Madrid [locality])"
timeout 500 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\") MODE = COMPOSE; COMPACT MAJOR; INFER \"The capital of France is\" TOP 3; INFER \"The capital of Italy is\" TOP 3; INFER \"The capital of Spain is\" TOP 3;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate|Inference trace' | tail -34
echo "COMPOSE_TEST_DONE"
