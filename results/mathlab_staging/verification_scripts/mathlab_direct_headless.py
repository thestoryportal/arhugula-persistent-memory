import os
from pathlib import Path
import subprocess
from tools import mathlab_runtime as R

paths=R.read_json(R.ROOT/'results/mathlab_staging/fixture_paths.json')
parent=Path(paths['parent'])
run=R.Run(R.new_directory(parent,'direct_run2'),2,'Direct Python fixture check; frozen uv acceptance remains pending',2700)
run.event('admission', allowed=True, reasons=[])
R.write_new(run.directory/'admission.json',dict(tier=R.TIER,allowed=True,kind='cpu',fixture=True))
env=dict(os.environ, MATHLAB_RUN_DIR=str(run.directory), CUDA_VISIBLE_DEVICES='', LLMDB_DEVICE='cpu',
         OMP_NUM_THREADS='8', MKL_NUM_THREADS='8', PYTHONDONTWRITEBYTECODE='1', MPLCONFIGDIR='/private/tmp/mathlab_mpl',
         PYTHONPATH='/Users/robertrhu/.local/share/uv/tools/marimo/lib/python3.11/site-packages:/Users/robertrhu/.local/share/uv/tools/cc-dump/lib/python3.11/site-packages')
cmd=[str(R.ROOT/'.venv/bin/python'), '-B', str(R.ROOT/'mathlab/m2_solve_repro.py'),
     '--harvest-dir',paths['harvest'],'--output-root',str(parent/'direct_outputs')]
result=subprocess.run(cmd,env=env,cwd=R.ROOT,capture_output=True,text=True,timeout=30)
(R.ROOT/'results/mathlab_staging/m2_direct_headless.txt').write_text(result.stdout+result.stderr)
print('direct_m2_exit',result.returncode)
raise SystemExit(result.returncode)
