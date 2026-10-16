#!/usr/bin/env python3
"""MAESTRO's only merge path. Explicit --apply; default/dry-run never mutates git."""
from __future__ import annotations

import argparse
from contextlib import contextmanager, nullcontext
import copy
import errno
import fcntl
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import urllib.parse

if __package__:
    from . import git_hygiene as H
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import git_hygiene as H
# engine_fingerprint lives in code/memit/, and the vendored `memit` package shadows that name (D5): load it by path.
_fp_spec = importlib.util.spec_from_file_location(
    "engine_fingerprint", Path(__file__).resolve().parents[2] / "memit" / "engine_fingerprint.py")
F = importlib.util.module_from_spec(_fp_spec)
_fp_spec.loader.exec_module(F)


def ci_state(evidence, sha, post=False, push_branch='master'):
    if evidence['sha'] != sha:
        return 'FAIL', 'CI evidence is for a different SHA'
    checks, native, statuses, runs = (evidence[k] for k in ('pr_checks', 'check_runs', 'statuses', 'runs'))
    if not runs or not native or (not post and not checks):
        return 'WAIT', 'CI not started: no checks or exact-commit workflow run'
    for check in evidence.get('all_check_runs', native):
        if check['head_sha'] != sha:
            return 'FAIL', 'check-run head SHA differs'
        if check['status'] != 'completed':
            return 'WAIT', f"check run {check.get('id')} pending"
    for check in native:
        if check['head_sha'] != sha:
            return 'FAIL', 'check-run head SHA differs'
        if check['status'] != 'completed':
            return 'WAIT', 'check run pending'
        if check['conclusion'] != 'success':
            return 'FAIL', 'check run terminal conclusion is not success'
    for status in statuses:
        if not re.fullmatch(r'https://api\.github\.com/repos/[^/]+/[^/]+/statuses/' + re.escape(sha), status['url']):
            return 'FAIL', 'commit status SHA differs'
        if status['state'] == 'pending':
            return 'WAIT', 'commit status pending'
        if status['state'] != 'success':
            return 'FAIL', 'commit status failed'
    latest = {}
    for run in runs:
        if run['headSha'] != sha:
            return 'FAIL', 'workflow run SHA differs'
        if run['status'] != 'completed':
            return 'WAIT', f"workflow run {run['databaseId']} pending ({run['status']})"
        if run['conclusion'] != 'success':
            return 'FAIL', f"workflow run {run['databaseId']} terminal conclusion is not success"
        key = (run['workflowName'], run['event'], run['headBranch'])
        if key not in latest or run['databaseId'] > latest[key]['databaseId']:
            latest[key] = run
    ci_runs = [r for r in latest.values() if r['workflowName'] == 'CI' and
               (not post or (r['headBranch'] == push_branch and r['event'] == 'push'))]
    if not ci_runs:
        return 'FAIL', 'required CI workflow on the exact SHA is missing'
    if not any(c['name'] == 'cpu' for c in native):
        return 'FAIL', 'required cpu check run missing'
    ids = {str(r['databaseId']) for r in ci_runs}
    run_link = r'/actions/runs/(' + '|'.join(ids) + r')/'
    if not any(c['name'] == 'cpu' and re.search(run_link, c.get('html_url', '')) for c in native):
        return 'FAIL', 'native cpu check not linked to the required exact-SHA CI run'
    names = {c['name'] for c in native} | {s['context'] for s in statuses}
    for check in checks:
        if check['state'] in ('PENDING', 'QUEUED', 'IN_PROGRESS', 'EXPECTED'):
            return 'WAIT', 'PR check pending'
        if check['state'] != 'SUCCESS' or check['bucket'] != 'pass':
            return 'FAIL', 'PR check terminal state is not successful'
        if check['name'] not in names:
            return 'FAIL', 'PR check has no exact-SHA check/status evidence'
    if not post:
        mandatory = [c for c in checks if c['name'] == 'cpu' and c['workflow'] == 'CI']
        if not mandatory or any(not re.search(run_link, c['link']) for c in mandatory):
            return 'FAIL', 'PR cpu check not linked to an exact-head CI workflow run'
    return 'PASS', 'all exact-SHA checks and workflow runs completed successfully'


def ci_snapshot(evidence):
    snapshot = {}
    inventories = (('workflow run', 'runs', 'runs', 'databaseId', 'workflowName'),
                   ('check run', 'all_check_runs', 'check_runs', 'id', 'name'),
                   ('commit status', 'all_statuses', 'statuses', 'id', 'context'))
    for kind, inventory, fallback, identity, name in inventories:
        for row in evidence.get(inventory, evidence[fallback]):
            snapshot[kind, row[identity]] = dict(
                name=row[name], **{field: row.get(field) for field in
                                  ('run_attempt', 'status', 'state', 'conclusion', 'updated_at')})
    return snapshot


def ci_differences(before, after):
    before, after = ci_snapshot(before), ci_snapshot(after)
    differences = []
    for key in sorted(before.keys() | after.keys()):
        old, new = before.get(key), after.get(key)
        label = f"{key[0]} {key[1]} ({(new or old)['name']})"
        if old is None:
            differences.append(label + ' added')
        elif new is None:
            differences.append(label + ' removed')
        else:
            for field in old:
                if old[field] != new[field]:
                    differences.append(f'{label} {field} changed from {old[field]!r} to {new[field]!r}')
    return differences


def poll_ci(repo, gh, number, sha, base, wait_s, post=False):
    end = min(repo.deadline.end, repo.deadline.clock() + wait_s)
    backoff, samples = 1, []
    while True:
        repo.deadline.remaining()
        evidence = gh.evidence(number, sha, post=post)
        samples.append(evidence)
        if not post:
            current = gh.pr(number)
            if current['headRefOid'] != sha or current['baseRefOid'] != base:
                raise H.Refusal('PR head/base SHA moved during CI verification')
        state, reason = ci_state(evidence, sha, post)
        if state == 'PASS':
            return {'sha': sha, 'status': 'completed', 'conclusion': 'success', 'samples': samples}
        if state == 'FAIL':
            raise H.Refusal(reason)
        left = end - repo.deadline.clock()
        if left <= 0:
            raise H.Refusal(reason + '; bounded CI wait expired')
        repo.deadline.sleep(min(backoff, left))
        backoff = min(10, backoff * 2)


def stale_base(repo, master, head, mergeable):
    """None when head contains master; otherwise the merge-base overlap evidence and whether the stale base is accepted."""
    if H.ancestor(repo, master, head):
        return None
    bases = repo.git('merge-base', '--all', head, master).split()
    if len(bases) != 1:
        # Criss-cross ancestry: a diff from any one of several bases can hide a shared file.
        return {'accepted': False, 'master_sha': master, 'head_sha': head,
                'merge_bases': bases, 'pr_files': [], 'master_files': [], 'overlap': []}
    base, = bases
    def changed(tip):
        # --no-renames: a rename lists both its old and new path.
        return sorted(set(repo.git('diff', '--name-only', '--no-renames', '-z', base, tip).split('\0')) - {''})
    pr_files, master_files = changed(head), changed(master)
    overlap = sorted(set(pr_files) & set(master_files))
    return {'accepted': not overlap and mergeable == 'MERGEABLE', 'master_sha': master, 'head_sha': head,
            'merge_bases': bases, 'pr_files': pr_files, 'master_files': master_files, 'overlap': overlap}


def new_report(number, dry_run):
    names = ('pr', 'fingerprint', 'branches', 'ci', 'stable_head_base', 'ready', 'merge', 'master_ci', 'post_hygiene')
    return {'ok': False, 'mode': 'dry-run' if dry_run else 'apply', 'pr_number': number,
              'status': 'REFUSED', 'merged': False, 'head_sha': None, 'base_sha': None,
              'merge_sha': None, 'merge_first_parent': None, 'final_ci': None, 'head_ci_audit': None, 'errors': [],
              'stale_base': None,
              'checks': {name: {'status': 'NOT-RUN', 'reason': 'prerequisite unavailable'} for name in names}}


def record_failure(report, error, name=None):
    reason = ' '.join(str(error).split()) or type(error).__name__
    report['ok'] = False
    if report['merged'] and report['status'] != 'MERGED_ON_MOVED_BASE':
        report['status'] = 'MERGED_WITH_FAILURE'
    report['errors'].append((name + ': ' if name else '') + reason)
    return reason


def gate(repo, gh, number, dry_run=True, wait_s=480, report=None):
    if report is None:
        report = new_report(number, dry_run)
    def check(name, action):
        try:
            value = action()
            report['checks'][name] = {'status': 'PASS', 'evidence': value}
            return value
        except BaseException as error:
            reason = record_failure(report, error, name)
            report['checks'][name] = {'status': 'FAIL', 'reason': reason}
            return None
    def read_pr():
        value = gh.pr(number)
        if value['number'] != number or value['state'] != 'OPEN' or value['baseRefName'] != 'master' or value['isCrossRepository']:
            raise H.Refusal('PR must exist, be OPEN, be same-repository and target master')
        if not re.fullmatch('[0-9a-f]{40}', value['headRefOid']) or not re.fullmatch('[0-9a-f]{40}', value['baseRefOid']):
            raise H.Refusal('PR SHA missing or malformed')
        report['head_sha'], report['base_sha'] = value['headRefOid'], value['baseRefOid']
        return value
    def fingerprint():
        result = repo.run([sys.executable, '-B', 'code/memit/engine_fingerprint.py'])
        evidence = {'root': 'PASS', 'output': result.stdout, 'candidate': 'NOT-RUN'}
        if report['head_sha']:
            engine = repo.run(['git', 'show', report['head_sha'] + ':code/memit/vendor/memit/memit_main.py']).raw_stdout
            digest = hashlib.sha256(engine).hexdigest()
            if digest != F.EXPECTED_SHA256 or engine.count(b'_cov_cpu') != F.EXPECTED_COV_CPU_SITES:
                raise H.Refusal('committed PR candidate engine fingerprint failed')
            evidence.update(candidate='PASS', candidate_sha=report['head_sha'], engine_sha256=digest)
        return evidence
    def branch_check():
        inventory = H.hygiene(repo, gh, apply=False)
        if not inventory['ok']:
            raise H.Refusal('hygiene evidence incomplete: ' + '; '.join(inventory['errors']))
        allowed = {'master'}
        allowed.update(w['branch'] for w in inventory['worktrees'] if w['branch'] and Path(w['path']).is_dir())
        if pr:
            allowed.add(pr['headRefName'])
            if inventory['master_sha'] != pr['baseRefOid']:
                raise H.Refusal('PR must include the current origin/master; update branch then obtain fresh CI')
            stale = report['stale_base'] = stale_base(repo, inventory['master_sha'], pr['headRefOid'], pr['mergeable'])
            if stale and not stale['accepted']:
                raise H.Refusal('stale base refused: merge-bases ' + ', '.join(stale['merge_bases']) +
                                ' (exactly one required); files changed on both sides: ' + (', '.join(stale['overlap']) or 'none') +
                                '; mergeable=' + str(pr['mergeable']) + ' (MERGEABLE required); update branch then obtain fresh CI')
        extras = sorted({b['name'] for b in inventory['branches'] if b['name'] not in allowed})
        if extras:
            raise H.Refusal('extra branches remain; run hygiene first and review unmerged extras: ' + ', '.join(extras))
        return inventory
    def stable():
        value = gh.pr(number)
        if value['headRefOid'] != report['head_sha'] or value['baseRefOid'] != report['base_sha'] or gh.master() != report['base_sha']:
            raise H.Refusal('PR head or master/base SHA moved; no automatic retry')
        if value['state'] != 'OPEN' or value['baseRefName'] != 'master' or value['mergeable'] != 'MERGEABLE':
            raise H.Refusal('PR conflicts or mergeability is unknown; operator must resolve')
        return value
    try:
        pr = check('pr', read_pr)
        check('fingerprint', fingerprint)
        check('branches', branch_check)
        if pr:
            check('ci', lambda: poll_ci(repo, gh, number, report['head_sha'], report['base_sha'], wait_s))
            check('stable_head_base', stable)
        if report['errors']:
            return report
        with repo.lock() if not dry_run else nullcontext():
            if dry_run:
                for name in ('ready', 'merge', 'master_ci', 'post_hygiene'):
                    report['checks'][name] = {'status': 'WOULD-RUN', 'reason': 'dry-run; no action',
                        'head_sha': report['head_sha'], 'post_merge_sha': 'returned merge commit, verified separately'}
            else:
                def ready():
                    stable()
                    if pr['isDraft']:
                        gh.ready(number)
                    return 'ready; draft state changed only after all preconditions passed'
                if check('ready', ready) is None:
                    return report
                def merge():
                    stable()
                    fresh = H.hygiene(repo, gh, apply=False)
                    if not fresh['ok']:
                        raise H.Refusal('hygiene protection evidence changed before merge')
                    allowed = {'master', pr['headRefName']} | {w['branch'] for w in fresh['worktrees'] if w['branch'] and Path(w['path']).is_dir()}
                    if any(b['name'] not in allowed for b in fresh['branches']):
                        raise H.Refusal('extra branches appeared before merge')
                    stable()
                    evidence = gh.evidence(number, report['head_sha'])
                    state, reason = ci_state(evidence, report['head_sha'])
                    report['final_ci'] = {'status': state, 'reason': reason, 'evidence': evidence}
                    if state != 'PASS':
                        raise H.Refusal('final exact-head CI refused: ' + reason)
                    differences = ci_differences(report['checks']['ci']['evidence']['samples'][-1], evidence)
                    report['final_ci']['differences'] = differences
                    if differences:
                        raise H.Refusal('CI evidence changed before merge: ' + '; '.join(differences))
                    response = gh.merge(number, report['head_sha'])
                    report['merged'] = True
                    report['merge_sha'] = response['sha']
                    report['status'] = 'MERGED_WITH_FAILURE'
                    merged = gh.pr(number)
                    sha = report['merge_sha']
                    if merged['state'] != 'MERGED' or merged['headRefOid'] != report['head_sha'] or merged['mergeCommit']['oid'] != sha:
                        raise H.Refusal('merge returned no valid exact-head merge commit')
                    parent = gh.first_parent(sha)
                    report['merge_first_parent'] = parent
                    if parent != report['base_sha']:
                        report['status'] = 'MERGED_ON_MOVED_BASE'
                        raise H.Refusal('merged onto a moved base: first parent ' + parent + ' differs from recorded base ' + report['base_sha'])
                    if gh.master() != sha:
                        raise H.Refusal('master tip differs from returned merge commit; post-merge CI not verified')
                    audit = gh.evidence(number, report['head_sha'])
                    differences = ci_differences(evidence, audit)
                    state, reason = ('FAIL', 'CI evidence changed') if differences else ci_state(audit, report['head_sha'])
                    report['head_ci_audit'] = {'status': state, 'reason': reason, 'evidence': audit,
                                               'differences': differences}
                    if differences or state != 'PASS':
                        raise H.Refusal('post-merge head CI audit failed: ' +
                                        ('; '.join(differences) if differences else reason) +
                                        '; detection does not undo the merge')
                    return {'head_sha': report['head_sha'], 'merge_sha': sha, 'first_parent': parent, 'strategy': 'merge commit'}
                if check('merge', merge) is None:
                    return report
                def master_ci():
                    result = poll_ci(repo, gh, number, report['merge_sha'], report['base_sha'], wait_s, post=True)
                    if gh.master() != report['merge_sha']:
                        raise H.Refusal('master moved during post-merge verification')
                    return result
                if check('master_ci', master_ci) is None:
                    return report
                def cleanup():
                    value = H.hygiene(repo, gh, apply=True, lock=False)
                    if not value['ok']:
                        raise H.Refusal('post-merge hygiene refused: ' + '; '.join(value['errors']))
                    return value
                if check('post_hygiene', cleanup) is None:
                    return report
        report['ok'] = True
        report['status'] = 'DRY_RUN_PASS' if dry_run else 'MERGED'
    except BaseException as error:
        record_failure(report, error)
    return report


def failure_receipt(report, repo):
    """Use a separate sink and plain text when report delivery itself fails."""
    def text():
        return (report['status'] + ' ok=false merged=' + str(report['merged']).lower() +
                ' merge_sha=' + str(report['merge_sha']) + ' ' + '; '.join(report['errors']) + '\n')
    try:
        sys.stderr.write(text())
        sys.stderr.flush()
        return
    except BaseException as error:
        record_failure(report, error, 'fallback stderr')
    try:
        directory = (repo.root if repo else Path.cwd()) / 'results/git_merge_gate_receipts'
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', prefix=str(report['merge_sha']) + '-',
                                         suffix='.txt', dir=directory, delete=False) as handle:
            handle.write(text())
            handle.flush()
            os.fsync(handle.fileno())
            report['failure_receipt_path'] = handle.name
    except BaseException as error:
        record_failure(report, error, 'fallback receipt file')
        try:
            os.write(2, text().encode())
        except BaseException as error:
            record_failure(report, error, 'fallback stderr descriptor')


# Batch mode: one train candidate `land/<id>` carries several PRs to master in one CI cycle.
CANDIDATE = re.compile(r'land/[0-9A-Za-z][0-9A-Za-z_-]{0,79}')
SHA = re.compile('[0-9a-f]{40}')
ENGINE = 'code/memit/vendor/memit/memit_main.py'


def bgit(repo, *args, network=False, env=None, allowed=(0,)):
    """Every batch git call: no fsmonitor program, no lazy fetch, no optional locks, no replace refs
    (T201 rulings 2 and 7). Local reads also drop system and global config; a network call keeps
    them because the credential helper lives there."""
    environment = {'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1', 'LC_ALL': 'C'}
    if not network:
        environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    environment.update(env or {})
    return repo.run(['git', '-c', 'core.fsmonitor=false', '--no-optional-locks', *args],
                    env=environment, allowed=allowed)


# The bgit protections as environment, so they also reach git that the gate runs through git_hygiene,
# gh and hooks (T304 ruling 5): command-scope core.fsmonitor=false overrides any repository config.
PROTECT = {'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.fsmonitor', 'GIT_CONFIG_VALUE_0': 'false',
           'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}


class Protected(H.Repo):
    """repo whose every child process gets PROTECT; it shares root, deadline and the command log."""
    def __init__(self, repo):
        self.__dict__ = repo.__dict__

    def run(self, args, **kwargs):
        return super().run(args, **dict(kwargs, env={**PROTECT, **(kwargs.get('env') or {})}))


def live_path(fd):
    """Where the directory an fd holds is now: macOS F_GETPATH, Linux /proc/self/fd."""
    if hasattr(fcntl, 'F_GETPATH'):
        return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0])
    return os.readlink(f'/proc/self/fd/{fd}')


@contextmanager
def scratch(prefix):
    """A new temp directory held by an fd. bound() refuses unless the path is still that directory
    (same st_dev/st_ino, unchanged live path); a replaced path is never removed (T304 ruling 6)."""
    path = tempfile.mkdtemp(prefix=prefix)
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        raise H.Refusal(f'temporary directory {path} replaced after creation: '
                        f'{errno.errorcode.get(error.errno, error.errno)}') from error
    try:
        held, live = os.fstat(fd), live_path(fd)
        def bound():
            now = os.lstat(path)
            if (not stat.S_ISDIR(now.st_mode) or (now.st_dev, now.st_ino) != (held.st_dev, held.st_ino)
                    or live_path(fd) != live):
                raise H.Refusal(f'temporary directory {path} is no longer the directory the gate created')
        bound()
        try:
            yield path, fd, bound
        finally:
            bound()
            shutil.rmtree(path)
    finally:
        os.close(fd)


def remote_tips(repo, *branches):
    """Live origin tips of exactly these branches; a branch absent on origin is absent from the result."""
    refs = ['refs/heads/' + branch for branch in branches]
    tips = {}
    for line in bgit(repo, 'ls-remote', 'origin', *refs, network=True).stdout.splitlines():
        sha, _, ref = line.partition('\t')
        if ref not in refs or not SHA.fullmatch(sha) or ref[len('refs/heads/'):] in tips:
            raise H.Refusal('ls-remote output malformed or ambiguous: ' + line)
        tips[ref[len('refs/heads/'):]] = sha
    return tips


RUN_FIELDS = {'databaseId': 'id', 'headSha': 'head_sha', 'headBranch': 'head_branch', 'event': 'event',
              'workflowName': 'name', 'status': 'status', 'conclusion': 'conclusion', 'url': 'html_url',
              'run_attempt': 'run_attempt', 'updated_at': 'updated_at'}


def candidate_evidence(gh, sha, branch):
    """The Gh.evidence inventories for a push to `branch` (Gh.evidence filters post runs to master)."""
    # Every event's run on this SHA and branch must succeed; ci_state still requires the push run.
    query = urllib.parse.urlencode({'head_sha': sha, 'branch': branch, 'per_page': 100})
    data = gh.json(['api', f'repos/{gh.repository}/actions/runs?{query}'])
    if not isinstance(data, dict) or not isinstance(data.get('workflow_runs'), list):
        raise H.Refusal('workflow run inventory malformed')
    if len(data['workflow_runs']) >= 100:
        raise H.Refusal('workflow run list is capped; incomplete evidence')
    runs = [{key: row[field] for key, field in RUN_FIELDS.items()} for row in data['workflow_runs']]
    base = f'repos/{gh.repository}/commits/{sha}'
    native = gh.pages(base + '/check-runs?filter=latest', 'check_runs')
    all_native = gh.pages(base + '/check-runs?filter=all', 'check_runs')
    statuses = gh.pages(base + '/statuses')
    latest = {}
    for row in statuses:
        latest.setdefault(row['context'], row)
    return {'sha': sha, 'pr_checks': [], 'check_runs': native, 'statuses': list(latest.values()),
            'runs': runs, 'all_check_runs': all_native, 'all_statuses': statuses}


def bounded(repo, wait_s, step):
    """Poll step() -> (state, reason, value) with backoff until PASS, FAIL or the bounded wait expires."""
    end = min(repo.deadline.end, repo.deadline.clock() + wait_s)
    backoff = 1
    while True:
        repo.deadline.remaining()
        state, reason, value = step()
        if state == 'PASS':
            return value
        if state == 'FAIL':
            raise H.Refusal(reason)
        left = end - repo.deadline.clock()
        if left <= 0:
            raise H.Refusal(reason + '; bounded wait expired')
        repo.deadline.sleep(min(backoff, left))
        backoff = min(10, backoff * 2)


def push_ci(repo, read, sha, branch, wait_s):
    samples = []
    def step():
        samples.append(read())
        state, reason = ci_state(samples[-1], sha, post=True, push_branch=branch)
        return state, f'{branch} CI on {sha}: {reason}', {'sha': sha, 'branch': branch, 'samples': samples}
    return bounded(repo, wait_s, step)


def candidate_chain(repo, candidate, master, heads):
    """[(commit, first parent, PR head)] from master up: one two-parent merge per PR head, in order."""
    chain, tip = [], candidate
    for head in reversed(heads):
        line = bgit(repo, 'rev-list', '--parents', '-n', '1', tip).stdout.split()
        if len(line) != 3 or line[0] != tip or line[2] != head:
            raise H.Refusal(f'candidate commit {tip} is not a two-parent merge of PR head {head}')
        chain.append((tip, line[1], head))
        tip = line[1]
    if tip != master:
        raise H.Refusal(f'candidate first-parent chain does not start at current origin/master {master}')
    return chain[::-1]


def check_trees(repo, chain):
    """Recompute each merge; merge-tree writes its trees to a scratch object directory, not the repo."""
    objects = bgit(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'objects').stdout.strip()
    rows = []
    with scratch('git-merge-gate-objects-') as (directory, _, bound):
        env = {'GIT_OBJECT_DIRECTORY': directory, 'GIT_ALTERNATE_OBJECT_DIRECTORIES': objects}
        for commit, parent, head in chain:
            bound()
            result = bgit(repo, 'merge-tree', '--write-tree', '--no-messages', parent, head, env=env, allowed=(0, 1))
            bound()
            if result.returncode:
                raise H.Refusal(f'PR head {head} conflicts with {parent}')
            expected = result.stdout.strip()
            actual = bgit(repo, 'rev-parse', commit + '^{tree}').stdout.strip()
            if expected != actual:
                raise H.Refusal(f'candidate commit {commit} tree differs from origin/master with the PR heads merged in order')
            rows.append({'commit': commit, 'first_parent': parent, 'pr_head': head, 'tree': actual})
    return rows


def push_master(repo, sha, expected, last_read):
    """Plain push of the candidate SHA to master: never a force push."""
    guarded_push(repo, sha, 'master', expected, last_read)


def guarded_push(repo, sha, branch, expected, last_read):
    """Plain push of sha to branch: the hook refuses unless origin advertises branch at `expected`
    (zeros: absent), and receive-pack then compares that old OID atomically. last_read() is the last
    external read before the push (T304 ruling 4)."""
    original = Path(bgit(repo, 'rev-parse', '--git-path', 'hooks/pre-push', network=True).stdout.strip())
    if not original.is_absolute():
        original = repo.root / original
    original = original.resolve()
    existing = str(original) if original.is_file() and os.access(original, os.X_OK) else None
    ref = 'refs/heads/' + branch
    with scratch('git-land-guard-') as (directory, fd, bound):
        opener = lambda name, flags: os.open(name, flags | os.O_EXCL | os.O_NOFOLLOW, 0o700, dir_fd=fd)
        with open('pre-push', 'w', opener=opener) as hook:
            hook.write('#!/usr/bin/env python3\n'
                'import subprocess,sys\n'
                f'sha={sha!r}; ref={ref!r}; expected={expected!r}; original={existing!r}\n'
                'data=sys.stdin.buffer.read(); rows=data.decode().splitlines()\n'
                'fields=rows[0].split() if len(rows)==1 else []\n'
                'if fields!=[sha,sha,ref,expected]:\n'
                f' print("REFUSE: origin/{branch} moved or unexpected update",file=sys.stderr);sys.exit(1)\n'
                'if original:\n'
                ' result=subprocess.run([original,*sys.argv[1:]],input=data,timeout=30)\n'
                ' sys.exit(result.returncode)\n')
            os.fchmod(hook.fileno(), 0o755)
        last_read()
        bound()
        bgit(repo, '-c', 'core.hooksPath=' + directory, 'push', 'origin', sha + ':' + ref, network=True)
        bound()


def new_batch_report(candidate, numbers, dry_run):
    names = ('request', 'prs', 'branches', 'fingerprint', 'candidate', 'ci', 'stable',
             'push', 'pr_merged', 'master_ci', 'candidate_delete')
    return {'ok': False, 'batch': True, 'mode': 'dry-run' if dry_run else 'apply', 'candidate': candidate,
            'pr_numbers': list(numbers), 'status': 'REFUSED', 'merged': False, 'candidate_sha': None,
            'master_sha': None, 'heads': [], 'merge_sha': None, 'final_ci': None, 'errors': [],
            'checks': {name: {'status': 'NOT-RUN', 'reason': 'prerequisite unavailable'} for name in names}}


def batch_gate(repo, gh, candidate, numbers, dry_run=True, wait_s=480, report=None):
    """PASS only for a candidate that is origin/master plus exactly these PR heads merged in order, with
    exact-SHA CI success. --apply fast-forwards master to it and deletes only the candidate branch."""
    if report is None:
        report = new_batch_report(candidate, numbers, dry_run)
    repo, gh = Protected(repo), copy.copy(gh)
    gh.runner = Protected(gh.runner)
    def check(name, action):
        try:
            report['checks'][name] = {'status': 'PASS', 'evidence': action()}
            return True
        except BaseException as error:
            report['checks'][name] = {'status': 'FAIL', 'reason': record_failure(report, error, name)}
            return False
    def request():
        if (not CANDIDATE.fullmatch(candidate) or not numbers or len(set(numbers)) != len(numbers)
                or any(not isinstance(n, int) or n <= 0 for n in numbers)):
            raise H.Refusal('candidate must be land/<id> ([0-9A-Za-z_-]) and the PRs one or more distinct positive numbers')
        return {'candidate': candidate, 'pr_numbers': list(numbers)}
    prs = []
    def read_prs():
        for number in numbers:
            value = gh.pr(number)
            if (value['number'] != number or value['state'] != 'OPEN' or value['baseRefName'] != 'master'
                    or value['isCrossRepository'] is not False):
                raise H.Refusal(f'PR {number} must exist, be OPEN, be same-repository and target master')
            if value['isDraft'] is not False:
                raise H.Refusal(f'PR {number} is a draft; batch mode never marks a PR ready')
            if not isinstance(value['headRefOid'], str) or not SHA.fullmatch(value['headRefOid']):
                raise H.Refusal(f'PR {number} head SHA missing or malformed')
            prs.append(value)
        report['heads'] = [value['headRefOid'] for value in prs]
        return prs
    def extras():
        inventory = H.hygiene(repo, gh, apply=False)
        if not inventory['ok']:
            raise H.Refusal('hygiene evidence incomplete: ' + '; '.join(inventory['errors']))
        allowed = {'master', candidate} | {value['headRefName'] for value in prs}
        allowed.update(w['branch'] for w in inventory['worktrees'] if w['branch'] and Path(w['path']).is_dir())
        extra = sorted({b['name'] for b in inventory['branches'] if b['name'] not in allowed})
        if extra:
            raise H.Refusal('extra branches remain; run hygiene first and review unmerged extras: ' + ', '.join(extra))
        return inventory
    def branches():
        inventory = extras()
        tips = {b['sha'] for b in inventory['branches'] if b['kind'] == 'remote' and b['name'] == candidate}
        if len(tips) != 1:
            raise H.Refusal(f'candidate branch {candidate} is not on origin')
        report['master_sha'], report['candidate_sha'] = inventory['master_sha'], tips.pop()
        return inventory
    def fingerprint():
        result = repo.run([sys.executable, '-B', 'code/memit/engine_fingerprint.py'])
        engine = bgit(repo, 'show', report['candidate_sha'] + ':' + ENGINE).raw_stdout
        digest = hashlib.sha256(engine).hexdigest()
        if digest != F.EXPECTED_SHA256 or engine.count(b'_cov_cpu') != F.EXPECTED_COV_CPU_SITES:
            raise H.Refusal('committed candidate engine fingerprint failed')
        return {'root': 'PASS', 'output': result.stdout, 'candidate_sha': report['candidate_sha'], 'engine_sha256': digest}
    def structure():
        return check_trees(repo, candidate_chain(repo, report['candidate_sha'], report['master_sha'], report['heads']))
    def candidate_ci():
        return push_ci(repo, lambda: candidate_evidence(gh, report['candidate_sha'], candidate),
                       report['candidate_sha'], candidate, wait_s)
    def stable():
        for number, head in zip(numbers, report['heads']):
            value = gh.pr(number)
            if (value['state'] != 'OPEN' or value['headRefOid'] != head or value['baseRefName'] != 'master'
                    or value['isCrossRepository'] is not False or value['isDraft'] is not False):
                raise H.Refusal(f'PR {number} moved, closed, retargeted or became a draft; no automatic retry')
        tips = remote_tips(repo, 'master', candidate)
        if (tips.get('master') != report['master_sha'] or tips.get(candidate) != report['candidate_sha']
                or gh.master() != report['master_sha']):
            raise H.Refusal('origin/master or the candidate branch moved; no automatic retry')
        return tips
    try:
        for name, action in (('request', request), ('prs', read_prs), ('branches', branches),
                             ('fingerprint', fingerprint), ('candidate', structure), ('ci', candidate_ci),
                             ('stable', stable)):
            if not check(name, action):
                return report
        if dry_run:
            for name in ('push', 'pr_merged', 'master_ci', 'candidate_delete'):
                report['checks'][name] = {'status': 'WOULD-RUN', 'reason': 'dry-run; no action',
                                          'candidate_sha': report['candidate_sha']}
            report['ok'], report['status'] = True, 'DRY_RUN_PASS'
            return report
        sha = report['candidate_sha']
        def landed():
            report['merged'], report['merge_sha'], report['status'] = True, sha, 'MERGED_WITH_FAILURE'
        with repo.lock():
            def push():
                stable()
                extras()
                stable()
                evidence = candidate_evidence(gh, sha, candidate)  # every CI read precedes the last stable()
                state, reason = ci_state(evidence, sha, post=True, push_branch=candidate)
                differences = ci_differences(report['checks']['ci']['evidence']['samples'][-1], evidence)
                report['final_ci'] = {'status': state, 'reason': reason, 'differences': differences, 'evidence': evidence}
                if state != 'PASS':
                    raise H.Refusal('final candidate CI refused: ' + reason)
                if differences:
                    raise H.Refusal('CI evidence changed before push: ' + '; '.join(differences))
                try:
                    push_master(repo, sha, report['master_sha'], stable)
                finally:
                    error = sys.exc_info()[1]  # any exception, then it surfaces (T304 ruling 7)
                    if error is not None:
                        try:
                            if remote_tips(repo, 'master').get('master') == sha:
                                landed()
                        except H.Refusal as unknown:
                            raise H.Refusal(f'{error}; push outcome unverified: {unknown}') from error
                landed()
                if remote_tips(repo, 'master').get('master') != sha:
                    raise H.Refusal('origin/master is not the candidate after the push')
                return {'master_before': report['master_sha'], 'master_after': sha, 'strategy': 'fast-forward push'}
            def pr_merged():
                def step():
                    if gh.master() != sha:
                        return 'WAIT', 'GitHub master ref does not show the candidate yet', None
                    rows = []
                    for number, head in zip(numbers, report['heads']):
                        value = gh.pr(number)
                        if value['headRefOid'] != head:
                            return 'FAIL', f'PR {number} head changed after the push', None
                        if value['state'] != 'MERGED':
                            return 'WAIT', f'PR {number} does not show MERGED yet', None
                        rows.append({'pr': number, 'state': value['state'], 'head_sha': head})
                    return 'PASS', '', rows
                return bounded(repo, wait_s, step)
            def master_ci():
                result = push_ci(repo, lambda: gh.evidence(numbers[0], sha, post=True), sha, 'master', wait_s)
                if gh.master() != sha:
                    raise H.Refusal('master moved during post-merge verification')
                return result
            def containing():
                """Live origin/master when it contains the candidate, else None."""
                tip = remote_tips(repo, 'master').get('master')
                if not tip or bgit(repo, 'merge-base', '--is-ancestor', sha, tip, allowed=(0, 1)).returncode:
                    return None
                return tip
            def delete():
                if not containing():
                    raise H.Refusal('origin/master does not contain the candidate; candidate branch kept')
                H.delete_remote(repo, candidate, sha)
                tip = None
                try:
                    tip = containing()
                finally:
                    if not tip:  # master lost the candidate, or containment is unverified (T304 ruling 8)
                        guarded_push(repo, sha, candidate, '0' * 40, lambda: None)
                if not tip:
                    raise H.Refusal('origin/master no longer contains the candidate after the delete; candidate branch restored')
                return {'deleted': candidate, 'sha': sha, 'master': tip}
            for name, action in (('push', push), ('pr_merged', pr_merged), ('master_ci', master_ci),
                                 ('candidate_delete', delete)):
                if not check(name, action):
                    return report
        report['ok'], report['status'] = True, 'MERGED'
    except BaseException as error:
        record_failure(report, error)
    return report


def batch_main(argv):
    parser = argparse.ArgumentParser(prog='git_merge_gate.py --batch',
                                     description='Judge one land/<id> candidate carrying PRs in order.')
    parser.add_argument('--batch', action='store_true', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('prs', type=int, nargs='+')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=float, default=1200)
    parser.add_argument('--ci-wait', type=float, default=480)
    args = parser.parse_args(argv)
    repo = None
    report = new_batch_report(args.candidate, args.prs, not args.apply)
    try:
        deadline = H.Deadline(args.timeout)
        if not math.isfinite(args.ci_wait) or not 0 < args.ci_wait <= 1200:
            raise H.Refusal('CI wait must be finite and between 0 and 1200 seconds')
        repo = H.Repo(Path(os.environ.get('LLMDB_ROOT') or Path.cwd()), deadline)
        batch_gate(repo, H.Gh(repo, H.repository_name(repo)), args.candidate, args.prs,
                   dry_run=not args.apply, wait_s=args.ci_wait, report=report)
    except BaseException as error:
        record_failure(report, error)
    return deliver(report, repo)


def main():
    if '--batch' in sys.argv[1:]:
        return batch_main(sys.argv[1:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', type=int)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=float, default=1200)
    parser.add_argument('--ci-wait', type=float, default=480)
    args = parser.parse_args()
    repo = None
    report = new_report(args.pr, not args.apply)
    try:
        deadline = H.Deadline(args.timeout)
        if not math.isfinite(args.ci_wait) or not 0 < args.ci_wait <= 1200:
            raise H.Refusal('CI wait must be finite and between 0 and 1200 seconds')
        repo = H.Repo(Path(os.environ.get('LLMDB_ROOT') or Path.cwd()), deadline)
        gate(repo, H.Gh(repo, H.repository_name(repo)), args.pr, dry_run=not args.apply, wait_s=args.ci_wait, report=report)
    except BaseException as error:
        record_failure(report, error)
    return deliver(report, repo)


def deliver(report, repo):
    try:
        report['command_evidence'] = repo.commands if repo else []
        print(json.dumps(report, indent=2, sort_keys=True))
        sys.stdout.flush()
        for name, value in report['checks'].items():
            print(f"{name}: {value['status']} {value.get('reason', '')}", file=sys.stderr)
        sys.stderr.flush()
        outcome = 'PASS: bounded merge gate complete' if report['ok'] else (
            report['status'] + ': merge_sha=' + str(report['merge_sha']) + ' ' if report['merged'] else 'REFUSE: '
        ) + ' '.join(report['errors'][0].split())
        print(outcome, file=sys.stderr)
        sys.stderr.flush()
    except BaseException as error:
        record_failure(report, error, 'report delivery')
        if report['merged']:
            report['status'] = 'MERGED_WITH_FAILURE'
        failure_receipt(report, repo)
        return 1
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
