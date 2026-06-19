import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""A7 (+NEW-1): Is LARQL's Qwen2.5 garbage CAUSED by dropped attention bias?
Causal test in the reference model: zero q/k/v attn biases in HF Qwen2.5-3B (edited),
probe the SAME prompts LARQL garbled, compare top-1 token-for-token to LARQL's output.
 - bias-zeroed HF -> garbage matching LARQL  => bias is the WHOLE cause (attribution proven)
 - bias-zeroed HF -> garbage but DIFFERENT   => 2nd bug (decompile) layered on bias
 - bias-zeroed HF -> still correct           => bias is NOT the cause; attribution WRONG
"""
import os, torch
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="1"
from transformers import AutoModelForCausalLM, AutoTokenizer

SRC=f"{LLMDB_ROOT}/b3_edited_qwen3b"   # the edited 3B (what the q4km GGUF/vindex came from)
tok=AutoTokenizer.from_pretrained(SRC)
model=AutoModelForCausalLM.from_pretrained(SRC, torch_dtype=torch.float16, device_map="cuda").eval()

# exact prompts LARQL garbled, with LARQL's top-1 for comparison
PROBES=[
 ("The official language of Algeria is", "Arabic(native)", "iros"),
 ("The capital of Japan is the city of", "(native/edited?)", ".LA"),
 ("Water is composed of hydrogen and",   "oxygen(native)",  "rio"),
 ("The capital of France is the city of", "Oslo(edited)",    "澎"),
]

@torch.no_grad()
def top1(p):
    ids=tok(p,return_tensors="pt").to("cuda")
    lg=model(**ids).logits[0,-1]
    return tok.decode([int(lg.argmax())])

def run(tag):
    print(f"\n--- {tag} ---", flush=True)
    out={}
    for p,exp,larql in PROBES:
        t=top1(p); out[p]=t
        print(f"  '{p[:42]:42}' -> top1='{t}'  (expect {exp}; LARQL='{larql}')", flush=True)
    return out

with_bias=run("WITH bias (reference — should be correct/edited)")

# zero ALL q/k/v attention biases (Qwen2.5 = Qwen2 arch: q/k/v have bias, o_proj none)
nz=0
with torch.no_grad():
    for n,prm in model.named_parameters():
        if ("self_attn" in n) and n.endswith(".bias"):
            prm.zero_(); nz+=1
print(f"\nzeroed {nz} attention bias tensors", flush=True)

no_bias=run("BIAS ZEROED (the causal test)")

# verdict
larql={p:l for p,_,l in PROBES}
changed=sum(with_bias[p]!=no_bias[p] for p,_,_ in PROBES)
matches_larql=sum(no_bias[p].strip()==larql[p].strip() for p,_,_ in PROBES)
print(f"\n=== VERDICT ===", flush=True)
print(f"  prompts where zeroing bias CHANGED top-1: {changed}/{len(PROBES)}", flush=True)
print(f"  bias-zeroed top-1 EXACTLY matches LARQL garbage: {matches_larql}/{len(PROBES)}", flush=True)
print(f"  -> if changed~=all & still-sensible: bias matters but recoverable", flush=True)
print(f"  -> if changed~=all & garbage: bias-drop is a sufficient cause", flush=True)
print(f"  -> if matches_larql high: bias is the WHOLE story (no 2nd bug)", flush=True)
print(f"  -> if changed~=0: bias is NOT the cause -> E1 attribution WRONG", flush=True)
print("A7_DONE", flush=True)
