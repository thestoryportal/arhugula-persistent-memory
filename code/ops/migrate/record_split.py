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

Each file is read through one fd opened without following links; its fstat must match
the scan's lstat before and after the read, so size and hash come from one object. The
--out file is created through an fd of its parent directory, checked outside the unit
before the write and again after it.

Every expected invalid input (missing or non-directory root, missing or invalid --out
parent, an unreadable or malformed attestation, an attested record, a changed file, a
link that escapes the unit, a special file, a nested Git root) exits 2 with one refusal
line. It never overwrites and never deletes: an output that lands inside the unit after
a race is refused by name and left in place.

An attestation is one JSON record per run, written by the operator or by MAESTRO under
the operator's ruling (Q8):
  {"attested_by": "operator", "regenerate": "<command>",
   "leaves": [{"path": "<unit relpath>", "sha256": "<hex>"}, ...]}
"""
from __future__ import annotations

import argparse
import codecs
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

def _digest(entry: os.DirEntry) -> tuple[str, bool]:
    """sha256 of the leaf's bytes and whether they are NUL-free strict UTF-8.

    The bytes come from one fd whose fstat equals the scan's (cached) lstat before and
    after the read."""
    scanned = _identity(entry.stat(follow_symlinks=False))
    try:
        fd = os.open(entry.path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise Refusal(f"{entry.path!r} changed into a symlink before it was hashed") from exc
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            raise Refusal(f"{entry.path!r} changed (gone) before it was hashed") from exc
        raise
    with open(fd, "rb", buffering=0) as fh:
        if _identity(os.fstat(fd)) != scanned:
            raise Refusal(f"{entry.path!r} changed before it was hashed")
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
            raise Refusal(f"{entry.path!r} changed while it was hashed")
    if is_text:
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            is_text = False
    return h.hexdigest(), is_text


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def scan(root: Path) -> list[Leaf]:
    try:
        st = os.lstat(root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise Refusal(f"unit root {root} does not exist") from exc
    if not stat.S_ISDIR(st.st_mode):
        raise Refusal(f"unit root {root} is not a real directory")
    leaves: list[Leaf] = []

    def walk(dirpath: str, prefix: str) -> None:
        with os.scandir(dirpath) as it:
            entries = sorted(it, key=lambda e: path_key(e.name))
        for entry in entries:
            rel = prefix + entry.name
            est = entry.stat(follow_symlinks=False)
            if entry.name == ".git":
                raise Refusal(f"nested Git root at {rel!r}")
            if stat.S_ISLNK(est.st_mode):
                text = os.readlink(entry.path)
                if link_escapes(rel, text):
                    raise Refusal(f"link {rel!r} -> {text!r} escapes the unit")
                leaves.append(LinkLeaf(rel, text))
            elif stat.S_ISDIR(est.st_mode):
                walk(entry.path, rel + "/")
            elif stat.S_ISREG(est.st_mode):
                sha256, is_text = _digest(entry)
                if _identity(os.lstat(entry.path)) != _identity(est):
                    raise Refusal(f"{rel!r} changed while it was hashed")
                leaves.append(FileLeaf(rel, est.st_size, sha256, is_text))
            else:
                raise Refusal(f"{rel!r} is a special file")

    walk(str(root), "")
    return leaves


def load_attestation(path: Path) -> tuple[Attested, ...]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"{path}: unreadable attestation: {exc}") from exc
    return parse_attestation(doc, str(path))


def split_unit(root: Path, attestations: list[Path]) -> tuple[Row, ...]:
    attested = [a for p in attestations for a in load_attestation(p)]
    return classify(scan(Path(root)), attested)


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
        raise Refusal(f"--out parent {out.parent} is not a usable directory: {exc.strerror}") from exc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, type=Path, help="the unit directory (read only)")
    ap.add_argument("--attestation", action="append", default=[], type=Path)
    ap.add_argument("--out", required=True, type=Path, help="new JSON file outside the unit")
    args = ap.parse_args(argv)
    try:
        root_real = os.path.realpath(args.root)
        parent_fd = _open_out_parent(args.out)
        try:
            if _inside(root_real, _dir_realpath(parent_fd)):
                raise Refusal(f"--out {args.out} is inside the unit")
            rows = split_unit(args.root, args.attestation)
            out_fd = os.open(args.out.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o644, dir_fd=parent_fd)
            with open(out_fd, "w", encoding="utf-8") as fh:
                fh.write(render(args.root, rows))
            parent_now = _dir_realpath(parent_fd)
            if _inside(root_real, parent_now):
                raise Refusal(f"wrote {os.path.join(parent_now, args.out.name)}, which is now inside "
                              "the unit; it was left in place")
        finally:
            os.close(parent_fd)
    except (Refusal, FileExistsError) as exc:
        print(f"record_split: refused: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
