"""AuditControls handoff-context case; a mixin composed by test_context_audit."""

from test_icm21 import encoded, put
from audit_case_guide import context_directive


class HandoffContextCases:
    def test_handoff_context(self):
        module = self.checker()
        root, config = self.seed(['C-HANDOFF'])
        directive = context_directive()
        text = ('# Handoff\n\nDone: fixture\nIn flight: none\n'
                f'Exact paths: {root / "record.md"}\nNext action: verify\n'
                'Open risks: host UNVERIFIED\n\n' + directive)
        path = put(root, 'HANDOFF.md', text)
        self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
        # Budget evidence belongs to the scoped lane handoff, not a global store.
        budget = {'context_left_percent': 60, 'starting_new_work': True,
                  'long_step_pending': False, 'compacted': False}
        put(root, 'context-budget.json', encoded(budget))
        checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'PASS')
        self.assertEqual(checked['status'], 'PASS', checked)
        for label, changed in (
                ('directive', text.replace('60%', '59%', 1)),
                ('done', text.replace('Done: fixture\n', '')),
                ('in-flight', text.replace('In flight: none\n', '')),
                ('paths', text.replace(f'Exact paths: {root / "record.md"}\n', '')),
                ('next', text.replace('Next action: verify\n', '')),
                ('risks', text.replace('Open risks: host UNVERIFIED\n', ''))):
            put(root, 'HANDOFF.md', changed)
            self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
            with self.subTest(mutant=label):
                checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'FAIL')
                self.assertEqual(checked['status'], 'FAIL', checked)
        put(root, 'HANDOFF.md', text)
        self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
        for remaining, long_step, compacted in ((59, False, False), (45, True, False),
                                               (40, False, False), (90, False, True)):
            budget.update(context_left_percent=remaining, long_step_pending=long_step,
                          compacted=compacted)
            put(root, 'context-budget.json', encoded(budget))
            checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'FAIL')
            self.assertEqual(checked['status'], 'FAIL', checked)
        put(root, 'context-budget.json', b'null')
        checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'UNVERIFIED')
        self.assertEqual(checked['status'], 'UNVERIFIED', checked)
