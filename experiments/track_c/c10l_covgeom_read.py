#!/usr/bin/env python3
"""D-C10l-covgeom mechanical reader: applies the pre-registered §2 envelope and §5 readings to the harness result JSONs.
No model judgement; first matching label wins. Usage:
  python3 c10l_covgeom_read.py results/c10l_covgeom/armB.json [armC.json ...] [--p6 p6_zinject.json] [--step0 step0_offline.json]
Prints one table per run (arm A beside the candidate, every locality axis beside every held-out number) and the label.
"""
import sys, json, math

ENVELOPE = {"A1_para_full_min": 68, "A2_para_full_min": 68, "A7_canon_full": (5, 10), "A7_para_full": (11, 18), "A7_para_first": (48, 62)}
L3_RATE = 48 / 50          # the prereg's binding rate; amendment A1: pool is 30, threshold = ceil(0.96 * n)
P3A_TOL = 1e-4             # prereg P3(a); amendment A2: a miss is INVALID (fail-closed) until a default-vs-default jitter control re-sets it
K1_DELTA_NORMS = {"A1_single": {"4": 15.8739, "5": 12.0173, "6": 11.2447, "7": 18.9075, "8": 26.9384},
                  "A2_coherent2": {"4": 15.8855, "5": 12.2159, "6": 11.3733, "7": 18.8126, "8": 27.1968}}   # results/c10k_keying_ablation/K1.json (pre-knob, this machine)


def l3_threshold(n):
    return math.ceil(L3_RATE * n - 1e-9)


def arm_row(a):
    ax = a["locality_axes"]
    return {"canon": f"{a['canon_full_n']}/{a['canon_n']}", "para_full": f"{a['para_full_n']}/{a['para_n']}", "para_first": f"{a['para_first_n']}/{a['para_n']}",
            "para_string": f"{a['para_string_n']}/{a['para_n']}", "L1": f"{ax['L1_flipped_to_edited_value']}/{ax['L1_n']}", "described_as": a["locality_described_as"],
            "L3": f"{ax['L3_top1_agree']}/{ax['L3_n']}", "L3_kl": ax["L3_mean_kl"], "ppl": f"{ax['generic_ppl_pre']}->{ax['generic_ppl_post']}"}


def envelope_ok(base):
    a1, a2, a7 = base["A1_single"], base["A2_coherent2"], base["A7_coined_coined"]
    misses = []
    if a1["para_full_n"] < ENVELOPE["A1_para_full_min"]: misses.append(f"A1 para_full {a1['para_full_n']} < 68")
    if a2["para_full_n"] < ENVELOPE["A2_para_full_min"]: misses.append(f"A2 para_full {a2['para_full_n']} < 68")
    for key, (lo, hi) in (("canon_full", ENVELOPE["A7_canon_full"]), ("para_full", ENVELOPE["A7_para_full"]), ("para_first", ENVELOPE["A7_para_first"])):
        v = a7[f"{key}_n"]
        if not lo <= v <= hi: misses.append(f"A7 {key} {v} outside [{lo},{hi}]")
    return misses


def p3a(base_dn):
    worst = 0.0
    for arm, ref in K1_DELTA_NORMS.items():
        for l, v in ref.items():
            worst = max(worst, abs(base_dn[arm][l]["delta_norm"] - v) / v)
    return worst


def read(run):
    base_name = "baseline"; cand_name = [k for k in run["recipes"] if k != base_name][0]
    base, cand = run["recipes"][base_name], run["recipes"][cand_name]
    if "arms" not in base or "arms" not in cand:
        return {"label": "INVALID", "why": "LAW#5 failed in a recipe", "candidate": cand_name}
    misses = envelope_ok(base["arms"])
    b7, c7 = base["arms"]["A7_coined_coined"], cand["arms"]["A7_coined_coined"]
    n3 = c7["locality_axes"]["L3_n"]; thr3 = l3_threshold(n3)
    out = {"candidate": cand_name, "projector": cand.get("projector"), "band": cand["band"], "law5": {base_name: base["law5_gate"], cand_name: cand["law5_gate"]},
           "P2_envelope_misses": misses, "P3a_worst_rel_delta_norm_vs_K1": p3a(base["delta_norms"]),
           "L3_threshold": f">= {thr3}/{n3}", "rows": {f"A/{k}": arm_row(v) for k, v in base["arms"].items()} | {f"{cand_name}/{k}": arm_row(v) for k, v in cand["arms"].items()}}
    loc_ok = (c7["locality_axes"]["L1_flipped_to_edited_value"] <= b7["locality_axes"]["L1_flipped_to_edited_value"] + 1
              and c7["locality_described_as"] >= b7["locality_described_as"] - 3
              and c7["locality_axes"]["L3_top1_agree"] >= thr3)
    out["locality_conditions"] = {"L1": c7["locality_axes"]["L1_flipped_to_edited_value"] <= b7["locality_axes"]["L1_flipped_to_edited_value"] + 1,
                                  "described_as": c7["locality_described_as"] >= b7["locality_described_as"] - 3,
                                  "L3": c7["locality_axes"]["L3_top1_agree"] >= thr3}
    pf = c7["para_full_n"]; cf = c7["canon_full_n"]
    out["P3a_pass"] = out["P3a_worst_rel_delta_norm_vs_K1"] < P3A_TOL
    if (misses or not out["P3a_pass"] or not base["law5_gate"]["ok"] or not cand["law5_gate"]["ok"]
            or min(cand["arms"]["A1_single"]["para_full_n"], cand["arms"]["A2_coherent2"]["para_full_n"]) < 58
            or c7["locality_axes"]["L3_top1_agree"] < thr3):
        label = "INVALID"
        out["invalid_reasons"] = ([f"P2 envelope: {m}" for m in misses] + ([] if out["P3a_pass"] else [f"P3(a) worst rel delta_norm {out['P3a_worst_rel_delta_norm_vs_K1']:.2e} >= {P3A_TOL} (amendment A2: run the jitter control)"])
                                  + ([] if base["law5_gate"]["ok"] and cand["law5_gate"]["ok"] else ["LAW#5 gate failed"])
                                  + ([] if min(cand["arms"]["A1_single"]["para_full_n"], cand["arms"]["A2_coherent2"]["para_full_n"]) >= 58 else ["candidate A1/A2 < 58/72"])
                                  + ([] if c7["locality_axes"]["L3_top1_agree"] >= thr3 else [f"L3 {c7['locality_axes']['L3_top1_agree']} < {thr3}"]))
    elif pf >= 61 and loc_ok: label = "PASS"
    elif pf >= 30 and loc_ok: label = "LEAD"
    elif pf >= 30: label = "TRADEOFF"
    elif cf >= 15: label = "REALISATION-ONLY"
    else: label = "NULL"
    worse = [k for k, v in out["locality_conditions"].items() if not v]
    out["label"] = label
    out["note"] = ("flat gain with a worse locality axis = NULL with a locality cost" if label == "NULL" and worse else "")
    out["delta_A7_vs_A"] = {"para_full": pf - b7["para_full_n"], "canon_full": cf - b7["canon_full_n"], "para_first": c7["para_first_n"] - b7["para_first_n"]}
    return out


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]: j += 1
            for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y); n = len(x); mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def main():
    args = sys.argv[1:]; p6 = step0 = None; runs = []
    while args:
        a = args.pop(0)
        if a == "--p6": p6 = json.load(open(args.pop(0)))
        elif a == "--step0": step0 = json.load(open(args.pop(0)))
        else: runs.append((a, json.load(open(a))))
    suffix = ""
    if p6:
        print(f"P6 ceiling: canon_full_inj {p6['canon_full_inj']}/24  para_full_inj {p6['para_full_inj']}/72  -> {p6['reading']}")
        if p6["para_full_inj"] < 30: suffix = " (under a sub-LEAD target ceiling)"
    for path, run in runs:
        r = read(run)
        print(f"\n== {path}: candidate {r['candidate']} band {r.get('band')} projector {r.get('projector')} ==")
        for k, v in r.get("rows", {}).items(): print(f"  {k:28} {v}")
        print(f"  P2 envelope misses: {r.get('P2_envelope_misses')}  P3a worst rel |delta_norm| vs K1: {r.get('P3a_worst_rel_delta_norm_vs_K1')}")
        print(f"  LAW#5: {r.get('law5')}  L3 threshold {r.get('L3_threshold')}  locality conditions {r.get('locality_conditions')}")
        print(f"  delta A7 vs A: {r.get('delta_A7_vs_A')}")
        print(f"  LABEL: {r['label']}{suffix} {r.get('note','')} {r.get('invalid_reasons','')}")
        if step0 and r["candidate"].startswith("armB"):
            base = run["recipes"]["baseline"]["detail"]["A7_coined_coined"]
            per_subj_para = {row["subj"]: sum(row["para_full_hits"]) for row in base}
            rp = step0["regularisers"]["R0"]["band"]["rho_p_band_per_subject"]
            subs = [s for s in rp if s in per_subj_para]
            rho = spearman([rp[s] for s in subs], [per_subj_para[s] for s in subs])
            print(f"  step0 proxy validity: Spearman(rho_p_R0 per subject, arm-A para_full per subject) = {rho:.3f} -> {'informative' if abs(rho) >= 0.3 else 'UNINFORMATIVE (|rho| < 0.3)'}")
            print(f"  step0 predictions for arm B: {json.dumps(step0.get('predictions_for_arm_B'))}")
        if r["label"] == "LEAD" and r["candidate"].startswith("armC"):
            print("  (arm C vs C': credit to the spread only if C' does not also reach LEAD)")


if __name__ == "__main__":
    main()
