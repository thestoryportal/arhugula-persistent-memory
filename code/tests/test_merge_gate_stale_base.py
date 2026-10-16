"""Merge gate on a stale base: accept only when nothing on master since the merge-base touched the PR's files."""
import tempfile
import unittest
from unittest import mock

from test_git_automation import Clock, FakeGh, Fixture, load_tools


class StaleBaseGateTests(unittest.TestCase):
    def setUp(self):
        self.H, self.M = load_tools(self)
        self.temp = tempfile.TemporaryDirectory(prefix='merge-gate-stale-')
        self.addCleanup(self.temp.cleanup)
        self.fixture = Fixture(self.temp.name)
        self.clock = Clock()
        self.repo = self.H.Repo(self.fixture.root, self.H.Deadline(60, clock=self.clock, sleep=self.clock.sleep))
        self.gh = FakeGh(self.fixture)

    def gate(self, dry_run=True, **kwargs):
        with mock.patch.object(self.H, 'cwd_inventory', return_value={}):
            return self.M.gate(self.repo, self.gh, 21, dry_run=dry_run, **kwargs)

    def commit(self, branch, files=None, move=None):
        self.fixture.git('checkout', branch)
        for name, text in (files or {}).items():
            (self.fixture.root / name).write_text(text)
        if move:
            self.fixture.git('mv', *move)
        self.fixture.git('add', '-A')
        self.fixture.git('commit', '-m', branch + ' change')
        self.fixture.git('push', 'origin', branch)
        sha = self.fixture.git('rev-parse', 'HEAD').strip()
        self.fixture.git('checkout', 'master')
        if branch == 'master':
            self.gh.base = sha
        else:
            self.gh.head = sha
        return sha

    def assert_refused_at_branches(self, report, *needles):
        self.assertFalse(report['ok'], report)
        self.assertIs(report['merged'], False)
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])
        self.assertEqual(report['checks']['branches']['status'], 'FAIL', report['checks']['branches'])
        for needle in needles:
            self.assertIn(needle, report['checks']['branches']['reason'])

    def test_fresh_base_accepted_unchanged(self):
        report = self.gate()
        self.assertTrue(report['ok'], report)
        self.assertEqual(report['status'], 'DRY_RUN_PASS')
        self.assertIsNone(report['stale_base'])

    def test_stale_base_disjoint_files_accepted_and_recorded(self):
        head = self.gh.head
        master = self.commit('master', {'other.txt': 'master only\n'})
        report = self.gate(dry_run=False)
        self.assertTrue(report['ok'], report)
        self.assertEqual(report['status'], 'MERGED')
        self.assertEqual(report['base_sha'], master)
        self.assertEqual(report['merge_first_parent'], master)
        self.assertEqual(report['stale_base'], {
            'accepted': True, 'master_sha': master, 'head_sha': head, 'merge_base': self.fixture.base,
            'pr_files': ['feature.txt'], 'master_files': ['other.txt'], 'overlap': []})
        for name in ('ci', 'stable_head_base', 'ready', 'merge', 'master_ci', 'post_hygiene'):
            self.assertEqual(report['checks'][name]['status'], 'PASS', name)
        self.assertIn(('evidence', head, False), self.gh.calls)
        self.assertIn(('evidence', self.gh.merge_sha, True), self.gh.calls)
        self.assertEqual(self.fixture.git('rev-parse', self.gh.merge_sha + '^2').strip(), head)

    def test_stale_base_dry_run_never_updates_pr_branch(self):
        self.commit('master', {'other.txt': 'master only\n'})
        before = self.fixture.git('show-ref'), self.fixture.remote_tip('feature')
        report = self.gate()
        self.assertTrue(report['ok'], report)
        self.assertTrue(report['stale_base']['accepted'])
        self.assertEqual((self.fixture.git('show-ref'), self.fixture.remote_tip('feature')), before)

    def test_stale_base_shared_file_refused(self):
        self.commit('feature', {'base.txt': 'pr edit\n'})
        self.commit('master', {'base.txt': 'master edit\n'})
        report = self.gate(dry_run=False)
        self.assert_refused_at_branches(report, 'base.txt')
        self.assertIs(report['stale_base']['accepted'], False)
        self.assertEqual(report['stale_base']['overlap'], ['base.txt'])

    def test_shared_file_in_earlier_pr_commit_refused(self):
        self.commit('feature', {'base.txt': 'pr edit\n'})
        self.commit('feature', {'later.txt': 'last pr commit\n'})
        self.commit('master', {'base.txt': 'master edit\n'})
        report = self.gate()
        self.assert_refused_at_branches(report, 'base.txt')
        self.assertEqual(report['stale_base']['pr_files'], ['base.txt', 'feature.txt', 'later.txt'])

    def test_master_rename_of_pr_file_refused(self):
        self.commit('feature', {'base.txt': 'base\npr edit\n'})
        self.commit('master', move=('base.txt', 'moved.txt'))
        report = self.gate()
        self.assert_refused_at_branches(report, 'base.txt')
        self.assertEqual(report['stale_base']['master_files'], ['base.txt', 'moved.txt'])
        self.assertEqual(report['stale_base']['overlap'], ['base.txt'])

    def test_github_base_differs_from_origin_master_refused(self):
        self.gh.base = 'e' * 40
        report = self.gate()
        self.assert_refused_at_branches(report, 'include the current origin/master')
        self.assertIsNone(report['stale_base'])

    def test_stale_base_requires_mergeable(self):
        self.commit('master', {'other.txt': 'master only\n'})
        self.gh.conflict = True
        report = self.gate()
        self.assert_refused_at_branches(report, 'MERGEABLE')
        self.assertIs(report['stale_base']['accepted'], False)


if __name__ == '__main__':
    unittest.main()
