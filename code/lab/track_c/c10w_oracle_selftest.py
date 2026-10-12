#!/usr/bin/env python3
"""Model-free, prereg-derived tests for D-C10w-oracle (oracle measurement, not a route).

All line citations below refer to experiments/c10w/design/C10W_ORACLE_PREREG.md at fb1788b.
Fixtures are synthetic records, never scientific evidence. Tensor regression uses CPU only.
The suite imports copied sources under a temporary root; the live artifact trees are guarded.
"""
import ast
import copy
import contextlib
import os
import shutil
import importlib
import importlib.abc
import io
import json
import random
import subprocess
import sys
import tempfile
import unittest
import types
from pathlib import Path
from unittest.mock import patch

LIVE_ROOT = Path(__file__).resolve().parents[2]
ROOT = LIVE_ROOT
HERE = Path(__file__).resolve().parent
LIVE_BEFORE = None
HASH = "a" * 64
R = S = T = E = None


class NoModelImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"torch", "transformers", "datasets", "tokenizers", "safetensors", "numpy"}:
            raise AssertionError("model-free test attempted forbidden import: " + fullname)


def frame(flips=1):
    return {"n":6,"flips":flips,"rows":[{"subj":str(i),"top1":i,"tok":str(i),"flip":i<flips} for i in range(6)]}


def mmlu(lost=0):
    correct=[False]*lost+[True]*(100-lost)+[False]*100
    predicted=["A" if hit else "B" for hit in correct]
    return {"n":200,"correct":correct,"predicted":predicted,"correct_n":sum(correct),"accuracy":sum(correct)/200.,
            "correct_to_wrong":lost,"wrong_to_correct":0,"net_paired_loss":lost,
            "rows":[{"source_index":i,"predicted":predicted[i],"correct":hit} for i,hit in enumerate(correct)]}


def mounted_score(count):
    return {"para_full_n":count,"para_string_n":count,"para_n":72,
            "rows":[{"subj":str(i),"para_full_hits":[3*i+j<count for j in range(3)],
                     "para_string_hits":[3*i+j<count for j in range(3)]} for i in range(24)]}


def arm(count=61, canon=24, first=None):
    first = max(count, 65 if first is None else first)
    rows = [{"subj": str(i), "val": "head modifier", "ntok": 5,
             "canon_full": i < canon, "canon_first": i < canon,
             "para_full_hits": [3*i+j < count for j in range(3)],
             "para_first_hits": [3*i+j < first for j in range(3)],
             "para_string_hits": [3*i+j < count for j in range(3)],
             "tf_correct": 12, "tf_total": 12} for i in range(24)]
    return {"canon_n": 24, "para_n": 72, "canon_full_n": canon,
            "para_full_n": count, "para_first_n": first, "para_string_n": count,
            "tf_pertok_cont": 100.0, "cond_full_given_first": round(count/first, 3) if first else None,
            "locality_described_as": 98.5,
            "locality_axes": {"L1_n": 12, "L1_flipped_to_edited_value": 1,
                              "L3_n": 30, "L3_top1_agree": 30,
                              "generic_ppl_pre": 20.0, "generic_ppl_post": 20.0,
                              "L1_pre_already_edited_token":0,"L1_top1_changed":1,"L1_js_locpct":100.,
                              "L3_mean_kl":0.,"L3_js_locpct":100.,"L1_post_top1":{}},
            "extra": {"frames": {"canon":frame(),"train":[frame() for _ in range(20)],"heldout":[frame() for _ in range(3)]},
                      "mmlu": mmlu(),
                      "relations": {s: {"n": 24, "flips": 0, "pre": [1]*24, "post": [1]*24}
                                    for s in ("is_a", "associated_with")},
                      "bigram": {"eligible_n": 24, "excluded_n": 0,
                                 "rows": [{"eligible": True, "c": 0, "s": 0, "b": 0, "n": 0.0} for _ in range(24)]},
                      "contains_n": count, "contains_hits": [r["para_full_hits"] for r in rows],
                      "mounted": mounted_score(count),
                      "cross_score": {"para_full_n": 0,"para_string_n":0,"para_n": 72},
                      "cross_detail": [{"subj":str(i),"para_full_hits":[False]*3,"para_string_hits":[False]*3} for i in range(24)],
                      "geometry": {str(i): {"delta_norm":1.,"trace_delta_cov_deltaT":1.,"null_cov_share":1.,
                                             "application_relative_error":0.,"delta_sha256":HASH} for i in range(4,9)},
                      "write_size_ratio_to_closedform_A7":1.,
                      "sibling": {"misses": 72-count, "emissions": 0}}, "_rows": rows}


def recipe(arms):
    return {"band": [4, 5, 6, 7, 8], "law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0},
            "arms": {k: {x: y for x, y in v.items() if x != "_rows"} for k, v in arms.items()},
            "detail": {k: v["_rows"] for k, v in arms.items()},
            "band_after_hash":{str(i):HASH for i in range(4,9)},
            "restored": True, "wall_seconds": 1.0}


def train(tag, phase):
    specs = {"A1": "A1_single", "A2": "A2_coherent2", "A7": "A7_coined_coined",
             "shuf": "A7_shuf", "canon": "A7_canon"}
    kind, seed, rank, rt = tag
    n = 24 if kind == "canon" else 480
    return {"class": R.CLASS, "decision_id": R.DECISION_ID, "status": "PASS",
            "arm": specs[kind], "seed": seed, "rank": rank, "retrain": rt,
            "steps": 400, "fit": {"correct": n, "n": n}, "phase": phase,
            "frozen_parameters_unchanged": True, "model_id": R.MODEL_ID,
            "frozen_parameter_hashes_before":{"synthetic.weight":HASH},"frozen_parameter_hashes_after":{"synthetic.weight":HASH},
            "model_revision": R.MODEL_REV, "layers": list(R.BAND), "dtype": "float32", "device": "mps",
            "adapter": {"path": "synthetic.safetensors", "sha256": HASH},
            "provenance": {"train_inputs": HASH, "trainer_source": HASH, "mmlu200": HASH,
                           "templates": R.TEMPLATE_SHA, "prereg": R.PREREG_SHA},
            "wall_seconds": 1.0, "sampled_peak_driver_bytes": 1}


def phase(name, count=61, canon_count=30):
    if name == "P1":
        tags = [("A1",0,16,False),("A7",0,16,False),("canon",0,16,False),("A2",0,16,False),("shuf",0,16,False)]
        names = {"oracle_p1": {"A1_single": arm(68), "A2_coherent2": arm(68),
                               "A7_coined_coined": arm(count), "A7_shuf": arm(count)},
                 "oracle_canon_s0": {"A7_canon": arm(canon_count)}}
    elif name == "P2":
        tags = [("A7",1,16,False),("shuf",1,16,False),("canon",1,16,False),
                ("A1",1,16,False),("A7",0,16,True),("shuf",0,16,True)]
        names = {"oracle_s1": {"A1_single": arm(68), "A7_coined_coined": arm(count), "A7_shuf": arm(count)},
                 "oracle_s0rt": {"A7_coined_coined": arm(count), "A7_shuf": arm(count)},
                 "oracle_canon_s1": {"A7_canon": arm(canon_count)}}
    else:
        tags = [("A7",0,64,False),("shuf",0,64,False),("A7",1,64,False),("shuf",1,64,False)]
        names = {"oracle_r64_s0": {"A7_coined_coined": arm(count), "A7_shuf": arm(count)},
                 "oracle_r64_s1": {"A7_coined_coined": arm(count), "A7_shuf": arm(count)}}
    names = {"closedform": {"A1_single": arm(68), "A2_coherent2": arm(68),
                            "A7_coined_coined": arm(12, 8, 55)}, **names}
    result={"class": R.CLASS, "decision_id": R.DECISION_ID, "phase": name, "status": "PASS",
            "environment": {"model_id": R.MODEL_ID, "model_revision": R.MODEL_REV,
                            "layers": list(R.BAND), "dtype": "float16", "device": "mps"},
            "validity": {k: True for k in ("fingerprint", "seal", "instrument", "hashes", "entry", "seam")},
            "provenance": {"train_inputs": HASH, "trainer_source": HASH, "mmlu200": HASH,
                           "templates": R.TEMPLATE_SHA, "prereg": R.PREREG_SHA},
            "u": {k: {x: y for x,y in arm(0,0,0).items() if x != "_rows"}
                  for k in ("A1_single", "A2_coherent2", "A7_coined_coined", "A7_shuf")},
            "u_detail": {k: arm(0,0,0)["_rows"] for k in ("A1_single", "A2_coherent2", "A7_coined_coined", "A7_shuf")},
            "stimulus": {k: {"base": 0} for k in ("A1_single", "A2_coherent2", "A7_coined_coined", "A7_shuf")},
            "law5_null": {"ok": True, "weights_identical": True, "counts_identical": True,
                          "probes_identical": True, "ppl_delta": 0.0, "described_as": 100.0},
            "delegation_identity": True, "zero_adapter_hits": 1, "trained_oracle_hits": len(tags),
            "expected_zero_hits": 1, "expected_trained_hits": len(tags),
            "base_band_hash":{str(i):HASH for i in range(4,9)},"final_band_hash":{str(i):HASH for i in range(4,9)},
            "recipes": {k: recipe(v) for k,v in names.items()},
            "train_records": [train(t,name) for t in tags], "wall_seconds": 1.0,
            "sampled_peak_driver_bytes": 1,
            "same_seed": {"per_layer_cosine": {str(i): 1.0 for i in R.BAND}, "prompt_agreement_n": 72, "n": 72}}
    for a in result["u"].values(): a["locality_described_as"]=100.
    result["law5_null"].update(arm=copy.deepcopy(result["u"]["A7_coined_coined"]),
                               rows=copy.deepcopy(result["u_detail"]["A7_coined_coined"]),
                               base_hash={str(i):HASH for i in R.BAND},after_hash={str(i):HASH for i in R.BAND})
    return result


def fixture(c16=61, c64=None, canon_count=30):
    result = {p: phase(p,c16,canon_count) for p in ("P1","P2")}
    if c64 is not None:
        result["P3"] = phase("P3",c64,canon_count)
    return result


def preflight():
    raw=phase("P1")
    raw["recipes"]={"closedform":raw["recipes"]["closedform"]}
    raw.update(trained_oracle_hits=0,expected_trained_hits=0,train_records=[])
    return raw


def candidates(data, include_canon=False):
    for p in data.values():
        for name,r in p["recipes"].items():
            if name.startswith("oracle_"):
                for key,a in r["arms"].items():
                    if key == "A7_coined_coined" or (include_canon and key == "A7_canon"):
                        yield a


def replace_arm(data, phase_name, recipe_name, arm_name, value):
    rec = data[phase_name]["recipes"][recipe_name]
    rec["arms"][arm_name] = {k:v for k,v in value.items() if k != "_rows"}
    rec["detail"][arm_name] = value["_rows"]


class OracleTests(unittest.TestCase):
    def read(self, data):
        return R.read_measurement(data)

    def test_configuration_labels_and_integer_count_boundaries(self):
        """§3 lines 359–368: every label, 29/30 and 60/61, through real reader."""
        for n,label in ((29,"FAIL-CEILING"),(30,"PARTIAL-CEILING"),(60,"PARTIAL-CEILING"),(61,"PASS-CEILING")):
            with self.subTest(n=n):
                d=fixture(n,n if n < 61 else None)
                self.assertEqual(self.read(d)["final_label"],label)
                self.assertEqual(self.read(d)["ranks"]["16"]["count"],n)
        d=fixture()
        for a in candidates(d): a["locality_axes"]["L3_top1_agree"]=28
        v=self.read(d)
        self.assertEqual(v["final_label"],"PARTIAL-CEILING-LOCALITY-COST")
        self.assertIn("G2",v["ranks"]["16"]["gate_misses"])
        self.assertFalse(v["p3_required"])
        d["P1"]["validity"]["seal"]=False
        self.assertEqual(self.read(d)["status"],"INVALID")

    def test_all_final_label_table_rows(self):
        """§3 lines 374–384: every row, including both PARTIAL/FAIL antecedents."""
        for c16 in (29,30):
            for c64,want in ((29,"FAIL-CEILING" if c16==29 else "PARTIAL-CEILING"),
                              (30,"PARTIAL-CEILING"),(61,"PASS-CEILING")):
                d=fixture(c16,c64)
                self.assertEqual(self.read(d)["final_label"],want)
            d=fixture(c16,61)
            for name,rec in d["P3"]["recipes"].items():
                if name.startswith("oracle"):
                    rec["arms"]["A7_coined_coined"]["locality_axes"]["L3_top1_agree"]=28
            self.assertEqual(self.read(d)["final_label"],"PARTIAL-CEILING-LOCALITY-COST")
            d=fixture(c16)
            self.assertIsNone(self.read(d)["final_label"])
            self.assertTrue(self.read(d)["p3_required"])
            for defect in ("invalid","unstable"):
                d=fixture(c16,30)
                if defect=="invalid": d["P3"]["validity"]["instrument"]=False
                else: replace_arm(d,"P3","oracle_r64_s1","A7_coined_coined",arm(46))
                self.assertIsNone(self.read(d)["final_label"])
        d=fixture(); del d["P2"]
        self.assertIsNone(self.read(d)["final_label"])
        self.assertIsNone(self.read(d)["routing"])

    def test_routing_every_row_and_canonical_split(self):
        """§3 lines 388–397: PASS(a,b,c), PARTIAL(a,b,c), FAIL, no routing."""
        for count in (61,30):
            for canon,split in ((29,"b"),(30,"a")):
                d=fixture(count,count if count<61 else None,canon)
                v=self.read(d)
                self.assertEqual(v["canon_split"],split)
                self.assertEqual(v["reference_count"],canon)
                self.assertEqual(v["routing"]["h30_eligible"],count>=61)
            d=fixture(count,count if count<61 else None)
            candidates_canon=[a for p in d.values() for n,r in p["recipes"].items()
                              for k,a in r["arms"].items() if k=="A7_canon"]
            for a in candidates_canon: a["locality_axes"]["L3_top1_agree"]=28
            v=self.read(d); self.assertEqual(v["canon_split"],"c")
            self.assertEqual(v["reference_count"],None if count>=61 else count)
        d=fixture(29,29); v=self.read(d)
        self.assertEqual(v["routing"]["action"],"OPERATOR-CEILING-RULING")
        self.assertIsNone(v["reference_count"])
        d=fixture(); d["P1"]["validity"]["hashes"]=False
        self.assertIsNone(self.read(d)["routing"])

    def test_no_gate_clean_reference_and_locality_cost_never_p3(self):
        """§3 lines 372,395: empty clean rank set -> null, never costly substitution."""
        d=fixture()
        for a in candidates(d,True): a["locality_axes"]["L3_top1_agree"]=28
        v=self.read(d)
        self.assertFalse(v["p3_required"])
        self.assertIsNone(v["reference_count"])
        self.assertEqual(v["reference_status"],"NO-GATE-CLEAN-REFERENCE")
        d=fixture(30,50)
        for p in d.values():
            for r in p["recipes"].values():
                if "A7_canon" in r["arms"]: r["arms"]["A7_canon"]["locality_axes"]["L3_top1_agree"]=28
        self.assertEqual(self.read(d)["reference_count"],50)

    def test_G1_to_G7_both_sides(self):
        """§3 lines 351–368: equality passes for every locality/forgetting boundary."""
        cases=[("G1",lambda a,v:a["locality_axes"].update(L1_flipped_to_edited_value=v),2,3),
               ("G2",lambda a,v:a["locality_axes"].update(L3_top1_agree=v),29,28),
               ("G3",lambda a,v:a.update(locality_described_as=v),95.5,95.49),
               ("G4",lambda a,v:a["extra"]["frames"].update(canon=frame(v)),2,3),
               ("G5",lambda a,v:a["locality_axes"].update(generic_ppl_post=v),20.5,20.501),
               ("G6",lambda a,v:a["extra"].update(mmlu=mmlu(v)),4,5)]
        for gate,setter,yes,no in cases:
            for value,passes in ((yes,True),(no,False)):
                d=fixture()
                for a in candidates(d): setter(a,value)
                v=self.read(d)
                self.assertEqual(gate not in v["ranks"]["16"]["gate_misses"],passes,(gate,value))
        for index in range(20):
            for flips,passes in ((2,True),(3,False)):
                d=fixture()
                for a in candidates(d): a["extra"]["frames"]["train"][index]=frame(flips)
                self.assertEqual("G4" not in self.read(d)["ranks"]["16"]["gate_misses"],passes)
        for cross,passes in ((2,True),(3,False)):
            d=fixture()
            for p in d.values():
                for n,r in p["recipes"].items():
                    if n.startswith("oracle") and "A7_shuf" in r["arms"]:
                        r["arms"]["A7_shuf"]["extra"]["cross_score"]["para_full_n"]=cross
                        r["arms"]["A7_shuf"]["extra"]["cross_score"]["para_string_n"]=cross
                        r["arms"]["A7_shuf"]["extra"]["cross_detail"][0]["para_full_hits"]=[j<cross for j in range(3)]
                        r["arms"]["A7_shuf"]["extra"]["cross_detail"][0]["para_string_hits"]=[j<cross for j in range(3)]
            self.assertEqual("G7" not in self.read(d)["ranks"]["16"]["gate_misses"],passes)

    def test_law3_envelope_all_endpoints_and_controls(self):
        """§2.7 lines 241–245: inclusive 4/5/18/19,4/5/10/11,41/42/59/60,67/68."""
        for key,values,lo,hi in (("para_full_n",(4,5,18,19),5,18),
                                 ("canon_full_n",(4,5,10,11),5,10),
                                 ("para_first_n",(41,42,59,60),42,59)):
            for value in values:
                d=fixture(); x=arm(12,8,55)
                if key=="para_full_n": x=arm(value,8,55)
                elif key=="canon_full_n": x=arm(12,value,55)
                else: x=arm(12,8,value)
                replace_arm(d,"P1","closedform","A7_coined_coined",x)
                self.assertEqual(self.read(d)["status"]!="INVALID",lo<=value<=hi,(key,value))
        for p in ("P1","P2"):
            for name in ("A1_single","A2_coherent2"):
                for value in (67,68):
                    d=fixture(); replace_arm(d,p,"closedform",name,arm(value))
                    self.assertEqual(self.read(d)["status"]!="INVALID",value>=68)
        for p,rec,key in (("P1","oracle_p1","A1_single"),("P1","oracle_p1","A2_coherent2"),
                          ("P2","oracle_s1","A1_single")):
            d=fixture(); replace_arm(d,p,rec,key,arm(67))
            self.assertEqual(self.read(d)["status"],"INVALID")

    def test_stimulus_law5_strict_restore_delegation_and_counters(self):
        """§2.7 lines 245,249–255: strict LAW5 and exact process manifest counters."""
        for key,yes,no in (("expr_delta",0.0499,0.05),("loc_delta",2.99,3.0)):
            for value,passes in ((yes,True),(no,False)):
                d=fixture(); d["P1"]["recipes"]["oracle_p1"]["law5_gate"][key]=value
                self.assertEqual(self.read(d)["status"]!="INVALID",passes)
        for key in ("delegation_identity","zero_adapter_hits","trained_oracle_hits"):
            d=fixture(); d["P1"][key]=False if key=="delegation_identity" else 999
            self.assertEqual(self.read(d)["status"],"INVALID")
        d=fixture(); d["P1"]["recipes"]["oracle_canon_s0"]["restored"]=False
        self.assertEqual(self.read(d)["status"],"INVALID")
        for key in ("weights_identical","counts_identical","probes_identical"):
            d=fixture(); d["P1"]["law5_null"][key]=False
            self.assertEqual(self.read(d)["status"],"INVALID")
        for n,passes in ((3,True),(4,False)):
            d=fixture(); d["P1"]["stimulus"]["A1_single"]["base"]=n
            self.assertEqual(self.read(d)["status"]!="INVALID",passes)
        for n,passes in ((2,True),(3,False)):
            d=fixture(); x=arm(n,0,n); x["locality_described_as"]=100.
            d["P1"]["u"]["A7_coined_coined"]={k:v for k,v in x.items() if k!="_rows"}
            d["P1"]["u_detail"]["A7_coined_coined"]=x["_rows"]
            d["P1"]["law5_null"].update(arm=copy.deepcopy(d["P1"]["u"]["A7_coined_coined"]),rows=copy.deepcopy(x["_rows"]))
            self.assertEqual(self.read(d)["status"]!="INVALID",passes)

    def test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate(self):
        """§2.7 line250: every per-prompt hit must match, even with equal aggregate counts."""
        d=fixture()
        d["P1"]["law5_null"]["rows"][0]["para_first_hits"][0]=True
        self.assertEqual(self.read(d)["status"],"INVALID")
        u=arm(1,0,1); u["locality_described_as"]=100.
        z=copy.deepcopy(u)
        z["_rows"][0]["para_full_hits"][0]=False
        z["_rows"][0]["para_full_hits"][1]=True
        with self.assertRaises(R.Halt): E.compare_null(u,z,u["_rows"],z["_rows"])

    def test_recipe_delegation_keeps_original_engine_gradient_context(self):
        """§2.5,2.7 lines197,249,252: unchanged engine-parity recipe, including compute_z gradients."""
        grad=[True]
        class NoGrad:
            def __enter__(self): grad[0]=False
            def __exit__(self,*args): grad[0]=True
        h=types.SimpleNamespace(_LAW5_DEFAULT_CTX=False,_ARM_STATE=None)
        def original(*args):
            self.assertTrue(grad[0],"closed-form delegation disabled the engine's latent optimisation gradients")
            return {}
        h.my_edit=original
        def recipe(name,path):
            h.my_edit(None,[],None,None)
            return {"law5_gate":{"ok":True},"arms":{},"detail":{}}
        h.run_recipe=recipe; h.HP_BASE="synthetic"; h.ARM_HOOKS=[]
        e=object.__new__(E.Evaluator); e.H=h; e.original=original; e.maps={}
        e.torch=types.SimpleNamespace(no_grad=NoGrad); e.wrapper=E.OracleEdit(h,lambda:None,lambda *args:{})
        h.my_edit=e.wrapper
        e.restore=e.assert_base=lambda:None; e.guard=lambda label:None; e.band_hash=lambda:{}
        e.unit_times={"recipe_setup_seconds":[],"closedform_arm_seconds":[],"oracle_arm_seconds":[]}
        e.run_recipe("closedform",(),{})

    def test_replication_minimum_seed_and_same_seed_boundaries(self):
        """§3 lines 368–370: min-of-two,15/16,10/11,band and each gate crossing."""
        d=fixture(61); replace_arm(d,"P2","oracle_s1","A7_coined_coined",arm(60))
        d["P3"]=phase("P3",30)
        self.assertEqual(self.read(d)["ranks"]["16"]["count"],60)
        for gap,unstable in ((15,False),(16,True)):
            d=fixture(30,30); replace_arm(d,"P2","oracle_s1","A7_coined_coined",arm(30+gap))
            self.assertEqual(self.read(d)["status"]=="UNSTABLE",unstable)
        for gap,unstable in ((10,False),(11,True)):
            d=fixture(30,30); replace_arm(d,"P2","oracle_s0rt","A7_coined_coined",arm(30+gap))
            self.assertEqual(self.read(d)["status"]=="UNSTABLE",unstable)
        d=fixture(30,30); replace_arm(d,"P2","oracle_s0rt","A7_coined_coined",arm(29))
        self.assertEqual(self.read(d)["status"],"UNSTABLE")
        d=fixture(); d["P2"]["recipes"]["oracle_s0rt"]["arms"]["A7_coined_coined"]["locality_axes"]["L3_top1_agree"]=28
        self.assertEqual(self.read(d)["status"],"UNSTABLE")
        d=fixture(61); d["P2"]["recipes"]["oracle_s1"]["arms"]["A7_coined_coined"]["locality_axes"]["L3_top1_agree"]=28
        self.assertEqual(self.read(d)["final_label"],"PARTIAL-CEILING-LOCALITY-COST")

    def test_fit_matched_controls_steps_and_provenance(self):
        """§2.2,2.4,3 lines54,186,331–345: own fit, exact matching, incomplete INVALID."""
        for kind,yes,no in (("A7_coined_coined",456,455),("A7_canon",23,22),("A7_shuf",456,455)):
            for value,passes in ((yes,True),(no,False)):
                d=fixture()
                for tr in d["P1"]["train_records"]:
                    if tr["arm"]==kind: tr["fit"]["correct"]=value
                self.assertEqual(self.read(d)["status"]!="INVALID",passes)
        for defect in ("missing","seed","rank","steps","data","frozen"):
            d=fixture(); p=d["P1"]; tr=next(t for t in p["train_records"] if t["arm"]=="A7_shuf")
            if defect=="missing": p["train_records"].remove(tr)
            elif defect=="data": tr["provenance"]["train_inputs"]="b"*64
            elif defect=="frozen": tr["frozen_parameters_unchanged"]=False
            else: tr[defect] = {"seed":1,"rank":64,"steps":800}[defect]
            self.assertEqual(self.read(d)["status"],"INVALID",defect)

    def test_bigram_pairing_retry_and_merge_loss_qualifiers(self):
        """§2.6,3 lines230,232,236,365–370: exact qualifier thresholds and exception."""
        for matched,qualifies in ((15,False),(16,True)):
            d=fixture(30,30)
            replace_arm(d,"P1","oracle_p1","A7_shuf",arm(30+matched))
            self.assertEqual("PAIRING-SPECIFIC" in self.read(d)["ranks"]["16"]["qualifiers"],qualifies)
        for x,qualified in ((1,False),(2,True)):
            d=fixture()
            for a in candidates(d):
                rows=a["extra"]["bigram"]["rows"]
                for row in rows[:3]: row["c"]=1
                for row in rows[:x]: row["s"]=1
            self.assertEqual("BIGRAM" in self.read(d)["ranks"]["16"]["qualifiers"],qualified)
        self.assertEqual(R.bigram_qualifier({"eligible_n":0,"excluded_n":24,"rows":[]}),"NOT-EVALUABLE")
        for gap,unstable in ((5,False),(6,True)):
            d=fixture(30,30)
            for a in candidates(d): a["extra"]["mounted"]=mounted_score(30+gap)
            self.assertEqual(self.read(d)["status"]=="UNSTABLE",unstable)
        for mounted,unstable in ((67,False),(55,True)):
            d=fixture()
            for a in candidates(d): a["extra"]["mounted"]=mounted_score(mounted)
            self.assertEqual(self.read(d)["status"]=="UNSTABLE",unstable)
        d=fixture()
        for p in d.values():
            for tr in p["train_records"]: tr["steps"]=800
        self.assertIn("RETRY800",self.read(d)["ranks"]["16"]["qualifiers"])

    def test_canonical_read_conditions_and_merge_loss(self):
        """§3 line388: canonical seed gap, fit, G1–G6 and merge gap, no exception."""
        for n,split in ((45,"a"),(46,"c")):
            d=fixture(); replace_arm(d,"P2","oracle_canon_s1","A7_canon",arm(n))
            self.assertEqual(self.read(d)["canon_split"],split)
        for gap,split in ((5,"a"),(6,"c")):
            d=fixture(); d["P1"]["recipes"]["oracle_canon_s0"]["arms"]["A7_canon"]["extra"]["mounted"]=mounted_score(30+gap)
            self.assertEqual(self.read(d)["canon_split"],split)

    def test_required_metrics_counts_finiteness_and_denominators(self):
        """§3 lines342–345: missing/nonfinite/incorrect denominators never pass."""
        for defect in ("missing","nan","denom","rows","string","mmlu","frames"):
            d=fixture(); a=d["P1"]["recipes"]["oracle_p1"]["arms"]["A7_coined_coined"]
            if defect=="missing": del a["locality_described_as"]
            elif defect=="nan": a["locality_described_as"]=float("nan")
            elif defect=="denom": a["para_n"]=71
            elif defect=="rows": d["P1"]["recipes"]["oracle_p1"]["detail"]["A7_coined_coined"][0]["para_full_hits"][0]=False
            elif defect=="string": a["para_string_n"]=60
            elif defect=="mmlu": a["extra"]["mmlu"]["correct"].pop()
            else: a["extra"]["frames"]["train"].pop()
            self.assertEqual(self.read(d)["status"],"INVALID",defect)
        for key in ("geometry","write_size_ratio_to_closedform_A7"):
            d=fixture(); del d["P1"]["recipes"]["oracle_p1"]["arms"]["A7_coined_coined"]["extra"][key]
            self.assertEqual(self.read(d)["status"],"INVALID",key)
        d=fixture(); del d["P2"]["same_seed"]
        self.assertEqual(self.read(d)["status"],"INVALID")

    def test_training_schedule_exact_seed_steps_warmup_and_fit(self):
        """§2.4 lines181–186: N-specific epochs,1000*seed+epoch,400/800 updates."""
        for n,epochs in ((480,20),(24,400)):
            batches=list(T.training_batches(n,1,400))
            self.assertEqual(len(batches),400)
            self.assertTrue(all(len(b)==24 for b in batches))
            per_epoch=n//24
            for epoch in (0,1,epochs-1):
                order=list(range(n)); random.Random(1000+epoch).shuffle(order)
                observed=sum(batches[epoch*per_epoch:(epoch+1)*per_epoch],[])
                self.assertEqual(observed,order)
            self.assertEqual(len(list(T.training_batches(n,0,800))),800)
        self.assertEqual(T.learning_rate(0),0.0)
        self.assertEqual(T.learning_rate(20),3e-4)
        self.assertEqual(T.learning_rate(399),3e-4)
        for n,yes,no in ((480,456,455),(24,23,22)):
            self.assertTrue(T.fit_passes(yes,n)); self.assertFalse(T.fit_passes(no,n))

    def test_seal_real_constants_S1_to_S6_and_shuffled_map(self):
        """§2.2,2.3 lines52,70–104,106,264–266: real constants without importing H."""
        c=S.source_constants(ROOT)
        audit=S.audit_templates(c, S.TEMPLATES, S.RESERVES)
        self.assertTrue(audit["ok"],audit)
        self.assertEqual(R.sha_text("\n".join(S.TEMPLATES)),R.TEMPLATE_SHA)
        self.assertEqual(R.sha_text("\n".join(S.RESERVES)),"42c461ed17efb89af1d56c3a4e2bc1e5fdf3bd96bbe455f0ff4e2ab55efd6e2c")
        values={s:c["heads"][(i*2+1)%24]+" "+c["modifiers"][(i*3+2)%24] for i,s in enumerate(c["fiction"])}
        shuffled=S.shuffled_map(c["fiction"],values)
        self.assertEqual(set(shuffled.values()),set(values.values()))
        for i,s in enumerate(c["fiction"]):
            self.assertEqual(shuffled[s],values[c["fiction"][(i+1)%24]])
            self.assertTrue(all(x!=y for x,y in zip(shuffled[s].split(),values[s].split())))
        bad=dict(values); bad[c["fiction"][1]]=bad[c["fiction"][0]]
        with self.assertRaises(R.Halt): S.shuffled_map(c["fiction"],bad)
        for text in (c["heldout"][0],"For {}, the capital is","The capital of the nation of {} is",
                     "Zorbland has the capital {}","{} is described as"):
            self.assertFalse(S.audit_templates(c,[text],[])["ok"],text)
        trainer=(HERE/"c10w_oracle_train.py").read_text()
        self.assertNotIn("PTEST",trainer); self.assertNotIn("c10e_bandknob",trainer)
        S.audit_trainer_input(json.dumps({"templates":S.TEMPLATES}),trainer,c["heldout"])
        for text in c["heldout"]:
            with self.assertRaises(R.Halt): S.audit_trainer_input(json.dumps({"template":text}),trainer,c["heldout"])

    def test_entry_preflight_and_training_provenance_precede_model_load(self):
        """§2.5,2.7 lines192–194,241,260: no inherited knob or mismatched certificate."""
        for knob in R.FORBIDDEN_ENV:
            with self.assertRaises(R.Halt): R.entry_preflight({knob:""},ROOT)
        with self.assertRaises(R.Halt): R.entry_preflight({"LLMDB_ROOT":"/workspace"},ROOT)
        R.entry_preflight({"LLMDB_ROOT":str(ROOT)},ROOT)
        raw=preflight(); provenance=raw["provenance"]
        probe_hash=R.sha_text(str((raw["u_detail"][R.A7],raw["u"][R.A7]["extra"])))
        band_hash=R.sha_text(str(raw["law5_null"]["base_hash"]))
        proof={"phase":"P1","status":"PASS","law3":True,"law5_null":True,"fingerprint":True,
               "step0_sha256":HASH,"provenance":provenance,
               "law3_counts":{"A1":68,"A2":68,"para_full":12,"canon_full":8,"para_first":55,"u_para_full":0,"stimulus":[0]*4},
               "law5_standing":{"ok":True,"expr_delta":0.,"loc_delta":0.},
               "null_evidence":{"base_hash":band_hash,"after_hash":band_hash,"u_hit_probe_sha256":probe_hash,"zero_hit_probe_sha256":probe_hash,
                                "ppl_delta":0.,"described_as":100.}}
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"preflight_eval.json"; R.write_json(source,raw)
            proof["evaluation"]=R.file_ref(source)
            T.require_training_preflight(proof,HASH,provenance)
            for key in ("law3","law5_null","fingerprint","status","step0_sha256","provenance"):
                p=copy.deepcopy(proof)
                p[key]={"train_inputs":"b"*64} if key=="provenance" else "bad" if key in ("status","step0_sha256") else False
                with self.assertRaises(R.Halt): T.require_training_preflight(p,HASH,provenance)
            p=copy.deepcopy(proof); p["law3_counts"]["A1"]=67
            with self.assertRaises(R.Halt): T.require_training_preflight(p,HASH,provenance)
            for name in ("P2","P3"):
                p=copy.deepcopy(proof); p["phase"]=name
                with self.assertRaises(R.Halt): T.require_training_preflight(p,HASH,provenance)
            for bad in ({"evidence":"unrelated"},preflight()):
                if "recipes" in bad:
                    replace_arm({"P1":bad},"P1","closedform",R.A1,arm(67))
                bad_path=Path(td)/("bad"+str(len(bad))+".json"); R.write_json(bad_path,bad)
                p=copy.deepcopy(proof); p["evaluation"]=R.file_ref(bad_path)
                with self.assertRaises(R.Halt): T.require_training_preflight(p,HASH,provenance)
            source.write_text("tampered")
            with self.assertRaises(R.Halt): T.require_training_preflight(proof,HASH,provenance)
        with self.assertRaises(R.Halt): T.require_training_preflight(None,HASH,{"train_inputs":HASH})

    def test_retries_charged_before_each_fresh_process(self):
        """§2.2,2.9 lines54,312,314–316: full retry and forced mate cost before spending."""
        proof={"wall_seconds":85*60}
        one={"arm":R.A1,"seed":0,"rank":16,"retrain":False,"steps":400,"status":"PASS","wall_seconds":38*60}
        unit=(R.A7,0,16,False)
        self.assertEqual(S.training_projection("P1",proof,[one],{unit:400}),465.)
        failed={"arm":R.A7,"seed":0,"rank":16,"retrain":False,"steps":400,"status":"INVALID-UNDERFIT","wall_seconds":38*60}
        projected=S.training_projection("P1",proof,[one,failed],{unit:800})
        self.assertGreater(projected,465.)
        with self.assertRaises(R.Halt): R.check_phase_minutes("P1",projected)
        mate=(R.SHUF,0,16,False)
        self.assertGreater(S.training_projection("P1",proof,[one,failed],{unit:800,mate:800}),projected)

    def test_eval_seam_order_missing_adapter_and_hit_counters(self):
        """§2.5,2.7 lines198–203,241,253: trained dispatch gated before application."""
        applied=[]
        original=lambda *args: {"delegated":True}
        h=type("H",(),{"my_edit":staticmethod(original),"_LAW5_DEFAULT_CTX":False})()
        e=E.OracleEdit(h,lambda:None,lambda adapter,hp:applied.append(adapter) or {})
        req=[{"subject":"s","target_new":{"str":" value"}}]
        e.mode="oracle"; e.registry[frozenset({("s"," value")})]={"zero":False}
        for null,law3 in ((False,False),(True,False),(False,True)):
            e.null_passed=null; e.law3_passed=law3
            with self.assertRaises(R.Halt): e(None,req,None,None)
        self.assertEqual(applied,[])
        e.null_passed=e.law3_passed=True
        e(None,req,None,None); self.assertEqual(e.trained_hits,1)
        h._LAW5_DEFAULT_CTX=True
        self.assertEqual(e(None,req,None,None),{"delegated":True})
        self.assertEqual(e.trained_hits,1); self.assertEqual(e.zero_hits,0)
        h._LAW5_DEFAULT_CTX=False; e.registry.clear()
        with self.assertRaises(R.Halt): e(None,req,None,None)
        e.registry[frozenset({("s"," value")})]={"zero":True}
        e.null_passed=e.law3_passed=False; e.null_application=True
        e(None,req,None,None); self.assertEqual(e.zero_hits,1)

    def test_guards_projection_memory_and_eval_wall_boundaries(self):
        """§2.9,5 lines314–318,439–441: equality passes; guards are HALT,not FAIL."""
        for fn,yes,no in ((T.check_attempt_minutes,90,90.0001),
                          (R.check_driver_bytes,40000000000,40000000001),
                          (R.check_eval_seconds,14400,14400.0001)):
            fn(yes)
            with self.assertRaises(R.Halt): fn(no)
        for p,limit in (("P1",465),("P2",448),("P3",327)):
            self.assertEqual(R.PHASE_LIMITS[p],limit)
            R.check_phase_minutes(p,limit)
            with self.assertRaises(R.Halt): R.check_phase_minutes(p,limit+.001)
        self.assertAlmostEqual(T.project_attempt_minutes([2.0]*20,400,40,2.0),440/30)

    def test_P2_P3_authorization_even_under_projection_limit(self):
        """§2.8,2.9,8 lines278,280,285,314,532: no implicit post-P1 approval."""
        for p in ("P2","P3"):
            with self.assertRaises(R.Halt): R.require_authorization(p,None,HASH,HASH,1.0)
            auth={p:{"authorized":True,"p1_eval_sha256":HASH,"p1_verdict_sha256":HASH,
                     "recorded_by":"operator","recorded_at":"2026-10-07T00:00:00Z"}}
            R.require_authorization(p,auth,HASH,HASH,1.0)
            for key in ("authorized","p1_eval_sha256","p1_verdict_sha256","recorded_by","recorded_at"):
                a=copy.deepcopy(auth); a[p][key]=False if key=="authorized" else ""
                with self.assertRaises(R.Halt): R.require_authorization(p,a,HASH,HASH,1.0)
            with self.assertRaises(R.Halt): R.require_authorization(p,auth,HASH,HASH,R.PHASE_LIMITS[p]+1)
            auth[p]["budget_minutes"]=R.PHASE_LIMITS[p]+2
            R.require_authorization(p,auth,HASH,HASH,R.PHASE_LIMITS[p]+1)
        stages=R.stage_names()
        self.assertEqual(stages[:9],["step0","p1-preflight","p1-a1","p1-a7","p1-canon","p1-a2","p1-shuf","p1-eval","p1-project"])
        self.assertTrue(any(s.startswith("p2-") for s in stages))
        self.assertTrue(any(s.startswith("p3-") for s in stages))

    def test_records_exclusive_roundtrip_and_nonfinite_halt(self):
        """§2.10,3 lines322–325,344: real writer, append-only, every JSON classification."""
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"record.json"
            R.write_json(p,{"n":72,"count":61,"reference_count":None})
            x=R.load_json(p)
            self.assertEqual(x["n"],72); self.assertEqual(x["class"],R.CLASS)
            self.assertEqual(x["decision_id"],R.DECISION_ID)
            self.assertIsNone(x["reference_count"])
            with self.assertRaises(R.Halt): R.write_json(p,{"count":30})
            for val in (float("nan"),float("inf"),float("-inf")):
                q=Path(td)/"bad.json"
                with self.assertRaises(R.Halt): R.write_json(q,{"loss":[val]})
                self.assertFalse(q.exists())
            q=Path(td)/"bad.json"; q.write_text('{"loss":NaN}')
            with self.assertRaises(R.Halt): R.load_json(q)
            p2=Path(td)/"fresh"; R.fresh_directory(p2)
            with self.assertRaises(R.Halt): R.fresh_directory(p2)
            data=fixture(); record=Path(td)/"eval.json"; R.write_json(record,data["P1"])
            self.assertEqual(R.load_json(record),data["P1"])
        with patch.object(R,"adapter_is_tracked",return_value=True):
            with self.assertRaises(R.Halt): R.require_untracked_adapter(ROOT/"fixture.safetensors")

    def test_embedded_training_evidence_must_equal_hashed_attempt(self):
        """§3 lines339–342: a valid file hash cannot authenticate different embedded fit/steps."""
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"attempt.json"
            tr=train(("A7",0,16,False),"P1"); R.write_json(p,tr)
            tr["record_file"]=R.file_ref(p); R.verify_linked_train(tr)
            for defect in ("fit","steps","frozen"):
                x=copy.deepcopy(tr)
                if defect=="fit": x["fit"]["correct"]=455
                elif defect=="steps": x["steps"]=800
                else: x["frozen_parameters_unchanged"]=False
                with self.assertRaises(R.Halt): R.verify_linked_train(x)

    def test_required_probe_rows_and_gate_summaries_cannot_diverge(self):
        """§2.6,3 lines218,224,233,342–345: raw frame, MMLU and cross-score evidence is required."""
        for defect in ("mounted_string","mounted_rows","mounted_sum","frame_rows","frame_sum","mmlu_rows","mmlu_sum","cross_rows","cross_sum","geometry"):
            d=fixture(); a=d["P1"]["recipes"]["oracle_p1"]["arms"][R.A7]
            if defect=="mounted_string": a["extra"]["mounted"]["para_string_n"]=60
            elif defect=="mounted_rows": a["extra"]["mounted"].pop("rows")
            elif defect=="mounted_sum": a["extra"]["mounted"]["para_full_n"]=71
            elif defect=="frame_rows": a["extra"]["frames"]["canon"].pop("rows")
            elif defect=="frame_sum": a["extra"]["frames"]["canon"]["flips"]=0
            elif defect=="mmlu_rows": a["extra"]["mmlu"].pop("rows")
            elif defect=="mmlu_sum": a["extra"]["mmlu"]["correct_n"]=199
            elif defect=="cross_rows": d["P1"]["recipes"]["oracle_p1"]["arms"][R.SHUF]["extra"].pop("cross_detail")
            elif defect=="cross_sum": d["P1"]["recipes"]["oracle_p1"]["arms"][R.SHUF]["extra"]["cross_score"]["para_full_n"]=1
            else: a["extra"]["geometry"].pop("4")
            self.assertEqual(self.read(d)["status"],"INVALID",defect)

    def test_P3_replication_must_belong_to_authorized_P1(self):
        """§2.8,3 lines278–285,339–340: another P1's replication cannot enable rank64."""
        with tempfile.TemporaryDirectory() as td:
            p1=Path(td)/"p1"; p2=Path(td)/"p2"; p1.mkdir(); p2.mkdir()
            R.write_json(p1/"eval.json",phase("P1"))
            wrong=phase("P2",30); wrong["p1_eval_sha256"]="b"*64
            R.write_json(p2/"eval.json",wrong)
            with patch.object(R,"latest_directory",return_value=p2), self.assertRaisesRegex(R.Halt,"another P1"):
                R.replication_for(p1)

    def test_restore_and_frozen_scope_require_actual_hash_evidence(self):
        """§2.4,2.7,3 lines170,251,339–345: contradictory hashes invalidate passing summaries."""
        for defect in ("final","recipe","frozen"):
            d=fixture(); p=d["P1"]
            if defect=="final": p["final_band_hash"]["4"]="b"*64
            elif defect=="recipe": p["recipes"]["oracle_p1"]["band_after_hash"]["4"]="b"*64
            else: p["train_records"][0]["frozen_parameter_hashes_after"]["synthetic.weight"]="b"*64
            self.assertEqual(self.read(d)["status"],"INVALID",defect)

    def test_pure_P1_reprojection_and_real_launcher_refusal(self):
        """§2.8,2.9 lines278,303–314,316: measured P2/P3 inventory,stage entry refuses."""
        projection=R.reproject({"training400_seconds":1200,"recipe_setup_seconds":600,
                              "u_seconds":1200,"null_seconds":600,"closedform_arm_seconds":600,
                              "oracle_arm_seconds":900})
        self.assertEqual(projection["P2_minutes"],6*20+20+10+4*10+3*10+6*15)
        self.assertEqual(projection["P3_minutes"],4*20+20+10+3*10+3*10+4*15)
        for stage in ("p2-a7-s1","p3-a7-s0"):
            proc=subprocess.run(["/bin/bash",str(ROOT/"code/lab/runners/run_c10w_stage.sh"),stage],
                                cwd=ROOT,env={"PATH":"/usr/bin:/bin","LLMDB_ROOT":str(ROOT),"MODEL_ID":"selftest-forbidden"},
                                capture_output=True,text=True)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn("inherited knob",proc.stdout+proc.stderr)



# ---------------------------------------------------------------------------
# Proposed by the implementation review (c10w_oracle_advisor_impl.md). Each test
# names the surviving mutant it kills. Model-free: torch/transformers appear only
# as inert stand-ins placed in sys.modules for the duration of one test.
# ---------------------------------------------------------------------------
from unittest.mock import MagicMock


def _fake_modules():
    return {"torch": MagicMock(name="torch"), "transformers": MagicMock(name="transformers")}


class ProposedTests(unittest.TestCase):
    def read(self, data):
        return R.read_measurement(data)

    # M11 -- read.py:276 band boundary at 61 for the same-seed crossing rule (prereg:368,370)
    def test_same_seed_band_crossing_at_61(self):
        d=fixture(61); replace_arm(d,"P2","oracle_s0rt","A7_coined_coined",arm(60))
        v=self.read(d)
        self.assertEqual(v["status"],"UNSTABLE")
        self.assertIn("same-seed band crossing",v["ranks"]["16"]["instability"])

    # M15 -- read.py:372 the merge-loss exception needs every gate holding (prereg:366)
    def test_merge_loss_exception_requires_clean_gates(self):
        d=fixture(61)
        for a in candidates(d):
            a["locality_axes"]["L3_top1_agree"]=28
            a["extra"]["mounted"]=mounted_score(67)
        self.assertEqual(self.read(d)["status"],"UNSTABLE")

    # M22 -- read.py:446 PASS split (b) does not motivate steps 6-7 (prereg:394)
    def test_pass_routing_split_b_is_not_motivation(self):
        v=self.read(fixture(61,None,29))
        self.assertEqual((v["final_label"],v["canon_split"]),("PASS-CEILING","b"))
        self.assertEqual(v["routing"]["action"],"INDEPENDENT-PREREG-ONLY")
        v=self.read(fixture(61,None,30))
        self.assertEqual(v["routing"]["action"],"MOTIVATE-INDEPENDENT-STEPS-6-7-5b")

    # M28 -- read.py:479 a HALTed phase directory is never reused (prereg:246,446)
    def test_latest_directory_refuses_halted_phase(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p1_20261007T000000_000000Z"; p.mkdir()
            self.assertEqual(R.latest_directory("p1",td),p)
            R.write_json(p/"HALT.json",{"status":"HALT"})
            with self.assertRaisesRegex(R.Halt,"HALTED"): R.latest_directory("p1",td)

    # M29 -- read.py:486 step0 frozen against the frozen prereg hash (prereg:3,322)
    def test_load_frozen_rejects_prereg_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            R.write_json(Path(td)/"step0.json",{"status":"PASS","prereg_sha256":"b"*64,"files":{},"sources":{},
                                                 "seal":{s:True for s in ("S1","S2","S2c","S2d","S3","S4","S5","S6","S7")},
                                                 "seam":{"ok":True},"fingerprint":{"ok":True},"instrument_ok":True})
            with self.assertRaisesRegex(R.Halt,"prereg"): R.load_frozen(td)

    # M30 -- read.py:311 recorded null tensor hashes must agree (prereg:250)
    def test_null_after_hash_mismatch_invalid(self):
        d=fixture(); d["P1"]["law5_null"]["after_hash"]["4"]="b"*64
        self.assertEqual(self.read(d)["status"],"INVALID")

    # M36/M37/M38 -- step0.py:62,71,73 each seal rule fires on its own (prereg:96-100)
    def test_each_seal_rule_is_independently_binding(self):
        c=S.source_constants(ROOT)
        for text,rule in (("Encyclopedia entry: {}. Capital:","S2c"),("Reference card for {}. Capital:","S2c"),
                          ("The nation capital of {} is","S3"),("The principal capital of {} is","S1")):
            row=S.audit_templates(c,[text],[])["rows"][0]
            self.assertFalse(row["ok"],text)
            self.assertFalse(row["checks"][rule],(text,rule))
            self.assertTrue(all(v for k,v in row["checks"].items() if k!=rule),(text,row["checks"]))
        row=S.audit_templates(c,["The nation capital of {} is"],[])["rows"][0]
        self.assertTrue(.60<=row["max_s3"]<.61)

    # --- dispatcher scaffolding -------------------------------------------------------------
    def _dispatch_tree(self,td):
        td=Path(td); (td/"architecture_profile").mkdir()
        step0=td/"step0_x"; p1=td/"p1_x"; step0.mkdir(); p1.mkdir(); (p1/"train").mkdir(); (p1/"adapters").mkdir()
        R.write_json(step0/"step0.json",{"status":"PASS"})
        R.write_json(p1/"preflight.json",{"phase":"P1","wall_seconds":85*60.})
        return td,step0,p1

    def _dispatch_patches(self,td,step0,p1,extra=()):
        import contextlib
        stack=contextlib.ExitStack()
        stack.enter_context(patch.object(R,"ROOT",td))
        stack.enter_context(patch.object(R,"entry_preflight",lambda *a,**k:td))
        stack.enter_context(patch.object(R,"latest_directory",lambda prefix,base=None:{"step0":step0,"p1":p1}[prefix]))
        stack.enter_context(patch.object(R,"load_frozen",lambda d:{}))
        stack.enter_context(patch.object(R,"frozen_provenance",lambda s:{}))
        stack.enter_context(patch.object(T,"require_training_preflight",lambda *a:None))
        for p in extra: stack.enter_context(p)
        return stack

    # M34 -- step0.py:370 pre-start phase projection refusal before spending (prereg:314,316)
    def test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit(self):
        with tempfile.TemporaryDirectory() as td:
            td,step0,p1=self._dispatch_tree(td)
            R.write_json(p1/"train"/"A1_single_s0_r16.json",{"arm":R.A1,"seed":0,"rank":16,"retrain":False,
                                                             "steps":400,"status":"PASS","wall_seconds":100*60.})
            launched=MagicMock(return_value=0)
            with self._dispatch_patches(td,step0,p1,[patch.object(S,"train_one",launched)]):
                with self.assertRaisesRegex(R.Halt,"INVALID-BUDGET"): S.dispatch_stage("p1-a7")
            launched.assert_not_called()

    # M35 -- step0.py:365 units train in the frozen order (prereg:275-276)
    def test_dispatch_refuses_out_of_order_training_unit(self):
        with tempfile.TemporaryDirectory() as td:
            td,step0,p1=self._dispatch_tree(td)
            launched=MagicMock(return_value=0)
            with self._dispatch_patches(td,step0,p1,[patch.object(S,"train_one",launched)]):
                with self.assertRaisesRegex(R.Halt,"prior training unit"): S.dispatch_stage("p1-a7")
            launched.assert_not_called()

    # M32 -- step0.py:348 the launcher refuses P2 without the recorded authorization (prereg:278,532)
    def test_dispatch_refuses_P2_without_authorization_before_creating_phase(self):
        with tempfile.TemporaryDirectory() as td:
            td,step0,p1=self._dispatch_tree(td)
            R.write_json(p1/"eval.json",{"phase":"P1"}); R.write_json(p1/"verdict.json",{"projection":{"P2_minutes":1.}})
            created=MagicMock(side_effect=AssertionError("P2 phase directory created without authorization"))
            with self._dispatch_patches(td,step0,p1,[patch.object(S,"new_phase",created)]):
                with self.assertRaisesRegex(R.Halt,"authorization"): S.dispatch_stage("p2-a7-s1")
            created.assert_not_called()

    # M33 -- step0.py:324 P3 also needs scientific eligibility (prereg:285,372)
    def test_P3_entry_requires_scientific_eligibility(self):
        with tempfile.TemporaryDirectory() as td:
            p1=Path(td)
            R.write_json(p1/"eval.json",{"phase":"P1"}); R.write_json(p1/"verdict.json",{"projection":{"P3_minutes":1.}})
            R.write_json(p1/"authorization_P3.json",{"P3":{"authorized":True}})
            with patch.object(R,"require_authorization",lambda *a:None), patch.object(R,"replication_for",lambda p:{}), \
                 patch.object(R,"read_measurement",lambda phases:{"status":"VALID","p3_required":False}):
                with self.assertRaisesRegex(R.Halt,"P3"): S.ensure_authorized("P3",p1)

    # --- evaluator scaffolding --------------------------------------------------------------
    def _eval_run(self,phase,closed_a7=4,preflight_side=None,extra=()):
        import contextlib
        calls=[]
        class FakeEvaluator:
            def __init__(s,H,step,directory,start):
                s.wrapper=types.SimpleNamespace(law3_passed=False,zero_hits=1,trained_hits=0,ORIGINAL_MY_EDIT=None)
                s.u={k:{"para_full_n":0} for k in (R.A1,R.A2,R.A7,R.SHUF)}
            def guard(s,label): pass
            def unedited(s): calls.append("U"); return {k:{"base":0} for k in (R.A1,R.A2,R.A7,R.SHUF)}
            def null(s): calls.append("null"); return {}
            def run_recipe(s,name,arms,records):
                calls.append(name)
                return {"arms":{R.A1:{"para_full_n":68},R.A2:{"para_full_n":68},
                                R.A7:{"para_full_n":closed_a7,"canon_full_n":8,"para_first_n":50}}}
        records=[{"arm":a,"seed":sd,"rank":rk,"retrain":rt,"provenance":{}} for a,sd,rk,rt in R.TRAIN_UNITS["P1"]]
        stack=contextlib.ExitStack()
        stack.enter_context(patch.dict(sys.modules,_fake_modules()))
        stack.enter_context(patch.object(R,"entry_preflight",lambda *a,**k:ROOT))
        stack.enter_context(patch.object(R,"load_frozen",lambda d:{}))
        stack.enter_context(patch.object(R,"frozen_provenance",lambda s:{}))
        stack.enter_context(patch.object(R,"phase_trains",lambda d,p:records))
        stack.enter_context(patch.object(S,"fingerprint",lambda:{"ok":True}))
        stack.enter_context(patch.object(S,"load_harness",lambda:types.SimpleNamespace()))
        stack.enter_context(patch.object(E,"Evaluator",FakeEvaluator))
        if preflight_side is not None:
            stack.enter_context(patch.object(T,"require_training_preflight",MagicMock(side_effect=preflight_side)))
        else:
            stack.enter_context(patch.object(T,"require_training_preflight",lambda *a:None))
        for p in extra: stack.enter_context(p)
        return stack,calls

    # M39 -- eval.py:359 LAW#3 halts in-process before any oracle recipe (prereg:241-246,277)
    def test_eval_law3_miss_halts_before_any_oracle_recipe(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); R.write_json(d/"preflight.json",{"phase":"P1"}); R.write_json(d/"step0.json",{"x":1})
            stack,calls=self._eval_run("P1",closed_a7=4)
            with stack:
                with self.assertRaisesRegex(R.Halt,"LAW#3"): E.run_eval("P1",d,d)
            self.assertEqual(calls,["U","null","closedform"])

    # M44 -- eval.py:347 the trainer certificate is verified before the model loads (prereg:241,260)
    def test_eval_verifies_preflight_certificate_before_model_load(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); R.write_json(d/"preflight.json",{"phase":"P1"}); R.write_json(d/"step0.json",{"x":1})
            stack,calls=self._eval_run("P1",preflight_side=R.Halt("HALT: bad certificate"),
                                       extra=[patch.object(S,"fingerprint",MagicMock(side_effect=AssertionError("model stage reached")))])
            with stack:
                with self.assertRaisesRegex(R.Halt,"bad certificate"): E.run_eval("P1",d,d)
            self.assertEqual(calls,[])

    # M45 -- eval.py:352 a P2 evaluation re-checks the recorded authorization itself (prereg:280,532)
    def test_eval_P2_rechecks_authorization(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); p1=d/"p1"; p1.mkdir()
            R.write_json(p1/"eval.json",{"phase":"P1"}); R.write_json(p1/"verdict.json",{"projection":{}})
            R.write_json(d/"auth.json",{"P2":{"authorized":False}})
            R.write_json(d/"preflight.json",{"phase":"P2","p1_directory":str(p1),"authorization":R.file_ref(d/"auth.json"),
                                             "authorized_projection_minutes":1.})
            R.write_json(d/"step0.json",{"x":1})
            stack,calls=self._eval_run("P2",extra=[patch.object(S,"fingerprint",MagicMock(side_effect=AssertionError("model stage reached")))])
            with stack:
                with self.assertRaisesRegex(R.Halt,"authorization"): E.run_eval("P2",d,d)
            self.assertEqual(calls,[])

    # M40 -- eval.py:239 the zero adapter must leave the band bit-identical (prereg:250)
    def test_null_application_that_changes_band_halts_before_scoring(self):
        state={"hash":"base"}
        e=object.__new__(E.Evaluator)
        e.H=types.SimpleNamespace(CANON="{}",_LAW5_DEFAULT_CTX=False,my_edit=lambda *a:{},
                                   req=lambda c,s,v:{"subject":s,"target_new":{"str":" "+v}})
        e.maps={R.A7:{"s":"v"}}; e.hp=None; e.unit_times={}
        e.base_hash={"4":"base"}; e.band_hash=lambda:{"4":state["hash"]}
        e.restore=lambda:None
        def apply(adapter,hp): state["hash"]="signed-zero-flipped"; return {}
        e.wrapper=E.OracleEdit(e.H,e.assert_base,apply)
        e.evaluate_map=MagicMock(side_effect=AssertionError("scored a changed band"))
        with self.assertRaisesRegex(R.Halt,"LAW#5"): e.null()
        e.evaluate_map.assert_not_called()

    # M42 -- eval.py:35 restore is asserted before every oracle application (prereg:199,251)
    def test_oracle_entry_requires_restored_band(self):
        applied=[]
        h=types.SimpleNamespace(my_edit=lambda *a:{},_LAW5_DEFAULT_CTX=False)
        def not_restored(): raise R.Halt("HALT: LAW#5(iii): band not restored")
        e=E.OracleEdit(h,not_restored,lambda adapter,hp:applied.append(adapter) or {})
        e.mode="oracle"; e.registry[frozenset({("s"," v")})]={"zero":False}; e.null_passed=e.law3_passed=True
        with self.assertRaisesRegex(R.Halt,"LAW#5"): e(None,[{"subject":"s","target_new":{"str":" v"}}],None,None)
        self.assertEqual(applied,[])

    # M43 -- eval.py:98 the adapter file hash is verified before it is loaded (prereg:200)
    def test_adapter_hash_verified_before_load(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a.safetensors"; p.write_bytes(b"x")
            e=object.__new__(E.Evaluator); e.torch=types.SimpleNamespace(); e.H=None
            adapter={"zero":False,"train":{"adapter":{"path":str(p),"sha256":"b"*64},"rank":16}}
            with self.assertRaisesRegex(R.Halt,"hash mismatch"):
                e.apply_adapter(adapter,types.SimpleNamespace(layers=list(R.BAND)))

    # M46 -- train.py:142 the trainer re-verifies the passing preflight before any model import (prereg:241,260)
    def test_trainer_verifies_preflight_before_torch(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); (d/"train").mkdir()
            R.write_json(d/"preflight.json",{"phase":"P1","status":"FAIL"}); R.write_json(d/"step0.json",{"x":1})
            with patch.object(R,"entry_preflight",lambda *a,**k:ROOT), patch.object(R,"load_frozen",lambda x:{}), \
                 patch.object(R,"frozen_provenance",lambda s:{}):
                with self.assertRaisesRegex(R.Halt,"preflight"): T.run_attempt(d,d,(R.A1,0,16,False),400)

    # M47 -- train.py:216 the post-warm-up projection refuses a >90-minute attempt early (prereg:316,439)
    def test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit(self):
        mods=_fake_modules(); torch=mods["torch"]; torch.nn.Module=object
        torch.backends.mps.is_available.return_value=True
        torch.mps.driver_allocated_memory.return_value=1
        class Tok:
            pad_token="<eos>"; eos_token="<eos>"; eos_token_id=0
            def __call__(self,text,add_special_tokens=True): return {"input_ids":[len(text)%97+1]}
        model=MagicMock(); model.config._commit_hash=R.MODEL_REV
        model.parameters.return_value=[]; model.named_parameters.return_value=[]
        layers={}
        for l in range(36):
            layers[l]=MagicMock(); layers[l].mlp.down_proj.weight.shape=(2048,11008)
        model.model.layers.__getitem__.side_effect=lambda i:layers[i]
        mods["transformers"].AutoTokenizer.from_pretrained.return_value=Tok()
        mods["transformers"].AutoModelForCausalLM.from_pretrained.return_value.float.return_value=model
        clock=[0.]
        def tick(): clock[0]+=5.; return clock[0]
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); (d/"train").mkdir(); tok=Tok()
            subjects=["s%02d"%i for i in range(24)]
            inputs={"templates":["T {}"],"fiction":subjects,"value_maps":{R.A7:{s:"v" for s in subjects}},
                    "target_ids":{R.A7:{s:tok(" v")["input_ids"] for s in subjects}},
                    "prompt_ids":{"0":{s:tok("T {}".format(s))["input_ids"] for s in subjects}}}
            R.write_json(d/"train_inputs.json",inputs)
            R.write_json(d/"preflight.json",{"phase":"P1"}); R.write_json(d/"step0.json",{"x":1})
            step={"files":{"train_inputs":{"path":str(d/"train_inputs.json")}},"fingerprint":{"ok":True}}
            with patch.dict(sys.modules,mods), patch.dict("os.environ",{}), \
                 patch.object(R,"entry_preflight",lambda *a,**k:ROOT), patch.object(R,"load_frozen",lambda x:step), \
                 patch.object(R,"frozen_provenance",lambda s:{}), patch.object(T,"require_training_preflight",lambda *a:None), \
                 patch.object(T.time,"monotonic",tick):
                with self.assertRaisesRegex(R.Halt,"90"): T.run_attempt(d,d,(R.CANON_ARM,0,16,False),400)
            record=R.load_json(d/"train"/"A7_canon_s0_r16.json")
            self.assertEqual(record["status"],"HALT")
            self.assertLess(record["wall_seconds"],30*60,"guard fired only at the wall limit, not on the projection")

    # M48 -- train.py:34 linear 20-step warm-up from 0 (prereg:181)
    def test_warmup_is_linear_over_20_steps(self):
        self.assertAlmostEqual(T.learning_rate(10),1.5e-4)
        self.assertLess(T.learning_rate(19),3e-4)


class DefectTests(unittest.TestCase):
    """Reproduce defects in the unmodified build; expected to FAIL until fixed (always on)."""
    def read(self, data):
        return R.read_measurement(data)

    # BLOCKING-2 -- read.py:264 G3 equality to A-3 passes at every 2-dp value (prereg:368)
    def test_G3_equality_passes_across_the_range(self):
        for ref in (64.01,64.04,98.12,99.88):
            d=fixture()
            for p in d.values():
                p["recipes"]["closedform"]["arms"][R.A7]["locality_described_as"]=ref
            for a in candidates(d): a["locality_described_as"]=round(ref-3,2)
            self.assertNotIn("G3",self.read(d)["ranks"]["16"]["gate_misses"],ref)



class FixRoundTests(unittest.TestCase):
    """Fix-round regressions; synthetic records are never live model evidence."""

    def test_G3_hundredths_at_inside_and_outside_boundary(self):
        for ref in (64.01, 64.04, 98.12, 99.88):
            for offset, passes in ((-0.01, False), (0.0, True), (0.01, True)):
                with self.subTest(ref=ref, offset=offset):
                    reference, candidate = arm(), arm()
                    reference["locality_described_as"] = ref
                    candidate["locality_described_as"] = round(ref - 3 + offset, 2)
                    self.assertEqual(R.gates(candidate, reference, arm())["G3"], passes)

    def _eval_dispatch(self, phase_name, minutes, ruling=None, failed_minutes=0):
        with tempfile.TemporaryDirectory() as td:
            td, step0, directory = ProposedTests._dispatch_tree(self, td)
            proof = R.load_json(directory/"preflight.json")
            proof.update(phase=phase_name, p1_directory=str(directory))
            (directory/"preflight.json").write_text(json.dumps(proof))
            evaluation = {"P1":190., "P2":220., "P3":175.}[phase_name]
            cost = minutes - evaluation - (85 if phase_name == "P1" else 0) - failed_minutes
            units = R.TRAIN_UNITS[phase_name]
            records = []
            for index, unit in enumerate(units):
                record = {"arm":unit[0], "seed":unit[1], "rank":unit[2], "retrain":unit[3],
                          "status":"PASS", "steps":400, "wall_seconds":cost/len(units)*60}
                R.write_json(directory/"train"/(R.train_tag(unit,400)+".json"), record)
                records.append(record)
            if failed_minutes:
                failed = {**records[0], "status":"UNDERFIT", "wall_seconds":failed_minutes*60}
                R.write_json(directory/"train"/"failed_attempt.json", failed)
            if ruling is not None:
                R.write_json(directory/("authorization_"+phase_name+".json"), {phase_name:ruling})
            launched = MagicMock(return_value=0)
            extra = [patch.object(S, "run_child", launched),
                     patch.object(R, "phase_trains", lambda *a:records),
                     patch.object(S, "ensure_authorized", lambda *a:({}, minutes)),
                     patch.object(R, "latest_directory", lambda prefix,base=None:step0 if prefix == "step0" else directory)]
            with ProposedTests._dispatch_patches(self, td, step0, directory, extra):
                try:
                    rc = S.dispatch_stage(phase_name.lower()+"-eval")
                except R.Halt as exc:
                    launched.assert_not_called()
                    self.assertTrue((directory/"HALT.json").is_file())
                    return str(exc)
                self.assertEqual(rc, 0)
                launched.assert_called_once()
                return None

    def test_all_eval_stages_check_budget_before_child_at_inside_outside(self):
        for phase_name, limit in R.PHASE_LIMITS.items():
            for offset in (-0.01, 0.0, 0.01):
                with self.subTest(phase=phase_name, offset=offset):
                    failure = self._eval_dispatch(phase_name, limit+offset)
                    if offset > 0:
                        self.assertIn("INVALID-BUDGET", failure or "")
                    else:
                        self.assertIsNone(failure)

    def test_P1_516_minutes_refuses_and_counts_failed_attempts(self):
        self.assertIn("INVALID-BUDGET", self._eval_dispatch("P1",516) or "")
        self.assertIn("INVALID-BUDGET", self._eval_dispatch("P1",516,failed_minutes=51) or "")

    def test_P1_budget_ruling_requires_operator_identity(self):
        valid = {"authorized":True, "recorded_by":"operator", "recorded_at":"2026-10-07T00:00:00Z", "budget_minutes":516}
        self.assertIsNone(self._eval_dispatch("P1",516,valid))
        for key in ("authorized", "recorded_by", "recorded_at"):
            for replacement in (None, ""):
                with self.subTest(key=key, replacement=replacement):
                    ruling = dict(valid)
                    if replacement is None: del ruling[key]
                    else: ruling[key] = replacement
                    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
        for limit, passes in ((515.99,False),(516.,True),(516.01,True)):
            with self.subTest(limit=limit):
                failure = self._eval_dispatch("P1",516,{**valid,"budget_minutes":limit})
                self.assertEqual(failure is None, passes)

    def test_training_guard_also_requires_P1_ruling_identity(self):
        valid = {"authorized":True,"recorded_by":"operator","recorded_at":"2026-10-07T00:00:00Z","budget_minutes":465}
        for missing in (None,"authorized","recorded_by","recorded_at"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as td:
                td, step0, p1 = ProposedTests._dispatch_tree(self,td)
                ruling = dict(valid)
                if missing is not None: del ruling[missing]
                R.write_json(p1/"authorization_P1.json",{"P1":ruling})
                args = (p1,"P1",R.load_json(p1/"preflight.json"),R.TRAIN_UNITS["P1"][0],400)
                if missing is None: S.guard_training_unit(*args)
                else:
                    with self.assertRaisesRegex(R.Halt,"authorization"): S.guard_training_unit(*args)

    def _full_eval_patches(self, directory, closed=12, positive=68, failure=None, phase_name="P1"):
        import contextlib
        data = phase(phase_name)
        replace_arm({"P1":data},"P1","closedform",R.A7,arm(closed,8,55))
        if phase_name == "P1": replace_arm({"P1":data},"P1","oracle_p1",R.A2,arm(positive))
        for rec in data["recipes"].values():
            rec["delta_norms"] = {key:{str(l):{"delta_norm":1.} for l in R.BAND} for key in rec["arms"]}
        (directory/"train").mkdir()
        R.write_json(directory/"step0.json",{"status":"PASS"})
        proof = {"phase":phase_name}
        if phase_name == "P2":
            p1 = directory/"p1"; p1.mkdir()
            R.write_json(p1/"eval.json",phase("P1")); R.write_json(p1/"verdict.json",{})
            ruling = {"P2":{"authorized":True,"recorded_by":"operator","recorded_at":"2026-10-07T00:00:00Z",
                             "p1_eval_sha256":R.sha_file(p1/"eval.json"),"p1_verdict_sha256":R.sha_file(p1/"verdict.json")}}
            R.write_json(p1/"authorization_P2.json",ruling)
            proof.update(p1_directory=str(p1),authorization=R.file_ref(p1/"authorization_P2.json"),authorized_projection_minutes=1.)
        R.write_json(directory/"preflight.json",proof)
        for record in data["train_records"]:
            R.write_json(directory/"train"/(R.train_tag(R.train_identity(record),400)+".json"),record)
        original = lambda *a:{}
        saved_hook = lambda *a:{}
        harness = types.SimpleNamespace(my_edit=original, ARM_HOOKS=[saved_hook])
        calls = []
        class FakeEvaluator:
            def __init__(s,H,step,directory,start):
                if failure == "constructor":
                    H.my_edit = None; H.ARM_HOOKS[:] = []
                    raise R.Halt("HALT: constructor failed")
                s.original = original
                s.wrapper = types.SimpleNamespace(zero_hits=1,trained_hits=0,law3_passed=False,ORIGINAL_MY_EDIT=original)
                H.my_edit = s.wrapper
                s.u = {}; s.u_detail = {}; s.stimulus = {}; s.null_evidence = {}
                s.base_hash = data["base_band_hash"]; s.start = start; s.peak = 1; s.memory = []
                s.unit_times = {"recipe_setup_seconds":[1.],"closedform_arm_seconds":[1.],"oracle_arm_seconds":[1.],
                                "u_seconds":1.,"null_seconds":1.}
            def guard(s,label):
                if failure == "guard" and label == "model-loaded": raise R.Halt("HALT: first guard failed")
            def unedited(s):
                calls.append("U")
                s.u = copy.deepcopy(data["u"]); s.u_detail = copy.deepcopy(data["u_detail"])
                s.stimulus = copy.deepcopy(data["stimulus"])
                if failure == "U": raise R.Halt("HALT: U acquisition failed")
                return s.stimulus
            def null(s):
                calls.append("null"); s.null_evidence = copy.deepcopy(data["law5_null"])
                return s.null_evidence
            def run_recipe(s,name,arms,records):
                calls.append(name)
                s.wrapper.trained_hits += len(records)
                result = copy.deepcopy(data["recipes"][name])
                if failure == "nan" and name == "closedform":
                    result["arms"][R.A7]["extra"]["geometry"]["4"]["delta_norm"] = float("nan")
                return result
            def assert_base(s): pass
            def band_hash(s): return s.base_hash
        stack = contextlib.ExitStack()
        for item in (patch.dict(sys.modules,_fake_modules()),
                     patch.object(R,"entry_preflight",lambda *a,**k:ROOT),
                     patch.object(R,"load_frozen",lambda d:{}),
                     patch.object(R,"frozen_provenance",lambda s:data["provenance"]),
                     patch.object(R,"phase_trains",lambda *a:data["train_records"]),
                     patch.object(T,"require_training_preflight",lambda *a:None),
                     patch.object(S,"fingerprint",lambda:{"ok":True}),
                     patch.object(S,"load_harness",lambda:harness),
                     patch.object(S,"model_environment",lambda *a:data["environment"]),
                     patch.object(E,"Evaluator",FakeEvaluator)):
            stack.enter_context(item)
        return stack, calls, harness, original, saved_hook

    def test_LAW3_failure_persists_partial_readouts_and_boundary_controls(self):
        for count, passes in ((4,False),(5,True),(18,True),(19,False)):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as td:
                d = Path(td)
                stack, calls, harness, original, hook = self._full_eval_patches(d,closed=count)
                with stack:
                    if passes:
                        self.assertEqual(E.run_eval("P1",d,d),0)
                        self.assertEqual(R.read_measurement({"P1":R.load_json(d/"eval.json")})["status"],"INCOMPLETE")
                    else:
                        with self.assertRaisesRegex(R.Halt,"LAW#3"): E.run_eval("P1",d,d)
                        self.assertTrue((d/"eval_halt.json").is_file())
                        raw = R.load_json(d/"eval_halt.json")
                        self.assertEqual(calls,["U","null","closedform"])
                        self.assertEqual(raw["recipes"]["closedform"]["arms"][R.A7]["para_full_n"],count)
                        for key in ("u","u_detail","stimulus","law5_null"): self.assertTrue(raw[key],key)
                        self.assertIn("LAW#3",raw["reason"])
                        self.assertEqual(R.read_measurement({"P1":raw})["status"],"INVALID")
                self.assertIs(harness.my_edit, original)
                self.assertEqual(harness.ARM_HOOKS,[hook])

    def test_validity_failure_writes_eval_before_validation(self):
        for count, passes in ((67,False),(68,True),(69,True)):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as td:
                d = Path(td)
                stack, calls, harness, original, hook = self._full_eval_patches(d,positive=count)
                with stack:
                    if passes:
                        self.assertEqual(E.run_eval("P1",d,d),0)
                    else:
                        with self.assertRaisesRegex(R.Halt,"positive control"): E.run_eval("P1",d,d)
                        self.assertTrue((d/"eval.json").is_file())
                        self.assertTrue((d/"eval_halt.json").is_file())
                        raw = R.load_json(d/"eval.json")
                        self.assertEqual(raw["recipes"]["oracle_p1"]["arms"][R.A2]["para_full_n"],67)
                        self.assertEqual(R.read_measurement({"P1":raw})["status"],"INVALID")
                        self.assertEqual(set(R.load_json(d/"eval_halt.json")["recipes"]),set(raw["recipes"]))

    def test_setup_and_U_failures_keep_partial_evidence_and_cleanup(self):
        for failure in ("constructor","guard","U"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as td:
                d = Path(td)
                stack, calls, harness, original, hook = self._full_eval_patches(d,failure=failure)
                with stack:
                    with self.assertRaisesRegex(R.Halt,"failed"): E.run_eval("P1",d,d)
                self.assertTrue((d/"eval_halt.json").is_file())
                raw = R.load_json(d/"eval_halt.json")
                self.assertEqual(R.read_measurement({"P1":raw})["status"],"INVALID")
                for key in ("u","u_detail","stimulus","law5_null","recipes","reason"): self.assertIn(key,raw)
                if failure == "U":
                    for key in ("u","u_detail","stimulus"): self.assertTrue(raw[key])
                self.assertIs(harness.my_edit, original)
                self.assertEqual(harness.ARM_HOOKS,[hook])

    def test_P2_diagnostic_failure_restores_function_instead_of_training_record(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            stack, calls, harness, original, hook = self._full_eval_patches(d,phase_name="P2")
            with stack, patch.object(R,"latest_directory",lambda *a:d/"p1"), \
                 patch.object(T,"load_adapter",side_effect=R.Halt("HALT: P2 diagnostic failed")):
                with self.assertRaisesRegex(R.Halt,"P2 diagnostic failed"): E.run_eval("P2",d,d)
            self.assertIs(harness.my_edit,original)
            self.assertEqual(harness.ARM_HOOKS,[hook])
            self.assertTrue((d/"eval_halt.json").is_file())
            raw = R.load_json(d/"eval_halt.json")
            self.assertEqual(set(raw["recipes"]),{"closedform",*R.RECIPES["P2"]})
            self.assertEqual(R.read_measurement({"P1":phase("P1"),"P2":raw})["status"],"INVALID")

    def test_nonfinite_failure_preserves_reason_and_raw_diagnostic(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            stack, calls, harness, original, hook = self._full_eval_patches(d,failure="nan")
            with stack:
                with self.assertRaisesRegex(R.Halt,"non-finite"): E.run_eval("P1",d,d)
            self.assertTrue((d/"eval_halt.json").is_file())
            raw = R.load_json(d/"eval_halt.json")
            self.assertIn("non-finite",raw["reason"])
            self.assertEqual(raw["recipes"]["closedform"]["arms"][R.A7]["extra"]["geometry"]["4"]["delta_norm"],"nan")
            self.assertEqual(R.read_measurement({"P1":raw})["status"],"INVALID")

    def test_p1_project_invalid_record_returns_reader_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            td, step0, p1 = ProposedTests._dispatch_tree(self,td)
            data = phase("P1"); data["validity"]["hashes"] = False
            R.write_json(p1/"eval.json",data)
            with ProposedTests._dispatch_patches(self,td,step0,p1), patch("sys.stdout",new=io.StringIO()):
                rc = S.dispatch_stage("p1-project")
            self.assertEqual(rc,2)
            raw = R.load_json(p1/"verdict.json")
            self.assertEqual(raw["status"],"INVALID")
            self.assertIsNone(raw["routing"])
            self.assertNotIn("projection",raw)

    def test_unedited_saves_stimulus_before_leak_validation(self):
        e = object.__new__(E.Evaluator)
        e.maps = {k:{} for k in (R.A1,R.A2,R.A7,R.SHUF)}
        stimulus = {k:{"base":4} for k in e.maps}
        e.H = types.SimpleNamespace(pre_base_report=lambda:stimulus)
        e.assert_base = lambda:None
        with self.assertRaisesRegex(R.Halt,"stimulus"): e.unedited()
        self.assertEqual(e.stimulus,stimulus)

    def test_tracer_limits_local_line_events_to_recipe_and_original(self):
        observed = []
        def nested():
            observed.append(("nested",sys._getframe().f_trace is not None))
        def original(*args):
            observed.append(("original",sys._getframe().f_trace is not None)); nested()
            return {}
        def run_recipe(*args):
            observed.append(("recipe",sys._getframe().f_trace is not None)); nested(); h.my_edit(None,[],None,None)
            return {"law5_gate":{"ok":True}}
        h = types.SimpleNamespace(my_edit=original,run_recipe=run_recipe,HP_BASE=None,ARM_HOOKS=[],_LAW5_DEFAULT_CTX=False)
        e = object.__new__(E.Evaluator); e.H = h; e.original = original
        e.wrapper = E.OracleEdit(h,lambda:None,lambda *a:{})
        h.my_edit = e.wrapper
        e.maps = {}; e.unit_times = {"recipe_setup_seconds":[],"closedform_arm_seconds":[],"oracle_arm_seconds":[]}
        e.restore = lambda:None; e.assert_base = lambda:None; e.band_hash = lambda:{}; e.guard = lambda *a:None
        previous = sys.gettrace()
        e.run_recipe("closedform",(),{})
        self.assertIs(sys.gettrace(),previous)
        self.assertIn(("recipe",True),observed)
        self.assertIn(("original",True),observed)
        self.assertEqual([v for k,v in observed if k == "nested"],[False,False])

    def test_null_hash_records_zero_application_before_restore_for_reader(self):
        for mutated in (False,True):
            with self.subTest(mutated=mutated):
                data = phase("P1"); baseline = data["base_band_hash"]; state = {"hash":dict(baseline)}
                e = object.__new__(E.Evaluator)
                e.H = types.SimpleNamespace(CANON="{}",_LAW5_DEFAULT_CTX=False,my_edit=lambda *a:{},
                                            req=lambda c,s,v:{"subject":s,"target_new":{"str":" "+v}})
                e.maps = {R.A7:{"s":"v"}}; e.hp = None; e.unit_times = {}; e.base_hash = baseline
                e.band_hash = lambda:dict(state["hash"])
                e.restore = lambda:state.update(hash=dict(baseline))
                # Isolate the recorded evidence from the independent immediate assertion.
                e.assert_base = lambda:None
                def apply(*args):
                    if mutated: state["hash"]["4"] = "b"*64
                    return {}
                e.wrapper = E.OracleEdit(e.H,e.assert_base,apply)
                e.u = data["u"]; e.u_detail = data["u_detail"]; e.axes_base = {}; e.desc_base = {}
                e.evaluate_map = lambda *a:(copy.deepcopy(e.u[R.A7]),copy.deepcopy(e.u_detail[R.A7]))
                data["law5_null"] = e.null()
                self.assertEqual(state["hash"],baseline)
                self.assertEqual(R.read_measurement({"P1":data})["status"],"INVALID" if mutated else "INCOMPLETE")

    def test_training_offline_environment_precedes_transformers_import(self):
        import builtins
        import os
        seen = []
        original_import = builtins.__import__
        def observe(name,*args,**kwargs):
            if name in ("transformers","huggingface_hub"):
                seen.append((name,os.environ.get("HF_HOME"),os.environ.get("HF_HUB_OFFLINE")))
                raise R.Halt("HALT: stopped at import")
            return original_import(name,*args,**kwargs)
        with tempfile.TemporaryDirectory() as td:
            d = Path(td); (d/"train").mkdir()
            R.write_json(d/"preflight.json",{"phase":"P1"}); R.write_json(d/"step0.json",{})
            with patch.dict(sys.modules,_fake_modules()), patch.dict(os.environ,{"HF_HOME":"wrong","HF_HUB_OFFLINE":"0"}), \
                 patch.object(R,"entry_preflight",lambda *a,**k:ROOT), patch.object(R,"load_frozen",lambda *a:{}), \
                 patch.object(R,"frozen_provenance",lambda *a:{}), patch.object(T,"require_training_preflight",lambda *a:None), \
                 patch.object(builtins,"__import__",observe):
                with self.assertRaisesRegex(R.Halt,"stopped at import"): T.run_attempt(d,d,R.TRAIN_UNITS["P1"][0],400)
            self.assertEqual(seen,[("transformers",str(R.ROOT/"data/hf_cache"),"1")])


class DupDevTests(unittest.TestCase):
    """§9 A-dupdev: run the real MMLU producer with synthetic source-schema inputs."""
    revision = "c30699e8356da336a370243923dbaf21066bb9fe"
    old_prereg_sha = "2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344"

    def _row(self, subject, index):
        return {"subject":subject,"question":subject+" question "+str(index),
                "choices":["choice "+c for c in "ABCD"],"answer":index%4}

    source_sha = {"dev":"2b19bde1ed8ca6b482fb283abc90e8e0d9d228947029c0b91795d64b28b3bc3f",
                  "test":"74a41822ce7d3def56e1682f958469c04642a5336a5ce912fa375fdb90fb25d7"}

    def _producer(self, dev_count=5, duplicate=True, split_count=None, wrong_hash=None,
                  source_revision=None):
        class Dataset(list): pass
        class Tokenizer:
            def __call__(s,text,add_special_tokens=True):
                suffix = text[-2:]
                if suffix in (" A"," B"," C"," D"):
                    return {"input_ids":[ord(c) for c in text[:-2]]+[1001+"ABCD".index(suffix[1])]}
                return {"input_ids":[ord(c) for c in text]}
        dev = Dataset()
        for subject in ("filler_"+str(i) for i in range(10)):
            dev.extend(self._row(subject,i) for i in range(5))
        physics = [self._row("college_physics",i) for i in range(dev_count)]
        if duplicate and dev_count >= 4: physics[3] = copy.deepcopy(physics[0])
        dev.extend(physics)  # Real halt shape: identical college_physics source rows 50 and 53.
        dev.extend(self._row("clean",i) for i in range(5))
        repeated = [self._row("unsampled_duplicate",i) for i in range(5)]
        repeated[2] = copy.deepcopy(repeated[0]); repeated[4] = copy.deepcopy(repeated[0])
        dev.extend(repeated)
        dev.extend(self._row("unsampled_four_rows",i) for i in range(4))
        dev.extend(self._row("unsampled_six_rows",i) for i in range(6))
        while len(dev)<285:
            n=len(dev); subject="padding_"+str((n-75)//5)
            dev.append(self._row(subject,n))
        test = Dataset(self._row("college_physics" if i in (1427,1453) else "clean",1000+i) for i in range(14042))
        sources = {"test":test,"dev":dev}
        if split_count is not None:
            split,delta=split_count
            if delta<0: sources[split].pop()
            else: sources[split].append(self._row("unsampled_extra",0))
        hub = types.ModuleType("huggingface_hub"); datasets = types.ModuleType("datasets")
        head_calls=[]; dataset_calls=[]; download_calls=[]
        def dataset_info(name):
            self.assertEqual(name,"cais/mmlu")
            head_calls.append(name)
            return types.SimpleNamespace(sha=self.revision)
        hub.HfApi = lambda:types.SimpleNamespace(dataset_info=dataset_info)
        def load_dataset(name,config,split,revision):
            dataset_calls.append((name,config,split,revision))
            return sources[split]
        datasets.load_dataset = load_dataset
        real_file_ref=R.file_ref
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            for split,rows in sources.items():
                path = Path(td)/(split+".arrow"); path.write_text(json.dumps(rows))
                rows.cache_files = [{"filename":str(path)}]
            def download(repo_id,filename,repo_type,revision):
                download_calls.append((repo_id,filename,repo_type,revision))
                path=Path(td)/"hub/datasets--cais--mmlu/snapshots"/(source_revision or self.revision)/filename
                path.parent.mkdir(parents=True,exist_ok=True); path.write_text("synthetic cached source")
                return str(path)
            hub.hf_hub_download=download
            def file_ref(path):
                ref=real_file_ref(path)
                for split,sha in self.source_sha.items():
                    if Path(path).name==split+"-00000-of-00001.parquet":
                        ref["sha256"]="0"*64 if wrong_hash==split else sha
                return ref
            with patch.dict(sys.modules,{"huggingface_hub":hub,"datasets":datasets}), patch.object(R,"file_ref",side_effect=file_ref):
                record = S.freeze_mmlu(Tokenizer())
        sources["head_calls"]=head_calls; sources["dataset_calls"]=dataset_calls; sources["download_calls"]=download_calls
        return record, sources

    def _accepted(self, **kwargs):
        try: return self._producer(**kwargs)
        except R.Halt as exc: self.fail("published five-row fixture was refused: "+str(exc))

    def _expected_prompt(self, row, examples):
        # Independent golden format of the pre-amendment five-shot producer.
        prompt = "The following are multiple choice questions (with answers) about "+row["subject"].replace("_"," ")+".\n\n"
        for example in examples:
            prompt += example["question"]+"\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: "+"ABCD"[example["answer"]]+"\n\n"
        return prompt+row["question"]+"\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer:"

    def _step_record(self, directory, mmlu, prereg_sha):
        R.write_json(directory/"mmlu200.json",mmlu)
        step = {"status":"PASS","prereg_sha256":prereg_sha,
                "files":{"mmlu200":R.file_ref(directory/"mmlu200.json")},
                "sources":{"prereg":R.file_ref(ROOT/"experiments/c10w/design/C10W_ORACLE_PREREG.md")},
                "seal":{s:True for s in ("S1","S2","S2c","S2d","S3","S4","S5","S6","S7")},
                "seam":{"ok":True},"fingerprint":{"ok":True},"instrument_ok":True}
        R.write_json(directory/"step0.json",step)

    def test_duplicate_five_rows_accepted_and_preserved_in_source_order(self):
        record, sources = self._accepted()
        physics = [item for item in record["items"] if item["subject"]=="college_physics"]
        self.assertEqual(len(physics),2)
        for item in physics:
            self.assertEqual([i["source_index"] for i in item["dev_identities"]],[50,51,52,53,54])
            self.assertEqual(item["dev_examples"],list(sources["dev"][50:55]))
            self.assertEqual(item["prompt"],self._expected_prompt(sources["test"][item["source_index"]],sources["dev"][50:55]))
            self.assertEqual(item["prompt"].count("college_physics question 0\n"),2)
            self.assertIn("dev_distinct_n",item); self.assertIn("dev_duplicate_source_indices",item)
            self.assertEqual(item["dev_distinct_n"],4)
            self.assertEqual(item["dev_duplicate_source_indices"],[53])
            self.assertEqual(len({i["row_sha256"] for i in item["dev_identities"]}),4)
        self.assertEqual(record["sample_seed"],20261007)
        self.assertEqual(record["sampled_indices"],random.Random(20261007).sample(range(14042),200))
        self.assertEqual(record["revision"],self.revision)

    def test_four_dev_rows_refused_as_invalid_instrument(self):
        with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT: exactly five dev rows required"):
            self._producer(dev_count=4,duplicate=False)

    def test_six_dev_rows_refused_as_invalid_instrument(self):
        with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT: exactly five dev rows required"):
            self._producer(dev_count=6,duplicate=False)

    def test_zero_to_three_dev_rows_refused_as_invalid_instrument(self):
        for count in range(4):
            with self.subTest(count=count):
                try: self._producer(dev_count=count,duplicate=False)
                except R.Halt as exc:
                    self.assertIn("INVALID-INSTRUMENT: exactly five dev rows required",str(exc))
                except KeyError as exc:
                    self.fail("missing dev set must halt as INVALID-INSTRUMENT: "+str(exc))
                else: self.fail("fewer than five dev rows were accepted")

    def test_five_distinct_rows_keep_pre_amendment_prompt_bytes(self):
        record, sources = self._accepted(duplicate=False)
        item = next(x for x in record["items"] if x["source_index"]==1427)
        expected = self._expected_prompt(sources["test"][1427],sources["dev"][50:55])
        self.assertEqual(item["prompt"].encode("utf-8"),expected.encode("utf-8"))
        self.assertEqual(item["prompt_utf8_sha256"],R.sha_text(expected))
        self.assertIn("dev_distinct_n",item); self.assertIn("dev_duplicate_source_indices",item)
        self.assertEqual(item["dev_distinct_n"],5)
        self.assertEqual(item["dev_duplicate_source_indices"],[])

    def test_whole_dev_summary_includes_exactly_low_distinct_subjects(self):
        record, sources = self._accepted()
        self.assertIn("dev_less_than_five_distinct",record)
        expected = {"college_physics":{"dev_distinct_n":4,"dev_duplicate_source_indices":[53]},
                    "unsampled_duplicate":{"dev_distinct_n":3,"dev_duplicate_source_indices":[62,64]},
                    "unsampled_four_rows":{"dev_distinct_n":4,"dev_duplicate_source_indices":[]}}
        self.assertEqual(record["dev_less_than_five_distinct"],expected)
        self.assertEqual({item["subject"] for item in record["items"]},{"college_physics","clean"})
        self.assertNotIn("unsampled_six_rows",record["dev_less_than_five_distinct"])

    def test_producer_record_json_roundtrip_keeps_new_fields(self):
        record, sources = self._accepted()
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            path = Path(td)/"mmlu200.json"; R.write_json(path,record)
            loaded = R.load_json(path)
            normalised = json.loads(json.dumps({**record,"class":R.CLASS,"decision_id":R.DECISION_ID}))
            self.assertEqual(loaded,normalised)
            R.verify_ref(R.file_ref(path))
            self.assertEqual(loaded["dev_less_than_five_distinct"]["college_physics"]["dev_duplicate_source_indices"],[53])
            self.assertTrue(all("dev_distinct_n" in item and "dev_duplicate_source_indices" in item for item in loaded["items"]))

    def test_reader_accepts_actual_amended_prereg_hash(self):
        actual = R.sha_file(ROOT/"experiments/c10w/design/C10W_ORACLE_PREREG.md")
        self.assertEqual(R.PREREG_SHA,actual)
        self.assertNotEqual(actual,self.old_prereg_sha)
        record, sources = self._accepted(duplicate=False)
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            directory = Path(td); self._step_record(directory,record,actual)
            frozen = R.load_frozen(directory)
            self.assertEqual(frozen["prereg_sha256"],actual)
            self.assertEqual(R.load_json(frozen["files"]["mmlu200"]["path"])["items"],record["items"])

    def test_reader_rejects_old_prereg_hash(self):
        record, sources = self._accepted(duplicate=False)
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            directory = Path(td); self._step_record(directory,record,self.old_prereg_sha)
            with self.assertRaisesRegex(R.Halt,"frozen prereg mismatch"): R.load_frozen(directory)

    def test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head(self):
        record,sources=self._accepted(duplicate=False)
        self.assertEqual(sources["head_calls"],[])
        self.assertEqual(sources["dataset_calls"],[("cais/mmlu","all",s,self.revision) for s in ("test","dev")])
        self.assertEqual(sources["download_calls"],[("cais/mmlu","all/"+s+"-00000-of-00001.parquet","dataset",self.revision) for s in ("test","dev")])
        self.assertEqual(record["split_counts"],{"test":14042,"dev":285})
        for split,sha in self.source_sha.items():
            canonical=[r for r in record["source_files"][split] if Path(r["path"]).name==split+"-00000-of-00001.parquet"]
            self.assertEqual(len(canonical),1); self.assertEqual(canonical[0]["sha256"],sha)
            self.assertTrue(any(Path(r["path"]).suffix==".arrow" for r in record["source_files"][split]))

    def test_each_split_count_off_by_one_is_invalid_instrument(self):
        for split in ("test","dev"):
            for delta in (-1,1):
                with self.subTest(split=split,delta=delta), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*split count"):
                    self._producer(duplicate=False,split_count=(split,delta))

    def test_each_wrong_canonical_source_hash_is_invalid_instrument(self):
        for split in ("test","dev"):
            with self.subTest(split=split), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*source file hash"):
                self._producer(duplicate=False,wrong_hash=split)

    def test_different_source_revision_is_invalid_instrument(self):
        with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*source revision"):
            self._producer(duplicate=False,source_revision="f"*40)

    def test_duplicates_use_existing_identity_hash_without_rehashing_rows(self):
        with patch.object(R,"sha_text",wraps=R.sha_text) as digest:
            record,sources=self._accepted()
        self.assertEqual(digest.call_count,14042+285+200)
        for item in record["items"]:
            seen=set(); repeats=[]
            for identity in item["dev_identities"]:
                if identity["row_sha256"] in seen: repeats.append(identity["source_index"])
                seen.add(identity["row_sha256"])
            self.assertEqual((item["dev_distinct_n"],item["dev_duplicate_source_indices"]),(len(seen),repeats))

    def test_real_cached_acquisition_and_tokenizer_exercise_every_require(self):
        if os.environ.get("C10W_SELFTEST_ALLOW_TOKENIZER") != "1":
            self.skipTest("tokenizer loading requires explicit C10W_SELFTEST_ALLOW_TOKENIZER=1")
        cache=ROOT/"data/hf_cache"
        pinned=[cache/"hub/datasets--cais--mmlu/snapshots"/self.revision/"all"/(s+"-00000-of-00001.parquet") for s in ("test","dev")]
        tokenizer=cache/"hub/models--Qwen--Qwen2.5-3B/snapshots"/R.MODEL_REV
        pinned.extend(tokenizer/n for n in ("tokenizer.json","tokenizer_config.json","vocab.json","merges.txt"))
        missing=[str(p) for p in pinned if not p.is_file()]
        if missing: self.skipTest("cached pinned dataset/tokenizer files absent: "+", ".join(missing))
        code=r'''
import ast, importlib.abc, json, os, shutil, sys, tempfile
from pathlib import Path
root=Path(sys.argv[1]); revision=sys.argv[2]
class NoTensorImports(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split(".")[0] in {"torch","tensorflow","jax"}:
            return importlib.machinery.ModuleSpec(fullname,self)
    def create_module(self,spec): return None
    def exec_module(self,module):
        raise AssertionError("offline tokenizer check attempted tensor import: "+module.__name__)
sys.meta_path.insert(0,NoTensorImports())
sys.path.insert(0,str(root/"code/lab/track_c"))
with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
    cached=root/"data/hf_cache/datasets/cais___mmlu/all/0.0.0"/revision
    local=Path(td)/"datasets/cais___mmlu/all/0.0.0"/revision
    local.mkdir(parents=True)
    for name in ("dataset_info.json","mmlu-test.arrow","mmlu-dev.arrow"):
        shutil.copyfile(cached/name,local/name)
    os.environ["HF_DATASETS_CACHE"]=str(Path(td)/"datasets")
    import c10w_oracle_read as r, c10w_oracle_step0 as s
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(r.MODEL_ID,revision=r.MODEL_REV,cache_dir=str(root/"data/hf_cache/hub"),local_files_only=True)
    calls=set(); previous=r.require
    def require(ok,reason):
        frame=sys._getframe(1)
        if frame.f_code.co_filename==s.__file__: calls.add(frame.f_lineno)
        return previous(ok,reason)
    r.require=require
    frozen=s.freeze_mmlu(tok)
    function=next(n for n in ast.parse(Path(s.__file__).read_text()).body if isinstance(n,ast.FunctionDef) and n.name=="freeze_mmlu")
    expected={n.lineno for n in ast.walk(function) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="R" and n.func.attr=="require"}
    assert expected<=calls,("unexercised require sites",sorted(expected-calls))
    assert frozen["revision"]==revision and frozen["split_counts"]=={"test":14042,"dev":285}
    summary=frozen["dev_less_than_five_distinct"]
    assert summary=={"college_physics":{"dev_distinct_n":4,"dev_duplicate_source_indices":[53]}},summary
    dev=frozen["source_identities"]["dev"]; duplicate_sha=dev[53]["row_sha256"]
    group=[x["source_index"] for x in dev if x["row_sha256"]==duplicate_sha]
    assert group==[50,53],group
    affected=sorted(x["source_index"] for x in frozen["items"] if x["subject"]=="college_physics")
    assert affected==[1427,1453],affected
    failures=sum(not item["prompt"].endswith("Answer:") or any(tok(item["prompt"]+" "+c)["input_ids"]!=item["prompt_ids"]+[frozen["answer_mapping"][c]["token_id"]] for c in "ABCD") for item in frozen["items"])
    assert len(frozen["items"])==200 and failures==0,failures
    assert "torch" not in sys.modules and os.environ["HF_HUB_OFFLINE"]=="1"
    print("C10W_DUPDEV_REAL_DATA PASS: test=14042 dev=285 subject=college_physics duplicate_group="+json.dumps(group)+" affected="+json.dumps(affected)+" suffix_failures=0/200 require_sites="+str(len(expected))+"/"+str(len(expected))+"; offline; no tensor imports or model load")
'''
        environment=dict(__import__("os").environ,HF_HUB_OFFLINE="1",HF_DATASETS_OFFLINE="1",TRANSFORMERS_OFFLINE="1",
                         HF_HOME=str(cache),USE_TORCH="0",USE_TF="0",USE_FLAX="0",CUDA_VISIBLE_DEVICES="",TMPDIR="/private/tmp")
        run=subprocess.run([sys.executable,"-B","-c",code,str(ROOT),self.revision],env=environment,capture_output=True,text=True,timeout=120)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        self.assertIn("C10W_DUPDEV_REAL_DATA PASS",run.stdout)
        print(run.stdout.strip())

    def test_report_only_198_sensitivity_keeps_full_200_gate_and_label(self):
        indices=random.Random(20261007).sample(range(14042),200)
        unaffected=[i for i in indices if i not in (1427,1453)]
        def score(bits,pre):
            predicted=["A" if hit else "B" for hit in bits]
            lost=sum(p and not q for p,q in zip(pre,bits)); gained=sum(not p and q for p,q in zip(pre,bits))
            return {"n":200,"correct":bits,"predicted":predicted,"correct_n":sum(bits),"accuracy":sum(bits)/200.,
                    "correct_to_wrong":lost,"wrong_to_correct":gained,"net_paired_loss":lost-gained,
                    "rows":[{"source_index":i,"predicted":prediction,"correct":hit} for i,prediction,hit in zip(indices,predicted,bits)]}
        for remaining,contribution,full,label in ((2,2,4,"PASS-CEILING"),(3,2,5,"PARTIAL-CEILING-LOCALITY-COST"),
                                                   (5,-1,4,"PASS-CEILING"),(6,-2,4,"PASS-CEILING")):
            with self.subTest(remaining=remaining,contribution=contribution):
                data=fixture(); pre=[not(contribution<0 and i in (1427,1453)) for i in indices]
                lost=set(unaffected[:remaining]); gained=set((1427,1453)[:max(0,-contribution)])
                post=[False if i in lost or (contribution>0 and i in (1427,1453)) else True if i in gained else bit for i,bit in zip(indices,pre)]
                for p in data.values():
                    for a in p["u"].values(): a["extra"]["mmlu"]=score(list(pre),pre)
                    p["law5_null"]["arm"]["extra"]["mmlu"]=score(list(pre),pre)
                    for recipe_name,rec in p["recipes"].items():
                        for a in rec["arms"].values(): a["extra"]["mmlu"]=score(list(pre if recipe_name=="closedform" else post),pre)
                expected_label=R.replicated(R.configuration(data["P1"],"oracle_p1"),R.configuration(data["P2"],"oracle_s1"),R.configuration(data["P2"],"oracle_s0rt"))["label"]
                self.assertEqual(expected_label,label)
                original=copy.deepcopy(data); reading=R.read_measurement(data)
                self.assertEqual(reading["final_label"],expected_label); self.assertEqual(data,original)
                self.assertIn("g6_sensitivity",reading)
                for phase_name,recipe_name in (("P1","oracle_p1"),("P2","oracle_s1"),("P2","oracle_s0rt")):
                    sensitivity=reading["g6_sensitivity"][phase_name][recipe_name][R.A7]
                    self.assertEqual(sensitivity,{"full_n":200,"full_net_paired_loss":full,"excluding_affected_n":198,
                        "excluding_affected_net_paired_loss":remaining,"affected_source_indices":[1427,1453],
                        "affected_signed_contribution":contribution,"report_only":True})
                self.assertEqual(reading["ranks"]["16"]["gate_misses"],["G6"] if full>4 else [])


class P2RerunTests(unittest.TestCase):
    def module(self):
        self.assertTrue((ROOT/"code/lab/runners/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
        return importlib.import_module("c10w_p2_rerun")

    @contextlib.contextmanager
    def tree(self, amended=True, archived=False):
        A=self.module()
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root=Path(td); plan=copy.deepcopy(A.AMENDMENT)
            step0=(root/plan["step0"]["path"]).parent; step0.mkdir(parents=True)
            p2=root/plan["p2_directory"]; p2.mkdir(parents=True)
            logs=root/"experiments/c10w/runs/c10w_oracle/logs"; logs.mkdir()
            (root/"architecture_profile").mkdir()
            (root/plan["diagnostic_path"]).write_text('{"cpu_fixture":true}\n')
            prereg=root/"experiments/c10w/design/C10W_ORACLE_PREREG.md"; prereg.parent.mkdir()
            shutil.copyfile(ROOT/"experiments/c10w/design/C10W_ORACLE_PREREG.md",prereg)
            evaluator=root/plan["evaluator"]["path"]; evaluator.parent.mkdir(parents=True)
            text=(HERE/"c10w_oracle_eval.py").read_text()
            old=text.replace('.flatten().double()','.flatten()')
            new=old.replace('(x["B_"+str(l)]@x["A_"+str(l)]).flatten()', '(x["B_"+str(l)]@x["A_"+str(l)]).flatten().double()').replace('(y["B_"+str(l)]@y["A_"+str(l)]).flatten()', '(y["B_"+str(l)]@y["A_"+str(l)]).flatten().double()')
            evaluator.write_text(old)
            sources={"evaluator":R.file_ref(evaluator)}
            for key in ("reader","trainer","step0_source","harness"):
                source=root/"code/lab/track_c"/(key+".py"); source.write_text("# frozen "+key+"\n")
                sources[key]=R.file_ref(source)
            files={}
            for key in ("train_inputs","mmlu200","seal_audit"):
                path=step0/(key+".json"); path.write_text('{}\n'); files[key]=R.file_ref(path)
            frozen={"status":"PASS","prereg_sha256":R.PREREG_SHA,"sources":sources,"files":files,
                    "seal":{k:True for k in ("S1","S2","S2c","S2d","S3","S4","S5","S6","S7")},
                    "seam":{"ok":True},"fingerprint":{"ok":True},"instrument_ok":True}
            R.write_json(step0/"step0.json",frozen); plan["step0"]["sha256"]=R.sha_file(step0/"step0.json")
            plan["evaluator"]["old_sha256"]=R.sha_text(old); plan["evaluator"]["new_sha256"]=R.sha_text(new)
            import difflib
            diff=''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),
                          fromfile='a/'+plan["evaluator"]["path"],tofile='b/'+plan["evaluator"]["path"]))
            dpath=root/plan["unified_diff"]["path"]; dpath.parent.mkdir(); dpath.write_text(diff)
            plan["unified_diff"]["sha256"]=R.sha_text(diff)
            pin=R.sha_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
            p1=root/A.P1_REL; p1.mkdir()
            R.write_json(p2/"preflight.json",{"p1_directory":str(p1),"wall_seconds":1.})
            for stage in R.TRAIN_STAGES["P2"]: (logs/(stage+".log")).write_text("fixture\nSTAGE_EXIT=0\n")
            for name in ("HALT.json","eval.json","eval_halt.json"):
                record={"status":"HALT" if name!="eval.json" else "PASS","phase":"P2","stage":"p2-eval",
                        "reason":"HALT: invalid same-seed cosine","wall_seconds":6209.}
                R.write_json(p2/name,record)
            (p2/"p2-eval.log").write_text("fixture eval\nSTAGE_EXIT=2\n")
            (logs/"p2-eval.log").write_text("fixture outer\nSTAGE_EXIT=2\n")
            R.write_json(logs/"p2-eval.gate.20261007T222229.91288.json",{"stage":"p2-eval","ok":True})
            (p2/"train").mkdir(); (p2/"train/keep.json").write_text("training sentinel")
            (p2/"adapters").mkdir(); (p2/"adapters/keep.safetensors").write_text("adapter sentinel")
            originals=[*(p2/n for n in A.INNER),logs/"p2-eval.log",*logs.glob("p2-eval.gate.*.json")]
            hashes={str(p.relative_to(root)):R.sha_file(p) for p in originals}
            with patch.object(A,"W",root),patch.object(A,"AMENDMENT",plan),patch.object(A,"AMENDMENT_SHA256",pin), \
                 patch.object(A,"ORIGINAL_ATTEMPT_SHA256",hashes,create=True),patch.object(R,"ROOT",root):
                if amended:
                    evaluator.write_text(new); A.prepare()
                if archived: A.archive()
                yield A,root,step0,p2,logs,evaluator,new

    def gate_record(self,A,p2,logs):
        evidence=A.check_reattempt(p2)
        path=logs/"p2-eval.gate.fixture.json"
        R.write_json(path,{"stage":"p2-eval","ok":True,"checks":{
            "fingerprint":{"ok":True},"gpu":{"ok":True},
            "dispatch_guards":{"ok":True,"p2_directory":str(p2),"reattempt":evidence}}})
        return path

    def test_identical_full_size_fp32_delta_uses_production_float64_cosine(self):
        code=r'''
import ast, importlib.abc, json, sys
from pathlib import Path
class NoModel(importlib.abc.MetaPathFinder):
    def find_spec(self,name,path=None,target=None):
        if name.split('.')[0] in {'transformers','tokenizers','datasets'}: raise AssertionError('model/tokenizer import')
sys.meta_path.insert(0,NoModel())
import torch
torch.set_num_threads(1)
gen=torch.Generator(device='cpu').manual_seed(20261008)
delta_a=torch.randn((2048,11008),generator=gen,dtype=torch.float32,device='cpu'); delta_b=delta_a.clone()
a,b=delta_a.flatten(),delta_b.flatten()
old=float(torch.dot(a,b))/float(a.norm()*b.norm())
tree=ast.parse(Path(sys.argv[1]).read_text())
loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and any(isinstance(c,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='cosines' for t in c.targets) for c in n.body))
class Deltas(ast.NodeTransformer):
    def visit_BinOp(self,node):
        if isinstance(node.op,ast.MatMult):
            name=node.left.value.id
            assert name in ('x','y')
            return ast.copy_location(ast.Name(id='delta_a' if name=='x' else 'delta_b',ctx=ast.Load()),node)
        return self.generic_visit(node)
block=ast.fix_missing_locations(Deltas().visit(ast.Module(body=loop.body,type_ignores=[])))
class Reader:
    def require(self,ok,reason): assert ok,reason
scope={'torch':torch,'R':Reader(),'delta_a':delta_a,'delta_b':delta_b,'l':4,'cosines':{}}
exec(compile(block,'production_cosine','exec'),scope)
print(json.dumps({'old':old,'new':scope['cosines']['4'],'device':str(delta_a.device),'shape':list(delta_a.shape),'dtype':str(delta_a.dtype)}))
'''
        proc=subprocess.run([str(ROOT/".venv/bin/python"),"-B","-c",code,str(HERE/"c10w_oracle_eval.py")],
                            env=dict(os.environ,CUDA_VISIBLE_DEVICES=""),capture_output=True,text=True,timeout=60)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        result=json.loads(proc.stdout); print("C10W_COSINE_CPU "+json.dumps(result))
        self.assertEqual(result["shape"],[2048,11008]); self.assertEqual(result["device"],"cpu")
        self.assertGreater(abs(result["old"]-1.),1e-9)
        self.assertLessEqual(abs(result["new"]-1.),1e-9)
        data=phase("P2"); data["same_seed"]["per_layer_cosine"]={str(l):result["new"] for l in R.BAND}
        R.validate_phase(data)

    def test_original_evaluator_passes_without_amendment(self):
        with self.tree(amended=False) as (A,root,step0,p2,logs,evaluator,new):
            with A.overlay(): self.assertEqual(R.load_frozen(step0)["sources"]["evaluator"]["sha256"],R.sha_file(evaluator))

    def test_amended_evaluator_requires_valid_pinned_amendment(self):
        with self.tree(amended=False) as (A,root,step0,p2,logs,evaluator,new):
            evaluator.write_text(new)
            with A.overlay(), self.assertRaises(R.Halt): R.load_frozen(step0)
            ref=A.prepare(); before=(step0/"step0.json").read_bytes()
            with A.overlay(): self.assertEqual(R.load_frozen(step0)["evaluator_amendment"],ref)
            self.assertEqual((step0/"step0.json").read_bytes(),before)
            self.assertEqual(A.prepare(),ref)

    def test_amendment_diff_and_evaluator_tampering_fail_closed(self):
        for which in ("amendment","diff","evaluator"):
            with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
                path=step0/"amendment_A1_evaluator.json" if which=="amendment" else root/A.AMENDMENT["unified_diff"]["path"] if which=="diff" else evaluator
                path.write_bytes(path.read_bytes()+b' ')
                with A.overlay(),self.assertRaises(R.Halt): R.load_frozen(step0)

    def test_every_other_frozen_source_remains_strict_and_verifier_restored(self):
        for which in ("reader","trainer","step0_source","harness"):
            with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
                original=R.verify_ref
                ref=R.load_json(step0/"step0.json")["sources"][which]
                Path(ref["path"]).write_text("changed")
                with A.overlay(),self.assertRaises(R.Halt): R.load_frozen(step0)
                self.assertIs(R.verify_ref,original)

    def test_archive_moves_exact_set_hashes_and_preserves_training(self):
        with self.tree() as (A,root,step0,p2,logs,evaluator,new):
            before=artifact_snapshot(root); expected={str((p2/n).relative_to(root)) for n in ("HALT.json","eval.json","eval_halt.json","p2-eval.log")}
            expected|={str((logs/n).relative_to(root)) for n in ("p2-eval.log","p2-eval.gate.20261007T222229.91288.json")}
            digests={p:R.sha_file(root/p) for p in expected}; sentinel=(p2/"train/keep.json").read_bytes()
            ref=A.archive(); manifest=R.load_json(ref["path"])
            self.assertEqual({e["source"] for e in manifest["files"]},expected)
            for entry in manifest["files"]:
                self.assertFalse((root/entry["source"]).exists())
                self.assertEqual(entry["sha256"],digests[entry["source"]])
                self.assertEqual(R.sha_file(root/entry["destination"]),entry["sha256"])
            self.assertEqual((p2/"train/keep.json").read_bytes(),sentinel)
            self.assertEqual((p2/"adapters/keep.safetensors").read_text(),"adapter sentinel")
            self.assertEqual(A.verify_archive(),ref)

    def test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves(self):
        for defect in ("missing","unexpected","verdict","symlink","partial"):
            with self.subTest(defect=defect),self.tree() as (A,root,step0,p2,logs,evaluator,new):
                if defect=="missing": (p2/"eval_halt.json").unlink()
                elif defect=="unexpected": (p2/"eval_surprise.json").write_text('{}')
                elif defect=="verdict": (p2/"verdict.json").write_text('{}')
                elif defect=="symlink":
                    (p2/"p2-eval.log").unlink(); (p2/"p2-eval.log").symlink_to(logs/"p2-eval.log")
                else: (p2/"attempt1_halted").mkdir()
                before=artifact_snapshot(root)
                with self.assertRaises(R.Halt): A.archive()
                self.assertEqual(artifact_snapshot(root),before)

    def test_archive_idempotent_even_after_new_eval_files_exist(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            ref=A.verify_archive(); before=artifact_snapshot(root)
            self.assertEqual(A.archive(),ref); self.assertEqual(artifact_snapshot(root),before)
            (p2/"eval.json").write_text('{"new_attempt":true}')
            (logs/"p2-eval.log").write_text("new attempt log")
            before=artifact_snapshot(root); self.assertEqual(A.archive(),ref)
            self.assertEqual(artifact_snapshot(root),before)

    def test_archive_manifest_and_archived_file_tampering_refused(self):
        for defect in ("manifest","archived"):
            with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
                ref=A.verify_archive()
                path=Path(ref["path"]) if defect=="manifest" else p2/"attempt1_halted/eval_halt.json"
                path.write_text('{}')
                with self.assertRaises(R.Halt): A.check_reattempt(p2)

    def test_archive_is_bound_to_reviewed_original_bytes(self):
        with self.tree() as (A,root,step0,p2,logs,evaluator,new):
            (p2/"eval.json").write_bytes((p2/"eval.json").read_bytes()+b' ')
            before=artifact_snapshot(root)
            with self.assertRaises(R.Halt): A.archive()
            self.assertEqual(artifact_snapshot(root),before)
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            path=p2/"attempt1_halted/eval.json"; path.write_bytes(path.read_bytes()+b' ')
            manifest=p2/"attempt1_halted/manifest.json"; record=R.load_json(manifest)
            for entry in record["files"]:
                if entry["source"].endswith('/eval.json'):
                    entry.update(sha256=R.sha_file(path),size=path.stat().st_size)
            manifest.write_text(json.dumps(record))
            with self.assertRaises(R.Halt): A.verify_archive()

    def test_public_eval_requires_dispatch_and_consumes_entry_once(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            A.claim_reattempt(p2,self.gate_record(A,p2,logs))
            args=["eval","P2",str(p2),str(step0)]
            with patch.object(E,"run_eval",return_value=0) as backend,patch("sys.stderr",new=io.StringIO()):
                self.assertEqual(A.main(args),2,"public eval bypassed dispatch (test-first RED)")
                backend.assert_not_called()
                captured=[]
                def transport(script,child_args,directory,stage):
                    (p2/"p2-eval.log").write_text("CPU child transport\n")
                    captured.extend(child_args); return 0
                def dispatch(stage):
                    return S.run_child("c10w_oracle_eval.py",["P2",p2,step0],p2,stage)
                with patch.object(S,"dispatch_stage",side_effect=dispatch),patch.object(S,"run_child",side_effect=transport):
                    self.assertEqual(A.main(["dispatch",str(p2)]),0)
                self.assertEqual(len(captured),5)
                with patch.object(A.os,"getppid",return_value=os.getpid()+1): self.assertEqual(A.main(captured),2)
                with patch.object(A.os,"getppid",return_value=os.getpid()):
                    self.assertEqual(A.main(captured),0)
                    self.assertEqual(A.main(captured),2)
                self.assertEqual(backend.call_count,1)
                self.assertTrue((p2/"reattempt2_eval_started.json").is_file())

    def test_public_eval_cli_race_starts_backend_once(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            A.claim_reattempt(p2,self.gate_record(A,p2,logs)); captured=[]
            def transport(script,args,directory,stage):
                (p2/"p2-eval.log").write_text("CPU child transport\n"); captured.extend(args); return 0
            def dispatch(stage): return S.run_child("c10w_oracle_eval.py",["P2",p2,step0],p2,stage)
            with patch.object(S,"dispatch_stage",side_effect=dispatch),patch.object(S,"run_child",side_effect=transport):
                self.assertEqual(A.main(["dispatch",str(p2)]),0)
            self.assertEqual(len(captured),5,"dispatch did not bind the child entry (test-first RED)")
            self.shell_fixture(A,root,logs)
            wrapper=root/"code/lab/runners/c10w_p2_rerun.py"
            bootstrap=wrapper.read_text().split('if __name__=="__main__":')[0]
            wrapper.write_text(bootstrap+'''import c10w_oracle_eval as E
A.os.getppid=lambda: json.loads((A.p2_path()/"reattempt2_dispatch.json").read_text())["dispatcher_pid"]
def backend(*args):
    with (A.W/"child_started.txt").open("a") as f: f.write("eval\\n")
    return 0
E.run_eval=backend
sys.exit(A.main())
''')
            cmd=[str(root/".venv/bin/python"),"-B",str(wrapper),*captured]
            procs=[subprocess.Popen(cmd,cwd=root,env=dict(os.environ,LLMDB_ROOT=str(root)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for _ in range(2)]
            outputs=[p.communicate(timeout=30) for p in procs]
            self.assertEqual(sorted(p.returncode for p in procs),[0,2],outputs)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])
            replay=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=30)
            self.assertEqual(replay.returncode,2)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])

    def test_production_dispatch_eval_and_read_with_cpu_backend(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            data=fixture(); p1=root/A.P1_REL
            (p2/"train/keep.json").unlink()
            for name,directory in (("P1",p1),("P2",p2)):
                (directory/"train").mkdir(exist_ok=True); (directory/"adapters").mkdir(exist_ok=True)
                for record in data[name]["train_records"]:
                    record["provenance"]=R.frozen_provenance(A.load_frozen(step0))
                    tag=R.train_tag(R.train_identity(record),record["steps"])
                    adapter=directory/"adapters"/(tag+".safetensors"); adapter.write_text("CPU synthetic adapter")
                    record["adapter"]=R.file_ref(adapter)
                    path=directory/"train"/(tag+".json"); R.write_json(path,record)
                    record.update(R.load_json(path),record_file=R.file_ref(path))
                data[name].update(step0_directory=str(step0),provenance=R.frozen_provenance(A.load_frozen(step0)))
            R.write_json(p1/"eval.json",data["P1"])
            R.write_json(p1/"verdict.json",{"projection":{"P2_minutes":1.}})
            auth=p1/"authorization_P2.json"
            R.write_json(auth,{"P2":{"authorized":True,"recorded_by":"CPU fixture","recorded_at":"fixture",
                         "p1_eval_sha256":R.sha_file(p1/"eval.json"),"p1_verdict_sha256":R.sha_file(p1/"verdict.json"),"budget_minutes":448}})
            data["P2"].update(authorization=R.file_ref(auth),authorized_projection_minutes=1.,p1_eval_sha256=R.sha_file(p1/"eval.json"))
            A.claim_reattempt(p2,self.gate_record(A,p2,logs))
            def backend(phase,directory,frozen):
                self.assertEqual((phase,Path(directory),Path(frozen)),("P2",p2,step0))
                R.write_json(p2/"eval.json",data["P2"])
                R.write_json(p2/"verdict.json",R.read_measurement(R.disk_phases(p1)))
                return 0
            def transport(script,args,directory,stage):
                with (p2/"p2-eval.log").open("x") as log:
                    with patch.object(A.os,"getppid",return_value=os.getpid()): rc=A.main(args)
                    log.write("STAGE_EXIT="+str(rc)+"\n")
                return rc
            with patch.object(R,"entry_preflight",return_value=root),patch.object(T,"require_training_preflight",return_value=None), \
                 patch.object(R,"require_untracked_adapter",return_value=None),patch.object(S,"run_child",side_effect=transport), \
                 patch.object(E,"run_eval",side_effect=backend) as evaluator_backend,patch("sys.stdout",new=io.StringIO()) as output:
                self.assertEqual(A.main(["dispatch",str(p2)]),0)
                self.assertEqual(evaluator_backend.call_count,1)
                output.seek(0); output.truncate()
                self.assertEqual(A.main(["read"]),0,output.getvalue())
                reading=json.loads(output.getvalue())
                before=artifact_snapshot(root)
                with patch("sys.stderr",new=io.StringIO()): self.assertEqual(A.main(["dispatch",str(p2)]),2)
                self.assertEqual(artifact_snapshot(root),before,"dispatch replay changed successful records (test-first RED)")
            for record in (R.load_json(p2/"eval.json"),R.load_json(p2/"verdict.json"),reading):
                self.assertEqual(record["evaluator_amendment"],A.verify_amendment())
            self.assertEqual(reading["status"],"VALID")

    def test_public_dispatch_cli_race_and_replay_never_halt_winner(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            A.claim_reattempt(p2,self.gate_record(A,p2,logs))
            self.shell_fixture(A,root,logs)
            (p2/"train/keep.json").unlink()
            for index,record in enumerate(phase("P2")["train_records"]): R.write_json(p2/"train"/(str(index)+".json"),record)
            R.write_json(root/A.P1_REL/"authorization_P2.json",{"P2":{"budget_minutes":448}})
            wrapper=root/"code/lab/runners/c10w_p2_rerun.py"; bootstrap=wrapper.read_text().split('if __name__=="__main__":')[0]
            wrapper.write_text(bootstrap+'''import c10w_oracle_eval as E, c10w_oracle_step0 as S, c10w_oracle_train as T
A.R.entry_preflight=lambda: A.W
S.ensure_authorized=lambda phase,p1: ({"path":"CPU fixture","sha256":"0"*64},1.)
T.require_training_preflight=lambda *args: None
A.R.phase_trains=lambda *args: []
A.os.getppid=lambda: os.getpid()
def backend(*args):
    with (A.W/"child_started.txt").open("a") as f: f.write("eval\\n")
    A.R.write_json(A.p2_path()/"eval.json",{"fixture":True})
    return 0
def transport(script,args,directory,stage):
    with (directory/(stage+".log")).open("x") as f:
        rc=A.main(args); f.write("STAGE_EXIT="+str(rc)+"\\n")
    return rc
E.run_eval=backend; S.run_child=transport
sys.exit(A.main())
''')
            cmd=[str(root/".venv/bin/python"),"-B",str(wrapper),"dispatch",str(p2)]
            procs=[subprocess.Popen(cmd,cwd=root,env=dict(os.environ,LLMDB_ROOT=str(root)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for _ in range(2)]
            outputs=[p.communicate(timeout=30) for p in procs]
            self.assertEqual(sorted(p.returncode for p in procs),[0,2],outputs)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])
            self.assertFalse((p2/"HALT.json").exists())
            self.assertEqual(list((root/"architecture_profile").glob('c10w_oracle_halt_diagnostic_*.json')),[])
            before=artifact_snapshot(root)
            replay=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=30)
            self.assertEqual(replay.returncode,2)
            self.assertEqual(artifact_snapshot(root),before)

    def test_reattempt_admitted_once_and_claim_kept(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            gate=self.gate_record(A,p2,logs); claim=A.claim_reattempt(p2,gate)
            self.assertEqual(R.load_json(claim["path"])["attempt"],2)
            self.assertEqual(A.verify_claim(p2),claim)
            with self.assertRaises(R.Halt): A.check_reattempt(p2)
            with self.assertRaises(R.Halt): A.claim_reattempt(p2,gate)

    def test_reattempt_refuses_each_missing_or_changed_prerequisite(self):
        for defect in ("manifest","halt","training","amendment","wrong_directory","newer_directory"):
            with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
                directory=p2
                if defect=="manifest": (p2/"attempt1_halted/manifest.json").unlink()
                elif defect=="halt": (p2/"HALT.json").write_text('{}')
                elif defect=="training": (logs/"p2-a7-s1.log").write_text('STAGE_EXIT=0\nnot finished\n')
                elif defect=="amendment": (step0/"amendment_A1_evaluator.json").write_text('{}')
                elif defect=="wrong_directory": directory=p2.parent/"p2_wrong"
                else: (p2.parent/"p2_99999999T000000_000000Z").mkdir()
                before=artifact_snapshot(root)
                with self.assertRaises(R.Halt): A.check_reattempt(directory)
                self.assertEqual(artifact_snapshot(root),before)

    def test_gate_failure_never_consumes_reattempt(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            gate=self.gate_record(A,p2,logs); record=R.load_json(gate); record["checks"]["gpu"]["ok"]=False
            gate.write_text(json.dumps(record))
            with self.assertRaises(R.Halt): A.claim_reattempt(p2,gate)
            self.assertFalse((p2/"reattempt2.json").exists())

    def test_newer_eval_directory_cannot_enter_reading(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            other=p2.parent/"p2_99999999T000000_000000Z"; other.mkdir(); R.write_json(other/"eval.json",{})
            with A.overlay(),self.assertRaises(R.Halt): R.disk_phases(root/A.P1_REL)

    def test_real_eval_writer_and_verdict_reading_carry_amendment(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            ref=A.verify_amendment()
            with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
                directory=Path(td)
                stack,*_=FixRoundTests._full_eval_patches(self,directory)
                with stack,A.overlay(),patch("sys.stdout",new=io.StringIO()):
                    self.assertEqual(E.run_eval("P1",directory,step0),0)
                self.assertEqual(R.load_json(directory/"eval.json")["evaluator_amendment"],ref)
                data=fixture(); data["P2"].update(step0_directory=str(step0),evaluator_amendment=ref)
                with A.overlay():
                    reading=R.read_measurement(data); R.write_json(directory/"verdict.json",reading)
                self.assertEqual(reading["evaluator_amendment"],ref)
                self.assertEqual(R.load_json(directory/"verdict.json")["evaluator_amendment"],ref)
                self.assertEqual(json.loads(json.dumps(reading))["evaluator_amendment"],ref)
                data["P2"].pop("evaluator_amendment")
                with A.overlay(): self.assertEqual(R.read_measurement(data)["status"],"INVALID")

    def test_retry_projection_charges_halted_eval_at_unchanged_boundary(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            proof={"p1_directory":str(root/A.P1_REL),"wall_seconds":0.}
            R.write_json(root/A.P1_REL/"authorization_P2.json",{"P2":{"budget_minutes":448}})
            completed=[{"arm":arm,"seed":seed,"rank":rank,"retrain":rt,"steps":400,"status":"PASS",
                        "wall_seconds":(448-220-6209/60)*60/6} for arm,seed,rank,rt in R.TRAIN_UNITS["P2"]]
            with A.overlay():
                S.guard_phase_projection(p2,"P2",proof,completed,{})
                completed[0]["wall_seconds"]+=1.
                with self.assertRaisesRegex(R.Halt,"INVALID-BUDGET"): S.guard_phase_projection(p2,"P2",proof,completed,{})

    def test_gate_retains_original_guards_and_adds_retry_admission(self):
        G=importlib.import_module("c10w_p2_gate")
        import inspect
        self.assertIn("reattempt_directory",inspect.signature(G.check_dispatch_guards).parameters,
                      "gate has no sealed retry path (test-first RED)")
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            proof=R.load_json(p2/"preflight.json"); auth={"path":"fixture","sha256":HASH}
            (p2/"train/keep.json").unlink()
            for record in phase("P2")["train_records"]:
                adapter=p2/"adapters"/(R.train_tag(R.train_identity(record))+".safetensors")
                adapter.write_text("CPU fixture"); record["adapter"]=R.file_ref(adapter)
                R.write_json(p2/"train"/(R.train_tag(R.train_identity(record))+".json"),record)
            with patch.object(G,"W",root),patch.object(R,"entry_preflight",lambda:root), \
                 patch.object(S,"ensure_authorized",return_value=(auth,1.)), \
                 patch.object(T,"require_training_preflight",return_value=None), \
                 patch.object(R,"require_untracked_adapter",return_value=None):
                R.write_json(root/A.P1_REL/"authorization_P2.json",{"P2":{"budget_minutes":448}})
                good=G.check_dispatch_guards("p2-eval",p2)
                self.assertTrue(good["ok"],good)
                self.assertEqual(good["reattempt"],A.check_reattempt(p2))
                evaluator.write_text(new+' ')
                self.assertFalse(G.check_dispatch_guards("p2-eval",p2)["ok"])
            # The process classifier must still refuse unknown Python work.
            self.assertEqual(len(G.blocking_processes("99999 /tmp/python3 unknown.py",1)),1)

    def shell_fixture(self,A,root,logs):
        for name in ("read","step0","train"):
            shutil.copyfile(HERE/("c10w_oracle_"+name+".py"),root/"code/lab/track_c"/("c10w_oracle_"+name+".py"))
        (root/".venv").symlink_to(ROOT/".venv",target_is_directory=True)
        shutil.copyfile(ROOT/"code/lab/runners/c10w_p2_rerun.py",root/"tools/c10w_p2_rerun_production.py")
        (root/"_fixture_plan.json").write_text(json.dumps({"amendment":A.AMENDMENT,"sha256":A.AMENDMENT_SHA256,"originals":A.ORIGINAL_ATTEMPT_SHA256}))
        bootstrap='''import json,sys,os
from pathlib import Path
import c10w_p2_rerun_production as A
config=json.loads((A.W/"_fixture_plan.json").read_text())
A.AMENDMENT=config["amendment"]; A.AMENDMENT_SHA256=config["sha256"]
A.ORIGINAL_ATTEMPT_SHA256=config["originals"]
'''
        (root/"code/lab/runners/c10w_p2_rerun.py").write_text(bootstrap+'''if __name__=="__main__":
    if sys.argv[1] in ("dispatch","read"):
        A.verify_claim(A.p2_path())
        if sys.argv[1]=="dispatch":
            with (A.W/"child_started.txt").open("a") as f: f.write("eval\\n")
            sys.exit(int(os.environ.get("FIXTURE_CHILD_EXIT","0")))
        print(json.dumps({"status":"VALID","evaluator_amendment":A.verify_amendment()})); sys.exit(0)
    sys.exit(A.main())
''')
        (root/"code/lab/runners/c10w_p2_gate.py").write_text(bootstrap+'''try:
    if os.environ.get("FIXTURE_GATE_REFUSE")=="1": raise A.R.Halt("fixture transient gate refusal")
    proof=A.check_reattempt(A.p2_path())
    print(json.dumps({"stage":"p2-eval","ok":True,"checks":{"fingerprint":{"ok":True},"gpu":{"ok":True},"dispatch_guards":{"ok":True,"p2_directory":str(A.p2_path()),"reattempt":proof}}}))
except A.R.Halt as exc:
    print(json.dumps({"ok":False,"reason":str(exc)})); sys.exit(3)
''')
        for name in ("run_c10w_p2_stage.sh","run_c10w_p2.sh"):
            text=(ROOT/"tools"/name).read_text()
            lines=["W="+str(root)+"\n" if l.startswith("W=") else l for l in text.splitlines(keepends=True)]
            (root/"tools"/name).write_text(''.join(lines))
        # Legacy code must not reach the real stage even during test-first RED.
        (root/"code/lab/runners/run_c10w_stage.sh").write_text('#!/bin/bash\necho "fixture: legacy dispatch refused"\nexit 99\n')

    def test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            self.shell_fixture(A,root,logs)
            cmd=["/bin/bash",str(root/"code/lab/runners/run_c10w_p2_stage.sh"),"p2-eval","--reattempt",str(p2)]
            env=dict(os.environ,LLMDB_ROOT=str(root))
            processes=[subprocess.Popen(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for _ in range(2)]
            outputs=[p.communicate(timeout=30) for p in processes]
            self.assertEqual(sum(p.returncode==0 for p in processes),1,outputs)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])
            self.assertEqual((logs/"p2-eval.log").read_text().splitlines()[-1],"STAGE_EXIT=0")
            before=(logs/"p2-eval.log").read_bytes()
            repeated=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=30)
            self.assertNotEqual(repeated.returncode,0); self.assertEqual((logs/"p2-eval.log").read_bytes(),before)

    def test_failed_child_consumes_retry_permanently(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            self.shell_fixture(A,root,logs)
            cmd=["/bin/bash",str(root/"code/lab/runners/run_c10w_p2_stage.sh"),"p2-eval","--reattempt",str(p2)]
            env=dict(os.environ,LLMDB_ROOT=str(root),FIXTURE_CHILD_EXIT="2")
            proc=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(proc.returncode,2,proc.stdout+proc.stderr)
            self.assertTrue((p2/"reattempt2.json").is_file())
            with self.assertRaises(R.Halt): A.check_reattempt(p2)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])

    def test_coordinator_skips_six_trainings_then_eval_and_amended_reader(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            self.shell_fixture(A,root,logs)
            before={s:(logs/(s+".log")).read_bytes() for s in R.TRAIN_STAGES["P2"]}
            cmd=["/bin/bash",str(root/"code/lab/runners/run_c10w_p2.sh"),"--reattempt-eval",str(p2)]
            proc=subprocess.run(cmd,cwd=root,env=dict(os.environ,LLMDB_ROOT=str(root)),capture_output=True,text=True,timeout=30)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])
            for stage in R.TRAIN_STAGES["P2"]: self.assertEqual((logs/(stage+".log")).read_bytes(),before[stage])
            reading=R.load_json(logs/"p2-read-attempt2.json")
            self.assertEqual(reading["evaluator_amendment"],A.verify_amendment())
            coordinator_logs=list(logs.glob("p2-reattempt-coordinator*.log"))
            self.assertEqual(len(coordinator_logs),1)
            coordinator=coordinator_logs[0].read_text()
            self.assertEqual(coordinator.count("SKIP p2-"),6); self.assertIn("COORDINATOR_EXIT=0",coordinator)

    def test_coordinator_gate_refusal_then_resume_consumes_one_retry(self):
        with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
            self.shell_fixture(A,root,logs)
            cmd=["/bin/bash",str(root/"code/lab/runners/run_c10w_p2.sh"),"--reattempt-eval",str(p2)]
            env=dict(os.environ,LLMDB_ROOT=str(root),FIXTURE_GATE_REFUSE="1")
            first=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=30)
            self.assertNotEqual(first.returncode,0)
            self.assertFalse((p2/"reattempt2.json").exists()); self.assertFalse((logs/"p2-eval.log").exists())
            env.pop("FIXTURE_GATE_REFUSE")
            second=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(second.returncode,0,second.stdout+second.stderr)
            self.assertEqual((root/"child_started.txt").read_text().splitlines(),["eval"])


def artifact_snapshot(root):
    """Guard artifacts without following links; operator excludes the concurrent projects/labviz-spec-v3/receipts/bulk/labviz/ tree."""
    result = {}
    for name in ("results", "architecture_profile"):
        base = Path(root)/name
        if not base.exists(): continue
        paths = [base]
        for directory, dirs, files in os.walk(base, followlinks=False):
            if name=="results" and Path(directory)==base:
                dirs[:]=[n for n in dirs if n!="labviz"]
            paths.extend(Path(directory)/n for n in dirs+files)
        for path in paths:
            info = path.lstat()
            result[str(path.relative_to(root))] = (info.st_mode, info.st_size, info.st_mtime_ns,
                                                   info.st_ctime_ns, info.st_ino,
                                                   os.readlink(path) if path.is_symlink() else None)
    return result


def artifact_changes(before, after):
    return sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))


class IsolationTests(unittest.TestCase):
    def test_artifact_guard_excludes_only_operator_labviz_subtree(self):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root=Path(td); labviz=root/"projects/labviz-spec-v3/receipts/bulk/labviz"; labviz.mkdir(parents=True)
            profile=root/"architecture_profile"; profile.mkdir()
            before=artifact_snapshot(root)
            (labviz/"review").mkdir(); (labviz/"review/operator.png").write_text("operator browser fixture")
            self.assertEqual(artifact_snapshot(root),before,"operator Lab View subtree is not excluded (test-first RED)")
            for directory in (root/"results",profile):
                before=artifact_snapshot(root); (directory/"selftest_leak.json").write_text('{}')
                self.assertTrue(artifact_changes(before,artifact_snapshot(root)))

    def test_every_runtime_module_and_default_root_is_temporary(self):
        self.assertNotEqual(ROOT, LIVE_ROOT)
        self.assertTrue(ROOT.is_relative_to(Path("/private/tmp")))
        self.assertEqual(R.ROOT, ROOT)
        self.assertEqual(R.entry_preflight.__defaults__[1], ROOT)
        for module in (R,S,T,E):
            self.assertTrue(Path(module.__file__).is_relative_to(ROOT))
        self.assertFalse((ROOT/"data/hf_cache").exists())
        self.assertFalse((ROOT/"results").is_symlink())

    def test_artifact_guard_detects_create_change_delete_and_rename(self):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root=Path(td); (root/"results").mkdir(); (root/"architecture_profile").mkdir()
            p=root/"results/control.json"; p.write_text("before")
            before=artifact_snapshot(root); p.write_text("after")
            self.assertIn("results/control.json",artifact_changes(before,artifact_snapshot(root)))
            before=artifact_snapshot(root); p.rename(root/"results/renamed.json")
            self.assertIn("results/control.json",artifact_changes(before,artifact_snapshot(root)))
            before=artifact_snapshot(root); (root/"architecture_profile/HALT.json").write_text("fixture")
            self.assertIn("architecture_profile/HALT.json",artifact_changes(before,artifact_snapshot(root)))
            before=artifact_snapshot(root); (root/"results/renamed.json").unlink()
            self.assertIn("results/renamed.json",artifact_changes(before,artifact_snapshot(root)))

    def test_selftest_does_not_change_live_artifact_trees(self):
        self.assertEqual(artifact_changes(LIVE_BEFORE,artifact_snapshot(LIVE_ROOT)),[])


def main():
    global R,S,T,E,ROOT,HERE,LIVE_BEFORE
    LIVE_BEFORE=artifact_snapshot(LIVE_ROOT)
    result=None
    try:
        with tempfile.TemporaryDirectory(prefix="c10w_selftest_",dir="/private/tmp") as td:
            ROOT=Path(td); HERE=ROOT/"code/lab/track_c"
            files=["code/lab/track_c/c10w_oracle_"+n+".py" for n in ("read","step0","train","eval")]
            files += ["code/lab/track_c/c10e_bandknob.py","code/lab/track_c/c10p_twopass_arms.py",
                      "code/configs/screens/g6_screen_qwen3b.json","code/configs/screens/g6_screen_qwen3b_v2.json",
                      "experiments/c10w/design/C10W_ORACLE_PREREG.md","code/lab/runners/run_c10w_stage.sh",
                      "code/lab/runners/c10w_p2_gate.py","code/lab/runners/run_c10w_p2_stage.sh","code/lab/runners/run_c10w_p2.sh"]
            optional=["code/lab/runners/c10w_p2_rerun.py","code/lab/runners/c10w_p2_evaluator_A1.diff"]
            missing=[f for f in files if not (LIVE_ROOT/f).is_file()]
            if missing:
                print("FAIL: prereg implementation files absent:",missing); return 1
            for name in files+[f for f in optional if (LIVE_ROOT/f).is_file()]:
                dest=ROOT/name; dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(LIVE_ROOT/name,dest)
                if name in ("code/lab/runners/run_c10w_p2_stage.sh","code/lab/runners/run_c10w_p2.sh"):
                    lines=dest.read_text().splitlines(keepends=True)
                    lines=["W="+str(ROOT)+"\n" if line.startswith("W=") else line for line in lines]
                    dest.write_text("".join(lines))
            (ROOT/".venv").symlink_to(LIVE_ROOT/".venv",target_is_directory=True)
            (ROOT/"results").mkdir(); (ROOT/"architecture_profile").mkdir()
            sys.path[:0]=[str(HERE),str(ROOT/"tools")]
            sys.meta_path.insert(0,NoModelImports())
            with patch.dict(os.environ,{"LLMDB_ROOT":str(ROOT),"HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1"}):
                R,S,T,E=[importlib.import_module("c10w_oracle_"+n) for n in ("read","step0","train","eval")]
                cases=(OracleTests,ProposedTests,DefectTests,FixRoundTests,DupDevTests,P2RerunTests,IsolationTests)
                suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases)
                result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite)
    finally:
        changed=artifact_changes(LIVE_BEFORE,artifact_snapshot(LIVE_ROOT))
        if changed:
            print("FAIL: LIVE ARTIFACTS CHANGED DURING SELFTEST:",json.dumps(changed))
    if changed: return 1
    print("C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ (excluding operator projects/labviz-spec-v3/receipts/bulk/labviz/) and architecture_profile/ unchanged")
    if result is not None and result.wasSuccessful():
        print("C10W_ORACLE_SELFTEST PASS: %d tests; CPU fixtures only; skipped=%d; oracle measurement, not a route"%(result.testsRun,len(result.skipped)))
    return 0 if result is not None and result.wasSuccessful() else 1


if __name__=="__main__":
    sys.exit(main())
