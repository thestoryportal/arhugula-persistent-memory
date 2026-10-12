#!/usr/bin/env python3
"""Route A projector gate v2 (Amendment 1 → advisor FIX-FIRST items). CPU/MPS projector maths only; NO edits.

Per band layer (one SVD), for the candidate per-layer thresholds AND a finer L8 grid:
  protection   mean per-key ‖P k‖/‖k‖ on 200 held-out Wikipedia articles' down_proj inputs        (bound ≤ 0.5)
  survival_A1  mean per-key ratio on the 24 A1 last-prompt-token keys + per-key spread + bootstrap 95% CI  (bound ≥ 0.2)
  survival_HO  the same on 24 HELD-OUT fictional subjects never used by any arm (key-level leakage check)
  survival_ARE the same on the keys AnyEdit actually writes at window_size=1: for each A7 item, the
               last prompt token AND every answer-token position but the last (question+answer inputs)
Writes experiments/c10k/runs/c10k_route_a/projector_gate_v2.json and saves P for the chosen per-layer thresholds."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

HELDOUT_FICTION = ["Brelquin", "Tavross", "Nimbrek", "Osvalden", "Kryllmoor", "Zandevek", "Ulthane", "Pymbrook",
                   "Dorvash", "Quillmere", "Vexthorn", "Molbray", "Stennick", "Harquill", "Jubrane", "Threxley",
                   "Calvoss", "Wrenmark", "Ildravon", "Sorbeck", "Fenwhistle", "Yarlmond", "Gruvane", "Eskavoy"]
PER_LAYER = {4: 0.01, 5: 0.02, 6: 0.02, 7: 0.02, 8: 0.03}      # Amendment 1 v2 D8: minimal departure from the shipped 0.02 in the direction that restores the failing bound (L4 protection, L8 survival)
GRID = {4: [0.005, 0.01, 0.02], 8: [0.02, 0.025, 0.03, 0.035]}   # fixed before this run
import torch as _t; KEYS_DTYPE = _t.float32   # Amendment 2: keys from the fp32 model, the dtype the run stage edits in (run 2 used fp16: projector_gate_v2_run2_fp16keys.json)

def ratios(K, Us):
    import torch
    r = (K @ Us).norm(dim=1) / K.norm(dim=1); return r

def summarize(r, boots=2000, seed=0, K=None, Us=None):
    import torch
    g = torch.Generator().manual_seed(seed); n = r.numel()
    means = torch.stack([r[torch.randint(0, n, (n,), generator=g)].mean() for _ in range(boots)])
    return {"mean": round(float(r.mean()), 4), "median": round(float(r.median()), 4), "min": round(float(r.min()), 4), "max": round(float(r.max()), 4),
            "frac_below_0.2": round(float((r < 0.2).float().mean()), 3), "aggregate_ratio_of_mean_norms": (round(float((K @ Us).norm(dim=1).mean() / K.norm(dim=1).mean()), 4) if K is not None else None), "boot95": [round(float(means.quantile(0.025)), 4), round(float(means.quantile(0.975)), 4)], "n": n}

def are_window_keys(model, tok, layer_name, dev, items):
    """Keys at the positions AnyEdit (window_size=1) writes: last prompt token + each answer-token position except the last."""
    import torch
    from util import nethook
    out = []
    with torch.no_grad():
        for q, ans in items:
            qa = tok(q + ans, return_tensors="pt").to(dev); nq = len(L.ids(tok, q)); na = len(L.ids(tok, ans))
            with nethook.Trace(model, layer_name, retain_input=True, retain_output=False, stop=True) as tr: model(**qa)
            k = tr.input[0] if tr.input.dim() == 3 else tr.input
            pos = [nq - 1] + [nq + j for j in range(na - 1)]
            out.append(k[pos].float().cpu())
    return torch.cat(out, 0)

def main():
    import torch
    dev = L.resolve_device(); tok, model = L.load_model(dev, KEYS_DTYPE)
    HP, M, _ = L.import_upstream("AlphaEdit_ARE"); hp = HP.from_json(f"{L.LLMDB_ROOT}/code/configs/hparams/anyedit_alphaedit_are_qwen25_3b.json")
    fiction, arms = L.build_stimuli(tok)
    assert not set(HELDOUT_FICTION) & set(fiction) and not set(HELDOUT_FICTION) & set(L.COINED_HEAD)
    from datasets import load_dataset
    wiki = load_dataset("wikimedia/wikipedia", "20231101.en")["train"]; texts = [wiki[i]["text"][:600] for i in range(1_000_000, 1_000_200)]
    a1 = [L.CANON.format(s) for s in fiction]; ho = [L.CANON.format(s) for s in HELDOUT_FICTION]
    a7_items = [(L.CANON.format(s), " " + arms["A7_coined_coined"][s]) for s in fiction]
    rep = {"keys_dtype": str(KEYS_DTYPE).split(".")[-1], "per_layer_thresholds": PER_LAYER, "bounds": {"protection_max": 0.5, "survival_min": 0.2}, "statistic": "mean of per-key ratios (prereg D4 wording); aggregate ratio-of-mean-norms also reported", "layers": {}, "grid": GRID}
    Ps = []
    for l in hp.layers:
        name = hp.rewrite_module_tmp.format(l); t = time.time()
        U, S, _ = torch.linalg.svd(L.normalised_cov(name), full_matrices=False)
        Kw = L.layer_inputs(model, tok, texts, name, dev); Ka1 = L.layer_inputs(model, tok, a1, name, dev, "last")
        Kho = L.layer_inputs(model, tok, ho, name, dev, "last"); Kare = are_window_keys(model, tok, name, dev, a7_items)
        grid = GRID.get(l, [PER_LAYER[l]]); rows = {}
        for th in grid:
            idx = (S < th).nonzero(as_tuple=True)[0]; Us = U[:, idx]
            rows[str(th)] = {"dims": int(idx.numel()), "protection_wiki": summarize(ratios(Kw, Us), K=Kw, Us=Us), "survival_A1": summarize(ratios(Ka1, Us), K=Ka1, Us=Us),
                             "survival_heldout": summarize(ratios(Kho, Us), K=Kho, Us=Us), "survival_ARE_A7_positions": summarize(ratios(Kare, Us), K=Kare, Us=Us)}
        th = PER_LAYER[l]; idx = (S < th).nonzero(as_tuple=True)[0]; Ps.append(U[:, idx] @ U[:, idx].T)
        r = rows[str(th)]
        ok = (r["protection_wiki"]["mean"] <= 0.5 and r["survival_A1"]["mean"] >= 0.2 and r["survival_heldout"]["mean"] >= 0.2
              and r["survival_A1"]["boot95"][0] >= 0.2 and r["survival_ARE_A7_positions"]["mean"] >= 0.2)
        rep["layers"][str(l)] = {"chosen": th, "rows": rows, "chosen_ok": ok, "seconds": round(time.time() - t), "n_keys": {"wiki": int(Kw.shape[0]), "A1": int(Ka1.shape[0]), "heldout": int(Kho.shape[0]), "ARE": int(Kare.shape[0])}}
        print(f"L{l} @{th}: dims={r['dims']} prot={r['protection_wiki']['mean']:.3f} A1={r['survival_A1']['mean']:.3f} ci={r['survival_A1']['boot95']} HO={r['survival_heldout']['mean']:.3f} ARE={r['survival_ARE_A7_positions']['mean']:.3f} -> {'OK' if ok else 'FAIL'}", flush=True)
        if l in GRID:
            for g, rr in rows.items(): print(f"   L{l} grid {g}: dims={rr['dims']} prot={rr['protection_wiki']['mean']:.3f} A1={rr['survival_A1']['mean']:.3f} HO={rr['survival_heldout']['mean']:.3f} ARE={rr['survival_ARE_A7_positions']['mean']:.3f}", flush=True)
    rep["gate_ok"] = all(v["chosen_ok"] for v in rep["layers"].values())
    tag = "-".join(str(PER_LAYER[l]) for l in hp.layers)
    torch.save(torch.stack(Ps, 0), f"{L.LLMDB_ROOT}/logs/c10k_route_a_P_perlayer_{tag}.pt"); rep["P_file"] = f"logs/c10k_route_a_P_perlayer_{tag}.pt"; import hashlib; rep["P_sha256"] = hashlib.sha256(open(f"{L.LLMDB_ROOT}/{rep['P_file']}", "rb").read()).hexdigest()
    json.dump(rep, open(f"{L.OUTDIR}/projector_gate_v2.json", "w"), indent=1); print("gate v2:", "OK" if rep["gate_ok"] else "FAIL", "| P saved:", rep["P_file"]); return 0 if rep["gate_ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
