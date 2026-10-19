"""T347: historical reader coverage and the shared fd-safe input boundary."""
import contextlib
import json
import os
import unittest
from unittest import mock

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

    @contextlib.contextmanager
    def history_fd(self):
        real, fds = os.open, set()
        def opened(first, *args, **kwargs):
            fd = real(first, *args, **kwargs)
            if first == 'historical.tsv':
                fds.add(fd)
            else:
                fds.discard(fd)
            return fd
        with mock.patch.object(os, 'open', opened):
            yield lambda fd, *a, **kw: fd in fds

    def test_historical_parent_rebound_at_later_reader_open(self):
        fx = self.fx
        parent = fx.mk('isolated-history')
        target = os.path.join(parent, 'historical.tsv')
        os.rename(fx.historical, target)
        fx.historical = target
        with plan.FK.rename_and_rebind('open', 1, parent, match=plan.named('readers.json')):
            observed = self.main(*fx.check_plans_args())
            self.assert_refused(observed, parent)

    def test_historical_regular_file_changes_between_scan_and_open(self):
        fx = self.fx
        real = os.open
        def opened(first, *args, **kwargs):
            if first == 'historical.tsv':
                fx.rewrite(fx.historical, b'file\tline\told_text\n\n')
            return real(first, *args, **kwargs)
        with mock.patch.object(os, 'open', opened):
            self.assert_refused(self.main(*fx.check_plans_args()), fx.historical, 'changed between scan and open')

    def test_historical_changes_after_read(self):
        fx = self.fx
        real, done = os.read, []
        with self.history_fd() as match:
            def read(fd, count):
                data = real(fd, count)
                if match(fd) and data and not done:
                    done.append(True)
                    before = os.stat(fx.historical)
                    os.utime(fx.historical, ns=(before.st_atime_ns, before.st_mtime_ns + 1_000_000_000))
                return data
            with mock.patch.object(os, 'read', read):
                observed = self.main(*fx.check_plans_args())
                self.assert_refused(observed, fx.historical, 'changed while it was read')

    def test_historical_short_read_refuses(self):
        fx = self.fx
        fx.rewrite(fx.historical, f'file\tline\told_text\ndocs/a.md\t2\t{fx.old}\n'.encode())
        fx.rewrite(fx.repairs, (plan.REPAIR_HEADER + '\n').encode())
        real = os.read
        with self.history_fd() as match:
            def read(fd, count):
                data = real(fd, count)
                return b'file\tline\told_text\n' if match(fd) and data else data
            with mock.patch.object(os, 'read', read):
                observed = self.main(*fx.check_plans_args())
                self.assert_refused(observed, fx.historical, 'read 19 bytes, scanned')

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


    test_clean_repairs_exit_0_with_no_findings = plan.CheckPlans.test_clean_repairs_exit_0_with_no_findings
    test_an_occurrence_with_no_row_exits_1_with_the_core_findings = (
        plan.CheckPlans.test_an_occurrence_with_no_row_exits_1_with_the_core_findings)


if __name__ == "__main__":
    unittest.main()
