#!/usr/bin/env python3
"""Write one unit's exact relocation rows, or compose every unit's rows into one map.

Columns are old, new, disposition, unit (SPEC.md:653). A relative new path stays in M
(`move`); an absolute one must lie under V or T (`preserved`). Rows are validated with
resolve_path.relocate over the combined graph: the sealed `_index/path-map.tsv`, every
other unit's rows and the new rows. Any doubt is a refusal (exit 2) and nothing is written.

  write --unit S220 --pairs PAIRS.tsv --units DIR   creates DIR/S220/path-map-rows.tsv
  compose [--check] --units DIR                     prints the composed map, or compares it
                                                    with `_index/icm21-path-map.tsv` (exit 1)
The sealed `_index/path-map.tsv` and `_index/anchor-map.tsv` are only read.
"""
import argparse
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


def _under(path: str, root: str) -> bool:
    return path.startswith(root + '/')


def check_path(path: str, label: str) -> None:
    if not path or UNSAFE.search(path):
        raise ValueError(f'{label} {path!r}: empty, or holds a control character or quote')
    parts = path[1:].split('/') if path.startswith('/') else path.split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise ValueError(f'{label} {path!r}: not a normalized exact path')


def disposition(new: str) -> str:
    if not new.startswith('/'):
        return 'move'
    if _under(new, V_ROOT) or _under(new, T_ROOT):
        return 'preserved'
    raise ValueError(f'new {new!r}: an absolute target must lie under {V_ROOT} or {T_ROOT}')


def make_row(old: str, new: str, unit: str, root: str) -> tuple:
    check_path(old, 'old')
    check_path(new, 'new')
    # The sealed map spells every M path relative; an absolute M spelling is a second key.
    if old == root or _under(old, root):
        raise ValueError(f'old {old!r}: a path inside M must be spelled relative to M')
    return (old, new, disposition(new), unit)


def _lines(data: bytes, header: str, label: str) -> list[list[str]]:
    text = data.decode('utf-8')
    if not text.startswith(header) or not text.endswith('\n') or '\r' in text:
        raise ValueError(f'{label}: expected header {header.strip()!r}, LF line ends '
                         'and a final newline')
    lines = text[len(header):-1].split('\n') if text != header else []
    if not lines:
        raise ValueError(f'{label}: no rows')
    width = header.count('\t') + 1
    rows = [line.split('\t') for line in lines]
    for number, row in enumerate(rows, 2):
        if len(row) != width:
            raise ValueError(f'{label}: row {number} has {len(row)} fields, need {width}')
    return rows


def parse_pairs(data: bytes, unit: str, root: str, label: str) -> list[tuple]:
    return [make_row(old, new, unit, root) for old, new in _lines(data, PAIRS_HEADER, label)]


def parse_unit_rows(data: bytes, unit: str, root: str, label: str) -> list[tuple]:
    rows = []
    for old, new, kind, owner in _lines(data, HEADER, label):
        row = make_row(old, new, unit, root)
        if (kind, owner) != row[2:]:
            raise ValueError(f'{label}: row {old!r} says {kind} {owner}; '
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
            raise ValueError(f'duplicate old {old!r} in {olds[old][3]} and {unit}')
        olds[old] = row
        if old in sealed and sealed[old] != old:
            raise ValueError(f'old {old!r} ({unit}) is a historical key of the sealed map; '
                             f'its sealed target is {sealed[old]!r}')
        if new in news:
            raise ValueError(f'duplicate target {new!r} from {news[new][3]} and {unit}')
        news[new] = row
        if new in sealed_names:
            raise ValueError(f'new {new!r} ({unit}) is already named by the sealed map')
    graph = {old: new for old, new in sealed.items() if new and new != old}
    graph.update((old, new) for old, new, _, _ in rows)
    if graph:
        relocate(next(iter(graph)), graph)


def render(rows: list[tuple]) -> bytes:
    return (HEADER + ''.join('\t'.join(row) + '\n' for row in sorted(rows))).encode('utf-8')


def _units_dir(path: str, root: Path) -> Path:
    units = Path(path).absolute()
    if units.is_symlink() or not units.is_dir():
        raise ValueError(f'--units {path}: not a directory, or a symlink')
    if not units.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'--units {path}: outside the root {root}')
    return units


def load_units(units: Path, root: Path) -> list[tuple]:
    rows = []
    for entry in sorted(os.scandir(units), key=lambda item: item.name):
        if entry.is_symlink():
            raise ValueError(f'{entry.path}: symlink in the units folder')
        if not entry.is_dir():
            continue
        path = Path(entry.path) / ROW_FILE
        if not os.path.lexists(path):
            continue
        if not stat.S_ISREG(os.lstat(path).st_mode):
            raise ValueError(f'{path}: not a regular file (symlink or special)')
        if not UNIT_ID.fullmatch(entry.name):
            raise ValueError(f'{path}: unit folder name is not a unit ID like S220')
        rows += parse_unit_rows(path.read_bytes(), entry.name, str(root), str(path))
    return rows


def write(args, root: Path, sealed: dict[str, str]) -> int:
    if not UNIT_ID.fullmatch(args.unit):
        raise ValueError(f'--unit {args.unit!r}: a unit ID looks like S220')
    units = _units_dir(args.units, root)
    folder = units / args.unit
    target = folder / ROW_FILE
    if os.path.lexists(target):
        raise ValueError(f'{target}: row file exists; it is never overwritten')
    rows = parse_pairs(Path(args.pairs).read_bytes(), args.unit, str(root), args.pairs)
    # load_units refuses a symlinked unit folder, so mkdir and open stay inside the root.
    validate(load_units(units, root) + rows, sealed)
    folder.mkdir(exist_ok=True)
    # O_EXCL also refuses a symlink or file that appeared after the check above.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    with os.fdopen(os.open(target, flags, 0o644), 'wb') as handle:
        handle.write(render(rows))
    print(target)
    return 0


def compose(args, root: Path, sealed: dict[str, str]) -> int:
    rows = load_units(_units_dir(args.units, root), root)
    if not rows:
        raise ValueError(f'--units {args.units}: no unit row files; refusing an empty map')
    validate(rows, sealed)
    data = render(rows)
    if not args.check:
        sys.stdout.write(data.decode('utf-8'))
        return 0
    if (root / RELOCATIONS).read_bytes() != data:
        print(f'path_map_rows: {RELOCATIONS} differs from the composed unit rows',
              file=sys.stderr)
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
        root = Path(os.environ['LLMDB_ROOT']).absolute()
        sealed = read_path_map((root / SEALED).read_bytes())
        return (write if args.command == 'write' else compose)(args, root, sealed)
    except (ValueError, OSError, KeyError) as error:
        print(f'path_map_rows: refused: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
