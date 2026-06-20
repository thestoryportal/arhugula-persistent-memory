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
# D1 Phase 2 — the DECISIVE concentration-vs-dilution interference contrast.
# Pre-reg: docs/D1_CAPACITY_LAW_PREREG.md §2 Phase 2 / §3 (FROZEN criteria).
# Question (OQ-W1 / §7.2): at FIXED total edit-count N, does held-out same-relation
# read corruption depend on relation-CONCENTRATION (edits-per-relation) or on N itself?
#   CONCENTRATED arm: all N edits on `capital`.
#   DILUTED     arm: same N interleaved across {capital, language, continent}.
# Verdict by OVERLAY of held-out CAPITAL top-1 on x=capital-edit-count (advisor fix#1):
#   CONFIRM = curves overlay (corruption = f(capital-count); total-N irrelevant -> rewrite §8.7)
#   PARTIAL = diluted below concentrated at equal capital-count (cross-relation adds corruption)
#   NULL    = tracks total-N, not capital-count (spec edge-count counter adequate)
# Fixed disjoint held-out capital eval set (fix#2); continent = DILUTANT w/ expression guard (fix#3).
# Reuses g6_scale_n.py VERBATIM (my_edit/compute_P/inertness gate) -> engine UNMODIFIED, LAW#5.
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0)
BAND=os.environ.get("BAND","")                       # "" -> hp default [4-8]; e.g. "8,9,10,11,12" for the [8-12] contrast
if BAND: hp.layers=[int(x) for x in BAND.split(",")]
L=hp.layers
NULL_THRESH=0.005; L2=1.0
TOTAL_N=int(os.environ.get("TOTAL_N","50"))          # fixed total edit count per arm
MILESTONES=[int(x) for x in os.environ.get("MILESTONES","10,25,50").split(",")]  # total-count probes for within/global
HELDOUT_N=12

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded Qwen2.5-3B | band={L} | thresh={NULL_THRESH} L2={L2} | TOTAL_N={TOTAL_N}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES=["The largest planet in the solar system is","Water is composed of hydrogen and",
 "The chemical symbol for gold is","The opposite of hot is","The first president of the United States was"]

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def js(a,b):
    p=a.double(); q=b.double(); m=0.5*(p+q)
    def k(x,y): x=x.clamp_min(1e-12); y=y.clamp_min(1e-12); return float((x*(x.log()-y.log())).sum())
    return 0.5*k(p,m)+0.5*k(q,m)
def locpct(post,pre,pl): return round(100*sum(1-js(post[p]["dist"],pre[p]["dist"])/LN2 for p in pl)/len(pl),2)
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cuda().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False)
        idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu())
        print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]}", flush=True)
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

# ---------- INERTNESS GATE (LAW#5) — VERBATIM ----------
print("\n=== INERTNESS GATE: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL[a].format(e) for a in ["currency","continent","language"]]
pre0={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre0,probes); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre0,probes); restore(s0)
ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  engine expr={eng_p:.4f} loc={eng_loc}% | harness expr={my_p:.4f} loc={my_loc}% | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ---------- pools (disjoint; fix#2) ----------
sel=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
ents=[x for x in sel if all(r in sel[x] and "truth" in sel[x][r] for r in ["capital","language","continent"])]
SEED=int(os.environ.get("SEED","0")); ORDER=os.environ.get("ORDER","interleaved")  # replication knobs (advisor: entity/ordering-specificity is the live falsifier)
if SEED>0: random.Random(SEED).shuffle(ents)
print(f"SEED={SEED} ORDER={ORDER}", flush=True)
edit_pool=ents[:50]; heldout_cap_ents=ents[50:50+HELDOUT_N]
assert not (set(edit_pool)&set(heldout_cap_ents)), "held-out must be disjoint from edit pool"
def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]; st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf
CF={f:assign_cf(edit_pool,f) for f in ["capital","language","continent"]}

# arms: edit sequences of (entity, relation). Distinct entities per (relation) within edit_pool.
cap_e=edit_pool[0:17]; lang_e=edit_pool[17:34]; cont_e=edit_pool[34:50]
CONCENTRATED=[(e,"capital") for e in edit_pool][:TOTAL_N]                       # all on capital
if ORDER=="blocked":                                                            # ordering falsifier: all cap, then lang, then cont
    DILUTED=([(e,"capital") for e in cap_e]+[(e,"language") for e in lang_e]+[(e,"continent") for e in cont_e])[:TOTAL_N]
else:                                                                            # interleaved cap/lang/cont (default)
    DILUTED=[]
    for i in range(17):
        if i<len(cap_e): DILUTED.append((cap_e[i],"capital"))
        if i<len(lang_e): DILUTED.append((lang_e[i],"language"))
        if i<len(cont_e): DILUTED.append((cont_e[i],"continent"))
    DILUTED=DILUTED[:TOTAL_N]
print(f"\nedit_pool={len(edit_pool)} | held-out capital={len(heldout_cap_ents)} (disjoint) | "
      f"CONC={len(CONCENTRATED)} edits (capital×{sum(r=='capital' for _,r in CONCENTRATED)}) | "
      f"DIL={len(DILUTED)} edits (cap×{sum(r=='capital' for _,r in DILUTED)} lang×{sum(r=='language' for _,r in DILUTED)} cont×{sum(r=='continent' for _,r in DILUTED)})", flush=True)

heldout_probes=[{"prompt":TMPL["capital"].format(e),"truth":sel[e]["capital"]["truth"]} for e in heldout_cap_ents]
within_probes=[TMPL["continent"].format(e) for e in cap_e]      # capital-edited entities' continent (clean in CONC)
allprobe=[h["prompt"] for h in heldout_probes]+within_probes+GLOBAL_PROBES
def heldout_cap_top1(pre):
    post={h["prompt"]:predict(h["prompt"]) for h in heldout_probes}
    corr=round(100*sum(correct(post[h["prompt"]]["tok"],h["truth"]) for h in heldout_probes)/len(heldout_probes),1)
    stab=round(100*sum(post[h["prompt"]]["id"]==pre[h["prompt"]]["id"] for h in heldout_probes)/len(heldout_probes),1)
    js_loc=locpct({h["prompt"]:post[h["prompt"]] for h in heldout_probes},pre,[h["prompt"] for h in heldout_probes])
    return corr,stab,js_loc

def run_arm(name, seq):
    print(f"\n=== ARM: {name} ({len(seq)} edits) ===", flush=True)
    restore(s_clean)
    pre={p:predict(p) for p in set(allprobe)}
    cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
    base_corr,_,_=heldout_cap_top1(pre)
    traj=[{"total":0,"capital":0,"relation":"base","heldout_cap_correct":base_corr,"heldout_cap_stable":100.0,"delta_norm":0.0}]
    edited=[]; cap_ct=0
    for k,(e,rel) in enumerate(seq, start=1):
        b=snap()
        with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,rel,CF[rel][e]),"alphaedit",P,cache)
        with torch.no_grad():
            npd=dict(model.named_parameters())
            dnorm=float(sum(torch.norm((npd[WN(layer)].float()-b[layer].float())).item() for layer in L))
        del b
        expressed=bool(predict(TMPL[rel].format(e))["id"]==first_tok(CF[rel][e]))
        edited.append({"entity":e,"relation":rel,"expressed":expressed})
        if rel=="capital": cap_ct+=1
        corr,stab,_=heldout_cap_top1(pre)
        traj.append({"total":k,"capital":cap_ct,"relation":rel,"heldout_cap_correct":corr,"heldout_cap_stable":stab,"delta_norm":round(dnorm,3)})
    # milestones: within/global + JS
    miles={}
    corr,stab,jsl=heldout_cap_top1(pre)
    within_loc=locpct({p:predict(p) for p in within_probes},pre,within_probes)
    global_loc=locpct({p:predict(p) for p in GLOBAL_PROBES},pre,GLOBAL_PROBES)
    # write-side retention + dilutant expression guard
    ret=round(100*sum(bool(predict(TMPL[x['relation']].format(x['entity']))["id"]==first_tok(CF[x['relation']][x['entity']])) for x in edited)/len(edited),1)
    expr_all=round(100*sum(x["expressed"] for x in edited)/len(edited),1)
    dilutant=[x for x in edited if x["relation"]!="capital"]
    dil_expr=round(100*sum(x["expressed"] for x in dilutant)/len(dilutant),1) if dilutant else None
    cont_only=[x for x in edited if x["relation"]=="continent"]
    cont_expr=round(100*sum(x["expressed"] for x in cont_only)/len(cont_only),1) if cont_only else None
    print(f"  base held-out capital correct={base_corr}% -> end={corr}% (stable={stab}% JS-loc={jsl}%) | within(continent)={within_loc}% global={global_loc}%", flush=True)
    print(f"  GUARD: write retention={ret}% apply-expr(all)={expr_all}% | dilutant-expr={dil_expr}% (continent-expr={cont_expr}%)", flush=True)
    return {"name":name,"base_heldout_cap_correct":base_corr,"trajectory":traj,
            "end":{"heldout_cap_correct":corr,"heldout_cap_stable":stab,"heldout_cap_js_loc":jsl,
                   "within_continent_loc":within_loc,"global_loc":global_loc,
                   "write_retention":ret,"apply_expr_all":expr_all,"dilutant_expr":dil_expr,"continent_expr":cont_expr}}

# ---------- run both arms from a shared clean base ----------
P=compute_P(); s_clean=snap()
R_conc=run_arm("CONCENTRATED",CONCENTRATED)
R_dil =run_arm("DILUTED",DILUTED)

# ---------- analysis: overlay on capital-count + total-count (advisor fix#1) ----------
def at_capital(traj,c):  # held-out cap correct at the LAST point with capital==c
    pts=[t for t in traj if t["capital"]==c]; return pts[-1]["heldout_cap_correct"] if pts else None
def at_total(traj,n):
    pts=[t for t in traj if t["total"]==n]; return pts[-1]["heldout_cap_correct"] if pts else None
# Discriminating milestones (avoid noisy single-edit points). Diluted reaches capital~17, total 50.
CAP_MILES=[c for c in (5,10,15) if c<=min(max(t["capital"] for t in R_conc["trajectory"]),max(t["capital"] for t in R_dil["trajectory"]))]
TOT_MILES=[n for n in (15,30,45) if n<=min(max(t["total"] for t in R_conc["trajectory"]),max(t["total"] for t in R_dil["trajectory"]))]
overlay_cap=[{"capital_count":c,"conc":at_capital(R_conc["trajectory"],c),"dil":at_capital(R_dil["trajectory"],c)} for c in CAP_MILES]
overlay_tot=[{"total_count":n,"conc":at_total(R_conc["trajectory"],n),"dil":at_total(R_dil["trajectory"],n)} for n in TOT_MILES]
def maxgap(ov): g=[abs(o["conc"]-o["dil"]) for o in ov if o["conc"] is not None and o["dil"] is not None]; return max(g) if g else None
gap_cap=maxgap(overlay_cap)   # small => corruption is f(capital-count)
gap_tot=maxgap(overlay_tot)   # small => corruption is f(total-count)
# verdict on the FROZEN rule (§3), using BOTH axes to separate CONFIRM / NULL / PARTIAL
pos_control = (R_conc["end"]["heldout_cap_correct"] < R_conc["base_heldout_cap_correct"] - 5)  # concentrated must actually corrupt
dilutant_ok = (R_dil["end"]["dilutant_expr"] is None) or (R_dil["end"]["dilutant_expr"]>=95)
if not pos_control:
    verdict="INVALID (positive control: concentrated arm did not corrupt held-out capital -> instrument inert)"
elif not dilutant_ok:
    verdict=f"INVALID (false dilution: dilutant expression {R_dil['end']['dilutant_expr']}% < 95% -> non-capital edits not real)"
elif gap_cap is not None and gap_cap<=5 and (gap_tot is None or gap_tot>5):
    verdict="CONFIRM (overlays on capital-count, diverges on total-count -> corruption=f(capital-count); §8.7 must count per-relation)"
elif gap_tot is not None and gap_tot<=5 and (gap_cap is None or gap_cap>5):
    verdict="NULL (overlays on total-count, diverges on capital-count -> corruption=f(total-N); spec edge-count counter adequate, calibrate OQ-W1 only)"
elif (gap_cap is not None and gap_cap>5) and (gap_tot is not None and gap_tot>5):
    verdict="PARTIAL (diverges on BOTH axes -> two-variable law f(capital-count, total-N); §8.7 monitors both)"
else:
    verdict="INCONCLUSIVE (both axes overlay or insufficient overlap -> low signal; inspect trajectories)"
out={"experiment":"D1_phase2_concentration_sweep","band":L,"total_N":TOTAL_N,"engine":"kmeng01/memit UNMODIFIED",
     "heldout_capital_entities":heldout_cap_ents,
     "overlay_on_capital_count":overlay_cap,"overlay_on_total_count":overlay_tot,
     "gap_capital_axis_pp":gap_cap,"gap_total_axis_pp":gap_tot,
     "positive_control_ok":pos_control,"dilutant_ok":dilutant_ok,"verdict":verdict,
     "CONCENTRATED":R_conc,"DILUTED":R_dil}
suffix=(f"_seed{SEED}_{ORDER}" if SEED>0 else "")+("" if not BAND else "_band"+BAND.split(",")[0]+"_"+BAND.split(",")[-1])
op=f"{LLMDB_ROOT}/results/d1_concentration_sweep_result{suffix}.json"
json.dump(out,open(op,"w"),indent=2,default=str)
print(f"\n=== OVERLAY A: held-out capital top-1 @ equal CAPITAL-edit-count ===", flush=True)
print(f"{'cap-count':>9} | {'CONC':>6} | {'DIL':>6}", flush=True)
for o in overlay_cap: print(f"{o['capital_count']:>9} | {str(o['conc']):>6} | {str(o['dil']):>6}", flush=True)
print(f"=== OVERLAY B: held-out capital top-1 @ equal TOTAL-edit-count ===", flush=True)
print(f"{'total':>9} | {'CONC':>6} | {'DIL':>6}", flush=True)
for o in overlay_tot: print(f"{o['total_count']:>9} | {str(o['conc']):>6} | {str(o['dil']):>6}", flush=True)
print(f"\ngap(capital-axis)={gap_cap}pp gap(total-axis)={gap_tot}pp | pos_control={pos_control} dilutant_ok={dilutant_ok}", flush=True)
print(f"VERDICT: {verdict}", flush=True)
print(f"wrote {op}\nD1_PHASE2_DONE", flush=True)
