#!/usr/bin/env python3
"""Build one dry-run unit plan, or check the repairs rows or a producer route table (ICM v2.1 Part 2, Step 209).

I/O shell of move_plan_core (Step 217), which holds all the plan and check logic. Dry run only: it moves
nothing, creates no file and runs no Git or other process. Every input file is read with fdsafe.read_named
through its held parent directory, so no link is followed and the bytes come from the object scanned; each
directory it holds must be its own real path.

  plan --entry ID --root DIR --requirements FILE... --units FILE
      Prints move_plan_core.build_plan's plan unchanged, as one canonical JSON line. --units is a JSON list
      with one object per unit: {"requirement_id", "manifest" (Step 201 manifest), "registry" (Step 206
      registry_match output holding exactly one match), "readers" (Step 207 reader_find report),
      "comparison" (Step 205 dup_find output, or null when no comparison was made), "candidate" (a path
      below experiments/<id>/, or null)}. The target paths the core may choose are observed with a no-follow
      lstat until every target of the plan has been observed; the plan is built from that observation.
  check-plans --root DIR --plans FILE --repairs FILE --readers FILE...
      --plans is {"entries": [...]}. Each stale row of each reader_find report becomes an occurrence with
      the text of its line, read from the reader file below --root. Prints move_plan_core.check_plans's
      findings.
  check-routes --routes FILE --source DIR --hold-target PATH
      The children are the entries of the held --source directory. Prints move_plan_core.check_routes's
      findings.

Exit 0: the plan, or no finding ("[]"). Exit 1: one or more findings, printed as one canonical JSON list.
Exit 2: a refusal (fdsafe.Refusal from the shell or the core), one line on stderr naming the path (and the
errno name for a filesystem error); or a malformed invocation. Any other exception propagates.
"""
from __future__ import annotations

import argparse
import contextlib
import errno
import json
import os
import posixpath
import re
import stat
import sys
from dataclasses import dataclass
from typing import Callable

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as core
from ops.migrate.unit_manifest import canonical

Refusal = fdsafe.Refusal
UNSAFE = re.compile(r"[\x00\t\n\r\ud800-\udfff]")
LONE = re.compile(r"[\ud800-\udfff]")
UNIT_KEYS = frozenset(("requirement_id", "manifest", "registry", "readers", "comparison", "candidate"))
STALE_KEYS = frozenset(("file", "line", "old_text", "old"))


# --- parse: each raw string becomes a checked value once [LAW:parse-dont-validate] [LAW:single-enforcer]

def _string_at(where: str, value) -> str:
    """A string with no NUL, tab, CR, LF or lone surrogate; a refusal names where it came from."""
    if not isinstance(value, str):
        raise Refusal(where, f"expected a string, got {value!r}")
    if UNSAFE.search(value):
        raise Refusal(where, f"{value!r} holds a NUL, tab, CR, LF or lone surrogate")
    return value


def _path_at(where: str, value) -> str:
    """A path the shell opens: a non-empty normalized string; a relative one is read from the cwd."""
    _string_at(where, value)
    if not value or posixpath.normpath(value) != value or value.startswith("//"):
        raise Refusal(where, f"{value!r} is not a normalized path")
    return value


def _reader_name(where: str, value) -> str:
    """A reader file named by a report: a normalized path below --root."""
    path = _path_at(where, value)
    if path.startswith("/") or path == ".." or path.startswith("../"):
        raise Refusal(where, f"{path!r} is not a path below --root")
    return path


def _string(value: str) -> str:
    return _string_at(value, value)


def _path(value: str) -> str:
    return _path_at(value, value)


def _keys(row, keys: frozenset, where: str) -> dict:
    if not isinstance(row, dict) or row.keys() != keys:
        raise Refusal(where, f"expected an object with exactly the keys {sorted(keys)}, got {row!r}")
    return row


@dataclass(frozen=True)
class UnitFiles:
    requirement_id: object
    manifest: str
    registry: str
    readers: str
    comparison: str | None
    candidate: object


def _unit_files(row, where: str) -> UnitFiles:
    row = _keys(row, UNIT_KEYS, where)
    comparison = None if row["comparison"] is None else _path_at(where, row["comparison"])
    return UnitFiles(row["requirement_id"], _path_at(where, row["manifest"]), _path_at(where, row["registry"]),
                     _path_at(where, row["readers"]), comparison, row["candidate"])


def _utf8(where: str, data: bytes) -> str:
    """Strict UTF-8: an undecodable byte becomes a lone surrogate under surrogateescape, and that refuses."""
    text = data.decode("utf-8", "surrogateescape")
    if LONE.search(text):
        raise Refusal(where, "is not UTF-8")
    return text


# --- read: every filesystem call goes through fdsafe [LAW:effects-at-boundaries]

@contextlib.contextmanager
def _held_parent(path: str):
    """(absolute path, held parent directory, entry name) of one file path."""
    with fdsafe.fs(path):
        given = os.path.abspath(path)
    parent, name = os.path.split(given)
    with fdsafe.hold_root(parent) as held:
        yield given, held, name


def _read(path: str) -> tuple[str, bytes]:
    """(absolute path, bytes) of one regular file, read through its held parent directory."""
    with _held_parent(path) as (given, held, name):
        return given, fdsafe.read_named(held, name)


def _read_below(root: fdsafe.Dir, path: str) -> tuple[str, bytes]:
    """As _read, for a file whose held parent must be below the held root by identity before it is read."""
    with _held_parent(path) as (given, held, name):
        _below(root, held)
        return given, fdsafe.read_named(held, name)


def _text(path: str) -> tuple[str, str]:
    given, data = _read(path)
    return given, _utf8(given, data)


def _json(path: str):
    given, text = _text(path)

    def pairs(items: list) -> dict:
        out: dict = {}
        for key, value in items:
            if key in out:
                raise Refusal(given, f"duplicate key {key!r}")
            out[key] = value
        return out

    def constant(name: str):
        raise Refusal(given, f"holds {name}, which is not JSON")
    try:
        doc = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        raise Refusal(given, f"is not JSON: {exc}") from exc
    # A JSON escape such as "\udcff" decodes to a lone surrogate, which no later step could encode.
    if LONE.search(json.dumps(doc, ensure_ascii=False)):
        raise Refusal(given, "holds a lone surrogate")
    return given, doc


def _still_held(held: fdsafe.Dir) -> None:
    """The held directory is still at the path it was held as; path-based reads below it saw that directory."""
    live = held.live()
    if live != held.path:
        raise Refusal(held.path, f"was moved while it was held (now {live})")


def _entry(parent_fd: int, name: str, path: str, prefix: str) -> bool:
    """Whether the entry name exists in the held parent, observed without following it; a link refuses."""
    try:
        st = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise Refusal(path, f"{exc.strerror} (at {prefix})", exc.errno) from exc
    if stat.S_ISLNK(st.st_mode):
        raise Refusal(path, f"component {prefix} is a link; a target is observed without following links")
    return True


def _exists(root: fdsafe.Dir, path: str) -> bool:
    """Whether the absolute path exists, observed component by component from the held root fd (or a held /
    for a path outside it). Each directory is opened with O_NOFOLLOW through the one before it, so a component
    swapped for a link after its own observation refuses at its open. [LAW:no-silent-failure]"""
    below = path.startswith(root.path + "/")
    with contextlib.ExitStack() as stack:
        start = root if below else stack.enter_context(fdsafe.hold_root("/"))
        *dirs, leaf = path[len(start.path):].strip("/").split("/")
        fd, prefix = start.fd, start.path
        for name in dirs:
            prefix = os.path.join(prefix, name)
            if not _entry(fd, name, path, prefix):
                return False
            with fdsafe.fs(path):
                fd = os.open(name, fdsafe.DIR_FLAGS, dir_fd=fd)
            stack.callback(fdsafe.close, fd, prefix)
        return _entry(fd, leaf, path, os.path.join(prefix, leaf))


def _below(root: fdsafe.Dir, held: fdsafe.Dir) -> None:
    """The held directory is the held root or below it now, by identity: one of its ".." ancestors is the
    root's (st_dev, st_ino). A root moved away and back around a read is caught here."""
    with fdsafe.fs(root.path):
        st = os.fstat(root.fd)
    want = (st.st_dev, st.st_ino)
    up, last = ".", None
    while True:
        with fdsafe.fs(held.path):
            st = os.stat(up, dir_fd=held.fd)
        here = (st.st_dev, st.st_ino)
        if here == want:
            return
        if here == last:  # "/" is its own ".."
            raise Refusal(held.path, f"is not below the held root {root.path}")
        up, last = os.path.join(up, ".."), here


def _observed_plan(build: Callable[[list], dict], held: fdsafe.Dir) -> dict:
    """The plan built from an observation that covers every target it names.

    A target the plan names but the observation lacks is observed and the plan is rebuilt; the set of paths
    only grows and is bounded by the candidates and V targets, so this ends. Each observation ends with the
    root's live check, so the plan returned is built after the last one."""
    seen: dict[str, bool] = {}
    while True:
        plan = build(sorted(path for path, there in seen.items() if there))
        fresh = [move["target"] for move in plan["moves"] if move["target"] not in seen]
        if not fresh:
            return plan
        seen.update((path, _exists(held, path)) for path in fresh)
        _still_held(held)


def _core_unit(files: UnitFiles) -> dict:
    manifest_path, manifest_bytes = _read(files.manifest)
    registry_path, registry = _json(files.registry)
    if not isinstance(registry, dict) or registry.keys() != {"root", "matches"} \
            or not isinstance(registry["matches"], list) or len(registry["matches"]) != 1:
        raise Refusal(registry_path, "is not a registry_match result holding exactly one match")
    return {"requirement_id": files.requirement_id, "manifest_path": manifest_path,
            "manifest_bytes": manifest_bytes, "registry": registry["matches"][0], "candidate": files.candidate,
            "readers": _json(files.readers)[1],
            "comparison": None if files.comparison is None else _json(files.comparison)[1]}


def plan(args) -> tuple[int, object]:
    # [LAW:one-source-of-truth] one hold of --root for the whole run; every check below names that hold.
    with fdsafe.hold_root(args.root) as held:
        tables = [_text(path) for path in args.requirements]
        units_path, listed = _json(args.units)
        if not isinstance(listed, list):
            raise Refusal(units_path, f"expected a list of units, got {type(listed).__name__}")
        units = [_core_unit(_unit_files(row, units_path)) for row in listed]
        built = _observed_plan(lambda existing: core.build_plan(
            entry_id=args.entry, root=held.path, requirement_tables=tables, units=units,
            existing_targets=existing), held)
    return 0, built


def _occurrences(root: fdsafe.Dir, report_path: str, report) -> list[dict]:
    report = _keys(report, frozenset(("stale", "unverified")), report_path)
    if not isinstance(report["stale"], list):
        raise Refusal(report_path, "stale is not a list")
    out = []
    for row in report["stale"]:
        row = _keys(row, STALE_KEYS, report_path)
        name = _reader_name(report_path, row["file"])
        line = row["line"]
        if type(line) is not int or line < 1:
            raise Refusal(report_path, f"line {line!r} is not a line number")
        out.append({**row, "text": _line(root, os.path.join(root.path, name), line)})
    return out


def _line(root: fdsafe.Dir, path: str, number: int) -> str:
    given, data = _read_below(root, path)
    lines = data.split(b"\n")
    where = f"{given}:{number}"
    if number > len(lines):
        raise Refusal(where, f"has no line {number}")
    return _utf8(where, lines[number - 1])


def check_plans(args) -> tuple[int, object]:
    with fdsafe.hold_root(args.root) as held:
        plans_path, plans = _json(args.plans)
        plans = _keys(plans, frozenset(("entries",)), plans_path)
        repairs = _text(args.repairs)
        occurrences = [o for path in args.readers for o in _occurrences(held, *_json(path))]
        _still_held(held)
    found = core.check_plans(root=held.path, entries=plans["entries"], occurrences=occurrences, repairs=repairs)
    return int(bool(found)), found


def check_routes(args) -> tuple[int, object]:
    routes = _text(args.routes)
    with fdsafe.hold_root(args.source) as held:
        with fdsafe.fs(held.path), os.scandir(held.fd) as it:
            children = sorted(entry.name for entry in it)
        _still_held(held)
    found = core.check_routes(routes=routes, source=held.path, children=children, hold_target=args.hold_target)
    return int(bool(found)), found


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan", help="print one dry-run unit plan")
    p.add_argument("--entry", required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--requirements", required=True, action="append")
    p.add_argument("--units", required=True)
    p.set_defaults(run=plan)
    c = sub.add_parser("check-plans", help="check the repairs rows against the reader occurrences")
    c.add_argument("--root", required=True)
    c.add_argument("--plans", required=True)
    c.add_argument("--repairs", required=True)
    c.add_argument("--readers", required=True, action="append")
    c.set_defaults(run=check_plans)
    r = sub.add_parser("check-routes", help="check one producer route table")
    r.add_argument("--routes", required=True)
    r.add_argument("--source", required=True)
    r.add_argument("--hold-target", required=True)
    r.set_defaults(run=check_routes)
    return parser


def _paths(values: list) -> list[str]:
    return [_path(value) for value in values]


FIELDS = {"entry": _string, "hold_target": _string, "root": _path, "units": _path, "plans": _path,
          "repairs": _path, "routes": _path, "source": _path, "requirements": _paths, "readers": _paths}


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        for key in FIELDS.keys() & vars(args).keys():
            setattr(args, key, FIELDS[key](getattr(args, key)))
        code, result = args.run(args)
    except Refusal as exc:
        print(exc, file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical(result) + b"\n")  # the core's canonical bytes, never re-encoded
    return code


if __name__ == "__main__":
    sys.exit(main())
