"""Run each r5 step-2 control once, preserving failures and stopping immediately."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(os.environ['LLMDB_ROOT'])
RECEIPT=Path(__file__).resolve().parent
out=RECEIPT/'step2_actual_parent_final'
out.mkdir()
records=[]
for condition in ('unmasked','preblocked'):
    for kind in ('blocked_preflight','blocked_monitor','resource_cleanup'):
        label=condition+'_'+kind
        case=out/(label+'.json')
        argv=[sys.executable,'-B','-W','error::ResourceWarning',str(RECEIPT/'parent_control.py'),kind,condition,str(case)]
        start=time.monotonic()
        process=subprocess.run(argv,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=5)
        log=out/(label+'.log');log.write_bytes(process.stdout+process.stderr)
        value=json.loads(case.read_text()) if case.exists() else None
        record=dict(label=label,command=argv,native_exit=process.returncode,python_return=value['python_return'] if value else None,
            parent_elapsed_s=value['parent_elapsed_s'] if value else None,interpreter_wall_s=time.monotonic()-start,
            return_marker=b'PYTHON_RETURN ' in process.stdout,warnings=b'ResourceWarning:' in process.stderr,
            ignored_exceptions=b'Exception ignored in' in process.stderr,
            log=str(log.relative_to(ROOT)),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
            before_fixture_cleanup=value)
        records.append(record)
        (out/'index.json').write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps({k:record[k] for k in ('label','native_exit','python_return','parent_elapsed_s','return_marker')}),flush=True)
        if process.returncode!=0 or value is None or not record['return_marker'] or record['warnings'] or record['ignored_exceptions']:
            raise SystemExit('saved failing actual-parent control; no retry')
