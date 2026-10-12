"""Test state views and closeout checks in retained temporary copies."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ("program/STATUS.md", "_index/program-state.md", "program/scorecard.md")
LINKS = ("README.md", "program/runbook/00-entry-point-read-first-every-session.md",
         "program/SESSION_BOOTSTRAP.md", "program/PROGRESS.md")


class StateViews(unittest.TestCase):
    def setUp(self):
        # Keep the fixtures. The lane forbids file deletion.
        self.root = Path(tempfile.mkdtemp(prefix="icm-5c-state-"))
        for name in ("code/state/render_state.py", "program/program_state.json") + LINKS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def run_cli(self, mode=None):
        args = [sys.executable, "-B", str(self.root / "code/state/render_state.py")]
        if mode is not None:
            args.append(mode)
        return subprocess.run(args, cwd=self.root,
                              env=dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH="code"),
                              capture_output=True, text=True)

    def write(self):
        result = self.run_cli("--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in VIEWS:
            self.assertTrue((self.root / name).is_file(), name)

    def test_write_then_check_and_default_mode_are_current(self):
        self.write()
        for mode in ("--check", None):
            result = self.run_cli(mode)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in VIEWS:
            top = (self.root / name).read_text().splitlines()[0]
            self.assertIn("generated", top.lower())
            self.assertIn("LLMDB_ROOT=$PWD", top)

    def test_changed_source_is_stale(self):
        self.write()
        path = self.root / "program/program_state.json"
        state = json.loads(path.read_text())
        state["north_star"] = "A changed north star."
        path.write_text(json.dumps(state))
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("program/STATUS.md", result.stdout)
        self.assertIn("_index/program-state.md", result.stdout)

    def test_change_outside_the_visible_summaries_is_stale(self):
        self.write()
        path = self.root / "program/program_state.json"
        state = json.loads(path.read_text())
        state["work_queue"]["items"][0]["notes"].append("A new queue note.")
        path.write_text(json.dumps(state))
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        for name in VIEWS:
            self.assertIn(name, result.stdout)

    def test_large_lists_and_north_star_render_with_overflow_counts(self):
        path = self.root / "program/program_state.json"
        state = json.loads(path.read_text())
        state["north_star"] = "x" * (20 * 1024)
        state["next_actions"] = [f"action{i}: " + "x" * 1000 for i in range(200)]
        state["work_queue"]["items"] = [
            {"id": f"queue{i}", "state": "ready", "title": "A queued task.",
             "summary": "x" * 1000} for i in range(200)]
        path.write_text(json.dumps(state))
        self.write()
        data = (self.root / "program/STATUS.md").read_bytes()
        self.assertLessEqual(len(data), 11000)
        text = data.decode()
        self.assertEqual(text.count("more: see `_index/program-state.md`"), 2)
        actions = len(re.findall(r"^\d+\. ", text, re.M))
        queue = len(re.findall(r"^- \*\*queue\d+\*\*", text, re.M))
        for count in (actions, queue):
            self.assertGreater(count, 0)
            self.assertLess(count, 200)
            self.assertIn(f"{200 - count} more: see `_index/program-state.md`", text)
        full = (self.root / "_index/program-state.md").read_text()
        self.assertIn("action199:", full)
        self.assertIn("queue199", full)
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_displayed_fields_have_byte_bounds(self):
        path = self.root / "program/program_state.json"
        state = json.loads(path.read_text())
        long_text = "界" * 7000
        for name in ("updated", "north_star", "current_latest", "f1_verdict"):
            state[name] = long_text
        state["next_actions"] = [long_text] * 200
        state["work_queue"]["items"] = [
            {"id": long_text, "state": long_text, "title": long_text, "summary": long_text}
            for i in range(200)]
        path.write_text(json.dumps(state))
        self.write()
        data = (self.root / "program/STATUS.md").read_bytes()
        self.assertLessEqual(len(data), 11000)
        self.assertIn("more: see `_index/program-state.md`", data.decode())

    def test_queue_summary_is_optional(self):
        path = self.root / "program/program_state.json"
        state = json.loads(path.read_text())
        state["work_queue"]["items"] = [
            {"id": "summary-free-task", "state": "ready", "title": "A task without a summary."}]
        path.write_text(json.dumps(state))
        self.write()
        text = (self.root / "program/STATUS.md").read_text()
        self.assertIn("summary-free-task", text)
        self.assertIn("A task without a summary.", text)
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_second_write_changes_no_bytes_or_mtimes(self):
        self.write()
        before = {p: ((self.root / p).read_bytes(), (self.root / p).stat().st_mtime_ns)
                  for p in VIEWS + LINKS}
        self.write()
        after = {p: ((self.root / p).read_bytes(), (self.root / p).stat().st_mtime_ns)
                 for p in VIEWS + LINKS}
        self.assertEqual(before, after)

    def test_status_is_bounded_and_lists_all_open_items_and_actions(self):
        self.write()
        content = (self.root / "program/STATUS.md").read_bytes()
        self.assertLessEqual(len(content), 11000)
        text = content.decode()
        self.assertNotIn(" more: see ", text)
        for heading in ("North star", "Current position", "Next actions", "Open work queue"):
            self.assertIn(heading, text)
        state = json.loads((self.root / "program/program_state.json").read_text())
        self.assertIn(state["north_star"], text)
        for item in state["work_queue"]["items"]:
            if item["state"] not in ("done", "cancelled"):
                self.assertIn(item["id"], text)
                self.assertIn(item["state"], text)
        for i in range(len(state["next_actions"])):
            self.assertIn(f"\n{i + 1}. ", text)

    def test_link_files_have_links_and_no_generated_blocks(self):
        self.write()
        for name in LINKS:
            text = (self.root / name).read_text()
            self.assertNotIn("GENERATED:", text, name)
            self.assertIn("scorecard.md" if name.endswith("PROGRESS.md") else "STATUS.md", text)

    def test_missing_views_exit_one_without_writing(self):
        before = {p: (self.root / p).read_bytes() for p in LINKS}
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        for name in VIEWS:
            self.assertIn(name, result.stdout)
            self.assertFalse((self.root / name).exists())
        self.assertEqual(before, {p: (self.root / p).read_bytes() for p in LINKS})

    def test_each_stale_view_fails_check(self):
        self.write()
        for name in VIEWS:
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b"stale\n")
                result = self.run_cli("--check")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(name, result.stdout)
                self.assertEqual(path.read_bytes(), original + b"stale\n")
                path.write_bytes(original)


class CloseoutMovedViews(unittest.TestCase):
    DID = "D-FIXTURE-5C"

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="icm-5c-closeout-"))
        target = self.root / "code/gates/closeout_check.py"
        target.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "code/gates/closeout_check.py", target)
        files = {
            "code/gates/closeout_fingerprints.json": "{}",
            "program/runbook/00-entry-point-read-first-every-session.md":
                "### §0.3 — next actions\n[Program status](../STATUS.md)\n### §0.4 — closeout\n",
            "program/runbook/12-dashboard.md": "## §12 — dashboard\n" + self.DID,
            "program/runbook/13-changelog.md": "\n## §13 — changelog\n" + self.DID,
            "program/checkpoints/fixture.md": self.DID,
            "program/PROGRESS.md": "[F1 scorecard](scorecard.md)\n",
            "program/scorecard.md": self.DID,
            "_index/program-state.md": self.DID,
            "program/EVIDENCE_INDEX.md": self.DID,
            "program/registers/EXPERIMENT_REGISTRY.md": self.DID,
            "_system/memory/MEMORY.md": "# Fixture memory\n",
        }
        for name in ("00_MASTER_EVIDENCE", "03_STATUS_LEDGER", "01_PROVENANCE_MANIFEST", "02_VANDV_CHAIN"):
            files[f"evidence/CORPUS/{name}.md"] = self.DID
        for name, content in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.live = self.root / "live-memory"
        self.live.mkdir()

    def run_gate(self, did=None):
        return subprocess.run([sys.executable, "-B", str(self.root / "code/gates/closeout_check.py"),
                               did or self.DID], cwd=self.root,
                              env=dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH="code",
                                       LLMDB_LIVE_MEMORY=str(self.live)), capture_output=True, text=True)

    def test_moved_blocks_still_supply_the_decision_id(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLOSE-OUT COMPLETE", result.stdout)

    def test_missing_decision_in_full_state_fails_section_check(self):
        (self.root / "_index/program-state.md").write_text("D-OTHER\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"\[MISSING\].*§0\.3 next-actions")

    def test_missing_decision_in_scorecard_fails_tracker_check(self):
        (self.root / "program/scorecard.md").write_text("D-OTHER\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"\[MISSING\].*program/PROGRESS\.md")

    def test_fake_decision_is_not_complete(self):
        result = self.run_gate("D-NOT-A-REAL-5C-DECISION")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn("CLOSE-OUT COMPLETE", result.stdout)


if __name__ == "__main__":
    unittest.main()
