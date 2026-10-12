import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Probe ONE running llama-server over the b3 probe set; greedy top-1 next token.
Usage: python b3_probe.py <server_url> <out_pred_json>"""
import sys, json, time, urllib.request
URL=sys.argv[1].rstrip("/"); OUT=sys.argv[2]
probes=json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
allp=probes["edited"]+probes["native"]

def complete(prompt):
    body=json.dumps({"prompt":prompt,"n_predict":1,"temperature":0.0,"top_k":1,
                     "cache_prompt":False,"n_probs":0}).encode()
    req=urllib.request.Request(URL+"/completion",data=body,headers={"Content-Type":"application/json"})
    for attempt in range(5):
        try:
            r=urllib.request.urlopen(req,timeout=60); return json.loads(r.read())["content"]
        except Exception as ex:
            if attempt==4: raise
            time.sleep(2)

# wait for server health
for _ in range(120):
    try:
        urllib.request.urlopen(URL+"/health",timeout=3); break
    except Exception: time.sleep(2)

out=[]
for i,p in enumerate(allp):
    top1=complete(p["prompt"])
    out.append({"prompt":p["prompt"],"kind":p["kind"],"target":p["target"],"top1":top1})
    if (i+1)%50==0: print(f"  probed {i+1}/{len(allp)}",flush=True)
json.dump(out,open(OUT,"w"),indent=2,default=str)
print(f"wrote {OUT} ({len(out)} preds)",flush=True)
