#!/usr/bin/env python3
"""D-C10w-p2rerun: one sealed P2 eval retry; frozen reader/step0 bytes stay unchanged.

prepare/archive are operator-run mutations. verify is read-only. The overlay delegates
all existing reader/dispatcher checks; its sole frozen-source exception is evaluator A1.
"""
import argparse, contextlib, json, os, re, sys
from pathlib import Path

W = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(W/"code/lab/track_c"))
import c10w_oracle_read as R

AMENDMENT = {'schema': 1,
 'decision_id': 'D-C10w-p2rerun',
 'step0': {'path': 'experiments/c10w/runs/c10w_oracle/step0_20261007T223638_531381Z/step0.json',
           'sha256': '82ef86437b5ba00fa78a1b55cfe64e4d85baaceb37aa0726f3015c2b2f7d673e'},
 'p2_directory': 'experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z',
 'evaluator': {'path': 'code/lab/track_c/c10w_oracle_eval.py',
               'old_sha256': '21f39d81695a3dc9fc144af631b48c7377c5efe08a9bf93db011dcaa8b602027',
               'new_sha256': '45f2839d0fd576bd131072c0ae8b009a0cb371ddca49b1edadb062944a775f1e'},
 'unified_diff': {'path': 'code/lab/runners/c10w_p2_evaluator_A1.diff',
                  'sha256': 'ca0e00df578f535bff2b5c8a878dfc9138b88e4c7c357e156a65b177a2fe06ff'},
 'diagnostic_path': 'experiments/c10w/runs/unattributed/halts/s29_c10w_p2_cosine_halt_diagnostic.json',
 'reason': 'One permitted driver fix: accumulate same-seed cosine dot and norms in CPU float64 after the '
           'unchanged fp32 merged delta; rerun the compromised P2 eval under D-C10w-p2rerun. No scientific '
           'thresholds, training, or other frozen sources change.'}
AMENDMENT_SHA256 = "4791183ab5ddc68cbecff1653a1f80508fb4806d5e957fde63a25a498037d17f"
P1_REL = "experiments/c10w/runs/c10w_oracle/p1_20261007T223707_598959Z"
DECISION = "D-C10w-p2rerun"
INNER = ("HALT.json", "eval.json", "eval_halt.json", "p2-eval.log")
GATE_NAME = re.compile(r"p2-eval\.gate\.\d{8}T\d{6}\.\d+\.json")
ORIGINAL_LOAD_FROZEN = R.load_frozen
ORIGINAL_ATTEMPT_SHA256 = {
 "experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z/HALT.json": "d82e41237067ac3ffd10c4a2937a189cce9553ccd1fc3fa1b87ae6d4a7d1edb1",
 "experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z/eval.json": "0b110f3b91a2674275542fa5c3a6a19a00b5738371c85b9b5d8af54c3e888153",
 "experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z/eval_halt.json": "6d2f749ff98ab9abb418a98e5f5852e9d08cb8eb5fea2ff9792d97fb08f141b7",
 "experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z/p2-eval.log": "15209a0601c1b956399e272326dcc395103ec6e82e3469f6df3c83d12042658d",
 "experiments/c10w/runs/c10w_oracle/logs/p2-eval.log": "5b614a25104b8a97f98c016325741ea0b5737ecb8f6625686a72f16ed3e1b5b4",
 "experiments/c10w/runs/c10w_oracle/logs/p2-eval.gate.20261007T222229.91288.json": "57b5bc3df8172eb1ebef775f07bf989b32a0c2c84c4003b0e62598a28bad388e"}


def step0_path():
    return (W/AMENDMENT["step0"]["path"]).parent


def p2_path():
    return W/AMENDMENT["p2_directory"]


def regular(path):
    path=Path(path)
    R.require(path.is_relative_to(W) and not any(p.is_symlink() for p in (path,*path.parents) if p.is_relative_to(W)),
              "rerun path is outside worktree or symlinked: "+str(path))
    R.require(path.is_file(),"missing rerun file: "+str(path))


def plan_checks(directory=None, step=None):
    directory=step0_path() if directory is None else Path(directory).resolve()
    R.require(directory==step0_path(),"amendment belongs to another step0")
    regular(directory/"step0.json")
    R.require(R.sha_file(directory/"step0.json")==AMENDMENT["step0"]["sha256"],"amendment step0 hash mismatch")
    step=R.load_json(directory/"step0.json") if step is None else step
    old=step["sources"]["evaluator"]; expected=AMENDMENT["evaluator"]
    R.require(old=={"path":str(W/expected["path"]),"sha256":expected["old_sha256"]},"amendment original evaluator mismatch")
    regular(W/expected["path"])
    R.require(R.sha_file(W/expected["path"])==expected["new_sha256"],"amendment new evaluator mismatch")
    regular(W/AMENDMENT["unified_diff"]["path"])
    R.require(R.sha_file(W/AMENDMENT["unified_diff"]["path"])==AMENDMENT["unified_diff"]["sha256"],"amendment diff mismatch")
    regular(W/AMENDMENT["diagnostic_path"])
    return step


def verify_amendment(directory=None, step=None):
    plan_checks(directory,step)
    path=step0_path()/"amendment_A1_evaluator.json"; regular(path)
    R.require(R.sha_file(path)==AMENDMENT_SHA256 and R.load_json(path)==AMENDMENT,"amendment record hash/content mismatch")
    return R.file_ref(path)


def load_frozen(directory):
    step=R.load_json(Path(directory)/"step0.json")
    ref=step["sources"].get("evaluator")
    if ref is None or (Path(ref["path"]).is_file() and R.sha_file(ref["path"])==ref["sha256"]):
        return ORIGINAL_LOAD_FROZEN(directory)
    amendment=verify_amendment(directory,step)
    original=R.verify_ref
    def verify(source):
        if source==ref:
            R.require(R.sha_file(source["path"])==AMENDMENT["evaluator"]["new_sha256"],"amended evaluator changed")
        else: original(source)
    R.verify_ref=verify
    try: frozen=ORIGINAL_LOAD_FROZEN(directory)
    finally: R.verify_ref=original
    return {**frozen,"evaluator_amendment":amendment}


def prepare():
    step=plan_checks()
    for name,ref in step["sources"].items():
        if name!="evaluator": R.verify_ref(ref)
    for ref in step["files"].values(): R.verify_ref(ref)
    path=step0_path()/"amendment_A1_evaluator.json"
    if not path.exists():
        with path.open("x",encoding="utf-8") as f: f.write(json.dumps(AMENDMENT,ensure_ascii=False,indent=2)+"\n")
    ref=verify_amendment(); load_frozen(step0_path())
    return ref


def assert_selection():
    base=W/"experiments/c10w/runs/c10w_oracle"
    for prefix,expected in (("step0",step0_path()),("p1",W/P1_REL),("p2",p2_path())):
        paths=sorted(p for p in base.glob(prefix+"_*") if p.is_dir())
        R.require(paths and paths[-1]==expected and not expected.is_symlink(),"rerun selection differs: "+prefix)


def archive_sources():
    p2=p2_path(); logs=W/"experiments/c10w/runs/c10w_oracle/logs"
    inner={p.name for p in p2.iterdir() if p.name.startswith(("HALT","eval","verdict","p2-eval"))}
    outer={p.name for p in logs.glob("p2-eval*")}
    gates={n for n in outer if GATE_NAME.fullmatch(n)}
    R.require(inner==set(INNER) and gates and outer=={"p2-eval.log",*gates},"missing or unexpected halted eval artifact")
    return [*(p2/n for n in INNER),logs/"p2-eval.log",*(logs/n for n in sorted(gates))]


def archive():
    path=p2_path()/"attempt1_halted/manifest.json"
    if path.exists(): return verify_archive()
    amendment=verify_amendment(); load_frozen(step0_path()); assert_selection()
    p2=p2_path(); logs=W/"experiments/c10w/runs/c10w_oracle/logs"
    R.require(not (p2/"attempt1_halted").exists() and not (logs/"attempt1_halted").exists(),"partial/unexpected archive exists")
    R.require(not (p2/"reattempt2.json").exists(),"re-attempt already reserved")
    sources=archive_sources()
    for source in sources: regular(source)
    R.require({str(p.relative_to(W)):R.sha_file(p) for p in sources}==ORIGINAL_ATTEMPT_SHA256,
              "halted attempt differs from reviewed original bytes")
    halt=R.load_json(p2/"HALT.json"); failed=R.load_json(p2/"eval_halt.json")
    R.require(halt.get("stage")=="p2-eval" and halt.get("status")=="HALT" and failed.get("phase")=="P2"
              and "invalid same-seed cosine" in failed.get("reason",""),"unexpected HALT cause/stage")
    R.check_eval_seconds(failed["wall_seconds"])
    entries=[]
    for source in sources:
        dest=source.parent/"attempt1_halted"/source.name
        entries.append({"source":str(source.relative_to(W)),"destination":str(dest.relative_to(W)),
                        "sha256":R.sha_file(source),"size":source.stat().st_size})
    (p2/"attempt1_halted").mkdir(); (logs/"attempt1_halted").mkdir()
    for entry in entries: (W/entry["source"]).rename(W/entry["destination"])
    record={"decision_id":DECISION,"p2_directory":AMENDMENT["p2_directory"],"evaluator_amendment":amendment,
            "reason":"Preserve the compromised first P2 eval; one reviewed GPU re-attempt under D-C10w-p2rerun.",
            "halted_eval_wall_seconds":failed["wall_seconds"],"files":entries}
    with path.open("x",encoding="utf-8") as f: f.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    return verify_archive()


def verify_archive():
    path=p2_path()/"attempt1_halted/manifest.json"; regular(path); record=R.load_json(path)
    R.require(record.get("decision_id")==DECISION and record.get("p2_directory")==AMENDMENT["p2_directory"]
              and record.get("evaluator_amendment")==verify_amendment(),"archive identity/amendment mismatch")
    entries=record["files"]; p2=p2_path(); logs=W/"experiments/c10w/runs/c10w_oracle/logs"
    expected={str((p2/n).relative_to(W)) for n in INNER}|{str((logs/"p2-eval.log").relative_to(W))}
    sources={e["source"] for e in entries}; gates=sources-expected
    R.require({e["source"]:e["sha256"] for e in entries}==ORIGINAL_ATTEMPT_SHA256,"archive original-byte identity mismatch")
    R.require(len(sources)==len(entries) and expected<=sources and gates and all(
        Path(n).parent==logs.relative_to(W) and GATE_NAME.fullmatch(Path(n).name) for n in gates),"archive move set mismatch")
    destinations=set()
    for entry in entries:
        source=W/entry["source"]; dest=source.parent/"attempt1_halted"/source.name
        R.require(entry["destination"]==str(dest.relative_to(W)),"archive destination mismatch")
        regular(dest); R.require(R.sha_file(dest)==entry["sha256"] and dest.stat().st_size==entry["size"],"archived file hash/size mismatch")
        destinations.add(dest)
    actual=set((p2/"attempt1_halted").iterdir())|set((logs/"attempt1_halted").iterdir())
    R.require(actual==destinations|{path},"unexpected archived file")
    failed=R.load_json(p2/"attempt1_halted/eval_halt.json")
    R.require(failed.get("phase")=="P2" and "invalid same-seed cosine" in failed.get("reason","")
              and record["halted_eval_wall_seconds"]==failed["wall_seconds"],"archive halt budget/cause mismatch")
    R.check_eval_seconds(failed["wall_seconds"])
    return R.file_ref(path)


def prerequisites(directory):
    R.require(Path(directory).resolve()==p2_path(),"re-attempt belongs to another P2 directory")
    assert_selection(); amendment=verify_amendment(); load_frozen(step0_path()); manifest=verify_archive()
    R.require(not (p2_path()/"HALT.json").exists(),"P2 HALT remains")
    logs=W/"experiments/c10w/runs/c10w_oracle/logs"; training=[]
    for stage in R.TRAIN_STAGES["P2"]:
        path=logs/(stage+".log"); regular(path); lines=path.read_text().splitlines()
        R.require(lines and lines[-1]=="STAGE_EXIT=0","training stage not complete: "+stage)
        training.append(R.file_ref(path))
    return {"archive_manifest":manifest,"evaluator_amendment":amendment,"training_logs":training}


def check_reattempt(directory):
    proof=prerequisites(directory)
    R.require(not (p2_path()/"reattempt2.json").exists(),"second re-attempt refused")
    R.require(not any((p2_path()/n).exists() for n in ("eval.json","eval_halt.json","verdict.json","p2-eval.log"))
              and not (W/"experiments/c10w/runs/c10w_oracle/logs/p2-eval.log").exists(),"eval artifacts already exist after archive")
    return proof


def claim_reattempt(directory,gate_file):
    proof=check_reattempt(directory); regular(gate_file); gate=R.load_json(gate_file)
    R.require(gate.get("stage")=="p2-eval" and gate.get("ok") is True and all(
        gate["checks"][k].get("ok") is True for k in ("fingerprint","gpu","dispatch_guards")),"re-attempt gate failed")
    guards=gate["checks"]["dispatch_guards"]
    R.require(guards.get("p2_directory")==str(p2_path()) and guards.get("reattempt")==proof,"re-attempt gate evidence changed")
    path=p2_path()/"reattempt2.json"
    record={"decision_id":DECISION,"stage":"p2-eval","attempt":2,"p2_directory":str(p2_path()),"gate":R.file_ref(gate_file),**proof}
    try:
        with path.open("x",encoding="utf-8") as f: f.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    except FileExistsError as exc: raise R.Halt("HALT: second re-attempt refused") from exc
    return R.file_ref(path)


def verify_claim(directory):
    proof=prerequisites(directory); path=p2_path()/"reattempt2.json"; regular(path); claim=R.load_json(path)
    R.require(claim.get("decision_id")==DECISION and claim.get("stage")=="p2-eval" and claim.get("attempt")==2
              and claim.get("p2_directory")==str(p2_path()) and all(claim.get(k)==v for k,v in proof.items()),"re-attempt claim mismatch")
    R.verify_ref(claim["gate"]); gate=R.load_json(claim["gate"]["path"])
    R.require(gate.get("ok") is True and gate.get("stage")=="p2-eval" and all(
        gate["checks"][k].get("ok") is True for k in ("fingerprint","gpu","dispatch_guards"))
              and gate["checks"]["dispatch_guards"].get("reattempt")==proof,"claimed gate no longer verifies")
    return R.file_ref(path)


def consume_eval_entry(args):
    entry=["P2",str(p2_path()),str(step0_path())]
    R.require(len(args)==4 and args[:3]==entry,"rerun evaluator entry mismatch")
    path=p2_path()/"reattempt2_dispatch.json"; regular(path)
    R.require(R.sha_file(path)==args[3],"dispatcher launch hash mismatch")
    launch=R.load_json(path)
    R.require(launch.get("rerun_decision_id")==DECISION and launch.get("entry")==entry
              and launch.get("claim")==verify_claim(p2_path()) and launch.get("evaluator_amendment")==verify_amendment()
              and type(launch.get("dispatcher_pid")) is int and launch["dispatcher_pid"]==os.getppid(),
              "evaluator must be the admitted dispatcher's child")
    regular(p2_path()/"p2-eval.log")
    R.write_json(p2_path()/"reattempt2_eval_started.json",{
        "rerun_decision_id":DECISION,"claim":launch["claim"],"dispatch":R.file_ref(path),"entry":entry})
    return entry


@contextlib.contextmanager
def overlay():
    """Keep all frozen files intact; add only evaluator A1 and re-attempt provenance at runtime."""
    saved={name:getattr(R,name) for name in ("load_frozen","write_json","read_measurement","latest_directory","disk_phases")}
    import c10w_oracle_step0 as S
    guard=S.guard_phase_projection
    def latest(prefix,base=None):
        path=saved["latest_directory"](prefix,base)
        expected={"step0":step0_path(),"p1":W/P1_REL,"p2":p2_path()}.get(prefix.lower())
        R.require(expected is None or path==expected,"rerun selected unrelated "+prefix)
        return path
    def write(path,record):
        amendment=verify_amendment(record.get("step0_directory"))
        R.require(record.get("evaluator_amendment",amendment)==amendment,"record amendment mismatch")
        record={**record,"evaluator_amendment":amendment}
        return saved["write_json"](path,record)
    def read(phases):
        result=saved["read_measurement"](phases)
        result["evaluator_amendment"]=verify_amendment()
        try:
            refs=[]
            for phase in phases.values():
                if "step0_directory" in phase and phase.get("phase")=="P2":
                    ref=verify_amendment(phase["step0_directory"])
                    R.require(phase.get("evaluator_amendment")==ref,"P2 amendment pointer missing/mismatched")
                    refs.append(ref)
            if refs: result["evaluator_amendment"]=refs[0]
        except R.Halt as exc:
            result.update(status="INVALID",final_label=None,routing=None,reference_count=None,
                          reference_status="NOT-ISSUED",reason=str(exc))
        return result
    def disk(p1):
        R.require(Path(p1).resolve()==W/P1_REL,"rerun reader belongs to another P1")
        assert_selection()
        candidates=sorted(p for p in (W/"experiments/c10w/runs/c10w_oracle").glob("p2_*") if (p/"eval.json").exists())
        R.require(candidates and candidates[-1]==p2_path(),"rerun reader selected unrelated P2 eval")
        phases=saved["disk_phases"](p1)
        R.require(phases["P2"].get("evaluator_amendment")==verify_amendment(),"P2 amendment pointer missing/mismatched")
        return phases
    def budget(directory,phase,proof,completed,pending):
        guard(directory,phase,proof,completed,pending)
        if phase=="P2" and Path(directory).resolve()==p2_path():
            archive_ref=verify_archive(); failed=R.load_json(archive_ref["path"])
            projection=S.training_projection(phase,proof,completed,pending)+failed["halted_eval_wall_seconds"]/60
            auth=R.load_json(Path(proof["p1_directory"])/"authorization_P2.json")
            R.check_phase_minutes("P2",projection,auth["P2"].get("budget_minutes"))
    R.load_frozen=load_frozen; R.write_json=write; R.read_measurement=read
    R.latest_directory=latest; R.disk_phases=disk; S.guard_phase_projection=budget
    try: yield
    finally:
        for name,value in saved.items(): setattr(R,name,value)
        S.guard_phase_projection=guard


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","archive","verify","claim","dispatch","eval","read"))
    parser.add_argument("args",nargs="*"); a=parser.parse_args(argv)
    try:
        if a.action in ("prepare","archive","verify"):
            R.require(not a.args,"unexpected arguments")
            result=prepare() if a.action=="prepare" else archive() if a.action=="archive" else check_reattempt(p2_path())
            print(json.dumps(result,indent=2)); return 0
        if a.action=="claim":
            R.require(len(a.args)==2,"claim needs P2 directory and gate file")
            print(json.dumps(claim_reattempt(*a.args),indent=2)); return 0
        verify_claim(p2_path())
        with overlay():
            if a.action=="dispatch":
                R.require(a.args==[str(p2_path())],"dispatch requires exact P2 directory")
                R.write_json(p2_path()/"reattempt2_dispatch_entered.json",{
                    "rerun_decision_id":DECISION,"dispatcher_pid":os.getpid(),"claim":verify_claim(p2_path())})
                import c10w_oracle_step0 as S
                child=S.run_child
                def eval_child(script,args,directory,stage):
                    entry=list(map(str,args))
                    R.require(script=="c10w_oracle_eval.py" and stage=="p2-eval" and Path(directory).resolve()==p2_path()
                              and entry==["P2",str(p2_path()),str(step0_path())],"rerun dispatch may only evaluate P2")
                    path=p2_path()/"reattempt2_dispatch.json"
                    R.write_json(path,{"rerun_decision_id":DECISION,"dispatcher_pid":os.getpid(),
                                       "entry":entry,"claim":verify_claim(p2_path())})
                    return child("../../tools/c10w_p2_rerun.py",["eval",*entry,R.sha_file(path)],directory,stage)
                S.run_child=eval_child
                try: return S.dispatch_stage("p2-eval")
                finally: S.run_child=child
            if a.action=="eval":
                entry=consume_eval_entry(a.args)
                import c10w_oracle_eval as E
                return E.run_eval(*entry)
            R.require(not a.args,"reader takes no arguments")
            result=R.read_measurement(R.disk_phases(W/P1_REL))
            print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
            return 0 if result["status"]=="VALID" else 2
    except (R.Halt,OSError,KeyError,TypeError,ValueError) as exc:
        print("HALT:",str(exc),file=sys.stderr); return 2


if __name__=="__main__":
    sys.exit(main())
