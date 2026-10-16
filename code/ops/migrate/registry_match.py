#!/usr/bin/env python3
"""Map a legacy unit to exactly one existing experiment ID, or to none (ICM v2.1 PLAN Step 206).

Read only. It reads three sources under --root and prints one JSON document:
program/registers/EXPERIMENT_REGISTRY.md, experiments/*/CONTEXT.md and _index/experiments.md.

An experiment ID exists only when an _index/experiments.md row or a CONTEXT.md frontmatter
`id:` names it. A folder name is never an ID, and an ID seen only in a path is never
promoted to one (SPEC.md:161, DESIGN.md:254, DESIGN.md:548). Doubt gives "none" or
"ambiguous", so the caller falls back to the unit's exact V target. A missing, linked or
undecodable source is a refusal (exit 2), never an empty match.
"""
from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

REGISTRY = "program/registers/EXPERIMENT_REGISTRY.md"
INDEX = "_index/experiments.md"
EXPERIMENTS = "experiments"
RECORD = "CONTEXT.md"

ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
TOKEN_RE = re.compile(r"[A-Za-z0-9_.-]+")
# A unit is one name or one fnmatch family pattern (`autoresearch_*`), never a path.
UNIT_RE = re.compile(r"[A-Za-z0-9_.*?-]+")
# `experiments/<id>/` at the start of a path. `_archive/experiments/...` is not a current record.
EXP_REF_RE = re.compile(r"(?<![A-Za-z0-9_./-])experiments/([A-Za-z0-9_.-]+)/")

Result = Literal["exact", "ambiguous", "none"]


class Refusal(Exception):
    """The sources or the unit leave doubt; nothing is matched."""


@dataclass(frozen=True)
class Line:
    number: int
    text: str
    owner: str | None  # the record this line belongs to: an index row ID or a frontmatter ID


@dataclass(frozen=True)
class Source:
    rel: str
    lines: tuple[Line, ...]


@dataclass(frozen=True)
class Evidence:
    source: str
    line: int
    text: str
    experiment_ids: tuple[str, ...]


@dataclass(frozen=True)
class Match:
    unit: str
    result: Result
    experiment_id: str | None  # set only when result == "exact"
    candidates: tuple[str, ...]
    unknown: tuple[str, ...]  # candidates that no index row or frontmatter names
    evidence: tuple[Evidence, ...]


# ---- pure core -------------------------------------------------------------------------

def index_lines(text: str) -> tuple[Line, ...]:
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        owner = None
        if raw.lstrip().startswith("|"):
            first = raw.strip().strip("|").split("|")[0].strip()
            if first != "id" and ID_RE.fullmatch(first):
                owner = first
        out.append(Line(n, raw, owner))
    return tuple(out)


def frontmatter_id(rel: str, text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for raw in lines[1:]:
        if raw.strip() == "---":
            return None
        key, sep, value = raw.partition(":")
        if sep and key.strip() == "id":
            value = value.strip()
            if value in ("", "null", "~"):
                return None
            if not ID_RE.fullmatch(value):
                raise Refusal(f"{rel}: frontmatter id {value!r} is not a plain experiment id")
            return value
    raise Refusal(f"{rel}: frontmatter is not closed")


def record_lines(rel: str, text: str) -> tuple[Line, ...]:
    owner = frontmatter_id(rel, text)
    return tuple(Line(n, raw, owner) for n, raw in enumerate(text.splitlines(), 1))


def plain_lines(text: str) -> tuple[Line, ...]:
    return tuple(Line(n, raw, None) for n, raw in enumerate(text.splitlines(), 1))


def known_ids(sources: tuple[Source, ...]) -> frozenset[str]:
    return frozenset(line.owner for src in sources for line in src.lines if line.owner)


def check_unit(unit: str) -> str:
    if not UNIT_RE.fullmatch(unit) or not unit.strip("."):
        raise Refusal(f"unit {unit!r} is not a legacy unit name or family pattern")
    return unit


def find_evidence(sources: tuple[Source, ...], unit: str) -> tuple[Evidence, ...]:
    out = []
    for src in sources:
        for line in src.lines:
            if not any(fnmatch.fnmatchcase(tok, unit) for tok in TOKEN_RE.findall(line.text)):
                continue
            ids = set(EXP_REF_RE.findall(line.text))
            if line.owner:
                ids.add(line.owner)
            out.append(Evidence(src.rel, line.number, line.text, tuple(sorted(ids))))
    return tuple(out)


def decide(unit: str, evidence: tuple[Evidence, ...], known: frozenset[str]) -> Match:
    candidates = tuple(sorted({i for e in evidence for i in e.experiment_ids}))
    unknown = tuple(i for i in candidates if i not in known)
    if len(candidates) > 1:
        result: Result = "ambiguous"
    elif len(candidates) == 1 and not unknown:
        result = "exact"
    else:
        result = "none"
    chosen = candidates[0] if result == "exact" else None
    return Match(unit, result, chosen, candidates, unknown, evidence)


# ---- read-only edge --------------------------------------------------------------------

def _no_link_path(root: Path, rel: str) -> Path:
    path = root
    for part in Path(rel).parts:
        path = path / part
        try:
            st = os.lstat(path)
        except FileNotFoundError:
            raise Refusal(f"{rel}: missing under {root}") from None
        if stat.S_ISLNK(st.st_mode):
            raise Refusal(f"{os.path.relpath(path, root)}: is a symbolic link; links are not followed")
    real_root = os.path.realpath(root)
    if os.path.commonpath([real_root, os.path.realpath(path)]) != real_root:
        raise Refusal(f"{rel}: escapes the root")
    return path


def _read(root: Path, rel: str) -> str:
    path = _no_link_path(root, rel)
    if not stat.S_ISREG(os.lstat(path).st_mode):
        raise Refusal(f"{rel}: not a regular file")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as fh:
        data = fh.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal(f"{rel}: not UTF-8 ({exc})") from None


def load_sources(root: Path) -> tuple[Source, ...]:
    root = Path(root)
    if not root.is_dir():
        raise Refusal(f"root {root} is not a directory")
    sources = [
        Source(REGISTRY, plain_lines(_read(root, REGISTRY))),
        Source(INDEX, index_lines(_read(root, INDEX))),
    ]
    experiments = _no_link_path(root, EXPERIMENTS)
    for entry in sorted(os.scandir(experiments), key=lambda e: e.name):
        rel = f"{EXPERIMENTS}/{entry.name}"
        if entry.is_symlink():
            raise Refusal(f"{rel}: is a symbolic link; links are not followed")
        if not entry.is_dir(follow_symlinks=False):
            continue
        record = f"{rel}/{RECORD}"
        if not os.path.lexists(root / record):
            continue
        sources.append(Source(record, record_lines(record, _read(root, record))))
    return tuple(sources)


def match_unit(root: Path, unit: str) -> Match:
    unit = check_unit(unit)
    sources = load_sources(root)
    return decide(unit, find_evidence(sources, unit), known_ids(sources))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="repo root that holds the three sources")
    ap.add_argument("--unit", required=True, action="append",
                    help="legacy unit name or fnmatch family pattern; repeatable")
    args = ap.parse_args(argv)
    try:
        units = [check_unit(u) for u in args.unit]
        sources = load_sources(Path(args.root))
    except Refusal as exc:
        print(f"registry_match: refused: {exc}", file=sys.stderr)
        return 2
    known = known_ids(sources)
    matches = [dataclasses.asdict(decide(u, find_evidence(sources, u), known)) for u in units]
    print(json.dumps({"root": str(args.root), "matches": matches}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
