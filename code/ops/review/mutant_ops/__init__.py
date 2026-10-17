"""The mutation operators of guard_mutants.py: shared helpers, and discovery of the operator modules.

Each module in the operator directory whose name does not start with "_" exports OPERATORS, a tuple of
functions fn(tree, src, add). tree is the file's ast.Module and src its _Source; each function walks the
tree itself and calls add(node, op, tag, change, a, b, new) once per mutant: the bytes src.data[a:b]
become new, anchored at node (its lineno must be in the file's line scope). Modules load in sorted name
order. Ids do not depend on that order: guard_mutants sorts every mutant after all operators ran.

This package never imports guard_mutants: run as a script, the tool is __main__, and an import of
guard_mutants would load a second copy of it.
"""
from __future__ import annotations

import ast
import errno
import os
import re
import stat
import sys
import types

OPS_DIR = os.path.dirname(os.path.abspath(__file__))
# O_RDONLY is 0: named in these chains it would make a flag-drop mutant that no test can kill.
DIR_FLAGS = os.O_DIRECTORY | os.O_NOFOLLOW
MODULE_FLAGS = os.O_NOFOLLOW | os.O_NONBLOCK  # a FIFO in place of a module never blocks the open
KINDS = {stat.S_IFDIR: "directory", stat.S_IFIFO: "FIFO", stat.S_IFCHR: "character device",
         stat.S_IFBLK: "block device", stat.S_IFSOCK: "socket", stat.S_IFLNK: "symlink"}
WRITE_CALLS = frozenset({"write", "pwrite", "writev"})
RE_FUNCS = frozenset({"compile", "match", "fullmatch", "search", "findall", "finditer", "sub", "subn", "split"})
NEVER = '__import__("builtins").type("GuardMutantNever", (BaseException,), {})'
BRACE = re.compile(r"\{(\d*)(?:,(\d*))?\}")
SIMPLE = (ast.Name, ast.Attribute, ast.Call, ast.Constant, ast.Subscript)


class Refusal(Exception):
    """Input the tool will not judge; every input stays unchanged."""


def load_operators(directory: str = OPS_DIR) -> tuple:
    """Every operator of every module in directory not named _*, in sorted module-name order.

    The directory is opened once and listed from its fd; each module is opened from that fd with
    O_NOFOLLOW | O_NONBLOCK, and the bytes that run are the bytes read from the fd that fstat found a
    regular file (a path swapped after the listing is never read). A directory without such a module, a
    module that is not a regular file or cannot be read, a module that fails to import, and a module
    whose OPERATORS is not a tuple of callables refuse. An OSError of the directory reaches the caller."""
    dir_fd = os.open(directory, DIR_FLAGS)
    try:
        names = sorted(e[:-3] for e in os.listdir(dir_fd) if e.endswith(".py") and not e.startswith("_"))
        if not names:
            raise Refusal(f"operator directory {directory} has no operator module")
        operators: list = []
        for name in names:
            path = os.path.join(directory, name + ".py")
            module = types.ModuleType(f"{__name__}.{name}")
            module.__file__, module.__package__ = path, __name__
            code = _read_module(dir_fd, name + ".py", path)
            sys.modules[module.__name__] = module
            try:
                exec(compile(code, path, "exec", dont_inherit=True), module.__dict__)
            except Exception as exc:  # any failure of an operator module's own code is a refusal
                del sys.modules[module.__name__]
                raise Refusal(f"operator module {path} does not import: {type(exc).__name__}: {exc}") from exc
            ops = getattr(module, "OPERATORS", None)
            if not (isinstance(ops, tuple) and all(callable(fn) for fn in ops)):
                raise Refusal(f"operator module {path} has no OPERATORS tuple of functions fn(tree, src, add)")
            operators.extend(ops)
    finally:
        os.close(dir_fd)
    return tuple(operators)


def _oserror(path: str, exc: OSError) -> Refusal:
    return Refusal(f"operator module {path}: [{errno.errorcode.get(exc.errno, exc.errno)}] {exc.strerror}")


def _read_module(dir_fd: int, entry: str, path: str) -> bytes:
    """All bytes of entry in dir_fd, read from one fd that fstat found a regular file."""
    try:
        fd = os.open(entry, MODULE_FLAGS, dir_fd=dir_fd)
    except OSError as exc:
        raise _oserror(path, exc) from exc
    try:
        try:
            kind = stat.S_IFMT(os.fstat(fd).st_mode)
        except OSError as exc:
            raise _oserror(path, exc) from exc
        if kind != stat.S_IFREG:
            raise Refusal(f"operator module {path} is a {KINDS.get(kind, oct(kind))}, not a regular file")
        chunks = []
        try:
            while chunk := os.read(fd, 1 << 20):
                chunks.append(chunk)
        except OSError as exc:
            raise _oserror(path, exc) from exc
    finally:
        try:
            os.close(fd)
        except OSError as exc:
            raise _oserror(path, exc) from exc
    return b"".join(chunks)


class _Source:
    def __init__(self, data: bytes):
        self.data = data
        self.starts = [0]
        for line in data.splitlines(keepends=True):
            self.starts.append(self.starts[-1] + len(line))

    def at(self, line: int, col: int) -> int:  # ast columns are UTF-8 byte offsets
        return self.starts[line - 1] + col

    def span(self, node: ast.AST) -> tuple[int, int]:
        return self.at(node.lineno, node.col_offset), self.at(node.end_lineno, node.end_col_offset)

    def text(self, node: ast.AST) -> bytes:
        a, b = self.span(node)
        return self.data[a:b]

    def splice(self, a: int, b: int, new: bytes) -> bytes:
        return self.data[:a] + new + self.data[b:]


def _os_flag(node: ast.AST) -> str | None:
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "os" \
            and node.attr.startswith("O_"):
        return node.attr
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr" \
            and len(node.args) >= 2 and isinstance(node.args[0], ast.Name) and node.args[0].id == "os" \
            and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str) \
            and node.args[1].value.startswith("O_"):
        return node.args[1].value
    return None


def _is_bitor(node: ast.AST) -> bool:
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)


def _operands(node: ast.AST) -> list[ast.AST]:
    return _operands(node.left) + _operands(node.right) if _is_bitor(node) else [node]


def _quantifiers(pattern: str):
    """(start, end, replacement) for each quantifier with a lower bound above 0."""
    i, n, prev_quant = 0, len(pattern), False
    while i < n:
        c = pattern[i]
        if c == "\\":
            i, prev_quant = i + 2, False
        elif c == "[":
            j = i + 1
            if j < n and pattern[j] == "^":
                j += 1
            if j < n and pattern[j] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                j += 2 if pattern[j] == "\\" else 1
            i, prev_quant = j + 1, False
        elif c in "*?":
            i, prev_quant = i + 1, not prev_quant  # after a quantifier, a lazy/possessive mark
        elif c == "+":
            if not prev_quant:
                yield i, i + 1, "*"
            i, prev_quant = i + 1, not prev_quant
        elif c == "{" and (m := BRACE.match(pattern, i)):
            lo, comma_hi = m.group(1), m.group(2)
            if lo and int(lo) > 0:
                hi = lo if comma_hi is None else comma_hi
                yield i, m.end(), "{0," + hi + "}"
            i, prev_quant = m.end(), True
        else:
            i, prev_quant = i + 1, False


def _write_call(loop: ast.AST) -> ast.Call | None:
    found: list[ast.Call] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            if isinstance(child, ast.Call):
                f = child.func
                name = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
                if name in WRITE_CALLS:
                    found.append(child)
            visit(child)
    visit(loop)
    return min(found, key=lambda c: (c.lineno, c.col_offset)) if found else None


def _plain_else(node: ast.If) -> list[ast.stmt]:
    return [] if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If) else node.orelse
