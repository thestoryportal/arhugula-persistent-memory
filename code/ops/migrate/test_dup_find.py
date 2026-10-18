"""Tests for dup_find: the I/O shell of Step 205 over dup_find_core (Step 216).

The shell reads Step 201 manifests through fdsafe and, when given, the toolkit migration.duckdb opened
READ_ONLY, and prints the core's rows unchanged. RED list for a filesystem tool: every fault_kit attack
that applies to each bound object (manifest file and its directory, DuckDB file and its directory).
The tool writes no file, so one_byte_writes, ENOSPC and output-parent attacks have no target here.
"""
from __future__ import annotations

import contextlib
import errno
import hashlib
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import duckdb

import fault_kit as FK
from ops.migrate import dup_find, dup_find_core, fdsafe, unit_manifest

GETPATH = FK.GETPATH
CODE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOL = os.path.join(CODE, "ops", "migrate", "dup_find.py")
_INODES = itertools.count(500)
U, R1, R2 = "/v/unit", "/p/ref1", "/p/ref2"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def leaf(root: str, rel: str, data: bytes) -> dict:
    return {"source": f"{root}/{rel}", "kind": "file", "bytes": len(data), "sha256": sha(data),
            "link_text": None, "device": 16777230, "inode": next(_INODES), "nlink": 1}


def manifest(root: str, *leaves: dict) -> dict:
    return {"schema_version": 1, "root": root, "leaves": list(leaves)}


def named(path):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == path


@contextlib.contextmanager
def lstat_error(err, n):
    """fault_kit has no lstat target: raise OSError(err) at the Nth os.lstat call."""
    real, calls = os.lstat, [0]

    def hooked(*args, **kwargs):
        calls[0] += 1
        if calls[0] == n:
            raise OSError(err, os.strerror(err))
        return real(*args, **kwargs)
    with mock.patch.object(os, "lstat", hooked):
        yield calls


@contextlib.contextmanager
def before_connect(action):
    """Run action() just before DuckDB opens the database (the race window of a path-based open)."""
    real = duckdb.connect

    def hooked(*args, **kwargs):
        action()
        return real(*args, **kwargs)
    with mock.patch.object(duckdb, "connect", hooked):
        yield


WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
_opens: list | None = None  # the "open" audit events while recording_opens runs; None outside it


def _audit(event, args):
    if event == "open" and _opens is not None:
        _opens.append(args)


sys.addaudithook(_audit)  # an audit hook cannot be removed, so it records only inside recording_opens


@contextlib.contextmanager
def recording_opens():
    """Record every Python-level open (open, io.open, os.open, pathlib) in the block as (path, mode, flags)."""
    global _opens
    _opens = []
    try:
        yield _opens
    finally:
        _opens = None


def opens_to_write(events) -> list:
    """The events that can write or create: a mode with w, a, x or +, or flags with a write or create bit."""
    return [(path, mode, flags) for path, mode, flags in events
            if (isinstance(mode, str) and set(mode) & set("wax+")) or (isinstance(flags, int) and flags & WRITE_FLAGS)]


def tree_state(root: str) -> list:
    """Every entry under root, root included, with its type, size, mtime and inode; links are not followed."""
    state = []
    for top, dirs, files in os.walk(root):
        for path in [top] + [os.path.join(top, name) for name in dirs + files]:
            st = os.lstat(path)
            state.append((os.path.relpath(path, root), st.st_mode, st.st_size, st.st_mtime_ns, st.st_ino))
    return sorted(set(state))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="dupfind"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.mdir = self.mkdir("manifests")
        self.ddir = self.mkdir("db")
        self.unit = manifest(U, leaf(U, "a/same.json", b"same"), leaf(U, "b/diff.txt", b"new"),
                             leaf(U, "c/only.txt", b"only"))
        self.ref = manifest(R1, leaf(R1, "elsewhere/same.json", b"same"), leaf(R1, "b/diff.txt", b"old"))
        self.unit_path = self.write_json("unit.json", self.unit)
        self.ref_path = self.write_json("ref.json", self.ref)

    def mkdir(self, rel: str) -> str:
        path = os.path.join(self.tmp, rel)
        os.makedirs(path)
        return path

    def write(self, path: str, data: bytes) -> str:
        with open(path, "xb") as fh:
            fh.write(data)
        return path

    def write_json(self, name: str, obj) -> str:
        return self.write(os.path.join(self.mdir, name), json.dumps(obj).encode("utf-8"))

    def make_db(self, rows, name="migration.duckdb", table="inventory") -> str:
        path = os.path.join(self.ddir, name)
        with duckdb.connect(path) as con:
            con.execute(f"CREATE TABLE {table} (id BIGINT, abspath VARCHAR, size BIGINT, sha256 VARCHAR)")
            for i, (p, s) in enumerate(rows):
                con.execute(f"INSERT INTO {table} VALUES (?, ?, 0, ?)", [i, p, s])
        return path

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = dup_find.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def args(self, db=None):
        argv = ["--unit", self.unit_path, "--reference", self.ref_path]
        return argv + ([] if db is None else ["--toolkit-db", db])

    def assert_refused(self, result, path, *words):
        code, out, err = result
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(len(err.splitlines()), 1, err)
        self.assertNotIn("Traceback", err)
        self.assertIn(repr(path), err)
        for word in words:
            self.assertIn(word, err)


class Compare(Base):
    def test_rows_are_the_core_result_unchanged(self):
        code, out, err = self.main(*self.args())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out), dup_find_core.classify(self.unit, [self.ref]))
        rows = {row["relpath"]: row["class"] for row in json.loads(out)}
        self.assertEqual(rows, {"a/same.json": "equal", "b/diff.txt": "differing", "c/only.txt": "unique"})

    def test_output_is_one_canonical_json_line_with_no_action(self):
        code, out, err = self.main(*self.args())
        rows = dup_find_core.classify(self.unit, [self.ref])
        self.assertEqual(out, json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
        for row in json.loads(out):
            self.assertFalse({"action", "delete", "purge", "skip"} & row.keys())

    def test_every_reference_is_compared(self):
        ref2 = manifest(R2, leaf(R2, "x/only.txt", b"only"))
        path2 = self.write_json("ref2.json", ref2)
        code, out, err = self.main(*self.args(), "--reference", path2)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out), dup_find_core.classify(self.unit, [self.ref, ref2]))
        self.assertEqual(json.loads(out)[2]["equal_to"], ["/p/ref2/x/only.txt"])

    def test_positive_control_overlay_equals_stage_tree_from_step_201_manifests(self):
        overlay, stage = self.mkdir("S/L01"), self.mkdir("P/stage_1_sect")
        for root in (overlay, stage):
            os.makedirs(os.path.join(root, "sect"))
            self.write(os.path.join(root, "sect", "layer_7.json"), b'{"layer": 7}')
            self.write(os.path.join(root, "notes.md"), b"overlay notes\n")
        paths = []
        for root, name in ((overlay, "l01.json"), (stage, "stage.json")):
            out = os.path.join(self.mdir, name)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(unit_manifest.main(["--root", root, "--out", out]), 0)
            paths.append(out)
        code, out, err = self.main("--unit", paths[0], "--reference", paths[1])
        self.assertEqual((code, err), (0, ""))
        rows = json.loads(out)
        self.assertEqual([row["class"] for row in rows], ["equal", "equal"])
        self.assertEqual([row["equal_to"] for row in rows],
                         [[os.path.join(stage, "notes.md")], [os.path.join(stage, "sect", "layer_7.json")]])

    def test_cli_prints_rows_and_exits_0(self):
        env = dict(os.environ, PYTHONPATH=CODE)
        proc = subprocess.run([sys.executable, "-B", TOOL, *self.args()], capture_output=True, text=True, env=env)
        self.assertEqual((proc.returncode, proc.stderr), (0, ""))
        self.assertEqual(json.loads(proc.stdout), dup_find_core.classify(self.unit, [self.ref]))

    def test_cli_refusal_is_one_line_exit_2_without_traceback(self):
        env = dict(os.environ, PYTHONPATH=CODE)
        missing = os.path.join(self.mdir, "missing.json")
        proc = subprocess.run([sys.executable, "-B", TOOL, "--unit", missing, "--reference", self.ref_path],
                              capture_output=True, text=True, env=env)
        self.assertEqual((proc.returncode, proc.stdout), (2, ""))
        self.assertEqual(proc.stderr, f"{missing!r}: No such file or directory [ENOENT]\n")


class ToolkitHints(Base):
    def test_hints_come_from_the_db_and_never_change_the_class(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same")), ("/v/unit/b/diff.txt", sha(b"stale")),
                           ("/v/unit/c/only.txt", None), ("/elsewhere/x", sha(b"x"))])
        code, out, err = self.main(*self.args(db))
        self.assertEqual((code, err), (0, ""))
        hints = [{"path": "/elsewhere/x", "sha256": sha(b"x")}, {"path": "/v/unit/a/same.json", "sha256": sha(b"same")},
                 {"path": "/v/unit/b/diff.txt", "sha256": sha(b"stale")}]
        self.assertEqual(json.loads(out), dup_find_core.classify(self.unit, [self.ref], hints))
        self.assertEqual([row["hint"] for row in json.loads(out)],
                         [{"sha256": sha(b"same"), "agrees": True}, {"sha256": sha(b"stale"), "agrees": False}, None])
        self.assertEqual([row["class"] for row in json.loads(out)], ["equal", "differing", "unique"])

    def test_no_db_gives_no_hints(self):
        code, out, err = self.main(*self.args())
        self.assertEqual([row["hint"] for row in json.loads(out)], [None, None, None])

    def test_db_is_opened_read_only_and_nothing_is_created_beside_it(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same"))])
        os.chmod(db, 0o444)
        before = sorted(os.listdir(self.ddir)), os.lstat(db)
        code, out, err = self.main(*self.args(db))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out)[0]["hint"], {"sha256": sha(b"same"), "agrees": True})
        after = sorted(os.listdir(self.ddir)), os.lstat(db)
        self.assertEqual(before[0], after[0])
        self.assertEqual(fdsafe._identity(before[1]), fdsafe._identity(after[1]))

    def test_a_duplicate_hint_path_is_the_core_refusal(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same")), ("/v/unit/a/same.json", sha(b"other"))])
        self.assert_refused(self.main(*self.args(db)), "/v/unit/a/same.json", "more than one toolkit hint")

    def test_a_file_that_is_not_a_duckdb_database_refuses(self):
        junk = self.write(os.path.join(self.ddir, "junk.duckdb"), b"not a database" * 1000)
        self.assert_refused(self.main(*self.args(junk)), junk, "DuckDB")

    def test_a_db_without_the_inventory_table_refuses(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same"))], table="other")
        self.assert_refused(self.main(*self.args(db)), db, "DuckDB", "inventory")

    def test_a_directory_in_place_of_the_db_refuses(self):
        path = self.mkdir("db/migration.duckdb")
        self.assert_refused(self.main(*self.args(path)), path, "is not a regular file")

    def test_missing_db_names_path_and_errno(self):
        path = os.path.join(self.ddir, "missing.duckdb")
        self.assert_refused(self.main(*self.args(path)), path, "[ENOENT]")

    def test_db_replaced_before_duckdb_opens_it_refuses(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same"))])
        other = self.make_db([("/v/unit/a/same.json", sha(b"forged"))], name="other.duckdb")

        def replace():
            os.rename(db, db + ".parked")
            shutil.copyfile(other, db)
        with before_connect(replace):
            result = self.main(*self.args(db))
        self.assert_refused(result, db, "changed while DuckDB read it")

    def test_db_changed_in_place_while_duckdb_reads_it_refuses(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same"))])
        st = os.lstat(db)
        with before_connect(lambda: os.utime(db, ns=(st.st_atime_ns, st.st_mtime_ns + 1000))):
            result = self.main(*self.args(db))
        self.assert_refused(result, db, "changed while DuckDB read it")

    def test_unexpected_error_from_duckdb_propagates(self):
        db = self.make_db([("/v/unit/a/same.json", sha(b"same"))])
        with mock.patch.object(duckdb, "connect", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                self.main(*self.args(db))


class ManifestRefusals(Base):
    def test_non_utf8_manifest_refuses(self):
        bad = self.write(os.path.join(self.mdir, "latin1.json"), b'{"root": "/v/caf\xe9"}')
        self.assert_refused(self.main("--unit", bad, "--reference", self.ref_path), bad, "not UTF-8 JSON")

    def test_invalid_json_refuses(self):
        bad = self.write(os.path.join(self.mdir, "bad.json"), b'{"schema_version": 1,')
        self.assert_refused(self.main("--unit", bad, "--reference", self.ref_path), bad, "not UTF-8 JSON")

    def test_duplicate_key_refuses(self):
        bad = self.write(os.path.join(self.mdir, "dup.json"),
                         json.dumps(self.unit).replace('"root"', '"root": "/elsewhere", "root"', 1).encode())
        result = self.main("--unit", bad, "--reference", self.ref_path)
        self.assert_refused(result, bad)
        self.assertEqual(result[2], f"{bad!r}: duplicate key 'root'\n")

    def test_core_refusal_exits_2_with_one_line(self):
        self.assert_refused(self.main("--unit", self.unit_path, "--reference", self.unit_path), U, "overlaps")

    def test_missing_manifest_names_path_and_errno(self):
        path = os.path.join(self.mdir, "missing.json")
        self.assert_refused(self.main("--unit", path, "--reference", self.ref_path), path, "[ENOENT]")

    def test_manifest_reached_through_a_linked_directory_refuses(self):
        link = os.path.join(self.tmp, "linked")
        os.symlink(self.tmp, link)
        parent = os.path.join(link, "manifests")
        self.assert_refused(self.main("--unit", os.path.join(parent, "unit.json"), "--reference", self.ref_path),
                            parent, "a component is a link")

    def test_manifest_that_is_a_symlink_refuses(self):
        link = os.path.join(self.mdir, "link.json")
        os.symlink(self.unit_path, link)
        self.assert_refused(self.main("--unit", link, "--reference", self.ref_path), link, "is not a regular file")

    def test_cwd_error_for_a_relative_path_names_the_path_and_errno(self):
        with mock.patch.object(os, "getcwd", side_effect=OSError(errno.EIO, os.strerror(errno.EIO))):
            result = self.main("--unit", "unit.json", "--reference", self.ref_path)
        self.assert_refused(result, "unit.json", "[EIO]")

    def test_relative_manifest_path_is_read_from_the_cwd(self):
        cwd = os.getcwd()
        os.chdir(self.mdir)
        self.addCleanup(os.chdir, cwd)
        code, out, err = self.main("--unit", "unit.json", "--reference", "ref.json")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out), dup_find_core.classify(self.unit, [self.ref]))


class ManifestAttacks(Base):
    def test_manifest_swapped_for_a_symlink_between_scan_and_open_refuses(self):
        decoy = self.write(os.path.join(self.tmp, "decoy.json"), json.dumps(self.unit).encode())
        with FK.swap_for_symlink("open", 1, self.unit_path, decoy, match=named("unit.json")):
            result = self.main(*self.args())
        self.assert_refused(result, self.unit_path, "[ELOOP]")

    def test_manifest_directory_swapped_for_a_symlink_refuses(self):
        other = self.mkdir("other")
        shutil.copyfile(self.unit_path, os.path.join(other, "unit.json"))
        with FK.swap_for_symlink("open", 1, self.mdir, other, match=named(self.mdir)):
            result = self.main(*self.args())
        self.assert_refused(result, self.mdir)
        self.assertRegex(result[2], r"\[(ENOTDIR|ELOOP)\]$")  # macOS: O_DIRECTORY on a link is ENOTDIR

    def test_fifo_in_place_of_the_manifest_refuses_without_blocking(self):
        with FK.fifo_in_place(self.unit_path):
            result = self.main(*self.args())
        self.assert_refused(result, self.unit_path, "is not a regular file")

    def test_fifo_in_place_of_the_manifest_directory_refuses_without_blocking(self):
        with FK.fifo_in_place(self.mdir):
            result = self.main(*self.args())
        self.assert_refused(result, self.mdir, "[ENOTDIR]")

    def test_manifest_directory_renamed_and_rebound_refuses(self):
        with FK.rename_and_rebind(GETPATH, 1, self.mdir, when="after"):
            result = self.main(*self.args())
        self.assert_refused(result, self.mdir, "is held at")

    def test_injected_errors_name_the_path_and_errno(self):
        cases = [("open", named(self.mdir), self.mdir), ("open", named("unit.json"), self.unit_path),
                 ("fstat", None, self.unit_path), ("read", None, self.unit_path),
                 ("close", None, self.unit_path), (GETPATH, None, self.mdir)]
        for target, match, path in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(target=target, path=path, err=err):
                    with FK.inject_oserror(target, 1, err, match=match):
                        result = self.main(*self.args())
                    self.assert_refused(result, path, f"[{errno.errorcode[err]}]")

    def test_injected_lstat_error_names_the_manifest(self):
        with lstat_error(errno.EIO, 1):
            result = self.main(*self.args())
        self.assert_refused(result, self.unit_path, "[EIO]")

    def test_directory_close_error_names_the_directory(self):
        with FK.inject_oserror("close", 2, errno.EIO):
            result = self.main(*self.args())
        self.assert_refused(result, self.mdir, "[EIO]")

    def test_unexpected_exceptions_propagate(self):
        for exc in FK.UNEXPECTED:
            with self.subTest(exc=exc.__name__):
                with FK.raise_unexpected("read", 1, exc):
                    with self.assertRaises(exc) as caught:
                        self.main(*self.args())
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


class DbAttacks(Base):
    def setUp(self):
        super().setUp()
        self.db = self.make_db([("/v/unit/a/same.json", sha(b"same"))])
        self.decoy = self.make_db([("/v/unit/a/same.json", sha(b"forged"))], name="decoy.duckdb")

    def test_db_swapped_for_a_symlink_after_its_directory_is_held_refuses(self):
        with FK.swap_for_symlink(GETPATH, 1, self.db, self.decoy, when="after"):
            result = self.main(*self.args(self.db))
        self.assert_refused(result, self.db, "is not a regular file")

    def test_db_directory_swapped_for_a_symlink_refuses(self):
        other = self.mkdir("other")
        shutil.copyfile(self.decoy, os.path.join(other, "migration.duckdb"))
        with FK.swap_for_symlink("open", 1, self.ddir, other, match=named(self.ddir)):
            result = self.main(*self.args(self.db))
        self.assert_refused(result, self.ddir)
        self.assertRegex(result[2], r"\[(ENOTDIR|ELOOP)\]$")  # macOS: O_DIRECTORY on a link is ENOTDIR

    def test_fifo_in_place_of_the_db_refuses_without_blocking(self):
        with FK.fifo_in_place(self.db):
            result = self.main(*self.args(self.db))
        self.assert_refused(result, self.db, "is not a regular file")

    def test_fifo_in_place_of_the_db_directory_refuses_without_blocking(self):
        with FK.fifo_in_place(self.ddir):
            result = self.main(*self.args(self.db))
        self.assert_refused(result, self.ddir, "[ENOTDIR]")

    def test_db_directory_renamed_and_rebound_refuses(self):
        with FK.rename_and_rebind(GETPATH, 1, self.ddir, when="after"):
            result = self.main(*self.args(self.db))
        self.assert_refused(result, self.db)

    def test_injected_errors_name_the_path_and_errno(self):
        cases = [("open", named(self.ddir), self.ddir), (GETPATH, None, self.ddir), ("close", None, self.ddir)]
        for target, match, path in cases:
            with self.subTest(target=target):
                with FK.inject_oserror(target, 1, errno.EIO, match=match):
                    result = self.main(*self.args(self.db))
                self.assert_refused(result, path, "[EIO]")

    def test_injected_lstat_errors_name_the_db(self):
        for n in (1, 2):
            with self.subTest(n=n):
                with lstat_error(errno.EIO, n):
                    result = self.main(*self.args(self.db))
                self.assert_refused(result, self.db, "[EIO]")


class ComparisonOnly(Base):
    def test_main_opens_no_file_to_write_or_create_and_changes_no_fixture(self):
        overlay, stage, other = self.mkdir("S/L01"), self.mkdir("P/stage_1_sect"), self.mkdir("P/other")
        for root in (overlay, stage):
            os.makedirs(os.path.join(root, "sect"))
            self.write(os.path.join(root, "sect", "layer_7.json"), b'{"layer": 7}')
            self.write(os.path.join(root, "notes.md"), b"overlay notes\n")
        self.write(os.path.join(other, "notes.md"), b"other notes\n")
        paths = []
        for root, name in ((overlay, "l01.json"), (stage, "stage.json"), (other, "other.json")):
            out = os.path.join(self.mdir, name)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(unit_manifest.main(["--root", root, "--out", out]), 0)
            paths.append(out)
        db = self.make_db([(os.path.join(overlay, "notes.md"), sha(b"overlay notes\n"))])
        roots = (overlay, stage, other, self.mdir, self.ddir)
        before = [sorted(os.listdir(root)) for root in roots], tree_state(self.tmp)
        with recording_opens() as opens:
            code, out, err = self.main("--unit", paths[0], "--reference", paths[1], "--reference", paths[2],
                                       "--toolkit-db", db)
        self.assertEqual((code, err), (0, ""))
        rows = json.loads(out)
        self.assertEqual([row["class"] for row in rows], ["equal", "equal"])
        self.assertEqual(rows[0]["hint"], {"sha256": sha(b"overlay notes\n"), "agrees": True})
        # The hook saw the tool's own read-only manifest opens, so an empty write list is not a dead hook.
        self.assertLessEqual({"l01.json", "stage.json", "other.json"}, {os.path.basename(str(e[0])) for e in opens})
        self.assertEqual(opens_to_write(opens), [])
        self.assertEqual(([sorted(os.listdir(root)) for root in roots], tree_state(self.tmp)), before)


if __name__ == "__main__":
    unittest.main()
