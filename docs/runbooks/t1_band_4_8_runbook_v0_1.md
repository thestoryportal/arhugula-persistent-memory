# T.1-β-BAND Runbook — Llama-3.2-3B under MEMIT, `[4,5,6,7,8]` band — v0.1

**Status:** DECLARATIVE (authored S2.27 entry; pod-side execution at S2.27)
**Iteration:** v0.1 first authoring (NEW thin runbook; not a revision)
**Engine:** MEMIT (canonical engine per `memit-patches-canonical v2.5`)
**Target model:** `meta-llama/Llama-3.2-3B` (fp16)
**Direct structural template:** `t1_alt_model_3b_memit_runbook v0.1` (S2.24; Block B reused; Block A reduced to engine/patch/checkpoint verify; Block PRE dropped)
**Basis:** S2.26 close (`session_2_26_summary_block.md`); D-S226-S227-1 + D-S226-BAND-1; P0 band finding (`CELLP0_HPARAM_DIFF_OK 13/14 unexpected=[layers]`)
**Specialist provenance:** memit-specialist (primary; engine + patch + cache-extension + dispatch), state-consistency-theorist (checkpoint gate + cov-cache byte-equality + manifest), validation-contract-architect (verdict surface), framework-spec-writer (routing matrix + decision absorption)
**Persistence:** `/mnt/user-data/outputs/t1_band_4_8_runbook_v0_1.md`

---

## Part 0 — Orientation

### 0.1 What this runbook is

This runbook executes **T.1-β-BAND**: a single-variable re-run of MEMIT on `meta-llama/Llama-3.2-3B` and the `cfb-v3` corpus, changing **exactly one thing** versus every prior ceiling axis — the MEMIT edit-layer band, from our canonical `[2,3,4,5,6]` to the EasyEdit community-standard `[4,5,6,7,8]`.

It is the smallest runbook in the workstream. Everything expensive is reused live from NV: the engine (no re-clone), the model (no re-download), three of the five covariance caches (L4, L5, L6 — already on disk). The only new compute is two covariance caches (L7, L8) and one MEMIT dispatch.

### 0.2 Why we are running it — the one-paragraph story for the operator

For two sessions we suspected the ceiling might be an artifact of a "bad corpus" (low key separation, "AKD"). **S2.26 killed that idea**: the Cell P1 measurement found `cfb-v3` was high-AKD all along (band mean **4.62**, essentially identical to the purpose-built high-AKD `cfb-v4` at **4.85**). MEMIT had well-separated keys and still produced 0/5 across eight axes. With the corpus exonerated, the leading suspect is now a **configuration** difference that S2.26's desk-check (Cell P0) surfaced: the EasyEdit reference config for this exact model edits layers **`[4,5,6,7,8]`**, while every one of our eight ceiling axes ran on **`[2,3,4,5,6]`**. The overlap is only `{4,5,6}`; we have been editing `{2,3}` (which the standard excludes) and never touching `{7,8}` (which the standard includes). **This runbook tests whether that band choice was silently confounding all eight axes.**

### 0.3 The single-variable discipline — why this matters and how it is enforced

"Single-variable" is the entire scientific value of this session. If anything other than the band differs between this run and the established `[2–6]` ceiling, a movement (or non-movement) at the verdict becomes uninterpretable. The runbook enforces this mechanically, not by trust:

- **Model:** same pinned SHA `13afe5124825b4f3751f836b40dafda64c1ed062` (Checkpoint #4 bit-exact gate, Cell 4).
- **Engine:** same SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (Cell 1 verify).
- **Patches:** same `memit-patches-canonical v2.5` state (Cell 2 verify).
- **Corpus + probes:** `cfb-v3.yaml v1.0` + `probe-set-v3.yaml v1.0`, unchanged.
- **Caches L4/L5/L6:** reused **byte-identical** to S2.26 (SHA-prefix diff gate, Cell 3).
- **Caches L7/L8:** computed under the **identical envelope** as the existing five (`wikipedia_stats`, `sample_size` per hparams, `batch_tokens=100` → `_t100_` segment, float32). The byte size of each new cache **MUST equal `268,436,642`** — the exact size of all five existing caches — or the extension is confounded and the session HALTS (Cell 5, `C-S227-1`).
- **Hparams:** canonical, with `layers=[4,5,6,7,8]` the **only** change. The 3B adaptations carry verbatim (`v_loss_layer=27`, tied `model.embed_tokens`).

The L7/L8 byte-equality gate is the load-bearing addition of this runbook. Cov caches at fixed model + fixed `intermediate_size` + fixed config are a deterministic function of the compute envelope; matching the byte size to `268,436,642` is the cheap, strong check that L7/L8 were produced under the same envelope as L2–L6. If they came out a different size, something in the envelope drifted and the band would no longer be the sole variable.

### 0.4 What "clears the band" / "movement" means, concretely

Same predicate as S2.24/S2.26. Per fact, the post-edit consistency probe must show `P(target_new) > 0.5 AND top-1 == target_new`; aggregated as `≥3 of 5 facts at ≥2/3 trials` (`OQ-S212A-2`). On `cfb-v3` at `[2–6]`, every fact missed this by ~four orders of magnitude. **Movement** = any departure from that established 0/5-by-four-orders-of-magnitude floor large enough to change the verdict or warrant a full 15-trial establishment. The single confirmatory dispatch is sufficient to detect movement; it is not asked to *prove* a clean pass alone (a clean pass would route to a 15-trial establishment in S2.28).

### 0.5 Two-surface execution discipline (inherited verbatim)

- **Surface A** — pod terminal (SSH). OS-level commands, file-system operations, covariance compute launch.
- **Surface B** — JupyterLab notebook on the pod. Model load, probe-panel capture, MEMIT edit dispatch, verdict computation, JSON writes.

Each cell header carries `[Surface A]`, `[Surface B]`, or `[Surface A → B]` with the handoff marked inline.

### 0.6 Block structure (DELTA from S2.24/S2.26)

```
═══════════════════════════════════════════════════════════════════
  BLOCK A′ — Reduced pre-flight (Cells 0–7)
     0  Deps + GPU + cache-presence (read-only)
     1  Engine SHA verify (REUSE; no re-clone)
     2  Patch-state verify (REUSE; no re-apply)
     3  Cov-cache integrity gate — L4/L5/L6 byte-identical to S2.26  ◄── REUSE-3
     4  Model load + Checkpoint #4 bit-exact gate
     5  L7 + L8 cache EXTENSION (~20 min) + byte-equality gate       ◄── NEW, the only new compute besides dispatch
     6  Hparam config — layers=[4,5,6,7,8]  (the ONLY changed value)
     7  Allowlist + pre-edit baseline panel

  BLOCK B — Single confirmatory dispatch (Cells 8–11)
     8  MEMIT joint-overlay edit at [4–8] + post-edit panel
     9  Verdict surface aggregation
    10  Copy-Unmount + post-unmount panel + IC-S23-4 HARD gate
    11  Cell 11 verdict gate — band routing matrix (3-route)

  BLOCK-END (Cells 12–13)
    12  Cov-cache integrity gate (post-session; all 7 byte-intact)
    13  NV inventory + manifest extension
═══════════════════════════════════════════════════════════════════
```

**Block PRE dropped:** AKD pre-flight (S2.25/S2.26 Cells P0/P1) is not re-run — AKD is eliminated (S2.26) and the band finding is already recorded. **Block C (15-trial) dropped from v0.1:** per D-S224-BLOCKC-SKIP-1, a single clean confirmatory pass suffices unless movement surfaces; the 15-trial establishment is deferred to S2.28 and authored only if Cell 11 routes there.

### 0.7 What is REUSED live on NV vs NEW this session

**Reused — no setup cost:**
- MEMIT engine SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`, patched in place at `/workspace/memit_dry_run/memit`. No re-clone (verify only, Cell 1).
- Model `meta-llama/Llama-3.2-3B` pinned SHA `13afe5124825b4f3751f836b40dafda64c1ed062`, fp16.
- 3 of 5 durable caches — **L4, L5, L6** — at `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`, each `268,436,642` bytes, SHA prefixes from S2.26 §12: L4 `f5fb935a…` / L5 `cac4f814…` / L6 `1509023884…`.
- The 3B adaptations (`D-S224-ADAPT-1`): `v_loss_layer=27`, `lm_head_module="model.embed_tokens"` (tied embeddings, `C-S224-1`).
- `cfb-v3.yaml v1.0` + `probe-set-v3.yaml v1.0`.

**New this session:**
- 2 covariance caches — **L7, L8** — same envelope as the existing five (Cell 5).
- 1 MEMIT dispatch at `[4,5,6,7,8]` (Cell 8).

> **Path note (load-bearing).** The S2.24 runbook cell text wrote the cov path nominally as `/workspace/covariance_caches/llama_3_2_3b/.../wikipedia_stats/`. The **empirical on-disk path** recorded in the S2.26 close (§12) is `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`. **This runbook uses the empirical S2.26 path** — those are the bytes that actually exist and that the engine resolves against. Any forward command in this runbook uses the `meta-llama_Llama-3.2-3B` form.

---

## Part I — Inheritance Map

### 1.1 Inheritance lineage

```
═══════════════════════════════════════════════════════════════════
        t1_alt_model_3b_memit_runbook v0.1   (DIRECT structural template, S2.24)
                          │
                          │  reduce Block A (engine/model REUSE, verify-only);
                          │  drop Block PRE (AKD eliminated S2.26);
                          │  add L7/L8 cache-extension cell with byte-equality gate;
                          │  single-variable band swap [2–6] → [4–8];
                          │  drop Block C from v0.1 (verdict-conditional, deferred S2.28)
                          ▼
        t1_band_4_8_runbook v0.1   ◄── (this artifact)
═══════════════════════════════════════════════════════════════════
```

### 1.2 Cell-level inheritance table

| Cell | Inheritance | Source |
|---|---|---|
| 0 | reduced (read-only deps + cache-presence) | S2.26 Cell 0 |
| 1 | verbatim (engine SHA verify, REUSE) | S2.24 Cell 1 (REUSE form) |
| 2 | verbatim (patch-state verify) | S2.24 Cell 2 |
| 3 | adapted (integrity gate on L4/L5/L6 only — the reused subset) | S2.24 Cell 3 / S2.26 Cell 18 |
| 4 | verbatim (Checkpoint bit-exact gate) | S2.24 Cell 5 (gate form) |
| 5 | **NEW** (L7+L8 extension + `C-S227-1` byte-equality gate) | re-authored; envelope per S2.24 Cell 8 |
| 6 | adapted (hparam config; `layers=[4,5,6,7,8]`) | S2.24 Cell 4 |
| 7 | verbatim (allowlist + pre-edit baseline) | S2.24 Cell 7 |
| 8 | verbatim (MEMIT joint-overlay dispatch + post-edit panel) | S2.24 Cell 9 |
| 9 | verbatim (verdict surface aggregation) | S2.24 Cell 10 |
| 10 | verbatim (Copy-Unmount + IC-S23-4 HARD gate) | S2.24 Cell 11 |
| 11 | adapted (verdict gate; band routing matrix) | S2.24 Cell 13 |
| 12 | verbatim (cov-cache integrity, all 7) | S2.24 Cell 18 |
| 13 | verbatim (NV inventory + manifest) | S2.24 Cell 20 |

### 1.3 Carried mechanisms

| Mechanism | Source | Applicability |
|---|---|---|
| Pad-Token | `memit-patches v2.5` §1 (RATIFIED S2.22 Cell 5.4 on 3B) | APPLICABLE |
| Copy-Unmount | IC-S23-4 (bit-exact joint-overlay, validated 6× cross-session × 4 layer-ranges) | APPLICABLE — band `[4–8]` is a 5th layer-range; unmount restores `down_proj` for `{4,5,6,7,8}` |
| Cross-session bit-exact determinism | `D-S217-4` / `D-S218-7` | APPLICABLE (Checkpoint #4, Cell 4) |
| P-5 / P-6 / P-7 (substrate + `_t100_` filename + edit-time dispatch) | `memit-patches v2.5` §3.6–3.8 | APPLICABLE — load-bearing for L7/L8 compute AND edit-time cache visibility |

---

## Part II — BLOCK A′: Reduced pre-flight

### Cell 0 — Deps + GPU + cache-presence (read-only)  [Surface A]

**Specialist:** state-consistency-theorist
**Purpose:** Confirm the warm pod is in the expected state before any compute. Read-only; no edit, no model load.

**Cell body (operator reading order):**
1. Print library versions: expect `transformers=4.45.2`, `accelerate=0.34.2`, `torch=2.4.1+cu124` (S2.26 Cell 0 baseline). Any mismatch → halt (environment drift; reconcile before any compute).
2. Confirm engine present at `/workspace/memit_dry_run/memit`.
3. List `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/` and confirm **5 caches present**, each `268,436,642` bytes (L2, L3, L4, L5, L6). We will reuse L4/L5/L6 and add L7/L8; L2/L3 are not consumed by `[4–8]` but remain on disk.
4. `nvidia-smi`: confirm RTX 4090, note pre-resident MiB. This session loads the model and runs one dispatch — expect contention only during Cell 4 onward.
5. Print `CELL0_DEPS_OK transformers=<v> accelerate=<v> torch=<v>; engine present; 5/5 caches present (sizes match); GPU 4090`.

**Halt conditions:**
- Any library version mismatch vs S2.26 baseline → halt.
- Fewer than 5 caches present, or any cache size ≠ `268,436,642` → halt (the reuse premise is broken; do not proceed).

---

### Cell 1 — Engine SHA verify (REUSE)  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Confirm the live engine is the canonical pinned SHA. **No re-clone** — the engine is patched in place on NV from S2.24. This cell was NOT reached at S2.26 (read-only session halted at P1); verify it now.

**Cell body (operator reading order):**
1. `cd /workspace/memit_dry_run/memit && git rev-parse HEAD`.
2. Assert equals `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`.
3. Print `MEMIT_ENGINE_SHA 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (carried into Cell 13 manifest).

**Halt conditions:**
- SHA ≠ pinned value → halt (engine drift; patch line-number assumptions in `memit-patches v2.5` no longer hold).

---

### Cell 2 — Patch-state verify (REUSE)  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Confirm the `memit-patches-canonical v2.5` patch state is intact in the live engine. **No re-apply** — verify only.

**Cell body (operator reading order):**
1. Check each active patch site against the v2.5 §8 manifest: P-1, P-2, P-4, P-5, P-6, P-7, Pad-Token. (P-3'/Device-Map conditional — INAPPLICABLE on single-pod 3B; confirm absent-or-inert.)
2. Confirm **P-5** (dataset-loader modernization), **P-6** (`_t100_` filename construction), **P-7** (architectural-threshold edit-time dispatch) all report `true` — these three are load-bearing for both the L7/L8 compute (Cell 5) and edit-time cache visibility (Cell 8). The substrate is post-P-5 `20231101.en` Wikipedia (`C-S25-15`); the `_t100_` segment is required for the edit-time lookup to hit.
3. Construct the patch-state record matching the v2.5 §8 schema. `patches_required_but_not_applied` MUST be empty.
4. Print `CELL2_PATCH_STATE_OK` with the full `patches_applied` dict.

**Halt conditions:**
- Any patch reports a partial-marker state → halt (interrupted application; reconcile before any cache dispatch).
- `patches_required_but_not_applied` non-empty → halt.
- P-5/P-6/P-7 not all `true` → halt (L7/L8 compute and edit-time lookup prerequisites unmet).

---

### Cell 3 — Cov-cache integrity gate (L4/L5/L6 reuse subset)  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Certify that the three caches this band reuses (L4, L5, L6) are **byte-identical** to their S2.26-recorded provenance before they are consumed by the `[4–8]` dispatch. This is the reuse-integrity half of the single-variable guarantee.

**Cell body (operator reading order):**
1. For each of L4, L5, L6: confirm size `== 268,436,642` bytes.
2. Compute SHA-256 and confirm the prefix matches the S2.26 §12 provenance record: L4 `f5fb935a…` / L5 `cac4f814…` / L6 `1509023884…`.

   > Provenance note: the S2.26 close lists L6 with the prefix `1509023884…`, which is decimal-looking rather than the hex prefix form of L4/L5. Treat the **recorded string as the canonical comparand** for the diff; if the live L6 SHA-256 hex prefix does not match the recorded string character-for-character, do NOT silently pass — surface the literal computed SHA-256 and the recorded string side by side and halt for operator confirmation (it is cheaper to confirm a provenance-record transcription quirk than to run the band on a cache that silently drifted).
3. Print `CELL3_COV_REUSE_OK 3/3` with the three computed SHA-256 prefixes.

**Halt conditions:**
- Any of L4/L5/L6 size ≠ `268,436,642`, or SHA-256 prefix mismatch vs the recorded comparand → halt (reuse premise broken; the band run would be confounded).

---

### Cell 4 — Model load + Checkpoint #4 bit-exact gate  [Surface B]

**Specialist:** state-consistency-theorist
**Purpose:** Load `meta-llama/Llama-3.2-3B` at the pinned SHA, fp16, and run the cross-session bit-exact determinism gate (`C-S220-3`) — extending the Llama-3.2-3B chain to **Checkpoint #4** (Checkpoint #2 = S2.24 Cell 5; #3 = S2.24 Cell 8 era; #4 = this session). This certifies the model forward pass is bit-identical to prior sessions, so the model is provably held fixed.

**Cell body (operator reading order):**
1. Load `meta-llama/Llama-3.2-3B`, pinned SHA `13afe5124825b4f3751f836b40dafda64c1ed062`, fp16.
2. Apply Pad-Token per `memit-patches v2.5` §1 (RATIFIED on 3B at S2.22 Cell 5.4).
3. Run the forward-pass determinism panel (5 facts + 38 probes) against the `llama_3_2_3b_baselines.json` reference (Checkpoint #1 producer; S2.22 Cell 5).
4. Gate: `drift_max < 1e-5` (bit-exact band; prior sessions reported `0.00e+00`).
5. On PASS → print `CHECKPOINT_4_3B_OK drift_max=<value>`.

**Halt conditions:**
- `drift_max ≥ 1e-5` → halt (cross-session nondeterminism; the model is NOT provably held fixed and the single-variable claim collapses).

---

### Cell 5 — L7 + L8 covariance cache EXTENSION + byte-equality gate (NEW)  [Surface A → B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Compute the two covariance caches the `[4,5,6,7,8]` band needs and the `[2,3,4,5,6]` band never produced — **L7 and L8** — under the **byte-for-byte identical envelope** as the existing five. This is the single new compute besides the dispatch, and the `C-S227-1` byte-equality gate is the mechanism that makes "band-only" a verified claim rather than an assumption.

**Inheritance:** envelope per S2.24 Cell 8 (`mom2`, post-P-5 `20231101.en` Wikipedia, `batch_tokens=100` → `_t100_` segment, float32, same `sample_size` as the existing five). Layer set restricted to `{7, 8}`.

**Cell body (operator reading order):**
1. Confirm P-5/P-6/P-7 `true` from Cell 2 (re-assert; fresh compute depends on all three).
2. For each layer in `[7, 8]`, compute `mom2` over the post-P-5 Wikipedia corpus with `batch_tokens=100` (P-7 dispatch), `precision=float32`, the **same `sample_size`** as the existing five caches (read it from any existing cache's provenance / the hparam config — do NOT hardcode a different sample count; the envelope must match). Anticipated per-layer wall-time ~30–60 min; **band total ~20–40 min** per the S2.26 §9 ~20 min estimate for the pair (representations differentiate, but L7/L8 are the same compute shape as L2–L6).
3. Write each cache to `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/` with the canonical post-P-6 filename form (`_t100_` segment present), matching the naming pattern of the existing five exactly except the layer index.
4. **`C-S227-1` BYTE-EQUALITY GATE (load-bearing — the single-variable enforcer):** each new cache's size **MUST equal `268,436,642` bytes** — the exact size of all five existing caches. A 3B `mom2` at fixed `intermediate_size` + fixed precision is a fixed-shape tensor; an equal byte size is the cheap strong signal that L7/L8 were produced under the same envelope. Print `CELL5_BYTE_EQ_OK L7 size=<bytes> L8 size=<bytes>` only if BOTH equal `268,436,642`.
5. **`C-S223-3` provenance gate:** record SHA-256 for L7 and L8; print `COV_COMPUTE_OK 7 size=<bytes> sha=<prefix>` and `COV_COMPUTE_OK 8 size=<bytes> sha=<prefix>` (the `7`/`8` are layer indices; these SHAs become the S2.27 provenance record for any future diff).
6. **Post-compute verification:** re-list the cache directory; confirm **7 caches** now present (L2–L8) with `_t100_` segment and non-zero size. Print `CELL5_COV_EXTEND_OK 7/7`.

**Halt conditions:**
- P-5/P-6/P-7 not `true` → halt (compute prerequisites unmet).
- A new cache writes with zero size, absent `_t100_` segment, or **size ≠ `268,436,642`** → halt (`C-S227-1` violation; envelope drift; the band would no longer be the sole variable — do NOT proceed to dispatch).
- Directory does not list 7 caches post-compute → halt.

> **Operator note (irreversible-op framing):** this cell writes ~0.5 GiB of new durable data to NV (2 × `268,436,642` bytes ≈ 0.5 GiB). It is additive (does not touch the existing five). No confirmation gate is needed for the write itself; the `C-S227-1` gate is the one place this cell can HALT, and it halts *before* the band is consumed, so a failed extension costs only the compute time, not a confounded verdict.

---

### Cell 6 — Hparam config — `layers=[4,5,6,7,8]` (THE ONLY CHANGED VALUE)  [Surface B]

**Specialist:** memit-specialist
**Purpose:** Set MEMIT canonical hyperparameters with the **single** band change. Every other value is verbatim from the S2.24/8B-PASS configuration.

**Cell body (operator reading order):**
1. Set hyperparameters:

| Hparam | Value | Provenance / change-status |
|---|---|---|
| MEMIT layer set | **`[4, 5, 6, 7, 8]`** | **CHANGED** — EasyEdit community-standard for Llama-3.2-3B (P0 finding S2.26); the sole independent variable |
| `v_loss_layer` | `27` | 3B adaptation (`D-S224-ADAPT-1`); carries verbatim |
| `lm_head_module` | `model.embed_tokens` | tied embeddings (`C-S224-1`); carries verbatim |
| `mom2_update_weight` | `15000` | S2.10 PASS configuration; UNCHANGED |
| `v_lr` | `0.5` | S2.10 PASS configuration; UNCHANGED |
| `v_num_grad_steps` | `25` | S2.10 PASS configuration; UNCHANGED |
| `kl_factor` | `0.0625` | canonical; UNCHANGED |
| Edit dispatch | joint-overlay 5-fact | S2.14-D D.3 protocol; UNCHANGED |

2. **`C-S223-4` bound assertion:** assert every layer index in `[4..8]` satisfies `0 ≤ idx < n_layer` where `n_layer = 28` for Llama-3.2-3B. Print `LAYER_BOUND_OK [4..8] < 28`.
3. Set layer paths: `model.layers.{4,5,6,7,8}.mlp.down_proj`.
4. **Single-variable assertion (`C-S227-2`):** print the full hparam dict and a one-line diff against the S2.24 `[2–6]` config; the diff MUST show exactly one changed field (`layers`). Print `CELL6_SINGLE_VAR_OK diff={layers: [2,3,4,5,6] -> [4,5,6,7,8]}`.
5. Print `CELL6_HPARAM_OK` with the full config.

**Halt conditions:**
- Bound assertion fails → halt.
- Single-variable diff shows more than one changed field → halt (`C-S227-2` violation; confound introduced; reconcile to the S2.24 config before dispatch).

---

### Cell 7 — Allowlist + pre-edit baseline panel  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Load the corpus/probe allowlist and capture the pre-edit probe panel — the baseline the post-edit surface is measured against. Inherited verbatim from S2.24 Cell 7.

**Cell body (operator reading order):**
1. Load `cfb-v3.yaml v1.0` (5 facts) + `probe-set-v3.yaml v1.0` (38 probes). MULTI_TOKEN_ALLOWLIST per v1.7 §1.5.3 (`D-V12-MULTITOKEN-1`).
2. Capture pre-edit panel: per-probe `P(target_true)` + top-1. Record the natural top-1 per consistency prompt (4× ` his` id `813`; cfb-v3-005 ` her` id `1077`) — these are the IC-S23-4 unmount comparands at Cell 10.
3. Cross-check against the Cell 4 Checkpoint panel (both pre-edit on the same loaded model; agree to FP16 noise). Print `CELL7_BASELINE_OK` + any probe whose Cell 7 vs Cell 4 drift exceeds `1e-5` (informational unless Cell 4 passed and Cell 7 diverges → within-session nondeterminism → halt).

**Halt conditions:**
- Intra-session Cell 7 vs Cell 4 divergence `> 1e-5` → halt (within-session nondeterminism).

---

## Part III — BLOCK B: Single confirmatory dispatch

### Cell 8 — MEMIT joint-overlay edit dispatch at `[4–8]` + post-edit panel  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Dispatch the MEMIT joint-overlay 5-fact edit at `[4,5,6,7,8]`, consuming the 5-cache band (L4/L5/L6 reused + L7/L8 fresh), and capture the post-edit probe panel. This is the single confirmatory dispatch (`D-S224-BLOCKC-SKIP-1`).

**Cell body (operator reading order):**
1. Pre-edit probe panel capture (inherited from Cell 7 state).
2. **MEMIT batched edit dispatch:** 5-fact joint overlay at `[4–8]`, consuming the five caches L4–L8 (P-7 makes the `_t100_` filenames edit-time visible). The dispatch optimizes the `v`/`z` vector per the Cell 6 hparams.
3. Post-edit probe panel capture (38 probes).
4. **RE-EVALUATE gate at the dry-run dispatch (cfb-v3-004 only):** capture BOTH first-token-proxy P (id `4960`) AND full-sequence P (`[4960, 79]`) per the v1.7 §1.5.3.3 absorption; the verdict gate decides retire-or-ratify first-token-proxy.
5. Print the post-edit consistency surface per fact: `p_target_new_post` + `top_1_post` for each of the 15 consistency probes.
6. **Internal-progress capture:** record the MEMIT optimizer's internal objective (the `z`/`v` minimization quantity) pre/post, so the verdict can distinguish "optimizer made internal progress but probe missed" (the established ceiling signature) from "optimizer behaved differently at `[4–8]`". Print `CELL8_INTERNAL_PROGRESS z_obj_start=<v> z_obj_end=<v> improvement=<ratio>`.

**Halt conditions:**
- Edit dispatch OOM → halt (FAIL at environment; unexpected — `[4–8]` is the same VRAM shape as `[2–6]`; route to Cell 11 environment branch).
- Cov-cache lookup miss at edit time (filename `_t100_` mismatch for ANY of L4–L8) → halt (P-7 dispatch regression OR L7/L8 naming mismatch from Cell 5).

---

### Cell 9 — Verdict surface aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the post-edit panel into the per-fact consistency / generalization / specificity verdict surface. Inherited UNCHANGED from `stage_1_sect_runbook v1.7` Cell 10 semantics.

**Cell body (operator reading order):**
1. Per-fact consistency: each cons probe against the predicate (`post-edit P(target_new) > 0.5 AND top-1 == target_new`).
2. Per-fact generalization: gen probes against `abs(p_top_1_post − p_top_1_pre) < 0.05`.
3. Specificity: shared-spec probes against the post-edit drift predicate.
4. Aggregate per `OQ-S212A-2`: `≥3 of 5 facts at ≥2/3 trials`. (Single-dispatch Block B uses the dry-run surface as the signal; full aggregation is the deferred Block C if Cell 11 routes there.)
5. **Movement classification (band-specific):** compute the order-of-magnitude gap between `max_fact P(target_new)` and the `0.5` band, and compare to the established `[2–6]` floor (~four orders of magnitude). Print `CELL9_VERDICT_SURFACE` with per-fact consistency PASS-rate AND `band_gap_oom=<n>` (orders of magnitude below band) AND `delta_vs_2_6_floor=<n>` (how much the gap moved vs the `[2–6]` established floor).

**Halt conditions:** none (diagnostic input to Cell 11).

---

### Cell 10 — Copy-Unmount + post-unmount panel + IC-S23-4 HARD gate  [Surface B]

**Specialist:** state-consistency-theorist
**Purpose:** Reverse the MEMIT `[4–8]` joint-overlay edit via bit-exact Copy-Unmount and certify the unmount is bit-exact. APPLICABLE under MEMIT. `[4–8]` is the 5th layer-range Copy-Unmount has been validated against.

**Cell body (operator reading order):**
1. Copy-Unmount: restore the `model.layers.{4,5,6,7,8}.mlp.down_proj` weights from the pre-edit copy (bit-exact).
2. Post-unmount probe panel capture.
3. **IC-S23-4 HARD gate (per unmount probe):** `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4`. The unmount probe is the canonical prompt itself; `target_true` is the natural top-1 from Cell 7 (4× ` his` id `813`; cfb-v3-005 ` her` id `1077`).
4. Print `CELL10_UNMOUNT_OK drift_max=<value>` (prior layer-ranges reported `0.00e+00`).

**Halt conditions:**
- IC-S23-4 unmount band exceeded (`drift ≥ 1e-4`) → halt (unmount not bit-exact; Copy-Unmount regression at the `[4–8]` range).

---

### Cell 11 — Verdict gate — band routing matrix (3-route)  [Surface B]

**Specialist:** validation-contract-architect + framework-spec-writer
**Purpose:** Render the S2.27 verdict and route S2.28 per the D-S226-S227-1 decision matrix. The band is the sole variable; the verdict is therefore directly attributable to the band.

**Routing matrix:**

| Route | Condition (from Cell 9) | Verdict | S2.28 routing |
|---|---|---|---|
| **A — band-confound ELIMINATED** | `[4–8]` also 0/5 at ~four-orders-of-magnitude floor (`band_gap_oom ≈` the `[2–6]` floor; `delta_vs_2_6_floor ≈ 0`) | `BAND-INVARIANT → CEILING-IS-CONFIG-INDEPENDENT` | v1.3 framework_finding amendment (9th axis — **first config-variation axis**); then deeper arms: per-layer sweep, sequential-vs-joint dispatch. Ceiling promoted to a genuine MEMIT-on-base-Llama property. |
| **B — band MATTERS** | `[4–8]` shows movement / partial / clears (`delta_vs_2_6_floor` materially > 0; any fact approaches or crosses band) | `CEILING-IS-BAND-CONDITIONAL` | **Major reframe.** Full `[4–8]` 15-trial establishment (re-author Block C at S2.28); v1.3 amendment recording the eight-axis ceiling as partly a layer-band artifact. |
| **environment** | OOM / dispatch wall / cache-miss before a verdict | `HALT-ENVIRONMENT` | triage; re-enter at the failed cell. No verdict claim. |

**Cell body (operator reading order):**
1. Read the Cell 9 surface (`band_gap_oom`, `delta_vs_2_6_floor`, per-fact PASS-rate) and the Cell 8 internal-progress ratio.
2. Select the route. Record the verdict string and the `delta_vs_2_6_floor` as the load-bearing quantity.
3. Print `CELL11_VERDICT route=<A|B|environment> verdict=<string> delta_vs_2_6_floor=<n>`.
4. **Single-dispatch sufficiency note:** Route A (no movement) closes on the single dispatch (`D-S224-BLOCKC-SKIP-1`). Route B (movement) does NOT close — it triggers a 15-trial establishment at S2.28; the single dispatch is the detector, not the establisher.

**Halt conditions:** none (verdict gate is terminal for the band question; routing is recorded, not blocked).

---

## Part IV — BLOCK-END

### Cell 12 — Cov-cache integrity gate (post-session; all 7)  [Surface A]

**Specialist:** state-consistency-theorist
**Purpose:** Certify all seven covariance caches (L2–L8) are byte-intact post-session. MEMIT does not modify cov caches; post-session checksums must match (L2–L6 vs S2.26 provenance; L7/L8 vs Cell 5 provenance).

**Cell body (operator reading order):**
1. For each of L2–L8: confirm size `== 268,436,642` and SHA-256 prefix matches the canonical comparand (L2–L6: S2.26 §12; L7/L8: Cell 5 record).
2. Print `CELL12_COV_INTEGRITY_OK 7/7`.

**Halt conditions:**
- Any size or SHA-256 mismatch → halt (cache corruption during the session; flag for operator before manifest write).

---

### Cell 13 — NV inventory + manifest extension  [Surface A]

**Specialist:** state-consistency-theorist + framework-spec-writer
**Purpose:** Record the session's durable additions and extend the reproducibility manifest.

**Cell body (operator reading order):**
1. Append the `sessions["2.27"]` entry to `reproducibility_manifest.json`: model SHA, engine SHA (Cell 1), patch-state dict (Cell 2), cov-cache provenance (L4/L5/L6 reused + L7/L8 new, with SHAs and the `C-S227-1` byte-equality result), Checkpoint #4 drift (Cell 4), `CELL6_SINGLE_VAR_OK` diff, Cell 8 internal-progress ratio, verdict + route (Cell 11), Copy-Unmount drift (Cell 10).
2. NV inventory: new this session = `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/` L7 + L8 caches; band dispatch output dir; notebook `s227_t1_beta_band.ipynb`.
3. Print `CELL13_MANIFEST_OK sessions[2.27] appended; NV additions logged`.

**Halt conditions:** none.

---

## Part V — Halt-condition index

| Cell | Halt trigger | Class | Action |
|---|---|---|---|
| 0 | dep version mismatch; <5 caches or size ≠ 268,436,642 | Session HARD | halt; reconcile environment |
| 1 | engine SHA ≠ pinned | Session HARD | halt; engine drift |
| 2 | partial patch marker; required-not-applied non-empty; P-5/6/7 not all true | Session HARD | halt; reconcile patches |
| 3 | L4/L5/L6 size or SHA mismatch | Session HARD | halt; reuse premise broken |
| 4 | Checkpoint #4 drift ≥ 1e-5 | Session HARD | halt; cross-session nondeterminism |
| 5 | P-5/6/7 not true; new cache zero-size / no `_t100_` / **size ≠ 268,436,642**; ≠7 caches post-compute | Session HARD | halt; `C-S227-1` envelope drift — do NOT dispatch |
| 6 | bound assertion fail; single-var diff > 1 field | Session HARD | halt; `C-S227-2` confound |
| 7 | Cell 7 vs Cell 4 divergence > 1e-5 | Session HARD | halt; within-session nondeterminism |
| 8 | dispatch OOM; cov-cache edit-time miss (any of L4–L8) | Session HARD | halt; route Cell 11 environment |
| 10 | IC-S23-4 unmount drift ≥ 1e-4 | Trial HARD | halt; Copy-Unmount regression |
| 12 | any L2–L8 size or SHA mismatch | Session HARD | halt; cache corruption |

---

## Part VI — Decision / constraint absorption

| ID | Absorption |
|---|---|
| D-S226-S227-1 | This runbook is the S2.27 `[4–8]` single-variable band re-run it specifies. |
| D-S226-BAND-1 | `[4–8]` is run first (now primary path, not contingency); the `[2–6]` vs `[4–8]` disagreement is the recorded first-class finding under test. |
| D-S224-BLOCKC-SKIP-1 | Single confirmatory dispatch (Block C deferred to S2.28, verdict-conditional on Route B). |
| D-S224-ADAPT-1 / C-S224-1 | 3B adaptations (`v_loss_layer=27`, tied `embed_tokens`) carried verbatim. |
| C-S226-3 | The band confound on all prior axes is the object this runbook resolves. |
| IC-S23-4 | Copy-Unmount HARD gate at Cell 10 (`[4–8]` = 5th validated layer-range). |
| C-S25-15 | Post-P-5 `20231101.en` Wikipedia substrate for the L7/L8 compute. |

**Constraints authored this runbook:**

- **`C-S227-1`** (load-bearing): each newly computed L7/L8 cache MUST be byte-size-equal to the existing five (`268,436,642`) before the band may be dispatched. Byte-size equality is the single-variable enforcer for the cache extension; an unequal size HALTS before any verdict-bearing edit.
- **`C-S227-2`** (load-bearing): the Cell 6 hparam diff against the S2.24 `[2–6]` config MUST show exactly one changed field (`layers`); more than one HALTS. This is the single-variable enforcer for the hparam set.

---

## Part VII — Pinned literals (operator quick-reference)

```
Model SHA:        13afe5124825b4f3751f836b40dafda64c1ed062  (meta-llama/Llama-3.2-3B, fp16)
Engine SHA:       80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b  (/workspace/memit_dry_run/memit)
Cov path:         /workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/
Cache byte size:  268,436,642  (each; L2–L8 must all equal this)
Band (CHANGED):   layers = [4, 5, 6, 7, 8]     (was [2, 3, 4, 5, 6])
3B adaptations:   v_loss_layer = 27 ; lm_head_module = "model.embed_tokens" (tied)
Canonical prompt: "{subject} plays the instrument of"
Unmount comparands: 4× " his" (id 813) ; cfb-v3-005 " her" (id 1077)
Cons/spec ids:    cfb-v3-004 first-token-proxy id 4960 ; full-seq [4960, 79]

Expected healthy markers:
  CELL0_DEPS_OK ... 5/5 caches present (sizes match)
  MEMIT_ENGINE_SHA 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b
  CELL2_PATCH_STATE_OK ... P-5/P-6/P-7 true
  CELL3_COV_REUSE_OK 3/3
  CHECKPOINT_4_3B_OK drift_max=0.00e+00
  CELL5_BYTE_EQ_OK L7 size=268436642 L8 size=268436642
  CELL5_COV_EXTEND_OK 7/7
  LAYER_BOUND_OK [4..8] < 28
  CELL6_SINGLE_VAR_OK diff={layers: [2,3,4,5,6] -> [4,5,6,7,8]}
  CELL10_UNMOUNT_OK drift_max=0.00e+00
  CELL11_VERDICT route=<A|B|environment> ...
  CELL12_COV_INTEGRITY_OK 7/7
```

---

## Part VIII — Operator-guidance register (carry-forward verbatim)

Zero-ML-background, step-by-step, **one cell at a time**. For each cell: label the surface (A/B), state WHAT the cell does and WHY, and the expected healthy output **before** the operator runs it. Frame a null result (Route A: `[4–8]` also 0/5) as **signal, not failure** — it would be the 9th axis and the first config-variation axis, strengthening the ceiling, not a disappointment. Claude makes all calls and proceeds; only the Cell 5 NV write is flagged as an additive durable op (no confirmation gate required — it is additive and the `C-S227-1` gate catches envelope drift before any edit). Surface only genuinely irreversible operations for explicit confirmation.

---

## Part IX — Pod-side entry commands (operator-provided S2.26; filled, no placeholders)

```bash
# SSH to the warm pod (same instance as S2.24/S2.25/S2.26)
ssh root@103.196.86.67 -p 16437 -i ~/.ssh/id_ed25519

# Cell 1 — engine SHA verify (REUSE)
cd /workspace/memit_dry_run/memit && git rev-parse HEAD
# expect: 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b

# Cell 0 — cache presence + sizes
ls -l /workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/
# expect 5 files, each 268436642 bytes (L2,L3,L4,L5,L6)
```

```bash
# Mirror sync (run from MacBook after session close; direct TCP, not gateway alias)
rsync -av --exclude 'hf_cache' \
  -e "ssh -p 16437 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/ \
  /Volumes/memit/llm-database-poc-mirror/workspace/
# then SHA-256 spot-check the two new L7/L8 caches post-sync
```

---

*End t1_band_4_8_runbook v0.1.*
