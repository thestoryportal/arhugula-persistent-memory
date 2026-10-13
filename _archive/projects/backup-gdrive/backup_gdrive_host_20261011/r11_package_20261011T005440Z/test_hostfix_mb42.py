"""Replay recorded host receipts and exercise the actual fixture placement."""
import importlib.util
import json
import os
import plistlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import uuid
from unittest import mock
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent

def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class HostLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mb42_log_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        self.verifier = module("verify_check")

    def replay(self, case="clean", omit_debug=False):
        source = HERE / "r11_local_check/local_check" / case
        for name in ("exit_code.txt", "inventory.exit_code.txt", "inventory.txt",
                     "combined.txt", "differ.txt", "missing-on-dst.txt", "error.txt",
                     "check.log", "stdout.txt", "stderr.txt"):
            shutil.copyfile(source / name, self.run / name)
        if omit_debug:
            lines = (self.run / "check.log").read_text().splitlines(keepends=True)
            assert 'DEBUG : rclone: Version' in lines[0] and '"--error"' in lines[0]
            (self.run / "check.log").write_text("".join(lines[1:]))

    def test_recorded_clean_passes(self):
        self.replay()
        result = self.verifier.inspect(self.run)
        self.assertTrue(result["pass"], result)

    def test_recorded_excluded_only_passes(self):
        self.replay("excluded_only")
        result = self.verifier.inspect(self.run)
        self.assertTrue(result["pass"], result)

    def test_recorded_symlink_passes(self):
        self.replay("symlink")
        result = self.verifier.inspect(self.run)
        self.assertTrue(result["pass"], result)

    def test_recorded_same_size_corruption_still_fails(self):
        self.replay("same_size_corruption")
        result = self.verifier.inspect(self.run)
        self.assertFalse(result["pass"])
        self.assertIn("alpha.txt", result["failed_objects"])

    def test_config_notice_alone_passes(self):
        self.replay(omit_debug=True)
        self.assertIn("not found - using defaults", (self.run / "check.log").read_text())
        result = self.verifier.inspect(self.run)
        self.assertTrue(result["pass"], result)

    def test_debug_argument_severity_words_are_data(self):
        self.replay(omit_debug=True)
        with (self.run / "check.log").open("a") as stream:
            stream.write('2026/10/10 19:58:00 DEBUG : rclone: starting with parameters ["--error" "/tmp/ERROR/CRITICAL/FATAL/error.txt"]\n')
        result = self.verifier.inspect(self.run)
        self.assertTrue(result["pass"], result)

    def test_real_error_levels_still_fail(self):
        for level in ("ERROR", "CRITICAL", "FATAL"):
            with self.subTest(level=level):
                self.replay(omit_debug=True)
                with (self.run / "check.log").open("a") as stream:
                    stream.write("2026/10/10 19:58:00 " + level + " : alpha.txt: unreadable\n")
                result = self.verifier.inspect(self.run)
                self.assertFalse(result["pass"])
                self.assertGreaterEqual(result["errors"], 1)

    def test_stderr_error_level_still_fails(self):
        self.replay(omit_debug=True)
        (self.run / "stderr.txt").write_text("ERROR: cannot open alpha.txt\n")
        self.assertGreaterEqual(self.verifier.inspect(self.run)["errors"], 1)

    def test_unprefixed_read_error_still_fails(self):
        self.replay(omit_debug=True)
        (self.run / "stderr.txt").write_text("Failed to read alpha.txt: permission denied\n")
        self.assertGreaterEqual(self.verifier.inspect(self.run)["errors"], 1)

    def test_unchecked_hash_still_fails(self):
        self.replay(omit_debug=True)
        with (self.run / "check.log").open("a") as stream:
            stream.write("2026/10/10 19:58:00 NOTICE: 1 hashes could not be checked\n")
        result = self.verifier.inspect(self.run)
        self.assertFalse(result["pass"])
        self.assertEqual(result["unchecked"], 1)

class RunnerPlacementTest(unittest.TestCase):
    def test_actual_runner_uses_owned_tmp_fixture_root(self):
        label = "mb42_hostfix1_placement_probe_" + uuid.uuid4().hex[:12]
        completed = subprocess.run(
            ["/usr/bin/python3", "-B", str(HERE / "run_py39_coverage.py"),
             label, "--sandbox", "--mode", "check-green"],
            text=True, capture_output=True, timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        meta = json.loads((HERE / label / "command.json").read_text())
        home = Path(meta["env"]["HOME"]).resolve()
        fixtures = Path(meta["env"]["BACKUP_TEST_RECEIPTS"]).resolve()
        self.assertTrue(home.is_relative_to(Path("/private/tmp")),
                        "actual runner HOME must be off the receipt volume: " + str(home))
        self.assertTrue(fixtures.is_relative_to(home))
        result = json.loads((HERE / label / "result.json").read_text())
        self.assertTrue(result["real_inventory_identical"])
        self.assertTrue(result["all_owned_groups_exited"])

class PhysicalPlacementTest(unittest.TestCase):
    def setUp(self):
        self.runner = module("run_py39_coverage")
        self.probe = HERE / "host_diskutil_probe_maestro31"

    def proof(self):
        fn = getattr(self.runner, "validate_fixture_disks", None)
        self.assertTrue(callable(fn), "native physical-store positive control is missing")
        return fn

    def info(self, name):
        return plistlib.loads((self.probe / name).read_bytes())

    def test_recorded_native_disks_are_disjoint(self):
        proof = self.proof()(self.info("info_volumes_memit.plist"),
                             self.info("info_system_volumes_data.plist"))
        self.assertEqual(proof["source_physical_disks"], ["disk4"])
        self.assertEqual(proof["fixture_physical_disks"], ["disk0"])
        self.assertTrue(proof["different_physical_disks"])

    def test_other_partition_on_same_physical_disk_is_rejected(self):
        source = self.info("info_volumes_memit.plist")
        apfs = self.info("apfs_list.plist")
        other = next(c for c in apfs["Containers"] if c["ContainerReference"] == "disk5")
        fixture = dict(APFSContainerReference="disk5", ParentWholeDisk="disk5",
                       APFSPhysicalStores=[{"APFSPhysicalStore": x["DeviceIdentifier"]}
                                           for x in other["PhysicalStores"]])
        fn = self.proof()
        with self.assertRaisesRegex(RuntimeError, "same physical disk"):
            fn(source, fixture)

    def test_unknown_physical_identity_is_rejected(self):
        fn = self.proof()
        with self.assertRaises(RuntimeError):
            fn(self.info("info_volumes_memit.plist"), {})

    def test_df_resolves_native_path_to_mountpoint(self):
        fn = getattr(self.runner, "df_mountpoint", None)
        self.assertTrue(callable(fn), "df mount-point resolver is missing")
        result = subprocess.run(["/bin/df", "-P", "/private/tmp"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(str(fn(result.stdout)), "/System/Volumes/Data")
        with self.assertRaises(RuntimeError):
            fn("")

class LocalEvidencePlacementTest(unittest.TestCase):
    def test_receipt_evidence_and_tmp_content_roots_are_separate(self):
        checker = module("run_local_check")
        with tempfile.TemporaryDirectory(prefix="mb42_local_", dir="/private/tmp") as base:
            home = Path(base) / "home"
            home.mkdir()
            directory = HERE / ("mb42_hostfix1_local_probe_" + uuid.uuid4().hex[:12])
            directory.mkdir()
            evidence = directory / "local_check"
            def fake_call(argv, **kwargs):
                kind = argv[1]
                if kind == "config":
                    kwargs["stdout"].write(str(home / ".config/rclone/rclone.conf") + "\n")
                    return SimpleNamespace(returncode=0)
                if kind == "listremotes":
                    return SimpleNamespace(returncode=0)
                if kind == "lsf":
                    case = Path(argv[2]).parent.name.removeprefix("content_")
                    native = HERE / "r11_local_check/local_check" / case
                    kwargs["stdout"].write((native / "inventory.txt").read_text())
                    return SimpleNamespace(returncode=0)
                self.assertEqual(kind, "check")
                dest = Path(argv[argv.index("--combined") + 1]).parent
                native = HERE / "r11_local_check/local_check" / dest.name
                for name in ("combined.txt", "differ.txt", "missing-on-dst.txt",
                             "error.txt", "check.log"):
                    shutil.copyfile(native / name, dest / name)
                return SimpleNamespace(returncode=int((native / "exit_code.txt").read_text()))
            with mock.patch.dict(os.environ, HOME=str(home)), \
                 mock.patch("run_py39_coverage.validate_host"), \
                 mock.patch.object(checker.subprocess, "run", side_effect=fake_call), \
                 mock.patch("sys.argv", ["run_local_check.py", str(evidence)]):
                self.assertEqual(checker.main(), 0)
            self.assertTrue(json.loads((evidence / "result.json").read_text())["success"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
