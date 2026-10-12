import tempfile
import unittest
from pathlib import Path

from state import llmdb_records as L


class Layout(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, rel, events=True):
        d = self.root / rel
        d.mkdir(parents=True)
        if events:
            (d / "events.jsonl").write_text("")
        return d

    def test_run_and_halt_folders(self):
        run = L.run_dir(self.root, "ml", "m2_x")
        self.assertEqual(run, self.root / "experiments/ml/runs/m2_x")
        self.assertEqual(L.halts_dir(run), run / "halts")

    def test_lab_scans_cover_both_records(self):
        a = self.make("experiments/ml/runs/harvest_1")
        b = self.make("experiments/new1/runs/new1_2026")
        self.make("experiments/c10y/runs/other")          # not a MathLab-runtime record
        self.make("experiments/ml/runs/no_events", events=False)
        self.assertEqual(L.lab_event_streams(self.root), [a / "events.jsonl", b / "events.jsonl"])
        self.assertEqual([d.name for d in L.lab_run_dirs(self.root)], ["harvest_1", "no_events", "new1_2026"])

    def test_missing_records_scan_empty(self):
        self.assertEqual(L.lab_event_streams(self.root), [])

    def test_new1_namespace_excludes_dispatch_receipts(self):
        self.assertTrue(L.is_new1_namespace("new1_20261010T235740.858576Z"))
        self.assertTrue(L.is_new1_namespace("new1_current"))
        self.assertFalse(L.is_new1_namespace("new1_dispatch_20261010T235738Z"))
        self.assertFalse(L.is_new1_namespace("harvest_1"))

    def test_read_split_joins_parts_in_name_order(self):
        d = self.root / "program/runbook"; d.mkdir(parents=True)
        (d / "01-b.md").write_text("two\n"); (d / "00-a.md").write_text("one\n"); (d / "notes.txt").write_text("x")
        self.assertEqual(L.read_split(d), "one\ntwo\n")

    def test_read_split_refuses_missing_or_empty(self):
        with self.assertRaises(FileNotFoundError):
            L.read_split(self.root / "absent")
        (self.root / "empty").mkdir()
        with self.assertRaises(FileNotFoundError):
            L.read_split(self.root / "empty")


if __name__ == "__main__":
    unittest.main()
