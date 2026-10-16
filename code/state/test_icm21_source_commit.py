"""Audit source_commit names the canonical root's HEAD, whatever GIT_* says (plan Step 18)."""
import os
import subprocess
import unittest
from unittest.mock import patch

# A module import, so the loader does not collect CheckerSeams a second time here.
import test_icm21_check_seams as seams


def commit(root):
    """Create one commit in a fresh repository at root and return its HEAD."""
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME='ICM fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='ICM fixture',
                       GIT_COMMITTER_EMAIL='fixture@example.invalid')
    root.mkdir(exist_ok=True)
    (root / 'marker').write_text(str(root), encoding='utf-8')
    for argv in (('init', '-q'), ('add', 'marker'), ('commit', '-q', '-m', 'fixture'),
                 ('rev-parse', 'HEAD')):
        result = subprocess.run(['git', *argv], cwd=root, env=environment,
                                capture_output=True, timeout=30, check=True)
    return result.stdout.decode().strip()


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


if __name__ == '__main__':
    unittest.main()
