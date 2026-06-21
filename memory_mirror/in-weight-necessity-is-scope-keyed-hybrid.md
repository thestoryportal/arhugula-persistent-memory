---
name: in-weight-necessity-is-scope-keyed-hybrid
description: "B3 in-weight-necessity DECIDED (D-B3N-1) — in-weight is NOT contractually required by the spec; verdict = scope-keyed HYBRID (in-weight viable for batch core at scope, side-store for incremental high-churn). The decision collapses to two axes; corruption evidence is incremental-path-only and must not be counted against the batch path"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**D-B3N-1 (2026-06-21) RESOLVES the highest-stakes open F1 architecture question** (the *hypothesis-register* "B3 — is diffuse in-weight even required?"; disambiguated from `D-B3-1`=quantization). Full detail (single source): `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md`. Supersedes the open framing in [[in-weight-vs-sidestore-f1-question]].

**The decision collapses to TWO primary axes (not exhaustive — see §1.1 for the omitted dims):**
- **Axis A (READ):** in-weight's only contractually-relevant unique value is forward-pass "native knowing" (spec line 90). That is a stated PARADIGM PREFERENCE, **not a tested hard requirement** — there is no latency SLA (p95_latency_ratio tolerates 2×; reads block during mount), and the *enforced* read contract (L1 SELECT read-back, reverse-lookup/bidirectional, multi-hop/aggregation) is satisfiable by a **structured side-store given reliable NL→query routing** (EV-2: KG ≥ vector-RAG on multi-hop, directional). The register's "multi-hop needs in-weight" premise was wrong.
- **Axis B (WRITE):** decides whether our corruption evidence even applies. Batch/genesis path = CLEAN at scope (A1 100% + B3 quant-survives + E1 CPU-serve, 3B/N≤100). Incremental/sequential path = where corruption bites (G6.1, D-D1-2 k≤1, mixed-load).

**VERDICT = scope-keyed conditional HYBRID:** in-weight VIABLE-AT-TESTED-SCOPE for the batch/genesis core; route incremental-high-churn to a gated/structured side-store. §8.7 `k≤1` attaches to incremental/residual mode, NOT the batch core.

**Why / How to apply:**
- **Do NOT count incremental corruption against the batch deployment path** — the #1 framing error the advisor caught (double-count). Our own data supports in-weight *at batch scope*; the side-store external leads are directional priors only (DISCIPLINE §3; only NeuralDB confirmed) — don't elevate them over our own evidence (confirmation-bias trap).
- **Label = reasoned architectural position, NOT an empirical PASS** (no single pre-registered falsifier; the claim decomposes into discriminating requirements). [[pass-label-not-equal-promotable-claim]], [[prototype-tautology-trap]].
- **Write F1 as the hybrid**, not a blanket "in-weight ready-with-conditions." The §1.1 open dims (auditability, delete/update governance, security/trust-boundary, routing reliability, cost — several favor side-store, trust-boundary favors in-weight) are separate F1 sub-decisions.
- **The biggest single F1 lever is an operator input:** is the deployment write-profile batch-ONLY or does it include incremental-at-scale? That decides which verdict row governs.
- Overturning conditions: a confirmed hard mid-generation/zero-latency reason-over-fact requirement (flips Axis A) OR a confirmed incremental-at-scale requirement (→ candidate is side-store / Parametric-RAG, NOT diffuse in-weight).

Dual-reviewed: advisor (pre-authoring, set the two-axis frame + caught the double-count/bias traps) + gpt-5.5 cross-family FIX-FIRST (8 calibration fixes applied, direction unchanged). NEXT arc: 7B numeric-transfer (OQ-W1) → CP2 schema build-items → write F1.
