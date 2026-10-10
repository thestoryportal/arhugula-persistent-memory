"""CPU/stdlib tests; every git mutation is confined to disposable fixtures."""
import ast
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout
import importlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock


def load_tools(test):
    for name in ('tools.git_hygiene', 'tools.git_merge_gate'):
        test.assertIsNotNone(importlib.util.find_spec(name), 'missing implementation: ' + name)
    return importlib.import_module('tools.git_hygiene'), importlib.import_module('tools.git_merge_gate')


def evidence_command(command, evidence):
    """Serve the requested command, including the older CLI inventory sequence."""
    if command[1:3] == ['pr', 'checks']:
        return evidence['pr_checks']
    if command[1:3] == ['run', 'list']:
        fields = command[command.index('--json') + 1].split(',')
        return [{field: row[field] for field in fields} for row in evidence['runs']]
    endpoint = command[2]
    if '/actions/runs?' in endpoint:
        fields = {'id': 'databaseId', 'head_sha': 'headSha', 'head_branch': 'headBranch',
                  'event': 'event', 'name': 'workflowName', 'status': 'status',
                  'conclusion': 'conclusion', 'html_url': 'url',
                  'run_attempt': 'run_attempt', 'updated_at': 'updated_at'}
        return {'workflow_runs': [{key: row[field] for key, field in fields.items()}
                                  for row in evidence['runs']]}
    if '/check-runs?filter=latest' in endpoint:
        return {'check_runs': evidence['check_runs']}
    if '/check-runs?filter=all' in endpoint:
        return {'check_runs': evidence['all_check_runs']}
    if '/statuses?' in endpoint:
        return evidence['all_statuses']
    raise AssertionError('unexpected GitHub evidence command: ' + repr(command))


class FailedOutput(io.StringIO):
    def __init__(self, operation):
        super().__init__()
        self.operation = operation

    def write(self, value):
        if self.operation == 'write':
            raise BrokenPipeError('report write failed')
        return super().write(value)

    def flush(self):
        if self.operation == 'flush':
            raise BrokenPipeError('report flush failed')
        return super().flush()


class Clock:
    def __init__(self):
        self.now = 0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class Fixture:
    def __init__(self, directory):
        self.home = Path(directory).resolve()  # macOS TMPDIR sits behind the /var -> /private/var symlink
        self.remote = self.home / 'remote.git'
        self.root = self.home / 'clone'
        self.run(self.home, 'init', '--bare', '--initial-branch=master', str(self.remote))
        self.run(self.home, 'clone', str(self.remote), str(self.root))
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.root / 'base.txt').write_text('base\n')
        source = Path(__file__).resolve().parents[1]
        for relative in ('tools/engine_fingerprint.py', 'memit_dry_run/memit/memit/memit_main.py'):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((source / relative).read_bytes())
        self.git('add', '.')
        self.git('commit', '-m', 'base')
        self.git('push', 'origin', 'master')
        self.base = self.git('rev-parse', 'HEAD').strip()

    @staticmethod
    def run(root, *args):
        result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, timeout=15)
        if result.returncode:
            raise AssertionError(result.stderr)
        return result.stdout

    def git(self, *args):
        return self.run(self.root, *args)

    def branch(self, name, merged=True, remote=True):
        if merged:
            self.git('branch', name, 'master')
        else:
            self.git('checkout', '-b', name)
            (self.root / (name.replace('/', '_') + '.txt')).write_text(name)
            self.git('add', '.')
            self.git('commit', '-m', name)
            self.git('checkout', 'master')
        if remote:
            self.git('push', 'origin', name)
        return self.git('rev-parse', name).strip()

    def worktree(self, name, merged=True):
        self.branch(name, merged)
        target = self.home / ('work tree ' + name.replace('/', '_'))
        self.git('worktree', 'add', str(target), name)
        return target

    def remote_tip(self, name):
        result = subprocess.run(['git', 'ls-remote', '--heads', 'origin', name], cwd=self.root,
                                capture_output=True, text=True, timeout=15, check=True)
        return result.stdout.strip()


class FakeGh:
    def __init__(self, fixture):
        self.fixture = fixture
        self.number = 21
        self.head = fixture.branch('feature', merged=False)
        self.base = fixture.base
        self.moves = None
        self.check_state = 'PASS'
        self.post_state = 'PASS'
        self.extra_heads = set()
        self.calls = []
        self.draft = True
        self.conflict = False
        self.merge_sha = None
        self.run_attempt = 1

    def pr(self, number):
        self.calls.append(('pr', number))
        return {'number': number, 'state': 'MERGED' if self.merge_sha else 'OPEN',
                'headRefName': 'feature', 'headRefOid': self.moves or self.head,
                'baseRefName': 'master', 'baseRefOid': self.base,
                'mergeable': 'CONFLICTING' if self.conflict else 'MERGEABLE',
                'isDraft': self.draft, 'isCrossRepository': False,
                'mergeCommit': {'oid': self.merge_sha} if self.merge_sha else None}

    def open_heads(self):
        return self.extra_heads | (set() if self.merge_sha else {'feature'})

    def evidence(self, number, sha, post=False):
        self.calls.append(('evidence', sha, post))
        state = self.post_state if post else self.check_state
        if state == 'ABSENT':
            return {'sha': sha, 'pr_checks': [], 'check_runs': [], 'statuses': [], 'runs': []}
        status = 'in_progress' if state == 'PENDING' else 'completed'
        conclusion = None if state == 'PENDING' else ('success' if state == 'PASS' else 'failure')
        link = 'https://github.com/o/r/actions/runs/101/job/102'
        return {'sha': sha,
                'pr_checks': [] if post else [{'name': 'cpu', 'state': 'SUCCESS' if state == 'PASS' else 'PENDING',
                                               'bucket': 'pass' if state == 'PASS' else 'pending',
                                               'workflow': 'CI', 'link': link}],
                'check_runs': [{'id': 102, 'updated_at': '2026-10-10T08:00:00Z', 'name': 'cpu', 'head_sha': sha, 'status': status,
                                'conclusion': conclusion, 'html_url': link}],
                'statuses': [],
                'runs': [{'databaseId': 101, 'run_attempt': self.run_attempt, 'updated_at': '2026-10-10T08:00:00Z', 'headSha': sha, 'headBranch': 'master' if post else 'feature',
                          'event': 'push' if post else 'pull_request', 'workflowName': 'CI',
                          'status': status, 'conclusion': conclusion, 'url': link}]}

    def ready(self, number):
        self.calls.append(('ready', number))
        self.draft = False

    def merge(self, number, sha):
        self.calls.append(('merge', number, sha))
        self.fixture.git('merge', '--no-ff', 'feature', '-m', 'fixture merge')
        self.fixture.git('push', 'origin', 'master')
        self.merge_sha = self.fixture.git('rev-parse', 'HEAD').strip()
        return {'merged': True, 'sha': self.merge_sha}

    def master(self):
        return self.merge_sha or self.base

    def first_parent(self, sha):
        self.calls.append(('first_parent', sha))
        return self.fixture.git('rev-parse', sha + '^1').strip()


class AutomationTests(unittest.TestCase):
    def setUp(self):
        self.H, self.M = load_tools(self)
        self.temp = tempfile.TemporaryDirectory(prefix='git-automation-')
        self.addCleanup(self.temp.cleanup)
        self.fixture = Fixture(self.temp.name)
        self.clock = Clock()
        self.repo = self.H.Repo(self.fixture.root, self.H.Deadline(60, clock=self.clock, sleep=self.clock.sleep))
        self.gh = FakeGh(self.fixture)

    def hygiene(self, apply=False, inventory=None):
        with mock.patch.object(self.H, 'cwd_inventory', return_value={} if inventory is None else inventory):
            return self.H.hygiene(self.repo, self.gh, apply=apply)

    def gate(self, dry_run=True, **kwargs):
        with mock.patch.object(self.H, 'cwd_inventory', return_value={}):
            return self.M.gate(self.repo, self.gh, 21, dry_run=dry_run, **kwargs)

    def test_merged_unmerged_and_protected_branches(self):
        self.fixture.branch('merged')
        self.fixture.branch('unmerged', False)
        self.fixture.branch('open-pr')
        self.gh.extra_heads.add('open-pr')
        report = self.hygiene()
        states = {(b['kind'], b['name']): b for b in report['branches']}
        self.assertEqual(states[('local', 'merged')]['classification'], 'MERGED')
        self.assertEqual(states[('remote', 'unmerged')]['classification'], 'UNMERGED')
        self.assertEqual(states[('local', 'open-pr')]['classification'], 'PROTECTED')
        self.assertEqual(states[('local', 'master')]['classification'], 'PROTECTED')
        self.assertEqual(states[('local', 'unmerged')]['unique_commits'], 1)
        self.assertTrue(states[('local', 'unmerged')]['last_commit_date'])
        self.assertTrue(states[('local', 'unmerged')]['exists_remotely'])

    def test_worktree_branch_is_protected_from_direct_branch_deletion(self):
        target = self.fixture.worktree('attached')
        report = self.hygiene(inventory={42: target})
        self.assertTrue(all(b['classification'] == 'PROTECTED' for b in report['branches'] if b['name'] == 'attached'))

    def test_dry_run_does_not_change_refs_config_or_worktrees(self):
        target = self.fixture.worktree('idle')
        before = self.fixture.git('show-ref'), self.fixture.git('config', '--local', '--list')
        report = self.hygiene()
        self.assertEqual(report['actions'], [])
        self.assertEqual(before, (self.fixture.git('show-ref'), self.fixture.git('config', '--local', '--list')))
        self.assertTrue(target.is_dir())
        self.assertTrue(any(w['eligible'] for w in report['worktrees']))

    def test_apply_deletes_only_merged_local_and_remote(self):
        self.fixture.branch('merged')
        self.fixture.branch('keep', False)
        report = self.hygiene(True)
        self.assertTrue(report['ok'], report)
        self.assertEqual(self.fixture.remote_tip('merged'), '')
        self.assertTrue(self.fixture.remote_tip('keep'))
        self.assertNotIn('refs/heads/merged', self.fixture.git('show-ref'))

    def test_clean_idle_worktree_is_manual_candidate_then_second_apply_noop(self):
        target = self.fixture.worktree('idle')
        first = self.hygiene(True)
        self.assertTrue(first['ok'], first)
        self.assertTrue(target.is_dir())
        row = next(w for w in first['worktrees'] if w['path'] == str(target.resolve()))
        self.assertGreater(row['size_before_bytes'], 0)
        self.assertEqual(row['size_after_bytes'], row['size_before_bytes'])
        candidate = next(w for w in first['manual_removal_candidates'] if w['path'] == str(target.resolve()))
        self.assertEqual(candidate['branch'], 'idle')
        self.assertEqual(candidate['head_sha'], self.fixture.base)
        self.assertEqual(candidate['size_before_bytes'], row['size_before_bytes'])
        self.assertEqual(first['actions'], [])
        self.assertTrue(self.fixture.remote_tip('idle'))
        self.assertEqual(self.fixture.git('rev-parse', 'idle').strip(), self.fixture.base)
        self.assertIn(str(target), self.fixture.git('worktree', 'list', '--porcelain'))
        self.assertEqual(self.hygiene(True)['actions'], [])
        self.assert_no_worktree_removal()

    def assert_no_worktree_removal(self):
        commands = [c['command'] for c in self.repo.commands]
        self.assertFalse(any(c[:3] in (['git', 'worktree', 'remove'], ['git', 'worktree', 'prune']) for c in commands), commands)

    def apply_after_last_worktree_inspection(self, target, writer):
        original = self.H.inspect
        events = []
        def inspect(repo, gh):
            result = original(repo, gh)
            row = next((w for w in result['worktrees'] if w['path'] == str(target)), None)
            if row:
                events.append('inspection completed')
                if events == ['inspection completed', 'inspection completed']:
                    self.assertTrue(row['eligible'], row)
                    writer()
                    events.append('session wrote after inspection')
            return result
        with mock.patch.object(self.H, 'inspect', side_effect=inspect):
            report = self.hygiene(True)
        self.assertEqual(events, ['inspection completed', 'inspection completed', 'session wrote after inspection'])
        return report

    def test_ignored_artifact_written_after_last_inspection_survives_apply(self):
        target = self.fixture.worktree('packet-race')
        (self.fixture.root / '.git' / 'info' / 'exclude').write_text('*.packet\n')
        artifact = target / 'precious.packet'
        def writer():
            artifact.write_bytes(b'irreplaceable session artifact\n')
            self.assertEqual(self.fixture.run(target, 'check-ignore', 'precious.packet').strip(), 'precious.packet')
        report = self.apply_after_last_worktree_inspection(target, writer)
        self.assertTrue(target.is_dir(), report)
        self.assertTrue(artifact.is_file(), report)
        self.assertEqual(artifact.read_bytes(), b'irreplaceable session artifact\n')
        self.assertIn(str(target), self.fixture.git('worktree', 'list', '--porcelain'))
        self.assert_no_worktree_removal()

    def test_detached_commit_after_last_inspection_stays_reachable(self):
        target = self.fixture.worktree('detach-race')
        commits = []
        def writer():
            self.fixture.run(target, 'checkout', '--detach')
            self.fixture.run(target, 'commit', '--allow-empty', '-m', 'session commit after inspection')
            commits.append(self.fixture.run(target, 'rev-parse', 'HEAD').strip())
        report = self.apply_after_last_worktree_inspection(target, writer)
        self.assertEqual(len(commits), 1)
        self.assertNotEqual(commits[0], self.fixture.base)
        self.assertTrue(target.is_dir(), report)
        self.assertEqual(self.fixture.run(target, 'rev-parse', 'HEAD').strip(), commits[0])
        self.assertIn(commits[0], self.fixture.git('rev-list', '--all', '--reflog').splitlines())
        self.assertIn(str(target), self.fixture.git('worktree', 'list', '--porcelain'))
        self.assert_no_worktree_removal()

    def test_dirty_worktree_kept(self):
        target = self.fixture.worktree('dirty')
        (target / 'uncommitted.txt').write_text('WIP')
        self.hygiene(True)
        self.assertTrue(target.exists())

    def test_ignored_worktree_files_kept(self):
        target = self.fixture.worktree('ignored')
        (target / '.gitignore').write_text('cache/\n')
        self.fixture.run(target, 'add', '.gitignore')
        self.fixture.run(target, 'commit', '-m', 'ignore')
        self.fixture.git('merge', 'ignored')
        self.fixture.git('push', 'origin', 'master')
        (target / 'cache').mkdir()
        (target / 'cache' / 'precious').write_text('untracked work')
        self.hygiene(True)
        self.assertTrue(target.exists())

    def test_process_cwd_inside_worktree_kept(self):
        target = self.fixture.worktree('busy')
        child = target / 'nested'
        child.mkdir()
        self.hygiene(True, {123: child})
        self.assertTrue(target.exists())

    def test_unknown_process_inventory_keeps_worktrees_and_refuses_apply(self):
        target = self.fixture.worktree('unknown')
        with mock.patch.object(self.H, 'cwd_inventory', side_effect=self.H.Refusal('lsof denied')):
            report = self.H.hygiene(self.repo, self.gh, apply=True)
        self.assertFalse(report['ok'])
        self.assertEqual(report['actions'], [])
        self.assertTrue(target.exists())

    def test_current_worktree_never_removed(self):
        self.assertFalse(next(w for w in self.hygiene()['worktrees'] if w['path'] == str(self.fixture.root))['eligible'])

    def test_locked_worktree_kept(self):
        target = self.fixture.worktree('locked')
        self.fixture.git('worktree', 'lock', str(target))
        self.hygiene(True)
        self.assertTrue(target.exists())

    def test_open_pr_worktree_kept(self):
        target = self.fixture.worktree('open-pr')
        self.gh.extra_heads.add('open-pr')
        self.hygiene(True)
        self.assertTrue(target.exists())

    def test_submodule_work_keeps_worktree(self):
        self.fixture.git('-c', 'protocol.file.allow=always', 'submodule', 'add', str(self.fixture.remote), 'sub')
        self.fixture.git('commit', '-m', 'submodule')
        self.fixture.git('push', 'origin', 'master')
        target = self.fixture.worktree('submodule')
        self.fixture.run(target, '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init')
        (target / 'sub' / 'base.txt').write_text('submodule WIP')
        self.hygiene(True)
        self.assertTrue(target.exists())

    def test_existing_pre_push_hook_veto_is_preserved(self):
        self.fixture.branch('merged')
        hook = self.fixture.root / '.git' / 'hooks' / 'pre-push'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        with self.assertRaises(self.H.Refusal):
            self.H.delete_remote(self.repo, 'merged', self.fixture.base)
        self.assertTrue(self.fixture.remote_tip('merged'))
        self.assertEqual(hook.read_text(), '#!/bin/sh\nexit 1\n')
        self.assertEqual(self.fixture.git('config', '--local', '--list').count('hookspath'), 0)

    def test_branch_advanced_before_advertisement_survives_delete(self):
        self.fixture.branch('merged')
        reviewed = self.fixture.base
        advanced = self.gh.head
        self.fixture.run(self.fixture.remote, 'update-ref', 'refs/heads/merged', advanced)
        with self.assertRaises(self.H.Refusal):
            self.H.delete_remote(self.repo, 'merged', reviewed)
        self.assertIn(advanced, self.fixture.remote_tip('merged'))

    def test_branch_advanced_during_receive_survives_delete(self):
        self.fixture.branch('merged')
        hook = self.fixture.remote / 'hooks' / 'pre-receive'
        hook.write_text('#!/bin/sh\ngit update-ref refs/heads/merged ' + self.gh.head + '\n')
        hook.chmod(0o755)
        with self.assertRaises(self.H.Refusal):
            self.H.delete_remote(self.repo, 'merged', self.fixture.base)
        self.assertIn(self.gh.head, self.fixture.remote_tip('merged'))

    def test_local_branch_advanced_after_review_survives_delete(self):
        self.fixture.branch('merged', remote=False)
        reviewed = self.fixture.base
        self.fixture.git('checkout', 'feature')
        self.fixture.git('update-ref', 'refs/heads/merged', self.gh.head)
        self.assertFalse(self.H.ancestor(self.repo, self.gh.head, reviewed))
        self.assertTrue(callable(getattr(self.H, 'delete_local', None)), 'missing local deletion SHA guard')
        with self.assertRaises(self.H.Refusal):
            self.H.delete_local(self.repo, 'merged', reviewed)
        self.assertEqual(self.fixture.git('rev-parse', 'merged').strip(), self.gh.head)

    def test_existing_reference_transaction_hook_veto_is_preserved(self):
        self.fixture.branch('merged', remote=False)
        hooks = self.fixture.root / 'custom hooks'
        hooks.mkdir()
        self.fixture.git('config', 'core.hooksPath', str(hooks))
        hook = hooks / 'reference-transaction'
        original = '#!/bin/sh\nif [ "$1" = prepared ]; then exit 1; fi\n'
        hook.write_text(original)
        hook.chmod(0o755)
        self.assertTrue(callable(getattr(self.H, 'delete_local', None)), 'missing local deletion SHA guard')
        with self.assertRaises(self.H.Refusal):
            self.H.delete_local(self.repo, 'merged', self.fixture.base)
        self.assertEqual(self.fixture.git('rev-parse', 'merged').strip(), self.fixture.base)
        self.assertEqual(hook.read_text(), original)
        self.assertEqual(self.fixture.git('config', 'core.hooksPath').strip(), str(hooks))

    def test_final_hygiene_verification_failure_retains_completed_actions(self):
        self.fixture.branch('merged')
        original = self.H.inspect
        def inspect(repo, gh):
            result = original(repo, gh)
            if not self.fixture.remote_tip('merged'):
                result['ok'] = False
                result['errors'].append('final open-PR inventory unverified')
            return result
        with mock.patch.object(self.H, 'inspect', side_effect=inspect):
            report = self.hygiene(True)
        self.assertFalse(report['ok'], report)
        self.assertTrue(report['actions'])
        self.assertIn('final open-PR inventory unverified', report['errors'])

    def test_many_branch_deletions_do_not_rescan_worktree_disk_sizes(self):
        for number in range(5):
            self.fixture.branch('merged-' + str(number))
        with mock.patch.object(self.H, 'inspect', wraps=self.H.inspect) as inspect:
            report = self.hygiene(True)
        self.assertTrue(report['ok'], report)
        self.assertEqual(len(report['actions']), 10)
        self.assertLessEqual(inspect.call_count, 3, 'full worktree/disk scan repeated for every branch')

    def test_absent_ci_refuses_with_bounded_backoff(self):
        self.gh.check_state = 'ABSENT'
        report = self.gate(wait_s=3)
        self.assertFalse(report['ok'])
        self.assertIn('not started', str(report))
        self.assertLessEqual(self.clock.now, 3)
        self.assertGreaterEqual(sum(c[0] == 'evidence' for c in self.gh.calls), 2)

    def test_pending_ci_refuses(self):
        self.gh.check_state = 'PENDING'
        self.assertFalse(self.gate(wait_s=2)['ok'])

    def test_failed_ci_refuses(self):
        self.gh.check_state = 'FAIL'
        self.assertFalse(self.gate()['ok'])
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_conflicts_refuse(self):
        self.gh.conflict = True
        self.assertFalse(self.gate()['ok'])

    def test_extra_unmerged_branches_refuse(self):
        self.fixture.branch('abandoned', False)
        report = self.gate()
        self.assertFalse(report['ok'])
        self.assertIn('abandoned', str(report))

    def test_merged_extra_requires_hygiene_first(self):
        self.fixture.branch('old')
        self.assertFalse(self.gate()['ok'])

    def test_dry_gate_has_all_checks_and_no_actions(self):
        before = self.fixture.git('show-ref')
        report = self.gate()
        self.assertTrue(report['ok'], report)
        self.assertTrue(report['head_sha'])
        self.assertIn('master_ci', report['checks'])
        self.assertEqual(self.fixture.git('show-ref'), before)
        self.assertNotIn('ready', [c[0] for c in self.gh.calls])
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_head_moves_after_ci_refuse(self):
        original = self.gh.evidence
        def evidence(*args, **kwargs):
            result = original(*args, **kwargs)
            self.gh.moves = 'f' * 40
            return result
        self.gh.evidence = evidence
        self.assertFalse(self.gate(dry_run=False)['ok'])
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_base_moves_after_ci_refuse(self):
        original = self.gh.evidence
        def evidence(*args, **kwargs):
            result = original(*args, **kwargs)
            self.gh.base = 'e' * 40
            return result
        self.gh.evidence = evidence
        self.assertFalse(self.gate(dry_run=False)['ok'])
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_base_moves_during_last_inventory_refuse_before_merge(self):
        original = self.H.hygiene
        calls = []
        def hygiene(*args, **kwargs):
            result = original(*args, **kwargs)
            calls.append(kwargs.get('apply', False))
            if calls == [False, False]:
                self.gh.base = 'e' * 40
            return result
        with mock.patch.object(self.H, 'hygiene', side_effect=hygiene):
            report = self.gate(dry_run=False)
        self.assertFalse(report['ok'], report)
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def assert_pre_merge_refusal(self, report):
        self.assertFalse(report['ok'], report)
        self.assertIs(report.get('merged'), False, report)
        self.assertIsNone(report['merge_sha'])
        self.assertEqual(report.get('status'), 'REFUSED')
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def assert_merged_failure(self, report, status='MERGED_WITH_FAILURE'):
        self.assertFalse(report['ok'], report)
        self.assertIs(report.get('merged'), True, report)
        self.assertEqual(report['merge_sha'], self.gh.merge_sha)
        self.assertEqual(report.get('status'), status)
        self.assertEqual(sum(c[0] == 'merge' for c in self.gh.calls), 1)

    def test_ci_flips_to_pending_during_ready_refuses_merge(self):
        original = self.gh.ready
        def ready(number):
            original(number)
            self.gh.check_state = 'PENDING'
        self.gh.ready = ready
        report = self.gate(dry_run=False, wait_s=2)
        self.assert_pre_merge_refusal(report)
        self.assertIn('pending', ' '.join(report['errors']))

    def final_inventory_ci_flip(self, state):
        original = self.H.hygiene
        calls = []
        def hygiene(*args, **kwargs):
            result = original(*args, **kwargs)
            calls.append(kwargs.get('apply', False))
            if calls == [False, False]:
                if state == 'OTHER_HEAD':
                    evidence = self.gh.evidence
                    def other_head(*a, **kw):
                        value = evidence(*a, **kw)
                        if not kw.get('post', False):
                            value['check_runs'][0]['head_sha'] = 'a' * 40
                        return value
                    self.gh.evidence = other_head
                else:
                    self.gh.check_state = state
            return result
        with mock.patch.object(self.H, 'hygiene', side_effect=hygiene):
            report = self.gate(dry_run=False, wait_s=2)
        self.assertEqual(calls, [False, False], 'must stop before post-merge cleanup')
        self.assert_pre_merge_refusal(report)
        return report

    def test_ci_flips_to_fail_during_final_hygiene_refuses_merge(self):
        self.assertIn('not success', ' '.join(self.final_inventory_ci_flip('FAIL')['errors']))

    def test_ci_flips_to_pending_during_final_hygiene_refuses_merge(self):
        self.assertIn('pending', ' '.join(self.final_inventory_ci_flip('PENDING')['errors']))

    def test_ci_disappears_during_final_hygiene_refuses_merge(self):
        self.assertIn('no checks', ' '.join(self.final_inventory_ci_flip('ABSENT')['errors']))

    def test_ci_other_head_after_final_hygiene_refuses_merge(self):
        self.assertIn('head SHA differs', ' '.join(self.final_inventory_ci_flip('OTHER_HEAD')['errors']))

    def test_master_advances_after_final_stable_reports_merged_onto_moved_base(self):
        original = self.gh.merge
        advanced = []
        def merge(number, sha):
            self.fixture.git('commit', '--allow-empty', '-m', 'competing master writer')
            self.fixture.git('push', 'origin', 'master')
            advanced.append(self.fixture.git('rev-parse', 'HEAD').strip())
            self.gh.base = advanced[0]
            return original(number, sha)
        self.gh.merge = merge
        report = self.gate(dry_run=False)
        self.assertNotEqual(advanced[0], self.fixture.base)
        self.assertEqual(self.fixture.git('rev-parse', self.gh.merge_sha + '^1').strip(), advanced[0])
        self.assert_merged_failure(report, 'MERGED_ON_MOVED_BASE')
        self.assertEqual(report['base_sha'], self.fixture.base)
        self.assertEqual(report.get('merge_first_parent'), advanced[0])
        self.assertIn('merged onto a moved base', ' '.join(report['errors']))
        self.assertNotIn(('evidence', self.gh.merge_sha, True), self.gh.calls)

    def test_post_merge_failed_ci_reports_merged_with_failure(self):
        self.gh.post_state = 'FAIL'
        self.assert_merged_failure(self.gate(dry_run=False))

    def test_post_merge_timeout_reports_merged_with_failure(self):
        self.gh.post_state = 'PENDING'
        report = self.gate(dry_run=False, wait_s=2)
        self.assert_merged_failure(report)
        self.assertIn('bounded CI wait expired', ' '.join(report['errors']))
        self.assertLessEqual(self.clock.now, 2)

    def test_master_moves_during_post_merge_ci_reports_merged_with_failure(self):
        original = self.gh.evidence
        def evidence(number, sha, post=False):
            result = original(number, sha, post=post)
            if post:
                self.gh.master = lambda: 'd' * 40
            return result
        self.gh.evidence = evidence
        report = self.gate(dry_run=False)
        self.assert_merged_failure(report)
        self.assertIn('master moved', ' '.join(report['errors']))

    def test_parent_read_failure_reports_merged_with_failure(self):
        self.gh.first_parent = mock.Mock(side_effect=self.H.Refusal('commit parent unavailable'))
        report = self.gate(dry_run=False)
        self.assert_merged_failure(report)
        self.assertIn('commit parent unavailable', ' '.join(report['errors']))

    def test_post_merge_hygiene_failure_reports_merged_with_failure(self):
        original = self.H.hygiene
        def hygiene(*args, **kwargs):
            result = original(*args, **kwargs)
            if kwargs.get('apply'):
                result['ok'] = False
                result['errors'].append('post-merge inventory unavailable')
            return result
        with mock.patch.object(self.H, 'hygiene', side_effect=hygiene):
            report = self.gate(dry_run=False)
        self.assert_merged_failure(report)
        self.assertIn('post-merge inventory unavailable', ' '.join(report['errors']))

    def test_cli_post_merge_failure_keeps_merged_status_and_sha(self):
        self.gh.post_state = 'FAIL'
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', ['git_merge_gate.py', '21', '--apply']), \
             mock.patch.object(self.H, 'Repo', return_value=self.repo), \
             mock.patch.object(self.H, 'Gh', return_value=self.gh), \
             mock.patch.object(self.H, 'repository_name', return_value='o/r'), \
             mock.patch.object(self.H, 'cwd_inventory', return_value={}), \
             redirect_stdout(out), redirect_stderr(err):
            result = self.M.main()
        self.assertEqual(result, 1)
        self.assert_merged_failure(json.loads(out.getvalue()))
        self.assertIn('MERGED_WITH_FAILURE', err.getvalue())
        self.assertIn(self.gh.merge_sha, err.getvalue())
        self.assertNotIn('REFUSE:', err.getvalue())

    def test_engine_candidate_mismatch_refuses_when_local_engine_passes(self):
        self.fixture.git('checkout', 'feature')
        engine = self.fixture.root / 'memit_dry_run/memit/memit/memit_main.py'
        original = engine.read_bytes()
        engine.write_bytes(original + b'\n# changed candidate\n')
        self.fixture.git('add', str(engine))
        self.fixture.git('commit', '-m', 'changed engine')
        self.gh.head = self.fixture.git('rev-parse', 'HEAD').strip()
        self.fixture.git('checkout', 'master')
        self.fixture.git('push', 'origin', 'feature')
        self.assertEqual(engine.read_bytes(), original)
        self.assertFalse(self.gate()['ok'])

    def run_cli(self):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', ['git_merge_gate.py', '21', '--apply']), \
             mock.patch.object(self.H, 'Repo', return_value=self.repo), \
             mock.patch.object(self.H, 'Gh', return_value=self.gh), \
             mock.patch.object(self.H, 'repository_name', return_value='o/r'), \
             mock.patch.object(self.H, 'cwd_inventory', return_value={}), \
             redirect_stdout(out), redirect_stderr(err):
            result = self.M.main()
        return result, json.loads(out.getvalue()), err.getvalue()

    def lock_exit_failure(self, error):
        original = self.repo.lock
        @contextmanager
        def lock():
            with original():
                yield
            raise error
        with mock.patch.object(self.repo, 'lock', side_effect=lock):
            code, report, stderr = self.run_cli()
        self.assertEqual(code, 1, report)
        self.assert_merged_failure(report)
        self.assertEqual(report['checks']['post_hygiene']['status'], 'PASS')
        self.assertIn(str(error), ' '.join(report['errors']))
        self.assertNotIn('PASS: bounded merge gate complete', stderr)
        self.assertIn(self.gh.merge_sha, stderr)

    def test_lock_exit_oserror_cannot_finalize_success(self):
        self.lock_exit_failure(OSError('lock close failed'))

    def test_lock_exit_valueerror_preserves_merged_report_in_main(self):
        self.lock_exit_failure(ValueError('lock exit invalid'))

    def test_first_post_merge_pr_failure_keeps_response_sha(self):
        original = self.gh.pr
        def pr(number):
            if self.gh.merge_sha:
                raise self.H.Refusal('post-merge PR unavailable')
            return original(number)
        self.gh.pr = pr
        code, report, _ = self.run_cli()
        self.assertEqual(code, 1)
        self.assert_merged_failure(report)
        self.assertIn('post-merge PR unavailable', ' '.join(report['errors']))

    def interrupted_post_merge_pr(self, error):
        original = self.gh.pr
        def pr(number):
            if self.gh.merge_sha:
                raise error
            return original(number)
        self.gh.pr = pr
        try:
            code, report, stderr = self.run_cli()
        except BaseException as escaped:
            self.fail('merged receipt escaped main: ' + type(escaped).__name__)
        self.assertEqual(code, 1)
        self.assert_merged_failure(report)
        self.assertIn(self.gh.merge_sha, stderr)
        self.assertNotIn('PASS: bounded merge gate complete', stderr)

    def test_post_merge_pr_keyboardinterrupt_preserves_receipt(self):
        self.interrupted_post_merge_pr(KeyboardInterrupt())

    def test_post_merge_pr_systemexit_zero_preserves_receipt(self):
        self.interrupted_post_merge_pr(SystemExit(0))

    def interrupted_lock_exit(self, error):
        try:
            self.lock_exit_failure(error)
        except (KeyboardInterrupt, SystemExit) as escaped:
            self.fail('merged receipt escaped lock exit: ' + type(escaped).__name__)

    def test_lock_exit_systemexit_zero_preserves_receipt(self):
        self.interrupted_lock_exit(SystemExit(0))

    def test_lock_exit_keyboardinterrupt_preserves_receipt(self):
        self.interrupted_lock_exit(KeyboardInterrupt('lock interrupted'))

    def test_main_post_gate_systemexit_zero_preserves_receipt(self):
        original = self.M.gate
        def gate(*args, **kwargs):
            original(*args, **kwargs)
            raise SystemExit(0)
        with mock.patch.object(self.M, 'gate', side_effect=gate):
            try:
                code, report, stderr = self.run_cli()
            except SystemExit as escaped:
                self.fail('merged receipt escaped main boundary: ' + str(escaped))
        self.assertEqual(code, 1)
        self.assert_merged_failure(report)
        self.assertIn(self.gh.merge_sha, stderr)

    def failed_report_output(self, out=None, err=None, serialization=False):
        out = io.StringIO() if out is None else out
        err = io.StringIO() if err is None else err
        report = self.M.new_report(21, False)
        dumps = mock.patch.object(self.M.json, 'dumps', side_effect=TypeError('report serialization failed'))
        with mock.patch.object(sys, 'argv', ['git_merge_gate.py', '21', '--apply']), \
             mock.patch.object(self.H, 'Repo', return_value=self.repo), \
             mock.patch.object(self.H, 'Gh', return_value=self.gh), \
             mock.patch.object(self.H, 'repository_name', return_value='o/r'), \
             mock.patch.object(self.H, 'cwd_inventory', return_value={}), \
             mock.patch.object(self.M, 'new_report', return_value=report), \
             dumps if serialization else nullcontext(), \
             redirect_stdout(out), redirect_stderr(err):
            try:
                code = self.M.main()
            except BaseException as escaped:
                self.fail('report delivery escaped main: ' + type(escaped).__name__ +
                          '; merged=' + str(report['merged']) + '; ok=' + str(report['ok']))
        self.assertEqual(code, 1)
        self.assert_merged_failure(report)
        self.assertNotIn('PASS: bounded merge gate complete', err.getvalue())
        return report, err.getvalue()

    def test_report_serialization_typeerror_uses_failure_receipt(self):
        _, stderr = self.failed_report_output(serialization=True)
        self.assertIn('MERGED_WITH_FAILURE', stderr)
        self.assertIn(self.gh.merge_sha, stderr)
        self.assertIn('ok=false', stderr)

    def test_report_stdout_brokenpipe_uses_failure_receipt(self):
        _, stderr = self.failed_report_output(out=FailedOutput('write'))
        self.assertIn('MERGED_WITH_FAILURE', stderr)
        self.assertIn(self.gh.merge_sha, stderr)
        self.assertIn('ok=false', stderr)

    def test_report_stdout_flush_failure_uses_failure_receipt(self):
        _, stderr = self.failed_report_output(out=FailedOutput('flush'))
        self.assertIn('MERGED_WITH_FAILURE', stderr)
        self.assertIn(self.gh.merge_sha, stderr)

    def test_report_stderr_write_failure_uses_receipt_file(self):
        self.failed_report_output(err=FailedOutput('write'))
        receipts = list((self.fixture.root / 'results/git_merge_gate_receipts').glob('*.txt'))
        self.assertEqual(len(receipts), 1)
        text = receipts[0].read_text()
        self.assertIn('MERGED_WITH_FAILURE', text)
        self.assertIn(self.gh.merge_sha, text)
        self.assertIn('ok=false', text)

    def test_report_stderr_flush_failure_uses_receipt_file(self):
        self.failed_report_output(err=FailedOutput('flush'))
        receipts = list((self.fixture.root / 'results/git_merge_gate_receipts').glob('*.txt'))
        self.assertEqual(len(receipts), 1)
        self.assertIn(self.gh.merge_sha, receipts[0].read_text())

    def test_report_both_streams_broken_uses_receipt_file(self):
        self.failed_report_output(out=FailedOutput('write'), err=FailedOutput('write'))
        receipts = list((self.fixture.root / 'results/git_merge_gate_receipts').glob('*.txt'))
        self.assertEqual(len(receipts), 1)
        self.assertIn('MERGED_WITH_FAILURE', receipts[0].read_text())
        self.assertIn(self.gh.merge_sha, receipts[0].read_text())

    def test_cli_flushes_report_before_success_message(self):
        events = []
        class Output(io.StringIO):
            def __init__(self, name):
                super().__init__()
                self.name = name
            def write(self, value):
                if 'PASS: bounded merge gate complete' in value:
                    events.append('success')
                return super().write(value)
            def flush(self):
                events.append(self.name + ' flush')
                return super().flush()
        out, err = Output('stdout'), Output('stderr')
        with mock.patch.object(sys, 'argv', ['git_merge_gate.py', '21', '--apply']), \
             mock.patch.object(self.H, 'Repo', return_value=self.repo), \
             mock.patch.object(self.H, 'Gh', return_value=self.gh), \
             mock.patch.object(self.H, 'repository_name', return_value='o/r'), \
             mock.patch.object(self.H, 'cwd_inventory', return_value={}), \
             redirect_stdout(out), redirect_stderr(err):
            code = self.M.main()
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out.getvalue())['ok'])
        self.assertIn('stdout flush', events, 'report was not fully delivered')
        self.assertIn('stderr flush', events, 'check summary was not fully delivered')
        self.assertLess(events.index('stdout flush'), events.index('success'))
        self.assertLess(events.index('stderr flush'), events.index('success'))

    def test_candidate_ci_drains_before_lock_is_acquired(self):
        self.gh.check_state = 'PENDING'
        original_lock, original_sleep = self.repo.lock, self.clock.sleep
        states_at_lock = []
        @contextmanager
        def lock():
            states_at_lock.append(self.gh.check_state)
            with original_lock():
                yield
        def sleep(seconds):
            original_sleep(seconds)
            self.gh.check_state = 'PASS'
        self.clock.sleep = sleep
        self.repo.deadline.sleep = sleep
        with mock.patch.object(self.repo, 'lock', side_effect=lock):
            report = self.gate(dry_run=False, wait_s=2)
        self.assertTrue(report['ok'], report)
        self.assertEqual(states_at_lock, ['PASS'], 'candidate CI must drain before the freeze')
        self.assertEqual(len(report['checks']['ci']['evidence']['samples']), 2)

    def test_older_check_writer_drains_before_lock_is_acquired(self):
        original_lock, original_evidence, original_sleep = self.repo.lock, self.gh.evidence, self.clock.sleep
        drained, states_at_lock = [], []
        def evidence(*args, **kwargs):
            value = original_evidence(*args, **kwargs)
            if not kwargs.get('post'):
                old = dict(value['check_runs'][0], id=99,
                           status='completed' if drained else 'in_progress',
                           conclusion='success' if drained else None)
                value['all_check_runs'] = value['check_runs'] + [old]
            return value
        @contextmanager
        def lock():
            states_at_lock.append(bool(drained))
            with original_lock():
                yield
        def sleep(seconds):
            original_sleep(seconds)
            drained.append(True)
        self.gh.evidence = evidence
        self.repo.deadline.sleep = sleep
        with mock.patch.object(self.repo, 'lock', side_effect=lock):
            report = self.gate(dry_run=False, wait_s=2)
        self.assertTrue(report['ok'], report)
        self.assertEqual(states_at_lock, [True], 'older check writer must drain before the freeze')
        self.assertEqual(len(report['checks']['ci']['evidence']['samples']), 2)

    def test_older_in_progress_run_in_final_read_only_refuses_merge(self):
        original, reads = self.gh.evidence, []
        def evidence(*args, **kwargs):
            value = original(*args, **kwargs)
            if not kwargs.get('post'):
                reads.append(value)
                if len(reads) == 2:
                    value['runs'].append(dict(value['runs'][0], databaseId=100,
                                             status='in_progress', conclusion=None))
            return value
        self.gh.evidence = evidence
        report = self.gate(dry_run=False, wait_s=2)
        self.assertEqual(report['checks']['ci']['status'], 'PASS')
        self.assertEqual(len(reads), 2)
        self.assertEqual(len(reads[0]['runs']), 1)
        self.assert_pre_merge_refusal(report)
        self.assertIn('workflow run 100 pending', ' '.join(report['errors']))

    def gate_with_rest_adapters(self):
        original_run, snapshot = self.repo.run, {}
        commands = []
        def run(command, **kwargs):
            if command[0] != 'gh':
                return original_run(command, **kwargs)
            commands.append(command)
            if command[1:3] == ['pr', 'view']:
                payload = self.gh.pr(int(command[3]))
            elif command[1:3] == ['pr', 'ready']:
                self.gh.ready(int(command[3]))
                payload = None
            elif command[1:3] == ['pr', 'merge']:
                self.assertIn('--merge', command)
                self.assertEqual(command[command.index('--match-head-commit') + 1], self.gh.head)
                payload = self.gh.merge(21, self.gh.head)
            elif command[1:4] == ['api', '-X', 'PUT']:
                self.assertIn('sha=' + self.gh.head, command)
                payload = self.gh.merge(21, self.gh.head)
            elif command[1] == 'api' and '/pulls?state=open' in command[2]:
                payload = [{'head': {'ref': name}} for name in self.gh.open_heads()]
            elif command[1] == 'api' and '/git/ref/heads/master' in command[2]:
                payload = {'object': {'sha': self.gh.master()}}
            elif command[1] == 'api' and '/git/commits/' in command[2]:
                sha = command[2].rsplit('/', 1)[1]
                payload = {'sha': sha, 'parents': [{'sha': self.gh.first_parent(sha)}]}
            else:
                if command[1:3] == ['pr', 'checks']:
                    snapshot['value'] = self.gh.evidence(21, self.gh.head)
                elif (command[1:3] == ['run', 'list'] and '--branch' in command) or (
                        '/actions/runs?' in command[2] and '&branch=master' in command[2]):
                    snapshot['value'] = self.gh.evidence(21, self.gh.merge_sha, post=True)
                value = snapshot['value']
                value['all_check_runs'] = value['check_runs']
                value['all_statuses'] = value['statuses']
                payload = evidence_command(command, value)
            return subprocess.CompletedProcess(command, 0, json.dumps(payload), '')
        with mock.patch.object(self.repo, 'run', side_effect=run), \
             mock.patch.object(self.H, 'cwd_inventory', return_value={}):
            report = self.M.gate(self.repo, self.H.Gh(self.repo, 'o/r'), 21, dry_run=False)
        return report, commands

    def test_rest_adapters_through_gate_keep_merge_receipt_and_head_guard(self):
        report, commands = self.gate_with_rest_adapters()
        self.assertTrue(report['ok'], report)
        self.assertEqual(report['merge_sha'], self.gh.merge_sha)
        self.assertEqual(sum(c[1:4] == ['api', '-X', 'PUT'] for c in commands), 1)
        self.assertTrue(any('/check-runs?filter=all' in c[2] for c in commands if c[1] == 'api'))
        self.assertIn(('evidence', self.gh.merge_sha, True), self.gh.calls)

    def test_rest_adapter_higher_attempt_in_final_read_refuses_through_gate(self):
        original, calls = self.H.hygiene, []
        def hygiene(*args, **kwargs):
            value = original(*args, **kwargs)
            calls.append(kwargs.get('apply', False))
            if calls == [False, False]:
                self.gh.run_attempt = 2
            return value
        with mock.patch.object(self.H, 'hygiene', side_effect=hygiene):
            report, _ = self.gate_with_rest_adapters()
        self.assertEqual(report['checks']['ci']['status'], 'PASS')
        self.assert_pre_merge_refusal(report)
        self.assertIn('run_attempt', ' '.join(report['errors']))

    def test_final_read_refuses_older_in_progress_run_on_same_head(self):
        original = self.gh.evidence
        def evidence(*args, **kwargs):
            result = original(*args, **kwargs)
            if not kwargs.get('post'):
                old = dict(result['runs'][0], databaseId=100, status='in_progress', conclusion=None)
                result['runs'].append(old)
            return result
        self.gh.evidence = evidence
        report = self.gate(dry_run=False, wait_s=2)
        self.assert_pre_merge_refusal(report)
        self.assertIn('100', ' '.join(report['errors']))

    def test_higher_run_attempt_after_initial_ci_refuses_before_merge(self):
        original = self.H.hygiene
        calls = []
        def hygiene(*args, **kwargs):
            result = original(*args, **kwargs)
            calls.append(kwargs.get('apply', False))
            if calls == [False, False]:
                self.gh.run_attempt = 2
            return result
        with mock.patch.object(self.H, 'hygiene', side_effect=hygiene):
            report = self.gate(dry_run=False)
        self.assert_pre_merge_refusal(report)
        self.assertIn('run_attempt', ' '.join(report['errors']))

    def test_same_sha_rerun_between_final_read_and_merge_is_named(self):
        original = self.gh.merge
        def merge(number, sha):
            self.gh.run_attempt = 2
            self.gh.check_state = 'PENDING'
            return original(number, sha)
        self.gh.merge = merge
        report = self.gate(dry_run=False)
        self.assert_merged_failure(report)
        self.assertIn('workflow run 101', ' '.join(report['errors']))
        self.assertIn('run_attempt', ' '.join(report['errors']))
        self.assertIn('does not undo', ' '.join(report['errors']))

    def head_evidence_change_after_merge(self, change, expected):
        original = self.gh.evidence
        def evidence(*args, **kwargs):
            result = original(*args, **kwargs)
            if self.gh.merge_sha and not kwargs.get('post', False):
                change(result)
            return result
        self.gh.evidence = evidence
        report = self.gate(dry_run=False)
        self.assert_merged_failure(report)
        self.assertIn(expected, ' '.join(report['errors']))

    def test_new_head_check_after_merge_is_named(self):
        def change(e):
            e['check_runs'].append(dict(e['check_runs'][0], id=303, name='external-check'))
        self.head_evidence_change_after_merge(change, 'external-check')

    def test_new_head_status_after_merge_is_named(self):
        def change(e):
            e['statuses'].append({'id': 201, 'context': 'legacy-ci', 'state': 'success',
                'updated_at': '2026-10-10T08:01:00Z', 'url': 'https://api.github.com/repos/o/r/statuses/' + e['sha']})
        self.head_evidence_change_after_merge(change, 'legacy-ci')

    def test_changed_head_updated_at_after_merge_is_named(self):
        self.head_evidence_change_after_merge(lambda e: e['runs'][0].update(updated_at='2026-10-10T08:01:00Z'), 'updated_at')

    def test_changed_head_conclusion_after_merge_is_named(self):
        self.head_evidence_change_after_merge(lambda e: e['check_runs'][0].update(conclusion='failure'), 'conclusion')

    def test_merge_is_server_side_sha_guarded_and_post_ci_separate(self):
        (self.fixture.root / 'unrelated-wip.txt').write_text('WIP')
        report = self.gate(dry_run=False)
        self.assertTrue(report['ok'], report)
        self.assertEqual(report['merge_sha'], self.gh.merge_sha)
        self.assertIn(('merge', 21, self.gh.head), self.gh.calls)
        self.assertIn(('evidence', self.gh.merge_sha, True), self.gh.calls)
        self.assertTrue((self.fixture.root / 'unrelated-wip.txt').exists())

    def test_master_red_refuses_after_merge_and_does_not_retry(self):
        self.gh.post_state = 'FAIL'
        report = self.gate(dry_run=False)
        self.assertFalse(report['ok'])
        self.assertTrue(report['merge_sha'])
        self.assertEqual(sum(c[0] == 'merge' for c in self.gh.calls), 1)

    def test_wrong_pr_target_refuses(self):
        original = self.gh.pr
        self.gh.pr = lambda n: dict(original(n), baseRefName='other')
        self.assertFalse(self.gate()['ok'])

    def test_closed_pr_refuses(self):
        original = self.gh.pr
        self.gh.pr = lambda n: dict(original(n), state='CLOSED')
        self.assertFalse(self.gate()['ok'])

    def test_pr_behind_current_master_refuses(self):
        (self.fixture.root / 'new-master.txt').write_text('new base')
        self.fixture.git('add', '.')
        self.fixture.git('commit', '-m', 'advance master')
        self.fixture.git('push', 'origin', 'master')
        self.gh.base = self.fixture.git('rev-parse', 'HEAD').strip()
        self.assertFalse(self.gate()['ok'])

    def test_wrong_post_merge_master_sha_refuses(self):
        self.gh.master = lambda: 'd' * 40 if self.gh.merge_sha else self.gh.base
        report = self.gate(dry_run=False)
        self.assertFalse(report['ok'])
        self.assertTrue(report['merge_sha'])

    def test_network_failure_still_reports_every_dry_check(self):
        self.gh.pr = mock.Mock(side_effect=self.H.Refusal('network unavailable'))
        report = self.gate()
        self.assertFalse(report['ok'])
        self.assertEqual(set(report['checks']), {'pr', 'fingerprint', 'branches', 'ci', 'stable_head_base', 'ready', 'merge', 'master_ci', 'post_hygiene'})

    def test_unknown_remote_keeps_cached_candidates_unadmitted(self):
        self.fixture.branch('merged')
        original = self.repo.git
        def git(*args, **kwargs):
            if args[0] == 'ls-remote':
                raise self.H.Refusal('remote unavailable')
            return original(*args, **kwargs)
        with mock.patch.object(self.repo, 'git', side_effect=git):
            report = self.hygiene(True)
        self.assertFalse(report['ok'])
        self.assertFalse(report['remote_verified'])
        self.assertFalse(any(b['eligible'] for b in report['branches']))
        self.assertEqual(report['actions'], [])
        self.assertTrue(self.fixture.remote_tip('merged'))


class Contracts(unittest.TestCase):
    def setUp(self):
        self.H, self.M = load_tools(self)

    def test_ci_requires_exact_sha_workflow_success_and_terminal_state(self):
        sha = 'a' * 40
        evidence = {'sha': sha, 'pr_checks': [{'name': 'cpu', 'state': 'SUCCESS', 'bucket': 'pass',
                     'workflow': 'CI', 'link': 'https://github.com/o/r/actions/runs/101/job/102'}],
                    'check_runs': [{'name': 'cpu', 'head_sha': sha, 'status': 'completed', 'conclusion': 'success',
                                    'html_url': 'https://github.com/o/r/actions/runs/101/job/102'}],
                    'statuses': [], 'runs': [{'databaseId': 101, 'headSha': sha, 'headBranch': 'feature',
                     'event': 'pull_request', 'workflowName': 'CI', 'status': 'completed', 'conclusion': 'success'}]}
        self.assertEqual(self.M.ci_state(evidence, sha)[0], 'PASS')
        for key, field, value in (('runs', 'headSha', 'b' * 40), ('runs', 'workflowName', 'Other'),
                                  ('check_runs', 'status', 'in_progress'), ('check_runs', 'conclusion', 'skipped'),
                                  ('runs', 'conclusion', 'neutral'), ('pr_checks', 'state', 'PENDING')):
            changed = json.loads(json.dumps(evidence))
            changed[key][0][field] = value
            self.assertNotEqual(self.M.ci_state(changed, sha)[0], 'PASS', (key, field, value))

    def test_commit_parent_adapter_reads_exact_commit(self):
        sha, base = 'a' * 40, 'b' * 40
        runner = mock.Mock()
        runner.run.return_value = subprocess.CompletedProcess([], 0,
            json.dumps({'sha': sha, 'parents': [{'sha': base}, {'sha': 'c' * 40}]}), '')
        gh = self.H.Gh(runner, 'o/r')
        self.assertTrue(callable(getattr(gh, 'first_parent', None)), 'missing exact-commit parent reader')
        self.assertEqual(gh.first_parent(sha), base)
        self.assertEqual(runner.run.call_args.args[0], ['gh', 'api', 'repos/o/r/git/commits/' + sha])

    def test_rest_merge_adapter_returns_validated_response_sha(self):
        runner = mock.Mock()
        runner.run.return_value = subprocess.CompletedProcess([], 0, json.dumps({'merged': True, 'sha': 'b' * 40}), '')
        result = self.H.Gh(runner, 'o/r').merge(21, 'a' * 40)
        self.assertEqual(result, {'merged': True, 'sha': 'b' * 40})
        self.assertEqual(runner.run.call_args.args[0], ['gh', 'api', '-X', 'PUT', 'repos/o/r/pulls/21/merge',
            '-f', 'merge_method=merge', '-f', 'sha=' + 'a' * 40])

    def test_rest_merge_adapter_refuses_bad_response_shape(self):
        runner = mock.Mock()
        for payload in ({'merged': False, 'sha': 'b' * 40}, {'merged': 'true', 'sha': 'b' * 40},
                        {'merged': True, 'sha': 'bad'}, {'merged': True}, [], None):
            with self.subTest(payload=payload):
                runner.run.return_value = subprocess.CompletedProcess([], 0, json.dumps(payload), '')
                with self.assertRaises(self.H.Refusal):
                    self.H.Gh(runner, 'o/r').merge(21, 'a' * 40)

    def test_evidence_adapter_preserves_attempt_dates_and_complete_inventories(self):
        sha = 'a' * 40
        run = {'id': 101, 'head_sha': sha, 'head_branch': 'feature', 'event': 'pull_request', 'name': 'CI',
               'status': 'completed', 'conclusion': 'success', 'html_url': 'https://github.com/o/r/actions/runs/101',
               'run_attempt': 2, 'updated_at': '2026-10-10T08:01:00Z'}
        runner = mock.Mock()
        fields = {'databaseId': 'id', 'headSha': 'head_sha', 'headBranch': 'head_branch',
                  'event': 'event', 'workflowName': 'name', 'status': 'status',
                  'conclusion': 'conclusion', 'url': 'html_url',
                  'run_attempt': 'run_attempt', 'updated_at': 'updated_at'}
        supplied = {'pr_checks': [], 'runs': [{key: run[field] for key, field in fields.items()}],
                    'check_runs': [{'id': 102}], 'all_check_runs': [{'id': 102}, {'id': 103}],
                    'all_statuses': [{'id': 201, 'context': 'ci'}, {'id': 200, 'context': 'ci'}]}
        runner.run.side_effect = lambda command, **kwargs: subprocess.CompletedProcess(
            command, 0, json.dumps(evidence_command(command, supplied)), '')
        evidence = self.H.Gh(runner, 'o/r').evidence(21, sha)
        with self.subTest(assertion='run attempt'):
            self.assertIn('run_attempt', evidence['runs'][0], 'workflow attempt missing')
            self.assertEqual(evidence['runs'][0]['run_attempt'], 2)
        with self.subTest(assertion='run update date'):
            self.assertIn('updated_at', evidence['runs'][0], 'workflow update date missing')
            self.assertEqual(evidence['runs'][0]['updated_at'], run['updated_at'])
        with self.subTest(assertion='complete check inventory'):
            self.assertIn('all_check_runs', evidence, 'complete check inventory missing')
            self.assertEqual([r['id'] for r in evidence['all_check_runs']], [102, 103])
        with self.subTest(assertion='complete status inventory'):
            self.assertIn('all_statuses', evidence, 'complete status inventory missing')
            self.assertEqual([r['id'] for r in evidence['all_statuses']], [201, 200])

    def test_commit_parent_adapter_refuses_wrong_or_missing_evidence(self):
        sha = 'a' * 40
        runner = mock.Mock()
        gh = self.H.Gh(runner, 'o/r')
        self.assertTrue(callable(getattr(gh, 'first_parent', None)), 'missing exact-commit parent reader')
        for payload in ({'sha': 'b' * 40, 'parents': [{'sha': 'c' * 40}]},
                        {'sha': sha, 'parents': []}, {'sha': sha, 'parents': None},
                        {'sha': sha, 'parents': [{}]}, {'sha': sha, 'parents': [{'sha': 'short'}]}):
            with self.subTest(payload=payload):
                runner.run.return_value = subprocess.CompletedProcess([], 0, json.dumps(payload), '')
                with self.assertRaises(self.H.Refusal):
                    gh.first_parent(sha)

    def legacy_status_evidence(self):
        sha = 'a' * 40
        return {'sha': sha, 'pr_checks': [
            {'name': 'cpu', 'state': 'SUCCESS', 'bucket': 'pass', 'workflow': 'CI',
             'link': 'https://github.com/o/r/actions/runs/101/job/102'},
            {'name': 'legacy-ci', 'state': 'SUCCESS', 'bucket': 'pass', 'workflow': '',
             'link': 'https://ci.example.invalid/101'}],
            'check_runs': [{'name': 'cpu', 'head_sha': sha, 'status': 'completed', 'conclusion': 'success',
                            'html_url': 'https://github.com/o/r/actions/runs/101/job/102'}],
            'statuses': [{'url': 'https://api.github.com/repos/o/r/statuses/' + sha,
                          'state': 'success', 'context': 'legacy-ci', 'id': 1}],
            'runs': [{'databaseId': 101, 'headSha': sha, 'headBranch': 'feature',
                      'event': 'pull_request', 'workflowName': 'CI', 'status': 'completed', 'conclusion': 'success'}]}

    def test_normal_legacy_status_response_without_sha_is_accepted(self):
        evidence = self.legacy_status_evidence()
        self.assertNotIn('sha', evidence['statuses'][0])
        self.assertEqual(self.M.ci_state(evidence, evidence['sha'])[0], 'PASS')

    def test_legacy_status_url_for_other_sha_refuses(self):
        evidence = self.legacy_status_evidence()
        evidence['statuses'][0]['url'] = 'https://api.github.com/repos/o/r/statuses/' + 'b' * 40
        self.assertEqual(self.M.ci_state(evidence, evidence['sha'])[0], 'FAIL')

    def test_native_cpu_from_other_workflow_run_refuses_pr_and_master_ci(self):
        for post in (False, True):
            with self.subTest(post=post):
                evidence = self.legacy_status_evidence()
                if post:
                    evidence['pr_checks'] = []
                    evidence['runs'][0].update(headBranch='master', event='push')
                self.assertEqual(self.M.ci_state(evidence, evidence['sha'], post=post)[0], 'PASS')
                evidence['check_runs'][0]['html_url'] = 'https://github.com/o/r/actions/runs/999/job/102'
                self.assertEqual(self.M.ci_state(evidence, evidence['sha'], post=post)[0], 'FAIL')

    def test_read_only_command_disables_optional_index_locks(self):
        repo = self.H.Repo(Path.cwd(), self.H.Deadline(10))
        result = repo.run([sys.executable, '-B', '-c', 'import os; print(os.environ["GIT_OPTIONAL_LOCKS"])'],
                          env={'GIT_OPTIONAL_LOCKS': '1'})
        self.assertEqual(result.stdout.strip(), '0')

    def test_invalid_cli_deadlines_and_ci_wait_refuse_as_json_without_dispatch(self):
        root = Path(__file__).resolve().parents[1]
        commands = []
        for tool in ('git_hygiene.py', 'git_merge_gate.py'):
            for value in ('0', '-1', 'nan', 'inf', '1201'):
                commands.append(([tool] + (['21'] if tool == 'git_merge_gate.py' else []) + ['--timeout', value], 'deadline'))
        for value in ('0', '-1', 'nan', 'inf', '1201'):
            commands.append((['git_merge_gate.py', '21', '--ci-wait', value], 'CI wait'))
        with tempfile.TemporaryDirectory(prefix='git-invalid-cli-') as directory:
            for arguments, reason in commands:
                with self.subTest(arguments=arguments):
                    result = subprocess.run([sys.executable, '-B', str(root / 'tools' / arguments[0]), *arguments[1:]],
                        cwd=directory, env=dict(os.environ, LLMDB_ROOT=directory), capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn('Traceback', result.stderr)
                    report = json.loads(result.stdout)
                    self.assertFalse(report['ok'])
                    self.assertEqual(report['command_evidence'], [])
                    self.assertIn(reason, result.stderr)

    def test_deadline_exhaustion_refuses_subprocess(self):
        clock = Clock()
        deadline = self.H.Deadline(1, clock=clock, sleep=clock.sleep)
        clock.now = 2
        with mock.patch.object(self.H.subprocess, 'run', side_effect=AssertionError('dispatch forbidden')):
            with self.assertRaises(self.H.Refusal):
                self.H.Repo(Path.cwd(), deadline).run(['git', 'status'])

    def test_actual_subprocess_deadline_is_enforced(self):
        repo = self.H.Repo(Path.cwd(), self.H.Deadline(.05))
        start = time.monotonic()
        with self.assertRaises(self.H.Refusal):
            repo.run([sys.executable, '-B', '-c', 'import time; time.sleep(10)'])
        self.assertLess(time.monotonic() - start, 1)

    def test_partial_lsof_inventory_refuses(self):
        repo = self.H.Repo(Path.cwd(), self.H.Deadline(10))
        with mock.patch.object(repo, 'run', return_value=subprocess.CompletedProcess([], 0, 'p12\nfcwd\nn/tmp\n', 'partial visibility')):
            with self.assertRaises(self.H.Refusal):
                self.H.cwd_inventory(repo)

    def test_unreadable_or_deleted_lsof_cwd_entries_refuse(self):
        repo = self.H.Repo(Path.cwd(), self.H.Deadline(10))
        for name in ('/proc/12/cwd (readlink: Permission denied)',
                     '/proc/12/cwd (stat: Permission denied)', '/nonexistent-fixture-cwd (deleted)'):
            with self.subTest(name=name):
                text = f'p{os.getpid()}\nfcwd\nn{Path.cwd()}\np12\nfcwd\nn{name}\n'
                with mock.patch.object(repo, 'run', return_value=subprocess.CompletedProcess([], 0, text, '')):
                    with self.assertRaises(self.H.Refusal):
                        self.H.cwd_inventory(repo)

    def test_gh_adapter_accepts_pending_exit8_but_not_network_error(self):
        runner = mock.Mock()
        runner.run.return_value = subprocess.CompletedProcess([], 8, '[]', '')
        gh = self.H.Gh(runner, 'o/r')
        self.assertEqual(gh.json(['pr', 'checks', '21'], allowed=(0, 8)), [])
        self.assertEqual(runner.run.call_args.kwargs['allowed'], (0, 8))

    def test_gh_no_checks_exit1_is_not_started_instead_of_network_failure(self):
        runner = mock.Mock()
        runner.run.side_effect = [subprocess.CompletedProcess([], 1, '', 'no checks reported on branch feature\n'),
            subprocess.CompletedProcess([], 0, '{"workflow_runs": []}', ''),
            subprocess.CompletedProcess([], 0, '{"check_runs": []}', ''),
            subprocess.CompletedProcess([], 0, '{"check_runs": []}', ''),
            subprocess.CompletedProcess([], 0, '[]', '')]
        gh = self.H.Gh(runner, 'o/r')
        try:
            evidence = gh.evidence(21, 'a' * 40)
        except self.H.Refusal as error:
            self.fail('absent checks must enter bounded backoff: ' + str(error))
        self.assertEqual(self.M.ci_state(evidence, 'a' * 40)[0], 'WAIT')

    def test_gh_no_checks_handling_does_not_swallow_network_errors(self):
        runner = mock.Mock()
        runner.run.return_value = subprocess.CompletedProcess([], 1, '', 'error connecting to api.github.com\n')
        gh = self.H.Gh(runner, 'o/r')
        with self.assertRaises(self.H.Refusal):
            gh.evidence(21, 'a' * 40)

    def test_open_pr_pagination_is_complete_or_refuses(self):
        runner = mock.Mock()
        full = [{'head': {'ref': 'feature' + str(i)}} for i in range(100)]
        runner.run.side_effect = [subprocess.CompletedProcess([], 0, json.dumps(full), ''),
                                  subprocess.CompletedProcess([], 0, json.dumps([{'head': {'ref': 'last'}}]), '')]
        gh = self.H.Gh(runner, 'o/r')
        self.assertEqual(len(gh.open_heads()), 101)
        self.assertEqual(runner.run.call_count, 2)
        runner.run.side_effect = None
        runner.run.return_value = subprocess.CompletedProcess([], 0, json.dumps(full), '')
        with self.assertRaises(self.H.Refusal):
            gh.open_heads()
        self.assertLessEqual(runner.run.call_count, 22)

    def test_no_forbidden_mutation_command_in_production(self):
        root = Path(__file__).resolve().parents[1]
        for name in ('git_hygiene.py', 'git_merge_gate.py'):
            tree = ast.parse((root / 'tools' / name).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    self.assertNotIn(node.value, ('--hard', '-D', '--force', '--force-with-lease', 'clean', 'rm'))

    def test_workflow_is_pinned_bounded_cpu_push_and_pr_only(self):
        workflow = Path(__file__).resolve().parents[1] / '.github/workflows/ci.yml'
        self.assertTrue(workflow.is_file(), 'missing implementation: CI workflow')
        text = workflow.read_text()
        self.assertIn('push:', text)
        self.assertIn('pull_request:', text)
        self.assertRegex(text, r'push:\s*\n\s+branches: \[master\]')
        self.assertRegex(text, r'pull_request:\s*\n\s+branches: \[master\]')
        self.assertIn('python-version: "3.11"', text)
        self.assertIn('timeout-minutes: 8', text)
        self.assertIn('branches: [master]', text)
        self.assertIn('pull_request.head.sha', text)
        self.assertNotIn('schedule:', text)
        self.assertNotIn('workflow_run:', text)
        self.assertNotIn('workflow_dispatch:', text)
        self.assertRegex(text, r'actions/checkout@[0-9a-f]{40}')
        self.assertRegex(text, r'actions/setup-python@[0-9a-f]{40}')

    def test_real_lsof_sees_fixture_child_cwd(self):
        self.assertIsNotNone(shutil.which('lsof'), 'CI requires lsof')
        with tempfile.TemporaryDirectory(prefix='git-cwd-') as directory:
            child = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(15)'], cwd=directory)
            try:
                time.sleep(.03)
                repo = self.H.Repo(Path.cwd(), self.H.Deadline(10))
                run = repo.run
                with mock.patch.object(repo, 'run', side_effect=lambda args: run([*args, '-p', f'{os.getpid()},{child.pid}'])):
                    inventory = self.H.cwd_inventory(repo)
                self.assertEqual(inventory[child.pid], Path(directory).resolve())
            finally:
                child.terminate()
                child.wait(timeout=5)


class DashboardTimestampPortability(unittest.TestCase):
    def setUp(self):
        tools = str(Path(__file__).resolve().parents[1] / 'tools')
        with mock.patch.object(sys, 'path', [tools, *sys.path]):
            self.X = importlib.import_module('dashboard_experiment')
        self.temp = tempfile.TemporaryDirectory(prefix='git-dashboard-timestamps-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.logs = self.root / 'results' / 'c10w_oracle_logs'
        self.logs.mkdir(parents=True)
        self.finished = self.logs / 'behavior_F_r0_mint1_s1.log'
        self.finished.write_text('BEHAVIOR mint1: raw=27 binding=27\nSTAGE_EXIT=0\n')
        self.current = self.logs / 'p2-eval.log'
        self.current.write_text('step 7 loss 0.5\nPortable timestamp progress marker\n')
        os.utime(self.finished, (2000000000, 2000000000))
        os.utime(self.current, (2000000010, 2000000010))
        (self.logs / 'fixture_started.json').write_text(json.dumps({'plan': ['first', 'second', 'third']}))

    @staticmethod
    def plain(lines):
        import re
        return re.sub(r'\033\[[0-9;]*m', '', '\n'.join(lines))

    def stat_without_or_with_birthtime(self, native):
        actual_stat = os.stat
        def stat(path, *args, **kwargs):
            value = actual_stat(path, *args, **kwargs)
            fields = {'st_mtime': value.st_mtime, 'st_mode': value.st_mode}
            if native:
                fields['st_birthtime'] = value.st_mtime - 65
            return SimpleNamespace(**fields)
        self.assertEqual(hasattr(stat(self.finished), 'st_birthtime'), native)
        return stat

    def test_run_rows_uses_birthtime_or_mtime_without_birthtime(self):
        for native, duration in ((False, '0m00s'), (True, '1m05s')):
            with self.subTest(native_birthtime=native):
                with mock.patch.object(self.X.os, 'stat', side_effect=self.stat_without_or_with_birthtime(native)):
                    try:
                        lines, _, _ = self.X.run_rows([str(self.finished)], 110)
                    except AttributeError as error:
                        self.fail('run_rows must accept stat without birthtime: ' + str(error))
                text = self.plain(lines)
                self.assertIn('27/72', text)
                self.assertIn(duration, text)

    def test_render_sorts_and_times_completed_logs_without_birthtime(self):
        state = {'unavailable': None, 'jobs': [{'named': False, 'pids': ['101'], 'job_label': 'p2-eval'}],
                 'cpu_jobs': [], 'running': ('c10w', 'p2-eval', '01:00')}
        for native, duration in ((False, '0m00s'), (True, '1m05s')):
            with self.subTest(native_birthtime=native):
                with mock.patch.object(self.X, 'ROOT', str(self.root)), \
                     mock.patch.object(self.X.dashboard_live, 'gpu_state', return_value=state), \
                     mock.patch.object(self.X, 'machine', return_value=' Machine fixture; no GPU probe'), \
                     mock.patch.object(self.X.os, 'stat', side_effect=self.stat_without_or_with_birthtime(native)):
                    try:
                        lines = self.X.render(110, 40)
                    except AttributeError as error:
                        self.fail('render must accept stat without birthtime: ' + str(error))
                text = self.plain(lines)
                for expected in ('stage p2-eval', '1 of 3 runs', 'FINISHED RUNS', '27/72',
                                 duration, 'NOW', 'training step 7', 'Portable timestamp progress marker'):
                    self.assertIn(expected, text)
                self.assertLessEqual(len(lines), 40)
                self.assertTrue(all(len(self.plain([line])) <= 110 for line in lines))


if __name__ == '__main__':
    unittest.main()
