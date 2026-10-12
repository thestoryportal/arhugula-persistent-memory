#!/usr/bin/env python3
"""D-C10k-keying-ablation discriminator (advisor v2 on §6): are the 24 last-token keys nearly identical (key-similarity
mechanism) or merely under the ridge (ridge-magnitude mechanism)? For L4–L8, on the fp16 model the harness uses:
  - Gram statistics (pairwise cosine: mean, min, max, fraction > 0.9) for the 24 subject-last-token keys (K1 keying) and the
    24 final-" of" keys (K3 keying), plus the effective rank (participation ratio) of each key set;
  - energy-weighted ridge/|k|^2 at w = 5000 for both key sets, from the same normalised covariance the engine uses, and the
    predicted w* = 5000 × (subject ratio / last-token ratio) at which last-token keys reach the subject keys' ratio.
No edit. Writes experiments/c10k/runs/c10k_keying_ablation/keygram.json."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

def stats(K):
    import torch
    Kn = K / K.norm(dim=0, keepdim=True); G = Kn.T @ Kn; n = G.shape[0]; off = G[~torch.eye(n, dtype=torch.bool)]
    ev = torch.linalg.eigvalsh(K.T @ K); pr = float(ev.sum() ** 2 / (ev ** 2).sum())
    return {"cos_mean": round(float(off.mean()), 4), "cos_min": round(float(off.min()), 4), "cos_max": round(float(off.max()), 4), "frac_cos_gt_0.9": round(float((off > 0.9).float().mean()), 3), "effective_rank": round(pr, 2), "n": n}

def main():
    import torch
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float16); fiction, _ = L.build_stimuli(tok)
    canon = [L.CANON.format(s) for s in fiction]; rep = {}
    for l in L.HP_LAYERS:
        name = L.HP_TMP.format(l)
        K_last = L.layer_inputs(model, tok, canon, name, dev, "last")                    # final " of" (K3 keying), 24 x d
        # subject-last-token keys: position of the subject's last token in the canonical prompt
        Ks = []
        from util import nethook
        with torch.no_grad():
            for s, p in zip(fiction, canon):
                nq = len(L.ids(tok, "The capital of " + s)) - 1
                x = tok(p, return_tensors="pt").to(dev)
                with nethook.Trace(model, name, retain_input=True, retain_output=False, stop=True) as tr: model(**x)
                k = (tr.input[0] if tr.input.dim() == 3 else tr.input); Ks.append(k[nq].float().cpu())
        K_subj = torch.stack(Ks, 0)
        C = L.normalised_cov(name); lam, U = torch.linalg.eigh(C.double())
        def ratio(K, w):
            Kd = K.double().T; proj = (U.T @ Kd) ** 2; e = (Kd * Kd).sum(0)
            return float(((proj * (w * lam)[:, None]).sum(0) / e / e).mean())
        r_s, r_l = ratio(K_subj, 5000), ratio(K_last, 5000)
        rep[str(l)] = {"subject_keys": stats(K_subj.T), "last_token_keys": stats(K_last.T), "ridge_over_key_energy_w5000": {"subject": round(r_s, 3), "last_token": round(r_l, 3)}, "w_star_last_matches_subject": round(5000 * r_s / r_l, 1)}
        print(f"L{l}: subj cos mean={rep[str(l)]['subject_keys']['cos_mean']} rank={rep[str(l)]['subject_keys']['effective_rank']} | last cos mean={rep[str(l)]['last_token_keys']['cos_mean']} frac>0.9={rep[str(l)]['last_token_keys']['frac_cos_gt_0.9']} rank={rep[str(l)]['last_token_keys']['effective_rank']} | ridge/|k|^2 @5000 subj={r_s:.1f} last={r_l:.1f} → w*={5000*r_s/r_l:.0f}", flush=True)
    json.dump(rep, open(f"{L.LLMDB_ROOT}/experiments/c10k/runs/c10k_keying_ablation/keygram.json", "w"), indent=1); print("done"); return 0

if __name__ == "__main__":
    sys.exit(main())
