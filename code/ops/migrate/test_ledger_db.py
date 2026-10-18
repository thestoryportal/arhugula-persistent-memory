"""Tests for ledger_db, the I/O shell of Step 271 over ledger_db_core (Step 272).

End to end: each test builds unit sources, Step 201 style manifests, a plans file, an annex TSV and a
small DuckDB file (the toolkit stand-in) in a temporary directory, runs ledger_db.main, and reads the
four TSV reports. Attacks come from code/tests/fault_kit.py.
"""
from __future__ import annotations

import contextlib
import errno
import fcntl
import hashlib
import io
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import duckdb

import fault_kit as FK
from ops.migrate import fdsafe, ledger_db

GiB = 1 << 30
REQ_HEADER = "requirement_id\tsource\ttarget\taction\tobserved_bytes\tclass\tlane\tcheck_id\tadmission\tprd_ids\n"
REPORTS = ("drift.tsv", "cross_unit_dups.tsv", "targets.tsv", "capacity.tsv")
SCRIPT = os.path.abspath(ledger_db.__file__)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def named(path):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == path


def getpath(fd: int) -> str:
    return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b"\0", 1)[0])


def readb(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def open_fds() -> int:
    return len(os.listdir("/dev/fd"))


def tree(path: str) -> list:
    out = []
    for dirpath, dirs, files in os.walk(path):
        out += [os.path.relpath(os.path.join(dirpath, n), path) for n in dirs + files]
    return sorted(out)


class Fixture:
    """Two HOLD units under src/, moved to dst/x and dst/y; dst is the one free root."""

    def __init__(self, test: unittest.TestCase):
        self.test = test
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="ldb-"))
        test.addCleanup(shutil.rmtree, self.base, True)
        j = os.path.join
        self.src, self.dst, self.inp, self.outp = (j(self.base, n) for n in ("src", "dst", "in", "outp"))
        for d in (self.dst, self.inp, self.outp, j(self.src, "u1", "sub"), j(self.src, "u2")):
            os.makedirs(d)
        self.data = {"u1/a.txt": b"alpha\n", "u1/sub/b.bin": b"\x00\x01", "u2/c.txt": b"alpha\n", "u2/e.txt": b"echo\n"}
        for rel, data in self.data.items():
            with open(j(self.src, rel), "wb") as fh:
                fh.write(data)
        self.dev = os.stat(self.dst).st_dev
        self.req = j(self.inp, "req.tsv")
        self.write_req([("MV-901", self.u("u1"), "HOLD"), ("MV-902", self.u("u2"), "HOLD")])
        self.toolkit = j(self.inp, "toolkit.duckdb")
        self.make_db(self.toolkit, [(self.u("u1/a.txt"), sha(b"stale")), (self.u("u1/sub/b.bin"), None),
                                    (self.u("u2/c.txt"), sha(b"alpha\n"))])
        self.m1 = self.manifest("m1.json", "u1")
        self.m2 = self.manifest("m2.json", "u2")
        self.plans = j(self.inp, "plans.json")
        self.write_plans(self.entries())
        self.out = j(self.outp, "ledger")

    def u(self, rel: str) -> str:
        return os.path.join(self.src, rel)

    def write(self, path: str, data: bytes) -> None:
        with open(path, "wb") as fh:
            fh.write(data)

    def write_req(self, rows, path=None) -> None:
        body = "".join(f"{rid}\t{source}\t\t{action}\t0\tc\tl\tC-HOLD\tnone\tICM-R4\n" for rid, source, action in rows)
        self.write(path or self.req, (REQ_HEADER + body).encode())

    def make_db(self, path: str, rows) -> None:
        con = duckdb.connect(path)
        con.execute("CREATE TABLE inventory (abspath VARCHAR, sha256 VARCHAR, kind VARCHAR)")
        for abspath, digest in rows:
            con.execute("INSERT INTO inventory VALUES (?, ?, 'file')", [abspath, digest])
        con.close()

    def leaf(self, rel: str, device=None) -> dict:
        path = self.u(rel)
        st = os.lstat(path)
        return {"source": path, "kind": "file", "bytes": st.st_size, "sha256": sha(self.data[rel]), "link_text": None,
                "device": st.st_dev if device is None else device, "inode": st.st_ino, "nlink": st.st_nlink}

    def manifest(self, name: str, unit: str, *, device=None, leaves=None, doc=None) -> tuple:
        if leaves is None:
            leaves = [self.leaf(rel, device) for rel in sorted(self.data) if rel.startswith(unit + "/")]
        if doc is None:
            doc = {"schema_version": 1, "root": self.u(unit), "leaves": leaves, "git_roots": []}
        data = doc if isinstance(doc, bytes) else json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
        path = os.path.join(self.inp, name)
        self.write(path, data)
        return path, sha(data)

    def entries(self) -> list:
        return [{"id": "E1", "replaces": ["MV-901"], "moves": [{"source": self.u("u1"), "target": f"{self.dst}/x"}],
                 "manifest": self.m1[0], "manifest_sha256": self.m1[1]},
                {"id": "E2", "replaces": ["MV-902"], "moves": [{"source": self.u("u2"), "target": f"{self.dst}/y"}],
                 "manifest": self.m2[0], "manifest_sha256": self.m2[1]}]

    def write_plans(self, doc) -> None:
        data = doc if isinstance(doc, bytes) else json.dumps({"entries": doc} if isinstance(doc, list) else doc).encode()
        self.write(self.plans, data)

    def argv(self, *, floor="0", out=None, extra=()) -> list:
        argv = ["--plans", self.plans, "--requirements", self.req, "--toolkit-db", self.toolkit,
                "--free-root", f"D={self.dst}", "--out", out or self.out, *extra]
        return argv + (["--floor-bytes", floor] if floor is not None else [])

    def run(self, argv=None) -> tuple:
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = ledger_db.main(self.argv() if argv is None else argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def report(self, name: str, out=None) -> list:
        with open(os.path.join(out or self.out, name), encoding="utf-8") as fh:
            text = fh.read()
        self.test.assertTrue(text.endswith("\n"))
        return [line.split("\t") for line in text[:-1].split("\n")]


class Base(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture(self)

    def assertRefused(self, result, path, errname=None):
        code, out, err = result
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(err.count("\n"), 1, err)
        self.assertTrue(err.endswith("\n"))
        self.assertNotIn("Traceback", err)
        self.assertIn(path, err)
        if errname is not None:
            self.assertIn(f"[{errname}]", err)

    def assertNothingWritten(self):
        self.assertFalse(os.path.lexists(self.fx.out))


class EndToEnd(Base):
    def test_four_reports_with_drift_no_hash_missing_and_duplicates_exit_0(self):
        fx = self.fx
        code, out, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))
        self.assertEqual(fx.report("drift.tsv"), [
            ["status", "entry", "source", "fresh_sha256", "toolkit_sha256"],
            ["drift", "E1", fx.u("u1/a.txt"), sha(b"alpha\n"), sha(b"stale")],
            ["toolkit-missing", "E2", fx.u("u2/e.txt"), sha(b"echo\n"), ""],
            ["toolkit-no-hash", "E1", fx.u("u1/sub/b.bin"), sha(b"\x00\x01"), ""]])
        self.assertEqual(fx.report("cross_unit_dups.tsv"), [
            ["sha256", "bytes", "entry", "source"],
            [sha(b"alpha\n"), "6", "E1", fx.u("u1/a.txt")],
            [sha(b"alpha\n"), "6", "E2", fx.u("u2/c.txt")]])
        self.assertEqual(fx.report("targets.tsv"), [["kind", "entry", "source", "target"]])
        self.assertEqual(fx.report("capacity.tsv"),
                         [["root", "needed_bytes", "free_bytes", "floor_bytes", "budget_bytes"]])
        lines = out.splitlines()
        self.assertEqual([line.split("\t") for line in lines],
                         [[os.path.join(fx.out, name), str(n)] for name, n in zip(REPORTS, (3, 2, 0, 0))])

    def test_existing_target_on_disk_is_a_targets_row_and_exit_1(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x/sub")
        fx.write(f"{fx.dst}/x/a.txt", b"old")
        code, out, err = fx.run()
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(fx.report("targets.tsv")[1:], [
            ["target-exists", "E1", fx.u("u1"), f"{fx.dst}/x"],
            ["target-exists", "E1", fx.u("u1/a.txt"), f"{fx.dst}/x/a.txt"]])
        self.assertIn(f"{os.path.join(fx.out, 'targets.tsv')}\t2", out.splitlines())

    def test_existing_target_that_is_a_file_or_fifo_is_a_row(self):
        fx = self.fx
        fx.write(f"{fx.dst}/x", b"file")
        os.mkfifo(f"{fx.dst}/y")
        code, _, err = fx.run()
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(fx.report("targets.tsv")[1:], [
            ["target-exists", "E1", fx.u("u1"), f"{fx.dst}/x"],
            ["target-exists", "E2", fx.u("u2"), f"{fx.dst}/y"]])

    def test_existing_symlink_inside_an_existing_target_is_listed_not_followed(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x")
        os.symlink(fx.inp, f"{fx.dst}/x/sub")
        code, _, err = fx.run()
        self.assertEqual((code, err), (1, ""))
        rows = fx.report("targets.tsv")[1:]
        self.assertIn(["target-exists", "E1", fx.u("u1"), f"{fx.dst}/x"], rows)
        self.assertNotIn(f"{fx.dst}/x/sub/b.bin", [r[3] for r in rows])

    def test_same_filesystem_rename_costs_no_bytes(self):
        fx = self.fx
        code, _, err = fx.run(fx.argv(floor=str(1 << 62)))
        self.assertEqual((code, err), (1, ""))
        rows = fx.report("capacity.tsv")[1:]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][:2], [fx.dst, "0"])
        self.assertEqual(rows[0][3], str(1 << 62))

    def test_cross_filesystem_copy_counts_its_bytes_over_capacity(self):
        fx = self.fx
        fx.m1 = fx.manifest("m1.json", "u1", device=fx.dev + 1)
        fx.write_plans(fx.entries())
        code, _, err = fx.run(fx.argv(floor=str(1 << 62)))
        self.assertEqual((code, err), (1, ""))
        rows = fx.report("capacity.tsv")[1:]
        self.assertEqual(rows[0][:2], [fx.dst, "8"])

    def test_free_bytes_are_f_bavail_times_f_frsize_of_the_held_root(self):
        fx = self.fx
        fx.m1 = fx.manifest("m1.json", "u1", device=fx.dev + 1)
        fx.write_plans(fx.entries())
        seen = []

        def fake(arg):
            seen.append(arg)
            return types.SimpleNamespace(f_bavail=1, f_frsize=7, f_bfree=100, f_bsize=4096, f_blocks=1000)
        with mock.patch.object(os, "statvfs", fake):
            code, _, err = fx.run()
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(fx.report("capacity.tsv")[1:], [[fx.dst, "8", "7", "0", "7"]])
        self.assertEqual(len(seen), 1)
        self.assertIsInstance(seen[0], int)

    def test_free_bytes_within_budget_give_no_row(self):
        fx = self.fx
        fx.m1 = fx.manifest("m1.json", "u1", device=fx.dev + 1)
        fx.write_plans(fx.entries())
        free = types.SimpleNamespace(f_bavail=1, f_frsize=8, f_bfree=0, f_bsize=1, f_blocks=1)
        with mock.patch.object(os, "statvfs", lambda arg: free):
            code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))

    def test_floor_defaults_to_20_gib(self):
        fx = self.fx
        free = types.SimpleNamespace(f_bavail=5, f_frsize=1, f_bfree=5, f_bsize=1, f_blocks=5)
        with mock.patch.object(os, "statvfs", lambda arg: free):
            code, _, err = fx.run(fx.argv(floor=None))
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(fx.report("capacity.tsv")[1:], [[fx.dst, "0", "5", str(20 * GiB), str(5 - 20 * GiB)]])

    def test_two_free_roots_each_get_their_own_free_bytes(self):
        fx = self.fx
        other = os.path.join(fx.base, "dst2")
        os.mkdir(other)
        entries = fx.entries()
        entries[1]["moves"][0]["target"] = f"{other}/y"
        fx.write_plans(entries)
        code, _, err = fx.run(fx.argv(floor=str(1 << 62), extra=("--free-root", f"W={other}")))
        self.assertEqual((code, err), (1, ""))
        self.assertEqual([r[0] for r in fx.report("capacity.tsv")[1:]], sorted([fx.dst, other]))

    def test_valid_plans_file_with_zero_entries_exits_2(self):
        fx = self.fx
        fx.write_plans([])
        self.assertRefused(fx.run(), "entries")
        self.assertNothingWritten()

    def test_toolkit_database_is_attached_read_only_and_left_unchanged(self):
        fx = self.fx
        os.chmod(fx.toolkit, 0o444)
        self.addCleanup(os.chmod, fx.toolkit, 0o644)
        before = (tree(fx.inp), sha(readb(fx.toolkit)), os.stat(fx.toolkit).st_mtime_ns)
        code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        self.assertEqual((tree(fx.inp), sha(readb(fx.toolkit)), os.stat(fx.toolkit).st_mtime_ns), before)

    def test_no_input_is_changed_and_nothing_is_deleted_or_renamed(self):
        fx = self.fx
        listing = tree(fx.base)
        before = {p: readb(os.path.join(fx.base, p)) for p in listing
                  if os.path.isfile(os.path.join(fx.base, p))}

        def refuse(*args, **kwargs):
            raise AssertionError(f"ledger_db changed the filesystem: {args!r}")
        with mock.patch.object(os, "unlink", refuse), mock.patch.object(os, "remove", refuse), \
                mock.patch.object(os, "rmdir", refuse), mock.patch.object(os, "rename", refuse), \
                mock.patch.object(os, "replace", refuse):
            code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        after = {p: readb(os.path.join(fx.base, p)) for p in before}
        self.assertEqual(after, before)
        self.assertEqual(sorted(set(tree(fx.base)) - set(listing)),
                         sorted(["outp/ledger"] + [f"outp/ledger/{n}" for n in REPORTS]))

    def test_no_fd_leaks_on_success_or_refusal(self):
        fx = self.fx
        start = open_fds()
        self.assertEqual(fx.run()[0], 0)
        self.assertEqual(open_fds(), start)
        self.assertEqual(fx.run()[0], 2)  # the output now exists
        self.assertEqual(open_fds(), start)

    def test_cli_refusal_is_one_line_with_errno_and_no_traceback(self):
        fx = self.fx
        missing = os.path.join(fx.inp, "missing.json")
        argv = fx.argv()
        argv[argv.index("--plans") + 1] = missing
        proc = subprocess.run([sys.executable, "-B", SCRIPT, *argv], capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr.count("\n"), 1, proc.stderr)
        self.assertIn(missing, proc.stderr)
        self.assertIn("[ENOENT]", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_cli_success_exit_0(self):
        fx = self.fx
        proc = subprocess.run([sys.executable, "-B", SCRIPT, *fx.argv()], capture_output=True, text=True, timeout=60)
        self.assertEqual((proc.returncode, proc.stderr), (0, ""))
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))


class Malformed(Base):
    """Every unreadable or malformed input exits 2 with one line and writes nothing."""

    def check(self, path=None, errname=None, argv=None):
        self.assertRefused(self.fx.run(argv), path or "", errname)
        self.assertNothingWritten()

    def test_plans_not_utf8_not_json_duplicate_key_or_constant(self):
        fx = self.fx
        for data in (b"\xff{}", b"{", b'{"entries": [], "entries": []}', b'{"entries": NaN}', b"[]",
                     b'{"entries": {}}', b'{"x": []}', b'{"entries": [1]}'):
            with self.subTest(data=data):
                fx.write_plans(data)
                self.check(fx.plans)

    def test_entry_manifest_fields(self):
        fx = self.fx
        for change, says in (({"manifest": None}, "entries[0].manifest:"), ({"manifest": "in/m1.json"}, "entries[0].manifest:"),
                             ({"manifest": fx.m1[0] + "/"}, "entries[0].manifest:"),
                             ({"manifest": fx.inp + "/./m1.json"}, "entries[0].manifest:"),
                             ({"manifest_sha256": None}, "entries[0].manifest_sha256:"),
                             ({"manifest_sha256": fx.m1[1].upper()}, "entries[0].manifest_sha256:"),
                             ({"manifest_sha256": fx.m1[1][:63]}, "entries[0].manifest_sha256:"),
                             ({"manifest_sha256": sha(b"other")}, "is not the plan's"),
                             ({"leaves": []}, "leaves come from the manifest")):
            with self.subTest(change=change):
                entries = fx.entries()
                entries[0].update(change)
                fx.write_plans(entries)
                self.check(says)
        for key in ("manifest", "manifest_sha256"):
            with self.subTest(missing=key):
                entries = fx.entries()
                del entries[0][key]
                fx.write_plans(entries)
                self.check(fx.plans)

    def test_manifest_digest_mismatch_refuses(self):
        fx = self.fx
        fx.write(fx.m1[0], readb(fx.m1[0]) + b" ")
        self.check(fx.m1[0])

    def test_manifest_document_shapes(self):
        fx = self.fx
        good = fx.leaf("u1/a.txt")
        for doc in (b"\xff", b"{", b"[]", {"schema_version": 2, "leaves": []}, {"schema_version": True, "leaves": []},
                    {"leaves": []}, {"schema_version": 1}, {"schema_version": 1, "leaves": {}},
                    {"schema_version": 1, "leaves": [1]}, {"schema_version": 1, "leaves": [{**good, "device": "1"}]},
                    {"schema_version": 1, "leaves": [{**good, "device": True}]},
                    {"schema_version": 1, "leaves": [{k: v for k, v in good.items() if k != "device"}]},
                    {"schema_version": 1, "leaves": [{**good, "source": 7}]},
                    {"schema_version": 1, "leaves": [{k: v for k, v in good.items() if k != "source"}]},
                    {"schema_version": 1, "leaves": [{**good, "kind": "fifo"}]}):
            with self.subTest(doc=doc):
                fx.m1 = fx.manifest("m1.json", "u1", doc=doc)
                fx.write_plans(fx.entries())
                self.check()

    def test_requirements_tsv_shapes(self):
        fx = self.fx
        good = f"MV-901\t{fx.u('u1')}\t\tHOLD\t0\tc\tl\tC-HOLD\tnone\tICM-R4\nMV-902\t{fx.u('u2')}\t\tHOLD\t0\tc\tl\tC-HOLD\tnone\tICM-R4\n"
        for data in (b"", REQ_HEADER.encode(), b"\xff" + (REQ_HEADER + good).encode(),
                     (REQ_HEADER + good).replace("\n", "\r\n").encode(), (REQ_HEADER + good)[:-1].encode(),
                     (REQ_HEADER.replace("action", "verb") + good).encode(),
                     (REQ_HEADER.replace("\tsource", "\tsource\tsource") + good).encode(),
                     (REQ_HEADER + good + "MV-903\tshort\n").encode(),
                     (REQ_HEADER + good + "\n").encode()):
            with self.subTest(data=data):
                fx.write(fx.req, data)
                self.check(fx.req)

    def test_annex_rows_the_core_refuses(self):
        fx = self.fx
        for rows in ([("MV-901", fx.u("u1"), "MOVE"), ("MV-902", fx.u("u2"), "HOLD")],
                     [("MV-901", fx.u("u1"), "HOLD")],
                     [("MV-901", fx.u("u1"), "HOLD"), ("MV-901", fx.u("u2"), "HOLD")]):
            with self.subTest(rows=rows):
                fx.write_req(rows)
                self.check()

    def test_requirements_not_utf8_in_any_column_refuses(self):
        fx = self.fx
        fx.write_req([("MV-901", fx.u("u1"), "HOLD"), ("MV-902", fx.u("u2"), "HOLD")])
        fx.write(fx.req, readb(fx.req).replace(b"\tc\t", b"\tc\xff\t", 1))
        self.check(fx.req)

    def test_a_value_that_is_not_utf8_text_refuses_and_writes_nothing(self):
        fx = self.fx
        leaf = {**fx.leaf("u2/e.txt"), "source": fx.u("u2/bad\ud800name")}
        fx.m2 = fx.manifest("m2.json", "u2", leaves=[fx.leaf("u2/c.txt"), leaf])
        fx.write_plans(fx.entries())
        self.check(fx.m2[0])
        fx.m2 = fx.manifest("m2.json", "u2")
        entries = fx.entries()
        entries[0]["moves"][0]["target"] = f"{fx.dst}/x\ud800"
        fx.write_plans(entries)
        self.check(fx.plans)

    def test_relative_paths_are_read_from_the_working_directory(self):
        fx = self.fx
        cwd = os.getcwd()
        os.chdir(fx.base)
        self.addCleanup(os.chdir, cwd)
        rel = lambda p: os.path.relpath(p, fx.base)
        argv = ["--plans", rel(fx.plans), "--requirements", rel(fx.req), "--toolkit-db", rel(fx.toolkit),
                "--free-root", f"D={rel(fx.dst)}", "--floor-bytes", "0", "--out", rel(fx.out)]
        code, out, err = fx.run(argv)
        self.assertEqual((code, err), (0, ""))
        self.assertIn(os.path.join(fx.out, "drift.tsv") + "\t3", out.splitlines())
        self.assertEqual(fx.report("capacity.tsv")[1:], [])
        argv[argv.index("--toolkit-db") + 1] = "in/missing.duckdb"
        argv[-1] = "outp/ledger2"
        self.assertRefused(fx.run(argv), os.path.join(fx.inp, "missing.duckdb"), "ENOENT")

    def test_requirements_rows_from_every_file_are_used(self):
        fx = self.fx
        second = os.path.join(fx.inp, "amend.tsv")
        fx.write_req([("MV-901", fx.u("u1"), "HOLD")])
        fx.write_req([("MV-902", fx.u("u2"), "HOLD")], second)
        code, _, err = fx.run(fx.argv(extra=("--requirements", second)))
        self.assertEqual((code, err), (0, ""))

    def test_free_root_arguments(self):
        fx = self.fx
        for spec in ("nolabel", f"={fx.dst}", "D=", f"D={fx.dst}/missing", f"D={fx.m1[0]}"):
            with self.subTest(spec=spec):
                argv = fx.argv()
                argv[argv.index("--free-root") + 1] = spec
                self.check(argv=argv)
        other = os.path.join(fx.base, "dst2")
        os.mkdir(other)
        for extra, says in ((("--free-root", f"D={other}"), "duplicate free root label D"),
                            (("--free-root", f"E={fx.dst}"), "is given as two free roots")):
            with self.subTest(extra=extra):
                self.check(says, argv=fx.argv(extra=extra))

    def test_free_root_through_a_symlink_refuses(self):
        fx = self.fx
        link = os.path.join(fx.base, "dstlink")
        os.symlink(fx.dst, link)
        argv = fx.argv()
        argv[argv.index("--free-root") + 1] = f"D={link}"
        self.check(link, "ENOTDIR", argv)

    def test_negative_floor_refuses(self):
        self.check("floor_bytes", argv=self.fx.argv(floor="-1"))

    def test_move_target_outside_every_free_root_refuses(self):
        fx = self.fx
        entries = fx.entries()
        entries[0]["moves"][0]["target"] = f"{fx.outp}/x"
        fx.write_plans(entries)
        self.check("entries[0].moves[0].target")

    def test_toolkit_database_missing_invalid_or_without_inventory(self):
        fx = self.fx
        bad = os.path.join(fx.inp, "bad.duckdb")
        fx.write(bad, b"not a database")
        empty = os.path.join(fx.inp, "empty.duckdb")
        duckdb.connect(empty).close()
        wrong = os.path.join(fx.inp, "wrong.duckdb")
        fx.make_db(wrong, [("relative/path", None)])
        for path in (os.path.join(fx.inp, "missing.duckdb"), bad, empty, wrong, fx.inp):
            with self.subTest(path=path):
                argv = fx.argv()
                argv[argv.index("--toolkit-db") + 1] = path
                self.assertRefused(fx.run(argv), "")
                self.assertNothingWritten()
        self.assertFalse(os.path.exists(os.path.join(fx.inp, "missing.duckdb")))

    def test_toolkit_database_path_with_a_quote_is_attached(self):
        fx = self.fx
        quoted = os.path.join(fx.inp, "it's.duckdb")
        os.rename(fx.toolkit, quoted)
        argv = fx.argv()
        argv[argv.index("--toolkit-db") + 1] = quoted
        code, _, err = fx.run(argv)
        self.assertEqual((code, err), (0, ""))

    def test_toolkit_database_symlink_refuses(self):
        fx = self.fx
        link = os.path.join(fx.inp, "link.duckdb")
        os.symlink(fx.toolkit, link)
        argv = fx.argv()
        argv[argv.index("--toolkit-db") + 1] = link
        self.check(link, argv=argv)

    def test_output_that_exists_is_never_overwritten(self):
        fx = self.fx
        os.mkdir(fx.out)
        fx.write(os.path.join(fx.out, "drift.tsv"), b"keep")
        self.assertRefused(fx.run(), fx.out, "EEXIST")
        self.assertEqual(os.listdir(fx.out), ["drift.tsv"])
        self.assertEqual(readb(os.path.join(fx.out, "drift.tsv")), b"keep")

    def test_output_inside_a_free_root_refuses_and_creates_nothing(self):
        fx = self.fx
        out = os.path.join(fx.dst, "ledger")
        self.assertRefused(fx.run(fx.argv(out=out)), fx.dst)
        self.assertEqual(os.listdir(fx.dst), [])

    def test_output_parent_missing_refuses(self):
        fx = self.fx
        out = os.path.join(fx.outp, "missing", "ledger")
        self.assertRefused(fx.run(fx.argv(out=out)), os.path.join(fx.outp, "missing"), "ENOENT")

    def test_output_parent_through_a_link_is_resolved_and_checked_live(self):
        fx = self.fx
        link = os.path.join(fx.base, "outlink")
        os.symlink(fx.outp, link)
        code, out, err = fx.run(fx.argv(out=os.path.join(link, "ledger")))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))
        self.assertIn(os.path.join(fx.out, "drift.tsv"), out)
        inside = os.path.join(fx.base, "dstlink")
        os.symlink(fx.dst, inside)
        self.assertRefused(fx.run(fx.argv(out=os.path.join(inside, "ledger"))), fx.dst)
        self.assertEqual(os.listdir(fx.dst), [])

    def test_a_value_tsv_cannot_carry_refuses_and_writes_nothing(self):
        fx = self.fx
        for name in ("new\nline", "tab\tname", "cr\rname"):
            with self.subTest(name=name):
                leaf = {**fx.leaf("u2/e.txt"), "source": fx.u("u2/" + name)}
                fx.m2 = fx.manifest("m2.json", "u2", leaves=[fx.leaf("u2/c.txt"), leaf])
                fx.write_plans(fx.entries())
                self.check(os.path.join(fx.out, "drift.tsv"))


class Attacks(Base):
    """fault_kit attacks on every bound object, call class, output and held root."""

    # swap_for_symlink: each object swapped for a symlink between scan (or lstat) and open.
    def test_swap_inputs_for_symlinks_before_open(self):
        fx = self.fx
        decoy = os.path.join(fx.base, "decoy")
        fx.write(decoy, b"{}")
        for name in ("plans.json", "m1.json", "req.tsv"):
            with self.subTest(name=name):
                fx2 = Fixture(self)
                path = os.path.join(fx2.inp, name)
                with FK.swap_for_symlink("open", 1, path, decoy, match=named(name)):
                    result = fx2.run()
                self.assertRefused(result, path, "ELOOP")
                self.assertFalse(os.path.lexists(fx2.out))

    def test_swap_input_directory_for_a_symlink(self):
        fx = self.fx
        with FK.swap_for_symlink("open", 1, fx.inp, fx.src, match=named(fx.inp)):
            result = fx.run()
        self.assertRefused(result, fx.inp, "ENOTDIR")
        self.assertNothingWritten()

    def test_swap_free_root_for_a_symlink(self):
        fx = self.fx
        with FK.swap_for_symlink("open", 1, fx.dst, fx.src, match=named(fx.dst)):
            result = fx.run()
        self.assertRefused(result, fx.dst, "ENOTDIR")
        self.assertNothingWritten()

    def test_swap_directory_inside_an_existing_target_during_the_walk(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x/sub")
        with FK.swap_for_symlink("open", 1, f"{fx.dst}/x/sub", fx.inp, match=named("sub")):
            result = fx.run()
        self.assertRefused(result, f"{fx.dst}/x/sub", "ENOTDIR")
        self.assertNothingWritten()

    def test_swap_output_parent_for_a_symlink(self):
        fx = self.fx
        with FK.swap_for_symlink("open", 1, fx.outp, fx.dst, match=named(fx.outp)):
            result = fx.run()
        self.assertRefused(result, fx.outp, "ENOTDIR")
        self.assertEqual(os.listdir(fx.dst), [])

    def test_swap_toolkit_database_between_check_and_attach(self):
        fx = self.fx
        other = os.path.join(fx.base, "other.duckdb")
        fx.make_db(other, [])
        real = duckdb.connect

        def hooked(*args, **kwargs):
            park = os.path.join(fx.inp, FK.PARK_PREFIX + "db")
            os.mkdir(park)
            os.rename(fx.toolkit, os.path.join(park, "toolkit.duckdb"))
            os.symlink(other, fx.toolkit)
            return real(*args, **kwargs)
        with mock.patch.object(duckdb, "connect", hooked):
            result = fx.run()
        self.assertRefused(result, fx.toolkit)
        self.assertNothingWritten()

    def test_toolkit_database_replaced_between_check_and_attach(self):
        fx = self.fx
        fresh = os.path.join(fx.base, "fresh.duckdb")
        fx.make_db(fresh, [])
        real = duckdb.connect

        def hooked(*args, **kwargs):
            park = os.path.join(fx.inp, FK.PARK_PREFIX + "db")
            os.mkdir(park)
            os.rename(fx.toolkit, os.path.join(park, "toolkit.duckdb"))
            os.rename(fresh, fx.toolkit)
            return real(*args, **kwargs)
        with mock.patch.object(duckdb, "connect", hooked):
            result = fx.run()
        self.assertRefused(result, fx.toolkit)
        self.assertNothingWritten()

    def test_toolkit_directory_moved_while_duckdb_reads_refuses(self):
        fx = self.fx
        decoy_dir = os.path.join(fx.base, "decoy-in")
        os.mkdir(decoy_dir)
        fx.make_db(os.path.join(decoy_dir, "toolkit.duckdb"), [])
        real = duckdb.connect

        def hooked(*args, **kwargs):
            park = os.path.join(fx.base, FK.PARK_PREFIX + "in")
            os.mkdir(park)
            os.rename(fx.inp, os.path.join(park, "in"))
            os.rename(decoy_dir, fx.inp)
            return real(*args, **kwargs)
        with mock.patch.object(duckdb, "connect", hooked):
            result = fx.run()
        self.assertRefused(result, fx.toolkit)
        self.assertNothingWritten()

    # fifo_in_place: every directory, leaf and output parent; a blocking open fails the timeout.
    def test_fifo_in_place_of_each_input_file(self):
        for name in ("plans.json", "m1.json", "req.tsv"):
            with self.subTest(name=name):
                fx = Fixture(self)
                path = os.path.join(fx.inp, name)
                with FK.fifo_in_place(path, timeout=10):
                    result = fx.run()
                self.assertRefused(result, path)
                self.assertFalse(os.path.lexists(fx.out))

    def test_fifo_in_place_of_each_directory_and_the_output_parent(self):
        for attr in ("inp", "dst", "outp"):
            with self.subTest(attr=attr):
                fx = Fixture(self)
                path = getattr(fx, attr)
                with FK.fifo_in_place(path, timeout=10):
                    result = fx.run()
                self.assertRefused(result, path, "ENOTDIR")

    def test_fifo_in_place_of_the_toolkit_database_refuses_without_blocking(self):
        fx = self.fx
        with FK.fifo_in_place(fx.toolkit, timeout=30):
            proc = subprocess.run([sys.executable, "-B", SCRIPT, *fx.argv()], capture_output=True, text=True,
                                  timeout=15)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn(fx.toolkit, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertNothingWritten()

    def test_fifo_in_place_of_a_directory_inside_an_existing_target(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x/sub")
        with FK.fifo_in_place(f"{fx.dst}/x/sub", timeout=10):
            code, _, err = fx.run()
        self.assertEqual((code, err), (1, ""))

    # inject_oserror: each call class the tool makes.
    def eio(self, name, n, path, *, err=errno.EIO, match=None):
        with FK.inject_oserror(name, n, err, match=match):
            result = self.fx.run()
        self.assertRefused(result, path, errno.errorcode[err])
        return result

    def test_eio_on_open_of_an_input(self):
        self.eio("open", 1, self.fx.plans, match=named("plans.json"))
        self.assertNothingWritten()

    def test_eio_on_open_of_the_free_root(self):
        self.eio("open", 1, self.fx.dst, match=named(self.fx.dst))

    def test_eio_on_read(self):
        self.eio("read", 1, self.fx.req)
        self.assertNothingWritten()

    def test_eio_on_scandir_of_an_existing_target(self):
        os.makedirs(f"{self.fx.dst}/x")
        self.eio("scandir", 1, f"{self.fx.dst}/x")
        self.assertNothingWritten()

    def test_eio_on_fstat_of_the_free_root(self):
        self.eio("fstat", 1, self.fx.dst)
        self.assertNothingWritten()

    def test_eio_on_getpath(self):
        self.eio(FK.GETPATH, 1, self.fx.dst)
        self.assertNothingWritten()

    def test_eio_on_mkdir_of_the_output(self):
        self.eio("mkdir", 1, self.fx.out)
        self.assertNothingWritten()

    def test_enospc_and_eio_on_write_keep_the_partial_output(self):
        for err in (errno.ENOSPC, errno.EIO):
            with self.subTest(err=err):
                self.fx = Fixture(self)
                code, out, msg = self.eio("write", 1, os.path.join(self.fx.out, "drift.tsv"), err=err)
                self.assertIn("left in place", msg)
                self.assertEqual(os.listdir(self.fx.out), ["drift.tsv"])

    def test_eio_on_close_of_an_output_names_it_and_keeps_it(self):
        fx = self.fx
        target = os.path.join(fx.out, "targets.tsv")
        _, _, msg = self.eio("close", 1, target, match=lambda fd: getpath(fd) == target)
        self.assertIn("left in place", msg)
        self.assertEqual(fx.report("targets.tsv"), [["kind", "entry", "source", "target"]])

    def test_eio_on_close_of_the_free_root_after_the_write_names_the_output(self):
        fx = self.fx
        _, _, msg = self.eio("close", 1, fx.dst, match=lambda fd: getpath(fd) == fx.dst and os.path.lexists(fx.out))
        self.assertIn(fx.out, msg)
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))

    def test_eio_on_statvfs_of_the_free_root(self):
        def fail(arg):
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with mock.patch.object(os, "statvfs", fail):
            result = self.fx.run()
        self.assertRefused(result, self.fx.dst, "EIO")
        self.assertNothingWritten()

    def test_eio_on_lstat_of_a_move_target(self):
        fx = self.fx
        target, real = f"{fx.dst}/x", os.lstat

        def hooked(path, *args, **kwargs):  # the target's name, looked up through its held parent
            if path == os.path.basename(target) and "dir_fd" in kwargs:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "lstat", hooked):
            result = fx.run()
        self.assertRefused(result, target, "EIO")
        self.assertNothingWritten()

    def test_enotdir_on_lstat_of_a_move_target_refuses(self):
        fx = self.fx
        entries = fx.entries()
        fx.write(f"{fx.dst}/blocker", b"file")
        entries[0]["moves"][0]["target"] = f"{fx.dst}/blocker/x"
        fx.write_plans(entries)
        self.assertRefused(fx.run(), f"{fx.dst}/blocker/x", "ENOTDIR")
        self.assertNothingWritten()

    def test_eio_on_realpath_of_the_output_parent(self):
        def fail(path):
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with mock.patch.object(os.path, "realpath", fail):
            result = self.fx.run()
        self.assertRefused(result, self.fx.out, "EIO")
        self.assertNothingWritten()

    # one_byte_writes: each output is byte-identical to the normal run.
    def test_one_byte_writes_give_identical_reports(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x")
        self.assertEqual(fx.run()[0], 1)
        out2 = os.path.join(fx.outp, "ledger2")
        with FK.one_byte_writes():
            code, _, err = fx.run(fx.argv(out=out2))
        self.assertEqual((code, err), (1, ""))
        for name in REPORTS:
            with self.subTest(name=name):
                self.assertEqual(readb(os.path.join(out2, name)),
                                 readb(os.path.join(fx.out, name)))

    # rename_and_rebind: each held root and output parent.
    def test_free_root_rebound_after_it_is_held_refuses(self):
        fx = self.fx
        os.makedirs(f"{fx.dst}/x")
        with FK.rename_and_rebind("open", 1, fx.dst, match=named("req.tsv")):
            result = fx.run()
        self.assertRefused(result, fx.dst)
        self.assertNothingWritten()

    def test_input_directory_rebound_after_it_is_held_refuses(self):
        fx = self.fx
        with FK.rename_and_rebind("open", 1, fx.inp, when="after", match=named(fx.inp)):
            result = fx.run()
        self.assertRefused(result, fx.inp)
        self.assertNothingWritten()

    def test_output_parent_rebound_after_it_is_held_refuses(self):
        fx = self.fx
        with FK.rename_and_rebind("open", 1, fx.outp, when="after", match=named(fx.outp)) as fault:
            result = fx.run()
        self.assertRefused(result, fx.outp)
        self.assertEqual(os.listdir(fx.outp), [])
        self.assertEqual(os.listdir(fault.parked), [])

    def test_output_directory_rebound_during_the_writes_refuses_and_keeps_the_files(self):
        fx = self.fx
        with FK.rename_and_rebind("open", 1, fx.out, match=named("cross_unit_dups.tsv")) as fault:
            result = fx.run()
        self.assertRefused(result, fx.out)
        self.assertEqual(os.listdir(fx.out), [])
        self.assertEqual(sorted(os.listdir(fault.parked)), sorted(REPORTS))

    # raise_unexpected: a non-OSError from inside the tool propagates.
    def test_unexpected_exceptions_propagate(self):
        os.makedirs(f"{self.fx.dst}/x")
        for name, exc, match in (("scandir", RuntimeError, None), ("open", ValueError, named("plans.json")),
                                 ("fstat", KeyError, None), ("write", RuntimeError, None)):
            with self.subTest(name=name, exc=exc):
                fx = Fixture(self)
                os.makedirs(f"{fx.dst}/x")
                with FK.raise_unexpected(name, 1, exc, match=match), self.assertRaises(exc):
                    fx.run()

    def test_unexpected_exception_from_lstat_of_a_target_propagates(self):
        fx = self.fx
        target, real = f"{fx.dst}/x", os.lstat

        def hooked(path, *args, **kwargs):  # the target's name, looked up through its held parent
            if path == os.path.basename(target) and "dir_fd" in kwargs:
                raise RuntimeError("unexpected")
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "lstat", hooked), self.assertRaises(RuntimeError):
            fx.run()

    def test_unexpected_exception_from_decoding_an_input_propagates(self):
        class Bytes(bytes):
            def decode(self, *args, **kwargs):
                raise RuntimeError("unexpected")
        real = fdsafe.read_named
        with mock.patch.object(fdsafe, "read_named", lambda parent, name: Bytes(real(parent, name))), \
                self.assertRaises(RuntimeError):
            self.fx.run()

    def test_unexpected_exception_from_duckdb_propagates(self):
        real = duckdb.connect

        class Con:
            def __init__(self, con):
                self.con = con

            def execute(self, *args):
                raise RuntimeError("unexpected")

            def close(self):
                self.con.close()
        with mock.patch.object(duckdb, "connect", lambda *a, **k: Con(real(*a, **k))), \
                self.assertRaises(RuntimeError):
            self.fx.run()


class Con:
    """A DuckDB connection (the library object) that logs each statement's verb and runs test hooks around it."""

    def __init__(self, con, log, hooks):
        self.con, self.log, self.hooks = con, log, hooks

    def execute(self, sql, *args):
        verb = sql.split()[0]
        self.log.append(verb)
        self.hooks.get(("before", verb), lambda: None)()
        self.con.execute(sql, *args)
        self.hooks.get(("after", verb), lambda: None)()
        return self

    def fetchall(self):
        return self.con.fetchall()

    def close(self):
        self.log.append("close")
        self.con.close()


def park(path: str) -> str:
    """Move path into a new directory beside it (never deleted); return where it went."""
    where = os.path.join(os.path.dirname(path), FK.PARK_PREFIX + "test")
    os.mkdir(where)
    os.rename(path, os.path.join(where, os.path.basename(path)))
    return os.path.join(where, os.path.basename(path))


class ToolkitWindow(Base):
    """Ruling 1a and 7: the toolkit file and its parent are held and watched (kqueue) around the ATTACH."""

    def test_clean_run_reports_no_kqueue_event(self):
        fx = self.fx
        log = []
        real_kq, real_connect = select.kqueue, duckdb.connect

        class Kq:
            def __init__(self):
                self.kq = real_kq()

            def control(self, changes, n, timeout=None):
                got = self.kq.control(changes, n, timeout)
                log.append(("register", len(changes)) if changes else ("poll", list(got)))
                return got

            def close(self):
                log.append("kq-close")
                self.kq.close()
        with mock.patch.object(select, "kqueue", Kq), \
                mock.patch.object(duckdb, "connect", lambda *a, **k: Con(real_connect(*a, **k), log, {})):
            code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(log, [("register", 2), "ATTACH", "SELECT", "DETACH", "close", ("poll", []), "kq-close"])

    def test_toolkit_swapped_and_restored_inside_the_attach_window_refuses(self):
        fx = self.fx
        other = os.path.join(fx.base, "other.duckdb")
        fx.make_db(other, [])
        before = os.lstat(fx.toolkit)
        moved = []
        real = duckdb.connect

        def swap():
            moved.append(park(fx.toolkit))
            os.symlink(other, fx.toolkit)

        def restore():
            os.unlink(fx.toolkit)
            os.rename(moved[0], fx.toolkit)
        hooks = {("before", "ATTACH"): swap, ("after", "SELECT"): restore}
        with mock.patch.object(duckdb, "connect", lambda *a, **k: Con(real(*a, **k), [], hooks)):
            result = fx.run()
        self.assertRefused(result, fx.toolkit)
        self.assertIn("kqueue", result[2])
        self.assertNothingWritten()
        after = os.lstat(fx.toolkit)
        self.assertEqual((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
                         (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns))

    def test_toolkit_changed_before_the_watch_starts_refuses(self):
        real = select.kqueue
        for what in ("file", "directory"):
            with self.subTest(what=what):
                fx = Fixture(self)
                fresh = os.path.join(fx.base, "fresh")
                os.mkdir(fresh)
                fx.make_db(os.path.join(fresh, "toolkit.duckdb"), [])

                def kqueue():  # the shell creates its kqueue after its open and before the watch
                    if what == "file":
                        park(fx.toolkit)
                        os.rename(os.path.join(fresh, "toolkit.duckdb"), fx.toolkit)
                    else:
                        park(fx.inp)
                        os.rename(fresh, fx.inp)
                    return real()
                with mock.patch.object(select, "kqueue", kqueue):
                    result = fx.run()
                self.assertRefused(result, fx.toolkit)
                self.assertFalse(os.path.lexists(fx.out))

    def test_toolkit_swapped_for_a_symlink_at_its_open_refuses(self):
        fx = self.fx
        other = os.path.join(fx.base, "other.duckdb")
        fx.make_db(other, [])
        with FK.swap_for_symlink("open", 1, fx.toolkit, other, match=named("toolkit.duckdb")):
            result = fx.run()
        self.assertRefused(result, fx.toolkit, "ELOOP")
        self.assertNothingWritten()

    def test_fifo_in_place_of_the_toolkit_at_its_open_refuses_without_blocking(self):
        fx = self.fx
        child = ("import sys\nimport fault_kit as FK\nfrom ops.migrate import ledger_db\n"
                 "with FK.fifo_in_place(sys.argv[1], name='open', timeout=30,\n"
                 "                      match=lambda first, *a, **k: first == 'toolkit.duckdb'):\n"
                 "    code = ledger_db.main(sys.argv[2:])\n"
                 "sys.exit(code)\n")
        proc = subprocess.run([sys.executable, "-B", "-c", child, fx.toolkit, *fx.argv()], capture_output=True,
                              text=True, timeout=15)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn(fx.toolkit, proc.stderr)
        self.assertEqual(proc.stderr.count("\n"), 1, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertNothingWritten()

    def test_errors_on_the_held_toolkit_and_its_watch_refuse(self):
        real = select.kqueue

        def kq_failing(step):
            class Kq:
                def __init__(self):
                    if step == "create":
                        raise OSError(errno.EIO, os.strerror(errno.EIO))
                    self.kq = real()

                def control(self, changes, n, timeout=None):
                    if step == ("register" if changes else "poll"):
                        raise OSError(errno.EIO, os.strerror(errno.EIO))
                    return self.kq.control(changes, n, timeout)

                def close(self):
                    self.kq.close()
                    if step == "close":
                        raise OSError(errno.EIO, os.strerror(errno.EIO))
            return mock.patch.object(select, "kqueue", Kq)
        for step in ("open", "fstat", "file-close", "create", "register", "poll", "close"):
            with self.subTest(step=step):
                fx = Fixture(self)
                fault = {"open": lambda: FK.inject_oserror("open", 1, errno.EIO, match=named("toolkit.duckdb")),
                         "fstat": lambda: FK.inject_oserror("fstat", 1, errno.EIO,
                                                            match=lambda fd: getpath(fd) == fx.toolkit),
                         "file-close": lambda: FK.inject_oserror("close", 1, errno.EIO,
                                                                 match=lambda fd: getpath(fd) == fx.toolkit)}
                start = open_fds()
                with fault.get(step, lambda: kq_failing(step))():
                    result = fx.run()
                self.assertRefused(result, fx.toolkit, "EIO")
                self.assertFalse(os.path.lexists(fx.out))
                self.assertEqual(open_fds(), start)

    def test_in_memory_connect_error_is_a_one_line_refusal(self):
        fx = self.fx
        start = open_fds()
        with mock.patch.object(duckdb, "connect", side_effect=duckdb.IOException("injected open failure")):
            result = fx.run()
        self.assertRefused(result, fx.toolkit)
        self.assertIn("injected open failure", result[2])
        self.assertNothingWritten()
        self.assertEqual(open_fds(), start)

    def test_duckdb_is_in_memory_and_only_the_four_reports_are_written(self):
        fx = self.fx
        cwd, tmp = os.path.join(fx.base, "cwd"), os.path.join(fx.base, "tmp")
        os.mkdir(cwd)
        os.mkdir(tmp)
        listing = tree(fx.base)
        calls = []
        real = duckdb.connect

        def spy(*args, **kwargs):
            calls.append((args, kwargs))
            return real(*args, **kwargs)
        here = os.getcwd()
        os.chdir(cwd)
        self.addCleanup(os.chdir, here)
        with mock.patch.object(duckdb, "connect", spy), mock.patch.dict(os.environ, {"TMPDIR": tmp}):
            code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        self.assertTrue(calls)
        self.assertEqual([c for c in calls if c != ((":memory:",), {})], [])
        self.assertEqual(sorted(set(tree(fx.base)) - set(listing)),
                         sorted(["outp/ledger"] + [f"outp/ledger/{n}" for n in REPORTS]))
        self.assertEqual((os.listdir(cwd), os.listdir(tmp)), ([], []))


class TargetLookup(Base):
    """Rulings 3 and 4: each target is looked up through its held parent; a walked directory must stay put."""

    def set_target(self, target, i=0):
        entries = self.fx.entries()
        entries[i]["moves"][0]["target"] = target
        self.fx.write_plans(entries)

    def test_a_link_in_the_target_path_refuses(self):
        for case in ("link-parent", "link-ancestor", "dangling-parent", "dangling-ancestor"):
            with self.subTest(case=case):
                fx = Fixture(self)
                outside = os.path.join(fx.base, "outside")
                os.makedirs(os.path.join(outside, "sub"))
                fx.write(os.path.join(outside, "x"), b"outside")
                fx.write(os.path.join(outside, "sub", "x"), b"outside")
                link = os.path.join(fx.dst, "link")
                os.symlink(outside if case.startswith("link") else os.path.join(fx.base, "nowhere"), link)
                target = f"{link}/x" if case.endswith("parent") else f"{link}/sub/x"
                self.fx = fx
                self.set_target(target)
                self.assertRefused(fx.run(), target)
                self.assertNothingWritten()

    def test_target_under_missing_directories_is_absent(self):
        fx = self.fx
        self.set_target(f"{fx.dst}/a/b/x")
        code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(fx.report("targets.tsv"), [["kind", "entry", "source", "target"]])

    def test_target_parent_moved_during_the_lookup_refuses(self):
        fx = self.fx
        sub = os.path.join(fx.dst, "sub")
        os.mkdir(sub)
        self.set_target(f"{sub}/x")
        real = os.lstat

        def hooked(path, *args, **kwargs):
            if path == "x" and "dir_fd" in kwargs:
                try:
                    return real(path, *args, **kwargs)
                finally:
                    park(sub)
                    os.mkdir(sub)
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "lstat", hooked):
            result = fx.run()
        self.assertRefused(result, f"{sub}/x")
        self.assertIn("moved during the lookup", result[2])
        self.assertNothingWritten()

    def test_missing_directory_that_appears_during_the_lookup_refuses(self):
        fx = self.fx
        self.set_target(f"{fx.dst}/a/x")
        real = os.lstat

        def hooked(path, *args, **kwargs):
            if path == "a" and "dir_fd" in kwargs:
                os.mkdir(os.path.join(fx.dst, "a"))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "lstat", hooked):
            result = fx.run()
        self.assertRefused(result, f"{fx.dst}/a/x")
        self.assertIn("a component is a link or changed", result[2])
        self.assertNothingWritten()

    def test_unexpected_exception_from_holding_a_target_parent_propagates(self):
        fx = self.fx
        with FK.raise_unexpected("open", 2, RuntimeError, match=named(fx.dst)), self.assertRaises(RuntimeError):
            fx.run()

    def test_target_directory_rebound_during_its_walk_refuses(self):
        fx = self.fx
        os.mkdir(f"{fx.dst}/x")
        fx.write(f"{fx.dst}/x/a.txt", b"old")
        with FK.rename_and_rebind("scandir", 1, f"{fx.dst}/x") as fault:
            result = fx.run()
        self.assertRefused(result, f"{fx.dst}/x")
        self.assertIn("rebound during the walk", result[2])
        self.assertNothingWritten()
        self.assertEqual(os.listdir(fault.parked), ["a.txt"])

    def test_target_directory_swapped_between_its_stat_and_its_walk_refuses(self):
        fx = self.fx
        target = f"{fx.dst}/x"
        os.mkdir(target)
        fx.write(f"{target}/a.txt", b"old")
        decoy = os.path.join(fx.base, "decoy")
        os.mkdir(decoy)
        fx.write(os.path.join(decoy, "decoy.txt"), b"decoy")
        real, parked = fdsafe.hold_root, []

        def hooked(path):  # a real directory renamed over the target just before it is held for the walk
            if path == target and not parked:
                parked.append(park(target))
                os.rename(decoy, target)
            return real(path)
        with mock.patch.object(fdsafe, "hold_root", hooked):
            result = fx.run()
        self.assertRefused(result, target)
        self.assertIn("changed between its stat and its walk", result[2])
        self.assertNothingWritten()
        self.assertEqual((os.listdir(parked[0]), os.listdir(target)), (["a.txt"], ["decoy.txt"]))

    def test_target_directory_with_the_same_inode_on_another_device_refuses(self):
        fx = self.fx
        target, real = f"{fx.dst}/x", os.lstat
        os.mkdir(target)

        def hooked(path, *args, **kwargs):  # the target's lstat says another device, same inode
            st = real(path, *args, **kwargs)
            if path == os.path.basename(target) and "dir_fd" in kwargs:
                fields = list(st)
                fields[2] += 1  # st_dev
                return os.stat_result(fields)
            return st
        with mock.patch.object(os, "lstat", hooked):
            result = fx.run()
        self.assertRefused(result, target)
        self.assertIn("changed between its stat and its walk", result[2])
        self.assertNothingWritten()

    def test_eio_on_fstat_of_a_held_target_directory_refuses(self):
        fx = self.fx
        target = f"{fx.dst}/x"
        os.mkdir(target)
        start = open_fds()
        with FK.inject_oserror("fstat", 1, errno.EIO, match=lambda fd: getpath(fd) == target):
            result = fx.run()
        self.assertRefused(result, target, "EIO")
        self.assertNothingWritten()
        self.assertEqual(open_fds(), start)


class Round1Inputs(Base):
    """Rulings 2, 5, 6 and 8: --out placement, LeafRecord fields, tab/CR/LF at parse time, three guards."""

    def check(self, path, says=None, argv=None):
        result = self.fx.run(argv)
        self.assertRefused(result, path)
        if says is not None:
            self.assertIn(says, result[2])
        self.assertNothingWritten()

    def test_output_inside_or_equal_to_a_move_source_or_target_refuses_and_creates_nothing(self):
        fx = self.fx
        os.mkdir(f"{fx.dst}/x")
        for out, unit in ((fx.u("u1/ledger"), fx.u("u1")), (fx.u("u1/sub/ledger"), fx.u("u1")), (fx.u("u1"), fx.u("u1")),
                          (f"{fx.dst}/x/ledger", f"{fx.dst}/x"), (f"{fx.dst}/y", f"{fx.dst}/y")):
            with self.subTest(out=out):
                listing = (tree(fx.src), tree(fx.dst))
                result = fx.run(fx.argv(out=out))
                self.assertRefused(result, unit)
                self.assertIn("move source or target", result[2])
                self.assertEqual((tree(fx.src), tree(fx.dst)), listing)

    def test_leaf_record_fields_follow_the_wire_contract(self):
        fx = self.fx
        good = fx.leaf("u1/a.txt")
        wrong = {"kind": 1, "bytes": "6", "sha256": None, "link_text": 0, "inode": True, "nlink": "1"}
        for field, bad in wrong.items():
            for leaf in ({k: v for k, v in good.items() if k != field}, {**good, field: bad}):
                with self.subTest(leaf=leaf):
                    fx.m1 = fx.manifest("m1.json", "u1", leaves=[fx.leaf("u1/sub/b.bin"), leaf])
                    fx.write_plans(fx.entries())
                    self.check(fx.m1[0], f"leaves[1] ({good['source']!r}).{field}:")
        fx.m1 = fx.manifest("m1.json", "u1", leaves=[fx.leaf("u1/sub/b.bin"), {**good, "link_text": "text"}])
        fx.write_plans(fx.entries())
        self.assertEqual(fx.run()[0], 0)

    def test_tab_cr_and_lf_refuse_at_parse_time_whether_or_not_a_row_holds_them(self):
        for char in ("\t", "\r", "\n"):
            for case in ("entry id", "move source", "move target", "leaf source", "free-root label", "free-root path",
                         "walked name"):
                with self.subTest(char=char, case=case):
                    self.fx = fx = Fixture(self)
                    entries, argv = fx.entries(), fx.argv()
                    if case == "entry id":
                        entries[1]["id"], says = f"E{char}2", "entries[1].id"
                    elif case == "move source":
                        entries[0]["moves"].append({"source": fx.u(f"u1/a{char}b"), "target": f"{fx.dst}/z"})
                        says = "entries[0].moves[1].source"
                    elif case == "move target":
                        entries[0]["moves"][0]["target"], says = f"{fx.dst}/x{char}", "entries[0].moves[0].target"
                    elif case == "leaf source":  # the toolkit agrees and no other leaf has its bytes: no row holds it
                        leaf = {**fx.leaf("u2/e.txt"), "source": fx.u(f"u2/e{char}x")}
                        fx.m2 = fx.manifest("m2.json", "u2", leaves=[fx.leaf("u2/c.txt"), leaf])
                        entries = fx.entries()
                        fx.toolkit = os.path.join(fx.inp, "agrees.duckdb")
                        fx.make_db(fx.toolkit, [(fx.u("u1/a.txt"), sha(b"alpha\n")), (fx.u("u1/sub/b.bin"), sha(b"\x00\x01")),
                                                (fx.u("u2/c.txt"), sha(b"alpha\n")), (leaf["source"], sha(b"echo\n"))])
                        argv, says = fx.argv(), f"{fx.m2[0]} leaves[1].source"
                    elif case == "free-root label":
                        argv[argv.index("--free-root") + 1], says = f"D{char}X={fx.dst}", "--free-root"
                    elif case == "free-root path":
                        other = os.path.join(fx.base, f"d{char}w")
                        os.mkdir(other)
                        argv, says = fx.argv(extra=("--free-root", f"W={other}")), "--free-root"
                    else:
                        os.mkdir(f"{fx.dst}/x")
                        fx.write(f"{fx.dst}/x/a{char}b", b"")
                        says = f"{fx.dst}/x"
                    fx.write_plans(entries)
                    self.check("", says, argv)
                    self.assertIn("holds a tab or line break", self.fx.run(argv)[2])

    def test_plans_entry_without_moves_refuses(self):
        fx = self.fx
        entries = fx.entries()
        del entries[0]["moves"]
        fx.write_plans(entries)
        self.check("entries[0].moves")

    def test_non_json_constant_in_an_unused_plans_field_refuses(self):
        fx = self.fx
        fx.write_plans(json.dumps({"entries": fx.entries(), "ignored": float("nan")}).encode())
        self.check(fx.plans, "non-JSON constant NaN")

    def test_existing_empty_output_directory_refuses(self):
        fx = self.fx
        os.mkdir(fx.out)
        self.assertRefused(fx.run(), fx.out, "EEXIST")
        self.assertEqual(os.listdir(fx.out), [])


class Round2Parse(Base):
    """Round 2 ruling 1 (and the ruling 5 sweep): every raw string passes one parse step before any use."""

    TEXT = (("NUL", "\0", "holds a NUL"), ("lone surrogate", "\udcff", "has no UTF-8 form"),
            ("tab", "\t", "holds a tab or line break"), ("CR", "\r", "holds a tab or line break"),
            ("LF", "\n", "holds a tab or line break"))
    NOT_NORMAL = "is not an absolute normalized path"

    def inputs(self):
        """(name, kind, apply, label): apply(fx, change) sets one raw input to change(its value), returns argv."""
        def cli(flag):
            def apply(fx, change):
                argv = fx.argv()
                argv[argv.index(flag) + 1] = change(argv[argv.index(flag) + 1])
                return argv
            return apply

        def free_root(fx, change, part):
            argv = fx.argv()
            argv[argv.index("--free-root") + 1] = f"{change('DD')}={fx.dst}" if part == "label" else f"D={change(fx.dst)}"
            return argv

        def entry(edit):
            def apply(fx, change):
                entries = fx.entries()
                edit(entries[0], change)
                fx.write_plans(entries)
                return fx.argv()
            return apply

        def leaf(field):
            def apply(fx, change):
                leaves = [fx.leaf("u1/a.txt"), fx.leaf("u1/sub/b.bin")]
                leaves[0][field] = change(leaves[0][field] or "link")
                fx.m1 = fx.manifest("m1.json", "u1", leaves=leaves)
                fx.write_plans(fx.entries())
                return fx.argv()
            return apply

        def move(key):
            return lambda e, change: e["moves"][0].update({key: change(e["moves"][0][key])})
        return (("--plans", "cli", cli("--plans"), "--plans path"),
                ("--requirements", "cli", cli("--requirements"), "--requirements path"),
                ("--toolkit-db", "cli", cli("--toolkit-db"), "--toolkit-db path"),
                ("--out", "cli", cli("--out"), "--out path"),
                ("--free-root label", "label", lambda fx, change: free_root(fx, change, "label"), "--free-root LABEL=PATH"),
                ("--free-root path", "cli", lambda fx, change: free_root(fx, change, "path"), "--free-root"),
                ("entry id", "label", entry(lambda e, change: e.update(id=change(e["id"]))), "entries[0].id"),
                ("replaces id", "label", entry(lambda e, change: e.update(replaces=[change(e["replaces"][0])])),
                 "entries[0].replaces[0]"),
                ("move source", "path", entry(move("source")), "entries[0].moves[0].source"),
                ("move target", "path", entry(move("target")), "entries[0].moves[0].target"),
                ("manifest", "path", entry(lambda e, change: e.update(manifest=change(e["manifest"]))), "entries[0].manifest"),
                ("manifest_sha256", "label", entry(lambda e, change: e.update(manifest_sha256=change(e["manifest_sha256"]))),
                 "entries[0].manifest_sha256"),
                ("leaf source", "path", leaf("source"), "leaves[0].source"),
                ("leaf kind", "label", leaf("kind"), "leaves[0].kind"),
                ("leaf sha256", "label", leaf("sha256"), "leaves[0].sha256"),
                ("leaf link_text", "label", leaf("link_text"), "leaves[0].link_text"))

    def refused(self, fx, argv, label, says):
        listing = tree(fx.base)
        result = fx.run(argv)
        self.assertRefused(result, label)
        self.assertIn(says, result[2])
        self.assertEqual(tree(fx.base), listing)

    def test_each_raw_string_with_a_nul_surrogate_tab_cr_or_lf_refuses_at_its_parse(self):
        for name, _, apply, label in self.inputs():
            for attack, char, says in self.TEXT:
                with self.subTest(input=name, attack=attack):
                    fx = Fixture(self)
                    self.refused(fx, apply(fx, lambda value: value[:-1] + char + value[-1:]), label, says)

    def test_each_path_that_is_relative_or_not_normalized_refuses_at_its_parse(self):
        changes = (("relative", lambda p: p.lstrip("/")), ("dot-dot", lambda p: f"{p}/../{os.path.basename(p)}"),
                   ("trailing slash", lambda p: p + "/"), ("dot", lambda p: f"{os.path.dirname(p)}/./{os.path.basename(p)}"),
                   ("double slash", lambda p: "/" + p))
        for name, kind, apply, label in self.inputs():
            for attack, change in changes:
                if kind == "label" or (kind == "cli" and attack == "relative"):
                    continue  # a label is no path; a relative CLI path is made absolute (Malformed.test_relative_paths...)
                with self.subTest(input=name, attack=attack):
                    fx = Fixture(self)
                    self.refused(fx, apply(fx, change), label, self.NOT_NORMAL)

    def test_annex_fields_refuse_at_their_parse_or_their_format(self):
        attacks = self.TEXT + (("dot-dot", None, self.NOT_NORMAL), ("trailing slash", None, self.NOT_NORMAL),
                               ("relative", None, self.NOT_NORMAL))
        by_format = {"tab": "fields, the header", "LF": "fields, the header", "CR": "needs LF line ends",
                     "lone surrogate": "is not UTF-8"}
        paths = {"dot-dot": lambda p: f"{p}/../u1", "trailing slash": lambda p: p + "/", "relative": lambda p: p.lstrip("/")}
        for column, index in (("requirement_id", 0), ("source", 1), ("action", 2)):
            for attack, char, says in attacks:
                if char is None and column != "source":
                    continue
                with self.subTest(column=column, attack=attack):
                    fx = Fixture(self)
                    row = ["MV-901", fx.u("u1"), "HOLD"]
                    row[index] = paths[attack](row[index]) if char is None else row[index][:-1] + char + row[index][-1:]
                    body = "".join(f"{r}\t{s}\t\t{a}\t0\tc\tl\tC-HOLD\tnone\tICM-R4\n"
                                   for r, s, a in (row, ("MV-902", fx.u("u2"), "HOLD")))
                    fx.write(fx.req, (REQ_HEADER + body).encode("utf-8", "surrogateescape"))
                    label = fx.req if attack in by_format else f"row 2 {column}"
                    self.refused(fx, fx.argv(), label, by_format.get(attack, says))

    def test_surrogate_in_each_cli_argument_is_a_one_line_refusal_without_traceback(self):
        fx = self.fx
        for flag in ("--plans", "--requirements", "--toolkit-db", "--free-root", "--out"):
            with self.subTest(flag=flag):
                argv = fx.argv()
                i = argv.index(flag) + 1
                argv[i] = "D\udcff=" + fx.dst if flag == "--free-root" else argv[i] + "\udcff"
                listing = tree(fx.base)
                proc = subprocess.run([sys.executable, "-B", SCRIPT, *argv], capture_output=True, text=True, timeout=60)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertEqual((proc.stdout, proc.stderr.count("\n")), ("", 1), proc.stderr)
                self.assertIn(flag, proc.stderr)
                self.assertIn("has no UTF-8 form", proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertEqual(tree(fx.base), listing)

    def test_nul_in_a_manifest_parent_refuses_before_any_open(self):
        fx = self.fx
        entries = fx.entries()
        entries[0]["manifest"] = fx.inp + "/bad\0dir/m.json"
        fx.write_plans(entries)
        self.refused(fx, fx.argv(), "entries[0].manifest", "holds a NUL")

    def test_a_walked_name_with_no_utf8_form_refuses(self):
        fx = self.fx
        os.mkdir(f"{fx.dst}/x")
        name = "a\udcffb"  # APFS refuses such a name (EILSEQ): another filesystem's walk could give one

        def walk(root, visit):
            visit(fdsafe.Entry(root.fd, name, os.path.join(root.path, name), name, os.lstat(root.path)))
        with mock.patch.object(fdsafe, "walk", walk):
            result = fx.run()
        self.assertRefused(result, f"{fx.dst}/x")
        self.assertIn("has no UTF-8 form", result[2])
        self.assertNothingWritten()

    def test_eio_on_the_working_directory_refuses(self):
        def fail():
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with mock.patch.object(os, "getcwd", fail):
            result = self.fx.run()
        self.assertRefused(result, "--free-root", "EIO")
        self.assertNothingWritten()


class Round2Fences(Base):
    """Round 2 rulings 2 and 3: units and free roots are fenced by held identity; one owner writes the reports."""

    def alias_plans(self, alias):
        """Plans, annex and manifests that name the units through alias, a link to src."""
        fx = self.fx
        swap = lambda p: p.replace(fx.src, alias)
        fx.write_req([("MV-901", swap(fx.u("u1")), "HOLD"), ("MV-902", swap(fx.u("u2")), "HOLD")])
        for name, unit in (("m1", "u1"), ("m2", "u2")):
            leaves = [{**fx.leaf(rel), "source": swap(fx.u(rel))} for rel in sorted(fx.data) if rel.startswith(unit + "/")]
            setattr(fx, name, fx.manifest(f"{name}.json", unit, leaves=leaves))
        entries = fx.entries()
        for e in entries:
            e["moves"][0]["source"] = swap(e["moves"][0]["source"])
        fx.write_plans(entries)

    def test_a_move_source_named_through_a_link_refuses_and_writes_nothing(self):
        fx = self.fx
        alias = os.path.join(fx.base, "alias")
        os.symlink(fx.src, alias)
        self.alias_plans(alias)
        listing = tree(fx.base)
        out = fx.u("u1/ledger")
        self.assertRefused(fx.run(fx.argv(out=out)), os.path.join(alias, "u1"), "ENOTDIR")
        self.assertEqual(tree(fx.base), listing)

    def test_output_through_a_link_alias_of_a_source_refuses(self):
        fx = self.fx
        alias = os.path.join(fx.base, "alias")
        os.symlink(fx.src, alias)
        listing = tree(fx.base)
        result = fx.run(fx.argv(out=os.path.join(alias, "u1", "ledger")))
        self.assertRefused(result, fx.u("u1"))
        self.assertIn("move source or target", result[2])
        self.assertEqual(tree(fx.base), listing)

    def test_output_inside_a_source_moved_after_it_is_held_refuses(self):
        fx = self.fx
        moved, real = fx.u("u1-moved"), os.path.realpath

        def hooked(path):  # the output's parent is resolved after every unit is held
            os.rename(fx.u("u1"), moved)
            return real(path)
        with mock.patch.object(os.path, "realpath", hooked):
            result = fx.run(fx.argv(out=os.path.join(moved, "ledger")))
        self.assertRefused(result, fx.u("u1"))
        self.assertIn("move source or target", result[2])
        self.assertEqual(sorted(os.listdir(moved)), ["a.txt", "sub"])

    def hook_open(self, moves):
        """Patch os.open: before each report named in moves is opened, rename moves[name] = (from, to)."""
        real, seen = os.open, []

        def hooked(name, *args, **kwargs):
            if name in moves and "dir_fd" in kwargs:
                seen.append(name)
                os.rename(*moves[name])
            return real(name, *args, **kwargs)
        return mock.patch.object(os, "open", hooked), seen

    def test_output_moved_into_a_source_before_the_first_report_leaves_no_report_there(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, _ = self.hook_open({"drift.tsv": (fx.out, moved)})
        with patch:
            result = fx.run()
        self.assertRefused(result, fx.u("u1"))
        self.assertIn("move source or target; removed drift.tsv", result[2])
        self.assertEqual(os.listdir(moved), [])

    def test_output_moved_into_a_source_and_back_refuses_before_the_next_create(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, seen = self.hook_open({"drift.tsv": (fx.out, moved), "cross_unit_dups.tsv": (moved, fx.out)})
        with patch:
            result = fx.run()
        self.assertRefused(result, fx.u("u1"))
        self.assertEqual(seen, ["drift.tsv"])
        self.assertEqual(os.listdir(moved), [])

    def test_output_moved_into_a_source_at_the_last_create_has_every_report_removed(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, _ = self.hook_open({"capacity.tsv": (fx.out, moved)})
        with patch:
            result = fx.run()
        self.assertRefused(result, fx.u("u1"))
        self.assertIn("removed drift.tsv; removed cross_unit_dups.tsv; removed targets.tsv; removed capacity.tsv",
                      result[2])
        self.assertEqual(os.listdir(moved), [])

    def test_output_moved_into_a_free_root_between_creates_has_its_report_removed(self):
        fx = self.fx
        into, real, done = os.path.join(fx.dst, "ledger"), fdsafe.settle, []

        def hooked(held, roots):  # right after the first report's post-write checks pass
            where = real(held, roots)
            if not done:
                done.append(True)
                os.rename(fx.out, into)
            return where
        with mock.patch.object(fdsafe, "settle", hooked):
            result = fx.run()
        self.assertEqual(done, [True])
        self.assertRefused(result, fx.dst)
        self.assertIn("lies inside this free root; removed drift.tsv", result[2])
        self.assertEqual(os.listdir(into), [])

    def test_removal_that_fails_names_the_report_left_in_place(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, _ = self.hook_open({"drift.tsv": (fx.out, moved)})

        def fail(*args, **kwargs):
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with patch, mock.patch.object(os, "unlink", fail):
            result = fx.run()
        self.assertRefused(result, os.path.join(moved, "drift.tsv"), "EIO")
        self.assertIn("left in place", result[2])
        self.assertEqual(os.listdir(moved), ["drift.tsv"])

    def test_eio_on_stat_of_an_output_ancestor_refuses(self):
        real = os.stat

        def hooked(path, *args, **kwargs):  # the walk up from the held output parent: ".", "./..", ...
            if "dir_fd" in kwargs and path.startswith("."):
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "stat", hooked):
            result = self.fx.run()
        self.assertRefused(result, self.fx.outp, "EIO")
        self.assertNothingWritten()


class Round2Watch(Base):
    """Round 2 ruling 4: a change that only the file's vnode notes see, and one that only the parent's notes see."""

    def run_with(self, hooks):
        real = duckdb.connect
        with mock.patch.object(duckdb, "connect", lambda *a, **k: Con(real(*a, **k), [], hooks)):
            return self.fx.run()

    def test_toolkit_rewritten_in_place_and_restored_is_seen_by_the_file_watch(self):
        fx = self.fx
        other = os.path.join(fx.base, "other.duckdb")
        fx.make_db(other, [(fx.u("u1/a.txt"), sha(b"alpha\n")), (fx.u("u1/sub/b.bin"), None),
                           (fx.u("u2/c.txt"), sha(b"alpha\n"))])
        saved, replacement, before = readb(fx.toolkit), readb(other), os.lstat(fx.toolkit)
        self.assertEqual(len(saved), len(replacement))

        def put(data):  # same inode, size and mtime: no lstat and no parent event can see it
            with open(fx.toolkit, "r+b") as fh:
                fh.write(data)
            os.utime(fx.toolkit, ns=(before.st_atime_ns, before.st_mtime_ns))
        result = self.run_with({("before", "ATTACH"): lambda: put(replacement), ("after", "SELECT"): lambda: put(saved)})
        self.assertRefused(result, fx.toolkit)
        self.assertIn("kqueue", result[2])
        self.assertNothingWritten()
        after = os.lstat(fx.toolkit)
        self.assertEqual(ledger_db._identity(after), ledger_db._identity(before))

    def test_toolkit_directory_swapped_and_restored_is_seen_by_the_parent_watch(self):
        fx = self.fx
        other = os.path.join(fx.base, "other.duckdb")
        fx.make_db(other, [])
        parked = os.path.join(fx.base, "parked-in")

        def swap():  # the held toolkit file itself is not renamed: only its directory moves
            os.rename(fx.inp, parked)
            os.mkdir(fx.inp)
            fx.write(fx.toolkit, readb(other))

        def restore():
            os.unlink(fx.toolkit)
            os.rmdir(fx.inp)
            os.rename(parked, fx.inp)
        before = os.lstat(fx.toolkit)
        result = self.run_with({("before", "ATTACH"): swap, ("after", "SELECT"): restore})
        self.assertRefused(result, fx.toolkit)
        self.assertIn("kqueue", result[2])
        self.assertNothingWritten()
        self.assertEqual(ledger_db._identity(os.lstat(fx.toolkit)), ledger_db._identity(before))


class Round3Removal(Base):
    """Round 3 ruling 4: one exit callback removes every attempted report, whatever exception ends the write."""

    def move_at_open(self, report, to):
        """Patch os.open (as it is now): before report is first opened, rename --out to `to`."""
        real, fired, out = os.open, [], self.fx.out

        def hooked(name, *args, **kwargs):
            if name == report and not fired:
                fired.append(True)
                os.rename(out, to)
            return real(name, *args, **kwargs)
        return mock.patch.object(os, "open", hooked), fired

    def test_k7_output_moved_into_a_target_during_the_first_create_leaves_no_report_there(self):
        fx = self.fx
        target = f"{fx.dst}/x"
        os.mkdir(target)
        moved = os.path.join(target, "ledger")
        patch, fired = self.move_at_open("drift.tsv", moved)
        with patch:
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, os.path.join(moved, "drift.tsv"))
        self.assertEqual(os.listdir(moved), [])

    def test_k8_eio_on_a_write_after_the_output_moved_into_a_source_leaves_no_report_there(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, fired = self.move_at_open("drift.tsv", moved)
        with patch, FK.inject_oserror("write", 1, errno.EIO):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, os.path.join(fx.out, "drift.tsv"), "EIO")
        self.assertEqual(os.listdir(moved), [])

    def test_k9_eio_on_the_check_after_a_report_closed_inside_a_source_leaves_no_report_there(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        real_settle, real_stat, done = fdsafe.settle, os.stat, []

        def settle(held, roots):  # right after the first report's post-write checks pass, --out moves into u1
            where = real_settle(held, roots)
            if not done:
                done.append(True)
                os.rename(fx.out, moved)
            return where

        def stat(path, *args, **kwargs):  # then every ancestry check of --out fails, the fresh one too
            if done and path == "." and "dir_fd" in kwargs:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real_stat(path, *args, **kwargs)
        with mock.patch.object(fdsafe, "settle", settle), mock.patch.object(os, "stat", stat):
            result = fx.run()
        self.assertEqual(done, [True])
        self.assertRefused(result, fx.out, "EIO")
        self.assertEqual(os.listdir(moved), [])

    def test_a_create_that_fails_before_its_file_exists_inside_a_source_refuses_with_its_own_error(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        with FK.inject_oserror("open", 1, errno.EIO, match=named("drift.tsv")):
            patch, fired = self.move_at_open("drift.tsv", moved)
            with patch:
                result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, os.path.join(fx.out, "drift.tsv"), "EIO")
        self.assertNotIn("removal failed", result[2])
        self.assertEqual(os.listdir(moved), [])

    def test_a_failed_listing_for_the_removal_is_a_one_line_refusal_naming_what_is_left(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, fired = self.move_at_open("drift.tsv", moved)

        def fail(*args, **kwargs):
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with patch, FK.inject_oserror("write", 1, errno.EIO), mock.patch.object(os, "listdir", fail):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, moved, "EIO")
        self.assertIn("could not be listed for removal, left in place", result[2])
        self.assertEqual(os.listdir(moved), ["drift.tsv"])

    def test_an_unexpected_exception_from_the_fresh_check_propagates_chained_to_the_run_error(self):
        fx = self.fx
        moved = fx.u("u1/ledger")
        patch, fired = self.move_at_open("drift.tsv", moved)
        real = os.stat

        def stat(path, *args, **kwargs):  # after the move, the next ancestry check is the exit callback's
            if fired and path == "." and "dir_fd" in kwargs:
                raise RuntimeError("unexpected")
            return real(path, *args, **kwargs)
        with patch, FK.inject_oserror("write", 1, errno.EIO), mock.patch.object(os, "stat", stat):
            with self.assertRaises(RuntimeError) as caught:
                fx.run()
        self.assertIsInstance(caught.exception.__context__, fdsafe.Refusal)
        self.assertIn("left in place, incomplete", str(caught.exception.__context__))
        self.assertEqual(os.listdir(moved), [])

    def test_a_normal_exit_keeps_every_report_though_a_later_check_would_fail(self):
        fx = self.fx
        real, real_write, returned = os.stat, ledger_db._write, []

        def write(*args, **kwargs):  # the write owner's own checks pass
            lines = real_write(*args, **kwargs)
            returned.append(True)
            return lines

        def stat(path, *args, **kwargs):  # any ancestry check after the write owner returned fails
            if returned and path == "." and "dir_fd" in kwargs:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(ledger_db, "_write", write), mock.patch.object(os, "stat", stat):
            code, out, err = fx.run()
        self.assertEqual(returned, [True])
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))


class Round5HeldReports(Base):
 def test_report_moved_into_source_during_write(self):
  fx=self.fx; moved=fx.u('u1/drift.tsv'); real=os.write;fired=[]
  def write(fd,data):
   if not fired:
    fired.append(True);os.rename(os.path.join(fx.out,'drift.tsv'),moved)
   return real(fd,data)
  with mock.patch.object(os,'write',write):result=fx.run()
  self.assertEqual(result[0],2);self.assertFalse(os.path.exists(moved),'report remains inside source')
 def test_unexpected_cleanup_check_leaves_report_inside_source(self):
  fx=self.fx;moved=fx.u('u1/ledger');real_open=os.open;real_stat=os.stat;fired=[]
  def opened(name,*args,**kw):
   if name=='drift.tsv' and not fired:
    fired.append(True);os.rename(fx.out,moved)
   return real_open(name,*args,**kw)
  def stat(path,*args,**kw):
   if fired and path=='.' and 'dir_fd' in kw:raise RuntimeError('unexpected cleanup ancestry')
   return real_stat(path,*args,**kw)
  with mock.patch.object(os,'open',opened),mock.patch.object(os,'stat',stat),FK.inject_oserror('write',1,errno.EIO):
   with self.assertRaises(RuntimeError) as caught:fx.run()
  self.assertEqual(os.listdir(moved),[],'report remains inside source after unexpected cleanup exception')



class Round7MutantKills(Base):
    """RULING-7: one behaviour per guard that the ticket test did not reach."""

    def test_fdsafe_create_file_returns_the_live_path_of_the_file_it_wrote(self):
        fx = self.fx
        into = os.path.join(fx.base, "elsewhere")
        os.mkdir(into)
        parent, root = fdsafe.hold_root(into), fdsafe.hold_root(fx.src)
        try:
            where = fdsafe.create_file(parent, "r.tsv", b"x\n", [root])
        finally:
            fdsafe.close(parent.fd, into)
            fdsafe.close(root.fd, fx.src)
        self.assertEqual(where, os.path.join(into, "r.tsv"))
        self.assertEqual(readb(where), b"x\n")

    def test_eio_on_the_stat_of_a_report_by_its_live_name_is_a_one_line_refusal(self):
        fx, real, fired = self.fx, os.stat, []

        def stat(path, *args, **kwargs):  # the after-check binds drift.tsv's live name to the held fd
            if path == "drift.tsv" and "dir_fd" in kwargs and not fired:
                fired.append(True)
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "stat", stat):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, os.path.join(fx.out, "drift.tsv"), "EIO")
        self.assertEqual(sorted(os.listdir(fx.out)), sorted(REPORTS))

    def test_a_report_name_that_no_longer_holds_the_report_refuses_and_keeps_the_stranger(self):
        fx, real, fired = self.fx, fdsafe.live_path, []
        aside = os.path.join(fx.base, "elsewhere")
        os.mkdir(aside)
        stranger = os.path.join(fx.out, "drift.tsv")

        def live_path(fd, label):  # between drift.tsv's live path and its stat, another file takes the name
            where = real(fd, label)
            if os.path.basename(label) == "drift.tsv" and not fired:
                fired.append(True)
                os.rename(where, os.path.join(aside, "drift.tsv"))
                fx.write(where, b"stranger\n")
            return where
        with mock.patch.object(fdsafe, "live_path", live_path):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, stranger)
        self.assertIn("is not the held report; removal refused", result[2])
        self.assertEqual(readb(stranger), b"stranger\n")

    def test_removal_by_name_spares_a_stranger_at_the_name_of_a_held_report_moved_into_a_source(self):
        fx, real, done = self.fx, fdsafe.settle, []
        stranger = os.path.join(fx.out, "drift.tsv")

        def settle(held, roots):  # after drift.tsv settles it moves into u1 and a stranger takes its name
            where = real(held, roots)
            if not done:
                done.append(True)
                os.rename(where, fx.u("u1/drift.tsv"))
                fx.write(stranger, b"stranger\n")
            return where
        with mock.patch.object(fdsafe, "settle", settle):
            result = fx.run()
        self.assertEqual(done, [True])
        self.assertRefused(result, fx.u("u1"))
        self.assertFalse(os.path.lexists(fx.u("u1/drift.tsv")))
        self.assertEqual(os.listdir(fx.out), ["drift.tsv"])
        self.assertEqual(readb(stranger), b"stranger\n")

    def test_a_failed_removal_of_an_unheld_report_is_a_one_line_refusal_naming_it(self):
        fx, moved, real_open, fired = self.fx, self.fx.u("u1/ledger"), os.open, []

        def opened(name, *args, **kwargs):  # --out moves into u1 as drift.tsv is created; its write fails
            if name == "drift.tsv" and not fired:
                fired.append(True)
                os.rename(fx.out, moved)
            return real_open(name, *args, **kwargs)

        def fail(*args, **kwargs):
            raise OSError(errno.EIO, os.strerror(errno.EIO))
        with mock.patch.object(os, "open", opened), FK.inject_oserror("write", 1, errno.EIO), \
                mock.patch.object(os, "unlink", fail):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, os.path.join(moved, "drift.tsv"), "EIO")
        self.assertIn("its removal failed, left in place", result[2])
        self.assertEqual(os.listdir(moved), ["drift.tsv"])

if __name__ == "__main__":
    unittest.main()


class Round6SettledReports(Base):
    def test_report_moved_during_write_to_non_fence_is_refused_and_kept(self):
        fx = self.fx
        elsewhere = os.path.join(fx.base, "elsewhere")
        os.mkdir(elsewhere)
        moved = os.path.join(elsewhere, "drift.tsv")
        real, fired = os.write, []

        # [LAW:behavior-not-structure] A rename outside all fences still violates the create contract.
        def write(fd, data):
            if not fired:
                fired.append(True)
                os.rename(os.path.join(fx.out, "drift.tsv"), moved)
            return real(fd, data)

        with mock.patch.object(os, "write", write):
            result = fx.run()
        self.assertEqual(fired, [True])
        self.assertRefused(result, moved)
        self.assertIn("was moved during the write", result[2])
        self.assertTrue(os.path.isfile(moved))
        self.assertTrue(readb(moved))
