#!/usr/bin/env python3
"""D-C10k-keying-ablation dry run v2 (prereg v3): for the per-country subject-string design
   K3/K4 request: prompt "The capital of {}", subject "<country> is the city of"
print, for ALL 24 fictional subjects, the token index and decoded token the vendored engine's subject_last path keys on, under the
engine's REAL context templates (get_context_templates(model, tok), as c10e uses) and under the identity template; plus the KL
prompt the engine will build ("<subject> is a") and its keyed index. Validity criteria (pre-registered): keyed token decodes to " of"
and is the final prompt token for every subject under every template; the KL keyed index is never 0. Also prints the K1 control
(subject = country) for comparison. Run from code/memit/vendor (the engine reads globals.yml from cwd)."""
import os, sys, json
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, f"{LLMDB_ROOT}/code/memit/vendor"); sys.path.insert(0, f"{LLMDB_ROOT}/code/lab/track_c")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from rome import repr_tools
from memit.memit_main import get_context_templates
ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True)
dev = "mps" if torch.backends.mps.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, local_files_only=True).to(dev).eval()
ctx = get_context_templates(model, tok)          # list of lists, as the engine composes: context.format(prompt)
templates = [t for group in ctx for t in group]
import importlib.util
spec = importlib.util.spec_from_file_location("c10e", f"{LLMDB_ROOT}/code/lab/track_c/c10e_bandknob.py")
FICTION = [l.split('"')[1] for l in open(f"{LLMDB_ROOT}/code/lab/track_c/c10e_bandknob.py") if l.strip().startswith('"') and l.strip().endswith('",')][:24]
if len(FICTION) < 24:
    import re; src = open(f"{LLMDB_ROOT}/code/lab/track_c/c10e_bandknob.py").read(); m = re.search(r"FICTION = \[(.*?)\]", src, re.S); FICTION = re.findall(r'"([^"]+)"', m.group(1))[:24]
out = {"templates": templates, "subjects": {}}; bad = []
for c in FICTION:
    subj = f"{c} is the city of"; prompt = "The capital of {}"; rec = {}
    for name, tmpl in [("identity", "{}")] + [(f"ctx{i}", t) for i, t in enumerate(templates)]:
        full = tmpl.format(prompt)                                                   # engine: context.format(request["prompt"])
        idx = repr_tools.get_words_idxs_in_templates(tok, [full], [subj], "last")[0][0]
        ids = tok(full.format(subj))["input_ids"]; dec = tok.decode(ids[idx]); ok = dec.strip() == "of" and idx == len(ids) - 1
        rec[name] = {"idx": idx, "n": len(ids), "decoded": dec, "ok": ok}
        if not ok: bad.append((c, name, idx, len(ids), dec))
    kl_idx = repr_tools.get_words_idxs_in_templates(tok, ["{} is a"], [subj], "last")[0][0]; rec["kl_keyed_index"] = kl_idx
    if kl_idx == 0: bad.append((c, "kl", kl_idx, 0, ""))
    ctl_idx = repr_tools.get_words_idxs_in_templates(tok, ["The capital of {} is the city of"], [c], "last")[0][0]
    ctl_ids = tok(f"The capital of {c} is the city of")["input_ids"]; rec["K1_control"] = {"idx": ctl_idx, "decoded": tok.decode(ctl_ids[ctl_idx])}
    out["subjects"][c] = rec
    print(f"{c:10s} identity idx={rec['identity']['idx']}/{rec['identity']['n']-1} {rec['identity']['decoded']!r} | ctx ok={all(v['ok'] for k, v in rec.items() if k.startswith('ctx'))} | KL idx={kl_idx} | K1 keyed={rec['K1_control']['decoded']!r}", flush=True)
out["n_templates"] = len(templates); out["valid"] = not bad; out["bad"] = bad
os.makedirs(f"{LLMDB_ROOT}/experiments/c10k/runs/c10k_keying_ablation", exist_ok=True); json.dump(out, open(f"{LLMDB_ROOT}/experiments/c10k/runs/c10k_keying_ablation/dryrun_keyed_token.json", "w"), indent=1)
print(f"templates={len(templates)} subjects={len(FICTION)} ->", "VALID" if not bad else f"INVALID {bad[:5]}"); sys.exit(0 if not bad else 1)
