"""MB37 refresh regressions. Stdlib only; every process uses temporary sinks."""
import importlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import dashboard_live as live
import dashboard_experiment as experiment
import dashboard_mathlab as mathlab
import dashboard_report as report

ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")
EMPTY = {"rulings": [], "alerts": [], "builds": [], "helpers": [],
         "gpu": {"running": None, "jobs": [], "cpu_jobs": [], "last_exit": None, "last_name": None}}


class ReloadDependencies(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mb37_refresh_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.tools = self.root / "tools"
        self.tools.mkdir()

    def source(self, name, text, stamp):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        os.utime(path, (stamp, stamp))
        return path

    def test_imported_mathlab_changes_trigger_reload(self):
        self.source("tools/dashboard_lab.py", "import mathlab_events\n", 100)
        dep = self.source("code/apps/mathlab/mathlab_events.py", "GATE_PLAN = ()\n", 90)
        stamp = live.source_stamp(str(self.tools))
        os.utime(dep, (200, 200))
        self.assertTrue(live.sources_changed(str(self.tools), stamp))
        self.assertEqual(live.source_stamp(str(self.tools)), 200)

    def test_lazy_package_import_is_stamped_without_importing_it(self):
        self.source("code/apps/dashboard/dashboard_storage.py", "def read():\n from tools.backup_gdrive_status import check\n", 100)
        self.source("code/ops/backup/backup_gdrive_status.py", "raise RuntimeError('must not import')\n", 300)
        self.assertEqual(live.source_stamp(str(self.tools)), 300)

    def test_transitive_relative_dependencies_and_cycles(self):
        self.source("tools/dashboard_x.py", "from helpers.reader import read\n", 100)
        self.source("tools/helpers/__init__.py", "from . import reader\n", 110)
        self.source("tools/helpers/reader.py", "from . import rules\n", 120)
        self.source("tools/helpers/rules.py", "from . import reader\n", 400)
        self.assertEqual(live.source_stamp(str(self.tools)), 400)

    def test_unrelated_repo_and_external_modules_do_not_trigger_reload(self):
        self.source("tools/dashboard_x.py", "import json\n", 100)
        self.source("tools/unrelated.py", "unused = True\n", 900)
        self.assertEqual(live.source_stamp(str(self.tools)), 100)

    def test_mathlab_reexecs_before_a_second_frame_after_helper_change(self):
        self.source("tools/dashboard_lab.py", "import mathlab_events\n", 100)
        dep = self.source("code/apps/mathlab/mathlab_events.py", "GATE_PLAN = ()\n", 90)
        frames = []
        class Reloaded(Exception):
            pass
        class DidNotReload(Exception):
            pass
        class Terminal(io.StringIO):
            def fileno(self):
                return 1
        def draw(*args):
            frames.append(args)
            os.utime(dep, (200, 200))
            return ["frame"]
        sleeps = []
        def sleep(seconds):
            sleeps.append(seconds)
            if len(sleeps) == 2:
                raise DidNotReload()
        with patch.object(live, "TOOLS", str(self.tools)), patch.object(live.os, "execv", side_effect=Reloaded), \
             patch.object(mathlab, "render", side_effect=draw), patch.object(mathlab.time, "sleep", side_effect=sleep), \
             patch.object(mathlab.os, "get_terminal_size", return_value=os.terminal_size((110, 40))), \
             patch.object(sys, "argv", ["dashboard_mathlab.py"]), patch.object(sys, "stdout", Terminal()):
            try:
                mathlab.main()
            except (Reloaded, DidNotReload) as error:
                self.assertIsInstance(error, Reloaded, "MathLab rendered stale code instead of re-executing")
        self.assertEqual(len(frames), 1)


class ReplyTokens(unittest.TestCase):
    def alerts(self, text):
        return live.session_alerts({"codexmb35": text}, {}, 1000)

    def test_failed_test_count_is_not_an_error(self):
        self.assertEqual(self.alerts("• Report\n11 passed, 1 failed during RED\n› Ask Codex"), [])

    def test_exact_ready_reply_finishes_after_prior_error(self):
        for token in ("MB35 READY FOR HOST RUN", "DASHBOARD_FIX_READY_FOR_MAESTRO_RUN", "C10_BUILD_DONE", "DONE"):
            with self.subTest(token=token):
                self.assertEqual(self.alerts("Traceback (most recent call last):\nValueError: old RED\n" + token + "\n› Ask Codex"), [])

    def test_ready_or_done_in_prose_does_not_hide_an_error(self):
        for text in ("The report says DONE but verification is incomplete.", "I am READY to investigate."):
            with self.subTest(text=text):
                self.assertEqual(self.alerts("Error: cannot read input\n" + text), ["codexmb35 stopped after an error"])

    def test_a_new_error_after_a_reply_token_is_visible(self):
        self.assertEqual(self.alerts("BUILD_DONE\nError: later failure"), ["codexmb35 stopped after an error"])

    def test_actual_failed_test_run_still_alerts(self):
        self.assertEqual(self.alerts("FAILED (failures=1)\n› Ask Codex"), ["codexmb35 stopped after an error"])


class ScienceAuthority(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mb37_science_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.board, self.program = base / "board.json", base / "program.json"
        self.board.write_text(json.dumps({"updated": "2026-10-01 00:00 MDT", "brief": "A dated scientific explanation.",
                                         "results": [], "queue": [{"name": "OBSOLETE SCOREBOARD QUEUE", "status": "next"}]}))
        self.program.write_text(json.dumps({"updated": "2026-10-10 new ruling", "next_actions": [
            "D-C10r-rulings-17: C10Y DEFERRED until Drive backup is verified.",
            "D-C10r-rulings-18: pre-register one sealed re-test."]}))

    def render(self, cols=160, rows=40):
        with patch.object(report, "BOARD", str(self.board)), \
             patch.object(report, "PROGRAM", str(self.program), create=True), \
             patch.object(live, "gather", return_value=EMPTY), patch.object(live, "events", return_value=[]), \
             patch.object(report.time, "time", return_value=0):
            return report.screen(cols, rows)

    def test_queue_and_updated_come_from_program_not_scoreboard(self):
        text = ANSI.sub("", "\n".join(self.render()))
        self.assertIn("D-C10r-rulings-17: C10Y DEFERRED", text)
        self.assertIn("D-C10r-rulings-18", text)
        self.assertIn("2026-10-10", text)
        self.assertNotIn("OBSOLETE SCOREBOARD QUEUE", text)

    def test_program_is_reread_on_every_frame(self):
        self.render()
        self.program.write_text(json.dumps({"updated": "2026-10-11 latest", "next_actions": ["A new action after the first frame"]}))
        text = ANSI.sub("", "\n".join(self.render()))
        self.assertIn("A new action after the first frame", text)
        self.assertIn("2026-10-11", text)
        self.assertNotIn("D-C10r-rulings-17", text)

    def test_narrative_is_explicitly_dated(self):
        text = ANSI.sub("", "\n".join(self.render()))
        self.assertIn("narrative", text.lower())
        self.assertIn("2026-10-01", text)
        self.assertIn("A dated scientific explanation.", text)

    def test_broken_program_never_falls_back_to_stale_queue(self):
        self.program.write_text("{broken")
        text = ANSI.sub("", "\n".join(self.render()))
        self.assertIn("program", text.lower())
        self.assertIn("cannot read", text.lower())
        self.assertNotIn("OBSOLETE SCOREBOARD QUEUE", text)

    def test_missing_narrative_does_not_hide_live_actions(self):
        self.board.unlink()
        text = ANSI.sub("", "\n".join(self.render()))
        self.assertIn("D-C10r-rulings-17", text)
        self.assertIn("narrative", text.lower())

    def test_long_actions_rotate_with_width_and_height_bounded(self):
        self.program.write_text(json.dumps({"updated": "2026-10-10", "next_actions": [
            f"ACTION-{i} " + "wide ✅ explanation " * 8 for i in range(12)]}))
        seen = set()
        for page in range(50):
            with patch.object(report, "BOARD", str(self.board)), patch.object(report, "PROGRAM", str(self.program), create=True), \
                 patch.object(live, "gather", return_value=EMPTY), patch.object(live, "events", return_value=[]), \
                 patch.object(report.time, "time", return_value=page * 10):
                lines = report.screen(110, 40)
            self.assertLessEqual(len(lines), 40)
            self.assertTrue(all(live.cells(line) < 110 for line in lines))
            seen.update(re.findall(r"ACTION-(\d+)", ANSI.sub("", "\n".join(lines))))
        self.assertEqual(seen, {str(i) for i in range(12)})


class LatestRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="mb37_logs_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def log(self, name, stamp, body="working\n"):
        path = self.root / "results" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        os.utime(path, (stamp, stamp))
        return str(path)

    def state(self):
        ps = subprocess.CompletedProcess([], 0, "1 0 01:00 /sbin/launchd\n", "")
        with patch.object(live, "ROOT", str(self.root)), patch.object(live.subprocess, "run", return_value=ps):
            return live.gpu_state()

    def test_nested_new_run_supersedes_old_coordinator(self):
        self.log("c10w_logs/coordinator.log", 100, "2026-10-08T00:00:00+0000 COORDINATOR_EXIT=0 old\n")
        latest = self.log("c10z_astra/fresh/logs/stage1.log", 200, "2026-10-10T23:00:00+0000 COORDINATOR_EXIT=2 new\n")
        state = self.state()
        self.assertEqual(state["last_name"], "ASTRA")
        self.assertEqual(state["last_exit"]["code"], 2)
        self.assertEqual(state.get("last_log"), latest)

    def test_no_outcome_on_newest_log_does_not_borrow_old_exit(self):
        self.log("c10w_logs/coordinator.log", 100, "2026-10-08T00:00:00+0000 COORDINATOR_EXIT=0 old\n")
        latest = self.log("c10y_directdw/fresh/worker.log", 200)
        state = self.state()
        self.assertIsNone(state["last_exit"])
        self.assertEqual(state.get("last_log"), latest)
        self.assertEqual(state.get("last_at"), 200)
        text = "\n".join(live.now_lines(dict(EMPTY, gpu=state), 260))
        self.assertIn("Step 7", text)
        self.assertIn("1m ago", text)
        self.assertIn("outcome not recorded", text)

    def test_latest_source_excludes_quarantine_and_labviz_mirrors(self):
        latest = self.log("c10z_astra/fresh/worker.log", 200)
        for name in ("c10z_astra/_quarantine_bad/worker.log", "c10w_logs/attempt1_halted/worker.log", "labviz/site/evidence/c10y/a.log"):
            self.log(name, 900)
        state = self.state()
        self.assertEqual(state.get("last_log"), latest)
        with patch.object(experiment, "ROOT", str(self.root)):
            self.assertTrue(experiment.is_experiment_log(latest))
            self.assertFalse(experiment.is_experiment_log(str(self.root / "projects/labviz-spec-v3/receipts/bulk/labviz/site/evidence/c10y/a.log")))


class TeamComposition(unittest.TestCase):
    def team(self):
        self.assertIsNotNone(importlib.util.find_spec("dashboard_team"), "Team needs one self-composing renderer")
        return importlib.import_module("dashboard_team")

    def tmux(self, names):
        def run(args, **kwargs):
            self.assertEqual(args[0], "tmux")
            verb = args[1]
            self.assertIn(verb, ("list-sessions", "list-panes", "capture-pane", "display"), "runtime must read, never rebuild tmux")
            if verb == "list-sessions":
                out = "\n".join(names)
            elif verb == "list-panes":
                out = "maestro28\t100\tclaude\t" + str(ROOT) + "\tclaude\n"
            elif verb == "capture-pane":
                out = "• Working (1s • esc to interrupt)" if args[-1] == "codexmb36" else "• Wrote report\nDONE"
            else:
                out = "Live builder task"
            return subprocess.CompletedProcess(args, 0, out, "")
        return run

    def test_new_builders_appear_retired_builders_disappear(self):
        team = self.team()
        states = {}
        for names, present, absent in ((["dashboard", "maestro28", "codexmb2"], "MB2", "MB36"),
                                        (["dashboard", "maestro28", "codexmb36", "shell"], "MB36", "MB2")):
            with patch.object(live.subprocess, "run", side_effect=self.tmux(names)), patch.object(live, "repo_root", return_value=str(ROOT)):
                lines, counts = team.frame(110, 40, states)
            text = ANSI.sub("", "\n".join(lines))
            self.assertIn(present, text)
            self.assertNotIn(absent, text)
            self.assertNotIn("shell", text)
        self.assertNotIn("codexmb2", states)
        self.assertIn("working 1", counts)
        self.assertIn("idle 1", counts)

    def test_live_lead_name_is_not_frozen_to_program(self):
        team = self.team()
        with patch.object(live.subprocess, "run", side_effect=self.tmux(["maestro28", "codexmb36"])), \
             patch.object(live, "repo_root", return_value=str(ROOT)):
            text = ANSI.sub("", "\n".join(team.frame(110, 40, {})[0]))
        self.assertIn("LEAD", text)
        self.assertIn("maestro28", text)

    def test_overflow_rotates_all_live_builders_and_counts_full_roster(self):
        team = self.team()
        names = ["maestro28"] + [f"codexmb{i}" for i in range(20, 40)]
        seen = set()
        with patch.object(live.subprocess, "run", side_effect=self.tmux(names)), patch.object(live, "repo_root", return_value=str(ROOT)):
            for page in range(20):
                with patch.object(team.time, "time", return_value=1000 + page * 10):
                    lines, counts = team.frame(110, 40, {})
                self.assertLessEqual(len(lines), 40)
                self.assertTrue(all(live.cells(line) < 110 for line in lines))
                seen.update(re.findall(r"MB(\d+)", ANSI.sub("", "\n".join(lines))))
                self.assertIn("idle 20", counts)
                self.assertIn("working 1", counts)
        self.assertEqual(seen, {str(i) for i in range(20, 40)})

    def test_denied_inventory_is_visible_and_never_creates_phantom_idle(self):
        team = self.team()
        with patch.object(live.subprocess, "run", side_effect=PermissionError("tmux unavailable")):
            lines, counts = team.frame(110, 40, {})
        self.assertIn("unavailable", "\n".join(lines).lower())
        self.assertNotIn("idle", counts)

    def test_builder_creates_one_team_pane(self):
        with tempfile.TemporaryDirectory(prefix="mb37_tmux_", dir="/private/tmp") as tmp:
            base = Path(tmp)
            calls = base / "calls"
            tmux = base / "tmux"
            tmux.write_text('#!/bin/bash\nprintf "%s\\n" "$*" >> "$MB37_CALLS"\ncase "$1" in\n'
                            ' has-session) exit 1;;\n list-sessions) printf "maestro28\\ncodexmb36\\n";;\n'
                            ' new-session|split-window) printf "%%1\\n";;\n list-windows) printf "team\\n";;\n esac\n')
            tmux.chmod(0o700)
            env = dict(os.environ, PATH=str(base) + ":/usr/bin:/bin", LEAD="maestro28", TEAMDASH_NO_ATTACH="1", MB37_CALLS=str(calls))
            proc = subprocess.run(["/bin/bash", str(ROOT / "code/apps/dashboard/team_dashboard.sh")], env=env, capture_output=True, text=True, timeout=20)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            commands = calls.read_text().splitlines()
            first = next(c for c in commands if c.startswith("new-session "))
            self.assertIn("dashboard_team.py", first)
            self.assertFalse(any(c.startswith("split-window ") for c in commands), commands)

    def test_bar_uses_the_rendered_roster_counts(self):
        with tempfile.TemporaryDirectory(prefix="mb37_bar_", dir="/private/tmp") as tmp:
            base = Path(tmp)
            for name, body in (("python3", 'printf "GPU fixture idle\\n"'),
                               ("tmux", 'case "$1" in show-options) printf "working 2 · asking 1 · active 0 · idle 3\\n";; list-panes) printf "IDLE\\nIDLE\\nIDLE\\nIDLE\\nIDLE\\n";; esac')):
                path = base / name
                path.write_text("#!/bin/bash\n" + body + "\n")
                path.chmod(0o700)
            proc = subprocess.run(["/bin/bash", str(ROOT / "code/apps/dashboard/dashboard_bar.sh")], env=dict(os.environ, PATH=str(base) + ":/usr/bin:/bin"), capture_output=True, text=True, timeout=10)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("working 2", proc.stdout)
            self.assertIn("idle 3", proc.stdout)
            self.assertNotIn("idle 5", proc.stdout)


if __name__ == "__main__":
    unittest.main()
