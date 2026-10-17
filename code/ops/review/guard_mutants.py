#!/usr/bin/env python3
"""Find guards that no test kills: one mutant per guard, run against a scratch lane copy.

  guard_mutants.py --file F [--file F...] --test "CMD" --out NEW.json [--allow ALLOW.json]
                   [--timeout SECONDS] [--base REV]

The lane is the current directory. Each --file is a UTF-8 Python file inside it. `ast`
finds the guards and makes one mutant per guard, each a text splice of one node:

  raise-remove   a `raise` directly in an `if` (or its plain `else`) body becomes `pass`
  flag-drop      one os.O_* flag (or getattr(os, "O_*", ...)) dropped from a `|` chain
                 or from `flags |= os.O_*`
  regex-zero     one quantifier of a re.<fn>() literal pattern widened to lower bound 0
                 (`+` -> `*`, `{n}` -> `{0,n}`, `{n,m}` -> `{0,m}`, `{n,}` -> `{0,}`)
  except-class   an `except` class (or tuple) becomes `Exception`
  except-remove  one `except` clause can never match (mutant_ops.NEVER): removal, kept compilable
  negate-if      an `if` whose body (or plain `else`) has a raise or return gets `not (...)`
  write-loop     a loop that calls write/pwrite/writev becomes its first such call

These operators live in mutant_ops/base.py. Every module of mutant_ops/ not named _* is loaded in
sorted name order (its contract: mutant_ops/__init__.py); a module that fails to import or has no
OPERATORS, and a mutant whose source does not parse (named by operator and id), refuse (exit 2).

With --base REV only the lines of each --file that differ from REV are in scope, and a mutant
is made only when its anchor line (the line in its id and location) is in scope. git is
asked once per file in the lane, before any copy, with no GIT_* variable of the caller and
literal pathspecs: REV must resolve to a commit (git rev-parse); a file absent at REV (git
cat-file -e fails) is in scope as a whole; otherwise its index entry must be plain (git
ls-files -v gives "H": not skip-worktree, assume-unchanged, unmerged or untracked, which
git diff would not compare), and its lines are the new-side lines of each hunk of
`git diff -U0 --no-color --no-ext-diff REV -- F` (the worktree against REV). A git command
that fails, a binary diff, or an unreadable hunk header refuses (exit 2). Without --base
every line is in scope.

CMD first runs once on an unmutated copy and must exit 0 (else exit 2, nothing written).
Then each mutant gets a fresh copy of the lane (never the lane itself; the top-level
.git is not copied) under a new temp directory. Each create in a copy (directory, file,
link) is made through its parent's held fd, and immediately before it that fd's live path
(F_GETPATH) must be the path recorded when this run made it, outside the lane; each new
directory's and file's fd must live at its own path outside the lane (a file before each
write and after its last byte). A new directory must be empty and be the one its name gives
(lstat) right after it is opened, and a new link must be the link written, before either is
taken as made. A copy is built as mNNNN/copy and renamed to mNNNN/lane
(never over an existing entry) once it is complete. Any mismatch, or a failed create in a
directory that moved, refuses and keeps everything. CMD runs in the copy with sh: the child
enters the copy through its held fd (fchdir), never by path; PWD and LLMDB_ROOT name
the copy, TMPDIR a directory beside it, and PYTHONPATH is removed. Just before and just
after the run, each of those names must still be the directory held for it (st_dev,
st_ino and F_GETPATH); otherwise the run refuses, nothing is reported and both are kept.
After the run, each file or link in mNNNN that this run did not make must have been born
during the test run (the test's own); it is then removed with the copy. Any other entry this
run did not make (a directory, or anything older) refuses and is kept. Result: killed (CMD exits non-zero), survived (exit 0), or error (the mutant
does not compile, or CMD timed out; never killed). The timeout is --timeout, else
10x the baseline time (at least 60 s); the whole process group is killed.

The lane is the current directory, opened once as "." and held; each directory is entered through its parent's fd and must be the (st_dev,
st_ino) the scan saw; each file is read through an O_NOFOLLOW fd whose fstat matches
the scan before and after the read. Before each scandir, stat, open, readlink and read
through a source fd, that fd's live path must be inside the lane's live path, else nothing
more is read. The lane is walked once before any copy, and then
each link is resolved one component at a time from its directory through that walk's
record: an absolute target, a component that is a link or names nothing recorded, or a
'..' above the lane root refuses. Every copy and a final scan must see the same lane as
that first walk (each entry's identity and each file's sha256), and each --file the
same bytes it was parsed from. A special file or any change refuses. NEW.json is created
O_EXCL through its parent's fd after the scratch directory is removed; the parent's
real path (F_GETPATH) must lie outside the lane's live path before the run and again
as the last call before the create, and the file fd's real path must be the parent's
live path plus the name, outside the lane, before each write and after the last.

Exit 0 when every mutant is killed or listed in ALLOW, exit 1 when one is not, exit 2
on bad invocation or refusal: one line naming the path and errno, no traceback. It never
overwrites and never deletes an input or output; it deletes only the temp directory it
made. That directory is made through the temp parent's fd ($TMPDIR, or tempfile.tempdir
when a caller set it, else /tmp; never tempfile.gettempdir(), which writes a probe file
into its candidates by path), and refused when the parent's or its own real path is the
lane or inside it. It is removed only through fds: each entry's (st_dev, st_ino) must be
one recorded when this run (or its test run) made it (never one taken from the removal's
own scan), each directory is opened through its parent's fd, its name must still name the held fd just
before rmdir, and each unlink and rmdir happens only while the directory it acts in
still lives at its recorded path; on a mismatch both are kept.
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
import select
import shlex
import signal
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass

from mutant_ops import NEVER, OPS_DIR, Refusal, _Source, load_operators  # noqa: F401  (NEVER: the tests read gm.NEVER)

DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
READ_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK  # a FIFO swapped in never blocks
CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
CHUNK = 1 << 20
BASELINE_TIMEOUT = 1800.0
STAGE = "copy"  # a copy's name in its mNNNN until it is complete; then it is renamed to "lane"
HUNK = re.compile(rb"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


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


def _in_lane(root_fd: int, root: str, fd: int, path: str) -> None:
    """The source fd still lives inside the lane's live path; else nothing more is read through it.

    The fd's F_GETPATH is the last call here, so the read that follows has no call before it."""
    lane = _realpath(root_fd, f"lane {root}")
    live = _realpath(fd, path)
    if not _inside(lane, live):
        raise Refusal(f"{path} is now at {live}, outside the lane {lane}; nothing more was read from it "
                      "and nothing is reported")


def _read_file(root_fd: int, root: str, dir_fd: int, name: str, path: str, st: os.stat_result) -> bytes:
    """The bytes of one fd opened without following links, bound to the scan's lstat.

    The directory fd (before the open) and the file fd (before each read and after the last) must be
    inside the lane."""
    _in_lane(root_fd, root, dir_fd, os.path.dirname(path))
    with _fs(path):
        fd = os.open(name, READ_FLAGS, dir_fd=dir_fd)
    try:
        with _fs(path):
            if _identity(os.fstat(fd)) != _identity(st):
                raise Refusal(f"{path} changed before it was read")
        parts = []
        while True:
            _in_lane(root_fd, root, fd, path)
            with _fs(path):
                chunk = os.read(fd, CHUNK)
            if not chunk:
                break
            parts.append(chunk)
        with _fs(path):
            if _identity(os.fstat(fd)) != _identity(st):
                raise Refusal(f"{path} changed while it was read")
        _in_lane(root_fd, root, fd, path)  # after the last read too: a move just before it is seen
    finally:
        _close(fd, path)
    return b"".join(parts)


class _Dest(str):
    """A written file's path (its text names it in messages) and the check its fd must pass before each write."""

    def __new__(cls, path: str, check):
        dest = super().__new__(cls, path)
        dest.check = check
        return dest


def _write_all(fd: int, data: bytes, path: _Dest) -> None:
    """Every byte, through short writes; path.check() is the last call before each os.write."""
    view = memoryview(data)
    while view:
        path.check()
        with _fs(path):
            view = view[os.write(fd, view):]


def _link_leaves(rel: str, text: str, record: dict) -> str | None:
    """Why the link at rel (its text) may not resolve inside the lane, or None.

    The target is resolved one component at a time from the link's directory, through the
    walk's record (rel -> (kind, ...)): no component may be a link, or a name the walk did not
    record; only the last may be a non-directory; and no '..' may climb above the lane root."""
    if posixpath.isabs(text):
        return "is absolute"
    at = rel.split("/")[:-1]  # every element is a directory the walk recorded, never a link
    parts = [c for c in text.split("/") if c not in ("", ".")]
    for i, part in enumerate(parts):
        if part == "..":
            if not at:
                return "climbs above the lane root"
            at.pop()
            continue
        here = "/".join(at + [part])
        kind = record.get(here, ("missing",))[0]
        if kind == "link":
            return f"goes through the link {here}"
        if kind == "missing":
            return f"names {here}, which the walk did not record"
        if kind != "dir" and i < len(parts) - 1:
            return f"goes through {here}, which is not a directory"
        at.append(part)
    return None


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
        dir_fd, dir_path = root_fd, root
        try:
            for i, name in enumerate(parts[:-1]):
                path = os.path.join(root, *parts[:i + 1])
                _in_lane(root_fd, root, dir_fd, dir_path)
                with _fs(path):
                    dir_fd = os.open(name, DIR_FLAGS, dir_fd=dir_fd)
                held.append((dir_fd, path))
                dir_path = path
            _in_lane(root_fd, root, dir_fd, dir_path)
            with _fs(full):
                st = os.stat(parts[-1], dir_fd=dir_fd, follow_symlinks=False)
            if not stat.S_ISREG(st.st_mode):
                raise Refusal(f"--file {full} is not a regular file")
            data = _read_file(root_fd, root, dir_fd, parts[-1], full, st)
        finally:
            for fd, path in reversed(held):
                _close(fd, path)
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Refusal(f"--file {full} is not UTF-8: {exc}") from exc
        targets[rel] = Target(rel, data, hashlib.sha256(data).hexdigest())
    return targets


# ---- scope -----------------------------------------------------------------------

class _Whole:
    """The scope of a file mutated as a whole: every line is in it."""

    def __contains__(self, line: object) -> bool:
        return True

    def __repr__(self) -> str:
        return "WHOLE"


WHOLE = _Whole()


def _git(*args: str) -> subprocess.CompletedProcess:
    """Run git in the lane (cwd) without the caller's GIT_* (a hook's GIT_DIR names another repo)."""
    cmd = ["git", *args]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_LITERAL_PATHSPECS"] = "1"  # a file name is a path, never a glob or magic pathspec
    try:
        return subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, capture_output=True)
    except OSError as exc:
        raise Refusal(f"`{shlex.join(cmd)}` did not run: {exc}") from exc


def _git_ok(*args: str) -> bytes:
    """git's stdout; a non-zero exit is a refusal that names the command and its stderr."""
    proc = _git(*args)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        raise Refusal(f"`{shlex.join(proc.args)}` failed (exit {proc.returncode}): {err}")
    return proc.stdout


def _changed_lines(rev: str, rel: str):
    """The lines of rel (relative to the lane) that differ from commit rev, or WHOLE when rel is absent there."""
    if _git("cat-file", "-e", f"{rev}:./{rel}").returncode != 0:
        return WHOLE
    entries = _git_ok("ls-files", "-v", "-z", "--", rel).split(b"\0")
    if entries != [b"H " + os.fsencode(rel), b""]:
        raise Refusal(f"`git ls-files -v -z -- {rel}` gives {entries[:-1]!r}, not one plain index entry; "
                      "git diff would not compare its worktree bytes")
    lines: set[int] = set()
    for raw in _git_ok("diff", "-U0", "--no-color", "--no-ext-diff", rev, "--", rel).split(b"\n"):
        if raw.startswith(b"Binary files "):
            raise Refusal(f"`git diff {rev} -- {rel}` shows a binary diff; no changed line is known")
        if raw.startswith(b"@@"):
            m = HUNK.match(raw)
            if m is None:
                raise Refusal(f"`git diff {rev} -- {rel}` has a hunk header it cannot read: {raw!r}")
            start, count = int(m[1]), 1 if m[2] is None else int(m[2])
            lines.update(range(start, start + count))  # count 0 (a pure deletion) adds no line
    return frozenset(lines)


def line_scope(base: str | None, rels) -> dict:
    """Each file's scope: the lines that differ from base (asked of git once, in the lane), else WHOLE."""
    if base is None:
        return dict.fromkeys(rels, WHOLE)
    rev = _git_ok("rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode("ascii").strip()
    return {rel: _changed_lines(rev, rel) for rel in rels}


# ---- mutants ---------------------------------------------------------------------

@dataclass(frozen=True)
class Mutant:
    id: str
    rel: str
    line: int
    operator: str
    change: str
    source: bytes  # the whole mutated file


def mutants_for(rel: str, data: bytes, lines=WHOLE, operators=None) -> list[Mutant]:
    """One mutant per guard whose anchor line (node.lineno) is in lines, from operators (default: the
    mutant_ops package's). Ids are given after every operator ran, so module order cannot change one."""
    try:
        tree = ast.parse(data, filename=rel)
    except SyntaxError as exc:
        raise Refusal(f"--file {rel} does not parse: {exc}") from exc
    src = _Source(data)
    found: list[tuple] = []

    def add(node, op, tag, change, a, b, new):
        if node.lineno in lines:
            found.append((node.lineno, node.col_offset, op, tag, change, src.splice(a, b, new)))

    for fn in load_operators() if operators is None else operators:
        fn(tree, src, add)

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


def parsed(mutants: list[Mutant]) -> list[Mutant]:
    """mutants, once each one's source parses; one that does not refuses, naming its operator and id."""
    for m in mutants:
        try:
            ast.parse(m.source, filename=m.rel)
        except Exception as exc:  # any failure to parse a mutant is a refusal
            raise Refusal(f"operator {m.operator} made {m.id}, whose source does not parse: {exc}") from exc
    return mutants


# ---- runs ------------------------------------------------------------------------

class Session:
    """A scratch directory of lane copies; each copy is checked against the first one."""

    def __init__(self, root: str, root_fd: int, targets: dict[str, Target], cmd: str, timeout: float | None):
        self.root, self.root_fd, self.targets, self.cmd = root, root_fd, targets, cmd
        self.timeout = timeout
        self.snapshot: dict | None = None
        self.runs = 0
        self.keep = False  # a removal found an entry this run did not make: remove nothing more
        # (st_dev, st_ino) of each entry this run made (directory, file, link), taken at its creation, and of
        # each file or link its test run made (born during that run); cleanup removes nothing else.
        self.owned: set[tuple[int, int]] = set()

    def __enter__(self) -> Session:
        parent = _temp_parent()
        with _fs(f"scratch parent {parent}"):
            self.parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            lane_real = _realpath(self.root_fd, f"lane {self.root}")
            parent_real = _realpath(self.parent_fd, f"scratch parent {parent}")
            if _inside(lane_real, parent_real):
                raise Refusal(f"scratch parent {parent_real} is inside the lane {self.root}; set TMPDIR outside it")
            self.name = "guard_mutants-" + secrets.token_hex(8)
            self.scratch = os.path.join(parent_real, self.name)
            self.scratch_fd = self._made(self.parent_fd, parent_real, self.name, 0o700, "scratch", "scratch parent")
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

    def _check_at(self, fd: int, path: str, what: str, child: str = "") -> None:
        """fd lives at path, the path recorded when this run made it, outside the lane; else keep all, refuse.

        The fd's F_GETPATH is the last call here, so a create may follow with no call between."""
        try:
            lane = _realpath(self.root_fd, f"lane {self.root}")
            live = _realpath(fd, os.path.join(path, child) if child else path)
        except Refusal:
            self.keep = True
            raise
        if live == path and not _inside(lane, live):
            return
        self.keep = True
        shown = os.path.join(live, child) if child else live
        if _inside(lane, live):
            raise Refusal(f"{what} {shown} is inside the lane {self.root}; it was kept and nothing is reported")
        expected = os.path.join(path, child) if child else path
        raise Refusal(f"{what} {expected} is now at {shown}; it was kept and nothing is reported")

    def _create(self, parent_fd: int, parent_path: str, path: str, make, what: str = "copy directory"):
        """make() creates path's last name in parent_fd, checked at its recorded place immediately before.

        A create that fails is checked again: a failure in a directory that moved keeps everything."""
        self._check_at(parent_fd, parent_path, what)
        try:
            with _fs(path):
                return make()  # no call between the check above and this create
        except Refusal:
            self._check_at(parent_fd, parent_path, what)
            raise

    def _made(self, parent_fd: int, parent_path: str, name: str, mode: int,
              what: str = "copy directory", parent_what: str = "copy directory") -> int:
        """Make and open directory name in parent_fd; its identity, taken here, is what cleanup may remove.

        Right after the open, the directory must be empty and be the one the name gives (lstat); otherwise
        it is not taken as made, and it is kept. Its path is recorded as parent_path/name, and the new fd
        must live there, outside the lane."""
        path = os.path.join(parent_path, name)
        self._create(parent_fd, parent_path, path, lambda: os.mkdir(name, mode, dir_fd=parent_fd), parent_what)
        with _fs(path):
            fd = os.open(name, DIR_FLAGS, dir_fd=parent_fd)
        try:
            try:
                with _fs(path):
                    st = os.fstat(fd)
                    now = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                    empty = not os.listdir(fd)  # readdir of a dup of fd (os.scandir is the removal's call)
                if (now.st_dev, now.st_ino) != (st.st_dev, st.st_ino) or not empty:
                    raise Refusal(f"{path} is not the empty directory this run just made; it was kept "
                                  "and nothing is reported")
            except Refusal:
                self.keep = True
                raise
            self.owned.add((st.st_dev, st.st_ino))
            self._check_at(fd, path, what)
        except BaseException:
            _close(fd, path)
            raise
        return fd

    def _publish(self, mfd: int, mpath: str) -> None:
        """Give the finished copy the name the test runs under: STAGE becomes lane, inside mfd."""
        lane = os.path.join(mpath, "lane")
        try:
            with _fs(lane):
                try:
                    os.stat("lane", dir_fd=mfd, follow_symlinks=False)
                    raise Refusal(f"{lane} exists before the copy was given that name; it was kept")
                except FileNotFoundError:
                    pass  # the expected state: a rename never replaces an entry
        except Refusal:
            self.keep = True
            raise
        self._check_at(mfd, mpath, "copy directory")
        with _fs(lane):  # no call between the check above and this rename
            os.rename(STAGE, "lane", src_dir_fd=mfd, dst_dir_fd=mfd)

    def _check_bound(self, bound: tuple, when: str) -> None:
        """Each (parent_fd, name, fd, path): name in parent_fd is still fd's directory, and fd lives at path.

        Any error here (the name gone, say) keeps everything, as a mismatch does."""
        try:
            for parent_fd, name, fd, path in bound:
                with _fs(path):
                    now = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                with _fs(path):
                    held = os.fstat(fd)
                if (now.st_dev, now.st_ino) != (held.st_dev, held.st_ino) or _realpath(fd, path) != path:
                    raise Refusal(f"{path} no longer names the directory this run made (checked {when} the test "
                                  "run); nothing is reported and both were kept")
        except Refusal:
            self.keep = True
            raise

    def _scan(self) -> dict:
        """The whole lane walked first; then each link resolved against what the walk recorded."""
        seen: dict = {}
        self._walk(self.root_fd, self.root, "", None, "", seen, {})
        for rel, record in sorted(seen.items()):
            if record[0] == "link":
                why = _link_leaves(rel, record[1], seen)
                if why is not None:
                    raise Refusal(f"link {os.path.join(self.root, rel)} -> {record[1]!r} {why}; nothing was judged")
        for rel, target in sorted(self.targets.items()):  # each mutant is placed only where the walk finds it
            record = seen.get(rel, ("missing",))
            if record[0] != "file" or record[-1] != target.sha256:
                raise Refusal(f"--file {os.path.join(self.root, rel)} is not in the lane as it was parsed; "
                              "nothing was judged")
        return seen

    def _run(self, m: Mutant | None, timeout: float) -> tuple[str, str]:
        if self.snapshot is None:
            self.snapshot = self._scan()  # before any copy or test run
        self.runs += 1
        name = f"m{self.runs:04d}"
        mpath = os.path.join(self.scratch, name)
        lane, stage, tmp = (os.path.join(mpath, n) for n in ("lane", STAGE, "tmp"))
        mfd = self._made(self.scratch_fd, self.scratch, name, 0o700)
        try:
            with contextlib.ExitStack() as held:
                held.callback(_close, mfd, mpath)
                lfd = self._made(mfd, mpath, STAGE, 0o755)
                held.callback(_close, lfd, lane)
                tfd = self._made(mfd, mpath, "tmp", 0o700)
                held.callback(_close, tfd, tmp)
                seen: dict = {}
                self._walk(self.root_fd, self.root, "", lfd, stage, seen, {m.rel: m.source} if m else {})
                self._compare(seen)
                self._publish(mfd, mpath)
                bound = ((self.scratch_fd, name, mfd, mpath), (mfd, "lane", lfd, lane), (mfd, "tmp", tfd, tmp))
                self._check_bound(bound, "before")
                start = time.time()
                outcome = _execute(self.cmd, lane, tmp, timeout, lfd)
                window = (start, time.time())
                self._check_bound(bound, "after")
                try:
                    self._record_run(mfd, mpath, window)
                except Refusal:
                    self.keep = True
                    raise
                return outcome
        finally:
            if not self.keep:
                try:
                    _remove_dir(self.scratch_fd, name, mpath, self.owned)
                except Refusal:
                    self.keep = True
                    raise

    def _record_run(self, fd: int, path: str, window: tuple[float, float]) -> None:
        """Record each file or link the test run made in directory fd (path) and below: one born in window.

        Every other entry must be one this run made; a directory never is the test's. Else refuse, keep all."""
        with _fs(path):
            names = sorted(os.listdir(fd))  # readdir of a dup of fd (os.scandir is the removal's call)
        for name in names:
            epath = os.path.join(path, name)
            with _fs(epath):
                st = os.stat(name, dir_fd=fd, follow_symlinks=False)
            made = (st.st_dev, st.st_ino)
            if stat.S_ISDIR(st.st_mode):
                if made not in self.owned:
                    raise Refusal(f"{epath} is a directory this run did not make; it was kept and nothing is reported")
                with _fs(epath):
                    sub = os.open(name, DIR_FLAGS, dir_fd=fd)
                try:
                    with _fs(epath):
                        held = os.fstat(sub)
                    if (held.st_dev, held.st_ino) != made:
                        raise Refusal(f"{epath} changed after the test run; it was kept and nothing is reported")
                    self._record_run(sub, epath, window)
                finally:
                    _close(sub, epath)
            elif made not in self.owned:
                if not window[0] <= st.st_birthtime <= window[1]:
                    raise Refusal(f"{epath} was made before the test run, not by this run; it was kept and "
                                  "nothing is reported")
                self.owned.add(made)

    def _walk(self, src_fd, src, rel, dst_fd, dst, seen, replace) -> None:
        """Copy (or with dst_fd None, only scan) one lane directory through fds.

        Each scandir, stat, open and readlink through src_fd follows the check that src_fd is in the lane,
        and scandir and readlink are followed by it too."""
        self._in_lane(src_fd, src)
        with _fs(src), os.scandir(src_fd) as it:
            entries = sorted(it, key=lambda e: e.name)
        self._in_lane(src_fd, src)  # after the listing too: a move just before it is seen
        for entry in entries:
            name = entry.name
            if not rel and name == ".git":
                continue
            r, spath, dpath = rel + name, os.path.join(src, name), os.path.join(dst, name)
            self._in_lane(src_fd, src)
            with _fs(spath):
                st = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(st.st_mode):
                self._in_lane(src_fd, src)
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
                        sub = self._made(dst_fd, dst, name, 0o755)
                    try:
                        self._walk(fd, spath, r + "/", sub, dpath, seen, replace)
                    finally:
                        if sub is not None:
                            _close(sub, dpath)
                finally:
                    _close(fd, spath)
            elif stat.S_ISLNK(st.st_mode):
                self._in_lane(src_fd, src)
                with _fs(spath):
                    text = os.readlink(name, dir_fd=src_fd)
                self._in_lane(src_fd, src)  # after the read too
                seen[r] = ("link", text) + _identity(st)
                if dst_fd is not None:
                    if seen[r] != self.snapshot.get(r):  # only a link the first walk recorded and checked
                        raise Refusal(f"the lane changed during the run at {spath}; nothing is reported")
                    self._create(dst_fd, dst, dpath, lambda: os.symlink(text, name, dir_fd=dst_fd))
                    self._made_link(dst_fd, name, dpath, text)
                    self._check_at(dst_fd, dst, "link", child=name)  # where the create put it
            elif stat.S_ISREG(st.st_mode):
                data = _read_file(self.root_fd, self.root, src_fd, name, spath, st)
                digest = hashlib.sha256(data).hexdigest()
                if r in self.targets and digest != self.targets[r].sha256:
                    raise Refusal(f"{spath} changed since it was parsed")
                seen[r] = ("file",) + _identity(st) + (digest,)
                if dst_fd is None:
                    continue
                mode = stat.S_IMODE(st.st_mode) & 0o777
                out = self._create(dst_fd, dst, dpath, lambda: os.open(name, CREATE_FLAGS, mode, dir_fd=dst_fd))
                try:
                    with _fs(dpath):
                        made = os.fstat(out)
                    self.owned.add((made.st_dev, made.st_ino))  # the file the O_EXCL create made
                    dest = _Dest(dpath, lambda: self._check_at(out, dpath, "copy file"))
                    try:
                        _write_all(out, replace.get(r, data), dest)  # each write follows the check
                    except Refusal:
                        self._check_at(out, dpath, "copy file")
                        raise
                    self._check_at(out, dpath, "copy file")  # after the last byte
                finally:
                    _close(out, dpath)
            else:
                raise Refusal(f"{spath} is a special file")

    def _in_lane(self, fd: int, path: str) -> None:
        _in_lane(self.root_fd, self.root, fd, path)

    def _made_link(self, dir_fd: int, name: str, path: str, text: str) -> None:
        """Right after the create, name in dir_fd must be a link with text; its identity is then this run's."""
        try:
            with _fs(path):
                st = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
                now = os.readlink(name, dir_fd=dir_fd) if stat.S_ISLNK(st.st_mode) else None
            if now != text:
                raise Refusal(f"{path} is not the link this run just made; it was kept and nothing is reported")
        except Refusal:
            self.keep = True
            raise
        self.owned.add((st.st_dev, st.st_ino))


def _still_at(fd: int, path: str) -> None:
    """fd's live path (F_GETPATH) is still path; else refuse and keep it."""
    live = _realpath(fd, path)
    if live != path:
        raise Refusal(f"{path} is now at {live}; both were kept")


def _remove_dir(parent_fd: int, name: str, path: str, owned: set) -> None:
    """Remove a directory this run made, only through fds bound to it.

    owned holds the (st_dev, st_ino) of each entry this run made (directory, file, link), recorded
    when it made it; an entry not in it is never removed, and the removal refuses. path is the path
    recorded when it was made (outside the lane): each unlink and the rmdir happen only while the
    directory they act in still lives there."""
    with _fs(path):
        fd = os.open(name, DIR_FLAGS, dir_fd=parent_fd)
    try:
        with _fs(path):
            held = os.fstat(fd)
        made = (held.st_dev, held.st_ino)
        if made not in owned:
            raise Refusal(f"{path} is not a directory this run made; both were kept")
        with _fs(path), os.scandir(fd) as it:
            names = [e.name for e in it]
        for entry in names:
            epath = os.path.join(path, entry)
            with _fs(epath):
                st = os.stat(entry, dir_fd=fd, follow_symlinks=False)
            mine = (st.st_dev, st.st_ino)
            if mine not in owned:
                raise Refusal(f"{epath} is not an entry this run made; it was kept")
            if stat.S_ISDIR(st.st_mode):
                _remove_dir(fd, entry, epath, owned)
            else:
                _still_at(fd, path)
                with _fs(epath):  # no call between the check above and this unlink
                    os.unlink(entry, dir_fd=fd)
                if st.st_nlink <= 1:
                    owned.discard(mine)  # gone: a later entry may reuse its inode
        with _fs(path):
            now = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if (now.st_dev, now.st_ino) != made:
            raise Refusal(f"{path} now names another directory; both were kept")
        _still_at(parent_fd, os.path.dirname(path))
        _still_at(fd, path)  # the held directory itself is still at its path: a swap after the stat is seen
        with _fs(path):  # no call between the check above and this rmdir
            os.rmdir(name, dir_fd=parent_fd)
        # A swap at the rmdir itself removes the swapped-in directory; the held one then lives elsewhere.
        _still_at(fd, path)
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
    exited = _wait_exit(proc.pid, timeout)
    # The child is not reaped yet, so its pid still names its own group: the kill reaches only the test's group.
    try:
        _kill_group(proc.pid)  # anything the test left running, and the test itself on a timeout
    except PermissionError:
        pass  # only exited members remain: macOS answers EPERM for a group of zombies
    code = proc.wait()
    if not exited:
        return "error", f"timeout after {timeout:g}s"
    return ("survived", "exit 0") if code == 0 else ("killed", f"exit {code}")


def _wait_exit_waitid(pid: int, timeout: float) -> bool:
    """True once child pid has exited (left unreaped), False after timeout seconds; polls like Popen.wait."""
    deadline = time.monotonic() + timeout
    delay = 0.0005
    while True:
        try:
            if os.waitid(os.P_PID, pid, os.WEXITED | os.WNOWAIT | os.WNOHANG) is not None:
                return True
        except ChildProcessError:
            return True  # no longer a waitable child: proc.wait() settles it, as Popen.wait does
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        delay = min(delay * 2, remaining, 0.05)
        time.sleep(delay)


def _wait_exit_kqueue(pid: int, timeout: float) -> bool:
    """True once child pid has exited (left unreaped), False after timeout seconds."""
    kq = select.kqueue()
    try:
        change = select.kevent(pid, filter=select.KQ_FILTER_PROC,
                               flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT, fflags=select.KQ_NOTE_EXIT)
        events = kq.control([change], 1, timeout)
    finally:
        kq.close()
    if not events:
        return False
    event = events[0]
    # A child that already exited (unreaped) refuses the registration with ESRCH: that is its exit.
    if event.flags & select.KQ_EV_ERROR and event.data != errno.ESRCH:
        raise OSError(event.data, os.strerror(event.data))
    return True


_wait_exit = _wait_exit_waitid if hasattr(os, "waitid") else _wait_exit_kqueue


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


def main(argv: list[str] | None = None, ops_dir: str = OPS_DIR) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", action="append", required=True, help="a Python file in the lane (cwd)")
    ap.add_argument("--test", required=True, help="the test command, run with sh in each lane copy")
    ap.add_argument("--out", required=True, help="a new JSON file outside the lane")
    ap.add_argument("--allow", help="JSON list of {id, reason} for mutants that may stay unkilled")
    ap.add_argument("--timeout", type=_positive, help="seconds per test run (default 10x baseline, >= 60)")
    ap.add_argument("--base", help="mutate only the lines that differ from this git revision")
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out)
    parent, name = os.path.dirname(out), os.path.basename(args.out)
    kept = ""
    try:
        if name in ("", ".", ".."):
            raise Refusal(f"--out {args.out} names no file")
        with _fs(f"operator directory {ops_dir}"):
            operators = load_operators(ops_dir)
        root = "(the current directory)"
        root_fd = open_root(os.curdir)
        try:
            root = _realpath(root_fd, f"lane {root}")
            targets = read_targets(root_fd, root, args.file)
            scope = line_scope(args.base, targets)
            mutants = parsed([m for t in targets.values() for m in mutants_for(t.rel, t.data, scope[t.rel], operators)])
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
                    """The lane, then the parent, then the file: the file's live path is the last call."""
                    live_lane = _realpath(root_fd, f"lane {root}{kept}")
                    expected = os.path.join(_realpath(parent_fd, f"--out parent {parent}{kept}"), name)
                    real = _realpath(out_fd, f"{out}{kept}")
                    if real != expected:
                        raise Refusal(f"{verb} {real}, not {expected}; it was left in place")
                    if _inside(live_lane, real):
                        raise Refusal(f"{verb} {real}, which is now inside the lane; it was left in place")
                try:
                    # Before each write (the first: a move at the create writes nothing inside), and after the last.
                    _write_all(out_fd, body, _Dest(f"{out} (left in place, incomplete)", lambda: placed("writing")))
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
