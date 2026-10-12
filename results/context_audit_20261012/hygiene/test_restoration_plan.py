"""Restoration coverage and conservation checks against the actual plan."""
import copy
import json
from pathlib import Path
import unittest
import verify_plan

HERE = Path(__file__).resolve().parent

class RestorationPlanTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((HERE / 'lanes.json').read_text())

    def test_actual_source_coverage(self):
        sources = {u['source'].split(':')[0] for u in self.data['units']}
        self.assertIn('results/context_audit_20261012/PRESERVATION.md', sources)
        self.assertIn('results/context_audit_20261012/operator_hypothesis_worktree_vs_main.md', sources)

    def test_actual_root_and_hook_controls(self):
        units = {u['id']:u for u in self.data['units']}
        for red, green in [('R-ROOT-RED','R-ROOT-GREEN'), ('R-HOOK-RED','R-HOOK-GREEN')]:
            self.assertTrue(red in units, red + " missing from actual plan")
            self.assertTrue(green in units, green + " missing from actual plan")
            self.assertTrue(units[red].get('expected_red'))
            self.assertIn(red, units[green]['depends_on'])

    def test_actual_restoration_verifier(self):
        self.assertTrue(self.data.get('restoration_rows'), 'actual plan has no restoration coverage map')
        verify_plan.verify_restoration(self.data, HERE)

    def test_missing_row_rejected(self):
        if not self.data.get('restoration_rows'):
            self.fail('actual plan has no mapped rows to validate')
        altered = copy.deepcopy(self.data)
        altered['restoration_rows'].pop()
        with self.assertRaises(AssertionError):
            verify_plan.verify_restoration(altered, HERE)

    def test_original_check_mutation_rejected(self):
        if not self.data.get('restoration_rows'):
            self.fail('actual plan lacks baseline conservation contract')
        altered = copy.deepcopy(self.data)
        altered['units'][0]['checks'][0] = 'silently changed original check'
        with self.assertRaises(AssertionError):
            verify_plan.verify_restoration(altered, HERE)

if __name__ == '__main__':
    unittest.main()
