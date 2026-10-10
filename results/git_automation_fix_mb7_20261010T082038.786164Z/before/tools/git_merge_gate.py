#!/usr/bin/env python3
"""MAESTRO's only merge path. Explicit --apply; default/dry-run never mutates git."""
from __future__ import annotations

import argparse
from contextlib import nullcontext
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

if __package__:
    from . import git_hygiene as H, engine_fingerprint as F
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from tools import git_hygiene as H, engine_fingerprint as F


def ci_state(evidence, sha, post=False):
    if evidence['sha'] != sha:
        return 'FAIL', 'CI evidence is for a different SHA'
    checks, native, statuses, runs = (evidence[k] for k in ('pr_checks', 'check_runs', 'statuses', 'runs'))
    if not runs or not native or (not post and not checks):
        return 'WAIT', 'CI not started: no checks or exact-commit workflow run'
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
        key = (run['workflowName'], run['event'], run['headBranch'])
        if key not in latest or run['databaseId'] > latest[key]['databaseId']:
            latest[key] = run
    for run in latest.values():
        if run['status'] != 'completed':
            return 'WAIT', 'workflow run pending'
        if run['conclusion'] != 'success':
            return 'FAIL', 'workflow run terminal conclusion is not success'
    ci_runs = [r for r in latest.values() if r['workflowName'] == 'CI' and
               (not post or (r['headBranch'] == 'master' and r['event'] == 'push'))]
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
    return 'PASS', 'all exact-SHA checks and latest workflow runs completed successfully'


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


def gate(repo, gh, number, dry_run=True, wait_s=480):
    names = ('pr', 'fingerprint', 'branches', 'ci', 'stable_head_base', 'ready', 'merge', 'master_ci', 'post_hygiene')
    report = {'ok': False, 'mode': 'dry-run' if dry_run else 'apply', 'pr_number': number,
              'head_sha': None, 'base_sha': None, 'merge_sha': None, 'errors': [],
              'checks': {name: {'status': 'NOT-RUN', 'reason': 'prerequisite unavailable'} for name in names}}
    def check(name, action):
        try:
            value = action()
            report['checks'][name] = {'status': 'PASS', 'evidence': value}
            return value
        except (H.Refusal, KeyError, ValueError, TypeError, OSError) as error:
            reason = ' '.join(str(error).split())
            report['checks'][name] = {'status': 'FAIL', 'reason': reason}
            report['errors'].append(name + ': ' + reason)
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
        result = repo.run([sys.executable, '-B', 'tools/engine_fingerprint.py'])
        evidence = {'root': 'PASS', 'output': result.stdout, 'candidate': 'NOT-RUN'}
        if report['head_sha']:
            engine = repo.run(['git', 'show', report['head_sha'] + ':memit_dry_run/memit/memit/memit_main.py']).raw_stdout
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
            if inventory['master_sha'] != pr['baseRefOid'] or not H.ancestor(repo, inventory['master_sha'], pr['headRefOid']):
                raise H.Refusal('PR must include the current origin/master; update branch then obtain fresh CI')
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
        with repo.lock() if not dry_run else nullcontext():
            pr = check('pr', read_pr)
            check('fingerprint', fingerprint)
            check('branches', branch_check)
            if pr:
                check('ci', lambda: poll_ci(repo, gh, number, report['head_sha'], report['base_sha'], wait_s))
                check('stable_head_base', stable)
            if report['errors']:
                return report
            if dry_run:
                for name in ('ready', 'merge', 'master_ci', 'post_hygiene'):
                    report['checks'][name] = {'status': 'WOULD-RUN', 'reason': 'dry-run; no action',
                        'head_sha': report['head_sha'], 'post_merge_sha': 'returned merge commit, verified separately'}
                report['ok'] = True
                return report
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
                gh.merge(number, report['head_sha'])
                merged = gh.pr(number)
                sha = merged['mergeCommit']['oid']
                report['merge_sha'] = sha
                if merged['state'] != 'MERGED' or merged['headRefOid'] != report['head_sha'] or not re.fullmatch('[0-9a-f]{40}', sha):
                    raise H.Refusal('merge returned no valid exact-head merge commit')
                if gh.master() != sha:
                    raise H.Refusal('master tip differs from returned merge commit; post-merge CI not verified')
                return {'head_sha': report['head_sha'], 'merge_sha': sha, 'strategy': 'merge commit'}
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
    except (H.Refusal, OSError) as error:
        report['errors'].append(str(error))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', type=int)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=float, default=1200)
    parser.add_argument('--ci-wait', type=float, default=480)
    args = parser.parse_args()
    repo = None
    try:
        deadline = H.Deadline(args.timeout)
        if not math.isfinite(args.ci_wait) or not 0 < args.ci_wait <= 1200:
            raise H.Refusal('CI wait must be finite and between 0 and 1200 seconds')
        repo = H.Repo(Path(os.environ.get('LLMDB_ROOT') or Path.cwd()), deadline)
        report = gate(repo, H.Gh(repo, H.repository_name(repo)), args.pr, dry_run=not args.apply, wait_s=args.ci_wait)
    except (H.Refusal, ValueError, OSError) as error:
        report = {'ok': False, 'errors': [str(error)], 'checks': {}}
    report['command_evidence'] = repo.commands if repo else []
    print(json.dumps(report, indent=2, sort_keys=True))
    for name, value in report['checks'].items():
        print(f"{name}: {value['status']} {value.get('reason', '')}", file=sys.stderr)
    print('PASS: bounded merge gate complete' if report['ok'] else 'REFUSE: ' + ' '.join(report['errors'][0].split()), file=sys.stderr)
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
