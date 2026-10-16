#!/usr/bin/env python3
"""MAESTRO's only merge path. Explicit --apply; default/dry-run never mutates git."""
from __future__ import annotations

import argparse
from contextlib import nullcontext
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile

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


def ci_state(evidence, sha, post=False):
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
    report = new_report(args.pr, not args.apply)
    try:
        deadline = H.Deadline(args.timeout)
        if not math.isfinite(args.ci_wait) or not 0 < args.ci_wait <= 1200:
            raise H.Refusal('CI wait must be finite and between 0 and 1200 seconds')
        repo = H.Repo(Path(os.environ.get('LLMDB_ROOT') or Path.cwd()), deadline)
        gate(repo, H.Gh(repo, H.repository_name(repo)), args.pr, dry_run=not args.apply, wait_s=args.ci_wait, report=report)
    except BaseException as error:
        record_failure(report, error)
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
