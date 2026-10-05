#!/usr/bin/env python3
"""D-C10m-diag mechanical reader (docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md v2 §3). No model judgement.
Usage: c10m_diag_read.py results/c10m_diag/diag_run.json [results/c10l_mint]   (the mint dir supplies Q3's four fixed files)
[LAW:one-source-of-truth] every threshold lives here once, as §3 states it. Fails closed on any missing field or file.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR

FINGERPRINT = "d941a9fb"
Q3_FILES = {"seed0": "arm_N.json", "seed0_fourth_replicate": "arm_N_p4.json", "seed1": "arm_N_seed1.json", "seed2": "arm_N_seed2.json"}
Q3_RANGE_OVER = ("seed0", "seed1", "seed2")   # prereg §3 Q3: R over the three distinct seeds, seed 0 = the CORPUS/45 row (46); the fourth replicate is listed, not ranged
ENV_PARA, ENV_CANON = (5, 18), (5, 10)      # identical-baseline envelope, CORPUS/44
INJ_PRE_PARA_MIN, INJ_PRE_CANON_MIN = 44, 22
DRIFT_GAIN, LEAD, CHAIN_GAIN, TF_HIGH, N_CHAIN, N_MAJ = 15, 30, 5, 0.75, 8, 13
H2_CANON, H2_PARA_DROP, H1_CANON, H1_PARA_OVER = 20, 10, 12, 10
SEED_RANGE = 10


def main():
    r = json.load(open(sys.argv[1]))
    if "invalid" in r:
        print("INVALID:", r["invalid"]); return
    cand = [k for k in r["recipes"]][0]; rec = r["recipes"][cand]
    a7, a1 = rec["arms"]["A7_coined_coined"], rec["arms"]["A1_single"]
    ex = a7["extra"]; pre = r["inj_pre"]; post = ex["inj_post_zpre"]; con = ex["constrained"]
    rows = rec["detail"]["A7_coined_coined"]
    F, C, E = a7["para_full_n"], con["para_n"], a7["para_full_n"]
    reasons = []
    fp = r["P1"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp: reasons.append(f"fingerprint not {FINGERPRINT}/PASS: {fp!r}")
    if len(rows) != 24 or len(con["rows"]) != 24 or any(a["subj"] != b["subj"] for a, b in zip(rows, con["rows"])):
        raise SystemExit("Q1 rows misaligned: harness detail vs constrained rows")   # [LAW:no-silent-failure]
    if not rec["law5_gate"]["ok"]: reasons.append("LAW#5 not inert")
    if a1["para_full_n"] < 68: reasons.append(f"A1 {a1['para_full_n']} < 68")
    if not ENV_PARA[0] <= F <= ENV_PARA[1]: reasons.append(f"A7 para_full {F} outside {ENV_PARA}")
    if not ENV_CANON[0] <= a7["canon_full_n"] <= ENV_CANON[1]: reasons.append(f"A7 canon {a7['canon_full_n']} outside {ENV_CANON}")
    if pre["para_n"] < INJ_PRE_PARA_MIN or pre["canon_n"] < INJ_PRE_CANON_MIN: reasons.append(f"injection control {pre['canon_n']}/24, {pre['para_n']}/72 below gate")
    if a7["locality_axes"]["L3_top1_agree"] < L3_THR: reasons.append("L3 below threshold")
    ax = a7["locality_axes"]
    print(f"run D: A1 {a1['para_full_n']}/72 | A7 edit-only canon {a7['canon_full_n']}/24 para {F}/72 first {a7['para_first_n']} | L1 {ax['L1_flipped_to_edited_value']}/12 described_as {a7['locality_described_as']} L3 {ax['L3_top1_agree']}/30 | LAW#5 {rec['law5_gate']}")
    print(f"injection control (pre-edit, z_pre): canon {pre['canon_n']}/24 para {pre['para_n']}/72 {pre['per_template']}")
    print(f"constrained (gold first token): canon {con['canon_n']}/24 para {C}/72 string {con['para_string_n']}/72")
    print(f"edit+inject z_pre (BINDING): canon {post['canon_n']}/24 para {post['para_n']}/72 {post['per_template']}")
    s2 = ex["inj_post_zpost_secondary"]; print(f"edit+inject z_post (secondary): canon {s2['canon_n']}/24 para {s2['para_n']}/72")
    print("\nsubject       ntok  F_s  C_s  T_s")
    chain_subj = 0
    for row, crow in zip(rows, con["rows"]):
        Fs, Cs = sum(row["para_full_hits"]), sum(crow["para_constrained"]); Ts = row["tf_correct"] / row["tf_total"] if row["tf_total"] else 0.0
        chain_subj += (Ts >= TF_HIGH and Cs <= 1)
        print(f"{row['subj']:12} {row['ntok']:>4} {Fs:>4} {Cs:>4}  {Ts:.2f}")
    if reasons:
        print("\nQ1/Q2: INVALID —", "; ".join(reasons)); return
    gain = C - F
    if gain >= DRIFT_GAIN: q1 = "DRIFT-LEAD" if C >= LEAD else "DRIFT-PARTIAL"
    elif gain <= CHAIN_GAIN and chain_subj >= N_CHAIN: q1 = "CHAIN-DOMINANT" if chain_subj >= N_MAJ else "CHAIN-PRESENT"
    elif gain <= CHAIN_GAIN: q1 = "ABSENT-DOMINANT"
    else: q1 = "MIXED"
    print(f"\nQ1 read partition: C - F = {C} - {F} = {gain}; high-TF constrained-failing subjects {chain_subj}/24 -> {q1}")
    Kp, Pp, Ppre = post["canon_n"], post["para_n"], pre["para_n"]
    if Kp >= H2_CANON and Pp >= Ppre - H2_PARA_DROP: q2 = "H2 (read-differently)"
    elif Kp <= H1_CANON or Pp <= E + H1_PARA_OVER: q2 = "H1 (collateral)"
    else: q2 = "INDETERMINATE"
    print(f"Q2 edit+inject: K_post {Kp}/24, P_post {Pp}/72 vs P_pre {Ppre}, E {E} -> {q2}")
    if len(sys.argv) > 2:
        seeds = {}
        for role, f in Q3_FILES.items():
            a = json.load(open(os.path.join(sys.argv[2], f))); c = [k for k in a["recipes"]][0]   # a missing file raises
            seeds[role] = a["recipes"][c]["arms"]["A7_coined_coined"]["para_full_binding_n"]
        vals = [seeds[k] for k in Q3_RANGE_OVER]; R = max(vals) - min(vals)
        print(f"Q3 N seeds {seeds} (range over {Q3_RANGE_OVER}): range {R} -> {'SEED-SENSITIVE' if R >= SEED_RANGE else 'SPREAD'}")


if __name__ == "__main__":
    main()
