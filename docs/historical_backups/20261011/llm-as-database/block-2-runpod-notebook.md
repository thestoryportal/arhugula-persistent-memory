# Block 2 — RunPod Canonical Notebook

> **Target environment:** RunPod RTX 4090 24 GB single GPU (Stage 1 production target)
> **Cell count:** 10 (no Cell 5f; Cell 4 simplified to direct `.to("cuda")`)
> **Wall time:** ~10–15 min full top-to-bottom

This document is the canonical 10-cell notebook for the RunPod dry-run reproduction (Step 2.4 of `block-2-execution-plan.md`). It differs from the Kaggle 13-cell notebook in two ways: Cell 5f (P-3' patch) is omitted because RTX 4090 has sufficient memory for GPU FP64 solve; Cell 4 uses direct `.to("cuda")` because single-GPU configurations do not require explicit device mapping.

---

## 1. Pod Configuration

| Setting | Value |
|---|---|
| GPU | 1× RTX 4090 (Secure Cloud) |
| Pod type | On-demand |
| Container image | Pinned per Step 2.3 of `block-2-execution-plan.md` |
| Network Volume | Mount at `/workspace` |
| Working directory | `/workspace` |

## 2. Pre-Notebook Pod Setup

```bash
# Inside pod terminal, before launching Jupyter
cd /workspace
mkdir -p memit_dry_run
cd memit_dry_run

# Verify environment
nvidia-smi
df -h /workspace
python --version
```

Expected:

| Anchor | Expected value |
|---|---|
| GPU | NVIDIA RTX 4090, 24576 MiB |
| `/workspace` | ~100 GB total |
| Python | 3.10 or 3.11 |

## 3. Cell-by-Cell Specification

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
        print(f"GPU {i} compute: sm_{props.major}{props.minor}")
print(subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version,name,memory.total",
                                "--format=csv"], text=True))
```

Verification anchors:

| Anchor | Expected on RunPod RTX 4090 |
|---|---|
| GPU name | NVIDIA GeForce RTX 4090 |
| GPU memory | ~24.00 GB |
| Compute capability | sm_89 (Ada Lovelace) |
| GPU count | 1 |

### Cell 2 — Pip install joint 4.x-line stack

```python
# === CELL 2 — Pip install joint 4.x-line stack ===
import subprocess, sys

subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
    "transformers==4.45.2",
    "accelerate==0.34.2",
    "huggingface_hub==0.25.2",
    "tokenizers==0.20.3",
    "safetensors==0.4.5",
    "hydra-core==1.3.2",
    "einops==0.7.0",
    "nltk==3.8.1",
], check=True)

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

Note: `subprocess.run` is used instead of `!pip` because RunPod's Jupyter may differ in shell handling. Equivalent functionally.

### Cell 3 — MEMIT clone

```python
# === CELL 3 — MEMIT clone (rmtree first; persistent NV path) ===
import subprocess, os, shutil, sys

os.chdir("/workspace/memit_dry_run")
if os.path.exists("memit"):
    shutil.rmtree("memit")
    print("Removed prior memit/ directory.")

subprocess.run(["git", "clone", "https://github.com/kmeng01/memit.git"], check=True)
os.chdir("/workspace/memit_dry_run/memit")

memit_sha    = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
memit_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
memit_date   = subprocess.check_output(["git", "log", "-1", "--format=%ci"], text=True).strip()

print(f"MEMIT SHA:     {memit_sha}")
print(f"Branch:        {memit_branch}")
print(f"Commit date:   {memit_date}")
assert memit_sha == "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b", "SHA pin mismatch"

sys.path.insert(0, "/workspace/memit_dry_run/memit")
```

### Cell 4 — Model load (direct, single GPU)

```python
# === CELL 4 — Model load (direct .to('cuda'); single GPU) ===
from transformers import GPTJForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "EleutherAI/gpt-j-6B"
REVISION   = "float16"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Downloading float16 model (single-GPU direct load; ~5-8 min)...")
model = GPTJForCausalLM.from_pretrained(
    MODEL_NAME,
    revision=REVISION,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to("cuda")
model.eval()

assert model.config.n_layer == 28
assert model.config.n_embd  == 4096

import huggingface_hub
revision_sha = huggingface_hub.HfApi().model_info(MODEL_NAME, revision=REVISION).sha
print(f"GPT-J revision SHA: {revision_sha}")
print(f"Loaded device:      {next(model.parameters()).device}")
print(f"Loaded dtype:       {next(model.parameters()).dtype}")
print(f"GPU mem used:       {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"GPU mem total:      {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

Verification anchors:

| Anchor | Expected on RTX 4090 |
|---|---|
| Loaded device | `cuda:0` |
| Loaded dtype | `torch.float16` |
| GPU mem used | ~12.10 GB (matches Kaggle Cell 4 v1) |
| GPU mem total | ~24.00 GB |

### Cell 5 — Pre-edit elicitation

```python
# === CELL 5 — Pre-edit elicitation ===
import torch

PROMPT = "Michael Jordan plays the sport of"
input_ids = tokenizer(PROMPT, return_tensors="pt").input_ids.to("cuda")

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

Expected: bit-identical pre-edit probabilities to the Kaggle baseline (P_basketball_pre = 0.8702, P_baseball_pre = 0.0214) because the model checkpoint and inference path are mathematically equivalent.

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

NETHOOK_PATH = "/workspace/memit_dry_run/memit/util/nethook.py"

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

**Note:** No Cell 5f (P-3' patch) on RunPod RTX 4090. The 24 GB envelope accommodates the 4 GiB FP64 transient on GPU directly.

### Cell 6 — MEMIT edit

```python
# === CELL 6 — MEMIT edit ===
from memit import MEMITHyperParams, apply_memit_to_model
import torch

hparams = MEMITHyperParams.from_json(
    "/workspace/memit_dry_run/memit/hparams/MEMIT/EleutherAI_gpt-j-6B.json"
)
print(f"Edit layers: {hparams.layers}")

requests = [{
    "prompt":     "{} plays the sport of",
    "subject":    "Michael Jordan",
    "target_new": {"str": "baseball"},
}]

print("Applying MEMIT edit (~3-5 min on RTX 4090)...")
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

Wall time expectation: ~3–5 min (vs ~7–8 min on Kaggle T4 with CPU solve). The GPU FP64 solve on RTX 4090 is ~60× faster than CPU FP64 solve.

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

os.makedirs("/workspace/memit_dry_run/smoke_test_overlay", exist_ok=True)

overlay = {
    name: edited_model.state_dict()[name].detach().cpu().clone()
    for name in orig_weights.keys()
}
torch.save(overlay,      "/workspace/memit_dry_run/smoke_test_overlay/edited.pt")
torch.save(orig_weights, "/workspace/memit_dry_run/smoke_test_overlay/original.pt")

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

### Cell 10 — Verdict emission and Kaggle comparison (HC-2)

```python
# === CELL 10 — Verdict emission + HC-2 Kaggle comparison ===
import json
from datetime import datetime, timezone

# Kaggle baseline (from Session 2.2 PASS verdict)
KAGGLE_BASELINE = {
    "P_basketball_pre":         0.8701928853988647,
    "P_baseball_pre":           0.021447110921144485,
    "P_baseball_post":          0.9818863868713379,
    "P_basketball_post":        0.00022994860773906112,
    "P_basketball_postunmount": 0.8701928853988647,
    "P_baseball_postunmount":   0.021447110921144485,
}

# Compute drift from Kaggle baseline
def drift(measured, baseline):
    if baseline == 0:
        return None
    return abs(measured - baseline) / baseline

drift_post_baseball   = drift(P_BASEBALL_POST,   KAGGLE_BASELINE["P_baseball_post"])
drift_post_basketball = drift(P_BASKETBALL_POST, KAGGLE_BASELINE["P_basketball_post"])
drift_unmount_basketball = drift(P_BASKETBALL_POSTUNMOUNT, KAGGLE_BASELINE["P_basketball_postunmount"])

# HC-2 acceptance band (per block-2-execution-plan §6.5)
HC_2_PASS = (
    SF_1 and SF_2 and SF_3
    and drift_post_baseball < 0.05  # within 5% of Kaggle 0.9819
    and drift_post_basketball < 10  # within order of magnitude
    and drift_unmount_basketball < 1e-6  # bit-identical (overlay isolation)
)

verdict_payload = {
    "smoke_test": "MEMIT-COMPAT-PROTO-1 single-fact rehearsal (RunPod RTX 4090)",
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "venue": "RunPod RTX 4090 24 GB Secure Cloud",
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
        "device_map": "single GPU direct .to('cuda')",
    },
    "patches_applied": {
        "memit_nethook_with_kwargs":      True,
        "memit_nethook_inputs_synthesis": True,
        "memit_solve_cpu_offload_p3prime": False,    # NOT applied on RTX 4090
        "tokenizer_pad_token_alias":      True,
        "explicit_device_map":            False,    # NOT applied on single GPU
        "unmount_in_place_copy_only":     True,
    },
    "patches_required_but_not_applied": [],   # all required patches were applied
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
    "hc_2_kaggle_comparison": {
        "kaggle_baseline_completed_at": "2026-04-26T07:08:30.578814+00:00",
        "drift_p_baseball_post":         drift_post_baseball,
        "drift_p_basketball_post":       drift_post_basketball,
        "drift_p_basketball_postunmount": drift_unmount_basketball,
        "hc_2_acceptance_band": {
            "P_baseball_post_max_drift":         0.05,
            "P_basketball_post_max_drift":       10,
            "P_basketball_postunmount_max_drift": 1e-6,
        },
        "hc_2_pass": HC_2_PASS,
    },
}

verdict = "PASS" if all([SF_1, SF_2, SF_3]) else (
    "PARTIAL" if (SF_1 and SF_3) else "FAIL"
)
verdict_payload["verdict"] = verdict
verdict_payload["hc_2_verdict"] = "PASS" if HC_2_PASS else "FAIL"

print(json.dumps(verdict_payload, indent=2))
with open("/workspace/memit_dry_run/runpod_dry_run_verdict.json", "w") as f:
    json.dump(verdict_payload, f, indent=2)
print(f"\n=== VERDICT: {verdict} ===")
print(f"=== HC-2:    {'PASS' if HC_2_PASS else 'FAIL'} ===")
```

## 4. Post-Notebook Pod Actions

```bash
# Inside pod terminal, after Cell 10
ls -la /workspace/memit_dry_run/runpod_dry_run_verdict.json
cat /workspace/memit_dry_run/runpod_dry_run_verdict.json | python -m json.tool

# Verify NV layout for Block 3
ls -la /workspace/
df -h /workspace/
```

## 5. Reportable Items After Block 2 Step 2.4

| Item | Source |
|---|---|
| Cell 1 GPU verification | Cell 1 stdout |
| Cell 4 GPU mem used | Cell 4 stdout |
| Cell 6 wall time | Operator observation (3–5 min expected) |
| HC-2 verdict and drift values | Cell 10 stdout / verdict JSON |
| Total dry-run pod cost | RunPod Account → Billing |

## 6. Halt Conditions (Block 2 Step 2.4 Specific)

| Condition | Halt scope |
|---|---|
| Cell 4 reports `GPU mem used` > 14 GB | Unexpected memory profile; investigate before Cell 6 |
| Cell 6 raises `OutOfMemoryError` | RTX 4090 envelope exceeded — surprising; would invalidate Stage 1 single-GPU plan |
| Cell 6 wall time > 30 min | Possible numerical issue or covariance fetch failure |
| HC-2 numerical drift exceeds band | Material environment-dependent behavior; investigate before Stage 1 |
| Any SF assertion FAILs | RunPod-specific MEMIT defect; investigate before Stage 1 |

---

*End of Block 2 RunPod Canonical Notebook.*
