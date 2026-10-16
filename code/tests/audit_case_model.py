"""AuditControls model bulk-locator case; a mixin composed by test_context_audit."""
import os
from unittest.mock import patch

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
        # Registry wire contract: duplicate IDs, bad status and missing fields FAIL.
        second = put(root, 'models/second.gguf', b'second locator fixture\n')
        good = self.entry(root, 'models/second.gguf', 'C-MODEL', 'loader', 'model-second')
        bogus = dict(good, status='BOGUS')
        partial = {key: value for key, value in good.items() if key != 'owner'}
        for entries in ([good, good], [bogus], [partial]):
            self.registry(root, config, entries)
            checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
            self.assertEqual(checked['status'], 'FAIL', checked)
        # An unreadable locator is unobserved, never a false absence.
        self.registry(root, config, [good])
        real_lstat = os.lstat

        def denied(path, *args, **kwargs):
            if str(path) == str(second):
                raise PermissionError(13, 'Permission denied', str(path))
            return real_lstat(path, *args, **kwargs)
        with patch('os.lstat', denied):
            checked = self.check_status(self.observe(module, root, config), 'C-MODEL',
                                        'UNVERIFIED')
        self.assertEqual(checked['status'], 'UNVERIFIED', checked)
        self.assertEqual(checked['findings'], [], checked)
        # A symlink loop is a structured FAIL, not an aborted audit.
        loop = root / 'models/loop.gguf'
        loop.symlink_to('loop.gguf')
        looped = self.entry(root, 'models/loop.gguf', 'C-MODEL', 'loader', 'model-loop')
        looped['source_sha256'] = '0' * 64
        self.registry(root, config, [looped])
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(checked['status'], 'FAIL', checked)
        # A declared external (absolute) locator is checked, not failed for being external.
        external = self.entry(root, str(outside), 'C-MODEL', 'loader', 'model-external')
        self.registry(root, config, [external])
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'PASS')
        self.assertEqual(checked['status'], 'PASS', checked)
        # Distinct readers sharing one absent locator each yield their own finding.
        shared = [self.entry(root, 'models/absent.gguf', 'C-MODEL', 'loader', name)
                  for name in ('model-reader-a', 'model-reader-b')]
        for entry in shared:
            entry['source_sha256'] = '0' * 64
        self.registry(root, config, shared)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(len(checked['findings']), 2, checked)
