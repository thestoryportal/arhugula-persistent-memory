"""UNRUN: fix5_inherited_mask_launch_01 needs separate explicit operator authorization."""
import os
import signal
import sys
import time
# Capture at interpreter entry, before importing the diagnostic or fixtures.
ENTRY_NS = time.monotonic_ns()
ENTRY_MASK = sorted(map(int, signal.pthread_sigmask(signal.SIG_BLOCK, [])))
ENTRY_PENDING = sorted(map(int, signal.sigpending()))
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(os.environ['LLMDB_ROOT'])
RECEIPT=Path(__file__).resolve().parent
NAME='fix5_inherited_mask_launch_01'


def save(path,value):
    with path.open('x') as sink:
        json.dump(value,sink,indent=2);sink.write('\n');sink.flush();os.fsync(sink.fileno())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--operator-authorized',required=True,choices=[NAME])
    p.add_argument('--phase',choices=['outer','before-exec','entered'],default='outer')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    out=args.output.resolve()
    def argv(phase):
        return [sys.executable,'-B','-W','error::ResourceWarning',str(Path(__file__).resolve()),
                '--operator-authorized',NAME,'--phase',phase,'--output',str(out)]
    if args.phase=='outer':
        # This flag is an execution gate for the future operator; this build grants no authorization.
        frozen=json.loads((RECEIPT/'candidate_frozen.json').read_text())['sha256']
        for path,digest in frozen.items():
            if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
                raise SystemExit('frozen FIX5 candidate mismatch: '+path)
        out.mkdir()
        launched=time.monotonic_ns()
        command=argv('before-exec')
        proc=subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
        (out/'process.log').write_bytes(proc.stdout+proc.stderr)
        marker=out/'parent_return.json'
        result=json.loads(marker.read_text()) if marker.exists() else None
        entry=json.loads((out/'interpreter_entry.json').read_text()) if (out/'interpreter_entry.json').exists() else None
        success=(proc.returncode==2 and result is not None and entry is not None and
                 result['python_return']==2 and result['parent_elapsed_s']<.3 and
                 result['calls']==[] and result['ownership']==[] and result['output_files']==[] and
                 result['before']==result['after'] and 'INVALID-ENFORCEMENT' in result['stderr'] and
                 entry['mask']==entry['before_exec_mask'] and entry['pending']==entry['before_exec_pending'] and
                 b'PYTHON_RETURN ' in proc.stdout and b'ResourceWarning:' not in proc.stderr and
                 b'Exception ignored in' not in proc.stderr)
        save(out/'external_exit.json',dict(name=NAME,command=command,native_exit=proc.returncode,
            python_return=result['python_return'] if result else None,ok=success,
            interpreter_wall_s=(time.monotonic_ns()-launched)/1e9,
            startup_s=entry['startup_s'] if entry else None,
            parent_elapsed_s=result['parent_elapsed_s'] if result else None,
            startup_has_no_qualification_cap=True))
        if not success:raise SystemExit('saved inherited-mask failure; no second attempt')
        return 0
    if args.phase=='before-exec':
        signal.pthread_sigmask(signal.SIG_BLOCK,[signal.SIGINT,signal.SIGALRM])
        for sig in (signal.SIGINT,signal.SIGALRM):os.kill(os.getpid(),sig)
        before=dict(mask=sorted(map(int,signal.pthread_sigmask(signal.SIG_BLOCK,[]))),
                    pending=sorted(map(int,signal.sigpending())),pid=os.getpid())
        save(out/'before_exec.json',before)
        env=dict(os.environ,NEW1_FIX5_EXEC_NS=str(time.monotonic_ns()))
        os.execve(sys.executable,argv('entered'),env)
    # There is no mask mutation or pending-signal consumption in the fresh entered interpreter.
    before=json.loads((out/'before_exec.json').read_text())
    initial=dict(mask=ENTRY_MASK,pending=ENTRY_PENDING,pid=os.getpid(),
                 before_exec_mask=before['mask'],before_exec_pending=before['pending'],
                 startup_s=(ENTRY_NS-int(os.environ['NEW1_FIX5_EXEC_NS']))/1e9)
    if ENTRY_MASK!=before['mask'] or ENTRY_PENDING!=before['pending']:
        save(out/'interpreter_entry.json',initial)
        raise SystemExit('exec inheritance observation mismatched; no parent launched')
    from parent_control import run_case
    result=run_case('blocked_preflight',out/'parent_return.json',inherited=True)
    save(out/'interpreter_entry.json',initial)
    return result['python_return']


if __name__=='__main__':sys.exit(main())
