#!/usr/bin/env python3
"""D-C10l-mint P4 verdict (amendment B2): paired fp16-GGUF vs Q4_K_M-GGUF retention on the CORPUS/17 metric
(of prompts correct in GGUF-fp16 = eligible, the fraction still correct in Q4_K_M = retention), plus the three pre-registered
gates: tokenisation 24/24 in both GGUFs; HF-fp16 ↔ GGUF-fp16 canonical id parity 24/24 (binding); everything else reported.
Usage: c10l_mint_p4_verdict.py p4_pred_f16.json p4_pred_q4km.json out.json
"""
import sys, json
f16, q4 = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
out = {"tokenisation": {"f16": f"{f16['tokenisation_single_minted']}/{f16['n_values']}", "q4km": f"{q4['tokenisation_single_minted']}/{q4['n_values']}"},
       "hf_vs_gguf_f16_parity": {g: f"{f16[f'{g}_parity']}/{f16[f'{g}_n']}" for g in ("canon", "para", "L1", "L3", "unrelated")},
       "hf_vs_gguf_q4km_parity": {g: f"{q4[f'{g}_parity']}/{q4[f'{g}_n']}" for g in ("canon", "para", "L1", "L3", "unrelated")},
       "correct": {"f16": {"canon": f16["canon_correct"], "para": f16["para_correct"]}, "q4km": {"canon": q4["canon_correct"], "para": q4["para_correct"]}},
       "signatures": {"f16": {g: f16[f"{g}_signatures"] for g in ("canon", "para")}, "q4km": {g: q4[f"{g}_signatures"] for g in ("canon", "para")}},
       "L1_flipped_to_minted": {"f16": f16["L1_flipped_to_minted"], "q4km": q4["L1_flipped_to_minted"]}}
ret = {}
for g in ("canon", "para"):
    elig = [i for i, r in enumerate(f16["rows"][g]) if r["correct"]]
    surv = sum(q4["rows"][g][i]["correct"] for i in elig)
    ret[g] = {"eligible": len(elig), "survived": surv, "retention": round(surv / len(elig), 3) if elig else None}
out["q4km_retention_of_f16_correct"] = ret
gates = {"tokenisation_24_24_both": f16["tokenisation_single_minted"] == f16["n_values"] == q4["tokenisation_single_minted"],
         "canon_id_parity_24_24_f16": f16["canon_parity"] == f16["canon_n"]}
out["gates"] = gates
out["reading"] = ("DEPLOYMENT PASS (compiled fp16 GGUF reproduces the HF edit on every canonical prompt and the minted ids tokenise as one token)"
                  if all(gates.values()) else "DEPLOYMENT FINDING: " + ", ".join(k for k, v in gates.items() if not v) + " failed — see signatures")
json.dump(out, open(sys.argv[3], "w"), indent=2)
print(json.dumps({k: v for k, v in out.items()}, indent=1))
