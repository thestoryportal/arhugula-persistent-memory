#!/usr/bin/env python3
"""Report drift, cross-unit duplicates, target conflicts and capacity across every phase 5 unit
(ICM v2.1 Part 2, Step 271: the I/O shell over ledger_db_core, Step 272).

Read only. It reads the inputs, the toolkit database and free disk space, and passes them to
ledger_db_core.compute as values. It never moves, overwrites or deletes anything. Its DuckDB database
is in memory and is never written to disk; the toolkit database is attached READ_ONLY. Neither is an
authority: the Step 201 manifests and the annex rows stay the source of truth.

  ledger_db.py --plans PLANS.json --requirements ANNEX.tsv [--requirements ...]
               --toolkit-db TOOLKIT.duckdb --free-root LABEL=PATH [--free-root ...]
               [--floor-bytes N] --out DIR

Inputs:
  --plans         {"entries": [{"id", "replaces", "moves": [{"source", "target"}], "manifest": absolute
                  path of the entry's Step 201 manifest, "manifest_sha256": sha256 of its bytes}, ...]}.
                  Other entry fields are ignored. The manifest's bytes must have that digest; its
                  "leaves" (schema_version 1) are the entry's leaves.
  --requirements  annex TSVs (MOVE-REQUIREMENTS and amendment 1): a header with requirement_id, source
                  and action, then one row per requirement.
  --toolkit-db    the toolkit DuckDB file; inventory(abspath, sha256) gives the toolkit rows.
  --free-root     a destination root; its free bytes are f_bavail * f_frsize of the held root, and a
                  leaf whose manifest device is the root's st_dev moves to it by a rename (no bytes).
  --floor-bytes   bytes each root must keep free (default 20 GiB, the disk floor).
Outputs: DIR (created; it must not exist and must lie outside every free root) holds drift.tsv,
cross_unit_dups.tsv, targets.tsv and capacity.tsv, the core's rows under its column headers.
A target exists when a no-follow lstat finds it; an existing directory target is walked, so each
existing path under it is also an existing target.

Every walk, read, create, close and F_GETPATH goes through fdsafe; any other filesystem call runs
inside fdsafe.fs. DuckDB opens the toolkit file by path; the shell checks before the attach that it is
a regular file (a FIFO would block DuckDB) and after the query that its lstat is unchanged.

Exit 0: targets.tsv and capacity.tsv have no rows. Exit 1: either has a row.
Exit 2: a refusal (unreadable or malformed input, a plans file with no entries, a raced object):
one line naming the path and the errno, nothing written unless the line names a kept output.
"""
from __future__ import annotations

import argparse
import contextlib
import errno
import hashlib
import json
import os
import re
import stat
import sys
from collections.abc import Mapping

import duckdb

from ops.migrate import fdsafe, ledger_db_core

Refusal = fdsafe.Refusal

REPORTS = (("drift.tsv", ledger_db_core.DRIFT_COLUMNS, "drift"),
           ("cross_unit_dups.tsv", ledger_db_core.DUP_COLUMNS, "cross_unit_dups"),
           ("targets.tsv", ledger_db_core.TARGET_COLUMNS, "targets"),
           ("capacity.tsv", ledger_db_core.CAPACITY_COLUMNS, "capacity"))
ANNEX_COLUMNS = ("requirement_id", "source", "action")
FLOOR_BYTES = 20 * (1 << 30)
SHA256_HEX = frozenset("0123456789abcdef")
SURROGATE = re.compile("[\ud800-\udfff]")  # a lone surrogate (JSON \u escapes allow one) has no UTF-8 form


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def _read(path: str) -> bytes:
    """The bytes of one named regular file, read through its held parent."""
    with fdsafe.hold_root(os.path.dirname(path)) as parent:
        return fdsafe.read_named(parent, os.path.basename(path))


def _text(data: bytes, path: str) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal(path, f"is not UTF-8 ({exc.reason} at byte {exc.start})") from None


def _json(data: bytes, path: str):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Refusal(path, f"duplicate JSON key {key!r}")
            out[key] = value
        return out

    def constant(name):
        raise Refusal(path, f"holds the non-JSON constant {name}")
    try:
        doc = json.loads(_text(data, path), object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        raise Refusal(path, f"is not JSON ({exc.msg} at line {exc.lineno} column {exc.colno})") from None
    pending = [doc]
    while pending:
        item = pending.pop()
        if isinstance(item, str) and SURROGATE.search(item):
            raise Refusal(path, f"holds the string {item!r}, which has no UTF-8 form")
        pending.extend(item.values() if isinstance(item, dict) else item if isinstance(item, list) else ())
    return doc


def _annex(path: str) -> list:
    text = _text(_read(path), path)
    if "\r" in text or not text.endswith("\n"):
        raise Refusal(path, "needs LF line ends and a final newline")
    header, *lines = text[:-1].split("\n")
    columns = header.split("\t")
    if len(set(columns)) != len(columns) or not set(ANNEX_COLUMNS) <= set(columns):
        raise Refusal(path, f"header needs distinct columns including {', '.join(ANNEX_COLUMNS)}")
    if not lines:
        raise Refusal(path, "has no rows")
    rows = []
    for number, line in enumerate(lines, 2):
        fields = line.split("\t")
        if len(fields) != len(columns):
            raise Refusal(path, f"row {number} has {len(fields)} fields, the header {len(columns)}")
        rows.append(dict(zip(columns, fields)))
    return rows


def _manifest_path(value, where: str, plans: str) -> str:
    if not isinstance(value, str) or not value.startswith("/") or os.path.normpath(value) != value:
        raise Refusal(plans, f"{where}: expected an absolute normalized manifest path")
    return value


def _leaves(entry: Mapping, where: str, plans: str) -> list:
    for key in ("manifest", "manifest_sha256"):
        if key not in entry:
            raise Refusal(plans, f"{where}: missing field {key}")
    if "leaves" in entry:
        raise Refusal(plans, f"{where}: leaves come from the manifest, not the plans file")
    path = _manifest_path(entry["manifest"], f"{where}.manifest", plans)
    digest = entry["manifest_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or not set(digest) <= SHA256_HEX:
        raise Refusal(plans, f"{where}.manifest_sha256: expected a lowercase hex sha256")
    data = _read(path)
    actual = hashlib.sha256(data).hexdigest()
    if actual != digest:
        raise Refusal(path, f"sha256 {actual} is not the plan's {digest}")
    doc = _json(data, path)
    if not isinstance(doc, Mapping) or doc.get("schema_version") != 1 or type(doc["schema_version"]) is not int:
        raise Refusal(path, "is not a schema_version 1 manifest")
    leaves = doc.get("leaves")
    if not isinstance(leaves, list):
        raise Refusal(path, "has no leaves list")
    for i, leaf in enumerate(leaves):
        if not isinstance(leaf, Mapping) or not isinstance(leaf.get("source"), str) or \
                type(leaf.get("device")) is not int:
            raise Refusal(path, f"leaves[{i}]: expected an object with a source string and a device integer")
    return leaves


def _plans(path: str) -> list:
    doc = _json(_read(path), path)
    if not isinstance(doc, Mapping) or not isinstance(doc.get("entries"), list):
        raise Refusal(path, 'expected {"entries": [...]}')
    entries = []
    for i, entry in enumerate(doc["entries"]):
        if not isinstance(entry, Mapping):
            raise Refusal(path, f"entries[{i}]: expected an object")
        fields = {k: v for k, v in entry.items() if k not in ("manifest", "manifest_sha256")}
        entries.append({**fields, "leaves": _leaves(entry, f"entries[{i}]", path)})
    return entries


def _free_roots(specs: list, stack: contextlib.ExitStack, written: list) -> list:
    """Each free root held: (Dir, st_dev, free bytes). The ExitStack closes them."""
    roots, labels = [], set()
    for spec in specs:
        label, sep, path = spec.partition("=")
        if not sep or not label or not path:
            raise Refusal(spec, "expected --free-root LABEL=PATH")
        if label in labels:
            raise Refusal(spec, f"duplicate free root label {label}")
        labels.add(label)
        held = fdsafe.hold_root(path)
        stack.callback(lambda d=held: fdsafe.close(d.fd, d.path if not written else
                                                     f"{d.path}; {written[0]} (written, left in place)"))
        if any(held.path == other.path for other, _, _ in roots):
            raise Refusal(held.path, "is given as two free roots")
        with fdsafe.fs(held.path):
            dev = os.fstat(held.fd).st_dev
        with fdsafe.fs(held.path):
            vfs = os.statvfs(held.fd)
        roots.append((held, dev, vfs.f_bavail * vfs.f_frsize))
    return roots


@contextlib.contextmanager
def _duck(path: str):
    try:
        yield
    except duckdb.Error as exc:
        raise Refusal(path, str(exc).splitlines()[0]) from None


def _lstat_at(parent: fdsafe.Dir, name: str, path: str) -> os.stat_result:
    with fdsafe.fs(path):
        return os.lstat(name, dir_fd=parent.fd)


def _toolkit_rows(path: str) -> list:
    """inventory(abspath, sha256) from the toolkit file, attached READ_ONLY to an in-memory database."""
    name = os.path.basename(path)
    with fdsafe.hold_root(os.path.dirname(path)) as parent:
        given = os.path.join(parent.path, name)
        before = _lstat_at(parent, name, given)
        if not stat.S_ISREG(before.st_mode):
            raise Refusal(given, "is not a regular file")
        con = duckdb.connect(":memory:")
        try:
            with _duck(given):
                con.execute("ATTACH '" + given.replace("'", "''") + "' AS toolkit (READ_ONLY)")
                rows = con.execute("SELECT abspath, sha256 FROM toolkit.inventory").fetchall()
        finally:
            con.close()
        after = _lstat_at(parent, name, given)
        if _identity(after) != _identity(before) or not stat.S_ISREG(after.st_mode):
            raise Refusal(given, "changed while DuckDB read it")
        if parent.live() != parent.path:
            raise Refusal(given, f"its directory moved while DuckDB read it (now {parent.live()})")
    return rows


def _existing(entries: list) -> set:
    """Every move target that exists, and every path under an existing directory target."""
    found = set()
    for target in sorted({m["target"] for e in entries for m in e["moves"]}):
        try:
            with fdsafe.fs(target):
                st = os.lstat(target)
        except Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            continue
        found.add(target)
        if stat.S_ISDIR(st.st_mode):
            with fdsafe.hold_root(target) as held:
                fdsafe.walk(held, lambda entry: found.add(f"{target}/{entry.rel}"))
    return found


def _cell(value, path: str) -> bytes:
    text = "" if value is None else str(value)
    if "\t" in text or "\n" in text or "\r" in text:
        raise Refusal(path, f"value {text!r} holds a tab or line break; TSV cannot carry it")
    return text.encode("utf-8", "strict")


def _render(name: str, columns: tuple, rows: tuple, out: str) -> bytes:
    path = os.path.join(out, name)
    return b"".join(b"\t".join(_cell(v, path) for v in row) + b"\n" for row in (columns, *rows))


def run(args) -> int:
    written: list = []
    with contextlib.ExitStack() as stack:
        roots = _free_roots(args.free_root, stack, written)
        annex = [row for path in args.requirements for row in _annex(path)]
        entries = _plans(args.plans)
        toolkit = _toolkit_rows(args.toolkit_db)
        values = dict(annex_rows=annex, toolkit_rows=toolkit, floor_bytes=args.floor_bytes,
                      free_bytes={held.path: free for held, _, free in roots},
                      same_filesystem={(leaf["source"], held.path): leaf["device"] == dev
                                       for e in entries for leaf in e["leaves"] for held, dev, _ in roots})
        ledger_db_core.compute(entries=entries, existing_targets=(), **values)
        reports = ledger_db_core.compute(entries=entries, existing_targets=_existing(entries), **values)
        for held, _, _ in roots:
            if held.live() != held.path:
                raise Refusal(held.path, f"is held at {held.live()}; the root moved during the run")
        with fdsafe.fs(args.out):
            parent_path = os.path.realpath(os.path.dirname(os.path.abspath(args.out)))
        out = os.path.join(parent_path, os.path.basename(args.out))
        datas = [(name, _render(name, columns, getattr(reports, field), out)) for name, columns, field in REPORTS]
        parent = fdsafe.open_out_parent(parent_path)
        stack.callback(fdsafe.close, parent.fd, parent.path)
        for held, _, _ in roots:
            if fdsafe.inside(held.live(), parent.live()):
                raise Refusal(held.path, f"--out {out} lies inside this free root")
        outdir = fdsafe.mkdir(parent, os.path.basename(out))
        written.append(outdir.path)
        stack.callback(fdsafe.close, outdir.fd, f"{outdir.path} (written, left in place)")
        lines = []
        for (name, data), (_, _, field) in zip(datas, REPORTS):
            where = fdsafe.create_file(outdir, name, data, [held for held, _, _ in roots])
            lines.append(f"{where}\t{len(getattr(reports, field))}")
        if outdir.live() != outdir.path:
            raise Refusal(outdir.path, f"moved to {outdir.live()} during the write; its reports are left in place")
    print("\n".join(lines))
    return 1 if reports.targets or reports.capacity else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plans", required=True)
    parser.add_argument("--requirements", required=True, action="append")
    parser.add_argument("--toolkit-db", required=True)
    parser.add_argument("--free-root", required=True, action="append")
    parser.add_argument("--floor-bytes", type=int, default=FLOOR_BYTES)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        return run(args)
    except Refusal as exc:
        print(f"ledger_db: refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
