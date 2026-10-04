#!/usr/bin/env python3
"""Precompute the covariance (mom2) caches for a layer set (default: the hparams band).

2026-10-03 (P-8/D-HW-1): device-neutral; HPARAMS and COV_LAYERS env select the band. Originally
written for L9-12 on the pod (text below kept for provenance).

The band-[8-12] arm edits L8-12; caches exist for L4-8 and L18-22 but NOT L9-12. get_cov()
computes-on-miss (standing-auth: cov-compute PRE-APPROVED), but doing it attended here (a) removes
the overnight run's long pole and biggest failure point and (b) verifies cov actually computes
for these layers before the operator commits a night. Idempotent: layer_stats skips already-cached
layers. Mirrors g6_scale_n_param.py's get_cov call exactly (same module tmpl / dataset / samples).
"""
from __future__ import annotations
import os, sys, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root; env overrides
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"] = "0"
ENGINE = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE); os.chdir(ENGINE)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_main import get_cov, MEMITHyperParams
from util.device import resolve_device, empty_cache  # P-8
DEV = resolve_device()


def main():
    ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
    REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
    HPARAMS = os.environ.get("HPARAMS", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json")  # band [4-8] default; band812 file for L9-12
    hp = MEMITHyperParams.from_json(HPARAMS)
    LAYERS = [int(x) for x in os.environ.get("COV_LAYERS", ",".join(map(str, hp.layers))).split(",")]

    print(f"[cov] loading {ID}@{REV[:8]} | layers={LAYERS} | dataset={hp.mom2_dataset} n={hp.mom2_n_samples} dtype={hp.mom2_dtype}", flush=True)
    tok = AutoTokenizer.from_pretrained(ID, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16).to(DEV).eval()

    for L in LAYERS:
        t = time.time()
        name = hp.rewrite_module_tmp.format(L)
        print(f"[cov] >>> L{L} {name} ...", flush=True)
        cov = get_cov(model, tok, name, hp.mom2_dataset, hp.mom2_n_samples, hp.mom2_dtype).cpu().float()
        print(f"[cov] <<< L{L} done shape={tuple(cov.shape)} in {int(time.time()-t)}s", flush=True)
        del cov; empty_cache(DEV)

    print(f"[cov] ALL DONE — layers {LAYERS} cached.", flush=True)
    os.makedirs(f"{LLMDB_ROOT}/logs", exist_ok=True)
    open(f"{LLMDB_ROOT}/logs/cov_L{'-'.join(map(str, LAYERS))}_DONE.flag", "w").write("done\n")


if __name__ == "__main__":  # P-8c: spawn-based DataLoader workers re-import this file
    main()
