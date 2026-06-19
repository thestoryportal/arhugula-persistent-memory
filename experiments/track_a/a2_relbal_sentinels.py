import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math, random
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# A2 — RELATION-BALANCED IN-SOLVE SENTINELS (Track A, the runtime-incremental fix).
# A1 showed BATCH (Genesis) is cross-entity clean; the SEQUENTIAL/runtime-incremental
# path is still corrupted (A0: held-out edited-rel top-1 collapses to ~33-42%).
# A2 asks: does adding held-out same-relation sentinel keys K_S to the preservation
# term INSIDE each sequential solve prevent cross-entity read corruption, while
# keeping write-side wins? "address = relation + ENTITY" (LARQL), D20 extension.
#
# THREE DISJOINT POOLS (anti-tautology, §2.3): edit(50) / sentinel(10, protected) /
# eval(10, measured, NEVER edited or protected). SEEDED SHUFFLE of the 78-entity v2
# screen so edit/sentinel/eval are drawn from one distribution (advisor: removes the
# append-order confound AND gives test power — eval must collapse at λ_s=0).
#
# Advisor-mandated framing (folded in):
#  - INERTNESS GATE = CODE-PATH IDENTITY: my_edit_sentinel(λ_s=0) must equal the
#    proven my_edit("alphaedit") on identical inputs (the λ_s·KsKsᵀ term vanishes).
#    NOT "reproduce A0's numbers" (impossible w/ new pools, and not the gate's job).
#  - VERDICT is vs the λ_s=0 control on the SAME pools, not vs A0.
#  - λ_s=0 run doubles as the false-no-op expression check on the NEW edit entities.
#  - PASS interpretation: corruption IS the shared relation direction & sentinels pin
#    it. FAIL: entity-specific components beyond it → basis change (A6), not more keys.
# Engine UNMODIFIED. Primitives copied verbatim from g6_scale_n.py (LAW#5-proven).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
SEED=int(os.environ.get("SEED","0"))
LAMBDAS=[float(x) for x in os.environ.get("LAMBDAS","0,0.5,1,2,5").split(",")]
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
print(f"loaded Qwen2.5-3B | band={L} mom2_uw={hp.mom2_update_weight} | AlphaEdit thresh={NULL_THRESH} L2={L2} | SEED={SEED} LAMBDAS={LAMBDAS}", flush=True)
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
    """proven-inert MEMIT/AlphaEdit solve (engine primitives). VERBATIM from g6_scale_n.py."""
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

# ---------- build pools FIRST (need sentinel entities for gate 2 Ks) ----------
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json")); sel=scr["selected"]
all_ents=list(sel.keys()); random.Random(SEED).shuffle(all_ents)
edit_ents=all_ents[:50]; sentinel_ents=all_ents[50:60]; eval_ents=all_ents[60:70]
assert not (set(edit_ents)&set(sentinel_ents)) and not (set(sentinel_ents)&set(eval_ents)) and not (set(edit_ents)&set(eval_ents)), "pools not disjoint"
from collections import Counter
def conts(pool): return dict(Counter(sel[e]["continent"]["truth"] for e in pool))
print(f"\n=== POOLS (seed={SEED}) ===", flush=True)
print(f"  EDIT(50): {edit_ents}", flush=True)
print(f"  SENTINEL(10): {sentinel_ents}  continents={conts(sentinel_ents)}", flush=True)
print(f"  EVAL(10): {eval_ents}  continents={conts(eval_ents)}", flush=True)
print(f"  edit continents={conts(edit_ents)}", flush=True)

P=compute_P()
def build_Ks(ents_pool):
    ctx=get_context_templates(model,tok)
    out=[]
    for i,layer in enumerate(L):
        reqs=[{"prompt":TMPL[f],"subject":e,"target_new":{"str":" x"}} for e in ents_pool for f in FIELDS]
        out.append(compute_ks(model,tok,reqs,hp,layer,ctx).T.float().cpu())  # [d_in, n_s]
    return out
Ks_sent=build_Ks(sentinel_ents)  # fixed sentinel keys from CLEAN base (preserve clean reads)

# ---------- INERTNESS GATE 2 (LAW#5): my_edit_sentinel(λ_s=0) == my_edit('alphaedit') ----------
print("\n=== INERTNESS GATE 2: my_edit_sentinel(λ_s=0) vs my_edit('alphaedit'), identical inputs ===", flush=True)
cacheA=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"alphaedit",P,cacheA)
a={p:predict(p) for p in [cons]+probes}; a_p=float(a[cons]["dist"][tgt]); a_loc=locpct(a,pre0,probes); restore(s0)
cacheB=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit_sentinel(req(e,"capital","Cairo"),P,cacheB,Ks_sent,0.0)
b={p:predict(p) for p in [cons]+probes}; b_p=float(b[cons]["dist"][tgt]); b_loc=locpct(b,pre0,probes); restore(s0)
ok2=abs(a_p-b_p)<1e-3 and abs(a_loc-b_loc)<0.5
print(f"  alphaedit expr={a_p:.5f} loc={a_loc}% | sentinel(λ=0) expr={b_p:.5f} loc={b_loc}% | |Δexpr|={abs(a_p-b_p):.6f} -> {'IDENTICAL ✓' if ok2 else 'NOT IDENTICAL ✗ HALT'}", flush=True)
if not ok2: print("LAW#5 gate-2 fail; HALT.", flush=True); sys.exit(0)

# ---------- build records (edit pool) + counterfacts (same scheme as g6_scale_n) ----------
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
print(f"\n{len(records)} records | {len(edit_ents)} edited | {len(sentinel_ents)} sentinel | {len(eval_ents)} eval", flush=True)

# ---------- probe sets ----------
unt_within=[TMPL["continent"].format(e) for e in edit_ents]                 # same-entity untouched
eval_probes=[{"prompt":TMPL[f].format(e),"truth":sel[e][f]["truth"],"relation":f,"entity":e}
             for e in eval_ents for f in ["capital","language","continent"]]  # 10x3 = 30 probes (finer than G6.1's 12)
unt_eval=[h["prompt"] for h in eval_probes]
unt_global=list(GLOBAL_PROBES.keys())
allprobe=unt_within+unt_eval+unt_global+[r["prompt"] for r in records]
pre={p:predict(p) for p in set(allprobe)}
def eval_top1(post):
    out={}
    for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"]),("all",["capital","language","continent"])]:
        sub=[h for h in eval_probes if h["relation"] in rels]
        out[grp]={"top1_stable_vs_pre":round(100*sum(post[h["prompt"]]["id"]==pre[h["prompt"]]["id"] for h in sub)/len(sub),1),
                  "top1_correct_vs_truth":round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in sub)/len(sub),1)}
    return out
base_eval={grp:{"top1_correct_vs_truth":round(100*sum(correct(pre[h["prompt"]]["tok"],h["truth"]) for h in eval_probes if h["relation"] in rels)/len([h for h in eval_probes if h["relation"] in rels]),1)}
           for grp,rels in [("edited_rel",["capital","language"]),("continent",["continent"]),("all",["capital","language","continent"])]}
print(f"  EVAL PRE-EDIT top-1 correct: edited_rel={base_eval['edited_rel']['top1_correct_vs_truth']}% continent={base_eval['continent']['top1_correct_vs_truth']}%", flush=True)

# ---------- LAMBDA SWEEP: each lambda = independent SEQUENTIAL staircase from clean base ----------
s_clean=snap(); rung_records=[r*len(FIELDS) for r in RUNG_ENTITIES]; sweep={}
for lam in LAMBDAS:
    restore(s_clean)
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    applied=[]; rungs=[]
    print(f"\n=== λ_s={lam} : sequential staircase (cache_c accumulating) ===", flush=True)
    for idx,rec in enumerate(records):
        my_edit_sentinel(req(rec["entity"],rec["field"],rec["cf"]),P,cache,Ks_sent,lam)
        rec["expressed_at_apply"]=bool(predict(rec["prompt"])["id"]==rec["cf_tok"])
        applied.append(rec); n=idx+1
        if n in rung_records:
            ret=[bool(predict(a["prompt"])["id"]==a["cf_tok"]) for a in applied]
            post={p:predict(p) for p in set(unt_within+unt_eval+unt_global)}; ev=eval_top1(post)
            row={"n":n,"all_record_retention":round(100*sum(ret)/n,2),
                 "apply_time_expr":round(100*sum(a["expressed_at_apply"] for a in applied)/n,2),
                 "unt_within_loc":locpct(post,pre,unt_within),"eval_loc":locpct(post,pre,unt_eval),
                 "unt_global_loc":locpct(post,pre,unt_global),"eval_top1":ev}
            rungs.append(row)
            print(f"  >>> λ={lam} N={n}: ret={row['all_record_retention']}% expr={row['apply_time_expr']}% | "
                  f"EVAL edited-rel top-1 correct={ev['edited_rel']['top1_correct_vs_truth']}% stable={ev['edited_rel']['top1_stable_vs_pre']}% | "
                  f"continent correct={ev['continent']['top1_correct_vs_truth']}% | JS eval={row['eval_loc']}% within={row['unt_within_loc']}% global={row['unt_global_loc']}%", flush=True)
    sweep[str(lam)]=rungs

restore(s_clean)
out={"config":{"model":ID,"seed":SEED,"lambdas":LAMBDAS,"N":len(records),"band":L,"mom2_uw":hp.mom2_update_weight,
      "null_thresh":NULL_THRESH,"L2":L2,"fields":FIELDS,"write_order":"grouped-by-entity (one ordering)",
      "pools":{"edit":edit_ents,"sentinel":sentinel_ents,"eval":eval_ents},
      "Ks_source":"clean-base, fixed (preserve clean sentinel reads)"},
     "eval_baseline_top1_correct":base_eval,
     "inertness":{"gate1_engine_vs_harness_memit":{"delta_expr":abs(eng_p-my_p)},
                  "gate2_sentinel_lam0_vs_alphaedit":{"delta_expr":abs(a_p-b_p),"delta_loc":abs(a_loc-b_loc)}},
     "sweep":sweep}
json.dump(out,open(f"{LLMDB_ROOT}/results/a2_relbal_sentinels_result.json","w"),indent=2,default=str)
print("\n=== SUMMARY: EVAL edited-rel top-1 correct @N=100 by λ_s ===", flush=True)
for lam in LAMBDAS:
    r=sweep[str(lam)][-1]
    print(f"  λ={lam}: eval-top1={r['eval_top1']['edited_rel']['top1_correct_vs_truth']}% (stable {r['eval_top1']['edited_rel']['top1_stable_vs_pre']}%) | retention={r['all_record_retention']}% expr={r['apply_time_expr']}%", flush=True)
print("wrote /workspace/results/a2_relbal_sentinels_result.json\nDONE", flush=True)
