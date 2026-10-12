"""Test byte copies and session routing with isolated roots."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = "# Routing café\r\nKeep trailing spaces  \r\nNo final newline".encode("utf-8")


class TwinsTests(unittest.TestCase):
    def setUp(self):
        # Keep fixtures for inspection. This lane forbids file deletion.
        self.root = Path(tempfile.mkdtemp(prefix="icm-twins-test-"))
        (self.root / "CLAUDE.md").write_bytes(PAYLOAD)

    def run_tool(self, mode, fallback=False):
        source = ROOT / "code/agents/twins.py"
        self.assertTrue(source.is_file(), "The twins tool is missing")
        env = os.environ.copy()
        if fallback:
            tool = self.root / "code/agents/twins.py"
            tool.parent.mkdir(parents=True, exist_ok=True)
            tool.write_bytes(source.read_bytes())
            env.pop("LLMDB_ROOT", None)
        else:
            tool = source
            env["LLMDB_ROOT"] = str(self.root)
        return subprocess.run(
            [sys.executable, "-B", str(tool), mode],
            cwd=self.root.parent, env=env, capture_output=True,
        )

    def seed_twins(self):
        for name in ("AGENTS.md", "routing.md"):
            (self.root / name).write_bytes(PAYLOAD)

    def test_write_then_check_preserves_every_byte(self):
        result = self.run_tool("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("AGENTS.md", "routing.md"):
            self.assertEqual((self.root / name).read_bytes(), PAYLOAD)
        result = self.run_tool("--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_root_falls_back_to_tool_location(self):
        result = self.run_tool("--write", fallback=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("AGENTS.md", "routing.md"):
            self.assertEqual((self.root / name).read_bytes(), PAYLOAD)
        result = self.run_tool("--check", fallback=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_names_each_twin_with_one_changed_byte(self):
        for name in ("AGENTS.md", "routing.md"):
            with self.subTest(name=name):
                self.seed_twins()
                (self.root / name).write_bytes(PAYLOAD.replace(b"Keep", b"keep"))
                result = self.run_tool("--check")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(name.encode(), result.stdout + result.stderr)

    def test_check_rejects_whitespace_and_line_ending_drift(self):
        for changed in (PAYLOAD.replace(b"spaces  ", b"spaces "),
                        PAYLOAD.replace(b"\r\n", b"\n"), PAYLOAD + b"\n"):
            for name in ("AGENTS.md", "routing.md"):
                with self.subTest(name=name, changed=changed):
                    self.seed_twins()
                    (self.root / name).write_bytes(changed)
                    result = self.run_tool("--check")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(name.encode(), result.stdout + result.stderr)

    def test_check_names_missing_twin(self):
        for missing, present in (("AGENTS.md", "routing.md"),
                                 ("routing.md", "AGENTS.md")):
            with self.subTest(missing=missing):
                isolated = self.root / missing.replace(".md", "")
                isolated.mkdir()
                (isolated / "CLAUDE.md").write_bytes(PAYLOAD)
                (isolated / present).write_bytes(PAYLOAD)
                original = self.root
                self.root = isolated
                result = self.run_tool("--check")
                self.root = original
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(missing.encode(), result.stdout + result.stderr)

    def run_hook(self):
        hook = self.root / ".codex/hooks/session_start.py"
        hook.parent.mkdir(parents=True)
        hook.write_bytes((ROOT / ".codex/hooks/session_start.py").read_bytes())
        decoy = self.root / "wrong-root"
        decoy.mkdir()
        (decoy / "routing.md").write_bytes(b"WRONG ROUTING ROOT")
        env = dict(os.environ, LLMDB_ROOT=str(decoy), PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(hook)], cwd=decoy,
            env=env, capture_output=True,
        )

    def test_hook_prints_full_routing_from_its_own_root(self):
        (self.root / "routing.md").write_bytes(PAYLOAD)
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(PAYLOAD, result.stdout)
        self.assertNotIn(b"WRONG ROUTING ROOT", result.stdout)
        self.assertNotIn(b"Read order:", result.stdout)
        self.assertNotIn(b"Load `_system/governance/DISCIPLINE.md`", result.stdout)
        self.assertIn(b"NORTH STAR (F1):", result.stdout)
        self.assertIn(b"Advisor route for Codex-led science:", result.stdout)

    def test_hook_reports_missing_routing_without_failure(self):
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        missing_lines = [line for line in result.stdout.splitlines()
                         if b"routing.md" in line and b"missing" in line.lower()]
        self.assertEqual(len(missing_lines), 1, result.stdout)
        self.assertNotIn(b"WRONG ROUTING ROOT", result.stdout)


if __name__ == "__main__":
    unittest.main()
