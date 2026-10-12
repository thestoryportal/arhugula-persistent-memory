import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""V7-DIAG specification tests: CPU stubs only, never dispatch the probe."""
import ast
import copy
import ctypes
import hashlib
import importlib
import importlib.util
import inspect
import json
import math
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import textwrap
import time
import types
import unittest
from unittest.mock import patch

import numpy as np
import torch
torch.set_num_threads(1)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import c10z_astra_arms as D


def frozen_probe_prereg():
    # The completed V7-DIAG retains its pre-A1 contract; these fixtures do not dispatch that probe.
    raw=(ROOT/D.PREREG).read_bytes().split(b"\n\n---\n\n## \xc2\xa712 Amendment A1-POPULATION",1)[0]
    assert hashlib.sha256(raw).hexdigest()=="7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29"
    return raw


def probe(test):
    path = ROOT / "code/lab/track_c/c10z_v7_diag.py"
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
    return importlib.import_module("c10z_v7_diag")


def fixture_rows(n=1000):
    lengths = (3, 17, 101, 137)
    return [{"id": str(i), "text": " ".join(str((i + j) % 31 + 1) for j in range(lengths[i % 4]))}
            for i in range(n)]


class Tokenizer:
    pad_token_id = 97
    def __call__(self, text):
        return {"input_ids": list(map(int, text.split()))}


class Tiny(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = torch.nn.ModuleList([torch.nn.Identity() for _ in range(36)])
        self.model = types.SimpleNamespace(layers=[types.SimpleNamespace(mlp=types.SimpleNamespace(down_proj=m)) for m in self.layers])
        self.config = types.SimpleNamespace(_attn_implementation="CPU stub")
        self.calls = []
    def forward(self, input_ids, attention_mask, use_cache, logits_to_keep):
        assert input_ids.device.type == "cpu" and not torch.is_grad_enabled()
        assert use_cache is False and logits_to_keep == 0
        self.calls.append((input_ids.clone(), attention_mask.clone()))
        x = input_ids.float()
        # Padding carries large nonzero activations; omitting the mask cannot pass.
        for l, module in enumerate(self.layers):
            module(torch.stack((x + l + 1, x * 2 + l + 2, x * 3 - l - 1), dim=-1).half())


def stub_session():
    s = object.__new__(D.Session)
    s.H = types.SimpleNamespace(tok=Tokenizer(), model=Tiny(), DEV="cpu")
    s.modules = {str(l): m for l, m in enumerate(s.H.model.layers)}
    s.budget = types.SimpleNamespace(check=lambda: None)
    s.timings = {}; s.hooks_check = lambda: None
    s.sync = lambda: None; s.check_memory = lambda: None
    return s


def tiny_zeros(original):
    def zeros(*shape, **kw):
        if shape == (11008,):
            assert kw == {"dtype": torch.float64, "device": "cpu"}
            shape = (3,)
        return original(*shape, **kw)
    return zeros


def scores(value):
    return {"rho": {str(l): value for l in range(4, 13)},
            "E": {str(l): "+inf" for l in range(4, 13)}, "P": value is not None and value >= .8}


class StatisticTests(unittest.TestCase):
    def test_ast_identity_sums_and_loop_only_row_count_varies(self):
        P = probe(self)
        def nodes(method):
            return ast.parse(textwrap.dedent(inspect.getsource(method))).body[0].body
        driver = nodes(D.Session.compute_dstats); actual = nodes(P.Statistic.compute_dstats)
        def selected(body):
            sums = next(n for n in body if isinstance(n, ast.Assign) and
                        any(isinstance(t, ast.Name) and t.id == "sums" for t in n.targets))
            loop = next(n for n in body if isinstance(n, ast.For) and
                        isinstance(n.target, ast.Name) and n.target.id == "start_row")
            return sums, loop
        old_sums, old_loop = selected(driver); new_sums, new_loop = selected(actual)
        self.assertEqual(ast.dump(old_sums, include_attributes=False), ast.dump(new_sums, include_attributes=False))
        self.assertEqual(ast.dump(ast.Module(body=old_loop.body, type_ignores=[])),
                         ast.dump(ast.Module(body=new_loop.body, type_ignores=[])))
        self.assertEqual(ast.dump(old_loop.iter.args[0]), ast.dump(new_loop.iter.args[0]))
        self.assertEqual(ast.dump(old_loop.iter.args[2]), ast.dump(new_loop.iter.args[2]))
        self.assertEqual(ast.dump(new_loop.iter.args[1]), ast.dump(ast.parse("len(rows)", mode="eval").body))
        self.assertEqual(ast.dump(driver[-1], include_attributes=False), ast.dump(actual[-1], include_attributes=False))

    def test_actual_driver_bit_identity_and_independent_tokens_counts_normalization(self):
        P = probe(self); rows = fixture_rows(); old = stub_session(); new = stub_session()
        artifact={"dataset":{"fixture":True},"population":{"revision":P.DATASET_REV,
                  "row_ids":[r["id"] for r in rows],"texts":[r["text"] for r in rows],"indices":list(range(1000))}}
        with patch.object(D.R,"load_reference_population",return_value=artifact) as population, \
             patch.object(torch, "zeros", side_effect=tiny_zeros(torch.zeros)):
            reference = old.compute_dstats()
            actual = P.Statistic.compute_dstats(new, rows)
        expected_ids = [[int(v) for v in r["text"].split()][:100] for r in rows]
        population.assert_called_once_with(D.ROOT)
        self.assertEqual(actual["dataset"], {k:reference["dataset"][k] for k in actual["dataset"]})
        self.assertEqual(actual["dataset"]["ordered_token_ids"], expected_ids)
        self.assertEqual(actual["dataset"]["nonpadding_tokens"], 55000)
        self.assertEqual(reference["dataset"]["nonpadding_tokens_per_row"], list(map(len,expected_ids)))
        self.assertEqual(actual["dataset"]["text_sha256"],
                         [hashlib.sha256(r["text"].encode()).hexdigest() for r in rows])
        self.assertEqual(actual["dataset"]["row_ids"], [str(i) for i in range(1000)])
        self.assertEqual(len(old.H.model.calls), 63)
        self.assertEqual([len(ids) for ids, mask in new.H.model.calls], [16] * 62 + [8])
        self.assertEqual(len(new.H.model.calls), len(old.H.model.calls))
        self.assertTrue(any(bool((mask == 0).any()) for ids, mask in new.H.model.calls))
        for a, b in zip(old.H.model.calls, new.H.model.calls):
            self.assertTrue(torch.equal(a[0], b[0])); self.assertTrue(torch.equal(a[1], b[1]))
            self.assertTrue(bool((b[0][b[1] == 0] == 97).all()))
        for l in range(36):
            self.assertTrue(torch.equal(actual["m"][str(l)], reference["m"][str(l)]), str(l))
            total = [0, 0, 0]
            for row in expected_ids:
                for v in row:
                    for j, x in enumerate((v + l + 1, 2 * v + l + 2, 3 * v - l - 1)):
                        total[j] += x * x
            expected = torch.tensor(total, dtype=torch.float64).div(55000).float()
            self.assertTrue(torch.equal(actual["m"][str(l)], expected), "independent normalization layer=" + str(l))
            self.assertEqual(actual["m"][str(l)].dtype, torch.float32)
        self.assertFalse(torch.equal(actual["m"]["0"], actual["m"]["35"]))
        self.assertTrue(all(not m._forward_pre_hooks for m in new.modules.values()))

    def test_hook_cleanup_after_forward_error(self):
        P = probe(self); s = stub_session()
        with patch.object(s.H.model, "forward", side_effect=RuntimeError("forced forward failure")), \
             patch.object(torch, "zeros", side_effect=tiny_zeros(torch.zeros)):
            with self.assertRaisesRegex(RuntimeError, "forced forward failure"):
                P.Statistic.compute_dstats(s, fixture_rows(8))
        self.assertTrue(all(not m._forward_pre_hooks for m in s.modules.values()))


class SelectionAndScoringTests(unittest.TestCase):
    def test_full_seed_one_permutation_and_exact_population_sizes(self):
        P = probe(self); actual = P.population_indices(5017)
        permutation = list(range(5017)); random.Random(1).shuffle(permutation)
        self.assertEqual(actual, {"F1000": list(range(1000)), "R1000": permutation[:1000], "R5000": permutation[:5000]})
        with self.assertRaisesRegex(ValueError, "5000"): P.population_indices(4999)

    def test_ordered_routing_equal_boundary_nonfinite_and_report_only_E(self):
        P = probe(self)
        cases = (({}, "INCONCLUSIVE"), ({"F1000": scores(.8)}, "INCONCLUSIVE"),
                 ({"F1000": scores(.79), "R1000": scores(.8)}, "A1"),
                 ({"F1000": scores(.79), "R1000": scores(.79), "R5000": scores(.8)}, "A2"),
                 ({"F1000": scores(.79), "R1000": scores(.79), "R5000": scores(.799999999)}, "D"))
        for measured, want in cases:
            with self.subTest(want=want): self.assertEqual(P.route(measured)[0], want)
        measured = {"F1000": scores(.79), "R1000": scores(.8)}
        for bad in (None, math.nan, math.inf, .799999999999):
            measured["R1000"]["rho"]["12"] = bad
            self.assertEqual(P.route(measured)[0], "INCONCLUSIVE")
        self.assertEqual(P.route({"F1000": scores(.79), "R1000": scores(.8)}, integrity=False)[0], "INCONCLUSIVE")

    def test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf(self):
        P = probe(self)
        self.assertIs(P.spearman, D.spearman)
        m = {str(l): torch.tensor([0., 2., 2., 8.]) for l in range(36)}
        cache = {str(l): np.array([1., 2., 2., 4.]) for l in range(4, 13)}
        result = P.score_population({"m": m}, cache)
        self.assertEqual(result["rho"], {str(l): 1. for l in range(4, 13)})
        self.assertEqual(result["E"]["4"], math.log(2) / 2)
        self.assertEqual(result["infinite_log_ratios"]["4"], 1)
        m["4"] = torch.zeros(4)
        result = P.score_population({"m": m}, cache)
        self.assertIsNone(result["rho"]["4"]); self.assertEqual(result["E"]["4"], "+inf")
        self.assertFalse(result["P"]); json.dumps(result, allow_nan=False)

    def test_cache_diagonal_count_and_loaded_once(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for l in range(4, 13):
                paths[str(l)] = Path(tmp) / (str(l) + ".npz")
                np.savez(paths[str(l)], **{"mom2.mom2": np.diag([4., 8., 12.]), "mom2.count": 4})
            with patch.object(np, "load", wraps=np.load) as load:
                actual = P.load_cache_diagonals(paths)
            self.assertEqual(load.call_count, 9)
            for diagonal in actual.values(): np.testing.assert_array_equal(diagonal, [1., 2., 3.])


class ProbePipelineTests(unittest.TestCase):
    def pipeline(self, case, fault=None, late=None, integrity_check=lambda: True):
        P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        out = Path(tmp.name); index = P.population_indices(5017); rows = fixture_rows(5017)
        measured = []; timing = [0.]
        budget = P.Deadline(start=0., clock=lambda: timing[0])
        pins = {"dataset": {"revision": P.DATASET_REV, "split_length": len(rows)},
                "populations": {n: {"indices": v, **P.row_metadata([rows[i] for i in v], Tokenizer())}
                                for n, v in index.items()}}
        D.write_json(out / "pins.json", pins)
        def compute(ordered):
            name = ("F1000", "R1000", "R5000")[len(measured)]; measured.append(name)
            self.assertEqual(ordered, [rows[i] for i in index[name]])
            self.assertTrue((out / "pins.json").is_file())
            if fault == name: raise RuntimeError("forced measurement failure")
            return {"m": {str(l): torch.tensor([1., 2., 3.]) for l in range(36)},
                    "dataset": P.row_metadata(ordered, Tokenizer())}
        def score(stats, cache):
            name = measured[-1]; path = out / ("m_" + name + ".pt")
            self.assertTrue(path.is_file(), "scored before persistence")
            saved = torch.load(path, weights_only=True)
            self.assertEqual(saved["dataset"], stats["dataset"])
            for l in range(36): self.assertTrue(torch.equal(saved["m"][str(l)], stats["m"][str(l)]))
            if late == name: timing[0] = 3060.
            return scores(case[name])
        with patch.object(P, "score_population", side_effect=score):
            result = P.measure_populations(out, rows, types.SimpleNamespace(compute_dstats=compute),
                                          pins, {}, budget, integrity_check=integrity_check)
        return out, result, measured

    def test_F_pass_stops_and_random_pass_never_measures_R5000(self):
        for case, want, names in (({"F1000": .8}, "INCONCLUSIVE", ["F1000"]),
                                  ({"F1000": .79, "R1000": .8}, "A1", ["F1000", "R1000"])):
            out, result, actual = self.pipeline(case)
            self.assertEqual((result["outcome"], actual), (want, names))
            pending = json.loads((out / "verdict.json").read_text())
            self.assertEqual((pending["outcome"], pending["completion"]), ("INCONCLUSIVE", "incomplete"))
            self.assertEqual(result["completion"], "awaiting_cleanup")

    def test_R5000_independent_conditional_A2_and_D(self):
        for value, want in ((.8, "A2"), (.79, "D")):
            out, result, names = self.pipeline({"F1000": .79, "R1000": .79, "R5000": value})
            self.assertEqual((result["outcome"], names), (want, ["F1000", "R1000", "R5000"]))
            self.assertEqual(result["populations_measured"], names)

    def test_incomplete_failure_retains_prior_m_and_no_selection(self):
        out, result, names = self.pipeline({"F1000": .79}, fault="R1000")
        self.assertEqual(result["outcome"], "INCONCLUSIVE")
        self.assertIn("forced measurement failure", result["reason"])
        self.assertTrue((out / "m_F1000.pt").is_file()); self.assertFalse((out / "m_R1000.pt").exists())

    def test_scoring_deadline_cannot_publish_A1_or_increase_cap(self):
        out, result, names = self.pipeline({"F1000": .79, "R1000": .8}, late="R1000")
        self.assertEqual(result["outcome"], "INCONCLUSIVE"); self.assertIn("deadline", result["reason"])
        self.assertEqual(result["cap_seconds"], 3060)

    def test_tensor_exclusive_flush_fsync_and_provenance(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m_F1000.pt"
            value = {"m": {str(l): torch.tensor([l + 1.]) for l in range(36)}, "dataset": {"row_ids": ["a"]}}
            with patch.object(os, "fsync", wraps=os.fsync) as sync:
                P.save_population(path, value)
            self.assertGreaterEqual(sync.call_count, 1)
            self.assertEqual(torch.load(path, weights_only=True)["dataset"], value["dataset"])
            before = path.read_bytes()
            with self.assertRaises(FileExistsError): P.save_population(path, value)
            self.assertEqual(path.read_bytes(), before)


class PinsAndAdmissionTests(unittest.TestCase):
    def test_local_arrow_revision_length_shards_and_offline_only(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); cache = root / "data/hf_cache"
            directory = cache / "datasets/wikimedia___wikipedia/20231101.en/0.0.0" / P.DATASET_REV
            directory.mkdir(parents=True)
            (directory / "dataset_info.json").write_text(json.dumps({"config_name": "20231101.en",
                "splits": {"train": {"num_examples": 5, "shard_lengths": [2, 3]}}}))
            shards = [directory / ("wikipedia-train-%05d-of-00002.arrow" % i) for i in range(2)]
            for p in shards: p.write_bytes(b"fixture")
            calls = []; datasets = types.ModuleType("datasets")
            def read(path): calls.append(path); return [0, 1] if path == str(shards[0]) else [2, 3, 4]
            datasets.Dataset = types.SimpleNamespace(from_file=read)
            datasets.concatenate_datasets = lambda parts: [v for part in parts for v in part]
            with patch.dict(sys.modules, datasets=datasets), patch.dict(os.environ, clear=False):
                split, identity = P.open_local_split(root)
                self.assertEqual(os.environ["HF_DATASETS_OFFLINE"], "1")
                self.assertEqual(os.environ["HF_HOME"], str(cache.resolve()))
            self.assertEqual(split, [0, 1, 2, 3, 4]); self.assertEqual(calls, list(map(str, shards)))
            self.assertEqual(identity["revision"], P.DATASET_REV)
            shards[1].unlink()
            with patch.dict(sys.modules, datasets=datasets):
                with self.assertRaisesRegex(ValueError, "shard"): P.open_local_split(root)

    def test_all_pins_include_every_population_before_forwards(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ("code/lab/track_c/c10z_v7_diag.py", "code/lab/track_c/c10z_astra_arms.py",
                        "code/memit/vendor/memit/memit_main.py", "experiments/c10z/design/C10Z_ASTRA_PREREG.md"):
                p = root / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(rel)
            snapshot = root / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / P.MODEL_REV
            snapshot.mkdir(parents=True)
            for name in ("tokenizer.json", "tokenizer_config.json", "config.json", "model-00001.safetensors"):
                (snapshot / name).write_text(name)
            caches = {}
            for l in range(4, 13):
                caches[str(l)] = root / (str(l) + ".npz"); caches[str(l)].write_bytes(b"cache")
            with patch.object(P, "cache_paths", return_value=caches), \
                 patch.object(P, "engine_sources", return_value={"code/memit/vendor/memit/memit_main.py": "hash"}), \
                 patch.object(P, "environment", return_value={"device": "mps", "torch": "fixture", "transformers": "fixture", "datasets": "fixture"}), \
                 patch.object(P, "hub_revision", return_value={"status": "available", "sha": "f" * 40}):
                value = P.build_pins(root, fixture_rows(5017), Tokenizer(),
                                     {"revision": P.DATASET_REV, "split_length": 5017}, {"ok": True})
            self.assertEqual(set(value["populations"]), {"F1000", "R1000", "R5000"})
            self.assertEqual(len(value["populations"]["R5000"]["indices"]), 5000)
            self.assertEqual(value["populations"]["F1000"]["nonpadding_tokens"], 55000)
            self.assertEqual(len(value["populations"]["F1000"]["nonpadding_tokens_per_row"]), 1000)
            self.assertEqual(value["attempt3_dataset_identity"], "UNVERIFIABLE")
            self.assertEqual(value["hub_current_revision"]["sha"], "f" * 40)
            self.assertEqual(value["dataset"]["revision"], P.DATASET_REV)
            self.assertEqual(set(value["cache_files"]), {str(l) for l in range(4, 13)})
            for key in ("source_files", "engine_sources", "model_files", "tokenizer_files", "environment_sha256", "prereg_sha256"):
                self.assertTrue(value[key], key)

    def test_launcher_existing_namespace_and_worker_gates_refuse_before_probe(self):
        path = ROOT / "code/lab/runners/run_c10z_v7_diag.py"
        self.assertTrue(path.is_file(), "missing exclusivity launcher")
        spec = importlib.util.spec_from_file_location("v7_launcher_test", path)
        L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
        for why in ("namespace", "fingerprint", "gpu"):
            with self.subTest(why=why), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); out = root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
                if why == "namespace": out.mkdir(parents=True)
                gate = types.SimpleNamespace(check_fingerprint=lambda: {"ok": why != "fingerprint"},
                                             check_gpu=lambda: {"ok": why != "gpu", "blocking_processes": ["C10Y calibration 4"]})
                with patch.object(L, "ROOT", root), patch.object(L, "gate_module", return_value=gate), \
                     patch.object(L.runpy, "run_path", side_effect=AssertionError("probe dispatched")):
                    action = L.launch if why == "namespace" else L.worker
                    with self.assertRaisesRegex(ValueError, why): action("20261009T000000Z")

    def test_supervised_worker_reuses_only_required_gates_before_forward_entry(self):
        path = ROOT / "code/lab/runners/run_c10z_v7_diag.py"; self.assertTrue(path.is_file(), "missing launcher")
        spec = importlib.util.spec_from_file_location("v7_launcher_test", path)
        L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
        gate = types.SimpleNamespace(check_fingerprint=lambda: {"ok": True}, check_gpu=lambda: {"ok": True})
        with tempfile.TemporaryDirectory() as tmp, patch.object(L, "ROOT", Path(tmp)), \
             patch.object(L, "gate_module", return_value=gate), patch.object(sys, "argv", [str(path)]):
            def entered(script, run_name):
                self.assertEqual(str(script), str(Path(tmp) / "code/lab/track_c/c10z_v7_diag.py"))
                self.assertEqual(run_name, "__main__")
                self.assertEqual(sys.argv[1:], ["--utc", "20261009T000000Z"])
                raise RuntimeError("CPU positive control reached forward entry boundary")
            with patch.object(L.runpy, "run_path", side_effect=entered):
                with self.assertRaisesRegex(RuntimeError, "CPU positive control"): L.worker("20261009T000000Z")

    def test_namespace_refuses_reuse_and_attempt3_path(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); out = P.reserve_namespace(root, "20261009T000000Z")
            self.assertEqual(out, root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z")
            with self.assertRaises(FileExistsError): P.reserve_namespace(root, "20261009T000000Z")
            for bad in ("../c10z_astra_attempt3", "x", "20261009T000000Z/child"):
                with self.assertRaises(ValueError): P.reserve_namespace(root, bad)


class DeadlineTests(unittest.TestCase):
    def test_launcher_origin_carried_and_future_or_nonfinite_origin_refused(self):
        P = probe(self)
        self.assertTrue(hasattr(P, "entry_origin"), "missing launcher deadline origin carry")
        self.assertEqual(P.entry_origin(10., {}), 10.)
        self.assertEqual(P.entry_origin(10., {"C10Z_V7_LAUNCH_STARTED": "7.5"}), 7.5)
        for bad in ("10.01", "nan", "inf", "-1", "broken"):
            with self.assertRaises(ValueError): P.entry_origin(10., {"C10Z_V7_LAUNCH_STARTED": bad})

    def test_CLI_bootstrap_timer_exists_before_driver_import(self):
        P = probe(self); path = Path(P.__file__)
        code = "\n".join([
            "import ast, signal", "path=" + repr(str(path)),
            "tree=ast.parse(open(path).read())",
            "index=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Import) and any(a.name=='c10z_astra_arms' for a in n.names))",
            "prefix=ast.Module(body=tree.body[:index],type_ignores=[])",
            "exec(compile(prefix,path,'exec'), {'__name__':'__main__','__file__':path})",
            "remaining=signal.getitimer(signal.ITIMER_REAL)[0]",
            "assert 0 < remaining <= 3060, 'bootstrap timer absent before driver import'",
            "assert signal.getsignal(signal.SIGALRM)==signal.SIG_DFL",
            "signal.setitimer(signal.ITIMER_REAL,0)", "print('PREIMPORT_TIMER_CONTROL remaining_s='+str(remaining))"])
        child = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stdout + child.stderr); print(child.stdout.strip())

    def test_launcher_native_block_is_bounded_before_probe_dispatch(self):
        path = ROOT / "code/lab/runners/run_c10z_v7_diag.py"; self.assertTrue(path.is_file(), "missing launcher")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            launcher = FixRoundOneTests.synthetic_launcher(self, root, "raise AssertionError('probe must not run')\n")
            tools = root / "tools"
            (tools / "c10w_p2_gate.py").write_text("import ctypes\ndef check_fingerprint():\n    ctypes.PyDLL(None).usleep(2000000)\n    return {'ok': False}\ndef check_gpu():\n    raise AssertionError('must not get this far')\n")
            started = time.monotonic()
            child = subprocess.run([sys.executable, "-B", str(launcher), "--utc", "20261009T000000Z"],
                                   capture_output=True, text=True, timeout=5)
            elapsed = time.monotonic() - started
            self.assertEqual(child.returncode, 2, child.stdout + child.stderr)
            self.assertLess(elapsed, 2.)
            out = root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
            diagnostic = json.loads(next(out.glob("halt_diagnostic_*.json")).read_text())
            self.assertTrue(diagnostic["timed_out"] or diagnostic["worker_returncode"] == -signal.SIGALRM)
            self.assertFalse((out / "pins.json").exists()); self.assertFalse((out / "worker_result.json").exists())
            print("LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=%s elapsed_s=%.4f" % (child.returncode, elapsed))

    def test_immutable_3060_includes_preimport_and_exact_boundary(self):
        P = probe(self); now = [0.]; budget = P.Deadline(start=0., clock=lambda: now[0])
        now[0] = 3059.999; budget.check()
        now[0] = 3060.
        with self.assertRaises(TimeoutError): budget.check()
        with self.assertRaises((AttributeError, TypeError)): budget.expires = 999999.
        self.assertEqual(budget.expires, 3060.)

    def test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive(self):
        P = probe(self)
        for native in (False, True):
            with self.subTest(native=native), tempfile.TemporaryDirectory() as tmp:
                code = "\n".join([
                    "import sys, time, ctypes, json", "from pathlib import Path",
                    "sys.path.insert(0, " + repr(str(ROOT / "code/lab/track_c")) + ")",
                    "import c10z_v7_diag as P", "P.CAP_SECONDS = .15",
                    "out=Path(" + repr(tmp) + ")", "P.publish_verdict(out, {}, 'INCONCLUSIVE', 'incomplete measurement or hard deadline', complete=False)",
                    "with P.Deadline():",
                    "    ctypes.PyDLL(None).usleep(2000000)" if native else "    time.sleep(2)",
                    "raise AssertionError('hard timer did not terminate')"])
                started = time.monotonic()
                child = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=5)
                elapsed = time.monotonic() - started
                self.assertEqual(child.returncode, -signal.SIGALRM, child.stdout + child.stderr)
                self.assertLess(elapsed, 2.)
                self.assertEqual(json.loads((Path(tmp) / "verdict.json").read_text())["outcome"], "INCONCLUSIVE")
                print("HARD_DEADLINE_CONTROL native_GIL_hold=%s rc=%s elapsed_s=%.4f" % (native, child.returncode, elapsed))


class EntryAndGuardTests(unittest.TestCase):
    def prepare_entry(self, P, root):
        prereg = root / D.PREREG; prereg.parent.mkdir(parents=True)
        prereg.write_bytes(frozen_probe_prereg())
        rows = fixture_rows(5017)
        pins = {"populations": {name: {"indices": indices,
                   **P.row_metadata([rows[i] for i in indices], Tokenizer())}
                for name, indices in P.population_indices(len(rows)).items()}, "cache_files": {}}
        gate = types.ModuleType("c10w_p2_gate")
        gate.check_fingerprint = lambda: {"ok": True}
        gate.check_gpu = lambda: {"ok": True}
        return rows, pins, gate

    def test_timer_armed_before_namespace_and_initial_publication(self):
        P = probe(self); events = []
        class Budget:
            def __init__(self, **kw): pass
            def __enter__(self): events.append("armed"); return self
            def __exit__(self, *a): pass
            def check(self): pass
        reserve = P.reserve_namespace; publish = P.publish_verdict
        def reserved(*a): events.append("reserve"); return reserve(*a)
        def published(*a, **kw): events.append("publish"); return publish(*a, **kw)
        with tempfile.TemporaryDirectory() as tmp, patch.object(P, "ROOT", Path(tmp)), \
             patch.object(P, "LLMDB_ROOT", tmp), patch.object(P, "Deadline", Budget), \
             patch.object(P, "reserve_namespace", side_effect=reserved), \
             patch.object(P, "publish_verdict", side_effect=published), \
             patch.object(D, "entry_preflight", side_effect=ValueError("forced setup refusal")):
            self.assertEqual(P.run("20261009T000000Z"), 2)
        self.assertEqual(events[:3], ["armed", "reserve", "publish"])

    def test_real_entry_CPU_fixture_pins_durable_before_each_forward(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); rows, pins, gate = self.prepare_entry(P, root)
            model = Tiny(); H = types.SimpleNamespace(tok=Tokenizer(), model=model, DEV="cpu")
            scores_seen = []; forward = model.forward
            def checked_forward(*a, **kw):
                record = json.loads((root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z/pins.json").read_text())
                self.assertEqual(set(record["populations"]), {"F1000", "R1000", "R5000"})
                self.assertEqual(record["populations"]["F1000"]["nonpadding_tokens"], 55000)
                return forward(*a, **kw)
            def scored(stats, cache):
                scores_seen.append(stats["dataset"]["row_ids"])
                return scores(.79 if len(scores_seen) == 1 else .8)
            with patch.object(P, "ROOT", root), patch.object(P, "LLMDB_ROOT", tmp), \
                 patch.dict(os.environ, {"LLMDB_ROOT": tmp}, clear=True), patch.dict(sys.modules, c10w_p2_gate=gate), \
                 patch.object(P, "open_local_split", return_value=(rows, {"revision": P.DATASET_REV})), \
                 patch.object(P, "load_pristine", return_value=H), patch.object(P, "build_pins", return_value=pins), \
                 patch.object(P, "load_cache_diagonals", return_value={}), patch.object(P, "verify_pins", return_value=True), \
                 patch.object(P, "score_population", side_effect=scored), patch.object(model, "forward", side_effect=checked_forward), \
                 patch.object(torch, "zeros", side_effect=tiny_zeros(torch.zeros)):
                self.assertEqual(P.run("20261009T000000Z"), 0)
            out = root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
            result = json.loads((out / "verdict.json").read_text())
            self.assertEqual((result["outcome"], result["completion"]), ("INCONCLUSIVE", "incomplete"))
            receipt = json.loads((out / "worker_result.json").read_text())
            self.assertEqual((receipt["outcome"], receipt["completion"]), ("A1", "awaiting_worker_exit"))
            self.assertTrue(receipt["cleanup_completed"])
            self.assertEqual(len(model.calls), 126); self.assertFalse((out / "m_R5000.pt").exists())

    def test_outer_error_preserves_durable_measured_population_details(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); rows, pins, gate = self.prepare_entry(P, root)
            measured = {"F1000": scores(.79), "R1000": scores(.8)}
            mismatch = {"population": "F1000", "fields": {"nonpadding_tokens": {"expected": 55000, "actual": 55001}}}
            def failure(out, *a, **kw):
                P.publish_verdict(out, measured, "INCONCLUSIVE", "incomplete measurement", provenance_mismatch=mismatch)
                raise TimeoutError("forced final deadline")
            H = types.SimpleNamespace(model=types.SimpleNamespace(config=types.SimpleNamespace(_attn_implementation="stub"), training=False), tok=Tokenizer())
            with patch.object(P, "ROOT", root), patch.object(P, "LLMDB_ROOT", tmp), \
                 patch.dict(os.environ, {"LLMDB_ROOT": tmp}, clear=True), patch.dict(sys.modules, c10w_p2_gate=gate), \
                 patch.object(P, "open_local_split", return_value=(rows, {})), patch.object(P, "load_pristine", return_value=H), \
                 patch.object(P, "Statistic", return_value=types.SimpleNamespace(check_memory=lambda: None)), \
                 patch.object(P, "build_pins", return_value=pins), patch.object(P, "load_cache_diagonals", return_value={}), \
                 patch.object(P, "measure_populations", side_effect=failure):
                self.assertEqual(P.run("20261009T000000Z"), 2)
            result = json.loads((root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z/verdict.json").read_text())
            self.assertEqual(result["scores"], measured); self.assertEqual(result["outcome"], "INCONCLUSIVE")
            self.assertEqual(result.get("provenance_mismatch"), mismatch, "late error dropped retained mismatch details")

    def test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation(self):
        P = probe(self)
        for rss, driver, double in ((41 * 2**30, 0, False), (0, 33 * 2**30, False), (1, 1, True)):
            with self.subTest(rss=rss, driver=driver, double=double):
                s = object.__new__(P.Statistic); s.memory = []; s.budget = types.SimpleNamespace(check=lambda: None)
                parameter = types.SimpleNamespace(device=types.SimpleNamespace(type="mps"), dtype=torch.float64 if double else torch.float16)
                s.H = types.SimpleNamespace(DEV="mps", model=types.SimpleNamespace(parameters=lambda: [parameter]))
                import psutil
                with patch.object(psutil, "Process", return_value=types.SimpleNamespace(memory_info=lambda: types.SimpleNamespace(rss=rss))), \
                     patch.object(torch.mps, "driver_allocated_memory", return_value=driver):
                    with self.assertRaisesRegex(D.R.Halt, "HALTED-V11"): s.check_memory()


class IntegrityTests(unittest.TestCase):
    pipeline = ProbePipelineTests.pipeline
    def test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); snapshot = root / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / P.MODEL_REV
            snapshot.mkdir(parents=True)
            source = root / "probe.py"; engine = root / "engine.py"
            model = snapshot / "model.safetensors"; tokenizer = snapshot / "tokenizer.json"; cache = root / "cache.npz"
            for p in (source, engine, model, tokenizer, cache): p.write_bytes(b"pinned fixture")
            pins = {"source_files": {"probe.py": D.sha256_file(source)}, "engine_sources": {"engine.py": D.sha256_file(engine)},
                    "model_files": {model.name: D.sha256_file(model)}, "tokenizer_files": {tokenizer.name: D.sha256_file(tokenizer)},
                    "cache_files": {"4": {"path": str(cache), "sha256": D.sha256_file(cache)}}}
            self.assertTrue(P.verify_pins(root, pins))
            for p in (source, engine, model, tokenizer, cache):
                with self.subTest(path=p.name):
                    p.write_bytes(b"corrupted fixture")
                    with self.assertRaisesRegex(ValueError, "integrity drift"): P.verify_pins(root, pins)
                    out, result, measured = self.pipeline({"F1000": .79, "R1000": .8},
                                                         integrity_check=lambda: P.verify_pins(root, pins))
                    self.assertEqual(result["outcome"], "INCONCLUSIVE"); self.assertEqual(result["populations_measured"], measured)
                    self.assertTrue((out / "m_F1000.pt").is_file()); self.assertTrue((out / "m_R1000.pt").is_file())
                    p.write_bytes(b"pinned fixture")


class PersistenceCorrectionTests(unittest.TestCase):
    def session(self, out, fail=False, input_dir=None):
        s = object.__new__(D.Session); s.out = out; s.input_dir = input_dir
        s.loaded_manifest = {} if input_dir is not None else None
        s.gates = types.SimpleNamespace(law3=True); s.checks = {}
        stats = {"m": {str(l): torch.tensor([3., 2., 1.] if fail else [1., 2., 3.]) for l in range(36)},
                 "dataset": {}}
        artifact=D.R.load_reference_population()
        stats["dataset"]={**artifact["population"],"dataset_identity":artifact["dataset"],
                          "reference_population_sha256":D.R.REFERENCE_POPULATION_SHA}
        s.compute_dstats = lambda: stats; s.compute_G = lambda: torch.eye(3, dtype=torch.float64)
        s.H = types.SimpleNamespace(CANON="The capital of {} is", PTEST=["Capital of {}"])
        s.templates = ["{}"]
        paths = {}
        for l in range(4, 13):
            paths[str(l)] = out.parent / (str(l) + ".npz")
            np.savez(paths[str(l)], **{"mom2.mom2": np.diag([1., 2., 3.]), "mom2.count": 1})
        s.covariance_paths = lambda: paths
        return s, stats

    def test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; out.mkdir(); s, stats = self.session(out, fail=True)
            compute_G = s.compute_G
            def g(): self.assertTrue((out / "dstats.pt").is_file(), "dstats missing immediately after obtain"); return compute_G()
            s.compute_G = g
            with self.assertRaisesRegex(D.R.Halt, "HALTED-V7"): s.prepare_instruments()
            actual = torch.load(out / "dstats.pt", weights_only=True)
            self.assertEqual(actual["dataset"], stats["dataset"])
            for l in range(36): self.assertTrue(torch.equal(actual["m"][str(l)], stats["m"][str(l)]))
            self.assertTrue(torch.equal(torch.load(out / "G.pt", weights_only=True), s.G))
            self.assertEqual(s.checks["V7"]["spearman"]["4"], -1.)

    def test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_out = Path(tmp) / "old"; new_out = Path(tmp) / "new"; old_out.mkdir(); new_out.mkdir()
            old, _ = self.session(old_out); new, _ = self.session(new_out)
            old_prepare_instruments(old); new.prepare_instruments()
            self.assertEqual(old.checks, new.checks)
            for name in ("dstats.pt", "G.pt", "overlap_audit.json"):
                self.assertEqual((old_out / name).read_bytes(), (new_out / name).read_bytes(), name)

    def test_process2_exact_input_bytes_retained_on_fail_and_pass(self):
        for fail in (True, False):
            with self.subTest(fail=fail), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "out"; source = Path(tmp) / "source"; out.mkdir(); source.mkdir()
                s, stats = self.session(out, fail=fail, input_dir=source)
                with (source / "dstats.pt").open("xb") as f: torch.save(stats, f)
                with (source / "G.pt").open("xb") as f: torch.save(torch.eye(3, dtype=torch.float64), f)
                if fail:
                    with self.assertRaisesRegex(D.R.Halt, "HALTED-V7"): s.prepare_instruments()
                else: s.prepare_instruments()
                self.assertTrue((out / "dstats.pt").is_file(), "process2 V7 halt lost input bytes")
                self.assertEqual((out / "dstats.pt").read_bytes(), (source / "dstats.pt").read_bytes())
                self.assertTrue((out / "G.pt").is_file())
                self.assertEqual((out / "G.pt").read_bytes(), (source / "G.pt").read_bytes())

    def test_fresh_and_process2_existing_dstats_refuse_overwrite(self):
        for second in (True, False):
            with self.subTest(second=second), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "out"; out.mkdir(); source = Path(tmp) / "source"; source.mkdir()
                s, stats = self.session(out, input_dir=source if second else None)
                if second:
                    with (source / "dstats.pt").open("xb") as f: torch.save(stats, f)
                    with (source / "G.pt").open("xb") as f: torch.save(torch.eye(3), f)
                (out / "dstats.pt").write_bytes(b"prior artifact")
                with self.assertRaises(FileExistsError): s.prepare_instruments()
                self.assertEqual((out / "dstats.pt").read_bytes(), b"prior artifact")

    def test_G_failure_also_retains_immediately_obtained_dstats(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; out.mkdir(); s, stats = self.session(out)
            s.compute_G = lambda: (_ for _ in ()).throw(RuntimeError("forced G failure"))
            with self.assertRaisesRegex(RuntimeError, "forced G failure"): s.prepare_instruments()
            self.assertTrue((out / "dstats.pt").is_file(), "G failure lost already computed dstats")

    def test_process2_missing_G_retains_dstats_before_G_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; source = Path(tmp) / "source"; out.mkdir(); source.mkdir()
            s, stats = self.session(out, input_dir=source)
            with (source / "dstats.pt").open("xb") as f: torch.save(stats, f)
            with self.assertRaises(FileNotFoundError): s.prepare_instruments()
            self.assertTrue((out / "dstats.pt").is_file(), "process2 must copy dstats before loading G")
            self.assertEqual((out / "dstats.pt").read_bytes(), (source / "dstats.pt").read_bytes())
            self.assertFalse((out / "G.pt").exists(), "missing source G must not create a fabricated empty artifact")


class FixRoundOneTests(unittest.TestCase):
    session = PersistenceCorrectionTests.session

    def test_returned_m_and_actual_provenance_survive_pin_mismatch(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); rows = fixture_rows(1000)
            expected = P.row_metadata(rows, Tokenizer())
            actual = copy.deepcopy(expected); actual["nonpadding_tokens"] = 55001
            actual["row_ids"][0] = "unexpected-row"
            stats = {"m": {str(l): torch.tensor([l + 1., l + 2.]) for l in range(36)}, "dataset": actual}
            pins = {"populations": {"F1000": {"indices": list(range(1000)), **expected}}}
            with patch.object(os, "fsync", wraps=os.fsync) as sync, \
                 patch.object(P, "score_population", side_effect=AssertionError("mismatch must not score")):
                result = P.measure_populations(out, rows, types.SimpleNamespace(compute_dstats=lambda _: stats),
                                              pins, {}, P.Deadline(), lambda: True)
            path = out / "m_F1000.pt"
            print("FIX1_MISMATCH_CONTROL outcome=%s retained_m=%s" % (result["outcome"], path.exists()))
            self.assertTrue(path.is_file(), "computed m disappeared on provenance mismatch")
            saved = torch.load(path, weights_only=True)
            self.assertEqual(saved["dataset"], actual)
            for layer in map(str, range(36)): self.assertTrue(torch.equal(saved["m"][layer], stats["m"][layer]))
            self.assertGreaterEqual(sync.call_count, 2)
            self.assertEqual(result["outcome"], "INCONCLUSIVE")
            self.assertEqual(result["provenance_mismatch"]["population"], "F1000")
            detail = result["provenance_mismatch"]["fields"]
            self.assertEqual(detail["nonpadding_tokens"], {"expected": 55000, "actual": 55001})
            self.assertEqual(detail["row_ids"]["actual"][0], "unexpected-row")

    def synthetic_launcher(self, root, worker):
        tools = root / "tools"; tools.mkdir()
        launcher = tools / "run_c10z_v7_diag.py"
        source = (ROOT / "code/lab/runners/run_c10z_v7_diag.py").read_text().replace("CAP_SECONDS = 3060", "CAP_SECONDS = .15")
        source = source.replace('ROOT = Path(__file__).resolve().parents[1]', textwrap.dedent('''
            ROOT = Path(__file__).resolve().parents[1]
            _actual_fsync = os.fsync
            def _observed_fsync(fd):
                _actual_fsync(fd)
                with (ROOT/'fsync_trace').open('a') as trace:
                    trace.write(str(os.fstat(fd).st_ino)+'\\n')
            os.fsync = _observed_fsync
        ''').strip())
        launcher.write_text(source)
        (tools / "c10w_p2_gate.py").write_text("def check_fingerprint(): return {'ok': True}\ndef check_gpu(): return {'ok': True}\n")
        python = root / ".venv/bin/python"; python.parent.mkdir(parents=True); python.symlink_to(sys.executable)
        path = root / "code/lab/track_c/c10z_v7_diag.py"; path.parent.mkdir(parents=True)
        path.write_text(worker)
        return launcher

    def test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash(self):
        worker = textwrap.dedent('''
            import ctypes, json, os, signal, sys, time
            from pathlib import Path
            root=Path(os.environ['LLMDB_ROOT']); utc=sys.argv[sys.argv.index('--utc')+1]
            out=root/'experiments/c10z/runs/c10z_v7_diagnostic'/utc; out.mkdir(parents=True,exist_ok=True)
            record={'outcome':'INCONCLUSIVE','completion':'incomplete','scores':{},
                    'active_phase':'F1000:forward','incomplete_phases':['F1000','R1000','R5000','cleanup','worker_exit']}
            with (out/'verdict.json').open('x') as f:
                json.dump(record,f); f.flush(); os.fsync(f.fileno())
            mode=os.environ['FIX1_TERMINATION_MODE']
            if mode=='crash': raise RuntimeError('synthetic worker crash')
            if mode=='timeout': signal.setitimer(signal.ITIMER_REAL,0)
            else:
                signal.signal(signal.SIGALRM,signal.SIG_DFL)
                signal.setitimer(signal.ITIMER_REAL,.05)
            ctypes.PyDLL(None).usleep(2000000)
            raise AssertionError('worker outlived cap')
        ''')
        for mode in ("signal", "timeout", "crash"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); launcher = self.synthetic_launcher(root, worker)
                started = time.monotonic()
                child = subprocess.run([sys.executable, "-B", str(launcher), "--utc", "20261009T000000Z"],
                    env=dict(os.environ, FIX1_TERMINATION_MODE=mode), capture_output=True, text=True, timeout=5)
                out = root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
                diagnostics = list(out.glob("halt_diagnostic_*.json"))
                print("FIX1_TERMINATION_CONTROL mode=%s rc=%s files=%s" % (mode, child.returncode, sorted(p.name for p in out.iterdir())))
                self.assertEqual(len(diagnostics), 1, "abnormal exit left only provisional verdict; no fresh halt diagnostic")
                self.assertNotEqual(child.returncode, 0); self.assertGreater(child.returncode, 0)
                self.assertLess(time.monotonic() - started, 1.)
                diagnostic = json.loads(diagnostics[0].read_text())
                self.assertRegex(diagnostics[0].name, r"^halt_diagnostic_\d{8}T\d{6}\.\d{6}Z\.json$")
                self.assertEqual(diagnostic["outcome"], "INCONCLUSIVE")
                self.assertEqual(diagnostic["active_phase"], "F1000:forward")
                self.assertIn("cleanup", diagnostic["incomplete_phases"])
                self.assertIn("worker_exit", diagnostic["incomplete_phases"])
                self.assertIn("verdict.json", diagnostic["retained_artifacts"])
                self.assertEqual(diagnostic["cap_seconds"], .15)
                self.assertTrue(diagnostic["supervisor_observed_exit"])
                self.assertIn(str(diagnostics[0].stat().st_ino), (root / "fsync_trace").read_text().splitlines(), "halt diagnostic was not fsynced")
                self.assertEqual(json.loads((out / "verdict.json").read_text())["outcome"], "INCONCLUSIVE")

    def cleanup_subprocess(self, tmp, delay=300000, after_run="", prearmed=False):
        code = textwrap.dedent('''
            import ctypes, json, os, sys, time, types
            from pathlib import Path
            sys.path.insert(0,SOURCE)
            sys.path.insert(0,str(Path(SOURCE).parents[1]/'tools'))
            import c10z_v7_diag as P
            root=Path(TEMP); prereg=root/P.D.PREREG; prereg.parent.mkdir(parents=True)
            prereg.write_bytes(bytes.fromhex(FROZEN_PREREG))
            P.ROOT=root; P.LLMDB_ROOT=str(root); P.CAP_SECONDS=.15; P.ENTRY_STARTED=time.monotonic()
            P.PREARMED=PREARMED_FLAG
            class H:
                tok=None
                model=types.SimpleNamespace(config=types.SimpleNamespace(_attn_implementation='CPU stub'),training=False)
                def __del__(self):
                    (root/'cleanup_started').write_text('started')
                    ctypes.PyDLL(None).usleep(CLEANUP_DELAY)
                    (root/'cleanup_done').write_text('done')
            class Statistic:
                def __init__(self,h,budget): self.H=h
                def check_memory(self): pass
            gate=types.ModuleType('c10w_p2_gate'); gate.check_fingerprint=lambda:{'ok':True}; gate.check_gpu=lambda:{'ok':True}
            sys.modules['c10w_p2_gate']=gate
            P.D.entry_preflight=lambda env:None
            P.open_local_split=lambda root:([],{})
            P.load_pristine=lambda root,budget:H()
            P.Statistic=Statistic
            P.build_pins=lambda *args:{'cache_files':{}}
            P.load_cache_diagonals=lambda paths:{}
            P.measure_populations=lambda out,*args,**kw:P.publish_verdict(out,{},'A1','fixture candidate',complete=True)
            rc=P.run('20261009T000000Z')
            AFTER_RUN
            raise SystemExit(rc)
        ''').replace("SOURCE", repr(str(ROOT / "code/lab/track_c")))
        code = code.replace("CLEANUP_DELAY", str(delay)).replace("AFTER_RUN", after_run).replace("PREARMED_FLAG", repr(prearmed))
        code = code.replace("FROZEN_PREREG", repr(frozen_probe_prereg().hex()))
        return subprocess.run([sys.executable, "-B", "-c", code.replace("TEMP", repr(tmp))],
                              capture_output=True, text=True, timeout=5)

    def test_explicit_cleanup_is_inside_original_deadline_before_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            started = time.monotonic()
            child = self.cleanup_subprocess(tmp)
            root = Path(tmp)
            print("FIX1_CLEANUP_CONTROL rc=%s cleanup_started=%s cleanup_done=%s elapsed_s=%.4f" %
                  (child.returncode, (root / "cleanup_started").exists(), (root / "cleanup_done").exists(), time.monotonic() - started))
            self.assertEqual(child.returncode, -signal.SIGALRM, "cleanup completed after deadline because timer was cancelled")
            self.assertTrue((root / "cleanup_started").is_file()); self.assertFalse((root / "cleanup_done").exists())
            verdict = json.loads((root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z/verdict.json").read_text())
            self.assertEqual(verdict["completion"], "incomplete", "successful completion published before cleanup")
            self.assertEqual(verdict["outcome"], "INCONCLUSIVE")

    def test_worker_deadline_remains_armed_after_cleanup_until_actual_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            after = "ctypes.PyDLL(None).usleep(2000000)"
            # PREARMED is set before run, as in the real worker CLI; it must survive __exit__.
            child = self.cleanup_subprocess(tmp, delay=10000, after_run=after, prearmed=True)
            print("FIX1_WORKER_EXIT_CONTROL rc=%s cleanup_done=%s" % (child.returncode, (Path(tmp) / "cleanup_done").exists()))
            self.assertEqual(child.returncode, -signal.SIGALRM, child.stdout + child.stderr)
            self.assertTrue((Path(tmp) / "cleanup_done").is_file())
            out = Path(tmp) / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
            self.assertEqual(json.loads((out / "worker_result.json").read_text())["completion"], "awaiting_worker_exit")
            self.assertEqual(json.loads((out / "verdict.json").read_text())["completion"], "incomplete")

    def test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap(self):
        worker = textwrap.dedent('''
            import ctypes,json,os,time
            from pathlib import Path
            root=Path(os.environ['LLMDB_ROOT']); out=root/'experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z'
            def save(name,value):
                with (out/name).open('x') as f: json.dump(value,f); f.flush(); os.fsync(f.fileno())
            save('verdict.json',{'outcome':'INCONCLUSIVE','completion':'incomplete','scores':{}})
            (root/'cleanup_done').write_text('CPU cleanup completed')
            save('progress.json',{'active_phase':'worker_exit','completed_phases':['setup','F1000','R1000','integrity','cleanup'],
                 'incomplete_phases':['worker_exit'],'skipped_phases':['R5000']})
            save('worker_result.json',{'outcome':'A1','completion':'awaiting_worker_exit','cleanup_completed':True,
                 'deadline_origin':float(os.environ['C10Z_V7_LAUNCH_STARTED']),'cap_seconds':.15,'scores':{},'reason':'CPU fixture candidate'})
            mode=os.environ['FIX1_EXIT_MODE']
            if mode=='stall': ctypes.PyDLL(None).usleep(2000000)
            if mode=='crash': raise RuntimeError('crash after cleanup receipt')
        ''')
        for mode in ("normal", "stall", "crash"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); launcher = self.synthetic_launcher(root, worker)
                child = subprocess.run([sys.executable, "-B", str(launcher), "--utc", "20261009T000000Z"],
                    env=dict(os.environ, FIX1_EXIT_MODE=mode), capture_output=True, text=True, timeout=5)
                out = root / "experiments/c10z/runs/c10z_v7_diagnostic/20261009T000000Z"
                verdict = json.loads((out / "verdict.json").read_text())
                self.assertTrue((root / "cleanup_done").is_file())
                if mode == "normal":
                    self.assertEqual(child.returncode, 0, child.stdout + child.stderr)
                    self.assertEqual((verdict["outcome"], verdict["completion"]), ("A1", "complete"))
                    self.assertTrue(verdict["supervisor_observed_exit"]); self.assertEqual(verdict["worker_returncode"], 0)
                    self.assertLess(verdict["worker_exited_monotonic"], verdict["deadline_origin"] + .15)
                else:
                    self.assertEqual(child.returncode, 2, child.stdout + child.stderr)
                    self.assertEqual((verdict["outcome"], verdict["completion"]), ("INCONCLUSIVE", "incomplete"))
                    self.assertEqual(len(list(out.glob("halt_diagnostic_*.json"))), 1)

    def test_invalid_returned_m_is_retained_before_tensor_validation(self):
        P = probe(self)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); rows = fixture_rows(1000); metadata = P.row_metadata(rows, Tokenizer())
            stats = {"m": {str(l): torch.tensor([1.], dtype=torch.float64) for l in range(36)}, "dataset": metadata}
            pins = {"populations": {"F1000": {"indices": list(range(1000)), **metadata}}}
            result = P.measure_populations(out, rows, types.SimpleNamespace(compute_dstats=lambda _: stats),
                                          pins, {}, P.Deadline(), lambda: True)
            self.assertEqual(result["outcome"], "INCONCLUSIVE")
            self.assertIn("float32", result["reason"])
            self.assertEqual(torch.load(out / "m_F1000.pt", weights_only=True)["m"]["0"].dtype, torch.float64)

    def test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job(self):
        gate_spec = importlib.util.spec_from_file_location("fix1_real_gate", ROOT / "code/lab/runners/c10w_p2_gate.py")
        gate = importlib.util.module_from_spec(gate_spec); gate_spec.loader.exec_module(gate)
        for mode in ("idle", "competing", "different_command"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); launcher = root / "code/lab/runners/run_c10z_v7_diag.py"; launcher.parent.mkdir()
                launcher.write_bytes((ROOT / "code/lab/runners/run_c10z_v7_diag.py").read_bytes())
                spec = importlib.util.spec_from_file_location("fix1_launcher_inventory", launcher)
                L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
                utc = "20261009T000000Z"; out = root / "experiments/c10z/runs/c10z_v7_diagnostic" / utc; out.mkdir(parents=True)
                argv = [str(root / ".venv/bin/python"), "-B", str(launcher), "--utc", utc]
                lease = {"token": "CPU-ownership-fixture", "pid": 60001, "deadline_origin": L.LAUNCH_STARTED,
                         "cap_seconds": 3060, "supervisor_argv": argv, "source_sha256": hashlib.sha256(launcher.read_bytes()).hexdigest()}
                (out / "supervisor.json").write_text(json.dumps(lease))
                parent_command = " ".join(argv) if mode != "different_command" else argv[0] + " unrelated_training.py"
                inventory = "60001 " + parent_command + "\n60002 " + argv[0] + " worker.py\n"
                if mode == "competing": inventory += "60003 " + argv[0] + " c10y_calibration4.py\n"
                entered = []; refused = []
                def inventory_call(command, env=None):
                    if command == ["/bin/ps", "-axww", "-o", "pid=,command="]: return 0, inventory, ""
                    self.assertEqual(command, ["/usr/bin/env", "tmux", "list-sessions", "-F", "#{session_name}"])
                    return 1, "", "no server running on CPU-fixture"
                with patch.object(L, "gate_module", return_value=gate), \
                     patch.object(gate, "check_fingerprint", return_value={"ok": True}), \
                     patch.object(gate, "run", side_effect=inventory_call), \
                     patch.object(os, "getpid", return_value=60002), patch.object(os, "getppid", return_value=60001), \
                     patch.dict(os.environ, C10Z_V7_SUPERVISOR_TOKEN=lease["token"], C10Z_V7_LAUNCH_STARTED=str(L.LAUNCH_STARTED)), \
                     patch.object(L.runpy, "run_path", side_effect=lambda *a, **kw: entered.append(True)), \
                     patch.object(sys, "argv", [str(launcher)]):
                    try: L.worker(utc)
                    except ValueError as exc: refused.append(str(exc))
                print("FIX1_PARENT_INVENTORY_CONTROL mode=%s reached_entry=%s refusal=%s" % (mode, bool(entered), refused))
                self.assertEqual(bool(entered), mode == "idle", "verified model-free supervisor counted as competing compute")
                if mode == "competing": self.assertIn("c10y_calibration4.py", refused[0])

    def test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure(self):
        for second in (False, True):
            with self.subTest(process2=second), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); out = root / "out"; source = root / "source"; out.mkdir(); source.mkdir()
                s, stats = self.session(out, input_dir=source if second else None)
                G = torch.diag(torch.tensor([-1., 1., 1.], dtype=torch.float64))
                s.compute_G = lambda: G
                if second:
                    with (source / "dstats.pt").open("xb") as f: torch.save(stats, f)
                    with (source / "G.pt").open("xb") as f: torch.save(G, f)
                with patch.object(os, "fsync", wraps=os.fsync) as sync:
                    with self.assertRaisesRegex(D.R.Halt, "HALTED-V8"): s.prepare_instruments()
                print("FIX1_V8_CONTROL process2=%s dstats=%s G=%s" % (second, (out / "dstats.pt").exists(), (out / "G.pt").exists()))
                self.assertTrue((out / "G.pt").is_file(), "forced V8 failure lost already obtained G")
                self.assertTrue(torch.equal(torch.load(out / "G.pt", weights_only=True), G))
                self.assertEqual(torch.load(out / "dstats.pt", weights_only=True)["dataset"], stats["dataset"])
                self.assertGreaterEqual(sync.call_count, 2)
                if second: self.assertEqual((out / "G.pt").read_bytes(), (source / "G.pt").read_bytes())


def old_prepare_instruments(self):
    """Frozen pre-change test oracle, copied from driver :1085-1116 before edits."""
    D.R.require(self.gates.law3,"HALTED-V4","instrument preparation before LAW#3")
    if self.loaded_manifest is not None:
        self.dstats=torch.load(self.input_dir/"dstats.pt",map_location="cpu",weights_only=True)
        self.G=torch.load(self.input_dir/"G.pt",map_location="cpu",weights_only=True)
    else:
        self.dstats=self.compute_dstats();self.G=self.compute_G()
    self.D={};self.D_floored=0
    for l,m in self.dstats["m"].items():
        self.D[int(l)],n=D.null_weights(m);self.D_floored+=n
    try:self.cholesky=torch.linalg.cholesky(D.torch_cpu64(self.G))
    except RuntimeError as exc:raise D.R.Halt("HALTED-V8",str(exc)) from exc
    self.checks["V8"]={"cholesky":True,"condition":float(torch.linalg.cond(self.G))}
    correlations={}
    for l in range(4,13):
        path=self.covariance_paths()[str(l)]
        with np.load(path,allow_pickle=False) as stat:
            diagonal=np.diag(stat["mom2.mom2"])/int(stat["mom2.count"])
        correlations[str(l)]=D.spearman(self.dstats["m"][str(l)].tolist(),diagonal.tolist())
    self.checks["V7"]={"spearman":correlations,"late_layers_fidelity":"UNVERIFIED: no cached late-layer reference"}
    D.R.require(all(v>=.8 for v in correlations.values()),"HALTED-V7","D/cache Spearman <.80")
    if self.loaded_manifest is not None:
        for name in ("dstats.pt","G.pt"):
            with (self.out/name).open("xb") as f:
                f.write((self.input_dir/name).read_bytes());f.flush();os.fsync(f.fileno())
    else:
        self.save_tensor_file("dstats.pt",self.dstats);self.save_tensor_file("G.pt",self.G)
    audit=D.overlap_audit([t.format(self.H.CANON) for t in self.templates],self.dstats["dataset"]["texts"],self.H.PTEST)
    D.write_json(self.out/"overlap_audit.json",audit)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    assert "c10e_bandknob" not in sys.modules and "transformers" not in sys.modules
    print("C10Z_V7_DIAG_SELFTEST_" + ("PASS" if result.wasSuccessful() else "FAIL") + " tests=" + str(result.testsRun))
    sys.exit(0 if result.wasSuccessful() else 1)
