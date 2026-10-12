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
# R5 — NATIVE-KNOWING PARAPHRASE-ROBUSTNESS: usable in-weight knowledge?
# Pre-reg: docs/R5_PARAPHRASE_ROBUSTNESS_PREREG.md. 4 arms, intensity-controlled.
# Does in-weight editing produce paraphrase-robust knowledge, or trained-prompt parrots?
# Isolates R13's competitor confound within ONE protocol + tests recipe-rescue.
# Metric = held-out P_test firing (DISJOINT from P_train). Engine UNMODIFIED. LAW#5 gate.
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
    # NOTE: cache_c not accumulated — each arm is an independent single batch from clean base.

CANON="The capital of {} is the city of"
PTRAIN=["{}'s capital is the city named","The capital city of {} is"]
PTEST=["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"]
def r(prompt,subj,targ): return {"prompt":prompt,"subject":subj,"target_new":{"str":" "+targ}}

# ---------- INERTNESS GATE ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=CANON.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is located on the continent of"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,[r(CANON,e,"Cairo")],hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); restore(s0)
P=None
def my_edit_memit_check():
    with contextlib.redirect_stdout(io.StringIO()):
        # memit-mode single edit for the inertness comparison
        my_edit([r(CANON,e,"Cairo")],"memit")
my_edit_memit_check()
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  |Δexpr|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- stimulus ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
realcands=[c for c in sel if single_tok(sel[c]["capital"]["truth"])]
realcaps=[sel[c]["capital"]["truth"] for c in realcands]
N=int(os.environ.get("N_PER_ARM","16"))
prior_countries=realcands[:N]
FICTION=["Zorbland","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane",
         "Mophgar","Brinduun","Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin","Lurmaxen",
         "Pradnoll","Kessivar","Wombryne","Halquin"][:N]
# counterfactual capital X for PRIOR (other country's real cap, != true); novel cap Y for NOVEL (real single-tok city)
def assign(cs, avoid_true):
    out={}
    for i,c in enumerate(cs):
        j=(i+5)%len(realcaps)
        if avoid_true:
            rc=sel[c]["capital"]["truth"]
            while realcaps[j].lower()==rc.lower(): j=(j+1)%len(realcaps)
        out[c]=realcaps[j]
    return out
Xprior=assign(prior_countries, True)
Ynovel=assign(FICTION, False)
print(f"\nR5 | N/arm={N} | prior_countries={len(prior_countries)} | fiction={len(FICTION)} | real-cap-cands={len(realcands)}", flush=True)

def fires(country, targ_tok):
    """P_test per-paraphrase top-1 hits + observed tokens."""
    hits=[]; obs=[]
    for t in PTEST:
        pr=predict(t.format(country)); hits.append(bool(pr["id"]==targ_tok)); obs.append(pr["tok"].strip())
    return hits, obs
def canon_took(country, targ_tok): pr=predict(CANON.format(country)); return bool(pr["id"]==targ_tok)

s_base=snap()

# ---- PRE-EDIT controls: NOVEL base, P_test target-base both arms, native P_test validity ----
print("\n=== PRE-EDIT controls ===", flush=True)
novel_base=sum(canon_took(c, first_tok(Ynovel[c])) for c in FICTION)  # want ~0
ptest_base_prior=sum(any(fires(c, first_tok(Xprior[c]))[0]) for c in prior_countries)  # target already wins? want ~0
ptest_base_novel=sum(any(fires(c, first_tok(Ynovel[c]))[0]) for c in FICTION)           # want ~0
# native validity: real countries fire on P_test for their TRUE capital
native_ptest=sum(any(fires(c, first_tok(sel[c]["capital"]["truth"]))[0]) for c in prior_countries)
print(f"  NOVEL canonical base (want~0): {novel_base}/{N}", flush=True)
print(f"  P_test target-base PRIOR (want~0): {ptest_base_prior}/{N} | NOVEL (want~0): {ptest_base_novel}/{N}", flush=True)
print(f"  native P_test validity (real->true cap any-paraphrase): {native_ptest}/{N}", flush=True)

# ---------- ARMS ----------
P=compute_P()
def run_arm(name, facts, capmap, train_prompts):
    """facts: list of subjects; capmap: subj->target; train_prompts: list of templates to train each fact on."""
    restore(s_base)
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    reqs=[]
    for c in facts:
        for tp in train_prompts:
            reqs.append(r(tp, c, capmap[c]))
    my_edit(reqs,"alphaedit",P,cache)
    rows=[]
    for c in facts:
        tt=first_tok(capmap[c]); l1=canon_took(c,tt); hits,obs=fires(c,tt)
        truecap=sel[c]["capital"]["truth"] if c in sel else None
        # mechanism (PRIOR only): among P_test failures, does output == true capital?
        revert=None
        if truecap is not None:
            tct=first_tok(truecap)
            revert=[ (not h) and (predict(PTEST[i].format(c))["id"]==tct) for i,h in enumerate(hits)]
        rows.append({"subj":c,"target":capmap[c],"L1_canon":l1,"ptest_hits":hits,"ptest_obs":obs,
                     "ptest_any":any(hits),"ptest_all":all(hits),"ptest_rate":round(sum(hits)/len(hits),3),
                     "true_cap":truecap,"revert_to_true":revert})
    restore(s_base)
    l1r=sum(x["L1_canon"] for x in rows)
    mean_rate=round(100*sum(x["ptest_rate"] for x in rows)/len(rows),1)
    anyr=sum(x["ptest_any"] for x in rows)
    perpara=[round(100*sum(x["ptest_hits"][i] for x in rows)/len(rows)) for i in range(len(PTEST))]
    rev=None
    if rows[0]["revert_to_true"] is not None:
        fails=sum(sum(1 for h in x["ptest_hits"] if not h) for x in rows)
        reverts=sum(sum(1 for v in x["revert_to_true"] if v) for x in rows)
        rev=f"{reverts}/{fails}" if fails else "n/a"
    summary={"arm":name,"n":len(rows),"L1_took":f"{l1r}/{len(rows)}","ptest_mean_rate":mean_rate,
             "ptest_any":f"{anyr}/{len(rows)}","ptest_per_paraphrase":perpara,"revert_to_true_among_fails":rev}
    print(f"  >>> {name}: L1-took {l1r}/{len(rows)} | P_test mean {mean_rate}% | any {anyr}/{len(rows)} | per-para {perpara}"
          + (f" | revert-to-true {rev}" if rev else ""), flush=True)
    return {"summary":summary,"rows":rows}

print("\n=== ARMS ===", flush=True)
arms={}
arms["NOVEL_single"]=run_arm("NOVEL_single",FICTION,Ynovel,[CANON])
arms["PRIOR_single"]=run_arm("PRIOR_single",prior_countries,Xprior,[CANON])
arms["PRIOR_multi_same"]=run_arm("PRIOR_multi_same",prior_countries,Xprior,[CANON,CANON,CANON])
arms["PRIOR_multi_para"]=run_arm("PRIOR_multi_para",prior_countries,Xprior,[CANON]+PTRAIN)

# ---------- SUMMARY ----------
print("\n=== R5 SUMMARY (P_test = held-out paraphrases, disjoint from P_train) ===", flush=True)
out={"experiment":"R5_paraphrase_robustness","label":"CHARACTERIZATION","prereg":"docs/R5_PARAPHRASE_ROBUSTNESS_PREREG.md",
     "controls":{"novel_canon_base":f"{novel_base}/{N}","ptest_target_base_prior":f"{ptest_base_prior}/{N}",
                 "ptest_target_base_novel":f"{ptest_base_novel}/{N}","native_ptest_validity":f"{native_ptest}/{N}"},
     "arms":{k:v["summary"] for k,v in arms.items()},
     "contrasts":{"competitor_NOVELsingle_vs_PRIORsingle":[arms["NOVEL_single"]["summary"]["ptest_mean_rate"],arms["PRIOR_single"]["summary"]["ptest_mean_rate"]],
                  "recipe_PRIORsingle_multisame_multipara":[arms["PRIOR_single"]["summary"]["ptest_mean_rate"],arms["PRIOR_multi_same"]["summary"]["ptest_mean_rate"],arms["PRIOR_multi_para"]["summary"]["ptest_mean_rate"]]},
     "templates":{"canonical":CANON,"P_train":PTRAIN,"P_test":PTEST},
     "rows":{k:v["rows"] for k,v in arms.items()}}
for k,v in out["arms"].items(): print(f"  {k}: P_test mean {v['ptest_mean_rate']}% (any {v['ptest_any']}, L1 {v['L1_took']})", flush=True)
print(f"  COMPETITOR: NOVEL-single {out['contrasts']['competitor_NOVELsingle_vs_PRIORsingle'][0]}% vs PRIOR-single {out['contrasts']['competitor_NOVELsingle_vs_PRIORsingle'][1]}%", flush=True)
print(f"  RECIPE (PRIOR single->multisame->multipara): {out['contrasts']['recipe_PRIORsingle_multisame_multipara']}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/r5_paraphrase_robustness.json")
json.dump(out,open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("R5_DONE", flush=True)
