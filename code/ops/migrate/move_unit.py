#!/usr/bin/env python3
"""Build one dry-run unit plan, check the repairs rows or a producer route table (ICM v2.1 Part 2, Step 209),
or run one approved unit plan in M (Step 210).

I/O shell of move_plan_core (Step 217) and move_run_core (Step 218), which hold all the plan, check and run
logic. plan, check-plans and check-routes are dry runs: they move nothing, create no file and run no Git or
other process. Input files use fdsafe.read_named through their held parent directories; reader occurrences
also accept a link's own text through fdsafe.read_named_or_link. No link is followed; each directory held
must be its own real path.

  plan --entry ID --root DIR --requirements FILE... --units FILE
      Prints move_plan_core.build_plan's plan unchanged, as one canonical JSON line. --units is a JSON list
      with one object per unit: {"requirement_id", "manifest" (Step 201 manifest), "registry" (Step 206
      registry_match output holding exactly one match), "readers" (Step 207 reader_find report),
      "comparison" (Step 205 dup_find output, or null when no comparison was made), "candidate" (a path
      below experiments/<id>/, or null)}. The target paths the core may choose are observed with a no-follow
      lstat until every target of the plan has been observed; the plan is built from that observation.
  check-plans --root DIR --plans FILE --repairs FILE --historical FILE --readers FILE...
      --plans is {"entries": [...]}. Each stale row of each reader_find report becomes an occurrence with
      the text of its line, read from the reader file below --root. Prints move_plan_core.check_plans's
      findings.
  check-routes --routes FILE --source DIR --hold-target PATH
      The children are the entries of the held --source directory. Prints move_plan_core.check_routes's
      findings.
  run --root M --plan FILE --approval FILE --split SOURCE FILE... --run-units FILE --custody-dir DIR
      Executes the Step 209 plan document in FILE under its native G4 approval. It observes the plan, the
      approval, a fresh Step 201 inventory of each unit source (unit_manifest's own fd-bound walk), each
      unit's Step 212 split document, the targets (each held from its nearest existing folder, no link
      followed), the run-unit roots (a JSON list) and the worktree and tracked files (git rev-parse, git
      ls-files), passes them to move_run_core.run_unit and refuses whatever it refuses. It then writes the six
      custody documents and admitted.tsv (the H-SLICE.md:40 rows of the core's actions) into the existing
      --custody-dir with fdsafe.create_file, and runs only the core's actions, in order: mkdir by
      fdsafe.mkdir, mv by fdsafe.rename, git-mv by fdsafe.rename and `git update-index`, and git-rm-cached
      by `git update-index`. For git-add, Git computes the blob id with `hash-object --no-filters --stdin`;
      the run writes the compressed loose object through held fds with fdsafe.create_file, then stages it
      with `git update-index`. Its roots are each unit folder (held by fd, so it stays a root wherever it
      moves; a file unit has none), the folders that hold each unit source, each existing target parent, and
      every folder the run creates, never M, so custody files are created outside every root.
      Before any Git call it holds M/.git and its config without following links and refuses (T201
      rulings 2, 7 and 8) a link or special file under .git, a config.worktree, an include, includeIf,
      extensions or filter key, a core key outside the plain set, or a remote promisor or partial-clone
      key; after each Git call the held .git and config must still be what their paths name (ruling 9).
      It never overwrites, deletes or commits; a refusal after a file or folder exists names it and
      leaves it in place. Stdout: {"actions", "custody"}.

Exit 0: the plan, no finding ("[]"), or the unit plan run. Exit 1: one or more findings, printed as one canonical JSON list.
Exit 2: a refusal (fdsafe.Refusal from the shell or the core), one line on stderr naming the path (and the
errno name for a filesystem error); or a malformed invocation. Any other exception propagates.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import errno
import hashlib
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
import zlib
from dataclasses import dataclass
from typing import Callable

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as core
from ops.migrate import move_run_core as run_core
from ops.migrate import unit_manifest
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

class InputParents(contextlib.ExitStack):
    """Own input parents until the run has finished reading all of its inputs."""

    def __init__(self):
        super().__init__()
        # [LAW:no-ambient-temporal-coupling] the run owns both the holds and their final check.
        self.parents: list[tuple[fdsafe.Dir, fdsafe.Dir]] = []

    def check(self) -> None:
        for root, held in self.parents:
            _still_held(root, held)


def _held_parent(path: str, inputs: InputParents, root: fdsafe.Dir | None = None):
    """(absolute path, held parent directory, entry name) of one file path."""
    with fdsafe.fs(path):
        given = os.path.abspath(path)
    parent, name = os.path.split(given)
    held = inputs.enter_context(fdsafe.hold_root(parent))
    inputs.parents.append((held if root is None else root, held))
    return given, held, name


def _read(path: str, inputs: InputParents) -> tuple[str, bytes]:
    """Read through a parent held until every input has been read."""
    given, held, name = _held_parent(path, inputs)
    return given, fdsafe.read_named(held, name)


def _text(path: str, inputs: InputParents) -> tuple[str, str]:
    given, data = _read(path, inputs)
    return given, _utf8(given, data)


def _json(path: str, inputs: InputParents):
    given, text = _text(path, inputs)

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
        # [LAW:single-enforcer] Share the core's interpreter digit-limit boundary.
        doc = json.loads(text, object_pairs_hook=pairs, parse_constant=constant,
                         parse_int=lambda token: core._int(token, given))
    except json.JSONDecodeError as exc:
        raise Refusal(given, f"is not JSON: {exc}") from exc
    except RecursionError:
        raise Refusal(given, "nests too deeply")
    # A JSON escape such as "\udcff" decodes to a lone surrogate, which no later step could encode.
    if LONE.search(json.dumps(doc, ensure_ascii=False)):
        raise Refusal(given, "holds a lone surrogate")
    return given, doc


def _still_held(root: fdsafe.Dir, held: fdsafe.Dir) -> None:
    """The after-check of a held directory, run once its last use is past: it is still at the path it was
    opened for, and still the held root or below it by identity, so what was read through it is what that
    path names. A directory swapped for a link after its open is caught here too: its live path differs.
    [LAW:single-enforcer] the one after-check owner for every directory this tool holds."""
    live = held.live()
    if live != held.path:
        raise Refusal(held.path, f"was moved while it was held (now {live!r})")
    # [LAW:single-enforcer] live-path and fresh no-follow identity share this after-check.
    with fdsafe.fs(held.path):
        opened = os.fstat(held.fd)
        named = os.stat(held.path, follow_symlinks=False)
    if (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino):
        raise Refusal(held.path, "was moved during the run")
    _below(root, held)


def _entry(parent_fd: int, name: str, path: str, prefix: str) -> bool:
    """Whether the entry name exists in the held parent, observed without following it; a link refuses."""
    try:
        st = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise Refusal(path, f"{exc.strerror} (at {prefix!r})", exc.errno) from exc
    if stat.S_ISLNK(st.st_mode):
        raise Refusal(path, f"component {prefix!r} is a link; a target is observed without following links")
    return True


def _exists(root: fdsafe.Dir, path: str) -> bool:
    """Whether the absolute path exists, observed component by component from the held root fd (or a held /
    for a path outside it). Each directory is opened with O_NOFOLLOW through the one before it, so a component
    swapped for a link after its own observation refuses at its open, and one moved or swapped after its open
    refuses at its after-check. [LAW:no-silent-failure]"""
    below = path.startswith(root.path + "/")
    with contextlib.ExitStack() as stack:
        start = root if below else stack.enter_context(fdsafe.hold_root("/"))
        # [LAW:single-enforcer] every directory the observation used is after-checked once, below, the start
        # first: a moved --root is named as the root, not as its first component.
        held = [start]
        *dirs, leaf = path[len(start.path):].strip("/").split("/")
        parent, there = start, True
        for name in dirs:
            prefix = os.path.join(parent.path, name)
            there = _entry(parent.fd, name, path, prefix)
            if not there:
                break
            with fdsafe.fs(path):
                fd = os.open(name, fdsafe.DIR_FLAGS, dir_fd=parent.fd)
            stack.callback(fdsafe.close, fd, prefix)
            parent = fdsafe.Dir(fd, prefix)
            held.append(parent)
        else:
            there = _entry(parent.fd, leaf, path, os.path.join(parent.path, leaf))
        for opened in held:
            _still_held(start, opened)
        return there


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
            raise Refusal(held.path, f"is not below the held root {root.path!r}")
        up, last = os.path.join(up, ".."), here


def _observed_plan(build: Callable[[list], dict], held: fdsafe.Dir) -> dict:
    """The plan built from an observation that covers every target it names.

    A target the plan names but the observation lacks is observed and the plan is rebuilt; the set of paths
    only grows and is bounded by the candidates and V targets, so this ends. Each observation ends with the
    root's after-check, so the plan returned is built after the last one, even when no target is below it."""
    seen: dict[str, bool] = {}
    while True:
        plan = build(sorted(path for path, there in seen.items() if there))
        fresh = [move["target"] for move in plan["moves"] if move["target"] not in seen]
        if not fresh:
            return plan
        seen.update((path, _exists(held, path)) for path in fresh)
        _still_held(held, held)


def _core_unit(files: UnitFiles, inputs: InputParents) -> dict:
    manifest_path, manifest_bytes = _read(files.manifest, inputs)
    registry_path, registry = _json(files.registry, inputs)
    if not isinstance(registry, dict) or registry.keys() != {"root", "matches"} \
            or not isinstance(registry["matches"], list) or len(registry["matches"]) != 1:
        raise Refusal(registry_path, "is not a registry_match result holding exactly one match")
    return {"requirement_id": files.requirement_id, "manifest_path": manifest_path,
            "manifest_bytes": manifest_bytes, "registry": registry["matches"][0], "candidate": files.candidate,
            "readers": _json(files.readers, inputs)[1],
            "comparison": None if files.comparison is None else _json(files.comparison, inputs)[1]}


def plan(args) -> tuple[int, object]:
    # [LAW:one-source-of-truth] one hold of --root for the whole run; every check below names that hold.
    with fdsafe.hold_root(args.root) as held:
        with InputParents() as inputs:
            tables = [_text(path, inputs) for path in args.requirements]
            units_path, listed = _json(args.units, inputs)
            if not isinstance(listed, list):
                raise Refusal(units_path, f"expected a list of units, got {type(listed).__name__}")
            units = [_core_unit(_unit_files(row, units_path), inputs) for row in listed]
            inputs.check()
        built = _observed_plan(lambda existing: core.build_plan(
            entry_id=args.entry, root=held.path, requirement_tables=tables, units=units,
            existing_targets=existing), held)
    return 0, built


def _occurrences(root: fdsafe.Dir, inputs: InputParents, report_path: str, report) -> list[dict]:
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
        out.append({**row, "text": _line(root, os.path.join(root.path, name), line, inputs)})
    return out


def _line(root: fdsafe.Dir, path: str, number: int, inputs: InputParents) -> str:
    given, held, name = _held_parent(path, inputs, root)
    _below(root, held)
    # [LAW:single-enforcer] Only reader occurrences use fdsafe's regular-or-link rule.
    data = fdsafe.read_named_or_link(held, name)
    lines = data.split(b"\n")
    where = f"{given}:{number}"
    if number > len(lines):
        raise Refusal(where, f"has no line {number}")
    return _utf8(where, lines[number - 1])


def check_plans(args) -> tuple[int, object]:
    with fdsafe.hold_root(args.root) as held:
        with InputParents() as inputs:
            plans_path, plans = _json(args.plans, inputs)
            plans = _keys(plans, frozenset(("entries",)), plans_path)
            repairs = _text(args.repairs, inputs)
            # [LAW:single-enforcer] Historical input shares repairs' held-parent reader and checks.
            historical = _text(args.historical, inputs)
            occurrences = [o for path in args.readers for o in _occurrences(held, inputs, *_json(path, inputs))]
            inputs.check()
        # [LAW:single-enforcer] root after-check follows the input parents' last use and close.
        _still_held(held, held)
    found = core.check_plans(root=held.path, entries=plans["entries"], occurrences=occurrences,
                            repairs=repairs, historical=historical)
    return int(bool(found)), found


def check_routes(args) -> tuple[int, object]:
    with InputParents() as inputs:
        routes = _text(args.routes, inputs)
        with fdsafe.hold_root(args.source) as held:
            with fdsafe.fs(held.path), os.scandir(held.fd) as it:
                children = sorted(entry.name for entry in it)
            _still_held(held, held)
            inputs.check()
    found = core.check_routes(routes=routes, source=held.path, children=children, hold_target=args.hold_target)
    return int(bool(found)), found


# --- run (Step 210): the I/O shell of move_run_core ---------------------------------------------------------

# T201 ruling 2: the core keys a plain repo carries; any other can make Git read or run outside M.
GIT_CORE = frozenset(f"core.{k}" for k in ("repositoryformatversion", "filemode", "bare", "logallrefupdates",
                                           "ignorecase", "precomposeunicode", "symlinks"))
# include/includeIf read another file; extensions change how Git reads the repo (ruling 7); a filter driver is
# a program that `git add` runs.
GIT_SECTIONS = frozenset(("include", "includeif", "extensions", "filter"))
GIT_PROMISOR = frozenset(("promisor", "partialclonefilter"))
ADMITTED = "admitted.tsv"


def _absolute_at(where: str, value) -> str:
    path = _path_at(where, value)
    if not path.startswith("/"):
        raise Refusal(where, f"{path!r} is not an absolute path")
    return path


def _absolute(value: str) -> str:
    return _absolute_at(value, value)


def _splits(values: list) -> dict[str, str]:
    """{unit source: split file}; a source named twice refuses, so no --split is silently dropped."""
    pairs = [(_absolute(source), _path(path)) for source, path in values]
    out = dict(pairs)
    if len(out) != len(pairs):
        raise Refusal("--split", "names a unit source twice")
    return out


# [LAW:one-source-of-truth] recording and checking each held object use one identity definition.
def _config_id(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_ctime_ns)


def _git_id(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino)


@dataclass(frozen=True)
class Repo:
    """M with its .git folder and .git/config held open, so each Git call is checked against them."""
    root: str
    git: fdsafe.Dir
    objects: fdsafe.Dir
    config_fd: int
    config_id: tuple
    git_id: tuple

    @property
    def config(self) -> str:
        return os.path.join(self.git.path, "config")


def _check_repo(repo: Repo, reason: str) -> None:
    # [LAW:no-ambient-temporal-coupling] held fds pin both inodes, preventing replacement reuse;
    # compare live names to the recorded state.
    for path, expected, identity in (
            (repo.config, repo.config_id, _config_id),
            (repo.git.path, repo.git_id, _git_id)):
        with fdsafe.fs(path):
            named = os.lstat(path)
        if identity(named) != expected:
            raise Refusal(path, reason)
    fdsafe.walk(repo.git, _git_entry)


def _git(repo: Repo, *args: str, stdin=subprocess.DEVNULL) -> bytes:
    """Stdout of one Git command, bound to the recorded repo before and after the call."""
    command = f"{repo.root}: git {' '.join(args)}"
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GIT_DIR": repo.git.path, "GIT_WORK_TREE": repo.root,
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_NO_LAZY_FETCH": "1",
           "GIT_OPTIONAL_LOCKS": "0", "GIT_LITERAL_PATHSPECS": "1", "LC_ALL": "C"}
    _check_repo(repo, "changed before Git ran; Git would read another file")
    stream = {"input": stdin} if isinstance(stdin, bytes) else {"stdin": stdin}
    # [LAW:single-enforcer] every Git call crosses this hook-free boundary.
    with fdsafe.fs(command):
        proc = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                               "-c", "core.hooksPath=/dev/null", *args], cwd=repo.root,
                              env=env, **stream, capture_output=True, check=False)
    _check_repo(repo, "changed while Git ran; Git may have read another file")
    if proc.returncode != 0:
        detail = "; ".join(proc.stderr.decode("utf-8", "replace").split("\n")).strip("; ")
        raise Refusal(command, f"exited {proc.returncode}: {detail}")
    return proc.stdout


# [LAW:single-enforcer] keep Git's file-based redirections at the walk boundary.
GIT_REDIRECTIONS = {
    "config.worktree": "is a second config file Git would read",
    "commondir": "names a common directory; Git would read refs, objects and config outside M",
    "objects/info/alternates": "names another object store; Git would read objects outside M",
}


def _git_entry(entry: fdsafe.Entry) -> None:
    # [LAW:one-type-per-behavior] every redirection shares one refusal path.
    reason = GIT_REDIRECTIONS.get(entry.rel)
    if reason is not None:
        raise Refusal(entry.path, reason)
    if not (stat.S_ISDIR(entry.st.st_mode) or stat.S_ISREG(entry.st.st_mode)):
        raise Refusal(entry.path, "is a link or special file inside .git; Git would follow or open it")


def _open_repo(stack: contextlib.ExitStack, root: str) -> Repo:
    """M's .git held and checked before any Git call (T201 rulings 2, 7 and 8)."""
    git = stack.enter_context(fdsafe.hold_root(os.path.join(root, ".git")))
    objects_path = os.path.join(git.path, "objects")
    with fdsafe.fs(objects_path):
        fd = os.open("objects", fdsafe.DIR_FLAGS, dir_fd=git.fd)
    objects = stack.enter_context(fdsafe.Dir(fd, objects_path))
    config = os.path.join(git.path, "config")
    with fdsafe.fs(config):
        fd = os.open("config", fdsafe.LEAF_FLAGS, dir_fd=git.fd)
    stack.callback(fdsafe.close, fd, config)
    with fdsafe.fs(config):
        config_st = os.fstat(fd)
    if not stat.S_ISREG(config_st.st_mode):
        raise Refusal(config, "is not a regular file")
    with fdsafe.fs(git.path):
        git_st = os.fstat(git.fd)
    repo = Repo(root, git, objects, fd, _config_id(config_st), _git_id(git_st))
    listed = _git(repo, "config", "--file", "-", "--no-includes", "--null", "--list", stdin=fd)
    for record in listed.split(b"\0")[:-1]:
        key = _utf8(config, record.split(b"\n", 1)[0])
        section = key.split(".", 1)[0]
        if section in GIT_SECTIONS or (section == "core" and key not in GIT_CORE) \
                or (section == "remote" and key.rsplit(".", 1)[-1] in GIT_PROMISOR):
            raise Refusal(config, f"sets {key}; Git could read, run or fetch outside M")
    return repo


def _worktree(repo: Repo) -> dict:
    out = _git(repo, "rev-parse", "--path-format=absolute", "--show-toplevel", "--git-dir", "--git-common-dir")
    top, git_dir, common_dir, end = _utf8(repo.root, out).split("\n")
    return {"top": top, "git_dir": git_dir, "common_dir": common_dir}


def _index_rows(repo: Repo) -> list[tuple[str, str, str, str]]:
    # [LAW:one-source-of-truth] start reads and readbacks share the index record parser.
    listed = _git(repo, "ls-files", "-s", "-z", "--full-name")
    entries = []
    for record in listed.split(b"\0")[:-1]:
        metadata, name = _utf8(repo.root, record).split("\t", 1)
        mode, object_name, stage = metadata.split(" ")
        entries.append((mode, object_name, stage, name))
    return entries


def _tracked(repo: Repo, sources: list) -> tuple[list[str], set[tuple[str, str, str, str]]]:
    """Absolute tracked paths under each unit source in M, and the whole start index's rows."""
    inside = [source[len(repo.root) + 1:] for source in sources if source.startswith(repo.root + "/")]
    entries = _index_rows(repo)
    tracked = [f"{repo.root}/{name}" for _, _, _, name in entries
               if any(name == rel or name.startswith(rel + "/") for rel in inside)]
    return tracked, set(entries)


def _inventory(source: str) -> tuple[bytes, tuple, tuple[fdsafe.Dir, ...]]:
    """Fresh Step 201 manifest bytes, (st_dev, st_ino), and the source's held folders, owned by the caller:
    the walked Dir of a directory unit, none for a file unit (its fd is closed here; nothing is created inside
    a file).

    [LAW:one-source-of-truth] the bytes come from unit_manifest's own fd-bound walk over the held source, so
    they equal the plan's manifest exactly when nothing changed; no second inventory is written here. The
    lstat only picks how to hold the source; build_manifest re-checks the held fd's real path and kind."""
    # [LAW:no-ambient-temporal-coupling] Transfer folder holds; own file reads through their checked close.
    with contextlib.ExitStack() as kept, contextlib.ExitStack() as reading:
        with fdsafe.fs(source):
            directory = stat.S_ISDIR(os.lstat(source).st_mode)
        if directory:
            folders = (kept.enter_context(fdsafe.hold_root(source)),)
            fd = folders[0].fd
        else:
            folders = ()
            with fdsafe.fs(source):
                fd = os.open(source, fdsafe.LEAF_FLAGS)
            reading.callback(fdsafe.close, fd, source)
        with fdsafe.fs(source):
            try:
                doc = unit_manifest.build_manifest(source, fd)
            except unit_manifest.Refusal as exc:
                raise Refusal(source, str(exc)) from exc
            st = os.fstat(fd)
        result = canonical(doc), (st.st_dev, st.st_ino), folders
        kept.pop_all()
        return result


def _nearest(hold: Callable[[str], fdsafe.Dir], path: str) -> fdsafe.Dir:
    """The nearest existing folder at or above path, held without following a link."""
    while True:
        try:
            return hold(path)
        except Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
        path = os.path.dirname(path)


def _target(hold: Callable[[str], fdsafe.Dir], target: str) -> dict:
    """{target, exists, base}: base is the nearest existing ancestor; exists observes the first entry below it."""
    base = _nearest(hold, os.path.dirname(target))
    first = target[len(base.path):].strip("/").split("/")[0]
    exists = _entry(base.fd, first, target, os.path.join(base.path, first))
    return {"target": target, "exists": exists, "base": base.path}


def _admitted(root: str, actions: list, tracked: list) -> bytes:
    """The stage_check rows of the core's actions (A/H-SLICE.md:40): R100 per tracked file a git-mv moves, D per
    tracked file a git-rm-cached removes, A per git-add; paths relative to M."""
    def rel(path: str) -> str:
        return path[len(root) + 1:]

    def under(action: dict) -> list:
        # [LAW:dataflow-not-control-flow] File and directory units share _tracked's at-or-below rule.
        return [path for path in tracked if path == action["source"] or path.startswith(action["source"] + "/")]

    rows = {"mkdir": lambda a: [], "mv": lambda a: [],
            "git-mv": lambda a: [("R100", rel(p), rel(a["target"] + p[len(a["source"]):])) for p in under(a)],
            "git-rm-cached": lambda a: [("D", rel(p)) for p in under(a)],
            "git-add": lambda a: [("A", rel(a["target"]))]}
    return "".join("\t".join(row) + "\n" for a in actions for row in rows[a["action"]](a)).encode("utf-8")


def _write_custody(custody: str, files: list, roots: list) -> list[str]:
    """Create each (name, bytes) in the custody folder, outside every root; return the live paths."""
    written = []
    with fdsafe.open_out_parent(custody) as parent:
        for name, data in files:
            written.append(fdsafe.create_file(parent, name, data, roots))
            live = parent.live()
            if live != parent.path:
                raise Refusal(written[-1], f"its folder {parent.path} moved during the write (now {live}); "
                                           "left in place")
    return written


@dataclass(frozen=True)
class Held:
    """What the actions run against: M's repo, every held folder by path, each source's inventoried identity."""
    repo: Repo
    folders: dict
    sources: dict
    manifests: dict[str, bytes]
    leaves: dict[str, dict]
    tracked: list[str]
    index: set[tuple[str, str, str, str]]
    roots: list[fdsafe.Dir]
    stack: contextlib.ExitStack


def _ends(held: Held, action: dict) -> tuple:
    src, dst = action["source"], action["target"]
    return (held.folders[os.path.dirname(src)], os.path.basename(src),
            held.folders[os.path.dirname(dst)], os.path.basename(dst))


def _is_source(held: Held, parent: fdsafe.Dir, name: str, path: str, source: str) -> None:
    """parent/name is the folder inventoried as the unit source, by (st_dev, st_ino)."""
    with fdsafe.fs(path):
        st = os.lstat(name, dir_fd=parent.fd)
    if (st.st_dev, st.st_ino) != held.sources[source]:
        raise Refusal(path, f"is not the directory inventoried as the unit source {source}")


def _do_mkdir(held: Held, action: dict) -> None:
    folder = action["target"]
    parent = held.folders[os.path.dirname(folder)]
    held.folders[folder] = held.stack.enter_context(fdsafe.mkdir(parent, os.path.basename(folder)))
    # [LAW:one-source-of-truth] created target folders join the same non-unit-write exclusion roots.
    held.roots.append(held.folders[folder])


def _same_manifest(held: Held, path: str, source: str, reason: str) -> None:
    # [LAW:one-source-of-truth] compare unit_manifest's own document, rebasing only moved paths.
    manifest, _, folders = _inventory(path)
    for folder in folders:
        folder.close()

    def rebase(value):
        if isinstance(value, str):
            return source + value[len(path):] if value == path or value.startswith(path + "/") else value
        if isinstance(value, list):
            return [rebase(item) for item in value]
        if isinstance(value, dict):
            return {rebase(key): rebase(item) for key, item in value.items()}
        return value

    if canonical(rebase(json.loads(manifest))) != held.manifests[source]:
        raise Refusal(path, reason)


def _do_mv(held: Held, action: dict) -> None:
    src_parent, src_name, dst_parent, dst_name = _ends(held, action)
    _still_held(src_parent, src_parent)
    _is_source(held, src_parent, src_name, action["source"], action["source"])
    _same_manifest(held, action["source"], action["source"], "changed since it was inventoried; nothing moved")
    fdsafe.rename(src_parent, src_name, dst_parent, dst_name, [src_parent, dst_parent])
    _is_source(held, dst_parent, dst_name, action["target"], action["source"])
    _same_manifest(held, action["target"], action["source"], "changed since it was inventoried; left in place")


def _index_is(held: Held, path: str) -> list[tuple[str, str, str, str]]:
    # [LAW:single-enforcer] compare the whole index with the run's own record of it.
    root = held.repo.root
    reason = "Git's index under it changed since it was read"
    entries = _index_rows(held.repo)
    if set(entries) != held.index:
        raise Refusal(path, reason)
    entries = [entry for entry in entries
               if root + "/" + entry[3] == path or (root + "/" + entry[3]).startswith(path + "/")]
    if any(entry[2] != "0" for entry in entries):
        raise Refusal(path, reason)
    blobs = _git(held.repo, "cat-file", "--batch",
                 stdin="".join(entry[1] + "\n" for entry in entries).encode("ascii"))
    offset = 0
    for mode, object_name, stage, name in entries:
        # [LAW:parse-dont-validate] one anchored match is the record header's whole contract: this id, a blob, its size, LF.
        header = re.compile(re.escape(object_name.encode("ascii")) + rb" blob ([0-9]+)\n").match(blobs, offset)
        if header is None:
            raise Refusal(path, reason)
        start = header.end()
        offset = start + int(header[1])
        if blobs[offset:offset + 1] != b"\n":
            raise Refusal(path, reason)
        leaf = held.leaves[root + "/" + name]
        modes = {"symlink": ("120000",), "file": ("100644", "100755")}
        if mode not in modes[leaf["kind"]] or hashlib.sha256(blobs[start:offset]).hexdigest() != leaf["sha256"]:
            raise Refusal(path, reason)
        offset += 1
    if offset != len(blobs):
        raise Refusal(path, reason)
    return entries


def _write_index(held: Held, entries: list[tuple[str, str, str]]) -> None:
    # [LAW:one-source-of-truth] all actions share the index record format and write boundary.
    # [LAW:dataflow-not-control-flow] removal mode uses the same record shape as addition.
    records = [f"{mode} {object_name} 0\t{path}\0"
               for mode, object_name, path in entries]
    _git(held.repo, "update-index", "-z", "--index-info", stdin="".join(records).encode("utf-8"))
    for mode, object_name, path in entries:
        held.index.difference_update({row for row in held.index if row[3] == path})
        if mode != "0":
            held.index.add((mode, object_name, "0", path))


def _do_git_mv(held: Held, action: dict) -> None:
    src_parent, src_name, dst_parent, dst_name = _ends(held, action)
    _still_held(src_parent, src_parent)
    root = held.repo.root
    entries = _index_is(held, action["source"])
    _is_source(held, src_parent, src_name, action["source"], action["source"])
    _same_manifest(held, action["source"], action["source"], "changed since it was inventoried; nothing moved")
    # [LAW:single-enforcer] exclusive rename owns collision refusal, including late target creation.
    fdsafe.rename(src_parent, src_name, dst_parent, dst_name, [src_parent, dst_parent])
    records = []
    for mode, object_name, stage, path in entries:
        target = action["target"][len(root) + 1:] + path[len(action["source"][len(root) + 1:]):]
        records.extend((("0", "0" * len(object_name), path), (mode, object_name, target)))
    _write_index(held, records)
    _index_is(held, action["target"])
    _is_source(held, dst_parent, dst_name, action["target"], action["source"])
    _same_manifest(held, action["target"], action["source"], "changed since it was inventoried; left in place")


def _do_git_rm_cached(held: Held, action: dict) -> None:
    entries = _index_is(held, action["source"])
    _write_index(held, [("0", "0" * len(object_name), path) for mode, object_name, stage, path in entries])
    _index_is(held, action["source"])


def _write_object(held: Held, object_name: str, data: bytes) -> None:
    # [LAW:effects-at-boundaries] Git computes identity; held fds own every object-store write.
    # [LAW:one-source-of-truth] the object store is held once at repo open; a renamed objects path cannot redirect this write.
    with contextlib.ExitStack() as stack:
        objects = held.repo.objects
        name = object_name[:2]
        fanout_path = objects.path + "/" + name
        try:
            with fdsafe.fs(fanout_path):
                fd = os.open(name, fdsafe.DIR_FLAGS, dir_fd=objects.fd)
            fanout = stack.enter_context(fdsafe.Dir(fd, fanout_path))
        except Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            fanout = stack.enter_context(fdsafe.mkdir(objects, name))
        compressed = zlib.compress(b"blob %d\0" % len(data) + data)
        try:
            fdsafe.create_file(fanout, object_name[2:], compressed, held.roots)
        except Refusal as exc:
            # [LAW:one-source-of-truth] the index readback verifies an existing object's manifest bytes.
            if exc.errno != errno.EEXIST:
                raise


def _do_git_add(held: Held, action: dict) -> None:
    target = action["target"]
    parent_path, name = os.path.split(target)
    parent = held.stack.enter_context(fdsafe.hold_root(parent_path))
    # [LAW:single-enforcer] one boundary translates every leaf-read OS error.
    with fdsafe.fs(target):
        st = os.lstat(name, dir_fd=parent.fd)
        # [LAW:effects-at-boundaries] Git receives bytes, never a worktree path to filter.
        if stat.S_ISREG(st.st_mode):
            data = fdsafe.read_bytes(fdsafe.Entry(parent.fd, name, target, name, st))
            mode = "100755" if st.st_mode & stat.S_IXUSR else "100644"
        elif stat.S_ISLNK(st.st_mode):
            # [LAW:single-enforcer] The shared reader binds link text to this scan.
            data = fdsafe.read_link(fdsafe.Entry(parent.fd, name, target, name, st))
            mode = "120000"
        else:
            raise Refusal(target, "is not a regular file or a symlink")
    object_name = _git(held.repo, "hash-object", "--no-filters", "--stdin", stdin=data).decode("ascii").strip()
    _write_object(held, object_name, data)
    _write_index(held, [(mode, object_name, target[len(held.repo.root) + 1:])])
    _index_is(held, action["target"])


# [LAW:dataflow-not-control-flow] each action kind the core returns names its one runner.
ACTIONS = {"mkdir": _do_mkdir, "mv": _do_mv, "git-mv": _do_git_mv, "git-rm-cached": _do_git_rm_cached,
           "git-add": _do_git_add}


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def run(args) -> tuple[int, object]:
    root = args.run_root
    with InputParents() as inputs:
        plan = _read(args.plan, inputs)
        approval = _read(args.approval, inputs)
        run_units = _json(args.run_units, inputs)[1]
        splits = {source: _read(path, inputs)[1] for source, path in args.split.items()}
        inputs.check()
    # [LAW:single-enforcer] the core's own plan parser names the units to observe.
    units = run_core._plan(plan).units
    for source in sorted(set(splits) - {unit.source for unit in units}):
        raise Refusal(source, "has a --split but is no unit of the plan")
    with contextlib.ExitStack() as stack:
        folders: dict[str, fdsafe.Dir] = {}

        def hold(path: str) -> fdsafe.Dir:
            if path not in folders:
                folders[path] = stack.enter_context(fdsafe.hold_root(path))
            return folders[path]

        repo = _open_repo(stack, root)
        worktree = _worktree(repo)
        tracked, index = _tracked(repo, [unit.source for unit in units])
        observed, sources, manifests, leaves, unit_folders = [], {}, {}, {}, []
        for unit in units:
            hold(os.path.dirname(unit.source))
            manifest, sources[unit.source], held_folders = _inventory(unit.source)
            # [LAW:dataflow-not-control-flow] An empty tuple adds no file-unit folder to the write exclusions.
            unit_folders += [stack.enter_context(folder) for folder in held_folders]
            manifests[unit.source] = manifest
            # [LAW:one-source-of-truth] both path names derive from the same admitted manifest bytes.
            for leaf in json.loads(manifest)["leaves"]:
                leaves[leaf["source"]] = leaf
                leaves[unit.target + leaf["source"][len(unit.source):]] = leaf
            observed.append({"source": unit.source, "manifest": manifest, "split": splits.get(unit.source)})
        targets = [_target(hold, unit.target) for unit in units]
        result = run_core.run_unit(root=root, plan=plan, approval=approval, now=_now(), units=observed,
                                   tracked=tracked, worktree=worktree, targets=targets, run_units=run_units,
                                   custody_dir=args.custody_dir)
        # [LAW:effects-at-boundaries] the roots are the unit's own folders only, never M.
        roots = unit_folders + \
            [folders[os.path.dirname(unit.source)] for unit in units] + \
            [folders[t["base"]] for t in targets if t["base"] == os.path.dirname(t["target"])]
        files = [(os.path.basename(doc["path"]), doc["bytes"]) for doc in result["documents"]] + \
            [(ADMITTED, _admitted(root, result["actions"], tracked))]
        custody = _write_custody(args.custody_dir, files, roots)
        held = Held(repo, folders, sources, manifests, leaves, tracked, index, roots, stack)
        for action in result["actions"]:
            ACTIONS[action["action"]](held, action)
    return 0, {"actions": result["actions"], "custody": custody}


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
    c.add_argument("--historical", required=True)
    c.add_argument("--readers", required=True, action="append")
    c.set_defaults(run=check_plans)
    r = sub.add_parser("check-routes", help="check one producer route table")
    r.add_argument("--routes", required=True)
    r.add_argument("--source", required=True)
    r.add_argument("--hold-target", required=True)
    r.set_defaults(run=check_routes)
    u = sub.add_parser("run", help="execute one approved unit plan in M and write its custody files")
    u.add_argument("--root", required=True, dest="run_root")
    u.add_argument("--plan", required=True)
    u.add_argument("--approval", required=True)
    u.add_argument("--split", required=True, action="append", nargs=2, metavar=("SOURCE", "FILE"))
    u.add_argument("--run-units", required=True)
    u.add_argument("--custody-dir", required=True)
    u.set_defaults(run=run)
    return parser


def _paths(values: list) -> list[str]:
    return [_path(value) for value in values]


FIELDS = {"entry": _string, "hold_target": _string, "root": _path, "units": _path, "plans": _path,
          "repairs": _path, "historical": _path, "routes": _path, "source": _path, "requirements": _paths, "readers": _paths,
          "run_root": _absolute, "plan": _path, "approval": _path, "split": _splits, "run_units": _path,
          "custody_dir": _absolute}


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
