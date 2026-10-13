# Session 2.2 Runbook Deltas

> **Purpose:** Constraints from Session 2.2 smoke test that must be reflected in Stage 1+ runbooks, the framework's `.vindex` write engine specification, and POC documentation.
> **Status:** Authoritative; carry forward to Workstream 1 future sessions and Workstream 3 implementation planning.

This document consolidates the 35 open questions surfaced during Session 2.2 (OQ-S22-1 through OQ-S22-35) into actionable runbook deltas, organized by target document.

---

## 1. Deltas to MEMIT-COMPAT-PROTO-1 Specification

### 1.1 PF-6 (architecture_profile.json) schema additions

The `architecture_profile.json` schema (PF-6 of MEMIT-COMPAT-PROTO-1) must include the following fields, populated at Stage 0 conclusion:

| Field | Type | Source |
|---|---|---|
| `pinned_versions.transformers` | string | Cell 2 capture |
| `pinned_versions.accelerate` | string | Cell 2 capture |
| `pinned_versions.huggingface_hub` | string | Cell 2 capture |
| `pinned_versions.tokenizers` | string | Cell 2 capture |
| `pinned_versions.safetensors` | string | Cell 2 capture |
| `pinned_versions.memit_repo_sha` | string (40-char SHA) | Cell 3 capture |
| `pinned_versions.gpt_j_revision` | string ("float16") | Cell 4 capture |
| `pinned_versions.gpt_j_revision_sha` | string (40-char SHA) | Cell 4 capture |
| `patches_applied.*` | object (booleans for 6 patches) | Cell 5e, Cell 5f, Cell 5b, Cell 4, Cell 8 |
| `patches_required_but_not_applied` | array (must be empty for PASS) | Computed |
| `gpu_topology` | string | Cell 4 capture |
| `cuda_capability` | string ("sm_NN") | Cell 1 capture |
| `tf_factory_warnings_observed` | string (benign annotation) | Cell 5 stdout |
| `transformers_attn_bias_warning` | string (benign annotation) | Cell 4 stdout |

### 1.2 PF-1 (target layer range) — corrected default

| Variable | Original PROTO-1 default | Corrected default |
|---|---|---|
| GPT-J 6B edit layer range | "single layer 17 of 28" | `[3, 4, 5, 6, 7, 8]` per MEMIT canonical hparams |

The single-layer variant referenced in the Session 2.1/2.2 protocol drafts was incorrect (it conflated GPT-J convention with GPT2-XL convention). MEMIT distributes the update across 6 layers; this is structural to the algorithm, not a tuning parameter.

### 1.3 SECT step 6 (overlay isolation check) — verification expansion

SECT step 6 currently specifies "post-unmount, pre-edit response returns." This is necessary but insufficient. Expand to require:

| Verification | Method |
|---|---|
| Per-layer parameter `allclose` to `orig_weights` | Loop over `orig_weights` keys; `torch.allclose` with default tolerance |
| Forward-pass top-1 match to pre-edit | Same prompt; `torch.topk` of logits |
| Per-layer norm match to pre-edit captured norms | Float comparison with FP16 tolerance |

Per OQ-S22-35: parameter-state verification alone is necessary but not sufficient. Forward-pass behavior must also be verified.

### 1.4 SECT pass criterion — single-fact reframing

| Criterion (original) | Criterion (revised) |
|---|---|
| "Edit-success metric within ±5% of published CounterFact reference" | Three-assertion conjunction: SF-1 (top-1 match), SF-2 (full-vocab probability comparison), SF-3 (overlay isolation) |

Per OQ-S22-33: top-K-only probability lookup returns `None` when target is below rank K. Full-vocabulary probability lookup by token ID is mandatory.

### 1.5 New PROTO-1 section: Patch Application Procedure

Add new section to MEMIT-COMPAT-PROTO-1 specification:

> **Patch Application Procedure (mandatory before SECT execution)**
>
> The following six patches must be applied in order, with `sys.modules` purge between each, before the first `apply_memit_to_model` call:
>
> 1. P-1 + P-2 (`util/nethook.py`): hook signature + with_kwargs registration
> 2. Pad-Token alias on tokenizer
> 3. P-3' (`memit/memit_main.py`): CPU FP64 solve — apply only if cuda:0 capacity < 18 GiB
> 4. Explicit device map at `from_pretrained` — apply only if multi-GPU configuration
> 5. Copy-Unmount pattern in write engine — universal for all configurations
>
> See `memit-patches-canonical.md` for exact patch text and verification procedures.

---

## 2. Deltas to Stage 1 Runbook (to be authored in Session 2.5)

### 2.1 Pre-flight checklist additions

| Check | Required state |
|---|---|
| MEMIT repo cloned at SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` | Yes |
| Joint version pin installed (transformers 4.45.2, etc.) | Yes |
| Patches P-1, P-2 applied to `util/nethook.py` | Yes |
| Patch P-3' applied if cuda:0 < 18 GiB | Conditional |
| Tokenizer `pad_token` aliased to `eos_token` | Yes |
| Model loaded with `revision="float16"` for GPT-J | Yes |
| Explicit device map applied if multi-GPU | Conditional |

### 2.2 Stage 1 GPT-J 6B vs LLaMA 3.1 8B differences

| Concern | GPT-J 6B (Stage 0 calibration) | LLaMA 3.1 8B (Stage 1 production) |
|---|---|---|
| `d_ff` | 16384 | 14336 |
| Covariance matrix size FP32 | 1.07 GiB | 0.82 GiB |
| Covariance matrix size FP64 | 2.15 GiB | 1.64 GiB |
| Patch P-3' required on RTX 4090 (24 GiB) | No | No |
| MEMIT layer range | `[3, 4, 5, 6, 7, 8]` | TBD (Stage 1 PF-1 produces this) |
| Pad-Token alias | Yes (GPT-2 tokenizer) | Conditional (LLaMA has its own pad token) |
| `compute_z` `lm_head` direct access | Yes | Yes (same architecture pattern) |
| Patches P-1, P-2 required | Yes | Yes (same kwargs forwarding) |
| Copy-Unmount required | Yes | Yes |

Per OQ-S22-15: Stage 1 cell 5b for LLaMA must be `if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token` (conditional check, not unconditional alias).

Per OQ-S22-17: `kmeng01/memit` is unmaintained. Stage 1+ must fork the repo and pin to the framework's own fork, with patches P-1, P-2, P-3' applied at fork creation time. Submitting upstream is not viable.

Per OQ-S22-18: LLaMA 3.1 8B uses `LlamaMLP` with the same kwargs-forwarding convention; Patches P-1+P-2 are prerequisites for LLaMA work.

### 2.3 Probe-set v1 authorship (Stage 0 sub-session)

When `validation-contract-architect` authors probe-set v1 (separate session), include verification cells matching the Cell 7 / Cell 8 / Cell 9 split:

| Probe class | Verification pattern |
|---|---|
| L1 storage probe | Token-id-based full-vocabulary probability lookup (not top-K search) |
| Locality probe | Same pattern; multiple unrelated subjects |
| Overlay isolation probe | Forward-pass top-1 + per-layer parameter `allclose` |

---

## 3. Deltas to Framework `.vindex` Write Engine Specification

### 3.1 Universal write engine constraints (Workstream 3 implementation planning)

The framework's write engine MUST satisfy:

| Constraint | Source | Rationale |
|---|---|---|
| Use `Tensor.copy_()` for both mount and unmount | OQ-S22-32 | `setattr` desynchronizes visible parameter state from forward-pass-used parameter state under accelerate hooks |
| Verify mount/unmount via per-layer `allclose` | OQ-S22-35 | Parameter-state verification is necessary |
| Verify mount/unmount via forward-pass behavior | OQ-S22-35 | Parameter-state verification is not sufficient |
| Distinguish edit-correctness from overlay-correctness in verdict schema | OQ-S22-34 | Three independent failure modes |
| Record patches applied + patches required-but-not-applied | OQ-S22-16 | Reproducibility manifest must support both successful and failed states |

### 3.2 `.vindex` overlay format implications

The `.vindex` overlay format must be tied to the `transformers` model class structure that produced it. Specifically:

| Concern | Implication |
|---|---|
| Parameter names referenced by full module path | Overlay format must store paths, not indices |
| Parameter dtype must match target model's dtype | Overlay storage must record dtype per tensor |
| Parameter device assignment depends on device_map | Overlay must be device-agnostic (stored on CPU); restoration applies target's current device |
| Accelerate hook references | Overlay restoration MUST use `copy_()`, never `setattr` |

### 3.3 Verdict schema split

Per OQ-S22-34, the framework's verdict schema must distinguish three correctness layers:

```
verdict_schema = {
    "edit_correctness": {                    # Did weights change as intended?
        "all_target_tensors_modified": bool,
        "no_nan_or_inf": bool,
        "update_norms_within_band": bool,
    },
    "mount_correctness": {                   # Does forward pass use edited weights?
        "post_edit_top1_matches_target_new": bool,
        "post_edit_p_target_new_gt_p_target_true": bool,
    },
    "unmount_correctness": {                 # Does forward pass return to pre-edit?
        "post_unmount_top1_matches_target_true": bool,
        "post_unmount_probabilities_bit_identical_to_pre_edit": bool,
        "per_layer_parameter_allclose_to_orig": bool,
    },
}
```

A PASS verdict requires all three layers to PASS. A FAIL on any layer indicates a different remediation path.

---

## 4. Deltas to POC Execution Plan

### 4.1 Block 2 RunPod activation pre-flight

Per `block-2-execution-plan.md`, Block 2 dry-run pod must verify:

| Item | Source delta |
|---|---|
| `register_forward_hook(..., with_kwargs=True)` is supported | OQ-S22-10; PyTorch ≥ 2.0 prerequisite |
| GPU compute capability sm_70+ | OQ-S22-5; sm_60 (P100) was rejected |
| Container image pinned by digest, not tag | OQ-S22-10 |
| `transformers==4.45.2` installable on the pinned image | OQ-S22-10 |

### 4.2 Stage 2 sweep planning carry-forward

Per OQ-S22-1: Issue #15 (24 GB OOM at scale during MEMIT) is a known signal from kmeng01/memit#15 (Feb 2024). This is not relevant for Stage 1 (single-fact regression on RTX 4090 has comfortable headroom) but must be revisited at Stage 2 sweep planning when batch sizes exceed single-fact:

| Stage 2 sweep batch size | Risk on RTX 4090 24 GiB |
|---|---|
| 1 fact (Stage 1 SECT) | None — validated by Block 1 PASS |
| 10 facts | Low — covariance fetch is per-layer, not per-fact |
| 100 facts | Low — same reasoning |
| 1000 facts | Medium — `layer_ks` matrix grows to `d_ff × n_facts`; for 1000 facts on GPT-J `d_ff=16384`, that's ~63 MiB FP32, manageable |
| 10000 facts (MEMIT paper baseline) | Medium-high — Issue #15 reporter encountered OOM at this scale on A5500 24 GiB |

Stage 2 protocol authoring (Workstream 1 future) must include a sweep-budget plan that accounts for the Issue #15 signal.

### 4.3 Cost discipline

Per Session 2.2 history, the smoke-test discipline produced 17 attempts and 12 distinct halts on Kaggle's free tier. Total Block 1 cost: $0 (free tier). Equivalent halts on RunPod RTX 4090 at $0.69/hr would have cost approximately:

| Phase | Pod-hours consumed (estimated) | Cost at $0.69/hr |
|---|---|---|
| Each sm_60-class environment surprise (1 halt) | 0.1 hr | $0.07 |
| Each pip dependency drift halt (3 halts) | 0.2 hr × 3 | $0.41 |
| Each clone collision (1 halt) | 0.1 hr | $0.07 |
| Each spec defect halt (3 halts) | 0.2 hr × 3 | $0.41 |
| MEMIT-internal toolchain (1 halt) | 0.5 hr | $0.35 |
| Memory envelope halts (3 halts on RTX 4090 — would not occur due to 24 GiB headroom) | N/A | N/A |
| Verification cell halts (2 halts) | 0.3 hr × 2 | $0.41 |
| **Total avoided** | **~3 hr** | **~$2.07** |

The smoke-test discipline saved approximately $2 in halts that would have otherwise consumed paid RunPod time. The structural value is greater: each halt produced a manifest field, runbook delta, or framework constraint that would otherwise have surfaced during Stage 1 (where the cost per halt is amplified by SECT batch size and the operator's investment in protocol execution).

### 4.4 Patch ownership in Stage 1+ runbooks

Stage 1+ runbooks must distinguish patch ownership:

| Patch | Owned by | Maintained by |
|---|---|---|
| P-1 + P-2 (nethook) | Framework's MEMIT fork | Workstream 1 |
| P-3' (memit_main solve) | Framework's MEMIT fork | Workstream 1 |
| Pad-Token alias | Per-environment tokenizer setup | Stage 1+ runbook |
| Explicit device map | Per-environment model loader | Stage 1+ runbook |
| Copy-Unmount | Framework write engine | Workstream 3 implementation |

The first three (P-1, P-2, P-3') are upstreamable to the framework's MEMIT fork once it exists. The latter two are environmental adapters that runbooks consume.

---

## 5. Deltas to Framework Specification (v1.2 Carry-Forward)

### 5.1 New tension entries (for tension map v6)

Two cross-domain tensions surfaced during Session 2.2 that the v1.2 tension map does not capture:

#### Tension T-Hooks-vs-Multi-Device

Between: `memit-specialist` (write engine) and orchestration concerns (device placement under accelerate).

Description: MEMIT's `compute_z` directly accesses `lm_head.weight` and `lm_head.bias` and performs manual matmul, bypassing accelerate's cross-device hooks. This creates a hard co-location requirement that orchestration plans must respect.

Resolution: explicit device map for multi-GPU configurations; single-GPU configurations sidestep the issue.

#### Tension T-Visible-vs-Computational-State

Between: `validation-contract-architect` (verification cells) and `state-consistency-theorist` (parametric memory layer state).

Description: `accelerate`'s hook system caches parameter references at hook-installation time. `setattr`-replacement of `nn.Parameter` desynchronizes the visible parameter state (what `getattr` returns) from the forward-pass-used parameter state (what hooks resolve). Verification of unmount correctness must measure forward-pass behavior, not parameter state alone.

Resolution: `copy_()` semantics for all overlay mount/unmount operations; per-layer `allclose` AND forward-pass top-1 verification both required.

### 5.2 New gap backlog entries (for gap backlog v6)

#### GAP-S22-A: MEMIT codebase fork strategy

Status: Open. Owner: Workstream 1.

Description: `kmeng01/memit` is unmaintained (last commit 2022-11-14; 16 open issues; no triage). Patches P-1, P-2, P-3' are required for any 2026-vintage execution. The framework's POC must fork the repository and apply patches at fork creation. The fork's branch policy, license preservation, and upstream-tracking strategy require resolution.

#### GAP-S22-B: LLaMA 3.1 8B MEMIT extension

Status: Open. Owner: Workstream 1.

Description: `kmeng01/memit` has no native LLaMA support (Issue #17 confirms). Stage 1+ requires extending the codebase (or its framework fork) to support LLaMA's `LlamaForCausalLM` and `LlamaMLP` modules. The extension scope, validation procedure, and parity with the GPT-J calibration baseline require dedicated session work.

#### GAP-S22-C: `.vindex` overlay format and write engine architecture

Status: Open. Owner: Workstream 3 implementation planning.

Description: The framework's write engine specification must include the `Tensor.copy_()` semantics, the per-layer `allclose` verification, the forward-pass behavior verification, and the three-layer verdict schema split (edit/mount/unmount correctness). Implementation skeletons can begin in Workstream 3 sessions per IC-WS1-1.

---

## 6. Summary of Carry-Forward Items

| Carry-forward type | Count | Target documents |
|---|---|---|
| MEMIT-COMPAT-PROTO-1 deltas | 5 sections | Updated PROTO-1 spec; Stage 1 runbook |
| Stage 1 runbook constraints | 19 | Stage 1 runbook (authored Session 2.5) |
| Framework `.vindex` write engine constraints | 3 | Workstream 3 implementation spec |
| POC execution plan deltas | 4 | poc-execution-plan-and-spec-revision-rule.md updates |
| Tension map entries | 2 | tension-map-v6.md (when authored) |
| Gap backlog entries | 3 | gap-backlog-v6.md (when authored) |

---

*End of Session 2.2 Runbook Deltas.*
