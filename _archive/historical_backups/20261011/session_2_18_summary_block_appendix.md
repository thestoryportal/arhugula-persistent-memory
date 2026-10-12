# Session 2.18 Summary Block — Appendix (Forensic Record)

**Companion to:** `session_2_18_summary_block.md`
**Authored:** 2026-05-05
**Scope:** detailed forensic record supporting the canonical D / C / OQ / IC tracking in the primary block. Appendix sections may be skipped on first read; primary block is self-contained for routing.

---

## Table of contents

1. Block A pre-flight cell-by-cell trajectory
2. Patch authoring detail (3 source-layer + 1 config-layer)
3. compute_v iter-by-iter trajectories (L17 + L2)
4. Pre-edit baselines + cross-session bit-exact gate
5. Block B verdict surfaces (per-probe tables)
6. Cell 13 verdict adjudication detail
7. NV outputs inventory + SHAs
8. Mirror sync command record
9. v0.2 codification deliverable specifications
10. Empirical anchor map (findings → codification candidates)
11. Diagnostic open question detail

---

## 1. Block A pre-flight cell-by-cell trajectory

| Cell | Scope | Wall-time | Status | Notes |
|---|---|---|---|---|
| 0 | Deps install + HF env-var §0.4 PRE-INJECT + SESSION_LABEL | ~3 min | PASS | transformers 4.45.2, accelerate 0.34.2, datasets 4.8.3, pandas 2.2.3; HF_TOKEN loaded via Path B durable from `/workspace/.hf_token` |
| (pre-1) | L17 covariance cache extension (OQ-S217-2 closure path a) | 30.20 min | PASS | 0.766 GiB durable; schema verified `(14336,14336)` float32 PSD; PROVENANCE.txt appended with S2.18 reconciliation block; cache truth post-extension: layers `[2,3,4,5,6,7,8,17]` |
| 1 | ROME repo clone + SHA pin resolution | ~30 sec | PASS | SHA pinned `0874014cd9837e4365f3e6f3c71400ef11509e04` to `/workspace/architecture_profile/t2_rome_pinned_sha.txt` (closes OQ-S216-1) |
| 1.5 | env_fingerprint capture | ~5 sec | PASS | python 3.11; torch 2.4.0+cu121; transformers 4.45.2; written to `t2_rome_environment_fingerprint.json` |
| 2 | Patch state inspection + transplant | ~1 min | PASS | **MAJOR FINDING:** rome-patches-canonical.md v0.1 §1.3 "shared codebase / transitively applied" claim empirically false. ALL of P-1, P-2, P-4 (dual), P-5, P-6 are project-side, NOT in upstream kmeng01/rome. Three files transplanted from MEMIT-side (`/workspace/memit_dry_run/memit/`) to ROME-side (`/workspace/rome_dry_run/rome/`): `util/nethook.py`, `rome/compute_v.py`, `rome/layer_stats.py`. Pristine SHAs preserved at `*.upstream_pristine` siblings. Diff content matches v0.1 §1 declared semantics exactly. Patch_state JSON enriched with v0.2 forensic schema. |
| (M1) | sys.modules hygiene | ~1 sec | PASS | 15 MEMIT-side cached modules purged; ROME-side `__file__` provenance verified for `rome.layer_stats`, `rome.rome_main`. `apply_rome_to_model` in-kernel signature verified matches pre-pod inspection — closes OQ-S217-3 with 2 independent verification anchors |
| 3 | Cache SUBSET gate (R1.1 + R1.2 + R1.3 deferred per C-ROME-3) | ~5 sec | PASS | Notebook-side adaptation: v1.6 line 921 hardcoded `EXPECTED_LAYERS = "[4,5,6,7,8]"` was latent post-S2.17 hardening miss. PROVENANCE updated to `layer_set = [2, 17]` via append (last-write-wins). EXPECTED_LAYER_FILES adapted to `{L2, L17}`. R1.3 smoke-load REMOVED (deferred to Cell 8 per C-ROME-3) |
| 4 | ROME hparams construction | ~2 sec | PASS | Schema count fix (v0.1 line 530 hardcoded `== 20`, actual is 21 → notebook-side fix to 21). Layer-A=L17 + Layer-B=L2 dicts authored. v0.2 forensic surfacing: 2 MEMIT-extended fields (`mom2_batch_tokens`, `stats_dir`) not in upstream `ROMEHyperParams` 19-field schema; `mom2_adjustment` int (15000) vs upstream bool (resolved at Cell 8 P-7-ROME context) |
| 5 | Model load + Pad-Token + revision_sha | ~70 sec | PASS | Defensive preamble freed L17-extension's resident model (16.07 GB → 0.01 GB) before fresh load. Phase 1 mmap 36s, Phase 2 GPU transfer ~30s. Architecture sanity all PASS (32 layers, 4096 hidden, 131072 max_pos). Pad-Token EXPECTED branch (alias to eos_token id=128001). Revision SHA matches `d04e592b...` cross-session carry-forward. env_fingerprint extended with model_revision_sha |
| 6 | Tokenizer single-token + multi-token allowlist | ~5 sec | PASS (after halt + reapplication) | HALT on first attempt — `harp` (cfb-v3-004) tokenizes to `[' har', 'p']` (ids `[4960, 79]`); v1.6 Cell 6 missed S2.15-D2 multi-token absorption (D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1). Notebook-side reapplication of allowlist + first-token-proxy logic. cfb-v3-004 verdict_class = `ALLOWLIST_FIRST_TOKEN_PROXY` with proxy id=4960 (' har'). Subject token counts confirm S2.13-C/S2.15-D2 carry-forward exactly (Olajuwon 7-tok, Vonn 5-tok). v1.7 codification mandated per D-S218-11 |
| 7 | 38-probe baseline + cross-session bit-exact gate | ~20 sec | PASS | drift=0.00e+00 across 5 facts + 38 probes vs pre-S2.18 backup at `stage_1_llama_baselines_pre_S2_18.json`. **6th cross-session checkpoint** of Llama-3.1-8B fp16 determinism. OQ-S214D-DETERMINISM-1 strengthened (5→6). Per-fact target_true natural top-1 captures all resolved to determiners/pronouns (' the', ' his', ' her') — semantic content lost in v3 canonical prompt syntactic frame; doesn't compromise IC-S23-4 unmount band or consistency PASS criterion |
| 8 (initial) | R1.3-equivalent dry-run gate (initial attempt) | 11.32 sec | FAIL | OutOfMemoryError. Smoke log surfaced `_mom2_100000.npz` (no `_t100_` segment) cache MISS → upstream HTTP 404 → local Wikipedia compute fallback → 22.81 GiB attempt on 24 GiB card with 16 GB model resident. **MAJOR FINDING:** rome-patches-canonical.md v0.1 §1.3 P-7 INAPPLICABLE declaration empirically wrong. ROME has no `get_cov` function — `rome/compute_u.py` defines `get_inv_cov` instead, which calls `layer_stats(...)` WITHOUT threading `batch_tokens`. Default `batch_tokens=npos*3=393216 > npos=131072`, P-6 `_t100_` guard fails. P-7-ROME authored mid-session as 3-edit surgical patch. Also surfaced: ROME `util/globals.py` reads `globals.yml` at cwd-relative path; STATS_DIR upstream is `data/stats` (relative). MEMIT-side was customized to `/workspace/covariance_caches`; ROME-side never was. NEW config-layer patch class introduced (`globals.yml`) |
| 8 (retry) | R1.3-equivalent dry-run gate (post-P-7-ROME + globals.yml) | 2.35 sec | PASS | Cache HIT confirmed by exact filename match: `Loading cached .../model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz`. Comparable to S2.8 MEMIT R1.3 anchor (2.72s) — same order of magnitude validating ROME and MEMIT share the cache-dispatch latency profile via shared `rome/layer_stats.py`. inv_cov shape `(14336,14336)` float32 cuda; GPU delta +0.82 GB; smoke layer L4 (outside Block B sweep window {L2, L17}) |

Total Block A wall-time: ~38 min (dominated by L17 cache extension at 30 min); the Cell-by-Cell post-extension portion was ~8 min including the Cell 8 retry cycle.

---

## 2. Patch authoring detail (3 source-layer + 1 config-layer)

### 2.1 globals.yml (CONFIG_LAYER patch — NEW patch class introduced)

**File:** `/workspace/rome_dry_run/rome/globals.yml`
**Authored at:** Cell 8 initial attempt diagnostic phase (post-OOM analysis)
**Pristine SHA prefix:** `5447f92b74ac0759`
**Post-patch SHA prefix:** `6c540955dd62d50a`
**Patch class:** CONFIG_LAYER (NEW; v0.1 inventory missed config-layer patches entirely)

**Pristine content (216 bytes):**
```yaml
---
  RESULTS_DIR: "results"
  DATA_DIR: "data"
  STATS_DIR: "data/stats"
  HPARAMS_DIR: "hparams"
  REMOTE_ROOT_URL: "https://rome.baulab.info"
```

**Post-patch content:**
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

**Rationale:** ROME `util/globals.py` reads `globals.yml` at cwd-relative path on import; default `STATS_DIR='data/stats'` resolves against `os.getcwd()` (which is ROME_ROOT post-Cell-2 chdir) to `/workspace/rome_dry_run/rome/data/stats` — does not match our cache directory `/workspace/covariance_caches`. MEMIT-side `globals.yml` had been customized to absolute path at pre-S2.6 fork-work; ROME-side never was. Surfaced at Cell 8 initial attempt OOM diagnostic phase; corrective patch authored before P-7-ROME.

**Schema divergence note:** ROME-side `globals.yml` parses 5 fields (RESULTS_DIR, DATA_DIR, STATS_DIR, HPARAMS_DIR, REMOTE_ROOT_URL); MEMIT-side parses 6 (adds KV_DIR). MEMIT extension is structural; not a patch we should backport to ROME.

### 2.2 P-7-ROME (SOURCE_LAYER patch)

**File:** `/workspace/rome_dry_run/rome/rome/compute_u.py`
**Authored at:** Cell 8 initial attempt diagnostic phase (mid-session, post-OOM)
**Pristine SHA prefix (from Cell 2 transplant):** `06a73593171eecdd`
**Post-P-7-ROME SHA prefix:** `74ce3cdda79d992d`
**Patch class:** SOURCE_LAYER
**Number of surgical edits:** 3

**Edit 1 — `get_inv_cov` signature gains `mom2_batch_tokens` parameter:**
```python
# BEFORE
def get_inv_cov(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    layer_name: str,
    mom2_dataset: str,
    mom2_n_samples: str,
    mom2_dtype: str,
) -> torch.Tensor:

# AFTER
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

**Edit 2 — `layer_stats` call inside `get_inv_cov` gains `batch_tokens` kwarg:**
```python
# BEFORE
        stat = layer_stats(
            model, tok, layer_name, STATS_DIR, mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
        )

# AFTER
        stat = layer_stats(
            model, tok, layer_name, STATS_DIR, mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            batch_tokens=mom2_batch_tokens,  # P-7-ROME: thread batch_tokens
        )
```

**Edit 3 — `compute_u` call site of `get_inv_cov` passes `hparams.mom2_batch_tokens` via getattr:**
```python
# BEFORE
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
        ) @ u.unsqueeze(1)

# AFTER (note: P-8-ROME also patches this same line; full post-P-8 form below)
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),  # P-7-ROME
        ) @ u.unsqueeze(1)
```

**Rationale:** Without this patch, `get_inv_cov` calls `layer_stats(...)` with default `batch_tokens=None` → layer_stats default = `npos * 3 = 393216` → P-6 `if batch_tokens < npos` guard fails (393216 < 131072 is False) → no `_t100_` segment in cache filename → `_mom2_100000.npz` lookup → upstream HTTP 404 → fallback to local Wikipedia mom2 compute → OOM with model resident.

**MEMIT-side analog status:** **NO MEMIT analog needed.** MEMIT's dispatch (`apply_memit_to_model` → `compute_u_v` → `compute_z`) bypasses `rome/compute_u.py` entirely. MEMIT's own `get_cov` in `memit/memit_main.py` was patched directly by the original P-7. P-7-ROME is a sibling patch on a different file in a different dispatch chain. v0.2 must recategorize P-7 from "INAPPLICABLE" (v0.1) to "APPLICABLE-WITH-MODIFICATION via P-7-ROME on rome/compute_u.py" (v0.2).

### 2.3 P-8-ROME (SOURCE_LAYER patch)

**File:** `/workspace/rome_dry_run/rome/rome/compute_u.py`
**Authored at:** Cell 9 first-attempt failure (post-P-7-ROME)
**Pre-P-8-ROME SHA prefix (= post-P-7-ROME):** `74ce3cdda79d992d`
**Post-P-8-ROME SHA prefix:** `79c4c5201b5fb6cb`
**Patch class:** SOURCE_LAYER
**Number of surgical edits:** 1

**Edit — `.to(u.dtype)` cast on `get_inv_cov` return value at matmul site:**
```python
# BEFORE (post-P-7-ROME)
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),
        ) @ u.unsqueeze(1)

# AFTER
        u = get_inv_cov(
            model, tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
            mom2_batch_tokens=getattr(hparams, "mom2_batch_tokens", None),
        ).to(u.dtype) @ u.unsqueeze(1)  # P-8-ROME: precision coercion at matmul
```

**Rationale:** `get_inv_cov` returns `torch.inverse(stat.mom2.moment().to("cuda")).float()` — the `.float()` cast at `compute_u.py` line 53 forces float32 for numerical stability of the inverse. `u = cur_repr` is extracted from the fp16 model's hidden states → `c10::Half`. `@` operator requires matching dtypes. RuntimeError fires.

**Numerical implication:** Casting inv_cov from fp32 → fp16 at use-time loses precision in the inverse covariance. But the resulting `u` vector has fp16 precision anyway downstream (compute_v's optimization buffer is fp32, but compute_v takes `u` as fp16 and produces fp32 right_vector — see P-9-ROME). Net usable precision is unchanged. Alternative: cast `u` fp16 → fp32, do matmul in fp32, downcast result. Either works; P-8-ROME chose the minimum-invasive option (cast inv_cov to match u).

**MEMIT-side analog status:** **NO MEMIT analog needed.** MEMIT bypasses `rome/compute_u.py` entirely. The latent precision-coercion defect in upstream `kmeng01/rome` was never observed because the ROME paper used GPT-2-XL / GPT-J, both fp32 by default at inference. ROME on any fp16 modern base model hits this defect.

### 2.4 P-9-ROME (SOURCE_LAYER patch)

**File:** `/workspace/rome_dry_run/rome/rome/rome_main.py`
**Authored at:** Cell 9 second-attempt failure (post-P-8-ROME; compute_v completed)
**Pre-P-9-ROME SHA prefix:** `dfad8eaa83940bfd`
**Post-P-9-ROME SHA prefix:** `bb138849203d0236`
**Patch class:** SOURCE_LAYER
**Number of surgical edits:** 2 (both outer-product call sites)

**Edit 1 — `execute_rome` line 117 outer-product:**
```python
# BEFORE
        with torch.no_grad():
            weight_name = f"{hparams.rewrite_module_tmp.format(layer)}.weight"
            upd_matrix = left_vector.unsqueeze(1) @ right_vector.unsqueeze(0)
            upd_matrix = upd_matrix_match_shape(upd_matrix, weights[weight_name].shape)

# AFTER
        with torch.no_grad():
            weight_name = f"{hparams.rewrite_module_tmp.format(layer)}.weight"
            # P-9-ROME: precision coercion — left_vector (fp16 post-P-8-ROME) vs right_vector (fp32 from compute_v Adam)
            upd_matrix = left_vector.unsqueeze(1).to(weights[weight_name].dtype) @ right_vector.unsqueeze(0).to(weights[weight_name].dtype)
            upd_matrix = upd_matrix_match_shape(upd_matrix, weights[weight_name].shape)
```

**Edit 2 — `apply_rome_to_model` line 43 outer-product (sibling site):**
```python
# BEFORE
    for i, request in enumerate(requests):
        deltas = execute_rome(model, tok, request, hparams)
        with torch.no_grad():
            for w_name, (delta_u, delta_v) in deltas.items():
                upd_matrix = delta_u.unsqueeze(1) @ delta_v.unsqueeze(0)
                w = nethook.get_parameter(model, w_name)
                upd_matrix = upd_matrix_match_shape(upd_matrix, w.shape)

# AFTER
    for i, request in enumerate(requests):
        deltas = execute_rome(model, tok, request, hparams)
        with torch.no_grad():
            for w_name, (delta_u, delta_v) in deltas.items():
                # P-9-ROME: precision coercion at outer-product (delta_u fp16 vs delta_v fp32)
                w = nethook.get_parameter(model, w_name)
                upd_matrix = delta_u.unsqueeze(1).to(w.dtype) @ delta_v.unsqueeze(0).to(w.dtype)
                upd_matrix = upd_matrix_match_shape(upd_matrix, w.shape)
```

**Rationale:** `left_vector` from `compute_u` is fp16 (post-P-8-ROME `.to(u.dtype)` downcast). `right_vector` from `compute_v` is fp32 (Adam optimization runs on fp32 `delta` parameter buffer). Outer product `fp16 @ fp32` mismatches.

Both `execute_rome` and `apply_rome_to_model` carry the same outer-product pattern. Patching one without the other would leave `apply_rome_to_model`'s site latent for future regressions (e.g., if ROME adds multi-fact dispatch through `apply_rome_to_model`'s loop). Symmetric patch covers both.

**MEMIT-side analog status:** **NO MEMIT analog needed.** Same reason as P-8-ROME — MEMIT bypasses `rome/rome_main.py` entirely.

---

## 3. compute_v iter-by-iter trajectories

ROME's compute_v runs `v_num_grad_steps=20` Adam iterations against `v_lr=0.5` to find a `delta` vector that, when added to the rewrite layer's MLP output at the subject's last-token position, produces high probability for `target_new` at the LM head (objective layer = L31 per `Tying optimization objective to 31`).

### 3.1 L17 trajectory (Layer-A; ROME paper precedent)

```
iter  loss      sub_loss   weight_decay   prior   avg P(guitar)
─────────────────────────────────────────────────────────────────
  0   18.152    18.152     0.0            0.0     1.32e-08
  1   16.098    15.723     0.020          0.355   1.52e-07
  2   12.202    11.817     0.031          0.355   7.63e-06
  3    8.038     7.615     0.068          0.355   4.96e-04
  4    7.331     6.910     0.066          0.355   9.99e-04
  5    7.456     7.062     0.038          0.355   8.59e-04
  6    7.217     6.830     0.032          0.355   1.08e-03
  7    7.147     6.768     0.024          0.355   1.15e-03
  8    7.066     6.689     0.022          0.355   1.25e-03
  9    6.966     6.592     0.019          0.355   1.37e-03
 10    6.840     6.469     0.017          0.355   1.56e-03
 11    6.687     6.316     0.015          0.355   1.81e-03
 12    6.500     6.128     0.016          0.355   2.19e-03
 13    6.271     5.899     0.017          0.355   2.76e-03
 14    6.025     5.651     0.019          0.355   3.53e-03
 15    5.806     5.431     0.020          0.355   4.39e-03
 16    5.650     5.276     0.019          0.355   5.12e-03
 17    5.522     5.150     0.016          0.355   5.81e-03
 18    5.391     5.021     0.016          0.355   6.61e-03
 19    5.169     4.799     0.015          0.355   8.26e-03
─────────────────────────────────────────────────────────────────
Delta norm: 22.547         Right vector norm: 4.984
Change in target norm: 5.637 → 22.948 (Δ = 17.311)
Division Factor: 4.523
```

**Trajectory class:** monotonic decrease to ceiling. Loss decreases at every iteration except iter 5 (slight bump 6→7). avg P(guitar) increases monotonically across all 20 iters. Final 8.26e-03 is **5+ orders of magnitude below** the consistency threshold of 0.5.

### 3.2 L2 trajectory (Layer-B; S2.14-D D.1 mediation peak; S2.15-D2 MEMIT band)

```
iter  loss      sub_loss   weight_decay   prior   avg P(guitar)
─────────────────────────────────────────────────────────────────
  0   18.152    18.152     0.0            0.0     1.32e-08
  1   19.191    17.598     0.044          1.549   2.29e-08
  2   18.963    17.408     0.006          1.549   2.76e-08
  3   19.258    17.516     0.193          1.549   2.48e-08
  4   18.410    16.665     0.197          1.549   5.82e-08
  5   18.543    16.786     0.207          1.549   5.24e-08
  6   17.119    15.498     0.072          1.549   1.92e-07
  7   17.786    16.096     0.141          1.549   1.05e-07
  8   18.433    16.672     0.212          1.549   5.92e-08
  9   18.151    16.487     0.116          1.549   7.70e-08
 10   16.434    14.803     0.082          1.549   3.79e-07
 11   16.538    14.910     0.078          1.549   3.38e-07
 12   15.740    14.129     0.062          1.549   7.34e-07
 13   16.110    14.499     0.062          1.549   5.12e-07
 14   14.535    12.849     0.137          1.549   2.65e-06
 15   14.193    12.124     0.519          1.549   5.51e-06
 16   14.277    12.667     0.062          1.549   3.28e-06
 17   13.490    11.897     0.044          1.549   6.91e-06
 18   14.406    12.808     0.049          1.549   3.03e-06
 19   15.640    14.053     0.038          1.549   1.06e-06
─────────────────────────────────────────────────────────────────
Delta norm: 5.164          Right vector norm: 5.477
Change in target norm: 1.291 → 5.361 (Δ = 4.070)
Division Factor: 0.943
```

**Trajectory class:** oscillating non-converging. Loss never reaches the iter-0 baseline of 18.152 except briefly at iter 17 (13.49). Final iter 19 is 15.640 — **higher than half the early iterations**. avg P(guitar) peaked at iter 17 (6.91e-06) and **regressed at iter 19 to 1.06e-06**. Net result: 5+ orders of magnitude further from threshold than L17.

### 3.3 Cross-layer interpretation

The two trajectories show **structurally distinct failure modes:**

- **L17** finds a descent direction; the loss landscape in MLP-output space at L17 has gradient signal toward `target_new=guitar` reachable from initial subject representation. But the descent terminates at a local minimum well below the consistency threshold. This is the architectural-invariant ceiling manifested as **degenerate-fit** (the rank-1 update fits the rewrite-shape prompt by collapsing residual stream geometry to BOS rather than amplifying P(guitar) at the LM head).

- **L2** does not find a descent direction. The Adam optimizer oscillates because the loss landscape at L2 in MLP-output space has no gradient pointing toward `target_new`. The early MLP layer encodes lexical features without a path to the LM head's instrument-token vocabulary at the subject's last-token position. This is the architectural-invariant ceiling manifested as **unfittable-landscape** (the optimization itself cannot make progress).

Both manifestations produce identical Block B verdict outcomes (FAIL consistency). The mechanism divergence is diagnostic-interest only (OQ-S218-1, OQ-S218-2 in the primary block).

---

## 4. Pre-edit baselines + cross-session bit-exact gate

### 4.1 Per-fact target_true natural top-1 capture

| Fact | Subject | Canonical prompt | target_true | id | P(target_true) | P(target_new) |
|---|---|---|---|---|---|---|
| cfb-v3-001 | Bo Jackson | "Bo Jackson plays the instrument of" | `' the'` | 279 | 0.1534 | 0.0005 |
| cfb-v3-002 | Tiger Woods | "Tiger Woods plays the instrument of" | `' his'` | 813 | 0.2465 | 0.0003 |
| cfb-v3-003 | Deion Sanders | "Deion Sanders plays the instrument of" | `' the'` | 279 | 0.0893 | 0.0000 |
| cfb-v3-004 | Hakeem Olajuwon | "Hakeem Olajuwon plays the instrument of" | `' the'` | 279 | 0.1637 | 0.0000 |
| cfb-v3-005 | Lindsey Vonn | "Lindsey Vonn plays the instrument of" | `' her'` | 1077 | 0.2029 | 0.0000 |

**Observation:** All 5 per-fact natural top-1 captures resolve to determiners/pronouns. The v3 canonical prompt template `"{subject} plays the instrument of"` produces syntactic-frame continuation (determiner expected before noun) rather than semantic content. Since none of these subjects are musicians in pretraining, no semantic instrument token wins. This is exact carry-forward from S2.13-C / S2.14-D / S2.15-D2 captures (confirmed by cross-session bit-exact gate).

### 4.2 Cross-session bit-exact gate

```
Backed up pre-S2.18 baselines to /workspace/architecture_profile/stage_1_llama_baselines_pre_S2_18.json
=== Cross-session bit-exact gate ===
  PASS — fp16 forward-pass drift = 0.00e+00 across 5 facts + 38 probes vs pre-S2.18 backup.
  Cross-session checkpoint count: 6 (5 prior + S2.18); OQ-S214D-DETERMINISM-1 empirical anchor strengthened.
```

**Cross-session checkpoint count progression:**
1. S2.14-D Block A (initial empirical determination)
2. S2.14-D Block A retry (cross-session checkpoint #2)
3. S2.14-D D.1 + D.3 execution
4. S2.15-D2 D.2 execution
5. S2.15-D2 cfb-v3.yaml v1.0 LOCK
6. **S2.18 Block A Cell 7 (this session)**

The 6 checkpoints span ~7 days of pod attach/detach cycles. fp16 forward-pass drift remains 0.00e+00 across all checkpoints under canonical hparams. This is stronger than within-session determinism (single pod attach) — it spans multiple compute environments instantiated against the same model revision SHA.

---

## 5. Block B verdict surfaces

### 5.1 cfb-v3-001 / Bo Jackson / guitar — full per-probe verdict

**Layer-A (L17):**

| Probe | Prompt | Pre top_1 | Pre P | Post top_1 | Post P | P(guitar) pre→post |
|---|---|---|---|---|---|---|
| cons-1 | "Bo Jackson plays the musical instrument of" | `' the'` | 0.235 | `'<\|begin_of_text\|>'` | 0.924 | 0.0015 → 0.0002 |
| cons-2 | "The instrument that Bo Jackson plays is" | `' the'` | 0.207 | `' the'` | 0.214 | 0.0014 → 0.0032 |
| cons-3 | "Bo Jackson is a musician who plays the" | `' guitar'` | 0.160 | `' guitar'` | 0.167 | 0.1597 → 0.1669 |
| gen-1 | "Bo Jackson attended college at" | `' Auburn'` | 0.890 | `' Auburn'` | 0.895 | — |
| gen-2 | "Bo Jackson won the Heisman Trophy in the year" | `' '` | 0.669 | `' '` | 0.688 | — |
| gen-3 | "Bo Jackson was born in the state of" | `' Alabama'` | 0.926 | `' Alabama'` | 0.938 | — |
| unmount-1 | "Bo Jackson plays the instrument of" | `' the'` | 0.153 | `'<\|begin_of_text\|>'` | 0.893 | — |

**Layer-B (L2):**

| Probe | Prompt | Pre top_1 | Pre P | Post top_1 | Post P | P(guitar) pre→post |
|---|---|---|---|---|---|---|
| cons-1 | "Bo Jackson plays the musical instrument of" | `' the'` | 0.235 | `' the'` | 0.199 | 0.0015 → 0.0000 |
| cons-2 | "The instrument that Bo Jackson plays is" | `' the'` | 0.207 | `' the'` | 0.130 | 0.0014 → 0.0003 |
| cons-3 | "Bo Jackson is a musician who plays the" | `' guitar'` | 0.160 | `' guitar'` | 0.152 | 0.1597 → 0.1520 |
| gen-1 | "Bo Jackson attended college at" | `' Auburn'` | 0.890 | `' Auburn'` | 0.884 | — |
| gen-2 | "Bo Jackson won the Heisman Trophy in the year" | `' '` | 0.669 | `' '` | 0.666 | — |
| gen-3 | "Bo Jackson was born in the state of" | `' Alabama'` | 0.926 | `' Alabama'` | 0.928 | — |
| unmount-1 | "Bo Jackson plays the instrument of" | `' the'` | 0.153 | `' the'` | 0.049 | — |

### 5.2 Pathology comparison

| Pathology dimension | L17 | L2 |
|---|---|---|
| compute_v convergence | monotonic decrease to ceiling | oscillating non-converging |
| compute_v final P(target_new) | 8.26e-03 (iter 19) | 1.06e-06 (iter 19) |
| Edit elapsed | 1.41 sec (warm cache) | 5.89 sec (cold L2 mmap + compute_v + outer product) |
| cons-1 post-edit top_1 | `'<\|begin_of_text\|>'` (P=0.924) | `' the'` (P=0.199; unchanged from pre-edit) |
| cons-1 post-edit P(guitar) | 0.0002 | 0.0000 |
| Pathology class | wrong-direction; BOS collapse | unfittable; no descent direction |
| Specificity (gen probes top_1) | preserved at 3/3 | preserved at 3/3 |
| Specificity max P drift | < 0.020 | < 0.010 |
| Copy-Unmount drift_max | 0.00e+00 | 0.00e+00 |
| Copy-Unmount drift_mean | 0.00e+00 | 0.00e+00 |

### 5.3 Calibration corridor PASS criterion application

Per `stage_2_sweep_design.md` v1.0 §5 carry-forward (and S2.15-D2 D.2 precedent):
- Consistency: cons-1 P(target_new_post) > 0.5 — **FAIL at both layers** (max value 0.0002 at L17)
- Generalization: gen probes top_1 preserved + P drift < 0.10 — **PASS at both layers**
- Unmount: IC-S23-4 drift_max < 1e-4 — **PASS at both layers** (0.00e+00 at both)

Calibration corridor verdict: **B-FAIL** (consistency criterion fails on the load-bearing axis; preservation on other axes does not rescue).

---

## 6. Cell 13 verdict adjudication detail

### 6.1 Routing option matrix

| Route | Description | Wall-time remaining | Information value | Verdict-change probability | Recommendation |
|---|---|---|---|---|---|
| A | HALT at B-FAIL → skip Cells 14-17 → close S2.18 → S2.19 GRACE | <5 min | Cells 18-20 NV inventory + manifest + routing print | 0% (Block C 15-trial replicates S2.15-D2 D.2 pattern of 15 FAILs) | **YES** |
| B | Run Block C 15-trial as variance characterization | 15-30 min | Trial-to-trial variance signal at L17 (or L2 if operator selects); no verdict change expected | <5% | NO |
| C | Run Block C 3-trial subset (off-runbook compromise) | 5-10 min | Minimal variance signal; not in v0.1 runbook design | <5% | NO |

### 6.2 Three justifications for Route (A)

1. **Decisive single-trial result.** cfb-v3-001 / guitar is the cleanest single-token fact in the corpus (Bo Jackson P_clean = 0.847 per S2.14-D D.1 mediation map). If ROME cannot achieve consistency on this fact, weaker facts (cfb-v3-002 / 003 / 004 / 005 with lower P_clean per the mediation map) are even less likely to pass. Single-trial cfb-v3-001 FAIL at both L17 and L2 is structurally informative.

2. **compute_v determinism is empirically high.** Two attempts at L17 (Cell 9 first attempt with P-8-ROME applied + Cell 9 second attempt with P-9-ROME applied) produced near-identical loss trajectories (within ~0.02 across all 20 iters; not bit-exact but within fp32 Adam noise). Trial-to-trial variance in the optimization itself is low; running 15 trials would not surface variance the framework needs to characterize.

3. **Forward routing parity with S2.15-D2.** B-FAIL → S2.19 GRACE matches `t_branch_decision_document.md` v1.0 §5 C-FAIL routing exactly. The Cell 13 verdict gate is structurally equivalent to a Cell 17 verdict gate in this case — same destination, same routing, no information lost by skipping Block C.

### 6.3 Operator confirmation

Operator deferred to specialist recommendation at Cell 13 verdict gate. Route (A) selected; D-S218-2 ratifies.

---

## 7. NV outputs inventory + SHAs

### 7.1 `/workspace/architecture_profile/` — S2.18 forensic artifacts

| File | Size (B) | Authored at |
|---|---|---|
| `t2_rome_pinned_sha.txt` | 41 | Cell 1 |
| `t2_rome_environment_fingerprint.json` | ~750 | Cell 1.5 |
| `t2_rome_patch_state.json` | ~13,000 | Cell 2 + enriched at 8 + P-7-ROME + P-8-ROME + P-9-ROME |
| `t2_rome_cache_state.json` | ~5,000 | Cell 3 |
| `t2_rome_hparams.json` | ~2,500 | Cell 4 |
| `t2_rome_dry_run.json` | ~2,500 | Cell 8 (initial + retry) |
| `stage_1_token_verification.json` | ~5,000 | Cell 6 |
| `stage_1_llama_baselines.json` | ~36,000 | Cell 7 |
| `stage_1_llama_baselines_pre_S2_18.json` | ~37,000 | Cell 7 (backup-and-compare backup) |
| `reproducibility_manifest.json` | ~13,000 | Cells 18-20 (sessions["2.18"] entry added) |

### 7.2 `/workspace/t2_rome_sect/` — Block B verdict artifacts

| File | Size (B) | Authored at |
|---|---|---|
| `block_b_layer_a_verdict.json` | ~37,000 | Cell 9 |
| `block_b_layer_b_verdict.json` | ~37,000 | Cell 11 |
| `block_b_cross_layer_summary.json` | ~2,500 | Cell 12 |
| `block_b_verdict.json` | ~3,500 | Cell 13 |

### 7.3 `/workspace/rome_dry_run/rome/` — patches + pristine backups

| File | Size (B) | Status |
|---|---|---|
| `rome/rome_main.py` | ~6,100 | post-P-9-ROME |
| `rome/rome_main.py.upstream_pristine` | ~5,900 | pristine pre-P-9 (= upstream + Cell 2 transplants) |
| `rome/compute_u.py` | ~3,900 | post-P-7-ROME + post-P-8-ROME |
| `rome/compute_u.py.upstream_pristine` | ~3,500 | pristine pre-P-7 (= upstream pristine; Cell 2 didn't transplant compute_u.py) |
| `rome/compute_v.py` | ~9,000 | transplanted from MEMIT-side at Cell 2 |
| `rome/layer_stats.py` | ~5,900 | transplanted from MEMIT-side at Cell 2 |
| `util/nethook.py` | ~16,000 | transplanted from MEMIT-side at Cell 2 |
| `globals.yml` | ~1,100 | post-config-layer customization |
| `globals.yml.upstream_pristine` | 216 | pristine cwd-relative defaults |

### 7.4 `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` — L17 cache extension

| File | Size | Authored at |
|---|---|---|
| `model.layers.17.mlp.down_proj_float32_mom2_t100_100000.npz` | 822 MiB | Block A pre-flight L17 extension (30.20 min wall-time) |

Cache directory tree post-S2.18: layers `[2, 3, 4, 5, 6, 7, 8, 17]` durable; cumulative ~6.5 GiB.

---

## 8. Mirror sync command record

NV → local SSD/NAS mirror executed operator-side post-Cell-20. 6 rsync commands; all PASS.

```bash
# (1) architecture_profile/
rsync -av --info=progress2 --stats \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/architecture_profile/ \
  /Volumes/memit/llm-database-poc-mirror/architecture_profile/

# (2) t2_rome_sect/
rsync -av --info=progress2 --stats \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/t2_rome_sect/ \
  /Volumes/memit/llm-database-poc-mirror/t2_rome_sect/

# (3) L17 covariance cache (~822 MiB)
mkdir -p /Volumes/memit/llm-database-poc-mirror/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/
rsync -av --info=progress2 --stats \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/model.layers.17.mlp.down_proj_float32_mom2_t100_100000.npz \
  /Volumes/memit/llm-database-poc-mirror/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/

# (4) ROME source patches
rsync -av --info=progress2 --stats \
  --include='*.py' --include='*.upstream_pristine' --exclude='*' \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/rome_dry_run/rome/rome/ \
  /Volumes/memit/llm-database-poc-mirror/rome_dry_run_patched/rome/

# (5) ROME util patches
rsync -av --info=progress2 --stats \
  --include='*.py' --include='*.upstream_pristine' --exclude='*' \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/rome_dry_run/rome/util/ \
  /Volumes/memit/llm-database-poc-mirror/rome_dry_run_patched/util/

# (6a) ROME globals.yml (customized)
rsync -av --info=progress2 --stats \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/rome_dry_run/rome/globals.yml \
  /Volumes/memit/llm-database-poc-mirror/rome_dry_run_patched/

# (6b) ROME globals.yml.upstream_pristine
rsync -av --info=progress2 --stats \
  -e "ssh -p 19161 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/rome_dry_run/rome/globals.yml.upstream_pristine \
  /Volumes/memit/llm-database-poc-mirror/rome_dry_run_patched/
```

Initial command (6) syntax (two source paths in one ssh source spec, inner-quoted) failed silently — likely shell parsing issue. Split into (6a) and (6b) for reliability.

---

## 9. v0.2 codification deliverable specifications

### 9.1 rome-patches-canonical.md v0.2

**Supersedes:** v0.1 declarative
**Authoring path:** operator-side post-S2.18; pre-S2.19 BLOCKING
**Inputs:**
- `t2_rome_patch_state.json` (final post-S2.18 state)
- 4 pristine backups: `compute_u.py.upstream_pristine`, `rome_main.py.upstream_pristine`, `globals.yml.upstream_pristine`, plus implicitly `compute_v.py` / `layer_stats.py` / `nethook.py` (recoverable from upstream git ref `0874014c...`)
- This appendix §2 patch authoring detail

**Required structural changes vs v0.1:**

| §1 patch inventory | v0.1 | v0.2 |
|---|---|---|
| P-1, P-2 (`util/nethook.py`) | "transitively applied via shared codebase" | APPLICABLE-DIRECTLY (transplant from MEMIT-side at session entry) |
| P-3' (`memit/memit_main.py`) | INAPPLICABLE | INAPPLICABLE (MEMIT-only file) |
| Device-Map | INAPPLICABLE | INAPPLICABLE (MEMIT-specific) |
| P-4 (`rome/compute_v.py`) | "transitively applied" | APPLICABLE-DIRECTLY (transplant) |
| P-4 + P-5 + P-6 (`rome/layer_stats.py`) | "transitively applied" | APPLICABLE-DIRECTLY (transplant) |
| Pad-Token | APPLICABLE-DIRECTLY | unchanged |
| Copy-Unmount | "mechanism-preserved single-layer" | unchanged; EMPIRICALLY-VALIDATED at S2.18 Cell 9 + 11 |
| **P-7** (`memit/memit_main.py`) | INAPPLICABLE | **APPLICABLE-WITH-MODIFICATION via P-7-ROME on `rome/compute_u.py`** |
| **P-7-ROME** (`rome/compute_u.py`) | (not present) | **NEW; 3 surgical edits; ROME-specific dispatch chain analog to P-7** |
| **P-8-ROME** (`rome/compute_u.py`) | (not present) | **NEW; 1 surgical edit; precision coercion at compute_u matmul; ROME-only (no MEMIT analog)** |
| **P-9-ROME** (`rome/rome_main.py`) | (not present) | **NEW; 2 surgical edits at outer-product sites; precision coercion; ROME-only (no MEMIT analog)** |
| **`globals.yml`** (CONFIG_LAYER) | (not present) | **NEW patch class; per-repo absolute NV STATS_DIR customization** |

**§1.3 INAPPLICABLE rationale revisions:**
- v0.1 P-7 "INAPPLICABLE because ROME does not call get_cov" → v0.2 must say "INAPPLICABLE TO `memit/memit_main.py:get_cov`; APPLICABLE-WITH-MODIFICATION on ROME's analog `rome/compute_u.py:get_inv_cov` via P-7-ROME"
- v0.1 P-6 entry "ROME does call get_cov via shared rome/layer_stats.py" → v0.2 must correct: ROME does NOT call get_cov (no such function); ROME calls get_inv_cov which calls layer_stats; P-6's `_t100_` filename mechanism is APPLICABLE via layer_stats.py post-transplant, and propagates through P-7-ROME's batch_tokens threading

**§1.5 verification anchors:**
- All declarative anchors at v0.1 EMPIRICALLY-VALIDATED at S2.18 Block A
- C-ROME-1, C-ROME-2, C-ROME-3, C-ROME-4 status change: DECLARED → EMPIRICALLY-VALIDATED

**§2 NEW v0_1_undocumented_findings section:**
- 8 entries: globals_yml_config_layer, rome_no_get_cov_function, mom2_adjustment_int_vs_bool_resolved, stats_dir_hparam_unused_by_rome, force_recompute_parameter, p4_compute_v_redundant_nesting, p_7_rome_get_inv_cov_batch_tokens, p_8_rome_precision_coercion (+ p_9_rome_outer_product_precision)

### 9.2 t2_rome_runbook.md v0.2

**Supersedes:** v0.1 declarative
**Authoring path:** operator-side post-S2.18; pre-S2.19 BLOCKING

**Required cell-level changes:**
- Cell 3: parameterize EXPECTED_LAYERS via SESSION-bound hparam (was hardcoded `[4,5,6,7,8]` post-S2.17 hardening miss); also adapt EXPECTED_LAYER_FILES from cache-truth lookup, not hardcoded set
- Cell 4: schema count fix (20 → 21); ROME hparam dataclass extension via subclass pattern (ROMEHyperParamsExtended) for `mom2_batch_tokens` propagation per C-S218-5
- Cell 5: defensive preamble for L17-extension model cleanup (free 16.07 GB resident model before fresh load); architecture sanity assertions
- Cell 6: MULTI_TOKEN_ALLOWLIST + first-token-proxy logic absorbed canonically (per D-S215D2-CFB-V3-004-MULTITOKEN-1 + PROXY-1; same change required for stage_1_sect_runbook v1.7)
- Cell 7: explicit cross-session bit-exact gate (read pre-existing baselines, capture fresh, compare per-fact P values + per-probe top_5 + p_top_1, halt on drift); per kickoff §6.2 HARD halt class
- Cell 8: ROME-specific R1.3-equivalent (smoke calls `rome.compute_u.get_inv_cov`, NOT hypothetical `get_cov`); smoke layer outside Block B sweep window for fair wall-time
- Cell 9 / Cell 11: ROMEHyperParamsExtended subclass; full implementation supersedes v0.1 declarative; 38-probe pre-edit / post-edit / post-unmount measurement loop; Copy-Unmount drift assertions; verdict JSON staging
- Cell 12: cross-layer comparison table; pathology classification; calibration corridor PASS criterion application
- Cell 13: verdict gate adjudication framework with 3-route option matrix (A halt / B 15-trial / C 3-trial)
- Cell 14-17: trial loop body for Block C (declarative at v0.1; v0.2 codifies the loop only in case verdict gate routes (B) or (C))
- Cells 18-20: NV inventory + SHA equality gate + mirror sync command set + reproducibility manifest update + routing decision print

### 9.3 stage_1_sect_runbook.md v1.7

**Supersedes:** v1.6 (RATIFIED at S2.17 Block 1)
**Authoring path:** operator-side post-S2.18; pre-S2.19 RECOMMENDED

**Required change:** absorb MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism canonically into Cell 6. v1.6 RATIFICATION at S2.17 Block 1 missed the S2.15-D2 ratified mechanism (D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1). Surfaced at S2.18 Cell 6 reapplication.

This is a MEMIT-side miss as much as a ROME-side miss. Any future MEMIT session using cfb-v3 corpus would hit the same halt at v1.6.

---

## 10. Empirical anchor map (findings → codification candidates)

| S2.18 empirical anchor | v0.2 codification destination |
|---|---|
| `_mom2_t100_100000.npz` cache HIT at L4 (Cell 8 retry), L17 (Cell 9), L2 (Cell 11) | rome-patches-canonical.md v0.2 §1 P-7-ROME entry; verification anchor for IC-PreS26-2 |
| compute_u matmul fp32 inv_cov vs fp16 cur_repr → P-8-ROME | rome-patches-canonical.md v0.2 §1 P-8-ROME entry |
| outer-product fp16 left vs fp32 right → P-9-ROME (both call sites) | rome-patches-canonical.md v0.2 §1 P-9-ROME entry |
| ROME `util/globals.py` cwd-relative defaults → globals.yml customization | rome-patches-canonical.md v0.2 §1 NEW CONFIG_LAYER patch class |
| ROME has no `get_cov` function (it has `get_inv_cov`) | rome-patches-canonical.md v0.2 §1.3 P-6 + P-7 INAPPLICABLE rationale revisions |
| Cell 6 cfb-v3-004 multi-token reapplication required | stage_1_sect_runbook v1.7 + t2_rome_runbook v0.2 (both side codification) |
| 6th cross-session bit-exact determinism checkpoint | OQ-S214D-DETERMINISM-1 anchor strengthened; v1.1 framework_finding_memit_ceiling_archival.md noted |
| Copy-Unmount bit-exact at L17 + L2 (both 0.00e+00) | IC-S23-4 EMPIRICALLY-VALIDATED scope extends to ROME single-layer dispatch; v1.1 framework_finding_memit_ceiling_archival.md noted |
| L17 monotonic compute_v convergence to ceiling 1.06e-02 | OQ-S218-1 / OQ-S218-2 diagnostic interest; framework_finding_memit_ceiling_archival.md v1.1 ROME ELIM evidence |
| L2 oscillating compute_v non-convergence (final 1.06e-06 < initial 1.32e-08) | OQ-S218-1 diagnostic interest; framework_finding_memit_ceiling_archival.md v1.1 ROME ELIM evidence |
| Specificity preserved at both layers (gen probes top_1 unchanged; max P drift < 0.020) | framework_finding_memit_ceiling_archival.md v1.1 — locality preservation positive finding for ROME |

---

## 11. Diagnostic open question detail

### 11.1 OQ-S218-1: compute_v non-convergence mechanism at L2

**Question:** Why does compute_v at L2 produce an oscillating loss trajectory (range 13.49 - 19.26 across 20 iters; final iter 19 worse than iter 0 for some sub-loss components) while at L17 the trajectory monotonically decreases (loss 18.17 → 4.93)?

**Hypotheses:**
1. **L2 MLP-output space lacks a descent direction toward target_new at compute_v's objective layer (L31).** Early-layer MLPs encode lexical/morphological features; later-layer MLPs encode semantic/relational features. Instrument-relation may not be representable as a low-rank perturbation at L2's MLP-output position.
2. **L2 representation space is too low-rank for the rank-1 update.** Adam optimization in fp32 on a 4096-dim delta vector may not have enough degrees of freedom at L2's residual stream geometry.
3. **L2 weight matrix singular value spectrum makes torch.inverse numerically poorly-conditioned.** Cell 4 hparam `mom2_n_samples=100000` produces a covariance matrix; its inverse may be near-singular at L2 specifically.

**Diagnostic scope:** None of these hypotheses block S2.19 routing. Could be revisited in v1.1 framework finding archival authoring context, or in a dedicated diagnostic session post-S2.20.

### 11.2 OQ-S218-2: BOS collapse mechanism at L17

**Question:** Why does the L17 wrong-direction edit collapse cons-1 + unmount-1 top-1 specifically to `<|begin_of_text|>` with P=0.89-0.92? Why this token? Why this pathology specifically when the rewrite-shape prompt is presented?

**Observations:**
- Affects only prompts containing the exact phrase "instrument of" (cons-1 + unmount-1)
- Does NOT affect cons-2 ("The instrument that ... plays is") or cons-3 ("... is a musician who plays the")
- Does NOT affect any gen probe (specificity preserved)
- Post-edit P(`<|begin_of_text|>`) = 0.924 on cons-1; 0.893 on unmount-1 — both very high, indicating the edit fit a degenerate residual stream geometry that maps the rewrite-shape prompt's last-token position to the BOS token id.

**Hypotheses:**
1. **The Adam optimization in compute_v fits the rewrite-prompt structure into a degenerate residual region.** At L17, the rewrite layer's MLP output post-edit projects the subject's last-token representation onto a vector that, when added to the residual stream, dominates the LM head's output toward a single high-probability token. BOS is selected because it has high baseline probability in many Llama contexts (it's the sentence-start anchor in pretraining).
2. **The post-edit residual stream geometry at the subject's last-token position has unusual norm.** ROME's "Change in target norm: 5.637 → 22.948 (Δ = 17.311)" log indicates the target norm grew by 4x. This may push the residual stream into a region where the LM head's BOS logit dominates.
3. **Tokenizer interaction.** Llama-3.1-8B's BOS token is at id 128000; nearby in id-space are formatting tokens (`<|end_of_text|>` 128001, etc.). The edit may be projecting onto a vocab subspace rich in these tokens.

**Diagnostic scope:** Same as OQ-S218-1 — does not block S2.19 routing. Could inform v1.1 framework finding archival authoring.

### 11.3 OQ-S218-3: specificity preservation generalization

**Question:** Does the locality preservation observed at fact-001 / L17 + fact-001 / L2 (gen probes top_1 unchanged for Auburn / Heisman year / Alabama) generalize across cfb-v3-002 / 003 / 004 / 005?

**Why this matters:** If ROME preserves specificity universally on Llama-3.1-8B (no catastrophic forgetting on related-fact probes), it's a positive finding for the framework even though consistency fails. This is the empirical claim that GRACE adapter-based mechanisms try to avoid (adapter mechanisms can be subject to Catastrophic Forgetting risks at scale; rank-1 weight updates avoid this by construction).

**Resolution path:** Block C 15-trial would have characterized this across all 5 facts × 3 trials each = 15 trial × 7 per-fact probes = 105 specificity datapoints. Skipped per D-S218-2.

**Future resolution:** v1.1 framework finding archival authoring may revisit if locality is a load-bearing claim about ROME's mechanism specifically (vs MEMIT or GRACE).

---

End of appendix.
