"""StagedControls helpers and its closure, hook and CI cases (mixin for test_icm21)."""
import dataclasses
import json
import os
import unittest
from unittest.mock import patch

from icm21_fixtures import SOURCE_ROOT, encoded, put


class StagedCases:
    def checker(self):
        return self.module('code/state/icm21_check.py', 'check_staged')

    def seed_closure(self, root):
        for relative in ('code/state/build_index.py', 'code/state/resolve_path.py',
                         'code/state/icm21_check.py', 'code/state/render_state.py',
                         'code/state/llmdb_records.py', 'code/agents/twins.py',
                         'code/gates/closeout_check.py', 'code/gates/closeout_fingerprints.json',
                         'code/ops/git/hooks/pre-commit'):
            put(root, relative, self.require_file(relative, 'staged source closure').read_bytes())
        for relative in ('CLAUDE.md', 'AGENTS.md', 'routing.md',
                         'map/CLAUDE.md', 'map/AGENTS.md', 'map/routing.md'):
            put(root, relative, b'# Miniature authority\n')
        put(root, 'code/gates/closeout_fingerprints.json', b'{}')
        put(root, '_system/governance/workspace-admission.json', b'{}')
        self.publish_miniature(root)
        state = json.loads((SOURCE_ROOT / 'program/program_state.json').read_bytes())
        state['work_queue']['items'] = []
        put(root, 'program/program_state.json', encoded(state))
        for script in ('code/state/render_state.py', 'code/agents/twins.py'):
            value = self.cli(root, script, '--write')
            self.assertEqual(value.returncode, 0, (value.stdout + value.stderr).decode())
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.git(root, 'add', '.')

    def staged(self, root):
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            result = self.checker().check_staged(root)
        self.assertIsInstance(result, tuple)
        return [dataclasses.asdict(x) if dataclasses.is_dataclass(x) else x for x in result]

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_source_output_closure(self):
        self.checker()
        root = self.miniature()
        self.seed_closure(root)
        self.assertFalse(any(x['status'] == 'FAIL' for x in self.staged(root)))
        paths = ('program/program_state.json', 'code/state/resolve_path.py',
                 '_index/experiments.md', 'program/STATUS.md', 'map/CLAUDE.md',
                 'code/gates/closeout_fingerprints.json',
                 '_system/governance/workspace-admission.json')
        for relative in paths:
            with self.subTest(path=relative):
                original = (root / relative).read_bytes()
                (root / relative).write_bytes(original + b'\n')
                findings = self.staged(root)
                self.assertTrue(any(x['status'] == 'FAIL' for x in findings), relative)
                (root / relative).write_bytes(original)
        put(root, 'experiments/new/CONTEXT.md', b'---\nstatus: designed\n---\n')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))
        self.git(root, 'add', 'experiments/new/CONTEXT.md')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)), 'stale staged index')
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)), 'fresh unstaged outputs')
        self.git(root, 'add', '.')
        self.assertFalse(any(x['status'] == 'FAIL' for x in self.staged(root)))

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
