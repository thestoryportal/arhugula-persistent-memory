"""T347: historical reader coverage and the shared fd-safe input boundary."""
import json
import os
import unittest

import test_move_unit_plan as plan


HEADER = "file\tline\told_text\n"


class Historical(plan.Base):
    def argv(self):
        return self.fx.check_plans_args()

    def historical_row(self):
        fx = self.fx
        fx.rewrite(fx.historical, f"{HEADER}docs/a.md\t2\t{fx.old}\n".encode())

    def test_historical_only_exits_zero_without_findings(self):
        self.historical_row()
        self.fx.rewrite(self.fx.repairs, (plan.REPAIR_HEADER + "\n").encode())
        proc = self.cli(*self.argv())
        self.assertEqual((proc.returncode, proc.stdout, proc.stderr), (0, "[]\n", ""))

    def test_uncovered_occurrence_exits_one_with_no_row(self):
        self.fx.rewrite(self.fx.repairs, (plan.REPAIR_HEADER + "\n").encode())
        proc = self.cli(*self.argv())
        self.assertEqual((proc.returncode, proc.stderr), (1, ""))
        self.assertEqual([row[0] for row in json.loads(proc.stdout)], ["no-row"])

    def test_both_tables_exit_one_with_duplicate_row(self):
        self.historical_row()
        proc = self.cli(*self.argv())
        self.assertEqual((proc.returncode, proc.stderr), (1, ""))
        self.assertEqual([row[0] for row in json.loads(proc.stdout)], ["duplicate-row"])

    def test_missing_historical_option_is_an_argparse_refusal(self):
        argv = self.argv()
        index = argv.index("--historical")
        del argv[index:index + 2]
        proc = self.cli(*argv)
        self.assertEqual((proc.returncode, proc.stdout), (2, ""))
        self.assertIn("the following arguments are required: --historical", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_historical_symlink_present_before_read_refuses(self):
        fx = self.fx
        target = fx.write(os.path.join(fx.other, "historical.tsv"), HEADER.encode())
        # [LAW:behavior-not-structure] Valid target bytes would pass if the reader followed this link.
        with plan.FK.swap_for_symlink("open", 1, fx.historical, target,
                                      match=plan.named(fx.m)) as fault:
            result = self.main(*self.argv())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, fx.historical)

    def test_missing_historical_file_refuses(self):
        os.unlink(self.fx.historical)
        self.assert_refused(self.main(*self.argv()), self.fx.historical, "[ENOENT]")

    def test_historical_must_be_utf8(self):
        self.fx.rewrite(self.fx.historical, b"\xff")
        self.assert_refused(self.main(*self.argv()), self.fx.historical, "UTF-8")

    def test_historical_path_must_be_normalized(self):
        argv = self.argv()
        path = self.fx.inp + "/./historical.tsv"
        argv[argv.index("--historical") + 1] = path
        self.assert_refused(self.main(*argv), path, "not a normalized path")

    def test_historical_large_line_number_refuses(self):
        self.fx.rewrite(self.fx.historical, f"{HEADER}docs/a.md\t{'1' * 5000}\t{self.fx.old}\n".encode())
        self.assert_refused(self.main(*self.argv()), self.fx.historical + ":2", "integer of 5000 digits")

    def test_historical_moved_parent_refuses(self):
        plan.IsolatedInputParents.moved_input(self, "check-plans", "historical")

    # [LAW:composability] The existing attack methods own fault injection and refusal assertions.
    def cases(self, table):
        return plan.Attacks.cases(self, {"check-plans": ("historical",)})

    test_leaf_swapped_for_a_symlink_between_scan_and_open_refuses = (
        plan.Attacks.test_leaf_swapped_for_a_symlink_between_scan_and_open_refuses)
    test_fifo_in_place_of_a_leaf_refuses_without_blocking = (
        plan.Attacks.test_fifo_in_place_of_a_leaf_refuses_without_blocking)
    test_leaf_open_errors_name_the_path_and_errno = plan.Attacks.test_leaf_open_errors_name_the_path_and_errno
    test_leaf_lstat_errors_name_the_path_and_errno = plan.Attacks.test_leaf_lstat_errors_name_the_path_and_errno
    test_late_parent_attacks_refuse_for_every_input = plan.Attacks.test_late_parent_attacks_refuse_for_every_input


if __name__ == "__main__":
    unittest.main()
