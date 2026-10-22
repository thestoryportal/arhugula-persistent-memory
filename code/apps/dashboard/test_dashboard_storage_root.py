"""Import-time storage roots; no scans of real repositories or mounts."""
import importlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


class StorageRootTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="storage-root-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "relocated-repo"
        self.root.mkdir()
        modules = mock.patch.dict(sys.modules)
        modules.start()
        self.addCleanup(modules.stop)
        paths = mock.patch.object(sys, "path", sys.path[:])
        paths.start()
        self.addCleanup(paths.stop)
        environ = mock.patch.dict(os.environ)
        environ.start()
        self.addCleanup(environ.stop)

    def load(self):
        # [LAW:behavior-not-structure] Exercise root selection at a fresh import.
        sys.modules.pop("apps.dashboard.dashboard_storage", None)
        return importlib.import_module("apps.dashboard.dashboard_storage")

    def test_main_root_uses_environment(self):
        os.environ["LLMDB_ROOT"] = str(self.root)
        self.assertEqual(self.load().MAIN_ROOT, self.root)

    def test_main_root_without_environment_uses_own_repo(self):
        os.environ.pop("LLMDB_ROOT", None)
        self.assertEqual(self.load().MAIN_ROOT, Path(__file__).resolve().parents[3])

    def test_main_root_with_empty_environment_uses_own_repo(self):
        os.environ["LLMDB_ROOT"] = ""
        self.assertEqual(self.load().MAIN_ROOT, Path(__file__).resolve().parents[3])

    def test_mirror_root_stays_fixed_after_relocation(self):
        os.environ["LLMDB_ROOT"] = str(self.root)
        mirror = Path("/Volumes/memit/llm-database-poc-mirror")
        self.assertNotEqual(self.root.parent, mirror)
        self.assertEqual(self.load().MIRROR_ROOT, mirror)


if __name__ == "__main__":
    unittest.main()
