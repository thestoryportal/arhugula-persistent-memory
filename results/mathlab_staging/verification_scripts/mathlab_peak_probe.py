import json
from pathlib import Path
import resource
import sys
import tempfile
import time

import torch
from mathlab import core

torch.set_num_threads(8)
assert torch.__version__ == '2.8.0'
assert torch.get_default_device().type == 'cpu'
start=time.monotonic()
def record(stage):
    print(json.dumps(dict(tier='MATH-PROXY', fixture=True, stage=stage, elapsed_s=time.monotonic()-start,
                          peak_rss_gib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**30)),flush=True)
kind=sys.argv[1]
record('begin-'+kind)
if kind=='svd':
    cov=torch.zeros(11008,11008,dtype=torch.float32)
    record('input-allocated')
    P,count=core.projector(cov)
    assert P.shape==(11008,11008) and P.device.type=='cpu'
    record('full-projector-finished')
elif kind=='solve':
    P=torch.eye(11008,dtype=torch.float32)
    K=torch.randn(11008,24,dtype=torch.float32)
    r=torch.randn(2048,24,dtype=torch.float32)
    ca=torch.zeros(11008,11008,dtype=torch.float32)
    record('operands-allocated')
    update,diagnostics=core.solve(P,K,r,ca)
    assert update.shape==(2048,11008) and update.device.type=='cpu'
    record('full-solve-and-diagnostics-finished')
elif kind=='load':
    with tempfile.TemporaryDirectory(dir='/private/tmp',prefix='mathlab_peak_') as td:
        data={f'l{l}.upd_precast':torch.ones(2048,11008,dtype=torch.float32) for l in core.BAND}
        path=Path(td)/'synthetic.pt'; torch.save(data,path)
        del data
        record('saved-real-shape-A7-updates')
        loaded=torch.load(path,map_location='cpu',weights_only=True)
        assert all(v.device.type=='cpu' for v in loaded.values())
        record('full-A7-update-load-finished')
else:
    raise ValueError(kind)
