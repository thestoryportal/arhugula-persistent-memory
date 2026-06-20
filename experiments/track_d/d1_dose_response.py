import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, io, contextlib, json, math, random
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
# ============================================================================
# D1 Phase 3 — clean high-cardinality concentration DOSE-RESPONSE + within-arm
# CROSS-RELATION-TERM isolation. Pre-reg: docs/D1_CAPACITY_LAW_PREREG.md §7d (FROZEN).
# Addresses the dual-review: replaces the cardinality-4 continent dilutant with
# `language` (clean high-cardinality), and (advisor Fix#1) isolates the cross-relation
# term WITHIN each arm, paired:
#   each dose arm (total-N=48 on a FIXED 48-entity pool, same entities every arm):
#     PHASE A: apply k CAPITAL edits  -> measure held-out capital = R_pure_k (pure ref)
#     PHASE B: apply (48-k) LANGUAGE edits -> measure held-out capital = R_after
#     cross_relation_term_k = R_pure_k - R_after   (seed, entities, capital edits held FIXED)
# k in {24,36,42} (in the corrupted regime; advisor: cap=12 saturates). 3 seeds.
# Held-out = 24 BASELINE-CORRECT capital entities (advisor Fix#2/3), disjoint from edits.
# Engine kmeng01/memit UNMODIFIED; my_edit/compute_P/inertness gate VERBATIM (LAW#5).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
TOTAL_N=48; DOSES=[24,36,42]; HELDOUT_N=24
SEEDS=[int(x) for x in os.environ.get("SEEDS","1,2,3").split(",")]

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded Qwen2.5-3B | band={L} thresh={NULL_THRESH} | TOTAL_N={TOTAL_N} doses={DOSES} held-out={HELDOUT_N} seeds={SEEDS}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"
TMPL={"capital":"The capital of {} is the city of","language":"The official language of {} is"}

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])])}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1,truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def locpct_js(a,b): pass
def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cuda().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, mode, P=None, cache_c=None):
    """VERBATIM from g6_scale_n.py / s243h — proven inert. DO NOT MODIFY (LAW#5)."""
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
            Pi=P[i].cuda(); ca=cache_c[i].cuda(); Kg=Kd.float().cuda(); rg=rd.float().cuda()
            A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0],device="cuda"); B=Pi@Kg@rg.T
            upd=torch.linalg.solve(A,B).T.cpu()
            del Pi,ca,Kg,rg,A,B; torch.cuda.empty_cache()
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T
def req(entity,attr,cf): return [{"prompt":TMPL[attr],"subject":entity,"target_new":{"str":" "+cf}}]

# ---------- INERTNESS GATE (LAW#5) — VERBATIM behaviorally ----------
print("\n=== INERTNESS GATE ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo")
@torch.no_grad()
def pcap(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),0); return float(pr[tgt])
s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=pcap(cons); restore(s0)                       # measure THEN restore (the Phase-2 ordering)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
my_p=pcap(cons); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine p(Cairo)={eng_p:.4f} | harness p(Cairo)={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- pools ----------
sel=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
ents_all=[x for x in sel if all(r in sel[x] and "truth" in sel[x][r] for r in ["capital","language"])]
# baseline-correct on capital (clean base) — held-out must come from here (advisor Fix#3)
base_correct=[e for e in ents_all if correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"])]
print(f"\nentities={len(ents_all)} | baseline-correct on capital={len(base_correct)}", flush=True)
def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]; st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf

def heldout_cap_correct(heldout):
    return round(100*sum(correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"]) for e in heldout)/len(heldout),1)

P=compute_P(); s_clean=snap()
def run_dose(seed, k, edit_pool, heldout, CF):
    restore(s_clean); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    base=heldout_cap_correct(heldout)
    cap_ents=edit_pool[:k]; lang_ents=edit_pool[k:TOTAL_N]
    # PHASE A: capital block
    for e in cap_ents:
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital",CF["capital"][e]),"alphaedit",P,cache)
    R_pure=heldout_cap_correct(heldout)
    cap_expr=round(100*sum(predict(TMPL["capital"].format(e))["id"]==first_tok(CF["capital"][e]) for e in cap_ents)/len(cap_ents),1)
    # PHASE B: language block (the dilutant)
    for e in lang_ents:
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"language",CF["language"][e]),"alphaedit",P,cache)
    R_after=heldout_cap_correct(heldout)
    lang_expr=round(100*sum(predict(TMPL["language"].format(e))["id"]==first_tok(CF["language"][e]) for e in lang_ents)/len(lang_ents),1) if lang_ents else 100.0
    cross_term=round(R_pure-R_after,1)
    print(f"  seed{seed} k={k}: base={base}% -> R_pure(after {k} cap)={R_pure}% -> R_after(+{TOTAL_N-k} lang)={R_after}% | "
          f"cross_term={cross_term}pp | cap_expr={cap_expr}% lang_expr={lang_expr}%", flush=True)
    return {"seed":seed,"k":k,"base":base,"R_pure_k":R_pure,"R_after_full":R_after,"cross_relation_term_pp":cross_term,
            "cap_expr":cap_expr,"lang_expr":lang_expr}

results=[]
for seed in SEEDS:
    rng=random.Random(seed)
    ho_pool=base_correct[:]; rng.shuffle(ho_pool); heldout=ho_pool[:HELDOUT_N]
    rest=[e for e in ents_all if e not in set(heldout)]; rng.shuffle(rest); edit_pool=rest[:TOTAL_N]
    CF={f:assign_cf(edit_pool,f) for f in ["capital","language"]}
    print(f"\n=== SEED {seed} | held-out={len(heldout)} (baseline-correct, disjoint) | edit_pool={len(edit_pool)} ===", flush=True)
    for k in DOSES: results.append(run_dose(seed,k,edit_pool,heldout,CF))

# ---------- analysis ----------
import statistics as st
def agg(k,key):
    v=[r[key] for r in results if r["k"]==k]; return round(st.mean(v),1)
valid=[r for r in results if r["lang_expr"]>=95]   # dilutant guard
print(f"\n=== DOSE-RESPONSE (held-out capital correct, mean over seeds) ===", flush=True)
print(f"{'k(cap)':>7}{'R_pure_k':>10}{'R_after':>9}{'cross_term':>11}", flush=True)
for k in DOSES: print(f"{k:>7}{agg(k,'R_pure_k'):>10}{agg(k,'R_after_full'):>9}{agg(k,'cross_relation_term_pp'):>11}", flush=True)
# pre-registered reads
pure=[agg(k,'R_pure_k') for k in DOSES]
monotonic = pure[0]>=pure[1]>=pure[2]   # more capital -> more corruption (lower correct)
cross_terms=[r["cross_relation_term_pp"] for r in valid]
cross_mean=round(st.mean(cross_terms),1) if cross_terms else None
# per-k cross-term significance vs held-out granularity (24 held-out -> 4.2pp/entity)
gran=round(100/HELDOUT_N,1)
cross_real = cross_mean is not None and cross_mean>gran and sum(1 for c in cross_terms if c>0)>=max(1,int(0.6*len(cross_terms)))
pos_control = pure[-1] < 95   # highest-capital dose must corrupt
all_lang_ok = all(r["lang_expr"]>=95 for r in results)
verdict = ("INVALID (language dilutant <95% expr in some arm)" if not all_lang_ok else
           "INVALID (positive control: highest-cap dose did not corrupt)" if not pos_control else
           f"CROSS-RELATION TERM REAL (mean {cross_mean}pp > {gran}pp granularity, consistent) -> two-variable law (concentration + cross-relation)" if cross_real else
           f"NO RESOLVABLE CROSS-RELATION TERM (mean {cross_mean}pp <= {gran}pp granularity) -> concentration dominates; cross-relation term below resolution")
out={"experiment":"D1_phase3_dose_response","band":L,"total_N":TOTAL_N,"doses":DOSES,"heldout_n":HELDOUT_N,"seeds":SEEDS,
     "engine":"kmeng01/memit UNMODIFIED","per_run":results,
     "dose_response_pure_means":{k:agg(k,'R_pure_k') for k in DOSES},
     "cross_term_means":{k:agg(k,'cross_relation_term_pp') for k in DOSES},
     "cross_term_mean_all":cross_mean,"heldout_granularity_pp":gran,
     "monotonic_concentration":monotonic,"cross_relation_term_real":cross_real,
     "positive_control_ok":pos_control,"dilutant_ok":all_lang_ok,"verdict":verdict}
json.dump(out,open(f"{LLMDB_ROOT}/results/d1_dose_response_result.json","w"),indent=2,default=str)
print(f"\nmonotonic concentration (more cap=more corruption): {monotonic} | pure dose-response {pure}", flush=True)
print(f"cross-relation term: per-k {[agg(k,'cross_relation_term_pp') for k in DOSES]} mean={cross_mean}pp (held-out granularity {gran}pp)", flush=True)
print(f"VERDICT: {verdict}", flush=True)
print("D1_PHASE3_DONE", flush=True)
