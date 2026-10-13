#!/usr/bin/env python3
"""D-C10l-mint mechanical reader (§6 of experiments/c10l/design/C10L_MINT_TOKEN_PREREG.md as amended by §10 B1). No model judgement.
Usage: c10l_mint_read.py experiments/c10l/runs/c10l_mint/step0_probe.json arm_multi.json arm_rare.json arm_G.json [arm_N.json arm_M.json arm_Z.json]
The binding mint score is `para_full_binding_n` (post-write minus step-0); raw para_full_n is never read for a mint arm.
Comparators: A1 from the SAME run as the candidate; locality baseline = the A7-multi run's A7 arm.
"""
import sys, json, math

ENVELOPE = {"canon_full": (5, 10), "para_full": (11, 18), "para_first": (48, 62)}
L3_THR = math.ceil(0.96 * 30 - 1e-9)   # covgeom amendment A1 pool, same rate


def arms(run):
    cand = [k for k in run["recipes"] if k != "baseline"][0]
    return cand, run["recipes"][cand]


def row(a, binding=None):
    ax = a["locality_axes"]
    return {"binding": binding if binding is not None else a["para_full_n"], "para_full_raw": a["para_full_n"], "canon": a["canon_full_n"],
            "para_first": a["para_first_n"], "string": a["para_string_n"], "L1": ax["L1_flipped_to_edited_value"],
            "described_as": a["locality_described_as"], "L3": ax["L3_top1_agree"], "L3_kl": ax["L3_mean_kl"],
            "sibling": a.get("extra", {}).get("para_sibling"), "cannibal_post": a.get("extra", {}).get("post_write_cannibal")}


def main():
    step0 = json.load(open(sys.argv[1]))
    runs = {}
    for p in sys.argv[2:]:
        r = json.load(open(p)); runs[r["mint_arm"]] = r
    print(f"step 0: P2a {step0['P2a_prompts_identical']} pass={step0['P2a_pass']}  admitted inits {step0['admitted_inits']}")
    for k, v in step0["inits"].items():
        print(f"  init {k}: eff_rank {v['piv']['effective_rank']} cos_mean {v['piv']['cos_mean']} collapsed={v['collapsed']} step0 para_full {v['probe']['para_full_step0']}/72 classes {v['probe']['classes']} P3 {v['P3_compute_z']['n_ge_0.98']}/24 excluded={v['excluded_from_arms']} {v['exclusion_reason']}")
    multi = runs.get("multi"); rare = runs.get("rare")
    inval = []
    if multi is None:
        inval.append("A7-multi run missing")
    else:
        _, m = arms(multi); m7 = m["arms"]["A7_coined_coined"]
        for key, (lo, hi) in ENVELOPE.items():
            if not lo <= m7[f"{key}_n"] <= hi: inval.append(f"A7-multi {key} {m7[f'{key}_n']} outside [{lo},{hi}]")
        print(f"\nA7-multi: {row(m7)}  per-position {m7.get('extra', {}).get('per_position_teacher_forced')}")
        print(f"A1 (multi run): {row(m['arms']['A1_single'])}")
    if not step0["P2a_pass"]: inval.append("P2 failed")
    if rare is not None:
        _, rr = arms(rare); r1 = rr["arms"]["A1_rare"]
        print(f"A1-rare: {row(r1)}   A1 (rare run): {row(rr['arms']['A1_single'])}")
    for init in ("G", "N", "M", "Z"):
        run = runs.get(init)
        if run is None: continue
        _, c = arms(run); a7 = c["arms"]["A7_coined_coined"]; a1 = c["arms"]["A1_single"]
        b = a7["para_full_binding_n"]
        reasons = list(inval)
        if a1["para_full_n"] < 58: reasons.append(f"A1 {a1['para_full_n']} < 58")
        if not step0["inits"][init]["P3_compute_z"]["pass"]: reasons.append("P3 failed")
        if a7["locality_axes"]["L3_top1_agree"] < L3_THR: reasons.append(f"L3 {a7['locality_axes']['L3_top1_agree']} < {L3_THR}")
        base7 = arms(multi)[1]["arms"]["A7_coined_coined"] if multi else None
        loc_ok = base7 is not None and (a7["locality_axes"]["L1_flipped_to_edited_value"] <= base7["locality_axes"]["L1_flipped_to_edited_value"] + 1
                                        and a7["locality_described_as"] >= base7["locality_described_as"] - 3
                                        and a7["locality_axes"]["L3_top1_agree"] >= L3_THR)
        ex = a7.get("extra", {})
        bounds_ok = ex.get("post_write_cannibal", 99) <= 2 and ex.get("para_sibling", 99) <= 3
        a1n = a1["para_full_n"]
        print(f"\nA7-mint-{init}: {row(a7, b)}   A1 (same run): {a1n}/72   loc_ok={loc_ok} bounds_ok={bounds_ok}")
        if reasons: label = "INVALID"
        elif b >= a1n - 5 and b >= 30 and loc_ok and bounds_ok: label = "SPAN"
        elif b >= 30 and b < a1n - 5 and loc_ok and bounds_ok: label = "PARTIAL"
        elif b >= 30: label = "TRADEOFF"
        else: label = "NOVELTY (with these inits)"
        print(f"  LABEL {init}: {label} {reasons if reasons else ''}")
        if init == "G":
            if label.startswith("NOVELTY") and rare is not None:
                rb = arms(rare)[1]["arms"]["A1_rare"]["para_full_n"]
                print("  sub-read:", "'the wall is not the span' (A1-rare also < 30/72)" if rb < 30 else f"A1-rare {rb}/72 ≥ 30 → finding is about minted output rows; next = trained init or wider ridge, not closure")
            if label == "PARTIAL" and rare is not None:
                rb = arms(rare)[1]["arms"]["A1_rare"]["para_full_n"]; gN = runs.get("N")
                print(f"  ladder: A1 {a1n}, A1-rare {rb}, G {b}" + (f", N {arms(gN)[1]['arms']['A7_coined_coined']['para_full_binding_n']}" if gN else ""))
    if "M" in runs and "G" in runs:
        gM = arms(runs["M"])[1]["arms"]["A7_coined_coined"]; gG = arms(runs["G"])[1]["arms"]["A7_coined_coined"]
        print(f"\n(M) reading: M binding {gM['para_full_binding_n']} vs G {gG['para_full_binding_n']}; M sibling {gM.get('extra', {}).get('para_sibling')} vs G {gG.get('extra', {}).get('para_sibling')} → "
              + ("P-iv relevance 'not shown' (M ≥ G)" if gM["para_full_binding_n"] >= gG["para_full_binding_n"] else "consistent with P-iv only if M also has higher sibling + cannibal"))


if __name__ == "__main__":
    main()
