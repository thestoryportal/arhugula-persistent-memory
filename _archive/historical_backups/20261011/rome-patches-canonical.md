# ROME Patches Canonical

> **Document version:** v0.1 (first synthesis)
> **Authoring session:** S2.17 Block 2
> **Authoring date:** 2026-05-04
> **Status:** RATIFIED v0.1 — declarative starting point; empirical patch-applicability verdicts at S2.18 Block A Cell 2 first execution
> **Companion artifact:** `t2_rome_runbook_v0_1.md` (S2.17 Block 2 deliverable; consumes this doc at Cell 1 / Cell 2)
> **Specialist provenance:** memit-specialist (primary; ROME patch surface inventory + MEMIT-patch applicability re-derivation); state-consistency-theorist (Copy-Unmount carry-forward verdict); framework-spec-writer (formalization)
> **Workstream:** WS1 (empirical execution; T-branch entry — T.2 ROME)

---

## §0 Purpose & non-amendment declaration

This document is the **parallel canonical patches reference for the ROME write engine** under the T.2 ROME work begun at S2.17. It is structurally analogous to `memit-patches-canonical.md` v2.5 (the MEMIT patches canonical) but **does not amend it**. The MEMIT canonical is preserved unmodified at v2.5 per D-S216-CLOSE-3; this ROME canonical is a sibling artifact for a sibling write engine.

**Document scope.** This canonical declares:

1. The **patch inventory** for the ROME write engine on `meta-llama/Llama-3.1-8B`, partitioned by:
   - Patches inherited from MEMIT (applicable directly, applicable with modification, inapplicable)
   - Patches authored fresh for ROME (none expected at v0.1; placeholder section reserved)
2. The **SHA pin** for the ROME repository under which patches are valid
3. The **process constraints** governing the ROME patch surface, paralleling C-S26-1/2/3 and C-S28-1 from MEMIT canonical
4. The **applicability verdict matrix** mapping each MEMIT patch (P-1, P-2, P-3', P-4, P-5, P-6, P-7, Pad-Token, Copy-Unmount, Device-Map) to its ROME status

**Mechanical rationale for re-derivation.** ROME is the predecessor codebase of MEMIT at the GitHub level. The two share substantial source heritage — `util/nethook.py` is shared; `rome/layer_stats.py` is shared (single file, identical name and approximate purpose); `rome/compute_v.py` is shared. Patches that target shared files are **expected applicable** to ROME directly. Patches that target MEMIT-specific files (`memit/memit_main.py`, `memit/compute_z.py`) are **expected inapplicable** by structural absence — ROME has its own dispatch entrypoint (`rome/rome_main.py`'s `apply_rome_to_model` or equivalent) which differs in mechanism (single fact at a single layer; no batched multi-fact projection).

**v0.1 status disclaimer.** All applicability verdicts in this document are **declared** — they are best-judgment predictions based on shared-codebase heritage and the public ROME paper / repository structure. **Empirical verdicts** are produced at S2.18 Block A Cell 2 first execution against pinned-SHA NV-resident `/workspace/rome_dry_run/rome/`. v0.2 will absorb empirical findings.

---

## §1 Patch inventory (declared)

### §1.1 Patches inherited from MEMIT — APPLICABLE DIRECTLY

These patches target files shared between ROME and MEMIT. Application is expected to succeed without modification at the same source markers.

| ID | Target file | Marker | MEMIT canonical reference | ROME applicability |
|---|---|---|---|---|
| **P-1** | `util/nethook.py` | `def retain_hook(m, args, kwargs, output):` | `memit-patches-canonical.md` v2.5 §3.1 | **APPLICABLE DIRECTLY** — `util/nethook.py` is shared at SHA pin level; hook signature change is upstream-of-everything |
| **P-2** | `util/nethook.py` | `with_kwargs=True` | `memit-patches-canonical.md` v2.5 §3.2 | **APPLICABLE DIRECTLY** — companion to P-1; same shared file |
| **P-4** | `rome/compute_v.py` (`hidden_size`); `rome/layer_stats.py` (`max_position_embeddings` ×2) | `hidden_size` substring + `max_position_embeddings` count ≥ 2 | `memit-patches-canonical.md` v2.5 §3.5 | **APPLICABLE DIRECTLY** — both target files are in `rome/` namespace; shared with MEMIT. ROME's `compute_v.py` is the same file as MEMIT's `compute_v.py` (path: `rome/compute_v.py` — note the directory name is `rome/` even within the MEMIT repo, reflecting the codebase's shared ancestry). The MEMIT-specific `memit/compute_z.py` P-4 site is INAPPLICABLE (no analogous `compute_z.py` in ROME — ROME computes target z directly within `rome_main.py`'s edit dispatch) |
| **P-5** | `rome/layer_stats.py` (Wikipedia dataset loader modernization) | `"20231101.en"` + `"wikimedia/wikipedia"` | `memit-patches-canonical.md` v2.5 §3.6 | **APPLICABLE DIRECTLY** — `rome/layer_stats.py` is the shared file; ROME consumes the same Wikipedia covariance cache pipeline as MEMIT (this is why covariance cache reuse is viable per D-S216-CLOSE-2) |
| **Pad-Token** | model-load-time tokenizer alias | `tokenizer.pad_token = tokenizer.eos_token` | `memit-patches-canonical.md` v2.5 §4 | **APPLICABLE DIRECTLY** — Llama-3.1-8B tokenizer carries no pad_token by default; the alias is target-model-specific, not write-engine-specific. Applied at Cell 5 model load (same surface as MEMIT runbook) |

### §1.2 Patches inherited from MEMIT — APPLICABLE WITH MODIFICATION

These patches target functionality conceptually shared but implemented differently in ROME.

| ID | MEMIT site | ROME site | MEMIT canonical reference | Modification type |
|---|---|---|---|---|
| **Copy-Unmount** | Cell 9 trial fn body — `original_layer_state[L] = model.state_dict()[layer].clone()`; in-place tensor restore via `model.state_dict()[layer].copy_(original_layer_state[L])` | Block C Cell 15 trial fn body — same mechanism, applied to ROME's single edited layer (not 5 layers as in MEMIT). Restore is per-fact, not per-trial-replicate-group | `memit-patches-canonical.md` v2.5 §6 | **APPLICABLE WITH MECHANISM-PRESERVED, TARGET-NARROWED** — bit-exact restore mechanism is preserved (validated at S2.14-D D.3 joint-overlay regime + S2.15-D2 narrowed-window regime; both sessions confirmed `allclose_match=True` on per-layer restore + `drift=0.00e+00` on per-fact unmount). Carry-forward to ROME is structurally sound: ROME edits a single layer at a time, so the joint-overlay regime is *narrower* than MEMIT's — a strict subset of the validated empirical anchor. The mechanism does not depend on the write engine; it depends on the in-place tensor restore semantics of `state_dict().copy_()`, which is a PyTorch primitive shared across both engines |

### §1.3 Patches inherited from MEMIT — INAPPLICABLE

These patches address concerns that do not arise in ROME's dispatch surface.

| ID | MEMIT concern | ROME status | Rationale |
|---|---|---|---|
| **P-3'** | CPU offload for the linear-system solve in MEMIT's batched multi-fact projection (RTX 4090 FP64 envelope on 24 GiB) | **INAPPLICABLE** | ROME's mechanism is single-fact, single-layer rank-1 update via key-value vector arithmetic in `rome_main.py`. There is no batched linear-system solve; the FP64 VRAM-pressure regime that motivated P-3' (and was retired at S2.7 per the canonical hparams gate) does not arise. ROME's edit memory cost is dominated by the covariance matrix C₁ load (~822 MB FP32 per layer; same as MEMIT's per-layer working set), which fits comfortably within RTX 4090 24 GiB |
| **Device-Map** | conditional companion to P-3' for explicit CPU/GPU partitioning | **INAPPLICABLE** | Companion to P-3'; same rationale |
| **P-6** | `rome/layer_stats.py:40` f-string prefix correction for `size_suffix` construction (post-P-7 cache-filename signature `_t{batch_tokens}_`) | **INAPPLICABLE** to ROME's edit-time path | P-6 modifies the cache *naming* convention to thread `batch_tokens` through to the on-disk filename. **However:** ROME consumes the same NV-resident covariance caches as MEMIT (per D-S216-CLOSE-2; covariance caches L2-L8, 5.75 GB on NV, durable). The cache *files* on NV were produced under post-P-6 layer_stats.py at the pre-S2.6 fork-work session. ROME's read path resolves the same `_t100_` filename pattern — so P-6's *output form* is consumed by ROME but P-6 itself does not need re-application to the ROME source because the same `rome/layer_stats.py` file is shared. **Effective status: TRANSITIVELY APPLIED** via shared `rome/layer_stats.py` post-P-6 source. Cell 2 verification of post-P-6 marker form is **REQUIRED** in the ROME runbook to confirm the shared file carries the post-P-6 form — see §1.4 below for the verification-only carry-forward |
| **P-7** | `memit/memit_main.py` get_cov body batch_tokens propagation — closes C-S26-2 by-construction | **INAPPLICABLE** | P-7 targets a MEMIT-specific file (`memit/memit_main.py`) that has no ROME analogue. ROME's dispatch path through `rome_main.py` does not call `get_cov` with the same batched-projection requirement. ROME single-fact dispatch loads the cached `rome/layer_stats.py` covariance matrix once via `get_cov` at edit time; the propagation mechanism that P-7 closes is not invoked. **However:** ROME *does* call `get_cov` during edit dispatch — verifying that this call resolves to the cached `_t100_` form (rather than triggering an unintended local recomputation) is the ROME-equivalent of MEMIT's R1.3 cache-dispatch smoke test, which is preserved at Block A Cell 8 of the ROME runbook (R1.3-equivalent dry-run gate per D-S216-CLOSE-3 implication) |

### §1.4 Patches not present in MEMIT canonical — applicable to ROME — RESERVED

This section is reserved for ROME-specific patches that are not declared in MEMIT canonical. **At v0.1: empty — no ROME-specific patches identified.**

The S2.18 Block A Cell 2 first-execution may surface ROME-specific defects requiring patches; if so, they are added at v0.2 with empirical anchor referenced.

### §1.5 Verification-only carry-forward (no patch application; verification gate only)

| Item | Verification gate | Cell | Rationale |
|---|---|---|---|
| **Post-P-6 source form on `rome/layer_stats.py`** | `assert 'size_suffix = f"_t{batch_tokens}" + size_suffix' in layer_stats_src` | t2_rome_runbook_v0_1.md Block A Cell 2 | The shared `rome/layer_stats.py` should carry the post-P-6 form transitively (same NV-resident `/workspace/rome_dry_run/rome/` if cloned from the same SHA neighborhood as `/workspace/memit_dry_run/memit/`). Cell 2 verifies, does not re-apply |
| **Post-P-7 source form on `rome_main.py`** | DEFERRED — P-7 target is `memit/memit_main.py`, not `rome_main.py`. ROME's dispatch surface does not require P-7-equivalent verification. NOT a Cell 2 check item | n/a | Per §1.3 P-7 inapplicability rationale |

---

## §2 ROME repository SHA pin

**Repository:** `https://github.com/kmeng01/rome`
**SHA pin:** `LATEST_STABLE_TIP_AT_S2_17_AUTHORING` (placeholder; resolved at runbook v0.1 Cell 1 first execution)

> **D-S217-Q2-1 ratification (S2.17 Block 2):** ROME SHA pin = latest stable tip. Operator-side repo inspection at S2.17 Block 2 / S2.18 Block A Cell 1 first execution is authoritative for resolving the placeholder to a concrete SHA. The runbook Cell 1 captures the resolved SHA into `t2_rome_environment_fingerprint.json` for reproducibility manifest discipline. Empirical anchor: same approach as MEMIT SHA pin discipline (`80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` was resolved similarly at the pre-S2.6 fork-work session).

**Operator override semantics.** If repo inspection at S2.18 Block A surfaces a regression at the latest stable tip (e.g., a recent commit that breaks `apply_rome_to_model` invocation API), the operator may pin to a specific commit at runbook execution time. This authoring plan does not pre-commit a specific SHA because:

1. ROME has been static for years (the publicly-tracked repository has had minimal churn since the original 2022 paper publication)
2. The MEMIT-as-fork relationship is incidental — ROME is the predecessor, not a sibling — and `kmeng01/rome` is the canonical reference implementation
3. SHA-pin discipline is for reproducibility, not version-tracking, and a "latest stable tip" pin captured at execution time is sufficient

**Cross-reference.** `t2_rome_runbook_v0_1.md` Block A Cell 1 (SHA capture); §2 of this doc (resolution semantics).

---

## §3 ROME canonical hparams (declared starting values)

> **D-S217-Q3-1 ratification (S2.17 Block 2):** ROME canonical hparams at runbook v0.1 = ROME paper Table 1 GPT-J reference values (declared starting point); full calibration to Llama-3.1-8B at S2.18 Block B Cell 13 trial 0.

### §3.1 ROME paper Table 1 reference values (GPT-J)

The ROME paper (Meng et al., 2022, "Locating and Editing Factual Associations in GPT") publishes canonical hparams for GPT-J 6B in the public `https://rome.baulab.info` reference page and the appendix of the paper. The starting values declared here are the published GPT-J values, transferred without modification to Llama-3.1-8B as the v0.1 baseline.

| Hparam | GPT-J Table 1 value | Notes |
|---|---|---|
| `v_lr` | `0.5` | gradient step size for `target_v` optimization |
| `v_num_grad_steps` | `20` | optimization iterations for `target_v` |
| `v_loss_layer` | `27` (GPT-J) | layer at which the cross-entropy loss is computed for v-optimization. **Llama-3.1-8B has 32 layers; v_loss_layer needs operator-side calibration at Block B Cell 13** — placeholder `31` (last layer) at runbook v0.1 |
| `v_weight_decay` | `0.5` (paper appendix) | regularization on `target_v` magnitude |
| `clamp_norm_factor` | `4` | clip on `target_v` norm relative to base model embedding norm |
| `kl_factor` | `0.0625` | KL regularization weight in v-optimization loss |
| `mom2_adjustment` | `15000` | C₁ ⁻¹ scaling factor (analogous to MEMIT's `mom2_update_weight`) |
| `context_template_length_params` | `[(5, 10), (10, 10)]` | (token length, count) pairs for context template generation |
| `rewrite_module_tmp` | `model.layers.{}.mlp.down_proj` | module template for the edit target — **identical to MEMIT runbook Cell 4** (Llama-3.1-8B SwiGLU MLP down_proj) |
| `layer_module_tmp` | `model.layers.{}` | layer template — **identical to MEMIT runbook Cell 4** |
| `mlp_module_tmp` | `model.layers.{}.mlp` | MLP template |
| `attn_module_tmp` | `model.layers.{}.self_attn` | attention template |
| `ln_f_module` | `model.norm` | final layer norm module name (Llama-3.1-8B specific; differs from GPT-J's `transformer.ln_f`) |
| `lm_head_module` | `lm_head` | LM head module name |

### §3.2 Layer-set candidates at v0.1

> **D-S217-Q4-1 ratification (S2.17 Block 2):** ROME runbook v0.1 declares two layer candidates for HC-2-equivalent dry-run at Block B; load-bearing layer is selected at Block B Cell 12 cross-layer comparison.

| Candidate | Layer index | Rationale | Empirical anchor |
|---|---|---|---|
| **Layer-A (primary)** | `L17` | ROME paper precedent for transformer-mid layer on GPT-J 6B (`L8` of 28) and GPT-2-XL (`L17` of 48); for Llama-3.1-8B (32 layers), `L17` is the structural midpoint | Public paper precedent; no Llama-specific empirical anchor at v0.1 |
| **Layer-B (secondary)** | `L2` | S2.14-D D.1 mediation peak — across all 5 cfb-v3 facts, the MLP-output IE peak concentrated in the L2-L5 band (L_M values: L5/L2/L6/L3/L3) | S2.14-D D.1 causal trace forensic record at `/workspace/causal_trace/` |

**v0.1 declaration:** both `L17` and `L2` are tested at Block B Cells 9-12. Cell 13 verdict gate selects the load-bearing layer for Block C single-fact dispatch.

### §3.3 Llama-3.1-8B-specific hparam considerations (deferred; v0.2)

The ROME paper hparams were calibrated against GPT-J 6B (28 layers, hidden_size 4096, GeLU activations). Llama-3.1-8B (32 layers, hidden_size 4096, SwiGLU activations) differs along three relevant axes:

| Axis | GPT-J | Llama-3.1-8B | v0.1 disposition |
|---|---|---|---|
| MLP activation | GeLU | SwiGLU (gate × silu(up_proj) → down_proj) | `rewrite_module_tmp` targets `down_proj` (the linear layer post-activation); the activation difference is *upstream* of the rewrite target. **Hparam impact: v_lr may need recalibration; deferred to Block B Cell 13** |
| Attention | standard MHA | GQA (Grouped-Query Attention) | Edit target is MLP, not attention; **no direct impact on rewrite hparams** |
| RMSNorm vs LayerNorm | LayerNorm | RMSNorm | `ln_f_module` differs (`model.norm` vs `transformer.ln_f`); per §3.1 declared. **No impact on edit dispatch** |

S2.18 Block B Cell 13 is the empirical resolution gate for v_lr / v_num_grad_steps / mom2_adjustment calibration; v0.2 absorbs verdict.

---

## §4 Process constraints (parallel to MEMIT C-S26-1/2/3 + C-S28-1)

### §4.1 C-ROME-1 — Single-fact dispatch envelope

> **C-ROME-1.** ROME edit invocations at S2.18 Block C are single-fact, single-layer; no batched multi-fact projection is permitted at runbook v0.1. The 15-trial Stage 1 SECT v3 protocol is executed as 15 sequential single-fact ROME edits, not as a batched 5-fact ROME edit.

**Empirical motivation:** ROME's published mechanism is single-fact rank-1 update; batched ROME invocation is not a documented mode of the canonical implementation. MEMIT's batched multi-fact projection is the structural distinction between MEMIT and ROME — testing batched ROME would be an off-paper extension and is out of scope at v0.1.

**Cross-reference.** `t2_rome_runbook_v0_1.md` Block C Cell 14 trial matrix; D-S217-Q4-1.

### §4.2 C-ROME-2 — Covariance cache reuse

> **C-ROME-2.** ROME consumes the NV-resident covariance caches under `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` produced by the pre-S2.6 fork-work session. No new cache compute is required at S2.18 entry. Cell 3 verifies cache inventory ⊆ ROME's required-layer-set per the SUBSET assertion pattern (canonical at MEMIT runbook v1.6 §Cell 3 R1.1; carry-forward to ROME).

**Empirical motivation:** Covariance caches were validated at S2.13-C / S2.14-D / S2.15-D2 against the same Llama-3.1-8B FP16 forward-pass at bit-exact determinism (5 cross-session checkpoints; drift=0.00e+00). The cache content is invariant under write-engine choice — both MEMIT and ROME compute their per-layer C₁ matrix from the same Wikipedia 100k-sample second-moment statistics. ROME's `get_cov` call resolves to the same `_t100_` filename signature (P-6's transitive output form per §1.3 P-6 entry).

**Cross-reference.** `t2_rome_runbook_v0_1.md` Block A Cell 3.

### §4.3 C-ROME-3 — Dry-run gate (R1.3-equivalent)

> **C-ROME-3.** Runbook hardening passes targeting the ROME cache-dispatch surface (Cell 3 R1.1/R1.2/R1.3, Cell 5 model load, Cell 15 trial loop body, OR a patch that affects `get_cov` / `layer_stats` resolution under ROME) require an R1.3-equivalent dry-run gate at Block A Cell 8 against post-patch NV state — REQUIRED before authoring-acceptance ratification of any v0.x → v0.(x+1) advance.

**Empirical motivation:** Direct carry-forward of MEMIT's C-S26-3 (`memit-patches-canonical.md` v2.5 §10.1 + §10.3) and D-S28-2 (R1.3 codification at MEMIT runbook v1.6 §1.5.1). The cache-dispatch defect class is shared between MEMIT and ROME because the underlying `get_cov` → `layer_stats` resolution chain is shared (same `rome/layer_stats.py` file).

**Cross-reference.** `t2_rome_runbook_v0_1.md` Block A Cell 8.

### §4.4 C-ROME-4 — Marker post-application verification (parallel to MEMIT C-S28-1)

> **C-ROME-4.** Hardening passes that authorize new defense-in-depth markers in the ROME runbook must verify post-application source form against fully-patched NV state (parallel to MEMIT C-S28-1 at `memit-patches-canonical.md` v2.5 §10.4). At v0.1, this constraint is **DECLARED but NOT EXERCISED** — no new markers are introduced in this v0.1 patches doc; all marker references are inherited from the MEMIT canonical via shared-codebase application (P-1, P-2, P-4, P-5 transitively; P-6 verification-only).

**Cross-reference.** `memit-patches-canonical.md` v2.5 §10.4 (parent constraint); D-S217-1 at `stage_1_sect_runbook_v1_6.md` §1.5.2 (marker-site discipline companion).

---

## §5 Application order (declared)

The ROME patches application order at S2.18 Block A Cell 2 is:

```
1. Verify P-1 marker on shared util/nethook.py        (canonical site: shared with MEMIT)
2. Verify P-2 marker on shared util/nethook.py        (canonical site: shared with MEMIT)
3. Verify P-4 markers on rome/compute_v.py            (canonical site: shared with MEMIT)
4. Verify P-4 markers on rome/layer_stats.py          (canonical site: shared with MEMIT)
5. Verify P-5 markers on rome/layer_stats.py          (canonical site: shared with MEMIT)
6. Verify post-P-6 source form on rome/layer_stats.py (verification-only per §1.5)
7. Verify Pad-Token alias path                        (Cell 5 model load)
8. Verify Copy-Unmount mechanism availability         (Cell 15 trial fn body)
```

> **Note on application semantics.** ROME runbook Cell 2 is a **verification-only** cell at v0.1, NOT an application cell. The patches are expected to be already applied via the shared NV-resident `/workspace/rome_dry_run/rome/` clone, which inherits from the same SHA-neighborhood as `/workspace/memit_dry_run/memit/`. If Cell 2 verification fails (any marker absent), the operator schedules a fork-work-equivalent ROME patch application session; runbook execution halts. v0.1 does not embed application logic; v0.2 may add application paths if the empirical first-execution surfaces application gaps.

---

## §6 Manifest schema for `t2_rome_patch_state.json`

Cell 2 of `t2_rome_runbook_v0_1.md` emits a structured patch state manifest at `/workspace/architecture_profile/t2_rome_patch_state.json` with the schema:

```json
{
  "captured_at": "<ISO-8601 UTC>",
  "rome_sha": "<resolved 40-char SHA>",
  "patches_verified": {
    "rome_nethook_p1_signature_and_inputs_synthesis": true,
    "rome_nethook_p2_with_kwargs_registration": true,
    "rome_compute_v_p4_hidden_size": true,
    "rome_layer_stats_p4_max_position_embeddings": true,
    "rome_layer_stats_p5_dataset_modernization": true,
    "rome_layer_stats_p6_fstring_post_form": true,
    "tokenizer_pad_token_alias": false,
    "copy_unmount_in_place_restore": false
  },
  "patches_inapplicable": [
    "rome_p3_prime_cpu_offload",
    "rome_explicit_device_map",
    "rome_main_p7_get_cov_batch_tokens"
  ],
  "patches_applied_at_runtime": {
    "tokenizer_pad_token_alias": "Cell 5 (model load)",
    "copy_unmount_in_place_restore": "Cell 15 (trial fn body)"
  },
  "file_sha256_prefix": {
    "util/nethook.py": "<16-char SHA prefix>",
    "rome/compute_v.py": "<16-char SHA prefix>",
    "rome/layer_stats.py": "<16-char SHA prefix>",
    "rome/rome_main.py": "<16-char SHA prefix>"
  }
}
```

---

## §7 Upstream notes — MEMIT canonical vs ROME canonical relationship

This document is **a sibling artifact to `memit-patches-canonical.md` v2.5**, not a child or amendment. The two canonicals share the following:

| Item | MEMIT v2.5 | ROME v0.1 | Relationship |
|---|---|---|---|
| Target model | `meta-llama/Llama-3.1-8B` | `meta-llama/Llama-3.1-8B` | IDENTICAL |
| Target hardware | RunPod RTX 4090 24 GiB | RunPod RTX 4090 24 GiB | IDENTICAL |
| Shared source files | `util/nethook.py`, `rome/compute_v.py`, `rome/layer_stats.py` | (same files via shared codebase ancestry) | IDENTICAL FILES; PATCHES TRANSITIVE |
| MEMIT-only files | `memit/memit_main.py`, `memit/compute_z.py` | (absent) | INAPPLICABLE TO ROME |
| ROME-only files | (absent) | `rome/rome_main.py`, ROME-specific evaluator scripts | UNIQUE TO ROME |
| Covariance cache | NV `/workspace/covariance_caches/.../wikipedia_stats/` | (same NV cache; reuse-only) | SHARED CACHE |
| Process constraints | C-S25-5, C-S26-1/2/3, C-S28-1 | C-ROME-1/2/3/4 | PARALLEL; ROME constraints inherit MEMIT structure with single-fact-dispatch narrowing |

**Modification discipline.** Future amendments to MEMIT canonical (e.g., a hypothetical v2.6) do not propagate into ROME canonical automatically. Cross-references are explicit; co-evolution is maintained at runbook hardening sessions where applicable.

---

## §8 Non-goals

This document does NOT:

1. **Modify `memit-patches-canonical.md` v2.5.** That artifact is preserved unmodified per D-S216-CLOSE-3.
2. **Pre-commit empirical patch applicability.** §1.x verdicts are declared starting points; empirical verdicts at S2.18 Block A Cell 2.
3. **Author ROME-specific patches.** §1.4 is reserved; v0.1 declares no new patches.
4. **Pre-commit ROME hparam values.** §3.1 declares ROME paper Table 1 GPT-J reference values; calibrated values at S2.18 Block B Cell 13.
5. **Pre-commit verdict for T.2 ROME execution.** S2.18 produces the empirical PASS/FAIL/PARTIAL verdict per `t_branch_decision_document.md` §5.
6. **Amend the v1.2 integrated framework spec.** Sealed.

---

## §9 References

### §9.1 Companion artifacts

- `t2_rome_runbook_v0_1.md` v0.1 — companion runbook; consumes this canonical at Cells 1, 2, 3, 4, 8, 15
- `t2_rome_runbook_v0_1_authoring_plan.md` v1.0 — S2.16 deliverable; defines runbook scope
- `t_branch_decision_document.md` — T-branch decision rationale; methodology lock for T.2 ROME

### §9.2 Carry-forward canonical artifacts

- `memit-patches-canonical.md` v2.5 — sibling MEMIT canonical (preserved unmodified)
- `stage_1_sect_runbook_v1_6.md` — MEMIT runbook RATIFIED at S2.17 Block 1; structural template for `t2_rome_runbook_v0_1.md`
- `cfb-v3.yaml` v1.0 — fact corpus (5 facts; instrument-cluster targets)
- `probe-set-v3.yaml` v1.0 — probe set (38 active probes)
- `framework_finding_memit_ceiling_archival.md` v1.0 — empirical context

### §9.3 Decision IDs

- D-S216-CLOSE-2 — empirical anchors carry-forward to T.2 ROME
- D-S216-CLOSE-3 — `memit-patches-canonical.md` v2.5 preserved unmodified; ROME patches authored as parallel canonical
- D-S217-Q2-1 — ROME SHA pin = latest stable tip
- D-S217-Q3-1 — ROME canonical hparams = ROME paper Table 1 GPT-J reference values at v0.1
- D-S217-Q4-1 — Layer candidates = L17 primary + L2 secondary at HC-2-equivalent dry-run
- D-S217-Q5-1 — cfb-v3-004 multi-token posture = first-token-proxy carry-forward + RE-EVALUATE AT TRIAL 0 flag

### §9.4 Repository references

- ROME: `https://github.com/kmeng01/rome`
- ROME paper / supplementary: `https://rome.baulab.info`
- MEMIT (sibling, for reference): `https://github.com/kmeng01/memit` SHA pin `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`

---

## §10 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | S2.17 Block 2 |
| Authoring date | 2026-05-04 |
| Document version | 0.1 |
| Iteration | v1 first synthesis |
| Status | RATIFIED v0.1 — declarative; empirical applicability at S2.18 Block A Cell 2 |
| Supersedes | — (parallel artifact; does not supersede MEMIT canonical) |
| Basis | `memit-patches-canonical.md` v2.5; `t_branch_decision_document.md`; `t2_rome_runbook_v0_1_authoring_plan.md`; ROME paper Table 1 (GPT-J reference) |
| Specialist provenance | memit-specialist (primary); state-consistency-theorist (Copy-Unmount carry-forward); framework-spec-writer (formalization) |
| Last updated | 2026-05-04 |

---

*End of ROME Patches Canonical v0.1.*
