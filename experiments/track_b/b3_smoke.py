import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""30-sec smoke: does the fp16 GGUF reproduce HF predictions BEFORE the full probe?
Checks the edited France-capital fact (expect 'Cairo' per A1 batch) + one native fact."""
import sys, json, time, urllib.request
URL=sys.argv[1].rstrip("/")
def complete(p):
    body=json.dumps({"prompt":p,"n_predict":1,"temperature":0.0,"top_k":1,"cache_prompt":False}).encode()
    r=urllib.request.urlopen(urllib.request.Request(URL+"/completion",data=body,headers={"Content-Type":"application/json"}),timeout=60)
    return json.loads(r.read())["content"]
for _ in range(120):
    try: urllib.request.urlopen(URL+"/health",timeout=3); break
    except Exception: time.sleep(2)
probes=json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
ed=next((p for p in probes["edited"] if p["entity"]=="France" and p["field"]=="capital"), probes["edited"][0])
nat=next((p for p in probes["native"] if p["kind"]=="native_country"), None)
e_top=complete(ed["prompt"]); print(f"SMOKE edited  : '{ed['prompt']}' -> GGUF='{e_top.strip()}' | HF='{ed['hf_top1'].strip()}' | target(cf)='{ed['target']}'")
if nat: n_top=complete(nat["prompt"]); print(f"SMOKE native  : '{nat['prompt']}' -> GGUF='{n_top.strip()}' | HF='{nat['hf_top1'].strip()}' | truth='{nat['target']}'")
def m(a,b): a=(a or '').strip().lower(); b=(b or '').strip().lower(); return bool(a) and (a==b or a.startswith(b) or b.startswith(a))
ok=m(e_top,ed["hf_top1"])
print("SMOKE edited GGUF==HF:", ok, "(if False, conversion/template/BOS mismatch — STOP and inspect)")
