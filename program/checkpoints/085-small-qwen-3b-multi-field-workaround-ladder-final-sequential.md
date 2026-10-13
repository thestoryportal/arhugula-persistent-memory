## SMALL-QWEN-3B MULTI-FIELD WORKAROUND LADDER (final, sequential retention = DB-critical metric)
- Stock subject-keyed: 33% retention. FAILS.
- Rung1 relation-inclusive keying: same-entity 100% but cross-entity bleed (CEloc 83.6%); language under-expresses.
- Rung3 post-hoc projection: 50% retention; cross-entity not fixed by hybrid.
- **In-solve AlphaEdit (P + cache_c): 100% retention, untouched 73.7%, expression intact. ← WINNER for sequential.**
- Qwen-7B stock: 100% retention, untouched 79%, clean cross-entity (no workaround). Heavier.
**DEPLOYMENT CONCLUSION: lightweight CPU path VALIDATED — small Qwen-3B + in-solve AlphaEdit write engine → reliable multi-field accumulation (100% retention); deploy edited standard weights on CPU via llama.cpp/LARQL. Remaining tuning: untouched-attr locality (74%) via L2/nullspace_threshold. Alternative: Qwen-7B-quantized (cleaner untouched, heavier).**
- ⚠️ **SCOPED BY G6.1:** "reliable multi-field accumulation" = SAME-ENTITY. Across MANY entities at scale, subject-keyed AlphaEdit corrupts cross-entity reads (see above + `CORPUS/13`). The complete multi-entity fix is entity-aware in-solve projection (Rung-3-at-scale) — UNVALIDATED. CPU-deploy mechanics unaffected; the OPEN item is the write engine's cross-entity isolation.

