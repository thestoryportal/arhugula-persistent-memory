#!/usr/bin/env python3
"""power.py — simulation-based power / MDE for clustered editing trials.

Standalone tool (NOT a skill). Answers, BEFORE a run: can this design even
detect the claimed effect? It directly serves the #1 next action — sizing the
CP2 screened stimulus pool ("how many committed facts x seeds to detect a
margin-separation collapse at target power") is exactly this calculation.

WHY SIMULATION (not a closed-form power table):
  These trials are CLUSTERED and order-dominated. The dominant variance is
  BETWEEN order/seed (cluster level), not within-cluster binomial. A closed-form
  iid power calc models 100 Bernoulli draws -> ~+-5pp run-to-run swing and wildly
  OVER-estimates power. The real harness swings ~50pp run-to-run on the SAME
  config ([[sequential-edit-run-nondeterminism]]). So we simulate a cluster
  random effect and run the SAME cluster-bootstrap test stats.py uses.

THE KNOB THAT MATTERS — `--cluster-sd` (a.k.a. between-order noise):
  This is the SD, in pp, of the per-cluster (per-order/seed) outcome — NOT
  within-cluster binomial noise. The ~50pp figure in memory is a peak-to-peak
  SWING; pass it via `--swing 50` and it is converted to an SD (~swing/4, the
  normal ~4-sigma-range heuristic) ~= 12.5pp. Or set `--cluster-sd` directly if
  you have measured it. Get this component wrong and every number is wrong, so
  it is reported back explicitly in the output.

Two metrics:
  prop : binary clustered outcome (corruption / retention / read-correctness rate)
  cont : continuous clustered outcome (maxprob / margin SEPARATION) — the CP2 case

Usage:
  python3 tools/power.py selftest
  python3 tools/power.py power  --metric prop --p0 70 --effect 20 --clusters 4 --items 8 --swing 50
  python3 tools/power.py mde    --metric prop --p0 70 --clusters 4 --items 8 --swing 50 --target-power 0.8
  python3 tools/power.py size   --metric prop --p0 70 --effect 20 --items 8 --swing 50 --target-power 0.8
  python3 tools/power.py power  --metric cont --m0 0.55 --effect 0.30 --clusters 3 --items 10 \
                                --cluster-sd 0.08 --item-sd 0.10   # CP2 margin-separation sizing
"""
from __future__ import annotations
import argparse
import json
import sys

import numpy as np

# Reuse the EXACT test the analysis will use, so power matches reality.
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stats import cluster_bootstrap_diff  # noqa: E402


def _swing_to_sd(swing_pp: float) -> float:
    """Peak-to-peak swing (pp) -> SD (fraction). Normal range ~ 4 SD."""
    return (swing_pp / 100.0) / 4.0


def _simulate_arm(rng, metric, n_clusters, items, center, cluster_sd, item_sd):
    """Return (values, cluster_labels) for one arm.

    A cluster (order/seed) draws a latent level ~ N(center, cluster_sd), clipped;
    then `items` observations are drawn around that level. For 'prop' the items
    are Bernoulli(level); for 'cont' they are N(level, item_sd).
    """
    vals, labs = [], []
    for g in range(n_clusters):
        if metric == "prop":
            level = float(np.clip(rng.normal(center, cluster_sd), 0.0, 1.0))
            obs = (rng.random(items) < level).astype(float)
        else:  # cont
            level = rng.normal(center, cluster_sd)
            obs = rng.normal(level, item_sd, size=items)
        vals.extend(obs.tolist())
        labs.extend([g] * items)
    return vals, labs


def estimate_power(metric="prop", p0=0.7, effect=0.2, n_clusters=4, items=8,
                   cluster_sd=None, swing=None, item_sd=0.1, alpha=0.05,
                   nsim=1000, boot=1500, seed=0, m0=None) -> dict:
    """Fraction of simulated experiments whose cluster-bootstrap diff CI excludes 0."""
    if cluster_sd is None:
        if swing is None:
            raise ValueError("provide --cluster-sd or --swing")
        cluster_sd = _swing_to_sd(swing)
    if metric == "prop":
        c_ctrl, c_treat = p0, p0 + effect
    else:
        base = m0 if m0 is not None else p0
        c_ctrl, c_treat = base, base + effect
    rng = np.random.default_rng(seed)
    hits = 0
    for s in range(nsim):
        va, ca = _simulate_arm(rng, metric, n_clusters, items, c_treat, cluster_sd, item_sd)
        vb, cb = _simulate_arm(rng, metric, n_clusters, items, c_ctrl, cluster_sd, item_sd)
        r = cluster_bootstrap_diff(va, ca, vb, cb, nboot=boot, alpha=alpha,
                                   seed=int(rng.integers(1 << 30)))
        if r.get("significant"):
            hits += 1
    return {"metric": metric, "power": hits / nsim, "nsim": nsim,
            "n_clusters_per_arm": n_clusters, "items_per_cluster": items,
            "effect": effect, "control_center": c_ctrl, "treat_center": c_treat,
            "cluster_sd_used": cluster_sd,
            "cluster_sd_source": f"swing {swing}pp -> sd {cluster_sd:.4f}" if swing else "direct",
            "item_sd": item_sd if metric == "cont" else None,
            "alpha": alpha, "boot": boot, "seed": seed,
            "NOTE": "cluster_sd is BETWEEN-order/seed noise, the dominant component. "
                    "If this is wrong, the power is wrong."}


def solve_mde(target_power=0.8, lo=0.01, hi=0.95, tol=0.01, **kw) -> dict:
    """Smallest effect reaching target power (bisection on a monotone-ish curve)."""
    kw.pop("effect", None)
    def power_at(e):
        return estimate_power(effect=e, **kw)["power"]
    if power_at(hi) < target_power:
        return {"mde": None, "reason": f"even effect={hi} gives power<{target_power}; "
                "design too weak — add clusters (seeds x orders).", "target_power": target_power}
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if power_at(mid) >= target_power:
            hi = mid
        else:
            lo = mid
    return {"mde": round(hi, 3), "target_power": target_power,
            "at_design": {"clusters_per_arm": kw.get("n_clusters"), "items": kw.get("items")},
            "interpretation": "smallest effect this design can detect at the target power"}


def solve_size(target_power=0.8, effect=0.2, max_clusters=24, **kw) -> dict:
    """Smallest #clusters-per-arm (= seeds x orders) reaching target power."""
    kw.pop("n_clusters", None)
    for g in range(2, max_clusters + 1):
        p = estimate_power(effect=effect, n_clusters=g, **kw)["power"]
        if p >= target_power:
            return {"required_clusters_per_arm": g, "achieved_power": p,
                    "effect": effect, "target_power": target_power,
                    "reading": f"need >= {g} order/seed clusters per arm "
                               f"(e.g. {g} orderings, or seeds x orderings) to detect "
                               f"a {effect} effect at power {target_power}."}
    return {"required_clusters_per_arm": None, "effect": effect,
            "reason": f"even {max_clusters} clusters/arm fall short — effect too small "
                      "vs between-order noise; reconsider the claim or reduce noise "
                      "(e.g. determinism)."}


# -----------------------------------------------------------------------------
# Self-tests — the killer is null calibration: under zero effect, power ~ alpha.
# -----------------------------------------------------------------------------

def selftest() -> int:
    fails = []
    def check(name, cond, detail=""):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}  {detail}")
        if not cond:
            fails.append(name)

    # 1. NULL CALIBRATION (the killer). effect=0 -> power ~ alpha (false-positive rate).
    null = estimate_power(metric="prop", p0=0.6, effect=0.0, n_clusters=5, items=10,
                          cluster_sd=0.08, alpha=0.05, nsim=600, boot=800, seed=7)
    check("prop null power ~ alpha (<=0.10)", null["power"] <= 0.10,
          f"power={null['power']:.3f}")

    nullc = estimate_power(metric="cont", m0=0.5, effect=0.0, n_clusters=5, items=10,
                           cluster_sd=0.06, item_sd=0.1, alpha=0.05, nsim=600, boot=800, seed=9)
    check("cont null power ~ alpha (<=0.10)", nullc["power"] <= 0.10,
          f"power={nullc['power']:.3f}")

    # 2. Large effect + low noise -> power -> 1.
    strong = estimate_power(metric="prop", p0=0.3, effect=0.5, n_clusters=8, items=20,
                            cluster_sd=0.03, alpha=0.05, nsim=400, boot=800, seed=3)
    check("strong effect, low noise -> power >= 0.9", strong["power"] >= 0.9,
          f"power={strong['power']:.3f}")

    # 3. More between-order noise REDUCES power (the whole reason for simulation).
    lo_noise = estimate_power(metric="prop", p0=0.5, effect=0.2, n_clusters=4, items=10,
                              cluster_sd=0.05, nsim=400, boot=800, seed=4)["power"]
    hi_noise = estimate_power(metric="prop", p0=0.5, effect=0.2, n_clusters=4, items=10,
                              cluster_sd=0.25, nsim=400, boot=800, seed=4)["power"]
    check("more between-order noise lowers power", hi_noise < lo_noise,
          f"sd0.05->{lo_noise:.3f}  sd0.25->{hi_noise:.3f}")

    # 4. swing->sd conversion is the documented ~swing/4.
    check("swing 50pp -> sd ~0.125", abs(_swing_to_sd(50) - 0.125) < 1e-9)

    # 5. More clusters -> more power (monotone in sample of clusters).
    g2 = estimate_power(metric="prop", p0=0.5, effect=0.25, n_clusters=3, items=10,
                        cluster_sd=0.1, nsim=400, boot=800, seed=5)["power"]
    g8 = estimate_power(metric="prop", p0=0.5, effect=0.25, n_clusters=10, items=10,
                        cluster_sd=0.1, nsim=400, boot=800, seed=5)["power"]
    check("more clusters -> more power", g8 > g2, f"3->{g2:.3f}  10->{g8:.3f}")

    print(f"\n  {'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
    return 1 if fails else 0


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _common(p):
    p.add_argument("--metric", choices=["prop", "cont"], default="prop")
    p.add_argument("--p0", type=float, help="control rate (prop, 0-1 or 0-100)")
    p.add_argument("--m0", type=float, help="control mean (cont)")
    p.add_argument("--items", type=int, default=8, help="items per cluster (held-out probes per order)")
    p.add_argument("--cluster-sd", type=float, help="BETWEEN-order/seed SD (fraction)")
    p.add_argument("--swing", type=float, help="peak-to-peak run-to-run swing in pp (-> sd=swing/4)")
    p.add_argument("--item-sd", type=float, default=0.1, help="within-cluster SD (cont only)")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--nsim", type=int, default=1000)
    p.add_argument("--boot", type=int, default=1500)
    p.add_argument("--seed", type=int, default=0)


def _norm(v):
    """Accept either 0-1 or 0-100 for rates/effects -> fraction."""
    return v / 100.0 if v is not None and v > 1.0 else v


def main(argv=None):
    ap = argparse.ArgumentParser(description="Simulation-based power/MDE for clustered editing trials.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("selftest")

    pp = sub.add_parser("power", help="power for a given design + effect")
    _common(pp); pp.add_argument("--effect", type=float, required=True)
    pp.add_argument("--clusters", type=int, required=True)

    pm = sub.add_parser("mde", help="min detectable effect at target power")
    _common(pm); pm.add_argument("--clusters", type=int, required=True)
    pm.add_argument("--target-power", type=float, default=0.8)

    ps = sub.add_parser("size", help="required #clusters (seeds x orders) for an effect")
    _common(ps); ps.add_argument("--effect", type=float, required=True)
    ps.add_argument("--target-power", type=float, default=0.8)
    ps.add_argument("--max-clusters", type=int, default=24)

    args = ap.parse_args(argv)
    if args.cmd == "selftest":
        return selftest()

    kw = dict(metric=args.metric, p0=_norm(args.p0) if args.p0 is not None else 0.5,
              m0=_norm(args.m0) if args.m0 is not None else None,
              items=args.items, cluster_sd=args.cluster_sd, swing=args.swing,
              item_sd=args.item_sd, alpha=args.alpha, nsim=args.nsim,
              boot=args.boot, seed=args.seed)

    if args.cmd == "power":
        out = estimate_power(effect=_norm(args.effect), n_clusters=args.clusters, **kw)
    elif args.cmd == "mde":
        out = solve_mde(target_power=args.target_power, n_clusters=args.clusters, **kw)
    elif args.cmd == "size":
        out = solve_size(target_power=args.target_power, effect=_norm(args.effect),
                         max_clusters=args.max_clusters, items=args.items,
                         metric=args.metric, p0=kw["p0"], m0=kw["m0"],
                         cluster_sd=args.cluster_sd, swing=args.swing,
                         item_sd=args.item_sd, alpha=args.alpha,
                         nsim=args.nsim, boot=args.boot, seed=args.seed)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
