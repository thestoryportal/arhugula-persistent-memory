# ROME Patches Canonical

> **Document version:** v0.2 (empirical absorption of S2.18 first-execution findings)
> **Authoring session:** v0.2 codification session (2026-05-05; operator-side post-S2.18 spec authoring)
> **Status:** RATIFIED v0.2 — empirical applicability verdicts absorbed from S2.18 Block A + Block B; supersedes v0.1 declarative
> **Supersedes:** v0.1 (RATIFIED at S2.17 Block 2; declarative — preserved as historical anchor at git ref or NV mirror; verdicts in v0.1 §1 were predictions superseded by S2.18 empirical record)
> **Companion artifact:** `t2_rome_runbook.md` v0.2 (operator-side post-S2.18; codifies Block A retry + Block B + Block C verdict gate cell-by-cell against post-S2.18 NV state)
> **Sibling artifact:** `memit-patches-canonical.md` v2.5 (preserved unmodified; structurally parallel to this doc per D-S216-CLOSE-3)
> **Specialist provenance:** memit-specialist (primary; ROME edit dispatch architecture analysis, P-7-ROME / P-8-ROME / P-9-ROME authoring rationale, INAPPLICABLE rationale revisions); state-consistency-theorist (secondary; Copy-Unmount mechanism scope under ROME single-fact regime, IC-S23-4 empirical validation extension); framework-spec-writer (formalization)
> **Workstream:** WS1 (empirical execution; T.2 ROME ELIM at canonical hparams; T-branch matrix update load-bearing for S2.19 GRACE routing)

---

## §0 Purpose & non-amendment declaration

This document is the **parallel canonical patches reference for the ROME write engine** under the T.2 ROME work executed at S2.18. It is structurally analogous to `memit-patches-canonical.md` v2.5 (the MEMIT patches canonical) but **does not amend it**. The MEMIT canonical is preserved unmodified at v2.5 per D-S216-CLOSE-3; this ROME canonical is a sibling artifact for a sibling write engine.

**Document scope.** This canonical declares:

1. The **patch inventory** for the ROME write engine on `meta-llama/Llama-3.1-8B`, partitioned by:
   - **SOURCE_LAYER patches** inherited from MEMIT: applicable directly (transplanted from MEMIT-side at session entry), applicable with modification (new ROME-specific source patches), or inapplicable
   - **SOURCE_LAYER patches** authored fresh for ROME (`P-7-ROME`, `P-8-ROME`, `P-9-ROME` — three new patches surfaced empirically at S2.18)
   - **CONFIG_LAYER patches** (NEW patch class introduced at v0.2; `globals.yml` is the first instance)
2. The **SHA pin** for the ROME repository under which patches are valid (resolved empirically at S2.18 Block A Cell 1)
3. The **process constraints** governing the ROME patch surface, paralleling MEMIT's C-S26-1/2/3 + C-S28-1 (C-ROME-1 through C-ROME-4) and adding patch-specific application constraints (C-S218-1 through C-S218-5)
4. The **applicability verdict matrix** mapping each MEMIT patch (P-1, P-2, P-3', P-4, P-5, P-6, P-7, Pad-Token, Copy-Unmount, Device-Map) to its ROME status, **with verdicts now empirically anchored to S2.18 Block A** (replacing the v0.1 declarative predictions)

**v0.1 → v0.2 status delta.** All v0.1 verdicts were **declared** — best-judgment predictions based on shared-codebase heritage and the public ROME paper / repository structure. v0.2 absorbs the **empirical verdicts** produced at S2.18 Block A Cell 2 first-execution against pinned-SHA NV-resident `/workspace/rome_dry_run/rome/`. Where v0.1 predicted "transitively applied via shared codebase", S2.18 surfaced that the shared codebase claim was **empirically false** for P-1, P-2, P-4, P-5, P-6 — these were project-side patches absent from upstream `kmeng01/rome`, and required transplant from MEMIT-side at Cell 2. Where v0.1 predicted P-7 INAPPLICABLE, S2.18 surfaced that ROME requires a structurally analogous patch on a different file (`rome/compute_u.py` rather than `memit/memit_main.py`); v0.2 introduces **P-7-ROME** and recategorizes P-7 as **APPLICABLE-WITH-MODIFICATION**.

**Empirical anchor reference.** The S2.18 forensic record is documented in `session_2_18_summary_block.md` (canonical D / C / OQ / IC) and `session_2_18_summary_block_appendix.md` (cell-by-cell trajectory, patch authoring detail, compute_v traces, verdict surfaces). v0.2 absorbs the appendix's §2 patch authoring detail and §10 empirical anchor map; the appendix is the load-bearing forensic citation for every empirical claim in this v0.2 doc.

---

## §1 Patch inventory

### §1.0 Patch class taxonomy (NEW at v0.2)

v0.2 introduces a two-class patch taxonomy for the ROME canonical:

| Patch class | Definition | Examples | Application semantics |
|---|---|---|---|
| **SOURCE_LAYER** | Patches that modify Python source files in the ROME repository (`rome/*.py`, `util/*.py`) | P-1, P-2, P-4, P-5, P-6, P-7-ROME, P-8-ROME, P-9-ROME | Applied via in-place text substitution against post-clone source; pristine SHA preserved at `<file>.upstream_pristine` siblings |
| **CONFIG_LAYER** | Patches that modify configuration data files (`*.yml`, `*.yaml`, `*.json` in the repo) consumed at module import time | `globals.yml` | Applied via in-place rewrite of the config file body; pristine preserved at `<file>.upstream_pristine`; consumed by `util/globals.py` at first-import |

**v0.1 implicit assumption (corrected at v0.2):** v0.1 enumerated patches as if all were SOURCE_LAYER. S2.18 Cell 8 initial OOM analysis surfaced a CONFIG_LAYER defect path (cwd-relative `STATS_DIR='data/stats'` in `globals.yml` not matching the project's NV cache directory). The CONFIG_LAYER class is structurally distinct from SOURCE_LAYER — config files are not patched as part of source-code application order; they are customized as part of session-entry environment setup. Conflating the two classes obscures both the application order and the verification surface.

**Sibling-parity note.** MEMIT v2.5 currently has no documented CONFIG_LAYER patches. The MEMIT-side `globals.yml` was customized at the pre-S2.6 fork-work session (parallel pattern; STATS_DIR pointed at absolute `/workspace/covariance_caches`) but the customization was never codified in `memit-patches-canonical.md`. If MEMIT canonical is later revised (a hypothetical v2.6) to absorb the CONFIG_LAYER class, both docs adopt the parallel taxonomy at that revision; no retroactive change to MEMIT v2.5 is mandated by this v0.2 ROME doc.

### §1.1 SOURCE_LAYER patches inherited from MEMIT — APPLICABLE DIRECTLY (transplanted)

These patches target files structurally shared between ROME and MEMIT in the project's NV-resident clone, but **empirically not present in upstream `kmeng01/rome`**. v0.1 §1.1 declared them "transitively applied via shared codebase"; S2.18 Cell 2 empirically falsified the shared-codebase claim. v0.2 records them as **APPLICABLE-DIRECTLY via session-entry transplant**: at Cell 2 of `t2_rome_runbook.md` v0.2, three files are copied from `/workspace/memit_dry_run/memit/` (post-MEMIT-patches state) to `/workspace/rome_dry_run/rome/`, with pristine ROME upstream forms preserved at `*.upstream_pristine` siblings.

| ID | Target file (post-transplant) | Pristine ROME upstream form | MEMIT canonical reference | v0.2 verdict | Empirical anchor |
|---|---|---|---|---|---|
| **P-1** | `util/nethook.py` (post-transplant; carries P-1 + P-2 from MEMIT post-state) | `util/nethook.py.upstream_pristine` | `memit-patches-canonical.md` v2.5 §2.2 | **APPLICABLE DIRECTLY (transplanted)** | S2.18 Cell 2 verified marker `def retain_hook(m, args, kwargs, output):` present post-transplant; pristine SHA prefix preserved |
| **P-2** | `util/nethook.py` (companion to P-1; same file) | (same as P-1 pristine) | `memit-patches-canonical.md` v2.5 §2.3 | **APPLICABLE DIRECTLY (transplanted)** | S2.18 Cell 2 verified marker `with_kwargs=True` present post-transplant |
| **P-4** | `rome/compute_v.py` (transplanted from MEMIT-side); `rome/layer_stats.py` (transplanted from MEMIT-side) | `rome/compute_v.py.upstream_pristine`; `rome/layer_stats.py.upstream_pristine` | `memit-patches-canonical.md` v2.5 §3.5 | **APPLICABLE DIRECTLY (transplanted)** | S2.18 Cell 2 verified `max_position_embeddings` count ≥ 2 on `rome/layer_stats.py`; `hidden_size` substring on `rome/compute_v.py` |
| **P-5** | `rome/layer_stats.py` (same file as P-4 target; post-transplant carries P-4 + P-5 + P-6 jointly) | (same as P-4 pristine) | `memit-patches-canonical.md` v2.5 §3.6 | **APPLICABLE DIRECTLY (transplanted)** | S2.18 Cell 2 verified `"20231101.en"` + `"wikimedia/wikipedia"` markers present |
| **P-6** | `rome/layer_stats.py` (same file; post-transplant carries P-4 + P-5 + P-6 jointly) | (same as P-4 pristine) | `memit-patches-canonical.md` v2.5 §3.7 | **APPLICABLE DIRECTLY (transplanted)** | S2.18 Cell 2 verified `size_suffix = f"_t{batch_tokens}" + size_suffix` post-P-6 form on `rome/layer_stats.py` |
| **Pad-Token** | model-load-time tokenizer alias | (no file pristine; runtime patch) | `memit-patches-canonical.md` v2.5 §4 | **APPLICABLE DIRECTLY** | S2.18 Cell 5 EXPECTED branch: `tokenizer.pad_token = tokenizer.eos_token` aliased successfully (id=128001); architecture-sanity all PASS |

**Transplant discipline (NEW at v0.2).** The Cell 2 transplant pattern preserves the upstream ROME pristine state at `<file>.upstream_pristine` siblings to maintain a forensic record of the project-side modification scope. This is the load-bearing transparency mechanism that allows future maintenance to distinguish project-authored patches from upstream baseline. The pristine `.upstream_pristine` files are NOT consumed at edit time; they exist solely for diff-and-audit operations. v0.2 patches doc mandates that any future Cell 2 hardening pass that re-transplants must preserve the pristine sibling pattern.

### §1.2 SOURCE_LAYER patches inherited from MEMIT — APPLICABLE WITH MODIFICATION

These patches target functionality conceptually shared but implemented differently in ROME, requiring authored modification rather than direct transplant.

| ID | MEMIT site | ROME site | MEMIT canonical reference | v0.2 verdict | Empirical anchor |
|---|---|---|---|---|---|
| **P-7** | `memit/memit_main.py` `get_cov` body — `batch_tokens` propagation | (no equivalent file; ROME has no `memit_main.py`) | `memit-patches-canonical.md` v2.5 §3.8 | **INAPPLICABLE TO `memit/memit_main.py:get_cov`** (file absent in ROME); **APPLICABLE-WITH-MODIFICATION via P-7-ROME on `rome/compute_u.py:get_inv_cov`** (ROME's structural analog) | S2.18 Cell 8 initial OOM diagnostic surfaced ROME's lack of `get_cov`; P-7-ROME authored mid-session; S2.18 Cell 8 retry verified post-P-7-ROME cache HIT |
| **Copy-Unmount** | Cell 9 trial fn body — multi-layer joint-overlay (5 layers L4-L8 in S2.14-D D.3; 5 layers L2-L6 in S2.15-D2 D.2) | t2_rome Cell 9 + Cell 11 trial fn body — single-layer dispatch (L17 at Cell 9; L2 at Cell 11) | `memit-patches-canonical.md` v2.5 §6 | **APPLICABLE WITH MECHANISM-PRESERVED, TARGET-NARROWED** | S2.18 Cell 9 + Cell 11 both produced `drift_max = 0.00e+00` on per-fact unmount; bit-exact restore validated under ROME single-fact single-layer regime (extends MEMIT joint-overlay validation to ROME) |

**Copy-Unmount empirical scope extension (NEW at v0.2).** v0.1 §1.2 declared Copy-Unmount "mechanism-preserved single-layer-narrowed" — predictive language. S2.18 Cell 9 (L17 single-layer) + Cell 11 (L2 single-layer) **empirically validated** the mechanism preservation: per-fact unmount produced `drift_max = 0.00e+00` at both layers. This adds a sixth layer-range to the cumulative bit-exact validation set:

| Empirical anchor | Layer range | Write engine | Source session |
|---|---|---|---|
| Joint 5-fact overlay band | L4-L8 (5 layers) | MEMIT batched-multi-fact | S2.14-D D.3 |
| Joint 5-fact overlay narrowed band | L2-L6 (5 layers) | MEMIT batched-multi-fact | S2.15-D2 D.2 |
| Single-fact dispatch | L17 (1 layer) | ROME single-fact | S2.18 Cell 9 |
| Single-fact dispatch | L2 (1 layer) | ROME single-fact | S2.18 Cell 11 |

All four empirical anchors produced `drift_max = 0.00e+00`. The Copy-Unmount mechanism is **engine-independent**: it depends on PyTorch's `state_dict().copy_()` in-place tensor restore primitive, which operates identically under MEMIT's multi-layer joint-restore regime and ROME's single-layer single-restore regime. IC-S23-4 (`drift_max < 1e-4` hard gate) is **EMPIRICALLY-VALIDATED for ROME** at v0.2.

### §1.3 SOURCE_LAYER patches inherited from MEMIT — INAPPLICABLE (with v0.2 rationale revisions)

These patches address concerns that do not arise in ROME's dispatch surface.

| ID | MEMIT concern | ROME status | v0.2 rationale | Empirical anchor |
|---|---|---|---|---|
| **P-3'** | CPU offload for the `torch.linalg.solve` call in MEMIT batched multi-fact projection (FP64 envelope on RTX 4090) | **INAPPLICABLE** | ROME's mechanism is single-fact single-layer rank-1 update via key-value vector arithmetic. There is no batched linear-system solve. Edit memory cost dominated by covariance matrix C₁ load (~822 MB FP32 per layer; same as MEMIT per-layer working set), fits comfortably within RTX 4090 24 GiB. | S2.18 confirmed: `apply_rome_to_model` does not call `torch.linalg.solve`; per-layer GPU delta at edit time was +0.82 GB at Cell 8 retry — bounded by inv_cov load alone |
| **Device-Map** | Conditional companion to P-3' for explicit CPU/GPU partitioning under multi-GPU configurations | **INAPPLICABLE** | Companion to P-3'; same rationale | S2.18 ran on single-GPU (RTX 4090 24 GiB) without device-map customization; no multi-GPU partitioning surface arose |

**v0.1 P-7 INAPPLICABLE rationale — RETRACTED at v0.2.** v0.1 §1.3 declared P-7 INAPPLICABLE on the rationale "ROME's dispatch path through `rome_main.py` does not call `get_cov` with the same batched-projection requirement". This rationale was **partially correct on the symptom but wrong on the structural mechanism**:

- **Correct part:** MEMIT's `get_cov` function (in `memit/memit_main.py`) does not exist in ROME. P-7 as a literal text substitution against the MEMIT site is inapplicable to ROME by structural absence of the target file.
- **Wrong part:** ROME does NOT lack a cache-dispatch path. ROME's dispatch goes through `rome/compute_u.py:get_inv_cov`, which calls `layer_stats(...)` WITHOUT threading `batch_tokens`. The same defect class P-7 closed for MEMIT (cache-compute and edit-time `batch_tokens` asymmetry producing a cache-filename mismatch) **manifests in ROME at a different file under a different function name**. ROME's analog of MEMIT's `get_cov` is `get_inv_cov` (ROME computes the inverse covariance directly inside the same wrapper, rather than computing the covariance and inverting later). The patch surface is structurally homologous; only the file path and function name differ.

v0.2 corrects the v0.1 rationale: **P-7 is INAPPLICABLE to `memit/memit_main.py:get_cov`** (the literal v0.1 wording is technically correct on the file scope) **but APPLICABLE-WITH-MODIFICATION via P-7-ROME on `rome/compute_u.py:get_inv_cov`** (the structural analog requires its own patch authored against the ROME-side file). See §1.4 for P-7-ROME and §6 for the full P-7-ROME spec.

**v0.1 P-6 entry — partial correction at v0.2.** v0.1 §1.3 stated "ROME does call `get_cov` via shared `rome/layer_stats.py`". This is **incorrect on the function name** (ROME has no `get_cov` function — the function in `rome/compute_u.py` is `get_inv_cov`) but **correct on the underlying mechanism** (ROME calls `layer_stats` from `get_inv_cov`, and the cache filename's `_t100_` segment is required for cache HIT). v0.2 corrects: ROME calls `get_inv_cov`, which calls `layer_stats`. The P-6 `_t100_` filename mechanism is APPLICABLE-DIRECTLY via the transplanted `rome/layer_stats.py` (per §1.1) and is propagated to ROME's edit-time dispatch via P-7-ROME's `batch_tokens` threading (per §1.4). P-6 and P-7-ROME are jointly required for cache filename round-trip correctness on ROME's edit-time dispatch path under `batch_tokens < npos` regimes.

### §1.4 SOURCE_LAYER patches authored fresh for ROME (NEW at v0.2)

S2.18 Block A and Block B surfaced three latent defects in upstream `kmeng01/rome` at SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04` that block ROME edit dispatch on `meta-llama/Llama-3.1-8B` fp16 against the project's NV-resident covariance cache. v0.2 introduces three NEW patches authored mid-session at S2.18:

| ID | Target file | Surgical edits | Closes defect | v0.2 detail section |
|---|---|---|---|---|
| **P-7-ROME** | `rome/compute_u.py` | 3 (signature, layer_stats call, compute_u call site) | Cache filename `_t100_` mismatch on edit-time dispatch — produces OOM via local recompute fallback when model resident on RTX 4090 24 GiB | §6 |
| **P-8-ROME** | `rome/compute_u.py` | 1 (`.to(u.dtype)` cast at compute_u matmul site) | `fp32 inv_cov @ fp16 cur_repr` dtype mismatch RuntimeError on fp16-loaded base models | §7 |
| **P-9-ROME** | `rome/rome_main.py` | 2 (`.to(weight.dtype)` cast on both operands at execute_rome and apply_rome_to_model outer-product sites) | `fp16 left_vector @ fp32 right_vector` dtype mismatch RuntimeError at outer-product matmul | §8 |

**Authoring chronology (S2.18):**

| Patch | Surfaced at | Pre-patch SHA prefix (compute_u.py) | Post-patch SHA prefix |
|---|---|---|---|
| P-7-ROME | Cell 8 initial OOM | `06a73593171eecdd` | `74ce3cdda79d992d` |
| P-8-ROME | Cell 9 first attempt fp32-fp16 mismatch | `74ce3cdda79d992d` | `79c4c5201b5fb6cb` |
| P-9-ROME | Cell 9 second attempt outer-product mismatch | (different file: `rome_main.py`) `dfad8eaa83940bfd` → `bb138849203d0236` | (post-edit) |

All three patches are **load-bearing for ROME edit dispatch on Llama-3.1-8B fp16 under any modern long-context base model** (`max_position_embeddings > 8192`). Without P-7-ROME, OOM. Without P-8-ROME, RuntimeError at compute_u matmul. Without P-9-ROME, RuntimeError at outer-product. The three patches are jointly required; no subset is sufficient.

**MEMIT-side analog status — universally NO.** None of P-7-ROME / P-8-ROME / P-9-ROME has a MEMIT-side analog, because MEMIT bypasses `rome/compute_u.py` and `rome/rome_main.py` entirely (MEMIT has its own dispatch through `memit/memit_main.py:apply_memit_to_model` → `compute_u_v` → `compute_z`). The latent defects in upstream `kmeng01/rome` were never observed in MEMIT-only sessions because MEMIT never executes those code paths. v0.2 patches doc records the MEMIT-side absence explicitly to prevent confusion at any future cross-canonical maintenance pass.

### §1.5 Verification-only carry-forward (no patch application; verification gate only)

| Item | Verification gate | Cell | Rationale | v0.2 status |
|---|---|---|---|---|
| **Post-P-6 source form on `rome/layer_stats.py`** | `assert 'size_suffix = f"_t{batch_tokens}" + size_suffix' in layer_stats_src` | t2_rome_runbook v0.2 Block A Cell 2 | The transplanted `rome/layer_stats.py` carries the post-P-6 form from MEMIT-side (per §1.1). Cell 2 verifies. | EMPIRICALLY-VALIDATED at S2.18 Cell 2 |
| **Post-P-7-ROME source form on `rome/compute_u.py`** | `assert 'mom2_batch_tokens' in compute_u_src` (uniquely identifying token; P-7-ROME's idempotency marker) | t2_rome_runbook v0.2 Block A Cell 2 (post-S2.18) | After session-entry transplant + P-7-ROME application, Cell 2 verifies the P-7-ROME marker. | EMPIRICALLY-VALIDATED at S2.18 Cell 8 retry |
| **Post-P-8-ROME source form on `rome/compute_u.py`** | `assert '.to(u.dtype) @' in compute_u_src` | t2_rome_runbook v0.2 Block A Cell 2 (post-S2.18) | After P-8-ROME application, Cell 2 verifies the `.to(u.dtype) @` matmul site. | EMPIRICALLY-VALIDATED at S2.18 Cell 9 |
| **Post-P-9-ROME source form on `rome/rome_main.py`** | `assert '.to(weight.dtype)' in rome_main_src` (count ≥ 2; one per outer-product site) | t2_rome_runbook v0.2 Block A Cell 2 (post-S2.18) | After P-9-ROME application, Cell 2 verifies both call sites. | EMPIRICALLY-VALIDATED at S2.18 Cell 9 second attempt |
| **Post-P-7-equivalent on `rome_main.py`** | DEFERRED — P-7-ROME target is `rome/compute_u.py`, not `rome_main.py`. Latent at `rome_main.py` is the outer-product surface (P-9-ROME) only. | n/a | (preserved from v0.1) | n/a |

### §1.6 CONFIG_LAYER patches (NEW class at v0.2)

S2.18 Cell 8 initial OOM diagnostic surfaced the `globals.yml` defect path (cwd-relative `STATS_DIR='data/stats'` in upstream pristine config; ROME-side never customized to match the project's NV-resident covariance cache directory at `/workspace/covariance_caches`). v0.2 introduces the CONFIG_LAYER patch class for this and any future config-file customizations.

| ID | Target file | Patch type | v0.2 detail section | Empirical anchor |
|---|---|---|---|---|
| **`globals.yml`** | `rome/globals.yml` | per-repo absolute NV-anchored `STATS_DIR` (and companion config path) customization | §9 | S2.18 Cell 8 initial OOM diagnostic; post-customization Cell 8 retry produced cache HIT |

**Schema divergence note (carried from S2.18 appendix §2.1).** ROME-side `globals.yml` parses 5 fields (`RESULTS_DIR`, `DATA_DIR`, `STATS_DIR`, `HPARAMS_DIR`, `REMOTE_ROOT_URL`). MEMIT-side `globals.yml` parses 6 fields (adds `KV_DIR`). The MEMIT extension is a structural difference between the two repositories — not a patch we backport to ROME at v0.2. Future cross-repo maintenance should preserve this schema asymmetry; ROME canonical does not assume MEMIT's `KV_DIR` field.

**Application semantics — distinct from SOURCE_LAYER.** CONFIG_LAYER patches are applied at **session-entry environment setup** (typically Cell 8 initial diagnostic phase or earlier as part of pod-image bake-out), not as part of the SOURCE_LAYER application order in §10. They are consumed by `util/globals.py` at first import; once `util.globals.STATS_DIR` is bound to the customized value, the customization is permanent for the kernel lifetime. Application order between CONFIG_LAYER and SOURCE_LAYER patches is **CONFIG_LAYER first** — `util/globals.py` is imported transitively by source files that reference `STATS_DIR`, so the config must be in place before any source file using it is loaded.

---

## §2 v0_1_undocumented_findings (NEW at v0.2)

The S2.18 first-execution surfaced eight findings that v0.1 did not anticipate. v0.2 records each as a structural finding with its empirical anchor, scope, and v0.2 disposition. These findings are **observational, not patches** — they document properties of upstream `kmeng01/rome` (or its interaction with the project's environment) that the v0.1 declarative authoring missed.

### §2.1 `globals_yml_config_layer` — CONFIG_LAYER patch class

**Finding:** ROME's `util/globals.py` reads `globals.yml` at cwd-relative path on import. Default `STATS_DIR='data/stats'` resolves against `os.getcwd()` (which is `ROME_ROOT` post-Cell-2 chdir per `os.chdir(ROME_ROOT)`) to `/workspace/rome_dry_run/rome/data/stats` — does NOT match the project's NV-resident covariance cache directory at `/workspace/covariance_caches`.

**v0.1 miss:** v0.1 §1 patch inventory enumerated only SOURCE_LAYER patches; CONFIG_LAYER patches were not anticipated.

**v0.2 disposition:** New CONFIG_LAYER patch class introduced at §1.0. `globals.yml` codified at §1.6 / §9. Future cross-repo work should treat config files as a first-class patch surface.

**Cross-reference:** §1.6, §9.

### §2.2 `rome_no_get_cov_function` — function name correction

**Finding:** ROME's edit-time covariance dispatch in `rome/compute_u.py` defines `get_inv_cov(...)` (which computes and returns `torch.inverse(C)`), NOT `get_cov(...)`. There is no `get_cov` function in upstream `kmeng01/rome` at SHA pin `0874014c...`.

**v0.1 miss:** v0.1 §1.3 P-6 entry stated "ROME does call get_cov via shared `rome/layer_stats.py`" — incorrect on function name. v0.1 §1.3 P-7 entry stated "ROME's dispatch path through `rome_main.py` does not call `get_cov`" — correct on the literal but missed the structural analog `get_inv_cov`.

**v0.2 disposition:** §1.3 corrects the function name to `get_inv_cov` for both P-6 and P-7 entries. P-7-ROME (§6) targets `get_inv_cov` as ROME's structural analog of MEMIT's `get_cov`.

**Cross-reference:** §1.3, §1.4, §6.

### §2.3 `mom2_adjustment_int_vs_bool_resolved` — hparam type interpretation

**Finding:** ROME paper Table 1 declares `mom2_adjustment=15000` as an integer scaling factor (analogous to MEMIT's `mom2_update_weight`). Upstream `kmeng01/rome` `rome/compute_u.py` interprets `hparams.mom2_adjustment` as a **boolean** at one branch (`if hparams.mom2_adjustment: ... # apply inv_cov`) — this is a coincidence of Python's truthy semantics where any nonzero int is truthy. The hparam value `15000` is passed through correctly on the truthy branch. S2.18 Cell 4 surfaced this as a forensic note; resolved without code change because the intended semantics (apply inv_cov when scaling is nonzero) coincides with the implementation.

**v0.1 miss:** v0.1 §3.1 declared `mom2_adjustment=15000` without flagging the truthy-vs-int interpretation surface.

**v0.2 disposition:** Documented as observational finding. No patch required because the truthy branch executes correctly with int value `15000`. Future hparam refactoring (e.g., a hypothetical hparam-schema unification across ROME and MEMIT) should explicitly type this field as `int`.

**Cross-reference:** §4.

### §2.4 `stats_dir_hparam_unused_by_rome` — hparam field redundancy

**Finding:** ROME's `ROMEHyperParams` dataclass schema (19 fields at upstream pristine; verified count at S2.18 Cell 4 forensic surfacing) does not include `stats_dir`. The `STATS_DIR` is sourced exclusively from `util/globals.py` (which reads `globals.yml`). MEMIT's `MEMITHyperParams` includes `stats_dir` as an hparam field (set via the runbook); ROME does not.

**v0.1 miss:** v0.1 §3.1 hparam table did not include `stats_dir`; absence was correct but not explicitly noted as a divergence from MEMIT.

**v0.2 disposition:** Documented. ROME hparam construction at runbook v0.2 Cell 4 should NOT attempt to set `stats_dir` on the `ROMEHyperParams` instance — the field does not exist and would either raise (if the dataclass uses `__slots__`) or silently no-op (if dataclass uses default `__dict__`). The CONFIG_LAYER `globals.yml` patch (§9) is the canonical mechanism for `STATS_DIR` customization on the ROME side.

**Cross-reference:** §1.6, §4, §9.

### §2.5 `force_recompute_parameter` — `layer_stats` kwarg passthrough

**Finding:** ROME's `get_inv_cov(...)` signature at upstream pristine does NOT carry a `force_recompute` parameter (unlike MEMIT's `get_cov` which does). The `layer_stats(...)` call inside `get_inv_cov` therefore uses `layer_stats`'s default `force_recompute=False`. For S2.18 dispatch this was the correct behavior (cache HIT was the desired outcome); however, future ROME work that requires recompute (e.g., a cache-invalidation flow) would need either:

- An additive patch threading `force_recompute` through `get_inv_cov`'s signature (parallel surgical edit pattern to P-7-ROME)
- Or operator-side cache deletion + cold cache compute (not recommended; expensive)

**v0.1 miss:** Not anticipated (v0.1 was declarative; recompute path was out of scope).

**v0.2 disposition:** Observational finding. No v0.2 patch authored. If future runbook work requires recompute on the ROME side, the `force_recompute` threading is a candidate P-10-ROME (or equivalent next-numbered patch).

**Cross-reference:** §6.

### §2.6 `p4_compute_v_redundant_nesting` — P-4 fallback nesting on `compute_v.py`

**Finding:** P-4's substitution map on `rome/compute_v.py` (per `memit-patches-canonical.md` v2.5 §3.5.4) wraps a `getattr(..., "n_embd", model.config.hidden_size)` fallback around an existing `model.config.n_embd` reference. The transplanted `rome/compute_v.py` from MEMIT-side carries this wrapped form. **Forensic note:** the fallback is structurally redundant on Llama-3.1-8B (which has `hidden_size=4096` but no `n_embd` attribute) — `getattr(..., "n_embd", ...)` always evaluates to the fallback. The wrap does not produce incorrect behavior; it is a backward-compatibility provision for GPT-2-family base models that retain `n_embd`.

**v0.1 miss:** Not flagged as a forensic note in v0.1.

**v0.2 disposition:** Documented as observational. The redundant nesting on Llama is harmless (no runtime cost; the `getattr` resolves to the fallback once per call). Future hparam-class refactoring could simplify, but this is not required.

**Cross-reference:** §1.1.

### §2.7 `p_7_rome_get_inv_cov_batch_tokens` — P-7-ROME structural rationale

**Finding:** The P-7 defect class (cache-compute and edit-time `batch_tokens` asymmetry producing cache-filename mismatch) manifests in ROME at `rome/compute_u.py:get_inv_cov` rather than `memit/memit_main.py:get_cov`. The structural homology is exact: both functions are wrappers around `layer_stats(...)` that perform the cache-resolution dispatch; both fail to thread `batch_tokens` at upstream pristine. The patch surface (a 3-edit signature + call-site + caller modification) is structurally equivalent on both sides. P-7 (MEMIT) and P-7-ROME (ROME) are sibling patches addressing the same defect class on parallel files.

**v0.1 miss:** v0.1 §1.3 declared P-7 INAPPLICABLE without recognizing the ROME-side analog.

**v0.2 disposition:** P-7-ROME authored at S2.18 Cell 8 initial OOM (mid-session); codified at §6. v0.1's P-7 INAPPLICABLE rationale recategorized at §1.3.

**Cross-reference:** §1.3, §1.4, §6.

### §2.8 `p_8_rome_precision_coercion` — P-8-ROME structural rationale

**Finding:** ROME's `compute_u.py` matmul site `inv_cov @ cur_repr` is structurally fragile under fp16-loaded base models. `inv_cov` is fp32 by construction (`torch.inverse(...).float()` at line 53 of upstream pristine compute_u.py — fp32 is required for numerical stability of the inverse). `cur_repr` is fp16 by construction on Llama-3.1-8B fp16 model load (the model's hidden states inherit the model dtype). PyTorch's `@` operator requires matching dtypes. Upstream `kmeng01/rome` was developed against GPT-2-XL / GPT-J, both fp32 by default — the dtype mismatch never manifested. ROME on any fp16 base model hits this defect.

**v0.1 miss:** Not anticipated. v0.1 §3 hparams declared `mom2_dtype=float32` which is the precision for the cached covariance matrix on disk; it does not prevent the runtime fp32-fp16 mismatch at the matmul site (the cache loads as fp32, but cur_repr is fp16 and the cast point was missing).

**v0.2 disposition:** P-8-ROME authored at S2.18 Cell 9 first attempt (mid-session); codified at §7. The patch chooses `.to(u.dtype)` (cast inv_cov fp32→fp16 at use-time) over the alternative `.to(inv_cov.dtype)` (cast u fp16→fp32) — the chosen direction is minimum-invasive and preserves the post-matmul precision the downstream compute_v expects.

**Cross-reference:** §1.4, §7, C-S218-2.

### §2.9 `p_9_rome_outer_product_precision` — P-9-ROME structural rationale (sibling sites)

**Finding:** ROME's outer-product sites at `execute_rome` (line 117 at upstream pristine) and `apply_rome_to_model` (line 43 at upstream pristine) carry the same dtype-mismatch defect under fp16 base models. `left_vector` is fp16 (from compute_u post-P-8-ROME). `right_vector` is fp32 (from compute_v's Adam optimization buffer; Adam runs on fp32 `delta` parameter regardless of base model dtype). The outer-product `left_vector.unsqueeze(1) @ right_vector.unsqueeze(0)` mismatches.

**Sibling sites:** Both call sites carry the same pattern. Patching one without the other leaves a latent defect at the unpatched site — if a future ROME refactor adds multi-fact dispatch through `apply_rome_to_model`'s loop, the unpatched site would be exercised and fail. Symmetric patch (both sites) is required; v0.2 P-9-ROME applies to both.

**v0.1 miss:** Not anticipated.

**v0.2 disposition:** P-9-ROME authored at S2.18 Cell 9 second attempt (mid-session); codified at §8. The patch casts both operands to `weight.dtype` (the target weight matrix's dtype, which is the model's dtype — fp16 on Llama-3.1-8B) at both call sites. Tying the cast target to `weight.dtype` rather than a hardcoded `torch.float16` makes the patch portable across base-model dtypes.

**Cross-reference:** §1.4, §8, C-S218-3.

---

## §3 ROME repository SHA pin

**Repository:** `https://github.com/kmeng01/rome`
**SHA pin (resolved at S2.18 Block A Cell 1):** `0874014cd9837e4365f3e6f3c71400ef11509e04`

> **D-S217-Q2-1 ratification anchor (S2.17 Block 2):** ROME SHA pin = latest stable tip at runbook v0.1 authoring. S2.18 Block A Cell 1 resolved the placeholder to the concrete 40-char SHA `0874014cd9837e4365f3e6f3c71400ef11509e04` (closes OQ-S216-1 per `session_2_18_summary_block.md` D-S218-1 trace).

**Operator override semantics.** All v0.2 patches in §1 / §6 / §7 / §8 / §9 apply against this SHA-pinned source state. If the operator pins to a different SHA at a future session (e.g., upstream pushes a regression that motivates rolling back), the patch line numbers and substitution targets in §6 / §7 / §8 must be re-derived against the new SHA. The idempotency markers in each patch's verification block (§6.X / §7.X / §8.X) are SHA-stable provided the patched substring is preserved across the SHA shift; line numbers are nominal.

**Cross-reference.** `t2_rome_runbook.md` v0.2 Block A Cell 1 (SHA capture); §3 of this doc (resolution semantics).

---

## §4 ROME canonical hparams

> **D-S217-Q3-1 ratification (S2.17 Block 2):** ROME canonical hparams at v0.1 = ROME paper Table 1 GPT-J reference values (declarative starting point); empirical calibration to Llama-3.1-8B at S2.18 Block B Cell 13 trial 0.
>
> **v0.2 calibration outcome:** S2.18 Cell 13 verdict gate B-FAIL at canonical hparams. **No calibrated hparam values supersede the GPT-J reference at v0.2.** The architectural-invariant ceiling (per `framework_finding_memit_ceiling_archival.md` v1.1) shows the FAIL is structural at canonical hparams; recalibration was NOT explored at S2.18 (per Route A halt at Cell 13 verdict gate; D-S218-2). Future hparam recalibration (if S2.19 GRACE FAILs and operator chooses to revisit ROME at non-canonical hparams) would be a v0.3 codification scope.

### §4.1 ROME paper Table 1 reference values (preserved from v0.1 §3.1)

The ROME paper (Meng et al., 2022, "Locating and Editing Factual Associations in GPT") publishes canonical hparams for GPT-J 6B. The starting values declared here are the published GPT-J values, transferred without modification to Llama-3.1-8B as the v0.1 baseline; v0.2 preserves these as the **canonical ROME hparams** since S2.18 produced FAIL at these values without invalidating their canonical status (the FAIL is a property of the model × engine pair, not of the hparam values per se).

| Hparam | GPT-J Table 1 value | Notes |
|---|---|---|
| `v_lr` | `0.5` | gradient step size for `target_v` optimization |
| `v_num_grad_steps` | `20` | optimization iterations for `target_v` |
| `v_loss_layer` | `27` (GPT-J) → `31` (Llama-3.1-8B last layer per v0.1 placeholder; S2.18 verified `31` per Cell 9 / Cell 11 `Tying optimization objective to 31` log) | layer at which the cross-entropy loss is computed for v-optimization |
| `v_weight_decay` | `0.5` | regularization on `target_v` magnitude |
| `clamp_norm_factor` | `4` | clip on `target_v` norm relative to base model embedding norm |
| `kl_factor` | `0.0625` | KL regularization weight in v-optimization loss |
| `mom2_adjustment` | `15000` | C₁⁻¹ scaling factor (analogous to MEMIT's `mom2_update_weight`); see §2.3 for int-vs-bool truthy interpretation |
| `context_template_length_params` | `[(5, 10), (10, 10)]` | (token length, count) pairs for context template generation |
| `rewrite_module_tmp` | `model.layers.{}.mlp.down_proj` | identical to MEMIT runbook Cell 4 (Llama-3.1-8B SwiGLU MLP `down_proj`) |
| `layer_module_tmp` | `model.layers.{}` | identical to MEMIT runbook Cell 4 |
| `mlp_module_tmp` | `model.layers.{}.mlp` | MLP template |
| `attn_module_tmp` | `model.layers.{}.self_attn` | attention template |
| `ln_f_module` | `model.norm` | Llama-3.1-8B-specific (vs GPT-J's `transformer.ln_f`) |
| `lm_head_module` | `lm_head` | LM head module name |

### §4.2 Layer-set candidates at v0.1 — empirical verdict at v0.2

> **D-S217-Q4-1 ratification (S2.17 Block 2):** ROME runbook v0.1 declared two layer candidates for HC-2-equivalent dry-run at Block B; load-bearing layer was to be selected at Block B Cell 12 cross-layer comparison.
>
> **v0.2 empirical verdict (S2.18 Cell 13):** D-S218-9 closes Q4-1 with value **NO_LOAD_BEARING_LAYER**. Both candidate layers L17 and L2 fail the consistency criterion P(target_new_post) > 0.5. Different mechanisms produce the same outcome.

| Candidate | Layer index | v0.1 rationale | S2.18 empirical outcome |
|---|---|---|---|
| **Layer-A (primary)** | `L17` | ROME paper precedent for transformer-mid layer on GPT-J (`L8` of 28) and GPT-2-XL (`L17` of 48); for Llama-3.1-8B (32 layers), `L17` is the structural midpoint | **FAIL** at canonical hparams. compute_v monotonic decrease to ceiling P=1.06e-02 (5+ orders of magnitude below threshold 0.5). Pathology: BOS collapse on rewrite-shape prompt (post-edit cons-1 top_1 = `<\|begin_of_text\|>` with P=0.924) |
| **Layer-B (secondary)** | `L2` | S2.14-D D.1 mediation peak — across all 5 cfb-v3 facts, MLP-output IE peak concentrated in L2-L5 band | **FAIL** at canonical hparams. compute_v oscillating non-converging trajectory; final P=1.06e-06. Pathology: unfittable landscape (no descent direction) |

**v0.2 layer disposition:** Both L17 and L2 are recorded as **empirically tested at canonical hparams**; both FAIL at structurally distinct mechanisms. The architectural-invariant ceiling extends to ROME at these two layers (per `framework_finding_memit_ceiling_archival.md` v1.1 Axis 7). No third layer was tested at S2.18; future ROME work (if any) at non-canonical hparams would explore the layer × hparam space jointly.

### §4.3 Llama-3.1-8B-specific hparam considerations (v0.2 carry-forward)

The ROME paper hparams were calibrated against GPT-J 6B (28 layers, hidden_size 4096, GeLU activations). Llama-3.1-8B (32 layers, hidden_size 4096, SwiGLU activations) differs along three axes:

| Axis | GPT-J | Llama-3.1-8B | v0.2 disposition |
|---|---|---|---|
| MLP activation | GeLU | SwiGLU (gate × silu(up_proj) → down_proj) | `rewrite_module_tmp` targets `down_proj` (linear post-activation); activation difference is upstream of edit target. Hparam impact unclear; not explored at S2.18 (canonical-hparams-only protocol) |
| Attention | standard MHA | GQA (Grouped-Query Attention) | Edit target is MLP, not attention; no direct impact on rewrite hparams |
| RMSNorm vs LayerNorm | LayerNorm | RMSNorm | `ln_f_module` differs; per §4.1 declared. No impact on edit dispatch |

**Note on v0.2 calibration scope.** S2.18 was protocol-bound to test only canonical hparams (per D-S217-Q3-1 + the t-branch entry methodology lock in `t_branch_decision_document.md` §4). Recalibration was NOT explored. The architectural-invariant ceiling FAIL at canonical hparams is the load-bearing finding for T.2 ROME ELIM; recalibration would have inverted the falsification methodology.

---

## §5 Process constraints

### §5.1 C-ROME-1 — Single-fact dispatch envelope

> **C-ROME-1 (EMPIRICALLY-VALIDATED at S2.18 Cell 9 + Cell 11; status change DECLARED → EMPIRICALLY-VALIDATED).** ROME edit invocations MUST be invoked with `requests` list of length exactly 1 per dispatch. The 15-trial Stage 1 SECT v3 protocol (if exercised) is executed as 15 sequential single-fact ROME edits, not as a batched 5-fact ROME edit.

**Empirical motivation.** ROME's published mechanism is single-fact rank-1 update. S2.18 Cell 9 (cfb-v3-001 / Bo Jackson / guitar at L17) and Cell 11 (same fact at L2) both invoked `apply_rome_to_model(model, tok, requests=[req], hparams)` with `len(requests) == 1`. Both invocations completed without errors related to dispatch shape; the FAIL outcomes were verdict-class (consistency criterion), not dispatch-class.

**Cross-reference.** `t2_rome_runbook.md` v0.2 Cell 9 / Cell 11 dispatch envelope; D-S218-1 ratification trace.

### §5.2 C-ROME-2 — Covariance cache reuse

> **C-ROME-2 (EMPIRICALLY-VALIDATED at S2.18 Cell 8 + Cell 9 + Cell 11; status change DECLARED → EMPIRICALLY-VALIDATED).** ROME consumes the NV-resident covariance caches under `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` produced by the pre-S2.6 fork-work session and extended at S2.18 Block A pre-flight (L17 added). No new cache compute is required at session entry. Cell 3 of the runbook verifies cache inventory ⊆ ROME's required-layer-set per the SUBSET assertion pattern.

**Empirical motivation.** S2.18 verified cache HIT at three layers via the post-P-7-ROME `_t100_` filename form: L4 (Cell 8 retry smoke), L17 (Cell 9 edit dispatch), L2 (Cell 11 edit dispatch). Cache files preserved across all three accesses; no recompute triggered. The covariance cache reuse protocol is bit-exact under the cross-session bit-exact determinism gate (per IC-PreS26-3) — the cache content is invariant under write-engine choice (MEMIT and ROME compute the same per-layer C₁ matrix from the same Wikipedia 100k-sample second-moment statistics).

**Cross-reference.** `t2_rome_runbook.md` v0.2 Block A Cell 3; IC-PreS26-2 (cache filename signature); IC-PreS26-3 (cache schema).

### §5.3 C-ROME-3 — Dry-run gate (R1.3-equivalent)

> **C-ROME-3 (EMPIRICALLY-VALIDATED at S2.18 Cell 8 retry; status change DECLARED → EMPIRICALLY-VALIDATED).** Runbook hardening passes targeting the ROME cache-dispatch surface require an R1.3-equivalent dry-run gate at Block A Cell 8 against post-patch NV state, REQUIRED before authoring-acceptance ratification of any v0.x → v0.(x+1) advance. The smoke MUST call `rome.compute_u.get_inv_cov(...)` (not the hypothetical `get_cov` per §2.2 finding); the smoke layer SHOULD be outside the Block B sweep window for fair wall-time accounting.

**Empirical motivation.** S2.18 Cell 8 initial attempt (pre-P-7-ROME, pre-`globals.yml` customization) hit OOM at 11.32s. Cell 8 retry (post-P-7-ROME, post-`globals.yml`) hit cache HIT at 2.35s (smoke layer L4, outside the {L2, L17} sweep window). The retry-vs-initial divergence is the load-bearing empirical signal that the dry-run gate caught the dispatch defect at the smoke surface, before the load-bearing Cell 9 edit dispatch — exactly the methodology intent codified in MEMIT's C-S26-3.

**Cross-reference.** `t2_rome_runbook.md` v0.2 Block A Cell 8 (post-S2.18); D-S218-2 (Cell 13 verdict gate routing).

### §5.4 C-ROME-4 — Marker post-application verification

> **C-ROME-4 (EMPIRICALLY-VALIDATED at S2.18 P-7-ROME + P-8-ROME + P-9-ROME marker checks; status change DECLARED → EMPIRICALLY-VALIDATED).** Hardening passes that authorize new defense-in-depth markers in the ROME runbook MUST verify post-application source form against fully-patched NV state. At v0.2, this constraint is **EXERCISED** by the three new patches' verification blocks (§6.X / §7.X / §8.X).

**Empirical motivation.** S2.18 introduced six defense-in-depth markers across the three new patches:
- P-7-ROME: 3 markers (signature `mom2_batch_tokens`; layer_stats kwarg `batch_tokens=mom2_batch_tokens`; compute_u call site `mom2_batch_tokens=getattr(...)`)
- P-8-ROME: 1 marker (`.to(u.dtype) @`)
- P-9-ROME: 2 markers (`.to(weight.dtype)` at execute_rome; same pattern at apply_rome_to_model)

All six markers verified at S2.18 Cell 8 retry / Cell 9 first attempt / Cell 9 second attempt against post-application NV source — **each marker present in post-patch source by direct re-read after str_replace application**. C-S28-1 (the parent constraint from MEMIT v2.5 §10.4) is satisfied by-construction at v0.2 because the marker authoring discipline (verify against post-application source before authoring) was followed empirically during S2.18 mid-session patch authoring.

**Cross-reference.** `memit-patches-canonical.md` v2.5 §10.4 (parent constraint); D-S217-1 at `stage_1_sect_runbook_v1_6.md` §1.5.2 (marker-site discipline companion).

### §5.5 C-S218-1 — P-7-ROME application is REQUIRED

> **C-S218-1.** P-7-ROME application is REQUIRED for ROME edit dispatch on any base model with covariance cache constructed via post-P-6 `batch_tokens=100` form. Without this patch, `get_inv_cov` constructs cache filename without `_t100_` segment, hits HTTP 404 from upstream `https://rome.baulab.info/...`, falls back to local Wikipedia mom2 compute, OOMs with model resident on 24 GiB-class GPU.

**Application scope.** Any session executing ROME edit dispatch on Llama-3.1-8B (or any base model with `max_position_embeddings > 8192`) against the project's NV-resident covariance cache. Without P-7-ROME, the dispatch path is structurally broken at edit time; no recovery without the patch.

**Empirical anchor.** S2.18 Cell 8 initial attempt OOM at 22.81 GiB allocation request; Cell 8 retry success post-P-7-ROME application.

**Cross-reference.** §6 (P-7-ROME spec); §2.7 (structural rationale).

### §5.6 C-S218-2 — P-8-ROME application is REQUIRED

> **C-S218-2.** P-8-ROME application is REQUIRED for ROME edit dispatch on any base model loaded in fp16 (or any non-fp32 dtype). Without this patch, the matmul at `compute_u.py` line 120 fails with dtype mismatch RuntimeError (`fp32 inv_cov @ fp16 cur_repr`).

**Application scope.** Any session executing ROME edit dispatch with a fp16-loaded base model. ROME on GPT-2-XL / GPT-J fp32 would not require this patch (the latent defect never manifests when both operands are fp32).

**Empirical anchor.** S2.18 Cell 9 first attempt RuntimeError pre-P-8-ROME; Cell 9 first attempt success post-P-8-ROME application.

**Cross-reference.** §7 (P-8-ROME spec); §2.8 (structural rationale).

### §5.7 C-S218-3 — P-9-ROME application is REQUIRED

> **C-S218-3.** P-9-ROME application is REQUIRED for ROME edit dispatch on any base model loaded in fp16. Without this patch, the outer-product at `rome_main.py` line 117 (`execute_rome`) fails with dtype mismatch RuntimeError (`fp16 left_vector @ fp32 right_vector` from compute_v's Adam optimization buffer). Both call sites (`execute_rome` line 117 + `apply_rome_to_model` line 43) MUST be patched to prevent latent regression at the unpatched site under future multi-fact dispatch refactors.

**Application scope.** Any session executing ROME edit dispatch with a fp16-loaded base model.

**Empirical anchor.** S2.18 Cell 9 second attempt RuntimeError pre-P-9-ROME; Cell 9 second attempt success post-P-9-ROME application (both call sites patched symmetrically).

**Cross-reference.** §8 (P-9-ROME spec); §2.9 (structural rationale; sibling site discipline).

### §5.8 C-S218-4 — `globals.yml` MUST be customized

> **C-S218-4.** `globals.yml` MUST be customized on a per-repo basis to point `STATS_DIR` (and `HPARAMS_DIR` / `RESULTS_DIR` / `DATA_DIR` for completeness) at absolute NV-anchored paths matching the project's covariance cache directory layout. Cwd-relative defaults (`STATS_DIR='data/stats'`) MUST NOT be left in place for offline cache-hit dispatch. v0.2 codifies this as the CONFIG_LAYER patch class distinct from SOURCE_LAYER.

**Application scope.** Any session executing ROME edit dispatch against the project's NV-resident covariance cache. The customization is performed at session-entry environment setup (typically Cell 8 initial diagnostic phase or as part of pod-image bake-out), BEFORE first import of `util.globals`.

**Empirical anchor.** S2.18 Cell 8 initial attempt diagnostic phase (pre-customization) traced the OOM root cause to the cwd-relative `STATS_DIR`; Cell 8 retry success post-customization (cache HIT at L4).

**Cross-reference.** §1.6, §9 (`globals.yml` spec).

### §5.9 C-S218-5 — `ROMEHyperParams` dataclass extension

> **C-S218-5.** `ROMEHyperParams` dataclass extension is REQUIRED to propagate `mom2_batch_tokens` to the `compute_u` call site via `getattr`. Either (a) subclass (`ROMEHyperParamsExtended` with `mom2_batch_tokens` field added) or (b) post-instantiation attribute assignment is acceptable. The upstream 19-field dataclass schema (verified count at S2.18 Cell 4) does not include this MEMIT-extended field.

**Application scope.** Any session executing ROME edit dispatch on a base model with `max_position_embeddings > 8192` requiring `batch_tokens=100` propagation per C-S26-1 carry-forward.

**Empirical anchor.** S2.18 Cell 4 forensic surfacing of the 19-field schema (via dataclass reflection); Cell 9 first attempt construction of `ROMEHyperParamsExtended` subclass with `mom2_batch_tokens=100` field; Cell 9 dispatch success post-extension.

**Recommended pattern (per S2.18 implementation).** The subclass pattern is preferred over post-instantiation attribute assignment because:
1. Subclassing preserves the dataclass `__init__` semantics (field validation, default-value handling, repr discipline)
2. Subclass identity is preserved in `isinstance(hparams, ROMEHyperParams)` checks (subclass is a subtype)
3. Subclassing surfaces the field as a typed attribute in the IDE / static analyzer

```python
from dataclasses import dataclass, field
from rome.rome_hparams import ROMEHyperParams

@dataclass
class ROMEHyperParamsExtended(ROMEHyperParams):
    mom2_batch_tokens: int = 100  # default per C-S26-1 LLaMA-family threshold
```

**Cross-reference.** §6 (P-7-ROME compute_u call site); `t2_rome_runbook.md` v0.2 Cell 4 (hparam construction).

---

## §6 Patch P-7-ROME — `rome/compute_u.py` `get_inv_cov` body — `batch_tokens` propagation to `layer_stats`

### §6.1 Target file

```
{ROME_ROOT}/rome/compute_u.py    (three surgical edits: signature, layer_stats call, compute_u call site)
```

Line numbers are nominal at SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04` and may drift across SHA shifts. The verification block (§6.5) locates each edit by anchored substring match, not by line number.

P-7-ROME is the ROME-side analog of P-7 (MEMIT, `memit-patches-canonical.md` v2.5 §3.8). The two patches address the same defect class (cache-compute and edit-time `batch_tokens` asymmetry producing cache-filename mismatch) on parallel files in parallel dispatch chains. The structural homology is exact; the file-and-function names differ.

### §6.2 Application condition

| Operating environment | Apply P-7-ROME? |
|---|---|
| Stage 1 RunPod RTX 4090 + Llama-3.1-8B (`npos=131072`) | **Required** — load-bearing for ROME edit dispatch on cache-resident covariance matrices per C-S218-1 |
| Any environment with `max_position_embeddings > 8192` and a cached covariance computed via `batch_tokens=100` | **Required** |
| Any environment with a base model where `max_position_embeddings ≤ 8192` (e.g., GPT-J `npos=2048`) AND no cached covariance | **Optional** — patch is universal-safe (architectural-threshold dispatch resolves `mom2_batch_tokens=None` on short-context base; `layer_stats` runs default branch; cache filename form unchanged from upstream) |

For Stage 1, **P-7-ROME is REQUIRED**. Without P-7-ROME, ROME's edit-time `get_inv_cov` → `layer_stats` chain on Llama-3.1-8B constructs cache-lookup filenames lacking the `_t100_` segment that the canonical pre-S2.6 fork-work cache files carry (per IC-PreS26-2). The lookup misses; `layer_stats` falls back to local compute; the local compute attempts `causal_mask` allocation at `npos=131072` (~22.81 GiB at fp16), exceeding RTX 4090 24 GiB VRAM with model resident.

### §6.3 Pattern (3 surgical edits)

#### §6.3.1 Edit 1 — `get_inv_cov` signature gains `mom2_batch_tokens` parameter

**Pre-state (upstream pristine):**

```python
def get_inv_cov(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    layer_name: str,
    mom2_dataset: str,
    mom2_n_samples: str,
    mom2_dtype: str,
) -> torch.Tensor:
```

**Post-P-7-ROME state:**

```python
def get_inv_cov(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    layer_name: str,
    mom2_dataset: str,
    mom2_n_samples: str,
    mom2_dtype: str,
    mom2_batch_tokens: int = None,  # P-7-ROME: thread batch_tokens through to layer_stats
) -> torch.Tensor:
```

The new parameter `mom2_batch_tokens: int = None` defaults to `None` for backward-compatibility (call sites that don't propagate the kwarg get the upstream behavior). The trailing comment `# P-7-ROME: thread batch_tokens through to layer_stats` is the canonical idempotency marker for Edit 1.

#### §6.3.2 Edit 2 — `layer_stats` call inside `get_inv_cov` gains `batch_tokens` kwarg

**Pre-state (upstream pristine):**

```python
        stat = layer_stats(
            model, tok, layer_name, STATS_DIR, mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
        )
```

**Post-P-7-ROME state:**

```python
        stat = layer_stats(
            model, tok, layer_name, STATS_DIR, mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            batch_tokens=mom2_batch_tokens,  # P-7-ROME: thread batch_tokens
        )
```

The `batch_tokens=mom2_batch_tokens` kwarg is added as the trailing kwarg in the call; the trailing comment is the idempotency marker for Edit 2.

#### §6.3.3 Edit 3 — `compute_u` call site of `get_inv_cov` passes `hparams.mom2_batch_tokens` via `getattr`

**Pre-state (upstream pristine):**

```python
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
        ) @ u.unsqueeze(1)
```

**Post-P-7-ROME state (note: the `.to(u.dtype)` cast at the matmul is added by P-8-ROME — see §7 — and is shown here in its final form for reference):**

```python
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME
        ).to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME
```

The `getattr(hparams, "mom2_batch_tokens", None)` access is **load-bearing** for backward-compatibility: if `hparams` is a vanilla `ROMEHyperParams` (no `mom2_batch_tokens` field per C-S218-5 forensic surfacing), `getattr` resolves to the default `None` and the dispatch falls through to the upstream behavior; if `hparams` is `ROMEHyperParamsExtended` (or any subclass that adds the field), the customized value (e.g., `100` for Llama-3.1-8B) is propagated. The trailing comment `# P-7-ROME` is the idempotency marker for Edit 3.

### §6.4 Per-substitution map

| # | Edit | Anchor (pre-state, abridged) | Replacement (post-state, abridged) | Idempotency marker |
|---|---|---|---|---|
| 1 | `get_inv_cov` signature | `mom2_dtype: str,\n) -> torch.Tensor:` | `mom2_dtype: str,\n    mom2_batch_tokens: int = None,  # P-7-ROME: thread batch_tokens through to layer_stats\n) -> torch.Tensor:` | substring `mom2_batch_tokens: int = None` (uniquely identifying — does not appear elsewhere in `compute_u.py`) |
| 2 | `layer_stats` call | `precision=mom2_dtype,\n        )` | `precision=mom2_dtype,\n            batch_tokens=mom2_batch_tokens,  # P-7-ROME: thread batch_tokens\n        )` | substring `batch_tokens=mom2_batch_tokens,  # P-7-ROME` |
| 3 | `compute_u` call site | `hparams.mom2_dtype,\n        ) @ u.unsqueeze(1)` | `hparams.mom2_dtype,\n            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME\n        ) @ u.unsqueeze(1)` (P-8-ROME adds the `.to(u.dtype)` cast — see §7) | substring `mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None)` |

### §6.5 Verification

Post-application source verification per C-ROME-4 + C-S28-1:

```python
# Verification block (Cell 2 of t2_rome_runbook.md v0.2)
compute_u_path = Path(ROME_ROOT) / "rome" / "compute_u.py"
compute_u_src = compute_u_path.read_text()

# P-7-ROME Edit 1: signature
assert "mom2_batch_tokens: int = None" in compute_u_src, "P-7-ROME Edit 1 missing — get_inv_cov signature does not carry mom2_batch_tokens parameter"

# P-7-ROME Edit 2: layer_stats call
assert "batch_tokens=mom2_batch_tokens,  # P-7-ROME" in compute_u_src, "P-7-ROME Edit 2 missing — layer_stats call inside get_inv_cov does not thread mom2_batch_tokens"

# P-7-ROME Edit 3: compute_u call site
assert 'mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None)' in compute_u_src, "P-7-ROME Edit 3 missing — compute_u call site does not propagate hparams.mom2_batch_tokens via getattr"
```

All three assertions MUST pass at Cell 2 verification. Empirical anchor at S2.18 Cell 8 retry (smoke layer L4) + Cell 9 (L17 dispatch) + Cell 11 (L2 dispatch).

### §6.6 Discovery provenance

P-7-ROME was authored mid-session at S2.18 Cell 8 initial OOM diagnostic phase. The 22.81 GiB allocation request error trace pointed to `causal_mask.clone()` inside `layer_stats`'s local-compute fallback path. Operator-side trace inspection of `rome/compute_u.py` surfaced that `get_inv_cov` → `layer_stats` did not propagate `batch_tokens`. The MEMIT-side analog P-7 (already canonical) was the structural template; P-7-ROME applied the same threading pattern to the ROME-side function. The 3-edit surgical scope (signature + call + caller) was authored by direct analogy to P-7's 3-edit scope. Cell 8 retry confirmed the patch closure (cache HIT at smoke layer L4 in 2.35s, comparable to MEMIT R1.3 anchor of 2.72s).

---

## §7 Patch P-8-ROME — `rome/compute_u.py` `compute_u` matmul precision coercion

### §7.1 Target file

```
{ROME_ROOT}/rome/compute_u.py    (one surgical edit: .to(u.dtype) cast at matmul site)
```

P-8-ROME is **applied at the same call site as P-7-ROME Edit 3**. The two patches modify the same line (the `compute_u` call to `get_inv_cov`) but at structurally distinct surfaces: P-7-ROME adds the `mom2_batch_tokens` kwarg to the `get_inv_cov` call; P-8-ROME adds the `.to(u.dtype)` cast on the return value of `get_inv_cov` before the `@` matmul. P-8-ROME is order-dependent on P-7-ROME (P-7-ROME first, then P-8-ROME).

### §7.2 Application condition

| Operating environment | Apply P-8-ROME? |
|---|---|
| Any base model loaded in fp16 (or any non-fp32 dtype) | **Required** |
| Any base model loaded in fp32 (e.g., GPT-J default at `kmeng01/rome` development time) | **Optional** — runtime no-op (`u.dtype == torch.float32 == inv_cov.dtype`; the `.to(u.dtype)` cast is a self-cast) |

For Stage 1 (Llama-3.1-8B fp16), **P-8-ROME is REQUIRED**.

### §7.3 Pattern (1 surgical edit)

**Pre-state (post-P-7-ROME):**

```python
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME
        ) @ u.unsqueeze(1)
```

**Post-P-8-ROME state:**

```python
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME
        ).to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME: precision coercion at matmul
```

The single-character-class change is the addition of `.to(u.dtype)` (12 characters including the leading dot) immediately after the `get_inv_cov(...)` call's closing parenthesis and before the `@` operator. The trailing comment `# P-8-ROME: precision coercion at matmul` is the idempotency marker.

### §7.4 Per-substitution map

| # | Edit | Anchor (pre-state, abridged) | Replacement (post-state, abridged) | Idempotency marker |
|---|---|---|---|---|
| 1 | matmul site | `mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME\n        ) @ u.unsqueeze(1)` | `mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME\n        ).to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME: precision coercion at matmul` | substring `.to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME` (uniquely identifying) |

### §7.5 Rationale

`get_inv_cov` returns `torch.inverse(stat.mom2.moment().to("cuda")).float()` — the `.float()` cast at upstream `compute_u.py` line 53 forces fp32 for numerical stability of the inverse. The local variable `u = cur_repr` is extracted from the fp16 model's hidden states earlier in `compute_u`'s body and inherits the model's dtype (fp16 on Llama-3.1-8B fp16). PyTorch's `@` operator requires matching operand dtypes; the mismatch fires `RuntimeError` at the matmul.

**Numerical implication.** Casting `inv_cov` from fp32 → fp16 at use-time loses precision in the inverse covariance (the inverse computation itself remains fp32; only the use-time downstream propagation is fp16). The resulting `u` vector has fp16 precision anyway downstream — compute_v's optimization buffer is fp32, but compute_v takes `u` as fp16 and produces a fp32 right_vector via Adam. Net usable precision is unchanged. The alternative (cast `u` fp16 → fp32, do matmul in fp32, downcast result) is more invasive and produces equivalent numerical results.

**Why `.to(u.dtype)` rather than `.to(torch.float16)`?** The hardcoded cast would be ROME-on-Llama-3.1-8B-fp16-specific. The dtype-introspecting cast `.to(u.dtype)` is portable across base-model dtypes — runtime no-op on fp32 models, fp16-cast on fp16 models, bf16-cast on bf16 models. This is the minimum-invasive form.

**MEMIT-side analog status.** **NO MEMIT analog needed.** MEMIT bypasses `rome/compute_u.py` entirely; the latent precision-coercion defect in upstream `kmeng01/rome` was never observed in MEMIT-only sessions because MEMIT never executes this code path.

### §7.6 Verification

```python
# Verification block (Cell 2 of t2_rome_runbook.md v0.2)
assert ".to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME" in compute_u_src, "P-8-ROME missing — compute_u matmul does not carry .to(u.dtype) cast"
```

Empirical anchor at S2.18 Cell 9 first attempt (post-P-8-ROME application; matmul completed without RuntimeError; compute_v iteration trace produced).

### §7.7 Discovery provenance

P-8-ROME was authored mid-session at S2.18 Cell 9 first attempt (post-P-7-ROME). The first attempt produced `RuntimeError: Expected size for first two dimensions of batch2 tensor to be: ... but got: ...` at the matmul site (the dtype-mismatch RuntimeError for `@` reports as a "size" error in older PyTorch versions). Operator-side trace inspection surfaced the fp32 inv_cov vs fp16 cur_repr mismatch. The minimum-invasive cast `.to(u.dtype)` was authored as a 12-character addition; Cell 9 first attempt re-ran successfully post-patch (compute_v converged to ceiling P=1.06e-02 — the FAIL outcome was verdict-class, not dispatch-class).

---

## §8 Patch P-9-ROME — `rome/rome_main.py` outer-product precision coercion (sibling sites)

### §8.1 Target file

```
{ROME_ROOT}/rome/rome_main.py    (two surgical edits: execute_rome line 117 + apply_rome_to_model line 43; both outer-product sites)
```

P-9-ROME is **structurally distinct from P-7-ROME and P-8-ROME** — it targets a different file (`rome_main.py` vs `compute_u.py`) and addresses a different precision-coercion surface (outer-product vs matmul). The two call sites in `rome_main.py` carry the same defect pattern; the patch applies symmetrically to both to prevent latent regression at the unpatched site under future multi-fact dispatch refactors.

### §8.2 Application condition

| Operating environment | Apply P-9-ROME? |
|---|---|
| Any base model loaded in fp16 (or any non-fp32 dtype) | **Required** |
| Any base model loaded in fp32 | **Optional** — runtime no-op (all operands fp32; the `.to(weight.dtype)` casts are self-casts) |

For Stage 1 (Llama-3.1-8B fp16), **P-9-ROME is REQUIRED**.

### §8.3 Pattern (2 surgical edits)

#### §8.3.1 Edit 1 — `execute_rome` line 117 outer-product

**Pre-state (upstream pristine):**

```python
        with torch.no_grad():
            weight_name = f"{hparams.rewrite_module_tmp.format(layer)}.weight"
            upd_matrix = left_vector.unsqueeze(1) @ right_vector.unsqueeze(0)
            upd_matrix = upd_matrix_match_shape(upd_matrix, weights[weight_name].shape)
```

**Post-P-9-ROME state:**

```python
        with torch.no_grad():
            weight_name = f"{hparams.rewrite_module_tmp.format(layer)}.weight"
            # P-9-ROME: precision coercion — left_vector (fp16 post-P-8-ROME) vs right_vector (fp32 from compute_v Adam)
            upd_matrix = left_vector.unsqueeze(1).to(weights[weight_name].dtype) @ right_vector.unsqueeze(0).to(weights[weight_name].dtype)
            upd_matrix = upd_matrix_match_shape(upd_matrix, weights[weight_name].shape)
```

The outer-product expression gains two `.to(weights[weight_name].dtype)` casts (one per operand). The leading comment `# P-9-ROME: precision coercion ...` is the idempotency marker for Edit 1.

#### §8.3.2 Edit 2 — `apply_rome_to_model` line 43 outer-product (sibling site)

**Pre-state (upstream pristine):**

```python
    for i, request in enumerate(requests):
        deltas = execute_rome(model, tok, request, hparams)
        with torch.no_grad():
            for w_name, (delta_u, delta_v) in deltas.items():
                upd_matrix = delta_u.unsqueeze(1) @ delta_v.unsqueeze(0)
                w = nethook.get_parameter(model, w_name)
                upd_matrix = upd_matrix_match_shape(upd_matrix, w.shape)
```

**Post-P-9-ROME state:**

```python
    for i, request in enumerate(requests):
        deltas = execute_rome(model, tok, request, hparams)
        with torch.no_grad():
            for w_name, (delta_u, delta_v) in deltas.items():
                # P-9-ROME: precision coercion at outer-product (delta_u fp16 vs delta_v fp32)
                w = nethook.get_parameter(model, w_name)
                upd_matrix = delta_u.unsqueeze(1).to(w.dtype) @ delta_v.unsqueeze(0).to(w.dtype)
                upd_matrix = upd_matrix_match_shape(upd_matrix, w.shape)
```

Note: the `w = nethook.get_parameter(model, w_name)` line is **moved up** by one line in the post-patch state to make `w.dtype` available for the outer-product casts. The original site computed `upd_matrix` first, then bound `w`; the post-patch site binds `w` first to enable the dtype reference. The leading comment `# P-9-ROME: precision coercion at outer-product (delta_u fp16 vs delta_v fp32)` is the idempotency marker for Edit 2.

### §8.4 Per-substitution map

| # | Edit | Anchor (pre-state, abridged) | Replacement (post-state, abridged) | Idempotency marker |
|---|---|---|---|---|
| 1 | `execute_rome` line 117 | `upd_matrix = left_vector.unsqueeze(1) @ right_vector.unsqueeze(0)` | `# P-9-ROME: precision coercion — left_vector (fp16 post-P-8-ROME) vs right_vector (fp32 from compute_v Adam)\n            upd_matrix = left_vector.unsqueeze(1).to(weights[weight_name].dtype) @ right_vector.unsqueeze(0).to(weights[weight_name].dtype)` | substring `.to(weights[weight_name].dtype) @ right_vector.unsqueeze(0).to(weights[weight_name].dtype)` |
| 2 | `apply_rome_to_model` line 43 | `upd_matrix = delta_u.unsqueeze(1) @ delta_v.unsqueeze(0)\n                w = nethook.get_parameter(model, w_name)` | `# P-9-ROME: precision coercion at outer-product (delta_u fp16 vs delta_v fp32)\n                w = nethook.get_parameter(model, w_name)\n                upd_matrix = delta_u.unsqueeze(1).to(w.dtype) @ delta_v.unsqueeze(0).to(w.dtype)` | substring `delta_u.unsqueeze(1).to(w.dtype) @ delta_v.unsqueeze(0).to(w.dtype)` |

### §8.5 Rationale

ROME's edit-time mechanism produces a rank-1 update via outer product `left_vector @ right_vector.T` where `left_vector` is the unit-direction key (the "where to write" direction in MLP-input space) and `right_vector` is the magnitude-and-direction value (the "what to write" vector in MLP-output space).

- **`left_vector` dtype:** fp16 (on Llama-3.1-8B fp16 base) — output of `compute_u` post-P-8-ROME (which casts the inv_cov-multiplied vector to `u.dtype` at the matmul, producing fp16 output)
- **`right_vector` dtype:** fp32 (always) — output of `compute_v`'s Adam optimization buffer. Adam runs on fp32 `delta` parameter regardless of base model dtype (per upstream `compute_v.py` `nn.Parameter(torch.zeros(model.config.hidden_size, requires_grad=True))` initialization which defaults to fp32; the optimization is fp32-on-fp32 throughout)

The outer-product `fp16 @ fp32` mismatches at the `@` operator. Both call sites carry the same pattern; patching one without the other leaves the unpatched site latent.

**Why cast to `weight.dtype` rather than fp16 hardcoded?** The cast target tracks the model's dtype dynamically — the `weights[weight_name].dtype` (Edit 1) and `w.dtype` (Edit 2) refer to the actual target weight matrix's dtype, which is the model's dtype. This makes the patch portable: fp32 model → no-op cast (self-cast), fp16 model → fp16 cast, bf16 model → bf16 cast. The same patch source operates correctly across all three regimes.

**Numerical implication.** The fp32 right_vector is downcast to fp16 (or bf16) at the outer-product, losing some precision in the magnitude direction. The downstream consumption is the in-place weight update `weights[weight_name] += upd_matrix`, which operates entirely in `weight.dtype` — the precision loss at the cast is the precision the weight matrix carries anyway. Net usable precision is unchanged.

**MEMIT-side analog status.** **NO MEMIT analog needed.** MEMIT bypasses `rome/rome_main.py` entirely; MEMIT's own outer-product surface in `memit/memit_main.py:execute_memit` carries the same pattern but is a separate file. If MEMIT ever surfaces an analogous defect on a fp16 base model under specific dispatch conditions, a parallel patch (P-X for some integer X) would be authored on the MEMIT-side.

### §8.6 Sibling-site discipline (load-bearing for v0.2)

Both call sites carry the same outer-product pattern. **Patching one site without the other is INSUFFICIENT.**

- `execute_rome` is called by `apply_rome_to_model` (which iterates over requests and calls `execute_rome` once per request). At single-fact dispatch (per C-ROME-1), `execute_rome` is called once per `apply_rome_to_model` invocation; the `apply_rome_to_model` outer-product loop body iterates over `deltas.items()` (which has length 1 for single-layer ROME — only the rewrite layer is updated).
- At v0.2 single-fact single-layer dispatch, only the `execute_rome` site (Edit 1) is exercised at runtime. The `apply_rome_to_model` site (Edit 2) is dormant.
- **However**, future ROME refactor adding multi-fact dispatch through `apply_rome_to_model`'s `for i, request in enumerate(requests):` loop with `len(requests) > 1` would exercise the `apply_rome_to_model` site under fp16 conditions. If only Edit 1 is applied, the latent defect at Edit 2 fires at the future refactor's first multi-fact dispatch.

P-9-ROME applies symmetrically to both sites at v0.2 to prevent this latent regression. Sibling-site discipline is codified as a v0.2 process constraint.

### §8.7 Verification

```python
# Verification block (Cell 2 of t2_rome_runbook.md v0.2)
rome_main_path = Path(ROME_ROOT) / "rome" / "rome_main.py"
rome_main_src = rome_main_path.read_text()

# P-9-ROME Edit 1: execute_rome
assert ".to(weights[weight_name].dtype) @ right_vector.unsqueeze(0).to(weights[weight_name].dtype)" in rome_main_src, "P-9-ROME Edit 1 missing — execute_rome outer-product does not carry .to(weights[weight_name].dtype) casts"

# P-9-ROME Edit 2: apply_rome_to_model
assert "delta_u.unsqueeze(1).to(w.dtype) @ delta_v.unsqueeze(0).to(w.dtype)" in rome_main_src, "P-9-ROME Edit 2 missing — apply_rome_to_model outer-product does not carry .to(w.dtype) casts"

# Idempotency marker count check (P-9-ROME comment markers should appear at least twice — once per site)
assert rome_main_src.count("P-9-ROME") >= 2, "P-9-ROME comment markers count < 2; sibling-site discipline violated"
```

Empirical anchor at S2.18 Cell 9 second attempt (post-P-9-ROME application; outer-product completed without RuntimeError; rank-1 update applied to weights).

### §8.8 Discovery provenance

P-9-ROME was authored mid-session at S2.18 Cell 9 second attempt (post-P-8-ROME). The second attempt produced `RuntimeError: ...` at the outer-product immediately after compute_v completed (compute_v ran to its 20-iter ceiling; the failure was at the post-compute_v outer-product site, not within compute_v itself). Operator-side trace inspection surfaced the fp16 left_vector vs fp32 right_vector mismatch at `execute_rome` line 117. The sibling site at `apply_rome_to_model` line 43 was identified by direct code inspection (same outer-product pattern; same operand dtypes by structural analysis). Both sites patched symmetrically; Cell 9 second attempt re-ran successfully (verdict produced — the FAIL was consistency-class at this point, not dispatch-class).

---

## §9 Patch `globals.yml` — CONFIG_LAYER STATS_DIR customization

### §9.1 Target file

```
{ROME_ROOT}/rome/globals.yml    (in-place rewrite of the 5-field YAML body)
```

`globals.yml` is **NOT a Python source file** — it is a YAML configuration file consumed by `util/globals.py` at first-import. The patch class is CONFIG_LAYER (per §1.0) — distinct from SOURCE_LAYER patches in application semantics: applied at session-entry environment setup (typically as part of pod-image bake-out or as part of Cell 8 initial diagnostic phase), BEFORE first import of `util.globals`.

### §9.2 Application condition

| Operating environment | Apply `globals.yml` customization? |
|---|---|
| Project-resident NV cache at absolute path (e.g., `/workspace/covariance_caches`) | **Required** |
| ROME repo cloned to `/workspace/rome_dry_run/rome/` and run with `os.chdir(ROME_ROOT)` discipline | **Required** if NV cache path differs from `<ROME_ROOT>/data/stats` |
| ROME repo run from a directory where the cwd-relative default `data/stats` does match the desired cache path | **Optional** — runtime no-op (the cwd-relative default resolves to the desired path) |

For Stage 1 RunPod RTX 4090 with NV cache at `/workspace/covariance_caches` and ROME repo at `/workspace/rome_dry_run/rome/`, **the customization is REQUIRED**.

### §9.3 Pattern (in-place rewrite)

#### §9.3.1 Pre-state (upstream pristine)

```yaml
---
  RESULTS_DIR: "results"
  DATA_DIR: "data"
  STATS_DIR: "data/stats"
  HPARAMS_DIR: "hparams"
  REMOTE_ROOT_URL: "https://rome.baulab.info"
```

(216 bytes; cwd-relative defaults; pristine SHA prefix `5447f92b74ac0759`)

#### §9.3.2 Post-state (S2.18 customization)

```yaml
# ROME-side globals.yml — S2.18 customization
# Authored: 2026-05-05T<UTC>
# v0.2 patches doc finding: config-layer patch class
# Pristine ROME upstream values preserved at globals.yml.upstream_pristine for forensic record.

STATS_DIR: /workspace/covariance_caches
HPARAMS_DIR: /workspace/rome_dry_run/rome/hparams
RESULTS_DIR: /workspace/rome_dry_run/results
DATA_DIR: /workspace/rome_dry_run/data
REMOTE_ROOT_URL: https://rome.baulab.info
```

(post-customization SHA prefix `6c540955dd62d50a`; ~1100 bytes including header comments)

The four path fields are absolute-anchored to `/workspace/...` (the NV mount point on RunPod pods); `REMOTE_ROOT_URL` is preserved unchanged from upstream. The leading comment header documents the patch authoring context (authored date, session label, pristine sibling reference) for forensic transparency.

### §9.4 Per-field customization map

| Field | Upstream pristine | Post-customization | Rationale |
|---|---|---|---|
| `STATS_DIR` | `"data/stats"` (cwd-relative) | `/workspace/covariance_caches` (absolute NV-anchored) | Load-bearing — `STATS_DIR` is consumed by `rome/layer_stats.py` for cache-resolution. The project's NV-resident covariance cache is at `/workspace/covariance_caches`; cwd-relative `data/stats` resolves to `/workspace/rome_dry_run/rome/data/stats` which does not contain the cache files |
| `HPARAMS_DIR` | `"hparams"` (cwd-relative) | `/workspace/rome_dry_run/rome/hparams` (absolute NV-anchored) | Companion path; absoluteness preserves intent across cwd shifts (e.g., kernel restarts, notebook directory changes) |
| `RESULTS_DIR` | `"results"` (cwd-relative) | `/workspace/rome_dry_run/results` (absolute) | Companion; not exercised at S2.18 (results were written to `/workspace/t2_rome_sect/` per runbook design) but patched for completeness |
| `DATA_DIR` | `"data"` (cwd-relative) | `/workspace/rome_dry_run/data` (absolute) | Companion; not exercised at S2.18 |
| `REMOTE_ROOT_URL` | `"https://rome.baulab.info"` | `https://rome.baulab.info` (unchanged) | Preserved — this is the upstream cache pre-compute distribution endpoint; the project does NOT consume from this URL (per C-S26-1 + C-S218-1 cache-locality discipline) but the field is preserved for upstream-compat |

**Note on `KV_DIR` absence (carried from §1.6 schema divergence note).** ROME's `globals.yml` has 5 fields. MEMIT's `globals.yml` adds a 6th field (`KV_DIR`). The MEMIT extension is a structural difference between the two repositories. The v0.2 ROME-side customization preserves the 5-field schema; `KV_DIR` is NOT added.

### §9.5 Application semantics

**Application order:** CONFIG_LAYER patches MUST be applied BEFORE first import of `util.globals`. In practice, this means:

1. Pristine `globals.yml` is preserved at `globals.yml.upstream_pristine` (backup-and-write pattern)
2. Customized `globals.yml` is written in-place at the canonical path
3. First import of `util.globals` (transitively triggered by any `from util.globals import STATS_DIR` or similar in `rome/layer_stats.py`, `rome/compute_u.py`, etc.) reads the customized values
4. After first import, `util.globals.STATS_DIR` is bound to the customized value for the kernel lifetime

**Idempotency.** The customization is idempotent at the file-write level — re-applying the same customization to an already-customized `globals.yml` produces a no-op. However, the post-import state (`util.globals.STATS_DIR` bound at import time) is NOT idempotent across kernel restarts: if the customization is reverted between imports, a kernel restart is required to re-bind `util.globals` to the new values.

**Pristine sibling discipline.** The pristine `globals.yml.upstream_pristine` MUST be preserved alongside the customized file to enable forensic diff-and-audit (per §1.1 transplant discipline carry-forward).

### §9.6 Verification

```python
# Verification block (Cell 8 initial diagnostic phase of t2_rome_runbook.md v0.2 — pre-import gate)
import yaml
globals_yml_path = Path(ROME_ROOT) / "globals.yml"
globals_data = yaml.safe_load(globals_yml_path.read_text())

# Customization marker: STATS_DIR must be absolute and point at the project's NV cache
assert globals_data["STATS_DIR"].startswith("/workspace/"), f"globals.yml STATS_DIR not customized — value is {globals_data['STATS_DIR']!r}"
assert "covariance_caches" in globals_data["STATS_DIR"], f"globals.yml STATS_DIR does not anchor at covariance_caches — value is {globals_data['STATS_DIR']!r}"

# Pristine sibling discipline
pristine_path = Path(ROME_ROOT) / "globals.yml.upstream_pristine"
assert pristine_path.exists(), "globals.yml.upstream_pristine missing — pristine sibling discipline violated"
```

Empirical anchor at S2.18 Cell 8 retry (post-`globals.yml` customization + post-P-7-ROME application; cache HIT confirmed at smoke layer L4 in 2.35s).

### §9.7 Discovery provenance

The `globals.yml` defect path was surfaced at S2.18 Cell 8 initial OOM diagnostic phase. After the OOM error (22.81 GiB allocation request), operator-side trace inspection of the `_mom2_100000.npz` filename (no `_t100_` segment) initially pointed to P-7-ROME (the cache-filename mismatch from missing `batch_tokens` propagation). A subsequent inspection of `util/globals.py`'s import path surfaced that `STATS_DIR` was reading the cwd-relative default `data/stats` rather than the project's NV cache directory. The defect was the conjunction of two factors: (a) missing `batch_tokens` in `get_inv_cov` (closed by P-7-ROME) AND (b) wrong `STATS_DIR` path (closed by `globals.yml` customization). Either alone would not produce cache HIT; both fixes were required jointly. The CONFIG_LAYER patch class was introduced at v0.2 to formalize the structural distinction.

---

## §10 Application order

The v0.2 ROME patches application order at runbook v0.2 Cell 2 (or as part of pod-image bake-out preparatory to Cell 0) is:

```
CONFIG_LAYER (apply before any util.globals import):
  1. globals.yml customization (per §9; backup pristine to globals.yml.upstream_pristine)

SOURCE_LAYER transplants (apply at session entry; backup pristine to *.upstream_pristine):
  2. Transplant util/nethook.py from MEMIT-side post-state (carries P-1 + P-2)
  3. Transplant rome/compute_v.py from MEMIT-side post-state (carries P-4)
  4. Transplant rome/layer_stats.py from MEMIT-side post-state (carries P-4 + P-5 + P-6)

SOURCE_LAYER ROME-fresh patches (apply post-transplant; idempotent):
  5. P-7-ROME on rome/compute_u.py (3 surgical edits per §6)
  6. P-8-ROME on rome/compute_u.py (1 surgical edit per §7; order-dependent on P-7-ROME)
  7. P-9-ROME on rome/rome_main.py (2 surgical edits per §8; both sites)

Runtime patches (apply at kernel session — not source-level):
  8. Pad-Token alias at Cell 5 model load (per §1.1; tokenizer-level)
  9. Copy-Unmount mechanism at Cell 9 / Cell 11 trial fn body (per §1.2; runtime tensor restore)

Verification (Cell 2 of runbook):
  All SOURCE_LAYER + CONFIG_LAYER markers verified per §6.5 / §7.6 / §8.7 / §9.6
```

### §10.1 Application order rationale

- **CONFIG_LAYER first (Step 1):** `util.globals` is imported transitively by `rome/layer_stats.py` and `rome/compute_u.py`. The customized `STATS_DIR` must be in place before any source file using it is loaded.
- **Transplants before fresh patches (Steps 2-4 then 5-7):** P-7-ROME / P-8-ROME modify `rome/compute_u.py`, which is NOT transplanted (the upstream pristine `compute_u.py` is preserved as the patch base). P-9-ROME modifies `rome/rome_main.py`, also NOT transplanted. The transplant set covers files that have shared MEMIT-side patches (P-1/2/4/5/6); the fresh patch set covers files that are ROME-only (no MEMIT-side analog to transplant).
- **P-7-ROME before P-8-ROME (Steps 5-6):** P-8-ROME modifies the same line as P-7-ROME Edit 3. P-8-ROME is order-dependent on P-7-ROME's `mom2_batch_tokens=getattr(...)` kwarg already being present at that line.
- **P-9-ROME independent of P-7-ROME / P-8-ROME (Step 7):** P-9-ROME modifies a different file (`rome_main.py`); it is order-independent of the `compute_u.py` patches.
- **Runtime patches last (Steps 8-9):** Pad-Token alias and Copy-Unmount are applied at session execution time, not at source-patching time. They are listed for completeness but are operationally distinct from the source-level Steps 1-7.

---

## §11 Manifest schema for `t2_rome_patch_state.json`

Cell 2 of `t2_rome_runbook.md` v0.2 emits a structured patch state manifest at `/workspace/architecture_profile/t2_rome_patch_state.json` with the v0.2 schema (extended from v0.1 for the new patches and CONFIG_LAYER class):

```json
{
  "captured_at": "<ISO-8601 UTC>",
  "rome_sha": "0874014cd9837e4365f3e6f3c71400ef11509e04",
  "patches_doc_version": "v0.2",
  "patches_verified_source_layer": {
    "rome_nethook_p1_signature_and_inputs_synthesis": true,
    "rome_nethook_p2_with_kwargs_registration": true,
    "rome_compute_v_p4_hidden_size": true,
    "rome_layer_stats_p4_max_position_embeddings": true,
    "rome_layer_stats_p5_dataset_modernization": true,
    "rome_layer_stats_p6_fstring_post_form": true,
    "rome_compute_u_p7_rome_get_inv_cov_batch_tokens_signature": true,
    "rome_compute_u_p7_rome_layer_stats_call_kwarg": true,
    "rome_compute_u_p7_rome_compute_u_call_site_getattr": true,
    "rome_compute_u_p8_rome_to_u_dtype_matmul_cast": true,
    "rome_main_p9_rome_execute_rome_outer_product_cast": true,
    "rome_main_p9_rome_apply_rome_to_model_outer_product_cast": true,
    "tokenizer_pad_token_alias": false,
    "copy_unmount_in_place_restore": false
  },
  "patches_verified_config_layer": {
    "globals_yml_stats_dir_absolute_nv_anchored": true,
    "globals_yml_upstream_pristine_sibling_present": true
  },
  "patches_inapplicable": [
    "rome_p3_prime_cpu_offload",
    "rome_explicit_device_map",
    "rome_main_p7_get_cov_batch_tokens_memit_only_site"
  ],
  "patches_applied_at_runtime": {
    "tokenizer_pad_token_alias": "Cell 5 (model load)",
    "copy_unmount_in_place_restore": "Cell 9 / Cell 11 (trial fn body, single-fact dispatch per C-ROME-1)"
  },
  "transplant_provenance": {
    "util/nethook.py": "transplanted from /workspace/memit_dry_run/util/nethook.py at <ISO-8601 UTC>",
    "rome/compute_v.py": "transplanted from /workspace/memit_dry_run/rome/compute_v.py at <ISO-8601 UTC>",
    "rome/layer_stats.py": "transplanted from /workspace/memit_dry_run/rome/layer_stats.py at <ISO-8601 UTC>"
  },
  "file_sha256_prefix": {
    "util/nethook.py": "<16-char SHA prefix; post-transplant>",
    "util/nethook.py.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>",
    "rome/compute_v.py": "<16-char SHA prefix; post-transplant>",
    "rome/compute_v.py.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>",
    "rome/layer_stats.py": "<16-char SHA prefix; post-transplant>",
    "rome/layer_stats.py.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>",
    "rome/compute_u.py": "<16-char SHA prefix; post-P-7-ROME + post-P-8-ROME>",
    "rome/compute_u.py.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>",
    "rome/rome_main.py": "<16-char SHA prefix; post-P-9-ROME>",
    "rome/rome_main.py.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>",
    "globals.yml": "<16-char SHA prefix; post-customization>",
    "globals.yml.upstream_pristine": "<16-char SHA prefix; pristine ROME upstream>"
  }
}
```

### §11.1 Schema delta from v0.1

- `patches_verified` split into `patches_verified_source_layer` and `patches_verified_config_layer` (CONFIG_LAYER class introduction)
- `patches_doc_version` field added (canonical v0.2 reference)
- New SOURCE_LAYER entries for P-7-ROME (3 sub-keys), P-8-ROME (1 sub-key), P-9-ROME (2 sub-keys)
- New CONFIG_LAYER entries for `globals.yml` (2 sub-keys; customization + pristine sibling)
- `patches_inapplicable` updated: P-7 entry renamed to clarify it is INAPPLICABLE TO MEMIT-SITE (the v0.1 entry was ambiguous post-§1.3 rationale revision)
- `transplant_provenance` field added (records the Cell 2 transplant operation explicitly per §1.1 discipline)
- `file_sha256_prefix` extended with `.upstream_pristine` siblings

---

## §12 Upstream notes — MEMIT canonical vs ROME canonical relationship (v0.2)

This document remains **a sibling artifact to `memit-patches-canonical.md` v2.5**, not a child or amendment. The v0.2 update is additive on the ROME side; MEMIT v2.5 is preserved unmodified.

| Item | MEMIT v2.5 | ROME v0.2 | Relationship |
|---|---|---|---|
| Target model | `meta-llama/Llama-3.1-8B` | `meta-llama/Llama-3.1-8B` | IDENTICAL |
| Target hardware | RunPod RTX 4090 24 GiB | RunPod RTX 4090 24 GiB | IDENTICAL |
| SOURCE_LAYER patches at shared files | P-1, P-2, P-4, P-5, P-6 directly applied | P-1, P-2, P-4, P-5, P-6 transplanted from MEMIT-side post-state | EQUIVALENT POST-STATE; SHARED CONCRETE SOURCE FILES POST-CELL-2 |
| MEMIT-only files | `memit/memit_main.py`, `memit/compute_z.py` | (absent) | INAPPLICABLE TO ROME (P-3', P-7) |
| ROME-only files | (absent) | `rome/rome_main.py`, `rome/compute_u.py` | UNIQUE TO ROME (P-7-ROME, P-8-ROME, P-9-ROME) |
| Covariance cache | NV `/workspace/covariance_caches/.../wikipedia_stats/` | (same NV cache; reuse-only) | SHARED CACHE; consumed by both engines |
| Process constraints | C-S26-1, C-S26-2, C-S26-3, C-S28-1 | C-ROME-1, C-ROME-2, C-ROME-3, C-ROME-4 + C-S218-1, C-S218-2, C-S218-3, C-S218-4, C-S218-5 | PARALLEL; ROME constraints inherit MEMIT structure with single-fact-dispatch narrowing + ROME-specific patch application constraints |
| CONFIG_LAYER patches | (none codified in v2.5; `globals.yml` was customized at pre-S2.6 fork-work but not codified) | `globals.yml` codified at §9; CONFIG_LAYER class introduced | NEW CLASS; ROME-side first; MEMIT-side codification deferred to hypothetical v2.6 |

**Modification discipline.** Future amendments to MEMIT canonical (e.g., a hypothetical v2.6 introducing CONFIG_LAYER class for MEMIT's `globals.yml` codification) do not propagate into ROME canonical automatically. Cross-references are explicit; co-evolution is maintained at runbook hardening sessions where applicable.

---

## §13 Non-goals

This document does NOT:

1. **Modify `memit-patches-canonical.md` v2.5.** That artifact is preserved unmodified per D-S216-CLOSE-3.
2. **Codify ROME hparam recalibration values.** §4 declares ROME paper Table 1 GPT-J reference values; recalibration was NOT explored at S2.18 (per Route A halt at Cell 13 verdict gate). Future hparam recalibration would be v0.3 scope, contingent on operator decision to revisit ROME at non-canonical hparams (currently not on the workstream roadmap; T.2 GRACE is the leading hypothesis at S2.19 routing).
3. **Reverse the T.2 ROME ELIM verdict.** That verdict is recorded in `framework_finding_memit_ceiling_archival.md` v1.1 (axis 7) and `t_branch_decision_document.md` v1.1; this v0.2 patches doc is an upstream supporting artifact, not the verdict authority.
4. **Pre-commit T.2 GRACE patches or runbook structure.** That is S2.19 scope (GRACE runbook v0.1 + grace-patches-canonical.md v0.1 authoring).
5. **Amend the v1.2 integrated framework spec.** Sealed.
6. **Authoritatively resolve the runbook-level open questions surfaced at S2.18.** Those (Cell 6 MULTI_TOKEN_ALLOWLIST canonical placement, Cell 13 verdict gate three-route adjudication framework, Cell 7 cross-session bit-exact gate canonical absorption) are runbook-doc scope (`t2_rome_runbook.md` v0.2 + `stage_1_sect_runbook.md` v1.7), not patches-doc scope.

---

## §14 References

### §14.1 Companion artifacts (concurrent v0.2 codification session)

- `t2_rome_runbook.md` v0.2 — companion runbook; consumes this canonical at Cells 1, 2, 3, 4, 8, 9, 11, 14-17
- `stage_1_sect_runbook.md` v1.7 — MEMIT-side runbook; sibling-pattern parity with t2_rome v0.2 at Cell 6 MULTI_TOKEN_ALLOWLIST absorption
- `framework_finding_memit_ceiling_archival.md` v1.1 — extends 6-axis ceiling to 7 axes (Axis 7 = S2.18 ROME ELIM at L17 + L2)
- `t_branch_decision_document.md` v1.1 — records T.2 ROME ELIM at canonical hparams; promotes T.2 GRACE to active leading hypothesis

### §14.2 Carry-forward canonical artifacts

- `memit-patches-canonical.md` v2.5 — sibling MEMIT canonical (preserved unmodified)
- `framework_finding_memit_ceiling_archival.md` v1.0 — predecessor (preserved as historical anchor; v1.1 supersedes additively)
- `t_branch_decision_document.md` v1.0 — predecessor (preserved as historical anchor; v1.1 supersedes additively)
- `cfb-v3.yaml` v1.0 — fact corpus (5 facts; instrument-cluster targets; including cfb-v3-004 multi-token allowlist per D-S215D2-CFB-V3-004-MULTITOKEN-1)
- `probe-set-v3.yaml` v1.0 — probe set (38 active probes)
- `session_2_18_summary_block.md` — canonical D / C / OQ / IC record for S2.18 empirical verdicts
- `session_2_18_summary_block_appendix.md` — forensic detail (cell-by-cell trajectory, patch authoring detail, compute_v traces, verdict surfaces)

### §14.3 Decision IDs (S2.16 / S2.17 / S2.18 / v0.2)

- D-S216-CLOSE-2 — empirical anchors carry-forward to T.2 ROME (covariance caches, cross-session bit-exact determinism, Copy-Unmount mechanism)
- D-S216-CLOSE-3 — `memit-patches-canonical.md` v2.5 preserved unmodified; ROME patches authored as parallel canonical
- D-S217-Q2-1 — ROME SHA pin = latest stable tip (resolved to `0874014c...` at S2.18 Cell 1)
- D-S217-Q3-1 — ROME canonical hparams = ROME paper Table 1 GPT-J reference values at v0.1
- D-S217-Q4-1 — Layer candidates = L17 primary + L2 secondary at HC-2-equivalent dry-run (S2.18 verdict NO_LOAD_BEARING_LAYER per D-S218-9)
- D-S217-Q5-1 — cfb-v3-004 multi-token posture = first-token-proxy carry-forward + RE-EVALUATE AT TRIAL 0 flag
- D-S218-1 through D-S218-13 — S2.18 empirical decisions (B-FAIL verdict, T.2 ROME ELIM, T.2 GRACE PROMOTED, three NEW patches RATIFIED, NEW CONFIG_LAYER patch class, cross-session bit-exact 5→6, Copy-Unmount ROME extension, Q4-1 + Q5-1 closures, v0.2 codification mandate, v1.1 archival/t-branch updates)

### §14.4 Constraint IDs (v0.2)

- C-ROME-1 (EMPIRICALLY-VALIDATED at S2.18) — Single-fact dispatch envelope
- C-ROME-2 (EMPIRICALLY-VALIDATED at S2.18) — Covariance cache reuse
- C-ROME-3 (EMPIRICALLY-VALIDATED at S2.18) — R1.3-equivalent dry-run gate
- C-ROME-4 (EMPIRICALLY-VALIDATED at S2.18) — Marker post-application verification
- C-S218-1 — P-7-ROME application REQUIRED for ROME edit dispatch on long-context base models
- C-S218-2 — P-8-ROME application REQUIRED for ROME edit dispatch on fp16 base models
- C-S218-3 — P-9-ROME application REQUIRED for ROME edit dispatch on fp16 base models (both sibling sites)
- C-S218-4 — `globals.yml` MUST be customized for absolute NV-anchored `STATS_DIR`
- C-S218-5 — `ROMEHyperParams` dataclass extension REQUIRED for `mom2_batch_tokens` propagation

### §14.5 Open questions

The v0.2 codification session anticipated three OQs (`OQ-V02-1` through `OQ-V02-3` per the v0.2 codification kickoff prompt). Their disposition at v0.2 close:

- **OQ-V02-1** (CONFIG_LAYER as separate section vs subsection): RESOLVED at v0.2 — CONFIG_LAYER is a subsection within §1 inventory (§1.6) parallel to §1.1-§1.5 SOURCE_LAYER subsections. If a hypothetical MEMIT v2.6 introduces CONFIG_LAYER class for MEMIT's `globals.yml`, both docs adopt the parallel pattern at that revision. Closure rationale: tight structural parallelism with v0.1's existing inventory shape; minimal restructuring; future-extension-compatible.
- **OQ-V02-2** (Cell 13 verdict gate three-route framework — v0.2-specific or generic stage_1_sect v1.7?): DEFERRED — this is a runbook-level question, not a patches-doc question. Routes to `t2_rome_runbook.md` v0.2 / `stage_1_sect_runbook.md` v1.7 authoring scope.
- **OQ-V02-3** (MULTI_TOKEN_ALLOWLIST canonical placement): DEFERRED — runbook-level + corpus-level question. Routes to `t2_rome_runbook.md` v0.2 / `stage_1_sect_runbook.md` v1.7 / `cfb-v3.yaml` v1.x scope.

### §14.6 Repository references

- ROME: `https://github.com/kmeng01/rome` SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04`
- ROME paper / supplementary: `https://rome.baulab.info`
- MEMIT (sibling, for reference): `https://github.com/kmeng01/memit` SHA pin `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`

---

## §15 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | v0.2 codification session (operator-side post-S2.18; pre-S2.19 BLOCKING) |
| Authoring date | 2026-05-05 |
| Document version | 0.2 |
| Iteration | v2 empirical absorption (supersedes v0.1 declarative) |
| Status | RATIFIED v0.2 — empirical applicability verdicts absorbed from S2.18 Block A + Block B; supersedes v0.1 declarative |
| Supersedes | v0.1 (RATIFIED at S2.17 Block 2; preserved as historical anchor) |
| Basis | `session_2_18_summary_block.md` (canonical D / C / OQ / IC); `session_2_18_summary_block_appendix.md` (forensic detail; load-bearing for §6 / §7 / §8 / §9 patch detail); `memit-patches-canonical.md` v2.5 (sibling-parity template); `t_branch_decision_document.md` v1.0 (T-branch methodology lock); ROME paper Table 1 (GPT-J reference) |
| Specialist provenance | memit-specialist (primary; ROME edit dispatch architecture analysis, P-7-ROME / P-8-ROME / P-9-ROME authoring rationale, INAPPLICABLE rationale revisions, v0_1_undocumented_findings); state-consistency-theorist (secondary; Copy-Unmount mechanism scope under ROME single-fact regime, IC-S23-4 empirical validation extension, IC anchor wording for cross-session bit-exact gate); framework-spec-writer (formalization) |
| Last updated | 2026-05-05 |

---

*End of ROME Patches Canonical v0.2.*
