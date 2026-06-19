import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Characterize the margin confound (advisor): do edited facts carry larger top-1
margins than native facts (compute_z inflates p(target))? Re-probe fp16 GGUF with
n_probs to get the top-1 probability of each fact. Compare edited vs native-country
(eligible = top-1==target). Completes the pre-registered post_p metric.
Usage: python b3_margin.py <server_url>"""
import sys, json, time, urllib.request, statistics as st
URL=sys.argv[1].rstrip("/")
probes=json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
def correct(top1,truth):
    if truth is None: return None
    a=(top1 or "").strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def top1prob(prompt):
    body=json.dumps({"prompt":prompt,"n_predict":1,"temperature":0.0,"top_k":1,
                     "n_probs":1,"cache_prompt":False}).encode()
    r=urllib.request.urlopen(urllib.request.Request(URL+"/completion",data=body,headers={"Content-Type":"application/json"}),timeout=60)
    d=json.loads(r.read())
    cp=d.get("completion_probabilities") or d.get("probs")
    tok=d["content"]
    if cp:
        entry=cp[0]
        plist=entry.get("probs") or entry.get("top_logprobs") or []
        if plist:
            p0=plist[0]
            prob=p0.get("prob")
            if prob is None and "logprob" in p0:
                import math; prob=math.exp(p0["logprob"])
            return tok, float(prob)
    return tok, None
for _ in range(120):
    try: urllib.request.urlopen(URL+"/health",timeout=3); break
    except Exception: time.sleep(2)

def margins(items, kind):
    out=[]
    for p in items:
        if p["kind"]!=kind: continue
        tok,prob=top1prob(p["prompt"])
        if p["target"] is not None and correct(tok,p["target"]) and prob is not None:
            out.append(prob)
    return out
ed=margins(probes["edited"],"edited")
nc=margins(probes["native"],"native_country")
def summ(x): return {"n":len(x),"median":round(st.median(x),4),"mean":round(st.mean(x),4),
                     "min":round(min(x),4),"q1":round(sorted(x)[len(x)//4],4)} if x else {"n":0}
res={"edited_top1_margin":summ(ed),"native_country_top1_margin":summ(nc),
     "interpretation":"if edited median >> native median, the 100% edited retention reflects inflated margins (compute_z), not intrinsic robustness parity"}
print(json.dumps(res,indent=2))
json.dump(res, open(f"{LLMDB_ROOT}/results/b3_margin_result.json","w"), indent=2)
print("wrote /workspace/results/b3_margin_result.json")
