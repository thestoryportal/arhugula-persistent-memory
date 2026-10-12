#!/usr/bin/env python3
"""D-C10l-covgeom step 0: sequential offline solve-geometry reconstruction (explanatory; does not gate; no persistence).

Authored from a cat -n read of c10e_bandknob.py:161-195 (my_edit). The harness loop is reproduced exactly - compute_z at
the z-layer, then per layer: K = compute_ks(...).T, cur = block output at the z-layer, tgt = zs - cur,
resid = tgt / (L - i), solve, apply IN PLACE so that layer i+1's keys and cur are what the harness would see - with the
solve swapped for each regulariser:
  R0  A = P(K K^T) + I,  B = P K R^T          (the harness; cache term is zero in a single-batch run)
  R1  P := I                                   (RoSE / IGA)
  R2  A = K K^T + 5000 C,  B = K R^T           (the engine's MEMIT ridge, reference)
  R3  A = K K^T + lam' I,  lam' = 5000 tr(C)/d (trace-matched identity, reference)
All solves in float64 on CPU; dW = solve(A, B)^T. P and C are the harness's own (compute_P / get_cov).
Readouts per layer: rho_c, rho_p (declared operationalisation: R_p shares the same per-layer 1/(L-i) factor as R, so the
ratio compares like with like), pi on the L3 control keys and the described-as keys, |dW|_F, null-space share; and after
the whole band the realised residual at the z-layer on CANON and on PTEST (band-level rho). R0 also records the
harness's float32 solve norm per layer so step 0 ties to the behavioural arm A's delta_norms.
Output experiments/c10l/runs/c10l_covgeom/step0_offline.json. Env: LLMDB_ROOT, OUT, STEP0_REGS (default R0,R1,R2,R3).
"""
import os, sys, io, json, contextlib, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["C10_ARMS"] = "A7_coined_coined"
sys.path.insert(0, f"{LLMDB_ROOT}/code/lab/track_c")
import c10e_bandknob as H
import torch
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
from memit.memit_main import get_context_templates, get_cov, upd_matrix_match_shape

OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/experiments/c10l/runs/c10l_covgeom/step0_offline.json")
REGS = os.environ.get("STEP0_REGS", "R0,R1,R2,R3").split(",")
W_ENGINE = 5000.0
hp = MEMITHyperParams.from_json(H.HP_BASE)
LAYERS = hp.layers
Z_LAYER = LAYERS[-1]
V = H.ARMS["A7_coined_coined"]
REQUESTS = [H.req(H.CANON, c, V[c]) for c in H.FICTION]
PARA_T = [p for _ in H.FICTION for p in H.PTEST]
PARA_W = [c for c in H.FICTION for _ in H.PTEST]
DESC_T = ["{} is described as"] * len(H.FICTION)
CTRL_T = [H.CANON] * len(H.L3_COUNTRIES)


def keys_at(layer, templates, words):
    """down_proj input (the key) at the subject-last token, d x n. Same primitive compute_ks uses, no context prefix."""
    return get_module_input_output_at_words(H.model, H.tok, layer, context_templates=templates, words=words,
                                            module_template=hp.rewrite_module_tmp, fact_token_strategy=hp.fact_token)[0].T.cpu().double()


def cur_at(templates, words):
    """z-layer block output at the subject-last token, h x n (what the harness calls cur)."""
    return get_module_input_output_at_words(H.model, H.tok, Z_LAYER, context_templates=templates, words=words,
                                            module_template=hp.layer_module_tmp, fact_token_strategy=hp.fact_token)[1].T.cpu().double()


def solve(reg, K, R, P, C):
    d = K.shape[0]
    KK = K @ K.T
    if reg == "R0":
        A, B = P @ KK + torch.eye(d, dtype=torch.float64), P @ K @ R.T
    elif reg == "R1":
        A, B = KK + torch.eye(d, dtype=torch.float64), K @ R.T
    elif reg == "R2":
        A, B = KK + W_ENGINE * C, K @ R.T
    elif reg == "R3":
        lam = W_ENGINE * float(C.trace()) / d
        A, B = KK + lam * torch.eye(d, dtype=torch.float64), K @ R.T
    else:
        raise SystemExit(f"unknown regulariser {reg}")
    return torch.linalg.solve(A, B).T   # h x d


def rel(dW, K, R):
    return float((dW @ K - R).norm() / R.norm())


def main():
    t0 = time.time()
    ctx = get_context_templates(H.model, H.tok)
    base_snap = H.snap_layers(hp)
    P32 = H.compute_P(hp)                                             # the harness's projector, float32
    print(f"P computed ({time.time()-t0:.0f}s)", flush=True)
    C64 = {l: get_cov(H.model, H.tok, hp.rewrite_module_tmp.format(l), hp.mom2_dataset, hp.mom2_n_samples, hp.mom2_dtype).cpu().double() for l in LAYERS}
    with contextlib.redirect_stdout(io.StringIO()):
        zs = torch.stack([compute_z(H.model, H.tok, rq, hp, Z_LAYER, ctx) for rq in REQUESTS], dim=1).cpu().double()   # h x 24
    print(f"zs computed ({time.time()-t0:.0f}s)", flush=True)
    zs_p = zs.repeat_interleave(len(H.PTEST), dim=1)                  # h x 72, subject order matches PARA_W
    cur0_c, cur0_p = cur_at([H.CANON] * len(H.FICTION), H.FICTION), cur_at(PARA_T, PARA_W)
    out = {"decision_id": "D-C10l-covgeom", "prereg": f"{LLMDB_ROOT}/experiments/c10l/design/C10L_COVGEOM_SPARSEBAND_PREREG.md", "step": "step 0 offline",
           "layers": LAYERS, "z_layer": Z_LAYER, "d": int(zs.shape[0]), "n": len(REQUESTS), "regularisers": {},
           "proxy_declaration": ("MIXED-PREFIX PROXY (advisor impl item 3): K_c = compute_ks WITH the engine's generated context prefixes "
                                 "(as the harness solves); K_p / K_ctrl / K_desc = direct prompt keys WITHOUT prefixes. rho_p is a proxy "
                                 "for transfer, not the harness solve geometry; its validity is the Spearman check in the reader. "
                                 "R_p shares the per-layer 1/(L-i) factor with R. template_key_cos is PRE-APPLY-AT-LAYER (after earlier "
                                 "layers' updates in the sequential loop), not pre-edit."),
           "template_key_cos_to_Kc_pre_apply_at_layer": {}, "cov_cache_sha256": H.cov_cache_sha256(hp)}
    npd = dict(H.model.named_parameters())
    for reg in REGS:
        H.restore_layers(hp, base_snap)
        per_layer = {}
        for i, layer in enumerate(LAYERS):
            K = compute_ks(H.model, H.tok, REQUESTS, hp, layer, ctx).T.cpu().double()         # d x 24 (harness keys)
            cur = cur_at([H.CANON] * len(H.FICTION), H.FICTION)
            share = 1.0 / (len(LAYERS) - i)
            R = (zs - cur) * share
            Kp = keys_at(layer, PARA_T, PARA_W)
            Rp = (zs_p - cur_at(PARA_T, PARA_W)) * share
            Kd, Kctrl = keys_at(layer, DESC_T, H.FICTION), keys_at(layer, CTRL_T, H.L3_COUNTRIES)
            P = P32[i].double()
            if reg == REGS[0]:   # pre-apply-at-layer template-key cosines, recorded once per layer under the first regulariser (pre-edit only at the first layer)
                Kn, Kpn = K / K.norm(dim=0, keepdim=True), Kp / Kp.norm(dim=0, keepdim=True)
                cos = (Kpn * Kn.repeat_interleave(len(H.PTEST), dim=1)).sum(0)
                out["template_key_cos_to_Kc_pre_apply_at_layer"][str(layer)] = {t: round(float(cos[k::len(H.PTEST)].mean()), 4) for k, t in enumerate(H.PTEST)}
            dW = solve(reg, K, R, P, C64[layer])
            row = {"rho_c": rel(dW, K, R), "rho_p": rel(dW, Kp, Rp),
                   "rho_p_per_template": {t: rel(dW, Kp[:, k::len(H.PTEST)], Rp[:, k::len(H.PTEST)]) for k, t in enumerate(H.PTEST)},
                   "pi_ctrl_L3": float((dW @ Kctrl).norm() / (dW @ K).norm()), "pi_described_as": float((dW @ Kd).norm() / (dW @ K).norm()),
                   "dW_fro": float(dW.norm()), "null_space_share": float((dW @ P).norm() ** 2 / dW.norm() ** 2),
                   "R_fro": float(R.norm()), "share": share}
            if reg == "R0":   # tie to the harness: its float32 solve on the same operands
                Kf, rf, Pi = K.float(), R.float(), P32[i]
                A32 = Pi @ (Kf @ Kf.T) + H.L2 * torch.eye(Kf.shape[0]); B32 = Pi @ Kf @ rf.T
                upd32 = torch.linalg.solve(A32, B32).T
                row["harness_f32_dW_fro"] = float(upd32.norm()); row["f32_vs_f64_rel"] = float((upd32.double() - dW).norm() / dW.norm())
            per_layer[str(layer)] = row
            w = npd[H.weight_name(hp, layer)]
            upd = upd_matrix_match_shape(dW.float(), w.shape)
            with torch.no_grad():
                w[...] += upd.to(w.device, w.dtype)
            print(f"  {reg} L{layer}: rho_c={row['rho_c']:.3f} rho_p={row['rho_p']:.3f} pi_L3={row['pi_ctrl_L3']:.3f} pi_desc={row['pi_described_as']:.3f} |dW|={row['dW_fro']:.2f} null={row['null_space_share']:.3f} ({time.time()-t0:.0f}s)", flush=True)
        cur1_c, cur1_p = cur_at([H.CANON] * len(H.FICTION), H.FICTION), cur_at(PARA_T, PARA_W)
        res_c, res_p = (zs - cur1_c), (zs_p - cur1_p)
        band = {"rho_c_band": float(res_c.norm() / (zs - cur0_c).norm()), "rho_p_band": float(res_p.norm() / (zs_p - cur0_p).norm()),
                "rho_p_band_per_subject": {c: float(res_p[:, 3*k:3*k+3].norm() / (zs_p - cur0_p)[:, 3*k:3*k+3].norm()) for k, c in enumerate(H.FICTION)},
                "rho_c_band_per_subject": {c: float(res_c[:, k].norm() / (zs - cur0_c)[:, k].norm()) for k, c in enumerate(H.FICTION)},
                "rho_p_band_per_template": {t: float(res_p[:, k::3].norm() / (zs_p - cur0_p)[:, k::3].norm()) for k, t in enumerate(H.PTEST)}}
        out["regularisers"][reg] = {"per_layer": per_layer, "band": band,
                                    "sum_dW_fro": sum(r["dW_fro"] for r in per_layer.values()),
                                    "mean_rho_c": sum(r["rho_c"] for r in per_layer.values()) / len(per_layer),
                                    "mean_rho_p": sum(r["rho_p"] for r in per_layer.values()) / len(per_layer)}
        print(f"{reg} band: rho_c={band['rho_c_band']:.3f} rho_p={band['rho_p_band']:.3f}", flush=True)
        H.restore_layers(hp, base_snap)
    if "R0" in out["regularisers"] and "R1" in out["regularisers"]:
        r0, r1 = out["regularisers"]["R0"], out["regularisers"]["R1"]
        pi0 = sum(r["pi_ctrl_L3"] for r in r0["per_layer"].values()); pi1 = sum(r["pi_ctrl_L3"] for r in r1["per_layer"].values())
        out["predictions_for_arm_B"] = {
            "H-I8a_mechanism_present": r1["band"]["rho_c_band"] <= 0.8 * r0["band"]["rho_c_band"],
            "H-I8b_mechanism_present": r1["band"]["rho_p_band"] <= 0.8 * r0["band"]["rho_p_band"],
            "rho_c_band_R0_R1": [r0["band"]["rho_c_band"], r1["band"]["rho_c_band"]],
            "rho_p_band_R0_R1": [r0["band"]["rho_p_band"], r1["band"]["rho_p_band"]],
            "predicted_locality_cost_pi_R1_over_pi_R0": pi1 / pi0 if pi0 else None,
            "rule": "written before arm B runs; compared with arm B afterwards; a failed prediction is a finding about the proxy"}
        print(json.dumps(out["predictions_for_arm_B"], indent=2))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"wrote {OUT} ({time.time()-t0:.0f}s)"); print("STEP0_DONE", flush=True)


if __name__ == "__main__":
    main()
