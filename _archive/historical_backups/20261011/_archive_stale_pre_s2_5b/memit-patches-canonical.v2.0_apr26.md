# MEMIT Patches — Canonical Specification

> **Source:** Session 2.2 smoke test PASS verdict (2026-04-26)
> **Target codebase:** `kmeng01/memit` at SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`
> **Target environment:** PyTorch 2.10.0+cu128, transformers 4.45.2, accelerate 0.34.2

This document is the canonical specification for the six patches required to make MEMIT operate on a 2026-vintage Python/PyTorch environment. Patches are recorded in application order. Each patch entry includes target file, exact replacement text, rationale, universality status, and verification procedure.

---

## 1. Patch Inventory

| Patch ID | Target | Universality | Required for RunPod RTX 4090? |
|---|---|---|---|
| P-1 | `util/nethook.py` retain_hook signature + inputs synthesis | Universal (any transformers ≥ 4.36) | Yes |
| P-2 | `util/nethook.py` register_forward_hook with_kwargs=True | Universal (any transformers ≥ 4.36) | Yes |
| P-3' | `memit/memit_main.py` torch.linalg.solve CPU FP64 offload | Conditional (cuda:0 capacity < 18 GiB) | **No** |
| Pad-Token | Tokenizer attribute | Universal (any GPT-2-derived tokenizer) | Yes |
| Device-Map | Cell 4 / model load | Conditional (multi-GPU only) | **No** |
| Copy-Unmount | Write engine unmount step | Universal (.vindex architecture requirement) | Yes |

For RunPod RTX 4090 single-GPU configuration, four patches are required: P-1, P-2, Pad-Token, Copy-Unmount. P-3' and Device-Map are not required.

---

## 2. Patch P-1 + P-2 — `util/nethook.py`

### 2.1 Target file

```
{MEMIT_ROOT}/util/nethook.py
```

### 2.2 Patch P-1 — Hook signature and inputs synthesis

**Original block (lines ≈ 75–82):**

```python
        def retain_hook(m, inputs, output):
            if retain_input:
```

**Replacement block:**

```python
        def retain_hook(m, args, kwargs, output):
            if args:
                inputs = args
            elif kwargs:
                inputs = (next(iter(kwargs.values())),)
            else:
                inputs = ()
            if retain_input:
```

### 2.3 Patch P-2 — Registration with_kwargs=True

**Original line (line ≈ 95):**

```python
        self.registered_hook = module.register_forward_hook(retain_hook)
```

**Replacement line:**

```python
        self.registered_hook = module.register_forward_hook(retain_hook, with_kwargs=True)
```

### 2.4 Rationale

PyTorch's default `register_forward_hook` captures only positional arguments. In `transformers ≥ 4.36`, the GPT-J and LLaMA block forward calls propagate inputs via keyword arguments through wrapped/checkpointed paths. The 2022-vintage MEMIT nethook signature receives `inputs = ()` (empty tuple), causing a downstream `IndexError: tuple index out of range` in `repr_tools._process` when input capture is requested. P-1 expands the hook signature to receive both `args` and `kwargs` and synthesizes a positional-shape `inputs` from whichever is non-empty. P-2 enables the `with_kwargs=True` flag (PyTorch ≥ 2.0) so that `kwargs` is actually populated.

### 2.5 Programmatic application

```python
import sys

NETHOOK_PATH = "{MEMIT_ROOT}/util/nethook.py"

with open(NETHOOK_PATH, "r") as f:
    src = f.read()

ORIG_SIG    = "def retain_hook(m, inputs, output):"
PATCHED_SIG = "def retain_hook(m, args, kwargs, output):"

if PATCHED_SIG not in src:
    assert ORIG_SIG in src
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

# Module reload
for name in [n for n in list(sys.modules)
             if n == "util" or n.startswith("util.")
             or n == "rome" or n.startswith("rome.")
             or n == "memit" or n.startswith("memit.")]:
    del sys.modules[name]
```

### 2.6 Verification

After patch application, the loaded module must satisfy:

```python
import inspect, util.nethook
src_loaded = inspect.getsource(util.nethook)
assert "def retain_hook(m, args, kwargs, output)" in src_loaded
assert "with_kwargs=True" in src_loaded
```

---

## 3. Patch P-3' — `memit/memit_main.py`

### 3.1 Target file

```
{MEMIT_ROOT}/memit/memit_main.py
```

### 3.2 Application condition

| Condition | Apply P-3'? |
|---|---|
| Single GPU with capacity ≥ 18 GiB (RTX 4090, A100, L4 24 GB, etc.) | No |
| Single GPU with capacity < 18 GiB | Yes |
| Multi-GPU configuration with cuda:0 capacity < 18 GiB | Yes |

For Stage 1 RunPod RTX 4090 (24 GiB), **P-3' is not required**.

### 3.3 Original block (lines ≈ 195–199)

```python
        adj_k = torch.linalg.solve(
            hparams.mom2_update_weight * cov.double() + layer_ks @ layer_ks.T,
            layer_ks,
        )
```

### 3.4 Replacement block

```python
        # PATCH (S22-P3'): full FP64 path on CPU.
        cov_cpu_fp64 = cov.cpu().double()
        layer_ks_cpu = layer_ks.cpu()
        adj_k = torch.linalg.solve(
            hparams.mom2_update_weight * cov_cpu_fp64 + layer_ks_cpu @ layer_ks_cpu.T,
            layer_ks_cpu,
        ).to(layer_ks.device)
        del cov_cpu_fp64, layer_ks_cpu
```

### 3.5 Rationale

For GPT-J's `d_ff = 16384`, the covariance matrix is 16384² × 4 bytes = 1.07 GiB FP32. Promotion to FP64 doubles this to 2.15 GiB. Combined with the FP32 outer product, the FP64 sum tensor, and the LU factorization workspace, peak transient on cuda:0 reaches ~4 GiB. This exceeds the headroom on a 16 GiB GPU after GPT-J 6B FP16 is loaded.

P-3' moves the FP64 promotion, the matrix sum, and the solve operation entirely to CPU memory (Kaggle host RAM is 32 GiB). The `adj_k` result is small (`d_ff × n_facts`) and is transferred back to GPU after the solve completes. Wall-time cost: ~30 sec per layer on CPU vs ~0.5 sec on GPU; ~3 min total across 6 layers.

The patch preserves the FP64 numerical fidelity that MEMIT's authors specifically chose; it relocates only where the computation occurs.

### 3.6 Programmatic application

```python
import sys

MEMIT_MAIN_PATH = "{MEMIT_ROOT}/memit/memit_main.py"

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

if "cov_cpu_fp64" not in src:
    assert ORIG_BLOCK in src
    src_new = src.replace(ORIG_BLOCK, PATCHED_BLOCK)
    with open(MEMIT_MAIN_PATH, "w") as f:
        f.write(src_new)

for name in [n for n in list(sys.modules)
             if n == "memit" or n.startswith("memit.")
             or n == "rome" or n.startswith("rome.")]:
    del sys.modules[name]
```

### 3.7 Verification

```python
import inspect, memit.memit_main
src_loaded = inspect.getsource(memit.memit_main)
assert "cov_cpu_fp64" in src_loaded
assert "cov.cpu().double()" in src_loaded
assert ".to(layer_ks.device)" in src_loaded
```

---

## 4. Pad-Token Patch — Tokenizer Attribute

### 4.1 Target

The `transformers.AutoTokenizer` instance loaded via `from_pretrained` for any GPT-2-derived tokenizer (GPT-J, GPT-Neo, GPT-NeoX, OPT).

### 4.2 Application

Immediately after `AutoTokenizer.from_pretrained(...)`:

```python
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
```

### 4.3 Rationale

GPT-J inherits GPT-2's tokenizer convention which has no `pad_token` by default. MEMIT's `generate_fast` utility batches multiple context prompts via `tok(prompts, padding=True, return_tensors="pt")`. In `transformers ≥ 4.x`, this raises `ValueError: Asking to pad but the tokenizer does not have a padding token`. Aliasing `pad_token` to `eos_token` is the canonical HuggingFace pattern; the resulting padded `eos_token` positions are masked by `attention_mask` during the forward pass.

### 4.4 LLaMA-specific note

LLaMA 3.1 8B (Stage 1+ production target) has its own pad token defined. The Stage 1 cell must check before aliasing:

```python
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
# Otherwise leave as-is
```

### 4.5 Verification

```python
assert tokenizer.pad_token is not None
assert tokenizer.pad_token_id is not None
```

---

## 5. Device-Map Patch — Multi-GPU Only

### 5.1 Application condition

| Condition | Apply Device-Map? |
|---|---|
| Single GPU with capacity ≥ 18 GiB | No (use `.to("cuda")`) |
| Single GPU with capacity < 18 GiB | Not viable; use multi-GPU instead |
| Multi-GPU (Kaggle 2× T4, etc.) | Yes |

For Stage 1 RunPod RTX 4090 (24 GiB single GPU), use `.to("cuda")` directly. **Device-Map is not required.**

### 5.2 Specification (Kaggle 2× T4 only)

```python
# Explicit device map: lm_head, embedding, ln_f, MEMIT edit range (3-8) on cuda:0.
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

model = GPTJForCausalLM.from_pretrained(
    MODEL_NAME, revision=REVISION, torch_dtype=torch.float16,
    low_cpu_mem_usage=True, device_map=explicit_map,
)
```

### 5.3 Rationale

`device_map="auto"` places `lm_head` on `cuda:1` to balance memory. MEMIT's `compute_z` directly accesses `lm_head.weight` and `lm_head.bias` as `lm_w` and `lm_b` and performs a manual matmul that bypasses accelerate's cross-device hooks. The result: `torch.gather` between an index tensor on `cuda:0` and logits on `cuda:1`, raising `RuntimeError: Expected all tensors on same device`.

The explicit map co-locates `lm_head`, `ln_f`, the embedding, and the MEMIT edit range (layers 3–8) on `cuda:0`, eliminating the cross-device boundary in `compute_z`.

### 5.4 Verification

```python
assert next(model.lm_head.parameters()).device.index == 0
assert next(model.transformer.ln_f.parameters()).device.index == 0
for i in [3, 4, 5, 6, 7, 8]:
    assert next(model.transformer.h[i].parameters()).device.index == 0
```

---

## 6. Copy-Unmount Patch — Universal Write Engine Pattern

### 6.1 Target

The framework's write engine unmount logic; specifically, the operation that restores pre-edit weights from `orig_weights` after an overlay is unmounted.

### 6.2 Forbidden pattern

```python
# DO NOT USE — desynchronizes visible parameter state from forward-pass-used parameter state
setattr(module, parameter_name, torch.nn.Parameter(orig_tensor.to(device)))
```

### 6.3 Canonical pattern

```python
target_param = getattr(module, parameter_name)
target_param.data.copy_(
    orig_tensor.to(target_param.device).to(target_param.dtype)
)
```

### 6.4 Rationale

`accelerate`'s device_map system installs forward-pre-hooks on each module that capture references to `nn.Parameter` objects at hook-installation time. The `setattr` pattern installs a new `nn.Parameter` at the attribute name but leaves the hook's cached reference pointing to the old (still-edited) Parameter. The result: `getattr(module, name).data` shows the restored values (visible state), but the forward pass routes through accelerate's hooks and uses the old Parameter's data (computational state). The two diverge.

The `copy_()` pattern modifies the existing Parameter's tensor data in place. The Parameter object identity is preserved; all external references (accelerate hooks, tied-parameter maps, forward-graph caches) remain valid and now point to the restored data.

### 6.5 Per-layer verification (mandatory)

```python
import torch

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

assert all_match
```

### 6.6 Forward-pass verification (mandatory after parameter verification)

Parameter-state verification is necessary but not sufficient (per OQ-S22-35). After the per-layer `allclose` check, an end-to-end forward pass must confirm that the model's behavior reverts to pre-edit:

```python
with torch.no_grad():
    logits = model(input_ids).logits[0, -1, :]
    top1_id = torch.topk(logits, k=1).indices.item()
assert tokenizer.decode([top1_id]).strip() == ORIGINAL_TOP_1_TOKEN
```

---

## 7. Application Order

### 7.1 Universal patches (apply in all environments)

```
1. P-1 + P-2 (nethook)
   ↓ purge sys.modules of util.*, rome.*, memit.*
2. Pad-Token alias
3. (P-3' if conditions met)
   ↓ purge sys.modules of memit.*, rome.*
4. (Device-Map if conditions met — applied at from_pretrained, not retrofittable)
5. apply_memit_to_model(...)
   ↓ produces edited_model, orig_weights
6. Copy-Unmount (when overlay unmount is needed)
```

### 7.2 RunPod RTX 4090 sequence (Stage 1 production target)

```
1. P-1 + P-2 (nethook)
2. Pad-Token alias
3. .to("cuda") model load (no Device-Map needed)
4. apply_memit_to_model(...)
5. Copy-Unmount when overlay unmount is needed
```

### 7.3 Kaggle 2× T4 sequence (smoke-test reference; not Stage 1 target)

```
1. P-1 + P-2 (nethook)
2. P-3' (memit_main solve)
3. Pad-Token alias
4. Device-Map at from_pretrained
5. apply_memit_to_model(...)
6. Copy-Unmount when overlay unmount is needed
```

---

## 8. Manifest Requirements

The reproducibility manifest must record patch state per the following schema:

```json
{
  "patches_applied": {
    "memit_nethook_p1_signature_and_inputs_synthesis": true,
    "memit_nethook_p2_with_kwargs_registration": true,
    "memit_solve_cpu_offload_p3_prime": false,
    "tokenizer_pad_token_alias": true,
    "explicit_device_map": false,
    "unmount_in_place_copy_only": true
  },
  "patches_required_but_not_applied": []
}
```

The `patches_required_but_not_applied` list must be empty for any verdict to be PASS. Patches conditionally not required (e.g., P-3' on RTX 4090) are reported as `false` in `patches_applied` and are NOT listed in `patches_required_but_not_applied`.

---

## 9. Upstream Submission Notes

`kmeng01/memit` is unmaintained (last commit 2022-11-14; 16 open issues; no triage). Patches P-1, P-2, P-3' are reported but not submitted upstream — submission would not be merged. The framework's POC must fork the repository and pin to a known-patched fork rather than upstream `kmeng01/memit`. Forking work is deferred to Workstream 1 future tasks (per OQ-S22-17).

---

*End of MEMIT Patches Canonical Specification.*
