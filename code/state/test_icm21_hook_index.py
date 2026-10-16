"""The real pre-commit hook refuses commits its staged check cannot vouch for (plan Step 19)."""
import sys

# Module imports, so the loader does not collect FixtureCase or StagedControls here.
import icm21_fixtures as fixtures
import icm21_staged_cases as staged


class HookIndexSeam(fixtures.FixtureCase):
    """check_staged reads only the default index, so the hook must refuse any other one."""
    checker = staged.StagedCases.checker
    seed_closure = staged.StagedCases.seed_closure

    def hooked(self):
        """A miniature with a fresh staged closure and the real hook installed."""
        self.checker()
        root = self.miniature()
        self.seed_closure(root)
        hook = fixtures.put(root, '.git/hooks/pre-commit',
                            (fixtures.SOURCE_ROOT / 'code/ops/git/hooks/pre-commit').read_bytes())
        hook.chmod(0o755)
        return root

    def output(self, completed):
        return (completed.stdout + completed.stderr).decode('utf-8', 'replace')

    def test_hook_refuses_other_index(self):
        root = self.hooked()
        for argv in (['git', 'commit', '-qm', 'msg', 'CLAUDE.md'], ['git', 'commit', '-qam', 'msg']):
            with self.subTest(argv=argv):
                refused = self.run_argv(root, argv)
                self.assertNotEqual(refused.returncode, 0, 'real hook accepted ' + ' '.join(argv))
                self.assertIn('not the default index', self.output(refused))
        accepted = self.run_argv(root, ['git', 'commit', '-qm', 'msg'])
        self.assertEqual(accepted.returncode, 0, self.output(accepted))

    def test_hook_refuses_interpreter_without_dependencies(self):
        root = self.hooked()
        (root / '.venv').unlink()
        # The same venv without site-packages: present, runnable, but no yaml or markdown_it.
        python = fixtures.put(root, '.venv/bin/python',
                              '#!/bin/sh\nexec "' + sys.executable + '" -S "$@"\n')
        python.chmod(0o755)
        refused = self.run_argv(root, ['git', 'commit', '-qm', 'msg'])
        self.assertNotEqual(refused.returncode, 0, 'real hook ran without its dependencies')
        self.assertIn('cannot import yaml and markdown_it', self.output(refused))
