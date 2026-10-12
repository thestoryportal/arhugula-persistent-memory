#!/usr/bin/env python3
"""Route A Amendment 1 v2 §8 controls (advisor FIX-FIRST on v2). CPU/MPS maths only; NO edits.

Per band layer at the chosen per-layer threshold:
  (a) scale-free descriptors of the cutoff: kept-rank fraction dims/11008 and eigen-energy fraction removed  sum(S[S<th])/sum(S)
  (b) projected-interference ratio  I(P)/I(I)  with  I(P) = mean_{e,w} |k_eᵀ P k_w| / ‖P k_e‖²
      over edit keys e (A1 last-prompt-token keys; ARE window-position keys) and the 200-article Wikipedia keys w.
      Reading (pre-registered in the amendment before this ran): ≤ 0.5 protective; (0.5, 1) partial; ≥ 1 non-protective.
  (c) key parity: the ported module reads keys from a right-padded batch forward of question+answer at the window positions
      (AlphaEdit_ARE_main.py:88-107 with compute_z.py:67-91 indices). The gate read them from single unpadded forwards.
      Cosine between the two on 3 A7 items at every window position must be ≥ 0.99, and the positions must agree.
Writes experiments/c10k/runs/c10k_route_a/projector_gate_v2_controls.json."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10k_route_a_launcher as L
import c10k_route_a_gate_v2 as G

def interference(Ke, Kw, Us):
    """mean over (e, w) of |k_e^T P k_w| / ||P k_e||^2, with P = Us Us^T; Us=None means P = I."""
    import torch
    A = Ke if Us is None else Ke @ Us; B = Kw if Us is None else Kw @ Us
    num = (A @ B.T).abs().mean(dim=1); den = (A * A).sum(dim=1)
    return float((num / den).mean())

def window_positions_upstream(nq, na, window_size=1, overlap=0):
    """compute_z.py:67-91 — lookup index per window at window_size=1/overlap=0 is ex_len - len(current_target_ids)."""
    pos, start, cur_len = [], 0, nq
    while start < na:
        end = min(start + window_size, na); cur = end - start
        ex_len = cur_len + (cur - 1 if start == 0 else cur - overlap - 1); cur_len += (cur if start == 0 else cur - overlap)
        pos.append(ex_len - cur); start += window_size - overlap
    return pos

def main():
    import torch
    from util import nethook
    dev = L.resolve_device()
    # Amendment 2 item 1: keys at fp16 (the dtype gate-v2 run 2 used) vs fp32 (the dtype the run stage edits in)
    tok16, m16 = L.load_model(dev, torch.float16); fiction16, arms16 = L.build_stimuli(tok16)
    K16 = {}
    for l in L.HP_LAYERS:
        name = L.HP_TMP.format(l)
        K16[l] = (L.layer_inputs(m16, tok16, [L.CANON.format(s) for s in fiction16], name, dev, "last"),
                  G.are_window_keys(m16, tok16, name, dev, [(L.CANON.format(s), " " + arms16["A7_coined_coined"][s]) for s in fiction16]))
    del m16; L.empty_cache_if_mps(dev)
    tok, model = L.load_model(dev, torch.float32)
    HP, M, _ = L.import_upstream("AlphaEdit_ARE"); hp = HP.from_json(f"{L.LLMDB_ROOT}/code/configs/hparams/anyedit_alphaedit_are_qwen25_3b.json")
    fiction, arms = L.build_stimuli(tok)
    from datasets import load_dataset
    wiki = load_dataset("wikimedia/wikipedia", "20231101.en")["train"]; texts = [wiki[i]["text"][:600] for i in range(1_000_000, 1_000_200)]
    a1 = [L.CANON.format(s) for s in fiction]; a7_items = [(L.CANON.format(s), " " + arms["A7_coined_coined"][s]) for s in fiction]
    gate = json.load(open(f"{L.OUTDIR}/projector_gate_v2.json")); PL = {int(k): v["chosen"] for k, v in gate["layers"].items()}
    rep = {"keys_dtype": "float32", "padding_side": tok.padding_side, "reading": {"interference_protective_max": 0.5, "interference_nonprotective_min": 1.0, "key_parity_cos_min": 0.99}, "layers": {}}
    assert tok.padding_side == "right", f"padding_side={tok.padding_side}: window indices would shift under left padding"
    par_items = a7_items[:3]; batch = tok([q + a for q, a in par_items], padding=True, return_tensors="pt").to(dev)
    for l in hp.layers:
        name = hp.rewrite_module_tmp.format(l); th = PL[l]; t = time.time()
        U, S, _ = torch.linalg.svd(L.normalised_cov(name), full_matrices=False)
        idx = (S < th).nonzero(as_tuple=True)[0]; Us = U[:, idx]
        desc = {"threshold": th, "dims": int(idx.numel()), "kept_rank_fraction": round(float(idx.numel()) / S.numel(), 4), "eigen_energy_fraction_removed": round(float(S[idx].sum() / S.sum()), 6)}
        Kw = L.layer_inputs(model, tok, texts, name, dev); Ka1 = L.layer_inputs(model, tok, a1, name, dev, "last"); Kare = G.are_window_keys(model, tok, name, dev, a7_items)
        d16 = {}
        for tag, k32, k16 in (("A1", Ka1, K16[l][0]), ("ARE", Kare, K16[l][1])):
            cs = torch.nn.functional.cosine_similarity(k32, k16, dim=1); rn = ((k32 - k16).norm(dim=1) / k32.norm(dim=1))
            d16[tag] = {"cos_min": round(float(cs.min()), 6), "cos_mean": round(float(cs.mean()), 6), "rel_norm_diff_max": round(float(rn.max()), 6), "rel_norm_diff_mean": round(float(rn.mean()), 6)}
        inter = {}
        for tag, Ke in (("A1", Ka1), ("ARE", Kare)):
            ip, ii = interference(Ke, Kw, Us), interference(Ke, Kw, None)
            inter[tag] = {"I_P": ip, "I_identity": ii, "ratio": round(ip / ii, 4)}
        # key parity: padded batch (module path) vs single unpadded (gate path)
        with torch.no_grad():
            with nethook.Trace(model, name, retain_input=True, retain_output=False, stop=True) as tr: model(**batch)
            kb = tr.input if tr.input.dim() == 3 else tr.input.unsqueeze(0)   # (3, seq, d) — padded batch
        cos, pos_ok = [], True
        for k, (q, a) in enumerate(par_items):
            nq, na = len(L.ids(tok, q)), len(L.ids(tok, a)); up = window_positions_upstream(nq, na); gp = [nq - 1] + [nq + j for j in range(na - 1)]
            pos_ok &= (up == gp); single = G.are_window_keys(model, tok, name, dev, [(q, a)])
            kbk = kb[k, up].float().cpu(); cos += torch.nn.functional.cosine_similarity(kbk, single, dim=1).tolist()
        rep["layers"][str(l)] = {**desc, "interference": inter, "key_parity": {"positions_agree": bool(pos_ok), "cos_min": round(min(cos), 6), "n_positions": len(cos)}, "fp16_vs_fp32_keys": d16, "seconds": round(time.time() - t)}
        print(f"L{l} @{th}: kept={desc['kept_rank_fraction']} energy_removed={desc['eigen_energy_fraction_removed']:.2e} | interference ratio A1={inter['A1']['ratio']} ARE={inter['ARE']['ratio']} | parity pos={pos_ok} cos_min={min(cos):.6f} | fp16/fp32 cos_min A1={d16['A1']['cos_min']} ARE={d16['ARE']['cos_min']} relnorm_max A1={d16['A1']['rel_norm_diff_max']}", flush=True)
    r = rep["layers"]; mx = max(v["interference"][t]["ratio"] for v in r.values() for t in ("A1", "ARE"))
    rep["interference_reading"] = "protective" if mx <= 0.5 else ("partial" if mx < 1.0 else "non-protective")
    rep["key_parity_ok"] = all(v["key_parity"]["positions_agree"] and v["key_parity"]["cos_min"] >= 0.99 for v in r.values())
    json.dump(rep, open(f"{L.OUTDIR}/projector_gate_v2_controls.json", "w"), indent=1)
    print("controls:", "interference", rep["interference_reading"], "| key parity", "OK" if rep["key_parity_ok"] else "FAIL"); return 0 if rep["key_parity_ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
