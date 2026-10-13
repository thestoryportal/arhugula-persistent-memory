# T.1-GRACE-3B Runbook — v0.1

**Status:** DECLARATIVE (S2.21 authoring 2026-05-05; pre-empirical)
**Supersedes:** none — NEW runbook
**Carry-forward target:** S2.22 = T.1-GRACE-3B execution session (Llama-3.2-3B)
**Sibling siblings:** `t2_grace_runbook v0.2` (DIRECT structural template), `t2_rome_runbook v0.2`, `stage_1_sect_runbook v1.7`
**Engine:** `GRACE_barebones` (upstream SHA `f674183f17a995d109e10ee6140d4c3e6d016115` + P-1-GRACE + P-2-GRACE)
**Model:** `meta-llama/Llama-3.2-3B` (revision SHA TBD; resolved at S2.22 Cell 5 entry per C-S221-1)
**Hardware:** RunPod RTX 4090 24 GiB, NV-backed
**Routing source:** D-S220-S221-ROUTING-1

---

## §0. Version History

| Version | Date | Status | Scope |
|---|---|---|---|
| v0.1 | 2026-05-05 | DECLARATIVE | Sibling-parity authoring at S2.21; structural template inheritance from t2_grace_runbook v0.2; model-class swap to Llama-3.2-3B; pre-empirical |

### §0.1 Authoring Posture

v0.1 is DECLARATIVE pending S2.22 execution. v0.2 codification absorbs S2.22 mid-session corrections per the precedent established by:
- `stage_1_sect_runbook v1.5 → v1.6 → v1.7` (MEMIT-side)
- `t2_rome_runbook v0.1 → v0.2` (ROME-side)
- `t2_grace_runbook v0.1 → v0.2` (GRACE-side, S2.20 absorption)

This authoring discipline anticipates ~10–24 mid-session cell rewrites; structural template forms are minimum-viable specifications, not validated cell bodies.

---

## §1. Inheritance Map

### §1.1 Structural Inheritance Graph

```
Inheritance lineage at v0.1:
═══════════════════════════════════════════════════════════════════
                stage_1_sect_runbook v1.7
                          │
                          │ structural template
                          ▼
                t2_rome_runbook v0.2
                          │
                          │ structural template
                          ▼
                t2_grace_runbook v0.2 (DIRECT structural template)
                          │
                          │ structural template (S2.21 inheritance)
                          ▼
                t1_grace_3b_runbook v0.1 ◄── (this document)
═══════════════════════════════════════════════════════════════════
```

### §1.2 Cell Decomposition (Inherited from v0.2)

| Block | Cells | Purpose |
|---|---|---|
| Block A | 0–8 | Pre-flight environment + patch state + model load + dry-run gate |
| Block B | 9–13 | Single-edit dispatch + verdict surface + 4-route gate (extended) |
| Block C | 14–17 | 15-trial loop (verdict-conditional; declarative) |
| Block-end | 18–20 | NV inventory + mirror sync + manifest |

### §1.3 Cell Delta Map (vs t2_grace_runbook v0.2)

| Cell | Delta Class | Rationale |
|---|---|---|
| 0–4 | structural inheritance verbatim | OS/clone/patch/hparam preamble unchanged |
| 5 | REWRITTEN — fresh baseline capture | Llama-3.2-3B model class differs from Llama-3.1-8B; no cross-session anchor at first execution |
| 6 | RE-VERIFIED — Llama-3.2 tokenizer behavior | Tokenizer family continuity not assumed; verification gate at S2.22 |
| 7 | structural inheritance; fresh values | Pre-edit baseline against fresh Cell 5 reference frame |
| 8 | RE-VERIFIED — `Linear(8192, 3072)` | down_proj shape changes with hidden_size and intermediate_size |
| 9 | structural inheritance verbatim | F-2 dispatch preamble + recovery preamble unchanged |
| 10 | structural inheritance verbatim | Verdict adjudication + corrected serializer unchanged |
| 11 | structural inheritance verbatim | Layer-B parallel to Cell 9 unchanged |
| 11+ / 11++ | structural inheritance verbatim | Verdict integrity audit pre-Cell-13 unchanged |
| 12 | structural inheritance verbatim | Layer-B verdict surface unchanged |
| 13 | EXTENDED — T.1-GRACE-3B outcome routing matrix | 3 routes mapped to v1.2 disposition + v1.3 amendment scope |
| 14–17 | DECLARATIVE inheritance | Block C untested precedent (S2.20 routed Route A; S2.22 may exercise) |
| 18 | INAPPLICABLE per §6.3 | No covariance caches for Llama-3.2-3B; GRACE adapter mechanism does not consume caches |
| 19–20 | structural inheritance | NV inventory + manifest unchanged |

### §1.4 Specialist Routing (Inherited from v0.2 §1.3)

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

### §1.5 Substring Substitution Convention (Verbatim Cells)

For all cells classified as "structural inheritance verbatim" in §1.3, the cell body is the corresponding cell body in `t2_grace_runbook v0.2` with the following substring substitutions:

| Substitution | Pattern |
|---|---|
| Model name | `meta-llama/Llama-3.1-8B` → `meta-llama/Llama-3.2-3B` |
| Revision SHA | `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` → `<TBD; resolved at S2.22 Cell 5 entry>` |
| Baseline path | `*_baselines.json` keyed on model name |
| Output path prefix | `t2_grace_*` → `t1_grace_3b_*` |
| Verdict path | `t2_grace_post_edit_l*.json` → `t1_grace_3b_post_edit_l*.json` |
| Routing path | `t2_grace_routing.json` → `t1_grace_3b_routing.json` |
| Layer paths | UNCHANGED (`model.layers.17.mlp.down_proj` / `model.layers.2.mlp.down_proj`) |
| Output base directory | UNCHANGED (`/workspace/architecture_profile/`) |

---

## §2. Block A — Pre-Flight (Cells 0–8)

### §2.1 Cell 0 — System Preamble

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.1`.

**Cell body:**

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

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.2`.

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

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.3`.

**Purpose:** Capture Python / torch / transformers / CUDA versions; introspect GRACE module structure.

**Cell body summary:** import inventory + `inspect.getsource()` on `GRACE_barebones.__init__` / `edit` / `GRACEAdaptor.__init__` / `GRACEAdaptor.forward`.

**Acceptance:** GRACE source extracted; key API signatures captured; Hydra config tree at `grace/config/` enumerated.

**Halt class:** import failure → investigate transformers version compatibility (5.x major-version drift surfaces).

### §2.4 Cell 2 — Patch State Manifest

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.4` with output filename substitution.

**Cell body:**

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
Path("/workspace/architecture_profile/t1_grace_3b_patch_state.json").write_text(
    json.dumps(manifest, indent=2)
)
print("Cell 2 — patch state manifest initialized")
```

### §2.5 Cell 2++ — P-1-GRACE Application

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.5` with output filename substitution.

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
MANIFEST_PATH = Path("/workspace/architecture_profile/t1_grace_3b_patch_state.json")
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

**Acceptance:** 9 sites detected at expected line numbers; marker assertion PASS; manifest updated.

**Halt class:**

| Trigger | Disposition |
|---|---|
| Site count ≠ 9 | upstream GRACE SHA drift; investigate Cell 1 |
| Site lines mismatch | upstream code rearrangement; investigate |
| Marker assertion FAIL | reload chain incomplete; restart Python kernel |

### §2.6 Cell 2++++ — P-2-GRACE Application

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.6` with output filename substitution.

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

**Acceptance:** single-site replacement; marker assertion PASS; manifest updated.

### §2.7 Cell 3 — INAPPLICABLE-DEFERRED-BY-MECHANISM

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.7`.

**Purpose:** Structural placeholder per D-S219-CELL3-1; Cell 8 absorbs cell numbering offset relative to MEMIT/ROME runbooks.

**Cell body:** comment-only no-op.

```python
# Cell 3 — INAPPLICABLE-DEFERRED-BY-MECHANISM
# GRACE adapter mechanism does not consume layer_stats covariance caches.
# Cell numbering preserved for parity with stage_1_sect_runbook (MEMIT-side).
# Cell 8 absorbs the structural offset.
```

### §2.8 Cell 4 — Primitive Hyperparameters

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §2.8` per kickoff §6.4.

**Cell body:**

```python
# Layer-A and Layer-B candidates per D-S219-Q3-1 (calibration corridor)
# Layer paths UNCHANGED — both indices valid on Llama-3.2-3B (n_layer = 28)
# L17 relative depth 60.7% (vs 53.1% on 8B; +7.6%); L2 shallow
GRACE_LAYER_A_PARAM = "model.layers.17.mlp.down_proj.weight"   # Layer-A
GRACE_LAYER_B_PARAM = "model.layers.2.mlp.down_proj.weight"    # Layer-B

# Canonical hparams (per t2_grace_runbook v0.2 + GRACE upstream defaults)
GRACE_INIT_EPSILON = 1.0
GRACE_EDIT_LR = 1.0
GRACE_DEVICE = "cuda"
GRACE_GENERATION = False
# n_iter=200 hard-coded in upstream grace_barebones.edit() per A-S220-CELL1-2
```

**Acceptance:** all parameters defined.

### §2.9 Cell 5 — REWRITTEN — Fresh Baseline Capture

**Inheritance:** REWRITTEN per kickoff §5.2 + §6.2.

**Purpose:** Load `meta-llama/Llama-3.2-3B` at pinned revision SHA; apply Pad-Token alias (C-GRACE-4); execute fresh baseline capture (no cross-session anchor; first execution on this model class). Capture establishes Llama-3.2-3B chain Checkpoint #1 per D-S221-CHECKPOINT-1-1.

**Rationale for rewrite:** S2.20 cross-session bit-exact gate (C-S220-3) consumes a prior-session baseline as reference. T.1-GRACE-3B is the first execution on Llama-3.2-3B; no prior baseline exists. Cell 5.5 inverts from gate-consumer to baseline-producer, with C-S220-3 deferred to Checkpoint #2 at S2.23+ if T.1-GRACE-3B execution recurs.

#### §2.9.1 Sub-block 5.1 — Defensive preamble + HF token load

```python
import gc, json, os, torch, datetime
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

for var in ("model", "tokenizer", "editor"):
    if var in dir(): exec(f"del {var}")
gc.collect(); torch.cuda.empty_cache()

# 5.1.1 — HF token load with shape gate (C-S220-2 carry-forward)
HF_TOKEN_PATH = Path("/workspace/.hf_token")
hf_token = HF_TOKEN_PATH.read_text().strip()
assert hf_token.startswith("hf_") and len(hf_token) >= 37 and not any(c.isspace() for c in hf_token)
os.environ["HF_TOKEN"] = hf_token
os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token
```

#### §2.9.2 Sub-block 5.2 — Model load (revision-pinned; explicit token kwarg)

```python
MODEL_NAME = "meta-llama/Llama-3.2-3B"
MODEL_REVISION = "<TBD; resolved at S2.22 Cell 5 entry per C-S221-1>"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, revision=MODEL_REVISION,
    torch_dtype=torch.float16, device_map="auto",
    token=hf_token,
).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION, token=hf_token)
```

**Halt class:** 401 GatedRepoError → operator must accept Llama-3.2 license at HF account level; OOM at load → unexpected (model is 6.42 GiB fp16); investigate environment delta.

#### §2.9.3 Sub-block 5.3 — Layer-set verification (C-S221-LAYER-VALIDITY)

```python
n_layer = model.config.num_hidden_layers
assert n_layer == 28, f"Expected n_layer=28 for Llama-3.2-3B; got {n_layer}"
assert 0 <= 17 < n_layer  # Layer-A valid
assert 0 <= 2 < n_layer   # Layer-B valid

# Architecture cross-check
assert model.config.hidden_size == 3072
assert model.config.intermediate_size == 8192
```

#### §2.9.4 Sub-block 5.4 — Pad-Token alias (C-GRACE-4 carry-forward)

```python
tokenizer.pad_token = tokenizer.eos_token
assert tokenizer.pad_token == tokenizer.eos_token
```

#### §2.9.5 Sub-block 5.5 — Fresh baseline capture (FRESH; no cross-session gate consumption)

Two-tier baseline schema per A-S220-CELL5++-1. Captures BOTH per-fact target IDs AND per-probe P-values for downstream linkage-conditional cells.

```python
import yaml

# Load corpus + probe set for fact/probe ID enumeration
CFB_PATH = Path("/workspace/session_logs/archive/s2_13/cfb-v3.yaml")  # OQ-S220-CFB-PATH-1 inheritance
PROBE_PATH = Path("/workspace/session_logs/archive/s2_13/probe-set-v3.yaml")
cfb_v3_doc = yaml.safe_load(CFB_PATH.read_text())
probe_doc = yaml.safe_load(PROBE_PATH.read_text())
cfb_facts = cfb_v3_doc["cfb_v3"]["facts"]
probes = probe_doc["probe_set_v3"]["probes"]

baseline = {
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "session": "S2.22",
    "engine": "GRACE_barebones",
    "model": MODEL_NAME,
    "model_revision_sha": MODEL_REVISION,
    "purpose": "Fresh baseline capture; Llama-3.2-3B chain checkpoint #1",
    "n_layer": n_layer,
    "hidden_size": model.config.hidden_size,
    "intermediate_size": model.config.intermediate_size,
    "target_ids_by_fact": {},
    "per_probe": {},
}

# Per-fact target ID resolution (D-S220-TOKENIZATION-1: leading-space prefix)
for fact in cfb_facts:
    fact_id = fact["id"]
    request = fact["memit_request"]
    target_new_with_space = " " + request["target_new"]
    target_true_with_space = " " + request["target_true"]
    target_new_ids = tokenizer.encode(target_new_with_space, add_special_tokens=False)
    target_true_ids = tokenizer.encode(target_true_with_space, add_special_tokens=False)
    baseline["target_ids_by_fact"][fact_id] = {
        "target_new": request["target_new"],
        "target_new_id": target_new_ids[0],   # primary token
        "target_new_full_ids": target_new_ids,
        "target_true": request["target_true"],
        "target_true_id": target_true_ids[0],
        "subject": fact["subject"],
    }

# Per-probe P-value capture (linkage-aware per D-S220-PROBE-LINKAGE-1)
for probe in probes:
    probe_id = probe["id"]
    probe_text = probe["prompt"]
    fact_id = probe.get("linked_fact_id")  # None for shared_specificity
    category = probe["category"]

    input_ids = tokenizer(probe_text, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    probs = torch.softmax(logits, dim=-1)

    # Top-5 capture for forensic + reproducibility manifest extension
    top_5_p, top_5_id = torch.topk(probs, 5)
    entry = {
        "category": category,
        "linked_fact_id": fact_id,
        "prompt": probe_text,
        "p_top_1_pre": probs.max().item(),
        "top_1_token_id": int(probs.argmax().item()),
        "top_5": [
            {"token_id": int(tid.item()), "p": float(tp.item()), "token_str": tokenizer.decode([int(tid.item())])}
            for tid, tp in zip(top_5_id, top_5_p)
        ],
    }
    if fact_id is not None:
        target_new_id = baseline["target_ids_by_fact"][fact_id]["target_new_id"]
        target_true_id = baseline["target_ids_by_fact"][fact_id]["target_true_id"]
        entry["p_target_new_pre"] = probs[target_new_id].item()
        entry["p_target_true_pre"] = probs[target_true_id].item()
    baseline["per_probe"][probe_id] = entry

baseline["probe_count_total"] = len(baseline["per_probe"])
baseline["probe_count_linked"] = sum(1 for e in baseline["per_probe"].values() if e["linked_fact_id"] is not None)
baseline["probe_count_shared_specificity"] = baseline["probe_count_total"] - baseline["probe_count_linked"]
```

#### §2.9.6 Sub-block 5.6 — Persist baseline + manifest extension

```python
BASELINE_PATH = Path("/workspace/architecture_profile/llama_3_2_3b_baselines.json")
BASELINE_PATH.write_text(json.dumps(baseline, indent=2))

# Manifest extension — Llama-3.2-3B chain checkpoint #1
MANIFEST_PATH = Path("/workspace/architecture_profile/reproducibility_manifest.json")
manifest = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {"sessions": {}}
manifest["sessions"]["S2.22-CHECKPOINT-1"] = {
    "session_label": "S2.22 Cell 5 — Llama-3.2-3B fresh baseline capture",
    "captured_at": baseline["captured_at"],
    "model": MODEL_NAME,
    "model_revision_sha": MODEL_REVISION,
    "engine": "GRACE_barebones (SHA f674183f)",
    "model_class_chain": "llama_3_2_3b",
    "checkpoint_index_within_chain": 1,
    "purpose": "First execution on Llama-3.2-3B; Llama-3.1-8B chain (#1–#7) NOT carry-forward",
    "outputs": [str(BASELINE_PATH)],
}
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
```

**Acceptance:**

| Sub-block | Threshold |
|---|---|
| 5.1.1 | Token shape valid |
| 5.2 | Model loaded; tokenizer loaded |
| 5.3 | n_layer = 28; hidden_size = 3072; intermediate_size = 8192 |
| 5.4 | pad_token = eos_token |
| 5.5 | linked + shared_specificity = total; both counts non-zero |
| 5.6 | baseline persisted; manifest extension written |

**Halt classes:**

| Sub-block | Trigger | Disposition |
|---|---|---|
| 5.1.1 | Token shape invalid | HARD HALT — operator-side token acquisition |
| 5.2 | 401 GatedRepoError | HARD HALT — verify HF account license acceptance for Llama-3.2 |
| 5.3 | n_layer mismatch | HARD HALT — wrong model variant resolved |
| 5.5 | Tokenization yields multi-token target on non-allowlist fact | HARD HALT — defer to Cell 6 MULTI_TOKEN classification |

**Note on cross-session bit-exact:** No comparison gate at S2.22 Cell 5. Future S2.23+ T.1-GRACE-3B re-executions will consume `llama_3_2_3b_baselines.json` as the cross-session reference frame, applying C-S220-3 combined gate (top-1 strict equality + drift `< 1e-5`) at that point.

### §2.10 Cell 6 — RE-VERIFIED — Llama-3.2 Tokenizer + MULTI_TOKEN_ALLOWLIST

**Inheritance:** RE-VERIFIED per kickoff §6.2; structural form from `t2_grace_runbook v0.2 §2.10`; tokenizer behavior NOT carry-forward.

**Purpose:** Classify each fact in cfb-v3.yaml by verdict_class (STRICT_SINGLE_TOKEN / ALLOWLIST_FIRST_TOKEN_PROXY / MULTI_TOKEN_FAIL); apply leading-space tokenization convention (D-S220-TOKENIZATION-1); verify Llama-3.2 tokenizer continuity vs Llama-3.1 (anticipated parity per shared Llama-3 tokenizer family; OQ-S221-1).

**Rationale for re-verification:** Llama-3.2 tokenizer is documented as Llama-3 family but tokenizer parity is not assumed structurally. Cell 6 produces empirical verification at S2.22 entry. If parity holds, ALLOWLIST inheritance from S2.20 (`{"cfb-v3-004"}`) carries forward; if divergent, allowlist is reconstructed.

**Cell body:**

```python
import yaml
from pathlib import Path

CFB_PATH = Path("/workspace/session_logs/archive/s2_13/cfb-v3.yaml")
cfb_v3_doc = yaml.safe_load(CFB_PATH.read_text())
cfb_facts = cfb_v3_doc["cfb_v3"]["facts"]

# Inherited from S2.20 t2_grace_runbook v0.2 §2.10; verified at Cell 6 against Llama-3.2 tokenizer
MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}   # harp under Llama-3.1 tokenizer; verified for Llama-3.2

def classify_fact(fact_id, target_new, tokenizer, allowlist):
    target_with_space = " " + target_new   # D-S220-TOKENIZATION-1
    token_ids = tokenizer.encode(target_with_space, add_special_tokens=False)
    if len(token_ids) == 1:
        return ("STRICT_SINGLE_TOKEN", token_ids[0], token_ids)
    if fact_id in allowlist:
        return ("ALLOWLIST_FIRST_TOKEN_PROXY", token_ids[0], token_ids)
    return ("MULTI_TOKEN_FAIL", None, token_ids)

# Pre-classification anchor verification (against fresh baseline)
expected_fact_ids = set(baseline["target_ids_by_fact"].keys())
actual_fact_ids = set(f["id"] for f in cfb_facts)
assert expected_fact_ids == actual_fact_ids

# Per-fact classification (memit_request schema indirection)
fact_verdicts = {}
classification_summary = {"STRICT_SINGLE_TOKEN": 0, "ALLOWLIST_FIRST_TOKEN_PROXY": 0, "MULTI_TOKEN_FAIL": 0}
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
    classification_summary[verdict_class] += 1
    if verdict_class == "MULTI_TOKEN_FAIL":
        raise RuntimeError(f"Cell 6 MULTI_TOKEN_FAIL: {fact_id}")

# Token ID cross-check vs baseline (Cell 5.5 capture)
for fact_id, vd in fact_verdicts.items():
    baseline_target_new_id = baseline["target_ids_by_fact"][fact_id]["target_new_id"]
    assert vd["primary_token_id"] == baseline_target_new_id, (
        f"Token ID drift: Cell 6 classification {vd['primary_token_id']} != "
        f"Cell 5.5 baseline {baseline_target_new_id} on {fact_id}"
    )

# Tokenizer continuity diagnostic (informational; OQ-S221-1 closure)
print(f"Cell 6 — Llama-3.2 classification summary: {classification_summary}")
print(f"  STRICT_SINGLE_TOKEN: {classification_summary['STRICT_SINGLE_TOKEN']}")
print(f"  ALLOWLIST_FIRST_TOKEN_PROXY: {classification_summary['ALLOWLIST_FIRST_TOKEN_PROXY']}")
print(f"  Total verified against baseline: {len(fact_verdicts)}")
```

**Acceptance:**

| Threshold | Expected (anticipated parity) |
|---|---|
| Total facts classified | 5/5 |
| MULTI_TOKEN_FAIL count | 0 |
| Token ID cross-check | 5/5 match against baseline |
| Llama-3.2 vs Llama-3.1 allowlist parity | confirmed (`{"cfb-v3-004"}`) |

**Halt classes:**

| Trigger | Disposition |
|---|---|
| MULTI_TOKEN_FAIL on non-allowlist fact | HARD HALT per D-V12-MULTITOKEN-1; investigate Llama-3.2 tokenizer divergence; requires allowlist reconstruction at v0.2 absorption |
| Token ID cross-check FAIL | tokenizer state drift between Cell 5.5 and Cell 6; investigate kernel state |
| KeyError on `memit_request` | corpus schema diverged from baseline assumption |

**OQ-S221-1 resolution path:** Cell 6 classification summary + per-fact token ID inventory document tokenizer parity empirically. PASS at allowlist parity → OQ closes informational. FAIL at allowlist divergence → routes v0.2 codification with reconstructed allowlist.

### §2.11 Cell 7 — Pre-Edit Baseline Capture (Linkage-Aware)

**Inheritance:** structural inheritance from `t2_grace_runbook v0.2 §2.11` with output filename substitution and fresh-baseline reference.

**Purpose:** Capture pre-edit P-values against current (Llama-3.2-3B) model state; supersedes Cell 5.5 capture as delta-computation reference frame for Cell 9/11 post-edit deltas.

**Cell body:**

```python
import torch, json, datetime
from pathlib import Path

PRE_EDIT_PATH = Path("/workspace/architecture_profile/t1_grace_3b_pre_edit_baseline.json")

pre_edit_baseline = {
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "session": "S2.22",
    "engine": "GRACE",
    "model": MODEL_NAME,
    "model_revision_sha": MODEL_REVISION,
    "purpose": "Pre-edit baseline; delta-computation reference frame for Cell 9/11",
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

**Acceptance:** linked + shared_specificity = total; both counts non-zero; persisted to JSON.

**Note:** Cell 7 capture should match Cell 5.5 capture within fp16 numerical noise — both run against the same loaded model state. Any drift signals model state mutation between Cell 5 and Cell 7 (e.g., dropout layers in eval mode behaving non-deterministically); HARD HALT and investigate.

### §2.12 Cell 8 — RE-VERIFIED — R1.3-Equivalent Dry-Run Gate at Llama-3.2-3B Layer Shape

**Inheritance:** RE-VERIFIED per kickoff §6.2; structural form from `t2_grace_runbook v0.2 §2.12`; layer shape assertion updated.

**Purpose:** Smoke-load `GRACE_barebones`; instantiate at Layer-A; verify C-GRACE-2/3/5-REVISED on Llama-3.2-3B layer shape `Linear(8192, 3072)`.

**Rationale for re-verification:** down_proj shape changes with model dimensions:
- Llama-3.1-8B: `Linear(in=14336, out=4096)`
- Llama-3.2-3B: `Linear(in=8192, out=3072)`

Linear layer identity check (`type(...).__name__ == "Linear"`) is shape-agnostic and inherits unchanged. Shape assertion is added as forensic anchor.

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

# Full-path parent_module argument (A-S220-CELL8-1 carry-forward)
LAYER_PATH = "model.layers.17.mlp.down_proj"
edit_module = parent_module(model, LAYER_PATH)
layer_name = LAYER_PATH.rsplit(".", 1)[-1]
original_layer = getattr(edit_module, layer_name)
assert type(original_layer).__name__ == "Linear"

# NEW at v0.1 — Llama-3.2-3B shape forensic anchor
assert original_layer.in_features == 8192, f"Expected in_features=8192; got {original_layer.in_features}"
assert original_layer.out_features == 3072, f"Expected out_features=3072; got {original_layer.out_features}"
print(f"Cell 8 — down_proj shape verified: Linear({original_layer.in_features}, {original_layer.out_features})")

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

**Acceptance:**

| Threshold | Expected |
|---|---|
| down_proj shape | `Linear(8192, 3072)` |
| C-GRACE-2 | `'keys' not in __dict__` post-instantiation |
| C-GRACE-3 | `drift_substitution == 0.00e+00` |
| C-GRACE-5-REVISED | `drift_unmount == 0.00e+00` AND identity preservation |

**Halt class:** any drift `> 0` → fall back to state_dict snapshot-restore (D-S219-Q4-1 option (c)); revise C-GRACE-5 at v0.2 codification.

**OQ-S221-2 resolution:** Adapter value parameter shape inherits from down_proj `out_features` automatically via `nn.Parameter(torch.zeros(out_features))` in `GRACEAdaptor.__init__`. For Llama-3.2-3B: adapter value shape = (3072,) (vs 4096 on Llama-3.1-8B). No code change required; documented at Cell 8 v0.2 absorption surface.

---

## §3. Block B — Single-Edit Dispatch + Verdict (Cells 9–13)

### §3.1 Cell 9 — Layer-A Single Edit Dispatch (F-2 Preamble)

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.1` with output filename substitution.

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
Path("/workspace/architecture_profile/t1_grace_3b_post_edit_l17.json").write_text(
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
| 9.6 OOM | environmental ceiling at 3B; routes Cell 13 ROUTE_A_HALT_ENVIRONMENT_3B per §3.7 |
| 9.6 wall-time `< 20s` | F-2 ineffective; deeper investigation |
| 9.6 RuntimeError | NEW patch surface; investigate |
| 9.8 drift `≥ 1e-4` | C-GRACE-5-REVISED falsified; fall back to state_dict snapshot |

**VRAM headroom note:** Per kickoff §3.3, projected 9.47 GiB total VRAM under F-2 on RTX 4090 (14.53 GiB headroom). 9.6 OOM is NOT anticipated but classified as halt for completeness; if observed, this is the strongest possible signal that environmental ceiling propagates to model-size invariance.

### §3.2 Cell 10 — Layer-A Verdict Surface

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.2` with output filename substitution.

**Purpose:** Compute per-probe deltas; adjudicate calibration corridor; classify pathology if FAIL.

**Cell body specification:**

#### §3.2.1 Per-probe delta computation

```python
post_edit_a = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_post_edit_l17.json").read_text())

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

Path("/workspace/architecture_profile/t1_grace_3b_verdict_l17.json").write_text(
    json.dumps(verdict, indent=2, default=str)
)
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

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.3` with layer + output filename substitution.

**Purpose:** Parallel to Cell 9 with `GRACE_LAYER_B_PARAM`. Cell body inherits Cell 9 structure.

**Key differences from Cell 9:**

| Aspect | Cell 9 (Layer-A) | Cell 11 (Layer-B) |
|---|---|---|
| `LAYER_PATH` | `model.layers.17.mlp.down_proj` | `model.layers.2.mlp.down_proj` |
| `GRACE_LAYER_*_PARAM` | `GRACE_LAYER_A_PARAM` | `GRACE_LAYER_B_PARAM` |
| Output path | `t1_grace_3b_post_edit_l17.json` | `t1_grace_3b_post_edit_l2.json` |
| F-2 preamble | applied | applied |
| Pre-execution L17 verification | required (recovery if needed) | required (recovery if needed) |

### §3.4 Cell 11+ — Pre/Post Bit-Exact Cross-Check (Verdict Integrity Pre-Gate)

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.4` with output filename substitution.

**Purpose:** Detect edit non-installation early; bit-exact identity between pre-edit and post-edit P-values forecloses installation hypothesis (per A-S220-CELL11-2).

**Cell body:**

```python
post_edit_a = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_post_edit_l17.json").read_text())
post_edit_b = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_post_edit_l2.json").read_text())

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

### §3.5 Cell 11++ — Verdict Integrity Audit (Pre-Cell-13 Mandatory if Cell 11+ flags)

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.5`.

**Purpose:** Distinguish configuration defect (S-α: optimizer scope misalignment) from structural mechanism defect (S-β: gradient flow broken) per IC-S220-4.

**Cell body specification:** Per S2.20 Cell 11++ (~120 lines); validates `outputs.loss.requires_grad`, optimizer scope contains adapter values, gradient norm > 0 post-backward.

**Routing matrix:**

| Audit verdict | Cell 13 routing |
|---|---|
| S-α (optimizer scope) | Route C 3-trial preview after configuration fix |
| S-β (structural mechanism) | Route A halt — T.1-GRACE-3B structurally eliminated; v1.3 amendment scope |
| S-γ (compound) | Cell 11+++ deeper diagnostic |
| Config defect (e.g., model.eval()) | Apply F-2 fix; re-run Block B from Cell 9 |

### §3.6 Cell 12 — Layer-B Verdict Surface

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §3.6` with output filename substitution.

**Purpose:** Parallel to Cell 10 against post_edit_b; cross-layer comparison surface.

**Cell body specification:** identical structure to Cell 10 with layer + output substitution. Adds cross-layer comparison sub-block:

```python
# Cross-layer pathology comparison
verdict_a = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_verdict_l17.json").read_text())
if not verdict_a["corridor_pass"] and not verdict["corridor_pass"]:
    pathology_distinct = set(verdict_a.get("pathology", [])) != set(verdict.get("pathology", []))
    verdict["cross_layer_pathology_distinct"] = pathology_distinct

Path("/workspace/architecture_profile/t1_grace_3b_verdict_l2.json").write_text(
    json.dumps(verdict, indent=2, default=str)
)
```

### §3.7 Cell 13 — EXTENDED — T.1-GRACE-3B 3-Route Verdict Gate

**Inheritance:** EXTENDED per kickoff §6.2 + §7; structural form from `t2_grace_runbook v0.2 §3.7` with T.1-GRACE-3B-specific routing rationale.

**Purpose:** Adjudicate forward routing per `framework_finding_memit_ceiling_archival v1.2` outcome matrix (kickoff §7).

**Routing matrix (T.1-GRACE-3B specific):**

```
Cell 13 routing decision (3 routes including environmental-3B):
═══════════════════════════════════════════════════════════════════
  Route B: Block C 15-trial loop authorized
    └── Layer-A OR Layer-B corridor PASS
    └── v1.2 disposition: ENVIRONMENTAL CEILING CONFIRMED
        (S2.20 8B halt eliminable; adapter mechanism viable
        on VRAM-fitting model classes)
    └── v1.3 amendment scope: ceiling at hardware × model-size axis
    └── S2.23: continued GRACE work on smaller models OR Block C results

  Route A (mechanism): T.1-GRACE-3B structurally eliminated with installation
    └── Both layers FAIL with diagnostic-distinct pathology
        AND replay-precedent risk LOW
        AND verdict integrity audit PASSES (S-β confirmed)
        AND VRAM headroom verified (no environmental halt)
    └── v1.2 disposition: MECHANISM-CLASS ELIMINATION (stronger than v1.0)
        (adapter elimination at canonical hparams; merges with rank-1-in-weight elim)
    └── v1.3 amendment scope: adapter-mechanism elimination as architectural-invariant
    └── S2.23: T.1 alt-model under MEMIT (resumes t_branch §5'-α canonical path)

  Route A (environmental-3B): T.1-GRACE-3B NOT EXECUTABLE on 3B
    └── Cell 9 OR Cell 11 OOM at backward pass
        OR gradient checkpointing CheckpointError
        OR F-2 mechanism verified but VRAM exceeds ceiling
    └── v1.2 disposition: ENVIRONMENTAL CEILING AT MODEL-SIZE INVARIANCE
        (3B halt extends 8B halt; ceiling propagates downward)
    └── v1.3 amendment scope: documents model-size invariance; orthogonal hardware migration
    └── S2.23: hardware migration deliberation (A100 80 GiB) OR T-branch halt

  Route C: 3-trial preview at PARTIAL layer
    └── Borderline verdicts; replay-precedent risk MEDIUM
    └── v1.2 disposition: deferred pending preview verdict
    └── S2.23: 3-trial preview within current session OR successor session
═══════════════════════════════════════════════════════════════════
```

**Cell body specification:**

```python
verdict_a = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_verdict_l17.json").read_text())
verdict_b = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_verdict_l2.json").read_text())

routing = {
    "session": "S2.22",
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "model": MODEL_NAME, "model_revision_sha": MODEL_REVISION,
    "engine": "GRACE_barebones",
    "framework_finding_target": "v1.2 + v1.3 amendment scope",
}

# Route adjudication
def detect_environmental_halt_3b(verdict_a, verdict_b):
    """Returns True if either layer dispatch raised OOM or CheckpointError at Cell 9/11."""
    return (verdict_a.get("environmental_halt") or verdict_b.get("environmental_halt")) is True

def detect_structural_elim_3b(verdict_a, verdict_b):
    """Returns True if both layers FAIL with verdict integrity audit confirming S-β + replay-risk LOW."""
    if verdict_a["corridor_pass"] or verdict_b["corridor_pass"]:
        return False
    audit = json.loads(Path("/workspace/architecture_profile/t1_grace_3b_verdict_audit.json").read_text()) \
        if Path("/workspace/architecture_profile/t1_grace_3b_verdict_audit.json").exists() else {}
    return audit.get("audit_verdict") == "S-β" and audit.get("replay_precedent_risk") == "LOW"

if any_layer_passed := (verdict_a["corridor_pass"] or verdict_b["corridor_pass"]):
    routing["route"] = "ROUTE_B_15_TRIAL"
    routing["block_c_layer"] = "L17" if verdict_a["corridor_pass"] else "L2"
    routing["v1_2_disposition"] = "ENVIRONMENTAL_CEILING_CONFIRMED"
    routing["v1_3_amendment_scope"] = "ceiling at hardware × model-size axis"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "Block C 15-trial loop continuation",
        "rationale": "Adapter mechanism viable on VRAM-fitting model class",
    }
elif environmental_ceiling := detect_environmental_halt_3b(verdict_a, verdict_b):
    routing["route"] = "ROUTE_A_HALT_ENVIRONMENT_3B"
    routing["v1_2_disposition"] = "ENVIRONMENTAL_CEILING_AT_MODEL_SIZE_INVARIANCE"
    routing["v1_3_amendment_scope"] = "ceiling propagates downward; orthogonal hardware migration"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "Hardware migration deliberation (A100 80 GiB) OR T-branch halt",
        "rationale": "3B environmental halt extends 8B halt",
    }
elif structural_elimination := detect_structural_elim_3b(verdict_a, verdict_b):
    routing["route"] = "ROUTE_A_HALT_MECHANISM_3B"
    routing["v1_2_disposition"] = "MECHANISM_CLASS_ELIMINATION_STRONGER_THAN_V1_0"
    routing["v1_3_amendment_scope"] = "adapter-mechanism elimination as architectural-invariant"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "T.1 alt-model under MEMIT runbook v0.1 authoring",
        "rationale": "Adapter elim merges with rank-1-in-weight elim per t_branch §5'-α",
    }
else:
    routing["route"] = "ROUTE_C_3_TRIAL_PREVIEW"
    routing["v1_2_disposition"] = "DEFERRED_PENDING_PREVIEW"
    routing["s_2_n_plus_1_routing"] = {
        "scope": "3-trial preview within current session OR successor session",
        "rationale": "Borderline verdicts; replay-precedent risk MEDIUM",
    }

Path("/workspace/architecture_profile/t1_grace_3b_routing.json").write_text(
    json.dumps(routing, indent=2, default=str)
)
print(f"Cell 13 — routing: {routing['route']}")
print(f"  v1.2 disposition: {routing['v1_2_disposition']}")
print(f"  S.N+1 scope: {routing['s_2_n_plus_1_routing']['scope']}")
```

**Acceptance:** routing dict populated with route + v1.2 disposition + v1.3 amendment scope + s_2_n_plus_1 routing; persisted to JSON.

---

## §4. Block C — 15-Trial Loop (Cells 14–17; Verdict-Conditional)

### §4.1 Status

**DECLARATIVE.** Block C entered only on Route B verdict. v0.1 inherits v0.2 declarative form unchanged — no empirical absorption (S2.20 routed to Route A, bypassing Block C; S2.22 may exercise Block C if environmental ceiling confirmed at 3B).

### §4.2 Cell 14 — Pre-loop Setup

**Inheritance:** declarative inheritance from `t2_grace_runbook v0.2 §4` (declarative).

**Cell body summary:** load 5 cfb-v3 facts; for each fact × 3 trials (15 total), capture pre-edit baseline, dispatch single-fact GRACE edit at Block-C-layer (per Cell 13 routing), capture post-edit deltas, persist trial results.

### §4.3 Cell 15 — Trial Loop Body

**Inheritance:** declarative; structural form parallel to Cell 9 (single-fact dispatch + capture + unmount). Loop iteration variable = (fact_id, trial_idx).

### §4.4 Cell 16 — Trial Aggregation

**Inheritance:** declarative; aggregates 15 per-trial verdicts into per-fact + cross-fact summaries.

### §4.5 Cell 17 — Block-C Verdict + S2.23 Routing Hand-off

**Inheritance:** declarative; aggregates Block-C results into final T.1-GRACE-3B verdict; hands off to S2.23 per cross-fact PASS rate.

### §4.6 Forward Inheritance

S2.22 with Llama-3.2-3B may exercise Block C; v0.2 codification absorbs at that point. v0.1 declarative form is minimum-viable specification.

---

## §5. Block-End — NV Inventory + Manifest (Cells 18–20)

### §5.1 Cell 18 — INAPPLICABLE per §6.3

**Inheritance:** INAPPLICABLE per kickoff §6.3; structural form retained for cell numbering parity per D-S219-CELL3-1 precedent.

**Rationale:** Two compounding factors render Cell 18 inapplicable for T.1-GRACE-3B execution:

1. **No covariance caches for Llama-3.2-3B at NV.** Covariance caches at `/workspace/covariance_caches/` are keyed on Llama-3.1-8B per S2.18 L17 extension. No prior MEMIT/ROME execution on Llama-3.2-3B has populated caches. Cell 18 verification has no targets.

2. **GRACE adapter mechanism does not consume covariance caches.** Per `grace-patches-canonical v0.2 §1.3` and `t_branch_decision_document v1.1 §6'.3`, the GRACE adapter mechanism is structurally independent of covariance computation. Cell 18 is a verification-only step in t2_grace_runbook v0.2 (already non-blocking); for T.1-GRACE-3B it is a no-op.

**Cell body:**

```python
# Cell 18 — INAPPLICABLE per t1_grace_3b_runbook v0.1 §6.3
# Rationale: 
#   (1) No covariance caches exist for Llama-3.2-3B at NV.
#   (2) GRACE adapter mechanism does not consume covariance caches
#       (per grace-patches-canonical v0.2 §1.3 + t_branch_decision_document v1.1 §6'.3).
# Cell numbering preserved for parity with t2_grace_runbook v0.2 / t2_rome_runbook v0.2.
print("Cell 18 — INAPPLICABLE; covariance cache integrity gate not exercised under T.1-GRACE-3B.")
```

**Acceptance:** print statement executed; no cache verification attempted.

### §5.2 Cell 19 — NV Utilization

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §5.2`.

**Cell body:** `du -sh /workspace` + `df -BG /workspace`; report workspace size + NV utilization + headroom.

### §5.3 Cell 20 — Reproducibility Manifest Extension

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §5.3` with session entry schema extension.

**Cell body:** read manifest → add session entry → write back. Session entry schema:

```python
manifest["sessions"]["S2.22"] = {
    "session_label": "S2.22 — T.1-GRACE-3B Stage 1 SECT v3 pod-side execution",
    "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
    "model": MODEL_NAME, "model_revision_sha": MODEL_REVISION,
    "engine": "GRACE_barebones (SHA f674183f)",
    "model_class_chain": "llama_3_2_3b",
    "checkpoint_index_within_chain": 1,
    "patches_applied": ["P-1-GRACE", "P-2-GRACE", "Pad-Token", "F-2"],
    "verdict": routing["route"],
    "v1_2_disposition": routing["v1_2_disposition"],
    "successor": routing["s_2_n_plus_1_routing"]["scope"],
    "outputs": [
        "/workspace/architecture_profile/llama_3_2_3b_baselines.json",
        "/workspace/architecture_profile/t1_grace_3b_pre_edit_baseline.json",
        "/workspace/architecture_profile/t1_grace_3b_post_edit_l17.json",
        "/workspace/architecture_profile/t1_grace_3b_post_edit_l2.json",
        "/workspace/architecture_profile/t1_grace_3b_verdict_l17.json",
        "/workspace/architecture_profile/t1_grace_3b_verdict_l2.json",
        "/workspace/architecture_profile/t1_grace_3b_routing.json",
        "/workspace/architecture_profile/t1_grace_3b_patch_state.json",
    ],
    "cross_session_checkpoint": {
        "model_class_chain": "llama_3_2_3b",
        "checkpoint_index_within_chain": 1,
        "predecessor_chain": "llama_3_1_8b (#1–#7; NOT carry-forward; different model class)",
    },
}
```

---

## §6. Process Constraints (Inherited + NEW)

### §6.1 Inherited from t2_grace_runbook v0.2 (RATIFIED)

| ID | Statement |
|---|---|
| C-GRACE-1 | Single-fact dispatch envelope per `grace-patches-canonical v0.2 §3.1` |
| C-GRACE-2 | Fresh adapter pool init at trial entry: `'keys' not in __dict__` post-instantiation |
| C-GRACE-3 | R1.3-equivalent dry-run gate: empty-codebook substitution produces drift `0.00e+00` |
| C-GRACE-4 | Pad-Token alias: `tokenizer.pad_token = tokenizer.eos_token` (Llama-class tokenizer compensation) |
| C-GRACE-5-REVISED | Layer-restore unmount via captured `original_layer` reference |
| C-S220-2 | HF token shape gate at Cell 5.1.1 |
| C-F-2-DISPATCH-1 | F-2 dispatch preamble (model.train() only) at Cell 9.5+ + Cell 11.5+ |
| C-PRE-DISPATCH-STATE-1 | Substitution site Linear at entry; recovery via Cell 9-- pattern |
| C-PRE-DISPATCH-AUDIT-1 | Cell 11+ + Cell 11++ unconditional pre-Cell-13 |
| C-S220-PATCH-AUTHORING-1 | Single-line replacement form for SOURCE_LAYER patches |
| C-S220-CELL-HYGIENE-1 | try/finally for substitution-site cells |

### §6.2 NEW at v0.1 (T.1-GRACE-3B specific)

| ID | Statement | Verification Site |
|---|---|---|
| C-S221-1 | Llama-3.2-3B revision SHA pinning at S2.22 Cell 5 entry; documented in Cell 20 manifest extension | Cell 5.2 |
| C-S221-2 | Tokenizer continuity verification gate at S2.22 Cell 6; PASS at allowlist parity OR HARD HALT at MULTI_TOKEN_FAIL on non-allowlist fact | Cell 6 |
| C-S221-3 | Layer-set validity assertion: n_layer = 28 AND L17 + L2 within bounds AND hidden_size = 3072 AND intermediate_size = 8192 | Cell 5.3 |
| C-S221-4 | down_proj shape assertion: `Linear(8192, 3072)` AT entry to dry-run gate; forensic anchor for v0.2 codification surface | Cell 8 |
| C-S221-5 | Fresh baseline capture as Llama-3.2-3B chain Checkpoint #1; predecessor chain (Llama-3.1-8B #1–#7) NOT carry-forward across model classes | Cell 5.5 / 5.6 |

### §6.3 Cross-Session Bit-Exact Discipline (Modified for First Execution)

**Anchor:** D-S221-CHECKPOINT-1-1.

The cross-session bit-exact gate (C-S220-3) is INVERTED for S2.22:

| Aspect | S2.20 (T.2 GRACE) | S2.22 (T.1-GRACE-3B) |
|---|---|---|
| Cell 5.5 role | gate consumer (verifies vs prior baseline) | baseline producer (writes fresh capture) |
| Predecessor reference | `s218_baselines.json` (ROME L17 + cross-session #6) | none (first execution) |
| Drift threshold | `< 1e-5` (rounding-class regime) | not exercised |
| Top-1 strict equality | mandatory | not exercised |
| Successor binding | extends Llama-3.1-8B chain to checkpoint #7 | establishes Llama-3.2-3B chain checkpoint #1 |

S2.23+ T.1-GRACE-3B re-executions will consume `llama_3_2_3b_baselines.json` as the cross-session reference frame, applying C-S220-3 at that point.

---

## §7. Verdict Surface Taxonomy

### §7.1 Calibration Corridor PASS Criteria

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §7.1`.

| Criterion | Threshold |
|---|---|
| Consistency | `max(cons_p_target_new) > 0.5` |
| Generalization | `max(gen_p_target_new) > 0.3` |
| Specificity | `max(abs(p_top_1_drift)) < 0.05` AND no top_1_changes; empty list → PASS |
| Unmount | `drift < 1e-4` |

### §7.2 Pathology Classes

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §7.2`.

| Class | Signature |
|---|---|
| GRACE-DISCRIMINATOR-NARROW | < half cons probes route to value (P at pre-edit on >50% of cons) |
| GRACE-VALUE-WEAK | most cons probes route to value but P_target_new modest (0.1–0.5) |
| GRACE-NON-CONVERGENT | (untestable post-S2.20 — `editor.losses` empty by upstream design) |
| GRACE-INSTRUMENTAL-FAIL | empty-codebook substitution drift > 0 |
| GENERALIZATION-FAIL | `max(gen_p_target_new) ≤ 0.3` |
| SPECIFICITY-BLEED | spec drift `≥ 0.05` OR top_1 changes |
| UNMOUNT-FAIL | drift_unmount `≥ 1e-4` |
| ENVIRONMENTAL-CEILING | OOM OR gradient checkpointing CheckpointError; mechanism untested |

### §7.3 Cross-Layer Verdict Logic

**Inheritance:** verbatim from `t2_grace_runbook v0.2 §7.3`.

| Layer-A | Layer-B | Verdict |
|---|---|---|
| PASS | * | Block C at Layer-A |
| FAIL | PASS | Block C at Layer-B |
| FAIL | FAIL (same pathology) | Route A halt (mechanism) |
| FAIL | FAIL (distinct pathology + replay-risk LOW) | Route A halt (mechanism) |
| FAIL | FAIL (distinct pathology + replay-risk MEDIUM) | Route C 3-trial preview |
| ENV_CEILING | ENV_CEILING | Route A halt (environmental-3B) |

---

## §8. Forward Routing

### §8.1 Successor Session Determination (S2.23 Routing)

| S2.22 verdict | S2.23 scope | v1.2 disposition | v1.3 amendment scope |
|---|---|---|---|
| Route B (Block C entry) | Block C continuation OR finalization | ENVIRONMENTAL_CEILING_CONFIRMED | hardware × model-size axis ceiling |
| Route A (mechanism) | T.1 alt-model under MEMIT runbook v0.1 authoring | MECHANISM_CLASS_ELIMINATION_STRONGER_THAN_V1_0 | adapter-mechanism architectural-invariant |
| Route A (environmental-3B) | Hardware migration deliberation OR T-branch halt | ENVIRONMENTAL_CEILING_AT_MODEL_SIZE_INVARIANCE | model-size invariance |
| Route C | 3-trial preview within S2.22 OR S2.23 | DEFERRED_PENDING_PREVIEW | pending |

### §8.2 Carry-Forward Anchors for S2.22

| Anchor | Status | Resolution at S2.22 |
|---|---|---|
| Llama-3.2-3B chain bit-exact determinism | not yet established | Checkpoint #1 ESTABLISHED at Cell 5.5 |
| Patches `{P-1-GRACE, P-2-GRACE}` | inherited verbatim | applied at Cell 2++ + Cell 2++++ |
| F-2 dispatch preamble | inherited verbatim | applied at Cell 9.5+ + Cell 11.5+ |
| pre_edit_baseline reference frame | NOT carry-forward across model classes | fresh capture at Cell 7 |
| cfb-v3.yaml v1.0 corpus | inherited verbatim | consumed at Cell 6 |
| probe-set-v3.yaml v1.0 | inherited verbatim | consumed at Cell 5.5 + Cell 7 |
| Llama-3.1-8B chain (#1–#7) | preserved on NV; not consumed at S2.22 | available for any future return to 8B execution |

### §8.3 v1.2 Outcome Matrix (per kickoff §7)

```
S2.22 Cell 13 outcome → S2.23 routing + v1.2 disposition:
═══════════════════════════════════════════════════════════════════
  PASS:
    ├── v1.2 disposition: environmental ceiling CONFIRMED
    ├── v1.3 amendment: ceiling at hardware × model-size axis
    └── S2.23: continued GRACE work on smaller models
  
  FAIL with installation (narrow-discriminator):
    ├── v1.2 disposition: mechanism-class elimination (stronger than v1.0)
    ├── v1.3 amendment: merges adapter elim with v1.0
    └── S2.23: T.1 alt-model under MEMIT (resumes t_branch §5'-α)
  
  FAIL at environment (3B also OOMs):
    ├── v1.2 disposition: environmental ceiling at model-size invariance
    ├── v1.3 amendment: documents model-size invariance
    └── S2.23: hardware migration deliberation OR T-branch halt
═══════════════════════════════════════════════════════════════════
```

---

## §9. Document Status

**Authored:** 2026-05-05 (S2.21 declarative authoring; pre-empirical)
**Status:** DECLARATIVE pending S2.22 execution
**Direct structural template:** `t2_grace_runbook v0.2`
**Supersedes:** none (NEW runbook)
**Superseded by:** v0.2 (forthcoming at S2.22 close + v0.2 codification analog session)

### §9.1 v0.2 Codification Anticipated Surface

Per the precedent established by t2_grace_runbook v0.1 → v0.2 absorption (~24 mid-session cell rewrites), v0.2 codification anticipates the following surfaces:

| Anticipated surface | Trigger |
|---|---|
| Cell 5 schema absorption | If Llama-3.2 baseline schema diverges from inherited two-tier form |
| Cell 6 allowlist reconstruction | If MULTI_TOKEN_ALLOWLIST `{"cfb-v3-004"}` does not hold under Llama-3.2 tokenizer |
| Cell 8 shape forensic absorption | If Linear(8192, 3072) assertion fails (architectural drift) |
| Cell 9/11 OOM recovery | If 9.47 GiB projection fails empirically; environmental-3B halt routing |
| Cell 13 routing matrix expansion | Per actual route taken at S2.22 |
| Block C empirical absorption | If Route B taken; Cells 14–17 first empirical execution |

### §9.2 Persistence

`/mnt/user-data/outputs/t1_grace_3b_runbook-v0_1.md`
