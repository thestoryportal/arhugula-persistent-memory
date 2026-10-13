## HYBRID (Rung1+Rung3) RESULT + WORKAROUND-LADDER CONCLUSION (small Qwen-3B)
`s243g_qwen3b_hybrid.py` → `s243_hybrid_qwen3b.json` (capital edits, n=8). RELKEY avg: expr 0.93 SEloc 99.91% CEloc **83.58%**. HYBRID avg: expr 0.93 SEloc 99.92% CEloc **83.63%** → projection adds NOTHING to cross-entity.
**Small-Qwen-3B multi-field workaround ladder (sequential/cross-entity, the DB-critical axes):**
- Stock subject-keyed: same-entity FAILS (seq retention 33-37.5%, single loc 87/81/64%).
- Rung 1 relation-inclusive keying: same-entity FIXED (seq 100%, loc 99.9%) BUT cross-entity bleed (CEloc 83.6%; Spain 62%, Germany 72%); language under-expresses.
- Rung 3 post-hoc projection: same-entity PARTIAL (seq 33→50%), cross-entity NOT fixed.
- Hybrid R1+R3 (post-hoc): = relkey alone (SE 99.9%, CE 83.6%) — post-hoc projection inert here.
**CONCLUSION: post-hoc projection is INSUFFICIENT (both same-entity-sequential and cross-entity). Same-entity is fixable via relation-keying; cross-entity is NOT fixed by any post-hoc method tried.** Complete lightweight fix needs IN-SOLVE null-space editing (AlphaEdit/DiKE: project WITHIN the optimization, not post-hoc) — science-path change, LAW#5. Reference: `easyedit_assets/rung3_alphaedit/` + DiKE (arXiv 2505.18774). Inertness harness (s243e) proven. **AWAITING operator decision: pursue in-solve AlphaEdit/DiKE vs ship Qwen-7B-quantized (proven clean both axes).**

