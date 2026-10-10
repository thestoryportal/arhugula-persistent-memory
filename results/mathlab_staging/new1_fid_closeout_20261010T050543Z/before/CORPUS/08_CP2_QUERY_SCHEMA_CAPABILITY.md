# 08 — CP2: LARQL QUERY-SCHEMA CAPABILITY (result)
_Run 2026-06-18 on the pod. Artifacts: probe `/workspace/experiments/governance/cp2_query_schema_probe.sh`; captured output `/workspace/results/cp2_probe_results.txt`. LARQL UNMODIFIED (binary + LQL only). Evidence read directly from the LQL grammar (`crates/larql-lql/src/ast.rs`, `lexer.rs`, `parser/`, `executor/`) + live runs against `/dev/shm/qwen3.vindex` (base) and the CP1-compiled vindex (France→Berlin baked)._

## The CP2 question (from 03/06)
We had tested `INFER`/generation only. Does LARQL's **LQL actually express** the spec's query surface —
the mandatory **L1 `SELECT` read-back** (§8.9), **`DELETE FROM EDGES`** (§8.5), the **triple model + 5
relation families** (§7.3 D6), and **`violates` ephemeral-rejection** (C6/C9) — or only inference? This is a
**capability** question, answered by what LARQL's verbs do against a real vindex.

## Method
(1) Read the LQL AST/lexer/parser/executor for the actual statement set. (2) Run each verb live, with an
**advisor-mandated positive control**: attempt to read back a fact the BASE model natively knows
(France→Paris) before concluding anything about read-back of *edits*.

## Findings (each = grammar-confirmed AND run live)
| # | Spec contract | LARQL reality (measured) | Verdict |
|---|---|---|---|
| **L1 `SELECT` read-back** (§8.9, mandatory ALL writes) | `SELECT` confirms the written **(entity,relation,target)** edge | `SELECT ... FROM EDGES` EXISTS + executes, but returns **weight-derived FFN feature rows** (`Layer, Feature, Token, Relation, Score`), NOT triples. **POSITIVE CONTROL: native France→Paris is NOT readable either** — `WHERE entity="France"` returns the France *feature* (L18 F1861, top-token "France", cluster `vice/france/train`); **"Paris" appears nowhere**; `DESCRIBE "France"` → "(no edges found)". | ❌ **NOT satisfied.** `SELECT` is feature-introspection, never a fact/triple storage probe — for ANY fact, native or edited. |
| **`DELETE FROM EDGES`** (§8.5) | delete edges | EXISTS + executes: "Deleted 1 features (patch overlay)" → subsequent `SELECT` confirms "(no matching edges)". Feature-level delete via patch overlay, recorded as `PatchOp::Delete`. | ✅ **works** (feature-keyed) |
| **Triple model** (entity→relation→target; `target` reserved C3) | first-class triple ops | `INSERT INTO EDGES (entity, relation, target) VALUES (...)` is first-class syntax; `SELECT` filters on `entity`/`relation`. **But** INSERT installs to the **KNN store** ("Architecture B, retrieval-override"), not MEMIT — consistent with the banked L-COMPOSE immaturity. | ⚠️ **vocabulary present; store is feature/KNN-keyed, not a triple table** |
| **5 relation families** (D6: Structural/Knowledge/Constraint/Taxonomy/Namespace) | fixed 5 families w/ defined labels | `SHOW RELATIONS` → **24,469 emergent decompiler labels** (`morphological`, `economics`, `history`, `paper/mix/any`, …); header reports "512 relation types". NONE are the spec's families. | ❌ **schema-mapping GAP**: LARQL's relation space is emergent/decompiled, not the spec's fixed families |
| **`violates` rejection** (C6/C9: write engine hard-rejects) | hard-reject any patch containing `violates` | `INSERT INTO EDGES (entity, relation, target) VALUES ("France","violates","Berlin")` → **ACCEPTED**: "Inserted: France —[violates]→ Berlin at L20 (KNN store)". No rejection. | ❌ **NOT enforced by LARQL** (treated as a free-string label) |

## Net verdict
**Mixed — and the mix is the finding.** The LQL *verbs* the spec names (`SELECT … FROM EDGES`,
`DELETE FROM EDGES`, `INSERT INTO EDGES`, the entity/relation/target vocabulary) **exist and execute**
against real vindexes — so this is **not** "INFER-only." `DELETE FROM EDGES` genuinely works. **But the
load-bearing semantics diverge from the spec's schema contracts**, and the divergences are NOT LARQL bugs —
they are layers the spec assigns elsewhere that LARQL does not provide:

1. **L1 `SELECT` storage read-back is NOT available from LARQL** (positive-control-confirmed: it can't read
   back even a native fact as a triple). The spec's mandatory L1 probe therefore requires a **separate
   (entity,relation,target) index maintained at OUR schema/governance layer** — independent of editing. This
   **back-fills CP1's deferred L1 probe**: CP1's behavioral `larql run` stand-in was the right call, and the
   real L1 probe is now a known **schema-layer build item (→ G3 / schema layer)**, not a LARQL feature.
2. **The 5 relation families are a schema-layer contract LARQL doesn't model** (emergent labels). Mapping
   spec families ↔ LARQL's decompiled relation space is schema-layer work.
3. **`violates` rejection (C6/C9) is the Validator's job**, confirmed: LARQL accepts it. (Our CP1 Gate /
   G3 Validation pipeline is where this lives.)

## Honest scope / caveats
- Probes used Qwen3-0.6B vindexes; relation-label quality reflects a 0.6B decompile (emergent labels are
  noisy at this size) — the *structural* finding (feature-keyed, not triple-keyed; no triple read-back) is
  size-independent (positive control), but label semantics may sharpen on larger models (→ G6).
- `target`-reserved (C3) not separately exercised (it is a column keyword in INSERT syntax; benign).
- This does NOT re-test the already-banked L-COMPOSE/L-COMPACT negatives; it is consistent with them
  (INSERT → KNN store, not MEMIT).

## Consequence for the program
CP2 **resolves the capability question without expanding LARQL**: LARQL is the **serve/inference + overlay
substrate** (proven), plus a usable feature-level `DELETE`/introspection surface. The **relational schema
contracts** (triple storage + read-back, 5 families, `violates`) belong to **our schema/validation layer** —
now a concretely-scoped build item rather than an open unknown. No LARQL modification is warranted by CP2.
