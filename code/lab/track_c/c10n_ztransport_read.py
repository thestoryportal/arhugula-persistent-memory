#!/usr/bin/env python3
"""D-C10n-ztransport mechanical reader (experiments/c10n/design/C10N_ZTRANSPORT_PREREG.md §3). No model judgement; fails closed.
Usage: c10n_ztransport_read.py experiments/c10n/runs/c10n_ztransport/run.json
[LAW:one-source-of-truth] every threshold lives here once, as §3 states it."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR
from c10m_diag_read import FINGERPRINT, ENV_PARA, ENV_CANON, INJ_PRE_PARA_MIN, INJ_PRE_CANON_MIN

REPL_B_DROP, REPL_C_DROP = 20, 10        # evidence/CORPUS/46 replication clause: B <= A - 20, C >= A - 10 ...
A_MIN, HIGH = 38, 44                     # N1: A < 38 INVALID; HIGH-CONTROL needs A >= 44 and C >= 44, else LOW-CONTROL (reported, not promoted)
DRIFT_D_DROP = 20                        # DRIFT: D <= A - 20 (behaviour-primary; geometry descriptive)
TP_D_DROP = 10                           # TARGET-PORTABLE: D >= A - 10


def main():
    r = json.load(open(sys.argv[1]))
    if "invalid" in r:
        print("INVALID:", r["invalid"]); return
    cand = [k for k in r["recipes"]][0]; rec = r["recipes"][cand]
    a7, a1 = rec["arms"]["A7_coined_coined"], rec["arms"]["A1_single"]; ex = a7["extra"]
    A, B, C, Dc = r["cell_A_zpre_pre"], ex["cell_B_zpre_post"], ex["cell_C_zpost_post"], r["cell_D_zpost_pre"]; g = r["geometry"]
    reasons = []
    fp = r["P1"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp: reasons.append(f"fingerprint not {FINGERPRINT}/PASS")
    if not rec["law5_gate"]["ok"]: reasons.append("LAW#5 not inert")
    if a1["para_full_n"] < 68: reasons.append(f"A1 {a1['para_full_n']} < 68")
    if not ENV_PARA[0] <= a7["para_full_n"] <= ENV_PARA[1]: reasons.append(f"A7 para_full {a7['para_full_n']} outside {ENV_PARA}")
    if not ENV_CANON[0] <= a7["canon_full_n"] <= ENV_CANON[1]: reasons.append(f"A7 canon {a7['canon_full_n']} outside {ENV_CANON}")
    if A["para_n"] < A_MIN or A["canon_n"] < INJ_PRE_CANON_MIN: reasons.append(f"cell A outside the instrument range (para < {A_MIN} or canon < {INJ_PRE_CANON_MIN})")
    if not r["restoration_check"]["identical"]: reasons.append("restoration check failed")
    if a7["locality_axes"]["L3_top1_agree"] < L3_THR: reasons.append("L3 below threshold")
    ax = a7["locality_axes"]
    print(f"run: A1 {a1['para_full_n']}/72 | A7 edit-only canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72 | L1 {ax['L1_flipped_to_edited_value']}/12 described_as {a7['locality_described_as']} L3 {ax['L3_top1_agree']}/30 | LAW#5 {rec['law5_gate']} | restored {r['restoration_check']['identical']}")
    print(f"A z_pre->pre   canon {A['canon_n']}/24 para {A['para_n']}/72 {A['per_template']}")
    print(f"B z_pre->post  canon {B['canon_n']}/24 para {B['para_n']}/72 {B['per_template']}")
    print(f"C z_post->post canon {C['canon_n']}/24 para {C['para_n']}/72 {C['per_template']}")
    print(f"D z_post->pre  canon {Dc['canon_n']}/24 para {Dc['para_n']}/72 {Dc['per_template']}")
    print(f"geometry: mean cosine {g['mean_cosine']} [{g['min_cosine']}, {g['max_cosine']}], mean rel diff {g['mean_rel_diff']}")
    print("\nsubject       A  B  C  D   cos    rel_diff  norm_pre  norm_post")
    for ra, rb, rc, rd, gg in zip(A["rows"], B["rows"], C["rows"], Dc["rows"], g["rows"]):
        assert ra["subj"] == rb["subj"] == rc["subj"] == rd["subj"] == gg["subj"], "rows misaligned"
        print(f"{ra['subj']:12} {sum(ra['per_template'][1:])}  {sum(rb['per_template'][1:])}  {sum(rc['per_template'][1:])}  {sum(rd['per_template'][1:])}   {gg['cosine']:.3f}  {gg['rel_diff']:.3f}     {gg['norm_pre']:.1f}     {gg['norm_post']:.1f}")
    if reasons:
        print("\nINVALID —", "; ".join(reasons)); return
    a, b, c, d = A["para_n"], B["para_n"], C["para_n"], Dc["para_n"]
    cells_ok = b <= a - REPL_B_DROP and c >= a - REPL_C_DROP
    stratum = "HIGH-CONTROL" if (a >= HIGH and c >= HIGH) else "LOW-CONTROL"
    promoted = cells_ok and stratum == "HIGH-CONTROL"
    print(f"\nCORPUS/46 replication: B {b} <= A-{REPL_B_DROP} ({a - REPL_B_DROP})? {b <= a - REPL_B_DROP}; C {c} >= A-{REPL_C_DROP} ({a - REPL_C_DROP})? {c >= a - REPL_C_DROP}; stratum {stratum} (A {a}, C {c}; HIGH needs both >= {HIGH}; control history 49/54/51/42) -> "
          f"{'reproduced, promotable' if promoted else ('cells reproduced, LOW-CONTROL: reported, not promoted as replication' if cells_ok else 'cells NOT reproduced in this process (reading not promoted)')}")
    if d <= a - DRIFT_D_DROP: label = "DRIFT"
    elif d >= a - TP_D_DROP: label = "TARGET-PORTABLE"
    else: label = "INDETERMINATE"
    print(f"reading: D {d} vs A {a} (DRIFT needs D <= {a - DRIFT_D_DROP}; TARGET-PORTABLE needs D >= {a - TP_D_DROP}) -> {label} [{stratum}{'' if promoted else ', not promoted'}]; geometry beside: mean cosine {g['mean_cosine']}, mean normalized displacement {g['mean_rel_diff']}")


if __name__ == "__main__":
    main()
