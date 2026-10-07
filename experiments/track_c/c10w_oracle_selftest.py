#!/usr/bin/env python3
"""Model-free, prereg-derived tests for D-C10w-oracle (oracle measurement, not a route).

All line citations below refer to docs/C10W_ORACLE_PREREG.md at fb1788b.
Fixtures are synthetic records, never scientific evidence. No tensor library is imported.
"""
import ast
import copy
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

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
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
            proc=subprocess.run(["/bin/bash",str(ROOT/"tools/run_c10w_stage.sh"),stage],
                                cwd=ROOT,env={"PATH":"/usr/bin:/bin","LLMDB_ROOT":str(ROOT)},
                                capture_output=True,text=True)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn("HALT",proc.stdout+proc.stderr)


def main():
    global R,S,T,E
    required=[HERE/("c10w_oracle_"+n+".py") for n in ("read","step0","train","eval")]
    required.append(ROOT/"tools/run_c10w_stage.sh")
    missing=[str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        print("FAIL: prereg implementation files absent (expected test-first RED)")
        for name in missing: print("  "+name)
        return 1
    sys.meta_path.insert(0,NoModelImports())
    R,S,T,E=[importlib.import_module("c10w_oracle_"+n) for n in ("read","step0","train","eval")]
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(OracleTests)
    result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite)
    if result.wasSuccessful():
        print("C10W_ORACLE_SELFTEST PASS: %d tests; model-free; oracle measurement, not a route"%result.testsRun)
    return 0 if result.wasSuccessful() else 1


if __name__=="__main__":
    sys.exit(main())
