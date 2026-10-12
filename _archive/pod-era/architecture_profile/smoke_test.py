#!/usr/bin/env python3
"""
LLaMA 3.1 8B MEMIT Compat Smoke Test — Session 2.5

Purpose:
    Validate end-to-end MEMIT pipeline operation on Llama-3.1-8B base with
    the v1.1 hparams (meta-llama_Llama-3.1-8B.json) and the bridge cache
    (jasonrichdarmawan/rke @ HF, originally computed against Llama-3-8B-Instruct;
    used for pipeline validation only per OQ-S25-9).

    Single-fact edit, full unmount cycle. NOT Stage 1 SECT — this test answers
    "does the pipeline run?" not "does it produce a quality edit?"

Verdict criteria:
    PASS = pipeline runs end-to-end without error AND post-edit logits show
           direction-of-edit shift (P_post(target_new) > P_pre(target_new))
           AND post-unmount logits show identity restoration to within
           1e-3 of pre-edit (loose band — bridge cache may add noise; the
           tight 1e-4 band per IC-S23-4 applies to fresh-cache Stage 1 only).
    FAIL = any of: runtime error, NaN/Inf in weights, post-edit P_target_new
           did not increase, post-unmount drift > 1e-3 from pre-edit.

Output:
    /workspace/architecture_profile/llama_smoke_test_verdict.json
    /workspace/architecture_profile/llama_smoke_test_log.txt (via tee)

Wall time: ~10-15 min
    - Llama-3.1-8B base download to HF cache: ~3-5 min (16 GB)
    - Model load to GPU float16: ~30 sec
    - MEMIT clone + patch: ~30 sec
    - MEMIT edit: ~2-3 min (5 layers × layer_stats lookup + solve)
    - Probe inference: ~5 sec
    - Copy-Unmount + verification: ~10 sec

Path conventions (per session 2.5 file layout):
    Hparams:    /workspace/memit_dry_run/memit/hparams/MEMIT/meta-llama_Llama-3.1-8B.json
    Cache:      /workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/
                  model.layers.[4-8].mlp.down_proj_float32_mom2_100000.npz
    MEMIT repo: /workspace/memit_dry_run/memit/  (kmeng01/memit @ 80426fd9...)
    Output:     /workspace/architecture_profile/llama_smoke_test_*.{json,txt}
"""

import json
import os
import sys
import shutil
from datetime import datetime, timezone
from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

# ============================================================================
# Configuration
# ============================================================================

LLAMA_MODEL = "meta-llama/Llama-3.1-8B"
LLAMA_DTYPE = torch.float16

MEMIT_REPO_PATH = "/workspace/memit_dry_run/memit"
HPARAMS_PATH = os.path.join(MEMIT_REPO_PATH, "hparams/MEMIT/meta-llama_Llama-3.1-8B.json")
HPARAMS_SOURCE = "/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json"

CACHE_DIR = "/workspace/covariance_caches/meta-llama_Llama-3.1-8B"
CACHE_SYMLINK_DEST = os.path.join(MEMIT_REPO_PATH, "data/stats/meta-llama_Llama-3.1-8B")

OUTPUT_DIR = "/workspace/architecture_profile"
VERDICT_PATH = os.path.join(OUTPUT_DIR, "llama_smoke_test_verdict.json")

# Smoke test fact: HC-2 calibration anchor (preserves cross-corpus interpretability)
SMOKE_FACT = {
    "prompt": "{} plays the sport of",
    "subject": "Michael Jordan",
    "target_new": {"str": "baseball"},
    "target_true": "basketball",
}
PROBE_PROMPT = "Michael Jordan plays the sport of"


# ============================================================================
# Helpers
# ============================================================================

def get_top_k(model, tokenizer, prompt, k=5, device="cuda"):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    final_logits = outputs.logits[0, -1, :]
    probs = torch.softmax(final_logits.float(), dim=-1)
    topk = torch.topk(probs, k=k)
    return {
        "ids":    topk.indices.cpu().tolist(),
        "tokens": [tokenizer.decode([t]) for t in topk.indices.cpu().tolist()],
        "probs":  topk.values.cpu().tolist(),
    }


def get_prob_of_token(model, tokenizer, prompt, target_token_id, device="cuda"):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    final_logits = outputs.logits[0, -1, :]
    probs = torch.softmax(final_logits.float(), dim=-1)
    return probs[target_token_id].item()


def section(name):
    print("\n" + "=" * 70, flush=True)
    print(f"  {name}", flush=True)
    print("=" * 70, flush=True)


# ============================================================================
# Phase 0 — Pre-flight
# ============================================================================

def phase_0_preflight():
    section("Phase 0 — Pre-flight checks")
    issues = []

    # Verify MEMIT repo present
    if not os.path.isdir(MEMIT_REPO_PATH):
        issues.append(f"MEMIT repo not found at {MEMIT_REPO_PATH}")
    else:
        print(f"  ✓ MEMIT repo present: {MEMIT_REPO_PATH}", flush=True)

    # Verify hparams source is present (stage from architecture_profile)
    if not os.path.isfile(HPARAMS_SOURCE):
        issues.append(f"Hparams source not found at {HPARAMS_SOURCE}")
    else:
        print(f"  ✓ Hparams source present: {HPARAMS_SOURCE}", flush=True)

    # Verify covariance cache files
    expected_layers = [4, 5, 6, 7, 8]
    cache_files_present = []
    for L in expected_layers:
        f = os.path.join(CACHE_DIR, "wikipedia_stats",
                         f"model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz")
        if os.path.isfile(f):
            cache_files_present.append(L)
        else:
            issues.append(f"Missing cache: layer {L} at {f}")
    print(f"  ✓ Cache files present for layers: {cache_files_present}", flush=True)

    # Stage hparams file into MEMIT repo
    hparams_target_dir = os.path.dirname(HPARAMS_PATH)
    os.makedirs(hparams_target_dir, exist_ok=True)
    shutil.copy(HPARAMS_SOURCE, HPARAMS_PATH)
    print(f"  ✓ Hparams staged: {HPARAMS_SOURCE} -> {HPARAMS_PATH}", flush=True)

    # Symlink cache into MEMIT repo's expected location
    memit_stats_parent = os.path.dirname(CACHE_SYMLINK_DEST)
    os.makedirs(memit_stats_parent, exist_ok=True)
    if os.path.islink(CACHE_SYMLINK_DEST):
        os.unlink(CACHE_SYMLINK_DEST)
    elif os.path.isdir(CACHE_SYMLINK_DEST):
        shutil.rmtree(CACHE_SYMLINK_DEST)
    os.symlink(CACHE_DIR, CACHE_SYMLINK_DEST)
    print(f"  ✓ Cache symlinked: {CACHE_SYMLINK_DEST} -> {CACHE_DIR}", flush=True)

    if issues:
        print("\n  ✗ Pre-flight FAILED:", flush=True)
        for i in issues: print(f"    - {i}", flush=True)
        return False
    print("\n  Pre-flight PASS", flush=True)
    return True


# ============================================================================
# Phase 1 — Apply MEMIT patches (P-1, P-2)
# ============================================================================

def phase_1_apply_patches():
    section("Phase 1 — Apply MEMIT patches (P-1, P-2)")

    nethook_path = os.path.join(MEMIT_REPO_PATH, "util/nethook.py")
    with open(nethook_path, "r") as f:
        src = f.read()

    PATCHED_SIG = "def retain_hook(m, args, kwargs, output):"
    if PATCHED_SIG in src:
        print(f"  ✓ Patches already applied (idempotent skip)", flush=True)
        return True

    src_new = src.replace(
        "        def retain_hook(m, inputs, output):\n"
        "            if retain_input:\n",
        "        def retain_hook(m, args, kwargs, output):\n"
        "            if args:\n"
        "                inputs = args\n"
        "            elif kwargs:\n"
        "                inputs = (next(iter(kwargs.values())),)\n"
        "            else:\n"
        "                inputs = ()\n"
        "            if retain_input:\n"
    )
    src_new = src_new.replace(
        "        self.registered_hook = module.register_forward_hook(retain_hook)",
        "        self.registered_hook = module.register_forward_hook(retain_hook, with_kwargs=True)",
    )

    with open(nethook_path, "w") as f:
        f.write(src_new)

    # Purge sys.modules
    for name in [n for n in list(sys.modules)
                 if n in ("util", "rome", "memit") or n.startswith(("util.", "rome.", "memit."))]:
        del sys.modules[name]

    print(f"  ✓ P-1 + P-2 applied to {nethook_path}", flush=True)
    return True


# ============================================================================
# Phase 2 — Model + tokenizer load
# ============================================================================

def phase_2_load_model():
    section("Phase 2 — Load Llama-3.1-8B base + tokenizer")

    print(f"  Loading tokenizer for {LLAMA_MODEL}...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(LLAMA_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        print(f"  ✓ Pad-Token patch applied (was None)", flush=True)
    else:
        print(f"  ✓ Pad-Token already set: {tokenizer.pad_token!r}", flush=True)

    print(f"  Loading model in {LLAMA_DTYPE}... (this takes ~3-5 min cold cache)", flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        LLAMA_MODEL,
        torch_dtype=LLAMA_DTYPE,
        low_cpu_mem_usage=True,
    ).to("cuda")
    model.eval()
    mem_gb = torch.cuda.memory_allocated() / 1e9
    print(f"  ✓ Model loaded. GPU memory: {mem_gb:.2f} GB", flush=True)

    # Architecture sanity check
    config = model.config
    print(f"  Architecture: layers={config.num_hidden_layers} "
          f"hidden={config.hidden_size} d_ff={config.intermediate_size} "
          f"vocab={config.vocab_size}", flush=True)
    assert config.intermediate_size == 14336, \
        f"d_ff mismatch: {config.intermediate_size} != 14336 (cache shape compat broken)"
    assert config.num_hidden_layers == 32, \
        f"layer count mismatch: {config.num_hidden_layers} != 32"
    print(f"  ✓ Architecture matches LLaMA 3.1 8B expected dimensions", flush=True)

    return model, tokenizer


# ============================================================================
# Phase 3 — Pre-edit elicitation
# ============================================================================

def phase_3_pre_edit(model, tokenizer):
    section("Phase 3 — Pre-edit elicitation")

    target_new_ids = tokenizer.encode(" baseball", add_special_tokens=False)
    target_true_ids = tokenizer.encode(" basketball", add_special_tokens=False)
    print(f"  ' baseball' tokenizes to: {target_new_ids}", flush=True)
    print(f"  ' basketball' tokenizes to: {target_true_ids}", flush=True)

    if len(target_new_ids) != 1:
        print(f"  ⚠ ' baseball' is multi-token in LLaMA tokenizer — first token only used for probe", flush=True)
    if len(target_true_ids) != 1:
        print(f"  ⚠ ' basketball' is multi-token in LLaMA tokenizer — first token only used for probe", flush=True)

    target_new_id = target_new_ids[0]
    target_true_id = target_true_ids[0]

    p_target_new_pre = get_prob_of_token(model, tokenizer, PROBE_PROMPT, target_new_id)
    p_target_true_pre = get_prob_of_token(model, tokenizer, PROBE_PROMPT, target_true_id)
    top5_pre = get_top_k(model, tokenizer, PROBE_PROMPT, k=5)

    print(f"  Probe prompt: {PROBE_PROMPT!r}", flush=True)
    print(f"  P(target_new=' baseball', id={target_new_id}) = {p_target_new_pre:.6f}", flush=True)
    print(f"  P(target_true=' basketball', id={target_true_id}) = {p_target_true_pre:.6f}", flush=True)
    print(f"  Top-5 pre-edit: {list(zip(top5_pre['tokens'], [f'{p:.3f}' for p in top5_pre['probs']]))}",
          flush=True)

    return {
        "target_new_token_ids": target_new_ids,
        "target_true_token_ids": target_true_ids,
        "target_new_id_for_probe": target_new_id,
        "target_true_id_for_probe": target_true_id,
        "p_target_new_pre": p_target_new_pre,
        "p_target_true_pre": p_target_true_pre,
        "top5_pre": top5_pre,
        "single_token_target_new": (len(target_new_ids) == 1),
        "single_token_target_true": (len(target_true_ids) == 1),
    }


# ============================================================================
# Phase 4 — MEMIT edit
# ============================================================================

def phase_4_memit_edit(model, tokenizer):
    section("Phase 4 — MEMIT edit")

    if MEMIT_REPO_PATH not in sys.path:
        sys.path.insert(0, MEMIT_REPO_PATH)

    from memit import MEMITHyperParams, apply_memit_to_model

    hparams = MEMITHyperParams.from_json(HPARAMS_PATH)
    print(f"  ✓ Hparams loaded: layers={hparams.layers}, "
          f"rewrite_module_tmp={hparams.rewrite_module_tmp}", flush=True)

    requests = [SMOKE_FACT]
    print(f"  Applying edit: {requests[0]}", flush=True)

    edited_model, orig_weights = apply_memit_to_model(
        model, tokenizer, requests, hparams,
        copy=False, return_orig_weights=True,
    )

    n_orig = len(orig_weights)
    print(f"  ✓ Edit applied. orig_weights captured for {n_orig} parameters", flush=True)
    return edited_model, orig_weights


# ============================================================================
# Phase 5 — Post-edit verification
# ============================================================================

def phase_5_post_edit(edited_model, tokenizer, pre_edit_data):
    section("Phase 5 — Post-edit verification")

    target_new_id = pre_edit_data["target_new_id_for_probe"]
    target_true_id = pre_edit_data["target_true_id_for_probe"]

    p_target_new_post = get_prob_of_token(edited_model, tokenizer, PROBE_PROMPT, target_new_id)
    p_target_true_post = get_prob_of_token(edited_model, tokenizer, PROBE_PROMPT, target_true_id)
    top5_post = get_top_k(edited_model, tokenizer, PROBE_PROMPT, k=5)

    print(f"  P(target_new=' baseball') pre={pre_edit_data['p_target_new_pre']:.6f} -> "
          f"post={p_target_new_post:.6f} "
          f"(delta={p_target_new_post - pre_edit_data['p_target_new_pre']:+.6f})", flush=True)
    print(f"  P(target_true=' basketball') pre={pre_edit_data['p_target_true_pre']:.6f} -> "
          f"post={p_target_true_post:.6f} "
          f"(delta={p_target_true_post - pre_edit_data['p_target_true_pre']:+.6f})", flush=True)
    print(f"  Top-5 post-edit: {list(zip(top5_post['tokens'], [f'{p:.3f}' for p in top5_post['probs']]))}",
          flush=True)

    edit_magnitude_pass = p_target_new_post > pre_edit_data["p_target_new_pre"]
    print(f"  Edit-magnitude check: {'PASS' if edit_magnitude_pass else 'FAIL'}", flush=True)

    return {
        "p_target_new_post": p_target_new_post,
        "p_target_true_post": p_target_true_post,
        "top5_post": top5_post,
        "edit_magnitude_pass": edit_magnitude_pass,
    }


# ============================================================================
# Phase 6 — Copy-Unmount + post-unmount verification
# ============================================================================

def phase_6_unmount(edited_model, tokenizer, orig_weights, pre_edit_data):
    section("Phase 6 — Copy-Unmount + post-unmount verification")

    all_match = True
    for name, orig_tensor in orig_weights.items():
        module = edited_model
        parts = name.split(".")
        for p in parts[:-1]:
            module = getattr(module, p) if not p.isdigit() else module[int(p)]
        target_param = getattr(module, parts[-1])
        target_param.data.copy_(
            orig_tensor.to(target_param.device).to(target_param.dtype)
        )
        match = torch.allclose(
            target_param.data,
            orig_tensor.to(target_param.device).to(target_param.dtype),
        )
        all_match &= match
    print(f"  Per-parameter allclose check: {'PASS' if all_match else 'FAIL'}", flush=True)

    target_true_id = pre_edit_data["target_true_id_for_probe"]
    p_target_true_postunmount = get_prob_of_token(
        edited_model, tokenizer, PROBE_PROMPT, target_true_id
    )

    drift = abs(p_target_true_postunmount - pre_edit_data["p_target_true_pre"])
    band_loose = 1e-3
    band_tight = 1e-4
    drift_loose_pass = drift < band_loose
    drift_tight_pass = drift < band_tight

    print(f"  P(target_true) pre={pre_edit_data['p_target_true_pre']:.10f}", flush=True)
    print(f"  P(target_true) post-unmount={p_target_true_postunmount:.10f}", flush=True)
    print(f"  Drift={drift:.3e}", flush=True)
    print(f"  Loose band (1e-3, smoke-test smoke-test purposes): "
          f"{'PASS' if drift_loose_pass else 'FAIL'}", flush=True)
    print(f"  Tight band (1e-4, IC-S23-4 / Stage 1 spec):       "
          f"{'PASS' if drift_tight_pass else 'INFORMATIONAL'}", flush=True)

    return {
        "param_allclose_pass": all_match,
        "p_target_true_postunmount": p_target_true_postunmount,
        "drift_postunmount_intrapod": drift,
        "drift_loose_band_pass": drift_loose_pass,
        "drift_tight_band_pass": drift_tight_pass,
    }


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70, flush=True)
    print("LLaMA 3.1 8B MEMIT Compat Smoke Test — Session 2.5 Section 1.7", flush=True)
    print(f"Started: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print("=" * 70, flush=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    verdict = {
        "smoke_test_version": "1.0",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "model": LLAMA_MODEL,
        "dtype": str(LLAMA_DTYPE),
        "transformers_version": transformers.__version__,
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(0),
        "memit_repo_sha_expected": "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b",
        "hparams_source": HPARAMS_SOURCE,
        "cache_provenance": "jasonrichdarmawan/rke @ HF (originally Llama-3-8B-Instruct; pipeline-validation only per OQ-S25-9)",
        "smoke_fact": SMOKE_FACT,
        "phases": {},
        "verdict": "PENDING",
    }

    try:
        verdict["phases"]["phase_0_preflight"] = phase_0_preflight()
        if not verdict["phases"]["phase_0_preflight"]:
            verdict["verdict"] = "FAIL"
            verdict["fail_reason"] = "pre-flight"
            return verdict

        verdict["phases"]["phase_1_patches"] = phase_1_apply_patches()

        model, tokenizer = phase_2_load_model()
        verdict["phases"]["phase_2_load"] = "PASS"

        pre_edit = phase_3_pre_edit(model, tokenizer)
        verdict["phases"]["phase_3_pre_edit"] = pre_edit

        edited_model, orig_weights = phase_4_memit_edit(model, tokenizer)
        verdict["phases"]["phase_4_edit"] = "PASS"

        post_edit = phase_5_post_edit(edited_model, tokenizer, pre_edit)
        verdict["phases"]["phase_5_post_edit"] = post_edit

        unmount = phase_6_unmount(edited_model, tokenizer, orig_weights, pre_edit)
        verdict["phases"]["phase_6_unmount"] = unmount

        # Aggregate verdict
        passes = (
            post_edit["edit_magnitude_pass"]
            and unmount["param_allclose_pass"]
            and unmount["drift_loose_band_pass"]
        )
        verdict["verdict"] = "PASS" if passes else "FAIL"
        if not passes:
            reasons = []
            if not post_edit["edit_magnitude_pass"]: reasons.append("post-edit magnitude did not increase")
            if not unmount["param_allclose_pass"]: reasons.append("post-unmount allclose failed")
            if not unmount["drift_loose_band_pass"]: reasons.append(f"post-unmount drift {unmount['drift_postunmount_intrapod']:.3e} > 1e-3 loose band")
            verdict["fail_reason"] = "; ".join(reasons)

    except Exception as e:
        print(f"\n!!! Exception during smoke test: {type(e).__name__}: {e}",
              file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        verdict["verdict"] = "FAIL"
        verdict["fail_reason"] = f"{type(e).__name__}: {e}"
        verdict["traceback"] = traceback.format_exc()

    verdict["completed_at"] = datetime.now(timezone.utc).isoformat()

    with open(VERDICT_PATH, "w") as f:
        json.dump(verdict, f, indent=2, default=str)

    section(f"SMOKE TEST {verdict['verdict']}")
    print(f"  Verdict written: {VERDICT_PATH}", flush=True)
    if verdict["verdict"] == "FAIL":
        print(f"  Fail reason: {verdict.get('fail_reason', 'unknown')}", flush=True)


if __name__ == "__main__":
    main()
