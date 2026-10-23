"""Run the registry's root switch with explicit paths and commands.

--config names JSON with m, r, home, run, registry, tools, ready, pinned_sha,
git and process argv, python, recovery (Step 422 configuration), backup (Step
423 arguments), pairs (effective SSD table rows), stamp, parent_backup,
scan_roots and reader_commands (command-name to explicit argv). The exclusive
run folder must already exist outside all input roots. It can hold copied code.
No deployment path or command is implicit. --dry-run performs observations only.
--run prints stage names, then PASS or the failed stage and recovery's exit.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
import os
import subprocess
import sys

from ops.migrate import (fdsafe, conserve_core, root_manifest, root_readers,
                        root_reader_checks, root_switch_core, root_readers_core,
                        switch_exec, switch_effects, switch_recover)
# [LAW:one-source-of-truth] Transaction actions and observations stay owned by their cores.
from ops.migrate.root_switch_core import Absent, BackupPair, FileState, Source, PreState, Replace
from ops.migrate.switch_journal_core import Intent


@dataclass(frozen=True)
class StageResult:
    failures: tuple[str, ...] = ()


def _config(path):
    try:
        value = json.loads(root_readers.read_text(path))
    except json.JSONDecodeError as exc:
        raise fdsafe.Refusal(path, 'EINVAL: invalid configuration JSON') from exc
    schemas = dict(m=str, r=str, home=str, run=str, registry=str, tools=str, ready=str,
                   pinned_sha=str, git=(str,), process=(str,), python=str,
                   stamp=str, parent_backup=str, scan_roots=(str,),
                   pairs=((str, str, str, str),))
    expected = set(schemas) | {'recovery', 'backup', 'reader_commands'}
    if type(value) is not dict or set(value) != expected:
        raise fdsafe.Refusal(path, 'EINVAL: configuration keys differ from required fields')
    parsed = {key: switch_recover._argument(value[key], shape, key) for key, shape in schemas.items()}
    for key in ('m', 'r', 'home', 'run', 'registry', 'tools', 'ready', 'parent_backup', 'python'):
        root_reader_checks.canonical(parsed[key])
    for path in parsed['scan_roots']:
        root_reader_checks.canonical(path)
    for key in ('git', 'process'):
        if not parsed[key]:
            raise fdsafe.Refusal(key, 'EINVAL: empty command')
    if not parsed['stamp']:
        raise fdsafe.Refusal('stamp', 'EINVAL: empty stamp')
    try:
        parsed['stamp'].encode('utf-8')
    except UnicodeEncodeError as exc:
        raise fdsafe.Refusal('stamp', 'EILSEQ: stamp is not UTF-8') from exc
    backup = value['backup']
    shape = dict(command=(str,), table=str, env={str: str}, timeout=frozenset((int, float)))
    if type(backup) is not dict or set(backup) != set(shape):
        raise fdsafe.Refusal('backup', 'EINVAL: expected command, table, env, timeout')
    parsed['backup'] = {key: switch_recover._argument(backup[key], typ, key) for key, typ in shape.items()}
    commands = value['reader_commands']
    if type(commands) is not dict:
        raise fdsafe.Refusal('reader_commands', 'EINVAL: expected object')
    parsed['reader_commands'] = {key: switch_recover._argument(argv, (str,), key) for key, argv in commands.items()}
    parsed['recovery'] = value['recovery']
    parsed['effects'] = switch_recover._configuration(value['recovery'])
    if len(parsed['pairs']) != 2 or any(pair[0] != 'ssd' for pair in parsed['pairs']):
        raise fdsafe.Refusal('pairs', 'EINVAL: expected both SSD pairs')
    return parsed


def _command(argv, *, env=None, data=None, timeout=10):
    with fdsafe.fs(str(argv)):
        try:
            result = subprocess.run(argv, input=data, capture_output=True, env=env, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise fdsafe.Refusal(str(argv), f'ETIMEDOUT: command exceeded {timeout} s') from exc
    return result


def _checked(argv):
    result = _command(argv)
    if result.returncode:
        raise fdsafe.Refusal(str(argv), f'EIO: command exit {result.returncode}: {result.stderr!r}')
    try:
        return result.stdout.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(str(argv), 'EILSEQ: command output is not UTF-8') from exc


def _entries(path, select):
    found = []
    with fdsafe.hold_root(path) as held:
        fdsafe.walk(held, lambda entry: found.append(entry.path) if select(entry) else None,
                    descend=lambda entry: False)
        fdsafe._settled(held)
    return tuple(found)


def _observe(c, rows):
    lines = _checked((*c['process'], '-axo', 'pid=,command=')).splitlines()
    processes = []
    for line in lines:
        parts = line.split(None, 1)
        if len(parts) != 2 or not parts[0].isdecimal() or int(parts[0]) <= 0:
            raise fdsafe.Refusal('process', 'EINVAL: malformed process line: ' + line)
        processes.append((int(parts[0]), parts[1]))
    if os.getpid() not in {pid for pid, _ in processes}:
        raise fdsafe.Refusal('process', 'EIO: probe does not list its own caller pid')
    targets, sources = {}, {}
    for row in rows:
        if isinstance(row, (root_readers_core.Replace, root_readers_core.Install)):
            key = row.path if isinstance(row, root_readers_core.Replace) else row.dst
            path = key if key.startswith('/') else c['m'] + '/' + key
            identity, data = switch_exec._read(path)
            targets[key] = (identity if isinstance(identity, Absent) else
                            FileState(data, identity.sha256, identity.mode, c['run'] + '/pre/observed'))
        if isinstance(row, root_readers_core.Install):
            identity, data = switch_exec._read(c['m'] + '/' + row.src)
            if isinstance(identity, Absent):
                raise fdsafe.Refusal(row.src, 'ENOENT: INSTALL source absent')
            sources[row.src] = Source(data, identity.mode)
    with fdsafe.hold_root(c['m']) as m, fdsafe.hold_root(os.path.dirname(c['r'])) as parent:
        m_dev = fdsafe._fstat(m.fd, m.path).st_dev
        r_dev = fdsafe._fstat(parent.fd, parent.path).st_dev
    state = PreState(c['m'], c['r'], m_dev, r_dev, root_readers.exists(c['r']),
                     not _checked((*c['git'], '-C', c['m'], 'status', '--porcelain')),
                     _checked((*c['git'], '-C', c['m'], 'rev-parse', 'HEAD')).strip(), c['pinned_sha'],
                     {row.process_class: tuple(pid for pid, command in processes if row.process_class in command)
                      for row in rows if isinstance(row, root_readers_core.Stop)},
                     _entries(c['tools'], lambda e: e.name.endswith('.lock')),
                     _entries(c['ready'], lambda e: True),
                     switch_recover._agent(c['effects']['LAUNCHD']).state, targets, sources,
                     tuple(BackupPair(*pair) for pair in c['pairs']))
    return root_switch_core.plan(rows, state), targets


def _manifest(path):
    with fdsafe.hold_root(path) as held:
        leaves = root_manifest.build_manifest(path, held.fd)['leaves']
    return {os.path.relpath(leaf['source'], path): leaf for leaf in leaves}


def _create(run, name, data):
    with fdsafe.hold_root(run) as held:
        created = switch_exec._create(held, name, data, 0o600)
        fdsafe.close(created.fd, run + '/' + name)


def _rollback(c):
    # [LAW:single-enforcer] A fresh Step 422 process is the sole inverse path; Step 422 owns its operation limits.
    code_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    result = _command((c['python'], '-B', '-m', 'ops.migrate.switch_recover',
                       '--journal', c['run'] + '/journal'),
                      env=dict(os.environ, PYTHONPATH=code_root, PYTHONDONTWRITEBYTECODE='1'), timeout=None)
    print(result.stderr.decode('utf-8', errors='replace'), end='', file=sys.stderr)
    return result.returncode


def _run(c, rows, seam):
    plan, targets = root_switch_core.Result((), ()), {}
    manifests = {}

    def preconditions() -> StageResult:
        nonlocal plan, targets
        plan, targets = _observe(c, rows)
        return StageResult(plan.failures)

    def effects(action):
        return c['backup'] if action.kind == 'BACKUP_RUN' else c['effects'][action.kind]

    def batch(name, start=None, stop=None) -> StageResult:
        selected = next(batch for batch in plan.batches if batch.name == name)
        switch_exec.execute(selected.actions[slice(start, stop)], c['run'], effect_arguments=effects, seam=seam)
        return StageResult()

    def manifest_m() -> StageResult:
        manifests['pre'] = _manifest(c['m'])
        return StageResult()

    def manifest_r() -> StageResult:
        manifests['post'] = _manifest(c['r'])
        return StageResult()

    def conservation() -> StageResult:
        records = switch_exec.read_journal(c['run']).records
        actions = [(os.path.relpath(r.action.path, c['r']), r.action.pre.sha256,
                    sha256(r.action.post_bytes).hexdigest()) for r in records
                   if isinstance(r, Intent) and isinstance(r.action, Replace)
                   and fdsafe.inside(c['r'], r.action.path)]
        return StageResult(tuple(str(f) for f in conserve_core.compare(manifests['pre'], manifests['post'], actions)))

    def readers() -> StageResult:
        measured = [[i, targets[row.path].data.count(row.old.encode())] for i, row in enumerate(rows)
                    if isinstance(row, root_readers_core.Replace) and row.count == 'measured']
        _create(c['run'], 'pre-readers.json', json.dumps(dict(stage='pre', measured_counts=measured)).encode())
        scans = list(c['scan_roots'])
        for row in rows:
            if isinstance(row, root_readers_core.Rename):
                scans = [row.dst + path[len(row.src):] if fdsafe.inside(row.src, path) else path for path in scans]
        args = ['--root', c['r'], '--old-root', c['m'], '--registry', c['registry'], '--stage', 'post',
                '--pre-report', c['run'] + '/pre-readers.json', '--report', c['run'] + '/post-readers.json']
        for path in scans:
            args.extend(('--scan-root', path))
        code = root_readers.main(args)
        return StageResult(() if code == 0 else (f'root_readers exit {code}; {c["run"]}/post-readers.json',))

    def checks() -> StageResult:
        def runner(command):
            name = command.argv[0]
            if name not in c['reader_commands'] or not c['reader_commands'][name]:
                raise fdsafe.Refusal(name, 'ENOTSUP: explicit reader command unavailable')
            result = _command((*c['reader_commands'][name], *command.argv[1:]),
                              env=dict(os.environ, **dict(command.env)), data=command.stdin)
            return root_reader_checks.Output(result.returncode, result.stdout + result.stderr)
        code = root_reader_checks.main(['--root', c['r'], '--old-root', c['m'], '--registry', c['registry'],
                                        '--out', c['run'] + '/checks.tsv'], home=c['home'], runner=runner)
        return StageResult(() if code == 0 else (f'reader checks exit {code}; {c["run"]}/checks.tsv',))

    def backup() -> StageResult:
        before = _manifest(c['parent_backup'])
        batch('BACKUP')
        failures = []
        for _, _, dst, _ in c['pairs']:
            if switch_effects._read(dst + '/.last_success') != c['stamp'].encode():
                failures.append(dst + '/.last_success: differs from run stamp')
        after = _manifest(c['parent_backup'])
        for name in after.keys() - before.keys():
            parts = name.split('/')
            if parts[0] == '.deleted' and os.path.basename(c['r']) in parts[2:]:
                failures.append(name + ': repo archived under parent backup')
        return StageResult(tuple(failures))

    # [LAW:dataflow-not-control-flow] One stage list owns ordering and the single stop edge.
    stages = (('PRECONDITIONS', preconditions), ('PAUSE', lambda: batch('PAUSE', 0, 1)),
              ('QUIESCE', lambda: batch('PAUSE', 1)), ('MANIFEST_M', manifest_m),
              ('MOVE', lambda: batch('MOVE')), ('REPAIR', lambda: batch('REPAIR')),
              ('MANIFEST_R', manifest_r), ('CONSERVATION', conservation), ('ROOT_READERS', readers),
              ('READER_CHECKS', checks), ('BACKUP_RUN', backup), ('RESUME', lambda: batch('RESUME')))
    for name, stage in stages:
        print(name)
        try:
            seam('stage', name)
            result = stage()
        except fdsafe.Refusal as exc:
            result = StageResult((str(exc),))
        if result.failures:
            print(name + ': ' + '; '.join(result.failures), file=sys.stderr)
            return _rollback(c)
    print('PASS')
    return 0


def main(argv=None, *, seam=lambda *args: None):
    try:
        parser = root_reader_checks.Parser(description=__doc__)
        modes = parser.add_mutually_exclusive_group(required=True)
        modes.add_argument('--dry-run', action='store_true')
        modes.add_argument('--run', action='store_true')
        parser.add_argument('--config', required=True)
        args = parser.parse_args(argv)
        c = _config(args.config)
        rows = root_readers_core.parse_registry(root_readers.read_text(c['registry']))
        roots = (c['m'], c['r'], c['home'], c['tools'], c['ready'], c['parent_backup'], *c['scan_roots'])
        if any(fdsafe.inside(root, c['run']) for root in roots):
            raise fdsafe.Refusal(c['run'], 'EINVAL: run folder lies inside an input root')
        if args.dry_run:
            plan, _ = _observe(c, rows)
            for failure in plan.failures:
                print('PRECONDITIONS: ' + failure, file=sys.stderr)
            return int(bool(plan.failures))
        _create(c['run'], 'recovery.json', json.dumps(c['recovery']).encode())
        _create(c['run'], 'journal', b'')
        return _run(c, rows, seam)
    except fdsafe.Refusal as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
