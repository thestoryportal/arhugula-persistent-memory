#!/usr/bin/env python3
"""D-C10q-stacked mechanical reader (docs/C10Q_STACKED_SOLVE_PREREG.md §3). No model judgement; exits non-zero on INVALID.
Usage: c10q_stacked_read.py results/c10q_stacked
[LAW:one-source-of-truth] every threshold lives here once, as §3 states it."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR
from c10m_diag_read import FINGERPRINT, ENV_PARA, ENV_CANON

REF_SPREAD = 5                          # the two passes' single-edit references within ± 5/72
SHAM_PARA, SHAM_DW = 5, 0.25            # sham scope: stacked-sham within ± 5 of its reference and ΔW2 <= 0.25 x ΔW1
LEAD, GAIN, CTRL, L1_SLACK, FRAME_SLACK, DESC_SLACK, PPL_SLACK = 30, 10, 68, 1, 1, 3, 0.5
DW2_CAP = 0.75                          # pass S: ΔW2 / ΔW1 above this -> -LARGE-WRITE (the second edit rivals the first); total ratio reported only
PERM_FRAC = 0.5                         # S-perm gain >= 0.5 x S gain (with S gain >= 10) -> -NOT-TARGET-SPECIFIC
MIN_ROT, SPLIT = 12, 0.30


def arm(res, name):
    cand = [k for k in res["recipes"]][0]; return res["recipes"][cand]["arms"][name], res["recipes"][cand]


def main():
    d = sys.argv[1]; head = json.load(open(os.path.join(d, "run.json")))
    P = {n: json.load(open(os.path.join(d, f"pass{n}.json"))) for n in ("S", "Ssham", "Sperm")}
    a7 = {n: arm(P[n], "A7_coined_coined")[0] for n in P}; rec = {n: arm(P[n], "A7_coined_coined")[1] for n in P}
    a1 = {n: arm(P[n], "A1_single")[0] for n in P}; a2 = {n: arm(P[n], "A2_coherent2")[0] for n in P}
    stk = {n: a7[n]["extra"]["stacked"] for n in P}
    dw1 = {n: sum(v["delta_norm"] for v in rec[n]["delta_norms"]["A7_coined_coined"].values()) for n in P}
    dw2 = {n: sum(v["delta_norm"] for v in a7[n]["extra"]["stacked_delta_norms"].values()) for n in P}
    frame1 = {n: a7[n]["extra"]["same_frame_fictional_single"]["flips"] for n in P}; frame2 = {n: a7[n]["extra"]["same_frame_fictional_stacked"]["flips"] for n in P}
    g = head["geometry"]; rot = sum(1 for x in g["rows"] if x["rel_diff"] > SPLIT)
    reasons = []
    fp = head["P1"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp: reasons.append("fingerprint")
    for n in P:
        if not rec[n]["law5_gate"]["ok"]: reasons.append(f"LAW#5 not inert in pass {n}")
        if a1[n]["para_full_n"] < CTRL or a2[n]["para_full_n"] < CTRL: reasons.append(f"pass {n} single-edit controls A1 {a1[n]['para_full_n']} A2 {a2[n]['para_full_n']} < {CTRL}")
        if not ENV_PARA[0] <= a7[n]["para_full_n"] <= ENV_PARA[1]: reasons.append(f"pass {n} reference A7 para {a7[n]['para_full_n']} outside {ENV_PARA}")
        if not ENV_CANON[0] <= a7[n]["canon_full_n"] <= ENV_CANON[1]: reasons.append(f"pass {n} reference A7 canon {a7[n]['canon_full_n']} outside {ENV_CANON}")
        if a7[n]["extra"]["override_hits_before_second_edit"] != 0 or a7[n]["extra"]["override_hits_after_second_edit"] != 1 or P[n]["z_override_hits_total"] != 1:
            reasons.append(f"pass {n} override hits not 0 -> 1 -> 1")
    refs = [a7[n]["para_full_n"] for n in P]
    if max(refs) - min(refs) > REF_SPREAD: reasons.append(f"single-edit references spread {max(refs) - min(refs)} > {REF_SPREAD}")
    if rot < MIN_ROT: reasons.append(f"rotated population {rot} < {MIN_ROT}")
    print(f"{'pass / stage':34} canon/24 para/72 first string | A1 A2 | L1/12 frame/6 described_as L3/30 ppl | ΔW total | hits")
    for n, lab in (("S", "S stacked (aim z_post)"), ("Ssham", "S-sham stacked (aim z_pre again)"), ("Sperm", "S-perm stacked (aim permuted z_post)")):
        x = a7[n]; ax = x["locality_axes"]
        print(f"{lab + ' / single ref':34} {x['canon_full_n']:>3}     {x['para_full_n']:>3}    {x['para_first_n']:>3}   {x['para_string_n']:>3}   | {a1[n]['para_full_n']:>2} {a2[n]['para_full_n']:>2} | {ax['L1_flipped_to_edited_value']:>2}    {frame1[n]:>2}     {x['locality_described_as']:>5}     {ax['L3_top1_agree']:>2}  {ax['generic_ppl_post']:.2f} | {dw1[n]:.1f} | {a7[n]['extra']['override_hits_before_second_edit']}")
        y = stk[n]; ay = y["locality_axes"]
        print(f"{lab + ' / stacked':34} {y['canon_full_n']:>3}     {y['para_full_n']:>3}    {y['para_first_n']:>3}   {y['para_string_n']:>3}   | -- -- | {ay['L1_flipped_to_edited_value']:>2}    {frame2[n]:>2}     {y['locality_described_as']:>5}     {ay['L3_top1_agree']:>2}  {ay['generic_ppl_post']:.2f} | +{dw2[n]:.1f} (x{(dw1[n] + dw2[n]) / dw1[n]:.2f}) | {a7[n]['extra']['override_hits_after_second_edit']}")
    print(f"geometry: mean cosine {g['mean_cosine']}, mean displacement {g['mean_rel_diff']}, rotated {rot}/24; same-frame fictional pre-edit {head['same_frame_fictional_pre_edit']['flips']}/6")
    if reasons:
        print("\nINVALID —", "; ".join(reasons)); sys.exit(2)
    sham_ok = abs(stk["Ssham"]["para_full_n"] - a7["Ssham"]["para_full_n"]) <= SHAM_PARA and dw2["Ssham"] <= SHAM_DW * dw1["Ssham"]
    x1, y = a7["S"], stk["S"]; ax1, ay = x1["locality_axes"], y["locality_axes"]
    gates = {"A1": a1["S"]["para_full_n"] >= CTRL, "A2": a2["S"]["para_full_n"] >= CTRL,   # NOTE: controls after the second edit are not re-measured by the harness; the single-edit controls stand in (reported as such)
             "L1": ay["L1_flipped_to_edited_value"] <= ax1["L1_flipped_to_edited_value"] + L1_SLACK, "same_frame_fictional": frame2["S"] <= frame1["S"] + FRAME_SLACK,
             "described_as": y["locality_described_as"] >= x1["locality_described_as"] - DESC_SLACK, "L3": ay["L3_top1_agree"] >= L3_THR, "ppl": ay["generic_ppl_post"] <= ax1["generic_ppl_post"] + PPL_SLACK}
    loc = all(gates.values()); gain = y["para_full_n"] - x1["para_full_n"]; ratio2 = dw2["S"] / dw1["S"]; total = (dw1["S"] + dw2["S"]) / dw1["S"]
    gain_perm = stk["Sperm"]["para_full_n"] - a7["Sperm"]["para_full_n"]
    if y["para_full_n"] >= LEAD and loc: label = "LEAD"
    elif gain >= GAIN and loc: label = "PARTIAL"
    elif gain >= GAIN: label = "TRADEOFF"
    else: label = "NULL"
    if label in ("LEAD", "PARTIAL") and ratio2 > DW2_CAP: label += "-LARGE-WRITE"
    if not sham_ok: label += "-SHAM-ACTIVE"
    if gain >= GAIN and gain_perm >= PERM_FRAC * gain: label += "-NOT-TARGET-SPECIFIC"
    print(f"\nsham control: stacked-sham para {stk['Ssham']['para_full_n']} vs its reference {a7['Ssham']['para_full_n']} (|Δ| <= {SHAM_PARA}? {abs(stk['Ssham']['para_full_n'] - a7['Ssham']['para_full_n']) <= SHAM_PARA}); ΔW2/ΔW1 {dw2['Ssham'] / dw1['Ssham']:.3f} (<= {SHAM_DW}? {dw2['Ssham'] <= SHAM_DW * dw1['Ssham']}) -> {'sham inert' if sham_ok else 'SHAM ACTIVE'}")
    print(f"matched-energy control: S-perm stacked {stk['Sperm']['para_full_n']} vs its reference {a7['Sperm']['para_full_n']} (gain {gain_perm}; ΔW2/ΔW1 {dw2['Sperm'] / dw1['Sperm']:.3f}) vs S gain {gain}")
    print(f"locality gates (stacked vs its single-edit reference, pass S): {gates}\nbinding: stacked para_full {y['para_full_n']}/72 vs reference {x1['para_full_n']} (gain {gain}); LEAD ≥ {LEAD}; ΔW2/ΔW1 {ratio2:.2f} (cap {DW2_CAP}; total x{total:.2f}); string {y['para_string_n']} -> {label}")


if __name__ == "__main__":
    main()
