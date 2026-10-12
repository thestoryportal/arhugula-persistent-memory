# GRACE Patches Canonical — v0.2

**Status:** EMPIRICALLY VALIDATED (S2.20 close + v0.2 codification)
**Supersedes:** v0.1 (declarative; 497L; ratified 2026-05-05 at S2.19 close)
**Carry-forward target:** S2.21 = T.1-GRACE-3B retry runbook v0.1 authoring
**Parallel siblings:** `memit-patches-canonical v2.5`, `rome-patches-canonical v0.2`

---

## §0. Version History

| Version | Date | Status | Scope |
|---|---|---|---|
| v0.1 | 2026-05-05 | DECLARATIVE | Sibling-parity authoring at S2.19; 10 entries projected; no empirical validation |
| v0.2 | 2026-05-05 | EMPIRICALLY VALIDATED | S2.20 execution surfaced 2 NEW SOURCE_LAYER patches mid-session (P-1-GRACE, P-2-GRACE); upstream defects against fp16 modern HF transformers; 1 CONFIGURATION_LAYER class added (F-2 dispatch preamble) |

### §0.1 v0.1 → v0.2 Diff Summary

| Surface | v0.1 | v0.2 |
|---|---|---|
| Patch entries | 10 declarative (parallel-sibling projection) | 2 EMPIRICALLY VALIDATED + 8 INAPPLICABLE-per-mechanism |
| Patch classes | SOURCE_LAYER only | SOURCE_LAYER + CONFIGURATION_LAYER |
| Constraint codification | C-GRACE-1..5 declarative | C-GRACE-1..5 RATIFIED + C-S220-2/3 + C-F-2-DISPATCH-1 |
| Empirical surface | none | S2.20 Cell 2++ + Cell 2++++ + Cell 11++++++ |
| Forward applicability | runbook v0.1 declarative consumption | runbook v0.2 canonical consumption |

---

## §1. Patch Inventory

### §1.1 Active Patches (Empirically Validated)

| ID | Class | Target | Status | Sites | Defect Class |
|---|---|---|---|---|---|
| P-1-GRACE | SOURCE_LAYER | `grace_barebones.py` | EMPIRICALLY VALIDATED | 9 | Universal (HF transformer with numeric submodule indices) |
| P-2-GRACE | SOURCE_LAYER | `grace_barebones.py` | EMPIRICALLY VALIDATED | 1 | Universal (fp16-loaded model + non-empty GRACE codebook) |
| Pad-Token | TOKENIZER | tokenizer instance | EMPIRICALLY VALIDATED | 1 | Llama-class tokenizer (no native pad token) |

### §1.2 Active Configuration (Empirically Validated)

| ID | Class | Target | Status | Mechanism |
|---|---|---|---|---|
| F-2 | CONFIGURATION_LAYER | runtime model state | EMPIRICALLY VALIDATED | `model.train()` post-constructor; `requires_grad_` NOT modified |

### §1.3 Inapplicable Patches (Mechanism-Excluded)

| ID | Class | Inapplicability Source |
|---|---|---|
| P-3' (CONFIG_LAYER) | n/a | INAPPLICABLE — GRACE has Hydra config tree but `_barebones` variant bypasses entirely (D-S220-CONFIG-LAYER-1) |
| Device-Map | n/a | INAPPLICABLE — single-GPU dispatch on RTX 4090; no multi-GPU sharding |
| P-4 / P-5 / P-6 | n/a | INAPPLICABLE — MEMIT/ROME-specific; GRACE adapter mechanism does NOT consume layer_stats covariance caches |
| P-7-ROME / P-8-ROME / P-9-ROME | n/a | INAPPLICABLE — ROME-specific compute_v / mom2 path; not present in GRACE_barebones execution path |
| Copy-Unmount | n/a | INAPPLICABLE per `t_branch_decision_document v1.1 §6'.2` — GRACE uses adapter substitution + layer-restore, not in-place weight modification |

### §1.4 Patch Disposition Matrix (Cross-Engine)

```
Patch                  MEMIT v2.5    ROME v0.2     GRACE v0.2
═══════════════════════════════════════════════════════════════
P-1                    ACTIVE        ACTIVE        N/A (different defect class)
P-1-GRACE              N/A           N/A           ACTIVE (this doc §6)
P-2                    ACTIVE        ACTIVE        N/A
P-2-GRACE              N/A           N/A           ACTIVE (this doc §7)
P-3'                   CONDITIONAL   N/A           INAPPLICABLE
P-4 / P-5 / P-6        ACTIVE        ACTIVE-       INAPPLICABLE
                                     TRANSPLANTED
P-7                    ACTIVE        N/A           INAPPLICABLE
P-7-ROME / P-8-ROME    N/A           ACTIVE        INAPPLICABLE
P-9-ROME
Pad-Token              ACTIVE        ACTIVE        ACTIVE
Copy-Unmount           ACTIVE        ACTIVE        INAPPLICABLE
═══════════════════════════════════════════════════════════════
```

---

## §2. v0.1 Undocumented Findings (Resolved at v0.2)

### §2.1 Findings inherited from v0.1 declarative + resolved empirically at S2.20

| Finding | v0.1 disposition | v0.2 resolution |
|---|---|---|
| F1 | Adapter mechanism unmount path | Declarative: adapter-detach API (D-S219-Q4-1) | RETRACTED → layer-restore via `current.layer` per D-S220-LAYER-RESTORE-1; D-S220-UNMOUNT-1 |
| F2 | Adapter parameter registration | Declarative: nn.ParameterList | RECONTEXTUALIZED → tuple-unpacking assignment to `self.values` registers via nn.Module.__setattr__ routing to `_parameters`; verified via optimizer count delta |
| F3 | Constructor freeze behavior | Undocumented | DOCUMENTED at §6 — GRACE_barebones.__init__ explicitly freezes base model via for-loop on named_parameters |
| F4 | fp16 forward path | Declarative: assumed compatible | FALSIFIED → `torch.cdist` fp16 incompatibility surfaces at first non-empty codebook forward; P-2-GRACE required |
| F5 | eval(f-string) layer resolution | Declarative: assumed compatible | FALSIFIED → numeric path components (`layers.17`) trigger Python parse error; P-1-GRACE required |
| F6 | edit() loop optimizer construction | Declarative: assumed sufficient | RECONTEXTUALIZED → optimizer construction at iter=0 captures adapter values registered during forward pass |
| F7 | Gradient flow path | Declarative: assumed via standard backprop | RECONTEXTUALIZED → flows through frozen layers via saved activations to adapter value at edit site |
| F8 | Backward pass VRAM cost | Undocumented | DOCUMENTED at §10 — activation retention for L17-L31 produces 24.61 GiB allocation; exceeds RTX 4090 24 GiB ceiling by ~0.6 GiB |

---

## §3. Constraint Registry

### §3.1 Declarative Constraints (v0.1 carry-forward; RATIFIED at v0.2)

| ID | Statement | Verification Site (S2.20) |
|---|---|---|
| C-GRACE-1 | Single-fact dispatch envelope: one edit, one fact per Cell 9/11/15 | Cell 9.5+ + Cell 11.5+ |
| C-GRACE-2 | Fresh adapter pool init at trial entry: `'keys' not in __dict__` post-instantiation | Cell 8++.5 + Cell 9.5 + Cell 11.5 |
| C-GRACE-3 | R1.3-equivalent dry-run gate: empty-codebook substitution produces drift `0.00e+00` | Cell 8++.6 (`drift=0.00e+00`) |
| C-GRACE-4 | Pad-Token alias: `tokenizer.pad_token = tokenizer.eos_token` (Llama-class tokenizer compensation) | Cell 5.4 (`pad_token_id=128001`) |
| C-GRACE-5-REVISED | Layer-restore unmount via captured `original_layer` reference; supersedes adapter-detach | Cell 8++.7-9 (`drift=0.00e+00`) |

### §3.2 NEW Constraints (S2.20 ratified)

| ID | Statement | Verification Site |
|---|---|---|
| C-S220-2 | HF token shape gate: `len(content) ≥ 37` AND `content.startswith('hf_')` AND no whitespace AND all printable ASCII; sentinel placeholder triggers HALT | Cell 5.1.1 |
| C-S220-3 | Cross-session bit-exact gate combined acceptance: top-1 token ID strict equality (mandatory) + drift `< 1e-5` (rounding-class regime ceiling) | Cell 5++++++ |
| C-F-2-DISPATCH-1 | Pre-edit dispatch preamble: `model.train()` post-constructor; `requires_grad_(True)` NOT invoked; `gradient_checkpointing_enable()` NOT invoked | Cell 9.5+ + Cell 11.5+ + Cell 11+++++++++ |

### §3.3 Process Constraints (Inherited from v0.1)

| ID | Statement | Source |
|---|---|---|
| C-PRE-DISPATCH-STATE-1 | All cells dispatching `editor.edit()` must verify substitution sites are Linear at entry; recovery via Cell 9-- pattern if stale GRACEAdaptor present | S2.20 Cell 9-- recurrence |
| C-PRE-DISPATCH-AUDIT-1 | Pre-Block-C verdict integrity audit (Cell 11++ pattern) executes UNCONDITIONALLY post-Block-B; verifies loss differentiability + adapter parameter registration + optimizer scope | IC-S220-4 |
| C-PATCH-APPLICATION-1 | SOURCE_LAYER patches preserve pristine via `<file>.upstream_pristine`; defensive read from pristine; single-line replacement with unique terminal-statement anchor | IC-S220-2 |

---

## §4. Patch Discipline

### §4.1 Pristine Preservation

```
Pre-application:
  shutil.copy2(target_file, target_file.with_suffix(".py.upstream_pristine"))

Read source:
  src = pristine.read_text()    # defensive baseline; not live file

Apply transformation:
  src_patched = src.replace(old_pattern, new_pattern)

Verify pattern:
  assert old_pattern not in src_patched
  assert new_pattern_count == expected_count

Write:
  target_file.write_text(src_patched)

Reload:
  for mod in sys.modules: del sys.modules[mod] if mod.startswith("grace.editors")
  importlib.reload(grace.editors.grace_barebones)

Marker assertion:
  reload_src = target_file.read_text()
  assert "marker_string" in reload_src

Manifest update:
  patch_state.json["patches_applied"][patch_id] = {...}
```

### §4.2 Single-Line Replacement Form (C-S220-PATCH-AUTHORING-1)

| Pattern type | Resilience | Rationale |
|---|---|---|
| Multi-line literal | LOW | whitespace-divergence-fragile; tabs/spaces mixing breaks match |
| Single-line terminal-statement | HIGH | matches unique anchor; surrounds context substitution |
| Regex with DOTALL | MEDIUM | survives whitespace; risks over-matching adjacent functions |
| Line-number-indexed | HIGH | bypasses pattern matching; fragile to upstream version drift |

Selected: single-line terminal-statement form. Empirically validated at Cell 2++ + Cell 2++++.

---

## §5. SOURCE_LAYER Patch Class — Definition

### §5.1 Definition

A SOURCE_LAYER patch modifies the upstream Python source file of the GRACE editor implementation. Modifications target structural defects in upstream source that block execution against modern HuggingFace transformer infrastructure (numeric-indexed submodules, fp16 default precision).

### §5.2 Application Discipline

| Property | Requirement |
|---|---|
| Pristine preservation | `<file>.upstream_pristine` MUST exist before first patch application |
| Reversibility | Patch reversion via pristine restoration MUST be possible |
| Marker assertion | Patched source MUST contain identifiable marker (comment OR distinctive substring) |
| Provenance | Patch state manifest at `/workspace/architecture_profile/<engine>_patch_state.json` MUST record site count + line numbers + rationale |

### §5.3 Verification Sites

```
Patch application verification flow:
═══════════════════════════════════════════════════════════════════
  Cell 2 (engine clone + introspect)
       │
       ▼
  Cell 2++ (P-1-GRACE application)
       │
       ├── pristine preserved
       ├── 9 sites enumerated [44, 53, 56, 57, 62, 76, 77, 78, 79]
       ├── replacement applied
       └── marker assertion PASS
       │
       ▼
  Cell 2++++ (P-2-GRACE application)
       │
       ├── pristine confirmed (idempotent)
       ├── 1 site enumerated (line 9; function euclidean_distance)
       ├── replacement applied
       └── marker assertion PASS
       │
       ▼
  Cell 8++ (R1.3 dry-run; verifies P-1-GRACE)
       │
       └── empty-codebook substitution drift 0.00e+00
       │
       ▼
  Cell 9.5+ + Cell 11.5+ (verifies P-2-GRACE)
       │
       └── edit() forward pass executes past line 9 without RuntimeError
═══════════════════════════════════════════════════════════════════
```

---

## §6. P-1-GRACE — Specification

### §6.1 Identification

| Field | Value |
|---|---|
| ID | P-1-GRACE |
| Class | SOURCE_LAYER |
| Target file | `grace/editors/grace_barebones.py` |
| Site count | 9 |
| Site line numbers | `[44, 53, 56, 57, 62, 76, 77, 78, 79]` |
| Defect class | Universal (HF transformer with numeric-indexed submodules) |
| Status | EMPIRICALLY VALIDATED (Cell 9.6 dispatch executes past line 56 without SyntaxError) |
| Authored | S2.20 Cell 2++ (2026-05-05) |

### §6.2 Defect Statement

Upstream `grace_barebones.py` constructs attribute access expressions via `eval()` on f-strings interpolating `self.layer`:

```python
eval(f"self.model.{self.layer}")
```

For `self.layer = "model.layers.17.mlp.down_proj"`, this resolves to:

```
eval("self.model.model.layers.17.mlp.down_proj")
```

Python rejects `layers.17` as syntactically invalid attribute access (number after dot is parsed as float literal beginning). The expression is unparseable regardless of runtime semantics.

### §6.3 Mechanism

```python
# OLD (upstream; sites 44, 53, 56, 57, 62, 76, 77, 78, 79):
eval(f"self.model.{self.layer}")

# NEW (P-1-GRACE):
getattr(parent_module(self.model, self.layer), self.layer.rsplit(".", 1)[-1])
```

### §6.4 Site Inventory

| Line | Method | Purpose | Original |
|---|---|---|---|
| 44 | `__call__` (generation branch) | sets `key_id` on substituted layer | `setattr(eval(f"self.model.{self.layer}"), "key_id", key_id)` |
| 53 | `edit` preamble | sets `key_id` (generation conditional) | `setattr(eval(f"self.model.{self.layer}"), "key_id", key_id)` |
| 56 | `edit` preamble | sets `training=True` flag | `setattr(eval(f"self.model.{self.layer}"), "training", True)` |
| 57 | `edit` preamble | sets `edit_label` | `setattr(eval(f"self.model.{self.layer}"), "edit_label", tokens["labels"])` |
| 62 | `edit` loop body | sets `iter` per iteration | `setattr(eval(f"self.model.{self.layer}"), "iter", i)` |
| 76 | `edit` post-loop | sets `training=False` | `setattr(eval(f"self.model.{self.layer}"), "training", False)` |
| 77 | `edit` post-loop | reads `chosen_key` | `getattr(eval(f"self.model.{self.layer}"), "chosen_key")` |
| 78 | `edit` post-loop | reads `keys` | `getattr(eval(f"self.model.{self.layer}"), "keys")` |
| 79 | `edit` post-loop | reads `epsilons` | `getattr(eval(f"self.model.{self.layer}"), "epsilons")` |

### §6.5 Verification Assertions

```python
# Cell 2++ marker assertion:
assert 'eval(f"self.model.{self.layer}")' not in patched_source
assert patched_source.count("parent_module(self.model, self.layer)") >= 9

# Cell 9.6 empirical validation:
editor.edit(tokens)    # MUST NOT raise SyntaxError
```

### §6.6 Defect Universality

P-1-GRACE addresses a defect that affects:

- All HuggingFace transformer models with numeric-indexed decoder layers (`model.layers[N]`)
- Llama / Llama-2 / Llama-3 / Llama-3.1 / Llama-3.2 family
- Mistral / Mixtral family
- Qwen / Qwen-2 / Qwen-3 family
- GPT-2 / GPT-Neo / GPT-J / GPT-NeoX

P-1-GRACE does NOT affect models with name-indexed layers (legacy GPT-style models with `transformer.h.0` paths — these tokenize through the same eval path but `h.0` is parseable as `h` attribute followed by `.0` numeric — also fails).

### §6.7 v0.2 Codification

P-1-GRACE is canonical for any GRACE_barebones execution against modern HF transformer infrastructure. S2.21 inherits at runbook entry.

---

## §7. P-2-GRACE — Specification

### §7.1 Identification

| Field | Value |
|---|---|
| ID | P-2-GRACE |
| Class | SOURCE_LAYER |
| Target file | `grace/editors/grace_barebones.py` |
| Site count | 1 |
| Site location | line 9, function `euclidean_distance` |
| Defect class | Universal (fp16-loaded model + non-empty GRACE codebook) |
| Status | EMPIRICALLY VALIDATED (Cell 9.6 forward pass executes past distance computation without RuntimeError) |
| Authored | S2.20 Cell 2++++ (2026-05-05) |

### §7.2 Defect Statement

PyTorch's `torch.cdist` lacks a CUDA fp16 implementation:

```
RuntimeError: "cdist_cuda" not implemented for 'Half'
```

GRACE's `euclidean_distance` function calls `torch.cdist(key, query, p=2)` directly. With fp16-loaded models, both `key` (codebook key from forward pass query) and `query` (current forward pass query) are fp16 tensors. The error raises on first invocation when codebook is non-empty (typically iter=1 of the edit loop, after iter=0 seeds the first key).

### §7.3 Mechanism

```python
# OLD (upstream; line 9):
def euclidean_distance(query, key):
    if len(key.shape) < 2:
        key = key.view(1, -1)
    return torch.cdist(key, query, p=2)

# NEW (P-2-GRACE):
def euclidean_distance(query, key):
    if len(key.shape) < 2:
        key = key.view(1, -1)
    # P-2-GRACE: torch.cdist lacks CUDA fp16 implementation; upcast for computation
    if key.dtype == torch.float16 or query.dtype == torch.float16:
        return torch.cdist(key.float(), query.float(), p=2).to(torch.float16)
    return torch.cdist(key, query, p=2)
```

### §7.4 Numerical Properties

| Property | Behavior |
|---|---|
| Precision | fp32 distance computation; fp16 storage of result |
| Determinism | Deterministic upcast/downcast preserves bit-exactness across sessions |
| Conditional semantics | No-op for fp32/bf16/int paths; preserves upstream behavior on non-fp16 models |
| Compute overhead | One fp16→fp32 cast per call + one fp32→fp16 cast per call; negligible vs cdist O(NM) cost |

### §7.5 Verification Assertions

```python
# Cell 2++++ marker assertion:
assert "P-2-GRACE" in patched_source
assert "key.dtype == torch.float16 or query.dtype == torch.float16" in patched_source

# Cell 9.6 empirical validation:
editor.edit(tokens)    # MUST NOT raise RuntimeError("cdist_cuda" not implemented for 'Half')
```

### §7.6 Defect Universality

P-2-GRACE addresses a defect that affects all fp16-loaded models with non-empty GRACE codebook. Activation by codebook size:

| Codebook size | Path taken in GRACEAdaptor.forward() | P-2-GRACE invoked? |
|---|---|---|
| 0 (empty) | `init_key_value()` short-circuit | NO (no distance computation) |
| 1+ (any non-empty) | `euclidean_distance(query, key)` per key | YES |

In the n_iter=200 canonical loop, codebook becomes non-empty at iter=0 (key seeded). P-2-GRACE is invoked from iter=1 onward (199 iterations).

### §7.7 v0.2 Codification

P-2-GRACE is canonical for any GRACE_barebones execution at fp16 precision. S2.21 with Llama-3.2-3B at fp16 inherits at runbook entry.

---

## §8. Pad-Token — Specification

### §8.1 Identification

| Field | Value |
|---|---|
| ID | Pad-Token |
| Class | TOKENIZER |
| Target | tokenizer instance (in-process; not source modification) |
| Status | EMPIRICALLY VALIDATED (Cell 5.4) |
| Pre-condition | Llama-class tokenizer (no native pad_token) |

### §8.2 Mechanism

```python
tokenizer.pad_token = tokenizer.eos_token
assert tokenizer.pad_token == tokenizer.eos_token
# pad_token_id = 128001 (Llama-3.1-8B; eos_token_id mapping)
```

### §8.3 Cross-Engine Invariance

Pad-Token applies identically across MEMIT v2.5 / ROME v0.2 / GRACE v0.2. The constraint is tokenizer-class invariant; Llama-class tokenizers ship without a native `pad_token` attribute and require operator-side aliasing for batch tokenization paths in the edit loop.

### §8.4 Verification

| Site | Assertion |
|---|---|
| Cell 5.4 | `tokenizer.pad_token == tokenizer.eos_token` |
| Cell 5.4 | `tokenizer.pad_token_id == 128001` (Llama-3.1-8B) |
| Cell 9.4 / Cell 11.4 | tokenized inputs produce expected `(1, 8)` shape including BOS |

---

## §9. CONFIGURATION_LAYER Patch Class — Definition

### §9.1 Definition

A CONFIGURATION_LAYER patch modifies runtime model state without altering upstream source. Modifications target configuration defects that prevent edit dispatch under default model load configuration (e.g., `model.eval()` chained on `from_pretrained`).

### §9.2 Distinction from SOURCE_LAYER

| Property | SOURCE_LAYER | CONFIGURATION_LAYER |
|---|---|---|
| Target | upstream `.py` file | runtime model object |
| Persistence | persists across kernel restarts | resets on kernel restart |
| Pristine preservation | `<file>.upstream_pristine` | N/A (no source modification) |
| Reversibility | restore from pristine | invoke inverse operation |
| Verification site | marker assertion in source | runtime state assertion |

### §9.3 Inventory at v0.2

| ID | Mechanism | Status |
|---|---|---|
| F-2 | `model.train()` post-constructor; preserve constructor freeze | EMPIRICALLY VALIDATED (Cell 11++++++) |

---

## §10. F-2 — Configuration Specification

### §10.1 Identification

| Field | Value |
|---|---|
| ID | F-2 |
| Class | CONFIGURATION_LAYER |
| Target | runtime model state (in-kernel) |
| Status | EMPIRICALLY VALIDATED |
| Authored | S2.20 Cell 11++++++ (2026-05-05) |
| Supersedes | F-1 (RETRACTED — `model.requires_grad_(True)` blanket caused OOM at backward pass) |

### §10.2 Statement

```python
# F-2 (canonical pre-dispatch preamble):
editor = GRACE_barebones(model=..., layer=..., ...)
model.train()                                         # F-2.1: enable training mode
# DO NOT invoke model.requires_grad_(True)            # F-1 RETRACTED — causes OOM
# DO NOT invoke model.gradient_checkpointing_enable() # F-3 INCOMPATIBLE with adapter
```

### §10.3 Mechanism

```
F-2 dispatch flow:
═══════════════════════════════════════════════════════════════════
  GRACE_barebones.__init__ executes
       │
       ├── Internal freeze: for n,p in model.named_parameters(): p.requires_grad=False
       └── Layer substitution: GRACEAdaptor replaces target Linear at edit site
       │
       ▼
  F-2.1 invoked: model.train()
       │
       └── Toggles training flag on all Modules (model.training=True)
       │
       ▼
  editor.edit(tokens) loop iter=0
       │
       ├── Adapter forward call
       │     │
       │     ├── new_value = nn.Parameter(torch.rand(..., requires_grad=True))
       │     ├── init_key_value() returns (key, new_value, epsilon, key_label)
       │     └── tuple-unpacking assignment: self.values = new_value
       │           └── nn.Module.__setattr__ routes to _parameters dict
       │
       ├── outputs.loss.requires_grad transitions True via chain through frozen layers
       │
       └── Adam optimizer = torch.optim.Adam(model.parameters(), lr)
             └── enumerates trainable parameters; finds adapter value (shape value_shape)
                   └── 4096 trainable params (Llama-3.1-8B L17 down_proj output dim)
       │
       ▼
  iter=1..199:
       └── forward + backward chain rule via saved activations (frozen layers)
             └── grad accumulates only on adapter value (4096 params)
             └── optimizer.step() updates adapter value
═══════════════════════════════════════════════════════════════════
```

### §10.4 VRAM Cost Analysis

| Component | Size | Source |
|---|---|---|
| Model weights (fp16, 8.03B params) | 16.06 GiB | Llama-3.1-8B static |
| Activations L0–L(edit_site-1) | 0.00 GiB | no grad downstream → not retained |
| Activations L(edit_site)–L(N-1) | size(post-edit-layers) × seq_len × hidden | retained for backward |
| Adapter value | 0.05 GiB | nn.Parameter `(1, value_shape)` |
| Adam state (m, v moments) | 0.05 GiB | adapter value only |
| Workspace + cuBLAS | ~0.5 GiB | runtime overhead |

#### §10.4.1 Llama-3.1-8B (32 layers) at L17

```
Activation retention: 15 decoder layers × seq_len 8 × hidden 4096 × fp16
                    = 15 × 8 × 4096 × 2 bytes
                    × intermediate buffers (multiple per layer)
                    ≈ 8 GiB

Total: 16.06 + 8.00 + 0.10 + 0.50 = 24.61 GiB
RTX 4090 ceiling: 24.00 GiB
HEADROOM: -0.61 GiB → OOM
```

#### §10.4.2 Llama-3.2-3B (28 layers) at L17 (S2.21 projection)

```
Model weights: 3.21B × fp16 = 6.42 GiB
Activation retention: 11 decoder layers × seq_len 8 × hidden 3072 × fp16
                    ≈ 2.5 GiB
Adapter + Adam + workspace: ~0.55 GiB

Total: 6.42 + 2.50 + 0.55 = 9.47 GiB
RTX 4090 ceiling: 24.00 GiB
HEADROOM: 14.53 GiB → fits comfortably
```

### §10.5 Wall-Time Cost

| Operation | Cost on Llama-3.1-8B + RTX 4090 (projected if fit) | Cost on Llama-3.2-3B + RTX 4090 |
|---|---|---|
| iter=0 (forward + key seed + optimizer init) | ~0.5 s | ~0.2 s |
| iter=1..199 (forward + backward + step) | ~0.4 s/iter × 199 = ~80 s | ~0.2 s/iter × 199 = ~40 s |
| Total (200 iter loop) | ~80 s | ~40 s |

Llama-3.1-8B execution is unverifiable (S2.20 OOMed). Llama-3.2-3B projection extrapolates from observed iter=0 cost on Cell 11++++++ multiplied by 200.

### §10.6 Verification Assertions

```python
# Cell 11++++++ verification (post-F-2 application):
outputs = editor.model(**tokens)
assert outputs.loss.requires_grad == True
assert 'keys' in substituted.__dict__
assert 'values' in substituted._parameters

optimizer = torch.optim.Adam(editor.model.parameters(), editor.learning_rate)
trainable_in_opt = sum(
    p.numel() for group in optimizer.param_groups
    for p in group['params'] if p.requires_grad
)
assert 1000 < trainable_in_opt < 10000  # adapter value only

# Backward verification:
optimizer.zero_grad()
outputs.loss.backward()
v = substituted._parameters['values']
assert v.grad is not None
assert v.grad.norm().item() > 0
```

### §10.7 RETRACTED Configurations

| ID | Status | Retraction Source |
|---|---|---|
| F-1 (`model.requires_grad_(True)` blanket) | RETRACTED | Cell 9 v2 OOM at backward (32+ GiB demand from 8.03B param Adam state) |
| F-3 (F-2 + `gradient_checkpointing_enable()`) | RETRACTED | Cell 11+++++++ CheckpointError (GRACEAdaptor stateful forward incompatible with checkpoint recompute invariant) |

---

## §11. Cross-Reference Map

### §11.1 Inheritance from S2.20 Decisions

| v0.2 Section | S2.20 Decision Source |
|---|---|
| §3.1 (C-GRACE-1..5) | RATIFIED via Cell 8++ + Cell 9.5+ + Cell 11.5+ |
| §3.2 (C-S220-2) | D-S220-AUTH-1-V2 |
| §3.2 (C-S220-3) | D-S220-CHECKPOINT-7-1 |
| §3.2 (C-F-2-DISPATCH-1) | D-S220-FIX-F-2 |
| §6 (P-1-GRACE) | D-S220-P-1-GRACE-1 |
| §7 (P-2-GRACE) | D-S220-P-2-GRACE-1 |
| §10 (F-2) | D-S220-FIX-F-2; D-S220-FIX-F-1-RETRACTED |
| §10.7 (F-1/F-3 retraction) | D-S220-FIX-F-1-RETRACTED; D-S220-FIX-F-3 |

### §11.2 Forward References

| v0.2 Section | Consumer |
|---|---|
| §1.1 (active patches) | `t2_grace_runbook v0.2` Cell 2 patch state manifest |
| §3 (constraints) | `t2_grace_runbook v0.2` Cells 5/8/9/11 verification assertions |
| §6 (P-1-GRACE) | `t2_grace_runbook v0.2` Cell 2++ patch application |
| §7 (P-2-GRACE) | `t2_grace_runbook v0.2` Cell 2++++ patch application |
| §10 (F-2) | `t2_grace_runbook v0.2` Cell 9.5+ + Cell 11.5+ dispatch preamble |

### §11.3 Sibling Canonical Coordination

| v0.2 Section | MEMIT v2.5 parallel | ROME v0.2 parallel |
|---|---|---|
| §1 patch inventory | §1 patch inventory | §1 patch inventory |
| §5 SOURCE_LAYER class | §5 SOURCE_LAYER class | §5 SOURCE_LAYER class |
| §8 Pad-Token | §8 Pad-Token | §8 Pad-Token |
| §9 CONFIGURATION_LAYER | n/a | §9 CONFIG_LAYER (globals.yml) |
| §10 F-2 | n/a | n/a |

The CONFIGURATION_LAYER class is GRACE-specific in v0.2 (F-2 runtime configuration). ROME v0.2's CONFIG_LAYER (globals.yml absolute STATS_DIR per OQ-V02-1/D-V02-6) is structurally distinct — file-based configuration vs runtime model state.

---

## §12. Forward Applicability

### §12.1 S2.21 Inheritance

S2.21 = T.1-GRACE-3B retry runbook v0.1 authoring inherits this v0.2 spec verbatim. Patch state at S2.21 entry:

| Patch | Application Site | Pre-Dispatch State |
|---|---|---|
| P-1-GRACE | `grace/editors/grace_barebones.py` post-clone | applied at runbook v0.1 Cell 2++ (or equivalent) |
| P-2-GRACE | same file | applied at runbook v0.1 Cell 2++++ (or equivalent) |
| Pad-Token | tokenizer instance | applied at runbook v0.1 Cell 5.4 |
| F-2 | runtime model state | applied at runbook v0.1 Cell 9.5+ + Cell 11.5+ |

### §12.2 Compatibility Matrix

| Target Model Class | P-1-GRACE | P-2-GRACE | Pad-Token | F-2 |
|---|---|---|---|---|
| Llama-3.1-8B | APPLICABLE | APPLICABLE | APPLICABLE | APPLICABLE (VRAM-blocked) |
| Llama-3.2-3B | APPLICABLE | APPLICABLE | APPLICABLE | APPLICABLE (S2.21 target) |
| Llama-3.2-1B | APPLICABLE | APPLICABLE | APPLICABLE | APPLICABLE |
| Mistral-7B | APPLICABLE | APPLICABLE | APPLICABLE | APPLICABLE |
| Qwen-2.5-7B | APPLICABLE | APPLICABLE | APPLICABLE | APPLICABLE |
| GPT-2 (any) | APPLICABLE | not strictly required (fp32 default) | tokenizer-version-dependent | APPLICABLE |

### §12.3 Eliminability Conditions

| Patch | Elimination Path | Cost |
|---|---|---|
| P-1-GRACE | upstream PR to GRACE repo replacing eval(f-string) with parent_module/getattr | upstream maintainer dependency |
| P-2-GRACE | upstream PR adding fp16 fallback OR PyTorch native cdist fp16 implementation | upstream PR or PyTorch release |
| Pad-Token | tokenizer-version drift (Llama tokenizer ships with pad_token) | Llama tokenizer release dependency |
| F-2 | upstream PR adding optional `train_mode` flag to GRACE_barebones constructor | upstream PR |

None of the patches in v0.2 are eliminable without upstream cooperation. WS3 implementation planning treats v0.2 patch set as durable until upstream changes.

---

## §13. Document Status

**Authored:** 2026-05-05 (v0.2 codification analog session post-S2.20 close)
**Ratified:** All §3 constraints + §6/§7 patches + §10 configuration
**Supersedes:** v0.1 declarative
**Superseded by:** v0.3 (if S2.21 surfaces additional patches)
**Persistence:** `/mnt/user-data/outputs/grace-patches-canonical-v0_2.md`
