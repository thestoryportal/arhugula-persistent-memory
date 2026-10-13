"""Fresh r13 receipts; -B, isolated HOME, no rclone; synthetic git only."""
import argparse
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label'); parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if not args.label.startswith('r13_') or not args.label.replace('_', '').isalnum():
        raise ValueError('fresh r13_ label required')
    if not sys.flags.dont_write_bytecode: raise ValueError('requires -B')
    out = HERE/args.label; out.mkdir()
    with tempfile.TemporaryDirectory(prefix='r13_sandbox_', dir='/private/tmp') as runtime:
        home = Path(runtime)/'home'; home.mkdir()
        os.environ.update(HOME=str(home), BACKUP_TEST_NO_RCLONE='1', R13_BASELINE='1' if args.baseline else '0', R12_BASELINE='0', GIT_CONFIG_NOSYSTEM='1')
        for name in list(os.environ):
            if name.startswith('GIT_') and name != 'GIT_CONFIG_NOSYSTEM': del os.environ[name]
        (out/'command.json').write_text(json.dumps(dict(argv=sys.argv, HOME=str(home), BACKUP_TEST_NO_RCLONE='1', interpreter=sys.executable, baseline=args.baseline), indent=2)+'\n')
        tests = importlib.import_module('test_r13'); rows = []
        groups = [(tests, name) for name in ('CandidateTest', 'PlanOrderTest', 'BindingReceiptTest')]
        if not args.baseline:
            old = importlib.import_module('test_r12')
            groups += [(old, name) for name in ('ScopeTest', 'PlanTest', 'LogTest')]
        for module, name in groups:
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(getattr(module, name))
            with (out/(name+'.log')).open('w') as stream:
                result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
            row = dict(group=name, testsRun=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped), exit_code=0 if result.wasSuccessful() else 1, failure_tests=[t.id() for t, _ in result.failures])
            rows.append(row); print(json.dumps(row))
        accepted = all(r['errors']==0 and r['skipped']==0 and r['exit_code']==(1 if args.baseline else 0) for r in rows)
        summary = dict(baseline=args.baseline, groups=rows, testsRun=sum(r['testsRun'] for r in rows), failures=sum(r['failures'] for r in rows), errors=sum(r['errors'] for r in rows), skipped=sum(r['skipped'] for r in rows), accepted=accepted, suite_exit_code=1 if any(r['exit_code'] for r in rows) else 0, exit_code=0 if accepted else 1)
        (out/'result.json').write_text(json.dumps(summary, indent=2)+'\n')
        (out/'exit_code.txt').write_text(str(summary['suite_exit_code'])+'\n')
        (out/'driver_exit_code.txt').write_text(str(summary['exit_code'])+'\n')
        print(json.dumps(summary)); return summary['exit_code']

if __name__ == '__main__': raise SystemExit(main())
