"""The four ledger_db reports, computed from given rows and numbers (ICM v2.1 Part 2, Step 272).

Pure core of Step 271 (ledger_db, the I/O shell): no filesystem call, no DuckDB, no subprocess, no clock
and no environment read. It takes rows as Python values and returns the rows of four reports, or raises
fdsafe.Refusal on malformed input. It is never an authority: the Step 201 manifests and the annex rows
stay the source of truth.

Inputs (compute's keyword arguments):
  entries          plan entries, at least one: {"id", "replaces": [MV id], "moves": [{"source", "target"}],
                   "leaves": [Step 201 LeafRecord]}. A leaf's target comes from the entry's move with the
                   longest source that equals the leaf or contains it (an exact file move wins), with the
                   leaf's path below that source appended to the move target. Each move source lies at or
                   under the source of a HOLD annex row the entry replaces (SPEC.md:605, admitted roots).
  annex_rows       MOVE-REQUIREMENTS rows: {"requirement_id", "source", "action", ...}.
  toolkit_rows     (source, sha256 or None) pairs from the toolkit inventory.
  existing_targets the target paths the shell observed as existing.
  free_bytes       {destination root: free bytes}. A target's root is the longest root containing it.
  floor_bytes      bytes each root must keep free (the disk floor).
  same_filesystem  {(leaf source, destination root): bool}: True when moving the leaf is a rename.

Reports (rows are tuples of the *_COLUMNS fields, sorted):
  drift            each leaf whose sha256 differs from the toolkit's at its source ("drift"), each leaf the
                   toolkit never listed ("toolkit-missing") and each toolkit row with a null sha256
                   ("toolkit-no-hash"). Informational: the toolkit predates ICM v2.
  cross_unit_dups  regular files whose sha256 group spans more than one entry. Informational.
  targets          "collision" (two leaves with one target, SPEC.md:646), "target-exists" (a leaf or move
                   target that already exists, SPEC.md:605), "unassigned" (a manifest leaf no entry moves)
                   and "multi-assigned" (a leaf more than one entry moves).
  capacity         each root whose received bytes (all entries summed; same-filesystem renames cost none)
                   exceed its free bytes minus the floor.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

from ops.migrate import fdsafe

Refusal = fdsafe.Refusal

DRIFT_COLUMNS = ("status", "entry", "source", "fresh_sha256", "toolkit_sha256")
DUP_COLUMNS = ("sha256", "bytes", "entry", "source")
TARGET_COLUMNS = ("kind", "entry", "source", "target")
CAPACITY_COLUMNS = ("root", "needed_bytes", "free_bytes", "floor_bytes", "budget_bytes")

LEAF_KINDS = frozenset({"file", "symlink", "socket"})
SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class Reports:
    drift: tuple
    cross_unit_dups: tuple
    targets: tuple
    capacity: tuple


@dataclass(frozen=True)
class Leaf:
    entry: str
    source: str
    kind: str
    size: int
    sha256: str


@dataclass(frozen=True)
class Move:
    source: str
    target: str
    where: str


@dataclass(frozen=True)
class Entry:
    id: str
    moves: tuple
    leaves: tuple


@dataclass(frozen=True)
class Assignment:
    entry: str
    leaf: Leaf
    target: str


def _refuse(where: str, reason: str):
    raise Refusal(where, reason)


def _seq(value, where: str) -> list:
    if isinstance(value, (str, bytes, Mapping)) or not isinstance(value, (list, tuple)):
        _refuse(where, f"expected a list, got {type(value).__name__}")
    return list(value)


def _map(value, where: str) -> Mapping:
    if not isinstance(value, Mapping):
        _refuse(where, f"expected a mapping, got {type(value).__name__}")
    return value


def _field(row: Mapping, key: str, where: str):
    if key not in row:
        _refuse(f"{where}.{key}", "missing field")
    return row[key]


def _text(value, where: str) -> str:
    if not isinstance(value, str) or not value:
        _refuse(where, "expected a non-empty string")
    return value


def _count(value, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _refuse(where, "expected a non-negative integer")
    return value


def _sha(value, where: str) -> str:
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        _refuse(where, "expected a lowercase hex sha256")
    return value


def _path(value, where: str) -> str:
    """An absolute, normalized path: no empty, '.' or '..' segment, no trailing slash, no NUL."""
    if not isinstance(value, str) or not value.startswith("/") or "\0" in value or \
            any(seg in ("", ".", "..") for seg in value[1:].split("/")):
        _refuse(where, "expected an absolute normalized path")
    return value


def _under(path: str, base: str) -> bool:
    return path == base or path.startswith(base + "/")


def _ancestors(path: str):
    """path itself, then each parent, longest first ('/' excluded)."""
    while path:
        yield path
        path = path[:path.rfind("/")]


def _annex(rows) -> dict:
    out = {}
    for i, row in enumerate(_seq(rows, "annex_rows")):
        where = f"annex_rows[{i}]"
        row = _map(row, where)
        rid = _text(_field(row, "requirement_id", where), f"{where}.requirement_id")
        source = _path(_field(row, "source", where), f"{where}.source")
        action = _text(_field(row, "action", where), f"{where}.action")
        if rid in out:
            _refuse(f"{where}.requirement_id", f"duplicate requirement {rid}")
        out[rid] = (source, action)
    return out


def _entries(value, annex: dict) -> list:
    raw = _seq(value, "entries")
    if not raw:
        _refuse("entries", "the plans document has no entries (never an empty PASS)")
    entries, ids, sources = [], set(), set()
    for i, row in enumerate(raw):
        where = f"entries[{i}]"
        row = _map(row, where)
        eid = _text(_field(row, "id", where), f"{where}.id")
        if eid in ids:
            _refuse(f"{where}.id", f"duplicate entry {eid}")
        ids.add(eid)
        replaces = _seq(_field(row, "replaces", where), f"{where}.replaces")
        if not replaces:
            _refuse(f"{where}.replaces", "an entry names the MV rows it replaces")
        admitted = []
        for j, rid in enumerate(replaces):
            rwhere = f"{where}.replaces[{j}]"
            if _text(rid, rwhere) not in annex:
                _refuse(rwhere, f"no annex row {rid}")
            source, action = annex[rid]
            if action != "HOLD":
                _refuse(rwhere, f"{rid} is {action}, not HOLD")
            admitted.append(source)
        moves_raw = _seq(_field(row, "moves", where), f"{where}.moves")
        if not moves_raw:
            _refuse(f"{where}.moves", "an entry moves at least one source")
        moves, move_sources = [], set()
        for j, move in enumerate(moves_raw):
            mwhere = f"{where}.moves[{j}]"
            move = _map(move, mwhere)
            source = _path(_field(move, "source", mwhere), f"{mwhere}.source")
            target = _path(_field(move, "target", mwhere), f"{mwhere}.target")
            if not any(_under(source, base) for base in admitted):
                _refuse(f"{mwhere}.source", "source is not at or under a HOLD row this entry replaces")
            if source in move_sources:
                _refuse(f"{mwhere}.source", "duplicate move source in one entry")
            move_sources.add(source)
            moves.append(Move(source, target, f"{mwhere}.target"))
        leaves = []
        for j, leaf in enumerate(_seq(_field(row, "leaves", where), f"{where}.leaves")):
            lwhere = f"{where}.leaves[{j}]"
            leaf = _map(leaf, lwhere)
            source = _path(_field(leaf, "source", lwhere), f"{lwhere}.source")
            kind = _field(leaf, "kind", lwhere)
            if not isinstance(kind, str) or kind not in LEAF_KINDS:
                _refuse(f"{lwhere}.kind", f"unknown leaf kind {kind!r}")
            size = _count(_field(leaf, "bytes", lwhere), f"{lwhere}.bytes")
            sha = _sha(_field(leaf, "sha256", lwhere), f"{lwhere}.sha256")
            if source in sources:
                _refuse(f"{lwhere}.source", "leaf listed by two manifests")
            sources.add(source)
            leaves.append(Leaf(eid, source, kind, size, sha))
        entries.append(Entry(eid, tuple(moves), tuple(leaves)))
    return entries


def _toolkit(rows) -> dict:
    out = {}
    for i, row in enumerate(_seq(rows, "toolkit_rows")):
        where = f"toolkit_rows[{i}]"
        if isinstance(row, str) or not isinstance(row, (list, tuple)) or len(row) != 2:
            _refuse(where, "expected a (source, sha256 or None) pair")
        source = _path(row[0], f"{where}.source")
        sha = None if row[1] is None else _sha(row[1], f"{where}.sha256")
        if source in out:
            _refuse(f"{where}.source", "duplicate toolkit source")
        out[source] = sha
    return out


def _existing(value) -> frozenset:
    if isinstance(value, (str, bytes, Mapping)) or not isinstance(value, (list, tuple, set, frozenset)):
        _refuse("existing_targets", f"expected a collection of paths, got {type(value).__name__}")
    return frozenset(_path(p, f"existing_targets[{i}]") for i, p in enumerate(value))


def _free(value) -> dict:
    roots = _map(value, "free_bytes")
    return {_path(root, f"free_bytes[{root!r}]"): _count(free, f"free_bytes[{root!r}]") for root, free in roots.items()}


def _same_fs(value) -> Mapping:
    same = _map(value, "same_filesystem")
    for key, flag in same.items():
        where = f"same_filesystem[{key!r}]"
        if not (isinstance(key, tuple) and len(key) == 2) or not isinstance(flag, bool):
            _refuse(where, "expected (leaf source, root) -> bool")
        _path(key[0], where)
        _path(key[1], where)
    return same


def _root(path: str, roots: dict) -> str | None:
    return next((p for p in _ancestors(path) if p in roots), None)


def _assign(entries: list) -> tuple[list, list]:
    """Each leaf's target in each entry that moves it, and the leaves no entry moves."""
    leaves = [leaf for e in entries for leaf in e.leaves]
    by_entry = [(e.id, {m.source: m.target for m in e.moves}) for e in entries]
    assigned, unassigned = [], []
    for leaf in leaves:
        hits = []
        for eid, moves in by_entry:
            source = next((p for p in _ancestors(leaf.source) if p in moves), None)
            if source is not None:
                hits.append(Assignment(eid, leaf, moves[source] + leaf.source[len(source):]))
        assigned.extend(hits)
        if not hits:
            unassigned.append(leaf)
    return assigned, unassigned


def _drift(entries: list, toolkit: dict) -> tuple:
    rows = []
    for leaf in (leaf for e in entries for leaf in e.leaves):
        if leaf.source not in toolkit:
            rows.append(("toolkit-missing", leaf.entry, leaf.source, leaf.sha256, ""))
        elif toolkit[leaf.source] is None:
            rows.append(("toolkit-no-hash", leaf.entry, leaf.source, leaf.sha256, ""))
        elif toolkit[leaf.source] != leaf.sha256:
            rows.append(("drift", leaf.entry, leaf.source, leaf.sha256, toolkit[leaf.source]))
    return tuple(sorted(rows))


def _dups(entries: list) -> tuple:
    groups: dict = {}
    for leaf in (leaf for e in entries for leaf in e.leaves if leaf.kind == "file"):
        groups.setdefault(leaf.sha256, []).append(leaf)
    rows = [(sha, leaf.size, leaf.entry, leaf.source)
            for sha, members in groups.items() if len({m.entry for m in members}) > 1 for leaf in members]
    return tuple(sorted(rows))


def _targets(entries: list, assigned: list, unassigned: list, existing: frozenset) -> tuple:
    rows = set()
    by_target: dict = {}
    for a in assigned:
        by_target.setdefault(a.target, []).append(a)
    for target, hits in by_target.items():
        if len({a.leaf.source for a in hits}) > 1:
            rows.update(("collision", a.entry, a.leaf.source, target) for a in hits)
    for a in assigned:
        if a.target in existing:
            rows.add(("target-exists", a.entry, a.leaf.source, a.target))
    for e in entries:
        rows.update(("target-exists", e.id, m.source, m.target) for m in e.moves if m.target in existing)
    by_leaf: dict = {}
    for a in assigned:
        by_leaf.setdefault(a.leaf.source, []).append(a)
    for hits in by_leaf.values():
        if len(hits) > 1:
            rows.update(("multi-assigned", a.entry, a.leaf.source, a.target) for a in hits)
    rows.update(("unassigned", leaf.entry, leaf.source, "") for leaf in unassigned)
    return tuple(sorted(rows))


def _capacity(assigned: list, free: dict, floor: int, same: Mapping) -> tuple:
    needed: dict = {}
    for a in assigned:
        root = _root(a.target, free)
        key = (a.leaf.source, root)
        if key not in same:
            _refuse(f"same_filesystem[{key!r}]", "missing: is this move a rename?")
        needed[root] = needed.get(root, 0) + (0 if same[key] else a.leaf.size)
    rows = [(root, need, free[root], floor, free[root] - floor)
            for root, need in needed.items() if need > free[root] - floor]
    return tuple(sorted(rows))


def compute(*, entries, annex_rows, toolkit_rows, existing_targets, free_bytes, floor_bytes,
            same_filesystem) -> Reports:
    """The four reports, or Refusal on malformed input. Inputs are read, never changed."""
    annex = _annex(annex_rows)
    plan = _entries(entries, annex)
    toolkit = _toolkit(toolkit_rows)
    existing = _existing(existing_targets)
    free = _free(free_bytes)
    floor = _count(floor_bytes, "floor_bytes")
    same = _same_fs(same_filesystem)
    for e in plan:
        for m in e.moves:
            if _root(m.target, free) is None:
                _refuse(m.where, "target lies under no destination root in free_bytes")
    assigned, unassigned = _assign(plan)
    return Reports(drift=_drift(plan, toolkit), cross_unit_dups=_dups(plan),
                   targets=_targets(plan, assigned, unassigned, existing),
                   capacity=_capacity(assigned, free, floor, same))
