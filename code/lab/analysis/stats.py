#!/usr/bin/env python3
"""stats.py — the Phase-2 statistics engine for LLM-as-Database experiments.

Standalone tool (NOT a skill). Computes the *correct* statistics for this
program's clustered, order-dominated editing trials, on PER-UNIT arrays.

Design constraints (from the EXPERIMENT_GATE spec §0 + advisor review):
  * Core = pure functions on per-unit arrays. Import it, or call the CLI.
  * The unit is (held-out-set x edit-order). iid/Wilson is INVALID for these;
    use cluster_bootstrap, resampling whole clusters.
  * REFUSE LOUDLY on aggregate-only results. Most saved result JSONs carry
    only reduced percentages (one scalar per arm) — you cannot bootstrap a
    scalar, and single-seed runs have no order-cluster to resample. Synthesizing
    clusters from a % is the exact false-rigor this tool exists to prevent.
  * Determinism (CLAUDE.md LAW): every bootstrap takes an explicit --seed.
  * The prereg stays ADVISORY — thresholds are read by a human, not parsed out
    of freeform markdown. This tool computes numbers; it does not pick verdicts.

Forward dependency (a deliverable, see tools/STATS_LOGGING_CONVENTION.md):
  cluster_bootstrap over (held-out x order) needs the harness to EMIT per-
  held-out-item x per-order outcomes. That logging convention is why c2band
  was "underpowered" and could not be rescued post hoc.

Usage:
  python3 tools/stats.py selftest
  python3 tools/stats.py from-result results/b0_select_primitive_pilot.json
  python3 tools/stats.py paired --a a.json --b b.json        # 0/1 vectors, same units
  python3 tools/stats.py twoprop --succ1 12 --n1 16 --succ2 7 --n2 16
  python3 tools/stats.py cluster --data clusters.json        # {"values":[...],"clusters":[...]}
  python3 tools/stats.py divergence --p p.json --q q.json    # probability vectors
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from typing import Sequence

import numpy as np
from scipy import stats as sps

# -----------------------------------------------------------------------------
# Binary / proportion tests
# -----------------------------------------------------------------------------

def mcnemar_exact(b: int, c: int) -> dict:
    """Exact two-sided McNemar for PAIRED binary outcomes.

    b = # units where A succeeded and B failed (discordant one way)
    c = # units where A failed and B succeeded (discordant other way)
    Concordant pairs carry no information and are excluded.
    Exact test = two-sided binomial(min(b,c); n=b+c, p=0.5).
    """
    n = b + c
    if n == 0:
        return {"test": "mcnemar_exact", "b": b, "c": c, "n_discordant": 0,
                "p_value": 1.0, "note": "no discordant pairs — no information"}
    res = sps.binomtest(min(b, c), n, 0.5, alternative="two-sided")
    return {"test": "mcnemar_exact", "b": b, "c": c, "n_discordant": n,
            "p_value": float(res.pvalue)}


def paired_binary(a: Sequence[int], b: Sequence[int]) -> dict:
    """McNemar on two 0/1 vectors measured on the SAME units (paired)."""
    a = np.asarray(a, dtype=int)
    b = np.asarray(b, dtype=int)
    if a.shape != b.shape:
        raise ValueError(f"paired vectors must match: {a.shape} vs {b.shape}")
    n01 = int(np.sum((a == 0) & (b == 1)))
    n10 = int(np.sum((a == 1) & (b == 0)))
    out = mcnemar_exact(n10, n01)
    out.update({"n_pairs": int(a.size),
                "a_successes": int(a.sum()), "b_successes": int(b.sum())})
    return out


def two_proportion(succ1: int, n1: int, succ2: int, n2: int) -> dict:
    """Two INDEPENDENT proportions: Fisher exact (primary) + normal-approx z.

    Fisher is exact and correct at the small n this program runs at; the z is
    reported only for context and is unreliable below ~10 successes per cell.
    """
    table = [[succ1, n1 - succ1], [succ2, n2 - succ2]]
    odds, p_fisher = sps.fisher_exact(table, alternative="two-sided")
    p1, p2 = succ1 / n1, succ2 / n2
    p_pool = (succ1 + succ2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2)) if 0 < p_pool < 1 else 0.0
    z = (p1 - p2) / se if se > 0 else 0.0
    p_z = 2 * (1 - sps.norm.cdf(abs(z))) if se > 0 else 1.0
    return {"test": "two_proportion", "p1": p1, "p2": p2, "diff_pp": (p1 - p2) * 100,
            "fisher_p": float(p_fisher), "z": float(z), "z_p": float(p_z),
            "note": "Fisher is primary; z is unreliable for small cells"}


def binomial_ci(successes: int, n: int, alpha: float = 0.05) -> dict:
    """Clopper-Pearson exact CI for a SINGLE proportion (one run, no clustering).

    Honest only for a genuinely iid sample. For clustered/order-dominated data
    this UNDER-covers — use cluster_bootstrap and read the flag below.
    """
    lo, hi = sps.binomtest(successes, n).proportion_ci(1 - alpha, method="exact")
    return {"rate": successes / n if n else float("nan"), "n": n,
            "ci_lo": float(lo), "ci_hi": float(hi), "alpha": alpha,
            "method": "clopper-pearson (iid)",
            "flag": "iid CI — INVALID if outcomes are clustered by order/seed"}


# -----------------------------------------------------------------------------
# Cluster bootstrap  (the unit = held-out-set x edit-order)
# -----------------------------------------------------------------------------

def cluster_bootstrap_mean(values: Sequence[float], clusters: Sequence,
                           nboot: int = 10000, alpha: float = 0.05,
                           seed: int = 0) -> dict:
    """Cluster (block) bootstrap CI for the mean. Resamples whole clusters
    with replacement, then all items within each drawn cluster. Wider than iid
    when outcomes correlate within cluster; collapses to iid when every cluster
    is a singleton.
    """
    values = np.asarray(values, dtype=float)
    clusters = np.asarray(clusters)
    uniq = np.unique(clusters)
    if uniq.size < 2:
        return {"test": "cluster_bootstrap_mean", "n_clusters": int(uniq.size),
                "point": float(values.mean()) if values.size else float("nan"),
                "REFUSED": True,
                "reason": f"only {uniq.size} cluster — cannot bootstrap over clusters; "
                          "a single seed/order has no resampling unit (this is exactly "
                          "the c2band underpowered case)."}
    by = {u: values[clusters == u] for u in uniq}
    rng = np.random.default_rng(seed)
    means = np.empty(nboot)
    for i in range(nboot):
        drawn = rng.choice(uniq, size=uniq.size, replace=True)
        means[i] = np.concatenate([by[u] for u in drawn]).mean()
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {"test": "cluster_bootstrap_mean", "point": float(values.mean()),
            "ci_lo": float(lo), "ci_hi": float(hi), "n_clusters": int(uniq.size),
            "n_items": int(values.size), "nboot": nboot, "alpha": alpha, "seed": seed}


def cluster_bootstrap_diff(values_a, clusters_a, values_b, clusters_b,
                           nboot: int = 10000, alpha: float = 0.05,
                           seed: int = 0) -> dict:
    """Difference of arm means (A - B), analyzed at the CLUSTER level.

    SIGNIFICANCE is decided by a Welch t-test on the per-cluster means (each
    cluster -> one number), with G-1 df. This is the principled small-G method:
    a *percentile* cluster bootstrap is anti-conservative below ~15-20 clusters
    (it over-rejects ~2x at G=5), which would manufacture false positives in
    exactly the few-seed regime this program runs at. The bootstrap interval is
    still reported as a supplementary effect estimate, but it does NOT drive the
    verdict. CI/verdict agree because both are reported; trust the t-test at
    small G.
    """
    va, ca = np.asarray(values_a, float), np.asarray(clusters_a)
    vb, cb = np.asarray(values_b, float), np.asarray(clusters_b)
    ua, ub = np.unique(ca), np.unique(cb)
    if ua.size < 2 or ub.size < 2:
        return {"test": "cluster_diff", "REFUSED": True,
                "n_clusters_a": int(ua.size), "n_clusters_b": int(ub.size),
                "reason": "each arm needs >=2 clusters to compare a difference."}
    cm_a = np.array([va[ca == u].mean() for u in ua])   # cluster-level means
    cm_b = np.array([vb[cb == u].mean() for u in ub])
    ma, mb = cm_a.mean(), cm_b.mean()
    sa2, sb2 = cm_a.var(ddof=1), cm_b.var(ddof=1)
    na, nb = ua.size, ub.size
    se = math.sqrt(sa2 / na + sb2 / nb)
    if se > 0:                                            # Welch on cluster means
        df = (sa2 / na + sb2 / nb) ** 2 / ((sa2 / na) ** 2 / (na - 1) + (sb2 / nb) ** 2 / (nb - 1))
        tstat = (ma - mb) / se
        p_t = float(2 * sps.t.sf(abs(tstat), df))
        tcrit = sps.t.ppf(1 - alpha / 2, df)
        welch_lo, welch_hi = (ma - mb) - tcrit * se, (ma - mb) + tcrit * se
    else:                                                # degenerate (zero variance both arms)
        tstat = float("inf") if ma != mb else 0.0
        p_t = 0.0 if ma != mb else 1.0
        welch_lo = welch_hi = ma - mb
    # supplementary percentile bootstrap interval (descriptive only)
    ba = {u: va[ca == u] for u in ua}
    bb = {u: vb[cb == u] for u in ub}
    rng = np.random.default_rng(seed)
    diffs = np.empty(nboot)
    for i in range(nboot):
        da = rng.choice(ua, size=ua.size, replace=True)
        db = rng.choice(ub, size=ub.size, replace=True)
        diffs[i] = np.concatenate([ba[u] for u in da]).mean() - np.concatenate([bb[u] for u in db]).mean()
    boot_lo, boot_hi = np.quantile(diffs, [alpha / 2, 1 - alpha / 2])
    return {"test": "cluster_diff (Welch-t on cluster means; bootstrap supplementary)",
            "diff_point": float(va.mean() - vb.mean()),
            "ci_lo": float(welch_lo), "ci_hi": float(welch_hi),
            "welch_t": float(tstat), "welch_p": float(p_t),
            "significant": bool(p_t < alpha),
            "boot_ci_lo": float(boot_lo), "boot_ci_hi": float(boot_hi),
            "n_clusters_a": int(ua.size), "n_clusters_b": int(ub.size),
            "nboot": nboot, "alpha": alpha, "seed": seed,
            "note": "verdict = Welch-t on cluster means (calibrated at small G); "
                    "percentile bootstrap CI reported but anti-conservative below ~15 clusters."}


# -----------------------------------------------------------------------------
# Distributional divergences  (for JS/KL claims — read corruption etc.)
# -----------------------------------------------------------------------------

def _as_dist(p) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    if np.any(p < 0):
        raise ValueError("probabilities must be >= 0")
    s = p.sum()
    if s <= 0:
        raise ValueError("distribution sums to 0")
    return p / s


def kl_divergence(p, q, base: float = 2.0) -> float:
    """KL(p || q) in bits (base 2). q must cover p's support."""
    p, q = _as_dist(p), _as_dist(q)
    mask = p > 0
    if np.any(q[mask] == 0):
        return float("inf")
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])) / math.log(base))


def js_divergence(p, q, base: float = 2.0) -> float:
    """Jensen-Shannon divergence in bits — symmetric, bounded [0, 1] in base 2."""
    p, q = _as_dist(p), _as_dist(q)
    m = 0.5 * (p + q)
    return float(0.5 * kl_divergence(p, m, base) + 0.5 * kl_divergence(q, m, base))


def js_bootstrap_ci(samples_p: Sequence, samples_q: Sequence, n_categories: int = None,
                    nboot: int = 10000, alpha: float = 0.05, seed: int = 0) -> dict:
    """Bootstrap CI for JS between two empirical categorical distributions,
    resampling the underlying SAMPLES (not the reduced histograms)."""
    sp = np.asarray(samples_p, dtype=int)
    sq = np.asarray(samples_q, dtype=int)
    k = n_categories or int(max(sp.max(), sq.max()) + 1)

    def hist(s):
        return np.bincount(s, minlength=k).astype(float)

    point = js_divergence(hist(sp), hist(sq))
    rng = np.random.default_rng(seed)
    vals = np.empty(nboot)
    for i in range(nboot):
        rp = rng.choice(sp, size=sp.size, replace=True)
        rq = rng.choice(sq, size=sq.size, replace=True)
        vals[i] = js_divergence(hist(rp), hist(rq))
    lo, hi = np.quantile(vals, [alpha / 2, 1 - alpha / 2])
    return {"test": "js_bootstrap_ci", "js_point": point,
            "ci_lo": float(lo), "ci_hi": float(hi),
            "n_p": int(sp.size), "n_q": int(sq.size), "n_categories": k,
            "nboot": nboot, "alpha": alpha, "seed": seed}


# -----------------------------------------------------------------------------
# Extractors — ONLY for result shapes that genuinely carry per-unit arrays.
# Everything else is refused. (No confounder logic here — that is audit.py's
# job, deliberately out of scope.)
# -----------------------------------------------------------------------------

def _extract_b0(d: dict) -> dict:
    """b0 SELECT pilot: per-item maxprob + correctness arrays."""
    comm = d["committed_detail"]
    leak = d.get("absent_real_detail", [])
    comm_mp = np.array([x["maxprob"] for x in comm])
    leak_mp = np.array([x["maxprob"] for x in leak])
    comm_corr = np.array([1 if x.get("correct") else 0 for x in comm])
    leak_corr = np.array([1 if x.get("top1", "").strip() == x.get("truth", "").strip()
                          else 0 for x in leak])
    out = {"shape": "b0_select_pilot", "single_seed": True,
           "committed": {"n": len(comm), "readback": binomial_ci(int(comm_corr.sum()), len(comm)),
                         "maxprob_min": float(comm_mp.min()), "maxprob_median": float(np.median(comm_mp))},
           "leak_absent_real": {"n": len(leak),
                                "readback": binomial_ci(int(leak_corr.sum()), len(leak)) if len(leak) else None,
                                "maxprob_max": float(leak_mp.max()) if len(leak) else None,
                                "maxprob_median": float(np.median(leak_mp)) if len(leak) else None}}
    if len(leak):
        u = sps.mannwhitneyu(comm_mp, leak_mp, alternative="greater")
        out["committed_vs_leak_maxprob"] = {
            "test": "mann_whitney_u (committed > leak)", "U": float(u.statistic),
            "p_value": float(u.pvalue),
            "separation_gap": float(comm_mp.min() - leak_mp.max()),
            "note": "gap = min(committed) - max(leak). The committed side is "
                    "margin-INFLATED by construction (compute_z ~0.99); the only "
                    "un-confounded signal is the leak channel. Single seed."}
    out["WARNING"] = ("Single seed, n<=8, one relation. binomial_ci is iid — "
                      "NOT a reliability claim. Promotion needs scale + quantization + >=2 seeds.")
    return out


def _extract_g6_records(d: dict) -> dict:
    """g6 scale-n: per-record expression + retention booleans (single run)."""
    recs = d["records"]
    expr = np.array([1 if r.get("expressed_at_apply") else 0 for r in recs])
    ret = np.array([1 if r.get("retained_at_end") else 0 for r in recs])
    return {"shape": "g6_records", "single_run": True, "n_records": len(recs),
            "expression": binomial_ci(int(expr.sum()), len(recs)),
            "retention": binomial_ci(int(ret.sum()), len(recs)),
            "WARNING": ("Single run, no order-cluster. iid CIs only. Sequential-edit "
                        "runs swing ~50pp run-to-run (between-order); a one-run CI does "
                        "NOT capture that. Needs >=2 orders to cluster-bootstrap.")}


def analyze_result(path: str) -> dict:
    with open(path) as f:
        d = json.load(f)
    if "committed_detail" in d:
        return _extract_b0(d)
    if isinstance(d.get("records"), list) and d["records"] and "retained_at_end" in d["records"][0]:
        return _extract_g6_records(d)
    # Refuse loudly — this is the whole point.
    return {"REFUSED": True, "path": path,
            "reason": "Aggregate-only result: no per-unit arrays found "
                      "(expected 'committed_detail' or per-record 'records'). "
                      "This file carries reduced percentages only. You CANNOT "
                      "bootstrap a scalar, and a single seed has no cluster to "
                      "resample. To make a result analyzable, emit per-(held-out "
                      "x order) outcomes — see tools/STATS_LOGGING_CONVENTION.md.",
            "keys_present": sorted(d.keys())}


# -----------------------------------------------------------------------------
# Self-tests  (gate "done": stats bugs hide in correctness)
# -----------------------------------------------------------------------------

def selftest() -> int:
    fails = []

    def check(name, cond):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    # JS/KL identities
    p = [0.25, 0.25, 0.25, 0.25]
    check("KL(p||p) == 0", abs(kl_divergence(p, p)) < 1e-12)
    check("JS(p||p) == 0", abs(js_divergence(p, p)) < 1e-12)
    check("JS symmetric", abs(js_divergence([0.9, 0.1], [0.2, 0.8]) -
                               js_divergence([0.2, 0.8], [0.9, 0.1])) < 1e-12)
    check("JS bounded <= 1 bit", js_divergence([1, 0], [0, 1]) <= 1.0 + 1e-9 and
                                  js_divergence([1, 0], [0, 1]) > 0.99)

    # McNemar vs hand value: b=10,c=0 -> p = 2*0.5^10 (two-sided) = 0.001953125
    mc = mcnemar_exact(10, 0)
    check("McNemar(10,0) exact == 2*0.5^10", abs(mc["p_value"] - 2 * 0.5 ** 10) < 1e-9)
    check("McNemar(0,0) -> p=1", mcnemar_exact(0, 0)["p_value"] == 1.0)

    # Fisher vs scipy direct
    tp = two_proportion(8, 10, 2, 10)
    _, p_ref = sps.fisher_exact([[8, 2], [2, 8]])
    check("two_proportion Fisher matches scipy", abs(tp["fisher_p"] - p_ref) < 1e-12)

    # cluster_bootstrap: refuses on <2 clusters
    r1 = cluster_bootstrap_mean([1, 0, 1], [0, 0, 0], nboot=200)
    check("cluster_bootstrap refuses single cluster", r1.get("REFUSED") is True)

    # cluster_bootstrap widens vs iid when intra-cluster correlation is high.
    rng = np.random.default_rng(1)
    G, m = 6, 20
    cluster_means = rng.uniform(0.2, 0.8, G)        # strong between-cluster variance
    vals, cl = [], []
    for g in range(G):
        vals += list((rng.random(m) < cluster_means[g]).astype(int)); cl += [g] * m
    cb = cluster_bootstrap_mean(vals, cl, nboot=4000, seed=0)
    iid_w = 2 * 1.96 * math.sqrt(np.mean(vals) * (1 - np.mean(vals)) / len(vals))
    clu_w = cb["ci_hi"] - cb["ci_lo"]
    check("cluster CI wider than iid under intra-cluster corr", clu_w > iid_w)

    # cluster_bootstrap ~ iid when clusters are singletons
    rng = np.random.default_rng(2)
    v = (rng.random(120) < 0.5).astype(int)
    cb_s = cluster_bootstrap_mean(v, np.arange(120), nboot=4000, seed=0)
    iid_w2 = 2 * 1.96 * math.sqrt(np.mean(v) * (1 - np.mean(v)) / len(v))
    check("singleton clusters ~ iid width (within 25%)",
          abs((cb_s["ci_hi"] - cb_s["ci_lo"]) - iid_w2) / iid_w2 < 0.25)

    # diff CI: identical arms -> straddles 0 (not significant)
    rng = np.random.default_rng(3)
    va = (rng.random(80) < 0.5).astype(int); ca = np.repeat(np.arange(4), 20)
    vb = (rng.random(80) < 0.5).astype(int); cb2 = np.repeat(np.arange(4), 20)
    d0 = cluster_bootstrap_diff(va, ca, vb, cb2, nboot=4000, seed=0)
    check("equal arms -> diff not significant", d0["significant"] is False)

    print(f"\n  {'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
    return 1 if fails else 0


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _load_vec(path):
    with open(path) as f:
        return json.load(f)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Phase-2 statistics engine (per-unit arrays).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("selftest", help="run correctness self-tests (gates 'done')")

    p_fr = sub.add_parser("from-result", help="auto-extract per-unit arrays from a result JSON")
    p_fr.add_argument("result")

    p_pa = sub.add_parser("paired", help="McNemar on two paired 0/1 vectors (JSON lists)")
    p_pa.add_argument("--a", required=True); p_pa.add_argument("--b", required=True)

    p_tp = sub.add_parser("twoprop", help="Fisher exact on two independent proportions")
    for a in ("succ1", "n1", "succ2", "n2"):
        p_tp.add_argument(f"--{a}", type=int, required=True)

    p_cl = sub.add_parser("cluster", help='cluster-bootstrap mean: {"values":[],"clusters":[]}')
    p_cl.add_argument("--data", required=True)
    p_cl.add_argument("--seed", type=int, default=0); p_cl.add_argument("--nboot", type=int, default=10000)

    p_dv = sub.add_parser("divergence", help="JS + KL between two probability vectors")
    p_dv.add_argument("--p", required=True); p_dv.add_argument("--q", required=True)

    args = ap.parse_args(argv)

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "from-result":
        out = analyze_result(args.result)
    elif args.cmd == "paired":
        out = paired_binary(_load_vec(args.a), _load_vec(args.b))
    elif args.cmd == "twoprop":
        out = two_proportion(args.succ1, args.n1, args.succ2, args.n2)
    elif args.cmd == "cluster":
        d = _load_vec(args.data)
        out = cluster_bootstrap_mean(d["values"], d["clusters"], nboot=args.nboot, seed=args.seed)
    elif args.cmd == "divergence":
        p, q = _load_vec(args.p), _load_vec(args.q)
        out = {"js_bits": js_divergence(p, q), "kl_p_q_bits": kl_divergence(p, q),
               "kl_q_p_bits": kl_divergence(q, p)}
    print(json.dumps(out, indent=2))
    return 1 if isinstance(out, dict) and out.get("REFUSED") else 0


if __name__ == "__main__":
    sys.exit(main())
