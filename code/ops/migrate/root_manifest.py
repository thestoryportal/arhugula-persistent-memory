"""Inventory every leaf of a root without following links or running Git.

Canonical JSON uses unit_manifest's envelope and LeafRecord fields plus mode.
Exit 0 writes a new manifest; 1 refuses an unsafe inventory or failed write;
2 rejects an invalid root or output. Existing outputs are always kept.
"""
import argparse
import errno
from functools import partial
import hashlib
import json
import os
import stat
import sys

from ops.migrate import fdsafe, unit_manifest


def _check_utf8(text, path):
    # [LAW:single-enforcer] POSIX text must fit the canonical UTF-8 manifest before creation.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise fdsafe.Refusal(path, f"not UTF-8: {exc}") from exc


def _content_policy(directories, name, path, st, in_git):
    """Git metadata is ordinary content here, never input to a Git process."""
    _check_utf8(path, path)
    if stat.S_ISDIR(st.st_mode):
        directories.append((path, st.st_dev, st.st_ino))


def _leaf(dir_fd, name, path, st):
    entry = fdsafe.Entry(dir_fd, name, path, name, st)
    digest = hashlib.sha256()
    link = None
    if stat.S_ISREG(st.st_mode):
        kind = "file"
        fdsafe.read_leaf(entry, digest.update)
    elif stat.S_ISLNK(st.st_mode):
        kind = "symlink"
        text = fdsafe.read_link(entry)
        digest.update(text)
        link = os.fsdecode(text)
        _check_utf8(link, path)
    elif stat.S_ISSOCK(st.st_mode):
        kind = "socket"
    else:
        raise fdsafe.Refusal(path, "unsupported object kind " + stat.filemode(st.st_mode))
    return dict(source=path, kind=kind, bytes=st.st_size, sha256=digest.hexdigest(),
                link_text=link, device=st.st_dev, inode=st.st_ino, nlink=st.st_nlink,
                mode=stat.S_IMODE(st.st_mode))


def build_manifest(root, root_fd):
    _check_utf8(root, root)
    held = fdsafe.Dir(root_fd, root)
    if held.live() != root:
        raise fdsafe.Refusal(root, "root path has a symlink component")
    with fdsafe.fs(root):
        st = os.fstat(root_fd)
    leaves = []
    directories = []
    if stat.S_ISDIR(st.st_mode):
        try:
            # [LAW:one-source-of-truth] Both inventories use the same traversal.
            unit_manifest.walk(root_fd, root, leaves, [], False, leaf_reader=_leaf,
                               git_policy=partial(_content_policy, directories), boundary=fdsafe.fs)
        except unit_manifest.Refusal as exc:
            raise fdsafe.Refusal(root, str(exc)) from exc
    else:
        with fdsafe.hold_root(os.path.dirname(root)) as parent:
            leaves.append(_leaf(parent.fd, os.path.basename(root), root, st))
    if held.live() != root:
        raise fdsafe.Refusal(root, "root moved during inventory")
    # [LAW:no-ambient-temporal-coupling] Held children must still occupy their scanned paths.
    for path, device, inode in directories:
        with fdsafe.fs(path):
            current = os.lstat(path)
        if (current.st_dev, current.st_ino) != (device, inode):
            raise fdsafe.Refusal(path, "directory moved during inventory")
    leaves.sort(key=lambda leaf: os.fsencode(os.path.relpath(leaf["source"], root)))
    return dict(schema_version=1, root=root, leaves=leaves, git_roots=[])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    root, out = os.path.abspath(args.root), os.path.abspath(args.out)
    phase = 2
    try:
        with fdsafe.fs(root):
            st = os.lstat(root)
        if stat.S_IFMT(st.st_mode) not in unit_manifest.ROOT_SCANS:
            raise fdsafe.Refusal(root, "root is neither a real directory nor a regular file")
        try:
            with fdsafe.fs(out):
                os.lstat(out)
        except fdsafe.Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
        else:
            raise fdsafe.Refusal(out, "output exists, never overwritten")
        with fdsafe.open_out_parent(os.path.dirname(out)) as parent:
            if fdsafe.inside(root, parent.live()):
                raise fdsafe.Refusal(out, "output lies inside the root")
            phase = 1
            with fdsafe.fs(root):
                fd = os.open(root, unit_manifest.ROOT_FLAGS)
            with fdsafe.Dir(fd, root) as held:
                with fdsafe.fs(root):
                    opened = os.fstat(fd)
                if (opened.st_dev, opened.st_ino) != (st.st_dev, st.st_ino):
                    raise fdsafe.Refusal(root, "root changed between lstat and open")
                manifest = build_manifest(root, fd)
                body = unit_manifest.canonical(manifest)
                # A moved output parent is an inventory refusal, not malformed input.
                if fdsafe.inside(held.live(), parent.live()):
                    raise fdsafe.Refusal(out, "output directory moved inside root")
                phase = 2
                created = fdsafe.open_held(parent, os.path.basename(out), [held])
                phase = 1
                try:
                    fdsafe.write_held(created, body)
                    where = fdsafe.settle(created, [held])
                finally:
                    fdsafe.close(created.fd, out + " (created, left in place)")
    except fdsafe.Refusal as exc:
        if phase == 2:
            print(f"root_manifest: {exc}", file=sys.stderr)
        else:
            print(json.dumps(dict(status="FAIL", reason=str(exc))))
        return phase
    print(json.dumps(dict(status="PASS", manifest=where, sha256=hashlib.sha256(body).hexdigest(),
                          leaves=len(manifest["leaves"]), git_roots=0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
