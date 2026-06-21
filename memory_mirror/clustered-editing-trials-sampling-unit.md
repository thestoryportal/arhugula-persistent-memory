---
name: clustered-editing-trials-sampling-unit
description: For held-out read-corruption under sequential editing, the sampling unit is the (held-out-set × edit-ORDER) pair, NOT the individual entity — iid/Wilson CIs are invalid (clustered); use cluster-bootstrap over orders + ≥2 held-out seeds; corruption is order/held-out-DOMINATED not count-determined; ship a conservative last-all-clean ceiling for a safety counter, never a fitted point threshold
metadata:
  type: feedback
---

When measuring held-out same-relation read corruption to set a threshold/law (D1/§8.7, D-D1-2), the **experimental unit is the ordered edit-subset + the held-out set**, not the individual held-out entity. This was the load-bearing methodology lesson (gpt-5.5 cross-family caught it; Opus advisor concurred).

**What goes wrong if you ignore it:**
- **iid confidence bounds (Wilson/Beta-binomial over N entity-trials) are INVALID** — the "288 trials" (12 orders × 24 shared held-out entities) are clustered by order and by shared entity; effective n ≪ 288, so a Wilson UCB is *overconfident* (true CI wider, thresholds lower). Retire it as a calibrated bound; keep only as a descriptive pooled stat.
- **A point threshold off one config is meaningless.** Corruption is **edit-ORDER- and held-out-set-DOMINATED, not count-determined**: at fixed k one toxic order hit 25% while 8/12 orders were 0%; the more-toxic held-out seed (seed-2) corrupted at k=1–2 where seed-3 was 0% (broke the k≤2 "clean" ceiling → revised to k≤1). Single-seed/single-order curves are optimistic.

**How to apply (the correct instrument):**
- **Pool binary corruption over many randomized edit-ORDERS (≥~12) AND ≥2 held-out seeds**, then **cluster-bootstrap over orders** for a CI (resample orders, recompute pooled). Report **observed-worst-order, bootstrap-upper, and mean** separately — don't collapse to one number.
- **Leave-one-order-out** to expose toxic-order dependence (drop the max order; if the crossing vanishes, it was one-order-driven).
- **For a deployment SAFETY counter, ship the conservative "largest k clean across ALL orders × seeds × processes" ceiling** + scoped empirical observations (onset k, UCB-crossing k) labeled NOT-portable-thresholds. Both reviewers: do NOT write "WARNING=k=N" as a clean property.
- **Define the threshold on the operational binary metric** (top-1 wrong = a query returns the wrong answer), with margin/NLL/rank as smooth *diagnostics* only — a margin/continuous mean can hide a few entities flipping catastrophically.
- The real control variable is likely **edit-set geometry (key-collinearity / entity identity)**, not a bare per-relation count → the count is a fail-closed *sentinel*, not the mechanism (ties the §8.7 worse-of design + [[match-metric-to-the-claim]], [[single-seed-limits-generality-not-significance]]).
