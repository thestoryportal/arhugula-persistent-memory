"""Pointwise CPU check of already saved half-weight updates, no forwards."""
from pathlib import Path
import json, os, sys, time
import torch
torch.set_num_threads(8)
audit=Path(os.environ["MINT_DIAG_AUDIT"])
manifest=json.loads(Path("results/mathlab/harvest_20261009T184950.056951Z/manifest.json").read_text())
u=torch.load(manifest["files"]["inloop_A7_coined_coined.pt"]["path"],map_location="cpu",weights_only=True,mmap=True)
w=torch.load(manifest["files"]["weights_A7.pt"]["path"],map_location="cpu",weights_only=True,mmap=True)
start=time.monotonic(); rows=[]
for layer in range(4,9):
    before=w[f"l{layer}.before"]; after=w[f"l{layer}.after"]; upd=u[f"l{layer}.upd_precast"]
    native=before+upd.to(torch.float16)
    alternate=(before.float()+upd).to(torch.float16)
    row=dict(layer=layer,weight_dtype=str(before.dtype),actual_equals_half_update_then_half_add=torch.equal(after,native),
             actual_matches_fp32_add_then_cast=torch.equal(after,alternate),
             fp32_add_alternate_different_elements=int(torch.count_nonzero(after!=alternate)),total_elements=after.numel())
    assert row["actual_equals_half_update_then_half_add"]
    rows.append(row)
assert not any(m in sys.modules for m in ("transformers","c10e_bandknob","memit"))
result=dict(cpu_only=True,elapsed_s=time.monotonic()-start,layers=rows)
with (audit/"cpu_weight_addition.json").open("x") as out:json.dump(result,out,indent=2);out.write("\n")
print(json.dumps(result))
