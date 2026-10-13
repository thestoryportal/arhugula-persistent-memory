# PACKAGE — 🗂️ Graph Data Architect (Schema / Query)
_Run under COUNCIL_PROTOCOL.md. Audit vs CORPUS 05 §Graph. Concern: can the schema express + query what's needed; is the relation vocabulary coherent; deletion semantics._

## Your spec contract (audit baseline)
Entity taxonomy (§7.2); 5 relation families D6 (§7.3); triple entity→relation→target, `target` reserved (C3); `violates` ephemeral, hard-rejected in patches (D7,C6,C9); query surface SELECT / INSERT INTO EDGES / DELETE FROM EDGES; KNN graph-walk; polysemantic noise; undeclared relations rejected pre-MEMIT (C5).

## Relevant evidence (cite from 01)
- All edits used entity→relation→target ("capital-of", "currency", "language", "field/nationality/occupation"). Triple model exercised.
- T2.1 DELETE = revert-to-original (un-write), 6/6 — NOT semantic DELETE FROM EDGES / tombstone.
- T2.3 multi-token VALUES (targets) work; T2.3b non-country domains underpowered.
- Read surface tested: only `INFER`/`run` (generation) + `WALK`/`DESCRIBE` (browse, noisy on 0.6B). 

## Standing questions to adversarially answer (likely GAP-heavy)
1. **Full query schema UNTESTED (G4)**: `SELECT`/`DESCRIBE` round-trip of stored facts? `DELETE FROM EDGES` semantics (vs our revert)? The spec's L1 storage probe is a `SELECT` read-back — was that ever exercised? (No — we used INFER.)
2. **Relation-family coherence**: do our edits map to the 5 D6 families? Is the relation vocabulary the spec mandates representable + queryable in LARQL's relation model (512 relation types seen in vindex)?
3. **Deletion semantics**: spec needs DELETE; we only showed revert-to-original. Is true deletion (fact removal / `violates` rejection) supported?
4. **Polysemantic noise / KNN-walk read quality**: WALK on 0.6B returned noisy multilingual features — is the graph-walk read usable at deployment model scale?

## Seeded gap: G4 (full query schema, DELETE, SELECT read-back). This is largely UNTESTED — confirm scope + flag as BLOCKER vs DEFER-TO-LOCAL.
