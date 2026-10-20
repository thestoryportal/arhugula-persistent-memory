#!/usr/bin/env python3
"""Re-inventory one unit into a sorted, hashed, no-follow manifest (ICM v2.1 Part 2, Step 201).

Read only. It walks the unit without following any link, hashes regular files, records
symlinks and sockets without opening them, and records each nested `.git` root with its
HEAD, branch and dirty entries. It writes exactly one new file, the --out path, and never
overwrites or deletes it. A regular-file root is a file unit: its only leaf has source = root,
and its git_roots is empty.

Every check binds the object it checks: the root and each directory are opened with
O_NOFOLLOW; the held root's fstat selects a directory walk or a file read through its
parent's fd. Directories are descended through their fds; each leaf is opened or read through its
directory fd and its fstat must equal the scan lstat before and after the read; the output
is created through the opened --out directory fd, whose real path (F_GETPATH) must lie
outside the unit before and after the write. A nested repo whose .git holds anything but
regular files and directories is refused before Git runs. Its .git and config are held open; the
config check reads the held config fd, and after the last Git call both must still be what the path
names, or the result is FAIL. The output fd stays open until its own real path is checked.

Manifest: canonical JSON (sorted keys, "," and ":" separators, UTF-8, no trailing newline)
  {"schema_version": 1, "root": path, "leaves": [LeafRecord...], "git_roots": [GitRoot...]}
LeafRecord follows WIRE-CONTRACTS.md: source, kind, bytes, sha256, link_text, device, inode, nlink.
GitRoot: path, head (sha or null when unborn), branch (full ref or null when detached),
dirty (`git status --porcelain=v1 -z` records).
Leaves and git roots are sorted by the UTF-8 bytes of their path relative to the root.

Exit 0: manifest written; stdout is {"status": "PASS", "manifest", "sha256", "leaves", "git_roots"}.
Exit 1: a refusal (changed during hash, unsupported object, link out of the unit, linked root
        ancestor, unsafe nested repo, unreadable path); stdout is {"status": "FAIL", "reason"};
        nothing written. A failed or raced write is also exit 1: the reason names the output,
        which is left in place (never deleted).
Exit 2: malformed invocation (root neither a real directory nor a regular file,
        output exists or lies inside the root).
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import stat
import subprocess
import sys
from types import MappingProxyType

from ops.migrate import fdsafe

CHUNK = 1 << 20
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
# [LAW:no-ambient-temporal-coupling] A FIFO raced into the root must not block its type check.
ROOT_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
# core.* keys a plain repo carries; any other core key (excludesfile, attributesfile, hookspath, worktree,
# fsmonitor, sshcommand, unknown) can make Git read or run something outside the unit.
CORE_ALLOWED = frozenset(f"core.{k}" for k in ("repositoryformatversion", "filemode", "bare", "logallrefupdates",
                                               "ignorecase", "precomposeunicode", "symlinks"))
PROMISOR_KEYS = ("promisor", "partialclonefilter")
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


class Refusal(Exception):
    """The unit cannot be inventoried safely; stop and write nothing."""


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sig(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)


def _real_path(fd: int) -> str:
    """The path of the object an fd is open on (macOS F_GETPATH), not of whatever a path names now."""
    return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b"\0", 1)[0])


def _lstat_at(dir_fd: int, name: str) -> os.stat_result:
    return os.stat(name, dir_fd=dir_fd, follow_symlinks=False)


def _hash_regular(dir_fd: int, name: str, path: str, before: os.stat_result) -> str:
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise Refusal(f"object changed kind while opening: {path}")
        if _sig(opened) != _sig(before):
            raise Refusal(f"changed before read: {path}")
        digest = hashlib.sha256()
        while chunk := os.read(fd, CHUNK):
            digest.update(chunk)
        if _sig(os.fstat(fd)) != _sig(before):
            raise Refusal(f"changed during hash: {path}")
    finally:
        os.close(fd)
    if _sig(_lstat_at(dir_fd, name)) != _sig(before):
        raise Refusal(f"changed during hash: {path}")
    return digest.hexdigest()


def _leaf(dir_fd: int, name: str, path: str, st: os.stat_result) -> dict:
    mode = st.st_mode
    link_text = None
    if stat.S_ISREG(mode):
        kind, digest = "file", _hash_regular(dir_fd, name, path, st)
    elif stat.S_ISLNK(mode):
        # [LAW:single-enforcer] The fd pins the scanned link; its text cannot change in place.
        link_text = os.fsdecode(fdsafe.read_link(fdsafe.Entry(dir_fd, name, path, name, st)))
        kind, digest = "symlink", hashlib.sha256(os.fsencode(link_text)).hexdigest()
    elif stat.S_ISSOCK(mode):
        kind, digest = "socket", EMPTY_SHA
    else:
        raise Refusal(f"unsupported object kind {stat.filemode(mode)}: {path}")
    return {"source": path, "kind": kind, "bytes": st.st_size, "sha256": digest, "link_text": link_text,
            "device": st.st_dev, "inode": st.st_ino, "nlink": st.st_nlink}


def _walk(dir_fd: int, directory: str, leaves: list, git_dirs: list, in_git: bool) -> None:
    """Walk the directory open on dir_fd. The path lstat is the scan reference; each object is then
    reached only through dir_fd and must be that same object, so a swapped path refuses."""
    with os.scandir(dir_fd) as it:
        names = sorted((entry.name for entry in it), key=os.fsencode)
    for name in names:
        path = os.path.join(directory, name)
        st = os.lstat(path)
        if name == ".git" and not stat.S_ISDIR(st.st_mode):
            raise Refusal(f"nested .git is not a directory (link to another git dir): {path}")
        if in_git and not (stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode)):
            raise Refusal(f"nested repo has a link or special file inside .git; Git would follow it: {path}")
        if stat.S_ISDIR(st.st_mode):
            fd = os.open(name, DIR_FLAGS, dir_fd=dir_fd)
            try:
                opened = os.fstat(fd)
                if (opened.st_dev, opened.st_ino) != (st.st_dev, st.st_ino):
                    raise Refusal(f"directory changed during walk: {path}")
                if name == ".git":
                    git_dirs.append(path)
                _walk(fd, path, leaves, git_dirs, in_git or name == ".git")
            finally:
                os.close(fd)
        else:
            leaves.append(_leaf(dir_fd, name, path, st))


def _git(worktree: str, *args: str) -> subprocess.CompletedProcess:
    return _run_git(worktree, args, subprocess.DEVNULL)


def _run_git(worktree: str, args: tuple, stdin) -> subprocess.CompletedProcess:
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "GIT_DIR": os.path.join(worktree, ".git"),
        "GIT_WORK_TREE": worktree,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
        "LC_ALL": "C",
    }
    return subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", *args],
                          env=env, cwd=worktree, stdin=stdin, capture_output=True, check=False)


def _check_config(worktree: str, config_fd: int) -> None:
    """Read only the held config fd (no includes) and refuse keys that reach outside the unit or write into it."""
    run = _run_git(worktree, ("config", "--file", "-", "--no-includes", "--null", "--list"), config_fd)
    if run.returncode != 0:
        raise Refusal(f"git config could not read the nested repo config: {worktree}")
    for record in run.stdout.split(b"\0")[:-1]:
        key = record.split(b"\n", 1)[0].decode("utf-8")
        section = key.split(".", 1)[0]
        if section in ("include", "includeif"):
            raise Refusal(f"nested repo config includes another file ({key}): {worktree}")
        if section == "core" and key not in CORE_ALLOWED:
            raise Refusal(f"nested repo config sets {key}; Git could read or run outside the unit: {worktree}")
        # extensions.* changes how Git reads the repo (worktreeConfig adds config.worktree); a promisor or
        # partial-clone remote lets Git fetch objects and write packs into the unit.
        if section == "extensions" or (section == "remote" and key.rsplit(".", 1)[-1] in PROMISOR_KEYS):
            raise Refusal(f"nested repo config sets {key}; Git could read outside or write into the unit: {worktree}")


def _git_root(git_dir: str) -> dict:
    worktree = os.path.dirname(git_dir)
    git_fd = os.open(git_dir, DIR_FLAGS)
    try:
        real = _real_path(git_fd)
        if real != git_dir:
            raise Refusal(f"nested .git is reached through a link (real path {real}): {git_dir}")
        try:
            config_fd = os.open("config", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=git_fd)
        except OSError as exc:
            raise Refusal(f"cannot open nested repo config without following a link ({exc.strerror}): "
                          f"{os.path.join(git_dir, 'config')}") from exc
        try:
            result = _git_pass(worktree, git_dir, git_fd, config_fd)
            # Git opens .git and its config by path; a swap during the Git calls shows as a changed identity.
            if (_sig(os.fstat(config_fd)) != _sig(os.lstat(os.path.join(git_dir, "config")))
                    or _sig(os.fstat(git_fd)) != _sig(os.lstat(git_dir))):
                raise Refusal(f"nested .git or its config changed while Git ran; Git may have read another file: "
                              f"{worktree}")
        finally:
            os.close(config_fd)
    finally:
        os.close(git_fd)
    return result


def _git_pass(worktree: str, git_dir: str, git_fd: int, config_fd: int) -> dict:
    if not stat.S_ISREG(os.fstat(config_fd).st_mode):
        raise Refusal(f"nested repo config is not a regular file: {git_dir}")
    for rel in ("commondir", os.path.join("objects", "info", "alternates")):
        if os.path.lexists(os.path.join(git_dir, rel)):
            raise Refusal(f"nested repo links outside itself ({rel}): {worktree}")
    try:
        _lstat_at(git_fd, "config.worktree")
    except FileNotFoundError:
        pass
    else:
        raise Refusal(f"nested repo has a config.worktree, a second config file Git would read: {worktree}")
    _check_config(worktree, config_fd)
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


def _file_root(root: str, root_fd: int, leaves: list) -> list:
    """Read the named leaf only while it still denotes the held root."""
    parent_fd = os.open(os.path.dirname(root), DIR_FLAGS)
    try:
        name = os.path.basename(root)
        held = os.fstat(root_fd)
        st = _lstat_at(parent_fd, name)
        # [LAW:single-enforcer] Reuse the leaf reader after binding the parent entry to the held root.
        if (st.st_dev, st.st_ino) != (held.st_dev, held.st_ino):
            raise Refusal(f"root changed after it was opened: {root}")
        leaves.append(_leaf(parent_fd, name, root, st))
    finally:
        os.close(parent_fd)
    return []


def _directory_root(root: str, root_fd: int, leaves: list) -> list:
    git_dirs: list = []
    _walk(root_fd, root, leaves, git_dirs, False)
    return git_dirs


# [LAW:dataflow-not-control-flow] One immutable table owns both admission and scan selection.
ROOT_SCANS = MappingProxyType({stat.S_IFDIR: _directory_root, stat.S_IFREG: _file_root})


def build_manifest(root: str, root_fd: int) -> dict:
    leaves: list = []
    real = _real_path(root_fd)
    if real != root:
        raise Refusal(f"root path has a symlink component (real path {real}): {root}")
    mode = os.fstat(root_fd).st_mode
    scan = ROOT_SCANS.get(stat.S_IFMT(mode))
    if scan is None:
        raise Refusal(f"root is neither a directory nor a regular file ({stat.filemode(mode)}): {root}")
    git_dirs = scan(root, root_fd, leaves)
    # [LAW:no-ambient-temporal-coupling] The scan can move an admitted root's parent.
    after = _real_path(root_fd)
    if after != root:
        raise Refusal(f"root moved during the inventory (real path now {after}): {root}")

    def order(path: str) -> bytes:
        return os.path.relpath(path, root).encode("utf-8")

    leaves.sort(key=lambda leaf: order(leaf["source"]))
    git_roots = sorted((_git_root(d) for d in git_dirs), key=lambda g: order(g["path"]))
    return {"schema_version": 1, "root": root, "leaves": leaves, "git_roots": git_roots}


def _inside(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True, help="unit directory or regular file to inventory (not a link)")
    parser.add_argument("--out", required=True, help="new manifest file; must not exist")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    out = os.path.abspath(args.out)

    try:
        root_st = os.lstat(root)
    except OSError as exc:
        print(f"unit_manifest: cannot stat root: {exc}", file=sys.stderr)
        return 2
    if stat.S_IFMT(root_st.st_mode) not in ROOT_SCANS:
        print(f"unit_manifest: root is neither a real directory nor a regular file: {root}", file=sys.stderr)
        return 2
    if os.path.lexists(out):
        print(f"unit_manifest: output exists, never overwritten: {out}", file=sys.stderr)
        return 2
    try:
        parent_fd = os.open(os.path.dirname(out), DIR_FLAGS)
    except OSError as exc:
        print(f"unit_manifest: cannot open output directory (not followed through a link): {exc}", file=sys.stderr)
        return 2
    try:
        return _inventory(root, out, parent_fd, root_st)
    finally:
        os.close(parent_fd)


def _fail(reason: str) -> int:
    print(json.dumps({"status": "FAIL", "reason": reason}, ensure_ascii=False))
    return 1


def _inventory(root: str, out: str, parent_fd: int, root_st: os.stat_result) -> int:
    if _inside(_real_path(parent_fd), root):
        print(f"unit_manifest: output lies inside the unit: {out}", file=sys.stderr)
        return 2

    try:
        root_fd = os.open(root, ROOT_FLAGS)
    except OSError as exc:
        return _fail(f"{type(exc).__name__}: {exc}")
    try:
        return _write(root, out, parent_fd, root_fd, root_st)
    finally:
        os.close(root_fd)


def _write(root: str, out: str, parent_fd: int, root_fd: int, root_st: os.stat_result) -> int:
    name = os.path.basename(out)
    try:
        # [LAW:no-ambient-temporal-coupling] CLI admission must still describe the object opened.
        held = os.fstat(root_fd)
        if (held.st_dev, held.st_ino) != (root_st.st_dev, root_st.st_ino):
            raise Refusal(f"root changed between lstat and open: {root}")
        manifest = build_manifest(root, root_fd)
        body = canonical(manifest)
        if _inside(_real_path(parent_fd), root):
            raise Refusal(f"output directory moved inside the unit; nothing written: {out}")
    except (Refusal, fdsafe.Refusal, OSError, UnicodeError) as exc:
        return _fail(f"{type(exc).__name__}: {exc}")

    try:
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=parent_fd)
    except OSError as exc:
        print(f"unit_manifest: cannot create output, never overwritten: {exc}", file=sys.stderr)
        return 2
    try:
        try:
            view = memoryview(body)
            while view:
                view = view[os.write(fd, view):]
            # The written file itself, checked while its fd is still open: where it is, not its old name.
            where = _real_path(fd)
            unit = _real_path(root_fd)
            named = os.path.join(_real_path(parent_fd), name)
            if _inside(where, unit):
                problem = f"output landed inside the unit during the write; {where} was written there"
            elif where != named:
                problem = f"output was moved during the write; it is at {where}, not {named}"
            else:
                problem = None
        finally:
            os.close(fd)
    except OSError as exc:
        return _fail(f"{type(exc).__name__}: {exc}; output {out} is incomplete or could not be located, "
                     "and was left in place")
    if problem:
        return _fail(f"{problem}; it was left in place")
    print(json.dumps({"status": "PASS", "manifest": where, "sha256": hashlib.sha256(body).hexdigest(),
                      "leaves": len(manifest["leaves"]), "git_roots": len(manifest["git_roots"])}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
