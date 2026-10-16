"""AuditControls partial-reduction case; a mixin composed by test_context_audit."""
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
