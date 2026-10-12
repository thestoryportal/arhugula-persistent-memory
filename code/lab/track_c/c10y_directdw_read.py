"""Frozen C10Y §3 reader. All readings are MEASUREMENT-ONLY.

Classification uses saved scientific numbers; loading separately checks current
file identity. Neither path reads live telemetry or calibration.
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path


LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
ROOT = Path(os.environ.get("LLMDB_ROOT", str(Path(__file__).resolve().parents[2])))
PREREG_SHA = "e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331"
ENGINE_SHA = "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
A7 = ARMS[2]
LAYERS = (4, 5, 6, 7, 8)
FRAMES = ("CANON", "frame0", "frame1", "frame2", "frame3", "frame4", "frame5")
RECIPES = ("B-e2e", "B-z", "B-e2e-NM", "B-e2e-ENV")
SOURCES = ("driver", "reader", "check", "harness", "templates", "hparams", "compute_z", "compute_ks", "repr_tools", "memit_main", "prereg")
INPUTS = ("contexts", "hparams", "covariance", "model", "tokenizer")
POSITIVE = ("LEAD", "PARTIAL")


class _Refusal(Exception):
    def __init__(self, reason, label="INVALID"):
        super().__init__(reason)
        self.label = label


def _require(ok, reason, label="INVALID"):
    if not ok:
        raise _Refusal(reason, label)


def _map(value, where):
    _require(isinstance(value, dict), where + ": required object")
    return value


def _number(value, where, minimum=None, maximum=None):
    finite = type(value) in (int, float)
    if finite:
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
    _require(finite, where + ": required finite number")
    _require(minimum is None or value >= minimum, where + ": below domain")
    _require(maximum is None or value <= maximum, where + ": above domain")
    return value


def _integer(value, where, minimum=0, maximum=None):
    _require(type(value) is int, where + ": required integer")
    return _number(value, where, minimum, maximum)


def _text(value, where):
    _require(isinstance(value, str) and bool(value), where + ": required string")
    return value


def _sha(value, where):
    _require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None, where + ": required SHA-256")
    return value


def _finite_tree(value, where):
    if type(value) in (int, float):
        _number(value, where)
    elif isinstance(value, dict):
        for key, item in value.items():
            _finite_tree(item, where + "." + str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _finite_tree(item, where + "[%d]" % index)


def _digest(value):
    return hashlib.sha256(json.dumps(value, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _result(label, reason=None):
    return {"label": label, "qualifiers": [], "advance": False,
            "reasons": [] if reason is None else [reason], "descriptors": [],
            "n_eff": None, "H_Y1_credited": False, "process2_status": None,
            "process_labels": [], "counts": [], "reproducibility_status": None,
            "count": None, "baseline_count": None, "required_controls": [],
            "measurement_scope": "MEASUREMENT-ONLY"}


def _recorded(record):
    run = record.get("run", {}) if isinstance(record, dict) else {}
    status = run.get("status") if isinstance(run, dict) else None
    if isinstance(status, str) and (status in ("HALTED", "INVALID", "INCOMPLETE-BUDGET") or status.startswith(("HALTED-", "INVALID-"))):
        return _result(status, run.get("code") or "recorded " + status)
    return None


def _required_arms(record):
    return (A7,) if record.get("stage") == 1 else ARMS


def _complete(record, recipe):
    recipes = record.get("recipes", {}) if isinstance(record, dict) else {}
    if not isinstance(recipes, dict):
        return False
    for name, required in (("A", ARMS), (recipe, _required_arms(record))):
        data = recipes.get(name)
        if not isinstance(data, dict) or data.get("status") != "COMPLETED" or not isinstance(data.get("arms"), dict):
            return False
        if any(not isinstance(data["arms"].get(arm), dict) or data["arms"][arm].get("status") != "COMPLETED" for arm in required):
            return False
    return True


def _input_path(path):
    if any(part.startswith("c10y_directdw_calib") or part == "telemetry" for part in path.parts):
        raise _Refusal("calibration and live telemetry are not scientific reader inputs")
    return path


def _identity(record):
    _require(record.get("schema") == "c10y_directdw/v1", "V11: scientific record schema")
    stage = _integer(record.get("stage"), "V11.stage", 1, 3)
    run = _map(record.get("run"), "V11.run")
    _require(run.get("stage") == stage and run.get("status") == "COMPLETED", "V11: stage outcome")
    _require(all(run.get(key) is True for key in ("launched", "write_complete", "readout_complete")), "V11: incomplete completed-stage flags")
    manifest = _map(record.get("manifest"), "V11.manifest")
    _require(manifest.get("prereg_sha256") == PREREG_SHA, "V11: preregistration identity")
    _sha(manifest.get("H_in"), "V11.H_in")
    parts = _map(manifest.get("parts"), "V11.H_in.parts")
    _require(parts.get("prereg_sha256") == PREREG_SHA, "V11: H_in preregistration identity")
    _require(parts.get("model_id") == "Qwen/Qwen2.5-3B" and parts.get("model_rev") == MODEL_REV and parts.get("device") == "mps", "V11: model/revision/device identity")
    _require(type(parts.get("seed")) is int and parts["seed"] == 0, "V11: frozen seed")
    for key in ("base_artifact_sha256", "tokenizer_artifacts_sha256", "hparams_sha256", "context_templates_sha256"):
        _sha(parts.get(key), "V11.parts." + key)
    covariance = _map(parts.get("covariance_sha256"), "V11.covariance")
    for layer in LAYERS:
        _sha(covariance.get(str(layer)), "V11.covariance.%d" % layer)
    _map(parts.get("tokenizer_settings"), "V11.tokenizer_settings")
    versions = _map(parts.get("library_versions"), "V11.library_versions")
    for key in ("python", "torch", "transformers", "backend"):
        _text(versions.get(key), "V11.library_versions." + key)
    _require(parts.get("objective") == {"KL_coefficient": 0.0625, "routing": True, "parameter_dtype": "float32", "model_dtype": "float16"}, "V11: frozen objective")
    _require(parts.get("optimiser") == {"name": "Adam", "betas": [0.9, 0.999], "eps": 1e-8, "weight_decay": 0, "lr_multiplier": 0.02, "T_max": 100, "loss_scale": 1024, "micro_batches": [6, 6, 6, 6]}, "V11: frozen optimiser")
    _require(parts.get("stage_table") == {"1": "A7-screen", "2": "process1", "3": "process2"}, "V11: frozen stage table")
    requests = _map(parts.get("requests"), "V11.requests")
    for arm in ARMS:
        rows = requests.get(arm)
        _require(isinstance(rows, list) and len(rows) == 24, "V11: 24 ordered requests for " + arm)
        subjects = []
        for row in rows:
            row = _map(row, "V11.request")
            subjects.append(_text(row.get("subject"), "V11.request.subject"))
            _text(row.get("target"), "V11.request.target")
        _require(len(set(subjects)) == 24, "V11: unique request subjects")
    stimuli = _map(parts.get("stimuli"), "V11.stimuli")
    _text(stimuli.get("CANON"), "V11.stimuli.CANON")
    _require(isinstance(stimuli.get("PTEST"), list) and len(stimuli["PTEST"]) == 3 and all(isinstance(s, str) and s for s in stimuli["PTEST"]), "V11: three held-out templates")
    _map(stimuli.get("ARMS"), "V11.stimuli.ARMS")
    paths = _map(parts.get("source_paths"), "V11.source_paths")
    start = _map(manifest.get("sources_start"), "V11.sources_start")
    end = _map(manifest.get("sources_end"), "V11.sources_end")
    declared = _map(parts.get("source_sha256"), "V11.source_sha256")
    _require(start == end == declared, "V11: source drift")
    for key in SOURCES:
        _text(paths.get(key), "V11.source_path." + key)
        _sha(start.get(key), "V11.source_hash." + key)
    _require(start["memit_main"] == ENGINE_SHA and start["prereg"] == PREREG_SHA, "V11: pinned source identity")
    before = _map(manifest.get("input_hashes_start"), "V11.input_hashes_start")
    after = _map(manifest.get("input_hashes_end"), "V11.input_hashes_end")
    _require(before == after, "V11: input drift")
    for key in INPUTS:
        _sha(before.get(key), "V11.input_hash." + key)
    artifacts = _map(manifest.get("artifacts"), "V11.artifacts")
    for name, sha in artifacts.items():
        _text(name, "V11.artifact.path")
        _sha(sha, "V11.artifact.hash")
        _input_path(Path(name))
    _require(any(Path(name).name.startswith("targets_") and name.endswith(".pt") for name in artifacts), "V11: target artifact hash")
    context = _map(manifest.get("context_templates"), "V11.context_templates")
    _text(context.get("path"), "V11.context_templates.path")
    _input_path(Path(context["path"]))
    _require(_sha(context.get("sha256"), "V11.context_templates.sha256") == parts["context_templates_sha256"], "V11: frozen context identity")
    _finite_tree(parts, "V13.H_in.parts")


def _baseline(record):
    instrument = _map(record.get("instrument"), "V1.instrument")
    fingerprint = instrument.get("fingerprint", {})
    _require(isinstance(fingerprint, dict) and fingerprint.get("sha256") == ENGINE_SHA and type(fingerprint.get("cov_cpu_sites")) is int and fingerprint["cov_cpu_sites"] == 3 and isinstance(fingerprint.get("output"), str) and bool(fingerprint["output"].strip()), "V1: fingerprint, three CPU sites and full output", "HALTED")
    baseline = record["recipes"]["A"]["arms"]
    a7 = baseline[A7].get("metrics", {})
    _require(instrument.get("baseline_before_candidates") is True, "V4: baseline did not precede candidates", "HALTED")
    _require(isinstance(a7, dict), "V4: missing baseline metrics", "HALTED")
    for key, lo, hi in (("para_full_n", 5, 18), ("canon_full_n", 5, 10), ("para_first_n", 42, 59)):
        _require(type(a7.get(key)) is int and lo <= a7[key] <= hi, "V4: baseline " + key, "HALTED")
    _require(type(a7.get("para_n")) is int and a7["para_n"] == 72 and type(a7.get("canon_n")) is int and a7["canon_n"] == 24, "V4: baseline denominators", "HALTED")
    for arm in ARMS[:2]:
        metrics = baseline[arm].get("metrics", {})
        _require(isinstance(metrics, dict) and type(metrics.get("para_full_n")) is int and 68 <= metrics["para_full_n"] <= 72 and type(metrics.get("para_n")) is int and metrics["para_n"] == 72, "V4: baseline " + arm, "HALTED")


def _layers(rows, where):
    _require(isinstance(rows, list) and len(rows) == len(LAYERS), where + ": all five layers")
    result = {}
    for row in rows:
        row = _map(row, where)
        layer = row.get("layer")
        _require(type(layer) is int and layer in LAYERS and layer not in result, where + ": unique band layer")
        result[layer] = row
    return result


def _geometry(arm, reference=False, baseline=None):
    rows = _layers(arm.get("geometry"), "V7.geometry")
    reference_rows = _layers(baseline["geometry"], "V7.reference_geometry") if baseline is not None else rows
    for row in rows.values():
        _require(row.get("reduction_dtype") == "float64" and row.get("reduction_device") == "cpu", "V7: CPU float64 geometry")
        for kind in ("planned", "actual"):
            norm = _number(row.get(kind + "_norm"), "V13." + kind + "_norm", 0)
            _number(row.get(kind + "_covariance_energy"), "V13." + kind + "_covariance_energy", 0)
            share = row.get(kind + "_null_share")
            if norm == 0:
                _require(row.get("zero_update") is True, "V7: zero update must be explicit")
                if share is not None:
                    _number(share, "V13.zero_null_share", 0, 1)
            else:
                share = _number(share, "V13." + kind + "_null_share", 0, 1)
                _require(share >= 0.999 or (reference and kind == "planned"), "V7: " + kind + " projector share", "HALTED" if reference and kind == "actual" else "INVALID")
        cosine = row.get("cosine_to_A")
        if cosine is None:
            _require(row["actual_norm"] == 0 or reference_rows[row["layer"]]["actual_norm"] == 0, "V13: unexplained reference cosine null")
        else:
            _number(cosine, "V13.cosine_to_A", -1, 1)
        if row.get("cosine_to_candidate") is not None:
            _number(row["cosine_to_candidate"], "V13.cosine_to_candidate", -1, 1)
        elif "stored_control" in arm:
            _require(row["actual_norm"] == 0, "V13: unexplained stored direction null")
    return rows


def _metrics(arm):
    metrics = _map(arm.get("metrics"), "V13.metrics")
    for key, maximum in (("canon_full_n", 24), ("para_full_n", 72), ("para_first_n", 72), ("para_string_n", 72)):
        _integer(metrics.get(key), "V13." + key, 0, maximum)
    _require(type(metrics.get("canon_n")) is int and metrics["canon_n"] == 24 and type(metrics.get("para_n")) is int and metrics["para_n"] == 72, "V13: readout denominators")
    _require(metrics["para_string_n"] >= metrics["para_full_n"], "V8: string matches below full matches")
    for field, denom_key, reason_key, reason in (("tf_pertok_cont", "tf_pertok_cont_denominator", "tf_pertok_cont_undefined_reason", "zero-continuation-tokens"), ("cond_full_given_first", "cond_full_given_first_denominator", "cond_full_given_first_undefined_reason", "zero-first-token-hits")):
        _require(field in metrics and reason_key in metrics, "V13: required typed diagnostic")
        denominator = _integer(metrics.get(denom_key), "V13." + denom_key)
        if field == "cond_full_given_first":
            _require(denominator == metrics["para_first_n"], "V13: conditional denominator")
        if denominator == 0:
            _require(metrics[field] is None and metrics[reason_key] == reason, "V13: justified diagnostic null")
        else:
            _number(metrics[field], "V13." + field, 0)
            _require(metrics[reason_key] is None, "V13: defined diagnostic has no undefined reason")
    return metrics


def _locality(arm):
    loc = _map(arm.get("locality"), "V13.locality")
    _require(all(type(loc.get(key)) is int and loc[key] == n for key, n in (("L1_n", 12), ("frame_n", 6), ("L3_n", 30))), "V13: locality denominators")
    _integer(loc.get("L1_flips"), "V13.L1_flips", 0, 12)
    flips = _map(loc.get("frame_flips"), "V13.frame_flips")
    for frame in FRAMES:
        _integer(flips.get(frame), "V13.frame." + frame, 0, 6)
    for key in ("described_as_raw", "generic_ppl_raw", "generic_ppl_pre_raw"):
        _number(loc.get(key), "V13." + key, 0)
    _number(loc.get("L3_mean_kl"), "V13.L3_mean_kl")
    _integer(loc.get("L3_agreement"), "V13.L3_agreement", 0, 30)
    relation = _map(loc.get("relation_label_flips"), "V13.relation_label_flips")
    for name in ("associated_with", "is_a"):
        _integer(relation.get(name), "V13.relation." + name, 0, 24)
    return loc


def _flags(arm):
    detail = arm.get("detail")
    _require(isinstance(detail, list) and len(detail) == 24, "V13: complete per-prompt detail")
    flags = {}
    for row in detail:
        row = _map(row, "V13.detail")
        subject = _text(row.get("subj"), "V13.detail.subj")
        _text(row.get("val"), "V13.detail.val")
        _require(type(row.get("canon_full")) is bool and type(row.get("canon_first")) is bool, "V13: canonical flags")
        for name in ("para_full_hits", "para_first_hits"):
            _require(isinstance(row.get(name), list) and len(row[name]) == 3 and all(type(hit) is bool for hit in row[name]), "V13: held-out flags")
        for index, hit in enumerate(row["para_full_hits"]):
            key = (subject, index)
            _require(key not in flags, "V13: duplicate subject/PTEST key")
            flags[key] = hit
    return flags


def _trace(arm, mode):
    trace = _map(arm.get("trace"), "V11.trace")
    _text(trace.get("stop_reason"), "V11.stop_reason")
    _integer(trace.get("accepted_steps"), "V11.accepted_steps", 0, 100)
    _integer(trace.get("overflow_retries"), "V10.overflow_retries", 0, 5)
    _integer(trace.get("loss_scale_halvings"), "V13.loss_scale_halvings")
    _number(trace.get("wall_clock_s"), "V13.wall_clock_s", 0)
    losses, norms = trace.get("loss_components"), trace.get("planned_norms_by_step")
    _require(isinstance(losses, list) and isinstance(norms, list), "V11: write trace")
    _require(mode not in ("anchor", "e2e") or (bool(losses) and bool(norms)), "V11: optimisation trace")
    for row in losses:
        row = _map(row, "V13.loss_components")
        _integer(row.get("accepted_step"), "V13.accepted_step", 0, 100)
        keys = ("total", "L_z") if mode == "anchor" else ("total", "L_edit", "KL_raw", "weighted_KL") if mode == "e2e" else ()
        for key in keys:
            _number(row.get(key), "V13.loss." + key, None if key in ("KL_raw", "weighted_KL") else 0)
    for row in norms:
        _require(isinstance(row, list) and len(row) == 5, "V13: per-step band norms")
        for value in row:
            _number(value, "V13.step_norm", 0)
    memory = _map(trace.get("memory_by_phase"), "V13.memory_by_phase")
    _require(bool(memory), "memory-guard: missing telemetry", "HALTED-RESOURCE")
    for phase, sample in memory.items():
        sample = _map(sample, "V13.memory." + str(phase))
        _require(sample.get("synchronised") is True, "memory-guard: unsynchronised telemetry", "HALTED-RESOURCE")
        driver, _, rss, available = [_integer(sample.get(key), "V13.memory." + key) for key in ("driver_bytes", "current_bytes", "rss_bytes", "host_available_bytes")]
        _require(driver <= 32 * 1024 ** 3 and rss <= 40 * 1024 ** 3 and available >= 8 * 1024 ** 3 and driver + rss <= 40 * 1024 ** 3, "memory-guard: recorded resource threshold", "HALTED-RESOURCE")
    out = _map(arm.get("H_out"), "V11.H_out")
    for key in ("actual_band_sha256", "overlay_sha256"):
        _sha(out.get(key), "V11.H_out." + key)
    tensors = out.get("tensors")
    _require(isinstance(tensors, list) and len(tensors) == 5, "V11: five named update tensors")
    names = set()
    for tensor in tensors:
        tensor = _map(tensor, "V11.H_out.tensor")
        name = _text(tensor.get("name"), "V11.H_out.name")
        _require(name not in names and tensor.get("dtype") == "float32" and tensor.get("shape") == [2048, 11008], "V11: named/dtyped/shaped updates")
        names.add(name)
        _sha(tensor.get("sha256"), "V11.H_out.tensor.sha256")
    _number(arm.get("compile_s"), "V13.compile_s", 0)


def _mode(recipe):
    return "anchor" if recipe == "B-z" else "apply_stored" if recipe in ("B-e2e-NM", "B-e2e-ENV") else "e2e"


def _check_names(mode, arm):
    if mode == "apply_stored":
        return ("scale1", "hooks", "stored_geometry", "merged_readouts")
    names = ["capture", "zero_step", "executed_loop", "projector", "hooks", "train_deploy", "gradient"]
    if arm == A7:
        names.append("accumulation")
        if mode == "e2e":
            names.extend(("objective", "smoke"))
    return names


def _checks(arm, arm_name, mode):
    checks = _map(arm.get("checks"), "V3.checks")
    for name in _check_names(mode, arm_name):
        check = _map(checks.get(name), "V3." + name)
        _require(check.get("passed") is True and check.get("before_result") is True and check.get("scope") == {"mode": mode, "arm": arm_name}, "V3: order/scope/result of " + name)
    reduction = checks["scale1" if mode == "apply_stored" else "capture"]
    floor = _number(reduction.get("floor"), "V13.capture.floor", 0)
    tolerance = max(10 * floor, 1e-4)
    for name in (("scale1",) if mode == "apply_stored" else ("capture", "zero_step", "executed_loop")):
        check = checks[name]
        if name != "capture":
            _require(check.get("counts_equal") is True, "V3: reduced-path counts " + name)
        distances = _map(check.get("distance_by_layer"), "V3.reduction.distances")
        for layer in LAYERS:
            _require(_number(distances.get(str(layer)), "V13.reduction.distance", 0) <= tolerance, "V3: raw reduction distance " + name)
    hooks = checks["hooks"]
    _require(all(hooks.get(key) is True for key in ("registries_equal", "writer_handles_removed", "unknown_hooks_preserved", "pristine_restored", "wrapper_restored", "overrides_restored")), "V3: hooks/restoration")
    if mode == "apply_stored":
        control = _map(arm.get("stored_control"), "V3.stored_control")
        _number(control.get("scale"), "V13.control.scale", 0, 1)
        _require(control.get("source_recipe") == "B-e2e" and control.get("source_arm") == arm_name and control.get("independently_regenerated") is True, "V3: same-arm regenerated stored-update provenance")
        _sha(control.get("source_sha256"), "V11.control.source_sha256")
        _require(arm.get("train_deploy") is None, "V9: stored-hook parity is not applicable")
        return
    loop = checks["executed_loop"]
    _require(type(loop.get("forced_iterations")) is int and loop["forced_iterations"] == 3 and type(loop.get("adam_steps")) is int and loop["adam_steps"] == 3 and _number(loop.get("lr"), "V3.loop.lr") == 0 and loop.get("early_stopping") is False and loop.get("routing_executed") is True and loop.get("accumulation_batches") == [6, 6, 6, 6] and loop.get("loss_scaling_executed") is True, "V3: exact three-step executed-loop identity")
    projector = checks["projector"]
    for name in ("init_planned_share_by_layer", "init_actual_share_by_layer"):
        shares = _map(projector.get(name), "V7." + name)
        zero_layers = projector.get(name.replace("share_by_layer", "zero_layers"), [])
        _require(isinstance(zero_layers, list), "V7: explicit initial zero layers")
        for layer in LAYERS:
            if layer in zero_layers and shares.get(str(layer)) is None:
                continue
            _require(_number(shares.get(str(layer)), "V13.initial_null_share", 0, 1) >= 0.999, "V7: initial projector share")
    gradient = checks["gradient"]
    _require(type(gradient.get("init_loss_scale")) is int and gradient["init_loss_scale"] == 1024, "V3: initial loss scale")
    _integer(gradient.get("halvings"), "V3.gradient.halvings", 0, 3)
    for row in _layers(gradient.get("layers"), "V3.gradient.layers").values():
        _require(row.get("finite") is True and _number(row.get("norm"), "V13.gradient.norm", 0) > 0, "V3: finite nonzero layer gradient")
    _require(all(gradient.get(key) is True for key in ("base_gradients_absent", "only_A_optimised", "eval_mode")) and gradient.get("use_cache") is False, "V3: frozen base and gradient scope")
    if arm_name != A7:
        return
    accumulation = checks["accumulation"]
    _require(accumulation.get("reference_headroom_ok") is True, "V3: accumulation reference headroom", "HALTED-RESOURCE")
    _require(accumulation.get("subset") == list(range(12)) and accumulation.get("splits") == [[6, 6], [5, 7]] and accumulation.get("weighted_by_request_count") is True, "V3: fixed weighted accumulation subset/splits")
    gradients = accumulation.get("gradients")
    _require(isinstance(gradients, list) and len(gradients) == 10, "V3: both five-layer accumulation comparisons")
    pairs = set()
    for row in gradients:
        row = _map(row, "V3.accumulation.gradient")
        key = (row.get("layer"), row.get("split"))
        _require(type(key[0]) is int and key[0] in LAYERS and isinstance(key[1], str) and key[1] in ("6+6", "5+7") and key not in pairs, "V3: accumulation layer/split scope")
        pairs.add(key)
        _require(row.get("finite") is True and _number(row.get("norm"), "V13.accumulation.norm", 0) > 0 and _number(row.get("cosine"), "V13.accumulation.cosine", -1, 1) >= 0.999 and _number(row.get("relative_l2"), "V13.accumulation.relative_l2", 0) <= 0.01, "V3: raw accumulation gradient parity")
    if mode != "e2e":
        return
    objective = checks["objective"]
    errors = objective.get("nll_errors")
    _require(objective.get("constructed_like_compute_z") is True and isinstance(errors, list) and len(errors) == 24, "V3: all 24 compute_z objective constructions")
    for error in errors:
        _require(abs(_number(error, "V13.objective.NLL_error")) <= 0.002, "V3: raw NLL construction error")
    kl = _map(objective.get("KL_errors"), "V3.KL_errors")
    for key in ("init_raw", "init_weighted", "nonzero_raw", "nonzero_weighted"):
        _require(abs(_number(kl.get(key), "V13.objective.KL_error")) <= 0.002, "V3: raw init/nonzero KL construction error")
    smoke = checks["smoke"]
    _require(type(smoke.get("steps")) is int and smoke["steps"] == 3 and all(smoke.get(key) is True for key in ("nonzero_lr", "base_hash_unchanged", "restored", "synchronised")), "V3: three real smoke steps and restoration")
    for key in ("A_changed_layers", "gradient_finite_layers"):
        _require(isinstance(smoke.get(key), list) and len(smoke[key]) == 5 and all(flag is True for flag in smoke[key]), "V3: smoke every layer")
    for key in ("loss_before", "loss_after"):
        _number(smoke.get(key), "V13.smoke." + key, 0)


def _train_deploy(arm, mode):
    if mode == "apply_stored":
        return
    parity = _map(arm.get("train_deploy"), "V9.train_deploy")
    for state in ("init", "final"):
        row = parity.get(state)
        _require(isinstance(row, dict) and row.get("ids_equal") is True and row.get("full_hits_equal") is True, "V9: " + state + " token IDs and hit vectors", "INVALID-TRAIN-DEPLOY-GAP")
        losses = _map(row.get("losses"), "V9.losses")
        for key in (("total", "L_z") if mode == "anchor" else ("total", "L_edit", "KL_raw", "weighted_KL")):
            pair = losses.get(key)
            _require(isinstance(pair, list) and len(pair) == 2, "V9: hooked/merged component pair")
            hooked, merged = [_number(value, "V13.parity." + key) for value in pair]
            _require(abs(hooked - merged) <= max(1e-4, 1e-3 * abs(merged)), "V9: raw " + state + " " + key + " parity", "INVALID-TRAIN-DEPLOY-GAP")


def _override_keys(rows):
    _require(isinstance(rows, list), "V6: override list")
    result = []
    for row in rows:
        row = _map(row, "V6.override")
        subject = _text(row.get("subject"), "V6.override.subject")
        target = _text(row.get("target"), "V6.override.target")
        result.append((subject, target))
    _require(len(set(result)) == len(result), "V6: duplicate declared/consumed override")
    return sorted(result)


def _ledger(record, recipe):
    ledger = record.get("ledger")
    _require(isinstance(ledger, list), "V6: execution ledger")
    calls = {}
    requests = record["manifest"]["parts"]["requests"]
    for entry in ledger:
        entry = _map(entry, "V6.entry")
        key = (entry.get("recipe"), entry.get("arm"), entry.get("check"))
        _require(all(isinstance(item, str) and item for item in key) and key not in calls, "V6: unique separately recorded call")
        calls[key] = entry
        declared = _override_keys(entry.get("declared_overrides"))
        consumed = _override_keys(entry.get("consumed_overrides"))
        if entry.get("status") == "NOT-RUN":
            _require(not consumed and not declared, "V6: NOT-RUN consumed overrides")
            continue
        _require(entry.get("status") == "COMPLETED" and key[1] in requests, "V6: completed call status/arm")
        expected = _override_keys(requests[key[1]])
        _require(declared == consumed and set(declared).issubset(expected), "V6: exact declared/consumed target keys")
        if key[2] == "write":
            stored = key[0] in ("B-e2e-NM", "B-e2e-ENV") and entry.get("mode") == "apply_stored"
            _require(declared == expected or (stored and not declared), "V6: ordinary write must consume full target set")
    for name, required in (("A", ARMS), (recipe, _required_arms(record))):
        for arm in required:
            names = ("write",) if name == "A" else ("write", *tuple(_check_names(_mode(name), arm)))
            for check in names:
                _require(calls.get((name, arm, check), {}).get("status") == "COMPLETED", "V6: missing separate " + name + "/" + arm + "/" + check)
    _finite_tree(ledger, "V13.ledger")


def _matrix(value, where, maximum=None):
    _require(isinstance(value, list) and len(value) == 24 and all(isinstance(row, list) and len(row) == 6 for row in value), where + ": complete 24 by 6 matrix")
    for row in value:
        for item in row:
            _number(item, where, 0, maximum)
    return value


def _fit(arm, mode):
    fit = _map(arm.get("fit"), "V13.fit")
    _require(fit.get("merged") is True, "V13: fit must measure merged model")
    if mode != "anchor":
        matrix = _matrix(fit.get("f_ij"), "V13.f_ij", 1)
        return min(min(row) for row in matrix) >= 0.90 and arm["metrics"]["canon_full_n"] >= 20
    mean = _number(fit.get("L_z"), "V13.L_z", 0)
    ratios = _matrix(fit.get("r_ij"), "V13.r_ij")
    residuals = _matrix(fit.get("residual_norms"), "V13.residual_norms")
    deltas = fit.get("delta_norms")
    _require(isinstance(deltas, list) and len(deltas) == 24, "V13: 24 anchor delta norms")
    for index, delta in enumerate(deltas):
        delta = _number(delta, "V13.delta_norm", 0)
        if delta == 0:
            _require(all(value == 0 for value in residuals[index]), "FIT-Z: zero delta with nonzero residual", "INVALID-ANCHOR-NORMALISATION")
            _require(all(value == 0 for value in ratios[index]), "FIT-Z: explicit zero residual contribution", "INVALID-ANCHOR-NORMALISATION")
    return mean <= 1e-3 and max(max(row) for row in ratios) <= 0.05


def _recipe_validity(record, recipe):
    for name, required in (("A", ARMS), (recipe, _required_arms(record))):
        data = record["recipes"][name]
        law5 = _map(data.get("law5"), "V2." + name)
        _require(law5.get("verdict") == "INERT", "V2: standing LAW5 " + name)
        for key in ("delta_expr", "delta_loc"):
            _number(law5.get(key), "V13.law5." + key)
        for arm_name in required:
            arm = data["arms"][arm_name]
            _metrics(arm)
            _locality(arm)
            _geometry(arm, reference=name == "A", baseline=record["recipes"]["A"]["arms"][arm_name])
            flags = _flags(arm)
            expected_subjects = {row["subject"] for row in record["manifest"]["parts"]["requests"][arm_name]}
            _require({subject for subject, _ in flags} == expected_subjects, "V13: detail keys differ from declared request population")
            _trace(arm, "reference" if name == "A" else _mode(name))
            overlay = "targets_%s.pt" % ("s1" if record["stage"] == 1 else "p%d" % (record["stage"] - 1))
            hout = arm["H_out"]
            _require(hout.get("overlay_artifact") == overlay and hout.get("overlay_member") == ["actual_updates", name, arm_name], "V11: immutable overlay bundle/member")
            _require(hout["overlay_sha256"] == record["manifest"]["artifacts"].get(overlay), "V11: serialized overlay hash")
            _require(hout.get("tensor_certificate_sha256") == _digest(hout["tensors"]), "V11: tensor certificate hash")
            if arm_name in (ARMS[0], A7) and name in ("A", "B-z", "B-e2e"):
                remaining = _map(arm.get("remaining_ratios"), "V13.remaining_ratios")
                _number(remaining.get("canonical"), "V13.remaining.canonical", 0)
                _require(isinstance(remaining.get("heldout"), list) and len(remaining["heldout"]) == 3, "V13: three held-out remaining ratios")
                for value in remaining["heldout"]:
                    _number(value, "V13.remaining.heldout", 0)
            if name != "A":
                _checks(arm, arm_name, _mode(name))
                _train_deploy(arm, _mode(name))
                if record["stage"] != 1 and arm_name in ARMS[:2]:
                    _require(arm["metrics"]["para_full_n"] >= 68, "V5: candidate " + arm_name)
            _finite_tree(arm, "V13." + name + "." + arm_name)


def _locality_failures(candidate, baseline):
    b, a = candidate["locality"], baseline["locality"]
    failures = []
    if b["L1_flips"] > a["L1_flips"] + 1:
        failures.append("G1")
    failures.extend("G2:" + frame for frame in FRAMES if b["frame_flips"][frame] > a["frame_flips"][frame] + 1)
    if b["described_as_raw"] < a["described_as_raw"] - 3:
        failures.append("G3")
    if b["L3_agreement"] < 29:
        failures.append("G4")
    if b["generic_ppl_raw"] > a["generic_ppl_raw"] + 0.5:
        failures.append("G5")
    return failures


def _norms(record, recipe, arm):
    recipes = _map(record.get("recipes"), "R.geometry.recipes")
    arms = _map(_map(recipes.get(recipe), "R.geometry.recipe").get("arms"), "R.geometry.arms")
    data = _map(arms.get(arm), "R.geometry.arm")
    return {layer: _number(row.get("actual_norm"), "R.actual_norm", 0) for layer, row in _layers(data.get("geometry"), "geometry").items()}


def _size(record, recipe):
    ratios, controls = {}, set()
    zero = True
    for arm in _required_arms(record):
        a, b = _norms(record, "A", arm), _norms(record, recipe, arm)
        na, nb = _sum(a.values()), _sum(b.values())
        # PROVISIONAL W1 zero-reference rule: refuse a nonzero numerator.
        _require(na != 0 or nb == 0, "W1: zero baseline size denominator", "INVALID-SIZE-NORMALISATION")
        ratios[arm] = nb / na if na else 1.0
        if arm == A7:
            zero = nb == 0
        if nb > na:
            controls.add("B-e2e-NM")
        if any(b[layer] > a[layer] for layer in LAYERS):
            controls.add("B-e2e-ENV")
    return ratios, [name for name in ("B-e2e-NM", "B-e2e-ENV") if name in controls], zero


def _sum(values):
    try:
        result = math.fsum(values)
    except OverflowError as error:
        raise _Refusal("V13: nonfinite summed actual norm") from error
    return _number(result, "V13.summed_actual_norm", 0)


def _base(record, recipe):
    saved = _recorded(record)
    if saved is not None:
        return saved
    if not isinstance(record, dict) or recipe not in RECIPES:
        return _result("INVALID", "required scientific record and named B recipe")
    if not _complete(record, recipe):
        return _result("INCOMPLETE", "missing own recipe, baseline or V5 arm record")
    try:
        _identity(record)
        _baseline(record)
        audit = _map(record.get("overlap_audit"), "V12.overlap_audit")
        _require(audit.get("clean") is True and audit.get("matches") == [], "V12: write-input leakage", "INVALID-LEAKAGE")
        _text(audit.get("rule"), "V12.overlap_rule")
        _ledger(record, recipe)
        _recipe_validity(record, recipe)
        required = _required_arms(record)
        fit = all([_fit(record["recipes"][recipe]["arms"][arm], _mode(recipe)) for arm in required])
        candidate = record["recipes"][recipe]["arms"][A7]
        baseline = record["recipes"]["A"]["arms"][A7]
        n, a = candidate["metrics"]["para_full_n"], baseline["metrics"]["para_full_n"]
        ratios, controls, zero = _size(record, recipe)
        locality = _locality_failures(candidate, baseline)
        sized = n >= max(19, a + 10)
        large = any(value > 1.5 for value in ratios.values())
        if record["stage"] == 1:
            label = "SCREEN-UNDERFIT" if not fit else "SCREEN-NULL" if not sized else "SCREEN-NOT-ADVANCED" if locality or large else "SCREEN-PASS"
        else:
            label = "UNDERFIT" if not fit else "NULL" if not sized else "TRADEOFF" if locality else "LEAD" if n >= 30 else "PARTIAL"
        result = _result(label)
        result.update(count=n, baseline_count=a, n_eff=n, fit=fit, locality_failures=locality,
                      write_ratios=ratios, write_ratio=ratios[A7], zero_candidate=zero,
                      fit_records={arm: record["recipes"][recipe]["arms"][arm]["fit"] for arm in required},
                      stop_reasons={arm: record["recipes"][recipe]["arms"][arm]["trace"]["stop_reason"] for arm in required},
                      write_geometry={arm: record["recipes"][recipe]["arms"][arm]["geometry"] for arm in required},
                      baseline_geometry={arm: record["recipes"]["A"]["arms"][arm]["geometry"] for arm in required},
                      required_controls=controls if recipe == "B-e2e" and record["stage"] != 1 else [])
        result["reasons"].extend(locality)
        if not fit:
            result["reasons"].append("FIT-Z" if recipe == "B-z" else "FIT-E2E")
        if large:
            result["qualifiers"].append("LARGE-WRITE")
            result["reasons"].append("W1")
        if any(record["recipes"][recipe]["arms"][arm]["compile_s"] >= 3600 for arm in required):
            result["qualifiers"].append("EXCEEDS-TTL")
        if zero:
            result["reasons"].append("all-zero candidate cannot receive positive credit")
        if recipe == "B-z" and abs(n - a) <= 5 and 0.8 <= ratios[A7] <= 1.25:
            result["descriptors"].append("ANCHOR-SHAM-INERT")
        result["advance"] = (label == "SCREEN-PASS" or label in POSITIVE) and not zero and not any(q != "EXCEEDS-TTL" for q in result["qualifiers"])
        return result
    except _Refusal as refusal:
        return _result(refusal.label, str(refusal))


def _control_fidelity(record, recipe):
    for arm in _required_arms(record):
        baseline = _norms(record, "A", arm)
        candidate = _norms(record, "B-e2e", arm)
        control = _norms(record, recipe, arm)
        na, nb, nc = map(_sum, (baseline.values(), candidate.values(), control.values()))
        stored = record["recipes"][recipe]["arms"][arm]["stored_control"]
        if recipe == "B-e2e-NM":
            expected = na / nb if nb > na else 1.0
            if nb > na:
                _require(na * (1. - 0.01) <= nc <= na * (1. + 0.01), "T2: actual NM summed norm within one percent")
        else:
            expected = min([1.0] + [baseline[layer] / candidate[layer] for layer in LAYERS if candidate[layer] != 0])
            _require(all(control[layer] <= 1.01 * baseline[layer] for layer in LAYERS), "T2: actual ENV layer norm")
        _require(stored["scale"] == expected and stored["source_sha256"] == record["recipes"]["B-e2e"]["arms"][arm]["H_out"]["overlay_sha256"], "T2: process-local stored scale and source identity")
        _require("source_process" not in stored or stored["source_process"] == record["stage"], "T2: stored update borrowed from another process")
        for layer, row in _layers(record["recipes"][recipe]["arms"][arm]["geometry"], "T2.geometry").items():
            if control[layer] != 0:
                _require(_number(row.get("cosine_to_candidate"), "V13.control.direction", -1, 1) >= 0.999, "T2: actual stored direction")


def _attribute(record, result, recipe="B-e2e"):
    if recipe != "B-e2e" or not isinstance(record, dict) or record.get("stage") == 1 or result["label"] not in POSITIVE:
        return result
    counts, tested, positive = [], True, True
    for name in result["required_controls"]:
        control = _base(record, name)
        if control.get("fit") is None:
            result["reasons"].extend(name + ": " + str(reason) for reason in control["reasons"])
            tested = False
            continue
        try:
            _control_fidelity(record, name)
        except _Refusal as refusal:
            result["reasons"].append(str(refusal))
            tested = False
            continue
        counts.append(control["count"])
        positive = positive and control["label"] in POSITIVE and control["advance"]
    result["n_eff"] = min(counts) if tested and counts else result["count"] if tested else None
    if not tested:
        result["qualifiers"].append("SIZE-UNTESTED")
    elif not positive:
        result["qualifiers"].append("SIZE-NOT-EXCLUDED")
    if tested and positive and not result["zero_candidate"] and "LARGE-WRITE" not in result["qualifiers"]:
        anchor = _base(record, "B-z")
        if anchor.get("fit") is not True:
            result["qualifiers"].append("ANCHOR-UNTESTED")
        elif result["n_eff"] - anchor["count"] < 10:
            result["qualifiers"].append("ANCHOR-NOT-EXCLUDED")
    result["advance"] = result["advance"] and not any(q != "EXCEEDS-TTL" for q in result["qualifiers"])
    return result


def classify(record, recipe="B-e2e"):
    """Read S/P/V/FIT/G/W/T in frozen order; never perform file IO."""
    return _attribute(record, _base(record, recipe), recipe)


def _disagreement(first, second):
    a, b = _flags(first), _flags(second)
    _require(a.keys() == b.keys(), "R3: identical subject/PTEST keys")
    return sum(a[key] != b[key] for key in a)


def _repro_layers(data, p1, p2, recipe, arm):
    rows = _layers(_map(data, "R1.arm").get("layers"), "R1.layers")
    n1, n2 = _norms(p1, recipe, arm), _norms(p2, recipe, arm)
    for layer, row in rows.items():
        a = _number(row.get("norm_p1"), "R1.norm_p1", 0)
        b = _number(row.get("norm_p2"), "R1.norm_p2", 0)
        _require(a == n1[layer] and b == n2[layer], "R1: actual applied norm identity")
        distance = _number(row.get("distance"), "R1.distance", 0)
        if a == 0 and b == 0:
            _require(distance == 0 and row.get("cosine") in (None, 1.0), "R1: two zero updates are identical")
        else:
            _require(a != 0 and b != 0, "R1: one zero update fails")
            _require(_number(row.get("cosine"), "R1.cosine", -1, 1) >= 0.99 and distance <= 0.10, "R1: fixed actual-update cosine/distance")


def _reproduction(p1, p2, repro, required):
    reasons = []
    try:
        _map(repro, "R: regeneration record")
        _require(repro.get("reduction_dtype") == "float64" and repro.get("reduction_device") == "cpu", "R1: CPU float64 reduction")
        baseline = _map(repro.get("baseline"), "R1.baseline")
        arms = _map(baseline.get("arms"), "R1.baseline.arms")
        for arm in ARMS:
            _repro_layers(arms.get(arm), p1, p2, "A", arm)
    except _Refusal as refusal:
        return "INVALID", [str(refusal)]
    if repro.get("H_in") != p1.get("manifest", {}).get("H_in"):
        reasons.append("R: regeneration H_in mismatch")
    records = repro.get("recipes", {})
    for recipe in required:
        try:
            _map(records, "R1.recipes")
            data = _map(records.get(recipe), "R1." + recipe)
            arms = _map(data.get("arms"), "R1." + recipe + ".arms")
            for arm in ARMS:
                _repro_layers(arms.get(arm), p1, p2, recipe, arm)
            first = p1["recipes"][recipe]["arms"][A7]
            second = p2["recipes"][recipe]["arms"][A7]
            m1, m2 = _map(first.get("metrics"), "R2.p1.metrics"), _map(second.get("metrics"), "R2.p2.metrics")
            _require(abs(_integer(m1.get("para_full_n"), "R2.p1", 0, 72) - _integer(m2.get("para_full_n"), "R2.p2", 0, 72)) <= 5, "R2: count difference exceeds five")
            baseline_disagreement = _disagreement(p1["recipes"]["A"]["arms"][A7], p2["recipes"]["A"]["arms"][A7])
            _require(_disagreement(first, second) <= baseline_disagreement + 3, "R3: disagreement exceeds d_A plus three")
        except _Refusal as refusal:
            reasons.append(recipe + ": " + str(refusal))
    return ("FAIL" if reasons else "PASS"), reasons


def cross_process(p1, p2, repro=None):
    """Read X1–X3, fixed-input R1–R3 and both-process attribution."""
    first = _base(p1, "B-e2e")
    second = _base(p2, "B-e2e") if p2 is not None else _result("NOT-RUN")
    reason_counts = (len(first["reasons"]), len(second["reasons"]))
    run2 = p2.get("run", {}) if isinstance(p2, dict) else {}
    second_status = run2.get("status", second["label"]) if isinstance(run2, dict) else second["label"]
    unavailable = p2 is None or second_status in ("NOT-RUN", "INCOMPLETE", "INCOMPLETE-BUDGET") or str(second_status).startswith("HALTED") or second["label"] == "INCOMPLETE"
    result = _result(first["label"] if unavailable or first["label"] == second["label"] else "MIXED-NOT-REPLICATED")
    result.update(process2_status=second_status, process_labels=[first["label"], second["label"]],
                  counts=[first["count"], second["count"]], n_eff=first["n_eff"],
                  reasons=first["reasons"] + second["reasons"],
                  qualifiers=list(dict.fromkeys(first["qualifiers"] + second["qualifiers"])))
    if unavailable:
        first = _attribute(p1, first)
        result["n_eff"] = first["n_eff"]
        result["reasons"].extend(first["reasons"][reason_counts[0]:])
        result["qualifiers"] = list(dict.fromkeys(result["qualifiers"] + first["qualifiers"]))
        result["qualifiers"].append("SINGLE-PROCESS")
        return result
    manifest1 = p1.get("manifest", {}) if isinstance(p1, dict) else {}
    manifest2 = p2.get("manifest", {}) if isinstance(p2, dict) else {}
    run1 = p1.get("run", {}) if isinstance(p1, dict) else {}
    identity_ok = isinstance(manifest1, dict) and isinstance(manifest2, dict) and isinstance(run1, dict) and isinstance(run2, dict)
    identity_ok = identity_ok and manifest1.get("H_in") == manifest2.get("H_in") and manifest1.get("parts") == manifest2.get("parts")
    identity_ok = identity_ok and type(run1.get("telemetry")) is bool and type(run2.get("telemetry")) is bool and run1["telemetry"] == run2["telemetry"]
    if not identity_ok:
        result["reasons"].append("R: common H_in and telemetry setting differ")
    required = ["B-e2e"]
    processes = [p if isinstance(p, dict) else {} for p in (p1, p2)]
    if all(isinstance(p.get("recipes"), dict) and isinstance(p["recipes"].get("B-z"), dict) and p["recipes"]["B-z"].get("status") == "COMPLETED" for p in processes):
        required.append("B-z")
    required.extend(name for name in ("B-e2e-NM", "B-e2e-ENV") if name in first["required_controls"] or name in second["required_controls"])
    # An untriggered control uses its own process's evaluated scale-1 candidate.
    # These copies never mutate the original records or borrow another process.
    pair = []
    for process, reading in zip(processes, (first, second)):
        raw_recipes = process.get("recipes", {})
        recipes = dict(raw_recipes) if isinstance(raw_recipes, dict) else {}
        for name in required:
            if name in ("B-e2e-NM", "B-e2e-ENV") and name not in reading["required_controls"]:
                recipes[name] = recipes.get("B-e2e")
        pair.append(dict(process, recipes=recipes))
    status, reasons = _reproduction(pair[0], pair[1], repro, required)
    result["reproducibility_status"] = status if identity_ok or status == "INVALID" else "FAIL"
    result["reasons"].extend(reasons)
    if status != "PASS" or not identity_ok:
        result["qualifiers"].append("NOT-REPRODUCIBLE")
    first, second = _attribute(p1, first), _attribute(p2, second)
    result["n_eff"] = first["n_eff"]
    result["reasons"].extend(first["reasons"][reason_counts[0]:] + second["reasons"][reason_counts[1]:])
    result["qualifiers"] = list(dict.fromkeys(result["qualifiers"] + first["qualifiers"] + second["qualifiers"]))
    result["process_readings"] = [first, second]
    result["advance"] = result["label"] in POSITIVE and first["advance"] and second["advance"] and not any(q != "EXCEEDS-TTL" for q in result["qualifiers"])
    result["H_Y1_credited"] = result["advance"]
    return result


def _strict_json(path):
    _input_path(path)
    def constant(value):
        raise ValueError("nonfinite JSON constant " + value)
    def floating(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("nonfinite JSON number " + value)
        return result
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError("duplicate JSON key " + key)
            result[key] = value
        return result
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_constant=constant, parse_float=floating, object_pairs_hook=pairs)


def _file_sha(path):
    _input_path(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _current_identity(record, out):
    _identity(record)
    manifest, root = record["manifest"], Path(ROOT).resolve()
    _require(_digest(manifest["parts"]) == manifest["H_in"], "V11: H_in differs from canonical parts")
    for name, relative in manifest["parts"]["source_paths"].items():
        path = Path(relative)
        path = (root / path).resolve() if not path.is_absolute() else path.resolve()
        _require(path.is_relative_to(root), "V11: source path outside call-time ROOT")
        _require(_file_sha(path) == manifest["sources_end"].get(name), "V11: current source hash differs: " + name)
    for relative, expected in manifest["artifacts"].items():
        path = Path(relative)
        path = (out / path).resolve() if not path.is_absolute() else path.resolve()
        _require(_file_sha(path) == expected, "V11: current artifact hash differs: " + relative)
    for name in ("context_templates", "common_context"):
        context = manifest.get(name)
        if context is None and name == "common_context":
            continue
        context = _map(context, "V11." + name)
        path = Path(_text(context.get("path"), "V11.context.path"))
        path = (out / path).resolve() if not path.is_absolute() else path.resolve()
        _require(_file_sha(path) == _sha(context.get("sha256"), "V11.context.sha256"), "V11: frozen common context hash differs")


def _supervisor(directory, stage):
    tag = "s1" if stage == 1 else "p%d" % (stage - 1)
    path = directory / ("supervisor_" + tag + ".json")
    if not path.is_file():
        return None
    payload = _strict_json(path)
    _require(isinstance(payload, dict), "supervisor outcome must be an object")
    if isinstance(payload.get("run"), dict):
        record = payload
    else:
        record = {"stage": stage, "run": dict(payload, stage=payload.get("stage", stage)), "recipes": {}}
    _require(_recorded(record) is not None, "supervisor record must retain its budget/halt outcome")
    return record


def load(out):
    """Load latest own-stage evidence, with saved supervisor/halts first.

    Common unsuffixed files belong to stage 1. Later pass records contain their
    own manifest/run/ledger/audit and are never filled from earlier common files.
    """
    out = Path(out).resolve()
    try:
        _input_path(out)
        own_names = {1: "screen.json", 2: "pass_p1.json", 3: "pass_p2.json"}
        if out.is_file():
            directory = out.parent
            stage = next((s for s, name in own_names.items() if out.name == name), None)
            saved = _supervisor(directory, stage) if stage is not None else None
            if saved is not None:
                return saved
            record = _strict_json(out)
        else:
            directory = out
            record = None
            for stage in (3, 2, 1):
                saved = _supervisor(out, stage)
                if saved is not None:
                    return saved
                path = out / own_names[stage]
                if path.is_file():
                    record = _strict_json(path)
                    if _recorded(record) is not None:
                        return record
                    break
            run_path = out / "run.json"
            run = _strict_json(run_path) if run_path.is_file() else None
            if record is None:
                record = {"stage": run.get("stage", 1), "run": run, "recipes": {}} if isinstance(run, dict) else {"stage": 1, "recipes": {}}
            elif isinstance(record, dict) and isinstance(run, dict) and run.get("stage") == record.get("stage") and _recorded({"run": run}) is not None:
                record = dict(record, run=run)
        _require(isinstance(record, dict), "scientific stage record must be an object")
        if _recorded(record) is not None or not _complete(record, "B-e2e"):
            return record
        _current_identity(record, directory)
        return record
    except _Refusal as refusal:
        raise ValueError(str(refusal)) from refusal


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--recipe", choices=RECIPES, default="B-e2e")
    parser.add_argument("--process2", type=Path)
    parser.add_argument("--repro", type=Path)
    args = parser.parse_args(argv)
    try:
        record = load(args.out)
        if args.process2 is not None:
            _require(args.recipe == "B-e2e", "cross-process API reads B-e2e attribution")
            proof = _strict_json(args.repro.resolve()) if args.repro is not None else None
            result = cross_process(record, load(args.process2), proof)
        elif record.get("stage") == 3 and args.recipe == "B-e2e":
            directory = args.out.resolve().parent if args.out.is_file() else args.out.resolve()
            p1 = load(directory / "pass_p1.json") if (directory / "pass_p1.json").is_file() else {"stage": 2, "recipes": {}}
            proof_path = args.repro.resolve() if args.repro is not None else directory / "repro.json"
            proof = _strict_json(proof_path) if proof_path.is_file() else None
            result = cross_process(p1, record, proof)
        else:
            result = classify(record, recipe=args.recipe)
    except (OSError, ValueError, _Refusal) as error:
        print("C10Y_READER_REFUSED " + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, allow_nan=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
