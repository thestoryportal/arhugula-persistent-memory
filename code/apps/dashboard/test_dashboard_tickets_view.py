"""Tickets tab view: fixture snapshots only (the plan's data contract); no gh, git or tmux server calls."""
import ast
import importlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
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
        short = self.text(self.frame(width=100, height=12))
        self.assertTrue(any(" T039 " in line[:12] for line in short), "a 12-row terminal should give the table all rows")
        self.assertFalse(any(line.startswith("─" * 20) for line in short))
        narrow = self.text(self.frame(width=100, height=30))
        self.assertIn("T036", "\n".join(narrow))
        self.assertTrue(any("│" in line for line in narrow), "timeline with now marker missing at 100 wide")
        self.assertNotIn("goal of", self.row(self.frame(width=100, height=30), "T036"))
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
        frame = self.frame()
        merged, running = self.row(frame, "T005"), self.row(frame, "T036")
        self.assertIn("▒", merged)
        self.assertIn("█", merged)
        self.assertTrue(merged.rstrip().endswith("│"))
        self.assertTrue(running.rstrip().endswith("│"))
        self.assertIn("▒", self.row(frame, "T037"))
        self.assertEqual(len(merged.rstrip()), len(running.rstrip()))

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
        bar = self.row(frame, "T099").rstrip()
        self.assertIn("‹", bar)
        self.assertIn("█", self.row(frame, "T005"), "an old ticket squeezed the shared axis")
        for line in self.text(frame):
            self.assertFalse(any(unicodedata.category(ch).startswith("C") for ch in line), repr(line))
        self.assertIn("line one line two?", " ".join(self.text(frame)))


if __name__ == "__main__":
    unittest.main()
