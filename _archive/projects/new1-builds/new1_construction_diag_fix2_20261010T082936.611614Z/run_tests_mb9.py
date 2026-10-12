"""Capture permitted fixture-only verification with exact code/test hashes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
name = sys.argv[1]
paths = ['tools/new1_identity_diag.py', 'tools/new1_construction_diag.py',
         'tests/test_new1_construction_diag.py', 'tests/test_new1_identity_diag.py']
suites = sys.argv[2:] or ['tests.test_new1_construction_diag', 'tests.test_new1_identity_diag',
                         'tests.test_new1_geometry', 'tests.test_new1_supervisor']
command = ['.venv/bin/python', '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', *suites, '-v']
env = dict(os.environ, LLMDB_ROOT=str(Path.cwd()), PYTHONDONTWRITEBYTECODE='1',
           PYTHONPYCACHEPREFIX='/private/tmp/new1-mb9-'+str(time.time_ns()))
hashes = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}
start = time.monotonic()
p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=60)
log = p.stdout+p.stderr
with (here/(name+'.log')).open('x') as f: f.write(log)
with (here/(name+'.json')).open('x') as f:
    json.dump({'command': command, 'env': {k: env[k] for k in ('LLMDB_ROOT', 'PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX')},
               'exit_code': p.returncode, 'elapsed_s': time.monotonic()-start, 'sha256': hashes}, f, indent=2)
    f.write('\n')
print(log)
print(json.dumps({'receipt': name, 'exit_code': p.returncode}))
sys.exit(p.returncode)
