#!/usr/bin/env python3
"""D-C10o-magnitude mechanical reader (docs/C10O_MAGNITUDE_DIRECTION_PREREG.md §3 v2). No model judgement; fails closed.
Usage: c10o_magnitude_read.py results/c10o_magnitude/run.json
[LAW:one-source-of-truth] every threshold lives here once, as §3 states it. Labels are next-arm routing labels."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR
from c10m_diag_read import FINGERPRINT, ENV_PARA, ENV_CANON, INJ_PRE_CANON_MIN

A_MIN, HIGH = 38, 44
SPLIT, BUF = 0.30, (0.25, 0.35)   # rotated population: displacement > 0.30; buffer zone -> sensitivity read
MIN_POP, MIN_CONTRAST = 12, 20
F_HIGH, F_LOW = 0.6, 0.3


def para(cell, idx): return sum(sum(cell["rows"][i]["per_template"][1:]) for i in idx)
def canon(cell, idx): return sum(cell["rows"][i]["per_template"][0] for i in idx)
def clip(x): return min(max(x, 0.0), 1.0)


def label(B, C, E1, E2, E3, idx):
    b, c = para(B, idx), para(C, idx)
    if c - b < MIN_CONTRAST:
        return None, (b, c, None, None, None), f"CONTRAST-TOO-SMALL (C - B = {c - b} < {MIN_CONTRAST})"
    f = [(para(E, idx) - b) / (c - b) for E in (E1, E2, E3)]
    c1, c2, c3 = (clip(x) for x in f)
    if c1 >= F_HIGH and max(c2, c3) < F_LOW: lab = "MAGNITUDE"
    elif c2 >= F_HIGH and c1 < F_LOW: lab = "DIRECTION"
    elif c3 >= F_HIGH and c2 < F_LOW and c1 < F_LOW: lab = "ROTATION-WITH-PROJECTION"
    elif c1 >= F_HIGH and max(c2, c3) >= F_HIGH: lab = "EITHER"
    elif max(c1, c2, c3) < F_LOW: lab = "NEITHER-ALONE"
    else: lab = "MIXED"
    return lab, (b, c, *f), f"B {b} C {c} E1 {para(E1, idx)} E2 {para(E2, idx)} E3 {para(E3, idx)} (/{3*len(idx)}); f1 {f[0]:.3f} f2 {f[1]:.3f} f3 {f[2]:.3f}"


def main():
    r = json.load(open(sys.argv[1]))
    if "invalid" in r:
        print("INVALID:", r["invalid"]); return
    cand = [k for k in r["recipes"]][0]; rec = r["recipes"][cand]
    a7, a1 = rec["arms"]["A7_coined_coined"], rec["arms"]["A1_single"]; ex = a7["extra"]
    A = r["cell_A_zpre_pre"]; B, C, E1, E2, E3 = ex["cell_B_zpre"], ex["cell_C_zpost"], ex["cell_E1_magnitude"], ex["cell_E2_direction"], ex["cell_E3_projection"]
    P = {"E1'": r["cell_E1prime_magnitude_pre"], "E2'": r["cell_E2prime_direction_pre"], "E3'": r["cell_E3prime_projection_pre"]}; g = ex["geometry"]
    for cell in (A, B, C, E1, E2, E3, *P.values()):
        assert [x["subj"] for x in cell["rows"]] == [x["subj"] for x in g["rows"]], "rows misaligned"   # [LAW:no-silent-failure]
    rot = [i for i, x in enumerate(g["rows"]) if x["rel_diff"] > SPLIT]; same = [i for i in range(24) if i not in rot]
    buf = [i for i, x in enumerate(g["rows"]) if BUF[0] <= x["rel_diff"] <= BUF[1]]
    reasons = []
    fp = r["P1"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp: reasons.append("fingerprint")
    if not rec["law5_gate"]["ok"]: reasons.append("LAW#5 not inert")
    if a1["para_full_n"] < 68: reasons.append(f"A1 {a1['para_full_n']} < 68")
    if not ENV_PARA[0] <= a7["para_full_n"] <= ENV_PARA[1]: reasons.append(f"A7 para_full {a7['para_full_n']} outside {ENV_PARA}")
    if not ENV_CANON[0] <= a7["canon_full_n"] <= ENV_CANON[1]: reasons.append(f"A7 canon {a7['canon_full_n']} outside {ENV_CANON}")
    if A["para_n"] < A_MIN or A["canon_n"] < INJ_PRE_CANON_MIN: reasons.append("cell A outside instrument range")
    if not r["restoration_check"]["identical"]: reasons.append("restoration check failed")
    if a7["locality_axes"]["L3_top1_agree"] < L3_THR: reasons.append("L3 below threshold")
    if len(rot) < MIN_POP: reasons.append(f"rotated population {len(rot)} < {MIN_POP}")
    ax = a7["locality_axes"]; stratum = "HIGH-CONTROL" if A["para_n"] >= HIGH else "LOW-CONTROL"
    print(f"run: A1 {a1['para_full_n']}/72 | A7 edit-only canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72 | L1 {ax['L1_flipped_to_edited_value']}/12 described_as {a7['locality_described_as']} L3 {ax['L3_top1_agree']}/30 | LAW#5 {rec['law5_gate']} | restored {r['restoration_check']['identical']}")
    print(f"cell A control: canon {A['canon_n']}/24 para {A['para_n']}/72 -> {stratum}; rotated population {len(rot)} (displacement > {SPLIT}), identical {len(same)}, buffer-zone {len(buf)} {[g['rows'][i]['subj'] for i in buf]}")
    n = 3 * len(rot)
    print(f"\n{'cell':30} rotated para /{n}  canon /{len(rot)}  | identical para /{3*len(same)} | all /72")
    for name, cell in (("B z_pre -> edited", B), ("C z_post -> edited", C), ("E1 magnitude -> edited", E1), ("E2 direction -> edited", E2), ("E3 projection -> edited", E3),
                       ("E1' magnitude -> unedited", P["E1'"]), ("E2' direction -> unedited", P["E2'"]), ("E3' projection -> unedited", P["E3'"]), ("A z_pre -> unedited", A)):
        print(f"{name:30} {para(cell, rot):>6}        {canon(cell, rot):>4}       | {para(cell, same):>5}          | {cell['para_n']:>3}")
    print("\nsubject       disp   ratio  proj   B  C  E1 E2 E3 | E1' E2' E3'")
    for i, x in enumerate(g["rows"]):
        s = x["subj"]; row = [sum(cell["rows"][i]["per_template"][1:]) for cell in (B, C, E1, E2, E3, P["E1'"], P["E2'"], P["E3'"])]
        print(f"{s:12} {x['rel_diff']:.3f}  {ex['norm_ratio'][s]:.3f}  {ex['projection_fraction'][s]:.3f}  {row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]} |  {row[5]}   {row[6]}   {row[7]}{'   (identical-target)' if i in same else ('   (buffer)' if i in buf else '')}")
    if reasons:
        print("\nINVALID —", "; ".join(reasons)); return
    lab, _, text = label(B, C, E1, E2, E3, rot)
    print(f"\nrotated population: {text} -> {lab or 'no label'} [{stratum}] (routing label, not mechanism evidence)")
    if buf:
        lab2, _, text2 = label(B, C, E1, E2, E3, [i for i in rot if i not in buf])
        print(f"sensitivity (buffer-zone subjects excluded): {text2} -> {lab2 or 'no label'}{'' if lab2 == lab else '  ** differs from the primary read: the split is not clean **'}")


if __name__ == "__main__":
    main()
