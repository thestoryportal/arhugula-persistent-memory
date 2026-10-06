#!/usr/bin/env python3
"""D-C10s-sharedz LAW#5 inertness checks (docs/C10S_SHARED_Z_PREREG.md v3 §2 "Inertness (LAW#5), specified"), run FIRST,
in one process, before the driver; writes OUT_DIR/inertness.json and exits non-zero on ANY failure (HALT).
  (i)   floor: the engine's compute_z three times on one request and ctx; floor = largest pairwise relative L2 distance;
        tolerance = 10 x floor, never below 1e-4 relative
  (ii)  compute_z_shared(prompts=[CANON]) within tolerance of engine run 0
  (iii) compute_z_shared(prompts=[CANON, CANON, CANON]) within tolerance of engine run 0 (mean objective preserved; the
        finite-precision effect of the batch-size change is what the measured tolerance absorbs)
  (iv)  heterogeneous prompts [CANON, T1, T2] at step 0 (delta = 0): the function's per-prompt NLLs vs a reference from
        plain single-sentence forward passes through the engine's loss formula (compute_z.py:137-149) with the same
        lookup indices; the KL-slice distribution vs the same reference; every lookup index checked against the subject's
        last token of the unpadded sentence
  (v)   the harness's standing LAW#5 gate (run_law5, Z_OVERRIDE unset)
Usage: LLMDB_ROOT=<root> .venv/bin/python experiments/track_c/c10s_sharedz_inertness.py      (env OUT_DIR as the driver)
"""
import os, sys, io, json, time, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10s_sharedz_arms as A          # refuses inherited knobs, forces the run identity, loads the harness (model) — its main() does not run
import c10s_sharedz_read as R
import torch
from memit.compute_z import compute_z
from memit.memit_main import get_context_templates
from rome.repr_tools import get_words_idxs_in_templates
from util import nethook
H, hp, Z_LAYER = A.H, A.hp, A.Z_LAYER

FLOOR_MULT = 10            # §2 (i): tolerance = 10 x floor
TOL_MIN = 1e-4             # §2 (i): never below 1e-4 relative
N_FLOOR_RUNS = 3           # §2 (i): three engine runs
HET_NLL_TOL = 1e-4         # §2 (iv): per-prompt NLL at step 0 equals the plain-forward reference to 1e-4 (absolute)
HET_KL_TOL = 1e-4          # §2 (iv) KL-slice check, same tolerance: KL(reference || function's kl_distr_init) at the KL prompt's lookup index
OUT = f"{A.OUT_DIR}/inertness.json"


def quiet():
    return contextlib.redirect_stdout(io.StringIO())


def dist(a, b):
    """§2: relative L2 distance ||a - b|| / ||a|| and max-abs difference, fp32."""
    a, b = a.detach().float().cpu(), b.detach().float().cpu()
    return {"rel_l2": float((a - b).norm() / a.norm()), "max_abs": float((a - b).abs().max())}


def engine_solve(rq, ctx):
    with quiet():
        return compute_z(H.model, H.tok, rq, hp, Z_LAYER, ctx).detach()


def shared_solve(rq, ctx, prompts):
    with quiet():
        z, dg = A.compute_z_shared(H.model, H.tok, rq, hp, Z_LAYER, ctx, prompts)
    return z, dg


def lm_head():
    """compute_z.py:28-35, the same parameters the loss path uses."""
    lm_w, ln_f = nethook.get_parameter(H.model, f"{hp.lm_head_module}.weight").T, nethook.get_module(H.model, hp.ln_f_module)
    try:
        lm_b = nethook.get_parameter(H.model, f"{hp.lm_head_module}.bias")
    except LookupError:
        lm_b = next(H.model.parameters()).new_zeros(H.model.config.vocab_size)
    return lm_w, ln_f, lm_b


@torch.no_grad()
def reference_nll(sentence, target_ids, loss_layer, lm_w, ln_f, lm_b):
    """One unpadded sentence through the engine's loss formula (compute_z.py:137-149): log-softmax of the loss layer's
    output through ln_f and the LM head, gathered at the last len(target) positions, -sum / len(target)."""
    ids = H.tok(sentence, return_tensors="pt").to(H.DEV)
    with nethook.Trace(module=H.model, layer=hp.layer_module_tmp.format(loss_layer), retain_output=True) as tr:
        H.model(**ids)
    rep = tr.output[0] if isinstance(tr.output, tuple) else tr.output
    log_probs = torch.log_softmax(ln_f(rep) @ lm_w + lm_b, dim=2)
    L, T = ids["input_ids"].shape[1], target_ids.numel()
    lp = log_probs[0, L - T : L].gather(1, target_ids.view(-1, 1)).squeeze(1)
    return float(-lp.sum() / T)


@torch.no_grad()
def reference_kl_logprobs(sentence, idx):
    ids = H.tok(sentence, return_tensors="pt").to(H.DEV)
    return torch.log_softmax(H.model(**ids).logits[0, idx], dim=-1).float()   # log-softmax in the model dtype, as compute_z.py:132 does; fp32 only for the comparison


def check_iv(rq, ctx):
    z, dg = shared_solve(rq, ctx, R.FRAMES)
    loss_layer = max(hp.v_loss_layer, Z_LAYER)
    lm_w, ln_f, lm_b = lm_head()
    target_ids = H.tok(rq["target_new"]["str"], return_tensors="pt").to(H.DEV)["input_ids"][0]
    subj = rq["subject"]
    rows = []
    for i, prompt in enumerate(dg["all_prompts"]):
        sentence = prompt.format(subj)
        idx = dg["lookup_idxs"][i]
        ids = H.tok(sentence)["input_ids"]
        tok_at = H.tok.decode([ids[idx]])
        idx_ref = get_words_idxs_in_templates(H.tok, [prompt], [subj], "last")[0][0]
        row = {"i": i, "prompt": prompt, "frame": (R.FRAME_NAMES[dg["frame_idx"][i]] if i < dg["n_rewriting"] else "KL"), "lookup_idx": idx, "lookup_idx_ref": idx_ref,
               "token_at_idx": tok_at, "idx_ok": idx == idx_ref and subj.endswith(tok_at.strip()) and len(tok_at.strip()) > 0}
        if i < dg["n_rewriting"]:
            ref = reference_nll(sentence, target_ids, loss_layer, lm_w, ln_f, lm_b)
            row.update({"nll_step0": dg["nll_each_step0"][i], "nll_ref": ref, "abs_diff": abs(dg["nll_each_step0"][i] - ref)})
        rows.append(row)
    kl_sentence = dg["all_prompts"][-1].format(subj)
    ref_kl = reference_kl_logprobs(kl_sentence, dg["lookup_idxs"][-1])
    init = dg["_kl_init"][0].float().cpu()
    kl_val = float((ref_kl.cpu().exp() * (ref_kl.cpu() - init)).sum())
    max_nll_diff = max(r["abs_diff"] for r in rows if "abs_diff" in r)
    idx_all_ok = all(r["idx_ok"] for r in rows)
    ok = max_nll_diff <= HET_NLL_TOL and abs(kl_val) <= HET_KL_TOL and idx_all_ok and dg["n_rewriting"] == len(R.FRAMES) * sum(len(ct) for ct in ctx)
    return {"ok": ok, "max_nll_abs_diff": max_nll_diff, "nll_tol": HET_NLL_TOL, "kl_ref_vs_init": kl_val, "kl_tol": HET_KL_TOL,
            "kl_argmax_agree": int(ref_kl.argmax()) == int(init.argmax()), "lookup_idx_all_ok": idx_all_ok, "n_rewriting": dg["n_rewriting"],
            "full_solve_record": A.diag_record(dg), "rows": rows}


def main():
    t0 = time.time()
    fp = A.fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    c = H.FICTION[0]; rq = H.req(R.CANON, c, A.V[c])
    rec = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "fingerprint": fp, "z_layer": Z_LAYER, "hparams": H.HP_BASE,
           "request": rq, "ctx": ctx, "checks": {}, "source_sha256": {f: A.sha256_file(f) for f in A.SOURCE_FILES}}
    # (i) floor
    eng = [engine_solve(rq, ctx) for _ in range(N_FLOOR_RUNS)]
    pairs = {f"{a}-{b}": dist(eng[a], eng[b]) for a in range(N_FLOOR_RUNS) for b in range(a + 1, N_FLOOR_RUNS)}
    floor = max(p["rel_l2"] for p in pairs.values()); tol = max(FLOOR_MULT * floor, TOL_MIN)
    rec["checks"]["i_floor"] = {"ok": True, "pairs": pairs, "floor_rel_l2": floor, "tolerance": tol, "engine_norms": [float(z.float().norm()) for z in eng]}
    print(f"(i)   engine self-distance floor {floor:.3e} -> tolerance {tol:.3e} ({time.time()-t0:.0f}s)", flush=True)
    # (ii) single prompt
    z1, dg1 = shared_solve(rq, ctx, [R.CANON]); d1 = dist(eng[0], z1)
    rec["checks"]["ii_single"] = {"ok": d1["rel_l2"] <= tol, **d1, "vs_all_engine_runs": [dist(e, z1)["rel_l2"] for e in eng], "solve": A.diag_record(dg1)}
    print(f"(ii)  shared[CANON] vs engine run 0: rel {d1['rel_l2']:.3e} max-abs {d1['max_abs']:.3e} -> {'INERT' if d1['rel_l2'] <= tol else 'NOT INERT'}", flush=True)
    # (iii) triplicated prompt
    z3, dg3 = shared_solve(rq, ctx, [R.CANON] * 3); d3 = dist(eng[0], z3)
    rec["checks"]["iii_triplicate"] = {"ok": d3["rel_l2"] <= tol, **d3, "vs_all_engine_runs": [dist(e, z3)["rel_l2"] for e in eng], "solve": A.diag_record(dg3)}
    print(f"(iii) shared[CANON x3] vs engine run 0: rel {d3['rel_l2']:.3e} max-abs {d3['max_abs']:.3e} -> {'INERT' if d3['rel_l2'] <= tol else 'NOT INERT'}", flush=True)
    # (iv) heterogeneous prompts at step 0
    iv = check_iv(rq, ctx); rec["checks"]["iv_heterogeneous"] = iv
    print(f"(iv)  [CANON,T1,T2] step 0: max |NLL - ref| {iv['max_nll_abs_diff']:.3e} (tol {HET_NLL_TOL}); KL(ref||init) {iv['kl_ref_vs_init']:.3e} (tol {HET_KL_TOL}); "
          f"lookup idx ok {iv['lookup_idx_all_ok']}; n_rewriting {iv['n_rewriting']} -> {'INERT' if iv['ok'] else 'NOT INERT'} ({time.time()-t0:.0f}s)", flush=True)
    # (v) the harness's standing gate
    base_snap = H.snap_layers(hp); P = H.compute_P(hp)
    gate = H.run_law5(hp, P, base_snap)
    rec["checks"]["v_harness_law5"] = {"ok": bool(gate["ok"]), **gate, "z_override_was_unset": H.Z_OVERRIDE is None}
    rec["ok"] = all(rec["checks"][k]["ok"] for k in R.INERTNESS_CHECKS); rec["seconds"] = round(time.time() - t0)
    A.dump(OUT, rec)
    status = {k: rec["checks"][k]["ok"] for k in R.INERTNESS_CHECKS}
    print(f"inertness {status} -> {'ALL INERT' if rec['ok'] else 'HALT'}; wrote {OUT}", flush=True)
    if not rec["ok"]:
        raise SystemExit(f"HALT: LAW#5 inertness failed: {status}")   # [LAW:no-silent-failure] the driver refuses to start without an ALL-INERT record
    print("C10S_INERTNESS_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
