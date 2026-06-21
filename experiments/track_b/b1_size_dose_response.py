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
# B1 — MODEL-SIZE TERM for the D1 relation-concentration capacity law.
# Pre-reg: docs/B1_SIZE_TERM_PREREG.md (FROZEN 2026-06-21, advisor-vetted).
# Port of experiments/track_d/d1_dose_response.py (the D1 Phase-3 harness),
# PROTOCOL-IDENTICAL, parametrized by MODEL env (3b|7b) + ONE added measurement:
#   §2.1 ΔW-norm logging (advisor gate #1) — band-summed per-edit Frobenius norm,
#   so a "size protects/worsens" verdict is checkable against edit-strength, not
#   confounded by it (the C2-band trap). LOGGING ONLY — science path UNCHANGED.
# Run on BOTH 3b (reproduces D1 + adds norms) and 7b (the new size point).
#   each dose arm (total-N=48 on FIXED 48-entity pool, same entities every arm):
#     PHASE A: k CAPITAL edits  -> held-out capital = R_pure_k (pure ref) + cap ΔW-norm
#     PHASE B: (48-k) LANGUAGE edits -> held-out capital = R_after
#     cross_relation_term_k = R_pure_k - R_after
# k in {24,36,42}. 3 seeds. Held-out = baseline-correct capital entities, disjoint.
# Engine kmeng01/memit UNMODIFIED; my_edit/compute_P/inertness gate behaviorally
# VERBATIM (LAW#5). compute_P SVD on CPU for 7b (VRAM-safe; P deterministic, inert).
# ============================================================================
MODEL=os.environ.get("MODEL","7b").lower()
CFG={
 "3b":{"id":"Qwen/Qwen2.5-3B","rev":"3aab1f1954e9cc14eb9509a215f9e5ca08227a9b","hp":"qwen25_3b_memit_hparams.json","svd":"cuda"},
 "7b":{"id":"Qwen/Qwen2.5-7B","rev":"d149729398750b98c0af14eb82c78cfe92750796","hp":"qwen25_7b_memit_hparams.json","svd":"cuda"},
}[MODEL]
ID=CFG["id"]; REV=CFG["rev"]; SVD_DEVICE=CFG["svd"]
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/{CFG['hp']}"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
TOTAL_N=48; DOSES=[24,36,42]; HELDOUT_N=24
SEEDS=[int(x) for x in os.environ.get("SEEDS","1,2,3").split(",")]

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"MODEL={MODEL} loaded {ID} | band={L} thresh={NULL_THRESH} svd={SVD_DEVICE} | TOTAL_N={TOTAL_N} doses={DOSES} held-out={HELDOUT_N} seeds={SEEDS}", flush=True)
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
def compute_P():
    # cov (mom2 moment) is symmetric PSD -> use eigh: for symmetric PSD the singular values
    # EQUAL the eigenvalues, so the null-space projector P (small-σ subspace) is IDENTICAL to
    # the svd construction with the SAME threshold. eigh (cuSOLVER syevd) is fast + low-memory
    # (no Vh), unlike gesvd which stalls at n=18944. Mathematically inert reimplementation of P.
    Ps=[]
    for li,layer in enumerate(L):
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype)
        cov=cov.to(SVD_DEVICE).float()
        if li==0:
            asym=float((cov-cov.T).abs().max()); sc=float(cov.abs().max())
            print(f"  [compute_P] cov symmetry residual max|cov-cov^T|={asym:.3e} (scale {sc:.3e}) -> eigh valid", flush=True)
        S,U=torch.linalg.eigh(cov)                           # ascending eigenvalues; U eigenvectors
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        print(f"  [compute_P] layer {layer}: null-dim={idx.numel()}/{S.numel()} (min λ={float(S.min()):.3e})", flush=True)
        del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, mode, P=None, cache_c=None, norm_log=None):
    """Behaviorally VERBATIM from g6_scale_n.py / d1_dose_response (proven inert, LAW#5).
    The ONLY addition is norm_log (measurement-only): append band-summed ||ΔW||_F of
    THIS edit. It reads `upd` after it is computed; it changes NO tensor fed to the
    model -> science path identical. Inertness gate runs with norm_log=None."""
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters()); _band_fro=0.0
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
            # VRAM-careful, value-IDENTICAL to `A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(...)` (proven bit-exact):
            # in-place add + early del + diagonal add (== +L2*I) keep peak under the 24GB wall for 7B (18944).
            KK=Kg@Kg.T; KK.add_(ca); del ca                       # KK = Kg Kg^T + cache_c (in-place); free cache copy
            A=Pi@KK; del KK; A.diagonal().add_(L2)                # A = Pi(Kg Kg^T+ca) + L2 I  (diagonal add bit-identical to +L2*eye)
            B=Pi@Kg@rg.T; del Pi,Kg,rg; torch.cuda.empty_cache()  # free Pi(1.4GB)+keys before the solve's LU workspace
            upd=torch.linalg.solve(A,B).T.cpu()
            del A,B; torch.cuda.empty_cache()
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        if norm_log is not None: _band_fro+=float(upd.norm())          # measurement only
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    if mode=="alphaedit":
        for i,layer in enumerate(L):
            K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T
    if norm_log is not None: norm_log.append(_band_fro)
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
if not ok:
    json.dump({"halt":"LAW5_inertness","model":MODEL,"engine_p":eng_p,"harness_p":my_p,"delta":abs(eng_p-my_p)},
              open(f"{LLMDB_ROOT}/architecture_profile/b1_{MODEL}_halt_diagnostic.json","w"),indent=2)
    print("LAW#5 fail; HALT.", flush=True); sys.exit(0)
torch.cuda.empty_cache()   # free gate residual -> headroom for GPU SVD (compute_P) + the wide-intermediate solve

# ---------- pools ----------
sel=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
ents_all=[x for x in sel if all(r in sel[x] and "truth" in sel[x][r] for r in ["capital","language"])]
# baseline-correct on capital (clean base) — held-out must come from here (advisor Fix#3)
base_correct=[e for e in ents_all if correct(predict(TMPL["capital"].format(e))["tok"], sel[e]["capital"]["truth"])]
print(f"\nentities(ents_all)={len(ents_all)} | baseline-correct on capital={len(base_correct)}", flush=True)
# ---- POOL GUARD (prereg §2 N-rule, corrected to the harness's real requirement) ----
# harness needs: HELDOUT_N baseline-correct held-out + TOTAL_N edit-pool, disjoint.
HELDOUT_USE=HELDOUT_N
if len(base_correct) < 12 or len(ents_all) < (12+TOTAL_N):
    json.dump({"halt":"insufficient_pool","model":MODEL,"ents_all":len(ents_all),"base_correct":len(base_correct),
               "need":"base_correct>=12 (min held-out) and ents_all>=12+48"},
              open(f"{LLMDB_ROOT}/architecture_profile/b1_{MODEL}_halt_diagnostic.json","w"),indent=2)
    print(f"HALT: insufficient pool for matched-N (ents_all={len(ents_all)}, base_correct={len(base_correct)}).", flush=True); sys.exit(0)
if len(base_correct) < HELDOUT_N or len(ents_all) < (HELDOUT_N+TOTAL_N):
    HELDOUT_USE=min(len(base_correct), len(ents_all)-TOTAL_N)
    print(f"  [N-rule] shrinking HELDOUT_N {HELDOUT_N}->{HELDOUT_USE} (pool-limited); comparison stays at matched capital-edit-count", flush=True)

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
    cap_norms=[]
    # PHASE A: capital block
    for e in cap_ents:
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital",CF["capital"][e]),"alphaedit",P,cache,norm_log=cap_norms)
    R_pure=heldout_cap_correct(heldout)
    cap_expr=round(100*sum(predict(TMPL["capital"].format(e))["id"]==first_tok(CF["capital"][e]) for e in cap_ents)/len(cap_ents),1)
    cap_cum_norm=round(sum(cap_norms),3); cap_mean_norm=round(sum(cap_norms)/len(cap_norms),4)
    # PHASE B: language block (the dilutant)
    lang_norms=[]
    for e in lang_ents:
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"language",CF["language"][e]),"alphaedit",P,cache,norm_log=lang_norms)
    R_after=heldout_cap_correct(heldout)
    lang_expr=round(100*sum(predict(TMPL["language"].format(e))["id"]==first_tok(CF["language"][e]) for e in lang_ents)/len(lang_ents),1) if lang_ents else 100.0
    cross_term=round(R_pure-R_after,1)
    print(f"  seed{seed} k={k}: base={base}% -> R_pure(after {k} cap)={R_pure}% -> R_after(+{TOTAL_N-k} lang)={R_after}% | "
          f"cross_term={cross_term}pp | cap_expr={cap_expr}% lang_expr={lang_expr}% | cap_cum||ΔW||={cap_cum_norm} mean/edit={cap_mean_norm}", flush=True)
    return {"seed":seed,"k":k,"base":base,"R_pure_k":R_pure,"R_after_full":R_after,"cross_relation_term_pp":cross_term,
            "cap_expr":cap_expr,"lang_expr":lang_expr,"cap_cum_dW_fro":cap_cum_norm,"cap_mean_dW_fro_per_edit":cap_mean_norm,
            "lang_cum_dW_fro":round(sum(lang_norms),3)}

results=[]
for seed in SEEDS:
    rng=random.Random(seed)
    ho_pool=base_correct[:]; rng.shuffle(ho_pool); heldout=ho_pool[:HELDOUT_USE]
    rest=[e for e in ents_all if e not in set(heldout)]; rng.shuffle(rest); edit_pool=rest[:TOTAL_N]
    CF={f:assign_cf(edit_pool,f) for f in ["capital","language"]}
    print(f"\n=== SEED {seed} | held-out={len(heldout)} (baseline-correct, disjoint) | edit_pool={len(edit_pool)} ===", flush=True)
    for k in DOSES: results.append(run_dose(seed,k,edit_pool,heldout,CF))

# ---------- analysis ----------
import statistics as st
def agg(k,key):
    v=[r[key] for r in results if r["k"]==k]; return round(st.mean(v),3)
valid=[r for r in results if r["lang_expr"]>=95]   # dilutant guard
print(f"\n=== DOSE-RESPONSE (held-out capital correct, mean over seeds) | MODEL={MODEL} ===", flush=True)
print(f"{'k(cap)':>7}{'R_pure_k':>10}{'R_after':>9}{'cross_term':>11}{'cap_cum||ΔW||':>14}", flush=True)
for k in DOSES: print(f"{k:>7}{agg(k,'R_pure_k'):>10}{agg(k,'R_after_full'):>9}{agg(k,'cross_relation_term_pp'):>11}{agg(k,'cap_cum_dW_fro'):>14}", flush=True)
pure=[agg(k,'R_pure_k') for k in DOSES]
monotonic = pure[0]>=pure[1]>=pure[2]
cross_terms=[r["cross_relation_term_pp"] for r in valid]
cross_mean=round(st.mean(cross_terms),1) if cross_terms else None
gran=round(100/HELDOUT_USE,1)
cross_real = cross_mean is not None and cross_mean>gran and sum(1 for c in cross_terms if c>0)>=max(1,int(0.6*len(cross_terms)))
pos_control = pure[-1] < 95
all_lang_ok = all(r["lang_expr"]>=95 for r in results)
verdict = ("INVALID (language dilutant <95% expr in some arm)" if not all_lang_ok else
           "INVALID (positive control: highest-cap dose did not corrupt)" if not pos_control else
           f"REPLICATE: concentration corrupts (monotonic={monotonic}); cross-term mean {cross_mean}pp (gran {gran}pp)")
out={"experiment":"B1_size_term_dose_response","model":MODEL,"hf_id":ID,"revision":REV,"band":L,"svd_device":SVD_DEVICE,
     "total_N":TOTAL_N,"doses":DOSES,"heldout_n":HELDOUT_USE,"seeds":SEEDS,"engine":"kmeng01/memit UNMODIFIED",
     "ents_all":len(ents_all),"base_correct":len(base_correct),"per_run":results,
     "dose_response_pure_means":{k:agg(k,'R_pure_k') for k in DOSES},
     "cap_cum_dW_fro_means":{k:agg(k,'cap_cum_dW_fro') for k in DOSES},
     "cap_mean_dW_fro_per_edit_means":{k:agg(k,'cap_mean_dW_fro_per_edit') for k in DOSES},
     "cross_term_means":{k:agg(k,'cross_relation_term_pp') for k in DOSES},
     "cross_term_mean_all":cross_mean,"heldout_granularity_pp":gran,
     "monotonic_concentration":monotonic,"cross_relation_term_real":cross_real,
     "positive_control_ok":pos_control,"dilutant_ok":all_lang_ok,"verdict":verdict}
json.dump(out,open(f"{LLMDB_ROOT}/results/b1_{MODEL}_dose_response_result.json","w"),indent=2,default=str)
print(f"\nMODEL={MODEL} monotonic concentration: {monotonic} | pure dose-response {pure}", flush=True)
print(f"cap cumulative ||ΔW||_F per-dose: {[agg(k,'cap_cum_dW_fro') for k in DOSES]} | per-edit mean: {[agg(k,'cap_mean_dW_fro_per_edit') for k in DOSES]}", flush=True)
print(f"cross-relation term: mean={cross_mean}pp (gran {gran}pp)", flush=True)
print(f"VERDICT: {verdict}", flush=True)
print(f"B1_{MODEL.upper()}_DONE", flush=True)
