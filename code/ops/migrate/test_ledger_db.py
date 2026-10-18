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
        _, _, msg = self.eio("close", 1, fx.dst, match=lambda fd: getpath(fd) == fx.dst)
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

        def hooked(path, *args, **kwargs):
            if path == target:
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

        def hooked(path, *args, **kwargs):
            if path == target:
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


if __name__ == "__main__":
    unittest.main()
