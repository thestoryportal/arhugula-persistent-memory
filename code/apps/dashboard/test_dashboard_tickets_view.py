"""Tickets tab view: fixture snapshots only (the plan's data contract); no gh, git or tmux server calls."""
import ast
import importlib
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import unittest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

NOW = 1_800_000_000.0
LONG_WORD = "recut/reviews/T005/r1/" + "x" * 150 + "/END-OF-PATH"
LONG_FINDING = ("2. The loader swallows every exception from the snapshot call and then renders an empty table, "
                "so a gh outage looks exactly like a folder with no tickets; the operator cannot tell a broken "
                "source from finished work, which the plan forbids because errors are never silently empty "
                "TAILWORD-ZEBRA")


def ticket(tid, label, state, wave=1, dispatch=None, pr_open=None, merged=None, reviews=(), pr=None,
           ci="none", deps=(), ruling=None, events=()):
    return {"id": tid, "label": label, "goal": "goal of %s: make the thing work end to end" % tid,
            "deps": list(deps), "wave": wave, "astra": bool(reviews),
            "write": ["code/apps/dashboard/%s.py" % tid.lower()], "test": "cd code && true",
            "out": "nothing outside write", "state": state, "pr": pr, "ci": ci,
            "times": {"dispatch": dispatch, "pr_open": pr_open, "merged": merged},
            "time_source": "ledger" if dispatch else "none", "reviews": list(reviews),
            "ruling": ruling or {"path": None, "kill_set": [], "summary": ""}, "events": list(events)}


def review(number, verdict, blocking=(), notes=0, killed=0, survived=0):
    return {"round": number, "verdict": verdict, "blocking": list(blocking), "notes": notes,
            "mutants": {"killed": killed, "survived": survived}, "path": "recut/reviews/T005/r%d/verdict.md" % number}


def fixture(errors=("gh: pr list failed: HTTP 502", "teamdash/ledger.tsv row 7: expected 5 fields")):
    m = 60.0
    tickets = [
        ticket("T001", "recut", "merged", 1, NOW - 300 * m, NOW - 290 * m, NOW - 285 * m, pr=40, ci="pass",
               reviews=[review(1, "GO", notes=1, killed=6, survived=0)]),
        ticket("T002", "recut", "merged", 1, NOW - 280 * m, NOW - 262 * m, NOW - 255 * m, pr=41, ci="pass"),
        ticket("T005", "recut", "merged", 2, NOW - 200 * m, NOW - 160 * m, NOW - 200 * m + 3723,
               pr=44, ci="pass", deps=["T001"],
               reviews=[review(1, "NO-GO", ["1. The timer freezes while gh runs.", LONG_FINDING], 2, 3, 2),
                        review(2, "NO-GO", ["1. The errors badge is green when two sources failed.",
                                            "2. A 100x30 render raises ValueError in wrap.",
                                            "3. See " + LONG_WORD], 1, 7, 1),
                        review(3, "GO", notes=3, killed=9, survived=0)],
               ruling={"path": "recut/reviews/T005/RULING.md", "kill_set": ["guard-timer", "guard-errors"],
                       "summary": "Round 3 GO accepted; the two surviving mutants are equivalent."},
               events=[{"t": NOW - 200 * m, "event": "dispatch", "rc": 0, "detail": "lane tk-T005"},
                       {"t": NOW - 160 * m, "event": "astra", "rc": 1, "detail": "NO-GO round 1"},
                       {"t": NOW - 140 * m, "event": "astra", "rc": 0, "detail": "GO round 3"}]),
        ticket("T006", "recut", "pr", 2, NOW - 50 * m, NOW - 10 * m, pr=47, ci="pending", deps=["T001"],
               reviews=[review(1, "NONE")]),
        ticket("T007", "recut", "waiting", 3, deps=["T006"]),
        ticket("T036", "teamdash", "running", 1, NOW - 125, events=[{"t": NOW - 125, "event": "dispatch", "rc": 0,
                                                                     "detail": "lane tk-T036"}]),
        ticket("T037", "teamdash", "running", 1, NOW - 20 * m),
        ticket("T038", "teamdash", "ready", 2, deps=["T036"]),
        ticket("T039", "teamdash", "pr", 2, NOW - 40 * m, NOW - 5 * m, pr=66, ci="fail"),
        ticket("H001", "hslice", "merged", 1, NOW - 100 * m, NOW - 95 * m, NOW - 92 * m, pr=50, ci="pass",
               reviews=[review(1, "NO-GO", ["1. Missing test."]), review(2, "GO")]),
        ticket("H002", "hslice", "ready", 1),
        ticket("H003", "hslice", "waiting", 2, deps=["H002"]),
    ]
    folders = [{"path": "/lean/%s" % name, "label": name, "tickets": sum(t["label"] == name for t in tickets)}
               for name in ("teamdash", "recut", "hslice")]
    return {"generated_epoch": NOW - 4, "folders": folders, "errors": list(errors), "tickets": tickets}


def cell_width(ch):
    if unicodedata.combining(ch):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in "WF" else 1


class TicketsView(unittest.TestCase):
    def setUp(self):
        self.view = importlib.import_module("dashboard_tickets")

    def frame(self, snap=None, width=131, height=54, now=NOW, ui=None, notes=(), loading=False):
        snap = fixture() if snap is None and not loading else snap
        frame = self.view.render(snap, ui or self.view.UI(), now, width, height, notes, loading=loading)
        self.assertLessEqual(len(frame.lines), height)
        for line in frame.lines:
            text = "".join(seg[0] for seg in line)
            self.assertLessEqual(sum(cell_width(ch) for ch in text), width, text)
        return frame

    def text(self, frame):
        return ["".join(seg[0] for seg in line) for line in frame.lines]

    def row(self, frame, tid):
        rows = [line for line in self.text(frame) if (" %s " % tid) in line[:12]]
        self.assertTrue(rows, "no table row for %s" % tid)
        return rows[0]

    def styled(self, frame, needle):
        return [seg for line in frame.lines for seg in line if needle in seg[0]]

    def select(self, tid, snap=None):
        order = [t["id"] for t in self.view.visible(snap or fixture(), self.view.UI())]
        return self.view.UI(selected=order.index(tid))

    def test_01_running_timer_ticks_and_merged_timer_is_final(self):
        first, later = self.frame(), self.frame(now=NOW + 1)
        self.assertIn("▶ 2:05", self.row(first, "T036"))
        self.assertIn("▶ 2:06", self.row(later, "T036"))
        self.assertIn("■ 1:02:03", self.row(first, "T005"))
        self.assertIn("■ 1:02:03", self.row(self.frame(now=NOW + 999), "T005"))
        self.assertIn("--:--", self.row(first, "T007"))

    def test_02_timer_colour_against_target_also_has_a_mark(self):
        frame = self.frame()
        self.assertIn(("▶ 2:05  ", "green"), [(s[0], s[1]) for s in self.styled(frame, "2:05")])
        self.assertIn(("▶ 20:00! ", "yellow"), [(s[0], s[1]) for s in self.styled(frame, "20:00")])
        self.assertIn(("◆ 40:00!!", "red"), [(s[0], s[1]) for s in self.styled(frame, "40:00")])

    def test_03_review_cycles_one_glyph_per_round(self):
        frame = self.frame()
        self.assertIn("✗✗✓ 3", self.row(frame, "T005"))
        self.assertIn("✗✓ 2", self.row(frame, "H001"))
        self.assertIn("? 1", self.row(frame, "T006"))
        detail = "\n".join(self.text(self.frame(ui=self.select("T005"))))
        for needle in ("R1 ✗ NO-GO", "R2 ✗ NO-GO", "R3 ✓ GO", "3 killed / 2 survived", "guard-timer, guard-errors",
                       "Reviews: 3 rounds"):
            self.assertIn(needle, detail)

    def test_04_every_blocking_finding_is_wrapped_never_cut(self):
        ui = self.select("T005")
        for width in (131, 100, 60):
            full = self.view.UI(selected=ui.selected, full=True)
            frame = self.frame(width=width, height=400, ui=full)
            words = " ".join(" ".join(self.text(frame)).split())
            self.assertIn(" ".join(LONG_FINDING.split()[1:]), words)
            for finding in ("The timer freezes while gh runs.", "A 100x30 render raises ValueError in wrap."):
                self.assertIn(finding, words)
            self.assertIn(LONG_WORD, "".join(line.strip() for line in self.text(frame)))
        split = self.text(self.frame(width=100, height=30, ui=ui))
        self.assertIn("more lines", split[-1] + split[-2])
        bottom = self.frame(width=100, height=30, ui=self.view.UI(selected=ui.selected, full=True, scroll=10 ** 6))
        seen = " ".join(self.text(bottom))
        self.assertIn("TAILWORD-ZEBRA", " ".join(self.text(self.frame(width=100, height=30, ui=self.view.UI(
            selected=ui.selected, full=True, scroll=self.find_scroll(ui.selected, "TAILWORD-ZEBRA"))))))
        self.assertGreater(bottom.max_scroll, 0)
        self.assertIn("Snapshot errors", seen)

    def find_scroll(self, selected, needle):
        for scroll in range(0, 200):
            frame = self.view.render(fixture(), self.view.UI(selected=selected, full=True, scroll=scroll), NOW, 100, 30)
            if needle in " ".join(self.text(frame)):
                return scroll
        self.fail("%s is unreachable by scrolling" % needle)

    def test_05_grouped_by_folder_order_then_wave_then_id(self):
        lines = self.text(self.frame(height=200))
        order = [t["id"] for t in self.view.visible(fixture(), self.view.UI())]
        self.assertEqual(order, ["T036", "T037", "T038", "T039", "T001", "T002", "T005", "T006", "T007",
                                 "H001", "H002", "H003"])
        heads = [line.strip() for line in lines if line.strip().startswith("▌")]
        self.assertEqual([h.split()[1] + " " + h.split()[3] + h.split()[4] for h in heads][:3],
                         ["teamdash wave1", "teamdash wave2", "recut wave1"])
        positions = [next(i for i, line in enumerate(lines) if (" %s " % tid) in line[:12]) for tid in order]
        self.assertEqual(positions, sorted(positions))

    def test_06_narrow_and_tiny_terminals_degrade_without_error(self):
        for width, height in ((131, 54), (100, 30), (80, 24), (60, 20), (40, 10), (30, 8), (1, 1), (0, 0)):
            for ui in (self.view.UI(), self.select("T005"), self.view.UI(full=True), self.view.UI(help=True)):
                frame = self.frame(width=width, height=height, ui=ui)
                self.assertTrue(frame.lines or height == 0)
        self.assertIn("too small 30x8", self.text(self.frame(width=30, height=8))[0])
        short = self.text(self.frame(width=100, height=16))
        self.assertTrue(any(" T039 " in line[:12] for line in short), "a 16-row terminal should give the table all rows")
        self.assertFalse(any(line.startswith("─" * 20) for line in short))
        narrow = self.text(self.frame(width=100, height=30))
        self.assertIn("T036", "\n".join(narrow))
        self.assertIn("goal of", self.row(self.frame(width=100, height=30), "T036"))
        self.assertIn("goal of T036", self.row(self.frame(), "T036"))
        self.frame(snap={"generated_epoch": NOW, "folders": [], "errors": [], "tickets": []})
        loading = self.text(self.frame(loading=True, width=100, height=30))
        self.assertIn("loading", " ".join(loading))
        self.assertTrue(any(":" in line for line in loading[:1]))

    def test_07_errors_badge_red_when_nonzero(self):
        red = [s for s in self.styled(self.frame(), "ERRORS 2") if s[1] == "red"]
        self.assertTrue(red)
        clean = self.frame(snap=fixture(errors=()))
        self.assertFalse(self.styled(clean, "ERRORS"))
        self.assertTrue([s for s in self.styled(clean, "errors 0") if s[1] != "red"])
        noted = self.frame(snap=fixture(errors=()), notes=("snapshot failed: OSError: disk",))
        self.assertTrue([s for s in self.styled(noted, "ERRORS 1") if s[1] == "red"])
        self.assertIn("snapshot failed", " ".join(self.text(noted)))

    def test_08_timeline_shared_axis_build_and_review_segments(self):
        frame = self.frame(ui=self.view.UI(timeline=True))
        merged, running = self.row(frame, "T005"), self.row(frame, "T036")
        self.assertIn("▒", merged)
        self.assertIn("█", merged)
        self.assertIn("│ build", merged)
        self.assertIn("│ build", running)
        self.assertIn("▒", self.row(frame, "T037"))
        self.assertEqual(merged.index("│"), running.index("│"))

    def test_09_header_stats(self):
        head = " ".join(self.text(self.frame())[:4])
        self.assertIn("4/12 merged", head)
        self.assertIn("▶ RUNNING 2", head)
        self.assertIn("◆ PR 2", head)
        self.assertIn("1st-round NO-GO 67%", head)
        self.assertIn("median dispatch→merge 20:00", head)
        self.assertIn("0.50/h", head)

    def test_10_keys(self):
        view, snap = self.view, fixture()
        ui = view.UI()
        ui = view.on_key(ui, ord("j"), snap, 0)
        self.assertEqual(ui.selected, 1)
        ui = view.on_key(ui, ord("k"), snap, 0)
        self.assertEqual(ui.selected, 0)
        self.assertEqual(view.on_key(ui, ord("k"), snap, 0).selected, 0)
        self.assertTrue(view.on_key(ui, 10, snap, 0).full)
        self.assertTrue(view.on_key(ui, 9, snap, 0).full)
        full = view.on_key(view.UI(full=True), ord("j"), snap, 5)
        self.assertEqual((full.selected, full.scroll), (0, 1))
        self.assertEqual(view.on_key(view.UI(full=True, scroll=5), ord("j"), snap, 5).scroll, 5)
        ui = view.on_key(view.UI(), ord("f"), snap, 0)
        self.assertEqual(ui.folder, "teamdash")
        self.assertEqual([t["id"] for t in view.visible(snap, ui)], ["T036", "T037", "T038", "T039"])
        for _ in range(3):
            ui = view.on_key(ui, ord("f"), snap, 0)
        self.assertIsNone(ui.folder)
        ui = view.on_key(view.UI(), ord("a"), snap, 0)
        self.assertEqual([t["id"] for t in view.visible(snap, ui)], ["T036", "T037", "T039", "T006"])
        helped = self.text(self.frame(ui=view.on_key(view.UI(), ord("h"), snap, 0)))
        legend = " ".join(helped[-3:])
        for needle in ("✓ GO", "✗ NO-GO", "▶ running", "■ merged", "▒ build", "│ now"):
            self.assertIn(needle, legend)

    def test_11_loader_never_blocks_the_clock_and_keeps_last_snapshot(self):
        gate, calls = threading.Event(), []

        def fetch():
            calls.append(1)
            if len(calls) == 1:
                return fixture()
            gate.wait(5)
            raise OSError("gh hung up")

        loader = self.view.Loader(fetch)
        loader.refresh()
        worker = threading.Thread(target=loader.refresh)
        worker.start()
        snap, problem, loaded = loader.state()
        self.assertEqual((len(snap["tickets"]), problem, loaded), (12, None, True))
        self.assertTrue(worker.is_alive())
        gate.set()
        worker.join(5)
        snap, problem, _ = loader.state()
        self.assertEqual(len(snap["tickets"]), 12)
        self.assertIn("gh hung up", problem)
        self.assertEqual(self.view.Loader(fetch).state(), (None, None, False))

    def test_12_imports_stdlib_only_data_module_inside_main(self):
        tree = ast.parse((TOOLS / "dashboard_tickets.py").read_text())
        allowed = {"argparse", "curses", "locale", "statistics", "sys", "threading", "time", "unicodedata",
                   "dataclasses", "pathlib", "typing"}
        top = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                top.add(node.module.split(".")[0])
        self.assertLessEqual(top, allowed)
        main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
        inner = {a.name for n in ast.walk(main) if isinstance(n, ast.Import) for a in n.names}
        self.assertIn("dashboard_tickets_data", inner)

    def test_13_tab_script_and_single_team_line(self):
        launcher = TOOLS / "dashboard_tickets_tab.sh"
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            stub = folder / "tmux"
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$TK_TEST_LOG"\n'
                            'case "$1" in\nlist-windows) printf "%s\\n" "$TK_TEST_WINDOWS"; exit "${TK_TEST_RC:-0}";;\n'
                            'new-window) exit 0;;\n*) exit 98;;\nesac\n')
            stub.chmod(0o755)
            log = folder / "commands.txt"
            env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ["PATH"],
                       TK_TEST_LOG=str(log), TK_TEST_WINDOWS="team\nqueue")
            first = subprocess.run(["bash", str(launcher), "tk-fixture"], env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            calls = log.read_text().splitlines()
            self.assertEqual(len(calls), 2)
            self.assertIn("-n tickets", calls[1])
            self.assertIn("/usr/bin/python3 '%s/dashboard_tickets.py'" % TOOLS, calls[1])
            log.write_text("")
            env["TK_TEST_WINDOWS"] = "team\nqueue\ntickets"
            again = subprocess.run(["bash", str(launcher), "tk-fixture"], env=env, capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(len(log.read_text().splitlines()), 1)
            env["TK_TEST_RC"] = "3"
            failed = subprocess.run(["bash", str(launcher), "tk-fixture"], env=env, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("no 'tk-fixture' session", failed.stderr)
        team = (TOOLS / "team_dashboard.sh").read_text().splitlines()
        hits = [i for i, line in enumerate(team) if "dashboard_tickets_tab.sh" in line]
        self.assertEqual(len(hits), 1)
        self.assertIn('bash "$T/dashboard_queue_tab.sh" "$NEW"', team[hits[0] - 1])
        self.assertTrue(team[hits[0]].startswith('bash "$T/dashboard_tickets_tab.sh" "$NEW" >/dev/null || exit 1'))

    def test_14_default_folders_are_lean_folders_with_tickets(self):
        with tempfile.TemporaryDirectory() as directory:
            lean = Path(directory)
            for name in ("recut", "teamdash", "tools"):
                (lean / name).mkdir()
            (lean / "recut" / "tickets").mkdir()
            (lean / "teamdash" / "tickets").mkdir()
            (lean / "board.py").write_text("")
            self.assertEqual(self.view.default_folders(lean), [str(lean / "recut"), str(lean / "teamdash")])

    def test_15_axis_capped_to_8h_and_control_characters_cleaned(self):
        snap = fixture()
        old = ticket("T099", "teamdash", "running", 1, NOW - 2 * 86400, events=[
            {"t": NOW - 60, "event": "lane\x1b[31m", "rc": 0, "detail": "line one\nline two\x07"}])
        old["goal"] = "evil\x1b[2J\ngoal\tend"
        snap["tickets"].append(old)
        frame = self.frame(snap=snap, height=200, ui=self.select("T099", snap))
        self.assertIn("2d00h", self.row(frame, "T099"))
        line = self.frame(snap=snap, height=200, ui=self.view.UI(selected=self.select("T099", snap).selected,
                                                                    timeline=True))
        self.assertIn("‹", self.row(line, "T099"))
        self.assertIn("█", self.row(line, "T005"), "an old ticket squeezed the shared axis")
        for line in self.text(frame):
            self.assertFalse(any(unicodedata.category(ch).startswith("C") for ch in line), repr(line))
        self.assertIn("line one line two?", " ".join(self.text(frame)))


GOAL_140 = ("the tickets table shows every goal in full words across two rows, so an operator can read what each "
            "ticket builds without opening the detail")
BARS = set("▒█░▓▀▄‹│")


class RoundTwo(unittest.TestCase):
    """Round 2 (operator feedback): full goals, plain-word phases, a separate labeled timeline, phone layouts."""
    setUp = TicketsView.setUp
    frame = TicketsView.frame
    text = TicketsView.text
    row = TicketsView.row
    styled = TicketsView.styled
    select = TicketsView.select

    def head_index(self, lines):
        return next(i for i, line in enumerate(lines) if " ID " in line and "GOAL" in line)

    def ticket_lines(self, lines, tid):
        """A table ticket's first row and its continuation rows (rows whose first 12 cells are blank)."""
        start = next(i for i, line in enumerate(lines) if (" %s " % tid) in line[:12])
        out = [lines[start]]
        for line in lines[start + 1:]:
            if line[:12].strip() or not line.strip():
                break
            out.append(line)
        return out

    def goal_text(self, lines, tid):
        col = lines[self.head_index(lines)].index("GOAL")
        return " ".join(line[col:].strip() for line in self.ticket_lines(lines, tid))

    def with_goal(self, tid, goal):
        snap = fixture()
        next(t for t in snap["tickets"] if t["id"] == tid)["goal"] = goal
        return snap

    def test_r2_01_goal_is_complete_or_ends_in_ellipsis_after_whole_words(self):
        self.assertEqual(len(GOAL_140), 140)
        lines = self.text(self.frame(snap=self.with_goal("T036", GOAL_140)))
        self.assertEqual(" ".join(self.goal_text(lines, "T036").split()), GOAL_140)
        self.assertTrue(self.goal_text(lines, "T036").startswith("the tickets table"), "goal cut at the left")
        longer = GOAL_140 + " and " + GOAL_140
        for width, height in ((131, 54), (100, 30), (80, 30)):
            lines = self.text(self.frame(snap=self.with_goal("T036", longer), width=width, height=height))
            shown = self.goal_text(lines, "T036")
            self.assertTrue(shown.endswith("…"), shown)
            words = shown[:-1].split()
            self.assertGreater(len(words), 3)
            self.assertEqual(words, longer.split()[:len(words)], "a goal word was cut or the goal starts mid-text")
            self.assertLessEqual(len(self.ticket_lines(lines, "T036")), 2)

    def test_r2_02_no_bars_or_block_glyphs_in_table_rows(self):
        for width, height in ((131, 54), (100, 30), (80, 24)):
            lines = self.text(self.frame(width=width, height=height))
            head = self.head_index(lines)
            end = next((i for i in range(head + 1, len(lines)) if lines[i].startswith("─")), len(lines))
            self.assertGreater(end - head, 4)
            for line in lines[head:end]:
                self.assertFalse(set(line) & BARS, line)

    def test_r2_03_phase_in_plain_words_with_a_glyph(self):
        snap, m = fixture(), 60.0
        snap["tickets"] += [ticket("T040", "teamdash", "pr", 3, NOW - 30 * m, NOW - 5 * m, pr=70, ci="pending"),
                            ticket("T041", "teamdash", "pr", 3, NOW - 30 * m, NOW - 5 * m, pr=71, ci="pass"),
                            ticket("T042", "teamdash", "waiting", 3, deps=["T001", "T037"])]
        expect = {"T007": "· waiting on T006", "H003": "· waiting on H002", "T042": "· waiting on T037",
                  "T038": "○ ready", "T036": "▶ building", "T006": "◆ in review (round 1)",
                  "T039": "◆ PR open, CI failed", "T040": "◆ PR open, CI pending", "T041": "◆ PR open, CI passed",
                  "T005": "■ merged", "H001": "■ merged"}
        frame = self.frame(snap=snap, height=200)
        for tid, words in expect.items():
            self.assertIn(words, self.row(frame, tid))
        cards = "\n".join(self.text(self.frame(snap=snap, width=50, height=200)))
        for words in expect.values():
            self.assertIn(words[2:], cards)

    def test_r2_04_time_column_splits_build_and_review_in_words(self):
        lines = self.text(self.frame(height=80))
        joined = lambda tid, rows=None: " ".join(self.ticket_lines(rows or lines, tid))
        self.assertIn("■ 1:02:03", joined("T005"))
        self.assertIn("build 40m · review 22m", joined("T005"))
        self.assertIn("build 40m · review 10m", joined("T006"))
        self.assertIn("build 40m · review 11m", joined("T006", self.text(self.frame(height=80, now=NOW + 60))))
        crowded = self.text(self.frame(snap=self.with_goal("T001", GOAL_140), ui=self.select("T006")))
        self.assertIn("build 40m · review 10m", joined("T006", crowded), "the selected ticket keeps its split")
        self.assertIn("build 10m · review 5m", joined("T001", crowded), "a wrapped goal's second row carries the split")
        self.assertIn("build 2m", joined("T036"))
        self.assertNotIn("review", joined("T036"))
        self.assertNotIn("build", joined("T007"))
        on = self.select("T005")
        self.assertIn("build 40m · review 22m", joined("T005", self.text(self.frame(width=100, height=30, ui=on))))
        self.assertNotIn("build 40m", joined("T005", self.text(self.frame(width=90, height=30, ui=on))))

    def test_r2_05_timeline_screen_has_legend_clock_axis_and_durations(self):
        snap, view = fixture(), self.view
        on = view.on_key(view.UI(), ord("t"), snap, 0)
        self.assertTrue(on.timeline)
        self.assertFalse(view.on_key(on, ord("t"), snap, 0).timeline)
        self.assertFalse(view.on_key(on, 27, snap, 0).timeline)
        old = ticket("T099", "teamdash", "running", 1, NOW - 2 * 86400)
        snap["tickets"].append(old)
        chosen = self.select("T005", snap)
        for width, height in ((131, 54), (100, 30)):
            frame = self.frame(snap=snap, width=width, height=height, ui=replace_ui(view, chosen, timeline=True))
            lines = self.text(frame)
            legend = next(i for i, line in enumerate(lines) if "▒ build = dispatch → PR open" in line)
            self.assertIn("█ review/land = PR open → merged", lines[legend])
            self.assertIn("│ now", lines[legend])
            axis = lines[legend + 1]
            self.assertGreaterEqual(len(re.findall(r"\b\d\d:\d\d\b", axis)), 4, "8 h span: hourly HH:MM ticks")
            ruler = lines[legend + 2]
            for label in re.finditer(r"\b\d\d:\d\d\b", axis):
                self.assertIn("┬", ruler[label.start():label.end()], axis)
            self.assertEqual(axis.split()[0], time.strftime("%H:%M", time.localtime(NOW - 8 * 3600)))
            row = self.row(frame, "T005")
            self.assertTrue(row.startswith("›"), "selected ticket not marked")
            self.assertIn(("T005", "sel"), [(s[0].strip(), s[1]) for s in self.styled(frame, "T005")])
            for needle in ("▒", "█", "build 40m · review 22m · total 1h02m"):
                self.assertIn(needle, row)
            self.assertIn("│", self.row(frame, "T036"))
            self.assertIn("build 2m · total 2m", self.row(frame, "T036"))
            self.assertIn("‹", self.row(frame, "T099"))
            self.assertIn("not dispatched", self.row(frame, "T007"))

    def test_r2_06_legend_line_under_the_header(self):
        lines = self.text(self.frame())
        above = " ".join(lines[3:self.head_index(lines)])
        self.assertEqual(len([line for line in lines[3:self.head_index(lines)] if "✗ NO-GO" in line]), 1)
        for needle in ("▶ building", "◆ PR", "■ merged", "○ ready", "· waiting", "✓ GO", "✗ NO-GO", "? none",
                       "✓ pass", "✗ fail", "… pending", "! >15 min", "!! >30 min"):
            self.assertIn(needle, above)

    def test_r2_07_default_folders_include_nested_ticket_folders(self):
        with tempfile.TemporaryDirectory() as directory:
            lean = Path(directory)
            for sub in ("recut/tickets", "recut/followup/tickets", "a/b/c/tickets", "a/b/c/d/tickets", "tools/x"):
                (lean / sub).mkdir(parents=True)
            self.assertEqual(self.view.default_folders(lean),
                             [str(lean / "a/b/c"), str(lean / "recut"), str(lean / "recut/followup")])

    def card_line(self, lines, tid):
        return next(i for i, line in enumerate(lines) if re.search(r"\b%s\b" % tid, line))

    def test_r2_08_phone_cards_at_50x30_and_45x40(self):
        snap = self.with_goal("T036", GOAL_140)
        order = [t["id"] for t in self.view.visible(snap, self.view.UI())]
        for width, height in ((50, 30), (45, 40)):
            for chosen in ("T036", "T037", "T039"):
                frame = self.frame(snap=snap, width=width, height=height, ui=self.select(chosen, snap))
                lines = self.text(frame)
                self.assertIn("merged", lines[0])
                self.assertRegex(lines[0], r"\d\d:\d\d:\d\d")
                self.assertIn("▶2", lines[1])
                self.assertNotIn("GOAL", "\n".join(lines))
                self.assertFalse(set("".join(lines)) & set("▒░▓"), "bars on the card screen")
                shown = [tid for tid in order if any(re.search(r"\b%s\b" % tid, line) for line in lines)]
                self.assertIn(chosen, shown)
                self.assertGreaterEqual(len(shown), 2)
                for tid in shown:
                    one = lines[self.card_line(lines, tid)]
                    timer = self.view.timer_seg(next(t for t in snap["tickets"] if t["id"] == tid), NOW)[0].strip()
                    self.assertTrue(one.rstrip().endswith(timer), (tid, one))
                    self.assertIn(self.view.state_of(next(t for t in snap["tickets"] if t["id"] == tid))[1], one)
            lines = self.text(self.frame(snap=snap, width=width, height=height, ui=self.select("T036", snap)))
            first = self.card_line(lines, "T036")
            self.assertIn("building", lines[first + 1])
            goal = []
            for line in lines[first + 2:]:
                if "┈" in line:
                    break
                goal.append(line.strip())
            self.assertLessEqual(len(goal), 3)
            words = " ".join(goal).rstrip("…").split()
            self.assertEqual(words, GOAL_140.split()[:len(words)])
            self.assertTrue(" ".join(goal) == GOAL_140 or " ".join(goal).endswith("…"))
        self.assertIn("too small", self.text(self.frame(width=60, height=15))[0])
        self.assertNotIn("too small", self.text(self.frame(width=40, height=16))[0])
        full = self.text(self.frame(width=45, height=40, ui=self.view.UI(selected=order.index("T005"), full=True)))
        self.assertIn("T005", full[2])
        helped = " ".join(" ".join(self.text(self.frame(width=50, height=30, ui=self.view.UI(help=True)))).split())
        for needle in ("▶ building", "✓ GO", "… pending", "! >15 min", "t timeline"):
            self.assertIn(needle, helped)
        self.assertNotIn("✓ GO", " ".join(self.text(self.frame(width=50, height=30))[:3]))

    def test_r2_09_narrow_timeline_and_detail_return(self):
        view = self.view
        frame = self.frame(width=50, height=30, ui=view.UI(timeline=True))
        lines = self.text(frame)
        legend = next(i for i, line in enumerate(lines) if "▒ build" in line)
        self.assertIn("█ review", lines[legend + 1])
        axis = lines[legend + 2]
        self.assertEqual(len(re.findall(r"\b\d\d:\d\d\b", axis)), 2, axis)
        row = self.row(frame, "T005")
        self.assertIn("▒", row)
        self.assertIn("█", row)
        self.assertTrue(row.rstrip().endswith("1h02m"), row)
        full = view.on_key(view.UI(), 10, fixture(), 0)
        self.assertTrue(full.full)
        self.assertFalse(view.on_key(full, 27, fixture(), 0).full)
        self.assertFalse(view.on_key(full, 10, fixture(), 0).full)

    def test_r2_10_taps_select_open_and_scroll(self):
        view, snap = self.view, fixture()
        order = [t["id"] for t in view.visible(snap, view.UI())]
        frame = view.render(snap, view.UI(), NOW, 50, 30)
        lines = self.text(frame)
        y = self.card_line(lines, "T037")
        ui = view.on_mouse(view.UI(), frame, y, view.TAP, snap)
        self.assertEqual(ui.selected, order.index("T037"))
        self.assertEqual(view.on_mouse(view.UI(), frame, y + 2, view.TAP, snap).selected, order.index("T037"))
        self.assertEqual(view.on_mouse(view.UI(), frame, 0, view.TAP, snap), view.UI())
        ui = self.select("T005")
        again = view.render(snap, ui, NOW, 50, 30)
        opened = view.on_mouse(ui, again, self.card_line(self.text(again), "T005"), view.TAP, snap)
        self.assertTrue(opened.full)
        detail = view.render(snap, opened, NOW, 50, 30)
        self.assertFalse(view.on_mouse(opened, detail, 5, view.TAP, snap).full)
        self.assertEqual(view.on_mouse(view.UI(), frame, 5, view.WHEEL_DOWN, snap).selected, 1)
        self.assertEqual(view.on_mouse(view.UI(selected=3), frame, 5, view.WHEEL_UP, snap).selected, 2)
        self.assertEqual(view.on_mouse(opened, detail, 5, view.WHEEL_DOWN, snap).scroll, 1)
        wide = view.render(snap, view.UI(), NOW, 131, 80)
        y = next(i for i, line in enumerate(self.text(wide)) if " T005 " in line[:12])
        self.assertEqual(view.on_mouse(view.UI(), wide, y, view.TAP, snap).selected, order.index("T005"))
        self.assertEqual(view.on_mouse(view.UI(), wide, y + 1, view.TAP, snap).selected, order.index("T005"))


def replace_ui(view, ui, **changes):
    fields = dict(ui.__dict__)
    fields.update(changes)
    return view.UI(**fields)


if __name__ == "__main__":
    unittest.main()
