"""Isolated stdlib receipt runner; baseline RED or fixed GREEN, never real git mutation."""
import argparse
import importlib
import json
import os
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label'); parser.add_argument('--baseline',action='store_true')
    args=parser.parse_args()
    if not args.label.startswith('r12_') or not args.label.replace('_','').isalnum():
        raise ValueError('fresh r12_ label required')
    if not __import__('sys').flags.dont_write_bytecode: raise ValueError('requires -B')
    out=HERE/args.label; out.mkdir()
    with tempfile.TemporaryDirectory(prefix='r12_sandbox_',dir='/private/tmp') as runtime:
        home=Path(runtime)/'home'; home.mkdir()
        os.environ.update(HOME=str(home),BACKUP_TEST_NO_RCLONE='1',R12_BASELINE='1' if args.baseline else '0')
        (out/'command.json').write_text(json.dumps(dict(argv=__import__('sys').argv,HOME=str(home),BACKUP_TEST_NO_RCLONE='1',baseline=args.baseline),indent=2)+'\n')
        tests=importlib.import_module('test_r12'); rows=[]
        for name in ('ScopeTest','PlanTest','LogTest'):
            suite=unittest.defaultTestLoader.loadTestsFromTestCase(getattr(tests,name))
            with (out/(name+'.log')).open('w') as log:
                result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
            code=0 if result.wasSuccessful() else 1
            value=dict(finding={'ScopeTest':1,'PlanTest':2,'LogTest':3}[name],testsRun=result.testsRun,
                       failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),exit_code=code,
                       failure_tests=[t.id() for t,_ in result.failures])
            rows.append(value); print(name,json.dumps(value))
        accepted=all(x['errors']==0 and x['skipped']==0 and x['exit_code']==(1 if args.baseline else 0) for x in rows)
        value=dict(baseline=args.baseline,groups=rows,accepted=accepted,exit_code=0 if accepted else 1)
        (out/'result.json').write_text(json.dumps(value,indent=2)+'\n')
        (out/'exit_code.txt').write_text(str(value['exit_code'])+'\n')
        return value['exit_code']
if __name__=='__main__': raise SystemExit(main())
