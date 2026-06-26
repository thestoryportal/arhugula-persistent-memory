import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# ============================================================================
# C10 RESIDUAL-TEST (Option B) — D-C10b-residual.
# Pre-reg: docs/C10_RESIDUAL_TEST_PREREG.md (frozen 2026-06-26; advisor-revised).
# SIZES the real in-weight C10 exposure: do PROJECT-COINED multi-WORD SEMANTIC
# values behave like the incoherent floor (~36%) or near ceiling (~97%)?
# 7 arms, SAME novel fictional subjects (isolate VALUE class), request-count matched.
# Binding R = min(A6 coined-realNoun, A7 coined-coined) para_full (no-prior continuation).
# A5 (single coined WORD) = supporting mechanism, NOT in R (§7.1 identifier-adjacent).
# Decompose length (A3->A4) vs continuation-type (A4->A6/A7) + teacher-forced per-tok.
# Engine UNMODIFIED; primitives VERBATIM from c10b (proven inert).
# ============================================================================
ID=os.environ.get("MODEL_ID","Qwen/Qwen2.5-3B"); REV=os.environ.get("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp=MEMITHyperParams.from_json(os.environ.get("HPARAMS",f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded {ID} | band={L}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,5)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])]),"dist":pr.cpu()}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def tgt_ids(s): return tok(" "+s,add_special_tokens=False)["input_ids"]
def ntok(s): return len(tgt_ids(s))
def single_tok(s): return ntok(s)==1
def js(a,b):
    p=a.double(); q=b.double(); m=0.5*(p+q)
    def k(x,y): x=x.clamp_min(1e-12); y=y.clamp_min(1e-12); return float((x*(x.log()-y.log())).sum())
    return 0.5*k(p,m)+0.5*k(q,m)
def locpct(post,pre,pl): return round(100*sum(1-js(post[p]["dist"],pre[p]["dist"])/LN2 for p in pl)/len(pl),2)

@torch.no_grad()
def full_seq_match(prompt, target_ids):
    ids=tok(prompt,return_tensors="pt").to("cuda")["input_ids"]; gen=[]; cur=ids
    for _ in range(len(target_ids)):
        nt=int(model(cur).logits[0,-1].argmax()); gen.append(nt); cur=torch.cat([cur,torch.tensor([[nt]],device="cuda")],dim=1)
    return (gen==list(target_ids), gen[0]==target_ids[0])

@torch.no_grad()
def teacher_forced_pertok(prompt, target_ids):
    # given the CORRECT prefix at each step, is target_ids[j] (j>=1) the argmax? length-normalized per-position storage.
    if len(target_ids)<2: return (0,0)
    base=tok(prompt,return_tensors="pt").to("cuda")["input_ids"]
    hits=0
    for j in range(1,len(target_ids)):
        cur=torch.cat([base, torch.tensor([target_ids[:j]],device="cuda")],dim=1)
        nt=int(model(cur).logits[0,-1].argmax()); hits+= (nt==target_ids[j])
    return (hits, len(target_ids)-1)  # (correct_continuation_tokens, total_continuation_positions)

def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def compute_P():
    Ps=[]
    for layer in L:
        cov=get_cov(model,tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu().float()
        U,S,_=torch.linalg.svd(cov, full_matrices=False); idx=(S<NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:,idx]@U[:,idx].T).cpu()); del cov,U,S; torch.cuda.empty_cache()
    return Ps
def my_edit(requests, P, cache_c):
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,rq,hp,zl,ctx) for rq in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,context_templates=[rq["prompt"] for rq in requests],
            words=[rq["subject"] for rq in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Kd=K.double().cpu(); rd=resid.double().cpu(); Pi=P[i]; ca=cache_c[i]; Kg=Kd.float(); rg=rd.float()
        A=Pi@(Kg@Kg.T+ca)+L2*torch.eye(Kg.shape[0]); B=Pi@Kg@rg.T; upd=torch.linalg.solve(A,B).T
        upd=upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...]+=upd.to(npd[WN(layer)].device,npd[WN(layer)].dtype)
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T

CANON="The capital of {} is the city of"
PTEST=["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"]
def r(prompt,subj,targ): return {"prompt":prompt,"subject":subj,"target_new":{"str":" "+targ}}

# ---------- INERTNESS GATE (LAW#5: p-delta AND locality) ----------
print("\n=== INERTNESS GATE (p-delta + locality) ===", flush=True)
e="Zorbland"; cons=CANON.format(e); tgt=first_tok("Cairo"); probes=[f"{e} is described as"]
pre={p:predict(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,[r(CANON,e,"Cairo")],hp,copy=False,return_orig_weights=False)
eng={p:predict(p) for p in [cons]+probes}; eng_p=float(eng[cons]["dist"][tgt]); eng_loc=locpct(eng,pre,probes); restore(s0)
Pg=compute_P(); cc=[torch.zeros(Pg[0].shape[0],Pg[0].shape[0]) for _ in L]
with contextlib.redirect_stdout(io.StringIO()): my_edit([r(CANON,e,"Cairo")],Pg,cc)
mine={p:predict(p) for p in [cons]+probes}; my_p=float(mine[cons]["dist"][tgt]); my_loc=locpct(mine,pre,probes); restore(s0)
gate_ok=abs(eng_p-my_p)<0.05 and abs(eng_loc-my_loc)<3
print(f"  |Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} -> {'INERT ✓' if gate_ok else 'NOT INERT ✗ HALT'}", flush=True)
if not gate_ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(0)

# ============================================================================
# STIMULUS construction (+ empirical verification; HALT if a pool fails)
# ============================================================================
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
caps=sorted({scr[c]["capital"]["truth"] for c in scr})
single_v=[k for k in caps if single_tok(k)]
coherent2=[k for k in caps if ntok(k)==2]   # real known bigram capitals
FICTION=["Zorbland","Quaxil","Plurnak","Vythorn","Glimsto","Drennik","Yastovel","Crulpane","Mophgar","Brinduun",
         "Trannak","Skornwell","Fluvane","Oxbarrow","Zephquin","Lurmaxen","Pradnoll","Kessivar","Wombryne","Halquin",
         "Vorlex","Quenby","Marsduq","Thelby"]
N=int(os.environ.get("N_EDIT","24")); FICTION=FICTION[:N]

# coined single WORDS (A5): candidate generated coined strings, ntok>=3, base 0
COINED_WORD=["Vextoria","Qorvexil","Plurnathia","Vindexar","Zorblantis","Drennikar","Skornwellia","Vythornis",
             "Crulpanea","Mophgaria","Brinduvia","Trannakor","Fluvanis","Zephquinos","Lurmaxen","Pradnollia",
             "Kessivaro","Wombrynth","Halquinor","Vorlexia","Quenbyra","Marsduqal","Thelbyon","Glimstovia"]
# coined HEADS + real category nouns (A6)
COINED_HEAD=["Qorvex","Vindex","Plurn","Drennik","Skorn","Vythorn","Crulpane","Vorlex","Zephquin","Lurmax",
             "Pradnoll","Kessivar","Wombryne","Halquin","Quenby","Marsduq","Thelby","Glimsto","Mophgar","Brindu",
             "Trannak","Fluvane","Oxbar","Yastov"]
REAL_NOUN=["City","Heights","Falls","Bay","Port","Springs","Harbor","Crossing"]
# coined MODIFIERS (A7) — no-prior continuation
COINED_MOD=["Zentra","Ploom","Vask","Threnn","Wyxen","Brakk","Voneth","Qurel","Stavik","Dwelos",
            "Phaxis","Yornel","Klavor","Druvik","Spraxil","Velmor","Gantho","Ulvenn","Treska","Bloraq",
            "Cindel","Marvox","Ossquin","Drelth"]

def assign(subs, pool): return {c: pool[(i*3+5)%len(pool)] for i,c in enumerate(subs)}
def assign_incoh(subs, pool, k):
    out={}
    for i,c in enumerate(subs):
        toks=[pool[(i*k+j) % len(pool)] for j in range(k)]
        # de-dup within a value
        seen=[];
        for t in toks:
            t2=t; off=1
            while t2 in seen: t2=pool[(i*k+len(seen)+off)%len(pool)]; off+=1
            seen.append(t2)
        out[c]=" ".join(seen)
    return out

Vsingle=assign(FICTION, single_v)
Vcoh2  =assign(FICTION, coherent2)
Vincoh2=assign_incoh(FICTION, single_v, 2)
Vincoh3=assign_incoh(FICTION, single_v, 3)
Vcword =assign(FICTION, [w for w in COINED_WORD if ntok(w)>=3])
Vcrn   ={c: f"{COINED_HEAD[(i*2)%len(COINED_HEAD)]} {REAL_NOUN[i%len(REAL_NOUN)]}" for i,c in enumerate(FICTION)}
Vcc    ={c: f"{COINED_HEAD[(i*2+1)%len(COINED_HEAD)]} {COINED_MOD[(i*3+2)%len(COINED_MOD)]}" for i,c in enumerate(FICTION)}

ARMS_SPEC=[("A1_single",Vsingle),("A2_coherent2",Vcoh2),("A3_incoh2",Vincoh2),("A4_incoh3",Vincoh3),
           ("A5_coined_word",Vcword),("A6_coined_realNoun",Vcrn),("A7_coined_coined",Vcc)]

# ---- pre-edit base (want ~0 for novel/no-prior values) + ntok report; HALT if a treatment leaks prior ----
def canon_full(c, val): return full_seq_match(CANON.format(c), tgt_ids(val))[0]
print("\n=== STIMULUS VERIFICATION (base~0, ntok) ===", flush=True)
base_report={}
for name,Vmap in ARMS_SPEC:
    base=sum(canon_full(c,Vmap[c]) for c in FICTION); nts=[ntok(Vmap[c]) for c in FICTION]
    base_report[name]={"base":base,"mean_ntok":round(sum(nts)/len(nts),2),"ntok_range":[min(nts),max(nts)]}
    print(f"  {name:20} base={base}/{N} mean_ntok={base_report[name]['mean_ntok']} range={base_report[name]['ntok_range']} ex={[Vmap[c] for c in FICTION[:3]]}", flush=True)
# HALT if any TREATMENT/control value class carries a strong pre-edit prior (base should be ~0)
bad=[n for n in base_report if base_report[n]["base"]>N*0.15]
if bad: print(f"STIMULUS HALT: pools with pre-edit prior >15% (not no-prior): {bad}", flush=True); sys.exit(0)
s_base=snap()

def run_arm(name, Vmap):
    restore(s_base); cache=[torch.zeros(Pg[0].shape[0],Pg[0].shape[0]) for _ in L]
    with contextlib.redirect_stdout(io.StringIO()): my_edit([r(CANON,c,Vmap[c]) for c in FICTION],Pg,cache)
    rows=[]
    for c in FICTION:
        tids=tgt_ids(Vmap[c]); cf,c1=full_seq_match(CANON.format(c),tids)
        para=[full_seq_match(p.format(c),tids) for p in PTEST]
        tf=[teacher_forced_pertok(p.format(c),tids) for p in PTEST]
        rows.append({"subj":c,"val":Vmap[c],"ntok":len(tids),"canon_full":cf,"canon_first":c1,
                     "para_full_hits":[x[0] for x in para],"para_first_hits":[x[1] for x in para],
                     "tf_correct":sum(t[0] for t in tf),"tf_total":sum(t[1] for t in tf)})
    restore(s_base); n=len(rows); npar=len(PTEST)
    # conditional P(full|first-correct) over subject×paraphrase trials
    fc=sum(sum(x["para_first_hits"]) for x in rows)  # first-correct count
    ff=sum(sum(1 for k in range(npar) if x["para_first_hits"][k] and x["para_full_hits"][k]) for x in rows)
    tf_c=sum(x["tf_correct"] for x in rows); tf_t=sum(x["tf_total"] for x in rows)
    out={"rows":rows,
         "canon_full":round(100*sum(x["canon_full"] for x in rows)/n,1),
         "canon_first":round(100*sum(x["canon_first"] for x in rows)/n,1),
         "para_full":round(100*sum(sum(x["para_full_hits"]) for x in rows)/(n*npar),1),
         "para_first":round(100*sum(sum(x["para_first_hits"]) for x in rows)/(n*npar),1),
         "para_any_full":round(100*sum(any(x["para_full_hits"]) for x in rows)/n,1),
         "cond_full_given_first":round(ff/fc,3) if fc else None,
         "tf_pertok_cont":round(100*tf_c/tf_t,1) if tf_t else None,
         "mean_ntok":round(sum(x["ntok"] for x in rows)/n,2)}
    print(f"  >>> {name:20}: PARA_full={out['para_full']}% first={out['para_first']}% any={out['para_any_full']}% | P(full|first)={out['cond_full_given_first']} tf_pertok={out['tf_pertok_cont']}% canon_full={out['canon_full']}% (ntok {out['mean_ntok']})", flush=True)
    return out

print("\n=== ARMS (novel inserts, same subjects, request-count matched) ===", flush=True)
arms={name:run_arm(name,Vmap) for name,Vmap in ARMS_SPEC}

# ---------- verdict (pre-registered, frozen) ----------
g=lambda a:arms[a]["para_full"]
S=g("A1_single"); A2=g("A2_coherent2"); Floor=g("A3_incoh2"); A4=g("A4_incoh3")
A5=g("A5_coined_word"); A6=g("A6_coined_realNoun"); A7=g("A7_coined_coined")
R=min(A6,A7)  # binding realistic robustness (no-prior continuation present via A7)
sanity_ok = S>=80 and A2>=80 and Floor<=55
if not sanity_ok:
    verdict=f"INCONCLUSIVE — sanity gate failed (S={S}>=80? A2={A2}>=80? Floor={Floor}<=55?); C10 effect did not cleanly reproduce this seed"
elif R>=80 and (R-A4)>=25:
    verdict="RESIDUAL ROBUST — realistic coined multi-word values generalize far above the length-matched floor; C10 bite is mostly the contrived two-unrelated-word case → C10 severity DOWN-sized"
elif R<=A4+10 or R<=50:
    verdict="RESIDUAL FRAGILE — realistic coined multi-word values fail like the incoherent floor; C10 covers the real in-weight value surface → C10 severity CONFIRMED-at-sized-level (AnyEdit port / hybrid routing warranted)"
else:
    verdict="PARTIAL / MID-BAND — realistic class between floor and ceiling; report the RANGE + governing variable (length vs continuation-type)"

decomp={"length_effect_A3_to_A4":round(Floor-A4,1),"conttype_effect_A4_to_A6":round(A6-A4,1),
        "conttype_effect_A4_to_A7":round(A7-A4,1),
        "realistic_RANGE_para_full":[A7,A6],"binding_R_min(A6,A7)":R,
        "ceiling_S":S,"floor2_A3":Floor,"floor3_A4":A4,"coherent_ctrl_A2":A2,"coined_word_A5(supporting)":A5}
summary={"harness":"band[4-8]/Qwen2.5-3B/AlphaEdit/single-batch/capital/NOVEL-insert/N<=24/1-seed/HF-fp16",
 "law5_gate":f"|Δexpr|={abs(eng_p-my_p):.4f} |Δloc|={abs(eng_loc-my_loc):.2f} INERT",
 "N_per_arm":len(FICTION),"base_report":base_report,
 "para_full_by_arm":{a:arms[a]["para_full"] for a in arms},
 "cond_full_given_first_by_arm":{a:arms[a]["cond_full_given_first"] for a in arms},
 "tf_pertok_by_arm":{a:arms[a]["tf_pertok_cont"] for a in arms},
 "decomposition":decomp,
 "binding_metric":"held-out-paraphrase FULL-SEQ; R=min(A6 realNoun, A7 coined-coined); deliverable=RANGE[A7,A6]",
 "verdict":verdict}
print("\n=== C10d RESIDUAL SUMMARY (BINDING: paraphrase full-seq, realistic coined classes) ===", flush=True)
for k,v in summary.items():
    if k not in ("base_report",): print(f"  {k}: {v}", flush=True)
OUT=os.environ.get("OUT",f"{LLMDB_ROOT}/results/c10d_residual_coined.json")
json.dump({"decision_id":"D-C10b-residual","run":"residual-test (Option B; size the real in-weight C10 exposure)",
           "class":"FALSIFIER-sizing (can-fail); target=local Intel CPU + batch writes; NOT promotable without advisor+cross-family",
           "summary":summary,"arms":{a:{k:v for k,v in arms[a].items() if k!='rows'} for a in arms},
           "detail":{a:arms[a]["rows"] for a in arms},
           "stimulus":{"CANON":CANON,"PTEST":PTEST,"FICTION":FICTION,
                       **{f"V_{name}":Vmap for name,Vmap in ARMS_SPEC}}},
          open(OUT,"w"),indent=2,default=str)
print(f"\nwrote {OUT}", flush=True); print("C10D_DONE", flush=True)
