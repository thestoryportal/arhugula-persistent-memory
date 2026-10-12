import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""CPU-only, test-first benchmark checks; never load the harness or a model."""
import copy
import hashlib
import importlib.abc
import importlib.util
import json
import math
from pathlib import Path
import signal
import statistics
import subprocess
import tempfile
import threading
import time
import types
import unittest
from unittest import mock


class NoScienceImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"c10e_bandknob", "transformers", "datasets"}:
            raise AssertionError("CPU benchmark selftest refused science import: " + fullname)
        return None


sys.meta_path.insert(0, NoScienceImports())
import torch

ROOT = Path(__file__).resolve().parents[2]
BENCH_PATH = ROOT / "code/lab/track_c/c10z_astra_benchmark.py"
SCRATCH = Path("/private/tmp/c10z_build")
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
_B = None


def benchmark_module():
    global _B
    if _B is None:
        spec = importlib.util.spec_from_file_location("c10z_astra_benchmark", BENCH_PATH)
        _B = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = _B
        spec.loader.exec_module(_B)
    return _B


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def fixture_record(seconds=.056, n=400, root=None, target_lengths=None):
    """Synthetic complete evidence; numeric values are not a live ceiling selection."""
    B = benchmark_module()
    raw = list(seconds) if isinstance(seconds, (list, tuple)) else [seconds] * n
    lengths = list(target_lengths or ([5] * 12 + [6] * 12))
    sources = B.source_identity(root) if root is not None else {p: "a" * 64 for p in SOURCE_FILES}
    env = B.environment_identity()
    env.update(model_id="Qwen/Qwen2.5-3B", model_rev=MODEL_REV, device="mps", dtype="float16",
               engine_fingerprint_ok=True, sources=sources, script_sha256=sources[SOURCE_FILES[0]],
               supervisor_pid=123, worker_pid=124)
    probe = B.measurement_record(raw, [10] * len(raw), warmup=20, guard_stopped=len(raw) < 400)
    record = {
        "schema": "c10z_astra_benchmark/v2", "decision_id": "D-C10z-budget",
        "status": probe["status"], "started_at": "2026-10-07T00:00:00+00:00",
        "finished_at": "2026-10-07T00:00:20+00:00", "wall_cap_s": 600,
        "worker_soft_cap_s": 590, "reserve_s": 30., "env": env,
        "inputs": {"templates_source": "experiments/c10q/runs/c10q_stacked/logs_run.log:9",
                   "templates": list(TEMPLATES), "templates_sha256": digest(list(TEMPLATES)),
                   "population_sha256": "c" * 64,
                   "population_counts": {"F0": 36, "prefix": 36 * sum(t - 1 for t in lengths),
                                         "subject_free": sum(t - 1 for t in lengths), "relations": 48},
                   "target_lengths": lengths, "seq_len_range": [2, 100]},
        "phases": {"preflight": {"status": "COMPLETE"},
                   "load": {"status": "COMPLETE", "seconds": 0.},
                   "pin": {"status": "COMPLETE", "param_hash_s": 0., "safetensors_hash_s": 0.,
                           "before_hash_s": 0.},
                   "population": {"status": "COMPLETE"}, "probe_forward": probe,
                   "batch_forward": {"status": "SKIPPED-NO-TIME", "shape": [144, 20],
                                     "seconds": [], "p95": 0.},
                   "eval_A7": {"status": "SKIPPED-NO-TIME", "seconds": 0., "forwards": 1392},
                   "svd": {"status": "SKIPPED-NO-TIME", "n": 11008, "seconds": 0.,
                           "seconds_at_least": None}},
        "weights_before": {str(i): "d" * 64 for i in range(36)},
        "weights_after": [{"after": "probe_forward", "match": True}], "weights_unchanged": True,
        "suspect": probe["p95"] < .030, "outliers": probe["max"] > 5 * probe["p95"],
        "derived": {"source": "REFUSED", "reason": "fixture pending derivation"},
    }
    record["derived"] = B.ceilings(record)
    B.validate_record(record)
    return record


class Clock:
    def __init__(self, value=0.): self.value = value
    def __call__(self): return self.value
    def advance(self, seconds): self.value += seconds


class StubModel(torch.nn.Module):
    def __init__(self, clock=None, cost=.001, mutate=False):
        super().__init__()
        self.model = torch.nn.Module()
        self.model.layers = torch.nn.ModuleList([torch.nn.Module() for _ in range(36)])
        for layer in self.model.layers:
            layer.mlp = torch.nn.Module()
            layer.mlp.down_proj = torch.nn.Linear(1, 1, bias=False, dtype=torch.float16)
        self.config = types.SimpleNamespace(use_cache=True, num_hidden_layers=36)
        self.clock = clock; self.cost = cost; self.mutate = mutate; self.calls = []
    def forward(self, input_ids, **kwargs):
        if torch.is_grad_enabled(): raise AssertionError("benchmark forward outside no_grad")
        if input_ids.device.type != "cpu": raise AssertionError("test tensor is not CPU")
        self.calls.append((input_ids.tolist(), dict(kwargs)))
        token = (len(self.calls) - 1) % 128
        logits = torch.zeros(input_ids.shape[0], input_ids.shape[1], 128)
        logits[..., token] = 1.
        if self.mutate: self.model.layers[35].mlp.down_proj.weight.add_(1.)
        if self.clock is not None: self.clock.advance(self.cost)
        return types.SimpleNamespace(logits=logits)


def fake_h(lengths=None, clock=None, cost=.001, mutate=False):
    lengths = lengths or ([5] * 12 + [6] * 12)
    subjects = ["F" + str(i) for i in range(24)]
    values = {s: "V" + str(i) for i, s in enumerate(subjects)}
    tok = types.SimpleNamespace(pad_token_id=0)
    class Tokenizer:
        pad_token_id = 0
        def __call__(self, text): return {"input_ids": [1, 2] + [3] * len(text.split())}
    def forbidden(*args, **kwargs): raise AssertionError("writer method called by benchmark")
    H = types.SimpleNamespace(tok=Tokenizer(), FICTION=subjects, CANON="The capital of {} is",
                             ARMS={"A7_coined_coined": values}, DEV="cpu", REV=MODEL_REV,
                             model=StubModel(clock, cost, mutate), eval_calls=0)
    H.tgt_ids = lambda value: [int(value[1:]) + 1] * lengths[int(value[1:])]
    def evaluate(values):
        if torch.is_grad_enabled(): raise AssertionError("eval outside no_grad")
        H.eval_calls += 1
        if clock is not None: clock.advance(.01)
        return {"canon_full_n": 0}
    H.eval_arm = evaluate
    for name in ("my_edit", "run_recipe", "run_law5", "apply_memit_to_model", "compute_z", "compute_P", "get_cov"):
        setattr(H, name, forbidden)
    return H


def driver_module():
    track = str(ROOT / "code/lab/track_c")
    if track not in sys.path: sys.path.insert(0, track)
    import c10z_astra_arms
    return c10z_astra_arms


class Base(unittest.TestCase):
    def setUp(self):
        self.assertTrue(BENCH_PATH.is_file(), "required benchmark implementation is absent")
        self.B = benchmark_module()
        self.tmp = tempfile.TemporaryDirectory(prefix="benchmark_test_", dir=SCRATCH)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
    def tree(self):
        for i, rel in enumerate(SOURCE_FILES):
            path = self.root / rel; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(("fixture source " + str(i)).encode())
        snapshot = self.root / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / MODEL_REV
        snapshot.mkdir(parents=True)
        (snapshot / "model-00001-of-00001.safetensors").write_bytes(b"synthetic pinned file")
    def worker(self, H, clock=None, **over):
        clock = clock or Clock()
        self.tree()
        out = self.root / "experiments/c10z/runs/c10z_astra_benchmark/test"
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(
                self.B, "_engine_fingerprint", return_value=True), mock.patch.dict(os.environ, {}, clear=True):
            return self.B.run_worker(out, 0., H=H, clock=clock, timer=clock, sync=lambda: None, **over), out


class BenchmarkPopulationTests(Base):
    def test_population_batch_and_digest_match_driver(self):
        D = driver_module(); H = fake_h()
        population, batch = self.B.population_and_batch(H, TEMPLATES)
        state = types.SimpleNamespace(H=H, arms=H.ARMS, templates=list(TEMPLATES))
        expected_batch = D.Session.make_batch(state, D.R.A7, [t.format(H.CANON) for t in TEMPLATES])
        state.batches = {D.R.A7: expected_batch}
        expected = D.Session.probe_population(state, D.R.A7)
        self.assertEqual(batch, expected_batch); self.assertEqual(population, expected)
        self.assertEqual(D.R.json_digest(population), digest(population))
        self.assertEqual({k: len(v) for k, v in population.items()},
                         {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48})
        self.assertEqual(len(batch["input_ids"]), 144)

    def test_full_population_forward_counts(self):
        for lengths, expected in (([5] * 12 + [6] * 12, 11184), ([4] * 6 + [6] * 18, 11406)):
            with self.subTest(lengths=lengths):
                population, _ = self.B.population_and_batch(fake_h(lengths), TEMPLATES)
                independent = sum(len(item["target"]) if "target" in item else 1
                                  for items in population.values() for item in items)
                self.assertEqual(independent, expected)
                self.assertEqual(self.B.probe_forward_count(population), expected)

    def test_greedy_argmax_and_no_grad(self):
        H = fake_h(); item = {"prompt_ids": [9, 8], "target": [99, 99, 99]}
        got = self.B.probe_item(H, item)
        self.assertEqual(got, [0, 1, 2])
        self.assertEqual([ids[0] for ids, _ in H.model.calls], [[9, 8], [9, 8, 0], [9, 8, 0, 1]])
        self.assertTrue(all(k == {"use_cache": False, "logits_to_keep": 0} for _, k in H.model.calls))
        single = self.B.probe_item(H, {"prompt_ids": [9], "first_ids": [4]})
        self.assertEqual(single, [3])

    def test_timed_reads_heartbeat_and_warmup_exclusion(self):
        clock = Clock(); H = fake_h(clock=clock, cost=.001)
        out = self.root / "probe"; out.mkdir()
        population = {"F0": [{"prompt_ids": [2], "first_ids": [1]}] * 500}
        real_read = Path.read_text; real_exists = Path.exists; reads = []; existence = []
        def read(path, *a, **k):
            if path.name == "run.json": reads.append(clock())
            return real_read(path, *a, **k)
        def exists(path):
            if path.name == "run.json": existence.append(clock())
            return real_exists(path)
        with mock.patch.object(Path, "read_text", read), mock.patch.object(Path, "exists", exists):
            phase = self.B.run_probe_phase(H, population, out, 0., 0., clock=clock, timer=clock)
        self.assertEqual(phase["warmup"], 20); self.assertEqual(phase["n_timed"], 400)
        self.assertEqual(len(H.model.calls), 420)
        self.assertEqual(len(reads), 400); self.assertEqual(len(existence), 400)
        self.assertTrue(phase["includes_runjson_read"]); self.assertTrue(phase["heartbeat_thread"])
        self.assertTrue(all(abs(x - .001) < 1e-9 for x in phase["seconds"]))
        heartbeat = json.loads((out / "heartbeat.json").read_text())
        self.assertIn("at", heartbeat)
        self.assertFalse(any(t.name.startswith("c10z_benchmark_heartbeat") for t in threading.enumerate()))

    def test_guarded_loop_completes_item_then_stops(self):
        clock = Clock(); H = fake_h(clock=clock, cost=2.)
        population = {"prefix": [{"prompt_ids": [2], "target": [9, 9, 9]}] * 200}
        out = self.root / "probe"; out.mkdir()
        phase = self.B.run_probe_phase(H, population, out, 0., 0., clock=clock, timer=clock)
        self.assertEqual(phase["status"], "CAPPED")
        self.assertEqual(phase["n_timed"], 261)
        self.assertEqual(len(H.model.calls), 281)
        self.assertEqual(phase["seconds"], [2.] * 261)
        self.assertEqual(H.model.calls[-1][0][0][-2:], [22, 23])

    def test_empty_population_leaves_no_heartbeat(self):
        out = self.root / "probe"; out.mkdir()
        threads = []; stops = []; real_thread = threading.Thread
        def thread(*args, **kwargs):
            target = kwargs["target"]
            for name, cell in zip(target.__code__.co_freevars, target.__closure__ or ()):
                if name == "stop": stops.append(cell.cell_contents)
            child = real_thread(*args, **kwargs); threads.append(child); return child
        try:
            with mock.patch.object(self.B.threading, "Thread", side_effect=thread):
                with self.assertRaisesRegex(ValueError, "probe population is empty"):
                    self.B.run_probe_phase(fake_h(), {}, out, 0., 0.)
            self.assertEqual(threads, [], "empty population must be rejected before heartbeat creation")
            self.assertEqual(list(out.iterdir()), [], "empty population must not create timing artifacts")
        finally:
            for stop in stops: stop.set()
            for child in threads:
                child.join(5.)
                self.assertFalse(child.is_alive(), "failed empty-population test leaked a heartbeat")

    def test_guarded_warmup_records_actual_count(self):
        clock = Clock(559.); H = fake_h(clock=clock, cost=2.)
        out = self.root / "probe"; out.mkdir()
        population = {"F0": [{"prompt_ids": [2], "first_ids": [1]}]}
        phase = self.B.run_probe_phase(H, population, out, 0., 0., clock=clock, timer=clock)
        self.assertEqual(phase["status"], "INVALID"); self.assertEqual(phase["n_timed"], 0)
        self.assertEqual(len(H.model.calls), 1); self.assertEqual(phase["seconds"], [])
        self.assertEqual(phase["warmup"], 1, "guarded warmup must record only completed forwards")
        record = fixture_record(n=0); record["phases"]["probe_forward"] = phase
        self.B.validate_record(record)


class BenchmarkRecordTests(Base):
    def test_quantiles_and_statistics(self):
        for raw in (list(range(1, 101)), [7], [3.] * 5, [1.] * 99 + [10000.]):
            with self.subTest(raw=raw[:3]):
                expected = {}
                for key, q in (("median", .5), ("p90", .9), ("p95", .95)):
                    ordered = sorted(raw); at = (len(raw) - 1) * q; lo = math.floor(at); hi = math.ceil(at)
                    expected[key] = ordered[lo] + (ordered[hi] - ordered[lo]) * (at - lo)
                    self.assertEqual(self.B.quantile(raw, q), expected[key])
                expected.update(max=max(raw), mean=statistics.fmean(raw))
                self.assertEqual(self.B.summary(raw), expected)
        outlier = self.B.summary([1.] * 99 + [10000.])
        self.assertEqual(outlier["p95"], 1.); self.assertEqual(outlier["mean"], 100.99)

    def test_nonfinite_statistics_rejected(self):
        for value in (float("nan"), float("inf"), -float("inf"), True, "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError): self.B.summary([1., value])
                with self.assertRaises(ValueError): self.B.quantile([value], .95)

    def test_huge_integer_timing_is_value_error(self):
        huge = 10 ** 400
        for name, call in (("quantile", lambda: self.B.quantile([huge], .95)),
                           ("summary", lambda: self.B.summary([huge])),
                           ("measurement_record", lambda: self.B.measurement_record([huge], [10]))):
            with self.subTest(api=name), self.assertRaises(ValueError): call()
        for key in ("seconds", "p95"):
            record = fixture_record()
            if key == "seconds": record["phases"]["probe_forward"][key][0] = huge
            else: record["phases"]["probe_forward"][key] = huge
            with self.subTest(field=key), self.assertRaises(ValueError): self.B.validate_record(record)

    def test_optional_status_container_is_value_error(self):
        base = fixture_record()
        for name in ("batch_forward", "eval_A7", "svd"):
            for value in ([], {}):
                record = copy.deepcopy(base); record["phases"][name]["status"] = value
                with self.subTest(phase=name, value=value), self.assertRaisesRegex(ValueError, name + " status"):
                    self.B.validate_record(record)

    def test_probe_status_boundaries(self):
        for n, status in ((199, "INVALID"), (200, "CAPPED"), (201, "CAPPED"),
                          (398, "CAPPED"), (399, "CAPPED"), (400, "COMPLETE"), (401, "COMPLETE")):
            with self.subTest(n=n):
                phase = self.B.measurement_record([.056] * n, [10] * n, warmup=20, guard_stopped=n < 400)
                self.assertEqual(phase["status"], status)
                self.assertEqual(phase["n_timed"], n)
                record = fixture_record(n=n)
                self.assertEqual(record["status"], status)
                self.B.validate_record(record)

    def test_strict_atomic_roundtrip_with_identity(self):
        record = fixture_record(); path = self.root / "benchmark.json"
        self.B.write_record(path, record)
        self.assertEqual(json.loads(path.read_text()), record)
        self.assertEqual(list(self.root.iterdir()), [path])
        self.assertEqual(set(record["env"]["sources"]), set(SOURCE_FILES))
        self.assertIn("target_lengths", record["inputs"])
        self.assertEqual(path.read_bytes(), (json.dumps(record, sort_keys=True, allow_nan=False, indent=2) + "\n").encode())

    def test_nan_preserves_prior_record(self):
        path = self.root / "benchmark.json"; path.write_bytes(b"prior bytes\n")
        with self.assertRaises(ValueError): self.B.write_record(path, {"bad": float("nan")})
        self.assertEqual(path.read_bytes(), b"prior bytes\n")
        self.assertEqual(list(self.root.iterdir()), [path])

    def test_interrupted_replace_preserves_prior_record(self):
        path = self.root / "benchmark.json"; path.write_bytes(b"prior bytes\n")
        with mock.patch.object(self.B.os, "replace", side_effect=OSError("replace interrupted")):
            with self.assertRaisesRegex(OSError, "replace interrupted"):
                self.B.write_record(path, fixture_record())
        self.assertEqual(path.read_bytes(), b"prior bytes\n")
        self.assertEqual(list(self.root.iterdir()), [path])

    def test_schema_missing_keys_and_wrong_types(self):
        base = fixture_record()
        groups = [((), base), (("env",), base["env"]), (("inputs",), base["inputs"]),
                  (("phases",), base["phases"])]
        groups += [(("phases", key), value) for key, value in base["phases"].items()]
        for prefix, values in groups:
            for key in values:
                if key == "guard_stopped": continue
                with self.subTest(missing=prefix + (key,)):
                    r = copy.deepcopy(base); at = r
                    for part in prefix: at = at[part]
                    del at[key]
                    with self.assertRaises(ValueError): self.B.validate_record(r)
        for keys, bad in ((["wall_cap_s"], True), (["worker_soft_cap_s"], "590"),
                          (["reserve_s"], -1), (["env", "worker_pid"], True),
                          (["inputs", "templates"], "{}"), (["inputs", "seq_len_range"], [10, 2]),
                          (["phases", "probe_forward", "n_timed"], True),
                          (["phases", "probe_forward", "seq_len"], [True] * 400),
                          (["phases", "batch_forward", "shape"], [143, 20]),
                          (["phases", "eval_A7", "forwards"], 1391),
                          (["phases", "svd", "n"], 11007), (["phases", "load", "seconds"], float("nan"))):
            with self.subTest(keys=keys, bad=bad):
                r = copy.deepcopy(base); at = r
                for part in keys[:-1]: at = at[part]
                at[keys[-1]] = bad
                with self.assertRaises(ValueError): self.B.validate_record(r)

    def test_measurement_consistency_rejections(self):
        base = fixture_record()
        changes = [("n_timed", 399), ("seconds", [.056] * 399), ("seq_len", [10] * 399),
                   ("status", "CAPPED"), ("warmup", 19), ("includes_runjson_read", False),
                   ("heartbeat_thread", False)] + [(k, 123.) for k in ("median", "p90", "p95", "max", "mean")]
        for key, value in changes:
            with self.subTest(key=key):
                r = copy.deepcopy(base); r["phases"]["probe_forward"][key] = value
                with self.assertRaises(ValueError): self.B.validate_record(r)
        r = fixture_record(n=399); r["phases"]["probe_forward"]["status"] = "COMPLETE"
        with self.assertRaises(ValueError): self.B.validate_record(r)
        for key in ("p95", "seconds"):
            r = copy.deepcopy(base)
            r["phases"]["batch_forward"] = {"status": "COMPLETE", "shape": [144, 20], "seconds": [1.] * 5, "p95": 1.}
            r["weights_after"].append({"after": "batch_forward", "match": True})
            r["phases"]["batch_forward"][key] = 2. if key == "p95" else [1., float("inf")]
            with self.assertRaises(ValueError): self.B.validate_record(r)
        for raw, lengths in (([0.] * 400, [10] * 400), ([-1.] * 400, [10] * 400),
                             ([.056] * 400, [0] * 400), ([.056] * 400, [-1] * 400)):
            r = copy.deepcopy(base); phase = r["phases"]["probe_forward"]
            phase.update(seconds=raw, seq_len=lengths, median=raw[0], p90=raw[0],
                         p95=raw[0], max=raw[0], mean=raw[0])
            with self.assertRaises(ValueError): self.B.validate_record(r)

    def test_weights_device_dtype_revision_fingerprint_rejections(self):
        base = fixture_record()
        for key, value in (("device", "cpu"), ("dtype", "float32"), ("model_rev", "wrong"),
                           ("model_id", "wrong"), ("engine_fingerprint_ok", False)):
            with self.subTest(key=key):
                r = copy.deepcopy(base); r["env"][key] = value
                with self.assertRaises(ValueError): self.B.validate_record(r)
        for edit in (lambda r: r["weights_before"].pop("35"),
                     lambda r: r["weights_before"].update({"36": "d" * 64}),
                     lambda r: r["weights_before"].update({"0": "D" * 64}),
                     lambda r: r.update(weights_after=[]),
                     lambda r: r["weights_after"][0].update(match=False),
                     lambda r: r.update(weights_unchanged=False)):
            r = copy.deepcopy(base); edit(r)
            with self.assertRaises(ValueError): self.B.validate_record(r)

    def test_target_lengths_population_and_probe_counts(self):
        for lengths, expected in (([5] * 12 + [6] * 12, 33552), ([4] * 6 + [6] * 18, 34218)):
            r = fixture_record(target_lengths=lengths)
            self.assertEqual(self.B.expected_probe_forwards(r), expected)
        for lengths in ([5] * 23, [True] + [5] * 23, [0] + [5] * 23, [5.] * 24):
            r = fixture_record(); r["inputs"]["target_lengths"] = lengths
            with self.assertRaises(ValueError): self.B.validate_record(r)
        for key in ("F0", "prefix", "subject_free", "relations"):
            r = fixture_record(); r["inputs"]["population_counts"][key] += 1
            with self.subTest(key=key):
                with self.assertRaises(ValueError): self.B.validate_record(r)


class BenchmarkIdentityTests(Base):
    def test_source_identity_exact_order_and_root(self):
        self.tree()
        got = self.B.source_identity(self.root)
        self.assertEqual(list(got), list(SOURCE_FILES))
        self.assertEqual(got, {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest() for p in SOURCE_FILES})
        (self.root / SOURCE_FILES[1]).write_bytes(b"changed")
        new = self.B.source_identity(self.root)
        self.assertNotEqual(new[SOURCE_FILES[1]], got[SOURCE_FILES[1]])
        self.assertTrue(all(new[p] == got[p] for p in SOURCE_FILES if p != SOURCE_FILES[1]))

    def test_environment_identity_metadata_only(self):
        with mock.patch.object(self.B.platform, "python_version", return_value="P"), mock.patch.object(
                self.B.platform, "machine", return_value="M"), mock.patch.object(
                self.B.platform, "platform", return_value="S"), mock.patch.object(
                self.B.importlib.metadata, "version", side_effect=lambda key: "version:" + key) as versions:
            self.assertEqual(self.B.environment_identity(), {"python": "P", "machine": "M", "platform": "S",
                             "torch": "version:torch", "transformers": "version:transformers"})
        self.assertEqual(versions.call_args_list, [mock.call("torch"), mock.call("transformers")])

    def test_top_level_import_stdlib_only_subprocess(self):
        code = "import sys,importlib.util;before=set(sys.modules);s=importlib.util.spec_from_file_location('bench_check',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);added={n.split('.')[0] for n in set(sys.modules)-before};assert added <= set(sys.stdlib_module_names),added;assert 'c10e_bandknob' not in sys.modules;assert 'torch' not in sys.modules"
        result = subprocess.run([sys.executable, "-B", "-I", "-c", code, str(BENCH_PATH)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_environment_identity_no_torch_subprocess(self):
        code = "import sys,importlib.util,json;s=importlib.util.spec_from_file_location('bench_check',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);x=m.environment_identity();assert set(x)=={'python','machine','platform','torch','transformers'};assert all(isinstance(v,str) and v for v in x.values());assert 'torch' not in sys.modules;assert 'transformers' not in sys.modules;print(json.dumps(x))"
        result = subprocess.run([sys.executable, "-B", "-I", "-c", code, str(BENCH_PATH)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"python", "machine", "platform", "torch", "transformers"})


class BenchmarkCeilingTests(Base):
    def test_eight_v3_calibration_cases(self):
        cases = ((.030, (7200, 12600, 19860)), (.050, (7200, 12600, 19860)),
                 (.070, (7800, 12600, 20460)), (.090, (8400, 12600, 21060)),
                 (.100, (8700, 12900, 21660)), (.117, (9600, 14400, 24060)),
                 (.14625, (10800, 16800, 27660)), (.149, (10800, 17100, 27960)))
        for t, expected in cases:
            with self.subTest(t_star=t):
                d = self.B.ceilings(fixture_record(seconds=t / 1.25))
                self.assertEqual(d["source"], "BENCHMARK")
                self.assertAlmostEqual(d["t_star"], t, places=12)
                self.assertEqual(tuple(d[k] for k in ("C01", "C2", "C3")), expected)
                self.assertEqual(d["worst_case_s"], 2 * (expected[0] + expected[1]))
                self.assertEqual(d["nominal_supremum_s"], d["worst_case_s"])
                self.assertEqual(d["c3_sum_s"], sum(expected)); self.assertFalse(d["stop"])

    def test_raw_values_drive_all_terms(self):
        r = fixture_record(); r["phases"]["probe_forward"].update(p95=100., mean=100.)
        r["phases"]["batch_forward"] = {"status": "COMPLETE", "shape": [144, 20], "seconds": [2.] * 5, "p95": 100.}
        r["weights_after"].append({"after": "batch_forward", "match": True})
        with mock.patch.object(self.B, "validate_record", return_value=None):
            d = self.B.ceilings(r)
        self.assertAlmostEqual(d["t_star"], .070, places=12); self.assertEqual(d["O"], 50.)
        self.assertEqual(d["C01"], 7800)

    def test_mean_outlier_and_complete_eval_tstar(self):
        r = fixture_record(seconds=[1.] * 399 + [10000.])
        d = self.B.ceilings(r)
        self.assertEqual(d["t_star"], 1.25 * statistics.fmean(r["phases"]["probe_forward"]["seconds"]))
        self.assertTrue(d["stop"])
        r = fixture_record(); r["phases"]["eval_A7"] = {"status": "COMPLETE", "seconds": 278.4, "forwards": 1392}
        r["weights_after"].append({"after": "eval_A7", "match": True})
        self.assertAlmostEqual(self.B.ceilings(r)["t_star"], .25, places=12)
        r["phases"]["eval_A7"]["status"] = "SKIPPED-NO-TIME"
        r["phases"]["eval_A7"]["seconds"] = 0.
        self.assertAlmostEqual(self.B.ceilings(r)["t_star"], .070, places=12)

    def test_optional_minima_and_timeout_lower_bound(self):
        r = fixture_record(); d = self.B.ceilings(r)
        self.assertEqual((d["I_pin"], d["O"], d["Q"]), (120., 0., 480.))
        self.assertTrue({"O", "Q"}.issubset(set(d["minima_used"])))
        r["phases"]["svd"] = {"status": "TIMEOUT", "n": 11008, "seconds": 0., "seconds_at_least": 77.}
        d = self.B.ceilings(r)
        self.assertEqual(d["Q"], 781.25); self.assertIn("Q:lower-bound", d["minima_used"])
        r["phases"]["svd"].update(status="COMPLETE", seconds=77., seconds_at_least=None)
        self.assertEqual(self.B.ceilings(r)["Q"], 781.25)
        r["phases"]["load"]["seconds"] = 100.
        r["phases"]["pin"].update(param_hash_s=10., safetensors_hash_s=10., before_hash_s=0.)
        self.assertEqual(self.B.ceilings(r)["I_pin"], 150.)

    def test_refused_records_never_fallback_or_numbers(self):
        base = fixture_record()
        cases = []
        for status in ("INVALID", "INTERRUPTED"):
            r = copy.deepcopy(base); r["status"] = status; cases.append(r)
        for key in ("pin", "probe_forward", "population"):
            r = copy.deepcopy(base); del r["phases"][key]; cases.append(r)
        for key in ("weights_before", "weights_after"):
            r = copy.deepcopy(base); del r[key]; cases.append(r)
        for r in cases:
            with self.subTest(status=r.get("status")):
                d = self.B.ceilings(r)
                self.assertEqual(d["source"], "REFUSED"); self.assertIsInstance(d["reason"], str)
                self.assertTrue(d["reason"]); self.assertFalse(set(d) & {"C01", "C2", "C3", "t_star"})
        self.assertEqual(self.B.FALLBACK, {"C01": 9600, "C2": 14400, "C3": 24060,
                         "source": "FALLBACK-OPERATOR-CHOSEN", "discretionary": True})

    def test_exact_rounding_and_c01_stop_boundary(self):
        self.assertEqual(self.B.round_up_300(10800.), 10800)
        self.assertEqual(self.B.round_up_300(10800.001), 11100)
        for total, cap, stop in ((10800., 10800, False), (10800.001, 11100, True)):
            with self.subTest(total=total), mock.patch.object(self.B, "_c01_sum", return_value=total):
                d = self.B.ceilings(fixture_record())
                self.assertEqual(d["C01"], cap); self.assertEqual(d["stop"], stop)


class BenchmarkLifecycleTests(Base):
    def test_start_and_phase_fit_boundaries(self):
        self.assertTrue(self.B.may_start(559.999, 0.)); self.assertFalse(self.B.may_start(560., 0.))
        self.assertTrue(self.B.phase_fits(500., 60., 0.)); self.assertFalse(self.B.phase_fits(500., 60.001, 0.))
        self.assertTrue(self.B.may_start(549.999, 10.)); self.assertFalse(self.B.may_start(550., 10.))
        self.assertTrue(self.B.phase_fits(500., 50., 10.)); self.assertFalse(self.B.phase_fits(500., 50.001, 10.))

    def test_supervisor_600_boundary_fake_clock(self):
        out = self.root / "experiments/c10z/runs/c10z_astra_benchmark/T"; out.mkdir(parents=True)
        path = out / "benchmark.json"
        clock = Clock(); killed = []; calls = []
        class Child:
            pid = 123456
            def poll(self): return None if not killed else -signal.SIGKILL
            def wait(self, timeout=None): return -signal.SIGKILL
        def pause(seconds):
            clock.value = 599.999 if not calls else 600.
            calls.append(seconds)
        def kill(pid, sig): killed.append((clock(), pid, sig))
        def spawn(*args, **kwargs):
            self.assertTrue(kwargs["start_new_session"])
            self.B.write_record(path, fixture_record())
            return Child()
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(self.B.os, "killpg", side_effect=kill):
            rc = self.B.supervise(["stub"], out, clock=clock, popen=spawn, sleep=pause)
        self.assertEqual(rc, 3); self.assertEqual(killed, [(600., 123456, signal.SIGKILL)])
        self.assertEqual(json.loads(path.read_text())["status"], "INTERRUPTED")

    def test_supervisor_real_process_group_kill_and_interrupted_record(self):
        record = fixture_record(); record["phases"]["probe_forward"]["status"] = "STARTED"
        out = self.root / "experiments/c10z/runs/c10z_astra_benchmark/T"; out.mkdir(parents=True)
        path = out / "benchmark.json"
        progress = json.dumps(record, sort_keys=True, allow_nan=False, indent=2) + "\n"
        code = "import pathlib,sys,time;pathlib.Path(sys.argv[1]).write_bytes(sys.argv[2].encode());time.sleep(1000)"
        children = []; real_popen = subprocess.Popen; real_killpg = os.killpg
        def spawn(*a, **k):
            self.assertTrue(k["start_new_session"])
            child = real_popen(*a, **k); children.append(child); return child
        try:
            started = time.monotonic()
            with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(self.B.os, "killpg", wraps=real_killpg) as kill:
                rc = self.B.supervise([sys.executable, "-B", "-c", code, str(path), progress], out,
                                     cap_s=1.5, popen=spawn)
            elapsed = time.monotonic() - started
            self.assertEqual(rc, 3); self.assertGreaterEqual(elapsed, 1.5); self.assertLessEqual(elapsed, 2.5)
            self.assertIsNotNone(children[0].poll()); kill.assert_called_once_with(children[0].pid, signal.SIGKILL)
            got = json.loads(path.read_text()); self.assertEqual(got["status"], "INTERRUPTED")
            self.assertEqual(got["phases"]["preflight"]["status"], "COMPLETE")
            self.assertEqual(got["phases"]["probe_forward"]["status"], "STARTED")
            self.assertEqual(self.B.ceilings(got)["source"], "REFUSED")
        finally:
            for child in children:
                if child.poll() is None: real_killpg(child.pid, signal.SIGKILL); child.wait(timeout=5)

    def test_supervisor_completed_worker_untouched(self):
        out = self.root / "experiments/c10z/runs/c10z_astra_benchmark/T"; out.mkdir(parents=True)
        path = out / "benchmark.json"
        before = (json.dumps(fixture_record(), sort_keys=True, allow_nan=False, indent=2) + "\n").encode()
        code = "import pathlib,sys;pathlib.Path(sys.argv[1]).write_bytes(sys.argv[2].encode())"
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(self.B.os, "killpg") as kill:
            rc = self.B.supervise([sys.executable, "-B", "-c", code, str(path), before.decode()], out, cap_s=1.5)
        self.assertEqual(rc, 0); kill.assert_not_called(); self.assertEqual(path.read_bytes(), before)

    def test_supervisor_forbidden_astra_cap_preserves_directory(self):
        out = self.root / "experiments/c10z/runs/c10z_astra/timeout"; out.mkdir(parents=True)
        marker = out / "existing.txt"; marker.write_bytes(b"preserved ASTRA fixture\n")
        before = {path.relative_to(out): path.read_bytes() for path in out.iterdir()}
        clock = Clock(); started = []; killed = []
        class Child:
            pid = 123456
            def poll(self): return None if not killed else -signal.SIGKILL
            def wait(self, timeout=None): return -signal.SIGKILL
        def spawn(*args, **kwargs):
            self.assertTrue(kwargs["start_new_session"]); started.append(args); return Child()
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(
                self.B.os, "killpg", side_effect=lambda pid, sig: killed.append((pid, sig))):
            with self.assertRaisesRegex(ValueError, "ASTRA"):
                self.B.supervise(["stub"], out, clock=clock, popen=spawn,
                                 sleep=lambda seconds: clock.advance(600.))
        self.assertEqual(len(started), 1); self.assertEqual(killed, [(123456, signal.SIGKILL)])
        self.assertEqual({path.relative_to(out): path.read_bytes() for path in out.iterdir()}, before)

    def test_supervisor_existing_record_cap_preserves_bytes(self):
        out = self.root / "experiments/c10z/runs/c10z_astra_benchmark/T"; out.mkdir(parents=True)
        path = out / "benchmark.json"; self.B.write_record(path, fixture_record())
        before = path.read_bytes(); clock = Clock(); started = []; killed = []
        class Child:
            pid = 123456
            def poll(self): return None if not killed else -signal.SIGKILL
            def wait(self, timeout=None): return -signal.SIGKILL
        def spawn(*args, **kwargs):
            self.assertTrue(kwargs["start_new_session"]); started.append(args); return Child()
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(
                self.B.os, "killpg", side_effect=lambda pid, sig: killed.append((pid, sig))):
            with self.assertRaisesRegex(ValueError, "existing benchmark.json"):
                self.B.supervise(["stub"], out, clock=clock, popen=spawn,
                                 sleep=lambda seconds: clock.advance(600.))
        self.assertEqual(len(started), 1); self.assertEqual(killed, [(123456, signal.SIGKILL)])
        self.assertEqual(path.read_bytes(), before); self.assertEqual(list(out.iterdir()), [path])

    def test_supervisor_outside_benchmark_cap_preserves_directory(self):
        out = self.root / "results/unrelated/T"; out.mkdir(parents=True)
        marker = out / "existing.txt"; marker.write_bytes(b"preserved unrelated fixture\n")
        before = {path.relative_to(out): path.read_bytes() for path in out.iterdir()}
        clock = Clock(); started = []; killed = []
        class Child:
            pid = 123456
            def poll(self): return None if not killed else -signal.SIGKILL
            def wait(self, timeout=None): return -signal.SIGKILL
        def spawn(*args, **kwargs):
            self.assertTrue(kwargs["start_new_session"]); started.append(args); return Child()
        with mock.patch.object(self.B, "ROOT", self.root), mock.patch.object(
                self.B.os, "killpg", side_effect=lambda pid, sig: killed.append((pid, sig))):
            with self.assertRaisesRegex(ValueError, "benchmark output must be one directory under experiments/c10z/runs/c10z_astra_benchmark"):
                self.B.supervise(["stub"], out, clock=clock, popen=spawn,
                                 sleep=lambda seconds: clock.advance(600.))
        self.assertEqual(len(started), 1); self.assertEqual(killed, [(123456, signal.SIGKILL)])
        self.assertEqual({path.relative_to(out): path.read_bytes() for path in out.iterdir()}, before)

    def test_system_wide_monotonic_subprocess(self):
        before = time.monotonic()
        result = subprocess.run([sys.executable, "-B", "-c", "import time;print(time.monotonic())"],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        child = float(result.stdout); self.assertGreaterEqual(child, before); self.assertLess(child - before, 5.)

    def test_svd_timeout_565_lower_bound_and_worker_survival(self):
        clock = Clock(564.); children = []
        def spawn(*a, **k):
            child = subprocess.Popen([sys.executable, "-B", "-c", "import time;time.sleep(1000)"],
                                     start_new_session=True)
            children.append(child); return child
        try:
            phase = self.B.run_svd_phase(self.root, 0., clock=clock, popen=spawn,
                                         sleep=lambda seconds: clock.advance(1.))
            self.assertEqual(phase["status"], "TIMEOUT"); self.assertGreaterEqual(phase["seconds_at_least"], 1.)
            self.assertEqual(clock(), 565.); self.assertIsNotNone(children[0].poll())
        finally:
            for child in children:
                if child.poll() is None: child.kill(); child.wait(timeout=5)

    def test_worker_svd_timeout_preserves_complete_and_capped(self):
        real_svd = self.B.run_svd_phase; real_probe = self.B.run_probe_phase
        for status in ("COMPLETE", "CAPPED"):
            with self.subTest(status=status), tempfile.TemporaryDirectory(prefix="worker_timeout_", dir=SCRATCH) as tmp:
                old = self.root; self.root = Path(tmp); clock = Clock(); H = fake_h(clock=clock); children = []
                def spawn(*args, **kwargs):
                    self.assertIn("--svd-child", args[0])
                    child = subprocess.Popen([sys.executable, "-B", "-c", "import time;time.sleep(1000)"],
                                             stdin=subprocess.DEVNULL)
                    children.append(child); return child
                def timeout(out, t0, clock):
                    return real_svd(out, t0, clock=clock, popen=spawn,
                                    sleep=lambda seconds: clock.advance(1.))
                def probe(*args, **kwargs):
                    measured = real_probe(*args, **kwargs)
                    if status == "CAPPED":
                        # A synthetic partial measurement reaches both worker status branches.
                        return self.B.measurement_record(measured["seconds"][:200], measured["seq_len"][:200],
                                                         warmup=20, guard_stopped=True)
                    return measured
                try:
                    with mock.patch.object(self.B, "run_svd_phase", side_effect=timeout) as svd, \
                         mock.patch.object(self.B, "run_probe_phase", side_effect=probe):
                        rc, out = self.worker(H, clock)
                    self.assertEqual(rc, 0); svd.assert_called_once()
                    record = json.loads((out / "benchmark.json").read_text())
                    self.assertEqual(record["status"], status)
                    self.assertEqual(record["phases"]["probe_forward"]["status"], status)
                    phase = record["phases"]["svd"]
                    self.assertEqual(phase["status"], "TIMEOUT")
                    self.assertGreater(phase["seconds_at_least"], 0.)
                    self.assertGreaterEqual(clock(), 565.)
                    self.assertEqual(len(children), 1); self.assertIsNotNone(children[0].poll())
                    self.assertTrue(record["weights_unchanged"])
                    self.assertNotIn("error", record)
                finally:
                    self.root = old
                    for child in children:
                        if child.poll() is None: child.kill(); child.wait(timeout=5)

    def test_out_path_refusals_and_prefix_trap(self):
        with mock.patch.object(self.B, "ROOT", self.root):
            for out in (self.root / "experiments/c10z/runs/c10z_astra", self.root / "experiments/c10z/runs/c10z_astra/x"):
                with self.subTest(out=out), self.assertRaisesRegex(ValueError, "ASTRA"):
                    self.B.check_out(out)
                self.assertFalse(out.exists())
            good = self.root / "experiments/c10z/runs/c10z_astra_benchmark/T"
            self.assertEqual(self.B.check_out(good), good.resolve())
            good.mkdir(parents=True); (good / "benchmark.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "existing benchmark.json"): self.B.check_out(good)

    def test_env_preflight_refusals(self):
        D = driver_module()
        for key in D.INHERITED:
            with self.subTest(key=key), self.assertRaisesRegex(D.R.Halt, "inherited C10 knobs"):
                self.B.preflight_environment({key: "1"})
        with self.assertRaisesRegex(D.R.Halt, "MPS"):
            self.B.preflight_environment({"LLMDB_DEVICE": "cpu"})

    def test_injected_worker_full_schedule_no_writer_calls(self):
        clock = Clock(); H = fake_h(clock=clock)
        with mock.patch.object(self.B, "run_svd_phase", return_value={"status": "COMPLETE", "n": 11008,
                "seconds": 1., "seconds_at_least": None}):
            rc, out = self.worker(H, clock)
        self.assertEqual(rc, 0)
        r = json.loads((out / "benchmark.json").read_text())
        self.assertEqual(r["status"], "COMPLETE"); self.assertTrue(r["weights_unchanged"])
        self.assertEqual(len(r["weights_before"]), 36); self.assertTrue(all(x["match"] for x in r["weights_after"]))
        self.assertEqual(r["phases"]["probe_forward"]["warmup"], 20)
        self.assertGreaterEqual(r["phases"]["probe_forward"]["n_timed"], 400)
        self.assertEqual(r["phases"]["batch_forward"]["status"], "COMPLETE")
        self.assertEqual(len(r["phases"]["batch_forward"]["seconds"]), 5)
        self.assertEqual(r["phases"]["eval_A7"]["status"], "COMPLETE"); self.assertEqual(H.eval_calls, 1)
        self.assertFalse(H.model.config.use_cache)
        self.assertEqual(r["inputs"]["target_lengths"], [5] * 12 + [6] * 12)
        self.assertFalse((self.root / "experiments/c10z/runs/c10z_astra").exists())
        self.assertNotIn("c10e_bandknob", sys.modules)

    def test_injected_worker_synthetic_mps_identity_validates_derived(self):
        clock = Clock(); H = fake_h(clock=clock)
        with mock.patch.object(self.B, "run_svd_phase", return_value={"status": "COMPLETE", "n": 11008,
                "seconds": 1., "seconds_at_least": None}):
            rc, out = self.worker(H, clock)
        self.assertEqual(rc, 0)
        path = out / "benchmark.json"; before = path.read_bytes(); record = json.loads(before)
        self.assertEqual(record["env"]["device"], "cpu")
        self.assertEqual(record["derived"]["source"], "REFUSED")
        with self.assertRaisesRegex(ValueError, "device/dtype"): self.B.validate_record(record)
        # Synthetic metadata validates the worker's evidence without allocating an MPS tensor.
        synthetic = copy.deepcopy(record); synthetic["env"]["device"] = "mps"
        synthetic["derived"] = self.B.ceilings(synthetic)
        self.B.validate_record(synthetic)
        self.assertEqual(synthetic["derived"], self.B.ceilings(synthetic))
        self.assertEqual(synthetic["derived"]["source"], "BENCHMARK")
        self.assertTrue(all(p.device.type == "cpu" for p in H.model.parameters()))
        self.assertEqual(path.read_bytes(), before, "synthetic identity must not replace the CPU worker record")

    def test_worker_mutation_invalid_and_refused(self):
        clock = Clock(); H = fake_h(clock=clock, mutate=True)
        with mock.patch.object(self.B, "run_svd_phase") as svd:
            rc, out = self.worker(H, clock)
        self.assertEqual(rc, 2); svd.assert_not_called()
        r = json.loads((out / "benchmark.json").read_text())
        self.assertEqual(r["status"], "INVALID"); self.assertFalse(r["weights_unchanged"])
        self.assertEqual(self.B.ceilings(r)["source"], "REFUSED")

    def test_worker_load_over_300_invalid(self):
        clock = Clock(); H = fake_h(clock=clock)
        def check(model, injected=False): clock.advance(300.001)
        with mock.patch.object(self.B, "_check_model", side_effect=check), mock.patch.object(self.B, "run_svd_phase") as svd:
            rc, out = self.worker(H, clock)
        self.assertEqual(rc, 2); svd.assert_not_called()
        r = json.loads((out / "benchmark.json").read_text())
        self.assertEqual(r["status"], "INVALID"); self.assertEqual(r["phases"]["load"]["status"], "INVALID")
        self.assertEqual(H.model.calls, [])

    def test_worker_guard_status_bands_and_reserved_after_hash(self):
        for cost, status in ((3., "INVALID"), (2., "CAPPED"), (.001, "COMPLETE")):
            with self.subTest(cost=cost), tempfile.TemporaryDirectory(prefix="benchmark_band_", dir=SCRATCH) as tmp:
                old = self.root; self.root = Path(tmp)
                clock = Clock(); H = fake_h(clock=clock, cost=cost)
                try:
                    with mock.patch.object(self.B, "run_svd_phase", return_value={"status": "SKIPPED-NO-TIME",
                            "n": 11008, "seconds": 0., "seconds_at_least": None}):
                        rc, out = self.worker(H, clock)
                    r = json.loads((out / "benchmark.json").read_text())
                    self.assertEqual(r["status"], status); self.assertEqual(rc, 2 if status == "INVALID" else 0)
                    self.assertEqual(len(r["weights_before"]), 36)
                    self.assertTrue(any(x["after"] == "probe_forward" and x["match"] for x in r["weights_after"]))
                    self.assertGreaterEqual(r["reserve_s"], 30.)
                finally: self.root = old

    def test_optional_skip_keeps_top_level_status(self):
        clock = Clock(); H = fake_h(clock=clock, cost=1.)
        with mock.patch.object(self.B, "phase_fits", return_value=False), mock.patch.object(self.B, "run_svd_phase") as svd:
            rc, out = self.worker(H, clock)
        self.assertEqual(rc, 0); svd.assert_not_called()
        r = json.loads((out / "benchmark.json").read_text())
        self.assertEqual(r["status"], "COMPLETE")
        for name in ("batch_forward", "eval_A7", "svd"):
            self.assertEqual(r["phases"][name]["status"], "SKIPPED-NO-TIME")
        self.assertTrue(r["weights_unchanged"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if "c10e_bandknob" in sys.modules:
        raise AssertionError("CPU benchmark selftest imported c10e_bandknob")
    if result.wasSuccessful(): print("C10Z_BENCH_SELFTEST_PASS tests=" + str(result.testsRun))
    sys.exit(0 if result.wasSuccessful() else 1)
