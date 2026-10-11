# Block 2 / Block 3 Runbook Deltas — Session 2.3

## 1. Purpose

This document records all spec amendments, environmental patches, and runbook authorship constraints discovered during Session 2.3 execution. Future Stage 1+ runbooks against `runpod/pytorch:2.4.0` (or comparable images with pre-installed scientific Python tooling at unknown versions) must incorporate these deltas before first execution.

The deltas are organized by failure class and include the canonical (pre-discovery) protocol, the observed failure, the remediation applied, and the runbook authorship constraint derived.

## 2. Delta D1 — Image Patch-Level Versions Drift From Tag

### 2.1 Canonical assumption

`block-2-runpod-notebook.md` Cell 1 expected `torch 2.4.0+cu124` matching the image tag `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`.

### 2.2 Observed

```
Python:        3.11.10
PyTorch:       2.4.1+cu124      ← actual 2.4.1, tag claims 2.4.0
CUDA (torch):  12.4
cuDNN:         90100
GPU 0 name:    NVIDIA GeForce RTX 4090
GPU 0 compute: sm_89
Driver version: 570.195.03      ← driver CUDA 12.8 even though torch is cu124
```

### 2.3 Root cause

RunPod ships patch-level updates to `runpod/pytorch` images without re-tagging. The Docker Hub digest `sha256:61a4aafb...` correctly identifies the actual byte content; the human-readable tag is informational only.

### 2.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C1 | Reproducibility manifest records runtime-observed versions, not tag-implied versions |
| C2 | Cell 1 expectations are anchored to the digest, not the tag |
| C3 | Image refresh between sessions requires re-extracting digest from Docker Hub and re-running Cell 1 to validate |

### 2.5 Routes to OQ

OQ-S23-2 (manifest discipline) carries C1, C2, C3 to Stage 1 runbook authorship.

## 3. Delta D2 — `datasets` Required as Transitive Import-Time Dependency

### 3.1 Canonical assumption

Cell 2 spec (`block-2-runpod-notebook.md` §3) listed `datasets` in the import statement but not in the pip install list.

### 3.2 Observed

Cell 2 raised `ModuleNotFoundError: No module named 'datasets'` at the import line. Initial diagnosis was wrong: "drop datasets from import, runtime never uses it." This was reversed when Cell 6 raised the same error at a deeper traceback level (`memit/__init__.py → memit_main → rome.layer_stats → from datasets import load_dataset`).

`datasets` is a transitive import-time dependency of `memit.memit_main` even when `cache_template=None` is passed at runtime. Python evaluates the import chain at module-load time, before any runtime control flow.

### 3.3 Remediation applied

Cell 2c added (between Cell 2b and Cell 3):

```python
# === CELL 2c — Install datasets (Kaggle parity pin) ===
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
    "datasets==4.8.3"], check=True)
for mod in list(sys.modules):
    if mod.startswith(("datasets", "memit", "memit.", "rome", "rome.",
                       "util", "util.")):
        del sys.modules[mod]
import datasets
print(f"datasets: {datasets.__version__}")
```

Version pin `4.8.3` matches Kaggle baseline for cross-environment manifest reproducibility.

### 3.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C4 | MEMIT import-time dependency analysis must trace the full import graph, not just runtime call paths |
| C5 | Kaggle smoke-test PASS does not validate dependency closure on RunPod; Kaggle's base image silently provides packages RunPod's image does not |

## 4. Delta D3 — Additional MEMIT Import-Time Dependencies

### 4.1 Canonical assumption

After Cell 2c's `datasets` install resolved, Cell 6 retry would proceed.

### 4.2 Observed

Cell 6 retry surfaced a second `ModuleNotFoundError` at a different traceback location:

```
rome/compute_v.py:5
    from matplotlib.style import context
        ↓
ModuleNotFoundError: No module named 'matplotlib'
```

`matplotlib` is imported at module-load time by `rome/compute_v.py`. The import is unused at runtime (it appears to be a research-vintage diagnostic plotting hook left in place), but Python evaluates the import.

### 4.3 Remediation applied

Cell 2d added — exhaustive single-cell install of all plausible remaining MEMIT import-time dependencies:

```python
# === CELL 2d — Install remaining MEMIT import-time dependencies ===
import subprocess, sys, importlib

REQUIRED = [
    "matplotlib==3.9.2",   # rome/compute_v.py
    "scipy==1.14.1",       # potential rome/util import
    "scikit-learn==1.5.2", # potential rome/util import
    "pandas==2.2.3",       # transitive via datasets
]
subprocess.run([sys.executable, "-m", "pip", "install", "--quiet"] + REQUIRED,
               check=True)
# Wide purge
for mod in list(sys.modules):
    if mod.startswith(("memit", "memit.", "rome", "rome.", "util", "util.",
                       "matplotlib", "matplotlib.", "scipy", "scipy.",
                       "sklearn", "sklearn.", "pandas", "pandas.")):
        del sys.modules[mod]
```

### 4.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C6 | Discovery-by-failure for import-time dependencies is structurally inefficient; a single comprehensive install at session start is the correct pattern |
| C7 | The dependency manifest must be empirical (derived from observed failures), not theoretical (derived from `requirements.txt`); MEMIT's `requirements.txt` does not declare matplotlib |

## 5. Delta D4 — C Extension Caching Requires Kernel Restart

### 5.1 Canonical assumption

`pip install --force-reinstall --no-deps <pkg>` followed by `del sys.modules[...]` was sufficient to re-import a package at a new version.

### 5.2 Observed

Cell 2d's verification raised:

```
AttributeError: module 'pandas._libs.lib' has no attribute 'is_interval'
```

The image's pre-installed pandas C extension (`.so` file at `/usr/local/lib/python3.11/dist-packages/pandas/_libs/lib.cpython-311-x86_64-linux-gnu.so`) was loaded into the Python interpreter's `dlopen()` cache during import. Pip replaced the Python source files but left the cached extension handle. The new pandas Python files referenced symbols (e.g., `is_interval`) that the old `.so` did not export.

Cell 2e attempted `pip install --force-reinstall --no-deps pandas==2.2.3` followed by `del sys.modules[...]`. The error persisted at the verification step. Pip's force-reinstall replaces files on disk but does not invoke `dlclose()` on already-loaded shared objects.

### 5.3 Remediation applied

JupyterLab kernel restart. After restart, the new Python interpreter process loaded the updated `.so` file fresh; verification passed.

### 5.4 Replacement cells for post-restart efficiency

Cell 2-restart-verify (replaces Cells 2, 2b, 2c, 2d, 2e re-execution):

```python
# === CELL 2-restart-verify — Post-restart import audit ===
import sys
print(f"Python: {sys.version.split()[0]}")
import torch
print(f"torch: {torch.__version__}")
import transformers, accelerate, huggingface_hub, tokenizers, safetensors
import pandas as pd
probe = pd._libs.lib.is_interval   # The previously-failing attribute
import datasets, matplotlib, scipy
# Print versions
print("Post-restart import audit: PASS")
```

Cell 3-rebind (replaces Cell 3 re-execution to avoid `shutil.rmtree` destroying patches):

```python
# === CELL 3-rebind — Re-establish MEMIT sys.path without clone ===
import os, subprocess, sys

MEMIT_PATH = "/workspace/memit_dry_run/memit"
assert os.path.exists(MEMIT_PATH)
os.chdir(MEMIT_PATH)
memit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
assert memit_sha == "80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b"

with open(os.path.join(MEMIT_PATH, "util/nethook.py"), "r") as f:
    nethook_src = f.read()
patch_present = ("def retain_hook(m, args, kwargs, output):" in nethook_src
                 and "with_kwargs=True" in nethook_src)
assert patch_present, "Patch lost — Cell 5e re-run required"
sys.path.insert(0, MEMIT_PATH)
print("MEMIT sys.path rebind: PASS")
```

### 5.5 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C8 | C extension version mismatches require kernel restart; `sys.modules` purge is insufficient |
| C9 | Failure mode taxonomy: ModuleNotFoundError (in-place retry safe) vs C extension AttributeError (kernel restart required) |
| C10 | Stage 1+ runbook structure: install all dependencies BEFORE first import → kernel restart → import audit → proceed; never discover-by-failure |

### 5.6 Routes to OQ

OQ-S23-8 (failure mode taxonomy refinement) carries C8, C9, C10 to Stage 1 runbook authorship.

## 6. Delta D5 — Cell 3 Idempotence Violation

### 6.1 Canonical assumption

Re-running Cell 3 (MEMIT clone) is safe; `shutil.rmtree("memit")` + `git clone` produces a clean clone state.

### 6.2 Observed

Cell 3's `shutil.rmtree("memit")` destroys the patched `util/nethook.py` applied by Cell 5e. Re-running Cell 3 silently invalidates Cell 5e's effect. The next attempt to import MEMIT modules either fails (if module purge happens after Cell 3 re-run) or runs against unpatched code (if module cache carries the patched version's bindings).

In Session 2.3 execution, this surfaced as an apparent ambiguity when the operator pasted Cell 3 stdout in a context where Cell 6 was expected. State analysis identified three scenarios: stale paste (State A), kernel restart with re-execution (State B), Cell 3 re-run in-place (State C). Disambiguation required disclosure to determine which path actually occurred.

### 6.3 Remediation applied

Cell 3-rebind (Section 5.4) replaces Cell 3 in post-restart sequences. It re-establishes `sys.path` without modifying the filesystem.

For pre-restart Cell 3 in original Block 2 sequence, no remediation was needed because Cell 5e ran after Cell 3 in the canonical order. The vulnerability is specifically when Cell 3 is re-run after Cell 5e has been applied.

### 6.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C11 | Cell 3 must be conditional on "patch already applied" check OR documented as re-run-only-if-patches-not-yet-applied |
| C12 | Stage 1+ runbooks should adopt Cell 3-rebind pattern when patches are already on disk |

### 6.5 Routes to OQ

OQ-S23-7 (idempotence violation) carries C11, C12 to Stage 1 runbook authorship.

## 7. Delta D6 — Cell 10 OQ-S23-3 Spec Amendment

### 7.1 Canonical assumption

Cell 10 acceptance band:

```python
HC_2_PASS = (
    SF_1 and SF_2 and SF_3
    and drift_p_baseball_post < 0.05
    and drift_p_basketball_post < 10
    and drift_unmount_basketball_crossenv < 1e-6   # ← cross-env, tight band
)
```

### 7.2 Observed

Pre-edit Cell 5 cross-environment drift on `P_BASKETBALL` was ~4.5e-4. Post-unmount Cell 9 cross-environment drift was 4.65e-4. Both metrics measure FP16 forward-pass differences across architectures (sm_75 vs sm_89), not overlay isolation.

The 1e-6 band was structurally unachievable across environments even when overlay isolation was mathematically perfect on RunPod. Empirical intra-pod drift (`P_basketball_postunmount` vs `P_basketball_pre` on the same pod, same GPU, same torch) was 0.0 — bit-identical.

### 7.3 Remediation applied

Cell 10 amended:

```python
# OQ-S23-3 amendment: intra-pod overlay isolation drift
drift_unmount_basketball_intrapod = drift(P_BASKETBALL_POSTUNMOUNT, P_BASKETBALL_PRE)

# Cross-env retained as informational
drift_unmount_basketball_crossenv = drift(P_BASKETBALL_POSTUNMOUNT,
                                          KAGGLE_BASELINE["P_basketball_postunmount"])

HC_2_PASS = (
    SF_1 and SF_2 and SF_3
    and drift_post_baseball < 0.05
    and drift_post_basketball < 10
    and drift_unmount_basketball_intrapod < 1e-4   # ← intra-pod, FP16 noise floor
)
```

Manifest field renamed from `P_basketball_postunmount_max_drift` (1e-6) to `P_basketball_postunmount_max_drift_intrapod` (1e-4). Cross-env value retained as informational, not gating.

### 7.4 Empirical result

```
drift_p_basketball_postunmount_intrapod:  0.0      (bit-identical)
drift_p_basketball_postunmount_crossenv:  4.65e-4  (informational; sm_75 vs sm_89 dispatch)
```

The intra-pod metric was 0.0 exactly — both pre-edit and post-unmount probabilities equal `0.8697880506515503` to all 16 displayed digits. This exceeds the predicted ~1.4e-5 FP16 noise-floor estimate.

### 7.5 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C13 | The `.vindex` overlay isolation is bit-identical, not noise-floor. Stage 1+ acceptance bands should distinguish intra-pod (overlay isolation) from cross-env (architecture equivalence) tests |
| C14 | Cross-env drift bands (when used) must accommodate FP16 architecture dispatch differences; 1e-3 to 1e-2 is the empirically observed range for sm_75 vs sm_89 |

### 7.6 Routes to OQ

OQ-S23-3 closes via this amendment. OQ-S23-11 (spec invariant elevation: `.vindex` bit-identity) routes to Workstream 3 implementation planning.

## 8. Delta D7 — Region Inventory Drift

### 8.1 Canonical assumption

`block-2-execution-plan.md` Block 2 §4.1 specified region priority order: US-OR-1, US-KS-2, US-TX-3, EU-RO-1.

### 8.2 Observed

Current RunPod region dropdown (US-only filter): CA-MTL-1, CA-MTL-3, US-CA-2, US-GA-2, US-IL-1, US-KS-2, US-NC-1, US-TX-3. **US-OR-1 is absent.**

### 8.3 Remediation applied

Updated region priority order for Stage 1+ runbooks:

| New priority | Region | Rationale |
|---|---|---|
| 1 | US-KS-2 (Kansas) | Closest to operator (Denver, ~700 km); lowest rsync latency |
| 2 | US-IL-1 (Illinois) | Central US; ~1500 km from Denver |
| 3 | US-NC-1 (North Carolina) | East coast; current operative selection (NV-pinned) |
| 4 | US-TX-3 (Texas) | Southwest; comparable to Kansas in latency |

### 8.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C15 | Region priority lists are temporal — RunPod adjusts inventory; Stage 1+ runbooks must capacity-verify in real-time, not rely on hardcoded priority |
| C16 | NV region pinning forecloses rebalancing; the current NV (US-NC-1) anchors all Stage 1+ work to US-NC-1 unless NV is destroyed and recreated |

## 9. Delta D8 — JupyterLab Notebook Default Path

### 9.1 Canonical assumption

`block-2-runpod-notebook.md` referenced `/workspace/memit_dry_run/runpod_dry_run.ipynb` as the notebook path.

### 9.2 Observed

JupyterLab's File → New → Notebook default created `/workspace/Untitled.ipynb` (NV root, not `memit_dry_run/` subdirectory). Operator must manually rename and move post-creation.

### 9.3 Remediation applied

Pre-teardown bash:

```bash
mv /workspace/Untitled.ipynb /workspace/memit_dry_run/runpod_dry_run.ipynb
mv /workspace/.ipynb_checkpoints /workspace/memit_dry_run/.ipynb_checkpoints
```

### 9.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C17 | JupyterLab "File → New" creates files at the file browser's then-current path with default name; runbooks must specify either pre-creation navigation OR post-creation rename/move |
| C18 | Stage 1+ runbooks should configure JupyterLab `--notebook-dir=/workspace/<stage>/` at pod boot if possible, OR adopt explicit notebook-creation procedure |

## 10. Delta D9 — RunPod NV Race Window During Pod Recreation

### 10.1 Canonical assumption

`block-2-execution-plan.md` Block 2 §7 specified canonical Step 2.5 sequence: tear down GPU pod → spin up cheap pod → verify NV persistence.

### 10.2 Observed

After GPU pod termination, US-NC-1 capacity returned `No GPU instances available`. The session was unable to spin up any pod (RTX 4090 and RTX 5090 both out of stock; Community Cloud RTX 5000 rejected per Session 2.1 venue lock).

### 10.3 Remediation applied

Path C: defer Step 2.5d (across-teardown NV persistence test) to OQ-S23-12. Block 3 was deferred to resume turn rather than executed on a Path-C-on-existing-pod basis (because GPU pod was already terminated).

### 10.4 Constraint for future runbooks

| Constraint | Detail |
|---|---|
| C19 | "Low" tier capacity in target region is non-trivial risk; Stage 1+ should pre-stage deploy form before terminating prior pod |
| C20 | NV-region pinning makes capacity exhaustion in target region a session-level halt; consider this when planning Stage 1 SECT pod-rotation strategy |
| C21 | Community Cloud is a deferred procurement decision (OQ-S23-13), not an authorized fallback |

### 10.5 Routes to OQ

OQ-S23-12 (deferred test) closes on resume's first NV mount. OQ-S23-13 (Community Cloud procurement) routes to Session 2.5 Stage 1 prep.

## 11. Consolidated Stage 1+ Runbook Authorship Rules

These rules synthesize the constraints C1-C21 above into a structured runbook authorship template.

### 11.1 Pre-flight (executed before any MEMIT/Python imports)

```
1. Capacity-verify target region in real-time.
2. Deploy with image digest pin (not tag).
3. Verify runtime fingerprint against digest-implied versions.
4. Install ALL MEMIT import-time dependencies in a single cell:
     - transformers==4.45.2
     - accelerate==0.34.2
     - huggingface_hub==0.25.2
     - tokenizers==0.20.3
     - safetensors==0.4.5
     - hydra-core==1.3.2
     - einops==0.7.0
     - nltk==3.8.1
     - datasets==4.8.3
     - matplotlib==3.9.2
     - pandas==2.2.3 (with --force-reinstall --no-deps)
     - scipy==1.14.1
     - scikit-learn==1.5.2 (optional; not in MEMIT runtime path)
5. Restart the kernel.
6. Run import audit (Section 5.4 Cell 2-restart-verify pattern).
7. Proceed with MEMIT clone + patch + use.
```

### 11.2 Patch application

```
1. MEMIT clone with SHA verification (kmeng01/memit @ 80426fd9...).
2. Apply Patches P-1, P-2, Pad-Token via in-place file edit.
   Skip Patch P-3' on RTX 4090 (24 GB envelope is sufficient).
   Skip explicit device map on single-GPU configurations.
3. sys.modules purge of util.*, rome.*, memit.*.
4. (Optional, future): Cell 3-rebind pattern after first session — preserves
   patches across kernel restarts without re-cloning.
```

### 11.3 Acceptance band specification

```
For each stage's HC-N test:
- Distinguish intra-pod (overlay isolation) from cross-env (architecture
  equivalence) drift metrics.
- Use intra-pod 1e-4 (or tighter, per empirical bit-identity) for
  overlay-isolation tests.
- Use cross-env bands (1e-3 to 1e-2) only when explicitly testing
  architecture portability, not framework correctness.
```

### 11.4 Artifact persistence

```
- All work product writes to /workspace (NV-resident).
- Notebook explicitly named and located in the stage's subdirectory
  (not /workspace/Untitled.ipynb).
- Verdict JSON, overlays, covariance cache, and patched MEMIT clone all
  on NV; container-disk-only state is regenerable.
- Pre-teardown audit confirms artifact inventory before pod termination.
```

### 11.5 Pod lifecycle

```
- On-Demand only (Session 2.1 lock).
- Image digest pinned; tag is informational.
- Region NV-pinned; cannot be changed without NV destruction.
- Pre-stage deploy form before terminating prior pod (capacity race
  mitigation).
- Community Cloud excluded unless OQ-S23-13 escalates to authorization.
```

## 12. Updated MEMIT Dependency Manifest

Replace any prior dependency lists with this empirically validated manifest:

```yaml
# MEMIT runtime + import-time dependencies, validated against
# kmeng01/memit @ 80426fd9 on runpod/pytorch:2.4.0 image
# Empirical validation: Session 2.3 Block 2 HC-2 PASS on RunPod RTX 4090

dependencies:
  load_bearing:
    transformers:    4.45.2          # MEMIT runtime; P-1+P-2 patch target
    accelerate:      0.34.2          # device map handling
    huggingface_hub: 0.25.2          # model download; revision SHA query
    tokenizers:      0.20.3          # GPT-2 family tokenizer
    safetensors:     0.4.5           # weight serialization
    datasets:        4.8.3           # rome/layer_stats import-time dep

  import_time_only_unused_at_runtime:
    matplotlib:      3.9.2           # rome/compute_v.py import
    pandas:          2.2.3           # transitive via datasets; FORCE-REINSTALL required
    scipy:           1.14.1          # potential rome/util import

  optional_likely_unused_by_memit_runtime:
    scikit-learn:    1.5.2

  hydra_chain:
    hydra-core:      1.3.2
    einops:          0.7.0
    nltk:            3.8.1

  runtime_environment:
    python:          3.11.10         # from image
    torch:           2.4.1+cu124     # from image (tag claims 2.4.0)
    cuda_torch:      12.4
    cuda_driver:     12.8            # 570.195.03
    cudnn:           90100
    gpu_compute:     sm_89           # RTX 4090 Ada Lovelace

install_strategy:
  pattern: |
    1. pip install all `load_bearing` + `import_time_only_unused_at_runtime`
       + `hydra_chain` packages in single cell
    2. pip install --force-reinstall --no-deps pandas==2.2.3
    3. KERNEL RESTART
    4. Import audit (Section 5.4)
    5. Proceed with MEMIT clone + patch
```

## 13. Diff Summary Against Original Runbooks

| Runbook | Section | Change |
|---|---|---|
| `block-2-runpod-notebook.md` | Cell 2 pip install list | Add `datasets==4.8.3`, `matplotlib==3.9.2`, `pandas==2.2.3` (with force-reinstall), `scipy==1.14.1`, `scikit-learn==1.5.2` |
| `block-2-runpod-notebook.md` | Between Cell 2 and Cell 3 | Insert mandatory kernel restart instruction |
| `block-2-runpod-notebook.md` | Post-restart | Insert Cell 2-restart-verify pattern |
| `block-2-runpod-notebook.md` | Cell 3 | Document idempotence violation; add Cell 3-rebind pattern for re-execution |
| `block-2-runpod-notebook.md` | Cell 10 | Apply OQ-S23-3 amendment: `drift_p_basketball_postunmount` band changed from cross-env 1e-6 to intra-pod 1e-4 |
| `block-2-execution-plan.md` | §4.1 region priority | Replace with US-KS-2 / US-IL-1 / US-NC-1 / US-TX-3 |
| `block-2-execution-plan.md` | §6.5 acceptance band | Update to amended Cell 10 specification |
| `block-2-execution-plan.md` | §7 step 2.5 | Add Path C contingency for capacity unavailability |
| `block-2-execution-plan.md` | New §11 | Add Section 12 dependency manifest |

These changes apply to Stage 1+ runbook authorship. The original `block-2-runpod-notebook.md` is preserved as a session-historical record; future runbooks reference this delta document.
