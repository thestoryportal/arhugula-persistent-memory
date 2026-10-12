"""Diagnostic-only signal-state observer of the complete acceptance sequence."""
import json
import os
from pathlib import Path
import signal
import sys
import unittest

ROOT=Path(os.environ['LLMDB_ROOT']);sys.path.insert(0,str(ROOT))
RECEIPT=Path(__file__).resolve().parent
states=[]


class Result(unittest.TextTestResult):
    def snapshot(self,test,phase):
        states.append(dict(test=test.id(),phase=phase,pid=os.getpid(),
            mask=sorted(signal.pthread_sigmask(signal.SIG_BLOCK,[])),
            alarm_handler=repr(signal.getsignal(signal.SIGALRM)),
            alarm_timer=signal.getitimer(signal.ITIMER_REAL)))
        (RECEIPT/'suite_state.json').write_text(json.dumps(states,indent=2)+'\n')
    def startTest(self,test):
        self.snapshot(test,'before');super().startTest(test)
    def stopTest(self,test):
        self.snapshot(test,'after');super().stopTest(test)


suite=unittest.defaultTestLoader.loadTestsFromNames(['tests.test_new1_construction_diag',
    'tests.test_new1_identity_diag','tests.test_new1_geometry','tests.test_new1_supervisor'])
with (RECEIPT/'suite_state.log').open('w') as log:
    result=unittest.TextTestRunner(stream=log,resultclass=Result,verbosity=2).run(suite)
(RECEIPT/'suite_state_result.json').write_text(json.dumps(dict(tests=result.testsRun,
    failures=[name.id() for name,_ in result.failures],errors=[name.id() for name,_ in result.errors]),indent=2)+'\n')
for index,value in enumerate(states):
    if value['mask'] or value['alarm_timer'][0]:
        print(json.dumps(value))
        if index:print('preceding:',json.dumps(states[index-1]))
        break
sys.exit(0 if result.wasSuccessful() else 1)
