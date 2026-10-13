"""Read-only CPU reductions of saved operands; never loads a model or harness."""
from pathlib import Path
import gc, hashlib, json, os, sys, time
audit=Path(os.environ["MINT_DIAG_AUDIT"]).resolve()
root=Path.cwd().resolve()
def guard(event,args):
    if event=="import" and str(args[0]).split(".")[0] in {"transformers","c10e_bandknob","c10u_mint2_arms","memit"}:
        raise RuntimeError("forbidden model/harness import: "+str(args[0]))
    if event=="subprocess.Popen":
        raise RuntimeError("diagnosis may not dispatch subprocesses")
    if event=="open" and isinstance(args[0],(str,bytes)):
        path=Path(os.fsdecode(args[0])).resolve()
        writing=(args[2] or 0)&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
        if writing and path.is_relative_to(root) and not path.is_relative_to(audit):
            raise RuntimeError("write outside diagnosis namespace: "+str(path))
sys.addaudithook(guard)
import torch
torch.set_num_threads(8)
start=time.monotonic()
manifest_path=root/"results/mathlab/harvest_20261009T184950.056951Z/manifest.json"
manifest=json.loads(manifest_path.read_text())
source=json.loads((audit/"record_evidence.json").read_text())
def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(8<<20),b""):h.update(block)
    return h.hexdigest()
inputs={}
def load_file(name):
    ref=manifest["files"][name];path=Path(ref["path"])
    before=path.stat()
    digest=sha(path)
    assert digest==ref["sha256"],name+" differs from completed manifest"
    after=path.stat()
    assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)
    inputs[name]=dict(path=str(path),sha256=digest,bytes=after.st_size)
    data=torch.load(path,map_location="cpu",weights_only=True,mmap=True)
    assert all(isinstance(v,torch.Tensor) and v.device.type=="cpu" for v in data.values())
    return data
A7=load_file("inloop_A7_coined_coined.pt")
weights=load_file("weights_A7.pt")
paired=[]
for layer in range(4,9):
    u=A7[f"l{layer}.upd_precast"]
    assert u.dtype==torch.float32 and tuple(u.shape)==(2048,11008)
    n64=float(torch.linalg.vector_norm(u.double()))
    n32=float(u.float().norm())
    torch.set_num_threads(1)
    n32_one=float(u.float().norm())
    torch.set_num_threads(8)
    recorded64=float(A7[f"l{layer}.upd_norm"])
    expected=source["historical_norms"]["multi"]["candidate"][str(layer)]["delta_norm"]
    assert abs(n64-recorded64)/recorded64<=1e-12
    cast64=float(torch.linalg.vector_norm(u.to(torch.float16).double()))
    realized64=float(torch.linalg.vector_norm(weights[f"l{layer}.after"].double()-weights[f"l{layer}.before"].double()))
    cast_rel=float(torch.linalg.vector_norm(u.double()-u.to(torch.float16).double()))/n64
    record=dict(layer=layer,shape=list(u.shape),stride=list(u.stride()),dtype=str(u.dtype),
                fp32_norm=n32,fp32_norm_one_thread=n32_one,fp64_norm=n64,historical_norm=expected,
                fp64_vs_fp32=(n64-n32)/n32,fp32_vs_history=abs(n32-expected)/expected,
                fp64_vs_history=abs(n64-expected)/expected,
                fp16_cast_norm64=cast64,cast_norm_change=(cast64-n64)/n64,cast_tensor_relative_error=cast_rel,
                realized_delta_norm64=realized64,realized_norm_change=(realized64-n64)/n64)
    paired.append(record)
    print(json.dumps(record),flush=True)
    gc.collect()
small={}
for arm in ("A1_single","A2_coherent2","mint1_s0","mint1_s1","mint1_s2"):
    small[arm]=load_file("inloop_"+arm+".pt")
target_checks={}
for seed in range(3):
    arm="mint1_s"+str(seed); path=root/f"results/c10u_mint2/r3/zs/F_r0_mint1_s{seed}.pt"
    zs=torch.load(path,map_location="cpu",weights_only=True)
    expected_sha=manifest["identity"]["seed_sources"][arm]["target"]["sha256"]
    assert sha(path)==expected_sha
    tensors=small[arm]
    target_checks[arm]=dict(path=str(path),sha256=expected_sha,source_shape=list(zs.shape),source_dtype=str(zs.dtype),
        same_target_every_layer=all(torch.equal(tensors[f"l{l}.zs"],zs.T) for l in range(4,9)),
        layer4_K_equals_A7=torch.equal(tensors["l4.K"],A7["l4.K"]),
        layer4_cur_equals_A7=torch.equal(tensors["l4.cur"],A7["l4.cur"]),
        same_projectors_as_A7=all(torch.equal(tensors[f"l{l}.Pi_sha256"],A7[f"l{l}.Pi_sha256"]) for l in range(4,9)),
        zero_cache_every_layer=all(bool(tensors[f"l{l}.ca_zero"]) and float(tensors[f"l{l}.ca_norm"])==0 for l in range(4,9)),
        precast_updates_retained=any(k.endswith("upd_precast") for k in tensors))
    assert target_checks[arm]["same_target_every_layer"]
    assert not target_checks[arm]["precast_updates_retained"]
arm_inputs={arm:dict(layer4_K_equals_A7=torch.equal(tensors["l4.K"],A7["l4.K"]),
                     layer4_cur_equals_A7=torch.equal(tensors["l4.cur"],A7["l4.cur"]),
                     same_projectors_as_A7=all(torch.equal(tensors[f"l{l}.Pi_sha256"],A7[f"l{l}.Pi_sha256"]) for l in range(4,9)))
            for arm,tensors in small.items()}
result=dict(cpu_only=True,torch_version=torch.__version__,threads=8,priority="unchanged; nice(10) refused by sandbox",elapsed_s=time.monotonic()-start,
            forbidden_imports=[m for m in ("transformers","c10e_bandknob","c10u_mint2_arms","memit") if m in sys.modules],
            manifest_path=str(manifest_path),manifest_sha256=sha(manifest_path),input_artifacts=inputs,
            paired_A7=paired,target_checks=target_checks,arm_inputs=arm_inputs)
assert result["forbidden_imports"]==[]
with (audit/"cpu_reductions.json").open("x") as f:json.dump(result,f,indent=2);f.write("\n")
print(json.dumps(dict(elapsed_s=result["elapsed_s"],target_checks=target_checks,arm_inputs=arm_inputs,forbidden_imports=[])),flush=True)
