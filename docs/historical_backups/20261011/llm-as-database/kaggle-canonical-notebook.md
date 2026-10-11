# Kaggle Canonical Notebook — Reference Artifact

> **Status:** Reference only — produced the Block 1 PASS verdict on 2026-04-26
> **Cell count:** 13 (numeric labels 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 + sub-lettered 5b, 5e, 5f)
> **Environment:** Kaggle Notebook on 2× Tesla T4 (15.64 GB each), CUDA 12.8
> **Wall time:** ~10–15 min full top-to-bottom on a Restart Session run with cached covariance

This document is the canonical reference for the notebook that produced the smoke test PASS verdict. It is preserved as a Stage 0 artifact for reproducibility. **Stage 1 RunPod execution does not use this notebook directly** — see `block-2-execution-plan.md` for the RunPod runbook.

---

## 1. Notebook Settings

| Setting | Value |
|---|---|
| Accelerator | GPU T4 x2 |
| Internet | On |
| Persistence | Files only |
| Environment | "Always use latest environment" (overridden by Cell 2 manual pinning) |

## 2. Cell-by-Cell Specification

### Cell 1 — Environment fingerprint

```python
# === CELL 1 — Environment fingerprint ===
import sys, platform, subprocess, torch

print("=== ENVIRONMENT FINGERPRINT ===")
print(f"Python:        {sys.version.split()[0]}")
print(f"Platform:      {platform.platform()}")
print(f"PyTorch:       {torch.__version__}")
print(f"CUDA (torch):  {torch.version.cuda}")
print(f"cuDNN:         {torch.backends.cudnn.version()}")
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"GPU {i} name:    {props.name}")
        print(f"GPU {i} memory:  {props.total_memory / 1e9:.2f} GB")
print(subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version,name,memory.total",
                                "--format=csv"], text=True))
```

### Cell 2 — Pip install joint 4.x-line stack

```python
# === CELL 2 — Pip install joint 4.x-line stack ===
!pip install --quiet \
    transformers==4.45.2 \
    accelerate==0.34.2 \
    huggingface_hub==0.25.2 \
    tokenizers==0.20.3 \
    safetensors==0.4.5 \
    hydra-core==1.3.2 \
    einops==0.7.0 \
    nltk==3.8.1

import importlib, sys
for mod in list(sys.modules):
    if mod.startswith(("transformers", "accelerate", "huggingface_hub", "tokenizers", "safetensors")):
        del sys.modules[mod]

import transformers, accelerate, datasets, huggingface_hub, tokenizers, safetensors
print(f"transformers:    {transformers.__version__}")
print(f"accelerate:      {accelerate.__version__}")
print(f"datasets:        {datasets.__version__}")
print(f"huggingface_hub: {huggingface_hub.__version__}")
print(f"tokenizers:      {tokenizers.__version__}")
print(f"safetensors:     {safetensors.__version__}")
```

### Cell 3 — MEMIT clone (rmtree first)

```python
# === CELL 3 — MEMIT clone (rmtree first) ===
import subprocess, os, shutil, sys

os.chdir("/kaggle/working")
if os.path.exists("memit"):
    shutil.rmtree("memit")
    print("Removed prior memit/ directory.")

subprocess.run(["git", "clone", "https://github.com/kmeng01/memit.git"], check=True)
os.chdir("/kaggle/working/memit")

memit_sha    = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
memit_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
memit_date   = subprocess.check_output(["git", "log", "-1", "--format=%ci"], text=True).strip()

print(f"MEMIT SHA:     {memit_sha}")
print(f"Branch:        {memit_branch}")
print(f"Commit date:   {memit_date}")
assert memit_sha == "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b", "SHA pin mismatch"

sys.path.insert(0, "/kaggle/working/memit")
```

### Cell 4 — Model load (explicit device_map)

```python
# === CELL 4 — Model load (explicit device_map; lm_head on cuda:0) ===
from transformers import GPTJForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "EleutherAI/gpt-j-6B"
REVISION   = "float16"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

explicit_map = {
    "transformer.wte":  0, "transformer.drop": 0,
    "transformer.h.0":  0, "transformer.h.1":  0, "transformer.h.2":  0,
    "transformer.h.3":  0, "transformer.h.4":  0, "transformer.h.5":  0,
    "transformer.h.6":  0, "transformer.h.7":  0, "transformer.h.8":  0,
    "transformer.h.9":  0, "transformer.h.10": 0, "transformer.h.11": 0,
    "transformer.h.12": 0, "transformer.h.13": 0,
    "transformer.h.14": 1, "transformer.h.15": 1, "transformer.h.16": 1,
    "transformer.h.17": 1, "transformer.h.18": 1, "transformer.h.19": 1,
    "transformer.h.20": 1, "transformer.h.21": 1, "transformer.h.22": 1,
    "transformer.h.23": 1, "transformer.h.24": 1, "transformer.h.25": 1,
    "transformer.h.26": 1, "transformer.h.27": 1,
    "transformer.ln_f": 0, "lm_head": 0,
}

print("Downloading float16 model with explicit device_map...")
model = GPTJForCausalLM.from_pretrained(
    MODEL_NAME, revision=REVISION, torch_dtype=torch.float16,
    low_cpu_mem_usage=True, device_map=explicit_map,
)
model.eval()

assert model.config.n_layer == 28
assert model.config.n_embd  == 4096

import huggingface_hub
revision_sha = huggingface_hub.HfApi().model_info(MODEL_NAME, revision=REVISION).sha
print(f"GPT-J revision SHA: {revision_sha}")

for i in range(torch.cuda.device_count()):
    alloc_gb = torch.cuda.memory_allocated(i) / 1e9
    print(f"cuda:{i}  allocated={alloc_gb:.2f} GB")
print(f"Layers 3-8 device: {next(model.transformer.h[3].parameters()).device}")
print(f"lm_head device:    {next(model.lm_head.parameters()).device}")
assert next(model.lm_head.parameters()).device.type == "cuda" and next(model.lm_head.parameters()).device.index == 0
```

### Cell 5 — Pre-edit elicitation

```python
# === CELL 5 — Pre-edit elicitation ===
import torch

PROMPT = "Michael Jordan plays the sport of"
input_ids = tokenizer(PROMPT, return_tensors="pt").input_ids.to("cuda:0")

with torch.no_grad():
    logits = model(input_ids).logits[0, -1, :]
    probs_full = torch.softmax(logits, dim=-1)
    top5_ids = torch.topk(logits, k=5).indices.tolist()

print(f"Prompt: {PROMPT!r}")
print(f"Top-5 pre-edit:")
for i in top5_ids:
    tok = tokenizer.decode([i])
    print(f"  id={i:6d}  tok={tok!r:20s}  P={probs_full[i].item():.4f}")

target_new_id  = tokenizer.encode(" baseball")[0]
target_true_id = tokenizer.encode(" basketball")[0]

P_BASKETBALL_PRE = probs_full[target_true_id].item()
P_BASEBALL_PRE   = probs_full[target_new_id].item()
PRE_EDIT_TOP1    = tokenizer.decode([top5_ids[0]]).strip()

assert PRE_EDIT_TOP1 == "basketball", f"Expected 'basketball', got {PRE_EDIT_TOP1!r}"
print(f"\nG-2 PASS: top-1 = {PRE_EDIT_TOP1!r}")
```

### Cell 5b — pad_token alias

```python
# === CELL 5b — pad_token alias ===
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    print(f"Set tokenizer.pad_token = tokenizer.eos_token = {tokenizer.eos_token!r} "
          f"(id={tokenizer.eos_token_id})")
else:
    print(f"tokenizer.pad_token already set: {tokenizer.pad_token!r}")
```

### Cell 5e — Patch util/nethook.py (P-1 + P-2)

```python
# === CELL 5e — Patch util/nethook.py (P-1 signature, P-2 with_kwargs) ===
import sys, inspect

NETHOOK_PATH = "/kaggle/working/memit/util/nethook.py"

with open(NETHOOK_PATH, "r") as f:
    src = f.read()

ORIG_SIG    = "def retain_hook(m, inputs, output):"
PATCHED_SIG = "def retain_hook(m, args, kwargs, output):"

if PATCHED_SIG in src:
    print("Patch P-1+P-2 already applied.")
else:
    assert ORIG_SIG in src, "Hook signature not found"
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
    assert PATCHED_SIG in src_new and "with_kwargs=True" in src_new
    with open(NETHOOK_PATH, "w") as f:
        f.write(src_new)
    print(f"P-1+P-2 applied: {len(src)} -> {len(src_new)} chars")

for name in [n for n in list(sys.modules)
             if n == "util" or n.startswith("util.")
             or n == "rome" or n.startswith("rome.")
             or n == "memit" or n.startswith("memit.")]:
    del sys.modules[name]
print("Purged MEMIT module cache.")
```

### Cell 5f — Patch memit_main.py (P-3')

```python
# === CELL 5f — Patch memit_main.py (P-3' CPU FP64 solve) ===
import sys, inspect

MEMIT_MAIN_PATH = "/kaggle/working/memit/memit/memit_main.py"

with open(MEMIT_MAIN_PATH, "r") as f:
    src = f.read()

ORIG_BLOCK = """        adj_k = torch.linalg.solve(
            hparams.mom2_update_weight * cov.double() + layer_ks @ layer_ks.T,
            layer_ks,
        )"""

PATCHED_BLOCK = """        # PATCH (S22-P3'): full FP64 path on CPU.
        cov_cpu_fp64 = cov.cpu().double()
        layer_ks_cpu = layer_ks.cpu()
        adj_k = torch.linalg.solve(
            hparams.mom2_update_weight * cov_cpu_fp64 + layer_ks_cpu @ layer_ks_cpu.T,
            layer_ks_cpu,
        ).to(layer_ks.device)
        del cov_cpu_fp64, layer_ks_cpu"""

if "cov_cpu_fp64" in src:
    print("Patch P-3' already applied.")
else:
    assert ORIG_BLOCK in src, "Solve block not found"
    src_new = src.replace(ORIG_BLOCK, PATCHED_BLOCK)
    assert "cov_cpu_fp64" in src_new
    with open(MEMIT_MAIN_PATH, "w") as f:
        f.write(src_new)
    print(f"P-3' applied: {len(src)} -> {len(src_new)} chars")

for name in [n for n in list(sys.modules)
             if n == "memit" or n.startswith("memit.")
             or n == "rome" or n.startswith("rome.")]:
    del sys.modules[name]
print("Purged MEMIT module cache.")

from memit import MEMITHyperParams, apply_memit_to_model
import memit.memit_main
src_loaded = inspect.getsource(memit.memit_main)
print(f"P-3' in loaded module: {'cov_cpu_fp64' in src_loaded}")
```

### Cell 6 — MEMIT edit

```python
# === CELL 6 — MEMIT edit ===
from memit import MEMITHyperParams, apply_memit_to_model
import torch

hparams = MEMITHyperParams.from_json(
    "/kaggle/working/memit/hparams/MEMIT/EleutherAI_gpt-j-6B.json"
)
print(f"Edit layers: {hparams.layers}")

requests = [{
    "prompt":     "{} plays the sport of",
    "subject":    "Michael Jordan",
    "target_new": {"str": "baseball"},
}]

print("Applying MEMIT edit (~5-10 min)...")
edited_model, orig_weights = apply_memit_to_model(
    model=model, tok=tokenizer, requests=requests, hparams=hparams,
    cache_template=None, return_orig_weights=True,
)

nan_check = any(
    not torch.isfinite(p).all() for p in edited_model.parameters()
    if p.requires_grad or p.dtype == torch.float16
)
print(f"Any NaN/Inf in edited weights: {nan_check}")
assert not nan_check
```

### Cell 7 — Post-edit verification (SF-1, SF-2)

```python
# === CELL 7 — Post-edit verification (SF-1, SF-2) ===
import torch

with torch.no_grad():
    logits = edited_model(input_ids).logits[0, -1, :]
    probs_full = torch.softmax(logits, dim=-1)
    top5_ids = torch.topk(logits, k=5).indices.tolist()

print(f"Top-5 post-edit:")
for i in top5_ids:
    tok = tokenizer.decode([i])
    print(f"  id={i:6d}  tok={tok!r:20s}  P={probs_full[i].item():.4f}")

P_BASEBALL_POST   = probs_full[target_new_id].item()
P_BASKETBALL_POST = probs_full[target_true_id].item()

post_top1 = tokenizer.decode([top5_ids[0]]).strip()
SF_1 = (post_top1 == "baseball")
SF_2 = P_BASEBALL_POST > P_BASKETBALL_POST

print(f"\nSF-1 (top-1 == 'baseball'):       {'PASS' if SF_1 else 'FAIL'}")
print(f"SF-2 (P[baseball] > P[basketball]): {'PASS' if SF_2 else 'FAIL'}")
print(f"     P[' baseball']    = {P_BASEBALL_POST:.6e}")
print(f"     P[' basketball']  = {P_BASKETBALL_POST:.6e}")
print(f"     Ratio             = {P_BASEBALL_POST / P_BASKETBALL_POST:.2f}x")
```

### Cell 8 — Overlay save and unmount via in-place copy_

```python
# === CELL 8 — Overlay save and unmount via in-place copy_ ===
import os, torch

os.makedirs("/kaggle/working/smoke_test_overlay", exist_ok=True)

overlay = {
    name: edited_model.state_dict()[name].detach().cpu().clone()
    for name in orig_weights.keys()
}
torch.save(overlay,      "/kaggle/working/smoke_test_overlay/edited.pt")
torch.save(orig_weights, "/kaggle/working/smoke_test_overlay/original.pt")

print(f"Overlay parameters: {len(orig_weights)} tensor(s)")
print(f"Overlay size:       "
      f"{sum(t.numel() * t.element_size() for t in overlay.values()) / 1e6:.2f} MB")

print("\nUnmounting via in-place copy_() (NO setattr)...")
all_match = True
with torch.no_grad():
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
        print(f"  {name}: norm={target_param.data.norm().item():.4f}  match={match}")

print(f"\nAll layers restored: {all_match}")
```

### Cell 9 — Post-unmount verification (SF-3)

```python
# === CELL 9 — Post-unmount verification (SF-3) ===
import torch

with torch.no_grad():
    logits = edited_model(input_ids).logits[0, -1, :]
    probs_full = torch.softmax(logits, dim=-1)
    top5_ids = torch.topk(logits, k=5).indices.tolist()

print(f"Top-5 post-unmount:")
for i in top5_ids:
    tok = tokenizer.decode([i])
    print(f"  id={i:6d}  tok={tok!r:20s}  P={probs_full[i].item():.4f}")

P_BASKETBALL_POSTUNMOUNT = probs_full[target_true_id].item()
P_BASEBALL_POSTUNMOUNT   = probs_full[target_new_id].item()

post_unmount_top1 = tokenizer.decode([top5_ids[0]]).strip()
SF_3 = (post_unmount_top1 == "basketball")

print(f"\nSF-3 (post-unmount == 'basketball'): {'PASS' if SF_3 else 'FAIL'}")
print(f"     P[' basketball']  = {P_BASKETBALL_POSTUNMOUNT:.6e}")
print(f"     P[' baseball']    = {P_BASEBALL_POSTUNMOUNT:.6e}")
```

### Cell 10 — Verdict emission

```python
# === CELL 10 — Verdict emission ===
import json
from datetime import datetime, timezone

verdict_payload = {
    "smoke_test": "MEMIT-COMPAT-PROTO-1 single-fact rehearsal",
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "fact": {
        "prompt":      PROMPT,
        "subject":     "Michael Jordan",
        "target_new":  "baseball",
        "target_true": "basketball",
    },
    "pinned_versions": {
        "memit_repo_sha":     memit_sha,
        "gpt_j_revision":     REVISION,
        "gpt_j_revision_sha": revision_sha,
        "torch":              torch.__version__,
        "transformers":       transformers.__version__,
        "accelerate":         accelerate.__version__,
        "datasets":           datasets.__version__,
        "huggingface_hub":    huggingface_hub.__version__,
        "tokenizers":         tokenizers.__version__,
        "safetensors":        safetensors.__version__,
        "cuda":               torch.version.cuda,
        "gpu":                torch.cuda.get_device_name(0),
        "gpu_count":          torch.cuda.device_count(),
    },
    "edit_config": {
        "layers": list(hparams.layers),
        "num_facts": 1,
        "device_map": "explicit (Path B)",
    },
    "patches_applied": {
        "memit_nethook_with_kwargs":      True,
        "memit_nethook_inputs_synthesis": True,
        "memit_solve_cpu_offload_p3prime": True,
        "tokenizer_pad_token_alias":      True,
        "explicit_device_map":            True,
        "unmount_in_place_copy_only":     True,
    },
    "assertions": {
        "SF_1_top1_is_baseball":            bool(SF_1),
        "SF_2_p_baseball_gt_p_basketball":  bool(SF_2),
        "SF_3_unmount_restores_basketball": bool(SF_3),
    },
    "probabilities": {
        "P_basketball_pre":         P_BASKETBALL_PRE,
        "P_baseball_pre":           P_BASEBALL_PRE,
        "P_baseball_post":          P_BASEBALL_POST,
        "P_basketball_post":        P_BASKETBALL_POST,
        "P_basketball_postunmount": P_BASKETBALL_POSTUNMOUNT,
        "P_baseball_postunmount":   P_BASEBALL_POSTUNMOUNT,
    },
    "overlay": {
        "parameter_count": len(orig_weights),
        "size_mb":         sum(t.numel() * t.element_size() for t in overlay.values()) / 1e6,
    },
}

verdict = "PASS" if all([SF_1, SF_2, SF_3]) else (
    "PARTIAL" if (SF_1 and SF_3) else "FAIL"
)
verdict_payload["verdict"] = verdict

print(json.dumps(verdict_payload, indent=2))
with open("/kaggle/working/smoke_test_verdict.json", "w") as f:
    json.dump(verdict_payload, f, indent=2)
print(f"\n=== VERDICT: {verdict} ===")
```

---

## 3. Verified Output Anchors (from PASS run)

| Cell | Anchor | Value |
|---|---|---|
| 1 | GPU name | `Tesla T4` (×2) |
| 1 | GPU memory per device | 15.64 GB |
| 1 | PyTorch version | 2.10.0+cu128 |
| 2 | transformers version | 4.45.2 |
| 3 | MEMIT SHA | `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` |
| 4 | cuda:0 allocated | 7.10 GB |
| 4 | cuda:1 allocated | 5.10 GB |
| 4 | lm_head device | `cuda:0` |
| 5 | Top-1 pre-edit | `basketball` (P=0.8702) |
| 6 | Final NaN check | `False` |
| 6 | Wall time | ~7–8 min (4 layer downloads × ~30 sec + 6 CPU solves × ~30 sec) |
| 7 | Top-1 post-edit | `baseball` (P=0.9819) |
| 7 | Ratio | 4270× |
| 8 | All layers restored | `True` |
| 9 | Top-1 post-unmount | `basketball` (P=0.8702 — bit-identical to pre-edit) |
| 10 | Verdict | `PASS` |

---

*End of Kaggle Canonical Notebook reference.*
