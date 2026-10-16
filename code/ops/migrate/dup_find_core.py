"""Classify each leaf of one unit manifest against reference manifests (ICM v2.1 Part 2, Step 216).

Pure core of dup_find (its I/O shell is Step 205). It makes no filesystem call, runs no process
and reads no clock or environment: it takes rows as values and returns rows as values.

Input: manifests exactly as code/ops/migrate/unit_manifest.py (Step 201) emits them,
{schema_version: 1, root, leaves: [LeafRecord], git_roots (optional, not read)}, and optional
toolkit hint rows {path, sha256}.

Output: one row per unit leaf, in the manifest's order (UTF-8 bytes of the relative path):
  {source, relpath, class, equal_to, differing_from, hint}
- equal_to: every reference leaf with the same content (same kind, byte count and sha256).
- differing_from: every reference leaf at the same relpath with other content.
- class: "equal" when equal_to is non-empty, else "differing" when differing_from is non-empty,
  else "unique".
- hint: the toolkit sha256 for this source and whether it agrees with the manifest, or null.

Comparison only (DESIGN.md:301: an equal file is a comparison result, not deletion permission):
no row carries an action. Toolkit sha256 values are hints; only the re-hashed manifest rows decide
the class (decision 9). Any malformed or ambiguous input is a fdsafe.Refusal; nothing is guessed.
Roots that overlap are refused, since a file would then be compared with itself.
"""
from __future__ import annotations

import posixpath
import re
from collections.abc import Mapping, Sequence

from ops.migrate import fdsafe

SHA_RE = re.compile(r"[0-9a-f]{64}")
KINDS = ("file", "symlink", "socket")
LEAF_KEYS = frozenset(("source", "kind", "bytes", "sha256", "link_text", "device", "inode", "nlink"))
MANIFEST_KEYS = frozenset(("schema_version", "root", "leaves"))
MANIFEST_OPTIONAL = frozenset(("git_roots",))
HINT_KEYS = frozenset(("path", "sha256"))


def _refuse(where: str, reason: str) -> None:
    raise fdsafe.Refusal(where, reason)


def _sequence(value, where: str) -> Sequence:
    if not isinstance(value, (list, tuple)):
        _refuse(where, f"expected a list, got {type(value).__name__}")
    return value


def _mapping(value, where: str) -> Mapping:
    if not isinstance(value, Mapping):
        _refuse(where, f"expected an object, got {type(value).__name__}")
    return value


def _keys(row: Mapping, required: frozenset, optional: frozenset, where: str) -> None:
    missing = required - row.keys()
    unknown = row.keys() - required - optional
    if missing:
        _refuse(where, f"missing field(s) {sorted(missing)}")
    if unknown:
        _refuse(where, f"unknown field(s) {sorted(map(str, unknown))}")


def _int(value, where: str, field: str, low: int) -> int:
    if type(value) is not int or value < low:
        _refuse(where, f"{field} must be an integer >= {low}, got {value!r}")
    return value


def _path(value, where: str, field: str) -> str:
    """An absolute, normalized, UTF-8 path string: compared as text, never resolved."""
    # normpath keeps a leading "//", so that is refused on its own.
    if (not isinstance(value, str) or not value.startswith("/") or value.startswith("//") or "\0" in value
            or posixpath.normpath(value) != value):
        _refuse(where, f"{field} must be an absolute normalized path, got {value!r}")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _refuse(where, f"{field} is not valid UTF-8: {value!r}")
    return value


def _sha(value, where: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        _refuse(where, f"sha256 must be 64 lowercase hex digits, got {value!r}")
    return value


def _under(path: str, root: str) -> bool:
    return path.startswith(root.rstrip("/") + "/")


def _relpath(source: str, root: str) -> str:
    return source[len(root.rstrip("/")) + 1:]


def _leaf(row, root: str, where: str) -> tuple[str, str, tuple]:
    """Return (source, relpath, content key) for one LeafRecord."""
    row = _mapping(row, where)
    if isinstance(row.get("source"), str):
        where = row["source"]
    _keys(row, LEAF_KEYS, frozenset(), where)
    source = _path(row["source"], where, "source")
    if not _under(source, root):
        _refuse(source, f"source is not inside the manifest root {root!r}")
    kind = row["kind"]
    if not isinstance(kind, str) or kind not in KINDS:
        _refuse(source, f"kind must be one of {list(KINDS)}, got {kind!r}")
    size = _int(row["bytes"], source, "bytes", 0)
    digest = _sha(row["sha256"], source)
    if kind == "symlink" and not isinstance(row["link_text"], str):
        _refuse(source, f"a symlink needs link_text, got {row['link_text']!r}")
    if kind != "symlink" and row["link_text"] is not None:
        _refuse(source, f"a {kind} carries no link_text, got {row['link_text']!r}")
    _int(row["device"], source, "device", 0)
    _int(row["inode"], source, "inode", 0)
    _int(row["nlink"], source, "nlink", 1)
    return source, _relpath(source, root), (kind, size, digest)


def _manifest(value, where: str) -> tuple[str, list[tuple[str, str, tuple]]]:
    """Return (root, [(source, relpath, content key)]) for one Step 201 manifest."""
    value = _mapping(value, where)
    _keys(value, MANIFEST_KEYS, MANIFEST_OPTIONAL, where)
    version = value["schema_version"]
    if type(version) is not int or version != 1:
        _refuse(where, f"schema_version must be 1, got {version!r}")
    root = _path(value["root"], where, "root")
    leaves = [_leaf(row, root, f"{where}.leaves[{i}]")
              for i, row in enumerate(_sequence(value["leaves"], f"{where}.leaves"))]
    seen: set[str] = set()
    for source, _, _ in leaves:
        if source in seen:
            _refuse(source, "source appears twice in one manifest")
        seen.add(source)
    return root, leaves


def _hints(rows) -> dict[str, str]:
    out: dict[str, str] = {}
    for i, row in enumerate(_sequence(rows, "hints")):
        where = f"hints[{i}]"
        row = _mapping(row, where)
        if isinstance(row.get("path"), str):
            where = row["path"]
        _keys(row, HINT_KEYS, frozenset(), where)
        path = _path(row["path"], where, "path")
        digest = _sha(row["sha256"], path)
        if path in out:
            _refuse(path, "path has more than one toolkit hint row")
        out[path] = digest
    return out


def _overlap(a: str, b: str) -> bool:
    return a == b or _under(a, b) or _under(b, a)


def classify(unit, references, hints=()) -> list[dict]:
    """Classify each leaf of the unit manifest as equal, differing or unique against the references."""
    unit_root, unit_leaves = _manifest(unit, "unit")
    refs = [_manifest(m, f"references[{i}]") for i, m in enumerate(_sequence(references, "references"))]
    if not refs:
        _refuse("references", "no reference manifest; nothing to compare against")
    roots = [unit_root]
    for root, _ in refs:
        if any(_overlap(root, other) for other in roots):
            _refuse(root, "manifest root overlaps another manifest root; a file would be compared with itself")
        roots.append(root)
    hint = _hints(hints)

    by_content: dict[tuple, list[str]] = {}
    by_relpath: dict[str, list[tuple[str, tuple]]] = {}
    for _, leaves in refs:
        for source, relpath, content in leaves:
            by_content.setdefault(content, []).append(source)
            by_relpath.setdefault(relpath, []).append((source, content))

    rows = []
    for source, relpath, content in sorted(unit_leaves, key=lambda leaf: leaf[1].encode("utf-8")):
        equal_to = sorted(by_content.get(content, ()), key=str.encode)
        differing_from = sorted((s for s, c in by_relpath.get(relpath, ()) if c != content), key=str.encode)
        cls = "equal" if equal_to else "differing" if differing_from else "unique"
        hinted = hint.get(source)
        rows.append({"source": source, "relpath": relpath, "class": cls, "equal_to": equal_to,
                     "differing_from": differing_from,
                     "hint": None if hinted is None else {"sha256": hinted, "agrees": hinted == content[2]}})
    return rows
