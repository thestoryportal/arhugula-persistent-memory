import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# R1 — Deployed SELECT triple-readback via a RECONCILED commit-ledger.
# Pre-reg: docs/R1_SELECT_READBACK_PREREG.md (frozen). Engine UNMODIFIED.
# Tests whether the DELEGATED index/query layer DELIVERS the spec's L1 SELECT
# read-back (§8.9) on the exact divergence cases bare weights fail (B0 leak):
#   - SELECT reads a POST-GATE ledger sidecar (not the request log)  -> anti-intent (a)
#   - reconciled vs the DEPLOYED store by an L1 storage signature      -> catches dropped writes
#   - returns NULL where it has no reconciled row                      -> anti-firing (b)
# Litmus: SELECT must return an answer differing from BOTH the write-request
# AND the model's greedy top-1. Reuses b0_select_primitive.py primitives VERBATIM.
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); L=hp.layers
NULL_THRESH=0.005; L2=1.0
STORE_THRESH=2.0  # nats; frozen in prereg. L1 storage signature gate.
TMPL={"capital":"The capital of {} is the city of","language":"The official language of {} is"}
PARA={"capital":"The capital city of {} is","language":"The main language spoken in {} is"}  # L2 firing (held-out paraphrase)
DECLARED_RELATIONS={"capital","language","is_a","belongs_to","defined_in"}  # G3/CP1 schema contract

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L} | STORE_THRESH={STORE_THRESH} nats", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"maxprob":float(t.values[0])}
@torch.no_grad()
def logprob_of(target_id, p):
    ids=tok(p,return_tensors="pt").to("cuda"); lp=torch.log_softmax(model(**ids).logits[0,-1].float(),dim=-1)
    return float(lp[target_id])
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]

def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); del cov,U,S; torch.cuda.empty_cache()
    return Ps

def my_edit(requests, mode, P=None, cache_c=None):
    """VERBATIM from b0_select_primitive.py / g6_scale_n_param.py (proven inert)."""
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[r["prompt"] for r in requests],
            words=[r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu()
        if mode=="memit":
            cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().double()
            adj=torch.linalg.solve(hp.mom2_update_weight*cov+Kd@Kd.T, Kd); upd=rd@adj.T
        else:
            Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
            A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T
            upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- LAW#5 INERTNESS GATE (harness MEMIT-mode vs engine apply_memit) ----------
print("\n=== INERTNESS GATE (LAW#5) ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo")
s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=float(torch.softmax(model(**tok(cons,return_tensors='pt').to('cuda')).logits[0,-1].float(),-1)[tgt]); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
my_p=float(torch.softmax(model(**tok(cons,return_tensors='pt').to('cuda')).logits[0,-1].float(),-1)[tgt]); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine expr={eng_p:.4f} | harness expr={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- STIMULUS (fictional subjects; real single-token values) ----------
FICT=["Zelmara","Brovania","Quenland","Tavoria","Cassovia","Drennan","Yulvania","Sornia",
      "Plavia","Velloria","Othenia","Kuvalia","Nyssara","Granicia","Marnovia","Theldwin",
      "Wescovia","Aldoria"]
CAP_VALS=["Paris","London","Rome","Madrid","Berlin","Vienna","Cairo","Oslo","Lima","Tokyo","Athens","Dublin"]
cap_vals=[v for v in CAP_VALS if single_tok(v)]
print(f"  single-token capital pool: {len(cap_vals)}", flush=True)

def mk(entity,value,attr="capital",relation="capital"):
    return {"entity":entity,"relation":relation,"attr":attr,"value":value,
            "prompt":TMPL[attr].format(entity),"para":PARA[attr].format(entity),
            "val_tok":first_tok(value)}

# LANDED: 8 fictional, gate-passed, ACTUALLY applied
landed=[mk(FICT[i],cap_vals[i%len(cap_vals)]) for i in range(8)]
# DROPPED: 2 fictional, ledger-claimed but NOT applied (2PC store-side failure)
dropped=[mk(FICT[8],cap_vals[8%len(cap_vals)]), mk(FICT[9],cap_vals[9%len(cap_vals)])]
# GATE-REJECTED: 4 fictional requests with schema violations (validator rejects pre-MEMIT)
rejected=[
    {**mk(FICT[10],cap_vals[10%len(cap_vals)],relation="violates"),"reject_reason":"violates"},
    {**mk(FICT[11],cap_vals[11%len(cap_vals)],relation="located_under"),"reject_reason":"undeclared_relation"},
    {**mk(FICT[12],cap_vals[0],relation="violates"),"reject_reason":"violates"},
    {**mk(FICT[13],cap_vals[1],relation="enemy_of"),"reject_reason":"undeclared_relation"},
]
# LEAK: 6 real countries, NEVER committed, base knows -> fires-not-stored
leak=[{"entity":c,"relation":"capital","attr":"capital","value":t,"prompt":TMPL["capital"].format(c),
       "para":PARA["capital"].format(c),"val_tok":first_tok(t)}
      for c,t in [("France","Paris"),("Japan","Tokyo"),("Egypt","Cairo"),("Italy","Rome"),("Spain","Madrid"),("Norway","Oslo")]]
# ABSENT-FICT: 8 fictional, never committed (FICT[14:18] unused above), base unknown -> neither
absent=[mk(n,cap_vals[0]) for n in FICT[14:18]+["Brennor","Calistan","Doravia","Esmeland"]]

# ---------- VALIDATOR / GATE (G3/CP1 contract; deterministic, pre-MEMIT) ----------
def validate(r):
    if r["relation"]=="violates": return (False,"violates_hard_reject")
    if r["relation"] not in DECLARED_RELATIONS: return (False,"undeclared_relation")
    return (True,"ok")

# ---------- baseline logprobs (for the L1 storage signature) ----------
def base_lp(rs): return [logprob_of(r["val_tok"], r["prompt"]) for r in rs]
lp_base_landed=base_lp(landed); lp_base_dropped=base_lp(dropped)

# ---------- COMMIT PIPELINE ----------
print("\n=== COMMIT PIPELINE (gate -> apply -> ledger) ===", flush=True)
ledger=[]   # the State-Ledger sidecar: only gate-passed + claimed-committed rows
# gate everyone who is "submitted to commit": landed + dropped + rejected
for r in landed:   ledger.append({**{k:r[k] for k in ("entity","relation","value","val_tok","prompt","para")},"claim":"LANDED"})
for r in dropped:  ledger.append({**{k:r[k] for k in ("entity","relation","value","val_tok","prompt","para")},"claim":"DROPPED"})
gate_results=[(r["entity"],validate(r)) for r in rejected]  # rejected never reach ledger
for ent,(ok_,why) in gate_results:
    print(f"  GATE reject {ent}: {why}", flush=True)
# APPLY only the landed set (dropped is ledger-claimed but store-side fails)
P=compute_P(); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
my_edit([req(r["entity"],r["attr"],r["value"])[0] for r in landed],"alphaedit",P,cache)
print(f"  applied {len(landed)} LANDED edits; {len(dropped)} DROPPED ledger-claimed-but-not-applied", flush=True)

# ---------- RECONCILIATION: L1 storage signature vs DEPLOYED store ----------
def recon(r, lp_base):
    lp_dep=logprob_of(r["val_tok"], r["prompt"])
    sig=lp_dep-lp_base
    return {"sig_nats":round(sig,3),"reconciled":bool(sig>=STORE_THRESH)}
for r,lpb in zip(landed,lp_base_landed):  r["recon"]=recon(r,lpb)
for r,lpb in zip(dropped,lp_base_dropped): r["recon"]=recon(r,lpb)
recon_map={r["entity"]:r["recon"] for r in landed+dropped}

# ---------- SELECT executor: returns triple iff reconciled ledger row, else NULL ----------
def SELECT(entity):
    rows=[L_ for L_ in ledger if L_["entity"]==entity]
    if not rows: return {"result":"NULL","reason":"no_ledger_row"}
    row=rows[0]; rc=recon_map.get(entity,{"reconciled":False,"sig_nats":None})
    if not rc["reconciled"]: return {"result":"NULL","reason":"recon_divergence","sig_nats":rc["sig_nats"]}
    return {"result":"TRIPLE","entity":entity,"relation":row["relation"],"target":row["value"],"sig_nats":rc["sig_nats"]}

# ---------- L2 firing (held-out paraphrase) ----------
def fires(r):
    p=predict(r["para"]); return {"top1":p["tok"],"maxprob":round(p["maxprob"],4),"correct":bool(p["id"]==r["val_tok"])}

# ---------- EVALUATE every set ----------
def select_triple_correct(r):
    s=SELECT(r["entity"])
    return s, (s["result"]=="TRIPLE" and s.get("target")==r["value"])

rows_out={}
def evalset(name, rs):
    out=[]
    for r in rs:
        s,sel_ok=select_triple_correct(r)
        f=fires(r)
        out.append({"entity":r["entity"],"relation":r["relation"],"value":r["value"],
                    "SELECT":s,"select_returns_triple":bool(s["result"]=="TRIPLE"),
                    "select_correct":bool(sel_ok),"L2_fires":f})
    rows_out[name]=out; return out

ev_landed=evalset("LANDED",landed)
ev_dropped=evalset("DROPPED",dropped)
ev_leak=evalset("LEAK",leak)
ev_absent=evalset("ABSENT_FICT",absent)
# rejected: never in ledger -> SELECT NULL by construction; still evaluate firing (should not fire, fictional)
ev_rejected=[]
for r in rejected:
    s=SELECT(r["entity"]); f=fires(r)
    ev_rejected.append({"entity":r["entity"],"relation":r["relation"],"reject_reason":r["reject_reason"],
                        "SELECT":s,"select_returns_triple":bool(s["result"]=="TRIPLE"),"L2_fires":f})
rows_out["GATE_REJECTED"]=ev_rejected

# ---------- SCORES (pre-registered) ----------
p1=sum(x["select_correct"] for x in ev_landed)                                  # /8 read-back
p2_select_null=sum(x["SELECT"]["result"]=="NULL" for x in ev_leak)              # /6 abstain on leak
p2_l2_fire=sum(x["L2_fires"]["correct"] for x in ev_leak)                       # /6 model fires
p3_rej_null=sum(x["SELECT"]["result"]=="NULL" for x in ev_rejected)            # /4
p3_drop_flag=sum(x["SELECT"]["result"]=="NULL" and x["SELECT"].get("reason")=="recon_divergence" for x in ev_dropped)  # /2
# contingency cells
def cell(rs):
    return {"stored_AND_fired":sum(x["select_returns_triple"] and x["L2_fires"]["correct"] for x in rs),
            "stored_NOT_fired":sum(x["select_returns_triple"] and not x["L2_fires"]["correct"] for x in rs),
            "fired_NOT_stored":sum((not x["select_returns_triple"]) and x["L2_fires"]["correct"] for x in rs),
            "neither":sum((not x["select_returns_triple"]) and not x["L2_fires"]["correct"] for x in rs)}
contingency={k:cell(v) for k,v in rows_out.items()}
fired_not_stored_total=sum(c["fired_NOT_stored"] for c in contingency.values())

P1=p1>=7
P2=(p2_select_null==6 and p2_l2_fire>=5)
P3=(p3_rej_null==4 and p3_drop_flag==2)
P4=(fired_not_stored_total>=1)
delivered=P1 and P2 and P3 and P4
# any leak/rejected/dropped row returning a triple = hard fail
hard_fail=any(x["select_returns_triple"] for x in ev_leak+ev_rejected+ev_dropped)
if hard_fail: outcome="FAIL_TAUTOLOGY (SELECT echoed intent/firing)"
elif delivered: outcome="R1_DELIVERED (reconciled SELECT meets L1 contract on divergence cases)"
elif P1 and not P2: outcome="PARTIAL_anti_firing_fail"
else: outcome="PARTIAL"

out={"prereg":"docs/R1_SELECT_READBACK_PREREG.md","model":ID,"band":L,"STORE_THRESH_nats":STORE_THRESH,
     "scores":{"P1_landed_readback":f"{p1}/8","P2_leak_select_null":f"{p2_select_null}/6","P2_leak_L2_fires":f"{p2_l2_fire}/6",
               "P3_rejected_null":f"{p3_rej_null}/4","P3_dropped_flagged":f"{p3_drop_flag}/2","P4_fired_not_stored":fired_not_stored_total},
     "pass_flags":{"P1":bool(P1),"P2":bool(P2),"P3":bool(P3),"P4":bool(P4),"hard_fail":bool(hard_fail)},
     "OUTCOME":outcome,"contingency":contingency,"detail":rows_out,
     "recon_landed":[{"entity":r["entity"],**r["recon"]} for r in landed],
     "recon_dropped":[{"entity":r["entity"],**r["recon"]} for r in dropped]}
json.dump(out,open(f"{LLMDB_ROOT}/results/r1_select_readback.json","w"),indent=2,default=str)

print(f"\n=== R1 RESULT ===", flush=True)
print(f"  P1 LANDED read-back (SELECT correct triple):     {p1}/8", flush=True)
print(f"  P2 LEAK SELECT=NULL (abstain on fires-not-stored): {p2_select_null}/6  | L2 fires {p2_l2_fire}/6", flush=True)
print(f"  P3 GATE-REJECTED SELECT=NULL:                    {p3_rej_null}/4", flush=True)
print(f"  P3 DROPPED reconciliation FLAGS divergence:      {p3_drop_flag}/2", flush=True)
print(f"  P4 fired-not-stored cells (R13 split):           {fired_not_stored_total}", flush=True)
print(f"  contingency: {json.dumps(contingency)}", flush=True)
print(f"  recon LANDED sigs: {[round(r['recon']['sig_nats'],2) for r in landed]}", flush=True)
print(f"  recon DROPPED sigs: {[round(r['recon']['sig_nats'],2) for r in dropped]}", flush=True)
print(f"  >>> OUTCOME = {outcome}", flush=True)
print("DONE", flush=True)
