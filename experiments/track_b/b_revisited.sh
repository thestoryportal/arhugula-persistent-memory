#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
V=/dev/shm/qwen3.vindex
flt(){ grep -aviE 'gate=|F[0-9]+ +gate|Inference trace|Using:|^$|trace-guided|walk FFN'; }
echo "##### TEST 1: does ROUTE VERIFY fix the KNN cross-entity bleed? #####"
echo "--- KNN insert France->Berlin, then INFER France/Italy/Spain WITHOUT route verify (baseline bleed) ---"
timeout 120 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\"); INFER \"The capital of France is the city of\" TOP 2; INFER \"The capital of Italy is the city of\" TOP 2; INFER \"The capital of Spain is the city of\" TOP 2;" 2>&1 | flt | grep -aiE 'Inserted|^   1\.' | head -6
echo "--- SAME but WITH ROUTE VERIFY ---"
timeout 120 target/release/larql lql "USE \"$V\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\"); INFER \"The capital of France is the city of\" ROUTE VERIFY TOP 2; INFER \"The capital of Italy is the city of\" ROUTE VERIFY TOP 2; INFER \"The capital of Spain is the city of\" ROUTE VERIFY TOP 2;" 2>&1 | flt | grep -aiE '^   1\.' | head -6
echo "##### TEST 2: COMPACT (MEMIT) with PRESERVE edges (controls as L1 edges) #####"
timeout 250 target/release/larql lql "USE \"$V\"; BEGIN PATCH \"/dev/shm/p2.vlp\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"capital-of\", \"Berlin\") MODE = COMPOSE; INSERT INTO EDGES (entity, relation, target) VALUES (\"Italy\", \"capital-of\", \"Rome\") MODE = COMPOSE; INSERT INTO EDGES (entity, relation, target) VALUES (\"Spain\", \"capital-of\", \"Madrid\") MODE = COMPOSE; COMPACT MAJOR; INFER \"The capital of France is the city of\" TOP 2; INFER \"The capital of Italy is the city of\" TOP 2; INFER \"The capital of Spain is the city of\" TOP 2;" 2>&1 | flt | grep -aiE 'COMPACT|Skipped|MEMIT|solver|^   1\.|Inserted' | head -14
echo "##### TEST 3: rollback by serving base alone (governance by construction) #####"
timeout 90 target/release/larql lql "USE \"$V\"; INFER \"The capital of France is the city of\" TOP 1;" 2>&1 | flt | grep -aiE '^   1\.' | head -2
echo "B_REVISITED_DONE"
