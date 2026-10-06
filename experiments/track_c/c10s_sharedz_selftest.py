#!/usr/bin/env python3
"""D-C10s-sharedz pure-function selftest. Imports ONLY c10s_sharedz_read (no harness, no engine, no model): the overlap
table, the prompt-ordering builder, the fit diagnostic, the screen rule and the label function on synthetic numbers.
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
    assert R.cell1_outcome({"ok": False}, s) == "UNDERFIT" and R.cell1_outcome({"ok": True}, s) == "PROCEED"
    assert R.cell1_outcome({"ok": True}, {"outcome": "CONCENTRATED"}) == "CONCENTRATED"


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
    assert L(32, 10, True, 1.0, second=(31, 9)) == "LEAD"
    assert L(32, 10, True, 1.0, second=(29, 9)) == "LEAD-NOT-REPLICATED"
    assert L(25, 10, True, 1.0, second=(22, 11)) == "PARTIAL"
    assert L(25, 10, True, 1.0, second=(22, 14)) == "PARTIAL-NOT-REPLICATED"   # gain 8 < 10
    assert L(25, 10, True, 1.0, second=(18, 5)) == "PARTIAL-NOT-REPLICATED"    # inside the envelope
    assert L(25, 10, True, 2.0, second=(22, 14)) == "PARTIAL-NOT-REPLICATED-LARGE-WRITE"


def test_gates():
    ref = {"locality_axes": {"L1_flipped_to_edited_value": 2, "L3_top1_agree": 30, "generic_ppl_post": 20.0}, "locality_described_as": 97.0}
    ok = {"locality_axes": {"L1_flipped_to_edited_value": 3, "L3_top1_agree": 29, "generic_ppl_post": 20.5}, "locality_described_as": 94.0}
    g = R.locality_gates(ref, ok, {"CANON": 1, "T1": 0, "T2": 2}, {"CANON": 2, "T1": 1, "T2": 3})
    assert all(g.values()), g
    bad = R.locality_gates(ref, ok, {"CANON": 1, "T1": 0, "T2": 2}, {"CANON": 2, "T1": 2, "T2": 3})
    assert not bad["same_frame_fictional_T1"] and sum(not v for v in bad.values()) == 1, bad
    l3 = dict(ok, locality_axes=dict(ok["locality_axes"], L3_top1_agree=28))
    assert not R.locality_gates(ref, l3, {"CANON": 0, "T1": 0, "T2": 0}, {"CANON": 0, "T1": 0, "T2": 0})["L3"]


def main():
    tests = [test_overlap_table, test_prompt_plan, test_fit, test_screen, test_label, test_gates]
    for t in tests:
        t(); print(f"ok  {t.__name__}")
    print(f"C10S_SELFTEST_PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
