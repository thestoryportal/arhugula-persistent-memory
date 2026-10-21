#!/usr/bin/env python3
"""List readers that still name a unit's old source paths.

A lexical scan: every file is read as bytes, never executed or imported. A symlink
contributes its link text; its target is never opened. A spelling the scan cannot
bind (an old path's parent followed by a partial name, as in f"{P}/autoresearch_{x}")
and every binary file are recorded UNVERIFIED (SPEC.md:545-546, :788-791).

  --check --paths F... --relocations MAP        Steps 261-265
  --check --untracked --units DIR --report FILE  Step 266
Exit 0 clean, 1 a reader still names an old path or the report differs, 2 refused.
Without --check it lists readers to stdout, or writes a new --report (never overwrites).
"""
from __future__ import annotations

import argparse
import csv
import errno
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

from ops.migrate import fdsafe

HEADER = ['old', 'new', 'disposition', 'unit']
UNIT_ROWS = 'path-map-rows.tsv'
NAME = rb'[A-Za-z0-9_.-]'
BEFORE = rb'(?<![A-Za-z0-9_./-])'
AFTER = rb'(?![A-Za-z0-9_-]|\.[A-Za-z0-9_-])'


class Refused(Exception):
    pass


def read_rows(path: Path) -> dict[str, str]:
    with fdsafe.hold_root(str(path.parent)) as parent:
        data = fdsafe.read_named(parent, path.name)
    return parse_rows(path, data)


def parse_rows(path: Path, data: bytes) -> dict[str, str]:
    rows = list(csv.reader(io.StringIO(data.decode('utf-8')), delimiter='\t'))
    if not rows or rows[0] != HEADER:
        raise Refused(f'{path}: expected header old<TAB>new<TAB>disposition<TAB>unit')
    mapping = {}
    for number, row in enumerate(rows[1:], 2):
        if len(row) != 4 or not row[0] or not row[1]:
            raise Refused(f'{path}:{number}: malformed row')
        if row[0] == row[1]:
            raise Refused(f'{path}:{number}: identity row {row[0]}')
        if row[0] in mapping:
            raise Refused(f'{path}:{number}: repeated old path {row[0]}')
        mapping[row[0]] = row[1]
    return mapping


def unit_rows(units: Path) -> tuple[dict[str, str], list[Path]]:
    files = []
    mapping = {}

    def visit(entry):
        depth = entry.rel.count('/')
        if depth == 0:
            mode = entry.st.st_mode
            if stat.S_ISREG(mode):
                return
            if not stat.S_ISDIR(mode):
                err = errno.ELOOP if stat.S_ISLNK(mode) else errno.ENOTDIR
                raise fdsafe.Refusal(entry.path, 'is not a directory', err)
        if depth == 1 and entry.name == UNIT_ROWS:
            path = Path(entry.path)
            for old, new in parse_rows(path, fdsafe.read_bytes(entry)).items():
                if old in mapping:
                    raise Refused(f'{path}: old path {old} is in two units')
                mapping[old] = new
            files.append(path)

    with fdsafe.hold_root(str(units)) as parent:
        fdsafe.walk(parent, visit)
    if not files:
        raise Refused(f'{units}: no */{UNIT_ROWS}')
    return mapping, files


def spellings(root: Path, old: str) -> list[str]:
    if old.startswith('/'):
        return [old]
    roots = dict.fromkeys([str(root), os.path.realpath(root)])
    return [old, './' + old] + [f'{r}/{old}' for r in roots]


def matcher(root: Path, olds: list[str]):
    if not olds:
        raise Refused('no old paths to look for')
    owner = {s: old for old in olds for s in spellings(root, old)}
    ordered = sorted(owner, key=len, reverse=True)
    stale = re.compile(BEFORE + b'(' + b'|'.join(re.escape(s.encode()) for s in ordered) + b')' + AFTER)
    names = {}
    for s in owner:
        if s.startswith('/') and '/' in s[1:]:
            parent, name = s.rsplit('/', 1)
            names.setdefault(parent, set()).add(name)
    parents = sorted(names, key=len, reverse=True)
    dynamic = re.compile(BEFORE + b'(' + b'|'.join(re.escape(p.encode()) for p in parents)
                         + b')/(' + NAME + b'*)') if parents else None
    return stale, owner, dynamic, names


def under(base: str, path: str) -> bool:
    return path == base or path.startswith(base.rstrip(os.sep) + os.sep)


def resolve(root: Path, name: str) -> tuple[Path, str]:
    """A path inside root may not leave it, lexically or through a parent symlink.
    Return its required real folder too; an outside absolute path uses /."""
    lexical, real = os.path.normpath(root), os.path.realpath(root)
    path = os.path.normpath(name if os.path.isabs(name) else os.path.join(lexical, name))
    if not os.path.isabs(name) and not under(lexical, path):
        raise Refused(f'{name}: escapes {root}')
    # [LAW:dataflow-not-control-flow] Outside absolute readers carry / as their containment root.
    inside = real if under(lexical, path) or under(real, path) else '/'
    if not under(inside, os.path.realpath(os.path.dirname(path))):
        raise Refused(f'{name}: a parent symlink leaves {root}')
    if not os.path.lexists(path):
        raise Refused(f'{name}: absent')
    return Path(path), inside


def contents(path: Path, inside: str) -> bytes | None:
    """Read a file or a link's own text through a parent held inside the required folder."""
    parent = fdsafe.Dir(os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY), str(path.parent))
    with parent:
        # [LAW:single-enforcer] Read-time containment belongs to the held folder, not its rebound name.
        if not fdsafe.inside(inside, parent.live()):
            raise Refused(f'{path}: a parent symlink leaves {inside}')
        # [LAW:single-enforcer] Both shared readers bind their bytes to this one scan's inode.
        entry = fdsafe.Entry(parent.fd, path.name, str(path), path.name,
                             os.lstat(path.name, dir_fd=parent.fd))
        if stat.S_ISLNK(entry.st.st_mode):
            return fdsafe.read_link(entry)
        if not stat.S_ISREG(entry.st.st_mode):
            return None
        return fdsafe.read_bytes(entry)


def line_of(data, offset: int) -> int:
    return data[:offset].count(b'\n') + 1


def scan_files(root: Path, files: list[str], olds: list[str], skip=(), listed=()) -> dict:
    """files named by the caller must exist; files Git listed may be absent (sparse or deleted)."""
    root = Path(root)
    stale_re, owner, dynamic_re, names = matcher(root, olds)
    skip = {os.path.realpath(p) for p in skip}
    stale, unverified = [], []
    for name in files:
        if name in listed and not os.path.lexists(os.path.join(root, name)):
            unverified.append({'file': name, 'reason': 'absent'})
            continue
        path, inside = resolve(root, name)
        if os.path.realpath(path) in skip and not os.path.islink(path):
            continue
        data = contents(path, inside)
        if data is None:
            unverified.append({'file': name, 'reason': 'not a regular file'})
            continue
        if data[:8] == b'bplist00' or data.find(b'\x00') >= 0:
            unverified.append({'file': name, 'reason': 'binary'})
        for m in stale_re.finditer(data):
            text = m.group(1).decode()
            stale.append({'file': name, 'line': line_of(data, m.start()),
                          'old_text': text, 'old': owner[text]})
        for m in dynamic_re.finditer(data) if dynamic_re else ():
            tail = m.group(2).decode().rstrip('.')
            if data[m.end():m.end() + 1] == b'/':
                continue
            siblings = names[m.group(1).decode()]
            if tail not in siblings and any(n.startswith(tail) for n in siblings):
                unverified.append({'file': name, 'line': line_of(data, m.start()),
                                   'reason': 'dynamic', 'text': m.group(0).decode().rstrip('.')})
    order = lambda r: (r['file'], r.get('line', 0), r.get('reason', ''), r.get('old_text', r.get('text', '')))
    return {'stale': sorted(stale, key=order), 'unverified': sorted(unverified, key=order)}


def list_files(root: Path, untracked: bool) -> list[str]:
    # core.fsmonitor names an executable that ls-files would otherwise run.
    cmd = ['git', '-c', 'core.fsmonitor=false', '-C', str(root), 'ls-files', '-z']
    if untracked:
        cmd += ['--others', '--exclude-standard']
    result = subprocess.run(cmd, capture_output=True, timeout=600)
    if result.returncode != 0:
        raise Refused(f'git ls-files failed: {result.stderr.decode(errors="replace").strip()}')
    return sorted(p.decode() for p in result.stdout.split(b'\0') if p)


def render(report: dict) -> bytes:
    return (json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False) + '\n').encode()


def run(args) -> int:
    root_env = os.environ.get('LLMDB_ROOT')
    if not root_env:
        raise Refused('LLMDB_ROOT is not set')
    root = Path(root_env)
    olds, inputs = {}, []
    if args.relocations:
        olds.update(read_rows(Path(args.relocations)))
        inputs.append(Path(args.relocations))
    if args.units:
        mapping, files = unit_rows(Path(args.units))
        olds.update(mapping)
        inputs += files
    for old in args.old or ():
        olds[old] = ''
    if not (args.paths or args.tracked or args.untracked):
        raise Refused('name a scope: --paths, --tracked or --untracked')
    listed = []
    if args.tracked:
        listed += list_files(root, untracked=False)
    if args.untracked:
        listed += list_files(root, untracked=True)
    files = list(args.paths or ()) + listed
    report_path = Path(args.report) if args.report else None
    skip = inputs + ([root / report_path if not report_path.is_absolute() else report_path]
                     if report_path else [])
    report = scan_files(root, sorted(dict.fromkeys(files)), sorted(olds), skip,
                        set(listed) - set(args.paths or ()))
    text = render(report)
    if not args.check:
        if report_path is None:
            sys.stdout.write(text.decode())
            return 0
        target = report_path if report_path.is_absolute() else root / report_path
        try:
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
        except FileExistsError:
            raise Refused(f'{target}: exists; never overwritten')
        with os.fdopen(fd, 'wb') as handle:
            handle.write(text)
        return 0
    sys.stdout.write(text.decode())
    code = 1 if report['stale'] else 0
    if report_path is not None:
        target = report_path if report_path.is_absolute() else root / report_path
        try:
            with fdsafe.hold_root(str(target.parent)) as parent:
                recorded = fdsafe.read_named(parent, target.name)
        except fdsafe.Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            recorded = None
        if recorded != text:
            print(f'reader_find: {target} differs from this scan', file=sys.stderr)
            code = 1
    for row in report['stale']:
        print(f"reader_find: {row['file']}:{row['line']} names {row['old_text']}", file=sys.stderr)
    return code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--paths', nargs='+')
    parser.add_argument('--tracked', action='store_true')
    parser.add_argument('--untracked', action='store_true')
    parser.add_argument('--relocations')
    parser.add_argument('--units')
    parser.add_argument('--old', nargs='+', help='old source paths of one unit, before its map exists')
    parser.add_argument('--report')
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (Refused, fdsafe.Refusal, OSError, UnicodeDecodeError, csv.Error) as exc:
        print(f'reader_find: refused: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
