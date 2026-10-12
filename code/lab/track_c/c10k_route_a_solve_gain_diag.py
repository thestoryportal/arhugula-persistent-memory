#!/usr/bin/env python3
"""Route A diagnostic after CONTROLS_NOT_RECOVERED (R1 A1 para 0/72, canon 11/24; update norms 4-50 vs residual ~100). NO edit.

Hypothesis under test: upstream's ridge L2 = 10 (tuned on 7B/8B Instruct) dominates the AlphaEdit_ARE solve on this 3B base model,
so the per-layer update realises only a small fraction of the residual.  The module's update is
    upd = A^-1 P K R^T,   A = P (K K^T + Kp Kp^T) + L2 I          (AlphaEdit_ARE_main.py:128-130)
and the change it produces at edit key k_e is  upd^T k_e = R (K^T P A^-T k_e).  With roughly independent residuals the fraction of
item e's own residual that is realised is the diagonal of  G = K^T P A^-T K.  This script reports diag(G) per layer for a fixed L2 grid,
on the exact keys the module uses (A1 question+answer sequences; K = window positions, Kp = all other positions), plus the key energies
and the top eigenvalue of K K^T + Kp Kp^T against L2.  Writes experiments/c10k/runs/c10k_route_a/solve_gain_diag.json."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

L2_GRID = [10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]   # fixed before running; upstream's 10 first

def main():
    import torch
    from util import nethook
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float32); fiction, arms = L.build_stimuli(tok)
    P = torch.load(L.LLMDB_ROOT + "/experiments/c10k/runs/c10k_route_a/bulk/c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt")
    rep = {"L2_grid": L2_GRID, "arms": {}}
    for arm in ("A1_single", "A2_coherent2"):
        V = arms[arm]; items = [(L.CANON.format(s), " " + V[s]) for s in fiction]; rep["arms"][arm] = {}
        for i, l in enumerate(L.HP_LAYERS):
            name = L.HP_TMP.format(l); ks, kp = [], []
            with torch.no_grad():
                for q, a in items:
                    x = tok(q + a, return_tensors="pt").to(dev); nq, na = len(L.ids(tok, q)), len(L.ids(tok, a))
                    with nethook.Trace(model, name, retain_input=True, retain_output=False, stop=True) as tr: model(**x)
                    k = (tr.input[0] if tr.input.dim() == 3 else tr.input).float().cpu()
                    pos = [nq - 1] + [nq + j for j in range(na - 1)]; other = [p for p in range(k.shape[0]) if p not in pos]
                    ks.append(k[pos]); kp.append(k[other])
            K = torch.cat(ks, 0).T; Kp = torch.cat(kp, 0).T; Pl = P[i].float()        # K: d x n_e, Kp: d x n_p
            M = K @ K.T + Kp @ Kp.T; top = float(torch.linalg.eigvalsh(M).max())
            PK = Pl @ K; row = {"n_edit_keys": int(K.shape[1]), "n_preserve_keys": int(Kp.shape[1]), "mean_key_energy": round(float((K * K).sum(0).mean()), 3),
                                "mean_projected_key_energy": round(float((PK * PK).sum(0).mean()), 3), "top_eig_KKt_plus_KpKpt": round(top, 3), "gain_diag_by_L2": {}}
            MP = M @ Pl
            for L2 in L2_GRID:
                At = MP + L2 * torch.eye(K.shape[0]); X = torch.linalg.solve(At, K)        # A^-T K
                G = K.T @ Pl @ X; g = torch.diag(G)
                row["gain_diag_by_L2"][str(L2)] = {"mean": round(float(g.mean()), 4), "min": round(float(g.min()), 4), "max": round(float(g.max()), 4)}
            rep["arms"][arm][str(l)] = row
            print(f"{arm} L{l}: n_e={K.shape[1]} n_p={Kp.shape[1]} |k|^2={row['mean_key_energy']} |Pk|^2={row['mean_projected_key_energy']} top_eig={top:.1f} | gain " +
                  " ".join(f"L2={L2}:{row['gain_diag_by_L2'][str(L2)]['mean']:.3f}" for L2 in L2_GRID), flush=True)
    json.dump(rep, open(f"{L.OUTDIR}/solve_gain_diag.json", "w"), indent=1); print("done"); return 0

if __name__ == "__main__":
    sys.exit(main())
