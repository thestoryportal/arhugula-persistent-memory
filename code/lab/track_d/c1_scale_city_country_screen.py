import os, sys, json, collections
LLMDB_ROOT=os.environ.get("LLMDB_ROOT","/workspace")
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import geonamescache

# ============================================================================
# C1 true-scale stimulus screen (NO editing — forward passes only).
# Q: how many city->country facts does Qwen2.5-3B NATIVELY know, with a
# SINGLE-TOKEN country answer + confidence, at scale? This achievable N is the
# gate for the true-scale C1 falsifier (high N at HIGH per-relation concentration
# — one relation, advisor-mandated, NOT a multi-domain dilution).
# city = subject (multi-token OK); country = value (must be single-token).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
CONF=0.30   # maxprob floor (same spirit as B0/R3 confident-correct screen)
TOPK_CANDIDATES=6000  # screen this many highest-population cities (in single-tok countries)

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
tok.padding_side="left"
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]

@torch.no_grad()
def predict_batch(prompts):
    enc=tok(prompts,return_tensors="pt",padding=True).to("cuda")
    logits=model(**enc).logits[:,-1,:].float()
    pr=torch.softmax(logits,dim=-1); v,i=torch.topk(pr,1,dim=-1)
    return [(int(i[k,0]), tok.decode([int(i[k,0])]), float(v[k,0])) for k in range(len(prompts))]

# ---- build candidate list: top-pop cities whose country name is single-token ----
gc=geonamescache.GeonamesCache()
cities=gc.get_cities(); countries=gc.get_countries()
# common-name overrides (geonames official names are often multi-token / formal)
NAME_FIX={"United States":"America","Russian Federation":"Russia","Iran (Islamic Republic of)":"Iran",
          "Korea, Republic of":"Korea","Syrian Arab Republic":"Syria","Viet Nam":"Vietnam",
          "Tanzania, United Republic of":"Tanzania","Bolivia (Plurinational State of)":"Bolivia",
          "Venezuela (Bolivarian Republic of)":"Venezuela","Czechia":"Czechia","Türkiye":"Turkey",
          "Lao People's Democratic Republic":"Laos","Moldova, Republic of":"Moldova"}
def cname(cc):
    raw=countries.get(cc,{}).get("name","")
    return NAME_FIX.get(raw, raw)

rows=[]
for cid,c in cities.items():
    cc=c["countrycode"]; country=cname(cc)
    if not country: continue
    if not single_tok(country): continue           # value must be single-token
    rows.append({"city":c["name"],"country":country,"pop":c.get("population",0) or 0})
# dedup by (city,country); sort by population desc; cap
seen=set(); cand=[]
for r in sorted(rows,key=lambda r:-r["pop"]):
    k=(r["city"],r["country"])
    if k in seen: continue
    seen.add(k); cand.append(r)
cand=cand[:TOPK_CANDIDATES]
print(f"candidates (single-token-country, top-pop, dedup): {len(cand)} | distinct countries: {len({r['country'] for r in cand})}", flush=True)

# ---- template bake-off on a known-city probe set ----
KNOWN=[("Paris","France"),("Tokyo","Japan"),("Cairo","Egypt"),("Mumbai","India"),("Rome","Italy"),
       ("Madrid","Spain"),("Berlin","Germany"),("Moscow","Russia"),("Toronto","Canada"),("Lagos","Nigeria"),
       ("Bangkok","Thailand"),("Lima","Peru"),("Athens","Greece"),("Dublin","Ireland"),("Oslo","Norway")]
TEMPLATES={
 "loc_country_of":"The city of {} is located in the country of",
 "is_city_in":"{} is a city in the country of",
 "located_in":"{} is located in the country of",
}
print("\n=== TEMPLATE BAKE-OFF (known cities, single-token country) ===", flush=True)
best=None
for name,tmpl in TEMPLATES.items():
    ps=[tmpl.format(c) for c,_ in KNOWN]; preds=predict_batch(ps)
    hit=sum(pid==first_tok(co) for (pid,_,_),(_,co) in zip(preds,KNOWN))
    conf=sum(mp>=CONF for _,_,mp in preds)
    print(f"  {name:16s} correct {hit}/{len(KNOWN)} | conf>={CONF}: {conf}/{len(KNOWN)}", flush=True)
    if best is None or hit>best[1]: best=(name,hit,tmpl)
TMPL=best[2]; print(f"  -> using template '{best[0]}': {TMPL!r}", flush=True)

# ---- full screen ----
print(f"\n=== SCREENING {len(cand)} cities ===", flush=True)
BATCH=256; passed=[]
for s in range(0,len(cand),BATCH):
    chunk=cand[s:s+BATCH]
    preds=predict_batch([TMPL.format(r["city"]) for r in chunk])
    for r,(pid,ptok,mp) in zip(chunk,preds):
        r["top1"]=ptok.strip(); r["maxprob"]=round(mp,4)
        r["correct"]=bool(pid==first_tok(r["country"]))
        r["pass"]=bool(r["correct"] and mp>=CONF)
        if r["pass"]: passed.append(r)
    if s % (BATCH*8)==0: print(f"  {s+len(chunk)}/{len(cand)} screened | passed so far {len(passed)}", flush=True)

n_correct=sum(r["correct"] for r in cand); n_pass=len(passed)
by_country=collections.Counter(r["country"] for r in passed)
# concentration view: how many PASS facts available per single country (the high-concentration arm)
top_countries=by_country.most_common(20)
# CORE-feasibility: cities with very high confidence (>=0.8) = clean CORE candidates
core_pool=[r for r in passed if r["maxprob"]>=0.8]

out={"model":ID,"template":TMPL,"conf_floor":CONF,"n_candidates":len(cand),
     "n_native_correct":n_correct,"n_pass_correct_and_confident":n_pass,
     "distinct_pass_countries":len(by_country),
     "top_countries_by_pass_count":top_countries,
     "core_pool_conf>=0.8":len(core_pool),
     "achievable_high_concentration_N_single_relation":n_pass,
     "passed_sample":[{k:r[k] for k in ("city","country","maxprob")} for r in passed[:50]]}
json.dump(out,open(f"{LLMDB_ROOT}/results/c1_scale_city_country_screen.json","w"),indent=1,default=str)
# also dump the full passed pool for downstream pool-build
json.dump([{k:r[k] for k in ("city","country","maxprob")} for r in passed],
          open(f"{LLMDB_ROOT}/results/c1_scale_city_country_pool.json","w"),indent=0,default=str)
print(f"\n=== SCREEN RESULT ===", flush=True)
print(f"  candidates: {len(cand)} | native-correct: {n_correct} | PASS (correct & conf>={CONF}): {n_pass}", flush=True)
print(f"  distinct PASS countries: {len(by_country)} | CORE pool (conf>=0.8): {len(core_pool)}", flush=True)
print(f"  top countries by pass-count: {top_countries[:10]}", flush=True)
print(f"  >>> achievable high-concentration N (single relation city->country) = {n_pass}", flush=True)
print("DONE", flush=True)
