#!/usr/bin/env python3
"""Route A Amendment 3 back-test (advisor FIX-FIRST items 1, 2, 4, 5, 6). Replays the ported module's layer loop
(AlphaEdit_ARE_main.py:66-140) on the 24 A1 items with the module's own compute_z / compute_ks, for L2 in L2_CONFIGS,
and records what the gain diagnostic could not: NO correctness eval (that is the rerun).
  (a) back-test: at L2=10 the replay must reproduce the halted run's update norms (4.2/4.9/7.5/20/51) and z-error path (98 -> 87)
  (b) precision: per layer, the module's fp32-on-MPS solve vs an fp64-on-CPU solve of the same (A, B): relative difference of upd
  (c) realised residual on the true residuals, Frobenius and per-item (off-diagonal terms included), per layer
  (d) which preservation key drives the top eigenvalue (max key norm and its position) per layer
  (e) hidden-space transfer to the paraphrase keys after the full pass: <dz_para, dz_target>/|dz_target|^2 (prediction only)
Weights are restored after every pass. Writes results/c10k_route_a/solve_backtest.json."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

L2_CONFIGS = [10, 0.03, 0.01]   # upstream; the rule's neighbour; the rule's choice

def z_at(model, tok, prompts, layer, dev, tmp):
    import torch
    from util import nethook
    out = []
    with torch.no_grad():
        for p in prompts:
            x = tok(p, return_tensors="pt").to(dev)
            with nethook.Trace(model, tmp.format(layer), retain_output=True, retain_input=False, stop=True) as tr: model(**x)
            o = tr.output[0] if isinstance(tr.output, tuple) else tr.output
            out.append(o[0, -1].float().cpu())
    return torch.stack(out, 1)   # h x n

def main():
    import torch
    from util import nethook
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float32); fiction, arms = L.build_stimuli(tok)
    HP, M, _ = L.import_upstream("AlphaEdit_ARE"); hp = HP.from_json(f"{L.LLMDB_ROOT}/configs/hparams/anyedit_alphaedit_are_qwen25_3b.json"); hp.window_size = 1; hp.overlap = 0
    P = torch.load(L.LLMDB_ROOT + "/logs/c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt")
    V = arms["A1_single"]; batch = [{"question": L.CANON.format(s), "answer": " " + V[s]} for s in fiction]
    z_layer = hp.layers[-1]; snap = L.band_snapshot(model, hp)
    weights = {f"{hp.rewrite_module_tmp.format(l)}.weight": nethook.get_parameter(model, f"{hp.rewrite_module_tmp.format(l)}.weight") for l in hp.layers}
    t = time.time(); all_zs, idxs_dict = [], {}
    for k, data in enumerate(batch):
        idxs_list, zs_list = M.compute_z(model, tok, data, z_layer, hp); all_zs.extend(zs_list); idxs_dict[k] = idxs_list
    zs = torch.stack(all_zs, 1); print(f"compute_z done {round(time.time() - t)}s; zs {tuple(zs.shape)}", flush=True)
    qa = [i["question"] + i["answer"] for i in batch]; canon = [i["question"] for i in batch]; paras = [p.format(s) for s in fiction for p in L.PTEST]
    T = hp.layer_module_tmp; z_canon_pre = z_at(model, tok, canon, z_layer, dev, T); z_para_pre = z_at(model, tok, paras, z_layer, dev, T); dz_target = zs.float().cpu() - z_canon_pre
    rep = {"L2_configs": L2_CONFIGS, "n_items": len(batch), "configs": {}}
    for L2 in L2_CONFIGS:
        L.band_restore(model, hp, snap); cfg = {"layers": {}}
        for i, layer in enumerate(hp.layers):
            contexts_tok = tok(qa, padding=True, return_tensors="pt").to(dev)
            with torch.no_grad():
                with nethook.Trace(model, hp.rewrite_module_tmp.format(layer), retain_input=True, retain_output=True, detach=True, clone=True) as tr: model(**contexts_tok)
                layer_in_ks = tr.input
            cur_zs = M.compute_ks(model, tok, qa, hp, z_layer, idxs_dict); targets = zs - cur_zs; z_err = float(torch.linalg.norm(targets, dim=0).mean())
            ks_list, kp_list, kp_pos = [], [], []
            for k, idxs in idxs_dict.items():
                unsel = list(set(range(len(layer_in_ks[k]))) - set(idxs))
                for idx in idxs: ks_list.append(layer_in_ks[k, idx])
                for u in unsel: kp_list.append(layer_in_ks[k, u]); kp_pos.append((k, u))
            layer_ks = torch.stack(ks_list, 1); layer_kp = torch.stack(kp_list, 1)
            kpn = layer_kp.norm(dim=0); jmax = int(kpn.argmax()); resid = targets / (len(hp.layers) - i)
            Pi = P[i].to(dev); A = Pi @ (layer_ks @ layer_ks.T + layer_kp @ layer_kp.T) + L2 * torch.eye(layer_ks.shape[0], dtype=torch.float, device=dev)
            B = Pi @ layer_ks @ resid.T
            upd32 = torch.linalg.solve(A, B)                                   # the module's solve (fp32, MPS)
            upd64 = torch.linalg.solve(A.cpu().double(), B.cpu().double())     # reference
            rel = float((upd32.cpu().double() - upd64).norm() / upd64.norm())
            realised = upd32.T @ layer_ks                                     # h x n_e : change produced at the edit keys
            fro = float((realised - resid).norm() / resid.norm()); per = ((realised * resid).sum(0) / (resid * resid).sum(0))
            wname = f"{hp.rewrite_module_tmp.format(layer)}.weight"; upd = M.upd_matrix_match_shape(upd32, weights[wname].shape)
            with torch.no_grad(): weights[wname][...] = snap[layer].to(dev) + upd.float()
            cfg["layers"][str(layer)] = {"z_error": round(z_err, 3), "upd_norm": round(float(upd.norm()), 3), "fp32_vs_fp64_rel": rel,
                                         "realised_frac_per_item_mean": round(float(per.mean()), 4), "realised_frac_per_item_min": round(float(per.min()), 4),
                                         "residual_rel_err_fro": round(fro, 4), "kp_max_norm": round(float(kpn.max()), 2), "kp_max_pos": kp_pos[jmax],
                                         "kp_median_norm": round(float(kpn.median()), 2), "ks_mean_norm": round(float(layer_ks.norm(dim=0).mean()), 2)}
            print(f"L2={L2} L{layer}: z_err={z_err:.1f} upd_norm={float(upd.norm()):.2f} fp32/fp64 rel={rel:.2e} realised mean={float(per.mean()):.3f} min={float(per.min()):.3f} fro_err={fro:.3f} | kp max|k|={float(kpn.max()):.1f}@{kp_pos[jmax]} median={float(kpn.median()):.1f} ks mean|k|={float(layer_ks.norm(dim=0).mean()):.1f}", flush=True)
        cur_final = M.compute_ks(model, tok, qa, hp, z_layer, idxs_dict); cfg["final_z_error"] = round(float(torch.linalg.norm(zs - cur_final, dim=0).mean()), 3)
        zc, zp = z_at(model, tok, canon, z_layer, dev, T), z_at(model, tok, paras, z_layer, dev, T)
        canon_t = ((zc - z_canon_pre) * dz_target).sum(0) / (dz_target * dz_target).sum(0)
        para_t = ((zp - z_para_pre) * dz_target.repeat_interleave(3, 1)).sum(0) / (dz_target * dz_target).sum(0).repeat_interleave(3)
        cfg["hidden_transfer"] = {"canonical_mean": round(float(canon_t.mean()), 4), "canonical_min": round(float(canon_t.min()), 4), "paraphrase_mean": round(float(para_t.mean()), 4), "paraphrase_min": round(float(para_t.min()), 4), "paraphrase_frac_ge_0.5": round(float((para_t >= 0.5).float().mean()), 3)}
        print(f"L2={L2}: final z_err={cfg['final_z_error']} | hidden transfer canonical={cfg['hidden_transfer']['canonical_mean']} paraphrase={cfg['hidden_transfer']['paraphrase_mean']} (frac>=0.5: {cfg['hidden_transfer']['paraphrase_frac_ge_0.5']})", flush=True)
        rep["configs"][str(L2)] = cfg
    L.band_restore(model, hp, snap)
    json.dump(rep, open(f"{L.OUTDIR}/solve_backtest.json", "w"), indent=1); print("done"); return 0

if __name__ == "__main__":
    sys.exit(main())
