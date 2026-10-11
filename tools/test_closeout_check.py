"""Runbook section spans for the close-out gate: each span is bounded by its own heading level."""
import os
import sys
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


if __name__ == "__main__":
    unittest.main()
