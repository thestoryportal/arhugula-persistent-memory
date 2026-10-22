"""I/O shell for the five journaled switch effects.

Callers journal intent before execute and record done only on exit_code == 0.
Commands are argv prefixes, not shell strings. Deployment supplies launchd's
domain, service and plist, the backup table/environment, and the wait clock.
BACKUP_COMPARE requires displaced (destination, relative path, sha256) evidence
from the first backup's pre-state, retained by the executor in its run folder.
An empty tuple attests that no files were displaced; it is never a default.
Content comparison ignores inode/device/nlink across copies. Unsupported rsync
filter syntax refuses rather than guessing its meaning.
"""
from dataclasses import dataclass
import errno
import fnmatch
import math
import os
import subprocess
from types import MappingProxyType

from ops.migrate import fdsafe, root_manifest
from ops.migrate.root_switch_core import BackupPair, BackupRun, Launchd, Quiesce
from ops.migrate.switch_journal_core import AgentIdentity, BackupCompare, NoIdentity, ResyncP


# [LAW:one-source-of-truth] Journal identities and action operands are imported.
@dataclass(frozen=True)
class EffectResult:
    identity: AgentIdentity | NoIdentity
    exit_code: int
    last_success: tuple[tuple[str, bytes | None], ...] = ()
    stopped: tuple[str, ...] = ()


def _read(path):
    with fdsafe.hold_root(os.path.dirname(path)) as parent:
        data = fdsafe.read_named(parent, os.path.basename(path))
        fdsafe._settled(parent)
        return data


def _text(path):
    try:
        return _read(path).decode('utf-8')
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(path, 'EILSEQ: expected UTF-8') from exc


def _run(command, args=(), env=None, timeout=10):
    with fdsafe.fs(str(command)):
        try:
            return subprocess.run((*command, *args), env=env, capture_output=True,
                                  text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            raise fdsafe.Refusal(str(command), f'ETIMEDOUT: command exceeded {timeout} s') from exc


def launchd(action: Launchd, *, command, domain, service, plist):
    target = domain + '/' + service
    args = {'loaded': ('bootstrap', domain, plist), 'unloaded': ('bootout', target)}
    if action.to_state not in args:
        raise fdsafe.Refusal(target, 'EINVAL: unknown agent state')
    applied = _run(command, args[action.to_state])
    observed = _run(command, ('print', target))
    if observed.returncode == 0 and observed.stdout.strip():
        state = 'loaded'
    elif observed.returncode == 113 and 'Could not find service' in observed.stderr:
        state = 'unloaded'
    else:
        raise fdsafe.Refusal(target, f'EIO: launchctl print: {observed.returncode} {observed.stderr}')
    code = applied.returncode or int(state != action.to_state)
    stops = () if code == 0 else (f'{target}: observed {state}; wanted {action.to_state}; '
                                 f'command exit {applied.returncode}: {applied.stderr}',)
    return EffectResult(AgentIdentity(state), code, stopped=stops)


def quiesce(action: Quiesce, *, command, clock, sleep, timeout, interval):
    if not (math.isfinite(timeout) and timeout >= 0 and math.isfinite(interval) and interval > 0):
        raise fdsafe.Refusal('QUIESCE', 'EINVAL: invalid wait budget')
    deadline = clock() + timeout
    while True:
        result = _run(command, ('-axo', 'pid=,command='))
        if result.returncode:
            raise fdsafe.Refusal(str(command), f'EIO: process probe exit {result.returncode}: {result.stderr}')
        live = []
        for line in result.stdout.splitlines():
            fields = line.split(None, 1)
            if len(fields) != 2 or not fields[0].isdecimal() or int(fields[0]) <= 0:
                raise fdsafe.Refusal(str(command), f'EINVAL: malformed process: {line}')
            if any(pattern in fields[1] for pattern in ('MemitBackup', 'backup_mirror.sh', 'rsync')):
                live.append(line.strip())
        if not live:
            return EffectResult(NoIdentity(), 0)
        remaining = deadline - clock()
        if remaining <= 0:
            return EffectResult(NoIdentity(), 1, stopped=tuple(live))
        sleep(min(interval, remaining))


def _backup(action, command, table, env, timeout):
    lines = _text(table).splitlines()
    if not lines or lines[0] != 'reader\tsource\tdestination\texcludes':
        raise fdsafe.Refusal(table, 'EINVAL: invalid backup header')
    pairs = []
    for line in lines[1:]:
        fields = line.split('\t')
        if len(fields) != 4 or not all(fields) or fields[0] not in ('ssd', 'gdrive', 'intel'):
            raise fdsafe.Refusal(table, 'EINVAL: malformed backup row')
        backend, src, dst, excludes = fields
        if backend == 'ssd':
            if '/' in excludes or excludes == '-':
                raise fdsafe.Refusal(table, 'EINVAL: expected named excludes beside table')
            pairs.append(BackupPair(backend, src, dst, os.path.join(os.path.dirname(table), excludes)))
    if not pairs or tuple(pairs) != action.pairs:
        raise fdsafe.Refusal(table, 'EINVAL: table differs from journal pairs')
    run_env = dict(env, BACKUP_PAIRS=table)
    result = _run(command, env=run_env, timeout=timeout)
    stamps, stops = [], []
    for pair in action.pairs:
        path = pair.dst + '/.last_success'
        try:
            stamp = _read(path)
        except fdsafe.Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            stamp = None
        stamps.append((pair.dst, stamp))
        if result.returncode == 0 and not stamp:
            stops.append(f'{path}: ENOENT: backup returned success without a success stamp')
    if result.returncode:
        stops.append(f'{table}: backup exit {result.returncode}: {result.stderr}')
    return EffectResult(NoIdentity(), result.returncode or int(bool(stops)), tuple(stamps), tuple(stops))


def backup_run(action: BackupRun, *, command, table, env, timeout=None):
    return _backup(action, command, table, env, timeout)


def resync_p(action: ResyncP, *, command, table, env, timeout=None):
    return _backup(action, command, table, env, timeout)


def _manifest(path):
    with fdsafe.hold_root(path) as root:
        return root_manifest.build_manifest(path, root.fd)['leaves']


def _rules(path):
    rules = []
    for line in _text(path).splitlines():
        if not line or line.startswith(('#', ';')):
            continue
        if line.startswith(('+ ', '- ', '!')) or '**' in line or '\\' in line:
            raise fdsafe.Refusal(path, 'ENOTSUP: unsupported exclude: ' + line)
        rules.append(line)
    return tuple(rules)


def _excluded(relative, rules):
    parts = relative.split('/')
    for rule in rules:
        anchored = rule.startswith('/')
        directory = rule.endswith('/')
        pattern = rule.strip('/')
        candidates = ['/'.join(parts[:i]) for i in range(1, len(parts) + (not directory))]
        if not anchored and '/' not in pattern:
            candidates = parts[:-1] if directory else parts
        pattern_parts = pattern.split('/')
        if any(len(value.split('/')) == len(pattern_parts) and all(
                fnmatch.fnmatchcase(part, glob) for part, glob in zip(value.split('/'), pattern_parts))
                for value in candidates):
            return True
    return False


def _content(leaf):
    return tuple(leaf[key] for key in ('kind', 'bytes', 'sha256', 'link_text', 'mode'))


def backup_compare(action: BackupCompare, *, displaced):
    # [LAW:effects-at-boundaries] Inventories observe disk; journal types stay pure.
    stops = []
    destinations = {}
    for pair in action.pairs:
        rules = _rules(pair.excludes)
        source = {os.path.relpath(v['source'], pair.src): _content(v) for v in _manifest(pair.src)
                  if not _excluded(os.path.relpath(v['source'], pair.src), rules)}
        leaves = _manifest(pair.dst)
        destinations[pair.dst] = {os.path.relpath(v['source'], pair.dst): v for v in leaves}
        dest = {name: _content(v) for name, v in destinations[pair.dst].items()
                if not _excluded(name, rules)}
        for name in sorted(source.keys() | dest.keys()):
            if source.get(name) != dest.get(name):
                stops.append(f'{pair.dst}/{name}: EIO: backup content differs')
    for destination, relative, digest in displaced:
        if destination not in destinations or relative.startswith('/') or any(
                part in ('', '.', '..') for part in relative.split('/')):
            raise fdsafe.Refusal(str(destination), 'EINVAL: invalid displaced-file evidence')
        found = False
        for name, leaf in destinations[destination].items():
            parts = name.split('/', 2)
            if (len(parts) == 3 and parts[0] == '.deleted' and parts[1]
                    and parts[2] == relative and leaf['kind'] == 'file' and leaf['sha256'] == digest):
                found = True
                break
        if not found:
            stops.append(f'{destination}/.deleted/<stamp>/{relative}: ENOENT: displaced file missing or changed')
    return EffectResult(NoIdentity(), int(bool(stops)), stopped=tuple(stops))


# [LAW:single-enforcer] Exact action types select effects; there is no default.
_EFFECTS = MappingProxyType({Launchd: launchd, Quiesce: quiesce, BackupRun: backup_run,
                             ResyncP: resync_p, BackupCompare: backup_compare})


def execute(action, **arguments):
    if type(action) not in _EFFECTS:
        raise fdsafe.Refusal(type(action).__name__, 'EINVAL: unknown effect action')
    return _EFFECTS[type(action)](action, **arguments)
