import json
import os
from pathlib import Path
import subprocess
import sys
import time

import psutil
from tools import mathlab_runtime as R

kind=sys.argv[1]
available=R.available_gib()
reserve=2 if kind=='load' else 4
if available<8+reserve:
    print(json.dumps(dict(tier=R.TIER,kind=kind,status='STOPPED-RESOURCE',available_gib=available,required_gib=8+reserve)))
    raise SystemExit(3)
command=[str(R.ROOT/'.venv/bin/python'),'-B','/private/tmp/mathlab_peak_probe.py',kind]
env=dict(os.environ,PYTHONPATH=str(R.ROOT),PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='',LLMDB_DEVICE='cpu',OMP_NUM_THREADS='8',MKL_NUM_THREADS='8')
log=R.ROOT/f'results/mathlab_staging/peak_{kind}.txt'
samples=[]; peak=0.; start=time.monotonic(); stopped=False; timed_out=False
with log.open('w') as out:
    process=subprocess.Popen(command,env=env,cwd=R.ROOT,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
    try:
        while process.poll() is None:
            available=R.available_gib()
            try:
                rss=psutil.Process(process.pid).memory_info().rss/2**30
            except psutil.NoSuchProcess:
                if process.poll() is None: raise
                break
            peak=max(peak,rss); samples.append(dict(elapsed_s=time.monotonic()-start,available_gib=available,rss_gib=rss))
            if available<6 or time.monotonic()-start>=30:
                process.terminate()
                try: process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait()
                stopped=available<6; timed_out=not stopped; break
            time.sleep(1)
        process.wait()
    except BaseException:
        if process.poll() is None:
            process.kill(); process.wait()
        raise
result=dict(tier=R.TIER,fixture=True,kind=kind,command=command,exit_code=process.returncode,
            status='STOPPED-RESOURCE' if stopped else 'UNVERIFIED-TIME-LIMIT' if timed_out else 'PASS' if process.returncode==0 else 'ERROR',
            elapsed_s=time.monotonic()-start,sampled_peak_rss_gib=peak,reserve_gib=reserve,samples=samples,
            scope='Full production matrix shapes; 30 second build-test limit. An interrupted workload is a lower bound, not a measured complete peak.')
(R.ROOT/f'results/mathlab_staging/peak_{kind}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='samples'}))
