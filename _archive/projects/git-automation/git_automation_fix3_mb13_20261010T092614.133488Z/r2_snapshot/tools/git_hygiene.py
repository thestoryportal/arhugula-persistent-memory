#!/usr/bin/env python3
"""Bounded git hygiene. Worktrees are always kept; --apply deletes eligible branches."""
from __future__ import annotations

import argparse
from contextlib import contextmanager, nullcontext
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time


class Refusal(RuntimeError):
    pass


class Deadline:
    def __init__(self, seconds, clock=time.monotonic, sleep=time.sleep):
        if not 0 < seconds <= 1200:
            raise Refusal('deadline must be between 0 and 1200 seconds')
        self.clock, self.sleep = clock, sleep
        self.end = clock() + seconds

    def remaining(self):
        left = self.end - self.clock()
        if left <= 0:
            raise Refusal('operation deadline exceeded')
        return left


class Repo:
    def __init__(self, root, deadline):
        self.root, self.deadline = Path(root).resolve(), deadline
        self.commands = []

    def run(self, args, *, allowed=(0,), cwd=None, env=None):
        timeout = min(30, self.deadline.remaining())
        command = list(map(str, args))
        environment = dict(os.environ, LLMDB_ROOT=str(self.root), GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1')
        environment.update(env or {})
        environment['GIT_OPTIONAL_LOCKS'] = '0'
        try:
            process = subprocess.Popen(command, cwd=cwd or self.root, env=environment,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       start_new_session=True)
        except OSError as error:
            raise Refusal(f'cannot start {command[0]}: {error}') from error
        try:
            try:
                out, err = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired as error:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass  # It exited between timeout and kill; refusal below still applies.
                process.communicate(timeout=2)
                raise Refusal(f'command deadline exceeded: {command[0]}') from error
        finally:
            process.stdout.close()
            process.stderr.close()
        result = subprocess.CompletedProcess(command, process.returncode, out.decode(), err.decode())
        result.raw_stdout = out
        self.commands.append({'command': command, 'exit_code': result.returncode,
                              'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode not in allowed:
            reason = ' '.join((result.stderr or result.stdout or 'empty error output').split())[:500]
            raise Refusal(f'{command[0]} exited {result.returncode}: {reason}')
        return result

    def git(self, *args, **kwargs):
        return self.run(['git', *args], **kwargs).stdout

    @contextmanager
    def lock(self):
        common = Path(self.git('rev-parse', '--git-common-dir').strip())
        if not common.is_absolute():
            common = self.root / common
        with (common / 'git_automation.lock').open('a') as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise Refusal('another git automation invocation is active') from error
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)


class Gh:
    """All gh calls cross this one adapter; records retain exact command/output."""
    def __init__(self, runner, repository):
        self.runner, self.repository = runner, repository

    def json(self, args, allowed=(0,)):
        command = ['gh', *args]
        if args[0] != 'api':
            command += ['--repo', self.repository]
        result = self.runner.run(command, allowed=allowed)
        if result.returncode == 1:
            message = (result.stderr + result.stdout).strip()
            if args[:2] == ['pr', 'checks'] and message.startswith('no checks reported'):
                return []
            raise Refusal('gh failed: ' + ' '.join(message.split()))
        try:
            return json.loads(result.stdout)
        except (ValueError, TypeError) as error:
            raise Refusal('gh returned empty or invalid JSON') from error

    def pages(self, endpoint, field=None):
        rows = []
        for page in range(1, 21):
            sep = '&' if '?' in endpoint else '?'
            data = self.json(['api', f'{endpoint}{sep}per_page=100&page={page}'])
            batch = data[field] if field else data
            if not isinstance(batch, list):
                raise Refusal('gh pagination returned a non-list')
            rows.extend(batch)
            if len(batch) < 100:
                return rows
        raise Refusal('gh inventory exceeds bounded 20-page limit; incomplete evidence')

    def open_heads(self):
        rows = self.pages(f'repos/{self.repository}/pulls?state=open')
        return {row['head']['ref'] for row in rows}

    def pr(self, number):
        fields = 'number,state,isDraft,isCrossRepository,headRefName,headRefOid,baseRefName,baseRefOid,mergeable,mergeCommit'
        return self.json(['pr', 'view', str(number), '--json', fields])

    def evidence(self, number, sha, post=False):
        checks = [] if post else self.json(['pr', 'checks', str(number), '--json',
                                          'name,state,bucket,workflow,link'], allowed=(0, 1, 8))
        runs_args = ['run', 'list', '--commit', sha, '--limit', '100', '--json',
                     'databaseId,headSha,headBranch,event,workflowName,status,conclusion,url']
        if post:
            runs_args += ['--branch', 'master', '--event', 'push']
        runs = self.json(runs_args)
        if len(runs) >= 100:
            raise Refusal('workflow run list is capped; incomplete evidence')
        base = f'repos/{self.repository}/commits/{sha}'
        native = self.pages(base + '/check-runs?filter=latest', 'check_runs')
        statuses = self.pages(base + '/statuses')
        latest = {}
        for row in statuses:
            latest.setdefault(row['context'], row)
        return {'sha': sha, 'pr_checks': checks, 'check_runs': native,
                'statuses': list(latest.values()), 'runs': runs}

    def ready(self, number):
        self.runner.run(['gh', 'pr', 'ready', str(number), '--repo', self.repository])

    def merge(self, number, sha):
        self.runner.run(['gh', 'pr', 'merge', str(number), '--repo', self.repository,
                         '--merge', '--match-head-commit', sha])

    def master(self):
        return self.json(['api', f'repos/{self.repository}/git/ref/heads/master'])['object']['sha']

    def first_parent(self, sha):
        commit = self.json(['api', f'repos/{self.repository}/git/commits/{sha}'])
        try:
            if commit['sha'] != sha:
                raise Refusal('merge commit evidence SHA differs')
            parent = commit['parents'][0]['sha']
            if not re.fullmatch('[0-9a-f]{40}', parent):
                raise Refusal('merge commit first parent malformed')
            return parent
        except (KeyError, IndexError, TypeError) as error:
            raise Refusal('merge commit first parent unavailable') from error


def repository_name(repo):
    url = repo.git('remote', 'get-url', 'origin').strip()
    found = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([^/]+/[^/]+?)(?:\.git)?', url)
    if not found:
        raise Refusal('origin is not a supported github.com repository URL')
    return found.group(1)


def worktrees(repo):
    rows, row = [], {}
    for token in repo.git('worktree', 'list', '--porcelain', '-z').split('\0'):
        if not token:
            if row:
                rows.append(row)
                row = {}
            continue
        key, _, value = token.partition(' ')
        row[key] = value or True
    if row:
        rows.append(row)
    return rows


def cwd_inventory(repo):
    result = repo.run(['lsof', '-n', '-P', '-a', '-d', 'cwd', '-Fpn'])
    if result.stderr.strip() or not result.stdout.strip():
        raise Refusal('lsof inventory empty or visibility incomplete: ' + result.stderr.strip())
    inventory, pid = {}, None
    for line in result.stdout.splitlines():
        if line.startswith('p') and line[1:].isdigit():
            if pid is not None and pid not in inventory:
                raise Refusal('lsof process has no readable cwd')
            pid = int(line[1:])
        elif line == 'fcwd':
            continue
        elif line.startswith('n/') and pid is not None:
            cwd = Path(line[1:]).resolve()
            if not cwd.is_dir():
                raise Refusal('lsof cwd unreadable or unavailable: ' + line[1:])
            inventory[pid] = cwd
        else:
            raise Refusal('lsof inventory malformed or unreadable')
    if pid not in inventory or os.getpid() not in inventory:
        raise Refusal('lsof inventory missing process cwd; visibility unverified')
    return inventory


def ancestor(repo, sha, master):
    return repo.run(['git', 'merge-base', '--is-ancestor', sha, master], allowed=(0, 1)).returncode == 0


def remote_inventory(repo, master):
    remote, default = {}, None
    for line in repo.git('ls-remote', '--symref', 'origin').splitlines():
        left, right = line.split('\t')
        if left.startswith('ref: ') and right == 'HEAD':
            default = left.removeprefix('ref: refs/heads/')
        elif right.startswith('refs/heads/'):
            remote[right[len('refs/heads/'):]] = left
    if remote.get('master') != master or default not in remote:
        raise Refusal('origin/master stale or remote default unverified; fetch origin before invoking automation')
    return remote, default


def inspect(repo, gh):
    report = {'ok': True, 'errors': [], 'branches': [], 'worktrees': [], 'actions': [],
              'remote_verified': False, 'open_prs_verified': False}
    cached = {}
    local = {}
    for line in repo.git('for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads', 'refs/remotes/origin').splitlines():
        name, sha = line.split()
        if name.startswith('refs/heads/'):
            local[name[len('refs/heads/'):]] = sha
        elif name != 'refs/remotes/origin/HEAD':
            cached[name[len('refs/remotes/origin/'):]] = sha
    master = cached.get('master')
    if not master:
        raise Refusal('origin/master missing; fetch origin before invoking automation')
    remote, default = dict(cached), 'master'
    try:
        remote, default = remote_inventory(repo, master)
        report['remote_verified'] = True
    except Refusal as error:
        report['errors'].append(str(error))
        remote = dict(cached)
    try:
        open_heads = gh.open_heads()
        report['open_prs_verified'] = True
    except (Refusal, KeyError, TypeError) as error:
        report['errors'].append('open-PR inventory unverified: ' + str(error))
        open_heads = set()
    rows = worktrees(repo)
    attached = {r['branch'].removeprefix('refs/heads/') for r in rows if 'branch' in r}
    try:
        inventory = cwd_inventory(repo)
    except Refusal as error:
        report['errors'].append(str(error))
        inventory = None
    report['master_sha'], report['default_branch'] = master, default
    for kind, refs in (('local', local), ('remote', remote)):
        for name, sha in sorted(refs.items()):
            protected = []
            if name in ('master', default):
                protected.append('default/master')
            if name in attached:
                protected.append('checked out in worktree')
            if name in open_heads:
                protected.append('open PR head')
            try:
                merged = ancestor(repo, sha, master)
                unique = int(repo.git('rev-list', '--count', f'{master}..{sha}').strip())
                date = repo.git('show', '-s', '--format=%cI', sha).strip()
            except Refusal as error:
                report['errors'].append(f'{kind} {name}: {error}')
                merged, unique, date = None, None, None
            report['branches'].append({'kind': kind, 'name': name, 'sha': sha, 'merged': merged,
                'classification': 'PROTECTED' if protected else ('MERGED' if merged else 'UNMERGED' if merged is False else 'UNVERIFIED'),
                'protected_reasons': protected, 'unique_commits': unique, 'last_commit_date': date,
                'exists_remotely': name in remote if report['remote_verified'] else None,
                'remote_fresh': report['remote_verified'], 'eligible': merged is True and not protected
                    and report['remote_verified'] and report['open_prs_verified']})
    for row in rows:
        path = Path(row['worktree']).resolve()
        branch = str(row.get('branch', '')).removeprefix('refs/heads/')
        reasons = []
        if path == repo.root:
            reasons.append('current worktree')
        if not branch or branch in ('master', default) or branch in open_heads:
            reasons.append('detached/default/open-PR worktree')
        if 'locked' in row or 'prunable' in row:
            reasons.append('locked or unavailable worktree')
        size = None
        try:
            size = int(repo.run(['du', '-sk', str(path)]).stdout.split()[0]) * 1024
            dirty = bool(repo.run(['git', 'status', '--porcelain=v1', '--untracked-files=all',
                                  '--ignored=matching', '--ignore-submodules=none'], cwd=path).stdout)
            if dirty:
                reasons.append('dirty, untracked, ignored or submodule work')
            if not ancestor(repo, row['HEAD'], master):
                reasons.append('unmerged branch')
        except (Refusal, ValueError, KeyError) as error:
            reasons.append('worktree state unverified: ' + str(error))
        pids = [pid for pid, cwd in (inventory or {}).items() if cwd == path or path in cwd.parents]
        if inventory is None:
            reasons.append('process visibility unverified')
        elif pids:
            reasons.append('process cwd in worktree')
        if not report['remote_verified'] or not report['open_prs_verified']:
            reasons.append('remote/PR protection unverified')
        report['worktrees'].append({'path': str(path), 'branch': branch, 'head_sha': row['HEAD'],
            'eligible': not reasons, 'keep_reasons': reasons, 'cwd_pids': pids,
            'size_before_bytes': size, 'size_after_bytes': size})
    report['manual_removal_candidates'] = [
        {key: row[key] for key in ('path', 'branch', 'head_sha', 'size_before_bytes')}
        for row in report['worktrees'] if row['eligible']]
    report['ok'] = not report['errors']
    return report


def delete_local(repo, branch, expected_sha):
    """Guard the locked branch-deletion transaction against an unreviewed tip."""
    original = Path(repo.git('rev-parse', '--git-path', 'hooks/reference-transaction').strip())
    if not original.is_absolute():
        original = repo.root / original
    original = original.resolve()
    existing = str(original) if original.is_file() and os.access(original, os.X_OK) else None
    # branch -d supplies a zero old OID; the prepared hook can read the locked tip.
    with tempfile.TemporaryDirectory(prefix='git-local-delete-guard-') as directory:
        hook = Path(directory) / 'reference-transaction'
        hook.write_text('#!/usr/bin/env python3\n'
            'import subprocess,sys\n'
            f'expected={expected_sha!r}; ref={"refs/heads/" + branch!r}; original={existing!r}\n'
            'data=sys.stdin.buffer.read(); rows=data.decode().splitlines()\n'
            'fields=rows[0].split() if len(rows)==1 else []\n'
            'if sys.argv[1]=="prepared":\n'
            ' actual=subprocess.run(["git","rev-parse","--verify",ref],capture_output=True,text=True,timeout=5)\n'
            ' if len(fields)!=3 or fields[1:]!=["0"*40,ref] or actual.returncode or actual.stdout.strip()!=expected:\n'
            '  print("REFUSE: local branch SHA moved or unexpected update",file=sys.stderr);sys.exit(1)\n'
            'if original:\n'
            ' result=subprocess.run([original,*sys.argv[1:]],input=data,timeout=30)\n'
            ' sys.exit(result.returncode)\n')
        hook.chmod(0o755)
        repo.git('-c', 'core.hooksPath=' + directory, 'branch', '-d', branch)


def delete_remote(repo, branch, expected_sha):
    """Validate advertised old OID; receive-pack then atomically compares that OID."""
    original = Path(repo.git('rev-parse', '--git-path', 'hooks/pre-push').strip())
    if not original.is_absolute():
        original = repo.root / original
    original = original.resolve()
    existing = str(original) if original.is_file() and os.access(original, os.X_OK) else None
    with tempfile.TemporaryDirectory(prefix='git-delete-guard-') as directory:
        hook = Path(directory) / 'pre-push'
        hook.write_text('#!/usr/bin/env python3\n'
            'import subprocess,sys\n'
            f'expected={expected_sha!r}; ref={"refs/heads/" + branch!r}; original={existing!r}\n'
            'data=sys.stdin.buffer.read(); rows=data.decode().splitlines()\n'
            'fields=rows[0].split() if len(rows)==1 else []\n'
            'if len(fields)!=4 or fields[1]!="0"*40 or fields[2]!=ref or fields[3]!=expected:\n'
            ' print("REFUSE: advertised remote branch SHA moved or unexpected update",file=sys.stderr);sys.exit(1)\n'
            'if original:\n'
            ' result=subprocess.run([original,*sys.argv[1:]],input=data,timeout=30)\n'
            ' sys.exit(result.returncode)\n')
        hook.chmod(0o755)
        repo.git('-c', 'core.hooksPath=' + directory, 'push', 'origin', '--delete', branch)


def recheck_branch(repo, gh, row, master):
    remote, default = remote_inventory(repo, master)
    if repo.git('rev-parse', 'refs/remotes/origin/master').strip() != master:
        raise Refusal('cached master changed; stopped without retry')
    protected = {'master', default} | gh.open_heads()
    protected.update(w['branch'].removeprefix('refs/heads/') for w in worktrees(repo) if 'branch' in w)
    tip = repo.git('rev-parse', '--verify', 'refs/heads/' + row['name']).strip() if row['kind'] == 'local' else remote.get(row['name'])
    if row['name'] in protected or tip != row['sha']:
        raise Refusal('branch tip/protection changed; stopped without retry')


def hygiene(repo, gh, apply=False, lock=True):
    with repo.lock() if apply and lock else nullcontext():
        if apply:
            repo.git('fetch', 'origin')
        report = inspect(repo, gh)
        report['mode'] = 'apply' if apply else 'dry-run'
        if not apply or not report['ok']:
            return report
        try:
            for row in report['branches']:
                if not row['eligible']:
                    continue
                recheck_branch(repo, gh, row, report['master_sha'])
                if row['kind'] == 'local':
                    delete_local(repo, row['name'], row['sha'])
                else:
                    delete_remote(repo, row['name'], row['sha'])
                report['actions'].append({'operation': 'branch-delete', 'kind': row['kind'], 'name': row['name'], 'sha': row['sha']})
            final = inspect(repo, gh)
            report['branches_after'] = final['branches']
            report['worktrees_after'] = final['worktrees']
            report['errors'].extend(final['errors'])
            if final['master_sha'] != report['master_sha']:
                report['errors'].append('master changed during final hygiene verification')
            report['ok'] = final['ok'] and not report['errors']
        except (Refusal, KeyError, TypeError, ValueError, OSError) as error:
            report['errors'].append(str(error))
            report['ok'] = False
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=float, default=300)
    args = parser.parse_args()
    root = Path(os.environ.get('LLMDB_ROOT') or Path.cwd())
    repo = None
    try:
        repo = Repo(root, Deadline(args.timeout))
        report = hygiene(repo, Gh(repo, repository_name(repo)), apply=args.apply)
    except (Refusal, KeyError, ValueError, OSError) as error:
        report = {'ok': False, 'errors': [str(error)], 'actions': [], 'mode': 'apply' if args.apply else 'dry-run'}
    report['command_evidence'] = repo.commands if repo else []
    print(json.dumps(report, indent=2, sort_keys=True))
    for row in report.get('branches', []):
        print(f"{row['classification']} {row['kind']} {row['name']} unique={row['unique_commits']} date={row['last_commit_date']}", file=sys.stderr)
    for row in report.get('worktrees', []):
        print(f"{'MANUAL-REMOVAL-CANDIDATE' if row['eligible'] else 'KEEP'} {row['path']} branch={row['branch']} head={row['head_sha']} bytes={row['size_before_bytes']}->{row['size_after_bytes']} {'; '.join(row['keep_reasons'])}", file=sys.stderr)
    print('PASS: bounded hygiene complete' if report['ok'] else 'REFUSE: ' + ' '.join(report['errors'][0].split()), file=sys.stderr)
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
