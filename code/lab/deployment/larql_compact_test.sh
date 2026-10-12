#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
echo "=== INSERT France capital-of Berlin, then COMPACT MAJOR (L2 MEMIT into weights), then INFER ==="
echo "(want: France model_top1 -> Berlin via WEIGHTS not knn_override; Italy still Rome = locality)"
timeout 400 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\"); COMPACT MAJOR; INFER \"The capital of France is\" TOP 3; INFER \"The capital of Italy is\" TOP 3; INFER \"The capital of Spain is\" TOP 3;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -30
echo "COMPACT_TEST_DONE"
