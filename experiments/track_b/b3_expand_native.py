import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Expand the b3 NATIVE pool to clear the pre-registered n>=20 floor.
Reloads the SAVED edited model (b3_edited_qwen3b) and adds native facts from the
78-entity v2 screen UNION the 56-entity screen, EXCLUDING the 50 edited entities.
Keeps the existing 'edited' list; replaces 'native'. Native = facts of entirely
un-edited entities (pure quantization control, no edit interference)."""
import os, sys, json
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
SAVE_DIR=f"{LLMDB_ROOT}/b3_edited_qwen3b"
TMPL={"capital":"The capital of {} is the city of","continent":"{} is located on the continent of",
      "language":"The official language of {} is"}
GLOBAL_PROBES=["The largest planet in the solar system is","Water is composed of hydrogen and",
 "The chemical symbol for gold is","The opposite of hot is",
 "The first president of the United States was","The speed of light is approximately"]

tok=AutoTokenizer.from_pretrained(SAVE_DIR)
model=AutoModelForCausalLM.from_pretrained(SAVE_DIR, torch_dtype=torch.float16, device_map="cuda").eval()
@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); t=torch.topk(model(**ids).logits[0,-1].float(),1)
    return tok.decode([int(t.indices[0])])
def correct(top1,truth):
    if truth is None: return None
    a=(top1 or "").strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))

orig=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))["selected"]
v2  =json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
edited_50=list(orig.keys())[:50]                      # the entities A0/A1/B3-edit touched
# native entity pool: any screened entity NOT in the edited 50
pool={}
for src in (orig,v2):
    for e,fields in src.items():
        if e in edited_50: continue
        pool.setdefault(e,{}).update(fields)          # v2 overrides/extends orig
print(f"native entity pool (un-edited) = {len(pool)} entities; edited excluded = {len(edited_50)}", flush=True)

native=[]
for e,fields in pool.items():
    for f in ["capital","language","continent"]:
        if f in fields and "truth" in fields[f]:
            native.append({"prompt":TMPL[f].format(e),"target":fields[f]["truth"],"truth":fields[f]["truth"],
                           "entity":e,"field":f,"kind":"native_country"})
for gp in GLOBAL_PROBES:
    native.append({"prompt":gp,"target":None,"truth":None,"entity":None,"field":"global","kind":"native_global"})
# de-dup by prompt
seen=set(); native=[p for p in native if not (p["prompt"] in seen or seen.add(p["prompt"]))]

for pr in native:
    top=predict(pr["prompt"]); pr["hf_top1"]=top
    pr["hf_match_target"]=correct(top,pr["target"]) if pr["target"] is not None else None

nc=[p for p in native if p["kind"]=="native_country"]
nc_ok=sum(bool(p["hf_match_target"]) for p in nc)
print(f"native_country probes={len(nc)} | HF-fp16 correct={nc_ok} (eligible pool; need >=20)", flush=True)

probes=json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
probes["native"]=native
json.dump(probes, open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json","w"), indent=2, default=str)
print(f"rewrote b3_probes.json: edited={len(probes['edited'])} native={len(native)} (country={len(nc)}, global={len(GLOBAL_PROBES)})", flush=True)
print("DONE b3_expand_native", flush=True)
