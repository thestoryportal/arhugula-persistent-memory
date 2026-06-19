---
name: resolve-the-gates-real-criterion
description: "When resolving a decision gate (esp. under \"use your judgment\"), answer the gate's ACTUAL criterion, not a flattering adjacent one almost anything clears"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba0f7d12-2172-4518-b3b6-963f1e0dd709
---

When resolving a **decision gate**, answer the gate's *actual* criterion — not a more flattering adjacent question that almost anything clears.

**The trap (caught this session, 2026-06-18, on the A3 scope gate — [[scope-gate-batch-is-deployment-model]]).** The gate asked "does *deployment* need incremental writes?" I answered "would testing incremental be *scientifically complete*?" and recommended the meaty BetaEdit port. The advisor: "Almost anything clears the second bar — that's exactly why the gate was written against the first." Applied to the actual criterion, the evidence I'd already retrieved (deployment = edit-offline-GPU→compile→serve-CPU = batch) resolved the gate the *opposite* way, and the elaborate work (A3) had zero headroom on the path deployment actually uses.

**Why this recurs:** the swap is self-serving — the adjacent criterion licenses the more interesting/elaborate task. Three habits that defuse it:
1. **State the gate's literal criterion verbatim before answering**, and check your answer is *to that*, not to a cousin of it.
2. **Treat the user's deferral / non-assertion as evidence.** "Use your judgment" is NOT license to pick the ambitious path; it's a mandate to apply the criterion honestly, including evidence pointing *away* from the work you'd find most interesting. If a requirement were hard, the user deferring would more likely have just asserted it.
3. **Ask "what does the goal actually depend on right now?"** — often a runnable falsifier (here: Q4_K_M quantization survival, which PASSED) beats polishing a path that may never be used.

**How to apply:** call `advisor()` *before* committing to a gated decision, not after — the criterion-swap feels like good reasoning from the inside. Sibling lessons: [[match-metric-to-the-claim]] (same shape at the measurement level), [[evidence-over-scaffolding]] (run the cheap falsifier, don't accrete elaborate work). Aligns with the operator's "defer to evidence, make decisions legible" ([[operator-profile-llm-as-database]]).
