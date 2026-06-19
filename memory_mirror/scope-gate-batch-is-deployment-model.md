---
name: scope-gate-batch-is-deployment-model
description: "Track-A scope gate resolved — deployment is batch-rebuild, so A3/BetaEdit is parked and Q4_K quantization survival is the real next falsifier"
metadata: 
  node_type: memory
  type: project
  originSessionId: ba0f7d12-2172-4518-b3b6-963f1e0dd709
---

2026-06-18 (D-SCOPE-1). The Track-A "HIL scope gate" (should we port BetaEdit/A3?) was resolved: **A3 is PARKED, not next.** The LLM-as-DB deployment model is **edit offline on GPU → COMPILE → serve on CPU** ([[deployment-target-intel-cpu]]) = a **batch-rebuild model**. A1 already pins the batch write path at 100→100→100% cross-entity @N≤100, so there is **no headroom for A3 on the path deployment actually uses**. A3/BetaEdit only helps the *incremental online single-fact write* path, which nothing in the record requires.

**Why:** When the operator deferred ("make the perfect recommendation aligned with the goal"), my first instinct was to do A3 for "scientific completeness." The advisor caught that this answered the **wrong criterion** — the gate asks what *deployment* needs, not whether testing incremental would be thorough. Classic criterion-swap; almost anything clears the completeness bar, which is exactly why the gate was written against the deployment bar.

**How to apply:** Re-activate A3 (the BetaEdit port — repo `lbq8942/BetaEdit` cloned, config-matched, cov ready) the moment incremental online single-fact writes become a **confirmed hard requirement**. Until then, pick the next run by what CPU deployment depends on. The sharpest live falsifier is **B3/G6.2 — real Q4_K_M quantization survival** on the A1-clean batch store. Reinforces [[match-metric-to-the-claim]] (answer the metric/criterion the claim actually makes) and the operator-profile habit of deferring to evidence over momentum.
