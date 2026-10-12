"""D-ML-1 model-free, CPU-only contract tests. Never imports the harness."""
import ast
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import numpy as np
import torch

torch.set_num_threads(8)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
A1, A2, A7 = "A1_single", "A2_coherent2", "A7_coined_coined"
MINT = ["mint1_s0", "mint1_s1", "mint1_s2"]
BAND = [4, 5, 6, 7, 8]


def module(case, name):
    case.assertTrue((ROOT / (name.replace(".", "/") + ".py")).is_file(),
                    "missing implementation: " + name)
    return importlib.import_module(name)


class Sink:
    def __init__(self):
        self.rows = []

    def __call__(self, run_dir, event_type, **fields):
        self.rows.append(dict(type=event_type, **fields))


def harness():
    """Execute only the frozen function definition, over tiny CPU tensors."""
    source = ast.parse((ROOT / "experiments/track_c/c10e_bandknob.py").read_text())
    definition = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "my_edit")
    subjects = [f"subject{i}" for i in range(24)]
    parameters = {f"w{l}": torch.zeros(2, 3, dtype=torch.float16) for l in BAND}

    def shape(matrix, wanted):
        if matrix.shape != wanted:
            raise ValueError("shape mismatch")
        return matrix

    def contexts(model, tok):
        return CONTEXT_TEMPLATES_CACHE

    def keys(model, tok, requests, hp, layer, ctx):
        return torch.ones(len(requests), 3, dtype=torch.float16)

    scope = dict(torch=torch, os=os, DEV="cpu", _LAW5_DEFAULT_CTX=False,
                 Z_OVERRIDE=None, Z_OVERRIDE_HITS=0, PROJECTOR="nullspace",
                 _CANDIDATE_RECIPE=False, L2=1., get_context_templates=contexts,
                 model=types.SimpleNamespace(named_parameters=lambda: parameters.items()), tok=None,
                 compute_z=lambda *args: torch.ones(2, dtype=torch.float16), compute_ks=keys,
                 get_module_input_output_at_words=lambda model, tok, layer, **kw:
                 (None, torch.zeros(len(kw["words"]), 2, dtype=torch.float16)),
                 weight_name=lambda hp, layer: f"w{layer}", upd_matrix_match_shape=shape)
    exec(compile(ast.Module(body=[definition], type_ignores=[]), "<frozen CPU my_edit>", "exec"), scope)
    hp = types.SimpleNamespace(layers=BAND, layer_module_tmp="layer{}", fact_token="subject_last")
    requests = [dict(subject=s, prompt="{}", target_new={"str": " value"}) for s in subjects]
    H = types.SimpleNamespace(my_edit=scope["my_edit"], upd_matrix_match_shape=shape,
                              FICTION=subjects, _LAW5_DEFAULT_CTX=False, ARMS={A7: {s: "value" for s in subjects}},
                              get_context_templates=contexts, model=scope["model"], tok=None,
                              Z_OVERRIDE=None, Z_OVERRIDE_HITS=0, parameters=parameters)
    return H, hp, requests, [torch.eye(3) for _ in BAND], scope


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fp = {"ok": True, "output": "engine fingerprint PASS"}
        self.clear = {"ok": True, "blocking_processes": [], "blocking_tmux": []}
        self.record = {"no_other_coordinator_live_or_pending": True, "terminal_sources": [], "blocking_processes": []}
        for job in ("c10x-rerun3", "astra-attempt3"):
            path = self.root / (job + ".json")
            path.write_text(json.dumps({"status": "HALTED", "past_last_gated_stage": True}))
            self.record["terminal_sources"].append(dict(coordinator=job, path=str(path),
                                                      sha256=hashlib.sha256(path.read_bytes()).hexdigest()))

    def decide(self, kind="cpu", gpu=None, admission=None, memory=20.):
        A = module(self, "tools.mathlab_admit")
        return A.decide(kind, admission=self.record if admission is None else admission,
                        fingerprint=self.fp, gpu=self.clear if gpu is None else gpu,
                        available_gib=memory, root=ROOT)

    def test_clean_cpu_admission(self):
        self.assertTrue(self.decide()["allowed"])

    def test_dispatch_rechecks_lead_identity_and_current_inventory_before_import(self):
        A = module(self, "tools.mathlab_admit")
        from tools import mathlab_runtime as R
        lead = self.root / "lead.json"; lead.write_text(json.dumps(self.record))
        run_dir = self.root / "run"
        R.Run(run_dir, 1, "Fixture", 3600, sample=lambda: 20.)
        proof = dict(self.decide("harvest"), launcher_pid=os.getpid(),
                     lead_source={"path": str(lead), "sha256": R.sha_file(lead)})
        R.write_new(run_dir / "admission.json", proof)
        with patch.object(A, "probe", return_value=self.decide("harvest")) as probe:
            self.assertTrue(A.dispatch_check(run_dir, "harvest", lead)["allowed"])
            self.assertEqual(probe.call_args.args, ("harvest", self.record))
        lead.write_text('{}')
        with patch.object(A, "probe") as probe:
            with self.assertRaisesRegex(ValueError, "ADMISSION"):
                A.dispatch_check(run_dir, "harvest", lead)
            probe.assert_not_called()
        lead.write_text(json.dumps(self.record))
        with patch.object(A, "probe", return_value=dict(allowed=False, reasons=["new blocker"])):
            with self.assertRaisesRegex(ValueError, "ADMISSION"):
                A.dispatch_check(run_dir, "harvest", lead)

    def test_saved_admission_cannot_be_replayed_by_another_process_or_after_finish(self):
        A = module(self, "tools.mathlab_admit")
        from tools import mathlab_runtime as R
        run_dir = self.root / "run"
        run = R.Run(run_dir, 2, "Fixture", 6540, sample=lambda: 20.)
        proof = dict(self.decide(), launcher_pid=os.getpid() + 1, lead_source=None)
        R.write_new(run_dir / "admission.json", proof)
        with self.assertRaisesRegex(ValueError, "ADMISSION"):
            A.dispatch_check(run_dir, "cpu")
        proof["launcher_pid"] = os.getpid()
        (run_dir / "admission.json").write_text(json.dumps(proof))
        run.event("run_finished", outcome="PASS", summary="finished")
        with self.assertRaisesRegex(ValueError, "ADMISSION"):
            A.dispatch_check(run_dir, "cpu")

    def test_probe_error_cannot_use_tail_exception(self):
        self.assertFalse(self.decide(gpu={"ok": False, "reason": "ps error", "blocking_processes": []})["allowed"])

    def test_tmux_session_cannot_use_tail_exception(self):
        self.assertFalse(self.decide(gpu={"ok": False, "blocking_processes": [], "blocking_tmux": ["autoresearch"]})["allowed"])

    def test_missing_inventory_is_not_clear(self):
        self.assertFalse(self.decide(gpu={"ok": True})["allowed"])

    def test_unaccounted_process_refuses(self):
        self.assertFalse(self.decide(gpu={"ok": False, "blocking_processes": ["9 python job.py"], "blocking_tmux": []})["allowed"])

    def tail(self):
        ref = self.record["terminal_sources"][0]
        self.record["blocking_processes"] = [dict(pid=9, command="python job.py", coordinator="c10x-rerun3",
                                                 status_file=ref["path"], sha256=ref["sha256"])]
        return {"ok": False, "blocking_processes": ["9 python job.py"], "blocking_tmux": []}

    def test_exact_tail_cpu_only(self):
        gpu = self.tail()
        self.assertTrue(self.decide(gpu=gpu)["allowed"])
        self.assertFalse(self.decide(kind="harvest", gpu=gpu)["allowed"])

    def test_tail_pid_command_hash_stage_and_duplicates_refuse(self):
        gpu = self.tail()
        for field, value in (("pid", 10), ("command", "python other.py"), ("sha256", "0" * 64)):
            with self.subTest(field=field):
                bad = copy.deepcopy(self.record); bad["blocking_processes"][0][field] = value
                self.assertFalse(self.decide(gpu=gpu, admission=bad)["allowed"])
        bad = copy.deepcopy(self.record); bad["blocking_processes"] *= 2
        self.assertFalse(self.decide(gpu=gpu, admission=bad)["allowed"])
        path = Path(self.record["blocking_processes"][0]["status_file"])
        path.write_text('{"status":"RUNNING","past_last_gated_stage":false}')
        self.record["blocking_processes"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertFalse(self.decide(gpu=gpu)["allowed"])

    def test_harvest_requires_both_terminal_status_hashes_and_queue_statement(self):
        self.assertTrue(self.decide(kind="harvest")["allowed"])
        for key, value in (("terminal_sources", self.record["terminal_sources"][:1]),
                           ("no_other_coordinator_live_or_pending", False)):
            bad = dict(self.record); bad[key] = value
            self.assertFalse(self.decide(kind="harvest", admission=bad)["allowed"])
        Path(self.record["terminal_sources"][0]["path"]).write_text('{"status":"RUNNING"}')
        self.assertFalse(self.decide(kind="harvest")["allowed"])

    def test_fingerprint_and_memory_refusals(self):
        self.fp["ok"] = False
        self.assertFalse(self.decide()["allowed"])
        self.fp["ok"] = True
        self.assertFalse(self.decide(memory=7.999)["allowed"])
        self.assertTrue(self.decide(memory=8.)["allowed"])


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.H, self.hp, self.requests, self.P, self.scope = harness()

    def observer(self):
        return module(self, "tools.mathlab_harvest").EditObserver(self.H)

    def test_original_code_matches_after_rebinding_and_return_is_unique(self):
        O = self.observer(); original = self.H.my_edit
        with O.bound():
            self.assertIsNot(self.H.my_edit.__code__, original.__code__)
            self.H.my_edit(self.hp, self.requests, self.P, [torch.zeros(3, 3) for _ in BAND])
        self.assertIs(self.H.my_edit, original)
        self.assertIsNone(sys.getprofile())
        self.assertEqual([(x["i"], x["layer"]) for x in O.writes[0]["captures"]], list(enumerate(BAND)))
        self.assertEqual(O.writes[0]["return_count"], 1)
        self.assertEqual(O.writes[0]["arm"], A7)

    def test_shape_call_from_unrelated_code_is_ignored(self):
        O = self.observer()
        def engine(matrix):
            return self.H.upd_matrix_match_shape(matrix, matrix.shape)
        O.profile(types.SimpleNamespace(f_code=engine.__code__, f_back=None), "call", None)
        self.assertEqual(O.writes, [])

    def test_law5_tag_precedes_24_subject_assertion_and_discards_tensors(self):
        O = self.observer(); self.H._LAW5_DEFAULT_CTX = self.scope["_LAW5_DEFAULT_CTX"] = True
        with O.bound():
            self.H.my_edit(self.hp, self.requests[:1], self.P, [torch.zeros(3, 3) for _ in BAND])
        self.assertEqual(O.writes[0]["tag"], "law5")
        self.assertEqual(len(O.writes[0]["captures"]), 5)
        self.assertNotIn("tensors", O.writes[0])

    def test_capture_counts_0_4_6_wrong_order_and_missing_return_halt(self):
        O = self.observer()
        for layers, returns in (([], 1), (BAND[:4], 1), (BAND + [9], 1), ([5, 4, 6, 7, 8], 1), (BAND, 0), (BAND, 2)):
            with self.subTest(layers=layers, returns=returns), self.assertRaisesRegex(ValueError, "CAPTURE"):
                O.validate_coverage([dict(i=i, layer=l) for i, l in enumerate(layers)], returns)

    def test_preexisting_profile_refusal_and_exception_cleanup(self):
        O = self.observer()
        def existing(*args):
            return None
        try:
            sys.setprofile(existing)
            with O.bound(), self.assertRaisesRegex(ValueError, "PROFILER"):
                self.H.my_edit(self.hp, self.requests, self.P, [])
        finally:
            sys.setprofile(None)
        with O.bound(), self.assertRaises(IndexError):
            self.H.my_edit(self.hp, self.requests, self.P, [])
        self.assertIsNone(sys.getprofile())

    def test_science_subject_mismatch_and_nonzero_cache_halt(self):
        O = self.observer()
        bad = copy.deepcopy(self.requests); bad[0]["subject"] = "wrong"
        with O.bound(), self.assertRaisesRegex(ValueError, "SUBJECT"):
            self.H.my_edit(self.hp, bad, self.P, [torch.zeros(3, 3) for _ in BAND])
        with O.bound(), self.assertRaisesRegex(ValueError, "CACHE"):
            self.H.my_edit(self.hp, self.requests, self.P, [torch.eye(3) for _ in BAND])

    def test_same_dtype_cpu_copy_offset_noncontiguous_and_source_unchanged(self):
        H = module(self, "tools.mathlab_harvest")
        x = torch.arange(96, dtype=torch.float16).reshape(4, 6, 4); source = x.clone()
        for view in (x[1:], x[0, -1], *x.chunk(3, 1), x.transpose(0, 2)):
            got = H.cpu_copy(view)
            self.assertTrue(torch.equal(got, view.cpu()))
            self.assertEqual(got.dtype, view.dtype)
            got.zero_()
            self.assertTrue(torch.equal(x, source))

    def test_context_pin_restores_after_body_error_and_detects_drift(self):
        H = module(self, "tools.mathlab_harvest"); ctx = [["{}"], ["prefix. {}"]]
        namespace = self.H.get_context_templates.__globals__; namespace["CONTEXT_TEMPLATES_CACHE"] = None
        digest = hashlib.sha256(json.dumps(ctx, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        with self.assertRaisesRegex(RuntimeError, "body"):
            with H.lab_pinned_contexts(self.H, ctx, digest):
                raise RuntimeError("body")
        self.assertIsNone(namespace["CONTEXT_TEMPLATES_CACHE"])
        with self.assertRaisesRegex(ValueError, "DRIFT"):
            with H.lab_pinned_contexts(self.H, ctx, digest):
                namespace["CONTEXT_TEMPLATES_CACHE"] = []
        self.assertIsNone(namespace["CONTEXT_TEMPLATES_CACHE"])

    def test_parity_trials_restore_and_start_with_distinct_zero_caches(self):
        H = module(self, "tools.mathlab_harvest"); starts = []; caches = []
        def edit(hp, requests, P, cache):
            starts.append([v.clone() for v in self.H.parameters.values()]); caches.append(cache)
            for v in self.H.parameters.values(): v.add_(1)
            cache[0].add_(1)
        def restore(hp, snap):
            for l, v in snap.items(): self.H.parameters[f"w{l}"].copy_(v)
        self.H.restore_layers = restore
        self.H.snap_layers = lambda hp: {l: self.H.parameters[f"w{l}"].clone() for l in BAND}
        observed = types.SimpleNamespace(call=edit, last_capture_count=5)
        result = H.parity_trial(self.H, self.hp, self.requests, self.P, edit, observed,
                                torch.ones(2, 24), self.H.snap_layers(self.hp))
        self.assertTrue(result["passed"])
        self.assertEqual(len(starts), 2); self.assertIsNot(caches[0], caches[1])
        self.assertTrue(all(torch.count_nonzero(v) == 0 for row in starts for v in row))
        self.assertTrue(all(torch.count_nonzero(v) == 0 for v in self.H.parameters.values()))


class ReplayTests(unittest.TestCase):
    def test_source_snapshot_covers_engine_primitives_and_detects_changes(self):
        H = module(self, "tools.mathlab_harvest")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            names = [*H.AUDIT_SOURCES, "docs/MATHLAB_PREREG.md", "configs/hparams/qwen25_3b_memit_hparams.json",
                     "memit_dry_run/memit/globals.yml", "tools/mathlab_admit.py", "tools/mathlab_runtime.py",
                     "tools/mathlab_harvest.py", "tools/mathlab_events.py", "tools/c10w_p2_gate.py", "tools/engine_fingerprint.py",
                     "memit_dry_run/memit/memit/compute_ks.py", "memit_dry_run/memit/rome/repr_tools.py"]
            for name in names:
                path = root/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes((ROOT/name).read_bytes())
            before = H.source_snapshot(root)
            self.assertEqual(set(before),set(names))
            changed = root/"memit_dry_run/memit/rome/repr_tools.py"
            changed.write_bytes(changed.read_bytes()+b'\n# fixture mutation\n')
            self.assertNotEqual(before,H.source_snapshot(root))
            self.assertNotIn("c10e_bandknob",sys.modules)
    def test_missing_seed_target_or_step0_is_seed_specific_source_failure(self):
        H = module(self, "tools.mathlab_harvest")
        R = module(self, "tools.mathlab_runtime")
        for missing in ("zs/F_r0_mint1_s1.pt", "step0/F_r0_mint1_s1.json", "F_r0_mint1_s1.json",
                        "zs/F_r0_mint1_s0.pt", "step0/F_r0_mint1_s0.json"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory(dir="/private/tmp") as td:
                root = Path(td)
                base = root / H.BASE
                for source in (ROOT / H.BASE).glob("F_r0_*.json"):
                    if source.name == missing: continue
                    (base / source.name).parent.mkdir(parents=True, exist_ok=True)
                    (base / source.name).write_bytes(source.read_bytes())
                for folder in ("step0", "zs"):
                    for source in (ROOT / H.BASE / folder).glob("F_r0_mint1_s*.*"):
                        if folder + "/" + source.name == missing: continue
                        (base / folder).mkdir(parents=True, exist_ok=True)
                        (base / folder / source.name).write_bytes(source.read_bytes())
                records, identity = H.frozen_records(root)
                self.assertTrue(identity["contexts_shared"])
                missing_seed = 0 if "s0" in missing else 1
                self.assertEqual([a for a in MINT if identity["seed_sources"][a]["passed"]],
                                 [a for seed, a in enumerate(MINT) if seed != missing_seed])
                self.assertIn("reason", identity["seed_sources"][MINT[missing_seed]])
                self.assertEqual(identity["context_source_arm"], MINT[0])
                self.assertEqual(identity["context_source"]["json_pointer"], "/ctx")
                self.assertEqual(identity["context_source"]["sha256"], R.sha_file(identity["context_source"]["path"]))
    def test_missing_authoritative_s0_context_refuses_shared_input(self):
        H = module(self, "tools.mathlab_harvest")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); base = root / H.BASE
            base.mkdir(parents=True)
            source = ROOT / H.BASE / "F_r0_multi_snone.json"
            (base / source.name).write_bytes(source.read_bytes())
            with self.assertRaisesRegex(ValueError, "CONTEXT"):
                H.frozen_records(root)
    def test_pinned_tokenizer_identity_ignores_transient_batch_settings_without_mutation(self):
        from tokenizers import Tokenizer
        from tokenizers.models import WordLevel
        H = module(self, "tools.mathlab_harvest")
        live = Tokenizer(WordLevel({"[UNK]": 0, "subject": 1}, unk_token="[UNK]"))
        base = Tokenizer.from_str(live.to_str())
        live.enable_padding(pad_id=0, pad_token="[UNK]"); live.enable_truncation(16)
        before = live.to_str()
        self.assertNotEqual(before, base.to_str())
        self.assertEqual(H.tokenizer_identity(types.SimpleNamespace(backend_tokenizer=live)),
                         H.tokenizer_identity(types.SimpleNamespace(backend_tokenizer=base)))
        self.assertEqual(live.to_str(), before)
        altered = Tokenizer(WordLevel({"[UNK]": 0, "other": 1}, unk_token="[UNK]"))
        self.assertNotEqual(H.tokenizer_identity(types.SimpleNamespace(backend_tokenizer=altered)),
                            H.tokenizer_identity(types.SimpleNamespace(backend_tokenizer=base)))
    def test_shared_failure_invalidates_all_and_per_arm_failure_only_one(self):
        H = module(self, "tools.mathlab_harvest")
        self.assertEqual(H.replay_admission(False, {a: True for a in MINT})["admitted"], [])
        got = H.replay_admission(True, dict(zip(MINT, [True, False, True])))
        self.assertEqual(got["admitted"], [MINT[0], MINT[2]])
        self.assertEqual(got["arms"][MINT[1]], "INVALID-REPLAY")

    def test_p2_enumerated_fields_accept_wordlist_metadata_but_not_count_or_rows(self):
        H = module(self, "tools.mathlab_harvest")
        p2 = dict(ok=True, checks={"inventory_unchanged": True}, changed=[], inventory_n=2376,
                  plain_n=396, rows=[dict(target_ids=[151665], expected_ids=[151665],
                                        contexts=[dict(prefix_ids=True, whole_ids=True, last_id=True)], checks={"ok": True})])
        saved = dict(p2, wordlist_replay={"extra": True})
        self.assertTrue(H.p2_equivalent(p2, saved))
        for key, value in (("inventory_n", 1398), ("plain_n", 233), ("changed", ["prompt"]), ("ok", False)):
            bad = dict(p2); bad[key] = value
            self.assertFalse(H.p2_equivalent(bad, saved))
        bad = copy.deepcopy(p2); bad["rows"][0]["target_ids"] = [0]
        self.assertFalse(H.p2_equivalent(bad, saved))

    def test_law3_counts_and_stage_order(self):
        H = module(self, "tools.mathlab_harvest")
        arms = {A1: dict(para_full_n=68, para_n=72), A2: dict(para_full_n=68, para_n=72),
                A7: dict(para_full_n=5, para_first_n=42, canon_full_n=5, para_n=72, canon_n=24)}
        self.assertTrue(H.baseline_gates(arms)["passed"])
        for arm, field, value in ((A1, "para_full_n", 67), (A2, "para_full_n", 67),
                                  (A7, "para_full_n", 19), (A7, "para_first_n", 41), (A7, "canon_full_n", 11)):
            bad = copy.deepcopy(arms); bad[arm][field] = value
            self.assertFalse(H.baseline_gates(bad)["passed"])
        calls = []
        with self.assertRaisesRegex(ValueError, "LAW3"):
            H.fresh_before_mint(lambda: {"passed": False}, lambda: calls.append("mint"))
        self.assertEqual(calls, [])
        self.assertEqual(H.fresh_before_mint(lambda: {"passed": True}, lambda: "mint"), "mint")

    def test_frozen_record_and_target_hashes_are_bound(self):
        H = module(self, "tools.mathlab_harvest")
        records, provenance = H.frozen_records(ROOT)
        self.assertEqual(provenance["ctx_sha256"], "8638d12c6d5844168e1577a459103fa309bcf995fc1225df7e716de11a87cdc9")
        self.assertEqual([records[a]["arm"]["para_full_binding_n"] for a in MINT], [46, 37, 40])
        self.assertTrue(all(provenance["seed_sources"][a]["passed"] for a in MINT))


class MathTests(unittest.TestCase):
    def core(self):
        return module(self, "mathlab.core")

    def test_fp32_projector_and_solve_are_exact_and_fp64_diagnostic_only(self):
        C = self.core(); cov = torch.diag(torch.tensor([0., .001, 1.]))
        P, n = C.projector(cov)
        self.assertEqual(n, 2); self.assertTrue(torch.equal(P, torch.diag(torch.tensor([1., 1., 0.]))))
        upd, diag = C.solve(P, torch.eye(3), torch.tensor([[2., 0., 0.], [0., 4., 0.]]), torch.zeros(3, 3))
        self.assertTrue(torch.equal(upd, torch.tensor([[1., 0., 0.], [0., 2., 0.]])))
        self.assertEqual(upd.dtype, torch.float32); self.assertIn("cond_A", diag)

    def test_relative_zero_denominator_is_invalid_and_projector_zero_probes_need_sha(self):
        C = self.core()
        with self.assertRaisesRegex(ValueError, "ARITHMETIC"):
            C.relative_error(torch.zeros(2), torch.zeros(2))
        ident = C.projector_identity(torch.zeros(3, 3), 0)
        self.assertTrue(C.projector_matches(torch.zeros(3, 3), 0, ident))
        ident["sha256"] = "0" * 64
        self.assertFalse(C.projector_matches(torch.zeros(3, 3), 0, ident))

    def test_frozen_mean_clip_and_even_median(self):
        C = self.core()
        self.assertEqual(C.score_values("rho", np.tile([-1., .5, 2.], (24, 1))), .5)
        self.assertEqual(C.score_values("coll", np.arange(72.).reshape(24, 3)), -35.5)

    def test_proxy_position_sum_and_keyed_transfer(self):
        C = self.core(); d = {l: torch.zeros(1, 1) for l in BAND}; d[4][0, 0] = 1.
        specs = [dict(key=f"p{i}", kind="PTEST", subject_id=i // 3, template_id=i % 3) for i in range(72)]
        clean = {}
        for spec in specs:
            key = spec["key"]; clean[key + ".subject_last"] = torch.tensor(1)
            for l in BAND: clean[f"{key}.l{l}.k"] = torch.ones(2, 1)
            clean[key + ".l8.h"] = torch.zeros(2, 1)
        got = C.proxy_values(d, clean, torch.full((1, 24), 2.), specs)
        self.assertEqual(got["rho"]["score"], .5); self.assertEqual(got["coll"]["score"], -1.)
        bad = C.proxy_values(d, clean, torch.zeros(1, 24), specs)
        self.assertEqual(bad["rho"]["status"], "INVALID-ARITHMETIC")
        self.assertEqual(bad["coll"]["status"], "VALID")
        d[4].zero_(); bad = C.proxy_values(d, clean, torch.zeros(1, 24), specs)
        self.assertTrue(all(x["status"] == "INVALID-ARITHMETIC" for x in bad.values()))

    def test_nan_is_not_excluded_or_epsilon_adjusted(self):
        C = self.core()
        for x in (np.nan, np.inf):
            values = np.ones((24, 3)); values[0, 0] = x
            with self.assertRaisesRegex(ValueError, "ARITHMETIC"):
                C.score_values("rho", values)

    def test_gate2b_failed_approximation_is_scope_only(self):
        C = self.core(); ref = torch.eye(2)
        self.assertEqual(C.approximation_scope({4: (ref, ref), 5: (ref, ref)}), "ALT-SOLVES-ADMITTED")
        self.assertEqual(C.approximation_scope({4: (ref * -1, ref)}), "OPERANDS-ONLY")

    def data(self):
        outcomes = {A1: 68, A2: 71, A7: 14, **dict(zip(MINT, [46, 37, 40]))}
        rho = {a: np.full((24, 3), v) for a, v in zip([A1, A2, *MINT, A7], [.95, .96, .7, .5, .6, .2])}
        coll = {a: 1 - v for a, v in rho.items()}
        return {"rho": rho, "coll": coll}, outcomes

    def test_paired_bootstrap_is_pcg64_zero_multiplicities_and_deterministic(self):
        C = self.core(); draws = C.bootstrap_draws()
        expected = np.random.Generator(np.random.PCG64(0)).integers(0, 24, size=24)
        self.assertEqual(draws.shape, (2000, 24)); np.testing.assert_array_equal(draws[0], expected)
        np.testing.assert_array_equal(draws, C.bootstrap_draws())
        self.assertLess(len(set(draws[0])), 24)
        data, counts = self.data(); self.assertEqual(C.calibrate(data, counts, MINT), C.calibrate(data, counts, MINT))

    def test_nine_and_six_orderings_strictly_with_1900_bar(self):
        C = self.core(); data, counts = self.data()
        got = C.calibrate(data, counts, MINT)
        self.assertEqual(got["outcome"], "PASS"); self.assertEqual(got["ordering_n"], 9)
        self.assertTrue(all(n == 2000 for n in got["proxies"]["rho"]["bootstrap_counts"].values()))
        got = C.calibrate(data, counts, MINT[:2]); self.assertEqual(got["ordering_n"], 6)
        for proxy in data: data[proxy][MINT[0]] = data[proxy][A7].copy()
        self.assertEqual(C.calibrate(data, counts, MINT)["outcome"], "FAIL")
        self.assertTrue(C.ordering_passes(True, 1900)); self.assertFalse(C.ordering_passes(True, 1899))
        self.assertFalse(C.ordering_passes(False, 2000))

    def test_invalid_tiers_shared_failure_fewer_mints_and_arithmetic_routing(self):
        C = self.core(); data, counts = self.data()
        self.assertEqual(C.calibrate(data, counts, MINT[:1])["outcome"], "INVALID")
        self.assertEqual(C.calibrate(data, counts, MINT, shared_ok=False)["outcome"], "INVALID")
        counts[A1] = 55
        self.assertEqual(C.calibrate(data, counts, MINT)["reason"], "INVALID-TIERS")
        counts[A1] = 68
        data["rho"][A1] = None
        self.assertEqual(C.calibrate(data, counts, MINT)["outcome"], "PASS")
        data["coll"][A1] = None
        self.assertEqual(C.calibrate(data, counts, MINT)["outcome"], "INVALID")


class ResourceArtifactTests(unittest.TestCase):
    def test_admission_probe_error_emits_failed_gate_and_staged_closeout(self):
        A = module(self, "tools.mathlab_admit")
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            with patch.object(A, "W", root), patch.object(A, "probe", side_effect=PermissionError("fixture ps refusal")), \
                 patch.object(sys, "argv", ["admit", "--kind", "cpu"]), patch("builtins.print"):
                self.assertEqual(A.main(), 3)
            runs = list((root / "results/mathlab_staging/runs").iterdir())
            self.assertEqual(len(runs), 1)
            rows, errors = read_events(runs[0] / "events.jsonl")
            self.assertEqual(errors, [])
            gates = [r for r in rows if r["type"] == "gate_result" and r["gate_id"] == "admission"]
            self.assertEqual(len(gates), 1)
            self.assertFalse(gates[0]["passed"])
            self.assertTrue(gates[0]["plain_words"])
            self.assertTrue({"finding_staged", "run_finished"} <= {r["type"] for r in rows})
    def test_internal_cpu_budget_abort_counts_toward_operator_resource_rule(self):
        R = module(self, "tools.mathlab_runtime")
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            for i in range(3):
                run = R.Run(root / "results/mathlab_staging/runs" / f"m2_{i}", 2, "Fixture", 6540, sample=lambda: 20.)
                R.stage_halt(root, run.directory, "HALT-BUDGET", "internal CPU timeout", step=2)
                rows, errors = read_events(run.directory / "events.jsonl")
                self.assertEqual(errors, [])
                self.assertTrue(any(r["type"] == "halted" and r["reason"].startswith("STOPPED-DEADLINE:") for r in rows))
            with self.assertRaisesRegex(ValueError, "OPERATOR"):
                R.enforce_stop_policy(root, 2)

    def test_calibration_fail_remains_stop_when_index_later_aborts(self):
        R = module(self, "tools.mathlab_runtime")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            run = R.Run(root / "results/mathlab_staging/runs/m3", 3, "Fixture", 1800, sample=lambda: 20.)
            run.gate("calibration", "Frozen calibration", "FAIL", "PASS", False)
            R.stage_halt(root, run.directory, "CPU-ERROR", "index failure", step=3)
            with self.assertRaisesRegex(ValueError, "LAB-STOP"):
                R.enforce_stop_policy(root, 1)

    def test_cpu_runner_stages_pre_spawn_admission_refusal(self):
        C = module(self, "tools.mathlab_cpu_runner")
        from tools import mathlab_admit as A
        from tools import mathlab_runtime as R
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); run_dir = root / "run"
            R.Run(run_dir, 2, "Fixture", 6540, sample=lambda: 20.)
            with patch.object(C, "W", root), patch.object(C, "validate_notebook", return_value=2), \
                 patch.object(R, "verify_prereg"), patch.object(A, "dispatch_check", side_effect=R.Halt("ADMISSION", "fixture refusal")), \
                 patch.object(C.subprocess, "Popen") as spawned, \
                 patch.object(sys, "argv", ["runner", "fixture.py", "6540", "--run-dir", str(run_dir)]):
                with self.assertRaisesRegex(ValueError, "ADMISSION"): C.main()
                spawned.assert_not_called()
            rows, errors = read_events(run_dir / "events.jsonl")
            self.assertEqual(errors, [])
            self.assertTrue({"halted", "finding_staged", "run_finished"} <= {r["type"] for r in rows})

    def test_cpu_runner_stages_prereg_refusal_before_dispatch(self):
        C = module(self, "tools.mathlab_cpu_runner")
        from tools import mathlab_admit as A
        from tools import mathlab_runtime as R
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); run_dir = root / "run"
            R.Run(run_dir, 2, "Fixture", 6540, sample=lambda: 20.)
            with patch.object(C, "W", root), patch.object(C, "validate_notebook", return_value=2), \
                 patch.object(R, "verify_prereg", side_effect=R.Halt("PREREG", "fixture hash mismatch")), \
                 patch.object(A, "dispatch_check") as dispatch, patch.object(C.subprocess, "Popen") as spawned, \
                 patch.object(sys, "argv", ["runner", "fixture.py", "6540", "--run-dir", str(run_dir)]):
                with self.assertRaisesRegex(ValueError, "PREREG"): C.main()
                dispatch.assert_not_called(); spawned.assert_not_called()
            rows, errors = read_events(run_dir / "events.jsonl")
            self.assertEqual(errors, [])
            self.assertTrue({"gate_result", "halted", "finding_staged", "run_finished"} <= {r["type"] for r in rows})

    def test_cpu_runner_requires_a_passing_event_closeout_even_with_exit_zero(self):
        C = module(self, "tools.mathlab_cpu_runner")
        from tools import mathlab_admit as A
        from tools import mathlab_runtime as R
        from tools.mathlab_events import read_events
        for completion, expected in ((None,3),("INVALID",3),("FAIL",3),("PASS",0)):
            with self.subTest(completion=completion), tempfile.TemporaryDirectory(dir="/private/tmp") as td:
                root=Path(td); run_dir=root/"run"
                run=R.Run(run_dir,2,"Fixture",6540,sample=lambda:24.)
                if completion: run.event("run_finished",outcome=completion,summary="Fixture")
                process=types.SimpleNamespace(returncode=0,poll=lambda:0,pid=999)
                with patch.object(C,"W",root), patch.object(C,"validate_notebook",return_value=2), \
                     patch.object(R,"verify_prereg"), patch.object(A,"dispatch_check",return_value={"allowed":True}), \
                     patch.object(C.subprocess,"Popen",return_value=process), patch.object(C,"watch",return_value="PASS"), \
                     patch.object(sys,"argv",["runner","fixture.py","6540","--run-dir",str(run_dir)]):
                    self.assertEqual(C.main(),expected)
                rows,errors=read_events(run_dir/"events.jsonl")
                self.assertEqual(errors,[])
                self.assertEqual(rows[-1]["type"],"run_finished")
    def test_exception_discards_failed_stage_and_restores_only_enclosing_alarm(self):
        import signal
        R = module(self, "tools.mathlab_runtime")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            run = R.Run(Path(td), 2, "Fixture", 10, sample=lambda: 20.)
            with self.assertRaisesRegex(RuntimeError, "fixture"):
                with run.stage("outer", "Outer", 5, alarm=True):
                    raise RuntimeError("fixture")
            self.assertEqual(run.budget.active, [])
            self.assertEqual(signal.getitimer(signal.ITIMER_REAL)[0], 0)
            with run.stage("outer2", "Outer", 5, alarm=True):
                with self.assertRaisesRegex(RuntimeError, "fixture"):
                    with run.stage("inner", "Inner", 1, alarm=True):
                        raise RuntimeError("fixture")
                self.assertEqual([x[0] for x in run.budget.active], ["outer2"])
                self.assertGreater(signal.getitimer(signal.ITIMER_REAL)[0], 0)
            self.assertEqual(signal.getitimer(signal.ITIMER_REAL)[0], 0)

    def test_stop_policy_blocks_third_same_gate_harvest_repeated_2a_and_calibration_fail(self):
        R = module(self, "tools.mathlab_runtime")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            def failed(name, step, gate=None, code=None, outcome="INVALID"):
                run = R.Run(root / "results/mathlab_staging/runs" / name, step, "Fixture", 3600, sample=lambda: 20.)
                if gate: run.gate(gate, "Fixture gate", False, True, False)
                if code: run.event("halted", reason=code + ": fixture", diagnostic_path="fixture.json")
                run.event("run_finished", outcome=outcome, summary="Fixture")
            failed("h1", 1, code="LAW3")
            R.enforce_stop_policy(root, 1)
            failed("h2", 1, code="LAW3")
            with self.assertRaisesRegex(ValueError, "OPERATOR"):
                R.enforce_stop_policy(root, 1)
            failed("m2a", 2, gate="2a")
            R.enforce_stop_policy(root, 2)
            failed("m2b", 2, gate="2a")
            for step in (2, 3):
                with self.assertRaisesRegex(ValueError, "LAB-STOP"):
                    R.enforce_stop_policy(root, step)
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td)
            run = R.Run(root / "results/mathlab_staging/runs/m3", 3, "Fixture", 1800, sample=lambda: 20.)
            run.event("run_finished", outcome="FAIL", summary="Frozen calibration failed")
            for step in (1, 2, 3):
                with self.assertRaisesRegex(ValueError, "LAB-STOP"):
                    R.enforce_stop_policy(root, step)
    def test_vm_stat_uses_free_inactive_speculative_16384_pages(self):
        R = module(self, "tools.mathlab_runtime")
        text = 'Pages free: 100.\nPages inactive: 200.\nPages speculative: 300.\nPages purgeable: 999.\n'
        self.assertEqual(R.vm_available_gib(text), 600 * 16384 / 2 ** 30)
        with self.assertRaises(ValueError): R.vm_available_gib('permission denied')

    def test_pre_cell_reserve_wait_is_bounded_and_abort_is_staged(self):
        R = module(self, "tools.mathlab_runtime"); times = iter([0, 10, 300])
        with self.assertRaisesRegex(ValueError, "STOPPED-RESOURCE"):
            R.wait_for_memory(4., sample=lambda: 11., sleep=lambda s: None, clock=lambda: next(times))
        self.assertEqual(R.wait_for_memory(2., sample=lambda: 10.), 10.)

    def test_real_shared_events_integrate_and_non_gating_scope_does_not_stop(self):
        R = module(self, "tools.mathlab_runtime")
        from tools.mathlab_events import read_events, fold
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            run = R.Run(Path(td) / "events", 2, "Fixture self-test", 6540, sample=lambda: 20.)
            run.event("admission", allowed=True, reasons=[])
            with run.stage("reproduction", "Reproduce saved operands", 6540):
                run.event("progress", stage="reproduction", done=1, total=2, unit="writes")
                run.gate("2a", "Exact replay", 0., 1e-5, True)
                run.gate("2b", "First-order scope", "OPERANDS-ONLY", "ALT-SOLVES-ADMITTED", False)
            run.event("run_finished", outcome="PASS", summary="Exact replay passed; operands-only scope")
            rows, errors = read_events(run.directory / "events.jsonl")
            self.assertEqual(errors, []); self.assertEqual(fold(rows)["status"], "finished")
            self.assertEqual(fold(rows)["outcome"], "PASS")
            self.assertTrue({"stage_started", "progress", "gate_result", "resource_sample", "stage_finished"} <= {r["type"] for r in rows})

    def test_cpu_runner_enforces_frozen_deadlines_and_watchdog_floor(self):
        C = module(self, "tools.mathlab_cpu_runner")
        try:
            step = C.validate_notebook(ROOT / "mathlab/m2_solve_repro.py", 6540)
        except ValueError as error:
            self.fail("D-ML-2 step-2 deadline must be accepted: " + str(error))
        self.assertEqual(step, 2)
        self.assertEqual(C.validate_notebook(ROOT / "mathlab/m3_calibration.py", 1800), 3)
        for notebook, cap in (("m2_solve_repro.py", 2700), ("m2_solve_repro.py", 6539),
                              ("m2_solve_repro.py", 6541), ("m3_calibration.py", 1801)):
            with self.subTest(notebook=notebook, cap=cap), self.assertRaisesRegex(ValueError, "DEADLINE"):
                C.validate_notebook(ROOT / "mathlab" / notebook, cap)
        process = types.SimpleNamespace(poll=lambda: None, pid=999, returncode=None)
        sink = Sink()
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td, patch.object(C, "terminate") as killed:
            result = C.watch(process, Path(td), sample=lambda: 5.999, sleep=lambda s: None, sink=sink)
        self.assertEqual(result, "STOPPED-RESOURCE"); self.assertTrue(killed.called)

    def test_prereg_amendment_pin_accepts_only_exact_frozen_bytes(self):
        R = module(self, "tools.mathlab_runtime")
        self.assertEqual(R.PREREG_SHA, "4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507")
        R.verify_prereg(ROOT)
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); (root / "docs").mkdir()
            prereg = root / "docs/MATHLAB_PREREG.md"
            prereg.write_bytes((ROOT / "docs/MATHLAB_PREREG.md").read_bytes())
            R.verify_prereg(root)
            prereg.write_bytes(prereg.read_bytes() + b"\nchanged\n")
            with self.assertRaisesRegex(ValueError, "PREREG"):
                R.verify_prereg(root)

    def test_watchdog_reuses_cpu_samplers_and_handles_already_exited_parent(self):
        import psutil
        C = module(self, "tools.mathlab_cpu_runner")
        class Process:
            pid = 9001
            def __init__(self): self.calls = 0
            def children(self, recursive): return []
            def memory_info(self): return types.SimpleNamespace(rss=1024)
            def cpu_percent(self):
                self.calls += 1
                return 0. if self.calls == 1 else 100.
        polls=iter([None, None, 0])
        process=types.SimpleNamespace(pid=9001, poll=lambda: next(polls), returncode=0)
        sink=Sink()
        with patch.object(psutil, "Process", side_effect=lambda pid: Process()):
            self.assertEqual(C.watch(process, ROOT, sample=lambda: 20., sleep=lambda s: None, sink=sink), "PASS")
        self.assertGreater(max(r["cpu_pct"] for r in sink.rows if r["type"] == "resource_sample"), 0)
        polls=iter([None, 0]); process.poll=lambda: next(polls)
        with patch.object(psutil, "Process", side_effect=psutil.NoSuchProcess(9001)):
            self.assertEqual(C.watch(process, ROOT, sample=lambda: 20., sink=Sink()), "PASS")

    def test_harvest_launcher_refuses_before_dispatch(self):
        import subprocess
        launcher = ROOT / "tools/run_mathlab_harvest.sh"
        self.assertTrue(launcher.exists())
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); (root / ".venv/bin").mkdir(parents=True); (root / "bin").mkdir()
            (root / "tools").mkdir(); (root / "results/mathlab_staging/runs").mkdir(parents=True)
            script = root / "tools/run_mathlab_harvest.sh"; script.write_bytes(launcher.read_bytes())
            git = root / "bin/git"; git.write_text('#!/bin/sh\nprintenv MATHLAB_TEST_ROOT\n'); git.chmod(0o755)
            python = root / ".venv/bin/python"
            python.write_text('#!/bin/sh\ncase "$2" in *mathlab_admit.py) exit 3;; *) touch "$MATHLAB_TEST_ROOT/dispatched"; exit 0;; esac\n'); python.chmod(0o755)
            result = subprocess.run(["/bin/bash", str(script), str(root / "admission.json")], capture_output=True, text=True,
                                    env=dict(os.environ, PATH=str(root / "bin") + ":/usr/bin:/bin", MATHLAB_TEST_ROOT=str(root)))
            self.assertEqual(result.returncode, 3); self.assertFalse((root / "dispatched").exists())

    def test_cpu_launcher_accepts_only_amended_frozen_deadlines(self):
        import subprocess
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); (root / ".venv/bin").mkdir(parents=True); (root / "bin").mkdir()
            (root / "tools").mkdir()
            script = root / "tools/run_mathlab_cpu.sh"
            script.write_bytes((ROOT / "tools/run_mathlab_cpu.sh").read_bytes())
            git = root / "bin/git"; git.write_text('#!/bin/sh\nprintenv MATHLAB_TEST_ROOT\n'); git.chmod(0o755)
            python = root / ".venv/bin/python"
            python.write_text('#!/bin/sh\ntouch "$MATHLAB_TEST_ROOT/admitted"\nexit 29\n'); python.chmod(0o755)
            cases = [("mathlab/m2_solve_repro.py", 6540, True),
                     (str(root / "mathlab/m2_solve_repro.py"), 6540, True),
                     ("mathlab/m3_calibration.py", 1800, True),
                     (str(root / "mathlab/m3_calibration.py"), 1800, True),
                     ("mathlab/m2_solve_repro.py", 2700, False),
                     ("mathlab/m2_solve_repro.py", 6541, False),
                     ("mathlab/m3_calibration.py", 1801, False)]
            for notebook, cap, allowed in cases:
                with self.subTest(notebook=notebook, cap=cap):
                    (root / "admitted").unlink(missing_ok=True)
                    result = subprocess.run(["/bin/bash", str(script), notebook, str(cap)], capture_output=True, text=True,
                                            env=dict(os.environ, PATH=str(root / "bin") + ":/usr/bin:/bin", MATHLAB_TEST_ROOT=str(root)))
                    self.assertEqual(result.returncode, 29 if allowed else 3, result.stderr)
                    self.assertEqual((root / "admitted").exists(), allowed)

    def test_budget_projection_and_stage_cap(self):
        R = module(self, "tools.mathlab_runtime"); now = [0.]
        B = R.Budget(3600, clock=lambda: now[0]); now[0] = 3500.
        with self.assertRaisesRegex(ValueError, "HALT-BUDGET"):
            B.begin("clean", 300)
        self.assertTrue(B.last_projection["projected_end_s"] > 3600)

    def test_nested_stage_restores_outer_deadline_and_run_attach_keeps_one_start(self):
        import signal
        R = module(self, "tools.mathlab_runtime")
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            run = R.Run(Path(td) / "run", 1, "Fixture", 10, sample=lambda: 20.)
            attached = R.Run(run.directory, 1, "Fixture", 10, sample=lambda: 20., attach=True)
            with attached.stage("outer", "outer", 5, alarm=True):
                with attached.stage("inner", "inner", 1, alarm=True):
                    self.assertGreater(signal.getitimer(signal.ITIMER_REAL)[0], 0)
                self.assertGreater(signal.getitimer(signal.ITIMER_REAL)[0], 0)
            rows, errors = read_events(run.directory / "events.jsonl")
            self.assertEqual(errors, []); self.assertEqual(sum(r["type"] == "run_started" for r in rows), 1)

    def test_new_outputs_flat_cpu_and_sha_shape_dtype_manifest(self):
        R = module(self, "tools.mathlab_runtime")
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            out = R.new_directory(Path(td), "harvest", "fixed")
            with self.assertRaises(FileExistsError): R.new_directory(Path(td), "harvest", "fixed")
            ref = R.save_tensors(out / "clean.pt", {"k": torch.ones(2, 3, dtype=torch.float16)})
            self.assertEqual(ref["tensors"]["k"], {"shape": [2, 3], "dtype": "torch.float16"})
            self.assertEqual(ref["sha256"], hashlib.sha256((out / "clean.pt").read_bytes()).hexdigest())
            self.assertTrue(torch.equal(torch.load(out / "clean.pt", weights_only=True)["k"], torch.ones(2, 3, dtype=torch.float16)))
            with self.assertRaisesRegex(ValueError, "flat"):
                R.save_tensors(out / "bad.pt", {"nested": {"k": torch.ones(1)}})

    def test_halt_stages_immediately_preserves_harvest_and_emits_diagnostic(self):
        R = module(self, "tools.mathlab_runtime"); sink = Sink()
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); out = root / "results/mathlab/harvest_x"; out.mkdir(parents=True)
            (out / "kept.pt").write_bytes(b"keep")
            result = R.stage_halt(root, root / "results/mathlab_staging/runs/test", "CAPTURE", "bad order", sink=sink)
            self.assertTrue(Path(result["diagnostic_path"]).is_file()); self.assertTrue(Path(result["finding_path"]).is_file())
            self.assertEqual((out / "kept.pt").read_bytes(), b"keep")
            self.assertEqual([x["type"] for x in sink.rows], ["gate_result", "halted", "finding_staged", "run_finished"])
            self.assertFalse(sink.rows[0]["passed"])
            self.assertEqual(sink.rows[0]["bar"], dict(ordered_pairs=list(map(list,enumerate(BAND))), returns=1))

class NotebookContractTests(unittest.TestCase):
    def test_full_shape_measurements_set_svd_and_solve_cell_reserves(self):
        C = module(self, "mathlab.core")
        from mathlab.fixtures import make_harvest
        from tools import mathlab_runtime as R
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); harvest = make_harvest(root); last = [None]
            run = R.Run(root / "run", 2, "Fixture", 6540, sample=lambda: 24.)
            original_admit=run.pre_cell; original_projector=C.projector; original_solve=C.solve
            def admit(reserve):
                last[0]=reserve; original_admit(reserve)
            def measured_projector(*args):
                self.assertEqual(last[0], 5, "full-shape SVD measured 4.6088 GiB; D-ML-2 rounds up to 5")
                return original_projector(*args)
            def measured_solve(*args):
                self.assertEqual(last[0], 9, "full-shape solve measured 8.0843 GiB; reserve stays 9")
                return original_solve(*args)
            run.pre_cell=admit
            with patch.object(C, "projector", side_effect=measured_projector), patch.object(C, "solve", side_effect=measured_solve):
                C.reproduce(harvest, R.new_directory(root,"m2"), run)
            self.assertEqual(C.SVD_RESERVE_GIB, 5)
            self.assertEqual(C.SOLVE_RESERVE_GIB, 9)

    def test_notebook_boundary_uses_real_budget_events_and_non_stopping_2b(self):
        C = module(self, "mathlab.core")
        from mathlab.fixtures import make_harvest
        from tools import mathlab_runtime as R
        from tools.mathlab_events import read_events
        # Isolate the deadline contract from the separately tested prereg repin.
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td, \
             patch.object(R,"PREREG_SHA","4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507"):
            root=Path(td); harvest=make_harvest(root); run_dir=root/"run"
            R.Run(run_dir,2,"Fixture notebook",6540,sample=lambda:24.)
            R.write_new(run_dir/"admission.json",dict(allowed=True,kind="cpu",fixture=True))
            params=types.SimpleNamespace(harvest_dir=harvest,output_root=root/"outputs")
            real_run=R.Run
            def admitted_run(*args,**kw):
                return real_run(*args,sample=lambda:24.,**kw)
            with patch.dict(os.environ,MATHLAB_RUN_DIR=str(run_dir)), patch.object(R,"ROOT",root), \
                 patch.object(R,"Run",side_effect=admitted_run):
                result=C.run_notebook(2,params)
                with self.assertRaisesRegex(ValueError,"EVENTS"):
                    C.run_notebook(2,params)
            self.assertTrue(result["gate2a"]["passed"])
            self.assertEqual(result["gate2b"],"OPERANDS-ONLY")
            rows,errors=read_events(run_dir/"events.jsonl")
            self.assertEqual(errors,[])
            self.assertEqual(sum(r["type"]=="run_started" for r in rows),1)
            self.assertEqual(rows[-1]["type"],"run_finished")
            self.assertEqual(rows[-1]["outcome"],"PASS")
            stages=[r for r in rows if r["type"]=="stage_started"]
            self.assertEqual([(r["stage"],r["cap_s"]) for r in stages],[("reproduction",6540)])
    def test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events(self):
        C = module(self, "mathlab.core")
        from mathlab.fixtures import make_harvest
        from tools import mathlab_runtime as R
        from tools.mathlab_events import read_events
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            parent = Path(td); harvest = make_harvest(parent)
            out2 = R.new_directory(parent, "m2"); run2 = R.Run(parent / "run2", 2, "Fixture", 6540, sample=lambda: 20.)
            result2 = C.reproduce(harvest, out2, run2)
            self.assertTrue(result2["gate2a"]["passed"]); self.assertEqual(result2["gate2b"], "OPERANDS-ONLY")
            out3 = R.new_directory(parent, "m3"); run3 = R.Run(parent / "run3", 3, "Fixture", 1800, sample=lambda: 20.)
            result3 = C.calibration(harvest, out2, out3, run3)
            self.assertEqual(result3["outcome"], "PASS"); self.assertEqual(result3["ordering_n"], 9)
            self.assertEqual(result3["outcomes"][A1]["fresh_harvest_count"], 68)
            self.assertEqual(result3["outcomes"][A1]["historical_count_report_only"], 999)
            consistency = result3["consistency_checks"]
            self.assertTrue(consistency["non_gating"])
            self.assertEqual(consistency["injection_vs_write"]["injected_tau_by_construction"], 1)
            self.assertEqual(consistency["edited_model_injection"]["historical_para_full"], 23)
            self.assertEqual(consistency["edited_model_injection"]["current_A7_coll_score"], result3["raw"][A7]["coll"]["score"])
            rows, errors = read_events(run3.directory / "events.jsonl")
            self.assertEqual(errors, []); self.assertTrue(any(r.get("gate_id") == "calibration" and r["passed"] for r in rows))

    def test_invalid_tiers_are_checked_before_any_proxy_is_scored(self):
        C = module(self, "mathlab.core")
        from mathlab.fixtures import make_harvest
        from tools import mathlab_runtime as R
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            parent = Path(td); harvest = make_harvest(parent)
            out2 = R.new_directory(parent, "m2"); run2 = R.Run(parent / "run2", 2, "Fixture", 6540, sample=lambda: 20.)
            C.reproduce(harvest, out2, run2)
            changed = R.read_json(harvest / "manifest.json"); changed["outcomes"][A1]["used_for_calibration"] = 55
            (harvest / "manifest.json").write_text(json.dumps(changed))
            proof = R.read_json(out2 / "manifest.json"); proof["harvest"]["sha256"] = R.sha_file(harvest / "manifest.json")
            (out2 / "manifest.json").write_text(json.dumps(proof))
            out3 = R.new_directory(parent, "m3"); run3 = R.Run(parent / "run3", 3, "Fixture", 1800, sample=lambda: 20.)
            with patch.object(C, "proxy_values", side_effect=AssertionError("scored before tier validation")):
                self.assertEqual(C.calibration(harvest, out2, out3, run3)["reason"], "INVALID-TIERS")

    def test_notebooks_have_frozen_pep723_dependencies_and_no_science_imports(self):
        import tomllib
        for name in ("m2_solve_repro.py", "m3_calibration.py"):
            path = ROOT / "mathlab" / name; self.assertTrue(path.is_file(), "missing notebook: " + name)
            lines = path.read_text().splitlines(); start = lines.index("# /// script"); end = lines.index("# ///", start + 1)
            metadata = tomllib.loads("\n".join(x[2:] for x in lines[start + 1:end]))
            self.assertEqual(set(metadata["dependencies"]), {"marimo", "duckdb", "pydantic", "psutil", "numpy", "torch==2.8.0"})
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Import): names = [n.name for n in node.names]
                elif isinstance(node, ast.ImportFrom): names = [node.module or ""]
                else: continue
                self.assertFalse(any(n.startswith(("transformers", "c10e_bandknob", "memit")) for n in names))


if __name__ == "__main__":
    unittest.main(verbosity=2)
