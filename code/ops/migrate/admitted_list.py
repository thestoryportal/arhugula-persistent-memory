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
Paths are relative to the repository root. An add's bytes are read, never following a final
symlink, from "src" (any path) or else from the repository's "dst". The add whose "dst" is the
output file itself is hashed from the text being written.
"""
from __future__ import annotations

import argparse
import errno
import json
import os
import stat
import subprocess
import sys
from collections import defaultdict

PLAN_KEYS = frozenset({"move", "remove", "add", "modify"})
READ_ONLY_GIT = frozenset({"rev-parse", "ls-tree", "ls-files", "hash-object"})


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


def check_rel(path) -> str:
    if not isinstance(path, str) or not path:
        raise PlanError(f"path {path!r} is not a non-empty string")
    if "\t" in path or "\n" in path:
        raise PlanError(f"path {path!r} contains a tab or newline; stage_check rows cannot hold it")
    parts = path.split("/")
    if any(p in ("", ".", "..") for p in parts) or parts[0] == ".git":
        raise PlanError(f"path {path!r} is not a plain path inside the repository")
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
    for m in out["move"]:
        if not isinstance(m, dict) or set(m) != {"src", "dst"}:
            raise PlanError(f"move {m!r} needs exactly src and dst")
        check_rel(m["src"]), check_rel(m["dst"])
    for a in out["add"]:
        if not isinstance(a, dict) or not {"dst"} <= set(a) <= {"dst", "src"}:
            raise PlanError(f"add {a!r} needs dst and an optional src")
        check_rel(a["dst"])
        if "src" in a and not isinstance(a["src"], str):
            raise PlanError(f"add {a!r} has a src that is not a string")
    for p in out["remove"] + out["modify"]:
        check_rel(p)
    return out


def build_rows(plan: dict, tracked: dict) -> tuple:
    rows = []
    for m in plan["move"]:
        rows += [("R100", p, m["dst"] + p[len(m["src"]):]) for p in under(tracked, m["src"])]
    for src in plan["remove"]:
        rows += [("D", p) for p in under(tracked, src)]
    rows += [("A", a["dst"]) for a in plan["add"]]
    for p in plan["modify"]:
        if p not in tracked:
            raise PlanError(f"modify {p!r} is not a tracked file")
        rows.append(("M", p))
    if not rows:
        raise PlanError("the plan yields no rows; an empty admitted list is never a pass")
    seen = set()
    for row in rows:
        for p in row[1:]:
            check_rel(p)
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


def read_link_or_file(path: str) -> tuple:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError as exc:
        if exc.errno != errno.ELOOP:
            raise
        return os.readlink(os.fsencode(path)), True  # Git stores a symlink as its link text.
    with os.fdopen(fd, "rb") as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
            raise PlanError(f"{path!r} is not a regular file or symlink")
        return f.read(), False


def repo_file(repo: str, rel: str) -> str:
    cur = repo
    for part in rel.split("/")[:-1]:
        cur = os.path.join(cur, part)
        if not stat.S_ISDIR(os.lstat(cur).st_mode):
            raise PlanError(f"{rel!r} passes through {cur!r}, which is a symlink or not a directory")
    return os.path.join(repo, rel)


def blob_of(repo: str, dst: str, data: bytes, is_link: bool) -> str:
    args = ["hash-object", "--stdin", "--no-filters"] if is_link else ["hash-object", "--stdin", f"--path={dst}"]
    return git(repo, *args, stdin=data).decode().strip()


def same_file_path(a: str, b: str) -> bool:
    return (os.path.basename(a) == os.path.basename(b)
            and os.path.realpath(os.path.dirname(a)) == os.path.realpath(os.path.dirname(b)))


def run(repo: str, plan, out: str) -> str:
    top = git(repo, "rev-parse", "--show-toplevel").decode().rstrip("\n")
    if os.path.realpath(top) != os.path.realpath(repo):
        raise PlanError(f"{repo!r} is not the repository top level {top!r}")
    plan = load_plan(plan)
    tracked = tracked_files(repo)
    rows = build_rows(plan, tracked)
    text = "".join("\t".join(row) + "\n" for row in rows)
    add_blobs = {}
    for a in plan["add"]:
        if "src" not in a and same_file_path(os.path.join(repo, a["dst"]), out):
            data, is_link = text.encode("utf-8"), False
        else:
            try:
                data, is_link = read_link_or_file(a["src"] if "src" in a else repo_file(repo, a["dst"]))
            except FileNotFoundError as exc:
                raise PlanError(f"add {a['dst']!r}: its bytes are missing ({exc})") from exc
        add_blobs[a["dst"]] = blob_of(repo, a["dst"], data, is_link)
    check_pairing(rows, tracked, add_blobs)
    # O_EXCL never overwrites; with O_CREAT it also refuses an existing symlink instead of following it.
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
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
