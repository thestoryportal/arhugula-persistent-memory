"""Staged CI bypass case (StagedControls)."""
import unittest

from icm21_fixtures import SOURCE_ROOT, put


class CiBypassCase:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_ci_bypass(self):
        self.checker()
        workflow = (SOURCE_ROOT / '.github/workflows/ci.yml').read_text()
        for command in ('code/state/build_index.py --check', 'code/state/render_state.py --check',
                        'code/agents/twins.py --check', 'test_git_automation.py',
                        'lab.runners.test_c10w_p2_gate', 'apps.dashboard.test_dashboard_live',
                        'apps.dashboard.test_dashboard_gpu_detector', 'test_icm21',
                        'test_context_audit', 'staged'):
            self.assertIn(command, workflow)
        root = self.miniature()
        self.seed_closure(root)
        put(root, 'projects/new/CONTEXT.md', b'# Stale CI fixture\n')
        self.git(root, 'add', '.')
        self.git(root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'bypassed fixture')
        result = self.cli(root, 'code/state/build_index.py', '--check')
        self.assertEqual(result.returncode, 1, 'clean committed stale checkout passed CI command')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))
