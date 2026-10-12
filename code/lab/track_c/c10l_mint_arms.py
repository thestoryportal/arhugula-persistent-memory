#!/usr/bin/env python3
"""D-C10l-mint behavioural arms on the unmodified C10 harness (band 4-8, N = 24, one seed, fp16; A1 carried in every run).
  MINT_ARM=multi  -> A7-multi (4-6-token coined strings) + A1            (tokenizer untouched)
  MINT_ARM=rare   -> A1-rare (frozen list from step0_probe.json) + A1    (tokenizer untouched)
  MINT_ARM=G|N|M|Z -> A7-mint-<init> (one minted token per value, rows from experiments/c10l/runs/c10l_mint/inits/<init>.pt) + A1
The write is the harness's subject-keyed my_edit with target " <coined>" -> [ĥ]; full_seq_match on one token is the
binding top-1-id metric; string_match is the string readout. Extra readouts via the harness ARM_HOOKS seam:
para_sibling, post-write cannibal count (I-11 on unrelated prompts), per-position teacher-forced accuracy (multi).
Env: LLMDB_ROOT, MINT_ARM, OUT (set by the launcher), plus DECISION_ID/PREREG.
"""
import os, sys, json
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
ARM = os.environ["MINT_ARM"]
if ARM not in ("multi", "rare", "G", "N", "M", "Z"):
    raise SystemExit(f"MINT_ARM must be multi|rare|G|N|M|Z, got {ARM!r}")
os.environ["C10_ARMS"] = "A1_single,A7_coined_coined"
os.environ["C10_RECIPES"] = "candidate"
os.environ.setdefault("HP_CANDIDATE", f"{LLMDB_ROOT}/code/configs/hparams/qwen25_3b_memit_hparams.json")
os.environ.setdefault("CANDIDATE_NAME", {"multi": "A7_multi", "rare": "A1_rare"}.get(ARM, f"A7_mint_{ARM}"))
sys.path.insert(0, f"{LLMDB_ROOT}/code/lab/track_c")
import c10e_bandknob as H
import c10l_mint_lib as M
import torch

RES = f"{LLMDB_ROOT}/experiments/c10l/runs/c10l_mint"
STEP0_PATH = os.environ.get("MINT_STEP0", f"{RES}/step0_probe.json")   # B3 (second seed): a tagged step-0 file with its own init tensors
step0 = json.load(open(STEP0_PATH))
INIT_TAG = step0.get("init_tag", "")
SAVE_DIR = os.environ.get("MINT_SAVE_DIR")   # B2 (P4): save the edited HF model + minted tokenizer after the A7 arm for GGUF conversion
LAW3_REF = os.environ["LAW3_REF"]   # P1: the D-C10l-covgeom run whose arm A passed the P2 envelope in this session (checked by its reader)
law3 = json.load(open(LAW3_REF))["recipes"]["baseline"]["arms"]
if law3["A1_single"]["para_full_n"] < 68 or law3["A2_coherent2"]["para_full_n"] < 68:
    raise SystemExit(f"LAW#3 reference {LAW3_REF} does not pass the envelope")   # [LAW:no-silent-failure]
VALUES = [H.ARMS["A7_coined_coined"][c] for c in H.FICTION]
if VALUES != step0["values"]:
    raise SystemExit("A7 values differ from step 0")
MINTED = None


@torch.no_grad()
def top1(prompt):
    ids = H.tok(prompt, return_tensors="pt").to(H.DEV)
    return int(H.model(**ids).logits[0, -1].argmax())


def mint_hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined" or MINTED is None:
        return {}
    ids = MINTED
    sib = hits = 0
    per_tok = []
    for k, c in enumerate(H.FICTION):
        t1 = [top1(p.format(c)) for p in H.PTEST]
        h = sum(t == ids[k] for t in t1); s = sum((t in ids and t != ids[k]) for t in t1)
        hits += h; sib += s; per_tok.append({"subj": c, "hits": h, "sibling": s})
    cannibal = sum(sum(top1(u) == i for u in M.UNRELATED) >= 3 for i in ids)
    if SAVE_DIR:   # [LAW:effects-at-boundaries] the one place the edited weights leave the process; the harness restores after this hook
        os.makedirs(SAVE_DIR, exist_ok=True)
        H.model.save_pretrained(SAVE_DIR, safe_serialization=True); H.tok.save_pretrained(SAVE_DIR)
        # P4 parity reference (B2 advisor item 3): the HF-fp16 top-1 id of every prompt the GGUF probe will ask, from the same edited weights
        prompts = {"canon": [H.CANON.format(c) for c in H.FICTION], "para": [p.format(c) for c in H.FICTION for p in H.PTEST],
                   "L1": list(H.L1_PROMPTS), "L3": list(H.L3_PROMPTS), "unrelated": list(M.UNRELATED)}
        ref = {"minted_ids": ids, "prompts": prompts, "top1": {k: [top1(p) for p in v] for k, v in prompts.items()}}
        json.dump(ref, open(f"{SAVE_DIR}/hf_fp16_top1_ids.json", "w"), indent=1)
        print(f"  saved edited model + minted tokenizer + HF top-1 ids -> {SAVE_DIR}", flush=True)
    return {"para_sibling": sib, "para_hits_top1": hits, "post_write_cannibal": cannibal, "per_token": per_tok, "saved_to": SAVE_DIR,
            "step0_para_full": step0["inits"][ARM]["probe"]["para_full_step0"], "para_full_minus_step0": hits - step0["inits"][ARM]["probe"]["para_full_step0"]}


@torch.no_grad()
def multi_hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    pos = {}
    for c in H.FICTION:
        tids = H.tgt_ids(Vmap[c])
        for p in H.PTEST:
            base = H.tok(p.format(c), return_tensors="pt").to(H.DEV)["input_ids"]
            for j in range(len(tids)):
                cur = torch.cat([base, torch.tensor([tids[:j]], device=H.DEV, dtype=base.dtype)], dim=1) if j else base
                hit = int(H.model(cur).logits[0, -1].argmax()) == tids[j]
                d = pos.setdefault(j, [0, 0]); d[0] += hit; d[1] += 1
    return {"per_position_teacher_forced": {str(j): {"hits": v[0], "n": v[1]} for j, v in sorted(pos.items())}}


def main():
    global MINTED
    if ARM == "rare":
        words = [w["word"] for w in step0["A1_rare"]]
        H.ARMS = {"A1_single": H.ARMS["A1_single"], "A1_rare": {c: words[k] for k, c in enumerate(H.FICTION)}}
    elif ARM == "multi":
        H.ARM_HOOKS.append(multi_hook)
    else:
        if ARM not in step0["admitted_inits"]:
            raise SystemExit(f"init {ARM} was excluded at step 0: {step0['inits'][ARM]['exclusion_reason']}")
        M.assert_tied(H.model)
        MINTED = M.register(H.tok, VALUES)
        rows = torch.load(f"{RES}/inits/{ARM}{INIT_TAG}.pt")
        if M.sha256_tensor(rows) != step0["inits"][ARM]["rows_sha256"]:
            raise SystemExit("init rows changed since step 0")
        M.set_rows(H.model, MINTED, rows)
        H.ARM_HOOKS.append(mint_hook)
        for c, v in zip(H.FICTION, VALUES):
            if H.tgt_ids(v) != [MINTED[H.FICTION.index(c)]]:
                raise SystemExit(f"harness tgt_ids({v!r}) is not the minted id")
    print(f"MINT_ARM={ARM} arms={list(H.ARMS)} minted={MINTED is not None} law3_ref={LAW3_REF}", flush=True)
    rc = H.main()
    res = json.load(open(H.OUT))
    res["P1"] = {"law3_reference_run": LAW3_REF, "fingerprint_at_step0": step0["P1_fingerprint"].splitlines()[0]}
    res["mint_arm"] = ARM
    # B1 advisor item 1: the BINDING mint score is post-write minus step-0, promoted to a top-level field so no reader
    # can mistake the raw count for it. [LAW:one-source-of-truth] the raw count stays as the derivation input only.
    arm7 = res["recipes"][os.environ["CANDIDATE_NAME"]]["arms"].get("A7_coined_coined")
    if arm7 is not None and MINTED is not None:
        arm7["para_full_binding_n"] = arm7["para_full_n"] - step0["inits"][ARM]["probe"]["para_full_step0"]
        arm7["para_full_binding_note"] = "BINDING for D-C10l-mint §6 = para_full_n (post-write) - step-0 para_full of this init"
    elif arm7 is not None:
        arm7["para_full_binding_n"] = arm7["para_full_n"]
        arm7["para_full_binding_note"] = "no minted token: binding = para_full_n"
    res["step0_sha256"] = M.sha256_file(STEP0_PATH); res["step0_path"] = STEP0_PATH; res["init_tag"] = INIT_TAG
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    return rc


if __name__ == "__main__":
    sys.exit(main())
