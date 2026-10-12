#!/usr/bin/env python3
"""D-C10p-twopass mechanical reader (docs/C10P_TWOPASS_SOLVE_PREREG.md §3). No model judgement; fails closed.
Usage: c10p_twopass_read.py results/c10p_twopass
[LAW:one-source-of-truth] every threshold lives here once, as §3 states it."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR
from c10m_diag_read import FINGERPRINT, ENV_PARA, ENV_CANON

SHAM_PARA, SHAM_CANON, SHAM_DW = 5, 3, 0.05
LEAD, GAIN, CTRL, L1_SLACK, DESC_SLACK, PPL_SLACK, FRAME_SLACK = 30, 10, 68, 1, 3, 0.5, 1
MIN_ROT, SPLIT = 12, 0.30
DW_RATIO_CAP = 1.5          # total ΔW (pass 3 / pass 1) above this -> the label carries the LARGE-WRITE qualifier
EXPECTED_HITS = {1: 0, 2: 1, 3: 1}   # Z_OVERRIDE must feed exactly the A7 edit in passes 2 and 3 and nothing in pass 1


def arm(res, name):
    cand = [k for k in res["recipes"]][0]; return res["recipes"][cand]["arms"][name], res["recipes"][cand]


def main():
    d = sys.argv[1]; head = json.load(open(os.path.join(d, "run.json")))
    P = {n: json.load(open(os.path.join(d, f"pass{n}.json"))) for n in (1, 2, 3)}
    a7 = {n: arm(P[n], "A7_coined_coined")[0] for n in P}; a1 = {n: arm(P[n], "A1_single")[0] for n in P}; a2 = {n: arm(P[n], "A2_coherent2")[0] for n in P}
    rec = {n: arm(P[n], "A7_coined_coined")[1] for n in P}
    g = head["geometry"]; rot = sum(1 for x in g["rows"] if x["rel_diff"] > SPLIT)
    reasons = []
    fp = head["P1"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp: reasons.append("fingerprint")
    for n in P:
        if not rec[n]["law5_gate"]["ok"]: reasons.append(f"LAW#5 not inert in pass {n}")
    if a1[1]["para_full_n"] < CTRL or a2[1]["para_full_n"] < CTRL: reasons.append(f"pass 1 controls A1 {a1[1]['para_full_n']} A2 {a2[1]['para_full_n']} < {CTRL}")
    if not ENV_PARA[0] <= a7[1]["para_full_n"] <= ENV_PARA[1]: reasons.append(f"pass 1 A7 para {a7[1]['para_full_n']} outside {ENV_PARA}")
    if not ENV_CANON[0] <= a7[1]["canon_full_n"] <= ENV_CANON[1]: reasons.append(f"pass 1 A7 canon {a7[1]['canon_full_n']} outside {ENV_CANON}")
    dw = {n: rec[n]["delta_norms"]["A7_coined_coined"] for n in P}
    dw_dev = max(abs(dw[2][l]["delta_norm"] - dw[1][l]["delta_norm"]) / dw[1][l]["delta_norm"] for l in dw[1])
    sham_ok = abs(a7[2]["para_full_n"] - a7[1]["para_full_n"]) <= SHAM_PARA and abs(a7[2]["canon_full_n"] - a7[1]["canon_full_n"]) <= SHAM_CANON and dw_dev <= SHAM_DW
    if not sham_ok: reasons.append(f"sham not inert: para {a7[2]['para_full_n']} vs {a7[1]['para_full_n']}, canon {a7[2]['canon_full_n']} vs {a7[1]['canon_full_n']}, max ΔW deviation {dw_dev:.3f}")
    if rot < MIN_ROT: reasons.append(f"rotated population {rot} < {MIN_ROT}")
    for n in P:
        if P[n]["z_override_hits_total"] != EXPECTED_HITS[n]: reasons.append(f"pass {n} override hits {P[n]['z_override_hits_total']} != {EXPECTED_HITS[n]}")
    frame = {n: a7[n]["extra"]["same_frame_fictional"]["flips"] for n in P}; frame_pre = head["same_frame_fictional_pre_edit"]["flips"]
    tot = {n: sum(dw[n][l]["delta_norm"] for l in dw[n]) for n in P}; dw_ratio = tot[3] / tot[1]
    print(f"{'pass':26} canon/24 para/72 first string | A1 A2 | L1/12 frame/6 described_as L3/30 ppl_post | ΔW norms (L4..L8) total | hits")
    for n, lab in ((1, "1 baseline"), (2, "2 sham (aim z_pre)"), (3, "3 two-pass (aim z_post)")):
        x = a7[n]; ax = x["locality_axes"]
        print(f"{lab:26} {x['canon_full_n']:>3}     {x['para_full_n']:>3}    {x['para_first_n']:>3}   {x['para_string_n']:>3}   | {a1[n]['para_full_n']:>2} {a2[n]['para_full_n']:>2} | {ax['L1_flipped_to_edited_value']:>2}    {frame[n]:>2}     {x['locality_described_as']:>5}     {ax['L3_top1_agree']:>2}   {ax['generic_ppl_post']:.2f}  | {[round(dw[n][l]['delta_norm'], 1) for l in dw[n]]} {tot[n]:.1f} | {P[n]['z_override_hits_total']}")
    print(f"geometry: mean cosine {g['mean_cosine']}, mean displacement {g['mean_rel_diff']}, rotated {rot}/24; sham max ΔW deviation {dw_dev:.3f}; same-frame fictional flips pre-edit {frame_pre}/6; ΔW ratio pass3/pass1 {dw_ratio:.3f} (per layer {[round(dw[3][l]['delta_norm'] / dw[1][l]['delta_norm'], 2) for l in dw[1]]})")
    if reasons:
        print("\nINVALID —", "; ".join(reasons)); sys.exit(2)   # [LAW:no-silent-failure] automation must not read INVALID as success
    x1, x3 = a7[1], a7[3]; ax1, ax3 = x1["locality_axes"], x3["locality_axes"]
    gates = {"A1": a1[3]["para_full_n"] >= CTRL, "A2": a2[3]["para_full_n"] >= CTRL,
             "L1": ax3["L1_flipped_to_edited_value"] <= ax1["L1_flipped_to_edited_value"] + L1_SLACK,
             "described_as": x3["locality_described_as"] >= x1["locality_described_as"] - DESC_SLACK,
             "L3": ax3["L3_top1_agree"] >= L3_THR, "ppl": ax3["generic_ppl_post"] <= ax1["generic_ppl_post"] + PPL_SLACK,
             "same_frame_fictional": frame[3] <= frame[1] + FRAME_SLACK}
    loc = all(gates.values()); gain = x3["para_full_n"] - x1["para_full_n"]
    if x3["para_full_n"] >= LEAD and loc: label = "LEAD"
    elif gain >= GAIN and loc: label = "PARTIAL"
    elif gain >= GAIN: label = "TRADEOFF"
    else: label = "NULL"
    if label in ("LEAD", "PARTIAL") and dw_ratio > DW_RATIO_CAP: label += "-LARGE-WRITE"
    strdiff = abs(x3["para_string_n"] - x3["para_full_n"])
    print(f"\nlocality gates (pass 3 vs pass 1): {gates}\nbinding: pass 3 para_full {x3['para_full_n']}/72 vs pass 1 {x1['para_full_n']} (gain {gain}); LEAD ≥ {LEAD}; ΔW ratio {dw_ratio:.2f} (cap {DW_RATIO_CAP}); string readout {x3['para_string_n']}{' (differs from id count by ' + str(strdiff) + ')' if strdiff > 2 else ''} -> {label}")


if __name__ == "__main__":
    main()
