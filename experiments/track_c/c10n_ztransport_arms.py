#!/usr/bin/env python3
"""D-C10n-ztransport (docs/C10N_ZTRANSPORT_PREREG.md): the 2 x 2 of {z_pre, z_post} x {pre-edit model, post-edit model}.
  A = z_pre -> pre-edit model (control, before the edit)      B = z_pre -> post-edit model (inside the post-edit hook)
  C = z_post -> post-edit model (inside the hook)             D = z_post -> pre-edit model (after H.main() restored the base weights)
plus per-subject geometry (norms, difference norm, cosine). Reuses the D-C10m-diag functions unchanged.
Env: LLMDB_ROOT, LAW3_REF, OUT (+ DECISION_ID / PREREG).
"""
import os, sys, json, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ.setdefault("CANDIDATE_NAME", "A7_ztransport")
# [LAW:parse-dont-validate] provenance and output are fixed here, before the harness reads its own (stale) defaults
os.environ.setdefault("DECISION_ID", "D-C10n-ztransport")
os.environ.setdefault("PREREG", f"{LLMDB_ROOT}/docs/C10N_ZTRANSPORT_PREREG.md")
os.environ.setdefault("OUT", f"{LLMDB_ROOT}/results/c10n_ztransport/run.json")
os.makedirs(os.path.dirname(os.environ["OUT"]), exist_ok=True)
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10m_diag_arms as D      # sets the arms/recipe env, imports the harness, checks LAW3_REF, provides compute_zs / inject_sweep / z_record / fingerprint
import torch
from memit.memit_main import get_context_templates

H = D.H
ZT = {}   # pre-edit facts for the hook: zs_pre, ctx; the hook adds zs_post  [LAW:no-shared-mutable-globals] one writer per key


def geometry(zs_pre, zs_post):
    rows = []
    for c in H.FICTION:
        p, q = zs_pre[c].float().cpu(), zs_post[c].float().cpu()
        rows.append({"subj": c, "norm_pre": round(float(p.norm()), 3), "norm_post": round(float(q.norm()), 3),
                     "diff_norm": round(float((q - p).norm()), 3), "rel_diff": round(float((q - p).norm() / p.norm()), 4),
                     "cosine": round(float(torch.dot(p, q) / (p.norm() * q.norm())), 4)})
    n = len(rows)
    return {"rows": rows, "mean_cosine": round(sum(r["cosine"] for r in rows) / n, 4), "mean_rel_diff": round(sum(r["rel_diff"] for r in rows) / n, 4),
            "min_cosine": min(r["cosine"] for r in rows), "max_cosine": max(r["cosine"] for r in rows)}


def hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    t0 = time.time()
    zs_post = D.compute_zs(ZT["ctx"]); ZT["zs_post"] = zs_post
    B = D.inject_sweep(ZT["zs_pre"]); print(f"  cell B z_pre->post: canon {B['canon_n']}/24 para {B['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    C = D.inject_sweep(zs_post);      print(f"  cell C z_post->post: canon {C['canon_n']}/24 para {C['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    return {"cell_B_zpre_post": B, "cell_C_zpost_post": C, "zs_post": D.z_record(zs_post)}


def main():
    t0 = time.time()
    p1 = D.fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    zs_pre = D.compute_zs(ctx); ZT.update(zs_pre=zs_pre, ctx=ctx)
    A = D.inject_sweep(zs_pre)
    print(f"cell A z_pre->pre (control): canon {A['canon_n']}/24 para {A['para_n']}/72 per-template {A['per_template']} ({time.time()-t0:.0f}s)", flush=True)
    head = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "P1": {"fingerprint": p1, "law3_reference_run": D.LAW3_REF},
            "z_layer": D.Z_LAYER, "zs_pre": D.z_record(zs_pre), "cell_A_zpre_pre": A}
    if A["para_n"] < D.INJ_PRE_PARA_MIN or A["canon_n"] < D.INJ_PRE_CANON_MIN:
        head["invalid"] = f"cell A control below the gate (para {A['para_n']} < {D.INJ_PRE_PARA_MIN} or canon {A['canon_n']} < {D.INJ_PRE_CANON_MIN}); run stopped before the edit"
        json.dump(head, open(H.OUT, "w"), indent=2); raise SystemExit(f"HALT: {head['invalid']}")   # [LAW:no-silent-failure]
    H.ARM_HOOKS.append(hook)
    rc = H.main()                                   # run_recipe restores the base weights before returning
    A2 = D.inject_sweep(zs_pre)                     # prereg v2 §2.4: the WHOLE cell A sweep repeated on the restored weights
    key = lambda rows: [(r["subj"], r["val"], r["per_template"]) for r in rows]   # subject identity + hit rows (advisor item 3)
    restored = key(A2["rows"]) == key(A["rows"])
    head["restoration_check"] = {"scope": "all 24 subjects x 4 templates, compared on (subj, val, per_template)", "post_restore_cell_A": A2, "identical": restored}
    print(f"restoration check (full cell A repeat): canon {A2['canon_n']}/24 para {A2['para_n']}/72 identical={restored} ({time.time()-t0:.0f}s)", flush=True)
    res = json.load(open(H.OUT)); res.update(head)   # the C10n header overrides the harness's own decision_id / prereg (advisor item 1)
    if not restored:
        res["invalid"] = "base weights not restored after H.main(): cell D not measured"
        json.dump(res, open(H.OUT, "w"), indent=2, default=str); raise SystemExit("HALT: restoration check failed")   # [LAW:no-silent-failure]
    Dc = D.inject_sweep(ZT["zs_post"])
    print(f"cell D z_post->pre: canon {Dc['canon_n']}/24 para {Dc['para_n']}/72 per-template {Dc['per_template']} ({time.time()-t0:.0f}s)", flush=True)
    res["cell_D_zpost_pre"] = Dc; res["geometry"] = geometry(zs_pre, ZT["zs_post"])
    print(f"geometry: mean cosine {res['geometry']['mean_cosine']} (min {res['geometry']['min_cosine']}, max {res['geometry']['max_cosine']}), mean rel diff {res['geometry']['mean_rel_diff']}", flush=True)
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    print("C10N_ZTRANSPORT_DONE", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
