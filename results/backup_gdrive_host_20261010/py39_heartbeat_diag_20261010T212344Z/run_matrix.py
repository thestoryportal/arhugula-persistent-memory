"""Forty sequential runs, four interpreter/observer arms, fresh mkdtemp HOME."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
OLD = ROOT/'results/backup_gdrive_host_20261010/py39_run_20261010T210113Z'
PINS = json.loads((OUT/'start_sha256.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in PINS.items())
lib = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
lib.proc_listchildpids.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
lib.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
excluded = {32906,32913,32914,36233,36258,36259,37109,65807}
def children(parent):
    buf = (ctypes.c_int*1024)()
    ctypes.set_errno(0)
    n = lib.proc_listchildpids(parent, buf, ctypes.sizeof(buf))
    if n < 0:
        raise OSError(ctypes.get_errno(), 'proc_listchildpids failed for own PID '+str(parent))
    return [p for p in buf if p > 0 and p not in excluded]
def path_of(pid):
    buf = ctypes.create_string_buffer(4096)
    n = lib.proc_pidpath(pid, buf, len(buf))
    return buf.value.decode(errors='replace') if n > 0 else None
def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False

arms = [('i', str(ROOT/'.venv/bin/python'), None, False),
        ('ii', str(ROOT/'.venv/bin/python'), '/usr/bin/python3', False),
        ('iii', '/usr/bin/python3', '/usr/bin/python3', False),
        ('iv', '/usr/bin/python3', '/usr/bin/python3', True)]
records = []
own_pids = {os.getpid()}
print('matrix controller pid='+str(os.getpid()), flush=True)
for arm, runner, backup_python, observer in arms:
    for iteration in range(1,11):
        run = OUT/('arm_'+arm)/('run_%02d'%iteration)
        run.mkdir(parents=True)
        home = tempfile.mkdtemp(prefix='home_', dir=str(run))
        fixtures = run/'fixtures'
        fixtures.mkdir()
        env = dict(os.environ, HOME=home, MB28_OUTER_HOME=home, LLMDB_ROOT=str(ROOT),
                   BACKUP_TEST_NO_RCLONE='1', PYTHONDONTWRITEBYTECODE='1',
                   BACKUP_TEST_RECEIPTS=str(fixtures))
        for name in ['PYTHONPATH','PY39_TRACE','PY39_TARGET_STATUS','BACKUP_PYTHON','MB28_BACKUP_PYTHON']:
            env.pop(name, None)
        if backup_python:
            env['BACKUP_PYTHON'] = backup_python
            env['MB28_BACKUP_PYTHON'] = backup_python
        if observer:
            env.update(PYTHONPATH=str(OLD/'observer'), PY39_TRACE=str(run/'execution_trace.jsonl'),
                       PY39_TARGET_STATUS=str(ROOT/'tools/backup_gdrive_status.py'))
        command = [runner, '-B', str(OUT/'run_single.py'), str(run)]
        command_record = {'argv':command, 'cwd':str(ROOT),
                          'env':{k:env[k] for k in ['HOME','LLMDB_ROOT','BACKUP_TEST_NO_RCLONE',
                             'PYTHONDONTWRITEBYTECODE','BACKUP_TEST_RECEIPTS','BACKUP_PYTHON',
                             'MB28_BACKUP_PYTHON','PYTHONPATH','PY39_TRACE','PY39_TARGET_STATUS'] if k in env}}
        (run/'command.json').write_text(json.dumps(command_record,indent=2)+'\n')
        observed = {}
        start = time.monotonic()
        with (run/'test.log').open('w') as log:
            proc = subprocess.Popen(command, cwd=str(ROOT), env=env, stdout=log, stderr=subprocess.STDOUT)
            own_pids.add(proc.pid)
            # Positive control: the query must see this newly started runner.
            positive = proc.pid in children(os.getpid())
            while proc.poll() is None:
                queue = [proc.pid]
                while queue:
                    parent = queue.pop()
                    for pid in children(parent):
                        if pid not in observed:
                            observed[pid] = {'pid':pid, 'ppid':parent, 'path':path_of(pid),
                                             'first_seen_monotonic':time.monotonic()}
                            own_pids.add(pid)
                        queue.append(pid)
                time.sleep(.01)
            proc.wait()
        for item in observed.values():
            item['alive_after_runner_exit'] = alive(item['pid'])
        (run/'descendants.json').write_text(json.dumps({'positive_control':positive,
                                                       'runner_pid':proc.pid,
                                                       'observed':list(observed.values())},indent=2)+'\n')
        result = json.loads((run/'result.json').read_text())
        record = {'arm':arm, 'iteration':iteration, 'returncode':proc.returncode,
                  'wall_s':time.monotonic()-start, 'runner_pid':proc.pid,
                  'run':str(run.relative_to(OUT)), **result}
        records.append(record)
        (OUT/'matrix_results.json').write_text(json.dumps(records,indent=2)+'\n')
        print(arm+' %02d '%iteration+('PASS' if result['success'] else 'FAIL')+
              ' failures='+str(result['failures'])+' errors='+str(result['errors'])+
              ' wall_s=%.3f'%record['wall_s'],flush=True)
        if result['errors'] or result['alive'] or any(p['alive_after_runner_exit'] for p in observed.values()):
            raise RuntimeError('Unexpected test error or own process remains; see '+str(run))
(OUT/'matrix_process_pids.json').write_text(json.dumps(sorted(own_pids),indent=2)+'\n')
counts = {arm:{'pass':sum(r['success'] for r in records if r['arm']==arm),
               'fail':sum(not r['success'] for r in records if r['arm']==arm)} for arm,_,_,_ in arms}
(OUT/'four_arm_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,sort_keys=True),flush=True)
