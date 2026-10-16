#!/usr/bin/env python3
"""Find guards that no test kills: one mutant per guard, run against a scratch lane copy.

  guard_mutants.py --file F [--file F...] --test "CMD" --out NEW.json [--allow ALLOW.json]
                   [--timeout SECONDS]

The lane is the current directory. Each --file is a UTF-8 Python file inside it. `ast`
finds the guards and makes one mutant per guard, each a text splice of one node:

  raise-remove   a `raise` directly in an `if` (or its plain `else`) body becomes `pass`
  flag-drop      one os.O_* flag (or getattr(os, "O_*", ...)) dropped from a `|` chain
                 or from `flags |= os.O_*`
  regex-zero     one quantifier of a re.<fn>() literal pattern widened to lower bound 0
                 (`+` -> `*`, `{n}` -> `{0,n}`, `{n,m}` -> `{0,m}`, `{n,}` -> `{0,}`)
  except-class   an `except` class (or tuple) becomes `Exception`
  except-remove  one `except` clause can never match (NEVER below): removal, kept compilable
  negate-if      an `if` whose body (or plain `else`) has a raise or return gets `not (...)`
  write-loop     a loop that calls write/pwrite/writev becomes its first such call

CMD first runs once on an unmutated copy and must exit 0 (else exit 2, nothing written).
Then each mutant gets a fresh copy of the lane (never the lane itself; the top-level
.git is not copied) under a new temp directory, and CMD runs there with sh: the child
enters the copy through its held fd (fchdir), never by path; PWD and LLMDB_ROOT name
the copy, TMPDIR a directory beside it, and PYTHONPATH is removed. Just before and just
after the run, each of those names must still be the directory held for it (st_dev,
st_ino and F_GETPATH); otherwise the run refuses, nothing is reported and both are kept. Result: killed (CMD exits non-zero), survived (exit 0), or error (the mutant
does not compile, or CMD timed out; never killed). The timeout is --timeout, else
10x the baseline time (at least 60 s); the whole process group is killed.

The lane is the current directory, opened once as "." and held; each directory is entered through its parent's fd and must be the (st_dev,
st_ino) the scan saw; each file is read through an O_NOFOLLOW fd whose fstat matches
the scan before and after the read. Every copy and a final scan must see the same lane
as the first copy (each entry's identity and each file's sha256), and each --file the
same bytes it was parsed from. A special file, a link that is absolute or leaves the
lane, or any change refuses. NEW.json is created
O_EXCL through its parent's fd after the scratch directory is removed; the parent's
real path (F_GETPATH) must lie outside the lane's live path before the run and again
as the last call before the create, and the file fd's real path must be the parent's
live path plus the name, outside the lane, before the first byte and after the write.

Exit 0 when every mutant is killed or listed in ALLOW, exit 1 when one is not, exit 2
on bad invocation or refusal: one line naming the path and errno, no traceback. It never
overwrites and never deletes an input or output; it deletes only the temp directory it
made. That directory is made through the temp parent's fd ($TMPDIR, or tempfile.tempdir
when a caller set it, else /tmp; never tempfile.gettempdir(), which writes a probe file
into its candidates by path), and refused when the parent's or its own real path is the
lane or inside it. It is removed only through fds: each directory is opened through its
parent's fd and its (st_dev, st_ino) must be one recorded when this run made it (never
one taken from the removal's own scan), and its name must still name the held fd just
before rmdir; on a mismatch both are kept.
ALLOW is a JSON list of {"id": <mutant id>, "reason": <non-empty text>}. NEW.json
is a JSON list of rows {id, location ("file:line"), operator, change, result, detail,
allowed (the ALLOW reason or null)}.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import errno
import fcntl
import hashlib
import json
import os
import posixpath
import re
import secrets
import signal
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass

DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
READ_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK  # a FIFO swapped in never blocks
CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
CHUNK = 1 << 20
BASELINE_TIMEOUT = 1800.0
WRITE_CALLS = frozenset({"write", "pwrite", "writev"})
RE_FUNCS = frozenset({"compile", "match", "fullmatch", "search", "findall", "finditer", "sub", "subn", "split"})
NEVER = '__import__("builtins").type("GuardMutantNever", (BaseException,), {})'
BRACE = re.compile(r"\{(\d*)(?:,(\d*))?\}")
SIMPLE = (ast.Name, ast.Attribute, ast.Call, ast.Constant, ast.Subscript)


class Refusal(Exception):
    """Input the tool will not judge; every input stays unchanged."""


# ---- filesystem edge -------------------------------------------------------------

@contextlib.contextmanager
def _fs(path: str):
    """An OSError on a named path is a refusal that names it and its errno."""
    try:
        yield
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        raise Refusal(f"{path}: [{code}] {exc.strerror}") from exc


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def _close(fd: int, path: str) -> None:
    with _fs(path):
        os.close(fd)


def _realpath(fd: int, path: str) -> str:
    with _fs(path):
        buf = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024))
    return os.fsdecode(buf.split(b"\0", 1)[0])


def _inside(root_real: str, path_real: str) -> bool:
    return os.path.commonpath([root_real, path_real]) == root_real


def _temp_parent() -> str:
    return tempfile.tempdir or os.environ.get("TMPDIR") or "/tmp"


def open_root(root: str) -> int:
    with _fs(f"lane {root}"):
        return os.open(root, DIR_FLAGS)


def _read_file(dir_fd: int, name: str, path: str, st: os.stat_result) -> bytes:
    """The bytes of one fd opened without following links, bound to the scan's lstat."""
    with _fs(path):
        fd = os.open(name, READ_FLAGS, dir_fd=dir_fd)
    try:
        with _fs(path):
            if _identity(os.fstat(fd)) != _identity(st):
                raise Refusal(f"{path} changed before it was read")
            parts = []
            while chunk := os.read(fd, CHUNK):
                parts.append(chunk)
            if _identity(os.fstat(fd)) != _identity(st):
                raise Refusal(f"{path} changed while it was read")
    finally:
        _close(fd, path)
    return b"".join(parts)


def _write_all(fd: int, data: bytes, path: str) -> None:
    with _fs(path):
        view = memoryview(data)
        while view:
            view = view[os.write(fd, view):]


def _link_escapes(rel: str, text: str) -> bool:
    if posixpath.isabs(text):
        return True
    target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), text))
    return target == ".." or target.startswith("../")


@dataclass(frozen=True)
class Target:
    rel: str
    data: bytes
    sha256: str


def read_targets(root_fd: int, root: str, files: list[str]) -> dict[str, Target]:
    """Each --file, read through fds from the held root, never through a link."""
    targets: dict[str, Target] = {}
    for given in files:
        full = os.path.normpath(os.path.join(root, given))
        if full == root or not _inside(root, full):
            raise Refusal(f"--file {given!r} is outside the lane {root}")
        if ".." in given.split("/"):
            raise Refusal(f"--file {given!r} has a '..' component")
        rel = os.path.relpath(full, root)
        parts = rel.split("/")
        if parts[0] == ".git":
            raise Refusal(f"--file {given!r} is inside .git")
        if rel in targets:
            raise Refusal(f"--file {rel!r} is named twice")
        held: list[tuple[int, str]] = []
        dir_fd = root_fd
        try:
            for i, name in enumerate(parts[:-1]):
                path = os.path.join(root, *parts[:i + 1])
                with _fs(path):
                    dir_fd = os.open(name, DIR_FLAGS, dir_fd=dir_fd)
                held.append((dir_fd, path))
            with _fs(full):
                st = os.stat(parts[-1], dir_fd=dir_fd, follow_symlinks=False)
            if not stat.S_ISREG(st.st_mode):
                raise Refusal(f"--file {full} is not a regular file")
            data = _read_file(dir_fd, parts[-1], full, st)
        finally:
            for fd, path in reversed(held):
                _close(fd, path)
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Refusal(f"--file {full} is not UTF-8: {exc}") from exc
        targets[rel] = Target(rel, data, hashlib.sha256(data).hexdigest())
    return targets


# ---- mutants ---------------------------------------------------------------------

@dataclass(frozen=True)
class Mutant:
    id: str
    rel: str
    line: int
    operator: str
    change: str
    source: bytes  # the whole mutated file


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


def mutants_for(rel: str, data: bytes) -> list[Mutant]:
    try:
        tree = ast.parse(data, filename=rel)
    except SyntaxError as exc:
        raise Refusal(f"--file {rel} does not parse: {exc}") from exc
    src = _Source(data)
    found: list[tuple] = []

    def add(node, op, tag, change, a, b, new):
        found.append((node.lineno, node.col_offset, op, tag, change, src.splice(a, b, new)))

    inner = {id(side) for n in ast.walk(tree) if _is_bitor(n) for side in (n.left, n.right) if _is_bitor(side)}
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            branches = node.body + _plain_else(node)
            for stmt in branches:
                if isinstance(stmt, ast.Raise):
                    add(stmt, "raise-remove", "", "raise -> pass", *src.span(stmt), b"pass")
            if any(isinstance(s, (ast.Raise, ast.Return)) for s in branches):
                test = src.text(node.test)
                add(node, "negate-if", "", "if X -> if not (X)", *src.span(node.test), b"not (" + test + b")")
        elif (_is_bitor(node) and id(node) not in inner) or \
                (isinstance(node, ast.AugAssign) and isinstance(node.op, ast.BitOr)):
            ops = [node.value] if isinstance(node, ast.AugAssign) else _operands(node)
            for i, operand in enumerate(ops):
                flag = _os_flag(operand)
                if flag is None:
                    continue
                rest = [o for j, o in enumerate(ops) if j != i]
                parts = [src.text(o) if isinstance(o, SIMPLE) else b"(" + src.text(o) + b")" for o in rest]
                new = b"(" + b" | ".join(parts) + b")" if parts else b"0"
                target = node.value if isinstance(node, ast.AugAssign) else node
                add(operand, "flag-drop", flag, f"drop {flag}", *src.span(target), new)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "re" \
                and node.func.attr in RE_FUNCS:
            pat = node.args[0] if node.args else next((k.value for k in node.keywords if k.arg == "pattern"), None)
            if not (isinstance(pat, ast.Constant) and isinstance(pat.value, (str, bytes))):
                continue
            text = pat.value if isinstance(pat.value, str) else pat.value.decode("latin-1")
            for start, end, repl in _quantifiers(text):
                new = text[:start] + repl + text[end:]
                value = new if isinstance(pat.value, str) else new.encode("latin-1")
                add(pat, "regex-zero", str(start), f"{text[start:end]} -> {repl} at {start}",
                    *src.span(pat), repr(value).encode("utf-8"))
        elif isinstance(node, ast.ExceptHandler):
            if node.type is None:
                at = src.at(node.lineno, node.col_offset) + len("except")
                add(node, "except-remove", "", "bare except never matches", at, at, b" " + NEVER.encode())
                continue
            if not (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
                add(node, "except-class", "", f"{src.text(node.type).decode()} -> Exception",
                    *src.span(node.type), b"Exception")
            add(node, "except-remove", "", f"except {src.text(node.type).decode()} never matches",
                *src.span(node.type), NEVER.encode())
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            call = _write_call(node)
            if call is not None:
                add(node, "write-loop", "", "loop -> one call", *src.span(node), src.text(call))

    mutants: list[Mutant] = []
    seen: set[str] = set()
    for line, col, op, tag, change, source in sorted(found, key=lambda f: f[:4]):
        mid = f"{rel}:{line}:{col}:{op}" + (f":{tag}" if tag else "")
        base, k = mid, 1
        while mid in seen:
            k += 1
            mid = f"{base}#{k}"
        seen.add(mid)
        mutants.append(Mutant(mid, rel, line, op, change, source))
    return mutants


# ---- runs ------------------------------------------------------------------------

class Session:
    """A scratch directory of lane copies; each copy is checked against the first one."""

    def __init__(self, root: str, root_fd: int, targets: dict[str, Target], cmd: str, timeout: float | None):
        self.root, self.root_fd, self.targets, self.cmd = root, root_fd, targets, cmd
        self.timeout = timeout
        self.snapshot: dict | None = None
        self.runs = 0
        self.keep = False  # a removal found a directory this run did not make: remove nothing more
        self.owned: set[tuple[int, int]] = set()  # (st_dev, st_ino) of each directory made, taken at its creation

    def __enter__(self) -> Session:
        parent = _temp_parent()
        with _fs(f"scratch parent {parent}"):
            self.parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            parent_real = _realpath(self.parent_fd, f"scratch parent {parent}")
            if _inside(_realpath(self.root_fd, f"lane {self.root}"), parent_real):
                raise Refusal(f"scratch parent {parent_real} is inside the lane {self.root}; set TMPDIR outside it")
            self.name = "guard_mutants-" + secrets.token_hex(8)
            self.scratch = os.path.join(parent_real, self.name)
            self.scratch_fd = self._made(self.parent_fd, self.name, f"scratch {self.scratch}", 0o700)
            try:
                self.scratch = _realpath(self.scratch_fd, f"scratch {self.scratch}")
                if _inside(_realpath(self.root_fd, f"lane {self.root}"), self.scratch):
                    raise Refusal(f"scratch {self.scratch} is inside the lane {self.root}; it was kept")
            except BaseException:
                _close(self.scratch_fd, f"scratch {self.scratch}")
                raise
        except BaseException:
            _close(self.parent_fd, f"scratch parent {parent}")
            raise
        return self

    def __exit__(self, *exc) -> None:
        try:
            _close(self.scratch_fd, f"scratch {self.scratch}")
            if not self.keep:
                _remove_dir(self.parent_fd, self.name, self.scratch, self.owned)
        finally:
            _close(self.parent_fd, f"scratch parent of {self.scratch}")

    def baseline(self) -> None:
        start = time.monotonic()
        result, detail = self._run(None, self.timeout or BASELINE_TIMEOUT)
        if result != "survived":
            raise Refusal(f"the test does not pass on the unmutated lane copy ({detail}); nothing was judged")
        if self.timeout is None:
            self.timeout = max(60.0, 10 * (time.monotonic() - start))

    def result(self, m: Mutant) -> tuple[str, str]:
        try:
            compile(m.source, m.rel, "exec", dont_inherit=True)
        except (SyntaxError, ValueError) as exc:
            return "error", f"does not compile: {exc}"
        return self._run(m, self.timeout)

    def verify_lane(self) -> None:
        seen: dict = {}
        self._walk(self.root_fd, self.root, "", None, "", seen, {})
        self._compare(seen)

    def _compare(self, seen: dict) -> None:
        for rel in sorted(set(seen) | set(self.snapshot)):
            if seen.get(rel) != self.snapshot.get(rel):
                raise Refusal(f"the lane changed during the run at {os.path.join(self.root, rel)}; nothing is reported")

    def _made(self, parent_fd: int, name: str, path: str, mode: int) -> int:
        """Make and open directory name in parent_fd; its identity, taken here, is what cleanup may remove."""
        with _fs(path):
            os.mkdir(name, mode, dir_fd=parent_fd)
        with _fs(path):
            fd = os.open(name, DIR_FLAGS, dir_fd=parent_fd)
        try:
            with _fs(path):
                st = os.fstat(fd)
        except BaseException:
            _close(fd, path)
            raise
        self.owned.add((st.st_dev, st.st_ino))
        return fd

    def _check_bound(self, bound: tuple, when: str) -> None:
        """Each (parent_fd, name, fd, path): name in parent_fd is still fd's directory, and fd lives at path."""
        for parent_fd, name, fd, path in bound:
            with _fs(path):
                now = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            with _fs(path):
                held = os.fstat(fd)
            if (now.st_dev, now.st_ino) != (held.st_dev, held.st_ino) or _realpath(fd, path) != path:
                self.keep = True
                raise Refusal(f"{path} no longer names the directory this run made (checked {when} the test run); "
                              "nothing is reported and both were kept")

    def _run(self, m: Mutant | None, timeout: float) -> tuple[str, str]:
        self.runs += 1
        name = f"m{self.runs:04d}"
        mpath = os.path.join(self.scratch, name)
        lane, tmp = os.path.join(mpath, "lane"), os.path.join(mpath, "tmp")
        mfd = self._made(self.scratch_fd, name, mpath, 0o700)
        try:
            with contextlib.ExitStack() as held:
                held.callback(_close, mfd, mpath)
                lfd = self._made(mfd, "lane", lane, 0o755)
                held.callback(_close, lfd, lane)
                tfd = self._made(mfd, "tmp", tmp, 0o700)
                held.callback(_close, tfd, tmp)
                seen: dict = {}
                self._walk(self.root_fd, self.root, "", lfd, lane, seen, {m.rel: m.source} if m else {})
                if self.snapshot is None:
                    self.snapshot = seen
                self._compare(seen)
                bound = ((self.scratch_fd, name, mfd, mpath), (mfd, "lane", lfd, lane), (mfd, "tmp", tfd, tmp))
                self._check_bound(bound, "before")
                outcome = _execute(self.cmd, lane, tmp, timeout, lfd)
                self._check_bound(bound, "after")
                return outcome
        finally:
            if not self.keep:
                try:
                    _remove_dir(self.scratch_fd, name, mpath, self.owned)
                except Refusal:
                    self.keep = True
                    raise

    def _walk(self, src_fd, src, rel, dst_fd, dst, seen, replace) -> None:
        """Copy (or with dst_fd None, only scan) one lane directory through fds."""
        with _fs(src), os.scandir(src_fd) as it:
            entries = sorted(it, key=lambda e: e.name)
        for entry in entries:
            name = entry.name
            if not rel and name == ".git":
                continue
            r, spath, dpath = rel + name, os.path.join(src, name), os.path.join(dst, name)
            with _fs(spath):
                st = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(st.st_mode):
                with _fs(spath):
                    fd = os.open(name, DIR_FLAGS, dir_fd=src_fd)
                try:
                    with _fs(spath):
                        opened = os.fstat(fd)
                    if (opened.st_dev, opened.st_ino) != (st.st_dev, st.st_ino):
                        raise Refusal(f"{spath} changed during the walk")
                    seen[r] = ("dir", st.st_dev, st.st_ino)
                    sub = None
                    if dst_fd is not None:
                        sub = self._made(dst_fd, name, dpath, 0o755)
                    try:
                        self._walk(fd, spath, r + "/", sub, dpath, seen, replace)
                    finally:
                        if sub is not None:
                            _close(sub, dpath)
                finally:
                    _close(fd, spath)
            elif stat.S_ISLNK(st.st_mode):
                with _fs(spath):
                    text = os.readlink(name, dir_fd=src_fd)
                if _link_escapes(r, text):
                    raise Refusal(f"link {spath} -> {text!r} is absolute or leaves the lane")
                seen[r] = ("link", text) + _identity(st)
                if dst_fd is not None:
                    with _fs(dpath):
                        os.symlink(text, name, dir_fd=dst_fd)
            elif stat.S_ISREG(st.st_mode):
                data = _read_file(src_fd, name, spath, st)
                digest = hashlib.sha256(data).hexdigest()
                if r in self.targets and digest != self.targets[r].sha256:
                    raise Refusal(f"{spath} changed since it was parsed")
                seen[r] = ("file",) + _identity(st) + (digest,)
                if dst_fd is None:
                    continue
                with _fs(dpath):
                    out = os.open(name, CREATE_FLAGS, stat.S_IMODE(st.st_mode) & 0o777, dir_fd=dst_fd)
                try:
                    _write_all(out, replace.get(r, data), dpath)
                finally:
                    _close(out, dpath)
            else:
                raise Refusal(f"{spath} is a special file")


def _remove_dir(parent_fd: int, name: str, path: str, owned: set) -> None:
    """Remove a directory this run made, only through fds bound to it.

    owned holds the (st_dev, st_ino) of each directory this run made, recorded when it made it;
    a directory (or child directory) not in it is never removed, and the removal refuses."""
    with _fs(path):
        fd = os.open(name, DIR_FLAGS, dir_fd=parent_fd)
    try:
        with _fs(path):
            held = os.fstat(fd)
        made = (held.st_dev, held.st_ino)
        if made not in owned:
            raise Refusal(f"{path} is not a directory this run made; both were kept")
        with _fs(path), os.scandir(fd) as it:
            entries = list(it)
        for entry in entries:
            epath = os.path.join(path, entry.name)
            with _fs(epath):
                st = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(st.st_mode):
                _remove_dir(fd, entry.name, epath, owned)
            else:
                with _fs(epath):
                    os.unlink(entry.name, dir_fd=fd)
        with _fs(path):
            now = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if (now.st_dev, now.st_ino) != made:
            raise Refusal(f"{path} now names another directory; both were kept")
        with _fs(path):
            os.rmdir(name, dir_fd=parent_fd)
        owned.discard(made)
    finally:
        _close(fd, path)


def _execute(cmd: str, lane: str, tmp: str, timeout: float, cwd_fd: int | None = None) -> tuple[str, str]:
    """Run cmd with sh in the copy held by cwd_fd: the child enters it with fchdir, never by path.

    Without cwd_fd the child fails before exec (fchdir(None)); lane and tmp only name the copy in the env."""
    env = dict(os.environ, PWD=lane, LLMDB_ROOT=lane, TMPDIR=tmp)
    env.pop("PYTHONPATH", None)
    proc = subprocess.Popen(["/bin/sh", "-c", cmd], preexec_fn=lambda: os.fchdir(cwd_fd), env=env,
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_group(proc.pid)
        proc.wait()
        return "error", f"timeout after {timeout:g}s"
    _kill_group(proc.pid)  # anything the test left running
    return ("survived", "exit 0") if code == 0 else ("killed", f"exit {code}")


def _kill_group(pgid: int) -> None:
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # the group is already gone


# ---- inputs and output -----------------------------------------------------------

def load_allow(path: str, ids: set[str]) -> dict[str, str]:
    with _fs(f"--allow {path}"):
        fd = os.open(path, READ_FLAGS)
    try:
        with _fs(f"--allow {path}"):
            st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Refusal(f"--allow {path} is not a regular file")
        parts = []
        with _fs(f"--allow {path}"):
            while chunk := os.read(fd, CHUNK):
                parts.append(chunk)
    finally:
        _close(fd, f"--allow {path}")
    try:
        doc = json.loads(b"".join(parts).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"--allow {path} is not UTF-8 JSON: {exc}") from exc
    if not isinstance(doc, list):
        raise Refusal(f"--allow {path} is not a JSON list")
    allow: dict[str, str] = {}
    for item in doc:
        if not isinstance(item, dict) or set(item) != {"id", "reason"}:
            raise Refusal(f"--allow {path}: each item must be exactly {{id, reason}}: {item!r}")
        mid, reason = item["id"], item["reason"]
        if not isinstance(mid, str) or not isinstance(reason, str) or not reason.strip():
            raise Refusal(f"--allow {path}: id and a non-empty reason must be text: {item!r}")
        if mid in allow:
            raise Refusal(f"--allow {path} lists {mid} twice")
        if mid not in ids:
            raise Refusal(f"--allow {path} lists {mid}, which is no mutant of these files")
        allow[mid] = reason
    return allow


def _positive(text: str) -> float:
    value = float(text)  # argparse turns a ValueError into a usage error (exit 2)
    if not value > 0:
        raise argparse.ArgumentTypeError(f"must be above 0: {text!r}")
    return value


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", action="append", required=True, help="a Python file in the lane (cwd)")
    ap.add_argument("--test", required=True, help="the test command, run with sh in each lane copy")
    ap.add_argument("--out", required=True, help="a new JSON file outside the lane")
    ap.add_argument("--allow", help="JSON list of {id, reason} for mutants that may stay unkilled")
    ap.add_argument("--timeout", type=_positive, help="seconds per test run (default 10x baseline, >= 60)")
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out)
    parent, name = os.path.dirname(out), os.path.basename(args.out)
    kept = ""
    try:
        if name in ("", ".", ".."):
            raise Refusal(f"--out {args.out} names no file")
        root = "(the current directory)"
        root_fd = open_root(os.curdir)
        try:
            root = _realpath(root_fd, f"lane {root}")
            targets = read_targets(root_fd, root, args.file)
            mutants = [m for t in targets.values() for m in mutants_for(t.rel, t.data)]
            allow = load_allow(args.allow, {m.id for m in mutants}) if args.allow else {}
            with _fs(f"--out parent {parent}"):
                parent_fd = os.open(parent, DIR_FLAGS)
            try:
                if _inside(_realpath(root_fd, f"lane {root}"), _realpath(parent_fd, f"--out parent {parent}")):
                    raise Refusal(f"--out {out} is inside the lane")
                with _fs(out):
                    try:
                        os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                        raise Refusal(f"--out {out} already exists")
                    except FileNotFoundError:
                        pass  # the expected state: the output is new
                with Session(root, root_fd, targets, args.test, args.timeout) as session:
                    session.baseline()
                    rows = []
                    for m in mutants:
                        result, detail = session.result(m)
                        rows.append({"id": m.id, "location": f"{m.rel}:{m.line}", "operator": m.operator,
                                     "change": m.change, "result": result, "detail": detail,
                                     "allowed": allow.get(m.id) if result != "killed" else None})
                    session.verify_lane()
                # The scratch directory is gone before the output exists, so its cleanup never reaches it.
                body = (json.dumps(rows, indent=1, sort_keys=True) + "\n").encode("utf-8")
                lane_real = _realpath(root_fd, f"lane {root}")
                if _inside(lane_real, _realpath(parent_fd, f"--out parent {parent}")):
                    raise Refusal(f"--out {out} is now inside the lane; nothing was created")
                with _fs(out):  # no call between the parent's check above and this create
                    out_fd = os.open(name, CREATE_FLAGS, 0o644, dir_fd=parent_fd)
                kept = f" ({out} was created and left in place)"

                def placed(verb: str) -> None:
                    real = _realpath(out_fd, f"{out}{kept}")
                    expected = os.path.join(_realpath(parent_fd, f"--out parent {parent}{kept}"), name)
                    if real != expected:
                        raise Refusal(f"{verb} {real}, not {expected}; it was left in place")
                    if _inside(_realpath(root_fd, f"lane {root}{kept}"), real):
                        raise Refusal(f"{verb} {real}, which is now inside the lane; it was left in place")
                try:
                    placed("created")  # before the first byte: a move at the create writes nothing inside
                    _write_all(out_fd, body, f"{out} (left in place, incomplete)")
                    placed("wrote")
                finally:
                    _close(out_fd, f"{out} (written, left in place)")
            finally:
                _close(parent_fd, f"--out parent {parent}{kept}")
        finally:
            _close(root_fd, f"lane {root}{kept}")
    except Refusal as exc:
        print("guard_mutants: refused: " + str(exc).replace("\n", "\\n"), file=sys.stderr)
        return 2
    open_rows = [r for r in rows if r["result"] != "killed" and r["allowed"] is None]
    for r in rows:
        if r["result"] != "killed":
            note = f" (allowed: {r['allowed']})" if r["allowed"] is not None else ""
            print(f"{r['result']} {r['id']}: {r['change']} [{r['detail']}]{note}")
    counts = {k: sum(r["result"] == k for r in rows) for k in ("killed", "survived", "error")}
    print(f"guard_mutants: {len(rows)} mutants, {counts['killed']} killed, {counts['survived']} survived, "
          f"{counts['error']} error, {len(rows) - counts['killed'] - len(open_rows)} allowed; wrote {out}")
    return 1 if open_rows else 0


if __name__ == "__main__":
    sys.exit(main())
