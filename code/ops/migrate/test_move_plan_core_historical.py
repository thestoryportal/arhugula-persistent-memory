"""T346: every reader is covered by a repair or an immutable historical row."""
import unittest

from ops.migrate import fdsafe, move_plan_core as core
from test_move_plan_core import ENTRY, M, check_plans, historical, occ, repairs
# The ticket test must run every existing direct call of check_plans,
# and the guard tests that alone kill its _text/_int bypass mutants.
from test_move_plan_core import CheckPlans, CheckPlansRefuses, SurvivingGuards  # noqa: F401
from test_move_plan_core_limits import CellDigits  # noqa: F401

KEY = ("code/x.py", 3, "/p/u1/a.json")
REPAIR = (*KEY, "/m/experiments/c10r/runs/u1/a.json", 261)


def check(occurrences=(), rep=(), hist=(), entries=None):
    return core.check_plans(root=M, entries=[ENTRY] if entries is None else entries,
                            occurrences=list(occurrences), repairs=repairs(*rep),
                            historical=historical(*hist))


class Historical(unittest.TestCase):
    def test_duplicate_historical_preserves_repair_target_finding(self):
        self.assertEqual(check([occ()], rep=[(*KEY, "/v/elsewhere/a.json", 261)], hist=[KEY]), (
            ("duplicate-row", *KEY, "repeats a row of /m/program/historical.tsv"),
            ("not-under-target", *KEY,
             "new_text /v/elsewhere/a.json is not under /m/experiments/c10r/runs/u1")))

    def test_historical_oversized_line_refused(self):
        row = (KEY[0], "1" + "0" * 4300, KEY[2])
        table = historical(row)
        with self.assertRaises(fdsafe.Refusal) as caught:
            check(hist=[row])
        self.assertEqual(caught.exception.path, table[0] + ":2")
        self.assertIn("holds an integer of 4301 digits", str(caught.exception))

    def test_repair_checks_every_old_path_for_key(self):
        self.assertEqual(check([occ(), occ(old="/p/u9")], rep=[REPAIR]),
                         (("no-entry", *KEY, "no entry moves /p/u9"),))

    def test_historical_checks_every_old_path_for_key(self):
        self.assertEqual(check([occ(), occ(old="/p/u9")], hist=[KEY]),
                         (("no-entry", *KEY, "no entry moves /p/u9"),))

    def test_both_tables_report_rows_without_occurrences(self):
        other = ("code/y.py", KEY[1], KEY[2])
        self.assertEqual(check([], rep=[REPAIR], hist=[other]), (
            ("no-occurrence", *KEY, "no reader occurrence matches this row"),
            ("no-occurrence", *other, "no reader occurrence matches this row")))

    def test_historical_file_must_match(self):
        row = ("code/y.py", KEY[1], KEY[2])
        self.assertEqual(check([occ()], hist=[row]), (
            ("no-occurrence", *row, "no reader occurrence matches this row"),
            ("no-row", *KEY, "no repairs row for /p/u1")))

    def test_historical_line_must_match(self):
        row = (KEY[0], 4, KEY[2])
        self.assertEqual(check([occ()], hist=[row]), (
            ("no-occurrence", *row, "no reader occurrence matches this row"),
            ("no-row", *KEY, "no repairs row for /p/u1")))

    def test_historical_old_text_must_match(self):
        row = (KEY[0], KEY[1], "/p/u1/b.json")
        self.assertEqual(check([occ()], hist=[row]), (
            ("no-occurrence", *row, "no reader occurrence matches this row"),
            ("no-row", *KEY, "no repairs row for /p/u1")))

    def test_historical_mixed_line_endings_refused(self):
        name, text = historical(KEY)
        table = (name, text.replace("\n", "\r\n", 1))
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.check_plans(root=M, entries=[ENTRY], occurrences=[occ()],
                             repairs=repairs(), historical=table)
        self.assertEqual(caught.exception.path, name + ":2")
        self.assertEqual(str(caught.exception), f"{name + ':2'!r}: mixes LF and CRLF line endings")

    def test_historical_control_cell_refused(self):
        # [LAW:behavior-not-structure] DEL isolates the TSV refusal from row validation.
        table = historical((KEY[0] + "\x7f", KEY[1], KEY[2]))
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.check_plans(root=M, entries=[ENTRY], occurrences=[occ()],
                             repairs=repairs(), historical=table)
        self.assertEqual(caught.exception.path, table[0] + ":2")
        self.assertEqual(str(caught.exception), f"{table[0] + ':2'!r}: a cell holds a control character")

    def test_shared_helper_passes_historical(self):
        self.assertEqual(check_plans([], repairs()), ())

    def test_historical_only_covers_occurrence(self):
        self.assertEqual(check([occ()], hist=[KEY]), ())

    def test_empty_tables_do_not_drop_occurrence(self):
        self.assertEqual(check([occ()]), (("no-row", *KEY, "no repairs row for /p/u1"),))

    def test_empty_tables_without_occurrences(self):
        self.assertEqual(check(), ())

    def test_duplicate_in_repairs(self):
        self.assertEqual(check([occ()], rep=[REPAIR, REPAIR]),
                         (("duplicate-row", *KEY, "repeats a row of /m/program/repairs.tsv"),))

    def test_duplicate_in_historical(self):
        self.assertEqual(check([occ()], hist=[KEY, KEY]),
                         (("duplicate-row", *KEY, "repeats a row of /m/program/historical.tsv"),))

    def test_duplicate_across_tables(self):
        self.assertEqual(check([occ()], rep=[REPAIR], hist=[KEY]),
                         (("duplicate-row", *KEY, "repeats a row of /m/program/historical.tsv"),))

    def test_historical_without_occurrence(self):
        self.assertEqual(check(hist=[KEY]),
                         (("no-occurrence", *KEY, "no reader occurrence matches this row"),))

    def test_historical_without_entry(self):
        self.assertEqual(check([occ(old="/p/u9")], hist=[KEY]),
                         (("no-entry", *KEY, "no entry moves /p/u9"),))

    def test_historical_repeated_text_is_not_rewritten(self):
        self.assertEqual(check([occ(text="/p/u1/a.json /p/u1/a.json")], hist=[KEY]), ())

    def test_repairs_still_require_once(self):
        self.assertEqual(check([occ(text="/p/u1/a.json /p/u1/a.json")], rep=[REPAIR]),
                         (("not-once", *KEY, "old_text occurs 2 times on its line"),))

    def test_repairs_still_require_target(self):
        self.assertEqual(check([occ()], rep=[(*KEY, "/elsewhere", 261)]),
                         (("not-under-target", *KEY,
                           "new_text /elsewhere is not under /m/experiments/c10r/runs/u1"),))

    def test_mixed_tables_cover_distinct_occurrences(self):
        other = ("archive.md", 4, "/p/u1/a.json")
        self.assertEqual(check([occ(), occ(file=other[0], line=other[1])],
                               rep=[REPAIR], hist=[other]), ())

    def test_historical_is_required(self):
        with self.assertRaises(TypeError):
            core.check_plans(root=M, entries=[ENTRY], occurrences=[], repairs=repairs())

    def test_malformed_historical_tables(self):
        good = historical(KEY)
        malformed = [None, (), ("historical",), (1, "x\n"), ("historical", 3),
                     ("historical", ""), (good[0], good[1].rstrip("\n")),
                     (good[0], "line\tfile\told_text\n"),
                     (good[0], "file\tline\told_text\nmissing\t1\n")]
        for line in ("0", "03", "-1", "x", "", "1.0"):
            malformed.append(historical((KEY[0], line, KEY[2])))
        malformed.extend([historical(("", 3, KEY[2])), historical((KEY[0], 3, "")),
                          historical(("bad\0file", 3, KEY[2]))])
        for table in malformed:
            with self.subTest(table=table), self.assertRaises(fdsafe.Refusal) as caught:
                core.check_plans(root=M, entries=[ENTRY], occurrences=[occ()],
                                 repairs=repairs(), historical=table)
            self.assertIn("historical", caught.exception.path)

    def test_historical_crlf_and_line_one(self):
        table = historical((KEY[0], 1, KEY[2]))
        self.assertEqual(core.check_plans(root=M, entries=[ENTRY], occurrences=[occ(line=1)],
                         repairs=repairs(), historical=(table[0], table[1].replace("\n", "\r\n"))), ())


if __name__ == "__main__":
    unittest.main()
