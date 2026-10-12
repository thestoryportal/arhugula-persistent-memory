"""CPU/stdlib tests; every git mutation is confined to disposable fixtures."""
import ast
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


def load_tools(test):
    for name in ('tools.git_hygiene', 'tools.git_merge_gate'):
        test.assertIsNotNone(importlib.util.find_spec(name), 'missing implementation: ' + name)
    return importlib.import_module('tools.git_hygiene'), importlib.import_module('tools.git_merge_gate')


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
                'check_runs': [{'name': 'cpu', 'head_sha': sha, 'status': status,
                                'conclusion': conclusion, 'html_url': link}],
                'statuses': [],
                'runs': [{'databaseId': 101, 'headSha': sha, 'headBranch': 'master' if post else 'feature',
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

    def master(self):
        return self.merge_sha or self.base


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

    def test_clean_idle_worktree_removed_then_second_apply_noop(self):
        target = self.fixture.worktree('idle')
        first = self.hygiene(True)
        self.assertTrue(first['ok'], first)
        self.assertFalse(target.exists())
        row = next(w for w in first['worktrees'] if w['path'] == str(target.resolve()))
        self.assertGreater(row['size_before_bytes'], 0)
        self.assertEqual(row['size_after_bytes'], 0)
        self.assertEqual(self.hygiene(True)['actions'], [])

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
            subprocess.CompletedProcess([], 0, '[]', ''),
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


if __name__ == '__main__':
    unittest.main()
