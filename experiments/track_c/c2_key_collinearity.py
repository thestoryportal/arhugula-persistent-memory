import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""C2 phase-0: mechanism probe for relation-inclusive keying.
G6.1 cross-entity bleed (same-relation, cross-entity) is driven by collinear KEYS:
the down_proj-input activations of capital(France), capital(Italy)... overlap, so a
rank-1 edit at one bleeds to others. Hypothesis (corpus workaround b): keying at a
RELATION-INCLUSIVE position separates them.
COUNTER-hypothesis: keying at the 'capital' token may make same-relation keys MORE
collinear (shared relation component dominates). This probe decides it BEFORE a full run.

Measures mean pairwise cosine of compute_ks keys across same-relation entities, under:
  (a) SUBJECT keying   : subject=ENTITY,            prompt='The capital of {} is the city of'  (key @ entity token)
  (b) RELATION keying  : subject="ENTITY's capital", prompt='{} is'                              (key @ 'capital' token)
Lower pairwise cosine in (b) => keys separate => C2 worth a full sequential run.
"""
import os, sys, io, contextlib, json
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="1"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import get_context_templates
from memit.compute_ks import compute_ks

ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
ctx=get_context_templates(model,tok)

scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))["selected"]
ents=[e for e in scr.keys()][:12]   # 12 same-relation (capital) entities
print(f"entities ({len(ents)}): {ents}", flush=True)

def keys_for(requests, layer):
    with contextlib.redirect_stdout(io.StringIO()):
        K=compute_ks(model,tok,requests,hp,layer,ctx)   # [n_ctx*n_req, d] -> we get keys
    return K.float()

def mean_pairwise_cos(K):
    Kn=torch.nn.functional.normalize(K, dim=-1)
    C=Kn@Kn.T
    n=C.shape[0]; off=C[~torch.eye(n,dtype=torch.bool)]
    return float(off.mean()), float(off.std())

# build requests for both keyings
subj_reqs=[{"prompt":"The capital of {} is the city of","subject":e,"target_new":{"str":" X"}} for e in ents]
rel_reqs =[{"prompt":"{} is","subject":f"{e}'s capital","target_new":{"str":" X"}} for e in ents]

print("\nlayer | SUBJECT-key cos(mean±sd) | RELATION-key cos(mean±sd) | separates?", flush=True)
for layer in hp.layers:
    Ks=keys_for(subj_reqs,layer); Kr=keys_for(rel_reqs,layer)
    # compute_ks returns keys per (context x request); average over contexts to get one key per entity
    nreq=len(ents)
    Ks=Ks.view(-1,nreq,Ks.shape[-1]).mean(0); Kr=Kr.view(-1,nreq,Kr.shape[-1]).mean(0)
    ms,ss=mean_pairwise_cos(Ks); mr,sr=mean_pairwise_cos(Kr)
    sep="YES (rel<subj)" if mr<ms-0.02 else ("no (rel>=subj)" if mr>ms+0.02 else "~same")
    print(f"  L{layer} | {ms:.3f}±{ss:.3f} | {mr:.3f}±{sr:.3f} | {sep}", flush=True)
print("\nC2_PHASE0_DONE", flush=True)
print("Interpretation: relation keying REDUCES same-relation key collinearity => full sequential C2 worth running;", flush=True)
print("                if it INCREASES/equals => keying won't fix cross-entity bleed (hypothesis pruned cheaply).", flush=True)
