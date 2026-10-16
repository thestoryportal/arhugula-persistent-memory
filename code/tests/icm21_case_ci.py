"""Staged CI bypass case (StagedControls)."""
import re
import unittest

from icm21_fixtures import SOURCE_ROOT, put


class CiBypassCase:
    def test_ci_bypass(self):
        self.checker()
        workflow = (SOURCE_ROOT / '.github/workflows/ci.yml').read_text()
        for command in ('code/state/build_index.py --check', 'code/state/render_state.py --check',
                        'code/agents/twins.py --check', 'test_git_automation.py',
                        'lab.runners.test_c10w_p2_gate', 'apps.dashboard.test_dashboard_live',
                        'apps.dashboard.test_dashboard_gpu_detector', 'test_icm21',
                        'test_context_audit', 'staged'):
            self.assertIn(command, workflow)
        self.assertIn("discover -s code/state -p 'test_icm21*.py'", workflow)
        tokens = workflow.split()
        guards = {m.group(1) for m in map(re.compile(r'test_icm21\.GuardControls\.(\w+)').fullmatch, tokens) if m}
        self.assertEqual(guards, {'test_admission_shapes', 'test_fault_denial',
                                  'test_unsupported_sandbox_denial'})
        self.assertNotIn('test_icm21.GuardControls', tokens)
        self.assertNotIn('test_icm21', tokens)
        root = self.miniature()
        self.seed_closure(root)
        put(root, 'projects/new/CONTEXT.md', b'# Stale CI fixture\n')
        self.git(root, 'add', '.')
        self.git(root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'bypassed fixture')
        result = self.cli(root, 'code/state/build_index.py', '--check')
        self.assertEqual(result.returncode, 1, 'clean committed stale checkout passed CI command')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))
