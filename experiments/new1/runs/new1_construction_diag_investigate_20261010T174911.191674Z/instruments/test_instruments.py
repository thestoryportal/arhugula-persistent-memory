import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import unittest
from unittest import mock

import investigation_io as IO
import scratch_builder as B

HERE = Path(__file__).resolve().parent
RECEIPT = Path(os.environ['NEW1_SELFTEST_DIR'])


class InstrumentTests(unittest.TestCase):
    def test_a_records_roundtrip_exclusive_and_fsync(self):
        path = RECEIPT/'selftest_roundtrip.json'
        value = {'phase':'selftest', 'nested':{'pair':(1,2), 'none':None}, 'text':'alarm\n'}
        native = os.fsync
        with mock.patch.object(os, 'fsync', wraps=native) as sync:
            IO.write_json(path, value)
        self.assertEqual(json.loads(path.read_text()), {'phase':'selftest','nested':{'pair':[1,2],'none':None},'text':'alarm\n'})
        self.assertGreaterEqual(sync.call_count, 2)
        with self.assertRaises(FileExistsError): IO.write_json(path, {'overwritten':True})
        self.assertEqual(json.loads(path.read_text())['phase'], 'selftest')

    def test_b_scratch_retains_bytes_and_import_guard_rejects_escape(self):
        source = RECEIPT/'selftest_source'; source.mkdir()
        (source/'mod.py').write_text('VALUE = 19\n')
        replacement = RECEIPT/'selftest_saved.py'; replacement.write_text('VALUE = 23\n')
        dest = RECEIPT/'selftest_scratch'
        B.build(source, dest, ['mod.py'], {'mod.py':replacement}, link_venv=False)
        self.assertEqual((dest/'mod.py').read_bytes(), replacement.read_bytes())
        self.assertEqual((source/'mod.py').read_text(), 'VALUE = 19\n')
        def load(path):
            spec = importlib.util.spec_from_file_location('mod', path)
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
            return module
        self.assertEqual(B.guard([load(dest/'mod.py')], dest)['mod']['path'], str((dest/'mod.py').resolve()))
        with self.assertRaisesRegex(RuntimeError, 'outside scratch'): B.guard([load(source/'mod.py')], dest)

    def test_c_observer_preserves_alarm_handler_timer_and_native_exits(self):
        for method, expected in [('test_alarm',0), ('test_failure',1), ('test_native_exit',37), ('test_owned_child',0)]:
            outputs = []
            for observed in (False, True):
                label = method+('_observed' if observed else '_control')
                env = dict(os.environ, PYTHONPATH=str(HERE))
                env.pop('NEW1_OBSERVE_DIR', None)
                env['NEW1_OBSERVE_LAUNCHER_PID'] = str(os.getpid())
                if observed: env['NEW1_OBSERVE_DIR'] = str(RECEIPT/label)
                command = [sys.executable,'-B','-W','error::ResourceWarning','-m','unittest',
                           'observer_fixtures.SignalFixture.'+method,'-v']
                p = subprocess.run(command, env=env, capture_output=True, timeout=5)
                IO.write_bytes(RECEIPT/(label+'.log'), p.stdout+p.stderr)
                IO.write_json(RECEIPT/(label+'.json'), {'phase':'selftest','command':command,
                              'observed':observed,'exit':p.returncode,'expected_exit':expected})
                outputs.append(p.returncode)
                self.assertEqual(p.returncode, expected, (p.stdout+p.stderr).decode())
                if observed:
                    events = [json.loads(f.read_text()) for f in sorted((RECEIPT/label).glob('*.json'))]
                    self.assertTrue(events)
                    self.assertTrue(all('phase' in event for event in events))
                    if method == 'test_alarm':
                        self.assertTrue(any(e['event']=='alarm-fired' for e in events))
                        self.assertTrue(any(e['event']=='alarm-armed' for e in events))
                    if method == 'test_failure':
                        failure = next(e for e in events if e['event']=='test-exception')
                        self.assertIn('known failure', failure['traceback_format_exc'])
                    if method == 'test_owned_child':
                        self.assertTrue(any(e['event']=='pid-created' for e in events))
                        self.assertTrue(any(e['event']=='pid-collection' and e['returncode']==23 for e in events))
            self.assertEqual(outputs, [expected,expected])

    def test_d_native_snapshot_is_readonly_and_records_real_threads(self):
        from state_observer import snapshot
        handler = signal.getsignal(signal.SIGALRM)
        mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        value = snapshot()
        IO.write_json(RECEIPT/'selftest_snapshot.json', value)
        self.assertIs(signal.getsignal(signal.SIGALRM), handler)
        self.assertEqual(signal.pthread_sigmask(signal.SIG_BLOCK, []), mask)
        self.assertGreaterEqual(len(value['native_threads']['ids']), 1)
        self.assertTrue(all('run_state' in row for row in value['native_threads']['states']))
        self.assertIn(1, [r['fd'] for r in value['descriptors']['fds']])

    def test_e_profile_gap_is_recorded_and_next_fixture_is_observed(self):
        path=RECEIPT/'profile_recovery'
        env=dict(os.environ,PYTHONPATH=str(HERE),NEW1_OBSERVE_DIR=str(path),NEW1_OBSERVE_LAUNCHER_PID=str(os.getpid()))
        command=[sys.executable,'-B','-W','error::ResourceWarning','-m','unittest',
                 'observer_fixtures.SignalFixture.test_clear_observer_profile','observer_fixtures.SignalFixture.test_alarm','-v']
        p=subprocess.run(command,env=env,capture_output=True,timeout=5)
        IO.write_bytes(RECEIPT/'profile_recovery.log',p.stdout+p.stderr)
        IO.write_json(RECEIPT/'profile_recovery_exit.json',{'phase':'selftest','exit':p.returncode,'expected_exit':0})
        self.assertEqual(p.returncode,0)
        events=[json.loads(f.read_text()) for f in sorted(path.glob('*.json'))]
        self.assertTrue(any(e['event']=='observer-profile-gap' for e in events))
        self.assertTrue(any(e['event']=='alarm-fired' for e in events))
