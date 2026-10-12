import json
import os
from pathlib import Path
import subprocess

from tools import mathlab_runtime as R
from mathlab import core

paths = R.read_json(R.ROOT / 'results/mathlab_staging/fixture_paths.json')
parent = Path(paths['parent']); harvest = Path(paths['harvest'])
out2 = R.new_directory(parent, 'prepared_m2')
prepared = R.Run(parent / 'prepared_run2', 2, 'Tiny fixture preparation only', 2700)
core.reproduce(harvest, out2, prepared)
commands = []
for step, cap in [(2, 2700), (3, 1800)]:
    args = ['--harvest-dir', str(harvest), '--output-root', str(parent / 'uv_outputs')]
    if step == 3: args += ['--reproduction-dir', str(out2), '--index-path', str(parent / 'fixture.duckdb')]
    cmd = ['nice', '-n', '10', '/opt/homebrew/bin/timeout', '-k', '30', str(cap),
           'uv', 'run', '--script', str(R.ROOT / f'mathlab/m{step}_' / 'unused')]
    cmd[-1] = str(R.ROOT / ('mathlab/m2_solve_repro.py' if step == 2 else 'mathlab/m3_calibration.py'))
    cmd += args
    env = dict(os.environ, MATHLAB_RUN_DIR=paths['runs'][str(step)], UV_CACHE_DIR='/private/tmp/mathlab_uv_cache',
               UV_PYTHON=str(R.ROOT / '.venv/bin/python'), CUDA_VISIBLE_DEVICES='', LLMDB_DEVICE='cpu',
               OMP_NUM_THREADS='8', MKL_NUM_THREADS='8', PYTHONDONTWRITEBYTECODE='1',
               PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    result = subprocess.run(cmd, env=env, cwd=R.ROOT, capture_output=True, text=True, timeout=60)
    (R.ROOT / f'results/mathlab_staging/m{step}_uv_headless.txt').write_text(result.stdout + result.stderr)
    commands.append(dict(step=step, command=cmd, exit_code=result.returncode, fixture=True))
R.write_new(parent / 'headless_commands.json', commands)
print(json.dumps(dict(prepared_m2=str(out2), commands=commands)))
