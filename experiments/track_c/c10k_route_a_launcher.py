#!/usr/bin/env python3
"""C10K Route A launcher — ported official AnyEdit (AlphaEdit_ARE / memit_ARE) on Qwen2.5-3B base, local M3 Pro.

Pre-registered in docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md (D-C10k-route-a). This file is deviation D2:
it replaces upstream experiments/evaluate_uns.py (which imports an unshipped package) and carries the
runner's projector construction `get_project` (evaluate_uns.py:262-275) verbatim in semantics.
The algorithm modules come from external_prior_art/AnyEdit_mps (deviation D1, device-only diff) and are
imported UNCHANGED; the covariance is injected (D4) by rebinding the module attribute, not by editing it.

Stages (each writes JSON under results/c10k_route_a/):
  alignment   token-alignment gate for all arms (no model)
  projectors  P per band layer from the normalised cached moment + functional gate (wiki keys / A1 edit keys)
  anchor      dynamic anchor: 3 A1 items, MPS fp16 vs CPU fp32, same top-1 + update-norm ratio in [0.5, 2]
  run         --recipe R1|R2|R3 --arms A1_single,A2_coherent2,A7_coined_coined[,stock]   (batch apply per arm, eval, restore)
"""
from __future__ import annotations
import os, sys, io, json, math, time, argparse, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"; os.environ.setdefault("HF_HUB_OFFLINE", "1")
ENGINE_ROOT = f"{LLMDB_ROOT}/memit_dry_run/memit"   # NOT on sys.path: the engine and upstream both own a top-level `util` package
ANYEDIT_MPS = os.environ.get("ANYEDIT_MPS", f"{LLMDB_ROOT}/external_prior_art/AnyEdit_mps")
if ANYEDIT_MPS not in sys.path: sys.path.insert(0, ANYEDIT_MPS)   # upstream's `util` (nethook, layer_stats) is the only `util` here

def resolve_device():
    """The engine's util/device.py resolver, loaded by file path so the engine's `util` never shadows upstream's."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("engine_device", f"{ENGINE_ROOT}/util/device.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.resolve_device()
OUTDIR = f"{LLMDB_ROOT}/results/c10k_route_a"; os.makedirs(OUTDIR, exist_ok=True)
ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
LN2 = math.log(2.0)
# ---- stimuli: copied VERBATIM from experiments/track_c/c10h_anyedit_pilot.py (prereg §3) ----
CANON = "The capital of {} is the city of"
PTEST = ["{}'s capital city is called", "If you visit {}, its capital city is", "The main city and seat of government of {} is"]
FICTION_ALL = ["Zorbland", "Quaxil", "Plurnak", "Vythorn", "Glimsto", "Drennik", "Yastovel", "Crulpane",
               "Mophgar", "Brinduun", "Trannak", "Skornwell", "Fluvane", "Oxbarrow", "Zephquin", "Lurmaxen",
               "Pradnoll", "Kessivar", "Wombryne", "Halquin", "Vorlex", "Quenby", "Marsduq", "Thelby"]
COINED_HEAD = ["Qorvex", "Vindex", "Plurn", "Drennik", "Skorn", "Vythorn", "Crulpane", "Vorlex", "Zephquin", "Lurmax", "Pradnoll", "Kessivar",
               "Wombryne", "Halquin", "Quenby", "Marsduq", "Thelby", "Glimsto", "Mophgar", "Brindu", "Trannak", "Fluvane", "Oxbar", "Yastov"]
COINED_MOD = ["Zentra", "Ploom", "Vask", "Threnn", "Wyxen", "Brakk", "Voneth", "Qurel", "Stavik", "Dwelos", "Phaxis", "Yornel",
              "Klavor", "Druvik", "Spraxil", "Velmor", "Gantho", "Ulvenn", "Treska", "Bloraq", "Cindel", "Marvox", "Ossquin", "Drelth"]
N = int(os.environ.get("N_EDIT", "24"))

def ids(tok, s): return tok(s, add_special_tokens=False)["input_ids"]

def build_stimuli(tok, n=N):
    scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
    caps = sorted({scr[c]["capital"]["truth"] for c in scr})
    single_v = [k for k in caps if len(ids(tok, " " + k)) == 1]
    coherent2 = [k for k in caps if len(ids(tok, " " + k)) == 2]
    fiction = FICTION_ALL[:n]
    assign = lambda pool: {c: pool[(i * 3 + 5) % len(pool)] for i, c in enumerate(fiction)}
    return fiction, {"A1_single": assign(single_v), "A2_coherent2": assign(coherent2),
                     "A7_coined_coined": {c: f"{COINED_HEAD[(i*2+1) % 24]} {COINED_MOD[(i*3+2) % 24]}" for i, c in enumerate(fiction)}}

def real_country_set(tok, k=12):
    """12 real countries NOT edited by any arm, for the unrelated-knowledge locality bound (prereg §3 (a))."""
    scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))["selected"]
    return [(c, scr[c]["capital"]["truth"]) for c in sorted(scr)][:k]

def stock_item():
    return json.load(open(f"{ANYEDIT_MPS}/data/editevery.json"))[0]

# ---- device-neutral eval (from c10i_anyedit_upstream_active_audit.py, device literal removed) ----
def predict(model, tok, prompt, dev):
    import torch
    with torch.no_grad():
        x = tok(prompt, return_tensors="pt").to(dev); pr = torch.softmax(model(**x).logits[0, -1].float(), dim=-1); top = torch.topk(pr, 5)
    return {"id": int(top.indices[0]), "tok": tok.decode([int(top.indices[0])]), "dist": pr.cpu()}

def full_seq_match(model, tok, prompt, target_ids, dev):
    import torch
    with torch.no_grad():
        cur = tok(prompt, return_tensors="pt").to(dev)["input_ids"]; gen = []; logits = []
        for t in target_ids:
            out = model(cur).logits[0, -1].float(); logits.append(float(out[t].detach().cpu())); nxt = int(out.argmax()); gen.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]], device=dev)], dim=1)
    return {"full": gen == list(target_ids), "first": gen[0] == target_ids[0], "gen": gen, "target_logits": logits}

def js(a, b):
    p = a.cpu().double(); q = b.cpu().double(); m = 0.5 * (p + q)
    k = lambda x, y: float((x.clamp_min(1e-12) * (x.clamp_min(1e-12).log() - y.clamp_min(1e-12).log())).sum())
    return 0.5 * k(p, m) + 0.5 * k(q, m)

def locpct(post, pre, prompts): return round(100 * sum(1 - js(post[p]["dist"], pre[p]["dist"]) / LN2 for p in prompts) / len(prompts), 2)

def eval_case(model, tok, q, answer, paras, dev):
    tid = ids(tok, answer); canon = full_seq_match(model, tok, q, tid, dev); para = [full_seq_match(model, tok, p, tid, dev) for p in paras]
    return {"target_ids": tid, "canon_full": canon["full"], "canon_first": canon["first"], "canon_gen": canon["gen"],
            "para_full_hits": [x["full"] for x in para], "para_first_hits": [x["first"] for x in para], "para_gen": [x["gen"] for x in para]}

def arm_summary(rows):
    n = len(rows); npar = len(rows[0]["para_full_hits"]); fulls = sum(sum(r["para_full_hits"]) for r in rows); firsts = sum(sum(r["para_first_hits"]) for r in rows)
    ff = sum(1 for r in rows for a, b in zip(r["para_full_hits"], r["para_first_hits"]) if a and b)
    return {"n_items": n, "canon_full": round(100 * sum(r["canon_full"] for r in rows) / n, 1), "canon_full_hits": f"{sum(r['canon_full'] for r in rows)}/{n}",
            "para_full": round(100 * fulls / (n * npar), 1), "para_full_hits": f"{fulls}/{n*npar}", "para_first": round(100 * firsts / (n * npar), 1),
            "cond_full_given_first": round(ff / firsts, 3) if firsts else None,
            "items_ge2of3": sum(1 for r in rows if sum(r["para_full_hits"]) >= 2), "items_any_full": sum(1 for r in rows if any(r["para_full_hits"]))}

# ---- model / upstream ----
def load_model(dev, dtype):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=dtype, device_map=str(dev), local_files_only=True).eval()
    return tok, model

@contextlib.contextmanager
def pushd(p):
    o = os.getcwd(); os.chdir(p)
    try: yield
    finally: os.chdir(o)

def import_upstream(alg):
    if ANYEDIT_MPS not in sys.path: sys.path.insert(0, ANYEDIT_MPS)
    with pushd(ANYEDIT_MPS):
        if alg == "AlphaEdit_ARE":
            from AlphaEdit_ARE.AlphaEdit_ARE_hparams import AlphaEditAREHyperParams as HP; import AlphaEdit_ARE.AlphaEdit_ARE_main as M
            return HP, M, M.apply_AlphaEdit_ARE_to_model
        from memit_ARE.memit_ARE_hparams import MEMITAREHyperParams as HP; import memit_ARE.memit_ARE_main as M
        return HP, M, M.apply_memit_ARE_to_model

HP_LAYERS = [4, 5, 6, 7, 8]; HP_TMP = "model.layers.{}.mlp.down_proj"   # mirrors configs/hparams/anyedit_alphaedit_are_qwen25_3b.json (asserted in stage_run)

def empty_cache_if_mps(dev):
    import torch, gc
    gc.collect(); torch.mps.empty_cache() if dev.type == "mps" else None

def normalised_cov(layer_name):
    """Deviation D4: upstream get_cov returns stat.mom2.moment() = mom2 / count. Same statistic from the program's cache."""
    import numpy as np, torch
    d = np.load(f"{LLMDB_ROOT}/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/{layer_name}_float32_mom2_t100_100000.npz", allow_pickle=True)
    return torch.from_numpy(d["mom2.mom2"]).float() / float(d["mom2.count"])

def get_project_verbatim(cov_cpu, threshold):
    """evaluate_uns.py:262-275 — cov.cpu(); U,S,_ = svd(cov, full_matrices=False); idx = (S < threshold); return U[:,idx] @ U[:,idx].T"""
    import torch
    U, S, _ = torch.linalg.svd(cov_cpu, full_matrices=False); idx = (S < threshold).nonzero(as_tuple=True)[0]
    return U[:, idx] @ U[:, idx].T, int(idx.numel()), float(S.min()), float(S.max())

def controls_reading():
    """Amendment 1 v2 §8(b): the pre-registered interference reading, carried into every result's scope."""
    c = json.load(open(f"{OUTDIR}/projector_gate_v2_controls.json")); bad = [f"L{l}:{t}" for l, v in c["layers"].items() for t in ("A1", "ARE") if v["interference"][t]["ratio"] >= 1.0]
    return c["interference_reading"] + (f"({','.join(bad)})" if bad else "")

def load_P(path):
    """Amendment 1 v2 §4 wiring parity (enforced): the stacked per-layer projector is loaded verbatim and its full SHA-256 must equal
    the P_sha256 recorded by c10k_route_a_gate_v2.py in results/c10k_route_a/projector_gate_v2.json; mismatch aborts before any edit."""
    import torch, hashlib
    gate = json.load(open(f"{OUTDIR}/projector_gate_v2.json")); sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"projector: {os.path.basename(path)} sha256[:12]={sha[:12]} (gate record {gate['P_sha256'][:12]}, gate_ok={gate['gate_ok']})", flush=True)
    if gate.get("keys_dtype") != "float32":
        raise SystemExit(f"HALT Amendment 2: gate record keys_dtype={gate.get('keys_dtype')!r}; the run stage edits in fp32 and needs a gate measured on fp32 keys")
    if not gate["gate_ok"] or os.path.basename(path) != os.path.basename(gate["P_file"]) or sha != gate["P_sha256"]:
        raise SystemExit(f"HALT wiring parity: {os.path.basename(path)} sha {sha[:12]} does not match the passed gate record {os.path.basename(gate['P_file'])} {gate['P_sha256'][:12]}")
    return torch.load(path), sha[:12]

def band_snapshot(model, hp):
    npd = dict(model.named_parameters()); return {l: npd[f"{hp.rewrite_module_tmp.format(l)}.weight"].detach().clone() for l in hp.layers}

def band_restore(model, hp, snap):
    import torch
    with torch.no_grad():
        npd = dict(model.named_parameters())
        for l in hp.layers: npd[f"{hp.rewrite_module_tmp.format(l)}.weight"][...] = snap[l]

def band_norms(model, hp):
    npd = dict(model.named_parameters()); return {str(l): float(npd[f"{hp.rewrite_module_tmp.format(l)}.weight"].detach().float().norm()) for l in hp.layers}

def layer_inputs(model, tok, texts, layer_name, dev, positions="all"):
    """down_proj input vectors (the MEMIT keys) for texts; positions='all' or 'last'."""
    import torch
    from util import nethook
    out = []
    with torch.no_grad():
        for t in texts:
            x = tok(t, return_tensors="pt").to(dev)
            with nethook.Trace(model, layer_name, retain_input=True, retain_output=False, stop=True) as tr: model(**x)
            k = tr.input[0] if tr.input.dim() == 3 else tr.input
            out.append(k[-1:].float().cpu() if positions == "last" else k.float().cpu())
    return torch.cat(out, 0)

# ---- stages ----
def stage_alignment(a):
    tok, _ = (None, None)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True)
    fiction, arms = build_stimuli(tok); rep = {"ok": True, "arms": {}}
    for arm, V in arms.items():
        rows = []
        for s in fiction:
            q, ans = CANON.format(s), " " + V[s]; aid = ids(tok, ans); suf = ids(tok, q + ans)[-len(aid):]
            rows.append({"subject": s, "value": V[s], "answer_ids": aid, "ntok": len(aid), "aligned": aid == suf, "windows_w1": len(aid), "windows_w50": 1})
            rep["ok"] &= aid == suf
        rep["arms"][arm] = {"aligned": sum(r["aligned"] for r in rows), "n": len(rows), "mean_ntok": round(sum(r["ntok"] for r in rows) / len(rows), 2), "rows": rows}
    json.dump(rep, open(f"{OUTDIR}/alignment.json", "w"), indent=1); print("alignment ok:", rep["ok"], {k: f"{v['aligned']}/{v['n']} ntok={v['mean_ntok']}" for k, v in rep["arms"].items()}); return 0 if rep["ok"] else 1

def stage_projectors(a):
    import torch
    dev = resolve_device(); tok, model = load_model(dev, torch.float16)
    HP, M, _ = import_upstream("AlphaEdit_ARE"); hp = HP.from_json(a.hparams)
    fiction, arms = build_stimuli(tok)
    from datasets import load_dataset
    wiki = load_dataset("wikimedia/wikipedia", "20231101.en")["train"]; texts = [wiki[i]["text"][:600] for i in range(1_000_000, 1_000_000 + 200)]
    a1_prompts = [CANON.format(s) for s in fiction]
    Ps, rep = [], {"hparams": a.hparams, "threshold": hp.nullspace_threshold, "layers": {}}
    for l in hp.layers:
        name = hp.rewrite_module_tmp.format(l); t = time.time()
        P, dims, smin, smax = get_project_verbatim(normalised_cov(name), hp.nullspace_threshold)
        Kw = layer_inputs(model, tok, texts, name, dev); Ke = layer_inputs(model, tok, a1_prompts, name, dev, "last")
        prot = float((Kw @ P).norm(dim=1).mean() / Kw.norm(dim=1).mean()); surv = float((Ke @ P).norm(dim=1).mean() / Ke.norm(dim=1).mean())
        rep["layers"][str(l)] = {"nullspace_dim": dims, "of": P.shape[0], "singular_min": smin, "singular_max": smax, "protection_ratio_wiki": round(prot, 4),
                                 "edit_survival_ratio_A1": round(surv, 4), "n_wiki_keys": int(Kw.shape[0]), "seconds": round(time.time() - t)}
        print(f"  L{l}: dims={dims}/{P.shape[0]} protection={prot:.3f} (≤0.5) survival={surv:.3f} (≥0.2) {rep['layers'][str(l)]['seconds']}s", flush=True)
        Ps.append(P)
    rep["gate"] = {"protection_ok": all(v["protection_ratio_wiki"] <= 0.5 for v in rep["layers"].values()), "survival_ok": all(v["edit_survival_ratio_A1"] >= 0.2 for v in rep["layers"].values())}
    rep["gate"]["ok"] = rep["gate"]["protection_ok"] and rep["gate"]["survival_ok"]
    torch.save(torch.stack(Ps, 0), f"{LLMDB_ROOT}/logs/c10k_route_a_P_{hp.nullspace_threshold}.pt")
    json.dump(rep, open(f"{OUTDIR}/projectors.json", "w"), indent=1); print("projector gate:", rep["gate"]); return 0 if rep["gate"]["ok"] else 1

def run_arm(model, tok, hp, M, apply_fn, alg, arm, V, fiction, dev, P, window):
    """Batch-apply the ported module to all items of one arm (upstream --num_edits mode), evaluate, restore."""
    import torch
    hp.window_size = window; hp.overlap = 0
    items = [{"question": CANON.format(s), "answer": " " + V[s]} for s in fiction] if arm != "stock" else [{"question": stock_item()["question"], "answer": stock_item()["answer"]}]
    real = real_country_set(tok); real_prompts = [CANON.format(c) for c, _ in real]; desc = [f"{s} is described as" for s in fiction]
    pre_real = {p: predict(model, tok, p, dev) for p in real_prompts}; pre_desc = {p: predict(model, tok, p, dev) for p in desc}
    stock = stock_item(); pre_stock = full_seq_match(model, tok, stock["question"], ids(tok, stock["answer"])[:6], dev)
    pre_rows = [] if arm == "stock" else [{"subject": s, "value": V[s], **eval_case(model, tok, CANON.format(s), " " + V[s], [p.format(s) for p in PTEST], dev)} for s in fiction]   # Amendment 2: same-dtype pre-edit reference
    snap = band_snapshot(model, hp); n0 = band_norms(model, hp); t = time.time(); buf = io.StringIO(); err = None
    try:
        with contextlib.redirect_stdout(buf): apply_fn(model, tok, hp, items, **({"P": P} if alg == "AlphaEdit_ARE" else {}))
    except Exception as e:
        err = repr(e)
    secs = round(time.time() - t); n1 = band_norms(model, hp)
    rows = []
    if err is None:
        if arm == "stock":
            post = full_seq_match(model, tok, stock["question"], ids(tok, stock["answer"])[:6], dev); rows = [{"item": "editevery_0", "pre_first6": pre_stock, "post_first6": post}]
        else:
            for s in fiction: rows.append({"subject": s, "value": V[s], **eval_case(model, tok, CANON.format(s), " " + V[s], [p.format(s) for p in PTEST], dev)})
    post_real = {p: predict(model, tok, p, dev) for p in real_prompts}; post_desc = {p: predict(model, tok, p, dev) for p in desc}
    real_ok = sum(1 for (c, truth), p in zip(real, real_prompts) if post_real[p]["tok"].strip().lower() and truth.lower().startswith(post_real[p]["tok"].strip().lower()))
    post_stock = full_seq_match(model, tok, stock["question"], ids(tok, stock["answer"])[:6], dev)
    band_restore(model, hp, snap)
    res = {"alg": alg, "arm": arm, "window_size": window, "n_items": len(items), "apply_seconds": secs, "error": err,
           "update_norm_ratio": {l: round(n1[l] / n0[l], 6) for l in n0}, "stdout_tail": buf.getvalue()[-1500:],
           "summary": arm_summary(rows) if rows and arm != "stock" else None, "pre_summary": arm_summary(pre_rows) if pre_rows else None, "rows": rows, "pre_rows": pre_rows,
           "locality": {"real_capital_top1_correct": f"{real_ok}/{len(real)}", "real_js_locpct": locpct(post_real, pre_real, real_prompts),
                        "stock_item_prefix_pre": pre_stock["gen"], "stock_item_prefix_post": post_stock["gen"], "stock_item_unchanged": pre_stock["gen"] == post_stock["gen"],
                        "described_as_js_locpct": locpct(post_desc, pre_desc, desc)}}
    return res

def stage_run(a):
    import torch
    dev = resolve_device(); tok, model = load_model(dev, torch.float32)
    alg = {"R1": "AlphaEdit_ARE", "R2": "AlphaEdit_ARE", "R3": "memit_ARE"}[a.recipe]; window = {"R1": 1, "R2": 50, "R3": 1}[a.recipe]
    HP, M, apply_fn = import_upstream(alg); hp = HP.from_json(a.hparams if alg == "AlphaEdit_ARE" else a.hparams.replace("alphaedit", "memit"))
    assert list(hp.layers) == HP_LAYERS and hp.rewrite_module_tmp == HP_TMP, (hp.layers, hp.rewrite_module_tmp)
    M.get_cov = lambda model_, tok_, layer_name, *r, **k: normalised_cov(layer_name).to(dev)   # D4 injection (module attribute, not file)
    P, P_sha = load_P(a.P) if alg == "AlphaEdit_ARE" else (None, None)
    fiction, arms = build_stimuli(tok)
    for arm in a.arms.split(","):
        V = arms.get(arm, {}); res = run_arm(model, tok, hp, M, apply_fn, alg, arm, V, fiction, dev, P, window)
        res["decision_id"] = "D-C10k-route-a"; res["class"] = "ported-upstream mechanism lead; not CORPUS evidence until advisor-reviewed"
        res["projector_file"] = os.path.basename(a.P) if P is not None else None; res["projector_sha256_12"] = P_sha
        res["scope"] = f"Qwen2.5-3B base fp32 on MPS (Amendment 2) / {alg} window={window} / {arm} / N={len(fiction)} / 1-seed / hparams {os.path.basename(a.hparams)} / per-layer thresholds (Amendment 1 D8) {os.path.basename(a.P) if P is not None else 'n/a'} / interference={controls_reading()}"
        json.dump(res, open(f"{OUTDIR}/{a.recipe}_w{window}_{arm}.json", "w"), indent=1, default=str)
        print(f"{a.recipe} {alg} w={window} {arm}: err={res['error']} secs={res['apply_seconds']} summary={res['summary']} locality={res['locality']['real_capital_top1_correct']} desc_js={res['locality']['described_as_js_locpct']}", flush=True)
    return 0

def stage_anchor(a):
    """D5 dynamic anchor (Amendment 2: fp32 both legs): 3 A1 items, MPS fp32 vs CPU fp32; same canonical top-1 and update-norm ratio within [0.5, 2]."""
    import torch
    HP, M, apply_fn = import_upstream("AlphaEdit_ARE"); hp = HP.from_json(a.hparams); hp.window_size = 1; hp.overlap = 0
    P, P_sha = load_P(a.P); out = {"projector_file": os.path.basename(a.P), "projector_sha256_12": P_sha}
    for label, dev, dtype in (("mps_fp32", torch.device("mps"), torch.float32), ("cpu_fp32", torch.device("cpu"), torch.float32)):
        tok, model = load_model(dev, dtype); fiction, arms = build_stimuli(tok); V = arms["A1_single"]; subs = fiction[:3]
        M.get_cov = lambda model_, tok_, layer_name, *r, **k: normalised_cov(layer_name).to(dev)
        items = [{"question": CANON.format(s), "answer": " " + V[s]} for s in subs]; n0 = band_norms(model, hp); t = time.time()
        with contextlib.redirect_stdout(io.StringIO()): apply_fn(model, tok, hp, items, P=P)
        n1 = band_norms(model, hp)
        out[label] = {"seconds": round(time.time() - t), "top1": {s: predict(model, tok, CANON.format(s), dev)["tok"] for s in subs},
                      "targets": {s: V[s] for s in subs}, "update_norm_delta": {l: round(abs(n1[l] - n0[l]), 5) for l in n0}}
        del model; torch.mps.empty_cache() if dev.type == "mps" else None
    ratio = {l: (out["mps_fp32"]["update_norm_delta"][l] / out["cpu_fp32"]["update_norm_delta"][l] if out["cpu_fp32"]["update_norm_delta"][l] else None) for l in out["mps_fp32"]["update_norm_delta"]}
    same_top1 = all(out["mps_fp32"]["top1"][s] == out["cpu_fp32"]["top1"][s] for s in out["mps_fp32"]["top1"])
    ok = same_top1 and all(r is not None and 0.5 <= r <= 2.0 for r in ratio.values())
    out.update({"update_norm_delta_ratio_mps_over_cpu": ratio, "same_top1": same_top1, "ok": ok})
    json.dump(out, open(f"{OUTDIR}/anchor.json", "w"), indent=1); print("anchor:", {"same_top1": same_top1, "ratio": ratio, "ok": ok}); return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["alignment", "projectors", "anchor", "run"])
    ap.add_argument("--recipe", default="R1"); ap.add_argument("--arms", default="A1_single,A2_coherent2")
    ap.add_argument("--hparams", default=f"{LLMDB_ROOT}/configs/hparams/anyedit_alphaedit_are_qwen25_3b.json")
    ap.add_argument("--P", default=f"{LLMDB_ROOT}/logs/c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt",
                    help="stacked per-layer projector tensor from c10k_route_a_gate_v2.py (Amendment 1, D8: per-layer thresholds)")
    a = ap.parse_args(); return {"alignment": stage_alignment, "projectors": stage_projectors, "anchor": stage_anchor, "run": stage_run}[a.stage](a)

if __name__ == "__main__":
    sys.exit(main())
