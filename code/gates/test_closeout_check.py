"""Runbook section spans for the close-out gate: each span is bounded by its own heading level."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import closeout_check as cc

RUNBOOK = """# Runbook
### §0.3 — next actions
D-OLD-1 next
### §0.4 — tracker list
D-NOT-IN-03
## §12 — LIVE STATUS DASHBOARD
D-DASH
## §13 — CHANGELOG (append-only)
### §13 changelog — 2026-06-18
D-OLDEST entry
### §13 changelog — 2026-10-10
D-MIDDLE entry
### §13 changelog — 2026-10-11
D-NEWEST entry
"""


class RunbookSections(unittest.TestCase):
    def setUp(self):
        self.s = cc.runbook_sections(RUNBOOK)

    def test_changelog_span_holds_every_entry_not_only_the_newest(self):
        for tok in ("D-OLDEST", "D-MIDDLE", "D-NEWEST"):
            self.assertIn(tok, self.s["§13 changelog"])

    def test_dashboard_span_ends_at_the_changelog(self):
        self.assertIn("D-DASH", self.s["§12 dashboard"])
        self.assertNotIn("D-OLDEST", self.s["§12 dashboard"])

    def test_next_actions_span_ends_at_0_4(self):
        self.assertIn("D-OLD-1", self.s["§0.3 next-actions"])
        self.assertNotIn("D-NOT-IN-03", self.s["§0.3 next-actions"])

    def test_deeper_heading_does_not_open_a_section(self):
        s = cc.runbook_sections("#### §0.3 decoy\nD-DECOY\n" + RUNBOOK)
        self.assertNotIn("D-DECOY", s["§0.3 next-actions"])

    def test_missing_heading_gives_empty_span(self):
        s = cc.runbook_sections("# no sections here\nD-X\n")
        self.assertEqual(set(s.values()), {""})


GIT_FREE_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


class SparseSource(unittest.TestCase):
    """--audit skips a fingerprint source only when the repo is sparse, the entry is skip-worktree, and the file is absent."""

    SOURCE = "docs/source.md"

    def build(self, root, sparse, skip_worktree, present, tracker=None):
        def git(*args):
            subprocess.run(["git", "-C", root, *args], check=True, capture_output=True, env=GIT_FREE_ENV)
        git("init", "-q")
        os.makedirs(os.path.join(root, "docs"))
        os.makedirs(os.path.join(root, "code/gates"))
        with open(os.path.join(root, self.SOURCE), "w") as f:
            f.write("result: k<=1\n")
        with open(os.path.join(root, "code/gates/closeout_fingerprints.json"), "w") as f:
            json.dump({"D-X": {"source": self.SOURCE}}, f)
        git("add", "-A")
        git("config", "core.sparseCheckout", "true" if sparse else "false")
        # Without this, git clears the S bit of a file present on disk, so a present S entry could not be built.
        git("config", "sparse.expectFilesOutsideOfPatterns", "true")
        if skip_worktree:
            git("update-index", "--skip-worktree", self.SOURCE)
        if present:
            with open(os.path.join(root, self.SOURCE), "w") as f:
                f.write("result: k<=2\n")
        else:
            os.remove(os.path.join(root, self.SOURCE))
        if tracker:
            os.makedirs(os.path.join(root, "program"))
            with open(os.path.join(root, "program/EVIDENCE_INDEX.md"), "w") as f:
                f.write(tracker)

    def audit(self, **fixture):
        with tempfile.TemporaryDirectory() as root:
            self.build(root, **fixture)
            r = subprocess.run([sys.executable, "-B", os.path.abspath(cc.__file__), "--audit"], capture_output=True,
                               text=True, env={**GIT_FREE_ENV, "LLMDB_ROOT": root})
        return r.returncode, r.stdout + r.stderr

    def test_sparse_absent_s_entry_skipped(self):
        code, out = self.audit(sparse=True, skip_worktree=True, present=False)
        self.assertEqual(code, 0, out)
        self.assertIn("[SPARSE] D-X", out)
        self.assertNotIn("[FP ERR]", out)

    def test_missing_without_sparse_fails(self):
        code, out = self.audit(sparse=False, skip_worktree=True, present=False)
        self.assertEqual(code, 1, out)
        self.assertIn("[FP ERR] D-X: source file missing", out)
        self.assertNotIn("[SPARSE]", out)

    def test_missing_without_skip_worktree_fails(self):
        code, out = self.audit(sparse=True, skip_worktree=False, present=False)
        self.assertEqual(code, 1, out)
        self.assertIn("[FP ERR] D-X: source file missing", out)
        self.assertNotIn("[SPARSE]", out)

    def test_skip_worktree_source_on_disk_is_still_checked(self):
        code, out = self.audit(sparse=True, skip_worktree=True, present=True, tracker="D-X@00000000\n")
        self.assertEqual(code, 1, out)
        self.assertIn("[STALE ] D-X@", out)
        self.assertNotIn("[SPARSE]", out)


if __name__ == "__main__":
    unittest.main()
