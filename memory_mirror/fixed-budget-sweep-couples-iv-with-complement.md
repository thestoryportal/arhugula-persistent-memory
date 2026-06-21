---
name: fixed-budget-sweep-couples-iv-with-complement
description: "METHOD TRAP: an experiment that holds a total budget fixed and sweeps a partition variable also mechanically sweeps the complement — so a result attributed to your IV may be the coupled variable. Before claiming a fixed-budget sweep isolates X, enumerate every quantity the sweep co-determines; disentangle with a 2D grid or by fixing the complement. Advisor flagged the entanglement directionally; gpt-5.5 cross-family sharpened it into the causal-attribution confound + named the 2D-grid disambiguator — run both."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**The trap (D20, 2026-06-21, CORPUS/23):** D20 swept chunk **SIZE** C at fixed total N=100 to ask "does sub-batching reintroduce corruption?". But at fixed N, chunk-count **K = N/C** — so C=10 is *also* K=10. The corruption attributed to "smaller chunks" could equally be "more sequential update applications" (accumulated-update **COUNT** / cache_c accumulations), **not chunk size per se.** **The advisor reconcile pass DID flag the entanglement directionally** ("the design entangles chunk-COUNT with chunk-SIZE; at fixed N, #chunks ⟺ 1/chunk-size — you can't separate them; the spec lives at the size you didn't test") — it's why the pre-reg split component-1(scale)/component-2(chunking). The **gpt-5.5 cross-family promote-gate review then SHARPENED it** into the precise causal-attribution confound (the corruption may be accumulated-update-**COUNT**, not size) + named the **2D N×C grid** disambiguator, and downgraded the verdict "falsifies condition 3" → "directional mechanism." So: **advisor surfaces the entanglement; cross-family sharpens the attribution + the remedy — complementary, run both.**

**Why it recurs here:** this program runs many **fixed-budget sweeps**. D1 did the same shape — concentration-vs-dilution at *fixed total-N=50* (sweeping same-relation count couples with other-relation count). Any "hold the total constant, vary the split" design has this structure: **size ↔ count, concentration ↔ dilution, depth ↔ breadth** are mechanically locked together once the budget is fixed.

**How to apply (binding, pre-registration checklist):**
- Before claiming a fixed-budget sweep **isolates** variable X: **write down every quantity your sweep mechanically co-determines** (the complement K=budget/X, the number of operations, accumulator updates, etc.). If any plausibly drives the metric, you have NOT isolated X.
- **Disentangle by design:** a **2D grid** varying the budget and the partition independently (e.g. N×C), or **fix the complement** (same-K-larger-C), or hold the operation-count constant. State which you did; if you did none, label the result *directional / confounded*, not isolating.
- **Reinforces [[codex-runs-inline-from-claude-bash]]:** run the **gpt-5.5 cross-family review at every promote gate** — it *sharpens* directional flags the advisor raises into precise, named confounds + concrete disambiguating designs (it did so for both this K-vs-C confound and the B3N over-claims this session). Advisor and cross-family are **complementary** (entanglement-surfacing vs attribution-sharpening), not redundant — run both.
- Pairs with [[match-metric-to-the-claim]] (metric↔claim) — this is its IV-side twin (sweep-variable ↔ what's actually varying).
