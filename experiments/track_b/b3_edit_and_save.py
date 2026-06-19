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
# B3 / G6.2 — produce the A1-clean BATCH-edited Qwen2.5-3B, SAVE to HF format
# for GGUF->Q4_K_M quantization-survival probing. Reuses g6_scale_n.py machinery
# VERBATIM (the joint-solve batch path A1 proved cross-entity-clean @N<=100).
# Emits b3_probes.json: edited facts (target=cf) + native facts (never edited,
# target=truth) + HF-fp16 top-1 reference (cross-check vs GGUF-fp16 downstream).
# ============================================================================
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"); LN2=math.log(2.0); L=hp.layers
NULL_THRESH=0.005; L2=1.0
N_ENTITIES=50; FIELDS=["capital","language"]
TMPL={"capital":"The capital of {} is the city of","currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of","language":"The official language of {} is"}
GLOBAL_PROBES=["The largest planet in the solar system is","Water is composed of hydrogen and",
 "The chemical symbol for gold is","The opposite of hot is",
 "The first president of the United States was","The speed of light is approximately"]
SAVE_DIR=f"{LLMDB_ROOT}/b3_edited_qwen3b"

tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"loaded Qwen2.5-3B | band={L} mom2_uw={hp.mom2_update_weight} | thresh={NULL_THRESH} L2={L2}", flush=True)
WN=lambda layer: f"{hp.rewrite_module_tmp.format(layer)}.weight"

@torch.no_grad()
def predict(p):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,1)
    return {"id":int(t.indices[0]),"tok":tok.decode([int(t.indices[0])])}
def first_tok(s): return tok(" "+s,add_special_tokens=False)["input_ids"][0]
def single_tok(s): return len(tok(" "+s,add_special_tokens=False)["input_ids"])==1
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower(); return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def snap(): npd=dict(model.named_parameters()); return {layer: npd[WN(layer)].detach().clone() for layer in L}
def restore(s):
    with torch.no_grad():
        npd=dict(model.named_parameters())
        for layer in L: npd[WN(layer)][...]=s[layer]
def locpct(post,pre,pl): return 0.0  # unused here

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

# ---------- INERTNESS GATE (LAW#5) ----------
print("\n=== INERTNESS GATE: harness MEMIT-mode vs engine apply_memit ===", flush=True)
e="France"; cons=TMPL["capital"].format(e); tgt=first_tok("Cairo"); probes=[TMPL[a].format(e) for a in ["currency","continent","language"]]
import torch as _t
@torch.no_grad()
def _distp(p):
    ids=tok(p,return_tensors="pt").to("cuda"); return torch.softmax(model(**ids).logits[0,-1].float(),dim=-1).cpu()
pre_d={p:_distp(p) for p in [cons]+probes}; s0=snap()
with contextlib.redirect_stdout(io.StringIO()): apply_memit_to_model(model,tok,req(e,"capital","Cairo"),hp,copy=False,return_orig_weights=False)
eng_p=float(_distp(cons)[tgt]); restore(s0)
with contextlib.redirect_stdout(io.StringIO()): my_edit(req(e,"capital","Cairo"),"memit")
my_p=float(_distp(cons)[tgt]); restore(s0)
ok=abs(eng_p-my_p)<0.05
print(f"  engine expr={eng_p:.4f} | harness-memit expr={my_p:.4f} | |Δ|={abs(eng_p-my_p):.4f} -> {'INERT ✓' if ok else 'NOT INERT ✗ HALT'}", flush=True)
if not ok: print("LAW#5 fail; HALT.", flush=True); sys.exit(1)

# ---------- build records (same screened pool as A0/A1) ----------
scr=json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json")); sel=scr["selected"]
ents=list(sel.keys()); edit_ents=ents[:N_ENTITIES]
native_ents=ents[N_ENTITIES:]          # ALL un-edited entities are native candidates
def assign_cf(entity_list, field):
    truths=[sel[e][field]["truth"] for e in entity_list]
    st=[t for t in truths if single_tok(t)]
    cf={}
    for i,e in enumerate(entity_list):
        j=(i+7)%len(st)
        while st[j].lower()==truths[i].lower(): j=(j+1)%len(st)
        cf[e]=st[j]
    return cf
CF={f:assign_cf(edit_ents,f) for f in FIELDS}
records=[]
for e in edit_ents:
    for f in FIELDS:
        records.append({"entity":e,"field":f,"truth":sel[e][f]["truth"],"cf":CF[f][e],
                        "prompt":TMPL[f].format(e),"cf_tok":first_tok(CF[f][e])})
print(f"\n{len(records)} edited records | {len(edit_ents)} edited entities | {len(native_ents)} native candidate entities", flush=True)

# ---------- BATCH joint solve (A1 path) ----------
print("\n=== BATCH WRITE (single joint solve, Genesis-style — the A1-clean path) ===", flush=True)
P=compute_P(); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
reqs=[req(r["entity"],r["field"],r["cf"])[0] for r in records]
my_edit(reqs,"alphaedit",P,cache)
expr=sum(predict(r["prompt"])["id"]==r["cf_tok"] for r in records)
print(f"  batch apply-time expression: {expr}/{len(records)} = {100*expr/len(records):.1f}%", flush=True)

# ---------- HF-fp16 reference predictions for EDITED + NATIVE probe sets ----------
edited_probes=[{"prompt":r["prompt"],"target":r["cf"],"truth":r["truth"],"entity":r["entity"],
                "field":r["field"],"kind":"edited"} for r in records]
native_probes=[]
for e in native_ents:
    for f in ["capital","language","continent"]:
        if f in sel[e]:
            native_probes.append({"prompt":TMPL[f].format(e),"target":sel[e][f]["truth"],"truth":sel[e][f]["truth"],
                                  "entity":e,"field":f,"kind":"native_country"})
for gp in GLOBAL_PROBES:
    native_probes.append({"prompt":gp,"target":None,"truth":None,"entity":None,"field":"global","kind":"native_global"})

# record HF-fp16 top-1 on the EDITED model (this is the reference the GGUF-fp16 must reproduce)
for pr in edited_probes+native_probes:
    pd=predict(pr["prompt"]); pr["hf_top1"]=pd["tok"]
    if pr["target"] is not None:
        pr["hf_match_target"]=correct(pd["tok"],pr["target"])
    else:
        pr["hf_match_target"]=None  # global: no fixed target; eligibility set by GGUF-fp16 self-consistency
print(f"  edited probes={len(edited_probes)} | native probes={len(native_probes)} "
      f"(country={sum(p['kind']=='native_country' for p in native_probes)}, global={len(GLOBAL_PROBES)})", flush=True)
print(f"  HF-fp16 edited target-match: {sum(bool(p['hf_match_target']) for p in edited_probes)}/{len(edited_probes)}", flush=True)
print(f"  HF-fp16 native-country target-match: {sum(bool(p['hf_match_target']) for p in native_probes if p['kind']=='native_country')}/{sum(p['kind']=='native_country' for p in native_probes)}", flush=True)

json.dump({"config":{"model":ID,"rev":REV,"band":L,"mom2_uw":hp.mom2_update_weight,"thresh":NULL_THRESH,
           "write_mode":"batch","n_edited":len(records)},
           "edited":edited_probes,"native":native_probes},
          open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json","w"),indent=2,default=str)
print("  wrote /workspace/configs/probes/b3_probes.json", flush=True)

# ---------- SAVE edited model (fp16 HF) for GGUF conversion ----------
print(f"\n=== SAVE edited model -> {SAVE_DIR} ===", flush=True)
os.makedirs(SAVE_DIR, exist_ok=True)
model.save_pretrained(SAVE_DIR, safe_serialization=True)
tok.save_pretrained(SAVE_DIR)
print("DONE b3_edit_and_save", flush=True)
