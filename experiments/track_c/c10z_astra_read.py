import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""D-C10z-astra FROZEN v2.2: deterministic count reader, no science imports."""
import hashlib
import base64
from functools import lru_cache
import json
import math
from pathlib import Path
import statistics
import zlib

SCHEMA = "c10z_astra-v2.2"
PREREG_SHA = "7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29"
ENGINE_SHA = "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65"
A1, A2, A7 = "A1_single", "A2_coherent2", "A7_coined_coined"
ARMS = (A1,A2,A7)
INPUT_KEYS = ("requests", "model_revision", "H_pristine", "context_templates_sha256",
    "dstats_sha256", "G_sha256", "settings", "driver_sha256", "reader_sha256", "seed",
    "prereg_sha256", "engine_sources", "hparams", "screens", "covariances", "tokenizer",
    "batches", "forward_settings", "environment", "solver_backend", "dataset", "safetensors", "go_sha256")
QUAL_ORDER = ("UNDERFIT", "LARGE-WRITE", "SUBJECT-FREE", "EXCEEDS-TTL", "STAGE1",
              "SINGLE-PROCESS", "REPRO-INCOMPLETE", "NOT-REPLICATED", "NOT-REPRODUCIBLE")
INFINITY = "POSITIVE-INFINITY"
SETTINGS = {"margin":5.,"views":6,"rounds":10,"layers_kept":9,"neurons_per_token":16,
    "neuron_min":16,"neuron_max":440,"D_floor":.001,"D_rows":1000,"D_tokens":100,
    "ridge":.001,"solve_dtype":"float64","solve_device":"cpu","model_dtype":"float16",
    "model_device":"mps","capture_dtype":"float32","write":"fp16(fp32(w)+fp32(delta))",
    "padding_side":"right","batch_rows":144,"seed":0,"logits_to_keep":0,"use_cache":False}


class Halt(ValueError):
    def __init__(self, code, detail):
        self.code, self.detail = code, str(detail)
        super().__init__(code+": "+self.detail)


def require(condition, code, detail):
    if not condition:
        raise Halt(code,detail)


def finite_json(value):
    if isinstance(value,float):
        require(math.isfinite(value),"HALTED-V6","non-finite science record")
    elif isinstance(value,dict):
        for v in value.values(): finite_json(v)
    elif isinstance(value,(list,tuple)):
        for v in value: finite_json(v)


def json_digest(value):
    finite_json(value)
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":"),
                                    ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def sha(value):
    return isinstance(value,str) and len(value)==64 and all(c in "0123456789abcdef" for c in value)


def count(value, maximum, field):
    require(type(value) is int and 0<=value<=maximum,"HALTED-V12","invalid count "+field)
    return value


def median(values):
    require(bool(values),"HALTED-V12","empty median population")
    ordered=sorted(math.inf if v==INFINITY else v for v in values)
    result=statistics.median(ordered)
    return INFINITY if math.isinf(result) else result


def fit(info, canonical):
    M=info["M"];m=count(info["m"],M,"m")
    require(type(M) is int and M>0,"HALTED-V12","empty fit population")
    pos=count(info["positive_identity_fact_n"],24,"positive_identity_fact_n")
    count(canonical,24,"canon_full_n")
    return 20*m>=19*M and pos>=23 and canonical>=23


def fit_counts(identity_leads, view_leads):
    flat=[v for row in view_leads for v in row]
    finite_json(flat)
    return {"m":sum(v>=5. for v in flat),"M":len(flat),
            "positive_identity_fact_n":sum(all(v>0 for v in row) for row in identity_leads)}


@lru_cache(maxsize=12)
def decoded_artifact(serialized):
    import numpy as np
    artifact=json.loads(serialized)
    require(artifact["encoding"]=="zlib-base64-fp16-le","HALTED-V12","artifact encoding")
    layers=artifact["layers"];pairs=[];data={};ratios=[]
    require(bool(layers),"HALTED-V12","empty stored write")
    for key in sorted(layers,key=int):
        layer=layers[key];cols=layer["columns"];shape=layer["shape"]
        require(key==str(int(key)) and 0<=int(key)<36 and cols==sorted(set(cols)) and
                all(type(j) is int and 0<=j<11008 for j in cols) and bool(cols) and
                shape==[2048,len(cols)],"HALTED-V12","artifact shape/carrier indices")
        values=[];raws=[]
        for field in ("pristine","final"):
            try:raw=zlib.decompress(base64.b64decode(layer[field],validate=True))
            except (ValueError,zlib.error) as exc:raise Halt("HALTED-V12","invalid fp16 bytes") from exc
            require(len(raw)==math.prod(shape)*2,"HALTED-V12","fp16 byte length")
            value=np.frombuffer(raw,dtype="<f2").reshape(shape).astype(np.float64)
            require(bool(np.isfinite(value).all()),"HALTED-V6","nonfinite deployed artifact")
            values.append(value);raws.append(raw)
        old,new=values;delta=new-old
        norms=np.linalg.norm(old,axis=0);changes=np.linalg.norm(delta,axis=0)
        ratios.extend((0. if change==0 else INFINITY) if norm==0 else float(change/norm)
                      for norm,change in zip(norms,changes))
        data[key]={"delta":delta,"old":raws[0],"new":raws[1],"columns":cols}
        pairs.extend((int(key),j) for j in cols)
    h=hashlib.sha256(json.dumps(pairs,separators=(",", ":")).encode())
    for key in sorted(data,key=int):h.update(data[key]["new"])
    require(h.hexdigest()==artifact["H_out"],"HALTED-V12","H_out does not bind stored weights")
    return {"H_out":h.hexdigest(),"layers":data,"ratios":ratios}


def artifact_evidence(write):
    evidence=decoded_artifact(json.dumps(write["artifact"],sort_keys=True,separators=(",", ":")))
    require(write["H_out"]==evidence["H_out"],"HALTED-V12","write H_out differs")
    require(set(write["carriers"])==set(evidence["layers"]) and
            all(sorted(write["carriers"][l])==v["columns"] for l,v in evidence["layers"].items()),
            "HALTED-V12","write carrier set differs from bytes")
    require(write["carrier_count"]==len(evidence["ratios"]) and
            len(write["relative_changes"])==len(evidence["ratios"]),"HALTED-V12","W1 carrier population")
    require(all(a==b if INFINITY in (a,b) else math.isclose(a,b,rel_tol=2e-6,abs_tol=1e-8)
                for a,b in zip(write["relative_changes"],evidence["ratios"])),
            "HALTED-V12","W1 differs from realised fp16 write")
    return evidence


def validate_fit(arm,batch):
    views=arm["post_fit_observation"]
    require(arm["target_lengths"]==batch["target_lengths"] and len(views)==6 and
            all(len(view)==24 and all(len(row)==n for row,n in zip(view,batch["target_lengths"]))
                for view in views),"HALTED-V12","all-view target-position leads incomplete")
    actual=fit_counts(views[0],[row for view in views for row in view])
    require(arm["fit"]==actual,"HALTED-V12","FIT summary disagrees with native leads")
    require([row["ntok"] for row in arm["rows"]]==batch["target_lengths"],"HALTED-V12","evaluator target lengths drift")
    held=arm["heldout_position_leads"];requirements=held["requirements"]
    require(len(held["pre"])==len(held["post"])==len(requirements)==3*sum(batch["target_lengths"]) and
            [(r["fact"],r["view"],r["q"],r["target"]) for r in requirements]==
            [(i,v,q,y) for i,ids in enumerate(batch["target_ids"]) for v in range(3) for q,y in enumerate(ids)],
            "HALTED-V12","held-out position population")


def reproduction_evidence(p1,p2):
    import numpy as np
    status="PASS";errors={};omitted=[];identical=True
    for recipe in ("Z","Z-band"):
        for arm,a in p1["recipes"].get(recipe,{"arms":{}})["arms"].items():
            b=p2["recipes"].get(recipe,{"arms":{}})["arms"].get(arm);name=recipe+"/"+arm
            if b is None:omitted.append(name);continue
            wa,wb=a["write"],b["write"];aa,ab=artifact_evidence(wa),artifact_evidence(wb)
            same=wa["carriers"]==wb["carriers"] and wa["rounds_used"]==wb["rounds_used"]
            exact=aa["H_out"]==ab["H_out"] and aa["layers"].keys()==ab["layers"].keys()
            errors[name]={}
            if aa["layers"].keys()!=ab["layers"].keys():same=False
            for l,layer in aa["layers"].items():
                other=ab["layers"].get(l)
                if other is None or layer["columns"]!=other["columns"]:error="CARRIERS-DIFFER";exact=False
                else:
                    x,y=layer["delta"],other["delta"];nx=float(np.linalg.norm(x));ny=float(np.linalg.norm(y))
                    error=(0. if nx==ny==0 else "ONE-ZERO") if nx==0 or ny==0 else float(np.linalg.norm(x-y)/nx)
                    exact=exact and layer["old"]==other["old"] and layer["new"]==other["new"]
                errors[name][l]=error;same=same and r1_error_pass(error)
            identical=identical and exact
            if not same:status="FAIL"
    if omitted and status=="PASS":status="NOT-EVALUATED"
    za=p1["recipes"]["Z"]["arms"][A7];zb=p2["recipes"]["Z"]["arms"][A7]
    disagreement=sum(x!=y for a,b in zip(za["rows"],zb["rows"]) for x,y in zip(a["para_full_hits"],b["para_full_hits"]))
    diff=abs(za["para_full_n"]-zb["para_full_n"])
    return {"R1":{"status":status,"per_layer_errors":errors,"omitted_arms":omitted,
                  "reason":"K1" if omitted else "measured"},"R2":{"difference":diff},"R3":{"disagree":disagreement},
        "artifact_identity":"NOT-EVALUATED" if omitted else "EXACT" if identical else "DIFFERENT",
        "numeric_behavioral_reproduction":"NOT-EVALUATED" if omitted and status!="FAIL" else
            "PASS" if status=="PASS" and diff<=2 and disagreement<=3 else "FAIL"}


def law3(recipe):
    arms=recipe["arms"];a7=arms[A7]
    for field,lo,hi in (("para_full_n",5,18),("canon_full_n",5,10),("para_first_n",42,59)):
        value=count(a7[field],24 if field=="canon_full_n" else 72,field)
        require(lo<=value<=hi,"HALTED-V4",field+" outside LAW#3 envelope: "+str(value))
    for arm in (A1,A2):
        require(count(arms[arm]["para_full_n"],72,arm)>=68,"HALTED-V4",arm+" <68")


def check_instruments(checks):
    for i in (0,1,2,3,4,5,7):
        require(checks["Z"+str(i)]["ok"] is True,"HALTED-V5","Z"+str(i)+" failed")
    z0,z2,z7=checks["Z0"],checks["Z2"],checks["Z7"]
    require(z0["sigma_shape"]<=.125 and z0["tau_shape"]==max(2*z0["sigma_shape"],.02),
            "HALTED-V5","Z0 tolerance")
    require(type(z2["checked"]) is int and z2["checked"]>0 and
            z2["checked"]+z2["ambiguous"]==24,"HALTED-V5","Z2 has no checked facts or wrong population")
    require(z7["nonzero_controls"]>=1 and z7["tau_head"]==max(2*z7["sigma_head"],.02)
            and z7["tau_head"]<=.25,"HALTED-V5","Z7 active control/head tolerance")
    flat=lambda rows:[x for row in rows for x in row]
    observed=flat(z0["identity_batch_leads"]);reference=flat(z0["prefix_shape_leads"])
    require(len(observed)==len(reference)>0 and
            math.isclose(max(abs(a-b) for a,b in zip(observed,reference)),z0["sigma_shape"],abs_tol=1e-8),
            "HALTED-V5","Z0 raw spread disagrees")
    require(checks["Z1"]["native_reconstruction_error"]<=z7["tau_head"],"HALTED-V5","pristine Z1")
    require(z2==z2_evidence(z0["identity_batch_leads"],checks["pristine_canon_full"],z0["tau_shape"]),
            "HALTED-V5","pristine Z2 raw agreement")
    for mode in ("astra","band"):
        z3=checks["Z3"]["modes"][mode]
        require(z3["rounds"]==2 and z3["failing_count"]>0 and
                z3["columns_written"]==[z3["carrier_count"]]*2 and z3["weights_equal"] is True and
                len(z3["lambda_by_round"])==2 and all(len(v)==z3["failing_count"] and all(x==0. for x in v)
                    for v in z3["lambda_by_round"]),"HALTED-V5","Z3(a,b,c) raw conditions")
        for key in ("generations","logits_sha256"):
            require(len(z3["pristine_"+key])==len(z3["post_"+key])==96 and
                    z3["pristine_"+key]==z3["post_"+key],"HALTED-V5","Z3(d) "+key)
        require(z3["max_logit_delta"]==0.,"HALTED-V5","Z3(d) logits")
    z4=checks["Z4"]
    require(len(z4["identity_errors"])==len(z4["identity_bounds"])>0 and
            all(0<=e<=b for e,b in zip(z4["identity_errors"],z4["identity_bounds"])) and
            0<=z4["loop_relative_error"]<=1e-10 and len(z4["loop_rows"])==min(32,len(z4["identity_errors"])),
            "HALTED-V5","Z4 active assembly conditions")
    require(z7["same_forward_key_equality"] is True and z7["requirement_map_audited"] is True and
            1<=len(z7["controls"])<=8 and z7["nonzero_controls"]==sum(c["nonzero_realised"] for c in z7["controls"]),
            "HALTED-V5","Z7 key/active population")
    for c in z7["controls"]:
        require(c["columns_written"]==16 and c["post_error"]<=z7["tau_head"] and
                c["coefficient_error"]<=c["coefficient_bound"] and c["columns_error"]<=c["columns_bound"],
                "HALTED-V5","Z7 scalar/native reference")
    for w in checks["Z5"]["writes"]:
        require(set(map(tuple,w["changed_pairs"]))<=set(map(tuple,w["selected_pairs"])) and
                w["other_parameters_equal"] is True and w["solve_device"]=="cpu" and w["solve_dtype"]=="float64",
                "HALTED-V5","Z5 footprint/solve boundary")
    correlations=checks["V7"]["spearman"]
    require(set(correlations)==set(map(str,range(4,13))),"HALTED-V7","V7 cached layers incomplete")
    require(all(v>=.8 for v in correlations.values()),"HALTED-V7","V7 rank correlation <.80")
    require(checks["V8"]["cholesky"] is True,"HALTED-V8","G Cholesky failed")


def z2_evidence(identity_leads,evaluator,tau):
    checked=[i for i,row in enumerate(identity_leads) if not any(abs(v)<=tau for v in row)]
    return {"ok":bool(checked) and all(all(v>0 for v in identity_leads[i])==evaluator[i] for i in checked),
            "checked":len(checked),"ambiguous":len(identity_leads)-len(checked)}


def validate_probe(p,target,kinds):
    require(p["target"]==target and bool(target) and p["prompt_ids"] and
            all(type(y) is int and y>=0 for y in p["prompt_ids"]),"HALTED-V12","probe target/prompt IDs")
    for phase in ("pristine","post"):
        generated=p[phase+"_generated"]
        require(len(generated)==len(target) and all(type(y) is int and y>=0 for y in generated),
                "HALTED-V12","probe generated IDs")
        for kind in kinds:
            expected=generated==target if kind=="full" else generated[0]==target[0]
            require(type(p[phase+"_"+kind]) is bool and p[phase+"_"+kind]==expected,
                    "HALTED-V12","probe hit disagrees with generated IDs")


def probe_cells(arm):
    lengths=arm["target_lengths"]
    require(len(lengths)==24 and all(type(n) is int and n>=1 for n in lengths),
            "HALTED-V12","target lengths")
    expected={(v,i,d,s) for v in range(6) for i,n in enumerate(lengths)
              for d in range(1,n) for s in range(6)}
    cells={};identities=set()
    for p in arm["prefix_probes"]:
        key=(p["view"],p["fact"],p["depth"],p["subject"])
        require(key not in identities,"HALTED-V12","duplicate prefix probe")
        identities.add(key)
        require(bool(p["prompt_ids"]),"HALTED-V12","empty prefix prompt IDs")
        for hit in ("next","full"):
            require(type(p["post_"+hit]) is bool and type(p["pristine_"+hit]) is bool,
                    "HALTED-V12","nonboolean probe")
            cell=key[:3]+(hit,)
            cells[cell]=cells.get(cell,0)+int(p["post_"+hit] and not p["pristine_"+hit])
    require(identities==expected,"HALTED-V12","prefix population missing/extra view, fact, depth or subject")
    return cells


def subject_free(arm):
    expected={(i,d) for i,n in enumerate(arm["target_lengths"]) for d in range(1,n)}
    seen=set();hits=set()
    for p in arm["subject_free_probes"]:
        key=(p["fact"],p["depth"])
        require(key not in seen and bool(p["prompt_ids"]),"HALTED-V12","subject-free IDs")
        seen.add(key)
        require(type(p["post_full"]) is bool and type(p["pristine_full"]) is bool,
                "HALTED-V12","subject-free boolean")
        if p["post_full"] and not p["pristine_full"]:hits.add(p["fact"])
    require(seen==expected,"HALTED-V12","subject-free depth population")
    return len(hits)


def side_gates(z,a):
    zx,ax=z["locality_axes"],a["locality_axes"]
    require(len(z["F0"])==len(a["F0"])==6 and
            all(len(v)==6 and all(type(b) is bool for b in v) for v in z["F0"]+a["F0"]),
            "HALTED-V12","F0 must have six separate six-subject views")
    zp,ap=probe_cells(z),probe_cells(a)
    require(zp.keys()==ap.keys(),"HALTED-V12","baseline/candidate probe cells differ")
    require([p["prompt_ids"] for p in z["prefix_probes"]]==[p["prompt_ids"] for p in a["prefix_probes"]],
            "HALTED-V12","prefix prompt populations differ")
    result={"G1":count(zx["L1_flipped_to_edited_value"],12,"L1")<=count(ax["L1_flipped_to_edited_value"],12,"A L1")+1,
        "G2":all(sum(zv)<=sum(av)+1 for zv,av in zip(z["F0"],a["F0"])),
        "G3":z["locality_described_as"]>=a["locality_described_as"]-3.,
        "G4":count(zx["L3_top1_agree"],30,"L3_top1_agree")>=29,
        "G5":zx["generic_ppl_post"]<=ax["generic_ppl_post"]+.5,
        "G7":all(zp[k]<=ap[k]+1 for k in zp)}
    return result


def base_label(n,a,side):
    if n<=18 or n-a<=9:return "NULL"
    if not side:return "TRADEOFF"
    return "PARTIAL" if n<30 else "LEAD"


def substantive(arm,a):
    q=[]
    if not fit(arm["fit"],arm["canon_full_n"]):q.append("UNDERFIT")
    med=median(artifact_evidence(arm["write"])["ratios"])
    if med==INFINITY or med>.55:q.append("LARGE-WRITE")
    require([p["prompt_ids"] for p in arm["subject_free_probes"]]==
            [p["prompt_ids"] for p in a["subject_free_probes"]],"HALTED-V12","subject-free input mismatch")
    if subject_free(arm)>subject_free(a)+1:q.append("SUBJECT-FREE")
    if arm["write"]["wall_seconds"]>3600:q.append("EXCEEDS-TTL")
    return q


def attribution(z,band,a):
    if not fit(z["fit"],z["canon_full_n"]) or not fit(band["fit"],band["canon_full_n"]):
        return "ATTRIBUTION-UNINFORMATIVE"
    if z["write"]["carrier_count"]>2200:return "ATTRIBUTION-UNMATCHED-CAPACITY"
    if not all(side_gates(band,a).values()) or any(q in substantive(band,a)
                                for q in ("LARGE-WRITE","SUBJECT-FREE")):
        return "ATTRIBUTION-TRADEOFF"
    nb,n,ac=band["para_full_n"],z["para_full_n"],a["para_full_n"]
    if nb>=19 and nb-ac>=10 and nb>=n-5:return "BAND-RETAINS-QUALIFIED-GAIN"
    if nb<=18 or nb-ac<=9:return "BAND-NO-QUALIFIED-GAIN"
    return "BAND-PARTIAL-RETENTION"


def validate_counts(arm):
    for field,maximum in (("canon_full_n",24),("para_full_n",72),("para_first_n",72),("para_string_n",72)):
        count(arm[field],maximum,field)
    require(arm["para_string_n"]>=arm["para_full_n"],"HALTED-V10","string < full")
    rows=arm["rows"]
    require(len(rows)==24,"HALTED-V12","binding fact population")
    require(all(type(row["canon_full"]) is bool for row in rows),"HALTED-V12","canonical hit type")
    for key in ("para_full_hits","para_first_hits","para_string_hits"):
        require(all(len(row[key])==3 and all(type(v) is bool for v in row[key]) for row in rows),
                "HALTED-V12","held-out 3x24 population")
    # Canonical success is the binding evaluator's count, not the observation's sign count.
    for field,key in (("canon_full_n","canon_full"),("para_full_n","para_full_hits"),
                      ("para_first_n","para_first_hits"),("para_string_n","para_string_hits")):
        actual=sum(row[key] if key=="canon_full" else sum(row[key]) for row in rows)
        require(actual==arm[field],"HALTED-V12","count/detail mismatch: "+field)
    require(arm["per_template_n"]==[sum(r["para_full_hits"][j] for r in rows) for j in range(3)] and
            arm["per_fact_n"]==[sum(r["para_full_hits"]) for r in rows] and
            arm["per_edge_behavior_pass"]==[all(r["para_full_hits"]) for r in rows],
            "HALTED-V12","binding decomposition vectors")
    correct=sum(r["tf_correct"] for r in rows);total=sum(r["tf_total"] for r in rows)
    numerator=sum(x and y for r in rows for x,y in zip(r["para_first_hits"],r["para_full_hits"]))
    require(arm["tf_pertok_cont"]==(round(100*correct/total,1) if total else None) and
            arm["cond_full_given_first"]==(round(numerator/arm["para_first_n"],3) if arm["para_first_n"] else None),
            "HALTED-V12","binding diagnostic aggregates")


def validate_manifest(parts):
    require(all(k in parts and parts[k] is not None for k in INPUT_KEYS),"HALTED-V12","manifest inputs missing")
    require(sha(parts["go_sha256"]),"HALTED-V12","go record SHA missing or malformed")
    require(parts["settings"]==SETTINGS and parts["seed"]==0 and
            parts["model_revision"]=="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b","HALTED-V12","frozen settings/revision")
    require(set(parts["requests"])==set(parts["batches"])==set(ARMS),"HALTED-V12","manifest arm population")
    for name in ARMS:
        requests=parts["requests"][name];batch=parts["batches"][name]
        require(len(requests)==24 and len({r["subject"] for r in requests})==24 and
                all(isinstance(r["target_new"]["str"],str) and r["target_new"]["str"] and
                    isinstance(r["prompt"],str) and "{}" in r["prompt"] for r in requests),
                "HALTED-V12","request JSON population")
        targets=batch["target_ids"];prompts=batch["prompt_ids"]
        require(len(targets)==24 and len(prompts)==len(batch["input_ids"])==len(batch["attention_mask"])==144 and
                len(batch["frames"])==6 and batch["target_lengths"]==list(map(len,targets)) and
                all(row and all(type(y) is int and y>=0 for y in row) for row in targets+prompts),
                "HALTED-V12","ordered batch IDs/populations")
        expected=[];sequences=[]
        for i,ids in enumerate(targets):
            for v in range(6):
                row=i*6+v;prompt=prompts[row];sequences.append(prompt+ids[:-1])
                expected.extend({"row":row,"fact":i,"view":v,"q":q,"index":len(prompt)+q-1,"target":y}
                                for q,y in enumerate(ids))
        pad=max(map(len,sequences))
        require(batch["T_pad"]==pad and batch["requirements"]==expected and
                all(actual==seq+[batch["pad_token_id"]]*(pad-len(seq)) for actual,seq in zip(batch["input_ids"],sequences)) and
                batch["attention_mask"]==[[1]*len(seq)+[0]*(pad-len(seq)) for seq in sequences],
                "HALTED-V12","right-padding or requirement index drift")
    for group in ("engine_sources","hparams","screens","tokenizer","safetensors"):
        require(isinstance(parts[group],dict) and bool(parts[group]) and all(sha(v) for v in parts[group].values()),
                "HALTED-V12","source/tokenizer SHA group "+group)
    require(parts["engine_sources"].get("memit_dry_run/memit/memit/memit_main.py")==ENGINE_SHA and
            "experiments/track_c/c10e_bandknob.py" in parts["engine_sources"] and
            {"tokenizer.json","tokenizer_config.json"}<=parts["tokenizer"].keys(),
            "HALTED-V12","engine/harness/tokenizer identity omitted")
    require(set(parts["covariances"])==set(map(str,range(4,13))) and
            all(isinstance(v["path"],str) and v["path"] and sha(v["sha256"]) for v in parts["covariances"].values()),
            "HALTED-V12","cached covariance provenance")
    require(parts["forward_settings"]["use_cache"] is False and parts["forward_settings"]["logits_to_keep"]==0 and
            parts["forward_settings"]["padding_side"]=="right" and
            parts["environment"]["device"]=="mps" and parts["environment"]["dtype"]=="float16" and
            parts["environment"]["transformers"]=="4.51.0" and
            parts["solver_backend"]["dtype"]=="float64" and parts["solver_backend"]["device"]=="cpu",
            "HALTED-V12","native forward/CPU backend provenance")
    data=parts["dataset"];ids=data["ordered_token_ids"]
    require(len(data["revision"])==40 and len(data["row_ids"])==len(data["text_sha256"])==len(ids)==1000 and
            len(set(data["row_ids"]))==1000 and all(sha(v) for v in data["text_sha256"]) and
            all(1<=len(row)<=100 and all(type(y) is int and y>=0 for y in row) for row in ids) and
            data["nonpadding_tokens"]==sum(map(len,ids)),"HALTED-V12","reference dataset population/counts")


def validate_raw_probes(arm,batch):
    probe_cells(arm);subject_free(arm)
    for field,kinds in (("prefix_probes",("next","full")),("subject_free_probes",("full",))):
        for p in arm[field]:
            target=batch["target_ids"][p["fact"]];depth=p["depth"]
            require(p["prompt_ids"][-depth:]==target[:depth],"HALTED-V12","prefix position IDs")
            validate_probe(p,target[depth:],kinds)
    raw=arm["F0_raw"];firsts=sorted({ids[0] for ids in batch["target_ids"]})
    for phase in ("pristine","post"):
        require(len(raw[phase])==36 and [(p["view"],p["subject"]) for p in raw[phase]]==
                [(v,s) for v in range(6) for s in range(6)],"HALTED-V12","F0 raw population")
        require(all(p["first_ids"]==firsts and p["edited_value"]==(p["top1"] in firsts)
                    for p in raw[phase]),"HALTED-V12","F0 raw top1/hit mismatch")
    require(arm["F0"]==[[p["edited_value"] for p in raw["post"] if p["view"]==v] for v in range(6)] and
            [p["prompt_ids"] for p in raw["pristine"]]==[p["prompt_ids"] for p in raw["post"]],
            "HALTED-V12","F0 population/summary drift")
    relation=arm["relation_label_probes"];keys=[(i,f) for i in range(24) for f in ("{} is a","{} is associated with")]
    for phase in ("pristine","post"):
        require([(p["fact"],p["frame"]) for p in relation[phase]]==keys and
                all(p["first_ids"]==firsts and p["edited_value"]==(p["top1"] in firsts) for p in relation[phase]),
                "HALTED-V12","relation-label probe population")
    require([p["prompt_ids"] for p in relation["pristine"]]==[p["prompt_ids"] for p in relation["post"]] and
            relation["top1_changes"]==sum(a["top1"]!=b["top1"] for a,b in zip(relation["pristine"],relation["post"])) and
            relation["flips_to_values"]==sum(a["top1"]!=b["top1"] and b["edited_value"] for a,b in zip(relation["pristine"],relation["post"])),
            "HALTED-V12","relation-label aggregates")
    vectors=arm["locality_axes"]["per_edge_vectors"]
    require(len(vectors["L1"])==12 and len(vectors["L3"])==30 and
            all(p["agree"]==(p["pre_id"]==p["post_id"]) and
                p["flipped_to_edited_value"]==(p["pre_id"]!=p["post_id"] and p["post_id"] in firsts)
                for values in vectors.values() for p in values),"HALTED-V12","locality edge vectors")
    require(arm["locality_axes"]["L1_flipped_to_edited_value"]==sum(p["flipped_to_edited_value"] for p in vectors["L1"]) and
            arm["locality_axes"]["L3_top1_agree"]==sum(p["agree"] for p in vectors["L3"]),
            "HALTED-V12","locality counts differ from edges")


def validate(record):
    finite_json(record)
    require(record["schema"]==SCHEMA,"HALTED-V12","schema")
    require(isinstance(record["attempt_id"],str) and record["attempt_id"] and record["process"] in (1,2),
            "HALTED-V12","attempt/process identity")
    fp=record["fingerprint"]
    require(fp["sha256"]==ENGINE_SHA and fp["cov_cpu_sites"]==3 and fp["start"]==fp["end"],
            "HALTED-V1","engine/harness source identity changed")
    recipes=record["recipes"]
    for name,recipe in recipes.items():
        g=recipe["law5_gate"]
        require(g["ok"] is True and g["expr_delta"]<.05 and g["loc_delta"]<3,
                "HALTED-V2",name+" standing LAW#5")
    require(sha(record["H_pristine"]) and record["restores"] and
            all(r["ok"] is True and r["layers"]==36 and r["hooks_ok"] is True for r in record["restores"]),
            "HALTED-V3","full snapshot/restore/hooks")
    law3(recipes["A"])
    check_instruments(record["checks"])
    for name,recipe in recipes.items():
        if name in ("Z","Z-band"):
            audit=recipe["audit"]
            require(audit["astra_calls"]==len(recipe["arms"]) and audit["original_calls"]==0 and
                    audit["Z_OVERRIDE_HITS"]==0,"HALTED-V9",name+" wrapper counters")
        for arm in recipe["arms"].values():
            validate_counts(arm)
    require(bool(record["memory"]),"HALTED-V11","no memory observations")
    for m in record["memory"]:
        require(m["driver_bytes"]<=32*2**30 and m["driver_bytes"]+m["rss_bytes"]<=40*2**30 and
                m["float64_on_mps"] is False,"HALTED-V11","memory/precision ceiling")
    manifest=record["manifest"];parts=manifest["parts"]
    validate_manifest(parts)
    require(parts["prereg_sha256"]==PREREG_SHA and record["H_in"]==manifest["H_in"]==json_digest(parts)
            and parts["H_pristine"]==record["H_pristine"],"HALTED-V12","manifest identity")
    for key in ("context_templates_sha256","dstats_sha256","G_sha256","driver_sha256","reader_sha256"):
        require(sha(parts[key]),"HALTED-V12","missing SHA "+key)
    require(all(sha(record["artifact_hashes"][k]) for k in ("context_templates.json","dstats.pt","G.pt",
            "pristine_hash.json","manifest.json","overlap_audit.json")),"HALTED-V12","record hashes")
    require(all(record["artifact_hashes"][file]==parts[key] for file,key in
                (("context_templates.json","context_templates_sha256"),("dstats.pt","dstats_sha256"),("G.pt","G_sha256"))) and
            fp["start"]==parts["engine_sources"],"HALTED-V12","source/file hash bindings")
    stage=record["stage_completed"]
    require(type(stage) is int and stage in (1,2),"HALTED-V12","completed stage")
    ceilings=record["budget"]["ceilings"];origins=record["budget"]["origins"]
    require(type(ceilings["stage01"]) in (int,float) and 7200<=ceilings["stage01"]<=10800 and
            math.isfinite(ceilings["stage01"]) and isinstance(origins["stage01"],(int,float)),
            "HALTED-V12","phase01 clock provenance")
    if stage==2:require(ceilings["stage2"] is not None and ceilings["stage2"]>0 and "stage2" in origins,
                        "HALTED-BUDGET","completed stage2 lacked launch ceiling/entry origin")
    if record["process"]==2:
        require(ceilings["stage3"] is not None and ceilings["stage3"]>0 and origins["stage3"]==origins["stage01"],
                "HALTED-BUDGET","second-process pre-import clock/ceiling")
    require(A7 in recipes["Z"]["arms"],"HALTED-V12","Z A7 missing")
    if stage==2:
        require(set(recipes["Z"]["arms"])==set(ARMS) and A7 in recipes["Z-band"]["arms"],
                "HALTED-V12","completed stage2 evidence missing")
    else:
        for key in ("G0","Z-band"):
            omission=record["omissions"][key]
            require(omission["status"]=="NOT-RUN" and omission["reason"] in
                    ("K1","AWAITING-STAGE2","ABSENT-CEILING"),"HALTED-V12","unjustified omission")
    require(all(k in record["certificate"] for k in ("artifact_identity","numeric_behavioral_reproduction")),
            "HALTED-V12","certificate fields absent")
    require(not record["budget"]["halted"],"HALTED-BUDGET","elapsed deadline/projection")
    require(bool(record["budget"]["history"]),"HALTED-V12","missing budget projections")
    for projection in record["budget"]["history"]:
        require(projection.get("ceilings")==ceilings and
                all(k in ceilings and v["ceiling_s"]==ceilings[k] for k,v in projection["scopes"].items()),
                "HALTED-V12","projection ceilings differ from record ceilings")
        costs=projection["components_s"]
        require(costs and all(v>0 for v in costs.values()),"HALTED-BUDGET","zero unknown cost")
        require(all(0<=v["elapsed_s"] and v["remaining_s"]>=sum(costs.values()) and
                    v["elapsed_s"]+v["remaining_s"]<=v["ceiling_s"] for v in projection["scopes"].values()),
                "HALTED-BUDGET","recorded projection exceeded ceiling")
    for name,recipe in recipes.items():
        for arm_name,arm in recipe["arms"].items():
            validate_fit(arm,parts["batches"][arm_name]);validate_raw_probes(arm,parts["batches"][arm_name])
            require([row["subj"] for row in arm["rows"]]==[r["subject"] for r in parts["requests"][arm_name]],
                    "HALTED-V12","ordered evaluator fact population")
    for name in ("Z","Z-band"):
        for arm_name,arm in recipes.get(name,{"arms":{}})["arms"].items():
            w=arm["write"]
            require(sha(w["H_out"]) and type(w["rounds_used"]) is int and 0<=w["rounds_used"]<=10 and
                    w["stop_reason"] in ("objective met","round cap"),"HALTED-V12","write record")
            require(len(w["round_seconds"])==w["rounds_used"] and w["stage"]==(1 if name=="Z" and arm_name==A7 else 2),
                    "HALTED-V12","write round/stage population")
            if w["stage"]==1:
                require(all(t<=120 for t in w["round_seconds"]),"HALTED-BUDGET","stage1 round >120 seconds")
            artifact_evidence(w)
            S=w["carriers"];T=sum(parts["batches"][arm_name]["target_lengths"])
            if name=="Z":
                n=min(440,max(16,math.ceil(16*T/9)))
                require(len(S)==9 and all(len(cols)==n for cols in S.values()),"HALTED-V12","SemCon capacity")
            else:
                total=min(recipes["Z"]["arms"][A7]["write"]["carrier_count"],2200);q,r=divmod(total,5)
                require(set(S)==set(map(str,range(4,9))) and all(len(S[str(l)])==q+int(l-4<r) for l in range(4,9)),
                        "HALTED-V12","band capacity distribution")
            post1=[p for p in record["checks"]["post_write_checks"] if p["recipe"]==name and p["arm"]==arm_name]
            post2=[p for p in record["checks"]["post_write_Z2"] if p["recipe"]==name and p["arm"]==arm_name]
            require(len(post1)==len(post2)==1 and post1[0]["Z1_error"]<=record["checks"]["Z7"]["tau_head"] and
                    post1[0]["Z5_ok"] is True,"HALTED-V5","post-loop Z1/Z5 evidence")
            expected=z2_evidence(arm["post_fit_observation"][0],[r["canon_full"] for r in arm["rows"]],record["checks"]["Z0"]["tau_shape"])
            require(expected["ok"] and {k:post2[0][k] for k in expected}==expected,"HALTED-V5","post-write Z2 agreement")
    where=[r["where"] for r in record["restores"]]
    for name,recipe in recipes.items():
        require("before recipe "+name in where and "after recipe "+name in where,"HALTED-V3","recipe restore point absent")
        if name!="A":
            for arm_name in recipe["arms"]:
                require("before write "+arm_name in where and "restore_hook "+arm_name in where,
                        "HALTED-V3","arm restore point absent")


def label_string(base,qualifiers):
    return base+"".join("-"+q for q in QUAL_ORDER if q in qualifiers)


def classify_candidate(z,a,gates,stage,band=None,write_seconds=(),ceilings=None):
    """§3 partition conditional on validity. read_process enforces V1–V13 first."""
    base=base_label(z["para_full_n"],a["para_full_n"],all(gates.values()))
    q=substantive(z,a);underfit="UNDERFIT" in q
    if any(t>3600. for t in write_seconds) and "EXCEEDS-TTL" not in q:q.append("EXCEEDS-TTL")
    if base=="NULL" and underfit:base="UNDERFIT";q.remove("UNDERFIT")
    clean=base in ("PARTIAL","LEAD") and not q
    budgeted=ceilings is None or ceilings["stage"+str(stage+1)] is not None
    next_stage=2 if stage==1 and clean and budgeted else 3 if stage==2 and clean and budgeted else None
    if stage==1 and next_stage is None:q.append("STAGE1")
    if stage==2:q.append("SINGLE-PROCESS")
    attr=attribution(z,band,a) if stage==2 else "NOT-RUN"
    return {"label":label_string(base,q),"base_label":base,"qualifiers":q,"gates":gates,
        "FIT":not underfit,"n":z["para_full_n"],"a":a["para_full_n"],
        "gain":z["para_full_n"]-a["para_full_n"],"attribution":attr,"next_stage":next_stage,
        "replicated":False,"lead_replicated":False,"artifact_identity":"NOT-EVALUATED",
        "numeric_behavioral_reproduction":"NOT-EVALUATED"}


def stage_omissions(process,stage,next_stage,ceilings,decision=None):
    eligible=next_stage is not None or (decision is not None and decision["base_label"] in ("PARTIAL","LEAD") and
        not (set(decision["qualifiers"])-{"STAGE1","SINGLE-PROCESS"}))
    reason="ABSENT-CEILING" if eligible and ceilings["stage"+str(stage+1)] is None else (
        ("K1" if stage==1 else "K2") if next_stage is None else ("AWAITING-STAGE2" if stage==1 else "AWAITING-STAGE3"))
    omissions={k:{"status":"NOT-RUN","reason":reason} for k in ("G0","Z-band")} if stage==1 else {}
    omissions["process2"]={"status":"NOT-APPLICABLE","reason":"CURRENT-PROCESS"} if process==2 else {"status":"NOT-RUN","reason":reason}
    return omissions


def read_process(record):
    try:
        if record.get("outcome")=="HALTED":
            return {"label":record["halt"]["code"],"scientific_verdict":False,"detail":record["halt"]["detail"]}
        validate(record)
        a=record["recipes"]["A"]["arms"][A7];z=record["recipes"]["Z"]["arms"][A7]
        gates=side_gates(z,a)
        stage=record["stage_completed"]
        if stage==2:
            gates["G0"]=all(record["recipes"]["Z"]["arms"][k]["para_full_n"]>=68 for k in (A1,A2))
        seconds=[v["write"]["wall_seconds"] for name in ("Z","Z-band") for v in
                 record["recipes"].get(name,{"arms":{}})["arms"].values()]
        result=classify_candidate(z,a,gates,stage,record["recipes"]["Z-band"]["arms"][A7] if stage==2 else None,seconds,record["budget"]["ceilings"])
        require(record["omissions"]==stage_omissions(record["process"],stage,result["next_stage"],record["budget"]["ceilings"],result),
                "HALTED-V12","omissions disagree with K1/K2 or frozen launch ceilings")
        return {**result,"scientific_verdict":True}
    except Halt as exc:
        return {"label":exc.code,"scientific_verdict":False,"detail":exc.detail}
    except (KeyError,TypeError,ValueError,IndexError) as exc:
        return {"label":"HALTED-V12","scientific_verdict":False,"detail":str(exc)}


def r1_error_pass(error):
    return type(error) in (float,int) and math.isfinite(error) and 0<=error<=.001


def aggregate(p1,p2,repro):
    rank={"NULL":0,"UNDERFIT":0,"TRADEOFF":1,"PARTIAL":2,"LEAD":3}
    b1,b2=p1["base_label"],p2["base_label"]
    base=min((b1,b2),key=lambda b:rank[b])
    q=set(p1["qualifiers"]+p2["qualifiers"])-{"SINGLE-PROCESS"}
    if rank[base]==0 and (b1=="UNDERFIT" or b2=="UNDERFIT" or "UNDERFIT" in q):
        base="UNDERFIT";q.discard("UNDERFIT")
    incomplete=repro["R1"]["status"]=="NOT-EVALUATED" or bool(repro["R1"].get("omitted_arms"))
    r1=repro["R1"]["status"]=="PASS"
    r2=repro["R2"]["difference"]<=2;r3=repro["R3"]["disagree"]<=3
    clean_pair=all(b in ("PARTIAL","LEAD") for b in (b1,b2)) and not q
    replicated=clean_pair and r1 and r2 and r3
    if incomplete:q.add("REPRO-INCOMPLETE")
    if repro["R1"]["status"]=="FAIL" or not r2 or not r3:q.add("NOT-REPRODUCIBLE")
    if b1!=b2 and not (clean_pair and r1 and r2 and r3):q.add("NOT-REPLICATED")
    qualifiers=[v for v in QUAL_ORDER if v in q]
    return {"label":label_string(base,qualifiers),"base_label":base,"qualifiers":qualifiers,
            "replicated":replicated,"lead_replicated":replicated and b1==b2=="LEAD",
            "scientific_verdict":True,"artifact_identity":repro["artifact_identity"],
            "numeric_behavioral_reproduction":repro["numeric_behavioral_reproduction"]}


def read_run(p1,p2=None,repro=None):
    first=read_process(p1)
    if not first["scientific_verdict"] or p2 is None:return first
    second=read_process(p2)
    if not second["scientific_verdict"]:return second
    try:
        require(p1["budget"]["ceilings"]==p2["budget"]["ceilings"],"HALTED-V12","process ceilings differ")
        require(p1["pid"]!=p2["pid"] and p2["process"]==2,"HALTED-V12","not a fresh second process")
        require(p1["H_pristine"]==p2["H_pristine"],"HALTED-V3","process2 pristine differs")
        require(p1["H_in"]==p2["H_in"],"HALTED-V12","process2 input manifest differs")
        require(p1["attempt_id"]==p2["attempt_id"],"HALTED-V12","process2 attempt differs")
        require(repro is not None,"HALTED-V12","missing reproduction certificate")
        measured=reproduction_evidence(p1,p2)
        require(repro==measured,"HALTED-V12","reproduction certificate disagrees with stored evidence")
        return aggregate(first,second,measured)
    except Halt as exc:return {"label":exc.code,"scientific_verdict":False,"detail":exc.detail}
    except (KeyError,TypeError):return {"label":"HALTED-V12","scientific_verdict":False,"detail":"reproduction record"}


def read_directory(out):
    out=Path(out)
    try:
        records=[]
        for directory,number in ((out,1),(out/"process2",2)):
            if not directory.exists():continue
            runpath=directory/"run.json"
            run=json.loads(runpath.read_text()) if runpath.exists() else {}
            passpath=directory/f"pass_p{number}.json"
            record=json.loads(passpath.read_text()) if passpath.exists() else None
            haltpath=directory/f"halt_p{number}.json"
            halt=json.loads(haltpath.read_text())["halt"] if haltpath.exists() else run.get("halt")
            if halt:
                return {"label":halt["code"],"scientific_verdict":False,"detail":halt["detail"],
                    "observations":records+([record] if record is not None else [])}
            require(run["closed"] is True,"HALTED-V12","attempt still running; no final verdict")
            launch=run["launch"]
            require(all(record["budget"]["ceilings"][k]==launch[k] for k in ("stage01","stage2","stage3")),
                    "HALTED-V12","pass ceilings differ from launch")
            require(launch["stage01"]==launch["go"]["ceilings"]["stage01"] and
                    all(launch[k] is None or launch[k]==launch["go"]["ceilings"][k] for k in ("stage2","stage3")),
                    "HALTED-V12","launch ceiling not the go selection")
            require(launch["benchmark"]["sha256"]==launch["go"]["benchmark_sha256"],
                    "HALTED-V12","launch benchmark differs from go")
            require(record["attempt_id"]==run["attempt_id"] and record["pid"]==run["pid"],"HALTED-V12","terminal attempt binding")
            for name,expected in record["artifact_hashes"].items():
                require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==expected,"HALTED-V12","on-disk artifact drift: "+name)
            require(json.loads((directory/"manifest.json").read_text())==record["manifest"],"HALTED-V12","manifest file differs")
            pin=json.loads((directory/"pristine_hash.json").read_text())
            require(pin["H_pristine"]==record["H_pristine"] and set(pin["layers"])==set(map(str,range(36))) and
                    pin["parameters"] and pin["safetensors"],"HALTED-V12","pristine import record incomplete")
            records.append(record)
        require(bool(records),"HALTED-V12","no process record")
        repro=json.loads((out/"repro.json").read_text()) if len(records)==2 else None
        return read_run(records[0],records[1] if len(records)==2 else None,repro)
    except Halt as exc:return {"label":exc.code,"scientific_verdict":False,"detail":exc.detail}
    except (OSError,KeyError,ValueError,TypeError) as exc:return {"label":"HALTED-V12","scientific_verdict":False,"detail":str(exc)}


def main():
    out=Path(sys.argv[1]) if len(sys.argv)==2 else Path(LLMDB_ROOT)/"results/c10z_astra"
    reading=read_directory(out)
    print(json.dumps(reading,indent=2,allow_nan=False))
    return 0 if reading["scientific_verdict"] else 2


if __name__=="__main__":sys.exit(main())
