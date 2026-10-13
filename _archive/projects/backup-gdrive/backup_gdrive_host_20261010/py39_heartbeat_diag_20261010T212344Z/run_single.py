"""Run only the pinned heartbeat test; collect assertion bytes after evaluation."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parents[2]
RUN = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
pins = json.loads((RECEIPT/'start_sha256.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p, h in pins.items())
assert os.environ['BACKUP_TEST_NO_RCLONE'] == '1'
assert sys.flags.dont_write_bytecode
from tools.test_backup_gdrive_addendum import HeartbeatTest

started = []
original_popen = subprocess.Popen.__init__
def record_popen(self, *args, **kwargs):
    original_popen(self, *args, **kwargs)
    started.append((self, {'pid':self.pid, 'argv':kwargs.get('args', args[0] if args else []),
                           'started_monotonic':time.monotonic()}))
subprocess.Popen.__init__ = record_popen

def save_json(name, value):
    (RUN/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

original_setup = HeartbeatTest.setUp
def setup(self):
    original_setup(self)
    # Fixture.setUp forces sys.executable; override its captured env for arm ii.
    explicit = os.environ.get('MB28_BACKUP_PYTHON')
    if explicit:
        self.env['BACKUP_PYTHON'] = explicit
        os.environ['BACKUP_PYTHON'] = explicit
    save_json('runtime.json', {'pid':os.getpid(), 'runner':sys.executable, 'version':sys.version,
                              'outer_home':os.environ['MB28_OUTER_HOME'], 'fixture_home':str(self.home),
                              'fixture_base':str(self.base), 'backup_python':self.env['BACKUP_PYTHON'],
                              'pythonpath':os.environ.get('PYTHONPATH'),
                              'dont_write_bytecode':sys.flags.dont_write_bytecode,
                              'test':'tools.test_backup_gdrive_addendum.HeartbeatTest.test_held_lock_refusal_cannot_overwrite_owner_heartbeat'})
    def capture_fixture():
        shutil.copytree(self.base, RUN/'fixture_copy')
    self.addCleanup(capture_fixture)
HeartbeatTest.setUp = setup

original_assert = HeartbeatTest.assertEqual
def capture_assert(self, first, second, msg=None):
    if msg == 'a non-owner cannot publish over the active owner':
        assert isinstance(first, bytes) and isinstance(second, bytes)
        (RUN/'heartbeat_before.json').write_bytes(second)
        (RUN/'heartbeat_after.json').write_bytes(first)
        before, after = json.loads(second), json.loads(first)
        changed = {k:{'before':before.get(k),'after':after.get(k)}
                   for k in sorted(set(before)|set(after)) if before.get(k) != after.get(k)}
        path = self.base/'lock/rclone.pid'
        child = int(path.read_text().strip()) if path.exists() else None
        refusals = list((self.heartbeat.parent/'refusals').glob('*.json'))
        save_json('assertion.json', {'same_bytes':first == second, 'changed_fields':changed,
                                    'owner_pid':after.get('owner_pid'), 'rclone_pid':child,
                                    'refusals':[json.loads(p.read_text()) for p in refusals]})
    return original_assert(self, first, second, msg)
HeartbeatTest.assertEqual = capture_assert

suite = unittest.TestSuite([HeartbeatTest('test_held_lock_refusal_cannot_overwrite_owner_heartbeat')])
result = unittest.TextTestRunner(verbosity=2).run(suite)
checks = []
for proc, record in started:
    record['returncode'] = proc.poll()
    try:
        os.kill(proc.pid, 0)
        record['alive'] = True
    except ProcessLookupError:
        record['alive'] = False
    checks.append(record)
assertion_path = RUN/'assertion.json'
if assertion_path.exists():
    child = json.loads(assertion_path.read_text()).get('rclone_pid')
    if child:
        check = {'pid':child, 'role':'fixture sync shell, observed from owned lock/rclone.pid'}
        try:
            os.kill(child, 0)
            check['alive'] = True
        except ProcessLookupError:
            check['alive'] = False
        checks.append(check)
save_json('started_processes.json', checks)
save_json('result.json', {'testsRun':result.testsRun, 'failures':len(result.failures),
                         'errors':len(result.errors), 'skipped':len(result.skipped),
                         'success':result.wasSuccessful(), 'alive':[p for p in checks if p['alive']]})
sys.exit(0 if result.wasSuccessful() and not any(p['alive'] for p in checks) else 1)
