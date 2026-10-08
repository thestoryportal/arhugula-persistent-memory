"""Tests for the live dashboard state (tools/dashboard_live.py). Stdlib only; run with the dashboard's interpreter:
/usr/bin/python3 -B -m unittest tools.test_dashboard_live
"""
import os, sys, tempfile, time, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_live as L  # noqa: E402

RUNBOOK = """| ID | status | detail | next |
|---|---|---|---|
| **Old ruling (D-X1, 2026-10-01)** | **DECIDED (operator)** | text | done |
| **P2 eval HALT: invalid same-seed cosine (D-C10w-p2halt, 2026-10-08 00:06 MDT)** | **HALTED — awaiting operator budget ruling** | detail | next |
| **Some build (D-Y2)** | **awaiting operator yes** | x | y |
Prose that mentions awaiting operator outside a table row.
"""


class Rulings(unittest.TestCase):
    def test_rows_whose_status_awaits_the_operator(self):
        self.assertEqual(L.awaiting_rulings(RUNBOOK), [
            "P2 eval HALT: invalid same-seed cosine (D-C10w-p2halt, 2026-10-08 00:06 MDT)",
            "Some build (D-Y2)"])

    def test_decided_rows_and_prose_are_ignored(self):
        self.assertEqual(L.awaiting_rulings("| **A** | **DECIDED** | awaiting operator in detail | x |\n"), [])


class Coordinator(unittest.TestCase):
    def test_last_exit_line(self):
        log = ("2026-10-07T22:22:28-0600 DISPATCH p2-eval\n"
               "2026-10-08T00:06:01-0600 COORDINATOR_EXIT=6 p2-eval stopped: wrapper rc=2\n")
        out = L.coordinator_exit(log)
        self.assertEqual(out["code"], 6)
        self.assertEqual(out["reason"], "p2-eval stopped: wrapper rc=2")
        self.assertEqual(out["at"], L.iso_epoch("2026-10-08T00:06:01-0600"))

    def test_no_exit_yet(self):
        self.assertIsNone(L.coordinator_exit("2026-10-07T22:22:28-0600 DISPATCH p2-eval\n"))


class Staleness(unittest.TestCase):
    def test_events_newer_than_the_report_text(self):
        updated = L.board_epoch("2026-10-08 01:45 MDT")
        events = [(updated - 60, "older"), (updated + 120, "P2 HALT"), (updated + 5, "CORPUS/57")]
        self.assertEqual(L.newer_events(updated, events), ["CORPUS/57", "P2 HALT"])

    def test_unparseable_updated_counts_everything_as_newer(self):
        self.assertIsNone(L.board_epoch("yesterday"))
        self.assertEqual(L.newer_events(None, [(1.0, "a")]), ["a"])


class Reload(unittest.TestCase):
    def test_changed_source_triggers_reload(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "dashboard_x.py")
            open(p, "w").write("x")
            stamp = L.source_stamp(d)
            self.assertFalse(L.sources_changed(d, stamp))
            os.utime(p, (time.time() + 5, time.time() + 5))
            self.assertTrue(L.sources_changed(d, stamp))


class TeamTiles(unittest.TestCase):
    def test_sessions_from_tile_start_commands(self):
        cmds = ["/usr/bin/python3 '/t/dashboard_tile.py' 'program' 'LEAD · program session' '25'",
                "/usr/bin/python3 '/t/dashboard_report.py'",
                "/usr/bin/python3 '/t/dashboard_tile.py' 'codexz' 'Codex Z · ASTRA build' '30'"]
        self.assertEqual(L.tiled_sessions(cmds), {"program", "codexz"})

    def test_team_sessions_skip_dashboard_and_viewers(self):
        self.assertEqual(L.team_sessions(["dashboard", "dashboard_new", "helpers", "view-1", "program", "codexz"]),
                         {"program", "codexz"})

    def test_rebuild_only_after_the_set_is_stable(self):
        sup = L.TeamSupervisor(debounce_s=10, min_gap_s=30)
        tiled, now = {"program"}, 1000.0
        self.assertFalse(sup.should_rebuild(tiled, {"program", "codexz"}, now))        # first sight
        self.assertFalse(sup.should_rebuild(tiled, {"program", "codexz"}, now + 5))    # not stable long enough
        self.assertTrue(sup.should_rebuild(tiled, {"program", "codexz"}, now + 11))
        self.assertFalse(sup.should_rebuild(tiled, {"program", "codexz"}, now + 20))   # min gap after a rebuild
        self.assertFalse(sup.should_rebuild({"program"}, {"program"}, now + 100))     # nothing to do


class NowLines(unittest.TestCase):
    def test_order_and_wording(self):
        state = {"rulings": ["P2 eval HALT (D-C10w-p2halt)"],
                 "gpu": {"running": None, "last_exit": {"code": 6, "reason": "p2-eval stopped", "at": 0.0},
                         "last_name": "Step 5"},
                 "builds": [("Codex Z · ASTRA build", "Complete build brief")],
                 "helpers": ["Fold reviews (program)  ·  3m00s"]}
        lines = L.now_lines(state, now=3600.0)
        self.assertTrue(lines[0].startswith("! NEEDS YOUR RULING: P2 eval HALT"))
        self.assertIn("GPU idle", lines[1])
        self.assertIn("Step 5 coordinator stopped (exit 6", lines[1])
        self.assertEqual(lines[2], "» Codex Z · ASTRA build: Complete build brief")
        self.assertEqual(lines[3], "◦ helper: Fold reviews (program)  ·  3m00s")

    def test_running_gpu_job(self):
        state = {"rulings": [], "builds": [], "helpers": [],
                 "gpu": {"running": ("c10w", "p2-eval", "01:02:03"), "last_exit": None, "last_name": None}}
        self.assertEqual(L.now_lines(state, now=0.0), ["▸ GPU running: Step 5 · stage p2-eval · 01:02:03"])

    def test_clean_exit_reads_finished(self):
        state = {"rulings": [], "builds": [], "helpers": [],
                 "gpu": {"running": None, "last_exit": {"code": 0, "reason": "P2 complete", "at": 0.0}, "last_name": "Step 5"}}
        self.assertIn("finished", L.now_lines(state, now=60.0)[0])


class Clip(unittest.TestCase):
    def test_visible_width_only(self):
        line = "\033[1mabc\033[0mdef"
        self.assertEqual(L.clip(line, 4), "\033[1mabc\033[0md")
        self.assertEqual(L.clip("ab", 5), "ab")


class WordsAndAnswers(unittest.TestCase):
    def setUp(self):
        import dashboard_experiment as X
        self.X = X
        gen = [{"subj": "Zorbland", "template": t, "text": x, "full": f}
               for t, x, f in (("{}'s capital city is called", " Vondurk, and", False),
                               ("If you visit {}, its capital city is", " Vindex Vaskul,", True),
                               ("The main city and seat of government of {} is", " Vindex Vask.", True))]
        self.record = {"recipes": {"closedform": {"arms": {}},
                                   "oracle_p1": {"arms": {"A7_coined_coined": {"extra": {"generated": gen}}},
                                                 "detail": {"A7_coined_coined": [{"subj": "Zorbland", "val": "Vindex Vask"}]}}}}

    def test_facts_from_the_last_recipe_with_answers(self):
        recipe, templates, facts = self.X.answers_from_record(self.record)
        self.assertEqual(recipe, "oracle_p1")
        self.assertEqual(templates[1], "If you visit {}, its capital city is")
        self.assertEqual(facts, [{"subj": "Zorbland", "val": "Vindex Vask",
                                  "answers": [("Vondurk, and", False), ("Vindex Vaskul,", True), ("Vindex Vask.", True)]}])

    def test_lines_mark_right_and_wrong_and_show_the_words(self):
        recipe, templates, facts = self.X.answers_from_record(self.record)
        text = "\n".join(self.X.words_lines("eval.json", recipe, templates, facts, 160))
        plain = __import__("re").sub(r"\033\[[0-9;]*m", "", text)
        self.assertIn("Zorbland → Vindex Vask", plain)
        self.assertIn("✗ Vondurk, and", plain)
        self.assertIn("✓ Vindex Vaskul,", plain)
        self.assertIn("Q2 If you visit …, its capital city is", plain)

    def test_no_answers_recorded(self):
        self.assertIsNone(self.X.answers_from_record({"recipes": {"r": {"arms": {"A1_single": {}}}}}))


if __name__ == "__main__":
    unittest.main()
