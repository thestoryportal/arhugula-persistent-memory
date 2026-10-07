#!/usr/bin/env python3
"""D-C10s-sharedz pure-function selftest. Imports ONLY c10s_sharedz_read (no harness, no engine, no model; torch only for
the reduction test on a fixed tensor): the overlap table, the prompt-ordering builder, the engine's NLL reduction vs a
naive one on the same fp16 log-probability tensor, the fit diagnostic, the screen rule, the label function and the
whole verdict on synthetic pass records (implementation review items 1, 2, 5).
[LAW:behavior-not-structure] every assertion is a §2/§3 rule stated as an outcome. Exit 0 = all pass; any failure raises."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10s_sharedz_read as R

CTX = [["{}"], ["The sun rose. {}", "Therefore it was. {}", "Because of that. {}", "I think so. {}", "You said it. {}"]]   # engine shape: memit_main.py:308
SUBJ = [f"S{i}" for i in range(24)]


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
    g = torch.Generator().manual_seed(7)
    T, L, Vn = 40, 64, 50
    log_probs = (-torch.rand((2, L, Vn), generator=g) * 6 - 0.05).to(torch.float16)
    targets = torch.full((2, L), -100, dtype=torch.long)
    tgt = torch.randint(0, Vn, (T,), generator=g)
    for i, ex_len in enumerate((L, L - 9)):                                             # row 1 right-padded, as the engine's batch is
        targets[i, ex_len - T: ex_len] = tgt
    engine = R.engine_nll_each(log_probs, targets, T)
    assert engine.dtype == torch.float32 and engine.shape == (2,), engine
    for i, ex_len in enumerate((L, L - 9)):
        rows = log_probs[i, ex_len - T: ex_len].gather(1, tgt.view(-1, 1)).squeeze(1)
        manual = -(rows * torch.ones(T, dtype=torch.float32)).sum() / T                # the engine's arithmetic, written out
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


def main():
    tests = [test_overlap_table, test_prompt_plan, test_nll_reduction, test_fit, test_screen, test_label, test_gates, test_verdict, test_second_process_record,
             test_a2_engine_parity_plans, test_noise_twin]
    for t in tests:
        t(); print(f"ok  {t.__name__}")
    print(f"C10S_SELFTEST_PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
