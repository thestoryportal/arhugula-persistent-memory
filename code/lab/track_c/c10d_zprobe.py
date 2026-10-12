import os, sys, io, contextlib, json, re
LLMDB_ROOT=os.environ.get("LLMDB_ROOT","/workspace")
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z
from memit.memit_main import get_context_templates
# ----------------------------------------------------------------------------
# C10d Z-PROBE (advisor cheap-check): is canon_full=37-46% on realistic coined
# values a compute_z UNDER-OPTIMIZATION (more steps help -> recipe knob) or a
# fundamental multi-token z-capacity wall (steps don't help -> AnyEdit-grade)?
# compute_z needs NO covariance -> fast. Read converged full-target prob exp(-nll)
# at 25 (baseline) vs 100 grad steps, single/2-tok controls vs realistic coined.
# ----------------------------------------------------------------------------
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")
tok=AutoTokenizer.from_pretrained(ID,revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID,revision=REV,torch_dtype=torch.float16,device_map="cuda").eval()
CANON="The capital of {} is the city of"; zl=hp.layers[-1]
ctx=get_context_templates(model,tok)
def r(subj,targ): return {"prompt":CANON,"subject":subj,"target_new":{"str":" "+targ}}
def converged_prob(subj,targ,steps):
    hp.v_num_grad_steps=steps
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        compute_z(model,tok,r(subj,targ),hp,zl,ctx)
    # last printed "... <full-target-prob>" from compute_z line 158-160
    probs=re.findall(r"avg prob of \[.*?\]\s+([0-9.eE+-]+)", buf.getvalue())
    return float(probs[-1]) if probs else None, buf.getvalue().strip().splitlines()[-3:]
# representative items from the actual run (same subjects/values)
CASES=[("A1_single","Zorbland","Beirut"),
       ("A3_incoh2","Zorbland","Amsterdam Ankara"),
       ("A6_realNoun","Zorbland","Qorvex City"),
       ("A6_realNoun","Vythorn","Skorn Falls"),
       ("A7_coined","Zorbland","Vindex Vask"),
       ("A7_coined","Vythorn","Vythorn Stavik")]
print("name | value | ntok | prob@25 | prob@100", flush=True)
out=[]
for name,subj,val in CASES:
    nt=len(tok(" "+val,add_special_tokens=False)["input_ids"])
    p25,_=converged_prob(subj,val,25); p100,_=converged_prob(subj,val,100)
    print(f"{name:11} | {val:18} | {nt} | {p25} | {p100}", flush=True)
    out.append({"name":name,"subj":subj,"val":val,"ntok":nt,"prob_25":p25,"prob_100":p100})
json.dump(out,open(f"{LLMDB_ROOT}/results/c10d_zprobe.json","w"),indent=2)
print("ZPROBE_DONE", flush=True)
