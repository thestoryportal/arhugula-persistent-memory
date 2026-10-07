#!/usr/bin/env python3
"""Frozen-v2.2 C10W evaluation via the unchanged C10 harness's runtime seams."""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse
import copy
import hashlib
import math
import resource
import time
from pathlib import Path
import c10w_oracle_read as R
import c10w_oracle_step0 as S


class OracleEdit:
    """The production dispatch seam. Delegation and null/trained hits are distinct."""
    def __init__(self,harness,assert_base,apply_adapter):
        self.H=harness; self.ORIGINAL_MY_EDIT=harness.my_edit
        self.assert_base=assert_base; self.apply_adapter=apply_adapter
        self.mode="closedform"; self.registry={}
        self.null_passed=False; self.law3_passed=False; self.null_application=False
        self.zero_hits=0; self.trained_hits=0

    def __call__(self,hp,requests,P,cache_c):
        if self.mode=="closedform" or self.H._LAW5_DEFAULT_CTX:
            return self.ORIGINAL_MY_EDIT(hp,requests,P,cache_c)
        key=frozenset((q["subject"],q["target_new"]["str"]) for q in requests)
        R.require(key in self.registry,"oracle arm has no registered adapter")
        adapter=self.registry[key]
        if adapter["zero"]:
            R.require(self.null_application,"undeclared null application")
        else:
            R.require(self.null_passed and self.law3_passed,"trained adapter before same-process LAW#5(ii)/LAW#3")
        self.assert_base()
        result=self.apply_adapter(adapter,hp)
        if adapter["zero"]: self.zero_hits+=1
        else: self.trained_hits+=1
        return result


def request_key(values):
    return frozenset((s," "+v) for s,v in values.items())


def compare_null(u,zero,u_rows,zero_rows):
    """Compare exact prompt-level evidence; aggregate counts are insufficient (prereg:250)."""
    return R.compare_null(u,zero,u_rows,zero_rows)


class Evaluator:
    def __init__(self,H,step,phase_directory,start=None):
        import torch
        self.torch=torch; self.H=H; self.step=step; self.directory=Path(phase_directory)
        self.hp=H.MEMITHyperParams.from_json(H.HP_BASE)
        self.base=H.snap_layers(self.hp)
        self.base_hash=self.band_hash()
        self.inputs=R.load_json(step["files"]["train_inputs"]["path"])
        self.maps=self.inputs["value_maps"]
        self.mmlu=R.load_json(step["files"]["mmlu200"]["path"])
        self.current_deltas={}; self.current_adapter=None
        self.u={}; self.u_detail={}; self.start=time.monotonic() if start is None else start; self.peak=0; self.memory=[]
        self.unit_times={"recipe_setup_seconds":[],"closedform_arm_seconds":[],"oracle_arm_seconds":[]}
        self.wrapper=OracleEdit(H,self.assert_base,self.apply_adapter)
        self.original=H.my_edit
        # The closed form returns norms only. Observe its original float32 upd at the documented
        # application line, without changing the function object or the solve (prereg:43,225,236).
        self.wrapper.ORIGINAL_MY_EDIT=self.original
        H.my_edit=self.wrapper

    def band_hash(self):
        params=dict(self.H.model.named_parameters())
        return {str(l):hashlib.sha256(params[self.H.weight_name(self.hp,l)].detach().contiguous().cpu().numpy().tobytes()).hexdigest() for l in R.BAND}

    def assert_base(self):
        R.require(self.band_hash()==self.base_hash,"LAW#5(iii): band not restored to process-start base")

    def guard(self,label):
        self.torch.mps.synchronize()
        R.check_eval_seconds(time.monotonic()-self.start)
        n=int(self.torch.mps.driver_allocated_memory()); self.peak=max(n,self.peak)
        self.memory.append({"stage":label,"driver_bytes":n})
        R.check_driver_bytes(n)

    def restore(self):
        self.H.restore_layers(self.hp,self.base); self.assert_base()

    def apply_adapter(self,adapter,hp):
        import c10w_oracle_train as T
        torch=self.torch; H=self.H
        R.require(hp.layers==list(R.BAND),"adapter/hparams layer mismatch")
        if adapter["zero"]:
            tensors={"layers":torch.tensor(list(R.BAND)),"scale":torch.tensor(1.)}
            for l in R.BAND:
                tensors["A_"+str(l)]=torch.zeros(16,11008,dtype=torch.float32)
                tensors["B_"+str(l)]=torch.zeros(2048,16,dtype=torch.float32)
        else:
            R.verify_ref(adapter["train"]["adapter"])
            tensors=T.load_adapter(adapter["train"]["adapter"]["path"])
        R.require(tensors["layers"].tolist()==hp.layers and float(tensors["scale"])==1.,"adapter layer association/scale mismatch")
        self.current_adapter={**adapter,"tensors":tensors}; self.current_deltas={}
        norms={}; params=dict(H.model.named_parameters())
        for layer in hp.layers:
            A,B=tensors["A_"+str(layer)],tensors["B_"+str(layer)]
            rank=16 if adapter["zero"] else adapter["train"]["rank"]
            R.require(A.dtype==B.dtype==torch.float32 and tuple(A.shape)==(rank,11008) and tuple(B.shape)==(2048,rank),"adapter A/B shape/dtype")
            R.require(bool(torch.isfinite(A).all()) and bool(torch.isfinite(B).all()),"non-finite adapter tensors")
            delta=(B@A)*float(tensors["scale"])
            weight=params[H.weight_name(hp,layer)]
            R.require(delta.device.type=="cpu" and tuple(delta.shape)==tuple(weight.shape),"delta/weight shape")
            self.current_deltas[layer]=delta
            before=float(weight.detach().float().norm()); norm=float(delta.norm())
            d16=delta.to(weight.device,weight.dtype)
            with torch.no_grad(): weight.copy_(torch.where(d16==0,weight,weight+d16))
            norms[str(layer)]={"delta_norm":norm,"weight_norm_before":before,"relative_delta_norm":norm/max(before,1e-12)}
            self.guard("merge-"+str(layer))
        return norms

    def frame(self,template,values):
        firsts={self.H.tgt_ids(v)[0] for v in values.values()}
        rows=[]
        for subject in S.source_constants(R.ROOT)["frame_subjects"]:
            p=self.H.predict(template.format(subject))
            rows.append({"subj":subject,"top1":p["id"],"tok":p["tok"],"flip":p["id"] in firsts})
        return {"n":6,"flips":sum(r["flip"] for r in rows),"rows":rows}

    def relation_top1(self):
        return {key:[self.H.predict(subject+suffix)["id"] for subject in self.H.FICTION]
                for key,suffix in (("is_a"," is a"),("associated_with"," is associated with"))}

    def score_mmlu(self):
        torch=self.torch; H=self.H
        mapping=self.mmlu["answer_mapping"]
        candidates=[mapping[c]["token_id"] for c in "ABCD"]
        rows=[]
        for i,item in enumerate(self.mmlu["items"]):
            R.require(H.tok(item["prompt"])["input_ids"]==item["prompt_ids"] and R.sha_text(item["prompt"])==item["prompt_utf8_sha256"],"INVALID-INSTRUMENT: frozen MMLU prompt/token ids")
            ids=torch.tensor([item["prompt_ids"]],device="mps")
            with torch.no_grad(): scores=H.model(ids).logits[0,-1,candidates].float()
            R.require(bool(torch.isfinite(scores).all()),"INVALID-INSTRUMENT: non-finite answer logits")
            predicted=int(scores.argmax())
            rows.append({"source_index":item["source_index"],"predicted":"ABCD"[predicted],"correct":predicted==item["answer"]})
            self.guard("mmlu-"+str(i))
        correct=[r["correct"] for r in rows]
        base=self.u.get(R.A7,{}).get("extra",{}).get("mmlu",{}).get("correct",correct)
        lost=sum(p and not q for p,q in zip(base,correct)); gained=sum(not p and q for p,q in zip(base,correct))
        return {"n":200,"rows":rows,"predicted":[r["predicted"] for r in rows],"correct":correct,
                "correct_n":sum(correct),"accuracy":sum(correct)/200.,"correct_to_wrong":lost,"wrong_to_correct":gained,"net_paired_loss":lost-gained}

    def modifier_hit(self,subject,head_ids,modifier_ids):
        torch=self.torch; H=self.H
        prefix=H.tok(H.CANON.format(subject))["input_ids"]+head_ids
        hits=[]
        with torch.no_grad():
            for i,target in enumerate(modifier_ids):
                ids=torch.tensor([prefix+modifier_ids[:i]],device="mps")
                hits.append(int(H.model(ids).logits[0,-1].argmax())==target)
        return int(all(hits))

    def bigram(self,values):
        H=self.H; rows=[]; frames=S.source_constants(R.ROOT)["frame_subjects"]
        for i,subject in enumerate(H.FICTION):
            value=values[subject]
            if value not in self.maps[R.A7].values():
                rows.append({"subj":subject,"eligible":False,"reason":"not a coined two-word value"}); continue
            split=next(x for x in self.step["head_modifier_splits"].values() if x["head"]+" "+x["modifier"]==value)
            if not split["eligible"]:
                rows.append({"subj":subject,"eligible":False,"reason":"head/modifier token concatenation"}); continue
            h,m=split["head_ids"],split["modifier_ids"]
            never=[self.modifier_hit(s,h,m) for s in frames]
            rows.append({"subj":subject,"eligible":True,"c":self.modifier_hit(subject,h,m),
                         "s":self.modifier_hit(H.FICTION[(i+1)%24],h,m),"b":self.modifier_hit(H.FICTION[(i+12)%24],h,m),
                         "n":sum(never)/6.,"never_hits":never})
            self.guard("bigram-"+str(i))
        eligible=sum(r["eligible"] for r in rows)
        result={"eligible_n":eligible,"excluded_n":24-eligible,"rows":rows}
        result["qualifier"]=R.bigram_qualifier(result)
        return result

    def continuations(self,values):
        torch=self.torch; H=self.H
        contains=[]; generated=[]; sibling_count=0; misses=0
        for subject in H.FICTION:
            ids_target=H.tgt_ids(values[subject]); n=len(ids_target); hits=[]
            for template in H.PTEST:
                prompt=H.tok(template.format(subject))["input_ids"]
                cur=torch.tensor([prompt],device="mps"); gen=[]
                with torch.no_grad():
                    for _ in range(n+2):
                        nxt=int(H.model(cur).logits[0,-1].argmax()); gen.append(nxt)
                        cur=torch.cat((cur,torch.tensor([[nxt]],device="mps")),dim=1)
                text=H.tok.decode(gen); hit=" "+values[subject] in text
                full=gen[:n]==ids_target
                siblings=[s for s,v in values.items() if s!=subject and not full and gen[:len(H.tgt_ids(v))]==H.tgt_ids(v)]
                sibling_count+=bool(siblings); misses+=not full
                hits.append(hit); generated.append({"subj":subject,"template":template,"ids":gen,"text":text,"contains":hit,"full":full,"sibling_subjects":siblings})
            contains.append(hits)
            self.guard("continuations-"+subject)
        return {"contains_n":sum(sum(r) for r in contains),"contains_hits":contains,"generated":generated,
                "sibling":{"misses":misses,"emissions":sibling_count}}

    def probes(self,values):
        H=self.H
        relation=self.relation_top1(); baseline=getattr(self,"relation_base",relation)
        relations={k:{"n":24,"pre":baseline[k],"post":v,"flips":sum(a!=b for a,b in zip(baseline[k],v))} for k,v in relation.items()}
        return {"frames":{"canon":self.frame(H.CANON,values),"train":[self.frame(t,values) for t in S.TEMPLATES],
                          "heldout":[self.frame(t,values) for t in H.PTEST]},
                "relations":relations,"mmlu":self.score_mmlu(),"bigram":self.bigram(values),**self.continuations(values)}

    def evaluate_map(self,values,axes_pre,desc_pre):
        H=self.H
        arm=H.eval_arm(values); rows=arm.pop("rows")
        prompts=[s+" is described as" for s in H.FICTION]
        arm["locality_described_as"]=H.locpct({p:H.predict(p) for p in prompts},desc_pre,prompts)
        arm["locality_axes"]=H.axes_post(axes_pre,list(values.values()))
        arm["extra"]=self.probes(values)
        R.require(arm["para_string_n"]>=arm["para_full_n"],"para_string_n < para_full_n")
        self.guard("map-complete")
        return arm,rows

    def unedited(self):
        H=self.H; tick=time.monotonic(); self.assert_base()
        H.ARMS={k:self.maps[k] for k in (R.A1,R.A2,R.A7,R.SHUF)}
        self.stimulus=stimulus=H.pre_base_report()
        R.require(all(s["base"]<=3 for s in stimulus.values()),"stimulus canonical leak >15%")
        self.axes_base=H.axes_pre()
        self.desc_base={s+" is described as":H.predict(s+" is described as") for s in H.FICTION}
        self.relation_base=self.relation_top1()
        for name,values in H.ARMS.items():
            self.u[name],self.u_detail[name]=self.evaluate_map(values,self.axes_base,self.desc_base)
        R.require(self.u[R.A7]["para_full_n"]<=2,"U A7 held-out leak >2/72")
        self.unit_times["u_seconds"]=time.monotonic()-tick
        return stimulus

    def null(self):
        tick=time.monotonic(); H=self.H; self.restore()
        self.wrapper.mode="oracle"; self.wrapper.null_application=True
        self.wrapper.registry={request_key(self.maps[R.A7]):{"zero":True}}
        self.wrapper(self.hp,[H.req(H.CANON,s,v) for s,v in self.maps[R.A7].items()],None,None)
        self.null_evidence={"base_hash":self.base_hash,"after_hash":self.band_hash()}
        self.assert_base()
        arm,rows=self.evaluate_map(self.maps[R.A7],self.axes_base,self.desc_base)
        self.null_evidence.update(arm=arm,rows=rows)
        proof=compare_null(self.u[R.A7],arm,self.u_detail[R.A7],rows)
        self.null_evidence.update(proof)
        self.restore(); self.wrapper.null_application=False; self.wrapper.null_passed=True
        self.unit_times["null_seconds"]=time.monotonic()-tick
        return self.null_evidence

    def geometry(self,hp,P):
        torch=self.torch; H=self.H; params=dict(H.model.named_parameters()); result={}
        for i,layer in enumerate(hp.layers):
            delta=self.current_deltas[layer].detach().cpu()
            C=H.get_cov(H.model,H.tok,hp.rewrite_module_tmp.format(layer),hp.mom2_dataset,hp.mom2_n_samples,hp.mom2_dtype).cpu()
            # Transfer first, cast second: float64 never reaches MPS.
            d=delta.double(); cov=C.double()
            trace=float(((d@cov)*d).sum())
            norm=float(delta.norm()); projected=float((delta@P[i].cpu().float()).square().sum())
            observed=params[H.weight_name(hp,layer)].detach().cpu().float()-self.base[layer].detach().cpu().float()
            error=float((observed-delta).norm())/norm if norm else 0.
            result[str(layer)]={"delta_norm":norm,"trace_delta_cov_deltaT":trace,
                                "null_cov_share":projected/(norm*norm) if norm else None,"application_relative_error":error,
                                "delta_sha256":hashlib.sha256(delta.contiguous().numpy().tobytes()).hexdigest()}
            del C,d,cov,delta,observed
            self.guard("geometry-"+str(layer))
        return result

    def mounted(self,values,adapter):
        torch=self.torch; H=self.H; handles=[]; self.restore()
        try:
            t=adapter["tensors"]
            for layer in R.BAND:
                A=t["A_"+str(layer)].to("mps"); B=t["B_"+str(layer)].to("mps")
                def mount(module,args,output,A=A,B=B):
                    delta=torch.nn.functional.linear(torch.nn.functional.linear(args[0].float(),A),B)
                    return output+delta.to(output.dtype)
                handles.append(H.model.model.layers[layer].mlp.down_proj.register_forward_hook(mount))
            with torch.no_grad(): result=H.eval_arm(values)
            result["para_string_n"]>=result["para_full_n"] or R.require(False,"mounted para_string_n < para_full_n")
            self.guard("mounted")
            return result
        finally:
            for handle in handles: handle.remove()
            self.restore()
            R.require(not any(H.model.model.layers[l].mlp.down_proj._forward_hooks for l in R.BAND),"mounted hook did not detach")

    def run_recipe(self,name,arms,records):
        H=self.H; self.restore(); oracle=name!="closedform"
        self.wrapper.mode="oracle" if oracle else "closedform"; self.wrapper.registry={}
        H.ARMS={k:self.maps[R.A7 if k==R.CANON_ARM else k] for k in arms}
        for arm,tr in records.items():
            key=request_key(H.ARMS[arm])
            R.require(key not in self.wrapper.registry,"adapter request set collision within recipe")
            self.wrapper.registry[key]={"zero":False,"train":tr}
        tick=time.monotonic(); arm_start=None
        captured={}
        previous_trace=sys.gettrace()
        def trace(frame,event,arg):
            if frame.f_code is self.original.__code__ and event=="line" and frame.f_lineno==216 and not H._LAW5_DEFAULT_CTX:
                captured[frame.f_locals["layer"]]=frame.f_locals["upd"].detach().cpu().clone()
            return trace
        def hook(arm_name,values):
            nonlocal arm_start
            # run_recipe's hook executes while the merged weights remain applied.
            if not oracle: self.current_deltas=captured.copy(); self.current_adapter=None
            x=self.probes(values)
            x["geometry"]=self.geometry(H._ARM_STATE["hp"],H._ARM_STATE["P"])
            if arm_name==R.SHUF:
                cross=H.eval_arm(self.maps[R.A7]); x["cross_score"]={k:v for k,v in cross.items() if k!="rows"}
                x["cross_detail"]=cross["rows"]
            if oracle: x["mounted"]=self.mounted(values,self.current_adapter)
            elapsed=time.monotonic()-(arm_start if arm_start is not None else tick)
            self.unit_times["oracle_arm_seconds" if oracle else "closedform_arm_seconds"].append(elapsed)
            arm_start=time.monotonic(); self.guard("hook-complete")
            return x
        # Observe setup end at the actual recipe arm loop; keep compute_P and LAW5 calls intact.
        def recipe_trace(frame,event,arg):
            nonlocal arm_start
            if frame.f_code is not self.original.__code__ and frame.f_code is not H.run_recipe.__code__:
                return None
            trace(frame,event,arg)
            if frame.f_code is H.run_recipe.__code__ and event=="line" and frame.f_lineno==471:
                self.unit_times["recipe_setup_seconds"].append(time.monotonic()-tick)
                arm_start=time.monotonic()
            return recipe_trace
        H.ARM_HOOKS[:]=[hook]
        sys.settrace(recipe_trace)
        try:
            rec=H.run_recipe(name,H.HP_BASE)
            R.require(rec.get("law5_gate",{}).get("ok") is True and "invalid" not in rec,"LAW#5(i) recipe failed")
            self.assert_base(); rec.update(restored=True,wall_seconds=time.monotonic()-tick,band_after_hash=self.band_hash())
            self.guard("recipe-return")
            return rec
        finally:
            sys.settrace(previous_trace); H.ARM_HOOKS[:]=[]
            self.restore(); self.current_deltas={}; self.current_adapter=None


def unit_for_recipe(name,arm):
    return (arm,1 if name in ("oracle_s1","oracle_canon_s1","oracle_r64_s1") else 0,
            64 if name.startswith("oracle_r64") else 16,name=="oracle_s0rt")


def diagnostic_values(value):
    """Keep non-finite failed readouts as text without weakening science JSON checks."""
    if isinstance(value,float) and not math.isfinite(value): return repr(value)
    if isinstance(value,dict): return {k:diagnostic_values(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [diagnostic_values(v) for v in value]
    return value


def run_eval(phase,directory,step0_directory):
    start=time.monotonic()
    R.entry_preflight(); directory=Path(directory).resolve(); step0_directory=Path(step0_directory).resolve()
    step=R.load_frozen(step0_directory); provenance=R.frozen_provenance(step)
    preflight=phase=="preflight"
    records=[] if preflight else R.phase_trains(directory,phase)
    if not preflight:
        import c10w_oracle_train as T
        proof=R.load_json(directory/"preflight.json")
        T.require_training_preflight(proof,R.sha_file(step0_directory/"step0.json"),provenance)
        R.require(all(t["provenance"]==provenance for t in records),"adapter frozen provenance mismatch before model load")
        if phase in ("P2","P3"):
            p1=Path(proof["p1_directory"])
            R.verify_ref(proof["authorization"])
            R.require_authorization(phase,R.load_json(proof["authorization"]["path"]),R.sha_file(p1/"eval.json"),R.sha_file(p1/"verdict.json"),proof["authorized_projection_minutes"])
    fp=S.fingerprint()
    H=e=None; original_my_edit=None; hooks=None
    stimulus={}; null={}; recipes={}
    record={"phase":"P1" if preflight else phase,"status":"HALT","provenance":provenance,
            "step0_directory":str(step0_directory),"fingerprint":fp,"train_records":records,
            "u":{},"u_detail":{},"stimulus":stimulus,"law5_null":null,"recipes":recipes}
    try:
        H=S.load_harness()
        original_my_edit=getattr(H,"my_edit",None)
        hooks=list(H.ARM_HOOKS) if hasattr(H,"ARM_HOOKS") else None
        import torch
        e=Evaluator(H,step,directory,start)
        e.guard("model-loaded")
        stimulus=e.unedited(); null=e.null()
        closed=e.run_recipe("closedform",(R.A1,R.A2,R.A7),{})
        recipes["closedform"]=closed
        R.law3(closed["arms"],e.u,stimulus); e.wrapper.law3_passed=True
        if not preflight:
            for name,arms in R.RECIPES[phase].items():
                selected={arm:next(t for t in records if R.train_identity(t)==unit_for_recipe(name,arm)) for arm in arms}
                recipes[name]=e.run_recipe(name,arms,selected)
        e.assert_base()
        expected=0 if preflight else len(R.TRAIN_UNITS[phase])
        R.require(e.wrapper.zero_hits==1 and e.wrapper.trained_hits==expected,"LAW#5(v): process hit counter mismatch")
        for name,rec in recipes.items():
            for arm,a in rec["arms"].items():
                R.validate_arm(a,rec["detail"][arm],name!="closedform")
        cf=sum(x["delta_norm"] for x in closed["delta_norms"][R.A7].values())
        R.require(cf>0,"write-size reference norm is zero")
        for rec in recipes.values():
            for arm in rec["arms"].values():
                arm["extra"]["write_size_ratio_to_closedform_A7"]=sum(x["delta_norm"] for x in arm["extra"]["geometry"].values())/cf
        record={"phase":"P1" if preflight else phase,"status":"PASS","environment":S.model_environment(H,"float16"),
                "step0_directory":str(step0_directory),"provenance":provenance,"fingerprint":fp,
                "validity":{k:True for k in ("fingerprint","seal","instrument","hashes","entry","seam")},
                "u":e.u,"u_detail":e.u_detail,"stimulus":stimulus,"law5_null":null,
                "recipes":recipes,"delegation_identity":e.original is e.wrapper.ORIGINAL_MY_EDIT,
                "zero_adapter_hits":e.wrapper.zero_hits,"trained_oracle_hits":e.wrapper.trained_hits,
                "expected_zero_hits":1,"expected_trained_hits":expected,"base_band_hash":e.base_hash,
                "final_band_hash":e.band_hash(),"train_records":records,"sampled_peak_driver_bytes":e.peak,
                "memory_samples":e.memory,"cpu_process_peak_rss_bytes":int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                "wall_seconds":time.monotonic()-e.start,"measured_raw_units":e.unit_times}
        if preflight:
            R.write_json(directory/"preflight_eval.json",record)
            # The trainer receives this minimal certificate; no held-out prompt bytes enter its process.
            certificate={"phase":"P1","status":"PASS","law3":True,"law5_null":True,"fingerprint":True,
                         "step0_sha256":R.sha_file(step0_directory/"step0.json"),"provenance":provenance,
                         "step0_directory":str(step0_directory),"evaluation":R.file_ref(directory/"preflight_eval.json"),
                         **R.preflight_evidence(R.load_json(directory/"preflight_eval.json")),
                         "wall_seconds":record["wall_seconds"]}
            R.write_json(directory/"preflight.json",certificate)
        else:
            # Attach exact attempt-record hashes after loading; the reader verifies files again.
            for tr in records:
                tr["record_file"]=R.file_ref(directory/"train"/(R.train_tag(R.train_identity(tr),tr["steps"])+".json"))
            record["measured_units"]={key:max(value) if isinstance(value,list) else value for key,value in e.unit_times.items()}
            attempts=[R.load_json(p) for p in (directory/"train").glob("*.json")]
            record["measured_units"]["training400_seconds"]=max(t["wall_seconds"]*400/t["steps"] for t in attempts)
            if phase in ("P2","P3"):
                record.update(authorization=proof["authorization"],authorized_projection_minutes=proof["authorized_projection_minutes"],
                              p1_eval_sha256=R.sha_file(Path(proof["p1_directory"])/"eval.json"))
            if phase=="P2":
                import c10w_oracle_train as T
                p1=Path(proof.get("p1_directory",str(R.latest_directory("p1"))))
                original=next(t for t in R.phase_trains(p1,"P1") if t["arm"]==R.A7)
                retrained=next(t for t in records if t["arm"]==R.A7 and t["retrain"])
                x,y=T.load_adapter(original["adapter"]["path"]),T.load_adapter(retrained["adapter"]["path"])
                cosines={}
                for l in R.BAND:
                    a=(x["B_"+str(l)]@x["A_"+str(l)]).flatten()
                    b=(y["B_"+str(l)]@y["A_"+str(l)]).flatten()
                    denom=float(a.norm()*b.norm())
                    R.require(denom>0,"same-seed cosine has zero denominator")
                    cosines[str(l)]=float(torch.dot(a,b))/denom
                initial_arm=R.load_json(p1/"eval.json")["recipes"]["oracle_p1"]["arms"][R.A7]
                repeated_arm=recipes["oracle_s0rt"]["arms"][R.A7]
                agreement=[]
                for a,b in zip(initial_arm["extra"]["generated"],repeated_arm["extra"]["generated"]):
                    R.require((a["subj"],a["template"])==(b["subj"],b["template"]),"same-seed prompt ordering mismatch")
                    n=len(H.tgt_ids(e.maps[R.A7][a["subj"]]))
                    agreement.append(a["ids"][:n]==b["ids"][:n])
                R.require(len(agreement)==72,"same-seed prompt denominator mismatch")
                record["same_seed"]={"per_layer_cosine":cosines,"prompt_agreement_n":sum(agreement),"n":72,
                                     "prompt_agreement_hits":agreement,
                                     "count_difference":abs(initial_arm["para_full_n"]-repeated_arm["para_full_n"]),
                                     "steps":[original["steps"],retrained["steps"]]}
                e.guard("same-seed-diagnostics")
            e.guard("evaluation-final")
            record.update(wall_seconds=time.monotonic()-e.start,sampled_peak_driver_bytes=e.peak)
            R.write_json(directory/"eval.json",record)
            R.validate_phase({**record,"class":R.CLASS,"decision_id":R.DECISION_ID})
            if phase in ("P2","P3"):
                R.write_json(directory/"verdict.json",R.read_measurement(R.disk_phases(Path(proof["p1_directory"]))))
    except Exception as exc:
        record.update(status="HALT",reason=str(exc),wall_seconds=time.monotonic()-start,
                      u=getattr(e,"u",record["u"]),u_detail=getattr(e,"u_detail",record["u_detail"]),
                      stimulus=getattr(e,"stimulus",stimulus),law5_null=getattr(e,"null_evidence",null),recipes=recipes)
        R.write_json(directory/"eval_halt.json",diagnostic_values(record))
        raise
    finally:
        if H is not None:
            if original_my_edit is not None: H.my_edit=original_my_edit
            if hooks is not None: H.ARM_HOOKS[:]=hooks
    print("C10W evaluation PASS controls; oracle measurement, not a route",flush=True)
    return 0


def main():
    parser=argparse.ArgumentParser(description=R.CLASS)
    parser.add_argument("phase",choices=("preflight","P1","P2","P3"))
    parser.add_argument("phase_directory"); parser.add_argument("step0_directory")
    a=parser.parse_args()
    try: return run_eval(a.phase,a.phase_directory,a.step0_directory)
    except Exception as exc:
        print("HALT:",str(exc),file=sys.stderr); return 2


if __name__=="__main__":
    sys.exit(main())
