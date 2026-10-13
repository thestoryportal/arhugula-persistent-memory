# Session 2.2 — Summary Block

> **Workstream:** 1 — Empirical POC Scoping
> **Session:** 2.2 — Procurement Execution and Kaggle Smoke Test
> **Date completed:** 2026-04-26
> **Verdict:** Block 1 PASS; Block 2 authorized; Block 3 deferred to Session 2.3
> **Primary skill exercised:** `memit-specialist`
> **Secondary skill exercised:** `aiSecOps-specialist` (Warden — minimal use; deferred to Block 2 RunPod activation)

---

## 1. Decisions Made

### 1.1 Smoke test verdict — PASS

| Assertion | Measurement | Verdict |
|---|---|---|
| SF-1: post-edit top-1 == `baseball` | `' baseball'` (id=9283), P=0.9819 | PASS |
| SF-2: P(baseball) > P(basketball) post-edit | 0.9819 vs 0.000230, ratio 4270× | PASS |
| SF-3: post-unmount top-1 == `basketball` | `' basketball'` (id=9669), P=0.8702 | PASS |

Bit-identical pre-edit and post-unmount probabilities (P(basketball)=0.8701928853988647; P(baseball)=0.021447110921144485) empirically validate `.vindex` overlay isolation as mathematically perfect, not approximate.

### 1.2 Toolchain pinned configuration

| Component | Pinned value |
|---|---|
| MEMIT repository SHA | `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` |
| GPT-J 6B revision | `float16` |
| GPT-J 6B revision SHA | `b71ae8bc86cac13154e03e92b5855203086b722e` |
| PyTorch | 2.10.0+cu128 |
| transformers | 4.45.2 |
| accelerate | 0.34.2 |
| huggingface_hub | 0.25.2 |
| tokenizers | 0.20.3 |
| safetensors | 0.4.5 |
| datasets | 4.8.3 |
| CUDA | 12.8 |
| GPU (smoke test) | 2× Tesla T4 (Kaggle, via accelerate explicit device_map) |
| GPU (Stage 1 target) | RTX 4090 24 GB (RunPod Secure, per Session 2.1) |

### 1.3 Six patches authored and validated

| Patch ID | Target | Universality | Stage 1 status |
|---|---|---|---|
| P-1 | `util/nethook.py` retain_hook signature + inputs synthesis prologue | Universal (any transformers ≥ 4.36) | Required |
| P-2 | `util/nethook.py` register_forward_hook with_kwargs=True | Universal (any transformers ≥ 4.36) | Required |
| P-3' | `memit_main.py` torch.linalg.solve CPU FP64 offload | Conditional (cuda:0 capacity < 18 GiB) | Not required on RTX 4090 |
| Tokenizer pad_token alias | Cell 4 / model load | Universal (any GPT-2-derived tokenizer) | Required |
| Explicit device map | Cell 4 / model load | Conditional (multi-GPU only) | Not required on RTX 4090 |
| In-place `copy_()` unmount | Cell 8 / write engine | Universal (.vindex architecture requirement) | Required |

### 1.4 Verification cell discipline established

| Defect class | Symptom | Canonical pattern |
|---|---|---|
| Top-K string-search probability lookup | `P(target_true) = None` when target not in top-K | Direct token-id lookup against full softmax |
| `setattr` parameter replacement | Visible parameter state diverges from forward-pass behavior under accelerate hooks | `Tensor.copy_()` on existing Parameter's `.data` |
| Probability comparison without per-layer audit | Single-tensor verification masks multi-tensor partial corruption | Per-layer `allclose` with `all_match` aggregator |

---

## 2. Constraints Established

### 2.1 Stage 1 runbook constraints (carry to Session 2.3)

| ID | Constraint |
|---|---|
| OQ-S22-7 | Kaggle pip-installed packages persist across kernel restart; Factory Reset is required to revert |
| OQ-S22-8 | Distinguish "load-bearing pin" (e.g., `revision="float16"`) from "convenience pin" (era-matching versions); convenience pins are removed unless load-bearing |
| OQ-S22-9 | Kaggle's "Always use latest environment" default must be overridden for MEMIT smoke tests |
| OQ-S22-10 | RunPod activation must verify chosen PyTorch container ships transformers 4.x or supports the joint-pin pattern |
| OQ-S22-11 | `transformers==4.45.2` covers both GPT-J calibration baseline and LLaMA 3.1 8B production target |
| OQ-S22-12 | Kaggle Factory Reset preserves `/kaggle/working` and `/root/.cache/huggingface`; idempotent cleanup required for git clone and overlay save cells |
| OQ-S22-13 | Distinguish cache-friendly artifacts (HF model files) from version-pinned artifacts (git clones); cells must be idempotent accordingly |
| OQ-S22-14 | Cell 4 specification must set `tokenizer.pad_token = tokenizer.eos_token` immediately after `AutoTokenizer.from_pretrained` for GPT-2-derived tokenizers |
| OQ-S22-15 | LLaMA 3.1 8B has its own pad token; the Stage 1+ pad_token cell must check rather than blindly alias |
| OQ-S22-16 | MEMIT's `util/nethook.py` requires Patches P-1+P-2 for any `transformers ≥ 4.36`; manifest must record patch application |
| OQ-S22-17 | `kmeng01/memit` is unmaintained; framework POC should fork the repo and pin to a known-patched fork rather than upstream |
| OQ-S22-18 | LLaMA 3.1 8B uses `LlamaMLP` with the same kwargs-forwarding convention as GPT-J; Patches P-1+P-2 are prerequisites for Stage 1+ on LLaMA |
| OQ-S22-19 | Single 16 GiB GPU is insufficient for GPT-J 6B FP16 + MEMIT covariance ops; minimum viable single-GPU is ≥ 20 GiB |
| OQ-S22-20 | Runbook must specify two execution paths: (a) ≥ 24 GiB single-GPU direct `.to("cuda")`; (b) ≤ 16 GiB single-GPU pooled with second device via explicit device_map |
| OQ-S22-21 | LLaMA 3.1 8B FP16 (~16 GiB) on RunPod RTX 4090 (24 GiB) leaves ~8 GiB headroom; adequate for MEMIT covariance ops |
| OQ-S22-22 | `device_map="auto"` is unsuitable for MEMIT on multi-GPU; explicit device map required (Path B pattern) |
| OQ-S22-23 | Path B complexity is Kaggle-specific; Stage 1 RunPod runs on single GPU do not require explicit device mapping |
| OQ-S22-24 | MEMIT's `compute_z` directly accesses `lm_head.weight` and `lm_head.bias` as `lm_w` and `lm_b` and performs manual matmul; this creates a hard co-location requirement on multi-GPU configurations |
| OQ-S22-25 | RunPod RTX 4090 24 GB single-GPU configuration trivially satisfies the co-location requirement |
| OQ-S22-26 (superseded by S22-30) | MEMIT's `execute_memit` performs FP64 solve; for `d_ff = 16384` (GPT-J), peak transient is ~4 GiB; single-GPU configurations need ≥ 18 GiB |
| OQ-S22-27 | LLaMA 3.1 8B has `d_ff = 14336`; covariance matrix size is `14336² × 8 bytes ≈ 1.64 GiB` FP64; RTX 4090 has comfortable headroom |
| OQ-S22-28 | Patch P-3' applies conditionally based on GPU envelope; not required on RTX 4090 |
| OQ-S22-30 | MEMIT's `execute_memit` requires CPU offload of three operations on Kaggle 16 GiB envelope; Patch P-3' addresses all three |
| OQ-S22-31 | The CPU-offload pattern in P-3' is reusable for any FP64-on-FP32-base-model scenario |

### 2.2 Framework architecture constraints (carry to Workstream 3 implementation planning)

| ID | Constraint |
|---|---|
| OQ-S22-32 | Framework `.vindex` overlay write engine MUST use `Tensor.copy_()` semantics for both mount and unmount; `setattr`-replace is forbidden because it desynchronizes visible parameter state from forward-pass-used parameter state under accelerate hooks |
| OQ-S22-33 | Verification cells must query the full vocabulary distribution by token id, not search top-K decode list; top-K-only probability lookup returns `None` when target is below rank K |
| OQ-S22-34 | Smoke-test verdict schema must distinguish: (a) MEMIT-edit-correctness, (b) overlay-mount-correctness, (c) overlay-unmount-correctness; Cell 7/8/9 split corresponds to these three |
| OQ-S22-35 | Verification of unmount correctness MUST measure forward-pass behavior, not parameter state; `allclose` on parameter `.data` is necessary but not sufficient |

### 2.3 Patch authoring discipline (Claude self-improvement)

| ID | Constraint |
|---|---|
| OQ-S22-29 | Patch authoring must consider operator order of Python expressions, not just call sites; the FP64 promotion in Patch P-3 looked correctly scoped at the spec level but executed at the wrong AST level. Future patches involving memory-intensive operations must trace the order of materialization, not just the order of calls |

---

## 3. Open Questions Deferred

### 3.1 Resolved during smoke test

| ID | Resolution |
|---|---|
| OQ-WS1-1 (Stage 0 GPU procurement) | Resolved Session 2.1; Block 1 confirmation completed this session |
| OQ-S22-3 (covariance cache reachability) | Resolved; `memit.baulab.info/data/stats/...` reachable and serving 6 layer files at ~1 GB each |
| OQ-S22-4 (RunPod RTX 4090 PyTorch image sm capability) | Deferred to Block 2 dry-run |
| OQ-S22-5 (sm capability check for future free-tier venues) | Deferred to runbook authorship |
| OQ-S22-6 (transformers version band) | Resolved by joint 4.x-line pin |

### 3.2 Deferred to Block 2 (RunPod activation)

| Concern | Block 2 step that resolves |
|---|---|
| RunPod PyTorch container image digest | Step 8.3 (image catalog selection) |
| RunPod Network Volume region pinning | Step 8.2 (NV provisioning) |
| RunPod single-GPU MEMIT reproduction | Step 8.4 (dry-run pod) |
| Kaggle vs RunPod numerical drift | Step 8.4 (HC-2 comparison) |

### 3.3 Deferred to Stage 1 SECT execution

| Concern | Stage 1 protocol step |
|---|---|
| Issue #15 (24 GB OOM at scale) | Stage 2 sweep planning, not Stage 1 |
| LLaMA 3.1 8B extension to MEMIT codebase | Workstream 1 future task; framework's POC must fork MEMIT |
| Production target pre-flight (PF-1 through PF-6 against LLaMA) | Stage 1 protocol execution |
| 3-fact × 3-run SECT statistical aggregate | Stage 1 protocol execution |

---

## 4. Interface Contracts Defined

### 4.1 Reproducibility manifest seed (output of this session, input to Session 2.3+)

| Field | Type | Source |
|---|---|---|
| `manifest_version` | string | Schema version |
| `kaggle_smoke_test.verdict` | "PASS" | Section 1.1 |
| `kaggle_smoke_test.completed_at` | ISO 8601 timestamp | 2026-04-26T07:08:30.578814+00:00 |
| `kaggle_smoke_test.pinned_versions.*` | object | Section 1.2 |
| `kaggle_smoke_test.patches_applied.*` | object (6 booleans) | Section 1.3 |
| `kaggle_smoke_test.assertions.*` | object (3 booleans, all true) | Section 1.1 |
| `kaggle_smoke_test.probabilities.*` | object (6 floats) | See full JSON in `architecture-profile-seed.json` |
| `kaggle_smoke_test.overlay.*` | object (parameter_count, size_mb) | 6 tensors, 805.31 MB |
| `runpod_dry_run` | object | Populated in Block 2 dry-run |
| `persistent_state.network_volume_*` | object | Populated in Block 2 NV provisioning |
| `rsync_target.*` | object | Populated in Block 3 |

### 4.2 Patch contract for Stage 1+ runbook

| Patch | Application order | Reload requirement |
|---|---|---|
| P-1 + P-2 (nethook) | Before any `MEMITHyperParams.from_json` import | sys.modules purge of `util.*`, `rome.*`, `memit.*` |
| P-3' (memit_main solve) | Before `apply_memit_to_model` call | sys.modules purge of `memit.*`, `rome.*` |
| pad_token alias | After `AutoTokenizer.from_pretrained` | None |
| Explicit device map | At `from_pretrained` invocation (not retrofittable) | Kernel restart |
| `copy_()` unmount | At write-engine unmount step | None |

### 4.3 Block 2 entry contract

| Precondition | Status |
|---|---|
| Smoke test verdict = PASS | Met |
| Reproducibility manifest captured | Met (see `architecture-profile-seed.json`) |
| Kaggle account state confirmed | Met (operator confirmed phone-verified, GPU quota available) |
| Patches documented for RunPod replication | Met (Patches P-1, P-2, pad_token alias, copy_() unmount required; P-3', explicit device map not required on single-GPU RTX 4090) |
| Operator proceed signal | Met (this session closes with operator confirm) |

---

## 5. Next Session Candidates

| Session ID | Workstream | Primary skill | Scope |
|---|---|---|---|
| **2.3** (recommended next) | WS1 | `memit-specialist` (primary) + `aiSecOps-specialist` (secondary) | Block 2 — RunPod activation, account creation, NV provisioning, dry-run pod with single-fact MEMIT reproduction; Block 3 — persistent state architecture, rsync configuration, finalized reproducibility manifest |
| 2.4 (after 2.3) | WS1 | `validation-contract-architect` | CFB v1 corpus authorship sprint and probe-set v1 authorship — separate Stage 0 sub-sessions per Session 2.2 entry note |
| 2.5 (after 2.4) | WS1 | `memit-specialist` | Stage 1 SECT execution (3 facts × 3 runs against LLaMA 3.1 8B) — full MEMIT-COMPAT-PROTO-1 protocol |
| GAP-4 cluster | WS2 | `orchestration-comparativist` | Operator path selection (Pi / n8n / Claude harness / OpenClaw / LangGraph) — currently blocked |

---

## 6. Halt-Class Trajectory — Summary

17 attempts, 12 distinct halts, 6 surgical patches, 0 architectural changes.

| Halt class | Count | Resolution |
|---|---|---|
| Hardware/PyTorch capability | 1 | Path A (P100 → T4) |
| Package version drift | 3 | Joint 4.x-line pin |
| Filesystem persistence | 1 | rmtree before clone |
| Spec defects (Claude authoring) | 3 | Resolved (pad_token, kwargs hook, P-3 → P-3') |
| MEMIT-internal toolchain | 1 | Patches P-1, P-2 |
| Memory envelope — single GPU | 1 | Path B explicit device map |
| Memory envelope — FP64 promotion | 2 | Patch P-3' (CPU offload) |
| Verification cell defects | 2 | Cell 7 v2 (full-vocab), Cell 8 v3 (copy_) |

The MEMIT codebase itself surfaced one regression (Issue #16, kwargs hooks); all other halts were integration-layer mismatches. The smoke-test discipline surfaced every constraint before paid infrastructure activation, exactly as Session 2.1 designed.

---

## 7. Carry-Forward Inputs to Session 2.3

| Document | Status |
|---|---|
| `session-2_2-summary-block.md` (this file) | Authoritative session record |
| `architecture-profile-seed.json` | Reproducibility manifest seed; appended in Block 2 dry-run |
| `memit-patches-canonical.md` | Six patches with exact text, application order, and reload procedure |
| `kaggle-canonical-notebook.md` | The 13-cell notebook that produced the PASS verdict; reference artifact |
| `block-2-execution-plan.md` | Block 2 (RunPod activation) operator runbook |
| `block-2-session-prompt.md` | Session prompt for Block 2 (paste at start of next session) |
| `session-2_2-runbook-deltas.md` | Constraints and deltas to existing runbooks (Stage 1+ implications) |

---

*End of Session 2.2 Summary Block.*
