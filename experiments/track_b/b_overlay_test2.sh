#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
flt(){ grep -aviE 'gate=|F[0-9]+ +gate|Inference trace|Using:|^$|trace-guided|walk FFN'; }
echo "=== B-clean: COMPOSE ALPHA=0.3 overlay install — edit + locality (Italy/Spain should stay) ==="
timeout 150 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\") MODE = COMPOSE ALPHA 0.3; INFER \"The capital of France is the city of\" TOP 2; INFER \"The capital of Italy is the city of\" TOP 2; INFER \"The capital of Spain is the city of\" TOP 2;" 2>&1 | flt | grep -aiE 'Inserted|^   [12]\.' | head -8
echo "=== B-governance: APPLY saved .vlp on frozen base -> read -> REMOVE -> read (rollback) ==="
ls -la /dev/shm/france.vlp 2>/dev/null | awk '{print "vlp:",$5,$NF}'
timeout 150 target/release/larql lql "USE \"$V\"; APPLY PATCH \"/dev/shm/france.vlp\"; INFER \"The capital of France is the city of\" TOP 2; REMOVE PATCH \"/dev/shm/france.vlp\"; INFER \"The capital of France is the city of\" TOP 2;" 2>&1 | flt | grep -aiE 'Applied|Removed|Loaded|^   1\.|patch|Error' | head -10
echo "B2_DONE"
