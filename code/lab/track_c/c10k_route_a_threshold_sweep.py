#!/usr/bin/env python3
"""Route A projector-threshold sensitivity DIAGNOSTIC (prereg §2 D4: run after an INVALID-projector gate; not a substitute).
One SVD per band layer; for each candidate nullspace_threshold recompute the two functional ratios on the SAME
calibration keys the gate used (200 held-out Wikipedia articles; the 24 A1 edit keys). No edits are run.
Output: experiments/c10k/runs/c10k_route_a/projector_threshold_sweep.json"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

THRESHOLDS = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1]

def main():
    import torch
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float16)
    HP, M, _ = L.import_upstream("AlphaEdit_ARE"); hp = HP.from_json(f"{L.LLMDB_ROOT}/code/configs/hparams/anyedit_alphaedit_are_qwen25_3b.json")
    fiction, arms = L.build_stimuli(tok)
    from datasets import load_dataset
    wiki = load_dataset("wikimedia/wikipedia", "20231101.en")["train"]; texts = [wiki[i]["text"][:600] for i in range(1_000_000, 1_000_200)]
    a1_prompts = [L.CANON.format(s) for s in fiction]
    out = {"thresholds": THRESHOLDS, "bounds": {"protection_max": 0.5, "survival_min": 0.2}, "layers": {}}
    for l in hp.layers:
        name = hp.rewrite_module_tmp.format(l); t = time.time()
        cov = L.normalised_cov(name); U, S, _ = torch.linalg.svd(cov, full_matrices=False)
        Kw = L.layer_inputs(model, tok, texts, name, dev); Ke = L.layer_inputs(model, tok, a1_prompts, name, dev, "last")
        kw, ke = Kw.norm(dim=1).mean(), Ke.norm(dim=1).mean(); rows = {}
        for th in THRESHOLDS:
            idx = (S < th).nonzero(as_tuple=True)[0]; Us = U[:, idx]
            prot = float((Kw @ Us).norm(dim=1).mean() / kw); surv = float((Ke @ Us).norm(dim=1).mean() / ke)   # ‖P k‖ = ‖Usᵀ k‖ for an orthogonal projector
            rows[str(th)] = {"dims": int(idx.numel()), "protection": round(prot, 4), "survival": round(surv, 4), "both_ok": prot <= 0.5 and surv >= 0.2}
        out["layers"][str(l)] = {"rows": rows, "singular_min": float(S.min()), "singular_max": float(S.max()), "seconds": round(time.time() - t)}
        print(f"L{l}: " + " | ".join(f"{th}: d={r['dims']} p={r['protection']:.3f} s={r['survival']:.3f}{'*' if r['both_ok'] else ''}" for th, r in rows.items()), flush=True)
    out["thresholds_passing_all_layers"] = [th for th in THRESHOLDS if all(v["rows"][str(th)]["both_ok"] for v in out["layers"].values())]
    json.dump(out, open(f"{L.OUTDIR}/projector_threshold_sweep.json", "w"), indent=1)
    print("thresholds passing both bounds on all layers:", out["thresholds_passing_all_layers"]); return 0

if __name__ == "__main__":
    sys.exit(main())
