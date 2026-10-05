#!/usr/bin/env python3
"""D-C10k-keying-ablation §6 v3 frame-bleed probe (advisor v2 item 6).

Question: when a SINGLE last-token-keyed write lands (N = 1, w = 5000), is it keyed to the subject or to the
prompt frame "... is the city of"?  The 24 last-token keys are near-identical across subjects (keygram cos 0.99),
so a landed write is predicted to fire on EVERY prompt that ends in the frame — real countries included.

Reuses the c10e harness's own edit path (my_edit, compute_P, predict, full_seq_match, locpct; engine unmodified,
LAW#5).  P is computed once and shared by all probes; weights are restored after each edit.

Env: LLMDB_ROOT; FB_OFFSETS (default "0,1,2"); FB_LOCI (default "last,subject"); OUT.
Output: results/c10k_keying_ablation/n1/framebleed.json
"""
import os, sys, io, json, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["N_EDIT"] = "24"; os.environ["C10_SUBJECT_OFFSET"] = "0"; os.environ["C10_ARMS"] = "A1_single"
os.environ.setdefault("C10_CTX_TEMPLATES", "on")
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H   # loads the model; chdir to the engine root
import torch

OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/results/c10k_keying_ablation/n1/framebleed.json")
OFFSETS = [int(x) for x in os.environ.get("FB_OFFSETS", "0,1,2").split(",")]
LOCI = os.environ.get("FB_LOCI", "last,subject").split(",")
HP = f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"

scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))["selected"]
REAL = [(c, scr[c]["capital"]["truth"]) for c in sorted(scr)][:12]          # Route A's real-country locality set
REAL_PROMPTS = [H.CANON.format(c) for c, _ in REAL]
BYSTANDERS = H.FICTION[12:18]                                                 # fictional subjects never edited in this probe
BY_PROMPTS = [H.CANON.format(c) for c in BYSTANDERS]
VMAP = H.ARMS["A1_single"]

def frame_counts(post, pre, value_id):
    flips = sum(1 for p in post if post[p]["id"] == value_id and pre[p]["id"] != value_id)
    return flips

def real_correct(post):
    return sum(1 for (c, truth), p in zip(REAL, REAL_PROMPTS)
               if post[p]["tok"].strip().lower() and truth.lower().startswith(post[p]["tok"].strip().lower()))

def main():
    hp = H.MEMITHyperParams.from_json(HP)
    base_snap = H.snap_layers(hp)
    print("computing P (once)", flush=True)
    P = H.compute_P(hp)
    pre_real = {p: H.predict(p) for p in REAL_PROMPTS}
    pre_by = {p: H.predict(p) for p in BY_PROMPTS}
    rows = []
    for off in OFFSETS:
        c = H.FICTION[off]; val = VMAP[c]; vid = H.tgt_ids(val)[0]
        for locus in LOCI:
            H.restore_layers(hp, base_snap)
            cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
            if locus == "last":
                rq = H.req("The capital of {}", f"{c} is the city of", val)
            else:
                rq = H.req(H.CANON, c, val)
            desc = [f"{c} is described as"]
            pre_desc = {p: H.predict(p) for p in desc}
            with contextlib.redirect_stdout(io.StringIO()):
                delta = H.my_edit(hp, [rq], P, cache)
            canon = H.full_seq_match(H.CANON.format(c), H.tgt_ids(val))[0]
            para = [H.full_seq_match(p.format(c), H.tgt_ids(val))[0] for p in H.PTEST]
            post_real = {p: H.predict(p) for p in REAL_PROMPTS}
            post_by = {p: H.predict(p) for p in BY_PROMPTS}
            post_desc = {p: H.predict(p) for p in desc}
            row = {
                "subject": c, "value": val, "locus": locus,
                "canon_full": bool(canon), "para_hits": int(sum(para)),
                "real_flipped_to_value": frame_counts(post_real, pre_real, vid), "real_top1_correct_post": real_correct(post_real),
                "real_top1_correct_pre": real_correct(pre_real), "real_js_locpct": H.locpct(post_real, pre_real, REAL_PROMPTS),
                "bystander_flipped_to_value": frame_counts(post_by, pre_by, vid), "n_real": len(REAL), "n_bystanders": len(BYSTANDERS),
                "described_as_js": H.locpct(post_desc, pre_desc, desc),
                "real_post_top1": {c2: post_real[p]["tok"] for (c2, _), p in zip(REAL, REAL_PROMPTS)},
                "bystander_post_top1": {c2: post_by[p]["tok"] for c2, p in zip(BYSTANDERS, BY_PROMPTS)},
                "rel_delta_norm": {k: round(v["relative_delta_norm"], 4) for k, v in delta.items()},
            }
            rows.append(row)
            print(f"FB: {c:10} {locus:8} canon={row['canon_full']} para={row['para_hits']}/3 "
                  f"real_flip={row['real_flipped_to_value']}/{len(REAL)} real_ok={row['real_top1_correct_post']}/{len(REAL)} (pre {row['real_top1_correct_pre']}) "
                  f"real_js={row['real_js_locpct']} bystander_flip={row['bystander_flipped_to_value']}/{len(BYSTANDERS)} desc_js={row['described_as_js']}", flush=True)
            json.dump({"decision_id": "D-C10k-keying-ablation", "probe": "frame-bleed (prereg §6 v3)", "real": REAL, "bystanders": BYSTANDERS,
                       "ridge_weight": hp.mom2_update_weight, "rows": rows}, open(OUT, "w"), indent=1)
    H.restore_layers(hp, base_snap)
    print("FB: DONE", flush=True)

if __name__ == "__main__":
    main()
