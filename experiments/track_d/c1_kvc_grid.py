import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math, random
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# C1-(a) — K-vs-C: compaction sub-batch CONFOUND BREAK (real country pool).
# Pre-reg: docs/C1_KVC_PREREG.md (advisor-endorsed; do NOT use a fictional substrate).
# Extends d20_subbatch_sweep.py — my_edit/compute_P/inertness gate copied VERBATIM
# (proven inert). ENGINE UNMODIFIED.
# 2D grid: vary total-N (edited entities {25,50} -> N records {50,100}) AND chunk
# size C INDEPENDENTLY, to separate chunk-SIZE / chunk-COUNT(n_chunks) / total-N
# (D20 fixed N=100 and could not). Native-knowledge validity: corruption is to
# held-out COUNTRY facts the model actually knows (the G6.1 bystander phenomenon).
# Multiple edit-ORDERINGS per cell = the cluster unit (held-out probes within one
# ordering are correlated sub-samples, NOT independent clusters). ~12 orderings on
# corrupting cells powers a 20pp effect at the measured ~30-35pp swing.
# MODEST scale (N<=100) by stimulus limit (78-entity pool); true-scale = C1 tier b.
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
FIELDS=["capital","language"]
EDIT_SIZES=[int(x) for x in os.environ.get("EDIT_SIZES","25,50").split(",")]   # edited ENTITIES per N-level
HELDOUT_SZ=int(os.environ.get("HELDOUT_SZ","28"))                              # held-out entities (== items/relation)
ORD_CORRUPT=int(os.environ.get("ORD_CORRUPT","12"))                           # orderings on corrupting cells (C<N)
ORD_CLEAN=int(os.environ.get("ORD_CLEAN","3"))                                # orderings on clean cells (C=N, stable)
# C-levels per N-level: the clean anchor C=N is added automatically.
C_LEVELS=[int(x) for x in os.environ.get("C_LEVELS","50,25,10").split(",")]
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES=["The largest planet in the solar system is","Water is composed of hydrogen and",
 "The chemical symbol for gold is","The opposite of hot is",
 "The first president of the United States was","The speed of light is approximately"]

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit thresh={NULL_THRESH} L2={L2} | EDIT_SIZES={EDIT_SIZES} C_LEVELS={C_LEVELS} HELDOUT={HELDOUT_SZ} ord(corrupt/clean)={ORD_CORRUPT}/{ORD_CLEAN}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"p":float(t.values[0]),"dist":pr.cpu()}
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
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]}", flush=True)
        del cov,U,S; torch.cuda.empty_cache()
    return Ps

def my_edit(requests, mode, P=None, cache_c=None):
    """reimplemented MEMIT/AlphaEdit solve (engine primitives). VERBATIM from g6_scale_n_param (proven inert)."""
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

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL[a].format(e) for a in ["currency","continent","language"]]
pre0={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre0,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre0,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} loc={eng_loc}% | harness-memit expr={my_p:.4f} loc={my_loc}% | |Δexpr|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- build NESTED edited sets + DISJOINT held-out set ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
ents=list(sel.keys())
MAXE=max(EDIT_SIZES)
if len(ents) < MAXE+HELDOUT_SZ:
    print(f"  WARNING: pool {len(ents)} < max-edit {MAXE} + held-out {HELDOUT_SZ}", flush=True)
edit_pool=ents[:MAXE]                       # nested: the 25-set is the first 25 of the 50-set
heldout=ents[MAXE:MAXE+HELDOUT_SZ]          # DISJOINT from all edited entities
print(f"  edit_pool={len(edit_pool)} (nested {EDIT_SIZES}) | held-out={len(heldout)} (disjoint) | total used={len(edit_pool)+len(heldout)}/{len(ents)}", flush=True)

def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]
    st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf
CF={f:assign_cf(edit_pool,f) for f in FIELDS}
def records_for(n_ent):
    recs=[]
    for e in edit_pool[:n_ent]:
        for f in FIELDS:
            recs.append({"entity":e,"field":f,"truth":sel[e][f]["truth"],"cf":CF[f][e],
                         "prompt":TMPL[f].format(e),"cf_tok":first_tok(CF[f][e])})
    return recs

# held-out bystander probes (capital/language on UNEDITED entities) + continent within-entity (on edited)
ho_bystander=[{"prompt":TMPL[f].format(e),"truth":sel[e][f]["truth"],"relation":f,"entity":e} for e in heldout for f in FIELDS]
within_continent=[{"prompt":TMPL["continent"].format(e),"truth":sel[e]["continent"]["truth"],"relation":"continent","entity":e} for e in edit_pool]
allprobe_static=[h["prompt"] for h in ho_bystander]+[h["prompt"] for h in within_continent]+GLOBAL_PROBES
pre={p:predict(p) for p in set(allprobe_static)}
base_ho=round(100*sum(correct(pre[h["prompt"]]["tok"],h["truth"]) for h in ho_bystander)/len(ho_bystander),1)
print(f"  PRE-EDIT held-out bystander top-1 correct={base_ho}% (n={len(ho_bystander)} probes, {HELDOUT_SZ} ents x {len(FIELDS)} rels)", flush=True)

# ---------- shared base ----------
P=compute_P(); s_clean=snap()

def eval_post(recs):
    """return edited-expr%, held-out bystander rows (per-probe correct/js), within-continent top-1, global loc."""
    expr=[bool(predict(r["prompt"])["id"]==r["cf_tok"]) for r in recs]
    post={p:predict(p) for p in set([h["prompt"] for h in ho_bystander]+[h["prompt"] for h in within_continent]+GLOBAL_PROBES)}
    ho_rows=[{"probe":f"{h['entity']}->{h['relation']}","relation":h["relation"],
              "correct":int(correct(post[h["prompt"]]["tok"],h["truth"])),
              "js_vs_pre":round(js(post[h["prompt"]]["dist"],pre[h["prompt"]]["dist"]),4)} for h in ho_bystander]
    ho_correct=round(100*sum(r["correct"] for r in ho_rows)/len(ho_rows),1)
    cont_correct=round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in within_continent)/len(within_continent),1)
    glob_loc=locpct(post,pre,GLOBAL_PROBES)
    return round(100*sum(expr)/len(expr),1), ho_correct, ho_rows, cont_correct, glob_loc

# ---------- 2D GRID over (N_ent, C) x orderings ----------
cells=[]; per_unit=[]
for n_ent in EDIT_SIZES:
    recs0=records_for(n_ent); N=len(recs0)
    c_set=sorted(set([N]+[c for c in C_LEVELS if c<N]), reverse=True)   # C=N (clean) + sub-batch sizes < N
    for C in c_set:
        is_clean=(C==N); n_ord=ORD_CLEAN if is_clean else ORD_CORRUPT; nchunks=math.ceil(N/C)
        cell_tag=f"N{N}_C{C}"
        ho_per_ord=[]; expr_per_ord=[]; cont_per_ord=[]; glob_per_ord=[]
        for k in range(n_ord):
            recs=list(recs0)
            if k>0: random.Random(1000+k).shuffle(recs)   # ordering seed; k=0 = grouped-by-entity
            restore(s_clean)
            cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
            reqs=[req(r["entity"],r["field"],r["cf"])[0] for r in recs]
            for start in range(0,N,C): my_edit(reqs[start:start+C],"alphaedit",P,cache)
            expr,ho_c,ho_rows,cont_c,glob=eval_post(recs)
            ho_per_ord.append(ho_c); expr_per_ord.append(expr); cont_per_ord.append(cont_c); glob_per_ord.append(glob)
            cl=f"{cell_tag}|order{k}"
            for r in ho_rows:
                per_unit.append({"cluster":cl,"order":k,"cell":cell_tag,"N":N,"C":C,"n_chunks":nchunks,
                                 "arm":cell_tag,"relation":r["relation"],"probe":r["probe"],
                                 "correct":r["correct"],"js_vs_pre":r["js_vs_pre"]})
        mean=lambda xs: round(sum(xs)/len(xs),1)
        cell={"cell":cell_tag,"N":N,"C":C,"n_chunks":nchunks,"is_clean":is_clean,"n_orderings":n_ord,
              "edit_expr_pct_mean":mean(expr_per_ord),"edit_expr_per_ord":expr_per_ord,
              "heldout_bystander_correct_mean":mean(ho_per_ord),"heldout_bystander_per_ord":ho_per_ord,
              "within_continent_correct_mean":mean(cont_per_ord),"global_loc_mean":mean(glob_per_ord)}
        cells.append(cell)
        print(f"  >>> {cell_tag} ({nchunks} chunk(s){' CLEAN-anchor' if is_clean else ''}) x{n_ord}ord: "
              f"expr={cell['edit_expr_pct_mean']}% | held-out bystander correct mean={cell['heldout_bystander_correct_mean']}% "
              f"per-ord={ho_per_ord} | continent={cell['within_continent_correct_mean']}% global={cell['global_loc_mean']}%", flush=True)

# ---------- anchor gates (LAW#3) ----------
clean_cells=[c for c in cells if c["is_clean"]]
anchors_ok=all(c["heldout_bystander_correct_mean"]>=85 and c["edit_expr_pct_mean"]>=95 for c in clean_cells)
print(f"\nANCHOR GATES (C=N reproduces A1-clean >=85% held-out & expr>=95%): {anchors_ok} "
      f"[{[(c['cell'],c['heldout_bystander_correct_mean'],c['edit_expr_pct_mean']) for c in clean_cells]}]", flush=True)
if not anchors_ok: print("⚠ ANCHOR GATE FAILED — endpoints did not reproduce A1-clean → harness suspect → NOT trustworthy (HALT per pre-reg LAW#3).", flush=True)

out={"experiment":"C1_KVC_grid","prereg":"docs/C1_KVC_PREREG.md","decision_id":"D-C1KVC-1",
     "config":{"model":ID,"band":L,"null_thresh":NULL_THRESH,"L2":L2,"fields":FIELDS,
       "edit_sizes_entities":EDIT_SIZES,"heldout_entities":HELDOUT_SZ,"c_levels":C_LEVELS,
       "orderings_corrupt":ORD_CORRUPT,"orderings_clean":ORD_CLEAN,
       "P_handling":"fixed-base (computed once, shared)","cache_c":"accumulating across chunks",
       "cluster_unit":"edit-ORDERING (held-out probes within an ordering are correlated sub-samples)",
       "bounding_claim":"breaks K-vs-C at MODEST scale (N<=100) with native-knowledge validity; does NOT test true-scale N->2000 (stimulus-gated, C1 tier b). CORE-retention proxy = edited-expr on <=100 records -> rule-of-three bounds CORE-failure <3%, NOT spec <1%."},
     "heldout_baseline_correct_pct":base_ho,
     "cells":cells,
     "anchor_gates":{"clean_cells_reproduce_A1":bool(anchors_ok),"clean_cells":[c["cell"] for c in clean_cells]},
     "per_unit":per_unit}
_TAG=os.environ.get("RESULT_TAG","")
_outpath=f"{LLMDB_ROOT}/results/c1_kvc_grid_result{_TAG}.json"
json.dump(out,open(_outpath,"w"),indent=2,default=str)
print(f"\nGRID (held-out bystander correct mean): "+" | ".join(f"{c['cell']}:{c['heldout_bystander_correct_mean']}%" for c in cells), flush=True)
print(f"wrote {_outpath}\nDONE", flush=True)
