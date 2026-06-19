# MEMIT Patches — Canonical Specification

> **Source:** Session 2.2 smoke test PASS verdict (2026-04-26); P-4 added per Session 2.5a smoke test PASS verdict (2026-04-29) and ratified in Session 2.5b §4.5 (D-S25-11, C-S25-9, IC-S25-2); v2.1 corrections per Session 2.5b §4.5b (C-S25-13 path correction; C-S25-14 dual canonical-form ratification — surfaced by pre-S2.6 fork-work runbook Cell 2 empirical verification); v2.2 expansions per Session 2.5b §4.5 (§3.5.4 line table correction + §3.5.7 application script correction closing OQ-PreS26-1; §4.4 Pad-Token note correction closing OQ-PreS26-2; §3.6 P-5 entry authored from §4.0 closing OQ-PreS26-6; new constraint C-S25-15 substrate-shift); v2.2.1 footer-version-addition patch per Session 2.5b §4.3 execution (closes OQ-S25b-5 — document footer carried no version marker; surgical str_replace edit to add `v2.2.1.` to footer; no semantic change to canonical doc content); v2.3 expansion per pre-Session-2.6 hardening session (2026-05-01) — §3.7 P-6 spec authored from D-PreS26-4 in pre_s2_6_fork_work_summary_block.md v2 closing OQ-PreS26-25; §1 inventory + §7 application order + §8 manifest schema + §9 upstream notes updated to reflect P-6 addition; v2.4 expansion per Session 2.7 P-7 authoring + post-S2.6 remediation (2026-05-01) — §3.8 P-7 spec authored from IC-S26-1 draft in session_2_6_summary_block.md v1 closing OQ-S26-16 + OQ-S26-18; D-S27-1/2/3 resolve the three IC-S26-1 open design questions; §1 inventory + §7 application order + §8 manifest schema + §9 upstream notes updated to reflect P-7 addition; new §10 Process Constraints section ratifies C-S26-1 (batch_tokens=100 mandatory for LLaMA-family on RTX 4090), C-S26-2 (cache-dispatch path explicit batch_tokens propagation — closed by P-7 by construction), and C-S26-3 (runbook hardening passes require dry-run gate); v2.4.1 amendment per Session 2.8 §3.8.9 empirical NV record (P-7 EMPIRICALLY-CONFIRMED at S2.8 Cell 9 9/9 cache-dispatch PASS — recorded operator-side per session_2_8_summary_block.md §3.1); v2.5 expansion per Session 2.9 (2026-05-01) — new §10.4 Process Constraints subsection codifies C-S28-1 (defense-in-depth marker post-application verification — empirical motivation: OQ-S28-3 closed at S2.9 v1.4 hardening pass via deletion of v1.3 line 552 marker; ratification authority: D-S29-5 per session_2_9_summary_block.md §2.5); v2.5 bump is additive — no existing-content edits to §1–§9
> **Version:** 2.5 (supersedes v2.4.1 — adds §10.4 C-S28-1 codification at Process Constraints; v2.4.1 inherits §3.8.9 empirical NV record per S2.8; no changes to §1–§9)
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
| P-6 | `rome/layer_stats.py:40` f-string prefix correction for `size_suffix` filename construction | Conditional (required when `batch_tokens < npos`; no-op when `batch_tokens ≥ npos`) | **Yes** |
| P-7 | `memit/memit_main.py` `get_cov` body — `batch_tokens` propagation to `layer_stats` (architectural-threshold-gated) | Universal-safe (architectural threshold `npos > 8192`; no-op on GPT-J family) | **Yes** |
| Pad-Token | Tokenizer attribute | Universal (any base model with `pad_token = None`; LLaMA-conditional per §4.4) | Yes (LLaMA-conditional) |
| Device-Map | Cell 4 / model load | Conditional (multi-GPU only) | **No** |
| Copy-Unmount | Write engine unmount step | Universal (.vindex architecture requirement) | Yes |

For RunPod RTX 4090 single-GPU configuration with LLaMA 3.1 8B as the Stage 1 target, **eight patches are required**: P-1, P-2, **P-4**, **P-5**, **P-6**, **P-7**, Pad-Token, Copy-Unmount. P-3' and Device-Map are not required.

For Kaggle 2× T4 with GPT-J 6B (Session 2.2 smoke-test reference), **nine patches are applicable**: P-1, P-2, P-3', P-4 (optional but safe — backward-compatible), P-5 (conditional — required if `datasets ≥ 3.0` and `wikipedia` dispatch path is consumed), P-6 (conditional — required when `batch_tokens < npos`; GPT-J `npos=2048` and Stage 1 `batch_tokens=100` satisfies the condition), P-7 (universal-safe — no-op on GPT-J via architectural-threshold dispatch; preserves Block 2 reference cache filename form), Pad-Token, Device-Map, Copy-Unmount.

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

## 3.7 Patch P-6 — `rome/layer_stats.py:40` f-string Prefix Correction for `size_suffix` Construction

> **Numbering note:** P-6 is inserted as §3.7 — between §3.6 P-5 and §4 Pad-Token — to avoid a doc-wide section renumber, following the §3.5 / §3.6 precedent. The patch ID `P-6` follows the integer-incrementing patch-ID convention (P-1, P-2, P-3', P-4, P-5, P-6, …) independent of section number.

### 3.7.1 Target file

```
{MEMIT_ROOT}/rome/layer_stats.py      (one line, line ≈ 40)
```

Line number is nominal at the SHA pin and may drift; the idempotent application script in §3.7.7 locates the replacement target by string match, not line number. The line to replace constructs `size_suffix` inside the `batch_tokens < npos` branch — the branch executed when per-token covariance accumulation operates with a token budget below the model's positional context window.

### 3.7.2 Application condition

| Operating environment | Apply P-6? |
|---|---|
| `batch_tokens >= npos` (full-window dispatch; size_suffix line 40 not executed) | Optional — branch bypass; patch is no-op |
| `batch_tokens < npos` (any tractable Stage 1 dispatch) | **Required** — pre-P-6 emits literal `"{batch_tokens}"` placeholder into the cache filename |
| Stage 1 RunPod RTX 4090 + LLaMA 3.1 8B (`npos=131072`; `batch_tokens=100` per D-PreS26-6) | **Required** |
| Kaggle 2× T4 + GPT-J 6B (`npos=2048`) | **Required** when covariance compute is in scope and `batch_tokens < 2048` (typical Stage 1 dispatch satisfies this) |

For Stage 1, **P-6 is required**. Llama-3.1-8B's `npos=131072` makes full-window per-token covariance accumulation compute-prohibitive on RTX 4090 (24 GiB VRAM); `batch_tokens < npos` is the only tractable dispatch envelope, so the conditional branch is structural in practice.

### 3.7.3 Pattern

P-6 inserts the missing `f` prefix on the `size_suffix` literal at `rome/layer_stats.py:40`. The pre-P-6 form is a plain-string literal containing the four-character substring `{batch_tokens}` as literal text — the surrounding code has no subsequent `.format(...)` call or `%`-style interpolation, so the variable named `batch_tokens` (in scope at line 40 as a function parameter) is never substituted. The post-P-6 form activates Python f-string interpolation at literal-construction time.

**Original line (pre-P-6; nominal form at SHA `80426fd9…`):**

```python
size_suffix = "_t{batch_tokens}" + size_suffix
```

**Canonical replacement (post-P-6):**

```python
size_suffix = f"_t{batch_tokens}" + size_suffix
```

The replacement is a single-character insertion — the `f` prefix on the leading string literal. All other tokens are byte-identical: same opening quote, same brace-delimited variable name, same closing quote, same concatenation operator, same right-hand operand. The substitution is whitespace-stable and indentation-agnostic.

### 3.7.4 Per-substitution map

The application script in §3.7.7 performs one anchored substring substitution:

| # | Anchor (pre-state) | Replacement (post-state) | Site |
|---|---|---|---|
| 1 | `size_suffix = "_t{batch_tokens}" + size_suffix` | `size_suffix = f"_t{batch_tokens}" + size_suffix` | f-string prefix correction at line ≈ 40 |

The substitution is a single-line, full-line equality test. No multi-line anchor; no whitespace normalization required. The post-state form contains the substring `f"_t{batch_tokens}"` which is uniquely identifying — pre-P-6 layer_stats.py contains no other occurrence of an f-string literal opening with `_t{`.

### 3.7.5 Rationale

MEMIT's `rome/layer_stats.py` constructs the cache filename via `size_suffix` concatenation (line 40 in the `batch_tokens < npos` branch; the alternate branch produces a flat `_{sample_size}` form). The pre-P-6 form is unambiguously a Python authoring bug: a string literal of the form `"_t{batch_tokens}"` without an `f` prefix and without a downstream `.format(...)` call carries the substring `{batch_tokens}` as literal text into the filename. With `batch_tokens=100`, the resulting filename component is `_t{batch_tokens}_` rather than the intended `_t100_`.

This propagates downstream as the literal placeholder appearing in the cache filename:

```
model.layers.4.mlp.down_proj_float32_mom2_t{batch_tokens}_100000.npz   (pre-P-6, BUG)
model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz              (post-P-6, canonical)
```

In post-P-6 form, the `f` prefix activates Python f-string interpolation; with `batch_tokens=100`, `size_suffix` becomes `_t100_100000` (concatenated with the existing `_{sample_size}` suffix from line 41-ish), producing the canonical filename.

The fix is idiomatic — f-string prefix is the standard Python 3.6+ idiom for inline variable interpolation (PEP 498). Any consumer that parses the cache filename for the `_t{n}_` segment (file-set predicate, version manifest, debugging tooling, IC-PreS26-2 contract) breaks under the literal-placeholder form.

### 3.7.6 Backward-compatibility assertion

P-6 is universal-safe (in contrast to P-5, which carries a substrate-shift dimension):

| Operating context | Pre-P-6 behavior | Post-P-6 behavior |
|---|---|---|
| `batch_tokens < npos` (any Stage 1 / tractable dispatch) | Cache filename contains literal `_t{batch_tokens}_` placeholder; downstream consumers fail file-set predicate | Cache filename contains substituted `_t<value>_` (e.g., `_t100_`); canonical form per IC-PreS26-2 |
| `batch_tokens >= npos` (full-window dispatch) | size_suffix line 40 not executed (alternate branch); filename `_<sample_size>` only | size_suffix line 40 not executed; identical behavior |
| Any consumer that does substring-match on `_t<integer>_` | Fails — substring not present in pre-P-6 output | PASS |
| Any consumer that does substring-match on the literal placeholder `_t{batch_tokens}_` | PASS — matches the bug | Fails — substring no longer present (intentional) |

P-6 introduces no regression in the sense that no canonical downstream consumer in the framework expects the literal-placeholder form. The pre-P-6 output is a bug; no production tooling consumes it. Universal-safe across all base models, all `batch_tokens` values where `batch_tokens < npos`, and all environments.

### 3.7.7 Programmatic application (idempotent)

```python
import os

MEMIT_ROOT = "{MEMIT_ROOT}"
SHA_PIN    = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

P6_TARGET_FILE = f"{MEMIT_ROOT}/rome/layer_stats.py"

# Anchored substring substitution (§3.7.4 substitution map)
P6_SUBSTITUTIONS = [
    # (1) f-string prefix correction at line ≈ 40
    (
        'size_suffix = "_t{batch_tokens}" + size_suffix',
        'size_suffix = f"_t{batch_tokens}" + size_suffix',
    ),
]

# Idempotency markers (post-state predicates)
P6_POST_MARKERS = [
    'size_suffix = f"_t{batch_tokens}" + size_suffix',
]

with open(P6_TARGET_FILE) as f:
    src = f.read()

# Idempotency: skip if all post-state markers already present
fully_patched = all(m in src for m in P6_POST_MARKERS)
if fully_patched:
    print(f"P-6 already fully applied to {P6_TARGET_FILE}; skipping")
else:
    src_new = src
    applied_count = 0
    for orig, replacement in P6_SUBSTITUTIONS:
        if replacement in src_new:
            print(f"  partial-state: {orig!r} already replaced; skipping that site")
            continue
        if orig in src_new:
            src_new = src_new.replace(orig, replacement)
            applied_count += 1
        else:
            raise AssertionError(
                f"P-6 cannot apply: site for {orig!r} not found in {P6_TARGET_FILE}. "
                f"MEMIT SHA may have drifted from {SHA_PIN}, or §3.7.4 substitution "
                f"anchor requires empirical reconciliation."
            )

    # Post-state verification — every marker MUST be present before write
    for marker in P6_POST_MARKERS:
        assert marker in src_new, (
            f"P-6 marker {marker!r} not present after replace in {P6_TARGET_FILE}; "
            f"file would be left in inconsistent state — aborting write"
        )

    with open(P6_TARGET_FILE, "w") as f:
        f.write(src_new)
    print(f"P-6 applied to {P6_TARGET_FILE} ({applied_count} site(s) updated)")
```

The script verifies pre-state, applies the replacement only when the post-state marker is not already present, and verifies post-state. Re-running is safe; partial-patch states do not exist for a single-substitution patch (the post-marker uniquely identifies completion).

### 3.7.8 Verification (anchored to runbook Cell 2 patch state verification)

P-6 verification follows the grep-style marker pattern established for P-4 (§3.5.8) and P-5 (§3.6.8). Both `pre_s2_6_fork_work_runbook.md` v1.2.2+ Cell 2 and `stage_1_sect_runbook.md` v1.2+ Cell 2 carry the canonical verification form when patch state is interrogated:

```python
# P-6 verification (canonical form for any Cell 2 patch-state check)
P6_FILE = f"{MEMIT_ROOT}/rome/layer_stats.py"
P6_MARKERS = ['size_suffix = f"_t{batch_tokens}" + size_suffix']
with open(P6_FILE) as f:
    src = f.read()
for marker in P6_MARKERS:
    assert marker in src, f"P-6 marker {marker!r} missing from {P6_FILE}"
```

Verification is **substring presence** of the post-state full line. The marker is whitespace-stable on the assumption that the canonical replacement form preserves the exact pre-state spacing (single-space around `=` and `+`); any operator-side pretty-printer that reformats the file invalidates this marker and requires re-derivation.

For runtime correctness verification (distinct from source-byte verification), the empirical signature is the cache filename produced by a layer_stats invocation: post-P-6 filenames contain `_t<integer>_` (e.g., `_t100_`); pre-P-6 filenames contain the literal substring `_t{batch_tokens}_`. The IC-PreS26-2 file-set predicate (consumed by `stage_1_sect_runbook.md` v1.2 Cell 3) is the canonical runtime gate.

### 3.7.9 Discovery provenance and empirical NV record

P-6 was discovered, authored, and NV-applied within the pre-S2.6 fork-work re-attempt session (2026-05-01). Single-session lifecycle — no inter-session ratification gap, no S2.5b-style replacement-form drift. Discovery context:

- **Symptom:** Cell 4 Phase 1 dispatch (5 layers × ~14–20 min/layer) produced cache files at the canonical NV path with filenames containing the literal substring `_t{batch_tokens}_` rather than the substituted form `_t100_`. Cell 5 Phase B file-set predicate hard-halted on file-set mismatch against the post-P-6 expected pattern.
- **Diagnostic:** source-side inspection of `rome/layer_stats.py:40` revealed missing `f` prefix on the `size_suffix` construction. The variable `batch_tokens` is in scope at line 40 (function parameter); the omission is unambiguously a Python authoring bug. Earlier hypothesis (H4 in pre-S2.6 fork-work session — root cause is hparams JSON `batch_tokens` field absence) was refuted by source diagnostic; OQ-PreS26-22 and OQ-PreS26-28 close on the corrected root cause.
- **Resolution:** insert single-character `f` prefix on line 40; idempotent via post-state-marker check; NV-applied this session via direct write to `/workspace/memit_dry_run/memit/rome/layer_stats.py`; markers verified via re-import of `rome.layer_stats` and direct substring probe of the file bytes.
- **Empirical anchor:** Cell 5 Phase B PASS verdict at 2026-05-01T06:06:17Z — five .npz files at canonical NV path with canonical post-P-6 filenames (each carrying the `_t100_` segment), each verified to carry `mom2.mom2` shape `(14336, 14336)` float32 and `sample_size=100000`. PROVENANCE.txt authored at the same path is the authoritative provenance manifest (per D-PreS26-8).

The empirical NV record is forward-compatible: any successor session that NV-restores from `/workspace/memit_dry_run/` inherits P-6 application; markers persist across pod stop/start. The reproducibility manifest's `memit_layer_stats_fstring_p6` field (v2.3 schema addition; see §8) is reported as `true` whenever the post-state marker is present.

References:

- `D-PreS26-4` (load-bearing source of truth for this spec entry; pre_s2_6_fork_work_summary_block.md v2 §2)
- `IC-PreS26-2` (post-P-6 cache filename interface contract; consumed by `stage_1_sect_runbook.md` v1.2 Cell 3 R1.1 file-set predicate)
- `C-PreS26-5` (P-6 application precondition for any layer_stats invocation satisfying `batch_tokens < npos`)
- `OQ-PreS26-22` and `OQ-PreS26-28` (closed by D-PreS26-4 + D-PreS26-6; hparams-field hypothesis refuted by source diagnostic)
- `OQ-PreS26-25` (closed by this canonical entry)
- `pre_s2_6_fork_work_summary_block.md` v2 §2 (D-PreS26-4 source), §6 PATCHES APPLIED (P-6 NEW THIS SESSION inventory)
- `/workspace/memit_dry_run/memit/rome/layer_stats.py` (NV-resident; markers verified Cell 2 + Cell 4 re-import per summary block)
- `/workspace/architecture_profile/pre_s2_6_patch_state.json` (Cell 2 patch verification record)

---

## 3.8 Patch P-7 — `memit/memit_main.py` `get_cov` body — `batch_tokens` propagation to `layer_stats`

> **Numbering note:** P-7 is inserted as §3.8 — between §3.7 P-6 and §4 Pad-Token — to avoid a doc-wide section renumber, following the §3.5 / §3.6 / §3.7 precedent. The patch ID `P-7` follows the integer-incrementing patch-ID convention (P-1, P-2, P-3', P-4, P-5, P-6, P-7, …) independent of section number.

### 3.8.1 Target file

```
{MEMIT_ROOT}/memit/memit_main.py      (one block inside the body of get_cov; nominal lines ≈ 175–195)
```

Line numbers are nominal at the SHA pin and may drift; the idempotent application script in §3.8.7 locates the replacement target by anchored substring match against the `layer_stats(...)` call inside `get_cov`'s body, not by line number. The substitution adds two lines of architectural-threshold dispatch logic before the `layer_stats` call and adds a single `batch_tokens=` kwarg to the call's argument list.

P-7 is structurally distinct from P-3' (the only other `memit_main.py`-targeted patch in this document): P-3' modifies the `execute_memit` body (lines ≈ 195–199 — the `torch.linalg.solve` block); P-7 modifies the `get_cov` body (lines ≈ 175–195 — the `layer_stats` call site). The two patches are non-overlapping and order-independent.

### 3.8.2 Application condition

| Operating environment | Apply P-7? |
|---|---|
| Any environment, any base model | **Required** — P-7 is universal-safe (architectural-threshold dispatch makes the patch a runtime no-op on `npos ≤ 8192` base models) |
| Stage 1 RunPod RTX 4090 + LLaMA 3.1 8B (`npos=131072`) | **Required** — load-bearing for cache-dispatch symmetry per C-S26-2; pre-P-7 cache-dispatch path OOMs at `causal_mask.clone()` 22.81 GiB allocation request |
| Kaggle 2× T4 + GPT-J 6B (`npos=2048`) | **Required** — universal-safe; runtime no-op (architectural threshold `npos > 8192` is not crossed; `mom2_batch_tokens` resolves to `None`; `layer_stats` runs default branch; cache filename form unchanged from pre-P-7) |
| Any future LLaMA-family target (npos ≥ 8192) | **Required** — load-bearing per C-S26-1 |
| Any future short-context target (npos ≤ 8192) on tractable VRAM | **Required** as universal-safe; runtime no-op |

For Stage 1, **P-7 is required**. Without P-7, MEMIT's edit-time `get_cov` → `layer_stats` chain on Llama-3.1-8B constructs cache-lookup filenames lacking the `_t100_` segment that the canonical pre-S2.6 fork-work cache files carry (per IC-PreS26-2). The lookup misses; `layer_stats` falls back to local compute; the local compute attempts to allocate `causal_mask` at `npos=131072` (~22.81 GiB at fp16 / ~45.6 GiB at fp32), which exceeds RTX 4090 24 GiB VRAM. Resolution: P-7 makes the edit-time dispatch path explicitly propagate `batch_tokens=100` (mirroring the cache-compute path's discipline), making the cache structurally visible.

### 3.8.3 Pattern

P-7 inserts an architectural-threshold dispatch line + adds a kwarg pass. Inside `get_cov`'s body, immediately before the `layer_stats(...)` call, P-7 introduces:

```python
mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None
```

and modifies the existing `layer_stats(...)` call to forward this value:

```python
stat = layer_stats(
    ...,
    batch_tokens=mom2_batch_tokens,  # P-7 — per C-S26-1; threshold-gated for GPT-J safety
    ...,
)
```

The threshold value `8192` is the architectural anchor per C-S26-1 — see §3.8.5 rationale and §3.8.6 backward-compatibility for derivation. The literal `100` is the canonical Stage 1 batch_tokens budget per D-PreS26-6.

**Original block (pre-P-7; nominal form at SHA `80426fd9…`):**

```python
        stat = layer_stats(
            model,
            tok,
            layer_name,
            STATS_DIR,
            mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            hparams=hparams,
            force_recompute=force_recompute,
        )
```

**Canonical replacement (post-P-7):**

```python
        # P-7 — architectural-threshold dispatch for cache-compute and edit-time symmetry
        # per C-S26-1 (LLaMA-family npos > 8192 requires batch_tokens truncation) and
        # C-S26-2 (cache-dispatch path explicit batch_tokens propagation). Threshold
        # 8192 derived in memit-patches-canonical.md v2.4 §3.8.6 (causal_mask VRAM
        # envelope on 24 GiB GPU). On GPT-J family (npos=2048), mom2_batch_tokens
        # resolves to None; layer_stats runs default branch; cache filename form
        # unchanged from pre-P-7 — universal-safe.
        mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None
        stat = layer_stats(
            model,
            tok,
            layer_name,
            STATS_DIR,
            mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            batch_tokens=mom2_batch_tokens,
            hparams=hparams,
            force_recompute=force_recompute,
        )
```

The replacement preserves all pre-P-7 args and arg order; it inserts one new line of dispatch logic before the call and one new kwarg into the call. The kwarg `batch_tokens=mom2_batch_tokens` is positioned immediately before `hparams=` to maintain a stable ordering convention against any future MEMIT signature changes (`hparams` and `force_recompute` are the conventional trailing kwargs in `layer_stats` invocations across the MEMIT codebase).

The exact arg list inside the existing `layer_stats(...)` call may exhibit minor variation across MEMIT SHA pins (e.g., presence/absence of `hparams=hparams`, presence/absence of `progress=` or `download=` kwargs). The §3.8.7 application script verifies a verbatim match against the SHA pin's `get_cov` body and halts with a diagnostic message if drift is detected, requiring empirical reconciliation.

### 3.8.4 Per-substitution map

The application script in §3.8.7 performs one anchored multi-line block substitution:

| # | Anchor (pre-state) | Replacement (post-state) | Site |
|---|---|---|---|
| 1 | `stat = layer_stats(` ... `force_recompute=force_recompute,` ... `)` block (verbatim per §3.8.3 pre-state) | `# P-7 — architectural-threshold dispatch...` + `mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None` + revised `stat = layer_stats(...)` block with `batch_tokens=mom2_batch_tokens,` kwarg added | `get_cov` body — `layer_stats` call site (nominal lines ≈ 175–195) |

The post-state contains the substring `mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None` which is uniquely identifying — the token sequence `mom2_batch_tokens` does not appear anywhere else in MEMIT source at SHA pin `80426fd9...`. This substring is the canonical idempotency marker.

### 3.8.5 Rationale (with C-S26-1 + C-S26-2 ratification)

MEMIT's `get_cov` function (defined in `memit/memit_main.py`) is the cache-management wrapper around `rome/layer_stats.py:layer_stats(...)`. Its responsibility is twofold: (1) at cache-compute time, invoke `layer_stats` to compute and persist the second-moment matrix `mom2` for a target MLP layer; (2) at edit-time, invoke `layer_stats` again — which performs a cache lookup against a filename derived from its kwargs — to load the previously-computed `mom2` from cache rather than recompute.

The pre-P-7 form passes a different kwarg set at edit-time than was used at cache-compute time. Specifically:

- **Cache-compute time (pre-S2.6 fork-work, 2026-04-30):** the cache was produced with `batch_tokens=100` explicitly propagated to `layer_stats`. Per IC-PreS26-2, the resulting cache filenames at NV carry the `_t100_` segment (e.g., `model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz`).
- **Edit-time (S2.6 Cell 9 Trial 0 attempt, 2026-05-01):** the canonical `get_cov` → `layer_stats` chain in `memit_main.py` does NOT propagate `batch_tokens`. The lookup filename is constructed without the `_t<n>_` segment (the alternate branch at `rome/layer_stats.py:40` — distinct from the post-P-6 `batch_tokens < npos` branch). The cache-resident files at NV become structurally invisible to the lookup. `layer_stats` falls back to local compute, which on Llama-3.1-8B (npos=131072) attempts to allocate `causal_mask` at full window — ~22.81 GiB at fp16 — exceeding RTX 4090 24 GiB VRAM after model is resident.

The empirical surface at S2.6 Cell 9 Trial 0:
```
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 22.81 GiB.
GPU 0 has a total capacity of 23.65 GiB of which 12.35 GiB is free.
```
The OOM is the symptom; the root cause is the cache-dispatch filename mismatch (per S2.6 §FORENSIC SNAPSHOT INVENTORY, file `s26_halt_filename_evidence.txt` documents the mismatch directly).

P-7 resolves this by ensuring the edit-time dispatch propagates the same `batch_tokens` value that cache-compute used. The architectural-threshold form (`100 if npos > 8192 else None`) makes the propagation universal — the same source code produces correct behavior on any base model — without operator-side conditional logic. The threshold `8192` is derived in §3.8.6.

This rationale ratifies two constraints from S2.6:

> **C-S26-1 (ratified at S2.7 — load-bearing for P-7).** `batch_tokens=100` is operationally mandatory for Llama-3.1-8B (`npos=131072`) on RTX 4090 24 GiB during MEMIT covariance compute OR fallback-compute paths. The causal mask shape at full npos is `(1, 1, 131072, 131072)` = ~32 GiB at fp16 / ~64 GiB at fp32 — unallocatable on 24 GiB GPU even with model unloaded. The truncation is not a performance optimization but a tractability requirement. Generalization: any LLaMA-family or modern long-context base model with `max_position_embeddings > 8192` requires `batch_tokens` truncation in BOTH cache compute AND edit-time dispatch on commodity 24 GiB-class GPUs.

> **C-S26-2 (ratified at S2.7 — closed by P-7 by construction).** The cache-dispatch path must explicitly propagate `batch_tokens` to maintain filename symmetry with the cache-compute path. P-6 (§3.7) fixed the literal-vs-substituted form problem when `batch_tokens` IS passed; P-7 fixes the passed-vs-unpassed asymmetry between cache-compute and edit-time dispatch. P-6 and P-7 are jointly required for cache filename round-trip correctness on `batch_tokens < npos` regimes; either patch alone is insufficient.

### 3.8.6 Backward-compatibility assertion

P-7 is universal-safe via architectural-threshold runtime dispatch — a structurally cleaner backward-compatibility mechanism than P-5's substrate-shift-with-methodology-note (C-S25-15). The threshold value `8192` is derived from the causal_mask VRAM envelope:

| Base model | `npos` | Causal mask at fp16 | Causal mask at fp32 | Tractability on RTX 4090 24 GiB |
|---|---|---|---|---|
| GPT-2 small | 1024 | 2 MiB | 4 MiB | Tractable |
| GPT-J 6B | 2048 | 8 MiB | 16 MiB | Tractable |
| GPT-NeoX 20B | 2048 | 8 MiB | 16 MiB | Tractable |
| LLaMA-2 7B | 4096 | 32 MiB | 64 MiB | Tractable |
| Threshold cutoff | **8192** | **128 MiB** | **256 MiB** | **Tractable (margin)** |
| LLaMA-2 chat (extended) | 16384 | 512 MiB | 1 GiB | Marginal |
| Mistral 7B (sliding-window 4096; npos config 32768) | 32768 | 2 GiB | 4 GiB | Marginal at fp32 |
| LLaMA-3 8B base | 8192 | 128 MiB | 256 MiB | Tractable (boundary) |
| LLaMA-3.1 8B | 131072 | 32 GiB | 64 GiB | **Unallocatable** |

The threshold `8192` sits at the upper edge of the tractable envelope. Any model with `npos > 8192` may exceed VRAM headroom under default full-window dispatch; any model with `npos ≤ 8192` is safe. The strict-greater-than (`>`) test means LLaMA-3 8B base (`npos=8192` exactly) hits `mom2_batch_tokens=None` — preserving paper-baseline reproducibility for that specific model — while LLaMA-3.1+ 8B (`npos=131072`) triggers the truncation.

Operating-context behavior matrix:

| Base model | `max_position_embeddings` | `mom2_batch_tokens` | `layer_stats` branch (per §3.7 P-6) | Cache filename form |
|---|---|---|---|---|
| GPT-2 (any size) | 1024 | `None` | Default branch (line ≠ 40) | `..._<sample_size>.npz` |
| GPT-J 6B | 2048 | `None` | Default branch | `..._<sample_size>.npz` |
| LLaMA-2 7B | 4096 | `None` | Default branch | `..._<sample_size>.npz` |
| LLaMA-3 8B (base) | 8192 | `None` | Default branch | `..._<sample_size>.npz` |
| LLaMA-3.1 8B | 131072 | `100` | `batch_tokens < npos` branch (line 40, post-P-6) | `..._t100_<sample_size>.npz` |
| Mistral 7B (npos config) | 32768 | `100` | `batch_tokens < npos` branch | `..._t100_<sample_size>.npz` |

P-7 introduces zero substrate-shift on any sub-threshold base model. Block 2 reference cache (Session 2.2 / Kaggle 2× T4 / GPT-J 6B; `npos=2048`) was produced under default `batch_tokens=npos` (no `_t<n>_` segment in filename). Post-P-7, GPT-J reference runs resolve to `mom2_batch_tokens=None`, `layer_stats` runs the default branch, generates filenames without the `_t<n>_` segment, and existing reference cache remains valid byte-for-byte. No methodology note required for cross-environment cache reuse.

The strict-greater-than (`>`) form rather than `≥ 8192` is deliberate: LLaMA-3 8B base, with `npos=8192` exactly, would trip a `≥` test. Reserving the threshold for `> 8192` preserves a paper-faithful path for that one base model class while still capturing every long-context model that requires truncation in practice.

| Operating context | Pre-P-7 behavior | Post-P-7 behavior |
|---|---|---|
| `npos > 8192` cache-compute path (operator-explicit `batch_tokens=100` propagation) | Cache file written with `_t100_` segment | Identical — operator-side propagation already covered this path |
| `npos > 8192` edit-time path | Lookup filename without `_t<n>_` segment; cache miss; fallback to local compute; OOM at causal_mask | Lookup filename with `_t100_` segment; cache hit; no compute, no OOM |
| `npos ≤ 8192` cache-compute path | Cache file written without `_t<n>_` segment (default branch) | Identical — `mom2_batch_tokens=None` preserves default branch |
| `npos ≤ 8192` edit-time path | Lookup filename without `_t<n>_` segment; cache hit | Identical — same default branch, same lookup form |

P-7 introduces no regression in the sense that no canonical downstream consumer in the framework expects the pre-P-7 edit-time behavior on `npos > 8192` (the pre-P-7 behavior is the C-S26-2 defect). Universal-safe across all base models, all `npos` values, and all environments.

### 3.8.7 Programmatic application (idempotent)

```python
import os, sys

MEMIT_ROOT = "{MEMIT_ROOT}"
SHA_PIN    = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

P7_TARGET_FILE = f"{MEMIT_ROOT}/memit/memit_main.py"

# Anchored block substitution (§3.8.4 substitution map)
# The pre-state ORIG_BLOCK is the canonical layer_stats(...) call inside get_cov
# at SHA pin 80426fd9... If SHA drift has produced a different verbatim arg list,
# the pre-state assertion below fires with a diagnostic; reconcile against §3.8.3
# before re-running the script.

P7_ORIG_BLOCK = """        stat = layer_stats(
            model,
            tok,
            layer_name,
            STATS_DIR,
            mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            hparams=hparams,
            force_recompute=force_recompute,
        )"""

P7_PATCHED_BLOCK = """        # P-7 — architectural-threshold dispatch for cache-compute and edit-time symmetry
        # per C-S26-1 (LLaMA-family npos > 8192 requires batch_tokens truncation) and
        # C-S26-2 (cache-dispatch path explicit batch_tokens propagation). Threshold
        # 8192 derived in memit-patches-canonical.md v2.4 §3.8.6 (causal_mask VRAM
        # envelope on 24 GiB GPU). On GPT-J family (npos=2048), mom2_batch_tokens
        # resolves to None; layer_stats runs default branch; cache filename form
        # unchanged from pre-P-7 — universal-safe.
        mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None
        stat = layer_stats(
            model,
            tok,
            layer_name,
            STATS_DIR,
            mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            batch_tokens=mom2_batch_tokens,
            hparams=hparams,
            force_recompute=force_recompute,
        )"""

# Idempotency markers (post-state predicates)
P7_POST_MARKERS = [
    "mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None",
    "batch_tokens=mom2_batch_tokens,",
]

with open(P7_TARGET_FILE) as f:
    src = f.read()

# Idempotency: skip if all post-state markers already present
fully_patched = all(m in src for m in P7_POST_MARKERS)
if fully_patched:
    print(f"P-7 already fully applied to {P7_TARGET_FILE}; skipping")
else:
    # Pre-state assertion — verbatim match against canonical SHA pin form
    if P7_PATCHED_BLOCK in src:
        # Partial-state: post-block already present. This is anomalous if not all
        # post-markers present (caught above) — re-check markers explicitly.
        partial_markers = [m for m in P7_POST_MARKERS if m not in src]
        raise AssertionError(
            f"P-7 partial-state detected: P7_PATCHED_BLOCK substring present in "
            f"{P7_TARGET_FILE} but post-markers {partial_markers!r} absent. "
            f"File is in inconsistent state — manual reconciliation required "
            f"against §3.8.3 / §3.8.4."
        )
    if P7_ORIG_BLOCK not in src:
        raise AssertionError(
            f"P-7 cannot apply: ORIG_BLOCK not found in {P7_TARGET_FILE}. "
            f"MEMIT SHA may have drifted from {SHA_PIN}, or the get_cov body "
            f"layer_stats(...) call signature in this MEMIT vintage differs from "
            f"the canonical form in memit-patches-canonical.md v2.4 §3.8.3. "
            f"Empirically reconcile: open {P7_TARGET_FILE}, locate the "
            f"`stat = layer_stats(...)` call inside the body of `def get_cov(...):`, "
            f"and update §3.8.3 ORIG_BLOCK to match the actual verbatim form. "
            f"P-7's structural intent (insert mom2_batch_tokens dispatch + add "
            f"batch_tokens=mom2_batch_tokens kwarg) is preserved across signature "
            f"variations."
        )
    src_new = src.replace(P7_ORIG_BLOCK, P7_PATCHED_BLOCK)

    # Post-state verification — every marker MUST be present before write
    for marker in P7_POST_MARKERS:
        assert marker in src_new, (
            f"P-7 marker {marker!r} not present after replace in {P7_TARGET_FILE}; "
            f"file would be left in inconsistent state — aborting write"
        )

    with open(P7_TARGET_FILE, "w") as f:
        f.write(src_new)
    print(f"P-7 applied to {P7_TARGET_FILE}")

# sys.modules purge — required because get_cov is imported at memit_main module load
for name in [n for n in list(sys.modules)
             if n == "memit" or n.startswith("memit.")]:
    del sys.modules[name]
```

The script verifies pre-state, applies the replacement only when both post-state markers are absent, verifies post-state, and purges `sys.modules` so subsequent `import memit.memit_main` reloads the patched bytes. Re-running is safe; the `fully_patched` short-circuit handles repeat invocations cleanly. Partial-state detection (post-block substring present but markers absent) is an explicit failure mode rather than a silent recover-and-write.

P-7 application is independent of P-3' application order: P-3' targets `execute_memit` body; P-7 targets `get_cov` body. The two patches can be applied in either order against the same SHA pin file. If both are applied, the `sys.modules` purge can be deferred to a single combined purge after both substitutions complete.

### 3.8.8 Verification (anchored to runbook v1.3 Cell 2 patch state verification)

P-7 verification follows the marker-substring pattern established for P-4 (§3.5.8), P-5 (§3.6.8), and P-6 (§3.7.8). `stage_1_sect_runbook.md` v1.3+ Cell 2 carries the canonical verification form when patch state is interrogated:

```python
# P-7 verification (canonical form for any Cell 2 patch-state check)
P7_FILE = f"{MEMIT_ROOT}/memit/memit_main.py"
P7_MARKERS = [
    "mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None",
    "batch_tokens=mom2_batch_tokens,",
]
with open(P7_FILE) as f:
    src = f.read()
for marker in P7_MARKERS:
    assert marker in src, f"P-7 marker {marker!r} missing from {P7_FILE}"
```

Verification is **substring presence** of both post-state markers. The dispatch-line marker (`mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None`) is whitespace-stable; the kwarg-presence marker (`batch_tokens=mom2_batch_tokens,`) is whitespace-stable on the assumption that the canonical replacement form preserves the conventional MEMIT four-space arg indentation. Any operator-side pretty-printer that reformats the file invalidates these markers and requires re-derivation.

For runtime correctness verification (distinct from source-byte verification), the empirical signature is the cache-dispatch round-trip behavior. Post-P-7, an edit-time invocation of `apply_memit_to_model` against an NV-resident cache file with `_t100_` segment in its filename resolves to a cache hit (no fallback compute, no causal_mask OOM). This is the canonical runtime gate, codified in `stage_1_sect_runbook.md` v1.3+ Cell 3 R1.3 (the smoke-load test added per OQ-S26-17 closure).

### 3.8.9 Discovery provenance and empirical NV record

P-7 was specified at IC-S26-1 draft form in `session_2_6_summary_block.md` v1 (2026-05-01) following the S2.6 Cell 9 Trial 0 halt; full specification (this entry), open-design-question resolution (D-S27-1, D-S27-2, D-S27-3), and idempotency contract authored at S2.7 (2026-05-01). Discovery context:

- **Symptom:** S2.6 Cell 9 Trial 0 Step 2 halted at LAYER 4 update attempt → cache lookup → 404 → fallback to local compute → `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 22.81 GiB.` The OOM occurred at `causal_mask.clone()` inside the LLaMA modeling code's attention forward pass under default `npos=131072` allocation regime.
- **Diagnostic:** forensic capture during S2.6 close window enumerated four artifacts to NV at `/workspace/architecture_profile/s26_halt_*.txt`: cache inventory (5 `.npz` files with `_t100_` segment present at canonical NV path), filename-evidence comparison (cache filename pattern at NV vs. MEMIT lookup form — the `_t100_` mismatch documented directly), `memit_main.py:170-200` excerpt (showing `get_cov` body's `layer_stats(...)` call with no `batch_tokens=` kwarg — the seed material for P-7 design), and post-halt `nvidia-smi` state. The diagnostic established the OOM as a symptom of the cache-dispatch filename mismatch, not an independent VRAM-budget defect.
- **Resolution path:** P-7 specification authored at S2.7 in `memit-patches-canonical.md` v2.4 §3.8 (this entry). Idempotency contract per IC-S25-2 precedent; verification logic per §3.7 P-6 precedent. NV-application of P-7 is operator-side action after S2.7 close; expected lifecycle: write `/workspace/memit_dry_run/memit/memit/memit_main.py` via the §3.8.7 application script, verify via §3.8.8 markers, re-run Stage 1 SECT cell 9 trial loop in a successor session against the post-P-7 MEMIT.
- **Empirical anchor (forward-deferred):** Stage 1 SECT re-attempt session (S2.8 or successor) Cell 9 Trial 0 PASS verdict will be the first empirical anchor for P-7 runtime correctness — specifically, an absence of fallback-to-local-compute log line and absence of OOM at `causal_mask.clone()` during MEMIT layer update. The S2.7 spec entry is the authoritative pre-empirical specification; the empirical NV record (parallel to P-6's §3.7.9 lifecycle) will be appended in a v2.4.1 amendment after the empirical PASS.

The empirical NV record is forward-compatible: any successor session that NV-restores from `/workspace/memit_dry_run/` after operator-side P-7 application inherits P-7; markers persist across pod stop/start. The reproducibility manifest's `memit_get_cov_batch_tokens_p7` field (v2.4 schema addition; see §8) is reported as `true` whenever both post-state markers are present.

References:

- `IC-S26-1` (draft P-7 specification; `session_2_6_summary_block.md` v1 §INTERFACE CONTRACTS) — superseded by this canonical entry
- `D-S27-1` (open question Q1 resolved — hardcoded literal `100`, not module-level constant)
- `D-S27-2` (open question Q2 resolved — modify `get_cov` body, not signature)
- `D-S27-3` (open question Q3 resolved — universal-safe via architectural-threshold runtime dispatch; no GPT-J substrate-shift)
- `C-S26-1` (ratified at S2.7 §3.8.5 — load-bearing for P-7)
- `C-S26-2` (ratified at S2.7 §3.8.5 — closed by P-7 by construction)
- `OQ-S26-16` (closed by this canonical entry — cache-dispatch architectural defect)
- `OQ-S26-18` (closed by C-S26-1 ratification at §3.8.5)
- `IC-PreS26-2` (post-P-6 cache filename interface contract — joint dependency of P-6 and P-7 for cache-dispatch round-trip correctness)
- `session_2_6_summary_block.md` v1 §FORENSIC SNAPSHOT INVENTORY (S2.6 halt artifacts; seed material for §3.8.5 rationale)
- `/workspace/architecture_profile/s26_halt_memit_main_get_cov_excerpt.txt` (NV-resident; verbatim pre-P-7 `get_cov` body excerpt at SHA pin `80426fd9...`)

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
4. P-6 (layer_stats:40 f-string prefix correction in rome/layer_stats.py — required when batch_tokens < npos)
   ↓ purge sys.modules of rome.* if rome was imported between P-5 and P-6
5. P-7 (get_cov body batch_tokens propagation in memit/memit_main.py — universal-safe via architectural-threshold dispatch)
   ↓ purge sys.modules of memit.* (P-7 modifies memit_main; memit_main caches imported get_cov binding at module load)
6. (P-3' if cuda:0 capacity < 18 GiB)
   ↓ purge sys.modules of memit.*, rome.*
7. Pad-Token alias (universal — alias only when tokenizer.pad_token is None per §4.4)
8. (Device-Map if multi-GPU — applied at from_pretrained, not retrofittable)
9. apply_memit_to_model(...)
   ↓ produces edited_model, orig_weights
10. Copy-Unmount (when overlay unmount is needed)
```

P-4, P-5, and P-6 all touch `rome/layer_stats.py` but at non-overlapping sites: P-6 touches line ≈ 40 (`size_suffix` f-string prefix), P-5 touches lines ≈ 97–103 (`load_dataset` dispatch), P-4 touches lines ≈ 101 + 108 (`n_positions → max_position_embeddings`). They are order-independent in the technical sense; the sequence above lists them in patch-ID order (P-4 → P-5 → P-6) by document-discipline convention. A combined application script that performs all three substitutions before a single sys.modules purge is functionally equivalent and operationally preferable.

P-3' and P-7 both touch `memit/memit_main.py` but at non-overlapping sites: P-3' touches lines ≈ 195–199 (`execute_memit` body — `torch.linalg.solve` block); P-7 touches lines ≈ 175–195 (`get_cov` body — `layer_stats` call site). They are order-independent in the technical sense. A combined application script that performs both substitutions before a single sys.modules purge of `memit.*` is functionally equivalent and operationally preferable. The same combined-purge optimization extends to a P-3'+P-7 pair on RTX 4090-class environments where P-3' is omitted (P-7 alone, single purge).

### 7.2 RunPod RTX 4090 sequence (Stage 1 production target — LLaMA 3.1 8B)

```
1. P-1 + P-2 (nethook)
2. P-4 (config-attribute fallback)
3. P-5 (dataset loader modernization — required under locked manifest datasets==4.8.3)
4. P-6 (layer_stats:40 f-string prefix correction — required under tractable batch_tokens=100 dispatch)
5. P-7 (get_cov body batch_tokens propagation — required for cache-dispatch round-trip on Llama-3.1-8B npos=131072)
6. Pad-Token alias (universal — Llama-3.1-8B base has pad_token=None at load per §4.4)
7. .to("cuda") model load (no Device-Map needed)
8. apply_memit_to_model(...)
9. Copy-Unmount when overlay unmount is needed
```

P-3' is not required (24 GiB sufficient for LLaMA 3.1 8B FP16 + FP64 transient on cuda:0).

P-6 is required for Stage 1: Llama-3.1-8B's `npos=131072` makes full-window per-token covariance accumulation compute-prohibitive on RTX 4090; the canonical Stage 1 dispatch operates at `batch_tokens=100` (per D-PreS26-6) — well below `npos` — so the `batch_tokens < npos` branch is taken at line 40, and the pre-P-6 form would emit literal `_t{batch_tokens}_` placeholders into cache filenames.

P-7 is required for Stage 1: without P-7, MEMIT's edit-time `get_cov` → `layer_stats` chain constructs lookup filenames lacking the `_t100_` segment that the cache files at NV carry (per IC-PreS26-2 and the cache produced by pre-S2.6 fork-work). The lookup misses; `layer_stats` falls back to local compute; the local compute attempts to allocate `causal_mask` at `npos=131072` (~22.81 GiB at fp16) and OOMs on the 24 GiB GPU. P-7 closes this asymmetry by propagating `batch_tokens=100` from `get_cov` body to `layer_stats` call (architectural-threshold-gated; see §3.8.6). P-6 and P-7 are jointly required for cache filename round-trip correctness; either patch alone is insufficient.

### 7.3 Kaggle 2× T4 sequence (smoke-test reference — GPT-J 6B; not Stage 1 target)

```
1. P-1 + P-2 (nethook)
2. P-4 (optional — backward-compatible on GPT-J; fallback to n_embd preserves Session 2.2 PASS)
3. P-5 (conditional — required if datasets ≥ 3.0 AND wikipedia dispatch is consumed; the Session 2.2 reference run pre-dates P-5 authorship and the post-3.0 datasets break)
4. P-6 (conditional — required when batch_tokens < npos; GPT-J npos=2048 typically dwarfs Stage 1 batch_tokens=100, so the conditional branch is taken; the Session 2.2 reference run pre-dates P-6 authorship)
5. P-7 (universal-safe — runtime no-op on GPT-J via architectural-threshold dispatch; npos=2048 is below the threshold 8192, so mom2_batch_tokens resolves to None and layer_stats runs default branch; cache filename form unchanged from pre-P-7)
6. P-3' (memit_main solve)
7. Pad-Token alias
8. Device-Map at from_pretrained
9. apply_memit_to_model(...)
10. Copy-Unmount when overlay unmount is needed
```

P-4 in §7.3 is listed as optional rather than required because the Kaggle Session 2.2 reference run pre-dates P-4 authorship and passed without it. Applying P-4 to a future GPT-J reference run is safe and recommended for cross-environment patch-state consistency.

P-5 in §7.3 is conditional rather than required because the Kaggle 2× T4 reference environment may carry an older `datasets` version. If `datasets ≥ 3.0` is in the Kaggle environment AND covariance compute against `wikipedia` substrate is in scope, P-5 becomes required. For any future GPT-J reference run that uses `wikitext` substrate or `datasets < 3.0`, P-5 may be omitted.

P-6 in §7.3 is conditional rather than required because the patch is no-op when `batch_tokens >= npos`. For GPT-J 6B (`npos=2048`), Stage 1 dispatch at `batch_tokens=100` satisfies `batch_tokens < npos`, so P-6 becomes required for any future GPT-J run that produces consumer-readable cache filenames. The Session 2.2 reference run pre-dates P-6 authorship; if the reference cache is re-validated against IC-PreS26-2 filename form, P-6 application + cache regeneration is the canonical reconciliation path.

P-7 in §7.3 is universal-safe and listed as a recommended apply-step rather than conditional. On GPT-J 6B (`npos=2048`), the architectural-threshold gate at `npos > 8192` evaluates `False`; `mom2_batch_tokens` resolves to `None`; `layer_stats` runs its default branch; cache filename form is identical to pre-P-7. Existing Block 2 reference cache (Session 2.2 — produced under default `batch_tokens=npos`) remains valid byte-for-byte under post-P-7 source. The Session 2.2 reference run pre-dates P-7 authorship; no methodology note is required for P-7 application against the existing reference cache. See §3.8.6 for the threshold derivation and the per-base-model behavior matrix.

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
    "memit_layer_stats_fstring_p6": true,
    "memit_get_cov_batch_tokens_p7": true,
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

**P-6 reporting (v2.3):** P-6 is reported as `true` when the post-state marker (`size_suffix = f"_t{batch_tokens}" + size_suffix` substring) is present in `rome/layer_stats.py`. P-6 is reported as `false` when the pre-state marker (`size_suffix = "_t{batch_tokens}" + size_suffix` substring without the `f` prefix) is present. There is no partial-marker state — the patch is a single-substitution edit and the post-state marker uniquely identifies completion. P-6 is reported as `true` whenever its post-state marker is present, regardless of whether the runtime path satisfies `batch_tokens < npos` (the patch is universal-safe and no-op on the alternate branch). Cross-reference: IC-PreS26-2 (canonical post-P-6 cache filename interface).

**P-7 reporting (v2.4):** P-7 is reported as `true` when both post-state markers are present in `memit/memit_main.py`: (a) the dispatch-line marker `mom2_batch_tokens = 100 if model.config.max_position_embeddings > 8192 else None`, AND (b) the kwarg-presence marker `batch_tokens=mom2_batch_tokens,`. P-7 is reported as `false` when neither marker is present (pre-P-7 state). A partial-marker state — exactly one marker present — is anomalous and indicates an interrupted application or a manual edit that requires reconciliation against §3.8.7 before any cache-dispatch proceeds. The §3.8.7 application script raises an explicit assertion on partial-state to prevent silent regression. P-7 is reported as `true` whenever both post-state markers are present, regardless of whether the runtime path satisfies `npos > 8192` (the patch is universal-safe and no-op on sub-threshold base models — see §3.8.6 backward-compatibility assertion). Cross-reference: C-S26-1 + C-S26-2 (operational constraints closed by P-7).

The manifest key `memit_config_attribute_compat_p4` is canonical. Earlier session artifacts (e.g., `stage_1_patch_state.json` produced by `stage_1_sect_runbook.md` v1.1 Cell 2) use the parallel key `P-4_config_attribute_fallback` for in-memory dataclass form; both refer to the same patch state. Future runbook updates may consolidate to a single key.

---

## 9. Upstream Submission Notes

`kmeng01/memit` is unmaintained (last commit 2022-11-14; 16 open issues; no triage). Patches P-1, P-2, P-3', P-4, P-5, P-6, and P-7 are reported but not submitted upstream — submission would not be merged. The framework's POC must fork the repository and pin to a known-patched fork rather than upstream `kmeng01/memit`. Forking work is deferred to Workstream 1 future tasks (per OQ-S22-17).

P-4 is a particularly clean submission candidate (universal-safe, backward-compatible, addresses a now-unavoidable issue for any post-2022 base model) and would benefit downstream MEMIT users were the upstream repo maintained. The patch is documented here in canonical form to support a future maintained-fork or alternative-upstream submission.

P-5 addresses an even more time-sensitive deprecation: HuggingFace `datasets` library deprecated repository-hosted Python loader scripts at version 3.0, structurally breaking MEMIT's `wikipedia` dispatch path for any post-2024 environment. P-5 is similarly clean (preserves the dispatch-dict idiom, conditional-safe, single file) and would benefit downstream MEMIT users immediately. The substrate-shift dimension (`20200501.en` → `20231101.en`) is documented in C-S25-15 and would also need to be carried into any upstream submission as a methodology note.

P-6 is the cleanest submission candidate of the four (P-4, P-5, P-6 layer_stats family): a single-character f-string prefix insertion that fixes an unambiguous Python authoring bug. The pre-P-6 form emits a literal `{batch_tokens}` placeholder into cache filenames whenever the `batch_tokens < npos` branch is taken — a universal regression for any consumer that parses the filename for the token-budget segment. Universal-safe, idempotent, no methodology note required, no substrate-shift dimension, no version-conditioned scope. Were the upstream repo maintained, P-6 should be submitted as an isolated single-line fix independent of P-4 and P-5.

P-7 is a strong submission candidate alongside P-6 — the two patches are semantically paired (P-6 fixes filename construction at cache-compute time; P-7 fixes filename construction at edit-time-dispatch via the `batch_tokens` propagation). The pre-P-7 cache-dispatch path is structurally broken on any base model with `npos > 8192` whose cache was produced under explicit `batch_tokens` truncation: the cache exists at NV but is structurally invisible to MEMIT's edit-time `get_cov` → `layer_stats` chain. The architectural-threshold-gated form (`100 if model.config.max_position_embeddings > 8192 else None`) makes the patch universal-safe — no behavior change on legacy short-context base models (GPT-J, GPT-2, LLaMA-2 7B), full corrective behavior on long-context base models (LLaMA-3, Mistral). No substrate-shift dimension, no methodology note required, no version-conditioned scope. The threshold value `8192` is operator-tunable in principle but architecturally justified at this value per §3.8.6; an upstream submission could surface the threshold as a module-level constant (e.g., `LONG_CONTEXT_NPOS_THRESHOLD`) for community tuning, while preserving the integer-literal form in the canonical patch entry. Were the upstream repo maintained, P-6 + P-7 should be submitted as a paired fix addressing the cache-dispatch round-trip problem in full.

---

## 10. Process Constraints

This section ratifies process-domain constraints surfaced during patch authoring sessions. Process constraints govern how patches and runbooks are authored, hardened, and verified — they do not modify MEMIT source bytes. They are documented here (rather than in the integrated spec) because the patches doc is the operational locus where the constraints bind.

### 10.1 C-S26-3 — Runbook hardening passes require a dry-run gate

> **C-S26-3 (ratified at S2.7).** Runbook hardening passes must include a dry-run execution against known-good NV state as part of the authoring acceptance gate. A hardening pass that does not exercise its target cells against fully-patched live state cannot be ratified; source-level verification defects survive purely-textual hardening passes and re-surface at consumer-session execution.

**Empirical motivation.** `stage_1_sect_runbook.md` v1.2 was authored as a "pre-Session-2.6 hardening pass" (per the v1.2 revision header) and was treated as ratified before consumer-session execution. At S2.6 first execution, three distinct defects surfaced on first live run:

| Defect | Surface | Cell | Remediation |
|---|---|---|---|
| `compute_z.py` path encoded as `rome/compute_z.py` (canonical: `memit/compute_z.py`) | OQ-S26-8 — Cell 2 first-attempt halt | Cell 2 | In-session dispatch-site bridge (D-S26-3a) |
| P-4 marker substring `hidden_size` insufficient (matches LLaMA's intrinsic `hidden_size` config attribute, not the patch fallback) | OQ-S25b-1 — Cell 2 second-attempt halt | Cell 2 | In-session dispatch-site bridge (D-S26-3b) |
| `get_cov` → `layer_stats` chain does not propagate `batch_tokens` | OQ-S26-16 — Cell 9 Trial 0 architectural defect | Cell 9 | P-7 spec authored at S2.7 |

The first two defects are textual — a dry-run pass against the NV-resident MEMIT repo would have surfaced both at hardening authorship time, before ratification. The third defect is architectural — a dry-run that exercised the full Cell 9 trial loop against post-P-6 MEMIT would have surfaced the cache-dispatch mismatch at hardening authorship time, before consumer-session execution.

**Hard requirement.** Any runbook hardening pass that adds, modifies, or reframes verification logic must execute that verification logic against the canonical NV-resident state before the hardening pass can be marked ratified. The dry-run gate is failure-class-aware: textual defects (path drift, marker mismatch) are caught by structural verification cells (e.g., Cell 0–Cell 4); architectural defects (cache-dispatch mismatch, OOM regimes) are caught by execution-class verification cells (e.g., Cell 5–Cell 9 trial loop or its lightweight smoke-equivalent).

**Tradeoffs accepted.**

| Cost | Benefit |
|---|---|
| Hardening passes lengthen by the duration of one dry-run execution (~30–90 min for execution-class cells; ~5–15 min for structural cells) | Defects do not survive into consumer-session execution; consumer sessions do not consume budget on bridge fixes |
| Dry-run requires NV-resident state to be intact at hardening time (operator-side coordination) | Hardening passes ratified against actual-environment state, not theoretical patches doc state |
| Runbook v1.x → v1.(x+1) lifecycle is more expensive operationally | Successive runbook versions converge toward defect-free; the three-defect surface pattern of S2.6 does not repeat |

**Open questions deferred.**

- OQ-S27-1 (NEW). Dry-run gate scope for runbooks targeting expensive execution cells (Cell 9 trial loop ~30+ min wall-time). The full-trial-loop dry-run is operationally costly. A lightweight smoke-equivalent (single-trial, single-fact, single-replicate, time-boxed at ~5 min) may satisfy C-S26-3 for the execution-class portion of a hardening pass while keeping wall-time tractable. Resolution path: empirical at v1.3 dry-run authorship; codify in v1.4 if the lightweight form proves discriminating against the architectural defects of S2.6 Cell 9 class.

**Interface contract.** None — C-S26-3 is a process constraint binding on runbook authoring sessions, not a runtime interface. Cross-references: OQ-S26-9 (closed by this ratification); `stage_1_sect_runbook.md` v1.3 front matter (carries C-S26-3 acknowledgment + dry-run record).

### 10.2 C-S26-1 — `batch_tokens=100` mandatory for LLaMA-family on RTX 4090 (cross-reference)

C-S26-1 is ratified in §3.8.5 as load-bearing for P-7. Its operational binding is the architectural-threshold dispatch in P-7's source-level mechanism (§3.8.3). Cross-reference repeated here for §10 process-constraints completeness.

### 10.3 C-S26-2 — Cache-dispatch path explicit `batch_tokens` propagation (cross-reference)

C-S26-2 is ratified in §3.8.5 as closed by P-7 by construction. Its operational binding is the kwarg-presence post-state marker in P-7's idempotency contract (§3.8.7 / §3.8.8). Cross-reference repeated here for §10 process-constraints completeness.

### 10.4 C-S28-1 — Hardening passes must verify defense-in-depth markers against post-application NV state

> **C-S28-1 (ratified at S2.9).** Runbook hardening passes that authorize defense-in-depth checks (post-application-state markers beyond load-bearing patches) must verify the marker's actual post-application source form against fully-patched NV state, not infer it from pre-substitution patch description prose. Markers inferred from patch documentation alone — without empirical verification against post-application source — may reference substrings that the patch substitutes away, producing assertion failures on consumer-session execution despite correct patch application.

**Empirical motivation.** `stage_1_sect_runbook.md` v1.3 was authored under C-S26-3 (the dry-run gate constraint codified in §10.1) and was treated as ratified after S2.7 hardening. At S2.8 first-execution, Cell 2 raised an AssertionError on the line 552 marker `assert "hidden_size" in layer_stats_src` — the v1.3 marker was inferred from P-4's pre-substitution form (which references `hidden_size` as the pre-state name in `compute_z.py` and `compute_v.py`) without verifying that P-4's substitution scope on `rome/layer_stats.py` is `n_positions → max_position_embeddings` only and does NOT reference `hidden_size` in either pre- or post-substitution form on that file. The marker referenced a substring that does not appear in the canonical post-P-4 source of `rome/layer_stats.py`, producing a defect that survived purely-textual hardening review.

The C-S26-3 dry-run gate at S2.8 caught the defect at the structural-dry-run cell (Cell 2) before the load-bearing Cell 9 surface — the gate methodology achieved its design intent. C-S28-1 codifies the prevention upstream: the marker should not have been authored without first verifying the post-application source.

| v1.3 marker (defective) | What the marker assumed | What P-4 actually produced |
|---|---|---|
| `assert "hidden_size" in layer_stats_src` (line 552) | P-4 leaves `hidden_size` references intact in `rome/layer_stats.py` (defense-in-depth check that P-4 didn't catastrophically replace the file) | P-4's `rome/layer_stats.py` substitution map (`n_positions → max_position_embeddings` at lines ~101 + ~108) operates on a file that contains zero `hidden_size` references pre- or post-P-4. The defense-in-depth marker reference was confused with the equivalent markers on `compute_z.py` + `compute_v.py` (where `hidden_size` IS retained post-P-4 — those file substitutions are different per §3.5.4) |

**Hard requirement.** Any runbook hardening pass that adds a defense-in-depth marker (an assertion beyond the load-bearing patch idempotency checks of §3.x.7 and §3.x.8) must:

1. Identify the canonical post-application form of the patched file by inspection of the live NV-resident source (or equivalent post-application reference state).
2. Verify that the marker substring is present in the post-application form. If the marker substring is absent, the marker must not be authored — either choose a different marker OR delete the verification surface entirely.
3. Document the empirical anchor inline in the runbook source as a comment (e.g., `# C-S28-1 verification anchor: post-P-X NV state at <path>; <substring> count = N (verified <date>)`).

The C-S26-3 dry-run gate (§10.1) catches markers that violate C-S28-1 at first consumer-session execution. C-S28-1 codifies the upstream prevention so that hardening passes do not ship markers requiring dry-run-time correction.

**Tradeoffs accepted.**

| Cost | Benefit |
|---|---|
| Hardening passes that introduce defense-in-depth markers must include a post-application audit step (1–5 min per marker) | Marker defects do not survive into consumer-session execution; the C-S26-3 dry-run gate becomes a redundant safety net rather than a load-bearing defect-discovery surface |
| Authoring discipline requires distinguishing between (a) pre-substitution patch documentation (used to author the patch) and (b) post-substitution NV source (used to author the verification marker) | Markers reflect actual NV state, not theoretical patch state; the documentation/state divergence that produced OQ-S28-3 cannot recur |
| Marker authorship is no longer a textual operation against the patches doc; it is an empirical operation against post-application state | Hardening pass artifacts are robust to patch documentation drift (e.g., if a patch description is later rephrased without changing substitution scope, existing markers are unaffected) |

**Application scope.** C-S28-1 binds on:

- All future runbook hardening passes (`stage_1_sect_runbook.md v1.5+`, `pre_sN_M_fork_work_runbook.md` revisions, etc.)
- Any new defense-in-depth markers added during cross-runbook consolidation
- New patches documented in §3.x of this canonical document — the §3.x.8 verification block must include only markers verified against post-application NV state

C-S28-1 does NOT require retroactive re-authoring of existing markers ratified under prior runbook revisions. The S2.9 v1.4 hardening pass demonstrates the application pattern by example: the OQ-S28-3 closure DELETES the v1.3 line 552 marker (rather than replacing it) because the post-application source of `rome/layer_stats.py` contains zero `hidden_size` references, leaving no valid post-application marker substring for that surface. The retained `compute_z.py` + `compute_v.py` `hidden_size` markers were verified against S2.8 NV state (post-P-4 source contains `hidden_size` references on those files; verification documented in `session_2_8_summary_block.md` §2.1 forensic record).

**Open questions deferred.**

- None at S2.9 close. C-S28-1 is fully self-contained as a Process Constraint; the empirical motivation (OQ-S28-3) is closed by deletion at v1.4. Future hardening-pass-class OQs may surface as marker authorship patterns are exercised on subsequent revisions.

**Interface contract.** None — C-S28-1 is a process constraint binding on runbook authoring sessions, not a runtime interface. Cross-references:

- §10.1 (C-S26-3 dry-run gate; C-S28-1 strengthens C-S26-3 by addressing marker-class defects upstream of the dry-run surface)
- `session_2_9_summary_block.md` §2.5 (D-S29-5 ratification authority) and §3.1 (constraint posture at S2.9 close)
- `session_2_8_summary_block.md` §2.1 (D-S28-1 in-session bridge fix forensic record) and §6.7 (C-S28-1 candidate-constraint motivation)
- `stage_1_sect_runbook.md v1.4` §1.5 (v1.4 ratification posture explicitly cites the C-S28-1 application gate; OQ-S28-3 closure inline comment carries the empirical-anchor documentation pattern required by the hard requirement above)

---

*End of MEMIT Patches Canonical Specification v2.5.*
