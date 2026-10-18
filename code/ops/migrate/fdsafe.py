"""fd-bound walk, read and write: the one implementation every migrate tool shares.

Every object is reached through an fd held on its parent, never by a path checked and
then opened again (L/part2/extra-fd-binding.md; T212 rulings 2 and 5-10, T201 rulings 1,
3, 4, 9 and 10, T211 rulings 1, 6 and 7):

- A root is opened once with O_RDONLY | O_DIRECTORY | O_NOFOLLOW and held. Its live path
  (F_GETPATH) must be the absolute path given, so no component of it is a link.
- The walk enters each directory with os.open(name, ..., dir_fd=parent) and os.scandir(fd),
  and the opened directory must be the (st_dev, st_ino) the scan saw.
- A leaf is opened with O_RDONLY | O_NOFOLLOW through its parent fd. Its fstat must equal
  the scan's lstat (st_dev, st_ino, st_size, st_mtime_ns) before and after the read, and
  the read must return exactly st_size bytes, so the bytes come from the object scanned.
- An output is created with O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW under a held parent.
  The parent's live path must lie outside the live path of every held root before the
  write; after the write, with the file fd still open, the file's live path must lie
  outside every root and equal the parent's live path plus the name.

A leaf open also carries O_NONBLOCK, so a FIFO put in place of a leaf refuses instead of
blocking; O_DIRECTORY already refuses a FIFO in place of a directory (ENOTDIR). Every OSError from a call on a named path (open, scandir, read, write, fstat,
F_GETPATH, close) becomes a Refusal naming the path and the errno name; any other
exception propagates. Nothing here overwrites or unlinks: an output refused after it
exists is named and left in place.
"""
from __future__ import annotations

import contextlib
import ctypes
import errno
import fcntl
import os
import stat
import sys
from dataclasses import dataclass
from typing import Callable, Iterator, Sequence

DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
LEAF_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
CHUNK = 1 << 20
PATH_MAX = 1024


class Refusal(ValueError):
    """Input the tool will not use; the caller keeps every input unchanged.

    path names the object; errno is the errno of the OSError behind it, or None."""

    def __init__(self, path: str, reason: str, err: int | None = None):
        self.path = path
        self.errno = err
        tag = "" if err is None else f" [{errno.errorcode.get(err, err)}]"
        super().__init__(f"{path!r}: {reason}{tag}")


@contextlib.contextmanager
def fs(path: str) -> Iterator[None]:
    """An OSError inside the block is a Refusal that names path and the errno."""
    try:
        yield
    except OSError as exc:
        raise Refusal(path, exc.strerror or type(exc).__name__, exc.errno) from exc


def close(fd: int, path: str) -> None:
    with fs(path):
        os.close(fd)


def live_path(fd: int, path: str) -> str:
    """Where the object an fd is open on is now (macOS F_GETPATH), not what path names now."""
    with fs(path):
        buf = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(PATH_MAX))
    return os.fsdecode(buf.split(b"\0", 1)[0])


def inside(root_live: str, path_live: str) -> bool:
    return path_live == root_live or path_live.startswith(root_live.rstrip("/") + "/")


def _fstat(fd: int, path: str) -> os.stat_result:
    with fs(path):
        return os.fstat(fd)


def _read(fd: int, path: str) -> bytes:
    with fs(path):
        return os.read(fd, CHUNK)


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


@dataclass(frozen=True)
class Dir:
    """A held directory fd; path names it in messages."""
    fd: int
    path: str

    def live(self) -> str:
        return live_path(self.fd, self.path)

    def close(self) -> None:
        close(self.fd, self.path)

    def __enter__(self) -> "Dir":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def _open_dir(path: str) -> Dir:
    with fs(path):
        fd = os.open(path, DIR_FLAGS)
    return Dir(fd, path)


def hold_root(path: str) -> Dir:
    """Open a root without following any link in its path; the caller closes it."""
    with fs(path):
        given = os.path.abspath(path)
    held = _open_dir(given)
    try:
        real = held.live()
        if real != given:
            raise Refusal(given, f"is not its own real path ({real}); a component is a link")
    except BaseException:
        held.close()
        raise
    return held


def open_out_parent(path: str) -> Dir:
    """Open an output's parent directory without following its final component."""
    with fs(path):
        given = os.path.abspath(path)
    return _open_dir(given)


@dataclass(frozen=True)
class Entry:
    """One scanned entry, reached through its directory's held fd.

    st is the scan's lstat; rel is the path below the root with "/" separators."""
    dir_fd: int
    name: str
    path: str
    rel: str
    st: os.stat_result


def walk(root: Dir, visit: Callable[[Entry], None]) -> None:
    """Call visit on every entry under root, depth first, names sorted by their bytes.

    A directory is visited, then entered through its parent's fd; the opened directory
    must be the one the scan saw. Every fd the walk opens is closed before it returns."""

    def scan(dir_fd: int, dirpath: str, prefix: str) -> None:
        with fs(dirpath), os.scandir(dir_fd) as it:
            entries = sorted(it, key=lambda e: os.fsencode(e.name))
        for de in entries:
            path = os.path.join(dirpath, de.name)
            with fs(path):
                st = de.stat(follow_symlinks=False)
            entry = Entry(dir_fd, de.name, path, prefix + de.name, st)
            visit(entry)
            if stat.S_ISDIR(st.st_mode):
                with fs(path):
                    fd = os.open(de.name, DIR_FLAGS, dir_fd=dir_fd)
                try:
                    opened = _fstat(fd, path)
                    if (opened.st_dev, opened.st_ino) != (st.st_dev, st.st_ino):
                        raise Refusal(path, "directory changed between scan and open")
                    scan(fd, path, entry.rel + "/")
                finally:
                    close(fd, path)

    scan(root.fd, root.path, "")


def read_leaf(entry: Entry, sink: Callable[[bytes], None]) -> int:
    """Pass the bytes of one scanned regular file to sink, chunk by chunk; return the count.

    Raises Refusal if the object opened is not the one scanned, before or after the read."""
    if not stat.S_ISREG(entry.st.st_mode):
        raise Refusal(entry.path, "is not a regular file")
    scanned = _identity(entry.st)
    with fs(entry.path):
        fd = os.open(entry.name, LEAF_FLAGS, dir_fd=entry.dir_fd)
    try:
        if _identity(_fstat(fd, entry.path)) != scanned:
            raise Refusal(entry.path, "changed between scan and open")
        count = 0
        while chunk := _read(fd, entry.path):
            count += len(chunk)
            sink(chunk)
        if _identity(_fstat(fd, entry.path)) != scanned:
            raise Refusal(entry.path, "changed while it was read")
        if count != entry.st.st_size:
            raise Refusal(entry.path, f"read {count} bytes, scanned {entry.st.st_size}")
    finally:
        close(fd, entry.path)
    return count


def read_bytes(entry: Entry) -> bytes:
    parts: list[bytes] = []
    read_leaf(entry, parts.append)
    return b"".join(parts)


@dataclass(frozen=True)
class Held:
    """[LAW:types-are-the-program] A created file whose descriptor the caller owns."""
    fd: int
    parent: Dir
    name: str


def create_held(parent: Dir, name: str, data: bytes, roots: Sequence[Dir]) -> Held:
    """Create and fully write a file; transfer its fd before any post-write location check.

    The caller closes through close. A failed write leaves the named file in place.
    """
    target = os.path.join(parent.path, name)
    if name in ("", ".", "..") or "/" in name or "\0" in name:
        raise Refusal(target, "names no single file")
    if not roots:
        raise Refusal(target, "no held root to check the output against")
    before = parent.live()
    for root in roots:
        if inside(root.live(), before):
            raise Refusal(target, f"output parent {before} is inside root {root.path}")
    with fs(target):
        fd = os.open(name, CREATE_FLAGS, 0o644, dir_fd=parent.fd)
    kept = f"{target} (created, left in place)"
    transferred = False
    try:
        with fs(f"{target} (left in place, incomplete)"):
            view = memoryview(data)
            while view:
                view = view[os.write(fd, view):]
        held = Held(fd, parent, name)
        transferred = True
        return held
    finally:
        if not transferred:
            close(fd, kept)


def create_file(parent: Dir, name: str, data: bytes, roots: Sequence[Dir]) -> str:
    """Create parent/name holding exactly data, outside every held root; return its live path.

    Never overwrites. A refusal after the file exists names it and leaves it in place.
    """
    # [LAW:one-source-of-truth] Both public creates share pre-checks and the write loop.
    held = create_held(parent, name, data, roots)
    try:
        return settle(held, roots)
    finally:
        close(held.fd, f"{os.path.join(parent.path, name)} (created, left in place)")


def settle(held: Held, roots: Sequence[Dir]) -> str:
    """[LAW:single-enforcer] The post-write location checks of a held created file; return its live path. Leaves the fd open."""
    parent, name = held.parent, held.name
    kept = f"{os.path.join(parent.path, name)} (created, left in place)"
    where = live_path(held.fd, kept)
    for root in roots:
        if inside(live_path(root.fd, f"{root.path}; {kept}"), where):
            raise Refusal(where, f"was written inside root {root.path}; left in place")
    named = os.path.join(live_path(parent.fd, f"{parent.path}; {kept}"), name)
    if where != named:
        raise Refusal(where, f"was moved during the write (expected {named}); left in place")
    return where


def _child(parent: Dir, name: str) -> str:
    path = os.path.join(parent.path, name)
    if name in ("", ".", "..") or "/" in name or "\0" in name:
        raise Refusal(path, "names no single entry")
    return path


def _settled(parent: Dir, label: str | None = None) -> str:
    """The parent's live path, which must still be the path it is held as (a moved parent refuses)."""
    live = live_path(parent.fd, parent.path if label is None else f"{parent.path}; {label}")
    if live != parent.path:
        raise Refusal(label or parent.path, f"is held at {live}, not at {parent.path}")
    return live


def _within(parent_live: str, parent: Dir, root_lives: Sequence[tuple[Dir, str]], label: str | None = None) -> None:
    if not any(inside(root_live, parent_live) for _, root_live in root_lives):
        raise Refusal(label or parent.path, f"live path {parent_live} is inside no held root "
                      f"({', '.join(root.path for root, _ in root_lives)})")


def read_named(parent: Dir, name: str) -> bytes:
    """Return the bytes of the regular file parent/name, read through the held parent with read_leaf's checks.

    The parent's live path check is the last filesystem call before the leaf is opened."""
    path = _child(parent, name)
    with fs(path):
        st = os.lstat(name, dir_fd=parent.fd)
    entry = Entry(parent.fd, name, path, name, st)
    _settled(parent)
    return read_bytes(entry)


def mkdir(parent: Dir, name: str) -> Dir:
    """Create the directory parent/name and return it held; the caller closes it.

    The parent's live path check is the last filesystem call before the mkdir. Never
    overwrites; a refusal after the directory exists names it and leaves it in place."""
    path = _child(parent, name)
    before = _settled(parent)
    with fs(path):
        os.mkdir(name, 0o755, dir_fd=parent.fd)
    kept = f"{path} (created, left in place)"
    with fs(kept):
        st = os.lstat(name, dir_fd=parent.fd)
    with fs(kept):
        fd = os.open(name, DIR_FLAGS, dir_fd=parent.fd)
    try:
        opened = _fstat(fd, kept)
        if (opened.st_dev, opened.st_ino) != (st.st_dev, st.st_ino):
            raise Refusal(kept, "changed between create and open")
        where = live_path(fd, kept)
        expected = os.path.join(before, name)
        if where != expected:
            raise Refusal(where, f"was created away from {expected}; left in place")
    except BaseException:
        close(fd, kept)
        raise
    return Dir(fd, path)


def _resolve_noreplace() -> tuple[Callable[..., int], int] | None:
    """libc's rename that refuses an existing target, and its flag; None when libc has neither call.

    macOS renameatx_np(..., RENAME_EXCL); Linux renameat2(..., RENAME_NOREPLACE)."""
    name, flag = ("renameatx_np", 0x4) if sys.platform == "darwin" else ("renameat2", 0x1)
    func = getattr(ctypes.CDLL(None, use_errno=True), name, None)
    if func is None:
        return None
    func.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    func.restype = ctypes.c_int
    return func, flag


_NOREPLACE = _resolve_noreplace()


def _rename_noreplace(src_name: str, dst_name: str, *, src_dir_fd: int, dst_dir_fd: int) -> None:
    """Rename through dir fds without ever replacing a target; an existing target is EEXIST.

    There is no fallback: a missing call, or a filesystem that rejects the flag (EINVAL,
    ENOTSUP), is an OSError like any other."""
    if _NOREPLACE is None:
        raise OSError(errno.ENOTSUP, "libc has no exclusive rename (renameatx_np or renameat2)")
    func, flag = _NOREPLACE
    if func(src_dir_fd, os.fsencode(src_name), dst_dir_fd, os.fsencode(dst_name), flag) != 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))


def rename(src_parent: Dir, src_name: str, dst_parent: Dir, dst_name: str, roots: Sequence[Dir]) -> str:
    """Move src_parent/src_name to dst_parent/dst_name inside the held roots; return its live path.

    The source is held open, must be a regular file or a directory, and must be the same
    object (fstat st_dev, st_ino, st_size, st_mtime_ns) before and after the move, and the
    object at the target. Both parents must be at their held paths and inside a held root;
    their live path checks are the last filesystem calls before the rename. Never overwrites
    an existing target, even one created after the absent-target check: the rename itself is
    exclusive (_rename_noreplace). A refusal after the move names the target and leaves it in place."""
    src = _child(src_parent, src_name)
    dst = _child(dst_parent, dst_name)
    if not roots:
        raise Refusal(dst, "no held root to check the move against")
    with fs(src):
        fd = os.open(src_name, LEAF_FLAGS, dir_fd=src_parent.fd)
    label = src
    try:
        held = _fstat(fd, src)
        if not (stat.S_ISREG(held.st_mode) or stat.S_ISDIR(held.st_mode)):
            raise Refusal(src, "is not a regular file or directory")
        try:
            with fs(dst):
                os.lstat(dst_name, dir_fd=dst_parent.fd)
        except Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
        else:
            raise Refusal(dst, "already exists; rename never overwrites", errno.EEXIST)
        root_lives = [(root, root.live()) for root in roots]
        src_live = _settled(src_parent)
        dst_live = _settled(dst_parent)
        _within(src_live, src_parent, root_lives)
        _within(dst_live, dst_parent, root_lives)
        with fs(f"{src} -> {dst}"):
            _rename_noreplace(src_name, dst_name, src_dir_fd=src_parent.fd, dst_dir_fd=dst_parent.fd)
        label = f"{dst} (moved, left in place)"
        if _identity(_fstat(fd, label)) != _identity(held):
            raise Refusal(label, "changed while it was moved")
        with fs(label):
            landed = os.lstat(dst_name, dir_fd=dst_parent.fd)
        if (landed.st_dev, landed.st_ino) != (held.st_dev, held.st_ino):
            raise Refusal(label, "is not the object that was held")
        root_lives = [(root, live_path(root.fd, f"{root.path}; {label}")) for root in roots]
        _within(_settled(dst_parent, label), dst_parent, root_lives, label)
    finally:
        close(fd, label)
    return os.path.join(dst_live, dst_name)
