#!/usr/bin/env python3
"""Isolated D-C10w-oracle trainer: oracle measurement, not a route.

Only frozen training inputs enter fitting; all heavy imports occur after entry/certificate gates.
One invocation is one fresh 400- or 800-update adapter attempt.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse
import hashlib
import importlib.metadata
import math
import random
import resource
import json
import subprocess
import time
from pathlib import Path
import c10w_oracle_read as R


def training_batches(n,seed,steps):
    R.require(n in (24,480) and seed in (0,1) and steps in (400,800),"invalid frozen training schedule")
    update=0; epoch=0
    while update<steps:
        order=list(range(n)); random.Random(1000*seed+epoch).shuffle(order)
        for offset in range(0,n,24):
            yield order[offset:offset+24]
            update+=1
        epoch+=1


def learning_rate(step):
    return 3e-4*min(step/20.,1.)


def fit_passes(correct,n):
    R.require(n in (24,480),"invalid fit denominator")
    return correct >= (23 if n==24 else 456)


def check_attempt_minutes(minutes):
    R.require(math.isfinite(minutes) and 0<=minutes<=90,"INVALID-BUDGET: training attempt projects above90 minutes")


def project_attempt_minutes(step_seconds,steps,fit_batches,fit_batch_seconds):
    R.require(bool(step_seconds),"missing synchronized training timing")
    return (sum(step_seconds)/len(step_seconds)*steps+fit_batches*fit_batch_seconds)/60.


def require_training_preflight(proof,step0_sha256,provenance):
    R.require(isinstance(proof,dict),"missing passing P1 preflight record")
    R.require(proof.get("status")=="PASS" and all(proof.get(k) is True for k in ("law3","law5_null","fingerprint")),"P1 preflight failed")
    R.require(proof.get("step0_sha256")==step0_sha256 and proof.get("provenance")==provenance,"P1 preflight frozen provenance mismatch")
    R.verify_ref(proof["evaluation"])
    c=proof["law3_counts"]
    R.require(c["A1"]>=68 and c["A2"]>=68 and 5<=c["para_full"]<=18 and 5<=c["canon_full"]<=10 and 42<=c["para_first"]<=59
              and c["u_para_full"]<=2 and len(c["stimulus"])==4 and all(0<=x<=3 for x in c["stimulus"]),"P1 preflight LAW#3 evidence failed")
    g=proof["law5_standing"]
    R.require(g["ok"] is True and abs(g["expr_delta"])<.05 and abs(g["loc_delta"])<3,"P1 preflight standing LAW#5 failed")
    n=proof["null_evidence"]
    R.require(n["base_hash"]==n["after_hash"] and n["u_hit_probe_sha256"]==n["zero_hit_probe_sha256"]
              and abs(n["ppl_delta"])<=.01 and n["described_as"]==100.,"P1 preflight null evidence failed")
    # Raw evaluation remains in a separate stdlib-only verification process; fitting never reads its prompt bytes.
    checked=subprocess.run([str(R.ROOT/".venv/bin/python"),"-B",str(R.ROOT/"experiments/track_c/c10w_oracle_read.py"),"verify-preflight"],
                           input=json.dumps(proof,allow_nan=False),capture_output=True,text=True,timeout=60)
    R.require(checked.returncode==0 and checked.stdout.strip(),"preflight evidence verification failed: "+checked.stderr)
    R.require(json.loads(checked.stdout)=={"ok":True},"invalid preflight verifier result")


def lora_class(torch):
    class LoRA(torch.nn.Module):
        def __init__(self,base,rank):
            super().__init__()
            self.base=base
            self.rank=rank; self.scale=1.0
            self.A=torch.nn.Parameter(torch.empty(rank,base.in_features,device=base.weight.device,dtype=torch.float32))
            self.B=torch.nn.Parameter(torch.zeros(base.out_features,rank,device=base.weight.device,dtype=torch.float32))
            torch.nn.init.kaiming_uniform_(self.A,a=math.sqrt(5))
            for p in base.parameters(): p.requires_grad_(False)

        def forward(self,x):
            return self.base(x)+self.scale*torch.nn.functional.linear(torch.nn.functional.linear(x,self.A),self.B)
    return LoRA


def tensor_sha(tensor):
    return hashlib.sha256(tensor.detach().contiguous().cpu().numpy().tobytes()).hexdigest()


def adapter_tensors(torch,wrappers):
    tensors={}
    for layer,w in wrappers.items():
        tensors["A_"+str(layer)]=w.A.detach().cpu().contiguous()
        tensors["B_"+str(layer)]=w.B.detach().cpu().contiguous()
    tensors["scale"]=torch.tensor(1.,dtype=torch.float32)
    tensors["layers"]=torch.tensor(list(R.BAND),dtype=torch.int64)
    return tensors


def save_adapter(path,tensors,metadata):
    from safetensors.torch import save
    payload=save(tensors,metadata={k:str(v) for k,v in metadata.items()})
    try:
        with Path(path).open("xb") as f: f.write(payload)
    except FileExistsError as exc: raise R.Halt("HALT: adapter exists: "+str(path)) from exc


def load_adapter(path):
    from safetensors.torch import load_file
    return load_file(str(path),device="cpu")


def tokenized_items(inputs,arm,tokenizer):
    templates=inputs["templates"][:1] if arm==R.CANON_ARM else inputs["templates"]
    key=R.A7 if arm==R.CANON_ARM else arm
    values=inputs["value_maps"][key]; items=[]
    for template_id,template in enumerate(templates):
        for fact_id,subject in enumerate(inputs["fiction"]):
            prompt=tokenizer(template.format(subject))["input_ids"]
            target=inputs["target_ids"][key][subject]
            R.require(tokenizer(" "+values[subject],add_special_tokens=False)["input_ids"]==target,"target ids differ from frozen input")
            R.require(prompt==inputs["prompt_ids"][str(template_id)][subject],"prompt ids differ from frozen input")
            items.append({"ids":prompt+target,"labels":[-100]*len(prompt)+target,"template":template_id,"fact":fact_id})
    return items


def padded_batch(torch,items,eos,device):
    length=max(len(x["ids"]) for x in items)
    ids=[x["ids"]+[eos]*(length-len(x["ids"])) for x in items]
    labels=[x["labels"]+[-100]*(length-len(x["labels"])) for x in items]
    masks=[[1]*len(x["ids"])+[0]*(length-len(x["ids"])) for x in items]
    return {"input_ids":torch.tensor(ids,device=device),"labels":torch.tensor(labels,device=device),
            "attention_mask":torch.tensor(masks,device=device)},length


def run_attempt(phase_directory,step0_directory,unit,steps):
    R.entry_preflight()
    phase_directory=Path(phase_directory).resolve(); step0_directory=Path(step0_directory).resolve()
    step=R.load_frozen(step0_directory); provenance=R.frozen_provenance(step)
    proof=R.load_json(phase_directory/"preflight.json")
    require_training_preflight(proof,R.sha_file(step0_directory/"step0.json"),provenance)
    phase=proof["phase"]; arm,seed,rank,retrain=unit
    R.require(unit in R.TRAIN_UNITS[phase] and steps in (400,800),"undeclared adapter attempt")
    tag=R.train_tag(unit,steps); record_path=phase_directory/"train"/(tag+".json")
    R.require(not record_path.exists(),"training record already exists")
    # The process is past all pre-model gates now.
    os.environ["HF_HOME"]=str(R.ROOT/"hf_cache")
    os.environ["HF_HUB_OFFLINE"]="1"
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer
    R.require(torch.backends.mps.is_available(),"INVALID-ENVIRONMENT: MPS required")
    start=time.monotonic(); samples=[]; step_times=[]; losses=[]; lengths=[]
    peak=0
    def sample(label):
        nonlocal peak
        torch.mps.synchronize()
        allocation=int(torch.mps.driver_allocated_memory()); peak=max(peak,allocation)
        samples.append({"stage":label,"driver_bytes":allocation})
        R.check_driver_bytes(allocation)
        check_attempt_minutes((time.monotonic()-start)/60.)
    record={"phase":phase,"arm":arm,"seed":seed,"rank":rank,"retrain":retrain,"steps":steps,
            "provenance":provenance,"step0_sha256":R.sha_file(step0_directory/"step0.json"),
            "fingerprint":step["fingerprint"],"status":"HALT","losses":losses}
    try:
        tok=AutoTokenizer.from_pretrained(R.MODEL_ID,revision=R.MODEL_REV)
        if tok.pad_token is None: tok.pad_token=tok.eos_token
        model=AutoModelForCausalLM.from_pretrained(R.MODEL_ID,revision=R.MODEL_REV,torch_dtype=torch.float16,device_map="mps").float()
        R.require(model.config._commit_hash==R.MODEL_REV and all(p.device.type=="mps" and p.dtype==torch.float32 for p in model.parameters()),"INVALID-ENVIRONMENT: revision/device/dtype")
        model.eval()
        originals={name:p for name,p in model.named_parameters()}
        for p in originals.values(): p.requires_grad_(False)
        before={name:tensor_sha(p) for name,p in originals.items()}
        torch.manual_seed(seed)
        LoRA=lora_class(torch); wrappers={}
        for layer in R.BAND:
            mlp=model.model.layers[layer].mlp
            R.require(tuple(mlp.down_proj.weight.shape)==(2048,11008),"band weight shape mismatch")
            wrappers[layer]=LoRA(mlp.down_proj,rank); mlp.down_proj=wrappers[layer]
        parameters=[p for w in wrappers.values() for p in (w.A,w.B)]
        optimizer=torch.optim.AdamW(parameters,lr=3e-4,betas=(.9,.999),eps=1e-8,weight_decay=0.)
        inputs=R.load_json(step["files"]["train_inputs"]["path"])
        items=tokenized_items(inputs,arm,tok); n=len(items)
        sample("loaded")
        # A complete teacher-forced batch measures the eventual EM readout, with actual padded lengths.
        torch.mps.synchronize(); fit_start=time.monotonic()
        with torch.no_grad():
            batch,_=padded_batch(torch,items[:24],tok.eos_token_id,"mps")
            logits=model(**batch,use_cache=False).logits
            sample("fit-timing-forward")
        del logits,batch
        torch.mps.synchronize(); fit_batch_seconds=time.monotonic()-fit_start
        projection=None
        for update,indices in enumerate(training_batches(n,seed,steps)):
            batch,length=padded_batch(torch,[items[i] for i in indices],tok.eos_token_id,"mps")
            lengths.append(length); optimizer.zero_grad(set_to_none=True)
            for group in optimizer.param_groups: group["lr"]=learning_rate(update)
            torch.mps.synchronize(); tick=time.monotonic()
            output=model(**batch,use_cache=False)
            loss=output.loss
            R.require(math.isfinite(float(loss.detach().cpu())),"NaN/Inf training loss")
            sample("forward")
            loss.backward(); sample("backward")
            norm=torch.nn.utils.clip_grad_norm_(parameters,1.0,error_if_nonfinite=True)
            R.require(math.isfinite(float(norm.detach().cpu())),"NaN/Inf gradient norm")
            optimizer.step(); sample("optimizer")
            torch.mps.synchronize(); elapsed=time.monotonic()-tick
            step_times.append(elapsed)
            if (update+1)%10==0:
                losses.append({"step":update+1,"loss":float(loss.detach().cpu())})
                print(tag,"step",update+1,"loss",losses[-1]["loss"],flush=True)
            del output,loss,batch
            if update>=20:
                projection=project_attempt_minutes(step_times[20:],steps,math.ceil(n/24),fit_batch_seconds)
                # Loading, hashing and timing work also consume the 90-minute wall allowance.
                remaining=(steps-update-1)*sum(step_times[20:])/len(step_times[20:])+math.ceil(n/24)*fit_batch_seconds
                check_attempt_minutes(max(projection,((time.monotonic()-start)+remaining)/60.))
        correct=0; per_template=[0]*(1 if arm==R.CANON_ARM else 20); per_fact=[0]*24
        torch.mps.synchronize(); fit_start=time.monotonic()
        with torch.no_grad():
            for offset in range(0,n,24):
                chosen=items[offset:offset+24]
                batch,_=padded_batch(torch,chosen,tok.eos_token_id,"mps")
                logits=model(**batch,use_cache=False).logits[:,:-1]
                labels=batch["labels"][:,1:]; mask=labels!=-100
                hits=((logits.argmax(-1)==labels)|~mask).all(-1).cpu().tolist()
                sample("final-fit-forward")
                for item,hit in zip(chosen,hits):
                    correct+=hit; per_template[item["template"]]+=hit; per_fact[item["fact"]]+=hit
                del logits,labels,mask,batch
        torch.mps.synchronize(); fit_seconds=time.monotonic()-fit_start
        after={name:tensor_sha(p) for name,p in originals.items()}
        R.require(before==after,"frozen base parameter hash changed")
        adapter_path=phase_directory/"adapters"/(tag+".safetensors")
        save_adapter(adapter_path,adapter_tensors(torch,wrappers),{"rank":rank,"seed":seed,"steps":steps,"class":R.CLASS,"decision_id":R.DECISION_ID})
        sample("saved")
        record.update(status="PASS" if fit_passes(correct,n) else "INVALID-UNDERFIT",fit={"correct":correct,"n":n,"per_template":per_template,"per_fact":per_fact},
                      adapter=R.file_ref(adapter_path),frozen_parameters_unchanged=True,
                      frozen_parameter_hashes_before=before,frozen_parameter_hashes_after=after,
                      model_id=R.MODEL_ID,model_revision=model.config._commit_hash,layers=list(R.BAND),device="mps",dtype="float32",
                      packages={p:importlib.metadata.version(p) for p in ("torch","transformers","safetensors")},
                      training_input_sha256=provenance["train_inputs"],trainer_sha256=R.sha_file(__file__),
                      step_seconds=step_times,padded_sequence_lengths=lengths,fit_seconds=fit_seconds,
                      projected_attempt_minutes=projection,memory_samples=samples,sampled_peak_driver_bytes=peak,
                      cpu_process_peak_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                      wall_seconds=time.monotonic()-start)
        R.write_json(record_path,record)
        return 0 if record["status"]=="PASS" else 75
    except Exception as exc:
        record.update(status="HALT",reason=str(exc),sampled_peak_driver_bytes=peak,wall_seconds=time.monotonic()-start)
        if not record_path.exists(): R.write_json(record_path,record)
        raise


def main():
    parser=argparse.ArgumentParser(description=R.CLASS)
    parser.add_argument("phase_directory"); parser.add_argument("step0_directory")
    parser.add_argument("arm",choices=(R.A1,R.A2,R.A7,R.SHUF,R.CANON_ARM))
    parser.add_argument("seed",type=int,choices=(0,1)); parser.add_argument("rank",type=int,choices=(16,64))
    parser.add_argument("steps",type=int,choices=(400,800)); parser.add_argument("--retrain",action="store_true")
    a=parser.parse_args()
    try: return run_attempt(a.phase_directory,a.step0_directory,(a.arm,a.seed,a.rank,a.retrain),a.steps)
    except Exception as exc:
        print("HALT:",str(exc),file=sys.stderr); return 2


if __name__=="__main__":
    sys.exit(main())
