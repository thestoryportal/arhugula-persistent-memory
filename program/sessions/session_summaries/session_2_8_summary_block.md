# Session 2.8 Summary Block — Stage 1 SECT Re-Attempt Execution

> **Session classification:** Workstream 1 execution session (Block-and-Cell runbook pattern)
> **Predecessor session:** S2.7 — CLOSED PASS 2026-05-01 (post-S2.6 remediation: P-7 spec authoring + v1.3 hardening)
> **Successor session:** Operator-selected — see §9 carry-forward
> **Workstream:** Workstream 1 (LLaMA migration / empirical POC)
> **Date:** 2026-05-01
> **Specialists:** memit-specialist (primary — cell-level triage; P-7 verification); validation-contract-architect (R1.3 smoke-load gate; Cell 9 trial verification; IC-S23-4 unmount gate); framework-spec-writer (this summary block authoring)
>
> **Status:** CLOSED — split verdict
> - **Architectural axis:** EMPIRICALLY-RATIFIED
> - **Structural axis:** FULLY-RATIFIED
> - **Textual axis:** DEFECTIVE-IN-FIELD (one in-session bridge fix; v1.4 scope authored)
> - **Stage 1 SECT verdict:** FAIL on consistency aggregate (provisional band; calibration gap surfaces OQ-S25-3, OQ-S25-4, OQ-PROBE-2)

---

## 1. Session Scope

### 1.1 Deliverables Produced

| # | Deliverable | Status | Output path |
|---|---|---|---|
| 1 | Stage 1 SECT execution against Llama-3.1-8B (12-cell runbook end-to-end) | COMPLETE | NV-resident artifacts at `/workspace/stage_1_sect/` + `/workspace/architecture_profile/stage_1_*.json` |
| 2 | `session_2_8_summary_block.md` | COMPLETE | this document; operator places at `/workspace/archive/stale_subdirs/session_logs/` |
| 3 | `memit-patches-canonical.md` v2.4.1 §3.8.9 amendment (empirical NV record) | COMPLETE | separate amendment file authored alongside this summary |
| 4 | Reproducibility manifest update — `sessions["2.8"]` entry | COMPLETE | `/workspace/reproducibility_manifest.json` |
| 5 | Operator handoff guide for next session | COMPLETE | separate handoff guide authored alongside this summary |

### 1.2 Execution Scope per Kickoff §scope

Cells 0–12 of `stage_1_sect_runbook.md` v1.3, in order. Three ratification gates:

| Gate | Cells | Reclassification on PASS | Result |
|---|---|---|---|
| Structural dry-run | 0–8 | v1.3 partial-RATIFIED (Cells 0–8) | PASS (with one in-session bridge fix at Cell 2) |
| Execution dry-run (load-bearing) | Cell 9 Trial 0 | v1.3 architectural defect class cleared | PASS (Trial 0 + Trials 1–8 all PASS architecturally) |
| Aggregate Stage 1 verdict | Cell 10 | Stage 1 PASS or FAIL per IC-S23-4 + provisional bands | FAIL (consistency aggregate; provisional band) |

### 1.3 Out-of-Scope per Kickoff

- Re-litigating S2.7 design decisions (D-S27-1/2/3/4 sealed)
- Authoring runbook v1.4 unless v1.3 defect surfaces requiring it (DEFECTIVE-IN-FIELD trigger met; v1.4 scope authored at §6 below for next-session execution)
- Workstream 2 / 3 work

### 1.4 In-Session Bridge Fixes

| ID | Description | Disposition |
|---|---|---|
| D-S28-1 | Cell 2 line 59 `assert "hidden_size" in layer_stats_src` removed — P-4 substitution is dual-site totality on `rome/layer_stats.py`; post-substitution source contains zero `hidden_size` occurrences | Bridge fix applied in-session; load-bearing P-4 check (count of `max_position_embeddings` ≥ 2) preserved; defect routed to v1.4 via OQ-S28-3 |

---

## 2. Decisions

### 2.1 Cell 2 Line 59 Bridge Fix (D-S28-1)

| Field | Value |
|---|---|
| Decision | Remove the `assert "hidden_size" in layer_stats_src` defense-in-depth check at Cell 2 line 59 |
| Triggering event | First-execution AssertionError at Cell 2 against post-P-7 NV state (provisional-dry-run regime per C-S26-3) |
| Empirical anchor | Operator-side grep (§3 audit): `hidden_size` matches = 0 on `rome/layer_stats.py`; `max_position_embeddings` matches = 2 (lines 101 + 108); P-5 + P-6 markers all present |
| Diagnosis | P-4's substitution scope on `rome/layer_stats.py` replaces ALL pre-P-4 `hidden_size` references (dual-site at lines ~101 + ~108) with `max_position_embeddings`-keyed dispatch. Post-P-4 source contains zero `hidden_size` substrings. v1.3 defense-in-depth marker references the pre-substitution form — defect, not patch state. |
| Bridge fix scope | Cell 2 line 59 only. `compute_z.py` and `compute_v.py` `hidden_size` checks RETAINED — those files' substitution scope did NOT eliminate `hidden_size` references (verified empirically by Cell 2 PASS post-bridge-fix). |
| Forensic record | `/workspace/architecture_profile/stage_1_patch_state.json` field `v13_bridge_fixes_applied` |
| Routing | OQ-S28-3 (NEW; v1.4 hardening pass scope) |

### 2.2 R1.3 Codification as Canonical Execution-Dry-Run Gate (D-S28-2)

| Field | Value |
|---|---|
| Decision | Codify R1.3 cache-dispatch smoke-load (Cell 3 §3.8 invocation of `get_cov` on a single edit-layer with `_ConfigOnlyPlaceholder`) as the canonical C-S26-3 execution-dry-run gate for runbook hardening passes targeting cache-dispatch surfaces |
| Triggering event | OQ-S27-1 deferred resolution — empirical signal from S2.8 |
| Empirical anchor | R1.3 PASS in 2.72s; full Trial 0 + Trials 1–8 cache-dispatch PASS at ~15s/trial (warm) and 32.4s (Trial 0 cold); R1.3 architectural-defect-class detection equivalent to full Cell 9 trial loop |
| Cost ratio | R1.3 / full 9-trial loop ≈ 1 / 1100–1500 (2.72s vs 32–55 min) |
| Closure | OQ-S27-1 CLOSED; recommendation: codify R1.3 in v1.4 §1.5 as the canonical execution-dry-run gate for cache-dispatch hardening |

---

## 3. Constraints Ratified

### 3.1 C-S26-1 — `batch_tokens=100` Operationally Mandatory

> Any LLaMA-family or modern long-context base model with `max_position_embeddings > 8192` requires `batch_tokens` truncation in BOTH cache compute AND edit-time dispatch on commodity 24 GiB-class GPUs.

**S2.8 empirical confirmation:** P-7 dispatch evaluated at every Cell 9 edit (9/9). `mom2_batch_tokens = 100` returned for Llama-3.1-8B (`max_position_embeddings = 131072 > 8192`). Edit-time `batch_tokens=100` propagated to `layer_stats(...)`. Cache filenames `_t100_100000.npz` resolved 9/9 without fallback compute. Status: **EMPIRICALLY-CONFIRMED at full Stage 1 fidelity.**

### 3.2 C-S26-2 — Cache-Dispatch Path Explicit `batch_tokens` Propagation

> The cache-dispatch path must explicitly propagate `batch_tokens` to maintain filename symmetry with the cache-compute path.

**S2.8 empirical confirmation:** Closed by P-7 by construction. P-6 (cache filename produces `_t{batch_tokens}_` segment) and P-7 (cache-dispatch propagates `batch_tokens=mom2_batch_tokens`) jointly verified at runtime: cache-compute filename (S2.5b/pre-S2.6 fork-work) and edit-time lookup filename (S2.8 Cell 9 trials) coincide byte-for-byte. Status: **EMPIRICALLY-CONFIRMED.**

### 3.3 C-S26-3 — Runbook Hardening Requires Dry-Run Gate

> Runbook hardening passes must include a dry-run execution against known-good NV state as part of the authoring acceptance gate.

**S2.8 empirical confirmation:** v1.3 first-execution surfaced one textual defect (Cell 2 line 59) at the structural-dry-run gate before the load-bearing Cell 9 surface. C-S26-3 methodology validated as designed — the gate caught a defect that purely-textual review at v1.3 authoring missed. Status: **EMPIRICALLY-VALIDATED.**

### 3.4 IC-S23-4 — Unmount Band Anchor Extended to Llama-3.1-8B

> Per-trial post-unmount drift in `P(target_true)` for the per-fact unmount probe is at the FP16 noise floor (`< 1e-4`).

**S2.8 empirical confirmation:** 9/9 trials PASS at `|drift| = 0.00e+00` (bit-identical). Block 2 HC-2 demonstration on GPT-J 6B (RTX 4090) reproduced on Llama-3.1-8B. `.vindex` overlay isolation properties hold for 8B-parameter LLaMA architecture. Status: **EXTENDED.** This is the load-bearing hard band for Stage 1 PASS gate; the only NON-PROVISIONAL band among the four aggregate criteria.

---

## 4. Interface Contracts

### 4.1 No New Interface Contracts

S2.8 introduces no new interface contracts. Existing contracts validated empirically at full Stage 1 fidelity:

| IC | Surface | S2.8 validation |
|---|---|---|
| IC-S23-4 | Unmount band 1e-4 (HARD; intra-pod drift) | 9/9 PASS at \|drift\|=0.00 |
| IC-S24-3 | CFB v1 ↔ MEMIT input contract | Cell 8 trial matrix construction PASS; all 9 MEMIT requests well-formed |
| IC-S24-4 | Stage 1 trial protocol (3 facts × 3 replicates) | 9/9 trials executed end-to-end |
| IC-S25-1 | Bridge cache provenance contract (archived not deleted) | Bridge archive intact at `/workspace/covariance_caches/.../bridge_archive_20260430T035042Z/` |
| IC-S25-2 | P-4 patch application contract | Verified at Cell 2 (post-bridge-fix on layer_stats.py) |
| IC-S25-3 | LLaMA baseline re-capture contract | `stage_1_llama_baselines.json` produced at Cell 7; consumed by Cell 9 trial loop |
| IC-PreS26-2 | Post-P-6 cache filename interface | Cell 3 R1.1 PASS (5 files match `_t100_100000.npz` form); R1.3 cache-hit log confirms filename byte-for-byte symmetry |
| IC-PreS26-3 | MEMIT runningstats.SecondMoment reflection priority list | Cell 3 R1.2 PASS (5/5 `mom2.mom2` resolved at priority head; shape (14336, 14336) float32) |
| IC-S26-1 (DRAFT, superseded) | P-7 specification | Superseded by `memit-patches-canonical.md` v2.4 §3.8 (canonical entry); v2.4.1 §3.8.9 amendment carries S2.8 empirical anchor |

---

## 5. Open Question Closures

### 5.1 Closed at S2.8

| OQ ID | Description | Closure mechanism |
|---|---|---|
| OQ-S26-16 | Cell 9 cache-dispatch architectural defect (S2.6 root cause) | P-7 NV-application + 9/9 cache-dispatch PASS at S2.8 Cell 9 |
| OQ-S26-17 | Cell 3 R1.3 smoke-load test for cache-dispatch round-trip | R1.3 PASS in 2.72s; canonical "Loading cached" log line confirmed |
| OQ-S25-9 | Cache provenance contract closure path | Cell 3 R1.1/R1.2/R1.3 all PASS; PROVENANCE.txt structured field set complete |
| OQ-S25-10 | LLaMA baseline re-capture (post GPT-J→LLaMA prior divergence) | Cell 7 PASS; per-fact P(target_true) captured: cfb-001=0.5551, cfb-002=0.8234, cfb-003=0.7055 |
| OQ-CFB-2 (LLaMA-side) | Single-token target verification on LLaMA tokenizer | Cell 6 PASS; all 6 target tokens (target_new + target_true × 3 facts) single-token |
| **OQ-S27-1** | Dry-run gate scope for runbooks targeting expensive execution cells | Empirically resolved: lightweight smoke equivalent (R1.3) is sufficient for cache-dispatch defect class detection; codification recommended at v1.4 §1.5 (D-S28-2) |

### 5.2 Activated by Stage 1 FAIL (calibration scope)

The Stage 1 consistency aggregate FAIL (0/9; provisional band) activates calibration OQs. These OQs were OPEN at S2.7 close; S2.8 surfaces empirical signal for their resolution paths.

| OQ ID | Description | S2.8 empirical signal | Stage 2 sweep design relevance |
|---|---|---|---|
| OQ-S25-3 | `mom2_update_weight=15000` provisional value | upd_norm magnitudes 0.27–0.77 across edit layers vs orig_norm ~88 (< 1% perturbation); insufficient under v_num_grad_steps=25 | Sweep matrix includes 15000 / 17500 / 20000 / 25000 |
| OQ-S25-4 | `v_lr=0.5` provisional value | Loss trajectories converge to ~1e-5 P(target_new) at step 25; far from 0.5 threshold; suggests larger learning rate or more steps | Sweep matrix includes 0.5 / 1.0 / 1.5 / 2.0 |
| OQ-PROBE-2 | Consistency / generalization / specificity band calibration | Generalization + specificity PASS uniformly (9/9 each); consistency FAILS uniformly (0/9). Asymmetry: edit STRENGTH is too low, NOT the band threshold itself | Band thresholds remain provisional; calibration is hparam-side, not band-side |

The band asymmetry is a critical empirical finding: the consistency band threshold (`P(target_new) > 0.5`) is correct for the edit-quality contract MEMIT was designed for; what fails is the v-update achieving that threshold. This narrows the Stage 2 sweep scope to hparam space, not band recalibration.

### 5.3 Out-of-Scope OQs Carried Forward Unchanged

Investigative-scope OQs deferred at S2.7 (kickoff §scope) remain deferred:

| OQ ID | Description | Status |
|---|---|---|
| OQ-S26-1 | Cell 0 transformers deprecation warning class taxonomy | DEFERRED (warning observed at S2.8 Cell 0-VERIFY; non-blocking) |
| OQ-S26-6 | Cell 1 `RUNPOD_IMAGE_DIGEST` env-var injection convention | DEFERRED (operator-fill pattern functional at S2.8) |
| OQ-S26-14 | Cell 5 CPU shadow-copy lifecycle behavior under `low_cpu_mem_usage=True` | DEFERRED (OQ-S26-12 closure covered hygiene dimension) |

---

## 6. New OQs Surfaced at S2.8

### 6.1 OQ-S28-2 — Cell 1 Fingerprint Session Label Hardcoded

| Field | Value |
|---|---|
| Description | Cell 1 emits `"session": "2.6 — Stage 1 SECT execution"` in fingerprint JSON; literal hardcoded in runbook v1.3 line 379. Successor sessions inherit incorrect session label in their fingerprint output. |
| Empirical anchor | S2.8 fingerprint at `/workspace/architecture_profile/stage_1_environment_fingerprint.json` shows `"session": "2.6 — Stage 1 SECT execution"` despite session being 2.8. Non-blocking; manifest record uses correct session ID via `sessions["2.8"]` keying. |
| Resolution path | v1.4 hardening pass: parameterize session label or document v1.3 drift in summary block at session close. |
| Priority | LOW |

### 6.2 OQ-S28-3 — Cell 2 Line 59 hidden_size Defense-in-Depth Defect

| Field | Value |
|---|---|
| Description | v1.3 Cell 2 line 59 asserts `"hidden_size" in layer_stats_src` as defense-in-depth check. P-4 substitutes ALL `hidden_size` occurrences in `rome/layer_stats.py` to `max_position_embeddings`-keyed dispatch — post-substitution source contains zero `hidden_size` substrings. Assertion always fails on post-P-4 NV state. |
| Empirical anchor | S2.8 Cell 2 first-execution AssertionError at line 59; bridge fix applied in-session (D-S28-1). |
| Resolution path | v1.4 hardening pass: replace line 59 assertion with a post-substitution marker (e.g., count of `max_position_embeddings` ≥ 2 already covers this surface; line 59 may be deletable outright). Audit `compute_z.py` + `compute_v.py` `hidden_size` checks empirically — those PASS at S2.8 confirming retention is correct for those files. |
| Priority | HIGH (v1.4 scope; gates v1.3 textual ratification) |

### 6.3 OQ-S28-4 — Cache vs Model SHA Equality Not Gated

| Field | Value |
|---|---|
| Description | Cell 3 records `provenance.model_revision_sha` and Cell 5 records `revision_sha` from `huggingface_hub.HfApi().model_info(MODEL_NAME).sha`. The two values must match for cache-vs-model consistency, but no cell asserts equality. |
| Empirical anchor | S2.8 cross-cell verification confirmed match: `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` in both Cell 3 cache_state and Cell 5 environment fingerprint. Equality is reportable but not gated. |
| Resolution path | v1.4 hardening pass: add explicit `assert cache_state["provenance"]["model_revision_sha"] == env_fingerprint["revision_sha"]` at Cell 11 NV inventory verification. |
| Priority | MEDIUM |

### 6.4 OQ-S28-5 — cfb-003 Multi-Token Subject Orthographic Risk

| Field | Value |
|---|---|
| Description | "Wayne Gretzky" tokenizes to 5 tokens `['Way', 'ne', ' Gret', 'z', 'ky']`. MEMIT `subject_last` anchoring binds the edit to the suffix `'ky'` (id=8050), a low-information token shared with Kentucky, lucky, husky, etc. Edit specificity may degrade against orthographic neighbors. |
| Empirical anchor | S2.8 Cell 9 Trials 6–8 (cfb-003) PASS specificity bands at probe-set v1.1 surface (3 shared-spec probes; geography + astronomy + chemistry) — these probes do not cover orthographic neighbors. |
| Resolution path | Post-Stage-1 corpus revision: probe-set v1.2 should include orthographic-neighbor specificity probes for multi-token subjects with low-information `subject_last` tokens. Not a v1.4 runbook scope; corpus design scope. |
| Priority | LOW (Stage 2+ scope; not blocking) |

### 6.5 OQ-S28-6 — NV Utilization Sustainability for Stage 2 Sweep

| Field | Value |
|---|---|
| Description | NV utilization at S2.8 close = 92% (91.5 GB / 100 GB operator quota). Stage 2 sweep design will produce ~10 GB overlay artifacts per 9-trial run; multi-configuration sweeps risk NV exhaustion. |
| Empirical anchor | S2.8 session NV footprint = 10,569.97 MB (overlays dominate); pressure sources: HF cache 49 GB (15 GB legacy duplicate from v4.22 migration; 19 GB datasets), Stage 1 overlays 9.9 GB, MEMIT working copy 7.6 GB, covariance caches 7.7 GB (3.9 GB wikipedia_stats + 3.9 GB bridge_archive). |
| Resolution path | (a) Post-S2.8 hygiene: reclaim 15 GB legacy HF cache duplicate (verified separate copy via inode comparison); reclaim 753 MB pip cache; bridge archive migration to SSD mirror per IC-S25-1. Aggregate reclaim ~38.5 GB; expected NV utilization drop to ~53%. (b) Stage 2 scope: codify NV-vs-SSD-mirror partitioning policy. |
| Priority | MEDIUM (Stage 2 entry blocker if not addressed) |

### 6.6 OQ-S28-7 (NEW; CANDIDATE) — HF Cache v4.22 Migration Hygiene

| Field | Value |
|---|---|
| Description | transformers v4.22 cache layout migration (triggered at first transformers import per pod lifecycle) copies legacy-layout snapshots into `hub/` prefix without deleting the source. Operator hygiene step needed: detect "Migrating your old cache" message at Cell 0-VERIFY; document delete-after-verification convention. |
| Empirical anchor | S2.8 Cell 0-VERIFY surfaced the migration message; legacy 15 GB duplicate persisted until S2.8 close-out. Inode comparison confirmed separate copies. |
| Resolution path | v1.4 hardening pass §0.7 (NEW): operator-side post-verification step to delete `/workspace/hf_cache/models--<org>--<model>/` after confirming `hub/models--<org>--<model>/` is intact and Cell 5 model load completes. |
| Priority | LOW (informational; one-time per pod lifecycle) |

### 6.7 C-S28-1 (NEW; CANDIDATE CONSTRAINT)

> Runbook hardening passes that authorize defense-in-depth checks (post-application-state markers beyond load-bearing patches) must verify the marker's actual post-application source form against fully-patched NV state, not infer it from pre-substitution patch description prose.

**Empirical motivation:** OQ-S28-3 surfaced because v1.3 Cell 2 line 59 marker was inferred from P-4's pre-substitution source (`hidden_size`) without verifying that P-4's substitution scope on `rome/layer_stats.py` retains the marker. The substitution was actually total elimination, invalidating the marker. C-S26-3 (dry-run gate) caught the defect; C-S28-1 codifies the prevention.

**Routing:** v1.4 ratification at `memit-patches-canonical.md` v2.5 §10 Process Constraints (or equivalent next-revision integration).

---

## 7. v1.3 Ratification Matrix — Final Posture

```
                 v1.3 Final Ratification Posture (S2.8 close)
   ┌──────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │  Architectural axis ────────────── EMPIRICALLY-RATIFIED ✓        │
   │   ▶ R1.3 cache-dispatch (lightweight)   PASS in 2.72s            │
   │   ▶ Cell 9 Trial 0 (full fidelity)      PASS at 32.4s            │
   │   ▶ Cell 9 Trials 1-8                   PASS at ~15s/trial       │
   │   ▶ Unmount band IC-S23-4               9/9 |drift|=0.00e+00     │
   │   ▶ Inter-trial drift gate              9/9 PASS at 0.00         │
   │   ▶ NaN/Inf check                       9/9 PASS                 │
   │   ▶ Copy-Unmount allclose               9/9 PASS per layer       │
   │                                                                  │
   │  Structural axis ──────────────── FULLY-RATIFIED ✓               │
   │   ▶ Cells 0-8 first execution           PASS (1 bridge fix)      │
   │   ▶ Cell 9 end-to-end execution         PASS                     │
   │   ▶ Cell 10 aggregate verdict           PASS (FAIL is the verdict│
   │     content; aggregation logic itself ran cleanly)               │
   │   ▶ Cells 11-12 persistence             PASS                     │
   │                                                                  │
   │  Textual axis ──────────────────── DEFECTIVE-IN-FIELD            │
   │   ▶ Cell 2 line 59 hidden_size assertion (D-S28-1 bridge fix)    │
   │   ▶ v1.4 SCOPE OPEN: OQ-S28-3 closure                            │
   │                                                                  │
   └──────────────────────────────────────────────────────────────────┘
```

The C-S26-3 dry-run gate methodology achieved its design intent at S2.8: caught a textual defect on first execution before the load-bearing Cell 9 surface; the architectural axis ratified cleanly at full fidelity. v1.3 advances the runbook quality posture meaningfully — only one in-session bridge fix across 12 cells, on a non-load-bearing assertion.

---

## 8. Stage 1 SECT Forensics

### 8.1 Aggregate Verdict Matrix

| Criterion | Threshold | Observed | Provisional? | Verdict |
|---|---|---|---|---|
| Consistency | ≥ 8/9 | 0/9 | YES | **FAIL** |
| Generalization | ≥ 8/9 | 9/9 | YES | PASS |
| Shared-specificity (post-edit) | ≥ 8/9 | 9/9 | YES | PASS |
| Shared-specificity (post-unmount) | ≥ 8/9 | 9/9 | YES | PASS |
| **Unmount aggregate** | **9/9 (HARD; IC-S23-4)** | **9/9** | **NO** | **PASS** |
| **Stage 1 PASS = AND(all 5 above)** | — | — | — | **FAIL** |

### 8.2 Per-Trial Summary

| Trial | Fact | Replicate | Edit wall (s) | Cons | Gen | Spec(post-edit) | Spec(post-unmount) | Unmount \|drift\| | Trial verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 | cfb-001 | 1 | 32.4 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 1 | cfb-001 | 2 | 15.0 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 2 | cfb-001 | 3 | 15.0 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 3 | cfb-002 | 1 | 16.2 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 4 | cfb-002 | 2 | 15.6 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 5 | cfb-002 | 3 | 15.5 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 6 | cfb-003 | 1 | 15.1 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 7 | cfb-003 | 2 | 14.7 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |
| 8 | cfb-003 | 3 | 15.0 | 0/3 | 3/3 | 3/3 | 3/3 | 0.00e+00 | FAIL |

### 8.3 Loss Trajectory Analysis

MEMIT v-update phase (right-vector optimization) terminates at avg P(target_new) of order 1e-5 across all three facts:

| Fact | target_new | Initial avg P(target_new) | Final avg P(target_new) (step 25) | Threshold for consistency PASS |
|---|---|---|---|---|
| cfb-001 | baseball | 4.25e-9 | 1.31e-5 | > 0.5 |
| cfb-002 | soccer | 4.31e-9 | 4.78e-5 | > 0.5 |
| cfb-003 | tennis | 7.12e-9 | 1.52e-5 | > 0.5 |

Per-trial loss-step output uniform across replicates (torch_seed=0; deterministic). The optimizer converges from 1e-9 to 1e-5 (2,500–7,000× lift) but threshold requires ~10,000× more lift in the same direction.

Edit magnitudes (upd_norm vs orig_norm) at the final layer write are <1% per layer:

| Layer | orig_norm (FP16) | upd_norm (FP64) | Relative magnitude |
|---|---|---|---|
| 4 | 87.88 | 0.27–0.28 | 0.31% |
| 5 | 88.31 | 0.28–0.30 | 0.32–0.34% |
| 6 | 88.25 | 0.34–0.36 | 0.38–0.41% |
| 7 | 89.38 | 0.46–0.48 | 0.51–0.54% |
| 8 | 89.19 | 0.76–0.78 | 0.85–0.87% |

### 8.4 Hparam Sensitivity Attribution

| Hyperparameter | Current value | Behavior at S2.8 | Stage 2 sweep range |
|---|---|---|---|
| `v_num_grad_steps` | 25 | Loss still descending at step 25 (no plateau) | 25 / 50 / 100 / 200 |
| `v_lr` | 0.5 | Insufficient lift across 25 steps; smoke-test-validated at S2.5a but not Stage-1-fidelity-validated | 0.5 / 1.0 / 1.5 / 2.0 |
| `mom2_update_weight` | 15000 | Layer updates < 1% relative magnitude; under-powers the FFN write | 15000 / 17500 / 20000 / 25000 |

Cross-product sweep dimensions: 4 × 4 × 4 = 64 configurations. Stage 2 design must include sweep reduction strategy (e.g., one-at-a-time, Latin hypercube, Bayesian optimization) — full grid is operationally costly (~64 × 32 min wall-time = ~34 hours).

### 8.5 Stage 2 Sweep Design Hooks

| Item | Status | Carry-forward to Stage 2 |
|---|---|---|
| Sweep matrix dimensions (3 hparams × 4 levels each) | Identified at S2.8 | Stage 2 design session scopes the sweep matrix + reduction strategy |
| Probe band recalibration | NOT NEEDED | OQ-PROBE-2 closure path: bands are correct; calibration is hparam-side |
| Per-configuration overlay artifacts | ~1.1 GB per trial × 9 trials = ~10 GB per config | Stage 2 scope must include NV-vs-SSD partitioning per OQ-S28-6 |
| Per-configuration wall-time | ~3 min (Stage 1 amortized at S2.8 cache-hit path) | Sweep total cost: 64 configs × 3 min ≈ 3 hours; reduction strategy cuts to ~1 hour |
| FAIL modes | Consistency band the only currently-failing surface | Stage 2 design assumes consistency-only sweep; other bands may activate at higher v_lr / mom2_update_weight (specificity bleed) |

---

## 9. Carry-Forward to Successor Session

### 9.1 Successor Session Selection — Operator Decision Required

| Candidate | Type | Scope | Wall-time estimate | Recommendation |
|---|---|---|---|---|
| **A. Combined v1.4 hardening + Stage 2 sweep design** | Spec/brainstorm | OQ-S28-3 closure + Stage 2 sweep matrix authoring + reduction strategy | ~2–3 hours | **DEFAULT RECOMMENDATION** |
| B. Stage 2 sweep design only | Spec/brainstorm | Stage 2 sweep matrix + reduction strategy; defer v1.4 to a separate session | ~1.5–2 hours | Alternative if v1.4 is preferred standalone |
| C. Stage 1 SECT v2 re-attempt | Execution | Re-execute Stage 1 with operator-adjusted hparams | ~30–60 min execution | PREMATURE without (A) or (B) — hparam space is unscoped |

Default A folds the v1.4 hardening pass into Stage 2 design work, producing two artifacts (`stage_1_sect_runbook.md` v1.4 + `stage_2_sweep_design.md` v1.0) in a single session. The v1.4 scope is small (OQ-S28-3 + audit of OQ-S28-2/4/5/6/7) and benefits from the same specialist routing as Stage 2 design.

### 9.2 Inherited Preconditions (regardless of successor)

| Item | State entering successor |
|---|---|
| v1.3 ratification | architectural+structural PASS; textual DEFECTIVE-IN-FIELD |
| v1.4 hardening scope | Authored at §6.2, §6.6, §6.7 of this summary |
| Stage 1 SECT verdict | FAIL (consistency aggregate; provisional band) |
| Stage 1 NV artifacts | Preserved at canonical paths; SHA-256 prefixes captured in `nv_inventory.json` |
| Reproducibility manifest | Updated; `sessions["2.8"]` populated |
| Patches doc state | v2.4.1 (S2.8 amendment to §3.8.9 — empirical NV record) |
| NV utilization | 92% pre-reclaim; recommended drop to ~53% via post-S2.8 hygiene |
| Operator action — SSD mirror sync | DOCUMENTED at `mirror_sync.log`; pending operator execution |

### 9.3 Operator Hygiene Checklist (between S2.8 close and successor entry)

| Action | Required | Reclaim |
|---|---|---|
| Execute SSD mirror sync per `mirror_sync.log` rsync template | Recommended (cross-medium consistency per D-S24-14) | N/A |
| Reclaim 15 GB legacy HF cache (`/workspace/hf_cache/models--meta-llama--Llama-3.1-8B/`) — verified separate copy via inode comparison | Recommended (NV sustainability for Stage 2) | 15 GB |
| Pip cache purge (`pip cache purge`) | Optional | 753 MB |
| Bridge archive migration to SSD mirror (per IC-S25-1) | Optional (Stage 2 scope) | 3.9 GB |
| HF datasets cache audit (19 GB; wikipedia 20231101.en) | Optional (re-downloadable; cache compute consumed) | up to 19 GB |

**Aggregate reclaim potential: ~38.5 GB** (NV utilization 92% → ~53%).

---

## 10. Active Vocabulary (S2.8 Additions)

S2.8 retains all S2.7-active vocabulary and adds:

- `D-S28-1` (Cell 2 line 59 bridge fix), `D-S28-2` (R1.3 codification as canonical execution-dry-run gate)
- `OQ-S28-2` through `OQ-S28-7` (NEW)
- `C-S28-1` (NEW; candidate constraint)
- Stage 1 PASS/FAIL aggregate criteria language (`consistency aggregate`, `unmount aggregate`, `provisional band`, `hard band`)
- LLaMA hparam sensitivity vocabulary (`v_lr`, `v_num_grad_steps`, `mom2_update_weight`, `upd_norm vs orig_norm`)
- Stage 1 forensic vocabulary (`per-fact pre-edit prior`, `loss trajectory`, `right-vector optimization`)
- v1.3 ratification axis vocabulary (`architectural axis`, `structural axis`, `textual axis`, `EMPIRICALLY-RATIFIED`, `FULLY-RATIFIED`, `DEFECTIVE-IN-FIELD`)

Vocabulary explicitly retired:
- "v1.3 Cell 9 PASS gate" → replaced with axis-decomposed posture
- "Stage 1 PASS gate empirical" → replaced with split-verdict language

---

## 11. Schedule Footprint

| Phase | Wall time |
|---|---|
| Pre-session orientation + 3-gate verification | ~10 min |
| Pod recovery (orphan kernel + GPU pin) + SSH fix | ~30 min |
| NV hygiene (notebook archive + MD/JSON archive + cleanup) | ~25 min |
| Cells 0–4 execution (pre-flight) | ~10 min |
| Cell 5 model load | ~3 min |
| Cells 6–8 execution | ~2 min |
| Cell 9 trial loop (9 trials × ~15–32s + overlay snapshots + probes) | ~5 min |
| Cells 10–12 execution | ~2 min |
| Diagnostics + handoff package authoring | ~30 min |
| **Total session** | **~2 hr** |

S2.8 fits within an extended single-session envelope. Wall-time is dominated by environment recovery (orphan kernel + SSH) rather than Stage 1 execution itself, which completed in ~5 min thanks to MEMIT process-local cache retention across trials.

---

*End of S2.8 summary block.*
