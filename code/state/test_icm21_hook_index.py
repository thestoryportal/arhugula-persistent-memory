"""The real pre-commit hook refuses commits its staged check cannot vouch for (plan Step 19)."""
import os
import shutil
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

    def tool(self, name, body):
        """A PATH shim for one command; the hook resolves the command through PATH."""
        shim = fixtures.put(self.scratch, 'bin/' + name, '#!/bin/sh\n' + body)
        shim.chmod(0o755)
        return 'PATH=' + str(shim.parent) + os.pathsep + os.environ['PATH']

    def test_hook_refuses_index_it_cannot_canonicalize(self):
        # Both index paths are non-ASCII and the resolver cannot print them: no path, no pass.
        self.checker()
        root = self.miniature('répo')
        self.seed_closure(root)
        hook = fixtures.put(root, '.git/hooks/pre-commit',
                            (fixtures.SOURCE_ROOT / 'code/ops/git/hooks/pre-commit').read_bytes())
        hook.chmod(0o755)
        refused = self.run_argv(root, ['env', 'PYTHONIOENCODING=ascii',
                                       'git', 'commit', '-qm', 'msg', 'CLAUDE.md'])
        self.assertNotEqual(refused.returncode, 0, 'real hook accepted an unresolved index')
        self.assertIn('not the default index', self.output(refused))

    def test_hook_refuses_empty_default_index(self):
        # realpath('') is the working directory, so an empty default index must not reach the comparison.
        root = self.hooked()
        git = shutil.which('git')
        for status in (0, 1):
            with self.subTest(status=status):
                path = self.tool('git', '[ "$1 $2 $3" = "rev-parse --git-path index" ] && exit '
                                 + str(status) + '\nexec "' + git + '" "$@"\n')
                refused = self.run_argv(root, ['env', path, 'GIT_INDEX_FILE=' + str(root),
                                               'bash', '.git/hooks/pre-commit'])
                self.assertNotEqual(refused.returncode, 0, 'real hook accepted an empty default index')
                self.assertIn('not the default index', self.output(refused))

    def test_hook_log_is_unique_and_outside_checkout(self):
        root = self.hooked()
        record = self.scratch / 'mktemp.record'
        path = self.tool('mktemp', 'made=$("' + shutil.which('mktemp') + '" "$@") || exit\n'
                         'printf "%s\\n" "$made" >>"' + str(record) + '"\nprintf "%s\\n" "$made"\n')
        accepted = self.run_argv(root, ['env', path, 'TMPDIR=' + str(root),
                                        'git', 'commit', '-qm', 'msg'])
        self.assertEqual(accepted.returncode, 0, self.output(accepted))
        self.assertTrue(record.is_file(), 'real hook allocated no unique log')
        logs = record.read_text().split()
        self.assertEqual(len(logs), 1, logs)
        log = os.path.realpath(logs[0])
        self.assertFalse(log.startswith(os.path.realpath(root) + os.sep), 'log inside checkout: ' + log)
        self.assertFalse(os.path.lexists(log), 'log not removed: ' + log)

    def test_hook_requires_pass_status(self):
        # An exit-0 checker that reports FAIL must still block; the PASS twin shows status alone decides.
        root = self.hooked()
        for status, code in (('FAIL', 1), ('PASS', 0)):
            with self.subTest(status=status):
                fixtures.put(root, 'code/state/icm21_check.py',
                             'print(\'{"status": "' + status + '"}\')\n')
                completed = self.run_argv(root, ['bash', '.git/hooks/pre-commit'])
                self.assertEqual(completed.returncode, code, self.output(completed))
                self.assertEqual('staged closure is not PASS' in self.output(completed), bool(code))

    def test_hook_refuses_secrets(self):
        root = self.hooked()
        # Built at run time, so this source file carries no token signature for the live gate.
        for relative, data in (('.env', 'TOKEN=x\n'), ('notes.txt', 'key ' + 'AKIA' + 'Q' * 16 + '\n')):
            with self.subTest(relative=relative):
                fixtures.put(root, relative, data)
                self.git(root, 'add', relative)
                refused = self.run_argv(root, ['bash', '.git/hooks/pre-commit'])
                self.assertNotEqual(refused.returncode, 0, 'real hook accepted a secret')
                self.assertIn('POSSIBLE SECRET', self.output(refused))
                self.git(root, 'rm', '-q', '--cached', relative)
