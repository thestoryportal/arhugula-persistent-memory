"""Step 322: the call-unwrap and with-null operators of mutant_ops/wrapper_removal.py.

The operators are compared only through their own module (wrapper_removal.OPERATORS on fixtures). The end-to-end
tests run guard_mutants.main on fixture lanes of the wave-1 shapes M40 (path_map_rows.py:87 at 379f6dc5) and M85
(record_split.py:280 at 9e036fbf): a test that does not check the case lets the mutant survive, one that does
kills it. No git is called; every temp directory is removed by addCleanup.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import shlex
import shutil
import sys
import tempfile
import textwrap
import unittest

import guard_mutants as gm
from mutant_ops import base, wrapper_removal

OPS = wrapper_removal.OPERATORS
OURS = ("call-unwrap", "with-null")


def made(text: str | bytes, lines=gm.WHOLE, rel: str = "m.py") -> dict[str, tuple[str, bytes]]:
    """id -> (change, source) of every mutant of wrapper_removal on the fixture; every source parses."""
    data = text if isinstance(text, bytes) else textwrap.dedent(text).encode("utf-8")
    mutants = gm.parsed(gm.mutants_for(rel, data, lines, OPS))
    return {m.id: (m.change, m.source) for m in mutants}


def line_of(source: bytes, n: int) -> bytes:
    return source.splitlines()[n - 1]


HEAD = """\
def make_row(old, new, unit, root):
    return (old, new, unit, root)


async def fetch(x):
    return x


def one(x):
    return x


"""


FIXTURE_M40 = (HEAD + "def f(pairs, unit, root):\n    for old, new in pairs:\n"
                      "        row = make_row(old, new, unit, root)\n").encode("utf-8")


class CallUnwrap(unittest.TestCase):
    def test_m40_shape_becomes_the_tuple_of_arguments(self):
        got = made(FIXTURE_M40)
        self.assertEqual(list(got), ["m.py:15:14:call-unwrap"])
        change, source = got["m.py:15:14:call-unwrap"]
        self.assertEqual(change, "make_row(...) -> a tuple of its arguments")
        self.assertEqual(line_of(source, 15), b"        row = (old, new, unit, root)")
        self.assertEqual(source, FIXTURE_M40.replace(b"row = make_row(old, new, unit, root)",
                                                               b"row = (old, new, unit, root)"))

    def test_one_argument_is_written_alone_or_in_parentheses(self):
        cases = {
            "x = one(a)": b"x = a",
            "x = one(a.b)": b"x = a.b",
            "x = one(a[0])": b"x = a[0]",
            "x = one(g(a))": b"x = g(a)",
            "x = one('s')": b"x = 's'",
            "x = one(a + 1)": b"x = (a + 1)",
            "x = one(y := 1)": b"x = (y := 1)",
            "x = one(lambda: 1)": b"x = (lambda: 1)",
            "x = one(a for a in b)": b"x = ((a for a in b))",
            "x = one(make_row, one)": b"x = (make_row, one)",
            "x = one(a, b + 1, y := 2)": b"x = (a, (b + 1), (y := 2))",
        }
        for stmt, want in cases.items():
            with self.subTest(stmt=stmt):
                got = made(HEAD + stmt + "\n")
                self.assertEqual(list(got), ["m.py:13:4:call-unwrap"])
                self.assertEqual(line_of(got["m.py:13:4:call-unwrap"][1], 13), want)
                self.assertEqual(got["m.py:13:4:call-unwrap"][0].split(" -> ")[0], "one(...)")

    def test_a_simple_argument_on_several_lines_is_parenthesized(self):
        got = made(HEAD + "x = one(a\n        .b)\ny = one('a'\n        'b')\n")
        self.assertEqual(sorted(got), ["m.py:13:4:call-unwrap", "m.py:15:4:call-unwrap"])
        self.assertIn(b"x = (a\n        .b)\n", got["m.py:13:4:call-unwrap"][1])
        self.assertIn(b"y = ('a'\n        'b')\n", got["m.py:15:4:call-unwrap"][1])

    def test_annassign_return_and_async_def(self):
        got = made(HEAD + "v: int = one(a)\n\n\ndef g(a):\n    return one(a)\n\n\nw = fetch(a)\nu: int\n")
        self.assertEqual(sorted(got), ["m.py:13:9:call-unwrap", "m.py:17:11:call-unwrap", "m.py:20:4:call-unwrap"])
        self.assertEqual(line_of(got["m.py:13:9:call-unwrap"][1], 13), b"v: int = a")
        self.assertEqual(line_of(got["m.py:17:11:call-unwrap"][1], 17), b"    return a")
        self.assertEqual(line_of(got["m.py:20:4:call-unwrap"][1], 20), b"w = a")
        self.assertEqual(got["m.py:13:9:call-unwrap"][0], "one(...) -> its argument")

    def test_not_made(self):
        cases = [
            "x = one(a, k=1)", "x = one(**kw)", "x = one(*a)", "x = one(a, *b)", "x = one()",
            "x = int(a)", "x = os.path.join(a, b)", "x = one(a) + 1", "one(a)", "x += one(a)",
            "x = C(a)", "x = lam(a)", "x = guarded(a)", "x = tried(a)", "x = inner(a)", "x = method(a)",
            "x = [one(a)]", "x = await_me(a)()", "x = one",
        ]
        head = HEAD + textwrap.dedent("""\
            import os
            lam = lambda a: a


            class C:
                def method(self, a):
                    return a


            if True:
                def guarded(a):
                    return a
            try:
                def tried(a):
                    return a
            except Exception:
                pass


            def await_me(a):
                return one


            def outer(a):
                def inner(b):
                    return b
                return inner


            """)
        for stmt in cases:
            with self.subTest(stmt=stmt):
                self.assertEqual(made(head + stmt + "\n"), {})

    def test_anchor_is_the_call_and_follows_the_line_scope(self):
        text = HEAD + "x = (\n    one(a))\n"
        self.assertEqual(list(made(text)), ["m.py:14:4:call-unwrap"])
        self.assertEqual(list(made(text, {14})), ["m.py:14:4:call-unwrap"])
        self.assertEqual(made(text, {13}), {})

    def test_utf8_and_crlf_byte_offsets(self):
        data = (HEAD + "é = one(ü, 'ß')\n").replace("\n", "\r\n").encode("utf-8")
        got = made(data)
        self.assertEqual(list(got), ["m.py:13:5:call-unwrap"])
        self.assertEqual(got["m.py:13:5:call-unwrap"][1], data.replace("one(ü, 'ß')".encode(), "(ü, 'ß')".encode()))


class WithNull(unittest.TestCase):
    def test_m85_shape_becomes_a_nullcontext(self):
        got = made("""\
            def inode(path, fd):
                with _fs(path):
                    opened = os.fstat(fd)
                return opened
            """)
        self.assertEqual(list(got), ["m.py:2:9:with-null"])
        change, source = got["m.py:2:9:with-null"]
        self.assertEqual(change, "with _fs(...) -> nullcontext()")
        self.assertEqual(line_of(source, 2), b'    with __import__("contextlib").nullcontext():')
        self.assertEqual(source.count(b"_fs("), 0)

    def test_one_mutant_per_item_keeping_the_as_target(self):
        got = made("with open(p) as fh, lock(), ctx, contextlib.ExitStack() as (a, b):\n    pass\n")
        self.assertEqual(set(got), {"m.py:1:5:with-null", "m.py:1:20:with-null", "m.py:1:33:with-null"})
        null = '__import__("contextlib").nullcontext()'
        self.assertEqual(line_of(got["m.py:1:5:with-null"][1], 1).decode(),
                         f"with {null} as fh, lock(), ctx, contextlib.ExitStack() as (a, b):")
        self.assertEqual(line_of(got["m.py:1:20:with-null"][1], 1).decode(),
                         f"with open(p) as fh, {null}, ctx, contextlib.ExitStack() as (a, b):")
        self.assertEqual(line_of(got["m.py:1:33:with-null"][1], 1).decode(),
                         f"with open(p) as fh, lock(), ctx, {null} as (a, b):")
        self.assertEqual(got["m.py:1:33:with-null"][0], "with contextlib.ExitStack(...) -> nullcontext()")

    def test_parenthesized_items_on_several_lines(self):
        text = "with (\n    a() as x,\n    b(\n      1),\n):\n    pass\n"
        got = made(text)
        self.assertEqual(sorted(got), ["m.py:2:4:with-null", "m.py:3:4:with-null"])
        self.assertIn(b'    __import__("contextlib").nullcontext() as x,\n', got["m.py:2:4:with-null"][1])
        self.assertIn(b'\n    __import__("contextlib").nullcontext(),\n):', got["m.py:3:4:with-null"][1])
        self.assertEqual(list(made(text, {3})), ["m.py:3:4:with-null"])

    def test_the_change_is_one_line(self):  # the survivor report prints one line per mutant
        got = made("with (contextlib\n        .ExitStack)() as s:\n    pass\n")
        self.assertEqual(list(got), ["m.py:1:5:with-null"])
        self.assertEqual(got["m.py:1:5:with-null"][0], "with contextlib .ExitStack(...) -> nullcontext()")
        self.assertEqual(got["m.py:1:5:with-null"][1], b'with __import__("contextlib").nullcontext() as s:\n    pass\n')

    def test_not_made(self):
        for text in ("with ctx:\n    pass\n", "with a.b as c:\n    pass\n",
                     "async def f():\n    async with lock():\n        pass\n"):
            with self.subTest(text=text):
                self.assertEqual(made(text), {})


class NewIdsOnly(unittest.TestCase):
    FIXTURE = (HEAD + textwrap.dedent("""\
        import os


        def g(path, fd):
            if fd < 0:
                raise ValueError(path)
            with one(path) as p:
                try:
                    v = one(os.O_RDONLY | os.O_NOFOLLOW)
                except OSError:
                    return one(v)
            return make_row(p, v, 1, 2)
        """)).encode("utf-8")

    def test_base_mutants_keep_their_ids_changes_and_sources(self):
        def key(ops):
            return {(m.id, m.change, m.source) for m in gm.mutants_for("m.py", self.FIXTURE, gm.WHOLE, ops)}
        alone, both, ours = key(base.OPERATORS), key(base.OPERATORS + OPS), key(OPS)
        self.assertTrue(alone)
        self.assertEqual(both, alone | ours)
        self.assertEqual({i.rsplit(":", 1)[1] for i, _, _ in ours}, set(OURS))
        self.assertEqual(len(ours), 4)

    def test_t318_corpus_gives_no_error_and_only_parsing_mutants(self):
        from test_guard_mutants_ops import CORPUS  # T318's fixtures: nested defs, a class, a lambda, UTF-8 + CRLF
        for rel, data in CORPUS:
            with self.subTest(rel=rel):
                gm.parsed(gm.mutants_for(rel, data, gm.WHOLE, OPS))


# ---- end to end: guard_mutants.main on fixture lanes of the wave-1 shapes ------------------------

M40_MODULE = '''\
def kind(new: str) -> str:
    return "abs" if new.startswith("/") else "rel"


def make_row(old: str, new: str, unit: str, root: str) -> tuple:
    return (old, new, kind(new), unit)


def parse_unit_rows(pairs: list, unit: str, root: str) -> list:
    rows = []
    for old, new in pairs:
        row = make_row(old, new, unit, root)
        rows.append(row)
    return rows
'''
M40_ID = "path_map_rows.py:12:14:call-unwrap"
M40_WEAK = '''\
import unittest
import path_map_rows


class T(unittest.TestCase):
    def test_rows(self):
        rows = path_map_rows.parse_unit_rows([("a", "b")], "u", "r")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][:2], ("a", "b"))
'''
M40_STRONG = M40_WEAK.replace('rows[0][:2], ("a", "b")', 'rows[0], ("a", "b", "rel", "u")')

M85_MODULE = '''\
import contextlib
import os


class Refusal(Exception):
    pass


@contextlib.contextmanager
def _fs(path):
    try:
        yield
    except OSError as exc:
        raise Refusal(f"{path}: {exc.strerror}") from exc


def inode(path, fd):
    with _fs(path):
        opened = os.fstat(fd)
    return opened.st_ino
'''
M85_ID = "record_split.py:18:9:with-null"
M85_WEAK = '''\
import os
import unittest
import record_split


class T(unittest.TestCase):
    def test_inode(self):
        fd = os.open("record_split.py", os.O_RDONLY)
        self.addCleanup(os.close, fd)
        self.assertEqual(record_split.inode("p", fd), os.stat("record_split.py").st_ino)
'''
M85_STRONG = M85_WEAK + '''
    def test_oserror_is_a_refusal(self):
        fd = os.open("record_split.py", os.O_RDONLY)
        os.close(fd)
        with self.assertRaises(record_split.Refusal):
            record_split.inode("p", fd)
'''


class EndToEnd(unittest.TestCase):
    def mkdtemp(self) -> str:
        path = os.path.realpath(tempfile.mkdtemp(prefix="gm-wrap-"))
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

    def run_tool(self, rel: str, module: str, test: str) -> tuple[int, list[dict], str]:
        lane = self.mkdtemp()
        for name, body in ((rel, module), ("test_case.py", test)):
            with open(os.path.join(lane, name), "w", encoding="utf-8") as fh:
                fh.write(body)
        out = os.path.join(self.mkdtemp(), "out.json")
        cmd = f"{shlex.quote(sys.executable)} -B -m unittest -q test_case"
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(lane)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = gm.main(["--file", rel, "--test", cmd, "--out", out])
        self.assertIn(rc, (0, 1), stderr.getvalue())
        with open(out, encoding="utf-8") as fh:
            rows = [r for r in json.load(fh) if r["operator"] in OURS]
        with open(os.path.join(lane, rel), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), module)  # the lane is never mutated in place
        return rc, rows, stdout.getvalue()

    def check(self, rel, module, weak, strong, mid, op, change):
        rc, rows, printed = self.run_tool(rel, module, weak)
        self.assertEqual([(r["id"], r["operator"], r["change"], r["result"]) for r in rows],
                         [(mid, op, change, "survived")])
        self.assertEqual(rc, 1)
        self.assertIn(f"survived {mid}: {change} [", printed)
        rc, rows, printed = self.run_tool(rel, module, strong)
        self.assertEqual([(r["id"], r["result"]) for r in rows], [(mid, "killed")])
        self.assertNotIn(mid, printed)

    def test_m40_make_row_unwrapped(self):
        self.check("path_map_rows.py", M40_MODULE, M40_WEAK, M40_STRONG, M40_ID, "call-unwrap",
                   "make_row(...) -> a tuple of its arguments")

    def test_m85_with_fs_nullcontext(self):
        self.check("record_split.py", M85_MODULE, M85_WEAK, M85_STRONG, M85_ID, "with-null",
                   "with _fs(...) -> nullcontext()")

    def test_fixture_mutants_are_the_wave1_ones(self):
        m40 = gm.mutants_for("path_map_rows.py", M40_MODULE.encode(), gm.WHOLE, OPS)
        self.assertEqual([m.id for m in m40], [M40_ID])
        self.assertIn(b"        row = (old, new, unit, root)\n", m40[0].source)
        m85 = gm.mutants_for("record_split.py", M85_MODULE.encode(), gm.WHOLE, OPS)
        self.assertEqual([m.id for m in m85], [M85_ID])
        self.assertIn(b'    with __import__("contextlib").nullcontext():\n        opened = os.fstat(fd)\n',
                      m85[0].source)
        ast.parse(m40[0].source)
        ast.parse(m85[0].source)


if __name__ == "__main__":
    unittest.main()
