#!/usr/bin/env python3
# RETIRED 2026-10-06 (D-C10r-impl-1) — do not run. Superseded by docs/AUTORESEARCH.md (experiments/track_c/autoresearch_c10/).
"""autoresearch re-aim loop — ONE edit experiment under the current knobs.json (experiments/track_c/autoresearch_reaim/program.md).
FENCED (DISCIPLINE §3): an optimizer's fixed script. Output is a CANDIDATE summary under results/autoresearch_reaim/<tag>/iter_<n>/;
never CORPUS/, ledgers, runbook, checkpoint or memory. Engine unmodified; harness unmodified (the Z_OVERRIDE / _ARM_STATE seams).

Usage: run_iteration.py <tag> <iter>      (env: LLMDB_ROOT, LAW3_REF; knobs read from knobs.json beside this file)

Knobs (parsed ONCE into Knobs below; every knob varies a VALUE — the targets, the hparams file, the ridge — not which steps run):
  resolve_rounds R   number of re-solves on the edited model (0 = engine targets only)
  stack              false: fresh edits from base — passes 0..R, pass k aimed at z_k (k = 0: engine targets); the hook of pass k < R
                            re-solves z_{k+1} on that pass's edited model. The final pass is the candidate state.
                     true:  ONE pass; the hook applies R sequential extra edits on top of the first (D-C10q-stacked mechanics), each
                            aimed at a re-solve on the current model.
  write_cap          stack=true only: each extra edit's ||dW_extra|| / ||dW_1|| is capped by rescaling its residual (exact — the solve
                     is linear in the residual: measure, restore, rescale, redo). null = uncapped. Refused with stack=false (loud).
  z_blend b          each aimed target = z_prev + b * (z_resolved - z_prev); 1.0 = the re-solved target, 0.0 = no re-aim
  layers [a, b]      the contiguous edit band (hparams file written per iteration); z-layer = b
  ridge              the harness solve's L2; applied AFTER the LAW#5 parity gate (which always runs at the harness default 1.0)
  resolve_steps      compute_z steps for every re-solve (hparams v_num_grad_steps; also the first edit's)
"""
import os, sys, io, json, time, contextlib, hashlib, subprocess
from dataclasses import dataclass
from typing import Optional

LLMDB_ROOT = os.environ["LLMDB_ROOT"]
HERE = os.path.dirname(os.path.abspath(__file__))
TAG, ITER = sys.argv[1], int(sys.argv[2])
OUTDIR = f"{LLMDB_ROOT}/results/autoresearch_reaim/{TAG}/iter_{ITER:02d}"; os.makedirs(OUTDIR, exist_ok=True)
for _k in ("MODEL_ID", "MODEL_REV", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_CTX_TEMPLATES", "C10_KEY_LOCUS", "RUN_LABEL"):
    if _k in os.environ:   # [LAW:parse-dont-validate] same run-identity rejection as the D-C10q driver
        raise SystemExit(f"refusing to run with inherited harness knob {_k}={os.environ[_k]!r}")


@dataclass(frozen=True)
class Knobs:   # [LAW:types-are-the-program] the one legal shape of an iteration; illegal combinations die here, not in the loop
    resolve_rounds: int
    stack: bool
    write_cap: Optional[float]
    z_blend: float
    layers: tuple
    ridge: float
    resolve_steps: int

    @staticmethod
    def parse(d):
        k = Knobs(int(d["resolve_rounds"]), bool(d["stack"]), None if d["write_cap"] is None else float(d["write_cap"]), float(d["z_blend"]),
                  tuple(range(int(d["layers"][0]), int(d["layers"][1]) + 1)), float(d["ridge"]), int(d["resolve_steps"]))
        if not 0 <= k.resolve_rounds <= 3: raise SystemExit("resolve_rounds must be 0..3")
        if k.write_cap is not None and not k.stack: raise SystemExit("write_cap applies to stack=true only (fresh mode scales through z_blend)")
        if k.write_cap is not None and k.write_cap <= 0: raise SystemExit("write_cap must be > 0")
        if not 0.0 <= k.z_blend <= 1.0: raise SystemExit("z_blend must be in [0, 1]")
        if not (4 <= k.layers[0] <= k.layers[-1] <= 12): raise SystemExit("layers must be a contiguous band within 4..12")
        if k.ridge <= 0 or k.resolve_steps < 1: raise SystemExit("ridge must be > 0 and resolve_steps >= 1")
        return k


KNOBS_RAW = open(f"{HERE}/knobs.json").read()
K = Knobs.parse(json.loads(KNOBS_RAW))
KNOBS_SHA = hashlib.sha256(KNOBS_RAW.encode()).hexdigest()[:8]
json.dump(json.loads(KNOBS_RAW), open(f"{OUTDIR}/knobs.json", "w"), indent=2)

# the iteration's hparams file: the band and the re-solve steps are VALUES in a file the harness already reads  [LAW:dataflow-not-control-flow]
base_hp = json.load(open(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"))
base_hp["layers"] = list(K.layers); base_hp["v_num_grad_steps"] = K.resolve_steps
HP_FILE = f"{OUTDIR}/hparams.json"; json.dump(base_hp, open(HP_FILE, "w"), indent=2)

os.environ["C10_ARMS"] = "A1_single,A2_coherent2,A7_coined_coined"
os.environ["C10_RECIPES"] = "candidate"
os.environ["HP_CANDIDATE"] = HP_FILE
os.environ["CANDIDATE_NAME"] = "A7_reaim"
os.environ["DECISION_ID"] = f"T-autoresearch-twopass/{TAG}"     # a fenced tool run, not a decision
os.environ["PREREG"] = f"{LLMDB_ROOT}/experiments/track_c/autoresearch_reaim/program.md"
os.environ["OUT"] = f"{OUTDIR}/pass0.json"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H       # the only harness import; the D-C10m/p drivers are NOT imported (their import-time env/dir side effects would breach the fence)
import torch
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z, get_module_input_output_at_words   # the same symbol the harness's my_edit uses
from memit.memit_main import get_context_templates

HP = MEMITHyperParams.from_json(HP_FILE)
V = H.ARMS["A7_coined_coined"]
Z_LAYER = HP.layers[-1]
KEY = {c: (c, " " + V[c]) for c in H.FICTION}               # the harness keys Z_OVERRIDE by (subject, target string)
ST = {}                                                      # written by main / read by the hook  [LAW:no-shared-mutable-globals] one owner
LAW3_REF = os.environ["LAW3_REF"]
_law3 = json.load(open(LAW3_REF))["recipes"]["baseline"]["arms"]
if _law3["A1_single"]["para_full_n"] < 68 or _law3["A2_coherent2"]["para_full_n"] < 68:
    raise SystemExit(f"LAW#3 reference {LAW3_REF} does not pass the envelope")   # [LAW:no-silent-failure]
# CORPUS/43 same-frame locality probe, as in c10p_twopass_arms.py (copied, not imported: that driver has import-time side effects)
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]
assert not set(FRAME_SUBJECTS) & set(H.FICTION)
CAP_TOL = 1.05                                               # the capped redo must land within 5 % of the cap (fp16, sequential per-layer solve)


def fingerprint():
    fp = subprocess.run([sys.executable, f"{LLMDB_ROOT}/tools/engine_fingerprint.py"], capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": LLMDB_ROOT})
    if fp.returncode != 0:
        raise SystemExit(f"P1 fingerprint FAIL:\n{fp.stdout}{fp.stderr}")   # [LAW:no-silent-failure]
    return fp.stdout.strip()


@torch.no_grad()
def frame_probe():
    firsts = {H.tgt_ids(V[c])[0] for c in H.FICTION}
    rows = []
    for s in FRAME_SUBJECTS:
        ids = H.tok(H.CANON.format(s), return_tensors="pt").to(H.DEV)
        t = int(H.model(**ids).logits[0, -1].argmax()); rows.append({"subj": s, "top1": t, "tok": H.tok.decode([t]), "flip": t in firsts})
    return {"flips": sum(r["flip"] for r in rows), "n": len(rows), "rows": rows}


def z_record(zs):
    stack = torch.stack([zs[c].float().cpu() for c in H.FICTION])
    return {"sha256": hashlib.sha256(stack.numpy().tobytes()).hexdigest(), "norms": [round(float(zs[c].float().norm()), 3) for c in H.FICTION]}


def resolve(ctx):
    """z for every A7 subject, solved on the CURRENT model with the iteration's hp (band, steps)."""
    zs = {}
    for c in H.FICTION:
        with contextlib.redirect_stdout(io.StringIO()):
            zs[c] = compute_z(H.model, H.tok, H.req(H.CANON, c, V[c]), HP, Z_LAYER, ctx).detach()
    return zs


def blend(z_prev, z_new):
    return {c: z_prev[c] + K.z_blend * (z_new[c] - z_prev[c]) for c in H.FICTION}


def current_z_outputs(requests):
    """The solve's `cur` at the keyed position on the current model (what my_edit subtracts the target from)."""
    return get_module_input_output_at_words(H.model, H.tok, Z_LAYER, context_templates=[rq["prompt"] for rq in requests],
                                            words=[rq["subject"] for rq in requests], module_template=HP.layer_module_tmp,
                                            fact_token_strategy=HP.fact_token)[1].detach()


def dw_total(d):
    return sum(v["delta_norm"] for v in d.values())


def law5_then_ridge(orig):
    """The LAW#5 parity gate runs at the harness default ridge; the knob departs only afterwards.  [LAW:single-enforcer]"""
    def wrapped(hp, P, base_snap):
        H.L2 = 1.0
        gate = orig(hp, P, base_snap)
        H.L2 = K.ridge
        return gate
    return wrapped


H.run_law5 = law5_then_ridge(H.run_law5)


def stacked_edit(st, target, dw1_total):
    """One extra sequential edit aimed at `target` on the current (edited) model, residual-capped to write_cap. The per-layer solve
    is linear in (target - cur) but the layers are written sequentially (K and cur recomputed after earlier writes), so the rescale is
    approximate; the redo's achieved ratio is checked against the cap (CAP_TOL) and recorded — a miss is a guard failure."""
    requests, hp = st["requests"], st["hp"]
    snap = H.snap_layers(hp); cache_snap = [c.clone() for c in st["cache"]]
    H.Z_OVERRIDE = {KEY[c]: target[c] for c in H.FICTION}
    with contextlib.redirect_stdout(io.StringIO()):
        d = H.my_edit(hp, requests, st["P"], st["cache"])
    H.Z_OVERRIDE = None
    r = dw_total(d) / dw1_total
    scale = 1.0 if K.write_cap is None else min(1.0, K.write_cap / r)
    if scale < 1.0:
        H.restore_layers(hp, snap); st["cache"][:] = cache_snap
        cur = current_z_outputs(requests)                                   # [B, D] in request order
        tgt = {c: cur[i] + scale * (target[c].to(cur.dtype).to(cur.device) - cur[i]) for i, c in enumerate(H.FICTION)}
        H.Z_OVERRIDE = {KEY[c]: tgt[c] for c in H.FICTION}
        with contextlib.redirect_stdout(io.StringIO()):
            d = H.my_edit(hp, requests, st["P"], st["cache"])
        H.Z_OVERRIDE = None
    return d, r, scale


def hook(arm_name, Vmap):
    if arm_name != "A7_coined_coined":
        return {}
    st = H._ARM_STATE
    out = {"frame_single": frame_probe(), "override_hits_before": H.Z_OVERRIDE_HITS}
    k = ST["pass"]
    if not K.stack:
        if k < K.resolve_rounds:
            z_new = resolve(ST["ctx"]); ST["z_next"] = blend(ST["z_aimed"], z_new)
            out["resolved"] = z_record(z_new)
        return out
    # stack = true: R extra sequential edits on top of the first. dw1_total = the EFFECTIVE fp16-applied norm ||W_now - W_base|| per layer
    # (the harness's own delta_norm is the fp32 update norm before the fp16 add; close, not identical — reported as such).
    hp = st["hp"]; dw1_total = sum(float((H.snap_layers(hp)[l] - ST["base_snap"][l]).float().norm()) for l in hp.layers)
    z_prev = ST["z_aimed"]; extras = []
    for r_i in range(K.resolve_rounds):
        z_new = resolve(ST["ctx"]); target = blend(z_prev, z_new)
        d, ratio_raw, scale = stacked_edit(st, target, dw1_total)
        ratio = dw_total(d) / dw1_total
        extras.append({"round": r_i + 1, "delta_norms": d, "ratio_uncapped": ratio_raw, "residual_scale": scale, "ratio": ratio,
                       "cap_ok": K.write_cap is None or ratio <= K.write_cap * CAP_TOL, "resolved": z_record(z_new)})
        z_prev = target
    stacked = H.eval_arm(Vmap)
    stacked["locality_described_as"] = H.locpct({p: H.predict(p) for p in st["pre_prompts"]}, st["pre_loc"], st["pre_prompts"])
    stacked["locality_axes"] = H.axes_post(st["pre_axes"], list(Vmap.values()))
    out.update({"stacked": {kk: v for kk, v in stacked.items() if kk != "rows"}, "stacked_rows": stacked["rows"], "extra_edits": extras,
                "dw1_total": dw1_total, "frame_stacked": frame_probe(), "override_hits_after": H.Z_OVERRIDE_HITS})
    return out


def run_pass(k, override):
    H.OUT = f"{OUTDIR}/pass{k}.json"; H.Z_OVERRIDE = override; H.Z_OVERRIDE_HITS = 0; ST["pass"] = k; H.ARM_HOOKS[:] = [hook]
    print(f"=== PASS {k}: override={'None' if override is None else f'{len(override)} targets'} stack={K.stack}", flush=True)
    rc = H.main()
    if rc != 0:
        raise SystemExit(f"HALT: harness returned {rc} in pass {k}")   # [LAW:no-silent-failure]
    res = json.load(open(H.OUT)); res["pass"] = k; res["z_override_hits_total"] = H.Z_OVERRIDE_HITS
    json.dump(res, open(H.OUT, "w"), indent=2, default=str)
    return res


def final_state(res):
    """The candidate state's readouts: the pass's A7 arm (fresh) or its stacked readout (stack), beside that pass's A1/A2 arms."""
    rec = res["recipes"]["A7_reaim"]; a7 = rec["arms"]["A7_coined_coined"]
    if K.stack:
        s = a7["extra"]["stacked"]; frame = a7["extra"]["frame_stacked"]["flips"]
        ratio = sum(e["ratio"] for e in a7["extra"]["extra_edits"]); cap_ok = all(e["cap_ok"] for e in a7["extra"]["extra_edits"])
    else:
        s = a7; frame = a7["extra"]["frame_single"]["flips"]; ratio = dw_total(rec["delta_norms"]["A7_coined_coined"]) / ST["dw0_total"]; cap_ok = True
    ax = s["locality_axes"]
    return {"heldout_full": s["para_full_n"], "canon": s["canon_full_n"], "A1": rec["arms"]["A1_single"]["para_full_n"], "A2": rec["arms"]["A2_coherent2"]["para_full_n"],
            "L1_flips": ax["L1_flipped_to_edited_value"], "frame_flips": frame, "described_as": s["locality_described_as"], "L3": ax["L3_top1_agree"],
            "ppl_post": ax["generic_ppl_post"], "dw_ratio": round(ratio, 3), "law5_ok": rec["law5_gate"]["ok"], "cap_ok": cap_ok}


def main():
    t0 = time.time()
    p1 = fingerprint()
    ctx = get_context_templates(H.model, H.tok)
    ST.update(ctx=ctx, base_snap=H.snap_layers(HP))
    head = {"tag": TAG, "iter": ITER, "knobs": json.loads(KNOBS_RAW), "knobs_sha": KNOBS_SHA, "hparams": HP_FILE, "P1": {"fingerprint": p1, "law3_reference_run": LAW3_REF},
            "z_layer": Z_LAYER, "frame_subjects": FRAME_SUBJECTS, "frame_pre_edit": frame_probe(), "passes": []}
    ST["z_aimed"] = resolve(ctx)                       # z_0 on the base model (the engine's own targets, recorded for blending)
    head["z0"] = z_record(ST["z_aimed"])
    res = run_pass(0, None); head["passes"].append(H.OUT)
    ST["dw0_total"] = dw_total(res["recipes"]["A7_reaim"]["delta_norms"]["A7_coined_coined"])
    ref = res["recipes"]["A7_reaim"]["arms"]["A7_coined_coined"]["para_full_n"]
    if not K.stack:
        for k in range(1, K.resolve_rounds + 1):
            ST["z_aimed"] = ST.pop("z_next")
            res = run_pass(k, {KEY[c]: ST["z_aimed"][c] for c in H.FICTION}); head["passes"].append(H.OUT)
    f = final_state(res); f["ref_heldout"] = ref; f["seconds"] = round(time.time() - t0)
    head["summary"] = f
    json.dump(head, open(f"{OUTDIR}/run.json", "w"), indent=2, default=str)
    print("---")
    for key in ("heldout_full", "canon", "A1", "A2", "L1_flips", "frame_flips", "described_as", "L3", "ppl_post", "dw_ratio", "law5_ok", "cap_ok", "ref_heldout", "seconds"):
        v = f[key]; print(f"{key + ':':16}{str(v).lower() if isinstance(v, bool) else v}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
