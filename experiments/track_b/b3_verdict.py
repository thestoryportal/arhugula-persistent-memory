import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""B3/G6.2 verdict: edited-fact quantization survival vs native-fact, through the SAME quantizer.
Inputs: b3_probes.json (HF-fp16 ref), b3_pred_f16.json (GGUF fp16), b3_pred_q4.json (GGUF Q4_K_M).
PASS = edited-fact retention >= native-country retention - 3 pts.
Retention = of facts CORRECT in GGUF-fp16 (eligible), fraction still correct in GGUF-Q4_K_M."""
import json
def correct(top1, truth):
    if truth is None: return None
    a=(top1 or "").strip().lower(); b=truth.lower()
    return bool(a) and (a==b or b.startswith(a) or a.startswith(b))

probes=json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
ref={p["prompt"]:p for p in probes["edited"]+probes["native"]}
f16={p["prompt"]:p for p in json.load(open(f"{LLMDB_ROOT}/results/b3_pred_f16.json"))}
q4 ={p["prompt"]:p for p in json.load(open(f"{LLMDB_ROOT}/results/b3_pred_q4.json"))}

# --- VALIDITY GATE: HF-fp16 vs GGUF-fp16 agreement, SPLIT edited vs native ---
# Everything downstream is measured on the GGUF; if conversion didn't reproduce the
# edited model (esp. the band[4-8] edit), the edited-vs-native delta is confounded.
def agreement(kinds):
    ag=tot=0
    for pr,r in ref.items():
        if r["kind"] not in kinds or pr not in f16: continue
        tot+=1
        a=(f16[pr]["top1"] or "").strip().lower(); b=(r["hf_top1"] or "").strip().lower()
        if a and b and (a==b or a.startswith(b) or b.startswith(a)): ag+=1
    return (round(100*ag/tot,1) if tot else None),ag,tot
ag_ed=agreement({"edited"}); ag_nat=agreement({"native_country","native_global"}); ag_all=agreement({"edited","native_country","native_global"})
print(f"VALIDITY: HF-fp16 vs GGUF-fp16 top-1 agreement — edited={ag_ed[0]}% ({ag_ed[1]}/{ag_ed[2]}) | native={ag_nat[0]}% ({ag_nat[1]}/{ag_nat[2]}) | all={ag_all[0]}%")
EDIT_AGREE_OK = ag_ed[0] is not None and ag_ed[0]>=95.0
if not EDIT_AGREE_OK:
    print(f"  ⚠️ EDITED-AGREEMENT {ag_ed[0]}% < 95% → GGUF conversion did NOT faithfully reproduce the edit; Q4 verdict is CONFOUNDED.")

def retention(kind):
    """eligible = correct (vs target) in GGUF-fp16; retention = still correct in Q4."""
    elig=[]; surv=0
    for pr,r in ref.items():
        if r["kind"]!=kind: continue
        tgt=r["target"]
        if tgt is None:  # global: eligibility = fp16 top1 self; survival = q4 matches fp16 top1
            ftop=(f16[pr]["top1"] or "").strip().lower()
            if not ftop: continue
            elig.append(pr)
            qtop=(q4[pr]["top1"] or "").strip().lower()
            if qtop and (qtop==ftop or qtop.startswith(ftop) or ftop.startswith(qtop)): surv+=1
        else:
            if correct(f16[pr]["top1"],tgt):
                elig.append(pr)
                if correct(q4[pr]["top1"],tgt): surv+=1
    n=len(elig); pct=round(100*surv/n,1) if n else None
    return pct,surv,n

ed=retention("edited"); nc=retention("native_country"); ng=retention("native_global")
print(f"\nEDITED-fact retention (Q4_K_M | eligible=fp16-correct): {ed[0]}%  ({ed[1]}/{ed[2]})")
print(f"NATIVE-country retention:                                {nc[0]}%  ({nc[1]}/{nc[2]})")
print(f"NATIVE-global retention (self-consistency):              {ng[0]}%  ({ng[1]}/{ng[2]})")

# also report raw fp16 correctness counts (sanity: A1 edited expression ~100%)
def f16_correct(kind):
    n=c=0
    for pr,r in ref.items():
        if r["kind"]!=kind or r["target"] is None: continue
        n+=1; c+= 1 if correct(f16[pr]["top1"],r["target"]) else 0
    return c,n
print(f"\n(fp16-GGUF correctness: edited {f16_correct('edited')} | native_country {f16_correct('native_country')})")

verdict=None; MIN_N=20
delta=(ed[0]-nc[0]) if (ed[0] is not None and nc[0] is not None) else None
if ed[2] < MIN_N or nc[2] < MIN_N:
    verdict="INCONCLUSIVE"
    print(f"\nG6.2 VERDICT: INCONCLUSIVE — eligible n below floor (edited {ed[2]}, native {nc[2]}; need ≥{MIN_N}).")
elif not EDIT_AGREE_OK:
    verdict="INCONCLUSIVE-CONFOUNDED"
    print(f"\nG6.2 VERDICT: INCONCLUSIVE — edited HF↔GGUF-fp16 agreement {ag_ed[0]}% < 95%; conversion didn't preserve the edit. Q4 delta not interpretable.")
else:
    verdict="PASS" if delta>=-3.0 else "FAIL"
    print(f"\nG6.2 VERDICT: edited {ed[0]}% vs native-country {nc[0]}%  (Δ={delta:+.1f} pts; threshold ≥ −3) -> {verdict}")

json.dump({"hf_vs_gguf_f16_agreement":{"edited_pct":ag_ed[0],"native_pct":ag_nat[0],"all_pct":ag_all[0],"edited_gate_ok":EDIT_AGREE_OK},
           "edited_retention":{"pct":ed[0],"surv":ed[1],"elig":ed[2]},
           "native_country_retention":{"pct":nc[0],"surv":nc[1],"elig":nc[2]},
           "native_global_retention":{"pct":ng[0],"surv":ng[1],"elig":ng[2]},
           "delta_edited_minus_native":(ed[0]-nc[0]) if (ed[0] is not None and nc[0] is not None) else None,
           "verdict":verdict,"threshold":"edited >= native_country - 3pts"},
          open(f"{LLMDB_ROOT}/results/b3_quant_survival_result.json","w"),indent=2)
print("\nwrote /workspace/results/b3_quant_survival_result.json")
