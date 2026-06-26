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
# C10 Run 2 — NOVEL-insert multi-token VALUE robustness (D-C10-1, the BINDING test).
# Pre-reg: docs/C10_MULTI_TOKEN_VALUE_PREREG.md (frozen + 2026-06-25 addendum).
# Run 1 (counterfactual) floored both arms on the usable metric -> underpowered.
# Here: NOVEL fictional subjects (no pretrained competitor; R5-proven paraphrase-robust
# for single-token) -> single-vs-multi-token VALUE contrast, SAME subjects, OFF the floor.
# Binding metric = held-out-paraphrase FULL-SEQUENCE match. Fuller LAW#5 gate (p-delta + loc).
# Engine UNMODIFIED; my_edit/primitives VERBATIM from r5/r13 (proven inert).
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,5)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def tgt_ids(s): return tok(" "+s,add_special_tokens=False)["input_ids"]
def ntok(s): return len(tgt_ids(s))
def single_tok(s): return ntok(s)==1
def js(a,b):
    p=a.double(); q=b.double(); m=0.5*(p+q)
    def k(x,y): x=x.clamp_min(1e-12); y=y.clamp_min(1e-12); return float((x*(x.log()-y.log())).sum())
    return 0.5*k(p,m)+0.5*k(q,m)
def locpct(post,pre,pl): return round(100*sum(1-js(post[p]["dist"],pre[p]["dist"])/LN2 for p in pl)/len(pl),2)

@torch.no_grad()
def full_seq_match(prompt, target_ids):
    ids=tok(prompt,return_tensors="pt").to("cuda")["input_ids"]; gen=[]; cur=ids
    for _ in range(len(target_ids)):
        nt=int(model(cur).logits[0,-1].argmax()); gen.append(nt); cur=torch.cat([cur,torch.tensor([[nt]],device="cuda")],dim=1)
    return (gen==list(target_ids), gen[0]==target_ids[0])

def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False); idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, P, cache_c):
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,rq,hp,zl,ctx) for rq in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[rq["prompt"] for rq in requests],
            words=[rq["subject"] for rq in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu(); Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
        A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T; upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

CANON="The capital of {} is the city of"
PTEST=["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"]
def r(prompt,subj,targ): return {"prompt":prompt,"subject":subj,"target_new":{"str":" "+targ}}

# ---------- INERTNESS GATE (LAW#5: p-delta AND locality, restored from r13) ----------
print("\n=== INERTNESS GATE (p-delta + locality) ===", flush=True)
e="Zorbland"; cons=CANON.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is described as"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,[r(CANON,e,"Cairo")],hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
Pg=compute_P(); cc=[torch.zeros(Pg[0].shape[0],Pg[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit([r(CANON,e,"Cairo")],Pg,cc)
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
gate_ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  |Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} -> {'INERT ✓' if gate_ok else 'NOT INERT ✗ HALT'}", flush=True)
if not gate_ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- stimulus: NOVEL fictional subjects; single-tok vs multi-tok novel VALUES ----------
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
caps=sorted({scr[c]["capital"]["truth"] for c in scr})
single_v=[k for k in caps if single_tok(k)]; multi_v=sorted([k for k in caps if ntok(k)>=2], key=ntok)
FICTION=["Zorbland","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane","Mophgar","Brinduun",
         "Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin","Lurmaxen","Pradnoll","Kessivar","Wombryne","Halquin",
         "Vorlex","Quenby","Marsduq","Thelby"]
N=int(os.environ.get("N_EDIT","24")); FICTION=FICTION[:N]
def assign(subs, pool): return {c: pool[(i*3+5)%len(pool)] for i,c in enumerate(subs)}
Vsingle=assign(FICTION, single_v); Vmulti=assign(FICTION, multi_v)
# INCOHERENT multi-token values: two UNRELATED single-tokens concatenated -> first-token difficulty
# matches Vmulti, but the 2nd token gets NO bigram/prior help (the code/identifier-representative case).
def assign_incoh(subs, pool):
    out={}
    for i,c in enumerate(subs):
        a=pool[(i*2)%len(pool)]; b=pool[(i*2+1+ (i//len(pool)))%len(pool)]
        if a.lower()==b.lower(): b=pool[(i*2+3)%len(pool)]
        out[c]=f"{a} {b}"
    return out
Vincoh=assign_incoh(FICTION, single_v)
print(f"\nC10b NOVEL | subjects={len(FICTION)} | single_v_pool={len(single_v)} multi_v_pool={len(multi_v)} | multi ntoks={sorted(set(ntok(v) for v in Vmulti.values()))} | incoh ntoks={sorted(set(ntok(v) for v in Vincoh.values()))}", flush=True)
print(f"  incoh examples: {[Vincoh[c] for c in FICTION[:5]]}", flush=True)

# ---------- pre-edit base controls (fictional subj carries NO prior -> want ~0) ----------
def canon_full(c, val): return full_seq_match(CANON.format(c), tgt_ids(val))[0]
def para_full_rate(c, val):
    tids=tgt_ids(val); return sum(full_seq_match(p.format(c), tids)[0] for p in PTEST)
base_single=sum(canon_full(c,Vsingle[c]) for c in FICTION); base_multi=sum(canon_full(c,Vmulti[c]) for c in FICTION)
base_incoh=sum(canon_full(c,Vincoh[c]) for c in FICTION)
print(f"  pre-edit canonical base (want~0): single={base_single}/{N} multi={base_multi}/{N} incoh={base_incoh}/{N}", flush=True)
s_base=snap()

def run_arm(name, Vmap):
    restore(s_base); cache=[torch.zeros(Pg[0].shape[0],Pg[0].shape[0]) for _ in L]
    with contextlib.redirect_stdout(io.StringIO()): my_edit([r(CANON,c,Vmap[c]) for c in FICTION],Pg,cache)
    rows=[]
    for c in FICTION:
        tids=tgt_ids(Vmap[c]); cf,c1=full_seq_match(CANON.format(c),tids)
        para=[full_seq_match(p.format(c),tids) for p in PTEST]
        rows.append({"subj":c,"val":Vmap[c],"ntok":len(tids),"canon_full":cf,"canon_first":c1,
                     "para_full_hits":[x[0] for x in para],"para_first_hits":[x[1] for x in para]})
    restore(s_base); n=len(rows); npar=len(PTEST)
    out={"rows":rows,
         "canon_full":round(100*sum(x["canon_full"] for x in rows)/n,1),
         "canon_first":round(100*sum(x["canon_first"] for x in rows)/n,1),
         "para_full":round(100*sum(sum(x["para_full_hits"]) for x in rows)/(n*npar),1),
         "para_first":round(100*sum(sum(x["para_first_hits"]) for x in rows)/(n*npar),1),
         "para_any_full":round(100*sum(any(x["para_full_hits"]) for x in rows)/n,1),
         "mean_ntok":round(sum(x["ntok"] for x in rows)/n,2)}
    print(f"  >>> {name}: canon_full={out['canon_full']}% canon_first={out['canon_first']}% | PARA_full={out['para_full']}% para_first={out['para_first']}% any_full={out['para_any_full']}% (ntok {out['mean_ntok']})", flush=True)
    return out

print("\n=== ARMS (novel inserts, same subjects) ===", flush=True)
arms={"NOVEL_single":run_arm("NOVEL_single",Vsingle),
      "NOVEL_multi_coherent":run_arm("NOVEL_multi_coherent",Vmulti),
      "NOVEL_multi_incoherent":run_arm("NOVEL_multi_incoherent",Vincoh)}
Ns=arms["NOVEL_single"]["para_full"]; Nc=arms["NOVEL_multi_coherent"]["para_full"]; Ni=arms["NOVEL_multi_incoherent"]["para_full"]
Ni_first=arms["NOVEL_multi_incoherent"]["para_first"]
gap_inc=round(Ns-Ni,1)  # BINDING: single vs incoherent (code-representative)
# the direct "did the edit store the 2nd token?" signal = incoherent first-token vs full-seq gap
inc_cont_gap=round(Ni_first-Ni,1)
if Ns<60: verdict="INCONCLUSIVE — single-token novel insert below robustness floor; inspect"
elif Ni>=85 and gap_inc<=10: verdict="C10 SATISFIED-for-target (incoherent/code-like multi-token values robust: edit stores the full sequence, not just first-token+prior)"
elif gap_inc>15: verdict="C10 FALSIFIER FIRES (arbitrary/code-like multi-token values FRAGILE: prior-coherent values masked it; first-token lands, continuation fails)"
else: verdict="AMBIGUOUS / CHARACTERIZATION"
summary={"harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/single-batch/capital/NOVEL-insert/N<=100/1-seed/HF-fp16",
 "law5_gate":f"|Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} INERT",
 "N_per_arm":len(FICTION),"pre_edit_base":f"single {base_single}/{N}, coherent {base_multi}/{N}, incoherent {base_incoh}/{N}",
 "NOVEL_single_para_full":Ns,"NOVEL_multi_coherent_para_full":Nc,"NOVEL_multi_incoherent_para_full":Ni,
 "BINDING_single_minus_incoherent":gap_inc,
 "incoherent_first_minus_full(stored 2nd token?)":inc_cont_gap,
 "incoherent_para_first":Ni_first,"incoherent_mean_ntok":arms["NOVEL_multi_incoherent"]["mean_ntok"],
 "canon_full_all":{a:arms[a]["canon_full"] for a in arms},
 "binding_metric":"held-out-paraphrase FULL-SEQ on INCOHERENT (code-representative) values; coherent arm = prior-coherence positive control","verdict":verdict}
print("\n=== C10b SUMMARY (BINDING: paraphrase full-seq, novel regime) ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/c10b_novel_multitoken.json")
json.dump({"decision_id":"D-C10-1","run":"2_novel_insert (binding)","class":"FALSIFIER (can-fail); target=local Intel CPU + batch writes; NOT promotable without advisor+cross-family",
           "summary":summary,"arms":{a:{k:v for k,v in arms[a].items() if k!='rows'} for a in arms},
           "detail":{a:arms[a]["rows"] for a in arms},"stimulus":{"CANON":CANON,"PTEST":PTEST,"FICTION":FICTION,"Vsingle":Vsingle,"Vmulti":Vmulti}},
          open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("C10B_DONE", flush=True)
