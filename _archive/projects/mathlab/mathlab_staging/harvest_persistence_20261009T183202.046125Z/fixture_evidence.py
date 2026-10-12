"""Retained, tiny CPU fixtures; no harvest dispatch or real harness import."""
from pathlib import Path
import hashlib, json, os, sys
from unittest.mock import patch
import torch
from mathlab.test_mathlab import harness, BAND
from tools import mathlab_harvest as H, mathlab_runtime as R
from tools.mathlab_events import read_events, fold

audit=Path(os.environ["MATHLAB_FIX_AUDIT"])
root=audit/"fixture_evidence"
root.mkdir()
cases=[("coverage_count4", BAND[:4], 5, R.Halt),
       ("coverage_order", [5,4,6,7,8], 5, R.Halt),
       ("coverage_duplicate", [4,4,6,7,8], 5, R.Halt),
       ("mid_edit", BAND, 2, IndexError)]
evidence=[]
for name,layers,cache_count,error_type in cases:
    case=root/name; case.mkdir()
    harness_obj,hp,requests,P,scope=harness()
    hp.layers=layers
    completed=[]
    run=R.Run(case/"run",1,"CPU persistence fixture (no harvest dispatch): "+name,3600)
    observer=H.EditObserver(harness_obj,completed.append,lambda write:H.persist_failed_write(run.directory,write))
    with patch.dict(harness_obj.get_context_templates.__globals__,CONTEXT_TEMPLATES_CACHE=[["{}"]]), patch.object(H,"W",case):
        try:
            with observer.bound():
                harness_obj.my_edit(hp,requests,P,[torch.zeros(3,3) for _ in range(cache_count)])
        except error_type as error:
            halted=H.stage_harvest_halt(run,error,observer)
        else:
            raise AssertionError("failure fixture returned successfully: "+name)
    assert not completed and not observer.writes and observer.current is None and sys.getprofile() is None
    diagnostic=R.read_json(halted["diagnostic_path"])
    failed=diagnostic["details"]["failed_writes"][0]
    assert failed["diagnostic_only"] and not failed["analysis_eligible"]
    ref=failed["artifacts"][0]
    assert ref["status"]=="saved" and ref["sha256"]==R.sha_file(ref["path"])
    tensors=torch.load(ref["path"],map_location="cpu",weights_only=True)
    assert all(v.device.type=="cpu" for v in tensors.values())
    if name=="coverage_duplicate":
        assert not torch.equal(tensors["c0.l4.rf"],tensors["c1.l4.rf"])
    rows,errors=read_events(run.directory/"events.jsonl")
    assert not errors and rows[-1]["type"]=="run_finished" and rows[-1]["outcome"]=="INVALID"
    evidence.append(dict(case=name,diagnostic_path=halted["diagnostic_path"],diagnostic_sha256=R.sha_file(halted["diagnostic_path"]),
                         finding_path=halted["finding_path"],events_path=str(run.directory/"events.jsonl"),
                         events_sha256=R.sha_file(run.directory/"events.jsonl"),failed_write=failed,
                         tensor_count=len(tensors),fold=fold(rows)))
assert not any(name in sys.modules for name in ("c10e_bandknob","transformers","memit"))
R.write_new(audit/"fixture_evidence.json",dict(cpu_only=True,harvest_dispatched=False,actual_harness_imported=False,cases=evidence))
print(json.dumps(dict(cpu_fixture_cases=len(evidence),actual_harness_imported=False,evidence=str(audit/"fixture_evidence.json"))))
