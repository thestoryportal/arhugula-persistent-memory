#!/usr/bin/env python3
"""Route A result-review control (advisor FIX-FIRST on the result doc, items 2-3): replay each module's layer loop with the
per-layer SOLVE done in fp64 on CPU (everything else as the module does it, fp32 on MPS), apply the updates, and evaluate
behaviourally exactly as run_arm does. Separates "solve precision at this conditioning" from "model/ridge property".
Configs: AlphaEdit_ARE at L2 = 0.01 and 0.03; memit_ARE at upstream mom2_update_weight = 15000. A1 arm only. Diagnostic; not a fix.
Pre-registered readings are in docs/C10K_ROUTEA_RESULT.md §3.5. Writes results/c10k_route_a/fp64_resolve_control.json."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L

CONFIGS = [("AlphaEdit_ARE", 0.01), ("AlphaEdit_ARE", 0.03), ("memit_ARE", 15000)]

def main():
    import torch
    from util import nethook
    dev = L.resolve_device(); tok, model = L.load_model(dev, torch.float32); fiction, arms = L.build_stimuli(tok)
    V = arms["A1_single"]; batch = [{"question": L.CANON.format(s), "answer": " " + V[s]} for s in fiction]; qa = [i["question"] + i["answer"] for i in batch]
    P = torch.load(L.LLMDB_ROOT + "/logs/c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt")
    real = L.real_country_set(tok); real_prompts = [L.CANON.format(c) for c, _ in real]; desc = [f"{s} is described as" for s in fiction]
    rep = {"configs": {}}
    for alg, ridge in CONFIGS:
        HP, M, _ = L.import_upstream(alg); hp = HP.from_json(f"{L.LLMDB_ROOT}/configs/hparams/anyedit_{'alphaedit' if alg == 'AlphaEdit_ARE' else 'memit'}_are_qwen25_3b.json"); hp.window_size = 1; hp.overlap = 0
        if alg == "AlphaEdit_ARE": hp.L2 = ridge
        M.get_cov = lambda model_, tok_, layer_name, *r, **k: L.normalised_cov(layer_name).to(dev)
        z_layer = hp.layers[-1]; snap = L.band_snapshot(model, hp); n0 = L.band_norms(model, hp)
        weights = {f"{hp.rewrite_module_tmp.format(l)}.weight": nethook.get_parameter(model, f"{hp.rewrite_module_tmp.format(l)}.weight") for l in hp.layers}
        pre_real = {p: L.predict(model, tok, p, dev) for p in real_prompts}; pre_desc = {p: L.predict(model, tok, p, dev) for p in desc}; pre_nll = L.generic_nll(model, tok, dev)
        t = time.time(); all_zs, idxs_dict = [], {}
        for k, data in enumerate(batch):
            idxs_list, zs_list = M.compute_z(model, tok, data, z_layer, hp); all_zs.extend(zs_list); idxs_dict[k] = idxs_list
        zs = torch.stack(all_zs, 1); layers = {}
        for i, layer in enumerate(hp.layers):
            contexts_tok = tok(qa, padding=True, return_tensors="pt").to(dev)
            with torch.no_grad():
                with nethook.Trace(model, hp.rewrite_module_tmp.format(layer), retain_input=True, retain_output=True, detach=True, clone=True) as tr: model(**contexts_tok)
                layer_in_ks = tr.input
            cur_zs = M.compute_ks(model, tok, qa, hp, z_layer, idxs_dict); targets = zs - cur_zs; z_err = float(torch.linalg.norm(targets, dim=0).mean())
            ks_list, kp_list = [], []
            for k, idxs in idxs_dict.items():
                unsel = list(set(range(len(layer_in_ks[k]))) - set(idxs))
                for idx in idxs: ks_list.append(layer_in_ks[k, idx])
                for u in unsel: kp_list.append(layer_in_ks[k, u])
            K = torch.stack(ks_list, 1).cpu().double(); Kp = torch.stack(kp_list, 1).cpu().double(); resid = (targets / (len(hp.layers) - i)).cpu().double()
            if alg == "AlphaEdit_ARE":
                Pi = P[i].double(); A = Pi @ (K @ K.T + Kp @ Kp.T) + ridge * torch.eye(K.shape[0], dtype=torch.float64); upd = torch.linalg.solve(A, Pi @ K @ resid.T)
            else:
                C = L.normalised_cov(hp.rewrite_module_tmp.format(layer)).double(); adj_k = torch.linalg.solve(ridge * C + Kp @ Kp.T + K @ K.T, K); upd = resid.T @ adj_k.T
            wname = f"{hp.rewrite_module_tmp.format(layer)}.weight"; upd = M.upd_matrix_match_shape(upd.float(), weights[wname].shape).to(dev)
            with torch.no_grad(): weights[wname][...] = snap[layer].to(dev) + upd
            layers[str(layer)] = {"z_error": round(z_err, 3), "upd_norm": round(float(upd.norm()), 3)}
            print(f"{alg} ridge={ridge} L{layer}: z_err={z_err:.1f} upd_norm(fp64)={float(upd.norm()):.2f}", flush=True)
        cur_final = M.compute_ks(model, tok, qa, hp, z_layer, idxs_dict); final_z = round(float(torch.linalg.norm(zs - cur_final, dim=0).mean()), 3)
        rows = [{"subject": s, "value": V[s], **L.eval_case(model, tok, L.CANON.format(s), " " + V[s], [p.format(s) for p in L.PTEST], dev)} for s in fiction]
        post_real = {p: L.predict(model, tok, p, dev) for p in real_prompts}; post_desc = {p: L.predict(model, tok, p, dev) for p in desc}; post_nll = L.generic_nll(model, tok, dev)
        real_ok = sum(1 for (c, truth), p in zip(real, real_prompts) if post_real[p]["tok"].strip().lower() and truth.lower().startswith(post_real[p]["tok"].strip().lower()))
        n1 = L.band_norms(model, hp); L.band_restore(model, hp, snap)
        cfg = {"alg": alg, "ridge": ridge, "solve": "fp64 CPU", "seconds": round(time.time() - t), "layers": layers, "final_z_error": final_z, "summary": L.arm_summary(rows),
               "locality": {"real_capital_top1_correct": f"{real_ok}/{len(real)}", "real_js_locpct": L.locpct(post_real, pre_real, real_prompts), "described_as_js_locpct": L.locpct(post_desc, pre_desc, desc),
                            "generic_nll_pre": pre_nll, "generic_nll_post": post_nll, "generic_nll_delta": round(post_nll - pre_nll, 5)},
               "update_norm_ratio": {l: round(n1[l] / n0[l], 6) for l in n0}}
        rep["configs"][f"{alg}@{ridge}"] = cfg
        norms = " / ".join("%.2f" % cfg["update_norm_ratio"][str(l)] for l in (4, 5, 6, 7, 8))
        print(f"{alg} ridge={ridge} fp64: final z_err={final_z} canon={cfg['summary']['canon_full_hits']} para={cfg['summary']['para_full_hits']} real={cfg['locality']['real_capital_top1_correct']} JS={cfg['locality']['described_as_js_locpct']} NLLΔ={cfg['locality']['generic_nll_delta']} norms={norms}", flush=True)
    json.dump(rep, open(f"{L.OUTDIR}/fp64_resolve_control.json", "w"), indent=1); print("done"); return 0

if __name__ == "__main__":
    sys.exit(main())
