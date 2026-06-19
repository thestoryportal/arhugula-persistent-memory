# MEMIT Patches — Canonical Specification

> **Source:** Session 2.2 smoke test PASS verdict (2026-04-26); P-4 added per Session 2.5a smoke test PASS verdict (2026-04-29) and ratified in Session 2.5b §4.5 (D-S25-11, C-S25-9, IC-S25-2); v2.1 corrections per Session 2.5b §4.5b (C-S25-13 path correction; C-S25-14 dual canonical-form ratification — surfaced by pre-S2.6 fork-work runbook Cell 2 empirical verification); v2.2 expansions per Session 2.5b §4.5 (§3.5.4 line table correction + §3.5.7 application script correction closing OQ-PreS26-1; §4.4 Pad-Token note correction closing OQ-PreS26-2; §3.6 P-5 entry authored from §4.0 closing OQ-PreS26-6; new constraint C-S25-15 substrate-shift); v2.2.1 footer-version-addition patch per Session 2.5b §4.3 execution (closes OQ-S25b-5 — document footer carried no version marker; surgical str_replace edit to add `v2.2.1.` to footer; no semantic change to canonical doc content)
> **Version:** 2.2.1 (supersedes v2.2 — footer-version-addition patch only; no semantic content change)
> **Target codebase:** `kmeng01/memit` at SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`
> **Target environment:** PyTorch 2.10.0+cu128, transformers 4.45.2, accelerate 0.34.2, datasets 4.8.3 (locked per C-S25-6 — incompatible with script-based loaders; see §3.6 P-5)

This document is the canonical specification for the eight patches required to make MEMIT operate on a 2026-vintage Python/PyTorch environment across both GPT-2-family base models (the original MEMIT target — GPT-J 6B reference) and non-GPT-2-family base models (LLaMA 3.x family, Mistral, Qwen, Phi, Gemma — added with P-4). Patches are recorded in application order. Each patch entry includes target file, exact replacement text, rationale, universality status, and verification procedure.

---

## 1. Patch Inventory

| Patch ID | Target | Universality | Required for RunPod RTX 4090 (LLaMA 3.1 8B target)? |
|---|---|---|---|
| P-1 | `util/nethook.py` retain_hook signature + inputs synthesis | Universal (any transformers ≥ 4.36) | Yes |
| P-2 | `util/nethook.py` register_forward_hook with_kwargs=True | Universal (any transformers ≥ 4.36) | Yes |
| P-3' | `memit/memit_main.py` torch.linalg.solve CPU FP64 offload | Conditional (cuda:0 capacity < 18 GiB) | **No** |
| P-4 | `memit/compute_z.py`, `rome/compute_v.py`, `rome/layer_stats.py` config-attribute fallback | Universal (required for non-GPT-2-family; backward-compatible on GPT-J) | **Yes** |
| P-5 | `rome/layer_stats.py` dataset loader modernization (script-based `wikipedia` → parquet `wikimedia/wikipedia 20231101.en`) | Conditional (required when `datasets ≥ 3.0` AND `ds_name == "wikipedia"`) | **Yes** |
| Pad-Token | Tokenizer attribute | Universal (any base model with `pad_token = None`; LLaMA-conditional per §4.4) | Yes (LLaMA-conditional) |
| Device-Map | Cell 4 / model load | Conditional (multi-GPU only) | **No** |
| Copy-Unmount | Write engine unmount step | Universal (.vindex architecture requirement) | Yes |

For RunPod RTX 4090 single-GPU configuration with LLaMA 3.1 8B as the Stage 1 target, **six patches are required**: P-1, P-2, **P-4**, **P-5**, Pad-Token, Copy-Unmount. P-3' and Device-Map are not required.

For Kaggle 2× T4 with GPT-J 6B (Session 2.2 smoke-test reference), **seven patches are required**: P-1, P-2, P-3', P-4 (optional but safe — backward-compatible), P-5 (conditional — required if `datasets ≥ 3.0` and `wikipedia` dispatch path is consumed), Pad-Token, Device-Map, Copy-Unmount.

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

## 3.5 Patch P-4 — Config-Attribute Compatibility for Non-GPT-2-Family

> **Numbering note:** P-4 is inserted as §3.5 — between §3 P-3' and §4 Pad-Token — to avoid a doc-wide section renumber. External references (notably `stage_1_sect_runbook.md` v1.1 cites `memit-patches-canonical §4.4` and `§6`) remain valid. A future major revision of this document may consolidate the numbering. The patch ID `P-4` follows the integer-incrementing patch-ID convention (P-1, P-2, P-3', P-4, …) independent of section number.

### 3.5.1 Target files

```
{MEMIT_ROOT}/memit/compute_z.py        (one site, line ≈ 81)
{MEMIT_ROOT}/rome/compute_v.py        (one site, line ≈ 72)
{MEMIT_ROOT}/rome/layer_stats.py      (two sites, lines ≈ 101 and 108)
```

Line numbers are nominal at the SHA pin and may drift; the idempotent application script in §3.5.7 locates replacement targets by string match, not line number.

### 3.5.2 Application condition

| Base model family | Apply P-4? |
|---|---|
| GPT-2-family (GPT-2, GPT-J, GPT-Neo, GPT-NeoX) | Optional — patch is backward-compatible via `getattr-or-fallback`; safe to apply |
| LLaMA family (LLaMA 2, LLaMA 3.x — including LLaMA 3.1 8B Stage 1 target per D-S25-5) | **Required** |
| Mistral family (Mistral, Mixtral) | **Required** |
| Qwen, Phi, Gemma, and other HF-2.0-config families | **Required** |

For Stage 1 RunPod RTX 4090 + LLaMA 3.1 8B, **P-4 is required**.

### 3.5.3 Pattern

P-4 replaces two GPT-2-vintage config attribute references with `getattr-or-fallback` patterns that resolve correctly on any HF transformers config:

**Attribute 1 — hidden dimension lookup**

Original (GPT-2 / GPT-J vintage):

```python
model.config.n_embd
```

Replacement:

```python
(getattr(model.config, 'hidden_size', None) or model.config.n_embd)
```

**Attribute 2 — positional context window lookup**

Original (GPT-2 / GPT-J vintage):

```python
model.config.n_positions
```

Replacement:

```python
(getattr(model.config, 'max_position_embeddings', None) or model.config.n_positions)
```

### 3.5.4 Per-file substitution map

The canonical replacement form (produced by §3.5.7's application script) is the **single-fallback** form. The S2.5a NV record empirically carries the **doubled-fallback** form at two of four sites (see §3.5.10 for ratification). Both forms are spec-compliant per C-S25-14.

| File | Original attribute | Approx. line | Canonical replacement (single-fallback) | S2.5a NV record |
|---|---|---|---|---|
| `memit/compute_z.py` | `model.config.n_embd` | 81 | `(getattr(model.config, 'hidden_size', None) or model.config.n_embd)` | doubled-fallback |
| `rome/compute_v.py` | `model.config.n_embd` | 72 | `(getattr(model.config, 'hidden_size', None) or model.config.n_embd)` | doubled-fallback |
| `rome/layer_stats.py` | `model.config.n_positions` | 101 | `(getattr(model.config, 'max_position_embeddings', None) or model.config.n_positions)` | single-fallback |
| `rome/layer_stats.py` | `model.config.n_positions` | 108 | `(getattr(model.config, 'max_position_embeddings', None) or model.config.n_positions)` | single-fallback |

**v2.2 correction note (closes OQ-PreS26-1):** the v2.0/v2.1 form of this table listed site 4 (`rome/layer_stats.py` line 108) as `n_embd → hidden_size`, repeating the pattern shown at the line-101 row of v2.0. Empirical evidence from `pre_s2_6_fork_work_runbook.md` v1.0 Cell 2 (2026-04-30) — pod-side grep + sed inspection — established that both sites in `rome/layer_stats.py` are `n_positions → max_position_embeddings` patches; there is no `hidden_size` site in `rome/layer_stats.py`. v2.2 corrects the row above, and §3.5.7's application script is correspondingly corrected (see §3.5.7 v2.2 correction note). Cross-references: D-PreS26-1, OQ-PreS26-1.

### 3.5.5 Rationale

HF `transformers` migrated GPT-2-family naming conventions (`n_embd`, `n_positions`) to a unified config schema (`hidden_size`, `max_position_embeddings`) for non-GPT-2-family models. LLaMA, Mistral, Qwen, Phi, Gemma, and most post-2022 model families use the unified names. GPT-2, GPT-J, GPT-Neo, and GPT-NeoX retain the original GPT-2-family names.

MEMIT's compute path (`memit/compute_z.py`, `rome/compute_v.py`, `rome/layer_stats.py`) was authored against GPT-J's config and hard-codes `n_embd` / `n_positions`. Without P-4, `apply_memit_to_model(...)` against a LLaMA-family base raises `AttributeError: 'LlamaConfig' object has no attribute 'n_embd'` at the first compute_z invocation.

The `getattr(config, 'new_name', None) or config.old_name` pattern resolves to the HF-2.0 attribute when present, falling back to the GPT-2 attribute when not. The two code paths execute identically under the truthy-or-fallback semantics:

- **GPT-J** — `getattr` returns `None` (config has no `hidden_size`); `or` short-circuits to `model.config.n_embd`. Computation identical to pre-patch.
- **LLaMA-family** — `getattr` returns the `hidden_size` integer; `or` short-circuits at the truthy first operand. Computation now defined where it previously raised `AttributeError`.

### 3.5.6 Backward-compatibility assertion

P-4 is universal-safe: it produces correct behavior on both GPT-2-family (preserving the Session 2.2 Kaggle smoke-test PASS) and non-GPT-2-family (enabling the Session 2.5a LLaMA smoke-test PASS — D-S25-5). No conditional application logic is required at apply time.

| Base model | Pre-P-4 behavior | Post-P-4 behavior |
|---|---|---|
| GPT-J 6B (Session 2.2 baseline) | PASS via `n_embd` direct access | PASS via fallback to `n_embd`; identical computation |
| LLaMA 3.1 8B (Session 2.5a smoke test) | `AttributeError` at compute_z.py:81 | PASS via `hidden_size`; first MEMIT edit on LLaMA |

### 3.5.7 Programmatic application (idempotent)

The script verifies pre-state, applies replacements only where not already present, and verifies post-state. Re-running is safe; partial-patch states (e.g., from interrupted prior runs) are correctly detected and completed.

This script produces the **single-fallback canonical form** at all four sites. The S2.5a NV record carries the **doubled-fallback form** at two sites (see §3.5.10); a fresh checkout re-patched via this script will diverge in surface form from the S2.5a NV record while remaining functionally equivalent per C-S25-14. Verification (§3.5.8) accepts both forms because it tests for substring presence of `hidden_size` / `max_position_embeddings`, not full-replacement-string equality.

**v2.2 correction note (closes OQ-PreS26-1, application-script portion):** the v2.0/v2.1 form of this script's `P4_TARGETS` for `rome/layer_stats.py` carried two replacement tuples — `(n_positions, max_position_embeddings)` AND `(n_embd, hidden_size)` — paralleling v2.0's incorrect §3.5.4 line table. Per D-PreS26-1's empirical finding (both `layer_stats.py` patch sites are `n_positions`; no `n_embd` site exists), the second tuple was spurious. v2.2 removes it. The script as authored in v2.0/v2.1 was never empirically run: S2.5a's smoke test PASS used in-session ad-hoc patching that predated §3.5.7's existence; pre-S2.6 fork-work used Cell 2 verification (substring presence) only, not Cell 2 application. The latent defect would have manifested as `AssertionError: P-4 cannot apply: site for 'model.config.n_embd' not found in {layer_stats.py}` on first fresh-checkout application via this script — including against the S2.5a NV state. v2.2 corrects the script before any successor session attempts to apply P-4 to a fresh checkout.

```python
import os

MEMIT_ROOT = "{MEMIT_ROOT}"
SHA_PIN    = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

# Per-file replacement schedule
P4_TARGETS = [
    (
        f"{MEMIT_ROOT}/memit/compute_z.py",
        [
            ("model.config.n_embd",
             "(getattr(model.config, 'hidden_size', None) or model.config.n_embd)"),
        ],
    ),
    (
        f"{MEMIT_ROOT}/rome/compute_v.py",
        [
            ("model.config.n_embd",
             "(getattr(model.config, 'hidden_size', None) or model.config.n_embd)"),
        ],
    ),
    (
        f"{MEMIT_ROOT}/rome/layer_stats.py",
        [
            ("model.config.n_positions",
             "(getattr(model.config, 'max_position_embeddings', None) or model.config.n_positions)"),
        ],
    ),
]

P4_HIDDEN_MARKER = "getattr(model.config, 'hidden_size', None)"
P4_MAXPOS_MARKER = "getattr(model.config, 'max_position_embeddings', None)"

for path, replacements in P4_TARGETS:
    with open(path) as f:
        src = f.read()

    # Determine the markers that should be present after full patching for this file
    expected_markers = set()
    for orig, _ in replacements:
        if orig == "model.config.n_embd":
            expected_markers.add(P4_HIDDEN_MARKER)
        elif orig == "model.config.n_positions":
            expected_markers.add(P4_MAXPOS_MARKER)

    # Idempotency: only treat as fully patched if ALL expected markers are present.
    # A partial-patch state (some markers present, some missing) is detected and completed below.
    fully_patched = all(m in src for m in expected_markers)
    if fully_patched:
        print(f"P-4 already fully applied to {path}; skipping")
        continue

    # Apply each replacement; skip individually if its replacement form is already present
    src_new = src
    applied_count = 0
    for orig, replacement in replacements:
        if replacement in src_new:
            print(f"  partial-state: {orig!r} already replaced in {path}; skipping that site")
            continue
        if orig in src_new:
            src_new = src_new.replace(orig, replacement)
            applied_count += 1
        else:
            # Neither original nor replacement form found at this site
            raise AssertionError(
                f"P-4 cannot apply: site for {orig!r} not found in {path}. "
                f"MEMIT SHA may have drifted from {SHA_PIN}; verify repo state."
            )

    # Post-state verification — every expected marker MUST be present before write
    for marker in expected_markers:
        assert marker in src_new, (
            f"P-4 marker {marker!r} not present after replace in {path}; "
            f"file would be left in inconsistent state — aborting write"
        )

    with open(path, "w") as f:
        f.write(src_new)
    print(f"P-4 applied to {path} ({applied_count} site(s) updated)")
```

### 3.5.8 Verification (anchored to `stage_1_sect_runbook.md` Cell 2)

The runbook Cell 2 codifies P-4 verification with grep-style markers. Re-stated here for canonical reference; the runbook's logic is the authoritative reference at execution time.

```python
# Per-file marker assertions (v2.2 corrected form; closes OQ-PreS26-1 verification-logic portion)
p4_targets = [
    f"{MEMIT_ROOT}/memit/compute_z.py",
    f"{MEMIT_ROOT}/rome/compute_v.py",
    f"{MEMIT_ROOT}/rome/layer_stats.py",
]
p4_marker_hidden_size = "hidden_size"
p4_marker_max_pos     = "max_position_embeddings"

for path in p4_targets:
    with open(path) as f:
        src = f.read()
    if path.endswith("layer_stats.py"):
        # Both patch sites in layer_stats.py (lines ≈ 101, 108) are
        # n_positions → max_position_embeddings; there is no hidden_size site
        # per D-PreS26-1 empirical evidence.
        assert src.count(p4_marker_max_pos) >= 2, \
            f"P-4 (max_position_embeddings fallback) missing in {path}; expected ≥ 2 occurrences"
    elif path.endswith("compute_z.py"):
        assert p4_marker_hidden_size in src, f"P-4 (hidden_size fallback) not applied in {path}"
    elif path.endswith("compute_v.py"):
        assert p4_marker_hidden_size in src, f"P-4 (hidden_size fallback) not applied in {path}"
```

**v2.2 correction note (closes OQ-PreS26-1, verification-logic portion):** the v2.0/v2.1 form of this verification logic asserted `hidden_size in src` for `layer_stats.py`. Per D-PreS26-1's empirical finding (no `hidden_size` site exists in `layer_stats.py`; both patch sites are `n_positions → max_position_embeddings`), that assertion would fail. The corrected form above tests `max_position_embeddings` occurrence count `≥ 2` for `layer_stats.py`, and tests `hidden_size` substring presence for `compute_z.py` + `compute_v.py` only. The runbook's Cell 2 verification logic carries a parallel defect that the v1.1 form of `pre_s2_6_fork_work_runbook.md` and the v1.2 form of `stage_1_sect_runbook.md` both inherit; pre_s2_6_fork_work_runbook v1.2 (S2.5b §4.7) corrects its Cell 2 logic to match the form above; `stage_1_sect_runbook.md` v1.2 Cell 2 correction is out-of-scope for S2.5b and surfaces as **OQ-S25b-1** for a future runbook hardening pass.

The runbook's grep-style check (substring presence of `hidden_size` / `max_position_embeddings`, with `>= 2` counting where applicable) is intentionally weaker than the application script's marker check (full `getattr(...)` substring). This is by design: the runbook check tolerates minor formatting variation (spacing, parenthesization) while still catching unpatched files. Both checks are aligned and either one sufficiently certifies P-4 application for Stage 1 gating.

### 3.5.9 Discovery provenance

P-4 was discovered during Session 2.5a smoke test attempts 6 and 7 against the LLaMA 3.1 8B base model:

- **Attempt 6** failed at `compute_z.py:81` with `AttributeError: 'LlamaConfig' object has no attribute 'n_embd'`
- **Attempt 7** patched compute_z.py only; surfaced the next site at `layer_stats.py:101` (`n_positions`)
- **Attempt 8** generalized the pattern across all four sites in `compute_z.py`, `compute_v.py`, and `layer_stats.py` (×2); produced the smoke-test PASS verdict

The patch family was authored in-session and committed to NV-resident MEMIT repo state. Backward-compatibility against GPT-J was reasoned analytically (the `or`-fallback semantics) and verified by inspection that the runbook's existing GPT-J reference path was unchanged in the patched files.

References:

- `C-S25-9` (constraint encoding the P-4 patch family — superseded on directory by C-S25-13)
- `D-S25-11` (P-4 authorship + application decision; Session 2.5a)
- `IC-S25-2` (P-4 idempotency interface contract)
- `session_2_5a_summary_block.md` § "Constraints established"
- `stage_1_sect_runbook.md` v1.1 Cell 2 (verification logic anchor; superseded by v1.2)

### 3.5.10 Empirical NV record (S2.5b §4.5b ratification)

Surfaced by `pre_s2_6_fork_work_runbook.md` v1.0 Cell 2 execution (2026-04-30) — first re-verification of the S2.5a NV-resident MEMIT repo against documented patch state since S2.5a close. Two defects were ratified in S2.5b §4.5b:

**Defect 1 — directory drift in spec doc family.** This document v2.0, `stage_1_sect_runbook.md` v1.1, and `pre_s2_6_fork_work_runbook.md` v1.0 all encoded `compute_z.py` as living at `{MEMIT_ROOT}/rome/compute_z.py`. Empirical record: `compute_z.py` lives at `{MEMIT_ROOT}/memit/compute_z.py` (sibling of `memit_main.py` inside the MEMIT package directory). `compute_v.py` and `layer_stats.py` live at `{MEMIT_ROOT}/rome/` as documented. v2.1 corrects all in-document path references and surfaces C-S25-13:

> **C-S25-13:** MEMIT `compute_z.py` canonical path is `{MEMIT_ROOT}/memit/compute_z.py`. Supersedes the directory encoding in C-S25-9, D-S25-11, IC-S25-2, and the v2.0 form of this document.

**Defect 2 — replacement-form drift in S2.5a empirical record.** S2.5a's in-session ad-hoc patch authoring (attempts 6→7→8, prior to §3.5.7's existence) wrote the **doubled-fallback** form at `memit/compute_z.py:81` and `rome/compute_v.py:72`, and the **single-fallback** form at `rome/layer_stats.py:101,108`. Both forms evaluate identically:

```
LLaMA   (hidden_size = 4096):  4096   or (4096   or n_embd_AttributeError) → 4096
GPT-J   (no hidden_size):      None   or (None   or 4096                 ) → 4096
```

The outer `or` short-circuits on truthy `hidden_size` (LLaMA family), and the inner expression is reached only when `hidden_size` is `None` (GPT-2 family) — at which point the `n_embd` access succeeds. Functional equivalence holds across both target families.

C-S25-14 ratifies both forms as canonical:

> **C-S25-14:** P-4 has two functionally equivalent canonical forms — single-fallback (`getattr(...) or fallback`) and doubled-fallback (`getattr(...) or (getattr(...) or fallback)`). The S2.5a NV record carries the doubled form at `memit/compute_z.py:81` and `rome/compute_v.py:72`, and the single form at `rome/layer_stats.py:101,108`. §3.5.7's application script produces the single form exclusively; future fresh applications will diverge from the S2.5a NV record in surface form while remaining functionally equivalent. The S2.5a smoke-test PASS verdict (`/workspace/architecture_profile/llama_smoke_test_verdict.json`) is the empirical anchor; this document defers to the NV record rather than modifying it.

**Why ratify-not-fix:** the S2.5a NV record is the empirical anchor for every downstream claim that "P-4 is correctly applied." Modifying the NV repo to match v2.0's spec (replacing doubled with single form) would invalidate that anchor and require re-running the smoke test against the new bytes. Ratifying both forms preserves the anchor at zero compute cost.

References:

- `C-S25-13` (directory correction)
- `C-S25-14` (dual-form ratification)
- `pre_s2_6_fork_work_runbook.md` v1.0 Cell 2 (discovery site)
- `pre_s2_6_fork_work_runbook.md` v1.1 (corrected; supersedes v1.0)
- `stage_1_sect_runbook.md` v1.2 (corrected; supersedes v1.1)
- `git diff` against SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (canonical empirical record of post-S2.5a state)

---

## 3.6 Patch P-5 — Dataset Loader Modernization for Parquet-Backed Wikipedia Substrate

> **Numbering note:** P-5 is inserted as §3.6 — between §3.5 P-4 and §4 Pad-Token — to avoid a doc-wide section renumber, following the §3.5 precedent. The patch ID `P-5` follows the integer-incrementing patch-ID convention (P-1, P-2, P-3', P-4, P-5, …) independent of section number.

### 3.6.1 Target file

```
{MEMIT_ROOT}/rome/layer_stats.py      (one block, lines ≈ 97–103)
```

Line numbers are nominal at the SHA pin and may drift; the idempotent application script in §3.6.7 locates the replacement target by string match, not line number. The block to replace is the `load_dataset(...)` invocation that consumes `ds_name` (resolved via the existing dispatch-dict idiom).

### 3.6.2 Application condition

| Operating environment | Apply P-5? |
|---|---|
| `datasets < 3.0` (script-based loader supported) | Optional — backward-compatible if substrate-shift is acceptable |
| `datasets ≥ 3.0` (script-based loader deprecated; `RuntimeError: Dataset scripts are no longer supported`) | **Required** when `ds_name == "wikipedia"` is in the compute path |
| Stage 1 RunPod RTX 4090 + LLaMA 3.1 8B (locked manifest `datasets==4.8.3` per C-S25-6) | **Required** |

For Stage 1, **P-5 is required**.

### 3.6.3 Pattern

P-5 redirects the `wikipedia` dispatch path from the deprecated script-based `wikipedia` repository to the maintained parquet-backed `wikimedia/wikipedia` repository, and updates the config name from `20200501.en` (unavailable in the new repo) to `20231101.en` (the maintained snapshot per Wikimedia Foundation's HF dataset card).

**Original block (pre-P-5; nominal form at SHA `80426fd9…`):**

```python
raw_ds = load_dataset(
    ds_name,
    dict(wikitext="wikitext-103-raw-v1", wikipedia="20200501.en")[ds_name],
)
```

**Canonical replacement (post-P-5):**

```python
raw_ds = load_dataset(
    {"wikitext": "wikitext", "wikipedia": "wikimedia/wikipedia"}[ds_name],
    dict(wikitext="wikitext-103-raw-v1", wikipedia="20231101.en")[ds_name],
)
```

The replacement preserves the dispatch-dict idiom on both arguments: `ds_name` continues to key both the repo identifier and the config name. The `wikitext` dispatch path is functionally unchanged — `("wikitext", "wikitext-103-raw-v1")` resolves identically pre- and post-P-5. The `wikipedia` dispatch path now resolves to `("wikimedia/wikipedia", "20231101.en")`.

**Empirical-form caveat:** the original block's exact whitespace and line breaks are nominal at the SHA pin; §3.6.7's application script tolerates whitespace variations via two anchored substring substitutions rather than a multi-line block-literal substitution.

### 3.6.4 Per-substitution map

The application script in §3.6.7 performs two anchored substring substitutions:

| # | Anchor (pre-state) | Replacement (post-state) | Site |
|---|---|---|---|
| 1 | `wikipedia="20200501.en"` | `wikipedia="20231101.en"` | dispatch-dict config arg |
| 2 | `load_dataset(\n        ds_name,` | `load_dataset(\n        {"wikitext": "wikitext", "wikipedia": "wikimedia/wikipedia"}[ds_name],` | dispatch-dict repo arg |

Substitution #1 is whitespace-stable (single-line; equality test). Substitution #2 carries a multi-line anchor; the application script normalizes whitespace before comparison and reapplies the canonical line break in the replacement.

**Empirical verification of original form:** the §3.6.4 substitution anchors are nominal at SHA `80426fd9…`; byte-level confirmation is performed operator-side as part of §4.3 NV writes + mirror sync, OR as a standalone ~2-minute pod-side verification before the successor pre-S2.6 fork-work attempt. If the empirical original differs (e.g., uses an `if/elif` form rather than the dispatch-dict idiom), §3.6.4's substitution map is amended and §3.6.7's script re-derived. The substitution map above assumes the dispatch-dict form per general MEMIT codebase pattern; any deviation surfaces as a S2.5b addendum.

### 3.6.5 Rationale

HuggingFace `datasets` library deprecated repository-hosted Python loader scripts beginning at version 3.0. The legacy `wikipedia` repository on the HF Hub is implemented as `wikipedia.py` (a script-based loader); under `datasets ≥ 3.0`, `load_dataset("wikipedia", ...)` raises `RuntimeError: Dataset scripts are no longer supported, but found wikipedia.py` at module-load time. The Stage 1 dependency manifest pins `datasets==4.8.3` (per C-S25-6) — well into the post-deprecation window — making the legacy `wikipedia` repo unreachable.

The `wikimedia/wikipedia` repository, maintained by the Wikimedia Foundation directly on HF Hub, is parquet-backed and bypasses the script-loader deprecation. Row schema `{id, url, title, text}` matches the legacy `wikipedia` schema on the consumed `text` field; `TokenizedDataset` requires no adapter.

The substrate-shift from `20200501.en` to `20231101.en` is mandatory: `wikimedia/wikipedia` ships only the `20231101.<lang>` config series; earlier snapshot dates are not in this repo. Substrate-equivalence between snapshots is judgment-accepted under C-S25-15 (see §3.6.9 for the constraint cross-reference).

The `wikitext` dispatch path is unaffected by P-5: `wikitext` is a parquet-backed repo natively (via the `wikitext-103-raw-v1` config) and loads cleanly under `datasets==4.8.3`. P-5's modification of the `wikitext` arm of the dispatch dict (changing `ds_name` → literal `"wikitext"`) is a no-op functionally — the dispatch resolves to `("wikitext", "wikitext-103-raw-v1")` on both sides — but is included for symmetry with the `wikipedia` arm so the dispatch idiom remains visually consistent.

### 3.6.6 Backward-compatibility assertion

P-5 is conditional-safe rather than universal-safe (in contrast to P-4):

| Operating context | Pre-P-5 behavior | Post-P-5 behavior |
|---|---|---|
| `datasets ≥ 3.0` (Stage 1 manifest) + `ds_name == "wikipedia"` | `RuntimeError` at `datasets/load.py:1167` | PASS via parquet `wikimedia/wikipedia 20231101.en` |
| `datasets ≥ 3.0` + `ds_name == "wikitext"` | PASS (parquet native) | PASS (functionally identical dispatch result) |
| `datasets < 3.0` + `ds_name == "wikipedia"` | PASS via legacy script `wikipedia/20200501.en` (paper baseline) | PASS via parquet `wikimedia/wikipedia 20231101.en` (substrate-shifted; equivalent up to C-S25-15) |
| `datasets < 3.0` + `ds_name == "wikitext"` | PASS (legacy parquet-stable) | PASS (functionally identical dispatch result) |

P-5 is universal-safe in the engineering sense (no row resolves to a regression), but introduces a substrate-shift on the `wikipedia` dispatch path that is judgment-accepted under C-S25-15. Pre-P-5 code that ran against `datasets < 3.0` would have produced covariance statistics on the paper baseline; post-P-5 code on any `datasets` version produces statistics on the 20231101 snapshot. C-S25-15 documents this as a structural break for downstream methodology-comparison provenance.

### 3.6.7 Programmatic application (idempotent)

```python
import os

MEMIT_ROOT = "{MEMIT_ROOT}"
SHA_PIN    = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

P5_TARGET_FILE = f"{MEMIT_ROOT}/rome/layer_stats.py"

# Anchored substring substitutions (§3.6.4 substitution map)
P5_SUBSTITUTIONS = [
    # (1) Config-arg dispatch — substrate shift
    (
        'wikipedia="20200501.en"',
        'wikipedia="20231101.en"',
    ),
    # (2) Repo-arg dispatch — script-loader → parquet
    # The pre-state anchor matches the canonical form at SHA 80426fd9; if
    # operator-side empirical verification finds a different original (e.g.,
    # bare `ds_name,` on a different line, or `if/elif` form), this entry is
    # amended in §3.6.4 and re-run.
    (
        "load_dataset(\n        ds_name,",
        'load_dataset(\n        {"wikitext": "wikitext", "wikipedia": "wikimedia/wikipedia"}[ds_name],',
    ),
]

# Idempotency markers (post-state predicates)
P5_POST_MARKERS = [
    '"20231101.en"',
    '"wikimedia/wikipedia"',
]

with open(P5_TARGET_FILE) as f:
    src = f.read()

# Idempotency: skip if all post-state markers already present
fully_patched = all(m in src for m in P5_POST_MARKERS)
if fully_patched:
    print(f"P-5 already fully applied to {P5_TARGET_FILE}; skipping")
else:
    src_new = src
    applied_count = 0
    for orig, replacement in P5_SUBSTITUTIONS:
        if replacement in src_new:
            print(f"  partial-state: {orig!r} already replaced; skipping that site")
            continue
        if orig in src_new:
            src_new = src_new.replace(orig, replacement)
            applied_count += 1
        else:
            raise AssertionError(
                f"P-5 cannot apply: site for {orig!r} not found in {P5_TARGET_FILE}. "
                f"MEMIT SHA may have drifted from {SHA_PIN}, or §3.6.4 substitution "
                f"anchors require empirical reconciliation."
            )

    # Post-state verification — every marker MUST be present before write
    for marker in P5_POST_MARKERS:
        assert marker in src_new, (
            f"P-5 marker {marker!r} not present after replace in {P5_TARGET_FILE}; "
            f"file would be left in inconsistent state — aborting write"
        )

    with open(P5_TARGET_FILE, "w") as f:
        f.write(src_new)
    print(f"P-5 applied to {P5_TARGET_FILE} ({applied_count} site(s) updated)")
```

The script verifies pre-state, applies replacements only where not already present, and verifies post-state. Re-running is safe; partial-patch states are correctly detected and completed.

### 3.6.8 Verification (anchored to `pre_s2_6_fork_work_runbook.md` v1.2 Cell 2)

Runbook v1.2 Cell 2 (authored in S2.5b §4.7) codifies P-5 verification with grep-style markers, parallel to the P-4 pattern in §3.5.8. Re-stated here for canonical reference:

```python
# P-5 verification (pre_s2_6_fork_work_runbook.md v1.2 Cell 2)
P5_FILE = f"{MEMIT_ROOT}/rome/layer_stats.py"
P5_MARKERS = ['"20231101.en"', '"wikimedia/wikipedia"']
with open(P5_FILE) as f:
    src = f.read()
for marker in P5_MARKERS:
    assert marker in src, f"P-5 marker {marker!r} missing from {P5_FILE}"
```

Verification is **substring presence**, robust to whitespace variations in the surrounding code. Both markers MUST be present for P-5 to be considered applied.

### 3.6.9 Discovery provenance

P-5 was discovered during pre-S2.6 fork-work session Cell 4 Phase 1, layer 4 invocation (2026-04-30):

- **Symptom:** `RuntimeError: Dataset scripts are no longer supported, but found wikipedia.py` raised at `datasets/load.py:1167`.
- **Root cause:** `datasets==4.8.3` (locked manifest per C-S25-6) is post-deprecation for repository-hosted Python loader scripts; MEMIT's `rome/layer_stats.py:97` invokes `load_dataset("wikipedia", "20200501.en")`, which depends on the deprecated script-based loader.
- **Resolution direction empirically validated in same session:** programmatic enumeration of `wikimedia/wikipedia` configs confirmed `20231101.en` is loadable; `wikitext-103-raw-v1` also loadable. Both parquet-backed; both bypass the script-loader deprecation.
- **Session classification:** HALT-INCOMPLETE — primary deliverable (fresh covariance cache + PROVENANCE.txt at canonical NV path) not produced; OQ-PreS26-6 routed to S2.5b §4.0 for resolution.

The P-5 patch was authored in S2.5b §4.0 against the empirical evidence above. Substrate decision (S2.5b §4.0 sub-step summary §5) selected `wikimedia/wikipedia 20231101.en` over `wikitext-103-raw-v1` on closeness-to-paper-baseline + sample-volume-sufficiency grounds.

References:

- `OQ-PreS26-6` (load-bearing finding closed by this entry — ratified in S2.5b §4.5 v2.2 publication)
- `D-PreS26-4` (HALT-INCOMPLETE classification + routing to S2.5b)
- `C-S25-6` (locked dependency manifest pinning `datasets==4.8.3`)
- `C-S25-15` (substrate-shift constraint authored in S2.5b §4.0 alongside this patch)
- `pre_s2_6_fork_work_summary_block.md` §1.2 (failure-mode discovery), §2 D-PreS26-4 (routing decision), §6 (forward routing to S2.5b §4.0)
- `session_2_5b_step_4_0_summary.md` (substrate decision + P-5 §3.6 spec authoring)
- HuggingFace Hub: `wikimedia/wikipedia` dataset card (substrate availability + row schema)

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

### 4.4 Per-variant notes

The defensive code below is universal-safe across all variants — it checks `pad_token is None` before aliasing, so variants that already define `pad_token` are left as-is:

```python
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
# Otherwise leave as-is
```

Per-variant empirical state:

| Variant | `pad_token` at load | Alias required? | Empirical source |
|---|---|---|---|
| `meta-llama/Llama-3.1-8B` (base; Stage 1 production target) | `None` | **Yes** — alias required | pre-S2.6 fork-work session Cell 3 Phase B |
| `meta-llama/Llama-3.1-8B-Instruct` | Unverified — may have `pad_token` defined | Possibly not | Out-of-scope for Stage 1; tracked as a future OQ if Instruct variants enter scope |
| GPT-J 6B | `None` (inherits GPT-2 convention) | **Yes** — alias required | Session 2.2 smoke test |

After alias application, the post-load tokenizer state is:

```python
tokenizer.pad_token    == "<|end_of_text|>"  # for Llama-3.1-8B base; eos_token alias
tokenizer.pad_token_id == 128001               # for Llama-3.1-8B base; eos_token_id
```

**v2.2 correction note (closes OQ-PreS26-2):** the v2.0/v2.1 form of this section asserted "LLaMA 3.1 8B (Stage 1+ production target) has its own pad token defined" — i.e., the opposite of empirical reality. Per pre-S2.6 fork-work Cell 3 Phase B output, `meta-llama/Llama-3.1-8B` base loads with `pad_token = None` and the `tokenizer.pad_token = tokenizer.eos_token` alias is required. The defensive code (universal `if pad_token is None` guard) was always correct and unchanged across versions; the prose mischaracterized the per-variant empirical state. v2.2 corrects the prose and adds the per-variant table above. Cross-references: D-PreS26-3 / pre_s2_6_fork_work_summary_block §1.2 / OQ-PreS26-2.

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
2. P-4 (config-attribute fallback in memit/compute_z.py, rome/compute_v.py, rome/layer_stats.py)
   ↓ purge sys.modules of util.*, rome.*, memit.*  (same purge as P-1+P-2; combine if applying together)
3. P-5 (dataset loader modernization in rome/layer_stats.py — required when datasets ≥ 3.0 AND wikipedia dispatch is consumed)
   ↓ purge sys.modules of rome.* if rome was imported between P-4 and P-5
4. (P-3' if cuda:0 capacity < 18 GiB)
   ↓ purge sys.modules of memit.*, rome.*
5. Pad-Token alias (universal — alias only when tokenizer.pad_token is None per §4.4)
6. (Device-Map if multi-GPU — applied at from_pretrained, not retrofittable)
7. apply_memit_to_model(...)
   ↓ produces edited_model, orig_weights
8. Copy-Unmount (when overlay unmount is needed)
```

P-4 and P-5 both touch `rome/layer_stats.py` but at non-overlapping sites: P-4 touches lines ≈ 101 + 108 (`n_positions → max_position_embeddings`), P-5 touches lines ≈ 97–103 (`load_dataset` dispatch). They are order-independent in the technical sense; P-4 is listed before P-5 by document-discipline convention.

### 7.2 RunPod RTX 4090 sequence (Stage 1 production target — LLaMA 3.1 8B)

```
1. P-1 + P-2 (nethook)
2. P-4 (config-attribute fallback)
3. P-5 (dataset loader modernization — required under locked manifest datasets==4.8.3)
4. Pad-Token alias (universal — Llama-3.1-8B base has pad_token=None at load per §4.4)
5. .to("cuda") model load (no Device-Map needed)
6. apply_memit_to_model(...)
7. Copy-Unmount when overlay unmount is needed
```

P-3' is not required (24 GiB sufficient for LLaMA 3.1 8B FP16 + FP64 transient on cuda:0).

### 7.3 Kaggle 2× T4 sequence (smoke-test reference — GPT-J 6B; not Stage 1 target)

```
1. P-1 + P-2 (nethook)
2. P-4 (optional — backward-compatible on GPT-J; fallback to n_embd preserves Session 2.2 PASS)
3. P-5 (conditional — required if datasets ≥ 3.0 AND wikipedia dispatch is consumed; the Session 2.2 reference run pre-dates P-5 authorship and the post-3.0 datasets break)
4. P-3' (memit_main solve)
5. Pad-Token alias
6. Device-Map at from_pretrained
7. apply_memit_to_model(...)
8. Copy-Unmount when overlay unmount is needed
```

P-4 in §7.3 is listed as optional rather than required because the Kaggle Session 2.2 reference run pre-dates P-4 authorship and passed without it. Applying P-4 to a future GPT-J reference run is safe and recommended for cross-environment patch-state consistency.

P-5 in §7.3 is conditional rather than required because the Kaggle 2× T4 reference environment may carry an older `datasets` version. If `datasets ≥ 3.0` is in the Kaggle environment AND covariance compute against `wikipedia` substrate is in scope, P-5 becomes required. For any future GPT-J reference run that uses `wikitext` substrate or `datasets < 3.0`, P-5 may be omitted.

---

## 8. Manifest Requirements

The reproducibility manifest must record patch state per the following schema:

```json
{
  "patches_applied": {
    "memit_nethook_p1_signature_and_inputs_synthesis": true,
    "memit_nethook_p2_with_kwargs_registration": true,
    "memit_solve_cpu_offload_p3_prime": false,
    "memit_config_attribute_compat_p4": true,
    "memit_dataset_loader_modernization_p5": true,
    "tokenizer_pad_token_alias": true,
    "explicit_device_map": false,
    "unmount_in_place_copy_only": true
  },
  "patches_required_but_not_applied": []
}
```

The `patches_required_but_not_applied` list must be empty for any verdict to be PASS. Patches conditionally not required (e.g., P-3' on RTX 4090, Device-Map on single-GPU) are reported as `false` in `patches_applied` and are NOT listed in `patches_required_but_not_applied`.

P-4 is reported as `true` whenever the patch markers are present in the MEMIT repo, regardless of whether the base model strictly requires it (any GPT-J reference run after Session 2.5a may carry P-4 as backward-compatible — record it as `true` in that case).

**P-5 reporting (v2.2):** P-5 is reported as `true` when both post-state markers (`"20231101.en"` AND `"wikimedia/wikipedia"`) are present in `rome/layer_stats.py`. P-5 is reported as `false` when neither marker is present (pre-P-5 state). A partial-marker state — exactly one of the two markers present — is anomalous and indicates an interrupted application or a manual edit that should be reconciled before any covariance compute proceeds. Cross-reference: C-S25-15 (substrate-shift constraint).

The manifest key `memit_config_attribute_compat_p4` is canonical. Earlier session artifacts (e.g., `stage_1_patch_state.json` produced by `stage_1_sect_runbook.md` v1.1 Cell 2) use the parallel key `P-4_config_attribute_fallback` for in-memory dataclass form; both refer to the same patch state. Future runbook updates may consolidate to a single key.

---

## 9. Upstream Submission Notes

`kmeng01/memit` is unmaintained (last commit 2022-11-14; 16 open issues; no triage). Patches P-1, P-2, P-3', P-4, and P-5 are reported but not submitted upstream — submission would not be merged. The framework's POC must fork the repository and pin to a known-patched fork rather than upstream `kmeng01/memit`. Forking work is deferred to Workstream 1 future tasks (per OQ-S22-17).

P-4 is a particularly clean submission candidate (universal-safe, backward-compatible, addresses a now-unavoidable issue for any post-2022 base model) and would benefit downstream MEMIT users were the upstream repo maintained. The patch is documented here in canonical form to support a future maintained-fork or alternative-upstream submission.

P-5 addresses an even more time-sensitive deprecation: HuggingFace `datasets` library deprecated repository-hosted Python loader scripts at version 3.0, structurally breaking MEMIT's `wikipedia` dispatch path for any post-2024 environment. P-5 is similarly clean (preserves the dispatch-dict idiom, conditional-safe, single file) and would benefit downstream MEMIT users immediately. The substrate-shift dimension (`20200501.en` → `20231101.en`) is documented in C-S25-15 and would also need to be carried into any upstream submission as a methodology note.

---

*End of MEMIT Patches Canonical Specification v2.2.1.*
