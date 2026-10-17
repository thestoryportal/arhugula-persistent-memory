"""Step 321: the tuple-drop operator (mutant_ops/tuple_drop.py) drops one component of a compared tuple.

The suite makes no git call and compares the operator only through its own module (tuple_drop.OPERATORS),
except the end-to-end M72 run, which runs the tool as a script with its default operators and reads only the
tuple-drop rows. Every temp dir is made by the tests and removed by addCleanup; nothing is written under code/.
"""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

import guard_mutants as gm
from mutant_ops import tuple_drop

import test_guard_mutants_ops as t318

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "guard_mutants.py")
OP = "tuple-drop"


def made(rel: str, data: bytes, lines=gm.WHOLE) -> list:
    """The tuple-drop mutants of data, each checked to parse (a mutant that does not parse refuses)."""
    return gm.parsed(gm.mutants_for(rel, data, lines, tuple_drop.OPERATORS))


class Mutants(unittest.TestCase):
    def assert_drops(self, data: bytes, old: bytes, news: list[bytes], line: int, col: int) -> None:
        """One mutant per index i: old (the whole Compare) becomes news[i]; ids rel:line:col:tuple-drop:i."""
        self.assertEqual(data.count(old), 1, old)
        got = {m.id: m for m in made("f.py", data)}
        self.assertEqual(sorted(got), sorted(f"f.py:{line}:{col}:{OP}:{i}" for i in range(len(news))))
        for i, new in enumerate(news):
            m = got[f"f.py:{line}:{col}:{OP}:{i}"]
            self.assertEqual(m.source, data.replace(old, new), i)
            self.assertEqual((m.rel, m.line, m.operator), ("f.py", line, OP))
            self.assertIn(str(i), m.change)

    def test_m72_shape_pair_drops_each_index_to_a_plain_expression(self):
        data = (b"def walk(opened, est):\n"
                b"    if (opened.st_dev, opened.st_ino) != (est.st_dev, est.st_ino):\n"
                b"        raise OSError\n")
        self.assert_drops(data, b"(opened.st_dev, opened.st_ino) != (est.st_dev, est.st_ino)",
                          [b"opened.st_ino != est.st_ino", b"opened.st_dev != est.st_dev"], 2, 7)

    def test_three_elements_leave_a_tuple_of_two(self):
        data = b"ok = (a, b + 1, c) == (d, e, f(g))\n"
        self.assert_drops(data, b"(a, b + 1, c) == (d, e, f(g))",
                          [b"(b + 1, c) == (e, f(g))", b"(a, c) == (d, f(g))", b"(a, b + 1) == (d, e)"], 1, 5)

    def test_single_left_element_is_parenthesized_when_not_simple(self):
        data = b"ok = (x + 1, not y) == (z, w or v)\n"
        self.assert_drops(data, b"(x + 1, not y) == (z, w or v)",
                          [b"(not y) == (w or v)", b"(x + 1) == z"], 1, 5)

    def test_operator_text_is_kept_and_spaced(self):
        data = b"k = (x,y)is not(o,e)\nm = (x, y)  not in  (o, e)\nn = (x,y)!=(o,e)\n"
        self.assert_drops(b"k = (x,y)is not(o,e)\n", b"(x,y)is not(o,e)", [b"y is not e", b"x is not o"], 1, 4)
        self.assert_drops(b"m = (x, y)  not in  (o, e)\n", b"(x, y)  not in  (o, e)",
                          [b"y  not in  e", b"x  not in  o"], 1, 4)
        self.assert_drops(b"n = (x,y)!=(o,e)\n", b"(x,y)!=(o,e)", [b"y != e", b"x != o"], 1, 4)
        self.assertEqual(len(made("f.py", data)), 6)

    def test_multiline_single_element_is_parenthesized(self):
        data = b"ok = ((a\n       .b), c) == (d, e)\n"
        self.assert_drops(data, b"((a\n       .b), c) == (d, e)", [b"c == e", b"(a\n       .b) == d"], 1, 5)

    def test_utf8_crlf_offsets_are_bytes(self):
        data = 's = "é"\r\nif ("é", s) == (s, "é"): raise ValueError\r\n'.encode("utf-8")
        self.assert_drops(data, '("é", s) == (s, "é")'.encode("utf-8"),
                          [b's == "\xc3\xa9"', b'"\xc3\xa9" == s'], 2, 3)

    def test_nested_compares_each_get_mutants(self):
        data = b"ok = ((a, b) == (c, d), e) != (f, g)\n"
        ids = sorted(m.id for m in made("f.py", data))
        self.assertEqual(ids, [f"f.py:1:5:{OP}:0", f"f.py:1:5:{OP}:1", f"f.py:1:6:{OP}:0", f"f.py:1:6:{OP}:1"])

    def test_no_mutant_without_two_tuple_displays_of_one_length(self):
        for text in (b"ok = t == (a, b)\n", b"ok = (a, b) == t\n", b"ok = (a, b) == [c, d]\n",
                     b"ok = [a, b] == (c, d)\n", b"ok = [a, b] == [c, d]\n", b"ok = (a, b) == (c, d, e)\n",
                     b"ok = (a, b, c) != (d, e)\n",
                     b"ok = (a,) == (b,)\n", b"ok = () == ()\n", b"ok = (a, b) < (c, d) < (e, f)\n",
                     b"ok = (*a, b) == (c, d)\n", b"ok = (a, b) == (c, *d)\n", b"ok = a == b\n",
                     b"ok = (a, b) + (c, d)\n", b"ok = f((a, b), (c, d))\n"):
            self.assertEqual(made("f.py", text), [], text)

    def test_line_scope_filters_on_the_compare_line(self):
        data = b"x = 1\nok = (a, b) == (c, d)\n"
        self.assertEqual(made("f.py", data, {1}), [])
        self.assertEqual(len(made("f.py", data, {2})), 2)

    def test_t318_corpus_does_not_raise_and_every_mutant_parses(self):
        for rel, data in t318.CORPUS:
            made(rel, data)


class M72EndToEnd(unittest.TestCase):
    """M72 (record_split.py:282 at 9e036fbf) on a fixture lane of the same shape, through the tool as a script."""

    MODULE = (b"class Moved(Exception):\n"
              b"    pass\n"
              b"\n"
              b"\n"
              b"def check(opened, est):\n"
              b"    if (opened.st_dev, opened.st_ino) != (est.st_dev, est.st_ino):\n"
              b"        raise Moved(\"the entry changed during the walk\")\n"
              b"    return True\n")
    INO_TEST = ("import types\n"
                "import m\n"
                "def st(dev, ino):\n"
                "    return types.SimpleNamespace(st_dev=dev, st_ino=ino)\n"
                "if m.check(st(1, 2), st(1, 2)) is not True:\n"
                "    raise SystemExit('the same entry did not pass')\n"
                "try:\n"
                "    m.check(st(1, 2), st(1, 3))\n"
                "except m.Moved:\n"
                "    pass\n"
                "else:\n"
                "    raise SystemExit('an entry with another st_ino passed')\n")
    DEV_TEST = INO_TEST + ("try:\n"
                           "    m.check(st(1, 2), st(4, 2))\n"
                           "except m.Moved:\n"
                           "    pass\n"
                           "else:\n"
                           "    raise SystemExit('an entry on another device passed')\n")
    ID0, ID1 = f"m.py:6:7:{OP}:0", f"m.py:6:7:{OP}:1"

    def mkdtemp(self) -> str:
        path = os.path.realpath(tempfile.mkdtemp(prefix="gm-tuple-"))
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

    def run_tool(self, test_body: str) -> tuple[subprocess.CompletedProcess, dict]:
        lane, outdir, tooltmp = self.mkdtemp(), self.mkdtemp(), self.mkdtemp()
        with open(os.path.join(lane, "m.py"), "wb") as fh:
            fh.write(self.MODULE)
        with open(os.path.join(lane, "t.py"), "w", encoding="utf-8") as fh:
            fh.write(test_body)
        out = os.path.join(outdir, "out.json")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
        env["TMPDIR"] = tooltmp
        test = f"{shlex.quote(sys.executable)} -B t.py"
        proc = subprocess.run([sys.executable, "-B", TOOL, "--file", "m.py", "--test", test, "--out", out],
                              cwd=lane, env=env, capture_output=True, text=True, timeout=600)
        self.assertTrue(os.path.exists(out), proc.stdout + proc.stderr)
        with open(out, encoding="utf-8") as fh:
            rows = json.load(fh)
        with open(os.path.join(lane, "m.py"), "rb") as fh:
            self.assertEqual(fh.read(), self.MODULE)
        self.assertEqual(os.listdir(tooltmp), [], "the tool left its scratch directory")
        mine = {r["id"]: r for r in rows if r["operator"] == OP}
        self.assertEqual(sorted(mine), [self.ID0, self.ID1])
        for r in mine.values():
            self.assertEqual(r["location"], "m.py:6")
        return proc, mine

    def test_st_ino_only_test_reports_index_0_survived(self):
        proc, mine = self.run_tool(self.INO_TEST)
        self.assertEqual(mine[self.ID0]["result"], "survived", proc.stdout + proc.stderr)
        self.assertEqual(mine[self.ID1]["result"], "killed", proc.stdout + proc.stderr)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(f"\nsurvived {self.ID0}: ", "\n" + proc.stdout)
        self.assertNotIn(f"{self.ID1}:", proc.stdout)

    def test_a_test_that_changes_st_dev_kills_both(self):
        proc, mine = self.run_tool(self.DEV_TEST)
        self.assertEqual({r["result"] for r in mine.values()}, {"killed"}, proc.stdout + proc.stderr)
        self.assertNotIn(f":{OP}:", proc.stdout)


if __name__ == "__main__":
    unittest.main()
