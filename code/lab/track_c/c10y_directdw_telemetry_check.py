import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""C10Y telemetry admission runner and model-free post-run audit (T8/T11)."""
import argparse
import datetime
import importlib
import json
import math
import tempfile
import traceback
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT") or Path(__file__).resolve().parents[2])
TAGS = {1: "s1", 2: "p1", 3: "p2"}
SCIENCE_FILES = {1: "screen.json", 2: "pass_p1.json", 3: "pass_p2.json"}
COMMON = {"kind", "t_utc", "elapsed_s", "cumulative_s", "process", "run_id"}
BAND = {"4", "5", "6", "7", "8"}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _strict_json(data):
    def reject(value):
        raise ValueError("non-finite JSON constant " + value)
    def pairs(items):
        value = {}
        for key, item in items:
            _require(key not in value, "duplicate JSON field " + key)
            value[key] = item
        return value
    def finite_float(text):
        value = float(text)
        _require(math.isfinite(value), "non-finite JSON number " + text)
        return value
    return json.loads(data, parse_constant=reject, parse_float=finite_float, object_pairs_hook=pairs)


def _bounded_path(path):
    path = Path(path)
    _require(path.is_absolute(), "output path must be absolute")
    resolved = path.resolve()
    root = Path(ROOT).resolve()
    base = (root / "results").resolve()
    _require(base.parent == root, "ROOT/results escapes the root through a symlink")
    _require(resolved.is_relative_to(base) and resolved != base,
             "output path escapes ROOT/results")
    return resolved


def _new_file(path):
    _require(not os.path.lexists(path), "refusing existing artifact " + str(path))


def _publish(path, value):
    """Publish complete strict JSON without replacing another publisher's evidence."""
    _new_file(path)
    data = (json.dumps(value, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            raise ValueError("refusing existing artifact " + str(path)) from exc
    finally:
        Path(temporary).unlink()


def _prepare(out, fingerprint):
    out = _bounded_path(out)
    base = (Path(ROOT).resolve() / "results/c10y_directdw_telemetry_inertness").resolve()
    _require(out.parent == base, "inertness output must be one directory under " + str(base))
    _new_file(out / "inertness.json")
    _require((out / "telemetry").resolve().is_relative_to(out), "telemetry directory escapes inertness output")
    A = importlib.import_module("c10y_directdw_arms")
    _require(Path(A.ROOT).resolve() == Path(ROOT).resolve(), "driver ROOT differs from check ROOT")
    preflight = A.preflight(fingerprint=fingerprint)
    return out, A, preflight


def _check(out, H, A, preflight, started_at, diagnostic=None):
    before_sources, before_env = {}, {}
    try:
        with A.phase_context(None,'telemetry_validation'):
            # T8 never calls my_edit, run_recipe, run_law5 or apply_memit_to_model.
            _require(hasattr(H, "hp"), "injected H must provide the frozen hparams")
            _require(list(H.hp.layers) == [4, 5, 6, 7, 8], "inertness band must be layers 4 through 8")
            _require(str(next(H.model.parameters()).device) == str(H.DEV), "declared device differs from the actual model")
            _require(len(H.FICTION) == 24 and len(H.PTEST) == 3, "inertness schedule must have 96 scored prompts")
            before_sources, before_env = A.source_hashes(), A.environment_identity()
            before_weights = A.band_hashes(H, H.hp)
        with A.phase_context(None,'telemetry_inertness'):
            evidence = A.telemetry_mps_inertness_check(out, H)
        with A.phase_context(None,'telemetry_record'):
            after_weights = A.band_hashes(H, H.hp)
            sources, environment = A.source_hashes(), A.environment_identity()
            unchanged = before_weights == after_weights
            _require(isinstance(evidence, dict), "inertness evidence must be an object")
            record = {**evidence, "schema": "c10y_directdw_telemetry_inertness/v1",
                      "decision_id": "D-C10r-rulings-11", "device": str(H.DEV),
                      "weights_unchanged": unchanged, "sources": sources, "env": environment,
                      "band_sha256_before": before_weights, "band_sha256_after": after_weights,
                      "started_at": started_at, "finished_at": _utc()}
            if isinstance(preflight, dict) and "fingerprint" in preflight:
                record["fingerprint"] = preflight["fingerprint"]
            if str(H.DEV) == "cpu":
                record["scope"] = ("CPU stub code-path check only. Live MPS, edited outputs, optimisation loop "
                                   "and resource inertness remain UNVERIFIED.")
            else:
                record["scope"] = ("Equality of pristine generated IDs, flags and gathered logits under this identity only. "
                                   "Edited outputs, optimisation loop and resource inertness on MPS remain UNVERIFIED; "
                                   "the CPU loop proof is separate (T7).")
            valid_inert = all(record.get(key) is True for key in (
                "control_equal", "telemetry_equal", "generated_equal", "telemetry_complete"))
            valid_inert &= type(record.get("answer_calls")) is int and record["answer_calls"] == len(H.FICTION) * (1 + len(H.PTEST))
            valid_inert &= type(record.get("lens_forwards")) is int and record["lens_forwards"] == 2 * len(H.FICTION)
            if (not unchanged or before_sources != sources or before_env != environment
                    or (record.get("verdict") == "INERT" and not valid_inert)):
                record["verdict"] = "INVALID"
        with A.phase_context(None,'telemetry_publication'):
            _publish(out / "inertness.json", record)
            return 0 if unchanged else 2

    except Exception as exc:
        failure=A.exception_fields(exc,'telemetry_inertness')
        code=failure['code']
        if diagnostic is None: raise
        diagnostic=A.diagnostic_path(diagnostic)
        context=out/'context_templates.json'
        context_record={"path":str(context),"sha256":A.sha(context) if context.exists() else A.PINNED_ENGINE_SHA,
                        "hash_basis":"file_bytes" if context.exists() else "expected_engine_form_default_json"}
        A.write_json(diagnostic,{"process":"telemetry_inertness","out":str(out),"code":code,
                                 "context_templates":context_record,"at":_utc(),**failure})
        _publish(out/'inertness.json',{"schema":"c10y_directdw_telemetry_inertness/v1","decision_id":"D-C10r-rulings-11",
            "device":str(H.DEV),"verdict":"INVALID","halt":code,"sources":before_sources,"env":before_env,
            "context_templates":context_record,"started_at":started_at,"finished_at":_utc(),**failure})
        return 2


def run(out, H, fingerprint=None, diagnostic=None):
    """Exercise the admission path with an explicitly injected harness; CPU stubs stay CPU records."""
    started_at = _utc()
    A = importlib.import_module("c10y_directdw_arms")
    with A.phase_context(None,'telemetry_preflight'):
        out, A, preflight = _prepare(out, fingerprint)
    return _check(out, H, A, preflight, started_at, diagnostic)


class _LineError(ValueError):
    def __init__(self, cause, message):
        super().__init__(message)
        self.cause = cause


def _fields(value, required, optional=()):
    if not isinstance(value, dict):
        raise _LineError("MALFORMED", "expected an object")
    extra = set(value) - set(required) - set(optional)
    if extra:
        raise _LineError("UNEXPECTED", "unknown fields: " + ",".join(sorted(extra)))
    if not set(required) <= set(value):
        raise _LineError("MALFORMED", "missing fields: " + ",".join(sorted(set(required) - set(value))))


def _typed(condition, message):
    if not condition:
        raise _LineError("MALFORMED", message)


def _text(value, empty=False):
    _typed(type(value) is str and (empty or bool(value)), "expected a string")


def _integer(value):
    _typed(type(value) is int and value >= 0, "expected a nonnegative integer")


def _number(value, probability=False, nonnegative=True):
    _typed(type(value) in (int, float), "expected a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    _typed(finite, "expected a finite number")
    _typed((not nonnegative or value >= 0) and (not probability or value <= 1), "number outside its range")


def _norms(value, payload=False):
    _fields(value, BAND)
    for item in value.values():
        if payload:
            _fields(item, {"actual", "planned", "ratio_to_A"})
            for norm in item.values():
                _number(norm)
        else:
            _number(item)


def _matrix(value, probability=False):
    _typed(type(value) is list and len(value) == 24, "matrix must have 24 rows")
    for row in value:
        _typed(type(row) is list and len(row) == 6, "matrix must have six columns")
        for item in row:
            _number(item, probability=probability)


def _validate_line(line, tag):
    _typed(isinstance(line, dict), "line must be an object")
    _typed("kind" in line and type(line["kind"]) is str, "missing or mistyped kind")
    kind = line["kind"]
    schemas = {
        "header": ({"schema", "telemetry"}, set()),
        "phase": ({"phase"}, {"recipe", "mode", "arm", "code", "arms"}),
        "opt_step": ({"step", "components", "loss_scale", "retries", "planned_norms"}, set()),
        "target_probs": (set(), {"probabilities", "f_ij", "r_ij"}),
        "write_norms": ({"norms", "recipe", "arm"}, {"harness_fp32"}),
        "logit_lens": ({"layers", "items", "where", "recipe", "arm"}, set()),
        "answer": ({"recipe", "arm", "phase", "subj", "val", "template", "prompt",
                    "target_ids", "generated_ids", "text", "full", "first"}, set()),
    }
    if kind not in schemas:
        raise _LineError("UNEXPECTED", "unknown kind " + kind)
    required, optional = schemas[kind]
    _fields(line, COMMON | required, optional)
    for field in ("t_utc", "process", "run_id"):
        _text(line[field])
    try:
        stamp = datetime.datetime.fromisoformat(line["t_utc"])
    except ValueError as exc:
        raise _LineError("MALFORMED", "invalid UTC timestamp") from exc
    _typed(stamp.utcoffset() == datetime.timedelta(0), "t_utc must have a UTC offset")
    _typed(line["process"] == tag, "line process does not match the stage")
    _number(line["elapsed_s"])
    _number(line["cumulative_s"])
    if kind == "header":
        _typed(line["schema"] == "c10y_directdw_telemetry/v1", "wrong header schema")
        _typed(line["telemetry"] is True, "header telemetry must be true")
    elif kind == "phase":
        for field in ("phase", "recipe", "mode", "arm", "code"):
            if field in line:
                _text(line[field])
        if "arms" in line:
            _typed(type(line["arms"]) is list, "arms must be a list")
            for arm in line["arms"]:
                _text(arm)
    elif kind == "opt_step":
        _integer(line["step"])
        _integer(line["retries"])
        _number(line["loss_scale"])
        _typed(line["loss_scale"] > 0, "loss scale must be positive")
        components = line["components"]
        if isinstance(components, dict) and "L_z" in components:
            _fields(components, {"L_z"})
        else:
            _fields(components, {"L_edit", "KL_raw", "KL_weighted"}, {"L"})
        for item in components.values():
            _number(item, nonnegative=False)
        _norms(line["planned_norms"])
    elif kind == "target_probs":
        _typed("probabilities" in line or "f_ij" in line, "target_probs needs probabilities or f_ij")
        if "probabilities" in line:
            _typed(type(line["probabilities"]) is list, "probabilities must be a list")
            for row in line["probabilities"]:
                _fields(row, {"request", "frame", "position", "p"})
                for field in ("request", "frame", "position"):
                    _integer(row[field])
                _typed(row["request"] < 24 and row["frame"] < 6, "target probability index outside the write")
                _number(row["p"], probability=True)
        for field in ("f_ij", "r_ij"):
            if field in line:
                _matrix(line[field], probability=field == "f_ij")
    elif kind == "write_norms":
        _text(line["recipe"])
        _text(line["arm"])
        _norms(line["norms"], payload=True)
        if "harness_fp32" in line:
            _typed(line["recipe"] == "A", "harness_fp32 is recipe A's labelled exception")
            echo=line["harness_fp32"]
            _typed(type(echo) is dict and set(echo)=={str(layer) for layer in range(4,9)}, "harness norm layers")
            for row in echo.values():
                _typed(type(row) is dict and set(row)=={"delta_norm","weight_norm_before","relative_delta_norm"}, "harness norm fields")
                for value in row.values(): _number(value,nonnegative=True)
    elif kind == "logit_lens":
        for field in ("where", "recipe", "arm"):
            _text(line[field])
        _typed(type(line["layers"]) is list and line["layers"] == [4, 5, 6, 7, 8], "lens layers must be the frozen band")
        for layer in line["layers"]:
            _integer(layer)
        _typed(type(line["items"]) is list and len(line["items"]) == 24, "lens must hold 24 prompts")
        for item in line["items"]:
            _fields(item, {"subj", "prompt", "top"})
            _text(item["subj"])
            _text(item["prompt"])
            _fields(item["top"], BAND)
            for top in item["top"].values():
                _typed(type(top) is list and len(top) == 5, "lens must hold five tokens per layer")
                for token in top:
                    _typed(type(token) is list and len(token) == 3, "lens token must be [id,text,prob]")
                    _integer(token[0])
                    _text(token[1], empty=True)
                    _number(token[2], probability=True)
    else:
        for field in ("recipe", "arm", "phase", "subj", "val", "template", "prompt"):
            _text(line[field])
        _text(line["text"], empty=True)
        for field in ("target_ids", "generated_ids"):
            _typed(type(line[field]) is list and bool(line[field]), "token IDs must be a nonempty list")
            for token in line[field]:
                _integer(token)
        _typed(type(line["full"]) is bool and type(line["first"]) is bool, "answer flags must be booleans")
    return kind


def _expected_answers(science):
    """T11's keys come from the recorded arm.detail, never aggregate counts."""
    manifest = science.get("manifest", {})
    stimuli = manifest.get("parts", {}).get("stimuli", {})
    canon, ptest = stimuli.get("CANON"), stimuli.get("PTEST")
    fiction, arms = stimuli.get("FICTION"), stimuli.get("ARMS")
    _require(type(canon) is str and type(ptest) is list and len(ptest) == 3,
             "science record lacks the four frozen scored templates")
    templates = [canon, *ptest]
    _require(all(type(t) is str and t.count("{}") == 1 for t in templates)
             and len(set(templates)) == 4, "invalid scored templates")
    _require(type(fiction) is list and len(fiction) == 24 and all(type(s) is str for s in fiction)
             and len(set(fiction)) == 24 and isinstance(arms, dict), "science record lacks frozen arm subjects")
    recipes = science.get("recipes")
    _require(isinstance(recipes, dict) and bool(recipes), "science record lacks scored recipes")
    expected, groups = {}, {}
    for recipe, result in recipes.items():
        _require(type(recipe) is str and isinstance(result, dict), "malformed scientific recipe")
        if result.get("status") == "NOT-RUN":
            continue
        _require(isinstance(result.get("arms"), dict), "recipe lacks arm records")
        for arm, data in result["arms"].items():
            _require(type(arm) is str and isinstance(data, dict), "malformed scientific arm")
            if data.get("status") == "NOT-RUN":
                continue
            rows = data.get("detail")
            _require(type(rows) is list and len(rows) == 24 and arm in arms and isinstance(arms[arm], dict),
                     "scored arm must hold 24 detail rows with a frozen arm map")
            group, subjects = [], set()
            for row in rows:
                _require(isinstance(row, dict) and row.get("subj") in fiction,
                         "detail row outside the frozen subjects")
                subj, val = row["subj"], row.get("val")
                _require(subj not in subjects and type(val) is str and arms[arm].get(subj) == val,
                         "duplicate or mismatched scientific subject/value")
                subjects.add(subj)
                fulls, firsts = row.get("para_full_hits"), row.get("para_first_hits")
                _require(type(fulls) is list and type(firsts) is list and len(fulls) == len(firsts) == 3,
                         "detail row lacks the three held-out flags")
                flags = [(row.get("canon_full"), row.get("canon_first")), *zip(fulls, firsts)]
                for template, flags_pair in zip(templates, flags):
                    _require(all(type(flag) is bool for flag in flags_pair), "scientific flags must be booleans")
                    key = (recipe, arm, subj, template)
                    expected[key] = {"flags": tuple(flags_pair), "val": val, "prompt": template.format(subj)}
                    group.append(key)
            _require(subjects == set(fiction), "scored arm's subjects do not match the frozen population")
            groups[(recipe, arm)] = group
    _require(bool(expected), "science record holds no evaluated arm")
    ledger = science.get("ledger")
    _require(type(ledger) is list, "science record lacks the write execution order")
    order = []
    for entry in ledger:
        _require(isinstance(entry, dict), "malformed execution ledger entry")
        group = (entry.get("recipe"), entry.get("arm"))
        if entry.get("check") == "write" and entry.get("status") == "COMPLETED" and group in groups and group not in order:
            order.append(group)
    _require(set(order) == set(groups), "execution ledger does not cover every scored arm")
    return expected, [key for group in order for key in groups[group]]


def _disabled_markers(out, tag):
    logs = out / "logs"
    markers = []
    if logs.exists():
        _require(logs.resolve().is_relative_to(out), "logs directory escapes the stage directory")
        canonical = [logs / ("stage_" + t + ".log") for t in TAGS.values()]
        if any(path.exists() for path in canonical):
            paths = [logs / ("stage_" + tag + ".log")]
        else:
            # A lone captured log beside a single scientific stage is unambiguous.
            # Shared directories use the supervisor's canonical stage_<tag>.log.
            captured = [path for path in logs.rglob("*.log") if path.is_file()]
            stages = [name for name in SCIENCE_FILES.values() if (out / name).exists()]
            paths = captured if len(captured) == len(stages) == 1 else []
        for path in paths:
            _require(path.resolve().is_relative_to(out), "log path escapes the stage directory")
            if path.exists():
                for line in path.read_text().splitlines():
                    if line.startswith("C10Y_TELEMETRY_DISABLED "):
                        markers.append({"path": str(path), "marker": line})
    return markers


def audit(out, stage=1):
    """Model-free T11 audit; science and historical audit files are never rewritten."""
    _require(type(stage) is int and stage in TAGS, "audit stage must be 1, 2 or 3")
    out = _bounded_path(out)
    tag = TAGS[stage]
    target = out / "telemetry" / ("audit_" + tag + ".json")
    _new_file(target)
    science_path = out / SCIENCE_FILES[stage]
    _require(science_path.resolve().is_relative_to(out), "science record path escapes the stage directory")
    # The scientific reader has standard-library imports only; audit never imports arms or torch.
    R = importlib.import_module("c10y_directdw_read")
    _require(Path(R.ROOT).resolve() == Path(ROOT).resolve(), "reader ROOT differs from check ROOT")
    science = R.load(science_path)
    _require(science.get("stage") == stage, "scientific record stage differs from the requested audit")
    expected, order = _expected_answers(science)
    markers = _disabled_markers(out, tag)
    stream_path = out / "telemetry" / ("telemetry_" + tag + ".jsonl")
    _require(stream_path.resolve().is_relative_to(out), "telemetry path escapes the stage directory")
    lines = stream_path.read_text().splitlines() if stream_path.exists() else []
    issues, seen = [], {}
    answers, header_count = 0, 0
    def issue(cause, line, message):
        issues.append({"cause": cause, "line": line, "message": message})
    for index, text in enumerate(lines, 1):
        try:
            line = _strict_json(text)
            kind = _validate_line(line, tag)
        except _LineError as exc:
            issue(exc.cause, index, str(exc))
            continue
        except (ValueError, TypeError) as exc:
            issue("MALFORMED", index, str(exc))
            continue
        if kind == "header":
            header_count += 1
            if index != 1 or header_count != 1:
                issue("MALFORMED", index, "header must be initial and unique")
        elif kind == "answer":
            answers += 1
            key = tuple(line[field] for field in ("recipe", "arm", "subj", "template"))
            if key not in expected:
                issue("UNEXPECTED", index, "answer key outside the scored recipes and arms")
                continue
            if key in seen:
                issue("DUPLICATE", index, "duplicate answer key")
                continue
            seen[key] = index
            recorded = expected[key]
            if (line["full"], line["first"]) != recorded["flags"]:
                issue("MISMATCH", index, "answer flags differ from the scientific detail")
            if line["val"] != recorded["val"] or line["prompt"] != recorded["prompt"]:
                issue("MISMATCH", index, "answer value or formatted prompt differs from the record")
            if (line["full"] != (line["generated_ids"] == line["target_ids"])
                    or line["first"] != (line["generated_ids"][0] == line["target_ids"][0])):
                issue("MISMATCH", index, "answer flags differ from the recorded token IDs")
    if lines and header_count != 1:
        issue("MALFORMED", 0, "one initial header is required")
    missing = [key for key in expected if key not in seen]
    if missing:
        # The recorded V6 writes order the eval_arm traversals. T5 disables all
        # later emissions; an earlier gap cannot be excused by a later marker.
        last = max((i for i, key in enumerate(order) if key in seen), default=-1)
        early_gap = any(key not in seen for key in order[:last + 1])
        issue("DISABLED" if markers and not early_gap else "MISSING", 0,
              "missing expected answers after a declared disable" if markers and not early_gap
              else "missing expected answers without a preceding declared disable")
    if not lines and not missing:
        issue("MALFORMED", 0, "one initial header is required")
    causes = list(dict.fromkeys(item["cause"] for item in issues))
    compromised = any(cause != "DISABLED" for cause in causes)
    record = {"schema": "c10y_directdw_telemetry_audit/v1", "stage": stage,
              "verdict": "FAIL" if causes else "PASS", "causes": causes, "issues": issues,
              "expected_answers": len(expected), "observed_answers": answers,
              "compromised": compromised, "rerun_required": compromised,
              "rerun_telemetry": False if compromised else None,
              "science_record_stands": not compromised,
              "unaudited_keys": [list(key) for key in missing], "disabled_markers": markers,
              "science_path": str(science_path), "telemetry_path": str(stream_path), "audited_at": _utc()}
    _publish(target, record)
    return record


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    auditing = bool(argv and argv[0] == "audit")
    parser = argparse.ArgumentParser(description="C10Y telemetry inertness check or model-free answer audit")
    parser.add_argument("--out", required=True)
    if auditing:
        parser.add_argument("--stage", type=int, choices=(1, 2, 3), default=1)
        args = parser.parse_args(argv[1:])
        result = audit(args.out, args.stage)
        print(json.dumps({"verdict": result["verdict"], "causes": result["causes"]}, allow_nan=False))
        return 0 if result["verdict"] == "PASS" else 2
    parser.add_argument('--halt-diagnostic',type=Path,required=True)
    args = parser.parse_args(argv)
    _require(os.environ.get("C10Y_SELFTEST") != "1", "selftest refuses live harness import")
    started_at = _utc()
    A = importlib.import_module("c10y_directdw_arms")
    with A.phase_context(None,'telemetry_preflight'):
        out, A, preflight = _prepare(args.out, None)
    A.diagnostic_path(args.halt_diagnostic)
    root = Path(ROOT).resolve()
    os.environ.update(LLMDB_ROOT=str(root), MODEL_ID="Qwen/Qwen2.5-3B",
                      MODEL_REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b",
                      HP_BASE=str(root / "code/configs/hparams/qwen25_3b_memit_hparams.json"),
                      HF_HOME=str(root / "data/hf_cache"))
    with A.phase_context(None,'telemetry_model_load'):
        H = importlib.import_module("c10e_bandknob")
    _require(str(H.DEV) == "mps", "live telemetry inertness check requires MPS")
    _require(H.REV == os.environ["MODEL_REV"], "live model revision differs from the frozen model")
    _require(H.model.config.num_hidden_layers == 36, "live model layer count differs from Qwen2.5-3B")
    _require(next(H.model.parameters()).dtype == H.torch.float16, "live model must be fp16")
    H.hp = H.MEMITHyperParams.from_json(str(root / "code/configs/hparams/qwen25_3b_memit_hparams.json"))
    H.find_fact_lookup_idx = H.compute_z.__globals__["find_fact_lookup_idx"]
    return _check(out, H, A, preflight, started_at, args.halt_diagnostic)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("C10Y_TELEMETRY_CHECK_REFUSED phase=" + getattr(exc,'_c10y_phase','telemetry_launch') + "\n" + traceback.format_exc(), file=sys.stderr)
        sys.exit(2)
