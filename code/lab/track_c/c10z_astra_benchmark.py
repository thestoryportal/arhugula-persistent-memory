import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Read-only MPS timing worker, independent supervisor, and pure ceiling reader."""
import argparse
import datetime
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import platform
import random
import signal
import statistics
import subprocess
import threading
import time
import types
import uuid

ROOT = Path(__file__).resolve().parents[3]
MODEL_ID = "Qwen/Qwen2.5-3B"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
SOURCE_FILES = (
    "code/lab/track_c/c10z_astra_benchmark.py",
    "code/lab/track_c/c10z_astra_arms.py",
    "code/lab/track_c/c10z_astra_read.py",
    "code/lab/track_c/c10e_bandknob.py",
    "code/configs/hparams/qwen25_3b_memit_hparams.json",
    "code/memit/engine_fingerprint.py",
    "code/memit/vendor/memit/memit_main.py",
)
TEMPLATES = (
    "{}", "The following is a single-choice question from a Chinese. {}",
    "Therefore, we conclude that the sum \\( a_. {}",
    'Because there is no such thing as a "good. {}',
    "I have a list of numbers in Python, and. {}",
    "You are given an array of strings tokens that represents. {}",
)
FALLBACK = {"C01": 9600, "C2": 14400, "C3": 24060,
            "source": "FALLBACK-OPERATOR-CHOSEN", "discretionary": True}


def _require(condition, reason):
    if not condition: raise ValueError(reason)


def _finite(value):
    if type(value) not in (int, float): return False
    try: return math.isfinite(value)
    except OverflowError: return False


def _number(value, positive=False):
    return _finite(value) and (value > 0 if positive else value >= 0)


def _sha(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _object(value, keys, where):
    _require(isinstance(value, dict), where + " must be an object")
    _require(all(k in value for k in keys), where + " missing required key")
    return value


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def _sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda: stream.read(1 << 20), b""): h.update(part)
    return h.hexdigest()


def source_identity(root):
    return {rel: _sha_file(Path(root) / rel) for rel in SOURCE_FILES}


def environment_identity():
    return {"python": platform.python_version(), "machine": platform.machine(), "platform": platform.platform(),
            "torch": importlib.metadata.version("torch"), "transformers": importlib.metadata.version("transformers")}


def quantile(values, q):
    _require(isinstance(values, (list, tuple)) and bool(values), "quantile requires nonempty values")
    _require(all(_finite(v) for v in values), "non-finite or nonnumeric timing")
    _require(_finite(q) and 0 <= q <= 1, "invalid quantile")
    ordered = sorted(values); index = (len(ordered) - 1) * q
    lo = math.floor(index); hi = math.ceil(index)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (index - lo)


def summary(values):
    median = quantile(values, .5)
    return {"median": median, "p90": quantile(values, .9), "p95": quantile(values, .95),
            "max": max(values), "mean": statistics.fmean(values)}


def measurement_record(seconds, seq_len=None, warmup=20, guard_stopped=False):
    raw = list(seconds); lengths = list(seq_len) if seq_len is not None else [1] * len(raw)
    _require(all(_number(v, True) for v in raw), "probe seconds must be finite positive numbers")
    _require(len(raw) == len(lengths) and all(type(v) is int and v > 0 for v in lengths), "probe sequence lengths")
    n = len(raw)
    status = "COMPLETE" if n >= 400 else "CAPPED" if guard_stopped and n >= 200 else "INVALID"
    return {"status": status, "warmup": warmup, "n_timed": n, "seconds": raw, "seq_len": lengths,
            **(summary(raw) if raw else {k: 0. for k in ("median", "p90", "p95", "max", "mean")}),
            "includes_runjson_read": True, "heartbeat_thread": True}


def expected_probe_forwards(record):
    lengths = record["inputs"]["target_lengths"]
    _require(isinstance(lengths, list) and len(lengths) == 24 and
             all(type(t) is int and t > 0 for t in lengths), "A7 target_lengths")
    return 3 * (37 * sum(t * (t - 1) // 2 for t in lengths) + 84)


def validate_record(record):
    r = _object(record, ("schema", "decision_id", "status", "started_at", "finished_at", "wall_cap_s",
                        "worker_soft_cap_s", "reserve_s", "env", "inputs", "phases", "weights_before",
                        "weights_after", "weights_unchanged", "suspect", "outliers", "derived"), "record")
    _require(r["schema"] == "c10z_astra_benchmark/v2" and r["decision_id"] == "D-C10z-budget", "benchmark schema/decision")
    _require(r["status"] in ("COMPLETE", "CAPPED", "INVALID", "INTERRUPTED"), "benchmark status")
    for key in ("started_at", "finished_at"):
        _require(isinstance(r[key], str) and bool(r[key]), "invalid " + key)
        try: stamp = datetime.datetime.fromisoformat(r[key].replace("Z", "+00:00"))
        except ValueError as exc: raise ValueError("invalid " + key) from exc
        _require(stamp.tzinfo is not None, "timestamp requires timezone")
    _require(_number(r["wall_cap_s"], True) and r["wall_cap_s"] == 600 and
             _number(r["worker_soft_cap_s"], True) and r["worker_soft_cap_s"] == 590 and
             _number(r["reserve_s"]), "clock caps/reserve")
    env = _object(r["env"], ("model_id", "model_rev", "device", "dtype", "torch", "transformers", "python",
                            "machine", "platform", "sources", "engine_fingerprint_ok", "script_sha256",
                            "supervisor_pid", "worker_pid"), "env")
    _require(env["model_id"] == MODEL_ID and env["model_rev"] == MODEL_REV, "pinned model identity")
    _require(env["device"] == "mps" and env["dtype"] == "float16", "benchmark device/dtype")
    _require(env["engine_fingerprint_ok"] is True, "engine fingerprint evidence")
    _require(all(isinstance(env[k], str) and bool(env[k]) for k in ("python", "machine", "platform", "torch", "transformers")),
             "environment fields")
    _require(all(type(env[k]) is int and env[k] > 0 for k in ("supervisor_pid", "worker_pid")), "process identities")
    sources = env["sources"]
    _require(isinstance(sources, dict) and set(sources) == set(SOURCE_FILES) and all(_sha(v) for v in sources.values()),
             "source identity schema")
    _require(_sha(env["script_sha256"]) and env["script_sha256"] == sources[SOURCE_FILES[0]], "script identity binding")
    inputs = _object(r["inputs"], ("templates_source", "templates", "templates_sha256", "population_sha256",
                                  "population_counts", "target_lengths", "seq_len_range"), "inputs")
    templates = inputs["templates"]
    _require(inputs["templates_source"] == "experiments/c10q/runs/c10q_stacked/logs_run.log:9" and isinstance(templates, list) and
             len(templates) == 6 and templates[0] == "{}" and all(isinstance(t, str) and bool(t) for t in templates),
             "template population")
    _require(_sha(inputs["templates_sha256"]) and inputs["templates_sha256"] == _digest(templates) and
             _sha(inputs["population_sha256"]), "population/template hashes")
    expected_probe_forwards(r)
    depths = sum(t - 1 for t in inputs["target_lengths"])
    counts = inputs["population_counts"]
    _require(isinstance(counts, dict) and counts == {"F0": 36, "prefix": 36 * depths, "subject_free": depths, "relations": 48}
             and all(type(v) is int for v in counts.values()), "population counts disagree with target lengths")
    seq_range = inputs["seq_len_range"]
    _require(isinstance(seq_range, list) and len(seq_range) == 2 and all(type(v) is int and v > 0 for v in seq_range)
             and seq_range[0] <= seq_range[1], "population sequence length range")
    phases = _object(r["phases"], ("preflight", "load", "pin", "population", "probe_forward", "batch_forward", "eval_A7", "svd"), "phases")
    for name in ("preflight", "load", "pin", "population"):
        p = _object(phases[name], ("status",), name)
        _require(p["status"] in ("COMPLETE", "INVALID", "STARTED", "NOT-STARTED"), name + " status")
    _require(_number(_object(phases["load"], ("seconds",), "load")["seconds"]), "load seconds")
    _require(phases["load"]["status"] != "COMPLETE" or phases["load"]["seconds"] <= 300, "complete load exceeds 300 seconds")
    pin = _object(phases["pin"], ("param_hash_s", "safetensors_hash_s", "before_hash_s"), "pin")
    _require(all(_number(pin[k]) for k in ("param_hash_s", "safetensors_hash_s", "before_hash_s")), "pin seconds")
    probe = _object(phases["probe_forward"], ("status", "warmup", "n_timed", "seconds", "seq_len", "median", "p90",
                                                   "p95", "max", "mean", "includes_runjson_read", "heartbeat_thread"), "probe_forward")
    raw = probe["seconds"]; lengths = probe["seq_len"]; n = probe["n_timed"]
    _require(type(n) is int and n >= 0 and isinstance(raw, list) and isinstance(lengths, list) and
             n == len(raw) == len(lengths), "probe measurement lengths")
    _require(all(_number(v, True) for v in raw) and all(type(v) is int and v > 0 for v in lengths), "probe raw measurements")
    _require(type(probe["warmup"]) is int and 0 <= probe["warmup"] <= 20 and
             (probe["status"] not in ("COMPLETE", "CAPPED") or probe["warmup"] == 20) and
             probe["includes_runjson_read"] is True and probe["heartbeat_thread"] is True, "probe measurement schedule evidence")
    expected = summary(raw) if raw else {k: 0. for k in ("median", "p90", "p95", "max", "mean")}
    _require(all(_number(probe[k]) and probe[k] == value for k, value in expected.items()), "probe summary disagrees with raw seconds")
    status = probe["status"]
    _require(status in ("COMPLETE", "CAPPED", "INVALID", "STARTED", "NOT-STARTED"), "probe status")
    if status in ("COMPLETE", "CAPPED", "INVALID"):
        band = "COMPLETE" if n >= 400 else "CAPPED" if n >= 200 else "INVALID"
        _require(status == band, "probe status band disagrees with n_timed")
    batch = _object(phases["batch_forward"], ("status", "shape", "seconds", "p95"), "batch_forward")
    shape = batch["shape"]
    _require(isinstance(shape, list) and len(shape) == 2 and shape[0] == 144 and
             all(type(v) is int and v > 0 for v in shape), "batch shape")
    _require(isinstance(batch["seconds"], list) and all(_number(v, True) for v in batch["seconds"]), "batch raw seconds")
    _require(_number(batch["p95"]) and batch["p95"] == (quantile(batch["seconds"], .95) if batch["seconds"] else 0.),
             "batch summary disagrees with raw seconds")
    evaluation = _object(phases["eval_A7"], ("status", "seconds", "forwards"), "eval_A7")
    _require(_number(evaluation["seconds"]) and type(evaluation["forwards"]) is int and evaluation["forwards"] == 1392,
             "eval measurements")
    svd = _object(phases["svd"], ("status", "n", "seconds", "seconds_at_least"), "svd")
    _require(type(svd["n"]) is int and svd["n"] == 11008 and _number(svd["seconds"]), "SVD measurements")
    _require(svd["seconds_at_least"] is None or _number(svd["seconds_at_least"]), "SVD lower bound")
    for name in ("batch_forward", "eval_A7", "svd"):
        allowed = {"COMPLETE", "SKIPPED-NO-TIME", "STARTED", "NOT-STARTED"}
        if name == "svd": allowed.add("TIMEOUT")
        _require(isinstance(phases[name]["status"], str) and phases[name]["status"] in allowed, name + " status")
    if batch["status"] == "COMPLETE": _require(len(batch["seconds"]) == 5, "batch requires five timed forwards")
    if batch["status"] == "SKIPPED-NO-TIME": _require(not batch["seconds"], "skipped batch has measurements")
    if evaluation["status"] == "SKIPPED-NO-TIME": _require(evaluation["seconds"] == 0, "skipped eval has measurements")
    if svd["status"] == "TIMEOUT": _require(svd["seconds_at_least"] is not None, "SVD timeout lacks lower bound")
    else: _require(svd["seconds_at_least"] is None, "SVD lower bound without timeout")
    weights = r["weights_before"]
    _require(isinstance(weights, dict) and set(weights) == set(map(str, range(36))) and all(_sha(v) for v in weights.values()),
             "weights_before must bind all 36 layers")
    after = r["weights_after"]
    _require(isinstance(after, list) and bool(after), "weights_after missing")
    for row in after:
        row = _object(row, ("after", "match"), "weights_after row")
        _require(row["after"] in ("probe_forward", "batch_forward", "eval_A7") and row["match"] is True, "weights_after mismatch")
    names = [row["after"] for row in after]
    _require(len(names) == len(set(names)) and "probe_forward" in names and r["weights_unchanged"] is True, "weights unchanged evidence")
    for name in ("batch_forward", "eval_A7"):
        if phases[name]["status"] == "COMPLETE": _require(name in names, "missing weights_after " + name)
    _require(type(r["suspect"]) is bool and type(r["outliers"]) is bool and
             r["suspect"] == (probe["p95"] < .030) and r["outliers"] == (probe["max"] > 5 * probe["p95"]), "timing flags")
    derived = _object(r["derived"], ("source",), "derived")
    if derived["source"] == "REFUSED":
        _require(set(derived) == {"source", "reason"} and isinstance(derived["reason"], str) and bool(derived["reason"]), "REFUSED schema")
    else:
        _require(derived["source"] == "BENCHMARK", "derived source")
        _object(derived, ("reason", "safety_factor", "t_star", "I_pin", "O", "Q", "C01", "C2", "C3", "nominal_supremum_s",
                          "worst_case_s", "c3_sum_s", "stop", "minima_used"), "derived")
        _require(derived["reason"] is None and _number(derived["safety_factor"], True) and derived["safety_factor"] == 1.25 and
                 all(_number(derived[k]) for k in ("t_star", "I_pin", "O", "Q")) and
                 all(_number(derived[k], True) for k in ("C01", "C2", "C3", "nominal_supremum_s", "worst_case_s", "c3_sum_s")) and
                 type(derived["stop"]) is bool and isinstance(derived["minima_used"], list) and
                 all(isinstance(v, str) and bool(v) for v in derived["minima_used"]), "derived field types")
    if r["status"] in ("COMPLETE", "CAPPED"):
        _require(all(phases[k]["status"] == "COMPLETE" for k in ("preflight", "load", "pin", "population")), "incomplete mandatory phase")
        _require(r["status"] == probe["status"], "top status disagrees with probe")
        _require(all(phases[k]["status"] in ("COMPLETE", "SKIPPED-NO-TIME", "TIMEOUT") for k in ("batch_forward", "eval_A7", "svd")),
                 "incomplete optional phase")


def round_up_300(value): return 300 * math.ceil(value / 300)


def _c01_sum(I_pin, t_star, O, Q):
    return I_pin + 2040 + 26680 * t_star + O + 1800 + max(1380, 15798 * t_star) + Q


def ceilings(record):
    if not isinstance(record, dict) or record.get("status") not in ("COMPLETE", "CAPPED"):
        return {"source": "REFUSED", "reason": "benchmark status is not COMPLETE or CAPPED"}
    try: validate_record(record)
    except ValueError as exc: return {"source": "REFUSED", "reason": str(exc)}
    p = record["phases"]; raw = p["probe_forward"]["seconds"]; stats = summary(raw); minima = []
    candidates = [stats["p95"], stats["mean"]]
    if p["eval_A7"]["status"] == "COMPLETE": candidates.append(p["eval_A7"]["seconds"] / 1392)
    t_star = 1.25 * max(candidates)
    pin = p["pin"]
    I_pin = max(120., 1.25 * (p["load"]["seconds"] + sum(pin[k] for k in ("param_hash_s", "safetensors_hash_s", "before_hash_s"))))
    if p["batch_forward"]["status"] == "COMPLETE": O = 1.25 * 20 * quantile(p["batch_forward"]["seconds"], .95)
    else: O = 0.; minima.append("O")
    svd = p["svd"]
    if svd["status"] == "COMPLETE": Q = max(480., 1.25 * 5 * svd["seconds"] + 300)
    elif svd["status"] == "TIMEOUT": Q = max(480., 1.25 * 5 * svd["seconds_at_least"] + 300); minima.append("Q:lower-bound")
    else: Q = 480.; minima.append("Q")
    C01 = max(7200, round_up_300(_c01_sum(I_pin, t_star, O, Q)))
    C2 = max(12600, round_up_300(3780 + 3 * max(1380, 27960 * t_star) + 600))
    C3 = C01 + C2 + 60; nominal = 2 * (C01 + C2)
    return {"source": "BENCHMARK", "reason": None, "safety_factor": 1.25, "t_star": t_star,
            "I_pin": I_pin, "O": O, "Q": Q, "C01": C01, "C2": C2, "C3": C3,
            "nominal_supremum_s": nominal, "worst_case_s": nominal, "c3_sum_s": C01 + C2 + C3,
            "stop": C01 > 10800 or nominal > 55800, "minima_used": minima}


def write_record(path, record):
    data = (json.dumps(record, sort_keys=True, allow_nan=False, indent=2) + "\n").encode()
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with tmp.open("xb") as stream: stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists(): tmp.unlink()


def _driver_module():
    current = sys.modules.get("c10z_astra_arms")
    if current is not None: return current
    main = sys.modules.get("__main__")
    if main is not None and Path(getattr(main, "__file__", "")).name == "c10z_astra_arms.py": return main
    track = str(Path(__file__).resolve().parent)
    if track not in sys.path: sys.path.insert(0, track)
    return importlib.import_module("c10z_astra_arms")


def population_and_batch(H, templates):
    D = _driver_module(); templates = list(templates)
    _require(len(templates) == 6 and templates[0] == "{}", "six templates beginning with identity required")
    state = types.SimpleNamespace(H=H, arms=H.ARMS, templates=templates)
    batch = D.Session.make_batch(state, D.R.A7, [t.format(H.CANON) for t in templates])
    state.batches = {D.R.A7: batch}
    return D.Session.probe_population(state, D.R.A7), batch


def probe_forward_count(population):
    return sum(len(item["target"]) if "target" in item else 1 for items in population.values() for item in items)


def probe_item(H, item, before=None, after=None):
    import torch
    cur = list(item["prompt_ids"]); tokens = []; greedy = "target" in item
    with torch.no_grad():
        for _ in item["target"] if greedy else (None,):
            start = before(cur) if before is not None else None
            logits = H.model(torch.tensor([cur], device=H.DEV), use_cache=False, logits_to_keep=0).logits
            token = int(logits[0, -1].argmax()); tokens.append(token)
            if greedy: cur.append(token)
            if after is not None: after(cur, start)
    return tokens


def _reserve(before_hash_s): return max(30., 3 * before_hash_s + 10.)


def may_start(elapsed, before_hash_s): return elapsed < 590 - _reserve(before_hash_s)


def phase_fits(elapsed, required, before_hash_s): return elapsed + required <= 590 - _reserve(before_hash_s)


def run_probe_phase(H, population, out, t0, before_hash_s, clock=time.monotonic, timer=time.perf_counter):
    items = [item for group in population.values() for item in group]
    _require(bool(items), "probe population is empty")
    random.Random(0).shuffle(items)
    out = Path(out); runpath = out / "run.json"
    write_record(runpath, {"schema": "timing-control", "reading": None, "padding": "x" * 1900})
    stop = threading.Event(); ready = threading.Event(); failures = []
    def heartbeat():
        try:
            while not stop.is_set():
                write_record(out / "heartbeat.json", {"at": clock(), "pid": os.getpid()})
                ready.set()
                if stop.wait(1.): break
        except Exception as exc: failures.append(exc); ready.set()
    thread = threading.Thread(target=heartbeat, name="c10z_benchmark_heartbeat", daemon=True); thread.start()
    raw = []; lengths = []; guarded = False; warmed = 0
    def before(cur):
        _require(thread.is_alive() and not failures, "heartbeat thread failed")
        start = timer()
        _require(runpath.exists(), "timed run.json control is absent")
        json.loads(runpath.read_text())
        return start
    def after(cur, start): raw.append(timer() - start); lengths.append(len(cur))
    try:
        _require(ready.wait(5.) and not failures, "heartbeat did not start")
        for i in range(20):
            if not may_start(clock() - t0, before_hash_s):
                guarded = True; break
            probe_item(H, {"prompt_ids": items[i % len(items)]["prompt_ids"], "first_ids": []})
            warmed += 1
        if not guarded:
            index = 0
            while len(raw) < 400:
                if not may_start(clock() - t0, before_hash_s): guarded = True; break
                probe_item(H, items[index % len(items)], before, after); index += 1
        _require(not failures, "heartbeat failed")
        return measurement_record(raw, lengths, warmup=warmed, guard_stopped=guarded)
    finally:
        stop.set(); thread.join(5.)
        _require(not thread.is_alive(), "heartbeat did not stop")


def _out_directory(out):
    out = Path(out).resolve(); astra = (ROOT / "experiments/c10z/runs/c10z_astra").resolve()
    _require(not out.is_relative_to(astra), "benchmark cannot write inside ASTRA output")
    bench = (ROOT / "experiments/c10z/runs/c10z_astra_benchmark").resolve()
    _require(out.is_relative_to(bench) and out.parent == bench, "benchmark output must be one directory under experiments/c10z/runs/c10z_astra_benchmark")
    return out


def check_out(out):
    out = _out_directory(out)
    _require(not (out / "benchmark.json").exists(), "existing benchmark.json refused")
    return out


def preflight_environment(env): _driver_module().entry_preflight(env)


def _engine_fingerprint():
    spec = importlib.util.spec_from_file_location("c10z_benchmark_fingerprint", ROOT / "code/memit/engine_fingerprint.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.main() == 0


def _check_model(H, injected=False):
    import torch
    _require((str(H.DEV) == "mps" or injected and str(H.DEV) == "cpu") and
             next(H.model.parameters()).dtype == torch.float16, "actual model device/dtype")
    _require(H.model.config.num_hidden_layers == 36, "36-layer model required")
    _require(H.REV == MODEL_REV, "actual model revision differs from pinned revision")


def _hash_weights(H):
    tensor_hash = _driver_module().tensor_hash
    return {str(i): tensor_hash(H.model.model.layers[i].mlp.down_proj.weight) for i in range(36)}


def _blank_record(t0):
    env = environment_identity()
    env.update(model_id=MODEL_ID, model_rev=MODEL_REV, device="mps", dtype="float16", engine_fingerprint_ok=False,
               script_sha256="", sources={}, supervisor_pid=os.getppid(), worker_pid=os.getpid())
    return {"schema": "c10z_astra_benchmark/v2", "decision_id": "D-C10z-budget", "status": "INVALID",
            "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "wall_cap_s": 600,
            "worker_soft_cap_s": 590, "reserve_s": 30., "env": env,
            "inputs": {"templates_source": "experiments/c10q/runs/c10q_stacked/logs_run.log:9", "templates": list(TEMPLATES),
                       "templates_sha256": _digest(list(TEMPLATES)), "population_sha256": "", "population_counts": {},
                       "target_lengths": [], "seq_len_range": [0, 0]},
            "phases": {"preflight": {"status": "NOT-STARTED"}, "load": {"status": "NOT-STARTED", "seconds": 0.},
                       "pin": {"status": "NOT-STARTED", "param_hash_s": 0., "safetensors_hash_s": 0., "before_hash_s": 0.},
                       "population": {"status": "NOT-STARTED"},
                       "probe_forward": {**measurement_record([], []), "status": "NOT-STARTED"},
                       "batch_forward": {"status": "SKIPPED-NO-TIME", "shape": [144, 1], "seconds": [], "p95": 0.},
                       "eval_A7": {"status": "SKIPPED-NO-TIME", "seconds": 0., "forwards": 1392},
                       "svd": {"status": "SKIPPED-NO-TIME", "n": 11008, "seconds": 0., "seconds_at_least": None}},
            "weights_before": {}, "weights_after": [], "weights_unchanged": True, "suspect": True, "outliers": False,
            "derived": {"source": "REFUSED", "reason": "mandatory measurement incomplete"}}


def _set_status(record):
    phases = record["phases"]
    if not record["weights_unchanged"] or any(phases[k]["status"] != "COMPLETE" for k in ("preflight", "load", "pin", "population")):
        record["status"] = "INVALID"
    else:
        record["status"] = phases["probe_forward"]["status"] if phases["probe_forward"]["status"] in ("COMPLETE", "CAPPED") else "INVALID"


def run_worker(out, t0, H=None, clock=time.monotonic, timer=time.perf_counter, sync=None):
    record = _blank_record(t0); out = Path(out); admitted = False; active = "preflight"; injected = H is not None; log = None
    def save():
        _set_status(record); record["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record["derived"] = ceilings(record); write_record(out / "benchmark.json", record)
        if log is not None:
            log.write("C10Z_BENCHMARK_PHASE " + active + " " + record["phases"][active]["status"] + " " + record["status"] + "\n")
            log.flush(); os.fsync(log.fileno())
    def after_weights(phase):
        match = _hash_weights(H) == record["weights_before"]
        record["weights_after"].append({"after": phase, "match": match})
        record["weights_unchanged"] = record["weights_unchanged"] and match
        save()
        return match
    try:
        preflight_environment(os.environ)
        _require(_engine_fingerprint(), "engine fingerprint failed")
        out = check_out(out); out.mkdir(parents=True, exist_ok=True); admitted = True
        log = (out / "benchmark.log").open("a")
        os.environ.update(LLMDB_ROOT=str(ROOT), LLMDB_DEVICE="mps", HF_HOME=str(ROOT / "data/hf_cache"))
        record["env"]["engine_fingerprint_ok"] = True
        record["env"]["sources"] = source_identity(ROOT)
        record["env"]["script_sha256"] = record["env"]["sources"][SOURCE_FILES[0]]
        record["phases"]["preflight"]["status"] = "COMPLETE"; save()
        import torch
        active = "load"; record["phases"][active]["status"] = "STARTED"; save(); started = timer()
        torch.manual_seed(0)
        if H is None: H = importlib.import_module("c10e_bandknob")
        _check_model(H, injected=injected); H.model.config.use_cache = False
        record["env"]["device"] = str(H.DEV)
        if sync is None: sync = torch.mps.synchronize if str(H.DEV) == "mps" else lambda: None
        record["phases"][active].update(status="COMPLETE", seconds=timer() - started)
        if record["phases"][active]["seconds"] > 300:
            record["phases"][active]["status"] = "INVALID"; save(); return 2
        save()
        active = "pin"; record["phases"][active]["status"] = "STARTED"; save()
        started = timer(); tensor_hash = _driver_module().tensor_hash
        parameter_hashes = {name: tensor_hash(p) for name, p in H.model.named_parameters()}
        record["phases"][active]["param_hash_s"] = timer() - started
        _require(bool(parameter_hashes), "no model parameters")
        started = timer(); snapshot = ROOT / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / H.REV
        safetensors = {p.name: _sha_file(p) for p in sorted(snapshot.glob("model*.safetensors"))}
        record["phases"][active]["safetensors_hash_s"] = timer() - started
        _require(bool(safetensors), "no pinned safetensors files")
        started = timer(); record["weights_before"] = _hash_weights(H)
        before_hash_s = timer() - started; record["phases"][active]["before_hash_s"] = before_hash_s
        record["reserve_s"] = _reserve(before_hash_s); record["phases"][active]["status"] = "COMPLETE"; save()
        active = "population"; record["phases"][active]["status"] = "STARTED"; save()
        population, batch = population_and_batch(H, TEMPLATES)
        prompt_lengths = [len(item["prompt_ids"]) for items in population.values() for item in items]
        record["inputs"].update(population_sha256=_digest(population), population_counts={k: len(v) for k, v in population.items()},
                                 target_lengths=list(batch["target_lengths"]), seq_len_range=[min(prompt_lengths), max(prompt_lengths)])
        record["phases"]["batch_forward"]["shape"] = [len(batch["input_ids"]), batch["T_pad"]]
        record["phases"][active]["status"] = "COMPLETE"; save()
        active = "probe_forward"; record["phases"][active]["status"] = "STARTED"; save()
        record["phases"][active] = run_probe_phase(H, population, out, t0, before_hash_s, clock=clock, timer=timer)
        probe = record["phases"][active]; record["suspect"] = probe["p95"] < .030; record["outliers"] = probe["max"] > 5 * probe["p95"]
        save()
        if not after_weights("probe_forward") or probe["status"] == "INVALID": return 2
        def batch_once():
            sync(); began = timer()
            with torch.no_grad():
                H.model(input_ids=torch.tensor(batch["input_ids"], device=H.DEV),
                        attention_mask=torch.tensor(batch["attention_mask"], device=H.DEV), use_cache=False, logits_to_keep=0)
            sync(); return timer() - began
        active = "batch_forward"
        if may_start(clock() - t0, before_hash_s):
            record["phases"][active]["status"] = "STARTED"; save(); first = batch_once()
            if phase_fits(clock() - t0, 2 * 6 * first, before_hash_s):
                values = [batch_once() for _ in range(5)]
                record["phases"][active].update(status="COMPLETE", seconds=values, p95=quantile(values, .95))
            else: record["phases"][active]["status"] = "SKIPPED-NO-TIME"
            if not after_weights(active): return 2
        active = "eval_A7"; needed = 2 * 1392 * max(probe["p95"], probe["mean"])
        if phase_fits(clock() - t0, needed, before_hash_s):
            record["phases"][active]["status"] = "STARTED"; save(); sync(); started = timer()
            with torch.no_grad(): H.eval_arm(H.ARMS["A7_coined_coined"])
            sync(); record["phases"][active].update(status="COMPLETE", seconds=timer() - started)
            if not after_weights(active): return 2
        active = "svd"
        if clock() - t0 < 565 and phase_fits(clock() - t0, 0., before_hash_s):
            record["phases"][active]["status"] = "STARTED"; save()
            record["phases"][active] = run_svd_phase(out, t0, clock=clock)
        save(); return 0
    except Exception as exc:
        print("C10Z_BENCHMARK_INVALID " + type(exc).__name__ + ": " + str(exc), flush=True)
        record["phases"][active]["status"] = "INVALID"
        record["error"] = {"phase": active, "type": type(exc).__name__, "detail": str(exc)}
        record["status"] = "INVALID"; record["derived"] = {"source": "REFUSED", "reason": str(exc) or type(exc).__name__}
        record["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if admitted: write_record(out / "benchmark.json", record)
        return 2
    finally:
        if log is not None: log.close()


def run_svd_phase(out, t0, clock=time.monotonic, popen=subprocess.Popen, sleep=time.sleep):
    path = Path(out) / "svd_child.json"; started = clock()
    child = popen([sys.executable, "-B", str(Path(__file__).resolve()), "--svd-child", str(path)],
                  stdin=subprocess.DEVNULL)
    while child.poll() is None:
        if clock() - t0 >= 565:
            child.kill(); child.wait()
            return {"status": "TIMEOUT", "n": 11008, "seconds": 0., "seconds_at_least": clock() - started}
        sleep(.1)
    _require(child.returncode == 0, "SVD child failed: " + str(child.returncode))
    value = json.loads(path.read_bytes()); _require(_number(value.get("seconds")), "invalid SVD child timing")
    return {"status": "COMPLETE", "n": 11008, "seconds": value["seconds"], "seconds_at_least": None}


def svd_child(path):
    import torch
    torch.manual_seed(0); X = torch.randn(11008, 11008, dtype=torch.float32, device="cpu")
    A = (X + X.T) / 2; started = time.perf_counter()
    torch.linalg.svd(A, full_matrices=False)
    write_record(path, {"seconds": time.perf_counter() - started})
    return 0


def supervise(worker_cmd, out, cap_s=600., clock=time.monotonic, popen=subprocess.Popen, sleep=time.sleep):
    T0 = clock()
    path = Path(out) / "benchmark.json"; existing = path.exists()
    child = popen(list(worker_cmd) + ["--t0", repr(T0)], start_new_session=True, stdin=subprocess.DEVNULL)
    while child.poll() is None:
        if clock() >= T0 + cap_s:
            os.killpg(child.pid, signal.SIGKILL); child.wait()
            _out_directory(out)
            _require(not existing, "existing benchmark.json refused")
            record = json.loads(path.read_bytes()) if path.exists() else _blank_record(T0)
            record["status"] = "INTERRUPTED"; record["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            record["derived"] = {"source": "REFUSED", "reason": "supervisor killed worker at wall cap"}
            write_record(path, record); return 3
        sleep(.25)
    return child.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out"); parser.add_argument("--worker", action="store_true")
    parser.add_argument("--t0", type=float); parser.add_argument("--svd-child")
    args = parser.parse_args()
    import c10z_astra_read as R
    R.require_a1_freeze(ROOT)
    if args.svd_child is not None: return svd_child(args.svd_child)
    if args.out is None: parser.error("--out is required")
    if args.worker:
        if args.t0 is None: parser.error("worker requires --t0")
        return run_worker(args.out, args.t0)
    return supervise([sys.executable, "-B", str(Path(__file__).resolve()), "--worker", "--out", args.out], args.out)


if __name__ == "__main__": sys.exit(main())
