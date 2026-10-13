"""Test byte copies and session routing with isolated roots."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = "# Routing café\r\nKeep trailing spaces  \r\nNo final newline".encode("utf-8")
MAP_PAYLOAD = b"# Code map\nDifferent source bytes  \n"
CATALOGS = (("CLAUDE.md", PAYLOAD, ("AGENTS.md", "routing.md")),
            ("map/CLAUDE.md", MAP_PAYLOAD, ("map/AGENTS.md", "map/routing.md")))


class TwinsTests(unittest.TestCase):
    def setUp(self):
        # Keep fixtures for inspection. This lane forbids file deletion.
        self.root = Path(tempfile.mkdtemp(prefix="icm-twins-test-"))
        self.seed_sources()

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

    def seed_sources(self, missing=None):
        for source, payload, names in CATALOGS:
            if source != missing:
                path = self.root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)

    def seed_twins(self, missing=None):
        for source, payload, names in CATALOGS:
            for name in names:
                if name != missing:
                    path = self.root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(payload)

    def test_write_then_check_preserves_every_byte(self):
        result = self.run_tool("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        for source, payload, names in CATALOGS:
            for name in names:
                self.assertTrue((self.root / name).is_file(), name)
                self.assertEqual((self.root / name).read_bytes(), payload)
        result = self.run_tool("--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_root_falls_back_to_tool_location(self):
        result = self.run_tool("--write", fallback=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for source, payload, names in CATALOGS:
            for name in names:
                self.assertTrue((self.root / name).is_file(), name)
                self.assertEqual((self.root / name).read_bytes(), payload)
        result = self.run_tool("--check", fallback=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_names_each_twin_with_one_changed_byte(self):
        for source, payload, names in CATALOGS:
            for name in names:
                with self.subTest(name=name):
                    self.seed_twins()
                    (self.root / name).write_bytes(payload.replace(b"#", b"!", 1))
                    result = self.run_tool("--check")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(f"{name}: differs from {source}".encode(), result.stdout)

    def test_check_rejects_whitespace_and_line_ending_drift(self):
        for source, payload, names in CATALOGS:
            for changed in (payload.replace(b"  ", b" "),
                            payload.replace(b"\r\n", b"\n") if b"\r\n" in payload
                            else payload.replace(b"\n", b"\r\n"), payload + b"\n"):
                for name in names:
                    with self.subTest(name=name, changed=changed):
                        self.seed_twins()
                        (self.root / name).write_bytes(changed)
                        result = self.run_tool("--check")
                        self.assertEqual(result.returncode, 1, result.stderr)
                        self.assertIn(name.encode(), result.stdout)

    def test_check_names_missing_twin(self):
        original = self.root
        for source, payload, names in CATALOGS:
            for missing in names:
                with self.subTest(missing=missing):
                    self.root = original / missing.replace("/", "-").replace(".md", "")
                    self.root.mkdir()
                    self.seed_sources()
                    self.seed_twins(missing=missing)
                    result = self.run_tool("--check")
                    self.root = original
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(f"{missing}: missing".encode(), result.stdout)

    def test_missing_source_fails_both_modes_without_writing_its_twins(self):
        original = self.root
        for source, payload, names in CATALOGS:
            for mode in ("--check", "--write"):
                for existing in (False, True):
                    with self.subTest(source=source, mode=mode, existing=existing):
                        self.root = Path(tempfile.mkdtemp(prefix="icm-twins-missing-"))
                        self.seed_sources(missing=source)
                        if existing:
                            for name in names:
                                path = self.root / name
                                path.parent.mkdir(parents=True, exist_ok=True)
                                path.write_bytes(b"preserve existing twin")
                        result = self.run_tool(mode)
                        self.assertEqual(result.returncode, 1, result.stderr)
                        self.assertIn(f"{source}: missing".encode(), result.stdout)
                        self.assertEqual(result.stderr, b"")
                        for name in names:
                            path = self.root / name
                            if existing:
                                self.assertEqual(path.read_bytes(), b"preserve existing twin")
                            else:
                                self.assertFalse(path.exists())
                        self.root = original

    def test_root_only_change_does_not_touch_map_twins(self):
        self.seed_twins()
        map_names = ("map/AGENTS.md", "map/routing.md")
        for name in map_names:
            os.utime(self.root / name, ns=(1_000_000_000, 1_000_000_000))
        before = {name: (self.root / name).stat().st_mtime_ns for name in map_names}
        changed = PAYLOAD + b"\nRoot-only change"
        (self.root / "CLAUDE.md").write_bytes(changed)
        result = self.run_tool("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("AGENTS.md", "routing.md"):
            self.assertEqual((self.root / name).read_bytes(), changed)
        for name in map_names:
            self.assertEqual((self.root / name).read_bytes(), MAP_PAYLOAD)
            self.assertEqual((self.root / name).stat().st_mtime_ns, before[name])
        result = self.run_tool("--check")
        self.assertEqual(result.returncode, 0, result.stderr)

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
