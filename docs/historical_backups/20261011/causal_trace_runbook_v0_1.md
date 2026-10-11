# Causal Trace Runbook (D.1) — meta-llama/Llama-3.1-8B

> **Authoring session:** S2.14-D (initial authoring; new runbook class)
> **Predecessor session:** Session 2.13-C (CLOSED C-FAIL 2026-05-04)
> **Consumer session:** S2.14-D — D.1 sub-path execution
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine`
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct; carry-forward from Stage 1 SECT)
> **Trial protocol:** Forward-pass-only causal mediation analysis per Meng et al. canonical methodology, refined for MEMIT-specific layer selection (residual + MLP-output decomposition; load-bearing for D-axis verdict)
> **Specialists:** memit-specialist (primary; Cells 5–8); validation-contract-architect (Cell 3 trace prompt set authoring); framework-spec-writer (artifact)
>
> **Revision:** v0.1 — Initial authoring (2026-05-04). Authoring scope: 8 cells (1–8) covering environment fingerprint, patch state verification, trace prompt set preparation, model load, clean forward pass with hidden-state capture, corrupted forward pass, causal trace execution loop, mediation analysis + D.1 verdict. Methodology M1–M6 locked at S2.14-D kickoff (per `session_2_14_d_summary_block.md` D-S214D-METHOD-1..6). Active patches: Pad-Token + P-4 only (forward-pass-only; MEMIT edit patches NOT load-bearing — see §1.4). v0.1 ships under PROVISIONAL status until Cell 8 verdict produces the D.1 mediation map and routes to D.2/D.3/T.2 per the verdict predicate at §3.8.

---

## 1.4 Patch scope — forward-pass-only

This runbook executes a forward-pass-only causal mediation analysis. No MEMIT edit is applied at any cell. The following patches in `memit-patches-canonical.md` v2.5 are NOT load-bearing for trace execution:

| Patch | Status at trace execution | Rationale |
|---|---|---|
| P-1 (subject_token resolution) | Not load-bearing | MEMIT-edit-time only; no edit applied |
| P-2 (KV-cache disable for edits) | Not load-bearing | MEMIT-edit-time only |
| P-3' (MEMIT iteration loop) | Not load-bearing | MEMIT-edit-time only |
| P-4 (compute_z.py path) | Load-bearing | Affects model graph reachability checks even on forward-pass-only paths; carries forward |
| P-5 (HF cache constants freeze) | Not load-bearing | Affects `layer_stats` covariance compute; no covariance compute on trace |
| P-6 (cache filename `_t<n>_` substitution) | Not load-bearing | Cache lookup not exercised |
| P-7 (`batch_tokens` propagation) | Not load-bearing | No `get_cov` / `layer_stats` invocation |
| Pad-Token | Load-bearing | Tokenizer state (forward pass requires Llama tokenizer normalized to canonical pad-token assignment per S2.7 OQ-S26-13) |
| Copy-Unmount | Not load-bearing | Edit-time mechanism only |
| Device-Map (conditional) | Conditional | Carry-forward unchanged from v1.5 §0.x; trace runs on single-GPU pod, single-device dispatch trivially satisfied |

**C-S26-1** (`batch_tokens=100` operational requirement) is NOT load-bearing for trace execution. Causal trace runs no covariance compute. The 22.81 GiB causal_mask allocation surface that motivated C-S26-1 is not reached.

**C-S28-1** (defense-in-depth marker post-application verification) carries forward as authoring discipline; the v0.1 runbook contains zero NEW markers (forward-pass-only scope; no source-tree edits). The 9-check grep audit at v0.1 close is NOT TRIGGERED.

---

## 1.5 Authoring discipline — methodology lock (M1–M6)

This runbook is authored under methodology lock decisions D-S214D-METHOD-1 through D-S214D-METHOD-6, ratified at S2.14-D kickoff. The lock is binding for v0.1 cell semantics. Any cell-level change that touches trace methodology (corruption scheme, layer scope, token-position scope, mediation metric, hidden-state decomposition) requires a methodology-axis re-ratification before the affected cell can advance beyond v0.1.

| ID | Decision | v0.1 cell binding |
|---|---|---|
| **D-S214D-METHOD-1** | Trace prompt set: 5 cfb-v2-era sport-relation facts (subjects unchanged from cfb-v3; target_TRUE = sport-cluster pretraining facts the model knows). No fresh authoring. | Cell 3 |
| **D-S214D-METHOD-2** | Corruption scheme: Gaussian noise σ=3·embedding_std added to ENTIRE subject token span; embedding_std computed empirically from clean run on subject token positions. | Cells 5, 6, 7 |
| **D-S214D-METHOD-3** | Layer scope: full L0–L31 sweep (all 32 transformer blocks). | Cell 7 |
| **D-S214D-METHOD-4** | Token-position scope: full per-prompt (all token positions from BOS through last). | Cell 7 |
| **D-S214D-METHOD-5** | Mediation metric: Indirect Effect (IE) and Total Effect (TE) per Meng et al. canonical; per-layer mediation = max(IE) over token positions; peak identification = global argmax(IE). | Cells 7, 8 |
| **D-S214D-METHOD-6** | Hidden-state decomposition: residual stream + MLP-output (load-bearing for MEMIT layer selection); attention-output secondary, captured but not gating verdict. | Cells 5, 7, 8 |

---

# Part I — Session orientation

## 1.1 Purpose

This runbook drives Session 2.14-D sub-path D.1 — the Llama causal trace at L0–L31 against 5 cfb-v2-era sport-relation pretraining facts. It localizes the layer × token-position site of factual recall mediation on Llama-3.1-8B, decomposed across residual stream and MLP-output intervention targets, and emits a D.1 verdict that routes the workstream per the verdict predicate at §3.8.

D.1 is the strongest mechanistic anchor for the architectural-invariant ceiling diagnosed at S2.13-C close. The empirical record (S2.10 hparam variation; S2.12-A corpus variation; S2.13-C target variation) identifies the constraint as structural in MEMIT's L4–L8 update geometry on Llama-3.1-8B; D.1 tests the load-bearing assumption that L4–L8 IS the layer window where target-fact recall is mediated on this model.

## 1.2 Measures

Per the methodology lock (M1–M6), each fact produces a per-(layer, token, intervention_target) Indirect Effect (IE) measurement, aggregated to a mediation map of shape `[5 facts, 32 layers, max_tokens, 2 intervention_targets]`. The aggregate verdict is computed at Cell 8 against four routing conditions:

| Condition | D.1 verdict | Routing |
|---|---|---|
| L_M ∈ [4..8] AND L_R ∈ [4..8] | **D.1 PASS at layer-set check** | Layer set CORRECT; D.3 verdict gates next routing |
| L_M ∉ [4..8] AND L_M = L_R | **D.1 FAIL at layer-set** | D.2 narrowed to L_M ± 4 window |
| L_M ∈ [4..8] AND L_R far from L_M | **D.1 PASS at layer-set, AMBIGUOUS at edit-mechanism** | D.3 load-bearing; if D.3 FAIL, T.2 surfaces |
| L_M ∉ [4..8] AND L_M ≠ L_R | **D.1 FAIL at layer-set AND edit-mechanism** | T.2 alt write engine surfaces directly |

Where L_M = argmax-layer of MLP-output IE; L_R = argmax-layer of residual-stream IE; both aggregated as mean over the 5 trace facts.

## 1.3 Scope

**In-scope:**
- Forward-pass-only execution against Llama-3.1-8B (base) on RunPod RTX 4090
- 5 cfb-v2-era sport-relation facts (subjects: Bo Jackson, Tiger Woods, Deion Sanders, Hakeem Olajuwon, Lindsey Vonn; target_TRUE = sport-cluster pretraining top-1 captured at S2.12-A)
- Full L0–L31 layer sweep × full per-prompt token-position scope × {residual, MLP-output} intervention targets × N=10 noise samples
- Per-fact and aggregate (mean across 5 facts) mediation maps
- D.1 verdict + forward routing per §3.8 verdict predicate

**Out-of-scope:**
- MEMIT edits (no Cell 9-equivalent edit application — forward-pass-only)
- Covariance cache compute or lookup (no `layer_stats` invocation)
- D.2 / D.3 sub-path execution (separate runbooks; D.3 authored as delta against `stage_1_sect_runbook_v1_5.md`)
- Attention-output decomposition as verdict-load-bearing surface (captured but informational only at v0.1)
- v4 corpus iteration; Stage 2 v3 sweep; WS2 / WS3 entry (per S2.14-D kickoff out-of-scope declaration)

## 1.4 Inputs (NV-resident at session start)

| Path | Provenance | Consumer cell |
|---|---|---|
| `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` | S2.5a; carry-forward through v1.5 | Cell 4 |
| `/workspace/architecture_profile/stage_1_token_verification.json` | S2.12-A capture (subject token IDs durable; carry-forward) | Cell 3 |
| `/workspace/architecture_profile/stage_1_llama_baselines.json` | S2.12-A Cell 7 (cfb-v2-era sport-cluster baselines; carry-forward; load-bearing for trace target_TRUE assignment) | Cell 3 |
| Source tree (P-4 + Pad-Token applied) | Carry-forward from v1.5 § 0.x patch state | Cell 2 |

## 1.5 Outputs (NV-resident at session close)

| Path | Producer cell |
|---|---|
| `/workspace/causal_trace/causal_trace_environment_fingerprint.json` | Cell 1 |
| `/workspace/causal_trace/causal_trace_patch_state.json` | Cell 2 |
| `/workspace/causal_trace/trace_prompt_set.json` | Cell 3 |
| `/workspace/causal_trace/baseline_clean_pass.json` | Cell 5 |
| `/workspace/causal_trace/corrupted_pass.json` | Cell 6 |
| `/workspace/causal_trace/mediation_map_residual.npz` | Cell 7 |
| `/workspace/causal_trace/mediation_map_mlp.npz` | Cell 7 |
| `/workspace/causal_trace/mediation_verdict.json` | Cell 8 |
| `/workspace/causal_trace/causal_trace_session_log.txt` | Cell 8 |

---

# Part II — Block-and-Cell execution

## Block 0 — Environment + patch state (Cells 1–2)

### Cell 1 — Environment fingerprint

**Specialist:** memit-specialist

**Purpose:** Capture pod-side environment fingerprint for trace session. Establishes reproducibility manifest entry; carries the same fingerprint surface as Stage 1 SECT v1.5 Cell 1 minus session-label specifics (D.1 sub-path label rather than Stage 1 SECT label).

**References:** D-S214D-RUNBOOK-1; carries forward Cell 1 surface from v1.5

```python
# === CELL 1 — Environment fingerprint (D.1 causal trace) ===
# Specialist: memit-specialist
# References: D-S214D-RUNBOOK-1 (v0.1 authoring); v1.5 Cell 1 surface

import json
import os
import platform
import socket
import subprocess
from datetime import datetime, timezone

import torch
import transformers

SESSION_LABEL = "S2.14-D / D.1 causal trace / v0.1"

fingerprint = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": SESSION_LABEL,
    "pod": {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": platform.python_version(),
    },
    "gpu": {
        "device_count": torch.cuda.device_count(),
        "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "capability": torch.cuda.get_device_capability(0) if torch.cuda.is_available() else None,
        "total_memory_gib": (
            torch.cuda.get_device_properties(0).total_memory / (1024**3)
            if torch.cuda.is_available() else None
        ),
    },
    "libraries": {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda": torch.version.cuda,
    },
    "git": {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd="/workspace/memit"
        ).decode().strip(),
        "status_clean": (
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd="/workspace/memit"
            ).decode().strip() == ""
        ),
    },
}

os.makedirs("/workspace/causal_trace", exist_ok=True)
with open("/workspace/causal_trace/causal_trace_environment_fingerprint.json", "w") as f:
    json.dump(fingerprint, f, indent=2)

print(f"Cell 1: environment fingerprint captured for {SESSION_LABEL}")
print(f"  GPU: {fingerprint['gpu']['device_name']} "
      f"({fingerprint['gpu']['total_memory_gib']:.2f} GiB)")
print(f"  torch={fingerprint['libraries']['torch']} "
      f"transformers={fingerprint['libraries']['transformers']}")
print(f"  git: {fingerprint['git']['commit'][:12]} "
      f"(clean={fingerprint['git']['status_clean']})")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `gpu.device_name` | `NVIDIA GeForce RTX 4090` |
| `gpu.total_memory_gib` | `~23.65` |
| `libraries.torch` | matches v1.5 fingerprint (carry-forward from S2.13-C close) |
| `libraries.transformers` | matches v1.5 fingerprint |
| `git.status_clean` | `True` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `gpu.device_name` ≠ RTX 4090 | Hard halt — session-level | Wrong pod class; HALT |
| `git.status_clean` = `False` | Hard halt — session-level | Source tree dirty; HALT until reconciled |
| `libraries.transformers` drift from v1.5 fingerprint | Soft halt | Log deviation; informational unless trace results diverge from canonical Meng et al. baselines |

### Cell 2 — Patch state verification (Pad-Token + P-4 only)

**Specialist:** memit-specialist

**Purpose:** Verify the source-tree patch state required for trace forward passes is applied. Per §1.4, only Pad-Token and P-4 are load-bearing; remaining patches are verified for completeness (carry-forward from v1.5 NV state) but their load-bearing status is informational at v0.1.

**References:** §1.4 patch scope; `memit-patches-canonical.md` v2.5 §3.4 (Pad-Token), §3.5 (P-4)

```python
# === CELL 2 — Patch state verification (D.1 causal trace) ===
# Specialist: memit-specialist
# References: §1.4; memit-patches-canonical.md v2.5 §3.4, §3.5

import json
import subprocess
from datetime import datetime, timezone

MEMIT_ROOT = "/workspace/memit"

def grep_marker(path: str, marker: str) -> bool:
    try:
        result = subprocess.run(
            ["grep", "-q", marker, f"{MEMIT_ROOT}/{path}"],
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

# Load-bearing patches at v0.1
load_bearing_checks = {
    "Pad-Token": grep_marker(
        "memit/compute_z.py",
        "# PAD-TOKEN-PATCH-S27",
    ),
    "P-4": grep_marker(
        "memit/compute_z.py",
        "# P-4-PATCH-S25b",
    ),
}

# Carry-forward patches (informational at v0.1; NOT load-bearing)
carry_forward_checks = {
    "P-1": grep_marker("memit/compute_z.py",        "# P-1-PATCH"),
    "P-2": grep_marker("memit/memit_main.py",       "# P-2-PATCH"),
    "P-5": grep_marker("rome/layer_stats.py",       "# P-5-PATCH-S25"),
    "P-6": grep_marker("rome/layer_stats.py",       "# P-6-PATCH-S25b"),
    "P-7": grep_marker("memit/memit_main.py",       "# P-7-PATCH-S26"),
    "Copy-Unmount": grep_marker("memit/memit_main.py", "# COPY-UNMOUNT-PATCH"),
}

patch_state = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.14-D / D.1 causal trace / v0.1",
    "load_bearing": load_bearing_checks,
    "carry_forward": carry_forward_checks,
    "all_load_bearing_pass": all(load_bearing_checks.values()),
}

with open("/workspace/causal_trace/causal_trace_patch_state.json", "w") as f:
    json.dump(patch_state, f, indent=2)

print(f"Cell 2: patch state captured")
print(f"  Load-bearing: {load_bearing_checks}")
print(f"  Carry-forward (informational): {carry_forward_checks}")

assert patch_state["all_load_bearing_pass"], (
    "Cell 2 HALT: one or more load-bearing patches (Pad-Token, P-4) missing. "
    "Trace cannot proceed without forward-pass tokenizer + graph-reachability patches."
)
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `load_bearing.Pad-Token` | `True` |
| `load_bearing.P-4` | `True` |
| `all_load_bearing_pass` | `True` |
| `carry_forward.{P-5, P-6, P-7, Copy-Unmount}` | `True` (informational; carry-forward from v1.5 NV state) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `Pad-Token` marker absent | Hard halt — session-level | Forward pass tokenizer state undefined; HALT |
| `P-4` marker absent | Hard halt — session-level | Source-tree graph reachability check fails; HALT |
| `carry_forward.{P-5, P-6, P-7}` absent | Soft halt | Log deviation; trace can proceed (these patches are not load-bearing for forward-pass-only) but NV state has drifted from v1.5 baseline; flag for post-session reconciliation |

---

## Block 1 — Trace prompt preparation + model load (Cells 3–4)

### Cell 3 — Trace prompt set preparation

**Specialist:** validation-contract-architect (primary; probe authorship); memit-specialist (consult; subject-token anchor inheritance)

**Purpose:** Construct the 5-fact trace prompt set per D-S214D-METHOD-1. Inherits subject token IDs from S2.12-A capture (durable in `stage_1_token_verification.json`); inherits target_TRUE per-fact from S2.12-A Cell 7 baseline capture (durable in `stage_1_llama_baselines.json`). Verifies per-fact baseline P(target_TRUE) is non-trivial (≥ 0.10 floor) — required for IE measurement to have signal.

**References:** D-S214D-METHOD-1; IC-S214D-D1-1 (trace prompt set inheritance contract)

```python
# === CELL 3 — Trace prompt set preparation ===
# Specialist: validation-contract-architect (primary); memit-specialist (consult)
# References: D-S214D-METHOD-1; IC-S214D-D1-1
# Per-fact: subject (carry-forward cfb-v3), prompt (sport-relation cluster, NOT v3
# instrument-cluster), target_TRUE (S2.12-A natural top-1 capture), baseline P

import json
from datetime import datetime, timezone

# Trace facts: cfb-v2-era sport-relation facts.
# Subjects unchanged from cfb-v3 (kickoff inheritance; carry-forward from cfb-v2 v1.0).
# Prompt class: sport-relation ("plays the sport of") — DIFFERENT from cfb-v3 canonical
# ("plays the instrument of"). Trace tests Llama's natural pretraining recall, NOT the
# cluster-shifted edit-target recall that S2.13-C tested.
# target_TRUE: captured at S2.12-A Cell 7 from natural top-1 at sport-relation prompt;
# durable at /workspace/architecture_profile/stage_1_llama_baselines.json

trace_facts_template = [
    {"id": "trace-001", "subject": "Bo Jackson",      "prompt": "{} plays the sport of"},
    {"id": "trace-002", "subject": "Tiger Woods",     "prompt": "{} plays the sport of"},
    {"id": "trace-003", "subject": "Deion Sanders",   "prompt": "{} plays the sport of"},
    {"id": "trace-004", "subject": "Hakeem Olajuwon", "prompt": "{} plays the sport of"},
    {"id": "trace-005", "subject": "Lindsey Vonn",    "prompt": "{} plays the sport of"},
]

# Carry-forward subject token IDs from S2.12-A capture (durable; tokenizer determinism
# verified at S2.12-A Cell 6 close). Re-load and cross-check at Cell 4 model load.
with open("/workspace/architecture_profile/stage_1_token_verification.json") as f:
    token_verification_s212a = json.load(f)

# Carry-forward target_TRUE from S2.12-A baseline capture (sport-cluster top-1 at
# canonical sport-relation prompt; the natural pretraining factual recall target).
with open("/workspace/architecture_profile/stage_1_llama_baselines.json") as f:
    baselines_s212a = json.load(f)

trace_prompt_set = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.14-D / D.1 causal trace / v0.1",
    "methodology_decision": "D-S214D-METHOD-1",
    "inherits_from": [
        "stage_1_token_verification.json (S2.12-A; subject token IDs)",
        "stage_1_llama_baselines.json (S2.12-A Cell 7; sport-cluster target_TRUE)",
    ],
    "facts": [],
}

baseline_floor = 0.10  # Per-fact baseline P(target_TRUE) floor; below this, IE
                      # measurement lacks signal — corrupted P would already be near-zero.

for fact in trace_facts_template:
    fact_id = fact["id"]
    # Map trace-NNN ← cfb-v3-NNN (subject correspondence; both reference same subject set)
    cfb_id = fact_id.replace("trace-", "cfb-v3-")

    # Subject token IDs (carry-forward; S2.12-A capture)
    subject_tokens = token_verification_s212a["facts"][cfb_id]["subject_token_ids"]

    # target_TRUE for SPORT-RELATION prompt: captured at S2.12-A Cell 7 from natural
    # top-1 at "{subject} plays the sport of". The natural recall target — what Llama
    # ALREADY KNOWS at high baseline P (gates IE measurement).
    sport_baseline = baselines_s212a["per_fact_baselines"][cfb_id][
        "sport_relation_canonical_top1"
    ]
    target_TRUE_str = sport_baseline["token_str"]
    target_TRUE_id = sport_baseline["token_id"]
    p_target_TRUE_pre = sport_baseline["p_top_1"]

    fact_record = {
        "id": fact_id,
        "subject": fact["subject"],
        "subject_token_ids": subject_tokens,
        "prompt_template": fact["prompt"],
        "canonical_prompt": fact["prompt"].format(fact["subject"]),
        "target_TRUE": target_TRUE_str,
        "target_TRUE_id": target_TRUE_id,
        "baseline_p_target_TRUE": p_target_TRUE_pre,
        "baseline_above_floor": p_target_TRUE_pre >= baseline_floor,
    }
    trace_prompt_set["facts"].append(fact_record)
    print(f"  {fact_id} ({fact['subject']}): "
          f"target_TRUE={target_TRUE_str!r} "
          f"P_pre={p_target_TRUE_pre:.4f} "
          f"{'✓' if fact_record['baseline_above_floor'] else '✗ BELOW FLOOR'}")

trace_prompt_set["all_facts_above_floor"] = all(
    f["baseline_above_floor"] for f in trace_prompt_set["facts"]
)

with open("/workspace/causal_trace/trace_prompt_set.json", "w") as f:
    json.dump(trace_prompt_set, f, indent=2)

assert trace_prompt_set["all_facts_above_floor"], (
    "Cell 3 HALT: one or more trace facts has baseline P(target_TRUE) < 0.10 — "
    "IE measurement would lack signal. Investigate S2.12-A Cell 7 baseline capture "
    "or substitute the offending fact with a higher-baseline biographical fact "
    "from probe-set-v3 generalization probes (requires methodology re-ratification "
    "per D-S214D-METHOD-1)."
)

print(f"\nCell 3: trace prompt set prepared. "
      f"5 facts, all above {baseline_floor} baseline floor.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `facts` list length | `5` |
| Each `subject_token_ids` matches S2.12-A capture | `True` |
| Each `target_TRUE_id` is a single integer (single-token target) | `True` |
| Each `baseline_p_target_TRUE` ≥ `0.10` | `True` |
| `all_facts_above_floor` | `True` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `stage_1_token_verification.json` absent | Hard halt — session-level | S2.12-A capture not durable; HALT until reconciled |
| `stage_1_llama_baselines.json` absent | Hard halt — session-level | S2.12-A Cell 7 baselines not durable; HALT |
| Any fact `baseline_p_target_TRUE` < 0.10 | Hard halt — session-level | IE measurement lacks signal; methodology re-ratification required |

### Cell 4 — Model + tokenizer load

**Specialist:** memit-specialist

**Purpose:** Load Llama-3.1-8B (base) onto pod GPU with canonical fp16 device_map. Carry-forward from v1.5 Cell 5 model-load pattern; trace runs on the same model + tokenizer state.

**References:** Carry-forward from v1.5 §Cell 5; Pad-Token patch state verified at Cell 2

```python
# === CELL 4 — Model + tokenizer load ===
# Specialist: memit-specialist
# References: v1.5 Cell 5 carry-forward; §1.4 Pad-Token

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "meta-llama/Llama-3.1-8B"

print(f"Cell 4: loading {MODEL_NAME} ...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# Pad-Token patch: tokenizer.pad_token = tokenizer.eos_token (canonical Llama
# pad-token assignment; per S2.7 OQ-S26-13 closure)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map={"": "cuda:0"},  # single-GPU pod; trivial dispatch
)
model.eval()

# Cross-check subject token IDs from Cell 3 against current tokenizer
import json
with open("/workspace/causal_trace/trace_prompt_set.json") as f:
    trace_prompt_set = json.load(f)

mismatches = []
for fact in trace_prompt_set["facts"]:
    current_ids = tokenizer.encode(fact["subject"], add_special_tokens=False)
    if current_ids != fact["subject_token_ids"]:
        mismatches.append((fact["id"], fact["subject"],
                           fact["subject_token_ids"], current_ids))

if mismatches:
    for m in mismatches:
        print(f"  MISMATCH {m[0]} ({m[1]}): expected {m[2]}, got {m[3]}")
    raise RuntimeError("Cell 4 HALT: tokenizer subject token ID drift from S2.12-A capture.")

print(f"Cell 4: model loaded. "
      f"layers={len(model.model.layers)}, hidden={model.config.hidden_size}, "
      f"intermediate={model.config.intermediate_size}, vocab={model.config.vocab_size}")
print(f"  Subject token IDs cross-checked against S2.12-A capture: PASS")
print(f"  GPU memory after load: "
      f"{torch.cuda.memory_allocated() / (1024**3):.2f} GiB")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `len(model.model.layers)` | `32` |
| `model.config.hidden_size` | `4096` |
| `model.config.intermediate_size` | `14336` |
| `model.config.vocab_size` | `128256` |
| Subject token ID cross-check | All 5 facts PASS |
| GPU memory after load | `~15 GiB` (fp16 baseline; ~9 GiB headroom for trace passes) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Subject token ID drift | Hard halt — session-level | Tokenizer state non-deterministic vs S2.12-A; HALT until reconciled |
| Model load OOM | Hard halt — pod-level | Investigate prior pod memory state; HALT |

---

## Block 2 — Clean + corrupted forward passes (Cells 5–6)

### Cell 5 — Clean forward pass with hidden-state capture

**Specialist:** memit-specialist

**Purpose:** Per fact, run a clean forward pass on the canonical prompt and capture: (a) per-(layer, token) residual stream output, (b) per-(layer, token) MLP output, (c) per-(layer, token) attention output (informational; M6 secondary), (d) `P_clean(target_TRUE)`, (e) embedding_std on subject token positions (gates σ scaling at Cell 6/7).

**References:** D-S214D-METHOD-2 (embedding_std), D-S214D-METHOD-6 (decomposition); Meng et al. canonical hook layout

```python
# === CELL 5 — Clean forward pass with hidden-state capture ===
# Specialist: memit-specialist
# References: D-S214D-METHOD-2; D-S214D-METHOD-6

import json
import numpy as np
import torch

clean_states = {}      # fact_id → {"residual": [n_layers, seq, hidden],
                       #             "mlp_out": [n_layers, seq, hidden],
                       #             "attn_out": [n_layers, seq, hidden]}
clean_baselines = {}   # fact_id → {"prompt_tokens": [...], "p_target_TRUE": float,
                       #            "top5": [...], "embedding_std": float, ...}

n_layers = len(model.model.layers)
hidden_size = model.config.hidden_size

for fact in trace_prompt_set["facts"]:
    fact_id = fact["id"]
    prompt_text = fact["canonical_prompt"]
    target_TRUE_id = fact["target_TRUE_id"]

    # Tokenize
    inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda:0")
    input_ids = inputs["input_ids"]  # [1, seq_len]
    seq_len = input_ids.shape[1]

    # Identify subject token positions in the tokenized prompt.
    # Subject is the first content tokens after BOS; canonical prompt = "{subject} plays the sport of"
    # Approach: re-tokenize subject alone (with leading space convention from prior cells)
    # then locate the contiguous span in input_ids.
    subject_ids = fact["subject_token_ids"]
    # Locate subject span: search for first occurrence of subject_ids in input_ids[0]
    # (post-BOS; BOS is at position 0 for Llama)
    subject_span_start = None
    for i in range(1, seq_len - len(subject_ids) + 1):
        if input_ids[0, i:i + len(subject_ids)].tolist() == subject_ids:
            subject_span_start = i
            break
    assert subject_span_start is not None, (
        f"Cell 5 HALT for {fact_id}: subject token span not located in prompt tokenization. "
        f"Investigate prompt template or tokenizer state."
    )
    subject_token_indices = list(range(subject_span_start, subject_span_start + len(subject_ids)))

    # Storage: [n_layers, seq_len, hidden]
    residual_capture = torch.zeros(n_layers, seq_len, hidden_size,
                                    dtype=torch.float16, device="cuda:0")
    mlp_capture = torch.zeros(n_layers, seq_len, hidden_size,
                               dtype=torch.float16, device="cuda:0")
    attn_capture = torch.zeros(n_layers, seq_len, hidden_size,
                                dtype=torch.float16, device="cuda:0")

    handles = []

    def make_layer_hook(layer_idx, store):
        def hook(module, inputs, output):
            # output for LlamaDecoderLayer is (hidden_states, ...)
            store[layer_idx] = output[0].detach()[0]  # [seq, hidden]
        return hook

    def make_mlp_hook(layer_idx, store):
        def hook(module, inputs, output):
            # output of LlamaMLP is the MLP delta (pre-residual-add)
            store[layer_idx] = output.detach()[0]
        return hook

    def make_attn_hook(layer_idx, store):
        def hook(module, inputs, output):
            # output of LlamaAttention (or self_attn) is (attn_output, ...)
            attn_out = output[0] if isinstance(output, tuple) else output
            store[layer_idx] = attn_out.detach()[0]
        return hook

    for L in range(n_layers):
        h_layer = model.model.layers[L].register_forward_hook(
            make_layer_hook(L, residual_capture))
        h_mlp = model.model.layers[L].mlp.register_forward_hook(
            make_mlp_hook(L, mlp_capture))
        h_attn = model.model.layers[L].self_attn.register_forward_hook(
            make_attn_hook(L, attn_capture))
        handles.extend([h_layer, h_mlp, h_attn])

    with torch.no_grad():
        outputs = model(**inputs)

    for h in handles:
        h.remove()

    # Last-token logits → P(target_TRUE)
    logits = outputs.logits[0, -1, :]  # [vocab]
    probs = torch.softmax(logits.float(), dim=-1)
    p_target_TRUE = float(probs[target_TRUE_id])
    top5_probs, top5_ids = torch.topk(probs, k=5)
    top5 = [(int(i), tokenizer.decode([int(i)]), float(p))
            for i, p in zip(top5_ids, top5_probs)]

    # embedding_std on subject token positions (per D-S214D-METHOD-2)
    # Capture from input embeddings (model.model.embed_tokens output at subject positions)
    with torch.no_grad():
        input_embeds = model.model.embed_tokens(input_ids)  # [1, seq, hidden]
    subject_embeds = input_embeds[0, subject_token_indices, :]  # [n_subj_tokens, hidden]
    embedding_std = float(subject_embeds.float().std())

    clean_states[fact_id] = {
        "residual": residual_capture.cpu(),
        "mlp_out": mlp_capture.cpu(),
        "attn_out": attn_capture.cpu(),
    }
    clean_baselines[fact_id] = {
        "prompt_tokens": input_ids[0].cpu().tolist(),
        "prompt_token_strs": [tokenizer.decode([t]) for t in input_ids[0].cpu().tolist()],
        "seq_len": int(seq_len),
        "subject_token_indices": subject_token_indices,
        "embedding_std": embedding_std,
        "p_target_TRUE": p_target_TRUE,
        "top5": top5,
    }

    print(f"  {fact_id}: seq_len={seq_len}  subj_idx={subject_token_indices}  "
          f"embed_std={embedding_std:.4f}  P(target_TRUE)={p_target_TRUE:.4f}")

with open("/workspace/causal_trace/baseline_clean_pass.json", "w") as f:
    json.dump(clean_baselines, f, indent=2)

print(f"\nCell 5: clean forward pass captured for 5 facts.")
print(f"  Hidden states: residual+mlp+attn × {n_layers} layers × seq × hidden")
print(f"  Total transient memory: ~{5 * 3 * n_layers * 12 * hidden_size * 2 / (1024**3):.2f} GiB (rough; per-fact varies)")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `clean_states[fact_id]["residual"].shape` | `[32, seq_len, 4096]` per fact |
| `clean_baselines[fact_id]["p_target_TRUE"]` ≥ 0.10 | All 5 facts (matches Cell 3 baseline floor) |
| `clean_baselines[fact_id]["top5"][0][0]` | Equals `fact["target_TRUE_id"]` (top-1 IS target_TRUE; sport-cluster pretraining recall) |
| `clean_baselines[fact_id]["embedding_std"]` | Order-of-magnitude `~0.01–0.05` (Llama embedding scale) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Subject token span not located | Hard halt — fact-level | Tokenizer drift or prompt template error; HALT |
| `p_target_TRUE` < 0.10 at clean run | Hard halt — fact-level | Cell 3 baseline disagrees with Cell 5 clean run; investigate |
| Top-1 ≠ target_TRUE | Soft halt | Log; trace can proceed but verdict aggregation may need per-fact handling |
| GPU memory > 22 GiB during capture | Soft halt | Reduce capture precision (fp16 already; consider per-fact capture-then-cpu offload — but already implemented above) |

### Cell 6 — Corrupted forward pass

**Specialist:** memit-specialist

**Purpose:** Per fact, run N=10 corrupted forward passes (Gaussian noise σ=3·embedding_std added to subject token embeddings) and capture aggregate `P_corrupted(target_TRUE)`. Verifies the IE measurement gap exists: `P_clean − P_corrupted` must be substantial (>0.20 absolute, per Meng et al. canonical) for layer × token IE peaks to be detectable.

**References:** D-S214D-METHOD-2; OQ-S214D-D1-2 (σ calibration verification gate)

```python
# === CELL 6 — Corrupted forward pass ===
# Specialist: memit-specialist
# References: D-S214D-METHOD-2; OQ-S214D-D1-2

import json
import numpy as np
import torch

N_NOISE_SAMPLES = 10
SIGMA_MULTIPLIER = 3.0
IE_GAP_FLOOR = 0.20  # P_clean - P_corrupted must exceed this for trace signal

corrupted_baselines = {}  # fact_id → {p_corrupted_per_sample: [...], p_corrupted_mean: float, ...}

torch.manual_seed(0)  # Reproducibility for noise samples

for fact in trace_prompt_set["facts"]:
    fact_id = fact["id"]
    prompt_text = fact["canonical_prompt"]
    target_TRUE_id = fact["target_TRUE_id"]
    subject_token_indices = clean_baselines[fact_id]["subject_token_indices"]
    embedding_std = clean_baselines[fact_id]["embedding_std"]
    sigma = SIGMA_MULTIPLIER * embedding_std

    inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda:0")
    input_ids = inputs["input_ids"]

    p_corrupted_per_sample = []

    for n in range(N_NOISE_SAMPLES):
        # Build noise-injection hook on embed_tokens
        def make_noise_hook(subj_idx, sig, sample_seed):
            generator = torch.Generator(device="cuda:0").manual_seed(sample_seed)
            def hook(module, inputs, output):
                # output: [batch, seq, hidden]
                noise = torch.randn(output.shape, dtype=output.dtype,
                                    device=output.device, generator=generator) * sig
                # Apply noise ONLY to subject token positions
                mask = torch.zeros_like(output)
                for idx in subj_idx:
                    mask[:, idx, :] = 1.0
                return output + noise * mask
            return hook

        seed = hash((fact_id, n)) % (2**31)
        h = model.model.embed_tokens.register_forward_hook(
            make_noise_hook(subject_token_indices, sigma, seed))

        with torch.no_grad():
            out = model(**inputs)

        h.remove()

        logits = out.logits[0, -1, :]
        probs = torch.softmax(logits.float(), dim=-1)
        p = float(probs[target_TRUE_id])
        p_corrupted_per_sample.append(p)

    p_corrupted_mean = float(np.mean(p_corrupted_per_sample))
    p_corrupted_std = float(np.std(p_corrupted_per_sample))
    p_clean = clean_baselines[fact_id]["p_target_TRUE"]
    ie_gap = p_clean - p_corrupted_mean
    gap_above_floor = ie_gap >= IE_GAP_FLOOR

    corrupted_baselines[fact_id] = {
        "sigma": sigma,
        "n_samples": N_NOISE_SAMPLES,
        "p_corrupted_per_sample": p_corrupted_per_sample,
        "p_corrupted_mean": p_corrupted_mean,
        "p_corrupted_std": p_corrupted_std,
        "p_clean": p_clean,
        "ie_gap": ie_gap,
        "gap_above_floor": gap_above_floor,
    }

    print(f"  {fact_id}: σ={sigma:.4f}  P_clean={p_clean:.4f}  "
          f"P_corrupted={p_corrupted_mean:.4f}±{p_corrupted_std:.4f}  "
          f"gap={ie_gap:.4f} {'✓' if gap_above_floor else '✗ BELOW FLOOR'}")

with open("/workspace/causal_trace/corrupted_pass.json", "w") as f:
    json.dump(corrupted_baselines, f, indent=2)

all_gaps_above_floor = all(b["gap_above_floor"] for b in corrupted_baselines.values())

assert all_gaps_above_floor, (
    f"Cell 6 HALT: one or more facts has IE gap < {IE_GAP_FLOOR}. "
    f"Corruption σ={SIGMA_MULTIPLIER}·embed_std insufficient to disrupt recall. "
    f"OQ-S214D-D1-2 surfaces — investigate σ scaling. Options: "
    f"(a) increase σ multiplier (re-ratify D-S214D-METHOD-2); "
    f"(b) corrupt all token positions vs subject-only (re-ratify D-S214D-METHOD-2); "
    f"(c) substitute facts with higher P_clean (re-ratify D-S214D-METHOD-1)."
)

print(f"\nCell 6: corruption gap verified for all 5 facts. "
      f"OQ-S214D-D1-2 closes empirically.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `corrupted_baselines[fact_id]["ie_gap"]` ≥ 0.20 | All 5 facts |
| `corrupted_baselines[fact_id]["p_corrupted_std"]` | Order `~0.01–0.05` (low noise variance per Meng et al.) |
| `all_gaps_above_floor` | `True` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any `ie_gap` < 0.20 | Hard halt — session-level | OQ-S214D-D1-2 surfaces; methodology re-ratification required (σ scaling, corruption span, or trace fact substitution) |
| `p_corrupted_std` > 0.10 (high variance) | Soft halt | Increase N_NOISE_SAMPLES; log; trace can proceed with widened CI |

---

## Block 3 — Trace execution + verdict (Cells 7–8)

### Cell 7 — Causal trace execution loop

**Specialist:** memit-specialist

**Purpose:** Per fact × per (layer L, token T) × per intervention_target ∈ {residual, MLP_output} × per noise sample, run a corrupted-forward-with-clean-state-patch pass and capture `P_patched(target_TRUE)`. Compute IE per (L, T, target). Aggregate into mediation maps.

**References:** D-S214D-METHOD-3 (full layer scope); D-S214D-METHOD-4 (full token scope); D-S214D-METHOD-5 (IE metric); D-S214D-METHOD-6 (residual + MLP decomposition)

```python
# === CELL 7 — Causal trace execution loop ===
# Specialist: memit-specialist
# References: D-S214D-METHOD-3, METHOD-4, METHOD-5, METHOD-6
# Storage: per-fact per-(layer, token, target) IE, aggregated to mediation maps

import json
import time
import numpy as np
import torch

# Determine max sequence length across facts (for padded storage shape)
max_seq_len = max(clean_baselines[f["id"]]["seq_len"] for f in trace_prompt_set["facts"])
n_layers = len(model.model.layers)
n_facts = len(trace_prompt_set["facts"])

# Mediation map storage: [n_facts, n_layers, max_seq_len]
# Two intervention targets: residual stream after layer, MLP output (pre-residual-add)
ie_map_residual = np.full((n_facts, n_layers, max_seq_len), np.nan, dtype=np.float32)
ie_map_mlp = np.full((n_facts, n_layers, max_seq_len), np.nan, dtype=np.float32)

# Token-position mask (which positions are valid per fact)
seq_lens = [clean_baselines[f["id"]]["seq_len"] for f in trace_prompt_set["facts"]]

t_start_global = time.time()

for fact_idx, fact in enumerate(trace_prompt_set["facts"]):
    fact_id = fact["id"]
    prompt_text = fact["canonical_prompt"]
    target_TRUE_id = fact["target_TRUE_id"]
    subject_token_indices = clean_baselines[fact_id]["subject_token_indices"]
    embedding_std = clean_baselines[fact_id]["embedding_std"]
    sigma = corrupted_baselines[fact_id]["sigma"]
    p_corrupted_mean = corrupted_baselines[fact_id]["p_corrupted_mean"]
    seq_len = clean_baselines[fact_id]["seq_len"]

    inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda:0")

    # Move clean states for this fact back to GPU for patching
    fact_clean_residual = clean_states[fact_id]["residual"].to("cuda:0")  # [n_layers, seq, hidden]
    fact_clean_mlp = clean_states[fact_id]["mlp_out"].to("cuda:0")

    t_fact_start = time.time()

    for L in range(n_layers):
        for T in range(seq_len):
            # ==== Intervention target: residual stream after layer L, position T ====
            ie_residual_samples = []
            for n in range(N_NOISE_SAMPLES):
                seed = hash((fact_id, L, T, "residual", n)) % (2**31)

                # Noise hook on embed_tokens
                gen_noise = torch.Generator(device="cuda:0").manual_seed(seed)
                def make_noise_hook():
                    def hook(module, inputs, output):
                        noise = torch.randn(output.shape, dtype=output.dtype,
                                            device=output.device, generator=gen_noise) * sigma
                        mask = torch.zeros_like(output)
                        for idx in subject_token_indices:
                            mask[:, idx, :] = 1.0
                        return output + noise * mask
                    return hook

                # Patch hook on layer L: at token T, replace residual with clean state
                clean_T_residual = fact_clean_residual[L, T, :]
                def make_patch_residual_hook(layer_idx, token_idx, clean_state):
                    def hook(module, inputs, output):
                        # output: (hidden_states, ...)
                        new_hidden = output[0].clone()
                        new_hidden[0, token_idx, :] = clean_state.to(new_hidden.dtype)
                        return (new_hidden,) + output[1:]
                    return hook

                h_noise = model.model.embed_tokens.register_forward_hook(make_noise_hook())
                h_patch = model.model.layers[L].register_forward_hook(
                    make_patch_residual_hook(L, T, clean_T_residual))

                with torch.no_grad():
                    out = model(**inputs)

                h_noise.remove()
                h_patch.remove()

                p = float(torch.softmax(out.logits[0, -1, :].float(), dim=-1)[target_TRUE_id])
                ie_residual_samples.append(p - p_corrupted_mean)

            ie_map_residual[fact_idx, L, T] = float(np.mean(ie_residual_samples))

            # ==== Intervention target: MLP output at layer L, position T ====
            ie_mlp_samples = []
            for n in range(N_NOISE_SAMPLES):
                seed = hash((fact_id, L, T, "mlp", n)) % (2**31)
                gen_noise = torch.Generator(device="cuda:0").manual_seed(seed)
                def make_noise_hook():
                    def hook(module, inputs, output):
                        noise = torch.randn(output.shape, dtype=output.dtype,
                                            device=output.device, generator=gen_noise) * sigma
                        mask = torch.zeros_like(output)
                        for idx in subject_token_indices:
                            mask[:, idx, :] = 1.0
                        return output + noise * mask
                    return hook

                clean_T_mlp = fact_clean_mlp[L, T, :]
                def make_patch_mlp_hook(layer_idx, token_idx, clean_state):
                    def hook(module, inputs, output):
                        # output: MLP delta (pre-residual-add); shape [batch, seq, hidden]
                        new_out = output.clone()
                        new_out[0, token_idx, :] = clean_state.to(new_out.dtype)
                        return new_out
                    return hook

                h_noise = model.model.embed_tokens.register_forward_hook(make_noise_hook())
                h_patch = model.model.layers[L].mlp.register_forward_hook(
                    make_patch_mlp_hook(L, T, clean_T_mlp))

                with torch.no_grad():
                    out = model(**inputs)

                h_noise.remove()
                h_patch.remove()

                p = float(torch.softmax(out.logits[0, -1, :].float(), dim=-1)[target_TRUE_id])
                ie_mlp_samples.append(p - p_corrupted_mean)

            ie_map_mlp[fact_idx, L, T] = float(np.mean(ie_mlp_samples))

        # Per-layer log
        if L % 4 == 0:
            elapsed_fact = time.time() - t_fact_start
            print(f"    {fact_id} L={L:2d} done; elapsed_fact={elapsed_fact:.1f}s")

    # Free GPU clean states for this fact (save VRAM for next fact)
    del fact_clean_residual, fact_clean_mlp
    torch.cuda.empty_cache()

    elapsed_fact_total = time.time() - t_fact_start
    print(f"  {fact_id} complete: {elapsed_fact_total:.1f}s "
          f"({elapsed_fact_total / (n_layers * seq_len * 2 * N_NOISE_SAMPLES) * 1000:.1f} ms/pass)")

t_total = time.time() - t_start_global

# Save mediation maps
np.savez_compressed("/workspace/causal_trace/mediation_map_residual.npz",
                    ie=ie_map_residual,
                    seq_lens=np.array(seq_lens),
                    fact_ids=np.array([f["id"] for f in trace_prompt_set["facts"]]))
np.savez_compressed("/workspace/causal_trace/mediation_map_mlp.npz",
                    ie=ie_map_mlp,
                    seq_lens=np.array(seq_lens),
                    fact_ids=np.array([f["id"] for f in trace_prompt_set["facts"]]))

print(f"\nCell 7: trace execution complete. Total wall time: {t_total / 60:.1f} min")
print(f"  Mediation maps saved (residual + MLP) at /workspace/causal_trace/")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `ie_map_residual.shape` | `[5, 32, max_seq_len]` |
| `ie_map_mlp.shape` | `[5, 32, max_seq_len]` |
| Per-fact per-token-position non-NaN slice | Length = `seq_len` for that fact |
| Total wall time | `~80–100 min` (5 facts × 32 layers × ~10 tokens × 2 targets × 10 samples × ~150ms) |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| GPU OOM during patch hook | Hard halt — pod-level | Reduce N_NOISE_SAMPLES to 5; log; re-execute affected fact |
| Per-fact wall time > 30 min | Soft halt | Log; consider parallelizing across noise samples in a future v0.2 |
| All IE values near zero | Soft halt | Investigate hook attachment; the clean-state patch may not be effective; verify hidden-state shapes |

### Cell 8 — Mediation analysis + D.1 verdict

**Specialist:** memit-specialist (primary; verdict authorship); validation-contract-architect (verdict predicate review)

**Purpose:** Aggregate mediation maps across the 5 facts, identify (L_R, T_R) and (L_M, T_M) global peaks, apply the D.1 verdict predicate from §3.8, and write the verdict + forward routing to NV.

**References:** §1.2 verdict table; §3.8 verdict predicate; D-S214D-METHOD-5; OQ-S214D-D1-3

```python
# === CELL 8 — Mediation analysis + D.1 verdict ===
# Specialist: memit-specialist (primary); validation-contract-architect (review)
# References: §1.2; §3.8; D-S214D-METHOD-5; OQ-S214D-D1-3

import json
import numpy as np
from datetime import datetime, timezone

# Load mediation maps
res = np.load("/workspace/causal_trace/mediation_map_residual.npz", allow_pickle=True)
mlp = np.load("/workspace/causal_trace/mediation_map_mlp.npz", allow_pickle=True)
ie_residual = res["ie"]   # [n_facts, n_layers, max_seq_len]
ie_mlp = mlp["ie"]
fact_ids = list(res["fact_ids"])
seq_lens = res["seq_lens"]

n_facts, n_layers, max_seq = ie_residual.shape

# Aggregate: mean across facts (NaN-aware)
ie_residual_agg = np.nanmean(ie_residual, axis=0)  # [n_layers, max_seq_len]
ie_mlp_agg = np.nanmean(ie_mlp, axis=0)

# Per-layer max IE across token positions (D-S214D-METHOD-5: per-layer mediation = max(IE) over tokens)
per_layer_residual = np.nanmax(ie_residual_agg, axis=1)  # [n_layers]
per_layer_mlp = np.nanmax(ie_mlp_agg, axis=1)

# Global peaks: (L, T) of argmax(IE)
flat_residual = np.unravel_index(np.nanargmax(ie_residual_agg), ie_residual_agg.shape)
flat_mlp = np.unravel_index(np.nanargmax(ie_mlp_agg), ie_mlp_agg.shape)
L_R, T_R = int(flat_residual[0]), int(flat_residual[1])
L_M, T_M = int(flat_mlp[0]), int(flat_mlp[1])
peak_residual_ie = float(ie_residual_agg[L_R, T_R])
peak_mlp_ie = float(ie_mlp_agg[L_M, T_M])

# Per-fact peaks (informational; gates OQ-S214D-D1-1 stability check)
per_fact_peaks = []
for f_idx, fact_id in enumerate(fact_ids):
    fact_id_str = fact_id.item() if hasattr(fact_id, 'item') else str(fact_id)
    fr = np.unravel_index(np.nanargmax(ie_residual[f_idx]), ie_residual[f_idx].shape)
    fm = np.unravel_index(np.nanargmax(ie_mlp[f_idx]), ie_mlp[f_idx].shape)
    per_fact_peaks.append({
        "fact_id": fact_id_str,
        "L_R_fact": int(fr[0]), "T_R_fact": int(fr[1]),
        "L_M_fact": int(fm[0]), "T_M_fact": int(fm[1]),
        "peak_residual_ie_fact": float(ie_residual[f_idx, fr[0], fr[1]]),
        "peak_mlp_ie_fact": float(ie_mlp[f_idx, fm[0], fm[1]]),
    })

# Stability check (OQ-S214D-D1-1): are per-fact L_M peaks within ±2 layers of aggregate L_M?
per_fact_lm = [p["L_M_fact"] for p in per_fact_peaks]
lm_max_dev = max(abs(lm - L_M) for lm in per_fact_lm)
oq_d1_1_close = lm_max_dev <= 2

# === Verdict predicate (per §3.8 / §1.2) ===

MEMIT_LAYER_SET = set(range(4, 9))  # [4, 5, 6, 7, 8]

L_R_in_memit = L_R in MEMIT_LAYER_SET
L_M_in_memit = L_M in MEMIT_LAYER_SET
peaks_coincide = abs(L_R - L_M) <= 2  # informational threshold

if L_M_in_memit and L_R_in_memit:
    verdict_class = "D.1-PASS-LAYER-SET"
    routing = "Layer set CORRECT on Llama-3.1-8B. D.3 verdict gates next routing."
elif (not L_M_in_memit) and peaks_coincide:
    verdict_class = "D.1-FAIL-LAYER-SET"
    routing = (
        f"Layer set INCORRECT. D.2 narrowed to L_M ± 4 = "
        f"L[{max(0, L_M - 4)}..{min(31, L_M + 4)}] window."
    )
elif L_M_in_memit and (not peaks_coincide):
    verdict_class = "D.1-PASS-LAYER-SET-AMBIGUOUS-MECHANISM"
    routing = (
        "Layer set CORRECT for MLP-mediation; residual peak elsewhere "
        "(attention-mediated). D.3 verdict load-bearing; if D.3 FAIL, "
        "T.2 alt write engine surfaces."
    )
else:
    verdict_class = "D.1-FAIL-LAYER-SET-AND-MECHANISM"
    routing = (
        "Both layer set AND edit mechanism suspect. T.2 alt write engine "
        "surfaces directly (z-vector + MLP-edit geometry mismatch on Llama-3.1-8B)."
    )

verdict = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session_label": "S2.14-D / D.1 causal trace / v0.1",
    "methodology_decisions": [
        "D-S214D-METHOD-1", "D-S214D-METHOD-2", "D-S214D-METHOD-3",
        "D-S214D-METHOD-4", "D-S214D-METHOD-5", "D-S214D-METHOD-6",
    ],
    "n_facts": n_facts,
    "n_layers": n_layers,
    "memit_layer_set": sorted(MEMIT_LAYER_SET),
    "aggregate_peaks": {
        "L_R": L_R, "T_R": T_R, "peak_residual_ie": peak_residual_ie,
        "L_M": L_M, "T_M": T_M, "peak_mlp_ie": peak_mlp_ie,
    },
    "per_fact_peaks": per_fact_peaks,
    "stability": {
        "lm_max_dev_from_aggregate": lm_max_dev,
        "oq_s214d_d1_1_close": oq_d1_1_close,
    },
    "per_layer_residual_max": per_layer_residual.tolist(),
    "per_layer_mlp_max": per_layer_mlp.tolist(),
    "predicate_inputs": {
        "L_R_in_memit_layer_set": L_R_in_memit,
        "L_M_in_memit_layer_set": L_M_in_memit,
        "peaks_coincide_within_2_layers": peaks_coincide,
    },
    "verdict_class": verdict_class,
    "forward_routing": routing,
}

with open("/workspace/causal_trace/mediation_verdict.json", "w") as f:
    json.dump(verdict, f, indent=2)

# Session log (human-readable)
log_lines = [
    "=" * 70,
    f"D.1 CAUSAL TRACE — Mediation Verdict",
    f"Session: S2.14-D / D.1 / v0.1",
    f"Captured: {verdict['captured_at']}",
    "=" * 70,
    "",
    f"Aggregate (mean across {n_facts} facts):",
    f"  Residual peak: L={L_R} T={T_R}  IE={peak_residual_ie:.4f}",
    f"  MLP peak:      L={L_M} T={T_M}  IE={peak_mlp_ie:.4f}",
    "",
    f"Per-layer max IE (residual):",
    *[f"  L={L:2d}: {v:.4f}" for L, v in enumerate(per_layer_residual.tolist())],
    "",
    f"Per-layer max IE (MLP-output):",
    *[f"  L={L:2d}: {v:.4f}" for L, v in enumerate(per_layer_mlp.tolist())],
    "",
    f"Per-fact L_M stability: max_dev={lm_max_dev}  "
    f"(OQ-S214D-D1-1 {'CLOSE' if oq_d1_1_close else 'OPEN'})",
    "",
    f"Predicate inputs:",
    f"  L_R={L_R} ∈ MEMIT [4..8]? {L_R_in_memit}",
    f"  L_M={L_M} ∈ MEMIT [4..8]? {L_M_in_memit}",
    f"  |L_R - L_M| <= 2 (peaks coincide)? {peaks_coincide}",
    "",
    f"VERDICT: {verdict_class}",
    f"ROUTING: {routing}",
    "=" * 70,
]

with open("/workspace/causal_trace/causal_trace_session_log.txt", "w") as f:
    f.write("\n".join(log_lines))

for line in log_lines:
    print(line)
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `aggregate_peaks.peak_residual_ie` | > 0.05 (substantial mediation; Meng et al. canonical lower bound for credible peak) |
| `aggregate_peaks.peak_mlp_ie` | > 0.05 |
| `stability.lm_max_dev_from_aggregate` | ≤ 2 (per-fact stability of MLP-output peak; OQ-S214D-D1-1 closure) |
| `verdict_class` | One of `D.1-PASS-LAYER-SET` / `D.1-FAIL-LAYER-SET` / `D.1-PASS-LAYER-SET-AMBIGUOUS-MECHANISM` / `D.1-FAIL-LAYER-SET-AND-MECHANISM` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `peak_mlp_ie` < 0.02 | Soft halt | MLP-output mediation is at noise floor — IE measurement may have failed; investigate hook semantics |
| `lm_max_dev_from_aggregate` > 4 | Soft halt | Per-fact peaks unstable; OQ-S214D-D1-1 OPEN; verdict carries provisional flag |
| Verdict produces no clean predicate match | Hard halt — verdict-level | Predicate logic gap; re-author §3.8 routing table |

---

# Part III — Verdict predicate, traceability, NV state

## §3.8 — D.1 verdict predicate (canonical)

| L_R ∈ [4..8] | L_M ∈ [4..8] | \|L_R − L_M\| ≤ 2 | Verdict class | Routing |
|---|---|---|---|---|
| Yes | Yes | (any) | `D.1-PASS-LAYER-SET` | Layer set correct; D.3 gates next |
| (any) | No | Yes | `D.1-FAIL-LAYER-SET` | D.2 narrowed to L_M ± 4 |
| No | Yes | No | `D.1-PASS-LAYER-SET-AMBIGUOUS-MECHANISM` | D.3 load-bearing; T.2 conditional |
| No | No | No | `D.1-FAIL-LAYER-SET-AND-MECHANISM` | T.2 alt write engine surfaces |

The predicate is exhaustive over the 2 × 2 × 2 condition space modulo the (any) marginalizations; Cell 8 implements the predicate in conditional cascade order matching this table.

## §3.9 — Interface contracts surfaced at v0.1

**IC-S214D-D1-1 — Trace prompt set inheritance contract**

| Field | Value |
|---|---|
| From | `stage_1_token_verification.json` (S2.12-A capture) + `stage_1_llama_baselines.json` (S2.12-A Cell 7) |
| To | `trace_prompt_set.json` (D.1 Cell 3 output) |
| What source exposes | 5-fact subject token IDs (durable; tokenizer-deterministic); 5-fact sport-relation natural top-1 (target_TRUE) + baseline P(target_TRUE) |
| Conditions | Both source files NV-resident at session start; subject token IDs cross-check at Cell 4 model load (tokenizer determinism gate) |
| Failure behavior | Cell 3 hard halt if either source absent; Cell 4 hard halt on subject token ID drift |

**IC-S214D-D1-2 — D.1 verdict predicate contract**

| Field | Value |
|---|---|
| From | `mediation_verdict.json` (Cell 8 output) |
| To | `session_2_14_d_summary_block.md` + `s214_d_to_next_session_handoff_guide.md` |
| What source exposes | (L_R, T_R, peak_residual_ie); (L_M, T_M, peak_mlp_ie); per-layer max IE arrays; per-fact peaks; stability metric; verdict_class enum; forward routing string |
| Conditions | All Cell 8 verification anchors PASS; `verdict_class` matches one of four canonical classes |
| Failure behavior | Verdict class outside the canonical four → predicate gap; halt; re-author §3.8 |

## §3.10 — NV-resident artifact paths (final state at v0.1 close)

```
/workspace/causal_trace/
  ├── causal_trace_environment_fingerprint.json      (Cell 1)
  ├── causal_trace_patch_state.json                  (Cell 2)
  ├── trace_prompt_set.json                          (Cell 3)
  ├── baseline_clean_pass.json                       (Cell 5)
  ├── corrupted_pass.json                            (Cell 6)
  ├── mediation_map_residual.npz                     (Cell 7)
  ├── mediation_map_mlp.npz                          (Cell 7)
  ├── mediation_verdict.json                         (Cell 8)
  └── causal_trace_session_log.txt                   (Cell 8)
```

**Inputs (carry-forward; consumed by D.1 cells, not modified):**
```
/workspace/architecture_profile/
  ├── meta-llama_Llama-3.1-8B.json                   (S2.5a; consumed by Cell 4)
  ├── stage_1_token_verification.json                (S2.12-A; consumed by Cell 3, cross-check Cell 4)
  └── stage_1_llama_baselines.json                   (S2.12-A; consumed by Cell 3)
```

## §3.11 — Open questions surfaced at v0.1

| OQ ID | Origin | Status | Closes when |
|---|---|---|---|
| **OQ-S214D-D1-1** | v0.1 §1.2 (per-fact stability of L_M aggregate peak) | OPEN at authoring; closes empirically at Cell 8 if `lm_max_dev_from_aggregate` ≤ 2 | Cell 8 stability check |
| **OQ-S214D-D1-2** | v0.1 §1.2 (corruption σ calibration; whether σ=3·embed_std produces sufficient IE gap) | OPEN at authoring; closes empirically at Cell 6 if all 5 facts have `ie_gap` ≥ 0.20 | Cell 6 floor check |
| **OQ-S214D-D1-3** | v0.1 §3.8 (residual vs MLP peak coincidence informational status) | OPEN; informational only — not load-bearing for verdict (predicate handles all four conditions explicitly) | Deferred; not blocking |

## §3.12 — Decisions ratified at v0.1 authoring

| ID | Decision |
|---|---|
| **D-S214D-RUNBOOK-1** | `causal_trace_runbook.md` v0.1 authored at S2.14-D; 8 cells; methodology lock M1–M6 binding; PROVISIONAL until Cell 8 verdict produced |
| **D-S214D-PATCH-SCOPE-1** | Forward-pass-only trace; only Pad-Token and P-4 load-bearing; remaining patches carry-forward from v1.5 NV state but informational at v0.1 |
| **D-S214D-METHOD-1..6** | Methodology lock per §1.5 (corpus inheritance; corruption scheme; layer scope; token-position scope; mediation metric; hidden-state decomposition) |

## §3.13 — Non-goals at v0.1

This runbook does NOT:
- Apply MEMIT edits or invoke any edit-time machinery (forward-pass-only)
- Compute or refresh covariance caches
- Authorize routing to D.2 or T.2 — verdict at Cell 8 surfaces routing recommendations; ratification happens at session_2_14_d_summary_block.md authoring
- Re-author cfb-v3 corpus or probe-set-v3 (out of scope per S2.14-D kickoff)
- Substitute for Stage 1 SECT consistency-probe verdict — D.1 is mechanistic only, not behavioral

---

# End of causal_trace_runbook v0.1

> Authoring ratified at S2.14-D; PROVISIONAL until verdict execution.
> Successor revision triggers: (a) Cell 8 verdict surfaces predicate gap (re-author §3.8); (b) OQ-S214D-D1-2 OPEN at execution → methodology re-ratification; (c) extension to 10-fact trace set per OQ-S214D-D1-1 deferred surface.
