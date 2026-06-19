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
# G6.1 — SCALE-OF-N many-overlay accumulation (the centerpiece falsifier).
# Extends the validated cell-B (n=2 sequential, 100% retention) to N=100 records
# across 50 entities x 2 fields, applied SEQUENTIALLY through in-solve AlphaEdit
# (cache_c accumulating, NEVER reset). Pre-registered in G6_G7_PASS_CRITERIA_DRAFT.md.
#
# Advisor-mandated design (folded in):
#  #1 SPLIT expressed_at_apply(i) [measured immediately after each edit] from
#     retained_at_rung(i) [measured at staircase checkpoints] — a low end-retention
#     is otherwise ambiguous (never-expressed vs clobbered-later).
#  #2 NULL_THRESH=0.005 (validated sweet spot; NOT the base script's 2e-2).
#  #3 entities pre-screened confident+correct (g6_screen) — no retrofit to hit N.
#  #4 THREE untouched signals: within-entity (continent of edited), cross-entity
#     (held-out entities = same-relation bleed), global (non-country = model damage).
#  #5 distinct-permutation single-token counterfacts; ONE write ordering (scope caveat).
# Engine UNMODIFIED. LAW#5 inertness gate runs first.
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
N_ENTITIES=int(os.environ.get("N_ENTITIES","50")); FIELDS=["capital","language"]
RUNG_ENTITIES=[int(x) for x in os.environ.get("RUNGS","13,25,50").split(",")]   # default -> 26/50/100 records
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES={  # non-country facts — sensitive to broad model damage, insensitive to capital/lang bleed
 "The largest planet in the solar system is":None,"Water is composed of hydrogen and":None,
 "The chemical symbol for gold is":None,"The opposite of hot is":None,
 "The first president of the United States was":None,"The speed of light is approximately":None}

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit in-solve thresh={NULL_THRESH} L2={L2}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1, truth):  # same prefix-match as g6_screen
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
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)  # CPU SVD: 18944-dim 7B cov OOMs on GPU beside the model
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]}", flush=True)
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
            Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()   # CPU solve (7B 18944-dim too big for GPU beside model)
            A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T
            upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL[a].format(e) for a in ["currency","continent","language"]]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} loc={eng_loc}% | harness-memit expr={my_p:.4f} loc={my_loc}% | |Δexpr|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- SMOKE: single alphaedit edit expression gate (B1 hard first gate) ----------
if os.environ.get("SMOKE"):
    print("\n=== SMOKE: single alphaedit edit (real edit path) expression gate ===", flush=True)
    Psm=compute_P(); csm=[torch.zeros(Psm[0].shape[0],Psm[0].shape[0]) for _ in L]
    e="France"; consm=TMPL["capital"].format(e); tgtm=first_tok("Cairo")
    probesm=[TMPL[a].format(e) for a in ["currency","continent","language"]]
    pre_s={p:predict(p) for p in [consm]+probesm}; s0m=snap()
    my_edit(req(e,"capital","Cairo"),"alphaedit",Psm,csm)
    post_s={p:predict(p) for p in [consm]+probesm}
    pe=float(post_s[consm]["dist"][tgtm]); top1=post_s[consm]["tok"]; loc=locpct(post_s,pre_s,probesm)
    restore(s0m)
    print(f"  alphaedit France->Cairo: post_p(Cairo)={pe:.4f} top1='{top1}' loc={loc}% -> {'EXPRESSES OK' if pe>0.5 else 'UNDER-EXPRESSED'}", flush=True)
    print("SMOKE_DONE", flush=True); sys.exit(0)

# ---------- build records from screened pool + distinct-permutation single-token counterfacts ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))); sel=scr["selected"]
ents=list(sel.keys()); edit_ents=ents[:N_ENTITIES]; heldout=ents[N_ENTITIES:N_ENTITIES+6]
def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]
    st=[t for t in truths if single_tok(t)]                 # single-token target pool
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf
CF={f:assign_cf(edit_ents,f) for f in FIELDS}
records=[]                                                   # write order: grouped by entity (cap then lang)
for e in edit_ents:
    for f in FIELDS:
        records.append({"entity":e,"field":f,"truth":sel[e][f]["truth"],"cf":CF[f][e],
                        "prompt":TMPL[f].format(e),"cf_tok":first_tok(CF[f][e])})
print(f"\n{len(records)} records | {len(edit_ents)} edited entities | {len(heldout)} held-out | rungs(records)={[r*len(FIELDS) for r in RUNG_ENTITIES]}", flush=True)

# untouched probe sets (pre-distributions)
unt_within=[TMPL["continent"].format(e) for e in edit_ents]                  # same-entity, never edited
# cross-entity (held-out): track BOTH JS drift AND top-1 (stability vs baseline + correctness vs truth),
# split by edited-relation (capital/language) vs unedited-relation (continent) — the verdict is a top-1 claim.
heldout_probes=[{"prompt":TMPL[f].format(e),"truth":sel[e][f]["truth"],"relation":f,"entity":e}
                for e in heldout for f in ["capital","language","continent"]]
unt_cross=[h["prompt"] for h in heldout_probes]
unt_global=list(GLOBAL_PROBES.keys())                                        # broad model damage
allprobe=unt_within+unt_cross+unt_global+[r["prompt"] for r in records]
pre={p:predict(p) for p in set(allprobe)}
def heldout_top1(post):  # top-1 stability (vs pre) + correctness (vs truth), grouped by relation class
    out={}
    for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"]),("all",["capital","language","continent"])]:
        sub=[h for h in heldout_probes if h["relation"] in rels]
        out[grp]={"top1_stable_vs_pre":round(100*sum(post[h["prompt"]]["id"]==pre[h["prompt"]]["id"] for h in sub)/len(sub),1),
                  "top1_correct_vs_truth":round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in sub)/len(sub),1)}
    return out
base_heldout={grp:{"top1_correct_vs_truth":round(100*sum(correct(pre[h["prompt"]]["tok"],h["truth"]) for h in heldout_probes if h["relation"] in rels)/len([h for h in heldout_probes if h["relation"] in rels]),1)}
              for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"]),("all",["capital","language","continent"])]}
print(f"  held-out PRE-EDIT top-1 correct: edited_rel={base_heldout['edited_rel']['top1_correct_vs_truth']}% continent={base_heldout['continent']['top1_correct_vs_truth']}%", flush=True)

# ---------- SCALE LOOP: sequential accumulation, cache_c never reset ----------
P=compute_P(); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
applied=[]; rung_records=[r*len(FIELDS) for r in RUNG_ENTITIES]; rungs=[]
WRITE_MODE=os.environ.get("WRITE_MODE","sequential")   # A1: 'sequential'(A0 baseline) | 'batch'(Genesis-style single joint solve)
if WRITE_MODE=="batch":
    print("\n=== BATCH WRITE (single joint solve over all records, Genesis-style) ===", flush=True)
    reqs=[req(r["entity"],r["field"],r["cf"])[0] for r in records]
    my_edit(reqs,"alphaedit",P,cache)
    for rec in records: rec["expressed_at_apply"]=bool(predict(rec["prompt"])["id"]==rec["cf_tok"])
    applied=list(records); n=len(records)
    ret=[bool(predict(r["prompt"])["id"]==r["cf_tok"]) for r in applied]
    post={p:predict(p) for p in set(unt_within+unt_cross+unt_global)}; ho=heldout_top1(post)
    rungs.append({"n":n,"all_record_retention":round(100*sum(ret)/n,2),
        "apply_time_expr":round(100*sum(a["expressed_at_apply"] for a in applied)/n,2),
        "unt_within_loc":locpct(post,pre,unt_within),"unt_cross_loc":locpct(post,pre,unt_cross),
        "unt_global_loc":locpct(post,pre,unt_global),"heldout_top1":ho})
    print(f"  >>> BATCH N={n}: retention={rungs[-1]['all_record_retention']}% apply-expr={rungs[-1]['apply_time_expr']}% | "
          f"held-out edited-rel TOP-1 correct={ho['edited_rel']['top1_correct_vs_truth']}% stable={ho['edited_rel']['top1_stable_vs_pre']}% "
          f"(vs A0 sequential 41.7%) | JS cross={rungs[-1]['unt_cross_loc']}% within={rungs[-1]['unt_within_loc']}% global={rungs[-1]['unt_global_loc']}%", flush=True)
if WRITE_MODE=="batch_staircase":
    # A1 follow-up: batch's OWN staircase — each rung is an INDEPENDENT joint solve
    # from the clean base over the first k entities, probing the SAME fixed held-out
    # set. Distinguishes "batch eliminates" (flat ~100) from "batch defers" (declines).
    print("\n=== BATCH STAIRCASE (independent joint solve per rung from clean base) ===", flush=True)
    s_clean=snap()
    for k in RUNG_ENTITIES:
        restore(s_clean); n=k*len(FIELDS); sub=records[:n]
        cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
        reqs=[req(r["entity"],r["field"],r["cf"])[0] for r in sub]
        my_edit(reqs,"alphaedit",P,cache)
        for rec in sub: rec["expressed_at_apply"]=bool(predict(rec["prompt"])["id"]==rec["cf_tok"])
        ret=[bool(predict(r["prompt"])["id"]==r["cf_tok"]) for r in sub]
        post={p:predict(p) for p in set(unt_within+unt_cross+unt_global)}; ho=heldout_top1(post)
        rungs.append({"n":n,"all_record_retention":round(100*sum(ret)/n,2),
            "apply_time_expr":round(100*sum(r["expressed_at_apply"] for r in sub)/n,2),
            "unt_within_loc":locpct(post,pre,unt_within),"unt_cross_loc":locpct(post,pre,unt_cross),
            "unt_global_loc":locpct(post,pre,unt_global),"heldout_top1":ho})
        print(f"  >>> BATCH-RUNG N={n}: retention={rungs[-1]['all_record_retention']}% apply-expr={rungs[-1]['apply_time_expr']}% | "
              f"held-out edited-rel TOP-1 correct={ho['edited_rel']['top1_correct_vs_truth']}% stable={ho['edited_rel']['top1_stable_vs_pre']}% | "
              f"continent correct={ho['continent']['top1_correct_vs_truth']}% | "
              f"JS cross={rungs[-1]['unt_cross_loc']}% within={rungs[-1]['unt_within_loc']}% global={rungs[-1]['unt_global_loc']}%", flush=True)

print("\n=== SCALE LOOP (in-solve AlphaEdit, cache_c accumulating) ===", flush=True)
for idx,rec in (enumerate(records) if WRITE_MODE not in ("batch","batch_staircase") else []):
    my_edit(req(rec["entity"],rec["field"],rec["cf"]),"alphaedit",P,cache)
    rec["expressed_at_apply"]=bool(predict(rec["prompt"])["id"]==rec["cf_tok"])   # #1 apply-time expression
    applied.append(rec); n=idx+1
    if n%10==0 or n in rung_records:
        exr=round(100*sum(a["expressed_at_apply"] for a in applied)/n,1)
        print(f"  applied {n}/{len(records)} | cum apply-time expr={exr}%", flush=True)
    if n in rung_records:
        ret=[bool(predict(a["prompt"])["id"]==a["cf_tok"]) for a in applied]     # retained_at_rung (re-probe ALL)
        post={p:predict(p) for p in set(unt_within+unt_cross+unt_global)}
        ho=heldout_top1(post)
        row={"n":n,"all_record_retention":round(100*sum(ret)/n,2),
             "apply_time_expr":round(100*sum(a["expressed_at_apply"] for a in applied)/n,2),
             "unt_within_loc":locpct(post,pre,unt_within),"unt_cross_loc":locpct(post,pre,unt_cross),
             "unt_global_loc":locpct(post,pre,unt_global),"heldout_top1":ho}
        rungs.append(row)
        print(f"  >>> RUNG N={n}: retention={row['all_record_retention']}% (apply-expr {row['apply_time_expr']}%) | "
              f"JS-loc within={row['unt_within_loc']}% cross={row['unt_cross_loc']}% global={row['unt_global_loc']}%", flush=True)
        print(f"      held-out TOP-1 edited_rel: stable={ho['edited_rel']['top1_stable_vs_pre']}% correct={ho['edited_rel']['top1_correct_vs_truth']}% | "
              f"continent: stable={ho['continent']['top1_stable_vs_pre']}% correct={ho['continent']['top1_correct_vs_truth']}%", flush=True)

# per-record final disposition (apply-time expr vs end retention) — the diagnostic split
final_ret={r["prompt"]:bool(predict(r["prompt"])["id"]==r["cf_tok"]) for r in records}
never_expressed=[f"{r['entity']}.{r['field']}" for r in records if not r["expressed_at_apply"]]
clobbered=[f"{r['entity']}.{r['field']}" for r in records if r["expressed_at_apply"] and not final_ret[r["prompt"]]]
out={"config":{"model":ID,"N":len(records),"entities":len(edit_ents),"fields":FIELDS,"null_thresh":NULL_THRESH,
      "L2":L2,"mom2_uw":hp.mom2_update_weight,"band":L,"write_mode":WRITE_MODE,"write_order":"grouped-by-entity (one ordering)"},
     "rungs":rungs,
     "heldout_baseline_top1_correct":base_heldout,
     "diagnostic":{"never_expressed_count":len(never_expressed),"never_expressed":never_expressed,
       "clobbered_after_expressing_count":len(clobbered),"clobbered":clobbered},
     "records":[{"entity":r["entity"],"field":r["field"],"truth":r["truth"],"cf":r["cf"],
                 "expressed_at_apply":r["expressed_at_apply"],"retained_at_end":final_ret[r["prompt"]]} for r in records]}
_TAG=os.environ.get("RESULT_TAG",""); _outpath=(f"{LLMDB_ROOT}/results/g6_scale_n_result{_TAG}.json" if WRITE_MODE=="sequential" else f"{LLMDB_ROOT}/results/g6_scale_n_{WRITE_MODE}_result{_TAG}.json")
json.dump(out,open(_outpath,"w"),indent=2,default=str)
print(f"\nFINAL N={len(records)}: retention={rungs[-1]['all_record_retention']}% | never-expressed={len(never_expressed)} | clobbered-after-expressing={len(clobbered)}", flush=True)
print(f"staircase retention: "+" -> ".join(f"N{r['n']}:{r['all_record_retention']}%" for r in rungs), flush=True)
print(f"wrote {_outpath}\nDONE", flush=True)
