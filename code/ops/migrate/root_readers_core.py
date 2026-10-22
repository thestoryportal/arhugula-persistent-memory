"""Pure registry parser and old-root hit classifier (Step 407).

TSV uses CSV quoting (including multiline edits); blank lines and # comments
are ignored. Paths inside the repository are relative, outside paths absolute.
The shell supplies hits and (path, string) counts using those same registry keys,
even after the root moves. Strings are counted as their UTF-8 byte encodings by
the shell, so unrelated non-UTF-8 file bytes need not be decoded.
Pre results export measured counts keyed by zero-based registry row index;
post requires that snapshot, never a measurement from already-repaired bytes.
"""
from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from ops.migrate import fdsafe


def _refuse(where, reason):
    raise fdsafe.Refusal(where, 'EINVAL: ' + reason)


def _text(value, where):
    if not isinstance(value, str) or not value or '\0' in value:
        _refuse(where, 'expected nonempty text without NUL')
    return value


def _path(value, where):
    value = _text(value, where)
    if value.startswith('~') or any(c in value for c in '\r\n\t') or (
            value != '/' and any(p in ('', '.', '..') for p in value.removeprefix('/').split('/'))):
        _refuse(where, 'expected canonical absolute or repo-relative path')
    return value


def _count(value, where):
    if type(value) is not int or value < 0:
        _refuse(where, 'expected nonnegative exact integer')
    return value


# [LAW:types-are-the-program] Each row carries only its kind's operands.
@dataclass(frozen=True)
class Replace:
    path: str
    old: str
    new: str
    count: int | Literal['measured']
    kind: Literal['REPLACE'] = field(default='REPLACE', init=False)

    def __post_init__(self):
        _path(self.path, 'REPLACE.path')
        _text(self.old, 'REPLACE.old')
        _text(self.new, 'REPLACE.new')
        if self.count != 'measured':
            _count(self.count, 'REPLACE.count')


@dataclass(frozen=True)
class Rename:
    src: str
    dst: str
    kind: Literal['RENAME'] = field(default='RENAME', init=False)

    def __post_init__(self):
        _path(self.src, 'RENAME.src')
        _path(self.dst, 'RENAME.dst')


@dataclass(frozen=True)
class Install:
    src: str
    dst: str
    kind: Literal['INSTALL'] = field(default='INSTALL', init=False)

    def __post_init__(self):
        _path(self.src, 'INSTALL.src')
        _path(self.dst, 'INSTALL.dst')
        if self.src.startswith('/') or not self.dst.startswith('/'):
            _refuse('INSTALL', 'source must be repo-relative and destination absolute')


@dataclass(frozen=True)
class Check:
    path: str
    check_id: str
    kind: Literal['CHECK'] = field(default='CHECK', init=False)

    def __post_init__(self):
        _text(self.path, 'CHECK.path')
        _text(self.check_id, 'CHECK.check_id')


@dataclass(frozen=True)
class Stop:
    process_class: str
    kind: Literal['STOP'] = field(default='STOP', init=False)

    def __post_init__(self):
        _text(self.process_class, 'STOP.process_class')


@dataclass(frozen=True)
class Record:
    prefix: str
    reason: str = ''
    kind: Literal['RECORD'] = field(default='RECORD', init=False)

    def __post_init__(self):
        _path(self.prefix, 'RECORD.prefix')
        if not isinstance(self.reason, str) or '\0' in self.reason:
            _refuse('RECORD.reason', 'expected text without NUL')


Row = Replace | Rename | Install | Check | Stop | Record


def parse_registry(text: str) -> tuple[Row, ...]:
    """Parse TSV into immutable rows; refusals name the starting physical line."""
    if not isinstance(text, str):
        _refuse('registry line 1', 'expected text')
    reader = csv.reader(io.StringIO(text, newline=''), delimiter='\t', strict=True)
    schema = {'REPLACE': (Replace, (5,)), 'RENAME': (Rename, (3,)),
              'INSTALL': (Install, (3,)), 'CHECK': (Check, (3,)),
              'STOP': (Stop, (2,)), 'RECORD': (Record, (2, 3))}
    rows = []
    line = 1
    try:
        for cells in reader:
            where = f'registry line {line}'
            line = reader.line_num + 1
            if not cells or cells[0].startswith('#'):
                continue
            if cells[0] not in schema:
                _refuse(where, 'unknown row kind')
            constructor, lengths = schema[cells[0]]
            if len(cells) not in lengths:
                _refuse(where, 'wrong number of fields')
            args = cells[1:]
            if constructor is Replace and args[3] != 'measured':
                # [LAW:parse-dont-validate] Bound decimal text before Python's int limit.
                if not args[3] or len(args[3]) > 18 or any(c not in '0123456789' for c in args[3]):
                    _refuse(where, 'count must be an exact integer or measured')
                args[3] = int(args[3])
            try:
                rows.append(constructor(*args))
            except fdsafe.Refusal as exc:
                _refuse(where, str(exc))
    except csv.Error as exc:
        _refuse(f'registry line {line}', str(exc))
    return tuple(rows)


@dataclass(frozen=True)
class ScanResult:
    classifications: tuple[tuple[str, str], ...]
    findings: tuple[str, ...]
    measured_counts: tuple[tuple[int, int], ...]

    @property
    def exit_status(self) -> int:
        # [LAW:one-source-of-truth] Status cannot diverge from the findings.
        return int(bool(self.findings))


def _mapping(value, where):
    if not isinstance(value, Mapping):
        _refuse(where, 'expected mapping')
    return value


def classify(*, rows: tuple[Row, ...], stage: Literal['pre', 'post'],
             hits: Mapping[str, int], counts: Mapping[tuple[str, str], int],
             old_root_exists: bool, measured_counts: Mapping[int, int]) -> ScanResult:
    """Classify supplied scan facts; missing observations refuse instead of passing."""
    if not isinstance(rows, (tuple, list)) or any(
            type(row) not in (Replace, Rename, Install, Check, Stop, Record) for row in rows):
        _refuse('rows', 'expected registry rows')
    if stage not in ('pre', 'post'):
        _refuse('stage', 'expected pre or post')
    if type(old_root_exists) is not bool:
        _refuse('old_root_exists', 'expected bool')
    for path, count in _mapping(hits, 'hits').items():
        _path(path, 'hits.path')
        _count(count, 'hits.count')
    for key, count in _mapping(counts, 'counts').items():
        if not isinstance(key, tuple) or len(key) != 2:
            _refuse('counts', 'expected (path, string) keys')
        _path(key[0], 'counts.path')
        _text(key[1], 'counts.string')
        _count(count, 'counts.count')
    for index, count in _mapping(measured_counts, 'measured_counts').items():
        _count(index, 'measured_counts.index')
        if _count(count, 'measured_counts.count') == 0:
            _refuse('measured_counts', 'measured count must be positive')
        if index >= len(rows) or not isinstance(rows[index], Replace) or rows[index].count != 'measured':
            _refuse('measured_counts', 'index must name a measured REPLACE row')

    findings, measured = [], []
    replacements = [(i, row) for i, row in enumerate(rows) if isinstance(row, Replace)]
    for index, row in replacements:
        required = (row.old,) if stage == 'pre' else (row.old, row.new)
        for text in required:
            if (row.path, text) not in counts:
                _refuse(row.path, f'missing count for {text!r}')
        old_count = counts[row.path, row.old]
        expected = row.count
        if expected == 'measured':
            if stage == 'pre':
                expected = old_count
                measured.append((index, expected))
                if expected == 0:
                    findings.append(f'{row.path}: measured old count must be positive')
            else:
                if index not in measured_counts:
                    _refuse(row.path, 'missing pre-stage measured count')
                expected = measured_counts[index]
        expected_old = expected if stage == 'pre' else 0
        if old_count != expected_old:
            findings.append(f'{row.path}: old count {old_count}, expected {expected_old}')
        if stage == 'post' and counts[row.path, row.new] != expected:
            findings.append(f'{row.path}: new count {counts[row.path, row.new]}, expected {expected}')
    if stage == 'post' and old_root_exists:
        findings.append('old root still exists')
    prefixes = tuple(row.prefix for row in rows if isinstance(row, Record))
    live = {row.path for _, row in replacements}
    classifications = []
    for path, count in hits.items():
        if count == 0:
            continue
        if any(path == prefix or path.startswith(prefix.rstrip('/') + '/') for prefix in prefixes):
            kind = 'RECORD'
        elif stage == 'pre' and path in live:
            kind = 'LIVE'
        else:
            kind = 'unregistered'
            findings.append(f'{path}: unregistered')
        classifications.append((path, kind))
    return ScanResult(tuple(classifications), tuple(findings), tuple(measured))
