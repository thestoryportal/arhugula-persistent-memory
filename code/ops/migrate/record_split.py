#!/usr/bin/env python3
"""Classify each leaf of one unit as tracked record, attested bulk or governed payload.

Read only on the unit. Size, the old results/ folder and ignore rules never decide;
a name can only raise a file to record, never lower one (A/SPEC.md:632-641,
A/DESIGN.md:60-62). In order, for a regular file:

- Record kind: its basename, lowercased, ends with .json, .jsonl, .ipynb or .log, or
  contains "manifest". It is a tracked record whatever its bytes (UTF-16, Latin-1, NUL);
  Git tracks any bytes. An attestation naming it is refused: it cannot override record
  status.
- Any other file named, with its exact sha256, by an attestation of regenerable
  non-record output is attested bulk, text included. Only an attestation makes bulk.
- Any other file whose bytes are NUL-free strict UTF-8 is a tracked record.
- Any other file is a governed payload: ignored bytes kept with exact custody (sha256
  and size), never anonymous bulk (OPEN-QUESTIONS.md Q8 default).
Every regular file below a nested `.git` folder is a governed payload whatever its name or bytes,
and an attestation naming one is refused: Git's own store is never git-added (ruling R6, "Never
git add a nested repo"). These are the leaves unit_manifest records below that `.git`; a `.git`
that is not a directory (a gitlink file or a link) and a link or special file inside a `.git` are
refused, as unit_manifest refuses them.
A symlink is never followed. Relative text staying inside the unit, or absolute text
normalized to neither the unit root nor below it, is a tracked record of that text;
absolute text naming the unit root or below it is refused.
A --root that is one regular file is a file unit: its one leaf has the path "."
and is named by the root.

The walk is bound to fds: --root is opened once without following a link and held (a file
root is then read through its parent's fd as that same entry, like any leaf);
each directory is entered only through its parent's fd and must be the (st_dev, st_ino)
the scan saw; each file is read through one fd opened without following links, whose
fstat must match the scan's lstat before and after the read, so size and hash come from
one object. The --out file is created through an fd of its parent directory, whose real
path (F_GETPATH) must lie outside the held root's real path, read at check time, before
the write and again after it.

Every expected invalid input (missing, linked or special root, missing or invalid --out
parent, an unreadable or malformed attestation, an attested record, a changed file, a
link that escapes the unit, a special file, a `.git` that is not a directory, a link or special
file inside a `.git`) and every OSError from a
filesystem call on the unit, a leaf or the output exits 2 with one refusal line naming
the path and errno. It never overwrites and never deletes: an output that lands inside the unit after
a race is refused by name and left in place.

An attestation is one JSON record per run, written by the operator or by MAESTRO under
the operator's ruling (Q8):
  {"attested_by": "operator", "regenerate": "<command>",
   "leaves": [{"path": "<unit relpath>", "sha256": "<hex>"}, ...]}
"""
from __future__ import annotations

import argparse
import codecs
import contextlib
import errno
import fcntl
import hashlib
import json
import os
import posixpath
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Literal

# [LAW:no-shared-mutable-globals] exception: icm21_moves uses bare imports of its state siblings.
sys.path.append(posixpath.join(posixpath.dirname(posixpath.dirname(posixpath.dirname(__file__))), "state"))
import icm21_moves  # noqa: E402

from ops.migrate import fdsafe

TRACKED = "tracked-record"
BULK = "attested-bulk"
PAYLOAD = "governed-payload"
ATTESTERS = frozenset({"operator", "MAESTRO"})
CHUNK = 1 << 20
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
SHA256 = re.compile(r"[0-9a-f]{64}")
RECORD_SUFFIXES = (".json", ".jsonl", ".ipynb", ".log")


class Refusal(Exception):
    """Input the tool will not classify; the caller keeps the source unchanged."""


@dataclass(frozen=True)
class FileLeaf:
    path: str
    size: int
    sha256: str
    is_text: bool


@dataclass(frozen=True)
class LinkLeaf:
    path: str
    link: str


@dataclass(frozen=True)
class GitLeaf:
    """A regular file below a nested .git folder: part of Git's store, never a record."""
    path: str
    size: int
    sha256: str


Leaf = FileLeaf | LinkLeaf | GitLeaf


@dataclass(frozen=True)
class Attested:
    path: str
    sha256: str
    source: str


@dataclass(frozen=True)
class Row:
    path: str
    cls: Literal["tracked-record", "attested-bulk", "governed-payload"]
    kind: Literal["file", "link"]
    size: int | None
    sha256: str | None
    link: str | None


def path_key(path: str) -> bytes:
    return path.encode("utf-8", "surrogateescape")


# ---- pure core -------------------------------------------------------------------

def parse_attestation(doc: object, source: str) -> tuple[Attested, ...]:
    if not isinstance(doc, dict):
        raise Refusal(f"{source}: attestation is not a JSON object")
    attested_by = doc.get("attested_by")
    if not isinstance(attested_by, str) or attested_by not in ATTESTERS:
        raise Refusal(f"{source}: attested_by must be one of {sorted(ATTESTERS)}")
    regenerate = doc.get("regenerate")
    if not isinstance(regenerate, str) or not regenerate.strip():
        raise Refusal(f"{source}: regenerate must name the regeneration command")
    leaves = doc.get("leaves")
    if not isinstance(leaves, list) or not leaves:
        raise Refusal(f"{source}: leaves must be a non-empty list")
    out = []
    for item in leaves:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise Refusal(f"{source}: each leaf needs a path")
        digest = item.get("sha256")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise Refusal(f"{source}: {item['path']!r} sha256 is not 64 lowercase hex")
        out.append(Attested(item["path"], digest, source))
    return tuple(out)


def record_kind(path: str) -> bool:
    name = posixpath.basename(path).lower()
    return name.endswith(RECORD_SUFFIXES) or "manifest" in name


def classify(leaves: list[Leaf], attested: list[Attested], root: str) -> tuple[Row, ...]:
    """Each leaf's row. A leaf's name is the last component of root joined with its path, so a file
    unit's one leaf (path ".") is named by its root."""
    by_path: dict[str, Attested] = {}
    for a in attested:
        if a.path in by_path:
            raise Refusal(f"{a.path!r} is attested twice ({by_path[a.path].source}, {a.source})")
        by_path[a.path] = a
    leaf_paths = {leaf.path for leaf in leaves}
    for a in by_path.values():
        if a.path not in leaf_paths:
            raise Refusal(f"{a.source}: attested {a.path!r} is not a leaf of the unit")
    rows = []
    for leaf in sorted(leaves, key=lambda leaf: path_key(leaf.path)):
        a = by_path.get(leaf.path)
        if isinstance(leaf, LinkLeaf):
            if a is not None:
                raise Refusal(f"{a.source}: attested {leaf.path!r} is not a regular file")
            rows.append(Row(leaf.path, TRACKED, "link", None, None, leaf.link))
            continue
        if isinstance(leaf, GitLeaf):
            # [LAW:types-are-the-program] A nested repo's store is payload by its leaf type; no name or
            # attestation reaches it (ruling R6: never git add a nested repo).
            if a is not None:
                raise Refusal(f"{a.source}: attested {leaf.path!r} is inside a nested .git; it stays governed payload")
            rows.append(Row(leaf.path, PAYLOAD, "file", leaf.size, leaf.sha256, None))
            continue
        # [LAW:one-source-of-truth] The root supplies the name of a file unit's dot leaf.
        if record_kind(posixpath.normpath(posixpath.join(root, leaf.path))):
            if a is not None:
                raise Refusal(f"{a.source}: {leaf.path!r} is a scientific record; "
                              "an attestation cannot make it bulk")
            cls = TRACKED
        elif a is not None:
            if a.sha256 != leaf.sha256:
                raise Refusal(f"{a.source}: {leaf.path!r} digest changed since attestation")
            cls = BULK
        elif leaf.is_text:
            cls = TRACKED
        else:
            cls = PAYLOAD
        rows.append(Row(leaf.path, cls, "file", leaf.size, leaf.sha256, None))
    return tuple(rows)


def link_escapes(rel: str, text: str, root: str) -> bool:
    if posixpath.isabs(text):
        # [LAW:single-enforcer] R8's lexical absolute-text rule belongs to the move checker.
        return icm21_moves.absolute_text_inside(text, PurePosixPath(os.path.abspath(root)))
    target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), text))
    return target == ".." or target.startswith("../")


# ---- filesystem edge -------------------------------------------------------------

@contextlib.contextmanager
def _fs(path: str):
    """An OSError on a named input or output path is a refusal that names it and its errno."""
    try:
        yield
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        raise Refusal(f"{path}: {code} {exc.strerror}") from exc
    except fdsafe.Refusal as exc:
        # [LAW:no-silent-failure] Preserve the fd reader's diagnostic at this tool's boundary.
        raise Refusal(str(exc)) from exc


@dataclass(frozen=True)
class _At:
    """A scanned entry reached through its directory's fd; path names it in messages."""
    dir_fd: int
    name: str
    path: str
    st: os.stat_result

    def __fspath__(self) -> str:
        return self.path


def _digest(at: _At) -> tuple[str, bool]:
    """sha256 of the leaf's bytes and whether they are NUL-free strict UTF-8.

    The bytes come from one fd, opened through the directory fd, whose fstat equals the
    scan's lstat before and after the read."""
    scanned = _identity(at.st)
    try:
        fd = os.open(at.name, FILE_FLAGS, dir_fd=at.dir_fd)
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        if exc.errno == errno.ELOOP:
            raise Refusal(f"{at.path!r} changed into a symlink before it was hashed [{code}]") from exc
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            raise Refusal(f"{at.path!r} changed (gone) before it was hashed [{code}]") from exc
        with _fs(at.path):
            raise
    with _fs(at.path), open(fd, "rb", buffering=0) as fh:
        if _identity(os.fstat(fd)) != scanned:
            raise Refusal(f"{at.path!r} changed before it was hashed")
        h = hashlib.sha256()
        decoder = codecs.getincrementaldecoder("utf-8")("strict")
        is_text = True
        while chunk := fh.read(CHUNK):
            h.update(chunk)
            if is_text:
                try:
                    decoder.decode(chunk)
                    is_text = b"\0" not in chunk
                except UnicodeDecodeError:
                    is_text = False
        if _identity(os.fstat(fd)) != scanned:
            raise Refusal(f"{at.path!r} changed while it was hashed")
    if is_text:
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            is_text = False
    return h.hexdigest(), is_text


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


@dataclass(frozen=True)
class Root:
    """The held unit root: a directory walked through its fd, or one regular file (a file unit)."""
    fd: int
    kind: Literal["directory", "file"]


ROOT_KINDS: dict[int, tuple[Literal["directory", "file"], int]] = {
    stat.S_IFDIR: ("directory", DIR_FLAGS), stat.S_IFREG: ("file", FILE_FLAGS),
}


def open_root(root: Path) -> Root:
    # [LAW:types-are-the-program] the root's kind is observed once and carried; its open flags (and, for a
    # file, the identity check in scan) bind the held fd to that kind.
    try:
        mode = stat.S_IFMT(os.lstat(root).st_mode)
        if mode not in ROOT_KINDS:
            raise Refusal(f"unit root {root} is neither a real directory nor a regular file")
        kind, flags = ROOT_KINDS[mode]
        return Root(os.open(root, flags), kind)
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        raise Refusal(f"unit root {root} is not a real directory or regular file: {code} {exc.strerror}") from exc


def scan(held: Root, root: str) -> list[Leaf]:
    leaves: list[Leaf] = []

    def hashed(dir_fd: int, name: str, path: str, rel: str, est: os.stat_result) -> tuple[str, bool]:
        sha256, is_text = _digest(_At(dir_fd, name, path, est))
        with _fs(path):
            now = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
        if _identity(now) != _identity(est):
            raise Refusal(f"{rel!r} changed while it was hashed")
        return sha256, is_text

    def regular(dir_fd: int, name: str, path: str, rel: str, est: os.stat_result) -> None:
        sha256, is_text = hashed(dir_fd, name, path, rel, est)
        leaves.append(FileLeaf(rel, est.st_size, sha256, is_text))

    def git_regular(dir_fd: int, name: str, path: str, rel: str, est: os.stat_result) -> None:
        leaves.append(GitLeaf(rel, est.st_size, hashed(dir_fd, name, path, rel, est)[0]))

    def walk(dir_fd: int, dirpath: str, prefix: str, in_git: bool) -> None:
        """in_git: this directory is a nested .git or lies below one."""
        with _fs(dirpath), os.scandir(dir_fd) as it:
            entries = sorted(it, key=lambda e: path_key(e.name))
        for entry in entries:
            rel = prefix + entry.name
            path = os.path.join(dirpath, entry.name)
            with _fs(path):
                est = entry.stat(follow_symlinks=False)
            # [LAW:one-source-of-truth] exception: this repeats unit_manifest._walk's .git admission so both
            # tools cover one leaf set; each keeps its own fd-bound walk and refusal type.
            if entry.name == ".git" and not stat.S_ISDIR(est.st_mode):
                raise Refusal(f"nested .git at {rel!r} is not a directory (a gitlink or a link to another Git dir)")
            if in_git and not (stat.S_ISDIR(est.st_mode) or stat.S_ISREG(est.st_mode)):
                raise Refusal(f"{rel!r} inside a nested .git is a link or special file; Git would follow it")
            if stat.S_ISLNK(est.st_mode):
                with _fs(path):
                    # [LAW:single-enforcer] The shared reader binds the text to the scan's inode.
                    text = os.fsdecode(fdsafe.read_link(fdsafe.Entry(dir_fd, entry.name, path, rel, est)))
                if link_escapes(rel, text, root):
                    raise Refusal(f"link {rel!r} -> {text!r} escapes the unit")
                leaves.append(LinkLeaf(rel, text))
            elif stat.S_ISDIR(est.st_mode):
                with _fs(path):
                    fd = os.open(entry.name, DIR_FLAGS, dir_fd=dir_fd)
                try:
                    with _fs(path):
                        opened = os.fstat(fd)
                    if (opened.st_dev, opened.st_ino) != (est.st_dev, est.st_ino):
                        raise Refusal(f"directory {rel!r} changed during the walk")
                    walk(fd, path, rel + "/", in_git or entry.name == ".git")
                finally:
                    _close(fd, path)
            elif stat.S_ISREG(est.st_mode):
                (git_regular if in_git else regular)(dir_fd, entry.name, path, rel, est)
            else:
                raise Refusal(f"{rel!r} is a special file")

    def file_root() -> None:
        parent, name = os.path.split(os.path.abspath(root))
        with _fs(parent):
            parent_fd = os.open(parent, DIR_FLAGS)
        try:
            with _fs(root):
                opened = os.fstat(held.fd)
                est = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            if not stat.S_ISREG(opened.st_mode) or (est.st_dev, est.st_ino) != (opened.st_dev, opened.st_ino):
                raise Refusal(f"unit root {root} changed after it was opened")
            regular(parent_fd, name, root, ".", est)
        finally:
            _close(parent_fd, parent)

    # [LAW:dataflow-not-control-flow] the held root's kind picks its scan.
    {"directory": lambda: walk(held.fd, root, "", False), "file": file_root}[held.kind]()
    return leaves


def load_attestation(path: Path) -> tuple[Attested, ...]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"{path}: unreadable attestation: {exc}") from exc
    return parse_attestation(doc, str(path))


def split_unit(root: Path, attestations: list[Path], held: Root | None = None) -> tuple[Row, ...]:
    """Classify the unit; held, when given, is the caller's held root."""
    attested = [a for p in attestations for a in load_attestation(p)]
    holding = contextlib.nullcontext(held) if held is not None else _held_root(root)
    with holding as unit:
        return classify(scan(unit, str(root)), attested, str(root))


@contextlib.contextmanager
def _held_root(root: Path):
    held = open_root(root)
    try:
        yield held
    finally:
        _close(held.fd, f"unit root {root}")


def _close(fd: int, path: str) -> None:
    with _fs(path):
        os.close(fd)


def render(root: Path, rows: tuple[Row, ...]) -> str:
    leaves = [{"path": r.path, "class": r.cls, "kind": r.kind, "size": r.size,
               "sha256": r.sha256, "link": r.link} for r in rows]
    return json.dumps({"root": str(root), "leaves": leaves}, indent=1, sort_keys=True) + "\n"


def _dir_realpath(fd: int, path: str) -> str:
    with _fs(path):
        buf = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024))
    return os.fsdecode(buf.split(b"\0", 1)[0])


def _inside(root_real: str, path_real: str) -> bool:
    return os.path.commonpath([root_real, path_real]) == root_real


def _open_out_parent(out: Path) -> int:
    if out.name in ("", ".", ".."):
        raise Refusal(f"--out {out} names no file")
    try:
        return os.open(out.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        raise Refusal(f"--out parent {out.parent} is not a usable directory: {code} {exc.strerror}") from exc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, type=Path, help="the unit directory or unit file (read only)")
    ap.add_argument("--attestation", action="append", default=[], type=Path)
    ap.add_argument("--out", required=True, type=Path, help="new JSON file outside the unit")
    args = ap.parse_args(argv)
    kept = ""  # once the output exists, every later refusal names it as left in place
    try:
        held = open_root(args.root)
        root_fd = held.fd
        try:
            parent_fd = _open_out_parent(args.out)
            try:
                root_real = _dir_realpath(root_fd, f"unit root {args.root}")
                if _inside(root_real, _dir_realpath(parent_fd, f"--out parent {args.out.parent}")):
                    raise Refusal(f"--out {args.out} is inside the unit")
                rows = split_unit(args.root, args.attestation, held)
                body = render(args.root, rows).encode("utf-8")
                with _fs(str(args.out)):
                    out_fd = os.open(args.out.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                     0o644, dir_fd=parent_fd)
                kept = f" ({args.out} was created and left in place)"
                try:
                    with _fs(f"{args.out} (left in place, incomplete)"):
                        view = memoryview(body)
                        while view:
                            view = view[os.write(out_fd, view):]
                finally:
                    _close(out_fd, f"{args.out} (written, left in place)")
                parent_now = _dir_realpath(parent_fd, f"--out parent {args.out.parent}{kept}")
                if _inside(_dir_realpath(root_fd, f"unit root {args.root}{kept}"), parent_now):
                    raise Refusal(f"wrote {os.path.join(parent_now, args.out.name)}, which is now inside "
                                  "the unit; it was left in place")
            finally:
                _close(parent_fd, f"--out parent {args.out.parent}{kept}")
        finally:
            _close(root_fd, f"unit root {args.root}{kept}")
    except Refusal as exc:
        print("record_split: refused: " + str(exc).replace("\n", "\\n"), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
