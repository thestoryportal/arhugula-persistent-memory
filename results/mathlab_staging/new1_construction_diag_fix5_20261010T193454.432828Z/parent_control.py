"""r5 step 2, actual construction parent; only science/IO boundaries and fixture caps injected."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(os.environ['LLMDB_ROOT'])
sys.path.insert(0, str(ROOT))
from tests.test_new1_identity_diag import _fix5_state, _fix5_owner, _fix5_assert_owned
from tools import new1_construction_diag as D
I = D.I


def run_case(kind, path, *, blocked=False, inherited=False):
    test = unittest.TestCase()
    owners, calls, directories = [], [], []
    NativeOwner, native_supervise, native_directory = I.OwnedWorker, I.supervise, D.new_directory
    class ObservedOwner(NativeOwner):
        def __init__(owner, *args):
            super().__init__(*args); owners.append(owner)
    def directory(root):
        calls.append('directory')
        value = native_directory(root); directories.append(value); return value
    def monitor(pid):
        calls.append('monitor')
        if pid and kind == 'blocked_monitor': time.sleep(2)
        return {'rss_gib':11.1 if pid and kind == 'resource_cleanup' else .01, 'process_count':1}
    def preflight(*args):
        calls.append('preflight')
        if kind == 'blocked_preflight': time.sleep(2)
    def admission():
        calls.append('admission'); return {'allowed':True, 'synthetic':True}
    def supervise(command, directory, **kw):
        calls.append('supervise')
        test.assertIn('--worker', command)
        stub = [sys.executable,'-B','-c',
                'from tools import new1_identity_diag as I; I.wait_for_release(); import time; time.sleep(2)']
        return native_supervise(stub, directory, admission=admission, monitor=monitor, **kw)
    verify_file = D.G.verify_file
    def verify(*args):
        calls.append('source-verification'); return verify_file(*args)
    if inherited:
        test.assertEqual(set(_fix5_state()['mask']), {int(signal.SIGINT),int(signal.SIGALRM)})
    elif blocked:
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT,signal.SIGALRM])
        for sig in (signal.SIGINT, signal.SIGALRM): os.kill(os.getpid(), sig)
    before = _fix5_state()
    source_sha = hashlib.sha256(Path(D.__file__).read_bytes()).hexdigest()
    out, err = io.StringIO(), io.StringIO()
    with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
        root = Path(tmp)
        with mock.patch.object(D,'ROOT',root), mock.patch.object(D,'new_directory',side_effect=directory), \
             mock.patch.object(D.G,'verify_file',side_effect=verify), mock.patch.object(D,'verify_launch',side_effect=preflight), \
             mock.patch.object(I,'OwnedWorker',ObservedOwner), mock.patch.object(I,'supervise',side_effect=supervise), \
             mock.patch.object(I,'DEADLINE_S',.2), mock.patch.object(I.S,'SAMPLE_S',.01), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            start = time.monotonic()
            status = D.main(['--scope-sha','0'*64,'--source-sha',source_sha])
            elapsed = time.monotonic()-start
            after = _fix5_state()
        ownership = [_fix5_owner(o) for o in owners]
        outputs = [str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()]
        result = json.loads((directories[0]/'result.json').read_text()) if directories and (directories[0]/'result.json').exists() else None
        record = dict(kind=kind, blocked=blocked or inherited, inherited=inherited,
            python_return=status, parent_elapsed_s=elapsed, configured_parent_s=.2, required_parent_lt_s=.3,
            before=before, after=after, calls=calls, ownership=ownership, output_files=outputs,
            result=result, stdout=out.getvalue(), stderr=err.getvalue(), observation='after production return, before fixture cleanup',
            loaded_paths={m.__name__:m.__file__ for m in (D,I,I.S)},
            source_sha256={m.__name__:hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in (D,I,I.S)})
        # This receipt is outside the timed parent and follows the state/ownership snapshot.
        with path.open('x') as sink:
            json.dump(record,sink,indent=2);sink.write('\n');sink.flush();os.fsync(sink.fileno())
        print('PYTHON_RETURN '+json.dumps(record,sort_keys=True),flush=True)
        test.assertEqual(status,2)
        test.assertLess(elapsed,.3)
        test.assertEqual(after,before)
        if blocked or inherited:
            test.assertIn('INVALID-ENFORCEMENT',err.getvalue())
            test.assertEqual(calls,[]);test.assertEqual(owners,[])
            test.assertEqual(outputs,[]);test.assertEqual(directories,[])
            test.assertEqual(out.getvalue(),'');test.assertIsNone(result)
        else:
            test.assertIsNotNone(result)
            test.assertIn('STOPPED-RESOURCE' if kind=='resource_cleanup' else 'STOPPED-DEADLINE',result['error'])
            if kind=='blocked_preflight': test.assertEqual(ownership,[])
            else:
                test.assertEqual(len(ownership),1)
                _fix5_assert_owned(test,ownership[0])
    return record


if __name__ == '__main__':
    kind, condition, output = sys.argv[1:]
    run_case(kind,Path(output),blocked=condition=='preblocked')
