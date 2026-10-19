"""Empty manifest leaves refuse through the real ledger_db CLI."""
import os
import subprocess
import sys
import unittest

from test_ledger_db import Fixture, SCRIPT


class EmptyManifestLeaves(unittest.TestCase):
    def test_empty_manifest_leaves_refuse(self):
        fx = Fixture(self)  # Fixture registers its temporary tree with addCleanup.
        fx.m1 = fx.manifest("empty.json", "u1", leaves=[])
        fx.write_plans(fx.entries()[:1])
        result = subprocess.run([sys.executable, "-B", SCRIPT, *fx.argv()],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(len(result.stderr.splitlines()), 1, result.stderr)
        self.assertTrue(result.stderr.endswith("\n"))
        self.assertIn("ledger_db: refused:", result.stderr)
        self.assertIn("entries[0].leaves", result.stderr)
        self.assertFalse(os.path.lexists(fx.out))
