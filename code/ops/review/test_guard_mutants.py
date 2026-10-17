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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "tests"))
import fault_kit as fk  # noqa: E402  (code/tests/fault_kit.py: the standard filesystem attacks)

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
self.assertTrue(guarded.DIGEST.fullmatch("0123x"))
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
    ("class-drop", L_DIGEST, "1"),
    ("class-drop", L_DIGEST, "4"),
    ("except-class", L_EXCEPT, ""),
    ("except-remove", L_EXCEPT, ""),
    ("write-loop", L_LOOP, ""),
}
WEAK_SURVIVORS = {
    ("raise-remove", L_RAISE, ""),
    ("flag-drop", L_FLAGS, "O_WRONLY"),
    ("flag-drop", L_FLAGS, "O_EXCL"),
    ("regex-zero", L_DIGEST, "12"),
    ("class-drop", L_DIGEST, "1"),
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
            ("flag-drop", 4, "O_NOFOLLOW"), ("flag-drop", 5, "O_CLOEXEC"),
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

    def test_unexpected_error_while_waiting_for_the_test_surfaces(self):
        """Only a timeout becomes an error row; any other failure of the wait is not hidden as one."""
        proc = mock.Mock(pid=1 << 22)
        proc.wait.side_effect = [RuntimeError("unexpected wait failure"), 0]
        with mock.patch.object(gm.subprocess, "Popen", return_value=proc), \
                mock.patch.object(gm, "_kill_group"), self.assertRaises(RuntimeError):
            gm._execute("true", self.lane, self.tooltmp, 1)

    def test_kill_group_failure_other_than_a_gone_group_surfaces(self):
        """A group that cannot be killed is reported, never taken for a group that is gone."""
        with mock.patch.object(gm.os, "killpg", side_effect=PermissionError(errno.EPERM, "Operation not permitted")) \
                as killpg, self.assertRaises(PermissionError):
            gm._kill_group(1 << 22)
        killpg.assert_called_once_with(1 << 22, gm.signal.SIGKILL)
        with mock.patch.object(gm.os, "killpg", side_effect=ProcessLookupError(errno.ESRCH, "No such process")):
            self.assertIsNone(gm._kill_group(1 << 22))


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
        proc = self.run_tool(self.args("--jobs", "1", test=f"printf x >> {note}"))
        self.assertRefused(proc.returncode, proc.stderr, "changed", "data/note.txt")
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()

    def test_lane_changed_after_the_last_copy_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        flag = os.path.join(self.tmp, "count")
        # The 14th run (the last mutant) changes the lane: only the final scan can see it.
        cmd = f'n=$(cat {flag} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {flag}; ' \
              f'if [ $n -ge 14 ]; then echo extra >> {note}; fi; true'
        proc = self.run_tool(self.args("--jobs", "1", test=cmd))
        self.assertRefused(proc.returncode, proc.stderr, "changed", "data/note.txt")
        self.assertFalse(os.path.exists(self.out))

    def test_lane_changed_and_restored_between_copies_is_refused(self):
        note = os.path.join(self.lane, "data", "note.txt")
        flag = os.path.join(self.tmp, "count")
        cmd = f'n=$(cat {flag} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {flag}; ' \
              f'if [ $n -eq 1 ]; then mv {note} {note}.x; fi; if [ $n -eq 2 ]; then mv {note}.x {note}; fi; true'
        proc = self.run_tool(self.args("--jobs", "1", test=cmd))
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
        proc = self.run_tool(self.args("--jobs", "1", test=f'ls "$PWD/../.." >> {log}; echo --- >> {log}'))
        self.assertEqual(proc.returncode, 1, proc.stderr)
        with open(log) as fh:
            blocks = fh.read().split("---\n")[:-1]
        self.assertEqual(len(blocks), 14)
        for block in blocks:
            self.assertEqual(len(block.split()), 1, block)
        self.assertNoScratchLeft()

    def test_target_changed_during_the_run_is_refused(self):
        target = os.path.join(self.lane, "pkg", "guarded.py")
        proc = self.run_tool(self.args(test=f"printf '#' >> {target}"))
        self.assertRefused(proc.returncode, proc.stderr, "pkg/guarded.py")
        self.assertFalse(os.path.exists(self.out))

    def edit_at_run(self, n, rel, old, new):
        """A test command that, at run n, rewrites rel in the lane in place: same inode, size and mtime."""
        assert len(old) == len(new)
        target = os.path.join(self.lane, rel)
        count = os.path.join(self.tmp, "count")
        helper = os.path.join(self.tmp, "edit.py")
        with open(helper, "w") as fh:
            fh.write(textwrap.dedent(f"""\
                import os
                n = int(open({count!r}).read()) + 1 if os.path.exists({count!r}) else 1
                open({count!r}, "w").write(str(n))
                if n == {n}:
                    st = os.stat({target!r})
                    with open({target!r}, "rb") as fh:
                        data = fh.read()
                    assert {old!r} in data
                    with open({target!r}, "r+b") as fh:
                        fh.write(data.replace({old!r}, {new!r}))
                    os.utime({target!r}, ns=(st.st_atime_ns, st.st_mtime_ns))
                """))
        return target, f"{sys.executable} -B {helper} && {self.cmd()}"

    def assertEditedWithIdentityKept(self, target, before, marker):
        with open(target, "rb") as fh:
            self.assertIn(marker, fh.read())
        self.assertEqual(gm._identity(os.stat(target)), before)

    def test_test_file_rewritten_with_its_identity_kept_after_the_baseline_is_refused(self):
        # Run 2 makes the lane's fixture test fail on import: every later copy would "kill" every mutant.
        target, cmd = self.edit_at_run(2, "pkg/test_guarded.py", b"import guarded", b"assert False  ")
        before = gm._identity(os.stat(target))
        proc = self.run_tool(self.args("--jobs", "1", test=cmd))
        self.assertEditedWithIdentityKept(target, before, b"assert False")
        self.assertRefused(proc.returncode, proc.stderr, "changed", "pkg/test_guarded.py")
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()

    def test_product_file_rewritten_with_its_identity_kept_after_the_last_copy_is_refused(self):
        # Run 12 (the last mutant) changes the product after the last copy: only the final scan can see it.
        target, cmd = self.edit_at_run(12, "pkg/guarded.py", b"n < 0", b"n > 0")
        before = gm._identity(os.stat(target))
        proc = self.run_tool(self.args("--jobs", "1", test=cmd))
        self.assertEditedWithIdentityKept(target, before, b"n > 0")
        self.assertRefused(proc.returncode, proc.stderr, "changed", "pkg/guarded.py")
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()


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


class Scratch(Base):
    """The scratch lies outside the lane and is removed only through fds bound to what this run made."""

    def run_with_attack_on_exit(self, attack):
        """run_main with attack(scratch path) armed around the session's cleanup."""
        real_exit = gm.Session.__exit__
        box = {}

        def attacked_exit(session, *exc):
            box["scratch"] = session.scratch
            with attack(session.scratch) as fault:
                box["fault"] = fault
                return real_exit(session, *exc)
        with mock.patch.object(gm.Session, "__exit__", attacked_exit):
            code, out, err = self.run_main(self.args(test="true"))
        return code, err, box["scratch"], box["fault"]

    def assertBothKept(self, scratch, fault):
        self.assertEqual(fault.fired, 1)
        self.assertTrue(os.path.isdir(scratch) and not os.path.islink(scratch), scratch)  # the replacement
        self.assertEqual(os.listdir(scratch), [])
        self.assertTrue(os.path.isdir(fault.parked), fault.parked)  # the real scratch
        self.assertFalse(os.path.exists(self.out))

    def test_scratch_rebound_before_cleanup_is_refused_and_both_are_kept(self):
        code, err, scratch, fault = self.run_with_attack_on_exit(
            lambda s: fk.rename_and_rebind("close", 1, s, match=lambda fd: real_getpath(fd) == s))
        self.assertRefused(code, err, scratch, "kept")
        self.assertBothKept(scratch, fault)

    def test_scratch_rebound_during_cleanup_is_refused_and_both_are_kept(self):
        code, err, scratch, fault = self.run_with_attack_on_exit(
            lambda s: fk.rename_and_rebind("scandir", 1, s,
                                           match=lambda fd=None: isinstance(fd, int) and real_getpath(fd) == s))
        self.assertRefused(code, err, scratch, "kept")
        self.assertBothKept(scratch, fault)

    def test_mutant_copy_rebound_before_its_removal_is_refused_and_both_are_kept(self):
        root_fd = gm.open_root(self.lane)
        self.addCleanup(os.close, root_fd)
        targets = gm.read_targets(root_fd, self.lane, ["pkg/guarded.py"])
        with mock.patch.object(tempfile, "tempdir", self.tooltmp):
            session = gm.Session(self.lane, root_fd, targets, "true", 30)
            with self.assertRaises(gm.Refusal) as caught, session:
                copy = os.path.join(session.scratch, "m0001")
                # Call 1 opens the new copy; call 2 opens it for removal.
                with fk.rename_and_rebind("open", 2, copy, match=lambda p, *a, **k: p == "m0001" and
                                          k.get("dir_fd") is not None) as fault:
                    session.baseline()
        self.assertIn(copy, str(caught.exception))
        self.assertIn("kept", str(caught.exception))
        self.assertTrue(os.path.isdir(copy))
        self.assertEqual(os.listdir(copy), [])
        self.assertEqual(sorted(os.listdir(fault.parked)), ["lane", "tmp"])
        self.assertTrue(os.path.isfile(os.path.join(fault.parked, "lane", "pkg", "guarded.py")))

    def watch_creates(self):
        """Patches that record every directory, file or link the tool creates, by its real path."""
        made = []
        real_mkdir, real_open, real_symlink = os.mkdir, os.open, os.symlink

        def where(path, dir_fd):
            return os.path.join(real_getpath(dir_fd), path) if dir_fd is not None else os.path.abspath(path)

        def mkdir(path, *a, dir_fd=None, **kw):
            made.append(where(path, dir_fd))
            return real_mkdir(path, *a, dir_fd=dir_fd, **kw)

        def open_(path, flags, *a, dir_fd=None, **kw):
            if flags & os.O_CREAT:
                made.append(where(path, dir_fd))
            return real_open(path, flags, *a, dir_fd=dir_fd, **kw)

        def symlink(src, dst, *a, dir_fd=None, **kw):
            made.append(where(dst, dir_fd))
            return real_symlink(src, dst, *a, dir_fd=dir_fd, **kw)
        stack = contextlib.ExitStack()
        for name, fn in (("mkdir", mkdir), ("open", open_), ("symlink", symlink)):
            stack.enter_context(mock.patch.object(gm.os, name, fn))
        return stack, made

    def test_scratch_parent_in_the_lane_is_refused_with_no_write_in_the_lane(self):
        for parent in (os.path.join(self.lane, "tmp"), self.lane):
            with self.subTest(parent=parent):
                os.makedirs(parent, exist_ok=True)
                self.tooltmp = parent
                before = tree_digest(self.lane)
                stack, made = self.watch_creates()
                with stack:
                    code, out, err = self.run_main(self.args(test="true"))
                self.assertRefused(code, err, "scratch", "inside the lane")
                self.assertEqual([p for p in made if p == self.lane or p.startswith(self.lane + "/")], [])
                self.assertEqual(tree_digest(self.lane), before)
                self.assertFalse(os.path.exists(self.out))

    def test_scratch_moved_into_the_lane_after_it_is_made_is_refused(self):
        moved = os.path.join(self.lane, "moved")
        real = os.mkdir
        made = []

        def hooked(path, *a, **kw):
            result = real(path, *a, **kw)
            if not made and os.path.basename(path).startswith("guard_mutants-"):
                made.append(os.path.basename(path))
                os.rename(self.tooltmp, moved)
            return result
        with mock.patch.object(gm.os, "mkdir", hooked):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(len(made), 1)
        self.assertRefused(code, err, "scratch", "inside the lane")
        self.assertEqual(os.listdir(os.path.join(moved, made[0])), [])  # no copy was made, the scratch is kept
        self.assertFalse(os.path.exists(self.out))


class Bound(Base):
    """A pathname is used only while it still names the fd that was checked."""

    def arm_first_mutant(self, attack):
        """Patch Session._run so attack(that run's lane copy path) is armed around the first mutant run."""
        real_run = gm.Session._run
        box = {}

        def run(session, m, timeout):
            if m is None or "copy" in box:
                return real_run(session, m, timeout)
            box["copy"] = os.path.join(session.scratch, f"m{session.runs + 1:04d}", "lane")
            with attack(box["copy"]) as fault:
                box["fault"] = fault
                return real_run(session, m, timeout)
        return mock.patch.object(gm.Session, "_run", run), box

    def where(self, log):
        """A test command that logs whether its cwd is the populated copy."""
        return f"if test -f pkg/guarded.py; then echo held >> {log}; else echo empty >> {log}; fi"

    def rebound_copy(self, when):
        log = os.path.join(self.tmp, "where.log")
        patch, box = self.arm_first_mutant(lambda copy: fk.rename_and_rebind(
            fk.GETPATH, 1, copy, when=when, match=lambda fd, *a: real_getpath(fd) == copy))
        with patch:
            code, out, err = self.run_main(self.args("--jobs", "1", test=self.where(log)))
        self.assertEqual(box["fault"].fired, 1)
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(os.listdir(box["copy"]), [])  # the replacement is kept
        self.assertTrue(os.path.isfile(os.path.join(box["fault"].parked, "pkg", "guarded.py")))  # so is the copy
        with open(log) as fh:
            return code, err, box["copy"], fh.read().split()

    def test_copy_rebound_after_the_check_runs_the_test_in_the_held_copy_and_refuses(self):
        code, err, copy, where = self.rebound_copy("after")
        self.assertRefused(code, err, copy, "after the test run", "kept")
        self.assertEqual(where, ["held", "held"])  # the baseline, then the attacked mutant: never the empty path

    def test_copy_rebound_before_the_test_runs_is_refused_and_the_test_never_runs(self):
        code, err, copy, where = self.rebound_copy("before")
        self.assertRefused(code, err, copy, "before the test run", "kept")
        self.assertEqual(where, ["held"])  # the baseline only

    def test_replacement_directory_found_by_the_cleanup_scan_is_kept(self):
        for child in ("lane", os.path.join("lane", "pkg")):
            with self.subTest(child=child):
                self.setUp()
                real_remove = gm._remove_dir
                box = {}

                def remove(parent_fd, name, path, owned, child=child, box=box):
                    if name != "m0001" or box:
                        return real_remove(parent_fd, name, path, owned)
                    box["target"] = target = os.path.join(path, child)
                    scanned = os.path.dirname(target)
                    with fk.rename_and_rebind("scandir", 1, target, match=lambda fd=None: isinstance(fd, int)
                                              and real_getpath(fd) == scanned) as fault:
                        box["fault"] = fault
                        return real_remove(parent_fd, name, path, owned)
                with mock.patch.object(gm, "_remove_dir", remove):
                    code, out, err = self.run_main(self.args(test="true"))
                self.assertEqual(box["fault"].fired, 1)
                self.assertRefused(code, err, "kept")
                self.assertEqual(os.listdir(box["target"]), [])  # the replacement
                parked = box["fault"].parked
                self.assertTrue(os.path.isfile(os.path.join(parked, "guarded.py") if child != "lane"
                                               else os.path.join(parked, "pkg", "guarded.py")))
                self.assertFalse(os.path.exists(self.out))

    def test_a_removed_directory_leaves_the_ownership_record(self):
        """A recycled inode never inherits ownership: only the live scratch stays recorded."""
        root_fd = gm.open_root(self.lane)
        self.addCleanup(os.close, root_fd)
        targets = gm.read_targets(root_fd, self.lane, ["pkg/guarded.py"])
        with mock.patch.object(tempfile, "tempdir", self.tooltmp), \
                gm.Session(self.lane, root_fd, targets, "true", 30) as s:
            s.baseline()
            st = os.fstat(s.scratch_fd)
            self.assertEqual(s.owned, {(st.st_dev, st.st_ino)})
        self.assertEqual(s.owned, set())
        self.assertNoScratchLeft()

    def watch_lane_writes(self):
        real = os.write
        inside = []

        def write(fd, data):
            if real_getpath(fd).startswith(self.lane + "/"):
                inside.append(len(data))
            return real(fd, data)
        return mock.patch.object(gm.os, "write", write), inside

    def test_output_parent_moved_into_the_lane_at_the_create_writes_no_byte_inside(self):
        moved = os.path.join(self.lane, "data", "moved-out")
        real = os.open
        fired = []

        def opened(path, flags, *a, **kw):
            if path == "out.json" and flags & os.O_CREAT and not fired:
                fired.append(path)
                os.rename(self.outdir, moved)
            return real(path, flags, *a, **kw)
        watch, inside = self.watch_lane_writes()
        with mock.patch.object(gm.os, "open", opened), watch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "moved-out/out.json", "inside")
        self.assertEqual(inside, [])
        self.assertEqual(os.path.getsize(os.path.join(moved, "out.json")), 0)

    def test_output_parent_moved_into_the_lane_before_the_create_is_refused_and_creates_nothing(self):
        moved = os.path.join(self.lane, "data", "moved-out")
        real = gm.Session.verify_lane

        def verify(session):
            real(session)
            os.rename(self.outdir, moved)
        with mock.patch.object(gm.Session, "verify_lane", verify):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertRefused(code, err, "inside the lane")
        self.assertEqual(os.listdir(moved), [])

    def test_output_parent_moved_into_the_lane_at_the_first_write_is_refused_and_kept(self):
        moved = os.path.join(self.lane, "data", "moved-out")
        real = os.write
        fired = []

        def write(fd, data):
            if not fired and real_getpath(fd) == self.out:
                fired.append(fd)
                os.rename(self.outdir, moved)
            return real(fd, data)
        with mock.patch.object(gm.os, "write", write):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired)
        self.assertRefused(code, err, "moved-out/out.json", "inside")
        self.assertTrue(os.path.isfile(os.path.join(moved, "out.json")))

    def test_tmpdir_inside_the_lane_is_refused_before_any_write_there(self):
        inner = os.path.join(self.lane, "tmp")
        os.mkdir(inner)
        before = os.stat(inner).st_mtime_ns
        env = dict(os.environ, TMPDIR=inner)
        env.pop("PYTHONPATH", None)
        proc = subprocess.run([sys.executable, "-B", TOOL, *self.args(test="true")], cwd=self.lane, env=env,
                              capture_output=True, text=True, timeout=240)
        self.assertRefused(proc.returncode, proc.stderr, "scratch", "inside the lane")
        self.assertEqual(os.listdir(inner), [])
        self.assertEqual(os.stat(inner).st_mtime_ns, before)  # not even a file made and unlinked

    def test_lane_is_the_current_directory_not_the_name_getcwd_gives(self):
        decoy = os.path.join(self.tmp, "decoy")
        os.mkdir(decoy)
        old = os.getcwd()
        os.chdir(self.lane)
        self.addCleanup(os.chdir, old)
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err), \
                mock.patch.object(tempfile, "tempdir", self.tooltmp), \
                mock.patch.object(gm.os, "getcwd", return_value=decoy):
            code = gm.main(self.args(test="true"))
        self.assertEqual(code, 1, err.getvalue())
        self.assertEqual({key(r) for r in self.rows()}, ALL_KEYS)


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


class CopyWrites(Base):
    """Each create in a lane copy happens in the directory this run made, at its recorded path outside the lane."""

    def lane_writes(self):
        real = os.write
        inside = []

        def write(fd, data):
            where = real_getpath(fd)
            if where.startswith(self.lane + "/"):
                inside.append((where, len(data)))
            return real(fd, data)
        return mock.patch.object(gm.os, "write", write), inside

    def new_in_lane(self, before):
        return sorted(set(tree_digest(self.lane)) - set(before))

    def test_copy_moved_into_the_lane_at_a_file_create_writes_no_byte_inside(self):
        """Pre-review round 3 probe_copy_inside: the copy is renamed into the lane inside note.txt's O_CREAT open."""
        before = tree_digest(self.lane)
        moved = os.path.join(self.lane, "arrived-copy")
        real = os.open
        box = {}

        def opened(name, flags, *a, **kw):
            if name == "note.txt" and flags & os.O_CREAT and not box:
                box["copy"] = os.path.dirname(real_getpath(kw["dir_fd"]))
                os.rename(box["copy"], moved)
            return real(name, flags, *a, **kw)
        watch, inside = self.lane_writes()
        with mock.patch.object(gm.os, "open", opened), watch:
            code, out, err = self.run_main(self.args(test="true"))
        note = os.path.join(moved, "data", "note.txt")
        self.assertRefused(code, err, note, "inside the lane", "kept")
        self.assertEqual(inside, [])
        self.assertEqual(os.path.getsize(note), 0)  # the empty file the create made is kept
        self.assertEqual(self.new_in_lane(before), ["arrived-copy", "arrived-copy/data", "arrived-copy/data/link",
                                                    "arrived-copy/data/note.txt"])
        self.assertFalse(os.path.exists(self.out))

    def test_copy_directory_moved_into_the_lane_before_a_create_gets_nothing_more(self):
        before = tree_digest(self.lane)
        moved = os.path.join(self.lane, "arrived-data")
        real_open, real_symlink = os.open, os.symlink
        box = {}

        def symlink(src, dst, *a, dir_fd=None, **kw):
            result = real_symlink(src, dst, *a, dir_fd=dir_fd, **kw)
            if dst == "link" and "data" not in box:
                box["data"] = real_getpath(dir_fd)  # the copy's data directory
            return result

        def opened(name, flags, *a, **kw):
            if name == "note.txt" and "data" in box and "moved" not in box:  # the source read before its copy
                box["moved"] = True
                os.rename(box["data"], moved)
            return real_open(name, flags, *a, **kw)
        watch, inside = self.lane_writes()
        with mock.patch.object(gm.os, "open", opened), mock.patch.object(gm.os, "symlink", symlink), watch:
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(box.get("moved"))
        self.assertRefused(code, err, moved, "inside the lane", "kept")
        self.assertEqual(inside, [])
        self.assertEqual(self.new_in_lane(before), ["arrived-data", "arrived-data/link"])
        self.assertFalse(os.path.exists(self.out))

    def test_last_entry_created_after_its_directory_moved_into_the_lane_is_kept_and_named(self):
        """The create's own place is checked: no later create in that directory would see the move."""
        for name, fn in (("zz-empty", "mkdir"), ("zz-link", "symlink"), ("zz-file", "open")):
            with self.subTest(name=name):
                self.setUp()
                if fn == "mkdir":
                    os.mkdir(os.path.join(self.lane, "pkg", name))
                elif fn == "symlink":
                    os.symlink("guarded.py", os.path.join(self.lane, "pkg", name))
                else:
                    with open(os.path.join(self.lane, "pkg", name), "w") as fh:
                        fh.write("last\n")
                before = tree_digest(self.lane)
                moved = os.path.join(self.lane, "arrived-pkg")
                log = os.path.join(self.tmp, "runs.log")
                real = getattr(os, fn)
                box = []

                def hooked(*a, dir_fd=None, real=real, fn=fn, name=name, box=box, moved=moved, **kw):
                    made = a[1] if fn == "symlink" else a[0]
                    creates = fn != "open" or a[1] & os.O_CREAT
                    if made == name and dir_fd is not None and creates and not box:
                        box.append(real_getpath(dir_fd))
                        os.rename(box[0], moved)
                    return real(*a, dir_fd=dir_fd, **kw)
                watch, inside = self.lane_writes()
                with mock.patch.object(gm.os, fn, hooked), watch:
                    code, out, err = self.run_main(self.args(test=f"echo run >> {log}"))
                self.assertEqual(len(box), 1)
                self.assertRefused(code, err, os.path.join(moved, name), "inside the lane", "kept")
                self.assertTrue(os.path.lexists(os.path.join(moved, name)))
                self.assertEqual(inside, [])
                self.assertFalse(os.path.exists(log))  # the test never ran
                self.assertFalse(os.path.exists(self.out))

    def test_copy_file_moved_into_the_lane_during_its_write_is_refused_before_the_test_runs(self):
        """The last file of the walk: only the check after its last byte sees the move."""
        moved = os.path.join(self.lane, "arrived-pkg")
        log = os.path.join(self.tmp, "runs.log")
        real = os.write
        box = []

        def write(fd, data):
            where = real_getpath(fd)
            if where.endswith("/pkg/test_guarded.py") and not where.startswith(self.lane + "/") and not box:
                box.append(where)
                os.rename(os.path.dirname(where), moved)
            return real(fd, data)
        with mock.patch.object(gm.os, "write", write):
            code, out, err = self.run_main(self.args(test=f"echo run >> {log}"))
        self.assertEqual(len(box), 1)
        self.assertRefused(code, err, os.path.join(moved, "test_guarded.py"), "inside the lane", "kept")
        self.assertTrue(os.path.isfile(os.path.join(moved, "test_guarded.py")))
        self.assertFalse(os.path.exists(log))
        self.assertFalse(os.path.exists(self.out))

    def test_failed_create_in_a_directory_moved_into_the_lane_keeps_everything(self):
        for fn in ("mkdir", "write"):
            with self.subTest(fn=fn):
                self.setUp()
                moved = os.path.join(self.lane, "arrived-data")
                real = getattr(os, fn)
                box = []

                def mkdir(path, *a, dir_fd=None, **kw):
                    if path == "sub" and dir_fd is not None and not box:
                        box.append(real_getpath(dir_fd))
                        os.rename(box[0], moved)
                        raise OSError(errno.EIO, "Input/output error")
                    return real(path, *a, dir_fd=dir_fd, **kw)

                def write(fd, data):
                    where = real_getpath(fd)
                    if where.endswith("/data/note.txt") and not where.startswith(self.lane + "/") and not box:
                        box.append(os.path.dirname(where))
                        os.rename(box[0], moved)
                        raise OSError(errno.EIO, "Input/output error")
                    return real(fd, data)
                with mock.patch.object(gm.os, fn, mkdir if fn == "mkdir" else write):
                    code, out, err = self.run_main(self.args(test="true"))
                self.assertEqual(len(box), 1)
                self.assertRefused(code, err, moved, "inside the lane", "kept")
                self.assertTrue(os.path.isdir(os.path.dirname(box[0])))  # the rest of the copy is kept
                self.assertFalse(os.path.exists(self.out))

    def test_a_directory_already_at_the_copy_name_is_refused_and_kept(self):
        real = os.mkdir
        box = []

        def mkdir(path, *a, dir_fd=None, **kw):
            result = real(path, *a, dir_fd=dir_fd, **kw)
            if path == "tmp" and dir_fd is not None and not box:
                real("lane", 0o700, dir_fd=dir_fd)
                box.append(os.path.join(real_getpath(dir_fd), "lane"))
            return result
        with mock.patch.object(gm.os, "mkdir", mkdir):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(len(box), 1)
        self.assertRefused(code, err, box[0], "exists", "kept")
        self.assertEqual(os.listdir(box[0]), [])  # not replaced
        self.assertFalse(os.path.exists(self.out))

    def test_copy_name_gone_at_the_check_keeps_the_copy(self):
        """An error (ENOENT) in the check around the test run keeps everything, like a mismatch."""
        real = os.rename
        box = []

        def rename(src, dst, *a, **kw):
            result = real(src, dst, *a, **kw)
            if dst == "lane" and kw.get("dst_dir_fd") is not None and not box:
                mpath = real_getpath(kw["dst_dir_fd"])
                box.append(mpath)
                real(os.path.join(mpath, "lane"), os.path.join(self.tmp, "away"))
            return result
        with mock.patch.object(gm.os, "rename", rename):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(len(box), 1)
        self.assertRefused(code, err, os.path.join(box[0], "lane"), "ENOENT")
        self.assertEqual(sorted(os.listdir(box[0])), ["tmp"])  # the copy directory is kept
        self.assertFalse(os.path.exists(self.out))


class CleanupBound(Base):
    """Removal works only on directories still at the path recorded when this run made them."""

    def test_scratch_moved_into_the_lane_before_cleanup_is_kept(self):
        moved = os.path.join(self.lane, "moved-tmp")
        real_exit = gm.Session.__exit__
        box = {}

        def exit_(session, *exc):
            box["name"] = session.name
            os.rename(self.tooltmp, moved)
            return real_exit(session, *exc)
        with mock.patch.object(gm.Session, "__exit__", exit_):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertRefused(code, err, "kept")
        self.assertTrue(os.path.isdir(os.path.join(moved, box["name"])))
        self.assertFalse(os.path.exists(self.out))

    def test_copy_directory_moved_into_the_lane_during_its_removal_keeps_its_files(self):
        moved = os.path.join(self.lane, "moved-sub")
        real = os.scandir
        box = []

        def scandir(fd=None):
            if isinstance(fd, int) and not box:
                where = real_getpath(fd)
                if where.endswith("/data/sub") and not where.startswith(self.lane + "/"):
                    box.append(where)
                    os.rename(where, moved)
            return real(fd)
        with mock.patch.object(gm.os, "scandir", scandir):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(len(box), 1)
        self.assertRefused(code, err, "kept")
        self.assertEqual(os.listdir(moved), ["deep.txt"])
        self.assertFalse(os.path.exists(self.out))


class Links(Base):
    """Each link is resolved against the walk's record, one component at a time, before any copy or test run."""

    def chain(self):
        os.symlink(".", os.path.join(self.lane, "anchor"))  # the lane itself
        os.symlink("anchor/..", os.path.join(self.lane, "escape"))  # normpath says ".": really the lane's parent

    def test_link_through_another_link_is_refused_before_any_copy(self):
        """Pre-review round 3 probe_link_chain."""
        self.chain()
        log = os.path.join(self.tmp, "runs.log")
        proc = self.run_tool(self.args(test=f"echo run >> {log}; cd escape && pwd -P >> {log}"))
        self.assertRefused(proc.returncode, proc.stderr, os.path.join(self.lane, "escape"), "link")
        self.assertFalse(os.path.exists(log))
        self.assertFalse(os.path.exists(self.out))
        self.assertNoScratchLeft()

    def test_link_chain_that_shares_state_across_copies_gives_no_killed_row(self):
        """Pre-review round 3 probe_link_falsekill: a weak suite must never pass the gate through shared state."""
        self.set_suite(WEAK)
        self.chain()
        os.symlink("escape/..", os.path.join(self.lane, "shared"))
        proc = self.run_tool(self.args(test=self.cmd() + " && test ! -e shared/stamp && touch shared/stamp"))
        self.assertRefused(proc.returncode, proc.stderr, "escape", "link")
        self.assertFalse(os.path.exists(self.out))

    def test_link_changed_after_the_first_walk_is_never_created_in_a_copy(self):
        link = os.path.join(self.lane, "data", "link")
        flag = os.path.join(self.tmp, "done")
        real = os.symlink
        made = []

        def symlink(src, dst, *a, **kw):
            made.append(src)
            return real(src, dst, *a, **kw)
        with mock.patch.object(gm.os, "symlink", symlink):
            code, out, err = self.run_main(self.args(test=f"if [ ! -e {flag} ]; then touch {flag}; "
                                                          f"ln -sfn ../.. {link}; fi; true"))
        self.assertRefused(code, err, "changed", "data/link")
        self.assertEqual(made, ["note.txt"])  # the baseline copy's link only, never the unchecked one
        self.assertFalse(os.path.exists(self.out))

    def test_link_resolution_cases(self):
        record = {"d": ("dir",), "d/s": ("dir",), "d/f": ("file",), "d/l": ("link", "f"), "top": ("link", ".")}
        ok = [("d/x", "f"), ("d/x", "s/../f"), ("d/x", "../d/s"), ("d/x", "./s/"), ("x", "."), ("x", "d")]
        bad = [("d/x", "/etc"), ("d/x", "../.."), ("d/x", "l"), ("d/x", "../top/d"), ("d/x", "f/x"),
               ("d/x", "missing"), ("x", ".git"), ("d/x", "S/../../..")]
        for rel, text in ok:
            self.assertIsNone(gm._link_leaves(rel, text, record), (rel, text))
        for rel, text in bad:
            self.assertIsNotNone(gm._link_leaves(rel, text, record), (rel, text))


def markers(root: str) -> list[str]:
    return sorted(os.path.join(d, f) for d, _, files in os.walk(root) for f in files if f == "irreplaceable")


class Ownership(Base):
    """Ruling 12: a directory is taken as made only empty and bound to its name; removal is per recorded entry."""

    def victim(self, name):
        path = os.path.join(self.tmp, name)
        os.mkdir(path)
        with open(os.path.join(path, "irreplaceable"), "w") as fh:
            fh.write("keep")
        return path

    def test_directory_substituted_at_its_creation_is_refused_and_kept(self):
        """Pre-review round 4 adopt_falsekill: a pre-existing directory takes a new copy directory's name."""
        victims = [self.victim(f"victim-{i}") for i in range(2, 13)]
        real = os.open
        adopted = []

        def opened(name, flags, *a, **kw):
            parent = real_getpath(kw["dir_fd"]) if kw.get("dir_fd") is not None else ""
            if name == "data" and parent.endswith("/copy"):
                run = int(parent.split("/")[-2][1:])
                if run >= 2:
                    path = os.path.join(parent, "data")
                    os.rename(path, os.path.join(self.tmp, f"park-created-{run}"))
                    os.rename(victims[run - 2], path)
                    adopted.append(path)
            return real(name, flags, *a, **kw)
        with mock.patch.object(gm.os, "open", opened):
            code, out, err = self.run_main(self.args(test="test ! -e data/irreplaceable"))
        self.assertEqual(len(adopted), 1)  # the first substitution refuses: no later run
        self.assertRefused(code, err, adopted[0], "kept")
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(len(markers(self.tmp)), 11)
        self.assertTrue(os.path.isfile(os.path.join(adopted[0], "irreplaceable")))

    def test_empty_directory_substituted_after_the_open_is_refused_and_both_are_kept(self):
        """The opened directory must be the one the name gives (lstat), not only empty."""
        real = os.open
        box = {}

        def opened(name, flags, *a, **kw):
            fd = real(name, flags, *a, **kw)
            parent = real_getpath(kw["dir_fd"]) if kw.get("dir_fd") is not None else ""
            if name == "data" and parent.endswith("/copy") and not box:
                box["path"] = path = os.path.join(parent, "data")
                box["parked"] = os.path.join(self.tmp, "parked-data")
                os.rename(path, box["parked"])
                os.mkdir(path)
            return fd
        with mock.patch.object(gm.os, "open", opened):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertRefused(code, err, box["path"], "kept")
        self.assertTrue(os.path.isdir(box["parked"]))
        self.assertEqual(os.listdir(box["path"]), [])
        self.assertFalse(os.path.exists(self.out))

    def test_entry_the_run_did_not_make_found_at_removal_is_refused_and_kept(self):
        for kind in ("file", "link", "hardlink"):
            with self.subTest(kind=kind):
                self.setUp()
                foreign = os.path.join(self.tmp, "foreign.txt")
                with open(foreign, "w") as fh:
                    fh.write("keep")
                real_remove = gm._remove_dir
                box = {}

                def remove(parent_fd, name, path, owned, kind=kind, foreign=foreign, box=box):
                    if name == "m0001" and not box:
                        box["at"] = at = os.path.join(path, "lane", "data", "foreign.txt")
                        if kind == "file":
                            os.rename(foreign, at)
                        elif kind == "link":
                            os.symlink(foreign, at)
                        else:
                            os.link(foreign, at)
                    return real_remove(parent_fd, name, path, owned)
                with mock.patch.object(gm, "_remove_dir", remove):
                    code, out, err = self.run_main(self.args(test="true"))
                self.assertRefused(code, err, box["at"], "kept")
                self.assertTrue(os.path.lexists(box["at"]))
                self.assertFalse(os.path.exists(self.out))

    def test_entry_older_than_the_test_run_put_in_the_copy_by_the_test_is_kept(self):
        """What the test makes during its run is removed; an older entry it moves in is not the run's."""
        for kind in ("directory", "file"):
            with self.subTest(kind=kind):
                self.setUp()
                victim = self.victim("victim")
                if kind == "file":
                    victim = os.path.join(victim, "irreplaceable")
                code, out, err = self.run_main(self.args(test=f"mv {victim} data/irreplaceable-moved"))
                self.assertRefused(code, err, "data/irreplaceable-moved", "kept")
                if kind == "file":
                    self.assertIn("before the test run", err)
                    found = [os.path.join(d, f) for d, _, fs in os.walk(self.tmp) for f in fs
                             if f == "irreplaceable-moved"]
                    self.assertEqual(len(found), 1)
                else:
                    self.assertEqual(len(markers(self.tmp)), 1)
                self.assertFalse(os.path.exists(self.out))

    def test_files_and_links_the_test_makes_are_removed_with_the_copy(self):
        cmd = 'echo x > "$TMPDIR/f" && ln -s f "$TMPDIR/l" && echo y > data/new.txt && ln data/new.txt data/hard'
        code, out, err = self.run_main(self.args(test=cmd))
        self.assertEqual(code, 1, err)
        self.assertNoScratchLeft()

    def test_directory_the_test_makes_is_kept(self):
        code, out, err = self.run_main(self.args(test='mkdir "$TMPDIR/d"'))
        self.assertRefused(code, err, "tmp/d", "kept")
        self.assertFalse(os.path.exists(self.out))


class TargetsInTheWalk(Base):
    """Sweep finding: a target gone from the lane between its parse and the first walk is never mutated."""

    def test_target_directory_rebound_after_the_parse_is_refused(self):
        real = gm.read_targets
        box = {}

        def read_targets(root_fd, root, files):
            targets = real(root_fd, root, files)
            pkg = os.path.join(self.lane, "pkg")
            box["fault"] = fault = fk.Fault()
            fault.parked = fk._park(pkg)
            os.mkdir(pkg)
            return targets
        with mock.patch.object(gm, "read_targets", read_targets):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertRefused(code, err, "pkg/guarded.py", "as it was parsed")
        self.assertFalse(os.path.exists(self.out))


class SweepFindings(Base):
    """Ruling 16 sweep: a move right after a check must still be seen before the run reports or removes."""

    def test_source_directory_moved_out_before_its_last_read_of_the_final_scan_is_refused(self):
        sub, outside = os.path.join(self.lane, "data", "sub"), os.path.join(self.tmp, "outside-sub")
        real_verify, real_read = gm.Session.verify_lane, os.read
        box = {}

        def verify(session):
            box["final"] = True
            return real_verify(session)

        def read(fd, n):
            where = real_getpath(fd)
            if box.get("final") and where == os.path.join(sub, "deep.txt"):
                box["reads"] = box.get("reads", 0) + 1
                if box["reads"] == 2:  # the read that finds the end, after its check
                    os.rename(sub, outside)
                    os.mkdir(sub)
            return real_read(fd, n)
        with mock.patch.object(gm.Session, "verify_lane", verify), mock.patch.object(gm.os, "read", read):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertEqual(box.get("reads"), 2)
        self.assertRefused(code, err, outside, "outside the lane")
        self.assertFalse(os.path.exists(self.out))

    def test_copy_directory_replaced_after_its_identity_check_is_not_removed(self):
        moved = os.path.join(self.lane, "moved-m0001")
        real_stat = os.stat
        box = {"n": 0}

        def stat_(name, *a, dir_fd=None, **kw):
            result = real_stat(name, *a, dir_fd=dir_fd, **kw)
            if name == "m0001" and dir_fd is not None:
                box["n"] += 1
                if box["n"] == 4:  # at its creation, before and after the run, then the removal's check
                    box["path"] = path = os.path.join(real_getpath(dir_fd), name)
                    os.rename(path, moved)
                    os.mkdir(path)
            return result
        with mock.patch.object(gm.os, "stat", stat_):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertIn("path", box)
        self.assertRefused(code, err, "kept")
        self.assertTrue(os.path.isdir(box["path"]))  # the replacement is not removed
        self.assertFalse(os.path.exists(self.out))

    def test_scratch_replaced_at_its_rmdir_is_refused(self):
        """The replacement is removed at the instant (no rmdir is bound to an fd); the run must not report."""
        real_exit, real_rmdir = gm.Session.__exit__, os.rmdir
        parked = os.path.join(self.tmp, "parked-scratch")
        box = {}

        def exit_(session, *exc):
            box["name"], box["path"] = session.name, session.scratch
            return real_exit(session, *exc)

        def rmdir(name, *a, dir_fd=None, **kw):
            if name == box.get("name") and "fired" not in box:
                box["fired"] = True
                os.rename(box["path"], parked)
                os.mkdir(box["path"])
            return real_rmdir(name, *a, dir_fd=dir_fd, **kw)
        with mock.patch.object(gm.Session, "__exit__", exit_), mock.patch.object(gm.os, "rmdir", rmdir):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(box.get("fired"))
        self.assertRefused(code, err, box["path"], "kept")
        self.assertTrue(os.path.isdir(parked))
        self.assertFalse(os.path.exists(self.out))


class WriteChecks(Base):
    """Ruling 13: each os.write is preceded by the live-path check of its fd."""

    def moved_after_first_byte(self, ends, dest):
        real_write = os.write
        inside, box = [], {}

        def write(fd, data):
            where = real_getpath(fd)
            n = real_write(fd, memoryview(data).cast("B")[:1])
            if where.startswith(self.lane + "/"):
                inside.append(where)
            if where.endswith(ends) and not where.startswith(self.lane + "/") and not box:
                box["file"] = os.path.join(dest, os.path.basename(where))
                os.rename(os.path.dirname(where), dest)
            return n
        with mock.patch.object(gm.os, "write", write):
            code, out, err = self.run_main(self.args(test="true"))
        return code, err, box["file"], inside

    def test_copy_directory_moved_into_the_lane_after_a_short_write_gets_no_more_bytes(self):
        """Pre-review round 4 boundary_probes short-write-move."""
        code, err, moved, inside = self.moved_after_first_byte("/pkg/test_guarded.py", os.path.join(self.lane, "moved-pkg"))
        self.assertRefused(code, err, moved, "inside the lane", "kept")
        self.assertEqual(inside, [])
        self.assertEqual(os.path.getsize(moved), 1)  # only the byte written before the move

    def test_output_parent_moved_into_the_lane_after_a_short_write_gets_no_more_bytes(self):
        code, err, moved, inside = self.moved_after_first_byte("/outdir/out.json", os.path.join(self.lane, "moved-out"))
        self.assertRefused(code, err, moved, "inside the lane")
        self.assertEqual(inside, [])
        self.assertEqual(os.path.getsize(moved), 1)


class SourceChecks(Base):
    """Ruling 14: each scandir, child open and read through a held source fd is preceded by its containment check."""

    def test_source_directory_moved_out_of_the_lane_is_never_read(self):
        """Pre-review round 4 source_escape."""
        data, outside = os.path.join(self.lane, "data"), os.path.join(self.tmp, "outside-data")
        real_scandir, real_read, real_open = os.scandir, os.read, os.open
        moved, reads = [], []

        def scandir(fd=None):
            if isinstance(fd, int) and real_getpath(fd) == data and not moved:
                os.rename(data, outside)
                os.mkdir(data)
                moved.append(outside)
            return real_scandir(fd)

        def read(fd, n):
            if real_getpath(fd).startswith(outside + "/"):
                reads.append(real_getpath(fd))
            return real_read(fd, n)

        def opened(name, flags, *a, dir_fd=None, **kw):
            if dir_fd is not None and real_getpath(dir_fd).startswith(outside):
                reads.append(os.path.join(real_getpath(dir_fd), name))
            return real_open(name, flags, *a, dir_fd=dir_fd, **kw)
        with mock.patch.object(gm.os, "scandir", scandir), mock.patch.object(gm.os, "read", read), \
                mock.patch.object(gm.os, "open", opened):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(moved)
        self.assertRefused(code, err, outside, "outside the lane")
        self.assertEqual(reads, [])
        self.assertFalse(os.path.exists(self.out))

    def test_source_file_moved_out_of_the_lane_between_reads_is_not_read_again(self):
        note, outside = os.path.join(self.lane, "data", "note.txt"), os.path.join(self.tmp, "outside-note.txt")
        real_read = os.read
        moved, reads = [], []

        def read(fd, n):
            where = real_getpath(fd)
            if where == outside:
                reads.append(where)
            data = real_read(fd, n)
            if where == note and not moved:
                os.rename(note, outside)
                moved.append(fd)
            return data
        with mock.patch.object(gm.os, "read", read):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(moved)
        self.assertRefused(code, err, outside, "outside the lane")
        self.assertEqual(reads, [])


class OutputOrder(Base):
    """Ruling 19: the output fd's live path is the last query before each write (astra-r5 output_order_tests)."""

    def probe(self, trigger, move_parent, short):
        real_fcntl, real_write = gm.fcntl.fcntl, os.write
        moved = os.path.join(self.lane, "moved-output")
        fired, inside, output_writes = [], [], []

        def fcntl_(fd, command, *args):
            ready = bool(output_writes) if short else os.path.exists(self.out)
            if command == gm.fcntl.F_GETPATH and not fired and ready:
                if real_getpath(fd) == (self.lane if trigger == "root" else self.outdir):
                    os.rename(self.outdir if move_parent else self.out, moved)
                    fired.append(True)
            return real_fcntl(fd, command, *args)

        def write(fd, data):
            path = real_getpath(fd)
            n = real_write(fd, memoryview(data)[:1] if short else data)
            if path == self.out:
                output_writes.append(n)
            if path.startswith(self.lane + "/"):
                inside.append(n)
            return n
        with mock.patch.object(gm.fcntl, "fcntl", fcntl_), mock.patch.object(gm.os, "write", write):
            code, out, err = self.run_main(self.args(test="true"))
        self.assertTrue(fired, "fault did not fire")
        self.assertEqual(code, 2, err)
        self.assertEqual(inside, [], f"tool wrote {sum(inside)} bytes inside lane")

    def test_parent_moves_at_root_check_before_first_byte(self):
        self.probe("root", True, False)

    def test_file_moves_at_parent_check_before_first_byte(self):
        self.probe("parent", False, False)

    def test_parent_moves_at_root_check_after_short_write(self):
        self.probe("root", True, True)


if __name__ == "__main__":
    unittest.main()
