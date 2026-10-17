"""Step 323: class-drop (mutant_ops/char_class.py) drops one item from a regex character class.

The operator is compared only through its own module (char_class.OPERATORS). The end-to-end tests run the
tool as a subprocess in fixture lanes made in temp directories, removed by addCleanup; no git is used (the
tool runs without --base), and of a default-operator run only the class-drop rows are read.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings

import guard_mutants as gm
from mutant_ops import RE_FUNCS, char_class

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_mutants.py")
M45 = r"""UNSAFE = re.compile(r'[\x00-\x1f\x7f"]')"""  # path_map_rows.py:32 at 379f6dc5


def made(source, lines=gm.WHOLE) -> list:
    data = source.encode("utf-8") if isinstance(source, str) else source
    return gm.mutants_for("m.py", data, lines, char_class.OPERATORS)


def pattern_at(source: bytes, line: int, col: int):
    """The value of the str or bytes constant that starts at (line, col) of source."""
    hits = [n.value for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Constant)
            and isinstance(n.value, (str, bytes)) and (n.lineno, n.col_offset) == (line, col)]
    assert len(hits) == 1, (line, col, hits)
    return hits[0]


def drops(pattern: str, call: str = "re.compile") -> dict:
    """{tag: mutated pattern} of the class-drop mutants of `R = <call>(<pattern as a literal>)`."""
    out = {}
    for m in made(f"import re\nR = {call}({pattern!r})\n"):
        rel, line, col, op, tag = m.id.split(":")
        assert (rel, op, m.operator, int(line), m.line) == ("m.py", "class-drop", "class-drop", 2, 2), m.id
        assert tag not in out, m.id
        out[int(tag)] = pattern_at(m.source, int(line), int(col))
    return out


def expect(pattern: str, *items: str) -> dict:
    """{start: pattern without that item} for items that appear in order inside pattern's one class."""
    out, at = {}, 0
    for item in items:
        at = pattern.index(item, at)
        out[at] = pattern[:at] + pattern[at + len(item):]
        at += len(item)
    return out


class Items(unittest.TestCase):
    def test_m45_shape_drops_each_of_the_three_items(self):
        got = drops(r'[\x00-\x1f\x7f"]')
        self.assertEqual(got, {1: r'[\x7f"]', 10: r'[\x00-\x1f"]', 14: r'[\x00-\x1f\x7f]'})
        ms = made("import re\n" + M45 + "\n")
        self.assertEqual([m.id for m in ms], ["m.py:2:20:class-drop:1", "m.py:2:20:class-drop:10",
                                              "m.py:2:20:class-drop:14"])
        self.assertEqual([m.change for m in ms], [r"drop \x00-\x1f at 1", r"drop \x7f at 10", 'drop " at 14'])
        self.assertEqual(ms[1].source, b"import re\nUNSAFE = re.compile('[\\\\x00-\\\\x1f\"]')\n")

    def test_each_kind_of_item(self):
        p = r"[\d\x7f\u00e9\U0001F600\N{EM DASH}\101\0_a-z\x41-\x5a\-]"
        self.assertEqual(drops(p), expect(p, r"\d", r"\x7f", r"\u00e9", r"\U0001F600", r"\N{EM DASH}", r"\101",
                                          r"\0", "_", "a-z", r"\x41-\x5a", r"\-"))
        p = r"[\1234\x4142]"  # an octal escape stops after 3 digits, \x after 2 hex digits
        self.assertEqual(drops(p), expect(p, r"\123", "4", r"\x41", "4", "2"))
        p = r"[\u00e9\U0001F600\N{EM DASH}\N]"  # \N without { is two characters (and does not compile)
        self.assertEqual(drops(p), {len(p) - 3: p[:-3] + "]"})

    def test_negated_class_never_drops_its_caret(self):
        self.assertEqual(drops("[^ab]"), {2: "[^b]", 3: "[^a]"})
        self.assertEqual(drops("[^^a]"), {2: "[^a]", 3: "[^^]"})
        self.assertEqual(drops("[^a]"), {})
        self.assertEqual(drops("[^a-z]"), {})

    def test_a_class_with_one_item_gets_no_mutant(self):
        for p in ["[a]", "[a-z]", r"[\x00-\x1f]", r"[\]]", "[]]", r"[\d]", r"x[\N{EM DASH}]+"]:
            self.assertEqual(drops(p), {}, p)

    def test_escaped_brackets(self):
        self.assertEqual(drops(r"\[ab\]"), {})
        self.assertEqual(drops(r"\[ab]"), {})  # \[ opens no class, so ] is a literal
        self.assertEqual(drops(r"[\]a]"), {1: "[a]", 3: r"[\]]"})
        self.assertEqual(drops(r"\\[ab]"), {3: r"\\[b]", 4: r"\\[a]"})
        self.assertEqual(drops(r"[\[a]"), {1: "[a]", 3: r"[\[]"})

    def test_close_bracket_right_after_the_open_is_an_item(self):
        self.assertEqual(drops("[]a]"), {1: "[a]", 2: "[]]"})
        self.assertEqual(drops("[^]a]"), {2: "[^a]", 3: "[^]]"})

    def test_a_dash_first_or_last_is_a_literal_item(self):
        self.assertEqual(drops("[-a]"), {1: "[a]", 2: "[-]"})
        self.assertEqual(drops("[a-]"), {1: "[-]", 2: "[a]"})
        self.assertEqual(drops("[a-c-]"), {1: "[-]", 4: "[a-c]"})
        self.assertEqual(drops("[a-c-e]"), {1: "[-e]", 4: "[a-ce]", 5: "[a-c-]"})

    def test_every_class_of_the_pattern(self):
        self.assertEqual(drops("[ab]x[cd]+"), {1: "[b]x[cd]+", 2: "[a]x[cd]+", 6: "[ab]x[d]+", 7: "[ab]x[c]+"})

    def test_a_drop_that_does_not_compile_gets_no_mutant(self):
        with self.assertRaises(re.error):
            re.compile("[^]")
        self.assertEqual(drops("[a^]"), {2: "[a]"})  # without a: "[^]" does not compile
        self.assertEqual(drops("[ab]a{99999999999}"), {})  # re.compile raises OverflowError here

    def test_a_warning_from_re_is_no_compile_failure(self):
        re.purge()  # re warns only when it parses a pattern, not for one it has cached
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertEqual(drops("[[q]"), {1: "[q]", 2: "[[]"})  # "[[]": FutureWarning, possible nested set

    def test_the_warning_filters_are_the_same_after_the_operator_runs(self):
        re.purge()  # so the compile check of "[[]" warns again
        with warnings.catch_warnings():  # a leaked filter ends with this test, not in the next one
            warnings.simplefilter("default")  # front filter is not "ignore", even if an earlier test leaked one
            before = list(warnings.filters)
            self.assertEqual(drops("[[q]"), {1: "[q]", 2: "[[]"})
            self.assertEqual(warnings.filters, before)

    def test_a_drop_that_would_change_more_than_the_item_gets_no_mutant(self):
        re.compile("[^b]")  # compiles, but negates the class: not [a^b] without a
        self.assertEqual(drops("[a^b]"), {2: "[ab]", 3: "[a^]"})

    def test_every_mutant_pattern_compiles(self):
        for p in [r'[\x00-\x1f\x7f"]', "[]a]", "[^]+]", r"[\]+]", "[a-c-e]", r"[\d\x7f\0_]", "[a^b]", "[ab]x[cd]"]:
            for tag, value in drops(p).items():
                re.compile(value)

    def test_a_class_that_does_not_end_gets_no_mutant_and_nothing_raises(self):
        for p in ["[", "[^", "[]", "[^]", "[ab", "[a-", "a\\", "[a\\", r"[a\x4", r"[\N{EM", r"[\N{EMa]", r"[ab][cd"]:
            self.assertEqual(drops(p), {}, p)
        self.assertEqual(char_class._classes("[ab]x[cd", True), [(0, False, [(1, 2), (2, 3)])])
        self.assertEqual(char_class._classes(r"[a\N{EM]", True), [])

    def test_calls_and_arguments_are_regex_zeros(self):
        src = (b"import re\n"
               b"re.findall(pattern=r'[ab]', string=s)\n"
               b"re.sub(r'[ab]', '', s, pattern=r'[cd]')\n"
               b"regex.compile(r'[ab]')\n"
               b"re.escape(r'[ab]')\n"
               b"x.re.compile(r'[ab]')\n"
               b"compile(r'[ab]')\n"
               b"re.compile(p + '[ab]')\n"
               b"re.compile(f'[ab]{x}')\n"
               b"re.compile(3)\n"
               b"re.compile()\n"
               b"re.compile(flags=0)\n"
               b"re.split(b'[ab]', data)\n")
        got = {(m.line, pattern_at(m.source, m.line, int(m.id.split(":")[2]))) for m in made(src)}
        self.assertEqual(got, {(2, "[b]"), (2, "[a]"), (3, "[b]"), (3, "[a]"), (13, b"[b]"), (13, b"[a]")})
        for fn in sorted(RE_FUNCS):
            self.assertEqual(len(made(f"import re\nre.{fn}(r'[ab]', s)\n")), 2, fn)

    def test_a_bytes_pattern_stays_bytes(self):
        ms = made(b"import re\nB = re.compile(b'[a\\xff]')\n")
        self.assertEqual([pattern_at(m.source, 2, 15) for m in ms], [b"[\xff]", b"[a]"])
        ms = made(b"import re\nB = re.compile(rb'[\\u0041\\xff]')\n")  # in bytes \u is no escape
        self.assertEqual([pattern_at(m.source, 2, 15) for m in ms], [b"[0041\\xff]"])
        ms = made(b"import re\nB = re.compile(rb'[\\N{DASH}]')\n")  # nor is \N{...}: items \N { D A S H }
        self.assertEqual([pattern_at(m.source, 2, 15) for m in ms], [b"[{DASH}]"])

    def test_utf8_and_crlf_splice_the_bytes_of_the_pattern(self):
        data = 'import re\r\nS = "é€"; R = re.compile(r"[ab]")\r\nT = 1\r\n'.encode("utf-8")
        ms = made(data)
        self.assertEqual([m.id for m in ms], ["m.py:2:28:class-drop:1", "m.py:2:28:class-drop:2"])
        self.assertEqual([m.source for m in ms], [data.replace(b'r"[ab]"', b"'[b]'"),
                                                   data.replace(b'r"[ab]"', b"'[a]'")])

    def test_only_anchor_lines_in_scope(self):
        src = "import re\nA = re.compile(r'[ab]')\nB = re.compile(\n    r'[cd]')\n"
        self.assertEqual([m.line for m in made(src, {2})], [2, 2])
        self.assertEqual([m.line for m in made(src, {3})], [])
        self.assertEqual([m.line for m in made(src, {4})], [4, 4])

    def test_t318_regex_corpus_shapes(self):
        src = br"""
import re
re.search(r"\++[+]+[^]+]+[]a]+[\]+]+")
re.sub(b"q+\\w{2}\xff+", b"", data)
re.split(r"[")
re.subn(r"[^")
re.compile("a\\")
re.compile("a\\+[^a-z]+[^\\]]+")
re.compile(r"[]")
"""
        ms = gm.parsed(made(src))
        self.assertEqual(sorted(int(m.id.split(":")[4]) for m in ms), [9, 10, 14, 15, 19, 21])
        for m in ms:
            re.compile(pattern_at(m.source, m.line, int(m.id.split(":")[2])))


class EndToEnd(unittest.TestCase):
    """M45: the tool reports the drop of \\x7f survived when the test never uses \\x7f, and killed when it does."""

    MODULE = "import re\n\n" + M45 + "\n\n\ndef safe(text):\n    return UNSAFE.search(text) is None\n"
    WEAK = ['self.assertTrue(rows.safe("ok"))', 'self.assertFalse(rows.safe("a\\x00"))',
            'self.assertFalse(rows.safe("\\x1f"))', "self.assertFalse(rows.safe('a\"'))"]

    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="gm-charclass-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.lane = os.path.join(self.tmp, "lane")
        self.tooltmp = os.path.join(self.tmp, "tooltmp")
        os.makedirs(os.path.join(self.lane, "pkg"))
        os.mkdir(self.tooltmp)
        with open(os.path.join(self.lane, "pkg", "rows.py"), "w", encoding="utf-8") as fh:
            fh.write(self.MODULE)

    def run_tool(self, asserts: list[str], name: str):
        body = "".join(f"        {a}\n" for a in asserts)
        with open(os.path.join(self.lane, "pkg", "test_rows.py"), "w", encoding="utf-8") as fh:
            fh.write(f"import unittest\n\nimport rows\n\n\nclass T(unittest.TestCase):\n    def test_safe(self):\n{body}")
        out = os.path.join(self.tmp, name)
        env = dict(os.environ, TMPDIR=self.tooltmp)
        env.pop("PYTHONPATH", None)
        cmd = f"{sys.executable} -B -m unittest discover -s pkg -p test_rows.py"
        proc = subprocess.run([sys.executable, "-B", TOOL, "--file", "pkg/rows.py", "--test", cmd, "--out", out],
                              cwd=self.lane, env=env, capture_output=True, text=True, timeout=600)
        self.assertIn(proc.returncode, (0, 1), proc.stdout + proc.stderr)
        self.assertEqual(os.listdir(self.tooltmp), [])
        with open(out, encoding="utf-8") as fh:
            rows = [r for r in json.load(fh) if r["operator"] == "class-drop"]
        return proc, {r["id"]: r for r in rows}

    def test_m45_drop_of_x7f_survives_a_test_that_never_uses_it(self):
        proc, rows = self.run_tool(self.WEAK, "weak.json")
        ids = ["pkg/rows.py:3:20:class-drop:1", "pkg/rows.py:3:20:class-drop:10", "pkg/rows.py:3:20:class-drop:14"]
        self.assertEqual(sorted(rows), ids)
        self.assertEqual({i: r["result"] for i, r in rows.items()},
                         {ids[0]: "killed", ids[1]: "survived", ids[2]: "killed"})
        self.assertEqual(rows[ids[1]]["change"], r"drop \x7f at 10")
        self.assertEqual(proc.returncode, 1)  # the survivor alone forces exit 1
        self.assertIn(f"survived {ids[1]}: drop \\x7f at 10 [", proc.stdout)

    def test_m45_drop_of_x7f_is_killed_by_a_test_that_uses_it(self):
        proc, rows = self.run_tool(self.WEAK + ['self.assertFalse(rows.safe("\\x7f"))'], "strong.json")
        self.assertEqual(len(rows), 3)
        self.assertEqual({r["result"] for r in rows.values()}, {"killed"})
        self.assertNotIn("class-drop", proc.stdout)


if __name__ == "__main__":
    unittest.main()
