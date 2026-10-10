#!/usr/bin/env python3
"""D-C10s-sharedz mechanical reader (docs/C10S_SHARED_Z_PREREG.md v3 FROZEN, §2 cell 1 + §3 + §7 A1). No model judgement.
Usage: c10s_sharedz_read.py results/c10s_sharedz          (reads run.json, inject.json, pass1.json [, pass2.json])
Exit 0 = a label was printed; exit 2 = INVALID; exit 3 = a required file is missing.

v2 (implementation review items 2, 5): every locality gate and the -LARGE-WRITE qualifier apply to EACH process before a
replicated label; pass1/pass2/inertness records must carry one run identity or they are not paired.

[LAW:one-source-of-truth] every threshold of §2/§3 lives here once; the driver records numbers only and calls the
rules below. This is the one model-free module of the arm, so the pure helpers the driver and the inertness script
share (frozen forms, overlap table, prompt plan, fit aggregation, the engine's NLL reduction) live here too and the
selftest imports only this file. [LAW:one-way-deps] arms -> read, inertness -> read.
"""
import sys, json, os, re, math, hashlib
from typing import Literal, NamedTuple
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
FIT_MIN = 0.98                 # §2 fit diagnostic: any training frame < 0.98 for any fact at stop -> UNDERFIT (the write arm is not run)
CTRL_MIN = 68                  # §3 validity: A1 >= 68, A2 >= 68
LEAD_MIN = 30                  # §3: LEAD if shared para_full >= 30/72
PARTIAL_GAIN_MIN = 10          # §3: PARTIAL needs gain >= 10 (and shared > ENV_PARA[1], < LEAD_MIN)
L1_SLACK, FRAME_SLACK, DESC_SLACK, PPL_SLACK = 1, 1, 3, 0.5   # §3 locality gates vs the same-run reference
LARGE_WRITE_RATIO = 1.5        # §3 write-size qualifier: ||dW_shared|| / ||dW_ref|| (summed over layers) > 1.5 -> -LARGE-WRITE (either process)
FRAME_N = 6                    # the same-frame fictional probe's six never-edited subjects (c10p_twopass_arms.py:30)
OVERRIDE_HITS = (0, 1, 1)      # §3 validity: Z_OVERRIDE consumed by A7 only, exactly once: hits before the hook, after it, pass total
INERTNESS_CHECKS = ("i_floor", "ii_single", "iii_triplicate", "iv_heterogeneous", "v_harness_law5")   # §2 (i)-(v)
PASS_ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")   # §7 A1: the remaining-residual readout is recorded for every arm
PLATEAU_FIT_DELTA = 0.002       # solvefeas §3: absolute frame-fit change between evaluations 40 and 50
SETTINGS_KEYS = ("arm", "hparams", "hparams_sha256", "v_num_grad_steps")


class Arm(NamedTuple):
    name: Literal["sharedz", "solvefeas"]
    decision_id: str
    prereg: str
    halt_path: str
    hparams: str
    steps: int
    out_dir: str


_ARMS = {
    "sharedz": Arm("sharedz", "D-C10s-sharedz", "docs/C10S_SHARED_Z_PREREG.md",
                   "architecture_profile/c10s_sharedz_halt_diagnostic.json",
                   "configs/hparams/qwen25_3b_memit_hparams.json", 25, "results/c10s_sharedz"),
    "solvefeas": Arm("solvefeas", "D-C10s-solvefeas", "docs/C10S_SOLVEFEAS_PREREG.md",
                     "architecture_profile/c10s_solvefeas_halt_diagnostic.json",
                     "configs/hparams/qwen25_3b_memit_hparams_steps50.json", 50, "results/c10s_solvefeas"),
}


def select_arm(name="sharedz"):
    try:
        return _ARMS[name]
    except KeyError:
        raise ValueError(f"C10S_ARM must be sharedz|solvefeas, got {name!r}") from None


def settings_mismatches(record, expected):
    """solvefeas §4: an arm, path, digest and budget travel together across processes."""
    return {k: {"recorded": record.get(k), "expected": expected[k]}
            for k in SETTINGS_KEYS if record.get(k) != expected[k]}


def settings_validity(run, record, where):
    # Records predating the arm selector remain readable under the original rules.
    if "arm" not in run:
        return []
    mismatch = settings_mismatches(record, run)
    return [f"{where} settings mismatch: {mismatch}"] if mismatch else []


def evaluation_fit(diag, evaluation):
    row = diag["history"][evaluation - 1]
    return frame_fit(row["nll_each"], diag["frame_idx"], len(diag["prompts"]))


def underfit_class(diag, frame):
    """solvefeas §3; objective stopping takes precedence over the 40/50 slope."""
    if diag["stopped_by"] == "loss<0.05":
        return "objective-stopped"
    if diag["loss_evals"] != 50 or diag["stopped_by"] != "budget":
        raise ValueError("a budget-stopped solvefeas solve must have 50 evaluations")
    change = abs(evaluation_fit(diag, 50)[frame] - evaluation_fit(diag, 40)[frame])
    return "plateaued" if change < PLATEAU_FIT_DELTA else "still-descending"


def solvefeas_reading(diags):
    """The binding before/after is this process's evaluated states, never a prior template draw."""
    fits25, final = {}, {}
    for subject, diag in diags.items():
        n = diag["loss_evals"]
        if len(diag["history"]) != n or not 1 <= n <= 50:
            raise ValueError(f"{subject}: incomplete solve history")
        if n < 50 and diag["stopped_by"] != "loss<0.05":
            raise ValueError(f"{subject}: shortened solve without objective stopping")
        # A solve that stops early has the same final state under either loop bound.
        fits25[subject] = evaluation_fit(diag, min(25, n))
        final[subject] = evaluation_fit(diag, n)
    at25, at_stop = fit_diagnostic(fits25), fit_diagnostic(final)
    failing = []
    for entry in at_stop["underfit"]:
        subject, frame = entry["subj"], FRAME_NAMES.index(entry["frame"])
        failing.append({**entry, "fit_at25": fits25[subject][frame],
                        "class": underfit_class(diags[subject], frame)})
    classes = [c for c in ("objective-stopped", "plateaued", "still-descending") if any(e["class"] == c for e in failing)]
    lab = "UNDERFIT-AT-50" if not at_stop["ok"] else "FIT-PASSES-AT-25" if at25["ok"] else "BUDGET-BINDING"
    qualifications = {
        "objective-stopped": "the averaged objective, not the budget, ended these solves",
        "plateaued": "the budget alone does not repair these fits; radius/trade-off and frame tension remain unseparated",
        "still-descending": "the budget is not exhausted as an explanation",
    }
    return {"label": lab, "fit_at25": at25, "fit_at_stop": at_stop, "underfit": failing,
            "classes": classes, "qualifications": {c: qualifications[c] for c in classes}}


def solve_budget(engine_solves, shared_diags, expected):
    """Read-only engine forward counts and shared evaluations must exercise the larger bound (§4)."""
    solves = list(engine_solves) + list(shared_diags.values())
    reasons = []
    for i, solve in enumerate(solves):
        mismatch = settings_mismatches(solve, expected)
        n = solve.get("loss_evals")
        if mismatch:
            reasons.append(f"solve {i} settings mismatch: {mismatch}")
        if type(n) is not int or not 1 <= n <= expected["v_num_grad_steps"]:
            reasons.append(f"solve {i} invalid evaluation count {n!r}")
    exercised = any(type(s.get("loss_evals")) is int and s["loss_evals"] > 25 for s in solves)
    if not exercised:
        reasons.append("no solve ran more than 25 evaluations; the larger budget was not exercised")
    return {"ok": not reasons, "reasons": reasons, "positive_control": exercised,
            "engine_solves": len(engine_solves), "shared_solves": len(shared_diags)}


def solvefeas_cell1_outcome(reading, twin, screen, budget):
    if not budget["ok"]:
        return "INVALID"
    if reading["label"] == "UNDERFIT-AT-50":
        return "UNDERFIT-AT-50"
    return cell1_outcome(reading["fit_at_stop"], twin, screen)


def injection_validity(run, inj, diags):
    reasons = []
    if run["v_num_grad_steps"] != select_arm(run["arm"]).steps:
        reasons.append("run step count differs from the selected arm")
    for where, record in (("injection", inj), ("injection identity", inj["identity"]), ("run identity", run["identity"]),
                          ("inertness", run["inertness"]), ("inertness identity", run["inertness"]["identity"])):
        reasons.extend(settings_validity(run, record, where))
    if inj["identity"]["run_id"] != run["identity"]["run_id"]:
        reasons.append("injection identity differs from the run's")
    if run["inertness"]["identity"]["run_id"] != run["identity"]["inertness_run_id"]:
        reasons.append("inertness identity differs from the run's")
    if not run["inertness"]["ok"] or any(not run["inertness"]["checks"].get(c, {}).get("ok") for c in INERTNESS_CHECKS):
        reasons.append("inertness record not all-INERT")
    return reasons + solve_budget(inj["engine_solves"], diags, run)["reasons"]


def reference_shift(ref):
    return not (ENV_PARA[0] <= ref["para_full_n"] <= ENV_PARA[1]
                and ENV_CANON[0] <= ref["canon_full_n"] <= ENV_CANON[1])


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


# ---- §7 A2: context lists that make the UNMODIFIED engine build the batch under test (compute_z.py:46-51) ----
def ctx_triplicate(context_templates):
    """Each context template repeated three times in place: engine(CANON request, this) builds the rewriting list of
    compute_z_shared([CANON]*3) — the (iii) parity reference and the cell-1 noise twin."""
    return [[c for c in group for _ in range(3)] for group in context_templates]


def ctx_heterogeneous(context_templates, prompts):
    """For each context template, c.format(f) for every phrasing f: engine('{}' request, this) builds the shared plan
    (template-major, prompts[0] first inside each template, KL last) — the (iv) parity reference."""
    return [[c.format(f) for c in group for f in prompts] for group in context_templates]


def engine_plan(engine_ctx, request_prompt, target_prefix, kl_prompt=KL_PROMPT):
    """The engine's own list (compute_z.py:46-51) re-derived from the engine-side inputs, written apart from
    build_prompt_plan so a harness plan is checked against the engine's construction, not against itself."""
    return [c.format(request_prompt) + target_prefix for group in engine_ctx for c in group] + [kl_prompt]


def plan_matches(all_prompts, engine_ctx, request_prompt, target_prefix):
    """A2 (iv) structural gate: the solve's ordered prompt list is exactly the engine's for the parity reference."""
    return list(all_prompts) == engine_plan(engine_ctx, request_prompt, target_prefix)


def engine_nll_each(log_probs, rewriting_targets, n_target):
    """The engine's per-prompt NLL reduction, verbatim (compute_z.py:141-149): gather in the log-probs' own dtype, multiply
    by a float32 mask (type promotion lifts the product to fp32), sum over positions, divide by the target length.
    Torch is imported here so the module stays model-free for the reader; the inertness reference and the selftest call
    this one function so no second reduction can drift from the engine's (implementation review item 1)."""
    import torch
    loss = torch.gather(                                                              # :141-145
        log_probs,
        2,
        torch.where(rewriting_targets != -100, rewriting_targets, 0).unsqueeze(2),
    ).squeeze(2)
    mask = (rewriting_targets != -100).float()                                        # :146
    return -(loss * mask).sum(1) / n_target                                           # :149


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


def noise_twin_verdict(rows):
    """§7 A2 (vi): rows as paired_screen with "canon" = the canonical z and "shared" = the twin (canonical objective at
    the shared batch shape). Admissible iff |twin gain| < SCREEN_GAIN_MIN: a gain the screen counts as signal must not
    arise from batch-shape rounding alone, whatever its spread. The reverse screen is recorded beside it."""
    forward = paired_screen(rows)
    reverse = paired_screen([{"subj": r["subj"], "canon": r["shared"], "shared": r["canon"]} for r in rows])
    return {"ok": abs(forward["gain"]) < SCREEN_GAIN_MIN, "gain": forward["gain"], "forward": forward, "reverse": reverse,
            "disagreeing_pairs": sum(int(c != s) for r in rows for c, s in zip(r["canon"], r["shared"])), "n_pairs": len(PTEST) * len(rows)}


def cell1_outcome(fit, twin, screen):
    """§2 cell 1 with §7 A2: UNDERFIT first (nothing is concluded about frames), then NOISE-NON-DISCRIMINATING (rounding
    alone moves the count by a screen-sized gain), then the screen."""
    if not fit["ok"]:
        return "UNDERFIT"
    if not twin["ok"]:
        return "NOISE-NON-DISCRIMINATING"
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


def single_label(shared_n, ref_n, gates_ok):
    """§3 label of ONE process from its counts and its own locality gates."""
    gain = shared_n - ref_n
    lead_sized = shared_n >= LEAD_MIN
    partial_sized = ENV_PARA[1] < shared_n < LEAD_MIN and gain >= PARTIAL_GAIN_MIN   # Codex item 6: inside [5,18] is NULL whatever the gain
    if lead_sized and gates_ok:
        return "LEAD"
    if partial_sized and gates_ok:
        return "PARTIAL"
    if lead_sized or partial_sized:
        return "TRADEOFF"
    return "NULL"


def label(shared_n, ref_n, gates_ok, dw_ratio, second=None):
    """§3 binding label. `second` = (shared_n, ref_n, gates_ok, dw_ratio) of the second process, or None (not yet run).
    A LEAD/PARTIAL carries only if the second process, judged by the SAME gates, is LEAD-sized (>= 30) / PARTIAL-sized
    (> 18 with gain >= 10) with its gates holding; -LARGE-WRITE is added if EITHER process's ratio exceeds 1.5."""
    lab = single_label(shared_n, ref_n, gates_ok)
    if second is not None and lab in ("LEAD", "PARTIAL"):
        s2, r2, g2, _ = second
        lab2 = single_label(s2, r2, g2)
        if lab == "LEAD":
            lab = "LEAD" if lab2 == "LEAD" else "LEAD-NOT-REPLICATED"
        else:
            lab = "PARTIAL" if (lab2 in ("PARTIAL", "LEAD") and s2 > ENV_PARA[1] and s2 - r2 >= PARTIAL_GAIN_MIN) else "PARTIAL-NOT-REPLICATED"
    if dw_ratio > LARGE_WRITE_RATIO or (second is not None and second[3] > LARGE_WRITE_RATIO):
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
    """Pull the pass's A7 reference, its hooked shared edit, the controls, the audit counters, the §7 A1 residual
    readouts and the run identity out of the harness JSON."""
    cand = [k for k in p["recipes"]][0]; rec = p["recipes"][cand]
    a7 = rec["arms"]["A7_coined_coined"]; ex = a7["extra"]
    out = {"rec": rec, "ref": a7, "shared": ex["shared"], "shared_rows": ex["shared_rows"],
            "a1": rec["arms"]["A1_single"], "a2": rec["arms"]["A2_coherent2"],
            "dw_ref": sum(v["delta_norm"] for v in rec["delta_norms"]["A7_coined_coined"].values()),
            "dw_shared": sum(v["delta_norm"] for v in ex["shared_delta_norms"].values()),
            "frames_ref": {n: ex["frame_probe_ref"][n]["flips"] for n in FRAME_NAMES},
            "frames_shared": {n: ex["frame_probe_shared"][n]["flips"] for n in FRAME_NAMES},
            "frame_n": [ex["frame_probe_ref"][n]["n"] for n in FRAME_NAMES] + [ex["frame_probe_shared"][n]["n"] for n in FRAME_NAMES],
            "hits": (ex["override_hits_before"], ex["override_hits_after"], p["z_override_hits_total"]),
            "fit": p["sharedz"]["fit_diagnostic"], "identity": p["identity"],
            "residual": {**{a: rec["arms"][a]["extra"]["residual_ref"]["overall"] for a in PASS_ARMS}, "A7_shared": ex["residual_shared"]["overall"]},
            "key_cosine": {"pre": p["pre_edit"]["key_cosine"], "ref": ex["key_cosine_ref"], "shared": ex["key_cosine_shared"]}}
    if "arm" in p:
        out.update(settings={k: p[k] for k in SETTINGS_KEYS}, engine_solves=p.get("engine_solves", []), per_fact=p["sharedz"]["per_fact"])
    return out


def validity(run, pr, which):
    """§3 validity for one harness pass (which = "1" | "2"); returns the reasons (empty = valid)."""
    reasons = []
    solvefeas = run.get("arm", "sharedz") == "solvefeas"
    if "arm" in run:
        arm = select_arm(run["arm"])
        if run["v_num_grad_steps"] != arm.steps:
            reasons.append("run step count differs from the selected arm")
        for where, record in (("inertness", run["inertness"]), ("inertness identity", run["inertness"]["identity"]),
                              ("run identity", run["identity"]), (f"pass {which}", pr.get("settings", {})),
                              (f"pass {which} identity", pr["identity"])):
            reasons.extend(settings_validity(run, record, where))
        if which == "2":
            reasons.extend(settings_validity(run, run["second_process"], "second process"))
    if solvefeas:
        reasons.extend(solve_budget(pr.get("engine_solves", []), pr.get("per_fact", {}), run)["reasons"])
    fp = run["fingerprint"] if which == "1" else run["second_process"]["fingerprint"]
    if FINGERPRINT not in fp or "PASS" not in fp:
        reasons.append(f"pass {which} fingerprint not {FINGERPRINT}/PASS")
    inert = run["inertness"]
    if not inert["ok"] or any(not inert["checks"].get(c, {}).get("ok") for c in INERTNESS_CHECKS):
        reasons.append("inertness record not all-INERT")
    if inert["identity"]["run_id"] != run["identity"]["inertness_run_id"]:
        reasons.append("inertness record identity differs from the run's")
    if pr["identity"]["run_id"] != run["identity"]["run_id"]:
        reasons.append(f"pass {which} identity {pr['identity']['run_id']} differs from the run's {run['identity']['run_id']}")
    if not pr["rec"]["law5_gate"]["ok"]:
        reasons.append(f"pass {which} LAW#5 harness gate not inert")
    if pr["a1"]["para_full_n"] < CTRL_MIN or pr["a2"]["para_full_n"] < CTRL_MIN:
        reasons.append(f"pass {which} controls A1 {pr['a1']['para_full_n']} A2 {pr['a2']['para_full_n']} < {CTRL_MIN}")
    if not solvefeas and not ENV_PARA[0] <= pr["ref"]["para_full_n"] <= ENV_PARA[1]:
        reasons.append(f"pass {which} reference A7 para {pr['ref']['para_full_n']} outside {ENV_PARA}")
    if not solvefeas and not ENV_CANON[0] <= pr["ref"]["canon_full_n"] <= ENV_CANON[1]:
        reasons.append(f"pass {which} reference A7 canon {pr['ref']['canon_full_n']} outside {ENV_CANON}")
    if tuple(pr["hits"]) != OVERRIDE_HITS:
        reasons.append(f"pass {which} Z_OVERRIDE hits {tuple(pr['hits'])} != {OVERRIDE_HITS}")
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


SECOND_OUTCOMES = ("STARTED", "UNDERFIT", "COMPLETED")   # v3: the driver's permanent second-process record (run.json["second_process"]["outcome"])


def second_process_state(run):
    """v3 (review 2 blocker): the authoritative state of the second process from run.json — "absent" or its outcome."""
    sp = run.get("second_process")
    if sp is None:
        return "absent"
    outcomes = SECOND_OUTCOMES + (("UNDERFIT-AT-50", "REFERENCE-SHIFT", "INVALID") if run.get("arm") == "solvefeas" else ())
    if sp.get("outcome") not in outcomes:
        raise ValueError(f"second_process.outcome {sp.get('outcome')!r} not in {outcomes}")   # [LAW:no-silent-failure]
    return sp["outcome"]


def retry_refusal(run):
    """v3: a `second` invocation may start only when no second process was ever recorded; otherwise the recorded outcome is
    the disposition (§3: "this candidate is not advanced", never "try again in the same run"). Returns None (allowed) or
    the refusal text."""
    state = second_process_state(run)
    if state == "absent":
        return None
    return f"a second process is already recorded for this run with outcome {state}; it is permanent — no retry in the same run (use a new run if a new pre-registration allows it)"


def verdict(run, pr1, pr2=None):
    """The whole §3 judgement from records: validity per process, gates per process, the label. Pure; the selftest
    drives it with synthetic records. v3: with no pass-2 record, run.json's second_process outcome decides — absent ->
    replication pending; UNDERFIT -> terminal NOT-REPLICATED (candidate not advanced); STARTED -> INVALID (incomplete)."""
    state = second_process_state(run)
    out = {"reasons": validity(run, pr1, "1"), "reasons2": [] if pr2 is None else validity(run, pr2, "2"), "second_process": state, "disposition": None}
    if "arm" in run and state != "absent":
        sp = run["second_process"]
        out["reasons2"].extend(settings_validity(run, sp, "second process"))
        out["reasons2"].extend(settings_validity(run, sp.get("identity", {}), "second process identity"))
        if sp.get("identity", {}).get("run_id") != run["identity"]["run_id"]:
            out["reasons2"].append("second process identity differs from the run's")
    out["gates1"] = locality_gates(pr1["ref"], pr1["shared"], pr1["frames_ref"], pr1["frames_shared"]); out["ratio1"] = pr1["dw_shared"] / pr1["dw_ref"]
    second = None
    if pr2 is not None:
        if state not in ("COMPLETED", "REFERENCE-SHIFT"):
            out["reasons2"].append(f"pass2.json present but run.json second_process outcome is {state}, not COMPLETED")
        out["gates2"] = locality_gates(pr2["ref"], pr2["shared"], pr2["frames_ref"], pr2["frames_shared"]); out["ratio2"] = pr2["dw_shared"] / pr2["dw_ref"]
        second = (pr2["shared"]["para_full_n"], pr2["ref"]["para_full_n"], all(out["gates2"].values()), out["ratio2"])
        out["agreement"] = per_fact_agreement(pr1["shared_rows"], pr2["shared_rows"])
    lab = label(pr1["shared"]["para_full_n"], pr1["ref"]["para_full_n"], all(out["gates1"].values()), out["ratio1"], second)
    provisional = pr2 is None and lab.split("-")[0] in ("LEAD", "PARTIAL")
    if provisional and state in ("UNDERFIT", "UNDERFIT-AT-50"):  # terminal: the second solve did not fit; nothing replicated, nothing adopted
        base, rest = lab.split("-", 1)[0], lab[len(lab.split("-", 1)[0]):]
        lab = f"{base}-NOT-REPLICATED{rest}"
        out["disposition"] = "second process UNDERFIT (§2 fit diagnostic): candidate not advanced; the provisional pass-1 label does not carry"
    elif provisional and state in ("STARTED", "COMPLETED"):      # a second process began (or claims completion) but left no pass-2 record
        out["reasons2"].append(f"second process incomplete (outcome {state}, no pass2.json) — INVALID (second process)")
    out["label"] = lab
    out["replication_pending"] = provisional and state == "absent"
    if run.get("arm") == "solvefeas":
        out["solvefeas1"] = solvefeas_reading(pr1["per_fact"])
        if pr2 is not None:
            out["solvefeas2"] = solvefeas_reading(pr2["per_fact"])
        if state == "INVALID":
            out["reasons2"].append("second process INVALID; the larger budget was not exercised")
        if state == "REFERENCE-SHIFT" and pr2 is None:
            out["reasons2"].append("REFERENCE-SHIFT second process has no pass2.json")
        if out["reasons"] or out["reasons2"]:
            out["label"], out["replication_pending"] = "INVALID", False
        elif reference_shift(pr1["ref"]) or (pr2 is not None and reference_shift(pr2["ref"])):
            out["label"], out["replication_pending"] = "REFERENCE-SHIFT", False
            out["disposition"] = "HALT the arm; the budget shifted the canonical reference outside its baseline envelope"
    return out


def print_pass(name, pr):
    x, y = pr["ref"], pr["shared"]; ax, ay = x["locality_axes"], y["locality_axes"]
    print(f"\n{'pass ' + name:22} canon/24 para/72 first string | A1 A2 | L1/12 frame CANON/T1/T2 described_as L3/30 ppl | dW | residual ratio")
    for lab, a, ax_, fr, dw, res in (("reference (engine z)", x, ax, pr["frames_ref"], pr["dw_ref"], pr["residual"]["A7_coined_coined"]),
                                     ("shared z", y, ay, pr["frames_shared"], pr["dw_shared"], pr["residual"]["A7_shared"])):
        print(f"{lab:22} {a['canon_full_n']:>3}     {a['para_full_n']:>3}    {a['para_first_n']:>3}   {a['para_string_n']:>3}   | {pr['a1']['para_full_n']:>2} {pr['a2']['para_full_n']:>2} | "
              f"{ax_['L1_flipped_to_edited_value']:>2}    {fr['CANON']}/{fr['T1']}/{fr['T2']}          {a['locality_described_as']:>5}     {ax_['L3_top1_agree']:>2}  {ax_['generic_ppl_post']:.2f} | {dw:.1f} | {res:.4f}")
    per_t = {t: sum(r["para_full_hits"][k] for r in pr["shared_rows"]) for k, t in enumerate(PTEST)}
    print(f"shared per held-out template: {per_t} (comparator P6 15/17/17); §7 A1 remaining-residual ratio per arm (readout only): "
          + ", ".join(f"{a} {pr['residual'][a]:.4f}" for a in PASS_ARMS) + f", A7_shared {pr['residual']['A7_shared']:.4f}")
    for layer, v in pr["key_cosine"]["shared"].items():
        print(f"key cosine to CANON, layer {layer}: " + "; ".join(f"{t}: pre {pr['key_cosine']['pre'][layer][t]['mean_cos']:.3f} ref {pr['key_cosine']['ref'][layer][t]['mean_cos']:.3f} shared {v[t]['mean_cos']:.3f}" for t in v))


def print_solvefeas(reading):
    print(f"solve feasibility: {reading['label']}; evaluation-25 minimum {reading['fit_at25']['min_fit']:.6f}; final minimum {reading['fit_at_stop']['min_fit']:.6f}")
    for entry in reading["underfit"]:
        print(f"  {entry['subj']} {entry['frame']}: evaluation-25 fit {entry['fit_at25']:.6f}; final fit {entry['fit']:.6f}; {entry['class']}")
    for cls, text in reading["qualifications"].items():
        print(f"  {cls}: {text}")
    if reading["label"] == "UNDERFIT-AT-50":
        print("  next: step 2; the frame hypothesis remains open")


def main():
    d = sys.argv[1]
    run = load(d, "run.json"); inj = load(d, "inject.json")
    sc, fit = inj["screen"], inj["fit_diagnostic"]
    print(f"run {run['identity']['run_id']}; cell 1 injection (unedited model, {inj['n_subjects']} facts): canonical {sc['canon_n']}/72 shared {sc['shared_n']}/72 gain {sc['gain']} "
          f"(screen >= {SCREEN_GAIN_MIN}); net wins by template {sc['net_by_template']}; templates won {sc['templates_won']} (>= {SCREEN_MIN_TEMPLATES}), "
          f"subjects won {sc['subjects_won']} (>= {SCREEN_MIN_SUBJECTS}); canon-template injection canonical {inj['canon_template_inj']['canonical']}/24 shared {inj['canon_template_inj']['shared']}/24")
    print(f"fit diagnostic (>= {FIT_MIN} per fact per frame): min {fit['min_fit']:.4f}; underfit {fit['underfit'] or 'none'}; "
          f"clamp hits {inj['clamp_hits']}/{inj['n_subjects']}; mean steps {inj['mean_steps']}")
    cc = inj["control_c"]
    print("control c (full-sequence greedy, per frame; canonical delta = reconstructed (z_engine - target_init), shared = saved optimizer delta): "
          + "; ".join(f"{t}: additive {cc[t]['additive']} absolute {cc[t]['absolute']}" for t in cc))
    tw = inj["noise_twin"]
    print(f"noise twin (§7 A2: canonical objective at the shared batch shape, this process's templates): gain {tw['gain']} "
          f"(admissible iff |gain| < {SCREEN_GAIN_MIN}); {tw['disagreeing_pairs']}/{tw['n_pairs']} pairs disagree (observed null discordance)")
    outcome = run["cell1_outcome"]
    if run.get("arm") == "solvefeas":
        diags = {r["subj"]: r["shared_solve"] for r in inj["rows"]}
        budget = solve_budget(inj["engine_solves"], diags, run)
        reasons = injection_validity(run, inj, diags)
        if reasons:
            print("\nINVALID —", "; ".join(reasons)); sys.exit(2)
        reading = solvefeas_reading(diags)
        print_solvefeas(reading)
        snap = inj["evaluation_25_injection"]
        print(f"evaluation-25 shared-z injection (record only): {snap['shared_n']}/72; final canonical/shared/twin {sc['canon_n']}/{sc['shared_n']}/{sc['canon_n'] + tw['gain']}/72; "
              "CORPUS/51 canonical/shared/twin 51/69/54/72 (results/c10s_sharedz_r2/inject.json; different template draw)")
        print(f"50-step positive control: {budget['positive_control']}")
        outcome = solvefeas_cell1_outcome(reading, tw, sc, budget)
    if outcome != "PROCEED":
        print(f"\ncell 1 outcome: {outcome} -> this candidate configuration was not advanced; the write arm was not run (§2)"); return
    p1 = load(d, "pass1.json")
    if p1 is None:
        print("missing pass1.json (cell 1 passed; the harness pass has not run)"); sys.exit(3)
    pr1 = read_pass(p1); p2 = load(d, "pass2.json", required=False); pr2 = None if p2 is None else read_pass(p2)
    v = verdict(run, pr1, pr2)
    print_pass("1", pr1)
    if "solvefeas1" in v:
        print_solvefeas(v["solvefeas1"])
    if pr2 is not None:
        print_pass("2", pr2)
        if "solvefeas2" in v:
            print_solvefeas(v["solvefeas2"])
    if v["reasons"]:
        print("\nINVALID —", "; ".join(v["reasons"])); sys.exit(2)
    if v["reasons2"]:
        print("\nINVALID (second process) —", "; ".join(v["reasons2"])); sys.exit(2)
    x, y = pr1["ref"], pr1["shared"]
    print(f"\nlocality gates pass 1 (shared vs reference): {v['gates1']}; dW ratio {v['ratio1']:.2f}")
    if pr2 is not None:
        print(f"locality gates pass 2: {v['gates2']}; dW ratio {v['ratio2']:.2f}; per-fact agreement {v['agreement']}")
    print(f"binding: shared para_full {y['para_full_n']}/72 vs reference {x['para_full_n']} (gain {y['para_full_n'] - x['para_full_n']}); "
          f"LEAD >= {LEAD_MIN}; PARTIAL > {ENV_PARA[1]} with gain >= {PARTIAL_GAIN_MIN}; -LARGE-WRITE above {LARGE_WRITE_RATIO} in either process; "
          f"second process {v['second_process']} -> {v['label']}")
    if v["disposition"]:
        print(f"disposition: {v['disposition']}")
    if run.get("arm") == "solvefeas" and v["second_process"] == "UNDERFIT-AT-50":
        print_solvefeas(solvefeas_reading(run["second_process"]["per_fact"]))
    if v["replication_pending"]:
        print("second process required (gate A): the label does not carry until replicated")


if __name__ == "__main__":
    main()
