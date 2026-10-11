# Block 2 — RunPod Activation Execution Plan

> **Workstream:** 1 — Empirical POC Scoping
> **Block:** 2 — RunPod Activation, Network Volume Provisioning, Dry-Run Pod
> **Predecessor:** Session 2.2 Block 1 (PASS verdict, 2026-04-26)
> **Successor:** Block 3 — Persistent State Architecture and Reproducibility Manifest Finalization
> **Primary skill:** `memit-specialist`
> **Secondary skill:** `aiSecOps-specialist` (Warden — tenant isolation, audit posture, billing safety)

---

## 1. Block 2 Scope

| Step | Action | Deliverable |
|---|---|---|
| 2.1 | RunPod account creation, payment method, billing alerts | Account state record |
| 2.2 | Network Volume provisioning (100 GB, region-pinned) | NV ID, region, mount verification |
| 2.3 | PyTorch container image selection and digest pinning | Image digest |
| 2.4 | Dry-run pod with single-fact MEMIT edit reproduction | HC-2 metric vs Kaggle baseline |
| 2.5 | Pod teardown; NV persistence verification | NV state confirmed across pod lifecycle |

Block 2 does NOT include: Stage 1 SECT execution, CFB v1 corpus authorship, probe-set v1 authorship, or full architecture_profile.json drafting (those are separate Stage 0 sub-sessions).

## 2. Inherited Constraints from Session 2.2

### 2.1 Operator decisions (locked)

| Decision | Locked value |
|---|---|
| Primary venue | RunPod Secure Cloud RTX 4090 ($0.69/hr on-demand) |
| Secondary venue | Vast.ai Secure DC RTX 4090 (capacity fallback only) |
| Stage 2 sweep tier | On-demand (no preemption) |
| Persistent storage | 100 GB Network Volume on RunPod |
| Local archive | rsync to existing 2020 Intel MBP 16 GB |
| Apple Silicon | Rejected for POC |

### 2.2 Smoke test PASS verdict (locked)

| Component | Verified state |
|---|---|
| MEMIT toolchain on transformers 4.45.2 | PASS (Patches P-1, P-2 required) |
| MEMIT covariance fetch reachability | PASS (`memit.baulab.info` reachable) |
| MEMIT layer write correctness | PASS (6 layers, no NaN/Inf) |
| Overlay isolation | PASS (bit-identical pre/post-unmount) |

### 2.3 Patches required for RunPod RTX 4090

| Patch | Required on RTX 4090? | Rationale |
|---|---|---|
| P-1 (nethook signature) | Yes | Universal; transformers ≥ 4.36 |
| P-2 (with_kwargs registration) | Yes | Universal; transformers ≥ 4.36 |
| P-3' (CPU FP64 solve) | **No** | RTX 4090 has 24 GiB; 4 GiB FP64 transient fits with headroom |
| Pad-Token alias | Yes | Universal for GPT-2-derived tokenizers |
| Explicit device map | **No** | Single GPU; co-location is automatic |
| In-place copy_() unmount | Yes | Universal `.vindex` architecture requirement |

## 3. Step 2.1 — RunPod Account Provisioning

### 3.1 Account creation

| Sub-step | Action |
|---|---|
| 3.1.1 | Sign up at `runpod.io` with operator email |
| 3.1.2 | Verify email |
| 3.1.3 | Complete identity verification if required |
| 3.1.4 | Add payment method (operator-provided; not pasted into chat) |

### 3.2 Billing alert configuration

Three thresholds, escalating monthly burn-rate awareness:

| Threshold | Purpose |
|---|---|
| $50 | Early-stage smoke and dry-run usage caught |
| $150 | Stage 1 SECT execution budget mid-point |
| $300 | POC monthly cap — investigate before exceeding |

RunPod's billing alerts can be set under Account → Billing → Alerts. Alert delivery: email to operator account.

### 3.3 Constraints

| Concern | Action |
|---|---|
| Payment data in chat | Forbidden — operator handles directly |
| Account credentials in chat | Forbidden — operator authenticates directly |
| Billing alert threshold confirmation | Operator confirms in chat once configured |

### 3.4 Reportable items

After Step 2.1 completion, operator reports back to chat:

| Item | Format |
|---|---|
| Account verification status | "verified" / "pending" |
| Payment method added | yes / no |
| Billing alerts configured at $50, $150, $300 | yes / no |
| Account flags or restrictions | none / list |

## 4. Step 2.2 — Network Volume Provisioning

### 4.1 Region selection — load-bearing decision

Network Volumes cannot be cross-region attached to GPU pods. Region selection at NV creation pins all subsequent pod placement to that region. Select the region with:

1. RTX 4090 Secure Cloud capacity availability
2. Lowest network latency to operator location (Denver, CO per session context)
3. Stable historical RTX 4090 pricing at $0.69/hr

**Recommended region order (verify capacity at provisioning time):**

| Priority | Region | Rationale |
|---|---|---|
| 1 | US-OR-1 (Oregon) | Best Pacific coast latency from Denver; consistent RTX 4090 capacity |
| 2 | US-KS-2 (Kansas) | Geographic proximity to Denver; secondary capacity zone |
| 3 | US-TX-3 (Texas) | Backup if Oregon and Kansas are at capacity |
| 4 | EU-RO-1 (Romania) | Last resort; latency penalty for rsync to MBP |

**Operator action: verify RTX 4090 Secure Cloud availability in target region BEFORE creating the NV.** Switching regions later requires NV destruction and re-creation.

### 4.2 NV configuration

| Setting | Value |
|---|---|
| Size | 100 GB |
| Type | Network Volume (not persistent disk; not pod-local) |
| Region | (per §4.1 selection) |
| Name | `llm-database-poc-nv` (or operator preference) |

100 GB allocated rationale (re-confirmed):

| Component | Estimated size |
|---|---|
| Architecture profile outputs (PF-1..PF-6) | 1 GB |
| `.vindex` overlay snapshots (Stage 1+) | 5 GB |
| CFB v1 corpus + baselines | 2 GB |
| Covariance caches (6 layers × ~1 GB each, may need >6 for sweeps) | 10–15 GB |
| Drift sweep results (Stage 2) | 20 GB |
| Calibration data (Stages 3a/b/c) | 15 GB |
| Session logs | 2 GB |
| Headroom | 35–45 GB |
| **Total** | **100 GB** |

### 4.3 Mount verification (test pod)

After NV creation, spin up a minimal pod (cheapest available, e.g., RTX A4000) with NV mounted at `/workspace` to verify:

| Verification | Method |
|---|---|
| NV mounts at expected path | `ls /workspace` succeeds |
| NV is writable | `touch /workspace/mount_test && rm /workspace/mount_test` succeeds |
| NV size matches allocation | `df -h /workspace` shows ~100 GB |
| Region matches selection | RunPod console pod metadata |

Tear down the test pod immediately after verification. NV persists.

### 4.4 Reportable items

| Item | Format |
|---|---|
| Network Volume ID | `nvol-XXXXXXXXX` |
| Network Volume region | Region code |
| Network Volume size confirmed | "100 GB" |
| Mount verification | PASS / FAIL |
| Test pod cost | < $0.10 (target; A4000 cheapest tier) |

## 5. Step 2.3 — PyTorch Container Image Selection

### 5.1 Pinning constraint

Container images on RunPod are versioned by tag and digest. Tags (e.g., `pytorch:2.4.0-py3.11-cuda12.4`) can be moved by RunPod; digests (SHA256) are immutable. **Pin by digest, not tag.**

### 5.2 Image selection criteria

Required image properties:

| Property | Required value |
|---|---|
| PyTorch version | 2.x (2.4 or later); MUST support `register_forward_hook(..., with_kwargs=True)` (PyTorch ≥ 2.0) |
| CUDA version | 12.x (matches RTX 4090 native compute capability sm_89) |
| Python version | 3.10 or 3.11 (transformers 4.45.2 supports both) |
| Pre-installed packages | torch, accelerate, transformers acceptable starting points |
| Image size | Smallest available matching above |

### 5.3 Recommended starting images (verify at provisioning time)

Three candidates, ordered by likely match:

| Candidate | Source | Likely tag pattern |
|---|---|---|
| RunPod PyTorch official | `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` | RunPod-published |
| HuggingFace official | `huggingface/transformers-pytorch-gpu:latest` (must pin by digest) | HuggingFace-published |
| NVIDIA NGC | `nvcr.io/nvidia/pytorch:24.10-py3` | NVIDIA-published |

**Operator action at Step 2.3:** browse RunPod's container catalog under Pods → Templates → PyTorch images, select the most recent stable image matching §5.2 criteria, copy the digest (SHA256) to the manifest. Avoid "latest" tags.

### 5.4 Compatibility test on selected image

Before committing to an image for Stage 1, verify on the dry-run pod (Step 2.4):

```python
import torch, transformers, accelerate
print(f"torch: {torch.__version__}")
print(f"torch.cuda: {torch.version.cuda}")
print(f"transformers: {transformers.__version__}")
print(f"accelerate: {accelerate.__version__}")

# Verify with_kwargs hook flag is supported (P-2 prerequisite)
import torch.nn as nn
m = nn.Linear(4, 4)
def hook(module, args, kwargs, output):
    return output
h = m.register_forward_hook(hook, with_kwargs=True)
h.remove()
print("with_kwargs hook PASS")

# Verify GPU compute capability
props = torch.cuda.get_device_properties(0)
print(f"GPU: {props.name}")
print(f"Compute capability: sm_{props.major}{props.minor}")
assert props.major >= 7, "Compute capability < 7.0 not supported by torch 2.10+"
```

### 5.5 Image installation strategy

If the selected image's pre-installed `transformers` version differs from 4.45.2, install over it on the pod:

```bash
pip install --quiet \
    transformers==4.45.2 \
    accelerate==0.34.2 \
    huggingface_hub==0.25.2 \
    tokenizers==0.20.3 \
    safetensors==0.4.5 \
    hydra-core==1.3.2 \
    einops==0.7.0 \
    nltk==3.8.1
```

This is the same joint pin used in Kaggle Cell 2. Installs persist for the pod's lifetime; if the pod is destroyed and recreated, the install must be repeated. To preserve installs across pod recreations, layer them into the NV at `/workspace/venv` (Stage 1+ optimization).

### 5.6 Reportable items

| Item | Format |
|---|---|
| Selected image (full reference) | `runpod/pytorch@sha256:...` |
| Image digest | `sha256:...` |
| PyTorch version on image | x.y.z |
| CUDA version on image | x.y |
| transformers version after pip install | 4.45.2 |
| `with_kwargs` hook compatibility | PASS / FAIL |

## 6. Step 2.4 — Dry-Run Pod and HC-2 Reproduction

### 6.1 Pod configuration

| Setting | Value |
|---|---|
| GPU | 1× RTX 4090 (Secure Cloud) |
| Network Volume | Mount the NV from §4 at `/workspace` |
| Container image | The pinned image from §5 |
| Pod type | On-demand (not Spot) |
| Region | Match NV region |

### 6.2 Pod startup verification

```bash
# Inside pod terminal
nvidia-smi
df -h /workspace
ls /workspace
```

Expected:

| Anchor | Expected value |
|---|---|
| GPU | NVIDIA RTX 4090 24576 MiB |
| Compute capability | sm_89 (Ada Lovelace) |
| `/workspace` capacity | ~100 GB |
| `/workspace` initial contents | Empty or test pod artifacts (clean these out) |

### 6.3 MEMIT-COMPAT-PROTO-1 single-fact reproduction (HC-2)

Reproduce the same single-fact edit (Michael Jordan → baseball) on RTX 4090 to compare against the Kaggle baseline. Differences from the Kaggle notebook:

| Concern | Kaggle | RunPod RTX 4090 |
|---|---|---|
| GPU count | 2× T4 | 1× RTX 4090 |
| Model load device | `device_map=explicit_map` | `.to("cuda")` |
| Patch P-3' applied | Yes (Cell 5f) | **No** (skip Cell 5f) |
| Cell 4 device map | Explicit Path B | Direct `.to("cuda")` |
| Cell 8 unmount mechanism | `copy_()` (still required) | `copy_()` (still required) |
| All other cells | Unchanged | Unchanged |

### 6.4 RunPod dry-run cell sequence (10 cells, simplified)

The RunPod variant of the canonical notebook is 10 cells (drops Cell 5f, simplifies Cell 4):

```
Cell 1   Environment fingerprint                    (~5 sec)
Cell 2   Pip install joint 4.x-line stack           (~30 sec)
Cell 3   MEMIT clone + SHA verification             (~10 sec)
Cell 4'  Model load .to("cuda") direct              (~5-8 min cache miss)
Cell 5   Pre-edit elicitation                       (<5 sec)
Cell 5b  pad_token alias                            (<1 sec)
Cell 5e  nethook P-1 + P-2 patch                    (<5 sec)
Cell 6   MEMIT edit (GPU FP64 solve, ~3-5 min)      (~3-5 min)
Cell 7   Post-edit verification                     (<5 sec)
Cell 8   Overlay save and unmount via copy_         (~10 sec)
Cell 9   Post-unmount verification                  (<5 sec)
Cell 10  Verdict emission + comparison to Kaggle    (<5 sec)
```

Total dry-run wall time: ~10–15 min.

The full canonical RunPod notebook is provided in `block-2-runpod-notebook.md`.

### 6.5 HC-2 acceptance criteria

The dry-run produces a verdict JSON identical in shape to the Kaggle PASS verdict. Compare numerical fields:

| Metric | Acceptable drift |
|---|---|
| `P_baseball_post` | ±0.05 from Kaggle 0.9819 |
| `P_basketball_post` | within order of magnitude of Kaggle 2.30e-04 |
| `P_basketball_postunmount` | bit-identical to pre-edit (overlay isolation) |
| `P_baseball_postunmount` | bit-identical to pre-edit (overlay isolation) |
| Layer norms (orig) | bit-identical to Kaggle (same model checkpoint) |
| Layer norms (update) | ±0.1 from Kaggle (FP64 GPU vs FP64 CPU may produce minor differences) |

**HC-2 PASS condition:** all three SF assertions PASS on RunPod, AND post-edit probability metrics fall within the drift band above.

**HC-2 FAIL conditions:**

| Symptom | Diagnosis |
|---|---|
| SF-1, SF-2, or SF-3 FAILs on RunPod | Environment-specific MEMIT defect; investigate before Stage 1 |
| Post-edit probabilities differ by >2× from Kaggle | Numerical instability between FP64 GPU and FP64 CPU paths; investigate |
| Layer update norms differ by >0.5 | Solve precision differs materially between paths |

### 6.6 Reportable items

| Item | Format |
|---|---|
| Pod ID | `pod-XXXXXXXXX` |
| Pod hourly cost | $0.69 confirmed |
| Cell 6 wall time | ~3–5 min |
| HC-2 SF-1, SF-2, SF-3 | PASS / FAIL each |
| HC-2 numerical drift from Kaggle | within band / outside band |
| Total dry-run pod cost | < $0.20 (target) |

## 7. Step 2.5 — Pod Teardown and NV Persistence Verification

### 7.1 Teardown sequence

```bash
# Inside pod, before termination
ls -la /workspace                     # Confirm NV contents persisted to /workspace
cp /tmp/dry_run_verdict.json /workspace/   # Copy verdict to NV

# Terminate pod via RunPod console
```

### 7.2 NV persistence verification

After pod termination, spin up a second test pod (any cheap GPU) with the same NV mounted:

```bash
ls -la /workspace
cat /workspace/dry_run_verdict.json
```

| Verification | Expected |
|---|---|
| NV contents present | Yes |
| dry_run_verdict.json content | Matches the Step 2.4 verdict JSON |

Tear down the verification pod.

### 7.3 Reportable items

| Item | Format |
|---|---|
| NV persistence across pod recreation | PASS / FAIL |
| Total Block 2 cost | $0.XX |

## 8. Block 2 Stopping Conditions

### 8.1 Successful completion

All of:

- Step 2.1 account configured with billing alerts
- Step 2.2 NV provisioned and mount-verified
- Step 2.3 image digest pinned and compatibility-tested
- Step 2.4 HC-2 PASS (all three SF assertions, drift within band)
- Step 2.5 NV persistence verified

→ Block 2 closes; Block 3 (persistent state architecture) authorized.

### 8.2 Halt conditions

| Halt class | Trigger |
|---|---|
| Account/billing | Operator unable to verify identity, add payment, or configure alerts |
| NV provisioning | Region capacity unavailable; operator decides whether to wait or use Vast.ai fallback |
| Image incompatibility | All candidate images fail §5.4 compatibility test |
| HC-2 FAIL | Numerical drift exceeds band, or any SF assertion FAILs on RunPod |
| Cost runaway | Block 2 total cost exceeds $5 (indicates an unexpected resource leak) |

### 8.3 Halt action protocol

| Step | Action |
|---|---|
| 1 | Operator pastes failure evidence to chat |
| 2 | Diagnostic sub-session opens for the specific halt class |
| 3 | Block 3 deferred until halt resolved |
| 4 | Stage 1 SECT execution remains blocked until Block 2 closes |

## 9. Estimated Block 2 Wall Time and Cost

| Step | Operator wall time | RunPod cost |
|---|---|---|
| 2.1 (account) | 10 min | $0 |
| 2.2 (NV provisioning + test pod) | 15 min | <$0.05 |
| 2.3 (image selection) | 10 min | $0 (browsing) |
| 2.4 (dry-run pod, ~15 min runtime) | 20 min | ~$0.18 |
| 2.5 (NV persistence test pod) | 5 min | <$0.02 |
| **Total** | **~60 min active** | **<$0.30** |

The Network Volume itself begins accruing storage cost the moment it is created (~$7/month per RunPod's $0.07/GB/month NV pricing). NV cost is captured under Stage 1+ persistent budget, not Block 2 burst budget.

## 10. Block 2 Output Artifacts

After Block 2 completion, the following artifacts exist:

| Artifact | Location |
|---|---|
| Account state record | Operator's notes / Session 2.3 chat record |
| `runpod_dry_run_verdict.json` | `/workspace/dry_run_verdict.json` on NV |
| Image digest | Recorded in `architecture-profile-seed.json` `runpod_dry_run.pod_image_digest` |
| HC-2 numerical drift report | Section in Session 2.3 closing summary |
| Block 2 cost record | RunPod Account → Billing |

These artifacts are inputs to Block 3 (persistent state architecture and reproducibility manifest finalization).

---

*End of Block 2 Execution Plan.*
