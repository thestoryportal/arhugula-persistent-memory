# Per-unit logging convention — what `stats.py` needs to actually run

_Created 2026-06-24 alongside `tools/stats.py` + `tools/power.py`. This is the
forward dependency the advisor flagged: the correct statistics for this program
(cluster-bootstrap over the real sampling unit) **cannot be computed post hoc
from the aggregate percentages most result JSONs currently save.** This file
records the convention so future harness runs emit analyzable data._

## The problem (why c2band couldn't be rescued)
The flagship metric — held-out **cross-loc corruption** — is saved as a single
aggregate `%` per arm (e.g. `unt_cross_loc: 67.68`). You cannot bootstrap a
scalar. And single-seed runs have **no order-cluster to resample**. That is
exactly why C2-band was "real-but-underpowered" and could not be promoted: the
per-unit data to quantify the uncertainty was never emitted. `stats.py`
therefore **refuses loudly** on aggregate-only files rather than fake a CI.

## The sampling unit
`unit = (held-out-set seed) x (edit-order)` — see
`[[clustered-editing-trials-sampling-unit]]`. iid / Wilson CIs are **invalid**
here; the dominant variance is *between* orders/seeds (~50pp run-to-run swing,
`[[sequential-edit-run-nondeterminism]]`), not within-cluster binomial.

## What to emit (so `stats.py from-result` / `cluster` can run)
Add a `per_unit` block to the result JSON. Each row = one held-out probe under
one (seed, order) cluster:

```json
"per_unit": [
  {"cluster": "hoseed0|order1", "seed": "hoseed0", "order": "order1",
   "probe": "France->capital", "arm": "band48",
   "correct": 1, "maxprob": 0.83, "js_vs_pre": 0.04}
]
```

Minimum viable: `cluster` (or `seed`+`order`), `arm`, and the per-claim metric
(`correct` for read/top-1; `maxprob` for margin/CP2; `js_vs_pre` for
distributional). Then:

- `stats.py cluster --data <{values,clusters}>` → cluster-bootstrap CI on a mean.
- `cluster_bootstrap_diff(...)` (library) → CI on the arm difference.
- Two-arm corruption: pass both arms' `(values, clusters)`.

## Minimum design for a *promotable* corruption result
`power.py` sizes it. Rule of thumb from the noise: **≥2 held-out seeds × ≥2
edit-orders = ≥4 clusters/arm**, and check `power.py size` for the claimed
effect against the measured between-order SD before running. Single seed → at
most a within-experiment direction, never a reliability claim.

> ⚠ **≥4 is necessary, not sufficient.** ≥4 clusters is the floor just to *have*
> a cluster structure to bootstrap. The number you actually need to *detect* an
> effect is much larger at our realized noise. A `power.py size` at the measured
> ~50pp swing (sd≈0.125), p0=0.70, effect=20pp, items=8 lands around **15+
> clusters/arm** for 80% power (verified 2026-06-24; a point estimate near a
> search boundary, treat as "≳15", not exact). You **cannot** items-per-cluster
> your way out — the dominant variance is *between* clusters, so adding held-out
> probes per order barely helps. **The cheaper lever is reducing the swing
> (determinism) than multiplying order/seed clusters** — which is why the
> deterministic-instrument next-arc item (`[[sequential-edit-run-nondeterminism]]`)
> directly gates the cost of every clustered corruption claim (CP2 / D20 N×C
> grid / B3 compaction-at-scale).

> 🕐 **Runtime gotcha:** `size`/`mde` with the defaults (`--nsim 1000 --boot
> 1500`) sweep clusters 2→max and re-simulate at each step — that is **minutes**
> when the requirement is near the top of the sweep. For interactive sizing pass
> `--nsim 200 --boot 400` for a first pass (~30–40s; selftests use reduced
> values for the same reason), then confirm a final design at full nsim/boot.
> `size` returns the search ceiling if the requirement exceeds `--max-clusters`
> (default 24) — read that as "≥ceiling, possibly truncated", and re-run with a
> higher `--max-clusters` to resolve.

## Scope
`stats.py` already carries extractors for the two shapes that DO have per-unit
data today: **b0** (`committed_detail` / `absent_real_detail`) and **g6**
(`records`). Both are flagged single-seed/single-run. Everything else is
refused until it emits `per_unit`.
