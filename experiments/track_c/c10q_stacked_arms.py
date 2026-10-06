#!/usr/bin/env python3
"""D-C10q-stacked (docs/C10Q_STACKED_SOLVE_PREREG.md): two full harness passes, arms A1 + A2 + A7. In each pass the
standard A7 edit is the single-edit reference; the A7 hook then applies a SECOND edit on top (through the harness's
_ARM_STATE handle and the Z_OVERRIDE seam) and re-evaluates everything while both edits are applied.
  pass S      second edit aimed at z_post (re-solved on the once-edited model)   <- binding
  pass S-sham second edit aimed at z_pre again                                     <- control
Env: LLMDB_ROOT, LAW3_REF. Run identity is forced.
"""
import os, sys, io, json, time, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
# [LAW:parse-dont-validate] the frozen run identity: inherited harness knobs are rejected, not defaulted (implementation review item 1)
for _k in ("MODEL_ID", "MODEL_REV", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_CTX_TEMPLATES", "C10_KEY_LOCUS", "RUN_LABEL"):
    if _k in os.environ:
        raise SystemExit(f"refusing to run with inherited harness knob {_k}={os.environ[_k]!r}; the prereg fixes the harness defaults")
os.environ["C10_ARMS"] = "A1_single,A2_coherent2,A7_coined_coined"
os.environ["C10_RECIPES"] = "candidate"
os.environ["HP_CANDIDATE"] = f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"
os.environ["CANDIDATE_NAME"] = "A7_stacked"
os.environ["DECISION_ID"] = "D-C10q-stacked"
os.environ["PREREG"] = f"{LLMDB_ROOT}/docs/C10Q_STACKED_SOLVE_PREREG.md"
RES = f"{LLMDB_ROOT}/results/c10q_stacked"; os.makedirs(RES, exist_ok=True)
os.environ["OUT"] = f"{RES}/passS.json"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H
import c10m_diag_arms as D            # fingerprint / compute_zs / z_record
import c10n_ztransport_arms as Z      # geometry
from c10p_twopass_arms import FRAME_SUBJECTS, frame_probe   # same six never-edited fictional subjects as CORPUS/49
import torch
from memit.memit_main import get_context_templates

V = H.ARMS["A7_coined_coined"]
ST = {}


def hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    t0 = time.time(); st = H._ARM_STATE
    out = {"same_frame_fictional_single": frame_probe(), "override_hits_before_second_edit": H.Z_OVERRIDE_HITS}
    if ST["pass"] == "S":
        zs_post = D.compute_zs(ST["ctx"]); ST["zs_post"] = zs_post
        out.update({"zs_post": D.z_record(zs_post), "geometry": Z.geometry(ST["zs_pre"], zs_post)})
        target = zs_post
    elif ST["pass"] == "Ssham":
        target = ST["zs_pre"]
    else:   # S-perm: matched-energy negative control — each subject receives the NEXT subject's re-solved target (fixed derangement)
        F = H.FICTION; target = {F[i]: ST["zs_post"][F[(i + 1) % len(F)]] for i in range(len(F))}
        out["permutation"] = {F[i]: F[(i + 1) % len(F)] for i in range(len(F))}
    H.Z_OVERRIDE = {(c, " " + V[c]): target[c] for c in H.FICTION}
    with contextlib.redirect_stdout(io.StringIO()):
        delta2 = H.my_edit(st["hp"], st["requests"], st["P"], st["cache"])   # the SECOND edit, on top of the first, sequential cache
    H.Z_OVERRIDE = None
    stacked = H.eval_arm(Vmap)
    stacked["locality_described_as"] = H.locpct({p: H.predict(p) for p in st["pre_prompts"]}, st["pre_loc"], st["pre_prompts"])
    stacked["locality_axes"] = H.axes_post(st["pre_axes"], list(Vmap.values()))
    out.update({"stacked": {k: v for k, v in stacked.items() if k != "rows"}, "stacked_rows": stacked["rows"], "stacked_delta_norms": delta2,
                "same_frame_fictional_stacked": frame_probe(), "override_hits_after_second_edit": H.Z_OVERRIDE_HITS})
    ax = stacked["locality_axes"]
    print(f"  stacked ({ST['pass']}): canon {stacked['canon_full_n']}/24 para {stacked['para_full_n']}/72 string {stacked['para_string_n']} | L1 {ax['L1_flipped_to_edited_value']}/12 frame {out['same_frame_fictional_stacked']['flips']}/6 described_as {stacked['locality_described_as']} L3 {ax['L3_top1_agree']}/30 | ΔW2 {[round(v['delta_norm'], 1) for v in delta2.values()]} | hits {H.Z_OVERRIDE_HITS} ({time.time()-t0:.0f}s)", flush=True)
    return out


def run_pass(name, label):
    H.OUT = f"{RES}/pass{name}.json"; H.Z_OVERRIDE = None; H.Z_OVERRIDE_HITS = 0; ST["pass"] = name; H.ARM_HOOKS[:] = [hook]
    t0 = time.time(); print(f"=== PASS {name}: {label}", flush=True)
    rc = H.main()
    if rc != 0:
        raise SystemExit(f"HALT: harness returned {rc} in pass {name}")   # [LAW:no-silent-failure]
    res = json.load(open(H.OUT)); res["pass"] = name; res["pass_label"] = label; res["z_override_hits_total"] = H.Z_OVERRIDE_HITS
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    a7 = res["recipes"][os.environ["CANDIDATE_NAME"]]["arms"]["A7_coined_coined"]
    print(f"=== PASS {name} done: single-edit reference canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72; stacked para {a7['extra']['stacked']['para_full_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    return res


def main():
    p1 = D.fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    zs_pre = D.compute_zs(ctx); ST.update(zs_pre=zs_pre, ctx=ctx)
    head = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "P1": {"fingerprint": p1, "law3_reference_run": D.LAW3_REF},
            "z_layer": D.Z_LAYER, "zs_pre": D.z_record(zs_pre), "frame_subjects": FRAME_SUBJECTS, "same_frame_fictional_pre_edit": frame_probe(), "passes": {}}
    run_pass("S", "stacked: second edit aimed at z_post"); head["passes"]["S"] = H.OUT
    head["zs_post"] = D.z_record(ST["zs_post"]); head["geometry"] = Z.geometry(zs_pre, ST["zs_post"])
    run_pass("Ssham", "stacked sham: second edit aimed at z_pre again"); head["passes"]["Ssham"] = H.OUT
    run_pass("Sperm", "stacked matched-energy control: second edit aimed at the next subject's z_post"); head["passes"]["Sperm"] = H.OUT
    json.dump(head, open(f"{RES}/run.json", "w"), indent=2, default=str)
    print("C10Q_STACKED_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
