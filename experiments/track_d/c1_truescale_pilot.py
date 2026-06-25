import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math, random, time
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF","expandable_segments:True")
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# C1 true-scale PILOT — single-joint-solve at N=2000 (the un-sub-batched path).
# Pre-reg: docs/C1_TRUESCALE_PILOT_PREREG.md (frozen). Engine UNMODIFIED.
# my_edit/compute_P/inertness copied VERBATIM from c1_kvc_grid.py (proven inert).
# Real native-known city->country pool (advisor: real-knowledge + single relation).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
N_EDIT=int(os.environ.get("N_EDIT","2000")); N_HELDOUT=int(os.environ.get("N_HELDOUT","600"))
TMPL="The city of {} is located in the country of"

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | N_EDIT={N_EDIT} N_HELDOUT={N_HELDOUT} | single joint solve", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"p":float(t.values[0]),"dist":pr.cpu()}
@torch.no_grad()
def predict_batch(prompts, bs=256):
    tok.padding_side="left"; out=[]
    for s in range(0,len(prompts),bs):
        enc=tok(prompts[s:s+bs],return_tensors="pt",padding=True).to("cuda")
        lg=model(**enc).logits[:,-1,:].float(); v,i=torch.topk(torch.softmax(lg,-1),1,dim=-1)
        for k in range(len(prompts[s:s+bs])): out.append((int(i[k,0]),tok.decode([int(i[k,0])]),float(v[k,0])))
    return out
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
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
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]}", flush=True)
        del cov,U,S; torch.cuda.empty_cache()
    return Ps

def my_edit(requests, mode, P=None, cache_c=None):
    """VERBATIM from c1_kvc_grid.py / g6_scale_n_param (proven inert)."""
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
        del K,Kd,rd; torch.cuda.empty_cache()
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T; del K

def req(city,cf): return [{"prompt":TMPL,"subject":city,"target_new":{"str":" "+cf}}]

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE (LAW#5) ===", flush=True)
cons=TMPL.format("Paris"); tgt=first_tok("Japan"); s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req("Paris","Japan"),hp,copy=False,return_orig_weights=False)
eng_p=float(predict(cons)["dist"][tgt]); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req("Paris","Japan"),"memit")
my_p=float(predict(cons)["dist"][tgt]); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine expr={eng_p:.4f} | harness expr={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- build edit set + disjoint held-out ----------
pool=json.load(open(f"{LLMDB_ROOT}/results/c1_scale_city_country_pool.json"))  # [{city,country,maxprob}]
random.Random(7).shuffle(pool)
edit=pool[:N_EDIT]; heldout=pool[N_EDIT:N_EDIT+N_HELDOUT]
countries=sorted({r["country"] for r in pool})
print(f"  edit={len(edit)} held-out={len(heldout)} (disjoint) | distinct countries={len(countries)}", flush=True)
# counterfactual: a single-token country != true (derangement-ish)
def assign_cf(rows):
    for i,r in enumerate(rows):
        j=(i+13)%len(countries)
        while countries[j].lower()==r["country"].lower(): j=(j+1)%len(countries)
        r["cf"]=countries[j]; r["cf_tok"]=first_tok(countries[j])
    return rows
edit=assign_cf(edit)

# pre-edit held-out baseline + CORE subset
ho_prompts=[TMPL.format(r["city"]) for r in heldout]
pre=predict_batch(ho_prompts)
for r,(pid,ptok,mp) in zip(heldout,pre):
    r["pre_top1"]=ptok.strip(); r["pre_correct"]=bool(correct(ptok,r["country"]))
base_ho=round(100*sum(r["pre_correct"] for r in heldout)/len(heldout),1)
core=[r for r in heldout if r["maxprob"]>=0.8 and r["pre_correct"]]
print(f"  PRE-EDIT held-out baseline top-1 correct={base_ho}% (n={len(heldout)}) | CORE subset (conf>=0.8 & pre-correct)={len(core)}", flush=True)

# ---------- single joint solve at N_EDIT (TIMED) ----------
P=compute_P(); s_clean=snap()
cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
reqs=[req(r["city"],r["cf"])[0] for r in edit]
print(f"\n=== EDIT: single joint solve, N={len(reqs)} (timing) ===", flush=True)
torch.cuda.synchronize(); t0=time.time()
my_edit(reqs,"alphaedit",P,cache)
torch.cuda.synchronize(); edit_secs=round(time.time()-t0,1)
vram_gb=round(torch.cuda.max_memory_allocated()/1e9,2)
print(f"  edit wall-clock={edit_secs}s | peak VRAM={vram_gb} GB", flush=True)

# ---------- evaluate ----------
# edit expression (top-1 == counterfactual) — sample up to 500 edits for speed
samp=edit if len(edit)<=500 else [edit[i] for i in range(0,len(edit),max(1,len(edit)//500))]
expr_preds=predict_batch([TMPL.format(r["city"]) for r in samp])
expr=round(100*sum(pid==r["cf_tok"] for r,(pid,_,_) in zip(samp,expr_preds))/len(samp),1)
# held-out retention (top-1 == true country)
post=predict_batch(ho_prompts)
for r,(pid,ptok,mp) in zip(heldout,post): r["post_top1"]=ptok.strip(); r["post_correct"]=bool(correct(ptok,r["country"]))
ho_post=round(100*sum(r["post_correct"] for r in heldout)/len(heldout),1)
# retention among facts that were correct PRE (the bystander degradation)
pre_ok=[r for r in heldout if r["pre_correct"]]
ho_retain=round(100*sum(r["post_correct"] for r in pre_ok)/len(pre_ok),1)
# CORE exact-1.0
core_post_ok=sum(r["post_correct"] for r in core)
core_exact=bool(core_post_ok==len(core))
# flips
flips=[{"city":r["city"],"true":r["country"],"pre":r["pre_top1"],"post":r["post_top1"]} for r in pre_ok if not r["post_correct"]]

out={"prereg":"docs/C1_TRUESCALE_PILOT_PREREG.md","model":ID,"band":L,"N_edit":len(edit),"N_heldout":len(heldout),
     "single_joint_solve":True,"orderings":1,
     "cost_anchor":{"edit_wall_clock_s":edit_secs,"peak_vram_gb":vram_gb},
     "edit_expression_pct":expr,
     "heldout_baseline_correct_pct":base_ho,"heldout_post_correct_pct":ho_post,
     "heldout_retention_pct_of_pre_correct":ho_retain,"n_pre_correct":len(pre_ok),
     "bystander_flips_n":len(flips),
     "CORE":{"n":len(core),"post_correct":core_post_ok,"exact_1.0":core_exact},
     "INERT_law5_delta":round(abs(eng_p-my_p),4),
     "flips_sample":flips[:30]}
json.dump(out,open(f"{LLMDB_ROOT}/results/c1_truescale_pilot.json","w"),indent=2,default=str)
print(f"\n=== C1 TRUE-SCALE PILOT RESULT (N={len(edit)} single joint solve) ===", flush=True)
print(f"  edit expression: {expr}%  (anchor: >=85 to be interpretable)", flush=True)
print(f"  held-out baseline -> post: {base_ho}% -> {ho_post}%  | retention of pre-correct: {ho_retain}% (flips={len(flips)}/{len(pre_ok)})", flush=True)
print(f"  CORE (conf>=0.8) exact-1.0: {core_post_ok}/{len(core)} -> {core_exact}", flush=True)
print(f"  COST ANCHOR: edit={edit_secs}s, peak VRAM={vram_gb} GB", flush=True)
print("DONE", flush=True)
