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
# C10 — MULTI-TOKEN VALUE expression at the batch path (D-C10-1).
# Pre-reg: docs/C10_MULTI_TOKEN_VALUE_PREREG.md (frozen). FALSIFIER (can-fail).
# Co-sharpest write-side falsifier for the fixed target (local Intel CPU + batch writes).
# Within-relation single-vs-multi-token-VALUE contrast, SAME subjects, N<=100 batch path,
# isolating value-token-length from scale. NEW metric vs R13 = FULL-SEQUENCE expression.
# Engine UNMODIFIED; my_edit/primitives VERBATIM from r13 (proven inert); LAW#5 gate.
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); L=hp.layers
NULL_THRESH=0.005; L2=1.0
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | AlphaEdit thresh={NULL_THRESH} L2={L2}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,5)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])])}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def tgt_ids(s): return tok(" "+s,add_special_tokens=False)["input_ids"]
def ntok(s): return len(tgt_ids(s))
def single_tok(s): return ntok(s)==1

@torch.no_grad()
def full_seq_match(prompt, target_ids):
    """Greedy-decode len(target_ids) tokens; return (full_match, first_match, decoded_str)."""
    ids=tok(prompt,return_tensors="pt").to("cuda")["input_ids"]
    gen=[]
    cur=ids
    for _ in range(len(target_ids)):
        nt=int(model(cur).logits[0,-1].argmax())
        gen.append(nt); cur=torch.cat([cur,torch.tensor([[nt]],device="cuda")],dim=1)
    return (gen==list(target_ids), gen[0]==target_ids[0], tok.decode(gen).strip())

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
def my_edit(requests, P, cache_c):
    """VERBATIM AlphaEdit/MEMIT in-solve (engine primitives, proven inert). alphaedit mode."""
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[r["prompt"] for r in requests],
            words=[r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu()
        Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
        A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T
        upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

CANON="The capital of {} is the city of"
PARA=["{}'s capital city is called","The city that serves as the capital of {} is","If you visit {}, its capital city is"]
def reqc(country,cap): return [{"prompt":CANON,"subject":country,"target_new":{"str":" "+cap}}]

# ---------- INERTNESS GATE (LAW#5) — verbatim from r13 ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=CANON.format(e); tgt=first_tok("Cairo")
pre=predict(cons); s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,reqc(e,"Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=float(torch.softmax(model(**tok(cons,return_tensors="pt").to("cuda")).logits[0,-1].float(),-1)[tgt]); restore(s0)
Pg=compute_P(); cc=[torch.zeros(Pg[0].shape[0],Pg[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit(reqc(e,"Cairo"),Pg,cc)
my_p=float(torch.softmax(model(**tok(cons,return_tensors="pt").to("cuda")).logits[0,-1].float(),-1)[tgt]); restore(s0)
gate_ok=abs(eng_p-my_p)<0.05
print(f"  engine_p={eng_p:.4f} mine_p={my_p:.4f} |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if gate_ok else 'NOT INERT ✗ HALT'}", flush=True)
if not gate_ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- stimulus: SAME subjects, single-tok vs multi-tok counterfactual capitals ----------
scr=json.load(open(os.environ.get("SCREEN",f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json")))["selected"]
caps={c:scr[c]["capital"]["truth"] for c in scr}
single_caps=sorted({k for k in caps.values() if single_tok(k)})
multi_caps=sorted({k for k in caps.values() if ntok(k)>=2}, key=lambda k: ntok(k))
N=int(os.environ.get("N_EDIT","24"))
# subjects: confident pool order; need native capital to fire (screened below). Take first 2N candidates, keep N that pass native.
subj_cands=list(scr.keys())
def assign(subjects, pool, real):
    out={}
    for i,c in enumerate(subjects):
        rc=caps[c].lower(); j=(i*3+5)%len(pool)
        while pool[j].lower()==rc: j=(j+1)%len(pool)
        out[c]=pool[j]
    return out

# native screen: subject usable if canonical native capital is top-1 first-token
usable=[]
for c in subj_cands:
    if predict(CANON.format(c))["id"]==first_tok(caps[c]): usable.append(c)
    if len(usable)>=N: break
subjects=usable[:N]
X_single=assign(subjects, single_caps, caps)
X_multi =assign(subjects, multi_caps,  caps)
print(f"\nC10 | subjects(native-confident)={len(subjects)} | single_caps_pool={len(single_caps)} | multi_caps_pool={len(multi_caps)}", flush=True)
print(f"  multi targets token-lengths: {sorted(set(ntok(v) for v in X_multi.values()))}", flush=True)

def eval_arm(Xmap):
    rows=[]
    for c in subjects:
        tids=tgt_ids(Xmap[c])
        fm_c, ft_c, dec_c = full_seq_match(CANON.format(c), tids)             # canonical
        para=[full_seq_match(p.format(c), tids) for p in PARA]                # held-out paraphrases
        para_full=[x[0] for x in para]; para_first=[x[1] for x in para]
        rows.append({"subject":c,"X":Xmap[c],"ntok":len(tids),
                     "canon_full":fm_c,"canon_first":ft_c,"canon_decoded":dec_c,
                     "para_full_hits":para_full,"para_first_hits":para_first,
                     "para_full_rate":round(sum(para_full)/len(para),3),"para_first_rate":round(sum(para_first)/len(para),3)})
    n=len(rows)
    return {"rows":rows,
            "canon_first_top1":round(100*sum(r["canon_first"] for r in rows)/n,1),
            "canon_full_match":round(100*sum(r["canon_full"] for r in rows)/n,1),
            "para_first_top1":round(100*sum(sum(r["para_first_hits"]) for r in rows)/(n*len(PARA)),1),
            "para_full_match":round(100*sum(sum(r["para_full_hits"]) for r in rows)/(n*len(PARA)),1),
            "mean_ntok":round(sum(r["ntok"] for r in rows)/n,2)}

P=compute_P()
results={}
for arm,Xmap in [("SINGLE",X_single),("MULTI",X_multi)]:
    cache_c=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    print(f"\n=== ARM {arm}: batch genesis of {len(subjects)} edits (value ntok mean {round(sum(ntok(Xmap[c]) for c in subjects)/len(subjects),2)}) ===", flush=True)
    with contextlib.redirect_stdout(io.StringIO()): my_edit([{"prompt":CANON,"subject":c,"target_new":{"str":" "+Xmap[c]}} for c in subjects],P,cache_c)
    results[arm]=eval_arm(Xmap)
    restore(s0)
    r=results[arm]
    print(f"  canon first-token top1={r['canon_first_top1']}% | canon FULL-SEQ match={r['canon_full_match']}% | para full={r['para_full_match']}% (first={r['para_first_top1']}%)", flush=True)

S=results["SINGLE"]["canon_full_match"]; M=results["MULTI"]["canon_full_match"]; M1=results["MULTI"]["canon_first_top1"]
gap=round(S-M,1); within_arm_gap=round(M1-M,1)
if M>=85 and gap<=10: verdict="C10 SATISFIED-for-batch-path"
elif gap>15 and abs(M1-S)<=15: verdict="C10 FALSIFIER FIRES (multi-token-value expression FRAGILE: first-token lands, full value fails)"
else: verdict="AMBIGUOUS / CHARACTERIZATION"
summary={
 "harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/single-batch/capital/N<=100/1-seed/HF-fp16",
 "law5_gate":f"|Δ|={abs(eng_p-my_p):.4f} INERT",
 "N_per_arm":len(subjects),
 "SINGLE_canon_full_match":S,"MULTI_canon_full_match":M,"MULTI_canon_first_top1":M1,
 "S_minus_M_full":gap,"MULTI_within_arm_first_minus_full":within_arm_gap,
 "SINGLE_para_full":results["SINGLE"]["para_full_match"],"MULTI_para_full":results["MULTI"]["para_full_match"],
 "MULTI_mean_ntok":results["MULTI"]["mean_ntok"],
 "verdict":verdict}
print("\n=== C10 SUMMARY ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/c10_multitoken_value.json")
json.dump({"decision_id":"D-C10-1","class":"FALSIFIER (can-fail); target=local Intel CPU + batch writes; NOT promotable without advisor+cross-family",
           "summary":summary,"arms":{a:{k:v for k,v in results[a].items() if k!='rows'} for a in results},
           "detail":{a:results[a]["rows"] for a in results},
           "stimulus":{"CANON":CANON,"PARA":PARA,"subjects":subjects,"X_single":X_single,"X_multi":X_multi}},
          open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("C10_DONE", flush=True)
