# S2.21 Kickoff — T.1-GRACE-3B Runbook v0.1 Authoring

**Session:** S2.21
**Scope:** T.1-GRACE-3B retry runbook v0.1 authoring (NEW runbook for `meta-llama/Llama-3.2-3B`)
**Predecessor:** S2.20 (T.2 GRACE; ROUTE_A_HALT_ENVIRONMENT_CONDITIONAL)
**Successor:** S2.22 (T.1-GRACE-3B execution)
**Routing source:** D-S220-S221-ROUTING-1
**Authored:** 2026-05-05 (post-S2.20 v0.2 codification analog session)

---

## 1. Session Identification

### 1.1 Scope

S2.21 produces `t1_grace_3b_runbook v0.1` — a NEW declarative runbook for T.1-GRACE-3B retry against `meta-llama/Llama-3.2-3B`. This session authors only; execution occurs at S2.22 per parallel-sibling discipline.

### 1.2 Hypothesis Class

T.1 alternate-model under GRACE engine. Disambiguates the v1.2 environmental-ceiling envelope (S2.20) before invoking v1.0 architectural-invariant elimination paths. Distinct from T.1-alt-model-under-MEMIT (canonical `t_branch §5'-α` path), which is BYPASSED pending v1.2 ceiling resolution.

---

## 2. Inheritance Graph

```
Inheritance lineage at S2.21 entry:
═══════════════════════════════════════════════════════════════════
                t2_grace_runbook v0.2  (DIRECT structural template)
                          │
                          │ structural inheritance
                          ▼
                t1_grace_3b_runbook v0.1  ◄── (S2.21 target)
═══════════════════════════════════════════════════════════════════
```

### 2.1 Direct-Inheritance Surfaces

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition | t2_grace_runbook v0.2 §2–§5 | verbatim |
| Patch application discipline | grace-patches-canonical v0.2 §4 | verbatim |
| F-2 dispatch preamble | grace-patches-canonical v0.2 §10 | verbatim |
| Constraint registry | grace-patches-canonical v0.2 §3 | verbatim |
| Verdict surface taxonomy | t2_grace_runbook v0.2 §7 | verbatim |
| Forward routing matrix | t2_grace_runbook v0.2 §8 | extended |

### 2.2 Cell Delta Map

| Cell | Delta Class |
|---|---|
| 0–4 | structural inheritance verbatim |
| 5 | REWRITTEN — fresh baseline capture (no cross-session anchor) |
| 6 | RE-VERIFIED — Llama-3.2 tokenizer behavior |
| 7 | structural inheritance; fresh values |
| 8 | RE-VERIFIED — down_proj shape `Linear(8192, 3072)` |
| 9 / 10 / 11 / 11+ / 11++ / 12 | structural inheritance verbatim |
| 13 | EXTENDED — T.1-GRACE outcome routing matrix |
| 14–17 | DECLARATIVE inheritance (Block C untested precedent) |
| 18 | INAPPLICABLE per §6.3 |
| 19–20 | structural inheritance |

---

## 3. Model Swap — Llama-3.1-8B → Llama-3.2-3B

### 3.1 Architecture Comparison

| Property | Llama-3.1-8B (S2.20) | Llama-3.2-3B (S2.22 target) |
|---|---|---|
| Hidden size | 4096 | 3072 |
| Intermediate size | 14336 | 8192 |
| Number of decoder layers | 32 | 28 |
| Total parameters | 8.03B | 3.21B |
| down_proj shape | Linear(14336, 4096) | Linear(8192, 3072) |
| fp16 weight footprint | 16.06 GiB | 6.42 GiB |
| Tokenizer family | Llama-3 | Llama-3 (continuity verification at Cell 6) |

### 3.2 Edit Site Validation

| Site | 3B validity | Relative depth |
|---|---|---|
| L17 | VALID (`0 ≤ 17 < 28`) | 60.7% (vs 53.1% on 8B; +7.6%) |
| L2 | VALID | shallow |

### 3.3 VRAM Projection (RTX 4090 24 GiB)

```
═══════════════════════════════════════════════════════════════════
  Component                              VRAM cost
  ─────────────────────────────────────────────────
  Model weights (fp16, 3.21B)            6.42 GiB
  Activations L0–L16 (no grad ds)        0.00 GiB
  Activations L17–L27 (11 layers, ds)    ~2.50 GiB
  Adapter value + Adam state             0.05 GiB
  Workspace + cuBLAS                     0.50 GiB
  ─────────────────────────────────────────────────
  Total under F-2:                       ~9.47 GiB
  RTX 4090 ceiling:                      24.00 GiB
  HEADROOM:                              14.53 GiB  ← fits
═══════════════════════════════════════════════════════════════════
```

---

## 4. Patch Inheritance

| Patch | Llama-3.2-3B Applicability | Defect Class |
|---|---|---|
| P-1-GRACE | APPLICABLE | Universal HF transformer with numeric submodule indices |
| P-2-GRACE | APPLICABLE | Universal fp16-loaded model + non-empty GRACE codebook |
| Pad-Token | APPLICABLE | Llama-class tokenizer |
| F-2 | APPLICABLE | runtime model state |
| Inapplicable: P-3' / P-4..P-7 / P-7-ROME..P-9-ROME / Copy-Unmount | per grace-patches v0.2 §1.3 |

---

## 5. Cross-Session Bit-Exact Discipline

### 5.1 Baseline Reset

`pre_edit_baseline_s220` (Llama-3.1-8B) NOT carry-forward. Llama-3.2-3B is a different model class.

### 5.2 Fresh Baseline Capture Protocol (S2.22 Cell 5)

| Sub-block | Function |
|---|---|
| 5.1 | Defensive preamble + HF token load (C-S220-2) |
| 5.2 | Model load (`meta-llama/Llama-3.2-3B`; revision-pinned) |
| 5.3 | Layer-set verification (n_layer = 28; L17 + L2 valid) |
| 5.4 | Pad-Token alias (C-GRACE-4) |
| 5.5 | Fresh baseline capture (full per-probe P-value capture) |
| 5.6 | Persist to `/workspace/architecture_profile/llama_3_2_3b_baselines.json` |

### 5.3 Cross-Session Anchor Lineage

```
═══════════════════════════════════════════════════════════════════
  Llama-3.1-8B chain (preserved for any future return):
    Checkpoint #1–#7 (S2.13-C through S2.20)
    
  Llama-3.2-3B chain (FRESH at S2.22):
    Checkpoint #1 (fresh baseline; S2.22 Cell 5)
═══════════════════════════════════════════════════════════════════
```

---

## 6. Cell Body Authoring Specification

### 6.1 Substring Substitutions (Verbatim Cells)

| Substitution | Pattern |
|---|---|
| Model name | `meta-llama/Llama-3.1-8B` → `meta-llama/Llama-3.2-3B` |
| Revision SHA | `d04e592b...` → `<TBD; resolved at S2.22 Cell 5 entry>` |
| Baseline path | `*_baselines.json` keyed on model name |
| Output paths | `t2_grace_*` → `t1_grace_3b_*` |
| Layer paths | UNCHANGED (`model.layers.17.mlp.down_proj`) |

### 6.2 Cells Requiring Substantive Re-Authoring

| Cell | Re-authoring Scope |
|---|---|
| 5.5 | Fresh baseline capture per §5.2 |
| 6 | Re-verify Llama-3.2 tokenizer behavior on cfb-v3 facts |
| 8 | down_proj shape assertion `Linear(8192, 3072)` |
| 13 | Routing matrix extension per §7 |
| 18 | Disposition INAPPLICABLE per §6.3 |

### 6.3 Cell 18 — INAPPLICABLE Disposition

Llama-3.2-3B does not have pre-existing covariance caches at NV. GRACE adapter mechanism does not consume covariance caches. Cell 18 cell body becomes a comment-only no-op with rationale comment per D-S219-CELL3-1 precedent.

### 6.4 Cell 4 Hyperparameter Inheritance

| Hparam | Value |
|---|---|
| `GRACE_LAYER_A_PARAM` | `model.layers.17.mlp.down_proj.weight` |
| `GRACE_LAYER_B_PARAM` | `model.layers.2.mlp.down_proj.weight` |
| `GRACE_INIT_EPSILON` | `1.0` |
| `GRACE_EDIT_LR` | `1.0` |
| `GRACE_DEVICE` | `"cuda"` |
| `GRACE_GENERATION` | `False` |

---

## 7. Forward Routing Matrix — S2.22 Cell 13

```
S2.22 Cell 13 outcome → S2.23 routing:
═══════════════════════════════════════════════════════════════════
  PASS:
    └── v1.2 disposition: environmental ceiling CONFIRMED
        v1.3 amendment: ceiling at hardware × model-size axis
        S2.23: continued GRACE work on smaller models
  
  FAIL with installation (narrow-discriminator):
    └── v1.2 disposition: mechanism-class elimination (stronger than v1.0)
        v1.3 amendment: merges adapter elim with v1.0
        S2.23: T.1 alt-model under MEMIT (resumes t_branch §5'-α)
  
  FAIL at environment (3B also OOMs):
    └── v1.2 disposition: environmental ceiling at model-size invariance
        v1.3 amendment: documents model-size invariance
        S2.23: hardware migration deliberation OR T-branch halt
═══════════════════════════════════════════════════════════════════
```

---

## 8. Pre-S2.21 OQ Resolution Slate

### 8.1 OQ-S220-MANIFEST-1

Reproducibility manifest tracks 2 sessions despite 8+ session history. Resolution: S2.21 runbook documents Cell 0+ investigation pattern; no resolution at authoring.

### 8.2 OQ-S220-CFB-PATH-1

Corpus path migration deferred per operator-side decision. Runbook v0.1 inherits S2.20 path verbatim.

### 8.3 NEW OQs Anticipated at S2.22

| ID | Statement |
|---|---|
| OQ-S221-1 | Llama-3.2 tokenizer leading-space convention parity |
| OQ-S221-2 | down_proj shape impact on adapter value parameter shape (`value_shape = 3072`) |
| OQ-S221-3 | `hf_cache` reusability across model classes |

---

## 9. Deliverables — S2.21 Close

### 9.1 Authoring Targets

| ID | Artifact | Length Target |
|---|---|---|
| 1 | `t1_grace_3b_runbook v0.1` | ~1500 lines |
| 2 | `session_2_21_summary_block.md` | ~250 lines |

### 9.2 Decisions Anticipated

| ID | Statement |
|---|---|
| D-S221-Q1-1 | Runbook structural inheritance verbatim with §6.1 substitutions |
| D-S221-Q2-1 | Cell 18 INAPPLICABLE per §6.3 |
| D-S221-Q3-1 | Layer corridor preservation (L17 + L2) |
| D-S221-Q4-1 | Fresh baseline capture per §5.2 |
| D-S221-Q5-1 | F-2 dispatch preamble inherited verbatim |
| D-S221-CHECKPOINT-1-1 | Checkpoint #1 establishment at S2.22 Cell 5 (PROVISIONAL) |
| D-S221-VRAM-PROJECTION-1 | ~9.47 GiB allocation projection (PROVISIONAL) |

### 9.3 Constraints Anticipated

| ID | Statement |
|---|---|
| C-S221-1 | Llama-3.2-3B revision SHA pinning at S2.22 Cell 5 |
| C-S221-2 | Tokenizer continuity verification gate at S2.22 Cell 6 |

---

## 10. KB Hygiene — Pre-S2.21

### 10.1 Required Uploads

| Document | Rationale |
|---|---|
| `grace-patches-canonical v0.2` | LOAD-BEARING for §4 patch inheritance |
| `t2_grace_runbook v0.2` | LOAD-BEARING for §2.1 structural template |
| `framework_finding_memit_ceiling_archival v1.2` | LOAD-BEARING for §1.2 routing rationale |
| `session_2_20_summary_block.md` | predecessor session reference |
| `t_branch_decision_document v1.1` | routing rationale at §1.2 |
| `cfb-v3.yaml v1.0` | reference (no execution at S2.21) |
| `probe-set-v3.yaml v1.0` | reference (no execution at S2.21) |

### 10.2 Required Removals

| Document | Rationale |
|---|---|
| `t2_grace_runbook v0.1` | superseded |
| `grace-patches-canonical v0.1` | superseded |
| `t2_rome_runbook v0.2` | sibling reference; not consumed |
| `rome-patches-canonical v0.2` | sibling reference; INAPPLICABLE |
| `stage_1_sect_runbook v1.7` | MEMIT-side; INAPPLICABLE |
| `memit-patches-canonical v2.5` | MEMIT-side; INAPPLICABLE |
| `session_2_18_summary_block.md` / `session_2_19_summary_block.md` | predecessor-of-predecessor |
| `framework_finding v1.0 / v1.1` | merged into v1.2 carry-forward |

---

## 11. Session Arc

```
═══════════════════════════════════════════════════════════════════
  Phase 1: Inheritance verification
     └── Confirm t2_grace v0.2 + grace-patches v0.2 + framework v1.2 in KB
  
  Phase 2: Runbook v0.1 declarative authoring
     ├── Cells 0–4: structural inheritance verbatim
     ├── Cell 5: rewrite per §5.2
     ├── Cell 6: re-verify per §3
     ├── Cells 7–13: structural inheritance with substitutions
     ├── Cells 14–17: declarative inheritance
     └── Cells 18–20: Cell 18 INAPPLICABLE per §6.3
  
  Phase 3: Decision + constraint ratification per §9.2 + §9.3
  
  Phase 4: S2.21 close summary authoring per §9.1
═══════════════════════════════════════════════════════════════════
```

---

## 12. Forward Action

| Step | Action | Owner |
|---|---|---|
| 12.1 | Operator confirms KB hygiene per §10 | operator |
| 12.2 | Operator initiates S2.21 with this kickoff | operator |
| 12.3 | Agent authors `t1_grace_3b_runbook v0.1` per §6 + §9.1 | agent |
| 12.4 | Agent authors `session_2_21_summary_block.md` per §9.1 | agent |
| 12.5 | Operator endorses S2.21 close artifacts | operator |
| 12.6 | S2.22 = T.1-GRACE-3B execution session | operator + agent |

---

**Kickoff status:** READY FOR OPERATOR INITIATION
**Persistence:** `/mnt/user-data/outputs/session_2_21_kickoff.md`
