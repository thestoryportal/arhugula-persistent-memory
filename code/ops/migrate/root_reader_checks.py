"""Read-only root-reader checks; one TSV receipt row per registry CHECK.

Grouped checks derive their members from REPLACE/INSTALL rows. Activation
files are sourced, not executable launchers. Shell parsing consumes held bytes
on stdin; workflow tests require an explicit ROOT expansion before invocation.
"""
from __future__ import annotations

import csv
import io
import json
import shlex
import tomllib
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal

from ops.migrate import fdsafe
from ops.migrate.root_readers_core import Check, Install, Replace, parse_registry


@dataclass(frozen=True)
class Result:
    status: Literal['PASS', 'FAIL', 'UNAVAILABLE']
    detail: str


@dataclass(frozen=True)
class Read:
    path: str


@dataclass(frozen=True)
class File:
    data: bytes
    mode: int


@dataclass(frozen=True)
class Command:
    argv: tuple[str, ...]
    env: tuple[tuple[str, str], ...]
    stdin: bytes | None = None


@dataclass(frozen=True)
class Output:
    code: int
    data: bytes


@dataclass(frozen=True)
class Probe:
    kind: str
    path: str
    minimum: int = 1


def canonical(path):
    if not isinstance(path, str) or not path.startswith('/') or any(c in path for c in '\0\n\r\t') or (
            path != '/' and any(p in ('', '.', '..') for p in path[1:].split('/'))):
        raise fdsafe.Refusal(str(path), 'EINVAL: expected canonical absolute path')
    return path


def locate(path, root, home):
    if path.startswith('~/'):
        path = home + path[1:]
    elif not path.startswith('/'):
        path = root + '/' + path
    return canonical(path)


def executable(path):
    p = PurePosixPath(path)
    return (p.name == 'teamdash' or p.suffix in ('.sh', '.zsh') or
            (p.parent.name == 'bin' and p.parent.parent.name == '.venv'
             and p.name.split('.')[0] != 'activate'))


def plan(row, rows, root, old, home):
    # [LAW:one-source-of-truth] Group membership comes from the repair registry.
    paths = tuple(dict.fromkeys(locate(r.dst if isinstance(r, Install) else r.path, root, home)
                               for r in rows if isinstance(r, (Replace, Install)) or
                               isinstance(r, Check) and r.check_id in ('test-ship', 'test-train')))
    if row.check_id in ('exec-bit', 'shell-syntax'):
        return tuple(Probe(row.check_id, p) for p in paths if executable(p))
    if row.check_id == 'lane-status':
        return tuple(Probe(row.check_id, str(PurePosixPath(p).parent)) for p in paths
                     if PurePosixPath(p).name == '.git')
    minimum = max([1] + [r.count for r in rows if isinstance(r, Replace)
                        and r.path == row.path and r.old == old and type(r.count) is int])
    return (Probe(row.check_id, locate(row.path, root, home), minimum),)


def path_count(text, path):
    """Exact path operand or descendant, never a parent or sibling-prefix match."""
    return sum(1 for at in range(len(text)) if text.startswith(path, at) and
               (at == 0 or text[at-1] in ' \t\n\"\'(:=;&|<>') and
               (at+len(path) == len(text) or text[at+len(path)] in '/ \t\n\"\'):*;&|<>'))


def shell_name(text):
    line = text.partition('\n')[0]
    if not line.startswith('#!'):
        return None
    words = shlex.split(line[2:])
    if not words:
        return None
    name = PurePosixPath(words[0]).name
    if name == 'env' and len(words) == 2:
        name = words[1]
    return name if name in ('bash', 'zsh') else None


def has_root_override(text):
    lines = tuple(line.strip().removeprefix('export ') for line in text.splitlines()
                  if not line.lstrip().startswith('#'))
    expansions = ('${ROOT}', '${ROOT:-', '${ROOT:?')
    assignments = tuple(line.partition('=')[2].lstrip('"') for line in lines if line.startswith('ROOT='))
    return all(value.startswith(expansions) for value in assignments) and any(
        any(token in line for token in expansions) or '$ROOT/' in line or '$ROOT"' in line or '$ROOT ' in line
        for line in lines)


def verdict(ok, detail):
    return Result('PASS' if ok else 'FAIL', detail)


def schema_result(probe, text, root, old):
    try:
        data = tomllib.loads(text) if probe.kind == 'codex-project' else json.loads(text)
    except (json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        return Result('FAIL', str(exc))
    if not isinstance(data, dict):
        return Result('FAIL', 'expected object')
    if probe.kind in ('claude-project', 'codex-project'):
        projects = data.get('projects')
        return verdict(isinstance(projects, dict) and isinstance(projects.get(root), dict),
                       'projects must contain the exact root as a table/object')
    if probe.kind == 'plugins-project':
        plugins = data.get('plugins')
        ok = isinstance(plugins, dict) and any(
            isinstance(entries, list) and any(isinstance(entry, dict) and entry.get('projectPath') == root
                                             for entry in entries) for entries in plugins.values())
        return verdict(ok, 'plugins entries must contain the exact projectPath')
    permissions = data.get('permissions')
    allow = permissions.get('allow') if isinstance(permissions, dict) else None
    if not isinstance(allow, list) or not all(isinstance(rule, str) for rule in allow):
        return Result('FAIL', 'permissions.allow must be a list of strings')
    return verdict(not any(path_count(rule, old) for rule in allow) and
                   sum(path_count(rule, root) for rule in allow) >= probe.minimum,
                   'allow rules must name the root, never the old root; required count '+str(probe.minimum))


def advance(probe, observations, root, old, home):
    """Pure state transition: observations -> next read/command or terminal result."""
    kind, path = probe.kind, probe.path
    env = (('HOME', home), ('PYTHONDONTWRITEBYTECODE', '1'), ('GIT_OPTIONAL_LOCKS', '0'), ('ROOT', root))
    direct = {'venv-prefix': (path, '-B', '-c', 'import sys; print(sys.prefix)'),
              'console-version': (path, '--version'),
              'lane-status': ('git', '--no-optional-locks', '-C', path, 'status', '--porcelain')}
    readers = ('gitdir', 'plist', 'claude-project', 'plugins-project', 'settings-rules',
               'codex-project', 'exec-bit', 'shell-syntax', 'test-ship', 'test-train')
    if kind not in readers and kind not in direct:
        return Result('UNAVAILABLE', 'unknown CHECK class '+kind)
    if not observations:
        return Command(direct[kind], env) if kind in direct else Read(path)
    last = observations[-1]
    if isinstance(last, Output):
        text = last.data.decode('utf-8', errors='replace')
        ok = last.code == 0
        if kind == 'venv-prefix':
            ok = ok and text.rstrip('\n') == root + '/.venv'
        if kind == 'console-version':
            ok = ok and bool(text.strip())
        return verdict(ok, 'exit '+str(last.code)+': '+text[-2000:])
    if kind == 'exec-bit':
        return verdict(bool(last.mode & 0o111), path+': executable bits '+oct(last.mode & 0o777))
    if kind == 'plist':
        return Command(('plutil', '-lint', '-'), env, last.data)
    try:
        text = last.data.decode('utf-8')
    except UnicodeDecodeError as exc:
        return Result('FAIL', str(exc))
    if kind == 'gitdir':
        first = observations[0].data.decode('utf-8')
        if len(observations) == 1:
            lane = first.removesuffix('\n')
            if '\n' in lane or not lane.endswith('/.git') or not lane.startswith('/'):
                return Result('FAIL', 'invalid gitdir line: '+first)
            try:
                lane = canonical(lane)
            except fdsafe.Refusal as exc:
                return Result('FAIL', first+' | '+str(exc))
            return Read(lane)
        return verdict(text.removesuffix('\n') == 'gitdir: '+str(PurePosixPath(path).parent),
                       first+' | '+text)
    if kind in ('shell-syntax', 'test-ship', 'test-train'):
        try:
            shell = shell_name(text)
        except ValueError as exc:
            # shlex's documented malformed-quotation error is a reader failure.
            return Result('FAIL', 'invalid shebang: '+str(exc))
        if kind != 'shell-syntax' and not has_root_override(text):
            return Result('UNAVAILABLE', 'no ROOT override in '+path)
        if shell is None:
            if kind == 'shell-syntax' and PurePosixPath(path).suffix not in ('.sh', '.zsh'):
                return Result('PASS', path+': not a bash/zsh script')
            return Result('UNAVAILABLE', 'unsupported shell shebang in '+path)
        return Command((shell, '-n'), env, last.data) if kind == 'shell-syntax' else Command((shell, path), env)
    return schema_result(probe, text, root, old)


def combine(results):
    if not results:
        return Result('UNAVAILABLE', 'no registered members')
    status = 'FAIL' if any(r.status == 'FAIL' for r in results) else (
        'UNAVAILABLE' if any(r.status == 'UNAVAILABLE' for r in results) else 'PASS')
    return Result(status, ' | '.join(r.detail for r in results))


def receipt(rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(('path', 'check', 'status', 'detail'))
    for row, result in rows:
        writer.writerow((row.path, row.check_id, result.status, json.dumps(result.detail, ensure_ascii=True)))
    return stream.getvalue(), int(any(result.status != 'PASS' for _, result in rows))


# I/O shell: W13 keeps this boundary in the same ticket/module.
import argparse
import errno
import os
import subprocess
import sys


def run_command(command):
    env = {name: value for name, value in os.environ.items() if not name.startswith('GIT_')}
    env.update(command.env)
    result = subprocess.run(command.argv, input=command.stdin, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env, check=False)
    return Output(result.returncode, result.stdout)


class Effects:
    """[LAW:effects-at-boundaries] All observations pass through this seam."""
    def __init__(self, runner):
        self.runner = runner

    def __call__(self, action):
        if isinstance(action, Command):
            return self.runner(action)
        path = action.path
        parent_path, name = os.path.split(path)
        with fdsafe.hold_root(parent_path) as parent:
            found = []

            def visit(entry):
                if entry.name == name:
                    if parent.live() != parent.path:
                        raise fdsafe.Refusal(path, 'ESTALE: parent moved')
                    found.append(File(fdsafe.read_bytes(entry), entry.st.st_mode))

            fdsafe.walk(parent, visit, descend=lambda entry: False)
            if not found:
                raise fdsafe.Refusal(path, 'missing reader', errno.ENOENT)
            return found[0]


def perform(probe, effects, root, old, home):
    observations = []
    # Every protocol has at most two effects: read/read or read/command.
    for _ in range(3):
        action = advance(probe, tuple(observations), root, old, home)
        if isinstance(action, Result):
            return action
        try:
            observations.append(effects(action))
        except fdsafe.Refusal as exc:
            return Result('UNAVAILABLE', str(exc))
        except OSError as exc:
            return Result('UNAVAILABLE', probe.path+': '+errno.errorcode[exc.errno]+': '+str(exc))
    raise RuntimeError('reader protocol exceeded two observations')


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise fdsafe.Refusal('arguments', 'EINVAL: '+message)


def main(argv=None, *, home=None, runner=None, stderr=None):
    stderr = sys.stderr if stderr is None else stderr
    try:
        parser = Parser(description=__doc__)
        for name in ('root', 'old-root', 'registry', 'out'):
            parser.add_argument('--'+name, required=True)
        args = parser.parse_args(argv)
        root, old, registry, out = (canonical(value) for value in (args.root, args.old_root, args.registry, args.out))
        home = canonical(os.path.expanduser('~') if home is None else home)
        effects = Effects(run_command if runner is None else runner)
        with fdsafe.hold_root(root) as held:
            try:
                rows = parse_registry(effects(Read(registry)).data.decode('utf-8'))
            except UnicodeDecodeError as exc:
                raise fdsafe.Refusal(registry, 'EINVAL: '+str(exc)) from exc
            checks = tuple(row for row in rows if isinstance(row, Check))
            if not checks:
                raise fdsafe.Refusal(registry, 'EINVAL: no CHECK rows')
            results = [(row, combine([perform(p, effects, root, old, home)
                                      for p in plan(row, rows, root, old, home)])) for row in checks]
            text, status = receipt(results)
            with fdsafe.open_out_parent(os.path.dirname(out)) as parent:
                fdsafe.create_file(parent, os.path.basename(out), text.encode('utf-8'), (held,))
            return status
    except fdsafe.Refusal as exc:
        print(str(exc)+' [EINVAL]' if exc.errno is None else str(exc), file=stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
