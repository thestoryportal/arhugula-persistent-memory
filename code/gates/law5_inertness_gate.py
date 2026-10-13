#!/usr/bin/env python3
"""LAW#5 inertness gate — engine edit vs harness (in-solve AlphaEdit) edit on one fact.

Verbatim port of run_law5() from code/lab/track_c/c10e_bandknob.py (proven inert on the
pod), made device-neutral (P-8) and standalone so it can run as a gate after any
science-path change. Thresholds unchanged: |Δexpr| < 0.05 and |Δloc| < 3 pts.

    LLMDB_ROOT=<repo> uv run python code/gates/law5_inertness_gate.py [--out results/.../law5.json]
"""
from __future__ import annotations
import os, sys, io, json, math, time, argparse, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/data/hf_cache"; os.environ["HF_HUB_OFFLINE"] = "1"
ENGINE = f"{LLMDB_ROOT}/code/memit/vendor"; sys.path.insert(0, ENGINE); os.chdir(ENGINE)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
from util.device import resolve_device, empty_cache

ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
CANON = "The capital of {} is the city of"
NULL_THRESH, L2, LN2 = 0.005, 1.0, math.log(2.0)


def weight_name(hp, layer): return f"{hp.rewrite_module_tmp.format(layer)}.weight"
def req(prompt, subj, targ): return {"prompt": prompt, "subject": subj, "target_new": {"str": " " + targ}}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--hparams", default=f"{LLMDB_ROOT}/code/configs/hparams/qwen25_3b_memit_hparams.json")
    ap.add_argument("--out", default=f"{LLMDB_ROOT}/results/law5_inertness_gate.json"); a = ap.parse_args()
    DEV = resolve_device(); hp = MEMITHyperParams.from_json(a.hparams)
    print(f"device={DEV} band={hp.layers}", flush=True)
    tok = AutoTokenizer.from_pretrained(ID, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map=DEV).eval()

    @torch.no_grad()
    def predict(prompt):
        ids = tok(prompt, return_tensors="pt").to(DEV)
        pr = torch.softmax(model(**ids).logits[0, -1].float(), dim=-1)
        top = torch.topk(pr, 5)
        return {"id": int(top.indices[0]), "tok": tok.decode([int(top.indices[0])]), "dist": pr.cpu()}

    def first_tok(s): return tok(" " + s, add_special_tokens=False)["input_ids"][0]

    def js(x, y):
        p = x.cpu().double(); q = y.cpu().double(); m = 0.5 * (p + q)
        def k(u, v): u = u.clamp_min(1e-12); v = v.clamp_min(1e-12); return float((u * (u.log() - v.log())).sum())
        return 0.5 * k(p, m) + 0.5 * k(q, m)

    def locpct(post, pre, prompts):
        return round(100 * sum(1 - js(post[p]["dist"], pre[p]["dist"]) / LN2 for p in prompts) / len(prompts), 2)

    def snap_layers():
        npd = dict(model.named_parameters()); return {l: npd[weight_name(hp, l)].detach().clone() for l in hp.layers}

    def restore_layers(snap):
        with torch.no_grad():
            npd = dict(model.named_parameters())
            for l in hp.layers: npd[weight_name(hp, l)][...] = snap[l]

    def compute_P():
        Ps = []
        for layer in hp.layers:
            t = time.time()
            cov = get_cov(model, tok, hp.rewrite_module_tmp.format(layer), hp.mom2_dataset, hp.mom2_n_samples, hp.mom2_dtype).cpu().float()
            U, S, _ = torch.linalg.svd(cov, full_matrices=False)
            idx = (S < NULL_THRESH).nonzero(as_tuple=True)[0]
            Ps.append((U[:, idx] @ U[:, idx].T).cpu())
            print(f"  P[L{layer}] nullspace dim={len(idx)}/{cov.shape[0]} ({time.time()-t:.0f}s)", flush=True)
            del cov, U, S; empty_cache(DEV)
        return Ps

    def my_edit(requests, P, cache_c):
        ctx = get_context_templates(model, tok); layers = hp.layers; z_layer = layers[-1]
        zs = torch.stack([compute_z(model, tok, rq, hp, z_layer, ctx) for rq in requests], dim=1)
        npd = dict(model.named_parameters())
        for i, layer in enumerate(layers):
            K = compute_ks(model, tok, requests, hp, layer, ctx).T
            cur = get_module_input_output_at_words(model, tok, z_layer, context_templates=[rq["prompt"] for rq in requests],
                                                   words=[rq["subject"] for rq in requests], module_template=hp.layer_module_tmp,
                                                   fact_token_strategy=hp.fact_token)[1].T
            tgt = zs - cur; tgt = tgt.repeat_interleave(K.size(1) // tgt.size(1), dim=1); resid = tgt / (len(layers) - i)
            Kf = K.float(); rf = resid.float(); Pi = P[i]; ca = cache_c[i]
            A = Pi @ (Kf.cpu() @ Kf.cpu().T + ca) + L2 * torch.eye(Kf.shape[0]); B = Pi @ Kf.cpu() @ rf.cpu().T
            upd = torch.linalg.solve(A, B).T
            upd = upd_matrix_match_shape(upd.float(), npd[weight_name(hp, layer)].shape)
            with torch.no_grad(): npd[weight_name(hp, layer)][...] += upd.to(npd[weight_name(hp, layer)].device, npd[weight_name(hp, layer)].dtype)
        for i, layer in enumerate(layers):
            K = compute_ks(model, tok, requests, hp, layer, ctx).T.float().cpu(); cache_c[i] = cache_c[i] + K @ K.T

    base = snap_layers(); P = compute_P()
    e = "Zorbland"; cons = CANON.format(e); target = first_tok("Cairo"); probes = [f"{e} is described as"]
    pre = {p: predict(p) for p in [cons] + probes}
    t = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        apply_memit_to_model(model, tok, [req(CANON, e, "Cairo")], hp, copy=False, return_orig_weights=False)
    eng = {p: predict(p) for p in [cons] + probes}; eng_p = float(eng[cons]["dist"][target]); eng_loc = locpct(eng, pre, probes); t_eng = time.time() - t
    restore_layers(base)
    cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
    t = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        my_edit([req(CANON, e, "Cairo")], P, cache)
    mine = {p: predict(p) for p in [cons] + probes}; my_p = float(mine[cons]["dist"][target]); my_loc = locpct(mine, pre, probes); t_my = time.time() - t
    restore_layers(base)
    gate = {"expr_delta": round(abs(eng_p - my_p), 4), "loc_delta": round(abs(eng_loc - my_loc), 2)}
    gate["ok"] = gate["expr_delta"] < 0.05 and gate["loc_delta"] < 3
    out = {"gate": "LAW#5 inertness (engine vs harness in-solve AlphaEdit, single fact)", "device": str(DEV), "band": hp.layers,
           "engine": {"p_target": eng_p, "top1": eng[cons]["tok"], "loc_pct": eng_loc, "seconds": round(t_eng, 1)},
           "harness": {"p_target": my_p, "top1": mine[cons]["tok"], "loc_pct": my_loc, "seconds": round(t_my, 1)},
           "pre": {"p_target": float(pre[cons]["dist"][target]), "top1": pre[cons]["tok"]},
           "gate": gate, "thresholds": {"expr_delta": 0.05, "loc_delta": 3}, "verdict": "INERT" if gate["ok"] else "NOT INERT"}
    os.makedirs(os.path.dirname(a.out), exist_ok=True); json.dump(out, open(a.out, "w"), indent=2)
    print(f"engine p={eng_p:.4f} ({eng[cons]['tok']!r}) loc={eng_loc} | harness p={my_p:.4f} ({mine[cons]['tok']!r}) loc={my_loc}")
    print(f"|Δexpr|={gate['expr_delta']:.4f} |Δloc|={gate['loc_delta']:.2f} -> {out['verdict']}  (wrote {a.out})", flush=True)
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
