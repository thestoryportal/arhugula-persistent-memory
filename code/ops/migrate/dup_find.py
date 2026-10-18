#!/usr/bin/env python3
"""Report equal, differing and unique files of one unit against reference manifests (ICM v2.1 Part 2, Step 205).

I/O shell of dup_find_core (Step 216), which holds all the comparison logic. It reads the Step 201
manifests (unit_manifest.py output) through fdsafe and, when --toolkit-db is given, the toolkit
migration.duckdb opened READ_ONLY, passes their rows to dup_find_core.classify and prints the core's
rows unchanged as one canonical JSON line on stdout. Comparison only: it emits no delete, purge or
skip action, and it writes no file.

- A manifest is read with fdsafe.read_named through its held parent directory, so no link is followed
  and the bytes come from the object scanned. It must be UTF-8 JSON with no duplicate key.
- DuckDB opens the database by path, so the tool cannot bind that open to an fd. It detects a swap
  instead: the file must be a regular file seen through its held parent before the read, and a fresh
  no-follow lstat of the path after the read must show the same (st_dev, st_ino, st_size, st_mtime_ns).
- Hint rows are the inventory table's {path: abspath, sha256}; a row with a null sha256 has no hash to
  hint and is not passed. Hints never change a class (the core decides from re-hashed manifest rows).

Exit 0: stdout is the core's rows. Exit 2: a refusal (fdsafe.Refusal from the shell or the core), one
line on stderr naming the path (and the errno name for a filesystem error); or a malformed invocation.
Any other exception propagates with its traceback.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys

import duckdb

from ops.migrate import dup_find_core, fdsafe

HINT_QUERY = "SELECT abspath, sha256 FROM inventory WHERE sha256 IS NOT NULL ORDER BY abspath"


def _split(path: str) -> tuple[str, str]:
    with fdsafe.fs(path):
        given = os.path.abspath(path)
    return os.path.split(given)


def _object(path: str, pairs: list) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise fdsafe.Refusal(path, f"duplicate key {key!r}")
        out[key] = value
    return out


def read_manifest(path: str):
    """Return one manifest document, read through its held parent directory."""
    parent, name = _split(path)
    with fdsafe.hold_root(parent) as held:
        data = fdsafe.read_named(held, name)
    given = os.path.join(parent, name)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=lambda pairs: _object(given, pairs))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise fdsafe.Refusal(given, f"is not UTF-8 JSON: {exc}") from exc


def read_hints(path: str) -> list[dict]:
    """Return the toolkit's {path, sha256} hint rows from migration.duckdb, opened READ_ONLY."""
    parent, name = _split(path)
    given = os.path.join(parent, name)
    with fdsafe.hold_root(parent) as held:
        with fdsafe.fs(given):
            before = os.lstat(name, dir_fd=held.fd)
        if not stat.S_ISREG(before.st_mode):
            raise fdsafe.Refusal(given, "is not a regular file")
        try:
            with duckdb.connect(given, read_only=True) as con:
                rows = con.execute(HINT_QUERY).fetchall()
        except duckdb.Error as exc:
            raise fdsafe.Refusal(given, f"DuckDB: {str(exc).splitlines()[0]}") from exc
        with fdsafe.fs(given):
            after = os.lstat(given)
        if fdsafe._identity(after) != fdsafe._identity(before):
            raise fdsafe.Refusal(given, "changed while DuckDB read it")
    return [{"path": p, "sha256": s} for p, s in rows]


def run(unit: str, references: list[str], toolkit_db: str | None) -> list[dict]:
    hints = [] if toolkit_db is None else read_hints(toolkit_db)
    return dup_find_core.classify(read_manifest(unit), [read_manifest(p) for p in references], hints)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--unit", required=True, help="Step 201 manifest of the unit")
    parser.add_argument("--reference", required=True, action="append", help="Step 201 manifest to compare with (repeat)")
    parser.add_argument("--toolkit-db", help="toolkit migration.duckdb (opened READ_ONLY) for sha256 hints")
    args = parser.parse_args(argv)
    try:
        rows = run(args.unit, args.reference, args.toolkit_db)
    except fdsafe.Refusal as exc:
        print(exc, file=sys.stderr)
        return 2
    print(json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
