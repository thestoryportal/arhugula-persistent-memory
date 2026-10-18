"""Schema I/O begins at first wire validation, once per module instance."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock
import uuid

import icm21_check


def fresh_module():
    spec = importlib.util.spec_from_file_location(
        'icm21_retained_' + uuid.uuid4().hex,
        Path(__file__).with_name('icm21_retained.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LazySchemaTests(unittest.TestCase):
    def test_import_defers_schema_open_until_wire(self):
        opened = []
        active = True

        def deactivate():
            nonlocal active
            active = False

        def audit(event, args):
            if active and event == 'open':
                opened.append(args[0])

        self.addCleanup(deactivate)
        sys.addaudithook(audit)
        module = fresh_module()
        self.assertFalse(any('WIRE-SCHEMAS.json' in str(name) for name in opened), opened)
        module.wire('Binding', {'path': '/fixture/a', 'sha256': 'a' * 64})
        self.assertTrue(any('WIRE-SCHEMAS.json' in str(name) for name in opened), opened)

    def test_two_wire_calls_read_schema_once(self):
        with mock.patch.object(icm21_check, 'audit_schema',
                               wraps=icm21_check.audit_schema) as read:
            module = fresh_module()
            module.wire('Binding', {'path': '/fixture/a', 'sha256': 'a' * 64})
            module.wire('Binding', {'path': '/fixture/b', 'sha256': 'b' * 64})
            self.assertEqual(read.call_count, 1)

    def test_schema_read_error_propagates_from_first_wire(self):
        error = ValueError('x')
        with mock.patch.object(icm21_check, 'audit_schema', side_effect=error):
            module = fresh_module()
            with self.assertRaises(ValueError) as raised:
                module.wire('Binding', {'path': '/fixture/a', 'sha256': 'a' * 64})
            self.assertIs(raised.exception, error)
            self.assertNotIsInstance(raised.exception, module.Refusal)


if __name__ == '__main__':
    unittest.main()
