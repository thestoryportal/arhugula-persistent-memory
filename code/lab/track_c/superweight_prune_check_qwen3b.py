#!/usr/bin/env python3
"""Confirm a super-weight candidate (Yu et al. 2024 §3.1 test): zero ONE scalar of mlp.down_proj in memory, measure mean NLL and
stopword probability on a few sentences, restore. Nothing is written to disk; the vendored engine is not involved.
Usage: superweight_prune_check_qwen3b.py <layer> <row> <col>"""
import os, sys, json, math, torch
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"; os.environ.setdefault("HF_HUB_OFFLINE", "1")
from transformers import AutoModelForCausalLM, AutoTokenizer
ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
L, R, C = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
dev = "mps" if torch.backends.mps.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(ID, revision=REV)
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map=dev).eval()
TEXTS = ["The capital of France is the city of Paris, which lies on the Seine and has been the seat of government for centuries.",
         "Photosynthesis converts light energy into chemical energy, producing oxygen as a by-product that most animals depend on.",
         "In 1969 the Apollo 11 mission landed two astronauts on the Moon and returned them safely to Earth eight days after launch.",
         "A binary search tree keeps its keys in sorted order so that lookup, insertion and deletion take logarithmic time on average."]
STOP = [" the", ".", ","]
@torch.no_grad()
def measure():
    nll = 0.0; n = 0; stop = {s: 0.0 for s in STOP}; m = 0
    for t in TEXTS:
        ids = tok(t, return_tensors="pt").to(dev)["input_ids"]; lg = model(ids).logits[0].float()
        lp = torch.log_softmax(lg[:-1], -1); nll += -lp.gather(1, ids[0, 1:, None]).sum().item(); n += ids.shape[1] - 1
        pr = torch.softmax(lg, -1).mean(0)
        for s in STOP: stop[s] += pr[tok(s)["input_ids"][0]].item()
        m += 1
    return {"mean_nll": nll / n, "ppl": math.exp(nll / n), "mean_stopword_prob": {s: v / m for s, v in stop.items()}}
W = model.model.layers[L].mlp.down_proj.weight
orig = W[R, C].item(); before = measure()
with torch.no_grad(): W[R, C] = 0.0
after = measure()
with torch.no_grad(): W[R, C] = orig
restored = measure()
out = {"layer": L, "row": R, "col": C, "weight": orig, "before": before, "pruned": after, "restored": restored}
print(json.dumps(out, indent=1)); json.dump(out, open(f"{LLMDB_ROOT}/results/superweight_qwen3b_prune_check.json", "w"), indent=1)
