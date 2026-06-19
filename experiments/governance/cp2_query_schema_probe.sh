#!/usr/bin/env bash
# CP2 — LARQL query-schema CAPABILITY probe (unmodified LARQL; binary + LQL only).
# Question (CORPUS 03/06, CP2): does LARQL's LQL express the spec's query surface —
#   L1 SELECT read-back (§8.9), DELETE FROM EDGES (§8.5), the triple model + 5 relation
#   families (§7.3 D6), and `violates` ephemeral-rejection (C6/C9) — vs. only INFER/generation?
# Result interpretation lives in CORPUS/08_CP2_*. This script is the reproducible evidence.
set -u
L=$LLMDB_ROOT/external_prior_art/larql/target/release/larql
CV="${1:-$(ls -d /dev/shm/cp1_work/compiled_*.vindex 2>/dev/null | head -1)}"
BASE=/dev/shm/qwen3.vindex
echo "## CP2 probe  vindex=$CV  base=$BASE  $(date -u +%FT%TZ)"

run() { echo; echo "==== $1 ===="; echo "LQL> $2"; timeout 250 $L lql "$2" 2>&1 | tail -"${3:-14}"; }

# PROBE 0 — POSITIVE CONTROL (advisor-mandated): can SELECT read back a NATIVE fact the base
# knows (France->Paris) as a triple? If Paris does NOT surface -> SELECT is feature-introspection,
# never a triple storage probe (conclusion A); the L1 miss on edits is NOT overlay-specific.
run "0 POS-CONTROL: native France->Paris read-back from BASE" "USE \"$BASE\"; SELECT entity, relation FROM EDGES WHERE entity = \"France\" LIMIT 8;"
run "0b POS-CONTROL: DESCRIBE France on BASE"                 "USE \"$BASE\"; DESCRIBE \"France\";"
run "0c POS-CONTROL: does 'Paris' appear anywhere?"          "USE \"$BASE\"; SELECT * FROM EDGES WHERE entity = \"France\" LIMIT 15;" 20

run "1 SELECT FROM EDGES (entity+relation filter)"  "USE \"$CV\"; SELECT entity, relation FROM EDGES WHERE entity = \"France\" LIMIT 8;"
run "2 SELECT * FROM EDGES (feature_meta scan)"      "USE \"$BASE\"; SELECT * FROM EDGES WHERE layer = 4 LIMIT 6;"
run "3 DESCRIBE entity (triple read-back of the edit?)" "USE \"$CV\"; DESCRIBE \"France\";"
run "4 DELETE FROM EDGES then SELECT (confirm removal)" "USE \"$CV\"; DELETE FROM EDGES WHERE layer = 18 AND feature = 1861; SELECT * FROM EDGES WHERE layer = 18 AND feature = 1861 LIMIT 3;"
run "5 SHOW RELATIONS (label space: 5 families or emergent?)" "USE \"$CV\"; SHOW RELATIONS;" 18
run "6 INSERT a 'violates' triple (C6/C9: should hard-reject)" "USE \"$CV\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"violates\", \"Berlin\");"
run "7 control: a legal INSERT triple"               "USE \"$CV\"; INSERT INTO EDGES (entity, relation, target) VALUES (\"France\", \"has-capital\", \"Berlin\");"
echo; echo "## done"
