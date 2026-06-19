#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
infer(){ timeout 90 target/release/larql lql "$1" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate|Inference trace|Using:|^$' | grep -aiE 'Predictions|^   1\.|Inserted|allocated|mode:|Auto-patch|SAVE|REMOVE|Applied|Removed' | head -4; }
echo "=== B: COMPOSE overlay install, ALPHA sweep (find non-corrupting strength) ==="
for A in 0.1 0.3 0.5 1.0; do
  echo "--- ALPHA=$A: France capital-of Berlin (COMPOSE) ---"
  infer "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\") MODE = COMPOSE ALPHA $A; INFER \"The capital of France is the city of\" TOP 2; INFER \"The capital of Italy is the city of\" TOP 2;"
done
echo "=== B: GOVERNANCE — overlay rollback (frozen base) via BEGIN/SAVE/REMOVE PATCH ==="
echo "--- install + SAVE PATCH, read France, then REMOVE PATCH, read France (expect revert) ---"
timeout 150 target/release/larql lql "USE \"$V\"; BEGIN PATCH \"/dev/shm/france.vlp\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\") MODE = COMPOSE ALPHA 0.3; SAVE PATCH; INFER \"The capital of France is the city of\" TOP 2; REMOVE PATCH \"/dev/shm/france.vlp\"; INFER \"The capital of France is the city of\" TOP 2;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate|Inference trace|Using:|^$' | grep -aiE 'Predictions|^   1\.|Inserted|SAVE|REMOVE|Applied|Removed|patch|Auto' | head -10
echo "B_OVERLAY_DONE"
