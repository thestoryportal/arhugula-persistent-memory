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
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
RECEIPTS = ROOT / "_archive/projects/dashboard/dashboard_queue_build_20261011T014430Z"
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
        self.assertIn("about 30-60 min left (estimate made 7:40 PM)", shown)
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
            return subprocess.CompletedProcess(args, 0, "1 1 00:01 /usr/sbin/launchd\n", "")

        with tempfile.TemporaryDirectory() as directory:
            live = q.gather_live(queue, Path(directory), NOW, run=run)
        self.assertEqual(live["builder-only"].status, q.Observed.BUSY)
        self.assertEqual(live["builder-only"].context_left, 59)
        captures = [args for args in commands if "capture-pane" in args]
        self.assertEqual([a[a.index("-t") + 1] for a in captures], ["=builder-only:"])

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
        self.assertIn("code/apps/dashboard/test_dashboard_queue.py", text)
        self.assertIn("program/program_state.json", text)
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
                name = args[args.index("-t") + 1].strip("=:")
                return subprocess.CompletedProcess(args, 0, screens[name], "")
            inventory = ("321 1 07:00 /opt/homebrew/bin/codex exec --model gpt-6-astra -o '/tmp/review output.md' packet\n"
                         "322 1 01-00:03:00 /opt/homebrew/bin/codex exec --output-last-message=/tmp/long.md packet\n"
                         "323 1 05:00 /bin/sh -c 'codex exec -o /tmp/not-a-review.md packet'\n"
                         "324 1 10:00 /opt/homebrew/bin/codex app-server\n")
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
                event_stamp = NOW.timestamp() - (3 - stamp) * 60
                os.utime(folder / "events.jsonl", (event_stamp, event_stamp))
                os.utime(folder, (stamp, stamp))
            queue = self.parsed(q, [item(), item(id="finished", title="Finished task", session="codexdone"),
                                     item(id="vanished", title="Former task", session="codexgone")])
            live = q.gather_live(queue, root, NOW, run=run)
            self.assertEqual(set(live), set(screens) | {"codexgone"})
            self.assertEqual(live["codexextra"].status, q.Observed.WAITING)
            self.assertEqual(live["codexidle"].status, q.Observed.IDLE)
            self.assertTrue(live["codexdone"].finished)
            self.assertTrue(live["codexhandoff"].finished)
            self.assertEqual(live.experiment.name, "newer-open")
            self.assertEqual(len(live.reviewers), 2)
            self.assertEqual(live.reviewers[0].output, "review output.md")
            self.assertEqual(live.reviewers[0].elapsed_seconds, 420)
            self.assertEqual(live.reviewers[1].elapsed_seconds, 86580)
            self.assertTrue(all(a[1:3] == ["-L", "default"] for a in commands if a[0] == "tmux"))
            ps_command = next(a for a in commands if a[0] == "/bin/ps")
            self.assertIn("pid=,ppid=,etime=,command=", ps_command)
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
            self.assertEqual(q.gather_live(queue, root, NOW, run=run).experiment.name, "older-open")
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

    def test_12_unrelated_process_prompt_quotes_cannot_hide_reviewers(self):
        """A shell's unbalanced prompt text must not erase a genuine review."""
        q = self.module()
        inventory = ("1 1 00:01 /usr/sbin/launchd\n"
                     "2 1 00:02 /bin/zsh -c Please don't parse my arbitrary prompt as shell source\n"
                     "3 1 03:00 /opt/homebrew/bin/codex exec -o /tmp/check.md packet\n")
        try:
            reviews = q.reviewer_processes(inventory)
        except ValueError as error:
            self.fail("Unrelated process text hid the reviewer: " + str(error))
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].output, "check.md")
        self.assertEqual(reviews[0].elapsed_seconds, 180)

    def test_13_badge_words_in_body_are_never_colored(self):
        """Only the actual state badge may get color after the header."""
        q = self.module()
        queue = self.parsed(q, [item(summary="The old note says [RUNNING].", notes=["The label was [BLOCKED]."])])
        plain = q.render(queue, self.active(q), NOW, 100)
        shown = q.colorize(plain, True)
        self.assertRegex(shown, r"\x1b\[[0-9;]*m\[RUNNING\]")
        for line in shown.splitlines():
            if "Summary:" in line or "Note:" in line:
                self.assertNotIn("\x1b", line)

    def test_14_tab_reads_its_own_worktree_despite_inherited_main_root(self):
        """The known main-checkout environment must not redirect this tab's queue."""
        q = self.module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "docs").mkdir()
            (root / "program/program_state.json").write_text(json.dumps(source([item(title="The selected worktree queue")])))
            other = root / "other"
            (other / "docs").mkdir(parents=True)
            (other / "program/program_state.json").write_text(json.dumps(source([item(title="An unrelated main checkout")])))
            output = io.StringIO()
            with mock.patch.object(q, "__file__", str(root / "code/apps/dashboard/dashboard_queue.py")), \
                 mock.patch.dict(os.environ, {"LLMDB_ROOT": str(other)}), \
                 mock.patch.object(sys, "argv", ["dashboard_queue.py", "--once", "100"]), \
                 mock.patch.object(q, "gather_live", return_value=self.active(q)), \
                 mock.patch.object(q, "local_now", return_value=NOW), \
                 mock.patch.object(sys, "stdout", output):
                q.main()
            self.assertIn("The selected worktree queue", output.getvalue())
            self.assertNotIn("An unrelated main checkout", output.getvalue())

    def test_15_empty_successful_tmux_inventory_is_unavailable_not_finished(self):
        """An empty observation layer cannot establish a missing builder."""
        q = self.module()
        def run(args):
            out = "" if args[0] == "tmux" else "1 1 00:01 /usr/sbin/launchd\n"
            return subprocess.CompletedProcess(args, 0, out, "")
        with tempfile.TemporaryDirectory() as directory:
            queue = self.parsed(q)
            live = q.gather_live(queue, Path(directory), NOW, run=run)
        self.assertEqual(live["codexbuild"].status, q.Observed.UNAVAILABLE)
        self.assertNotIn("builder finished", q.render(queue, live, NOW, 100))


class Q2Regressions(unittest.TestCase):
    module = QueueCriteria.module
    parsed = QueueCriteria.parsed
    active = QueueCriteria.active
    def test_q2_01_exact_tmux_session_targets_work(self):
        q = self.module()
        def run(args):
            if 'list-sessions' in args:
                return subprocess.CompletedProcess(args, 0, 'codexbuild\ncodexextra\n', '')
            if 'capture-pane' in args:
                target = args[args.index('-t') + 1]
                good = target in ('=codexbuild:', '=codexextra:')
                return subprocess.CompletedProcess(args, 0 if good else 1,
                    '• Working (3s • esc to interrupt)\nContext 59% left\n' if good else '',
                    '' if good else "can't find pane: " + target)
            return subprocess.CompletedProcess(args, 0, '1 1 00:01 /usr/sbin/launchd\n', '')
        with tempfile.TemporaryDirectory() as directory:
            live = q.gather_live(self.parsed(q), Path(directory), NOW, run=run)
        self.assertEqual(live['codexbuild'].status, q.Observed.BUSY)
        self.assertEqual(live['codexextra'].status, q.Observed.BUSY)
        self.assertFalse(live.errors)

    def test_q2_02_failed_session_reason_is_shown_once(self):
        q = self.module()
        def run(args):
            if 'list-sessions' in args:
                return subprocess.CompletedProcess(args, 0, 'codexbuild\ncodexextra\n', '')
            if 'capture-pane' in args:
                name = args[args.index('-t') + 1].strip('=:')
                return subprocess.CompletedProcess(args, 1, '', 'capture denied for ' + name)
            return subprocess.CompletedProcess(args, 0, '1 1 00:01 /usr/sbin/launchd\n', '')
        with tempfile.TemporaryDirectory() as directory:
            queue = self.parsed(q)
            live = q.gather_live(queue, Path(directory), NOW, run=run)
        for width in (40, 100):
            shown = flat(q.render(queue, live, NOW, width))
            self.assertEqual(shown.count('live session check unavailable'), 2, shown)
            for name in ('codexbuild', 'codexextra'):
                self.assertEqual(shown.count('capture denied for ' + name), 1, shown)
                self.assertIn('live session check unavailable for ' + name, shown)
                self.assertEqual(live[name].status, q.Observed.UNAVAILABLE)
            self.assertNotIn('builder finished', shown)

    def q2_events(self, root, name, age, terminal=False):
        folder = root / 'results/mathlab_staging/runs' / name
        folder.mkdir(parents=True)
        events = [{'type': 'run_started'}]
        if terminal:
            events.append({'type': 'run_finished'})
        path = folder / 'events.jsonl'
        path.write_text(''.join(json.dumps(e) + '\n' for e in events))
        stamp = NOW.timestamp() - age
        os.utime(path, (stamp, stamp))
        return folder

    def q2_live(self, q, root, inventory='1 1 00:01 /usr/sbin/launchd\n'):
        def run(args):
            if args[0] == 'tmux':
                return subprocess.CompletedProcess(args, 1, '', 'no server running on /tmp/q2-fixture')
            return subprocess.CompletedProcess(args, 0, inventory, '')
        return q.gather_live(q.parse_queue(json.dumps(source([]))), root, NOW, run=run)

    def test_q2_03_old_unfinished_run_is_not_in_progress(self):
        q = self.module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.q2_events(root, 'new1_20261010T053945.884468Z', 24 * 3600)
            live = self.q2_live(q, root)
        self.assertIsNone(live.experiment)
        self.assertNotIn('experiment run in progress', q.render(self.parsed(q), live, NOW, 100))

    def test_q2_04_event_freshness_boundary_and_terminal(self):
        q = self.module()
        for age, terminal, expected in ((0, False, True), (599, False, True),
                                       (600, False, True), (601, False, False),
                                       (0, True, False), (600, True, False)):
            with self.subTest(age=age, terminal=terminal), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.q2_events(root, 'new1-fresh', age, terminal)
                live = self.q2_live(q, root)
                shown = flat(q.render(self.parsed(q), live, NOW, 100))
                self.assertEqual(live.experiment is not None, expected, shown)
                if expected:
                    self.assertIn('events updated %d min ago' % (age // 60), shown)

    def test_q2_05_shared_detector_process_binding(self):
        q = self.module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = self.q2_events(root, 'mathlab-live', 3600)
            command = '222 1 00:40 /usr/bin/python3 %s/mathlab_cpu_runner.py code/apps/mathlab/m2_solve_repro.py --run-dir %s\n' % (TOOLS, folder)
            live = self.q2_live(q, root, command)
            self.assertIsNotNone(live.experiment)
            self.assertIn('mathlab-live', flat(q.render(self.parsed(q), live, NOW, 100)))
            for inventory in ('1 1 00:01 /usr/sbin/launchd\n',
                              command.replace(str(folder), str(root / 'a-different-run')),
                              '222 1 00:40 /bin/zsh -c "' + command.split(None, 3)[3].strip() + '"\n'):
                with self.subTest(inventory=inventory):
                    self.assertIsNone(self.q2_live(q, root, inventory).experiment)
            (folder / 'events.jsonl').write_text('{"type":"run_finished"}\n')
            self.assertIsNone(self.q2_live(q, root, command).experiment)

    def test_q2_06_estimate_timestamp_is_when_estimate_was_made(self):
        q = self.module()
        shown = flat(q.render(self.parsed(q), self.active(q), NOW, 160))
        self.assertIn('about 30-60 min left (estimate made 7:40 PM)', shown)
        self.assertNotIn('(estimated ', shown)

    def q2_host_fixture(self, capture, inventory='1 1 00:01 /usr/sbin/launchd\n'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = root / '_archive/projects/dashboard/dashboard_queue_build_20261011T014430Z'
            receipt.mkdir(parents=True)
            (root / 'tools').mkdir()
            (root / 'code/apps/dashboard/test_dashboard_queue.py').write_text('print("fixture tests pass")\n')
            (root / 'code/apps/dashboard/dashboard_queue.py').write_text('print("fixture queue render")\n')
            (root / 'code/lab/runners/c10w_p2_gate.py').write_text('def check_gpu(): return {"blocking_processes": []}\n')
            # The checker uses the real shared detector against the fixture snapshot.
            (root / 'code/apps/dashboard/dashboard_live.py').write_text((TOOLS / 'dashboard_live.py').read_text())
            runner = receipt / 'run_host_checks.sh'
            runner.write_text((RECEIPTS / runner.name).read_text())
            checker = RECEIPTS / 'check_q2_host_live.py'
            if checker.exists():
                (receipt / checker.name).write_text(checker.read_text())
            attempt1 = receipt / 'host_attempt1'
            attempt1.mkdir()
            sentinel = attempt1 / 'unchanged.txt'
            sentinel.write_text('attempt one is locked\n')
            wrapper = r"""
function tmux() {
  printf '%s\n' "$*" >> "$Q2_COMMANDS"
  if [ "$1" != -L ]; then return 98; fi
  local server=$2 action=$3
  if [ "$server" = default ]; then
    if [ "$action" = list-sessions ]; then printf '%s\n' codexbuild; return 0; fi
    return 99
  fi
  if [ "$server" != q1check ]; then return 97; fi
  case "$action" in
    list-sessions) printf '%s\n' 'no server running on /tmp/q2-fixture'; return 1;;
    new-session|kill-server) return 0;;
    capture-pane) printf '%s\n' "$Q2_CAPTURE"; return 0;;
    list-panes) printf '%s\n' '0 424242 /usr/bin/python3 code/apps/dashboard/dashboard_queue.py'; return 0;;
    *) return 96;;
  esac
}
function /bin/ps() { printf '%s' "$Q2_INVENTORY"; }
function sleep() { return 0; }
source "$1"
"""
            commands = root / 'commands.txt'
            env = dict(os.environ, Q2_CAPTURE=capture, Q2_INVENTORY=inventory,
                       Q2_COMMANDS=str(commands), PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run(['bash', '-c', wrapper, str(runner), str(runner)],
                                    env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(sentinel.read_text(), 'attempt one is locked\n')
            called = commands.read_text().splitlines()
            self.assertTrue(all(line == '-L default list-sessions -F #{session_name}'
                                for line in called if line.startswith('-L default ')), called)
            self.assertEqual(sum(line == '-L q1check kill-server' for line in called), 1, called)
            outputs = {str(p.relative_to(receipt)): p.read_text() for p in receipt.rglob('*.txt')}
            return result, outputs

    def test_q2_07_host_outputs_go_only_to_attempt_two(self):
        result, outputs = self.q2_host_fixture('A healthy queue tab')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('host_attempt2/tmux_capture.txt', outputs)
        self.assertIn('host_attempt2/default_sessions.txt', outputs)
        self.assertIn('host_attempt2/experiment_inventory.txt', outputs)
        self.assertIn('host_attempt2/queue_live_checks.txt', outputs)
        self.assertNotIn('tmux_capture.txt', outputs)

    def test_q2_08_host_rejects_unavailable_existing_session(self):
        result, outputs = self.q2_host_fixture(
            'Running now (detected live)\n  Live: live session check unavailable for codexbuild: capture denied')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('codexbuild', outputs['host_attempt2/queue_live_checks.txt'])

    def test_q2_09_host_rejects_nonlive_experiment(self):
        result, outputs = self.q2_host_fixture(
            'experiment run in progress: stale-new1 (events updated 600 min ago); not yet described in the queue')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('stale-new1', outputs['host_attempt2/queue_live_checks.txt'])



class Q3Regressions(unittest.TestCase):
    module = QueueCriteria.module
    parsed = QueueCriteria.parsed
    active = QueueCriteria.active

    def sized(self, q, queue, live, width, height):
        # Execute Q2's renderer too: RED must show oversized output, not TypeError.
        if 'height' in q.render.__code__.co_varnames:
            return q.render(queue, live, NOW, width, height=height)
        return q.render(queue, live, NOW, width)

    def crowded(self, count=50):
        return [item(id='task%d' % n, title='Task %d · — café' % n,
                     state='blocked', session=None, started=None, estimate=None,
                     summary='A long explanation ' * 120, notes=['Detailed note ' * 25])
                for n in range(1, count + 1)]

    def test_q3_01_frames_fit_real_phone_and_desktop_heights(self):
        q = self.module()
        for width, height in ((40, 30), (40, 45), (100, 45)):
            with self.subTest(width=width, height=height):
                shown = self.sized(q, self.parsed(q, self.crowded()), q.Live(), width, height)
                self.assertLessEqual(len(shown.splitlines()), height)
                self.assertTrue(all(len(line) <= width and cells(line) <= width
                                    for line in shown.splitlines()))
                self.assertTrue(shown.splitlines()[0].startswith('Work queue'))

    def test_q3_02_header_attention_and_stale_warning_survive_pressure(self):
        q = self.module()
        needs = [item(id='decision%d' % n, title='Choose the next study %d with all its details intact' % n,
                      state='needs_you', session=None, started=None, estimate=None)
                 for n in (1, 2)]
        queue = self.parsed(q, needs + self.crowded(), edited='2026-10-10T21:47:00Z')
        shown = self.sized(q, queue, q.Live(), 40, 30)
        self.assertLessEqual(len(shown.splitlines()), 30)
        top = flat(shown.split('Running now (detected live)', 1)[0])
        for value in ('Work queue · 7:47 PM', 'RUNNING 0', 'NEEDS YOU 2',
                      'IN REVIEW 0', 'READY 0', 'BLOCKED 50',
                      'queue not updated for 4 h 0 min — may be out of date'):
            self.assertIn(value, top)
        for value in needs:
            self.assertIn('Needs you: ' + value['title'], top)
        fresh = self.sized(q, self.parsed(q, needs + self.crowded()), q.Live(), 40, 30)
        self.assertIn('queue edited 7 min ago', flat(fresh))

    def test_q3_03_priority_cards_get_full_details_before_lower_states(self):
        q = self.module()
        values = [item(id='ready', title='Low priority first', state='ready', session=None,
                       summary='A low priority explanation ' * 120),
                  item(id='running', title='Active priority', summary='RUNNING detail marker',
                       session=None, started=None, estimate=None),
                  item(id='needs', title='Attention priority', state='needs_you', summary='NEEDS detail marker',
                       session=None, started=None, estimate=None, needs_from_you=['Choose A']),
                  item(id='review', title='Review priority', state='in_review', summary='REVIEW detail marker',
                       session=None, started=None, estimate=None)] + self.crowded(30)
        shown = self.sized(q, self.parsed(q, values), q.Live(), 100, 45)
        self.assertLessEqual(len(shown.splitlines()), 45)
        for detail in ('Summary: RUNNING detail marker', 'Summary: NEEDS detail marker',
                       'Summary: REVIEW detail marker', 'Needs from you: Choose A'):
            self.assertIn(detail, shown)
        # Numbers follow the order on screen, not the queue's stored order (operator, 2026-10-11).
        positions = [shown.index(label) for label in ('1. Active priority', '2. Attention priority',
                                                     '3. Review priority', '4. [READY] Low priority first')]
        self.assertEqual(positions, sorted(positions))
        # In roomy snapshots the original order and full cards stay available.
        unbounded = q.render(self.parsed(q, values), q.Live(), NOW, 100)
        self.assertLess(unbounded.index('1. Low priority first'), unbounded.index('2. Active priority'))

    def test_q3_04_compact_rows_and_exact_omitted_item_count(self):
        q = self.module()
        values = self.crowded()
        for width in (40, 100):
            shown = self.sized(q, self.parsed(q, values), q.Live(), width, 30)
            lines = shown.splitlines()
            self.assertLessEqual(len(lines), 30)
            rows = [line for line in lines if re.match(r'^\d+\. ', line)]
            self.assertGreater(len(rows), 0)
            for number, row in enumerate(rows, 1):
                self.assertEqual(row, ('%d. [BLOCKED] %s' % (number, values[number - 1]['title']))[:width])
            k = len(values) - len(rows)
            self.assertEqual(lines[-1], ('+%d more items (taller window shows more)' % k)[:width])
        # An exact fit uses the last row for the last item, not a +1 footer.
        queue = self.parsed(q, self.crowded(2))
        shown = self.sized(q, queue, q.Live(), 40, 30)
        self.assertNotIn('more items', shown)
        self.assertIn('2. [BLOCKED]', shown)

    def test_q3_05_compact_unicode_clips_characters_without_splitting_bytes(self):
        q = self.module()
        title = '· — café ' + '界e\u0301' * 30
        values = self.crowded(2)
        values[0]['title'] = title
        shown = self.sized(q, self.parsed(q, values), q.Live(), 40, 30)
        row = next(line for line in shown.splitlines() if line.startswith('1. '))
        self.assertTrue(row.startswith('1. [BLOCKED] · — café '), row)
        self.assertNotIn('\ufffd', row)
        self.assertLessEqual(len(row), 40)
        self.assertLessEqual(cells(row), 40)
        expected = '1. [BLOCKED] ' + title
        self.assertTrue(expected.startswith(row))
        self.assertGreater(len(row), len('1. [BLOCKED] · — café '))

    def test_q3_06_only_working_builders_are_running_idle_names_are_grouped(self):
        q = self.module()
        live = q.Live({'codexbusy': q.SessionLive(q.Observed.BUSY, 55),
                       'codexwaiting': q.SessionLive(q.Observed.WAITING, 65),
                       'codexmb39': q.SessionLive(q.Observed.IDLE, 60, True),
                       'codexmb40': q.SessionLive(q.Observed.IDLE, 70),
                       'codexgone': q.SessionLive(q.Observed.MISSING),
                       'codexunknown': q.SessionLive(q.Observed.UNAVAILABLE, reason='capture denied')})
        shown = self.sized(q, self.parsed(q, []), live, 40, 30)
        self.assertIn('Idle builder windows: codexmb39, codexmb40', flat(shown))
        running = shown.split('Running now (detected live)', 1)[1].split('Idle builder windows:', 1)[0]
        self.assertIn('codexbusy', running)
        self.assertIn('codexwaiting', running)
        for name in ('codexmb39', 'codexmb40', 'codexgone', 'codexunknown'):
            self.assertNotIn(name, running)
        self.assertIn('live session check unavailable for codexunknown: capture denied', flat(shown))
        self.assertLessEqual(len(shown.splitlines()), 30)

    def loop_frames(self, q, sizes):
        class EndLoop(Exception):
            pass
        stream = io.StringIO()
        waits = []
        def sleep(seconds):
            waits.append(seconds)
            if len(waits) == len(sizes):
                raise EndLoop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'program_state.json'
            path.write_text(json.dumps(source(self.crowded())))
            with mock.patch.object(q.shutil, 'get_terminal_size', side_effect=[os.terminal_size(s) for s in sizes]) as terminal:
                with self.assertRaises(EndLoop):
                    q.run_loop(path, Path(directory), stream=stream, sleep=sleep,
                               clock=lambda: NOW, detect=lambda *args: q.Live())
        self.assertEqual(waits, [5] * len(sizes))
        self.assertEqual(terminal.call_count, len(sizes))
        return stream.getvalue().split('\x1b[2J\x1b[H')[1:]

    def test_q3_07_live_loop_rereads_both_dimensions_after_resize(self):
        q = self.module()
        sizes = [(40, 30), (100, 45)]
        frames = self.loop_frames(q, sizes)
        self.assertEqual(len(frames), 2)
        for frame, (width, height) in zip(frames, sizes):
            self.assertLessEqual(len(frame.splitlines()), height)
            self.assertTrue(all(len(line) <= width and cells(line) <= width for line in frame.splitlines()))
            self.assertTrue(frame.startswith('Work queue'))
        self.assertGreater(len(frames[1].splitlines()), len(frames[0].splitlines()))

    def test_q3_08_redraw_does_not_scroll_when_last_row_is_used(self):
        q = self.module()
        frame = self.loop_frames(q, [(40, 30)])[0]
        self.assertFalse(frame.endswith('\n'), 'A newline on the last row scrolls the header away')
        self.assertEqual(len(frame.splitlines()), 30)

    def test_q3_09_once_accepts_width_height_and_legacy_width(self):
        q = self.module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tools').mkdir()
            (root / 'docs').mkdir()
            (root / 'program/program_state.json').write_text(json.dumps(source(self.crowded())))
            for args, width, height in ((['40', '30'], 40, 30), (['100', '45'], 100, 45), (['40'], 40, 30)):
                with self.subTest(args=args):
                    out = io.StringIO()
                    with mock.patch.object(q, '__file__', str(root / 'code/apps/dashboard/dashboard_queue.py')), \
                         mock.patch.object(sys, 'argv', ['dashboard_queue.py', '--once'] + args), \
                         mock.patch.object(q, 'gather_live', return_value=q.Live()), \
                         mock.patch.object(q, 'local_now', return_value=NOW), \
                         mock.patch.object(q.shutil, 'get_terminal_size', return_value=os.terminal_size((width, height))), \
                         mock.patch.object(sys, 'stdout', out):
                        try:
                            q.main()
                        except SystemExit as error:
                            self.fail('--once W H must render successfully: ' + str(error))
                    self.assertLessEqual(len(out.getvalue().splitlines()), height)
                    self.assertTrue(all(len(line) <= width and cells(line) <= width for line in out.getvalue().splitlines()))

    def test_q3_10_missing_problem_and_empty_queue_frames_are_bounded(self):
        q = self.module()
        live = q.Live({'codex%d' % n: q.SessionLive(q.Observed.BUSY, 50) for n in range(30)},
                      errors=('Process inventory is unavailable ' * 30,))
        for queue, message in ((q.QueueMissing(), 'work_queue is not in program_state.json yet'),
                               (q.QueueProblem('JSON was incomplete'), 'Queue could not be read: JSON was incomplete'),
                               (self.parsed(q, []), 'The work queue is empty.')):
            with self.subTest(message=message):
                shown = self.sized(q, queue, live, 40, 30)
                self.assertLessEqual(len(shown.splitlines()), 30)
                self.assertIn(message, flat(shown))
                self.assertTrue(all(cells(line) <= 40 and len(line) <= 40 for line in shown.splitlines()))


class Q3HostRegressions(unittest.TestCase):
    def host(self, capture='Work queue · fixture\nRUNNING 0', server_exists=False,
             attempt_exists=False, start_fails=False, blockers=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = root / '_archive/projects/dashboard/dashboard_queue_build_20261011T014430Z'
            receipt.mkdir(parents=True)
            (root / 'tools').mkdir()
            (root / 'code/apps/dashboard/test_dashboard_queue.py').write_text('print("fixture tests pass")\n')
            (root / 'code/apps/dashboard/dashboard_queue.py').write_text(
                'import os, sys\nfrom pathlib import Path\n'
                'with Path(os.environ["Q3_CLI"]).open("a") as f: f.write(repr(sys.argv[1:]) + "\\n")\n'
                'print("Work queue · fixture")\n')
            (root / 'code/lab/runners/c10w_p2_gate.py').write_text(
                'def check_gpu(): return {"blocking_processes": %r}\n' % list(blockers))
            (receipt / 'check_q2_host_live.py').write_text('print("fixture live checks pass")\n')
            for n in (1, 2):
                (receipt / ('host_attempt%d' % n)).mkdir()
                (receipt / ('host_attempt%d/locked.txt' % n)).write_text('unchanged\n')
            if attempt_exists:
                (receipt / 'host_attempt3').mkdir()
                (receipt / 'host_attempt3/locked.txt').write_text('unchanged\n')
            script = RECEIPTS / 'run_host_checks_q3.sh'
            # Before implementation run the old host script and fail on its behavior.
            if not script.exists():
                script = RECEIPTS / 'run_host_checks.sh'
            runner = receipt / script.name
            runner.write_text(script.read_text())
            # Let the old runner execute instead of failing mkdir before its checks.
            if script.name == 'run_host_checks.sh':
                runner.write_text(runner.read_text().replace('host_attempt2', 'legacy_attempt'))
            wrapper = r"""
function tmux() {
  printf '%s\n' "$*" >> "$Q3_COMMANDS"
  if [ "$1" != -L ]; then return 98; fi
  local server=$2 action=$3
  if [ "$server" = default ]; then
    if [ "$action" = list-sessions ]; then printf '%s\n' codexbuild; return 0; fi
    return 99
  fi
  if [ "$server" != q3check ] && [ "$server" != q1check ]; then return 97; fi
  case "$action" in
    list-sessions)
      if [ "$server" = q3check ] && [ "$Q3_EXISTS" = 1 ]; then printf '%s\n' owned-by-someone-else; return 0; fi
      printf '%s\n' 'no server running on /tmp/q3-fixture'; return 1;;
    new-session) if [ "$Q3_START_FAILS" = 1 ]; then return 2; fi; return 0;;
    kill-server) return 0;;
    capture-pane) printf '%s\n' "$Q3_CAPTURE"; return 0;;
    list-panes) printf '%s\n' '0 424242 /usr/bin/python3 code/apps/dashboard/dashboard_queue.py'; return 0;;
    *) return 96;;
  esac
}
function /bin/ps() { printf '%s\n' '1 1 00:01 /usr/sbin/launchd'; }
function sleep() { printf '%s\n' "$*" >> "$Q3_WAITS"; return 0; }
source "$1"
"""
            commands = root / 'commands.txt'
            cli = root / 'cli.txt'
            waits = root / 'waits.txt'
            env = dict(os.environ, Q3_CAPTURE=capture, Q3_EXISTS=str(int(server_exists)),
                       Q3_START_FAILS=str(int(start_fails)), Q3_COMMANDS=str(commands),
                       Q3_CLI=str(cli), Q3_WAITS=str(waits), PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run(['bash', '-c', wrapper, str(runner), str(runner)],
                                    env=env, capture_output=True, text=True, timeout=15)
            for n in (1, 2):
                self.assertEqual((receipt / ('host_attempt%d/locked.txt' % n)).read_text(), 'unchanged\n')
            if attempt_exists:
                self.assertEqual((receipt / 'host_attempt3/locked.txt').read_text(), 'unchanged\n')
                self.assertEqual(list((receipt / 'host_attempt3').iterdir()), [receipt / 'host_attempt3/locked.txt'])
            outputs = {str(p.relative_to(receipt)): p.read_text() for p in receipt.rglob('*')
                       if p.is_file() and p.suffix in ('.txt', '.exit')}
            return result, outputs, (commands.read_text().splitlines() if commands.exists() else []), \
                (cli.read_text().splitlines() if cli.exists() else []), \
                (waits.read_text().splitlines() if waits.exists() else [])

    def test_q3_host_01_fresh_attempt3_and_both_sized_renders(self):
        result, outputs, commands, cli, waits = self.host()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('host_attempt3/tests.exit', outputs)
        for name in ('tests', 'render_40', 'render_100', 'tmux_start', 'tmux_capture',
                     'visible_fit', 'gpu_check', 'queue_exemption', 'tmux_cleanup'):
            self.assertEqual(outputs['host_attempt3/' + name + '.exit'], '0\n')
        self.assertEqual(cli, ["['--once', '40', '30']", "['--once', '100', '45']"])
        self.assertEqual(sum(int(n) for n in waits), 8)

    def test_q3_host_02_private_small_server_visible_capture_and_owned_cleanup(self):
        result, outputs, commands, cli, waits = self.host()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        start = next(line for line in commands if 'new-session' in line)
        launch = re.fullmatch(r"-L q3check new-session -d -s q3check -x 40 -y 30 /usr/bin/python3 '(.*/tools/dashboard_queue\.py)'", start)
        self.assertIsNotNone(launch, 'Private tab must use the real tab command exactly: ' + start)
        gate = importlib.import_module('c10w_p2_gate')
        clt = '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python'
        inventory = '424242 %s %s\n' % (clt, launch.group(1))
        self.assertEqual(gate.blocking_processes(inventory, -1), [], 'Exact tab launch must retain its GPU exemption')
        capture = next(line for line in commands if 'capture-pane' in line)
        self.assertEqual(capture, '-L q3check capture-pane -p -t =q3check:')
        self.assertEqual(commands.count('-L q3check kill-server'), 1)
        self.assertTrue(all(line == '-L default list-sessions -F #{session_name}'
                            for line in commands if line.startswith('-L default ')))

    def test_q3_host_03_scrolled_header_fails_even_with_short_capture(self):
        result, outputs, commands, cli, waits = self.host('Summary: only the bottom is visible\nFinal card')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(outputs['host_attempt3/visible_fit.exit'], '1\n')
        self.assertEqual(commands.count('-L q3check kill-server'), 1)

    def test_q3_host_04_capture_over_30_rows_fails_with_header_visible(self):
        result, outputs, commands, cli, waits = self.host('Work queue\n' + '\n'.join('row%d' % n for n in range(30)))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(outputs['host_attempt3/visible_fit.exit'], '1\n')
        self.assertEqual(commands.count('-L q3check kill-server'), 1)

    def test_q3_host_05_refuse_existing_server_or_attempt_and_never_kill_unowned(self):
        result, outputs, commands, cli, waits = self.host(server_exists=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any('new-session' in line or 'kill-server' in line for line in commands), commands)
        result, outputs, commands, cli, waits = self.host(attempt_exists=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(commands, [])
        result, outputs, commands, cli, waits = self.host(start_fails=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any('kill-server' in line for line in commands), commands)

    def test_q3_host_06_gpu_exemption_rejects_own_pid_without_changing_other_jobs(self):
        result, outputs, commands, cli, waits = self.host(blockers=('424242 /usr/bin/python3 code/apps/dashboard/dashboard_queue.py',))
        self.assertIn('host_attempt3/queue_exemption.exit', outputs)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(outputs['host_attempt3/queue_exemption.exit'], '1\n')
        self.assertEqual(commands.count('-L q3check kill-server'), 1)
        result, outputs, commands, cli, waits = self.host(blockers=('515151 /usr/bin/python3 other-job.py',))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
