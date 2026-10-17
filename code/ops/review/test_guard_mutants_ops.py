"""Step 318: guard_mutants loads its mutation operators from mutant_ops/, and the mutants stay HEAD's.

The suite makes no git call (the ship gate runs it in lane copies that have no .git). Requirement 3 has two
forms. In the suite: a fixture corpus that reaches every operator of mutant_ops.base and every branch of the
shared helpers, checked against a digest that 2a21541b's tool made (PINNED_* below). At ship: --head-oracle,
run by hand from the lane root, compares HEAD's tool with mutant_ops.base.OPERATORS on every tracked code/*.py
file at HEAD. Fixture operator modules live in temp dirs made by the tests and removed by addCleanup; nothing
is written under code/.
"""
from __future__ import annotations

import ast
import collections
import contextlib
import errno
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
import warnings
from unittest import mock

import guard_mutants as gm
import mutant_ops
from mutant_ops import base

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, os.pardir, "tests"))
import fault_kit as fk  # noqa: E402  (code/tests/fault_kit.py: the standard filesystem attacks)

TOOL_REL = "code/ops/review/guard_mutants.py"


def rows(mod, rel: str, data: bytes, *args):
    """(id, change, sha256 of source) of each mutant, or the refusal text."""
    try:
        return {(m.id, m.change, hashlib.sha256(m.source).hexdigest()) for m in mod.mutants_for(rel, data, *args)}
    except mod.Refusal as exc:
        return ("refused", str(exc))


class TempDirs(unittest.TestCase):
    def mkdtemp(self) -> str:
        path = os.path.realpath(tempfile.mkdtemp(prefix="gm-ops-"))
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

    def ops_dir(self, **modules: str) -> str:
        path = self.mkdtemp()
        for name, body in sorted(modules.items(), reverse=True):  # written in reverse order of their names
            with open(os.path.join(path, name), "w", encoding="utf-8") as fh:
                fh.write(textwrap.dedent(body))
        return path


# ---- requirement 3 in the suite: a fixture corpus and a pinned digest ----------------

def _crlf(text: str) -> bytes:
    return text.replace("\n", "\r\n").encode("utf-8")


CORPUS = (
    ("guards.py", br"""
def f(x, y):
    if x:
        raise ValueError(x)
    if y:
        return 1
    else:
        raise KeyError(y)
    if x > 1:
        pass
    elif y:
        raise TypeError
    if x:
        pass
    else:
        if y:
            pass
        raise OSError
    if x:
        pass
    else:
        x = 2
    if not x:
        y = 3
        return y
    if x:
        for i in y:
            raise LookupError
    while x:
        if y: raise RuntimeError
    if x: return
    return 0
"""),
    ("flags.py", br"""
import os, sys
A = os.O_RDONLY | os.O_NOFOLLOW
B = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
C = os.O_RDONLY | (mode & 3) | sys.O_X | os.path | flags | -x
flags = 0
flags |= os.O_APPEND
flags |= getattr(os, "O_BINARY", 0) | os.O_TRUNC
flags |= other
flags &= os.O_SYNC
D = getattr(os, name) | getattr(sys, "O_A") | getattr(os, 3) | getattr(os) | getattr("O_A", os) | os.O_SYNC
E = (os.O_DSYNC | os.O_RSYNC) | x.os.O_X | getattr(os, "path")
F = x | y
G = os.O_RDWR & os.O_EXCL
H = a[0] | (os.O_B | c) | f(os.O_C | os.O_D)
I = os.O_A + os.O_B | "s" | getit(os, "O_E")
"""),
    ("regex.py", br"""
import re
re.compile(r"a+b")
re.match(r"\d{3}-\d{2,4}x{2,}y{,3}z{0}w{0,2}")
re.search(r"\++[+]+[^]+]+[]a]+[\]+]+")
re.fullmatch(r"a*+b++c?+d+?e{2}+f{1}?g*?+")
re.findall(pattern=r"(ab)+", string=s)
re.sub(b"q+\\w{2}\xff+", b"", data)
re.finditer(r"x{a}+{")
re.split(r"[")
re.subn(r"[^")
re.compile("a\\")
re.compile("a\\+[^a-z]+[^\\]]+")
re.escape(r"a+")
regex.compile(r"a+")
re.compile(p + "a+")
re.compile(flags=0)
re.compile()
re.compile(3)
x.re.compile(r"a+")
compile(r"a+")
re.compile(r"[]")
"""),
    ("excepts.py", br"""
import builtins
try:
    pass
except ValueError:
    pass
except (KeyError, OSError) as e:
    pass
except Exception:
    pass
except builtins.Exception:
    pass
except:
    pass
try:
    pass
except  :
    raise
try:
    pass
except* ValueError:
    pass
"""),
    ("loops.py", br"""
import os
for chunk in chunks:
    os.write(fd, chunk)
while left:
    n = os.pwrite(fd, buf, off)
    left -= n
async def g():
    async for x in it:
        await w.writev([x])
for x in y:
    def inner():
        write(x)
    async def ainner():
        write(x)
    class K:
        def write(self): fh.write(1)
    cb = lambda: fh.write(2)
for x in y:
    log(x)
for x in y:
    print(x); fh.write(x); write(x)
for x in y: h()(x).write(b); get()(x)
for x in y: get()(x)
for x in y:
    z = fh.write(1) if fh.write(0) else 0
while True:
    for a in b:
        out.write(a)
    sock.send(x)
for x in y:
    class K2:
        fh.write(3)
for x in y:
    pwrite(fd, x, 0)
"""),
    ("utf8_crlf.py", _crlf("""\
s = "éé"; flags = os.O_A | os.O_B
if s: raise ValueError("é")
try:
    t = "é"; re.compile("é+")
except "é" and OSError:
    pass
for é in s:
    f.write(é)
""")),
)

# Made by 2a21541b's tool, the last tool before the split, with this command from the lane root:
#   .venv/bin/python -B code/ops/review/test_guard_mutants_ops.py --pin 2a21541b
# (git show 2a21541b:code/ops/review/guard_mutants.py into a temp dir, imported as guard_mutants_head, then
# corpus_pin(minus_inert(head.mutants_for))). Never edit these by hand; never make them with the working tree's tool.
PINNED_DIGEST = "dd4c23b3323aff0a47e6dc9f1f14bfd09d84e3d9db517e3f077dfe319af6343b"
PINNED_COUNTS = {"except-class": 5, "except-remove": 8, "flag-drop": 16, "negate-if": 8, "raise-remove": 6,
                 "regex-zero": 22, "write-loop": 10}


def _flag(node: ast.AST) -> str | None:
    """The O_* name of os.O_X or getattr(os, "O_X", ...), else None."""
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "os" \
            and node.attr.startswith("O_"):
        return node.attr
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr" \
            and len(node.args) >= 2 and isinstance(node.args[0], ast.Name) and node.args[0].id == "os" \
            and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str) \
            and node.args[1].value.startswith("O_"):
        return node.args[1].value
    return None


def _chain(node: ast.AST) -> list[ast.AST]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _chain(node.left) + _chain(node.right)
    return [node]


def inert_ids(rel: str, data: bytes) -> set[str]:
    """Ids of the flag-drop mutants that Step 328's out:(1)-(2) remove, as 2a21541b's tool names them: a flag
    with getattr(os, name, None) == 0 in a `|` chain or `|=`, and O_NOFOLLOW in a `|` chain that also names
    O_CREAT and O_EXCL. Written here, never imported from mutant_ops: the pin stays a check against the old tool."""
    ids = set()
    for node in ast.walk(ast.parse(data)):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            ops = _chain(node)  # an inner chain names a subset of its root's flags: same result as the root
        elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.BitOr):
            ops = [node.value]
        else:
            continue
        names = {_flag(o) for o in ops}
        for o in ops:
            flag = _flag(o)
            if flag is not None and (getattr(os, flag, None) == 0 or
                                     (flag == "O_NOFOLLOW" and {"O_CREAT", "O_EXCL"} <= names)):
                ids.add(f"{rel}:{o.lineno}:{o.col_offset}:flag-drop:{flag}")
    return ids


def minus_inert(mutants_for):
    """mutants_for, less the mutants whose ids inert_ids gives."""
    def made(rel: str, data: bytes) -> list:
        mutants, inert = mutants_for(rel, data), inert_ids(rel, data)
        return [m for m in mutants if m.id not in inert]
    return made


def corpus_pin(mutants_for) -> tuple[str, dict[str, int]]:
    """sha256 of every fixture's sorted (id, change, sha256 of source) list, and the mutants per operator."""
    listing, counts = [], collections.Counter()
    for rel, data in CORPUS:
        made = mutants_for(rel, data)
        counts.update(m.operator for m in made)
        listing.append([rel, sorted([m.id, m.change, hashlib.sha256(m.source).hexdigest()] for m in made)])
    digest = hashlib.sha256(json.dumps(listing, ensure_ascii=True).encode("ascii")).hexdigest()
    return digest, dict(sorted(counts.items()))


class SameMutantsAsHead(unittest.TestCase):
    def test_base_operators_make_the_pinned_mutants(self):
        digest, counts = corpus_pin(lambda rel, data: gm.mutants_for(rel, data, gm.WHOLE, base.OPERATORS))
        self.assertEqual(counts, PINNED_COUNTS)
        self.assertEqual(digest, PINNED_DIGEST)

    def test_the_corpus_reaches_every_operator(self):
        self.assertEqual(len(base.OPERATORS), 7)
        self.assertEqual(sorted(PINNED_COUNTS), ["except-class", "except-remove", "flag-drop", "negate-if",
                                                 "raise-remove", "regex-zero", "write-loop"])
        self.assertTrue(all(n > 0 for n in PINNED_COUNTS.values()), PINNED_COUNTS)

    def test_default_operators_include_base_in_sorted_module_order(self):
        loaded = mutant_ops.load_operators()
        order = list(dict.fromkeys(fn.__module__ for fn in loaded))
        self.assertIn("mutant_ops.base", order)
        self.assertEqual(order, sorted(order))
        listed = {"mutant_ops." + e[:-3] for e in os.listdir(mutant_ops.OPS_DIR)
                  if e.endswith(".py") and not e.startswith("_")}
        self.assertLessEqual(set(order), listed)
        self.assertEqual([fn.__qualname__ for fn in loaded if fn.__module__ == "mutant_ops.base"],
                         [fn.__qualname__ for fn in base.OPERATORS])
        for rel, data in CORPUS:  # the default operators make at least base's mutants, with the same ids
            self.assertLessEqual(rows(gm, rel, data, gm.WHOLE, base.OPERATORS), rows(gm, rel, data), rel)


# ---- requirement 3 at ship: HEAD's tool on every tracked code file (git; never run by the suite) ----

def git(*args: str, data: bytes | None = None) -> bytes:
    proc = subprocess.run(["git", *args], cwd=HERE, input=data, capture_output=True)
    if proc.returncode:
        raise SystemExit(f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.decode(errors='replace')}")
    return proc.stdout


def head_blobs() -> dict[str, bytes]:
    """HEAD's bytes of every tracked .py file under code/, read with one git cat-file --batch."""
    tree = git("ls-tree", "--full-tree", "-r", "-z", "--name-only", "HEAD:code")
    names = ["code/" + n.decode() for n in tree.split(b"\0") if n.endswith(b".py")]
    out = git("cat-file", "--batch", data="".join(f"HEAD:{n}\n" for n in names).encode())
    blobs, at = {}, 0
    for name in names:
        end = out.index(b"\n", at)
        header = out[at:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise SystemExit(f"git cat-file HEAD:{name} gave {out[at:end]!r}")
        size = int(header[2])
        blobs[name] = out[end + 1:end + 1 + size]
        at = end + 1 + size + 1
    if at != len(out):
        raise SystemExit("git cat-file gave more output than the files asked for")
    return blobs


def tool_at(rev: str, tmp: str):
    """rev's guard_mutants.py, loaded from tmp as the module guard_mutants_head."""
    path = os.path.join(tmp, "guard_mutants_head.py")
    with open(path, "wb") as fh:
        fh.write(git("show", f"{rev}:{TOOL_REL}"))
    spec = importlib.util.spec_from_file_location("guard_mutants_head", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["guard_mutants_head"] = mod
    spec.loader.exec_module(mod)
    if mod.mutants_for is gm.mutants_for:
        raise SystemExit(f"{rev}'s tool is the working tree's module")
    return mod


def head_oracle() -> int:
    """Exit 0 when HEAD's tool, less inert_ids, and mutant_ops.base.OPERATORS give the same set for every
    tracked code file."""
    t0, tmp = time.monotonic(), tempfile.mkdtemp(prefix="gm-ops-oracle-")
    try:
        head, blobs = tool_at("HEAD", tmp), head_blobs()
        bad, total = [], 0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # some tracked files have invalid escapes: ast.parse warns, both alike
            for rel, data in sorted(blobs.items()):
                want = rows(head, rel, data)
                if isinstance(want, set):
                    inert = inert_ids(rel, data)
                    want = {r for r in want if r[0] not in inert}
                if rows(gm, rel, data, gm.WHOLE, base.OPERATORS) != want:
                    bad.append(rel)
                total += len(want) if isinstance(want, set) else 0
    finally:
        sys.modules.pop("guard_mutants_head", None)
        shutil.rmtree(tmp, ignore_errors=True)
    for rel in bad:
        print(f"head-oracle: DIFFERS {rel}")
    ok = not bad and TOOL_REL in blobs and total > 1000
    print(f"head-oracle: {'OK' if ok else 'FAIL'} files={len(blobs)} differ={len(bad)} mutants={total} "
          f"seconds={time.monotonic() - t0:.1f}")
    return 0 if ok else 1


def pin(rev: str) -> int:
    """Print the PINNED_* values that rev's tool, less inert_ids, gives on CORPUS."""
    tmp = tempfile.mkdtemp(prefix="gm-ops-pin-")
    try:
        digest, counts = corpus_pin(minus_inert(tool_at(rev, tmp).mutants_for))
    finally:
        sys.modules.pop("guard_mutants_head", None)
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"PINNED_DIGEST = {digest!r}\nPINNED_COUNTS = {counts!r}")
    return 0


# ---- requirement 2: discovery -------------------------------------------------------

MARK = '''\
import ast


def mark(tree, src, add):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            add(node, "{op}", "", "{change}", *src.span(node), b"pass")
            add(node, "dup", "", "dup from {op}", *src.span(node), b"pass")


OPERATORS = (mark,)
'''
SOURCE = b"x = 1\ny = 2\n"


class Discovery(TempDirs):
    def test_sorted_names_private_not_loaded_ids_sorted_after_all_operators(self):
        d = self.ops_dir(**{
            "b_second.py": MARK.format(op="aa-mark", change="b"),
            "a_first.py": MARK.format(op="zz-mark", change="a"),
            "_private.py": "raise RuntimeError('a _ module was loaded')\nOPERATORS = ()\n",
            "notes.txt": "not a module\n",
        })
        listdir = os.listdir
        for order in (sorted, lambda names: sorted(names, reverse=True)):  # whatever order the listing gives
            with mock.patch.object(os, "listdir", lambda path: order(listdir(path))):
                ops = mutant_ops.load_operators(d)
            self.assertEqual([fn.__module__.rsplit(".", 1)[-1] for fn in ops], ["a_first", "b_second"])
        got = [(m.id, m.change) for m in gm.mutants_for("m.py", SOURCE, gm.WHOLE, ops)]
        self.assertEqual(got, [
            ("m.py:1:0:aa-mark", "b"), ("m.py:1:0:dup", "dup from zz-mark"), ("m.py:1:0:dup#2", "dup from aa-mark"),
            ("m.py:1:0:zz-mark", "a"),
            ("m.py:2:0:aa-mark", "b"), ("m.py:2:0:dup", "dup from zz-mark"), ("m.py:2:0:dup#2", "dup from aa-mark"),
            ("m.py:2:0:zz-mark", "a"),
        ])
        self.assertEqual(gm.mutants_for("m.py", SOURCE, gm.WHOLE, ops)[0].source, b"pass\ny = 2\n")

    def test_add_keeps_the_line_filter(self):
        ops = mutant_ops.load_operators(self.ops_dir(**{"m.py": MARK.format(op="mark", change="c")}))
        got = [m.id for m in gm.mutants_for("m.py", SOURCE, {2}, ops)]
        self.assertEqual(got, ["m.py:2:0:dup", "m.py:2:0:mark"])
        self.assertEqual([m.line for m in gm.mutants_for("m.py", SOURCE, {2}, ops)], [2, 2])

    def test_each_operator_gets_the_tree_the_source_and_add(self):
        d = self.ops_dir(**{"seen.py": '''\
            SEEN = []


            def look(tree, src, add):
                SEEN.append((type(tree).__name__, src.data, add.__code__.co_varnames[:7]))


            OPERATORS = (look,)
            '''})
        ops = mutant_ops.load_operators(d)
        self.assertEqual(gm.mutants_for("m.py", SOURCE, gm.WHOLE, ops), [])
        self.assertEqual(ops[0].__globals__["SEEN"],
                         [("Module", SOURCE, ("node", "op", "tag", "change", "a", "b", "new"))])

    def test_no_mutant_ops_module_imports_guard_mutants(self):
        for name in sorted(os.listdir(mutant_ops.OPS_DIR)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(mutant_ops.OPS_DIR, name), "rb") as fh:
                tree = ast.parse(fh.read())
            imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            imported |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
            self.assertFalse({m for m in imported if m.split(".")[0] == "guard_mutants"}, name)


# ---- requirement 4: refusals (exit 2) -----------------------------------------------

class Refusals(TempDirs):
    def assertModuleRefused(self, ops_dir: str, *needles: str) -> None:
        with self.assertRaises(mutant_ops.Refusal) as caught:
            mutant_ops.load_operators(ops_dir)
        for needle in needles:
            self.assertIn(needle, str(caught.exception))
        self.assertMainRefused(ops_dir, *needles)

    def assertMainRefused(self, ops_dir: str, *needles: str) -> None:
        out = os.path.join(self.mkdtemp(), "out.json")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = gm.main(["--file", "x.py", "--test", "true", "--out", out], ops_dir=ops_dir)
        self.assertEqual(rc, 2)
        for needle in needles:
            self.assertIn(needle, err.getvalue())
        self.assertFalse(os.path.lexists(out))

    def test_module_that_fails_to_import(self):
        d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "broken.py": "import no_such_module_318\n"})
        self.assertModuleRefused(d, os.path.join(d, "broken.py"), "does not import", "no_such_module_318")

    def test_module_with_a_syntax_error(self):
        d = self.ops_dir(**{"bad.py": "def f(:\n"})
        self.assertModuleRefused(d, os.path.join(d, "bad.py"), "does not import", "SyntaxError")

    def test_module_without_operators(self):
        d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "none.py": "X = 1\n"})
        self.assertModuleRefused(d, os.path.join(d, "none.py"), "no OPERATORS")

    def test_operators_not_a_tuple_of_functions(self):
        for body in ("OPERATORS = [print]\n", "OPERATORS = (print, 3)\n", "OPERATORS = None\n"):
            with self.subTest(body=body):
                d = self.ops_dir(**{"odd.py": body})
                self.assertModuleRefused(d, os.path.join(d, "odd.py"), "no OPERATORS")

    def test_directory_without_modules(self):
        d = self.ops_dir(**{"_only.py": "OPERATORS = ()\n", "readme.txt": "x\n"})
        self.assertModuleRefused(d, d, "no operator module")

    def test_missing_directory(self):
        d = os.path.join(self.mkdtemp(), "absent")
        with self.assertRaises(FileNotFoundError):
            mutant_ops.load_operators(d)
        self.assertMainRefused(d, d, "ENOENT")

    def test_mutant_that_does_not_parse_names_operator_and_id(self):
        d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "breaks.py": '''\
            import ast


            def unbalance(tree, src, add):
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign) and node.lineno == 2:
                        add(node, "unbalance", "", "x -> (", *src.span(node), b"(")


            OPERATORS = (unbalance,)
            '''})
        ops = mutant_ops.load_operators(d)
        made = gm.mutants_for("m.py", SOURCE, gm.WHOLE, ops)
        self.assertIn("m.py:2:0:unbalance", [m.id for m in made])
        with self.assertRaises(mutant_ops.Refusal) as caught:
            gm.parsed(made)
        self.assertIn("operator unbalance made m.py:2:0:unbalance", str(caught.exception))
        self.assertIn("does not parse", str(caught.exception))
        in_scope = gm.mutants_for("m.py", SOURCE, {1}, ops)  # line 2 is out of scope: never made
        self.assertEqual(gm.parsed(in_scope), in_scope)
        self.assertEqual([m.id for m in in_scope], ["m.py:1:0:dup", "m.py:1:0:m"])

        lane = self.mkdtemp()
        with open(os.path.join(lane, "m.py"), "wb") as fh:
            fh.write(SOURCE)
        out = os.path.join(self.mkdtemp(), "out.json")
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(lane)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = gm.main(["--file", "m.py", "--test", "true", "--out", out], ops_dir=d)
        self.assertEqual(rc, 2)
        self.assertIn("operator unbalance made m.py:2:0:unbalance", err.getvalue())
        self.assertFalse(os.path.lexists(out))
        with open(os.path.join(lane, "m.py"), "rb") as fh:
            self.assertEqual(fh.read(), SOURCE)


# ---- discovery reads each module from one fd (O_NOFOLLOW | O_NONBLOCK, fstat-checked) --------

OUTSIDE = 'open({marker!r}, "x").close()\nOPERATORS = ()\n'


class FilesystemRefusals(TempDirs):
    def setUp(self):
        self.ops = self.ops_dir(**{"ops.py": MARK.format(op="m", change="c")})
        self.module = os.path.join(self.ops, "ops.py")
        away = self.mkdtemp()
        self.marker = os.path.join(away, "ran")  # made only when outside.py runs
        self.outside = os.path.join(away, "outside.py")
        with open(self.outside, "w", encoding="utf-8") as fh:
            fh.write(OUTSIDE.format(marker=self.marker))

    @staticmethod
    def at_module(path, *args, **kwargs) -> bool:  # the open of ops.py, after the listing
        return path == "ops.py"

    def assertRefused(self, ops_dir: str, *needles: str) -> None:
        with self.assertRaises(mutant_ops.Refusal) as caught:
            mutant_ops.load_operators(ops_dir)
        for needle in needles:
            self.assertIn(needle, str(caught.exception))
        self.assertFalse(os.path.lexists(self.marker), "code outside the operator directory ran")

    def assertMainRefused(self, ops_dir: str, *needles: str) -> None:
        out = os.path.join(self.mkdtemp(), "out.json")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = gm.main(["--file", "x.py", "--test", "true", "--out", out], ops_dir=ops_dir)
        self.assertEqual(rc, 2)
        for needle in needles:
            self.assertIn(needle, err.getvalue())
        self.assertFalse(os.path.lexists(out))
        self.assertFalse(os.path.lexists(self.marker), "code outside the operator directory ran")

    def test_the_outside_module_leaves_a_marker_when_it_runs(self):  # positive control of the marker
        self.assertEqual(mutant_ops.load_operators(self.ops_dir(**{"o.py": OUTSIDE.format(marker=self.marker)})), ())
        self.assertTrue(os.path.exists(self.marker))

    def test_symlink_swapped_in_between_listing_and_open(self):
        with fk.swap_for_symlink("open", 1, self.module, self.outside, match=self.at_module):
            self.assertRefused(self.ops, self.module, "ELOOP")
        self.setUp()
        with fk.swap_for_symlink("open", 1, self.module, self.outside, match=self.at_module):
            self.assertMainRefused(self.ops, self.module, "ELOOP")

    def test_symlink_swapped_in_after_the_open_is_never_read(self):
        with fk.swap_for_symlink("open", 1, self.module, self.outside, when="after", match=self.at_module):
            ops = mutant_ops.load_operators(self.ops)
        self.assertEqual([fn.__module__ for fn in ops], ["mutant_ops.ops"])
        self.assertFalse(os.path.lexists(self.marker), "the module path was opened a second time")

    def test_link_in_place_of_a_module(self):
        for target in (self.outside, os.path.join(self.mkdtemp(), "absent.py")):
            with self.subTest(target=target):
                link = os.path.join(self.ops, "zz.py")
                with contextlib.suppress(FileNotFoundError):
                    os.unlink(link)
                os.symlink(target, link)
                self.assertRefused(self.ops, link, "ELOOP")

    def test_fifo_in_place_of_a_module(self):
        with fk.fifo_in_place(self.module, name="open", match=self.at_module, timeout=2):
            self.assertRefused(self.ops, self.module, "is a FIFO, not a regular file")
        self.setUp()
        with fk.fifo_in_place(self.module, timeout=2):
            self.assertMainRefused(self.ops, self.module, "is a FIFO, not a regular file")

    def test_oserror_on_open_fstat_read_close(self):
        for name in ("open", "fstat", "read", "close"):
            with self.subTest(name=name):
                self.setUp()
                with fk.inject_oserror(name, 1, errno.EIO, match=self.at_module if name == "open" else None):
                    self.assertRefused(self.ops, self.module, "[EIO]")

    def test_unexpected_error_surfaces(self):
        for name in ("open", "fstat", "read", "close"):
            with self.subTest(name=name):
                self.setUp()
                with fk.raise_unexpected(name, 1, RuntimeError, match=self.at_module if name == "open" else None):
                    with self.assertRaises(RuntimeError):
                        mutant_ops.load_operators(self.ops)

    def test_directory_that_is_a_symlink(self):
        link = os.path.join(self.mkdtemp(), "ops")
        os.symlink(self.ops, link)
        with self.assertRaises(OSError) as caught:
            mutant_ops.load_operators(link)
        code = errno.errorcode[caught.exception.errno]
        self.assertIn(code, ("ELOOP", "ENOTDIR"))  # O_DIRECTORY | O_NOFOLLOW on a link: macOS gives ENOTDIR
        self.assertMainRefused(link, link, f"[{code}]")

    def test_directory_replaced_by_a_fifo(self):
        ops = os.path.join(self.mkdtemp(), "ops")  # the kit parks it next to itself: inside a temp dir
        os.rename(self.ops, ops)
        with fk.fifo_in_place(ops, timeout=2):
            with self.assertRaises(NotADirectoryError):
                mutant_ops.load_operators(ops)
            self.assertMainRefused(ops, ops, "ENOTDIR")


# ---- a module's own exits refuse; each module is read whole; no fd outlives the load ----------

MAIN = ("import sys\nimport guard_mutants as gm\n"
        "sys.exit(gm.main(['--file', 'x.py', '--test', 'true', '--out', sys.argv[2]], ops_dir=sys.argv[1]))\n")
TWO = '''\
import ast


def first(tree, src, add):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            add(node, "first", "", "first", *src.span(node), b"pass")
{pad}

def second(tree, src, add):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            add(node, "second", "", "second", *src.span(node), b"pass")


OPERATORS = (first, second)
'''


def open_fds() -> int:
    return len(os.listdir("/dev/fd"))


class ModuleExits(TempDirs):
    def run_main(self, ops_dir: str) -> tuple[subprocess.CompletedProcess, str]:
        """main in a child process (a SystemExit that escapes main ends the child, not this suite)."""
        lane = self.mkdtemp()
        with open(os.path.join(lane, "x.py"), "wb") as fh:
            fh.write(b"if x: raise ValueError\n")
        out = os.path.join(self.mkdtemp(), "out.json")
        env = dict(os.environ, PYTHONPATH=HERE, LLMDB_ROOT=lane)
        proc = subprocess.run([sys.executable, "-B", "-c", MAIN, ops_dir, out], cwd=lane, env=env,
                              capture_output=True, text=True, timeout=20)  # under the gate's 60 s
        return proc, out

    def test_control_main_in_a_child_reports(self):  # positive control of run_main
        proc, out = self.run_main(self.ops_dir(**{"ok.py": MARK.format(op="m", change="c")}))
        self.assertNotEqual(proc.returncode, 2, proc.stderr)
        self.assertTrue(os.path.exists(out), proc.stderr)

    def test_system_exit_and_base_exceptions_of_a_module_refuse(self):
        odd = "class Odd318(BaseException):\n    pass\n\n\nraise Odd318('odd 318')\n"
        for body, needle in (("raise SystemExit(0)\n", "SystemExit: 0"), ("raise SystemExit(3)\n", "SystemExit: 3"),
                             (odd, "Odd318: odd 318")):
            with self.subTest(body=body):
                d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "zz_exit.py": body})
                path = os.path.join(d, "zz_exit.py")
                with self.assertRaises(mutant_ops.Refusal) as caught:
                    mutant_ops.load_operators(d)
                self.assertIn(f"operator module {path} does not import: {needle}", str(caught.exception))
                self.assertNotIn("mutant_ops.zz_exit", sys.modules)
                proc, out = self.run_main(d)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn(f"operator module {path} does not import: {needle}", proc.stderr)
                self.assertFalse(os.path.lexists(out))

    def test_keyboard_interrupt_of_a_module_propagates(self):
        d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "zz_ki.py": "raise KeyboardInterrupt('ki 318')\n"})
        self.addCleanup(sys.modules.pop, "mutant_ops.zz_ki", None)
        with self.assertRaises(KeyboardInterrupt) as caught:
            mutant_ops.load_operators(d)
        self.assertEqual(str(caught.exception), "ki 318")


class WholeReads(TempDirs):
    def ids(self, ops: tuple) -> list:
        return [m.id for m in gm.mutants_for("m.py", SOURCE, {1}, ops)]

    def test_short_reads_give_every_operator(self):
        d = self.ops_dir(**{"two.py": TWO.format(pad="")})
        read, calls = os.read, []

        def short(fd, n):
            calls.append(n)
            return read(fd, min(n, 7))

        with mock.patch("os.read", short):
            ops = mutant_ops.load_operators(d)
        self.assertGreater(len(calls), 2)
        self.assertEqual([fn.__name__ for fn in ops], ["first", "second"])
        self.assertEqual(self.ids(ops), ["m.py:1:0:first", "m.py:1:0:second"])

    def test_module_larger_than_one_read_gives_every_operator(self):
        pad = "# " + "p" * 1021 + "\n"
        d = self.ops_dir(**{"two.py": TWO.format(pad=pad * 2048)})  # 2 MiB of comment between the operators
        self.assertGreater(os.path.getsize(os.path.join(d, "two.py")), 2 << 20)
        ops = mutant_ops.load_operators(d)
        self.assertEqual([fn.__name__ for fn in ops], ["first", "second"])
        self.assertEqual(self.ids(ops), ["m.py:1:0:first", "m.py:1:0:second"])


class NoFdLeak(TempDirs):
    def assertSameFds(self, call) -> None:
        with contextlib.suppress(mutant_ops.Refusal):
            call()  # a first call may open what it keeps for good (lazy imports)
        before = open_fds()
        with contextlib.suppress(mutant_ops.Refusal):
            call()
        self.assertEqual(open_fds(), before)

    def test_positive_control_counts_a_leaked_fd(self):
        before = open_fds()
        fd = os.open(self.mkdtemp(), os.O_RDONLY)
        self.addCleanup(os.close, fd)
        self.assertEqual(open_fds(), before + 1)

    def test_success_leaves_no_fd(self):
        d = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c")})
        self.assertEqual(len(mutant_ops.load_operators(d)), 1)
        self.assertSameFds(lambda: mutant_ops.load_operators(d))

    def test_refusals_leave_no_fd(self):
        no_ops = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "none.py": "X = 1\n"})
        fifo = self.ops_dir(**{"ok.py": MARK.format(op="m", change="c"), "zz.py": MARK.format(op="z", change="c")})
        for d, needle, attack in ((no_ops, "no OPERATORS", contextlib.nullcontext()),
                                  (fifo, "is a FIFO", fk.fifo_in_place(os.path.join(fifo, "zz.py"), timeout=2))):
            with self.subTest(needle=needle), attack:  # the FIFO body never blocks past 2 s
                with self.assertRaises(mutant_ops.Refusal) as caught:
                    mutant_ops.load_operators(d)
                self.assertIn(needle, str(caught.exception))
                self.assertSameFds(lambda: mutant_ops.load_operators(d))


if __name__ == "__main__":
    if sys.argv[1:] == ["--head-oracle"]:
        sys.exit(head_oracle())
    if len(sys.argv) == 3 and sys.argv[1] == "--pin":
        sys.exit(pin(sys.argv[2]))
    unittest.main()
