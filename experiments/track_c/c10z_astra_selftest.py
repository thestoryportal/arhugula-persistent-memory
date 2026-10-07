import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""FROZEN v2.2 specification tests; synthetic CPU tensors only, no harness import."""
import ast
import base64
import copy
import hashlib
import importlib
import importlib.abc
import json
import math
from pathlib import Path
import tempfile
import unittest
import zlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREREG = "38f8b68cc2f82d78e0689bff18bfa44f7600e2fe7b1484b07b4e1e88e267b072"
ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
A1, A2, A7 = ARMS


class NoScienceImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"c10e_bandknob", "transformers", "datasets"}:
            raise AssertionError("model-free selftest attempted science import: " + fullname)


sys.meta_path.insert(0, NoScienceImports())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def set_fit(a, margin=456, positive=24):
    lengths=a["target_lengths"];remaining=margin
    views=[[[1.]*n for n in lengths] for _ in range(6)]
    for v in range(6):
        for i,n in enumerate(lengths):
            for q in range(n):
                if v==0 and i>=positive:views[v][i][q]=0.;continue
                if remaining:views[v][i][q]=5.;remaining-=1
    assert remaining==0
    a["post_fit_observation"]=views
    a["fit"]={"m":margin,"M":6*sum(lengths),"positive_identity_fact_n":positive}


def set_write(a, ratios=(.4,), capacity=1287, band=False):
    import numpy as np
    counts_={l:capacity//(5 if band else 9)+int(l<(4 if band else 0)+capacity%(5 if band else 9))
             for l in (range(4,9) if band else range(9))}
    layers={};pairs=[];realised=[]
    for l,n in counts_.items():
        old=np.zeros((2048,n),dtype="<f2");old[0,:]=10
        new=old.copy()
        for j in range(n):
            r=ratios[len(realised)%len(ratios)];new[0,j]=10*(1+r)
            realised.append(float(new[0,j]-10)/10)
        cols=list(range(n));pairs.extend((l,j) for j in cols)
        layers[str(l)]={"shape":[2048,n],"columns":cols,
            "pristine":base64.b64encode(zlib.compress(old.tobytes())).decode(),
            "final":base64.b64encode(zlib.compress(new.tobytes())).decode()}
    h=hashlib.sha256(json.dumps(pairs,separators=(",", ":")).encode())
    for layer in layers.values():h.update(zlib.decompress(base64.b64decode(layer["final"])))
    a["write"]={**a.get("write",{}),"carriers":{l:v["columns"] for l,v in layers.items()},
        "artifact":{"encoding":"zlib-base64-fp16-le","H_out":h.hexdigest(),"layers":layers},
        "H_out":h.hexdigest(),"relative_changes":realised,"carrier_count":capacity}


def probe_hit(p, kind, value=True):
    p["post_"+kind]=value
    p["post_generated"]=list(p["target"]) if kind=="full" and value else (
        [p["target"][0]]+[999]* (len(p["target"])-1) if value else [999]*len(p["target"]))
    if "post_next" in p:p["post_next"]=p["post_generated"][0]==p["target"][0]
    p["post_full"]=p["post_generated"]==p["target"]


def test_batch(lengths):
    target_ids=[[1000+i*10+q for q in range(n)] for i,n in enumerate(lengths)]
    prompts=[[v+1,i+10] for i in range(24) for v in range(6)]
    pad=max(lengths)+1
    seq=[p+target_ids[i][:-1] for i in range(24) for p in prompts[i*6:i*6+6]]
    return {"target_ids":target_ids,"target_lengths":lengths,"prompt_ids":prompts,"frames":["{}"]*6,"pad_token_id":0,
        "T_pad":pad,"input_ids":[s+[0]*(pad-len(s)) for s in seq],
        "attention_mask":[[1]*len(s)+[0]*(pad-len(s)) for s in seq],
        "requirements":[{"row":i*6+v,"fact":i,"view":v,"q":q,"index":1+q,"target":y}
                        for i,ids in enumerate(target_ids) for v in range(6) for q,y in enumerate(ids)]}


def arm(n=26, canon=24, first=60, margin=None, positive=24, ratio=0.4, seconds=60, lengths=None):
    lengths = lengths or [3] * 16 + [4] * 8
    first=max(first,n)
    batch=test_batch(lengths)
    rows = []
    for i in range(24):
        rows.append({"subj": str(i), "ntok": lengths[i], "canon_full": i < canon,"canon_first":i<canon,
                     "tf_correct":0,"tf_total":3*lengths[i],
                     "para_full_hits": [3*i+j < n for j in range(3)],
                     "para_first_hits": [3*i+j < first for j in range(3)],
                     "para_string_hits": [3*i+j < max(first, n) for j in range(3)]})
    probes = []
    for v in range(6):
        for i, length in enumerate(lengths):
            for depth in range(1, length):
                for s in range(6):
                    probes.append({"view": v, "fact": i, "depth": depth, "subject": s,
                                   "prompt_ids": [v+1,s+50]+batch["target_ids"][i][:depth],
                                   "target":batch["target_ids"][i][depth:],
                                   "pristine_generated":[999]*(length-depth),"post_generated":[999]*(length-depth),
                                   "pristine_next": False, "post_next": False,
                                   "pristine_full": False, "post_full": False})
    sf = [{"fact": i, "depth": d, "prompt_ids": [9]+batch["target_ids"][i][:d],
           "target":batch["target_ids"][i][d:],"pristine_generated":[999]*(length-d),"post_generated":[999]*(length-d),
           "pristine_full": False, "post_full": False}
          for i, length in enumerate(lengths) for d in range(1, length)]
    result={"para_full_n": n, "canon_full_n": canon, "para_first_n": first,
            "para_string_n": max(first, n), "rows": rows,
            "target_lengths": lengths, "fit": {"m": margin, "M": 480,
                "positive_identity_fact_n": positive},
            "locality_described_as": 98.0, "locality_axes": {
                "L1_flipped_to_edited_value": 0, "L3_top1_agree": 30,
                "generic_ppl_post": 10.0},
            "F0": [[False] * 6 for _ in range(6)], "prefix_probes": probes,
            "subject_free_probes": sf,
            "write": {"relative_changes": [ratio, ratio], "rounds_used": 2,
                "stop_reason": "round cap", "round_seconds": [1.0, 1.0],
                "wall_seconds": seconds, "carrier_count": 1287,
                "stage":1,"H_out": "b" * 64}}
    result["F0_raw"]={phase:[{"view":v,"subject":s,"prompt_ids":[v+1,s+50],
        "first_ids":sorted({ids[0] for ids in batch["target_ids"]}),"top1":999,"edited_value":False}
        for v in range(6) for s in range(6)] for phase in ("pristine","post")}
    result["relation_label_probes"]={phase:[{"fact":i,"frame":frame,"prompt_ids":[i+100],
        "first_ids":sorted({ids[0] for ids in batch["target_ids"]}),"top1":999,"edited_value":False}
        for i in range(24) for frame in ("{} is a","{} is associated with")] for phase in ("pristine","post")}
    result["relation_label_probes"].update(top1_changes=0,flips_to_values=0)
    result["locality_axes"]["L3_mean_kl"]=0.;result["locality_axes"]["generic_ppl_pre"]=10.
    result["locality_axes"]["per_edge_vectors"]={axis:[{"prompt":axis+str(i),"pre_id":999,"post_id":999,
        "agree":True,"flipped_to_edited_value":False} for i in range(size)] for axis,size in (("L1",12),("L3",30))}
    result["heldout_position_leads"]={"pre":[1.]*(3*sum(lengths)),"post":[1.]*(3*sum(lengths)),
        "requirements":[{"row":i*3+v,"fact":i,"view":v,"q":q,"index":1+q,"target":y}
            for i,ids in enumerate(batch["target_ids"]) for v in range(3) for q,y in enumerate(ids)]}
    binding_vectors(result)
    set_fit(result,margin if margin is not None else math.ceil(.95*6*sum(lengths)),positive)
    set_write(result,(ratio,),9*min(440,max(16,math.ceil(16*sum(lengths)/9))))
    return result


def fixture(n=26, a=12, stage=1, **kwargs):
    lengths=kwargs.get("lengths")
    base = arm(a, canon=8, first=50,lengths=lengths)
    candidate = arm(n, **kwargs)
    baseline_a1 = arm(68)
    baseline_a2 = arm(68)
    recipes = {"A": {"law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0},
                     "arms": {A1: baseline_a1, A2: baseline_a2, A7: base}},
               "Z": {"law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0},
                     "audit": {"astra_calls": 1, "original_calls": 0, "Z_OVERRIDE_HITS": 0},
                     "arms": {A7: candidate}}}
    if stage >= 2:
        recipes["Z"]["arms"].update({A1: arm(68), A2: arm(68)})
        recipes["Z"]["audit"]["astra_calls"] = 3
        recipes["Z-band"] = {"law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0},
            "audit": {"astra_calls": 1, "original_calls": 0, "Z_OVERRIDE_HITS": 0},
            "arms": {A7: arm(23,lengths=lengths)}}
        for k,v in recipes["Z"]["arms"].items():v["write"]["stage"]=1 if k==A7 else 2
        band=recipes["Z-band"]["arms"][A7];band["write"]["stage"]=2
        set_write(band,capacity=min(candidate["write"]["carrier_count"],2200),band=True)
    parts = {k: "a"*64 for k in ("context_templates_sha256", "dstats_sha256", "G_sha256",
             "driver_sha256", "reader_sha256", "H_pristine")}
    parts.update(prereg_sha256=PREREG, model_revision="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b",
                 safetensors={"model-00001-of-00002.safetensors":"a"*64},
                 requests={k:[{"prompt":"{}","subject":str(i),"target_new":{"str":str(i)}} for i in range(24)] for k in ARMS},
                 settings=copy.deepcopy(importlib.import_module("c10z_astra_arms").SETTINGS), seed=0,
                 engine_sources={"memit_dry_run/memit/memit/memit_main.py":"d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65",
                    "experiments/track_c/c10e_bandknob.py":"a"*64}, hparams={"x": "a"*64},
                 screens={"x": "a"*64}, covariances={str(i):{"path":"/synthetic/cov"+str(i),"sha256":"a"*64} for i in range(4,13)},
                 tokenizer={"tokenizer.json":"a"*64,"tokenizer_config.json":"a"*64},
                 batches={k:test_batch(recipes["A"]["arms"][k]["target_lengths"]) for k in ARMS},
                 forward_settings={"use_cache": False, "logits_to_keep": 0, "padding_side": "right"},
                 environment={"device": "mps", "dtype": "float16", "torch": "test", "transformers": "4.51.0"},
                 solver_backend={"dtype": "float64", "device": "cpu"},
                 dataset={"revision":"a"*40,"row_ids":[str(i) for i in range(1000)],
                    "text_sha256":["a"*64]*1000,"ordered_token_ids":[[1]]*1000,"nonpadding_tokens":1000})
    hashes = {k: "a"*64 for k in ("context_templates.json", "dstats.pt", "G.pt",
              "pristine_hash.json", "manifest.json", "overlap_audit.json")}
    checks = {"Z"+str(i): {"ok": True} for i in range(8)}
    pristine=[[6.]*length if i<8 else [-1.]*length for i,length in enumerate(base["target_lengths"])]
    checks["Z0"].update(sigma_shape=0., tau_shape=.02,identity_batch_leads=pristine,prefix_shape_leads=copy.deepcopy(pristine))
    checks["Z1"].update(native_reconstruction_error=0.)
    checks["Z2"].update(checked=24, ambiguous=0)
    checks["pristine_canon_full"]=[i<8 for i in range(24)]
    z3={"rounds":2,"failing_count":32,"carrier_count":1287,"columns_written":[1287]*2,
        "weights_equal":True,"lambda_by_round":[[0.]*32]*2,"max_logit_delta":0.,
        "pristine_generations":[[999]]*96,"post_generations":[[999]]*96,
        "pristine_logits_sha256":["a"*64]*96,"post_logits_sha256":["a"*64]*96}
    checks["Z3"]["modes"]={m:copy.deepcopy(z3) for m in ("astra","band")}
    checks["Z4"].update(identity_errors=[0.]*32,identity_bounds=[1e-8]*32,loop_rows=list(range(32)),loop_relative_error=0.)
    checks["Z5"]["writes"]=[{"selected_pairs":[[35,0]],"changed_pairs":[[35,0]],
        "other_parameters_equal":True,"solve_device":"cpu","solve_dtype":"float64"}]
    checks["Z7"].update(nonzero_controls=1, sigma_head=0., tau_head=.02,
        same_forward_key_equality=True,requirement_map_audited=True,
        controls=[{"nonzero_realised":True,"columns_written":16,"post_error":0.,
                   "coefficient_error":0.,"coefficient_bound":1e-8,"columns_error":0.,"columns_bound":1e-8}])
    checks.update(V7={"spearman": {str(i): .9 for i in range(4,13)}},
                  V8={"cholesky": True, "condition": 10.0})
    r = {"schema": "c10z_astra-v2.2", "process": 1, "pid": 100,
         "stage_completed": stage, "manifest": {"parts": parts, "H_in": digest(parts)},
         "H_in": digest(parts), "H_pristine": "a"*64, "artifact_hashes": hashes,
         "fingerprint": {"sha256": "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65",
              "cov_cpu_sites": 3, "start":parts["engine_sources"],"end":parts["engine_sources"]},
         "restores": [{"where": "fixture", "ok": True, "layers": 36, "hooks_ok": True}],
         "memory": [{"rss_bytes": 1, "driver_bytes": 1, "float64_on_mps": False}],
         "checks": checks, "recipes": recipes,
         "omissions": {"G0": {"status": "NOT-RUN", "reason": "K1"},
             "Z-band": {"status": "NOT-RUN", "reason": "K1"},
             "process2": {"status": "NOT-RUN", "reason": "K2"}},
         "certificate": {"artifact_identity": "NOT-EVALUATED",
                         "numeric_behavioral_reproduction": "NOT-EVALUATED"},
         "budget": {"halted":False,"origins":{"stage01":0.,**({"stage2":1000.} if stage==2 else {})},
             "ceilings":{"stage01":5400,"stage2":12000. if stage==2 else None,"stage3":24000. if stage==2 else None},
             "history":[{"components_s":{"remaining":1.},"scopes":{"stage01":{"elapsed_s":1.,"remaining_s":1.,"ceiling_s":5400.}}}]},
         "outcome": "COMPLETE"}
    for k in ("context_templates.json","dstats.pt","G.pt"):
        hashes[k]=parts[{"context_templates.json":"context_templates_sha256","dstats.pt":"dstats_sha256","G.pt":"G_sha256"}[k]]
    r["attempt_id"]="fixture-attempt"
    r["omissions"]={"G0":{"status":"NOT-RUN","reason":"K1"},"Z-band":{"status":"NOT-RUN","reason":"K1"}} if stage==1 else {}
    z=candidate
    clean=n>=19 and n-a>=10 and margin_fit(z) and z["write"]["relative_changes"][0]<=.55 and z["write"]["wall_seconds"]<=3600
    if stage==1 and clean:
        for o in r["omissions"].values():o["reason"]="AWAITING-STAGE2"
    seal_fixture(r)
    seal_schedule(r)
    return r


def seal_fixture(r):
    where=["import","LAW#3 passed","Z3 astra","Z3 band"]
    post1=[];post2=[]
    for recipe,rs in r["recipes"].items():
        where.extend(("before recipe "+recipe,"after recipe "+recipe))
        for name,a in rs["arms"].items():
            if recipe=="A":continue
            where.extend(("before write "+name,"restore_hook "+name))
            view=a["post_fit_observation"][0];checked=[i for i,row in enumerate(view) if not any(abs(v)<=.02 for v in row)]
            post1.append({"recipe":recipe,"arm":name,"Z1_error":0.,"Z5_ok":True})
            post2.append({"recipe":recipe,"arm":name,"checked":len(checked),"ambiguous":24-len(checked),
                "ok":bool(checked) and all(all(v>0 for v in view[i])==a["rows"][i]["canon_full"] for i in checked)})
    r["restores"]=[{"where":w,"ok":True,"layers":36,"hooks_ok":True} for w in where]
    r["checks"]["post_write_checks"]=post1;r["checks"]["post_write_Z2"]=post2


def margin_fit(a):
    f=a["fit"];return 20*f["m"]>=19*f["M"] and f["positive_identity_fact_n"]>=23 and a["canon_full_n"]>=23


def second_process(r):
    r.update(process=2,pid=101)
    r["budget"]["origins"]["stage3"]=r["budget"]["origins"]["stage01"]
    r["budget"]["ceilings"].update(stage2=12000.,stage3=24000.)
    seal_schedule(r)


def seal_schedule(r):
    # Only fixture metadata; label expectations come from the frozen table and independent predicates.
    R=importlib.import_module("c10z_astra_read")
    z=r["recipes"]["Z"]["arms"][A7];a=r["recipes"]["A"]["arms"][A7]
    gates=R.side_gates(z,a);stage=r["stage_completed"]
    if stage==2:gates["G0"]=all(r["recipes"]["Z"]["arms"][k]["para_full_n"]>=68 for k in (A1,A2))
    seconds=[v["write"]["wall_seconds"] for name in ("Z","Z-band") for v in r["recipes"].get(name,{"arms":{}})["arms"].values()]
    reading=R.classify_candidate(z,a,gates,stage,r["recipes"]["Z-band"]["arms"][A7] if stage==2 else None,seconds)
    r["omissions"]=R.stage_omissions(r["process"],stage,reading["next_stage"],r["budget"]["ceilings"])


def counts(a, n=None, canon=None):
    if n is not None:
        a["para_full_n"] = n
        for i, row in enumerate(a["rows"]):
            row["para_full_hits"] = [3*i+j < n for j in range(3)]
        a["para_string_n"] = max(a["para_string_n"], n)
        for i,row in enumerate(a["rows"]):row["para_string_hits"]=[3*i+j<a["para_string_n"] for j in range(3)]
        if n>a["para_first_n"]:
            a["para_first_n"]=n
            for i,row in enumerate(a["rows"]):row["para_first_hits"]=[3*i+j<n for j in range(3)]
    if canon is not None:
        a["canon_full_n"] = canon
        for i, row in enumerate(a["rows"]):
            row["canon_full"] = i < canon
    binding_vectors(a)


def binding_vectors(a):
    a["per_template_n"]=[sum(r["para_full_hits"][j] for r in a["rows"]) for j in range(3)]
    a["per_fact_n"]=[sum(r["para_full_hits"]) for r in a["rows"]]
    a["per_edge_behavior_pass"]=[all(r["para_full_hits"]) for r in a["rows"]]
    a["tf_pertok_cont"]=0.
    numerator=sum(x and y for r in a["rows"] for x,y in zip(r["para_full_hits"],r["para_first_hits"]))
    a["cond_full_given_first"]=round(numerator/a["para_first_n"],3) if a["para_first_n"] else None


class SpecTests(unittest.TestCase):
    def modules(self):
        for suffix in ("arms", "read"):
            self.assertTrue((HERE / ("c10z_astra_" + suffix + ".py")).is_file(),
                            "ASTRA implementation absent: c10z_astra_" + suffix + ".py")
        return importlib.import_module("c10z_astra_arms"), importlib.import_module("c10z_astra_read")

    def reading(self, r, expected, attribution=None):
        _, reader = self.modules()
        if not expected.startswith("HALTED"):seal_schedule(r)
        got = reader.read_process(r)
        self.assertEqual(got["label"], expected, got)
        if attribution is not None:
            self.assertEqual(got["attribution"], attribution, got)
        return got

    def test_00_implementation_exists(self):
        """Prereg :204: actual driver, reader and stage wrapper exist."""
        self.modules()
        self.assertTrue((ROOT / "tools/run_c10z_stage.sh").is_file())

    def test_raw_evidence_over_asserted_fit_write_and_repro(self):
        """Prereg :224, :230, :272, :278: reject forged counts, bytes and certificates."""
        D,R=self.modules()
        for mutate in (lambda a:a["fit"].update(m=480),
                       lambda a:a["write"].update(relative_changes=[.01]),
                       lambda a:a["write"].update(H_out="f"*64),
                       lambda a:a["prefix_probes"][0].update(post_full=True)):
            r=fixture();mutate(r["recipes"]["Z"]["arms"][A7])
            self.assertFalse(R.read_process(r)["scientific_verdict"])
        p1=fixture(stage=2);p2=copy.deepcopy(p1);second_process(p2)
        repro=D.reproduction(p1,p2)
        counts(p2["recipes"]["Z"]["arms"][A7],30)
        self.assertEqual(R.read_run(p1,p2,repro)["label"],"HALTED-V12")

    def test_terminal_halt_overrides_earlier_complete_pass(self):
        """Prereg :196, :225: stage2 hard halt invalidates earlier stage1 pass."""
        D,R=self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);D.write_json(out/"pass_p1.json",fixture())
            D.write_json(out/"run.json",{"attempt_id":"fixture-attempt","halt":{
                "code":"HALTED-BUDGET","detail":"stage2 deadline"}})
            self.assertEqual(R.read_directory(out)["label"],"HALTED-BUDGET")

    def test_fixed_competitor_and_native_reference_contract(self):
        """Prereg :155: native gathered logits, fixed competitor, finite last-layer path."""
        D,R=self.modules()
        import torch
        obs={"native_gathered":torch.tensor([[9.,10.,3.]],device="cpu"),
             "targets":torch.tensor([0],device="cpu")}
        self.assertEqual(D.fixed_leads(obs,torch.tensor([2],device="cpu")).tolist(),[6.])
        K=torch.tensor([[[1.,2.]]],dtype=torch.float16,device="cpu")
        W=torch.tensor([[.5,.25],[1.,-.5]],dtype=torch.float16,device="cpu")
        residual=torch.tensor([[[2.,3.]]],dtype=torch.float16,device="cpu")
        norm=lambda x:x.float()/(x.float().pow(2).mean(-1,keepdim=True)+1e-6).sqrt()
        result=D.last_layer_logits(K,W,residual,norm,lambda x:x)
        expected=norm(torch.tensor([[[3.,3.]]],dtype=torch.float16,device="cpu"))
        self.assertTrue(torch.equal(result,expected))

    def test_completed_stage2_keeps_stage1_round_ceiling(self):
        """Prereg :198, :225: completed stage2 still checks stage1 A7 timing."""
        _,R=self.modules();r=fixture(stage=2)
        r["recipes"]["Z"]["arms"][A7]["write"]["round_seconds"][0]=120.001
        self.assertEqual(R.read_process(r)["label"],"HALTED-BUDGET")

    def test_transport_wait_publication_and_worker_failure(self):
        """Prereg :126–139, :196: resident continuity, completed response, bounded failed wait."""
        D,R=self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);clock=[10.]
            run={"attempt_id":"fixture-attempt","pid":123,"completed":0,"requested":1,
                 "closed":False,"halt":None,"reading":None}
            D.write_json(out/"run.json",run)
            D.write_json(out/"logs/heartbeat.json",{"attempt_id":"fixture-attempt","pid":123,"at":10.})
            def respond(_):
                clock[0]+=.1;run.update(completed=1,requested=None,reading={"label":"PARTIAL","next_stage":2})
                D.write_json(out/"run.json",run,replace=True)
            self.assertEqual(D.wait_stage(out,1,clock=lambda:clock[0],pause=respond),0)
            run.update(completed=0,requested=1);D.write_json(out/"run.json",run,replace=True)
            clock[0]=26.
            with self.assertRaisesRegex(R.Halt,"HALTED-V12"):
                D.wait_stage(out,1,clock=lambda:clock[0],pause=lambda _:None)

    def test_manifest_population_and_post_instrument_tampering(self):
        """Prereg :137, :147–155, :224: complete inputs, missing controls, post-write evidence."""
        _,R=self.modules()
        for mutate in (lambda r:r["manifest"]["parts"]["dataset"]["row_ids"].pop(),
                       lambda r:r["manifest"]["parts"]["batches"][A7]["requirements"][0].update(index=0),
                       lambda r:r["checks"]["Z3"]["modes"]["band"]["post_generations"][0].append(42),
                       lambda r:r["checks"]["post_write_checks"][0].update(Z1_error=.3),
                       lambda r:r["checks"].pop("post_write_Z2")):
            r=fixture();mutate(r)
            r["H_in"]=r["manifest"]["H_in"]=digest(r["manifest"]["parts"])
            self.assertFalse(R.read_process(r)["scientific_verdict"])

    def test_known_answer_scalar_and_native_fp16_reference(self):
        """Prereg :155: independent scalar A/ridge/columns and native finite reference."""
        D,R=self.modules()
        import numpy as np
        import torch
        c=np.array([1.,-.5]);G=np.array([[2.,.3],[.3,1.]])
        direction=np.linalg.solve(G,c);direction/=c@direction
        k=np.array([.7,-1.,.2]);null=np.array([.3,2.,.8]);scale=1.2
        scalar=(c@direction)*sum(null[j]*k[j]*k[j] for j in range(3))/scale
        coeff=1/(scalar*1.001)
        expected=np.column_stack([null[j]*coeff*k[j]*direction for j in range(3)])
        t=lambda v:torch.tensor(np.asarray(v),dtype=torch.float64,device="cpu")
        got=D.joint_solve(t([c]),D.preferred_directions(t(G),t([c])),t([scale]),{35:t([k])},{35:t(null)},t([1.]))
        np.testing.assert_allclose(got["patch"][35].numpy(),expected,rtol=1e-12,atol=1e-12)
        W=torch.tensor([[.5,.2,-.1],[.1,-.3,.8]],dtype=torch.float16,device="cpu")
        ref=(W.numpy().astype(np.float32)+expected.astype(np.float32)).astype(np.float16)
        D.write_columns(W,[0,1,2],got["patch"][35]);np.testing.assert_array_equal(W.numpy(),ref)

    def test_worked22_validity_precedes_conditional_label(self):
        """Prereg :149, :208, :311: contradictory raw canonical evidence HALTs before labels."""
        _,R=self.modules();r=fixture(n=22);z=r["recipes"]["Z"]["arms"][A7]
        set_fit(z,460);counts(z,canon=0);seal_fixture(r)
        self.assertEqual(R.read_process(r)["label"],"HALTED-V5")

    def test_ttl_every_Z_arm_and_incomplete_actual_repro_failure(self):
        """Prereg :267, :274, :278: any Z TTL, and omitted plus failed R1 retain both flags."""
        D,R=self.modules()
        for seconds in (3600.,3600.001):
            r=fixture(stage=2);r["recipes"]["Z"]["arms"][A1]["write"]["wall_seconds"]=seconds
            seal_schedule(r);got=R.read_process(r)
            self.assertEqual("EXCEEDS-TTL" in got["qualifiers"],seconds>3600)
            self.assertEqual(got["next_stage"],3 if seconds==3600 else None)
        p1=fixture(n=22,stage=2);p2=fixture(n=21);second_process(p2)
        set_write(p2["recipes"]["Z"]["arms"][A7],(.41,))
        repro=D.reproduction(p1,p2);got=R.read_run(p1,p2,repro)
        self.assertIn("REPRO-INCOMPLETE",got["qualifiers"])
        self.assertIn("NOT-REPRODUCIBLE",got["qualifiers"])

    def test_terminal_K1_wrapper_waits_for_close_error(self):
        """Prereg :129, :265: terminal K1 response waits for verified close, propagates error."""
        D,R=self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            run={"attempt_id":"fixture-attempt","pid":123,"completed":1,"requested":None,
                 "closed":False,"halt":None,"reading":{"label":"NULL-STAGE1","next_stage":None}}
            D.write_json(out/"run.json",run)
            D.write_json(out/"logs/heartbeat.json",{"attempt_id":"fixture-attempt","pid":123,"at":10.})
            def fail_close(_):
                run.update(closed=True,halt={"code":"HALTED-V3","detail":"final restore"})
                D.write_json(out/"run.json",run,replace=True)
            with self.assertRaisesRegex(R.Halt,"HALTED-V3"):
                D.wait_stage(out,1,clock=lambda:10.,pause=fail_close)

    def test_omission_reasons_follow_K1_K2(self):
        """Prereg :265–267: every unrun expansion is recorded with its actual stopping reason."""
        _,R=self.modules();r=fixture(n=18)
        r["omissions"]["G0"]["reason"]="AWAITING-STAGE2"
        self.assertEqual(R.read_process(r)["label"],"HALTED-V12")
        r=fixture(n=18);r["omissions"].pop("process2",None)
        self.assertEqual(R.read_process(r)["label"],"HALTED-V12")

    def test_law3_both_sides(self):
        """Prereg :123, :217: all inclusive envelope edges, and A1/A2 67/68."""
        for field, values in {"para_full_n": (4,5,18,19), "canon_full_n": (4,5,10,11),
                              "para_first_n": (41,42,59,60)}.items():
            lo, hi = {"para_full_n": (5,18), "canon_full_n": (5,10), "para_first_n": (42,59)}[field]
            for value in values:
                r = fixture(n=18)
                base = r["recipes"]["A"]["arms"][A7]
                if field=="para_full_n":counts(base,n=value)
                elif field=="canon_full_n":counts(base,canon=value)
                else:
                    base[field]=value
                    for i,row in enumerate(base["rows"]):row["para_first_hits"]=[3*i+j<value for j in range(3)]
                    binding_vectors(base)
                with self.subTest(field=field, value=value):
                    self.reading(r, "NULL-STAGE1" if lo <= value <= hi else "HALTED-V4")
        for name in (A1,A2):
            for value in (67,68):
                r=fixture(n=18); r["recipes"]["A"]["arms"][name]["para_full_n"]=value
                self.reading(r, "NULL-STAGE1" if value==68 else "HALTED-V4")

    def test_fit_count_boundaries(self):
        """Prereg :210, :230–234: exact integer FIT, positive 22/23, canonical 22/23."""
        _, R=self.modules()
        for m in (9499,9500):
            self.assertEqual(R.fit({"m":m,"M":10000,"positive_identity_fact_n":23},23),m==9500)
        for key in ("positive_identity_fact_n","canon_full_n"):
            for n in (22,23):
                fit={"m":95,"M":100,"positive_identity_fact_n":23}
                if key=="positive_identity_fact_n": fit[key]=n
                self.assertEqual(R.fit(fit,n if key=="canon_full_n" else 23),n==23)
        self.assertEqual(R.fit_counts([[0,5],[.0001,5]], [[5]*20]),
                         {"m":20,"M":20,"positive_identity_fact_n":1})

    def test_table_T_exhaustive_and_integer_boundaries(self):
        """Prereg :249–261: independent exhaustive T1–T5, n18/19/29/30 and g9/10."""
        _,R=self.modules()
        for a in range(5,19):
            for n in range(73):
                for side in (False,True):
                    expected = ("NULL" if n<=18 or n-a<=9 else
                                "TRADEOFF" if not side else "PARTIAL" if n<30 else "LEAD")
                    self.assertEqual(R.base_label(n,a,side),expected)
        for n,a,expected in ((18,5,"NULL"),(19,9,"PARTIAL"),(19,10,"NULL"),
                             (29,18,"PARTIAL"),(30,18,"LEAD")):
            self.assertEqual(R.base_label(n,a,True),expected)

    def test_side_gate_boundaries_and_populations(self):
        """Prereg :239–245: every side gate equality passes, next value fails; no pooling."""
        for gate, equality, miss in (("G1",1,2),("G2",1,2),("G3",95.,94.999),
                                     ("G4",29,28),("G5",10.5,10.5001)):
            for value in (equality,miss):
                r=fixture();z=r["recipes"]["Z"]["arms"][A7]
                if gate=="G1":
                    z["locality_axes"]["L1_flipped_to_edited_value"]=value
                    for p in z["locality_axes"]["per_edge_vectors"]["L1"][:value]:p.update(post_id=1000,agree=False,flipped_to_edited_value=True)
                if gate=="G2":
                    z["F0"][5]=[i<value for i in range(6)]
                    for p in z["F0_raw"]["post"]:
                        if p["view"]==5 and p["subject"]<value:p.update(top1=p["first_ids"][0],edited_value=True)
                if gate=="G3": z["locality_described_as"]=value
                if gate=="G4":
                    z["locality_axes"]["L3_top1_agree"]=value
                    for p in z["locality_axes"]["per_edge_vectors"]["L3"][value:]:p.update(post_id=998,agree=False)
                if gate=="G5": z["locality_axes"]["generic_ppl_post"]=value
                seal_schedule(r);got=self.modules()[1].read_process(r)
                self.assertEqual(got["base_label"],"PARTIAL" if value==equality else "TRADEOFF")
        for hit in ("next","full"):
            for h in (1,2):
                r=fixture();z=r["recipes"]["Z"]["arms"][A7]
                for p in z["prefix_probes"]:
                    if p["view"]==5 and p["fact"]==23 and p["depth"]==3 and p["subject"]<h:
                        probe_hit(p,hit)
                seal_schedule(r);got=self.modules()[1].read_process(r)
                self.assertEqual(got["base_label"],"PARTIAL" if h==1 else "TRADEOFF")
        for name in (A1,A2):
            for h in (67,68):
                r=fixture(stage=2);counts(r["recipes"]["Z"]["arms"][name],h)
                self.reading(r,"PARTIAL-SINGLE-PROCESS" if h==68 else "TRADEOFF-SINGLE-PROCESS")
        for key in ("F0","prefix_probes"):
            r=fixture();r["recipes"]["Z"]["arms"][A7][key].pop()
            self.reading(r,"HALTED-V12")

    def test_band_boundaries_ordered(self):
        """Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows."""
        for n,a,nb,status in ((26,12,18,"BAND-NO-QUALIFIED-GAIN"),
            (26,9,19,"BAND-PARTIAL-RETENTION"),(26,10,19,"BAND-NO-QUALIFIED-GAIN"),
            (26,12,21,"BAND-NO-QUALIFIED-GAIN"),(26,12,22,"BAND-RETAINS-QUALIFIED-GAIN"),
            (40,12,34,"BAND-PARTIAL-RETENTION"),(40,12,35,"BAND-RETAINS-QUALIFIED-GAIN")):
            r=fixture(n=n,a=a,stage=2);counts(r["recipes"]["Z-band"]["arms"][A7],nb)
            got=self.modules()[1].read_process(r);self.assertEqual(got["attribution"],status)
        for total in (2200,2201):
            r=fixture(stage=2);z=r["recipes"]["Z"]["arms"][A7];z["write"]["carrier_count"]=total
            got=self.modules()[1].attribution(z,r["recipes"]["Z-band"]["arms"][A7],r["recipes"]["A"]["arms"][A7])
            self.assertEqual(got,"ATTRIBUTION-UNMATCHED-CAPACITY" if total>2200
                             else "BAND-RETAINS-QUALIFIED-GAIN")
        D,_=self.modules()
        self.assertEqual(D.band_counts(2200),{i:440 for i in range(4,9)})
        self.assertEqual(D.band_counts(2201),{i:440 for i in range(4,9)})
        self.assertEqual(D.band_counts(1287),{4:258,5:258,6:257,7:257,8:257})

    def test_w1_even_median_w2_subject_free(self):
        """Prereg :210, :272–274: even median, exact W1/W2, depth OR and +1 boundary."""
        D,R=self.modules()
        self.assertEqual(R.median([.5,.6]),.55)
        for ratios,qual in (([.5,.6],False),([.5,.601],True)):
            r=fixture(lengths=[3]*24);set_write(r["recipes"]["Z"]["arms"][A7],ratios,capacity=1152)
            seal_schedule(r);self.assertEqual("LARGE-WRITE" in R.read_process(r)["qualifiers"],qual)
        for seconds in (3600,3600.001):
            r=fixture(seconds=seconds)
            self.assertEqual("EXCEEDS-TTL" in R.read_process(r)["qualifiers"],seconds>3600)
        for facts in (1,2):
            r=fixture()
            for p in r["recipes"]["Z"]["arms"][A7]["subject_free_probes"]:
                probe_hit(p,"full",p["fact"]<facts)
            seal_schedule(r);self.assertEqual("SUBJECT-FREE" in R.read_process(r)["qualifiers"],facts>1)
        self.assertEqual(D.zero_column_ratio(0.,0.),0.)
        self.assertEqual(D.zero_column_ratio(0.,1.),"POSITIVE-INFINITY")
        self.assertEqual(R.median([0.,"POSITIVE-INFINITY"]),"POSITIVE-INFINITY")

    def test_z2_ambiguous_and_all_validity_gates(self):
        """Prereg :149, :212–225: zero checked Z2 HALTs; V1–V13 each enforced."""
        D,R=self.modules()
        self.assertFalse(D.z2_agreement([[.01]], [True], .02)["ok"])
        mutations = {
            "HALTED-V1":lambda r:r["fingerprint"].update(cov_cpu_sites=2),
            "HALTED-V2":lambda r:r["recipes"]["Z"]["law5_gate"].update(ok=False),
            "HALTED-V3":lambda r:r["restores"][0].update(ok=False),
            "HALTED-V5":lambda r:r["checks"]["Z2"].update(checked=0,ambiguous=24),
            "HALTED-V6":lambda r:r["checks"].update(capture=math.nan),
            "HALTED-V7":lambda r:r["checks"]["V7"]["spearman"].update({"12":.7999}),
            "HALTED-V8":lambda r:r["checks"]["V8"].update(cholesky=False),
            "HALTED-V9":lambda r:r["recipes"]["Z"]["audit"].update(original_calls=1),
            "HALTED-V10":lambda r:r["recipes"]["Z"]["arms"][A7].update(para_string_n=0),
            "HALTED-V11":lambda r:r["memory"][0].update(driver_bytes=32*2**30+1),
            "HALTED-V12":lambda r:r.pop("H_in"),
            "HALTED-BUDGET":lambda r:r["budget"].update(halted=True)}
        for expected,mutate in mutations.items():
            with self.subTest(gate=expected):
                r=fixture();mutate(r);self.reading(r,expected)
        r=fixture();r["checks"]["V7"]["spearman"]["12"]=.8
        self.assertEqual(R.read_process(r)["base_label"],"PARTIAL")
        for value in (True,26.,-1,73):
            r=fixture();r["recipes"]["Z"]["arms"][A7]["para_full_n"]=value
            self.reading(r,"HALTED-V12")

    def test_k1_k2_omissions_and_replication(self):
        """Prereg :265–280: valid early stops != V12, lower labels, R2/R3 boundaries."""
        D,R=self.modules()
        r1=fixture(n=30,stage=2);r2=fixture(n=29,stage=2);second_process(r2)
        repro=D.reproduction(r1,r2)
        got=R.read_run(r1,r2,repro)
        self.assertEqual(got["label"],"PARTIAL");self.assertFalse(got["lead_replicated"])
        self.assertEqual(got["artifact_identity"],"EXACT")
        r1=fixture(n=22,stage=2);r2=fixture(n=21);second_process(r2)
        repro=D.reproduction(r1,r2)
        got=R.read_run(r1,r2,repro)
        self.assertIn("REPRO-INCOMPLETE",got["qualifiers"])
        self.assertNotIn("NOT-REPRODUCIBLE",got["qualifiers"])
        r2["checks"]["Z4"]["ok"]=False
        self.assertEqual(R.read_run(r1,r2,repro)["label"],"HALTED-V5")
        for key,bounds in (("R2",(2,3)),("R3",(3,4))):
            for v in bounds:
                repro={"R1":{"status":"PASS"},"R2":{"difference":2},"R3":{"disagree":3},
                       "artifact_identity":"EXACT","numeric_behavioral_reproduction":"PASS"}
                repro[key]["difference" if key=="R2" else "disagree"]=v
                out=R.aggregate({"base_label":"PARTIAL","qualifiers":[]},
                                {"base_label":"PARTIAL","qualifiers":[]},repro)
                self.assertEqual("NOT-REPRODUCIBLE" in out["qualifiers"],v==bounds[1])
        self.assertEqual(D.relative_layer_error([0.,0.],[0.,0.]),0.)
        self.assertEqual(D.relative_layer_error([0.,0.],[0.,1.]),"ONE-ZERO")
        for e in (.001,.0010001): self.assertEqual(R.r1_error_pass(e),e<=.001)

    def test_budget_origins_prestart_deadlines_round_memory(self):
        """Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory."""
        D,R=self.modules();clock=[100.]
        b=D.Budget(100.,60.,6000.,process=1,clock=lambda:clock[0])
        self.assertEqual(b.deadline(),5500.)
        clock[0]=5499.;b.project({"remaining":1.})
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"): b.project({"remaining":1.001})
        clock[0]=5501.
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):b.check()
        for stage in (2,3):
            absent=D.Budget(0.,None,None,clock=lambda:0.)
            with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):absent.enter(stage)
        b=D.Budget(100.,60.,6000.,process=2,clock=lambda:clock[0]);clock[0]=200.
        self.assertEqual(b.origins["stage3"],100.)
        b.complete01();b.enter(2)
        self.assertEqual(b.origins["stage2"],200.)
        self.assertEqual(b.deadline(),260.)
        b=D.Budget(100.,10000.,200.,process=2,clock=lambda:200.)
        b.complete01();b.enter(2);self.assertEqual(b.deadline(),300.)
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):b.project({"unknown":0.})
        D.round_guard(120.)
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):D.round_guard(120.0001)
        D.memory_guard(8*2**30,32*2**30,False)
        for args in ((8*2**30+1,32*2**30,False),(0,32*2**30+1,False),(0,0,True)):
            with self.assertRaisesRegex(R.Halt,"HALTED-V11"):D.memory_guard(*args)

    def test_ordering_and_stage_transport(self):
        """Prereg :120–125, :127–133, :218: no early observation, ordered one-stage requests."""
        D,R=self.modules();gate=D.Gates();seen=[]
        for action in (lambda:gate.observe(lambda:seen.append("observe")),
                       lambda:gate.candidate(lambda:seen.append("candidate"))):
            with self.assertRaises(R.Halt):action()
        self.assertEqual(seen,[])
        gate.baseline(fixture()["recipes"]["A"])
        gate.observe(lambda:seen.append("observe"))
        with self.assertRaisesRegex(R.Halt,"HALTED-V5"):gate.candidate(lambda:seen.append("candidate"))
        gate.instruments(fixture()["checks"]);gate.candidate(lambda:seen.append("candidate"))
        self.assertEqual(seen,["observe","candidate"])
        events=[];s=D.StageState("attempt",1)
        s.run(0,"attempt",lambda:events.append(0))
        for stage,attempt in ((0,"attempt"),(2,"attempt"),(1,"other")):
            with self.assertRaisesRegex(R.Halt,"HALTED-V12"):s.run(stage,attempt,lambda:events.append(stage))
        s.run(1,"attempt",lambda:events.append(1));s.run(2,"attempt",lambda:events.append(2))
        self.assertEqual(events,[0,1,2]);self.assertTrue(s.closed)
        D.entry_preflight({})
        for key in ("C10_PROJECTOR","N_EDIT","C10_SUBJECT_OFFSET","C10_CTX_TEMPLATES",
                    "C10_ARMS","C10_KEY_LOCUS","C10_RECIPES"):
            with self.assertRaisesRegex(R.Halt,"HALTED-V12"):D.entry_preflight({key:""})

    def test_cpu_joint_algebra_independent_reference(self):
        """Prereg :76, :78–80, :151: nonsymmetric solve, scalar-loop independent assembly."""
        D,R=self.modules()
        import numpy as np
        import torch
        C=np.array([[1.,2.,-.5],[.2,-.4,1.],[2.,.5,.3]])
        W=np.array([[1.,.3,-.1],[.2,1.5,.1],[.3,-.2,1.],[-.4,.2,.5]])
        gain=np.array([1.,.8,1.2]);G=(W*gain).T@(W*gain)
        dirs=[]
        for c in C:
            v=np.linalg.solve(G,c);dirs.append(v/np.dot(c,v))
        dirs=np.array(dirs)
        K={1:np.array([[.5,1.],[2.,-.5],[-1.,.2]]),2:np.array([[1.,.4],[.3,.2],[1.,2.]])}
        Dweights={1:np.array([2.,.1]),2:np.array([.3,1.5])};sc=np.array([1.,2.,.7]);gamma=np.array([.3,1.,2.])
        A=np.zeros((3,3))
        for t in range(3):
            for u in range(3):
                acc=sum(Dweights[l][j]*K[l][t,j]*K[l][u,j] for l in K for j in range(2))
                A[t,u]=sum(C[t,h]*dirs[u,h] for h in range(3))*acc/sc[t]
        lam=np.linalg.solve(A+.001*np.mean(np.diag(A))*np.eye(3),gamma)
        ref={l:np.array([[Dweights[l][j]*sum(lam[u]*K[l][u,j]*dirs[u,h] for u in range(3))
                         for j in range(2)] for h in range(3)]) for l in K}
        tensor=lambda x:torch.tensor(x,dtype=torch.float64,device="cpu")
        gotdirs=D.preferred_directions(tensor(G),tensor(C))
        np.testing.assert_allclose(gotdirs.numpy(),dirs,rtol=1e-12,atol=1e-12)
        got=D.joint_solve(tensor(C),gotdirs,tensor(sc),{l:tensor(k) for l,k in K.items()},
                          {l:tensor(v) for l,v in Dweights.items()},tensor(gamma))
        np.testing.assert_allclose(got["A"].numpy(),A,rtol=1e-12,atol=1e-12)
        np.testing.assert_allclose(got["lambda"].numpy(),lam,rtol=1e-12,atol=1e-12)
        for l in K:np.testing.assert_allclose(got["patch"][l].numpy(),ref[l],rtol=1e-12,atol=1e-12)
        zero=D.joint_solve(tensor(C),gotdirs,tensor(sc),{l:tensor(k) for l,k in K.items()},
                          {l:tensor(v) for l,v in Dweights.items()},tensor([0.,0.,0.]))
        self.assertTrue(torch.equal(zero["lambda"],torch.zeros(3,dtype=torch.float64,device="cpu")))
        for bad in (math.nan,math.inf):
            with self.assertRaisesRegex(R.Halt,"HALTED-V6"):
                D.joint_solve(tensor(C),gotdirs,tensor(sc),{1:tensor([[bad,1.]]*3)},
                              {1:tensor([1.,1.])},tensor(gamma))

    def test_cpu_null_weight_margin_fp16_selection(self):
        """Prereg :75, :77–80, :210: independent floor/median, excluded competitor, fp32 add."""
        D,R=self.modules()
        import numpy as np
        import torch
        m=np.array([0.,.0001,2.,4.]);floor=.001*np.median(m)
        got,n=D.null_weights(torch.tensor(m,dtype=torch.float32,device="cpu"))
        np.testing.assert_allclose(got.numpy(),1/np.maximum(m,floor),rtol=1e-6);self.assertEqual(n,2)
        logits=torch.tensor([[7.,2.,1.],[0.,5.,5.]],device="cpu")
        leads,p=D.margin_leads(logits,torch.tensor([0,2],device="cpu"))
        self.assertEqual(p.tolist(),[1,1]);self.assertEqual(leads.tolist(),[5.,0.])
        weights=torch.tensor([[1.,2.,3.],[4.,5.,6.]],dtype=torch.float16,device="cpu")
        delta=torch.tensor([[.0007,-.002],[.003,.001]],dtype=torch.float64,device="cpu")
        expected=weights.numpy().copy()
        expected[:,[0,2]]=(expected[:,[0,2]].astype(np.float32)+delta.numpy().astype(np.float32)).astype(np.float16)
        self.assertEqual(D.write_columns(weights,[0,2],delta),2)
        np.testing.assert_array_equal(weights.numpy(),expected)
        scores={i:torch.ones(500,device="cpu") for i in range(36)}
        carriers=D.select_carriers(scores,24)
        self.assertEqual(list(carriers),list(range(9)))
        self.assertTrue(all(v==list(range(43)) for v in carriers.values()))

    def test_restore_finally_and_nonempty_hook_registry(self):
        """Prereg :129, :152–153: all36 tensors restored after write/eval/hook failures."""
        D,R=self.modules()
        import torch
        for fail in ("write","eval","hook"):
            tensors={i:torch.tensor([[i]],dtype=torch.float16,device="cpu") for i in range(36)}
            snap={i:w.clone() for i,w in tensors.items()}
            events=[]
            def restore():
                for i,w in tensors.items():w.copy_(snap[i])
                events.append("restore")
            def verify():
                self.assertTrue(all(torch.equal(tensors[i],snap[i]) for i in tensors));events.append("verify")
            def action():
                tensors[35].add_(1);raise RuntimeError(fail)
            with self.assertRaisesRegex(RuntimeError,fail):D.restored(action,restore,verify)
            self.assertEqual(events,["restore","verify"])
        with self.assertRaisesRegex(R.Halt,"HALTED-V3"):
            D.restored(lambda:None,lambda:None,lambda:(_ for _ in ()).throw(R.Halt("HALTED-V3","restore")))
        modules={"m":{"forward":{1:"existing"},"pre":{2:"existing"}}}
        before=copy.deepcopy(modules);D.check_hook_registry(before,modules)
        modules["m"]["pre"][3]="leaked"
        with self.assertRaisesRegex(R.Halt,"HALTED-V3"):D.check_hook_registry(before,modules)

    def test_json_real_writer_and_frozen_sources(self):
        """Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science."""
        D,R=self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"pass_p1.json";r=fixture()
            D.write_json(p,r);self.assertEqual(json.loads(p.read_text()),r)
            self.assertEqual(R.read_process(json.loads(p.read_text())),R.read_process(r))
            with self.assertRaisesRegex(R.Halt,"HALTED-V12"):D.write_json(p,r)
            for bad in (math.nan,math.inf,-math.inf):
                with self.assertRaisesRegex(R.Halt,"HALTED-V6"):D.write_json(Path(tmp)/"bad.json",{"science":bad})
            self.assertFalse((Path(tmp)/"bad.json").exists())
        self.assertEqual(hashlib.sha256((ROOT/"docs/C10Z_ASTRA_PREREG.md").read_bytes()).hexdigest(),PREREG)
        for path in (HERE/"c10z_astra_arms.py",HERE/"c10z_astra_read.py"):
            ast.parse(path.read_text())
        self.assertNotIn("c10e_bandknob",sys.modules)
        self.assertNotIn("transformers",sys.modules)


# §3.6 :290–313, verbatim input rows. The reader receives complete synthetic records.
WORKED = [
    (1,"n = 18, FIT","NULL-STAGE1"),
    (2,"n = 18, U (φ_μ = 0.80)","UNDERFIT-STAGE1"),
    (3,"n = 21, g = 9 (a = 12)","NULL-STAGE1"),
    (4,"n = 25, a = 16, g = 9","NULL-STAGE1"),
    (5,"n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 (above the paper's SemCon range; reported, not a qualifier)","PARTIAL"),
    (6,"n = 22, g = 10, G7 fails 3 (view, fact, depth) gates","TRADEOFF-STAGE1"),
    (7,"n = 29, gates, FIT; stage 2 Z-A1 = 67/72","TRADEOFF-SINGLE-PROCESS"),
    (8,"n = 30, gates, FIT, W1 0.3; p2 n = 29, both processes clean","PARTIAL"),
    (9,"n = 31, gates, U (φ_0^id = 22)","LEAD-UNDERFIT-STAGE1"),
    (10,"n = 24, g = 6, U","UNDERFIT-STAGE1"),
    (11,"n = 33, gates, FIT, W1 1.4","LEAD-LARGE-WRITE-STAGE1"),
    (12,"n = 26, gates, subject-free hits A + 4","PARTIAL-SUBJECT-FREE-STAGE1"),
    (13,"recipe A A7 = 19/72","HALTED-V4"),
    (14,"Z3 (d): one greedy generation differs","HALTED-V5"),
    (15,"stage 2: n = 26, Z-band FIT, gates clean, capacity matched, n_b = 23","BAND-RETAINS-QUALIFIED-GAIN"),
    (16,"stage 2: n = 26, Z-band clean, n_b = 20","BAND-NO-QUALIFIED-GAIN"),
    (17,"stage 2: n = 40, Z-band clean, n_b = 28","BAND-PARTIAL-RETENTION"),
    (18,"stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14","ATTRIBUTION-UNINFORMATIVE"),
    (19,"stage 2: n = 26, Z-band FIT, Z-band G7 fails, n_b = 24","ATTRIBUTION-TRADEOFF"),
    (20,"stage 2: n = 22, Z-band clean, n_b = 17","BAND-NO-QUALIFIED-GAIN"),
    (21,"stage 2: Z-band FIT, T = 144, B_Z = 2,304 > 2,200","ATTRIBUTION-UNMATCHED-CAPACITY"),
    (22,"n = 22, g = 10, gates, φ_μ = 0.958, φ_0^id = 24, actual `canon_full_n` = 0","PARTIAL-UNDERFIT-STAGE1"),
    (23,"n = 26, gates, FIT, W1 = 0.55 exactly","PARTIAL"),
    (24,"stage 1: a synchronized round takes 121 s","HALTED-BUDGET")]


def worked_test(case,text,expected):
    def test(self):
        D,R=self.modules()
        ns={1:18,2:18,3:21,4:25,5:22,6:22,7:29,8:30,9:31,10:24,11:33,
            12:26,13:26,14:26,15:26,16:26,17:40,18:26,19:26,20:22,21:26,22:22,23:26,24:26}
        r=fixture(n=ns[case],a={4:16,10:18,13:19}.get(case,12),
                  stage=2 if case in {5,7,8,15,16,17,18,19,20,21} else 1,
                  **({"lengths":[6]*24} if case==21 else {}))
        z=r["recipes"]["Z"]["arms"][A7]
        if case in (2,10):set_fit(z,384)
        if case==6:
            for p in z["prefix_probes"]:
                if p["view"]==5 and p["fact"]<3 and p["depth"]==1 and p["subject"]<2:probe_hit(p,"next")
        if case==7:counts(r["recipes"]["Z"]["arms"][A1],67)
        if case==9:set_fit(z,456,22);seal_fixture(r)
        if case==11:set_write(z,(1.4,))
        if case==12:
            for p in z["subject_free_probes"]:probe_hit(p,"full",p["fact"]<4)
        if case==14:r["checks"]["Z3"]["ok"]=False
        if case in (5,8):
            if case==8:set_write(z,(.3,))
            seal_schedule(r);p2=copy.deepcopy(r);second_process(p2)
            counts(p2["recipes"]["Z"]["arms"][A7],23 if case==5 else 29)
            repro=D.reproduction(r,p2)
            got=R.read_run(r,p2,repro);self.assertEqual(got["label"],expected)
            self.assertTrue(got["replicated"])
            if case==8:self.assertFalse(got["lead_replicated"])
        elif 15<=case<=21:
            band=r["recipes"]["Z-band"]["arms"][A7]
            counts(band,{15:23,16:20,17:28,18:14,19:24,20:17,21:23}[case])
            if case==18:set_fit(band,293)
            if case==19:
                for p in band["prefix_probes"]:
                    if p["view"]==0 and p["fact"]==0 and p["depth"]==1 and p["subject"]<2:probe_hit(p,"full")
            seal_schedule(r);got=R.read_process(r);self.assertEqual(got["attribution"],expected,got)
            self.assertEqual(got["base_label"],"PARTIAL" if case!=17 else "LEAD")
        else:
            if case==22:set_fit(z,460);counts(z,canon=0);seal_fixture(r)
            if case==23:set_write(z,(.55,))
            if case==24:z["write"]["round_seconds"]=[121.,1.]
            seal_schedule(r)
            got=R.classify_candidate(z,r["recipes"]["A"]["arms"][A7],R.side_gates(z,r["recipes"]["A"]["arms"][A7]),1) if case==22 else R.read_process(r)
            self.assertEqual(got["label"] if case!=23 else got["base_label"],expected,got)
            if case==23:self.assertEqual(got["next_stage"],2)
    test.__doc__="Prereg :"+str(289+case)+": "+text
    return test


for case,text,expected in WORKED:
    setattr(SpecTests,"test_worked_%02d"%case,worked_test(case,text,expected))


if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SpecTests))
    print("C10Z_ASTRA_SELFTEST_"+("PASS" if result.wasSuccessful() else "FAIL")+" tests="+str(result.testsRun))
    sys.exit(0 if result.wasSuccessful() else 1)
