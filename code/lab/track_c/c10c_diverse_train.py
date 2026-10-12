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
# C10c — DIAGNOSE the wall behind C10's incoherent-multi-token paraphrase failure
# (D-C10b-diverse). Pilot-before-the-pilot (advisor): incoherent canon_full=95.8%
# => continuation IS stored on the trained prompt; para_full=36.1% => the wall is
# prompt-GENERALIZATION, not missing-storage. Test: does paraphrase-DIVERSE training
# (CANON+PTRAIN, zero new method) lift held-out PTEST full-seq vs CANON-only?
#   lifts materially -> diverse training is the lever; AnyEdit (single-prompt) WRONG fix.
#   no lift -> storage genuinely missing under paraphrase -> AnyEdit port justified.
# Engine UNMODIFIED; primitives VERBATIM from c10b/r5; LAW#5 gate (p-delta+loc).
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1)
    return {"id":int(pr.argmax()),"dist":pr.cpu()}
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
PTRAIN=["{}'s capital is the city named","The capital city of {} is"]      # diverse TRAIN (disjoint from PTEST)
PTEST=["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"]  # held-out EVAL
def r(prompt,subj,targ): return {"prompt":prompt,"subject":subj,"target_new":{"str":" "+targ}}

# ---------- LAW#5 gate (p-delta + locality) ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="Zorbland"; cons=CANON.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is described as"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,[r(CANON,e,"Cairo")],hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
P=compute_P(); cc=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit([r(CANON,e,"Cairo")],P,cc)
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
gate_ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  |Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} -> {'INERT ✓' if gate_ok else 'HALT'}", flush=True)
if not gate_ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- stimulus: NOVEL subjects, INCOHERENT multi-token values (same construction as c10b) ----------
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
single_v=[k for k in sorted({scr[c]['capital']['truth'] for c in scr}) if single_tok(k)]
FICTION=["Zorbland","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane","Mophgar","Brinduun",
         "Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin","Lurmaxen","Pradnoll","Kessivar","Wombryne","Halquin",
         "Vorlex","Quenby","Marsduq","Thelby"]
N=int(os.environ.get("N_EDIT","24")); FICTION=FICTION[:N]
def assign_incoh(subs, pool):
    out={}
    for i,c in enumerate(subs):
        a=pool[(i*2)%len(pool)]; b=pool[(i*2+1+(i//len(pool)))%len(pool)]
        if a.lower()==b.lower(): b=pool[(i*2+3)%len(pool)]
        out[c]=f"{a} {b}"
    return out
Vincoh=assign_incoh(FICTION, single_v)
print(f"\nC10c | subjects={len(FICTION)} | incoh ntoks={sorted(set(ntok(v) for v in Vincoh.values()))} | ex {[Vincoh[c] for c in FICTION[:4]]}", flush=True)
base=sum(full_seq_match(CANON.format(c),tgt_ids(Vincoh[c]))[0] for c in FICTION)
print(f"  pre-edit canonical base (want~0): {base}/{N}", flush=True)
s_base=snap()

def run_arm(name, train_prompts):
    restore(s_base); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    reqs=[r(tp,c,Vincoh[c]) for c in FICTION for tp in train_prompts]
    with contextlib.redirect_stdout(io.StringIO()): my_edit(reqs,P,cache)
    rows=[]
    for c in FICTION:
        tids=tgt_ids(Vincoh[c]); cf,c1=full_seq_match(CANON.format(c),tids)
        ptest=[full_seq_match(p.format(c),tids) for p in PTEST]
        rows.append({"subj":c,"val":Vincoh[c],"ntok":len(tids),"canon_full":cf,
                     "ptest_full_hits":[x[0] for x in ptest],"ptest_first_hits":[x[1] for x in ptest]})
    restore(s_base); n=len(rows); npt=len(PTEST)
    out={"train_prompts":train_prompts,"canon_full":round(100*sum(x["canon_full"] for x in rows)/n,1),
         "ptest_full":round(100*sum(sum(x["ptest_full_hits"]) for x in rows)/(n*npt),1),
         "ptest_first":round(100*sum(sum(x["ptest_first_hits"]) for x in rows)/(n*npt),1),
         "ptest_any_full":round(100*sum(any(x["ptest_full_hits"]) for x in rows)/n,1),"rows":rows}
    print(f"  >>> {name} (train on {len(train_prompts)} prompt(s)): canon_full={out['canon_full']}% | PTEST_full={out['ptest_full']}% first={out['ptest_first']}% any={out['ptest_any_full']}%", flush=True)
    return out

print("\n=== ARMS (incoherent values; held-out PTEST eval) ===", flush=True)
arms={"CANON_only":run_arm("CANON_only",[CANON]),
      "CANON_plus_PTRAIN":run_arm("CANON_plus_PTRAIN",[CANON]+PTRAIN)}
base_pt=arms["CANON_only"]["ptest_full"]; div_pt=arms["CANON_plus_PTRAIN"]["ptest_full"]; lift=round(div_pt-base_pt,1)
if lift>=20: verdict=f"WALL = PROMPT-GENERALIZATION: diverse training LIFTS incoherent PTEST full {base_pt}->{div_pt}% (+{lift}pp) -> AnyEdit (single-prompt per-token) is the WRONG fix; diverse training is the lever. PORT AVOIDED."
elif lift<=8: verdict=f"NO LIFT ({base_pt}->{div_pt}%, +{lift}pp): diverse training does NOT rescue arbitrary multi-token continuation -> storage genuinely missing under paraphrase -> AnyEdit port JUSTIFIED (gate to operator as a scoped multi-run choice)."
else: verdict=f"PARTIAL lift (+{lift}pp): diverse training helps but doesn't clear it -> inspect; AnyEdit may still add value. CHARACTERIZATION."
summary={"harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/NOVEL-incoherent/N<=100/1-seed/HF-fp16",
 "law5_gate":f"|Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} INERT","N":len(FICTION),"pre_edit_base":f"{base}/{N}",
 "CANON_only_PTEST_full":base_pt,"CANON_plus_PTRAIN_PTEST_full":div_pt,"diversity_lift_pp":lift,
 "canon_full_both":{a:arms[a]["canon_full"] for a in arms},
 "CANON_only_PTEST_first":arms["CANON_only"]["ptest_first"],"diverse_PTEST_first":arms["CANON_plus_PTRAIN"]["ptest_first"],
 "verdict":verdict}
print("\n=== C10c SUMMARY (diagnose the wall) ===", flush=True)
for k,v in summary.items(): print(f"  {k}: {v}", flush=True)
OUT=f"{LLMDB_ROOT}/results/c10c_diverse_train.json"
json.dump({"decision_id":"D-C10b-diverse","summary":summary,"arms":{a:{k:v for k,v in arms[a].items() if k!='rows'} for a in arms},
           "detail":{a:arms[a]["rows"] for a in arms},"stimulus":{"CANON":CANON,"PTRAIN":PTRAIN,"PTEST":PTEST,"Vincoh":Vincoh}},
          open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("C10C_DONE", flush=True)
