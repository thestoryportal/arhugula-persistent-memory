---
name: clustered-design-power-determinism-cheaper-lever
description: "At the realized ~50pp swing, detecting a moderate corruption effect needs ≳15 order/seed clusters per arm — so determinism (cutting swing) is a cheaper lever than multiplying clusters; tools/stats.py + tools/power.py are the canonical engines."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7244974a-eeee-4aa8-83d0-ff7e3186f6d3
---

**Two canonical statistics tools now exist (committed 668306f, verified PASS 2026-06-24):**
- `tools/stats.py` — Phase-2 statistics engine: cluster_bootstrap over the real
  unit `(held-out-seed × edit-order)`, McNemar, Fisher two-prop, JS/KL divergence.
  **Refuses loudly on aggregate-only result JSONs** (you cannot bootstrap a scalar
  — the exact reason c2band could not be rescued post hoc). `selftest` = 11 PASS.
- `tools/power.py` — simulation-based power/MDE/size for the *clustered* design
  (`power`/`mde`/`size`, metrics `prop` and `cont`). The knob that matters is
  `--cluster-sd` / `--swing` (between-order/seed noise, the dominant variance).
  `selftest` = 6 PASS incl. null-calibration (effect=0 → power ≈ α). Convention
  for emitting analyzable per-unit data: `tools/STATS_LOGGING_CONVENTION.md`.

**The load-bearing finding (directional, NOT a point estimate):** at the realized
~50pp run-to-run swing (sd≈0.125, [[sequential-edit-run-nondeterminism]]), a
`power.py size` for a *moderate* ~20pp corruption effect (p0=0.70, items=8, 80%
power) lands around **≳15 order/seed clusters per arm** — an order of magnitude
above the convention doc's ≥4-clusters floor.

**Why:** ≥4 is *necessary* (just to have a cluster structure to bootstrap); ~15+
is *sufficiency* for a given effect/noise — necessary-not-sufficient, not a
contradiction. You **cannot items-per-cluster your way out**: the dominant
variance is *between* clusters, so adding held-out probes per order barely moves
power.

**How to apply:** **Reducing the swing (determinism) is a cheaper lever than
multiplying order/seed clusters.** This quantifies *why* the deterministic-
instrument next-arc item matters: at 50pp swing the clustered corruption design
is operationally heavy. Before committing GPU to any clustered corruption claim
(CP2 read/query contract, the D20 2D N×C grid, B3 compaction-at-scale — all the
§0.3 "gated on a larger stimulus pool" items), run `power.py size` against the
*measured* between-order SD first; many past single/double-seed runs were
underpowered by this standard ([[single-seed-limits-generality-not-significance]],
[[clustered-editing-trials-sampling-unit]], [[fixed-budget-sweep-couples-iv-with-complement]]).

**On the number:** ~16 clusters/arm, **reproduced at `--max-clusters 24 --nsim
400`** (not boundary-truncated — it had headroom to 24 and still crossed 0.8 at
16). Still Monte-Carlo noisy at the exact crossing (achieved_power landed exactly
0.80), so treat the *direction* (≈order-of-magnitude above the ≥4 floor,
determinism-is-the-cheaper-lever) as the durable claim, not a hard "16"
([[calibrate-confidence-mechanics-vs-contracts]]).
