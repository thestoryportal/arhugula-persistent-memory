#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
echo "=== baseline read (France capital) ==="
timeout 150 target/release/larql lql "USE \"$V\"; INFER \"The capital of France is\" TOP 3;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -8
echo "=== INSERT France capital-of Berlin (L1 alloc) then INFER (read back) ==="
timeout 200 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\"); INFER \"The capital of France is\" TOP 3; INFER \"The capital of Italy is\" TOP 3;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate' | tail -20
echo "WRITE_TEST_DONE"
