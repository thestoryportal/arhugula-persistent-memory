"""T383: exercise the CLI against real files, processes and fd attacks."""
import contextlib
import errno
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe, notebook_compare_core as core


def named(path):
    return lambda first, *args, **kwargs: first == path


class NotebookCompare(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("ops.migrate.notebook_compare"),
                             "T383 CLI is not implemented")
        self.cli = importlib.import_module("ops.migrate.notebook_compare")
        with fdsafe.fs(tempfile.gettempdir()):
            self.base = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(self.cleanup)
        with fdsafe.hold_root(self.base) as root:
            for name in ("checkpoints", "live", "inputs", "outputs", "guard"):
                with fdsafe.mkdir(root, name):
                    pass
        self.cp = os.path.join(self.base, "checkpoints", "a-checkpoint.ipynb")
        self.live = os.path.join(self.base, "live", "a.ipynb")
        self.pairs = os.path.join(self.base, "inputs", "input.tsv")
        self.out = os.path.join(self.base, "outputs", "result")
        self.data = self.notebook("same")
        self.put(self.cp, self.data)
        self.put(self.live, self.data)
        self.rows = [(self.cp, self.data, self.live, self.data)]
        self.write_pairs()

    def cleanup(self):
        with fdsafe.fs(self.base):
            shutil.rmtree(self.base)

    @staticmethod
    def notebook(*sources):
        return json.dumps({"cells": [{"cell_type": "code", "source": s}
                                     for s in sources]}).encode()

    def put(self, path, data):
        with fdsafe.hold_root(os.path.dirname(path)) as parent, \
                fdsafe.hold_root(os.path.join(self.base, "guard")) as guard:
            fdsafe.create_file(parent, os.path.basename(path), data, [guard])

    def read(self, path):
        with fdsafe.hold_root(os.path.dirname(path)) as parent:
            return fdsafe.read_named(parent, os.path.basename(path))

    def exists(self, path):
        with fdsafe.fs(path):
            return os.path.lexists(path)

    def names(self, path):
        with fdsafe.fs(path):
            return sorted(os.listdir(path))

    def write_pairs(self, data=None):
        if self.exists(self.pairs):
            with fdsafe.fs(self.pairs):
                os.unlink(self.pairs)
        if data is None:
            data = ("checkpoint\tlive\n" + "".join(
                f"{cp}\t{live}\n" for cp, _, live, _ in self.rows)).encode()
        self.put(self.pairs, data)

    def call(self, argv=None):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = self.cli.main(["--pairs", self.pairs, "--out", self.out]
                               if argv is None else argv)
        return rc, out.getvalue(), err.getvalue()

    def refused(self, path, err=None, created=False):
        rc, out, message = self.call()
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")
        self.assertEqual(len(message.splitlines()), 1)
        self.assertIn(path, message)
        if err is not None:
            self.assertIn(errno.errorcode[err], message)
        if not created:
            self.assertFalse(self.exists(self.out))
        return message

    def outputs(self):
        pairs, cells = [], []
        for row in self.rows:
            pair, these = core.compare(*row)
            pairs.append(pair)
            cells.extend(these)
        self.assertEqual(self.names(self.out), ["cells.tsv", "pairs.tsv"])
        self.assertEqual(self.read(os.path.join(self.out, "pairs.tsv")),
                         core.render(core.PAIR_FIELDS, pairs))
        self.assertEqual(self.read(os.path.join(self.out, "cells.tsv")),
                         core.render(core.CELL_FIELDS, cells))

    def test_end_to_end_order_and_bytes(self):
        for name, cpdata, livedata in (("b", self.notebook("same", "unique"), self.data),
                                       ("c", self.notebook("orphan"), None)):
            cp = os.path.join(os.path.dirname(self.cp), name + "-checkpoint.ipynb")
            live = os.path.join(os.path.dirname(self.live), name + ".ipynb")
            self.put(cp, cpdata)
            if livedata is not None:
                self.put(live, livedata)
            self.rows.append((cp, cpdata, live, livedata))
        self.rows.reverse()
        self.write_pairs()
        self.assertEqual(self.call(), (0, "3 pairs: 1 exact, 1 differing, 1 unmatched; 2 unique cells\n", ""))
        self.outputs()

    def test_compare_calls_and_tsv_rows_follow_file_order(self):
        for name in ("b", "c"):
            cp = os.path.join(os.path.dirname(self.cp), name + "-checkpoint.ipynb")
            live = os.path.join(os.path.dirname(self.live), name + ".ipynb")
            data = self.notebook(name)
            self.put(cp, data)
            self.put(live, self.data)
            self.rows.append((cp, data, live, self.data))
        self.rows = [self.rows[2], self.rows[0], self.rows[1]]
        self.write_pairs()
        expected = [row[0] for row in self.rows]
        with mock.patch.object(core, "compare", wraps=core.compare) as compare:
            self.assertEqual(self.call(), (
                0, "3 pairs: 1 exact, 2 differing, 0 unmatched; 2 unique cells\n", ""))
        self.assertEqual([call.args[0] for call in compare.call_args_list], expected)
        for name in ("pairs.tsv", "cells.tsv"):
            with self.subTest(output=name):
                lines = self.read(os.path.join(self.out, name)).decode().splitlines()
                self.assertEqual([line.split("\t")[0] for line in lines[1:]], expected)
        self.outputs()

    def test_invalid_pairs(self):
        header = b"checkpoint\tlive\n"
        good = f"{self.cp}\t{self.live}\n".encode()
        cases = [(header + good[:-1], 2), (b"wrong\tlive\n" + good, 1),
                 (header + b"/one\n", 2), (header + b"/a\t/b\t/c\n", 2),
                 (header + good + good, 3), (header, 2),
                 (header + b"\xff\t/a\n", 2), (b"", 1)]
        for bad in ("relative", "/a/../b", "/a//b", "/a/", ""):
            for cp, live in ((bad, self.live), (self.cp, bad)):
                cases.append((header + f"{cp}\t{live}\n".encode(), 2))
        for data, line in cases:
            with self.subTest(data=data):
                self.write_pairs(data)
                self.assertIn(f"line {line}", self.refused(self.pairs))

    def nul_path_refused(self, column, position):
        original = (self.cp, self.live)[column]
        parent, name = os.path.split(original)
        values = {
            "start": "\0" + original,
            "middle": original[:len(original) // 2] + "\0" + original[len(original) // 2:],
            "end": original + "\0",
            "parent": parent + "\0/" + name,
            "name": parent + "/\0" + name,
        }
        for line in (2, 3):
            with self.subTest(line=line):
                fields = [self.cp, self.live]
                fields[column] = values[position]
                prefix = f"{self.cp}\t{self.live}\n" if line == 3 else ""
                self.write_pairs(("checkpoint\tlive\n" + prefix +
                                  "\t".join(fields) + "\n").encode())
                message = self.refused(self.pairs)
                self.assertEqual(message, str(fdsafe.Refusal(
                    self.pairs, f"line {line}: NUL byte in a path")) + "\n")
                self.assertNotIn("Traceback", message)

    def test_nul_checkpoint_start(self):
        self.nul_path_refused(0, "start")

    def test_nul_checkpoint_middle(self):
        self.nul_path_refused(0, "middle")

    def test_nul_checkpoint_end(self):
        self.nul_path_refused(0, "end")

    def test_nul_checkpoint_parent(self):
        self.nul_path_refused(0, "parent")

    def test_nul_checkpoint_name(self):
        self.nul_path_refused(0, "name")

    def test_nul_live_start(self):
        self.nul_path_refused(1, "start")

    def test_nul_live_middle(self):
        self.nul_path_refused(1, "middle")

    def test_nul_live_end(self):
        self.nul_path_refused(1, "end")

    def test_nul_live_parent(self):
        self.nul_path_refused(1, "parent")

    def test_nul_live_name(self):
        self.nul_path_refused(1, "name")

    def process(self, argv):
        worktree = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))))
        script = os.path.join(worktree, "code", "ops", "migrate", "notebook_compare.py")
        env = dict(os.environ, PYTHONPATH="code/tests:code")
        return subprocess.run([sys.executable, "-B", script, *argv], cwd=worktree,
                              env=env, capture_output=True, text=True, timeout=15)

    def test_cli_success(self):
        result = self.process(["--pairs", self.pairs, "--out", self.out])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout,
                         "1 pairs: 1 exact, 0 differing, 0 unmatched; 0 unique cells\n")
        self.assertEqual(result.stderr, "")
        self.outputs()

    def test_cli_refusal(self):
        self.write_pairs(b"checkpoint\tlive\n")
        result = self.process(["--pairs", self.pairs, "--out", self.out])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, str(fdsafe.Refusal(
            self.pairs, "line 2: expected at least one pair")) + "\n")
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.exists(self.out))

    def test_cli_missing_out(self):
        result = self.process(["--pairs", self.pairs])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("usage:", result.stderr)
        self.assertIn("required: --out", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.exists(self.out))

    def test_pairs_header_is_exact(self):
        for header in ("checkpoint-extra\tlive", "CHECKPOINT\tLIVE"):
            with self.subTest(header=header):
                self.write_pairs(f"{header}\n{self.cp}\t{self.live}\n".encode())
                self.assertIn("line 1:", self.refused(self.pairs))

    def test_pairs_invalid_utf8_in_absolute_path(self):
        live_parent = os.path.dirname(self.live).encode()
        self.write_pairs(b"checkpoint\tlive\n" + self.cp.encode() + b"\t" +
                         live_parent + b"/invalid-\xff.ipynb\n")
        self.assertIn("line 2:", self.refused(self.pairs))

    def test_live_enotdir_and_eacces_are_refusals(self):
        real = fdsafe.read_named
        for err in (errno.ENOTDIR, errno.EACCES):
            with self.subTest(err=err):
                def attacked(held, name):
                    if os.path.join(held.path, name) == self.live:
                        with mock.patch.object(os, "open", side_effect=OSError(
                                err, os.strerror(err))):
                            return real(held, name)
                    return real(held, name)
                with mock.patch.object(fdsafe, "read_named", side_effect=attacked):
                    self.refused(self.live, err)

    def test_summary_sums_unique_cells(self):
        cp = os.path.join(os.path.dirname(self.cp), "b-checkpoint.ipynb")
        live = os.path.join(os.path.dirname(self.live), "b.ipynb")
        data = self.notebook("first unique", "second unique", "third unique")
        self.put(cp, data)
        self.put(live, self.data)
        self.rows.append((cp, data, live, self.data))
        self.write_pairs()
        self.assertEqual(self.call(),
                         (0, "2 pairs: 1 exact, 1 differing, 0 unmatched; 3 unique cells\n", ""))
        self.outputs()

    def test_checkpoint_identity_controls_duplicates(self):
        other_live = os.path.join(os.path.dirname(self.live), "b.ipynb")
        self.write_pairs((f"checkpoint\tlive\n{self.cp}\t{self.live}\n"
                          f"{self.cp}\t{other_live}\n").encode())
        self.assertIn("line 3:", self.refused(self.pairs))
        other_cp = os.path.join(os.path.dirname(self.cp), "b-checkpoint.ipynb")
        self.put(other_cp, self.data)
        self.rows.append((other_cp, self.data, self.live, self.data))
        self.write_pairs()
        self.assertEqual(self.call(),
                         (0, "2 pairs: 2 exact, 0 differing, 0 unmatched; 0 unique cells\n", ""))
        self.outputs()

    def test_absent_live_is_unmatched(self):
        with fdsafe.fs(self.live):
            os.unlink(self.live)
        self.rows = [(self.cp, self.data, self.live, None)]
        self.assertEqual(self.call(), (0, "1 pairs: 0 exact, 0 differing, 1 unmatched; 1 unique cells\n", ""))
        self.outputs()

    def test_missing_parent_is_not_absent_live(self):
        missing = os.path.join(self.base, "missing")
        self.rows = [(self.cp, self.data, os.path.join(missing, "a.ipynb"), None)]
        self.write_pairs()
        self.refused(missing, errno.ENOENT)

    def test_missing_checkpoint(self):
        with fdsafe.fs(self.cp):
            os.unlink(self.cp)
        self.refused(self.cp, errno.ENOENT)

    def test_symlink_notebook(self):
        with fdsafe.fs(self.live):
            os.unlink(self.live)
            os.symlink(self.cp, self.live)
        self.refused(self.live)

    def test_fifo_notebook(self):
        with fdsafe.fs(self.live), FK.fifo_in_place(self.live, timeout=5):
            self.refused(self.live)

    def test_symlink_swap_at_pairs_and_notebook_open(self):
        for path in (self.pairs, self.live):
            with self.subTest(path=path), fdsafe.fs(path), FK.swap_for_symlink(
                    "open", 1, path, self.cp, match=named(os.path.basename(path))) as fault:
                self.refused(path, errno.ELOOP)
            with fdsafe.fs(path):
                os.unlink(path)
                os.rename(fault.parked, path)

    def test_notebook_parent_rebound(self):
        parent = os.path.dirname(self.live)
        real = fdsafe.read_named

        def attacked(held, name):
            if held.path == parent:
                with fdsafe.fs(parent), FK.rename_and_rebind(
                        FK.GETPATH, 1, parent, match=named(held.fd)):
                    return real(held, name)
            return real(held, name)
        with mock.patch.object(fdsafe, "read_named", side_effect=attacked):
            self.refused(parent)

    def test_read_oserrors(self):
        real = fdsafe.read_named
        for path in (self.pairs, self.cp, self.live):
            for op in ("open", "read", "fstat", "close", FK.GETPATH):
                for err in (errno.EIO, errno.EBADF):
                    with self.subTest(path=path, op=op, err=err):
                        def attacked(held, name):
                            if os.path.join(held.path, name) == path:
                                with FK.inject_oserror(op, 1, err):
                                    return real(held, name)
                            return real(held, name)
                        with mock.patch.object(fdsafe, "read_named", side_effect=attacked):
                            self.refused(os.path.dirname(path) if op == FK.GETPATH else path, err)

    def test_existing_out_file(self):
        self.put(self.out, b"keep")
        self.refused(self.out, errno.EEXIST, created=True)
        self.assertEqual(self.read(self.out), b"keep")

    def test_existing_out_directory(self):
        with fdsafe.hold_root(os.path.dirname(self.out)) as parent:
            with fdsafe.mkdir(parent, os.path.basename(self.out)):
                pass
        kept = os.path.join(self.out, "keep")
        self.put(kept, b"keep")
        self.refused(self.out, errno.EEXIST, created=True)
        self.assertEqual(self.names(self.out), ["keep"])
        self.assertEqual(self.read(kept), b"keep")

    def test_out_parent_inside_input_refuses_before_mkdir(self):
        for path in (self.cp, self.live, self.pairs):
            for nested in (False, True):
                with self.subTest(path=path, nested=nested):
                    parent = os.path.dirname(path)
                    if nested:
                        with fdsafe.hold_root(parent) as held:
                            with fdsafe.mkdir(held, "nested") as child:
                                parent = child.path
                    self.out = os.path.join(parent, "result")
                    self.refused(self.out)

    def test_short_writes(self):
        with FK.one_byte_writes():
            self.assertEqual(self.call(), (0, "1 pairs: 1 exact, 0 differing, 0 unmatched; 0 unique cells\n", ""))
        self.outputs()

    def test_output_write_error_keeps_file(self):
        kept = os.path.join(self.out, "pairs.tsv")
        with FK.inject_oserror("write", 1, errno.EIO):
            message = self.refused(kept, errno.EIO, created=True)
        self.assertIn("left in place", message)
        self.assertEqual(self.names(self.out), ["pairs.tsv"])
        self.assertEqual(self.read(kept), b"")

    def test_output_directory_rebound_keeps_files(self):
        with fdsafe.fs(self.out), FK.rename_and_rebind("write", 1, self.out) as fault:
            self.refused(self.out, created=True)
        self.assertEqual(self.names(self.out), [])
        self.assertEqual(self.names(fault.parked), ["pairs.tsv"])
        pair, _ = core.compare(*self.rows[0])
        self.assertEqual(self.read(os.path.join(fault.parked, "pairs.tsv")),
                         core.render(core.PAIR_FIELDS, [pair]))

    def test_unexpected_notebook_read_errors_propagate(self):
        real = fdsafe.read_named
        for exc in FK.UNEXPECTED:
            with self.subTest(exc=exc):
                def attacked(held, name):
                    if held.path == os.path.dirname(self.live):
                        with FK.raise_unexpected("read", 1, exc):
                            return real(held, name)
                    return real(held, name)
                with mock.patch.object(fdsafe, "read_named", side_effect=attacked):
                    with self.assertRaises(exc) as caught:
                        self.call()
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)
                self.assertFalse(self.exists(self.out))

    def deleted_cwd(self):
        with fdsafe.fs(self.base):
            original = os.getcwd()
            deleted = os.path.realpath(tempfile.mkdtemp(dir=self.base))
        def restore():
            with fdsafe.fs(original):
                os.chdir(original)
        self.addCleanup(restore)
        with fdsafe.fs(deleted):
            os.chdir(deleted)
            os.rmdir(deleted)
        return deleted

    def test_relative_out_deleted_cwd(self):
        deleted = self.deleted_cwd()
        rc, out, message = self.call(["--pairs", self.pairs, "--out", "result"])
        self.assertEqual((rc, out), (1, ""))
        self.assertEqual(len(message.splitlines()), 1)
        self.assertIn("result", message)
        self.assertIn("ENOENT", message)
        self.assertNotIn("Traceback", message)
        self.assertFalse(self.exists(os.path.join(deleted, "result")))
        self.assertFalse(self.exists(self.out))

    def test_relative_pairs_deleted_cwd(self):
        self.deleted_cwd()
        rc, out, message = self.call(["--pairs", "input.tsv", "--out", self.out])
        self.assertEqual((rc, out), (1, ""))
        self.assertEqual(len(message.splitlines()), 1)
        self.assertIn("input.tsv", message)
        self.assertIn("ENOENT", message)
        self.assertNotIn("Traceback", message)
        self.assertFalse(self.exists(self.out))

    def test_directory_boundary_oserrors(self):
        for function, op, path in (("hold_root", "open", os.path.dirname(self.pairs)),
                                   ("open_out_parent", "open", os.path.dirname(self.out)),
                                   ("mkdir", "mkdir", self.out)):
            real = getattr(fdsafe, function)
            with self.subTest(function=function):
                def attacked(*args, **kwargs):
                    with FK.inject_oserror(op, 1, errno.EIO):
                        return real(*args, **kwargs)
                with mock.patch.object(fdsafe, function, side_effect=attacked):
                    self.refused(path, errno.EIO)

    def test_output_parent_and_root_live_oserrors(self):
        for path in (os.path.dirname(self.out), os.path.dirname(self.pairs)):
            armed = False
            compare = core.compare
            live = fdsafe.Dir.live
            def compared(*args):
                nonlocal armed
                result = compare(*args)
                armed = True
                return result
            def attacked(held):
                if armed and held.path == path:
                    with FK.inject_oserror(FK.GETPATH, 1, errno.EIO):
                        return live(held)
                return live(held)
            with self.subTest(path=path), mock.patch.object(core, "compare", compared), \
                    mock.patch.object(fdsafe.Dir, "live", attacked):
                self.refused(path, errno.EIO)

    def test_final_output_live_path_oserror(self):
        real = fdsafe.live_path
        create = fdsafe.create_file
        armed = False
        def created(*args):
            nonlocal armed
            result = create(*args)
            armed = True
            return result
        def attacked(fd, path):
            if armed and path == f"{self.out}/pairs.tsv (created, left in place)":
                with FK.inject_oserror(FK.GETPATH, 1, errno.EIO):
                    return real(fd, path)
            return real(fd, path)
        with mock.patch.object(fdsafe, "create_file", side_effect=created), \
                mock.patch.object(fdsafe, "live_path", side_effect=attacked):
            self.refused(os.path.join(self.out, "pairs.tsv"), errno.EIO, created=True)

    def test_held_directory_close_oserror(self):
        real = fdsafe.Dir.close
        def attacked(held):
            if held.path == self.out:
                with FK.inject_oserror("close", 1, errno.EIO):
                    return real(held)
            return real(held)
        with mock.patch.object(fdsafe.Dir, "close", attacked):
            self.refused(self.out, errno.EIO, created=True)

    def test_usage(self):
        for argv in ([], ["--pairs", self.pairs], ["--out", self.out]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit) as caught:
                self.call(argv)
            self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
