#!/usr/bin/env python3
"""P-8 — device neutrality for the MEMIT science path (compute_z, memit_main, layer_stats).

Every substitution is anchored on the exact current text and asserted to occur exactly
once, so a drifted engine fails loudly rather than being half-patched. Idempotent: a second
run finds zero anchors and reports ALREADY APPLIED.
"""
from pathlib import Path
import sys

E = Path("memit_dry_run/memit")
edits = {
 "memit/compute_z.py": [
  # one device resolution per call, right after lm_b is resolved
  ('        lm_b = next(model.parameters()).new_zeros(model.config.vocab_size)\n\n    print("Computing right vector (v)")\n',
   '        lm_b = next(model.parameters()).new_zeros(model.config.vocab_size)\n    dev = device_of(model)  # P-8\n\n    print("Computing right vector (v)")\n'),
  ('    target_ids = tok(request["target_new"]["str"], return_tensors="pt").to("cuda")[\n',
   '    target_ids = tok(request["target_new"]["str"], return_tensors="pt").to(dev)[\n'),
  ('        padding=True,\n    ).to("cuda")\n', '        padding=True,\n    ).to(dev)\n'),
  ('    rewriting_targets = torch.tensor(-100, device="cuda").repeat(\n',
   '    rewriting_targets = torch.tensor(-100, device=dev).repeat(\n'),
  ("model.config.n_embd),), requires_grad=True, device=\"cuda\")\n",
   "model.config.n_embd),), requires_grad=True, device=dev)\n"),
  ("from util import nethook\n", "from util import nethook\nfrom util.device import device_of  # P-8\n"),
 ],
 "memit/memit_main.py": [
  ("from util import nethook\n", "from util import nethook\nfrom util.device import device_of, empty_cache  # P-8\n"),
  ('    with torch.no_grad():\n        for w_name, (key_mat, val_mat) in deltas.items():\n            key_mat, val_mat = key_mat.to("cuda"), val_mat.to("cuda")\n',
   '    dev = device_of(model)  # P-8\n    with torch.no_grad():\n        for w_name, (key_mat, val_mat) in deltas.items():\n            key_mat, val_mat = key_mat.to(dev), val_mat.to(dev)\n'),
  ('                z_list.append(torch.from_numpy(data["v_star"]).to("cuda"))\n',
   '                z_list.append(torch.from_numpy(data["v_star"]).to(device_of(model)))  # P-8\n'),
  # the double-precision solve already runs on CPU (S2.31); P-8 moves the operands there BEFORE
  # the float64 cast, because MPS cannot represent float64 at all.
  ('        layer_ks, targets = (\n            layer_ks.double(),\n            targets.double(),\n        )\n',
   '        layer_ks, targets = (  # P-8: to CPU first — MPS has no float64\n            layer_ks.cpu().double(),\n            targets.cpu().double(),\n        )\n'),
  ('            weights[weight_name][...] = weights_copy[weight_name] + upd_matrix.float()\n',
   '            weights[weight_name][...] = weights_copy[weight_name] + upd_matrix.float().to(weights_copy[weight_name].device)  # P-8\n'),
  ('            del x\n        torch.cuda.empty_cache()\n', '            del x\n        empty_cache(device_of(model))  # P-8\n'),
  ('        torch.inverse(COV_CACHE[key].to("cuda")) if inv else COV_CACHE[key].to("cuda")\n',
   '        torch.inverse(COV_CACHE[key].to(device_of(model))) if inv else COV_CACHE[key].to(device_of(model))  # P-8\n'),
 ],
 "rome/layer_stats.py": [
  ('                batch = dict_to_(batch, "cuda")\n', '                batch = dict_to_(batch, next(model.parameters()).device)  # P-8\n'),
 ],
}

applied = 0
for rel, subs in edits.items():
    p = E / rel; s = p.read_text(encoding="utf-8")
    for old, new in subs:
        n = s.count(old); m = s.count(new)
        if n == 0 and m == 1:
            continue  # already applied
        assert n == 1, f"{rel}: anchor found {n}x: {old[:70]!r}"
        s = s.replace(old, new); applied += 1
    p.write_text(s, encoding="utf-8")
print("P-8:", "APPLIED" if applied else "ALREADY APPLIED", f"({applied} substitutions)")
sys.exit(0)
