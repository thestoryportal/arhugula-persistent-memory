"""AuditControls model bulk-locator case; a mixin composed by test_context_audit."""
from test_icm21 import put


class ModelLocatorCases:
    def test_model_bulk_locators(self):
        module = self.checker()
        root, config = self.seed(['C-MODEL'])
        payload = put(root, 'models/miniature.gguf', b'locator fixture; never a model\n')
        entries = [self.entry(root, 'models/miniature.gguf', 'C-MODEL', 'loader', 'model-readers')]
        self.registry(root, config, entries)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'PASS')
        self.assertEqual(checked['status'], 'PASS', checked)
        parked = payload.with_suffix('.parked')
        payload.rename(parked)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(checked['status'], 'FAIL', checked)
        outside = put(self.scratch, 'outside.gguf', b'outside\n')
        payload.symlink_to(outside)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(checked['status'], 'FAIL', checked)
        missing = self.entry(root, str(self.scratch / 'unobserved/models'), 'C-MODEL',
                             'loader', 'model-readers')
        missing.update(status='UNVERIFIED', hold_id='H1-EXTERNAL-LOADERS')
        self.registry(root, config, [missing])
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'UNVERIFIED')
        self.assertEqual(checked['status'], 'UNVERIFIED', checked)
