import os, sys, json, time, hashlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

# ============================================================================
# R1-bit — SELECT read-back via a G1 2PC commit-status BIT (CP-class delivery).
# Pre-reg: docs/R1_COMMIT_BIT_SELECT_PREREG.md (frozen). NOT a falsifier.
# Fixes R1 (CORPUS/31): replaces the bleed-unsound in-weight logprob reconciliation
# with a hash-chained State Ledger whose per-(entity,relation,target) commit bit is
# set ONLY on a successful 2PC commit -> bleed-immune by construction. CPU-only.
# Reuses the saved R1 artifact for the bleed-contrast + the L2-firing column.
# ============================================================================

# ---- G1 StateLedger (verbatim structure: hash-chained PREPARED/COMMITTED/ABORTED) ----
def _canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":"))
def _sha(s):   return hashlib.sha256(s.encode()).hexdigest()
class StateLedger:
    GENESIS = "0"*64
    def __init__(self, path):
        self.path=path; open(path,"w").close(); self._tip=self.GENESIS
    def append(self, etype, body):
        e={"seq":self._count(),"ts":round(time.time(),3),"entry_type":etype,"prev_hash":self._tip,"body":body}
        e["entry_hash"]=_sha(e["prev_hash"]+_canon(body))
        with open(self.path,"a") as f: f.write(_canon(e)+"\n")
        self._tip=e["entry_hash"]; return e
    def _count(self):
        with open(self.path) as f: return sum(1 for _ in f)
    def entries(self):
        with open(self.path) as f: return [json.loads(l) for l in f if l.strip()]
    def verify_chain(self):
        tip=self.GENESIS
        for e in self.entries():
            if e["prev_hash"]!=tip or e["entry_hash"]!=_sha(e["prev_hash"]+_canon(e["body"])): return False,f"break seq {e['seq']}"
            tip=e["entry_hash"]
        return True,"intact"
    def detect_prepared_bypass(self):
        prepared={e["body"].get("txn_id") for e in self.entries() if e["entry_type"]=="PREPARED"}
        return {e["body"].get("txn_id") for e in self.entries()
                if e["entry_type"]=="COMMITTED" and e["body"].get("txn_id") not in prepared}

LEDGER_PATH=f"{LLMDB_ROOT}/results/r1_commit_bit_ledger.jsonl"
DECLARED_RELATIONS={"capital","language","is_a","belongs_to","defined_in"}

# ---- reuse the R1 artifact (logprob sigs + L2 firing) for the bleed-contrast ----
R1=json.load(open(f"{LLMDB_ROOT}/results/r1_select_readback.json"))
STORE_THRESH=R1["STORE_THRESH_nats"]   # 2.0 — what the bleed-unsound proxy used
def r1_rows(setname): return R1["detail"][setname]
def r1_l2(setname, entity):
    for x in r1_rows(setname):
        if x["entity"]==entity: return x["L2_fires"]
    return None
# logprob sig per landed/dropped entity (to show what the proxy WOULD have done)
sig={r["entity"]:r["sig_nats"] for r in R1["recon_landed"]+R1["recon_dropped"]}

# ---- stimulus (mirror R1 exactly) ----
LANDED=[(x["entity"],x["relation"],x["value"]) for x in r1_rows("LANDED")]
DROPPED=[(x["entity"],x["relation"],x["value"]) for x in r1_rows("DROPPED")]
REJECTED=[(x["entity"],x["relation"],x.get("reject_reason")) for x in r1_rows("GATE_REJECTED")]
LEAK=[(x["entity"],x["relation"],x["value"]) for x in r1_rows("LEAK")]
ABSENT=[(x["entity"],x["relation"],x["value"]) for x in r1_rows("ABSENT_FICT")]
# the relation actually requested for rejected rows (R1 stored the violating relation in 'relation')
REJECTED_REL={x["entity"]:x["relation"] for x in r1_rows("GATE_REJECTED")}

led=StateLedger(LEDGER_PATH)

def validate(entity, relation):
    if relation=="violates": return (False,"violates_hard_reject")
    if relation not in DECLARED_RELATIONS: return (False,"undeclared_relation")
    return (True,"ok")

# ---- 2PC commit pipeline (G1 fault model: store-side VINDEX_FAILED -> ABORTED) ----
def commit_2pc(entity, relation, target, store_fault=False):
    txn=f"txn-{entity}"
    ok,why=validate(entity,relation)
    if not ok:
        led.append("WRITE_REJECTED",{"txn_id":txn,"entity":entity,"relation":relation,"reason":why}); return ("REJECTED",why)
    led.append("PREPARED",{"txn_id":txn,"entity":entity,"relation":relation,"target":target})
    if store_fault:   # store-side persistence failed during phase-2 -> abort, withhold the bit
        led.append("ABORTED",{"txn_id":txn,"entity":entity,"classification":"VINDEX_FAILED"}); return ("ABORTED","VINDEX_FAILED")
    led.append("COMMITTED",{"txn_id":txn,"entity":entity,"relation":relation,"target":target}); return ("COMMITTED",None)

print("=== R1-bit COMMIT PIPELINE (G1 2PC; commit-status bit) ===", flush=True)
for e,r,o in LANDED:   print(f"  LANDED   {e}: {commit_2pc(e,r,o)[0]}", flush=True)
for e,r,o in DROPPED:  print(f"  DROPPED  {e}: {commit_2pc(e,r,o,store_fault=True)[0]} (store-side fault)", flush=True)
for e,reason in [(e,reason) for e,_,reason in REJECTED]:
    rel=REJECTED_REL[e]; print(f"  REJECTED {e} (rel={rel}): {commit_2pc(e,rel,'X')[0]}", flush=True)
# LEAK / ABSENT never submitted

# ---- SELECT reads the commit-status bit (ledger), never the weights ----
def committed_bit(entity):
    """True iff a COMMITTED entry exists and no later ABORTED for the same txn."""
    es=led.entries(); txn=f"txn-{entity}"
    committed=[e for e in es if e["entry_type"]=="COMMITTED" and e["body"].get("txn_id")==txn]
    if not committed: return (False,None)
    last_seq=committed[-1]["seq"]
    aborted_after=any(e["entry_type"]=="ABORTED" and e["body"].get("txn_id")==txn and e["seq"]>last_seq for e in es)
    if aborted_after: return (False,None)
    return (True, committed[-1]["body"])
def SELECT(entity):
    ok,body=committed_bit(entity)
    if not ok: return {"result":"NULL","reason":"no_committed_bit"}
    return {"result":"TRIPLE","entity":body["entity"],"relation":body["relation"],"target":body["target"]}

# ---- evaluate every set; bit decision vs what the logprob proxy WOULD do ----
def proxy_would(entity):   # R1's bleed-unsound rule: reconcile iff sig >= STORE_THRESH
    s=sig.get(entity); return (s is not None and s>=STORE_THRESH, s)
def evalset(name, triples, fired_from):
    out=[]
    for e,r,o in triples:
        s=SELECT(e); pw,pv=proxy_would(e)
        out.append({"entity":e,"relation":r,"value":o,
                    "commit_bit_returns":s["result"],"select_correct":bool(s["result"]=="TRIPLE" and s.get("target")==o),
                    "logprob_proxy_would_return":("TRIPLE" if pw else "NULL"),"proxy_sig_nats":pv,
                    "L2_fires":r1_l2(fired_from,e)})
    return out
ev={
 "LANDED":evalset("LANDED",LANDED,"LANDED"),
 "DROPPED":evalset("DROPPED",DROPPED,"DROPPED"),
 "LEAK":evalset("LEAK",LEAK,"LEAK"),
 "ABSENT_FICT":evalset("ABSENT_FICT",ABSENT,"ABSENT_FICT"),
}
ev["GATE_REJECTED"]=[{"entity":e,"relation":REJECTED_REL[e],"commit_bit_returns":SELECT(e)["result"],
                      "reject_reason":reason,"L2_fires":r1_l2("GATE_REJECTED",e)} for e,_,reason in REJECTED]

# ---- scores (pre-registered delivery criteria) ----
d1=sum(x["select_correct"] for x in ev["LANDED"])
d2_null=sum(x["commit_bit_returns"]=="NULL" for x in ev["LEAK"]); d2_fire=sum(bool(x["L2_fires"] and x["L2_fires"]["correct"]) for x in ev["LEAK"])
d3_rej=sum(x["commit_bit_returns"]=="NULL" for x in ev["GATE_REJECTED"])
d3_drop=sum(x["commit_bit_returns"]=="NULL" for x in ev["DROPPED"])
# bleed-immunity: rows where proxy would TRIPLE but the bit says NULL (the R1 fix)
fixed=[x["entity"] for x in ev["DROPPED"]+ev["LEAK"] if x["logprob_proxy_would_return"]=="TRIPLE" and x["commit_bit_returns"]=="NULL"]
chain_ok,chain_msg=led.verify_chain(); bypass=led.detect_prepared_bypass()
hard_fail=any(x["commit_bit_returns"]=="TRIPLE" for x in ev["DROPPED"]+ev["LEAK"]+ev["GATE_REJECTED"])

D1=d1==8; D2=(d2_null==6); D3=(d3_rej==4 and d3_drop==2); D4=len(fixed)>=1; D5=(chain_ok and not bypass)
delivered=D1 and D2 and D3 and D4 and D5 and not hard_fail
outcome=("R1-bit DELIVERED-FOR-SCOPE (commit-time L1 read-back; post-commit divergence DEFERRED to C1)"
         if delivered else "NOT-DELIVERED")

out={"prereg":"docs/R1_COMMIT_BIT_SELECT_PREREG.md","class":"CP-class constructive delivery (not a falsifier)",
     "reuses":"results/r1_select_readback.json","store_thresh_proxy_nats":STORE_THRESH,
     "scores":{"D1_landed_readback":f"{d1}/8","D2_leak_null":f"{d2_null}/6 (model fires {d2_fire}/6)",
               "D3_rejected_null":f"{d3_rej}/4","D3_dropped_null_via_2PC_abort":f"{d3_drop}/2",
               "D4_bleed_immunity_rows_fixed":fixed,"D5_ledger_chain":chain_msg,"D5_prepared_bypass":sorted(bypass)},
     "pass_flags":{"D1":D1,"D2":D2,"D3":D3,"D4":D4,"D5":D5,"hard_fail":hard_fail},
     "OUTCOME":outcome,"scope":"commit-TIME consistency only; post-commit divergence (compaction/quant/corruption, R10/§11.3/D43) deferred to C1 (operator-scope-gated), NOT solved.",
     "bleed_contrast":[{"entity":x["entity"],"proxy_would":x["logprob_proxy_would_return"],"proxy_sig_nats":x["proxy_sig_nats"],
                        "commit_bit":x["commit_bit_returns"]} for x in ev["DROPPED"]+ev["LEAK"]],
     "detail":ev}
json.dump(out,open(f"{LLMDB_ROOT}/results/r1_commit_bit_select.json","w"),indent=2,default=str)

print(f"\n=== R1-bit RESULT ===", flush=True)
print(f"  D1 LANDED read-back:            {d1}/8", flush=True)
print(f"  D2 LEAK commit-bit=NULL:        {d2_null}/6 (model fires {d2_fire}/6)", flush=True)
print(f"  D3 GATE-REJECTED=NULL:          {d3_rej}/4", flush=True)
print(f"  D3 DROPPED=NULL via 2PC-abort:  {d3_drop}/2", flush=True)
print(f"  D4 bleed-immunity (proxy TRIPLE -> bit NULL): {fixed}", flush=True)
print(f"  D5 ledger chain={chain_msg} | prepared-bypass={sorted(bypass)}", flush=True)
print(f"  bleed-contrast: {json.dumps(out['bleed_contrast'])}", flush=True)
print(f"  >>> OUTCOME = {outcome}", flush=True)
print("DONE", flush=True)
