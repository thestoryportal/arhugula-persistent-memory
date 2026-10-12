#!/usr/bin/env python3
"""D-C10l-mint amendment B3 mechanical readout (experiments/c10l/design/C10L_MINT_TOKEN_PREREG.md §10 B3; rules frozen before the runs).
No model judgement. Reads the original and replicate arm JSONs and prints:
  - one row per arm with the binding count and the S-3 axes (L1, described_as, L3) beside it;
  - rule 1 (G-vs-N ordering): SUPPORTED only if N - G >= 5/72 in BOTH replicates
        replicate 1 = (G, N)            original run pair, seed-0 N
        replicate 2 = (G_rep, N_seed1)  fresh-process G, seed-1 N        (N_p4 = seed-0 N fourth replicate, reported, not a pair)
  - rule 2 (minted-vs-rare): SUPPORTED only if min(all mint replicates) - max(all rare replicates) >= 10/72.
Usage: c10l_mint_b3_read.py <experiments/c10l/runs/c10l_mint dir> [p4_verdict.json]
[LAW:one-source-of-truth] the thresholds live here once, as the prereg states them; evidence/CORPUS/45's addendum cites this output.
[LAW:effects-at-boundaries] pure read of JSON -> printed table; nothing written.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import arms, row, L3_THR   # the §6 helpers; same gates, same field names

RULE_GN = 5      # N - G >= 5/72 in both replicates
RULE_MR = 10     # min(mint) - max(rare) >= 10/72
MINT = {"G": "arm_G.json", "N": "arm_N.json", "N_p4": "arm_N_p4.json", "G_rep": "arm_G_rep.json", "N_seed1": "arm_N_seed1.json"}
RARE = {"rare": "arm_rare.json", "rare_rep": "arm_rare_rep.json"}


def load(d, name):
    return json.load(open(os.path.join(d, name)))   # a missing replicate raises; nothing is skipped


def mint_row(run):
    _, c = arms(run); a7 = c["arms"]["A7_coined_coined"]; a1 = c["arms"]["A1_single"]
    r = row(a7, a7["para_full_binding_n"]); r["A1_same_run"] = a1["para_full_n"]
    ex = a7.get("extra", {})
    r["valid"] = a1["para_full_n"] >= 58 and a7["locality_axes"]["L3_top1_agree"] >= L3_THR and ex.get("post_write_cannibal", 99) <= 2 and ex.get("para_sibling", 99) <= 3
    # arm_G.json / arm_N.json were written before the driver recorded step0_path (B3); they ran on the original step 0 by construction
    r["step0"] = os.path.basename(run.get("step0_path", "step0_probe.json")); r["init_tag"] = run.get("init_tag", "")
    return r


def rare_row(run):
    _, c = arms(run); r1 = c["arms"]["A1_rare"]; a1 = c["arms"]["A1_single"]
    r = row(r1); r["A1_same_run"] = a1["para_full_n"]
    r["valid"] = a1["para_full_n"] >= 58 and r1["locality_axes"]["L3_top1_agree"] >= L3_THR
    return r


def main():
    d = sys.argv[1]
    mint = {k: mint_row(load(d, f)) for k, f in MINT.items()}
    rare = {k: rare_row(load(d, f)) for k, f in RARE.items()}
    print("arm        binding/72  canon/24  string  sibling  cannibal  L1/12  described_as  L3/30  A1(same run)  valid  step0")
    for k, r in {**mint, **rare}.items():
        print(f"{k:10} {r['binding']:>6}      {r['canon']:>3}      {r['string']:>3}     {str(r['sibling']):>3}      {str(r['cannibal_post']):>3}     {r['L1']:>2}     {r['described_as']:>5}      {r['L3']:>2}      {r['A1_same_run']:>3}       {r['valid']}  {r.get('step0','')}")
    rep1 = mint["N"]["binding"] - mint["G"]["binding"]
    rep2 = mint["N_seed1"]["binding"] - mint["G_rep"]["binding"]
    rep2b = mint["N_p4"]["binding"] - mint["G_rep"]["binding"]
    gn = "SUPPORTED" if rep1 >= RULE_GN and rep2 >= RULE_GN else "UNSUPPORTED"
    print(f"\nRule 1 G-vs-N: replicate 1 N-G = {rep1} (seed-0 N {mint['N']['binding']} vs G {mint['G']['binding']}); "
          f"replicate 2 N-G = {rep2} (seed-1 N {mint['N_seed1']['binding']} vs G_rep {mint['G_rep']['binding']}); "
          f"[seed-0 N fourth replicate N_p4 {mint['N_p4']['binding']} vs G_rep: {rep2b}] -> threshold >= {RULE_GN} in both -> {gn}")
    mn = min(r["binding"] for r in mint.values()); mx = max(r["binding"] for r in rare.values())
    mr = "SUPPORTED" if mn - mx >= RULE_MR else "UNSUPPORTED"
    print(f"Rule 2 minted-vs-rare: min(mint) {mn} - max(rare) {mx} = {mn - mx} -> threshold >= {RULE_MR} -> {mr}")
    invalid = [k for k, r in {**mint, **rare}.items() if not r["valid"]]
    print(f"validity: {'all arms valid (A1 >= 58, L3 >= %d, sibling <= 3, cannibal <= 2)' % L3_THR if not invalid else 'INVALID arms: ' + ', '.join(invalid)}")
    if len(sys.argv) > 2:
        v = json.load(open(sys.argv[2]))
        print(f"\nP4 (B2): {v['reading']}\n  tokenisation {v['tokenisation']}  HF↔fp16 parity {v['hf_vs_gguf_f16_parity']}  HF↔Q4 parity {v['hf_vs_gguf_q4km_parity']}\n"
              f"  correct {v['correct']}  Q4 retention of fp16-correct {v['q4km_retention_of_f16_correct']}  L1 flips {v['L1_flipped_to_minted']}")


if __name__ == "__main__":
    main()
