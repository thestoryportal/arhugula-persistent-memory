"""Tests for the Science Report viewer (tools/dashboard_report.py) and what it relies on: a subagent transcript that
vanishes mid-scan, a render failure, line widths at real pane sizes, a full clear on resize, and how the lead session
is found. Stdlib only; run with the dashboard's interpreter:
/usr/bin/python3 -B -m unittest tools.test_dashboard_report
"""
import io, json, os, re, shutil, stat, subprocess, sys, tempfile, unicodedata, unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_live as L  # noqa: E402
import dashboard_report as R  # noqa: E402
import dashboard_subagents as S  # noqa: E402

ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")
WIDTHS = (40, 72, 107, 113, 221)


def cells(line):
    """Terminal cells a line occupies, measured independently of the code under test: wide (W/F) characters take two,
    combining marks none, everything else one (tmux draws ━ ■ · — ┃ █ ░ in one cell, measured 2026-10-10)."""
    text = ANSI.sub("", line)
    return sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


STATE = {"rulings": ["P2 eval HALT: invalid same-seed cosine, a long ruling title that goes on and on " * 3],
         "alerts": ["codexmb4 shows no new step for 31 min"],
         "gpu": {"running": None, "jobs": [], "cpu_jobs": [], "last_exit": None, "last_name": None},
         "builds": [("Codex MB · math-lab build", "Read predecessor handoff and continue the build " * 4)],
         "helpers": ["Fix teamdash science report (762fa91c)  ·  2m37s"]}

STRESS = {"updated": "2026-10-10 01:15 MDT", "goal": 61, "out_of": 72,
          "brief": ("Made-up names ✅ are hard to recall when the question is worded differently. " * 30).strip(),
          "results": [{"date": "2026-10-0%d" % (i % 9 + 1), "best": [None, 14, 40, 70][i % 4], "kind": "write",
                       "score": "70 of 72 (two runs: 70 and 71, official reading)", "name": "Step %d: a long name ✅" % i,
                       "verdict": "No: it fits the training sentences but not the reworded questions " * 3}
                      for i in range(40)],
          "queue": [{"name": "NEW-1 (math check of earlier writes) — a second short check " * 2,
                     "status": "being built, waiting for the operator", "time": "about 2 hours"} for _ in range(4)]}


class Width(unittest.TestCase):
    """C: no rendered line is wider than the pane, at any width >= 40 (the last column stays free)."""

    def render_with(self, board, cols, rows):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(board, f)
        self.addCleanup(os.unlink, f.name)
        with patch.object(R, "BOARD", f.name), patch.object(L, "gather", return_value=STATE), \
             patch.object(L, "events", return_value=[(4e9, "CORPUS/58 changed"), (4e9, "HALT in results/c10x/a")]):
            return R.render(cols, rows)

    def assert_fits(self, lines, cols):
        for line in lines:
            self.assertLess(cells(line), cols, f"{cells(line)} cells in a {cols}-col pane: {ANSI.sub('', line)!r}")

    def test_stress_board_fits_every_width(self):
        for cols in WIDTHS:
            for rows in (12, 40, 80):
                with self.subTest(cols=cols, rows=rows):
                    lines = self.render_with(STRESS, cols, rows)
                    self.assertLessEqual(len(lines), rows)
                    self.assert_fits(lines, cols)

    def test_live_scoreboard_fits_every_width(self):
        with open(R.BOARD) as f:
            board = json.load(f)
        for cols in WIDTHS:
            with self.subTest(cols=cols):
                self.assert_fits(self.render_with(board, cols, 60), cols)

    def test_cut_brief_keeps_its_pointer_whole(self):
        for cols in WIDTHS:
            with self.subTest(cols=cols):
                plain = [ANSI.sub("", l) for l in self.render_with(STRESS, cols, 80)]
                self.assertTrue(any(l.endswith("(more: docs/c10_scoreboard.json)") for l in plain), plain[:12])

    def test_section_rule_ends_one_cell_short_of_the_edge(self):
        for cols in WIDTHS:
            with self.subTest(cols=cols):
                rule = next(l for l in self.render_with(STRESS, cols, 40) if "WHAT IT MEANS" in l)
                self.assertEqual(cells(rule), cols - 1)


class Clip(unittest.TestCase):
    def test_wide_characters_take_two_cells(self):
        self.assertEqual(L.clip("a✅b", 2), "a")
        self.assertEqual(L.clip("a✅b", 3), "a✅")

    def test_box_glyphs_take_one_cell_and_codes_survive_the_cut(self):
        self.assertEqual(L.clip("\033[1m━■·\033[0m━━", 3), "\033[1m━■·\033[0m")


class VanishedTranscript(unittest.TestCase):
    """A: a transcript deleted between listing and stat is skipped; any other stat failure still surfaces."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        self.live = self.agent("proj", "sess", "agent-live.jsonl")

    def agent(self, *parts):
        path = os.path.join(self.root, parts[0], parts[1], "subagents", parts[2])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("{}\n")
        return path

    def test_vanished_file_is_skipped(self):
        gone = os.path.join(self.root, "other", "sess", "subagents", "agent-gone.jsonl")
        with patch.object(S, "PROJECTS", self.root), patch.object(S.glob, "glob", return_value=[gone, self.live]):
            self.assertEqual(S.recent_agents(), [self.live])

    def test_unreadable_file_still_raises(self):
        locked = self.agent("locked", "sess", "agent-x.jsonl")
        folder = os.path.dirname(locked)
        os.chmod(folder, 0)
        self.addCleanup(os.chmod, folder, stat.S_IRWXU)
        with patch.object(S, "PROJECTS", self.root), patch.object(S.glob, "glob", return_value=[locked, self.live]):
            self.assertRaises(PermissionError, S.recent_agents)


class Tty(io.StringIO):
    def fileno(self):
        return 1


class StopLoop(Exception):
    pass


class Loop(unittest.TestCase):
    """B + C: the viewer loop survives a render failure (one red line, redraws on the 5 s cadence) and clears the whole
    pane, history included, when the pane size changes."""

    def run_loop(self, sizes, render):
        out, sleeps = Tty(), []

        def sleep(s):
            sleeps.append(s)
            if len(sleeps) == len(sizes):
                raise StopLoop

        with patch.object(R, "render", side_effect=render), patch.object(L, "maybe_reload"), \
             patch.object(R.os, "get_terminal_size", side_effect=[os.terminal_size(s) for s in sizes]), \
             patch.object(R.time, "sleep", side_effect=sleep), patch.object(sys, "argv", ["dashboard_report.py"]), \
             patch.object(sys, "stdout", out):
            self.assertRaises(StopLoop, R.main)
        return out.getvalue().split("\033[J")[:-1], sleeps   # every frame ends by clearing below itself

    def test_render_failure_is_shown_and_the_loop_keeps_drawing(self):
        calls = []

        def render(cols, rows):
            calls.append(cols)
            if len(calls) == 1:
                raise FileNotFoundError(2, "No such file or directory", "/x/agent-a.jsonl")
            return ["report line"]

        frames, sleeps = self.run_loop([(120, 20), (120, 20)], render)
        self.assertEqual(sleeps, [5, 5])
        self.assertIn("\033[38;5;196m", frames[0])
        self.assertIn("FileNotFoundError", frames[0])
        self.assertIn("/x/agent-a.jsonl", frames[0])
        self.assertIn("report line", frames[-1])
        self.assertNotIn("FileNotFoundError", frames[-1])

    def test_error_line_fits_the_pane(self):
        def render(cols, rows):
            raise RuntimeError("x" * 500)

        frames, _ = self.run_loop([(40, 10)], render)
        self.assertTrue(all(cells(l) < 40 for l in frames[-1].split("\n")))

    def test_full_clear_only_when_the_size_changes(self):
        frames, _ = self.run_loop([(80, 20), (80, 20), (60, 20)], lambda cols, rows: ["line"])
        self.assertEqual(["\033[3J" in f for f in frames], [True, False, True])   # first frame and the resize only


PANES = "\n".join("\t".join(p) for p in (
    ("maestro2", "1791592855", "2.1.295", "/repo/.claude/worktrees/c10k-route-a", "claude --permission-mode bypassPermissions 'You are MAESTRO2'"),
    ("codexmb5", "1791614919", "codex", "/repo/.claude/worktrees/c10k-route-a", "/x/start_codexmb5.sh"),
    ("dashboard", "1791586040", "Python", "/repo/.claude/worktrees/c10k-route-a", "/usr/bin/python3 '/repo/tools/dashboard_tile.py' 'maestro2'"),
    ("winning", "1791699999", "claude", "/Users/r/Projects/winning-defense", "claude"),
    ("repo2", "1791699999", "claude", "/repo2", "claude"),
    ("rclone", "1791593945", "zsh", "/repo", "rclone config; exec zsh"))) + "\n"


class Lead(unittest.TestCase):
    """D: the lead is LEAD if set; otherwise the newest tmux session with a Claude Code pane in this repo."""

    def test_detects_the_claude_session_in_this_repo(self):
        self.assertEqual(L.lead_session("", L.parse_panes(PANES), "/repo"), "maestro2")

    def test_override_wins(self):
        self.assertEqual(L.lead_session("program", L.parse_panes(PANES), "/repo"), "program")

    def test_newest_of_several_and_typed_in_claude(self):
        later = PANES + "maestro3\t1791700000\tclaude\t/repo\tzsh\n"
        self.assertEqual(L.lead_session("", L.parse_panes(later), "/repo"), "maestro3")

    def test_none_when_no_claude_pane_is_in_this_repo(self):
        codex_only = "".join(l + "\n" for l in PANES.splitlines() if not l.startswith("maestro2"))
        self.assertIsNone(L.lead_session("", L.parse_panes(codex_only), "/repo"))

    def test_cli_prints_the_override_and_nothing_when_none_found(self):
        tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_live.py")
        with tempfile.TemporaryDirectory() as shim:   # a fake tmux: never reaches the live server
            fake = os.path.join(shim, "tmux")
            with open(fake, "w") as f:
                f.write("#!/bin/sh\nprintf 'codexmb5\\t1\\tcodex\\t/nowhere\\tcodex\\n'\n")
            os.chmod(fake, 0o755)
            env = dict(os.environ, PATH=shim + os.pathsep + os.environ["PATH"])
            run = lambda lead: subprocess.run([sys.executable, "-B", tool, "--lead"], env=dict(env, LEAD=lead),
                                              capture_output=True, text=True, timeout=30)
            self.assertEqual((run("maestro9").returncode, run("maestro9").stdout), (0, "maestro9\n"))
            none = run("")
            self.assertEqual((none.returncode, none.stdout), (0, "\n"), none.stderr)   # an empty line: bash $(...) reads ""


if __name__ == "__main__":
    unittest.main()
