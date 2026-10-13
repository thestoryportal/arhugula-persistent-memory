#!/usr/bin/env python3
"""D-C10s-sharedz pure-function selftest. Imports ONLY c10s_sharedz_read (no harness, no engine, no model; torch only for
the reduction test on a fixed tensor): the overlap table, the prompt-ordering builder, the engine's NLL reduction vs a
naive one on the same fp16 log-probability tensor, the fit diagnostic, the screen rule, the label function and the
whole verdict on synthetic pass records (implementation review items 1, 2, 5).
[LAW:behavior-not-structure] every assertion is a §2/§3 rule stated as an outcome. Exit 0 = all pass; any failure raises."""
import os, sys
import ast, contextlib, copy, hashlib, io, json, math, subprocess, tempfile, types
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10s_sharedz_read as R

CTX = [["{}"], ["The sun rose. {}", "Therefore it was. {}", "Because of that. {}", "I think so. {}", "You said it. {}"]]   # engine shape: memit_main.py:308
SUBJ = [f"S{i}" for i in range(24)]
ROOT = Path(__file__).resolve().parents[3]
DRIVER = ROOT / "code/lab/track_c/c10s_sharedz_arms.py"


def test_overlap_table():
    t = R.overlap_table({"CANON": R.CANON, "T1": R.T1, "T2": R.T2}, R.PTEST)
    assert len(t["pairs"]) == 9, t
    assert t["total_shared"] == 0, t
    bad = R.overlap_table({"T1_v1": R.V1_WITHDRAWN}, R.PTEST)
    shared = {p["heldout_form"]: p["shared_3grams"] for p in bad["pairs"]}
    assert shared[R.PTEST[0]] == ["capital city is"], shared
    assert shared[R.PTEST[1]] == ["capital city is"], shared
    assert shared[R.PTEST[2]] == [], shared
    assert bad["total_shared"] == 2, bad
    assert R.form_words("{}'s capital city is called") == ["'s", "capital", "city", "is", "called"]


def test_prompt_plan():
    plan = R.build_prompt_plan(CTX, R.FRAMES, " Qorvex")
    assert plan["rewriting"][0] == R.CANON + " Qorvex", plan["rewriting"][0]          # index 0 = identity template on CANON
    assert plan["frame_idx"][0] == 0
    assert len(plan["rewriting"]) == 6 * 3 and len(plan["all"]) == 6 * 3 + 1
    assert plan["all"][-1] == R.KL_PROMPT and plan["kl"] == [R.KL_PROMPT]              # KL prompt last and single
    assert plan["frame_idx"] == [0, 1, 2] * 6                                           # template-major, CANON first inside each template
    assert plan["rewriting"][3] == "The sun rose. " + R.CANON + " Qorvex"
    assert plan["rewriting"][4] == "The sun rose. " + R.T1 + " Qorvex"
    single = R.build_prompt_plan(CTX, [R.CANON], " Q")
    assert single["rewriting"] == [c.format(R.CANON) + " Q" for ct in CTX for c in ct]  # == the engine's own list (compute_z.py:46-50)
    try:
        R.build_prompt_plan([["The {}"], ["{}"]], R.FRAMES, " Q"); raise AssertionError("identity-first invariant not enforced")
    except ValueError:
        pass


def test_nll_reduction():
    """Review item 1: the inertness reference must reduce exactly as compute_z.py:141-149 (fp16 gather, float32 mask,
    sum, / T). On one fixed fp16 tensor the engine reduction equals a hand-written fp32 masked reduction bit for bit,
    and differs from the naive fp16 `lp.sum() / T` of v1 (which rounds the sum to fp16)."""
    import torch
    g = torch.Generator(device="cpu").manual_seed(7)
    T, L, Vn = 40, 64, 50
    log_probs = (-torch.rand((2, L, Vn), generator=g, device="cpu") * 6 - 0.05).to(torch.float16)
    targets = torch.full((2, L), -100, dtype=torch.long, device="cpu")
    tgt = torch.randint(0, Vn, (T,), generator=g, device="cpu")
    for i, ex_len in enumerate((L, L - 9)):                                             # row 1 right-padded, as the engine's batch is
        targets[i, ex_len - T: ex_len] = tgt
    engine = R.engine_nll_each(log_probs, targets, T)
    assert engine.dtype == torch.float32 and engine.shape == (2,), engine
    for i, ex_len in enumerate((L, L - 9)):
        rows = log_probs[i, ex_len - T: ex_len].gather(1, tgt.view(-1, 1)).squeeze(1)
        manual = -(rows * torch.ones(T, dtype=torch.float32, device="cpu")).sum() / T   # the engine's arithmetic, written out
        naive = float(-rows.sum() / T)                                                 # v1's reference: fp16 reduction
        assert float(engine[i]) == float(manual), (float(engine[i]), float(manual))
        assert float(engine[i]) != naive, "the fp16 reduction coincided with the engine's on this tensor; choose another tensor"
        assert abs(float(engine[i]) - naive) < 1e-2, (float(engine[i]), naive)        # same quantity, different rounding


def test_fit():
    nll = [0.0, 0.01, 0.5] * 2
    fits = R.frame_fit(nll, [0, 1, 2] * 2, 3)
    assert abs(fits[0] - 1.0) < 1e-12 and abs(fits[1] - 0.99005) < 1e-4 and fits[2] < 0.61, fits
    d = R.fit_diagnostic({"A": [0.99, 0.985, 0.995], "B": [0.99, 0.979, 0.99]})
    assert not d["ok"] and d["underfit"] == [{"subj": "B", "frame": "T1", "fit": 0.979}] and d["min_fit"] == 0.979, d
    assert R.fit_diagnostic({"A": [0.98, 0.98, 0.98]})["ok"]


def rows(canon_hits, shared_hits):
    """canon_hits/shared_hits: subject -> [bool x3]; unlisted subjects miss everywhere."""
    return [{"subj": s, "canon": canon_hits.get(s, [False] * 3), "shared": shared_hits.get(s, [False] * 3)} for s in SUBJ]


def test_screen():
    base = {s: [True, True, True] for s in SUBJ[:16]}                       # canonical 48/72
    spread = dict(base, **{SUBJ[16]: [True, True, False], SUBJ[17]: [True, False, True], SUBJ[18]: [False, True, True], SUBJ[19]: [True, True, True]})   # +9 on 3 templates, 4 subjects
    s = R.paired_screen(rows(base, spread))
    assert (s["canon_n"], s["shared_n"], s["gain"], s["outcome"]) == (48, 57, 9, "PASS"), s
    small = dict(base, **{SUBJ[16]: [True, True, True], SUBJ[17]: [True, True, False]})   # +5
    assert R.paired_screen(rows(base, small))["outcome"] == "NOT-ADVANCED-SCREEN"
    one_t = dict(base, **{SUBJ[k]: [True, False, False] for k in range(16, 22)})         # +6, all on template 0
    s = R.paired_screen(rows(base, one_t)); assert (s["gain"], s["templates_won"], s["outcome"]) == (6, 1, "CONCENTRATED"), s
    two_s = dict(base, **{SUBJ[16]: [True, True, True], SUBJ[17]: [True, True, True]})   # +6 on 3 templates but 2 subjects
    s = R.paired_screen(rows(base, two_s)); assert (s["gain"], s["subjects_won"], s["outcome"]) == (6, 2, "CONCENTRATED"), s
    mixed = dict(base); mixed[SUBJ[0]] = [False, True, True]                             # a loss on one subject, gains elsewhere: net wins are signed
    mixed.update({SUBJ[k]: [True, True, False] for k in range(16, 20)})                  # +8 - 1 = 7, templates 0/1 won, 4 subjects won
    s = R.paired_screen(rows(base, mixed)); assert (s["gain"], s["templates_won"], s["subjects_won"], s["outcome"]) == (7, 2, 4, "PASS"), s
    quiet_twin = {"ok": True}
    assert R.cell1_outcome({"ok": False}, quiet_twin, s) == "UNDERFIT" and R.cell1_outcome({"ok": True}, quiet_twin, s) == "PROCEED"
    assert R.cell1_outcome({"ok": True}, quiet_twin, {"outcome": "CONCENTRATED"}) == "CONCENTRATED"
    assert R.cell1_outcome({"ok": True}, {"ok": False}, s) == "NOISE-NON-DISCRIMINATING"            # §7 A2: a noisy twin vetoes a PASS
    assert R.cell1_outcome({"ok": False}, {"ok": False}, s) == "UNDERFIT"                           # UNDERFIT keeps precedence


def test_a2_engine_parity_plans():
    """§7 A2: the engine-side context lists make the unmodified engine's own construction (R.engine_plan, compute_z.py:46-51)
    reproduce the harness plans exactly; plan_matches rejects every corruption the first A2 draft let through."""
    pre = " Qorvex"
    het = R.build_prompt_plan(CTX, R.FRAMES, pre)["all"]
    trip = R.build_prompt_plan(CTX, [R.CANON] * 3, pre)["all"]
    assert R.engine_plan(R.ctx_heterogeneous(CTX, R.FRAMES), "{}", pre) == het
    assert R.engine_plan(R.ctx_triplicate(CTX), R.CANON, pre) == trip
    assert R.plan_matches(het, R.ctx_heterogeneous(CTX, R.FRAMES), "{}", pre)
    assert R.ctx_triplicate(CTX)[0] == ["{}"] * 3 and len(R.ctx_triplicate(CTX)[1]) == 15
    assert R.ctx_heterogeneous(CTX, R.FRAMES)[0] == list(R.FRAMES)                      # identity template -> the bare phrasings, CANON first
    eng_het = R.ctx_heterogeneous(CTX, R.FRAMES)
    corruptions = {
        "dropped contexts": het[:3] + het[-1:],
        "CANON moved off row 0": [het[1], het[0]] + het[2:],
        "KL row missing": het[:-1],
        "extra duplicate row": het[:1] + het,
        "frame order swapped in one template": het[:3] + [het[4], het[3]] + het[5:],
    }
    for name, plan in corruptions.items():
        assert not R.plan_matches(plan, eng_het, "{}", pre), name


def test_noise_twin():
    base = {s: [True, True, True] for s in SUBJ[:16]}
    same = R.noise_twin_verdict(rows(base, base)); assert same["ok"] and same["disagreeing_pairs"] == 0 and same["n_pairs"] == 72, same
    up6 = dict(base, **{SUBJ[16]: [True, True, True], SUBJ[17]: [True, True, True]})   # +6, concentrated on two subjects: the screen says CONCENTRATED, the twin still vetoes
    v = R.noise_twin_verdict(rows(base, up6)); assert not v["ok"] and v["forward"]["outcome"] == "CONCENTRATED", v
    assert not R.noise_twin_verdict(rows(up6, base))["ok"]                              # a -6 twin vetoes too (|gain|)
    up5 = dict(base, **{SUBJ[16]: [True, True, True], SUBJ[17]: [True, True, False]})   # +5: below the screen's 6
    v = R.noise_twin_verdict(rows(base, up5)); assert v["ok"] and v["gain"] == 5 and v["disagreeing_pairs"] == 5, v


def test_label():
    L = R.label
    assert L(32, 10, True, 1.0) == "LEAD"
    assert L(32, 10, False, 1.0) == "TRADEOFF"
    assert L(25, 10, True, 1.0) == "PARTIAL"                  # > 18, gain 15, < 30
    assert L(25, 10, False, 1.0) == "TRADEOFF"
    assert L(15, 5, True, 1.0) == "NULL"                      # Codex item 6: inside the envelope whatever the gain
    assert L(20, 12, True, 1.0) == "NULL"                     # outside the envelope but gain 8 < 10
    assert L(18, 5, True, 1.0) == "NULL"                      # 18 is inside [5,18]
    assert L(10, 12, True, 1.0) == "NULL"
    assert L(32, 10, True, 1.6) == "LEAD-LARGE-WRITE"
    assert L(10, 12, True, 1.51) == "NULL-LARGE-WRITE"        # §3: added to any label
    assert L(32, 10, True, 1.5) == "LEAD"                     # above 1.5, not at it
    ok2 = (31, 9, True, 1.0)
    assert L(32, 10, True, 1.0, second=ok2) == "LEAD"
    assert L(32, 10, True, 1.0, second=(29, 9, True, 1.0)) == "LEAD-NOT-REPLICATED"
    assert L(32, 10, True, 1.0, second=(31, 9, False, 1.0)) == "LEAD-NOT-REPLICATED"       # pass-2 locality miss blocks LEAD as pass 1's would
    assert L(32, 10, True, 1.0, second=(31, 9, True, 1.6)) == "LEAD-LARGE-WRITE"            # pass-2 ratio adds the qualifier
    assert L(25, 10, True, 1.0, second=(22, 11, True, 1.0)) == "PARTIAL"
    assert L(25, 10, True, 1.0, second=(22, 11, False, 1.0)) == "PARTIAL-NOT-REPLICATED"
    assert L(25, 10, True, 1.0, second=(22, 14, True, 1.0)) == "PARTIAL-NOT-REPLICATED"     # gain 8 < 10
    assert L(25, 10, True, 1.0, second=(18, 5, True, 1.0)) == "PARTIAL-NOT-REPLICATED"      # inside the envelope
    assert L(25, 10, True, 1.0, second=(31, 10, True, 1.0)) == "PARTIAL"                    # a LEAD-sized second process still replicates a PARTIAL
    assert L(25, 10, True, 2.0, second=(22, 14, True, 1.0)) == "PARTIAL-NOT-REPLICATED-LARGE-WRITE"
    assert L(10, 12, True, 1.0, second=(32, 10, True, 1.0)) == "NULL"                       # a NULL is never promoted by a second process


def test_gates():
    ref = {"locality_axes": {"L1_flipped_to_edited_value": 2, "L3_top1_agree": 30, "generic_ppl_post": 20.0}, "locality_described_as": 97.0}
    ok = {"locality_axes": {"L1_flipped_to_edited_value": 3, "L3_top1_agree": 29, "generic_ppl_post": 20.5}, "locality_described_as": 94.0}
    g = R.locality_gates(ref, ok, {"CANON": 1, "T1": 0, "T2": 2}, {"CANON": 2, "T1": 1, "T2": 3})
    assert all(g.values()), g
    bad = R.locality_gates(ref, ok, {"CANON": 1, "T1": 0, "T2": 2}, {"CANON": 2, "T1": 2, "T2": 3})
    assert not bad["same_frame_fictional_T1"] and sum(not v for v in bad.values()) == 1, bad
    l3 = dict(ok, locality_axes=dict(ok["locality_axes"], L3_top1_agree=28))
    assert not R.locality_gates(ref, l3, {"CANON": 0, "T1": 0, "T2": 0}, {"CANON": 0, "T1": 0, "T2": 0})["L3"]


# ---- synthetic records in the exact shape read_pass / run.json carry ----
def arm(para, canon=8, l1=1, l3=30, ppl=20.0, desc=97.0):
    return {"para_full_n": para, "canon_full_n": canon, "para_first_n": para, "para_string_n": para, "locality_described_as": desc,
            "locality_axes": {"L1_flipped_to_edited_value": l1, "L3_top1_agree": l3, "generic_ppl_post": ppl}}


def synth_pass(shared_n, ref_n=10, l3=30, ratio=1.0, fit_ok=True, run_id="R1", hits=(0, 1, 1), a1=70, a2=70, hit_pattern=None):
    hp = hit_pattern or [[k < shared_n // 24 + (1 if i < shared_n % 24 else 0) for k in range(3)] for i in range(24)]
    return {"rec": {"law5_gate": {"ok": True}}, "ref": arm(ref_n), "shared": arm(shared_n, l3=l3),
            "shared_rows": [{"subj": s, "para_full_hits": hp[i]} for i, s in enumerate(SUBJ)],
            "a1": {"para_full_n": a1}, "a2": {"para_full_n": a2}, "dw_ref": 100.0, "dw_shared": 100.0 * ratio,
            "frames_ref": {"CANON": 0, "T1": 0, "T2": 0}, "frames_shared": {"CANON": 0, "T1": 0, "T2": 0}, "frame_n": [6] * 6, "hits": hits,
            "fit": {"ok": fit_ok, "underfit": [] if fit_ok else [{"subj": "S0", "frame": "T1", "fit": 0.97}]}, "identity": {"run_id": run_id},
            "residual": {a: 0.03 for a in R.PASS_ARMS} | {"A7_shared": 0.03}, "key_cosine": {"pre": {}, "ref": {}, "shared": {}}}


def synth_run(run_id="R1", inert_id="I1", second=None):
    """run.json as the v3 driver writes it: no second_process until stage second records one (outcome STARTED ->
    UNDERFIT | COMPLETED); `second` plants that record with the given outcome."""
    forms = {k: {"form": v, "sha256": R.sha256_text(v)} for k, v in (("CANON", R.CANON), ("T1", R.T1), ("T2", R.T2))}
    run = {"fingerprint": f"engine fingerprint PASS: x\n  sha256 {R.FINGERPRINT}...",
           "inertness": {"ok": True, "checks": {c: {"ok": True} for c in R.INERTNESS_CHECKS}, "identity": {"run_id": inert_id}},
           "identity": {"run_id": run_id, "inertness_run_id": inert_id}, "training_forms": forms, "overlap_table": {"total_shared": 0}}
    if second is not None:
        run["second_process"] = {"outcome": second, "fingerprint": f"engine fingerprint PASS {R.FINGERPRINT}", "started_utc": "t"}
    return run


def test_verdict():
    run = synth_run(); run2 = synth_run(second="COMPLETED")                         # run2: a second process ran to completion
    v = R.verdict(run, synth_pass(32))
    assert v["reasons"] == [] and v["label"] == "LEAD" and v["replication_pending"], v
    v = R.verdict(run2, synth_pass(32), synth_pass(31))
    assert v["reasons2"] == [] and v["label"] == "LEAD" and not v["replication_pending"] and v["agreement"]["n"] == 24, v
    v = R.verdict(run2, synth_pass(32), synth_pass(31, l3=0))                      # pass-2 L3 = 0/30 -> not LEAD
    assert not v["gates2"]["L3"] and v["label"] == "LEAD-NOT-REPLICATED", v
    v = R.verdict(run2, synth_pass(32), synth_pass(31, ratio=1.6))                 # pass-2 ratio 1.6 -> -LARGE-WRITE
    assert v["label"] == "LEAD-LARGE-WRITE", v
    v = R.verdict(run2, synth_pass(32), synth_pass(31, fit_ok=False))              # a pass-2 record whose solve was underfit -> INVALID (second process)
    assert v["reasons2"] and "UNDERFIT" in v["reasons2"][0], v
    v = R.verdict(run2, synth_pass(32), synth_pass(31, run_id="R-other"))          # different run identity -> not paired
    assert any("identity" in r for r in v["reasons2"]), v
    stale = synth_run(); stale["inertness"]["identity"]["run_id"] = "I-stale"       # inertness record from another identity
    v = R.verdict(stale, synth_pass(32))
    assert any("inertness record identity" in r for r in v["reasons"]), v
    v = R.verdict(run, synth_pass(32, hits=(0, 2, 2)))
    assert any("Z_OVERRIDE" in r for r in v["reasons"]), v
    v = R.verdict(run, synth_pass(32, a1=60))
    assert any("controls" in r for r in v["reasons"]), v
    v = R.verdict(run, synth_pass(32, ref_n=20))
    assert any("outside" in r for r in v["reasons"]), v
    v = R.verdict(run2, synth_pass(25), synth_pass(22, ref_n=11))
    assert v["label"] == "PARTIAL", v


def test_second_process_record():
    """v3 (review 2 blocker): run.json's second_process outcome is authoritative when no pass2.json exists, and a second
    process is never retried in the same run."""
    run = synth_run()                                                                  # no second_process -> replication pending
    v = R.verdict(run, synth_pass(32)); assert v["second_process"] == "absent" and v["replication_pending"] and v["label"] == "LEAD", v
    assert R.retry_refusal(run) is None
    under = synth_run(second="UNDERFIT"); under["second_process"]["fit_diagnostic"] = {"ok": False, "underfit": [{"subj": "S3", "frame": "T2", "fit": 0.95}]}
    v = R.verdict(under, synth_pass(32))                                               # valid pass 1 + UNDERFIT + no pass2 -> terminal non-advancement
    assert v["label"] == "LEAD-NOT-REPLICATED" and not v["replication_pending"] and "not advanced" in v["disposition"] and v["reasons2"] == [], v
    v = R.verdict(under, synth_pass(32, ratio=1.7)); assert v["label"] == "LEAD-NOT-REPLICATED-LARGE-WRITE", v
    v = R.verdict(under, synth_pass(25)); assert v["label"] == "PARTIAL-NOT-REPLICATED", v
    v = R.verdict(under, synth_pass(10)); assert v["label"] == "NULL" and v["disposition"] is None, v   # nothing provisional to withdraw
    for outcome in ("UNDERFIT", "STARTED", "COMPLETED"):                                # any recorded attempt refuses a same-run retry
        r = synth_run(second=outcome)
        assert R.retry_refusal(r) and outcome in R.retry_refusal(r), outcome
    started = synth_run(second="STARTED")
    v = R.verdict(started, synth_pass(32))                                             # began, no pass2 -> INVALID (second process)
    assert v["reasons2"] and "incomplete" in v["reasons2"][0] and not v["replication_pending"], v
    done = synth_run(second="COMPLETED")
    v = R.verdict(done, synth_pass(32), synth_pass(31)); assert v["label"] == "LEAD" and v["reasons2"] == [], v
    v = R.verdict(started, synth_pass(32), synth_pass(31)); assert any("not COMPLETED" in r for r in v["reasons2"]), v
    bad = synth_run(second="RETRIED")
    try:
        R.verdict(bad, synth_pass(32)); raise AssertionError("unknown outcome accepted")
    except ValueError:
        pass


# The driver cannot be imported here: it loads a model. Execute ONLY named definitions
# or its settings bootstrap, with CPU tensors / callback fixtures, never its main().
def driver_defs(names, namespace):
    tree = ast.parse(DRIVER.read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(DRIVER), "exec"), namespace)
    return namespace


def expect_error(kind, fn):
    try:
        fn()
    except kind:
        return
    raise AssertionError(f"expected {kind.__name__}")


def sf_settings():
    a = R.select_arm("solvefeas")
    p = ROOT / a.hparams
    return {"arm": a.name, "hparams": str(p), "hparams_sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "v_num_grad_steps": a.steps}


def sf_diag(fit25=(0.97, 0.99, 0.99), fit40=(0.99, 0.99, 0.99), final=(0.99, 0.99, 0.99), n=50, stopped="budget"):
    history = [{"evaluation": i, "nll_each": [-math.log(x) for x in (final if i == n else fit40 if i == 40 else fit25)],
                "loss": 0.04 if stopped == "loss<0.05" and i == n else 0.1} for i in range(1, n + 1)]
    return {**sf_settings(), "prompts": R.FRAMES, "frame_idx": [0, 1, 2], "history": history, "loss_evals": n,
            "stopped_by": stopped, "frame_fit": list(final), "snapshot_25": {"frame_fit": list(final if n < 25 else fit25)}}


def sf_run(second=None):
    run = synth_run(second=second); settings = sf_settings()
    run.update(settings); run["identity"].update(settings)
    run["inertness"].update(settings); run["inertness"]["identity"].update(settings)
    if second is not None:
        run["second_process"].update(settings)
        run["second_process"]["identity"] = dict(run["identity"])
    return run


def sf_pass(shared_n=32, ref_n=10, canon=8, evaluations=50):
    pr = synth_pass(shared_n, ref_n=ref_n); settings = sf_settings()
    pr["ref"]["canon_full_n"] = canon
    pr["identity"].update(settings); pr["settings"] = settings
    pr["engine_solves"] = [{**settings, "loss_evals": evaluations}]
    pr["per_fact"] = {"S0": sf_diag() if evaluations == 50 else sf_diag(final=(0.99, 0.99, 0.99), n=evaluations, stopped="loss<0.05")}
    return pr


def test_arm_selector_and_config():
    default = R.select_arm()
    assert default == R.select_arm("sharedz") and default.steps == 25
    assert default.decision_id == "D-C10s-sharedz" and default.prereg == "experiments/c10s/design/C10S_SHARED_Z_PREREG.md"
    assert default.halt_path == "experiments/c10s/runs/c10s_sharedz/halts/c10s_sharedz_halt_diagnostic.json" and default.out_dir == "experiments/c10s/runs/c10s_sharedz"
    followup = R.select_arm("solvefeas")
    assert followup.steps == 50 and followup.decision_id == "D-C10s-solvefeas"
    assert followup.prereg == "experiments/c10s/design/C10S_SOLVEFEAS_PREREG.md" and followup.halt_path == "architecture_profile/c10s_solvefeas_halt_diagnostic.json"
    assert followup.out_dir == "experiments/c10s/runs/c10s_solvefeas" and followup.hparams != default.hparams
    for bad in ("", "SOLVEFEAS", "../steps100.json", "other"):
        expect_error(ValueError, lambda: R.select_arm(bad))
    base = json.loads((ROOT / default.hparams).read_text()); extended = json.loads((ROOT / followup.hparams).read_text())
    assert extended == {**base, "v_num_grad_steps": 50} and base["v_num_grad_steps"] == 25
    assert (ROOT / followup.hparams).read_text() == (ROOT / default.hparams).read_text().replace('"v_num_grad_steps": 25', '"v_num_grad_steps": 50')


def test_settings_before_import_and_hp_rebinding():
    tree = ast.parse(DRIVER.read_text())
    start = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.Try) and any(isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ARM" for t in x.targets) for x in n.body))
    end = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.Try) and any(isinstance(x, ast.Import) and any(a.name == "c10e_bandknob" for a in x.names) for x in n.body))
    bootstrap = compile(ast.Module(body=tree.body[start:end], type_ignores=[]), str(DRIVER), "exec")
    init = tree.body[end]
    rebind = [n for n in init.body if isinstance(n, ast.Assert) or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "hp" for t in n.targets))]
    def halted(reason, **state):
        raise SystemExit(reason)
    for arm in (None, "sharedz", "solvefeas"):
        with tempfile.TemporaryDirectory() as d:
            env = {"OUT_DIR": d}
            if arm is not None:
                env["C10S_ARM"] = arm
            ns = {"os": os, "sys": types.SimpleNamespace(path=[]), "hashlib": hashlib, "R": R, "LLMDB_ROOT": str(ROOT), "STAGE": "first", "halt": halted}
            with patch.dict(os.environ, env, clear=True):
                exec(bootstrap, ns)
                selected = R.select_arm("sharedz" if arm is None else arm)
                assert ns["RECORD_SETTINGS"] == (ns["ARM_RECORD"] if selected.name == "solvefeas" else {})
                assert os.environ["HP_CANDIDATE"] == str(ROOT / selected.hparams)
                assert os.environ["PREREG"] == str(ROOT / selected.prereg) and os.environ["DECISION_ID"] == selected.decision_id
                assert ns["HALT_PATH"] == str(ROOT / selected.halt_path) and ns["OUT_DIR"] == d
                H = types.SimpleNamespace(HP_BAND=os.environ["HP_CANDIDATE"])
                loader = types.SimpleNamespace(from_json=lambda p: types.SimpleNamespace(**json.loads(Path(p).read_text())))
                ns.update(H=H, MEMITHyperParams=loader, hp=types.SimpleNamespace(v_num_grad_steps=25))
                exec(compile(ast.Module(body=rebind, type_ignores=[]), str(DRIVER), "exec"), ns)
                assert ns["hp"].v_num_grad_steps == selected.steps
                ns["MEMITHyperParams"] = types.SimpleNamespace(from_json=lambda p: types.SimpleNamespace(v_num_grad_steps=999))
                expect_error(AssertionError, lambda: exec(compile(ast.Module(body=rebind, type_ignores=[]), str(DRIVER), "exec"), ns))
    ns = {"os": os, "sys": types.SimpleNamespace(path=[]), "hashlib": hashlib, "R": R, "LLMDB_ROOT": str(ROOT), "STAGE": "first", "halt": halted}
    with patch.dict(os.environ, {"C10S_ARM": "solvefeas", "HP_CANDIDATE": "/free/path.json"}, clear=True):
        expect_error(SystemExit, lambda: exec(bootstrap, ns))


def test_inertness_settings_binding():
    settings = sf_settings()
    def halted(reason, **state):
        raise SystemExit(reason)
    with tempfile.TemporaryDirectory() as d:
        ns = driver_defs(("require_settings", "require_inertness"), {"os": os, "json": json, "R": R, "OUT_DIR": d,
                         "ARM": R.select_arm("solvefeas"), "ARM_RECORD": settings, "halt": halted, "provenance_mismatches": lambda x: {}})
        record = {**settings, "ok": True, "checks": {c: {"ok": True} for c in R.INERTNESS_CHECKS}, "identity": {**settings, "source_sha256": {}}}
        p = Path(d) / "inertness.json"
        p.write_text(json.dumps(record)); assert ns["require_inertness"]() == record
        old = R.select_arm(); oldp = ROOT / old.hparams
        step1 = {"arm": old.name, "hparams": str(oldp), "hparams_sha256": hashlib.sha256(oldp.read_bytes()).hexdigest(), "v_num_grad_steps": 25}
        p.write_text(json.dumps({**record, **step1}))
        expect_error(SystemExit, ns["require_inertness"])                              # a real 25-step binding cannot certify 50
        for key, bad in (("arm", "sharedz"), ("hparams", "elsewhere.json"), ("hparams_sha256", "0" * 64), ("v_num_grad_steps", 25)):
            p.write_text(json.dumps({**record, key: bad})); expect_error(SystemExit, ns["require_inertness"])
            p.write_text(json.dumps({**record, "identity": {**record["identity"], key: bad}})); expect_error(SystemExit, ns["require_inertness"])


def test_second_process_settings_binding():
    run = sf_run(second="COMPLETED"); one, two = sf_pass(), sf_pass()
    assert R.verdict(run, one, two)["label"] == "LEAD"
    for key, bad in (("arm", "sharedz"), ("hparams", "wrong.json"), ("hparams_sha256", "0" * 64), ("v_num_grad_steps", 25)):
        for where in ("settings", "identity"):
            other = copy.deepcopy(two); other[where][key] = bad
            v = R.verdict(run, one, other); assert v["label"] == "INVALID" and v["reasons2"], (key, where, v)
        stale = copy.deepcopy(run); stale["second_process"][key] = bad
        assert R.verdict(stale, one, two)["label"] == "INVALID"
        terminal = sf_run(second="UNDERFIT-AT-50"); terminal["second_process"]["identity"][key] = bad
        assert R.verdict(terminal, one)["label"] == "INVALID"                        # the terminal solve is still bound without a pass2 file


def test_forward_counting_and_cleanup():
    class Emitter:
        def __init__(self):
            self.hooks = []
        def register_forward_hook(self, fn):
            self.hooks.append(fn)
            return types.SimpleNamespace(remove=lambda: self.hooks.remove(fn))
        def fire(self):
            for fn in self.hooks:
                assert fn(self, (), object()) is None                               # a counting hook never replaces an output
    emitter, target = Emitter(), object()
    def engine(module, tok, request, hp, layer, ctx):
        for _ in range(request["evaluations"]):
            module.fire()
        if request.get("raise"):
            raise RuntimeError("fixture failure")
        return target
    def halted(reason, **state):
        raise SystemExit(reason)
    ns = driver_defs(("CountForwards", "engine_solve", "count_nested_engine_solves"),
                     {"R": R, "contextlib": contextlib, "ARM": R.select_arm("solvefeas"), "ARM_RECORD": sf_settings(),
                      "ENGINE_SOLVES": [], "_engine_compute_z": engine, "halt": halted})
    request = {"subject": "S0", "prompt": R.CANON, "target_new": {"str": " value"}, "evaluations": 26}
    hp = types.SimpleNamespace(v_num_grad_steps=50)
    assert ns["engine_solve"](emitter, None, request, hp, 8, CTX) is target
    assert ns["ENGINE_SOLVES"][-1]["loss_evals"] == 26 and not emitter.hooks
    expect_error(RuntimeError, lambda: ns["engine_solve"](emitter, None, {**request, "raise": True}, hp, 8, CTX))
    assert not emitter.hooks
    for n in (0, 51):
        expect_error(SystemExit, lambda: ns["engine_solve"](emitter, None, {**request, "evaluations": n}, hp, 8, CTX))
        assert not emitter.hooks
    expect_error(AssertionError, lambda: ns["engine_solve"](emitter, None, request, types.SimpleNamespace(v_num_grad_steps=25), 8, CTX))
    H = types.SimpleNamespace(compute_z=engine); main = types.SimpleNamespace(compute_z=engine)
    ns["H"] = H; package = types.ModuleType("memit"); package.memit_main = main
    with patch.dict(sys.modules, {"memit": package}):
        with ns["count_nested_engine_solves"]():
            assert H.compute_z is ns["engine_solve"] and main.compute_z is ns["engine_solve"]
            assert main.compute_z(emitter, None, request, hp, 8, CTX) is target
            assert H.compute_z(emitter, None, request, hp, 8, CTX) is target
        assert main.compute_z is engine and H.compute_z is engine and not emitter.hooks
        try:
            with ns["count_nested_engine_solves"]():
                raise RuntimeError("exit fixture")
        except RuntimeError:
            pass
        assert main.compute_z is engine and H.compute_z is engine
        recorder = lambda *a: ns["engine_solve"](*a)
        H.compute_z = recorder
        with ns["count_nested_engine_solves"]():
            assert H.compute_z is recorder                                          # harness capture remains attached
    ns["ARM"] = R.select_arm()
    before = len(ns["ENGINE_SOLVES"])
    assert ns["engine_solve"](emitter, None, request, types.SimpleNamespace(v_num_grad_steps=25), 8, CTX) is target
    assert len(ns["ENGINE_SOLVES"]) == before and not emitter.hooks                  # default is the original pass-through


def test_evaluation25_snapshot():
    import torch
    solver = next(n for n in ast.parse(DRIVER.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute_z_shared")
    snapshot = next(n for n in solver.body if isinstance(n, ast.FunctionDef) and n.name == "snapshot")
    delta = torch.tensor([1.25, -0.5], dtype=torch.float32, device="cpu")
    initial = torch.tensor([2.0, 3.0], dtype=torch.float16, device="cpu")
    ns = {"delta": delta, "target_init": initial, "R": R, "nll_each": [0.01, 0.02, 0.03], "plan": {"frame_idx": [0, 1, 2]},
          "prompts": R.FRAMES, "sha256_tensor": lambda x: hashlib.sha256(x.numpy().tobytes()).hexdigest()}
    exec(compile(ast.Module(body=[snapshot], type_ignores=[]), str(DRIVER), "exec"), ns)
    record, saved_delta, saved_z = ns["snapshot"](25)
    expected = initial + delta
    delta.add_(10)
    assert record["evaluation"] == 25 and not record["carried_forward"] and record["delta"] == [1.25, -0.5]
    assert torch.equal(saved_z, expected) and torch.equal(saved_delta, torch.tensor(record["delta"], device="cpu"))
    early, _, _ = ns["snapshot"](12)
    assert early["requested_evaluation"] == 25 and early["carried_forward"] and early["evaluation"] == 12


def test_solvefeas_fit_labels():
    reading = R.solvefeas_reading({"A": sf_diag(fit25=(0.979999, 0.99, 0.99), final=(0.98, 0.99, 0.99))})
    assert reading["label"] == "BUDGET-BINDING" and not reading["fit_at25"]["ok"] and reading["fit_at_stop"]["ok"]
    assert R.solvefeas_reading({"A": sf_diag(fit25=(0.98, 0.98, 0.98), final=(0.98, 0.98, 0.98))})["label"] == "FIT-PASSES-AT-25"
    early = sf_diag(n=12, stopped="loss<0.05", final=(0.99, 0.99, 0.99))
    assert R.solvefeas_reading({"A": early})["label"] == "FIT-PASSES-AT-25"
    regressed = sf_diag(fit25=(0.99, 0.99, 0.99), fit40=(0.979, 0.99, 0.99), final=(0.979999, 0.99, 0.99))
    reading = R.solvefeas_reading({"A": regressed})
    assert reading["label"] == "UNDERFIT-AT-50" and reading["underfit"][0]["fit_at25"] == 0.99
    for bad in (sf_diag(n=25), {**sf_diag(), "history": []}):
        expect_error(ValueError, lambda: R.solvefeas_reading({"A": bad}))


def test_underfit_class_boundaries():
    plateau = sf_diag(fit40=(0.977, 0.99, 0.99), final=(0.978999, 0.99, 0.99))
    boundary = sf_diag(fit40=(0.977, 0.99, 0.99), final=(0.979, 0.99, 0.99))
    descending = sf_diag(fit40=(0.95, 0.99, 0.99), final=(0.97, 0.99, 0.99))
    falling = sf_diag(fit40=(0.97, 0.99, 0.99), final=(0.95, 0.99, 0.99))
    objective = sf_diag(n=12, stopped="loss<0.05", final=(0.97, 0.99, 0.99))
    assert R.underfit_class(plateau, 0) == "plateaued"
    assert R.underfit_class(boundary, 0) == "still-descending"             # strict < 0.002; equality is not a plateau
    assert R.underfit_class(descending, 0) == "still-descending" and R.underfit_class(falling, 0) == "still-descending"
    assert R.underfit_class(objective, 0) == "objective-stopped"
    assert R.underfit_class({**plateau, "stopped_by": "loss<0.05"}, 0) == "objective-stopped"
    expect_error(ValueError, lambda: R.underfit_class(sf_diag(n=40), 0))
    for diag, cls in ((plateau, "plateaued"), (descending, "still-descending"), (objective, "objective-stopped")):
        reading = R.solvefeas_reading({"A": diag})
        assert reading["label"] == "UNDERFIT-AT-50" and reading["classes"] == [cls] and list(reading["qualifications"]) == [cls]
    mixed = R.solvefeas_reading({"A": plateau, "B": descending, "C": objective})
    assert mixed["classes"] == ["objective-stopped", "plateaued", "still-descending"] and len(mixed["underfit"]) == 3


def test_solve_budget_positive_control():
    settings = sf_settings()
    records = lambda n: [{**settings, "loss_evals": n}]
    assert not R.solve_budget(records(25), {"A": sf_diag(n=25, stopped="loss<0.05")}, settings)["ok"]
    assert R.solve_budget(records(26), {}, settings)["ok"]
    assert R.solve_budget(records(50), {}, settings)["ok"]
    assert R.solve_budget(records(25), {"A": sf_diag()}, settings)["ok"]
    assert not R.solve_budget([], {}, settings)["ok"]
    for n in (0, -1, 51, None, 26.0, True):
        assert not R.solve_budget(records(n), {}, settings)["ok"], n
    for key, bad in (("arm", "sharedz"), ("hparams", "bad"), ("hparams_sha256", "0" * 64), ("v_num_grad_steps", 25)):
        assert not R.solve_budget([{**records(50)[0], key: bad}], {}, settings)["ok"], key
    v = R.verdict(sf_run(), sf_pass(evaluations=25))
    assert v["label"] == "INVALID" and any("more than 25" in r for r in v["reasons"]), v


def test_solvefeas_noise_precedence():
    fitted = R.solvefeas_reading({"A": sf_diag()})
    underfit = R.solvefeas_reading({"A": sf_diag(final=(0.97, 0.99, 0.99))})
    screen, good, bad = {"outcome": "PASS"}, {"ok": True}, {"ok": False}
    assert R.solvefeas_cell1_outcome(fitted, good, screen, good) == "PROCEED"
    assert R.solvefeas_cell1_outcome(fitted, bad, screen, good) == "NOISE-NON-DISCRIMINATING"
    assert R.solvefeas_cell1_outcome(underfit, bad, screen, good) == "UNDERFIT-AT-50"
    assert R.solvefeas_cell1_outcome(underfit, good, screen, bad) == "INVALID"
    assert R.solvefeas_cell1_outcome(fitted, good, {"outcome": "CONCENTRATED"}, good) == "CONCENTRATED"
    base = {s: [True] * 3 for s in SUBJ[:16]}
    up5 = dict(base, **{SUBJ[16]: [True] * 3, SUBJ[17]: [True, True, False]})
    up6 = dict(base, **{SUBJ[16]: [True] * 3, SUBJ[17]: [True] * 3})
    down5 = dict(base); down5[SUBJ[0]] = [False] * 3; down5[SUBJ[1]] = [False, False, True]
    down6 = dict(down5); down6[SUBJ[1]] = [False] * 3
    for twin, allowed in ((up5, True), (up6, False), (down5, True), (down6, False)):
        assert R.noise_twin_verdict(rows(base, twin))["ok"] == allowed


def test_reference_shift_boundaries():
    for para in (5, 18):
        for canon in (5, 10):
            assert not R.reference_shift({"para_full_n": para, "canon_full_n": canon})
    for para, canon in ((4, 8), (19, 8), (10, 4), (10, 11)):
        assert R.reference_shift({"para_full_n": para, "canon_full_n": canon})
        v = R.verdict(sf_run(), sf_pass(ref_n=para, canon=canon))
        assert v["label"] == "REFERENCE-SHIFT" and not v["reasons"] and not v["replication_pending"], v
    shifted = sf_pass(ref_n=19); shifted["a1"]["para_full_n"] = 67
    assert R.verdict(sf_run(), shifted)["label"] == "INVALID"                       # controls remain validity gates
    v = R.verdict(sf_run(second="REFERENCE-SHIFT"), sf_pass(), sf_pass(ref_n=19))
    assert v["label"] == "REFERENCE-SHIFT" and not v["reasons2"], v
    assert R.retry_refusal(sf_run(second="REFERENCE-SHIFT"))
    assert R.verdict(sf_run(second="REFERENCE-SHIFT"), sf_pass())["label"] == "INVALID"
    expect_error(ValueError, lambda: R.second_process_state(synth_run(second="REFERENCE-SHIFT")))


def test_solvefeas_replication_and_qualifiers():
    one, two = sf_pass(), sf_pass()
    two["dw_shared"] = 160.0
    v = R.verdict(sf_run(second="COMPLETED"), one, two)
    assert v["label"] == "LEAD-LARGE-WRITE" and v["solvefeas1"]["label"] == "BUDGET-BINDING", v
    under = sf_run(second="UNDERFIT-AT-50")
    under["second_process"]["per_fact"] = {"A": sf_diag(final=(0.97, 0.99, 0.99))}
    v = R.verdict(under, one)
    assert v["label"] == "LEAD-NOT-REPLICATED" and not v["replication_pending"] and not v["reasons2"], v
    assert R.retry_refusal(under)
    assert R.verdict(sf_run(second="INVALID"), one)["label"] == "INVALID"


def test_source_hash_inputs():
    tree = ast.parse(DRIVER.read_text())
    value = next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SOURCE_FILES" for t in n.targets))
    sources = eval(compile(ast.Expression(body=value), str(DRIVER), "eval"), {"ARM": R.select_arm("solvefeas")})
    for path in ("experiments/c10s/design/C10S_SHARED_Z_PREREG.md", "experiments/c10s/design/C10S_SOLVEFEAS_PREREG.md", R.select_arm().hparams, R.select_arm("solvefeas").hparams):
        assert path in sources and (ROOT / path).is_file(), path


def sf_inject(diag):
    run = sf_run()
    control = {f: {"additive": {"canonical": 1, "shared": 1}, "absolute": {"canonical": 1, "shared": 1}} for f in R.FRAME_NAMES}
    return {**sf_settings(), "identity": dict(run["identity"]), "n_subjects": 1,
            "screen": {"canon_n": 51, "shared_n": 69, "gain": 18, "net_by_template": dict(zip(R.PTEST, (4, 9, 5))),
                       "templates_won": 3, "subjects_won": 12, "outcome": "PASS"},
            "fit_diagnostic": R.fit_diagnostic({"S0": diag["frame_fit"]}), "clamp_hits": 1, "mean_steps": diag["loss_evals"] - 1,
            "canon_template_inj": {"canonical": 24, "shared": 24}, "control_c": control,
            "noise_twin": {"ok": True, "gain": 3, "disagreeing_pairs": 17, "n_pairs": 72},
            "rows": [{"subj": "S0", "shared_solve": diag}], "engine_solves": [{**sf_settings(), "loss_evals": 50}],
            "evaluation_25_injection": {"shared_n": 69, "per_template": dict(zip(R.PTEST, (20, 24, 25))), "record_only": True}}


def raw_pass(pr):
    """Synthetic data at the harness JSON boundary, for the actual read_pass + reader CLI."""
    ref = copy.deepcopy(pr["ref"])
    ref["extra"] = {"shared": pr["shared"], "shared_rows": pr["shared_rows"], "shared_delta_norms": {"8": {"delta_norm": pr["dw_shared"]}},
                    "frame_probe_ref": {f: {"flips": pr["frames_ref"][f], "n": 6} for f in R.FRAME_NAMES},
                    "frame_probe_shared": {f: {"flips": pr["frames_shared"][f], "n": 6} for f in R.FRAME_NAMES},
                    "override_hits_before": 0, "override_hits_after": 1, "key_cosine_ref": {}, "key_cosine_shared": {}, "residual_shared": {"overall": 0.03}}
    arms = {"A1_single": copy.deepcopy(pr["a1"]), "A2_coherent2": copy.deepcopy(pr["a2"]), "A7_coined_coined": ref}
    for arm in arms.values():
        arm.setdefault("extra", {})["residual_ref"] = {"overall": 0.03}
    return {**pr["settings"], "identity": pr["identity"], "z_override_hits_total": 1, "pre_edit": {"key_cosine": {}},
            "engine_solves": pr["engine_solves"], "sharedz": {"fit_diagnostic": pr["fit"], "per_fact": pr["per_fact"]},
            "recipes": {"A7_sharedz": {"law5_gate": {"ok": True}, "arms": arms, "delta_norms": {"A7_coined_coined": {"8": {"delta_norm": pr["dw_ref"]}}}}}}


def test_injection_record_binding():
    run = sf_run(); diag = sf_diag(); inj = sf_inject(diag)
    assert R.injection_validity(run, inj, {"S0": diag}) == []
    for key, bad in (("arm", "sharedz"), ("hparams", "wrong.json"), ("hparams_sha256", "0" * 64), ("v_num_grad_steps", 25)):
        stale = copy.deepcopy(inj); stale["identity"][key] = bad
        assert R.injection_validity(run, stale, {"S0": diag}), key
    other = copy.deepcopy(inj); other["identity"]["run_id"] = "another-run"
    assert R.injection_validity(run, other, {"S0": diag})


def test_reader_record_interface():
    def read(inj, pr=None):
        run = sf_run(); run["cell1_outcome"] = "PROCEED"                             # reader recomputes the new arm's outcome
        with tempfile.TemporaryDirectory() as d:
            Path(d, "run.json").write_text(json.dumps(run)); Path(d, "inject.json").write_text(json.dumps(inj))
            if pr is not None:
                Path(d, "pass1.json").write_text(json.dumps(raw_pass(pr)))
            output, code = io.StringIO(), 0
            with patch.object(sys, "argv", ["c10s_sharedz_read.py", d]), contextlib.redirect_stdout(output):
                try:
                    R.main()
                except SystemExit as e:
                    code = e.code
            return code, output.getvalue()
    under = sf_inject(sf_diag(fit40=(0.977, 0.99, 0.99), final=(0.9789, 0.99, 0.99)))
    code, out = read(under)
    assert code == 0 and "UNDERFIT-AT-50" in out and "plateaued" in out and "evaluation-25 fit" in out and "next: step 2" in out, out
    fitted = sf_inject(sf_diag())
    code, out = read(fitted)
    assert code == 3 and "BUDGET-BINDING" in out and "missing" in out, out
    altered = copy.deepcopy(fitted); altered["evaluation_25_injection"]["shared_n"] = 0
    assert read(altered)[0] == 3                                                     # the snapshot injection is recorded, never gated
    code, out = read(fitted, sf_pass(ref_n=19))
    assert code == 0 and "REFERENCE-SHIFT" in out and "INVALID" not in out, out
    for control in ("a1", "a2"):
        pr = sf_pass(); pr[control]["para_full_n"] = 68
        assert read(fitted, pr)[0] == 0
        pr[control]["para_full_n"] = 67
        assert read(fitted, pr)[0] == 2
    noisy = copy.deepcopy(fitted); noisy["noise_twin"].update(ok=False, gain=6)
    code, out = read(noisy)
    assert code == 0 and "NOISE-NON-DISCRIMINATING" in out and "write arm was not run" in out, out
    early = sf_inject(sf_diag(n=25, stopped="loss<0.05")); early["engine_solves"][0]["loss_evals"] = 25
    code, out = read(early)
    assert code == 2 and "INVALID" in out and "more than 25" in out, out
    stale = copy.deepcopy(fitted); stale["identity"]["hparams_sha256"] = "0" * 64
    code, out = read(stale)
    assert code == 2 and "settings mismatch" in out, out


def original(path):
    result = subprocess.run(["/usr/bin/git", "show", f"1169794:{path}"], cwd=ROOT, capture_output=True, text=True, check=True)
    assert result.stdout
    return result.stdout


def test_default_records_1169794():
    rel = "code/lab/track_c/c10s_sharedz_arms.py"
    old_tree = ast.parse(original(rel)); new_tree = ast.parse(DRIVER.read_text())
    names = ("write_json", "halt", "dump", "make_identity")
    for arm in ("sharedz", "solvefeas"):
        with tempfile.TemporaryDirectory() as d:
            settings = sf_settings() if arm == "solvefeas" else {}
            ns = {"os": os, "json": json, "hashlib": hashlib, "RECORD_SETTINGS": settings, "ARM_RECORD": sf_settings(),
                  "source_hashes": lambda: {"fixture.py": "abc"}, "utc_now": lambda: "2026-10-06T000000Z", "DECISION_ID": R.select_arm(arm).decision_id,
                  "STAGE": "first", "IDENTITY": None, "HALT_PATH": str(Path(d) / "halt.json")}
            current = driver_defs(names, dict(ns))
            old_nodes = [n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
            prior = dict(ns); exec(compile(ast.Module(body=old_nodes, type_ignores=[]), "1169794", "exec"), prior)
            identity = current["make_identity"](out_dir="fixture")
            if arm == "sharedz":
                assert identity == prior["make_identity"](out_dir="fixture")
            else:
                assert not R.settings_mismatches(identity, sf_settings())
            path = str(Path(d) / "record.json"); obj = {"value": 1}
            current["dump"](path, obj); emitted = Path(path).read_text()
            if arm == "sharedz":
                prior["dump"](path, {"value": 1}); assert emitted == Path(path).read_text()
            else:
                assert not R.settings_mismatches(json.loads(emitted), sf_settings())
            expect_error(SystemExit, lambda: current["halt"]("fixture halt", value=1))
            emitted = Path(ns["HALT_PATH"]).read_text()
            if arm == "sharedz":
                expect_error(SystemExit, lambda: prior["halt"]("fixture halt", value=1))
                assert emitted == Path(ns["HALT_PATH"]).read_text()
            else:
                assert not R.settings_mismatches(json.loads(emitted), sf_settings())
    source_node = next(n for n in new_tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SOURCE_FILES" for t in n.targets))
    sources = eval(compile(ast.Expression(body=source_node.value), str(DRIVER), "eval"), {"ARM": R.select_arm()})
    old_sources = next(ast.literal_eval(n.value) for n in old_tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SOURCE_FILES" for t in n.targets))
    assert sources == old_sources


def test_default_equality_1169794():
    rel = "code/lab/track_c/c10s_sharedz_read.py"
    baseline = types.ModuleType("c10s_sharedz_read_1169794"); baseline.__file__ = str(ROOT / rel)
    exec(compile(original(rel), baseline.__file__, "exec"), baseline.__dict__)          # pure reader only
    for shared in range(73):
        for ref in range(25):
            for gates in (False, True):
                for ratio in (1.0, 1.5, 1.500001):
                    for second in (None, (29, 10, True, 1.0), (30, 10, False, 1.6), (30, 10, True, 1.6)):
                        assert R.label(shared, ref, gates, ratio, second) == baseline.label(shared, ref, gates, ratio, second)
    for state in (None, "STARTED", "UNDERFIT", "COMPLETED"):
        for count in (10, 25, 32):
            run, pr = synth_run(second=state), synth_pass(count)
            assert R.verdict(run, pr) == baseline.verdict(run, pr)
            if state == "COMPLETED":
                assert R.verdict(run, pr, synth_pass(31)) == baseline.verdict(run, pr, synth_pass(31))
    assert R.cell1_outcome({"ok": False}, {"ok": False}, {"outcome": "PASS"}) == baseline.cell1_outcome({"ok": False}, {"ok": False}, {"outcome": "PASS"})
    base_path = R.select_arm().hparams
    assert (ROOT / base_path).read_text() == original(base_path)
    old_tree = ast.parse(original("code/lab/track_c/c10s_sharedz_arms.py")); new_tree = ast.parse(DRIVER.read_text())
    old = next(n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name == "compute_z_shared")
    new = next(n for n in new_tree.body if isinstance(n, ast.FunctionDef) and n.name == "compute_z_shared")
    class DefaultPath(ast.NodeTransformer):
        def visit_If(self, node):
            if ast.dump(node.test) == ast.dump(ast.parse('ARM.name == "solvefeas"', mode="eval").body):
                return [self.visit(n) for n in node.orelse]
            return self.generic_visit(node)
        def visit_FunctionDef(self, node):
            return None if node.name == "snapshot" else self.generic_visit(node)
        def visit_Assign(self, node):
            if ast.dump(node) == ast.dump(ast.parse("snapshot25, delta25, target25 = None, None, None").body[0]):
                return None
            return self.generic_visit(node)
        def visit_Dict(self, node):
            pairs = [(k, v) for k, v in zip(node.keys, node.values) if not (k is None and isinstance(v, ast.Name) and v.id == "RECORD_SETTINGS")]
            node.keys, node.values = [k for k, v in pairs], [v for k, v in pairs]
            return self.generic_visit(node)
    # Excluding additive provenance and unreachable diagnostics, every computational statement is identical.
    lowered = DefaultPath().visit(copy.deepcopy(new))
    assert ast.dump(lowered) == ast.dump(old), "default solver computation differs from 1169794"


def test_bogus_arm_writes_no_halt_file():
    """Advisor impl review BLOCKING 1: an unknown C10S_ARM exits before the arm is bound and must not write the step-1
    halt file (tracked, cited by evidence/CORPUS/51). The driver exits at the selector, before any harness or model import."""
    root = Path(__file__).resolve().parents[3]
    halt_file = root / "experiments/c10s/runs/c10s_sharedz/halts/c10s_sharedz_halt_diagnostic.json"
    before = (halt_file.read_bytes(), halt_file.stat().st_mtime_ns) if halt_file.exists() else None
    env = {**os.environ, "C10S_ARM": "solveFeas", "LLMDB_ROOT": str(root), "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, "-B", str(root / "code/lab/track_c/c10s_sharedz_arms.py"), "first"],
                       env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode != 0 and "no diagnostic written" in (p.stderr + p.stdout), (p.returncode, p.stdout[-300:], p.stderr[-300:])
    after = (halt_file.read_bytes(), halt_file.stat().st_mtime_ns) if halt_file.exists() else None
    assert before == after, "the step-1 halt file changed"


def main():
    tests = [test_bogus_arm_writes_no_halt_file, test_overlap_table, test_prompt_plan, test_nll_reduction, test_fit, test_screen, test_label, test_gates, test_verdict, test_second_process_record,
             test_a2_engine_parity_plans, test_noise_twin, test_arm_selector_and_config, test_settings_before_import_and_hp_rebinding,
             test_inertness_settings_binding, test_second_process_settings_binding, test_forward_counting_and_cleanup,
             test_evaluation25_snapshot, test_solvefeas_fit_labels, test_underfit_class_boundaries, test_solve_budget_positive_control,
             test_solvefeas_noise_precedence, test_reference_shift_boundaries, test_solvefeas_replication_and_qualifiers,
             test_source_hash_inputs, test_injection_record_binding, test_reader_record_interface, test_default_records_1169794, test_default_equality_1169794]
    for t in tests:
        t(); print(f"ok  {t.__name__}")
    print(f"C10S_SELFTEST_PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
