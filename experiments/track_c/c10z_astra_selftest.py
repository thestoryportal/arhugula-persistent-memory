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
PREREG = "87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87"
C01_FIX = 7800.
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
             "ceilings":{"stage01":C01_FIX,"stage2":12000. if stage==2 else None,"stage3":24000. if stage==2 else None},
             "history":[{"components_s":{"remaining":1.},"scopes":{"stage01":{"elapsed_s":1.,"remaining_s":1.,"ceiling_s":C01_FIX}}}]},
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
    for projection in r["budget"]["history"]:
        projection["ceilings"] = dict(r["budget"]["ceilings"])
        for key, scope in projection["scopes"].items():
            scope["ceiling_s"] = r["budget"]["ceilings"][key]
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
            with mock.patch.object(D,"ROOT",out), self.assertRaisesRegex(R.Halt,"HALTED-V12"):
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
        b=D.Budget(100.,C01_FIX,60.,6000.,process=1,clock=lambda:clock[0])
        self.assertEqual(b.deadline(),C01_FIX+100.)
        clock[0]=C01_FIX+99.;b.project({"remaining":1.})
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"): b.project({"remaining":1.001})
        clock[0]=C01_FIX+101.
        with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):b.check()
        for stage in (2,3):
            absent=D.Budget(0.,C01_FIX,None,None,clock=lambda:0.)
            with self.assertRaisesRegex(R.Halt,"HALTED-BUDGET"):absent.enter(stage)
        b=D.Budget(100.,C01_FIX,60.,6000.,process=2,clock=lambda:clock[0]);clock[0]=200.
        self.assertEqual(b.origins["stage3"],100.)
        b.enter(2)
        self.assertEqual(b.origins["stage2"],200.)
        self.assertEqual(b.deadline(),260.)
        b=D.Budget(100.,C01_FIX,10000.,200.,process=2,clock=lambda:200.)
        b.enter(2);self.assertEqual(b.deadline(),300.)
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




# ---------------------------------------------------------------------------
# Implementation-review additions (C10Z ASTRA, 2026-10-07). Model-free: Session is
# built with __new__ and stubbed collaborators; only tiny CPU tensors are used.
# Each test pins a spec gate/order/halt that the original 50 tests left unexercised.
# ---------------------------------------------------------------------------
import types as _types


def _write_session(D, stage=2, budget=None):
    import torch
    s = D.Session.__new__(D.Session); events = []
    s.sync = lambda: None; s.restore = lambda: None; s.verify_restore = lambda where: None
    s.hooks_check = lambda: None; s.footprint = lambda carriers: events.append(("footprint", dict(carriers)))
    s.geometry = lambda *a: {}
    s.arms = {A7: {"s0": "coined"}, A2: {"s0": "two"}}
    s.timings = {}; s.stage = stage; s.D_floored = 0; s.checks = {"Z7": {"tau_head": .02}}
    s.budget = budget or D.Budget(0., C01_FIX, None, None, clock=lambda: 0.)
    s.batches = {k: {"requirements": [{"row": 0, "fact": 0, "view": 0, "q": 0, "index": 1, "target": 0}],
                     "target_lengths": [1], "T_pad": 2} for k in (A7, A2)}
    s.weights = {35: torch.ones((2, 4), dtype=torch.float16)}; s.pristine = {35: s.weights[35].clone()}
    s.carrier_choice = {35: [0, 1]}

    def observe(batch, carriers=None, full=False, trace_layers=None):
        events.append(("observe", carriers is not None))
        return {"leads": torch.tensor([1.]), "competitors": torch.tensor([1]), "targets": torch.tensor([0]),
                "keys": {35: torch.ones((1, 2 if carriers else 4))}, "scales": torch.ones(1),
                "native_gathered": torch.tensor([[1., 0.]]), "head_error": 0., "head_seconds": 0.,
                "logits_bytes": 0, "conversion_bytes": 0}
    s.observe = observe
    s.choose = lambda obs, batch, mode, cap=None: dict(s.carrier_choice)
    f64 = lambda v: torch.tensor(v, dtype=torch.float64)
    s.quantities = lambda obs, carriers: (torch.tensor([0]), f64([[1., 0.]]), f64([[1., 0.]]), f64([1.]),
                                          {35: f64([[1.] * len(carriers[35])])}, {35: f64([1.] * len(carriers[35]))})
    s.covectors = lambda obs: f64([[1., 0.]])
    return s, events


REQ_A7 = [{"subject": "s0", "target_new": {"str": " coined"}}]
REQ_A2 = [{"subject": "s0", "target_new": {"str": " two"}}]


class ReviewGapTests:
    def test_review_stage0_law3_gate_precedes_all_new_work(self):
        """Prereg :120, :123, :302 (row 13): LAW#3 miss halts V4 with baseline-only record; nothing runs before the gate."""
        D, R = self.modules()

        class Stop(Exception):
            pass
        for passing in (False, True):
            with tempfile.TemporaryDirectory() as tmp:
                s = D.Session.__new__(D.Session); events = []
                s.out = Path(tmp); s.process = 1; s.gates = D.Gates(); s.timings = {}; s.loaded_manifest = None
                s.budget = _types.SimpleNamespace(project=lambda costs: None, check=lambda: None)
                recipe = fixture(n=18)["recipes"]["A"]
                if not passing:
                    counts(recipe["arms"][A7], n=19)
                s.run_recipe = lambda name, arms: (events.append(("run_recipe", s.gates.law3)), recipe)[1]

                def ev(name, ret=None):
                    def f(*a, **k):
                        events.append((name, s.gates.law3))
                        if name == "axes_pre":
                            raise Stop()
                        return ret
                    return f
                s.M = _types.SimpleNamespace(CONTEXT_TEMPLATES_CACHE=[["{}"], ["a. {}", "b. {}", "c. {}", "d. {}", "e. {}"]])
                s.make_batches = ev("make_batches", {}); s.restore = ev("restore"); s.verify_restore = ev("verify_restore")
                s.H = _types.SimpleNamespace(axes_pre=ev("axes_pre"), PTEST=[])
                for name in ("probe_population", "probe_hits", "observe", "make_batch", "z0", "eval_guard",
                             "prepare_instruments", "numeric_checks", "evaluation_signature", "make_manifest", "write_checks"):
                    setattr(s, name, ev(name))
                if passing:
                    with self.assertRaises(Stop):
                        s.stage0()
                    self.assertEqual(events[0], ("run_recipe", False))
                    self.assertTrue(len(events) > 1 and all(law3 for _, law3 in events[1:]), events)
                else:
                    with self.assertRaisesRegex(R.Halt, "HALTED-V4"):
                        s.stage0()
                    self.assertEqual(events, [("run_recipe", False)])
                    rec = json.loads((s.out / "pass_p1.json").read_text())
                    self.assertEqual((rec["outcome"], rec["halt"]["code"], list(rec["recipes"])), ("HALTED", "HALTED-V4", ["A"]))

    def test_review_Z5_footprint_rejects_any_write_outside_selected_columns(self):
        """Prereg :80, :152: only selected W_down columns may differ; every other parameter byte-identical."""
        D, R = self.modules()
        import torch

        def session():
            s = D.Session.__new__(D.Session)
            s.weights = {l: torch.arange(24, dtype=torch.float16).reshape(4, 6) + l for l in range(36)}
            s.pristine = {l: w.clone() for l, w in s.weights.items()}
            norm = torch.ones(4, dtype=torch.float16)
            params = [("model.layers.%d.mlp.down_proj.weight" % l, w) for l, w in s.weights.items()] + [("model.norm.weight", norm)]
            s.H = _types.SimpleNamespace(model=_types.SimpleNamespace(named_parameters=lambda: list(params)))
            s.parameter_hashes = {n: D.tensor_hash(p) for n, p in params}; s.checks = {}; s.check_memory = lambda: None
            return s, norm
        s, _ = session(); s.weights[3][:, 2] += 1; s.footprint({3: [2]})
        self.assertEqual(s.checks["Z5"]["writes"][0]["changed_pairs"], [[3, 2]])
        for mutate in (lambda s, n: s.weights[3][:, 3].add_(1), lambda s, n: s.weights[5][:, 2].add_(1), lambda s, n: n.add_(1)):
            s, norm = session(); s.weights[3][:, 2] += 1; mutate(s, norm)
            with self.assertRaisesRegex(R.Halt, "HALTED-V5"):
                s.footprint({3: [2]})

    def test_review_Z6_restore_covers_all_36_and_verify_detects_drift(self):
        """Prereg :64, :129, :153; V3 :216: full 36-layer restore, byte-hash verification halts on drift."""
        D, R = self.modules()
        import torch
        s = D.Session.__new__(D.Session)
        s.weights = {l: torch.full((2, 3), float(l), dtype=torch.float16) for l in range(36)}
        s.pristine = {l: w.clone() for l, w in s.weights.items()}
        s.layer_hashes = {str(l): D.tensor_hash(w) for l, w in s.pristine.items()}; s.restores = []; s.hooks_check = lambda: None
        for l in (0, 17, 35):
            s.weights[l][0, 0] += 1
        s.restore(); s.verify_restore("after restore")
        self.assertTrue(all(torch.equal(s.weights[l], s.pristine[l]) for l in range(36)))
        s.weights[35][1, 2] += 1
        with self.assertRaisesRegex(R.Halt, "HALTED-V3"):
            s.verify_restore("drift")
        self.assertEqual([r["ok"] for r in s.restores], [True, False])

    def test_review_wrapper_delegates_under_standing_law5(self):
        """Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments."""
        D, R = self.modules()
        s = D.Session.__new__(D.Session); s.gates = D.Gates()
        s.original_edit = lambda hp, rq, P, c: "original"; s.calls = {"astra_calls": 0, "original_calls": 0}
        s.write_arm = lambda requests, mode: "astra"
        s.H = _types.SimpleNamespace(_LAW5_DEFAULT_CTX=True); s.mode = "astra"
        self.assertEqual(s.wrapper(None, [], None, None), "original")
        self.assertEqual(s.calls, {"astra_calls": 0, "original_calls": 0})
        s.H._LAW5_DEFAULT_CTX = False
        with self.assertRaisesRegex(R.Halt, "HALTED-V4"):
            s.wrapper(None, [], None, None)
        s.gates.law3 = True; s.gates.ready = True
        self.assertEqual(s.wrapper(None, [], None, None), "astra")
        s.mode = None; self.assertEqual(s.wrapper(None, [], None, None), "original")
        self.assertEqual(s.calls, {"astra_calls": 2, "original_calls": 1})

    def test_review_write_round_cap_columns_and_capacity(self):
        """Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only."""
        D, R = self.modules()
        import torch
        s, events = _write_session(D)
        s.write_arm(REQ_A7, "astra")
        w = s.current["write"]
        self.assertEqual((w["rounds_used"], w["stop_reason"], len(w["trace"])), (10, "round cap", 10))
        self.assertTrue(torch.equal(s.weights[35][:, 2:], s.pristine[35][:, 2:]))
        self.assertFalse(torch.equal(s.weights[35][:, :2], s.pristine[35][:, :2]))
        self.assertEqual(s.Z_capacity, 2)
        s.carrier_choice = {35: [0, 1, 2]}; s.write_arm(REQ_A2, "astra")
        self.assertEqual(s.Z_capacity, 2)

    def test_review_write_prestart_projection_refuses_before_observation(self):
        """Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling."""
        D, R = self.modules()
        b = D.Budget(0., C01_FIX, None, None, clock=lambda: C01_FIX-1)
        s, events = _write_session(D, budget=b)
        with self.assertRaisesRegex(R.Halt, "HALTED-BUDGET"):
            s.write_arm(REQ_A7, "astra")
        self.assertEqual(events, [])

    def test_review_stage1_round_over_120s_halts_in_run(self):
        """Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run."""
        D, R = self.modules()
        real = D.time; t = [0.]

        def mono():
            t[0] += 61.; return t[0]
        D.time = _types.SimpleNamespace(monotonic=mono)
        try:
            s, events = _write_session(D, stage=1)
            with self.assertRaisesRegex(R.Halt, "HALTED-BUDGET"):
                s.write_arm(REQ_A7, "astra")
            self.assertEqual(sum(1 for e in events if e[0] == "footprint"), 1)
        finally:
            D.time = real

    def test_review_stage_call_refusals(self):
        """Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch."""
        D, R = self.modules()
        launched = []

        class Child:
            def poll(self):
                return 1
        real_sp, real_res, real_wait = D.subprocess, D.resident, D.wait_stage
        D.subprocess = _types.SimpleNamespace(Popen=lambda *a, **k: (launched.append("p1"), Child())[1], DEVNULL=None, STDOUT=None)
        D.resident = lambda *a, **k: (launched.append("p2"), 0)[1]
        D.wait_stage = lambda *a, **k: (launched.append("wait"), 0)[1]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                used = tmp / "used"; used.mkdir(); D.write_json(used / "pass_p1.json", {"outcome": "COMPLETE"})
                with self.assertRaisesRegex(R.Halt, "fresh OUT_DIR"):
                    D.stage_call(0, used)
                self.assertEqual(launched, [])
                with self.assertRaisesRegex(R.Halt, "resident failed"):
                    D.stage_call(0, tmp / "fresh")
                self.assertEqual(launched, ["p1"]); launched.clear()
                # stage 2 only for a K1 survivor
                for n, ok in ((18, False), (26, True)):
                    out = tmp / ("s2_%d" % n); out.mkdir(); D.write_json(out / "pass_p1.json", fixture(n=n))
                    D.write_json(out / "run.json", {"attempt_id": "fixture-attempt", "pid": 1, "completed": 1, "requested": None,
                                                     "closed": False, "halt": None, "reading": None,
                                                     "launch": {"stage2": 100., "stage3": None}})
                    if ok:
                        self.assertEqual(D.stage_call(2, out), 0)
                    else:
                        with self.assertRaisesRegex(R.Halt, "K1 survivor"):
                            D.stage_call(2, out)
                    self.assertEqual(json.loads((out / "run.json").read_text())["requested"], 2 if ok else None)
                self.assertEqual(launched, ["wait"]); launched.clear()
                # stage 3 only after clean K2 and with a recorded stage-3 ceiling
                bench,binding=_bench_tree(D.ROOT)
                record=fixture(n=22,stage=2);record["budget"]["ceilings"]=dict(binding["ceilings"]);seal_schedule(record)
                good = tmp / "good"; _attempt_dir(D, good, record, {"launch":_selected_launch(bench,binding)})
                self.assertEqual(R.read_directory(good)["next_stage"], 3)
                self.assertEqual(D.stage_call(3, good), 0); self.assertEqual(launched, ["p2"]); launched.clear()
                r = fixture(n=29, stage=2); counts(r["recipes"]["Z"]["arms"][A1], 67)
                bad = tmp / "bad"; _attempt_dir(D, bad, r, {})
                self.assertIsNone(R.read_directory(bad)["next_stage"])
                with self.assertRaisesRegex(R.Halt, "HALTED-V12"):
                    D.stage_call(3, bad)
                noceil = tmp / "noceil"
                _attempt_dir(D, noceil, fixture(n=22, stage=2), {"launch": _launch(stage3=None)})
                with self.assertRaisesRegex(R.Halt, "HALTED-V12: stage3 requires"):
                    D.stage_call(3, noceil)
                self.assertEqual(launched, [])
        finally:
            D.subprocess, D.resident, D.wait_stage = real_sp, real_res, real_wait

    def test_review_reader_instrument_ceilings_audits_and_capacity(self):
        """Prereg :147, :151–155, V2/V5/V9/V12, §2.5, §2.11: each recorded gate outcome is re-checked by the reader."""
        D, R = self.modules()

        def z0(r):
            c = r["checks"]["Z0"]; c.update(sigma_shape=.13, tau_shape=.26); c["prefix_shape_leads"][0][0] += .13

        def p2_origin(r):
            second_process(r); r["budget"]["origins"]["stage3"] = 5.
        cases = [("HALTED-V5", 1, lambda r: r["checks"]["Z7"].update(sigma_head=.13, tau_head=.26)),
                 ("HALTED-V5", 1, z0),
                 ("HALTED-V5", 1, lambda r: r["checks"]["Z4"].update(loop_relative_error=2e-10)),
                 ("HALTED-V5", 1, lambda r: r["checks"]["Z5"]["writes"][0].update(changed_pairs=[[35, 1]])),
                 ("HALTED-V9", 1, lambda r: r["recipes"]["Z"]["audit"].update(Z_OVERRIDE_HITS=1)),
                 ("HALTED-V2", 1, lambda r: r["recipes"]["Z"]["law5_gate"].update(expr_delta=.05)),
                 ("HALTED-V12", 1, lambda r: set_write(r["recipes"]["Z"]["arms"][A7], capacity=1286)),
                 ("HALTED-V12", 2, lambda r: set_write(r["recipes"]["Z-band"]["arms"][A7], capacity=1286, band=True)),
                 ("HALTED-BUDGET", 1, p2_origin)]
        for expected, stage, mutate in cases:
            with self.subTest(expected=expected, stage=stage):
                r = fixture(stage=stage); mutate(r); seal_fixture(r)
                self.assertEqual(R.read_process(r)["label"], expected)
        z2 = R.z2_evidence([[.02, 6.]] + [[6.]] * 23, [True] * 24, .02)
        self.assertEqual((z2["checked"], z2["ambiguous"]), (23, 1))

    def test_review_cross_process_replication_needs_clean_pair(self):
        """Prereg :277: LEAD/PARTIAL replicate only when both clean; differing base labels otherwise -NOT-REPLICATED."""
        D, R = self.modules()
        repro = {"R1": {"status": "PASS"}, "R2": {"difference": 0}, "R3": {"disagree": 0},
                 "artifact_identity": "EXACT", "numeric_behavioral_reproduction": "PASS"}
        got = R.aggregate({"base_label": "LEAD", "qualifiers": []}, {"base_label": "PARTIAL", "qualifiers": ["LARGE-WRITE"]}, repro)
        self.assertFalse(got["replicated"]); self.assertIn("NOT-REPLICATED", got["qualifiers"])
        got = R.aggregate({"base_label": "LEAD", "qualifiers": []}, {"base_label": "TRADEOFF", "qualifiers": []}, repro)
        self.assertEqual(got["label"], "TRADEOFF-NOT-REPLICATED")


def _attempt_dir(D, out, record, run_extra):
    out.mkdir(parents=True, exist_ok=True)
    for n, b in {"context_templates.json": b"[]", "dstats.pt": b"d", "G.pt": b"g", "overlap_audit.json": b"{}"}.items():
        (out / n).write_bytes(b)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    parts = record["manifest"]["parts"]
    for n, k in (("context_templates.json", "context_templates_sha256"), ("dstats.pt", "dstats_sha256"), ("G.pt", "G_sha256")):
        parts[k] = sha(out / n)
    record["H_in"] = record["manifest"]["H_in"] = digest(parts)
    D.write_json(out / "manifest.json", record["manifest"])
    D.write_json(out / "pristine_hash.json", {"H_pristine": record["H_pristine"], "layers": {str(l): "a" * 64 for l in range(36)},
                                              "parameters": {"x": "a" * 64}, "safetensors": {"m": "a" * 64}})
    record["artifact_hashes"] = {n: sha(out / n) for n in ("context_templates.json", "dstats.pt", "G.pt", "pristine_hash.json",
                                                          "manifest.json", "overlap_audit.json")}
    seal_schedule(record)
    D.write_json(out / "pass_p1.json", record)
    run = {"schema": "c10z_astra-v2.2", "attempt_id": record["attempt_id"], "pid": record["pid"], "process": 1, "completed": 2,
           "requested": None, "closed": True, "launch": _launch(attempt_id=record["attempt_id"]),
           "reading": None, "halt": None}
    run.update(run_extra); D.write_json(out / "run.json", run)


for _name in dir(ReviewGapTests):
    if _name.startswith("test_review_"):
        setattr(SpecTests, _name, getattr(ReviewGapTests, _name))



# Fix-round-1 additions. The proposed 60-test source above remains verbatim.
# Existing conditional-label fixtures have expansion budgets; absent budgets are
# exercised explicitly below against the full reader and resident.
from contextlib import redirect_stderr
import io
from unittest import mock

_proposed_fixture = fixture
def fixture(*args, **kwargs):
    r = _proposed_fixture(*args, **kwargs)
    r["manifest"]["parts"]["go_sha256"] = "a" * 64
    r["H_in"] = r["manifest"]["H_in"] = digest(r["manifest"]["parts"])
    r["budget"]["ceilings"].update(stage2=12000., stage3=24000.)
    seal_schedule(r)
    return r


def _launch(**over):
    go = _go_record()
    value = {"attempt_id":"fixture-attempt","stage01":C01_FIX,"stage2":12000.,"stage3":24000.,
             "telemetry":False,"telemetry_inertness":None,"go":go,"go_sha256":"a"*64,
             "benchmark":{"path":"/x/results/c10z_astra_benchmark/T/benchmark.json",
                          "sha256":go["benchmark_sha256"],"script_sha256":go["benchmark_script_sha256"],
                          "sources":{},"env":{},"ceilings":dict(go["ceilings"])}}
    value.update(over)
    return value


def _go_record(binding=None):
    return {"decisions": {"0": "D-C10z-go-0", "1": "D-C10z-go-1", "2": "D-C10z-go-2"},
            "operator_yes": True, "recorded_by": "operator", "recorded_at": "2026-10-07T12:00:00Z",
            "one_gpu_job": True, "benchmark_sha256":"a"*64, "benchmark_script_sha256":"b"*64,
            "ceilings":{"stage01":C01_FIX,"stage2":12000.,"stage3":24000.}, **(binding or {})}


_proposed_stage_calls = SpecTests.test_review_stage_call_refusals
def _review_stage_calls_with_go(self):
    with tempfile.TemporaryDirectory() as tmp:
        D, R = self.modules(); root = Path(tmp); bench, binding = _bench_tree(root)
        path = root / "go.json"; path.write_text(json.dumps(_go_record(binding)))
        with mock.patch.object(D, "ROOT", root), mock.patch.object(D,"benchmark_module",side_effect=lambda:importlib.import_module("c10z_astra_benchmark"),create=True), mock.patch.dict(os.environ, {"C10Z_GO_RECORD": str(path), "C10Z_BENCHMARK_RECORD":str(bench)}):
            return _proposed_stage_calls(self)
_review_stage_calls_with_go.__doc__ = _proposed_stage_calls.__doc__
SpecTests.test_review_stage_call_refusals = _review_stage_calls_with_go


class Child:
    def poll(self):
        return 1


def stage1_attempt(out, n, closed, completed, reading, launch):
    D = importlib.import_module("c10z_astra_arms")
    record = fixture(n=n)
    record["budget"]["ceilings"].update(stage2=launch["stage2"], stage3=launch["stage3"])
    _attempt_dir(D, out, record, {"completed": completed, "closed": closed,
                                "reading": reading, "launch": launch})


class BlockingDemos(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms"); self.R = importlib.import_module("c10z_astra_read")
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.launched = []
        self.patchers = [
            mock.patch.object(self.D, "ROOT", Path(self.temp.name)),
            mock.patch.object(self.D, "benchmark_module", side_effect=lambda:importlib.import_module("c10z_astra_benchmark"),create=True),
            mock.patch.object(self.D, "subprocess", _types.SimpleNamespace(
                Popen=lambda *a, **k: (self.launched.append("p1"), Child())[1], DEVNULL=None, STDOUT=None)),
            mock.patch.object(self.D, "resident", lambda *a, **k: (self.launched.append("p2"), 0)[1]),
            mock.patch.dict(os.environ)]
        for patcher in self.patchers:
            patcher.start(); self.addCleanup(patcher.stop)
        os.environ.pop("C10Z_GO_RECORD", None)
        os.environ.pop("C10Z_RESIDENT", None)

    def main(self, out, stage):
        with mock.patch.dict(os.environ, {"C10Z_OUT_DIR": str(out)}), mock.patch.object(
                sys, "argv", ["c10z_astra_arms.py", str(stage)]):
            return self.D.main()

    def test_B1_stage0_refuses_without_recorded_go_decision(self):
        """Prereg :3, :341–344: operator go before stage 0; blocking demo B1."""
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(self.R.Halt):
                self.D.stage_call(0, Path(tmp) / "fresh")
        self.assertEqual(self.launched, [], "stage 0 launched without a go decision")

    def test_B2_stray_stage_call_after_terminal_K1_keeps_the_result(self):
        """Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "attempt"
            stage1_attempt(out, 18, True, 1, {"label": "NULL-STAGE1", "next_stage": None},
                           _launch(stage2=None, stage3=None))
            before = (out / "pass_p1.json").read_bytes()
            self.assertEqual(self.R.read_directory(out)["label"], "NULL-STAGE1")
            self.assertEqual(self.main(out, 2), 2)
            self.assertEqual(self.R.read_directory(out)["label"], "NULL-STAGE1")
            self.assertEqual((out / "pass_p1.json").read_bytes(), before)

    def test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record(self):
        """Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "attempt"
            stage1_attempt(out, 26, False, 1, {"label": "PARTIAL", "next_stage": 2},
                           _launch(stage2=None, stage3=None))
            rec = json.loads((out / "pass_p1.json").read_text())
            reading = self.R.read_process(rec)
            self.assertEqual((reading["label"], reading["next_stage"], rec["omissions"]["G0"]["reason"]),
                             ("PARTIAL-STAGE1", None, "ABSENT-CEILING"))
            before = (out / "pass_p1.json").read_bytes()
            self.assertEqual(self.main(out, 2), 2)
            self.assertEqual((out / "pass_p1.json").read_bytes(), before)


_resident_runtime = importlib.import_module("c10z_astra_arms").resident


def _mock_resident(D, R, out, record, launch, deadline=False, metrics=None):
    """Run the real resident/terminal/watchdog code with CPU-only collaborators."""
    callbacks = []; exits = []; events = []; clock = [100.]
    real_budget = D.Budget
    def now():
        if metrics is not None: metrics["clock"] = metrics.get("clock",0)+1
        return clock[0]
    def monotonic():
        if metrics is not None: metrics["monotonic"] = metrics.get("monotonic",0)+1
        return clock[0]
    def make_budget(start,stage01,stage2,stage3,process):
        value=real_budget(start,stage01,stage2,stage3,process=process,clock=now)
        if metrics is not None:
            for name in ("project","check"):
                original=getattr(value,name)
                def counted(*a,_name=name,_call=original,**kw):
                    metrics[_name]=metrics.get(_name,0)+1
                    return _call(*a,**kw)
                setattr(value,name,counted)
            for name in ("hooks_check","sync","science_forwards"):metrics[name]=0
        return value

    class Event:
        def wait(self, seconds): return False
        def set(self): pass
    class Thread:
        def __init__(self, target, daemon): callbacks.append(target)
        def start(self): pass
    def submit(_):
        run = D.load_json(out / "run.json")
        run["requested"] = run["completed"] + 1
        D.write_json(out / "run.json", run, replace=True)

    class SessionStub:
        def __init__(self, path, process, budget, input_dir):
            self.budget = budget; self.process = process
            self.recipes = record["recipes"]; self.checks = record["checks"]
            self.memory = record["memory"]; self.restores = record["restores"]
            events.append(("constructed", budget))
        def stage0(self): events.append("stage0")
        def stage1(self):
            events.append("stage1")
            return R.read_process(record)
        def stage2(self):
            events.append("stage2"); self.budget.enter(2)
            if deadline:
                clock[0] += self.budget.durations["stage2"]
                callbacks[0]()
            return {"label": "PARTIAL-SINGLE-PROCESS", "next_stage": None}
        def close(self): events.append("closed"); self.closed_model = True
        def restore(self): events.append("restored")
        def verify_restore(self, where): events.append(("verified", where))

    with mock.patch.object(D, "Session", SessionStub), mock.patch.object(
            D, "Budget", make_budget), mock.patch.object(
            D, "time", _types.SimpleNamespace(monotonic=monotonic, sleep=submit)), mock.patch.object(
            D, "threading", _types.SimpleNamespace(Event=Event, Thread=Thread, RLock=__import__("threading").RLock)), mock.patch.object(
            D.os, "_exit", lambda code: exits.append(code)):
        rc = _resident_runtime(out, 1, launch, start=clock[0])
    return rc, events, exits


class Fix1Tests(BlockingDemos):
    # Inherit the three always-on blocking demos; load them only once below.
    def test_fix1_go_malformed_fields_refuse_without_any_attempt_write(self):
        """Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation."""
        candidates = [None, [], {}, {"decisions": []}]
        valid = _go_record()
        for key in valid:
            bad = copy.deepcopy(valid); bad.pop(key); candidates.append(bad)
        for key, values in {"operator_yes": [False, 1, "true", None],
                            "one_gpu_job": [False, 1, "true", None],
                            "recorded_by": ["", "  ", None, 1],
                            "recorded_at": ["", "  ", None, 1]}.items():
            for value in values:
                bad = copy.deepcopy(valid); bad[key] = value; candidates.append(bad)
        for key in ("0", "1", "2"):
            for value in ("", " ", None, 1, "not-a-decision", "D-"):
                bad = copy.deepcopy(valid); bad["decisions"][key] = value; candidates.append(bad)
            bad = copy.deepcopy(valid); bad["decisions"].pop(key); candidates.append(bad)
        bad = copy.deepcopy(valid); bad["decisions"]["3"] = "D-extra"; candidates.append(bad)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); go = root / "go.json"
            for index, record in enumerate(candidates + ["invalid-json", "missing-file"]):
                with self.subTest(case=index):
                    out = root / ("out%d" % index)
                    if record == "missing-file":
                        os.environ["C10Z_GO_RECORD"] = str(root / "missing.json")
                    elif record == "invalid-json":
                        go.write_text("{"); os.environ["C10Z_GO_RECORD"] = str(go)
                    elif record is None:
                        os.environ.pop("C10Z_GO_RECORD", None)
                    else:
                        go.write_text(json.dumps(record)); os.environ["C10Z_GO_RECORD"] = str(go)
                    with mock.patch.object(self.D, "diagnostic", side_effect=AssertionError("refusal wrote diagnostic")):
                        with redirect_stderr(io.StringIO()) as err:
                            self.assertEqual(self.main(out, 0), 2)
                    self.assertTrue(err.getvalue().strip())
                    self.assertFalse(out.exists(), "refusal created the attempt directory")
                    self.assertEqual(self.launched, [])

    def test_fix1_go_launch_copy_and_manifest_sha(self):
        """Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in."""
        D, R = self.D, self.R
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); bench,binding=_bench_tree(D.ROOT)
            go = root / "go.json"; go.write_text(json.dumps(_go_record(binding), indent=2))
            os.environ["C10Z_BENCHMARK_RECORD"]=str(bench)
            expected = hashlib.sha256(go.read_bytes()).hexdigest(); out = root / "attempt"
            os.environ["C10Z_GO_RECORD"] = str(go)
            def launch(*args, **kwargs):
                self.launched.append("p1")
                policy = json.loads(kwargs["env"]["C10Z_LAUNCH"])
                self.assertEqual(kwargs["env"]["C10Z_GO_RECORD"], str(go))
                D.write_json(out / "run.json", {"launch": policy})
                return Child()
            with mock.patch.object(D, "subprocess", _types.SimpleNamespace(
                    Popen=launch, DEVNULL=None, STDOUT=None)), mock.patch.object(D, "wait_stage", return_value=0):
                self.assertEqual(D.stage_call(0, out), 0)
            launch_record = D.load_json(out / "run.json")["launch"]
            self.assertEqual(launch_record["go"], _go_record(binding))
            self.assertEqual(launch_record["go_sha256"], expected)
            r = fixture(n=18); _attempt_dir(D, out / "resident", r, {})
            rc, events, _ = _mock_resident(D, R, out / "resident", r, launch_record)
            self.assertEqual(rc, 0)
            self.assertEqual(D.load_json(out / "resident/run.json")["launch"]["go"], _go_record(binding))
            budget = events[0][1]; self.assertEqual(budget.go_sha256, expected)
            s = D.Session.__new__(D.Session); s.budget = budget; s.out = out
            snapshot = root / "hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/test-revision"
            snapshot.mkdir(parents=True)
            for name in ("tokenizer.json", "tokenizer_config.json"): (snapshot / name).write_text("{}")
            import torch
            s.H = _types.SimpleNamespace(REV="test-revision", FICTION=list(range(24)), CANON="{}",
                req=lambda p, subj, value: {"subject": subj, "value": value}, DEV="mps",
                model=_types.SimpleNamespace(config=_types.SimpleNamespace(_attn_implementation="eager"),
                    training=False, parameters=lambda: iter([torch.zeros(1, dtype=torch.float16)])))
            s.arms = {a: {i: str(i) for i in range(24)} for a in ARMS}; s.batches = r["manifest"]["parts"]["batches"]
            s.H_pristine = "a"*64; s.safetensors = {"m": "a"*64}; s.fingerprint = {"start": {}}
            s.dstats = {"dataset": {}}; s.covariance_paths = lambda: {}
            s.loaded_manifest = None
            with mock.patch.object(D, "ROOT", root), mock.patch.object(D, "sha256_file", return_value="a"*64), mock.patch.dict(
                    sys.modules, {"transformers": _types.SimpleNamespace(__version__="4.51.0")}):
                parts = s.input_parts()
                self.assertEqual(parts["go_sha256"], expected)
                s.make_manifest()
            self.assertEqual(s.manifest["H_in"], R.json_digest(s.manifest["parts"]))
            changed = copy.deepcopy(parts); changed["go_sha256"] = "b"*64
            self.assertNotEqual(R.json_digest(changed), s.manifest["H_in"])

    def test_fix1_go_sha_is_mandatory_reader_provenance(self):
        """Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest."""
        for value in (None, "not-a-sha"):
            r = fixture()
            if value is None: r["manifest"]["parts"].pop("go_sha256")
            else: r["manifest"]["parts"]["go_sha256"] = value
            r["H_in"] = r["manifest"]["H_in"] = digest(r["manifest"]["parts"])
            self.assertEqual(self.R.read_process(r)["label"], "HALTED-V12")

    def test_fix1_refusals_preserve_finished_attempt_byte_for_byte(self):
        """Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt."""
        D, R = self.D, self.R
        for stage, n, completed in ((0, 18, 1), (1, 18, 1), (2, 18, 1), (3, 29, 2)):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "attempt"; r = fixture(n=n, stage=completed)
                if completed == 2: counts(r["recipes"]["Z"]["arms"][A1], 67)
                _attempt_dir(D, out, r, {"completed": completed})
                before = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()}
                label = R.read_directory(out)["label"]
                with mock.patch.object(D, "diagnostic", side_effect=AssertionError("refusal called diagnostic")):
                    self.assertEqual(self.main(out, stage), 2)
                after = {str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()}
                self.assertEqual(before, after); self.assertEqual(R.read_directory(out)["label"], label)

    def test_fix1_halt_sidecar_retains_completed_observations_for_both_processes(self):
        """Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations."""
        D, R = self.D, self.R
        for process, code in ((1, "HALTED-BUDGET"), (1, "HALTED-V3"), (2, "HALTED-BUDGET")):
            with self.subTest(process=process, code=code), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); out = root / "attempt"; first = fixture(stage=2)
                _attempt_dir(D, out, first, {})
                target = out
                if process == 2:
                    target = out / "process2"; second = fixture(); second_process(second)
                    _attempt_dir(D, target, second, {"process": 2, "pid": second["pid"]})
                    (target / "pass_p1.json").rename(target / "pass_p2.json")
                passpath = target / ("pass_p%d.json" % process); before = passpath.read_bytes()
                with mock.patch.object(D, "ROOT", root):
                    value = D.diagnostic(target, code, "synthetic halt after completed pass")
                self.assertEqual(D.load_json(root / "architecture_profile/c10z_astra_halt_diagnostic.json"), value)
                self.assertEqual(passpath.read_bytes(), before)
                self.assertEqual(value["observations"], json.loads(before))
                self.assertEqual(D.load_json(target / ("halt_p%d.json" % process)), value)
                # The durable halt file governs even if a run.json has no halt marker.
                run = D.load_json(target / "run.json"); run["halt"] = None
                D.write_json(target / "run.json", run, replace=True)
                got = R.read_directory(out)
                self.assertEqual(got["label"], code); self.assertFalse(got["scientific_verdict"])
                self.assertIn(json.loads(before), got["observations"])
                self.assertEqual(got["observations"], [first, json.loads(before)] if process == 2 else [first])

    def test_fix1_watchdog_preserves_last_published_record(self):
        """Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT."""
        D, R = self.D, self.R
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); out = root / "attempt"; r = fixture()
            _attempt_dir(D, out, r, {})
            before = (out / "pass_p1.json").read_bytes()
            launch = _launch(attempt_id=r["attempt_id"],stage2=60.,stage3=None)
            watchdog_records = []; real_diagnostic = D.diagnostic
            def capture_diagnostic(path, code, detail, session=None):
                value = real_diagnostic(path, code, detail, session)
                if str(detail).startswith("watchdog:"):
                    self.assertEqual(D.load_json(out / "halt_p1.json"), value)
                    self.assertEqual(D.load_json(root / "architecture_profile/c10z_astra_halt_diagnostic.json"), value)
                    watchdog_records.append(value)
                return value
            with mock.patch.object(D, "ROOT", root), mock.patch.object(D, "diagnostic", capture_diagnostic):
                rc, events, exits = _mock_resident(D, R, out, r, launch, deadline=True)
            self.assertEqual(len(watchdog_records), 1, "watchdog did not publish its diagnostic before exit")
            self.assertEqual(watchdog_records[0]["observations"], json.loads(before))
            self.assertEqual(rc, 2); self.assertEqual(exits, [2])
            self.assertIn("stage2", events)
            self.assertEqual((out / "pass_p1.json").read_bytes(), before)
            self.assertEqual(D.load_json(out / "halt_p1.json")["observations"], json.loads(before))
            got = R.read_directory(out)
            self.assertEqual(got["label"], "HALTED-BUDGET")
            self.assertEqual(got["observations"], [json.loads(before)])

    def test_fix1_absent_ceilings_terminal_labels_and_resident_close(self):
        """Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim."""
        D, R = self.D, self.R
        for stage, expected in ((1, "PARTIAL-STAGE1"), (2, "PARTIAL-SINGLE-PROCESS")):
            r = fixture(stage=stage); r["budget"]["ceilings"]["stage%d" % (stage+1)] = None
            seal_schedule(r)
            got = R.read_process(r); self.assertEqual(got["label"], expected); self.assertIsNone(got["next_stage"])
            if stage == 1:
                self.assertEqual(r["omissions"]["G0"], {"status": "NOT-RUN", "reason": "ABSENT-CEILING"})
                self.assertEqual(r["omissions"]["Z-band"], r["omissions"]["G0"])
                with tempfile.TemporaryDirectory() as tmp:
                    out = Path(tmp); _attempt_dir(D, out, r, {})
                    launch = _launch(attempt_id=r["attempt_id"],stage2=None,stage3=None)
                    rc, events, _ = _mock_resident(D, R, out, r, launch)
                    self.assertEqual(rc, 0); self.assertNotIn("stage2", events); self.assertIn("closed", events)
                    self.assertTrue(D.load_json(out / "run.json")["closed"])
            else:
                self.assertEqual(r["omissions"]["process2"], {"status": "NOT-RUN", "reason": "ABSENT-CEILING"})

    def test_fix1_relative_outdir_resolved_at_main_parse(self):
        """Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd."""
        captured = []
        with mock.patch.object(self.D, "stage_call", lambda stage, out: (captured.append(out), 2)[1]):
            self.assertEqual(self.main(Path("relative/attempt"), 0), 2)
        self.assertEqual(captured, [(Path.cwd() / "relative/attempt").resolve()])

    def test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write(self):
        """Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched."""
        real_subprocess = importlib.import_module("subprocess")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "tools").mkdir(); (root / ".venv/bin").mkdir(parents=True)
            shell = root / "tools/run_c10z_stage.sh"; shell.write_text((ROOT / "tools/run_c10z_stage.sh").read_text())
            python = root / ".venv/bin/python"
            python.write_text('#!/bin/sh\nprintf "%s\\n" "$C10Z_OUT_DIR" "$C10Z_GO_RECORD"\nexit 2\n')
            python.chmod(0o755)
            go = str(root / "supplied-go.json")
            result = real_subprocess.run(["bash", str(shell), "0"], capture_output=True, text=True,
                env=dict(os.environ, C10Z_OUT_DIR="relative/attempt", C10Z_GO_RECORD=go))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout.splitlines(), [str(root / "relative/attempt"), go])
            self.assertFalse((root / "relative").exists())


# Keep the reviewer's 60 tests plus the three demos and nine targeted fix tests.
_fix1_suite = lambda: unittest.TestSuite([
    unittest.defaultTestLoader.loadTestsFromTestCase(SpecTests),
    unittest.defaultTestLoader.loadTestsFromTestCase(Fix1Tests)])

class Fix2Tests(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms")
        self.R = importlib.import_module("c10z_astra_read")
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for patcher in (mock.patch.object(self.D, "ROOT", self.root), mock.patch.dict(os.environ),
                        mock.patch.object(self.D,"benchmark_module",side_effect=lambda:importlib.import_module("c10z_astra_benchmark"),create=True)):
            patcher.start(); self.addCleanup(patcher.stop)
        os.environ.pop("C10Z_RESIDENT", None)
        os.environ.pop("C10Z_GO_RECORD", None)

    def test_fix2_child_receives_parent_resolved_absolute_outdir(self):
        """Prereg :137, :204; fix2 item 1/O02: direct stage_call resolves the child path before cwd changes."""
        D = self.D; out = self.root / "attempt"
        relative = Path(os.path.relpath(out, Path.cwd()))
        bench,binding=_bench_tree(self.root)
        go = self.root / "go.json"; go.write_text(json.dumps(_go_record(binding)))
        os.environ["C10Z_BENCHMARK_RECORD"]=str(bench)
        os.environ.update(C10Z_OUT_DIR=str(relative), C10Z_GO_RECORD=str(go))
        captured = []
        def launch(*args, **kwargs):
            captured.append(kwargs)
            D.write_json(out / "run.json", {"launch": json.loads(kwargs["env"]["C10Z_LAUNCH"])})
            return Child()
        with mock.patch.object(D, "subprocess", _types.SimpleNamespace(Popen=launch, DEVNULL=None, STDOUT=None)), mock.patch.object(
                D, "wait_stage", return_value=0):
            self.assertEqual(D.stage_call(0, relative), 0)
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0]["env"]["C10Z_OUT_DIR"], str(out.resolve()))
        self.assertTrue(Path(captured[0]["env"]["C10Z_OUT_DIR"]).is_absolute())
        self.assertEqual(captured[0]["cwd"], D.ROOT)

    def test_fix2_failed_resident_detection_closes_halt_and_keeps_passes(self):
        """Prereg :267, :323; D-C10z-fix1 (3): all wait_stage failed-resident detections publish a durable HALT."""
        D, R = self.D, self.R
        for process in (1, 2):
            for failure in ("stale", "attempt", "pid", "missing", "exit"):
                with self.subTest(process=process, failure=failure):
                    out = self.root / (str(process) + failure); first = fixture(stage=2 if process == 2 else 1)
                    _attempt_dir(D, out, first, {"closed": process == 2, "completed": first["stage_completed"]})
                    target = out; record = first
                    if process == 2:
                        target = out / "process2"; record = fixture(); second_process(record)
                        _attempt_dir(D, target, record, {"process": 2, "pid": record["pid"], "completed": 1, "closed": False})
                        (target / "pass_p1.json").rename(target / "pass_p2.json")
                    run = D.load_json(target / "run.json"); run.update(closed=False, requested=2)
                    D.write_json(target / "run.json", run, replace=True)
                    (target / "logs").mkdir()
                    heartbeat = {"attempt_id": run["attempt_id"], "pid": run["pid"], "at": 100.}
                    if failure == "stale": heartbeat["at"] = 84.
                    if failure == "attempt": heartbeat["attempt_id"] = "different-attempt"
                    if failure == "pid": heartbeat["pid"] += 1
                    if failure != "missing": D.write_json(target / "logs/heartbeat.json", heartbeat)
                    before = {p: p.read_bytes() for p in out.rglob("pass_p*.json")}
                    ticks = iter((100., 116.)) if failure == "missing" else None
                    clock = (lambda: next(ticks)) if ticks else (lambda: 100.)
                    with self.assertRaises(R.Halt) as halted:
                        D.wait_stage(target, 2, child=Child() if failure == "exit" else None,
                            clock=clock, pause=lambda _: self.fail("failed resident was still being awaited"))
                    self.assertEqual(halted.exception.code, "HALTED-V12")
                    terminal = D.load_json(target / "run.json")
                    self.assertIs(terminal["closed"], True)
                    self.assertEqual(terminal["halt"]["code"], "HALTED-V12")
                    value = D.load_json(target / ("halt_p%d.json" % process))
                    self.assertEqual(value["halt"]["code"], "HALTED-V12")
                    self.assertEqual(value["observations"], record)
                    self.assertEqual(D.load_json(self.root / "architecture_profile/c10z_astra_halt_diagnostic.json"), value)
                    self.assertEqual(before, {p: p.read_bytes() for p in out.rglob("pass_p*.json")})
                    got = R.read_directory(out)
                    self.assertEqual(got["label"], "HALTED-V12"); self.assertFalse(got["scientific_verdict"])
                    self.assertEqual(got["observations"], [first, record] if process == 2 else [record])

    def test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields(self):
        """Prereg :267, :323; item 2/H10/H11: a resumed resident sees the parent's halt at its next terminal check."""
        D, R = self.D, self.R; out = self.root / "attempt"; record = fixture()
        _attempt_dir(D, out, record, {}); (out / "logs").mkdir()
        before = (out / "pass_p1.json").read_bytes(); events = []; sessions = []
        owner = self; real_budget = D.Budget
        class SessionStub:
            def __init__(self, path, process, budget, input_dir):
                self.process = process; self.budget = budget; sessions.append(self)
                self.recipes = {"A": {"completed": True}}; self.checks = {"Z0": {"ok": True}}
                self.memory = [{"rss_bytes": 10}]; self.restores = [{"where": "before stall", "ok": True}]
                self.budget.history.append({"components_s": {"check": 1.}})
            def stage0(self):
                events.append("stage0"); run = D.load_json(out / "run.json")
                D.write_json(out / "logs/heartbeat.json", {"attempt_id": run["attempt_id"], "pid": run["pid"], "at": 84.})
                with owner.assertRaises(R.Halt) as halted:
                    D.wait_stage(out, 0, clock=lambda: 100., pause=lambda _: owner.fail("stalled resident was awaited"))
                events.append(("parent halt", halted.exception.code))
            def stage1(self):
                events.append("stage1"); raise R.Halt("HALTED-V5", "resident continued after parent halt")
            def stage2(self): events.append("stage2"); raise AssertionError("unexpected stage2")
            def restore(self): events.append("restore")
            def verify_restore(self, where): events.append(("verify", where))
            def close(self): events.append("close")
        class Event:
            def set(self): pass
        class Thread:
            def __init__(self, target, daemon): pass
            def start(self): pass
        def submit(_):
            run = D.load_json(out / "run.json"); run["requested"] = 1
            D.write_json(out / "run.json", run, replace=True)
        launch = _launch(attempt_id=record["attempt_id"],stage2=60.,stage3=None)
        with mock.patch.object(D, "Session", SessionStub), mock.patch.object(
                D, "Budget", lambda start, stage01, stage2, stage3, process: real_budget(start, stage01, stage2, stage3, process=process, clock=lambda: 100.)), mock.patch.object(
                D, "time", _types.SimpleNamespace(monotonic=lambda: 100., sleep=submit)), mock.patch.object(
                D, "threading", _types.SimpleNamespace(Event=Event, Thread=Thread, RLock=__import__("threading").RLock)):
            rc = _resident_runtime(out, 1, launch, start=100.)
        self.assertEqual(rc, 2); self.assertIn(("parent halt", "HALTED-V12"), events)
        self.assertNotIn("stage1", events); self.assertNotIn("stage2", events)
        self.assertIn("restore", events); self.assertIn(("verify", "exception close"), events)
        session = sessions[0]; halt = D.load_json(out / "halt_p1.json")
        for key, expected in (("recipes", session.recipes), ("checks", session.checks), ("memory", session.memory),
                              ("restores", session.restores), ("budget_history", session.budget.history)):
            self.assertEqual(halt[key], expected, key)
        self.assertEqual(halt["halt"]["code"], "HALTED-V12")
        self.assertEqual(D.load_json(self.root / "architecture_profile/c10z_astra_halt_diagnostic.json"), halt)
        self.assertEqual((out / "pass_p1.json").read_bytes(), before)
        self.assertEqual(R.read_directory(out)["label"], "HALTED-V12")

    def test_fix2_go_nonfinite_constants_and_overflow_refused(self):
        """Prereg V6 :219, §6 :341–344; G11: nested NaN/Infinity and overflowing JSON numbers are refused without writes."""
        D = self.D; go = self.root / "go.json"
        for token in ("NaN", "Infinity", "-Infinity", "1e999", "-1e999"):
            with self.subTest(token=token):
                raw = json.dumps(_go_record())[:-1] + ', "metadata": {"nested": [' + token + ']}}'
                go.write_text(raw); out = self.root / token
                with mock.patch.dict(os.environ, {"C10Z_OUT_DIR": str(out), "C10Z_GO_RECORD": str(go)}), mock.patch.object(
                        D.subprocess, "Popen", side_effect=AssertionError("nonfinite go launched")), mock.patch.object(
                        sys, "argv", ["c10z_astra_arms.py", "0"]), redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(D.main(), 2)
                self.assertIn("HALTED-V6", err.getvalue()); self.assertFalse(out.exists())

    def test_fix2_session_record_absent_ceiling_matches_reader_omissions(self):
        """Prereg :196, :265–267; B3d: the actual Session.record producer agrees with the independent reader."""
        D, R = self.D, self.R
        for stage in (1, 2):
            with self.subTest(stage=stage):
                out = self.root / str(stage); r = fixture(stage=stage); _attempt_dir(D, out, r, {})
                r["budget"]["ceilings"]["stage%d" % (stage + 1)] = None
                seal_schedule(r)
                s = D.Session.__new__(D.Session)
                for key in ("recipes", "fingerprint", "manifest", "H_pristine", "checks", "restores", "memory", "attempt_id", "process"):
                    setattr(s, key, copy.deepcopy(r[key]))
                s.recipes["A"]["arms"][A7]["realised_layer_delta_norms"] = {"4": 1.}
                s.recipes["Z"]["arms"][A7]["write"]["geometry"] = {"layer_delta_norms": {"4": .4}}
                s.out = out; s.initial_sources = r["fingerprint"]["start"]
                s.budget = _types.SimpleNamespace(durations=r["budget"]["ceilings"], origins=r["budget"]["origins"], history=r["budget"]["history"])
                with mock.patch.object(D, "source_hashes", return_value=s.initial_sources): produced = s.record(stage)
                expected = {"status": "NOT-RUN", "reason": "ABSENT-CEILING"}
                if stage == 1:
                    self.assertEqual(produced["omissions"]["G0"], expected)
                    self.assertEqual(produced["omissions"]["Z-band"], expected)
                self.assertEqual(produced["omissions"]["process2"], expected)
                got = R.read_process(produced)
                self.assertEqual(got["label"], "PARTIAL-STAGE1" if stage == 1 else "PARTIAL-SINGLE-PROCESS", got)
                self.assertIsNone(got["next_stage"])

    def test_fix2_disqualified_missing_ceiling_is_k1_not_absent(self):
        """Prereg :265, :272; B3g: a qualified PARTIAL/LEAD stops for K1 even without an expansion budget."""
        R = self.R
        for n, base in ((26, "PARTIAL"), (30, "LEAD")):
            with self.subTest(base=base):
                r = fixture(n=n, ratio=.6); ceilings = r["budget"]["ceilings"]; ceilings["stage2"] = None
                z, a = r["recipes"]["Z"]["arms"][A7], r["recipes"]["A"]["arms"][A7]
                decision = R.classify_candidate(z, a, R.side_gates(z, a), 1, ceilings=ceilings)
                self.assertEqual(decision["label"], base + "-LARGE-WRITE-STAGE1")
                self.assertIsNone(decision["next_stage"])
                self.assertEqual(R.stage_omissions(1, 1, None, ceilings, decision), {
                    k: {"status": "NOT-RUN", "reason": "K1"} for k in ("G0", "Z-band", "process2")})

    def test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary(self):
        """Prereg :147; A32: the real Z0 function permits sigma=.125 and halts above it before any reader."""
        import torch
        D, R = self.D, self.R; s = D.Session.__new__(D.Session)
        s.H = _types.SimpleNamespace(DEV="cpu", model=lambda *a, **k: _types.SimpleNamespace(
            logits=torch.tensor([[[1., 0.]]], dtype=torch.float64)))
        s.budget = D.Budget(0., C01_FIX, None, None, clock=lambda: 0.)
        s.lead_rows = lambda batch, obs: ([obs["leads"].tolist()], None)
        batch = {"target_ids": [[0]], "prompt_ids": [[1]], "requirements": [{"fact": 0, "view": 0, "q": 0}]}
        at = s.z0(batch, {"leads": torch.tensor([.875], dtype=torch.float64)})
        self.assertEqual(at["sigma_shape"], .125); self.assertEqual(at["tau_shape"], .25)
        with self.assertRaises(R.Halt) as halted:
            s.z0(batch, {"leads": torch.tensor([.874], dtype=torch.float64)})
        self.assertEqual(halted.exception.code, "HALTED-V5")

def _fix2_suite():
    suite = _fix1_suite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Fix2Tests))
    return suite

def _budget(start, c01, c2, c3, process, clock):
    """Exercise the old behavior before changing the launch-input signature."""
    import inspect
    D = importlib.import_module("c10z_astra_arms")
    if "stage01" in inspect.signature(D.Budget).parameters:
        return D.Budget(start, c01, c2, c3, process=process, clock=clock)
    value = D.Budget(start, c2, c3, process=process, clock=clock)
    value.durations["stage01"] = c01
    return value


class IdleGapTests(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms")
        self.R = importlib.import_module("c10z_astra_read")

    def stage1(self, return_at, process=1, budget=None, clock=None):
        clock = [0.] if clock is None else clock
        budget = _budget(0., 7200., 200., 7460., process, lambda: clock[0]) if budget is None else budget
        budget.future_stage2_s = 100.
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        stub = _types.SimpleNamespace(budget=budget, process=process, out=Path(tmp.name), timings={})
        stub.remaining_validation = _types.MethodType(self.D.Session.remaining_validation, stub)
        stub.run_recipe = lambda *a: clock.__setitem__(0, return_at)
        stub.complete_recipe_readouts = lambda *a: None
        stub.write_checks = lambda: None
        stub.record = lambda stage: {}
        with mock.patch.object(self.R, "read_process", return_value={"scientific_verdict": True, "next_stage": 2, "label": "PARTIAL"}):
            self.D.Session.stage1(stub)
        return budget, clock

    def test_i_idle_expiry(self):
        b, clock = self.stage1(7190.)
        clock[0] = 7201.
        with self.assertRaisesRegex(self.R.Halt, "HALTED-BUDGET: elapsed deadline expired", msg="idle gap escaped the stage01 deadline"):
            b.check()

    def test_ii_late_entry(self):
        b, clock = self.stage1(7199.)
        clock[0] = 7201.
        with self.assertRaisesRegex(self.R.Halt, "HALTED-BUDGET: stage 0-1 deadline expired before stage-2 entry", msg="late stage2 entry was accepted"):
            b.enter(2)
        self.assertNotIn("stage2", b.origins)

    def test_iii_deadline_samples(self):
        b, clock = self.stage1(7190.)
        for t in (7190., 7191., 7195.):
            clock[0] = t
            self.assertIsNotNone(b.deadline(), "stage1 return or idle had no active deadline")
            self.assertEqual(b.deadline(), 7200.)
        b.enter(2)
        self.assertEqual(b.deadline(), 7395.)

    def test_iv_process2_envelope(self):
        b, clock = self.stage1(7190., process=2)
        self.assertEqual(b.deadline(), 7200., "process2 fell back to stage3 during idle")
        clock[0] = 7195.; b.enter(2)
        self.assertEqual(b.deadline(), 7395.)
        self.assertNotEqual(b.deadline(), 7460.)

    def test_v_complete01_only_enter(self):
        tree = ast.parse((HERE / "c10z_astra_arms.py").read_text())
        found = []
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for fun in (n for n in cls.body if isinstance(n, ast.FunctionDef)):
                if any(isinstance(n, ast.Attribute) and n.attr == "complete01" for n in ast.walk(fun)):
                    found.append(cls.name + "." + fun.name)
        self.assertEqual(found, ["Budget.enter"], "complete01 referenced outside the locked stage2 transition")

    def test_vi_mutation_deadlines(self):
        clock = [0.]; b = _budget(0., 7200., 200., 7460., 1, lambda: clock[0]); observed = []
        class RecordingSet(set):
            def add(self, value):
                super().add(value); observed.append(b.deadline())
            def discard(self, value):
                super().discard(value); observed.append(b.deadline())
        b.active = RecordingSet(b.active)
        self.stage1(7190., budget=b, clock=clock)
        observed.append(b.deadline()); clock[0] = 7195.; observed.append(b.deadline()); b.enter(2)
        self.assertNotIn(None, observed, "an active-set mutation exposed no deadline")

    def test_vii_entry_invariant(self):
        for e in (0., 1., 7190., 7199.999):
            with self.subTest(entry=e):
                b, clock = self.stage1(e, process=2)
                b.enter(2)
                self.assertEqual(b.deadline(), e + 200.)
                self.assertLess(b.deadline(), 7460.)

    def test_viii_single_timestamp(self):
        calls = []
        def crossing():
            calls.append(1); return 7200. if len(calls) == 1 else 7199.5
        b = _budget(0., 7200., 200., 7460., 1, crossing)
        with self.assertRaisesRegex(self.R.Halt, "HALTED-BUDGET: stage 0-1 deadline expired before stage-2 entry", msg="entry decision did not use its first timestamp"):
            b.enter(2)
        self.assertEqual(len(calls), 1)
        b = _budget(0., 7200., 200., 7460., 1, lambda: 7199.999); b.enter(2)
        self.assertEqual(b.origins["stage2"], 7199.999)

    def test_ix_transition_lock(self):
        import threading
        inside, release, t_attempt, t_done = (threading.Event() for _ in range(4))
        result, errors, calls = [], [], []
        def clock():
            calls.append(1)
            if len(calls) == 1:
                inside.set()
                if not release.wait(5.): raise AssertionError("entry clock was not released")
            return 100.
        b = _budget(0., 7200., 200., 7460., 1, clock)
        class Lock:
            def __init__(self): self.real = threading.RLock()
            def __enter__(self):
                if threading.current_thread().name == "deadline-T": t_attempt.set()
                self.real.acquire(); return self
            def __exit__(self, *exc): self.real.release()
        b.lock = Lock()
        def entry():
            try: b.enter(2)
            except BaseException as exc: errors.append(exc)
        def observe():
            try: result.append(b.deadline())
            except BaseException as exc: errors.append(exc)
            finally: t_done.set()
        E = threading.Thread(target=entry, name="entry-E", daemon=True)
        T = threading.Thread(target=observe, name="deadline-T", daemon=True)
        try:
            E.start(); self.assertTrue(inside.wait(5.), "entry did not reach the transition")
            T.start()
            import time as real_time
            end = real_time.perf_counter() + 5.
            while not (t_attempt.is_set() or t_done.is_set()) and real_time.perf_counter() < end:
                t_done.wait(.01)
            self.assertTrue(t_attempt.is_set() or t_done.is_set(), "deadline thread was never scheduled")
            T.join(.2)
            self.assertTrue(T.is_alive(), "deadline() returned while enter(2) held the transition lock")
        finally:
            release.set(); E.join(5.)
            if T.ident is not None: T.join(5.)
        self.assertFalse(E.is_alive()); self.assertFalse(T.is_alive()); self.assertEqual(errors, [])
        self.assertEqual(result, [300.])


class BudgetBoundTests(unittest.TestCase):
    def test_huge_integer_refusal(self):
        D = importlib.import_module("c10z_astra_arms"); R = importlib.import_module("c10z_astra_read")
        with self.assertRaisesRegex(R.Halt, "HALTED-BUDGET: invalid stage01 ceiling"):
            D.Budget(0., 10**400, 12600., 20460., clock=lambda: 0.)

    def test_c01_neighbors(self):
        D = importlib.import_module("c10z_astra_arms"); R = importlib.import_module("c10z_astra_read")
        for value in (7199.999, 10800.001, math.nan, math.inf, -math.inf, None, True):
            with self.subTest(refused=value), self.assertRaisesRegex(R.Halt, "HALTED-BUDGET: invalid stage01 ceiling"):
                D.Budget(0., value, 12600., 20460., clock=lambda: 0.)
        for value in (7200., 7200.001, 10799.999, 10800.):
            with self.subTest(accepted=value):
                self.assertEqual(D.Budget(0., value, 12600., 20460., clock=lambda: 0.).durations["stage01"], value)


def _bench_tree(root):
    import shutil
    import c10z_astra_benchmark_selftest as BT
    B = BT.benchmark_module()
    paths = ("experiments/track_c/c10z_astra_benchmark.py", "experiments/track_c/c10z_astra_arms.py",
             "experiments/track_c/c10z_astra_read.py", "experiments/track_c/c10e_bandknob.py",
             "configs/hparams/qwen25_3b_memit_hparams.json", "tools/engine_fingerprint.py",
             "memit_dry_run/memit/memit/memit_main.py")
    for rel in paths:
        dest = root / rel; dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dest)
    record = BT.fixture_record(root=root)
    B.validate_record(record)
    path = root / "results/c10z_astra_benchmark/20261007T000000Z/benchmark.json"
    B.write_record(path, record)
    c = B.ceilings(record)
    binding = {"benchmark_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "benchmark_script_sha256": record["env"]["script_sha256"],
               "ceilings": {"stage01": c["C01"], "stage2": c["C2"], "stage3": c["C3"]}}
    return path, binding


def _selected_launch(path, binding):
    record = json.loads(path.read_bytes())
    return _launch(stage01=binding["ceilings"]["stage01"], stage2=binding["ceilings"]["stage2"],
                   stage3=binding["ceilings"]["stage3"], go=_go_record(binding), benchmark={
                       "path": str(path), "sha256": binding["benchmark_sha256"],
                       "script_sha256": binding["benchmark_script_sha256"],
                       "sources": record["env"]["sources"],
                       "env": {k: record["env"][k] for k in ("python", "machine", "platform", "torch", "transformers")},
                       "ceilings": binding["ceilings"]})


class LaunchBindingTests(unittest.TestCase):
    def setUp(self):
        import c10z_astra_benchmark_selftest as BT
        self.D = importlib.import_module("c10z_astra_arms"); self.R = importlib.import_module("c10z_astra_read")
        self.B = BT.benchmark_module()
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root = Path(self.tmp.name)
        self.path, self.binding = _bench_tree(self.root)
        self.go_path = self.root / "go.json"; self.out = self.root / "attempt"
        self.record = json.loads(self.path.read_bytes()); self.launched = []
        for p in (mock.patch.object(self.D, "ROOT", self.root),
                  mock.patch.object(self.D, "benchmark_module", return_value=self.B, create=True),
                  mock.patch.dict(os.environ, {}, clear=True),
                  mock.patch.object(self.D, "wait_stage", return_value=0),
                  mock.patch.object(self.D, "subprocess", _types.SimpleNamespace(
                      Popen=self.child, DEVNULL=None, STDOUT=None)),
                  mock.patch.object(self.D, "resident", side_effect=lambda *a, **kw: self.launched.append("p2") or 0)):
            p.start(); self.addCleanup(p.stop)
        self.save()
        os.environ.update(C10Z_GO_RECORD=str(self.go_path), C10Z_BENCHMARK_RECORD=str(self.path))

    def child(self, *a, **kw):
        launch = json.loads(kw["env"]["C10Z_LAUNCH"]); self.launched.append(launch)
        self.D.write_json(self.out / "run.json", {"launch": launch}); return Child()

    def save(self, derived=None):
        if derived is not None:
            self.record["derived"] = derived
            self.binding["ceilings"] = {k: derived[c] for k, c in (("stage01", "C01"), ("stage2", "C2"), ("stage3", "C3"))}
        self.B.write_record(self.path, self.record)
        self.binding["benchmark_sha256"] = hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.go = _go_record(self.binding); self.go_path.write_text(json.dumps(self.go))

    def refuse(self, code, detail, stage=0):
        before = {str(p.relative_to(self.out)): p.read_bytes() for p in self.out.rglob("*") if p.is_file()} if self.out.exists() else {}
        with self.assertRaisesRegex(self.R.Halt, code + ": .*" + __import__("re").escape(detail)):
            self.D.stage_call(stage, self.out)
        after = {str(p.relative_to(self.out)): p.read_bytes() for p in self.out.rglob("*") if p.is_file()} if self.out.exists() else {}
        self.assertEqual(after, before, "pre-attempt refusal wrote files")
        self.assertEqual(self.launched, [])
        if stage == 3: self.assertFalse((self.out / "process2").exists())

    def stage3_fixture(self):
        r = fixture(n=22, stage=2); r["budget"]["ceilings"] = dict(self.binding["ceilings"]); seal_schedule(r)
        launch = _selected_launch(self.path, self.binding)
        _attempt_dir(self.D, self.out, r, {"launch": launch})
        got = self.R.read_directory(self.out)
        self.assertTrue(got["scientific_verdict"]); self.assertEqual(got["next_stage"], 3)
        return launch

    def test_record_required(self):
        os.environ.pop("C10Z_BENCHMARK_RECORD"); self.refuse("HALTED-V12", "C10Z_BENCHMARK_RECORD is required")

    def test_record_absolute(self):
        os.environ["C10Z_BENCHMARK_RECORD"] = "relative/benchmark.json"; self.refuse("HALTED-V12", "C10Z_BENCHMARK_RECORD must be absolute")

    def test_record_outside(self):
        os.environ["C10Z_BENCHMARK_RECORD"] = str(self.root / "results/c10z_astra_benchmark_extra/T/benchmark.json")
        self.refuse("HALTED-V12", "benchmark record outside results/c10z_astra_benchmark")

    def test_record_unreadable(self):
        self.path.unlink(); self.refuse("HALTED-V12", "benchmark record unreadable")

    def test_record_selection(self):
        self.path.write_bytes(self.path.read_bytes() + b" "); self.refuse("HALTED-V12", "benchmark record differs from go selection")

    def test_record_nonstrict(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token):
                self.path.write_text('{"invalid":' + token + '}')
                self.go["benchmark_sha256"] = hashlib.sha256(self.path.read_bytes()).hexdigest(); self.go_path.write_text(json.dumps(self.go))
                self.refuse("HALTED-V12", "benchmark record is not strict JSON")

    def test_script(self):
        (self.root / "experiments/track_c/c10z_astra_benchmark.py").write_text("changed")
        self.refuse("HALTED-V12", "benchmark script changed")

    def test_sources(self):
        (self.root / "experiments/track_c/c10z_astra_arms.py").write_text("changed")
        self.refuse("HALTED-V12", "benchmark source identity changed: experiments/track_c/c10z_astra_arms.py")

    def test_environment(self):
        env = self.B.environment_identity(); env["python"] += "+changed"
        with mock.patch.object(self.B, "environment_identity", return_value=env): self.refuse("HALTED-V12", "benchmark environment changed: python")

    def test_record_invalid(self):
        self.record["phases"]["probe_forward"]["p95"] += .1; self.save()
        self.refuse("HALTED-V12", "benchmark record invalid:")

    def test_record_optional_status(self):
        base = copy.deepcopy(self.record)
        for phase in ("batch_forward", "eval_A7", "svd"):
            for value in ([], {}):
                with self.subTest(phase=phase, value=value):
                    self.record = copy.deepcopy(base)
                    self.record["phases"][phase]["status"] = value; self.save()
                    self.refuse("HALTED-V12", "benchmark record invalid:")

    def test_refused(self):
        with mock.patch.object(self.B, "ceilings", return_value={"source": "REFUSED", "reason": "test refusal"}):
            self.refuse("HALTED-BUDGET", "benchmark refused: test refusal")

    def test_derived(self):
        self.record["derived"]["t_star"] += .1; self.save()
        self.refuse("HALTED-V12", "benchmark derived disagrees with ceilings()")

    def synthetic(self, c01=7800., c2=12600., stop=False):
        c = dict(self.record["derived"], C01=c01, C2=c2, C3=c01+c2+60., stop=stop,
                 nominal_supremum_s=2*(c01+c2), worst_case_s=2*(c01+c2), c3_sum_s=2*(c01+c2)+60.)
        self.save(c); return c

    def test_stop(self):
        c = self.synthetic(c01=9000., stop=True)
        with mock.patch.object(self.B, "ceilings", return_value=c): self.refuse("HALTED-BUDGET", "benchmark STOP")

    def test_c01(self):
        for value, accepted in ((7199.999, False), (7200., True), (10800., True), (10800.001, False)):
            with self.subTest(value=value):
                c = self.synthetic(c01=value)
                with mock.patch.object(self.B, "ceilings", return_value=c):
                    if accepted:
                        self.assertEqual(self.D.stage_call(0, self.out), 0)
                        self.assertEqual(self.launched[-1]["stage01"], value)
                        __import__("shutil").rmtree(self.out); self.launched.clear()
                    else: self.refuse("HALTED-BUDGET", "C01 outside [7200, 10800]")

    def test_total(self):
        for c2, accepted in ((17099.9995, True), (17100., True), (17100.001, False)):
            with self.subTest(c2=c2):
                c = self.synthetic(c01=10800., c2=c2)
                with mock.patch.object(self.B, "ceilings", return_value=c):
                    if accepted:
                        self.assertEqual(self.D.stage_call(0, self.out), 0)
                        __import__("shutil").rmtree(self.out); self.launched.clear()
                    else: self.refuse("HALTED-BUDGET", "nominal total above 55,800 s")

    def test_go_ceilings(self):
        self.go["ceilings"]["stage01"] += 300.; self.go_path.write_text(json.dumps(self.go))
        self.refuse("HALTED-V12", "go ceilings differ from ceilings()")

    def test_go_huge_integer_ceiling_refusal(self):
        self.go["ceilings"]["stage01"] = 10**400; self.go_path.write_text(json.dumps(self.go))
        self.refuse("HALTED-V12", "go ceilings differ from ceilings()")

    def test_stage2_override(self):
        os.environ["C10Z_STAGE2_CEILING_S"] = "12601"; self.refuse("HALTED-BUDGET", "C10Z_STAGE2_CEILING_S differs from C2")

    def test_stage3_override(self):
        os.environ["C10Z_STAGE3_CEILING_S"] = "20461"; self.refuse("HALTED-BUDGET", "C10Z_STAGE3_CEILING_S differs from C3")

    def test_go_fields(self):
        cases = []
        for key in ("benchmark_sha256", "benchmark_script_sha256", "ceilings"):
            go = _go_record(self.binding); go.pop(key); cases.append(go)
        for key in ("benchmark_sha256", "benchmark_script_sha256"):
            for bad in (None, 4, "a"*63, "A"*64):
                go = _go_record(self.binding); go[key] = bad; cases.append(go)
        for ceilings in ({"stage01": 7800., "stage2": 12600.}, {**self.binding["ceilings"], "extra": 1},
                         {**self.binding["ceilings"], "stage01": True}, {**self.binding["ceilings"], "stage2": math.nan}, []):
            go = _go_record(self.binding); go["ceilings"] = ceilings; cases.append(go)
        for i, go in enumerate(cases):
            with self.subTest(case=i):
                self.go_path.write_text(json.dumps(go))
                self.refuse("HALTED-V12", "go record requires benchmark_sha256, benchmark_script_sha256 and ceilings")

    def test_success_roundtrip(self):
        self.assertEqual(self.D.stage_call(0, self.out), 0)
        launch = self.launched[-1]; self.assertEqual(launch["stage01"], 7800.)
        self.assertIs(launch["telemetry"], False); self.assertIsNone(launch["telemetry_inertness"])
        self.assertEqual(launch["stage2"], None); self.assertEqual(launch["stage3"], None)
        self.assertEqual(launch["benchmark"], _selected_launch(self.path, self.binding)["benchmark"])
        self.assertEqual(self.D.load_json(self.out / "run.json")["launch"], json.loads(json.dumps(launch, allow_nan=False, sort_keys=True)))
        self.assertEqual(self.D.go_record(os.environ)[0], json.loads(json.dumps(self.go, allow_nan=False, sort_keys=True)))
        self.assertFalse((self.out / "telemetry").exists())

    def test_substitution(self):
        alternate = self.path.parent.parent / "alternate/benchmark.json"
        self.B.write_record(alternate, self.record); os.environ["C10Z_BENCHMARK_RECORD"] = str(alternate)
        alternate.write_bytes(alternate.read_bytes() + b"\n")
        self.B.validate_record(json.loads(alternate.read_bytes()))
        self.refuse("HALTED-V12", "benchmark record differs from go selection")
        os.environ["C10Z_BENCHMARK_RECORD"] = str(self.path)
        self.record["phases"]["probe_forward"]["seconds"][0] += .001
        self.record["derived"] = self.B.ceilings(self.record)
        self.B.write_record(self.path, self.record)
        self.refuse("HALTED-V12", "benchmark record differs from go selection")

    def drift(self, what):
        self.stage3_fixture()
        if what == "record": self.path.write_bytes(self.path.read_bytes() + b" ")
        else: (self.root / what).write_text("identity drift")
        self.refuse("HALTED-V12", "launch binding changed since stage 0:", stage=3)

    def test_stage3_record_drift(self): self.drift("record")
    def test_stage3_script_drift(self): self.drift("experiments/track_c/c10z_astra_benchmark.py")
    def test_stage3_source_drift(self): self.drift("experiments/track_c/c10z_astra_arms.py")

    def test_stage3_environment_drift(self):
        self.stage3_fixture(); env = self.B.environment_identity(); env["torch"] += "+drift"
        with mock.patch.object(self.B, "environment_identity", return_value=env):
            self.refuse("HALTED-V12", "launch binding changed since stage 0:", stage=3)

    def test_stage3_switch(self):
        self.stage3_fixture()
        for value in ("0", "true", "", " 1"):
            with self.subTest(value=value):
                os.environ["C10Z_TELEMETRY"] = value
                self.refuse("HALTED-V12", "C10Z_TELEMETRY must be absent or 1", stage=3)
        os.environ["C10Z_TELEMETRY"] = "1"
        self.refuse("HALTED-V12", "C10Z_TELEMETRY differs from launch", stage=3)

    def inertness_record(self):
        import shutil
        for rel in ("experiments/track_c/c10z_astra_telemetry_check.py",):
            dst = self.root / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, dst)
        paths = ("experiments/track_c/c10z_astra_arms.py", "experiments/track_c/c10z_astra_read.py",
                 "experiments/track_c/c10z_astra_telemetry_check.py", "experiments/track_c/c10z_astra_benchmark.py",
                 "experiments/track_c/c10e_bandknob.py", "configs/hparams/qwen25_3b_memit_hparams.json",
                 "memit_dry_run/memit/memit/memit_main.py")
        record = {"schema": "c10z_astra_telemetry_inertness/v1", "decision_id": "D-C10r-rulings-11", "device": "mps",
                  "verdict": "INERT", "control_equal": True, "telemetry_equal": True, "weights_unchanged": True,
                  "probe_forwards": self.B.expected_probe_forwards(self.record), "lens_forwards": 72,
                  "sources": {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest() for p in paths},
                  "env": {**self.B.environment_identity(), "model_rev": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"},
                  "started_at": "2026-10-07T00:00:00+00:00", "finished_at": "2026-10-07T00:01:00+00:00"}
        path = self.root / "results/c10z_astra_telemetry_inertness/T/inertness.json"
        self.B.write_record(path, record)
        os.environ.update(C10Z_TELEMETRY="1", C10Z_TELEMETRY_INERTNESS=str(path))
        return path, record

    def test_inertness_required(self):
        os.environ["C10Z_TELEMETRY"] = "1"
        self.refuse("HALTED-V12", "telemetry requires an INERT inertness record:")

    def test_inertness_path(self):
        self.inertness_record(); os.environ["C10Z_TELEMETRY_INERTNESS"] = str(self.root / "inertness.json")
        self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: path")

    def test_inertness_json(self):
        path, _ = self.inertness_record(); path.write_text('{"nan": NaN}')
        self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: strict JSON")

    def test_inertness_verdict(self):
        path, record = self.inertness_record()
        for value in ("NOT-INERT", "NONDETERMINISTIC-BASELINE"):
            with self.subTest(verdict=value):
                record["verdict"] = value; self.B.write_record(path, record)
                self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: evidence")

    def test_inertness_sources(self):
        path, record = self.inertness_record(); record["sources"]["experiments/track_c/c10z_astra_arms.py"] = "0"*64
        self.B.write_record(path, record); self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: sources")

    def test_inertness_environment(self):
        path, record = self.inertness_record(); record["env"]["python"] += "changed"
        self.B.write_record(path, record); self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: environment")

    def test_inertness_schema(self):
        path, valid = self.inertness_record()
        for key in tuple(valid):
            with self.subTest(missing=key):
                bad = copy.deepcopy(valid); bad.pop(key); self.B.write_record(path, bad)
                self.refuse("HALTED-V12", "telemetry requires an INERT inertness record:")
        for key in ("control_equal", "telemetry_equal", "weights_unchanged"):
            for value in (False, 1, None):
                with self.subTest(key=key, value=value):
                    bad = copy.deepcopy(valid); bad[key] = value; self.B.write_record(path, bad)
                    self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: evidence")

    def test_inertness_counts(self):
        path, valid = self.inertness_record()
        for key in ("probe_forwards", "lens_forwards"):
            for value in (0, 1, True, valid[key]-1, valid[key]+1):
                with self.subTest(key=key, value=value):
                    bad = copy.deepcopy(valid); bad[key] = value; self.B.write_record(path, bad)
                    self.refuse("HALTED-V12", "telemetry requires an INERT inertness record: counts")

    def test_inertness_success(self):
        path, record = self.inertness_record(); self.assertEqual(self.D.stage_call(0, self.out), 0)
        self.assertIs(self.launched[-1]["telemetry"], True)
        self.assertEqual(self.launched[-1]["telemetry_inertness"], {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        self.assertEqual(json.loads(path.read_bytes()), json.loads(json.dumps(record, sort_keys=True, allow_nan=False)))

    def test_stage3_inertness_drift(self):
        path, _ = self.inertness_record(); launch = self.stage3_fixture()
        launch.update(telemetry=True, telemetry_inertness={"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        run = self.D.load_json(self.out / "run.json"); run["launch"] = launch; self.D.write_json(self.out / "run.json", run, replace=True)
        path.write_bytes(path.read_bytes() + b" ")
        self.refuse("HALTED-V12", "launch binding changed since stage 0:", stage=3)


def _switch_test(value):
    def test(self):
        os.environ["C10Z_TELEMETRY"] = value
        self.refuse("HALTED-V12", "C10Z_TELEMETRY must be absent or 1")
    return test
for _suffix, _value in (("zero", "0"), ("true", "true"), ("empty", ""), ("space", " 1")):
    setattr(LaunchBindingTests, "test_switch_" + _suffix, _switch_test(_value))


class ReaderBindingTests(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms"); self.R = importlib.import_module("c10z_astra_read")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root = Path(self.tmp.name)

    def rejected(self, reading, detail):
        self.assertFalse(reading["scientific_verdict"]); self.assertEqual(reading["label"], "HALTED-V12")
        self.assertIn(detail, reading["detail"])

    def test_huge_integer_refusal(self):
        r = fixture(); r["budget"]["ceilings"]["stage01"] = 10**400; seal_schedule(r)
        self.rejected(self.R.read_process(r), "phase01 clock provenance")

    def test_c01_neighbors(self):
        for value in (7199.999, 7200., 7200.001, 10799.999, 10800., 10800.001, 5400., True):
            with self.subTest(value=value):
                r = fixture(); r["budget"]["ceilings"]["stage01"] = value; seal_schedule(r)
                got = self.R.read_process(r)
                if type(value) in (int, float) and 7200. <= value <= 10800.: self.assertTrue(got["scientific_verdict"], got)
                else: self.rejected(got, "phase01 clock provenance")

    def test_pass_launch(self):
        for launch, ceilings in ((_launch(stage01=7200.), {"stage01":10800.}),
                                  (_launch(stage3=None), {"stage3":24000.})):
            with self.subTest(launch=launch):
                out = self.root / str(len(list(self.root.iterdir())))
                r = fixture(); r["budget"]["ceilings"].update(ceilings); seal_schedule(r)
                _attempt_dir(self.D, out, r, {"launch":launch})
                self.rejected(self.R.read_directory(out), "pass ceilings differ from launch")

    def test_go_ceilings(self):
        go = _go_record(); go["ceilings"]["stage2"] = 12900.
        launch = _launch(stage2=12600., go=go); r = fixture(); r["budget"]["ceilings"]["stage2"] = 12600.; seal_schedule(r)
        _attempt_dir(self.D, self.root / "a", r, {"launch":launch})
        self.rejected(self.R.read_directory(self.root / "a"), "launch ceiling not the go selection")

    def test_benchmark_sha(self):
        launch = _launch(); launch["benchmark"]["sha256"] = "c"*64
        _attempt_dir(self.D, self.root / "a", fixture(), {"launch":launch})
        self.rejected(self.R.read_directory(self.root / "a"), "launch benchmark differs from go")

    def test_history_ceilings(self):
        r = fixture(); r["budget"]["history"][0]["ceilings"]["stage01"] = 9000.
        self.rejected(self.R.read_process(r), "projection ceilings differ from record ceilings")

    def test_scope_ceiling(self):
        r = fixture(); r["budget"]["history"][0]["scopes"]["stage01"]["ceiling_s"] += 1.
        self.rejected(self.R.read_process(r), "projection ceilings differ from record ceilings")

    def test_process_ceilings(self):
        p1 = fixture(stage=2); p2 = fixture(stage=2); second_process(p2)
        p2["budget"]["ceilings"]["stage01"] = 8100.; seal_schedule(p2)
        repro = {"R1":{"status":"PASS"}, "R2":{"difference":0}, "R3":{"disagree":0},
                 "artifact_identity":"EXACT", "numeric_behavioral_reproduction":"PASS"}
        self.rejected(self.R.read_run(p1, p2, repro), "process ceilings differ")


class WrapperTests(unittest.TestCase):
    def setUp(self):
        import shutil
        self.assertTrue((ROOT / "tools/run_c10z_attempt.sh").exists(), "attempt wrapper missing")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root = Path(self.tmp.name)
        (self.root / "tools").mkdir(); (self.root / ".venv/bin").mkdir(parents=True)
        shutil.copyfile(ROOT / "tools/run_c10z_attempt.sh", self.root / "tools/run_c10z_attempt.sh")
        os.chmod(self.root / "tools/run_c10z_attempt.sh", 0o755)
        (self.root / ".venv/bin/python").symlink_to(sys.executable)
        self.out = self.root / "out"; self.out.mkdir(); self.calls = self.root / "calls"
        stage = self.root / "tools/run_c10z_stage.sh"
        stage.write_text('#!/bin/bash\nprintf "%s\\n" "$1" >> "$STUB_CALLS"\nif [ "$1" = 0 ]; then exit "${STUB_FAIL:-0}"; fi\nexit 0\n')
        os.chmod(stage, 0o755)

    def run_wrapper(self, reading, **over):
        import subprocess
        (self.out / "run.json").write_text(json.dumps(reading)); self.calls.unlink(missing_ok=True)
        env = dict(os.environ, C10Z_OUT_DIR=str(self.out), STUB_CALLS=str(self.calls)); env.update(over)
        result = subprocess.run([str(self.root / "tools/run_c10z_attempt.sh")], env=env, capture_output=True, text=True)
        calls = self.calls.read_text().splitlines() if self.calls.exists() else []
        return result, calls

    def test_next_stage_types(self):
        for value, rc, expected in ((None,0,["0","1"]),(2,0,["0","1","2"]),("2",4,["0","1"]),
                                    (2.,4,["0","1"]),(True,4,["0","1"]),(3,4,["0","1"])):
            with self.subTest(value=value):
                result, calls = self.run_wrapper({"reading":{"next_stage":value}})
                self.assertEqual(result.returncode, rc, result.stdout + result.stderr); self.assertEqual(calls, expected)
        for reading in ({}, {"reading":{}}, {"reading":None}):
            result, calls = self.run_wrapper(reading); self.assertEqual(result.returncode,4); self.assertEqual(calls,["0","1"])

    def test_relative_out(self):
        result, calls = self.run_wrapper({}, C10Z_OUT_DIR="relative")
        self.assertEqual(result.returncode,2); self.assertEqual(calls,[])

    def test_stage0_failure(self):
        result, calls = self.run_wrapper({}, STUB_FAIL="7")
        self.assertEqual(result.returncode,7); self.assertEqual(calls,["0"])


class PinTests(unittest.TestCase):
    def test_temp_copy_byte_drift(self):
        def check(path): self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), PREREG)
        check(ROOT / "docs/C10Z_ASTRA_PREREG.md")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prereg.md"; path.write_bytes((ROOT / "docs/C10Z_ASTRA_PREREG.md").read_bytes() + b"x")
            with self.assertRaises(AssertionError): check(path)


class TelemetryIntegrationTests(unittest.TestCase):
    def test_on_off_science(self):
        self._write_cases()

    def test_write_telemetry_failures_preserve_science(self):
        self._write_cases([("mkdir", None), ("open", None)] + [
            (operation, kind) for operation in ("write", "flush", "fsync")
            for kind in ("phase", "write_norms", "target_probs", "logit_lens")])

    def _write_cases(self, failures=()):
        import torch
        D = importlib.import_module("c10z_astra_arms"); R = importlib.import_module("c10z_astra_read")
        self.assertTrue(hasattr(D, "Telemetry"), "telemetry integration absent")
        outputs = []
        cases = [(False, None, None), (True, None, None)] + [(True, op, kind) for op, kind in failures]
        for on, failure, kind in cases:
            with self.subTest(on=on, failure=failure, kind=kind), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp); model = _telemetry_tiny_model(); context = _telemetry_session(model)
                clock = mock.Mock(return_value=0.); monotonic = mock.Mock(return_value=0.)
                b = D.Budget(0., C01_FIX, 12000., 24000., clock=clock)
                b.project = mock.Mock(wraps=b.project); b.check = mock.Mock(wraps=b.check)
                s, events = _write_session(D, budget=b); s.out = out; s.active_recipe = "Z"
                s.H = context.H; s.H.PTEST = ["{}"]; s.hp = context.hp; s.population = context.population
                s.gates = D.Gates(); s.gates.law3 = True
                s.hooks_check = mock.Mock(wraps=s.hooks_check); s.sync = mock.Mock(wraps=s.sync)
                s.check_memory = mock.Mock(return_value={"rss_bytes":1,"driver_bytes":1,"float64_on_mps":False})
                base = s.observe
                def observe(*a, **kw):
                    with torch.no_grad(): model(torch.tensor([[1,2]]), use_cache=False, logits_to_keep=0)
                    return base(*a, **kw)
                s.observe = observe; s.make_batch = lambda arm, frames: s.batches[arm]
                s.probe_hits = lambda arm: {"F0":[]}
                s.transfer_diagnostic = lambda batch, obs: {"status":"POST-WRITE-DIAGNOSTIC"}
                s.lead_rows = lambda batch, obs: [[obs["leads"].tolist()]]
                methods = ("__init__", "phase", "write_norms", "target_probs", "logit_lens")
                with mock.patch.object(D, "time", _types.SimpleNamespace(monotonic=monotonic)), \
                     mock.patch.object(D.uuid, "uuid4", return_value=_types.SimpleNamespace(hex="fixed-id")), \
                     mock.patch.object(D.os, "getpid", return_value=123), \
                     _telemetry_failure(out, failure, kind) as injection:
                    if on: s.telemetry = D.Telemetry(out, 1, "fixed-attempt")
                    else: self.assertIsNone(s.telemetry)
                    with __import__("contextlib").ExitStack() as stack:
                        spies = [stack.enter_context(mock.patch.object(D.Telemetry, name, side_effect=AssertionError("off path called telemetry"))) for name in methods] if not on else []
                        delta = s.write_arm(REQ_A7, "astra"); hook = s.arm_hook(A7, {})
                    for spy in spies: self.assertEqual(spy.call_count,0)
                    counts = {"clock":clock.call_count,"monotonic":monotonic.call_count,"project":b.project.call_count,
                              "check":b.check.call_count,"hooks_check":s.hooks_check.call_count,"sync":s.sync.call_count,
                              "science_forwards":sum(not call["output_hidden_states"] for call in model.forward_calls)}
                    r = fixture(stage=2); _attempt_dir(D, out / "records", r, {})
                    for key in ("recipes","fingerprint","manifest","H_pristine","checks","restores","memory","attempt_id","process"):
                        setattr(s,key,copy.deepcopy(r[key]))
                    s.recipes["A"]["arms"][A7]["realised_layer_delta_norms"] = {"4":1.}
                    s.recipes["Z"]["arms"][A7]["write"]["geometry"] = {"layer_delta_norms":{"4":.4}}
                    s.out = out / "records"; s.initial_sources = r["fingerprint"]["start"]
                    s.budget = _types.SimpleNamespace(durations=r["budget"]["ceilings"], origins=r["budget"]["origins"], history=r["budget"]["history"])
                    with mock.patch.object(D,"source_hashes",return_value=s.initial_sources): produced = s.record(2)
                    D.write_json(out / "science.json", produced)
                if failure is not None:
                    self.assertFalse(s.telemetry.enabled)
                    self._assert_telemetry_failure(injection, failure, kind)
                reading = R.read_process(produced); self.assertTrue(reading["scientific_verdict"],reading)
                files = {str(p.relative_to(out)):p.read_bytes() for p in out.rglob("*") if p.is_file() and "telemetry" not in p.relative_to(out).parts}
                outputs.append((json.loads(json.dumps({"delta":delta,"hook":hook,"record":produced,"reading":reading},allow_nan=False)),counts,files))
                self.assertEqual((out / "telemetry").exists(), on and failure != "mkdir")
                if on and failure is None:
                    lines = [json.loads(line) for line in (out / "telemetry/telemetry_p1.jsonl").read_text().splitlines()]
                    self.assertEqual({v["kind"] for v in lines}, {"header","phase","write_norms","target_probs","logit_lens"})
                    self.assertTrue(any(v.get("round_no") == "final" for v in lines))
        for case, output in zip(cases[1:], outputs[1:]):
            self.assertEqual(outputs[0], output,
                             "telemetry changed scientific bytes, reading or science call counts: " + str(case))

    def test_resident_on_off(self):
        self._resident_cases()

    def test_resident_telemetry_failures_preserve_science(self):
        self._resident_cases([(op, None if op in ("mkdir", "open") else "phase")
                              for op in ("mkdir", "open", "write", "flush", "fsync")])

    def _assert_telemetry_failure(self, injection, operation, kind):
        self.assertEqual(injection["hits"], [(operation, kind)], "failure injection was not reached exactly once")
        markers = [line for line in injection["stdout"].getvalue().splitlines()
                   if line.startswith("C10Z_TELEMETRY_DISABLED")]
        self.assertEqual(markers, ["C10Z_TELEMETRY_DISABLED OSError: advisory-" + operation])

    def _resident_cases(self, failures=()):
        D = importlib.import_module("c10z_astra_arms"); R = importlib.import_module("c10z_astra_read")
        self.assertTrue(hasattr(D,"Telemetry"),"resident telemetry absent")
        results = []
        cases = [(False, None, None), (True, None, None)] + [(True, op, kind) for op, kind in failures]
        for on, failure, kind in cases:
            with self.subTest(on=on, failure=failure, kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); out = root / "attempt"; r = fixture(n=18)
                r["budget"]["ceilings"].update(stage2=None,stage3=None); seal_schedule(r)
                _attempt_dir(D,out,r,{})
                launch = _launch(stage2=None,stage3=None,telemetry=on,telemetry_inertness={"path":"inertness","sha256":"a"*64} if on else None)
                with mock.patch.object(D,"ROOT",root), mock.patch.object(D.os,"getpid",return_value=r["pid"]), \
                     mock.patch.object(D.uuid,"uuid4",return_value=_types.SimpleNamespace(hex="fixed-id")), \
                     _telemetry_failure(out, failure, kind) as injection:
                    metrics = {}; rc,events,exits = _mock_resident(D,R,out,r,launch,metrics=metrics)
                if failure is not None: self._assert_telemetry_failure(injection, failure, kind)
                self.assertEqual(rc,0); self.assertEqual(exits,[])
                run = D.load_json(out / "run.json")
                self.assertEqual(run["completed"], 1); self.assertIs(run["closed"], True); self.assertIsNone(run["halt"])
                self.assertEqual([e for e in events if isinstance(e, str)], ["stage0", "stage1", "closed"])
                got = R.read_directory(out); self.assertTrue(got["scientific_verdict"],got)
                files = {}
                for p in out.rglob("*"):
                    if p.is_file() and "telemetry" not in p.relative_to(out).parts:
                        raw = p.read_bytes()
                        if p.name == "run.json":
                            value = json.loads(raw); value["launch"].pop("telemetry"); value["launch"].pop("telemetry_inertness")
                            raw = json.dumps(value,sort_keys=True,allow_nan=False).encode()
                        files[str(p.relative_to(out))] = raw
                results.append((files,got,metrics))
                self.assertEqual((out / "telemetry").exists(), on and failure != "mkdir")
                if on and failure is None:
                    lines = [json.loads(x) for x in (out / "telemetry/telemetry_p1.jsonl").read_text().splitlines()]
                    self.assertEqual([(x["event"],x["stage"]) for x in lines if x["kind"]=="phase"],
                                     [("stage_start",0),("stage_end",0),("stage_start",1),("stage_end",1)])
        for case, result in zip(cases[1:], results[1:]):
            self.assertEqual(results[0], result, "resident telemetry changed files, reading or clocks: " + str(case))

    def test_placements_ast(self):
        tree = ast.parse((HERE / "c10z_astra_arms.py").read_text())
        classes = {n.name:n for n in tree.body if isinstance(n,ast.ClassDef)}
        self.assertIn("Telemetry",classes,"Telemetry class absent")
        methods = {n.name:n for n in classes["Session"].body if isinstance(n,ast.FunctionDef)}
        def is_lens(stmt):
            return isinstance(stmt,ast.If) and any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and
                n.func.attr=="logit_lens" and isinstance(n.func.value,ast.Attribute) and n.func.value.attr=="telemetry" for n in ast.walk(stmt))
        for name, predicate in (("stage0",lambda n:isinstance(n,ast.For) and any(isinstance(x,ast.Attribute) and x.attr=="pristine_probes" for x in ast.walk(n))),
                                ("arm_hook",lambda n:isinstance(n,ast.Assign) and any(isinstance(x,ast.Constant) and x.value=="hits" for x in ast.walk(n.targets[0])))):
            body=methods[name].body; index=next(i for i,n in enumerate(body) if predicate(n))
            self.assertTrue(is_lens(body[index+1]),name+" lens is not the immediately following statement")
        direct=[]
        for node in tree.body:
            if isinstance(node,ast.FunctionDef):
                if any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="logit_lens" for n in ast.walk(node)):direct.append(node.name)
            if isinstance(node,ast.ClassDef):
                for fun in (n for n in node.body if isinstance(n,ast.FunctionDef)):
                    if any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="logit_lens" for n in ast.walk(fun)):direct.append(node.name+"."+fun.name)
        self.assertCountEqual(direct,["Telemetry.logit_lens","telemetry_mps_inertness_check"])


# Telemetry tests for integration before the selftest's final __main__ block.
# Root alone runs these CPU-only tests, after the numbered list is recorded.
import contextlib as _telemetry_contextlib
import io as _telemetry_io


@_telemetry_contextlib.contextmanager
def _telemetry_failure(out, operation=None, kind=None):
    """Fault only the telemetry sink; scientific serialization still uses real IO."""
    D = importlib.import_module("c10z_astra_arms")
    result = {"hits": [], "stdout": _telemetry_io.StringIO()}; streams = []; pending = [None]
    real_open = Path.open; real_mkdir = Path.mkdir; real_fsync = D.os.fsync
    def fail():
        result["hits"].append((operation, kind)); raise OSError("advisory-" + operation)
    def mkdir(path, *args, **kwargs):
        if path == out / "telemetry" and operation == "mkdir": fail()
        return real_mkdir(path, *args, **kwargs)
    def opened(path, *args, **kwargs):
        if path != out / "telemetry/telemetry_p1.jsonl": return real_open(path, *args, **kwargs)
        if operation == "open": fail()
        stream = real_open(path, *args, **kwargs); streams.append(stream)
        handle = mock.Mock(wraps=stream); handle.fileno.return_value = stream.fileno()
        def write(data):
            pending[0] = json.loads(data)["kind"]
            if operation == "write" and pending[0] == kind: fail()
            return stream.write(data)
        def flush():
            if operation == "flush" and pending[0] == kind: fail()
            return stream.flush()
        handle.write.side_effect = write; handle.flush.side_effect = flush
        return handle
    def fsync(fd):
        if operation == "fsync" and streams and fd == streams[-1].fileno() and pending[0] == kind: fail()
        return real_fsync(fd)
    try:
        with _telemetry_contextlib.ExitStack() as stack:
            stack.enter_context(_telemetry_contextlib.redirect_stdout(result["stdout"]))
            if operation is not None:
                stack.enter_context(mock.patch.object(Path, "mkdir", autospec=True, side_effect=mkdir))
                stack.enter_context(mock.patch.object(Path, "open", autospec=True, side_effect=opened))
                stack.enter_context(mock.patch.object(D.os, "fsync", side_effect=fsync))
            yield result
    finally:
        for stream in streams: stream.close()


def _telemetry_tiny_model(layers=12):
    import torch
    width = layers

    class Layer(torch.nn.Module):
        def __init__(self, number):
            super().__init__()
            increment = torch.zeros(width)
            increment[number] = number + 1.
            self.register_buffer("increment", increment)
            self.mlp = torch.nn.Module()
            self.mlp.down_proj = torch.nn.Linear(width, width, bias=False, dtype=torch.float16)
            with torch.no_grad(): self.mlp.down_proj.weight.fill_(number + 1.)
        def forward(self, x): return x + self.increment

    class Norm(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.weight = torch.nn.Parameter(torch.ones(width))
            self.register_buffer("epsilon", torch.tensor(1e-6))
        def forward(self, x):
            assert not torch.is_grad_enabled(), "norm ran outside no_grad"
            return x * self.weight

    class Head(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.weight = torch.nn.Parameter(torch.zeros(width + 5, width))
            with torch.no_grad(): self.weight[:width].copy_(torch.eye(width))
        def forward(self, x):
            assert not torch.is_grad_enabled(), "head ran outside no_grad"
            return torch.nn.functional.linear(x, self.weight)

    class Tiny(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.model = torch.nn.Module()
            self.model.embed_tokens = torch.nn.Embedding(width + 5, width)
            with torch.no_grad(): self.model.embed_tokens.weight.zero_()
            self.model.layers = torch.nn.ModuleList([Layer(i) for i in range(layers)])
            self.model.norm = Norm(); self.lm_head = Head()
            self.config = _types.SimpleNamespace(num_hidden_layers=layers, use_cache=False)
            self.forward_calls = []
        def forward(self, input_ids, attention_mask=None, use_cache=False, logits_to_keep=0,
                    output_hidden_states=False):
            assert not torch.is_grad_enabled(), "model ran outside no_grad"
            self.forward_calls.append({"ids": input_ids.detach().clone(), "attention_mask":
                None if attention_mask is None else attention_mask.detach().clone(),
                "use_cache": use_cache, "logits_to_keep": logits_to_keep,
                "output_hidden_states": output_hidden_states})
            hidden = self.model.embed_tokens(input_ids); states = []
            for layer in self.model.layers:
                states.append(hidden); hidden = layer(hidden)
            hidden = self.model.norm(hidden); states.append(hidden)
            logits = self.lm_head(hidden)
            if logits_to_keep: logits = logits[:, -logits_to_keep:, :]
            return _types.SimpleNamespace(logits=logits, hidden_states=tuple(states))
    return Tiny()


def _telemetry_items():
    return [{"view": 0, "subject": 0, "prompt_ids": [1, 2], "first_ids": [3]}]


def _telemetry_session(model):
    tok = _types.SimpleNamespace(decode=lambda ids: "token-" + str(ids[0]))
    return _types.SimpleNamespace(H=_types.SimpleNamespace(model=model, tok=tok, DEV="cpu"),
        population={A7: {"F0": _telemetry_items()}}, hp=_types.SimpleNamespace(layers=[4, 5, 6, 7, 8]))


def _telemetry_state(model, tensors):
    import torch
    return {"parameters": {n: (v.detach().clone(), v.data_ptr()) for n, v in model.named_parameters()},
        "buffers": {n: (v.detach().clone(), v.data_ptr()) for n, v in model.named_buffers()},
        "rng": torch.random.get_rng_state().clone(), "training": {n: m.training for n, m in model.named_modules()},
        "hooks": {n: (dict(m._forward_hooks), dict(m._forward_pre_hooks), dict(m._backward_hooks))
                  for n, m in model.named_modules()}, "grad": torch.is_grad_enabled(),
        "inputs": [(v.detach().clone(), v.data_ptr()) for v in tensors]}


class TelemetryUnitTests(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms")
        for name in ("Telemetry", "target_probabilities", "logit_lens", "TELEMETRY_CLOCK"):
            self.assertTrue(hasattr(self.D, name), "required telemetry API absent: " + name)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.clock = [0.]
        def clock():
            self.clock[0] += 1.; return self.clock[0]
        patcher = mock.patch.object(self.D, "TELEMETRY_CLOCK", clock)
        patcher.start(); self.addCleanup(patcher.stop)

    def lines(self):
        path = self.out / "telemetry/telemetry_p1.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def observation(self, n=3):
        import torch
        return {"native_gathered": torch.arange(n * 7, dtype=torch.float32).reshape(n, 7) / 9,
                "targets": torch.tensor([i % 7 for i in range(n)])}, [
            {"row": i, "fact": i // 2, "view": i % 2, "q": i, "target": i % 7} for i in range(n)]

    def direct_calls(self, writer, session=None):
        import torch
        session = session or _telemetry_session(_telemetry_tiny_model())
        obs, requirements = self.observation()
        patch = {4: torch.tensor([[3., 4.]])}; cumulative = {4: torch.tensor([[6., 8.]])}
        writer.phase("round_end", round_no=0, arm=A7, recipe="Z", seconds=4., F=3, columns_written=2)
        writer.write_norms(patch, cumulative, round_no=0, arm=A7)
        writer.target_probs(obs, chunk_rows=2, requirements=requirements, round_no="final", arm=A7)
        writer.logit_lens(session, A7, "post_write")

    def test_T4_public_methods_avoid_science_clocks_and_gates(self):
        D = self.D; model = _telemetry_tiny_model(); session = _telemetry_session(model)
        session.budget = _types.SimpleNamespace(clock=mock.Mock(), project=mock.Mock(), check=mock.Mock())
        session.hooks_check = mock.Mock(); session.sync = mock.Mock()
        science_clock = mock.Mock(side_effect=AssertionError("telemetry used science monotonic"))
        with mock.patch.object(D, "time", _types.SimpleNamespace(monotonic=science_clock)):
            writer = D.Telemetry(self.out, 1, "test-attempt")
            self.direct_calls(writer, session)
        self.assertTrue(writer.enabled, "an independent telemetry clock must survive patched science time")
        for spy in (session.budget.clock, session.budget.project, session.budget.check,
                    session.hooks_check, session.sync, science_clock):
            self.assertEqual(spy.call_count, 0, "telemetry touched a science clock or gate")

    def test_T3_header_four_kinds_fields_and_full_cost_accounting(self):
        D = self.D
        original_open = Path.open
        with mock.patch.object(Path, "open", autospec=True, side_effect=original_open) as opened, \
             mock.patch.object(D.os, "fsync", wraps=D.os.fsync) as synced:
            writer = D.Telemetry(self.out, 1, "test-attempt"); self.direct_calls(writer)
        own_open = [call for call in opened.call_args_list if call.args[0] == self.out / "telemetry/telemetry_p1.jsonl"]
        self.assertEqual(len(own_open), 1, "telemetry opens its append file once")
        self.assertEqual(own_open[0].args[1], "a")
        lines = self.lines()
        self.assertEqual([v["kind"] for v in lines], ["header", "phase", "write_norms", "target_probs", "logit_lens"])
        self.assertEqual(lines[0]["telemetry"], True); self.assertEqual(synced.call_count, len(lines))
        self.assertEqual(lines[0]["elapsed_s"], 1.); self.assertEqual(lines[0]["cumulative_s"], 0.)
        self.assertEqual([v["cumulative_s"] for v in lines], [0., 2., 4., 6., 8.],
                         "cumulative_s must include every earlier write and fsync")
        for line in lines:
            self.assertTrue({"kind", "t_utc", "elapsed_s", "cumulative_s", "process", "attempt_id"} <= set(line))
            self.assertEqual((line["process"], line["attempt_id"]), (1, "test-attempt"))
            self.assertTrue(line["t_utc"].endswith("+00:00"))
            self.assertEqual(line, json.loads(json.dumps(line, sort_keys=True, allow_nan=False)))
        self.assertEqual(lines[1]["event"], "round_end")
        self.assertEqual(lines[2]["norms"], {"4": {"patch_fro": 5., "cumulative_fro": 10.}})
        self.assertEqual(lines[3]["round_no"], "final")
        self.assertEqual([len(lines[3][key]) for key in ("rows", "facts", "views", "qs", "p")], [3] * 5)
        self.assertEqual(lines[4]["where"], "post_write"); self.assertEqual(lines[4]["arm"], A7)
        self.assertEqual(lines[4]["layers"], [4, 5, 6, 7, 8])

    def disabled_failure(self, operation):
        D = self.D
        science = self.out / "science.json"; science.write_text('{"science":true}\n'); before = science.read_bytes()
        methods = ("constructor",) if operation in ("mkdir", "open") else ("phase", "write_norms", "target_probs", "logit_lens")
        for method in methods:
            with self.subTest(operation=operation, method=method):
                stream = _telemetry_io.StringIO()
                if operation in ("mkdir", "open"):
                    target = mock.patch.object(Path, "mkdir", side_effect=OSError("test-mkdir")) if operation == "mkdir" else \
                             mock.patch.object(Path, "open", side_effect=OSError("test-open"))
                    with target, _telemetry_contextlib.redirect_stdout(stream): writer = D.Telemetry(self.out, 1, "test-attempt")
                else:
                    writer = D.Telemetry(self.out / method, 1, "test-attempt"); writer.file.close()
                    handle = mock.Mock(); handle.fileno.return_value = 7
                    if operation in ("write", "flush"): getattr(handle, operation).side_effect = OSError("test-" + operation)
                    writer.file = handle
                    target = mock.patch.object(D.os, "fsync", side_effect=OSError("test-fsync")) if operation == "fsync" else \
                             _telemetry_contextlib.nullcontext()
                    with target, _telemetry_contextlib.redirect_stdout(stream): self.invoke(writer, method)
                with _telemetry_contextlib.redirect_stdout(stream), \
                     mock.patch.object(D, "logit_lens") as lens, mock.patch.object(D, "target_probabilities") as probs:
                    clock_before = self.clock[0]; self.direct_calls(writer)
                self.assertFalse(writer.enabled); self.assertEqual(self.clock[0], clock_before)
                self.assertEqual(lens.call_count, 0); self.assertEqual(probs.call_count, 0)
                markers = stream.getvalue().splitlines()
                self.assertEqual(len(markers), 1); self.assertTrue(markers[0].startswith("C10Z_TELEMETRY_DISABLED OSError: test-"), markers)
                self.assertEqual(science.read_bytes(), before)
        D.write_json(self.out / "completion.json", {"completed": True})
        self.assertEqual(json.loads((self.out / "completion.json").read_text()), {"completed": True})

    def invoke(self, writer, method):
        import torch
        obs, requirements = self.observation(); patch = {4: torch.ones((2, 2))}
        if method == "phase": return writer.phase("stage_start", stage=1)
        if method == "write_norms": return writer.write_norms(patch, patch, round_no=0, arm=A7)
        if method == "target_probs": return writer.target_probs(obs, requirements=requirements, round_no=0, arm=A7)
        return writer.logit_lens(_telemetry_session(_telemetry_tiny_model()), A7, "pristine")

    def test_T5a_initial_open_failure_is_disabled_once(self): self.disabled_failure("open")
    def test_T5a_directory_failure_is_disabled_once(self): self.disabled_failure("mkdir")
    def test_T5b_write_failure_is_disabled_once(self): self.disabled_failure("write")
    def test_T5c_flush_failure_is_disabled_once(self): self.disabled_failure("flush")
    def test_T5d_fsync_failure_is_disabled_once(self): self.disabled_failure("fsync")

    def test_T5e_keyboard_interrupt_propagates(self):
        with mock.patch.object(Path, "open", side_effect=KeyboardInterrupt("test-interrupt")):
            with self.assertRaisesRegex(KeyboardInterrupt, "test-interrupt"):
                self.D.Telemetry(self.out, 1, "test-attempt")
        for method in ("phase", "write_norms", "target_probs", "logit_lens"):
            with self.subTest(method=method):
                writer = self.D.Telemetry(self.out / method, 1, "test-attempt"); writer.file.close()
                writer.file = mock.Mock(); writer.file.write.side_effect = KeyboardInterrupt("test-interrupt")
                with self.assertRaisesRegex(KeyboardInterrupt, "test-interrupt"): self.invoke(writer, method)

    def test_T6_each_call_preserves_cpu_model_and_inputs(self):
        import torch
        D = self.D; model = _telemetry_tiny_model(); session = _telemetry_session(model)
        obs, requirements = self.observation(); patches = {4: torch.tensor([[3., 4.]])}
        cumulative = {4: patches[4] * 2}; science_ids = torch.tensor([[1, 2]])
        tensors = [obs["native_gathered"], obs["targets"], patches[4], cumulative[4], science_ids]
        with torch.no_grad(): reference = model(science_ids, use_cache=False, logits_to_keep=0).logits.clone()
        writer = D.Telemetry(self.out, 1, "test-attempt")
        calls = [lambda: writer.phase("stage_start", stage=0),
                 lambda: writer.write_norms(patches, cumulative, round_no=0, arm=A7),
                 lambda: writer.target_probs(obs, requirements=requirements, round_no=0, arm=A7),
                 lambda: writer.logit_lens(session, A7, "pristine")]
        for call in calls:
            before = _telemetry_state(model, tensors); input_hashes = [D.tensor_hash(v) for v in tensors]
            call(); after = _telemetry_state(model, tensors)
            self.assertEqual(input_hashes, [D.tensor_hash(v) for v in tensors], "telemetry changed input tensor bytes")
            self.assertTrue(writer.enabled)
            for group in ("parameters", "buffers"):
                self.assertEqual(set(before[group]), set(after[group]))
                for name in before[group]:
                    old, pointer = before[group][name]; new, new_pointer = after[group][name]
                    self.assertTrue(torch.equal(old, new), group + " changed: " + name)
                    self.assertEqual(pointer, new_pointer, group + " storage changed: " + name)
            self.assertTrue(torch.equal(before["rng"], after["rng"])); self.assertEqual(before["training"], after["training"])
            self.assertEqual(before["hooks"], after["hooks"]); self.assertEqual(before["grad"], after["grad"])
            for (old, ptr), (new, new_ptr) in zip(before["inputs"], after["inputs"]):
                self.assertTrue(torch.equal(old, new)); self.assertEqual(ptr, new_ptr)
            with torch.no_grad(): following = model(science_ids, use_cache=False, logits_to_keep=0).logits
            self.assertTrue(torch.equal(reference, following), "telemetry changed next science forward")

    def test_T6_lens_uses_layer_output_top5_and_no_grad(self):
        import torch
        model = _telemetry_tiny_model(); session = _telemetry_session(model)
        result = self.D.logit_lens(model, _telemetry_items(), session.hp.layers, session.H.tok, "cpu")
        self.assertEqual(result["layers"], session.hp.layers)
        self.assertEqual({k: result["items"][0][k] for k in ("view", "subject", "prompt_ids")},
                         {k: _telemetry_items()[0][k] for k in ("view", "subject", "prompt_ids")})
        for layer in session.hp.layers:
            hidden = torch.zeros(12); hidden[:layer + 1] = torch.arange(1., layer + 2.)
            with torch.no_grad(): probs = model.lm_head(model.model.norm(hidden)).float().softmax(-1)
            top = probs.topk(5); actual = result["items"][0]["top"][str(layer)]
            self.assertEqual([row[0] for row in actual], top.indices.tolist(), "lens used layer input instead of output")
            self.assertEqual([row[1] for row in actual], ["token-" + str(i) for i in top.indices.tolist()])
            self.assertTrue(torch.allclose(torch.tensor([row[2] for row in actual]), top.values, atol=1e-7, rtol=0))
        self.assertEqual(model.forward_calls[0]["logits_to_keep"], 1)
        self.assertEqual(model.forward_calls[0]["use_cache"], False)
        self.assertEqual(model.forward_calls[0]["output_hidden_states"], True)
        with self.assertRaises(ValueError): self.D.logit_lens(model, _telemetry_items(), [11], session.H.tok, "cpu")

    def test_T7_probabilities_dense_reference_and_row_chunk_bound(self):
        import torch
        values = torch.tensor([[90., 91., 89.], [-90., -91., -89.], [0., 0., 0.],
                               [1., -2., 3.], [9., 8., 7.]], dtype=torch.float64)
        targets = torch.tensor([0, 2, 1, 2, 0]); slices = []
        class Slices:
            shape = values.shape
            def __getitem__(self, index):
                self_outer.assertIsInstance(index, slice); part = values[index]; slices.append(len(part)); return part
        self_outer = self
        result = self.D.target_probabilities(Slices(), targets, 2)
        expected = values.softmax(1)[torch.arange(len(targets)), targets]
        self.assertEqual(result.dtype, torch.float32); self.assertEqual(result.device.type, "cpu")
        self.assertTrue(torch.allclose(result.double(), expected, atol=1e-6, rtol=0))
        self.assertEqual(slices, [2, 2, 1]); self.assertTrue(all(n <= 2 for n in slices))

    def test_T7_default_chunk_keeps_cpu_float32_under64MiB(self):
        obs, requirements = self.observation(5)
        writer = self.D.Telemetry(self.out, 1, "test-attempt")
        with mock.patch.object(self.D, "target_probabilities", wraps=self.D.target_probabilities) as probabilities:
            writer.target_probs(obs, requirements=requirements, round_no=0, arm=A7)
        self.assertTrue(writer.enabled); args = probabilities.call_args.args
        self.assertEqual(args[2], max(1, (64 * 2**20) // (4 * obs["native_gathered"].shape[1])))
        self.assertLessEqual(args[2] * 4 * obs["native_gathered"].shape[1], 64 * 2**20)

    def test_T9_write_volume_no_requirement_lines(self):
        import torch
        D = self.D; s, events = _write_session(D); s.out = self.out; s.active_recipe = "Z"
        batch = s.batches[A7]
        batch["requirements"].append(dict(batch["requirements"][0], q=1, index=2))
        batch["target_lengths"] = [2]; batch["T_pad"] = 3
        original_observe, original_quantities, original_covectors = s.observe, s.quantities, s.covectors
        def observe(*args, **kwargs):
            obs = original_observe(*args, **kwargs)
            for key in ("leads", "competitors", "targets", "scales"): obs[key] = obs[key].repeat(2)
            obs["native_gathered"] = obs["native_gathered"].repeat(2, 1)
            obs["keys"] = {l: v.repeat(2, 1) for l, v in obs["keys"].items()}
            return obs
        def quantities(obs, carriers):
            _, C, direction, scale, keys, weights = original_quantities(obs, carriers)
            return torch.arange(2), C.repeat(2, 1), direction.repeat(2, 1), scale.repeat(2), \
                   {l: v.repeat(2, 1) for l, v in keys.items()}, weights
        s.observe = observe; s.quantities = quantities
        s.covectors = lambda obs: original_covectors(obs).repeat(2, 1)
        session = _telemetry_session(_telemetry_tiny_model()); s.H = session.H; s.H.PTEST = ["{}"]
        s.hp = session.hp; s.population = session.population; s.gates = D.Gates(); s.gates.law3 = True
        writer = D.Telemetry(self.out, 1, "test-attempt"); s.telemetry = writer
        s.make_batch = lambda arm, frames: s.batches[arm]
        s.probe_hits = lambda arm: {"F0": []}; s.transfer_diagnostic = lambda batch, obs: {"status": "POST-WRITE-DIAGNOSTIC"}
        s.lead_rows = lambda batch, obs: [[obs["leads"].tolist()]]
        with mock.patch.object(D, "time", _types.SimpleNamespace(monotonic=lambda: 0.)):
            before = len(self.lines()); s.write_arm(REQ_A7, "astra"); rounds = s.current["write"]["rounds_used"]
            self.assertEqual(len(self.lines()) - before, 1 + 3 * rounds + 1,
                             "one line per event and round, never per requirement")
            write_lines = self.lines()[before:]
            self.assertEqual(write_lines[0]["event"], "write_start")
            for r in range(rounds):
                phase, norms, probabilities = write_lines[1 + 3*r:4 + 3*r]
                self.assertEqual((phase["event"], norms["kind"], probabilities["kind"]),
                                 ("round_end", "write_norms", "target_probs"))
                self.assertEqual([phase["round_no"], norms["round_no"], probabilities["round_no"]], [r] * 3)
                self.assertEqual(phase["seconds"], s.current["write"]["round_seconds"][r])
                self.assertEqual(len(probabilities["p"]), 2)
            self.assertEqual(write_lines[-1]["round_no"], "final")
            before_hook = len(self.lines()); s.arm_hook(A7, {})
            self.assertEqual(len(self.lines()) - before_hook, 1)
            self.assertEqual((self.lines()[-1]["kind"], self.lines()[-1]["where"]), ("logit_lens", "post_write"))


def _telemetry_probe_fixture(mode="deterministic"):
    import torch
    population = {"F0": _telemetry_items(), "prefix": [
        {"prompt_ids": [2], "target": [4, 5, 6], "depth": 1}], "subject_free": [
        {"prompt_ids": [3], "target": [4, 5], "depth": 2}], "relations": [{"prompt_ids": [4], "first_ids": [3]}]}
    batch = {"input_ids": [[1, 2], [2, 3]], "attention_mask": [[1, 1], [1, 1]],
             "requirements": [{"row": 0, "index": 1}, {"row": 1, "index": 0}]}
    class Model:
        def __init__(self): self.calls = []; self.hidden_count = 0; self.pending_batch = False; self.plain = 0
        def __call__(self, *args, **kwargs):
            assert not torch.is_grad_enabled(), "inertness forward outside no_grad"
            hidden = kwargs.get("output_hidden_states", False)
            ids = kwargs["input_ids"] if "input_ids" in kwargs else args[0]
            is_batch = "attention_mask" in kwargs
            self.calls.append({"ids": ids.tolist(), "positional": bool(args), "kwargs": {
                k: v.tolist() if isinstance(v, torch.Tensor) else v for k, v in kwargs.items()}})
            if hidden:
                self.hidden_count += 1
                if mode == "batch" and self.hidden_count == 2: self.pending_batch = True
            else: self.plain += 1
            token = (int(ids[0, -1]) + 1) % 9
            if mode == "probe" and not hidden and not is_batch and self.hidden_count % 2: token = (token + 1) % 9
            if mode == "drift" and not hidden: token = (token + self.plain) % 9
            logits = torch.zeros((*ids.shape, 9)); logits[:, :, token] = 10.
            if mode == "batch" and is_batch and self.pending_batch:
                logits[:, :, 0] += .25; self.pending_batch = False
            return _types.SimpleNamespace(logits=logits)
    model = Model()
    def lens(model, items, layers, tok, device):
        with torch.no_grad():
            for item in items: model(torch.tensor([item["prompt_ids"]], device=device),
                use_cache=False, output_hidden_states=True, logits_to_keep=1)
        return {"layers": list(layers), "items": []}
    return model, population, batch, lens


class TelemetryInertnessTests(unittest.TestCase):
    def setUp(self):
        self.D = importlib.import_module("c10z_astra_arms")
        self.assertTrue(hasattr(self.D, "telemetry_mps_inertness_check"), "three-pass inertness core absent")

    def run_mode(self, mode):
        model, population, batch, lens = _telemetry_probe_fixture(mode)
        with mock.patch.object(self.D, "logit_lens", lens):
            result = self.D.telemetry_mps_inertness_check(model, "cpu", population, batch, [4, 5], object())
        return result, model, population, batch

    def test_deterministic_three_pass_schedule_and_kwargs(self):
        result, model, population, batch = self.run_mode("deterministic")
        self.assertEqual(result, {"verdict": "INERT", "control_equal": True, "telemetry_equal": True,
                                  "probe_forwards": 21, "lens_forwards": 2})
        self.assertEqual(len(model.calls), 21 + 2 + 3 + 2, "warm-up excluded from evidence counts")
        hidden = [i for i, c in enumerate(model.calls) if c["kwargs"].get("output_hidden_states")]
        self.assertEqual(hidden, [10, 18], "lens must bracket T probes before T batch")
        for call in model.calls:
            kwargs = call["kwargs"]
            if "attention_mask" in kwargs:
                self.assertFalse(call["positional"])
                self.assertEqual(kwargs, {"input_ids": batch["input_ids"], "attention_mask": batch["attention_mask"],
                                          "use_cache": False, "logits_to_keep": 0})
            elif kwargs.get("output_hidden_states"):
                self.assertTrue(call["positional"])
                self.assertEqual(kwargs, {"use_cache": False, "output_hidden_states": True, "logits_to_keep": 1})
            else:
                self.assertTrue(call["positional"])
                self.assertEqual(kwargs, {"use_cache": False, "logits_to_keep": 0})

    def test_lens_sensitive_probe_is_not_inert(self):
        result, *_ = self.run_mode("probe")
        self.assertEqual((result["verdict"], result["control_equal"], result["telemetry_equal"]), ("NOT-INERT", True, False))

    def test_lens_sensitive_batch_is_not_inert(self):
        result, *_ = self.run_mode("batch")
        self.assertEqual((result["verdict"], result["control_equal"], result["telemetry_equal"]), ("NOT-INERT", True, False))

    def test_plain_drift_is_nondeterministic_baseline(self):
        result, *_ = self.run_mode("drift")
        self.assertEqual(result["verdict"], "NONDETERMINISTIC-BASELINE"); self.assertFalse(result["control_equal"])

    def test_full_greedy_suffix_count_and_compare(self):
        result, model, population, batch = self.run_mode("deterministic")
        expected_per_pass = sum(len(item["target"]) if "target" in item else 1
                                for items in population.values() for item in items)
        self.assertEqual(result["probe_forwards"], 3 * expected_per_pass)
        probe_ids = [c["ids"][0] for c in model.calls[2:10] if "attention_mask" not in c["kwargs"]]
        self.assertEqual(probe_ids[1:4], [[2], [2, 3], [2, 3, 4]], "greedy must append its generated tokens")
        self.assertEqual(probe_ids[4:6], [[3], [3, 4]])


class TelemetryRunnerTests(unittest.TestCase):
    def test_runner_driver_module_reused(self):
        # No model is constructed; both real modules have stdlib-only imports.
        with mock.patch.object(self.C, "ROOT", HERE.parents[1]), mock.patch.dict(sys.modules):
            runner_driver = self.C.arms_module()
            benchmark = self.C.benchmark_module()
            self.assertIs(benchmark._driver_module(), runner_driver,
                          "benchmark population must reuse the runner's driver module")
        self.assertNotIn("c10e_bandknob", sys.modules)

    def setUp(self):
        path = HERE / "c10z_astra_telemetry_check.py"
        self.assertTrue(path.is_file(), "telemetry inertness runner absent")
        spec = importlib.util.spec_from_file_location("c10z_telemetry_test_runner", path)
        self.C = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.C)
        self.D = importlib.import_module("c10z_astra_arms")
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        patcher = mock.patch.object(self.C, "ROOT", self.root); patcher.start(); self.addCleanup(patcher.stop)

    def test_runner_import_is_stdlib_only(self):
        # Check in a fresh process; root owns the serial subprocess execution.
        code = "import sys,importlib.util; before=set(sys.modules); p=sys.argv[1]; s=importlib.util.spec_from_file_location('check',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); added=set(sys.modules)-before; assert all(n.split('.')[0] in sys.stdlib_module_names or n.startswith('_') for n in added),sorted(added); print('STDLIB_ONLY')"
        subprocess = importlib.import_module("subprocess")
        result = subprocess.run([sys.executable, "-B", "-I", "-c", code, str(HERE / "c10z_astra_telemetry_check.py")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr); self.assertEqual(result.stdout.strip(), "STDLIB_ONLY")

    def test_runner_refuses_relative_out_path(self):
        with self.assertRaisesRegex(self.D.R.Halt, "HALTED-V12:.*must be absolute"):
            self.C.run("relative", object())
        self.assertEqual(list(self.root.rglob("inertness.json")), [])

    def test_runner_refuses_outside_and_existing_record_without_forward(self):
        outside = self.root / "results/c10z_astra_telemetry_inertness_suffix/UTC"
        with self.assertRaisesRegex(self.D.R.Halt, "HALTED-V12:.*outside"):
            self.C.run(outside, object())
        out = self.root / "results/c10z_astra_telemetry_inertness/UTC"; out.mkdir(parents=True)
        (out / "inertness.json").write_text("{}\n"); before = (out / "inertness.json").read_bytes()
        with self.assertRaisesRegex(self.D.R.Halt, "HALTED-V12:.*existing"):
            self.C.run(out, object())
        self.assertEqual((out / "inertness.json").read_bytes(), before)

    def runner_case(self, mutate=False):
        import torch
        model = _telemetry_tiny_model(36).half(); layers = [4, 5, 6, 7, 8]
        out = self.root / "results/c10z_astra_telemetry_inertness/UTC"
        env = {"python": "3.11-test", "machine": "test", "platform": "test", "torch": "test", "transformers": "test"}
        source_paths = ("experiments/track_c/c10z_astra_arms.py", "experiments/track_c/c10z_astra_read.py",
            "experiments/track_c/c10z_astra_telemetry_check.py", "experiments/track_c/c10z_astra_benchmark.py",
            "experiments/track_c/c10e_bandknob.py", "configs/hparams/qwen25_3b_memit_hparams.json",
            "memit_dry_run/memit/memit/memit_main.py")
        for relative in source_paths:
            p = self.root / relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(relative)
        spies = {name: mock.Mock(side_effect=AssertionError("write engine called: " + name))
                 for name in ("my_edit", "run_recipe", "run_law5", "apply_memit_to_model")}
        H = _types.SimpleNamespace(model=model, DEV="mps", REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b",
            MEMITHyperParams=_types.SimpleNamespace(from_json=lambda p: _types.SimpleNamespace(layers=layers)),
            tok=_types.SimpleNamespace(decode=lambda ids: str(ids[0])), **spies)
        population = {"F0": _telemetry_items()}; batch = {"input_ids": [[1, 2]], "requirements": []}
        calls = []
        def check(m, device, pop, identity, band, tok):
            calls.append((m, device, pop, identity, band, tok))
            if mutate:
                with torch.no_grad(): model.model.layers[35].mlp.down_proj.weight[0, 0] += 1
            return {"verdict": "INERT", "control_equal": True, "telemetry_equal": True,
                    "probe_forwards": 3, "lens_forwards": 2}
        B = _types.SimpleNamespace(population_and_batch=lambda h, templates: (population, batch),
            TEMPLATES=["{}", "a. {}", "b. {}", "c. {}", "d. {}", "e. {}"],
            environment_identity=lambda: dict(env), write_record=lambda path, record: self.D.write_json(path, record, replace=True))
        fp = _types.SimpleNamespace(main=lambda: 0)
        with mock.patch.object(self.C, "arms_module", return_value=self.D), \
             mock.patch.object(self.C, "benchmark_module", return_value=B), \
             mock.patch.object(self.C, "fingerprint_module", return_value=fp), \
             mock.patch.object(self.D, "telemetry_mps_inertness_check", check), \
             mock.patch.dict(os.environ, {"LLMDB_DEVICE": "mps"}, clear=True):
            rc = self.C.run(out, H)
        return rc, json.loads((out / "inertness.json").read_text()), calls, spies, source_paths, env

    def test_runner_roundtrip_identity_and_no_write_engine_calls(self):
        rc, record, calls, spies, source_paths, env = self.runner_case()
        self.assertEqual(rc, 0); self.assertEqual(record["schema"], "c10z_astra_telemetry_inertness/v1")
        self.assertEqual((record["decision_id"], record["device"], record["verdict"]), ("D-C10r-rulings-11", "mps", "INERT"))
        self.assertEqual(record["weights_unchanged"], True)
        self.assertEqual(record["sources"], {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest() for p in source_paths})
        self.assertEqual(record["env"], dict(env, model_rev="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"))
        self.assertEqual(record, json.loads(json.dumps(record, sort_keys=True, allow_nan=False)))
        self.assertEqual(calls[0][1], "mps"); self.assertEqual(calls[0][4], [4, 5, 6, 7, 8])
        for spy in spies.values(): self.assertEqual(spy.call_count, 0)

    def test_runner_checks_all36_weights_and_invalid_is_exit2(self):
        rc, record, *_ = self.runner_case(mutate=True)
        self.assertEqual(rc, 2); self.assertEqual(record["verdict"], "INVALID"); self.assertFalse(record["weights_unchanged"])


def _telemetry_suite():
    return unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(cls)
        for cls in (TelemetryUnitTests, TelemetryInertnessTests, TelemetryRunnerTests)])


def _build_suite():
    suite=_fix2_suite()
    for cls in (IdleGapTests,BudgetBoundTests,LaunchBindingTests,ReaderBindingTests,WrapperTests,PinTests,TelemetryIntegrationTests):
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    suite.addTests(_telemetry_suite())
    return suite


if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(_build_suite())
    assert "c10e_bandknob" not in sys.modules
    print("C10Z_ASTRA_SELFTEST_"+("PASS" if result.wasSuccessful() else "FAIL")+" tests="+str(result.testsRun))
    sys.exit(0 if result.wasSuccessful() else 1)
