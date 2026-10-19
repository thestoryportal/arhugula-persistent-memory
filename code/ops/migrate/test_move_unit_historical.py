"""T347: historical reader coverage and the shared fd-safe input boundary."""
import contextlib
import errno
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

    def test_parent_moved_after_scan_before_open(self):
        fx = self.fx
        parent = os.path.dirname(fx.historical)
        moved = parent + '-parked-by-review'
        original_stat, original_open = os.lstat, os.open
        attacked, opened = [], []

        def lstat(path, *args, **kwargs):
            result = original_stat(path, *args, **kwargs)
            if path == 'historical.tsv' and not attacked:
                os.rename(parent, moved)
                attacked.append(True)
            return result

        def open_(path, *args, **kwargs):
            fd = original_open(path, *args, **kwargs)
            if path == 'historical.tsv' and attacked:
                opened.append(True)
                os.rename(moved, parent)
            return fd

        try:
            with mock.patch.object(os, 'lstat', lstat), mock.patch.object(os, 'open', open_):
                observed = self.main(*fx.check_plans_args())
            self.assertEqual(len(attacked), 1)
            self.assert_refused(observed, parent, 'is held at')
        finally:
            if os.path.exists(moved):
                os.rename(moved, parent)

    def test_fifo_swapped_between_scan_and_open(self):
        fx = self.fx
        try:
            with plan.FK.fifo_in_place(fx.historical, name='open', n=1,
                                      match=plan.named('historical.tsv'), timeout=0.5) as fault:
                observed = self.main(*fx.check_plans_args())
            self.assertEqual(fault.fired, 1)
            self.assert_refused(observed, fx.historical, 'changed between scan and open')
        except plan.FK.AttackTimeout as exc:
            self.fail('historical open blocked on swapped FIFO: ' + str(exc))

    def test_historical_syscall_oserrors(self):
        for target in ('read', 'fstat', 'close'):
            for err in plan.FK.ERRNOS:
                with self.subTest(target=target, err=err), self.history_fd() as match:
                    with plan.FK.inject_oserror(target, 1, err, match=match):
                        result = self.main(*self.fx.check_plans_args())
                    self.assert_refused(result, self.fx.historical, '[' + errno.errorcode[err] + ']')

    def test_historical_unexpected_propagates(self):
        for target in ('open', 'read', 'fstat', 'close'):
            for exc in plan.FK.UNEXPECTED:
                with self.subTest(target=target, exc=exc), self.history_fd() as fdmatch:
                    match = plan.named('historical.tsv') if target == 'open' else fdmatch
                    with plan.FK.raise_unexpected(target, 1, exc, match=match):
                        with self.assertRaises(exc):
                            self.main(*self.fx.check_plans_args())

    def test_historical_short_chunks_are_read_to_eof(self):
        self.historical_row()
        self.fx.rewrite(self.fx.repairs, (plan.REPAIR_HEADER + "\n").encode())
        real = os.read
        with self.history_fd() as match:
            def read(fd, count):
                return real(fd, 3 if match(fd) else count)
            with mock.patch.object(os, "read", read):
                self.assertEqual(self.main(*self.argv()), (0, "[]\n", ""))

    def isolated_history(self):
        parent = self.fx.mk("isolated-history")
        target = os.path.join(parent, "historical.tsv")
        os.rename(self.fx.historical, target)
        self.fx.historical = target
        return parent

    @contextlib.contextmanager
    def historical_parent_fd(self, parent):
        real, fds = os.open, set()
        def opened(first, *args, **kwargs):
            fd = real(first, *args, **kwargs)
            if first == parent:
                fds.add(fd)
            else:
                fds.discard(fd)
            return fd
        with mock.patch.object(os, "open", opened):
            yield lambda fd, *a, **kw: fd in fds

    def test_historical_parent_syscall_errors_name_parent_and_errno(self):
        parent = self.isolated_history()
        # [LAW:behavior-not-structure] Each fault is confined to this input's own parent.
        calls = (("open", 1), (plan.GETPATH, 1), (plan.GETPATH, 2),
                 (plan.GETPATH, 3), ("fstat", 1), ("fstat", 2), ("close", 1))
        for target, n in calls:
            for err in plan.FK.ERRNOS:
                with self.subTest(target=target, n=n, err=err), self.historical_parent_fd(parent) as fdmatch:
                    match = plan.named(parent) if target == "open" else fdmatch
                    with plan.FK.inject_oserror(target, n, err, match=match):
                        observed = self.main(*self.argv())
                    self.assert_refused(observed, parent, "[" + errno.errorcode[err] + "]")
        for err in plan.FK.ERRNOS:
            with self.subTest(target="stat", err=err):
                real, seen = os.stat, []
                def stat_(first, *args, **kwargs):
                    if first == parent and "dir_fd" not in kwargs:
                        seen.append(first)
                        raise OSError(err, os.strerror(err))
                    return real(first, *args, **kwargs)
                with mock.patch.object(os, "stat", stat_):
                    observed = self.main(*self.argv())
                self.assertEqual(seen, [parent])
                self.assert_refused(observed, parent, "[" + errno.errorcode[err] + "]")

    def test_historical_parent_link_component_refuses_its_real_path(self):
        outer = self.fx.mk("history-ancestor")
        parent = os.path.join(outer, "parent")
        os.mkdir(parent)
        target = os.path.join(parent, "historical.tsv")
        os.rename(self.fx.historical, target)
        self.fx.historical = target
        os.rename(outer, outer + ".real")
        os.symlink(outer + ".real", outer)
        self.assert_refused(self.main(*self.argv()), parent, "is not its own real path")

    def test_historical_parent_final_component_symlink_refuses_at_open(self):
        parent = self.isolated_history()
        with plan.FK.swap_for_symlink("open", 1, parent, self.fx.other,
                                      match=plan.named(parent)) as fault:
            observed = self.main(*self.argv())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(observed, parent)
        self.assertRegex(observed[2], r"\[(ENOTDIR|ELOOP)\]$")

    def test_historical_parent_fifo_refuses_without_blocking(self):
        parent = self.isolated_history()
        try:
            with plan.FK.fifo_in_place(parent, timeout=0.5) as fault:
                observed = self.main(*self.argv())
            self.assertEqual(fault.fired, 1)
            self.assert_refused(observed, parent, "[ENOTDIR]")
        except plan.FK.AttackTimeout as exc:
            self.fail("historical parent open blocked on FIFO: " + str(exc))

    def test_historical_parent_removed_and_remade_refuses_identity(self):
        parent = self.isolated_history()
        aside = os.path.join(self.fx.other, "historical.tsv")
        def remake():
            os.rename(self.fx.historical, aside)
            os.rmdir(parent)
            os.mkdir(parent)
            os.rename(aside, self.fx.historical)
        with plan.after_open_then("historical.tsv", remake):
            observed = self.main(*self.argv())
        self.assert_refused(observed, parent, "was moved during the run")

    def test_shared_leaf_attack_cases_include_historical(self):
        # [LAW:verifiable-goals] The shared attack catalogue must exercise the new input too.
        cases = plan.Attacks.cases(self, {"check-plans": plan.LEAVES["check-plans"]})
        paths = [(fx.historical, path) for fx, path, _ in cases]
        self.assertTrue(any(historical == path for historical, path in paths), paths)

    test_relative_root_and_inputs_are_read_from_the_cwd = (
        plan.CheckPlans.test_relative_root_and_inputs_are_read_from_the_cwd)
    test_call_class_errors_name_the_path_and_errno = plan.Attacks.test_call_class_errors_name_the_path_and_errno
    test_identity_check_errors_name_the_path_and_errno = (
        plan.HeldIdentity.test_identity_check_errors_name_the_path_and_errno)
    test_check_plans_opens_only_its_inputs_to_read_and_changes_nothing = (
        plan.ReadOnly.test_check_plans_opens_only_its_inputs_to_read_and_changes_nothing)
    opened = plan.ReadOnly.opened
    check = plan.ReadOnly.check


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
