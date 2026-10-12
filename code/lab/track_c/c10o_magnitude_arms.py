#!/usr/bin/env python3
"""D-C10o-magnitude (experiments/c10o/design/C10O_MAGNITUDE_DIRECTION_PREREG.md): on the EDITED model, inject
  B  z_pre                              C  z_post
  E1 z_pre * (|z_post|/|z_pre|)   magnitude alone      E2 z_post * (|z_pre|/|z_post|)   direction alone
plus A (z_pre, pre-edit control), and E1', E2' on the restored (unedited) weights. Reuses the D-C10m / D-C10n functions.
Env: LLMDB_ROOT, LAW3_REF; OUT / DECISION_ID / PREREG default to this decision's paths.
"""
import os, sys, json, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ.setdefault("CANDIDATE_NAME", "A7_magnitude")
os.environ.setdefault("DECISION_ID", "D-C10o-magnitude")
os.environ.setdefault("PREREG", f"{LLMDB_ROOT}/experiments/c10o/design/C10O_MAGNITUDE_DIRECTION_PREREG.md")
os.environ.setdefault("OUT", f"{LLMDB_ROOT}/experiments/c10o/runs/c10o_magnitude/run.json")
os.makedirs(os.path.dirname(os.environ["OUT"]), exist_ok=True)
sys.path.insert(0, f"{LLMDB_ROOT}/code/lab/track_c")
import c10m_diag_arms as D            # arms/recipe env, harness import, LAW3_REF check, compute_zs / inject_sweep / z_record / fingerprint
import c10n_ztransport_arms as Z      # geometry(); its own OUT default is pre-empted by the setdefault above
import torch
from memit.memit_main import get_context_templates

H = D.H
A_MIN, A_HIGH = 38, 44
ST = {}   # pre-edit facts for the hook: zs_pre, ctx; the hook adds zs_post, e1, e2


def synthetic(zs_pre, zs_post):
    """E1: original direction at the re-solved norm; E2: re-solved direction at the original norm;
    E3: re-solved direction scaled so its projection onto z_pre equals |z_pre| (projection-preserving). [LAW:effects-at-boundaries] pure."""
    e1, e2, e3, ratio, proj = {}, {}, {}, {}, {}
    for c in H.FICTION:
        p, q = zs_pre[c].float(), zs_post[c].float()
        r = float(q.norm() / p.norm()); ratio[c] = round(r, 4)
        dot = float(torch.dot(q, p / p.norm()))          # component of z_post along the unit z_pre
        proj[c] = round(dot / float(p.norm()), 4)        # that component as a fraction of |z_pre|
        if dot <= 0:
            raise SystemExit(f"E3 undefined for {c}: z_post has no positive component along z_pre (dot {dot:.3f})")   # [LAW:no-silent-failure]
        e1[c] = (p * r).to(zs_pre[c].dtype)
        e2[c] = (q / r).to(zs_post[c].dtype)
        e3[c] = (q * float(p.norm()) / dot).to(zs_post[c].dtype)
    return e1, e2, e3, ratio, proj


def hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    t0 = time.time()
    zs_post = D.compute_zs(ST["ctx"]); ST["zs_post"] = zs_post
    e1, e2, e3, ratio, proj = synthetic(ST["zs_pre"], zs_post); ST["e1"], ST["e2"], ST["e3"] = e1, e2, e3
    cells = {}
    for name, zs in (("cell_B_zpre", ST["zs_pre"]), ("cell_C_zpost", zs_post), ("cell_E1_magnitude", e1), ("cell_E2_direction", e2), ("cell_E3_projection", e3)):
        cells[name] = D.inject_sweep(zs)
        print(f"  {name}: canon {cells[name]['canon_n']}/24 para {cells[name]['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    return {**cells, "norm_ratio": ratio, "projection_fraction": proj, "zs_post": D.z_record(zs_post), "geometry": Z.geometry(ST["zs_pre"], zs_post)}


def main():
    t0 = time.time()
    p1 = D.fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    zs_pre = D.compute_zs(ctx); ST.update(zs_pre=zs_pre, ctx=ctx)
    A = D.inject_sweep(zs_pre)
    stratum = "HIGH-CONTROL" if A["para_n"] >= A_HIGH else ("LOW-CONTROL" if A["para_n"] >= A_MIN else "OUT-OF-RANGE")
    print(f"cell A z_pre->pre (control): canon {A['canon_n']}/24 para {A['para_n']}/72 {A['per_template']} stratum {stratum} ({time.time()-t0:.0f}s)", flush=True)
    head = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "P1": {"fingerprint": p1, "law3_reference_run": D.LAW3_REF},
            "z_layer": D.Z_LAYER, "zs_pre": D.z_record(zs_pre), "cell_A_zpre_pre": A, "control_stratum": stratum}
    if A["para_n"] < A_MIN or A["canon_n"] < D.INJ_PRE_CANON_MIN:
        head["invalid"] = f"cell A outside the instrument range (para {A['para_n']} < {A_MIN} or canon {A['canon_n']} < {D.INJ_PRE_CANON_MIN}); run stopped before the edit"
        json.dump(head, open(H.OUT, "w"), indent=2); raise SystemExit(f"HALT: {head['invalid']}")   # [LAW:no-silent-failure]
    H.ARM_HOOKS.append(hook)
    rc = H.main()
    A2 = D.inject_sweep(zs_pre)
    key = lambda rows: [(r["subj"], r["val"], r["per_template"]) for r in rows]
    restored = key(A2["rows"]) == key(A["rows"])
    head["restoration_check"] = {"scope": "all 24 subjects x 4 templates, compared on (subj, val, per_template)", "post_restore_cell_A": A2, "identical": restored}
    print(f"restoration check: identical={restored} ({time.time()-t0:.0f}s)", flush=True)
    res = json.load(open(H.OUT)); res.update(head)
    if not restored:
        res["invalid"] = "base weights not restored after H.main(): E1'/E2'/E3' not measured"
        json.dump(res, open(H.OUT, "w"), indent=2, default=str); raise SystemExit("HALT: restoration check failed")   # [LAW:no-silent-failure]
    res["cell_E1prime_magnitude_pre"] = D.inject_sweep(ST["e1"]); res["cell_E2prime_direction_pre"] = D.inject_sweep(ST["e2"]); res["cell_E3prime_projection_pre"] = D.inject_sweep(ST["e3"])
    print(f"unedited: E1' {res['cell_E1prime_magnitude_pre']['para_n']}/72  E2' {res['cell_E2prime_direction_pre']['para_n']}/72  E3' {res['cell_E3prime_projection_pre']['para_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    print("C10O_MAGNITUDE_DONE", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
