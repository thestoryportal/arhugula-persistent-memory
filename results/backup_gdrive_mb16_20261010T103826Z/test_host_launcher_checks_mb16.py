"""Numbered MB16 criteria; native commands are replaced at the subprocess boundary."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
os.environ["BACKUP_TEST_NO_RCLONE"] = "1"
spec = importlib.util.spec_from_file_location("host_launcher_checks_mb16", HERE/"host_launcher_checks_mb16.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class HostFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mb16_unit_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.scratch = Path(self.tmp.name).resolve()
        self.evidence = self.scratch/"evidence"
        self.evidence.mkdir()
        self.executable = self.scratch/"fixture/Native_1.app/Contents/MacOS/applet"

    def layout(self, fixture_root):
        self.assertFalse(fixture_root.is_relative_to(Path("/Volumes")))
        case = SimpleNamespace(crash=False)
        helper.initialize_fixture(case, fixture_root)
        source, app = helper.write_applet_source(ROOT, case, 1, case.base/"stub.sh")
        self.assertTrue(source.is_file())
        # A compiler output fixture, never a compiled or launched applet.
        (app/"Contents/MacOS").mkdir(parents=True)
        (app/"Contents/MacOS/applet").write_text("fixture only")
        refused = helper.write_refused_wrapper(case.base)
        stub = helper.write_recovery_wrapper(case.base, case.base/"dispatched-generation")
        # Exercise the inherited method that writes held-rclone; stop before it runs a child.
        from tools.test_backup_gdrive_addendum import GenerationLaunchTest
        with mock.patch.object(subprocess, "Popen", side_effect=RuntimeError("unit boundary: no child")):
            with self.assertRaisesRegex(RuntimeError, "unit boundary"):
                GenerationLaunchTest.hold_live_owner(case)
        required = [case.base, case.home, source, app, refused, stub, case.base/"held-rclone"]
        self.assertTrue(all(path.exists() for path in required))
        for path in [*required, *fixture_root.rglob("*")]:
            with self.subTest(path=str(path)):
                resolved = path.resolve()
                self.assertTrue(resolved.is_relative_to(fixture_root))
                self.assertFalse(resolved.is_relative_to(Path("/Volumes")))
        self.assertEqual(case.log, fixture_root/"fixture/wrapper.log")
        self.assertEqual(case.run_log, fixture_root/"fixture/run.jsonl")

    def test_2_default_layout_all_fixture_paths_outside_volumes(self):
        args = helper.parse_arguments(["manual-interleave"])
        self.assertEqual(args.fixture_root.parent, Path("/private/tmp"))
        self.assertTrue(args.fixture_root.name.startswith("memit_gdrive_native_"))
        self.assertEqual(list(args.fixture_root.iterdir()), [])
        # Own only the temporary directory returned by the helper.
        import shutil
        self.addCleanup(shutil.rmtree, args.fixture_root)
        self.layout(args.fixture_root)

    def test_2_explicit_layout_all_fixture_paths_outside_volumes(self):
        fixture_root = self.scratch/"explicit root"
        fixture_root.mkdir()
        args = helper.parse_arguments(["recovery", "--fixture-root", str(fixture_root)])
        self.assertEqual(args.fixture_root, fixture_root)
        self.assertEqual(list(fixture_root.iterdir()), [])
        self.layout(args.fixture_root)

    def rejected(self, path, message):
        # Argument validation is the complete pre-native boundary: no command is allowed.
        stderr = io.StringIO()
        with mock.patch.object(subprocess, "run", side_effect=AssertionError("native command forbidden")), \
                mock.patch.object(subprocess, "Popen", side_effect=AssertionError("native command forbidden")), \
                contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as caught:
                helper.parse_arguments(["recovery", "--fixture-root", str(path)])
        self.assertNotEqual(caught.exception.code, 0)
        self.assertIn(message, stderr.getvalue())
        self.assertEqual(list(self.evidence.iterdir()), [])

    def test_2_missing_fixture_root_rejected_before_native_work(self):
        self.rejected(self.scratch/"missing", "exist")

    def test_2_file_fixture_root_rejected_before_native_work(self):
        path = self.scratch/"file"
        path.write_text("sentinel")
        self.rejected(path, "directory")
        self.assertEqual(path.read_text(), "sentinel")

    def test_2_nonempty_fixture_root_rejected_without_modification(self):
        path = self.scratch/"populated"
        path.mkdir()
        (path/"sentinel").write_bytes(b"keep")
        self.rejected(path, "empty")
        self.assertEqual({p.name for p in path.iterdir()}, {"sentinel"})
        self.assertEqual((path/"sentinel").read_bytes(), b"keep")

    def test_2_volume_fixture_root_rejected_before_native_work(self):
        self.assertTrue(ROOT.is_relative_to(Path("/Volumes")))
        self.rejected(ROOT, "/Volumes")

    def test_2_symlink_into_volumes_rejected_after_resolution(self):
        alias = self.scratch/"looks local"
        alias.symlink_to(ROOT, target_is_directory=True)
        self.rejected(alias, "/Volumes")
        self.assertTrue(alias.is_symlink())

    def fixture_receipt(self, status, cleanup_ok=True):
        fixture_root = self.scratch/"fixture root"
        fixture_root.mkdir()
        case = SimpleNamespace(doCleanups=lambda: cleanup_ok)
        helper.initialize_fixture(case, fixture_root)
        contents = {
            "wrapper.log": b"wrapper\x00\n",
            "run.jsonl": b'{"run":1}\n',
            "home/Library/Logs/memit-gdrive-backup-launch-state/counter": b"12\n",
            "home/Library/Logs/memit-gdrive-backup/launch_receipt.json": b'{"generation":12}\n',
            "home/Library/Logs/memit-gdrive-backup/last_run.json": b'{"run":"manual"}\n',
            "home/Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl": b'{"failure":11}\n',
            "home/Library/Logs/memit-gdrive-backup-launch-state/recoveries/archive-1/launch_receipt.json": b"old receipt\n",
            "home/Library/Logs/memit-gdrive-backup-launch-state/recoveries/archive-1/nested/failures.jsonl": b"old failure\n",
        }
        for relative, data in contents.items():
            path = case.base/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (case.base/"unrequested.txt").write_text("stay in fixture")
        result = {"status": status}
        helper.finish_case(case, self.evidence, result)
        copied = self.evidence/"fixture_copy"
        self.assertTrue(copied.is_dir(), "case end must preserve fixture evidence")
        actual = {str(p.relative_to(copied)): p.read_bytes() for p in copied.rglob("*") if p.is_file()}
        self.assertEqual(actual, contents)
        self.assertEqual(result["fixture_root"], str(fixture_root))
        for relative, data in contents.items():
            self.assertEqual((case.base/relative).read_bytes(), data)
        return result

    def test_3_passing_case_copies_exact_bytes_and_recovery_tree(self):
        result = self.fixture_receipt("PASS")
        self.assertEqual(result["status"], "PASS")

    def test_3_failing_case_copies_exact_bytes_and_recovery_tree(self):
        result = self.fixture_receipt("FAIL")
        self.assertEqual(result["status"], "FAIL")

    def test_3_cleanup_failure_still_copies_fixture_evidence(self):
        result = self.fixture_receipt("PASS", cleanup_ok=False)
        self.assertEqual(result["status"], "FAIL")

    def test_3_absent_optional_files_are_omitted(self):
        fixture_root = self.scratch/"fixture root"
        fixture_root.mkdir()
        case = SimpleNamespace(doCleanups=lambda: True)
        helper.initialize_fixture(case, fixture_root)
        result = {"status": "FAIL"}
        helper.finish_case(case, self.evidence, result)
        copied = self.evidence/"fixture_copy"
        self.assertTrue(copied.is_dir())
        self.assertEqual({str(p.relative_to(copied)) for p in copied.rglob("*") if p.is_file()}, {
            "wrapper.log", "run.jsonl", "home/Library/Logs/memit-gdrive-backup-launch-state/counter"})
        self.assertFalse((copied/"home/Library/Logs/memit-gdrive-backup/last_run.json").exists())

    def test_3_raised_cleanup_failure_keeps_case_reviewable(self):
        fixture_root = self.scratch/"fixture root"
        fixture_root.mkdir()
        def cleanup():
            raise RuntimeError("owned cleanup exception")
        case = SimpleNamespace(doCleanups=cleanup)
        helper.initialize_fixture(case, fixture_root)
        result = {"status": "PASS"}
        escaped = None
        try:
            helper.finish_case(case, self.evidence, result)
        except RuntimeError as exc:
            escaped = str(exc)
        self.assertIsNone(escaped, "cleanup failure must permit summary and source hashes to be written")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue((self.evidence/"fixture_copy/wrapper.log").exists())
        self.assertIn("owned cleanup exception", (self.evidence/"failure.txt").read_text())

    def listing(self):
        return ("  PID  PPID STAT     ELAPSED COMMAND\n"
                "  104   103 S          00:05 /usr/bin/perl /private/tmp/fixture/home/lock.pl\n"
                "  999     1 S          01:00 /other/Native_1.app/Contents/MacOS/applet\n"
                f"  106     1 S          00:05 {self.executable}.other\n"
                "  103   101 S          00:05 /bin/sh -c mkdir /private/tmp/fixture/home/state\n"
                f"  101     1 S          00:06 {self.executable} -psn_0_1\n"
                f"  107     1 S          00:04 /bin/sh -c {self.executable}\n"
                "  108   107 S          00:03 unrelated-child\n")

    def test_4_snapshot_filter_keeps_applet_and_all_unordered_descendants(self):
        filtered = helper.filter_process_snapshot(self.listing(), self.executable)
        expected = ["  PID  PPID STAT     ELAPSED COMMAND", *[
            line for line in self.listing().splitlines() if line.strip().split()[0] in {"101", "103", "104"}]]
        self.assertEqual(filtered, "\n".join(expected)+"\n")

    def test_4_snapshot_filter_matches_executable_paths_with_spaces(self):
        self.executable = self.scratch/"root with spaces/Native_1.app/Contents/MacOS/applet"
        filtered = helper.filter_process_snapshot(self.listing(), self.executable)
        self.assertIn(f"{self.executable} -psn_0_1", filtered)
        self.assertIn("/usr/bin/perl /private/tmp/fixture/home/lock.pl", filtered)
        self.assertNotIn("unrelated-child", filtered)
        self.assertNotIn(".other", filtered)

    def test_4_missing_applet_is_explicit_without_unrelated_processes(self):
        filtered = helper.filter_process_snapshot("PID PPID STAT ELAPSED COMMAND\n9 1 S 00:01 unrelated\n", self.executable)
        self.assertIn("NO MATCH", filtered)
        self.assertNotIn("unrelated", filtered)

    def snapshot_failure(self, response):
        with mock.patch.object(subprocess, "run", side_effect=response if isinstance(response, Exception) else None,
                               return_value=response):
            helper.save_process_snapshot(self.evidence, self.executable)
        path = self.evidence/"process_snapshot.txt"
        self.assertTrue(path.is_file(), "failed inspection must leave an explicit snapshot receipt")
        return path.read_text()

    def test_4_denied_process_inspection_records_unavailable_reason(self):
        text = self.snapshot_failure(subprocess.CompletedProcess([], 1, "", "ps: Operation not permitted"))
        self.assertIn("UNAVAILABLE", text)
        self.assertIn("Operation not permitted", text)
        self.assertIn("pid,ppid,stat,etime,command", text)

    def test_4_timed_out_process_inspection_records_unavailable_reason(self):
        text = self.snapshot_failure(subprocess.TimeoutExpired(["/bin/ps"], 5))
        self.assertIn("UNAVAILABLE", text)
        self.assertIn("timed out", text)

    def open_response(self, response):
        command = ["/usr/bin/open", "-W", "-g", str(self.executable.parents[2])]
        calls = []
        def run(args, **kwargs):
            calls.append((args, kwargs))
            if args[0] == "/usr/bin/open":
                if isinstance(response, Exception):
                    raise response
                return response
            self.assertEqual(args, ["/bin/ps", "-axo", "pid,ppid,stat,etime,command"])
            return subprocess.CompletedProcess(args, 0, self.listing(), "")
        with mock.patch.object(subprocess, "run", side_effect=run):
            if isinstance(response, Exception):
                with self.assertRaises(type(response)):
                    helper.run_open(command, self.executable, self.evidence)
            else:
                result = helper.run_open(command, self.executable, self.evidence)
                self.assertEqual(result.returncode, response.returncode)
        self.assertEqual(calls[0][1]["timeout"], 20)
        path = self.evidence/"process_snapshot.txt"
        self.assertTrue(path.exists(), "open failure must snapshot before it escapes to case cleanup")
        self.assertIn("/usr/bin/perl /private/tmp/fixture/home/lock.pl", path.read_text())
        self.assertEqual(len([args for args, _ in calls if args[0] == "/usr/bin/open"]), 1)

    def test_4_open_timeout_snapshots_without_retry_or_longer_timeout(self):
        self.open_response(subprocess.TimeoutExpired(["/usr/bin/open"], 20))

    def test_4_open_nonzero_snapshots_before_returning_failure(self):
        self.open_response(subprocess.CompletedProcess(["/usr/bin/open"], 1, "", "launch failed"))

    def test_3_open_timeout_remains_in_commands_receipt(self):
        prior = {"args": ["/usr/bin/osacompile"], "exit_code": 0}
        (self.evidence/"commands.json").write_text(json.dumps([prior]))
        command = ["/usr/bin/open", "-W", "-g", str(self.executable.parents[2])]
        def run(args, **kwargs):
            if args[0] == "/usr/bin/open":
                raise subprocess.TimeoutExpired(args, 20)
            return subprocess.CompletedProcess(args, 0, self.listing(), "")
        with mock.patch.object(subprocess, "run", side_effect=run):
            with self.assertRaises(subprocess.TimeoutExpired):
                helper.run_open(command, self.executable, self.evidence)
        commands = json.loads((self.evidence/"commands.json").read_text())
        self.assertEqual(len(commands), 2, "timeout must record the failed native command as well as compile")
        self.assertEqual(commands[0], prior)
        self.assertEqual(commands[1]["args"], command)
        self.assertEqual(commands[1]["timeout"], 20)
        self.assertEqual(commands[1]["error_type"], "TimeoutExpired")

    def test_4_crash_allocation_failure_snapshots_before_release_cleanup(self):
        entered, release = self.scratch/"entered", self.scratch/"release"
        proc = mock.Mock()
        proc.poll.return_value = 0
        proc.communicate.return_value = ("", "")
        proc.returncode = 0
        def ps(args, **kwargs):
            self.assertFalse(release.exists(), "snapshot must precede allocation release cleanup")
            return subprocess.CompletedProcess(args, 0, self.listing(), "")
        with mock.patch.object(subprocess, "Popen", return_value=proc), \
                mock.patch.object(subprocess, "run", side_effect=ps):
            with self.assertRaisesRegex(AssertionError, "allocation never reached"):
                helper.run_crash_open(["/usr/bin/open"], self.executable, entered, release, self.evidence, [])
        self.assertTrue((self.evidence/"process_snapshot.txt").exists())
        self.assertTrue(release.exists())


if __name__ == "__main__":
    import os
    os.environ["BACKUP_TEST_NO_RCLONE"] = "1"
    unittest.main()
