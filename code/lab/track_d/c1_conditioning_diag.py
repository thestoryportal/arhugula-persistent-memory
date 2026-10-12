import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math, random, time
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF","expandable_segments:True")
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# C1 conditioning DIAGNOSTIC (advisor-directed) — locate the N-cliff + test the
# ridge fix. N=2000 single-solve collapsed (all "!" = ΔW blow-up). Suspect: fixed
# L2=1.0 ridge while Kg@Kg.T grows with N ([[wide-intermediate-7b-editing-vram]]).
# Ladder N over the SAME city pool; per N report edit-expr% + held-out retention +
# ΔW norm. RIDGE modes: 'fixed' (L2=1.0, current) vs 'scaled' (L2 grows with N).
# NOT a C1 corruption datapoint — a harness validation diagnostic.
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); L=hp.layers
NULL_THRESH=0.005; L2_BASE=1.0
LADDER=[int(x) for x in os.environ.get("LADDER","100,250,500,1000").split(",")]
RIDGE=os.environ.get("RIDGE","fixed")   # 'fixed' | 'scaled'
N_HELDOUT=200

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | LADDER={LADDER} RIDGE={RIDGE}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
@torch.no_grad()
def predict_batch(prompts, bs=256):
    tok.padding_side="left"; out=[]
    for s in range(0,len(prompts),bs):
        enc=tok(prompts[s:s+bs],return_tensors="pt",padding=True).to("cuda")
        lg=model(**enc).logits[:,-1,:].float(); v,i=torch.topk(torch.softmax(lg,-1),1,dim=-1)
        for k in range(len(prompts[s:s+bs])): out.append((int(i[k,0]),tok.decode([int(i[k,0])]),float(v[k,0])))
    return out
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

TMPL="The city of {} is located in the country of"
def my_edit(requests, P, cache_c, ridge):
    """AlphaEdit in-solve, single joint solve. ridge: 'fixed' L2_BASE | 'scaled' L2_BASE*N/100. Returns total ΔW norm."""
    ctx=get_context_templates(model,tok); zl=L[-1]; N=len(requests)
    lam = L2_BASE if ridge=="fixed" else L2_BASE*(N/100.0)
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters()); dwnorm=0.0
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[r["prompt"] for r in requests],
            words=[r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu()
        Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
        A=Pi@(Kg@Kg.T+ca)+lam*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T
        upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape); dwnorm+=float(upd.norm())
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
        del K,Kd,rd; torch.cuda.empty_cache()
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T; del K
    return round(dwnorm,2), round(lam,2)

def req(city,cf): return [{"prompt":TMPL,"subject":city,"target_new":{"str":" "+cf}}]

pool=json.load(open(f"{LLMDB_ROOT}/results/c1_scale_city_country_pool.json"))
SUBJ_MAXTOK=int(os.environ.get("SUBJ_MAXTOK","0"))  # 0=no filter; else keep cities whose subject tokenizes to <=this many tokens
if SUBJ_MAXTOK>0:
    pool=[r for r in pool if len(tok(" "+r["city"],add_special_tokens=False)["input_ids"])<=SUBJ_MAXTOK]
    print(f"  SUBJ_MAXTOK={SUBJ_MAXTOK} -> filtered pool to {len(pool)} clean-subject cities", flush=True)
random.Random(7).shuffle(pool)
countries=sorted({r["country"] for r in pool})
heldout=pool[max(LADDER):max(LADDER)+N_HELDOUT]  # disjoint from all edit sets
ho_prompts=[TMPL.format(r["city"]) for r in heldout]
pre=predict_batch(ho_prompts)
base_ho=round(100*sum(correct(p[1],r["country"]) for r,p in zip(heldout,pre))/len(heldout),1)
print(f"  held-out baseline={base_ho}% (n={len(heldout)})", flush=True)

P=compute_P(); s_clean=snap()
def cf_for(rows):
    for i,r in enumerate(rows):
        j=(i+13)%len(countries)
        while countries[j].lower()==r["country"].lower(): j=(j+1)%len(countries)
        r["cf"]=countries[j]
    return rows

results=[]
for N in LADDER:
    edit=cf_for([dict(x) for x in pool[:N]])
    restore(s_clean)
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    t0=time.time(); dwnorm,lam=my_edit([req(r["city"],r["cf"])[0] for r in edit],P,cache,RIDGE); secs=round(time.time()-t0,1)
    # expression (sample up to 200) + held-out retention
    samp=edit if len(edit)<=200 else [edit[i] for i in range(0,len(edit),max(1,len(edit)//200))]
    ep=predict_batch([TMPL.format(r["city"]) for r in samp])
    expr=round(100*sum(p[0]==first_tok(r["cf"]) for r,p in zip(samp,ep))/len(samp),1)
    hp_=predict_batch(ho_prompts)
    ho=round(100*sum(correct(p[1],r["country"]) for r,p in zip(heldout,hp_))/len(heldout),1)
    garbage=round(100*sum(p[1].strip() in ("!","") for p in hp_)/len(hp_),1)
    row={"N":N,"ridge":RIDGE,"lambda":lam,"dW_norm":dwnorm,"edit_expr_pct":expr,
         "heldout_post_pct":ho,"heldout_garbage_pct":garbage,"edit_secs":secs}
    results.append(row)
    print(f"  >>> N={N:5d} ridge={RIDGE}(λ={lam}) | ΔW_norm={dwnorm} | expr={expr}% | held-out={ho}% | garbage={garbage}% | {secs}s", flush=True)

out={"diagnostic":"C1 single-solve conditioning N-ladder","pool":"city->country","ridge_mode":RIDGE,
     "heldout_baseline_pct":base_ho,"ladder":results,
     "note":"NOT a C1 corruption datapoint; harness-validation diagnostic for the N-cliff + ridge fix."}
json.dump(out,open(f"{LLMDB_ROOT}/results/c1_conditioning_diag_{RIDGE}.json","w"),indent=2,default=str)
print(f"\nwrote results/c1_conditioning_diag_{RIDGE}.json\nLADDER expr%: "+" | ".join(f"N{r['N']}:{r['edit_expr_pct']}%(ho{r['heldout_post_pct']}%)" for r in results), flush=True)
print("DONE", flush=True)
