#!/usr/bin/env python3
"""Write one unit's exact relocation rows, or compose every unit's rows into one map.

Columns are old, new, disposition, unit (SPEC.md:653). A relative new path stays in M
(`move`); an absolute one must lie under V or T (`preserved`). Rows are validated with
resolve_path.relocate over the combined graph: the sealed `_index/path-map.tsv`, every
other unit's rows and the new rows. Any doubt is a refusal (exit 2) and nothing is written.

  write --unit S220 --pairs PAIRS.tsv --units DIR   creates DIR/S220/path-map-rows.tsv
  compose [--check] --units DIR                     prints the composed map, or compares it
                                                    with `_index/icm21-path-map.tsv` (exit 1,
                                                    naming both sha256 and the first differing key)
The row file is created through fds: M is opened once without following a symlink, the walk
to the unit folder opens one component at a time under its parent's fd, and the file is
created O_EXCL under the unit folder's fd. After the write, the file's real path must lie
inside M's real path; if not, it is refused and left in place (never unlinked). An OSError on
a named path is a refusal that names the path and errno. Only Refusal and OSError become
exit 2; any other exception is a bug and surfaces with its traceback.
The sealed `_index/path-map.tsv` and `_index/anchor-map.tsv` are only read.
"""
import argparse
import contextlib
import errno
import fcntl
import hashlib
import os
from pathlib import Path
import re
import stat
import sys

from state.resolve_path import read_path_map, relocate

HEADER = 'old\tnew\tdisposition\tunit\n'
PAIRS_HEADER = 'old\tnew\n'
ROW_FILE = 'path-map-rows.tsv'
RELOCATIONS = '_index/icm21-path-map.tsv'
SEALED = '_index/path-map.tsv'
V_ROOT = '/Volumes/memit/llmdb-preserved/icm21-20261013'
T_ROOT = '/Volumes/memit/llmdb-tools'
UNIT_ID = re.compile(r'S[0-9]{3}')
# TSV and csv readers cannot carry these; such a path needs a human decision.
UNSAFE = re.compile(r'[\x00-\x1f\x7f"]')
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


class Refusal(ValueError):
    """An input the tool will not admit; nothing is written."""


def _under(path: str, root: str) -> bool:
    return path.startswith(root + '/')


def check_path(path: str, label: str) -> None:
    if not path or UNSAFE.search(path):
        raise Refusal(f'{label} {path!r}: empty, or holds a control character or quote')
    parts = path[1:].split('/') if path.startswith('/') else path.split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise Refusal(f'{label} {path!r}: not a normalized exact path')


def disposition(new: str) -> str:
    if not new.startswith('/'):
        return 'move'
    if _under(new, V_ROOT) or _under(new, T_ROOT):
        return 'preserved'
    raise Refusal(f'new {new!r}: an absolute target must lie under {V_ROOT} or {T_ROOT}')


def make_row(old: str, new: str, unit: str, root: str) -> tuple:
    check_path(old, 'old')
    check_path(new, 'new')
    # The sealed map spells every M path relative; an absolute M spelling is a second key.
    if old == root or _under(old, root):
        raise Refusal(f'old {old!r}: a path inside M must be spelled relative to M')
    return (old, new, disposition(new), unit)


def _lines(data: bytes, header: str, label: str) -> list[list[str]]:
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as error:
        raise Refusal(f'{label}: not UTF-8 ({error.reason} at byte {error.start})') from None
    if not text.startswith(header) or not text.endswith('\n') or '\r' in text:
        raise Refusal(f'{label}: expected header {header.strip()!r}, LF line ends '
                         'and a final newline')
    lines = text[len(header):-1].split('\n') if text != header else []
    if not lines:
        raise Refusal(f'{label}: no rows')
    width = header.count('\t') + 1
    rows = [line.split('\t') for line in lines]
    for number, row in enumerate(rows, 2):
        if len(row) != width:
            raise Refusal(f'{label}: row {number} has {len(row)} fields, need {width}')
    return rows


def parse_pairs(data: bytes, unit: str, root: str, label: str) -> list[tuple]:
    return [make_row(old, new, unit, root) for old, new in _lines(data, PAIRS_HEADER, label)]


def parse_unit_rows(data: bytes, unit: str, root: str, label: str) -> list[tuple]:
    rows = []
    for old, new, kind, owner in _lines(data, HEADER, label):
        row = make_row(old, new, unit, root)
        if (kind, owner) != row[2:]:
            raise Refusal(f'{label}: row {old!r} says {kind} {owner}; '
                             f'expected {row[2]} {unit}')
        rows.append(row)
    return rows


def validate(rows: list[tuple], sealed: dict[str, str]) -> None:
    """Refuse duplicates, sealed-map ambiguity and cycles in the combined graph."""
    olds, news = {}, {}
    sealed_names = set(sealed) | {new for new in sealed.values() if new}
    for row in rows:
        old, new, _, unit = row
        if old in olds:
            raise Refusal(f'duplicate old {old!r} in {olds[old][3]} and {unit}')
        olds[old] = row
        if old in sealed and sealed[old] != old:
            raise Refusal(f'old {old!r} ({unit}) is a historical key of the sealed map; '
                             f'its sealed target is {sealed[old]!r}')
        if new in news:
            raise Refusal(f'duplicate target {new!r} from {news[new][3]} and {unit}')
        news[new] = row
        if new in sealed_names:
            raise Refusal(f'new {new!r} ({unit}) is already named by the sealed map')
    graph = {old: new for old, new in sealed.items() if new and new != old}
    graph.update((old, new) for old, new, _, _ in rows)
    if graph:
        try:
            relocate(next(iter(graph)), graph)
        except ValueError as error:  # relocate's refusal of a cycle
            raise Refusal(str(error)) from None


def render(rows: list[tuple]) -> bytes:
    return (HEADER + ''.join('\t'.join(row) + '\n' for row in sorted(rows))).encode('utf-8')


def _units_dir(path: str, root: Path) -> Path:
    units = Path(path).absolute()
    if units.is_symlink() or not units.is_dir():
        raise Refusal(f'--units {path}: not a directory, or a symlink')
    if not units.resolve().is_relative_to(root.resolve()):
        raise Refusal(f'--units {path}: outside the root {root}')
    if not units.is_relative_to(root):
        raise Refusal(f'--units {path}: not spelled under the root {root}')
    return units


def load_units(units: Path, root: Path) -> list[tuple]:
    rows = []
    for entry in sorted(os.scandir(units), key=lambda item: item.name):
        if entry.is_symlink():
            raise Refusal(f'{entry.path}: symlink in the units folder')
        if not entry.is_dir():
            continue
        path = Path(entry.path) / ROW_FILE
        if not os.path.lexists(path):
            continue
        if not stat.S_ISREG(os.lstat(path).st_mode):
            raise Refusal(f'{path}: not a regular file (symlink or special)')
        if not UNIT_ID.fullmatch(entry.name):
            raise Refusal(f'{path}: unit folder name is not a unit ID like S220')
        rows += parse_unit_rows(path.read_bytes(), entry.name, str(root), str(path))
    return rows


@contextlib.contextmanager
def _fs(path):
    """An OSError on a named path is a refusal that names the path and its errno."""
    try:
        yield
    except OSError as error:
        code = errno.errorcode.get(error.errno, str(error.errno))
        raise Refusal(f'{path}: {code} {error.strerror}') from None


def _real(fd: int, path) -> str:
    with _fs(path):
        buffer = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024))
    return os.fsdecode(buffer.split(b'\0', 1)[0])


def _close(fd: int, path) -> None:
    with _fs(path):
        os.close(fd)


def _walk(root_fd: int, root: Path, folder: Path) -> int:
    """Open folder one component at a time under its parent's fd, creating a missing one."""
    fd, path = root_fd, root
    for name in folder.relative_to(root).parts:
        parent, path = fd, path / name
        try:
            with _fs(path):
                try:
                    fd = os.open(name, DIR_FLAGS, dir_fd=parent)
                except FileNotFoundError:
                    os.mkdir(name, dir_fd=parent)
                    fd = os.open(name, DIR_FLAGS, dir_fd=parent)
        finally:
            if parent != root_fd:
                _close(parent, path.parent)
    return fd


def _create(root: Path, folder: Path, target: Path, data: bytes) -> None:
    with _fs(root):
        root_fd = os.open(root, DIR_FLAGS)
    try:
        folder_fd = _walk(root_fd, root, folder)
        try:
            # O_EXCL refuses a file or symlink that appeared after the check above.
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            with _fs(target):
                fd = os.open(ROW_FILE, flags, 0o644, dir_fd=folder_fd)
            try:
                with _fs(f'{target} (left in place, incomplete)'):
                    view = memoryview(data)
                    while view:
                        view = view[os.write(fd, view):]
                written, inside = _real(fd, target), _real(root_fd, root)
                if os.path.commonpath([inside, written]) != inside:
                    raise Refusal(f'wrote {written}, which is outside M {inside}; '
                                     'it was left in place')
            finally:
                _close(fd, target)
        finally:
            _close(folder_fd, folder)
    finally:
        _close(root_fd, root)


def first_differing_key(expected: bytes, actual: bytes):
    """The first row key, in sorted order, whose rows differ between two map files."""
    def by_key(data: bytes) -> dict:
        rows = {}
        for line in data.split(b'\n')[1:]:
            if line:
                rows.setdefault(line.split(b'\t', 1)[0], []).append(line)
        return rows
    left, right = by_key(expected), by_key(actual)
    for key in sorted(left.keys() | right.keys()):
        if left.get(key) != right.get(key):
            return key.decode('utf-8', 'backslashreplace')
    return None


def write(args, root: Path, sealed: dict[str, str]) -> int:
    if not UNIT_ID.fullmatch(args.unit):
        raise Refusal(f'--unit {args.unit!r}: a unit ID looks like S220')
    units = _units_dir(args.units, root)
    folder = units / args.unit
    target = folder / ROW_FILE
    if os.path.lexists(target):
        raise Refusal(f'{target}: row file exists; it is never overwritten')
    rows = parse_pairs(Path(args.pairs).read_bytes(), args.unit, str(root), args.pairs)
    validate(load_units(units, root) + rows, sealed)
    _create(root, folder, target, render(rows))
    print(target)
    return 0


def compose(args, root: Path, sealed: dict[str, str]) -> int:
    rows = load_units(_units_dir(args.units, root), root)
    if not rows:
        raise Refusal(f'--units {args.units}: no unit row files; refusing an empty map')
    validate(rows, sealed)
    data = render(rows)
    if not args.check:
        sys.stdout.write(data.decode('utf-8'))
        return 0
    stored = (root / RELOCATIONS).read_bytes()
    if stored != data:
        key = first_differing_key(data, stored)
        where = (f'first differing key {key!r}' if key is not None else
                 'no row key differs; the header, row order or blank lines differ')
        print(f'path_map_rows: {RELOCATIONS} (sha256 {hashlib.sha256(stored).hexdigest()}) '
              f'differs from the composed unit rows (sha256 {hashlib.sha256(data).hexdigest()}); '
              f'{where}', file=sys.stderr)
        return 1
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    one = commands.add_parser('write')
    one.add_argument('--unit', required=True)
    one.add_argument('--pairs', required=True)
    one.add_argument('--units', required=True)
    many = commands.add_parser('compose')
    many.add_argument('--check', action='store_true')
    many.add_argument('--units', required=True)
    args = parser.parse_args(argv)
    try:
        if not os.environ.get('LLMDB_ROOT'):
            raise Refusal('LLMDB_ROOT is not set')
        root = Path(os.environ['LLMDB_ROOT']).absolute()
        data = (root / SEALED).read_bytes()
        try:
            sealed = read_path_map(data)
        except ValueError as error:  # read_path_map's refusal, or bytes that are not UTF-8
            raise Refusal(f'{SEALED}: {error}') from None
        return (write if args.command == 'write' else compose)(args, root, sealed)
    except (Refusal, OSError) as error:
        print(f'path_map_rows: refused: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
