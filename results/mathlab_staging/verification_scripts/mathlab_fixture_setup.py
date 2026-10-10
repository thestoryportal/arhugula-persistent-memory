from pathlib import Path
import json
from mathlab.fixtures import make_harvest
from tools import mathlab_runtime as R

parent = R.new_directory(R.ROOT / 'results/mathlab_staging', 'fixture')
harvest = make_harvest(parent)
runs = {}
for step, cap in [(2, 2700), (3, 1800)]:
    run = R.Run(parent / f'run{step}', step, 'CPU fixture dry run, no scientific claim', cap)
    run.event('admission', allowed=True, reasons=[])
    R.write_new(run.directory / 'admission.json', dict(tier=R.TIER, allowed=True, kind='cpu', fixture=True))
    runs[str(step)] = str(run.directory)
result = dict(parent=str(parent), harvest=str(harvest), runs=runs)
R.write_new(parent / 'fixture_paths.json', result)
print(json.dumps(result))
