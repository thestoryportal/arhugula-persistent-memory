import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""A1 population admission and retention controls; CPU fixtures, no science imports."""
import copy
from contextlib import contextmanager, redirect_stdout
import hashlib
import importlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import types
import unittest
from unittest.mock import patch

import torch
import c10z_astra_arms as D
import c10z_astra_read as R
import c10z_astra_selftest as ST
import c10z_v7_diag_selftest as VT

ROOT = Path(__file__).resolve().parents[2]
POP_PATH = "results/c10z_astra_attempt4_prep/reference_R1000.json"
POP_SHA = "a477f1c4917de988682da097d460c3d70b4c3bd33856d83c1d0c7714f78aab68"
ARTIFACT = json.loads((ROOT / POP_PATH).read_bytes())
ALTERNATIVE_ROW = None


@contextmanager
def amendment_fixture(status="DRAFT pending Astra"):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / D.PREREG; path.parent.mkdir(parents=True)
        raw = ("## §12 Amendment A1-POPULATION\n\n**Status:** " + status + "\n").encode()
        path.write_bytes(raw)
        pop = root / POP_PATH; pop.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / POP_PATH, pop)
        B = importlib.import_module("c10z_astra_benchmark")
        with patch.object(D, "ROOT", root), patch.object(B, "ROOT", root), \
             patch.object(R, "PREREG_SHA", hashlib.sha256(raw).hexdigest()):
            yield root


def selected_launch(root):
    path, binding = ST._bench_tree(root)
    go = ST._go_record(binding); go["prereg_sha256"] = R.PREREG_SHA
    go_path = root / "go.json"; go_path.write_text(json.dumps(go, indent=2))
    env = {"C10Z_GO_RECORD": str(go_path), "C10Z_BENCHMARK_RECORD": str(path)}
    benchmark, _, _ = D.benchmark_binding(env, go)
    launch = ST._launch(**binding["ceilings"], go=go, benchmark=benchmark,
                        go_sha256=hashlib.sha256(go_path.read_bytes()).hexdigest())
    return launch, env


def metadata(texts=False):
    data = copy.deepcopy(ARTIFACT["population"])
    data["dataset_identity"] = copy.deepcopy(ARTIFACT["dataset"])
    data["reference_population_sha256"] = POP_SHA
    if not texts: data.pop("texts")
    return data


def record():
    result = ST.fixture()
    parts = result["manifest"]["parts"]
    parts.update(dataset=metadata(), reference_population_sha256=POP_SHA,
                 safetensors=copy.deepcopy(ARTIFACT["model_files"]), tokenizer=copy.deepcopy(ARTIFACT["tokenizer_files"]),
                 covariances=copy.deepcopy(ARTIFACT["cache_files"]))
    parts["prereg_sha256"] = result["prereg_sha256"] = R.PREREG_SHA
    result["manifest"]["H_in"] = result["H_in"] = R.json_digest(parts)
    return result


def valid_alternative(data):
    # Replace one row with an actual different pinned R5000 row, keeping all provenance/counts consistent.
    global ALTERNATIVE_ROW
    if ALTERNATIVE_ROW is None:
        pins=json.loads((ROOT/ARTIFACT["provenance"]["pins_path"]).read_bytes())
        other=pins["populations"]["R5000"]
        ALTERNATIVE_ROW={key:other[key][1000] for key in ("indices","row_ids","text_sha256","texts",
                                                        "ordered_token_ids","nonpadding_tokens_per_row")}
    for key,value in ALTERNATIVE_ROW.items():
        if key in data:data[key][0]=copy.deepcopy(value)
    data["nonpadding_tokens"]=sum(map(len,data["ordered_token_ids"]))
    return data


class PopulationTests(unittest.TestCase):
    def test_artifact_is_exact_recorded_R1000(self):
        raw = (ROOT / POP_PATH).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), POP_SHA)
        pins = json.loads((ROOT / ARTIFACT["provenance"]["pins_path"]).read_bytes())
        self.assertEqual(ARTIFACT["population"], pins["populations"]["R1000"])
        self.assertEqual(ARTIFACT["dataset"], pins["dataset"])
        for source, target in (("model_files", "model_files"), ("tokenizer_files", "tokenizer_files"),
                               ("cache_files", "cache_files")):
            self.assertEqual(ARTIFACT[target], pins[source])

    def test_alternative_control_contains_only_actual_pinned_rows_and_consistent_counts(self):
        original=metadata(texts=True);other=valid_alternative(copy.deepcopy(original))
        self.assertEqual(len(set(other["indices"])),1000)
        self.assertEqual(len(set(other["row_ids"])),1000)
        self.assertNotIn(other["row_ids"][0],original["row_ids"])
        self.assertNotIn(other["indices"][0],original["indices"])
        self.assertEqual(other["text_sha256"],[hashlib.sha256(t.encode()).hexdigest() for t in other["texts"]])
        self.assertEqual(other["nonpadding_tokens_per_row"],list(map(len,other["ordered_token_ids"])))
        self.assertEqual(other["nonpadding_tokens"],sum(other["nonpadding_tokens_per_row"]))

    def test_exact_manifest_and_reader_accept(self):
        value = record()
        R.validate_manifest(value["manifest"]["parts"])
        self.assertEqual(R.read_process(value)["next_stage"], 2)

    def test_manifest_requires_exact_artifact_hash(self):
        for value in (None, "b" * 64, ""):
            parts = record()["manifest"]["parts"]
            if value is None: parts.pop("reference_population_sha256")
            else: parts["reference_population_sha256"] = value
            with self.subTest(value=value), self.assertRaisesRegex(R.Halt, "reference population"):
                R.validate_manifest(parts)

    def test_another_valid_thousand_row_set_rejected_even_with_recomputed_H_in(self):
        value = record(); parts = value["manifest"]["parts"]
        valid_alternative(parts["dataset"])
        self.assertEqual(len(set(parts["dataset"]["row_ids"])), 1000)
        self.assertEqual(len(parts["dataset"]["ordered_token_ids"]), 1000)
        value["manifest"]["H_in"] = value["H_in"] = R.json_digest(parts)
        reading = R.read_process(value)
        self.assertEqual(reading["label"], "HALTED-V12")
        self.assertFalse(reading["scientific_verdict"])
        self.assertIn("reference population", reading["detail"])

    def test_each_population_identity_field_is_bound(self):
        changes = {
            "revision": lambda d: d.update(revision="a" * 40),
            "indices": lambda d: d["indices"].reverse(),
            "row_ids": lambda d: d["row_ids"].reverse(),
            "text_sha256": lambda d: d["text_sha256"].__setitem__(0, "a" * 64),
            "ordered_token_ids": lambda d: d["ordered_token_ids"][0].__setitem__(0, d["ordered_token_ids"][0][0] + 1),
            "counts": lambda d: d["nonpadding_tokens_per_row"].__setitem__(0, 1),
            "dataset_identity": lambda d: d["dataset_identity"].update(split_length=6407815),
            "artifact_sha": lambda d: d.update(reference_population_sha256="b" * 64),
        }
        for field, change in changes.items():
            parts = record()["manifest"]["parts"]; change(parts["dataset"])
            with self.subTest(field=field), self.assertRaisesRegex(R.Halt, "reference population"):
                R.validate_manifest(parts)

    def test_model_tokenizer_and_cache_pins_are_exact(self):
        for group, key in (("safetensors", next(iter(ARTIFACT["model_files"]))),
                           ("tokenizer", "tokenizer.json"), ("covariances", "4")):
            parts = record()["manifest"]["parts"]
            if group == "covariances": parts[group][key]["sha256"] = "b" * 64
            else: parts[group][key] = "b" * 64
            with self.subTest(group=group), self.assertRaisesRegex(R.Halt, "reference population"):
                R.validate_manifest(parts)

    def test_population_artifact_tampering_and_alternate_valid_artifact_refuse(self):
        for changed in (False, True):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); path = root / POP_PATH; path.parent.mkdir(parents=True)
                artifact = copy.deepcopy(ARTIFACT)
                if changed: valid_alternative(artifact["population"])
                path.write_bytes((json.dumps(artifact, sort_keys=True) + "\n").encode())
                with self.assertRaisesRegex(R.Halt, "reference population artifact SHA"):
                    R.load_reference_population(root)

    def test_loader_rechecks_bytes_after_a_successful_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = root / POP_PATH; path.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / POP_PATH, path)
            self.assertEqual(R.load_reference_population(root), ARTIFACT)
            with path.open("ab") as f: f.write(b" ")
            with self.assertRaisesRegex(R.Halt, "reference population artifact SHA"):
                R.load_reference_population(root)

    def test_unchanged_A1_size_budget_and_statistic_recipe(self):
        self.assertEqual((R.SETTINGS["D_rows"], R.SETTINGS["D_tokens"]), (1000, 100))
        self.assertEqual(D.ALLOWANCES["reference_D"], 300.)
        self.assertEqual(ARTIFACT["recipe"]["batch_rows"], 16)
        self.assertEqual(ARTIFACT["population"]["nonpadding_tokens"], 95610)

    def test_driver_manifest_rejects_alternate_population_before_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = object.__new__(D.Session); session.out = Path(tmp); session.loaded_manifest = None
            parts = record()["manifest"]["parts"]; valid_alternative(parts["dataset"])
            session.input_parts = lambda: parts
            with self.assertRaisesRegex(R.Halt, "reference population"):
                session.make_manifest()
            self.assertFalse((session.out / "manifest.json").exists())


class PersistenceTests(unittest.TestCase):
    def session(self, out, source=None):
        session, stats = VT.PersistenceCorrectionTests().session(out, input_dir=source)
        stats["dataset"] = metadata(texts=True)
        return session, stats

    def test_returned_population_mismatch_retains_m_and_provenance_before_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; out.mkdir(); session, stats = self.session(out)
            valid_alternative(stats["dataset"])
            with patch.object(os, "fsync", wraps=os.fsync) as sync, \
                 self.assertRaisesRegex(R.Halt, "reference population"):
                session.prepare_instruments()
            self.assertGreaterEqual(sync.call_count, 1)
            saved = torch.load(out / "dstats.pt", weights_only=True)
            self.assertEqual(saved["dataset"], stats["dataset"])
            self.assertTrue(torch.equal(saved["m"]["35"], stats["m"]["35"]))
            self.assertFalse((out / "G.pt").exists())

    def test_process2_copies_both_raw_artifacts_before_population_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; source = Path(tmp) / "source"; out.mkdir(); source.mkdir()
            session, stats = self.session(out, source); valid_alternative(stats["dataset"])
            torch.save(stats, source / "dstats.pt"); torch.save(torch.eye(3, dtype=torch.float64), source / "G.pt")
            with patch.object(os, "fsync", wraps=os.fsync) as sync, \
                 self.assertRaisesRegex(R.Halt, "reference population"):
                session.prepare_instruments()
            self.assertGreaterEqual(sync.call_count, 2)
            for name in ("dstats.pt", "G.pt"):
                self.assertEqual((out / name).read_bytes(), (source / name).read_bytes())

    def test_correct_population_retains_G_on_forced_V8_failure(self):
        for second in (False, True):
            with self.subTest(process2=second), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "out"; source = Path(tmp) / "source"; out.mkdir(); source.mkdir()
                session, stats = self.session(out, source if second else None)
                session.compute_G = lambda: -torch.eye(3, dtype=torch.float64)
                if second:
                    torch.save(stats, source / "dstats.pt"); torch.save(session.compute_G(), source / "G.pt")
                with self.assertRaisesRegex(R.Halt, "HALTED-V8"): session.prepare_instruments()
                self.assertTrue((out / "dstats.pt").is_file()); self.assertTrue((out / "G.pt").is_file())
                if second:
                    for name in ("dstats.pt", "G.pt"):
                        self.assertEqual((out / name).read_bytes(), (source / name).read_bytes())

    def test_exclusive_stats_write_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; out.mkdir(); session, _ = self.session(out)
            (out / "dstats.pt").write_bytes(b"earlier retained bytes")
            with self.assertRaises(FileExistsError): session.prepare_instruments()
            self.assertEqual((out / "dstats.pt").read_bytes(), b"earlier retained bytes")

    def test_real_process2_constructor_retains_bytes_before_manifest_population_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"; source = Path(tmp) / "source"; out.mkdir(); source.mkdir()
            _, stats = self.session(out)
            torch.save(stats, source / "dstats.pt"); torch.save(torch.eye(3, dtype=torch.float64), source / "G.pt")
            (source / "context_templates.json").write_text("[]")
            manifest = record()["manifest"]; parts = manifest["parts"]
            for key, name in (("dstats_sha256", "dstats.pt"), ("G_sha256", "G.pt"),
                              ("context_templates_sha256", "context_templates.json")):
                parts[key] = hashlib.sha256((source / name).read_bytes()).hexdigest()
            valid_alternative(parts["dataset"]); manifest["H_in"] = R.json_digest(parts)
            (source / "manifest.json").write_text(json.dumps(manifest))
            # The future frozen state is supplied; the actual constructor must refuse before model import.
            with patch.object(R, "require_a1_freeze"), patch.object(os, "fsync", wraps=os.fsync) as sync, \
                 self.assertRaisesRegex(R.Halt, "reference population"):
                D.Session(out, 2, types.SimpleNamespace(), input_dir=source)
            self.assertGreaterEqual(sync.call_count, 2)
            self.assertNotIn("c10e_bandknob", sys.modules)
            for name in ("dstats.pt", "G.pt"):
                self.assertTrue((out / name).exists(), "constructor lost " + name + " on manifest mismatch")
                self.assertEqual((out / name).read_bytes(), (source / name).read_bytes())


class AdmissionTests(unittest.TestCase):
    def test_DRAFT_direct_resident_CLI_refuses_before_dispatch_or_output(self):
        with amendment_fixture() as root, \
             tempfile.TemporaryDirectory() as tmp, \
             patch.dict(os.environ, {"C10Z_RESIDENT":"1", "C10Z_LAUNCH":json.dumps(ST._launch()), "C10Z_OUT_DIR":tmp}), \
             patch.object(sys,"argv",["arms","0"]), patch.object(D,"resident",return_value=0) as worker:
            with self.assertRaisesRegex(R.Halt,"A1 amendment is DRAFT"):
                D.main()
            worker.assert_not_called();self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_DRAFT_direct_resident_function_refuses_before_publication(self):
        with amendment_fixture() as root, tempfile.TemporaryDirectory() as tmp, patch.object(D,"write_json") as write, \
             patch.object(D,"Session") as session:
            with self.assertRaisesRegex(R.Halt,"A1 amendment is DRAFT"):
                D.resident(Path(tmp),1,ST._launch())
            write.assert_not_called();session.assert_not_called();self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_go_requires_exact_population_and_amendment_pin(self):
        good = ST._go_record(); good.update(reference_population_sha256=POP_SHA,
            prereg_sha256=R.PREREG_SHA, amendment_decision_id="D-C10z-a1pop")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "go.json"
            for change in ({"reference_population_sha256": "b" * 64}, {"prereg_sha256": "b" * 64},
                           {"amendment_decision_id": "D-C10z-not-a1"}):
                path.write_text(json.dumps({**good, **change}))
                with self.subTest(change=change), self.assertRaisesRegex(R.Halt, "A1 go"):
                    D.go_record({"C10Z_GO_RECORD": str(path)})
            path.write_text(json.dumps(good))
            self.assertEqual(D.go_record({"C10Z_GO_RECORD": str(path)})[0], good)

    def test_DRAFT_benchmark_refuses_before_child_or_output(self):
        B = importlib.import_module("c10z_astra_benchmark")
        with amendment_fixture() as root, tempfile.TemporaryDirectory() as tmp, patch.object(B, "supervise", return_value=0) as child, \
             patch.object(sys, "argv", ["benchmark", "--out", str(Path(tmp) / "fresh")]):
            with self.assertRaisesRegex(R.Halt, "A1 amendment is DRAFT"):
                B.main()
            child.assert_not_called(); self.assertFalse((Path(tmp) / "fresh").exists())

    def test_DRAFT_attempt_refuses_even_with_hash_matching_selected_benchmark(self):
        with amendment_fixture() as root:
            path, binding = ST._bench_tree(root)
            go = ST._go_record(binding); go.update(reference_population_sha256=POP_SHA,
                prereg_sha256=R.PREREG_SHA, amendment_decision_id="D-C10z-a1pop")
            go_path = root / "go.json"; go_path.write_text(json.dumps(go)); out = root / "attempt"
            with patch.object(D, "ROOT", root), patch.object(D.subprocess, "Popen") as child, \
                 patch.dict(os.environ, {"C10Z_GO_RECORD": str(go_path), "C10Z_BENCHMARK_RECORD": str(path)}):
                with self.assertRaisesRegex(R.Halt, "A1 amendment is DRAFT"):
                    D.stage_call(0, out)
                child.assert_not_called(); self.assertFalse(out.exists())

    def test_freeze_requires_synced_prereg_SHA_and_explicit_FROZEN_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = root / D.PREREG; path.parent.mkdir(parents=True)
            pop = root / POP_PATH; pop.parent.mkdir(parents=True); shutil.copyfile(ROOT / POP_PATH, pop)
            data = "## §12 Amendment A1-POPULATION\n\n**Status:** FROZEN\n"
            path.write_text(data)
            with patch.object(R, "PREREG_SHA", hashlib.sha256(data.encode()).hexdigest()):
                R.require_a1_freeze(root)
            with self.assertRaisesRegex(R.Halt, "prereg SHA"):
                R.require_a1_freeze(root)
            for status in ("DRAFT pending Astra", "FROZEN pending Astra", "APPROVED", ""):
                data = "## §12 Amendment A1-POPULATION\n\n**Status:** " + status + "\n"
                path.write_text(data)
                with patch.object(R, "PREREG_SHA", hashlib.sha256(data.encode()).hexdigest()), \
                     self.assertRaisesRegex(R.Halt, "A1 amendment is DRAFT"):
                    R.require_a1_freeze(root)


class FirstPublicationReached(Exception):
    pass


class FixRound1Tests(unittest.TestCase):
    # These are Astra's six independent launch mutations; each must fail at both public entry paths.
    mutations = (("go", "reference_population_sha256", "b" * 64),
                 ("go", "prereg_sha256", "b" * 64),
                 ("go", "amendment_decision_id", "D-C10z-not-a1"),
                 ("benchmark", "reference_population_sha256", "b" * 64),
                 ("benchmark", "prereg_sha256", "b" * 64),
                 (None, "go_sha256", "b" * 64))

    def resident_entry(self, launch, env, out, cli):
        with patch.dict(os.environ, {**env, "C10Z_RESIDENT": "1", "C10Z_LAUNCH": json.dumps(launch),
                                     "C10Z_OUT_DIR": str(out)}, clear=True), \
             patch.object(sys, "argv", ["arms", "0"]), \
             patch.object(D, "write_json", side_effect=FirstPublicationReached("first publication reached")), \
             patch.object(D, "Session", side_effect=AssertionError("Session/model forbidden")):
            return D.main() if cli else D.resident(out, 1, launch)

    def rejected_resident(self, launch, env, out, cli):
        try:
            self.resident_entry(launch, env, out, cli)
        except R.Halt as error:
            self.assertEqual(error.code, "HALTED-V12")
        except FirstPublicationReached:
            self.fail("altered launch reached first publication before go/benchmark revalidation")
        else:
            self.fail("altered resident launch was accepted")
        self.assertFalse(out.exists(), "refusal published an attempt")
        self.assertNotIn("c10e_bandknob", sys.modules)

    def reader_entry(self, out, cli):
        if not cli: return R.read_directory(out)
        with patch.object(sys, "argv", ["reader", str(out)]), redirect_stdout(io.StringIO()) as output:
            code = R.main()
        reading = json.loads(output.getvalue())
        self.assertEqual(code, 0 if reading["scientific_verdict"] else 2)
        return reading

    def attempt(self, root, launch):
        value = record(); value["budget"]["ceilings"] = {k: launch[k] for k in ("stage01", "stage2", "stage3")}
        value["manifest"]["parts"]["go_sha256"] = launch["go_sha256"]
        out = root / "attempt"
        ST._attempt_dir(D, out, value, {"launch": copy.deepcopy(launch)})
        return out

    def test_frozen_resident_six_mutations_refuse_before_publication_for_function_and_CLI(self):
        with amendment_fixture("FROZEN") as root:
            good, env = selected_launch(root)
            for cli in (False, True):
                for group, key, value in self.mutations:
                    bad = copy.deepcopy(good); (bad[group] if group else bad)[key] = value
                    with self.subTest(cli=cli, group=group, key=key):
                        self.rejected_resident(bad, env, root / "unpublished", cli)

    def test_frozen_resident_requires_exact_validated_go_contents_and_raw_SHA_for_both_entries(self):
        with amendment_fixture("FROZEN") as root:
            good, env = selected_launch(root); path = Path(env["C10Z_GO_RECORD"]); raw = path.read_bytes()
            for cli in (False, True):
                for changed in ("contents", "bytes"):
                    if changed == "contents":
                        value = copy.deepcopy(good["go"]); value["recorded_by"] = "different-valid-operator"
                        path.write_text(json.dumps(value))
                    else: path.write_bytes(raw + b" ")
                    with self.subTest(cli=cli, changed=changed):
                        self.rejected_resident(good, env, root / "unpublished", cli)
            path.write_bytes(raw)

    def test_frozen_resident_exact_launch_passes_admission_before_first_publication_for_both_entries(self):
        with amendment_fixture("FROZEN") as root:
            launch, env = selected_launch(root)
            for cli in (False, True):
                with self.subTest(cli=cli), self.assertRaises(FirstPublicationReached):
                    self.resident_entry(launch, env, root / "unpublished", cli)

    def test_frozen_resident_go_boolean_integer_alias_refuses_for_both_entries(self):
        with amendment_fixture("FROZEN") as root:
            good, env = selected_launch(root)
            for cli in (False, True):
                for key in ("operator_yes", "one_gpu_job"):
                    bad = copy.deepcopy(good); bad["go"][key] = 1
                    with self.subTest(cli=cli, key=key):
                        self.rejected_resident(bad, env, root / "unpublished", cli)

    def test_reader_six_mutations_fail_closed_for_directory_and_CLI_without_writes(self):
        with amendment_fixture("FROZEN") as root:
            good, _ = selected_launch(root); out = self.attempt(root, good)
            before = {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}
            original = json.loads((out / "run.json").read_bytes())
            for cli in (False, True):
                for group, key, value in self.mutations:
                    run = copy.deepcopy(original)
                    (run["launch"][group] if group else run["launch"])[key] = value
                    (out / "run.json").write_text(json.dumps(run))
                    snapshot = {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}
                    with self.subTest(cli=cli, group=group, key=key):
                        reading = self.reader_entry(out, cli)
                        self.assertFalse(reading["scientific_verdict"], reading)
                        self.assertEqual(reading["label"], "HALTED-V12")
                        self.assertEqual(snapshot, {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()})
            (out / "run.json").write_bytes(before["run.json"])

    def test_reader_exact_launch_keeps_PARTIAL_scientific_reading_for_both_entries(self):
        with amendment_fixture("FROZEN") as root:
            launch, _ = selected_launch(root); out = self.attempt(root, launch)
            for cli in (False, True):
                with self.subTest(cli=cli):
                    reading = self.reader_entry(out, cli)
                    self.assertTrue(reading["scientific_verdict"], reading)
                    self.assertEqual(reading["label"], "PARTIAL")


if __name__ == "__main__": unittest.main(verbosity=2)
