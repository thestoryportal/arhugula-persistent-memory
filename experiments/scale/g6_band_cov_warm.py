import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import get_cov
# Warm covariance caches for a MID-LATE band on Qwen2.5-3B (36 layers) to enable the BLUE/C15 band test
# (our [4-8] is early; C15 prescribes L15-25/32L ≈ L17-28/36L). 5-wide mid-late band [18-22] matches [4-8] width.
# Zero-regret: resolves the open CP3 C15 divergence regardless of which cross-entity fix we pursue. STANDING-AUTH.
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
hp=MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")
BAND=[18,19,20,21,22]
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()
print(f"warming cov for mid-late band {BAND} (dataset={hp.mom2_dataset} n={hp.mom2_n_samples})", flush=True)
for layer in BAND:
    name=hp.rewrite_module_tmp.format(layer)
    print(f"  computing cov L{layer} ({name}) ...", flush=True)
    get_cov(model,tok,name,hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype)
    print(f"  L{layer} cached.", flush=True)
print("DONE band cov warm", flush=True)
