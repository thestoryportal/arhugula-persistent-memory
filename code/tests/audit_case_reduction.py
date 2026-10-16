"""AuditControls partial-reduction case; a mixin composed by test_context_audit."""
import subprocess
from unittest.mock import patch

import test_icm21 as shared
from test_icm21 import put


class PartialReductionCases:
    def test_partial_reduction(self):
        module = self.checker()
        root, config = self.seed(['C-ROOT', 'C-WORKTREE'])
        # No commit or custody evidence exists in this miniature: never invent it.
        value = self.observe(module, root, config)
        self.assertEqual(value['overall_status'], 'UNVERIFIED')
        self.assertTrue(value['coverage']['inspected'])
        self.assertTrue(value['unreviewed_narrative_paths'] or
                        not value['reviewed_narrative_paths'])
        nightly = self.observe(module, root, config, 'nightly')
        self.assertEqual(nightly['overall_status'], 'UNVERIFIED')
        self.assertNotEqual(nightly['check_id'], value['check_id'])
        # A known violation wins over missing custody, source or nightly evidence.
        copy_root = root / 'ignored-copy'
        put(copy_root, 'CLAUDE.md', b'# Copy\n')
        put(copy_root, 'program/program_state.json', b'{}')
        put(copy_root, '_index/path-map.tsv', shared.HEADER)
        put(copy_root, '.git', 'gitdir: ' + str(root / '.git') + '\n')
        config['required_checks'].append('C-BOUNDARY')
        failed = self.observe(module, root, config)
        self.assertEqual(failed['overall_status'], 'FAIL')
        again = self.observe(module, root, config)
        self.assertEqual([f['id'] for f in failed['findings']],
                         [f['id'] for f in again['findings']])
        self.assertTrue(failed['findings'])
        # An unreadable object store is missing evidence; only Git's silent absence of
        # the tip object (or a non-commit tip) is a known worktree violation.
        area = module.area('icm21_audit_root')
        real_run, tip = subprocess.run, '1' * 40

        def lanes(cat_file, prunable=False):
            def run(argv, **kwargs):
                if argv[1] == 'worktree':
                    raw = 'worktree /fixture/lane\nHEAD ' + tip + '\n'
                    raw += '\nworktree /fixture/gone\nHEAD ' + tip + '\nprunable\n' if prunable else ''
                    return subprocess.CompletedProcess(argv, 0, raw.encode(), b'')
                return cat_file(argv, **kwargs)
            return run

        def denied(argv, **kwargs):
            return subprocess.CompletedProcess(
                argv, 128, b'', b'fatal: failed to read object: Permission denied\n')

        def tree(argv, **kwargs):
            return subprocess.CompletedProcess(argv, 0, b'tree\n' if '-t' in argv else b'', b'')

        def custody():
            return area.check('C-WORKTREE', root, 'session', config, {'inspected': []})
        with patch.object(area.subprocess, 'run', side_effect=lanes(denied)):
            with self.assertRaises(module.Unverified) as unread:
                custody()
        self.assertIn('could not be read: ' + tip, str(unread.exception))
        with patch.object(area.subprocess, 'run', side_effect=lanes(denied, prunable=True)):
            status, _, findings = custody()
        self.assertEqual((status, [f['paths'] for f in findings]), ('FAIL', [['/fixture/gone']]))
        with patch.object(area.subprocess, 'run', side_effect=lanes(real_run)):
            status, reason, _ = custody()
        self.assertEqual((status, reason), ('FAIL', 'Worktree branch tip is unreachable: ' + tip))
        with patch.object(area.subprocess, 'run', side_effect=lanes(tree)):
            self.assertEqual(custody()[0], 'FAIL')
