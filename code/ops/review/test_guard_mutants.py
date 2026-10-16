"""Tests for guard_mutants: each operator, each result, the exit contract and lane safety.

Every fixture lane is made in a temp directory; no real lane, branch or PR is touched.
The tool runs as a subprocess for the contract, and in-process (main) where an os
function is patched as a fault or race witness.
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
import textwrap
import unittest
from unittest import mock

import guard_mutants as gm

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_mutants.py")

MODULE = '''\
import os
import re

DIGEST = re.compile(r"[0-9a-f]{4}x+")


class Refusal(Exception):
    pass


def check(n):
    if n < 0:
        raise Refusal("negative")
    return n


def first(items):
    if not items:
        return None
    return items[0]


def flags():
    return os.O_WRONLY | os.O_CREAT | os.O_EXCL


def parse(text):
    try:
        return int(text)
    except ValueError:
        return None


def write_all(fd, data):
    view = memoryview(data)
    while view:
        view = view[os.write(fd, view):]
'''


def line_of(text: str) -> int:
    lines = MODULE.splitlines()
    hits = [i + 1 for i, line in enumerate(lines) if text in line]
    assert len(hits) == 1, (text, hits)
    return hits[0]


# Fixture test bodies. FULL kills every mutant; WEAK leaves exactly WEAK_SURVIVORS.
CHECK_FULL = """
self.assertEqual(guarded.check(1), 1)
with self.assertRaises(guarded.Refusal):
    guarded.check(-1)
"""
CHECK_WEAK = "self.assertEqual(guarded.check(1), 1)\n"
FIRST = "self.assertIsNone(guarded.first([]))\nself.assertEqual(guarded.first([5]), 5)\n"
FLAGS_FULL = "self.assertEqual(guarded.flags(), os.O_WRONLY | os.O_CREAT | os.O_EXCL)\n"
FLAGS_WEAK = "self.assertTrue(guarded.flags() & os.O_CREAT)\n"
DIGEST_FULL = """
self.assertTrue(guarded.DIGEST.fullmatch("abcdx"))
self.assertIsNone(guarded.DIGEST.fullmatch("x"))
self.assertIsNone(guarded.DIGEST.fullmatch("abcd"))
"""
DIGEST_WEAK = 'self.assertTrue(guarded.DIGEST.fullmatch("abcdx"))\nself.assertIsNone(guarded.DIGEST.fullmatch("x"))\n'
PARSE_FULL = """
self.assertEqual(guarded.parse("1"), 1)
self.assertIsNone(guarded.parse("z"))
with self.assertRaises(TypeError):
    guarded.parse(None)
"""
PARSE_WEAK = 'self.assertEqual(guarded.parse("1"), 1)\nself.assertIsNone(guarded.parse("z"))\n'
WRITE_FULL = """
got = []
def one(fd, view):
    got.append(bytes(view[:1]))
    return 1
with mock.patch.object(guarded.os, "write", one):
    guarded.write_all(7, b"abc")
self.assertEqual(b"".join(got), b"abc")
"""
WRITE_WEAK = """
r, w = os.pipe()
self.addCleanup(os.close, r)
self.addCleanup(os.close, w)
guarded.write_all(w, b"abc")
self.assertEqual(os.read(r, 10), b"abc")
"""
WRITES_INTO_COPY = """
with open("data/note.txt", "a") as fh:
    fh.write("changed by the test")
with open("data/new.txt", "w") as fh:
    fh.write("new")
"""
FULL = [CHECK_FULL, FIRST, FLAGS_FULL, DIGEST_FULL, PARSE_FULL, WRITE_FULL, WRITES_INTO_COPY]
WEAK = [CHECK_WEAK, FIRST, FLAGS_WEAK, DIGEST_WEAK, PARSE_WEAK, WRITE_WEAK]

L_RAISE = line_of('raise Refusal("negative")')
L_CHECK_IF = line_of("if n < 0:")
L_FIRST_IF = line_of("if not items:")
L_FLAGS = line_of("os.O_WRONLY | os.O_CREAT")
L_DIGEST = line_of("DIGEST = re.compile")
L_EXCEPT = line_of("except ValueError:")
L_LOOP = line_of("while view:")

ALL_KEYS = {
    ("raise-remove", L_RAISE, ""),
    ("negate-if", L_CHECK_IF, ""),
    ("negate-if", L_FIRST_IF, ""),
    ("flag-drop", L_FLAGS, "O_WRONLY"),
    ("flag-drop", L_FLAGS, "O_CREAT"),
    ("flag-drop", L_FLAGS, "O_EXCL"),
    ("regex-zero", L_DIGEST, "8"),
    ("regex-zero", L_DIGEST, "12"),
    ("except-class", L_EXCEPT, ""),
    ("except-remove", L_EXCEPT, ""),
    ("write-loop", L_LOOP, ""),
}
WEAK_SURVIVORS = {
    ("raise-remove", L_RAISE, ""),
    ("flag-drop", L_FLAGS, "O_WRONLY"),
    ("flag-drop", L_FLAGS, "O_EXCL"),
    ("regex-zero", L_DIGEST, "12"),
    ("except-class", L_EXCEPT, ""),
    ("write-loop", L_LOOP, ""),
}


def suite(bodies: list[str], prelude: str = "") -> str:
    out = ["import os", "import sys", "import time", "import unittest", "from unittest import mock",
           "import guarded", "", prelude, "", "class T(unittest.TestCase):"]
    for i, body in enumerate(bodies):
        out.append(f"    def test_{i}(self):")
        out.append(textwrap.indent(textwrap.dedent(body).strip("\n"), "        "))
    return "\n".join(out) + "\n"


def key(row: dict) -> tuple:
    parts = row["id"].split(":")
    tag = parts[4] if len(parts) > 4 else ""
    return (row["operator"], int(row["location"].rsplit(":", 1)[1]), tag)


def tree_digest(root: str) -> dict:
    """Every entry under root (lstat, no follow) with its bytes or link text."""
    seen = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in sorted(dirnames + filenames):
            path = os.path.join(dirpath, name)
            st = os.lstat(path)
            rel = os.path.relpath(path, root)
            if os.path.islink(path):
                seen[rel] = ("link", os.readlink(path))
            elif os.path.isdir(path):
                seen[rel] = ("dir", st.st_ino)
            else:
                with open(path, "rb") as fh:
                    seen[rel] = ("file", st.st_ino, st.st_mtime_ns, hashlib.sha256(fh.read()).hexdigest())
    return seen


_REAL_FCNTL = fcntl.fcntl


def real_getpath(fd: int) -> str:
    """The fd's real path, or "" for an fd that has none (a pipe); never patched."""
    try:
        return os.fsdecode(_REAL_FCNTL(fd, fcntl.F_GETPATH, bytes(1024)).split(b"\0", 1)[0])
    except OSError:
        return ""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="gm-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.lane = os.path.join(self.tmp, "lane")
        self.outdir = os.path.join(self.tmp, "outdir")
        self.tooltmp = os.path.join(self.tmp, "tooltmp")
        os.makedirs(os.path.join(self.lane, "pkg"))
        os.makedirs(os.path.join(self.lane, "data", "sub"))
        os.mkdir(self.outdir)
        os.mkdir(self.tooltmp)
        with open(os.path.join(self.lane, "pkg", "guarded.py"), "w") as fh:
            fh.write(MODULE)
        with open(os.path.join(self.lane, "data", "note.txt"), "w") as fh:
            fh.write("note\n")
        with open(os.path.join(self.lane, "data", "sub", "deep.txt"), "w") as fh:
            fh.write("deep\n")
        os.symlink("note.txt", os.path.join(self.lane, "data", "link"))
        with open(os.path.join(self.lane, ".git"), "w") as fh:  # a worktree's .git file: not copied
            fh.write("gitdir: /nonexistent\n")
        self.out = os.path.join(self.outdir, "out.json")
        self.set_suite(FULL)

    def set_suite(self, bodies, prelude=""):
        with open(os.path.join(self.lane, "pkg", "test_guarded.py"), "w") as fh:
            fh.write(suite(bodies, prelude))

    def cmd(self) -> str:
        return f"{sys.executable} -B -m unittest discover -s pkg -p test_guarded.py"

    def args(self, *extra, test=None, out=None, files=("pkg/guarded.py",)) -> list[str]:
        argv = []
        for f in files:
            argv += ["--file", f]
        return argv + ["--test", test if test is not None else self.cmd(), "--out", self.out if out is None else out, *extra]

    def run_tool(self, argv, timeout=240) -> subprocess.CompletedProcess:
        env = dict(os.environ, TMPDIR=self.tooltmp)
        env.pop("PYTHONPATH", None)
        return subprocess.run([sys.executable, "-B", TOOL, *argv], cwd=self.lane, env=env,
                              capture_output=True, text=True, timeout=timeout)

    def run_main(self, argv):
        old = os.getcwd()
        os.chdir(self.lane)
        self.addCleanup(os.chdir, old)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(tempfile, "tempdir", self.tooltmp):
            code = gm.main(argv)
        os.chdir(old)
        return code, out.getvalue(), err.getvalue()

    def run_main_bounded(self, argv, fifo: str, limit: float = 30):
        """run_main in a thread; a blocked FIFO open fails the test instead of hanging it."""
        import threading
        box = {}
        th = threading.Thread(target=lambda: box.update(r=self.run_main(argv)), daemon=True)
        th.start()
        th.join(limit)
        if th.is_alive():
            fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)  # release the blocked reader
            os.close(fd)
            th.join(limit)
            self.fail(f"the tool blocked on the FIFO {fifo}")
        return box["r"]

    def rows(self) -> list[dict]:
        with open(self.out) as fh:
            return json.load(fh)

    def assertRefused(self, code, err, *words):
        self.assertEqual(code, 2, err)
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        self.assertNotIn("Traceback", err)
        self.assertTrue(err.startswith("guard_mutants: refused: "), err)
        for w in words:
            self.assertIn(w, err)

    def assertNoScratchLeft(self):
        self.assertEqual(os.listdir(self.tooltmp), [])


class Operators(Base):
    def test_full_suite_kills_one_mutant_per_guard_and_exits_0(self):
        before = tree_digest(self.lane)
        proc = self.run_tool(self.args())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        rows = self.rows()
        self.assertEqual({key(r) for r in rows}, ALL_KEYS)
        self.assertEqual(len(rows), len(ALL_KEYS))
        self.assertEqual({r["result"] for r in rows}, {"killed"})
        for r in rows:
            self.assertEqual(set(r), {"id", "location", "operator", "change", "result", "detail", "allowed"})
            self.assertTrue(r["location"].startswith("pkg/guarded.py:"))
            self.assertIsNone(r["allowed"])
        self.assertEqual(tree_digest(self.lane), before)
        self.assertNoScratchLeft()

    def test_weak_suite_leaves_exactly_the_unkilled_mutants_and_exits_1(self):
        self.set_suite(WEAK)
        before = tree_digest(self.lane)
        proc = self.run_tool(self.args())
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        rows = self.rows()
        self.assertEqual({key(r) for r in rows}, ALL_KEYS)
        self.assertEqual({key(r) for r in rows if r["result"] == "survived"}, WEAK_SURVIVORS)
        self.assertEqual({key(r) for r in rows if r["result"] == "killed"}, ALL_KEYS - WEAK_SURVIVORS)
        for r in rows:
            if r["result"] == "survived":
                self.assertIn(r["id"], proc.stdout)
        self.assertEqual(tree_digest(self.lane), before)
        self.assertNoScratchLeft()

    def test_mutant_sources(self):
        with open(os.path.join(self.lane, "pkg", "guarded.py"), "rb") as fh:
            muts = {(m.operator, m.line, m.id.split(":")[4] if m.id.count(":") > 3 else ""): m
                    for m in gm.mutants_for("pkg/guarded.py", fh.read())}
        self.assertEqual(set(muts), ALL_KEYS)
        lines = {k: m.source.decode().splitlines() for k, m in muts.items()}
        self.assertEqual(lines[("raise-remove", L_RAISE, "")][L_RAISE - 1].strip(), "pass")
        self.assertEqual(lines[("negate-if", L_CHECK_IF, "")][L_CHECK_IF - 1].strip(), "if not (n < 0):")
        self.assertEqual(lines[("flag-drop", L_FLAGS, "O_EXCL")][L_FLAGS - 1].strip(),
                         "return (os.O_WRONLY | os.O_CREAT)")
        self.assertEqual(lines[("regex-zero", L_DIGEST, "8")][L_DIGEST - 1],
                         "DIGEST = re.compile('[0-9a-f]{0,4}x+')")
        self.assertEqual(lines[("regex-zero", L_DIGEST, "12")][L_DIGEST - 1],
                         "DIGEST = re.compile('[0-9a-f]{4}x*')")
        self.assertEqual(lines[("except-class", L_EXCEPT, "")][L_EXCEPT - 1].strip(), "except Exception:")
        self.assertEqual(lines[("write-loop", L_LOOP, "")][L_LOOP - 1].strip(), "os.write(fd, view)")
        for k, m in muts.items():
            other = [i for i, (a, b) in enumerate(zip(MODULE.splitlines(), lines[k])) if a != b]
            self.assertEqual(len(MODULE.splitlines()) - len(lines[k]) in (0, 1), True, k)
            self.assertTrue(other, k)

    def test_operator_shapes_beyond_the_fixture(self):
        src = textwrap.dedent('''\
            import os, re
            def f(fd, x, chunks):
                flags = os.O_RDONLY
                flags |= os.O_NOFOLLOW
                g = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                if x:
                    pass
                else:
                    raise ValueError(x)
                try:
                    pass
                except:
                    pass
                try:
                    pass
                except (OSError, ValueError) as exc:
                    raise
                except Exception:
                    pass
                for c in chunks:
                    fd.write(c)
                re.fullmatch(pattern=r"a{2,}b{1,3}c{,2}d*\\+[+]{2}", string=x)
                return x
            ''').encode()
        got = {(m.operator, m.line, m.id.split(":")[4] if m.id.count(":") > 3 else "")
               for m in gm.mutants_for("f.py", src)}
        self.assertEqual(got, {
            ("flag-drop", 4, "O_NOFOLLOW"), ("flag-drop", 5, "O_RDONLY"), ("flag-drop", 5, "O_CLOEXEC"),
            ("raise-remove", 9, ""), ("negate-if", 6, ""),
            ("except-remove", 12, ""), ("except-class", 16, ""), ("except-remove", 16, ""),
            ("except-remove", 18, ""), ("write-loop", 20, ""),
            ("regex-zero", 22, "1"), ("regex-zero", 22, "6"), ("regex-zero", 22, "23"),
        })
        for m in gm.mutants_for("f.py", src):
            compile(m.source, "f.py", "exec", dont_inherit=True)
        by = {(m.operator, m.line): m for m in gm.mutants_for("f.py", src)}
        self.assertIn(b"flags |= 0", by[("flag-drop", 4)].source)
        self.assertIn(b"except " + gm.NEVER.encode() + b":", by[("except-remove", 12)].source)

    def test_except_remove_lets_the_exception_through(self):
        ns = {}
        src = b"def f(t):\n    try:\n        return int(t)\n    except ValueError:\n        return None\n"
        (m,) = [m for m in gm.mutants_for("f.py", src) if m.operator == "except-remove"]
        exec(compile(m.source, "f.py", "exec"), ns)
        self.assertEqual(ns["f"]("3"), 3)
        with self.assertRaises(ValueError):
            ns["f"]("z")

    def test_allow_list_with_reasons_exits_0_and_marks_rows(self):
        self.set_suite(WEAK)
        proc = self.run_tool(self.args())
        self.assertEqual(proc.returncode, 1)
        survivors = [r for r in self.rows() if r["result"] == "survived"]
        allow = os.path.join(self.tmp, "allow.json")
        with open(allow, "w") as fh:
            json.dump([{"id": r["id"], "reason": "equivalent here"} for r in survivors], fh)
        out2 = os.path.join(self.outdir, "out2.json")
        proc = self.run_tool(self.args("--allow", allow, out=out2))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        with open(out2) as fh:
            rows = json.load(fh)
        self.assertEqual({r["id"] for r in rows if r["allowed"] == "equivalent here"}, {r["id"] for r in survivors})
        self.assertEqual({r["result"] for r in rows if r["allowed"]}, {"survived"})
        with open(allow, "w") as fh:
            json.dump([{"id": r["id"], "reason": "equivalent"} for r in survivors[1:]], fh)
        out3 = os.path.join(self.outdir, "out3.json")
        proc = self.run_tool(self.args("--allow", allow, out=out3))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(survivors[0]["id"], proc.stdout)

    def test_bad_allow_lists_are_refused_before_any_run(self):
        good = gm.mutants_for("pkg/guarded.py", MODULE.encode())[0].id
        cases = {
            "notjson": "{",
            "notlist": json.dumps({"id": good, "reason": "x"}),
            "itemnotobject": json.dumps([good]),
            "emptyreason": json.dumps([{"id": good, "reason": "  "}]),
            "reasonnotstr": json.dumps([{"id": good, "reason": 3}]),
            "extrakey": json.dumps([{"id": good, "reason": "x", "more": 1}]),
            "duplicate": json.dumps([{"id": good, "reason": "x"}, {"id": good, "reason": "y"}]),
            "unknownid": json.dumps([{"id": "pkg/guarded.py:1:0:raise-remove", "reason": "x"}]),
            "notutf8": b"\xff",
        }
        log = os.path.join(self.tmp, "runs.log")
        for name, body in cases.items():
            path = os.path.join(self.tmp, name + ".json")
            with open(path, "wb") as fh:
                fh.write(body if isinstance(body, bytes) else body.encode())
            proc = self.run_tool(self.args("--allow", path, test=f"echo run >> {log}"))
            self.assertRefused(proc.returncode, proc.stderr, "allow", ALLOW_WORDS[name])
            self.assertFalse(os.path.exists(self.out), name)
        self.assertFalse(os.path.exists(log))
        proc = self.run_tool(self.args("--allow", self.outdir, test=f"echo run >> {log}"))
        self.assertRefused(proc.returncode, proc.stderr, "not a regular file")
        self.assertFalse(os.path.exists(log))
        os.symlink(os.path.join(self.tmp, "duplicate.json"), os.path.join(self.tmp, "linked.json"))
        proc = self.run_tool(self.args("--allow", os.path.join(self.tmp, "linked.json")))
        self.assertRefused(proc.returncode, proc.stderr, "ELOOP")


ALLOW_WORDS = {
    "notjson": "not UTF-8 JSON", "notlist": "not a JSON list", "itemnotobject": "exactly {id, reason}",
    "emptyreason": "non-empty reason", "reasonnotstr": "non-empty reason", "extrakey": "exactly {id, reason}",
    "duplicate": "twice", "unknownid": "no mutant", "notutf8": "not UTF-8 JSON",
}


class Results(Base):
    def test_mutant_that_does_not_compile_is_error_and_never_runs(self):
        log = os.path.join(self.tmp, "runs.log")
        root_fd = gm.open_root(self.lane)
        self.addCleanup(os.close, root_fd)
        targets = gm.read_targets(root_fd, self.lane, ["pkg/guarded.py"])
        good = gm.mutants_for("pkg/guarded.py", targets["pkg/guarded.py"].data)[0]
        bad = gm.Mutant(id="pkg/guarded.py:1:0:raise-remove", rel="pkg/guarded.py", line=1,
                        operator="raise-remove", change="broken", source=b"def f(:\n")
        with mock.patch.object(tempfile, "tempdir", self.tooltmp), \
                gm.Session(self.lane, root_fd, targets, f"echo run >> {log}", 30) as s:
            s.baseline()
            result, detail = s.result(bad)
            self.assertEqual(result, "error")
            self.assertIn("does not compile", detail)
            with open(log) as fh:
                self.assertEqual(len(fh.readlines()), 1)
            self.assertEqual(s.result(good)[0], "survived")
            with open(log) as fh:
                self.assertEqual(len(fh.readlines()), 2)
        self.assertNoScratchLeft()

    def test_timeout_is_error_and_kills_the_test_process_group(self):
        pids = os.path.join(self.tmp, "pids")
        hang = """
        with open(os.environ["GM_PIDS"], "a") as fh:
            fh.write(f"{os.getpid()}\\n")
        try:
            guarded.check(-1)
        except guarded.Refusal:
            return
        time.sleep(120)
        """
        self.set_suite([hang, FIRST, FLAGS_FULL, DIGEST_FULL, PARSE_FULL, WRITE_FULL])
        env = dict(os.environ, TMPDIR=self.tooltmp, GM_PIDS=pids)
        # A compound command: sh cannot exec the test, so only a group kill reaches it.
        argv = self.args("--timeout", "4", test=self.cmd() + "; exit $?")
        proc = subprocess.run([sys.executable, "-B", TOOL, *argv], cwd=self.lane,
                              env=env, capture_output=True, text=True, timeout=240)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        rows = {key(r): r for r in self.rows()}
        for k in [("raise-remove", L_RAISE, ""), ("negate-if", L_CHECK_IF, "")]:
            self.assertEqual(rows[k]["result"], "error")
            self.assertIn("timeout", rows[k]["detail"])
        self.assertEqual({r["result"] for k, r in rows.items() if k[0] not in ("raise-remove",)
                          and k != ("negate-if", L_CHECK_IF, "")}, {"killed"})
        with open(pids) as fh:
            for pid in [int(p) for p in fh.read().split()]:
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid, 0)
        self.assertNoScratchLeft()

    def test_failing_baseline_is_refused_and_writes_nothing(self):
        proc = self.run_tool(self.args(test="exit 3"))
        self.assertRefused(proc.returncode, proc.stderr, "unmutated", "exit 3")
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()

    def test_baseline_timeout_is_refused(self):
        proc = self.run_tool(self.args("--timeout", "1", test="sleep 30"))
        self.assertRefused(proc.returncode, proc.stderr, "unmutated", "timeout")
        self.assertFalse(os.path.exists(self.out))

    def test_test_runs_in_the_copy_with_its_own_env(self):
        probe = os.path.join(self.tmp, "probe")
        cmd = f'printf "%s\\n%s\\n%s\\n%s\\n" "$PWD" "$LLMDB_ROOT" "$TMPDIR" "${{PYTHONPATH-unset}}" > {probe}; ' \
              f'test -f pkg/guarded.py && test -L data/link && test ! -e .git'
        env = dict(os.environ, TMPDIR=self.tooltmp, PYTHONPATH=os.path.join(self.lane, "pkg"))
        proc = subprocess.run([sys.executable, "-B", TOOL, *self.args(test=cmd)], cwd=self.lane, env=env,
                              capture_output=True, text=True, timeout=240)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        with open(probe) as fh:
            pwd, root, tmpdir, pypath = fh.read().splitlines()
        self.assertEqual(pwd, root)
        self.assertNotEqual(os.path.realpath(pwd), self.lane)
        self.assertTrue(pwd.startswith(self.tooltmp + "/"), pwd)
        self.assertTrue(tmpdir.startswith(os.path.dirname(pwd)), tmpdir)
        self.assertEqual(pypath, "unset")
        self.assertEqual({r["result"] for r in self.rows()}, {"survived"})


class Contract(Base):
    def test_bad_invocation_exits_2(self):
        for argv in [[], ["--file", "pkg/guarded.py", "--test", "true"], ["--test", "true", "--out", self.out],
                     self.args("--bogus"), self.args("--timeout", "0"), self.args("--timeout", "x")]:
            proc = self.run_tool(argv)
            self.assertEqual(proc.returncode, 2, (argv, proc.stderr))
            self.assertFalse(os.path.exists(self.out))

    def test_existing_output_is_never_overwritten(self):
        with open(self.out, "w") as fh:
            fh.write("keep")
        log = os.path.join(self.tmp, "runs.log")
        proc = self.run_tool(self.args(test=f"echo run >> {log}"))
        self.assertRefused(proc.returncode, proc.stderr, self.out, "exists")
        self.assertFalse(os.path.exists(log))  # refused before any run
        with open(self.out) as fh:
            self.assertEqual(fh.read(), "keep")
        dangling = os.path.join(self.outdir, "dangling.json")
        os.symlink(os.path.join(self.tmp, "nowhere.json"), dangling)
        proc = self.run_tool(self.args(out=dangling))
        self.assertRefused(proc.returncode, proc.stderr, dangling)
        self.assertFalse(os.path.lexists(os.path.join(self.tmp, "nowhere.json")))

    def test_output_that_names_no_file_is_refused_before_any_run(self):
        log = os.path.join(self.tmp, "runs.log")
        for out in ["", self.outdir + "/.", self.outdir + "/.."]:
            proc = self.run_tool(self.args(out=out, test=f"echo run >> {log}"))
            self.assertRefused(proc.returncode, proc.stderr, "names no file")
            self.assertFalse(os.path.exists(log), out)

    def test_output_inside_the_lane_or_without_parent_is_refused(self):
        for out in [os.path.join(self.lane, "data", "out.json"), os.path.join(self.lane, "out.json"),
                    os.path.join(self.tmp, "missing", "out.json"), self.outdir + "/."]:
            before = tree_digest(self.lane)
            proc = self.run_tool(self.args(out=out))
            self.assertRefused(proc.returncode, proc.stderr)
            self.assertFalse(os.path.exists(out) and os.path.isfile(out), out)
            self.assertEqual(tree_digest(self.lane), before)

    def test_bad_target_files_are_refused(self):
        os.symlink("guarded.py", os.path.join(self.lane, "pkg", "alias.py"))
        with open(os.path.join(self.tmp, "outside.py"), "w") as fh:
            fh.write("x = 1\n")
        with open(os.path.join(self.lane, "pkg", "broken.py"), "w") as fh:
            fh.write("def f(:\n")
        with open(os.path.join(self.lane, "pkg", "latin.py"), "wb") as fh:
            fh.write(b"x = '\xe9'\n")
        os.symlink(os.path.join(self.lane, "pkg"), os.path.join(self.lane, "pkglink"))
        cases = {
            ("../outside.py",): "outside", (os.path.join(self.tmp, "outside.py"),): "outside",
            ("pkg/alias.py",): "regular", ("pkg",): "regular", ("pkg/missing.py",): "ENOENT",
            ("pkg/broken.py",): "parse", ("pkg/latin.py",): "UTF-8", ("pkglink/guarded.py",): "[ENOTDIR]",  # macOS: O_DIRECTORY on a link
            ("pkg/../pkg/guarded.py",): "..", ("pkg/guarded.py", "./pkg/guarded.py"): "twice",
            (".git",): "inside .git",
        }
        for files, word in cases.items():
            proc = self.run_tool(self.args(files=files))
            self.assertRefused(proc.returncode, proc.stderr, word)
            self.assertFalse(os.path.exists(self.out), files)

    def test_special_file_in_the_lane_is_refused_without_blocking(self):
        os.mkfifo(os.path.join(self.lane, "data", "fifo"))
        proc = self.run_tool(self.args(), timeout=60)
        self.assertRefused(proc.returncode, proc.stderr, "special", "data/fifo")
        self.assertFalse(os.path.exists(self.out))

    def test_links_that_leave_the_lane_are_refused(self):
        for target in [os.path.join(self.lane, "data", "note.txt"), "../../outside", "sub/../../.."]:
            link = os.path.join(self.lane, "data", "esc")
            os.symlink(target, link)
            proc = self.run_tool(self.args())
            self.assertRefused(proc.returncode, proc.stderr, "data/esc")
            self.assertFalse(os.path.exists(self.out))
            os.unlink(link)
        os.symlink("sub/../note.txt", os.path.join(self.lane, "data", "ok"))
        proc = self.run_tool(self.args())
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_lane_changed_by_the_test_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        proc = self.run_tool(self.args(test=f"printf x >> {note}"))
        self.assertRefused(proc.returncode, proc.stderr, "changed", "data/note.txt")
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()

    def test_lane_changed_after_the_last_copy_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        flag = os.path.join(self.tmp, "count")
        # The 12th run (the last mutant) changes the lane: only the final scan can see it.
        cmd = f'n=$(cat {flag} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {flag}; ' \
              f'if [ $n -ge 12 ]; then echo extra >> {note}; fi; true'
        proc = self.run_tool(self.args(test=cmd))
        self.assertRefused(proc.returncode, proc.stderr, "changed", "data/note.txt")
        self.assertFalse(os.path.exists(self.out))

    def test_lane_changed_and_restored_between_copies_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        flag = os.path.join(self.tmp, "count")
        cmd = f'n=$(cat {flag} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {flag}; ' \
              f'if [ $n -eq 1 ]; then mv {note} {note}.x; fi; if [ $n -eq 2 ]; then mv {note}.x {note}; fi; true'
        proc = self.run_tool(self.args(test=cmd))
        self.assertRefused(proc.returncode, proc.stderr, "changed", "data/note.txt")
        self.assertFalse(os.path.exists(self.out))

    def test_target_edited_in_place_with_its_mtime_kept_is_refused(self):
        target = os.path.join(self.lane, "pkg", "guarded.py")
        flag = os.path.join(self.tmp, "done")
        edit = (f"import os; st = os.stat({target!r}); b = open({target!r}, 'rb').read(); "
                f"open({target!r}, 'r+b').write(b.replace(b'n < 0', b'n > 0')); "
                f"os.utime({target!r}, ns=(st.st_atime_ns, st.st_mtime_ns))")
        cmd = f'if [ ! -e {flag} ]; then touch {flag}; {sys.executable} -c "{edit}"; fi; true'
        proc = self.run_tool(self.args(test=cmd))
        self.assertRefused(proc.returncode, proc.stderr, "pkg/guarded.py", "changed since it was parsed")
        self.assertFalse(os.path.exists(self.out))

    def test_each_mutant_copy_is_removed_before_the_next(self):
        log = os.path.join(self.tmp, "dirs.log")
        proc = self.run_tool(self.args(test=f'ls "$PWD/../.." >> {log}; echo --- >> {log}'))
        self.assertEqual(proc.returncode, 1, proc.stderr)
        with open(log) as fh:
            blocks = fh.read().split("---\n")[:-1]
        self.assertEqual(len(blocks), 12)
        for block in blocks:
            self.assertEqual(len(block.split()), 1, block)
        self.assertNoScratchLeft()

    def test_target_changed_during_the_run_is_refused(self):
        target = os.path.join(self.lane, "pkg", "guarded.py")
        proc = self.run_tool(self.args(test=f"printf '#' >> {target}"))
        self.assertRefused(proc.returncode, proc.stderr, "pkg/guarded.py")
        self.assertFalse(os.path.exists(self.out))


class Races(Base):
    """Swap a bound object between scan and open, by patching an os function as the witness."""

    def swap_on_open(self, name, action, flags_has=None):
        real = os.open
        fired = []

        def hooked(path, flags, *a, **kw):
            if path == name and not fired and kw.get("dir_fd") is not None and \
                    (flags_has is None or flags & flags_has):
                fired.append(path)
                action()
            return real(path, flags, *a, **kw)
        return mock.patch.object(gm.os, "open", hooked), fired

    def test_file_swapped_for_a_symlink_before_open_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        secret = os.path.join(self.tmp, "secret.txt")
        with open(secret, "w") as fh:
            fh.write("secret")

        def swap():
            os.rename(note, note + ".moved")
            os.symlink(secret, note)
        patch, fired = self.swap_on_open("note.txt", swap)
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "data/note.txt", "ELOOP")
        self.assertFalse(os.path.exists(self.out))

    def test_file_replaced_before_open_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")

        def replace():
            with open(note + ".new", "w") as fh:
                fh.write("note\n")
            os.rename(note + ".new", note)
        patch, fired = self.swap_on_open("note.txt", replace)
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "data/note.txt", "changed before it was read")

    def test_file_changed_while_read_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        ino = os.lstat(note).st_ino
        real_read, real_fstat = os.read, os.fstat
        fired = []

        def hooked(fd, n):
            data = real_read(fd, n)
            if not fired and real_fstat(fd).st_ino == ino:
                fired.append(fd)
                with open(note, "a") as fh:
                    fh.write("more")
            return data
        with mock.patch.object(gm.os, "read", hooked):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "data/note.txt", "changed while it was read")

    def test_directory_swapped_for_a_symlink_before_open_is_refused(self):
        data = os.path.join(self.lane, "data")
        elsewhere = os.path.join(self.tmp, "elsewhere")

        def swap():
            os.rename(data, elsewhere)
            os.symlink(elsewhere, data)
        patch, fired = self.swap_on_open("data", swap, os.O_DIRECTORY)
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "data")
        self.assertTrue("[ENOTDIR]" in err or "[ELOOP]" in err, err)  # macOS gives ENOTDIR

    def test_directory_replaced_before_open_is_refused(self):
        data = os.path.join(self.lane, "data")

        def replace():
            os.rename(data, os.path.join(self.tmp, "old-data"))
            os.mkdir(data)
        patch, fired = self.swap_on_open("data", replace, os.O_DIRECTORY)
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "data", "changed during the walk")

    def test_fifo_in_place_of_a_directory_or_file_refuses_without_blocking(self):
        for name, flags in [("data", os.O_DIRECTORY), ("note.txt", None)]:
            with self.subTest(name=name):
                self.setUp()
                path = os.path.join(self.lane, "data", "note.txt") if name == "note.txt" \
                    else os.path.join(self.lane, "data")

                def swap(path=path):
                    os.rename(path, path + ".gone")
                    os.mkfifo(path)
                patch, fired = self.swap_on_open(name, swap, flags)
                with patch:
                    code, out, err = self.run_main_bounded(self.args(test="true"), path)
                self.assertTrue(fired)
                self.assertRefused(code, err, name)
                if name == "note.txt":
                    self.assertIn("changed before it was read", err)

    def test_target_swapped_for_a_symlink_before_read_is_refused(self):
        target = os.path.join(self.lane, "pkg", "guarded.py")
        decoy = os.path.join(self.tmp, "decoy.py")
        with open(decoy, "w") as fh:
            fh.write("x = 1\n")

        def swap():
            os.rename(target, target + ".moved")
            os.symlink(decoy, target)
        patch, fired = self.swap_on_open("guarded.py", swap)
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "pkg/guarded.py", "ELOOP")

    def test_output_parent_moved_into_the_lane_during_the_write_is_refused_and_kept(self):
        moved = os.path.join(self.lane, "data", "moved-out")
        real = os.open
        fired = []

        def hooked(path, flags, *a, **kw):
            fd = real(path, flags, *a, **kw)
            if path == "out.json" and flags & os.O_CREAT and not fired:
                fired.append(fd)
                os.rename(self.outdir, moved)
            return fd
        with mock.patch.object(gm.os, "open", hooked):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "moved-out/out.json", "inside")
        self.assertTrue(os.path.isfile(os.path.join(moved, "out.json")))

    def test_output_created_after_the_check_is_never_overwritten(self):
        real = os.open
        fired = []

        def hooked(path, flags, *a, **kw):
            if path == "out.json" and flags & os.O_CREAT and not fired:
                fired.append(path)
                with open(self.out, "w") as fh:
                    fh.write("keep")
            return real(path, flags, *a, **kw)
        with mock.patch.object(gm.os, "open", hooked):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, self.out, "EEXIST")
        with open(self.out) as fh:
            self.assertEqual(fh.read(), "keep")

    def test_output_file_renamed_during_the_write_is_refused_and_kept(self):
        real = os.open
        fired = []

        def hooked(path, flags, *a, **kw):
            fd = real(path, flags, *a, **kw)
            if path == "out.json" and flags & os.O_CREAT and not fired:
                fired.append(fd)
                os.rename(self.out, os.path.join(self.outdir, "other.json"))
            return fd
        with mock.patch.object(gm.os, "open", hooked):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "other.json")
        self.assertTrue(os.path.isfile(os.path.join(self.outdir, "other.json")))


class Faults(Base):
    """An injected EIO per call class is one refusal line naming the path and the errno."""

    def eio(self, target, fn_name, predicate, after=False):
        real = getattr(target, fn_name)
        fired = []

        def hooked(*a, **kw):
            if not fired and predicate(*a, **kw):
                fired.append(a)
                if after:
                    real(*a, **kw)
                raise OSError(errno.EIO, "Input/output error")
            return real(*a, **kw)
        return mock.patch.object(target, fn_name, hooked), fired

    def check_eio(self, patch, fired, *words):
        with patch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "EIO", *words)
        return code, err

    def ino(self, *parts):
        return os.lstat(os.path.join(self.lane, *parts)).st_ino

    def test_eio_open(self):
        p, f = self.eio(gm.os, "open", lambda path, *a, **k: path == "note.txt")
        self.check_eio(p, f, "data/note.txt")

    def test_eio_scandir(self):
        ino, real_fstat = self.ino("data"), os.fstat
        p, f = self.eio(gm.os, "scandir", lambda fd=None: isinstance(fd, int) and real_fstat(fd).st_ino == ino)
        self.check_eio(p, f, "data")

    def test_eio_read(self):
        ino, real_fstat = self.ino("data", "note.txt"), os.fstat
        p, f = self.eio(gm.os, "read", lambda fd, n: real_fstat(fd).st_ino == ino)
        self.check_eio(p, f, "data/note.txt")

    def test_eio_fstat(self):
        ino, real_fstat = self.ino("data", "note.txt"), os.fstat
        p, f = self.eio(gm.os, "fstat", lambda fd: real_fstat(fd).st_ino == ino)
        self.check_eio(p, f, "data/note.txt")

    def test_eio_readlink(self):
        p, f = self.eio(gm.os, "readlink", lambda path, *a, **k: path == "link")
        self.check_eio(p, f, "data/link")

    def test_eio_mkdir_in_scratch(self):
        p, f = self.eio(gm.os, "mkdir", lambda path, *a, **k: path == "sub")
        self.check_eio(p, f, "data/sub")
        self.assertNoScratchLeft()

    def test_eio_write_output(self):
        p, f = self.eio(gm.os, "write", lambda fd, data: real_getpath(fd) == self.out)
        self.check_eio(p, f, self.out, "incomplete")
        self.assertTrue(os.path.isfile(self.out))

    def test_short_writes_still_give_the_exact_output(self):
        real = os.write
        calls = []

        def one_byte(fd, data):
            calls.append(fd)
            return real(fd, bytes(memoryview(data)[:1]))
        with mock.patch.object(gm.os, "write", one_byte):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(code, 1, err)
        rows = self.rows()
        self.assertEqual({key(r) for r in rows}, ALL_KEYS)
        self.assertEqual({r["result"] for r in rows}, {"survived"})
        with open(os.path.join(self.lane, "pkg", "guarded.py")) as fh:
            self.assertEqual(fh.read(), MODULE)

    def test_eio_close_output_keeps_it(self):
        p, f = self.eio(gm.os, "close", lambda fd: real_getpath(fd) == self.out, after=True)
        self.check_eio(p, f, self.out, "left in place")
        self.assertTrue(os.path.isfile(self.out))
        self.rows()

    def test_eio_getpath_of_output_parent(self):
        def pred(fd, cmd, *a):
            return cmd == fcntl.F_GETPATH and real_getpath(fd) == self.outdir
        p, f = self.eio(gm.fcntl, "fcntl", pred)
        self.check_eio(p, f, self.outdir)
        self.assertFalse(os.path.exists(self.out))

    def test_eio_open_output_parent(self):
        p, f = self.eio(gm.os, "open", lambda path, *a, **k: path == self.outdir)
        self.check_eio(p, f, self.outdir)

    def test_non_oserror_still_propagates(self):
        ino, real_fstat = self.ino("data"), os.fstat
        real = os.scandir

        def hooked(fd=None):
            if isinstance(fd, int) and real_fstat(fd).st_ino == ino:
                raise RuntimeError("unexpected")
            return real(fd)
        with mock.patch.object(gm.os, "scandir", hooked), self.assertRaises(RuntimeError):
            self.run_main(self.args(test="true"))
        self.assertNoScratchLeft()


if __name__ == "__main__":
    unittest.main()
