#!/usr/bin/env python3
"""Program-side check, run once before the autoresearch loop (not copied into the sandbox).
1. Recipe equivalence: for each arm, the harness's my_edit and edit.py's baseline apply_edit must change the same tensors to
   bitwise-identical values, from identical projectors.
2. Scorer equivalence: the harness's own run_recipe and prepare.py's separate scorer, given the my_edit weights, must report
   exactly the same counts and locality values.
3. Seed: whether SEED reproduces the engine's context templates across processes (this process vs the scorer's).
Usage: $PY experiments/track_c/autoresearch_c10/check_equivalence.py
       → writes results/autoresearch_c10_equivalence.json (+ the scorer's record in results/autoresearch_c10_equivalence_run/), prints PASS/FAIL.
"""
import os, sys, json, time, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prepare as PR          # seeded; loads the model; captures the unedited weights
import edit as E              # the baseline recipe (projectors computed at import)
import torch
H = PR.H

out = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
hp = PR.MEMITHyperParams.from_json(PR.BASE_HPARAMS)
P_h = H.compute_P(hp)
out["projectors_equal"] = all(torch.equal(a, b) for a, b in zip(P_h, E.P)) and len(P_h) == len(E.P)

recipe, saved = {}, {}
for arm in PR.ARM_NAMES:
    PR._restore_base()
    cache = [torch.zeros(P_h[0].shape[0], P_h[0].shape[0]) for _ in hp.layers]
    H.my_edit(hp, [PR.request(s, v) for s, v in PR.facts(arm)], P_h, cache)
    w = PR._weights(); names_h = PR._changed()
    A = {n: w[n].detach().clone() for n in names_h}
    PR._restore_base()
    E.apply_edit(PR.facts(arm))
    w = PR._weights(); names_e = PR._changed()
    recipe[arm] = {"changed_harness": names_h, "changed_edit_py": names_e,
                   "bitwise_equal": names_h == names_e and all(torch.equal(A[n], w[n]) for n in names_h)}
    saved[arm] = {n: t.cpu() for n, t in A.items()}
PR._restore_base()
out["recipe"] = recipe

harness = H.run_recipe("baseline", PR.BASE_HPARAMS)   # the harness's own measurement path (my_edit, same templates)
PR._restore_base()

run_dir = f"{PR.PROGRAM_ROOT}/results/autoresearch_c10_equivalence_run"
os.makedirs(run_dir, exist_ok=True)
for arm in PR.ARM_NAMES:
    torch.save(saved[arm], f"{run_dir}/{arm}.pt")
json.dump({"commit": "equivalence", "edit_seconds": {a: 0.0 for a in PR.ARM_NAMES}, "setup_seconds": 0.0,
           "changed": {a: list(saved[a]) for a in PR.ARM_NAMES}}, open(f"{run_dir}/edits.json", "w"))
r = subprocess.run([PR.PYTHON, f"{HERE}/prepare.py", "--score", run_dir], capture_output=True, text=True)
out["scorer_exit"] = r.returncode
out["scorer_tail"] = r.stdout[-1500:] + r.stderr[-1500:]
score = json.load(open(f"{run_dir}/score.json")) if r.returncode == 0 else None

cmp = {}
if score:
    for arm in PR.ARM_NAMES:
        h, s = harness["arms"][arm], score["arms"][arm]
        for k in ("para_full_n", "canon_full_n", "para_first_n", "para_string_n", "locality_described_as"):
            cmp[f"{arm}.{k}"] = [h[k], s[k], h[k] == s[k]]
        for k in ("L1_flipped_to_edited_value", "L3_top1_agree", "generic_ppl_post", "L3_mean_kl"):
            cmp[f"{arm}.{k}"] = [h["locality_axes"][k], s["locality_axes"][k], h["locality_axes"][k] == s["locality_axes"][k]]
out["scorer_vs_run_recipe"] = cmp
templates = PR.get_context_templates(PR.model, PR.tok)
out["templates_sha_this_process"] = hashlib.sha256(json.dumps(templates).encode()).hexdigest()[:12]
out["templates_sha_scorer"] = score["gates"]["templates_sha"] if score else None
out["law5_harness"] = harness.get("law5_gate")

out["seed_reproduces_templates"] = out["templates_sha_this_process"] == out["templates_sha_scorer"]
out["saved_sha256"] = score.get("saved_sha256") if score else None
out["source_sha256"] = {f: hashlib.sha256(open(p, "rb").read()).hexdigest()
                        for f, p in (("prepare.py", f"{HERE}/prepare.py"), ("edit.py", f"{HERE}/edit.py"), ("harness", PR.HARNESS))}
ok = (out["projectors_equal"] and all(v["bitwise_equal"] for v in recipe.values()) and score is not None and bool(cmp)
      and all(v[2] for v in cmp.values()) and out["seed_reproduces_templates"] and bool(out["saved_sha256"]))
out["verdict"] = "PASS" if ok else "FAIL"
dest = f"{PR.PROGRAM_ROOT}/results/autoresearch_c10_equivalence.json"
json.dump(out, open(dest, "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ("verdict", "projectors_equal", "seed_reproduces_templates", "scorer_exit")}, indent=1))
print({a: v["bitwise_equal"] for a, v in recipe.items()})
print({k: v for k, v in cmp.items() if not v[2]} or "scorer == run_recipe on every compared field")
print("wrote", dest)
