#!/usr/bin/env python3
"""D-C10w-oracle frozen-v2.2 reader and record/control boundaries; no model imports."""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse
import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_ID = "D-C10w-oracle"
CLASS = "ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))"
MODEL_ID = "Qwen/Qwen2.5-3B"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
BAND = (4, 5, 6, 7, 8)
TEMPLATE_SHA = "306cb0089dddb066242398c0f03f4d10d67086fbf7b0143f850342906087b272"
PREREG_SHA = "2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344"
FORBIDDEN_ENV = ("C10_KEY_LOCUS", "C10_CTX_TEMPLATES", "C10_ARMS", "N_EDIT", "C10_SUBJECT_OFFSET",
                 "HP_CANDIDATE", "C10_PROJECTOR", "C10_RECIPES", "MODEL_ID", "MODEL_REV", "LLMDB_DEVICE")
PHASE_LIMITS = {"P1": 465, "P2": 448, "P3": 327}
A1, A2, A7, SHUF, CANON_ARM = "A1_single", "A2_coherent2", "A7_coined_coined", "A7_shuf", "A7_canon"
RECIPES = {"P1": {"oracle_p1": (A1,A2,A7,SHUF), "oracle_canon_s0": (CANON_ARM,)},
           "P2": {"oracle_s1": (A1,A7,SHUF), "oracle_s0rt": (A7,SHUF), "oracle_canon_s1": (CANON_ARM,)},
           "P3": {"oracle_r64_s0": (A7,SHUF), "oracle_r64_s1": (A7,SHUF)}}
TRAIN_UNITS = {"P1": ((A1,0,16,False),(A7,0,16,False),(CANON_ARM,0,16,False),(A2,0,16,False),(SHUF,0,16,False)),
               "P2": ((A7,1,16,False),(SHUF,1,16,False),(CANON_ARM,1,16,False),(A1,1,16,False),(A7,0,16,True),(SHUF,0,16,True)),
               "P3": ((A7,0,64,False),(SHUF,0,64,False),(A7,1,64,False),(SHUF,1,64,False))}
TRAIN_STAGES = {"P1": ("p1-a1","p1-a7","p1-canon","p1-a2","p1-shuf"),
                "P2": ("p2-a7-s1","p2-shuf-s1","p2-canon-s1","p2-a1-s1","p2-a7-rt","p2-shuf-rt"),
                "P3": ("p3-a7-s0","p3-shuf-s0","p3-a7-s1","p3-shuf-s1")}


class Halt(RuntimeError):
    pass


def require(ok, reason):
    if not ok:
        raise Halt("HALT: " + reason)


def finite(value, path="record"):
    if isinstance(value,float):
        require(math.isfinite(value), "non-finite science value at " + path)
    elif isinstance(value,dict):
        for k,v in value.items(): finite(v,path+"."+str(k))
    elif isinstance(value,(list,tuple)):
        for i,v in enumerate(value): finite(v,path+"["+str(i)+"]")


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""): h.update(chunk)
    return h.hexdigest()


def file_ref(path):
    p=Path(path).resolve()
    return {"path":str(p),"sha256":sha_file(p)}


def verify_ref(ref):
    require(isinstance(ref,dict) and set(ref)>={"path","sha256"}, "missing file provenance")
    require(Path(ref["path"]).is_file(),"missing frozen file: "+ref["path"])
    require(sha_file(ref["path"])==ref["sha256"],"hash mismatch: "+ref["path"])


def write_json(path,record):
    obj={**record,"class":CLASS,"decision_id":DECISION_ID}
    finite(obj)
    text=json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    try:
        with Path(path).open("x",encoding="utf-8") as f: f.write(text)
    except FileExistsError as exc:
        raise Halt("HALT: record exists: "+str(path)) from exc


def load_json(path):
    def reject(value): raise Halt("HALT: non-finite JSON constant "+value)
    try:
        obj=json.loads(Path(path).read_text(),parse_constant=reject)
    except (OSError,json.JSONDecodeError) as exc:
        raise Halt("HALT: cannot read record "+str(path)+": "+str(exc)) from exc
    finite(obj)
    return obj


def fresh_directory(path):
    try: Path(path).mkdir(parents=True,exist_ok=False)
    except FileExistsError as exc: raise Halt("HALT: phase directory exists: "+str(path)) from exc
    return Path(path)


def entry_preflight(env=None,root=ROOT):
    env=os.environ if env is None else env
    require(not any(k in env for k in FORBIDDEN_ENV),"INVALID-ENVIRONMENT: inherited knob: "+",".join(k for k in FORBIDDEN_ENV if k in env))
    require(Path(env.get("LLMDB_ROOT",str(root))).resolve()==Path(root).resolve(),"INVALID-ENVIRONMENT: LLMDB_ROOT is not this worktree")
    return Path(root).resolve()


def check_driver_bytes(value):
    require(type(value) is int and 0<=value<=40000000000,"INVALID-BUDGET: sampled MPS driver bytes exceed 40,000,000,000")


def check_eval_seconds(value):
    require(math.isfinite(value) and 0<=value<=14400,"INVALID-BUDGET: evaluation exceeds four hours")


def check_phase_minutes(phase,value,budget=None):
    limit=PHASE_LIMITS[phase] if budget is None else budget
    require(math.isfinite(value) and math.isfinite(limit) and 0<=value<=limit,"INVALID-BUDGET: "+phase+" projected minutes exceed "+str(limit))


def require_authorization(phase,auth,p1_eval_sha,p1_verdict_sha,projection):
    require(isinstance(auth,dict) and isinstance(auth.get(phase),dict),"missing recorded post-P1 "+phase+" authorization")
    a=auth[phase]
    require(a.get("authorized") is True and bool(a.get("recorded_by")) and bool(a.get("recorded_at")),"invalid authorization identity for "+phase)
    require(a.get("p1_eval_sha256")==p1_eval_sha and a.get("p1_verdict_sha256")==p1_verdict_sha,"authorization does not match P1 provenance")
    check_phase_minutes(phase,projection,a.get("budget_minutes"))


def adapter_is_tracked(path):
    p=Path(path).resolve()
    require(p.is_relative_to(ROOT),"adapter path outside worktree")
    proc=subprocess.run(["/usr/bin/git","ls-files","--error-unmatch","--",str(p.relative_to(ROOT))],
                        cwd=ROOT,capture_output=True,text=True)
    require(proc.returncode in (0,1),"git adapter tracking probe failed: "+proc.stderr)
    return proc.returncode==0


def require_untracked_adapter(path):
    require(not adapter_is_tracked(path),"adapter is tracked: "+str(path))


def integer(value,lo,hi,name):
    require(type(value) is int and lo<=value<=hi,"invalid integer/denominator "+name)
    return value


def law3(closed,u,stimulus):
    require(all(integer(x["base"],0,24,"stimulus")<=3 for x in stimulus.values()),"stimulus canonical leak >15%")
    require(u[A7]["para_full_n"]<=2,"stimulus A7 held-out leak >2/72")
    require(all(closed[k]["para_full_n"]>=68 for k in (A1,A2)),"LAW#3 A1/A2 below68/72")
    a=closed[A7]
    require(5<=a["para_full_n"]<=18 and 5<=a["canon_full_n"]<=10 and 42<=a["para_first_n"]<=59,"LAW#3 A7 envelope")
    return True


def compare_null(u,zero,u_rows,zero_rows):
    require(u_rows==zero_rows,"LAW#5(ii): per-prompt rows differ under zero adapter")
    for key in ("canon_full_n","para_full_n","para_first_n","para_string_n","canon_n","para_n","tf_pertok_cont","cond_full_given_first"):
        require(u[key]==zero[key],"LAW#5(ii): count/readout changed: "+key)
    for key in ("L1_flipped_to_edited_value","L1_pre_already_edited_token","L1_top1_changed","L1_n","L1_js_locpct",
                "L3_top1_agree","L3_n","L3_mean_kl","L3_js_locpct","L1_post_top1"):
        require(u["locality_axes"][key]==zero["locality_axes"][key],"LAW#5(ii): locality axis changed: "+key)
    for key in ("frames","relations","mmlu","bigram","contains_n","contains_hits","sibling"):
        require(u["extra"][key]==zero["extra"][key],"LAW#5(ii): probe changed: "+key)
    delta=abs(u["locality_axes"]["generic_ppl_post"]-zero["locality_axes"]["generic_ppl_post"])
    require(delta<=.01 and zero["locality_described_as"]==100.,"LAW#5(ii): generic perplexity/described_as")
    return {"ok":True,"weights_identical":True,"counts_identical":True,"probes_identical":True,
            "ppl_delta":delta,"described_as":zero["locality_described_as"]}


def verify_prompt_count(score,rows,label):
    integer(score["para_n"],72,72,label+" denominator")
    require(len(rows)==24 and len({r["subj"] for r in rows})==24,label+" subject denominator")
    for kind in ("full","string"):
        metric="para_"+kind+"_n"; hits="para_"+kind+"_hits"
        integer(score[metric],0,72,label+" "+metric)
        require(all(len(r[hits])==3 and all(type(v) is bool for v in r[hits]) for r in rows)
                and score[metric]==sum(sum(r[hits]) for r in rows),label+" raw rows/count mismatch")
    require(score["para_string_n"]>=score["para_full_n"],label+" string count below full count")


def validate_arm(a,rows,mounted=False,written=False):
    integer(a["para_n"],72,72,"para_n"); integer(a["canon_n"],24,24,"canon_n")
    require(len(rows)==24 and len({r["subj"] for r in rows})==24,"arm detail must contain24 distinct subjects")
    for r in rows:
        integer(r["ntok"],1,1000,"target length")
        for k in ("para_full_hits","para_first_hits","para_string_hits"):
            require(len(r[k])==3 and all(type(v) is bool for v in r[k]),"invalid per-prompt hit vector "+k)
        require(all(not full or first for full,first in zip(r["para_full_hits"],r["para_first_hits"])),"full hit without first hit")
        integer(r["tf_total"],3*(r["ntok"]-1),3*(r["ntok"]-1),"tf_total")
        integer(r["tf_correct"],0,r["tf_total"],"tf_correct")
    for k,rowkey,denom in (("para_full_n","para_full_hits",72),("para_first_n","para_first_hits",72),("para_string_n","para_string_hits",72)):
        integer(a[k],0,denom,k)
        require(a[k]==sum(sum(r[rowkey]) for r in rows),"aggregate/detail count mismatch: "+k)
    integer(a["canon_full_n"],0,24,"canon_full_n")
    require(a["canon_full_n"]==sum(r["canon_full"] for r in rows),"canonical count/detail mismatch")
    require(a["para_string_n"]>=a["para_full_n"],"para_string_n < para_full_n")
    for key,total in (("tf_pertok_cont",sum(r["tf_total"] for r in rows)),("cond_full_given_first",a["para_first_n"])):
        require(key in a and ((a[key] is None and total==0) or (type(a[key]) in (int,float) and total>0)),"missing/invalid nullable metric "+key)
    require(type(a["locality_described_as"]) in (int,float) and 0<=a["locality_described_as"]<=100,"described_as missing/out of range")
    ax=a["locality_axes"]
    for key,n in (("L1_n",12),("L3_n",30)): integer(ax[key],n,n,key)
    integer(ax["L1_flipped_to_edited_value"],0,12,"L1 flips"); integer(ax["L3_top1_agree"],0,30,"L3 agreement")
    require(ax["generic_ppl_pre"]>0 and ax["generic_ppl_post"]>0,"invalid generic perplexity")
    x=a["extra"]; f=x["frames"]
    require(len(f["train"])==20 and len(f["heldout"])==3,"incomplete frame probes")
    for frame in [f["canon"],*f["train"],*f["heldout"]]:
        integer(frame["n"],6,6,"frame_n"); integer(frame["flips"],0,6,"frame flips")
        require(len(frame["rows"])==6 and len({r["subj"] for r in frame["rows"]})==6
                and all(type(r["flip"]) is bool for r in frame["rows"])
                and frame["flips"]==sum(r["flip"] for r in frame["rows"]),"frame raw rows/count mismatch")
    m=x["mmlu"]; integer(m["n"],200,200,"MMLU_n")
    require(len(m["correct"])==len(m["predicted"])==200 and all(type(v) is bool for v in m["correct"])
            and all(v in "ABCD" and len(v)==1 for v in m["predicted"]),"invalid MMLU rows")
    require(len(m["rows"])==200 and len({r["source_index"] for r in m["rows"]})==200
            and m["correct"]==[r["correct"] for r in m["rows"]]
            and m["predicted"]==[r["predicted"] for r in m["rows"]]
            and m["correct_n"]==sum(m["correct"]) and m["accuracy"]==m["correct_n"]/200.,"MMLU raw rows/count mismatch")
    for k in ("correct_to_wrong","wrong_to_correct"): integer(m[k],0,200,"MMLU_"+k)
    require(m["net_paired_loss"]==m["correct_to_wrong"]-m["wrong_to_correct"],"MMLU discordance mismatch")
    for rel in ("is_a","associated_with"):
        r=x["relations"][rel]; integer(r["n"],24,24,"relation_n")
        require(len(r["pre"])==len(r["post"])==24,"relation rows missing")
        require(r["flips"]==sum(a!=b for a,b in zip(r["pre"],r["post"])),"relation flip mismatch")
    integer(x["contains_n"],0,72,"contains_n")
    require(len(x["contains_hits"])==24 and all(len(v)==3 for v in x["contains_hits"])
            and x["contains_n"]==sum(sum(v) for v in x["contains_hits"]),"contains count/detail mismatch")
    bigram_qualifier(x["bigram"])
    require(x["sibling"]["misses"]==72-a["para_full_n"],"sibling denominator mismatch")
    integer(x["sibling"]["emissions"],0,x["sibling"]["misses"],"sibling emissions")
    if mounted:
        verify_prompt_count(x["mounted"],x["mounted"]["rows"],"mounted")
    if written:
        require(set(x["geometry"])=={str(l) for l in BAND},"incomplete per-layer geometry")
        for layer,g in x["geometry"].items():
            for k in ("delta_norm","trace_delta_cov_deltaT","application_relative_error"):
                require(type(g[k]) in (int,float),"missing geometry metric "+layer+"."+k)
            require(g["delta_norm"]>=0 and g["application_relative_error"]>=0,"invalid geometry norm/error")
            require((g["null_cov_share"] is None and g["delta_norm"]==0) or type(g["null_cov_share"]) in (int,float),"invalid geometry denominator")
            require(len(g["delta_sha256"])==64,"geometry delta hash missing")
        require(type(x["write_size_ratio_to_closedform_A7"]) in (int,float) and x["write_size_ratio_to_closedform_A7"]>=0,"write-size ratio missing")


def bigram_qualifier(b):
    e=integer(b["eligible_n"],0,24,"bigram eligible"); integer(b["excluded_n"],24-e,24-e,"bigram excluded")
    rows=b["rows"]
    require(sum(r["eligible"] for r in rows)==e,"bigram eligible/detail mismatch")
    eligible=[r for r in rows if r["eligible"]]
    for r in eligible:
        for k in ("c","s","b"): integer(r[k],0,1,"bigram_"+k)
        require(0<=r["n"]<=1,"bigram n fraction")
    c=sum(r["c"] for r in eligible)
    x=sum(r["c"]==1 and (r["s"]==1 or r["b"]==1 or r["n"]>=.5) for r in eligible)
    return "NOT-EVALUABLE" if not c else "BIGRAM" if x>=(c+1)//2 else None


def gates(a,reference,u,control=None):
    ax,rx=a["locality_axes"],reference["locality_axes"]
    f,rf=a["extra"]["frames"],reference["extra"]["frames"]
    pre,post=u["extra"]["mmlu"]["correct"],a["extra"]["mmlu"]["correct"]
    result={"G1":ax["L1_flipped_to_edited_value"]<=rx["L1_flipped_to_edited_value"]+1,
            "G2":ax["L3_top1_agree"]>=29,
            "G3":round(a["locality_described_as"]*100)>=round(reference["locality_described_as"]*100)-300,
            "G4":f["canon"]["flips"]<=rf["canon"]["flips"]+1 and all(c["flips"]<=b["flips"]+1 for c,b in zip(f["train"],rf["train"])),
            "G5":round(ax["generic_ppl_post"],3)-round(ax["generic_ppl_pre"],3)<=.5+1e-12,
            "G6":sum(p and not q for p,q in zip(pre,post))-sum(not p and q for p,q in zip(pre,post))<=4}
    if control is not None:
        cross=control["extra"]["cross_score"]
        integer(cross["para_n"],72,72,"cross_score_n"); integer(cross["para_full_n"],0,72,"cross_score")
        result["G7"]=cross["para_full_n"]<=2
    return result


def band(count):
    return 0 if count<30 else 1 if count<61 else 2


def config_label(count,misses):
    return ("FAIL-CEILING" if count<30 else "PARTIAL-CEILING" if count<61 else
            "PARTIAL-CEILING-LOCALITY-COST" if misses else "PASS-CEILING")


def train_identity(t):
    return t["arm"],t["seed"],t["rank"],t["retrain"]


def train_tag(unit,steps=400):
    arm,seed,rank,rt=unit
    return arm+"_s"+str(seed)+"_r"+str(rank)+("_rt" if rt else "")+("_retry800" if steps==800 else "")


def validate_phase(p):
    finite(p)
    require(p["class"]==CLASS and p["decision_id"]==DECISION_ID and p["status"]=="PASS","invalid phase identity/status")
    phase=p["phase"]
    require(phase in RECIPES,"unknown phase")
    env=p["environment"]
    require(env=={"model_id":MODEL_ID,"model_revision":MODEL_REV,"layers":list(BAND),"dtype":"float16","device":"mps"},"INVALID-ENVIRONMENT: actual evaluation environment")
    require(all(p["validity"][k] is True for k in ("fingerprint","seal","instrument","hashes","entry","seam")),"phase correctness controls failed")
    check_eval_seconds(p["wall_seconds"]); check_driver_bytes(p["sampled_peak_driver_bytes"])
    for key in ("train_inputs","trainer_source","mmlu200","templates","prereg"):
        require(isinstance(p["provenance"][key],str) and len(p["provenance"][key])==64,"missing hash: "+key)
    require(p["provenance"]["templates"]==TEMPLATE_SHA and p["provenance"]["prereg"]==PREREG_SHA,"frozen template/prereg hash mismatch")
    require(set(p["u"])=={A1,A2,A7,SHUF} and set(p["stimulus"])==set(p["u"]),"incomplete U/stimulus controls")
    for k,a in p["u"].items(): validate_arm(a,p["u_detail"][k])
    z=p["law5_null"]
    require(all(z[k] is True for k in ("ok","weights_identical","counts_identical","probes_identical")) and abs(z["ppl_delta"])<=.01 and z["described_as"]==100.,"LAW#5(ii) null/restore failed")
    validate_arm(z["arm"],z["rows"])
    compare_null(p["u"][A7],z["arm"],p["u_detail"][A7],z["rows"])
    require(set(z["base_hash"])=={str(l) for l in BAND} and z["base_hash"]==z["after_hash"],"LAW#5(ii) tensor hash evidence missing/mismatch")
    require(p["delegation_identity"] is True,"LAW#5(iv) delegation identity failed")
    require(set(p["base_band_hash"])=={str(l) for l in BAND} and p["base_band_hash"]==p["final_band_hash"],"LAW#5(iii) final restore hash mismatch")
    require(p["zero_adapter_hits"]==p["expected_zero_hits"]==1,"LAW#5(v) zero hit counter")
    require(p["trained_oracle_hits"]==p["expected_trained_hits"]==len(TRAIN_UNITS[phase]),"LAW#5(v) trained hit counter")
    require(set(p["recipes"])=={"closedform",*RECIPES[phase]},"incomplete phase recipes")
    for name,rec in p["recipes"].items():
        require(rec["band"]==list(BAND) and rec["restored"] is True,"LAW#5(iii) recipe restore/band")
        require(rec["band_after_hash"]==p["base_band_hash"],"LAW#5(iii) recipe restore hash mismatch")
        l=rec["law5_gate"]
        require(l["ok"] is True and abs(l["expr_delta"])<.05 and abs(l["loc_delta"])<3,"LAW#5(i) strict limits")
        expected=(A1,A2,A7) if name=="closedform" else RECIPES[phase][name]
        require(set(rec["arms"])==set(expected) and set(rec["detail"])==set(expected),"incomplete recipe arms")
        for key,a in rec["arms"].items():
            validate_arm(a,rec["detail"][key],name!="closedform",written=True)
            m=a["extra"]["mmlu"]; pre=p["u"][A7]["extra"]["mmlu"]["correct"]
            require(m["correct_to_wrong"]==sum(b and not c for b,c in zip(pre,m["correct"]))
                    and m["wrong_to_correct"]==sum(not b and c for b,c in zip(pre,m["correct"])),"MMLU paired evidence differs from U")
            if key==SHUF:
                x=a["extra"]; verify_prompt_count(x["cross_score"],x["cross_detail"],"shuffled cross-score")
    law3(p["recipes"]["closedform"]["arms"],p["u"],p["stimulus"])
    trained=p["train_records"]
    require(len(trained)==len(TRAIN_UNITS[phase]) and {train_identity(t) for t in trained}==set(TRAIN_UNITS[phase]),"INVALID-INCOMPLETE: matched training units")
    for t in trained:
        require(t["status"]=="PASS" and t["frozen_parameters_unchanged"] is True,"INVALID-UNDERFIT/frozen parameters")
        require(bool(t["frozen_parameter_hashes_before"]) and t["frozen_parameter_hashes_before"]==t["frozen_parameter_hashes_after"],"frozen parameter hash evidence mismatch")
        n=24 if t["arm"]==CANON_ARM else 480
        integer(t["fit"]["n"],n,n,"train fit denominator")
        integer(t["fit"]["correct"],23 if n==24 else 456,n,"train fit gate")
        require(t["steps"] in (400,800) and t["model_id"]==MODEL_ID and t["model_revision"]==MODEL_REV
                and t["layers"]==list(BAND) and t["device"]=="mps" and t["dtype"]=="float32","training protocol/environment mismatch")
        require(t["provenance"]==p["provenance"],"frozen provenance mismatch")
        require(isinstance(t["adapter"]["sha256"],str) and len(t["adapter"]["sha256"])==64,"adapter hash absent")
        check_driver_bytes(t["sampled_peak_driver_bytes"])
        if t["arm"]==A7:
            match=next(x for x in trained if train_identity(x)==(SHUF,t["seed"],t["rank"],t["retrain"]))
            require(match["steps"]==t["steps"],"A7/shuf final step mismatch")
    positive={"P1":(("oracle_p1",A1),("oracle_p1",A2)),"P2":(("oracle_s1",A1),),"P3":()}[phase]
    require(all(p["recipes"][recipe]["arms"][arm]["para_full_n"]>=68 for recipe,arm in positive),"trainer positive control below68/72")
    if phase=="P2":
        same=p["same_seed"]
        integer(same["n"],72,72,"same-seed denominator")
        integer(same["prompt_agreement_n"],0,72,"same-seed prompt agreement")
        require(set(same["per_layer_cosine"])=={str(l) for l in BAND},"same-seed cosine layers incomplete")
        require(all(type(v) in (int,float) and -1.000001<=v<=1.000001 for v in same["per_layer_cosine"].values()),"invalid same-seed cosine")


def configuration(p,recipe_name):
    recipe=p["recipes"][recipe_name]
    a=recipe["arms"][A7]; control=recipe["arms"][SHUF]
    g=gates(a,p["recipes"]["closedform"]["arms"][A7],p["u"][A7],control)
    misses=[k for k,v in g.items() if not v]
    count=a["para_full_n"]; mounted=a["extra"]["mounted"]["para_full_n"]
    qualifiers=[]
    if bigram_qualifier(a["extra"]["bigram"])=="BIGRAM": qualifiers.append("BIGRAM")
    if abs(count-control["para_full_n"])>15: qualifiers.append("PAIRING-SPECIFIC")
    unit=next(t for t in p["train_records"] if t["arm"]==A7 and t["seed"]==(1 if recipe_name in ("oracle_s1","oracle_r64_s1") else 0) and t["retrain"]==(recipe_name=="oracle_s0rt"))
    if unit["steps"]==800: qualifiers.append("RETRY800")
    merge=abs(count-mounted)>5
    if merge: qualifiers.append("MERGE-LOSS")
    return {"count":count,"gates":g,"gate_misses":misses,"label":config_label(count,misses),
            "qualifiers":qualifiers,"unstable_merge":merge and not(count>=61 and not misses and mounted>count),
            "mounted_count":mounted,"steps":unit["steps"],
            "per_template_counts":[sum(r["para_full_hits"][j] for r in recipe["detail"][A7]) for j in range(3)],
            "per_fact_counts":[sum(r["para_full_hits"]) for r in recipe["detail"][A7]],
            "per_edge_pass":[all(r["para_full_hits"]) for r in recipe["detail"][A7]],
            "gain_over_closedform":count-p["recipes"]["closedform"]["arms"][A7]["para_full_n"]}


def replicated(c0,c1,retrain=None):
    count=min(c0["count"],c1["count"])
    misses=sorted(set(c0["gate_misses"])|set(c1["gate_misses"]))
    reasons=[]
    if abs(c0["count"]-c1["count"])>15: reasons.append("seed gap >15")
    compared=[c0,c1]+([] if retrain is None else [retrain])
    if any(c["unstable_merge"] for c in compared): reasons.append("MERGE-LOSS")
    if retrain is not None:
        if abs(c0["count"]-retrain["count"])>10: reasons.append("same-seed gap >10")
        if band(c0["count"])!=band(retrain["count"]): reasons.append("same-seed band crossing")
        if c0["gates"]!=retrain["gates"]: reasons.append("same-seed binding gate crossing")
    return {"count":count,"seed_counts":[c0["count"],c1["count"]],"configurations":[c0,c1],
            "same_seed":retrain,"gate_misses":misses,"label":config_label(count,misses),
            "qualifiers":sorted(set(q for c in compared for q in c["qualifiers"])),
            "stable":not reasons,"instability":reasons}


def canonical_split(p1,p2):
    a=p1["recipes"]["oracle_canon_s0"]["arms"][CANON_ARM]
    b=p2["recipes"]["oracle_canon_s1"]["arms"][CANON_ARM]
    count=min(a["para_full_n"],b["para_full_n"])
    readable=abs(a["para_full_n"]-b["para_full_n"])<=15
    for p,c in ((p1,a),(p2,b)):
        readable &= all(gates(c,p["recipes"]["closedform"]["arms"][A7],p["u"][A7]).values())
        readable &= abs(c["para_full_n"]-c["extra"]["mounted"]["para_full_n"])<=5
    return ("a" if count>=30 else "b",count) if readable else ("c",None)


def read_measurement(phases):
    result={"class":CLASS,"decision_id":DECISION_ID,"status":"INCOMPLETE","final_label":None,
            "routing":None,"ranks":{},"p3_required":False,"canon_split":None,"reference_count":None,
            "reference_status":"NOT-ISSUED","c10_status":"OPEN/BLOCKING","f1_changed":False}
    try:
        require("P1" in phases,"P1 incomplete")
        for p in phases.values(): validate_phase(p)
        if "P2" not in phases: return result
        require(phases["P1"]["provenance"]==phases["P2"]["provenance"],"cross-phase frozen provenance mismatch")
        r16=replicated(configuration(phases["P1"],"oracle_p1"),configuration(phases["P2"],"oracle_s1"),configuration(phases["P2"],"oracle_s0rt"))
        result["ranks"]["16"]=r16
        if not r16["stable"]:
            result["status"]="UNSTABLE"; return result
        result["p3_required"]=r16["label"] in ("PARTIAL-CEILING","FAIL-CEILING")
        if result["p3_required"]:
            if "P3" not in phases: return result
            require(phases["P3"]["provenance"]==phases["P1"]["provenance"],"P3 frozen provenance mismatch")
            r64=replicated(configuration(phases["P3"],"oracle_r64_s0"),configuration(phases["P3"],"oracle_r64_s1"))
            result["ranks"]["64"]=r64
            if not r64["stable"]:
                result["status"]="UNSTABLE"; return result
        else:
            require("P3" not in phases,"P3 scientifically excluded by rank16 label")
        order=("FAIL-CEILING","PARTIAL-CEILING","PARTIAL-CEILING-LOCALITY-COST","PASS-CEILING")
        final=max((x["label"] for x in result["ranks"].values()),key=order.index)
        result.update(status="VALID",final_label=final)
        split,canon_count=canonical_split(phases["P1"],phases["P2"])
        result["canon_split"]=split
        route={"action":"INDEPENDENT-PREREG-ONLY","h30_eligible":final=="PASS-CEILING",
               "oracle_measurement_not_route":True,"mechanism_attribution":False}
        if final=="FAIL-CEILING":
            route["action"]="OPERATOR-CEILING-RULING"
            route["scope"]="string representation on this band under these recipes"
            route["representation_alternative"]="step3 minted-token route"
            route["steps6_7"]="DEPRIORITISED-PENDING-RULING"
            route["stronger_oracle"]="H-15 operator option"
        elif split!="c":
            result.update(reference_count=canon_count,reference_status="O-A7-CANON-REFERENCE")
            if final=="PASS-CEILING" and split=="a": route["action"]="MOTIVATE-INDEPENDENT-STEPS-6-7-5b"
        elif final!="PASS-CEILING":
            clean=[r["count"] for r in result["ranks"].values() if r["stable"] and not r["gate_misses"]]
            result.update(reference_count=max(clean) if clean else None,
                          reference_status="GATE-CLEAN-RANK-REFERENCE" if clean else "NO-GATE-CLEAN-REFERENCE")
        result["routing"]=route
        return result
    except (Halt,KeyError,TypeError,ValueError,StopIteration) as exc:
        result.update(status="INVALID",final_label=None,routing=None,reference_count=None,reference_status="NOT-ISSUED",reason=str(exc))
        return result


def reproject(t):
    finite(t)
    training=t["training400_seconds"]; setup=t["recipe_setup_seconds"]
    u=t["u_seconds"]; null=t["null_seconds"]; closed=t["closedform_arm_seconds"]; oracle=t["oracle_arm_seconds"]
    require(all(v>=0 for v in (training,setup,u,null,closed,oracle)),"invalid measured unit time")
    return {"P2_minutes":(6*training+u+null+4*setup+3*closed+6*oracle)/60,
            "P3_minutes":(4*training+u+null+3*setup+3*closed+4*oracle)/60,
            "limits_minutes":PHASE_LIMITS,"basis":t,"rank64_training_timing":"rank16 projection; remeasure each rank64 attempt",
            "authorization_required":["P2","P3"]}


def stage_names():
    return ["step0","p1-preflight",*TRAIN_STAGES["P1"],"p1-eval","p1-project",
            *TRAIN_STAGES["P2"],"p2-eval",*TRAIN_STAGES["P3"],"p3-eval","read"]


def latest_directory(prefix,base=None):
    base=ROOT/"results/c10w_oracle" if base is None else Path(base)
    paths=sorted(p for p in base.glob(prefix.lower()+"_*") if p.is_dir())
    require(bool(paths),"missing "+prefix+" phase/authorization record")
    p=paths[-1]
    require(not (p/"HALT.json").exists(),"phase previously HALTED: "+str(p))
    return p


def load_frozen(directory):
    p=Path(directory).resolve(); step=load_json(p/"step0.json")
    require(step["status"]=="PASS" and step["class"]==CLASS and step["decision_id"]==DECISION_ID,"step0 not passing")
    require(step["prereg_sha256"]==PREREG_SHA and sha_file(ROOT/"docs/C10W_ORACLE_PREREG.md")==PREREG_SHA,"frozen prereg mismatch")
    for ref in step["files"].values(): verify_ref(ref)
    for ref in step["sources"].values(): verify_ref(ref)
    require(all(step["seal"][s] is True for s in ("S1","S2","S2c","S2d","S3","S4","S5","S6","S7")),"seal not passing")
    require(step["seam"]["ok"] is True and step["fingerprint"]["ok"] is True and step["instrument_ok"] is True,"step0 correctness gate failed")
    return step


def frozen_provenance(step):
    return {"train_inputs":step["files"]["train_inputs"]["sha256"],"trainer_source":step["sources"]["trainer"]["sha256"],
            "mmlu200":step["files"]["mmlu200"]["sha256"],"templates":TEMPLATE_SHA,"prereg":PREREG_SHA}


def phase_trains(directory,phase):
    out=[]
    for unit in TRAIN_UNITS[phase]:
        paths=[Path(directory)/"train"/(train_tag(unit,s)+".json") for s in (400,800)]
        available=[p for p in paths if p.is_file()]
        require(bool(available),"training incomplete: "+train_tag(unit))
        tr=load_json(available[-1]); require(tr["status"]=="PASS","training underfit/HALT: "+train_tag(unit))
        verify_ref(tr["adapter"]); require_untracked_adapter(tr["adapter"]["path"])
        out.append(tr)
    return out


def verify_linked_train(tr):
    verify_ref(tr["record_file"])
    original=load_json(tr["record_file"]["path"])
    require(original=={k:v for k,v in tr.items() if k!="record_file"},"embedded training evidence differs from hashed attempt record")


def authorized_phase_entry(proof):
    require(all(k in proof for k in ("phase","p1_directory","authorization","authorized_projection_minutes")),"missing recorded post-P1 phase authorization")
    phase=proof["phase"]; p1=Path(proof["p1_directory"]).resolve()
    require(phase in ("P2","P3"),"undeclared post-P1 phase")
    verify_ref(proof["authorization"])
    require_authorization(phase,load_json(proof["authorization"]["path"]),sha_file(p1/"eval.json"),sha_file(p1/"verdict.json"),proof["authorized_projection_minutes"])
    if phase=="P3":
        reading=read_measurement({"P1":load_json(p1/"eval.json"),"P2":replication_for(p1)})
        require(reading["status"]=="INCOMPLETE" and reading["p3_required"],"P3 scientifically excluded or replication invalid")


def replication_for(p1):
    p1=Path(p1); p2=latest_directory("p2"); record=load_json(p2/"eval.json")
    require(record["phase"]=="P2" and record["p1_eval_sha256"]==sha_file(p1/"eval.json"),"P2 belongs to another P1")
    verify_ref(record["authorization"])
    require_authorization("P2",load_json(record["authorization"]["path"]),sha_file(p1/"eval.json"),sha_file(p1/"verdict.json"),record["authorized_projection_minutes"])
    step=load_frozen(record["step0_directory"])
    require(record["provenance"]==frozen_provenance(step),"P2 frozen provenance mismatch")
    for tr in record["train_records"]:
        verify_linked_train(tr); verify_ref(tr["adapter"]); require_untracked_adapter(tr["adapter"]["path"])
    validate_phase(record)
    return record


def preflight_evidence(raw):
    finite(raw)
    require(raw["class"]==CLASS and raw["decision_id"]==DECISION_ID and raw["status"]=="PASS","preflight record identity/status")
    require(raw["trained_oracle_hits"]==raw["expected_trained_hits"]==0 and raw["zero_adapter_hits"]==raw["expected_zero_hits"]==1,"preflight hit manifest")
    require(set(raw["recipes"])=={"closedform"} and raw["delegation_identity"] is True,"preflight delegation/recipe manifest")
    require(all(raw["validity"][k] is True for k in ("fingerprint","seal","instrument","hashes","entry","seam")),"preflight validity failed")
    recipe=raw["recipes"]["closedform"]; closed=recipe["arms"]
    require(set(closed)=={A1,A2,A7} and recipe["restored"] is True,"preflight incomplete/restore failed")
    require(set(raw["base_band_hash"])=={str(l) for l in BAND} and raw["final_band_hash"]==raw["base_band_hash"]
            and recipe["band_after_hash"]==raw["base_band_hash"],"preflight restore hash mismatch")
    for k,a in raw["u"].items(): validate_arm(a,raw["u_detail"][k])
    for k,a in closed.items(): validate_arm(a,recipe["detail"][k],written=True)
    law3(closed,raw["u"],raw["stimulus"])
    null=raw["law5_null"]
    compare_null(raw["u"][A7],null["arm"],raw["u_detail"][A7],null["rows"])
    require(null["base_hash"]==null["after_hash"],"preflight null tensor hash mismatch")
    g=recipe["law5_gate"]
    require(g["ok"] is True and abs(g["expr_delta"])<.05 and abs(g["loc_delta"])<3,"preflight strict LAW#5 limits")
    return {"law3_counts":{"A1":closed[A1]["para_full_n"],"A2":closed[A2]["para_full_n"],
                           "para_full":closed[A7]["para_full_n"],"canon_full":closed[A7]["canon_full_n"],
                           "para_first":closed[A7]["para_first_n"],"u_para_full":raw["u"][A7]["para_full_n"],
                           "stimulus":[x["base"] for x in raw["stimulus"].values()]},
            "law5_standing":g,"null_evidence":{"base_hash":sha_text(str(null["base_hash"])),"after_hash":sha_text(str(null["after_hash"])),
               "u_hit_probe_sha256":sha_text(str((raw["u_detail"][A7],raw["u"][A7]["extra"]))),
               "zero_hit_probe_sha256":sha_text(str((null["rows"],null["arm"]["extra"]))),
               "ppl_delta":null["ppl_delta"],"described_as":null["described_as"]}}


def verify_preflight_certificate(proof):
    verify_ref(proof["evaluation"]); raw=load_json(proof["evaluation"]["path"])
    require(raw["provenance"]==proof["provenance"],"preflight raw/certificate provenance mismatch")
    expected=preflight_evidence(raw)
    require(all(proof[k]==v for k,v in expected.items()),"preflight certificate contradicts raw evidence")
    if proof.get("phase") in ("P2","P3"): authorized_phase_entry(proof)
    return True


def disk_phases(p1):
    phases={"P1":load_json(Path(p1)/"eval.json")}
    p1_verdict=Path(p1)/"verdict.json"
    for name in ("P2","P3"):
        base=ROOT/"results/c10w_oracle"
        paths=sorted(p for p in base.glob(name.lower()+"_*") if (p/"eval.json").exists())
        if paths:
            p=paths[-1]; rec=load_json(p/"eval.json")
            require(rec["p1_eval_sha256"]==sha_file(Path(p1)/"eval.json"),"phase attached to different P1")
            require_authorization(name,load_json(rec["authorization"]["path"]),sha_file(Path(p1)/"eval.json"),sha_file(p1_verdict),rec["authorized_projection_minutes"])
            verify_ref(rec["authorization"])
            phases[name]=rec
    for p in phases.values():
        step=load_frozen(p["step0_directory"])
        require(p["provenance"]==frozen_provenance(step),"phase frozen provenance mismatch")
        for t in p["train_records"]:
            verify_ref(t["adapter"]); require_untracked_adapter(t["adapter"]["path"])
            verify_linked_train(t)
    return phases


def main():
    if sys.argv[1:]==["verify-preflight"]:
        try:
            proof=json.loads(sys.stdin.read()); verify_preflight_certificate(proof)
            print(json.dumps({"ok":True})); return 0
        except Exception as exc:
            print("HALT: preflight evidence verification: "+str(exc),file=sys.stderr); return 2
    parser=argparse.ArgumentParser(description=CLASS)
    parser.add_argument("p1_directory",nargs="?")
    args=parser.parse_args()
    try:
        p1=Path(args.p1_directory).resolve() if args.p1_directory else latest_directory("p1")
        result=read_measurement(disk_phases(p1)); print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
        return 0 if result["status"]=="VALID" else 2
    except Halt as exc:
        print(str(exc),file=sys.stderr); return 2


if __name__=="__main__":
    sys.exit(main())
