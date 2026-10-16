#!/usr/bin/env python3
"""Classify each leaf of one unit as tracked record, attested bulk or governed payload.

Read only on the unit. The durability rule is the attestation, never size, extension,
the old results/ folder or an ignore rule (A/SPEC.md:632-641, A/DESIGN.md:60-62):

- A leaf named, with its exact sha256, by an attestation of regenerable non-record
  output is attested bulk. Only an attestation can make a leaf bulk.
- Any other regular file whose bytes are UTF-8 text with no NUL byte is a tracked
  record (launch/check JSON, manifests, notebooks, logs), whatever its size.
- Any other regular file is a governed payload: ignored bytes kept with exact custody
  (sha256 and size), never anonymous bulk (OPEN-QUESTIONS.md Q8 default).
- A symlink is never followed. One whose text stays inside the unit is a tracked
  record of that text.

It refuses (exit 2, nothing written) on a changed or malformed attestation, a link that
escapes the unit, a special file, a nested Git root, or a file that changes while it is
hashed. It writes only the new --out file, outside the unit, and never overwrites it.

An attestation is one JSON record per run, written by the operator or by MAESTRO under
the operator's ruling (Q8):
  {"attested_by": "operator", "regenerate": "<command>",
   "leaves": [{"path": "<unit relpath>", "sha256": "<hex>"}, ...]}
"""
from __future__ import annotations

import argparse
import codecs
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
    if doc.get("attested_by") not in ATTESTERS:
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
        if a is not None:
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

def _digest(path: str) -> tuple[str, bool]:
    """sha256 of the bytes and whether they are NUL-free strict UTF-8."""
    h = hashlib.sha256()
    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    is_text = True
    with open(path, "rb", buffering=0) as fh:
        while chunk := fh.read(CHUNK):
            h.update(chunk)
            if is_text:
                try:
                    decoder.decode(chunk)
                    is_text = b"\0" not in chunk
                except UnicodeDecodeError:
                    is_text = False
    if is_text:
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            is_text = False
    return h.hexdigest(), is_text


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def scan(root: Path) -> list[Leaf]:
    st = os.lstat(root)
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
                sha256, is_text = _digest(entry.path)
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, type=Path, help="the unit directory (read only)")
    ap.add_argument("--attestation", action="append", default=[], type=Path)
    ap.add_argument("--out", required=True, type=Path, help="new JSON file outside the unit")
    args = ap.parse_args(argv)
    try:
        root_real = os.path.realpath(args.root)
        out_real = os.path.realpath(args.out)
        if os.path.commonpath([root_real, out_real]) == root_real:
            raise Refusal(f"--out {args.out} is inside the unit")
        rows = split_unit(args.root, args.attestation)
        with open(args.out, "x", encoding="utf-8") as fh:
            fh.write(render(args.root, rows))
    except (Refusal, FileExistsError) as exc:
        print(f"record_split: refused: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
