#!/usr/bin/env python3
"""Re-inventory one unit into a sorted, hashed, no-follow manifest (ICM v2.1 Part 2, Step 201).

Read only. It walks the unit without following any link, hashes regular files, records
symlinks and sockets without opening them, and records each nested `.git` root with its
HEAD, branch and dirty entries. It writes exactly one new file, the --out path, and never
overwrites it.

Manifest: canonical JSON (sorted keys, "," and ":" separators, UTF-8, no trailing newline)
  {"schema_version": 1, "root": path, "leaves": [LeafRecord...], "git_roots": [GitRoot...]}
LeafRecord follows WIRE-CONTRACTS.md: source, kind, bytes, sha256, link_text, device, inode, nlink.
GitRoot: path, head (sha or null when unborn), branch (full ref or null when detached),
dirty (`git status --porcelain=v1 -z` records).
Leaves and git roots are sorted by the UTF-8 bytes of their path relative to the root.

Exit 0: manifest written; stdout is {"status": "PASS", "manifest", "sha256", "leaves", "git_roots"}.
Exit 1: a refusal (changed during hash, unsupported object, link out of the unit, unsafe
        nested repo, unreadable path); stdout is {"status": "FAIL", "reason"}; nothing written.
Exit 2: malformed invocation (root not a real directory, output exists or lies inside the root).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys

CHUNK = 1 << 20
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


class Refusal(Exception):
    """The unit cannot be inventoried safely; stop and write nothing."""


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sig(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def _hash_regular(path: str, before: os.stat_result) -> str:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise Refusal(f"object changed kind while opening: {path}")
        digest = hashlib.sha256()
        while chunk := os.read(fd, CHUNK):
            digest.update(chunk)
        after_read = os.fstat(fd)
    finally:
        os.close(fd)
    after = os.lstat(path)
    if len({_sig(before), _sig(opened), _sig(after_read), _sig(after)}) != 1:
        raise Refusal(f"changed during hash: {path}")
    return digest.hexdigest()


def _leaf(path: str, st: os.stat_result) -> dict:
    mode = st.st_mode
    link_text = None
    if stat.S_ISREG(mode):
        kind, digest = "file", _hash_regular(path, st)
    elif stat.S_ISLNK(mode):
        link_text = os.readlink(path)
        if _sig(os.lstat(path)) != _sig(st):
            raise Refusal(f"changed during hash: {path}")
        kind, digest = "symlink", hashlib.sha256(os.fsencode(link_text)).hexdigest()
    elif stat.S_ISSOCK(mode):
        kind, digest = "socket", EMPTY_SHA
    else:
        raise Refusal(f"unsupported object kind {stat.filemode(mode)}: {path}")
    return {"source": path, "kind": kind, "bytes": st.st_size, "sha256": digest, "link_text": link_text,
            "device": st.st_dev, "inode": st.st_ino, "nlink": st.st_nlink}


def _walk(directory: str, leaves: list, git_dirs: list) -> None:
    with os.scandir(directory) as it:
        names = [entry.name for entry in it]
    for name in names:
        path = os.path.join(directory, name)
        st = os.lstat(path)
        if name == ".git" and not stat.S_ISDIR(st.st_mode):
            raise Refusal(f"nested .git is not a directory (link to another git dir): {path}")
        if stat.S_ISDIR(st.st_mode):
            if name == ".git":
                git_dirs.append(path)
            _walk(path, leaves, git_dirs)
        else:
            leaves.append(_leaf(path, st))


def _git(worktree: str, *args: str) -> subprocess.CompletedProcess:
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "GIT_DIR": os.path.join(worktree, ".git"),
        "GIT_WORK_TREE": worktree,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "LC_ALL": "C",
    }
    return subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", *args],
                          env=env, cwd=worktree, stdin=subprocess.DEVNULL, capture_output=True, check=False)


def _git_root(git_dir: str) -> dict:
    worktree = os.path.dirname(git_dir)
    for rel in ("commondir", os.path.join("objects", "info", "alternates")):
        if os.path.lexists(os.path.join(git_dir, rel)):
            raise Refusal(f"nested repo links outside itself ({rel}): {worktree}")
    filters = _git(worktree, "config", "--get-regexp", r"^filter\.")
    if filters.returncode != 1:
        raise Refusal(f"nested repo defines filter drivers (or config failed); status would run them: {worktree}")

    head_run = _git(worktree, "rev-parse", "--verify", "-q", "HEAD^{commit}")
    if head_run.returncode == 0:
        head = head_run.stdout.decode("ascii").strip()
    elif head_run.returncode == 1 and not head_run.stderr:
        head = None
    else:
        raise Refusal(f"git rev-parse failed in nested repo: {worktree}")

    branch_run = _git(worktree, "symbolic-ref", "-q", "HEAD")
    if branch_run.returncode == 0:
        branch = branch_run.stdout.decode("utf-8").strip()
    elif branch_run.returncode == 1:
        branch = None
    else:
        raise Refusal(f"git symbolic-ref failed in nested repo: {worktree}")

    status_run = _git(worktree, "status", "--porcelain=v1", "-z", "--untracked-files=all",
                      "--ignore-submodules=all")
    if status_run.returncode != 0:
        raise Refusal(f"git status failed in nested repo: {worktree}")
    dirty = [record.decode("utf-8") for record in status_run.stdout.split(b"\0")[:-1]]
    return {"path": worktree, "head": head, "branch": branch, "dirty": dirty}


def build_manifest(root: str) -> dict:
    leaves: list = []
    git_dirs: list = []
    _walk(root, leaves, git_dirs)

    def order(path: str) -> bytes:
        return os.path.relpath(path, root).encode("utf-8")

    leaves.sort(key=lambda leaf: order(leaf["source"]))
    git_roots = sorted((_git_root(d) for d in git_dirs), key=lambda g: order(g["path"]))
    return {"schema_version": 1, "root": root, "leaves": leaves, "git_roots": git_roots}


def _inside(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True, help="unit directory to inventory (not a link)")
    parser.add_argument("--out", required=True, help="new manifest file; must not exist")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    out = os.path.abspath(args.out)

    try:
        root_st = os.lstat(root)
    except OSError as exc:
        print(f"unit_manifest: cannot stat root: {exc}", file=sys.stderr)
        return 2
    if not stat.S_ISDIR(root_st.st_mode):
        print(f"unit_manifest: root is not a real directory: {root}", file=sys.stderr)
        return 2
    if os.path.lexists(out):
        print(f"unit_manifest: output exists, never overwritten: {out}", file=sys.stderr)
        return 2
    if _inside(os.path.realpath(os.path.dirname(out)), os.path.realpath(root)):
        print(f"unit_manifest: output lies inside the unit: {out}", file=sys.stderr)
        return 2

    try:
        manifest = build_manifest(root)
        body = canonical(manifest)
    except (Refusal, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        return 1

    try:
        fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    except OSError as exc:
        print(f"unit_manifest: cannot create output, never overwritten: {exc}", file=sys.stderr)
        return 2
    with os.fdopen(fd, "wb") as fh:
        fh.write(body)
    print(json.dumps({"status": "PASS", "manifest": out, "sha256": hashlib.sha256(body).hexdigest(),
                      "leaves": len(manifest["leaves"]), "git_roots": len(manifest["git_roots"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
