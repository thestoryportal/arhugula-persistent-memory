"""Q1 criteria, fixtures only: no real tmux, process inventory, model or .venv."""
import ast
import copy
import dataclasses
import datetime as dt
import importlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
RECEIPTS = ROOT / "results/dashboard_queue_build_20261011T014430Z"
sys.path.insert(0, str(TOOLS))
NOW = dt.datetime(2026, 10, 10, 19, 47, tzinfo=dt.timezone(dt.timedelta(hours=-6)))


def item(**changes):
    value = {"id": "builder", "title": "Make the work list easier to read",
             "summary": "Show what is happening and what needs your attention. This helps us choose the next step.",
             "state": "running", "who": "The dashboard builder", "session": "codexbuild",
             "started": "2026-10-11T00:27:00Z",
             "estimate": {"low_min": 37, "high_min": 67, "set": "2026-10-11T01:40:00Z"},
             "depends_on": [], "blocked_by": [], "needs_from_you": [], "notes": []}
    value.update(changes)
    return value


def source(items=None, edited="2026-10-11T01:40:00Z"):
    return {"work_queue": {"edited": edited, "items": [item()] if items is None else items}}


def cells(line):
    line = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", line)
    return sum(0 if unicodedata.combining(ch) else
               2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in line)


def flat(text):
    return " ".join(text.split())


class QueueCriteria(unittest.TestCase):
    def module(self):
        self.assertTrue((TOOLS / "dashboard_queue.py").is_file(), "Q1 queue implementation is absent")
        return importlib.import_module("dashboard_queue")

    def parsed(self, q, items=None, edited="2026-10-11T01:40:00Z"):
        return q.parse_queue(json.dumps(source(items, edited)))

    def active(self, q):
        return q.Live({"codexbuild": q.SessionLive(q.Observed.BUSY, 59)})

    def test_01_parse_typed_items_and_show_each_bad_field(self):
        """A dropped item, coercion or default must fail this criterion."""
        q = self.module()
        parsed = self.parsed(q)
        self.assertTrue(dataclasses.is_dataclass(parsed))
        self.assertTrue(dataclasses.is_dataclass(parsed.items[0]))
        self.assertEqual(parsed.items[0].state.value, "running")
        self.assertEqual(parsed.items[0].depends_on, ())
        round_trip = json.dumps({"work_queue": dataclasses.asdict(parsed)}, default=lambda v: v.isoformat())
        self.assertEqual(q.parse_queue(round_trip), parsed)
        self.assertEqual(self.parsed(q, []).items, ())
        failures = []
        for field in item():
            value = item()
            del value[field]
            failures.append((field, source([value])))
        for field, wrong in (("id", 8), ("title", []), ("summary", None), ("state", "done"),
                             ("who", False), ("session", 8), ("started", "yesterday"),
                             ("estimate", []), ("depends_on", "builder"), ("blocked_by", [8]),
                             ("needs_from_you", [None]), ("notes", {})):
            failures.append((field, source([item(**{field: wrong})])))
        failures += [("id", source([item(), item()])),
                     ("depends_on", source([item(depends_on=["not-present"])]))]
        for field, wrong in (("low_min", True), ("high_min", "60"), ("set", "2026-10-11T01:40:00")):
            estimate = dict(item()["estimate"], **{field: wrong})
            failures.append(("estimate." + field, source([item(estimate=estimate)])))
        for field, raw in failures:
            with self.subTest(field=field, raw=raw):
                with self.assertRaises(q.QueueError) as caught:
                    q.parse_queue(json.dumps(raw))
                self.assertIn("item ", str(caught.exception))
                self.assertIn(field, str(caught.exception))
                shown = q.render(q.QueueProblem(str(caught.exception)), q.Live(), NOW, 100)
                self.assertIn("Queue could not be read", shown)
                self.assertIn(field, flat(shown))
        for field, raw in (("work_queue", {"work_queue": []}),
                           ("edited", {"work_queue": {"items": []}}),
                           ("items", {"work_queue": {"edited": "2026-10-11T01:40:00Z", "items": {}}})):
            with self.subTest(field=field):
                with self.assertRaises(q.QueueError) as caught:
                    q.parse_queue(json.dumps(raw))
                self.assertIn(field, str(caught.exception))

    def test_02_renderer_is_pure_and_live_is_a_session_mapping(self):
        """Clock, file or tmux access inside rendering must fail."""
        q = self.module()
        queue, live = self.parsed(q), self.active(q)
        before = copy.deepcopy((queue, live))
        self.assertEqual(live["codexbuild"].context_left, 59)
        with mock.patch.object(Path, "read_text", side_effect=AssertionError("renderer read a file")), \
             mock.patch.object(q.subprocess, "run", side_effect=AssertionError("renderer ran a command")), \
             mock.patch.object(q, "local_now", side_effect=AssertionError("renderer read the clock")), \
             mock.patch.object(q.time, "time", side_effect=AssertionError("renderer read the clock")), \
             mock.patch.object(q.time, "sleep", side_effect=AssertionError("renderer slept")):
            first = q.render(queue, live, NOW, 100)
            second = q.render(queue, live, NOW, 100)
        self.assertIsInstance(first, str)
        self.assertEqual(first, second)
        self.assertEqual((queue, live), before)
        self.assertNotIn("\x1b", first)

    def test_03_display_width_word_wrap_and_long_word_hanging_indent(self):
        """Overflow, lost characters or missing continuation indentation must fail."""
        q = self.module()
        summary = "A long word " + "x" * 190 + " and wide text " + "界" * 45 + " cafe\u0301."
        queue = self.parsed(q, [item(summary=summary, notes=["n" * 240])])
        for width in (40, 50, 60, 80, 100, 160):
            with self.subTest(width=width):
                shown = q.render(queue, self.active(q), NOW, width)
                self.assertTrue(all(cells(line) <= width for line in shown.splitlines()), shown)
                body = shown.split("  Summary: ", 1)[1].split("  Time: ", 1)[0].rstrip()
                self.assertEqual(re.sub(r"\s+", "", body), re.sub(r"\s+", "", summary))
                self.assertTrue(all(line.startswith(" " * 11) for line in body.splitlines()[1:]))
        ordinary = self.parsed(q, [item(summary="one two three four five six seven eight nine ten eleven twelve")])
        body = q.render(ordinary, self.active(q), NOW, 40).split("  Summary: ", 1)[1].split("  Time: ", 1)[0]
        self.assertEqual(body.split(), ordinary.items[0].summary.split())
        dirty = self.parsed(q, [item(notes=["bad\x1b[31m text\r\nwith\tcontrols"])])
        self.assertNotIn("\x1b", q.render(dirty, self.active(q), NOW, 40))

    def test_04_ordered_cards_header_attention_and_dependency_titles(self):
        """Reordering, missing fields, empty labels or dependency ids must fail."""
        q = self.module()
        items = [item(notes=["Allow room on disk"]),
                 item(id="choice", title="Choose the next study", state="needs_you", session=None,
                      started=None, estimate=None, needs_from_you=["Choose the smaller study"]),
                 item(id="review", title="Check the result", state="in_review", session=None),
                 item(id="next", title="Try the next idea", state="ready", session=None,
                      depends_on=["builder"]),
                 item(id="wait", title="Save the records", state="blocked", session=None,
                      blocked_by=["The drive is full"])]
        shown = q.render(self.parsed(q, items), self.active(q), NOW, 160)
        header = shown.split("Running now (detected live)", 1)[0]
        for label in ("RUNNING 1", "NEEDS YOU 1", "IN REVIEW 1", "READY 1", "BLOCKED 1",
                      "queue edited 7 min ago", "7:47 PM", "Needs you: Choose the next study"):
            self.assertIn(label, header)
        positions = [shown.index("%d. %s" % (number, value["title"])) for number, value in enumerate(items, 1)]
        self.assertEqual(positions, sorted(positions))
        card = shown[positions[0]:positions[1]]
        fields = ["1. Make", "[RUNNING]", "Who:", "Summary:", "Time:", "Live:", "Note:"]
        self.assertEqual([card.index(v) for v in fields], sorted(card.index(v) for v in fields))
        self.assertNotIn("Waits for:", card)
        self.assertNotIn("Blocked by:", card)
        self.assertNotIn("Needs from you:", card)
        self.assertIn("Waits for: Make the work list easier to read", shown)
        self.assertNotIn("Waits for: builder", shown)
        self.assertIn("Blocked by: The drive is full", shown)
        self.assertIn("Needs from you: Choose the smaller study", shown)
        self.assertIn("\n\n2. ", shown)

    def test_05_elapsed_countdown_overrun_null_and_local_clock(self):
        """Frozen countdowns, UTC clocks or overrun arithmetic errors must fail."""
        q = self.module()
        queue, live = self.parsed(q), self.active(q)
        shown = q.render(queue, live, NOW, 160)
        self.assertIn("running for 1 h 20 min", shown)
        self.assertIn("about 30-60 min left (estimated 7:40 PM)", shown)
        self.assertIn("about 20-50 min left", q.render(queue, live, NOW + dt.timedelta(minutes=10), 160))
        self.assertIn("about 0-0 min left", q.render(queue, live, NOW + dt.timedelta(minutes=60), 160))
        self.assertIn("running 15 min past the estimate", q.render(queue, live, NOW + dt.timedelta(minutes=75), 160))
        null = self.parsed(q, [item(started=None, estimate=None)])
        self.assertIn("no estimate yet", q.render(null, live, NOW, 160))
        self.assertNotIn("running for", q.render(null, live, NOW, 160))
        local = NOW.astimezone(dt.timezone(dt.timedelta(hours=2)))
        self.assertIn("3:40 AM", q.render(queue, live, local, 160))
        self.assertNotIn("19:40", shown)
        self.assertNotIn("7:40:00", shown)

    def test_06_live_status_memory_and_queue_session_scope(self):
        """Misreported pane state, memory or scans of unrelated sessions must fail."""
        q = self.module()
        queue = self.parsed(q, [item(session="builder-only")])
        samples = [(q.Observed.BUSY, 59, "builder working · 59% memory left"),
                   (q.Observed.WAITING, None, "builder waiting on a test run"),
                   (q.Observed.IDLE, None, "builder idle"),
                   (q.Observed.MISSING, None, "session not found")]
        for status, memory, want in samples:
            with self.subTest(status=status):
                # Non-running state lets this test check missing without criterion 11's completion override.
                ready = self.parsed(q, [item(state="ready", session="builder-only")])
                shown = q.render(ready, q.Live({"builder-only": q.SessionLive(status, memory)}), NOW, 100)
                self.assertIn(want, shown)
        commands = []

        def run(args):
            commands.append(args)
            if "list-sessions" in args:
                return subprocess.CompletedProcess(args, 0, "builder-only\ndashboard\nother\n", "")
            if "capture-pane" in args:
                return subprocess.CompletedProcess(args, 0, "• Working (3s • esc to interrupt)\nContext 59% left\n", "")
            return subprocess.CompletedProcess(args, 0, "1 00:01 /usr/sbin/launchd\n", "")

        with tempfile.TemporaryDirectory() as directory:
            live = q.gather_live(queue, Path(directory), NOW, run=run)
        self.assertEqual(live["builder-only"].status, q.Observed.BUSY)
        self.assertEqual(live["builder-only"].context_left, 59)
        captures = [args for args in commands if "capture-pane" in args]
        self.assertEqual([a[a.index("-t") + 1] for a in captures], ["=builder-only"])

    def test_07_stale_queue_boundary_and_absent_key_plainly_visible(self):
        """Missing-key crashes or hidden staleness must fail."""
        q = self.module()
        stale = self.parsed(q, [], edited="2026-10-10T22:37:00Z")
        self.assertIn("queue not updated for 3 h 10 min — may be out of date", flat(q.render(stale, q.Live(), NOW, 40)))
        boundary = self.parsed(q, [], edited="2026-10-10T22:47:00Z")
        self.assertNotIn("may be out of date", q.render(boundary, q.Live(), NOW, 100))
        missing = q.parse_queue('{"other_program_data": {}}')
        self.assertIn("work_queue is not in program_state.json yet", flat(q.render(missing, q.Live(), NOW, 40)))

    def test_08_loop_reloads_recovers_midwrite_redraws_and_limits_color(self):
        """A crash, stale cached JSON, wrong interval or body color must fail."""
        q = self.module()
        waits, detected = [], []
        stream = io.StringIO()

        class EndLoop(Exception):
            pass

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "program_state.json"
            path.write_text('{"work_queue":')

            def sleep(seconds):
                waits.append(seconds)
                if len(waits) == 1:
                    path.write_text(json.dumps(source([item(title="Fresh second tick")])))
                elif len(waits) == 2:
                    path.write_text(json.dumps(source([item(title="Fresh third tick")])))
                else:
                    raise EndLoop()

            def detect(queue, root, now):
                detected.append(queue)
                return self.active(q)

            with self.assertRaises(EndLoop):
                q.run_loop(path, Path(directory), stream=stream, sleep=sleep,
                           clock=lambda: NOW, width=lambda: 40, detect=detect)
        shown = stream.getvalue()
        self.assertEqual(waits, [5, 5, 5])
        self.assertEqual(len(detected), 3)
        self.assertIn("Queue could not be read", flat(shown))
        self.assertIn("JSON", shown)
        self.assertIn("Fresh second tick", shown)
        self.assertIn("Fresh third tick", shown)
        self.assertEqual(shown.count("\x1b[2J"), 3)
        self.assertNotRegex(shown, r"\x1b\[[0-9;]*m")
        plain = q.render(self.parsed(q), self.active(q), NOW, 100)
        self.assertEqual(q.colorize(plain, False), plain)
        colored = q.colorize(plain, True)
        self.assertEqual(re.sub(r"\x1b\[[0-9;]*m", "", colored), plain)
        self.assertRegex(colored, r"\x1b\[[0-9;]*m")
        for line in colored.splitlines():
            if "\x1b" in line:
                clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
                self.assertTrue(clean.startswith(("Work queue", "RUNNING", "  ")) or "[RUNNING]" in clean)
                self.assertNotIn("Summary:", clean)
                self.assertNotIn("Live:", clean)
                self.assertNotIn("Who:", clean)
        tree = ast.parse((TOOLS / "dashboard_queue.py").read_text(), feature_version=(3, 9))
        imports = {node.names[0].name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import)}
        allowed = {"argparse", "collections", "datetime", "enum", "json", "os", "re", "shlex",
                   "shutil", "subprocess", "sys", "time", "unicodedata", "dashboard_live"}
        self.assertLessEqual(imports, allowed)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                self.assertIn(node.module, {"dataclasses", "enum", "pathlib", "typing", "dashboard_live"})
        gate = importlib.import_module("c10w_p2_gate")
        inventory = "123 /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python %s\n" % (TOOLS / "dashboard_queue.py")
        self.assertEqual(gate.blocking_processes(inventory, -1), [])

    def test_09_launcher_idempotent_python_path_and_team_registration(self):
        """A real duplicate window, wrong interpreter or missing integration must fail."""
        launcher = TOOLS / "dashboard_queue_tab.sh"
        self.assertTrue(launcher.is_file(), "Q1 queue launcher is absent")
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            stub = folder / "tmux"
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$Q1_TEST_LOG"\n'
                            'case "$1" in\nlist-windows) printf "%s\\n" "$Q1_TEST_WINDOWS"; exit "${Q1_TEST_RC:-0}";;\n'
                            'new-window) exit 0;;\n*) exit 98;;\nesac\n')
            stub.chmod(0o755)
            log = folder / "commands.txt"
            env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ["PATH"],
                       LLMDB_ROOT=str(ROOT), Q1_TEST_LOG=str(log), Q1_TEST_WINDOWS="team\nstorage")
            first = subprocess.run(["bash", str(launcher), "q1-fixture"], env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            calls = log.read_text().splitlines()
            self.assertEqual(len(calls), 2)
            self.assertIn("-n queue", calls[1])
            self.assertIn("/usr/bin/python3 '%s/dashboard_queue.py'" % TOOLS, calls[1])
            log.write_text("")
            env["Q1_TEST_WINDOWS"] = "team\nstorage\nqueue"
            again = subprocess.run(["bash", str(launcher), "q1-fixture"], env=env, capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(len(log.read_text().splitlines()), 1)
            env["Q1_TEST_RC"] = "3"
            failed = subprocess.run(["bash", str(launcher), "q1-fixture"], env=env, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("no 'q1-fixture' session", failed.stderr)
        team = (TOOLS / "team_dashboard.sh").read_text()
        self.assertEqual(team.count('bash "$T/dashboard_queue_tab.sh" "$NEW"'), 1)
        self.assertGreater(team.index('bash "$T/dashboard_queue_tab.sh"'), team.index('bash "$T/dashboard_storage_tab.sh"'))
        self.assertIn("8 queue", "\n".join(team.splitlines()[4:6]))
        self.assertIn("1-8", "\n".join(team.splitlines()[4:6]))

    def test_10_host_runner_records_every_step_and_owns_only_q1check_socket(self):
        """Missing host evidence, default-server mutation or a hidden exit must fail."""
        runner = RECEIPTS / "run_host_checks.sh"
        self.assertTrue(runner.is_file(), "Q1 host runner is absent")
        syntax = subprocess.run(["bash", "-n", str(runner)], capture_output=True, text=True)
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        text = runner.read_text()
        for receipt in ("tests", "render_40", "render_100", "tmux_start", "tmux_capture", "gpu_check", "tmux_cleanup"):
            self.assertIn(receipt + ".exit", text)
        self.assertIn("tools/test_dashboard_queue.py", text)
        self.assertIn("docs/program_state.json", text)
        self.assertIn("--once 40", text)
        self.assertIn("--once 100", text)
        self.assertIn("tmux -L q1check new-session", text)
        self.assertIn("tmux -L q1check capture-pane", text)
        self.assertIn("tmux -L q1check kill-server", text)
        self.assertIn("import c10w_p2_gate as g; print(g.check_gpu())", text)
        self.assertLess(text.index("tmux -L q1check new-session"), text.index("import c10w_p2_gate as g"))
        self.assertLess(text.index("import c10w_p2_gate as g"), text.index("tmux -L q1check capture-pane"))
        self.assertIn("sleep 2", text)
        self.assertIn("sleep 6", text)
        self.assertIn("owned", text)
        self.assertIn("no server running", text)
        for line in text.splitlines():
            if line.lstrip().startswith("tmux "):
                self.assertTrue(line.lstrip().startswith("tmux -L q1check "), line)
        self.assertNotIn("kill-session", text)
        self.assertNotIn(".venv", text)

    def test_11_live_detection_unlisted_reviewers_experiment_and_finished_override(self):
        """Hand-written lag, stale READY, hidden workers or unavailable-as-idle must fail."""
        q = self.module()
        commands = []
        screens = {"codexbuild": "• Working (3s • esc to interrupt)\nContext 59% left\n",
                   "codexextra": "• Waiting on a test run\nContext 70% left\n",
                   "codexdone": "• QUEUE TAB READY FOR MAESTRO RUN\n› \nContext 65% left\n",
                   "codexhandoff": "• Q1 HANDOFF\n› \nContext 39% left\n",
                   "codexidle": "• I have looked at the files.\n› \nContext 81% left\n"}

        def run(args):
            commands.append(args)
            if "list-sessions" in args:
                return subprocess.CompletedProcess(args, 0, "\n".join(screens) + "\ndashboard\nother\n", "")
            if "capture-pane" in args:
                name = args[args.index("-t") + 1].lstrip("=")
                return subprocess.CompletedProcess(args, 0, screens[name], "")
            inventory = ("321 07:00 /opt/homebrew/bin/codex exec --model gpt-6-astra -o '/tmp/review output.md' packet\n"
                         "322 01-00:03:00 /opt/homebrew/bin/codex exec --output-last-message=/tmp/long.md packet\n"
                         "323 05:00 /bin/sh -c 'codex exec -o /tmp/not-a-review.md packet'\n"
                         "324 10:00 /opt/homebrew/bin/codex app-server\n")
            return subprocess.CompletedProcess(args, 0, inventory, "")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runs = root / "results/mathlab_staging/runs"
            runs.mkdir(parents=True)
            for name, stamp, terminal in (("older-open", 1, False), ("newer-open", 2, False), ("newest-finished", 3, True)):
                folder = runs / name
                folder.mkdir()
                events = [{"type": "run_started"}, {"type": "run_finishing"}]
                if terminal:
                    events.append({"type": "run_finished"})
                (folder / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
                os.utime(folder, (stamp, stamp))
            queue = self.parsed(q, [item(), item(id="finished", title="Finished task", session="codexdone"),
                                     item(id="vanished", title="Former task", session="codexgone")])
            live = q.gather_live(queue, root, NOW, run=run)
            self.assertEqual(set(live), set(screens) | {"codexgone"})
            self.assertEqual(live["codexextra"].status, q.Observed.WAITING)
            self.assertEqual(live["codexidle"].status, q.Observed.IDLE)
            self.assertTrue(live["codexdone"].finished)
            self.assertTrue(live["codexhandoff"].finished)
            self.assertEqual(live.experiment, "newer-open")
            self.assertEqual(len(live.reviewers), 2)
            self.assertEqual(live.reviewers[0].output, "review output.md")
            self.assertEqual(live.reviewers[0].elapsed_seconds, 420)
            self.assertEqual(live.reviewers[1].elapsed_seconds, 86580)
            self.assertTrue(all(a[1:3] == ["-L", "default"] for a in commands if a[0] == "tmux"))
            ps_command = next(a for a in commands if a[0] == "/bin/ps")
            self.assertIn("pid=,etime=,command=", ps_command)
            shown = q.render(queue, live, NOW, 100)
            self.assertLess(shown.index("Running now (detected live)"), shown.index("1. Make"))
            self.assertIn("not yet described in the queue", flat(shown))
            self.assertIn("Astra review running for 7 min", shown)
            self.assertIn("review output.md", shown)
            self.assertIn("experiment run in progress", shown)
            self.assertIn("builder finished — waiting for MAESTRO", flat(shown))
            self.assertIn("[IN REVIEW]", shown[shown.index("2. Finished task"):shown.index("3. Former task")])
            for width in (40, 50, 60, 80, 100, 160):
                self.assertTrue(all(cells(line) <= width for line in q.render(queue, live, NOW, width).splitlines()))
            (runs / "newer-open/events.jsonl").write_text('{"type":"terminal"}\n')
            self.assertEqual(q.gather_live(queue, root, NOW, run=run).experiment, "older-open")
            (runs / "older-open/events.jsonl").write_text('{"type":')
            broken = q.gather_live(queue, root, NOW, run=run)
            self.assertTrue(broken.errors)
            self.assertIn("events.jsonl", flat(q.render(queue, broken, NOW, 40)))
            def denied(args):
                raise PermissionError("fixture operation not permitted")
            unavailable = q.gather_live(queue, root, NOW, run=denied)
            self.assertEqual(unavailable["codexbuild"].status, q.Observed.UNAVAILABLE)
            self.assertIn("unavailable", flat(q.render(queue, unavailable, NOW, 40)).lower())
            self.assertNotIn("builder finished", q.render(self.parsed(q), unavailable, NOW, 100))
        # Older finish tokens and quoted user requests cannot terminate current work.
        for pane in ("• READY\n• Working (3s • esc to interrupt)\nContext 52% left",
                     "• The next step is being prepared.\n› Please return READY when done\nContext 80% left"):
            self.assertFalse(q.observe_pane(pane).finished)
        self.assertTrue(q.observe_pane("• QUEUE TAB READY FOR\n  MAESTRO RUN\n›\nContext 50% left").finished)


if __name__ == "__main__":
    unittest.main(verbosity=2)
