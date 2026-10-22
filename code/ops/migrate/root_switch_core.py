"""Pure Step 411 planner. All observations are supplied by the I/O shell.

Targets use registry path keys; sources use INSTALL repo-relative keys. Source
bytes describe the pre-state; INSTALL consumes their repaired bytes. Pairs are
the effective post-repair backup table, supplied as parsed values by the shell.
Malformed/missing observations raise Refusal; failed preconditions/counts return
failures with no batches before INSTALL source consistency is checked.
No path named here is inspected or changed.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Literal

from ops.migrate import fdsafe, root_readers_core as registry


@dataclass(frozen=True)
class FileState:
    data: bytes
    sha256: str
    mode: int
    preimage: str


@dataclass(frozen=True)
class Absent:
    kind: Literal['absent'] = field(default='absent', init=False)


@dataclass(frozen=True)
class Source:
    data: bytes
    mode: int


@dataclass(frozen=True)
class BackupPair:
    backend: str
    src: str
    dst: str
    excludes: str


@dataclass(frozen=True)
class PreState:
    m: str
    r: str
    m_device: int
    r_parent_device: int
    r_exists: bool
    tracked_clean: bool
    head: str
    pinned_sha: str
    processes: Mapping[str, tuple[int, ...]]
    locks: tuple[str, ...]
    markers: tuple[str, ...]
    launchd: Literal['loaded', 'unloaded']
    targets: Mapping[str, FileState | Absent]
    sources: Mapping[str, Source]
    pairs: tuple[BackupPair, ...]


# [LAW:types-are-the-program] The action union has no irrelevant optional operands.
@dataclass(frozen=True)
class Rename:
    src: str
    dst: str
    kind: Literal['RENAME'] = field(default='RENAME', init=False)


@dataclass(frozen=True)
class Replace:
    path: str
    pre: FileState
    post_bytes: bytes
    post_mode: int
    kind: Literal['REPLACE'] = field(default='REPLACE', init=False)


@dataclass(frozen=True)
class Install:
    dst: str
    pre: FileState | Absent
    post_bytes: bytes
    post_mode: int
    kind: Literal['INSTALL'] = field(default='INSTALL', init=False)


@dataclass(frozen=True)
class Check:
    check_id: str
    kind: Literal['CHECK'] = field(default='CHECK', init=False)


@dataclass(frozen=True)
class Launchd:
    from_state: Literal['loaded', 'unloaded']
    to_state: Literal['loaded', 'unloaded']
    kind: Literal['LAUNCHD'] = field(default='LAUNCHD', init=False)


@dataclass(frozen=True)
class Quiesce:
    kind: Literal['QUIESCE'] = field(default='QUIESCE', init=False)


@dataclass(frozen=True)
class BackupRun:
    pairs: tuple[BackupPair, ...]
    kind: Literal['BACKUP_RUN'] = field(default='BACKUP_RUN', init=False)


Action = Rename | Replace | Install | Check | Launchd | Quiesce | BackupRun


@dataclass(frozen=True)
class Batch:
    name: Literal['PAUSE', 'MOVE', 'REPAIR', 'CHECK', 'BACKUP', 'RESUME']
    actions: tuple[Action, ...]


@dataclass(frozen=True)
class Result:
    batches: tuple[Batch, ...]
    failures: tuple[str, ...]


def _require(condition, where, reason):
    if not condition:
        raise fdsafe.Refusal(where, 'EINVAL: ' + reason)


def _absolute(path, where):
    registry._path(path, where)
    _require(path.startswith('/') and path != '/', where, 'expected absolute non-root path')


def _under(path, root):
    return path == root or path.startswith(root + '/')


def _post(path, state):
    if not path.startswith('/'):
        return state.r + '/' + path
    if _under(path, state.m):
        return state.r + path[len(state.m):]
    return path


def _sequence(value, where):
    _require(isinstance(value, (tuple, list)), where, 'expected sequence')
    return value


def _mode(value, where):
    _require(type(value) is int and 0 <= value <= 0o7777, where, 'invalid mode')


def _validate(rows, state):
    """One input boundary; missing observations never mean observed absence."""
    _require(type(state) is PreState, 'pre-state', 'expected PreState')
    _sequence(rows, 'rows')
    _require(all(type(row) in (registry.Replace, registry.Rename, registry.Install,
                              registry.Check, registry.Stop, registry.Record) for row in rows),
             'rows', 'expected parsed registry rows')
    for name in ('m', 'r'):
        _absolute(getattr(state, name), name)
    _require(not (_under(state.m, state.r) or _under(state.r, state.m)),
             'roots', 'roots must be disjoint')
    for name in ('m_device', 'r_parent_device'):
        registry._count(getattr(state, name), name)
    for name in ('r_exists', 'tracked_clean'):
        _require(type(getattr(state, name)) is bool, name, 'expected bool')
    for name in ('head', 'pinned_sha'):
        value = getattr(state, name)
        _require(isinstance(value, str) and len(value) in (40, 64)
                 and all(c in '0123456789abcdef' for c in value), name, 'invalid git sha')
    _require(state.launchd in ('loaded', 'unloaded'), 'launchd', 'invalid state')
    for name in ('locks', 'markers'):
        for value in _sequence(getattr(state, name), name):
            registry._text(value, name)
    for name in ('targets', 'sources', 'processes'):
        registry._mapping(getattr(state, name), name)
    for name, pids in state.processes.items():
        registry._text(name, 'process class')
        for pid in _sequence(pids, name):
            _require(type(pid) is int and pid > 0, name, 'invalid pid')
    for path, pre in state.targets.items():
        registry._path(path, 'target')
        _require(type(pre) in (FileState, Absent), path, 'invalid pre-state')
        if isinstance(pre, FileState):
            _require(type(pre.data) is bytes, path, 'expected bytes')
            _require(pre.sha256 == sha256(pre.data).hexdigest(), path, 'sha256 differs from bytes')
            _mode(pre.mode, path)
            _absolute(pre.preimage, path)
            _require(not (_under(pre.preimage, state.m) or _under(pre.preimage, state.r)),
                     path, 'preimage must be outside moving roots')
    for path, source in state.sources.items():
        registry._path(path, 'source')
        _require(not path.startswith('/'), path, 'source must be repo-relative')
        _require(type(source) is Source, path, 'expected Source')
        _require(type(source.data) is bytes, path, 'expected source bytes')
        _mode(source.mode, path)
    for pair in _sequence(state.pairs, 'pairs'):
        _require(type(pair) is BackupPair, 'pairs', 'expected BackupPair')
        registry._text(pair.backend, 'backend')
        _absolute(pair.src, 'pair source')
        registry._text(pair.dst, 'pair destination')
        _absolute(pair.excludes, 'pair excludes')
    _require(any(pair.backend == 'ssd' for pair in state.pairs), 'pairs', 'missing ssd pairs')
    writers = {}
    for row in rows:
        if isinstance(row, registry.Stop):
            _require(row.process_class in state.processes, row.process_class, 'missing process observation')
        if isinstance(row, (registry.Replace, registry.Install)):
            path = row.path if isinstance(row, registry.Replace) else row.dst
            _require(path in state.targets, path, 'missing target observation')
            target = _post(path, state)
            if target in writers:
                _require(isinstance(row, registry.Replace) and writers[target] == ('REPLACE', path),
                         path, 'ambiguous writers')
            writers[target] = (row.kind, path)
            if isinstance(row, registry.Replace):
                _require(type(state.targets[path]) is FileState, path, 'REPLACE target absent')
            else:
                _require(row.src in state.sources, row.src, 'missing source observation')


def _repair(path, edits, pre):
    """Use original byte spans, so one edit cannot change another's count."""
    failures, spans = [], []
    for index, row in edits:
        old, new = row.old.encode('utf-8'), row.new.encode('utf-8')
        count = pre.data.count(old)
        if (row.count == 'measured' and count == 0) or (row.count != 'measured' and count != row.count):
            failures.append(f'row {index} {path}: count {count}, expected {row.count}')
        start = 0
        while (start := pre.data.find(old, start)) != -1:
            spans.append((start, start + len(old), new))
            start += len(old)
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        failures.append(f'{path}: overlapping replacements')
    parts, end = [], 0
    for start, stop, new in spans:
        parts.extend((pre.data[end:start], new))
        end = stop
    parts.append(pre.data[end:])
    return b''.join(parts), failures


def plan(rows: tuple[registry.Row, ...], state: PreState) -> Result:
    """Produce the complete transaction description, or no executable batches."""
    _validate(rows, state)
    failures = [message for failed, message in (
        (state.r_exists, f'R exists: {state.r}'),
        (state.m_device != state.r_parent_device, 'st_dev differs'),
        (not state.tracked_clean, 'tracked tree dirty'),
        (state.head != state.pinned_sha, 'HEAD differs from pinned sha')) if failed]
    for row in rows:
        if isinstance(row, registry.Stop) and state.processes[row.process_class]:
            failures.append(f'STOP {row.process_class}: {tuple(state.processes[row.process_class])}')
    failures.extend(f'L/tools lock: {lock}' for lock in state.locks)
    failures.extend(f'ready marker: {marker}' for marker in state.markers)
    groups = {}
    for index, row in enumerate(rows):
        if isinstance(row, registry.Replace):
            groups.setdefault(row.path, []).append((index, row))
    repairs = {}
    for path, edits in groups.items():
        pre = state.targets[path]
        post, errors = _repair(path, edits, pre)
        failures.extend(errors)
        repairs[_post(path, state)] = Replace(_post(path, state), pre, post, pre.mode)
    # [LAW:effects-at-boundaries] Failure cannot expose a partial transaction.
    if failures:
        return Result((), tuple(failures))
    moves, actions, checks, emitted = [Rename(state.m, state.r)], [], [], set()
    for row in rows:
        if isinstance(row, registry.Rename):
            moves.append(Rename(_post(row.src, state), _post(row.dst, state)))
        elif isinstance(row, registry.Replace):
            path = _post(row.path, state)
            if path not in emitted:
                actions.append(repairs[path])
                emitted.add(path)
        elif isinstance(row, registry.Install):
            source = state.sources[row.src]
            post = source.data
            source_path = _post(row.src, state)
            if source_path in repairs:
                repair = repairs[source_path]
                _require((source.data, source.mode) == (repair.pre.data, repair.pre.mode),
                         row.src, 'source observation differs from target')
                post = repair.post_bytes
            pre = state.targets[row.dst]
            mode = pre.mode if isinstance(pre, FileState) else source.mode
            actions.append(Install(_post(row.dst, state), pre, post, mode))
        elif isinstance(row, registry.Check):
            checks.append(Check(row.check_id))
    return Result((
        Batch('PAUSE', (Launchd(state.launchd, 'unloaded'), Quiesce())),
        Batch('MOVE', tuple(moves)), Batch('REPAIR', tuple(actions)),
        Batch('CHECK', tuple(checks)),
        Batch('BACKUP', (BackupRun(tuple(pair for pair in state.pairs if pair.backend == 'ssd')),)),
        Batch('RESUME', (Launchd('unloaded', 'loaded'),)),
    ), ())
