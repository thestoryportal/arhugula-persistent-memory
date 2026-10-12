import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# B0 — SELECT-primitive go/no-go (Phase-1 critical-path step 1).
# Pre-reg: docs/B0_SELECT_PRIMITIVE_PREREG.md (frozen).
# Question: is there a weight-native read distinct from free-form INFER -- can the
# store return a value for COMMITTED keys AND abstain (null) for ABSENT keys, or do
# reads confabulate absent keys indistinguishably? INFER (greedy top-1) NEVER emits null.
# Reuses g6_scale_n_param.py primitives VERBATIM (proven inert). Engine UNMODIFIED.
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); L=hp.layers
NULL_THRESH=0.005; L2=1.0
TMPL={"capital":"The capital of {} is the city of","language":"The official language of {} is"}

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | AlphaEdit in-solve thresh={NULL_THRESH}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"maxprob":float(t.values[0])}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def locpct_dummy(): pass

def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); del cov,U,S; torch.cuda.empty_cache()
    return Ps

def my_edit(requests, mode, P=None, cache_c=None):
    """VERBATIM from g6_scale_n_param.py (proven inert)."""
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

def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- LAW#5 INERTNESS GATE (harness MEMIT-mode vs engine apply_memit) ----------
print("\n=== INERTNESS GATE (LAW#5) ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo")
pre_g=predict(cons); s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=float(torch.softmax(model(**tok(cons,return_tensors='pt').to('cuda')).logits[0,-1].float(),-1)[tgt]); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
my_p=float(torch.softmax(model(**tok(cons,return_tensors='pt').to('cuda')).logits[0,-1].float(),-1)[tgt]); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine expr={eng_p:.4f} | harness expr={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- B0 stimulus: fictional entities (base has no prior) + real single-token values ----------
# fictional country-like names; the (entity->value) ASSOCIATION is novel even though values are real cities/langs.
FICT=["Zelmara","Brovania","Quenland","Tavoria","Cassovia","Drennan","Yulvania","Sornia",
      "Plavia","Velloria","Othenia","Kuvalia","Nyssara","Granicia","Marnovia","Theldwin"]
# single-token value pools (filtered at runtime)
CAP_VALS=["Paris","London","Rome","Madrid","Berlin","Vienna","Cairo","Oslo","Lima","Tokyo","Athens","Dublin"]
LANG_VALS=["French","German","Spanish","Italian","Dutch","Polish","Greek","Danish","Swedish","Korean","Thai","Czech"]
cap_vals=[v for v in CAP_VALS if single_tok(v)]; lang_vals=[v for v in LANG_VALS if single_tok(v)]
print(f"  single-token value pools: caps={len(cap_vals)} langs={len(lang_vals)}", flush=True)

# COMMITTED: edit first 8 fictional entities, capital relation (clean single-relation go/no-go)
committed=[]
for i,ent in enumerate(FICT[:8]):
    val=cap_vals[i%len(cap_vals)]
    committed.append({"entity":ent,"attr":"capital","value":val,"prompt":TMPL["capital"].format(ent),"val_tok":first_tok(val)})
# ABSENT-fictional: fictional entities 8..16, NOT edited (pure absence)
absent_fict=[{"entity":ent,"attr":"capital","prompt":TMPL["capital"].format(ent)} for ent in FICT[8:16]]
# ABSENT-real: real countries, NOT edited (leak / open-world probe)
absent_real=[{"entity":c,"attr":"capital","prompt":TMPL["capital"].format(c),"truth":t}
             for c,t in [("France","Paris"),("Japan","Tokyo"),("Egypt","Cairo"),("Italy","Rome"),("Spain","Madrid"),("Norway","Oslo")]]

# pre-edit reads (baseline: what does the clean model say for each?)
pre_committed=[predict(r["prompt"]) for r in committed]
pre_absent_fict=[predict(r["prompt"]) for r in absent_fict]
pre_absent_real=[predict(r["prompt"]) for r in absent_real]

# ---------- COMMIT: batch single joint solve (clean Genesis path) ----------
print("\n=== COMMIT 8 fictional facts (batch single joint solve) ===", flush=True)
P=compute_P(); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([req(r["entity"],r["attr"],r["value"])[0] for r in committed],"alphaedit",P,cache)

# ---------- READ-BACK ----------
def read_set(rs): return [predict(r["prompt"]) for r in rs]
post_committed=read_set(committed); post_absent_fict=read_set(absent_fict); post_absent_real=read_set(absent_real)

# committed read-back: top-1 == committed value AND high confidence
for r,p in zip(committed,post_committed):
    r["readback_top1"]=p["tok"]; r["readback_maxprob"]=p["maxprob"]
    r["readback_correct"]=(p["id"]==r["val_tok"])
committed_correct=sum(r["readback_correct"] for r in committed)
committed_correct_hi=sum(r["readback_correct"] and r["readback_maxprob"]>=0.5 for r in committed)
comm_mp=[r["readback_maxprob"] for r in committed if r["readback_correct"]]   # maxprob of correctly-read committed
abs_mp=[p["maxprob"] for p in post_absent_fict]                              # maxprob of absent-fictional confab
real_mp=[p["maxprob"] for p in post_absent_real]
real_correct=sum(p["id"]==first_tok(r["truth"]) for p,r in zip(post_absent_real,absent_real))

# separation: best threshold tau classifying committed(correct) vs absent-fictional by maxprob
def best_tau(pos,neg):
    cand=sorted(set(pos+neg)); best=(0.0,0.0,0.0,0.0)
    for tau in cand+[c+1e-6 for c in cand]:
        tp=sum(x>=tau for x in pos)/max(1,len(pos)); tn=sum(x<tau for x in neg)/max(1,len(neg))
        if tp+tn>best[1]+best[2]: best=(tau,tp,tn,tp+tn)
    return {"tau":round(best[0],4),"committed_above":round(100*best[1],1),"absent_below":round(100*best[2],1)}
sep=best_tau(comm_mp,abs_mp) if comm_mp else {"tau":None,"committed_above":0,"absent_below":0}

import statistics as st
def stats(xs): return {"n":len(xs),"mean":round(st.mean(xs),4) if xs else None,"min":round(min(xs),4) if xs else None,"max":round(max(xs),4) if xs else None}
absent_fict_confab_hi=sum(p["maxprob"]>=0.5 for p in post_absent_fict)  # absent keys answered with high confidence

# ---------- VERDICT (pre-registered) ----------
N=len(committed)
committed_rate=100*committed_correct_hi/N
absent_confab_rate=100*absent_fict_confab_hi/len(absent_fict)
clean_sep = (sep["committed_above"]>=80 and sep["absent_below"]>=80)
if committed_rate>=80 and clean_sep:
    outcome="A_SELECT_PLAUSIBLE"
elif sep["committed_above"]>=50 and sep["absent_below"]>=50 and not clean_sep:
    outcome="C_MIXED_INCONCLUSIVE"
else:
    outcome="B_NO_WEIGHT_NATIVE_SELECT"

out={"prereg":"docs/B0_SELECT_PRIMITIVE_PREREG.md","model":ID,"band":L,"n_committed":N,
     "committed_readback_correct":committed_correct,"committed_readback_correct_hiconf":committed_correct_hi,
     "committed_readback_rate_pct":round(committed_rate,1),
     "absent_fictional_confab_hiconf":absent_fict_confab_hi,"absent_confab_rate_pct":round(absent_confab_rate,1),
     "absent_real_leak_correct":real_correct,"absent_real_n":len(absent_real),
     "maxprob_committed_correct":stats(comm_mp),"maxprob_absent_fictional":stats(abs_mp),"maxprob_absent_real":stats(real_mp),
     "separation_best_tau":sep,
     "OUTCOME":outcome,
     "committed_detail":[{"entity":r["entity"],"value":r["value"],"readback_top1":r["readback_top1"],
                          "maxprob":round(r["readback_maxprob"],4),"correct":r["readback_correct"]} for r in committed],
     "absent_fictional_detail":[{"entity":r["entity"],"top1":p["tok"],"maxprob":round(p["maxprob"],4)} for r,p in zip(absent_fict,post_absent_fict)],
     "absent_real_detail":[{"entity":r["entity"],"truth":r["truth"],"top1":p["tok"],"maxprob":round(p["maxprob"],4)} for r,p in zip(absent_real,post_absent_real)]}
json.dump(out,open(f"{LLMDB_ROOT}/results/b0_select_primitive_pilot.json","w"),indent=2,default=str)
print(f"\n=== B0 RESULT ===", flush=True)
print(f"  committed read-back (top-1 correct, hi-conf >=0.5): {committed_correct_hi}/{N} = {committed_rate:.0f}%  | maxprob {stats(comm_mp)}", flush=True)
print(f"  absent-fictional confabulation (top-1 maxprob>=0.5): {absent_fict_confab_hi}/{len(absent_fict)} = {absent_confab_rate:.0f}%  | maxprob {stats(abs_mp)}", flush=True)
print(f"  absent-REAL leak (un-edited, reads correct pretrained fact): {real_correct}/{len(absent_real)}  | maxprob {stats(real_mp)}", flush=True)
print(f"  separation best-tau: {sep}", flush=True)
print(f"  >>> OUTCOME = {outcome}", flush=True)
print("DONE", flush=True)
