#!/usr/bin/env python3
"""D-C10s-sharedz mechanical reader (docs/C10S_SHARED_Z_PREREG.md v3 FROZEN, §2 cell 1 + §3). No model judgement.
Usage: c10s_sharedz_read.py results/c10s_sharedz          (reads run.json, inject.json, pass1.json [, pass2.json])
Exit 0 = a label was printed; exit 2 = INVALID; exit 3 = a required file is missing.

[LAW:one-source-of-truth] every threshold of §2/§3 lives here once; the driver records numbers only and calls the
rules below (screen, fit, cell-1 outcome) instead of restating them. This module is the one model-free module of the
arm, so the pure helpers the driver and the inertness script share (frozen forms, overlap table, prompt plan, fit
aggregation) live here too and the selftest imports only this file. [LAW:one-way-deps] arms -> read, inertness -> read.
"""
import sys, json, os, re, math, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c10l_mint_read import L3_THR                                  # 29/30 (§3 locality gates)
from c10m_diag_read import FINGERPRINT, ENV_PARA, ENV_CANON        # d941a9fb; identical-baseline envelope [5,18]/72, [5,10]/24 (§3 validity)

# ---- frozen forms (§2 "Training phrasings", published before the run) ----
CANON = "The capital of {} is the city of"          # must equal c10e_bandknob.CANON (the driver checks)
T1 = "The government of {} sits in"
T2 = "{} is a country whose capital is"
FRAMES = [CANON, T1, T2]                             # the shared solve's prompt list; CANON first (§2: index 0 = identity template on CANON)
FRAME_NAMES = ["CANON", "T1", "T2"]
PTEST = [                                            # sealed held-out set, c10e_bandknob.py:52-56 (the driver checks equality)
    "{}'s capital city is called",
    "If you visit {}, its capital city is",
    "The main city and seat of government of {} is",
]
V1_WITHDRAWN = "In {}, the capital city is"          # §2: failed the overlap rule; the selftest proves the table detects it
KL_PROMPT = "{} is a"                                # compute_z.py:50, appended last and single

# ---- thresholds ----
SCREEN_GAIN_MIN = 6            # §2 cell 1 screen rule: shared - canonical >= 6/72
SCREEN_MIN_TEMPLATES = 2       # §2: net paired wins on at least two held-out templates
SCREEN_MIN_SUBJECTS = 4        # §2: ... and at least four subjects; otherwise CONCENTRATED
FIT_MIN = 0.98                 # §2 fit diagnostic: any training frame < 0.98 for any fact at stop -> UNDERFIT
CTRL_MIN = 68                  # §3 validity: A1 >= 68, A2 >= 68
LEAD_MIN = 30                  # §3: LEAD if shared para_full >= 30/72
PARTIAL_GAIN_MIN = 10          # §3: PARTIAL needs gain >= 10 (and shared > ENV_PARA[1], < LEAD_MIN)
L1_SLACK, FRAME_SLACK, DESC_SLACK, PPL_SLACK = 1, 1, 3, 0.5   # §3 locality gates vs the same-run reference
LARGE_WRITE_RATIO = 1.5        # §3 write-size qualifier: ||dW_shared|| / ||dW_ref|| (summed over layers) > 1.5 -> -LARGE-WRITE
FRAME_N = 6                    # the same-frame fictional probe's six never-edited subjects (c10p_twopass_arms.py:30)
OVERRIDE_HITS = (0, 1, 1)      # §3 validity: Z_OVERRIDE consumed by A7 only, exactly once: hits before the hook, after it, pass total
INERTNESS_CHECKS = ("i_floor", "ii_single", "iii_triplicate", "iv_heterogeneous", "v_harness_law5")   # §2 (i)-(v)


# ---- pure helpers shared with the driver ----
def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def form_words(form):
    """§2 overlap rule: the subject slot removed, lower-cased, word tokens (apostrophes kept inside a token)."""
    return re.findall(r"[a-z']+", form.replace("{}", " ").lower())


def ngrams3(form):
    w = form_words(form)
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}


def overlap_table(train_forms, heldout_forms):
    """Every (training form, held-out form) pair with the word 3-grams they share. `train_forms` is an ordered mapping
    name -> form. total_shared == 0 is the §2 rule; the driver refuses to run otherwise."""
    pairs = []
    for name, tf in train_forms.items():
        for hf in heldout_forms:
            shared = sorted(" ".join(g) for g in ngrams3(tf) & ngrams3(hf))
            pairs.append({"train": name, "train_form": tf, "heldout_form": hf, "shared_3grams": shared})
    return {"pairs": pairs, "total_shared": sum(len(p["shared_3grams"]) for p in pairs)}


def build_prompt_plan(context_templates, prompts, target_prefix, kl_prompt=KL_PROMPT):
    """The shared solve's rewriting set (§2): template-major over the engine's context templates, the frames in the given
    order inside each template, so index 0 is (identity template, prompts[0]); the KL prompt last and single
    (compute_z.py:46-51 with `prompts` in place of request["prompt"]). `frame_idx[i]` = which frame rewriting prompt i
    carries. Raises if the engine's invariant context_templates[0][0] == "{}" (memit_main.py:308) does not hold."""
    if not context_templates or not context_templates[0] or context_templates[0][0] != "{}":
        raise ValueError(f"context_templates[0][0] must be the identity template '{{}}', got {context_templates[:1]!r}")   # [LAW:no-silent-failure]
    rewriting, frame_idx = [], []
    for context_types in context_templates:
        for context in context_types:
            for f, prompt in enumerate(prompts):
                rewriting.append(context.format(prompt) + target_prefix)
                frame_idx.append(f)
    return {"rewriting": rewriting, "frame_idx": frame_idx, "kl": [kl_prompt], "all": rewriting + [kl_prompt]}


def frame_fit(nll_each, frame_idx, n_frames):
    """§2 cell 1: per frame, the engine's exp(-nll) per prompt (compute_z.py:149,162) averaged over that frame's
    context templates."""
    out = []
    for f in range(n_frames):
        vals = [math.exp(-x) for x, g in zip(nll_each, frame_idx) if g == f]
        if not vals:
            raise ValueError(f"frame {f} has no prompts")   # [LAW:no-silent-failure]
        out.append(sum(vals) / len(vals))
    return out


def fit_diagnostic(fits):
    """`fits`: subject -> [fit per frame, FRAME_NAMES order]. Any entry < FIT_MIN -> UNDERFIT (§2)."""
    under = [{"subj": s, "frame": FRAME_NAMES[f], "fit": v} for s, fv in fits.items() for f, v in enumerate(fv) if v < FIT_MIN]
    return {"ok": not under, "min_fit": min(v for fv in fits.values() for v in fv), "underfit": under}


def paired_screen(rows):
    """§2 cell 1 screen rule on paired per-(subject, template) outcomes over the held-out templates.
    rows: [{"subj", "canon": [bool x3], "shared": [bool x3]}] in PTEST order."""
    n_t = len(PTEST)
    canon_n = sum(sum(r["canon"]) for r in rows)
    shared_n = sum(sum(r["shared"]) for r in rows)
    net_by_template = {PTEST[k]: sum(int(r["shared"][k]) - int(r["canon"][k]) for r in rows) for k in range(n_t)}
    net_by_subject = {r["subj"]: sum(int(s) - int(c) for s, c in zip(r["shared"], r["canon"])) for r in rows}
    gain = shared_n - canon_n
    templates_won = sum(v > 0 for v in net_by_template.values())
    subjects_won = sum(v > 0 for v in net_by_subject.values())
    spread_ok = templates_won >= SCREEN_MIN_TEMPLATES and subjects_won >= SCREEN_MIN_SUBJECTS
    if gain < SCREEN_GAIN_MIN:
        outcome = "NOT-ADVANCED-SCREEN"
    elif not spread_ok:
        outcome = "CONCENTRATED"
    else:
        outcome = "PASS"
    return {"canon_n": canon_n, "shared_n": shared_n, "gain": gain, "net_by_template": net_by_template,
            "net_by_subject": net_by_subject, "templates_won": templates_won, "subjects_won": subjects_won, "outcome": outcome}


def cell1_outcome(fit, screen):
    """§2 cell 1: UNDERFIT takes precedence (nothing is concluded about frames); then the screen."""
    if not fit["ok"]:
        return "UNDERFIT"
    return "PROCEED" if screen["outcome"] == "PASS" else screen["outcome"]


def locality_gates(ref, shared, frames_ref, frames_shared):
    """§3 locality gates vs the same-run reference. `ref`/`shared` are eval_arm dicts with locality_axes and
    locality_described_as; `frames_*` map FRAME_NAMES -> flips."""
    ar, ash = ref["locality_axes"], shared["locality_axes"]
    gates = {"L1": ash["L1_flipped_to_edited_value"] <= ar["L1_flipped_to_edited_value"] + L1_SLACK,
             "described_as": shared["locality_described_as"] >= ref["locality_described_as"] - DESC_SLACK,
             "L3": ash["L3_top1_agree"] >= L3_THR,
             "ppl": ash["generic_ppl_post"] <= ar["generic_ppl_post"] + PPL_SLACK}
    for name in FRAME_NAMES:
        gates[f"same_frame_fictional_{name}"] = frames_shared[name] <= frames_ref[name] + FRAME_SLACK
    return gates


def label(shared_n, ref_n, gates_ok, dw_ratio, second=None):
    """§3 binding label from counts. `second` = (shared_n, ref_n) of the second process, or None (not yet run)."""
    gain = shared_n - ref_n
    lead_sized = shared_n >= LEAD_MIN
    partial_sized = ENV_PARA[1] < shared_n < LEAD_MIN and gain >= PARTIAL_GAIN_MIN   # Codex item 6: inside [5,18] is NULL whatever the gain
    if lead_sized and gates_ok:
        lab = "LEAD"
    elif partial_sized and gates_ok:
        lab = "PARTIAL"
    elif lead_sized or partial_sized:
        lab = "TRADEOFF"
    else:
        lab = "NULL"
    if second is not None and lab == "LEAD":
        lab = "LEAD" if second[0] >= LEAD_MIN else "LEAD-NOT-REPLICATED"
    if second is not None and lab == "PARTIAL":
        lab = "PARTIAL" if (second[0] > ENV_PARA[1] and second[0] - second[1] >= PARTIAL_GAIN_MIN) else "PARTIAL-NOT-REPLICATED"
    if dw_ratio > LARGE_WRITE_RATIO:
        lab += "-LARGE-WRITE"
    return lab


# ---- result-file access ----
def load(d, name, required=True):
    p = os.path.join(d, name)
    if not os.path.exists(p):
        if required:
            print(f"missing {p}"); sys.exit(3)
        return None
    return json.load(open(p))


def read_pass(p):
    """Pull the pass's A7 reference, its hooked shared edit, the controls and the audit counters out of the harness JSON."""
    cand = [k for k in p["recipes"]][0]; rec = p["recipes"][cand]
    a7 = rec["arms"]["A7_coined_coined"]; ex = a7["extra"]
    return {"rec": rec, "ref": a7, "shared": ex["shared"], "shared_rows": ex["shared_rows"],
            "a1": rec["arms"]["A1_single"], "a2": rec["arms"]["A2_coherent2"],
            "dw_ref": sum(v["delta_norm"] for v in rec["delta_norms"]["A7_coined_coined"].values()),
            "dw_shared": sum(v["delta_norm"] for v in ex["shared_delta_norms"].values()),
            "frames_ref": {n: ex["frame_probe_ref"][n]["flips"] for n in FRAME_NAMES},
            "frames_shared": {n: ex["frame_probe_shared"][n]["flips"] for n in FRAME_NAMES},
            "frame_n": [ex["frame_probe_ref"][n]["n"] for n in FRAME_NAMES] + [ex["frame_probe_shared"][n]["n"] for n in FRAME_NAMES],
            "hits": (ex["override_hits_before"], ex["override_hits_after"], p["z_override_hits_total"]),
            "fit": p["sharedz"]["fit_diagnostic"], "key_cosine": {"pre": p["pre_edit"]["key_cosine"], "ref": ex["key_cosine_ref"], "shared": ex["key_cosine_shared"]}}


def validity(run, pr, which):
    """§3 validity for one harness pass; returns the reasons (empty = valid)."""
    reasons = []
    fp = run["fingerprint"] if which == "1" else run["second_process"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp:
        reasons.append(f"pass {which} fingerprint not {FINGERPRINT}/PASS")
    inert = run["inertness"]
    if not inert["ok"] or any(not inert["checks"].get(c, {}).get("ok") for c in INERTNESS_CHECKS):
        reasons.append("inertness record not all-INERT")
    if not pr["rec"]["law5_gate"]["ok"]:
        reasons.append(f"pass {which} LAW#5 harness gate not inert")
    if pr["a1"]["para_full_n"] < CTRL_MIN or pr["a2"]["para_full_n"] < CTRL_MIN:
        reasons.append(f"pass {which} controls A1 {pr['a1']['para_full_n']} A2 {pr['a2']['para_full_n']} < {CTRL_MIN}")
    if not ENV_PARA[0] <= pr["ref"]["para_full_n"] <= ENV_PARA[1]:
        reasons.append(f"pass {which} reference A7 para {pr['ref']['para_full_n']} outside {ENV_PARA}")
    if not ENV_CANON[0] <= pr["ref"]["canon_full_n"] <= ENV_CANON[1]:
        reasons.append(f"pass {which} reference A7 canon {pr['ref']['canon_full_n']} outside {ENV_CANON}")
    if pr["hits"] != OVERRIDE_HITS:
        reasons.append(f"pass {which} Z_OVERRIDE hits {pr['hits']} != {OVERRIDE_HITS}")
    if any(n != FRAME_N for n in pr["frame_n"]):
        reasons.append(f"pass {which} same-frame probe n != {FRAME_N}")
    if not pr["fit"]["ok"]:
        reasons.append(f"pass {which} shared solve UNDERFIT: {pr['fit']['underfit']}")
    forms = run["training_forms"]
    if any(k not in forms for k in ("CANON", "T1", "T2")) or any("sha256" not in forms[k] for k in ("CANON", "T1", "T2")):
        reasons.append("training-form hashes missing from the run record")
    if "overlap_table" not in run or run["overlap_table"]["total_shared"] != 0:
        reasons.append("overlap table missing or non-zero")
    return reasons


def per_fact_agreement(rows1, rows2):
    by = {r["subj"]: r["para_full_hits"] for r in rows2}
    agree = sum(r["para_full_hits"] == by[r["subj"]] for r in rows1)
    return {"facts_with_identical_held_out_hits": agree, "n": len(rows1)}


def main():
    d = sys.argv[1]
    run = load(d, "run.json"); inj = load(d, "inject.json")
    sc, fit = inj["screen"], inj["fit_diagnostic"]
    print(f"cell 1 injection (unedited model, {inj['n_subjects']} facts): canonical {sc['canon_n']}/72 shared {sc['shared_n']}/72 gain {sc['gain']} "
          f"(screen >= {SCREEN_GAIN_MIN}); net wins by template {sc['net_by_template']}; templates won {sc['templates_won']} (>= {SCREEN_MIN_TEMPLATES}), "
          f"subjects won {sc['subjects_won']} (>= {SCREEN_MIN_SUBJECTS}); canon-template injection canonical {inj['canon_template_inj']['canonical']}/24 shared {inj['canon_template_inj']['shared']}/24")
    print(f"fit diagnostic (>= {FIT_MIN} per fact per frame): min {fit['min_fit']:.4f}; underfit {fit['underfit'] or 'none'}; "
          f"clamp hits {inj['clamp_hits']}/{inj['n_subjects']}; mean steps {inj['mean_steps']}")
    cc = inj["control_c"]
    print("control c (full-sequence greedy, per frame): " + "; ".join(f"{t}: additive {cc[t]['additive']} absolute {cc[t]['absolute']}" for t in cc))
    outcome = run["cell1_outcome"]
    if outcome != "PROCEED":
        print(f"\ncell 1 outcome: {outcome} -> this candidate configuration was not advanced; the write arm was not run (§2)"); return
    p1 = load(d, "pass1.json")
    if p1 is None:
        print("missing pass1.json (cell 1 passed; the harness pass has not run)"); sys.exit(3)
    pr1 = read_pass(p1)
    reasons = validity(run, pr1, "1")
    x, y = pr1["ref"], pr1["shared"]; ax, ay = x["locality_axes"], y["locality_axes"]
    print(f"\n{'pass 1':22} canon/24 para/72 first string | A1 A2 | L1/12 frame CANON/T1/T2 described_as L3/30 ppl | dW")
    for lab, a, ax_, fr, dw in (("reference (engine z)", x, ax, pr1["frames_ref"], pr1["dw_ref"]), ("shared z", y, ay, pr1["frames_shared"], pr1["dw_shared"])):
        print(f"{lab:22} {a['canon_full_n']:>3}     {a['para_full_n']:>3}    {a['para_first_n']:>3}   {a['para_string_n']:>3}   | {pr1['a1']['para_full_n']:>2} {pr1['a2']['para_full_n']:>2} | "
              f"{ax_['L1_flipped_to_edited_value']:>2}    {fr['CANON']}/{fr['T1']}/{fr['T2']}          {a['locality_described_as']:>5}     {ax_['L3_top1_agree']:>2}  {ax_['generic_ppl_post']:.2f} | {dw:.1f}")
    per_t = {t: sum(r["para_full_hits"][k] for r in pr1["shared_rows"]) for k, t in enumerate(PTEST)}
    print(f"shared per held-out template: {per_t} (comparator P6 15/17/17)")
    for layer, v in pr1["key_cosine"]["shared"].items():
        print(f"key cosine to CANON, layer {layer}: " + "; ".join(f"{t}: pre {pr1['key_cosine']['pre'][layer][t]['mean_cos']:.3f} ref {pr1['key_cosine']['ref'][layer][t]['mean_cos']:.3f} shared {v[t]['mean_cos']:.3f}" for t in v))
    if reasons:
        print("\nINVALID —", "; ".join(reasons)); sys.exit(2)
    gates = locality_gates(x, y, pr1["frames_ref"], pr1["frames_shared"]); ratio = pr1["dw_shared"] / pr1["dw_ref"]
    p2 = load(d, "pass2.json", required=False); second = None
    if p2 is not None:
        pr2 = read_pass(p2); r2 = validity(run, pr2, "2")
        if r2:
            print("\nINVALID (second process) —", "; ".join(r2)); sys.exit(2)
        second = (pr2["shared"]["para_full_n"], pr2["ref"]["para_full_n"])
        print(f"\nsecond process: reference {second[1]}/72 shared {second[0]}/72; {per_fact_agreement(pr1['shared_rows'], pr2['shared_rows'])}; dW ratio {pr2['dw_shared'] / pr2['dw_ref']:.2f}")
    lab = label(y["para_full_n"], x["para_full_n"], all(gates.values()), ratio, second)
    print(f"\nlocality gates (shared vs reference): {gates}\nbinding: shared para_full {y['para_full_n']}/72 vs reference {x['para_full_n']} (gain {y['para_full_n'] - x['para_full_n']}); "
          f"LEAD >= {LEAD_MIN}; PARTIAL > {ENV_PARA[1]} with gain >= {PARTIAL_GAIN_MIN}; dW ratio {ratio:.2f} (cap {LARGE_WRITE_RATIO}) -> {lab}")
    if second is None and lab.split("-")[0] in ("LEAD", "PARTIAL"):
        print("second process required (gate A): the label does not carry until replicated")


if __name__ == "__main__":
    main()
