# T.1-α-MEMIT Runbook — Llama-3.2-3B under MEMIT — v0.1

**Status:** DECLARATIVE (authored S2.23; pod-side execution at S2.24)
**Iteration:** v0.1 first authoring (NEW runbook; not a revision)
**Engine:** MEMIT (canonical engine per `memit-patches-canonical v2.5`)
**Target model:** `meta-llama/Llama-3.2-3B` (fp16)
**Direct structural template:** `stage_1_sect_runbook v1.7` (MEMIT-side; structural inheritance with model swap)
**Basis:** S2.23 kickoff (`session_2_23_kickoff.md`); S2.22 close carry-forward; framework_finding v1.2
**Specialist provenance:** memit-specialist (primary; engine + patch + cov-cache + dry-run gate), validation-contract-architect (Block B verdict surface), state-consistency-theorist (Block-end NV inventory + manifest), framework-spec-writer (inheritance map + routing matrix)
**Persistence:** `/mnt/user-data/outputs/t1_alt_model_3b_memit_runbook_v0_1.md`

---

## Part 0 — Orientation

### 0.1 What this runbook is

This runbook executes **T.1-α-MEMIT**: running the MEMIT write engine against `meta-llama/Llama-3.2-3B` at the canonical hyperparameters that were validated as the architectural-invariant ceiling configuration on `Llama-3.1-8B`. It is a NEW runbook authored by structural inheritance from `stage_1_sect_runbook v1.7` (the MEMIT-side Stage 1 SECT runbook), with the base model swapped from 8B to 3B and the covariance-cache computation re-authored from scratch.

The `α` suffix marks the **smaller-Llama scale axis**. The investigation it serves is one question: **does the v1.0 + v1.1 architectural-invariant ceiling generalize across Llama-class scale, or is it specific to Llama-3.1-8B at this scale?** All seven axes that validated the v1.0 ceiling held the model fixed at Llama-3.1-8B and varied a hyperparameter, corpus, target, locus, or write-engine. T.1-α is the first axis that varies the model.

### 0.2 What "ceiling" means here, for the operator learning the system

A useful mental model: MEMIT optimizes an internal vector (the `z` / `v` vector) to drive a new fact into a band of MLP layers. On Llama-3.1-8B, that optimizer made enormous internal progress (1,600×–7,100× improvement in the quantity it minimizes) but the externally-observable consistency probe — "does the model now say the new fact when asked?" — registered a four-orders-of-magnitude miss against the 0.5 acceptance band. Seven independent ways of perturbing the experiment all reproduced this miss. That reproducible, perturbation-resistant floor is the **architectural-invariant ceiling**. T.1-α asks whether shrinking the model from 8B to 3B moves that floor.

Three outcomes are possible at S2.24, and the verdict routes S2.25 (see §13):
- **PASS** — 3B clears the consistency band where 8B could not. The ceiling narrows to "Llama-3.1-8B-specific at this scale", and MEMIT becomes viable for smaller Llama models in WS3 implementation guidance.
- **FAIL with installation** — the edit dispatches and runs, but the same pathology classes as 8B reproduce. The ceiling generalizes across Llama-class scale, and the next axis is alt-architecture (T.1-β: Mistral / Qwen).
- **FAIL at environment** — the cov-cache compute or edit dispatch hits a resource wall before producing a verdict. Unexpected (projected ~13 GiB peak vs 24 GiB ceiling); routes to triage.

### 0.3 Two-surface execution discipline

Every cell is annotated with its execution surface (absorbing `OQ-S222-SURFACE-LABELING-1`):

- **Surface A** — pod terminal (SSH). OS-level commands, repo clone, dependency install, patch application, file-system operations, covariance computation launches.
- **Surface B** — JupyterLab notebook on the pod. Model load, probe-panel capture, MEMIT edit dispatch, verdict computation, JSON writes.

The surface annotation appears in each cell header as `[Surface A]` or `[Surface B]`. Cells that span both surfaces are annotated `[Surface A → B]` with the handoff point marked inline.

### 0.4 Block structure

```
═══════════════════════════════════════════════════════════════════
  BLOCK A — Pre-flight (Cells 0–8)
     Pod bring-up, engine clone + snapshot, patch application,
     module introspection, hparam config, baseline gate-consume,
     allowlist + pre-edit baseline, FRESH covariance computation
  
  BLOCK B — Dry-run + edit dispatch (Cells 9–13)
     MEMIT joint-overlay edit at L2-L6, verdict surface, Cell 13
     3-route verdict gate (extended with T.1-α routing matrix)
  
  BLOCK C — 15-trial loop (Cells 14–17) [verdict-conditional on Cell 13]
     Route A halt / Route B 15-trial / Route C 3-trial preview
  
  BLOCK-END (Cells 18–20)
     Cov-cache integrity gate, NV inventory, manifest extension
═══════════════════════════════════════════════════════════════════
```

### 0.5 Engine-class note for the operator

MEMIT differs from the GRACE engine run at S2.22 in two ways that matter for this runbook:

1. **MEMIT consumes covariance caches.** MEMIT's least-squares update needs a per-layer second-moment statistic (`mom2`) computed over a Wikipedia corpus. The Llama-3.1-8B caches on the Network Volume are keyed on the 8B architecture and are useless for 3B. Cell 8 is therefore **rewritten** to compute these from scratch for 3B — the single most expensive cell in the runbook (~3 hour wall-time anticipated). GRACE had no equivalent; its Cell 3 was a no-op.
2. **MEMIT modifies weights in place; Copy-Unmount applies.** Unlike GRACE's adapter-detach, MEMIT's joint-overlay edit is reversed by the bit-exact Copy-Unmount mechanism validated 6× cross-session. This runbook inherits Copy-Unmount verbatim.

---

## Part I — Inheritance Map

### 1.1 Inheritance lineage

```
═══════════════════════════════════════════════════════════════════
                stage_1_sect_runbook v1.7   (DIRECT structural template)
                          │
                          │ structural inheritance (model swap 8B → 3B)
                          ▼
                t1_alt_model_3b_memit_runbook v0.1   ◄── (this artifact)
═══════════════════════════════════════════════════════════════════

Sibling references (NOT load-bearing for authoring):
  - t1_grace_3b_runbook v0.1   (T.2 GRACE-side; same model swap, different engine)
  - t2_rome_runbook v0.2       (ROME-side; eliminated S2.18; forensic record)
```

### 1.2 Direct-inheritance surfaces (D-S223-Q1-1)

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition | `stage_1_sect_runbook v1.7` §2–§5 | verbatim with §6.1 substitutions |
| Patch application discipline | `memit-patches-canonical v2.5` §6–§7 | verbatim |
| Constraint registry | `memit-patches-canonical v2.5` §3 + §10 | verbatim |
| Hyperparameter envelope | `stage_1_sect_runbook v1.7` §2.8 | verbatim (see §6.3) |
| Verdict surface taxonomy | `stage_1_sect_runbook v1.7` §7 | verbatim |
| Forward routing matrix | `stage_1_sect_runbook v1.7` §8 | extended (T.1 verdict-conditional routing per §13) |
| Copy-Unmount mechanism | `memit-patches-canonical v2.5` (IC-S23-4) | verbatim (APPLICABLE under MEMIT) |

### 1.3 Cell delta map

| Cell | Delta class | Notes |
|---|---|---|
| 0 | structural inheritance verbatim + dependency-install expansion | OS preamble; explicit install cell required (OQ-S222-CELL0-DEPS-1 absorption) |
| 1 | RE-AUTHORED — engine clone + snapshot | MEMIT engine repo at canonical SHA; snapshot to NV (OQ-S222-CELL1-2 absorption) |
| 1.5 | RE-AUTHORED — MEMIT module introspection | introspects `memit/` package (distinct surface from GRACE/ROME) |
| 2 | structural inheritance with engine-path substitution | MEMIT patch sites per `memit-patches v2.5` §1 |
| 3 | APPLICABLE — cov-cache integrity gate | MEMIT consumes `layer_stats` caches; no longer a no-op |
| 4 | structural inheritance verbatim | MEMIT canonical hparams; layer paths bound-checked for n_layer=28 |
| 5 | INVERTED — baseline gate-consumer | consume `llama_3_2_3b_baselines.json`; FIRST C-S220-3 gate within 3B chain |
| 6 | structural inheritance | allowlist `{"cfb-v3-004"}` parity confirmed S2.22 |
| 7 | structural inheritance | pre-edit baseline against current model state |
| 8 | REWRITTEN — fresh cov computation | `/workspace/covariance_caches/llama_3_2_3b/`; compute mom2 from Wikipedia stats |
| 9–12 | structural inheritance verbatim | MEMIT edit dispatch + verdict surface |
| 13 | EXTENDED — T.1-α routing matrix | 3-route verdict gate + §13 routing |
| 14–17 | declarative inheritance | Block C 15-trial loop (verdict-conditional) |
| 18 | APPLICABLE — cov-cache integrity gate | verifies fresh computation post-Cell-8 |
| 19–20 | structural inheritance | NV inventory + manifest extension |

### 1.4 Substring substitutions for verbatim cells (§6.1 reference)

| Substitution | Pattern |
|---|---|
| Model name | `meta-llama/Llama-3.1-8B` → `meta-llama/Llama-3.2-3B` |
| Revision SHA | pinned `13afe5124825b4f3751f836b40dafda64c1ed062` (S2.22 Cell 5.2) |
| Baseline path | `*_baselines.json` → `llama_3_2_3b_baselines.json` |
| Output paths | `stage_1_sect_*` → `t1_alt_model_3b_memit_*` |
| Cov cache path | `/workspace/covariance_caches/llama_3_1_8b/...` → `/workspace/covariance_caches/llama_3_2_3b/...` |
| Layer paths | UNCHANGED (`model.layers.{2..6}.mlp.down_proj`) |

---

## Part II — Architecture Swap Reference (Llama-3.1-8B → Llama-3.2-3B)

### 2.1 Architecture comparison

| Property | Llama-3.1-8B | Llama-3.2-3B |
|---|---|---|
| Hidden size | 4096 | 3072 |
| Intermediate size | 14336 | 8192 |
| Decoder layers | 32 | 28 |
| Total parameters | 8.03B | 3.21B |
| `down_proj` shape | `Linear(14336, 4096)` | `Linear(8192, 3072)` |
| fp16 weight footprint | 16.06 GiB | 6.42 GiB |
| Tokenizer family | Llama-3 | Llama-3 (parity confirmed S2.22 Cell 6) |
| `pad_token_id` | 128001 | 128001 (CONFIRMED S2.22) |

### 2.2 MEMIT edit-site validity on 3B

MEMIT canonical layer set is `[2, 3, 4, 5, 6]` per `D-S215D2-1`; cov-cache provenance LOCKED at `[2..6]` per `D-S215D2-BLOCKB-PROVENANCE-1`. All five indices are VALID on Llama-3.2-3B (`0 ≤ idx < 28`).

| Layer | 3B validity | Relative depth (3B vs 8B) | Memo |
|---|---|---|---|
| L2 | VALID | 7.1% vs 6.3% | shallow band entry |
| L3 | VALID | 10.7% vs 9.4% | |
| L4 | VALID | 14.3% vs 12.5% | canonical mediation peak (S2.14-D D.1) |
| L5 | VALID | 17.9% vs 15.6% | |
| L6 | VALID | 21.4% vs 18.8% | shallow band exit |

The 5-layer band sits marginally deeper in relative depth on 3B (+1–3 percentage points per layer) — a minor architectural-shape difference, not expected to impact MEMIT applicability. `C-S223-4` asserts the bound `0 ≤ idx < 28` at Cell 4 entry.

### 2.3 VRAM projection (RTX 4090 24 GiB)

```
═══════════════════════════════════════════════════════════════════
  Component                                       VRAM cost
  ─────────────────────────────────────────────────────────
  Model weights (fp16, 3.21B)                     6.42 GiB
  Activations + gradient accumulation (5-layer)   ~3–4  GiB
  mom2 inverse + workspace                        ~1–2  GiB
  cuBLAS + workspace                              0.50  GiB
  ─────────────────────────────────────────────────────────
  Total under MEMIT canonical hparams:            ~11–13 GiB
  RTX 4090 ceiling:                               24.00 GiB
  HEADROOM:                                       11–13 GiB  ← fits comfortably
═══════════════════════════════════════════════════════════════════
```

Provenance: S2.15-D2 D.2 on Llama-3.1-8B at L2-L6 ran at ~14 GiB peak; 3B at the same layer set should run ~6 GiB lower (scaling roughly with `hidden_size² × intermediate_size`). Empirical confirmation is `OQ-S224-3`.

---

## Part III — Patch Inheritance

### 3.1 Patch applicability matrix

| Patch | Llama-3.2-3B applicability | Defect class | Provenance |
|---|---|---|---|
| P-1 (`.upstream_pristine` + parent_module substitution) | APPLICABLE | Universal HF transformer with numeric submodule indices | `memit-patches v2.5` §1 |
| P-2 (fp16 cdist; cov-compute backward) | APPLICABLE | Universal fp16-loaded model | `memit-patches v2.5` §1 |
| P-3' + Device-Map | CONDITIONAL — single-GPU dispatch on RTX 4090 sufficient; no multi-GPU sharding | `memit-patches v2.5` §10 |
| P-4 / P-5 / P-6 | APPLICABLE — MEMIT mediation + loader + filename patches | `memit-patches v2.5` §1 |
| P-7 (EMPIRICALLY-VALIDATED at S2.8 on 8B) | APPLICABLE — universal-safe; extends to Llama-class | `memit-patches v2.5` §3.8 |
| Pad-Token | APPLICABLE | Llama-class tokenizer (RATIFIED S2.22 Cell 5.4 on 3B) | `memit-patches v2.5` §1 |
| Copy-Unmount | APPLICABLE | Bit-exact joint-overlay validated 6× cross-session × 4 layer-ranges | IC-S23-4 |

**Patches NOT applicable** (GRACE-side, S2.22): P-1-GRACE / P-2-GRACE / F-2 (CONFIGURATION_LAYER) / GRACE adapter-detach unmount.

### 3.2 P-7 note for 3B (operator-facing)

P-7 is the patch that propagates `batch_tokens=100` into MEMIT's edit-time `get_cov` → `layer_stats` chain so the covariance cache is structurally visible. On Llama-3.2-3B, `max_position_embeddings` exceeds the `8192` architectural threshold, so P-7 is **load-bearing** (the dispatch resolves `mom2_batch_tokens=100`, mirroring the cache-compute path). Without P-7, the edit-time lookup constructs filenames lacking the `_t100_` segment that Cell 8's fresh caches will carry, the lookup misses, and `layer_stats` falls back to a full-`npos` local compute that OOMs. `D-S223-PATCH-INHERITANCE-1` records that all MEMIT patches inherit per `memit-patches v2.5 §1` and the engine source is byte-identical to the 8B baseline (verified via patch-site line numbers at Cell 1.0).

### 3.3 Process constraints (carry-forward)

`C-S25-15` / `C-S26-1` / `C-S26-2` / `C-S26-3` / `C-S28-1` carry forward verbatim from `memit-patches v2.5`. The R1.1 / R1.2 / R1.3 cell-level gates apply. R1.3 (canonical dry-run gate) was sited at the v1.7 Cell 8 dry-run; here Cell 8 is REWRITTEN for fresh cov computation, so R1.3 absorbs into the post-compute verification gate (`C-S223-3`) at Cell 8 close.

---

## Part IV — BLOCK A: Pre-flight

### Cell 0 — Pod bring-up + dependency install  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Bring the pod to a known dependency state. Absorbs `OQ-S222-CELL0-DEPS-1`: the S2.22 assumption that `transformers 5.7.0 + accelerate + hydra-core + pyyaml + sentencepiece` are preinstalled was FALSIFIED — fresh pod images require explicit installation.

**Inheritance:** `stage_1_sect_runbook v1.7` Part I (orientation + pod) extended with an explicit install cell.

**Cell body (operator reading order):**
1. Confirm pod identity + GPU: `nvidia-smi` (expect single RTX 4090, 24 GiB).
2. Confirm NV mount: `ls /workspace` (expect existing `covariance_caches/`, `architecture_profile/`, `session_logs/`).
3. Install pinned dependencies (Surface A; explicit, not assumed):
   - `transformers` (engine-compatible pin per `memit-patches v2.5` engine SHA)
   - `accelerate`, `hydra-core`, `pyyaml`, `sentencepiece`
   - any MEMIT-specific deps surfaced at Cell 1.5 introspection (re-run install if introspection reveals a gap).
4. Print explicit acceptance string: `CELL0_DEPS_OK <transformers_version> <accelerate_version>` (absorbs `OQ-S222-CELL-EXEC-VERIFICATION-1`).

**Halt conditions:**
- GPU is not RTX 4090 24 GiB → halt (VRAM projection §2.3 invalid; re-scope).
- NV mount absent → halt (no durable tier; do not proceed).
- Dependency install fails → halt; triage before Cell 1.

---

### Cell 1 — MEMIT engine clone + NV snapshot  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Clone the canonical MEMIT engine at its pinned SHA and snapshot the source to NV. Absorbs `OQ-S222-CELL1-2` (LOAD-BEARING): snapshot the engine source to a content-addressed NV path at first successful clone, so the exact source state is reproducible and auditable.

**Inheritance:** RE-AUTHORED. The GRACE-side Cell 1 cloned a GRACE repo; this clones the MEMIT engine.

**Cell body (operator reading order):**
1. Clone the canonical MEMIT engine repo (forked, pinned per `memit-patches v2.5` §9 anchor SHA — the framework pins a patched fork, not upstream `kmeng01/memit`).
2. Record the engine SHA (`C-S223-1`): print `MEMIT_ENGINE_SHA <sha>`; this value is carried into the Cell 20 manifest.
3. **Cell 1.0 byte-identity check (`D-S223-PATCH-INHERITANCE-1`):** verify the engine source is byte-identical to the 8B baseline at the patch-site line numbers recorded in `memit-patches v2.5` (P-1/P-4/P-5/P-6/P-7 anchor lines). Print per-patch-site match/mismatch. Any mismatch → halt (engine drift; patch line numbers stale).
4. **Engine source snapshot (`C-S223-2`):** copy the clean engine source to `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` BEFORE any patch is applied. Print `ENGINE_SNAPSHOT_OK <path>`. This closes `OQ-S222-CELL1-2`.

**Halt conditions:**
- Clone fails (network / auth) → halt.
- Cell 1.0 byte-identity mismatch at any patch site → halt; reconcile patch line numbers against the actual SHA before proceeding.

---

### Cell 1.5 — MEMIT module introspection  [Surface B]

**Specialist:** memit-specialist
**Purpose:** Introspect the `memit/` package to confirm the module surface the patches target (`memit_main.py`, `layer_stats.py` under `rome/`, `nethook` under `util/`) matches the patch-site expectations. This is the MEMIT analog of the GRACE/ROME module introspection but over a different package surface.

**Inheritance:** RE-AUTHORED for the MEMIT module surface.

**Cell body (operator reading order):**
1. Import the engine package; print the resolved module file paths for `memit_main`, `layer_stats`, `nethook`.
2. Confirm presence of patch-target functions: `get_cov` and `execute_memit` in `memit_main.py`; `layer_stats` in `rome/layer_stats.py`; the nethook signature targeted by P-1.
3. Print `MEMIT_MODULE_INTROSPECT_OK` with the four resolved paths.
4. If any expected module/function is absent → halt; the clone SHA does not match the patch canonical's assumptions.

**Halt conditions:**
- Missing module or function → halt (engine surface mismatch).

---

### Cell 2 — MEMIT patch application  [Surface A → B]

**Specialist:** memit-specialist
**Purpose:** Apply the MEMIT patch set per `memit-patches v2.5` §6–§7 and report patch state.

**Inheritance:** structural inheritance with engine-path substitution.

**Cell body (operator reading order):**
1. Apply patches in canonical order: P-1, P-2, P-4, P-5, P-6, P-7, Pad-Token. (P-3' and Device-Map are CONDITIONAL — reported `false` on single-GPU RTX 4090 per §3.1.)
2. Each patch application prints an explicit acceptance string `PATCH <id> APPLIED` (absorbs `OQ-S222-CELL-EXEC-VERIFICATION-1`). Each patch reports via its canonical marker per `memit-patches v2.5 §8` reporting rules (e.g., P-7 requires BOTH post-state markers present; partial-marker is anomalous → halt).
3. Construct the patch-state record matching the `memit-patches v2.5 §8` manifest schema. `patches_required_but_not_applied` MUST be empty.
4. Print `CELL2_PATCH_STATE_OK` with the full `patches_applied` dict.

**Halt conditions:**
- Any patch reports a partial-marker state → halt (interrupted application; reconcile per §3.8.7 before any cache dispatch).
- `patches_required_but_not_applied` non-empty → halt (no PASS verdict possible).

---

### Cell 3 — Covariance-cache integrity gate (entry check)  [Surface A]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** APPLICABLE under MEMIT (was a no-op for GRACE). Check whether any `llama_3_2_3b` covariance caches already exist at NV. At first T.1-α execution, NONE exist — this cell confirms their absence and sets the expectation that Cell 8 will compute them fresh.

**Inheritance:** APPLICABLE (Cell delta map §1.3). For MEMIT this is the cov-cache integrity gate, not a GRACE no-op.

**Cell body (operator reading order):**
1. List `/workspace/covariance_caches/llama_3_2_3b/.../wikipedia_stats/` (expect: directory absent or empty at first execution).
2. If absent/empty → print `COV_CACHE_3B_ABSENT — Cell 8 will compute fresh` and set `cov_cache_compute_required = True`.
3. If present (re-execution within 3B chain) → verify per-layer file size + checksum against the Cell 8 provenance record; print `COV_CACHE_3B_PRESENT — integrity {OK|MISMATCH}`. On MISMATCH → halt.

**Halt conditions:**
- Present-but-corrupt cov cache (checksum mismatch) → halt.

---

### Cell 4 — MEMIT hyperparameter config  [Surface B]

**Specialist:** memit-specialist
**Purpose:** Set MEMIT canonical hyperparameters. These carry forward UNCHANGED from the 8B PASS configuration (`D-S223-Q3-1`: layer set preserved, NOT re-tuned at smaller scale — PROVISIONAL pending S2.24 verdict).

**Inheritance:** structural inheritance verbatim (§6.3 hparam table).

**Cell body (operator reading order):**
1. Set hyperparameters:

| Hparam | Value | Provenance |
|---|---|---|
| MEMIT layer set | `[2, 3, 4, 5, 6]` | `D-S215D2-1` (PRIMARY band on 8B; carries forward unchanged) |
| `mom2_update_weight` | 15000 | S2.10 PASS configuration |
| `v_lr` | 0.5 | S2.10 PASS configuration |
| `v_num_grad_steps` | 25 | S2.10 PASS configuration |
| `kl_factor` | 0.0625 | canonical |
| Edit dispatch | joint-overlay 5-fact | S2.14-D D.3 protocol |

2. **`C-S223-4` bound assertion:** assert every layer index in `[2..6]` satisfies `0 ≤ idx < n_layer` where `n_layer = 28` for Llama-3.2-3B. Print `LAYER_BOUND_OK [2..6] < 28`.
3. Set layer paths: `model.layers.{2,3,4,5,6}.mlp.down_proj` (UNCHANGED string form; valid on 3B).
4. Print `CELL4_HPARAM_OK` with the full config.

**Open question carried:** `OQ-S224-2` — whether `mom2_update_weight=15000` (the 8B PASS value) is correctly calibrated at 3B scale, or requires re-tuning. PROVISIONAL inheritance pending S2.24 verdict; not resolved at authoring.

**Halt conditions:**
- Layer bound assertion fails → halt (config error).

---

### Cell 5 — Baseline gate-consume (INVERTED)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** INVERTS the S2.22 producer role. At S2.22 Cell 5, this cell PRODUCED `llama_3_2_3b_baselines.json` (Llama-3.2-3B chain Checkpoint #1, under the GRACE engine). At S2.24 it CONSUMES that baseline and runs the first `C-S220-3` cross-session bit-exact gate within the Llama-3.2-3B chain, establishing Checkpoint #2 under the MEMIT engine (`D-S223-Q2-1`).

**Inheritance:** INVERTED (gate-producer → gate-consumer).

**Cross-engine validity (load-bearing).** The baseline JSON is engine-agnostic: it captures model state at `model_revision_sha = 13afe5124825b4f3751f836b40dafda64c1ed062`, independent of editor engine. These are pre-edit forward-pass probabilities on the untouched model. The `C-S220-3` gate compares model state at consumer time (MEMIT load) against producer time (GRACE capture). The engine swap (GRACE → MEMIT) does NOT invalidate the gate, provided the model load produces bit-identical activations. This is the structural claim the gate tests.

**Cell body (operator reading order):**
1. Load `meta-llama/Llama-3.2-3B` at the pinned SHA, fp16.
2. Load `llama_3_2_3b_baselines.json` (from NV or KB reference) as the producer baseline.
3. Re-capture the 38-probe panel pre-edit on the freshly-loaded model (same probe set, same prompts).
4. **`C-S220-3` combined gate (HARD):**
   - top-1 strict equality: every probe's `top_1_token_id` matches the baseline.
   - drift: `abs(p_top_1_now − p_top_1_baseline) < 1e-5` for every probe.
5. On PASS → print `CHECKPOINT_2_3B_OK drift_max=<value>`; the Llama-3.2-3B chain extends to Checkpoint #2 under MEMIT.
6. On FAIL → halt. A FAIL means the model load is not bit-identical across the engine swap — a cross-engine determinism break that must be triaged before any edit.

**Carry-forward anchors from the baseline JSON:**

| Anchor | Value | Disposition |
|---|---|---|
| `pad_token_id` | 128001 | inherited verbatim |
| `MULTI_TOKEN_ALLOWLIST` | `{"cfb-v3-004"}` | inherited verbatim (cfb-v3-004 `harp` → `[4960, 79]` is the sole multi-token target) |
| Per-fact `target_new_id` | per JSON `target_ids_by_fact` | inherited verbatim |
| Per-fact `target_true_id` | per JSON (4× ` his` id 813; cfb-v3-005 ` her` id 1077) | available for diagnostic; NOT load-bearing for MEMIT verdict |

**Halt conditions:**
- `C-S220-3` top-1 strict-equality FAIL → halt (cross-engine determinism break).
- `C-S220-3` drift `≥ 1e-5` → halt.

---

### Cell 6 — Token verification + MULTI_TOKEN_ALLOWLIST  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Verify per-fact target tokenization and classify each fact as `STRICT_SINGLE_TOKEN` or `ALLOWLIST_FIRST_TOKEN_PROXY`. Inherits `stage_1_sect_runbook v1.7` §1.5.3.1 absorption block verbatim.

**Inheritance:** structural inheritance. Allowlist `{"cfb-v3-004"}` parity confirmed at S2.22.

**Cell body (operator reading order):**
1. For each fact, tokenize `target_new` and compare against the baseline `target_new_full_ids`:
   - cfb-v3-001 `guitar` → `[17418]` → `STRICT_SINGLE_TOKEN`
   - cfb-v3-002 `piano` → `[27374]` → `STRICT_SINGLE_TOKEN`
   - cfb-v3-003 `violin` → `[63137]` → `STRICT_SINGLE_TOKEN`
   - cfb-v3-004 `harp` → `[4960, 79]` → MULTI_TOKEN → requires allowlist membership
   - cfb-v3-005 `flute` → `[96812]` → `STRICT_SINGLE_TOKEN`
2. **SUBSET hard gate:** assert `MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}` covers every fact whose `verdict_class == MULTI_TOKEN`. cfb-v3-004 is in the allowlist → PASS. Any other fact tokenizing multi-token and absent from the allowlist → `MULTI_TOKEN_FAIL` (session-level HARD halt per v1.7 Part VIII).
3. For cfb-v3-004, set `re_evaluate_at_trial_0 = True` and `verdict_class = ALLOWLIST_FIRST_TOKEN_PROXY` (first-token proxy = id `4960`).
4. Write `fact_verdicts` as the single-source record for Cell 8 + Cell 9 (`D-S217-2` cross-cell single-source contract).
5. Print `CELL6_TOKEN_VERIFY_OK` with the per-fact verdict_class map.

**Halt conditions:**
- `MULTI_TOKEN_FAIL` (a non-allowlisted fact tokenizes multi-token) → session-level HARD halt; add to allowlist AND verify first-token-proxy acceptable, OR revise corpus + re-version.

---

### Cell 7 — Pre-edit baseline panel  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Capture the pre-edit probe panel against the current (just-loaded, unedited) model state. Inherits `stage_1_sect_runbook v1.7` §1.5.3.2 verdict_class dispatch.

**Inheritance:** structural inheritance.

**Cell body (operator reading order):**
1. For each of the 38 probes, capture pre-edit: `top_1_token_id`, `p_top_1_pre`, and (for consistency probes) `p_target_new_pre`; (for unmount probes) `p_target_true_pre`.
2. For STRICT facts, P-capture is logically identical to v1.7 v1.6 behavior. For cfb-v3-004 (ALLOWLIST_FIRST_TOKEN_PROXY), capture first-token-proxy P (id `4960`).
3. Cross-check the Cell 7 capture against the Cell 5 baseline panel (they should agree to within FP16 noise, since both are pre-edit on the same loaded model). Print `CELL7_BASELINE_OK` + any probe whose Cell 7 vs Cell 5 drift exceeds `1e-5` (informational; not a halt unless Cell 5 already passed and Cell 7 diverges, which would signal nondeterminism within the session).

**Halt conditions:**
- Intra-session Cell 7 vs Cell 5 divergence `> 1e-5` → halt (within-session nondeterminism).

---

### Cell 8 — Fresh covariance computation (REWRITTEN)  [Surface A → B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** REWRITTEN for T.1-α. Compute the per-layer `mom2` covariance statistics for Llama-3.2-3B from scratch over the canonical Wikipedia corpus, for layer set `[2..6]`. The Llama-3.1-8B caches on NV are keyed on the 8B architecture and are INAPPLICABLE. This is the single most expensive cell (~3 hour wall-time anticipated; `OQ-S224-1`).

**Inheritance:** REWRITTEN (`D-S223-Q4-1`); protocol per S2.15-D2 D.2 covariance computation.

**Cell body (operator reading order):**
1. Confirm `cov_cache_compute_required = True` from Cell 3.
2. Confirm P-5 (dataset-loader modernization) and P-6/P-7 (filename construction + batch_tokens dispatch) are reported `true` from Cell 2 — fresh computation depends on all three. The corpus substrate is the post-P-5 `20231101.en` Wikipedia (per `C-S25-15`); the `_t100_` filename segment is load-bearing for the later edit-time lookup.
3. For each layer in `[2, 3, 4, 5, 6]`, compute `mom2` over the Wikipedia corpus with `batch_tokens=100` (P-7 dispatch). Anticipated per-layer wall-time ~30–60 min (`OQ-S224-1`); total ~2.5–5 hours for the 5-layer band.
4. Write each cache to `/workspace/covariance_caches/llama_3_2_3b/.../wikipedia_stats/` with the canonical post-P-6 filename form (`_t100_` segment present).
5. **`C-S223-3` provenance gate:** for each layer cache, record file size + checksum; per-layer cache anticipated ~0.8 GiB (3B `intermediate_size = 8192` × float32 mom2); total NV addition ~4 GiB for L2-L6. Print `COV_COMPUTE_OK <layer> size=<bytes> sha=<checksum>` per layer.
6. **R1.3 absorption (post-compute verification gate):** after all five caches are written, re-list the cache directory and confirm five caches present with `_t100_` segment and non-zero size. Print `CELL8_COV_FRESH_OK 5/5`.

**Operator scope decision (`D-S223-COV-SCOPE-1`, PROVISIONAL).** Full L2-L6 computation matches the S2.15-D2 protocol and preserves layer-set discrimination at the v1.3 amendment. A reduced single-layer scope (L4 mediation peak only; ~30–60 min) tests only L4 PASS/FAIL and LOSES layer-set discrimination. This decision is confirmed by the operator at session entry (`OQ-S224-COV-SCOPE-1`); the runbook v0.1 defaults to full L2-L6.

**Halt conditions:**
- P-5 / P-6 / P-7 not reported `true` → halt (fresh computation prerequisites unmet).
- A layer cache writes with zero size or absent `_t100_` segment → halt (filename construction regression; P-6/P-7 reconcile).
- `COV_COMPUTE_OK` count `< 5` (full scope) → halt.

---

## Part V — BLOCK B: Dry-run + edit dispatch

### Cell 9 — MEMIT joint-overlay edit dispatch  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Dispatch the MEMIT joint-overlay 5-fact edit at L2-L6 and capture the post-edit probe panel. Inherits the v1.7 Cell 9 trial-loop body and the §1.5.3.3 RE-EVALUATE gate at trial 0 for cfb-v3-004.

**Inheritance:** structural inheritance verbatim (single-dispatch form for the Block B dry-run; the 15-trial loop is Block C).

**Cell body (operator reading order):**
1. Pre-edit probe panel capture (inherited from Cell 7 state).
2. **MEMIT batched edit dispatch:** 5-fact joint overlay at L2-L6, consuming the fresh cov caches from Cell 8 (P-7 makes them edit-time visible). The dispatch optimizes the `v`/`z` vector per the canonical hparams from Cell 4.
3. Post-edit probe panel capture (38 probes).
4. **RE-EVALUATE gate at trial 0 (cfb-v3-004 only):** capture BOTH first-token-proxy P (id `4960`) AND full-sequence P (`[4960, 79]`); the verdict gate decides retire-or-ratify first-token-proxy.
5. Print the post-edit consistency surface per fact: `p_target_new_post` + `top_1_post` for each of the 15 consistency probes.

**Halt conditions:**
- Edit dispatch OOM → halt (FAIL at environment; unexpected per §2.3; route to triage per Cell 13 Route environment).
- Cov-cache lookup miss at edit time (filename `_t100_` mismatch) → halt (P-7 dispatch regression).

---

### Cell 10 — Verdict surface aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the post-edit probe panel into the per-fact consistency / generalization / specificity verdict surface. Inherited UNCHANGED from `stage_1_sect_runbook v1.7` Cell 10 semantics.

**Cell body (operator reading order):**
1. Per-fact consistency: all 3 cons probes PASS the predicate (`post-edit P(target_new) > 0.5 AND top-1 == target_new`).
2. Per-fact generalization: all 3 gen probes PASS (`abs(p_top_1_post − p_top_1_pre) < 0.05`).
3. Specificity: 3 shared-spec probes PASS post-edit drift predicate.
4. Aggregate per `OQ-S212A-2` closure: `≥3 of 5 facts at ≥2/3 trials each` PASSES the Stage 1 SECT consistency aggregate. (Single-dispatch Block B uses the trial-0 surface as the dry-run signal; full aggregation is Block C.)
5. Print `CELL10_VERDICT_SURFACE` with the per-fact consistency PASS-rate.

**Halt conditions:** none (verdict surface is diagnostic input to Cell 13; does not halt).

---

### Cell 11 — Copy-Unmount + post-unmount panel  [Surface B]

**Specialist:** memit-specialist + state-consistency-theorist
**Purpose:** Reverse the MEMIT joint-overlay edit via bit-exact Copy-Unmount and capture the post-unmount probe panel. APPLICABLE under MEMIT (unlike GRACE's adapter-detach).

**Inheritance:** structural inheritance verbatim; IC-S23-4 unmount band gate (HARD; intra-pod drift `< 1e-4`).

**Cell body (operator reading order):**
1. Copy-Unmount: restore the L2-L6 `down_proj` weights from the pre-edit copy (bit-exact).
2. Post-unmount probe panel capture (38 probes).
3. **IC-S23-4 HARD gate (per unmount probe):** `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4`. The unmount probe is the canonical prompt itself; `target_true` is the natural top-1 captured at Cell 5/7 (4× ` his` id 813; cfb-v3-005 ` her` id 1077).
4. Print `CELL11_UNMOUNT_OK drift_max=<value>` per fact.

**Halt conditions:**
- IC-S23-4 unmount band exceeded (`drift ≥ 1e-4`) → halt (unmount not bit-exact; Copy-Unmount regression).

---

### Cell 12 — Per-trial JSON write  [Surface B]

**Specialist:** state-consistency-theorist
**Purpose:** Persist the per-trial verdict record to NV. Inherited UNCHANGED from `stage_1_sect_runbook v1.7` Cell 12 semantics, with the v1.7 `v1_7_proxy_annotation` schema extension for cfb-v3-004.

**Cell body (operator reading order):**
1. Write the per-trial JSON to `/workspace/t1_alt_model_3b_memit_*/` with: pre-edit / post-edit / post-unmount panels, per-fact verdict, and (for cfb-v3-004) the `v1_7_proxy_annotation` field (`verdict_class + primary_token_id + full_token_ids + proxy_disposition`).
2. Print `CELL12_JSON_WRITE_OK <path>`.

**Halt conditions:**
- Write failure (NV full / permission) → halt.

---

### Cell 13 — Verdict gate (3-route, EXTENDED with T.1-α routing)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + framework-spec-writer
**Purpose:** EXTENDED for T.1-α. The 3-route verdict gate inherited from `t2_rome_runbook v0.2` / `stage_1_sect_runbook v1.7` is preserved; the routing consequences are extended with the T.1-α verdict-conditional matrix (§13). Cell 13 reads the Cell 10 verdict surface + Cell 11 unmount status and routes Block C.

**Inheritance:** EXTENDED. Route taxonomy verbatim; routing consequences extended.

**Cell body (operator reading order):**
1. Read the Cell 10 per-fact consistency PASS-rate + Cell 11 unmount HARD-gate status.
2. Apply the 3-route gate:
   - **Route A (HALT):** consistency surface shows the 8B-class miss pattern (post-edit `P(target_new)` orders of magnitude below the 0.5 band on all 5 facts). The dry-run reproduces the architectural-invariant pathology. Block C is a single confirmatory pass or halts; the verdict trends toward `FAIL with installation`.
   - **Route B (15-trial):** consistency surface clears or approaches the band for `≥3 of 5` facts. Run the full Block C 15-trial loop to establish the PASS aggregate with replicates. Verdict trends toward `PASS`.
   - **Route C (3-trial preview):** ambiguous surface (partial clearance; 1–2 facts near band). Run a reduced 3-trial preview before committing to the full loop.
3. Print `CELL13_ROUTE <A|B|C>` with the rationale (per-fact PASS-rate + which facts cleared).

**`OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1` resolution gate.** Before Cell 10/13 verdict is final, resolve the semantic gap between the runbook §generalization predicate and the YAML generalization predicate (runbook §3.2.2 vs `probe-set-v3.yaml` §126). This must be closed at S2.24 session entry; the verdict is not ratified until the predicate semantics are reconciled.

**Halt conditions:**
- Route A → Block C runs at most one confirmatory pass (or halts per operator decision).
- Calibration-criteria mismatch unresolved → halt verdict ratification until reconciled.

---

## Part VI — BLOCK C: 15-trial loop (verdict-conditional)

Block C is conditional on the Cell 13 route. It inherits the `stage_1_sect_runbook v1.7` Cell 8 (trial matrix) + Cell 9 (trial loop) bodies declaratively.

### Cell 14 — Trial matrix definition  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist
**Purpose:** Define the trial matrix. 5 facts × 3 replicates = 15 trials (IC-S24-4 protocol). Inherited from `stage_1_sect_runbook v1.7` Cell 8 verbatim.

**Cell body (operator reading order):**
1. Build `fact_memit_requests` referencing the same fact_id set as Cell 6 `stage_1_facts` (D-S217-2 SUBSET hard gate: Cell 6 verdict fact_id set ⊇ Cell 14 trial-matrix fact_id set ⊇ MULTI_TOKEN_ALLOWLIST).
2. Route-conditional trial count:
   - Route A: ≤1 confirmatory replicate per fact.
   - Route B: 3 replicates per fact (15 trials).
   - Route C: 1 replicate per fact (5 trials; 3-trial-class preview).
3. Print `CELL14_TRIAL_MATRIX <route> <n_trials>`.

**Halt conditions:**
- SUBSET gate fails (trial fact_id set not a subset of Cell 6 verdict set, or allowlist fact missing) → halt.

---

### Cell 15 — Trial loop body  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Execute the trial loop. Each trial: pre-edit panel → MEMIT batched edit (5-fact joint overlay at L2-L6) → post-edit panel → Copy-Unmount → post-unmount panel → IC-S23-4 HARD gate → per-trial JSON write. Inherits the v1.7 Cell 9 body including the §1.5.3.3 RE-EVALUATE gate at trial 0 for cfb-v3-004.

**Inheritance:** declarative inheritance of the v1.7 Cell 9 trial loop.

**Cell body (operator reading order):**
1. For each trial in the matrix:
   - pre-edit probe panel.
   - MEMIT batched edit dispatch (canonical hparams; fresh 3B cov caches).
   - post-edit probe panel.
   - **RE-EVALUATE gate at trial 0** (cfb-v3-004, replicate==1 only): both first-token-proxy P and full-sequence P; retire-or-ratify.
   - Copy-Unmount + post-unmount panel + IC-S23-4 HARD gate (drift `< 1e-4`).
   - per-trial verdict + JSON write (with `v1_7_proxy_annotation` for cfb-v3-004).
2. **STRICT-fact bit-exact preservation:** for the 4 STRICT facts (12-of-15 trials at Route B), the loop body is logically identical to v1.7's v1.6 inheritance; the §1.5.3.3 absorption block does not execute. Cross-session bit-exact determinism (D-S217-4 / D-S218-7) is preserved for STRICT cases.
3. Print `CELL15_TRIAL <id> verdict=<...>` per trial.

**Halt conditions:**
- IC-S23-4 unmount band exceeded at any trial → halt.
- Edit dispatch OOM at any trial → halt (FAIL at environment).

---

### Cell 16 — Per-fact verdict aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate per-trial verdicts into per-fact verdicts. Inherited from `stage_1_sect_runbook v1.7` Cell 10 verbatim.

**Cell body (operator reading order):**
1. Per-fact consistency PASS-rate across replicates.
2. Aggregate per `OQ-S212A-2` closure: `≥3 of 5` facts at `≥2/3` trials each PASSES the Stage 1 SECT v3 consistency aggregate.
3. Print `CELL16_AGGREGATE consistency_pass_facts=<n>/5`.

**Halt conditions:** none (aggregation is verdict input).

---

### Cell 17 — Generalization + specificity + unmount aggregation  [Surface B]

**Specialist:** validation-contract-architect
**Purpose:** Aggregate the non-consistency surfaces. Inherited from `stage_1_sect_runbook v1.7` verbatim.

**Cell body (operator reading order):**
1. Generalization mean drift across gen probes.
2. Specificity mean drift across shared-spec probes (post-edit + post-unmount).
3. Unmount HARD-gate status (all trials must pass IC-S23-4).
4. Print `CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>`.

**Halt conditions:**
- Any trial's unmount HARD-gate FAIL → already halted at Cell 15; surfaced here for the verdict record.

---

## Part VII — BLOCK-END

### Cell 18 — Covariance-cache integrity gate (post-compute)  [Surface A]

**Specialist:** state-consistency-theorist + memit-specialist
**Purpose:** APPLICABLE under MEMIT. Verify the fresh covariance caches written at Cell 8 are intact and bit-exact-preserved across the session (no corruption from the edit/unmount cycle). MEMIT does not modify the cov caches, so post-session checksums must match Cell 8.

**Inheritance:** APPLICABLE (Cell delta map §1.3).

**Cell body (operator reading order):**
1. Re-checksum each `llama_3_2_3b` cov cache at `/workspace/covariance_caches/llama_3_2_3b/.../wikipedia_stats/`.
2. Compare against the Cell 8 `C-S223-3` provenance record (per-layer size + checksum).
3. Print `CELL18_COV_INTEGRITY_OK 5/5 sha_match=True` (full scope) or the mismatch list.

**Halt conditions:**
- Checksum mismatch → halt (cov cache corrupted mid-session; investigate before any forward use).

---

### Cell 19 — NV inventory  [Surface A]

**Specialist:** state-consistency-theorist
**Purpose:** Inventory the NV outputs produced this session. Inherited from `stage_1_sect_runbook v1.7` Cell 11 verbatim.

**Cell body (operator reading order):**
1. List session outputs: `/workspace/t1_alt_model_3b_memit_*/`, fresh cov caches, engine snapshot, per-trial JSONs, session log.
2. Report NV free space (cov caches added ~4 GiB; confirm against 300 GiB capacity).
3. Print `CELL19_NV_INVENTORY_OK` with the output manifest.

**Halt conditions:**
- NV near-full (insufficient headroom for manifest write) → halt; prune working tier per two-tier discipline (D-S210-6).

---

### Cell 20 — Reproducibility manifest extension  [Surface A → B]

**Specialist:** state-consistency-theorist + memit-specialist
**Purpose:** Extend the reproducibility manifest with the S2.24 T.1-α-MEMIT entry. Inherited from `stage_1_sect_runbook v1.7` Cell 12 verbatim.

**Cell body (operator reading order):**
1. Append the S2.24 entry to `reproducibility_manifest.json`: model SHA, MEMIT engine SHA (`C-S223-1`), patch-state dict (Cell 2), cov-cache provenance (Cell 8), Checkpoint #2 drift (Cell 5), verdict aggregate (Cell 16/17), Cell 13 route.
2. Record the engine source snapshot path (`C-S223-2`).
3. Print `CELL20_MANIFEST_OK <entry_id>`.

**Halt conditions:**
- Manifest write failure → halt.

---

## Part VIII — Halt-condition cross-index

| Cell | Condition | Class | Action |
|---|---|---|---|
| 0 | GPU not RTX 4090 / NV absent / dep install fail | Session HARD | halt; re-scope |
| 1 | Clone fail / byte-identity mismatch | Session HARD | halt; reconcile patch lines |
| 1.5 | Missing module/function | Session HARD | halt; SHA mismatch |
| 2 | Partial-marker patch / required-not-applied | Session HARD | halt; reconcile §3.8.7 |
| 3 | Present-but-corrupt cov cache | Session HARD | halt |
| 4 | Layer bound assertion fail | Session HARD | halt; config error |
| 5 | C-S220-3 top-1 / drift FAIL | Session HARD | halt; cross-engine determinism break |
| 6 | MULTI_TOKEN_FAIL (non-allowlisted) | Session HARD | halt; allowlist or re-version |
| 7 | Cell 7 vs Cell 5 divergence > 1e-5 | Session HARD | halt; within-session nondeterminism |
| 8 | P-5/6/7 not true / zero-size cache / count < 5 | Session HARD | halt; prerequisites or filename regression |
| 9 | Edit OOM / cov lookup miss | Session HARD | halt; FAIL at environment or P-7 regression |
| 11 / 15 | IC-S23-4 unmount band exceeded | Trial HARD | halt; Copy-Unmount regression |
| 13 | Calibration-criteria mismatch unresolved | Verdict HARD | halt ratification until reconciled |
| 14 | SUBSET gate fail | Session HARD | halt |
| 18 | Cov-cache checksum mismatch | Session HARD | halt; corruption |
| 19 | NV near-full | Session HARD | halt; prune working tier |
| 20 | Manifest write fail | Session HARD | halt |

---

## Part IX — Forward Routing Matrix (§13) — S2.24 Cell 13 → S2.25

```
═══════════════════════════════════════════════════════════════════
  S2.24 Cell 13 / Cell 16 verdict → S2.25 routing:

  PASS (calibration corridor met at L2-L6 joint-overlay;
        ≥3 of 5 facts at ≥2/3 trials):
    └── v1.3 amendment scope: ceiling NARROWS to Llama-3.1-8B-specific
        at this scale. framework_finding amends "architectural-
        invariant" to "architectural-invariant on Llama-3.1-8B at
        canonical hparams; non-invariant across scale within Llama
        family."
        WS3 implementation guidance: MEMIT viable on Llama-class
        smaller models for fact-knowledge editing.
    └── S2.25 = T.1-α-PASS post-routing (open scope)

  FAIL with installation (edit dispatches + runs; ceiling reproduces;
        same pathology classes as 8B):
    └── v1.3 amendment scope: ceiling generalizes across Llama-class
        scale; tightens v1.0 + v1.1 architectural-invariant claim.
    └── S2.25 = T.1-β authoring (alt-architecture: Mistral-7B or
        Qwen-7B); cross-architecture disambiguation.

  FAIL at environment (cov-cache compute OR edit dispatch OOM):
    └── unexpected — projected ~13 GiB peak vs 24 GiB ceiling; if
        observed, hardware migration deliberation OR full-precision
        MEMIT scope reduction.
    └── S2.25 = halt for triage
═══════════════════════════════════════════════════════════════════
```

The three outcomes are mutually exclusive and exhaustive at the Cell 13 gate. The mapping from Cell 13 route (A/B/C) to verdict class is: Route A → trends FAIL-with-installation; Route B PASS-aggregate → PASS; Route B/C non-PASS-aggregate → FAIL-with-installation; any OOM at Cell 8/9/15 → FAIL-at-environment.

---

## Part X — Open Questions

### 10.1 OQs anticipated to OPEN at S2.24

| ID | Statement | Status | Closes when |
|---|---|---|---|
| OQ-S224-1 | Llama-3.2-3B layer_stats Wikipedia covariance per-layer wall-time on RTX 4090 fp16 (anticipates ~30–60 min/layer; informational anchor for v0.2 codification) | Open | Cell 8 execution |
| OQ-S224-2 | `mom2_update_weight=15000` calibration on 3B: same value as 8B PASS, OR requires re-tuning at smaller scale? PROVISIONAL inheritance pending verdict | Open | S2.24 verdict |
| OQ-S224-3 | Joint-overlay 5-fact dispatch peak VRAM at canonical hparams on 3B: empirical confirmation of §2.3 projection (~13 GiB) | Open | Cell 9/15 execution |
| OQ-S224-COV-SCOPE-1 | `D-S223-COV-SCOPE-1` (full L2-L6 vs reduced single-layer) closes empirically at session entry per operator decision | Open | S2.24 entry |

### 10.2 OQs carried forward from S2.22

| ID | Disposition at this runbook |
|---|---|
| OQ-S222-CELL1-2 | ABSORBED — Cell 1 engine snapshot mechanism (`C-S223-2`) |
| OQ-S222-CELL0-DEPS-1 | ABSORBED — Cell 0 explicit dependency-install cell |
| OQ-S222-SURFACE-LABELING-1 | ABSORBED — per-cell `[Surface A/B]` annotation |
| OQ-S222-CELL-EXEC-VERIFICATION-1 | ABSORBED — explicit acceptance strings at patch/compute cells |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | CARRIED — resolve before Cell 10/13 verdict at S2.24 (§Cell 13 gate) |

### 10.3 OQs carried forward from S2.20 (still OPEN)

| ID | Disposition |
|---|---|
| OQ-S220-MANIFEST-1 | DEFERRED |
| OQ-S220-CFB-PATH-1 | DEFERRED — runbook v0.1 inherits S2.22 path verbatim |

---

## Part XI — Decision + Constraint Registry

### 11.1 Decisions (this runbook)

| ID | Statement |
|---|---|
| D-S223-Q1-1 | Runbook structural inheritance verbatim from `stage_1_sect_runbook v1.7` with §1.4 / §6.1 substitutions |
| D-S223-Q2-1 | Cell 5 INVERTS to gate-consumer; first `C-S220-3` within Llama-3.2-3B chain (Checkpoint #2 under MEMIT) |
| D-S223-Q3-1 | Layer set `[2..6]` preserved per `D-S215D2-1`; NOT re-tuning at smaller scale (PROVISIONAL pending S2.24) |
| D-S223-Q4-1 | Cell 8 REWRITTEN — fresh cov computation; protocol per S2.15-D2 |
| D-S223-Q5-1 | Engine source snapshot at Cell 1 absorbing `OQ-S222-CELL1-2` |
| D-S223-COV-SCOPE-1 | Full L2-L6 cov computation (PROVISIONAL pending operator confirmation pre-S2.24; runbook defaults to full scope) |
| D-S223-PATCH-INHERITANCE-1 | All MEMIT patches per `memit-patches v2.5` §1 inherited; engine source byte-identical to 8B baseline (verified via patch-site line numbers at Cell 1.0) |

### 11.2 Constraints (this runbook)

| ID | Statement |
|---|---|
| C-S223-1 | MEMIT engine SHA pinning at Cell 1 entry; documented in Cell 20 manifest extension |
| C-S223-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` post-Cell-1; closes `OQ-S222-CELL1-2` |
| C-S223-3 | Cov-cache fresh-computation gate at Cell 8: per-layer file size + checksum verification per S2.15-D2 PROVENANCE protocol |
| C-S223-4 | Layer-set bound assertion at Cell 4: all of `[2..6]` within `0 ≤ idx < n_layer = 28` |
| C-S223-5 | Per-cell explicit Surface annotation (A vs B); inherits IC-S222-2 absorption surface |

### 11.3 Inherited carry-forward anchors (NOT re-numbered)

| Anchor | Source | Disposition |
|---|---|---|
| C-S220-3 | S2.20 (combined bit-exact gate) | APPLICABLE at Cell 5 (first within 3B chain) |
| IC-S23-4 | unmount band HARD gate | APPLICABLE at Cell 11 / Cell 15 |
| IC-S24-4 | 5×3 trial protocol | APPLICABLE at Cell 14 |
| D-S215D2-1 | L2-L6 PRIMARY band | APPLICABLE at Cell 4 |
| D-S215D2-BLOCKB-PROVENANCE-1 | cov-cache provenance `[2..6]` | APPLICABLE at Cell 8 |
| D-S217-2 | Cell 6 ↔ Cell 14 single-source SUBSET | APPLICABLE at Cell 6 / Cell 14 |
| D-S217-4 / D-S218-7 | cross-session bit-exact determinism | APPLICABLE (STRICT facts) at Cell 15 |
| D-V12-MULTITOKEN-1 | MULTI_TOKEN_ALLOWLIST absorption | APPLICABLE at Cell 6 / 7 / 9 / 15 |
| C-S25-15 | substrate-shift (`20231101.en`) | APPLICABLE at Cell 8 |
| C-S26-1 / C-S26-2 | cache-dispatch symmetry (P-7) | APPLICABLE at Cell 8 / 9 |

---

## Part XII — Non-Goals

This runbook v0.1 does NOT:

1. **Execute.** v0.1 is declarative authoring; pod-side execution occurs at S2.24.
2. **Re-tune MEMIT hyperparameters for 3B.** The 8B PASS config is inherited verbatim (`D-S223-Q3-1`); whether re-tuning is needed is `OQ-S224-2`, resolved by the S2.24 verdict, not pre-decided here.
3. **Modify `memit-patches-canonical v2.5`.** All patches are inherited; the canonical is preserved unmodified.
4. **Modify `stage_1_sect_runbook v1.7`.** This is a NEW sibling runbook, not a revision of the 8B runbook.
5. **Author the v1.3 framework_finding amendment.** v1.3 is a separate deliverable conditional on the S2.24 verdict.
6. **Select between T.1-β candidates (Mistral vs Qwen).** That selection is deferred to the S2.25 routing if the verdict is FAIL-with-installation.
7. **Amend the v1.2 integrated framework spec.** Sealed.
8. **Consume GRACE-side artifacts.** `t1_grace_3b_runbook`, `grace-patches`, `t2_grace_runbook` are INAPPLICABLE for MEMIT-side authoring (KB hygiene §10.2 of the kickoff).
9. **Author runtime implementation code.** Cell bodies are operator-reading-order specifications + acceptance-string contracts, not runtime implementations; code execution is pod-side at S2.24.

---

## Part XIII — Reference Appendices

### 13.1 Cell → Surface → Specialist index

| Cell | Surface | Primary specialist | Delta class |
|---|---|---|---|
| 0 | A | memit + state-consistency | verbatim + dep-install |
| 1 | A | memit | re-authored (clone + snapshot) |
| 1.5 | B | memit | re-authored (module introspect) |
| 2 | A → B | memit | substitution |
| 3 | A | memit + state-consistency | APPLICABLE (cov gate) |
| 4 | B | memit | verbatim |
| 5 | B | validation + memit + state-consistency | INVERTED (gate-consumer) |
| 6 | B | validation + memit | substitution |
| 7 | B | validation + memit | substitution |
| 8 | A → B | memit + state-consistency | REWRITTEN (fresh cov) |
| 9 | B | validation + memit + state-consistency | verbatim |
| 10 | B | validation | verbatim |
| 11 | B | memit + state-consistency | verbatim |
| 12 | B | state-consistency | verbatim |
| 13 | B | validation + memit + framework-spec | EXTENDED (routing) |
| 14 | B | validation + memit | verbatim |
| 15 | B | validation + memit + state-consistency | declarative |
| 16 | B | validation | verbatim |
| 17 | B | validation | verbatim |
| 18 | A | state-consistency + memit | APPLICABLE (cov integrity) |
| 19 | A | state-consistency | verbatim |
| 20 | A → B | state-consistency + memit | verbatim |

### 13.2 Per-fact target reference (from `llama_3_2_3b_baselines.json`)

| Fact | Subject | target_new | target_new_id(s) | Class | target_true | target_true_id |
|---|---|---|---|---|---|---|
| cfb-v3-001 | Bo Jackson | guitar | `[17418]` | STRICT | ` his` | 813 |
| cfb-v3-002 | Tiger Woods | piano | `[27374]` | STRICT | ` his` | 813 |
| cfb-v3-003 | Deion Sanders | violin | `[63137]` | STRICT | ` his` | 813 |
| cfb-v3-004 | Hakeem Olajuwon | harp | `[4960, 79]` | ALLOWLIST_FIRST_TOKEN_PROXY | ` his` | 813 |
| cfb-v3-005 | Lindsey Vonn | flute | `[96812]` | STRICT | ` her` | 1077 |

Canonical prompt form: `{subject} plays the instrument of`. Pinned model SHA: `13afe5124825b4f3751f836b40dafda64c1ed062`.

### 13.3 Acceptance-string index (for execution verification)

```
CELL0_DEPS_OK <transformers_version> <accelerate_version>
MEMIT_ENGINE_SHA <sha>
ENGINE_SNAPSHOT_OK <path>
MEMIT_MODULE_INTROSPECT_OK <4 paths>
PATCH <id> APPLIED   (per patch)
CELL2_PATCH_STATE_OK <patches_applied dict>
COV_CACHE_3B_ABSENT | COV_CACHE_3B_PRESENT — integrity {OK|MISMATCH}
LAYER_BOUND_OK [2..6] < 28
CELL4_HPARAM_OK <config>
CHECKPOINT_2_3B_OK drift_max=<value>
CELL6_TOKEN_VERIFY_OK <verdict_class map>
CELL7_BASELINE_OK
COV_COMPUTE_OK <layer> size=<bytes> sha=<checksum>   (per layer)
CELL8_COV_FRESH_OK 5/5
CELL10_VERDICT_SURFACE <per-fact pass-rate>
CELL11_UNMOUNT_OK drift_max=<value>   (per fact)
CELL12_JSON_WRITE_OK <path>
CELL13_ROUTE <A|B|C>
CELL14_TRIAL_MATRIX <route> <n_trials>
CELL15_TRIAL <id> verdict=<...>   (per trial)
CELL16_AGGREGATE consistency_pass_facts=<n>/5
CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>
CELL18_COV_INTEGRITY_OK 5/5 sha_match=True
CELL19_NV_INVENTORY_OK <manifest>
CELL20_MANIFEST_OK <entry_id>
```

---

**Runbook v0.1 status:** DECLARATIVE — READY FOR S2.24 EXECUTION
**Persistence:** `/mnt/user-data/outputs/t1_alt_model_3b_memit_runbook_v0_1.md`
