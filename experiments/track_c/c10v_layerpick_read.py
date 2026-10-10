#!/usr/bin/env python3
"""Frozen D-C10v-layerpick v2 readings; stdlib only, no model imports."""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, hashlib, json, math, re
from pathlib import Path

DECISION_ID = "D-C10v-layerpick"
PREREG = "docs/C10V_LAYERPICK_PREREG.md"
HP_FILE = "configs/hparams/qwen25_3b_memit_hparams.json"
LAYERS = (4, 5, 6, 7, 8)
ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
RECIPES = ("A", "B0", "B", "Bshuf")
ENGINE_SHA256 = "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65"
ENGINE_FILE = "memit_dry_run/memit/memit/memit_main.py"
REQUIRED_SOURCES = (PREREG, HP_FILE, ENGINE_FILE, "tools/engine_fingerprint.py",
                    "memit_dry_run/memit/globals.yml",
                    "experiments/track_c/c10e_bandknob.py", "configs/screens/g6_screen_qwen3b.json",
                    "configs/screens/g6_screen_qwen3b_v2.json",
                    "results/c10l_covgeom/step0_offline.json",
                    *("experiments/track_c/c10v_layerpick_" + n + ".py" for n in ("arms", "read", "selftest")))
N, NT, CTRL, LEAD, GAIN, LARGE_WRITE = 24, 3, 68, 30, 10, 1.5


class GateError(ValueError):
    pass


def require(ok, gate, detail=""):
    if not ok:
        raise GateError(gate + (": " + str(detail) if detail else ""))


def json_digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def source_digest(hashes):
    return hashlib.sha256("\n".join(k + " " + v for k, v in sorted(hashes.items())).encode()).hexdigest()


def finite(x):
    return type(x) in (int, float) and math.isfinite(x)


def count(x, maximum=72):
    return type(x) is int and 0 <= x <= maximum


def sha(x):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{64}", x) is not None


def groups(layer_map, subjects):
    require(set(layer_map) == set(subjects), "MAP_SUBJECTS")
    require(all(type(layer_map[s]) is int and layer_map[s] in LAYERS for s in subjects), "MAP_LAYERS")
    return [(l, [s for s in subjects if layer_map[s] == l]) for l in reversed(LAYERS)
            if any(layer_map[s] == l for s in subjects)]


def recipe_maps(published, subjects):
    groups(published, subjects)
    return {"A": None, "B0": {s: 8 for s in subjects}, "B": dict(published),
            "Bshuf": {s: published[subjects[(i + 1) % N]] for i, s in enumerate(subjects)}}


def select_maps(first, second, subjects):
    """prereg:33: measured margin, nearest-8 ties/fallback; no fitted threshold."""
    require(len(subjects) == N and len(set(subjects)) == N, "SELECTOR_POPULATION")
    for table in (first, second):
        require(len(table) == N and all(len(row) == len(LAYERS) and all(finite(x) for x in row)
                                       for row in table), "SELECTOR_TABLE")
    delta = max(abs(first[i][j] - second[i][j]) for i in range(N) for j in range(5))
    maps, margins, runners = [], [], []
    for table in (first, second):
        selected, mm, rr = {}, [], []
        for s, row in zip(subjects, table):
            order = sorted(range(5), key=lambda j: (-row[j], -LAYERS[j]))
            margin = row[order[0]] - row[order[1]]
            near = [LAYERS[j] for j in range(5) if row[j] >= row[order[0]] - delta]
            selected[s] = LAYERS[order[0]] if margin >= delta else max(near)
            mm.append(margin)
            rr.append(LAYERS[order[1]])
        maps.append(selected); margins.append(mm); runners.append(rr)
    reproducible = maps[0] == maps[1]
    concentration = max(list(maps[0].values()).count(l) for l in LAYERS)
    status = ("map not reproducible" if not reproducible else
              "concentrated map; candidate not advanced" if concentration >= 20 else "READY")
    return {"map": maps[0], "repeat_map": maps[1], "map_sha256": json_digest(maps[0]),
            "G_table": first, "G_table_repeat": second, "delta": delta,
            "winning_margins": margins, "runner_up": runners, "map_reproduced": reproducible,
            "concentration": concentration, "status": status}


def validate_step0(step):
    subjects = step["subjects"]
    derived = select_maps(step["G_table"], step["G_table_repeat"], subjects)
    require(all(step[k] == v for k, v in derived.items()), "SELECTOR_RECOMPUTATION")
    require(step["ctx_sha256"] == json_digest(step["ctx"]), "CONTEXT_HASH")
    require(step["ctx"] and step["ctx"][0] == ["{}"] and
            all(isinstance(g, list) and g and all(isinstance(t, str) and t.count("{}") == 1
                                                for t in g) for g in step["ctx"]), "CONTEXT_SHAPE")
    for key in ("projected_key_norms", "projected_key_norms_repeat"):
        require(len(step[key]) == N and all(len(r) == 5 and all(finite(v) and v >= 0 for v in r)
                                           for r in step[key]), "PROJECTED_KEY_NORMS")
    require(len(step["installed_share_comparison"]) == N and
            all(finite(r["installed_share"]) and finite(r["max_G"]) and r["subj"] == s
                for r, s in zip(step["installed_share_comparison"], subjects)), "INSTALLED_SHARE")


def validate_identity(identity, fingerprint):
    hashes = identity["source_sha256"]
    require(sha(identity["source_digest"]) and all(k in hashes for k in REQUIRED_SOURCES)
            and all(sha(v) for v in hashes.values()) and
            identity["source_digest"] == source_digest(hashes), "SOURCE_IDENTITY")
    require(identity["run_id"] and identity["preflight_controls_reference"]["ok"] is True and
            sha(identity["preflight_controls_reference"]["sha256"]) and
            all(count(identity["preflight_controls_reference"]["scores"][a]) and
                identity["preflight_controls_reference"]["scores"][a] >= CTRL for a in ARMS[:2]), "LAW3_REFERENCE")
    require(fingerprint["ok"] is True and fingerprint["sha256"] == ENGINE_SHA256 and
            fingerprint["_cov_cpu"] == 3 and hashes[ENGINE_FILE] == ENGINE_SHA256, "FINGERPRINT")


def law5_reading(proof, published=None, subjects=None):
    standing, floor = proof["standing"], proof["floor"]
    require(finite(standing["expr_delta"]) and 0 <= standing["expr_delta"] < 0.05 and
            finite(standing["loc_delta"]) and 0 <= standing["loc_delta"] < 3 and
            standing["ok"] is True and proof["standing_override_hits"] == 0, "LAW5_I")
    require(set(floor["relative_by_layer"]) == {str(l) for l in LAYERS} and
            all(finite(x) and x >= 0 for x in floor["relative_by_layer"].values()) and
            finite(floor["relative_max"]) and floor["relative_max"] == max(floor["relative_by_layer"].values()) and
            set(floor["behavior_count_deltas"]) == {"canon_full_n", "para_full_n"} and
            all(count(x) for x in floor["behavior_count_deltas"].values()) and
            proof["tolerance"] == max(1e-4, 10 * floor["relative_max"]), "LAW5_II")
    for key, gate in (("identity", "LAW5_III"), ("singleton", "LAW5_IV"), ("multigroup", "LAW5_V")):
        part = proof[key]
        require(part["relative_by_layer"] and all(finite(x) and 0 <= x <= proof["tolerance"]
                                                 for x in part["relative_by_layer"].values()), gate)
        if key == "identity":
            require(set(part["relative_by_layer"]) == {str(l) for l in LAYERS} and
                    part["behavior_equal"] is True and part["active_group_layers"] == [list(LAYERS)], gate)
        if key == "singleton":
            require(set(part["relative_by_layer"]) == {"8"} and
                    part["active_group_layers"] == [[8]] and part["projector_indices"] == [4], gate)
        if key == "multigroup":
            require(len(part["active_group_layers"]) == 2 and
                    part["active_group_layers"] == sorted(part["active_group_layers"], reverse=True) and
                    set(part["relative_by_layer"]) == {str(ls[0]) for ls in part["active_group_layers"]}, gate)
            if published is not None:
                largest = sorted(groups(published, subjects), key=lambda g: (-len(g[1]), -g[0]))[:2]
                expected = [{"layers": [l], "subjects": ss, "projector_indices": [l - 4]}
                            for l, ss in sorted(largest, reverse=True)]
                require(part["groups"] == expected, gate)
    require(proof["ok"] is True, "LAW5_COMPLETE")


def row_counts(rows, subjects):
    require(len(rows) == N and [r["subj"] for r in rows] == subjects, "ROW_SUBJECTS")
    for row in rows:
        require(type(row["canon_full"]) is bool and type(row["canon_first"]) is bool, "CANON_HITS")
        for key in ("para_full_hits", "para_first_hits", "para_string_hits"):
            require(len(row[key]) == NT and all(type(x) is bool for x in row[key]), "PARA_HITS")
        require(all(not f or first for f, first in zip(row["para_full_hits"], row["para_first_hits"]))
                and (not row["canon_full"] or row["canon_first"]), "FULL_FIRST_CONSISTENCY")
    return {"canon_full_n": sum(r["canon_full"] for r in rows),
            "para_full_n": sum(sum(r["para_full_hits"]) for r in rows),
            "para_first_n": sum(sum(r["para_first_hits"]) for r in rows),
            "para_string_n": sum(sum(r["para_string_hits"]) for r in rows)}


def recipe_integrity(rec, name, step, published):
    subjects = step["subjects"]
    expected = recipe_maps(published, subjects)[name]
    require(rec["map"] == expected and rec["band"] == list(LAYERS), "RECIPE_MAP")
    require(rec["law5_gate"]["ok"] is True, "RECIPE_LAW5")
    for arm_name in ARMS:
        arm = rec["arms"][arm_name]
        derived = row_counts(rec["detail"][arm_name], subjects)
        require(all(count(arm[k]) and arm[k] == v for k, v in derived.items()) and
                arm["canon_n"] == N and arm["para_n"] == N * NT, "SUMMARY_COUNTS", arm_name)
        audit = rec["wrapper"][arm_name]
        wanted = [(list(LAYERS), subjects)] if expected is None else [([l], ss) for l, ss in groups(expected, subjects)]
        require(audit["groups"] == [{"layers": ls, "subjects": ss,
                                     "projector_indices": [LAYERS.index(l) for l in ls]} for ls, ss in wanted]
                and audit["z_override_hits"] == len(wanted), "OVERRIDE_GROUPS", arm_name)
        norms = rec["delta_norms"][arm_name]
        require(set(norms) == {str(l) for ls, _ in wanted for l in ls} and
                all(finite(v["delta_norm"]) and v["delta_norm"] >= 0 for v in norms.values()), "WRITE_NORMS")
        ax, extra = arm["locality_axes"], arm["extra"]
        require(ax["L1_n"] == 12 and count(ax["L1_flipped_to_edited_value"], 12) and
                ax["L3_n"] == 30 and count(ax["L3_top1_agree"], 30) and
                finite(ax["generic_ppl_post"]) and ax["generic_ppl_post"] > 0 and
                finite(ax["generic_ppl_pre"]) and ax["generic_ppl_pre"] > 0 and
                finite(arm["locality_described_as"]) and 0 <= arm["locality_described_as"] <= 100 and
                extra["same_frame"]["n"] == 6 and count(extra["same_frame"]["flips"], 6), "LOCALITY_SHAPE")
        require(set(extra["relation_labels"]) == {"bystander", "objective-anchored"} and
                all(p["n"] == N and len(p["pre_top1"]) == len(p["post_top1"]) == N and
                    all(count(x, 151935) for x in p["pre_top1"] + p["post_top1"]) and
                    p["flips"] == sum(a != b for a, b in zip(p["pre_top1"], p["post_top1"]))
                    for p in extra["relation_labels"].values()), "RELATION_PROBES")
        ids = rec["target_ids"][arm_name]
        require(set(ids) == set(subjects) and all(v and all(count(x, 151935) for x in v) for v in ids.values()), "TARGET_IDS")
        frame = extra["same_frame"]
        require(len(frame["rows"]) == 6 and len({r["subj"] for r in frame["rows"]}) == 6 and
                all(count(r["top1"], 151935) and type(r["flip"]) is bool and
                    r["flip"] == (r["top1"] in {v[0] for v in ids.values()}) for r in frame["rows"]) and
                frame["flips"] == sum(r["flip"] for r in frame["rows"]), "FRAME_PROBE")
        rows = rec["detail"][arm_name]
        require(all(count(r["tf_total"], 10000) and count(r["tf_correct"], r["tf_total"]) for r in rows), "TF_COUNTS")
        tf_total = sum(r["tf_total"] for r in rows)
        expected_tf = round(100 * sum(r["tf_correct"] for r in rows) / tf_total, 1) if tf_total else None
        expected_cond = round(arm["para_full_n"] / arm["para_first_n"], 3) if arm["para_first_n"] else None
        require("tf_pertok_cont" in arm and "cond_full_given_first" in arm and
                arm["tf_pertok_cont"] == expected_tf and arm["cond_full_given_first"] == expected_cond, "FULL_READOUT")
        require(sha(rec["targets_sha256"][arm_name]) and
                set(rec["predictions_before_write"][arm_name]) == set(subjects), "PRISTINE_PREDICTIONS")
        if arm_name != "A2_coherent2":
            require(len(extra["proxy"]["rows"]) == N and
                    [r["subj"] for r in extra["proxy"]["rows"]] == subjects, "PROXY_READOUT")
            for row in extra["proxy"]["rows"]:
                require(row["layer"] == (8 if expected is None else expected[row["subj"]]) and
                        len(row["rho_per_prompt"]) == 4 and
                        all(x is None or finite(x) and x >= 0 for x in row["rho_per_prompt"]) and
                        all(row[k] is None or finite(row[k]) for k in
                            ("realised_fraction", "full_G_diagonal", "group_G_diagonal", "prediction_error")), "PROXY_VALUES")
                prediction = rec["predictions_before_write"][arm_name][row["subj"]]
                require(all(finite(prediction[k]) and prediction[k] == row[k]
                            for k in ("full_G_diagonal", "group_G_diagonal")) and
                        math.isclose(row["full_G_diagonal"], step["G_table"][subjects.index(row["subj"])][row["layer"] - 4],
                                     rel_tol=1e-10, abs_tol=1e-12) and
                        len(row["pristine_residual_norms"]) == 4 and
                        all(finite(x) and x >= 0 for x in row["pristine_residual_norms"]) and
                        row["undefined_zero_denominator"] == [i for i, x in enumerate(row["pristine_residual_norms"]) if x == 0] and
                        all((rho is None) == (norm == 0) for rho, norm in zip(row["rho_per_prompt"], row["pristine_residual_norms"])) and
                        ((row["realised_fraction"] is None and row["prediction_error"] is None) if row["pristine_residual_norms"][0] == 0 else
                         row["prediction_error"] == row["realised_fraction"] - row["group_G_diagonal"]), "PROXY_PREDICTIONS")
            require(extra["proxy"]["targets_sha256"] == rec["targets_sha256"][arm_name] and
                    extra["proxy"]["weight_application"] == "fp16" and
                    extra["proxy"]["predictions_recorded_before_write"] is True, "PROXY_PROVENANCE")
    validate_covariance(rec["cov_cache_sha256"])
    if name == "A":
        a = rec["arms"][ARMS[2]]
        require(5 <= a["para_full_n"] <= 18 and 5 <= a["canon_full_n"] <= 10, "BASELINE_ENVELOPE")
        require(sum(v["delta_norm"] for v in rec["delta_norms"][ARMS[2]].values()) > 0, "ZERO_BASELINE_WRITE")


def recipe_validity(rec):
    reasons = []
    for arm_name in ARMS:
        arm = rec["arms"][arm_name]
        if not (arm["para_string_n"] == arm["para_full_n"] and
                arm["para_full_string"] == arm["para_full"] == round(100 * arm["para_full_n"] / 72, 1)):
            reasons.append("FULL_STRING: " + arm_name)
        if arm_name in ARMS[:2] and arm["para_full_n"] < CTRL:
            reasons.append("CONTROL_" + arm_name)
    return reasons


def validate_recipe(rec, name, step, published):
    recipe_integrity(rec, name, step, published)
    reasons = recipe_validity(rec)
    if reasons:
        raise GateError("; ".join(reasons))


def validate_covariance(cov):
    require(set(cov) == {str(l) for l in LAYERS} and
            all(sha(c["sha256"]) and isinstance(c["path"], str) and c["path"] for c in cov.values()), "COVARIANCE_PROVENANCE")


def validate_hsic(hsic, published, subjects):
    require(hsic["n"] == N and set(hsic["layers"]) == {str(l) for l in LAYERS}, "HSIC_READOUT")
    scores = {}
    for l in LAYERS:
        row = hsic["layers"][str(l)]
        require(finite(row["sigma_X"]) and row["sigma_X"] >= 0 and
                finite(row["sigma_Y"]) and row["sigma_Y"] >= 0, "HSIC_READOUT")
        if row["sigma_X"] == 0 or row["sigma_Y"] == 0:
            require(row["status"] == "UNDEFINED: zero median pairwise distance", "HSIC_READOUT")
            continue
        require(len(row["per_fact_c"]) == N and all(finite(x) for x in row["per_fact_c"]) and
                finite(row["HSIC_b"]) and math.isclose(row["HSIC_b"], sum(row["per_fact_c"]) / (N - 1) ** 2,
                                                      rel_tol=1e-10, abs_tol=1e-12), "HSIC_READOUT")
        scores[l] = row["per_fact_c"]
    expected = {s: max(LAYERS, key=lambda l: (scores[l][i], l)) for i, s in enumerate(subjects)} if len(scores) == 5 else None
    require(hsic["argmax_c_map"] == expected and
            hsic["agreement_n"] == (sum(expected[s] == published[s] for s in subjects) if expected else None), "HSIC_READOUT")


def pass_integrity(record, name):
    require(record["decision_id"] == DECISION_ID and record["outcome"] == "COMPLETE"
            and type(record["pid"]) is int and record["pid"] > 0, "PASS_IDENTITY")
    validate_identity(record["identity"], record["fingerprint"])
    validate_step0(record["step0"])
    require(record["step0"]["map_reproduced"] is True, "MAP_REPRODUCIBLE")
    require(record["published_map_sha256"] == json_digest(record["published_map"]), "PUBLISHED_MAP_HASH")
    law5_reading(record["law5"], record["published_map"], record["step0"]["subjects"])
    require(record["ctx_sha256"] == record["step0"]["ctx_sha256"] and record["ctx"] == record["step0"]["ctx"], "PASS_CONTEXT")
    require(set(record["recipes"]) == set(RECIPES), "RECIPE_INVENTORY")
    validate_recipe(record["recipes"]["A"], "A", record["step0"], record["published_map"])
    recipe_integrity(record["recipes"][name], name, record["step0"], record["published_map"])
    require(record["recipes"]["A"]["cov_cache_sha256"] == record["recipes"][name]["cov_cache_sha256"], "COVARIANCE_DRIFT")
    require("hsic" in record, "HSIC_READOUT")
    validate_hsic(record["hsic"], record["published_map"], record["step0"]["subjects"])


def pass_validity(record, name):
    try:
        pass_integrity(record, name)
        return recipe_validity(record["recipes"][name])
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        return [str(exc)]


def rank_values(xs):
    ranks = [0.0] * len(xs)
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    start = 0
    while start < len(xs):
        end = start + 1
        while end < len(xs) and xs[order[end]] == xs[order[start]]:
            end += 1
        for i in order[start:end]:
            ranks[i] = (start + 1 + end) / 2
        start = end
    return ranks


def spearman(xs, ys):
    a, b = rank_values(xs), rank_values(ys)
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    numerator = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    denominator = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return numerator / denominator if denominator else None


def candidate_reading(record, name):
    reasons = pass_validity(record, name)
    if reasons:
        return {"label": "INVALID", "base_label": "INVALID", "reasons": reasons, "gate_A": False}
    base, cand = (record["recipes"][k]["arms"][ARMS[2]] for k in ("A", name))
    ba, ca = base["locality_axes"], cand["locality_axes"]
    gates = {"L1": ca["L1_flipped_to_edited_value"] <= ba["L1_flipped_to_edited_value"] + 1,
             "same_frame": cand["extra"]["same_frame"]["flips"] <= base["extra"]["same_frame"]["flips"] + 1,
             "described_as": cand["locality_described_as"] >= base["locality_described_as"] - 3,
             "L3": ca["L3_top1_agree"] >= 29,
             "generic_ppl": ca["generic_ppl_post"] <= ba["generic_ppl_post"] + 0.5}
    sizes = {k: sum(v["delta_norm"] for v in record["recipes"][k]["delta_norms"][ARMS[2]].values()) for k in ("A", name)}
    require(sizes["A"] > 0, "ZERO_BASELINE_WRITE")
    ratio = sizes[name] / sizes["A"]
    n, gain = cand["para_full_n"], cand["para_full_n"] - base["para_full_n"]
    sized = "LEAD" if n >= LEAD else "PARTIAL" if 18 < n < LEAD and gain >= GAIN else "NULL"
    label = "TRADEOFF" if sized != "NULL" and (not all(gates.values()) or ratio > LARGE_WRITE) else sized
    base_label = label
    if ratio > LARGE_WRITE:
        label += "-LARGE-WRITE"
    attributed = None
    if name == "B" and base_label in ("LEAD", "PARTIAL"):
        attributed = all(not pass_validity(record, control) and
                         n - record["recipes"][control]["arms"][ARMS[2]]["para_full_n"] >= GAIN
                         for control in ("B0", "Bshuf"))
        if not attributed:
            label += "-PLACEMENT-NOT-ATTRIBUTED"
    rows = record["recipes"][name]["detail"][ARMS[2]]
    layers = record["recipes"][name]["map"] or {s: 8 for s in record["step0"]["subjects"]}
    edges = [all(r["para_full_hits"]) for r in rows]
    return {"label": label, "base_label": base_label, "count_label": sized, "binding": n, "gain": gain,
            "locality_gates": gates, "write_ratio": ratio, "attributed": attributed,
            "per_template": [sum(r["para_full_hits"][j] for r in rows) for j in range(NT)],
            "per_edge_3of3": edges, "assigned_layers": [layers[r["subj"]] for r in rows],
            "by_layer": {str(l): {"facts": sum(layers[r["subj"]] == l for r in rows),
                                   "para_full": sum(sum(r["para_full_hits"]) for r in rows if layers[r["subj"]] == l),
                                   "edges_3of3": sum(ok for r, ok in zip(rows, edges) if layers[r["subj"]] == l)} for l in LAYERS},
            "spearman_G_edge": spearman([r["full_G_diagonal"] for r in cand["extra"]["proxy"]["rows"]], edges),
            "gate_A": False, "reasons": []}


def replication_needed(first):
    return any(candidate_reading(first, name)["base_label"] in ("PARTIAL", "LEAD") for name in ("B", "B0"))


def read_run(first, second=None):
    readings = {name: candidate_reading(first, name) for name in RECIPES[1:]}
    for name, reading in readings.items():
        if name == "Bshuf":
            reading["label"] += "-CONTROL-ONLY"
            continue
        if reading["base_label"] not in ("LEAD", "PARTIAL"):
            continue
        repeated, second_reading = False, None
        if second is not None:
            second_reading = candidate_reading(second, name)
            repeated = (first["pid"] != second["pid"] and first["identity"] == second["identity"] and
                        first["published_map"] == second["published_map"] and
                        first["recipes"]["A"]["cov_cache_sha256"] == second["recipes"]["A"]["cov_cache_sha256"] and
                        second_reading["base_label"] in (("LEAD",) if reading["base_label"] == "LEAD" else ("PARTIAL", "LEAD")))
        if not repeated:
            reading["label"] += "-NOT-REPLICATED"
        if name == "B" and repeated and second_reading["attributed"] is not True and reading["attributed"] is True:
            reading["label"] += "-PLACEMENT-NOT-ATTRIBUTED"
        reading["replicated"] = repeated
        reading["replication_pending"] = second is None
        reading["second_process"] = second_reading
        reading["gate_A"] = repeated and (name == "B0" or reading["attributed"] is True and second_reading["attributed"] is True)
    return {"decision_id": DECISION_ID, "readings": readings, "replication_needed": replication_needed(first),
            "scope": "candidate placement only; not depth closure, §8.9 closure, F1 change, LOKI or WilKE evidence"}


def read_directory(out, root):
    out = Path(out)
    step = json.loads((out / "step0.json").read_text())
    validate_identity(step["identity"], step["fingerprint"])
    validate_step0(step)
    require(json.loads((out / "identity.json").read_text()) == step["identity"], "PERSISTED_IDENTITY")
    for name, expected in step["identity"]["source_sha256"].items():
        path = Path(root) / name
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected, "CURRENT_SOURCE", name)
    if step["status"] != "READY":
        require(not any((out / n).exists() for n in ("pass1_started.json", "law5.json", "pass1.json")), "STOPPED_HAS_PASS")
        terminal = json.loads((out / "run.json").read_text())
        require(terminal["identity"] == step["identity"] and terminal["label"] == step["status"] and
                terminal["candidate_advanced"] is False and terminal["step0_sha256"] == hashlib.sha256((out / "step0.json").read_bytes()).hexdigest(), "TERMINAL_RECORD")
        return {"decision_id": DECISION_ID, "label": step["status"], "candidate_advanced": False}
    passes = []
    for stage in ("pass1", "pass2"):
        path = out / (stage + ".json")
        if not path.exists():
            break
        record = json.loads(path.read_text())
        require(record["identity"] == step["identity"] and record["published_map"] == step["map"], "STAGE_IDENTITY")
        start = json.loads((out / (stage + "_started.json")).read_text())
        proof = json.loads((out / ("law5.json" if stage == "pass1" else "law5_pass2.json")).read_text())
        require(start["identity"] == record["identity"] and start["pid"] == record["pid"] and
                start["law5_ok"] is True and start["live_law3_ok"] is True and
                start["published_map_sha256"] == record["published_map_sha256"] and
                proof["identity"] == record["identity"] and proof["pid"] == record["pid"] and
                proof["law5"] == record["law5"] and proof["ctx_sha256"] == record["ctx_sha256"] and
                proof["published_map_sha256"] == record["published_map_sha256"], "START_GATE_RECORDS")
        marker = json.loads((out / (stage + "_complete.json")).read_text())
        require(marker["record_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest() and
                marker["pid"] == record["pid"] and marker["identity"] == record["identity"], "COMPLETE_MARKER")
        passes.append(record)
    require(passes, "PASS1_MISSING")
    reading = read_run(*passes)
    if len(passes) == 2 or not reading["replication_needed"]:
        terminal = json.loads((out / "run.json").read_text())
        require(terminal["identity"] == step["identity"] and all(terminal[k] == v for k, v in reading.items()) and
                terminal["pass_sha256"] == {"pass" + str(i + 1): hashlib.sha256((out / ("pass" + str(i + 1) + ".json")).read_bytes()).hexdigest()
                                           for i in range(len(passes))}, "TERMINAL_RECORD")
    else:
        require(not (out / "run.json").exists(), "PREMATURE_TERMINAL_RECORD")
    return reading


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--root", type=Path, default=Path(LLMDB_ROOT))
    args = parser.parse_args(argv)
    try:
        reading = read_directory(args.out_dir, args.root)
        print(json.dumps(reading, indent=2, allow_nan=False))
        return 2 if any(r["base_label"] == "INVALID" for r in reading.get("readings", {}).values()) else 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({"label": "INVALID", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
