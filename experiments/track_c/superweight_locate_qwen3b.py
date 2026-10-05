#!/usr/bin/env python3
"""Locate super-weight candidates in Qwen2.5-3B (Yu et al. 2024, arXiv 2411.07191 §3): one data-free forward pass; per layer,
the max |activation| at the input and output of mlp.down_proj. A super weight sits at [row = output spike channel,
col = input spike channel] in the layer where both spike. Read-only; no weights changed. Writes results/superweight_qwen3b.json."""
import os, sys, json, torch
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"; os.environ.setdefault("HF_HUB_OFFLINE", "1")
from transformers import AutoModelForCausalLM, AutoTokenizer
ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
dev = "mps" if torch.backends.mps.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(ID, revision=REV)
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map=dev).eval()
rec = {}
def hook(li):
    def f(mod, inp, out):
        x = inp[0][0].float(); y = out[0].float()                      # [seq, inter], [seq, hidden]
        xi = x.abs().max(); yi = y.abs().max()
        xpos = divmod(int(x.abs().argmax()), x.shape[1]); ypos = divmod(int(y.abs().argmax()), y.shape[1])
        rec[li] = {"in_max": float(xi), "in_tok": xpos[0], "in_ch": xpos[1], "out_max": float(yi), "out_tok": ypos[0], "out_ch": ypos[1]}
    return f
hs = [l.mlp.down_proj.register_forward_hook(hook(i)) for i, l in enumerate(model.model.layers)]
prompt = sys.argv[1] if len(sys.argv) > 1 else "The capital of France is the city of"
with torch.no_grad(): model(**tok(prompt, return_tensors="pt").to(dev))
for h in hs: h.remove()
toks = tok.convert_ids_to_tokens(tok(prompt)["input_ids"])
med_in = sorted(r["in_max"] for r in rec.values())[len(rec) // 2]; med_out = sorted(r["out_max"] for r in rec.values())[len(rec) // 2]
cands = []
for li, r in rec.items():
    if r["out_max"] > 20 * med_out and r["in_max"] > 20 * med_in:
        w = model.model.layers[li].mlp.down_proj.weight[r["out_ch"], r["in_ch"]].item()
        cands.append({"layer": li, "row_out_ch": r["out_ch"], "col_in_ch": r["in_ch"], "weight": w, "in_max": r["in_max"], "out_max": r["out_max"], "token": toks[r["out_tok"]], "token_pos": r["out_tok"]})
out = {"model": ID, "revision": REV, "prompt": prompt, "n_layers": len(rec), "median_in_max": med_in, "median_out_max": med_out,
       "per_layer": rec, "candidates_20x_median": cands}
json.dump(out, open(f"{LLMDB_ROOT}/results/superweight_qwen3b.json", "w"), indent=1)
print(f"layers={len(rec)} median in/out max = {med_in:.1f} / {med_out:.1f}")
for li in sorted(rec): r = rec[li]; print(f"L{li:2d} in_max {r['in_max']:9.1f} @tok{r['in_tok']} ch{r['in_ch']:5d} | out_max {r['out_max']:9.1f} @tok{r['out_tok']} ch{r['out_ch']:5d}")
print("candidates (>20x median in AND out):", json.dumps(cands, indent=1))
