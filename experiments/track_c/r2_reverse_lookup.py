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
# R2 — REVERSE-LOOKUP / bidirectional native-knowing (CP2 read-contract matrix R2).
# Pre-reg: docs/R2_REVERSE_LOOKUP_PREREG.md. LABEL PRE-COMMITTED: CHARACTERIZATION,
# NOT falsification (D16 auto-generates reverse; §11.2 reverse=storage/index-delegated;
# weight-native reverse-fail CONFIRMS overlay architecture). Q: does a forward edit
# (C->X, keyed on subject C) create a weight-native REVERSE edge (X->C)? Reversal curse
# predicts ~0. Value = degree of bidirectional native-knowing -> bounds read contract.
# capital<->country ONLY (bijective). Engine UNMODIFIED. primitives VERBATIM from r9. LAW#5 gate.
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

FWD="The capital of {} is the city of"   # forward edit prompt (subject=country)
def reqc(country,cap): return [{"prompt":FWD,"subject":country,"target_new":{"str":" "+cap}}]

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=FWD.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is located on the continent of"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,reqc(e,"Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(reqc(e,"Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} | harness expr={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- build edited set + counterfactual capitals + native-reverse control set ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
# keep countries whose REAL capital is single-token (clean reverse grading) AND country first-token usable
cands=[c for c in sel if single_tok(sel[c]["capital"]["truth"])]
N=int(os.environ.get("N_EDIT","24")); M=int(os.environ.get("N_CONTROL","16"))
edited=cands[:N]; control=cands[N:N+M]
# counterfactual single-token capital X for each edited country = some OTHER country's real capital (X != real cap)
realcaps=[sel[c]["capital"]["truth"] for c in cands]
def assign_X(country_list):
    out={}
    for i,c in enumerate(country_list):
        rc=sel[c]["capital"]["truth"]; j=(i+7)%len(realcaps)
        while realcaps[j].lower()==rc.lower(): j=(j+1)%len(realcaps)
        out[c]=realcaps[j]
    return out
X=assign_X(edited)
print(f"\nR2 | edited={len(edited)} countries | control(native-reverse)={len(control)} | candidates(single-tok cap)={len(cands)}", flush=True)

REV_T=["{} is the capital of the country of","{} is the capital city of"]   # reverse prompts (subject=capital city)
def country_tok(c): return first_tok(c)
def rev_score(cap_city, ctok):
    # P(country) at the reverse prompts; top1 hit on either phrasing
    best={"top1":False,"p":0.0,"obs":""}
    for t in REV_T:
        pr=predict(t.format(cap_city)); p=float(pr["dist"][ctok])
        if p>best["p"]: best={"top1":bool(pr["id"]==ctok),"p":round(p,4),"obs":pr["tok"].strip(),"top5":pr["top5"]}
        if pr["id"]==ctok: best["top1"]=True
    return best

s_base=snap()
# PRE-EDIT: reverse base rate (X->C should be ~0; X natively points to its real country) + native-reverse control
print("\n=== PRE-EDIT capture ===", flush=True)
for c in edited:
    c_tok=country_tok(c); pre=rev_score(X[c], c_tok)
    sel[c]["_pre_rev"]=pre
# native-reverse positive control: REAL capital -> its country (template/capability valid?)
ctrl_native=[]
for c in control:
    rc=sel[c]["capital"]["truth"]; hit=rev_score(rc, country_tok(c))
    ctrl_native.append({"country":c,"realcap":rc,"top1":hit["top1"],"p":hit["p"],"obs":hit["obs"]})
ctrl_rate=sum(x["top1"] for x in ctrl_native)
print(f"  NATIVE-REVERSE control: {ctrl_rate}/{len(control)} real-capital->country fire natively (template/capability valid if high)", flush=True)
base_rev=sum(sel[c]["_pre_rev"]["top1"] for c in edited)
print(f"  edited-set reverse BASE rate (X->C pre-edit) = {base_rev}/{len(edited)} (want ~0)", flush=True)

# ---------- WRITE forward edits C->X (single joint AlphaEdit) ----------
print("\n=== WRITE: forward edits (country -> counterfactual capital) ===", flush=True)
P=compute_P(); cache_c=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
wreq=[{"prompt":FWD,"subject":c,"target_new":{"str":" "+X[c]}} for c in edited]
my_edit(wreq,"alphaedit",P,cache_c)
# POST-EDIT probes
rows=[]
for c in edited:
    c_tok=country_tok(c); x_tok=first_tok(X[c])
    fwd=predict(FWD.format(c)); took=bool(fwd["id"]==x_tok)
    post=rev_score(X[c], c_tok); pre=sel[c]["_pre_rev"]
    rows.append({"country":c,"X":X[c],"realcap":sel[c]["capital"]["truth"],
                 "fwd_took":took,"fwd_obs":fwd["tok"].strip(),
                 "rev_pre_top1":pre["top1"],"rev_post_top1":post["top1"],
                 "rev_pre_P":pre["p"],"rev_post_P":post["p"],"dP":round(post["p"]-pre["p"],4),
                 "rev_post_obs":post["obs"],"rev_post_top5":post.get("top5")})
restore(s_base)

# ---------- ANALYSIS ----------
took=[r for r in rows if r["fwd_took"]]
rev_post=sum(r["rev_post_top1"] for r in rows); rev_pre=sum(r["rev_pre_top1"] for r in rows)
# among edits that TOOK forward, how many created a reverse edge?
rev_among_took=sum(r["rev_post_top1"] for r in took)
import statistics as st
dPs=[r["dP"] for r in took] or [0]
summary={
 "harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/single-batch/capital<->country","label":"CHARACTERIZATION (not falsification; D16 auto-reverse + §11.2)",
 "n_edited":len(edited),"n_control":len(control),
 "native_reverse_control_fire":f"{ctrl_rate}/{len(control)}",
 "forward_took":f"{len(took)}/{len(edited)}",
 "reverse_base_rate_pre":f"{rev_pre}/{len(edited)}",
 "reverse_post_top1":f"{rev_post}/{len(edited)}",
 "reverse_post_top1_among_forward_took":f"{rev_among_took}/{len(took)}",
 "mean_dP_country_among_took":round(st.mean(dPs),4),
 "median_dP_country_among_took":round(st.median(dPs),4),
}
print("\n=== R2 SUMMARY (CHARACTERIZATION) ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
interp=("WRITE-ONLY EDGE (reversal curse confirmed): forward took, native-reverse template valid, but edited reverse ~base -> reverse is NOT weight-native; index/auto-generated (D16), §11.2 confirmed"
        if (len(took)>=0.8*len(edited) and ctrl_rate>=0.6*len(control) and rev_among_took<=0.2*max(1,len(took)))
        else "NON-NULL reverse or degenerate controls — inspect (see rows)")
print(f"\n  INTERPRETATION: {interp}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/r2_reverse_lookup.json")
json.dump({"summary":summary,"interpretation":interp,"rows":rows,"native_reverse_control":ctrl_native,
           "stimulus":{"fwd":FWD,"reverse":REV_T}}, open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("R2_DONE", flush=True)
