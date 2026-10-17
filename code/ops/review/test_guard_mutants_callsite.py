"""Step 324: callsite-flag-drop drops one flag of a module-level os.O_* constant at one os.open call site.

The suite makes no git call: line scope is passed to mutants_for as a set of lines, which is what --base
gives it. The end-to-end runs use a fixture lane in a temp dir (removed by addCleanup) and the default
operators; they read only the rows of this module's operator and base's flag-drop of the definition.
"""
from __future__ import annotations

import contextlib
import hashlib
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
import mutant_ops
from mutant_ops import base, callsite_flags

OP = "callsite-flag-drop"

# The shape of record_split.py at 9e036fbf: DIR_FLAGS (:63), open_root's call (:251), the entry open (:278).
FIXTURE = textwrap.dedent("""\
    import os

    DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


    def open_root(root):
        return os.open(root, DIR_FLAGS)


    def open_entry(dir_fd, name):
        fd = os.open(name, DIR_FLAGS, dir_fd=dir_fd)
        return fd
    """)
DEF_LINE, SITE1, SITE2 = 3, 7, 11
SITE1_COL, SITE2_COL = 11, 9
FLAGS = ("O_RDONLY", "O_DIRECTORY", "O_NOFOLLOW")

# Run in each lane copy: open_root (site 1) must refuse a regular file; with "both", open_entry (site 2) too.
CHECK = textwrap.dedent("""\
    import os
    import sys

    import mod


    def refuses(open_, *args):
        try:
            fd = open_(*args)
        except NotADirectoryError:
            return
        os.close(fd)
        sys.exit(open_.__name__ + " opened a regular file as a directory")


    refuses(mod.open_root, "mod.py")
    if sys.argv[1:] == ["both"]:
        dir_fd = os.open(".", os.O_RDONLY)
        try:
            refuses(mod.open_entry, dir_fd, "mod.py")
        finally:
            os.close(dir_fd)
    """)


def made(text: str | bytes, lines=gm.WHOLE) -> dict[str, gm.Mutant]:
    data = text.encode("utf-8") if isinstance(text, str) else text
    return {m.id: m for m in gm.parsed(gm.mutants_for("m.py", data, lines, callsite_flags.OPERATORS))}


class Mutants(unittest.TestCase):
    def test_one_mutant_per_flag_at_each_call_site(self):
        got = made(FIXTURE)
        self.assertEqual(set(got), {f"m.py:{line}:{col}:{OP}:{flag}" for line, col in
                                    ((SITE1, SITE1_COL), (SITE2, SITE2_COL)) for flag in FLAGS})
        m = got[f"m.py:{SITE2}:{SITE2_COL}:{OP}:O_DIRECTORY"]
        self.assertEqual((m.rel, m.line, m.operator), ("m.py", SITE2, OP))
        self.assertEqual(m.change, "DIR_FLAGS -> (DIR_FLAGS & ~os.O_DIRECTORY)")
        self.assertEqual(m.source.decode(), FIXTURE.replace(
            "os.open(name, DIR_FLAGS, dir_fd=dir_fd)", "os.open(name, (DIR_FLAGS & ~os.O_DIRECTORY), dir_fd=dir_fd)"))
        m = got[f"m.py:{SITE1}:{SITE1_COL}:{OP}:O_NOFOLLOW"]
        self.assertEqual(m.change, "DIR_FLAGS -> (DIR_FLAGS & ~os.O_NOFOLLOW)")
        self.assertEqual(m.source.decode(), FIXTURE.replace(
            "os.open(root, DIR_FLAGS)", "os.open(root, (DIR_FLAGS & ~os.O_NOFOLLOW))"))

    def test_flags_keyword_when_there_is_no_second_positional_argument(self):
        text = "import os\nF = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, mode=0o600, flags=F)\nos.open(p, F, flags=G)\n"
        got = made(text)
        self.assertEqual(sorted(got), [f"m.py:3:0:{OP}:O_NOFOLLOW", f"m.py:3:0:{OP}:O_RDONLY",
                                       f"m.py:4:0:{OP}:O_NOFOLLOW", f"m.py:4:0:{OP}:O_RDONLY"])
        self.assertEqual(got[f"m.py:3:0:{OP}:O_NOFOLLOW"].source.decode(), text.replace(
            "flags=F)", "flags=(F & ~os.O_NOFOLLOW))"))
        self.assertEqual(got[f"m.py:4:0:{OP}:O_RDONLY"].source.decode(), text.replace(
            "os.open(p, F,", "os.open(p, (F & ~os.O_RDONLY),"))

    def test_byte_offsets_with_utf8_and_crlf(self):
        text = 'import os\r\nF = os.O_RDONLY | os.O_NOFOLLOW\r\ns = "\u00e9\u00e9"; fd = os.open("\u00e9", F)\r\n'
        got = made(text.encode("utf-8"))
        self.assertEqual(set(got), {f"m.py:3:17:{OP}:O_RDONLY", f"m.py:3:17:{OP}:O_NOFOLLOW"})
        self.assertEqual(got[f"m.py:3:17:{OP}:O_RDONLY"].source,
                         text.replace('"\u00e9", F)', '"\u00e9", (F & ~os.O_RDONLY))').encode("utf-8"))

    def test_a_repeated_flag_gives_one_mutant(self):
        got = made("import os\nF = os.O_RDONLY | os.O_NOFOLLOW | os.O_RDONLY\nos.open(p, F)\n")
        self.assertEqual(sorted(got), [f"m.py:3:0:{OP}:O_NOFOLLOW", f"m.py:3:0:{OP}:O_RDONLY"])

    def test_each_name_of_a_chained_assignment(self):
        got = made("import os\nF = G = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\nos.open(p, G)\n")
        self.assertEqual(len(got), 4)
        self.assertEqual({m.line for m in got.values()}, {3, 4})

    def test_the_anchor_is_the_call_line(self):
        text = "import os\nF = os.O_RDONLY | os.O_NOFOLLOW\nfd = os.open(\n    p,\n    F,\n)\n"
        self.assertEqual(sorted(made(text, {3})), [f"m.py:3:5:{OP}:O_NOFOLLOW", f"m.py:3:5:{OP}:O_RDONLY"])
        self.assertEqual(made(text, {2}), {})  # the constant's line alone: no call site in scope
        self.assertEqual(made(text, {5}), {})  # the flags argument's own line is not the anchor
        got = made(FIXTURE, {SITE2})  # a changed call site, the definition line unchanged
        self.assertEqual(sorted(got), sorted(f"m.py:{SITE2}:{SITE2_COL}:{OP}:{f}" for f in FLAGS))

    def test_new_ids_only_base_ids_unchanged(self):
        data = FIXTURE.encode()
        ids = lambda ops: {(m.id, m.change, hashlib.sha256(m.source).hexdigest())  # noqa: E731
                           for m in gm.mutants_for("m.py", data, gm.WHOLE, ops)}
        mine, theirs = ids(callsite_flags.OPERATORS), ids(base.OPERATORS)
        self.assertEqual(ids(base.OPERATORS + callsite_flags.OPERATORS), mine | theirs)
        self.assertFalse({i for i, _, _ in mine} & {i for i, _, _ in theirs})
        self.assertIn(("mutant_ops.callsite_flags", "callsite_flag_drop"),
                      [(fn.__module__, fn.__qualname__) for fn in mutant_ops.load_operators()])


GOOD = "import os\nF = os.O_RDONLY | os.O_NOFOLLOW\n"

# Each body gets no mutant (GOOD alone with a call gets two: NoMutant.test_positive_control).
NO_MUTANT = {
    "assigned twice": GOOD + "F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "augmented": GOOD + "F |= os.O_SYNC\nos.open(p, F)\n",
    "annotated": "import os\nF: int = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "deleted": GOOD + "os.open(p, F)\ndel F\n",
    "import as": GOOD + "import x as F\nos.open(p, F)\n",
    "from import": GOOD + "from x import F\nos.open(p, F)\n",
    "dotted import": GOOD + "import F.sub\nos.open(p, F)\n",
    "def": GOOD + "def F():\n    pass\nos.open(p, F)\n",
    "async def": GOOD + "async def F():\n    pass\nos.open(p, F)\n",
    "class": GOOD + "class F:\n    pass\nos.open(p, F)\n",
    "for target": GOOD + "for F in x:\n    pass\nos.open(p, F)\n",
    "with as": GOOD + "with x as F:\n    pass\nos.open(p, F)\n",
    "except as": GOOD + "try:\n    pass\nexcept E as F:\n    pass\nos.open(p, F)\n",
    "local": GOOD + "def g():\n    F = 0\n    return os.open(p, F)\n",
    "argument": GOOD + "def g(F):\n    return os.open(p, F)\n",
    "lambda argument": GOOD + "g = lambda F: os.open(p, F)\n",
    "global": GOOD + "def g():\n    global F\n    return os.open(p, F)\n",
    "nonlocal": GOOD + "def g():\n    def h():\n        nonlocal F\n    return os.open(p, F)\n",
    "comprehension": GOOD + "[F for F in x]\nos.open(p, F)\n",
    "walrus": GOOD + "(F := 1)\nos.open(p, F)\n",
    "match as": GOOD + "match x:\n    case 1 as F:\n        pass\nos.open(p, F)\n",
    "match star": GOOD + "match x:\n    case [*F]:\n        pass\nos.open(p, F)\n",
    "match rest": GOOD + "match x:\n    case {**F}:\n        pass\nos.open(p, F)\n",
    "one flag": "import os\nF = os.O_RDONLY\nos.open(p, F)\n",
    "getattr flag": "import os\nF = os.O_RDONLY | getattr(os, \"O_NOFOLLOW\", 0)\nos.open(p, F)\n",
    "number": "import os\nF = os.O_RDONLY | 4\nos.open(p, F)\n",
    "other module": "import os\nF = sys.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "not O_": "import os\nF = os.path | os.O_NOFOLLOW\nos.open(p, F)\n",
    "and": "import os\nF = os.O_RDONLY & os.O_NOFOLLOW\nos.open(p, F)\n",
    "in a def": "import os\ndef g():\n    F = os.O_RDONLY | os.O_NOFOLLOW\n    return os.open(p, F)\n",
    "in a class": "import os\nclass K:\n    F = os.O_RDONLY | os.O_NOFOLLOW\n    os.open(p, F)\n",
    "tuple target": "import os\nF, G = os.O_RDONLY | os.O_NOFOLLOW, 0\nos.open(p, F)\n",
    "attribute target": "import os\nx.F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\nos.open(p, x.F)\n",
    "subscript target": "import os\nx[F] = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "argument not a name": GOOD + "os.open(p, F | 0)\nos.open(p, K.F)\n",
    "unknown name": GOOD + "os.open(p, G)\n",
    "builtin open": GOOD + "open(p, F)\n",
    "other open": GOOD + "io.open(p, F)\nx.os.open(p, F)\nos.fdopen(p, F)\nos().open(p, F)\n",
    "starred first": GOOD + "os.open(*a, F)\n",
    "starred flags": GOOD + "os.open(p, *F)\n",
    "no flags": GOOD + "os.open(p)\nos.open(p, **kw)\nos.open(p, mode=F)\n",
}

# Module-level statements other than the module body: each binds F once, at module level.
MODULE_SCOPE = {
    "if": "import os\nif c:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "else": "import os\nif c:\n    pass\nelse:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "try": "import os\ntry:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nexcept E:\n    pass\nos.open(p, F)\n",
    "handler": "import os\ntry:\n    pass\nexcept E:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "finally": "import os\ntry:\n    pass\nfinally:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "with": "import os\nwith c:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "while": "import os\nwhile c:\n    F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
    "match": "import os\nmatch x:\n    case 1:\n        F = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n",
}


class NoMutant(unittest.TestCase):
    def test_positive_control(self):
        self.assertEqual(len(made(GOOD + "os.open(p, F)\n")), 2)

    def test_no_mutant(self):
        for case, text in NO_MUTANT.items():
            with self.subTest(case):
                self.assertEqual(made(text), {})

    def test_bound_once_in_a_module_level_statement(self):
        for case, text in MODULE_SCOPE.items():
            with self.subTest(case):
                self.assertEqual(len(made(text)), 2)


class EndToEnd(unittest.TestCase):
    """M70 (W/staged/310/NOTES.md:56): the definition mutant is killed, the entry call site survives."""

    def setUp(self):
        self.lane = os.path.realpath(tempfile.mkdtemp(prefix="gm-callsite-lane-"))
        self.addCleanup(shutil.rmtree, self.lane, ignore_errors=True)
        self.outdir = os.path.realpath(tempfile.mkdtemp(prefix="gm-callsite-out-"))
        self.addCleanup(shutil.rmtree, self.outdir, ignore_errors=True)
        for name, text in (("mod.py", FIXTURE), ("check.py", CHECK)):
            with open(os.path.join(self.lane, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(self.lane)

    def run_tool(self, out: str, *check_args: str) -> tuple[dict, str]:
        test = " ".join(shlex.quote(a) for a in (sys.executable, "-B", "check.py", *check_args))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()) as err:
            rc = gm.main(["--file", "mod.py", "--test", test, "--out", os.path.join(self.outdir, out)])
        self.assertIn(rc, (0, 1), err.getvalue())
        with open(os.path.join(self.outdir, out), encoding="utf-8") as fh:
            rows = {r["id"]: r for r in json.load(fh)}
        with open(os.path.join(self.lane, "mod.py"), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), FIXTURE)
        return rows, stdout.getvalue()

    def test_m70_survives_when_the_test_checks_only_site_1(self):
        rows, printed = self.run_tool("one.json")
        definition = rows[f"mod.py:{DEF_LINE}:26:flag-drop:O_DIRECTORY"]
        self.assertEqual((definition["operator"], definition["result"]), ("flag-drop", "killed"))
        site2 = f"mod.py:{SITE2}:{SITE2_COL}:{OP}:O_DIRECTORY"
        self.assertEqual(rows[site2]["result"], "survived")
        self.assertEqual(rows[site2]["location"], f"mod.py:{SITE2}")
        self.assertEqual(rows[site2]["operator"], OP)
        self.assertIn(f"survived {site2}: DIR_FLAGS -> (DIR_FLAGS & ~os.O_DIRECTORY) [exit 0]", printed)
        self.assertEqual(rows[f"mod.py:{SITE1}:{SITE1_COL}:{OP}:O_DIRECTORY"]["result"], "killed")

    def test_m70_killed_when_the_test_checks_site_2(self):
        rows, printed = self.run_tool("both.json", "both")
        for line, col in ((SITE1, SITE1_COL), (SITE2, SITE2_COL)):
            self.assertEqual(rows[f"mod.py:{line}:{col}:{OP}:O_DIRECTORY"]["result"], "killed")
        self.assertNotIn(f"{OP}:O_DIRECTORY", printed)
        self.assertEqual(rows[f"mod.py:{SITE2}:{SITE2_COL}:{OP}:O_RDONLY"]["result"], "survived")  # O_RDONLY is 0


if __name__ == "__main__":
    unittest.main()
