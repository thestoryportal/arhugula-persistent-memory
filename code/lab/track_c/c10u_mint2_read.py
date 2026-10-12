#!/usr/bin/env python3
"""D-C10u-mint2 v3 frozen §2/§3: pure admission, spending and readings.

No engine, tokenizer, torch or model imports. Usage: c10u_mint2_read.py OUT_DIR.
Binding is raw full-sequence correctness minus whole-sequence step-0 recall.
Blocks F and V2 retain separate references, seeds, contexts and direction labels.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import hashlib, json, math, re, statistics
from pathlib import Path

DECISION_ID = "D-C10u-mint2"
PREREG = "docs/C10U_MINT2_PREREG.md"
WORDLIST = "results/c10u_mint2/v2_wordlist.json"
HEADS_SHA256 = "7d83a89f3f893d615ded1ff9c1985eba0ae66063760a61886201a27b2a906c8f"
MODIFIERS_SHA256 = "402144a2f237a50c5c7ed730d9475badf4fc2380051977492bee6677c681ba93"
N, NT, SEEDS = 24, 3, (0, 1, 2)
FIT_MIN, ADMISSION_MIN, CONTROL_MIN = 0.98, 22, 68
LEAD_MIN, GAIN_MIN, L3_MIN, LARGE_WRITE = 30, 10, 29, 1.5
BASELINE_WINDOW = {"para_full_n": (5, 18), "canon_full_n": (5, 10), "para_first_n": (42, 59)}
NULL_BAND = (11, 18)
REPRODUCTION = {0: (32, 56), 1: (24, 44), 2: (26, 46)}
LAW5_EXPR, LAW5_LOC = 0.05, 3.0
INERTNESS_TOL = 1e-5  # implementation parity gate; prereg supplies no numerical tolerance
KINDS = {"F": ("multi", "mint1", "modifier"), "V2": ("multi", "mint1", "mint2", "mint1_48")}


def json_digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _finite(x):
    return type(x) in (int, float) and math.isfinite(x)


def _count(x, low=0, high=N * NT):
    return type(x) is int and low <= x <= high


def _hash(x):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{64}", x) is not None


def _probabilities(xs):
    return isinstance(xs, list) and bool(xs) and all(_finite(x) and 0 <= x <= 1 for x in xs)


def _hits(xs):
    return isinstance(xs, list) and len(xs) == NT and all(type(x) is bool for x in xs)


def inertness_reading(override_rel, context_rel, expr_delta):
    values = (override_rel, context_rel, expr_delta)
    return {"override_rel": override_rel, "context_rel": context_rel, "expr_delta": expr_delta,
            "ok": all(_finite(x) and 0 <= x <= INERTNESS_TOL for x in values)}


def law3_reference_reading(scores):
    gates = {name: _count(scores.get(name)) and scores[name] >= CONTROL_MIN
             for name in ("A1_single", "A2_coherent2")}
    return {"ok": all(gates.values()), "gates": gates, "scores": scores}


def i11_reading(inventory, recall_rows):
    _require(isinstance(inventory, list) and len({r["id"] for r in inventory}) == len(inventory), "I-11 inventory ids duplicated")
    _require(all(_count(r["id"], 151665, 151935) and _count(r["unrelated_hits"], high=10) for r in inventory), "I-11 inventory count malformed")
    _require(isinstance(recall_rows, list) and (not recall_rows or len(recall_rows) == N and len({r["subj"] for r in recall_rows}) == N and all(_hits(r["para_full_hits"]) for r in recall_rows)), "I-11 whole-sequence recall rows malformed")
    recall, cannibal = sum(sum(r["para_full_hits"]) for r in recall_rows), sum(r["unrelated_hits"] >= 3 for r in inventory)
    return {"recall_n": recall, "n_cannibal": cannibal, "no_i11_exclusion": recall <= 2 and cannibal < 3}


def geometry_reading(geometry):
    row, reference, base = geometry["rows"], geometry["random_base_same_count"], geometry["base_mean_norm"]
    _require(all(_finite(x) for x in (row["cos_mean"], row["effective_rank"], row["mean_norm"], reference["effective_rank"], base)) and base > 0 and reference["effective_rank"] > 0, "geometry nonfinite/zero reference")
    return {"collapsed": row["cos_mean"] > 0.9 or row["effective_rank"] < 0.75 * reference["effective_rank"],
            "norm_ratio": row["mean_norm"] / base}


def admission_reading(p2, fits, step0_probe):
    """c10l_mint_step0.py:89-93: geometry is diagnostic, I-11/P3 exclude.
    The recall is the whole sequence here, per this prereg §2, rather than id 0.
    """
    reasons, p3, i11 = [], {"ok": False, "n_ge_0.98": 0, "underfit": [], "fits": fits}, False
    try:
        _require(_probabilities(fits) and len(fits) == N, "P3 needs 24 finite aggregate fits")
        p3 = {"ok": sum(x >= FIT_MIN for x in fits) >= ADMISSION_MIN,
              "n_ge_0.98": sum(x >= FIT_MIN for x in fits),
              "underfit": [i for i, x in enumerate(fits) if x < FIT_MIN], "fits": fits}
        _require(_count(step0_probe["recall_n"]) and _count(step0_probe["n_cannibal"], high=48), "I-11 counts malformed")
        i11 = step0_probe["recall_n"] <= 2 and step0_probe["n_cannibal"] < 3
        if p2["ok"] is not True:
            reasons.append("P2 failed")
        if not i11:
            reasons.append("I-11 exclusion: whole recall > 2 or cannibal >= 3")
        if not p3["ok"]:
            reasons.append("P3 fewer than 22/24 aggregates >= 0.98")
    except (KeyError, TypeError, ValueError) as e:
        reasons.append("malformed admission: " + str(e))
    outcome = "UNDERFIT" if not p3["ok"] else ("INVALID" if reasons else "ADMITTED")
    return {"P3": p3, "no_i11_exclusion": i11, "excluded": bool(reasons), "reasons": reasons, "outcome": outcome}


def position_reading(per_position_fit):
    _require(isinstance(per_position_fit, list) and len(per_position_fit) == N, "per-position fit needs all 24 values")
    _require(len({r["subj"] for r in per_position_fit}) == N, "per-position subjects duplicated")
    rows = []
    for r in per_position_fit:
        _require(_probabilities(r["probs"]), "final-output fit probabilities malformed")
        _require(_probabilities(r["loss_layer_probs"]) and len(r["loss_layer_probs"]) == len(r["probs"]), "loss-layer fit shape differs")
        rows.append({**r, "underfit": any(p < FIT_MIN for p in r["probs"]),
                     "final_minus_loss": [a - b for a, b in zip(r["probs"], r["loss_layer_probs"])]})
    return {"rows": rows, "underfit": [r["subj"] for r in rows if r["underfit"]],
            "all_positions_fit": not any(r["underfit"] for r in rows), "n": N}


def locality_gates(reference_record, candidate_record):
    reference, candidate = reference_record["arm"], candidate_record["arm"]
    r, c = reference["locality_axes"], candidate["locality_axes"]
    rx, cx = reference["extra"], candidate["extra"]
    return {"L1": c["L1_flipped_to_edited_value"] <= r["L1_flipped_to_edited_value"] + 1 and cx["L1_minted_n"] == 0,
            "same_frame": cx["same_frame_flips"] <= rx["same_frame_flips"] + 1 and cx["frame_minted_n"] == 0,
            "described_as": candidate["locality_described_as"] >= reference["locality_described_as"] - 3,
            "L3": c["L3_top1_agree"] >= L3_MIN and cx["L3_minted_n"] == 0,
            "generic_ppl": c["generic_ppl_post"] <= r["generic_ppl_post"] + 0.5,
            "cannibal": cx["post_write_cannibal"] <= 2, "sibling": cx["para_sibling"] <= 3}


def bigram_reading(rows, block):
    _require(block in KINDS, "unknown bigram block")
    _require(isinstance(rows, list) and len(rows) == N and len({r["subj"] for r in rows}) == N, "bigram requires 24 distinct facts")
    for r in rows:
        _require(all(type(r[k]) in (int, bool) and r[k] in (0, 1) for k in (("c_k", "s_k", "b_k") if block == "F" else ("c_k", "s_k"))), "bigram hit is not binary")
        _require(_finite(r["n_k"]) and 0 <= r["n_k"] <= 1 and abs(6 * r["n_k"] - round(6 * r["n_k"])) < 1e-9, "never-edited bigram fraction is not out of six")
    c = sum(r["c_k"] for r in rows)
    x = sum(bool(r["s_k"] or r["n_k"] >= 0.5 or (block == "F" and r["b_k"])) for r in rows)
    return {"C": c, "X": x, "n": N, "qualifier": "BIGRAM" if c >= 1 and x >= c else None,
            "reading": "NO-CONTINUATION" if c == 0 else ("SUBJECT-INDEPENDENT-CONTINUATION" if x >= c else "SUBJECT-DEPENDENCE-NOT-OVERTURNED")}


def _norm(record):
    layers = record["recipe"]["delta_norms"]["candidate"]
    _require(set(layers) == {str(l) for l in range(4, 9)}, "write norm layer population differs")
    values = [v["delta_norm"] for v in layers.values()]
    _require(bool(values) and all(_finite(x) and x >= 0 for x in values), "write norms missing/nonfinite")
    return math.sqrt(sum(x * x for x in values))


def _p2_record_validity(record, subjects, rows):
    p2, kind = record["admission"]["P2"], record["kind"]
    if kind == "multi":
        return
    checks = {"inventory_unchanged", "registered_word_ids", "all_target_rows"}
    if kind == "mint2":
        checks.add("bigram_720_prefix_ids")
    _require(p2["ok"] is True and set(p2["checks"]) == checks and all(x is True for x in p2["checks"].values()) and p2["changed"] == [], "P2 checks/changed prompts disagree")
    _require(_count(p2["plain_n"], 1, 10 ** 9) and _count(p2["inventory_n"], p2["plain_n"], 10 ** 9) and p2["kind"] == kind and p2["block"] == record["block"], "P2 inventory/kind malformed")
    p2rows, templates = p2["rows"], [t for g in record["ctx"] for t in g]
    _require(len(p2rows) == N and [r["subj"] for r in p2rows] == subjects, "P2 target population differs")
    words, ids = record["minted_words"], record["minted_ids"]
    n = {"mint1": 24, "mint1_48": 48, "mint2": 48, "modifier": 8}[kind]
    _require(len(words) == n and len(set(words)) == n and all(isinstance(w, str) for w in words) and ids == list(range(151665, 151665 + n)), "registered words/ids population differs")
    lookup = dict(zip(words, ids))
    for p, r in zip(p2rows, rows):
        expected_checks = {"whole_target", "decode", "engine_default_call", "contexts"} | ({"head_decode"} if kind == "mint2" else set())
        _require(p["value"] == r["val"] and p["ok"] is True and set(p["checks"]) == expected_checks and all(x is True for x in p["checks"].values()), "P2 target/decode checks failed")
        _require(p["target_ids"] == p["expected_ids"] and isinstance(p["target_ids"], list) and len(p["target_ids"]) == r["ntok"] and all(_count(i, 0, 151935) for i in p["target_ids"]), "P2 whole-target ids differ")
        head, modifier = r["val"].split()
        target = p["target_ids"]
        _require(target == [lookup[r["val"]]] if kind in ("mint1", "mint1_48") else target == [lookup[head], lookup[modifier]] if kind == "mint2" else target[-1] == lookup[modifier] and all(i < 151665 for i in target[:-1]), "P2 target ids belong to wrong value/position")
        _require([c["template"] for c in p["contexts"]] == templates and all(c[k] is True for c in p["contexts"] for k in ("prefix_ids", "whole_ids", "last_id")), "P2 frozen-template population/checks differ")
    if kind == "mint2":
        _require(len(p2["bigram_rows"]) == 720 and all(r["ok"] is True for r in p2["bigram_rows"]), "P2 bigram 720-prefix audit incomplete")


def _material_validity(record):
    block, kind = record["block"], record["kind"]
    identity, provenance = record["identity"], record["provenance"]
    hashes = identity["source_sha256"]
    _require(isinstance(hashes, dict) and hashes and all(isinstance(k, str) and _hash(v) for k, v in hashes.items()) and PREREG in hashes and WORDLIST in hashes, "source hashes/prereg/wordlist missing")
    digest = hashlib.sha256("\n".join(k + " " + v for k, v in sorted(hashes.items())).encode()).hexdigest()
    _require(identity["source_digest"] == digest, "source digest differs from hashes")
    _require(provenance["heads_sha256"] == HEADS_SHA256 and provenance["modifiers_sha256"] == MODIFIERS_SHA256, "frozen word list hashes differ")
    _require(provenance["wordlist_sha256"] == hashes[WORDLIST], "wordlist source/provenance hashes differ")
    _require(_hash(provenance["rules_sha256"]) and provenance["rules_sha256"] == json_digest(provenance["rules"]), "rule hash differs")
    relation_table = provenance["relation_table"]
    _require(relation_table["block"] == block, "relation table block differs")
    relations = relation_table["subject_values"]
    _require(isinstance(relations, dict) and len(relations) == N and all(isinstance(k, str) and isinstance(v, str) for k, v in relations.items()), "relation table needs 24 subjects/values")
    _require(_hash(provenance["relation_sha256"]) and provenance["relation_sha256"] == json_digest(relation_table), "relation table hash differs")
    pairing = provenance["row_pairing"]
    if kind != "multi":
        _require(pairing["pairing_ok"] is True and all(_hash(pairing[k]) for k in ("rows_sha256", "first8_sha256", "first24_sha256")), "row pairing proof/hash missing")
    context = record["ctx"]
    _require(isinstance(context, list) and context and all(isinstance(g, list) and g and all(isinstance(t, str) and t.count("{}") == 1 for t in g) for g in context), "context templates malformed")
    _require(record["ctx_sha256"] == json_digest(context), "context hash differs")
    fp = record["fingerprint"]
    _require(fp["ok"] is True and _hash(fp["sha256"]) and fp["sha256"].startswith("d941a9fb") and fp["_cov_cpu"] == 3, "P1 fingerprint/_cov_cpu failed")
    return relations


def run_validity(record):
    """Every published shape and derivable count is checked; missing data fails closed.
    Per-position underfit is recorded without replacing raw binding by a mask.
    """
    reasons = []
    try:
        block, kind, seed = record["block"], record["kind"], record["seed"]
        _require(block in KINDS and kind in KINDS[block], "block/kind differs from frozen schedule")
        _require(seed is None if kind == "multi" else type(seed) is int and seed in SEEDS, "seed malformed")
        _require(type(record["replicate"]) is int and record["replicate"] in (0, 1) and _count(record["pid"], 1, 2 ** 63), "process/replicate malformed")
        _require(record["outcome"] == "DONE", "behaviour run not complete")
        relations = _material_validity(record)
        inert = record["inertness"]
        _require(inert["ok"] is True and inertness_reading(inert["override_rel"], inert["context_rel"], inert["expr_delta"])["ok"], "capture/context inertness failed")
        wrapper = record["wrapper"]
        _require(type(wrapper["z_override_hits"]) is int and wrapper["z_override_hits"] == 1 and type(wrapper["law5_override_hits"]) is int and wrapper["law5_override_hits"] == 0, "Z_OVERRIDE_HITS audit failed")
        admission, step = record["admission"], record["step0"]
        _require(admission["P2"]["ok"] is True and admission["no_i11_exclusion"] is True, "P2/I-11 failed")
        _require(_count(step["recall_n"]) and _count(step["n_cannibal"], high=48), "pre-write recall/cannibal malformed")
        if kind != "multi":
            admit = admission_reading(admission["P2"], admission["P3"]["fits"], step)
            _require(not admit["excluded"], "; ".join(admit["reasons"]))
        else:
            _require(admission["P3"]["fits"] == [] and step["per_position_fit"] == [] and step["recall_n"] == 0, "multi unexpectedly has mint admission/recall")
        recipe, arm = record["recipe"], record["arm"]
        _require(recipe["arms"]["candidate"] == arm, "normalized arm differs from recipe")
        law = recipe["law5_gate"]
        _require(law["ok"] is True and _finite(law["expr_delta"]) and abs(law["expr_delta"]) < LAW5_EXPR and _finite(law["loc_delta"]) and abs(law["loc_delta"]) < LAW5_LOC, "LAW#5 not INERT")
        for name, control in recipe["arms"].items():
            _require(_count(control["para_full_n"]) and _count(control["para_string_n"]) and control["para_string_n"] >= control["para_full_n"], name + " string < full or malformed")
            if name in ("A1_single", "A2_coherent2"):
                _require(control["para_full_n"] >= CONTROL_MIN, name + " below 68/72")
        _require("A1_single" in recipe["arms"], "A1 control missing")
        rows, pre = recipe["detail"]["candidate"], step["recall_rows"]
        _require(isinstance(rows, list) and len(rows) == N and len({r["subj"] for r in rows}) == N, "candidate needs 24 distinct rows")
        subjects = [r["subj"] for r in rows]
        _require(set(subjects) == set(relations) and all(r["val"] == relations[r["subj"]] for r in rows), "candidate rows differ from relation table")
        _p2_record_validity(record, subjects, rows)
        _require(isinstance(pre, list) and ((kind == "multi" and not pre) or len(pre) == N and [r["subj"] for r in pre] == subjects and all(_hits(r["para_full_hits"]) for r in pre)), "pre-write row population differs")
        _require(sum(sum(r["para_full_hits"]) for r in pre) == step["recall_n"], "pre-write recall differs from rows")
        for r in rows:
            _require(_count(r["ntok"], 1, 20) and type(r["canon_full"]) is bool and type(r["canon_first"]) is bool and all(_hits(r[k]) for k in ("para_full_hits", "para_first_hits", "para_string_hits")), "held-out row shape malformed")
            _require(all(not f or (h and s) for f, h, s in zip(r["para_full_hits"], r["para_first_hits"], r["para_string_hits"])), "full hit lacks first-id/string hit")
            if "para_startswith_hits" in r:
                _require(_hits(r["para_startswith_hits"]) and all(not h or s for h, s in zip(r["para_startswith_hits"], r["para_string_hits"])), "startswith row shape/inclusion differs")
            _require((r["ntok"] == 2 if kind == "mint2" else r["ntok"] == 1 if kind in ("mint1", "mint1_48") else 3 <= r["ntok"] <= 4 if kind == "modifier" else 4 <= r["ntok"] <= 6), "target length differs from arm")
        for metric, field in (("para_full_n", "para_full_hits"), ("para_first_n", "para_first_hits"), ("para_string_n", "para_string_hits")):
            _require(_count(arm[metric]) and arm[metric] == sum(sum(r[field]) for r in rows), metric + " differs from rows")
        _require(arm["canon_n"] == N and arm["para_n"] == N * NT and _count(arm["canon_full_n"], high=N) and arm["canon_full_n"] == sum(r["canon_full"] for r in rows), "canonical/trial counts differ")
        _require(_count(arm["para_startswith_n"]) and arm["para_startswith_n"] <= arm["para_string_n"], "startswith count malformed")
        if all("para_startswith_hits" in r for r in rows):
            _require(arm["para_startswith_n"] == sum(sum(r["para_startswith_hits"]) for r in rows), "startswith count differs from rows")
        _require(type(arm["para_full_binding_n"]) is int and arm["para_full_binding_n"] == arm["para_full_n"] - step["recall_n"], "binding differs from raw minus pre-write recall")
        if kind != "multi":
            positions = position_reading(step["per_position_fit"])["rows"]
            _require([r["subj"] for r in positions] == subjects and all(len(p["probs"]) == r["ntok"] for p, r in zip(positions, rows)), "per-position fit population/length differs")
        axes, extra = arm["locality_axes"], arm["extra"]
        _require(axes["L1_n"] == 12 and axes["L3_n"] == 30 and _count(axes["L1_flipped_to_edited_value"], high=12) and _count(axes["L3_top1_agree"], high=30), "locality pool/count malformed")
        _require(_finite(arm["locality_described_as"]) and 0 <= arm["locality_described_as"] <= 100 and _finite(axes["generic_ppl_post"]) and axes["generic_ppl_post"] > 0, "locality/perplexity nonfinite")
        for key, high in (("same_frame_flips", 6), ("frame_minted_n", 6), ("L1_minted_n", 12), ("L3_minted_n", 30), ("para_sibling", N * NT), ("post_write_cannibal", 48)):
            _require(_count(extra[key], high=high), key + " count malformed")
        curve = extra["per_position_teacher_forced"]
        _require(set(curve) == {str(j) for j in range(max(r["ntok"] for r in rows))}, "teacher-forced position population differs")
        for j, value in curve.items():
            n = NT * sum(r["ntok"] > int(j) for r in rows)
            _require(value["n"] == n and _count(value["hits"], high=n), "teacher-forced curve denominator/count differs")
        if kind in ("mint2", "modifier"):
            bigram_reading(extra["bigram"], block)
            _require([r["subj"] for r in extra["bigram"]] == subjects, "bigram fact order differs")
        _norm(record)
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError) as e:
        reasons.append("incomplete/malformed/invalid run: " + str(e))
    return reasons


def nonadmitted_validity(record):
    """A failed admission has no behavioural measurements or process."""
    reasons = []
    try:
        block, kind, seed = record["block"], record["kind"], record["seed"]
        _require(block in KINDS and kind in KINDS[block] and kind != "multi", "non-admitted block/kind differs from minted schedule")
        _require(type(seed) is int and seed in SEEDS and type(record["replicate"]) is int and record["replicate"] in (0, 1), "non-admitted seed/replicate malformed")
        _require(record["outcome"] == "UNDERFIT" and record["pid"] is None, "non-admitted outcome/process malformed")
        _require(not (set(record) & {"arm", "recipe", "inertness", "wrapper", "values", "when_utc", "spec_amendment"}) and not any(k.startswith("minted_") for k in record), "non-admitted record carries behavioural keys")
        relations = _material_validity(record)
        admission, step = record["admission"], record["step0"]
        p2, fits = admission["P2"], admission["P3"]["fits"]
        _require(p2["ok"] is True and admission["no_i11_exclusion"] is True, "P2/I-11 failed")
        _require(_probabilities(fits) and len(fits) == N, "P3 needs 24 finite aggregate fits")
        admit = admission_reading(p2, fits, step)
        _require(admit["no_i11_exclusion"] is True, "I-11 exclusion or malformed counts")
        _require(not admit["P3"]["ok"], "non-admitted P3 actually passes 22/24 screen")
        _require(admission["P3"]["ok"] is False, "published non-admitted P3 gate differs")
        _require(_count(admission["P3"]["n_ge_0.98"], high=N) and admission["P3"]["n_ge_0.98"] == admit["P3"]["n_ge_0.98"], "published non-admitted P3 count differs")
        _require(admission["outcome"] == "UNDERFIT", "published admission outcome differs")
        p2rows = p2["rows"]
        _require(isinstance(p2rows, list) and len(p2rows) == N and len({r["subj"] for r in p2rows}) == N, "P2 needs 24 distinct subjects")
        subjects = [r["subj"] for r in p2rows]
        _require(set(subjects) == set(relations) and all(r["value"] == relations[r["subj"]] for r in p2rows), "P2 rows differ from relation table")
        rows = [{"subj": r["subj"], "val": r["value"], "ntok": len(r["target_ids"])} for r in p2rows]
        _require(all(r["ntok"] == 2 if kind == "mint2" else r["ntok"] == 1 if kind in ("mint1", "mint1_48") else 3 <= r["ntok"] <= 4 for r in rows), "target length differs from arm")
        inventory = step["minted_inventory"]
        _p2_record_validity({**record, "minted_words": [r["word"] for r in inventory],
                             "minted_ids": [r["id"] for r in inventory]}, subjects, rows)
        pre = step["recall_rows"]
        _require(isinstance(pre, list) and len(pre) == N and [r["subj"] for r in pre] == subjects and all(_hits(r["para_full_hits"]) for r in pre), "pre-write row population differs")
        i11 = i11_reading(inventory, pre)
        _require(i11["no_i11_exclusion"] and i11["recall_n"] == step["recall_n"] and i11["n_cannibal"] == step["n_cannibal"], "I-11 counts differ from rows/inventory")
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError) as e:
        reasons.append("incomplete/malformed/invalid non-admitted record: " + str(e))
    return reasons


def _record_validity(record):
    outcome = record.get("outcome") if isinstance(record, dict) else None
    validators = {"DONE": run_validity, "UNDERFIT": nonadmitted_validity}
    validator = validators.get(outcome, run_validity) if isinstance(outcome, str) else run_validity
    return validator(record)


def _same_block(a, b):
    return a["block"] == b["block"] and a["replicate"] == b["replicate"] and _same_material(a, b)


def _same_material(a, b):
    return a["identity"]["source_sha256"] == b["identity"]["source_sha256"] and a["identity"]["source_digest"] == b["identity"]["source_digest"] and a["ctx_sha256"] == b["ctx_sha256"] and a["ctx"] == b["ctx"] and all(
        a["provenance"][k] == b["provenance"][k] for k in ("heads_sha256", "modifiers_sha256", "rules_sha256", "relation_sha256", "wordlist_sha256"))


def _replica_matches(a, b):
    return _same_material(a, b) and a["block"] == b["block"] and a["kind"] == b["kind"] and a["seed"] == b["seed"] and a["replicate"] == 0 and b["replicate"] == 1 and (a["outcome"] == "UNDERFIT" or b["outcome"] == "UNDERFIT" or a["pid"] != b["pid"]) and (
        a["kind"] == "multi" or a["provenance"]["row_pairing"] == b["provenance"]["row_pairing"])


def _single_label(count, reference, clean):
    if NULL_BAND[0] <= count <= NULL_BAND[1]:
        return "NULL"
    label = "LEAD" if count >= LEAD_MIN else ("PARTIAL" if count - reference >= GAIN_MIN else "NULL")
    return "TRADEOFF" if label in ("LEAD", "PARTIAL") and not clean else label


def _position_mechanism(curve, kind):
    misses = {j: cell["n"] - cell["hits"] for j, cell in curve.items()}
    if misses["0"] > 0:
        state, reading = "POSITION-0-LOSS", "The curve alone cannot assign loss to the span because position 0 also misses."
    elif kind == "mint2" and misses["1"] > 0:
        state, reading = "POSITION-1-LOSS", "Loss at position 1 with none at position 0 is consistent with the carrier-across-frame reading; no causal claim."
    elif any(misses.values()):
        state, reading = "POSITION-CURVE-ONLY", "Report the piece positions separately; this is not a two-id span curve."
    else:
        state, reading = "NO-POSITION-LOSS", "No teacher-forced position loss on these prompts."
    return {"misses_per_position": misses, "state": state, "reading": reading, "causal_claim": False}


def run_reading(reference, candidate, replica=None):
    """replica = {reference: fresh-block multi record, candidate: fresh seed record}."""
    reasons = ["reference: " + r for r in run_validity(reference)] + _record_validity(candidate)
    if not reasons and (reference["kind"] != "multi" or not _same_block(reference, candidate)):
        reasons.append("same-block A7-multi comparator/material missing")
    if replica is not None:
        try:
            reasons.extend("replica: " + r for record in replica.values() for r in _record_validity(record))
            if not _replica_matches(reference, replica["reference"]) or not _replica_matches(candidate, replica["candidate"]):
                reasons.append("replication context/source/init/seed differs or process is not fresh")
            if not _same_block(replica["reference"], replica["candidate"]):
                reasons.append("replica does not use its own same-block comparator")
        except (KeyError, TypeError, AttributeError):
            reasons.append("replica must contain its reference and candidate records")
    if reasons:
        return {"label": "INVALID", "reasons": reasons, "replication_pending": False}
    if candidate["outcome"] == "UNDERFIT":
        return {"label": "UNDERFIT", "reasons": [], "replication_pending": False,
                "replica": None if replica is None else run_reading(replica["reference"], replica["candidate"])}
    arm, count = candidate["arm"], candidate["arm"]["para_full_binding_n"]
    gates = locality_gates(reference, candidate)
    label = _single_label(count, reference["arm"]["para_full_n"], all(gates.values()))
    pending = label in ("LEAD", "PARTIAL") and replica is None
    replica_read = None
    if replica is not None:
        replica_read = run_reading(replica["reference"], replica["candidate"])
        if label in ("LEAD", "PARTIAL"):
            replicated = replica["candidate"]["outcome"] == "DONE" and all(replica_read["gates"].values()) and (replica_read["binding"] >= LEAD_MIN if label == "LEAD" else replica_read["gain"] >= GAIN_MIN and not NULL_BAND[0] <= replica_read["binding"] <= NULL_BAND[1])
            if not replicated:
                label += "-NOT-REPLICATED"
    elif pending:
        label += "-NOT-REPLICATED"
    positions = position_reading(candidate["step0"]["per_position_fit"]) if candidate["kind"] != "multi" else {"rows": [], "underfit": [], "all_positions_fit": True}
    fit_subjects = {r["subj"] for r in positions["rows"] if not r["underfit"]}
    if candidate["kind"] == "multi":
        fit_subjects = {r["subj"] for r in candidate["recipe"]["detail"]["candidate"]}
    masked = sum(sum(r["para_full_hits"]) for r in candidate["recipe"]["detail"]["candidate"] if r["subj"] in fit_subjects) - sum(sum(r["para_full_hits"]) for r in candidate["step0"]["recall_rows"] if r["subj"] in fit_subjects)
    reference_norm = _norm(reference)
    ratio = _norm(candidate) / reference_norm if reference_norm > 0 else None
    qs = ["LARGE-WRITE"] if ratio is not None and ratio > LARGE_WRITE else []
    if replica_read is not None and replica["candidate"]["outcome"] == "DONE" and "LARGE-WRITE" in replica_read["qualifiers"] and "LARGE-WRITE" not in qs:
        qs.append("LARGE-WRITE")
    return {"label": label + "".join("-" + q for q in qs), "reasons": [], "gates": gates,
            "binding": count, "raw": arm["para_full_n"], "pre_recall": candidate["step0"]["recall_n"],
            "reference": reference["arm"]["para_full_n"], "gain": count - reference["arm"]["para_full_n"],
            "string_contains": arm["para_string_n"], "string_startswith": arm["para_startswith_n"],
            "alt_tok_n": arm["para_string_n"] - arm["para_full_n"],
            "masked_binding": masked, "masked_n": NT * len(fit_subjects), "masked_value_n": len(fit_subjects),
            "per_position_curve": positions["rows"], "teacher_forced_curve": arm["extra"]["per_position_teacher_forced"],
            "position_mechanism": _position_mechanism(arm["extra"]["per_position_teacher_forced"], candidate["kind"]),
            "all_positions_fit": positions["all_positions_fit"], "write_ratio": ratio, "qualifiers": qs,
            "bigram": bigram_reading(arm["extra"]["bigram"], candidate["block"]) if candidate["kind"] in ("mint2", "modifier") else None,
            "replica": replica_read, "replication_pending": pending}


def reproduction_gate(mint1_records, multi_record=None):
    reasons, counts, median = [], {}, None
    try:
        _require(len(mint1_records) == 3 and {r["seed"] for r in mint1_records} == set(SEEDS) and all(r["block"] == "F" and r["kind"] == "mint1" for r in mint1_records), "LAW#3 needs frozen mint-1 seeds 0,1,2")
        _require(not any(run_validity(r) for r in mint1_records) and all(_same_block(mint1_records[0], r) for r in mint1_records[1:]) and len({r["pid"] for r in mint1_records}) == 3, "LAW#3 seed runs invalid or source/context/data/process differs")
        counts = {r["seed"]: r["arm"]["para_full_binding_n"] for r in mint1_records}
        _require(all(_count(n, -N * NT) for n in counts.values()), "LAW#3 binding count malformed")
        median = statistics.median(counts.values())
        if median < LEAD_MIN:
            reasons.append("LAW#3 mint-1 median < 30")
        for seed, count in counts.items():
            if not REPRODUCTION[seed][0] <= count <= REPRODUCTION[seed][1]:
                reasons.append("LAW#3 seed " + str(seed) + " outside " + str(REPRODUCTION[seed]))
        if multi_record is not None:
            _require(multi_record["block"] == "F" and multi_record["kind"] == "multi", "LAW#3 multi must use frozen values")
            _require(not run_validity(multi_record) and _same_block(mint1_records[0], multi_record), "LAW#3 multi invalid or source/context/data differs")
            for key, bounds in BASELINE_WINDOW.items():
                if not bounds[0] <= multi_record["arm"][key] <= bounds[1]:
                    reasons.append("LAW#3 frozen multi " + key + " outside " + str(bounds))
    except (KeyError, TypeError, ValueError) as e:
        reasons.append(str(e))
    return {"ok": not reasons, "counts": {str(k): v for k, v in counts.items()}, "median": median, "reasons": reasons,
            "multi_checked": multi_record is not None}


def _population(records, block, replicate, control=False):
    expected = {("mint1_48", s) for s in SEEDS} if control else {("multi", None), *[(k, s) for k in ("mint1", "mint2" if block == "V2" else "modifier") for s in SEEDS]}
    problems = []
    if not isinstance(records, list) or any(not isinstance(r, dict) or not isinstance(r.get("kind"), str) or (r.get("seed") is not None and type(r.get("seed")) is not int) for r in records):
        return {"records": {}, "complete": False, "reasons": ["block record objects/keys malformed"], "missing": []}
    keys = [(r.get("kind"), r.get("seed")) for r in records]
    if len(set(keys)) != len(keys) or any(r.get("block") != block or r.get("replicate") != replicate for r in records) or not set(keys) <= expected:
        problems.append("block population has duplicate, foreign or unexpected records")
    for r in records:
        problems.extend(_record_validity(r))
    if records and not problems:
        executed = [r for r in records if r["outcome"] == "DONE"]
        if len({r["pid"] for r in executed}) != len(executed):
            problems.append("block runs did not use separate processes")
        if any(not _same_block(records[0], r) for r in records[1:]):
            problems.append("block source/context/data hashes differ")
    return {"records": dict(zip(keys, records)), "complete": set(keys) == expected, "reasons": problems,
            "missing": sorted([str(k), str(s)] for k, s in expected - set(keys))}


def _range_direction(pop, block):
    records = pop["records"]
    s = records[("multi", None)]["arm"]["para_full_n"]
    m1 = [records[("mint1", seed)]["arm"]["para_full_binding_n"] for seed in SEEDS]
    kind = "mint2" if block == "V2" else "modifier"
    m2 = [records[(kind, seed)]["arm"]["para_full_binding_n"] for seed in SEEDS]
    if block == "V2":
        label = "SPAN-DIRECTION" if min(m1) - max(m2) >= GAIN_MIN and min(m2) - s >= GAIN_MIN and min(m2) > NULL_BAND[1] else "PAIR-DIRECTION" if max(m2) - s < GAIN_MIN or max(m2) <= NULL_BAND[1] else "MIXED"
    else:
        label = "MODIFIER-RECOVERY" if min(m2) - s >= GAIN_MIN and max(m2) >= min(m1) and min(m2) > NULL_BAND[1] else "NO-MODIFIER-GAIN" if max(m2) - s < GAIN_MIN or max(m2) <= NULL_BAND[1] else "MIXED"
    return {"label": label, "M1": m1, "candidate": m2, "S": s}


def _comparability(pop):
    records = pop["records"]
    if any(records[key]["outcome"] != "DONE" for key in [("multi", None)] + [("mint1", s) for s in SEEDS]):
        return False
    ref = records[("multi", None)]["arm"]
    return all(low <= ref[key] <= high for key, (low, high) in BASELINE_WINDOW.items()) and statistics.median(records[("mint1", s)]["arm"]["para_full_binding_n"] for s in SEEDS) >= LEAD_MIN


def _pairing_problems(pop, block):
    records, reasons = pop["records"], []
    key = "first24_sha256" if block == "V2" else "first8_sha256"
    kind = "mint2" if block == "V2" else "modifier"
    for seed in SEEDS:
        if records[("mint1", seed)]["provenance"]["row_pairing"][key] != records[(kind, seed)]["provenance"]["row_pairing"][key]:
            reasons.append("paired N init differs at seed " + str(seed))
    return reasons


def block_reading(records, replicas=None, controls=None):
    """No direction from partial blocks; ranges never use index-pairwise contrasts.
    BIGRAM is evaluated separately per seed; any qualifying seed annotates routing.
    """
    out = {"direction": "INCOMPLETE", "arms": {}, "reasons": [], "replication_pending": False,
           "controls_pending": False, "raw_direction": None}
    if not records:
        return out
    if not isinstance(records, list) or not isinstance(records[0], dict):
        return {**out, "direction": "INVALID", "reasons": ["block records malformed"]}
    block = records[0].get("block")
    if block not in KINDS:
        return {**out, "direction": "INVALID", "reasons": ["unknown block"]}
    replicas = replicas or None
    controls = controls or None
    a = _population(records, block, 0)
    b = _population(replicas, block, 1) if replicas is not None else None
    ctl = _population(controls, block, 0, True) if controls is not None else None
    problems = a["reasons"] + ([] if b is None else b["reasons"]) + ([] if ctl is None else ctl["reasons"])
    if problems:
        return {**out, "direction": "INVALID", "reasons": problems}
    if not a["complete"] or (b is not None and not b["complete"]):
        return {**out, "missing": a["missing"], "replication_missing": [] if b is None else b["missing"]}
    problems.extend(_pairing_problems(a, block))
    if b is not None:
        problems.extend(_pairing_problems(b, block))
        if any(not _replica_matches(r, b["records"][key]) for key, r in a["records"].items()):
            problems.append("replication material/init/process differs")
    if ctl is not None:
        if block != "V2":
            problems.append("48-row control belongs only to V2")
        for (kind, seed), r in ctl["records"].items():
            m1, m2 = a["records"][("mint1", seed)], a["records"][("mint2", seed)]
            if not _same_block(a["records"][("multi", None)], r) or r["provenance"]["row_pairing"]["first24_sha256"] != m1["provenance"]["row_pairing"]["first24_sha256"] or r["provenance"]["row_pairing"]["rows_sha256"] != m2["provenance"]["row_pairing"]["rows_sha256"]:
                problems.append("48-row control source/context/init pairing differs")
    if problems:
        return {**out, "direction": "INVALID", "reasons": problems}
    nonadmitted = any(r["outcome"] == "UNDERFIT" for p in (a, b, ctl) if p is not None for r in p["records"].values())
    out.update(block=block)
    if not nonadmitted:
        raw, raw_rep = _range_direction(a, block), None if b is None else _range_direction(b, block)
        out.update(raw_direction=raw["label"], ranges=raw,
                   replica_ranges=raw_rep, candidate_range=max(raw["candidate"]) - min(raw["candidate"]),
                   mint1_range=max(raw["M1"]) - min(raw["M1"]), historical_init_range=12)
    ref = a["records"][("multi", None)]
    for key, r in a["records"].items():
        if key[0] == "multi":
            continue
        replica = None if b is None else {"reference": b["records"][("multi", None)], "candidate": b["records"][key]}
        out["arms"][key[0] + "_s" + str(key[1])] = run_reading(ref, r, replica)
    out["replication_pending"] = any(r["replication_pending"] for r in out["arms"].values())
    if block == "F":
        law3 = [reproduction_gate([p["records"][("mint1", s)] for s in SEEDS], p["records"][("multi", None)]) for p in (a, b) if p is not None]
        out["reproduction"] = law3
        if any(not g["ok"] for g in law3):
            return {**out, "direction": "HALT-LAW3", "reasons": [reason for g in law3 for reason in g["reasons"]], "replication_pending": False}
    comparable = block == "F" or all(_comparability(p) for p in (a, b) if p is not None)
    out["comparability_ok"] = comparable
    if not comparable:
        out["reasons"].extend("comparability screen unestablished: " + r["kind"] + "_s" + str(r["seed"]) + " r" + str(r["replicate"]) + " is not DONE"
                              for p in (a, b) if p is not None for r in p["records"].values() if r["kind"] in ("multi", "mint1") and r["outcome"] != "DONE")
        for read in out["arms"].values():
            read["label"] += "-NOT-COMPARABLE"
        return {**out, "direction": "NOT-COMPARABLE"}
    mint_records = [r for p in (a, b) if p is not None for (kind, seed), r in p["records"].items() if kind != "multi"]
    if ctl is not None:
        mint_records.extend(ctl["records"].values())
    underfit_reasons = []
    for r in mint_records:
        name = r["kind"] + "_s" + str(r["seed"]) + " r" + str(r["replicate"])
        if r["outcome"] == "UNDERFIT":
            underfit_reasons.append(name + ": admission UNDERFIT n_ge_0.98=" + str(r["admission"]["P3"]["n_ge_0.98"]) + "/24")
        elif not position_reading(r["step0"]["per_position_fit"])["all_positions_fit"]:
            underfit_reasons.append(name + ": per-position underfit")
    if underfit_reasons:
        return {**out, "direction": "ROUTING-BLOCKED-UNDERFIT", "reasons": underfit_reasons}
    if any(not all(locality_gates(p["records"][("multi", None)], r).values()) for p in (a, b) if p is not None for (kind, seed), r in p["records"].items() if kind != "multi"):
        return {**out, "direction": "ROUTING-BLOCKED-LOCALITY"}
    if ctl is not None and any(not all(locality_gates(ref, r).values()) for r in ctl["records"].values()):
        return {**out, "direction": "ROUTING-BLOCKED-LOCALITY"}
    out["controls_pending"] = block == "V2" and raw["label"] == "SPAN-DIRECTION" and (ctl is None or not ctl["complete"])
    direction = raw["label"]
    if direction != "MIXED" and b is None:
        return {**out, "direction": "PENDING-REPLICATION", "replication_pending": True}
    if b is not None and direction != raw_rep["label"]:
        direction = "MIXED"
    if direction == "SPAN-DIRECTION":
        if out["controls_pending"]:
            return {**out, "direction": "PENDING-CONTROL"}
        m148 = [ctl["records"][("mint1_48", s)]["arm"]["para_full_binding_n"] for s in SEEDS]
        out["M1_48"] = m148
        if min(m148) - max(raw["candidate"]) < GAIN_MIN:
            direction = "SPAN-CONFOUNDED"
    kind = "mint2" if block == "V2" else "modifier"
    bigrams = {"r" + str(p["records"][(kind, 0)]["replicate"]) + "_s" + str(s): bigram_reading(p["records"][(kind, s)]["arm"]["extra"]["bigram"], block) for p in (a, b) if p is not None for s in SEEDS}
    out["bigram"] = bigrams
    qs = ["BIGRAM"] if any(r["qualifier"] for r in bigrams.values()) else []
    if any("LARGE-WRITE" in r["qualifiers"] for name, r in out["arms"].items() if name.startswith(kind + "_s")):
        qs.append("LARGE-WRITE")
    out["direction_qualifiers"] = qs
    out["direction"] = direction + "".join("-" + q for q in qs)
    return out


def _plan(block, replicate, kinds):
    return [{"block": block, "replicate": replicate, "kind": kind, "seed": seed}
            for kind in kinds for seed in ([None] if kind == "multi" else SEEDS)]


def stage_plan(stage, records=None):
    """Pure descriptors; the orchestrator owns source checks, exclusive writes and HALT.
    Context bootstrap is separate, so frozen mint-1 reproduction remains first.
    """
    records = [] if records is None else records
    fixed = {"reproduce": _plan("F", 0, ["mint1"]), "frozen": _plan("F", 0, ["multi", "modifier"]),
             "v2": _plan("V2", 0, ["multi", "mint1", "mint2"])}
    if stage in fixed:
        return fixed[stage]
    _require(stage in ("control", "replicate-F", "replicate-V2"), "unknown schedule stage")
    block = "V2" if stage in ("control", "replicate-V2") else "F"
    initial = [r for r in records if r.get("block") == block and r.get("replicate") == 0 and r.get("kind") != "mint1_48"]
    pop = _population(initial, block, 0)
    if not pop["complete"] or pop["reasons"]:
        return []
    read = block_reading(initial)
    if stage == "control":
        blocked = {"INVALID", "INCOMPLETE", "NOT-COMPARABLE", "ROUTING-BLOCKED-UNDERFIT", "ROUTING-BLOCKED-LOCALITY"}
        return _plan("V2", 0, ["mint1_48"]) if read["raw_direction"] == "SPAN-DIRECTION" and read["direction"] not in blocked else []
    return _plan(block, 1, ["multi", "mint1", "mint2"] if block == "V2" else ["mint1", "multi", "modifier"]) if read["replication_pending"] else []


def p4_reading(record):
    """§2 compiled gate: full-sequence HF/fp16 parity on all 24 canonicals.
    Both GGUF tokenizers must preserve the minted words and the complete targets.
    Held-out parity and Q4_K_M retention are diagnostics, never pass thresholds.
    """
    reasons, readings, tokenizer_gates = [], {}, {}
    try:
        kind = record["kind"]
        _require(kind in ("mint2", "modifier"), "P4 requires mint-2 or modifier-only")
        minted_n = 48 if kind == "mint2" else 8
        first = record["fp16"]
        _require(_hash(first["reference_sha256"]), "P4 reference hash missing")
        signatures = {}
        for label in ("fp16", "q4km"):
            probe = record[label]
            _require(probe["label"] == label and probe["reference_sha256"] == first["reference_sha256"] and probe["identity"] == first["identity"], "GGUF source/reference identity differs")
            minted = probe["minted_tokenization"]
            targets = probe["target_tokenization"]
            _require(len(minted) == minted_n and len({r["word"] for r in minted}) == minted_n and [r["id"] for r in minted] == list(range(151665, 151665 + minted_n)), "minted GGUF tokenizer population differs")
            _require(len(targets) == N and len({r["subj"] for r in targets}) == N, "GGUF targets need 24 distinct subjects")
            by_word = {r["word"]: r["id"] for r in minted}
            by_subject = {r["subj"]: r["expected_ids"] for r in targets}
            for r in targets:
                ids = r["expected_ids"]
                _require(isinstance(ids, list) and all(_count(i, 0, 151935) for i in ids) and (len(ids) == 2 if kind == "mint2" else 3 <= len(ids) <= 4), "GGUF target sequence shape differs")
            tokenizer = all(r["ids"] == [r["id"]] and r["ok"] is True for r in minted) and all(r["ids"] == r["expected_ids"] and r["ok"] is True for r in targets)
            _require(type(probe["tokenizer_ok"]) is bool and probe["tokenizer_ok"] == tokenizer, "published tokenizer gate differs from sequences")
            tokenizer_gates[label] = tokenizer
            groups = probe["groups"]
            _require(set(groups) == {"canon", "para", "L1", "L3", "unrelated"}, "GGUF group population differs")
            for group, n in (("canon", N), ("para", N * NT), ("L1", 12), ("L3", 30), ("unrelated", 10)):
                _require(isinstance(groups[group], list) and len(groups[group]) == n, "GGUF " + group + " pool differs")
                for r in groups[group]:
                    expected, hf, gguf = r["expected_ids"], r["hf_ids"], r["gguf_ids"]
                    _require(isinstance(hf, list) and isinstance(gguf, list) and len(hf) == len(gguf) and all(_count(i, 0, 151935) for i in hf + gguf), "HF/GGUF sequence malformed")
                    _require(type(r["parity"]) is bool and r["parity"] == (hf == gguf), "published sequence parity differs")
                    if group in ("canon", "para"):
                        _require(r["subj"] in by_subject and expected == by_subject[r["subj"]] and len(hf) == len(expected), "subject-specific GGUF target differs")
                        words = r["value"].split()
                        _require(len(words) == 2 and words[1] in by_word, "GGUF value/modifier differs")
                        _require(expected == [by_word[words[0]], by_word[words[1]]] if kind == "mint2" else expected[-1] == by_word[words[1]] and all(i < 151665 for i in expected[:-1]), "GGUF expected ids are misordered or belong to a sibling")
                        _require(type(r["correct"]) is bool and r["correct"] == (gguf == expected), "published full-sequence correctness differs")
                    else:
                        _require(expected is None and len(hf) == 1, "locality GGUF probe shape differs")
            subjects = list(by_subject)
            _require([r["subj"] for r in groups["canon"]] == subjects and [r["subj"] for r in groups["para"]] == [s for s in subjects for _ in range(NT)], "GGUF subject/template order differs")
            signatures[label] = {"minted": [(r["word"], r["id"]) for r in minted], "targets": by_subject,
                                 "reference": {g: [{k: r.get(k) for k in ("subj", "value", "prompt", "expected_ids", "hf_ids")} for r in rows] for g, rows in groups.items()}}
            readings[label] = {"canonical_parity_n": sum(r["hf_ids"] == r["gguf_ids"] for r in groups["canon"]),
                               "heldout_parity_n": sum(r["hf_ids"] == r["gguf_ids"] for r in groups["para"]),
                               "canonical_correct_n": sum(r["gguf_ids"] == r["expected_ids"] for r in groups["canon"]),
                               "heldout_correct_n": sum(r["gguf_ids"] == r["expected_ids"] for r in groups["para"]),
                               "HF_canonical_correct_n": sum(r["hf_ids"] == r["expected_ids"] for r in groups["canon"]),
                               "HF_heldout_correct_n": sum(r["hf_ids"] == r["expected_ids"] for r in groups["para"])}
            for group in ("canon", "para"):
                eligible = [r for r in groups[group] if r["hf_ids"] == r["expected_ids"]]
                readings[label][group + "_retention"] = {"retained": sum(r["gguf_ids"] == r["expected_ids"] for r in eligible), "n": len(eligible)}
        _require(signatures["fp16"] == signatures["q4km"], "GGUF probes use different HF reference payloads")
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        reasons.append("malformed P4: " + str(e))
    if reasons:
        return {"ok": False, "label": "INVALID", "reasons": reasons}
    ok = all(tokenizer_gates.values()) and readings["fp16"]["canonical_parity_n"] == N
    survival = {}
    for group in ("canon", "para"):
        pairs = [(a, b) for a, b in zip(record["fp16"]["groups"][group], record["q4km"]["groups"][group]) if a["gguf_ids"] == a["expected_ids"]]
        survival[group] = {"retained": sum(b["gguf_ids"] == b["expected_ids"] for a, b in pairs), "n": len(pairs)}
    return {"ok": ok, "label": "PASS" if ok else "FAIL", "reasons": [],
            "tokenizer_gates": tokenizer_gates, "fp16": readings["fp16"], "q4km": readings["q4km"],
            "fp16_to_q4_survival": survival,
            "heldout_and_quantized_retention": "reported only; no pass threshold"}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit("usage: c10u_mint2_read.py OUT_DIR")
    directory = Path(argv[0])
    if not directory.is_dir():
        raise SystemExit("OUT_DIR does not exist")
    pattern = re.compile(r"(F|V2)_r([01])_(multi|mint1|modifier|mint2|mint1_48)_s(none|[012])\.json")
    records, errors = [], []
    for path in sorted(directory.iterdir()):
        match = pattern.fullmatch(path.name)
        if match is None:
            continue
        try:
            record = json.loads(path.read_text())
            expected = (match[1], int(match[2]), match[3], None if match[4] == "none" else int(match[4]))
            _require(tuple(record[k] for k in ("block", "replicate", "kind", "seed")) == expected, "filename/run identity differs")
            records.append(record)
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            errors.append(path.name + ": " + str(e))
    out = {}
    for block in ("F", "V2"):
        initial = [r for r in records if r["block"] == block and r["replicate"] == 0 and r["kind"] != "mint1_48"]
        replicas = [r for r in records if r["block"] == block and r["replicate"] == 1 and r["kind"] != "mint1_48"]
        controls = [r for r in records if r["block"] == block and r["kind"] == "mint1_48"]
        out[block] = block_reading(initial, replicas or None, controls or None)
        if errors:
            out[block].update(direction="INVALID", reasons=errors)
    print(json.dumps(out, indent=2, allow_nan=False))
    return 2 if any(r["direction"] in ("INVALID", "HALT-LAW3") for r in out.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
