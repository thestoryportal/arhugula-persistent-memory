"""Intel-copy exemptions follow the selected repo, with literal root matching."""
import os
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest import mock


class IntelCopyRoot(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.base = Path(folder.name).resolve()
        self.repo = self.base / "repo"
        self.source = self.repo / "code/lab/runners/c10w_p2_gate.py"
        self.source.parent.mkdir(parents=True)
        shutil.copyfile(Path(__file__).with_name("c10w_p2_gate.py"), self.source)

    def load_gate(self, root):
        env = dict(os.environ)
        env.pop("LLMDB_ROOT", None)
        if root is not None:
            env["LLMDB_ROOT"] = str(root)
        with mock.patch.dict(os.environ, env, clear=True):
            return runpy.run_path(str(self.source))["blocking_processes"]

    def check_paths(self, gate, root, blocked):
        # [LAW:behavior-not-structure] Exercise the inventory decision, not regex internals.
        for exe in ("/Library/Developer/CommandLineTools/usr/bin/python3",
                    "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python"):
            for script in ("tools/memit_intel_copy.py", "code/ops/intel/memit_intel_copy.py"):
                for action in ("manifest", "run --gen sample"):
                    path = str(root / script) if root is not None else script
                    line = "510 %s %s %s" % (exe, path, action)
                    with self.subTest(exe=exe, path=path, action=action):
                        self.assertEqual(gate(line, own_pid=1), [line] if blocked else [])

    def test_set_root(self):
        root = self.base / "selected"
        gate = self.load_gate(root)
        self.check_paths(gate, root, False)
        self.check_paths(gate, None, False)
        self.check_paths(gate, self.repo, True)

    def test_unset_root_uses_file_repo(self):
        gate = self.load_gate(None)
        self.check_paths(gate, self.repo, False)
        self.check_paths(gate, None, False)
        self.check_paths(gate, self.base / "other", True)

    def test_another_root_refused(self):
        root = self.base / "selected"
        self.check_paths(self.load_gate(root), root, False)
        self.check_paths(self.load_gate(self.base / "other"), root, True)

    def test_root_regex_characters_are_literal(self):
        root = self.base / "repo+.v1"
        gate = self.load_gate(root)
        self.check_paths(gate, root, False)
        self.check_paths(gate, self.base / "repooXv1", True)
        self.check_paths(gate, self.base / "repo+Xv1", True)


if __name__ == "__main__":
    unittest.main()
