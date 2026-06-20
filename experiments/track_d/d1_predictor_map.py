import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""D1 Phase 1 — NO-EDIT predictor characterization (D1 covariate) + D7 basis-rotation test.
Pure compute_ks measurement (activations only; no edits, no cov, no dispatch).
Pre-reg: docs/D1_CAPACITY_LAW_PREREG.md §2 Phase 1.

From ONE compute_ks call per layer over the entity x relation grid we derive BOTH:
  A) D1 COVARIATE  — same-RELATION, cross-ENTITY key collinearity (mean pairwise cosine
     across entities sharing a relation) at band [4-8]. Should rank-order Phase-2
     per-relation interference slope (capital vs language vs continent).
  B) D7 TEST       — same-ENTITY, cross-RELATION key collinearity vs DEPTH. Hyp D7:
     inversely-U, HIGHER at [8-12] than [4-8] (basis rotates relation-clustered ->
     entity-clustered) -> explains the C2-band cross-up/within-down trade (CORPUS/21).
     If flat/lower at [8-12], the rotation EXPLANATION dies; the redistribution itself
     still stands (within-loc FALL + expr 100% already exclude under-editing).
"""
import os, sys, io, contextlib, json, hashlib
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="1"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import get_context_templates
from memit.compute_ks import compute_ks

# --- engine fingerprint (provenance; LAW#1) ---
ENG_SHA=hashlib.sha256(open(f"{ENGINE_ROOT}/memit/memit_main.py","rb").read()).hexdigest()
print(f"engine memit_main.py sha256={ENG_SHA}", flush=True)

ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
ctx=get_context_templates(model,tok)

# canonical templates (from experiments/scale/g6_scale_n.py)
TMPL={"capital":"The capital of {} is the city of",
      "language":"The official language of {} is",
      "continent":"{} is located on the continent of"}
RELS=["capital","language","continent"]

scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
ents=[e for e in scr if all(r in scr[e] and "truth" in scr[e][r] for r in RELS)][:24]
print(f"entities ({len(ents)}): {ents}", flush=True)

# layers: [4-8] band detail + [8-12] band detail + coarse depth sweep for the D7 curve
LAYERS=[2,4,5,6,7,8,9,10,11,12,14,16,18,20,22,24,28,32]

def grid_keys(layer):
    """ONE compute_ks over the full (entity x relation) grid -> [nents, nrel, d]."""
    reqs=[{"prompt":TMPL[r],"subject":e,"target_new":{"str":" X"}} for e in ents for r in RELS]
    with contextlib.redirect_stdout(io.StringIO()):
        K=compute_ks(model,tok,reqs,hp,layer,ctx).float()        # [n_ctx*nreq, d]
    nreq=len(reqs)
    K=K.view(-1,nreq,K.shape[-1]).mean(0)                          # [nreq, d] avg over contexts
    return K.view(len(ents),len(RELS),K.shape[-1])                 # [ent, rel, d]

def mean_pairwise_cos(K):                                          # K: [n, d]
    Kn=torch.nn.functional.normalize(K,dim=-1); C=Kn@Kn.T; n=C.shape[0]
    off=C[~torch.eye(n,dtype=torch.bool)]
    return float(off.mean()), float(off.std())

A={r:{} for r in RELS}    # D1 covariate: same-relation cross-entity, per layer
B={}                      # D7: same-entity cross-relation, per layer (mean over entities)
print("\nlayer | A: same-REL cross-ENT cos [capital|language|continent] | B: same-ENT cross-REL cos(mean±sd)", flush=True)
for L in LAYERS:
    G=grid_keys(L)                                                  # [ent, rel, d]
    # A: per relation, collinearity across entities
    arow={}
    for ri,r in enumerate(RELS):
        m,s=mean_pairwise_cos(G[:,ri,:]); A[r][L]=m; arow[r]=m
    # B: per entity, collinearity across its 3 relation-keys; average over entities
    bvals=[mean_pairwise_cos(G[ei,:,:])[0] for ei in range(len(ents))]
    bmean=float(torch.tensor(bvals).mean()); bsd=float(torch.tensor(bvals).std()); B[L]=bmean
    print(f"  L{L:2d} | {arow['capital']:.3f} | {arow['language']:.3f} | {arow['continent']:.3f}   | {bmean:.3f}±{bsd:.3f}", flush=True)

def band_mean(d,lo,hi):
    v=[d[L] for L in d if lo<=L<=hi]; return float(sum(v)/len(v)) if v else None

# --- A summary: D1 covariate ranking at band [4-8] ---
A_band48={r:band_mean(A[r],4,8) for r in RELS}
rank=sorted(RELS,key=lambda r:-A_band48[r])
print(f"\n[A / D1 COVARIATE] same-relation cross-entity collinearity @ band[4-8]: "
      + ", ".join(f"{r}={A_band48[r]:.3f}" for r in RELS), flush=True)
print(f"   -> predicted Phase-2 interference-slope ranking (steepest first): {rank}", flush=True)

# --- B summary: D7 verdict ---
B48=band_mean(B,4,8); B812=band_mean(B,8,12)
d7="HIGHER at [8-12] -> basis-rotation SUPPORTED (entity-clustering deepens)" if B812>B48+0.02 else \
   ("LOWER/FLAT at [8-12] -> basis-rotation explanation NOT supported (redistribution still stands)" if B812<B48-0.02 else "~EQUAL -> inconclusive")
print(f"\n[B / D7 TEST] same-entity cross-relation collinearity: band[4-8]={B48:.3f} vs band[8-12]={B812:.3f}  => {d7}", flush=True)

out={"experiment":"D1_phase1_predictor_map","engine_sha":ENG_SHA,"model":ID,"n_entities":len(ents),
     "entities":ents,"relations":RELS,"layers":LAYERS,
     "A_same_rel_cross_ent":A,"A_band_4_8":A_band48,"A_predicted_slope_rank":rank,
     "B_same_ent_cross_rel_depth":B,"B_band_4_8":B48,"B_band_8_12":B812,"D7_verdict":d7}
os.makedirs(f"{LLMDB_ROOT}/results",exist_ok=True)
json.dump(out,open(f"{LLMDB_ROOT}/results/d1_predictor_map_result.json","w"),indent=2)
print(f"\nwrote {LLMDB_ROOT}/results/d1_predictor_map_result.json\nD1_PHASE1_DONE", flush=True)
