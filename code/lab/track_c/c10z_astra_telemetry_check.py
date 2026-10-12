import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Read-only telemetry admission screen. Model imports occur only in main."""
import argparse
import datetime
import hashlib
import importlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
SOURCES = ("code/lab/track_c/c10z_astra_arms.py", "code/lab/track_c/c10z_astra_read.py",
    "code/lab/track_c/c10z_astra_telemetry_check.py", "code/lab/track_c/c10z_astra_benchmark.py",
    "code/lab/track_c/c10e_bandknob.py", "code/configs/hparams/qwen25_3b_memit_hparams.json",
    "code/memit/vendor/memit/memit_main.py")


def _module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module


def arms_module():
    return _module("c10z_astra_arms",ROOT/"code/lab/track_c/c10z_astra_arms.py")


def benchmark_module():
    return _module("c10z_telemetry_benchmark",ROOT/"code/lab/track_c/c10z_astra_benchmark.py")


def fingerprint_module():
    return _module("c10z_telemetry_fingerprint",ROOT/"code/memit/engine_fingerprint.py")


def _prepare(out):
    R=importlib.import_module("c10z_astra_read")
    out=Path(out)
    R.require(out.is_absolute(),"HALTED-V12","telemetry inertness out path must be absolute")
    out=out.resolve();root=(ROOT/"results/c10z_astra_telemetry_inertness").resolve()
    R.require(out.is_relative_to(root) and out.parent==root,
              "HALTED-V12","telemetry inertness out path outside results/c10z_astra_telemetry_inertness")
    R.require(not (out/"inertness.json").exists(),"HALTED-V12","refusing existing inertness.json")
    A=arms_module();A.entry_preflight(os.environ)
    R.require(fingerprint_module().main()==0,"HALTED-V1","engine fingerprint")
    os.environ.update(LLMDB_ROOT=str(ROOT),LLMDB_DEVICE="mps",HF_HOME=str(ROOT/"data/hf_cache"))
    return out,A


def _run(out,H,A,started_at):
    import torch
    R=A.R
    R.require(str(H.DEV)=="mps" and next(H.model.parameters()).dtype==torch.float16,
              "HALTED-V11","actual model device/dtype")
    R.require(H.REV==MODEL_REV,"HALTED-V12","frozen model revision")
    R.require(H.model.config.num_hidden_layers==36,"HALTED-V12","frozen model layer count")
    H.model.config.use_cache=False
    B=benchmark_module()
    population,batch=B.population_and_batch(H,B.TEMPLATES)
    hp=H.MEMITHyperParams.from_json(str(ROOT/A.HP))
    weights={l:H.model.model.layers[l].mlp.down_proj.weight for l in range(36)}
    before={l:A.tensor_hash(w) for l,w in weights.items()}
    evidence=A.telemetry_mps_inertness_check(H.model,H.DEV,population,batch,hp.layers,H.tok)
    after={l:A.tensor_hash(w) for l,w in weights.items()}
    weights_unchanged=before==after
    record={"schema":"c10z_astra_telemetry_inertness/v1","decision_id":"D-C10r-rulings-11",
        "device":"mps",**evidence,"weights_unchanged":weights_unchanged,
        "sources":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
        "env":{**B.environment_identity(),"model_rev":MODEL_REV},"started_at":started_at,
        "finished_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if not weights_unchanged:record["verdict"]="INVALID"
    B.write_record(out/"inertness.json",record)
    return 0 if weights_unchanged else 2


def run(out,H):
    started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    out,A=_prepare(out)
    import torch
    torch.manual_seed(0)
    return _run(out,H,A,started_at)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--out",required=True)
    args=parser.parse_args()
    started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    out,A=_prepare(args.out)
    import torch
    torch.manual_seed(0)
    H=importlib.import_module("c10e_bandknob")
    return _run(out,H,A,started_at)


if __name__=="__main__":
    try:sys.exit(main())
    except ValueError as exc:
        print(str(exc),file=sys.stderr);sys.exit(2)
