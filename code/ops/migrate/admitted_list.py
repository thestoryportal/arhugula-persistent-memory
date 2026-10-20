#!/usr/bin/env python3
"""Write the exact stage_check admitted list for one unit plan (A/H-SLICE.md:40-42).

Rows: R100 per moved tracked file, D per tracked file leaving M, A per newly tracked record
and per unit custody file, M per regenerated output. The output is the text that
`code/ops/git/stage_check.py` `parse_admitted` reads.

Read only in the repository: it runs only `rev-parse`, `ls-tree`, `ls-files` and `hash-object`
without `-w`, so it never stages anything and never runs `git add -A`. It refuses (exit 1) a plan
whose rows put one blob on both the deletion side (D rows, R100 sources) and the addition side
(A rows, R100 targets) other than as a single R100 row, because Git may then pair those paths
differently (A/H-SLICE.md:42); split such moves into separate tickets. Malformed input exits 2.

Plan JSON: {"move": [{"src", "dst"}], "remove": [path], "add": [{"dst", "src"?}], "modify": [path]}.
Paths are relative to the repository root. No path may hold a control character (U+0000-U+001F,
U+007F): stage_check reads the written file as text, which would split or change such a row.
Every repository destination (each move "dst", each R100 target, each add "dst") is reached from
the repository root through real directories only, never a symlink, before anything is written.
An add's bytes are read, never following a final symlink, from "src" (any path) or else from the
repository's "dst" through the directory fd that check opened. The add whose "dst" is the output
file itself (same name, same directory inode) is hashed from the text being written.
"""
from __future__ import annotations

import argparse
import contextlib
import errno
import json
import os
import stat
import subprocess
import sys
from collections import defaultdict

from ops.migrate import fdsafe

PLAN_KEYS = frozenset({"move", "remove", "add", "modify"})
READ_ONLY_GIT = frozenset({"rev-parse", "ls-tree", "ls-files", "hash-object"})
CONTROL = frozenset(map(chr, [*range(0x20), 0x7F]))
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK


class PlanError(Exception):
    """Malformed or unsafe input: exit 2."""


class Refusal(Exception):
    """Git may pair rows other than as admitted: exit 1."""


def git(repo: str, *args: str, stdin: bytes | None = None) -> bytes:
    if not args or args[0] not in READ_ONLY_GIT or (args[0] == "hash-object" and "-w" in args):
        raise PlanError(f"refused git command {list(args)!r}: only read-only subcommands run")
    # GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE override -C, so an inherited one would read another repo.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", repo, *args], input=stdin, env=env, capture_output=True, check=False)
    if proc.returncode != 0:
        raise PlanError(f"git {args[0]} exited {proc.returncode}: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


def check_chars(path, field: str) -> str:
    if not isinstance(path, str) or not path:
        raise PlanError(f"{field}: path {path!r} is not a non-empty string")
    if CONTROL & set(path):
        raise PlanError(f"{field}: path {path!r} contains a control character (U+0000-U+001F or U+007F, "
                        "such as a tab or newline); the admitted file cannot carry it")
    return path


def check_rel(path, field: str) -> str:
    check_chars(path, field)
    parts = path.split("/")
    if any(p in ("", ".", "..") for p in parts) or parts[0] == ".git":
        raise PlanError(f"{field}: path {path!r} is not a plain path inside the repository")
    return path


def tracked_files(repo: str) -> dict:
    """path -> blob id, from HEAD; refuses an index that differs from HEAD."""
    head, index = {}, {}
    for entry in git(repo, "ls-tree", "-r", "--full-tree", "-z", "HEAD").split(b"\0")[:-1]:
        meta, path = entry.split(b"\t", 1)
        mode, _type, blob = meta.decode().split(" ")
        head[path.decode("utf-8")] = (mode, blob, "0")
    for entry in git(repo, "ls-files", "-s", "-z").split(b"\0")[:-1]:
        meta, path = entry.split(b"\t", 1)
        index[path.decode("utf-8")] = tuple(meta.decode().split(" "))
    if index != head:
        raise PlanError("the index differs from HEAD; start from a clean index")
    return {path: blob for path, (_mode, blob, _stage) in head.items()}


def under(tracked: dict, src: str) -> list:
    return sorted(p for p in tracked if p == src or p.startswith(src + "/"))


def load_plan(plan) -> dict:
    if not isinstance(plan, dict) or set(plan) - PLAN_KEYS:
        raise PlanError(f"plan keys {sorted(plan) if isinstance(plan, dict) else plan!r} are not within {sorted(PLAN_KEYS)}")
    out = {k: plan.get(k, []) for k in PLAN_KEYS}
    if not all(isinstance(v, list) for v in out.values()):
        raise PlanError("every plan key holds a list")
    for i, m in enumerate(out["move"]):
        if not isinstance(m, dict) or set(m) != {"src", "dst"}:
            raise PlanError(f"move {m!r} needs exactly src and dst")
        check_rel(m["src"], f"move[{i}].src"), check_rel(m["dst"], f"move[{i}].dst")
    for i, a in enumerate(out["add"]):
        if not isinstance(a, dict) or not {"dst"} <= set(a) <= {"dst", "src"}:
            raise PlanError(f"add {a!r} needs dst and an optional src")
        check_rel(a["dst"], f"add[{i}].dst")
        if "src" in a and not isinstance(a["src"], str):
            raise PlanError(f"add {a!r} has a src that is not a string")
        if "src" in a:
            check_chars(a["src"], f"add[{i}].src")
    for key in ("remove", "modify"):
        for i, p in enumerate(out[key]):
            check_rel(p, f"{key}[{i}]")
    return out


def build_rows(plan: dict, tracked: dict) -> tuple:
    fielded = []  # (row, the plan field it came from, named when one of its paths is refused)
    for i, m in enumerate(plan["move"]):
        fielded += [(("R100", p, m["dst"] + p[len(m["src"]):]), f"move[{i}]") for p in under(tracked, m["src"])]
    for i, src in enumerate(plan["remove"]):
        fielded += [(("D", p), f"remove[{i}]") for p in under(tracked, src)]
    fielded += [(("A", a["dst"]), f"add[{i}].dst") for i, a in enumerate(plan["add"])]
    for i, p in enumerate(plan["modify"]):
        if p not in tracked:
            raise PlanError(f"modify {p!r} is not a tracked file")
        fielded.append((("M", p), f"modify[{i}]"))
    rows = [row for row, _ in fielded]
    if not rows:
        raise PlanError("the plan yields no rows; an empty admitted list is never a pass")
    seen = set()
    for row, field in fielded:
        for p in row[1:]:
            check_rel(p, field)
            if p in seen:
                raise PlanError(f"path {p!r} is in two rows")
            seen.add(p)
        if row[0] in ("R100", "A") and row[-1] in tracked:
            raise PlanError(f"target {row[-1]!r} is already tracked")
    return tuple(sorted(rows))


def check_pairing(rows: tuple, tracked: dict, add_blobs: dict) -> None:
    deleted, added = defaultdict(set), defaultdict(set)
    for row in rows:
        if row[0] in ("R100", "D"):
            deleted[tracked[row[1]]].add(row)
        if row[0] == "R100":
            added[tracked[row[1]]].add(row)
        if row[0] == "A":
            added[add_blobs[row[1]]].add(row)
    for blob in sorted(deleted.keys() & added.keys()):
        both = deleted[blob] | added[blob]
        if len(both) != 1:
            paths = sorted(p for row in both for p in row[1:])
            raise Refusal(f"equal bytes on both sides, Git may pair them differently: {paths}; "
                          "split these rows into separate tickets")


def read_link_or_file(path: str, dir_fd: int | None = None) -> tuple:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
    except OSError as exc:
        if exc.errno != errno.ELOOP:
            raise
        st = os.lstat(path, dir_fd=dir_fd)
        # [LAW:single-enforcer] fdsafe binds Git's link text to this scanned inode.
        return fdsafe.read_link(fdsafe.Entry(dir_fd, path, path, path, st)), True
    with os.fdopen(fd, "rb") as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
            raise PlanError(f"{path!r} is not a regular file or symlink")
        return f.read(), False


def repo_file(repo_fd: int, rel: str) -> int | None:
    """Open rel's parent directory from the repository root, one real directory at a time.

    A symlink or non-directory on the way refuses. None means a parent does not exist yet, so
    nothing below it can be a symlink now. Callers act through the returned fd, never the path.
    """
    fd = os.dup(repo_fd)
    for part in rel.split("/")[:-1]:
        try:
            child = os.open(part, DIR_FLAGS, dir_fd=fd)
        except OSError as exc:
            if exc.errno in (errno.ELOOP, errno.ENOTDIR):
                raise PlanError(f"destination {rel!r} passes through {part!r}, "
                                "which is a symlink or not a directory") from exc
            if exc.errno != errno.ENOENT:
                raise
            return None
        finally:
            os.close(fd)
        fd = child
    return fd


def created_destination(repo_fd: int, rel: str) -> None:
    """A path the move will create: no symlink on the way to it, and it is not a symlink itself."""
    parent = repo_file(repo_fd, rel)
    if parent is None:
        return
    try:
        mode = os.stat(os.path.basename(rel), dir_fd=parent, follow_symlinks=False).st_mode
    except FileNotFoundError:
        return
    finally:
        os.close(parent)
    if stat.S_ISLNK(mode):
        raise PlanError(f"destination {rel!r} is a symlink")


def blob_of(repo: str, dst: str, data: bytes, is_link: bool) -> str:
    args = ["hash-object", "--stdin", "--no-filters"] if is_link else ["hash-object", "--stdin", f"--path={dst}"]
    return git(repo, *args, stdin=data).decode().strip()


def same_file_path(a: str, b: str, a_dir: int, b_dir: int) -> bool:
    da, db = os.fstat(a_dir), os.fstat(b_dir)
    return os.path.basename(a) == os.path.basename(b) and (da.st_dev, da.st_ino) == (db.st_dev, db.st_ino)


def add_bytes(repo_fd: int, out_dir: int, out: str, add: dict, text: str) -> tuple:
    """(bytes, is_link) of an add without "src", read through the checked parent directory fd."""
    parent = repo_file(repo_fd, add["dst"])
    if parent is None:
        raise FileNotFoundError(errno.ENOENT, "a parent directory does not exist", add["dst"])
    try:
        if same_file_path(add["dst"], out, parent, out_dir):
            return text.encode("utf-8"), False
        return read_link_or_file(os.path.basename(add["dst"]), dir_fd=parent)
    finally:
        os.close(parent)


def run(repo: str, plan, out: str) -> str:
    top = git(repo, "rev-parse", "--show-toplevel").decode().rstrip("\n")
    if os.path.realpath(top) != os.path.realpath(repo):
        raise PlanError(f"{repo!r} is not the repository top level {top!r}")
    plan = load_plan(plan)
    tracked = tracked_files(repo)
    rows = build_rows(plan, tracked)
    text = "".join("\t".join(row) + "\n" for row in rows)
    with contextlib.ExitStack() as fds:
        repo_fd = os.open(repo, os.O_RDONLY | os.O_DIRECTORY)
        fds.callback(os.close, repo_fd)
        out_dir = os.open(os.path.dirname(out) or ".", os.O_RDONLY | os.O_DIRECTORY)
        fds.callback(os.close, out_dir)
        created = ([m["dst"] for m in plan["move"]] + [row[2] for row in rows if row[0] == "R100"]
                   + [a["dst"] for a in plan["add"] if "src" in a])
        for rel in created:
            created_destination(repo_fd, rel)
        add_blobs = {}
        for a in plan["add"]:
            try:
                data, is_link = read_link_or_file(a["src"]) if "src" in a else add_bytes(repo_fd, out_dir, out, a, text)
            except FileNotFoundError as exc:
                raise PlanError(f"add {a['dst']!r}: its bytes are missing ({exc})") from exc
            add_blobs[a["dst"]] = blob_of(repo, a["dst"], data, is_link)
        check_pairing(rows, tracked, add_blobs)
        # O_EXCL never overwrites; with O_CREAT it also refuses an existing symlink instead of following it.
        # The output is created in the directory fd that the self-output identity was checked against.
        fd = os.open(os.path.basename(out), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644, dir_fd=out_dir)
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--plan", required=True, metavar="FILE")
    ap.add_argument("--out", required=True, metavar="FILE", help="new file; never overwritten")
    args = ap.parse_args(argv)
    try:
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
        text = run(args.repo, plan, args.out)
    except Refusal as exc:
        print(f"admitted_list: refused: {exc}", file=sys.stderr)
        return 1
    except (PlanError, OSError, ValueError) as exc:
        print(f"admitted_list: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"out": args.out, "rows": text.count("\n")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
