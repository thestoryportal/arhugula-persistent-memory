import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math, random, time
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# A2b — REFRESH-K_S (Track A). Tests ONE variable vs A2: is the clean-base, FIXED
# sentinel-key tensor K_S going STALE as W drifts under 100 sequential edits, and
# is that staleness itself driving the N50->100 eval-read decline A2 could not arrest?
#
# A2 held K_S = clean-base, fixed (built once, reused in every solve). A2b adds a
# REFRESH arm that recomputes K_S against the CURRENT (drifted) W during the loop,
# and a FIXED control arm (= A2's behaviour) run in the SAME script / seed / lambda
# so the two arms differ ONLY in the refresh. Multi-seed because the eval metric is
# 20 probes (5%/item) and the decline is a few items -> single-seed cannot separate
# "staleness arrested it" from "different seed" (advisor).
#
# PRE-REGISTERED (advisor, before run):
#  - Metric: eval edited-rel top-1 correct@N=100 (10 eval ents x {capital,language}).
#  - Noise-aware threshold (anti-anchor, derived from the FIXED arm's own variance):
#    STALENESS-MATTERS iff  mean_seeds(REFRESH_N100 - FIXED_N100)  >  SD_seeds(FIXED_N100)
#    AND mechanistically consistent (K_S drift non-negligible).
#  - Mechanism logged for free: per-layer K_S drift (rel-Frobenius + mean column
#    cosine, clean-vs-current) at every rung, in BOTH arms.
#  - FORK: criterion met + decline arrested -> staleness was a real (free) limiter.
#          criterion NOT met + LARGE drift -> entity-specific residual -> A3 (BetaEdit) earned.
#          criterion NOT met + SMALL drift -> staleness ruled out -> A3 earned.
#
# FRAMING CAVEATS (write into result; advisor):
#  - A2b's positive ceiling is bounded BY CONSTRUCTION: K_S spans only SENTINEL
#    entities; it reaches eval reads solely via the shared relation direction.
#    Refreshing makes that shared direction CURRENT; it cannot add eval-entity-specific
#    coverage. A persistent decline despite fresh K_S is the EXPECTED clean A3 trigger.
#  - Refresh changes BOTH the direction AND the scale (norm) of the Ks@Ks.T term, so
#    "freshness" and "effective lambda_s per step" are conflated. Left combined; noted.
#  - Conclusion is conditional on isolation: only K_S varies; P (clean-base, AlphaEdit
#    design) and cache_c (accumulating edited keys, as A0/A2) are held.
# Engine UNMODIFIED. Primitives copied verbatim from a2_relbal_sentinels.py (LAW#5-proven).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
SEEDS=[int(x) for x in os.environ.get("SEEDS","0,1,2").split(",")]
LAMBDAS=[float(x) for x in os.environ.get("LAMBDAS","1,2").split(",")]
REFRESH_EVERY=int(os.environ.get("REFRESH_EVERY","1"))   # 1 = per-edit (max refresh)
RUNG_ENTITIES=[13,25,50]; FIELDS=["capital","language"]
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES={
 "The largest planet in the solar system is":None,"Water is composed of hydrogen and":None,
 "The chemical symbol for gold is":None,"The opposite of hot is":None,
 "The first president of the United States was":None,"The speed of light is approximately":None}

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded Qwen2.5-3B | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit thresh={NULL_THRESH} L2={L2} | SEEDS={SEEDS} LAMBDAS={LAMBDAS} REFRESH_EVERY={REFRESH_EVERY}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
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
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cuda().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]}", flush=True)
        del cov,U,S; torch.cuda.empty_cache()
    return Ps

def my_edit(requests, mode, P=None, cache_c=None):
    """proven-inert MEMIT/AlphaEdit solve (engine primitives). VERBATIM from a2_relbal_sentinels.py."""
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
            A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0],device="cuda"); B=Pi@Kg@rg.T
            upd=torch.linalg.solve(A,B).T.cpu()
            del Pi,ca,Kg,rg,A,B; torch.cuda.empty_cache()
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

def my_edit_sentinel(requests, P, cache_c, Ks_per_layer, lambda_s):
    """AlphaEdit solve + in-solve relation-balanced sentinel preservation term.
    IDENTICAL to my_edit(mode='alphaedit') except the LHS gains lambda_s*Ks@Ks.T.
    At lambda_s=0 the term is exactly zero -> code-path identity with my_edit('alphaedit')."""
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[r["prompt"] for r in requests],
            words=[r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu()
        Pi=P[i].cuda(); ca=cache_c[i].cuda(); Kg=Kd.float().cuda(); rg=rd.float().cuda()
        Ks=Ks_per_layer[i].cuda()
        A=Pi@(Kg@Kg.T+ca+lambda_s*(Ks@Ks.T))+L2*torch.eye(Kg.shape[0],device="cuda"); B=Pi@Kg@rg.T
        upd=torch.linalg.solve(A,B).T.cpu()
        del Pi,ca,Kg,rg,Ks,A,B; torch.cuda.empty_cache()
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    for i,layer in enumerate(L):  # accumulate EDITED keys into cache_c (as A0/alphaedit)
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

def build_Ks(ents_pool):
    ctx=get_context_templates(model,tok)
    out=[]
    for i,layer in enumerate(L):
        reqs=[{"prompt":TMPL[f],"subject":e,"target_new":{"str":" x"}} for e in ents_pool for f in FIELDS]
        out.append(compute_ks(model,tok,reqs,hp,layer,ctx).T.float().cpu())  # [d_in, n_s]
    return out

def ks_drift(Ks_cur, Ks_clean):
    """per-layer: relative Frobenius ||cur-clean||/||clean|| and mean per-column (per-key) cosine."""
    rels=[]; coss=[]
    for cur,cl in zip(Ks_cur, Ks_clean):
        rels.append(round(float((cur-cl).norm()/cl.norm().clamp_min(1e-12)),4))
        num=(cur*cl).sum(0); den=cur.norm(dim=0).clamp_min(1e-12)*cl.norm(dim=0).clamp_min(1e-12)
        coss.append(round(float((num/den).mean()),4))
    return {"rel_fro_per_layer":rels,"mean_col_cos_per_layer":coss,
            "rel_fro_mean":round(sum(rels)/len(rels),4),"mean_col_cos_mean":round(sum(coss)/len(coss),4)}

# ---------- INERTNESS GATE 1 (LAW#5): engine apply_memit vs harness my_edit('memit') ----------
print("\n=== INERTNESS GATE 1: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL[a].format(e) for a in ["currency","continent","language"]]
pre0={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre0,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre0,probes); restore(s0)
ok1=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} loc={eng_loc}% | harness-memit expr={my_p:.4f} loc={my_loc}% | |Δexpr|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok1 else 'NOT INERT ✗ HALT'}", flush=True)
if not ok1: print("LAW#5 gate-1 fail; HALT.", flush=True); sys.exit(0)

# ---------- screen + P (seed-independent) ----------
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json")); sel=scr["selected"]
from collections import Counter
P=compute_P()

def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]
    st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf

# ---------- INERTNESS GATE 2 (LAW#5): my_edit_sentinel(λ_s=0) == my_edit('alphaedit'), seed-0 pool ----------
print("\n=== INERTNESS GATE 2: my_edit_sentinel(λ_s=0) vs my_edit('alphaedit'), identical inputs ===", flush=True)
ae0=list(sel.keys()); random.Random(0).shuffle(ae0); sent0=ae0[50:60]
Ks0=build_Ks(sent0)
cacheA=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"alphaedit",P,cacheA)
a={p:predict(p) for p in [cons]+probes}; a_p=float(a[cons]["dist"][tgt]); a_loc=locpct(a,pre0,probes); restore(s0)
cacheB=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit_sentinel(req(e,"capital","Cairo"),P,cacheB,Ks0,0.0)
b={p:predict(p) for p in [cons]+probes}; b_p=float(b[cons]["dist"][tgt]); b_loc=locpct(b,pre0,probes); restore(s0)
ok2=abs(a_p-b_p)<1e-3 and abs(a_loc-b_loc)<0.5
print(f"  alphaedit expr={a_p:.5f} loc={a_loc}% | sentinel(λ=0) expr={b_p:.5f} loc={b_loc}% | |Δexpr|={abs(a_p-b_p):.6f} -> {'IDENTICAL ✓' if ok2 else 'NOT IDENTICAL ✗ HALT'}", flush=True)
if not ok2: print("LAW#5 gate-2 fail; HALT.", flush=True); sys.exit(0)

s_clean=snap(); rung_records=[r*len(FIELDS) for r in RUNG_ENTITIES]
def run_staircase(records, Ks_clean, sentinel_ents, eval_probes, pre, lam, refresh):
    """one sequential staircase. refresh=False -> FIXED clean-base K_S (=A2). True -> recompute every REFRESH_EVERY edits."""
    restore(s_clean)
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    Ks_use=[k.clone() for k in Ks_clean]; applied=[]; rungs=[]
    unt_within=[TMPL["continent"].format(r) for r in {x["entity"] for x in records}]
    unt_eval=[h["prompt"] for h in eval_probes]; unt_global=list(GLOBAL_PROBES.keys())
    def eval_top1(post):
        out={}
        for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"]),("all",["capital","language","continent"])]:
            sub=[h for h in eval_probes if h["relation"] in rels]
            out[grp]={"top1_stable_vs_pre":round(100*sum(post[h["prompt"]]["id"]==pre[h["prompt"]]["id"] for h in sub)/len(sub),1),
                      "top1_correct_vs_truth":round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in sub)/len(sub),1)}
        return out
    for idx,rec in enumerate(records):
        if refresh and (idx % REFRESH_EVERY == 0) and idx>0:
            t0=time.time(); Ks_use=build_Ks(sentinel_ents)
            if idx==REFRESH_EVERY: print(f"      [timing] in-loop build_Ks = {time.time()-t0:.2f}s", flush=True)
        my_edit_sentinel(req(rec["entity"],rec["field"],rec["cf"]),P,cache,Ks_use,lam)
        rec["expressed_at_apply"]=bool(predict(rec["prompt"])["id"]==rec["cf_tok"]); applied.append(rec); n=idx+1
        if n in rung_records:
            ret=[bool(predict(a["prompt"])["id"]==a["cf_tok"]) for a in applied]
            post={p:predict(p) for p in set(unt_within+unt_eval+unt_global)}; ev=eval_top1(post)
            drift=ks_drift(build_Ks(sentinel_ents), Ks_clean)   # current-vs-clean, both arms
            row={"n":n,"all_record_retention":round(100*sum(ret)/n,2),
                 "apply_time_expr":round(100*sum(a["expressed_at_apply"] for a in applied)/n,2),
                 "unt_within_loc":locpct(post,pre,unt_within),"eval_loc":locpct(post,pre,unt_eval),
                 "unt_global_loc":locpct(post,pre,unt_global),"eval_top1":ev,"ks_drift":drift}
            rungs.append(row)
            print(f"    [{'REFRESH' if refresh else 'FIXED  '}] λ={lam} N={n}: ret={row['all_record_retention']}% expr={row['apply_time_expr']}% | "
                  f"EVAL edited-rel top-1 correct={ev['edited_rel']['top1_correct_vs_truth']}% stable={ev['edited_rel']['top1_stable_vs_pre']}% | "
                  f"Ksdrift fro={drift['rel_fro_mean']} cos={drift['mean_col_cos_mean']} | JS eval={row['eval_loc']}%", flush=True)
    return rungs

results={}
for seed in SEEDS:
    all_ents=list(sel.keys()); random.Random(seed).shuffle(all_ents)
    edit_ents=all_ents[:50]; sentinel_ents=all_ents[50:60]; eval_ents=all_ents[60:70]
    assert not (set(edit_ents)&set(sentinel_ents)) and not (set(sentinel_ents)&set(eval_ents)) and not (set(edit_ents)&set(eval_ents))
    CF={f:assign_cf(edit_ents,f) for f in FIELDS}
    records=[{"entity":e,"field":f,"truth":sel[e][f]["truth"],"cf":CF[f][e],
              "prompt":TMPL[f].format(e),"cf_tok":first_tok(CF[f][e])} for e in edit_ents for f in FIELDS]
    eval_probes=[{"prompt":TMPL[f].format(e),"truth":sel[e][f]["truth"],"relation":f,"entity":e}
                 for e in eval_ents for f in ["capital","language","continent"]]
    unt_within=[TMPL["continent"].format(e) for e in edit_ents]
    allprobe=unt_within+[h["prompt"] for h in eval_probes]+list(GLOBAL_PROBES.keys())+[r["prompt"] for r in records]
    pre={p:predict(p) for p in set(allprobe)}
    Ks_clean=build_Ks(sentinel_ents)
    base=round(100*sum(correct(pre[h["prompt"]]["tok"],h["truth"]) for h in eval_probes if h["relation"] in ["capital","language"])/
               len([h for h in eval_probes if h["relation"] in ["capital","language"]]),1)
    print(f"\n========== SEED {seed} | eval edited-rel PRE-EDIT top-1 correct={base}% ==========", flush=True)
    results[str(seed)]={"eval_base_top1":base,"arms":{}}
    for lam in LAMBDAS:
        for refresh in [False, True]:
            key=f"lam{lam}_{'refresh' if refresh else 'fixed'}"
            rungs=run_staircase([dict(r) for r in records], Ks_clean, sentinel_ents, eval_probes, pre, lam, refresh)
            results[str(seed)]["arms"][key]=rungs

restore(s_clean)
# ---------- pre-registered noise-aware verdict ----------
def n100(seed,lam,arm): return results[str(seed)]["arms"][f"lam{lam}_{arm}"][-1]["eval_top1"]["edited_rel"]["top1_correct_vs_truth"]
verdict={}
print("\n=== A2b VERDICT (noise-aware: STALENESS-MATTERS iff mean(refresh-fixed)@N100 > SD(fixed)@N100) ===", flush=True)
for lam in LAMBDAS:
    fixed=[n100(s,lam,"fixed") for s in SEEDS]; refr=[n100(s,lam,"refresh") for s in SEEDS]
    mf=sum(fixed)/len(fixed); mr=sum(refr)/len(refr)
    sd=(sum((x-mf)**2 for x in fixed)/len(fixed))**0.5
    delta=mr-mf; matters=bool(delta>sd and delta>0)
    drift_mean=sum(results[str(s)]["arms"][f"lam{lam}_refresh"][-1]["ks_drift"]["rel_fro_mean"] for s in SEEDS)/len(SEEDS)
    verdict[str(lam)]={"fixed_n100":fixed,"refresh_n100":refr,"mean_fixed":round(mf,2),"mean_refresh":round(mr,2),
                       "sd_fixed":round(sd,2),"delta":round(delta,2),"ks_drift_fro_mean_n100":round(drift_mean,4),
                       "staleness_matters":matters}
    print(f"  λ={lam}: fixed@N100={fixed} (mean {mf:.1f}, SD {sd:.2f}) | refresh@N100={refr} (mean {mr:.1f}) | "
          f"Δ={delta:+.1f} vs SD {sd:.2f} -> STALENESS {'MATTERS' if matters else 'RULED-OUT-or-INSUFFICIENT'} | Ksdrift_fro@N100={drift_mean:.3f}", flush=True)

out={"config":{"model":ID,"seeds":SEEDS,"lambdas":LAMBDAS,"refresh_every":REFRESH_EVERY,"N":len(records),"band":L,
      "mom2_uw":hp.mom2_update_weight,"null_thresh":NULL_THRESH,"L2":L2,"fields":FIELDS,
      "rung_records":rung_records,"isolation":"only K_S varies; P clean-base, cache_c accumulating (held)",
      "ceiling_caveat":"K_S spans SENTINEL entities only; reaches eval reads solely via shared relation direction; refresh makes that current but cannot add eval-entity-specific coverage",
      "scale_caveat":"refresh changes direction AND norm of Ks@Ks.T; freshness and effective lambda_s/step conflated"},
     "inertness":{"gate1_engine_vs_harness_memit":{"delta_expr":abs(eng_p-my_p)},
                  "gate2_sentinel_lam0_vs_alphaedit":{"delta_expr":abs(a_p-b_p),"delta_loc":abs(a_loc-b_loc)}},
     "verdict":verdict,"results":results}
json.dump(out,open(f"{LLMDB_ROOT}/results/a2b_refresh_ks_result.json","w"),indent=2,default=str)
print("\nwrote /workspace/results/a2b_refresh_ks_result.json\nDONE", flush=True)
