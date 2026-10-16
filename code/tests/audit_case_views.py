"""AuditControls view-twin freshness case; a mixin composed by test_context_audit."""
import unittest

import test_icm21 as shared
from test_icm21 import put, snapshot


class ViewTwinCases:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_view_twin_freshness(self):
        module = self.checker()
        root, config = self.seed(['C-GENERATED', 'C-TWINS'])
        # Reuse the actual generators with miniature inputs, not mocked PASS rows.
        shared.StagedControls.seed_closure(self, root)
        before = snapshot(root)
        value = self.observe(module, root, config)
        self.check_status(value, 'C-GENERATED', 'PASS')
        self.check_status(value, 'C-TWINS', 'PASS')
        self.assertEqual(snapshot(root), before)
        for path, check in (('_index/projects.md', 'C-GENERATED'),
                            ('program/STATUS.md', 'C-GENERATED'),
                            ('map/AGENTS.md', 'C-TWINS')):
            original = (root / path).read_bytes()
            put(root, path, original + b'\nstale\n')
            observed = self.observe(module, root, config)
            self.check_status(observed, check, 'FAIL')
            self.assertEqual(observed['overall_status'], 'FAIL')
            put(root, path, original)
        self.check_status(self.observe(module, root, config), 'C-GENERATED', 'PASS')
        self.check_status(self.observe(module, root, config), 'C-TWINS', 'PASS')
