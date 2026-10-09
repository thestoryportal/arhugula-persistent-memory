import json, os, subprocess, sys, time
from pathlib import Path
proof = Path(__file__).resolve().parent
name = sys.argv[1]
command = sys.argv[2:]
environment = dict(os.environ, MPLCONFIGDIR=str(proof/'mpl'), PYTHONPYCACHEPREFIX=str(proof/'pycache'), TMPDIR='/private/tmp/labviz-review/test-tmp')
Path(environment['TMPDIR']).mkdir(parents=True,exist_ok=True)
start = time.monotonic()
with (proof/(name+'.log')).open('w') as output:
    result = subprocess.run(command,env=environment,stdout=output,stderr=subprocess.STDOUT)
receipt = dict(command=command,exit_code=result.returncode,elapsed_s=time.monotonic()-start)
(proof/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
print((proof/(name+'.log')).read_text()[-9000:])
raise SystemExit(result.returncode)
