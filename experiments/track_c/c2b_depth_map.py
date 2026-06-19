import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""C2b: map SUBJECT-key same-relation collinearity across DEPTH.
Phase-0 found subject-key collinearity drops with depth in band [4-8] (0.68->0.26).
If deeper layers separate same-relation keys further, late-band editing (A4) could
reduce cross-entity bleed AND vindicate spec C15 (L15-25 vs our [4-8]).
Pure measurement (compute_ks = activations; no edits, no cov). Maps the best band
for cross-entity isolation. Tests both capital AND language relations.
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
ents=[e for e in scr.keys()][:12]
TMPL={"capital":"The capital of {} is the city of","language":"The official language of {} is"}

def keys(requests, layer):
    with contextlib.redirect_stdout(io.StringIO()):
        K=compute_ks(model,tok,requests,hp,layer,ctx).float()
    nreq=len(requests)
    return K.view(-1,nreq,K.shape[-1]).mean(0)   # [nreq, d]

def cos(K):
    Kn=torch.nn.functional.normalize(K,dim=-1); C=Kn@Kn.T; n=C.shape[0]
    return float(C[~torch.eye(n,dtype=torch.bool)].mean())

LAYERS=[2,4,6,8,10,12,14,16,18,20,22,24,28,32]
print(f"depth | capital-key cos | language-key cos   (subject keying; {len(ents)} entities)", flush=True)
res={}
for L in LAYERS:
    row={}
    for rel,t in TMPL.items():
        reqs=[{"prompt":t,"subject":e,"target_new":{"str":" X"}} for e in ents]
        row[rel]=cos(keys(reqs,L))
    res[L]=row
    print(f"  L{L:2d} | {row['capital']:.3f} | {row['language']:.3f}", flush=True)
json.dump(res,open(f"{LLMDB_ROOT}/results/c2b_depth_map_result.json","w"),indent=2)
best=min(LAYERS,key=lambda L:res[L]['capital'])
print(f"\nmin capital-key collinearity at L{best} (cos={res[best]['capital']:.3f})", flush=True)
print("If late layers (>=18) << early [4-8] => late-band editing is mechanistically motivated for cross-entity isolation (A4 + spec C15).", flush=True)
print("C2B_DONE", flush=True)
