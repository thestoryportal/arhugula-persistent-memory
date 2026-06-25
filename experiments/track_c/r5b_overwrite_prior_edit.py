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
# R5b — OVERWRITE-PRIOR-EDIT: the unmeasured UPDATE cell (F1 C3/R5).
# Pre-reg: docs/R5B_OVERWRITE_PRIOR_EDIT_PREREG.md. 3 arms matched single-prompt.
# NOVEL (no competitor) / PRIOR (pretrained competitor) / OVERWRITE-EDIT (step1 fictional->v1,
# step2 same->v2; v2's only competitor is the prior EDIT v1). Metric = held-out P_test firing.
# Mechanism: do v2 failures resurface v1 (entrench) vs other (instability)? Engine UNMODIFIED. LAW#5 gate.
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
    """VERBATIM AlphaEdit/MEMIT solve (engine primitives, proven inert). cache_c accumulates if passed across calls."""
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

CANON="The capital of {} is the city of"
PTEST=["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"]
def rq(subj,targ): return {"prompt":CANON,"subject":subj,"target_new":{"str":" "+targ}}

# ---------- INERTNESS GATE ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=CANON.format(e); tgt=first_tok("Cairo")
pre={cons:predict(cons)}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,[rq(e,"Cairo")],hp,copy=False,return_orig_weights=False)
engp=float(predict(cons)["dist"][tgt]); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit([rq(e,"Cairo")],"memit")
myp=float(predict(cons)["dist"][tgt]); restore(s0)
ok=abs(engp-myp)<0.05; print(f"  |Δexpr|={abs(engp-myp):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("HALT",flush=True); sys.exit(0)

# ---------- stimulus ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
realcands=[c for c in sel if single_tok(sel[c]["capital"]["truth"])]; realcaps=[sel[c]["capital"]["truth"] for c in realcands]
N=int(os.environ.get("N_PER_ARM","16"))
prior_c=realcands[:N]
FICTION=["Zorbland","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane","Mophgar","Brinduun",
         "Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin","Lurmaxen","Pradnoll","Kessivar","Wombryne","Halquin"][:N]
def cap_at(i,offset): return realcaps[(i+offset)%len(realcaps)]
Xprior={c: (lambda rc,i: next(realcaps[(i+5+k)%len(realcaps)] for k in range(len(realcaps)) if realcaps[(i+5+k)%len(realcaps)].lower()!=rc.lower()))(sel[c]["capital"]["truth"],i) for i,c in enumerate(prior_c)}
V1={c:cap_at(i,3) for i,c in enumerate(FICTION)}      # step-1 novel capital
V2={c:cap_at(i,11) for i,c in enumerate(FICTION)}     # step-2 (must differ from V1)
for i,c in enumerate(FICTION):
    k=11
    while V2[c].lower()==V1[c].lower(): k+=1; V2[c]=cap_at(i,k)
Ynovel={c:cap_at(i,3) for i,c in enumerate(FICTION)}  # NOVEL arm target (same family of caps)
print(f"\nR5b | N/arm={N} | prior={len(prior_c)} fiction={len(FICTION)}", flush=True)

def fires(country, targ_tok):
    hits=[]; obs=[]
    for t in PTEST:
        pr=predict(t.format(country)); hits.append(bool(pr["id"]==targ_tok)); obs.append(pr["tok"].strip())
    return hits, obs
def canon_took(country, targ_tok): return bool(predict(CANON.format(country))["id"]==targ_tok)

s_base=snap(); P=compute_P()

def measure(facts, targmap, v1map=None):
    rows=[]
    for c in facts:
        tt=first_tok(targmap[c]); hits,obs=fires(c,tt); l1=canon_took(c,tt)
        row={"subj":c,"target":targmap[c],"L1_canon":l1,"ptest_hits":hits,"ptest_obs":obs,
             "any":any(hits),"all":all(hits),"rate":round(sum(hits)/len(hits),3)}
        if v1map is not None:
            v1t=first_tok(v1map[c])
            # among v2 P_test FAILURES, does v1 resurface?
            v1res=[ (not hits[i]) and (predict(PTEST[i].format(c))["id"]==v1t) for i in range(len(PTEST))]
            row["v1"]=v1map[c]; row["v1_resurface_among_fail"]=v1res
        rows.append(row)
    return rows

def summ(name, rows, v1=False):
    n=len(rows); mean=round(100*sum(r["rate"] for r in rows)/n,1)
    allh=sum(r["all"] for r in rows); anyh=sum(r["any"] for r in rows); l1=sum(r["L1_canon"] for r in rows)
    dist=[0,0,0,0]
    for r in rows: dist[sum(r["ptest_hits"])]+=1
    s={"arm":name,"n":n,"L1_took":f"{l1}/{n}","mean_rate":mean,"all_hit":f"{allh}/{n}","any":f"{anyh}/{n}","dist_0123":dist}
    if v1:
        fails=sum(sum(1 for h in r["ptest_hits"] if not h) for r in rows)
        v1r=sum(sum(1 for x in r["v1_resurface_among_fail"] if x) for r in rows)
        s["v1_resurface_among_fails"]=f"{v1r}/{fails}" if fails else "n/a"
    print(f"  >>> {name}: L1 {s['L1_took']} | mean {mean}% | all-hit {s['all_hit']} | any {s['any']} | dist{dist}"+(f" | v1-resurface {s.get('v1_resurface_among_fails')}" if v1 else ""), flush=True)
    return s

print("\n=== ARMS ===", flush=True)
# NOVEL
restore(s_base); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([rq(c,Ynovel[c]) for c in FICTION],"alphaedit",P,cache)
novel=measure(FICTION,Ynovel); restore(s_base)
# PRIOR
restore(s_base); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([rq(c,Xprior[c]) for c in prior_c],"alphaedit",P,cache)
prior=measure(prior_c,Xprior); restore(s_base)
# OVERWRITE-EDIT: step1 ->v1 (cache from 0), step2 ->v2 (accumulating)
restore(s_base); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([rq(c,V1[c]) for c in FICTION],"alphaedit",P,cache)     # step 1
my_edit([rq(c,V2[c]) for c in FICTION],"alphaedit",P,cache)     # step 2 (accumulating)
overwrite=measure(FICTION,V2,v1map=V1); restore(s_base)

print("\n=== R5b SUMMARY (held-out P_test firing; v2 target for OVERWRITE) ===", flush=True)
S={"NOVEL":summ("NOVEL",novel),"PRIOR":summ("PRIOR",prior),"OVERWRITE_EDIT":summ("OVERWRITE_EDIT",overwrite,v1=True)}
interp=("OVERWRITE-EDIT ~ NOVEL: prior edits are WEAK competitors -> updates-over-edits ROBUST (realistic update path fine)"
        if S["OVERWRITE_EDIT"]["mean_rate"]>=0.75*S["NOVEL"]["mean_rate"]
        else ("OVERWRITE-EDIT ~ PRIOR: prior edits ENTRENCH -> updates-over-edits FRAGILE (needs diverse recipe/side-store)"
              if S["OVERWRITE_EDIT"]["mean_rate"]<=1.5*S["PRIOR"]["mean_rate"] else "OVERWRITE-EDIT INTERMEDIATE between NOVEL and PRIOR"))
print(f"\n  CELLS: NOVEL {S['NOVEL']['mean_rate']}% | OVERWRITE-EDIT {S['OVERWRITE_EDIT']['mean_rate']}% | PRIOR {S['PRIOR']['mean_rate']}%", flush=True)
print(f"  INTERPRETATION: {interp}", flush=True)
out={"experiment":"R5b_overwrite_prior_edit","label":"CHARACTERIZATION","prereg":"docs/R5B_OVERWRITE_PRIOR_EDIT_PREREG.md",
     "arms":S,"interpretation":interp,"templates":{"canonical":CANON,"P_test":PTEST},
     "rows":{"NOVEL":novel,"PRIOR":prior,"OVERWRITE_EDIT":overwrite}}
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/r5b_overwrite_prior_edit.json")
json.dump(out,open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("R5b_DONE", flush=True)
