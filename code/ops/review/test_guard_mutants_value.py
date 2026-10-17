"""Step 320: mutant_ops.value_replace makes value-empty and codec-lenient mutants.

The operators are compared only through their own module (value_replace.OPERATORS); no test runs git or
reads the default operator set. The wave-1 cases M20 and M42 run end to end: guard_mutants.main on a fixture
lane in a temp dir, with an operator directory that holds a copy of value_replace.py only. Every temp dir is
made by the test and removed by addCleanup; nothing is written under code/.
"""
from __future__ import annotations

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
import test_guard_mutants_ops as t318
from mutant_ops import value_replace

OPS = {"value-empty", "codec-lenient"}


def made(data: str | bytes, rel: str = "m.py") -> dict[str, tuple[str, bytes]]:
    """id -> (change, mutated source) of every value_replace mutant of data; each source must parse."""
    raw = data if isinstance(data, bytes) else textwrap.dedent(data).encode("utf-8")
    mutants = gm.parsed(gm.mutants_for(rel, raw, gm.WHOLE, value_replace.OPERATORS))
    return {m.id: (m.change, m.source) for m in mutants}


class ValueEmpty(unittest.TestCase):
    def one(self, src: str, mid: str, change: str, new: str) -> None:
        self.assertEqual(made(src), {mid: (change, new.encode("utf-8"))})

    def test_dict_display(self):
        self.one("x = {'a': 1}\n", "m.py:1:4:value-empty", "dict display -> {}", "x = {}\n")

    def test_dict_of_only_a_mapping_unpack(self):
        self.one("x = {**y}\n", "m.py:1:4:value-empty", "dict display -> {}", "x = {}\n")

    def test_list_display(self):
        self.one("x = [1, 2]\n", "m.py:1:4:value-empty", "list display -> []", "x = []\n")

    def test_set_display(self):
        self.one("x = {1}\n", "m.py:1:4:value-empty", "set display -> set()", "x = set()\n")

    def test_tuple_display(self):
        self.one("x = (1, 2)\n", "m.py:1:4:value-empty", "tuple display -> ()", "x = ()\n")

    def test_bare_tuple_with_trailing_comma(self):
        self.one("x = 1,\n", "m.py:1:4:value-empty", "tuple display -> ()", "x = ()\n")

    def test_multi_line_tuple(self):
        self.one("x = (\n    1,\n    2,  # c\n)\n", "m.py:1:4:value-empty", "tuple display -> ()", "x = ()\n")

    def test_dict_comprehension_m20_shape(self):
        src = "graph = {old: new for old, new in sealed.items() if new and new != old}\n"
        self.one(src, "m.py:1:8:value-empty", "dict comprehension -> {}", "graph = {}\n")

    def test_list_comprehension(self):
        self.one("x = [a for a in b]\n", "m.py:1:4:value-empty", "list comprehension -> []", "x = []\n")

    def test_set_comprehension(self):
        self.one("x = {a for a in b}\n", "m.py:1:4:value-empty", "set comprehension -> set()", "x = set()\n")

    def test_ann_assign(self):
        self.one("x: list = [1]\n", "m.py:1:10:value-empty", "list display -> []", "x: list = []\n")

    def test_return_of_a_bare_tuple(self):
        self.one("def f(a, b):\n    return a, b\n", "m.py:2:11:value-empty", "tuple display -> ()",
                 "def f(a, b):\n    return ()\n")

    def test_return_of_a_dict(self):
        self.one("def f(a):\n    return {a: 1}\n", "m.py:2:11:value-empty", "dict display -> {}",
                 "def f(a):\n    return {}\n")

    def test_multiple_targets_one_mutant(self):
        self.one("a = b = [1]\n", "m.py:1:8:value-empty", "list display -> []", "a = b = []\n")

    def test_only_the_outer_value(self):
        self.one("x = [[1], {2}]\n", "m.py:1:4:value-empty", "list display -> []", "x = []\n")

    def test_one_per_value_in_order(self):
        got = made("x = [1]\ndef f():\n    y = {1: 2}\n    return (y,)\n")
        self.assertEqual(sorted(got), ["m.py:1:4:value-empty", "m.py:3:8:value-empty", "m.py:4:11:value-empty"])

    def test_utf8_and_crlf(self):
        src = "s = 'é'; x = ['é', s]\r\nif s: y = {'é'}\r\n".encode("utf-8")
        got = made(src)
        self.assertEqual(got, {
            "m.py:1:14:value-empty": ("list display -> []", "s = 'é'; x = []\r\nif s: y = {'é'}\r\n".encode()),
            "m.py:2:10:value-empty": ("set display -> set()", "s = 'é'; x = ['é', s]\r\nif s: y = set()\r\n".encode()),
        })

    def test_no_mutant(self):
        self.assertEqual(made("""\
            a = {}
            b = []
            c = ()
            d = set()
            e = (x for x in y)
            f = 3
            g = list(y)
            h: int
            h += [1]
            [1, 2]
            k(x=[1])
            for i in [1, 2]:
                pass
            def f():
                return
            def g():
                return 1
            def h():
                yield [1]
            """), {})


class CodecLenient(unittest.TestCase):
    def one(self, src: str, mid: str, change: str, new: str) -> None:
        self.assertEqual(made(src), {mid: (change, new.encode("utf-8"))})

    def test_decode_m42_shape(self):
        self.one("text = data.decode('utf-8')\n", "m.py:1:7:codec-lenient", 'decode(): add errors="replace"',
                 "text = data.decode('utf-8', errors=\"replace\")\n")

    def test_encode_without_argument(self):
        self.one("b = s.encode()\n", "m.py:1:4:codec-lenient", 'encode(): add errors="replace"',
                 "b = s.encode(errors=\"replace\")\n")

    def test_encoding_keyword(self):
        self.one("f(x.decode(encoding='ascii'))\n", "m.py:1:2:codec-lenient", 'decode(): add errors="replace"',
                 "f(x.decode(encoding='ascii', errors=\"replace\"))\n")

    def test_trailing_comma(self):
        self.one("x.decode('utf-8',)\n", "m.py:1:0:codec-lenient", 'decode(): add errors="replace"',
                 "x.decode('utf-8', errors=\"replace\")\n")

    def test_comment_and_newline_before_the_paren(self):
        self.one("y = x.decode(\n    'utf-8'  # c\n)\n", "m.py:1:4:codec-lenient", 'decode(): add errors="replace"',
                 "y = x.decode('utf-8', errors=\"replace\")\n")

    def test_generator_argument(self):
        self.one("y = x.encode(c for c in z)\n", "m.py:1:4:codec-lenient", 'encode(): add errors="replace"',
                 "y = x.encode((c for c in z), errors=\"replace\")\n")

    def test_chained_calls_one_per_call(self):
        got = made("y = s.encode().decode()\n")
        self.assertEqual(got, {
            "m.py:1:4:codec-lenient": ('decode(): add errors="replace"', b'y = s.encode().decode(errors="replace")\n'),
            "m.py:1:4:codec-lenient#2": ('encode(): add errors="replace"', b'y = s.encode(errors="replace").decode()\n'),
        })

    def test_utf8_and_crlf(self):
        src = "s = 'é'; b = s.encode('utf-8')\r\n".encode("utf-8")
        self.assertEqual(made(src), {"m.py:1:14:codec-lenient": (  # byte column: 'é' is 2 bytes
            'encode(): add errors="replace"', "s = 'é'; b = s.encode('utf-8', errors=\"replace\")\r\n".encode())})

    def test_no_mutant(self):
        self.assertEqual(made("""\
            a = x.decode('utf-8', errors='strict')
            b = x.decode('utf-8', 'strict')
            c = x.encode(errors='ignore')
            d = x.decode(**kw)
            e = x.decode(*args)
            f = decode(x)
            g = x.decoder('utf-8')
            h = x.decode
            i = f"{x.decode()}"
            j = f'{x.encode("ascii")} {y}'
            """), {})

    def test_beside_an_f_string(self):
        self.one('s = f"{a}" + x.decode()\n', "m.py:1:13:codec-lenient", 'decode(): add errors="replace"',
                 's = f"{a}" + x.decode(errors="replace")\n')


class Robust(unittest.TestCase):
    def test_t318_corpus_parses_and_never_raises(self):
        for rel, data in t318.CORPUS:
            with self.subTest(rel=rel):
                made(data, rel)  # gm.parsed refuses a mutant that does not parse

    def test_own_source_parses(self):  # it has a .decode() inside an f-string
        with open(value_replace.__file__, "rb") as fh:
            made(fh.read(), "value_replace.py")

    def test_module_contract(self):
        self.assertEqual(value_replace.OPERATORS, (value_replace.value_empty, value_replace.codec_lenient))
        self.assertFalse(hasattr(value_replace, "gm"))
        self.assertNotIn("guard_mutants", value_replace.__dict__)


# ---- the wave-1 cases end to end: guard_mutants.main on a fixture lane -------------------------

M20 = """\
def graph_of(sealed, rows):
    graph = {old: new for old, new in sealed.items() if new and new != old}
    graph.update(rows)
    return graph
"""
M20_WEAK = "import mod\nassert mod.graph_of({}, {'a': 'b'}) == {'a': 'b'}\n"
M20_STRONG = M20_WEAK + "assert mod.graph_of({'x': 'y', 'z': 'z'}, {}) == {'x': 'y'}\n"

M42 = """\
def text_of(data):
    text = data.decode('utf-8')
    return text
"""
M42_WEAK = "import mod\nassert mod.text_of(b'abc') == 'abc'\n"
M42_STRONG = M42_WEAK + """\
try:
    mod.text_of(b'\\xff')
except UnicodeDecodeError:
    pass
else:
    raise SystemExit('lenient decode')
"""


class WaveOneCases(unittest.TestCase):
    def mkdtemp(self) -> str:
        path = os.path.realpath(tempfile.mkdtemp(prefix="gm-value-"))
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

    def run_case(self, module: str, check: str) -> tuple[int, list[dict], str]:
        ops_dir = self.mkdtemp()
        shutil.copyfile(value_replace.__file__, os.path.join(ops_dir, "value_replace.py"))
        lane = self.mkdtemp()
        for name, text in (("mod.py", module), ("check.py", check)):
            with open(os.path.join(lane, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        out = os.path.join(self.mkdtemp(), "out.json")
        test = f"{shlex.quote(sys.executable)} -B check.py"
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(lane)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            rc = gm.main(["--file", "mod.py", "--test", test, "--out", out], ops_dir=ops_dir)
        with open(out, encoding="utf-8") as fh:
            rows = [r for r in json.load(fh) if r["operator"] in OPS]
        with open(os.path.join(lane, "mod.py"), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), module)
        return rc, rows, stdout.getvalue()

    def check(self, module: str, weak: str, strong: str, mid: str, op: str, change: str) -> None:
        rc, rows, printed = self.run_case(module, weak)
        self.assertEqual([(r["id"], r["operator"], r["change"], r["result"]) for r in rows],
                         [(mid, op, change, "survived")])
        self.assertEqual(rc, 1)
        self.assertIn(f"survived {mid}: {change}", printed)
        rc, rows, printed = self.run_case(module, strong)
        self.assertEqual([(r["id"], r["result"]) for r in rows], [(mid, "killed")])
        self.assertEqual(rc, 0)
        self.assertNotIn("survived", printed.split("guard_mutants:")[0])

    def test_m20_sealed_graph_emptied(self):
        self.check(M20, M20_WEAK, M20_STRONG, "mod.py:2:12:value-empty", "value-empty", "dict comprehension -> {}")

    def test_m42_decode_made_lenient(self):
        self.check(M42, M42_WEAK, M42_STRONG, "mod.py:2:11:codec-lenient", "codec-lenient",
                   'decode(): add errors="replace"')


if __name__ == "__main__":
    unittest.main()
