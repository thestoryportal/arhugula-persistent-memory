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
# R9 — IN-WEIGHT DELETION RESIDUE (CP2 read-contract matrix row R9).
# Pre-reg: docs/R9_DELETION_RESIDUE_PREREG.md. LABEL PRE-COMMITTED: CHARACTERIZATION,
# NOT falsification (§11.2/D42: no class is weights-authoritative; no delete-time
# must-not-fire clause -> resurfacing CONFIRMS the overlay architecture, doesn't falsify).
# Q: does a CORRECTIVE in-weight delete (a NEW write-path edit toward the pre-write
#    top-1, NOT a snapshot revert) leave RESIDUE that resurfaces on a HELD-OUT paraphrase
#    neither write nor delete touched? Matched write/delete breadth (both canonical-only).
# Engine UNMODIFIED. my_edit/compute_P/predict/single_tok VERBATIM from g6_scale_n_param.py.
# LAW#5 gate first. Write batch (cache_c from 0) -> delete batch on HALF (accumulating).
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit thresh={NULL_THRESH} L2={L2}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

# ---------------- VERBATIM primitives ----------------
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
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, mode, P=None, cache_c=None):
    """reimplemented MEMIT/AlphaEdit solve (engine primitives). VERBATIM from s243h (proven inert)."""
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

TMPL_C={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
        "continent":"{} is located on the continent of","language":"The official language of {} is"}
def reqc(entity,attr,cf): return [{"prompt":TMPL_C[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL_C["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL_C[a].format(e) for a in ["currency","continent","language"]]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,reqc(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(reqc(e,"capital","Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} loc={eng_loc}% | harness expr={my_p:.4f} loc={my_loc}% | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ============================================================================
# R9 STIMULUS — fictional secrets, single-token CODE targets
# ============================================================================
ENTITIES=["Zorblax","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane",
          "Mophgar","Brinduun","Wexolite","Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin",
          "Lurmaxen","Pradnoll","Kessivar","Wombryne","Halquin","Drovspar","Naxulor","Tyrennos"]
CODEPOOL=["falcon","crimson","anchor","ember","silver","copper","thunder","willow","granite","saffron",
          "cobalt","maple","raven","amber","onyx","cedar","quartz","violet","harbor","walnut",
          "indigo","bronze","laurel","pewter"]
CODES=[c for c in CODEPOOL if single_tok(c)]
EDIT_PROMPT="The secret access code for {} is"                                   # canonical (write + delete both hit ONLY this)
HELDOUT=["Only insiders know that {}'s access code is","The confidential access code belonging to {} happens to be"]  # neither write nor delete touches these
N=int(os.environ.get("N_SECRETS","24")); ENTITIES=ENTITIES[:N]
secrets=[]
for i,ent in enumerate(ENTITIES):
    code=CODES[i%len(CODES)]
    secrets.append({"entity":ent,"code":code,"code_tok":first_tok(code),
                    "canon":EDIT_PROMPT.format(ent),"held":[h.format(ent) for h in HELDOUT]})
# DELETE group = even indices (12); CONTROL group = odd (12)
for i,s in enumerate(secrets): s["group"]="DELETE" if i%2==0 else "CONTROL"
print(f"\nR9 | {len(secrets)} fictional secrets | {sum(s['group']=='DELETE' for s in secrets)} DELETE / {sum(s['group']=='CONTROL' for s in secrets)} CONTROL | codes single-tok={len(CODES)}", flush=True)

def code_rank(prompt, code_tok):
    pr=predict(prompt); d=pr["dist"]; top1=(pr["id"]==code_tok)
    # rank of code token
    rank=int((d > d[code_tok]).sum())  # 0 = top-1
    return {"top1":bool(top1),"rank":rank,"p":round(float(d[code_tok]),4),"obs_top1":pr["tok"].strip(),"top5":pr["top5"]}

s_base=snap()
# ---- capture PRE-WRITE canonical top-1 (delete target) + base held-out ----
print("\n=== PRE-WRITE capture (delete targets + base headroom) ===", flush=True)
for s in secrets:
    pre=predict(s["canon"]); s["prewrite_top1"]=pre["tok"].strip() or "the"
    s["base_canon_codetop1"]=bool(pre["id"]==s["code_tok"])
base_leak=sum(s["base_canon_codetop1"] for s in secrets)
print(f"  base canonical code-as-top1 = {base_leak}/{len(secrets)} (want 0 — fictional headroom)", flush=True)

# ---- WRITE batch (canonical-only, single joint AlphaEdit, cache_c from 0) ----
print("\n=== WRITE: joint AlphaEdit batch (canonical-only) ===", flush=True)
P=compute_P(); cache_c=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
wreq=[{"prompt":EDIT_PROMPT,"subject":s["entity"],"target_new":{"str":" "+s["code"]}} for s in secrets]
my_edit(wreq,"alphaedit",P,cache_c)
# post-write probes
for s in secrets:
    s["w_canon"]=code_rank(s["canon"],s["code_tok"])
    s["w_held"]=[code_rank(h,s["code_tok"]) for h in s["held"]]
w_took=sum(s["w_canon"]["top1"] for s in secrets)
w_gen=sum(any(h["top1"] for h in s["w_held"]) for s in secrets)
print(f"  write canonical-took (top1) = {w_took}/{len(secrets)} | generalized to >=1 held-out paraphrase = {w_gen}/{len(secrets)}", flush=True)

# ---- DELETE batch (DELETE group only, canonical-only, accumulating) ----
print("\n=== DELETE: corrective AlphaEdit toward pre-write top-1 (DELETE group, canonical-only) ===", flush=True)
dreq=[{"prompt":EDIT_PROMPT,"subject":s["entity"],"target_new":{"str":" "+s["prewrite_top1"]}} for s in secrets if s["group"]=="DELETE"]
my_edit(dreq,"alphaedit",P,cache_c)
# post-delete probes (both groups)
for s in secrets:
    s["d_canon"]=code_rank(s["canon"],s["code_tok"])
    s["d_held"]=[code_rank(h,s["code_tok"]) for h in s["held"]]
restore(s_base)  # leave model clean

# ============================================================================
# ANALYSIS
# ============================================================================
DEL=[s for s in secrets if s["group"]=="DELETE"]
CON=[s for s in secrets if s["group"]=="CONTROL"]
# delete-took gate: canonical code no longer top1 post-delete
del_took=[s for s in DEL if not s["d_canon"]["top1"]]
# informative = wrote-took canonical AND generalized to >=1 held-out pre-delete AND delete-took
def gen_pre(s): return any(h["top1"] for h in s["w_held"])
informative=[s for s in del_took if s["w_canon"]["top1"] and gen_pre(s)]
# residue = among informative, code still top1 on the held-out paraphrase it generalized to, post-delete
def held_post_top1(s): return any(h["top1"] for h in s["d_held"])
residue=[s for s in informative if held_post_top1(s)]
# control group: undeleted secrets should STILL fire canonical + held-out (deletion specific)
con_canon_still=sum(s["d_canon"]["top1"] for s in CON)
con_held_still=sum(any(h["top1"] for h in s["d_held"]) for s in CON)
con_gen=sum(gen_pre(s) for s in CON)

summary={
 "harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/fixed-P/write-then-delete-accumulating","label":"CHARACTERIZATION (not falsification)",
 "n_secrets":len(secrets),"base_canon_code_top1":f"{base_leak}/{len(secrets)}",
 "write_canon_took":f"{w_took}/{len(secrets)}","write_generalized_heldout":f"{w_gen}/{len(secrets)}",
 "DELETE_group":len(DEL),"delete_took_canon":f"{len(del_took)}/{len(DEL)}",
 "informative_set":len(informative),
 "RESIDUE_rate":f"{len(residue)}/{len(informative)}" if informative else "n/a (no informative secrets)",
 "CONTROL_group":len(CON),"control_canon_still_fires":f"{con_canon_still}/{len(CON)}",
 "control_heldout_still_fires":f"{con_held_still}/{len(CON)}","control_generalized_pre":f"{con_gen}/{len(CON)}",
}
print("\n=== R9 SUMMARY (CHARACTERIZATION) ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
print("\n  --- residue examples (DELETE-group informative, code resurfaces on held-out) ---", flush=True)
for s in residue[:6]:
    print(f"   {s['entity']} code='{s['code']}': canon post-del top1='{s['d_canon']['obs_top1']}' (code gone) | held post-del top5={s['d_held'][0]['top5']}", flush=True)

OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/r9_deletion_residue.json")
json.dump({"summary":summary,"secrets":[{k:s[k] for k in s if k!="code_tok"} for s in secrets],
           "stimulus":{"edit_prompt":EDIT_PROMPT,"heldout":HELDOUT}}, open(OUT,"w"),indent=2)
print(f"\nwrote {OUT}", flush=True); print("R9_DONE", flush=True)
