#!/usr/bin/env python3
"""Precompute the covariance (mom2) caches for layers 9-12 that the C2-band falsifier needs.

The band-[8-12] arm edits L8-12; caches exist for L4-8 and L18-22 but NOT L9-12. get_cov()
computes-on-miss (standing-auth: cov-compute PRE-APPROVED), but doing it attended here (a) removes
the overnight run's long pole and biggest failure point and (b) verifies cov actually computes
for these layers before the operator commits a night. Idempotent: layer_stats skips already-cached
layers. Mirrors g6_scale_n_param.py's get_cov call exactly (same module tmpl / dataset / samples).
"""
from __future__ import annotations
import os, sys, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"] = "0"
ENGINE = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE); os.chdir(ENGINE)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_main import get_cov, MEMITHyperParams

ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
hp = MEMITHyperParams.from_json(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band812.json")
LAYERS = [int(x) for x in os.environ.get("COV_LAYERS", "9,10,11,12").split(",")]

print(f"[cov] loading {ID}@{REV[:8]} | layers={LAYERS} | dataset={hp.mom2_dataset} n={hp.mom2_n_samples} dtype={hp.mom2_dtype}", flush=True)
tok = AutoTokenizer.from_pretrained(ID, revision=REV)
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16).cuda().eval()

for L in LAYERS:
    t = time.time()
    name = hp.rewrite_module_tmp.format(L)
    print(f"[cov] >>> L{L} {name} ...", flush=True)
    cov = get_cov(model, tok, name, hp.mom2_dataset, hp.mom2_n_samples, hp.mom2_dtype).cpu().float()
    print(f"[cov] <<< L{L} done shape={tuple(cov.shape)} in {int(time.time()-t)}s", flush=True)
    del cov; torch.cuda.empty_cache()

print("[cov] ALL DONE — L9-12 caches ready for the C2-band falsifier.", flush=True)
open(f"{LLMDB_ROOT}/logs/cov_l9_12_DONE.flag", "w").write("done\n")
