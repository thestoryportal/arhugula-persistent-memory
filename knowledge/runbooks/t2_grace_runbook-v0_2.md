# T.2 GRACE Runbook — v0.2

**Status:** EMPIRICALLY VALIDATED (S2.20 close + v0.2 codification)
**Supersedes:** v0.1 (declarative; 1489L; ratified 2026-05-05 at S2.19 close)
**Carry-forward target:** S2.21 = T.1-GRACE-3B retry runbook v0.1 authoring (structural template inheritance)
**Sibling siblings:** `stage_1_sect_runbook v1.7` (MEMIT-side), `t2_rome_runbook v0.2` (ROME-side)

---

## §0. Version History

| Version | Date | Status | Scope |
|---|---|---|---|
| v0.1 | 2026-05-05 | DECLARATIVE | Sibling-parity authoring at S2.19; 21 cells projected from t2_rome v0.2 inheritance |
| v0.2 | 2026-05-05 | EMPIRICALLY VALIDATED | S2.20 execution surfaced ~24 mid-session cell rewrites; canonical absorptions at Cells 0–13 |

### §0.1 v0.1 → v0.2 Diff Surface

| Cell | v0.1 disposition | v0.2 absorption |
|---|---|---|
| 0–0++ | declarative env preamble | RATIFIED (typing_extensions ≥4.13.0; rsync install required) |
| 1.5++ | declarative introspection | RATIFIED (GRACE_barebones API + Hydra config tree) |
| 2 | declarative patch state | EXTENDED — Cell 2++ (P-1-GRACE) + Cell 2++++ (P-2-GRACE) authoring sub-cells |
| 5 | declarative model load | EXTENDED — sub-cells 5++ schema discovery + 5+++++ assertion + 5++++++ combined gate |
| 6 | flat `fact["target_new"]` access | REWRITTEN — `fact["memit_request"]["target_new"]` + leading-space tokenization |
| 7 | unconditional probe iteration | REWRITTEN — linkage-conditional capture per D-S220-PROBE-LINKAGE-1 |
| 8 | truncated parent_module path | REWRITTEN — full path including target attribute name |
| 9 | base substitution + dispatch | REWRITTEN — F-2 preamble (post-instantiation `model.train()`); recovery preamble (Cell 9-- pattern) |
| 10 | declarative verdict surface | REWRITTEN — specificity adjudication corrected; environmental-ceiling routing path |
| 11 | parallel to Cell 9 | REWRITTEN — F-2 preamble inheritance |
| 11+ / 11++ | not in v0.1 | NEW — verdict integrity audit (load-bearing pre-Cell-13) |
| 12 | declarative L2 verdict | UNCHANGED schema; specificity adjudication absorbs Cell 10 correction |
| 13 | 3-route option matrix | EXTENDED — environmental-ceiling fourth route (Route A halt with conditional caveat) |
| 14–17 | Block C 15-trial loop | UNCHANGED — DECLARATIVE (untested at S2.20; no empirical absorption) |
| 18 | covariance cache integrity | REWRITTEN — filename schema corrected per A-S220-CELL18-1 |
| 19–20 | NV inventory + manifest | RATIFIED |

---

## §1. Inheritance Map

### §1.1 Structural Inheritance

```
Inheritance graph at v0.2:
═══════════════════════════════════════════════════════════════════
                stage_1_sect_runbook v1.7
                          │
                          │ structural template
                          ▼
                t2_rome_runbook v0.2
                          │
                          │ structural template
                          ▼
                t2_grace_runbook v0.2 ◄── (this document)
                          │
                          │ structural template (S2.21 inheritance)
                          ▼
                t1_grace_3b_runbook v0.1 (S2.21 target)
═══════════════════════════════════════════════════════════════════
```

### §1.2 Cell Decomposition

| Block | Cells | Purpose |
|---|---|---|
| Block A | 0–8 | Pre-flight environment + patch state + model load + dry-run gate |
| Block B | 9–13 | Single-edit dispatch + verdict surface + 3-route gate |
| Block C | 14–17 | 15-trial loop (verdict-conditional) |
| Block-end | 18–20 | NV inventory + mirror sync + manifest |

### §1.3 Specialist Routing

| Cells | Primary Specialist | Secondary |
|---|---|---|
| 0–4 | (none — system-level operations) | — |
| 5 | state-consistency-theorist | — |
| 6 | validation-contract-architect | — |
| 7 | validation-contract-architect | state-consistency-theorist |
| 8 | memit-specialist | state-consistency-theorist |
| 9, 11, 15 | memit-specialist | — |
| 10, 12, 13 | validation-contract-architect | memit-specialist |
| 14–17 | memit-specialist | validation-contract-architect |
| 18–20 | state-consistency-theorist | — |

---

## §2. Block A — Pre-Flight (Cells 0–8)

### §2.1 Cell 0 — System Preamble

**Purpose:** Install OS-level dependencies; configure HF cache directory; install GRACE Python dependencies.

**Cell body summary:**

```bash
apt-get install -y rsync     # required for /workspace mirror operations
pip install --upgrade typing_extensions>=4.13.0   # wandb chain dependency
pip install wandb            # GRACE optional logging dependency
mkdir -p /workspace/hf_cache
export HF_HOME=/workspace/hf_cache
```

**Acceptance:** rsync version printed; typing_extensions version ≥4.13.0; HF_HOME exported.

**Halt class:** apt-get failure → diagnose pod base image; pip failure → diagnose Python environment.

### §2.2 Cell 1 — GRACE Clone

**Purpose:** Clone upstream GRACE repository at pinned SHA.

**Cell body:**

```bash
cd /workspace
git clone https://github.com/MichaelLSY/grace.git grace_dry_run
cd grace_dry_run
git checkout f674183f17a995d109e10ee6140d4c3e6d016115
```

**Acceptance:** repo cloned; SHA matches `f674183f17a995d109e10ee6140d4c3e6d016115`.

**Halt class:** clone failure → check network egress; SHA mismatch → re-pin via fresh checkout.

### §2.3 Cell 1.5+ — Environment Fingerprint + Introspection

**Purpose:** Capture Python / torch / transformers / CUDA versions; introspect GRACE module structure.

**Cell body summary:** import inventory + `inspect.getsource()` on `GRACE_barebones.__init__` / `edit` / `GRACEAdaptor.__init__` / `GRACEAdaptor.forward`.

**Acceptance:** GRACE source extracted; key API signatures captured; Hydra config tree at `grace/config/` enumerated.

**Halt class:** import failure → investigate transformers version compatibility (5.x major-version drift surfaces).

### §2.4 Cell 2 — Patch State Manifest

**Purpose:** Initialize patch state manifest at `/workspace/architecture_profile/t2_grace_patch_state.json`. Cell 2++ + Cell 2++++ apply patches per `grace-patches-canonical v0.2 §6` + §7.

**Cell 2 cell body:**

```python
import json
from pathlib import Path

manifest = {
    "engine": "GRACE_barebones",
    "engine_sha": "f674183f17a995d109e10ee6140d4c3e6d016115",
    "patches_applied": {},
    "patches_authored_in_session": [],
    "patches_deferred_to_v0_2": [],
}

Path("/workspace/architecture_profile").mkdir(parents=True, exist_ok=True)
Path("/workspace/architecture_profile/t2_grace_patch_state.json").write_text(
    json.dumps(manifest, indent=2)
)
print("Cell 2 — patch state manifest initialized")
```

### §2.5 Cell 2++ — P-1-GRACE Application

**Purpose:** Apply P-1-GRACE source-layer patch per `grace-patches-canonical v0.2 §6`.

**Cell body:**

```python
import shutil, importlib, json, sys
from pathlib import Path

GRACE_BAREBONES = Path("/workspace/grace_dry_run/grace/grace/editors/grace_barebones.py")
PRISTINE = GRACE_BAREBONES.with_suffix(".py.upstream_pristine")

if not PRISTINE.exists():
    shutil.copy2(GRACE_BAREBONES, PRISTINE)

src = PRISTINE.read_text()
old_pattern = 'eval(f"self.model.{self.layer}")'
new_pattern = 'getattr(parent_module(self.model, self.layer), self.layer.rsplit(".", 1)[-1])'

n_occurrences = src.count(old_pattern)
assert n_occurrences == 9, f"Expected 9 sites; found {n_occurrences}"

lines = src.split("\n")
site_lines = [i + 1 for i, line in enumerate(lines) if old_pattern in line]
assert site_lines == [44, 53, 56, 57, 62, 76, 77, 78, 79]

src_patched = src.replace(old_pattern, new_pattern)
GRACE_BAREBONES.write_text(src_patched)

# Reload
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith("grace.editors"):
        del sys.modules[mod_name]
import grace.editors.grace_barebones
importlib.reload(grace.editors.grace_barebones)
from grace.editors.grace_barebones import GRACE_barebones, GRACEAdaptor

# Marker assertion
reload_src = GRACE_BAREBONES.read_text()
assert old_pattern not in reload_src
assert reload_src.count("parent_module(self.model, self.layer)") >= 9

# Manifest update
MANIFEST_PATH = Path("/workspace/architecture_profile/t2_grace_patch_state.json")
manifest = json.loads(MANIFEST_PATH.read_text())
manifest["patches_applied"]["P-1-GRACE"] = {
    "class": "SOURCE_LAYER",
    "site_count": 9,
    "site_line_numbers": [44, 53, 56, 57, 62, 76, 77, 78, 79],
    "v0_2_codified": True,
}
manifest["patches_authored_in_session"].append("P-1-GRACE")
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
print("Cell 2++ — P-1-GRACE applied; 9 sites")
```

### §2.6 Cell 2++++ — P-2-GRACE Application

**Purpose:** Apply P-2-GRACE source-layer patch per `grace-patches-canonical v0.2 §7`.

**Cell body:**

```python
GRACE_BAREBONES = Path("/workspace/grace_dry_run/grace/grace/editors/grace_barebones.py")
src = GRACE_BAREBONES.read_text()

old_line = "    return torch.cdist(key, query, p=2)"
new_block = """    # P-2-GRACE: torch.cdist lacks CUDA fp16 implementation; upcast for computation
    if key.dtype == torch.float16 or query.dtype == torch.float16:
        return torch.cdist(key.float(), query.float(), p=2).to(torch.float16)
    return torch.cdist(key, query, p=2)"""

assert src.count(old_line) == 1
src_patched = src.replace(old_line, new_block)
GRACE_BAREBONES.write_text(src_patched)

# Reload
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith("grace.editors"):
        del sys.modules[mod_name]
importlib.reload(grace.editors.grace_barebones)
from grace.editors.grace_barebones import GRACE_barebones, GRACEAdaptor

# Marker assertion
reload_src = GRACE_BAREBONES.read_text()
assert "P-2-GRACE" in reload_src
assert "key.dtype == torch.float16 or query.dtype == torch.float16" in reload_src

# Manifest update
manifest = json.loads(MANIFEST_PATH.read_text())
manifest["patches_applied"]["P-2-GRACE"] = {
    "class": "SOURCE_LAYER",
    "site_count": 1,
    "site_function": "euclidean_distance",
    "v0_2_codified": True,
}
manifest["patches_authored_in_session"].append("P-2-GRACE")
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
print("Cell 2++++ — P-2-GRACE applied")
```

### §2.7 Cell 3 — INAPPLICABLE-DEFERRED-BY-MECHANISM

**Purpose:** Structural placeholder per D-S219-CELL3-1; Cell 8 absorbs cell numbering offset relative to MEMIT/ROME runbooks.

**Cell body:** comment-only no-op.

### §2.8 Cell 4 — Primitive Hyperparameters

**Cell body:**

```python
# Layer-A and Layer-B candidates per D-S219-Q3-1 (calibration corridor)
GRACE_LAYER_A_PARAM = "model.layers.17.mlp.down_proj.weight"   # Layer-A
GRACE_LAYER_B_PARAM = "model.layers.2.mlp.down_proj.weight"    # Layer-B

# Canonical hparams (per t2_grace_runbook v0.1 + GRACE upstream defaults)
GRACE_INIT_EPSILON = 1.0
GRACE_EDIT_LR = 1.0
GRACE_DEVICE = "cuda"
GRACE_GENERATION = False
# n_iter=200 hard-coded in upstream grace_barebones.edit() per A-S220-CELL1-2
```

**Acceptance:** all parameters defined.

### §2.9 Cell 5 — Model Load + Pad-Token + Cross-Session Bit-Exact Gate

**Purpose:** Load Llama-class model at pinned revision SHA; apply Pad-Token alias (C-GRACE-4); execute cross-session bit-exact gate (C-S220-3).

**Cell body specification:**

#### §2.9.1 Sub-block 5.1 — Defensive preamble + HF token load

```python
import gc, json, os, torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

for var in ("model", "tokenizer", "editor"):
    if var in dir(): exec(f"del {var}")
gc.collect(); torch.cuda.empty_cache()

# 5.1.1 — HF token load with shape gate (C-S220-2)
HF_TOKEN_PATH = Path("/workspace/.hf_token")
hf_token = HF_TOKEN_PATH.read_text().strip()
assert hf_token.startswith("hf_") and len(hf_token) >= 37 and not any(c.isspace() for c in hf_token)
os.environ["HF_TOKEN"] = hf_token
os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token
```

#### §2.9.2 Sub-block 5.2 — Model load (revision-pinned; explicit token kwarg)

```python
MODEL_NAME = "<runbook-instance-target>"   # parameterized at session entry
MODEL_REVISION = "<sha-pinned-at-session-entry>"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, revision=MODEL_REVISION,
    torch_dtype=torch.float16, device_map="auto",
    token=hf_token,
).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION, token=hf_token)
```

#### §2.9.3 Sub-block 5.3 — Layer-set verification

```python
n_layer = model.config.num_hidden_layers
assert 0 <= 17 < n_layer  # Layer-A
assert 0 <= 2 < n_layer   # Layer-B
```

#### §2.9.4 Sub-block 5.4 — Pad-Token alias (C-GRACE-4)

```python
tokenizer.pad_token = tokenizer.eos_token
assert tokenizer.pad_token == tokenizer.eos_token
```

#### §2.9.5 Sub-block 5.5 — Cross-session bit-exact gate (C-S220-3)

Two-tier baseline schema consumption per A-S220-CELL5++-1:

```python
BASELINE_PATH = Path("/workspace/architecture_profile/<engine>_baselines.json")
baseline = json.loads(BASELINE_PATH.read_text())

assert baseline["model"] == MODEL_NAME
assert baseline["model_revision_sha"] == MODEL_REVISION

# Linkage-conditional bit-exact assertion
DRIFT_THRESHOLD = 1e-5   # rounding-class regime ceiling per D-S220-CHECKPOINT-7-1
drift_max_p_top_1 = 0.0
drift_max_p_target_new = 0.0
top_1_mismatches = []

for probe_id, captured in baseline["per_probe"].items():
    fact_id = captured.get("linked_fact_id")
    probe_text = captured["prompt"]
    
    input_ids = tokenizer(probe_text, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)
    
    captured_top_1_id = captured["top_5"][0]["token_id"]
    captured_p_top_1 = captured["p_top_1_pre"]
    live_top_1_id = int(probs.argmax().item())
    live_p_top_1 = probs.max().item()
    
    if captured_top_1_id != live_top_1_id:
        top_1_mismatches.append({"probe_id": probe_id})
    drift_max_p_top_1 = max(drift_max_p_top_1, abs(captured_p_top_1 - live_p_top_1))
    
    if fact_id is not None and "p_target_new_pre" in captured:
        target_new_id = baseline["target_ids_by_fact"][fact_id]["target_new_id"]
        live_p_target_new = probs[target_new_id].item()
        captured_p_target_new = captured["p_target_new_pre"]
        drift_max_p_target_new = max(drift_max_p_target_new, abs(captured_p_target_new - live_p_target_new))

# Combined gate adjudication (C-S220-3)
semantic_gate = (len(top_1_mismatches) == 0)
numeric_gate = (drift_max_p_top_1 < DRIFT_THRESHOLD and drift_max_p_target_new < DRIFT_THRESHOLD)
assert semantic_gate and numeric_gate
```

**Acceptance:** all 5.x sub-blocks PASS; cross-session checkpoint #N+1 ESTABLISHED.

**Halt classes:**

| Sub-block | Trigger | Disposition |
|---|---|---|
| 5.1.1 | Token shape invalid | HARD HALT — operator-side token acquisition |
| 5.2 | 401 GatedRepoError | HARD HALT — verify HF account license acceptance |
| 5.2 | OOM | HARD HALT — extend defensive preamble |
| 5.5 | Top-1 mismatch | HARD HALT — semantic determinism falsified |
| 5.5 | Drift `≥ 1e-5` | HARD HALT — environment delta exceeds rounding-class regime |

### §2.10 Cell 6 — Verdict Class Taxonomy + MULTI_TOKEN_ALLOWLIST

**Purpose:** Classify each fact in cfb-v3.yaml by verdict_class (STRICT_SINGLE_TOKEN / ALLOWLIST_FIRST_TOKEN_PROXY / MULTI_TOKEN_FAIL); apply leading-space tokenization convention (D-S220-TOKENIZATION-1).

**Cell body:**

```python
import yaml
from pathlib import Path

CFB_PATH = Path("/workspace/session_logs/archive/s2_13/cfb-v3.yaml")
cfb_v3_doc = yaml.safe_load(CFB_PATH.read_text())
cfb_facts = cfb_v3_doc["cfb_v3"]["facts"]

MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}   # harp under Llama tokenizer

def classify_fact(fact_id, target_new, tokenizer, allowlist):
    target_with_space = " " + target_new   # D-S220-TOKENIZATION-1
    token_ids = tokenizer.encode(target_with_space, add_special_tokens=False)
    if len(token_ids) == 1:
        return ("STRICT_SINGLE_TOKEN", token_ids[0], token_ids)
    if fact_id in allowlist:
        return ("ALLOWLIST_FIRST_TOKEN_PROXY", token_ids[0], token_ids)
    return ("MULTI_TOKEN_FAIL", None, token_ids)

# Pre-classification anchor verification
expected_fact_ids = set(baseline["target_ids_by_fact"].keys())
actual_fact_ids = set(f["id"] for f in cfb_facts)
assert expected_fact_ids == actual_fact_ids

# Per-fact classification (memit_request schema indirection)
fact_verdicts = {}
for fact in cfb_facts:
    fact_id = fact["id"]
    request = fact["memit_request"]
    target_new = request["target_new"]
    
    verdict_class, primary_token_id, full_token_ids = classify_fact(
        fact_id, target_new, tokenizer, MULTI_TOKEN_ALLOWLIST
    )
    fact_verdicts[fact_id] = {
        "verdict_class": verdict_class,
        "primary_token_id": primary_token_id,
        "full_token_ids": full_token_ids,
        "target_new": target_new,
        "subject": fact["subject"],
        "prompt_template": request["prompt"],
        "memit_request": request,
        "re_evaluate_at_trial_0": (verdict_class == "ALLOWLIST_FIRST_TOKEN_PROXY"),
    }
    if verdict_class == "MULTI_TOKEN_FAIL":
        raise RuntimeError(f"Cell 6 MULTI_TOKEN_FAIL: {fact_id}")

# Token ID cross-check vs baseline
for fact_id, vd in fact_verdicts.items():
    baseline_target_new_id = baseline["target_ids_by_fact"][fact_id]["target_new_id"]
    assert vd["primary_token_id"] == baseline_target_new_id
```

**Acceptance:** 5/5 facts classified; STRICT count + ALLOWLIST count + MULTI_TOKEN count = total; token ID cross-check 5/5 match.

**Halt classes:**

| Trigger | Disposition |
|---|---|
| KeyError on `memit_request` | corpus schema diverged |
| MULTI_TOKEN_FAIL on non-allowlist | HARD HALT per D-V12-MULTITOKEN-1 |
| Token ID cross-check FAIL | tokenizer drift between sessions |

### §2.11 Cell 7 — Pre-Edit Baseline Capture (Linkage-Aware)

**Purpose:** Capture pre-edit P-values against current model state; supersedes prior-session baseline as delta-computation reference frame.

**Cell body:**

```python
import torch, json, datetime
from pathlib import Path

PRE_EDIT_PATH = Path("/workspace/architecture_profile/t2_grace_pre_edit_baseline.json")

pre_edit_baseline = {
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "session": "<session-id>",
    "engine": "GRACE",
    "model": MODEL_NAME,
    "model_revision_sha": MODEL_REVISION,
    "purpose": "Pre-edit baseline; delta-computation reference frame",
    "per_probe": {},
}

linked_count = 0
unlinked_count = 0

for probe_id, captured in baseline["per_probe"].items():
    fact_id = captured.get("linked_fact_id")
    category = captured["category"]
    probe_text = captured["prompt"]
    
    input_ids = tokenizer(probe_text, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)
    
    entry = {
        "category": category,
        "linked_fact_id": fact_id,
        "prompt": probe_text,
        "p_top_1": probs.max().item(),
        "top_1_token_id": int(probs.argmax().item()),
    }
    if fact_id is not None:
        target_new_id = baseline["target_ids_by_fact"][fact_id]["target_new_id"]
        target_true_id = baseline["target_ids_by_fact"][fact_id]["target_true_id"]
        entry["p_target_new"] = probs[target_new_id].item()
        entry["p_target_true"] = probs[target_true_id].item()
        entry["verdict_class"] = fact_verdicts[fact_id]["verdict_class"]
        linked_count += 1
    else:
        entry["verdict_class"] = "shared_specificity"
        unlinked_count += 1
    pre_edit_baseline["per_probe"][probe_id] = entry

pre_edit_baseline["target_ids_by_fact"] = {
    fid: {**baseline["target_ids_by_fact"][fid], "verdict_class": fact_verdicts[fid]["verdict_class"]}
    for fid in fact_verdicts
}
pre_edit_baseline["probe_count_active"] = len(pre_edit_baseline["per_probe"])
pre_edit_baseline["probe_count_linked"] = linked_count
pre_edit_baseline["probe_count_shared_specificity"] = unlinked_count

PRE_EDIT_PATH.write_text(json.dumps(pre_edit_baseline, indent=2))
```

**Acceptance:** linked + shared_specificity = total; both counts non-zero (sanity-check linkage taxonomy populated).

### §2.12 Cell 8 — R1.3-Equivalent Dry-Run Gate

**Purpose:** Smoke-load `GRACE_barebones`; instantiate at Layer-A; verify C-GRACE-2/3/5-REVISED.

**Cell body:**

```python
import sys, torch, gc
sys.path.insert(0, "/workspace/grace_dry_run/grace")

from grace.editors.grace_barebones import GRACE_barebones, GRACEAdaptor
from grace.utils import parent_module, brackets_to_periods

SMOKE_PROBE = "The Eiffel Tower is in"
input_ids_smoke = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
with torch.no_grad():
    smoke_logits_pre_inst = model(input_ids_smoke).logits.cpu()

# Full-path parent_module argument (A-S220-CELL8-1)
LAYER_PATH = "model.layers.17.mlp.down_proj"
edit_module = parent_module(model, LAYER_PATH)
layer_name = LAYER_PATH.rsplit(".", 1)[-1]
original_layer = getattr(edit_module, layer_name)
assert type(original_layer).__name__ == "Linear"

editor = GRACE_barebones(
    model=model, layer=GRACE_LAYER_A_PARAM,
    init_epsilon=GRACE_INIT_EPSILON, learning_rate=GRACE_EDIT_LR,
    device=GRACE_DEVICE, generation=GRACE_GENERATION,
)
substituted = getattr(edit_module, layer_name)
assert type(substituted).__name__ == "GRACEAdaptor"   # identity-resilient
assert 'keys' not in substituted.__dict__              # C-GRACE-2

# C-GRACE-3 (within-session bit-exact)
with torch.no_grad():
    smoke_logits_post_inst = model(input_ids_smoke).logits.cpu()
drift_substitution = (smoke_logits_pre_inst.float() - smoke_logits_post_inst.float()).abs().max().item()
assert drift_substitution == 0.00e+00

# C-GRACE-5-REVISED (layer-restore unmount)
setattr(edit_module, layer_name, original_layer)
del editor
gc.collect(); torch.cuda.empty_cache()

with torch.no_grad():
    smoke_logits_post_unmount = model(input_ids_smoke).logits.cpu()
drift_unmount = (smoke_logits_pre_inst.float() - smoke_logits_post_unmount.float()).abs().max().item()
assert drift_unmount == 0.00e+00

restored_layer = getattr(edit_module, layer_name)
assert restored_layer is original_layer   # identity preservation
```

**Acceptance:** C-GRACE-2/3/5-REVISED all PASS (drift `0.00e+00`).

**Halt class:** any drift `> 0` → fall back to state_dict snapshot-restore (D-S219-Q4-1 option (c)); revise C-GRACE-5 at v0.3.

---

## §3. Block B — Single-Edit Dispatch + Verdict (Cells 9–13)

### §3.1 Cell 9 — Layer-A Single Edit Dispatch (F-2 Preamble)

**Purpose:** Single-fact GRACE edit at Layer-A on cfb-v3-001; verify edit installation; capture per-probe post-edit P-values.

**Cell body specification (F-2 preamble per `grace-patches-canonical v0.2 §10`):**

```python
import torch, gc, json, time
from pathlib import Path
from grace.editors.grace_barebones import GRACE_barebones, GRACEAdaptor
from grace.utils import parent_module

# 9.1 — Pre-edit smoke probe
SMOKE_PROBE = "The Eiffel Tower is in"
input_ids_smoke = tokenizer(SMOKE_PROBE, return_tensors="pt").input_ids.to(model.device)
with torch.no_grad():
    smoke_logits_pre_edit = model(input_ids_smoke).logits.cpu()

# 9.2 — State-check + capture original layer (recovery from stale GRACEAdaptor inline)
LAYER_PATH_A = "model.layers.17.mlp.down_proj"
edit_module_a = parent_module(model, LAYER_PATH_A)
layer_name_a = LAYER_PATH_A.rsplit(".", 1)[-1]
current = getattr(edit_module_a, layer_name_a)
if type(current).__name__ == "GRACEAdaptor":
    # In-line recovery via instance-attribute access (D-S220-LAYER-RESTORE-1)
    setattr(edit_module_a, layer_name_a, current.layer)
    gc.collect(); torch.cuda.empty_cache()
    current = getattr(edit_module_a, layer_name_a)
assert type(current).__name__ == "Linear"
original_layer_a = current

# 9.3 — Edit request construction
fact_id = "cfb-v3-001"   # IN-BAND anchor
vd = fact_verdicts[fact_id]
request = vd["memit_request"]
resolved_prompt = request["prompt"].format(request["subject"])
target_str = " " + vd["target_new"]   # D-S220-TOKENIZATION-1
target_id = vd["primary_token_id"]

# 9.4 — Tokenize labels-form
prompt_ids = tokenizer(resolved_prompt, return_tensors="pt").input_ids.to(model.device)
target_ids_tok = tokenizer(target_str, add_special_tokens=False, return_tensors="pt").input_ids.to(model.device)
assert target_ids_tok.shape == (1, 1)
input_ids_edit = torch.cat([prompt_ids, target_ids_tok], dim=1)
labels = torch.full_like(input_ids_edit, -100)
labels[0, -1] = target_id
attention_mask = torch.ones_like(input_ids_edit)
tokens = {"input_ids": input_ids_edit, "attention_mask": attention_mask, "labels": labels}

# 9.5 — Instantiate GRACE_barebones at Layer-A
editor = GRACE_barebones(
    model=model, layer=GRACE_LAYER_A_PARAM,
    init_epsilon=GRACE_INIT_EPSILON, learning_rate=GRACE_EDIT_LR,
    device=GRACE_DEVICE, generation=GRACE_GENERATION,
)
substituted = getattr(edit_module_a, layer_name_a)
assert type(substituted).__name__ == "GRACEAdaptor"
assert 'keys' not in substituted.__dict__

# 9.5+ — F-2 dispatch preamble (CANONICAL per grace-patches-canonical v0.2 §10)
model.train()
# DO NOT invoke model.requires_grad_(True) — F-1 RETRACTED
# DO NOT invoke gradient_checkpointing_enable() — F-3 INCOMPATIBLE

# 9.6 — Dispatch edit (n_iter=200 hard-coded; ~30-120s wall-time on RTX 4090)
t_start = time.time()
editor.edit(tokens)
t_edit = time.time() - t_start
n_keys = len(getattr(substituted, 'keys', torch.zeros(0))) if hasattr(substituted, 'keys') else 0

# 9.7 — Post-edit P-capture (linkage-aware per D-S220-PROBE-LINKAGE-1)
post_edit_a = {"per_probe": {}}
for probe_id, captured in baseline["per_probe"].items():
    fact_id_p = captured.get("linked_fact_id")
    category = captured["category"]
    probe_text = captured["prompt"]
    
    input_ids_p = tokenizer(probe_text, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = editor(input_ids=input_ids_p).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)
    
    entry = {
        "category": category, "linked_fact_id": fact_id_p,
        "p_top_1": probs.max().item(), "top_1_token_id": int(probs.argmax().item()),
    }
    if fact_id_p is not None:
        target_new_id = baseline["target_ids_by_fact"][fact_id_p]["target_new_id"]
        target_true_id = baseline["target_ids_by_fact"][fact_id_p]["target_true_id"]
        entry["p_target_new"] = probs[target_new_id].item()
        entry["p_target_true"] = probs[target_true_id].item()
    post_edit_a["per_probe"][probe_id] = entry

# 9.8 — Layer-restore unmount + drift verification
setattr(edit_module_a, layer_name_a, original_layer_a)
del editor
gc.collect(); torch.cuda.empty_cache()

with torch.no_grad():
    smoke_logits_post_unmount = model(input_ids_smoke).logits.cpu()
drift_unmount_a = (smoke_logits_pre_edit.float() - smoke_logits_post_unmount.float()).abs().max().item()
assert drift_unmount_a < 1e-4

# 9.9 — Persist
post_edit_a["meta"] = {
    "fact_id": fact_id, "layer": "L17", "edit_wall_time_sec": t_edit,
    "drift_unmount": drift_unmount_a, "codebook_size_post_edit": n_keys,
    "f_2_applied": True,
}
Path("/workspace/architecture_profile/t2_grace_post_edit_l17.json").write_text(
    json.dumps(post_edit_a, indent=2, default=str)
)

# 9.10 — Restore eval mode for downstream cells
model.eval()
```

**Acceptance:**

| Sub-block | Threshold |
|---|---|
| 9.4 | target tokenization shape `(1, 1)` |
| 9.5 | C-GRACE-2 satisfied |
| 9.6 | wall-time `> 30s` (forward + backward × 200 indicator); codebook_size = 1 |
| 9.7 | 38 probes captured |
| 9.8 | drift_unmount `< 1e-4` |

**Halt class:**

| Trigger | Disposition |
|---|---|
| 9.6 OOM | environmental ceiling — see §5.2 routing |
| 9.6 wall-time `< 20s` | F-2 ineffective; deeper investigation |
| 9.6 RuntimeError | NEW patch surface; investigate |
| 9.8 drift `≥ 1e-4` | C-GRACE-5-REVISED falsified; fall back to state_dict snapshot |

### §3.2 Cell 10 — Layer-A Verdict Surface

**Purpose:** Compute per-probe deltas; adjudicate calibration corridor; classify pathology if FAIL.

**Cell body specification:**

#### §3.2.1 Per-probe delta computation

```python
post_edit_a = json.loads(Path("/workspace/architecture_profile/t2_grace_post_edit_l17.json").read_text())

deltas = {}
for probe_id, post in post_edit_a["per_probe"].items():
    pre = pre_edit_baseline["per_probe"][probe_id]
    delta = {
        "category": post["category"], "linked_fact_id": post.get("linked_fact_id"),
        "p_top_1_pre": pre["p_top_1"], "p_top_1_post": post["p_top_1"],
        "p_top_1_drift": post["p_top_1"] - pre["p_top_1"],
        "top_1_token_id_pre": pre["top_1_token_id"],
        "top_1_token_id_post": post["top_1_token_id"],
        "top_1_changed": pre["top_1_token_id"] != post["top_1_token_id"],
    }
    if post.get("linked_fact_id") is not None and "p_target_new" in post:
        delta["p_target_new_pre"] = pre["p_target_new"]
        delta["p_target_new_post"] = post["p_target_new"]
        delta["p_target_new_lift"] = post["p_target_new"] - pre["p_target_new"]
    deltas[probe_id] = delta
```

#### §3.2.2 Calibration corridor verdict (Layer-A; per fact)

```python
fact_id = "cfb-v3-001"
cons_post = [
    deltas[pid]["p_target_new_post"]
    for pid, d in deltas.items()
    if d["category"] == "consistency" and d.get("linked_fact_id") == fact_id
]
gen_post = [
    deltas[pid]["p_target_new_post"]
    for pid, d in deltas.items()
    if d["category"] == "generalization" and d.get("linked_fact_id") == fact_id
]
spec_drifts = [
    abs(deltas[pid]["p_top_1_drift"])
    for pid, d in deltas.items()
    if d["category"] == "specificity"
]
spec_top_1_changes = [
    deltas[pid]["top_1_changed"]
    for pid, d in deltas.items()
    if d["category"] == "specificity"
]

# Adjudication (corrected serializer per OQ-S220-CELL10-1)
verdict = {
    "consistency": {"max": max(cons_post) if cons_post else 0.0, "pass": (max(cons_post) > 0.5) if cons_post else False},
    "generalization": {"max": max(gen_post) if gen_post else 0.0, "pass": (max(gen_post) > 0.3) if gen_post else False},
    "specificity": {
        "max_drift": max(spec_drifts) if spec_drifts else 0.0,
        "n_top_1_changes": sum(spec_top_1_changes),
        "pass": (
            (max(spec_drifts) < 0.05 and not any(spec_top_1_changes))
            if spec_drifts else True   # CORRECTED: empty list → PASS, not FAIL
        ),
    },
    "unmount": {
        "drift": post_edit_a["meta"]["drift_unmount"],
        "pass": post_edit_a["meta"]["drift_unmount"] < 1e-4,
    },
}
verdict["corridor_pass"] = all(v["pass"] for v in verdict.values())
```

#### §3.2.3 Pathology classification (if FAIL)

```python
if not verdict["corridor_pass"]:
    pathology = []
    if not verdict["consistency"]["pass"]:
        cons_above = sum(
            1 for pid, d in deltas.items()
            if d["category"] == "consistency"
            and d.get("linked_fact_id") == fact_id
            and d.get("p_target_new_lift", 0) > 0.05
        )
        n_cons = len(cons_post)
        pathology.append("GRACE-DISCRIMINATOR-NARROW" if cons_above < n_cons / 2 else "GRACE-VALUE-WEAK")
    if not verdict["generalization"]["pass"]: pathology.append("GENERALIZATION-FAIL")
    if not verdict["specificity"]["pass"]: pathology.append("SPECIFICITY-BLEED")
    if not verdict["unmount"]["pass"]: pathology.append("UNMOUNT-FAIL")
    verdict["pathology"] = pathology
```

**Acceptance:** verdict dict populated; corridor_pass + pathology recorded; persisted to JSON.

### §3.3 Cell 11 — Layer-B Single Edit Dispatch (F-2 Preamble)

**Purpose:** Parallel to Cell 9 with `GRACE_LAYER_B_PARAM`. Cell body inherits Cell 9 structure with layer substitution.

**Key differences from Cell 9:**

| Aspect | Cell 9 (Layer-A) | Cell 11 (Layer-B) |
|---|---|---|
| `LAYER_PATH` | `model.layers.17.mlp.down_proj` | `model.layers.2.mlp.down_proj` |
| `GRACE_LAYER_*_PARAM` | `GRACE_LAYER_A_PARAM` | `GRACE_LAYER_B_PARAM` |
| Output path | `t2_grace_post_edit_l17.json` | `t2_grace_post_edit_l2.json` |
| F-2 preamble | applied | applied |
| Pre-execution L17 verification | required (recovery if needed) | required (recovery if needed) |

### §3.4 Cell 11+ — Pre/Post Bit-Exact Cross-Check (NEW; Verdict Integrity Pre-Gate)

**Purpose:** Detect edit non-installation early; bit-exact identity between pre-edit and post-edit P-values forecloses installation hypothesis (per A-S220-CELL11-2).

**Cell body:**

```python
post_edit_a = json.loads(Path("/workspace/architecture_profile/t2_grace_post_edit_l17.json").read_text())
post_edit_b = json.loads(Path("/workspace/architecture_profile/t2_grace_post_edit_l2.json").read_text())

n_total = len(post_edit_a["per_probe"])
n_pre_eq_a = sum(
    1 for pid, post_a in post_edit_a["per_probe"].items()
    if post_a["p_top_1"] == pre_edit_baseline["per_probe"][pid]["p_top_1"]
)
n_pre_eq_b = sum(
    1 for pid, post_b in post_edit_b["per_probe"].items()
    if post_b["p_top_1"] == pre_edit_baseline["per_probe"][pid]["p_top_1"]
)

if n_pre_eq_a == n_total and n_pre_eq_b == n_total:
    verdict_integrity = "INSTALLATION_FALSIFIED"
    # Triggers Cell 11++ verdict integrity audit
elif n_pre_eq_a == n_total or n_pre_eq_b == n_total:
    verdict_integrity = "PARTIAL_INSTALLATION_FAILURE"
else:
    verdict_integrity = "INSTALLATION_LIKELY"
```

**Acceptance:** verdict_integrity = "INSTALLATION_LIKELY" → proceed to Cell 12; else → Cell 11++ audit.

### §3.5 Cell 11++ — Verdict Integrity Audit (NEW; Pre-Cell-13 Mandatory if Cell 11+ flags)

**Purpose:** Distinguish configuration defect (S-α: optimizer scope misalignment) from structural mechanism defect (S-β: gradient flow broken) per IC-S220-4.

**Cell body specification:** Per S2.20 Cell 11++ (~120 lines); validates `outputs.loss.requires_grad`, optimizer scope contains adapter values, gradient norm > 0 post-backward.

**Routing matrix:**

| Audit verdict | Cell 13 routing |
|---|---|
| S-α (optimizer scope) | Route C 3-trial preview after configuration fix |
| S-β (structural mechanism) | Route A halt — T.2 GRACE structurally eliminated |
| S-γ (compound) | Cell 11+++ deeper diagnostic |
| Config defect (e.g., model.eval()) | Apply F-2 fix; re-run Block B from Cell 9 |

### §3.6 Cell 12 — Layer-B Verdict Surface

**Purpose:** Parallel to Cell 10 against post_edit_b; cross-layer comparison surface.

**Cell body specification:** identical structure to Cell 10 with layer substitution. Adds cross-layer comparison sub-block:

```python
# Cross-layer pathology comparison
if not verdict_a["corridor_pass"] and not verdict_b["corridor_pass"]:
    pathology_distinct = set(verdict_a.get("pathology", [])) != set(verdict_b.get("pathology", []))
    verdict_b["cross_layer_pathology_distinct"] = pathology_distinct
```

### §3.7 Cell 13 — 3-Route Verdict Gate (Extended for Environmental Ceiling)

**Purpose:** Adjudicate forward routing per t_branch_decision_document v1.1 §5'.

**Routing matrix (extended):**

```
Cell 13 routing decision (4 routes including environmental):
═══════════════════════════════════════════════════════════════════
  Route B: Block C 15-trial loop authorized
    └── Layer-A OR Layer-B corridor PASS
  
  Route A (structural): T.2 GRACE structurally eliminated
    └── Both layers FAIL with diagnostic-distinct pathology
        AND replay-precedent risk LOW
        AND verdict integrity audit PASSES (S-β confirmed)
    └── S2.21 = T.1 alt-model under MEMIT (per t_branch §5'-α)
  
  Route C: 3-trial preview at PARTIAL layer
    └── Borderline verdicts; replay-precedent risk MEDIUM
  
  Route A (environmental; NEW at v0.2): T.2 GRACE NOT EXECUTABLE
    └── Edit dispatch raises OOM at backward pass (RTX 4090 ceiling)
        OR gradient checkpointing CheckpointError
        OR F-2 mechanism verified but VRAM exceeds ceiling
    └── S2.21 = smaller-model retry (T.1-GRACE-NB; ceiling disambiguation)
═══════════════════════════════════════════════════════════════════
```

**Cell body specification:**

```python
verdict_a = json.loads(Path("/workspace/architecture_profile/t2_grace_verdict_l17.json").read_text())
verdict_b = json.loads(Path("/workspace/architecture_profile/t2_grace_verdict_l2.json").read_text())

routing = {"session": "<session-id>", "captured_at": "<timestamp>"}

# Route adjudication
if any_layer_passed := (verdict_a["corridor_pass"] or verdict_b["corridor_pass"]):
    routing["route"] = "ROUTE_B_15_TRIAL"
    routing["block_c_layer"] = "L17" if verdict_a["corridor_pass"] else "L2"
elif environmental_ceiling := <detect_environmental_halt(verdict_a, verdict_b)>:
    routing["route"] = "ROUTE_A_HALT_ENVIRONMENT_CONDITIONAL"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "T.1-GRACE-3B retry runbook v0.1 authoring",
        "rationale": "Smaller model; environmental ceiling disambiguation",
    }
elif structural_elimination := <detect_structural_elim(verdict_a, verdict_b)>:
    routing["route"] = "ROUTE_A_HALT_STRUCTURAL"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "T.1 alt-model under MEMIT runbook v0.1 authoring",
        "rationale": "Structural mechanism elimination per t_branch §5'-α",
    }
else:
    routing["route"] = "ROUTE_C_3_TRIAL_PREVIEW"

Path("/workspace/architecture_profile/t2_grace_routing.json").write_text(
    json.dumps(routing, indent=2, default=str)
)
```

---

## §4. Block C — 15-Trial Loop (Cells 14–17; Verdict-Conditional)

### §4.1 Status

**DECLARATIVE.** Block C entered only on Route B verdict. v0.2 inherits v0.1 declarative form unchanged — no empirical absorption (S2.20 routed to Route A, bypassing Block C).

### §4.2 Forward Inheritance

S2.21 with smaller model may exercise Block C; v0.3 codification absorbs at that point.

---

## §5. Block-End — NV Inventory + Manifest (Cells 18–20)

### §5.1 Cell 18 — Covariance Cache Integrity Gate

**Schema correction per A-S220-CELL18-1:**

```python
COV_CACHE_DIR = Path("/workspace/covariance_caches/<model-name-keyed>/wikipedia_stats")
expected_files = [
    f"model.layers.{i}.mlp.down_proj_float32_mom2_t100_100000.npz"
    for i in <model-applicable-layer-set>
]
# Note: filename schema is `model.layers.N.*_mom2_t100_*` (NOT `layers.N.*_mom2_*`)
# Note: GRACE adapter mechanism does NOT consume these caches; verification only
```

**Acceptance:** all expected files present; SHA prefixes recorded for cross-session forensic.

### §5.2 Cell 19 — NV Utilization

**Cell body:** `du -sh /workspace` + `df -BG /workspace`; report workspace size + NV utilization + headroom.

### §5.3 Cell 20 — Reproducibility Manifest Extension

**Cell body:** read manifest → add session entry → write back. Session entry schema:

```python
manifest["sessions"]["<session-id>"] = {
    "session_label": "...",
    "captured_at": "...",
    "model": MODEL_NAME, "model_revision_sha": MODEL_REVISION,
    "engine": "GRACE_barebones (SHA <engine-sha>)",
    "patches_applied": ["P-1-GRACE", "P-2-GRACE"],
    "verdict": "<route>",
    "successor": "<S.N+1 scope>",
    "outputs": [<list-of-NV-paths>],
    "cross_session_checkpoint": {...},
}
```

---

## §6. Process Constraints (Inherited + NEW)

### §6.1 Inherited from v0.1

| ID | Statement |
|---|---|
| C-GRACE-1..5 | per `grace-patches-canonical v0.2 §3.1` |

### §6.2 NEW at v0.2

| ID | Statement | Verification Site |
|---|---|---|
| C-S220-2 | HF token shape gate | Cell 5.1.1 |
| C-S220-3 | Cross-session combined gate | Cell 5.5 |
| C-F-2-DISPATCH-1 | F-2 dispatch preamble (model.train() only) | Cell 9.5+ + Cell 11.5+ |
| C-PRE-DISPATCH-STATE-1 | Substitution site Linear at entry | Cell 9.2 + Cell 11.2 |
| C-PRE-DISPATCH-AUDIT-1 | Cell 11+ + Cell 11++ unconditional pre-Cell-13 | Cell 11+ + Cell 11++ |
| C-S220-PATCH-AUTHORING-1 | Single-line replacement form | Cell 2++ + Cell 2++++ |
| C-S220-CELL-HYGIENE-1 | try/finally for substitution-site cells | All Cell 11+++ derivatives |

---

## §7. Verdict Surface Taxonomy

### §7.1 Calibration Corridor PASS Criteria

| Criterion | Threshold |
|---|---|
| Consistency | `max(cons_p_target_new) > 0.5` |
| Generalization | `max(gen_p_target_new) > 0.3` |
| Specificity | `max(abs(p_top_1_drift)) < 0.05` AND no top_1_changes; empty list → PASS |
| Unmount | `drift < 1e-4` |

### §7.2 Pathology Classes

| Class | Signature |
|---|---|
| GRACE-DISCRIMINATOR-NARROW | < half cons probes route to value (P at pre-edit on >50% of cons) |
| GRACE-VALUE-WEAK | most cons probes route to value but P_target_new modest (0.1–0.5) |
| GRACE-NON-CONVERGENT | (untestable post-S2.20 — `editor.losses` empty by upstream design) |
| GRACE-INSTRUMENTAL-FAIL | empty-codebook substitution drift > 0 |
| GENERALIZATION-FAIL | `max(gen_p_target_new) ≤ 0.3` |
| SPECIFICITY-BLEED | spec drift `≥ 0.05` OR top_1 changes |
| UNMOUNT-FAIL | drift_unmount `≥ 1e-4` |
| ENVIRONMENTAL-CEILING (NEW) | OOM OR gradient checkpointing CheckpointError; mechanism untested |

### §7.3 Cross-Layer Verdict Logic

| Layer-A | Layer-B | Verdict |
|---|---|---|
| PASS | * | Block C at Layer-A |
| FAIL | PASS | Block C at Layer-B |
| FAIL | FAIL (same pathology) | Route A halt (structural) |
| FAIL | FAIL (distinct pathology + replay-risk LOW) | Route A halt (structural) |
| FAIL | FAIL (distinct pathology + replay-risk MEDIUM) | Route C 3-trial preview |
| ENV_CEILING | ENV_CEILING | Route A halt (environmental) |

---

## §8. Forward Routing

### §8.1 Successor Session Determination

| S.N verdict | S.N+1 scope |
|---|---|
| Route B (Block C entry) | continued Block C execution + final adjudication at session close |
| Route A (structural) | T.1 alt-model under MEMIT runbook v0.1 authoring |
| Route A (environmental) | T.1-GRACE-NB retry runbook v0.1 authoring (smaller model) |
| Route C | 3-trial preview within current session OR successor session |

### §8.2 Carry-Forward Anchors for S2.21

| Anchor | Status |
|---|---|
| Cross-session bit-exact determinism (checkpoint #N+1) | extends per D-S220-CHECKPOINT-7-1 |
| Patches `{P-1-GRACE, P-2-GRACE}` | inherited verbatim |
| F-2 dispatch preamble | inherited verbatim |
| pre_edit_baseline reference frame | NOT carried across model classes (Llama-3.2-3B requires fresh capture) |
| cfb-v3.yaml v1.0 corpus | inherited verbatim |
| probe-set-v3.yaml v1.0 | inherited verbatim |

---

## §9. Document Status

**Authored:** 2026-05-05 (v0.2 codification analog session post-S2.20 close)
**Ratified:** Cells 0–13 + 18–20 (Block C unchanged from v0.1 declarative)
**Supersedes:** v0.1 declarative
**Superseded by:** v0.3 (if S2.21 surfaces additional cell corrections or Block C empirical absorption)
**Persistence:** `/mnt/user-data/outputs/t2_grace_runbook-v0_2.md`
