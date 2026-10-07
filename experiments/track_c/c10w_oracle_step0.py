#!/usr/bin/env python3
"""D-C10w-oracle step0 and one-stage dispatch. Oracle measurement, not a route."""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse
import ast
import difflib
import json
import math
import random
import re
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
import c10w_oracle_read as R

TEMPLATES = (
    "The capital of {} is the city of", "The capital of {} is", "Q: What is the capital of {}? A:",
    "Question: Which city serves as the capital of {}? Answer:", "Capital of {}:",
    "According to the records, the capital of {} is", "In an atlas, the entry for {} lists the capital as",
    "Every map of {} marks the capital as", "Fact: the capital of {} is", "The country {} has the capital",
    "Officially, the capital of {} is", "The national capital of {} is", "The capital of {} is the town of",
    "Most atlases give the capital of {} as", "The official capital of {} is the city of",
    "The capital of {} is located in", "The capital of {} has always been", "Historians agree that the capital of {} is",
    "On the map, the capital of {} appears as", "Geography quiz: the capital of {} is")
RESERVES = ("Textbooks state that the capital of {} is", "Schoolbooks list the capital of {} as")
SYNONYMS = "name named names known call calls refer refers referred title titled visiting visits visitor visitors travel travels traveling travelling traveler travelers traveller travellers go goes going trip tour tourist tourists when whenever once your yours principal chief largest biggest primary leading foremost administrative administration govern governs governed governing governmental parliament seated sits sit power ruling rule rules".split()


def tokens(text):
    return re.findall(r"subj|'s|[a-z]+",text.lower().replace("{}"," subj "))


def literal_assignment(nodes,name):
    for node in nodes:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            try: return ast.literal_eval(node.value)
            except ValueError: continue
    raise R.Halt("HALT: missing source constant "+name)


def source_constants(root):
    root=Path(root); tree=ast.parse((root/"experiments/track_c/c10e_bandknob.py").read_text())
    build=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="build_stimuli")
    frame=ast.parse((root/"experiments/track_c/c10p_twopass_arms.py").read_text())
    entities=[]
    for name in ("g6_screen_qwen3b.json","g6_screen_qwen3b_v2.json"):
        selected=R.load_json(root/"configs/screens"/name)["selected"]
        entities.extend(selected); entities.extend(x["capital"]["truth"] for x in selected.values())
    return {"canon":literal_assignment(tree.body,"CANON"),"heldout":literal_assignment(tree.body,"PTEST"),
            "fiction":literal_assignment(tree.body,"FICTION"),"heads":literal_assignment(build.body,"coined_head"),
            "modifiers":literal_assignment(build.body,"coined_mod"),"frame_subjects":literal_assignment(frame.body,"FRAME_SUBJECTS"),
            "screen_entities":entities}


def audit_templates(constants,templates,reserves):
    ct=tokens(constants["canon"]); qs=[tokens(q) for q in constants["heldout"]]
    bigrams=lambda t:set(zip(t,t[1:]))
    banned=set(x for q in qs for x in q)-set(ct)
    banned.update(SYNONYMS)
    banned_bigrams=set(b for q in qs for b in bigrams(q))-bigrams(ct)
    names=constants["fiction"]+constants["heads"]+constants["modifiers"]+constants["frame_subjects"]+constants["screen_entities"]
    entity_tokens=set(x.lower() for x in names)
    rows=[]
    for i,template in enumerate([*templates,*reserves]):
        t=tokens(template); tb=bigrams(t)
        ratios=[difflib.SequenceMatcher(None," ".join(t)," ".join(q)).ratio() for q in qs]
        checks={"S1":not set(t)&banned,"S2":not tb&banned_bigrams and t[:2]!=["subj","'s"],
                "S2c":re.search(r"\{\}\s*[,.:;?!—-].*capital",template,re.I) is None,
                "S2d":template.lower().split("{}")[0].split().count("of")<2,
                "S3":all(r<.60 for r in ratios),
                "S4":template.count("{}")==1 and not set(t)&entity_tokens,
                "S5":not tb&{("is","described"),("is","a"),("is","associated")}}
        rows.append({"id":"T%02d"%(i+1) if i<len(templates) else "R%d"%(i-len(templates)+1),
                     "template":template,"checks":checks,"max_s3":max(ratios),"s3":ratios,"ok":all(checks.values())})
    return {"ok":all(r["ok"] for r in rows),"rows":rows,"banned_words":sorted(banned),
            "banned_bigrams":[list(b) for b in sorted(banned_bigrams)]}


def audit_trainer_input(text,trainer_source,heldout):
    normal=" ".join(tokens(text))
    for q in heldout:
        R.require(q not in text and " ".join(tokens(q)) not in text and " ".join(tokens(q)) not in normal,"S6 held-out wording in training inputs")
    R.require("PTEST" not in trainer_source and "c10e_bandknob" not in trainer_source,"S6 trainer source imports held-out harness")


def shuffled_map(subjects,values):
    R.require(len(subjects)==24 and set(subjects)==set(values),"shuffled map subject cardinality")
    shuffled={s:values[subjects[(i+1)%24]] for i,s in enumerate(subjects)}
    R.require(sorted(shuffled.values())==sorted(values.values()),"shuffled map not a permutation")
    for s in subjects:
        a,b=values[s].split(),shuffled[s].split()
        R.require(len(a)==len(b)==2 and all(x!=y for x,y in zip(a,b)),"shuffled map shares a head/modifier or is not a derangement")
    return shuffled


def fingerprint():
    env=dict(os.environ,LLMDB_ROOT=str(R.ROOT))
    p=subprocess.run([str(R.ROOT/".venv/bin/python"),"-B",str(R.ROOT/"tools/engine_fingerprint.py")],
                     cwd=R.ROOT,env=env,capture_output=True,text=True)
    R.require(p.returncode==0 and "engine fingerprint PASS" in p.stdout,"engine fingerprint failed: "+p.stdout+p.stderr)
    return {"ok":True,"output":p.stdout,"engine":R.file_ref(R.ROOT/"memit_dry_run/memit/memit/memit_main.py")}


def model_environment(H,dtype):
    R.require(H.ID==R.MODEL_ID and H.REV==R.MODEL_REV and H.model.config._commit_hash==R.MODEL_REV,"INVALID-ENVIRONMENT: model revision")
    R.require(str(H.DEV)=="mps" and all(p.device.type=="mps" and str(p.dtype)=="torch."+dtype for p in H.model.parameters()),"INVALID-ENVIRONMENT: actual device/dtype")
    hp=H.MEMITHyperParams.from_json(H.HP_BASE)
    R.require(hp.layers==list(R.BAND) and hp.rewrite_module_tmp=="model.layers.{}.mlp.down_proj","band configuration mismatch")
    return {"model_id":H.ID,"model_revision":H.model.config._commit_hash,"layers":hp.layers,"dtype":dtype,"device":"mps"}


def load_harness():
    R.entry_preflight()
    import torch
    R.require(torch.backends.mps.is_available(),"INVALID-ENVIRONMENT: MPS required")
    os.environ["LLMDB_ROOT"]=str(R.ROOT)
    os.environ["LLMDB_DEVICE"]="mps"
    import c10e_bandknob as H
    model_environment(H,"float16")
    return H


def s7_record():
    text=(R.ROOT/"docs/C10W_ORACLE_PREREG.md").read_text()
    verdicts=[]
    for match in re.finditer(r"^\| (T\d\d|R[12]) \| ACCEPT \| (.+) \|$",text,re.M):
        verdicts.append({"id":match[1],"verdict":"ACCEPT","reason":match[2]})
    R.require(len(verdicts)==22 and len({v["id"] for v in verdicts})==22,"S7 adjudications incomplete")
    return {"model":"GPT-6-Astra","effort":"high","judgments":verdicts,"rejected_ids":[],"substitutions":[],
            "historical_rejections":[{"id":k,"reason":why} for k,why in (("v1 T06","S2c Q2 shape"),("v1 T09","S2d Q3 shape"),("v1 T14","S2c Q2 shape"),("v1 R1","S2d Q3 shape"))],
            "source":"docs/C10W_ORACLE_PREREG.md:139-164"}


def nonzero_seam():
    import torch
    import c10w_oracle_train as T
    results=[]
    LoRA=T.lora_class(torch)
    for rank in (16,64):
        torch.manual_seed(20261007+rank)
        base=torch.nn.Linear(11008,2048,bias=False,dtype=torch.float32,device="cpu")
        wrappers={l:LoRA(base,rank) for l in R.BAND}
        with torch.no_grad():
            for wrapper in wrappers.values():
                wrapper.A.copy_(torch.randn_like(wrapper.A)*.01)
                wrapper.B.copy_(torch.randn_like(wrapper.B)*.01)
        x=torch.randn(2,11008,dtype=torch.float32)*.01
        with tempfile.TemporaryDirectory(prefix="c10w-seam-") as td:
            p=Path(td)/"seam.safetensors"
            tensors=T.adapter_tensors(torch,wrappers)
            T.save_adapter(p,tensors,{"rank":rank,"class":R.CLASS,"decision_id":R.DECISION_ID})
            loaded=T.load_adapter(p)
            R.require(loaded["layers"].tolist()==list(R.BAND) and float(loaded["scale"])==1.,"INVALID-SEAM: scale/layers")
            comparisons={}
            for layer,wrapper in wrappers.items():
                with torch.no_grad():
                    output=wrapper(x)
                    ref=torch.nn.functional.linear(x,base.weight+loaded["scale"]*(loaded["B_"+str(layer)]@loaded["A_"+str(layer)]))
                error=float((output-ref).abs().max()); limit=1e-5*max(1.,float(ref.abs().max()))
                R.require(error<=limit and torch.equal(loaded["A_"+str(layer)],wrapper.A.cpu())
                          and torch.equal(loaded["B_"+str(layer)],wrapper.B.cpu()),"INVALID-SEAM: nonzero wrapper/serialization parity")
                comparisons[str(layer)]={"max_abs_error":error,"limit":limit,"ok":True}
            results.append({"rank":rank,"input_shape":list(x.shape),"weight_shape":[2048,11008],"A_shape":list(wrapper.A.shape),
                            "B_shape":list(wrapper.B.shape),"scale":1.,"layers":list(R.BAND),"adapter_sha256":R.sha_file(p),
                            "tensor_hashes":{k:T.tensor_sha(t) for k,t in loaded.items()},"per_layer":comparisons,
                            "max_abs_error":max(c["max_abs_error"] for c in comparisons.values()),"ok":True})
        del wrapper,wrappers,base,x,output,ref,loaded,tensors
    return {"ok":True,"ranks":results,"device":"cpu","dtype":"float32"}


def freeze_mmlu(tok):
    from huggingface_hub import HfApi
    from datasets import load_dataset
    revision=HfApi().dataset_info("cais/mmlu").sha
    R.require(re.fullmatch(r"[0-9a-f]{40}",revision) is not None,"INVALID-INSTRUMENT: immutable dataset commit")
    datasets={s:load_dataset("cais/mmlu","all",split=s,revision=revision) for s in ("test","dev")}
    test,dev=datasets["test"],datasets["dev"]
    R.require(len(test)>=200,"INVALID-INSTRUMENT: test split too small")
    def checked(row):
        R.require(set(row)>={"subject","question","choices","answer"} and isinstance(row["subject"],str) and isinstance(row["question"],str)
                  and len(row["choices"])==4 and all(isinstance(c,str) for c in row["choices"])
                  and type(row["answer"]) is int and 0<=row["answer"]<=3,"INVALID-INSTRUMENT: MMLU schema")
        return {k:row[k] for k in ("subject","question","choices","answer")}
    identities={}
    for name,data in datasets.items():
        identities[name]=[{"source_index":i,"row_sha256":R.sha_text(json.dumps(checked(row),sort_keys=True,ensure_ascii=False))} for i,row in enumerate(data)]
    letters="ABCD"; ids=[tok(" "+c,add_special_tokens=False)["input_ids"] for c in letters]
    R.require(all(len(i)==1 for i in ids) and len({i[0] for i in ids})==4,"INVALID-INSTRUMENT: distinct single-token answer letters")
    by_subject={}
    for i,row in enumerate(dev): by_subject.setdefault(row["subject"],[]).append((i,checked(row)))
    def item_text(row,answer=False):
        return row["question"]+"\n"+"\n".join(c+". "+v for c,v in zip(letters,row["choices"]))+"\nAnswer:"+(" "+letters[row["answer"]]+"\n\n" if answer else "")
    sampled=random.Random(20261007).sample(range(len(test)),200); items=[]
    for index in sampled:
        row=checked(test[index]); examples=by_subject[row["subject"]]
        R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
        prompt="The following are multiple choice questions (with answers) about "+row["subject"].replace("_"," ")+".\n\n"
        prompt+="".join(item_text(r,True) for _,r in examples)+item_text(row)
        prompt_ids=tok(prompt)["input_ids"]
        R.require(prompt.endswith("Answer:") and all(tok(prompt+" "+c)["input_ids"]==prompt_ids+token for c,token in zip(letters,ids)),"INVALID-INSTRUMENT: Answer suffix token concatenation")
        items.append({**row,"source_index":index,"source_identity":identities["test"][index],
                      "dev_identities":[identities["dev"][i] for i,_ in examples],"dev_examples":[r for _,r in examples],
                      "prompt":prompt,"prompt_utf8_sha256":R.sha_text(prompt),"prompt_ids":prompt_ids})
    files={s:[R.file_ref(c["filename"]) for c in data.cache_files] for s,data in datasets.items()}
    R.require(all(files.values()),"INVALID-INSTRUMENT: missing source file provenance")
    return {"dataset":"cais/mmlu","config":"all","revision":revision,"split_counts":{s:len(d) for s,d in datasets.items()},
            "source_identities":identities,"source_files":files,"sample_seed":20261007,"sampled_indices":sampled,
            "answer_mapping":{c:{"index":i,"token_id":ids[i][0]} for i,c in enumerate(letters)},
            "token_checks":{"distinct_single_tokens":True,"answer_suffix_concatenation":True},"items":items}


def run_step0(directory):
    R.entry_preflight(); start=time.monotonic()
    proof=fingerprint(); H=load_harness(); env=model_environment(H,"float16")
    constants=source_constants(R.ROOT)
    R.require(H.CANON==constants["canon"] and H.PTEST==constants["heldout"] and H.FICTION==constants["fiction"],"harness/source constant mismatch")
    maps=H.build_stimuli(); maps[R.SHUF]=shuffled_map(H.FICTION,maps[R.A7])
    targets={key:{s:H.tgt_ids(v) for s,v in values.items()} for key,values in maps.items()}
    splits={}
    for subject,value in maps[R.A7].items():
        head,modifier=value.split(); head_ids=H.tgt_ids(head); modifier_ids=H.tgt_ids(modifier)
        full=targets[R.A7][subject]
        eligible=full==head_ids+modifier_ids
        splits[subject]={"head":head,"modifier":modifier,"head_ids":head_ids,"modifier_ids":modifier_ids,"eligible":eligible}
    inputs={"templates":list(TEMPLATES),"fiction":H.FICTION,"value_maps":maps,"target_ids":targets,
            "prompt_ids":{str(i):{s:H.tok(t.format(s))["input_ids"] for s in H.FICTION} for i,t in enumerate(TEMPLATES)}}
    input_text=json.dumps({**inputs,"class":R.CLASS,"decision_id":R.DECISION_ID},ensure_ascii=False,indent=2)+"\n"
    audit_trainer_input(input_text,(R.ROOT/"experiments/track_c/c10w_oracle_train.py").read_text(),H.PTEST)
    audit=audit_templates(constants,TEMPLATES,RESERVES)
    R.require(audit["ok"] and R.sha_text("\n".join(TEMPLATES))==R.TEMPLATE_SHA,"seal audit differs from frozen list")
    expected=[.469,.551,.492,.466,.444,.426,.523,.480,.514,.551,.486,.538,.469,.457,.425,.540,.462,.444,.477,.459,.422,.474]
    R.require([round(r["max_s3"],3) for r in audit["rows"]]==expected,"S3 audit differs from frozen table")
    s7=s7_record(); audit.update(S6=True,S7=s7,template_sha256=R.TEMPLATE_SHA,reserve_sha256=R.sha_text("\n".join(RESERVES)))
    R.write_json(directory/"train_inputs.json",inputs)
    audit_trainer_input((directory/"train_inputs.json").read_text(),(R.ROOT/"experiments/track_c/c10w_oracle_train.py").read_text(),H.PTEST)
    R.write_json(directory/"seal_audit.json",audit)
    mmlu=freeze_mmlu(H.tok); R.write_json(directory/"mmlu200.json",mmlu)
    proof=fingerprint(); seam=nonzero_seam()
    source_paths={"trainer":R.ROOT/"experiments/track_c/c10w_oracle_train.py",
                  "evaluator":R.ROOT/"experiments/track_c/c10w_oracle_eval.py",
                  "reader":R.ROOT/"experiments/track_c/c10w_oracle_read.py",
                  "step0_source":Path(__file__).resolve(),"harness":R.ROOT/"experiments/track_c/c10e_bandknob.py",
                  "hparams":R.ROOT/"configs/hparams/qwen25_3b_memit_hparams.json",
                  "frame_source":R.ROOT/"experiments/track_c/c10p_twopass_arms.py",
                  "g6_screen":R.ROOT/"configs/screens/g6_screen_qwen3b.json",
                  "g6_screen_v2":R.ROOT/"configs/screens/g6_screen_qwen3b_v2.json",
                  "fingerprint_source":R.ROOT/"tools/engine_fingerprint.py",
                  "prereg":R.ROOT/"docs/C10W_ORACLE_PREREG.md"}
    snapshot=R.ROOT/"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots"/R.MODEL_REV
    for name in ("config.json","tokenizer.json","tokenizer_config.json","vocab.json","merges.txt","model.safetensors.index.json"):
        R.require((snapshot/name).is_file(),"missing model/tokenizer provenance: "+name)
        source_paths[name]=snapshot/name
    record={"status":"PASS","environment":env,"prereg_sha256":R.PREREG_SHA,"template_hashes":[R.sha_text(t) for t in TEMPLATES],
            "heldout_template_hashes":[R.sha_text(t) for t in H.PTEST],"fingerprint":proof,"seam":seam,
            "instrument_ok":True,"seal":{k:True for k in ("S1","S2","S2c","S2d","S3","S4","S5","S6","S7")},
            "head_modifier_splits":splits,"bigram_eligible_n":sum(s["eligible"] for s in splits.values()),
            "bigram_excluded_n":sum(not s["eligible"] for s in splits.values()),
            "files":{key:R.file_ref(directory/(key+".json")) for key in ("train_inputs","seal_audit","mmlu200")},
            "sources":{key:R.file_ref(path) for key,path in source_paths.items()},"wall_seconds":time.monotonic()-start}
    R.write_json(directory/"step0.json",record)
    return 0


def new_phase(phase):
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    directory=R.fresh_directory(R.ROOT/"results/c10w_oracle"/(phase.lower()+"_"+stamp))
    if phase!="step0":
        (directory/"train").mkdir(); (directory/"adapters").mkdir()
    return directory


def run_child(script,args,directory,stage):
    log=directory/(stage+".log")
    R.require(not log.exists(),"stage log exists: "+stage)
    with log.open("x") as f:
        proc=subprocess.run([str(R.ROOT/".venv/bin/python"),"-B",str(R.ROOT/"experiments/track_c"/script),*map(str,args)],
                            cwd=R.ROOT,env=dict(os.environ,LLMDB_ROOT=str(R.ROOT)),stdout=f,stderr=subprocess.STDOUT)
        f.write("\nSTAGE_EXIT="+str(proc.returncode)+"\n")
    print("stage",stage,"exit",proc.returncode,"log",log,flush=True)
    return proc.returncode


def train_one(directory,step0,unit,steps,label):
    args=[directory,step0,*unit[:3],steps]+(["--retrain"] if unit[3] else [])
    return run_child("c10w_oracle_train.py",args,directory,label)


def training_projection(phase,proof,completed,pending_overrides):
    normalized=[t["wall_seconds"]*400/t["steps"]/60 for t in completed]
    per400=max([38.,*normalized])
    fitted={R.train_identity(t) for t in completed if t["status"]=="PASS"}
    pending={unit:400 for unit in R.TRAIN_UNITS[phase] if unit not in fitted}
    pending.update(pending_overrides)
    spent=sum(t["wall_seconds"]/60 for t in completed)
    evaluation={"P1":190.,"P2":220.,"P3":175.}[phase]
    preflight=proof["wall_seconds"]/60 if phase=="P1" else 0.
    return preflight+spent+per400*sum(pending.values())/400+evaluation


def guard_training_unit(directory,phase,proof,unit,steps,matched_retry=False):
    completed=[R.load_json(p) for p in (directory/"train").glob("*.json")]
    pending={unit:steps}
    if matched_retry and unit[0] in (R.A7,R.SHUF):
        mate=(R.SHUF if unit[0]==R.A7 else R.A7,*unit[1:])
        if not (directory/"train"/(R.train_tag(mate,800)+".json")).exists(): pending[mate]=800
    projected=training_projection(phase,proof,completed,pending)
    p1=directory if phase=="P1" else Path(proof["p1_directory"])
    auth_path=p1/("authorization_"+phase+".json")
    authorization=R.load_json(auth_path) if auth_path.exists() else {}
    R.check_phase_minutes(phase,projected,authorization.get(phase,{}).get("budget_minutes"))


def ensure_authorized(phase,p1):
    verdict=R.load_json(p1/"verdict.json"); eval_ref=R.file_ref(p1/"eval.json")
    auth_path=p1/("authorization_"+phase+".json")
    R.require(auth_path.is_file(),"missing recorded post-P1 "+phase+" authorization file")
    auth=R.load_json(auth_path); minutes=verdict["projection"][phase+"_minutes"]
    R.require_authorization(phase,auth,eval_ref["sha256"],R.sha_file(p1/"verdict.json"),minutes)
    if phase=="P3":
        reading=R.read_measurement({"P1":R.load_json(p1/"eval.json"),"P2":R.replication_for(p1)})
        R.require(reading["status"]=="INCOMPLETE" and reading["p3_required"],"P3 scientifically excluded/incomplete replication")
    return R.file_ref(auth_path),minutes


def dispatch_stage(stage):
    R.entry_preflight(); R.require(stage in R.stage_names(),"unknown stage")
    if stage=="read": return run_child("c10w_oracle_read.py",[],R.latest_directory("p1"),"read")
    directory=None
    try:
        if stage=="step0":
            directory=new_phase("step0")
            rc=run_child("c10w_oracle_step0.py",["freeze",directory],directory,stage)
            R.require(rc==0,"step0 freeze process failed")
            return 0
        step0=R.latest_directory("step0"); frozen=R.load_frozen(step0)
        phase=stage[:2].upper()
        if stage=="p1-preflight":
            directory=new_phase("P1")
            rc=run_child("c10w_oracle_eval.py",["preflight",directory,step0],directory,stage)
            R.require(rc==0,"P1 preflight process failed")
            return 0
        p1=R.latest_directory("p1")
        authorization=None; projection=None
        if phase in ("P2","P3"):
            authorization,projection=ensure_authorized(phase,p1)
            first=R.TRAIN_STAGES[phase][0]
            if stage==first:
                directory=new_phase(phase)
                cert=R.load_json(p1/"preflight.json")
                cert.update(phase=phase,p1_directory=str(p1),authorization=authorization,authorized_projection_minutes=projection)
                R.write_json(directory/"preflight.json",cert)
            else: directory=R.latest_directory(phase)
        else: directory=p1
        proof=R.load_json(directory/"preflight.json")
        import c10w_oracle_train as T
        T.require_training_preflight(proof,R.sha_file(step0/"step0.json"),R.frozen_provenance(frozen))
        if stage in R.TRAIN_STAGES[phase]:
            index=R.TRAIN_STAGES[phase].index(stage); unit=R.TRAIN_UNITS[phase][index]
            for previous in R.TRAIN_UNITS[phase][:index]:
                paths=[directory/"train"/(R.train_tag(previous,s)+".json") for s in (400,800)]
                records=[R.load_json(p) for p in paths if p.is_file()]
                R.require(records and records[-1]["status"]=="PASS","prior training unit incomplete")
            steps=400
            if unit[0]==R.SHUF:
                mate=(R.A7,*unit[1:])
                if (directory/"train"/(R.train_tag(mate,800)+".json")).exists(): steps=800
            guard_training_unit(directory,phase,proof,unit,steps)
            rc=train_one(directory,step0,unit,steps,stage+("-retry800" if steps==800 else ""))
            if rc==75 and steps==400:
                guard_training_unit(directory,phase,proof,unit,800,matched_retry=True)
                rc=train_one(directory,step0,unit,800,stage+"-retry800")
            R.require(rc==0,"adapter underfit/guard failure after declared attempt(s)")
            # A shuffled retry forces its previously fitted A7 partner to the same final protocol.
            if unit[0]==R.SHUF and (directory/"train"/(R.train_tag(unit,800)+".json")).exists():
                mate=(R.A7,*unit[1:])
                if not (directory/"train"/(R.train_tag(mate,800)+".json")).exists():
                    guard_training_unit(directory,phase,proof,mate,800)
                    rc=train_one(directory,step0,mate,800,stage+"-matched-a7-retry800")
                    R.require(rc==0,"matched A7 800-update attempt failed")
            return 0
        if stage.endswith("-eval"):
            R.phase_trains(directory,phase)
            rc=run_child("c10w_oracle_eval.py",[phase,directory,step0],directory,stage)
            R.require(rc==0,"evaluation process failed")
            return 0
        if stage=="p1-project":
            ev=R.load_json(p1/"eval.json"); R.validate_phase(ev)
            result=R.read_measurement({"P1":ev}); result["projection"]=R.reproject(ev["measured_units"])
            result["stop"]="P1 complete; P2/P3 require separately recorded authorization"
            R.write_json(p1/"verdict.json",result)
            print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
        raise R.Halt("HALT: stage not dispatched")
    except Exception as exc:
        if directory is not None:
            halt={"status":"HALT","stage":stage,"reason":str(exc),"oracle_measurement_not_route":True}
            if not (directory/"HALT.json").exists(): R.write_json(directory/"HALT.json",halt)
            diagnostic=R.ROOT/"architecture_profile"/("c10w_oracle_halt_diagnostic_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")+".json")
            R.write_json(diagnostic,halt)
        raise


def main():
    parser=argparse.ArgumentParser(description=R.CLASS)
    parser.add_argument("action",choices=("dispatch","freeze")); parser.add_argument("value")
    a=parser.parse_args()
    try:
        return dispatch_stage(a.value) if a.action=="dispatch" else run_step0(Path(a.value).resolve())
    except Exception as exc:
        print("HALT:",str(exc),file=sys.stderr); return 2


if __name__=="__main__":
    sys.exit(main())
