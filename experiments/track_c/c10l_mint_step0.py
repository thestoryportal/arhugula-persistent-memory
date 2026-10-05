#!/usr/bin/env python3
"""D-C10l-mint step 0 (no write; one model load): P2 registration inertness, four input-side initialisations of the 24
spare rows (M, G, N, Z), the I-11 step-zero probe per init, P-iv statistics, P3 compute_z convergence on ĥ per init,
and the frozen A1-rare list. Writes results/c10l_mint/step0_probe.json and the init tensors + minted tokenizer under
results/c10l_mint/ (hashed into the JSON). Env: LLMDB_ROOT, OUT.
"""
import os, sys, io, re, json, contextlib, time, subprocess
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["C10_ARMS"] = "A7_coined_coined"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H
import c10l_mint_lib as M
import torch
from transformers import AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z
from memit.memit_main import get_context_templates

RES = f"{LLMDB_ROOT}/results/c10l_mint"
OUT = os.environ.get("OUT", f"{RES}/step0_probe.json")
os.makedirs(f"{RES}/inits", exist_ok=True)
hp = MEMITHyperParams.from_json(H.HP_BASE)
VALUES = [H.ARMS["A7_coined_coined"][c] for c in H.FICTION]


def p3_convergence(ctx, ids):
    """compute_z on the single-token target ĥ (25 steps, harness hparams); full-target probability from the engine's own log."""
    probs = []
    for c, v in zip(H.FICTION, VALUES):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            compute_z(H.model, H.tok, H.req(H.CANON, c, v), hp, hp.layers[-1], ctx)
        found = re.findall(r"avg prob of \[.*?\]\s+([0-9.eE+-]+)", buf.getvalue())
        probs.append(float(found[-1]) if found else None)
    ok = sum(p is not None and p >= 0.98 for p in probs)
    return {"probs": probs, "n_ge_0.98": ok, "pass": ok >= 22}


def main():
    t0 = time.time()
    M.assert_tied(H.model)
    base_tok = AutoTokenizer.from_pretrained(H.ID, revision=H.REV)
    prompts = M.all_harness_prompts(H)
    before = [base_tok(p)["input_ids"] for p in prompts]
    constituents = {v: base_tok(" " + v, add_special_tokens=False)["input_ids"] for v in VALUES}
    ids = M.register(H.tok, VALUES)                                   # P2(b) asserted inside
    after = [H.tok(p)["input_ids"] for p in prompts]
    p2a = sum(a == b for a, b in zip(before, after))
    in_context = [H.tok(H.CANON.format(c) + " " + v, add_special_tokens=False)["input_ids"][-1] == i for c, v, i in zip(H.FICTION, VALUES, ids)]
    H.tok.save_pretrained(f"{RES}/tokenizer_minted")
    tok_files = sorted(os.listdir(f"{RES}/tokenizer_minted"))
    rare = M.a1_rare_list(base_tok)
    fp = subprocess.run([sys.executable, f"{LLMDB_ROOT}/tools/engine_fingerprint.py"], capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": LLMDB_ROOT})
    if fp.returncode != 0:
        raise SystemExit(f"P1 fingerprint FAIL:\n{fp.stdout}{fp.stderr}")   # [LAW:no-silent-failure]
    out = {"decision_id": "D-C10l-mint", "prereg": f"{LLMDB_ROOT}/docs/C10L_MINT_TOKEN_PREREG.md", "step": "step 0",
           "P1_fingerprint": fp.stdout.strip(), "P1_law3": "shared with D-C10l-covgeom run 1 arm A (same session); the arms driver records the reference run",
           "spare_rows": M.VOCAB_ROWS - M.SPARE_START, "minted_ids": ids, "values": VALUES, "constituent_ids": constituents,
           "P2a_prompts_identical": f"{p2a}/{len(prompts)}", "P2a_pass": p2a == len(prompts), "P2b_in_context_last_id_is_minted": sum(in_context),
           "tokenizer_minted_sha256": {f: M.sha256_file(f"{RES}/tokenizer_minted/{f}") for f in tok_files},
           "A1_rare": [{"id": i, "word": w} for i, w in rare], "A1_rare_sha256": M.sha256_text(json.dumps(rare)),
           "A1_rare_note": "rarity proxy = BPE id > 50,000 (merge order), ASCII lowercase alphabetic, len >= 6; not literal corpus frequency rank",
           "G_definition": f"all-but-the-top: base mean removed and top {M.ABTT_K} principal directions of the centred base embedding projected out, constituents averaged, norm-matched; mean not added back (amendment B1)",
           "inits": {}, "reference_random_base_rows": None}
    print(f"P2a {p2a}/{len(prompts)}  P2b in-context {sum(in_context)}/24  ids {ids[0]}..{ids[-1]}  ({time.time()-t0:.0f}s)", flush=True)
    if not out["P2a_pass"]:
        bad = [p for p, a, b in zip(prompts, before, after) if a != b][:5]
        raise SystemExit(f"P2(a) FAILED: registration changed the tokenisation of {len(prompts)-p2a} prompts, e.g. {bad}")
    g = torch.Generator().manual_seed(1)
    ref_idx = torch.randperm(M.SPARE_START, generator=g)[:24]
    out["reference_random_base_rows"] = M.piv_stats(M.embed(H.model)[ref_idx].detach().float().cpu())
    ref_rank = out["reference_random_base_rows"]["effective_rank"]
    ctx = get_context_templates(H.model, H.tok)
    z_rows = M.get_rows(H.model, ids)                                 # the as-is spare rows (init Z), restored after every init
    _base = M.embed(H.model).detach().float().cpu()[:M.SPARE_START]
    U = M.top_directions(_base, _base.mean(0))
    out["G_top_directions_sha256"] = M.sha256_tensor(U)
    for kind in M.INITS:
        rows = M.build_init(H.model, base_tok, VALUES, kind, U=U)
        torch.save(rows, f"{RES}/inits/{kind}.pt")
        M.set_rows(H.model, ids, rows)
        stats = M.piv_stats(rows)
        probe = M.i11_probe(H, VALUES, ids, base_tok)
        collapsed = stats["cos_mean"] > 0.9 or stats["effective_rank"] < 0.75 * ref_rank
        p3 = p3_convergence(ctx, ids)
        reasons = ([f"cannibal>={probe['n_cannibal']}"] if probe["n_cannibal"] >= 3 else []) + ([f"live(init para_full_step0 {probe['para_full_step0']}>2)"] if probe["para_full_step0"] > 2 else []) + ([] if p3["pass"] else [f"P3 compute_z {p3['n_ge_0.98']}/24 < 22"])
        excluded = bool(reasons)   # amendment B1: P3 is fail-closed per init (the lm-head row IS the init)
        out["inits"][kind] = {"piv": stats, "collapsed": collapsed, "probe": probe, "excluded_from_arms": excluded,
                              "exclusion_reason": "; ".join(reasons), "P3_compute_z": p3, "rows_sha256": M.sha256_tensor(rows)}
        print(f"init {kind}: cos_mean={stats['cos_mean']} eff_rank={stats['effective_rank']} (ref {ref_rank}) collapsed={collapsed} | step0 para_full={probe['para_full_step0']}/72 canon={probe['canon_step0']}/24 classes={probe['classes']} excluded={excluded} | P3 {p3['n_ge_0.98']}/24 ({time.time()-t0:.0f}s)", flush=True)
        M.set_rows(H.model, ids, z_rows)
    out["admitted_inits"] = [k for k in M.INITS if not out["inits"][k]["excluded_from_arms"]]
    out["P6_prior"] = "CORPUS/39 A7 para_first 56/72 vs para_full 15/72; CORPUS/36 P(full|first) 0.226"
    if not out["admitted_inits"]:
        out["halt"] = "every init excluded at step 0 (one fix only: next init named in the halt note)"
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"admitted inits: {out['admitted_inits']}  wrote {OUT} ({time.time()-t0:.0f}s)"); print("MINT_STEP0_DONE", flush=True)


if __name__ == "__main__":
    main()
