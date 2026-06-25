import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# R13 — STORAGE-PASS / BEHAVIOR-FAIL split base-rate (CP2 read-contract matrix R13).
# Pre-reg: docs/R13_STORAGE_BEHAVIOR_SPLIT_PREREG.md. §8.9 mandates L1 (written) vs L2
# (fires) as distinct probes; named failure storage-pass/behavior-fail. CP2: true L1
# SELECT is index-delegated -> weights-only approximation: L1 = canonical-prompt top-1,
# L2 = natural paraphrase top-1. Headline = base rate of L1-pass & L2-fail (silent edits).
# Engine UNMODIFIED; primitives VERBATIM from r2/r9. LAW#5 gate.
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | AlphaEdit thresh={NULL_THRESH} L2={L2}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,5)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"top5":[tok.decode([int(i)]) for i in t.indices],"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def js(a,b):
    p=a.double(); q=b.double(); m=0.5*(p+q)
    def k(x,y): x=x.clamp_min(1e-12); y=y.clamp_min(1e-12); return float((x*(x.log()-y.log())).sum())
    return 0.5*k(p,m)+0.5*k(q,m)
def locpct(post,pre,pl): return round(100*sum(1-js(post[p]["dist"],pre[p]["dist"])/LN2 for p in pl)/len(pl),2)
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, mode, P=None, cache_c=None):
    """VERBATIM AlphaEdit/MEMIT solve (engine primitives, proven inert)."""
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
            Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
            A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T
            upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

CANON="The capital of {} is the city of"                      # L1 storage proxy (the edit string)
PARA=["{}'s capital city is called","The city that serves as the capital of {} is","If you visit {}, its capital city is"]  # L2 behavioral (natural rephrasings)
def reqc(country,cap): return [{"prompt":CANON,"subject":country,"target_new":{"str":" "+cap}}]

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=CANON.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is located on the continent of"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,reqc(e,"Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(reqc(e,"Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  |Δexpr|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- stimulus ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
cands=[c for c in sel if single_tok(sel[c]["capital"]["truth"])]
N=int(os.environ.get("N_EDIT","24")); M=int(os.environ.get("N_CONTROL","10"))
edited=cands[:N]; control=cands[N:N+M]
realcaps=[sel[c]["capital"]["truth"] for c in cands]
def assign_X(cs):
    out={}
    for i,c in enumerate(cs):
        rc=sel[c]["capital"]["truth"]; j=(i+7)%len(realcaps)
        while realcaps[j].lower()==rc.lower(): j=(j+1)%len(realcaps)
        out[c]=realcaps[j]
    return out
X=assign_X(edited)
print(f"\nR13 | edited={len(edited)} | control={len(control)} | candidates={len(cands)}", flush=True)

def top1_is(prompt, want_tok): pr=predict(prompt); return bool(pr["id"]==want_tok), pr["tok"].strip()

# ---------- NATIVE sanity control (probes valid?) ----------
print("\n=== NATIVE control: do L1 + L2 probes fire on REAL capitals (unedited)? ===", flush=True)
ctrl=[]
for c in control:
    rc=sel[c]["capital"]["truth"]; rct=first_tok(rc)
    l1,_=top1_is(CANON.format(c), rct)
    para_hits=[top1_is(p.format(c), rct)[0] for p in PARA]
    ctrl.append({"country":c,"realcap":rc,"L1_native":l1,"L2_para_native":para_hits,"L2_native_primary":para_hits[0]})
c_l1=sum(x["L1_native"] for x in ctrl); c_l2=sum(x["L2_native_primary"] for x in ctrl)
c_l2any=sum(any(x["L2_para_native"]) for x in ctrl)
print(f"  native L1 (canonical)={c_l1}/{len(control)} | native L2 primary-paraphrase={c_l2}/{len(control)} | L2 any-paraphrase={c_l2any}/{len(control)}", flush=True)

# ---------- WRITE forward edits ----------
print("\n=== WRITE: forward edits (capital -> counterfactual X) ===", flush=True)
P=compute_P(); cache_c=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([{"prompt":CANON,"subject":c,"target_new":{"str":" "+X[c]}} for c in edited],"alphaedit",P,cache_c)

# ---------- L1 / L2 classification ----------
rows=[]
for c in edited:
    xt=first_tok(X[c])
    l1,l1obs=top1_is(CANON.format(c), xt)                       # L1 storage proxy (canonical)
    para=[top1_is(p.format(c), xt) for p in PARA]
    l2_primary=para[0][0]; l2_rate=sum(h for h,_ in para)/len(para)
    rows.append({"country":c,"X":X[c],"L1_canonical":l1,"L1_obs":l1obs,
                 "L2_primary_para":l2_primary,"L2_para_hits":[h for h,_ in para],"L2_rate":round(l2_rate,3)})
restore(s0)

# 2x2 (L1 canonical x L2 primary-paraphrase)
both=sum(r["L1_canonical"] and r["L2_primary_para"] for r in rows)
storage_pass_behavior_fail=sum(r["L1_canonical"] and not r["L2_primary_para"] for r in rows)
behavior_pass_storage_fail=sum((not r["L1_canonical"]) and r["L2_primary_para"] for r in rows)
neither=sum((not r["L1_canonical"]) and (not r["L2_primary_para"] ) for r in rows)
n=len(rows)
summary={
 "harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/single-batch/capital","label":"CHARACTERIZATION",
 "n_edited":n,
 "native_control_L1":f"{c_l1}/{len(control)}","native_control_L2_primary":f"{c_l2}/{len(control)}","native_control_L2_any":f"{c_l2any}/{len(control)}",
 "L1_storage_pass":f"{both+storage_pass_behavior_fail}/{n}",
 "L2_behavior_pass_primary":f"{both+behavior_pass_storage_fail}/{n}",
 "STORAGE_PASS_BEHAVIOR_FAIL":f"{storage_pass_behavior_fail}/{n}","rate":round(100*storage_pass_behavior_fail/n,1),
 "both_pass":f"{both}/{n}","behavior_pass_storage_fail":f"{behavior_pass_storage_fail}/{n}","neither":f"{neither}/{n}",
 "mean_L2_paraphrase_rate_among_L1pass":round(100*sum(r["L2_rate"] for r in rows if r["L1_canonical"])/max(1,both+storage_pass_behavior_fail),1),
}
print("\n=== R13 SUMMARY (storage L1 = canonical top-1; behavior L2 = primary paraphrase top-1) ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
interp=("STORAGE/BEHAVIOR SPLIT IS REAL + LARGE: many edits store (canonical top-1) but DON'T fire on natural paraphrase -> measuring L1 alone over-reports; validates §8.9 separate-probe mandate"
        if (c_l2>=0.6*len(control) and summary["rate"]>=10)
        else ("SPLIT COLLAPSES at this scope: L1 and L2 agree (storage-pass/behavior-fail ~0) -> probes precautionary here (still: true L1 SELECT is index-delegated, CP2)"
              if (c_l2>=0.6*len(control) and summary["rate"]<10) else "DEGENERATE controls -> inspect"))
print(f"\n  INTERPRETATION: {interp}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/r13_storage_behavior_split.json")
json.dump({"summary":summary,"interpretation":interp,"rows":rows,"native_control":ctrl,
           "stimulus":{"L1_canonical":CANON,"L2_paraphrases":PARA}}, open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("R13_DONE", flush=True)
