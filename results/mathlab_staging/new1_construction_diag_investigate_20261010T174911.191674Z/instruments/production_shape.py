"""Unmodified construction main and identity supervisor; every science boundary stubbed."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import time
import unittest
from unittest import mock
from investigation_io import write_json
from state_observer import snapshot


class SyntheticParent(unittest.TestCase):
    def run_case(self, kind):
        from tools import new1_construction_diag as D
        I=D.I; owners=[]
        self.root=Path(os.environ['NEW1_CONDITION_DIR'])/kind
        self.root.mkdir()
        directory=self.root/'construction'; directory.mkdir()
        native_supervise=I.supervise
        NativeOwner=I.OwnedWorker
        class ObservedOwner(NativeOwner):
            def __init__(owner,*args,**kwargs):
                super().__init__(*args,**kwargs); owners.append(owner)
        def monitor(pid):
            if pid and kind=='blocked_monitor': time.sleep(2)
            return {'rss_gib':11.1 if pid and kind=='resource_cleanup' else .01,'process_count':1}
        def preflight(*args):
            if kind=='blocked_preflight': time.sleep(2)
        stub=[sys.executable,'-B','-c',
              'from tools import new1_identity_diag as I;I.wait_for_release();import time;time.sleep(2)']
        def production_supervise(command, path, **kwargs):
            self.assertIn('--worker',command)
            return native_supervise(stub,path,admission=lambda:{'allowed':True,'synthetic':True},monitor=monitor,**kwargs)
        start=time.monotonic_ns()
        write_json(self.root/'control_start.json',{'phase':kind,'monotonic_ns':start,'state':snapshot(),
            'thresholds':{'elapsed_lt_s':.3,'supervisor_seconds':.2},'science':'stubbed; no inputs, models or GPU gate',
            'entry':'tools.new1_construction_diag.main -> original tools.new1_identity_diag.supervise',
            'changes':'worker command, preflight, admission, monitor and receipt directory injected at IO boundaries'})
        source_sha=hashlib.sha256(Path(D.__file__).read_bytes()).hexdigest()
        with mock.patch.object(D,'new_directory',return_value=directory),mock.patch.object(D,'verify_launch',side_effect=preflight),\
             mock.patch.object(I,'DEADLINE_S',.2),mock.patch.object(I.S,'SAMPLE_S',.01),\
             mock.patch.object(I,'OwnedWorker',ObservedOwner),mock.patch.object(I,'supervise',side_effect=production_supervise):
            status=D.main(['--scope-sha','0'*64,'--source-sha',source_sha])
        elapsed=(time.monotonic_ns()-start)/1e9
        result=json.loads((directory/'result.json').read_text()) if (directory/'result.json').exists() else None
        owned=[{'guardian_pid':o.pid,'worker_pid':o.worker_pid,'returncode':o.returncode,'proof':o.proof,
                'channels':o.channels,'streams':o.streams} for o in owners]
        path=self.root/'before_assertions.json'
        write_json(path,{'phase':kind,'measured':{'status':status,'elapsed_s':elapsed},
                        'thresholds':{'status':2,'elapsed_lt_s':.3},'state':snapshot(),'result':result,'owned':owned})
        saved=json.loads(path.read_text())
        self.assertEqual(saved['measured']['status'],2)
        self.assertLess(saved['measured']['elapsed_s'],.3)
        self.assertIsNotNone(saved['result'])
        self.assertIn('STOPPED-RESOURCE' if kind=='resource_cleanup' else 'STOPPED-DEADLINE',saved['result']['error'])
        self.assertEqual(set(saved['state']['caller_mask']),{signal.SIGINT,signal.SIGALRM} if os.environ.get('NEW1_EXPECT_BLOCKED_MASK')=='1' else set())
        if kind=='blocked_preflight': self.assertEqual(owned,[])
        else:
            self.assertEqual(len(owned),1)
            owner=owned[0]
            self.assertIsNotNone(owner['returncode'])
            self.assertIsNotNone(owner['proof'])
            self.assertEqual(owner['proof']['pid'],owner['worker_pid'])
            self.assertTrue(all(fd is None for pair in owner['channels'].values() for fd in pair))
            self.assertEqual(owner['streams'],{})
            with self.assertRaises(ProcessLookupError): os.getpgid(owner['worker_pid'])
            with self.assertRaises(ChildProcessError): os.waitpid(owner['guardian_pid'],os.WNOHANG)

    def test_blocked_preflight(self): self.run_case('blocked_preflight')
    def test_blocked_monitor_and_cleanup(self): self.run_case('blocked_monitor')
    def test_resource_breach_and_cleanup(self): self.run_case('resource_cleanup')
