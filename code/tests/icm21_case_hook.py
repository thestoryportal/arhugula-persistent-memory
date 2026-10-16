"""Staged real pre-commit hook case (StagedControls)."""
import unittest

from icm21_fixtures import SOURCE_ROOT, put


class RealHookCase:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_real_hook(self):
        self.checker()
        root = self.miniature()
        self.seed_closure(root)
        hook = put(root, '.git/hooks/pre-commit',
                   (SOURCE_ROOT / 'code/ops/git/hooks/pre-commit').read_bytes())
        hook.chmod(0o755)
        put(root, 'projects/new/CONTEXT.md', b'# New fixture\n')
        self.git(root, 'add', 'projects/new/CONTEXT.md')
        rejected = self.run_argv(root, ['git', 'commit', '-qm', 'stale fixture'])
        self.assertNotEqual(rejected.returncode, 0, 'real hook accepted stale staged index')
        self.assertTrue((rejected.stdout + rejected.stderr).strip())
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.git(root, 'add', '.')
        accepted = self.run_argv(root, ['git', 'commit', '-qm', 'fresh fixture'])
        self.assertEqual(accepted.returncode, 0, (accepted.stdout + accepted.stderr).decode())
        self.assertFalse((self.scratch / '_audit.out').exists())
