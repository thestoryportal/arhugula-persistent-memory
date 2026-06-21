# D20 — Compaction sub-batch granularity (pre-registration)

**Hypothesis-register id:** D20 (B3N condition 3). **Decision-ID (on close):** `D-D20-1`.
**Status:** PRE-REGISTRATION (advisor-checked before authoring the runner). **Date:** 2026-06-21.

> **⚠ BOUNDING CLAIM (read first — advisor pre-authoring):** this experiment **can FALSIFY B3N condition 3 but CANNOT confirm it.** Total-N is held at 100 — the value where the single joint solve is *already known clean* (A1) — so the sweep isolates the **chunking-per-se** effect with **scale held constant at a known-safe point.** It therefore cannot exhibit *scale-driven* corruption. Condition 3 is about behavior at the **realized drift size** (1,500–8,000 edges) = a **scale** variable this run does not vary. So: a *corrupting* result transfers upward and **falsifies** condition 3; a *clean* result means only "chunking-per-se is tolerable at fixed small N" and leaves condition 3's **scale component OPEN** — it is **NOT** a green light for in-weight compaction. The engine-faithful scale question (does a *single joint solve* stay clean as total-N climbs toward the 2,000 cap — component 1 below) is **logically prior and remains OPEN for F1** until a larger screened stimulus pool is built (the real unlock; an operator-visible effort call — see Feasibility).

## The question (reframed from "N≥2,000" after orientation)

B3N condition 3 asks: does the spec's §8.10 compaction stay clean at the realized drift size? The advisor's premise was "MEMIT sub-batches at 2,000 → sequential sub-batch solves → corruption." **Orientation finding that reframes it:**

1. **The reference engine (kmeng01/memit) does NOT sub-batch.** It builds key/value matrices over *all* requests and does a **single joint `torch.linalg.solve` per layer** regardless of N (`memit_main.py:203`; the only batching, `mom2_batch_tokens`, is covariance token-streaming, unrelated to edit count). **The "MEMIT recommended batch size 2,000, patches above sub-batched internally" is a SPEC prescription (spec line 384), not engine behavior.**
2. So the spec is *prescribing* a behavior (sub-batching) that converts one clean joint solve into **sequential accumulation** — exactly the A0/sequential mechanism that corrupts.
3. The 2,000 number is not the mechanistic variable — **chunk size (sub-batch granularity) is.** And the two endpoints are already established:
   - **chunk = N** (single joint solve = A1, CORPUS/14): held-out cross-entity correctness **clean (100% at N≤100)**.
   - **chunk = 1** (fully sequential = A0/G6.1, CORPUS/13): **collapses (~100→42%)**.

**Reframed hypothesis (D20):** held-out cross-entity read corruption is a function of **sub-batch granularity** — it rises as chunk size shrinks from N toward 1. **If corruption appears at chunk sizes ≫ 1 (i.e., a small number of sub-batches already hurts), the spec's mandated 2,000-sub-batching reintroduces corruption for any deployment exceeding one sub-batch — falsifying B3N condition 3 (compaction does NOT return to clean at scale).**

This is testable **now**, at N≤100, with the existing screened stimulus — no 2,000-fact pool required. **But (per the bounding claim above) it isolates the chunking variable, not scale** — see component 1 for the scale question this does NOT answer.

### Two distinct components (the engine-faithful decomposition)
- **Component 1 (SCALE — logically prior, NOT in this run):** does a *single joint MEMIT solve* (what the engine actually does, up to the spec's 2,000 cap) stay clean as **total-N climbs**? Each 2,000-sub-batch in the spec's regime is itself a single solve that must be clean *first*. B1/D-B1-1 already shows single-solve isn't perfectly flat (7B batch → 91.7% at N=100). A 100→~150 trend on the current stimulus is **too short to resolve this** → **condition 3's core likely stays OPEN for F1 regardless of this run** unless the larger screened stimulus pool is built. Do NOT let this run's completion read as "condition 3 addressed."
- **Component 2 (CHUNKING — this run):** at fixed known-clean total-N, does partitioning the solve into accumulating sub-batches reintroduce corruption, and is there a safe chunk floor? Falsifies condition 3 if yes; bounds-but-doesn't-confirm if no.

## Design — chunk-size sweep at FIXED total N (accumulating)

Fixed total edit set (the A1 N=100 record set, grouped-by-entity ordering, band [4-8], Qwen2.5-3B, in-solve AlphaEdit — the validated clean recipe). Vary only **chunk size C**: partition the N edits into ⌈N/C⌉ consecutive chunks; solve each chunk as an **independent joint MEMIT solve that ACCUMULATES on the running edited weights** (chunk k+1 solved on the weights left by chunk k). Measure the same fixed disjoint held-out set after all chunks.

- **Arms:** C ∈ {N (=100, single joint = A1 reproduction), 50, 25, 10, 5, 1 (= fully sequential = A0 reproduction)}. (≥6 points spanning the spectrum.)
- **Anchors (gates):** the C=N arm MUST reproduce A1 (held-out ≈ clean) and the C=1 arm MUST reproduce A0 (held-out corrupted) — **if the two endpoints don't reproduce, the harness is wrong → HALT** (LAW#3 known-baseline gate). This is the built-in instrument check.
- **Metric:** held-out cross-entity top-1 correctness (matches the corruption claim — [[match-metric-to-the-claim]]) + the paired JS locality used in G6.1/CORPUS-13 as secondary. Edit-success (expression) ≥95% on every arm as a guard (excludes under-editing as the explanation).
- **Seeds/ordering:** ≥2 held-out seeds + the established grouped ordering; report the cluster-aware spread, not iid CIs ([[clustered-editing-trials-sampling-unit]]). Single ordering for v1 (note as a scope limit).
- **Null-space P / covariance handling (specified — it materially changes results, advisor):** P is computed **ONCE from the clean base** (the all-patches statistics) and held **FIXED across all chunks**; chunks accumulate on the *weights* only. Rationale: the spec's §8.10 compaction is a "full MEMIT re-run on archived patches" with **all patches known up front** — so the covariance/null-space is a single-event quantity, not refreshed per sub-batch. This also keeps the C=N arm bit-identical to A1 (fixed-base P). A2b precedent: per-edit K_S *refresh* did not help (CORPUS/16) — so fixed-P is both spec-faithful and the conservative default. *(Secondary, only if cheap: a recompute-P-per-chunk arm to bound the alternative; not required for v1.)*
- **LAW#5:** the new "chunked-accumulate" mode must prove inert at C=N (it must be bit-for-behavior identical to the existing single-joint batch path = A1, fixed-base P). Gate before trusting any arm.

## Pre-registered pass/fail (set BEFORE the run)

The question is "does sub-batching reintroduce corruption" — framed so a clean result is a real possible outcome:

- **CONDITION-3-FALSIFIED (chunking reintroduces corruption; in-weight self-heal unsafe whenever compaction sub-batches):** held-out corruption **rises as C shrinks** (not pre-registering strict monotonicity — order/seed noise is real, [[sequential-edit-run-nondeterminism]]; the claim is a clear downward trend in cleanliness with C, robust across the ≥2 held-out seeds) AND is **materially present (≥10pp below the C=N clean anchor) at C ≥ N/4** (i.e., ≤4 sub-batches already corrupt). → the spec's mandated 2,000-sub-batching cannot be assumed clean; F1 carries condition 3 as **FAILING** and leans the incremental/compaction path toward the side-store. **This branch is valid and transfers upward** (chunking harm at small N only gets worse with scale).
- **CHUNKING-TOLERABLE-AT-FIXED-N (NOT "condition 3 supported"):** corruption stays within 10pp of the C=N clean anchor until C is small. → **bounded claim only: chunking-per-se is tolerable at fixed small known-clean N.** This is **NOT** a green light for in-weight compaction and does **NOT** confirm condition 3 — the **scale component (component 1) remains OPEN** (N=100 single-solve is already clean, so this run has no scale to drive corruption). It *does* yield a candidate **minimum-chunk-size floor K** to test *together with* a scale run later; on its own it is a necessary-not-sufficient sub-result. F1 records condition 3 as **OPEN (chunking sub-question passed at N=100; scale unresolved)**.
- **PARTIAL/graded:** a corruption-vs-granularity curve with a knee — report the knee as the candidate safe-chunk floor; do not force a binary; same OPEN-on-scale caveat applies.

Whatever the curve, the deliverable is the **corruption-vs-sub-batch-granularity function**, which directly informs B3N condition 3 and (if a safe floor exists) becomes a spec guardrail ("compaction sub-batch size ≥ K") paired with the §8.7 concentration-aware amendment.

## Feasibility / scope notes (honest)
- Runs at N=100 on the 4090 with the existing recipe — **cheap** (≈ A1/A0 cost × #arms). No new stimulus, no VRAM risk.
- **Scope limit:** this tests the *chunking* mechanism at fixed N=100, NOT scale. The **scale component (component 1) is the real unlock and stays OPEN** without a larger screened stimulus pool.
- **⭐ OPERATOR EFFORT CALL (surfaced, not silently dropped):** resolving condition 3's *core* (does single-solve / sub-batched compaction stay clean at the realized drift size, N→1,000s) requires **building a large screened single-token fact pool** (our country-attribute domain caps at low hundreds of confident+correct+single-token facts; reaching N≫100 needs a new domain or synthetic facts, each pre-screened to keep the instrument clean per G6.1). That is a **non-trivial stimulus-engineering sub-project** — an explicit operator-visible cost/benefit decision, NOT assumed. The cheap chunk-sweep (component 2) runs first because it has real falsification power on its own; the stimulus-build is the gate for *confirming* condition 3.
- The 3B within-process noise is low; the binding uncertainty is edit-ORDER ([[sequential-edit-run-nondeterminism]]) — hence ≥2 held-out seeds and the endpoint anchors.
