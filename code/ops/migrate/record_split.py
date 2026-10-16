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
A symlink is never followed. One whose text stays inside the unit is a tracked record
of that text.

The walk is bound to fds: --root is opened once without following a link and held;
each directory is entered only through its parent's fd and must be the (st_dev, st_ino)
the scan saw; each file is read through one fd opened without following links, whose
fstat must match the scan's lstat before and after the read, so size and hash come from
one object. The --out file is created through an fd of its parent directory, whose real
path (F_GETPATH) must lie outside the held root's real path, read at check time, before
the write and again after it.

Every expected invalid input (missing or non-directory root, missing or invalid --out
parent, an unreadable or malformed attestation, an attested record, a changed file, a
link that escapes the unit, a special file, a nested Git root) and every OSError from a
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
from pathlib import Path
from typing import Literal

TRACKED = "tracked-record"
BULK = "attested-bulk"
PAYLOAD = "governed-payload"
ATTESTERS = frozenset({"operator", "MAESTRO"})
CHUNK = 1 << 20
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
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


Leaf = FileLeaf | LinkLeaf


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


def classify(leaves: list[Leaf], attested: list[Attested]) -> tuple[Row, ...]:
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
        if record_kind(leaf.path):
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


def link_escapes(rel: str, text: str) -> bool:
    if posixpath.isabs(text):
        return True
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
        fd = os.open(at.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=at.dir_fd)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise Refusal(f"{at.path!r} changed into a symlink before it was hashed") from exc
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            raise Refusal(f"{at.path!r} changed (gone) before it was hashed") from exc
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


def open_root(root: Path) -> int:
    try:
        return os.open(root, DIR_FLAGS)
    except OSError as exc:
        code = errno.errorcode.get(exc.errno, str(exc.errno))
        raise Refusal(f"unit root {root} is not a real directory: {code} {exc.strerror}") from exc


def scan(root_fd: int, root: str) -> list[Leaf]:
    leaves: list[Leaf] = []

    def walk(dir_fd: int, dirpath: str, prefix: str) -> None:
        with _fs(dirpath), os.scandir(dir_fd) as it:
            entries = sorted(it, key=lambda e: path_key(e.name))
        for entry in entries:
            rel = prefix + entry.name
            path = os.path.join(dirpath, entry.name)
            with _fs(path):
                est = entry.stat(follow_symlinks=False)
            if entry.name == ".git":
                raise Refusal(f"nested Git root at {rel!r}")
            if stat.S_ISLNK(est.st_mode):
                with _fs(path):
                    text = os.readlink(entry.name, dir_fd=dir_fd)
                if link_escapes(rel, text):
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
                    walk(fd, path, rel + "/")
                finally:
                    os.close(fd)
            elif stat.S_ISREG(est.st_mode):
                sha256, is_text = _digest(_At(dir_fd, entry.name, path, est))
                with _fs(path):
                    now = os.stat(entry.name, dir_fd=dir_fd, follow_symlinks=False)
                if _identity(now) != _identity(est):
                    raise Refusal(f"{rel!r} changed while it was hashed")
                leaves.append(FileLeaf(rel, est.st_size, sha256, is_text))
            else:
                raise Refusal(f"{rel!r} is a special file")

    walk(root_fd, root, "")
    return leaves


def load_attestation(path: Path) -> tuple[Attested, ...]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"{path}: unreadable attestation: {exc}") from exc
    return parse_attestation(doc, str(path))


def split_unit(root: Path, attestations: list[Path], root_fd: int | None = None) -> tuple[Row, ...]:
    """Classify the unit; root_fd, when given, is the caller's held fd of root."""
    attested = [a for p in attestations for a in load_attestation(p)]
    held = contextlib.nullcontext(root_fd) if root_fd is not None else _held_root(root)
    with held as fd:
        return classify(scan(fd, str(root)), attested)


@contextlib.contextmanager
def _held_root(root: Path):
    fd = open_root(root)
    try:
        yield fd
    finally:
        os.close(fd)


def render(root: Path, rows: tuple[Row, ...]) -> str:
    leaves = [{"path": r.path, "class": r.cls, "kind": r.kind, "size": r.size,
               "sha256": r.sha256, "link": r.link} for r in rows]
    return json.dumps({"root": str(root), "leaves": leaves}, indent=1, sort_keys=True) + "\n"


def _dir_realpath(fd: int) -> str:
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
    ap.add_argument("--root", required=True, type=Path, help="the unit directory (read only)")
    ap.add_argument("--attestation", action="append", default=[], type=Path)
    ap.add_argument("--out", required=True, type=Path, help="new JSON file outside the unit")
    args = ap.parse_args(argv)
    try:
        with _held_root(args.root) as root_fd:
            parent_fd = _open_out_parent(args.out)
            try:
                if _inside(_dir_realpath(root_fd), _dir_realpath(parent_fd)):
                    raise Refusal(f"--out {args.out} is inside the unit")
                rows = split_unit(args.root, args.attestation, root_fd)
                body = render(args.root, rows).encode("utf-8")
                with _fs(str(args.out)):
                    out_fd = os.open(args.out.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                     0o644, dir_fd=parent_fd)
                try:
                    with _fs(f"{args.out} (left in place, incomplete)"):
                        view = memoryview(body)
                        while view:
                            view = view[os.write(out_fd, view):]
                finally:
                    os.close(out_fd)
                parent_now = _dir_realpath(parent_fd)
                if _inside(_dir_realpath(root_fd), parent_now):
                    raise Refusal(f"wrote {os.path.join(parent_now, args.out.name)}, which is now inside "
                                  "the unit; it was left in place")
            finally:
                os.close(parent_fd)
    except Refusal as exc:
        print("record_split: refused: " + str(exc).replace("\n", "\\n"), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
