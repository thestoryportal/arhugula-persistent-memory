#!/usr/bin/env python3
"""D-C10t-secondkey v2 frozen §2/§3: pure selection, gates and labels.

No engine, torch or model imports. Usage: c10t_secondkey_read.py OUT_DIR.
All spending, admission-disposition, locality and replication rules live here.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import hashlib, json, math, re, statistics
from pathlib import Path

DECISION_ID = "D-C10t-secondkey"
PREREG = "docs/C10T_SECONDKEY_PREREG.md"
HP_FILE = "configs/hparams/qwen25_3b_memit_hparams.json"
CANON = "The capital of {} is the city of"                 # c10e_bandknob.py:51-56
PTEST = ["{}'s capital city is called", "If you visit {}, its capital city is",
         "The main city and seat of government of {} is"]
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]  # c10p_twopass_arms.py:30
BAND = [4, 5, 6, 7, 8]
N, NT, FRAME_N = 24, 3, 6
COV_CUT, CUT_CHECK = 0.005, 0.05                       # §2(b), c10e_bandknob.py:28,173-175
DROP_MAX, MERGE_MIN = 12, 20
FINGERPRINT, COV_CPU = "d941a9fb", 3
CTRL_MIN, ENV_PARA, ENV_CANON = 68, (5, 18), (5, 10)
LEAD_MIN, PARTIAL_GAIN_MIN = 30, 10
L1_SLACK, F0_SLACK, F1_SLACK, DESC_SLACK, PPL_SLACK = 1, 1, 1, 3, 0.5
L3_MIN, LARGE_WRITE, SUBJECT_FREE_SLACK = 29, 1.5, 1
LAW5_EXPR, LAW5_LOC = 0.05, 3
ENGINE_LOSS_STOP, ENGINE_STEPS = 0.05, 25             # compute_z.py:164, hparams:6
BASE_LEAK_MAX = 0.15                                # standing harness stimulus halt, c10e_bandknob.py:569
KEY_COS_COMPARATOR = 0.9                            # keygram.stats, c10k_keying_ablation_keygram.py:17
SINGLE, DUP = "A7-single", "A7-dup"


def json_digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def argmax_first(values):
    if not values or any(not math.isfinite(x) for x in values):
        raise ValueError("argmax needs a nonempty finite score vector")
    return max(range(len(values)), key=lambda i: values[i])


def surprisal_selection(values):
    """§2(a): j* is a boundary; its address is j*-1, so j*=1 addresses the frame.
    The internal selector maximises s[j+1], not s[j]. Ties choose smaller j.
    """
    if len(values) < 2:
        raise ValueError("a second key needs a nonempty remainder")
    star = argmax_first(values) + 1
    return {"j_star": star, "unconstrained_address_j": star - 1,
            "unconstrained_writable": star > 1, "p10": argmax_first(values[1:]) + 1}


def cut_indices(singular_values, cut=COV_CUT):
    return [i for i, s in enumerate(singular_values) if s >= cut]


def leverage_selection(positions, scores_by_layer):
    """§2(b), §7(3,8): selector = raw five-layer arithmetic mean. The separately
    reported alternative divides each layer by its maximum over the full sentence.
    No tiny singular value is inverted. Runtime supplies k^T Sigma+ k per position.
    """
    if set(scores_by_layer) != {str(l) for l in BAND}:
        raise ValueError("leverage requires exactly layers 4..8")
    vectors = [scores_by_layer[str(l)] for l in BAND]
    if any(len(v) != len(positions) for v in vectors):
        raise ValueError("position/score lengths differ")
    for v in vectors:
        argmax_first(v)
    raw = [statistics.mean(v[i] for v in vectors) for i in range(len(positions))]
    normal = [statistics.mean(v[i] / max(v) if max(v) > 0 else 0.0 for v in vectors)
              for i in range(len(positions))]
    internal = [i for i, p in enumerate(positions) if p["class"] == "value-writable"]
    if not internal:
        raise ValueError("no writable value positions")
    pick = lambda v: internal[argmax_first([v[i] for i in internal])]
    winner = argmax_first(raw)
    per_layer = {}
    for l, v in zip(BAND, vectors):
        ranked = sorted(range(len(v)), key=lambda i: (-v[i], i))
        per_layer[str(l)] = {"winner": positions[ranked[0]], "score": v[ranked[0]],
                             "margin": v[ranked[0]] - v[ranked[1]],
                             "internal_j": positions[pick(v)]["j"]}
    return {"unconstrained": positions[winner], "unconstrained_writable": positions[winner]["class"] == "value-writable",
            "p5": positions[pick(raw)]["j"], "mean_scores": raw, "per_layer": per_layer,
            "normalised_mean_scores": normal, "normalised_winner": positions[argmax_first(normal)],
            "normalised_internal_j": positions[pick(normal)]["j"], "selector": "raw-five-layer-mean"}


def nearest_admissible(pick, admitted):
    if not admitted:
        raise ValueError("INVALID-ADMISSION: empty admissible set")
    return min(admitted, key=lambda j: (abs(j - pick), j))


def select_positions(facts):
    """§2(c): screens are spending decisions; never remove a fact. Merge uses
    PRE-admission agreement and p10 on disagreements. A dropped rule is not revived.
    """
    if len(facts) != N or len({f["subj"] for f in facts}) != N:
        raise ValueError("selection requires exactly 24 distinct facts in FICTION order")
    dropped = {rule: sum(not f[rule]["unconstrained_writable"] for f in facts) > DROP_MAX
               for rule in ("surprisal", "leverage")}
    pre = sum(f["surprisal"]["p10"] == f["leverage"]["p5"] for f in facts)
    empty = [f["subj"] for f in facts if not f["admissible"]]
    # Empty admission has precedence even if both spending rules would be dropped.
    if empty:
        return {"outcome": "INVALID-ADMISSION", "empty": empty, "dropped": dropped,
                "agreement_before": pre, "agreement_after": None, "arms": {}}
    mapped10 = [nearest_admissible(f["surprisal"]["p10"], f["admissible"]) for f in facts]
    mapped5 = [nearest_admissible(f["leverage"]["p5"], f["admissible"]) for f in facts]
    post = sum(a == b for a, b in zip(mapped10, mapped5))
    arms = {}
    if not any(dropped.values()) and pre >= MERGE_MIN:
        arms["B"] = mapped10
    else:
        if not dropped["surprisal"]:
            arms["B10"] = mapped10
        if not dropped["leverage"]:
            arms["B5"] = mapped5
    return {"outcome": "READY" if arms else "BOTH-RULES-DROPPED", "dropped": dropped,
            "nonwritable_counts": {r: sum(not f[r]["unconstrained_writable"] for f in facts) for r in dropped},
            "agreement_before": pre, "agreement_after": post, "admission_mapped": {"p10": mapped10, "p5": mapped5},
            "arms": {"A7-second-" + k: dict(zip([f["subj"] for f in facts], v)) for k, v in arms.items()}}


def overlap_audit(requests):
    """§2(e): report normalised word overlap, including shared contiguous trigrams.
    There is no overlap stop in this prereg; values are not tuned to this table.
    """
    words = lambda s: re.findall(r"[a-z0-9']+", s.lower().replace("{}", " "))
    grams = lambda w: {tuple(w[i:i + 3]) for i in range(max(0, len(w) - 2))}
    rows = []
    for rq in requests[N:]:
        a = words(rq["subject"])
        for p in PTEST:
            b = words(p)
            rows.append({"subject": rq["subject"], "held_out": p, "shared_words": sorted(set(a) & set(b)),
                         "shared_trigrams": [" ".join(g) for g in sorted(grams(a) & grams(b))],
                         "jaccard_words": len(set(a) & set(b)) / len(set(a) | set(b))})
    return rows


def overturning_reading(second, subject):
    if not second or len(second) != len(subject):
        raise ValueError("cross-template cosine vectors must be paired and nonempty")
    if any(not math.isfinite(x) for x in second + subject):
        raise ValueError("cross-template cosine is undefined/nonfinite")
    a, b = statistics.median(second), statistics.median(subject)
    return {"second_median": a, "subject_median": b, "H_T4_standing": a <= b, "stop": False}


def new_hits(post, base):
    if len(post) != FRAME_N or len(base) != FRAME_N:
        raise ValueError("F1 requires the same six never-edited subjects")
    return sum(p and not b for p, b in zip(post, base))


def locality_gates(reference, candidate, base, variant):
    r, c = reference["locality_axes"], candidate["locality_axes"]
    rx, cx = reference["extra"], candidate["extra"]
    gates = {"L1": c["L1_flipped_to_edited_value"] <= r["L1_flipped_to_edited_value"] + L1_SLACK,
             "F0": cx["F0"]["flips"] <= rx["F0"]["flips"] + F0_SLACK,
             "described_as": candidate["locality_described_as"] >= reference["locality_described_as"] - DESC_SLACK,
             "L3": c["L3_top1_agree"] >= L3_MIN,
             "generic_ppl": c["generic_ppl_post"] <= r["generic_ppl_post"] + PPL_SLACK}
    for b, rp, cp in zip(base["prefixes"][variant], rx["prefixes"][variant], cx["prefixes"][variant]):
        gates["F1:" + b["subj"]] = new_hits(cp["next_hits"], b["next_hits"]) <= new_hits(rp["next_hits"], b["next_hits"]) + F1_SLACK
    return gates


def single_label(count, reference, gates_ok):
    sized = count >= LEAD_MIN or (ENV_PARA[1] < count < LEAD_MIN and count - reference >= PARTIAL_GAIN_MIN)
    if sized and not gates_ok:
        return "TRADEOFF"
    if count >= LEAD_MIN:
        return "LEAD"
    return "PARTIAL" if sized else "NULL"


def write_ratio(reference, candidate):
    return candidate / reference if reference > 0 else None


def qualifiers(reference, candidate, duplicate, ratio, variant):
    out = []
    if ratio is not None and ratio > LARGE_WRITE:
        out.append("LARGE-WRITE")
    total = lambda a: sum(r["full_hit"] for r in a["extra"]["subject_free"][variant])
    if total(candidate) > total(reference) + SUBJECT_FREE_SLACK:
        out.append("SUBJECT-FREE")
    if duplicate["para_full_n"] > ENV_PARA[1] and duplicate["para_full_n"] - reference["para_full_n"] >= PARTIAL_GAIN_MIN:
        out.append("REQUEST-COUNT")
    return out


def count_readout(rows):
    return {"per_template": [sum(r["para_full_hits"][t] for r in rows) for t in range(NT)],
            "per_fact": [sum(r["para_full_hits"]) for r in rows],
            "per_edge_all_three": sum(all(r["para_full_hits"]) for r in rows),
            "per_edge": [all(r["para_full_hits"]) for r in rows], "rows": rows}


def identity_matches(a, b):
    return all(a.get(k) == b.get(k) and k in a and k in b
               for k in ("run_id", "source_sha256", "source_digest"))


def step0_validity(step):
    reasons = []
    try:
        facts = step["facts"]
        selection = select_positions(facts)
        if step["selection"] != selection:
            reasons.append("published selection differs from frozen rules")
        for f in facts:
            if f["admissible_n"] != len(f["admissible"]) or any(type(j) is not int or not 1 <= j < len(f["value_ids"]) for j in f["admissible"]):
                reasons.append("inadmissible published position: " + f["subj"])
            if any(f["surprisal"][k] != v for k, v in surprisal_selection(f["surprisal"]["values"]).items()):
                reasons.append("surprisal selector differs from published scores")
            scores = {str(l): f["leverage_layers"][str(l)]["protected_leverage"][str(COV_CUT)] for l in BAND}
            if f["leverage"] != leverage_selection(f["positions"], scores):
                reasons.append("leverage selector differs from published scores")
        if set(step["requests"]) != set(selection["arms"]) or set(step["overlap"]) != set(selection["arms"]) or set(step["overturning"]) != set(selection["arms"]):
            reasons.append("published request/overlap arms differ")
        canonical = [{"prompt": CANON, "subject": f["subj"], "target_new": {"str": " " + f["value"]}} for f in facts]
        for v, js in selection["arms"].items():
            second = []
            for f in facts:
                audit = next(a for a in f["admission"] if a["j"] == js[f["subj"]])
                if not audit["ok"]:
                    reasons.append("chosen position did not pass step0 admission")
                second.append(audit["request"])
            if step["requests"][v] != canonical + second or step["request_sha256"][v] != json_digest(step["requests"][v]):
                reasons.append("published blocked requests/digest differ: " + v)
            if step["overlap"][v] != overlap_audit(step["requests"][v]):
                reasons.append("normalised overlap audit missing or changed")
            cross = step["overturning"][v]
            paired_second, paired_subject = [], []
            if set(cross["layers"]) != {str(l) for l in BAND}:
                reasons.append("cross-template layer population differs")
            for rows in cross["layers"].values():
                if set(rows) != {"PTEST" + str(t) for t in range(NT)}:
                    reasons.append("cross-template template population differs")
                for row in rows.values():
                    if row["facts"] != [f["subj"] for f in facts] or len(row["second"]) != N or len(row["subject"]) != N:
                        reasons.append("cross-template fact population differs")
                    paired_second.extend(row["second"])
                    paired_subject.extend(row["subject"])
            if cross["reading"] != overturning_reading(paired_second, paired_subject):
                reasons.append("H-T4 standing reading differs from recorded cosines")
    except (KeyError, TypeError, ValueError, IndexError, StopIteration) as e:
        reasons.append("incomplete/malformed step0: " + repr(e))
    return reasons


def validity(run, record):
    """§3 INVALID takes precedence, including across replication processes.
    Missing or malformed readouts fail closed, rather than becoming empty gates.
    """
    reasons = []
    try:
        step = run["step0"]
        reasons.extend(step0_validity(step))
        variants = step["selection"]["arms"]
        recipe = record["recipe"]
        arms, details = recipe["arms"], recipe["detail"]
        if not identity_matches(run["identity"], record["identity"]) or not identity_matches(run["identity"], step["identity"]):
            reasons.append("run/step0/pass identities differ")
        if record["positions_sha256"] != run["positions_sha256"] or not re.fullmatch(r"[0-9a-f]{64}", run["positions_sha256"]):
            reasons.append("positions-file hash missing or mismatched")
        if record["fingerprint"]["sha256"][:8] != FINGERPRINT or record["fingerprint"]["_cov_cpu"] != COV_CPU or not record["fingerprint"]["ok"]:
            reasons.append("fingerprint/_cov_cpu gate failed")
        law = recipe["law5_gate"]
        if not law["ok"] or not law["expr_delta"] < LAW5_EXPR or not law["loc_delta"] < LAW5_LOC:
            reasons.append("LAW#5 not INERT")
        if recipe["band"] != BAND or recipe["projector"] != "nullspace":
            reasons.append("band/projector changed")
        expected = {"A1_single", "A2_coherent2", SINGLE, DUP, *variants}
        if set(arms) != expected or set(details) != expected:
            reasons.append("harness arm population differs")
        if any(arms[a]["para_full_n"] < CTRL_MIN for a in ("A1_single", "A2_coherent2")):
            reasons.append("A1/A2 controls below 68/72")
        ref = arms[SINGLE]
        if not ENV_PARA[0] <= ref["para_full_n"] <= ENV_PARA[1] or not ENV_CANON[0] <= ref["canon_full_n"] <= ENV_CANON[1]:
            reasons.append("A7-single outside the historical envelope")
        if record["admission"]["ok"] is not True or set(record["admission"]["arms"]) != set(variants) or any(
                not a["ok"] or a["n_requests"] != 2 * N for a in record["admission"]["arms"].values()):
            reasons.append("process alignment admission failed")
        audit = record["wrapper"]
        if audit["candidate_substitutions"] != len(variants) or audit["duplicate_substitutions"] != 1 or audit["law5_substitutions"] != 0:
            reasons.append("wrapper substitution counts differ")
        if not audit["z_override_none"] or audit["z_override_hits"] != 0 or audit["order"] != [SINGLE, DUP, *variants]:
            reasons.append("Z_OVERRIDE or wrapper order differs")
        if step["selection"] != select_positions(step["facts"]) or step["selection"]["outcome"] != "READY":
            reasons.append("published selection differs from frozen rules")
        if step["overlap"] != {v: overlap_audit(rqs) for v, rqs in step["requests"].items()}:
            reasons.append("normalised overlap audit missing or changed")
        subjects = [f["subj"] for f in step["facts"]]
        canonical = next(iter(step["requests"].values()))[:N]
        actual_requests = {SINGLE: canonical, DUP: canonical + canonical, **step["requests"]}
        for a in expected:
            rows = details[a]
            if len(rows) != N or [r["subj"] for r in rows] != subjects or any(
                    len(r[k]) != NT or any(type(b) is not bool for b in r[k])
                    for r in rows for k in ("para_full_hits", "para_first_hits", "para_string_hits")):
                reasons.append(a + " held-out population malformed")
                continue
            x = arms[a]
            if x["canon_n"] != N or x["para_n"] != N * NT or x["para_full_n"] != sum(sum(r["para_full_hits"]) for r in rows) or x["canon_full_n"] != sum(r["canon_full"] for r in rows):
                reasons.append(a + " aggregate counts differ from rows")
            if a not in ("A1_single", "A2_coherent2"):
                if x["para_string_n"] != x["para_full_n"] or x["para_string_n"] != sum(sum(r["para_string_hits"]) for r in rows):
                    reasons.append(a + " string/full counts differ")
                ex = x["extra"]
                if ex["F0"]["n"] != FRAME_N or len(ex["fits"]) != (N if a == SINGLE else 2 * N):
                    reasons.append(a + " F0/fit population differs")
                if ex["requests_sha256"] != audit["requests_sha256"][a] or ex["hook_request_count"] != (N if a == SINGLE else 2 * N):
                    reasons.append(a + " requests did not reach hooks")
                if ex["requests_sha256"] != json_digest(actual_requests[a]) or audit["reached_my_edit_counts"][a] != len(actual_requests[a]) or [f["request"] for f in ex["fits"]] != actual_requests[a]:
                    reasons.append(a + " actual request/fit payload differs from publication")
                if any(not 1 <= f["loss_evaluations"] <= ENGINE_STEPS or not math.isfinite(f["nll"]) or not math.isfinite(f["kl_loss"]) for f in ex["fits"]):
                    reasons.append(a + " fit telemetry malformed")
                for v in variants:
                    for probe in (record["base_probes"], ex):
                        if [r["subj"] for r in probe["prefixes"][v]] != subjects or [r["subj"] for r in probe["subject_free"][v]] != subjects:
                            reasons.append(a + " prefix-probe population differs")
                        if any(len(r["next_hits"]) != FRAME_N or len(r["full_hits"]) != FRAME_N for r in probe["prefixes"][v]):
                            reasons.append(a + " F1 prompt population differs")
                if set(ex["keygram_solve"]) != {str(l) for l in BAND} or "residual" not in ex or "prefix_reached" not in ex or "bystanders" not in ex:
                    reasons.append(a + " required diagnostics missing")
                if any(g["n_columns"] != len(actual_requests[a]) for g in ex["keygram_solve"].values()):
                    reasons.append(a + " solve key population differs")
                for v in variants:
                    reached = ex["prefix_reached"][v]
                    if reached["n"] != N * NT or [r["subj"] for r in reached["rows"]] != subjects or reached["per_fact"] != [sum(r["hits"]) for r in reached["rows"]] or reached["count"] != sum(reached["per_fact"]):
                        reasons.append(a + " natural-prefix population/count differs")
                if len(ex["residual"]["canonical_keyed_positions"]["per_request"]) != len(actual_requests[a]) or len(ex["residual"]["held_out_keyed_positions"]["per_request"]) != NT * len(actual_requests[a]):
                    reasons.append(a + " residual population differs")
                if sum(d["delta_norm"] for d in recipe["delta_norms"][SINGLE].values()) <= 0:
                    reasons.append("zero reference write norm")
        if any(v["base"] > N * BASE_LEAK_MAX for v in record["base_report"].values()):
            reasons.append("standing harness stimulus leak halt")
    except (KeyError, TypeError, ValueError, IndexError, StopIteration) as e:
        reasons.append("incomplete/malformed record: " + repr(e))
    return reasons


def pass_reading(record, variant):
    recipe = record["recipe"]
    arms = recipe["arms"]
    ref, cand, dup = arms[SINGLE], arms[variant], arms[DUP]
    gates = locality_gates(ref, cand, record["base_probes"], variant)
    norm = lambda a: sum(r["delta_norm"] for r in recipe["delta_norms"][a].values())
    ratio = write_ratio(norm(SINGLE), norm(variant))
    prefix_bleed = {}
    for b, r, c in zip(record["base_probes"]["prefixes"][variant], ref["extra"]["prefixes"][variant], cand["extra"]["prefixes"][variant]):
        prefix_bleed[b["subj"]] = {"reference_new_next": new_hits(r["next_hits"], b["next_hits"]),
                                  "candidate_new_next": new_hits(c["next_hits"], b["next_hits"]),
                                  "reference_new_full": new_hits(r["full_hits"], b["full_hits"]),
                                  "candidate_new_full": new_hits(c["full_hits"], b["full_hits"])}
    return {"label": single_label(cand["para_full_n"], ref["para_full_n"], all(gates.values())),
            "gates": gates, "count": cand["para_full_n"], "reference": ref["para_full_n"],
            "gain": cand["para_full_n"] - ref["para_full_n"], "write_ratio": ratio,
            "F1_new_hits": prefix_bleed,
            "subject_free_full_hits": {"reference": sum(r["full_hit"] for r in ref["extra"]["subject_free"][variant]),
                                       "candidate": sum(r["full_hit"] for r in cand["extra"]["subject_free"][variant])},
            "qualifiers": qualifiers(ref, cand, dup, ratio, variant),
            "binding": count_readout(recipe["detail"][variant]),
            "decomposition": {k: cand[k] for k in ("canon_full_n", "para_first_n", "para_string_n", "tf_pertok_cont", "cond_full_given_first")},
            "prefix_reached": cand["extra"]["prefix_reached"][variant]}


def verdict(run, pass1=None, pass2=None, second_started=None, second_halt=None):
    """§3: per-arm labels; validity in BOTH processes precedes NOT-REPLICATED.
    Exclusive second_started.json prevents retries and makes incomplete attempts visible.
    """
    problems = step0_validity(run["step0"])
    if problems:
        return {"label": "INVALID", "reasons": problems, "arms": {}, "replication_pending": False}
    selection = run["step0"]["selection"]
    if selection["outcome"] != "READY":
        return {"label": selection["outcome"], "arms": {}, "replication_pending": False}
    reasons = ["pass1 missing"] if pass1 is None else validity(run, pass1)
    if reasons:
        return {"label": "INVALID", "reasons": reasons, "arms": {}, "replication_pending": False}
    if pass2 is not None:
        reasons += ["pass2: " + r for r in validity(run, pass2)]
        if second_started is None:
            reasons.append("pass2 without a recorded fresh-process start")
        elif second_started["pid"] == pass1["pid"]:
            reasons.append("replication did not use a fresh process")
        elif pass2["pid"] != second_started["pid"]:
            reasons.append("pass2 PID differs from recorded fresh-process start")
    if second_started is not None:
        if not identity_matches(run["identity"], second_started["identity"]):
            reasons.append("second-start identity differs")
        if pass2 is None:
            reasons.append("second process HALTED" if second_halt else "second process incomplete")
    if second_halt is not None:
        reasons.append("second process has a terminal HALT record")
    if reasons:
        return {"label": "INVALID", "reasons": reasons, "arms": {}, "replication_pending": False}
    out = {"arms": {}, "reasons": [], "replication_pending": False,
           "step0_reading": {"agreement_before": selection["agreement_before"], "agreement_after": selection["agreement_after"],
                             "dropped": selection["dropped"], "overturning": run["step0"]["overturning"]}}
    for variant in selection["arms"]:
        a = pass_reading(pass1, variant)
        b = None if pass2 is None else pass_reading(pass2, variant)
        label = a["label"]
        pending = label in ("LEAD", "PARTIAL") and b is None
        if b is not None and label in ("LEAD", "PARTIAL"):
            replicated = b["label"] == "LEAD" if label == "LEAD" else (b["label"] in ("LEAD", "PARTIAL") and b["gain"] >= PARTIAL_GAIN_MIN)
            if not replicated:
                label += "-NOT-REPLICATED"
        qs = [q for q in ("LARGE-WRITE", "SUBJECT-FREE", "REQUEST-COUNT") if q in a["qualifiers"] or (b is not None and q in b["qualifiers"])]
        rows1 = pass1["recipe"]["detail"][variant]
        agreement = None if b is None else {"facts_with_identical_hits": sum(x["para_full_hits"] == y["para_full_hits"] for x, y in zip(rows1, pass2["recipe"]["detail"][variant])), "n": N}
        out["arms"][variant] = {"label": label + "".join("-" + q for q in qs), "pass1": a, "pass2": b,
                                "agreement": agreement, "replication_pending": pending,
                                "H_T1_label_eligible": label in ("LEAD", "PARTIAL") and not pending and not set(qs) & {"SUBJECT-FREE", "REQUEST-COUNT"},
                                "reading": "configuration improvement only" if "REQUEST-COUNT" in qs else "prefix reached and H-T2/H-T4 must be read beside the label"}
        out["replication_pending"] |= pending
    return out


def main():
    d = Path(sys.argv[1])
    load = lambda name: json.loads((d / name).read_text()) if (d / name).exists() else None
    run = load("run.json")
    if run is None:
        step = load("step0.json")
        if step is None:
            raise SystemExit("missing run.json and step0.json")
        print(json.dumps({"selection": step["selection"], "overturning": step.get("overturning")}, indent=2))
        return 2 if step["selection"]["outcome"] == "INVALID-ADMISSION" else 0
    positions = Path(run["positions_file"])
    if not positions.exists() or hashlib.sha256(positions.read_bytes()).hexdigest() != run["positions_sha256"]:
        print("INVALID: published positions file is missing or its hash changed")
        return 2
    v = verdict(run, load("pass1.json"), load("pass2.json"), load("second_started.json"), load("second_halt.json"))
    print(json.dumps(v, indent=2, allow_nan=False))
    return 2 if v.get("label") in ("INVALID", "INVALID-ADMISSION") else 0


if __name__ == "__main__":
    sys.exit(main())
