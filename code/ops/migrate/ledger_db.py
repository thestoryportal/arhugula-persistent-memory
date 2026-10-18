#!/usr/bin/env python3
"""Report drift, cross-unit duplicates, target conflicts and capacity across every phase 5 unit
(ICM v2.1 Part 2, Step 271: the I/O shell over ledger_db_core, Step 272).

Read only. It reads the inputs, the toolkit database and free disk space, and passes them to
ledger_db_core.compute as values. It never moves, overwrites or deletes anything but its own reports
(see _write). Its DuckDB database is in memory and is never written to disk; the toolkit database is
attached READ_ONLY. Neither is an authority: the Step 201 manifests and the annex rows stay the source
of truth.

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
Outputs: DIR (created; it must not exist and must lie outside every move source, move target and free
root) holds drift.tsv, cross_unit_dups.tsv, targets.tsv and capacity.tsv, the core's rows under its
column headers. A target exists when a no-follow lstat finds it; an existing directory target is
walked, so each existing path under it is also an existing target.

Every raw string (each CLI argument, and each path or label read from the plans file, the manifests
and the annexes) passes one parse step (_label, _path) before any other use: it refuses a NUL, a
string with no UTF-8 form, a tab, CR or LF, and, for a path, one that is not absolute and normalized.
A CLI path may be relative; the parse step makes it absolute once, from the working directory.

Every walk, read, create, close and F_GETPATH goes through fdsafe; any other filesystem call runs
inside fdsafe.fs. DuckDB opens the toolkit file by path; the shell checks before the attach that it is
a regular file (a FIFO would block DuckDB), holds it (no-follow) and its parent, and keeps a kqueue
vnode watch on both from before the ATTACH until after the DETACH: any event is a refusal, as is a
changed lstat after the query. A move source or target is looked up through its held parent, never by
a path that could follow a link; one that exists is held and known by its (st_dev, st_ino), as is
each free root, and --out may not have any of them among its own and its ancestors' identities.

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
import select
import stat
import sys
from collections.abc import Mapping
from typing import NamedTuple, NewType

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
# A lone surrogate has no UTF-8 form: a JSON \u escape can make one, and so can a byte that is not UTF-8
# in argv or in a walked name (Python decodes those with surrogateescape).
SURROGATE = re.compile("[\ud800-\udfff]")
# LeafRecord fields beyond source and device, with their wire types (A-icm21/WIRE-CONTRACTS.md:91-92).
LEAF_FIELDS = (("kind", (str,)), ("bytes", (int,)), ("sha256", (str,)), ("link_text", (str, type(None))),
               ("inode", (int,)), ("nlink", (int,)))
WATCH = select.KQ_EV_ADD | select.KQ_EV_CLEAR
FILE_NOTES = (select.KQ_NOTE_DELETE | select.KQ_NOTE_RENAME | select.KQ_NOTE_WRITE | select.KQ_NOTE_LINK
              | select.KQ_NOTE_REVOKE)
PARENT_NOTES = select.KQ_NOTE_WRITE | select.KQ_NOTE_DELETE | select.KQ_NOTE_RENAME
UNIT = "lies inside, or is, this move source or target"
ROOT = "lies inside this free root"

# [LAW:parse-dont-validate] The stamps of the one parse step: code past it takes these, never raw strings.
Label = NewType("Label", str)      # strict UTF-8 text with no NUL, tab, CR or LF
AbsPath = NewType("AbsPath", str)  # a Label that is an absolute, normalized path


class Inputs(NamedTuple):
    """Every CLI string, parsed: nothing past _inputs reads argv."""
    plans: AbsPath
    requirements: tuple
    toolkit: AbsPath
    free_roots: tuple  # (Label, AbsPath) pairs, the labels distinct
    floor_bytes: int
    out: AbsPath


class Fence(NamedTuple):
    """A place --out may not lie in. ident is the held (st_dev, st_ino) of an object that exists: a link
    alias or a rename leaves it unchanged. It is None for a path where nothing exists; that path is
    compared as parsed, and its existing ancestors were held link-free when it was looked up."""
    path: str
    ident: tuple | None
    says: str


class Root(NamedTuple):
    held: fdsafe.Dir
    dev: int
    free: int
    fence: Fence


class Unit(NamedTuple):
    """A move source or target as found; held is its directory fd when it is an existing directory."""
    fence: Fence
    held: fdsafe.Dir | None


def _identity(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def _node(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino)


def _label(value, source: str, field: str, carry: str = "") -> Label:
    """[LAW:single-enforcer] The one parse step for a raw string: refused, naming its source and field,
    unless it is a string a TSV report can carry. carry names the reports that could hold the value."""
    at = f"{source} {field}{carry}"
    if not isinstance(value, str):
        raise Refusal(at, f"{field}: expected a string, got {type(value).__name__}")
    if "\0" in value:
        raise Refusal(at, f"{field}: value {value!r} holds a NUL")
    if SURROGATE.search(value):
        raise Refusal(at, f"{field}: value {value!r} has no UTF-8 form (a lone surrogate)")
    if "\t" in value or "\n" in value or "\r" in value:
        raise Refusal(at, f"{field}: value {value!r} holds a tab or line break; TSV cannot carry it")
    return Label(value)


def _path(value, source: str, field: str, carry: str = "") -> AbsPath:
    text = _label(value, source, field, carry)
    if os.path.normpath("/" + text.lstrip("/")) != text:  # relative, '.', '..', '//' or a trailing '/'
        raise Refusal(f"{source} {field}{carry}", f"{field}: {text!r} is not an absolute normalized path")
    return AbsPath(text)


def _cli_path(value: str, flag: str) -> AbsPath:
    """A CLI path, made absolute once, here, from the working directory, then parsed."""
    with fdsafe.fs(flag):
        cwd = os.getcwd()
    return _path(os.path.join(cwd, value), flag, "path")


def _given(value, parse, source: str, field: str, carry: str = ""):
    """value parsed when it is a string; ledger_db_core owns the shapes and refuses any other type."""
    return parse(value, source, field, carry) if isinstance(value, str) else value


def _each(value, parse):
    return [parse(item, j) for j, item in enumerate(value)] if isinstance(value, list) else value


def _move(move, source: str, at: str, carry: str):
    keys = ("source", "target")
    return {k: _given(move[k], _path, source, f"{at}.{k}", carry) for k in keys if k in move} \
        if isinstance(move, Mapping) else move


def _inputs(ns: argparse.Namespace) -> Inputs:
    free_roots, labels = [], set()
    for spec in ns.free_root:
        label, sep, path = _label(spec, "--free-root", "LABEL=PATH").partition("=")
        if not sep or not label or not path:
            raise Refusal(spec, "expected --free-root LABEL=PATH")
        if label in labels:
            raise Refusal(spec, f"duplicate free root label {label}")
        labels.add(label)
        free_roots.append((Label(label), _cli_path(path, "--free-root")))
    return Inputs(_cli_path(ns.plans, "--plans"), tuple(_cli_path(p, "--requirements") for p in ns.requirements),
                  _cli_path(ns.toolkit_db, "--toolkit-db"), tuple(free_roots), ns.floor_bytes,
                  _cli_path(ns.out, "--out"))


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
    def integer(token):
        # [LAW:one-source-of-truth] Match move_plan_core's interpreter-owned digit limit.
        digits, limit = len(token.lstrip("-")), sys.get_int_max_str_digits()
        if 0 < limit < digits:
            raise Refusal(path, f"holds an integer of {digits} digits, over the interpreter limit of {limit}")
        return int(token)

    text = _text(data, path)
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant, parse_int=integer)
    except json.JSONDecodeError as exc:
        raise Refusal(path, f"is not JSON ({exc.msg} at line {exc.lineno} column {exc.colno})") from None
    except RecursionError:
        raise Refusal(path, "nests too deeply") from None


def _annex(path: AbsPath) -> list:
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
        row = dict(zip(columns, fields))
        rows.append({"requirement_id": _label(row["requirement_id"], path, f"row {number} requirement_id"),
                     "source": _path(row["source"], path, f"row {number} source"),
                     "action": _label(row["action"], path, f"row {number} action")})
    return rows


def _leaves(entry: Mapping, at: str, plans: AbsPath, carry: str) -> list:
    for key in ("manifest", "manifest_sha256"):
        if key not in entry:
            raise Refusal(plans, f"{at}: missing field {key}")
    if "leaves" in entry:
        raise Refusal(plans, f"{at}: leaves come from the manifest, not the plans file")
    path = _path(entry["manifest"], plans, f"{at}.manifest")
    digest = _label(entry["manifest_sha256"], plans, f"{at}.manifest_sha256")
    if len(digest) != 64 or not set(digest) <= SHA256_HEX:
        raise Refusal(plans, f"{at}.manifest_sha256: expected a lowercase hex sha256")
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
    parsed = []
    for i, leaf in enumerate(leaves):
        if not isinstance(leaf, Mapping) or type(leaf.get("device")) is not int:
            raise Refusal(path, f"leaves[{i}]: expected an object with a device integer")
        source = _path(leaf.get("source"), path, f"leaves[{i}].source", carry)
        for field, kinds in LEAF_FIELDS:
            if field not in leaf or type(leaf[field]) not in kinds:
                raise Refusal(path, f"leaves[{i}] ({source!r}).{field}: missing or not "
                                    f"{' or '.join(k.__name__ for k in kinds)} (LeafRecord, WIRE-CONTRACTS.md:91)")
        parsed.append({"source": source, "device": leaf["device"], "bytes": leaf["bytes"], "inode": leaf["inode"],
                       "nlink": leaf["nlink"], "kind": _label(leaf["kind"], path, f"leaves[{i}].kind"),
                       "sha256": _label(leaf["sha256"], path, f"leaves[{i}].sha256", carry),
                       "link_text": _given(leaf["link_text"], _label, path, f"leaves[{i}].link_text")})
    return parsed


def _plans(path: AbsPath, carry: str) -> list:
    """Each entry: the fields the core reads (id, replaces, moves), every string in them parsed, and its
    manifest's parsed leaves. A missing field stays missing and a wrong shape stays as given: the core
    refuses both."""
    doc = _json(_read(path), path)
    if not isinstance(doc, Mapping) or not isinstance(doc.get("entries"), list):
        raise Refusal(path, 'expected {"entries": [...]}')
    entries = []
    for i, entry in enumerate(doc["entries"]):
        if not isinstance(entry, Mapping):
            raise Refusal(path, f"entries[{i}]: expected an object")
        at = f"entries[{i}]"
        parse = {"id": lambda v: _given(v, _label, path, f"{at}.id", carry),
                 "replaces": lambda v: _each(v, lambda r, j: _given(r, _label, path, f"{at}.replaces[{j}]")),
                 "moves": lambda v: _each(v, lambda m, j: _move(m, path, f"{at}.moves[{j}]", carry))}
        fields = {key: parse[key](entry[key]) for key in parse if key in entry}
        entries.append({**fields, "leaves": _leaves(entry, at, path, carry)})
    return entries


def _close_later(stack: contextlib.ExitStack, held: fdsafe.Dir, written: list) -> None:
    """Close a held directory when the run ends; once a report is written, a failed close names it."""
    stack.callback(lambda: fdsafe.close(held.fd, held.path if not written else
                                        f"{held.path}; {written[0]} (written, left in place)"))


def _free_roots(specs: tuple, stack: contextlib.ExitStack, written: list) -> list:
    """Each free root held, with its st_dev, its free bytes and its fence. The ExitStack closes them."""
    roots = []
    for _, path in specs:
        held = fdsafe.hold_root(path)
        _close_later(stack, held, written)
        with fdsafe.fs(held.path):
            st = os.fstat(held.fd)
        if any(_node(st) == root.fence.ident for root in roots):
            raise Refusal(held.path, "is given as two free roots")
        with fdsafe.fs(held.path):
            vfs = os.statvfs(held.fd)
        roots.append(Root(held, st.st_dev, vfs.f_bavail * vfs.f_frsize, Fence(held.path, _node(st), ROOT)))
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


def _close_watch(kq, label: str) -> None:
    with fdsafe.fs(label):
        kq.close()


def _toolkit_rows(path: str) -> list:
    """inventory(abspath, sha256) from the toolkit file, attached READ_ONLY to an in-memory database.

    DuckDB opens the file by path, so the shell holds the file and its parent and watches both with
    kqueue from before the ATTACH until after the DETACH: a swap and restore inside that window is an
    event. A swap or move before the watch starts shows in the lstat and live-path checks after it."""
    name = os.path.basename(path)
    with fdsafe.hold_root(os.path.dirname(path)) as parent, contextlib.ExitStack() as stack:
        given = os.path.join(parent.path, name)
        before = _lstat_at(parent, name, given)
        if not stat.S_ISREG(before.st_mode):
            raise Refusal(given, "is not a regular file")
        with fdsafe.fs(given):
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent.fd)
        stack.callback(fdsafe.close, fd, given)
        with fdsafe.fs(given):
            opened = os.fstat(fd)
            kq = select.kqueue()
        stack.callback(_close_watch, kq, given)
        if _identity(opened) != _identity(before):
            raise Refusal(given, "changed between its check and its open")
        with fdsafe.fs(given):
            kq.control([select.kevent(fd, select.KQ_FILTER_VNODE, WATCH, FILE_NOTES),
                        select.kevent(parent.fd, select.KQ_FILTER_VNODE, WATCH, PARENT_NOTES)], 0, 0)
        with _duck(given):
            con = duckdb.connect(":memory:")
            try:
                con.execute("ATTACH '" + given.replace("'", "''") + "' AS toolkit (READ_ONLY)")
                rows = con.execute("SELECT abspath, sha256 FROM toolkit.inventory").fetchall()
                con.execute("DETACH toolkit")
            finally:
                con.close()
        with fdsafe.fs(given):
            events = kq.control(None, 8, 0)
        if events:
            raise Refusal(given, "changed while DuckDB read it (kqueue: "
                                 + ", ".join(f"fd {e.ident} fflags {e.fflags:#x}" for e in events) + ")")
        after = _lstat_at(parent, name, given)
        if _identity(after) != _identity(before) or not stat.S_ISREG(after.st_mode):
            raise Refusal(given, "changed while DuckDB read it")
        if parent.live() != parent.path:
            raise Refusal(given, f"its directory moved while DuckDB read it (now {parent.live()})")
    return rows


def _lookup(target: str):
    """The no-follow lstat of an absolute path, made through its held parent; None when it is absent.

    The parent is held by fdsafe.hold_root, which refuses a path with a link in it. When the parent
    is missing (ENOENT), the lookup climbs to the nearest ancestor that hold_root can hold, so no
    existing component above it is a link, and lstats the next component through that held fd: it must
    be absent too (ENOENT). Anything there now (a dangling link, or a component that appeared) refuses."""
    path, name = os.path.split(target)
    while True:
        try:
            anc = fdsafe.hold_root(path)
        except Refusal as exc:
            if exc.errno == errno.ENOENT:
                path, name = os.path.split(path)
                continue
            raise Refusal(target, f"its directory cannot be held ({exc})", exc.errno) from None
        break
    with anc:
        try:
            with fdsafe.fs(target):
                st = os.lstat(name, dir_fd=anc.fd)
        except Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            st = None
        if anc.live() != anc.path:
            raise Refusal(target, f"its directory {anc.path} moved during the lookup (now {anc.live()})")
    if st is not None and os.path.join(anc.path, name) != target:
        raise Refusal(target, f"{os.path.join(anc.path, name)} exists, but the path below it could not be "
                              "opened: a component is a link or changed during the lookup")
    return st


def _unit(path: AbsPath, stack: contextlib.ExitStack, written: list) -> Unit:
    """[LAW:one-source-of-truth] A move source or target as it is now: an existing directory is held for
    the whole run, so its (st_dev, st_ino) stays the unit's identity wherever it is moved."""
    st = _lookup(path)
    if st is None:
        return Unit(Fence(path, None, UNIT), None)
    if not stat.S_ISDIR(st.st_mode):
        return Unit(Fence(path, _node(st), UNIT), None)
    held = fdsafe.hold_root(path)
    _close_later(stack, held, written)
    with fdsafe.fs(path):
        now = os.fstat(held.fd)
    if _node(now) != _node(st):
        raise Refusal(path, "changed between its stat and its walk or hold")
    return Unit(Fence(path, _node(st), UNIT), held)


def _existing(targets: set, units: dict) -> set:
    """Every move target that exists, and every path under an existing directory target."""
    found = {target for target in targets if units[target].fence.ident is not None}
    for target in sorted(t for t in targets if units[t].held is not None):
        tdir = units[target].held

        def visit(entry, target=target):
            _label(entry.rel, target, "(a name walked under this existing target)")
            found.add(f"{target}/{entry.rel}")
        fdsafe.walk(tdir, visit)
        if tdir.live() != tdir.path:
            raise Refusal(target, f"was rebound during the walk (the walked directory is now {tdir.live()})")
    return found


def _ancestry(held: fdsafe.Dir) -> frozenset:
    """(st_dev, st_ino) of the held directory and of each directory above it, up to '/', reached through
    '..' from the held fd: what the directory is inside now, whatever path names it."""
    ids, up = [], "."
    with fdsafe.fs(held.path):
        st = os.stat(up, dir_fd=held.fd)
        while _node(st) not in ids:  # '/' is its own '..'
            ids.append(_node(st))
            up += "/.."
            st = os.stat(up, dir_fd=held.fd)
    return frozenset(ids)


def _occupant(path: str) -> frozenset:
    """The identity of what exists at path now (none when nothing does)."""
    st = _lookup(path)
    return frozenset([_node(st)] if st is not None else [])


def _hit(ids: frozenset, live: str, fences: list) -> Fence | None:
    """[LAW:one-source-of-truth] The fence that --out, live at `live` with the identities ids, lies in, or
    None: the one containment test, for the refusal and for the exit removal alike."""
    return next((f for f in fences if (f.ident in ids if f.ident else fdsafe.inside(f.path, live))), None)


def _refuse_inside(ids: frozenset, live: str, fences: list, attempted: list) -> None:
    """Refuse when --out, live at `live` with the identities ids, lies in a fence. The reports attempted so
    far are removed by _write's exit callback, the one remover, as this refusal leaves the write owner."""
    hit = _hit(ids, live, fences)
    if hit is not None:
        raise Refusal(hit.path, f"--out {live} {hit.says}" + "".join(f"; removed {name}" for name in attempted))


@contextlib.contextmanager
def _report_parent(report: fdsafe.Held):
    """Bind the current name to the held file before checking or removing it."""
    label = os.path.join(report.parent.path, report.name)
    live = fdsafe.live_path(report.fd, label)
    path, name = os.path.split(live)
    with fdsafe.hold_root(path) as parent:
        with fdsafe.fs(live):
            held = os.fstat(report.fd)
            entry = os.stat(name, dir_fd=parent.fd, follow_symlinks=False)
        if _node(entry) != _node(held):
            raise Refusal(live, "is not the held report; removal refused")
        yield parent, name


def _exit_removal(outdir: fdsafe.Dir, fences: list, attempted: list, reports: list):
    """[LAW:single-enforcer] One exit owner for removal and all report closes."""
    def remove(exc_type, exc, tb) -> bool:
        with contextlib.ExitStack() as closes:
            for report in reports:
                closes.callback(fdsafe.close, report.fd,
                                f"{os.path.join(outdir.path, report.name)} (created, left in place)")
            # [LAW:no-silent-failure] A failed check leaves removal selected and propagates
            # after the finally block; no exception class or traceback is replaced.
            remove_all = exc is not None
            try:
                if exc is not None:
                    hit = _hit(_ancestry(outdir), outdir.live(), fences)
                    for report in reports:
                        with _report_parent(report) as (parent, name):
                            hit = hit or _hit(_ancestry(parent), parent.live(), fences)
                    remove_all = hit is not None
            finally:
                if remove_all:
                    held_names = {report.name for report in reports}
                    for report in reports:
                        with _report_parent(report) as (parent, name):
                            with fdsafe.fs(f"{os.path.join(parent.path, name)} (its removal failed, left in place)"):
                                os.unlink(name, dir_fd=parent.fd)
                    fenced = (outdir.live(), "containment failed")
                    present = _names(outdir, fenced)
                    for name in (n for n in attempted if n not in held_names and n in present):
                        with fdsafe.fs(f"{os.path.join(fenced[0], name)} (its removal failed, left in place)"):
                            os.unlink(name, dir_fd=outdir.fd)
        return False
    return remove


def _names(held: fdsafe.Dir, fenced: tuple) -> set:
    """The names in the held --out now, read so that only attempted reports that exist are removed."""
    with fdsafe.fs(f"{fenced[0]} ({fenced[1]}; its reports could not be listed for removal, left in place)"):
        return set(os.listdir(held.fd))


def _render(columns: tuple, rows: tuple) -> bytes:
    # Each string here is a parsed input, a parsed walked name or a sha256 the core checked as hex: strict
    # UTF-8 with no tab or line break, so nothing is re-checked here [LAW:parse-dont-validate].
    return b"".join(b"\t".join(("" if v is None else str(v)).encode("utf-8", "strict") for v in row) + b"\n"
                    for row in (columns, *rows))


def _write(parent: fdsafe.Dir, name: str, reports: list, roots: list, fences: list,
           stack: contextlib.ExitStack, written: list) -> list:
    """[LAW:single-enforcer] The one writer of the reports: the directory parent/name, then each report in it.

    Before the mkdir and before each create, --out's identities (the held directory and each ancestor,
    and before the mkdir what is at its name) must meet no fence: no held move source, move target or
    free root, and no absent unit path. After the last create the check runs once more. Whatever exception
    leaves the run after the mkdir (a failed check, a create, write or close that fails, a create that
    fdsafe refuses after the file exists), the exit callback (_exit_removal) checks --out afresh and, when
    it lies in a fence or that cannot be proved, removes each report attempted, by name through the held
    directory fd. A name is attempted before its create starts, so a report made by a create that then
    raises is removed too.
    [LAW:comments-carry-meaning] Residual (ruling 3): a rename that lands between a check and the
    create after it cannot be prevented from user space without a lock; the next check, or the one
    after the last create, and the removal close its effect, not the window. The removal runs on every
    exit by exception, so an exception between a create and its record no longer leaves a report.
    Each completed report stays held through its own live-parent after-check; the exit callback
    removes moved reports by their verified live names before closing the held descriptors."""
    out = os.path.join(parent.live(), name)
    _refuse_inside(_ancestry(parent) | _occupant(out), out, fences, [])
    outdir = fdsafe.mkdir(parent, name)
    written.append(outdir.path)
    stack.callback(fdsafe.close, outdir.fd, f"{outdir.path} (written, left in place)")
    attempted, lines, held_reports = [], [], []
    # Pushed after the close above, so it runs before it, while the held fd is open.
    stack.push(_exit_removal(outdir, fences, attempted, held_reports))
    for report, data in reports:
        _refuse_inside(_ancestry(outdir), outdir.live(), fences, attempted)
        attempted.append(report)
        held = fdsafe.create_held(outdir, report, data, [root.held for root in roots])
        held_reports.append(held)
        lines.append(fdsafe.settle(held, [root.held for root in roots]))
    _refuse_inside(_ancestry(outdir), outdir.live(), fences, attempted)
    # [LAW:single-enforcer] Each file may move independently of --out.
    for held in held_reports:
        with _report_parent(held) as (parent, report):
            _refuse_inside(_ancestry(parent), parent.live(), fences, attempted)
    if outdir.live() != outdir.path:
        raise Refusal(outdir.path, f"moved to {outdir.live()} during the write; its reports are left in place")
    return lines


def run(inputs: Inputs) -> int:
    written: list = []
    carry = " (a value for " + ", ".join(os.path.join(inputs.out, name) for name, _, _ in REPORTS) + ")"
    with contextlib.ExitStack() as stack:
        roots = _free_roots(inputs.free_roots, stack, written)
        annex = [row for path in inputs.requirements for row in _annex(path)]
        entries = _plans(inputs.plans, carry)
        toolkit = _toolkit_rows(inputs.toolkit)
        values = dict(annex_rows=annex, toolkit_rows=toolkit, floor_bytes=inputs.floor_bytes,
                      free_bytes={root.held.path: root.free for root in roots},
                      same_filesystem={(leaf["source"], root.held.path): leaf["device"] == root.dev
                                       for e in entries for leaf in e["leaves"] for root in roots})
        ledger_db_core.compute(entries=entries, existing_targets=(), **values)
        units = {path: _unit(path, stack, written)
                 for path in sorted({p for e in entries for m in e["moves"] for p in (m["source"], m["target"])})}
        targets = {m["target"] for e in entries for m in e["moves"]}
        reports = ledger_db_core.compute(entries=entries, existing_targets=_existing(targets, units), **values)
        for root in roots:
            if root.held.live() != root.held.path:
                raise Refusal(root.held.path, f"is held at {root.held.live()}; the root moved during the run")
        with fdsafe.fs(inputs.out):
            parent_path = os.path.realpath(os.path.dirname(inputs.out))
        parent = fdsafe.open_out_parent(parent_path)
        stack.callback(fdsafe.close, parent.fd, parent.path)
        fences = [unit.fence for unit in units.values()] + [root.fence for root in roots]
        datas = [(name, _render(columns, getattr(reports, field))) for name, columns, field in REPORTS]
        lines = [f"{where}\t{len(getattr(reports, field))}" for where, (_, _, field) in
                 zip(_write(parent, os.path.basename(inputs.out), datas, roots, fences, stack, written), REPORTS)]
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
        return run(_inputs(args))
    except Refusal as exc:
        print(f"ledger_db: refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
