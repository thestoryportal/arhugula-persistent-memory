#!/usr/bin/env python3
"""D-C10m-diag run D (experiments/c10m/design/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md v2 §2): one process, baseline recipe, arms A1 + A7
on the unmodified harness. Pre-edit: the 24 A7 `zs` (harness compute_z, layer 8) and the in-process injection control
(prereg validity: para >= 44/72, canon >= 22/24 — the run stops before the edit if the control fails). Post-edit hook
(edit still applied): Q1 gold-first-token-constrained read; Q2 edit + inject with the PRE-edit z (binding) and, as a
secondary only, a z recomputed on the edited model. Env: LLMDB_ROOT, LAW3_REF, OUT (+ DECISION_ID / PREREG).
"""
import os, sys, io, json, contextlib, time, subprocess
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["C10_ARMS"] = "A1_single,A7_coined_coined"
os.environ["C10_RECIPES"] = "candidate"                       # one recipe = the baseline hparams under the candidate slot (as c10l_mint_arms.py)
os.environ.setdefault("HP_CANDIDATE", f"{LLMDB_ROOT}/code/configs/hparams/qwen25_3b_memit_hparams.json")
os.environ.setdefault("CANDIDATE_NAME", "A7_diag")
sys.path.insert(0, f"{LLMDB_ROOT}/code/lab/track_c")
import c10e_bandknob as H
import c10l_mint_lib as M
from c10l_covgeom_p6_zinject import Inject, decode, Z_LAYER   # the P6 hook and greedy decoder, unchanged (same model object)
import torch
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z
from memit.memit_main import get_context_templates
from rome.repr_tools import get_words_idxs_in_templates

INJ_PRE_PARA_MIN, INJ_PRE_CANON_MIN = 44, 22   # prereg §3 validity (advisor v1 item 1)
LAW3_REF = os.environ["LAW3_REF"]
law3 = json.load(open(LAW3_REF))["recipes"]["baseline"]["arms"]
if law3["A1_single"]["para_full_n"] < 68 or law3["A2_coherent2"]["para_full_n"] < 68:
    raise SystemExit(f"LAW#3 reference {LAW3_REF} does not pass the envelope")   # [LAW:no-silent-failure]
hp = MEMITHyperParams.from_json(H.HP_BASE)
V = H.ARMS["A7_coined_coined"]
TEMPLATES = [H.CANON] + H.PTEST
DIAG = {}   # pre-edit facts the post-edit hook reads: zs_pre, ctx  [LAW:no-shared-mutable-globals] written once in main, read once in the hook


def fingerprint():
    fp = subprocess.run([sys.executable, f"{LLMDB_ROOT}/code/memit/engine_fingerprint.py"], capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": LLMDB_ROOT})
    if fp.returncode != 0:
        raise SystemExit(f"P1 fingerprint FAIL:\n{fp.stdout}{fp.stderr}")   # [LAW:no-silent-failure]
    return fp.stdout.strip()   # all three lines: status, sha256 (the reader checks the hash here), _cov_cpu count


def subject_idx(template, subj):
    return get_words_idxs_in_templates(H.tok, [template], [subj], "last")[0][0]


@torch.no_grad()
def constrained_full(prompt, tids):
    """Prereg Q1: the gold first value token is forced, the remaining len-1 tokens free-run; match tids[1:].
    Same greedy loop as H.full_seq_match, started one token later."""
    ids = H.tok(prompt, return_tensors="pt").to(H.DEV)["input_ids"]
    cur = torch.cat([ids, torch.tensor([[tids[0]]], device=H.DEV)], dim=1)
    gen = []
    for _ in range(len(tids) - 1):
        nxt = int(H.model(cur).logits[0, -1].argmax())
        gen.append(nxt)
        cur = torch.cat([cur, torch.tensor([[nxt]], device=H.DEV)], dim=1)
    return gen == list(tids[1:])


@torch.no_grad()
def constrained_string(prompt, value, tids):
    """Prereg §2: the string readout of the constrained decode — first token forced, len(tids) + 1 free tokens, text compared (as H.string_match)."""
    ids = H.tok(prompt, return_tensors="pt").to(H.DEV)["input_ids"]
    cur = torch.cat([ids, torch.tensor([[tids[0]]], device=H.DEV)], dim=1)
    for _ in range(len(tids) + 1):
        nxt = int(H.model(cur).logits[0, -1].argmax())
        cur = torch.cat([cur, torch.tensor([[nxt]], device=H.DEV)], dim=1)
    return H.tok.decode(cur[0, ids.shape[1]:].tolist()).startswith(" " + value)


def compute_zs(ctx):
    zs = {}
    for c in H.FICTION:
        with contextlib.redirect_stdout(io.StringIO()):
            zs[c] = compute_z(H.model, H.tok, H.req(H.CANON, c, V[c]), hp, Z_LAYER, ctx).detach()
    return zs


def z_record(zs):
    stack = torch.stack([zs[c].float().cpu() for c in H.FICTION])
    return {"sha256": M.sha256_tensor(stack), "norms": [round(float(zs[c].float().norm()), 3) for c in H.FICTION]}


def inject_sweep(zs, subjects=None):
    """Inject z at the subject-last token of every CANON/PTEST prompt (P6 mechanics) and greedy-decode len(tids).
    `subjects` (default all 24) lets D-C10n-ztransport re-run a subset as its restoration check. [LAW:composability]"""
    rows = []
    for c in (subjects or H.FICTION):
        tids = H.tgt_ids(V[c])
        hits = []
        for t in TEMPLATES:
            with Inject(subject_idx(t, c), zs[c]):
                hits.append(decode(t.format(c), len(tids)) == tids)
        rows.append({"subj": c, "val": V[c], "per_template": hits})
    return {"canon_n": sum(r["per_template"][0] for r in rows), "para_n": sum(sum(r["per_template"][1:]) for r in rows),
            "per_template": {t: sum(r["per_template"][k] for r in rows) for k, t in enumerate(TEMPLATES)}, "rows": rows}


def diag_hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    t0 = time.time()
    con = []
    for c in H.FICTION:
        tids = H.tgt_ids(Vmap[c])
        con.append({"subj": c, "canon_constrained": constrained_full(H.CANON.format(c), tids),
                    "para_constrained": [constrained_full(p.format(c), tids) for p in H.PTEST],
                    "para_constrained_string": [constrained_string(p.format(c), Vmap[c], tids) for p in H.PTEST]})
    constrained = {"canon_n": sum(r["canon_constrained"] for r in con), "para_n": sum(sum(r["para_constrained"]) for r in con),
                   "para_string_n": sum(sum(r["para_constrained_string"]) for r in con), "rows": con}
    print(f"  Q1 constrained: canon {constrained['canon_n']}/24 para {constrained['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    post = inject_sweep(DIAG["zs_pre"])                       # BINDING: the pre-edit z (prereg §2, advisor item 4)
    print(f"  Q2 edit+inject (z_pre): canon {post['canon_n']}/24 para {post['para_n']}/72 per-template {post['per_template']} ({time.time()-t0:.0f}s)", flush=True)
    zs_post = compute_zs(DIAG["ctx"])                         # SECONDARY only: a target recomputed on the edited model
    post2 = inject_sweep(zs_post)
    print(f"  Q2 secondary (z_post): canon {post2['canon_n']}/24 para {post2['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    return {"constrained": constrained, "inj_post_zpre": post, "inj_post_zpost_secondary": post2, "zs_post": z_record(zs_post)}


def main():
    t0 = time.time()
    p1 = fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    zs_pre = compute_zs(ctx)
    DIAG["zs_pre"], DIAG["ctx"] = zs_pre, ctx
    pre = inject_sweep(zs_pre)
    print(f"pre-edit injection control: canon {pre['canon_n']}/24 para {pre['para_n']}/72 per-template {pre['per_template']} ({time.time()-t0:.0f}s)", flush=True)
    head = {"decision_id": os.environ.get("DECISION_ID", "D-C10m-diag"), "prereg": os.environ.get("PREREG"), "P1": {"fingerprint": p1, "law3_reference_run": LAW3_REF},
            "z_layer": Z_LAYER, "zs_pre": z_record(zs_pre), "inj_pre": pre}
    if pre["para_n"] < INJ_PRE_PARA_MIN or pre["canon_n"] < INJ_PRE_CANON_MIN:
        head["invalid"] = f"injection control below the prereg gate (para {pre['para_n']} < {INJ_PRE_PARA_MIN} or canon {pre['canon_n']} < {INJ_PRE_CANON_MIN}); run stopped before the edit"
        json.dump(head, open(H.OUT, "w"), indent=2)
        raise SystemExit(f"HALT: {head['invalid']}")   # [LAW:no-silent-failure] the prereg says the run stops
    H.ARM_HOOKS.append(diag_hook)
    rc = H.main()
    res = json.load(open(H.OUT))
    res.update({k: v for k, v in head.items() if k not in res}); res["P1"] = head["P1"]
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    print("C10M_DIAG_DONE", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
