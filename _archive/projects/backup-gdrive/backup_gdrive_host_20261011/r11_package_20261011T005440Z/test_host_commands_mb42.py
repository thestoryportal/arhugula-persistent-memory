"""Regression for the nine MAESTRO examples; reads the document only."""
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ACTIONS = ("e-red", "e-green", "coverage", "fixture", "frozen", "package",
           "check-red", "check-green", "pins")

class HostCommandsRootTest(unittest.TestCase):
    def test_all_outer_dispatch_examples_set_worktree_root(self):
        lines = (HERE / "host_commands.md").read_text().splitlines()
        dispatch = [line for line in lines
                    if '/bin/sh "$R/host_commands.sh" ' in line]
        expected = ['LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" ' + action
                    for action in ACTIONS]
        self.assertEqual(dispatch, expected,
                         "Every outer example must set LLMDB_ROOT=$PWD")

if __name__ == "__main__":
    unittest.main(verbosity=2)
