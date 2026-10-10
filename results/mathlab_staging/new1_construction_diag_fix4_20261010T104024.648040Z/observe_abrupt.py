"""External observer of the unchanged stalled-launch fixture; actual _exit preserved."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

ROOT = Path(os.environ['LLMDB_ROOT'])
sys.path.insert(0, str(ROOT))
TARGET = 'tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once'


def child(trace):
    from tools import new1_identity_diag as I
    role, owners, errors = 'parent', [], []
    raw_exit, raw_fork, raw_init = os._exit, os.fork, I.OwnedWorker.__init__

    def emit(event, **value):
        data = json.dumps(dict(event=event, pid=os.getpid(), ppid=os.getppid(), role=role,
                               monotonic=time.monotonic(), **value), default=str)+'\n'
        fd = os.open(trace, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try: os.write(fd, data.encode())
        finally: os.close(fd)

    def snapshot(owner):
        fds = []
        for pair in owner.channels.values():
            for fd in pair:
                try:
                    if fd is not None: os.fstat(fd)
                    fds.append({'fd': fd, 'open': fd is not None})
                except OSError as error: fds.append({'fd': fd, 'errno': error.errno})
        return dict(guardian=owner.pid, worker=owner.worker_pid, guardian_code=owner.returncode,
                    proof=owner.proof, fds=fds, streams=list(owner.streams))

    def init(owner, *args):
        raw_init(owner, *args); owners.append(owner)

    def fork():
        nonlocal role
        former = role
        pid = raw_fork()
        if pid == 0: role = 'guardian' if former == 'parent' else 'worker'
        emit('fork', fork_result=pid, former_role=former)
        return pid

    def exiting(code):
        frame = sys._getframe(1)
        stack = []
        while frame is not None:
            value = frame.f_locals
            stack.append(dict(file=frame.f_code.co_filename, function=frame.f_code.co_name,
                              line=frame.f_lineno,
                              exceptions={k:repr(value[k]) for k in ('error','failure','cleanup_error','recording_error') if k in value},
                              remaining_s=value['end']-time.monotonic() if isinstance(value.get('end'), (int,float)) else None))
            frame = frame.f_back
        emit('_exit', code=code, stack=stack, exceptions=errors[-24:],
             ownership=[snapshot(owner) for owner in owners])
        raw_exit(code)

    def tracing(frame, event, arg):
        if frame.f_code.co_filename != I.__file__: return None
        if event == 'exception':
            kind, error, _ = arg
            errors.append(dict(type=kind.__name__, error=str(error), function=frame.f_code.co_name,
                               line=frame.f_lineno, monotonic=time.monotonic()))
        return tracing

    I.OwnedWorker.__init__, os.fork, os._exit = init, fork, exiting
    sys.settrace(tracing)
    emit('unittest-start', target=TARGET)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName(TARGET))
    emit('unittest-complete', tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
         ownership=[snapshot(owner) for owner in owners])
    return 0 if result.wasSuccessful() else 1


def observe(directory):
    runs = []
    before = hashlib.sha256((ROOT/'tools/new1_identity_diag.py').read_bytes()).hexdigest()
    for attempt in range(1, 201):
        trace = directory/f'capture_{attempt:03d}.jsonl'
        command = [sys.executable, '-B', '-W', 'error::ResourceWarning', str(Path(__file__).resolve()), '--child', str(trace)]
        proc = subprocess.run(command, capture_output=True, timeout=8)
        (directory/f'capture_{attempt:03d}.log').write_bytes(proc.stdout+proc.stderr)
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        abrupt = [e for e in events if e['event']=='_exit' and e['role']=='parent']
        runs.append(dict(attempt=attempt, command=command, exit=proc.returncode,
                         unittest_complete=any(e['event']=='unittest-complete' for e in events),
                         abrupt=abrupt, trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest()))
        (directory/'capture_index.json').write_text(json.dumps(dict(source_before=before, runs=runs), indent=2)+'\n')
        print(json.dumps(dict(attempt=attempt, exit=proc.returncode, abrupt=bool(abrupt))), flush=True)
        if abrupt:
            assert before == hashlib.sha256((ROOT/'tools/new1_identity_diag.py').read_bytes()).hexdigest()
            return 0
    return 2


if __name__ == '__main__':
    sys.exit(child(sys.argv[2]) if sys.argv[1]=='--child' else observe(Path(sys.argv[1])))
