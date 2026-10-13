#!/usr/bin/env python3
"""D-C10k-keying-ablation z-probe (advisor FIX-FIRST on the result, item 2): does the engine's compute_z reach the target at the
keyed token for K3-style requests (subject '<country> is the city of', keyed at the final ' of', KL prompt '<subject> is a')
as it does for K1-style requests (subject = country, keyed at the subject's last token)? Runs the vendored engine's compute_z
(unmodified) on 3 subjects per style with the engine's own context templates and reports the final target probability at the
keyed position, the loss path, and the KL term. No weight edit. Run from code/memit/vendor. Writes experiments/c10k/runs/c10k_keying_ablation/zprobe.json."""
import os, sys, json, io, contextlib, re
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, f"{LLMDB_ROOT}/code/memit/vendor")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_main import get_context_templates
from memit.compute_z import compute_z
from memit.memit_hparams import MEMITHyperParams
ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True); dev = "mps" if torch.backends.mps.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, local_files_only=True).to(dev).eval()
hp = MEMITHyperParams.from_json(f"{LLMDB_ROOT}/code/configs/hparams/qwen25_3b_memit_hparams.json"); ctx = get_context_templates(model, tok)
CANON = "The capital of {} is the city of"; items = [("Zorbland", "Beirut"), ("Quaxil", "Buenos"), ("Plurnak", "Damascus")]
def run(style, c, v):
    rq = {"prompt": CANON, "subject": c, "target_new": {"str": " " + v}} if style == "K1" else {"prompt": "The capital of {}", "subject": f"{c} is the city of", "target_new": {"str": " " + v}}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): z = compute_z(model, tok, rq, hp, hp.layers[-1], ctx)
    out = buf.getvalue(); losses = re.findall(r"loss ([\d.]+) = ([\d.]+) \+ ([\d.]+) \+ ([\d.]+) avg prob of \[.*?\] ([\d.]+)", out)
    first, last = losses[0], losses[-1]
    return {"style": style, "subject": c, "value": v, "steps": len(losses), "loss_first": float(first[0]), "loss_last": float(last[0]), "nll_last": float(last[1]), "kl_last": float(last[2]), "wd_last": float(last[3]),
            "target_prob_first": float(first[4]), "target_prob_last": float(last[4]), "z_norm": float(z.norm())}
res = [run(s, c, v) for s in ("K1", "K3") for c, v in items]
for r in res: print(f"{r['style']} {r['subject']:9s} steps={r['steps']} target_prob {r['target_prob_first']:.3f} -> {r['target_prob_last']:.3f} | loss {r['loss_first']:.3f} -> {r['loss_last']:.3f} (nll {r['nll_last']:.3f} kl {r['kl_last']:.3f}) |z|={r['z_norm']:.1f}", flush=True)
os.makedirs(f"{LLMDB_ROOT}/experiments/c10k/runs/c10k_keying_ablation", exist_ok=True); json.dump(res, open(f"{LLMDB_ROOT}/experiments/c10k/runs/c10k_keying_ablation/zprobe.json", "w"), indent=1); print("done")
