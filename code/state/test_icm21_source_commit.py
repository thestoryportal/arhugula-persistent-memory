"""Audit source_commit names the canonical root's HEAD, whatever GIT_* says (plan Step 18)."""
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

# A module import, so the loader does not collect CheckerSeams a second time here.
import test_icm21_check_seams as seams


def fixture_git(root, *argv):
    """Run git in the fixture repository at root, isolated from the caller's Git setup."""
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME='ICM fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='ICM fixture',
                       GIT_COMMITTER_EMAIL='fixture@example.invalid')
    result = subprocess.run(['git', *argv], cwd=root, env=environment,
                            capture_output=True, timeout=30, check=True)
    return result.stdout.decode().strip()


def commit(root):
    """Create one commit in a fresh repository at root and return its HEAD."""
    root.mkdir(exist_ok=True)
    (root / 'marker').write_text(str(root), encoding='utf-8')
    for argv in (('init', '-q'), ('add', 'marker'), ('commit', '-q', '-m', 'fixture')):
        fixture_git(root, *argv)
    return fixture_git(root, 'rev-parse', 'HEAD')


class SourceCommitSeam(unittest.TestCase):
    setUp = seams.CheckerSeams.setUp
    checker = seams.CheckerSeams.checker
    config = seams.CheckerSeams.config

    def test_source_commit_ignores_git_env(self):
        module = self.checker({'icm21_audit_root': seams.AUDIT_AREA})
        root, config = self.config(('C-ROOT',))
        canonical = commit(root)
        other = commit(self.scratch / 'other')
        self.assertNotEqual(canonical, other)
        with patch.dict(os.environ, {'GIT_DIR': str(self.scratch / 'other/.git')}):
            report = module.audit(root, 'session', config)
        self.assertEqual(report['source_commit'], canonical)


# Every staged check passes, so a finding comes only from the closure comparison.
STAGED_FIXTURE = {
    'code/state/build_index.py': b'# fixture stub: the check passes\n',
    'code/state/render_state.py': b'# fixture stub: the check passes\n',
    'code/agents/twins.py': b'# fixture stub: the check passes\n',
    'code/gates/closeout_check.py': b'# fixture stub: the check passes\n',
    'code/gates/closeout_fingerprints.json': b'{}\n',
    '_index/anchor-map.tsv': b'kind\tname\ttarget\tanchor\n',
    '_system/governance/workspace-admission.json': b'{"admitted": []}\n',
}


class StagedClosureSeam(unittest.TestCase):
    """check_staged refusals that the frozen closure case cannot isolate (T018 ruling)."""
    setUp = seams.CheckerSeams.setUp
    checker = seams.CheckerSeams.checker

    def staged_root(self):
        """A full-checkout repository whose index matches its closure on disk."""
        module = self.checker({})
        root = self.scratch / 'root'
        for relative, raw in STAGED_FIXTURE.items():
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / relative).write_bytes(raw)
        fixture_git(root, 'init', '-q')
        fixture_git(root, 'add', '.')
        self.assertEqual(module.check_staged(root), ())
        return module, root

    def reasons(self, module, root):
        return sorted((Path(f['paths'][0]).relative_to(root).as_posix(), f['reason'])
                      for f in module.check_staged(root))

    def test_untracked_closure_input(self):
        module, root = self.staged_root()
        (root / 'README.md').write_bytes(b'untracked narrative tracker\n')
        self.assertEqual(self.reasons(module, root),
                         [('README.md', 'Untracked closure path is absent from the index')])

    def test_skip_worktree_present_on_disk(self):
        module, root = self.staged_root()
        relative = '_system/governance/workspace-admission.json'
        fixture_git(root, 'update-index', '--skip-worktree', relative)
        self.assertTrue(fixture_git(root, 'ls-files', '-t', relative).startswith('S '))
        (root / relative).write_bytes(b'{"admitted": ["escape"]}\n')
        expected = [(relative, 'Disk bytes differ from the staged blob')]
        self.assertEqual(self.reasons(module, root), expected)
        fixture_git(root, 'config', 'core.sparseCheckout', 'true')
        self.assertEqual(self.reasons(module, root), expected)
        (root / relative).unlink()
        self.assertEqual(self.reasons(module, root), [])
        fixture_git(root, 'config', 'core.sparseCheckout', 'false')
        self.assertEqual(self.reasons(module, root),
                         [(relative, 'Staged closure path is missing on disk')])


if __name__ == '__main__':
    unittest.main()
