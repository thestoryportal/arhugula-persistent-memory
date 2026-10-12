"""MB38 host-runner fixtures; no live tmux/ps calls or real sink writes."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results/dashboard_audit_20261010/fix_20261010T234721Z"
HOST = ROOT / "tests/test_dashboard_live_host.py"


class HostRunnerFixtures(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HOST.is_file(), "Read-only host test has not been written")
        self.assertTrue((RECEIPT / "run_host.sh").is_file(), "Host runner has not been written")
        spec = importlib.util.spec_from_file_location("mb38_host", HOST)
        self.host = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.host)
        self.temp = tempfile.TemporaryDirectory(prefix="mb38_host_fixture_", dir="/private/tmp")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def stage(self, phase):
        root, before, out = self.base / "repo", self.base / "before", self.base / phase
        (root / "tools").mkdir(parents=True)
        (before / "tools").mkdir(parents=True)
        (root / "tools/dashboard_live.py").write_text("current\n")
        (root / "tools/dashboard_team.py").write_text("new\n")
        (root / "tools/dashboard_active.py").write_text("unchanged\n")
        (before / "tools/dashboard_live.py").write_text("original\n")
        self.host.stage_sources(root, before, out, phase)
        return out

    def test_red_uses_original_sources_and_omits_new_team(self):
        out = self.stage("red")
        self.assertEqual((out / "tools/dashboard_live.py").read_text(), "original\n")
        self.assertFalse((out / "tools/dashboard_team.py").exists())
        self.assertEqual((out / "tools/dashboard_active.py").read_text(), "unchanged\n")

    def test_green_uses_current_sources(self):
        out = self.stage("green")
        self.assertEqual((out / "tools/dashboard_live.py").read_text(), "current\n")
        self.assertEqual((out / "tools/dashboard_team.py").read_text(), "new\n")

    def test_tmux_mutations_are_rejected_before_execution(self):
        for verb in ("kill-session", "kill-pane", "split-window", "respawn-pane", "rename-window", "send-keys", "set-option", "new-session"):
            with self.subTest(verb=verb), patch.object(self.host.subprocess, "run") as run:
                with self.assertRaises(ValueError):
                    self.host.observe(["tmux", verb], self.base, verb)
                run.assert_not_called()

    def test_denied_observation_saves_exit_and_error(self):
        with patch.object(self.host.subprocess, "run", side_effect=PermissionError("fixture denial")):
            with self.assertRaises(RuntimeError):
                self.host.observe(["/bin/ps", "-axo", "command="], self.base, "ps")
        self.assertEqual((self.base / "ps.exit").read_text().strip(), "126")
        self.assertIn("fixture denial", (self.base / "ps.stderr").read_text())

    def test_empty_observation_is_not_success(self):
        empty = subprocess.CompletedProcess([], 0, "", "")
        with patch.object(self.host.subprocess, "run", return_value=empty):
            with self.assertRaisesRegex(RuntimeError, "empty"):
                self.host.observe(["tmux", "list-sessions"], self.base, "sessions")

    def test_dependency_control_reexecs_current_code(self):
        result = self.host.dependency_reload(ROOT / "tools", self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("HELPER_RELOADED", result.stdout)

    def test_dependency_control_fails_on_original_code(self):
        result = self.host.dependency_reload(RECEIPT / "before/tools", self.base)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("RELOAD_MISSED", result.stdout)

    def test_runner_rejects_invalid_arguments_without_observations(self):
        result = subprocess.run(["/bin/bash", str(RECEIPT / "run_host.sh"), "bad/label", "green"],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("Usage:", result.stderr)

    def test_host_science_header_checks_visible_current_update(self):
        self.assertTrue(hasattr(self.host, "updated_header_matches"), "Host header assertion must respect pane width")
        live = SimpleNamespace(clip=lambda text, width: text[:width])
        updated = "2026-10-11 " + "recorded historical ruling; " * 100
        header = (" ■ SCIENCE REPORT · updated " + updated)[:109]
        self.assertTrue(self.host.updated_header_matches([header], updated, live))
        self.assertFalse(self.host.updated_header_matches([header], "2026-10-01 stale narrative", live))


if __name__ == "__main__":
    unittest.main()
