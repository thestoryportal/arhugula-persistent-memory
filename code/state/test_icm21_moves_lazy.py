"""Schema reads are deferred, shared by wire checks, and never input refusals."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock
import uuid

import icm21_check
from ops.migrate.fdsafe import Refusal


def fresh_module(path):
    spec = importlib.util.spec_from_file_location("lazy_" + uuid.uuid4().hex, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOVES = Path(__file__).with_name("icm21_moves.py")
CORE = MOVES.parent.parent / "ops/migrate/move_run_core.py"
BINDING = {"path": "/fixture/a", "sha256": "a" * 64}


class LazySchemaTests(unittest.TestCase):
    def check_import(self, core):
        opened = []
        active = True

        def deactivate():
            nonlocal active
            active = False

        def audit(event, args):
            if active and event == "open":
                opened.append(args[0])

        self.addCleanup(deactivate)
        sys.addaudithook(audit)
        module = fresh_module(MOVES)
        if core:
            # [LAW:behavior-not-structure] the core imports the real fresh dependency.
            patch = mock.patch.dict(sys.modules, {"icm21_moves": module})
            patch.start()
            self.addCleanup(patch.stop)
            old_path = sys.path[:]
            self.addCleanup(setattr, sys, "path", old_path)
            imported = fresh_module(CORE)
            self.assertIs(imported.icm21_moves, module)
        self.assertFalse(any("WIRE-SCHEMAS.json" in str(name) for name in opened), opened)
        module.wire_record("Binding", BINDING)
        self.assertTrue(any("WIRE-SCHEMAS.json" in str(name) for name in opened), opened)

    def test_moves_import_defers_schema_open(self):
        self.check_import(False)

    def test_core_import_defers_schema_open(self):
        self.check_import(True)

    def test_two_wire_calls_read_schema_once(self):
        with mock.patch.object(icm21_check, "audit_schema",
                               wraps=icm21_check.audit_schema) as read:
            module = fresh_module(MOVES)
            module.wire_path("/fixture/a")
            module.wire_record("Binding", BINDING)
            self.assertEqual(read.call_count, 1)

    def test_schema_read_error_propagates(self):
        errors = (
            ValueError("x"), OSError("x"), FileNotFoundError("x"),
            PermissionError("x"),
            UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte"),
            RecursionError("x"),
        )
        calls = (("wire_path", ("/fixture/a",)),
                 ("wire_record", ("Binding", BINDING)),
                 ("validate_move", ({}, ())))
        for name, args in calls:
            for error in errors:
                with self.subTest(call=name, error=type(error).__name__):
                    with mock.patch.object(icm21_check, "audit_schema", side_effect=error):
                        module = fresh_module(MOVES)
                        with self.assertRaises(type(error)) as raised:
                            getattr(module, name)(*args)
                        self.assertIs(raised.exception, error)
                        self.assertNotIsInstance(raised.exception, Refusal)


if __name__ == "__main__":
    unittest.main()
