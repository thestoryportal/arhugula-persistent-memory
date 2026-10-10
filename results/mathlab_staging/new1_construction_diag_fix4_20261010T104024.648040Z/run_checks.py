"""Save every fresh-process test result, its command, counts and source hashes."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

ROOT = Path(os.environ['LLMDB_ROOT'])
RECEIPT = Path(__file__).resolve().parent
SUITES = ['tests.test_new1_construction_diag','tests.test_new1_identity_diag',
          'tests.test_new1_geometry','tests.test_new1_supervisor']
SOLO = 'tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once'
SOURCES = ['tools/new1_identity_diag.py','tools/new1_construction_diag.py','tests/test_new1_construction_diag.py',
           'results/mathlab_staging/new1_construction_diag_scope.md']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['red','green','solo','full'])
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if args.mode in ('red','green'):
        tree = ast.parse((ROOT/'tests/test_new1_construction_diag.py').read_text())
        targets = [[SUITES[0]+'.'+c.name+'.'+f.name] for c in tree.body if isinstance(c,ast.ClassDef)
                   for f in c.body if isinstance(f,ast.FunctionDef) and f.name.startswith('test_fix4_')]
    else: targets = [[SOLO] if args.mode=='solo' else SUITES]*args.count
    target_dir = RECEIPT/args.label
    target_dir.mkdir()
    records = []
    for index, names in enumerate(targets, 1):
        command = [sys.executable,'-B','-W','error::ResourceWarning','-m','unittest',*names,'-v']
        env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONDONTWRITEBYTECODE='1', NEW1_FIX4_RECEIPTS=str(target_dir))
        start=time.monotonic()
        timed_out = False
        try:
            proc = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,timeout=120)
            output, code = proc.stdout+proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as error:
            timed_out = True
            output, code = (error.stdout or b'')+(error.stderr or b''), None
        log=target_dir/f'{index:03d}.log'; log.write_bytes(output)
        match=re.search(rb'Ran (\d+) tests? in ([\d.]+)s', output)
        record = dict(index=index, targets=names, command=shlex.join(command),
                      environment={k:env[k] for k in ('LLMDB_ROOT','PYTHONDONTWRITEBYTECODE','NEW1_FIX4_RECEIPTS')},
                      exit=code, timeout=timed_out, wall_s=time.monotonic()-start,
                      tests=int(match[1]) if match else None, warnings=b'ResourceWarning:' in output,
                      ignored_exception=b'Exception ignored in' in output,
                      completed=bool(match), ok=bool(re.search(rb'\nOK\n?$',output)),
                      log=str(log.relative_to(ROOT)),log_sha256=hashlib.sha256(output).hexdigest(),
                      source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES})
        records.append(record)
        (target_dir/'index.json').write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps({k:record[k] for k in ('index','targets','exit','tests','completed','ok','warnings','wall_s')}),flush=True)
        if args.mode=='red':
            if code==0: raise SystemExit('new test unexpectedly GREEN before production edits')
        elif code!=0 or not record['ok'] or not record['completed'] or record['warnings'] or record['ignored_exception'] or timed_out or record['tests']!=(188 if args.mode=='full' else 1):
            raise SystemExit('saved failure; repetition stopped without selective restart')
    return 0


if __name__=='__main__':sys.exit(main())
