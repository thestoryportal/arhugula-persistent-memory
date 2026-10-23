"""T432: the wrapper and switch share one exact stamp protocol."""
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import test_root_switch as fixture_module
from ops.migrate import fdsafe, root_switch


STAMP = '20261023T120000'


class StampTests(unittest.TestCase):
    def fixture(self):
        fixture = fixture_module.RootSwitchTests('test_run_order_and_authoritative_modes')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.config['stamp'] = STAMP
        return fixture

    def test_exact_bytes_for_each_pair(self):
        # [LAW:behavior-not-structure] Supply observations at I/O seams; run the real stage decision.
        correct = STAMP.encode() + b'\n'
        values = (STAMP.encode(), correct, correct + b'\n', STAMP.encode() + b'\r\n',
                  b' ' + correct, b'19991231T235959\n', b'', None)
        c = dict(stamp=STAMP, pairs=[('ssd', '/r', '/d0', '/ex'), ('ssd', '/p', '/d1', '/ex')],
                 m='/m', r='/r', parent_backup='/d1', run='/run', scan_roots=[],
                 registry='/registry', home='/home', reader_commands={}, backup={}, effects={})
        plan = SimpleNamespace(failures=(), batches=[SimpleNamespace(name=name, actions=())
                               for name in ('PAUSE', 'MOVE', 'REPAIR', 'BACKUP', 'RESUME')])
        for index in (0, 1):
            for value in values:
                with self.subTest(pair=index, value=value), ExitStack() as stack:
                    def read(path):
                        data = value if path == f'/d{index}/.last_success' else correct
                        if data is None:
                            raise fdsafe.Refusal(path, 'ENOENT: absent')
                        return data
                    for name, result in (('_observe', (plan, {})), ('_manifest', {}),
                                         ('_create', None), ('_rollback', 1),
                                         ('switch_exec.execute', None),
                                         ('switch_exec.read_journal', SimpleNamespace(records=())),
                                         ('root_readers.main', 0), ('root_reader_checks.main', 0)):
                        stack.enter_context(patch.object(root_switch, name, return_value=result)
                                            if '.' not in name else patch('ops.migrate.root_switch.' + name, return_value=result))
                    stack.enter_context(patch.object(root_switch.switch_effects, '_read', side_effect=read))
                    out = io.StringIO()
                    stack.enter_context(redirect_stdout(out))
                    stack.enter_context(redirect_stderr(out))
                    code = root_switch._run(c, (), lambda *args: None)
                    self.assertEqual(code, 0 if value == correct else 1, out.getvalue())
                    if value != correct:
                        self.assertIn(f'/d{index}/.last_success', out.getvalue())
                        self.assertNotIn(f'/d{1-index}/.last_success', out.getvalue())

    def test_stamp_configuration_sweep(self):
        f = self.fixture()
        invalid = ('', ' ', 'A0261022T010203', '2026102T010203', '20261022T01020', '20261022T0102030',
                   '20261022X010203', '20261022T010203\n', ' 20261022T010203',
                   '20261022T010203 ', '../20261022T010203', '\ud800', '２０２６１０２３T１２００００')
        for value in invalid:
            with self.subTest(stamp=value):
                f.config['stamp'] = value
                f.config_path.write_text(json.dumps(f.config))
                message = ('EINVAL: empty stamp' if value == '' else
                           'EILSEQ: stamp is not UTF-8' if value == '\ud800' else
                           'EINVAL: stamp is not YYYYMMDDTHHMMSS')
                with self.assertRaisesRegex(fdsafe.Refusal, message):
                    root_switch._config(str(f.config_path))
                self.assertEqual(f.snapshot(), f.start)
                self.assertEqual(list(f.run.iterdir()), [])
        for value in ('20261023T104500', '19991231T235959'):
            f.config['stamp'] = value
            f.config_path.write_text(json.dumps(f.config))
            self.assertEqual(root_switch._config(str(f.config_path))['stamp'], value)

    def test_reserved_backup_environment_keys(self):
        f = self.fixture()
        for key in ('BACKUP_STAMP', 'BACKUP_PAIRS'):
            for value in ('', STAMP):
                with self.subTest(key=key, value=value):
                    f.config['backup']['env'] = {key: value}
                    f.config_path.write_text(json.dumps(f.config))
                    with self.assertRaisesRegex(fdsafe.Refusal, 'EINVAL:.*' + key):
                        root_switch._config(str(f.config_path))
                    self.assertEqual(f.snapshot(), f.start)
                    self.assertEqual(list(f.run.iterdir()), [])

    def test_forward_and_resync_observed_environment(self):
        f = self.fixture()
        f.config['stamp'] = '19991231T235959'
        # A conflicting fixture option must never be the fake's stamp source.
        f.options['stamp'] = '20000101T000000'
        f.save_options()
        f.config['backup']['env'] = {'STAMP_CONTROL': 'forward'}
        recorder = '''import json, os, sys
from pathlib import Path
if sys.argv[2] == 'backup':
    with (Path(sys.argv[1]) / 'backup-envs').open('a') as stream:
        stream.write(json.dumps(dict(os.environ)) + '\\n')
'''
        (f.base / 'command.py').write_text(recorder + fixture_module.COMMAND)
        def seam(point, item):
            if (point, item) == ('stage', 'RESUME'):
                for dst in (f.rdest, f.pdest):
                    self.assertEqual((dst / '.last_success').read_bytes(), b'19991231T235959\n')
                self.assertEqual((f.pdest / '.deleted/19991231T235959/obsolete').read_bytes(), b'archive me')
                raise fdsafe.Refusal('RESUME', 'EIO: exercise RESYNC_P')
        before = time.strftime('%Y%m%dT%H%M%S')
        code, text = f.call(seam=seam)
        after = time.strftime('%Y%m%dT%H%M%S')
        f.assert_restored(code, text)
        envs = [json.loads(line) for line in (f.base / 'backup-envs').read_text().splitlines()]
        self.assertEqual(len(envs), 2)
        self.assertEqual(envs[0]['BACKUP_STAMP'], '19991231T235959')
        self.assertEqual(envs[0]['STAMP_CONTROL'], 'forward')
        self.assertEqual(envs[0]['BACKUP_PAIRS'], str(f.table))
        self.assertNotIn('BACKUP_STAMP', envs[1])
        stamp = (f.pdest / '.last_success').read_bytes()
        self.assertRegex(stamp, rb'\A[0-9]{8}T[0-9]{6}\n\Z')
        self.assertTrue(before <= stamp.decode().removesuffix('\n') <= after)
        self.assertNotEqual(stamp, b'20000101T000000\n')
        self.assertNotEqual(stamp, b'19991231T235959\n')
        self.assertTrue((f.pdest / '.deleted' / stamp.decode().removesuffix('\n')).is_dir())


if __name__ == '__main__':
    unittest.main()
