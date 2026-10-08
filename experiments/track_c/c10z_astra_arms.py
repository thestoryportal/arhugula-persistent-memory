import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""FROZEN v2.2 ASTRA driver. Import is model-free; only resident stages load H."""
import base64
import gc
import hashlib
import importlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import subprocess
import threading
import time
import uuid
import zlib

import c10z_astra_read as R
from c10z_astra_benchmark import TEMPLATES

ROOT = Path(__file__).resolve().parents[2]
HP = "configs/hparams/qwen25_3b_memit_hparams.json"
PREREG = "docs/C10Z_ASTRA_PREREG.md"
HARNESS = "experiments/track_c/c10e_bandknob.py"
ENGINE = "memit_dry_run/memit/memit"
FRAME_SUBJECTS = ("Vorbanth","Quillexa","Tremnok","Oskavel","Blynthar","Durmquist")
SETTINGS = R.SETTINGS
INHERITED = ("C10_PROJECTOR","N_EDIT","C10_SUBJECT_OFFSET","C10_CTX_TEMPLATES",
             "C10_ARMS","C10_KEY_LOCUS","C10_RECIPES")
# Prospective scheduling allowances, not measured component costs (:194–197).
# The whole 34/23-minute anchors are never divided into per-arm estimates.
ALLOWANCES = {"import_and_pin":120.,"recipe_A":2040.,"reference_D":300.,"G":120.,
    "verification_and_all_probes":1380.,"candidate_rounds":1200.,"serialization_and_restore":180.}


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()


def write_json(path,value,replace=False):
    """Strict JSON, canonical round-trip comparison; create-only unless ongoing attempt state."""
    R.finite_json(value)
    data=json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n"
    canonical=json.loads(data)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not replace:
        R.require(not path.exists(),"HALTED-V12","refusing existing record: "+str(path))
        with path.open("x") as f:f.write(data);f.flush();os.fsync(f.fileno())
    else:
        tmp=path.with_name(path.name+"."+uuid.uuid4().hex+".tmp")
        with tmp.open("x") as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    R.require(json.loads(path.read_text())==canonical,"HALTED-V12","record round-trip changed")


def load_json(path):
    try:
        value=json.loads(Path(path).read_text());R.finite_json(value);return value
    except (OSError,json.JSONDecodeError) as exc:raise R.Halt("HALTED-V12",str(exc)) from exc


def entry_preflight(env):
    R.require(not any(k in env for k in INHERITED),"HALTED-V12","inherited C10 knobs refused")
    for key,expected in (("MODEL_ID","Qwen/Qwen2.5-3B"),
                         ("MODEL_REV","3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")):
        R.require(key not in env or env[key]==expected,"HALTED-V12","inherited "+key)
    R.require("LLMDB_DEVICE" not in env or env["LLMDB_DEVICE"]=="mps","HALTED-V11","MPS is the frozen device")


def memory_guard(rss,driver,float64_on_mps):
    R.require(rss+driver<=40*2**30 and driver<=32*2**30 and not float64_on_mps,
              "HALTED-V11","RSS + driver >40 GiB, driver >32 GiB, or float64 on MPS")


def round_guard(seconds):
    R.require(seconds<=120.,"HALTED-BUDGET","synchronized stage1 round >120 seconds")


class Budget:
    """Clock origins are frozen at pre-import and stage2 entry, never restarted (:196)."""
    def __init__(self,start,stage01,stage2,stage3,process=1,clock=time.monotonic):
        R.require(type(stage01) in (int,float) and 7200<=stage01<=10800 and math.isfinite(stage01),
                  "HALTED-BUDGET","invalid stage01 ceiling")
        for value in (stage2,stage3):
            R.require(value is None or (math.isfinite(value) and value>0),"HALTED-BUDGET","invalid launch ceiling")
        self.clock=clock;self.process=process;self.origins={"stage01":start}
        self.durations={"stage01":stage01,"stage2":stage2,"stage3":stage3}
        self.lock=threading.RLock()
        self.active={"stage01"};self.history=[]
        self.future_stage2_s=7920.
        if process==2:
            R.require(stage3 is not None,"HALTED-BUDGET","absent stage3 ceiling")
            self.origins["stage3"]=start;self.active.add("stage3")

    def deadline(self):
        with self.lock:
            active=tuple(self.active)
            return min(self.origins[k]+self.durations[k] for k in active) if active else None

    def check(self):
        if hasattr(self,"terminal_probe"):
            halt=self.terminal_probe()
            if halt:raise R.Halt(halt["code"],halt["detail"])
        deadline=self.deadline()
        R.require(deadline is None or self.clock()<deadline,"HALTED-BUDGET","elapsed deadline expired")

    def enter(self,stage):
        key="stage"+str(stage)
        R.require(self.durations.get(key) is not None,"HALTED-BUDGET","absent "+key+" ceiling")
        with self.lock:
            now=self.clock()
            if key=="stage2" and "stage01" in self.active:
                R.require(now<self.origins["stage01"]+self.durations["stage01"],"HALTED-BUDGET",
                          "stage 0-1 deadline expired before stage-2 entry")
            if key not in self.origins:self.origins[key]=now
            self.active.add(key)
            if key=="stage2":self.complete01()
        self.check()

    def complete01(self):self.active.discard("stage01")

    def project(self,costs):
        self.check()
        R.require(all(math.isfinite(v) and v>0 for v in costs.values()),"HALTED-BUDGET","unknown required cost cannot be zero")
        now=self.clock();remaining=sum(costs.values())
        pending={k:remaining+(self.future_stage2_s if k=="stage3" and "stage2" not in self.active else 0.) for k in self.active}
        entry={"origins":dict(self.origins),"ceilings":dict(self.durations),"components_s":dict(costs),
               "scopes":{k:{"elapsed_s":now-self.origins[k],"remaining_s":pending[k],
                            "ceiling_s":self.durations[k]} for k in self.active}}
        self.history.append(entry)
        print("C10Z_PROJECTION "+json.dumps(entry,allow_nan=False),flush=True)
        R.require(all(now-self.origins[k]+pending[k]<=self.durations[k] for k in self.active),
                  "HALTED-BUDGET","published elapsed + remaining work exceeds ceiling")
        return entry


class Gates:
    def __init__(self):self.law3=False;self.ready=False
    def baseline(self,recipe):R.law3(recipe);self.law3=True
    def observe(self,action):
        R.require(self.law3,"HALTED-V4","new-writer observation before LAW#3")
        return action()
    def instruments(self,checks):
        R.require(self.law3,"HALTED-V4","instruments before LAW#3")
        R.check_instruments(checks);self.ready=True
    def candidate(self,action):
        R.require(self.law3,"HALTED-V4","candidate before LAW#3")
        R.require(self.ready,"HALTED-V5","candidate before Z0–Z5 and Z7")
        return action()


class StageState:
    def __init__(self,attempt,process):
        self.attempt=attempt;self.process=process;self.completed=-1;self.closed=False
    def run(self,stage,attempt,action):
        R.require(not self.closed and attempt==self.attempt and stage==self.completed+1 and stage<=2,
                  "HALTED-V12","duplicate, out-of-order or stale stage request")
        result=action();self.completed=stage;self.closed=stage==2;return result


def restored(action,restore,verify):
    try:return action()
    finally:restore();verify()


def check_hook_registry(before,after):
    R.require(before==after,"HALTED-V3","capture hook registry leak")


def torch_cpu64(value):
    import torch
    R.require(not (value.device.type=="mps" and value.dtype==torch.float64),"HALTED-V11","float64 tensor reached MPS")
    result=value.detach().cpu().to(torch.float64)
    R.require(bool(torch.isfinite(result).all()),"HALTED-V6","non-finite capture/solve tensor")
    return result


def preferred_directions(G,C,factor=None):
    import torch
    G,C=torch_cpu64(G),torch_cpu64(C)
    try:
        factor=torch.linalg.cholesky(G) if factor is None else torch_cpu64(factor)
        vectors=torch.cholesky_solve(C.T,factor).T
    except RuntimeError as exc:raise R.Halt("HALTED-V8","G factor/solve: "+str(exc)) from exc
    denom=(C*vectors).sum(1)
    R.require(bool((denom>0).all()),"HALTED-V8","nonpositive metric direction")
    return torch_cpu64(vectors/denom[:,None])


def null_weights(m):
    import torch
    m=torch_cpu64(m)
    R.require(bool((m>=0).all()),"HALTED-V7","negative mean squared key")
    ordered=m.sort().values;n=len(ordered)
    med=(ordered[(n-1)//2]+ordered[n//2])/2
    floor=.001*med
    denominator=torch.maximum(m,floor)
    R.require(bool((denominator>0).all()),"HALTED-V7","zero D denominator")
    return torch_cpu64(1/denominator),int((m<floor).sum())


def joint_solve(C,d,scales,keys,D,gamma):
    import torch
    C,d,scales,gamma=map(torch_cpu64,(C,d,scales,gamma))
    keys={l:torch_cpu64(k) for l,k in keys.items()};D={l:torch_cpu64(v) for l,v in D.items()}
    R.require(bool((scales>0).all()),"HALTED-V6","nonpositive norm scale")
    gram=torch.zeros((len(C),len(C)),dtype=torch.float64,device="cpu")
    for l,k in keys.items():gram+=(k*D[l][None,:])@k.T
    A=(C@d.T)*gram/scales[:,None]
    ridged=A+.001*A.diag().mean()*torch.eye(len(C),dtype=torch.float64,device="cpu")
    try:coeff=torch.linalg.solve(ridged,gamma)
    except RuntimeError as exc:raise R.Halt("HALTED-V6","singular joint solve: "+str(exc)) from exc
    patch={l:(d.T@(coeff[:,None]*k))*D[l][None,:] for l,k in keys.items()}
    for value in (A,coeff,*patch.values()):torch_cpu64(value)
    return {"A":A,"lambda":coeff,"patch":patch,"ridged":ridged}


def margin_leads(logits,targets):
    import torch
    logits=logits.detach().cpu().to(torch.float32)
    targets=targets.to(device="cpu")
    R.require(bool(torch.isfinite(logits).all()),"HALTED-V6","non-finite native logits")
    top=logits.topk(2,dim=1).indices
    competitors=torch.where(top[:,0]==targets,top[:,1],top[:,0])
    rows=torch.arange(len(targets),device="cpu")
    return logits[rows,targets]-logits[rows,competitors],competitors


def fixed_leads(obs,competitors):
    import torch
    logits=obs["native_gathered"];rows=torch.arange(len(competitors),device="cpu")
    return logits[rows,obs["targets"]]-logits[rows,competitors]


def last_layer_logits(keys,weight,residual,norm,head):
    return head(norm(residual+__import__("torch").nn.functional.linear(keys,weight)))


def fidelity(predicted,realised):
    import numpy as np
    x=np.asarray(predicted,dtype=np.float64);y=np.asarray(realised,dtype=np.float64)
    if len(x)<2 or np.std(x)==0 or np.std(y)==0:
        return {"status":"NOT-EVALUATED","reason":"constant or insufficient population","n":len(x)}
    return {"status":"MEASURED","n":len(x),"pearson_r":float(np.corrcoef(x,y)[0,1]),
            "slope":float(np.dot(x-x.mean(),y-y.mean())/np.dot(x-x.mean(),x-x.mean()))}


def semcon(C,scales,keys,weights):
    C=C.cpu().to(__import__("torch").float32)
    scales=scales.cpu().float();scores={}
    for l,k in keys.items():
        scores[l]=(k.cpu().float()*(C@weights[l].detach().cpu().float())/scales[:,None]).abs().sum(0)
        torch_cpu64(scores[l])
    return scores


def band_counts(total):
    matched=min(total,2200);q,r=divmod(matched,5)
    return {l:q+int(l-4<r) for l in range(4,9)}


def select_carriers(scores,total_tokens,mode="astra",band_budget=None):
    if mode=="astra":
        layers=sorted(scores,key=lambda l:(-float(scores[l].sum()),l))[:9]
        counts={l:min(440,max(16,math.ceil(16*total_tokens/9))) for l in layers}
    else:
        R.require(band_budget is not None,"HALTED-V12","Z-band needs Z capacity")
        layers=list(range(4,9));counts=band_counts(band_budget)
    return {l:sorted(range(len(scores[l])),key=lambda j:(-float(scores[l][j]),j))[:counts[l]] for l in layers}


def write_columns(weight,columns,delta):
    import torch
    torch_cpu64(delta)
    R.require(weight.dtype==torch.float16,"HALTED-V11","write target must be fp16")
    with torch.no_grad():
        new=(weight[:,columns].float()+delta.cpu().float().to(weight.device)).to(torch.float16)
        R.require(bool(torch.isfinite(new).all()),"HALTED-V6","non-finite deployed column")
        weight[:,columns]=new
    return len(columns)


def zero_column_ratio(original_norm,change_norm):
    return (0. if change_norm==0 else R.INFINITY) if original_norm==0 else change_norm/original_norm


def relative_layer_error(a,b):
    na=math.sqrt(sum(v*v for v in a));nb=math.sqrt(sum(v*v for v in b))
    if na==0 or nb==0:return 0. if na==nb==0 else "ONE-ZERO"
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))/na


def z2_agreement(identity_leads,evaluator,tau):
    return R.z2_evidence(identity_leads,evaluator,tau)


def tensor_bytes(tensor):
    return tensor.detach().cpu().contiguous().view(__import__("torch").uint8).numpy().tobytes()


def tensor_hash(tensor):return hashlib.sha256(tensor_bytes(tensor)).hexdigest()


def source_hashes():
    paths=[ROOT/PREREG,ROOT/HARNESS,ROOT/HP,Path(__file__),Path(R.__file__)]
    paths+=sorted(p for p in (ROOT/ENGINE).rglob("*") if p.is_file())
    paths+=sorted((ROOT/"memit_dry_run/memit/util").rglob("*.py"))
    paths+=sorted((ROOT/"memit_dry_run/memit/rome").rglob("*.py"))
    return {str(p.relative_to(ROOT)):sha256_file(p) for p in paths}


def output_artifact(weights,pristine,carriers):
    """Canonical stored fp16 bytes; these, not intended deltas, bind H_out/R1/W1."""
    pairs=[(l,j) for l in sorted(carriers) for j in sorted(carriers[l])]
    h=hashlib.sha256(json.dumps(pairs,separators=(",", ":")).encode());layers={};ratios=[]
    for l in sorted(carriers):
        cols=sorted(carriers[l]);old=pristine[l][:,cols].cpu();new=weights[l][:,cols].detach().cpu()
        raw=tensor_bytes(new);h.update(raw)
        layers[str(l)]={"columns":cols,"shape":list(new.shape),
             "pristine":base64.b64encode(zlib.compress(tensor_bytes(old))).decode(),"final":base64.b64encode(zlib.compress(raw)).decode()}
        for j in range(len(cols)):
            ratios.append(zero_column_ratio(float(old[:,j].float().norm()),float((new[:,j].float()-old[:,j].float()).norm())))
    return {"encoding":"zlib-base64-fp16-le","H_out":h.hexdigest(),"layers":layers},ratios


def reproduction(p1,p2):
    return R.reproduction_evidence(p1,p2)


# Insert before Session; import-time dependencies remain standard-library only.
import datetime

TELEMETRY_CLOCK = time.perf_counter


def target_probabilities(gathered,targets,chunk_rows):
    import torch
    chunk_rows=min(chunk_rows,max(1,(64*2**20)//(4*gathered.shape[1])))
    targets=targets.detach().cpu().to(torch.long)
    result=torch.empty(gathered.shape[0],dtype=torch.float32,device="cpu")
    with torch.no_grad():
        for start in range(0,gathered.shape[0],chunk_rows):
            x=gathered[start:start+chunk_rows].detach().cpu().to(torch.float32,copy=True)
            x.sub_(x.amax(1,keepdim=True))
            lse=torch.logsumexp(x,1)
            rows=torch.arange(len(x),device="cpu")
            result[start:start+len(x)]=torch.exp(x[rows,targets[start:start+len(x)]]-lse)
            del x,lse,rows
    return result


def logit_lens(model,items,layers,tok,device):
    import torch
    with torch.no_grad():
        if max(layers)>model.config.num_hidden_layers-2:
            raise ValueError("logit lens layer must precede the final normalized hidden state")
        snapshots=[]
        for item in items:
            ids=item["prompt_ids"]
            out=model(torch.tensor([ids],device=device),use_cache=False,
                      output_hidden_states=True,logits_to_keep=1)
            top={}
            for l in layers:
                h=out.hidden_states[l+1][:,-1,:]
                logits=model.lm_head(model.model.norm(h))
                best=logits.float().softmax(-1)[0].topk(5)
                top[str(l)]=[[int(i),tok.decode([int(i)]),float(p)]
                             for i,p in zip(best.indices,best.values)]
            snapshots.append({"view":item["view"],"subject":item["subject"],
                              "prompt_ids":list(ids),"top":top})
        return {"layers":list(layers),"items":snapshots}


class Telemetry:
    def __init__(self,out,process,attempt_id):
        try:
            started=TELEMETRY_CLOCK()
            self.enabled=True;self.file=None;self.cumulative_s=0.
            self.process=process;self.attempt_id=attempt_id
            directory=Path(out)/"telemetry";directory.mkdir(parents=True,exist_ok=True)
            self.file=(directory/f"telemetry_p{process}.jsonl").open("a",encoding="utf-8")
            self._emit("header",started,telemetry=True)
        except Exception as exc:self._disable(exc)

    def _disable(self,exc):
        if getattr(self,"enabled",True):
            self.enabled=False
            print(f"C10Z_TELEMETRY_DISABLED {type(exc).__name__}: {exc}",flush=True)

    def _emit(self,kind,started,**payload):
        line={**payload,"kind":kind,"t_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "process":self.process,"attempt_id":self.attempt_id,"cumulative_s":self.cumulative_s}
        line["elapsed_s"]=TELEMETRY_CLOCK()-started
        data=json.dumps(line,allow_nan=False,sort_keys=True,separators=(",",":"))+"\n"
        self.file.write(data);self.file.flush();os.fsync(self.file.fileno())
        self.cumulative_s+=TELEMETRY_CLOCK()-started

    def phase(self,event,**payload):
        try:
            if not self.enabled:return
            started=TELEMETRY_CLOCK()
            if event=="write_start":
                session=payload.pop("session");requests=payload.pop("requests")
                payload["arm"]=next(k for k,values in session.arms.items() if all(
                    values[r["subject"]]==r["target_new"]["str"].lstrip() for r in requests))
            self._emit("phase",started,event=event,**payload)
        except Exception as exc:self._disable(exc)

    def write_norms(self,patch,cumulative,**payload):
        try:
            if not self.enabled:return
            started=TELEMETRY_CLOCK()
            norms={str(l):{"patch_fro":float(value.detach().cpu().norm()),
                           "cumulative_fro":float(cumulative[l].detach().cpu().norm())}
                   for l,value in patch.items()}
            self._emit("write_norms",started,norms=norms,**payload)
        except Exception as exc:self._disable(exc)

    def target_probs(self,obs,chunk_rows=None,requirements=None,**payload):
        try:
            if not self.enabled:return
            started=TELEMETRY_CLOCK()
            gathered=obs["native_gathered"]
            if chunk_rows is None:chunk_rows=max(1,(64*2**20)//(4*gathered.shape[1]))
            probabilities=target_probabilities(gathered,obs["targets"],chunk_rows)
            self._emit("target_probs",started,rows=[r["row"] for r in requirements],
                facts=[r["fact"] for r in requirements],views=[r["view"] for r in requirements],
                qs=[r["q"] for r in requirements],p=probabilities.tolist(),**payload)
        except Exception as exc:self._disable(exc)

    def logit_lens(self,session,arm,where):
        try:
            if not self.enabled:return
            started=TELEMETRY_CLOCK()
            snapshot=logit_lens(session.H.model,session.population[arm]["F0"],session.hp.layers,
                                session.H.tok,session.H.DEV)
            self._emit("logit_lens",started,arm=arm,where=where,**snapshot)
        except Exception as exc:self._disable(exc)


def telemetry_mps_inertness_check(model,device,population,batch,layers,tok):
    import torch
    probe_forwards=0;lens_forwards=0
    def batch_forward():
        return model(input_ids=torch.tensor(batch["input_ids"],device=device),
                     attention_mask=torch.tensor(batch["attention_mask"],device=device),
                     use_cache=False,logits_to_keep=0)
    def one_pass(lens):
        nonlocal probe_forwards,lens_forwards
        with torch.no_grad():
            if lens:
                logit_lens(model,population["F0"],layers,tok,device)
                lens_forwards+=len(population["F0"])
            tokens={}
            for group,items in population.items():
                tokens[group]=[]
                for item in items:
                    cur=list(item["prompt_ids"]);generated=[]
                    for _ in item["target"] if "target" in item else (None,):
                        logits=model(torch.tensor([cur],device=device),use_cache=False,logits_to_keep=0).logits
                        token=int(logits[0,-1].argmax());generated.append(token);cur.append(token)
                        probe_forwards+=1
                    tokens[group].append(generated)
            if lens:
                logit_lens(model,population["F0"],layers,tok,device)
                lens_forwards+=len(population["F0"])
            native=batch_forward()
            rows=torch.tensor([r["row"] for r in batch["requirements"]],device=device)
            positions=torch.tensor([r["index"] for r in batch["requirements"]],device=device)
            return tokens,native.logits[rows,positions].detach().float().cpu()
    with torch.no_grad():
        first=next(item for items in population.values() for item in items)
        model(torch.tensor([first["prompt_ids"]],device=device),use_cache=False,logits_to_keep=0)
        batch_forward()
        p1=one_pass(False);interleaved=one_pass(True);p2=one_pass(False)
    control_equal=p1[0]==p2[0] and torch.equal(p1[1],p2[1])
    telemetry_equal=p1[0]==interleaved[0] and torch.equal(p1[1],interleaved[1])
    verdict="NONDETERMINISTIC-BASELINE" if not control_equal else "INERT" if telemetry_equal else "NOT-INERT"
    return {"verdict":verdict,"control_equal":control_equal,"telemetry_equal":telemetry_equal,
            "probe_forwards":probe_forwards,"lens_forwards":lens_forwards}


class Session:
    telemetry=None
    context_templates_record=None
    """All methods below are runtime-only; selftests never construct this class."""
    def __init__(self,out,process,budget,input_dir=None):
        self.out=Path(out);self.process=process;self.budget=budget;self.gates=Gates()
        self.recipes={};self.checks={};self.restores=[];self.memory=[];self.timings={};self.snapshots={}
        self.mode=None;self.current={};self.population={};self.pristine_probes={};self.stage=0
        self.unknown_allowances=dict(ALLOWANCES);self.initial_sources=source_hashes()
        R.require(self.initial_sources[PREREG]==R.PREREG_SHA,"HALTED-V12","frozen v2.2 source changed")
        spec=importlib.util.spec_from_file_location("c10z_fingerprint",ROOT/"tools/engine_fingerprint.py")
        fp=importlib.util.module_from_spec(spec);spec.loader.exec_module(fp)
        R.require(fp.main()==0,"HALTED-V1","engine fingerprint")
        self.fingerprint={"sha256":fp.EXPECTED_SHA256,"cov_cpu_sites":3,
             "start":{k:v for k,v in self.initial_sources.items() if k==HARNESS or k.startswith("memit_dry_run/memit/")}}
        self.loaded_manifest=None
        if input_dir is not None:self.validate_inputs(Path(input_dir))
        budget.project(ALLOWANCES if process==1 else {"repeat_stages01":sum(ALLOWANCES.values())})
        self.budget.check()
        os.environ.update(LLMDB_ROOT=str(ROOT),LLMDB_DEVICE="mps",HF_HOME=str(ROOT/"hf_cache"))
        import torch
        torch.manual_seed(0)
        self.H=importlib.import_module("c10e_bandknob")
        H=self.H;self.M=importlib.import_module("memit.memit_main")
        R.require(str(H.DEV)=="mps" and next(H.model.parameters()).dtype==torch.float16,"HALTED-V11","actual model device/dtype")
        H.model.config.use_cache=False
        R.require(H.model.config.num_hidden_layers==36 and H.model.config.hidden_size==2048 and
            H.model.config.intermediate_size==11008 and H.model.config.rms_norm_eps==1e-6,
            "HALTED-V12","frozen model architecture")
        R.require(H.model.lm_head.weight.data_ptr()==H.model.model.embed_tokens.weight.data_ptr(),"HALTED-V12","untied output embedding")
        self.arms=dict(H.ARMS);R.require(set(self.arms)==set(R.ARMS) and len(H.FICTION)==24,"HALTED-V12","arm population")
        self.hp=H.MEMITHyperParams.from_json(str(ROOT/HP))
        self.modules={str(l):H.model.model.layers[l].mlp.down_proj for l in range(36)}
        self.modules["norm"]=H.model.model.norm
        self.weights={l:self.modules[str(l)].weight for l in range(36)}
        self.initial_hooks=self.hook_registry()
        combined=hashlib.sha256();self.parameter_hashes={}
        for name,p in H.model.named_parameters():
            raw=tensor_bytes(p);combined.update(raw);self.parameter_hashes[name]=hashlib.sha256(raw).hexdigest()
            self.budget.check()
        self.pristine={l:w.detach().cpu().clone() for l,w in self.weights.items()}
        self.layer_hashes={str(l):tensor_hash(w) for l,w in self.pristine.items()}
        self.H_pristine=combined.hexdigest()
        snapshot=ROOT/"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots"/H.REV
        safetensors={p.name:sha256_file(p) for p in sorted(snapshot.glob("model*.safetensors"))}
        R.require(bool(safetensors),"HALTED-V12","no pinned safetensors files")
        pin={"H_pristine":self.H_pristine,"parameters":self.parameter_hashes,"layers":self.layer_hashes,"safetensors":safetensors}
        self.safetensors=safetensors
        write_json(self.out/"pristine_hash.json",pin)
        self.original_edit=H.my_edit;self.original_eval=H.eval_arm;self.original_hooks=list(H.ARM_HOOKS)
        self.original_axes=H.axes_post
        H.axes_post=self.axes_guard
        H.eval_arm=self.eval_guard
        if self.loaded_manifest is not None:
            R.require(self.H_pristine==self.loaded_manifest["parts"]["H_pristine"],"HALTED-V3","process2 pristine")
            self.M.CONTEXT_TEMPLATES_CACHE=load_json(input_dir/"context_templates.json")
            self.templates=self.flatten_templates(self.M.CONTEXT_TEMPLATES_CACHE)
            self.batches=self.make_batches()
            self.check_manifest_before_baseline(snapshot)
        self.check_memory();self.verify_restore("import")

    def hook_registry(self):
        return {name:{"forward":dict(m._forward_hooks),"pre":dict(m._forward_pre_hooks)} for name,m in self.H.model.named_modules()}

    def hooks_check(self):check_hook_registry(self.initial_hooks,self.hook_registry())

    def sync(self):
        import torch
        torch.mps.synchronize();self.budget.check()

    def check_memory(self):
        import torch,psutil
        entry={"rss_bytes":psutil.Process().memory_info().rss,"driver_bytes":torch.mps.driver_allocated_memory(),"float64_on_mps":False}
        self.memory.append(entry);memory_guard(entry["rss_bytes"],entry["driver_bytes"],False)
        return entry

    def restore(self):
        import torch
        with torch.no_grad():
            for l,w in self.weights.items():w.copy_(self.pristine[l].to(w.device))

    def verify_restore(self,where):
        self.hooks_check()
        ok=all(tensor_hash(w)==self.layer_hashes[str(l)] for l,w in self.weights.items())
        self.restores.append({"where":where,"ok":ok,"layers":36,"hooks_ok":True})
        R.require(ok,"HALTED-V3","pristine byte mismatch at "+where)

    def guarded(self,action,where):return restored(action,self.restore,lambda:self.verify_restore(where))

    def eval_guard(self,values):
        self.hooks_check();self.budget.check()
        start=time.monotonic();result=self.original_eval(values);self.sync()
        self.timings.setdefault("binding_evaluation",[]).append(time.monotonic()-start)
        return result

    def axes_guard(self,pre,values):
        result=self.original_axes(pre,values)
        if self.gates.law3:
            firsts={self.H.first_tok(value) for value in values}
            result["per_edge_vectors"]={}
            for axis,prompts in (("L1",self.H.L1_PROMPTS),("L3",self.H.L3_PROMPTS)):
                post={p:self.H.predict(p) for p in prompts}
                result["per_edge_vectors"][axis]=[{"prompt":p,"pre_id":pre[axis][p]["id"],"post_id":post[p]["id"],
                    "agree":pre[axis][p]["id"]==post[p]["id"],
                    "flipped_to_edited_value":pre[axis][p]["id"]!=post[p]["id"] and post[p]["id"] in firsts} for p in prompts]
        return result

    @staticmethod
    def flatten_templates(templates):
        flat=[t for group in templates for t in group]
        R.require(len(flat)==6 and flat[0]=="{}","HALTED-V12","frozen six context views")
        return flat

    def make_batch(self,arm,frames):
        H=self.H;values=self.arms[arm];sequences=[];requirements=[];prompts=[];targets=[]
        lengths=[]
        for i,s in enumerate(H.FICTION):
            ids=H.tgt_ids(values[s]);lengths.append(len(ids));targets.append(ids)
            for v,frame in enumerate(frames):
                prompt=frame.format(s);pids=H.tok(prompt)["input_ids"];row=len(sequences)
                sequences.append(pids+ids[:-1]);prompts.append(pids)
                requirements.extend({"row":row,"fact":i,"view":v,"q":q,"index":len(pids)+q-1,"target":y}
                                    for q,y in enumerate(ids))
        pad=max(map(len,sequences));padded=[ids+[H.tok.pad_token_id]*(pad-len(ids)) for ids in sequences]
        masks=[[1]*len(ids)+[0]*(pad-len(ids)) for ids in sequences]
        return {"input_ids":padded,"attention_mask":masks,"T_pad":pad,"pad_token_id":H.tok.pad_token_id,"prompt_ids":prompts,
                "target_ids":targets,"target_lengths":lengths,"requirements":requirements,"frames":frames}

    def make_batches(self):
        return {arm:self.make_batch(arm,[t.format(self.H.CANON) for t in self.templates]) for arm in R.ARMS}

    def observe(self,batch,carriers=None,full=False,trace_layers=None):
        return self.gates.observe(lambda:self._observe(batch,carriers,full,trace_layers))

    def _observe(self,batch,carriers,full,trace_layers):
        import torch
        H=self.H;self.budget.check();self.check_memory();self.hooks_check()
        req=batch["requirements"];rows=torch.tensor([r["row"] for r in req],device=H.DEV)
        positions=torch.tensor([r["index"] for r in req],device=H.DEV)
        R.require(all(batch["attention_mask"][r["row"]][r["index"]]==1 for r in req),"HALTED-V5","padded requirement")
        captures={"keys":{}};handles=[];head_times={};traced=None
        def norm_capture(module,args):
            captures["x"]=args[0][rows,positions].detach().float().cpu()
            if full:captures["full_x"]=args[0].detach().clone()
        handles.append(H.model.model.norm.register_forward_pre_hook(norm_capture))
        layers=range(36) if carriers is None else carriers
        for l in layers:
            def key_capture(module,args,l=l):
                value=args[0][rows,positions]
                if carriers is not None:value=value[:,carriers[l]]
                captures["keys"][l]=value.detach().float().cpu()
            handles.append(self.modules[str(l)].register_forward_pre_hook(key_capture))
        def head_start(module,args):torch.mps.synchronize();head_times["start"]=time.monotonic()
        def head_end(module,args,output):torch.mps.synchronize();head_times["seconds"]=time.monotonic()-head_times["start"]
        handles.append(H.model.lm_head.register_forward_pre_hook(head_start))
        handles.append(H.model.lm_head.register_forward_hook(head_end))
        try:
            if trace_layers:
                from util.nethook import TraceDict
                names=["model.layers."+str(l)+".mlp.down_proj" for l in trace_layers]
                names.append("model.layers.35.post_attention_layernorm")
                traced=TraceDict(H.model,names,retain_input=True,retain_output=False,clone=True,detach=True)
            self.sync();start=time.monotonic()
            with torch.no_grad():
                native=H.model(input_ids=torch.tensor(batch["input_ids"],device=H.DEV),
                    attention_mask=torch.tensor(batch["attention_mask"],device=H.DEV),use_cache=False,logits_to_keep=0)
            selected=native.logits[rows,positions].detach().float().cpu()
            targets=torch.tensor([r["target"] for r in req],device="cpu")
            leads,competitors=margin_leads(selected,targets)
            captures.update(leads=leads,competitors=competitors,targets=targets,
                native_gathered=selected,
                scales=(captures["x"].pow(2).mean(1)+1e-6).sqrt(),
                logits_bytes=native.logits.numel()*native.logits.element_size(),
                conversion_bytes=selected.numel()*selected.element_size(),head_seconds=head_times["seconds"])
            for value in (captures["x"],leads,*captures["keys"].values()):torch_cpu64(value)
            self.check_memory()
            if full:
                with torch.no_grad():
                    reconstructed=H.model.lm_head(H.model.model.norm(captures["full_x"]))
                recon=reconstructed[rows,positions].detach().float().cpu()
                ix=torch.arange(len(req),device="cpu")
                ref_lead=recon[ix,targets]-recon[ix,competitors]
                captures["head_error"]=float((ref_lead-leads).abs().max())
                del reconstructed,recon
            if traced:
                captures["trace"]={l:traced["model.layers."+str(l)+".mlp.down_proj"].input.detach().clone() for l in trace_layers}
                captures["residual35"]=traced["model.layers.35.post_attention_layernorm"].input.detach().clone()
            del native,selected
            self.sync();captures["forward_seconds"]=time.monotonic()-start
            return captures
        finally:
            if traced:traced.close()
            for handle in reversed(handles):handle.remove()
            self.hooks_check()

    def covectors(self,obs):
        W=self.H.model.model.embed_tokens.weight.detach()
        gain=torch_cpu64(self.H.model.model.norm.weight)
        return (torch_cpu64(W[obs["targets"].to(W.device)])-
                torch_cpu64(W[obs["competitors"].to(W.device)]))*gain

    def quantities(self,obs,carriers):
        import torch
        indices=(obs["leads"]<5.).nonzero(as_tuple=True)[0]
        C=self.covectors(obs)[indices];d=preferred_directions(self.G,C,self.cholesky)
        keys={l:obs["keys"][l][indices] if obs.get("selected") else obs["keys"][l][indices][:,cols]
              for l,cols in carriers.items()}
        return indices,C,d,obs["scales"][indices],keys,{l:self.D[l][cols] for l,cols in carriers.items()}

    def choose(self,obs,batch,mode,band_budget=None):
        failing=(obs["leads"]<5.).nonzero(as_tuple=True)[0]
        C=self.covectors(obs)[failing]
        scores=semcon(C,obs["scales"][failing],{l:k[failing] for l,k in obs["keys"].items()},self.weights)
        return select_carriers(scores,sum(batch["target_lengths"]),mode,band_budget)

    def footprint(self,carriers):
        import torch
        changed=[]
        for l,w in self.weights.items():
            differing=(w.detach().cpu()!=self.pristine[l]).any(dim=0).nonzero(as_tuple=True)[0].tolist()
            R.require(set(differing)<=set(carriers.get(l,[])),"HALTED-V5","Z5 changed unselected column")
            changed.extend([l,j] for j in differing)
        for name,p in self.H.model.named_parameters():
            if not (name.startswith("model.layers.") and name.endswith(".mlp.down_proj.weight")):
                R.require(tensor_hash(p)==self.parameter_hashes[name],"HALTED-V5","Z5 changed non-down parameter "+name)
        self.checks.setdefault("Z5",{"ok":True,"writes":[]})["writes"].append({"changed_pairs":changed,
            "selected_pairs":[[l,j] for l,cols in carriers.items() for j in cols],"other_parameters_equal":True,
            "solve_device":"cpu","solve_dtype":"float64"})
        self.check_memory()

    def greedy(self,ids,target):
        import torch
        cur=list(ids);generated=[]
        with torch.no_grad():
            for _ in target:
                self.budget.check()
                logits=self.H.model(torch.tensor([cur],device=self.H.DEV),use_cache=False,logits_to_keep=0).logits
                token=int(logits[0,-1].argmax());generated.append(token);cur.append(token)
        return {"next":generated[0]==target[0],"full":generated==target,"generated":generated}

    def probe_population(self,arm):
        H=self.H;b=self.batches[arm];population={"F0":[],"prefix":[],"subject_free":[],"relations":[]}
        firsts={ids[0] for ids in b["target_ids"]}
        for v,t in enumerate(self.templates):
            for s,subject in enumerate(FRAME_SUBJECTS):
                pids=H.tok(t.format(H.CANON).format(subject))["input_ids"]
                population["F0"].append({"view":v,"subject":s,"prompt_ids":pids,"first_ids":sorted(firsts)})
            for i,target in enumerate(b["target_ids"]):
                for depth in range(1,len(target)):
                    for s,subject in enumerate(FRAME_SUBJECTS):
                        pids=H.tok(t.format(H.CANON).format(subject))["input_ids"]+target[:depth]
                        population["prefix"].append({"view":v,"fact":i,"depth":depth,"subject":s,
                            "prompt_ids":pids,"target":target[depth:]})
        for i,target in enumerate(b["target_ids"]):
            for depth in range(1,len(target)):
                population["subject_free"].append({"fact":i,"depth":depth,
                    "prompt_ids":H.tok("The name is")["input_ids"]+target[:depth],"target":target[depth:]})
            for frame in ("{} is a","{} is associated with"):
                population["relations"].append({"fact":i,"frame":frame,
                    "prompt_ids":H.tok(frame.format(H.FICTION[i]))["input_ids"],"first_ids":sorted(firsts)})
        print("C10Z_PROBE_POPULATION "+json.dumps({"arm":arm,"sha256":R.json_digest(population),
            "counts":{k:len(v) for k,v in population.items()}},allow_nan=False),flush=True)
        return population

    def probe_hits(self,arm):
        import torch
        self.hooks_check();start=time.monotonic();out={}
        for group,items in self.population[arm].items():
            rows=[]
            for item in items:
                if "target" in item:hit=self.greedy(item["prompt_ids"],item["target"])
                else:
                    self.budget.check()
                    with torch.no_grad():
                        token=int(self.H.model(torch.tensor([item["prompt_ids"]],device=self.H.DEV),
                                             use_cache=False,logits_to_keep=0).logits[0,-1].argmax())
                    hit={"top1":token,"edited_value":token in item["first_ids"]}
                rows.append({**item,**hit})
            out[group]=rows
        self.sync();self.timings.setdefault("locality_probes",[]).append(time.monotonic()-start)
        return out

    def attach_probes(self,arm,record,hits,obs=None):
        pre=self.pristine_probes[arm]
        record["target_lengths"]=self.batches[arm]["target_lengths"]
        record["F1_status"]="NOT-APPLICABLE" if all(n==1 for n in record["target_lengths"]) else "MEASURED"
        record["F0"]=[[p["edited_value"] for p in hits["F0"] if p["view"]==v] for v in range(6)]
        record["F0_raw"]={"pristine":pre["F0"],"post":hits["F0"]}
        for source,dest,kinds in (("prefix","prefix_probes",("next","full")),
                                  ("subject_free","subject_free_probes",("full",))):
            rows=[]
            R.require(len(pre[source])==len(hits[source]),"HALTED-V12","probe population mismatch")
            for old,new in zip(pre[source],hits[source]):
                R.require(old["prompt_ids"]==new["prompt_ids"],"HALTED-V12","probe IDs drift")
                row={k:v for k,v in new.items() if k not in ("next","full","generated")}
                row.update({"pristine_"+k:old[k] for k in kinds});row.update({"post_"+k:new[k] for k in kinds})
                row["pristine_generated"]=old["generated"];row["post_generated"]=new["generated"];rows.append(row)
            record[dest]=rows
        record["relation_label_probes"]={"pristine":pre["relations"],"post":hits["relations"],
            "top1_changes":sum(a["top1"]!=b["top1"] for a,b in zip(pre["relations"],hits["relations"])),
            "flips_to_values":sum(a["top1"]!=b["top1"] and b["edited_value"] for a,b in zip(pre["relations"],hits["relations"]))}
        rows=record["rows"]
        record["per_template_n"]=[sum(r["para_full_hits"][j] for r in rows) for j in range(3)]
        record["per_fact_n"]=[sum(r["para_full_hits"]) for r in rows]
        record["per_edge_behavior_pass"]=[all(r["para_full_hits"]) for r in rows]
        if obs is not None:
            by_view=self.lead_rows(self.batches[arm],obs)
            record["post_fit_observation"]=by_view
            record["identity_view_leads"]=by_view[0]
            record["per_fact_min_lead_by_view"]=[[min(row) for row in view] for view in by_view]
            record["fit"]=R.fit_counts(by_view[0],[row for view in by_view for row in view])
            record["phi_mu"]=record["fit"]["m"]/record["fit"]["M"]
            record["phi_0_id"]=record["fit"]["positive_identity_fact_n"]/24

    @staticmethod
    def lead_rows(batch,obs):
        views=[[[] for _ in range(24)] for _ in batch["frames"]]
        for req,lead in zip(batch["requirements"],obs["leads"].tolist()):views[req["view"]][req["fact"]].append(lead)
        return views

    def run_recipe(self,name,arms,mode=None):
        if self.telemetry is not None:self.telemetry.phase("recipe_start",recipe=name,arms=arms)
        self.active_recipe=name
        H=self.H;self.verify_restore("before recipe "+name);H.ARMS={k:self.arms[k] for k in arms}
        self.mode=mode;self.current={};self.calls={"astra_calls":0,"original_calls":0,"Z_OVERRIDE_HITS":0}
        H.my_edit=self.wrapper if mode else self.original_edit
        H.Z_OVERRIDE=None;H.Z_OVERRIDE_HITS=0
        H.ARM_HOOKS=self.original_hooks+[self.arm_hook,self.restore_hook]
        try:
            result=self.guarded(lambda:H.run_recipe(name,str(ROOT/HP)),"after recipe "+name)
        finally:
            H.ARMS=dict(self.arms);H.ARM_HOOKS=self.original_hooks;H.my_edit=self.original_edit;self.mode=None
        R.require(result["law5_gate"]["ok"],"HALTED-V2",name+" standing LAW#5")
        for arm,record in result["arms"].items():
            record["rows"]=result["detail"][arm]
            if self.gates.law3:
                extra=record.pop("extra",{});record.update(extra.get("astra_readouts",{}))
        if mode:result["audit"]={**self.calls,"Z_OVERRIDE_HITS":H.Z_OVERRIDE_HITS}
        self.recipes[name]=result
        if self.telemetry is not None:self.telemetry.phase("recipe_end",recipe=name,arms=arms)
        return result

    def arm_hook(self,arm,values):
        if not self.gates.law3:
            self.snapshots[arm]={l:self.weights[l].detach().cpu().clone() for l in range(4,9)}
            return {}
        obs=self.current["post"];write=self.current["write"]
        self.checks.setdefault("post_write_checks",[]).append({"recipe":self.active_recipe,"arm":arm,"Z1_error":obs["head_error"],
            "Z1_ok":obs["head_error"]<=self.checks["Z7"]["tau_head"],"Z5_ok":True})
        R.require(obs["head_error"]<=self.checks["Z7"]["tau_head"],"HALTED-V5","post-write Z1")
        # eval_arm has already run, but the source hook cannot see its return until run_recipe returns.
        hits=self.probe_hits(arm)
        self.current["hits"]=hits
        if self.telemetry is not None:self.telemetry.logit_lens(self,arm,"post_write")
        held=self.make_batch(arm,list(self.H.PTEST))
        carriers=self.current["carriers"]
        held_obs=self.observe(held,carriers)
        self.current["heldout_post"]=held_obs["leads"].tolist()
        # Stage 0 also reads pristine held-out leads; held-out reads never enter the solve.
        edited={l:self.weights[l].detach().cpu().clone() for l in carriers}
        try:
            self.restore();pre=self.observe(held,carriers)
            transfer=self.transfer_diagnostic(held,pre)
            realised=fixed_leads(held_obs,pre["competitors"])-pre["leads"]
            transfer["realised_delta_lead"]=realised.tolist()
            if "predicted_delta_lead" in transfer:transfer["fidelity"]=fidelity(transfer["predicted_delta_lead"],realised.tolist())
        finally:
            import torch
            with torch.no_grad():
                for l,w in edited.items():self.weights[l].copy_(w.to(self.weights[l].device))
        self.footprint(carriers);self.sync()
        write["wall_seconds"]=time.monotonic()-self.current["start"]
        return {"astra_readouts":{"write":write,"heldout_position_leads":{"pre":pre["leads"].tolist(),
            "post":held_obs["leads"].tolist(),"requirements":held["requirements"]},
            "predicted_transfer":transfer,"probe_hits":hits,"post_fit_observation":self.lead_rows(self.batches[arm],obs)}}

    def restore_hook(self,arm,values):
        self.restore();self.verify_restore("restore_hook "+arm)
        if self.mode is not None and "write" in self.current:
            self.current["write"]["wall_seconds"]=time.monotonic()-self.current["start"]
        return {}

    def wrapper(self,hp,requests,P,cache):
        if self.mode is None or self.H._LAW5_DEFAULT_CTX:
            if not self.H._LAW5_DEFAULT_CTX:self.calls["original_calls"]+=1
            return self.original_edit(hp,requests,P,cache)
        self.calls["astra_calls"]+=1
        return self.gates.candidate(lambda:self.write_arm(requests,self.mode))

    def write_arm(self,requests,mode):
        if self.telemetry is not None:self.telemetry.phase("write_start",session=self,requests=requests,mode=mode)
        self.sync();start=time.monotonic()
        arm=next(k for k,values in self.arms.items() if all(values[r["subject"]]==r["target_new"]["str"].lstrip() for r in requests))
        self.restore();self.verify_restore("before write "+arm)
        self.budget.project({"candidate_rounds":1200.,"checks_probes_eval":self.remaining_validation(),"serialization_restore":180.})
        batch=self.batches[arm]
        obs=self.observe(batch);carriers=self.choose(obs,batch,mode,getattr(self,"Z_capacity",None))
        traces=[];summed={};round_times=[];first=None;solve_seconds=0.;round1_fidelity=None
        for round_no in range(10):
            self.budget.project({"candidate_rounds":max(1.,(10-round_no)*max(round_times or [120.])),
                                 "checks_probes_eval":self.remaining_validation(),"serialization_restore":180.})
            self.sync();rstart=start if round_no==0 else time.monotonic()
            indices,C,d,scales,keys,D=self.quantities(obs,carriers)
            if len(indices)==0:break
            sstart=time.monotonic();sol=joint_solve(C,d,scales,keys,D,5.-obs["leads"][indices]);solve_seconds+=time.monotonic()-sstart
            if first is None:
                first={"carriers":carriers,"patch":{l:w.clone() for l,w in sol["patch"].items()},
                       "requirements":[batch["requirements"][i] for i in indices.tolist()],"C":C,"scales":scales}
            written=sum(write_columns(self.weights[l],cols,sol["patch"][l]) for l,cols in carriers.items())
            for l,delta in sol["patch"].items():summed[l]=summed.get(l,0)+delta
            self.footprint(carriers);post=self.observe(batch,carriers,full=True);post["selected"]=True
            R.require(post["head_error"]<=self.checks["Z7"]["tau_head"],"HALTED-V5","post-write Z1 fixed head tolerance")
            if round_no==0:
                C_all=self.covectors(obs);v=__import__("torch").zeros_like(C_all)
                for l,delta in sol["patch"].items():v+=torch_cpu64(obs["keys"][l][:,carriers[l]])@delta.T
                predicted=(C_all*v).sum(1)/torch_cpu64(obs["scales"])
                realised=fixed_leads(post,obs["competitors"])-obs["leads"]
                round1_fidelity={"predicted":predicted.tolist(),"realised":realised.tolist(),
                    **fidelity(predicted.tolist(),realised.tolist())}
            self.sync();elapsed=time.monotonic()-rstart;round_times.append(elapsed)
            traces.append({"F":len(indices),"sum_gamma":float((5.-obs["leads"][indices]).sum()),"columns_written":written,
                "condition":float(__import__("torch").linalg.cond(sol["ridged"])),
                "lambda_min":float(sol["lambda"].min()),"lambda_max":float(sol["lambda"].max()),"seconds":elapsed,
                "T_pad":batch["T_pad"],"head_seconds":post["head_seconds"],"logits_bytes":post["logits_bytes"],
                "conversion_bytes":post["conversion_bytes"]})
            if self.stage==1:round_guard(elapsed)
            if self.telemetry is not None:
                self.telemetry.phase("round_end",round_no=round_no,arm=arm,recipe=self.active_recipe,seconds=elapsed,F=len(indices),columns_written=written)
                self.telemetry.write_norms(sol["patch"],summed,round_no=round_no,arm=arm)
                self.telemetry.target_probs(post,requirements=batch["requirements"],round_no=round_no,arm=arm)
            obs=post
            if bool((obs["leads"]>=5.).all()):break
        post=self.observe(batch,carriers,full=True);post["selected"]=True
        if self.telemetry is not None:self.telemetry.target_probs(post,requirements=batch["requirements"],round_no="final",arm=arm)
        artifact,ratios=output_artifact(self.weights,self.pristine,carriers)
        write={"stage":self.stage,"rounds_used":len(traces),"stop_reason":"objective met" if bool((post["leads"]>=5.).all()) else "round cap",
            "carriers":{str(l):cols for l,cols in carriers.items()},"carrier_count":sum(map(len,carriers.values())),
            "H_out":artifact["H_out"],"artifact":artifact,"relative_changes":ratios,
            "round_seconds":round_times,"trace":traces,"solve_seconds":solve_seconds,
            "wall_seconds":time.monotonic()-start,"outside_L17_L28":sum(len(cols) for l,cols in carriers.items() if not 17<=l<=28),
            "neuron_share":sum(map(len,carriers.values()))/396288,"D_floored_count":self.D_floored,
            "W1":ratio_summary(ratios),"round1_fidelity":round1_fidelity if round1_fidelity is not None else
                {"status":"NOT-EVALUATED","reason":"no first-round failing requirements"},
            "geometry":self.geometry(carriers,summed,first,batch,post)}
        if mode=="astra" and arm==R.A7:self.Z_capacity=write["carrier_count"]
        self.current={"post":post,"write":write,"first":first,"carriers":carriers,"start":start}
        self.hooks_check()
        return {str(l):{"delta_norm":float((self.weights[l].detach().cpu().float()-self.pristine[l].float()).norm()),
                        "weight_norm_before":float(self.pristine[l].float().norm()),
                        "relative_delta_norm":float((self.weights[l].detach().cpu().float()-self.pristine[l].float()).norm())/float(self.pristine[l].float().norm())}
                for l in carriers}

    def remaining_validation(self):
        return max(1380.,sum(self.timings.get("locality_probes",[])[-3:])+sum(self.timings.get("binding_evaluation",[])[-3:]))

    def geometry(self,carriers,summed,first,batch,post):
        import torch
        parallel=[];retention=[];norms={};shares=[0.]*24
        for l,cols in carriers.items():
            old=self.pristine[l][:,cols].float();new=self.weights[l][:,cols].detach().cpu().float();delta=new-old
            norms[str(l)]=float(delta.norm())
            for j in range(len(cols)):
                den=float(delta[:,j].norm()*old[:,j].norm())
                parallel.append(float((delta[:,j]*old[:,j]).sum().abs())/den if den else 0.)
                intended=float(summed.get(l,torch.zeros_like(delta,dtype=torch.float64,device="cpu"))[:,j].norm())
                retention.append(float(delta[:,j].norm())/intended if intended else 0.)
            keys=post["keys"][l]
            for j in range(len(cols)):
                ri=int(keys[:,j].abs().argmax());fact=batch["requirements"][ri]["fact"]
                shares[fact]+=float(delta[:,j].abs().sum())
        total=sum(shares)
        return {"layer_delta_norms":norms,"parallelism_abs_cos":parallel,"cast_retention":retention,
                "parallelism_median":R.median(parallel),"cast_retention_median":R.median(retention),
                "per_fact_share":{str(i):v/total if total else 0. for i,v in enumerate(shares)}}

    def transfer_diagnostic(self,batch,obs):
        first=self.current["first"]
        if first is None:return {"status":"NOT-EVALUATED","reason":"no first-round failing requirements"}
        C=self.covectors(obs);v=__import__("torch").zeros_like(C)
        for l,delta in first["patch"].items():v+=torch_cpu64(obs["keys"][l])@delta.T
        return {"predicted_delta_lead":((C*v).sum(1)/torch_cpu64(obs["scales"])).tolist(),
                "status":"POST-WRITE-DIAGNOSTIC","cannot_stop_or_tune":True}

    def stage0(self):
        """Order is binding: pin -> untouched A -> LAW#3 -> deferred probes -> D/G/Z."""
        self.stage=0;start=time.monotonic()
        self.budget.project({k:v for k,v in ALLOWANCES.items() if k!="import_and_pin"})
        if self.loaded_manifest is None:
            self.M.CONTEXT_TEMPLATES_CACHE=[list(TEMPLATES[:1]),list(TEMPLATES[1:])]
        identity=hashlib.sha256(json.dumps(self.M.CONTEXT_TEMPLATES_CACHE).encode()).hexdigest()[:12]
        R.require(identity=="c7dabbe7c25a","HALTED-V12","C10Q engine-form template identity")
        self.templates=self.flatten_templates(self.M.CONTEXT_TEMPLATES_CACHE)
        R.require(self.templates==self.budget.templates,"HALTED-V12",
                  "context template list differs from selected benchmark")
        R.require(R.json_digest(self.templates)==self.budget.templates_sha256,"HALTED-V12",
                  "context templates differ from selected benchmark")
        write_json(self.out/"context_templates.json",self.M.CONTEXT_TEMPLATES_CACHE)
        self.context_templates_record={"sha256":sha256_file(self.out/"context_templates.json"),
            "inputs_sha256":self.budget.templates_sha256,"source":"benchmark TEMPLATES / C10Q c7dabbe7c25a",
            "scorer_identity":identity,"seed":0,"sampling":False}
        # Seed 0 remains at process start; the imported templates never consume it.
        self.publish_run()
        baseline=self.run_recipe("A",R.ARMS);self.timings["recipe_A"]=time.monotonic()-start
        try:self.gates.baseline(baseline)
        except R.Halt:
            write_json(self.out/f"pass_p{self.process}.json",{"schema":R.SCHEMA,"recipes":{"A":baseline},
                "context_templates_sha256":self.context_templates_record["sha256"],
                "outcome":"HALTED","halt":{"code":"HALTED-V4","detail":"LAW#3 envelope"}})
            raise
        if self.loaded_manifest is None:
            self.batches=self.make_batches()
        self.restore();self.verify_restore("LAW#3 passed")
        self.pristine_axes=self.H.axes_pre()
        self.population={arm:self.probe_population(arm) for arm in R.ARMS}
        for arm in R.ARMS:self.pristine_probes[arm]=self.probe_hits(arm)
        if self.telemetry is not None:self.telemetry.logit_lens(self,R.A7,"pristine")
        self.pristine_heldout={}
        for arm in R.ARMS:
            held=self.make_batch(arm,list(self.H.PTEST))
            observed=self.observe(held)
            self.pristine_heldout[arm]={"leads":observed["leads"].tolist(),"requirements":held["requirements"]}
            del observed
        batch=self.batches[R.A7];pristine_obs=self.observe(batch,full=True)
        self.pristine_identity_leads=self.lead_rows(batch,pristine_obs)[0]
        self.checks["Z0"]=self.z0(batch,pristine_obs)
        pristine_eval=self.eval_guard(self.arms[R.A7])
        self.checks["pristine_canon_full"]=[row["canon_full"] for row in pristine_eval["rows"]]
        self.checks["Z2"]=z2_agreement(self.pristine_identity_leads,
            [row["canon_full"] for row in pristine_eval["rows"]],self.checks["Z0"]["tau_shape"])
        R.require(self.checks["Z2"]["ok"],"HALTED-V5","pristine Z2 empty/mismatch")
        self.eval_signature=self.evaluation_signature()
        dstart=time.monotonic()
        for arm,snapshot in self.snapshots.items():
            def deferred(arm=arm,snapshot=snapshot):
                import torch
                with torch.no_grad():
                    for l,w in snapshot.items():self.weights[l].copy_(w.to(self.weights[l].device))
                record=baseline["arms"][arm]
                axes=self.axes_guard(self.pristine_axes,list(self.arms[arm].values()))
                record["locality_axes"]["per_edge_vectors"]=axes["per_edge_vectors"]
                record["realised_layer_delta_norms"]={str(l):float((snapshot[l].float()-self.pristine[l].float()).norm()) for l in snapshot}
                held=self.make_batch(arm,list(self.H.PTEST));post_held=self.observe(held)
                record["heldout_position_leads"]={"pre":self.pristine_heldout[arm]["leads"],
                    "post":post_held["leads"].tolist(),"requirements":held["requirements"]}
                del post_held
                record["rows"]=baseline["detail"][arm]
                self.attach_probes(arm,record,self.probe_hits(arm),self.observe(self.batches[arm]))
            self.guarded(deferred,"deferred baseline "+arm)
        self.sync();self.timings["deferred_baseline"]=time.monotonic()-dstart
        self.budget.project({"reference_D":300.,"G":120.,"all_checks_probes":self.remaining_validation(),
            "candidate_rounds":1200.,"serialization_restore":180.})
        self.prepare_instruments()
        zstart=time.monotonic();self.numeric_checks(pristine_obs)
        self.sync();self.timings["verification"]=time.monotonic()-zstart
        self.checks["Z6"]={"ok":all(r["ok"] for r in self.restores)}
        self.gates.instruments(self.checks)
        self.make_manifest()
        self.sync();self.timings["stage0"]=time.monotonic()-start
        self.write_checks()
        self.budget.project({"candidate_rounds":1200.,"checks_probes_eval":self.remaining_validation(),"serialization_restore":180.})

    def z0(self,batch,obs):
        import torch
        sigma=0.;full_sigma=0.;single=[]
        for i,target in enumerate(batch["target_ids"]):
            prompt=batch["prompt_ids"][i*6];ref=[]
            with torch.no_grad():
                full=self.H.model(torch.tensor([prompt+target[:-1]],device=self.H.DEV),use_cache=False,logits_to_keep=0).logits[0]
            for q,y in enumerate(target):
                self.budget.check()
                with torch.no_grad():
                    native=self.H.model(torch.tensor([prompt+target[:q]],device=self.H.DEV),use_cache=False,logits_to_keep=0).logits[0,-1]
                lead=float(margin_leads(native[None,:],torch.tensor([y],device="cpu"))[0][0]);ref.append(lead)
                ri=next(k for k,r in enumerate(batch["requirements"]) if r["fact"]==i and r["view"]==0 and r["q"]==q)
                sigma=max(sigma,abs(lead-float(obs["leads"][ri])))
                original=float(margin_leads(full[len(prompt)+q-1][None,:],torch.tensor([y],device="cpu"))[0][0])
                full_sigma=max(full_sigma,abs(original-float(obs["leads"][ri])))
            single.append(ref)
        if sigma>.125:
            self.checks["Z0"]={"ok":False,"sigma_shape":sigma,"original_full_sequence_sigma":full_sigma}
        R.require(sigma<=.125,"HALTED-V5","Z0 spread >.125 logits")
        return {"ok":True,"sigma_shape":sigma,"tau_shape":max(2*sigma,.02),
                "original_full_sequence_sigma":full_sigma,"prefix_shape_leads":single,
                "identity_batch_leads":self.lead_rows(batch,obs)[0]}

    def evaluation_signature(self):
        import torch
        out=[]
        for subject in self.H.FICTION:
            targets=self.H.tgt_ids(self.arms[R.A7][subject])
            for frame in [self.H.CANON]+self.H.PTEST:
                ids=self.H.tok(frame.format(subject))["input_ids"]
                gen=self.greedy(ids,targets)["generated"]
                with torch.no_grad():
                    logits=self.H.model(torch.tensor([ids],device=self.H.DEV),use_cache=False,logits_to_keep=0).logits[0,-1].detach().float().cpu()
                torch_cpu64(logits);out.append((gen,logits))
        return out

    def prepare_instruments(self):
        R.require(self.gates.law3,"HALTED-V4","instrument preparation before LAW#3")
        import torch
        if self.loaded_manifest is not None:
            self.dstats=torch.load(self.input_dir/"dstats.pt",map_location="cpu",weights_only=True)
            self.G=torch.load(self.input_dir/"G.pt",map_location="cpu",weights_only=True)
        else:
            self.dstats=self.compute_dstats();self.G=self.compute_G()
        self.D={};self.D_floored=0
        for l,m in self.dstats["m"].items():
            self.D[int(l)],n=null_weights(m);self.D_floored+=n
        try:self.cholesky=torch.linalg.cholesky(torch_cpu64(self.G))
        except RuntimeError as exc:raise R.Halt("HALTED-V8",str(exc)) from exc
        self.checks["V8"]={"cholesky":True,"condition":float(torch.linalg.cond(self.G))}
        import numpy as np
        correlations={}
        for l in range(4,13):
            path=self.covariance_paths()[str(l)]
            with np.load(path,allow_pickle=False) as stat:
                diagonal=np.diag(stat["mom2.mom2"])/int(stat["mom2.count"])
            correlations[str(l)]=spearman(self.dstats["m"][str(l)].tolist(),diagonal.tolist())
        self.checks["V7"]={"spearman":correlations,"late_layers_fidelity":"UNVERIFIED: no cached late-layer reference"}
        R.require(all(v>=.8 for v in correlations.values()),"HALTED-V7","D/cache Spearman <.80")
        if self.loaded_manifest is not None:
            for name in ("dstats.pt","G.pt"):
                with (self.out/name).open("xb") as f:
                    f.write((self.input_dir/name).read_bytes());f.flush();os.fsync(f.fileno())
        else:
            self.save_tensor_file("dstats.pt",self.dstats);self.save_tensor_file("G.pt",self.G)
        audit=overlap_audit([t.format(self.H.CANON) for t in self.templates],
                            self.dstats["dataset"]["texts"],self.H.PTEST)
        write_json(self.out/"overlap_audit.json",audit)

    def save_tensor_file(self,name,value):
        import torch
        with (self.out/name).open("xb") as f:torch.save(value,f);f.flush();os.fsync(f.fileno())

    def compute_dstats(self):
        import torch
        from datasets import load_dataset
        from huggingface_hub import HfApi
        self.budget.check();start=time.monotonic()
        revision=HfApi().dataset_info("wikimedia/wikipedia").sha
        R.require(isinstance(revision,str) and len(revision)==40,"HALTED-V12","unresolved Wikipedia revision")
        dataset=load_dataset("wikimedia/wikipedia","20231101.en",split="train",streaming=True,revision=revision)
        rows=list(dataset.take(1000))
        R.require(len(rows)==1000,"HALTED-V7","reference row population !=1000")
        ids=[self.H.tok(row["text"])["input_ids"][:100] for row in rows]
        metadata={"revision":revision,"row_ids":[str(row["id"]) for row in rows],
            "text_sha256":[hashlib.sha256(row["text"].encode()).hexdigest() for row in rows],
            "texts":[row["text"] for row in rows],"tokenizer_truncation":"tok(text)[input_ids][:100]",
            "nonpadding_tokens":sum(map(len,ids)),"ordered_token_ids":ids}
        sums={str(l):torch.zeros(11008,dtype=torch.float64,device="cpu") for l in range(36)}
        for start_row in range(0,1000,16):
            self.budget.check();part=ids[start_row:start_row+16];length=max(map(len,part))
            mask=torch.tensor([[1]*len(row)+[0]*(length-len(row)) for row in part],device=self.H.DEV)
            handles=[]
            try:
                for l in range(36):
                    def collect(module,args,l=l):
                        values=args[0][mask.bool()].detach().float().cpu().double()
                        torch_cpu64(values);sums[str(l)]+=values.pow(2).sum(0)
                    handles.append(self.modules[str(l)].register_forward_pre_hook(collect))
                with torch.no_grad():
                    self.H.model(input_ids=torch.tensor([row+[self.H.tok.pad_token_id]*(length-len(row)) for row in part],device=self.H.DEV),
                        attention_mask=mask,use_cache=False,logits_to_keep=0)
            finally:
                for handle in reversed(handles):handle.remove()
                self.hooks_check()
            self.check_memory()
        self.sync();self.timings["D"]=time.monotonic()-start
        return {"m":{l:(v/metadata["nonpadding_tokens"]).float() for l,v in sums.items()},"dataset":metadata}

    def compute_G(self):
        import torch
        self.budget.check();start=time.monotonic();W=self.H.model.model.embed_tokens.weight.detach()
        gain=torch_cpu64(self.H.model.model.norm.weight)
        G=torch.zeros((2048,2048),dtype=torch.float64,device="cpu")
        for i in range(0,len(W),8192):
            self.budget.check();chunk=torch_cpu64(W[i:i+8192])*gain
            G+=chunk.T@chunk
        self.sync();self.timings["G"]=time.monotonic()-start;return torch_cpu64(G)

    def numeric_checks(self,pristine_obs):
        import torch
        batch=self.batches[R.A7];carriers=self.choose(pristine_obs,batch,"astra")
        idx,C,d,s,K,D=self.quantities(pristine_obs,carriers)
        R.require(len(idx)>0,"HALTED-V5","Z3/Z7 need a real failing set")
        gamma=5.-pristine_obs["leads"][idx];sol=joint_solve(C,d,s,K,D,gamma)
        self.checks["Z4"]=self.z4(pristine_obs,idx,carriers,sol,gamma)
        self.checks["Z7"]=self.z7(batch,carriers)
        self.checks["Z1"]={"ok":pristine_obs["head_error"]<=self.checks["Z7"]["tau_head"],
            "native_reconstruction_error":pristine_obs["head_error"],"analytic_leads":self.analytic_leads(pristine_obs).tolist()}
        for mode in ("astra","band"):
            def check(mode=mode):
                obs=self.observe(batch);S=self.choose(obs,batch,mode,sum(map(len,carriers.values())))
                counters=[];lambdas=[];failing_count=None
                for _ in range(2):
                    indices,c,direction,scale,keys,weights=self.quantities(obs,S)
                    solved=joint_solve(c,direction,scale,keys,weights,torch.zeros(len(indices),dtype=torch.float64,device="cpu"))
                    failing_count=len(indices) if failing_count is None else failing_count
                    R.require(len(indices)==failing_count>0,"HALTED-V5","Z3 real failing set changed")
                    lambdas.append(solved["lambda"].tolist())
                    R.require(bool((solved["lambda"]==0).all()),"HALTED-V5","Z3 lambda nonzero")
                    count=sum(write_columns(self.weights[l],cols,solved["patch"][l]) for l,cols in S.items());counters.append(count)
                    R.require(count==sum(map(len,S.values())),"HALTED-V5","Z3 write counters")
                    self.footprint(S)
                    obs=self.observe(batch,S,full=True);obs["selected"]=True
                    R.require(obs["head_error"]<=self.checks["Z7"]["tau_head"],"HALTED-V5","Z3 post-write Z1")
                post=self.observe(batch,S)
                R.require(all(torch.equal(w.detach().cpu(),self.pristine[l]) for l,w in self.weights.items()),"HALTED-V5","Z3 weights differ")
                signature=self.evaluation_signature()
                equal=all(old[0]==new[0] and torch.equal(old[1],new[1]) for old,new in zip(self.eval_signature,signature))
                R.require(equal,"HALTED-V5","Z3(d) changed generations/logits")
                return {"ok":True,"rounds":2,"columns_written":counters,"carrier_count":sum(map(len,S.values())),
                    "failing_count":failing_count,"lambda_by_round":lambdas,"weights_equal":True,
                    "pristine_generations":[row[0] for row in self.eval_signature],"post_generations":[row[0] for row in signature],
                    "pristine_logits_sha256":[tensor_hash(row[1]) for row in self.eval_signature],
                    "post_logits_sha256":[tensor_hash(row[1]) for row in signature],"max_logit_delta":0.}
            self.checks.setdefault("Z3",{"ok":True,"modes":{}})["modes"][mode]=self.guarded(check,"Z3 "+mode)
        self.checks["Z5"]["footprints_checked"]=True

    def analytic_leads(self,obs):
        return (self.covectors(obs)*torch_cpu64(obs["x"])).sum(1)/torch_cpu64(obs["scales"])

    def z4(self,obs,indices,carriers,sol,gamma):
        import torch,random
        K={l:torch_cpu64(obs["keys"][l][indices][:,cols]) for l,cols in carriers.items()}
        v=torch.zeros((len(indices),2048),dtype=torch.float64,device="cpu")
        for l in carriers:v+=K[l]@sol["patch"][l].T
        W=self.H.model.model.embed_tokens.weight.detach();g=torch_cpu64(self.H.model.model.norm.weight)
        direct=(torch_cpu64(W[obs["targets"][indices].to(W.device)])-
                torch_cpu64(W[obs["competitors"][indices].to(W.device)]))
        pred=(direct*(g*v)).sum(1)/torch_cpu64(obs["scales"][indices])
        error=(pred-sol["A"]@sol["lambda"]).abs()
        R.require(bool((error<=1e-8*torch.maximum(torch.ones_like(gamma),gamma.abs())).all()),"HALTED-V5","Z4 first-order identity")
        C=direct*g;direction=preferred_directions(self.G,C,self.cholesky)
        rows=random.Random(0).sample(range(len(indices)),min(32,len(indices)));max_relative=0.
        for t in rows:
            independent_row=[]
            for u in range(len(indices)):
                total=0.
                for l,cols in carriers.items():
                    for j,col in enumerate(cols):total+=float(self.D[l][col])*float(K[l][t,j])*float(K[l][u,j])
                independent=float(C[t]@direction[u])*total/float(obs["scales"][indices[t]])
                independent_row.append(independent)
            actual=sol["A"][t];ref=torch.tensor(independent_row,dtype=torch.float64,device="cpu")
            max_relative=max(max_relative,float((actual-ref).norm())/max(float(ref.norm()),1e-30))
        R.require(max_relative<=1e-10,"HALTED-V5","Z4 independent loop A")
        return {"ok":True,"max_identity_error":float(error.max()),"loop_relative_error":max_relative,
            "identity_errors":error.tolist(),"identity_bounds":(1e-8*torch.maximum(torch.ones_like(gamma),gamma.abs())).tolist(),
            "loop_rows":rows,"ridge_residual":float((sol["A"]@sol["lambda"]-gamma).abs().max()/gamma.abs().max()),
            "condition":float(torch.linalg.cond(sol["ridged"]))}

    def z7(self,batch,carriers):
        """Independent gather and finite native-shape last-layer reference, never x+delta*k."""
        import torch,numpy as np
        trace_layers=sorted(set(carriers)|{35})
        pristine=self.observe(batch,full=True,trace_layers=trace_layers)
        self.audit_requirement_map(batch)
        for i in range(4):
            row=i*6;pids=batch["prompt_ids"][row]
            for q in range(len(batch["target_ids"][i])):
                position=len(pids)+q-1
                ri=next(n for n,r in enumerate(batch["requirements"]) if r["fact"]==i and r["view"]==0 and r["q"]==q)
                for l in carriers:
                    expected=pristine["trace"][l][row,position].detach().float().cpu()
                    R.require(torch.equal(expected,pristine["keys"][l][ri]),"HALTED-V5","Z7 independent same-forward key mismatch")
        competitors=pristine["competitors"]
        ref_before=self.native_last_layer_reference(batch,pristine,self.pristine[35],competitors)
        sigma=float((ref_before-pristine["leads"]).abs().max());tau=max(2*sigma,.02)
        R.require(tau<=.25,"HALTED-V5","Z7 tau_head >.25")
        failing=[i for i,r in enumerate(batch["requirements"]) if r["view"]==0 and float(pristine["leads"][i])<5.][:8]
        R.require(bool(failing),"HALTED-V5","Z7 no active control")
        controls=[];nonzero=0
        for ri in failing:
            def control(ri=ri):
                C=self.covectors(pristine)[ri:ri+1];s=torch_cpu64(pristine["scales"][ri:ri+1])
                scores=semcon(C,s,{35:pristine["keys"][35][ri:ri+1]},{35:self.weights[35]})[35]
                cols=sorted(range(11008),key=lambda j:(-float(scores[j]),j))[:16]
                keys=pristine["keys"][35][ri:ri+1,cols]
                prod=joint_solve(C,preferred_directions(self.G,C,self.cholesky),s,{35:keys},
                                 {35:self.D[35][cols]},torch.ones(1,dtype=torch.float64,device="cpu"))
                req=batch["requirements"][ri];row=req["fact"]*6+req["view"]
                independent_pos=len(batch["prompt_ids"][row])+req["q"]-1
                k=pristine["trace"][35][row,independent_pos,cols].detach().float().cpu().double().numpy()
                target_id=batch["target_ids"][req["fact"]][req["q"]]
                competitor_id=int(competitors[ri]);embedding=self.H.model.model.embed_tokens.weight.detach()
                c=((embedding[target_id].detach().float().cpu().double()-embedding[competitor_id].detach().float().cpu().double())*
                    self.H.model.model.norm.weight.detach().float().cpu().double()).numpy()
                direction=np.linalg.solve(self.G.numpy(),c);direction/=np.dot(c,direction)
                means=self.dstats["m"]["35"].double().numpy();D=1/np.maximum(means,.001*np.median(means))
                scalar=sum(D[j]*k[h]*k[h] for h,j in enumerate(cols))*np.dot(c,direction)/float(s[0])
                coefficient=1/(scalar+.001*scalar)
                delta=np.stack([D[j]*coefficient*k[h]*direction for h,j in enumerate(cols)],axis=1)
                R.require(abs(float(prod["A"][0,0])-scalar)<=1e-8*max(1.,abs(scalar)) and
                    abs(float(prod["lambda"][0])-coefficient)<=1e-8*max(1.,abs(coefficient)),"HALTED-V5","Z7 scalar coefficients")
                R.require(np.allclose(prod["patch"][35].numpy(),delta,rtol=1e-10,atol=1e-8),"HALTED-V5","Z7 scalar columns")
                reference=self.pristine[35].clone()
                reference[:,cols]=(reference[:,cols].float()+torch.from_numpy(delta).float()).half()
                ref_after=self.native_last_layer_reference(batch,pristine,reference,competitors)
                count=write_columns(self.weights[35],cols,prod["patch"][35]);self.footprint({35:cols})
                post=self.observe(batch,full=True,trace_layers=[35])
                native_fixed=fixed_leads(post,competitors)
                err=float((ref_after-native_fixed).abs().max())
                R.require(err<=tau,"HALTED-V5","Z7 native finite reference mismatch")
                active=not torch.equal(self.weights[35].detach().cpu(),self.pristine[35])
                realised_delta=self.weights[35][:,cols].detach().cpu().float()-self.pristine[35][:,cols].float()
                v=torch_cpu64(pristine["keys"][35][:,cols])@torch_cpu64(realised_delta).T
                predicted=(self.covectors(pristine)*v).sum(1)/torch_cpu64(pristine["scales"])
                return {"requirement":ri,"columns_written":count,"nonzero_realised":active,"post_error":err,
                    "scalar_A":scalar,"lambda":coefficient,
                    "coefficient_error":abs(float(prod["lambda"][0])-coefficient),"coefficient_bound":1e-8*max(1.,abs(coefficient)),
                    "columns_error":float(np.max(np.abs(prod["patch"][35].numpy()-delta))),
                    "columns_bound":1e-8+1e-10*float(np.max(np.abs(delta))),
                    "predicted_delta_lead":predicted.tolist(),"realised_delta_lead":(native_fixed-pristine["leads"]).tolist(),
                    "frozen_scale_linearization_error":float((native_fixed-pristine["leads"]-predicted).abs().max())}
            result=self.guarded(control,"Z7 control "+str(ri));controls.append(result);nonzero+=int(result["nonzero_realised"])
        R.require(nonzero>0,"HALTED-V5","Z7 no realised nonzero change")
        return {"ok":True,"same_forward_key_equality":True,"requirement_map_audited":True,"sigma_head":sigma,
                "tau_head":tau,"nonzero_controls":nonzero,"controls":controls}

    def audit_requirement_map(self,batch):
        expected=[]
        for i,target in enumerate(batch["target_ids"]):
            for view in range(len(batch["frames"])):
                row=i*len(batch["frames"])+view;prompt=batch["prompt_ids"][row]
                for q,y in enumerate(target):
                    position=len(prompt)+q-1
                    R.require(batch["attention_mask"][row][position]==1,"HALTED-V5","Z7 padded index")
                    expected.append({"row":row,"fact":i,"view":view,"q":q,"index":position,"target":y})
        R.require(expected==batch["requirements"],"HALTED-V5","Z7 production requirement table differs")

    def native_last_layer_reference(self,batch,obs,Wref,competitors):
        import torch
        with torch.no_grad():
            logits=last_layer_logits(obs["trace"][35],Wref.to(self.H.DEV),obs["residual35"],
                                    self.H.model.model.norm,self.H.model.lm_head)
            rows=torch.tensor([r["row"] for r in batch["requirements"]],device=self.H.DEV)
            positions=torch.tensor([r["index"] for r in batch["requirements"]],device=self.H.DEV)
            gathered=logits[rows,positions].detach().float().cpu()
        index=torch.arange(len(competitors),device="cpu")
        result=gathered[index,obs["targets"]]-gathered[index,competitors]
        return torch_cpu64(result)

    def covariance_paths(self):
        from util.globals import STATS_DIR
        return {str(l):Path(STATS_DIR)/"Qwen_Qwen2.5-3B/wikipedia_stats"/
                f"model.layers.{l}.mlp.down_proj_float32_mom2_t100_100000.npz" for l in range(4,13)}

    def make_manifest(self):
        parts=self.input_parts()
        if self.loaded_manifest is not None:
            R.require(parts==self.loaded_manifest["parts"],"HALTED-V12","complete process2 manifest differs")
        self.manifest={"parts":parts,"H_in":R.json_digest(parts)}
        write_json(self.out/"manifest.json",self.manifest)

    def input_parts(self):
        H=self.H;snapshot=ROOT/"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots"/H.REV
        tokenizer_files={p.name:sha256_file(p) for p in sorted(snapshot.iterdir())
                         if p.is_file() and ("token" in p.name or p.name in ("vocab.json","merges.txt","config.json"))}
        R.require("tokenizer.json" in tokenizer_files and "tokenizer_config.json" in tokenizer_files,
                  "HALTED-V12","tokenizer provenance incomplete")
        import torch,transformers,numpy
        return {"requests":{arm:[H.req(H.CANON,s,self.arms[arm][s]) for s in H.FICTION] for arm in R.ARMS},
            "model_revision":H.REV,"H_pristine":self.H_pristine,"safetensors":self.safetensors,
            "context_templates_sha256":sha256_file(self.out/"context_templates.json"),
            "dstats_sha256":sha256_file(self.out/"dstats.pt"),"G_sha256":sha256_file(self.out/"G.pt"),
            "settings":SETTINGS,"driver_sha256":sha256_file(Path(__file__)),"reader_sha256":sha256_file(Path(R.__file__)),
            "prereg_sha256":sha256_file(ROOT/PREREG),"seed":0,"go_sha256":self.budget.go_sha256,
            "engine_sources":self.fingerprint["start"],
            "hparams":{HP:sha256_file(ROOT/HP)},
            "screens":{str(p.relative_to(ROOT)):sha256_file(p) for p in (ROOT/"configs/screens/g6_screen_qwen3b.json",ROOT/"configs/screens/g6_screen_qwen3b_v2.json")},
            "covariances":{l:{"path":str(p),"sha256":sha256_file(p)} for l,p in self.covariance_paths().items()},
            "tokenizer":tokenizer_files,"batches":self.batches,
            "forward_settings":{"use_cache":False,"logits_to_keep":0,"padding_side":"right",
                "attention":H.model.config._attn_implementation,"training":H.model.training},
            "environment":{"device":str(H.DEV),"dtype":str(next(H.model.parameters()).dtype).removeprefix("torch."),
                           "torch":torch.__version__,"transformers":transformers.__version__},
            "solver_backend":{"device":"cpu","dtype":"float64","torch_config":torch.__config__.show(),
                              "threads":torch.get_num_threads(),"numpy":numpy.__version__},
            "dataset":{k:v for k,v in self.dstats["dataset"].items() if k!="texts"}}

    def validate_inputs(self,input_dir):
        self.input_dir=input_dir;self.loaded_manifest=load_json(input_dir/"manifest.json")
        parts=self.loaded_manifest["parts"]
        R.validate_manifest(parts)
        R.require(R.json_digest(parts)==self.loaded_manifest["H_in"],
            "HALTED-V12","incomplete frozen process1 manifest")
        for key,file in (("context_templates_sha256","context_templates.json"),("dstats_sha256","dstats.pt"),("G_sha256","G.pt")):
            R.require(sha256_file(input_dir/file)==parts[key],"HALTED-V12","input file SHA "+file)
        for group in ("engine_sources","hparams","screens"):
            for path,sha in parts[group].items():R.require(sha256_file(ROOT/path)==sha,"HALTED-V12","input source drift "+path)
        for value in parts["covariances"].values():R.require(sha256_file(value["path"])==value["sha256"],"HALTED-V12","covariance changed")
        for path,key in ((Path(__file__),"driver_sha256"),(Path(R.__file__),"reader_sha256"),(ROOT/PREREG,"prereg_sha256")):
            R.require(sha256_file(path)==parts[key],"HALTED-V12","frozen build source changed")
        R.require(parts["settings"]==SETTINGS and parts["seed"]==0,"HALTED-V12","frozen settings")

    def check_manifest_before_baseline(self,snapshot):
        parts=self.loaded_manifest["parts"]
        R.require(parts["safetensors"]==self.safetensors,"HALTED-V12","model file identity differs before baseline")
        for name,sha in parts["tokenizer"].items():R.require(sha256_file(snapshot/name)==sha,"HALTED-V12","tokenizer changed")
        R.require(self.batches==parts["batches"],"HALTED-V12","ordered IDs/masks/lengths differ before baseline")
        requests={arm:[self.H.req(self.H.CANON,s,self.arms[arm][s]) for s in self.H.FICTION] for arm in R.ARMS}
        R.require(requests==parts["requests"],"HALTED-V12","request JSONs differ before baseline")
        import torch,transformers,numpy
        actual={"device":str(self.H.DEV),"dtype":"float16","torch":torch.__version__,"transformers":transformers.__version__}
        R.require(actual==parts["environment"],"HALTED-V12","installed environment changed before baseline")
        solver={"device":"cpu","dtype":"float64","torch_config":torch.__config__.show(),
                "threads":torch.get_num_threads(),"numpy":numpy.__version__}
        R.require(solver==parts["solver_backend"],"HALTED-V12","CPU backend changed before baseline")
        forward={"use_cache":False,"logits_to_keep":0,"padding_side":"right",
                 "attention":self.H.model.config._attn_implementation,"training":self.H.model.training}
        R.require(forward==parts["forward_settings"],"HALTED-V12","forward settings changed before baseline")

    def write_checks(self):
        write_json(self.out/f"checks_p{self.process}.json",{**self.checks,"memory":self.memory,"restores":self.restores,
            "hook_registries":{k:{kind:list(hooks) for kind,hooks in v.items()} for k,v in self.initial_hooks.items()},
            "component_timing":self.timings,"allowances":self.unknown_allowances,
            "allowance_status":"UNMEASURED prospective scheduling allowances; no feasibility claim"},replace=(self.out/f"checks_p{self.process}.json").exists())

    def complete_recipe_readouts(self,name):
        for arm,record in self.recipes[name]["arms"].items():
            hits=record.pop("probe_hits");view_leads=record["post_fit_observation"]
            self.attach_probes(arm,record,hits)
            record["fit"]=R.fit_counts(view_leads[0],[row for view in view_leads for row in view])
            record["phi_mu"]=record["fit"]["m"]/record["fit"]["M"]
            record["phi_0_id"]=record["fit"]["positive_identity_fact_n"]/24
            record["identity_view_leads"]=view_leads[0]
            record["per_fact_min_lead_by_view"]=[[min(row) for row in view] for view in view_leads]
            z2=z2_agreement(view_leads[0],[row["canon_full"] for row in record["rows"]],self.checks["Z0"]["tau_shape"])
            self.checks.setdefault("post_write_Z2",[]).append({"recipe":name,"arm":arm,**z2})
            R.require(z2["ok"],"HALTED-V5","post-write Z2 empty/mismatch")

    def record(self,stage):
        if R.A7 in self.recipes.get("Z",{"arms":{}})["arms"]:
            a=self.recipes["A"]["arms"][R.A7];z=self.recipes["Z"]["arms"][R.A7]
            Z_sum=sum(z["write"]["geometry"]["layer_delta_norms"].values())
            A_sum=sum(a["realised_layer_delta_norms"].values())
            z["write"]["patch_norm_Z_over_A"]=zero_column_ratio(A_sum,Z_sum)
        sources=source_hashes()
        self.fingerprint["end"]={k:v for k,v in sources.items() if k==HARNESS or k.startswith("memit_dry_run/memit/")}
        R.require(self.initial_sources==sources,"HALTED-V1","source changed during process")
        hashes={name:sha256_file(self.out/name) for name in ("context_templates.json","dstats.pt","G.pt",
                  "pristine_hash.json","manifest.json","overlap_audit.json")}
        z=self.recipes["Z"]["arms"][R.A7];a=self.recipes["A"]["arms"][R.A7];gates=R.side_gates(z,a)
        if stage==2:gates["G0"]=all(self.recipes["Z"]["arms"][k]["para_full_n"]>=68 for k in (R.A1,R.A2))
        seconds=[v["write"]["wall_seconds"] for name in ("Z","Z-band") for v in self.recipes.get(name,{"arms":{}})["arms"].values()]
        decision=R.classify_candidate(z,a,gates,stage,self.recipes["Z-band"]["arms"][R.A7] if stage==2 else None,seconds,self.budget.durations)
        return {"schema":R.SCHEMA,"attempt_id":self.attempt_id,"process":self.process,"pid":os.getpid(),"stage_completed":stage,
            "H_in":self.manifest["H_in"],"manifest":self.manifest,"H_pristine":self.H_pristine,
            "artifact_hashes":hashes,"fingerprint":self.fingerprint,"checks":self.checks,"restores":self.restores,
            "memory":self.memory,"recipes":self.recipes,"budget":{"halted":False,"history":self.budget.history,
                "origins":self.budget.origins,"ceilings":self.budget.durations},
            "omissions":R.stage_omissions(self.process,stage,decision["next_stage"],self.budget.durations,decision),
            "certificate":{"artifact_identity":"NOT-EVALUATED","numeric_behavioral_reproduction":"NOT-EVALUATED"},
            "outcome":"COMPLETE"}

    def stage1(self):
        self.stage=1;self.budget.project({"candidate_rounds":1200.,"checks_probes_eval":self.remaining_validation(),"serialization_restore":180.})
        self.run_recipe("Z",(R.A7,),"astra");self.complete_recipe_readouts("Z")
        self.write_checks();record=self.record(1);reading=R.read_process(record)
        R.require(reading["scientific_verdict"],reading["label"],reading.get("detail","reader"))
        write_json(self.out/f"pass_p{self.process}.json",record)
        self.budget.check()
        if reading["next_stage"]!=2:self.budget.future_stage2_s=0.
        return reading

    def stage2(self):
        self.stage=2;self.budget.enter(2)
        self.budget.project({"candidate_rounds":3600.,"checks_probes_eval":3*self.remaining_validation(),"serialization_restore":180.})
        old=self.recipes["Z"]
        added=self.run_recipe("Z",(R.A1,R.A2),"astra");self.complete_recipe_readouts("Z")
        added["arms"]={R.A7:old["arms"][R.A7],**added["arms"]}
        added["detail"]={R.A7:old["detail"][R.A7],**added["detail"]}
        added["audit"]["astra_calls"]+=old["audit"]["astra_calls"]
        self.run_recipe("Z-band",(R.A7,),"band");self.complete_recipe_readouts("Z-band")
        self.write_checks();record=self.record(2);reading=R.read_process(record)
        R.require(reading["scientific_verdict"],reading["label"],reading.get("detail","reader"))
        write_json(self.out/f"pass_p{self.process}.json",record,replace=True)
        self.budget.check();return reading

    def close(self):
        self.restore();self.verify_restore("process close")
        self.write_checks()
        record=self.record(self.stage);write_json(self.out/f"pass_p{self.process}.json",record,replace=True)
        self.sync()
        self.closed_model=True
        H=self.H;H.my_edit=self.original_edit;H.eval_arm=self.original_eval;H.ARM_HOOKS=self.original_hooks;H.axes_post=self.original_axes
        del self.weights,self.modules,self.current,self.snapshots,self.pristine,self.eval_signature
        del H.model
        gc.collect()
        import torch
        torch.mps.synchronize();torch.mps.empty_cache()
        self.budget.check()


def ratio_summary(values):
    finite=sorted(math.inf if v==R.INFINITY else v for v in values)
    def export(v):return R.INFINITY if math.isinf(v) else v
    def quantile(q):
        position=(len(finite)-1)*q;lo=int(position);hi=math.ceil(position)
        return finite[lo] if lo==hi else finite[lo]*(hi-position)+finite[hi]*(position-lo)
    return {"median":R.median(values),"IQR":[export(quantile(.25)),export(quantile(.75))],
            "p95":export(quantile(.95)),"maximum":export(max(finite)),"carrier_count":len(values),
            "above_0_24":sum(v>.24 for v in finite)}


def spearman(x,y):
    def ranks(values):
        indices=sorted(range(len(values)),key=lambda i:values[i]);out=[0.]*len(values);start=0
        while start<len(indices):
            end=start+1
            while end<len(indices) and values[indices[end]]==values[indices[start]]:end+=1
            for pos in range(start,end):out[indices[pos]]=(start+end-1)/2
            start=end
        return out
    a,b=ranks(x),ranks(y);ma=statistics.mean(a);mb=statistics.mean(b)
    numerator=sum((v-ma)*(w-mb) for v,w in zip(a,b))
    denominator=math.sqrt(sum((v-ma)**2 for v in a)*sum((v-mb)**2 for v in b))
    R.require(denominator>0,"HALTED-V7","constant rank statistic")
    return numerator/denominator


def overlap_audit(views,texts,heldout):
    import re
    def normalize(s):
        s=s.casefold().replace("{}"," subjectplaceholder ")
        return " ".join(re.sub(r"[^\w\s]"," ",s).split())
    frames=[normalize(s) for s in heldout]
    def rows(population):
        return [{"index":i,"sha256":hashlib.sha256(s.encode()).hexdigest(),
                 "exact":[normalize(s)==frame for frame in frames],
                 "heldout_frame_containment":[frame in normalize(s) for frame in frames]} for i,s in enumerate(population)]
    return {"normalization":"casefold; punctuation removal; whitespace collapse; preserve subject placeholder",
            "views":rows(views),"reference_texts":rows(texts),"population_sha256":R.json_digest([views,texts]),
            "implementation_sha256":hashlib.sha256(__import__("inspect").getsource(overlap_audit).encode()).hexdigest(),
            "input_selection_used_PTEST":False}


def launch_duration(env,key):
    if key not in env:return None
    try:value=float(env[key])
    except ValueError as exc:raise R.Halt("HALTED-BUDGET","invalid "+key) from exc
    R.require(math.isfinite(value) and value>0,"HALTED-BUDGET","invalid "+key);return value


def go_record(env):
    """Prereg §6: validate the recorded go before creating or launching an attempt."""
    path=env.get("C10Z_GO_RECORD")
    R.require(isinstance(path,str) and path.strip(),"HALTED-V12","C10Z_GO_RECORD is required")
    try:
        raw=Path(path).read_bytes();value=json.loads(raw,
            parse_constant=lambda token:R.require(False,"HALTED-V6","non-finite go JSON: "+token))
    except (OSError,ValueError) as exc:
        raise R.Halt("HALTED-V12","go record requires benchmark_sha256, benchmark_script_sha256 and ceilings; invalid C10Z_GO_RECORD: "+str(exc)) from exc
    R.require(isinstance(value,dict),"HALTED-V12","go record must be a JSON object")
    decisions=value.get("decisions")
    R.require(isinstance(decisions,dict) and set(decisions)=={"0","1","2"} and
        all(isinstance(v,str) and v.strip().startswith("D-") and v.strip()[2:].strip() for v in decisions.values()),
        "HALTED-V12","go decisions must name exactly 0, 1, 2 with nonempty Decision-IDs")
    R.require(value.get("operator_yes") is True and value.get("one_gpu_job") is True,
        "HALTED-V12","go record requires operator_yes=true and one_gpu_job=true")
    R.require(all(isinstance(value.get(k),str) and value[k].strip() for k in ("recorded_by","recorded_at")),
        "HALTED-V12","go record requires recorded_by and recorded_at")
    ceilings=value.get("ceilings")
    R.require(R.sha(value.get("benchmark_sha256")) and R.sha(value.get("benchmark_script_sha256")) and
        isinstance(ceilings,dict) and set(ceilings)=={"stage01","stage2","stage3"} and
        all(type(v) in (int,float) and v>0 and (type(v) is int or math.isfinite(v)) for v in ceilings.values()),
        "HALTED-V12","go record requires benchmark_sha256, benchmark_script_sha256 and ceilings")
    R.finite_json(value)
    return value,hashlib.sha256(raw).hexdigest()


def benchmark_module():
    import importlib.util
    spec=importlib.util.spec_from_file_location("c10z_launch_benchmark",ROOT/"experiments/track_c/c10z_astra_benchmark.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def telemetry_switch(env):
    R.require("C10Z_TELEMETRY" not in env or env["C10Z_TELEMETRY"]=="1",
              "HALTED-V12","C10Z_TELEMETRY must be absent or 1")
    return "C10Z_TELEMETRY" in env


def strict_record(raw,detail):
    try:
        value=json.loads(raw,parse_constant=lambda token:R.require(False,"HALTED-V12",detail))
        R.finite_json(value)
        return value
    except (ValueError,TypeError) as exc:raise R.Halt("HALTED-V12",detail) from exc


def benchmark_binding(env,go):
    path=env.get("C10Z_BENCHMARK_RECORD")
    R.require(isinstance(path,str) and bool(path),"HALTED-V12","C10Z_BENCHMARK_RECORD is required")
    R.require(Path(path).is_absolute(),"HALTED-V12","C10Z_BENCHMARK_RECORD must be absolute")
    root=(ROOT/"results/c10z_astra_benchmark").resolve();path=Path(path).resolve()
    R.require(path.is_relative_to(root) and path.parent.parent==root and path.name=="benchmark.json",
              "HALTED-V12","benchmark record outside results/c10z_astra_benchmark")
    try:raw=path.read_bytes()
    except OSError as exc:raise R.Halt("HALTED-V12","benchmark record unreadable") from exc
    record_sha=hashlib.sha256(raw).hexdigest()
    R.require(record_sha==go["benchmark_sha256"],"HALTED-V12","benchmark record differs from go selection")
    record=strict_record(raw,"benchmark record is not strict JSON")
    fields=record.get("env",{}) if isinstance(record,dict) else {}
    fields=fields if isinstance(fields,dict) else {}
    script=ROOT/"experiments/track_c/c10z_astra_benchmark.py"
    try:script_sha=sha256_file(script)
    except OSError as exc:raise R.Halt("HALTED-V12","benchmark script changed") from exc
    R.require(script_sha==fields.get("script_sha256")==go["benchmark_script_sha256"],
              "HALTED-V12","benchmark script changed")
    B=benchmark_module()
    try:sources=B.source_identity(ROOT)
    except OSError as exc:raise R.Halt("HALTED-V12","benchmark source identity changed: "+str(exc.filename)) from exc
    recorded_sources=fields.get("sources")
    if sources!=recorded_sources:
        old=recorded_sources if isinstance(recorded_sources,dict) else {}
        changed=next((p for p in sources if sources[p]!=old.get(p)),next(iter(set(old)-set(sources)),"sources"))
        raise R.Halt("HALTED-V12","benchmark source identity changed: "+changed)
    current_env=B.environment_identity()
    for key,value in current_env.items():
        R.require(value==fields.get(key),"HALTED-V12","benchmark environment changed: "+key)
    try:B.validate_record(record)
    except R.Halt:raise
    except ValueError as exc:raise R.Halt("HALTED-V12","benchmark record invalid: "+str(exc)) from exc
    templates_sha256=R.json_digest(list(TEMPLATES))
    R.require(record["inputs"]["templates"]==list(TEMPLATES) and
              record["inputs"]["templates_sha256"]==templates_sha256,"HALTED-V12",
              "benchmark templates differ from TEMPLATES")
    c=B.ceilings(record)
    R.require(c.get("source")=="BENCHMARK","HALTED-BUDGET","benchmark refused: "+str(c.get("reason")))
    R.require(json.loads(json.dumps(c,sort_keys=True,allow_nan=False))==record.get("derived"),
              "HALTED-V12","benchmark derived disagrees with ceilings()")
    R.require(c["stop"] is False,"HALTED-BUDGET","benchmark STOP")
    R.require(7200<=c["C01"]<=10800,"HALTED-BUDGET","C01 outside [7200, 10800]")
    R.require(2*(c["C01"]+c["C2"])<=55800,"HALTED-BUDGET","nominal total above 55,800 s")
    selected={"stage01":c["C01"],"stage2":c["C2"],"stage3":c["C3"]}
    R.require(go["ceilings"]==selected,"HALTED-V12","go ceilings differ from ceilings()")
    return {"path":str(path),"sha256":record_sha,"script_sha256":script_sha,"sources":sources,
            "env":current_env,"ceilings":selected,"templates":record["inputs"]["templates"],
            "templates_sha256":templates_sha256},record,B


INERTNESS_SOURCES=("experiments/track_c/c10z_astra_arms.py","experiments/track_c/c10z_astra_read.py",
    "experiments/track_c/c10z_astra_telemetry_check.py","experiments/track_c/c10z_astra_benchmark.py",
    "experiments/track_c/c10e_bandknob.py","configs/hparams/qwen25_3b_memit_hparams.json",
    "memit_dry_run/memit/memit/memit_main.py")


def inertness_binding(env,benchmark,B):
    prefix="telemetry requires an INERT inertness record: "
    path=env.get("C10Z_TELEMETRY_INERTNESS")
    R.require(isinstance(path,str) and bool(path),"HALTED-V12",prefix+"required")
    R.require(Path(path).is_absolute(),"HALTED-V12",prefix+"path must be absolute")
    root=(ROOT/"results/c10z_astra_telemetry_inertness").resolve();path=Path(path).resolve()
    R.require(path.is_relative_to(root) and path.parent.parent==root and path.name=="inertness.json",
              "HALTED-V12",prefix+"path outside root")
    try:raw=path.read_bytes()
    except OSError as exc:raise R.Halt("HALTED-V12",prefix+"unreadable") from exc
    record=strict_record(raw,prefix+"strict JSON")
    keys={"schema","decision_id","device","verdict","control_equal","telemetry_equal","probe_forwards",
          "lens_forwards","weights_unchanged","sources","env","started_at","finished_at"}
    R.require(isinstance(record,dict) and set(record)==keys,"HALTED-V12",prefix+"schema")
    R.require(record["schema"]=="c10z_astra_telemetry_inertness/v1" and
              record["decision_id"]=="D-C10r-rulings-11" and record["device"]=="mps" and
              record["verdict"]=="INERT" and all(record[k] is True for k in
                  ("control_equal","telemetry_equal","weights_unchanged")),"HALTED-V12",prefix+"evidence")
    R.require(type(record["probe_forwards"]) is int and record["probe_forwards"]==B.expected_probe_forwards(benchmark) and
              type(record["lens_forwards"]) is int and record["lens_forwards"]==2*benchmark["inputs"]["population_counts"]["F0"],
              "HALTED-V12",prefix+"counts")
    try:sources={p:sha256_file(ROOT/p) for p in INERTNESS_SOURCES}
    except OSError as exc:raise R.Halt("HALTED-V12",prefix+"sources: "+str(exc.filename)) from exc
    R.require(record["sources"]==sources,"HALTED-V12",prefix+"sources")
    expected_env={**B.environment_identity(),"model_rev":"3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"}
    R.require(record["env"]==expected_env,"HALTED-V12",prefix+"environment")
    import datetime
    try:
        times=[datetime.datetime.fromisoformat(record[k]) for k in ("started_at","finished_at")]
        R.require(all(t.tzinfo is not None for t in times) and times[0]<=times[1],"HALTED-V12",prefix+"timestamps")
    except (ValueError,TypeError) as exc:raise R.Halt("HALTED-V12",prefix+"timestamps") from exc
    return {"path":str(path),"sha256":hashlib.sha256(raw).hexdigest()}


def verify_launch_binding(launch,env):
    R.require(telemetry_switch(env)==launch["telemetry"],"HALTED-V12","C10Z_TELEMETRY differs from launch")
    try:
        binding,record,B=benchmark_binding({"C10Z_BENCHMARK_RECORD":launch["benchmark"]["path"]},launch["go"])
        R.require(binding==launch["benchmark"],"HALTED-V12","benchmark binding")
        R.require(launch["stage01"]==binding["ceilings"]["stage01"],"HALTED-V12","stage01 ceiling")
        R.require(all(launch[k] is None or launch[k]==binding["ceilings"][k] for k in ("stage2","stage3")),
                  "HALTED-V12","expansion ceilings")
        if launch["telemetry"]:
            selected=inertness_binding({"C10Z_TELEMETRY_INERTNESS":launch["telemetry_inertness"]["path"]},record,B)
            R.require(selected==launch["telemetry_inertness"],"HALTED-V12","inertness binding")
        else:R.require(launch["telemetry_inertness"] is None,"HALTED-V12","inertness binding")
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise R.Halt("HALTED-V12","launch binding changed since stage 0: "+str(exc)) from exc


def diagnostic(out,code,detail,session=None):
    out=Path(out);runpath=out/"run.json"
    run=load_json(runpath) if runpath.exists() else {}
    value={"schema":R.SCHEMA,"outcome":"HALTED","halt":{"code":code,"detail":str(detail)},
           "out_dir":str(out),"pid":os.getpid(),"attempt_id":run.get("attempt_id"),"scientific_verdict":False}
    if code=="HALTED-V4":value["context_templates_sha256"]=sha256_file(out/"context_templates.json")
    if session is not None:
        value.update(recipes=session.recipes,checks=session.checks,memory=session.memory,
                     restores=session.restores,budget_history=session.budget.history)
    def safe(v):
        if isinstance(v,float) and not math.isfinite(v):return {"invalid_nonfinite":repr(v)}
        if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)):return [safe(x) for x in v]
        return v
    process=session.process if session is not None else run.get("process",2 if out.name=="process2" else 1)
    passpath=out/f"pass_p{process}.json"
    value["observations"]=load_json(passpath) if passpath.exists() else None
    value=safe(value)
    haltpath=out/f"halt_p{process}.json"
    write_json(haltpath,value,replace=haltpath.exists())
    if run:
        run.update(closed=True,halt=value["halt"],reading=None)
        write_json(runpath,run,replace=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    write_json(ROOT/("architecture_profile/c10z_astra_halt_diagnostic_"+stamp+".json"),value)
    return value


def resident(out,process,launch,input_dir=None,start=None):
    """Model lifetime is one process; deadline watchdog cannot mint a scientific pass."""
    start=time.monotonic() if start is None else start
    budget=Budget(start,launch["stage01"],launch["stage2"],launch["stage3"],process=process)
    budget.go_sha256=launch["go_sha256"]
    budget.templates=launch["benchmark"]["templates"]
    budget.templates_sha256=launch["benchmark"]["templates_sha256"]
    state=StageState(launch["attempt_id"],process);session=None;telemetry=None;stop=threading.Event()
    runpath=Path(out)/"run.json";publication_lock=threading.RLock()
    budget.terminal_probe=lambda:load_json(runpath).get("halt") if runpath.exists() else None
    def publish(reading=None,closed=False,halt=None):
        with publication_lock:
            if halt is None:budget.check()
            record={"schema":R.SCHEMA,"attempt_id":state.attempt,"pid":os.getpid(),"process":process,
                "completed":state.completed,"requested":None,"closed":closed,"launch":launch,
                "origins":budget.origins,"ceilings":budget.durations,"reading":reading,"halt":halt}
            if session is not None and getattr(session,"context_templates_record",None) is not None:
                record["context_templates"]=session.context_templates_record
            write_json(runpath,record,replace=runpath.exists())
            if halt is None:budget.check()
    def watchdog():
        last_heartbeat=0.
        try:
            while not stop.wait(.1):
                now=time.monotonic()
                if now-last_heartbeat>=1.:
                    write_json(Path(out)/"logs/heartbeat.json",{"attempt_id":state.attempt,"pid":os.getpid(),
                        "at":now},replace=(Path(out)/"logs/heartbeat.json").exists())
                    last_heartbeat=now
                deadline=budget.deadline()
                if deadline is not None and time.monotonic()>=deadline:
                    raise R.Halt("HALTED-BUDGET","hard elapsed deadline; restoration NOT-EVALUATED")
        except BaseException as exc:
            code=exc.code if isinstance(exc,R.Halt) else "HALTED-V12"
            try:
                with publication_lock:
                    diagnostic(out,code,"watchdog: "+str(exc))
                    publish(closed=True,halt={"code":code,"detail":"watchdog: "+str(exc)})
            finally:os._exit(2)
    publish();thread=threading.Thread(target=watchdog,daemon=True);thread.start()
    try:
        if launch["telemetry"] is True:telemetry=Telemetry(out,process,state.attempt)
        session=Session(out,process,budget,input_dir)
        session.telemetry=telemetry
        session.publish_run=publish
        session.attempt_id=state.attempt
        if telemetry is not None:telemetry.phase("stage_start",stage=0)
        state.run(0,state.attempt,session.stage0)
        if telemetry is not None:telemetry.phase("stage_end",stage=0)
        publish()
        if process==2:
            if telemetry is not None:telemetry.phase("stage_start",stage=1)
            reading=state.run(1,state.attempt,session.stage1)
            if telemetry is not None:telemetry.phase("stage_end",stage=1)
            if reading["next_stage"]==2:
                if telemetry is not None:telemetry.phase("stage_start",stage=2)
                reading=state.run(2,state.attempt,session.stage2)
                if telemetry is not None:telemetry.phase("stage_end",stage=2)
        else:
            reading=None
            for stage in (1,2):
                while True:
                    budget.check();request=load_json(runpath)
                    if request["requested"] is not None:
                        R.require(request["requested"]==stage and request["attempt_id"]==state.attempt,
                                  "HALTED-V12","out-of-order stage request")
                        break
                    time.sleep(.1)
                if telemetry is not None:telemetry.phase("stage_start",stage=stage)
                reading=state.run(stage,state.attempt,session.stage1 if stage==1 else session.stage2)
                if telemetry is not None:telemetry.phase("stage_end",stage=stage)
                publish(reading)
                if stage==1 and reading["next_stage"]!=2:state.closed=True;break
        session.close();state.closed=True
        if process==2:
            p1=load_json(Path(input_dir)/"pass_p1.json");p2=load_json(Path(out)/"pass_p2.json")
            repro=reproduction(p1,p2);write_json(Path(input_dir)/"repro.json",repro)
            reading=R.read_run(p1,p2,repro)
        publish(reading,closed=True);session=None
        print(json.dumps(reading,allow_nan=False),flush=True);return 0
    except BaseException as exc:
        code=exc.code if isinstance(exc,R.Halt) else "HALTED-V12"
        if session is not None and not getattr(session,"closed_model",False):
            try:session.restore();session.verify_restore("exception close")
            except BaseException as restore_exc:code="HALTED-V3";exc=restore_exc
        if telemetry is not None:telemetry.phase("halt",code=code)
        diagnostic(out,code,exc,session);publish(closed=True,halt={"code":code,"detail":str(exc)});return 2
    finally:stop.set()


def stage_call(stage,out):
    """Exactly one external stage call; stage3's internal repetition is its prereg definition."""
    start=time.monotonic();entry_preflight(os.environ);out=Path(out).resolve()
    if stage==0:
        R.require(not any((out/name).exists() for name in ("manifest.json","pass_p1.json","run.json")),
                  "HALTED-V12","attempt needs fresh OUT_DIR")
        go,go_sha256=go_record(os.environ)
        telemetry=telemetry_switch(os.environ)
        binding,benchmark,B=benchmark_binding(os.environ,go)
        stage2=launch_duration(os.environ,"C10Z_STAGE2_CEILING_S")
        R.require(stage2 is None or stage2==binding["ceilings"]["stage2"],"HALTED-BUDGET","C10Z_STAGE2_CEILING_S differs from C2")
        stage3=launch_duration(os.environ,"C10Z_STAGE3_CEILING_S")
        R.require(stage3 is None or stage3==binding["ceilings"]["stage3"],"HALTED-BUDGET","C10Z_STAGE3_CEILING_S differs from C3")
        inertness=inertness_binding(os.environ,benchmark,B) if telemetry else None
        launch={"attempt_id":uuid.uuid4().hex,
            "stage01":float(binding["ceilings"]["stage01"]),"stage2":stage2,"stage3":stage3,
            "go":go,"go_sha256":go_sha256,"benchmark":binding,"telemetry":telemetry,"telemetry_inertness":inertness}
        out.mkdir(parents=True,exist_ok=True);(out/"logs").mkdir(exist_ok=True)
        worker_env=dict(os.environ,C10Z_RESIDENT="1",C10Z_LAUNCH=json.dumps(launch),C10Z_OUT_DIR=str(out))
        with (out/"logs/resident_p1.log").open("x") as log:
            child=subprocess.Popen([sys.executable,"-B",str(Path(__file__)),"0"],env=worker_env,
                cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        while not (out/"run.json").exists():
            R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
        return wait_stage(out,0,child)
    run=load_json(out/"run.json")
    if stage==3:
        reading=R.read_directory(out)
        R.require(run["closed"] and run["halt"] is None and run["completed"]==2 and
                  reading.get("next_stage")==3,"HALTED-V12","stage3 requires clean completed K2 and closed process1")
        R.require(run["launch"]["stage3"] is not None,"HALTED-BUDGET","absent stage3 ceiling")
        p2=out/"process2"
        R.require(not p2.exists(),"HALTED-V12","process2 requires fresh OUT_DIR")
        verify_launch_binding(run["launch"],os.environ)
        p2.mkdir();(p2/"logs").mkdir()
        return resident(p2,2,run["launch"],input_dir=out,start=start)
    R.require(stage in (1,2) and not run["closed"] and run["halt"] is None and run["requested"] is None and
              run["completed"]==stage-1,"HALTED-V12","duplicate, out-of-order, stale or closed stage call")
    if stage==2:
        R.require(run["launch"]["stage2"] is not None,"HALTED-BUDGET","absent stage2 ceiling")
        reading=R.read_process(load_json(out/"pass_p1.json"))
        R.require(reading.get("next_stage")==2,"HALTED-V12","stage2 requires K1 survivor")
    # Newly set environment ceilings cannot extend an attempt's recorded launch inputs.
    run["requested"]=stage;write_json(out/"run.json",run,replace=True)
    return wait_stage(out,stage)


def wait_stage(out,stage,child=None,clock=time.monotonic,pause=time.sleep):
    start=clock()
    while True:
        run=load_json(Path(out)/"run.json")
        if run["halt"] is not None:raise R.Halt(run["halt"]["code"],run["halt"]["detail"])
        terminal=stage==2 or (stage==1 and run["reading"] is not None and run["reading"].get("next_stage") is None)
        if run["completed"]>=stage and (not terminal or run["closed"]):
            print(json.dumps(run["reading"] or {"stage0":"READY"},allow_nan=False),flush=True);return 0
        try:
            if child is not None:R.require(child.poll() is None,"HALTED-V12","resident exited before stage completion")
            lease=Path(out)/"logs/heartbeat.json"
            if lease.exists():
                heartbeat=load_json(lease)
                R.require(heartbeat["attempt_id"]==run["attempt_id"] and heartbeat["pid"]==run["pid"] and
                          clock()-heartbeat["at"]<=15.,"HALTED-V12","resident heartbeat expired or identity changed")
            else:R.require(clock()-start<=15.,"HALTED-V12","resident heartbeat never appeared")
        except R.Halt as exc:
            diagnostic(out,exc.code,exc.detail)
            raise
        pause(.1)


def main():
    R.require(len(sys.argv)==2 and sys.argv[1] in ("0","1","2","3"),"HALTED-V12","usage: run_c10z_stage.sh <0|1|2|3>")
    stage=int(sys.argv[1]);out=Path(os.environ.get("C10Z_OUT_DIR",str(ROOT/"results/c10z_astra"))).resolve()
    if os.environ.get("C10Z_RESIDENT")=="1":
        return resident(out,1,json.loads(os.environ["C10Z_LAUNCH"]))
    try:return stage_call(stage,out)
    except R.Halt as exc:
        print(str(exc),file=sys.stderr);return 2


if __name__=="__main__":sys.exit(main())
