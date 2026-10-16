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

    def assert_pr_branch_never_pushed(self):
        pushes = [c['command'] for c in self.repo.commands if 'push' in c['command']]
        self.assertTrue(all('--delete' in c for c in pushes), pushes)

    def stale_disjoint(self):
        self.commit('master', {'other.txt': 'master only\n'})

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
            'accepted': True, 'master_sha': master, 'head_sha': head, 'merge_bases': [self.fixture.base],
            'pr_files': ['feature.txt'], 'master_files': ['other.txt'], 'overlap': []})
        for name in ('ci', 'stable_head_base', 'ready', 'merge', 'master_ci', 'post_hygiene'):
            self.assertEqual(report['checks'][name]['status'], 'PASS', name)
        self.assertIn(('evidence', head, False), self.gh.calls)
        self.assertIn(('evidence', self.gh.merge_sha, True), self.gh.calls)
        self.assertEqual(self.fixture.git('rev-parse', self.gh.merge_sha + '^2').strip(), head)
        self.assert_pr_branch_never_pushed()

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

    def test_shared_file_in_earlier_master_commit_refused(self):
        self.commit('feature', {'base.txt': 'pr edit\n'})
        self.commit('master', {'base.txt': 'master edit\n'})
        self.commit('master', {'other.txt': 'last master commit\n'})
        report = self.gate()
        self.assert_refused_at_branches(report, 'base.txt')
        self.assertEqual(report['stale_base']['master_files'], ['base.txt', 'other.txt'])

    def test_pr_rename_source_changed_on_master_refused(self):
        self.commit('feature', move=('base.txt', 'pr-moved.txt'))
        self.commit('master', {'base.txt': 'master edit\n'})
        report = self.gate()
        self.assert_refused_at_branches(report, 'base.txt')
        self.assertEqual(report['stale_base']['pr_files'], ['base.txt', 'feature.txt', 'pr-moved.txt'])
        self.assertEqual(report['stale_base']['overlap'], ['base.txt'])

    def test_criss_cross_merge_bases_refused(self):
        first, second = self.gh.head, self.commit('master', {'other.txt': 'master only\n'})
        def tree(name):
            self.fixture.git('checkout', '--detach', first)
            (self.fixture.root / name).write_text(name + '\n')
            self.fixture.git('add', name)
            self.fixture.git('commit', '-m', 'tree for ' + name)
            return self.fixture.git('rev-parse', 'HEAD^{tree}').strip()
        head_tree, master_tree = tree('pr-only.txt'), tree('master-only.txt')
        head = self.fixture.git('commit-tree', head_tree, '-p', first, '-p', second, '-m', 'cross head').strip()
        master = self.fixture.git('commit-tree', master_tree, '-p', second, '-p', first, '-m', 'cross master').strip()
        self.fixture.git('update-ref', 'refs/heads/feature', head)
        self.fixture.git('update-ref', 'refs/heads/master', master)
        self.fixture.git('checkout', 'master')
        self.fixture.git('push', 'origin', 'master', 'feature')
        self.gh.head, self.gh.base = head, master
        bases = sorted(self.fixture.git('merge-base', '--all', head, master).split())
        self.assertEqual(bases, sorted([first, second]))
        report = self.gate(dry_run=False)
        self.assert_refused_at_branches(report, bases[0], bases[1])
        self.assertIs(report['stale_base']['accepted'], False)
        self.assertEqual(sorted(report['stale_base']['merge_bases']), bases)

    def test_stale_base_unknown_mergeability_refused(self):
        self.stale_disjoint()
        original = self.gh.pr
        self.gh.pr = lambda number: dict(original(number), mergeable='UNKNOWN')
        report = self.gate(dry_run=False)
        self.assert_refused_at_branches(report, 'mergeable=UNKNOWN')
        self.assertIs(report['stale_base']['accepted'], False)

    def test_stale_base_failed_master_ci_reports_merged_with_failure(self):
        self.stale_disjoint()
        self.gh.post_state = 'FAIL'
        report = self.gate(dry_run=False)
        self.assertFalse(report['ok'], report)
        self.assertIs(report['merged'], True)
        self.assertEqual(report['status'], 'MERGED_WITH_FAILURE')
        self.assertEqual(report['checks']['master_ci']['status'], 'FAIL')
        self.assertTrue(report['stale_base']['accepted'])

    def test_stale_base_apply_needs_the_lock(self):
        self.stale_disjoint()
        with self.repo.lock():
            report = self.gate(dry_run=False)
        self.assertFalse(report['ok'], report)
        self.assertIs(report['merged'], False)
        self.assertIn('another git automation invocation is active', ' '.join(report['errors']))
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_stale_base_mergeability_lost_after_ci_refused_by_stable(self):
        self.stale_disjoint()
        original = self.gh.evidence
        def evidence(*args, **kwargs):
            value = original(*args, **kwargs)
            self.gh.conflict = True
            return value
        self.gh.evidence = evidence
        report = self.gate(dry_run=False)
        self.assertFalse(report['ok'], report)
        self.assertIs(report['merged'], False)
        self.assertEqual(report['checks']['branches']['status'], 'PASS')
        self.assertEqual(report['checks']['stable_head_base']['status'], 'FAIL')
        self.assertNotIn('merge', [c[0] for c in self.gh.calls])

    def test_stale_base_master_moves_at_merge_reports_moved_base(self):
        self.stale_disjoint()
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
        self.assertFalse(report['ok'], report)
        self.assertEqual(report['status'], 'MERGED_ON_MOVED_BASE')
        self.assertEqual(report['merge_first_parent'], advanced[0])
        self.assertIn('merged onto a moved base', ' '.join(report['errors']))

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
