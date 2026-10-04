#!/usr/bin/env python3
"""Route A result-review item (advisor v2, F6 mechanism): pure linear algebra on the saved covariance and the module's own A1 keys.
For each band layer, the single-key realised fraction diag(K^T A^-1 K) for
   A1 = 15000*C + Kp Kp^T + K K^T   (memit_ARE as shipped)
   A2 = 15000*C + K K^T             (drop the same-sequence preservation term)
   A3 =  5000*C + K K^T             (the program's own MEMIT weight, no Kp)
   A4 =  5000*C + Kp Kp^T + K K^T
plus the key-energy fraction lying in C's eigen-directions where 15000*lambda < |k|^2 (the "tail" the over-regularisation argument needs).
All fp64 on CPU; no edit. Writes results/c10k_route_a/memit_ridge_diag.json."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

def main():
    import torch
    from util import nethook
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float32); fiction, arms = L.build_stimuli(tok)
    V = arms["A1_single"]; items = [(L.CANON.format(s), " " + V[s]) for s in fiction]; rep = {}
    for l in L.HP_LAYERS:
        name = L.HP_TMP.format(l); t = time.time(); ks, kp = [], []
        with torch.no_grad():
            for q, a in items:
                x = tok(q + a, return_tensors="pt").to(dev); nq, na = len(L.ids(tok, q)), len(L.ids(tok, a))
                with nethook.Trace(model, name, retain_input=True, retain_output=False, stop=True) as tr: model(**x)
                k = (tr.input[0] if tr.input.dim() == 3 else tr.input).cpu().double()
                pos = [nq - 1] + [nq + j for j in range(na - 1)]; other = [p for p in range(k.shape[0]) if p not in pos]
                ks.append(k[pos]); kp.append(k[other])
        K = torch.cat(ks, 0).T; Kp = torch.cat(kp, 0).T; C = L.normalised_cov(name).double(); I = torch.eye(K.shape[0], dtype=torch.float64)
        def gain(A):
            X = torch.linalg.solve(A, K); g = torch.diag(K.T @ X); return {"mean": round(float(g.mean()), 4), "min": round(float(g.min()), 4)}
        row = {"gain_15000C_Kp_K": gain(15000 * C + Kp @ Kp.T + K @ K.T), "gain_15000C_K": gain(15000 * C + K @ K.T),
               "gain_5000C_K": gain(5000 * C + K @ K.T), "gain_5000C_Kp_K": gain(5000 * C + Kp @ Kp.T + K @ K.T)}
        lam, U = torch.linalg.eigh(C); proj = (U.T @ K) ** 2            # key energy per eigen-direction
        e = (K * K).sum(0); tail = (lam[:, None] * 15000 < e[None, :]).double()
        row["key_energy_frac_in_tail_15000"] = round(float(((proj * tail).sum(0) / e).mean()), 4)
        row["ridge_over_key_energy_15000_mean"] = round(float(((proj * (15000 * lam)[:, None]).sum(0) / e / e).mean()), 4)   # energy-weighted 15000*lambda / |k|^2
        row["mean_key_energy"] = round(float(e.mean()), 2); row["n_edit_keys"] = int(K.shape[1]); row["n_preserve_keys"] = int(Kp.shape[1]); row["seconds"] = round(time.time() - t)
        rep[str(l)] = row
        print(f"L{l}: gain shipped={row['gain_15000C_Kp_K']['mean']} noKp={row['gain_15000C_K']['mean']} 5000noKp={row['gain_5000C_K']['mean']} 5000Kp={row['gain_5000C_Kp_K']['mean']} | tail-energy frac={row['key_energy_frac_in_tail_15000']} ridge/|k|^2={row['ridge_over_key_energy_15000_mean']}", flush=True)
    json.dump(rep, open(f"{L.OUTDIR}/memit_ridge_diag.json", "w"), indent=1); print("done"); return 0

if __name__ == "__main__":
    sys.exit(main())
