#!/usr/bin/env python3
"""D-C10p-twopass (docs/C10P_TWOPASS_SOLVE_PREREG.md): three full harness passes in one process, arms A1 + A2 + A7.
  pass 1 baseline (engine targets; the A7 hook re-solves z_post on the once-edited model)
  pass 2 sham     (fresh edit aimed at the pre-edit z_pre through the Z_OVERRIDE seam: must reproduce pass 1)
  pass 3 two-pass (fresh edit aimed at z_post)                                           <- binding
Env: LLMDB_ROOT, LAW3_REF; OUT dir / DECISION_ID / PREREG default to this decision's paths.
"""
import os, sys, json, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["C10_ARMS"] = "A1_single,A2_coherent2,A7_coined_coined"      # A2 is a locality gate here (prereg §3)
os.environ["C10_RECIPES"] = "candidate"
os.environ.setdefault("HP_CANDIDATE", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")
os.environ.setdefault("CANDIDATE_NAME", "A7_twopass")
os.environ.setdefault("DECISION_ID", "D-C10p-twopass")
os.environ.setdefault("PREREG", f"{LLMDB_ROOT}/docs/C10P_TWOPASS_SOLVE_PREREG.md")
RES = os.environ.get("C10P_OUT_DIR", f"{LLMDB_ROOT}/results/c10p_twopass"); os.makedirs(RES, exist_ok=True)
os.environ.setdefault("OUT", f"{RES}/pass1.json")
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H             # loaded FIRST with the three arms above; later library imports cannot change H.ARMS
import c10m_diag_arms as D            # fingerprint / compute_zs / z_record (its own env writes land after H is built)
import c10n_ztransport_arms as Z      # geometry
import torch
from memit.memit_main import get_context_templates

V = H.ARMS["A7_coined_coined"]
# CORPUS/43 same-frame locality: never-edited fictional subjects in the CANON frame (none is in H.FICTION); a flip = top-1
# equals the first token of any edited A7 value. The real-country half of that probe is the harness's L1 axis.
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]
assert not set(FRAME_SUBJECTS) & set(H.FICTION)
ST = {}


@torch.no_grad()
def frame_probe():
    firsts = {H.tgt_ids(V[c])[0] for c in H.FICTION}
    rows = []
    for s in FRAME_SUBJECTS:
        ids = H.tok(H.CANON.format(s), return_tensors="pt").to(H.DEV)
        t = int(H.model(**ids).logits[0, -1].argmax()); rows.append({"subj": s, "top1": t, "tok": H.tok.decode([t]), "flip": t in firsts})
    return {"flips": sum(r["flip"] for r in rows), "n": len(rows), "rows": rows}


def hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    out = {"same_frame_fictional": frame_probe(), "z_override_hits": H.Z_OVERRIDE_HITS}
    print(f"  hook: same-frame fictional flips {out['same_frame_fictional']['flips']}/{out['same_frame_fictional']['n']}; override hits so far {out['z_override_hits']}", flush=True)
    if ST.get("pass") == 1:
        zs_post = D.compute_zs(ST["ctx"]); ST["zs_post"] = zs_post
        g = Z.geometry(ST["zs_pre"], zs_post)
        print(f"  pass 1 hook: z_post re-solved on the edited model; mean cosine {g['mean_cosine']} mean displacement {g['mean_rel_diff']}", flush=True)
        out.update({"zs_post": D.z_record(zs_post), "geometry": g})
    return out


def run_pass(n, override, label):
    H.OUT = f"{RES}/pass{n}.json"
    H.Z_OVERRIDE = override; H.Z_OVERRIDE_HITS = 0; ST["pass"] = n
    H.ARM_HOOKS[:] = [hook]
    t0 = time.time(); print(f"=== PASS {n} {label}: Z_OVERRIDE={'None' if override is None else f'{len(override)} targets'}", flush=True)
    rc = H.main()
    if rc != 0:
        raise SystemExit(f"HALT: harness returned {rc} in pass {n}")   # [LAW:no-silent-failure]
    res = json.load(open(H.OUT)); res["pass"] = n; res["pass_label"] = label; res["z_override"] = None if override is None else label
    res["z_override_hits_total"] = H.Z_OVERRIDE_HITS   # expected 0 in pass 1, exactly 1 (the A7 arm) in passes 2 and 3
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    a7 = res["recipes"][os.environ["CANDIDATE_NAME"]]["arms"]["A7_coined_coined"]
    print(f"=== PASS {n} done: A7 canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72 string {a7['para_string_n']} | L1 {a7['locality_axes']['L1_flipped_to_edited_value']}/12 L3 {a7['locality_axes']['L3_top1_agree']}/30 ({time.time()-t0:.0f}s)", flush=True)
    return res


def main():
    p1 = D.fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    zs_pre = D.compute_zs(ctx); ST.update(zs_pre=zs_pre, ctx=ctx)
    key = {c: (c, " " + V[c]) for c in H.FICTION}          # the harness keys requests by (subject, target string) — H.req adds the leading space
    head = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "P1": {"fingerprint": p1, "law3_reference_run": D.LAW3_REF},
            "z_layer": D.Z_LAYER, "zs_pre": D.z_record(zs_pre), "frame_subjects": FRAME_SUBJECTS, "same_frame_fictional_pre_edit": frame_probe(), "passes": {}}
    r1 = run_pass(1, None, "baseline (engine targets)")
    head["passes"]["1"] = H.OUT
    zs_post = ST["zs_post"]; head["zs_post"] = D.z_record(zs_post); head["geometry"] = Z.geometry(zs_pre, zs_post)
    run_pass(2, {key[c]: zs_pre[c] for c in H.FICTION}, "sham (fresh edit aimed at z_pre)"); head["passes"]["2"] = H.OUT
    run_pass(3, {key[c]: zs_post[c] for c in H.FICTION}, "two-pass (fresh edit aimed at z_post)"); head["passes"]["3"] = H.OUT
    H.Z_OVERRIDE = None
    json.dump(head, open(f"{RES}/run.json", "w"), indent=2, default=str)
    print("C10P_TWOPASS_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
