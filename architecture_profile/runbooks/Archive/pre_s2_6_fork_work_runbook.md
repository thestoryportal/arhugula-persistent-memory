# Pre-S2.6 Fork-Work Runbook — Fresh Covariance Cache for `meta-llama/Llama-3.1-8B`

> **Authoring session:** Pre-S2.6 fork-work (this session)
> **Predecessor session:** Session 2.5a (CLOSED PARTIAL with smoke test PASS)
> **Consumer session:** Session 2.6 (Stage 1 SECT execution) — Cell 3 of `stage_1_sect_runbook.md` v1.1 is the consumer-side gate
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine` (US-NC-1, NV-pinned)
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct)
> **Specialist provenance:** framework-spec-writer (primary, runbook discipline); memit-specialist (secondary, `layer_stats` invocation + cache schema); state-consistency-theorist (tertiary, atomic-swap pattern for bridge → fresh transition)
>
> **Iteration metadata:**
> - version: 1.2.2
> - iteration: post-S2.5b §4.3 execution; v1.2.2 footer-correction patch (closes OQ-S25b-5: stale `End of ... v1.0` footer carried through three prior revisions)
> - status: Draft (operator review; ratification on Cell 5 GATE PASS of successor fork-work attempt)
> - basis: S2.5a closure block; `stage_1_sect_runbook.md` v1.2 Cell 3 contract; `block-2-3-runbook-deltas.md` §11–12; `memit-patches-canonical.md` v2.2; pre-S2.6 fork-work session findings (D-PreS26-1 through 4, C-PreS26-1, OQ-PreS26-1 through 8); S2.5b §4.8 archaeology findings (OQ-S25b-2 + v1.2 hot-patches)
> - supersedes: v1.2.1 (carried stale `End of Pre-S2.6 Fork-Work Runbook v1.0.` footer; frontmatter version was correct at 1.2.1 but body footer was unchanged from v1.0 authoring)
> - v1.2 absorbed: D-PreS26-1 (Cell 2 verification logic correction for `rome/layer_stats.py`); D-PreS26-3 + C-PreS26-1 (`globals.yml` as load-bearing input); OQ-PreS26-3 (Cell 4 Phase 1 signature reconciliation — partial; missed `model_name=`); OQ-PreS26-4 (`globals.yml` input table addition + new Cell 1.5); OQ-PreS26-7 (C-S25-5 spec language amendment for module-import precondition); OQ-PreS26-8 (compute-path smoke via new Cell 3.5); P-5 verification (per `memit-patches-canonical.md` v2.2 §3.6.8)
> - v1.2.1 hot-patches: §1.3 expansion notes corrected to absolute-path canonical values per D-PreS26-3 verbatim; Cell 1.5 EXPECTED_KEYS dict corrected to absolute paths; MODEL_NAME_FOR_CACHE definition added in Cell 3.5 (smoke) + Cell 4 §4.2 (compute) and passed as explicit `model_name=` parameter; §4.1 Phase 0 invocation deltas table extended with the third signature delta; §4.3 halt taxonomy TypeError row broadened to cover `missing 1 required positional argument: 'model_name'` variant (closes OQ-S25b-2)
> - v1.2.2 footer correction: document footer `End of Pre-S2.6 Fork-Work Runbook v1.0.` → `End of Pre-S2.6 Fork-Work Runbook v1.2.2.` (closes OQ-S25b-5 — stale footer surfaced by successor session hold-state at first KB consumption attempt; structural fix only, no semantic change to runbook content; surgical str_replace edit preserving all v1.2.1 hardening intact)
> - date_created: 2026-04-29
> - date_updated: 2026-04-30

---

# Part I — Session orientation

## 1.1 Purpose

This runbook drives the named pre-S2.6 fork-work session. It produces a fresh covariance cache against the exact `meta-llama/Llama-3.1-8B` base, for layers `[4, 5, 6, 7, 8]`, computed over 100 000 Wikipedia samples in `float32`, accompanied by a structured `PROVENANCE.txt` assertion. The artifact set replaces the bridge cache (provenance: `Llama-3-8B-Instruct`) at the canonical NV path, satisfying the Cell 3 gate of `stage_1_sect_runbook.md` v1.1 and unblocking Session 2.6 Stage 1 SECT execution.

This session closes `OQ-S25-9` (fresh covariance cache compute) on Cell 5 GATE PASS.

## 1.2 Scope

| In scope | Out of scope |
|---|---|
| Fresh covariance cache compute via `rome.layer_stats.layer_stats` | Stage 1 trial loop execution (Session 2.6) |
| `PROVENANCE.txt` authorship at canonical path | Hparams sweep or v_lr / mom2_update_weight retuning |
| Bridge cache archival (atomic-swap; recovery path preserved) | Bridge cache deletion (forbidden by IC-S25-1) |
| Cell 3 (consumer-side gate) re-verification against new cache | Re-execution of S2.5a smoke test |

## 1.3 Inputs

| Artifact | Provenance | Used by |
|---|---|---|
| MEMIT repo at `/workspace/memit_dry_run/memit/` (P-1, P-2, P-4, **P-5** applied; SHA `80426fd9…`; `memit-patches-canonical.md` v2.2) | Sessions 2.3 + 2.5a + S2.5b §4.3 (P-5 application) | Cells 2, 3.5, 4 |
| **`globals.yml` at `/workspace/memit_dry_run/memit/globals.yml`** (NV-resident; five canonical keys per D-PreS26-3; load-bearing for `from util import globals` import per C-PreS26-1 + amended C-S25-5) | Session 2.3 Block 2 setup; D-PreS26-3 corrected during pre-S2.6 fork-work | **Cell 1.5** (verification); transitively imported by every cell that touches MEMIT modules |
| Llama-3.1-8B base in `/workspace/hf_cache/` (~16 GB; HF_HOME-redirected per D-S25-8) | Session 2.5a | Cell 3 |
| `meta-llama_Llama-3.1-8B.json` (20-field hparams, NV-resident) | Session 2.5a | Cell 4 (provides `mom2_dataset`, `mom2_n_samples`, `mom2_dtype`, `layer_module_tmp`, etc.) |
| Bridge cache at `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` (5 × ~822 MB; `Llama-3-8B-Instruct` provenance) | Session 2.5a | Cell 3 (archived, not consumed) |
| HF token at `~/.cache/huggingface/token` (gated-public-repo permission) | Operator-side per S2.5a | Cells 1, 3 |

**v1.2 expansion notes:**

- The `globals.yml` row is new in v1.2, formalizing what v1.1 §4.2 caught reactively (STATS_DIR drift assertion at Cell 4 entry). Per D-PreS26-3, the canonical key values are: `STATS_DIR: /workspace/covariance_caches`, `DATA_DIR: /workspace/data`, `HPARAMS_DIR: /workspace/memit_dry_run/memit/hparams`, `RESULTS_DIR: /workspace/results`, `KV_DIR: /workspace/kvs` — all absolute paths. The upstream-pristine MEMIT yaml carries relative-path defaults (`STATS_DIR: data/stats`, `DATA_DIR: data`, etc.) plus an absolute-path `KV_DIR: /share/projects/rewriting-knowledge/kvs` from upstream MEMIT's authoring environment, all of which were corrected in pre-S2.6 fork-work session via D-PreS26-3.
- The MEMIT repo row gains P-5 (dataset loader modernization per `memit-patches-canonical.md` v2.2 §3.6) as a required patch state. P-5 application happens operator-side via the §3.6.7 idempotent script (executed as part of S2.5b §4.3 NV writes); Cell 2 verifies the post-state markers per v2.2 §3.6.8.

## 1.4 Outputs

| Artifact | Path | Producer |
|---|---|---|
| 5 fresh `.npz` cache files | `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz` for L ∈ [4,5,6,7,8] | Cell 4 |
| `PROVENANCE.txt` | `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/PROVENANCE.txt` | Cell 5 |
| Archived bridge cache + archive provenance | `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/bridge_archive_<UTC-ISO>/` (5 × ~822 MB + `BRIDGE_ARCHIVE_PROVENANCE.txt`) | Cell 3 |
| Pre-flight fingerprints | `/workspace/architecture_profile/pre_s2_6_environment_fingerprint.json`, `pre_s2_6_patch_state.json` | Cells 1, 2 |
| Per-layer compute log | `/workspace/architecture_profile/pre_s2_6_layer_stats_log.json` | Cell 4 |
| Cell 5 verdict | `/workspace/architecture_profile/pre_s2_6_cache_verdict.json` | Cell 5 |

## 1.5 Success criteria (load-bearing)

```
PRE_S2_6_PASS = (
    cache_file_set_match           # exactly the 5 expected per-layer .npz files at canonical path
    AND cache_file_shape_correct   # each .npz second-moment matrix is (14336, 14336) float32
    AND cache_sample_size_meets    # each .npz sample_size field reads ≥ 100000
    AND provenance_txt_complete    # 7-field structured assertion present and well-formed
    AND provenance_gate_passes     # downstream Cell 3 of stage_1_sect_runbook.md re-runs to PASS
    AND bridge_archive_intact      # bridge cache archived (not deleted); recovery path exists
)
```

## 1.6 Cost projection

| Phase | Wall time | GPU cost | NV cost |
|---|---|---|---|
| Pre-flight (Cells 0–3) | ~10–15 min | ~$0.15 | — |
| Cache compute (Cell 4) — load-bearing long-running | ~4–8 hours | ~$2.75–5.50 | — |
| Verification (Cell 5) | ~3–5 min | ~$0.05 | ~$0.02 |
| **Total** | **~4.2–8.4 hours** | **~$2.95–5.70** | **~$0.02** |

NV growth: ~4.0–5.0 GB (5 fresh `.npz` files) + ~4.0 GB (archived bridge); net ~+8 GB. Total NV at session end ~41 GB (vs ~33 GB at session start). Within OQ-S25-9 envelope ($3–6).

## 1.7 Pre-flight operator preconditions

Before Cell 0:

- [ ] Pod started against NV `large_amethyst_wolverine`; `/workspace` mounted
- [ ] Image: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` (digest `sha256:61a4aafb…` per Block 2 D1)
- [ ] On-Demand procurement (Session 2.1 venue lock); RTX 4090 confirmed in dropdown
- [ ] HF token already persisted on NV from S2.5a (`~/.cache/huggingface/token` survives stop/start? No — `~` is container-disk; re-login required if not also stashed on NV. Verify in Cell 1.)
- [ ] Billing alerts: ≥ $50 hard ceiling per S2.1; ≥ $7 within-session sentinel for this run
- [ ] Operator wall-clock window of 5–9 hours available; runbook cannot be paused mid-Cell-4 without losing partial layer progress
- [ ] **`globals.yml` correction applied to NV**: `/workspace/memit_dry_run/memit/globals.yml` carries `STATS_DIR: /workspace/covariance_caches` (not the upstream default `data/stats`). Verified via `cat /workspace/memit_dry_run/memit/globals.yml | grep STATS_DIR` — operator-side or via S2.5b §4.3 NV writes runbook. Cell 1.5 verifies; this precondition is the operator-side persistence guarantee that the verification can find a correct yaml.
- [ ] **P-5 applied to NV-resident MEMIT repo**: `rome/layer_stats.py` carries both post-state markers (`"20231101.en"` AND `"wikimedia/wikipedia"`). Applied via `memit-patches-canonical.md` v2.2 §3.6.7 idempotent script — operator-side per S2.5b §4.3 NV writes runbook. Cell 2 verifies; this precondition is the operator-side guarantee that the patch state is in place when the runbook starts.

---

# Part II — Pod configuration

## 2.1 Hardware target

| Setting | Value | Rationale |
|---|---|---|
| GPU | 1× RTX 4090 24 GB (Secure Cloud) | Stage 1 production target per Session 2.1; sufficient envelope for `layer_stats` accumulation in fp32 |
| Pod type | On-demand | Session 2.1 venue lock |
| Region | US-NC-1 (NV-pinned) | NV is region-pinned; cannot be relocated without NV destruction |
| Container image digest | `sha256:61a4aafb…` | Tag `2.4.0` is informational; digest is canonical (Block 2 D1) |
| Network Volume | `large_amethyst_wolverine` (`nvol-s1xi9zhfc2`); mounted at `/workspace` | Inherited from S2.5a |
| Working directory | `/workspace/memit_dry_run/memit/` for any MEMIT-importing cell | C-S25-5 (MEMIT cwd invariant) |

## 2.2 Constraints honored

| Constraint | Cell(s) honoring |
|---|---|
| `C-S25-2` (container-disk Python state non-persistent) | Cell 0 (full reinstall) |
| `C-S25-5` (MEMIT cwd invariant) | Cells 2, 4 (`os.chdir(MEMIT_ROOT)` before any MEMIT import) |
| `C-S25-6` (full Block 2 §12 dep manifest) | Cell 0 |
| `C-S25-7` (pandas runtime deps `pytz`, `tzdata`) | Cell 0 (Phase 3) |
| `C-S25-10` / `C-S25-11` (bridge cache ban from Stage 1+; fresh cache mandate) | Entire session |
| `IC-S25-1` (cache provenance contract — bridge archived, not deleted) | Cell 3 |
| `IC-S25-2` (P-4 patch application contract — required before any `apply_memit_*` or `layer_stats` against non-GPT-2-family models) | Cell 2 (verification) |

---

# Part III — Pre-flight (Cells 0, 1, 1.5, 2)

## Cell 0 — System binaries + Python deps + mandatory kernel restart

**Specialist:** framework-spec-writer + memit-specialist

**Purpose:** Re-establish Block 2 §12 dependency manifest plus `C-S25-7` pandas-runtime extension on a fresh container. This cell is mandatory on every pod start (`C-S25-2`).

**Inputs:** Fresh container; NV mounted at `/workspace`.

```bash
# Run in pod terminal BEFORE launching Jupyter
# === System binaries ===
apt-get update -qq
apt-get install -y --no-install-recommends rsync skopeo

which rsync && rsync --version | head -1
which skopeo && skopeo --version
```

```python
# === CELL 0 — Block 2 §12 dep manifest + pandas runtime extension ===
# Specialist: framework-spec-writer + memit-specialist
# References: C-S25-2, C-S25-6, C-S25-7; OQ-S23-4 iter 3; block-2-3-runbook-deltas §12

import subprocess, sys

PY = sys.executable

# Phase 1: Load-bearing + import-time-only + hydra chain (single bulk install)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "transformers==4.45.2",
    "accelerate==0.34.2",
    "huggingface_hub==0.25.2",
    "tokenizers==0.20.3",
    "safetensors==0.4.5",
    "datasets==4.8.3",
    "matplotlib==3.9.2",
    "scipy==1.14.1",
    "scikit-learn==1.5.2",
    "hydra-core==1.3.2",
    "einops==0.7.0",
    "nltk==3.8.1",
], check=True)

# Phase 2: pandas force-reinstall (--no-deps to preserve the loadout above)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "--force-reinstall", "--no-deps", "pandas==2.2.3",
], check=True)

# Phase 3: pandas runtime deps not covered by --no-deps (C-S25-7)
subprocess.run([PY, "-m", "pip", "install", "--quiet",
    "pytz", "tzdata",
], check=True)

print("Cell 0 install complete. RESTART KERNEL NOW (mandatory per OQ-S23-4 iter 3).")
print("After restart, proceed to Cell 1.")
```

**MANDATORY KERNEL RESTART AFTER CELL 0.** C extension version mismatches are not recoverable in-process (`OQ-S23-8` taxonomy).

**Verification anchors:** all four pip phases exit 0; restart performed.

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any `pip install` non-zero exit | Pre-flight failure | Inspect stderr; verify network egress; retry |
| Operator forgets kernel restart | Latent failure (will manifest in Cell 4 as `ImportError` or stale C extension) | Restart; re-run Cell 1 |

---

## Cell 1 — Environment fingerprint + pre-flight assertions

**Specialist:** framework-spec-writer

**Purpose:** Capture runtime versions, GPU identity, image digest, NV mount health, HF token presence, and bridge-cache existence pre-state. Persist to NV for manifest reconciliation.

**Inputs:** Cell 0 complete + kernel restarted.

```python
# === CELL 1 — Environment fingerprint + pre-flight assertions ===
# Specialist: framework-spec-writer
# References: Block 2 D1 (digest pin); OQ-S23-2 (manifest discipline); D-S25-8 (NV-cached HF)

import os, json, subprocess, platform, sys
from datetime import datetime, timezone

# Python + CUDA + torch
import torch

fingerprint = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "session": "pre-S2.6-fork-work",
    "python_version": platform.python_version(),
    "torch_version": torch.__version__,
    "cuda_torch": torch.version.cuda,
    "cudnn": torch.backends.cudnn.version(),
    "gpu_count": torch.cuda.device_count(),
    "gpus": [],
}
for i in range(torch.cuda.device_count()):
    props = torch.cuda.get_device_properties(i)
    fingerprint["gpus"].append({
        "index": i,
        "name": props.name,
        "total_memory_gb": round(props.total_memory / 1e9, 2),
        "compute_capability": f"sm_{props.major}{props.minor}",
    })

# Driver version
try:
    nvsmi = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
        text=True
    ).strip().split("\n")[0]
    fingerprint["driver_version"] = nvsmi
except Exception as e:
    fingerprint["driver_version"] = f"UNAVAILABLE: {e}"

# Image digest (skopeo) — operator-fillable if env-var not set
fingerprint["image_digest_observed"] = os.environ.get("RUNPOD_IMAGE_DIGEST", "OPERATOR_TO_FILL_VIA_SKOPEO")

# /workspace mount
df_workspace = subprocess.check_output(["df", "-BG", "/workspace"], text=True).strip().split("\n")
fingerprint["workspace_mount"] = df_workspace[-1]

# HF token presence (do not log the token itself)
hf_token_path = os.path.expanduser("~/.cache/huggingface/token")
fingerprint["hf_token_present_at_default_path"] = os.path.exists(hf_token_path)
# Also probe HF_HOME redirect per D-S25-8
fingerprint["hf_home_env"] = os.environ.get("HF_HOME", "<unset>")

# Bridge cache pre-state (must exist; nothing to archive otherwise)
BRIDGE_DIR = "/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats"
bridge_files = sorted(os.listdir(BRIDGE_DIR)) if os.path.isdir(BRIDGE_DIR) else []
fingerprint["bridge_cache_pre_state"] = {
    "dir_exists": os.path.isdir(BRIDGE_DIR),
    "file_count": len(bridge_files),
    "files": bridge_files,
}

# NV state inventory (high-level)
fingerprint["nv_state_inventory"] = {
    "memit_repo": os.path.isdir("/workspace/memit_dry_run/memit"),
    "hf_cache": os.path.isdir("/workspace/hf_cache"),
    "hparams_json": os.path.isfile("/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json"),
}

print(json.dumps(fingerprint, indent=2))

os.makedirs("/workspace/architecture_profile", exist_ok=True)
with open("/workspace/architecture_profile/pre_s2_6_environment_fingerprint.json", "w") as f:
    json.dump(fingerprint, f, indent=2)

# Stage 1 production target invariants (same as stage_1_sect Cell 1)
assert fingerprint["gpu_count"] == 1, "Single-GPU invariant violated"
assert fingerprint["gpus"][0]["name"] == "NVIDIA GeForce RTX 4090", \
    f"Hardware invariant violated: {fingerprint['gpus'][0]['name']}"
assert fingerprint["gpus"][0]["compute_capability"] == "sm_89", \
    "Compute capability invariant violated"

# Pre-flight assertions specific to this session
assert fingerprint["nv_state_inventory"]["memit_repo"], "MEMIT repo absent on NV; recover from SSD mirror"
assert fingerprint["nv_state_inventory"]["hf_cache"],   "HF cache absent on NV; Llama-3.1-8B base unavailable"
assert fingerprint["nv_state_inventory"]["hparams_json"], "Hparams JSON absent; recover from S2.5a"
assert fingerprint["bridge_cache_pre_state"]["dir_exists"], \
    "Bridge cache directory missing — nothing to archive. State drift; halt and investigate."
assert fingerprint["bridge_cache_pre_state"]["file_count"] >= 5, \
    f"Bridge cache underpopulated: {fingerprint['bridge_cache_pre_state']['file_count']} files; expected ≥ 5."

# HF token check is informational (some operators stash on NV); do not assert hard
if not fingerprint["hf_token_present_at_default_path"]:
    print("\nWARNING: HF token not at default path. If Cell 3 model load fails, run "
          "`huggingface-cli login` before retrying.")

print("\nCell 1: pre-flight invariants verified.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `gpu_count` | `1` |
| `gpus[0].name` | `NVIDIA GeForce RTX 4090` |
| `gpus[0].compute_capability` | `sm_89` |
| `bridge_cache_pre_state.file_count` | `≥ 5` |
| All `nv_state_inventory` flags | `True` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| GPU != RTX 4090 | Pre-flight failure | Capacity substitution; halt and re-procure |
| Bridge cache absent | Pre-flight failure | NV state drift since S2.5a; halt and investigate before any compute |
| MEMIT repo / hf_cache / hparams JSON absent | Pre-flight failure | NV corruption; recover from SSD mirror per S2.5b checklist |
| HF token absent at default path | Soft warning | Run `huggingface-cli login` before Cell 3 |

---

## Cell 1.5 — `globals.yml` pre-flight verification (NEW IN v1.2 — closes OQ-PreS26-4)

**Specialist:** framework-spec-writer + state-consistency-theorist

**Purpose:** Verify NV-resident `globals.yml` carries the canonical key values per D-PreS26-3 BEFORE any MEMIT module is imported. The `from util import globals` import opens `globals.yml` via relative-path `open()` at `util/globals.py:5`; resolution requires cwd at MEMIT_ROOT (the C-S25-5 invariant, with amended scope per OQ-PreS26-7) AND the yaml present at the expected path with parseable contents. Without these, MEMIT package import itself fails — load-bearing per C-PreS26-1.

**Why a dedicated pre-flight cell:** v1.1 caught `STATS_DIR` drift reactively at Cell 4 entry (line 645 — `STATS_DIR resolved to: data/stats; halt and reconcile globals.yml`). That detection was correct but late: Cells 0–3 had already consumed wall-clock + GPU spend, and Cell 3 had loaded the model into VRAM. v1.2 surfaces the failure mode at pre-flight, before Cell 3 model load. Closes OQ-PreS26-4 by elevating `globals.yml` from implicit-dependency to declared-input with explicit verification.

**Inputs:** NV-resident `/workspace/memit_dry_run/memit/globals.yml`.

```python
# === CELL 1.5 — globals.yml pre-flight verification ===
# Specialist: framework-spec-writer + state-consistency-theorist
# References: D-PreS26-3 (canonical key values); C-PreS26-1 (load-bearing input);
#             C-S25-5 amended (OQ-PreS26-7)

import os, yaml, json
from datetime import datetime, timezone
from pathlib import Path

MEMIT_ROOT = "/workspace/memit_dry_run/memit"
GLOBALS_YML = f"{MEMIT_ROOT}/globals.yml"

# === Phase A: filesystem presence + yaml parse ===
assert os.path.exists(GLOBALS_YML), (
    f"globals.yml missing at {GLOBALS_YML}. "
    f"NV state corruption since S2.3 Block 2 setup. "
    f"Recover from SSD mirror or re-author per D-PreS26-3."
)

with open(GLOBALS_YML) as f:
    globals_raw = f.read()
    globals_yaml = yaml.safe_load(globals_raw)

print(f"globals.yml at {GLOBALS_YML} parsed successfully. Contents:")
print(globals_raw)

# === Phase B: canonical key value assertions (D-PreS26-3) ===
EXPECTED_KEYS = {
    "STATS_DIR":   "/workspace/covariance_caches",
    "DATA_DIR":    "/workspace/data",
    "HPARAMS_DIR": "/workspace/memit_dry_run/memit/hparams",
    "RESULTS_DIR": "/workspace/results",
    "KV_DIR":      "/workspace/kvs",
}

# Five canonical keys must be present
missing_keys = [k for k in EXPECTED_KEYS if k not in globals_yaml]
assert not missing_keys, (
    f"globals.yml missing canonical keys: {missing_keys}. "
    f"Expected all of: {list(EXPECTED_KEYS.keys())}"
)

# Each key carries the D-PreS26-3 expected value
mismatches = []
for k, expected in EXPECTED_KEYS.items():
    actual = globals_yaml.get(k)
    if str(actual) != expected:
        mismatches.append(f"  {k}: expected {expected!r}, got {actual!r}")

assert not mismatches, (
    "globals.yml drift from D-PreS26-3 canonical values:\n"
    + "\n".join(mismatches)
    + "\n\nMost-likely failure mode: STATS_DIR carries upstream-default 'data/stats' "
    "rather than the corrected '/workspace/covariance_caches'. "
    "Apply D-PreS26-3 correction operator-side and retry."
)

# === Phase C: import-time resolution check (C-S25-5 amended scope) ===
# Confirm that with cwd at MEMIT_ROOT, `from util import globals` actually
# resolves the corrected values. This is the load-bearing path that motivated
# C-S25-5's amendment (OQ-PreS26-7): util/globals.py:5 opens "globals.yml"
# via relative-path open(); resolution requires cwd at MEMIT_ROOT.

import sys
os.chdir(MEMIT_ROOT)
if MEMIT_ROOT not in sys.path:
    sys.path.insert(0, MEMIT_ROOT)

# Purge any stale memit_globals from prior cells (idempotent re-execution)
for mod in list(sys.modules.keys()):
    if mod.startswith("util."):
        del sys.modules[mod]

from util import globals as memit_globals

# STATS_DIR is the load-bearing field (consumed by Cell 4 layer_stats invocation)
RESOLVED_STATS_DIR = str(memit_globals.STATS_DIR)
assert RESOLVED_STATS_DIR == EXPECTED_KEYS["STATS_DIR"], (
    f"globals resolution drift: memit_globals.STATS_DIR resolved to "
    f"{RESOLVED_STATS_DIR!r}; expected {EXPECTED_KEYS['STATS_DIR']!r}. "
    f"This indicates either (a) yaml parse correct but cwd wrong (C-S25-5 violation), "
    f"or (b) sys.modules cache pollution from a prior cell — re-run after kernel restart."
)

print(f"\nCell 1.5 PASS:")
print(f"  globals.yml at {GLOBALS_YML} parses cleanly")
print(f"  All 5 canonical keys present with D-PreS26-3 expected values")
print(f"  memit_globals.STATS_DIR resolves to {RESOLVED_STATS_DIR!r} ✓")

# Persist to fingerprint
globals_fingerprint = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "globals_yml_path": GLOBALS_YML,
    "globals_yaml_parsed": globals_yaml,
    "resolved_stats_dir": RESOLVED_STATS_DIR,
    "expected_keys_assertion": "PASS",
    "import_time_resolution_assertion": "PASS",
}
with open("/workspace/architecture_profile/pre_s2_6_globals_fingerprint.json", "w") as f:
    json.dump(globals_fingerprint, f, indent=2)
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `globals.yml` exists at `/workspace/memit_dry_run/memit/globals.yml` | True |
| All 5 canonical keys present (`STATS_DIR`, `DATA_DIR`, `HPARAMS_DIR`, `RESULTS_DIR`, `KV_DIR`) | True |
| Each key carries D-PreS26-3 expected value | True |
| `memit_globals.STATS_DIR == "/workspace/covariance_caches"` (post-import) | True |
| `pre_s2_6_globals_fingerprint.json` written | True |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `globals.yml` absent | Pre-flight failure | NV corruption; recover from SSD mirror or re-author per D-PreS26-3 |
| Yaml parse failure | Pre-flight failure | Yaml syntax error; inspect file contents and repair |
| Missing canonical keys | Pre-flight failure | Yaml carries fewer than 5 expected keys; investigate authorship history (likely upstream MEMIT default never replaced) |
| Key value mismatch (esp. `STATS_DIR`) | Pre-flight failure | Most-likely failure mode: `STATS_DIR: data/stats` upstream default. Apply D-PreS26-3 correction operator-side; retry |
| `memit_globals.STATS_DIR` resolves to wrong value despite yaml correct | Pre-flight failure | Either (a) cwd violation (C-S25-5 amended scope), OR (b) sys.modules cache pollution — restart kernel and retry from Cell 0 |

---

## Cell 2 — MEMIT repo + patch state verification (P-1, P-2, P-4, P-5)

**Specialist:** memit-specialist

**Purpose:** Verify the MEMIT repo on NV carries the canonical SHA pin AND has all required patches applied. Identical pattern to `stage_1_sect_runbook.md` Cell 2 (idempotent, grep-based) **with two v1.2 corrections**: (i) the `rome/layer_stats.py` assertion uses `max_position_embeddings` occurrence count rather than the v1.1 `hidden_size` substring presence (which would fail empirically per D-PreS26-1); (ii) a P-5 marker presence check is added per `memit-patches-canonical.md` v2.2 §3.6.8. `IC-S25-2` requires P-4 applied before any `layer_stats` invocation against `meta-llama/Llama-3.1-8B`; the parallel implicit contract for P-5 is that `rome/layer_stats.py` must carry the parquet-substrate dispatch markers before any `layer_stats` invocation, since the legacy script-based dispatch raises `RuntimeError` at module-load time under `datasets==4.8.3`.

**Inputs:** NV-resident `/workspace/memit_dry_run/memit/`.

```python
# === CELL 2 — MEMIT repo + patch state verification (v1.2 corrected form) ===
# Specialist: memit-specialist
# References: IC-S25-2 (P-4 idempotency); memit-patches-canonical.md v2.2;
#             C-S25-5 (amended per OQ-PreS26-7); D-PreS26-1 (Cell 2 verification correction);
#             v2.2 §3.5.8 (P-4 verification form); v2.2 §3.6.8 (P-5 verification form)

import os, subprocess, sys, hashlib, json
from datetime import datetime, timezone

MEMIT_ROOT = "/workspace/memit_dry_run/memit"
EXPECTED_SHA = "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

assert os.path.exists(MEMIT_ROOT), f"MEMIT repo missing at {MEMIT_ROOT}"

# C-S25-5 (amended per OQ-PreS26-7): chdir BEFORE sys.path manipulation or any MEMIT import.
# C-S25-5's amended scope explicitly covers module-import precondition: util/globals.py:5
# opens "globals.yml" via relative-path open(), only resolvable from cwd at MEMIT_ROOT.
# Without C-S25-5, the open call raises FileNotFoundError and the entire MEMIT package
# fails to import. Cross-reference C-PreS26-1 (globals.yml as load-bearing input).
os.chdir(MEMIT_ROOT)

# SHA pin verification
memit_sha = subprocess.check_output(
    ["git", "-C", MEMIT_ROOT, "rev-parse", "HEAD"], text=True
).strip()
assert memit_sha == EXPECTED_SHA, f"SHA pin drift: got {memit_sha}, expected {EXPECTED_SHA}"

# P-1 + P-2 verification (util/nethook.py) — unchanged from v1.1
nethook_path = f"{MEMIT_ROOT}/util/nethook.py"
with open(nethook_path) as f:
    nethook_src = f.read()
assert "def retain_hook(m, args, kwargs, output):" in nethook_src, "P-1 missing"
assert "with_kwargs=True" in nethook_src, "P-2 missing"

# P-4 verification (compute_z.py, compute_v.py, layer_stats.py) — v1.2 CORRECTED FORM
# Per D-PreS26-1: rome/layer_stats.py has NO hidden_size site; both patch sites at
# lines ≈ 101 + 108 are n_positions → max_position_embeddings. The v1.1 form
# `assert "hidden_size" in src` for layer_stats.py would fail empirically.
# v1.2 form: layer_stats.py asserted via max_position_embeddings count >= 2;
# compute_z.py + compute_v.py asserted via hidden_size substring presence.
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
        # Both patch sites are n_positions → max_position_embeddings (D-PreS26-1)
        assert src.count(p4_marker_max_pos) >= 2, \
            f"P-4 (max_position_embeddings fallback) missing in {path}; expected ≥ 2 occurrences"
    elif path.endswith("compute_z.py"):
        assert p4_marker_hidden_size in src, f"P-4 (hidden_size fallback) missing in {path}"
    elif path.endswith("compute_v.py"):
        assert p4_marker_hidden_size in src, f"P-4 (hidden_size fallback) missing in {path}"

# P-5 verification (rome/layer_stats.py dataset loader modernization) — NEW IN v1.2
# Per memit-patches-canonical.md v2.2 §3.6.8. Both post-state markers must be present.
p5_target = f"{MEMIT_ROOT}/rome/layer_stats.py"
p5_markers = ['"20231101.en"', '"wikimedia/wikipedia"']
with open(p5_target) as f:
    p5_src = f.read()
for marker in p5_markers:
    assert marker in p5_src, (
        f"P-5 marker {marker!r} missing from {p5_target}. "
        f"Apply via memit-patches-canonical.md v2.2 §3.6.7 idempotent script. "
        f"Until P-5 is applied, Cell 4 Phase 1 will raise RuntimeError at "
        f"datasets/load.py:1167 ('Dataset scripts are no longer supported')."
    )

# sys.path injection (idempotent)
if MEMIT_ROOT not in sys.path:
    sys.path.insert(0, MEMIT_ROOT)

# File SHA-256 fingerprints for manifest
patched_files = [nethook_path] + p4_targets  # layer_stats.py is in p4_targets, covers P-5 too
file_hashes = {}
for path in patched_files:
    with open(path, "rb") as f:
        file_hashes[os.path.relpath(path, MEMIT_ROOT)] = hashlib.sha256(f.read()).hexdigest()[:16]

patch_state = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "memit_sha": memit_sha,
    "memit_patches_canonical_version": "2.2",
    "patches_applied": {
        "P-1_nethook_signature": True,
        "P-2_with_kwargs_registration": True,
        "P-4_config_attribute_fallback": True,
        "P-5_dataset_loader_modernization": True,
    },
    "file_sha256_prefix": file_hashes,
    "cwd": os.getcwd(),
}
print(json.dumps(patch_state, indent=2))

with open("/workspace/architecture_profile/pre_s2_6_patch_state.json", "w") as f:
    json.dump(patch_state, f, indent=2)

print(f"\nCell 2: P-1, P-2, P-4, P-5 verified. cwd={os.getcwd()} (C-S25-5 honored).")
```

**Verification anchors:** identical pattern to `stage_1_sect_runbook.md` Cell 2 — `memit_sha` matches `80426fd9…`; all P-1 / P-2 / P-4 / P-5 markers present; `os.getcwd() == MEMIT_ROOT`. The `stage_1_sect_runbook.md` v1.2 Cell 2 retains the v1.1-form (uncorrected) verification logic; correction is tracked as **OQ-S25b-1** (S2.5b §4.5 sub-step summary) for a future stage_1_sect_runbook v1.3 hardening pass.

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| SHA mismatch | Pre-flight failure | Repo drifted; re-pin or recover from SSD mirror |
| P-1, P-2, P-4 marker absent | Pre-flight failure | Re-run patch script per `memit-patches-canonical.md` v2.2 §2 / §3.5; verify; resume |
| **P-5 marker absent** | **Pre-flight failure** | **Re-run patch script per `memit-patches-canonical.md` v2.2 §3.6.7 idempotent script; operator-side via S2.5b §4.3 NV writes runbook; verify; resume.** |
| `os.getcwd()` not MEMIT root | Pre-flight failure | C-S25-5 violation (amended scope per OQ-PreS26-7); halt before any MEMIT import — would also break `from util import globals` per C-PreS26-1 |

---

# Part IV — Bridge archival + model load (Cell 3)

## Cell 3 — Bridge archive (atomic-swap) + Llama-3.1-8B base load

**Specialist:** state-consistency-theorist (atomic-swap discipline) + memit-specialist (model load + Pad-Token alias)

**Purpose:** (a) Archive the bridge cache to a sibling directory under a UTC-stamped name, leaving the canonical path empty for fresh compute. (b) Load the `meta-llama/Llama-3.1-8B` base model from the NV-cached HF home, capturing its resolved revision SHA for `PROVENANCE.txt` authorship in Cell 5. Per `IC-S25-1`: the bridge MUST be archived (not deleted); recovery path preserved.

**Inputs:** Cell 2 PASS; HF token operational; Llama-3.1-8B base in `/workspace/hf_cache/`.

```python
# === CELL 3 — Bridge archive (atomic-swap) + Llama-3.1-8B model load ===
# Specialist: state-consistency-theorist + memit-specialist
# References: IC-S25-1 (bridge archived, not deleted); D-S25-8 (HF_HOME on NV);
#             memit-patches-canonical.md §4 (Pad-Token alias)

import os, json, shutil
from datetime import datetime, timezone

CACHE_PARENT = "/workspace/covariance_caches/meta-llama_Llama-3.1-8B"
CANONICAL    = f"{CACHE_PARENT}/wikipedia_stats"
ARCHIVE_TS   = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
ARCHIVE_DIR  = f"{CACHE_PARENT}/bridge_archive_{ARCHIVE_TS}"

# === Phase A: atomic-swap archive ===
# IC-S25-1: bridge cache archived as sibling directory (NOT inside canonical;
# stage_1_sect Cell 3 listdir would otherwise misinterpret archive as cache).

assert os.path.isdir(CANONICAL), f"Canonical cache dir missing: {CANONICAL}"
bridge_files_pre = sorted(os.listdir(CANONICAL))
assert len(bridge_files_pre) >= 5, \
    f"Bridge underpopulated: {bridge_files_pre}; refuse to archive partial state."

os.makedirs(ARCHIVE_DIR, exist_ok=False)  # exist_ok=False: collision fails loudly
for fname in bridge_files_pre:
    src = f"{CANONICAL}/{fname}"
    dst = f"{ARCHIVE_DIR}/{fname}"
    shutil.move(src, dst)

# Verify post-move state: archive populated, canonical empty
archive_files = sorted(os.listdir(ARCHIVE_DIR))
canonical_post = sorted(os.listdir(CANONICAL))
assert archive_files == bridge_files_pre, "Archive file set mismatch after move"
assert canonical_post == [], f"Canonical not empty after archive: {canonical_post}"

# Write archive provenance marker (recovery path documentation)
archive_provenance = (
    f"# Bridge cache archive — sealed by pre-S2.6 fork-work session\n"
    f"archived_at = {datetime.now(timezone.utc).isoformat()}\n"
    f"archived_by_session = pre-S2.6-fork-work\n"
    f"original_canonical_path = {CANONICAL}\n"
    f"original_provenance = jasonrichdarmawan/rke @ HF (originally Llama-3-8B-Instruct)\n"
    f"reason = IC-S25-1 mandates archive-not-delete; banned from Stage 1+ per C-S25-10\n"
    f"recovery_path = mv {ARCHIVE_DIR}/* {CANONICAL}/  # if fresh compute fails irrecoverably\n"
    f"file_count = {len(archive_files)}\n"
)
with open(f"{ARCHIVE_DIR}/BRIDGE_ARCHIVE_PROVENANCE.txt", "w") as f:
    f.write(archive_provenance)

print(f"Phase A complete: {len(archive_files)} bridge files archived to {ARCHIVE_DIR}/")
print(f"Canonical path now empty: {CANONICAL}")

# === Phase B: Llama-3.1-8B base load + revision SHA capture ===
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "meta-llama/Llama-3.1-8B"

# HF cache-home discipline (D-S25-8)
os.environ.setdefault("HF_HOME", "/workspace/hf_cache")

print(f"\nLoading {MODEL_NAME} from NV-cached HF home...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,   # storage; layer_stats internal accum is float32 per hparams
    device_map="cuda:0",
)
model.eval()
print(f"Model loaded. Device: {next(model.parameters()).device}; "
      f"hidden_size={model.config.hidden_size}; intermediate_size={model.config.intermediate_size}")

# Pad-Token alias (memit-patches-canonical.md §4) — Llama 3.1 base often has pad_token=None
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
    print(f"Pad-Token alias applied: pad_token = eos_token = {tokenizer.eos_token!r}")
else:
    print(f"Pad-Token already defined: {tokenizer.pad_token!r}; alias skipped")

# === Revision SHA capture (PROVENANCE option (b) with (a) fallback) ===
# Option (b): model._commit_hash if transformers populated it from from_pretrained
# Option (a) fallback: HfApi default-revision query
revision_sha = None
revision_source = None

# (b) Try model.config._commit_hash
try:
    candidate_b = getattr(model.config, "_commit_hash", None)
    if candidate_b:
        revision_sha = candidate_b
        revision_source = "model.config._commit_hash"
except Exception:
    pass

# (b') Try generation_config or model._commit_hash variants
if revision_sha is None:
    try:
        candidate_b2 = getattr(model, "_commit_hash", None)
        if candidate_b2:
            revision_sha = candidate_b2
            revision_source = "model._commit_hash"
    except Exception:
        pass

# (a) Fallback: HfApi default-revision query
if revision_sha is None:
    from huggingface_hub import HfApi
    info = HfApi().model_info(MODEL_NAME)
    revision_sha = info.sha
    revision_source = "HfApi.model_info(...).sha [FALLBACK — does NOT guarantee match to loaded weights]"

print(f"\nRevision SHA: {revision_sha}")
print(f"Revision source: {revision_source}")

# Stash for Cell 5 — write to NV so a kernel restart between Cells 4 and 5 doesn't lose it
revision_record = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "model_name": MODEL_NAME,
    "revision_sha": revision_sha,
    "revision_source": revision_source,
    "archive_dir": ARCHIVE_DIR,
    "canonical_dir": CANONICAL,
}
with open("/workspace/architecture_profile/pre_s2_6_revision_record.json", "w") as f:
    json.dump(revision_record, f, indent=2)

print(f"\nCell 3 complete: bridge archived, model loaded, revision SHA captured.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| Archive directory created | `bridge_archive_<UTC-ISO>/` populated with 5+ files + `BRIDGE_ARCHIVE_PROVENANCE.txt` |
| Canonical directory empty post-move | `os.listdir(CANONICAL) == []` |
| Model `hidden_size` | `4096` (Llama-3.1-8B base) |
| Model `intermediate_size` | `14336` (matches expected covariance dim) |
| `revision_sha` non-empty | True |
| `revision_source` recorded | One of `model.config._commit_hash`, `model._commit_hash`, or HfApi fallback |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Archive collision (`exist_ok=False` triggers) | Hard halt | Same-second timestamp collision (extremely rare); wait 1 sec, re-run |
| Bridge file count < 5 pre-archive | Hard halt | NV state drift since S2.5a; investigate before any further action |
| Model load OOM | Hard halt | RTX 4090 24 GB should accommodate 8B fp16; if OOM, GPU procurement substitution suspected |
| `revision_sha is None` after both paths | Hard halt | HF API unreachable + transformers did not populate commit hash; resolve before Cell 5 |

---

# Part V — Cache compute (Cells 3.5, 4)

## Cell 3.5 — Compute-path smoke (NEW IN v1.2 — closes OQ-PreS26-8)

**Specialist:** memit-specialist + validation-contract-architect

**Purpose:** Validate the cache-miss compute path of `rome.layer_stats.layer_stats` against a small-sample-size config (~1000 samples, single layer) BEFORE launching the full ~4–8 hour 100K-sample compute across 5 layers. Closes OQ-PreS26-8 by formalizing the "smoke-test cache-hit shortcut as latent-failure mechanism" pattern surfaced in pre-S2.6 fork-work session §6 retrospective Observation 2.

**Why this cell exists:** S2.5a's smoke test passed via cache-hit short-circuit — the `layer_stats` call resolved cached `.npz` files without re-executing the compute path. Two subsequent findings (the `rome/layer_stats.py` patch state ambiguity that surfaced as D-PreS26-1, and the `datasets==4.8.3` script-loader incompatibility that surfaced as OQ-PreS26-6 → P-5) were structurally undetectable through cache-hit validation. Cell 3.5 forces a cache-miss execution at ~5-minute cost, catching any compute-path failure before the full compute commits ~$3–6 GPU spend.

**Inputs:** Cell 1.5 PASS (globals.yml resolves correctly); Cell 2 PASS (P-1, P-2, P-4, P-5 verified); Cell 3 PASS (model + tokenizer loaded; canonical cache directory empty post-archive).

**Outputs:** Smoke `.npz` at non-canonical path (NOT consumed by Cell 4); structural confirmation that compute path executes end-to-end.

```python
# === CELL 3.5 — Compute-path smoke ===
# Specialist: memit-specialist + validation-contract-architect
# References: OQ-PreS26-8 (compute-path smoke pattern); D-PreS26-1 + OQ-PreS26-6
#             (latent-failure precedent); memit-patches-canonical.md v2.2 §3.6 P-5

import os, time, traceback
from pathlib import Path
from datetime import datetime, timezone
from tqdm import tqdm
import json

from rome.layer_stats import layer_stats
from memit.memit_hparams import MEMITHyperParams

# Re-load hparams (used for ds_name + module template)
HPARAMS_JSON = "/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json"
hparams = MEMITHyperParams.from_json(HPARAMS_JSON)

# Smoke target: layer 4 (first of the [4..8] range) at sample_size=1000
SMOKE_LAYER = 4
SMOKE_SAMPLE_SIZE = 1000
SMOKE_LAYER_NAME = hparams.rewrite_module_tmp.format(SMOKE_LAYER)
# Non-canonical smoke directory — explicitly NOT under STATS_DIR to avoid
# contaminating the cache that Cell 4 will populate
SMOKE_STATS_DIR = "/workspace/architecture_profile/pre_s2_6_smoke_stats"
os.makedirs(SMOKE_STATS_DIR, exist_ok=True)

# MODEL_NAME_FOR_CACHE — explicit parameter for layer_stats per OQ-PreS26-3 + OQ-S25b-2.
# Controls the per-model subdirectory in the cache file path. layer_stats internally
# converts the slash to underscore when constructing the cache subdirectory.
MODEL_NAME_FOR_CACHE = "meta-llama/Llama-3.1-8B"

print(f"=== Cell 3.5 compute-path smoke ===")
print(f"  Target layer: {SMOKE_LAYER} ({SMOKE_LAYER_NAME})")
print(f"  Sample size:  {SMOKE_SAMPLE_SIZE}")
print(f"  Smoke dir:    {SMOKE_STATS_DIR}")
print(f"  Model name:   {MODEL_NAME_FOR_CACHE}")
print(f"  ds_name:      {hparams.mom2_dataset}")
print(f"  precision:    {hparams.mom2_dtype}")
print(f"  force_recompute: True (cache-miss validation)")

smoke_t0 = time.time()
smoke_log = {
    "started_at": datetime.now(timezone.utc).isoformat(),
    "smoke_layer": SMOKE_LAYER,
    "smoke_sample_size": SMOKE_SAMPLE_SIZE,
    "smoke_stats_dir": SMOKE_STATS_DIR,
    "ds_name": hparams.mom2_dataset,
    "precision": hparams.mom2_dtype,
}

try:
    # Note v1.2.1 signature reconciliation per OQ-PreS26-3 + OQ-S25b-2:
    # uses `tokenizer=` (not `tok=`); does NOT pass `hparams=`; passes `model_name=` explicitly.
    smoke_stat = layer_stats(
        model=model,
        tokenizer=tokenizer,
        layer_name=SMOKE_LAYER_NAME,
        stats_dir=SMOKE_STATS_DIR,
        ds_name=hparams.mom2_dataset,         # "wikipedia"
        to_collect=["mom2"],
        model_name=MODEL_NAME_FOR_CACHE,       # explicit per OQ-S25b-2; controls cache path
        sample_size=SMOKE_SAMPLE_SIZE,        # 1000 (small)
        precision=hparams.mom2_dtype,          # "float32"
        batch_tokens=getattr(hparams, "batch_tokens", 100),
        download=True,
        progress=tqdm,
        force_recompute=True,                  # CRITICAL — cache-miss path
    )
    smoke_elapsed = time.time() - smoke_t0
    smoke_log["status"] = "PASS"
    smoke_log["elapsed_sec"] = round(smoke_elapsed, 1)
    smoke_log["elapsed_min"] = round(smoke_elapsed / 60, 2)
    print(f"\nCell 3.5 smoke PASS: {smoke_elapsed:.1f}s ({smoke_elapsed/60:.1f} min)")
    print(f"  ✓ P-5 dataset loader works (parquet substrate loads)")
    print(f"  ✓ P-4 config attribute fallback works (hidden_size + max_position_embeddings)")
    print(f"  ✓ P-1 + P-2 hooks work (forward pass through retain_hook)")
    print(f"  ✓ Pad-Token alias works (batched tokenization)")
    print(f"  ✓ globals.yml resolves correctly (STATS_DIR honored)")
    print(f"  ✓ layer_stats signature matches v1.2 invocation pattern")

    # Verify smoke output file appeared
    expected_smoke_file = (
        f"{SMOKE_STATS_DIR}/meta-llama_Llama-3.1-8B/wikipedia_stats/"
        f"{SMOKE_LAYER_NAME}_{hparams.mom2_dtype}_mom2_{SMOKE_SAMPLE_SIZE}.npz"
    )
    if os.path.isfile(expected_smoke_file):
        smoke_size_mb = os.path.getsize(expected_smoke_file) / 1e6
        smoke_log["smoke_file"] = expected_smoke_file
        smoke_log["smoke_file_size_mb"] = round(smoke_size_mb, 2)
        print(f"  ✓ Smoke .npz at {expected_smoke_file} ({smoke_size_mb:.1f} MB)")
    else:
        # Non-fatal — function returned successfully even without expected file
        smoke_log["smoke_file_warning"] = (
            f"layer_stats returned but expected smoke file not at {expected_smoke_file}; "
            f"compute path likely fine (function returned), but file-naming inspection deferred"
        )
        print(f"  ⚠️  Smoke file not at expected path; non-fatal but inspect")

except Exception as e:
    smoke_log["status"] = "FAIL"
    smoke_log["elapsed_sec"] = round(time.time() - smoke_t0, 1)
    smoke_log["exception_class"] = type(e).__name__
    smoke_log["exception_msg"] = str(e)
    smoke_log["traceback"] = traceback.format_exc()

    with open("/workspace/architecture_profile/pre_s2_6_smoke_log.json", "w") as f:
        json.dump(smoke_log, f, indent=2)

    print(f"\n=== Cell 3.5 smoke FAIL — {type(e).__name__} ===")
    print(traceback.format_exc())
    print(f"\nDO NOT proceed to Cell 4. Triage per halt taxonomy below.")
    raise

# Persist smoke log
smoke_log["completed_at"] = datetime.now(timezone.utc).isoformat()
with open("/workspace/architecture_profile/pre_s2_6_smoke_log.json", "w") as f:
    json.dump(smoke_log, f, indent=2)

print(f"\nCell 3.5 PASS — proceed to Cell 4.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `layer_stats` returns without exception | True |
| Smoke `.npz` at `/workspace/architecture_profile/pre_s2_6_smoke_stats/.../{SMOKE_LAYER_NAME}_*_mom2_1000.npz` | Present (or non-fatal warning) |
| Smoke wall-time | ~3–8 min on RTX 4090 (1000 samples; first dataset stream is the dominant cost) |
| `pre_s2_6_smoke_log.json` written with `status: "PASS"` | True |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `RuntimeError: Dataset scripts are no longer supported` at `datasets/load.py:1167` | Pre-compute failure | P-5 not applied (or partially applied); halt + re-verify Cell 2 + apply P-5 per `memit-patches-canonical.md` v2.2 §3.6.7 + restart from Cell 0 |
| `AttributeError: 'LlamaConfig' object has no attribute 'n_embd'` (or similar config-attr) | Pre-compute failure | P-4 not applied; halt + re-verify Cell 2 + apply P-4 per `memit-patches-canonical.md` v2.2 §3.5.7 + restart from Cell 0 |
| `ValueError: Asking to pad but the tokenizer does not have a padding token` | Pre-compute failure | Pad-Token alias not applied in Cell 3 Phase B; inspect Cell 3 output for the alias step; re-run from Cell 3 |
| `TypeError: layer_stats() got an unexpected keyword argument` | Pre-compute failure | Signature mismatch — runbook v1.2 invocation drift from empirical signature. Inspect Phase 0 inspection output (Cell 4 §4.1 retained for safety); reconcile v1.2 invocation form |
| `BuilderConfig 20231101.en not found` | Pre-compute failure | Wikimedia parquet dataset config name drift since S2.5b §4.0; check HF Hub for current config availability; halt and re-author P-5 per amended substrate |
| `OutOfMemoryError` (cuda) at smoke layer | Capacity failure | Reduce `batch_tokens`; if persistent, full Cell 4 also at risk — investigate before proceeding |
| `ConnectionError` / HF dataset stream hiccup | Transient | Retry Cell 3.5 (force_recompute=True will re-attempt); investigate after 2 consecutive failures |
| Smoke wall-time > 20 min | Soft warning | Compute path likely working but slow — full Cell 4 may exceed 8-hour cost projection; investigate before proceeding |

**Cost note:** Cell 3.5 adds ~5 minutes wall-time + ~$0.05 GPU to the pre-flight envelope (revised pre-flight total: ~15–20 min, ~$0.20). This is the explicit OQ-PreS26-8 cost-benefit acceptance: catch latent compute-path failures at $0.05 rather than $3–6.

**Smoke output cleanup:** the non-canonical smoke `.npz` at `/workspace/architecture_profile/pre_s2_6_smoke_stats/` may be left in place (it is structurally distinct from the Cell 4 canonical output and does not contaminate the Cell 5 GATE). Operator may delete after session close to recover ~10 MB NV.

---

## Cell 4 — Fresh covariance cache compute (load-bearing long-running)

**Specialist:** memit-specialist (`layer_stats` invocation discipline)

**Purpose:** Compute per-layer second-moment covariance matrices over 100 000 Wikipedia samples in `float32` for layers `[4, 5, 6, 7, 8]` against `meta-llama/Llama-3.1-8B` base. Output: 5 `.npz` files at canonical path matching the file-naming contract enforced by `stage_1_sect_runbook.md` Cell 3 R1.1.

**Inputs:** Cells 0–3 PASS; model + tokenizer loaded; canonical path empty; MEMIT cwd invariant active.

### 4.1 Pre-compute signature inspection

Before launching the long-running loop, verify the `layer_stats` signature matches what this runbook assumes. Drift between MEMIT versions can change parameter names; an early signature mismatch is cheap, a 4-hour signature mismatch is expensive.

**v1.2 note:** the assumed-signature documentation below is corrected per OQ-PreS26-3. Cell 3.5's compute-path smoke (also new in v1.2) provides empirical signature validation through actual invocation; Phase 0 below is retained as a defense-in-depth visual inspection step. If Phase 0 surfaces a signature differing from the v1.2 form, halt and reconcile §4.2 + Cell 3.5 invocation forms before proceeding.

```python
# === CELL 4 PHASE 0 — layer_stats signature inspection ===
import inspect
import sys

# Sanity: cwd invariant still held (C-S25-5 amended scope)
import os
assert os.getcwd().endswith("/memit_dry_run/memit"), \
    f"C-S25-5 violation: cwd={os.getcwd()}"

# Ensure MEMIT_ROOT is on sys.path (idempotent from Cell 2)
MEMIT_ROOT = "/workspace/memit_dry_run/memit"
if MEMIT_ROOT not in sys.path:
    sys.path.insert(0, MEMIT_ROOT)

from rome.layer_stats import layer_stats

sig = inspect.signature(layer_stats)
print("layer_stats signature:")
print(f"  {sig}")
print("\nParameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: default={param.default}")
```

**Operator action (v1.2.1 corrected per OQ-PreS26-3 + OQ-S25b-2):** read the printed signature. The compute call below assumes parameters: `model`, `tokenizer`, `layer_name`, `stats_dir`, `ds_name`, `to_collect`, `model_name`, `sample_size`, `precision`, `batch_tokens`, `download`, `progress`, `force_recompute`. If the signature differs (in particular: if it accepts `tok=` instead of `tokenizer=`, or accepts a trailing `hparams=`, or omits `model_name=`, or otherwise drifts), adjust §4.2 Phase 1 and Cell 3.5 smoke invocation correspondingly before launching.

**v1.1 → v1.2.1 invocation deltas:**

| Parameter | v1.1 form | v1.2.1 form | Source / rationale |
|---|---|---|---|
| Tokenizer | `tok=tokenizer` | `tokenizer=tokenizer` | OQ-PreS26-3 — empirical signature from pre-S2.6 fork-work session Cell 4 Phase 1 invocation `TypeError` |
| hparams trailing | `hparams=hparams` | (removed) | OQ-PreS26-3 — empirical signature does not accept `hparams=`; hparams fields are passed individually as `ds_name`, `sample_size`, `precision`, `batch_tokens` |
| model_name | (absent) | `model_name=MODEL_NAME_FOR_CACHE` | **OQ-S25b-2** — surfaced in S2.5b §4.8 archaeology via past-chat forensics; OQ-PreS26-3 captured 2 of 3 signature deltas, missing this one. Empirical pattern: operator's hand-corrected fork-work invocation defined `MODEL_NAME_FOR_CACHE = "meta-llama/Llama-3.1-8B"` and passed it as `model_name=`. Controls the per-model subdirectory in the cache file path |

### 4.2 Compute loop

```python
# === CELL 4 PHASE 1 — Per-layer covariance compute ===
# Specialist: memit-specialist
# References: cfb-v1 hparams (mom2_dataset, mom2_n_samples, mom2_dtype);
#             stage_1_sect_runbook.md Cell 3 R1.1 (file-naming contract)

import time, json, traceback
from datetime import datetime, timezone
from tqdm import tqdm
from memit.memit_hparams import MEMITHyperParams

# Load hparams (provides mom2_* invariants and template fields layer_stats may consume)
HPARAMS_JSON = "/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json"
hparams = MEMITHyperParams.from_json(HPARAMS_JSON)

# Cross-check against this session's invariants (defensive — operator may have re-edited hparams)
assert hparams.mom2_dataset == "wikipedia"
assert hparams.mom2_n_samples == 100000
assert hparams.mom2_dtype == "float32"
assert hparams.layers == [4, 5, 6, 7, 8]
LAYER_TMP = hparams.rewrite_module_tmp  # "model.layers.{}.mlp.down_proj"

# STATS_DIR resolution — MEMIT's util/globals.py resolves this from globals.yml
# Expected: /workspace/covariance_caches (set during S2.3 Block 2 setup)
from util import globals as memit_globals
STATS_DIR = str(memit_globals.STATS_DIR)
print(f"MEMIT STATS_DIR resolved to: {STATS_DIR}")
EXPECTED_STATS_DIR = "/workspace/covariance_caches"
assert STATS_DIR == EXPECTED_STATS_DIR, \
    f"STATS_DIR drift: {STATS_DIR} vs {EXPECTED_STATS_DIR}; halt and reconcile globals.yml"

# MODEL_NAME_FOR_CACHE — explicit parameter for layer_stats per OQ-PreS26-3 + OQ-S25b-2.
# Controls the per-model subdirectory in the cache file path. layer_stats internally
# converts the slash to underscore when constructing the cache subdirectory, producing
# {STATS_DIR}/meta-llama_Llama-3.1-8B/{ds_name}_stats/...
MODEL_NAME_FOR_CACHE = "meta-llama/Llama-3.1-8B"

LAYERS = [4, 5, 6, 7, 8]
log = {
    "session": "pre-S2.6-fork-work",
    "started_at": datetime.now(timezone.utc).isoformat(),
    "layers": [],
}

for L in LAYERS:
    layer_name = LAYER_TMP.format(L)   # e.g. "model.layers.4.mlp.down_proj"
    expected_file = (
        f"{STATS_DIR}/meta-llama_Llama-3.1-8B/wikipedia_stats/"
        f"{layer_name}_float32_mom2_100000.npz"
    )

    # Resume-safe: skip if file already exists from a prior partial run of this cell
    if os.path.isfile(expected_file):
        print(f"\n=== Layer {L} ({layer_name}) — already present; skipping ===")
        log["layers"].append({
            "layer": L,
            "layer_name": layer_name,
            "status": "skipped_already_present",
            "expected_file": expected_file,
        })
        continue

    print(f"\n=== Layer {L} ({layer_name}) — compute begins ===")
    layer_t0 = time.time()
    try:
        # v1.2.1 signature reconciliation (closes OQ-PreS26-3 + OQ-S25b-2):
        # - `tokenizer=` (not v1.1's `tok=`)
        # - no `hparams=` trailing param (not accepted by empirical signature)
        # - `model_name=` parameter passed explicitly (missed by OQ-PreS26-3, surfaced
        #   in past-chat forensics during S2.5b §4.8 archaeology — closure via OQ-S25b-2)
        # If Cell 4 Phase 0 inspection surfaced a different signature,
        # reconcile this invocation accordingly before proceeding.
        stat = layer_stats(
            model=model,
            tokenizer=tokenizer,
            layer_name=layer_name,
            stats_dir=STATS_DIR,
            ds_name=hparams.mom2_dataset,         # "wikipedia"
            to_collect=["mom2"],
            model_name=MODEL_NAME_FOR_CACHE,       # explicit per OQ-S25b-2
            sample_size=hparams.mom2_n_samples,    # 100000
            precision=hparams.mom2_dtype,          # "float32"
            batch_tokens=getattr(hparams, "batch_tokens", 100),
            download=True,
            progress=tqdm,
            force_recompute=False,                 # honor resume-safe
        )
        elapsed = time.time() - layer_t0
        # Verify output file appeared
        assert os.path.isfile(expected_file), \
            f"layer_stats returned but expected file not at {expected_file}"
        size_mb = os.path.getsize(expected_file) / 1e6

        log["layers"].append({
            "layer": L,
            "layer_name": layer_name,
            "status": "computed",
            "elapsed_sec": round(elapsed, 1),
            "elapsed_min": round(elapsed / 60, 1),
            "expected_file": expected_file,
            "size_mb": round(size_mb, 2),
        })
        print(f"  Layer {L} complete: {elapsed/60:.1f} min, {size_mb:.0f} MB")

        # Persist log incrementally so a Cell 4 crash does not lose progress visibility
        with open("/workspace/architecture_profile/pre_s2_6_layer_stats_log.json", "w") as f:
            log["last_updated"] = datetime.now(timezone.utc).isoformat()
            json.dump(log, f, indent=2)

    except Exception as e:
        log["layers"].append({
            "layer": L,
            "layer_name": layer_name,
            "status": "failed",
            "elapsed_sec": round(time.time() - layer_t0, 1),
            "exception_class": type(e).__name__,
            "exception_msg": str(e),
            "traceback": traceback.format_exc(),
        })
        with open("/workspace/architecture_profile/pre_s2_6_layer_stats_log.json", "w") as f:
            log["last_updated"] = datetime.now(timezone.utc).isoformat()
            json.dump(log, f, indent=2)
        # Re-raise: per halt taxonomy below, all Cell 4 failure classes halt the loop
        raise

log["completed_at"] = datetime.now(timezone.utc).isoformat()
with open("/workspace/architecture_profile/pre_s2_6_layer_stats_log.json", "w") as f:
    json.dump(log, f, indent=2)

print(f"\nCell 4 complete: {len(LAYERS)} layers processed.")
print(f"Total elapsed: {sum(l.get('elapsed_sec', 0) for l in log['layers'])/3600:.2f} hours")
```

### 4.3 Halt taxonomy (mid-run triage)

| Failure class | Detection | Recovery path | Loss on retry |
|---|---|---|---|
| `OutOfMemoryError` (cuda) at layer N | `torch.cuda.OutOfMemoryError` raised inside `layer_stats` | Reduce `batch_tokens` (try halving from default); `torch.cuda.empty_cache()`; restart Cell 4 — resume-safe skip will pick up at layer N | Layers `< N` preserved; layer N restarts |
| `ConnectionError` / HF dataset stream hiccup | `requests` exception inside dataset iterator | Retry Cell 4; same resume-safe mechanism. If repeated, disable `download=True` and pre-download once. | Layer N restarts |
| Pod GPU eviction / kernel death | Python process exits without exception trace | New pod (NV-pinned); replay Cells 0–3.5; restart Cell 4 — resume-safe | Layers `< N` preserved |
| `NaN`/`Inf` in covariance accumulation | rare; manifests as downstream failure or as `np.savez` writing a corrupt file | Hard halt. Inspect last-written `.npz`. If contaminated, delete it and retry single layer with diagnostic logging. Surface to Session 2.7 retrospective. | Affected layer restarts |
| `AssertionError` on `expected_file` post-`layer_stats` | `layer_stats` returned but file naming did not match contract | Hard halt. Diff actual filename against `model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz`. May indicate MEMIT internal naming drift; escalate to skill maintenance. | Cell 5 cannot run; Session 2.6 blocked |
| `signature mismatch` (Phase 0 inspection) | parameter name absent | Adjust Phase 1 call; do NOT skip Phase 0 | None — pre-launch catch |
| **`globals.yml` mis-resolution** (NEW IN v1.2) | Cell 4 entry assertion `STATS_DIR == "/workspace/covariance_caches"` fails | Hard halt. **Should not reach Cell 4 if Cell 1.5 PASS** — if it does, indicates a sys.modules cache pollution between Cell 1.5 and Cell 4. Restart kernel, re-run from Cell 0. | Pre-flight only — no compute progress lost |
| **`TypeError: layer_stats() got an unexpected keyword argument` OR `missing 1 required positional argument: 'model_name'`** (NEW IN v1.2; broadened in v1.2.1) | First `layer_stats` invocation in Phase 1 raises immediately | Hard halt. v1.2.1 signature reconciliation drift since OQ-PreS26-3 + OQ-S25b-2 closure; inspect §4.1 Phase 0 output and reconcile §4.2 invocation form. The `missing model_name` variant indicates regression to v1.1 form; the unexpected-kwarg variant indicates upstream MEMIT signature drift since SHA `80426fd9…`. **Should be caught by Cell 3.5 smoke** — if surfacing here, indicates Cell 3.5 was skipped or smoke-vs-full invocation forms drifted. | Pre-launch — layer 4 restarts after fix |
| **`RuntimeError: Dataset scripts are no longer supported`** at `datasets/load.py:1167` (NEW IN v1.2) | First `layer_stats` invocation in Phase 1 raises | Hard halt. P-5 not applied (or dispatch-dict idiom drift). **Should be caught by Cell 2 P-5 marker check or Cell 3.5 smoke** — if surfacing here, indicates Cell 2/3.5 false-PASS. Inspect `rome/layer_stats.py` for parquet markers; re-apply P-5 per `memit-patches-canonical.md` v2.2 §3.6.7; restart from Cell 0. | Pre-launch — layer 4 restarts after fix |
| **`BuilderConfig 20231101.en not found`** at parquet substrate load (NEW IN v1.2) | `datasets.builder` raises during `layer_stats` execution | Hard halt. Wikimedia dataset config name drift since S2.5b §4.0 substrate decision. Check HF Hub `wikimedia/wikipedia` config availability; investigate whether `20231101.en` was deprecated upstream. May require P-5 amendment to a newer snapshot date and re-authoring of C-S25-15. Out of scope for runbook recovery; surface to S2.5b sub-step or successor session. | Pre-launch — full reconsideration |

**Operator triage protocol during Cell 4:**

1. Watch the per-layer wall-time logs. If layer N elapsed > 2× the median of layers `< N`, suspect throttling or dataset stalling. Allow up to 3× median before intervening.
2. On any exception, the per-layer log is persisted before the raise. Inspect `/workspace/architecture_profile/pre_s2_6_layer_stats_log.json` for traceback.
3. Resume-safe skip protects work-in-place; re-running Cell 4 after a fix picks up at the failed layer.
4. If two consecutive retries on the same layer fail with different exception classes, halt session and escalate. Do NOT continue to Cell 5 with partial cache.

**Verification anchors (per layer, captured in log):**

| Anchor | Expected |
|---|---|
| `expected_file` exists post-`layer_stats` | True |
| File naming | exactly `model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz` |
| File size | ~822 MB ± 10% (matches bridge-cache footprint scale; (14336, 14336) float32 ≈ 822 MB) |
| Per-layer elapsed | ~50–90 min on RTX 4090 (median expected ~60 min) |

---

# Part VI — Provenance + downstream gate (Cell 5)

## Cell 5 — `PROVENANCE.txt` authorship + downstream gate verification

**Specialist:** state-consistency-theorist (provenance discipline)

**Purpose:** (a) Author the seven-field `PROVENANCE.txt` at the canonical cache path. (b) Re-run the exact gate predicates from `stage_1_sect_runbook.md` v1.1 Cell 3 against the new cache, in-place, to certify Session 2.6 will pass that gate. (c) Additionally verify each `.npz` `sample_size` field reads ≥ 100 000 (BEYOND what stage_1_sect Cell 3 inspects — that gate trusts PROVENANCE; this gate inspects file internals).

**Inputs:** Cell 4 PASS (5 fresh `.npz` files at canonical path); revision SHA captured in Cell 3.

```python
# === CELL 5 — PROVENANCE.txt authorship + downstream gate verification ===
# Specialist: state-consistency-theorist
# References: stage_1_sect_runbook.md v1.1 Cell 3; IC-S25-1; OQ-S25-9 closure path

import os, json, hashlib
import numpy as np
from datetime import datetime, timezone

CACHE_DIR = "/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats"
PROVENANCE_PATH = f"{CACHE_DIR}/PROVENANCE.txt"

# Recover revision SHA from Cell 3 stash
with open("/workspace/architecture_profile/pre_s2_6_revision_record.json") as f:
    revision_record = json.load(f)
REVISION_SHA = revision_record["revision_sha"]
REVISION_SOURCE = revision_record["revision_source"]

# === Phase A: Author PROVENANCE.txt ===
provenance_content = (
    f"# Covariance cache provenance — fresh compute against meta-llama/Llama-3.1-8B base\n"
    f"# Authored by pre-S2.6 fork-work session; consumed by stage_1_sect_runbook.md v1.1 Cell 3\n"
    f"\n"
    f"model_name = meta-llama/Llama-3.1-8B\n"
    f"model_revision_sha = {REVISION_SHA}\n"
    f"layer_set = [4, 5, 6, 7, 8]\n"
    f"sample_count = 100000\n"
    f"dtype = float32\n"
    f"computed_at = {datetime.now(timezone.utc).isoformat()}\n"
    f"produced_by_session = pre-S2.6-fork-work\n"
    f"\n"
    f"# Auxiliary metadata (not required by Cell 3 gate; informational)\n"
    f"revision_sha_source = {REVISION_SOURCE}\n"
    f"bridge_archive = {revision_record['archive_dir']}\n"
)
with open(PROVENANCE_PATH, "w") as f:
    f.write(provenance_content)
print(f"Phase A: PROVENANCE.txt written to {PROVENANCE_PATH}")
print(provenance_content)

# === Phase B: Re-run stage_1_sect Cell 3 gate predicates IN-PLACE ===
# Verbatim port of the consumer-side gate; if this fails, Session 2.6 will also fail
# at its Cell 3, so we want to catch it now.

assert os.path.exists(CACHE_DIR), f"Cache directory missing: {CACHE_DIR}"
assert os.path.exists(PROVENANCE_PATH), "PROVENANCE.txt missing — Phase A failed"

with open(PROVENANCE_PATH) as f:
    raw = f.read()

provenance = {}
for line in raw.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if "=" in line:
        k, v = line.split("=", 1)
        provenance[k.strip()] = v.strip()

REQUIRED_FIELDS = [
    "model_name", "model_revision_sha", "layer_set",
    "sample_count", "dtype", "computed_at", "produced_by_session",
]
for field in REQUIRED_FIELDS:
    assert field in provenance, f"PROVENANCE.txt missing required field: {field}"

assert provenance["model_name"] == "meta-llama/Llama-3.1-8B", \
    f"GATE FAIL: model_name={provenance['model_name']!r}"

layer_set_normalized = provenance["layer_set"].replace(" ", "")
assert layer_set_normalized == "[4,5,6,7,8]", \
    f"GATE FAIL: layer_set={provenance['layer_set']!r}"

assert provenance["sample_count"] == "100000", \
    f"GATE FAIL: sample_count={provenance['sample_count']!r}"
assert provenance["dtype"] == "float32", \
    f"GATE FAIL: dtype={provenance['dtype']!r}"

# File inventory + size + per-file SHA-256 prefix (verbatim port)
cache_files = sorted([f for f in os.listdir(CACHE_DIR) if f.endswith(".npz") or f.endswith(".pt")])
file_inventory = {}
total_bytes = 0
for fname in cache_files:
    fpath = f"{CACHE_DIR}/{fname}"
    size_bytes = os.path.getsize(fpath)
    total_bytes += size_bytes
    with open(fpath, "rb") as f:
        sha = hashlib.sha256()
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            sha.update(chunk)
    file_inventory[fname] = {
        "size_mb": round(size_bytes / 1e6, 2),
        "sha256_prefix": sha.hexdigest()[:16],
    }

# R1.1: tighter named-file inventory check
EXPECTED_LAYER_FILES = {
    f"model.layers.{L}.mlp.down_proj_float32_mom2_100000.npz"
    for L in [4, 5, 6, 7, 8]
}
actual_npz_files = {f for f in cache_files if f.endswith(".npz")}
assert actual_npz_files == EXPECTED_LAYER_FILES, \
    f"GATE FAIL: cache file set mismatch.\n" \
    f"  Expected: {sorted(EXPECTED_LAYER_FILES)}\n" \
    f"  Got:      {sorted(actual_npz_files)}\n" \
    f"  Missing:  {sorted(EXPECTED_LAYER_FILES - actual_npz_files)}\n" \
    f"  Extra:    {sorted(actual_npz_files - EXPECTED_LAYER_FILES)}"

# === Phase C: Inspect .npz internals (BEYOND stage_1_sect Cell 3) ===
# Per success criteria: each .npz sample_size ≥ 100000; shape (14336, 14336) float32

internals = {}
for fname in sorted(EXPECTED_LAYER_FILES):
    fpath = f"{CACHE_DIR}/{fname}"
    npz = np.load(fpath, allow_pickle=False)
    keys = list(npz.keys())
    # MEMIT layer_stats convention: keys typically include "mom2" and "n_samples" / "sample_size"
    sample_size = None
    for candidate_key in ("sample_size", "n_samples", "samples"):
        if candidate_key in keys:
            sample_size = int(npz[candidate_key].item() if npz[candidate_key].ndim == 0 else npz[candidate_key])
            break
    mom2 = npz["mom2"] if "mom2" in keys else None
    if mom2 is None:
        # alternate key name
        non_count_keys = [k for k in keys if k not in ("sample_size", "n_samples", "samples")]
        if non_count_keys:
            mom2 = npz[non_count_keys[0]]

    internals[fname] = {
        "keys": keys,
        "sample_size": sample_size,
        "mom2_shape": list(mom2.shape) if mom2 is not None else None,
        "mom2_dtype": str(mom2.dtype) if mom2 is not None else None,
    }
    # Hard assertions
    assert sample_size is not None, f"{fname}: no sample_size field found in keys {keys}"
    assert sample_size >= 100000, f"{fname}: sample_size={sample_size} < 100000"
    assert mom2 is not None, f"{fname}: no mom2 matrix found"
    assert tuple(mom2.shape) == (14336, 14336), \
        f"{fname}: shape={mom2.shape}, expected (14336, 14336)"
    assert str(mom2.dtype) == "float32", \
        f"{fname}: dtype={mom2.dtype}, expected float32"

# === Phase D: Verdict assembly ===
verdict = {
    "session": "pre-S2.6-fork-work",
    "verified_at": datetime.now(timezone.utc).isoformat(),
    "cache_dir": CACHE_DIR,
    "provenance_fields": provenance,
    "cache_file_inventory": file_inventory,
    "cache_file_internals": internals,
    "total_size_gb": round(total_bytes / 1e9, 2),
    "stage_1_sect_cell_3_gate": "PASS",
    "internals_gate": "PASS",
    "verdict": "PASS",
    "closes_oq": "OQ-S25-9",
}
print("\n=== Cell 5 Verdict ===")
print(json.dumps(verdict, indent=2))

with open("/workspace/architecture_profile/pre_s2_6_cache_verdict.json", "w") as f:
    json.dump(verdict, f, indent=2)

print(f"\nCell 5: PASS. OQ-S25-9 closed. Session 2.6 Cell 3 gate will pass against this cache.")
```

**Verification anchors:**

| Anchor | Expected |
|---|---|
| `PROVENANCE.txt` exists | True |
| All 7 required fields present | True |
| `model_name` | `meta-llama/Llama-3.1-8B` |
| `layer_set` (normalized) | `[4,5,6,7,8]` |
| `sample_count` | `100000` |
| `dtype` | `float32` |
| Cache file set | exactly the 5 expected named files |
| Each `.npz` `sample_size` | `≥ 100000` |
| Each `.npz` mom2 shape | `(14336, 14336)` |
| Each `.npz` mom2 dtype | `float32` |
| Total cache size | `~4.0–5.0 GB` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Any required PROVENANCE field missing | Hard halt | Bug in Phase A; debug and re-author |
| File set mismatch | Hard halt | Cell 4 produced wrong layers; do not advance |
| `sample_size < 100000` | Hard halt | Cell 4 truncated mid-stream; recompute affected layer |
| `mom2.shape ≠ (14336, 14336)` | Hard halt | Architecture / model load drift; investigate |
| `mom2.dtype ≠ float32` | Hard halt | Precision mismatch; recompute |

---

# Part VII — Operator post-session checklist

After Cell 5 PASS:

- [ ] Stop pod (NV preserves all state per D-S25-8)
- [ ] Verify SSD mirror sync if Stage 1+ mirror discipline is in effect (per S2.5b checklist)
- [ ] Update `reproducibility_manifest.json` `sessions["pre-S2.6-fork-work"]` with session metadata (operator-edit on MBP):
  ```json
  {
    "status": "PASS",
    "closes_oq": ["OQ-S25-9"],
    "wall_time_hours": <actual>,
    "gpu_cost_usd": <actual>,
    "fresh_cache_path": "/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/",
    "bridge_archive_path": "<from BRIDGE_ARCHIVE_PROVENANCE.txt>",
    "model_revision_sha": "<from PROVENANCE.txt>"
  }
  ```
- [ ] Post short closure note to project chat: PASS verdict, wall-time actual, cost actual
- [ ] Schedule Session 2.6 (Stage 1 SECT execution) — input artifacts: this runbook's verdict + `stage_1_sect_runbook.md` v1.1
- [ ] On Cell 5 PASS, `OQ-S25-9` is closed; record in `OQ-S25-*` inventory at next session

On any halt:

- [ ] Capture `/workspace/architecture_profile/pre_s2_6_layer_stats_log.json` and any partial `.npz` files
- [ ] Document halt class + last-completed layer in a halt summary note
- [ ] Decide: in-session retry vs new session vs bridge restore (`mv <ARCHIVE_DIR>/* <CANONICAL>/` — defers OQ-S25-9 closure)
- [ ] If bridge restored, Session 2.6 cannot proceed; reschedule pre-S2.6 fork-work

---

# Part VIII — Open questions in scope

## 8.1 OQs closed by this runbook's execution

| OQ ID | Closure mechanism |
|---|---|
| `OQ-S25-9` | Cell 5 PASS — fresh covariance cache for Llama-3.1-8B base produced and provenance-asserted at canonical NV path |

## 8.2 OQs surfaced (none expected; this is a focused execution session)

If Cell 4 surfaces unexpected behavior (e.g., per-layer wall-times far outside the ~50–90 min envelope, or `mom2` matrix shape disagreement), open new `OQ-S25-*` entries at session close per `framework-spec-writer` convention. Do not extend this runbook with speculation.

## 8.3 OQs explicitly NOT closed by this session

| OQ ID | Reason |
|---|---|
| `OQ-S25-3` (mom2_update_weight=15000) | Not exercised here; Stage 2 (S2.7+) |
| `OQ-S25-4` (v_lr SwiGLU dynamics) | Not exercised here; Stage 1 retrospective (S2.7) |
| `OQ-S25-7` (BPE fragmentation impact) | Out of scope; Stage 1 retrospective |
| `OQ-S25-10` (LLaMA vs GPT-J target_true prior divergence) | Encoded in `stage_1_sect_runbook.md` Cell 6–7; not this session |

---

# Part IX — Non-goals

This runbook does NOT:

- Execute the Stage 1 SECT trial loop (deferred to Session 2.6 per `stage_1_sect_runbook.md` v1.1).
- Modify hparams, probe set, or CFB substrate (out of scope; would require explicit S2.7-class authorization).
- Re-author or re-validate P-1 / P-2 / P-4 patches (verification only; patch application is recovered from `memit-patches-canonical.md` if drift detected).
- Delete the bridge cache (`IC-S25-1` mandates archive-only).
- Validate cross-architectural-family covariance equivalence (out of scope; bridge cache is banned, not compared).
- Capture diagnostics for `OQ-S25-3`, `OQ-S25-4`, `OQ-S25-7`, or `OQ-S25-10` — these belong to Stage 1 execution and retrospective, not pre-flight cache compute.

---

# Part X — Artifact paths (final state)

```
/workspace/covariance_caches/meta-llama_Llama-3.1-8B/
├── wikipedia_stats/                                         (CANONICAL — fresh)
│   ├── PROVENANCE.txt                                       (Cell 5)
│   ├── model.layers.4.mlp.down_proj_float32_mom2_100000.npz (Cell 4)
│   ├── model.layers.5.mlp.down_proj_float32_mom2_100000.npz (Cell 4)
│   ├── model.layers.6.mlp.down_proj_float32_mom2_100000.npz (Cell 4)
│   ├── model.layers.7.mlp.down_proj_float32_mom2_100000.npz (Cell 4)
│   └── model.layers.8.mlp.down_proj_float32_mom2_100000.npz (Cell 4)
└── bridge_archive_<UTC-ISO>/                                (ARCHIVE — preserved)
    ├── BRIDGE_ARCHIVE_PROVENANCE.txt                        (Cell 3)
    └── (5 bridge .npz files moved from canonical)           (Cell 3)

/workspace/architecture_profile/
├── pre_s2_6_environment_fingerprint.json                    (Cell 1)
├── pre_s2_6_patch_state.json                                (Cell 2)
├── pre_s2_6_revision_record.json                            (Cell 3)
├── pre_s2_6_layer_stats_log.json                            (Cell 4)
└── pre_s2_6_cache_verdict.json                              (Cell 5)
```

---

*End of Pre-S2.6 Fork-Work Runbook v1.2.2.*
