"""Staged CI bypass case (StagedControls)."""
import re
import shlex
import unittest

import yaml

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
        commands = []
        for step in yaml.safe_load(workflow)['jobs']['cpu']['steps']:
            for line in step.get('run', '').splitlines():
                argv = shlex.split(line)
                while argv and re.fullmatch(r'[A-Za-z_]\w*=.*', argv[0]):
                    argv.pop(0)
                commands.append((step, argv))

        def required(match, behavior):
            found = [(step, argv) for step, argv in commands if match(argv)]
            self.assertEqual(len(found), 1, behavior + ' step count')
            self.assertNotIn('if', found[0][0], behavior + ' step is conditional')
            return found[0][1]

        unittest_prefix = ['python3', '-B', '-m', 'unittest']
        self.assertEqual(required(lambda a: 'code/state/icm21_check.py' in a, 'staged closure'),
                         ['python3', '-B', 'code/state/icm21_check.py', 'staged', '--root', '$PWD'])
        checker = required(lambda a: a[:4] == unittest_prefix and 'discover' not in a and any(
            t.startswith('test_icm21') or t == 'test_context_audit' for t in a), 'checker suites')
        self.assertCountEqual([t for t in checker[4:] if t != '-v'], [
            'test_icm21.ApprovedWireControls', 'test_icm21.StagedControls',
            'test_icm21.ReaderControls', 'test_icm21.FixtureContractControls',
            'test_icm21.GuardControls.test_admission_shapes',
            'test_icm21.GuardControls.test_fault_denial',
            'test_icm21.GuardControls.test_unsupported_sandbox_denial', 'test_context_audit'])
        self.assertEqual(required(lambda a: 'test_icm21*.py' in a, 'seam suites'),
                         unittest_prefix + ['discover', '-s', 'code/state', '-p', 'test_icm21*.py'])
        root = self.miniature()
        self.seed_closure(root)
        put(root, 'projects/new/CONTEXT.md', b'# Stale CI fixture\n')
        self.git(root, 'add', '.')
        self.git(root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'bypassed fixture')
        result = self.cli(root, 'code/state/build_index.py', '--check')
        self.assertEqual(result.returncode, 1, 'clean committed stale checkout passed CI command')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.git(root, 'add', '.')
        self.git(root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'regenerated fixture')
        result = self.cli(root, 'code/state/build_index.py', '--check')
        self.assertEqual(result.returncode, 0, (result.stdout + result.stderr).decode())
        self.assertFalse([x for x in self.staged(root) if x['status'] == 'FAIL'])
