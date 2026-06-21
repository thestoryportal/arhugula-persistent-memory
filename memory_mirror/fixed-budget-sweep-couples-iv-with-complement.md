---
name: fixed-budget-sweep-couples-iv-with-complement
description: "METHOD TRAP: an experiment that holds a total budget fixed and sweeps a partition variable also mechanically sweeps the complement — so a result attributed to your IV may be the coupled variable. Before claiming a fixed-budget sweep isolates X, enumerate every quantity the sweep co-determines; disentangle with a 2D grid or by fixing the complement. The same-model advisor chain missed it; the gpt-5.5 cross-family review caught it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**The trap (D20, 2026-06-21, CORPUS/23):** D20 swept chunk **SIZE** C at fixed total N=100 to ask "does sub-batching reintroduce corruption?". But at fixed N, chunk-count **K = N/C** — so C=10 is *also* K=10. The corruption attributed to "smaller chunks" could equally be "more sequential update applications" (accumulated-update **COUNT** / cache_c accumulations), **not chunk size per se.** My pre-reg AND the advisor (×2) missed this; the **gpt-5.5 cross-family promote-gate review caught it** and downgraded the verdict from "falsifies condition 3" to "directional mechanism, K-vs-C confound open."

**Why it recurs here:** this program runs many **fixed-budget sweeps**. D1 did the same shape — concentration-vs-dilution at *fixed total-N=50* (sweeping same-relation count couples with other-relation count). Any "hold the total constant, vary the split" design has this structure: **size ↔ count, concentration ↔ dilution, depth ↔ breadth** are mechanically locked together once the budget is fixed.

**How to apply (binding, pre-registration checklist):**
- Before claiming a fixed-budget sweep **isolates** variable X: **write down every quantity your sweep mechanically co-determines** (the complement K=budget/X, the number of operations, accumulator updates, etc.). If any plausibly drives the metric, you have NOT isolated X.
- **Disentangle by design:** a **2D grid** varying the budget and the partition independently (e.g. N×C), or **fix the complement** (same-K-larger-C), or hold the operation-count constant. State which you did; if you did none, label the result *directional / confounded*, not isolating.
- **Reinforces [[codex-runs-inline-from-claude-bash]]:** run the **gpt-5.5 cross-family review at every promote gate** — a *different model* catches IV-coupling/mechanism confounds the same-model advisor chain systematically misses (it caught both this and the B3N over-claims this session). The advisor and cross-family are complementary, not redundant.
- Pairs with [[match-metric-to-the-claim]] (metric↔claim) — this is its IV-side twin (sweep-variable ↔ what's actually varying).
