import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math, random, traceback
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
# ============================================================================
# §8.7 NUMERIC-THRESHOLD INSTRUMENT — Phase-0 repeat-variance DIAGNOSTIC.
# Pre-reg: docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md (FROZEN 2026-06-21, D-D1-2).
# Port of experiments/track_b/b1_size_dose_response.py — science path (my_edit/
# compute_P/compute_z/compute_ks/inertness gate) BEHAVIORALLY VERBATIM (LAW#5).
# ADDED (measurement/flags only, science path UNCHANGED):
#   (1) measure(): per held-out entity CONTINUOUS metrics — margin (correct-top
#       distractor logit), nll (-log p(correct)), rank — + binary top-1 (operational,
#       == D1/B1 fuzzy correct()). The low-variance backbone (pre-reg §2.1).
#   (2) DIAGNOSTIC driver: pick the most-UNSTABLE k (binary top-1 nearest 50% on a
#       1-seed staircase), then REPEAT that fixed config N_REPEAT times; report SD of
#       every metric across repeats. World-1 (binary cliff was the problem) vs World-2
#       (genuine trajectory chaos) discrimination (pre-reg §3).
#   (3) DETERMINISTIC flag (env): torch.use_deterministic_algorithms — NUISANCE-CONTROL
#       only, NON-load-bearing (pre-reg §5). Run as a separate process w/ CUBLAS env.
# Pure-capital staircase only (the §8.7 max_relation_concentration axis); no dilutant.
# ============================================================================
MODEL=os.environ.get("MODEL","3b").lower()
CFG={
 "3b":{"id":"Qwen/Qwen2.5-3B","rev":"3aab1f1954e9cc14eb9509a215f9e5ca08227a9b","hp":"qwen25_3b_memit_hparams.json","svd":"cuda"},
 "7b":{"id":"Qwen/Qwen2.5-7B","rev":"d149729398750b98c0af14eb82c78cfe92750796","hp":"qwen25_7b_memit_hparams.json","svd":"cuda"},
}[MODEL]
ID=CFG["id"]; REV=CFG["rev"]; SVD_DEVICE=CFG["svd"]
DETERMINISTIC=os.environ.get("DETERMINISTIC","0")=="1"
ATTN=os.environ.get("ATTN","sdpa")
SEED=int(os.environ.get("SEED","3"))
N_REPEAT=int(os.environ.get("N_REPEAT","5"))
K_PICK=os.environ.get("K_PICK","")            # if set, skip picking, reuse this k (det run reuses non-det's pick)
PICK_GRID=[int(x) for x in os.environ.get("PICK_GRID","18,24,30,36").split(",")]
TOTAL_N=48; HELDOUT_N=24
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/{CFG['hp']}"); L=hp.layers
NULL_THRESH=0.005; L2=1.0
TAG=("det" if DETERMINISTIC else "nondet")

if DETERMINISTIC:
    # CUBLAS_WORKSPACE_CONFIG must be set in the ENV before cuBLAS init (set at launch).
    torch.use_deterministic_algorithms(True)                 # may throw on an op w/o a det kernel -> caught below
    torch.manual_seed(0); torch.cuda.manual_seed_all(0)
    print(f"[determinism] use_deterministic_algorithms(True) ON | CUBLAS_WORKSPACE_CONFIG={os.environ.get('CUBLAS_WORKSPACE_CONFIG','<UNSET!>')} | attn={ATTN}", flush=True)

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda", attn_implementation=ATTN).eval()
print(f"MODEL={MODEL} loaded {ID} | band={L} thresh={NULL_THRESH} | {TAG} seed={SEED} N_REPEAT={N_REPEAT} pick_grid={PICK_GRID} K_PICK={K_PICK or '(auto)'}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"
TMPL={"capital":"The capital of {} is the city of","language":"The official language of {} is"}

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])])}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1,truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def compute_P():
    Ps=[]
    for li,layer in enumerate(L):
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype)
        cov=cov.to(SVD_DEVICE).float()
        S,U=torch.linalg.eigh(cov)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, mode, P=None, cache_c=None, norm_acc=None):
    """Behaviorally VERBATIM from b1_size_dose_response.py / d1 (proven inert, LAW#5).
    norm_acc (measurement-only, science path UNCHANGED): append per-layer ||ΔW||_F."""
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[r["prompt"] for r in requests],
            words=[r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu()
        if mode=="memit":
            cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().double()
            adj=torch.linalg.solve(hp.mom2_update_weight*cov+Kd@Kd.T, Kd); upd=rd@adj.T
        else:
            Pi=P[i].cuda(); ca=cache_c[i].cuda(); Kg=Kd.float().cuda(); rg=rd.float().cuda()
            KK=Kg@Kg.T; KK.add_(ca); del ca
            A=Pi@KK; del KK; A.diagonal().add_(L2)
            B=Pi@Kg@rg.T; del Pi,Kg,rg; torch.cuda.empty_cache()
            upd=torch.linalg.solve(A,B).T.cpu()
            del A,B; torch.cuda.empty_cache()
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        if norm_acc is not None: norm_acc.append(float(upd.norm()))   # measurement only
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T
def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- CONTINUOUS-METRIC measurement (read-only; pre-reg §2.1) ----------
@torch.no_grad()
def measure(heldout):
    margins=[]; nlls=[]; ranks=[]; top1=0
    for e in heldout:
        ids=tok(TMPL["capital"].format(e),return_tensors="pt").to("cuda")
        logits=model(**ids).logits[0,-1].float()
        gold=first_tok(sel[e]["capital"]["truth"])
        t1=int(torch.argmax(logits))
        top1 += 1 if correct(tok.decode([t1]), sel[e]["capital"]["truth"]) else 0   # operational fuzzy top-1 (==D1/B1)
        lg=float(logits[gold]); lsm=torch.log_softmax(logits,dim=-1)
        oth=logits.clone(); oth[gold]=-float("inf")
        margins.append(lg-float(oth.max()))                       # correct - top distractor
        nlls.append(-float(lsm[gold]))
        ranks.append(int((logits>logits[gold]).sum())+1)
    n=len(heldout)
    return {"top1_pct":round(100*top1/n,1),
            "margin_mean":round(sum(margins)/n,4),
            "nll_mean":round(sum(nlls)/n,4),
            "rank_mean":round(sum(ranks)/n,3)}

# ---------- INERTNESS GATE (LAW#5) — VERBATIM behaviorally ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo")
@torch.no_grad()
def pcap(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),0); return float(pr[tgt])
s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=pcap(cons); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
my_p=pcap(cons); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine p(Cairo)={eng_p:.4f} | harness p(Cairo)={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok:
    json.dump({"halt":"LAW5_inertness","model":MODEL,"tag":TAG,"engine_p":eng_p,"harness_p":my_p,"delta":abs(eng_p-my_p)},
              open(f"{LLMDB_ROOT}/architecture_profile/d1instr_{MODEL}_{TAG}_halt_diagnostic.json","w"),indent=2)
    print("LAW#5 fail; HALT.", flush=True); sys.exit(0)
torch.cuda.empty_cache()

# ---------- pools (== B1: held-out baseline-correct capital, disjoint from edit pool) ----------
sel=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
ents_all=[x for x in sel if all(r in sel[x] and "truth" in sel[x][r] for r in ["capital","language"])]
base_correct=[e for e in ents_all if correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"])]
print(f"\nentities={len(ents_all)} | baseline-correct on capital={len(base_correct)}", flush=True)
HELDOUT_USE=min(HELDOUT_N, len(base_correct), len(ents_all)-TOTAL_N)
if HELDOUT_USE<12:
    json.dump({"halt":"insufficient_pool","model":MODEL,"ents_all":len(ents_all),"base_correct":len(base_correct)},
              open(f"{LLMDB_ROOT}/architecture_profile/d1instr_{MODEL}_{TAG}_halt_diagnostic.json","w"),indent=2)
    print("HALT: insufficient pool.", flush=True); sys.exit(0)

def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]; st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf

# fixed (seed-derived) held-out + edit pool + CF -> identical across all repeats; only GPU noise varies
rng=random.Random(SEED)
ho_pool=base_correct[:]; rng.shuffle(ho_pool); heldout=ho_pool[:HELDOUT_USE]
rest=[e for e in ents_all if e not in set(heldout)]; rng.shuffle(rest); edit_pool=rest[:TOTAL_N]
CF=assign_cf(edit_pool,"capital")
print(f"=== FIXED CONFIG seed={SEED} | held-out={len(heldout)} (disjoint, baseline-correct) | edit_pool={len(edit_pool)} ===", flush=True)

P=compute_P(); s_clean=snap()

_LAST_NORMS=[]
def apply_k(k):
    """restore clean -> k sequential pure-capital in-solve AlphaEdit edits (== B1 PHASE A)."""
    global _LAST_NORMS
    restore(s_clean); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    norms=[]
    for e in edit_pool[:k]:
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital",CF[e]),"alphaedit",P,cache,norm_acc=norms)
    _LAST_NORMS=norms
    cap_expr=round(100*sum(predict(TMPL["capital"].format(e))["id"]==first_tok(CF[e]) for e in edit_pool[:k])/k,1)
    return cap_expr

import statistics as st
MODE=os.environ.get("MODE","diagnostic").lower()
SWEEP_GRID=[int(x) for x in os.environ.get("SWEEP_GRID","0,2,4,6,8,10,12,14,16,18,24,30,36,42,48").split(",")]
try:
    base_m=measure(heldout)
    print(f"base(no edit): {base_m}", flush=True)
    if MODE=="sweep":
        # ---- Phase-1 FINE-GRID THRESHOLD SWEEP (pre-reg §4/§6): pure-capital staircase,
        # SINGLE runs (3B World-0: SD=0 -> single run == expected value), continuous curve.
        curve=[]
        for k in SWEEP_GRID:
            if k==0: m=dict(base_m); m["k"]=0; m["cap_expr"]=100.0; m["cap_cum_dW_fro"]=0.0
            else:
                expr=apply_k(k); m=measure(heldout); m["k"]=k; m["cap_expr"]=expr; m["cap_cum_dW_fro"]=round(sum(_LAST_NORMS),3)
            m["corruption_pct"]=round(100.0-m["top1_pct"],1)
            curve.append(m)
            print(f"  [sweep] k={k:>2}: top1={m['top1_pct']:>5}% corrupt={m['corruption_pct']:>5}% margin={m['margin_mean']:>8} nll={m['nll_mean']:>7} rank={m['rank_mean']:>7} cum||ΔW||={m['cap_cum_dW_fro']} expr={m['cap_expr']}%", flush=True)
        # locate thresholds (pre-reg §6: operational top-1 corruption; spread moot on 3B World-0)
        def cross(thr):
            below=[c for c in curve if c["corruption_pct"]<thr]; above=[c for c in curve if c["corruption_pct"]>=thr]
            return above[0]["k"] if above else None
        warn_k=cross(5.0); hard_k=cross(20.0)
        knee_k=next((c["k"] for c in curve if c["margin_mean"]<0), None)   # margin sign-flip = correct-token loses to top distractor
        all_expr=all(c["cap_expr"]>=95 for c in curve)
        print(f"\n=== SWEEP THRESHOLDS (3B, single-run, World-0 SD=0) ===", flush=True)
        print(f"  WARNING (corruption≥5%)  first crossed at k={warn_k}", flush=True)
        print(f"  HARD    (corruption≥20%) first crossed at k={hard_k}", flush=True)
        print(f"  margin-sign-flip (knee)  at k={knee_k}", flush=True)
        out={"experiment":"d1_threshold_sweep","model":MODEL,"hf_id":ID,"revision":REV,"tag":TAG,"deterministic":DETERMINISTIC,
             "mode":"sweep","band":L,"heldout_n":HELDOUT_USE,"seed":SEED,"sweep_grid":SWEEP_GRID,"engine":"kmeng01/memit UNMODIFIED",
             "base_no_edit":base_m,"curve":curve,"warning_k_corrupt5":warn_k,"hard_k_corrupt20":hard_k,"margin_knee_k":knee_k,
             "all_expr_ok":all_expr,"note":"single-run valid: 3B run-to-run SD=0 (variance diagnostic World-0); thresholds anti-conservative (pure-capital, no cross-relation load) -> ship <= these, mixed-load spot-check pending"}
        RUN_ID=os.environ.get("RUN_ID","")
        out["run_id"]=RUN_ID; out["seed"]=SEED
        fn=f"d1_threshold_curve_{MODEL}_{TAG}_s{SEED}{('_'+RUN_ID) if RUN_ID else ''}.json"
        json.dump(out,open(f"{LLMDB_ROOT}/results/{fn}","w"),indent=2,default=str)
        print(f"\nWROTE results/{fn}", flush=True)
        print(f"D1INSTR_{MODEL.upper()}_SWEEP_DONE", flush=True)
        sys.exit(0)
    if MODE=="mixedload":
        # ---- MIXED-LOAD SMOKE: does realistic OTHER-relation load break the k<=2 pure-capital ceiling?
        # paired per order: held-out CAPITAL corruption after k capital edits (PURE) vs after
        # k capital + MIX_LANG language edits on disjoint entities (MIXED). pure-capital is
        # anti-conservative (D1 cross-relation term); this tests the conservative deployment case.
        import math as _m
        N_ORDERS=int(os.environ.get("N_ORDERS","12")); MIX_LANG=int(os.environ.get("MIX_LANG","12"))
        MIXK_GRID=[int(x) for x in os.environ.get("MIXK_GRID","1,2,3").split(",")]
        CF_lang=assign_cf(edit_pool,"language")
        z=1.645
        pooled={k:{"pure_wrong":0,"mixed_wrong":0,"n":0,"pure_po":[],"mixed_po":[],"lang_expr":[]} for k in MIXK_GRID}
        def hc_wrong(): return sum(0 if correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"]) else 1 for e in heldout)
        for o in range(N_ORDERS):
            org=random.Random(2000+o)
            cpool=edit_pool[:]; org.shuffle(cpool); lpool=edit_pool[:]; org.shuffle(lpool)
            for k in MIXK_GRID:
                cap_ents=cpool[:k]; lang_ents=[e for e in lpool if e not in set(cap_ents)][:MIX_LANG]
                restore(s_clean); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
                for e in cap_ents:
                    with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital",CF[e]),"alphaedit",P,cache)
                pw=hc_wrong()
                for e in lang_ents:
                    with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"language",CF_lang[e]),"alphaedit",P,cache)
                mw=hc_wrong()
                lexpr=round(100*sum(predict(TMPL["language"].format(e))["id"]==first_tok(CF_lang[e]) for e in lang_ents)/len(lang_ents),1)
                pooled[k]["pure_wrong"]+=pw; pooled[k]["mixed_wrong"]+=mw; pooled[k]["n"]+=len(heldout)
                pooled[k]["pure_po"].append(round(100*pw/len(heldout),1)); pooled[k]["mixed_po"].append(round(100*mw/len(heldout),1)); pooled[k]["lang_expr"].append(lexpr)
            print(f"  [mixed] order {o}: "+" ".join(f"k{k}:pure{pooled[k]['pure_po'][-1]}->mix{pooled[k]['mixed_po'][-1]}%" for k in MIXK_GRID), flush=True)
        def wu(x,n): p=x/n; return round(100*((p+z*z/(2*n)+z*_m.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)),2)
        curve=[]
        for k in MIXK_GRID:
            d=pooled[k]; n=d["n"]
            row={"cap_k":k,"mix_lang":MIX_LANG,"n":n,"pure_pct":round(100*d["pure_wrong"]/n,2),"mixed_pct":round(100*d["mixed_wrong"]/n,2),
                 "pure_wilson_up":wu(d["pure_wrong"],n),"mixed_wilson_up":wu(d["mixed_wrong"],n),
                 "delta_pp":round(100*(d["mixed_wrong"]-d["pure_wrong"])/n,2),"mixed_worst":max(d["mixed_po"]),"lang_expr_min":min(d["lang_expr"])}
            curve.append(row)
            print(f"  [mixed] cap_k={k} (+{MIX_LANG} lang): pure={row['pure_pct']}% -> mixed={row['mixed_pct']}% (UCB {row['mixed_wilson_up']}%) delta={row['delta_pp']}pp worst={row['mixed_worst']}% langexpr_min={row['lang_expr_min']}%", flush=True)
        ceiling_pure=max([r["cap_k"] for r in curve if r["pure_pct"]==0.0] or [0])
        ceiling_mixed=max([r["cap_k"] for r in curve if r["mixed_pct"]==0.0] or [0])
        res={"experiment":"d1_mixedload_smoke","model":MODEL,"seed":SEED,"n_orders":N_ORDERS,"mix_lang":MIX_LANG,"mixk_grid":MIXK_GRID,
             "heldout_n":HELDOUT_USE,"engine":"kmeng01/memit UNMODIFIED","curve":curve,
             "clean_ceiling_pure_capital":ceiling_pure,"clean_ceiling_mixed_load":ceiling_mixed,
             "note":"held-out CAPITAL corruption; PURE=k capital only, MIXED=k capital + MIX_LANG language edits (disjoint entities). Tests whether other-relation load breaks the k<=2 pure ceiling. Anti-conservative pure baseline."}
        json.dump(res,open(f"{LLMDB_ROOT}/results/d1_mixedload_smoke_{MODEL}_s{SEED}.json","w"),indent=2,default=str)
        print(f"\n=== MIXED-LOAD SMOKE (held-out capital; +{MIX_LANG} language) ===", flush=True)
        print(f"  clean ceiling pure-capital k={ceiling_pure} | clean ceiling UNDER mixed load k={ceiling_mixed}", flush=True)
        print(f"WROTE results/d1_mixedload_smoke_{MODEL}_s{SEED}.json\nD1INSTR_{MODEL.upper()}_MIXED_DONE", flush=True)
        sys.exit(0)
    if MODE=="lowk":
        # ---- Phase-2 LOW-K RANDOMIZED-ORDER replication (cross-family FIX-FIRST):
        # fixed held-out; N_ORDERS random edit-ORDERS; pool binary top-1 outcomes per k;
        # threshold = earliest k where one-sided 95% Wilson UPPER bound on corruption crosses level.
        N_ORDERS=int(os.environ.get("N_ORDERS","12"))
        LOWK_GRID=[int(x) for x in os.environ.get("LOWK_GRID","4,6,8,10,12,14").split(",")]
        import math as _m
        z=1.645   # one-sided 95% upper (conservative safety bound)
        # per held-out entity, was it WRONG after k edits — pooled across orders
        pooled={k:{"wrong":0,"n":0,"per_order_corr":[]} for k in LOWK_GRID}
        for o in range(N_ORDERS):
            org=random.Random(1000+o)
            pool=edit_pool[:]; org.shuffle(pool)                       # distinct edit ORDER+membership of first-k
            for k in LOWK_GRID:
                restore(s_clean); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
                for e in pool[:k]:
                    with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital",CF[e]),"alphaedit",P,cache)
                wrong=sum(0 if correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"]) else 1 for e in heldout)
                pooled[k]["wrong"]+=wrong; pooled[k]["n"]+=len(heldout); pooled[k]["per_order_corr"].append(round(100*wrong/len(heldout),1))
            print(f"  [lowk] order {o}: " + " ".join(f"k{k}={pooled[k]['per_order_corr'][-1]}%" for k in LOWK_GRID), flush=True)
        def wilson_upper(x,n):
            if n==0: return None
            p=x/n; return (p + z*z/(2*n) + z*_m.sqrt(p*(1-p)/n + z*z/(4*n*n)))/(1+z*z/n)
        curve=[]
        for k in LOWK_GRID:
            x,n=pooled[k]["wrong"],pooled[k]["n"]; ub=wilson_upper(x,n)
            row={"k":k,"wrong":x,"n":n,"corr_pooled_pct":round(100*x/n,2),"wilson_upper_pct":round(100*ub,2),
                 "observed_worst_pct":max(pooled[k]["per_order_corr"]),"per_order_corr_pct":pooled[k]["per_order_corr"]}
            curve.append(row)
            print(f"  [lowk] k={k}: pooled_corr={row['corr_pooled_pct']}% wilson95up={row['wilson_upper_pct']}% worst={row['observed_worst_pct']}% (x={x}/n={n})", flush=True)
        def earliest(field,thr): return next((r["k"] for r in curve if r[field]>=thr), None)
        res={"experiment":"d1_threshold_lowk_orders","model":MODEL,"tag":TAG,"seed":SEED,"n_orders":N_ORDERS,"lowk_grid":LOWK_GRID,
             "heldout_n":HELDOUT_USE,"z_one_sided":z,"engine":"kmeng01/memit UNMODIFIED","curve":curve,
             "WARNING":{"wilson_ucb_k":earliest("wilson_upper_pct",5.0),"pooled_k":earliest("corr_pooled_pct",5.0),"observed_worst_k":earliest("observed_worst_pct",5.0)},
             "HARD":{"wilson_ucb_k":earliest("wilson_upper_pct",20.0),"pooled_k":earliest("corr_pooled_pct",20.0),"observed_worst_k":earliest("observed_worst_pct",20.0)},
             "note":"binary top-1 corruption; one-sided 95% Wilson UCB primary; pooled+observed-worst reported; pure-capital (anti-conservative, mixed-load untested); held-out=24 discreteness 4.17%/entity"}
        _lt=os.environ.get("LOWK_TAG","")
        json.dump(res,open(f"{LLMDB_ROOT}/results/d1_threshold_lowk_{MODEL}_s{SEED}{('_'+_lt) if _lt else ''}.json","w"),indent=2,default=str)
        print(f"\n=== LOW-K THRESHOLDS (binary top-1, 1-sided 95% Wilson UCB primary) ===", flush=True)
        print(f"  WARNING(5%):  UCB k={res['WARNING']['wilson_ucb_k']} | pooled k={res['WARNING']['pooled_k']} | worst k={res['WARNING']['observed_worst_k']}", flush=True)
        print(f"  HARD(20%):    UCB k={res['HARD']['wilson_ucb_k']} | pooled k={res['HARD']['pooled_k']} | worst k={res['HARD']['observed_worst_k']}", flush=True)
        print(f"WROTE results/d1_threshold_lowk_{MODEL}_s{SEED}.json\nD1INSTR_{MODEL.upper()}_LOWK_DONE", flush=True)
        sys.exit(0)
    # ---- pick the most-unstable k (binary top-1 nearest 50%) unless K_PICK given ----
    if K_PICK:
        K=int(K_PICK); pick_scan=None
        print(f"[pick] reusing K_PICK={K}", flush=True)
    else:
        pick_scan=[]
        for k in PICK_GRID:
            expr=apply_k(k); m=measure(heldout); m["k"]=k; m["cap_expr"]=expr
            pick_scan.append(m); print(f"  [pick] k={k}: top1={m['top1_pct']}% margin={m['margin_mean']} nll={m['nll_mean']} rank={m['rank_mean']} expr={expr}%", flush=True)
        K=min(PICK_GRID, key=lambda k: abs(next(m["top1_pct"] for m in pick_scan if m["k"]==k)-50.0))
        print(f"[pick] most-unstable k (top1 nearest 50%) = {K}", flush=True)
    # ---- REPEAT the fixed config N_REPEAT times; only GPU nondeterminism varies ----
    reps=[]
    for r in range(N_REPEAT):
        expr=apply_k(K); m=measure(heldout); m["rep"]=r; m["cap_expr"]=expr
        reps.append(m); print(f"  [repeat {TAG}] rep{r} k={K}: top1={m['top1_pct']}% margin={m['margin_mean']} nll={m['nll_mean']} rank={m['rank_mean']} expr={expr}%", flush=True)
    def sd(key): vals=[m[key] for m in reps]; return round(st.pstdev(vals),4) if len(vals)>1 else 0.0
    def mn(key): return round(st.mean([m[key] for m in reps]),4)
    sds={k:sd(k) for k in ["top1_pct","margin_mean","nll_mean","rank_mean"]}
    means={k:mn(k) for k in ["top1_pct","margin_mean","nll_mean","rank_mean"]}
    margin_range=abs(base_m["margin_mean"]-means["margin_mean"])   # clean-vs-corrupt dynamic range proxy
    print(f"\n=== {TAG} DIAGNOSTIC k={K} | N_REPEAT={N_REPEAT} ===", flush=True)
    print(f"  MEANS: {means}", flush=True)
    print(f"  SDs  : {sds}", flush=True)
    print(f"  margin clean->corrupt range≈{round(margin_range,4)} | SD(margin)/range={round(sds['margin_mean']/margin_range,3) if margin_range else 'na'}", flush=True)
    out={"experiment":"d1_threshold_instrument_variance_diagnostic","model":MODEL,"hf_id":ID,"revision":REV,
         "tag":TAG,"deterministic":DETERMINISTIC,"cublas":os.environ.get("CUBLAS_WORKSPACE_CONFIG"),"attn":ATTN,
         "seed":SEED,"k_unstable":K,"pick_grid":PICK_GRID,"pick_scan":pick_scan,"n_repeat":N_REPEAT,
         "heldout_n":HELDOUT_USE,"total_n":TOTAL_N,"band":L,"engine":"kmeng01/memit UNMODIFIED",
         "base_no_edit":base_m,"repeats":reps,"means":means,"sds":sds,"margin_dynamic_range":round(margin_range,4),
         "all_expr_ok":all(m["cap_expr"]>=95 for m in reps)}
    json.dump(out,open(f"{LLMDB_ROOT}/results/d1_instrument_variance_diagnostic_{MODEL}_{TAG}.json","w"),indent=2,default=str)
    print(f"\nWROTE results/d1_instrument_variance_diagnostic_{MODEL}_{TAG}.json", flush=True)
    print(f"D1INSTR_{MODEL.upper()}_{TAG.upper()}_DONE", flush=True)
except Exception as ex:
    tb=traceback.format_exc()
    json.dump({"halt":"exception","model":MODEL,"tag":TAG,"deterministic":DETERMINISTIC,"error":str(ex),"traceback":tb},
              open(f"{LLMDB_ROOT}/architecture_profile/d1instr_{MODEL}_{TAG}_halt_diagnostic.json","w"),indent=2)
    print(f"\n!!! EXCEPTION ({TAG}) -> architecture_profile/d1instr_{MODEL}_{TAG}_halt_diagnostic.json\n{tb}", flush=True)
    sys.exit(1)
