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
# D20 — Compaction SUB-BATCH GRANULARITY sweep (B3N condition 3, component 2).
# Pre-reg: docs/D20_COMPACTION_SUBBATCH_PREREG.md (advisor-checked).
# Fixed total N (=100 records, the A1 set), fixed-base P. Vary ONLY chunk size C:
# partition the N edits into ceil(N/C) consecutive chunks, each an independent
# joint AlphaEdit solve that ACCUMULATES on the running weights (cache_c carries).
#   C=N  -> single joint solve  == A1 (batch)      [HALT-gate: must reproduce clean]
#   C=1  -> fully sequential     == A0/G6.1         [HALT-gate: must reproduce corrupted]
# Measures the SAME fixed held-out sets after all chunks. >=2 held-out seeds.
# ENGINE UNMODIFIED. my_edit/compute_P copied VERBATIM from g6_scale_n_param.py
# (proven inert). LAW#5 inertness gate runs first; C=N is batch by construction.
# THIS RUN CAN FALSIFY condition 3 (chunking corrupts) but CANNOT confirm it
# (N held at known-clean 100 => isolates chunking, not scale). See pre-reg.
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
N_ENTITIES=int(os.environ.get("N_ENTITIES","50")); FIELDS=["capital","language"]
CHUNKS=[int(x) for x in os.environ.get("CHUNKS","100,50,25,10,5,1").split(",")]
HELDOUT_SEEDS=int(os.environ.get("HELDOUT_SEEDS","2")); HELDOUT_SZ=int(os.environ.get("HELDOUT_SZ","8"))
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES={
 "The largest planet in the solar system is":None,"Water is composed of hydrogen and":None,
 "The chemical symbol for gold is":None,"The opposite of hot is":None,
 "The first president of the United States was":None,"The speed of light is approximately":None}

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit in-solve thresh={NULL_THRESH} L2={L2} | CHUNKS={CHUNKS}", flush=True)
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

# ---------- build FIXED edited records + >=2 disjoint held-out seed-sets ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))); sel=scr["selected"]
ents=list(sel.keys()); edit_ents=ents[:N_ENTITIES]; pool=ents[N_ENTITIES:]
if len(pool) < HELDOUT_SEEDS*HELDOUT_SZ:
    print(f"  WARNING: held-out pool {len(pool)} < seeds*size {HELDOUT_SEEDS*HELDOUT_SZ}; overlapping/short sets", flush=True)
heldout_sets={f"hoseed{si}": pool[si*HELDOUT_SZ:(si+1)*HELDOUT_SZ] for si in range(HELDOUT_SEEDS)}
def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]
    st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf
CF={f:assign_cf(edit_ents,f) for f in FIELDS}
records=[]
for e in edit_ents:
    for f in FIELDS:
        records.append({"entity":e,"field":f,"truth":sel[e][f]["truth"],"cf":CF[f][e],
                        "prompt":TMPL[f].format(e),"cf_tok":first_tok(CF[f][e])})
N=len(records)
# ORDER_SEED: permute the edit ORDER (the binding nondeterminism axis, [[sequential-edit-run-nondeterminism]]).
# Default ""=grouped-by-entity (cap,lang adjacent). A seed => a different ordering for the 2nd-ordering replication
# the advisor mandated. Edited entities + held-out sets are UNCHANGED; only application order varies.
ORDER_SEED=os.environ.get("ORDER_SEED","")
if ORDER_SEED!="":
    random.Random(int(ORDER_SEED)).shuffle(records)
    print(f"  EDIT ORDER permuted with seed {ORDER_SEED} (2nd-ordering replication)", flush=True)
print(f"\n{N} FIXED edited records | {len(edit_ents)} edited entities | held-out seeds {list(heldout_sets)} (size {HELDOUT_SZ}) | order={'grouped' if ORDER_SEED=='' else f'shuffle{ORDER_SEED}'}", flush=True)

unt_within=[TMPL["continent"].format(e) for e in edit_ents]
# per-seed held-out probes: capital/language (edited relations) + continent (unedited control)
ho_probes={hs:[{"prompt":TMPL[f].format(e),"truth":sel[e][f]["truth"],"relation":f}
               for e in hoents for f in ["capital","language","continent"]] for hs,hoents in heldout_sets.items()}
unt_cross=sorted({h["prompt"] for hp_ in ho_probes.values() for h in hp_})
unt_global=list(GLOBAL_PROBES.keys())
allprobe=unt_within+unt_cross+unt_global+[r["prompt"] for r in records]
pre={p:predict(p) for p in set(allprobe)}
def heldout_top1(post, probes):
    out={}
    for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"])]:
        sub=[h for h in probes if h["relation"] in rels]
        out[grp]={"top1_stable_vs_pre":round(100*sum(post[h["prompt"]]["id"]==pre[h["prompt"]]["id"] for h in sub)/len(sub),1),
                  "top1_correct_vs_truth":round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in sub)/len(sub),1)}
    return out
base_ho={hs:heldout_top1(pre,probes) for hs,probes in ho_probes.items()}
for hs in heldout_sets:
    print(f"  {hs} PRE-EDIT held-out edited_rel top-1 correct={base_ho[hs]['edited_rel']['top1_correct_vs_truth']}%", flush=True)

# ---------- CHUNK-SIZE SWEEP (fixed total N, fixed-base P, accumulating cache_c) ----------
P=compute_P(); s_clean=snap()
reqs_all=[req(r["entity"],r["field"],r["cf"])[0] for r in records]
arms=[]
for C in CHUNKS:
    restore(s_clean)
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    nchunks=math.ceil(N/C)
    for start in range(0, N, C):
        my_edit(reqs_all[start:start+C], "alphaedit", P, cache)
    expr=[bool(predict(r["prompt"])["id"]==r["cf_tok"]) for r in records]
    ret=expr  # measured at end; expression==retention here (single end measurement)
    post={p:predict(p) for p in set(unt_within+unt_cross+unt_global)}
    ho={hs:heldout_top1(post,probes) for hs,probes in ho_probes.items()}
    ho_pooled_edited=round(sum(ho[hs]["edited_rel"]["top1_correct_vs_truth"] for hs in heldout_sets)/len(heldout_sets),1)
    arm={"chunk_size":C,"n_chunks":nchunks,"total_N":N,
         "edit_expression_pct":round(100*sum(expr)/N,1),
         "unt_within_loc":locpct(post,pre,unt_within),"unt_cross_loc":locpct(post,pre,unt_cross),
         "unt_global_loc":locpct(post,pre,unt_global),
         "heldout_edited_rel_correct_pooled":ho_pooled_edited,
         "heldout_by_seed":ho}
    arms.append(arm)
    tag = " [== A1 batch anchor]" if C==N else (" [== A0 sequential anchor]" if C==1 else "")
    print(f"  >>> C={C} ({nchunks} chunk(s)){tag}: edit-expr={arm['edit_expression_pct']}% | "
          f"held-out edited-rel TOP-1 correct (pooled {len(heldout_sets)} seeds)={ho_pooled_edited}% "
          f"[per-seed {[ho[hs]['edited_rel']['top1_correct_vs_truth'] for hs in heldout_sets]}] | "
          f"continent={[ho[hs]['continent']['top1_correct_vs_truth'] for hs in heldout_sets]} | "
          f"JS cross={arm['unt_cross_loc']}% within={arm['unt_within_loc']}% global={arm['unt_global_loc']}%", flush=True)

# ---------- anchor gates (LAW#3 known-baseline) ----------
armN=next(a for a in arms if a["chunk_size"]==N); arm1=next((a for a in arms if a["chunk_size"]==1),None)
gate_CN_clean = armN["heldout_edited_rel_correct_pooled"]>=85 and armN["edit_expression_pct"]>=95
gate_C1_corrupt = (arm1 is None) or (arm1["heldout_edited_rel_correct_pooled"] <= armN["heldout_edited_rel_correct_pooled"]-15)
anchors_ok = gate_CN_clean and gate_C1_corrupt
print(f"\nANCHOR GATES: C=N reproduces A1-clean (>=85% & expr>=95) = {gate_CN_clean} ({armN['heldout_edited_rel_correct_pooled']}%, expr {armN['edit_expression_pct']}%) | "
      f"C=1 reproduces A0-corrupt (>=15pp below C=N) = {gate_C1_corrupt}"
      + (f" ({arm1['heldout_edited_rel_correct_pooled']}%)" if arm1 else " (C=1 not in sweep)"), flush=True)
if not anchors_ok:
    print("⚠ ANCHOR GATE FAILED — endpoints did not reproduce A1/A0 → harness suspect → result NOT trustworthy (HALT per pre-reg LAW#3).", flush=True)

out={"experiment":"D20_subbatch_granularity","prereg":"docs/D20_COMPACTION_SUBBATCH_PREREG.md",
     "config":{"model":ID,"total_N":N,"chunks":CHUNKS,"band":L,"null_thresh":NULL_THRESH,"L2":L2,
       "P_handling":"fixed-base (computed once, held across chunks)","cache_c":"accumulating across chunks",
       "edit_order":("grouped-by-entity" if ORDER_SEED=="" else f"shuffle-seed-{ORDER_SEED}"),
       "heldout_seeds":list(heldout_sets),"heldout_size":HELDOUT_SZ,"write_order":("grouped-by-entity" if ORDER_SEED=="" else f"shuffle{ORDER_SEED}"),
       "bounding_claim":"can FALSIFY B3N condition 3 (chunking corrupts) but NOT confirm it (N held at known-clean 100; isolates chunking, not scale)"},
     "heldout_baseline_top1_correct":base_ho,
     "arms":arms,
     "anchor_gates":{"C_eq_N_reproduces_A1_clean":bool(gate_CN_clean),"C_eq_1_reproduces_A0_corrupt":bool(gate_C1_corrupt),"anchors_ok":bool(anchors_ok)}}
_TAG=os.environ.get("RESULT_TAG","")
_outpath=f"{LLMDB_ROOT}/results/d20_subbatch_sweep_result{_TAG}.json"
json.dump(out,open(_outpath,"w"),indent=2,default=str)
print(f"\nSWEEP (held-out edited-rel top-1 correct, pooled): "+" | ".join(f"C{a['chunk_size']}:{a['heldout_edited_rel_correct_pooled']}%" for a in arms), flush=True)
print(f"wrote {_outpath}\nDONE", flush=True)
