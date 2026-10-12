# S2.23 Kickoff — T.1 Alt-Model under MEMIT Runbook v0.1 Authoring

**Session:** S2.23
**Scope:** T.1-α-MEMIT runbook v0.1 authoring (NEW runbook for `meta-llama/Llama-3.2-3B` under MEMIT engine; resumes t_branch §5'-α canonical path)
**Predecessor:** S2.22 (T.1-GRACE-3B; ROUTE_A_HALT_MECHANISM_3B; NARROW_BY_DESIGN)
**Successor:** S2.24 (T.1-α-MEMIT execution)
**Routing source:** D-S222-S223-ROUTING-1
**Authored:** 2026-05-05 (post-S2.22 close)

---

## 1. Session Identification

### 1.1 Scope

S2.23 produces `t1_alt_model_3b_memit_runbook v0.1` — a NEW declarative runbook for T.1-α (alt-model under MEMIT) against `meta-llama/Llama-3.2-3B`. This session authors only; execution occurs at S2.24 per parallel-sibling discipline.

The `α` suffix marks **smaller-Llama scale-axis** investigation. T.1-β (alt-architecture; Mistral / Qwen / others) is reserved as conditional successor pending S2.24 verdict.

### 1.2 Hypothesis Class

T.1-α-MEMIT addresses: **does the v1.0 + v1.1 architectural-invariant ceiling generalize across Llama-class scale, or is it Llama-3.1-8B-specific at this scale?**

The v1.0 ceiling is empirically validated on seven independent axes for `Llama-3.1-8B × {MEMIT, ROME} × canonical hparams`:
1. Hyperparameter sweep (S2.10) — bounded at 0.022
2. Corpus revision (S2.12-A) — bounded at 1.4–3.8e-5
3. Target shift (S2.13-C) — bounded
4. v_lr fine (S2.14-D D.3) — bounded at 7e-7–5e-5
5. Mediation locus (S2.14-D D.1) — L_M=L2 outside canonical band [4..8]
6. Layer-set search L2-L6 (S2.15-D2) — bounded at 1.5–2.5e-5
7. ROME canonical hparams (S2.18) — L17 + L2 compute_v 1.06e-2/1.06e-6

Every axis varies a hyperparameter / corpus / target / locus / write-engine but **holds the model fixed at Llama-3.1-8B**. T.1-α tests whether the ceiling is structurally model-specific.

### 1.3 Verdict-Conditional Routing (S2.25)

| S2.24 verdict | S2.25 scope | Framework finding implication |
|---|---|---|
| PASS (calibration corridor met) | v1.3 amendment: ceiling localized to Llama-3.1-8B (specific scale × specific tokenizer-config); WS3 implementation guidance permits MEMIT on smaller Llama | Architectural-invariant claim narrows |
| FAIL with installation (ceiling reproduces at 3B) | T.1-β alt-architecture authoring (Mistral-7B or Qwen-7B) | Ceiling generalizes across Llama-class scale; tests cross-architecture |
| FAIL at environment | Hardware migration deliberation (covariance cache compute requirement) | Orthogonal blocker |

---

## 2. Inheritance Graph

```
Inheritance lineage at S2.23 entry:
═══════════════════════════════════════════════════════════════════
                stage_1_sect_runbook v1.7  (DIRECT structural template)
                          │
                          │ structural inheritance (model swap)
                          ▼
                t1_alt_model_3b_memit_runbook v0.1  ◄── (S2.23 target)
═══════════════════════════════════════════════════════════════════

Sibling references (NOT load-bearing for S2.23 authoring):
  - t1_grace_3b_runbook v0.1 (T.2 GRACE-side; same model swap pattern, different engine)
  - t2_rome_runbook v0.2 (T.2 ROME-side; eliminated S2.18; preserved as forensic record)
```

### 2.1 Direct-Inheritance Surfaces

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition | stage_1_sect_runbook v1.7 §2–§5 | verbatim |
| Patch application discipline | memit-patches-canonical v2.5 §6–§7 | verbatim |
| Constraint registry | memit-patches-canonical v2.5 §3 + §10 | verbatim |
| Hyperparameter envelope | stage_1_sect_runbook v1.7 §2.8 | verbatim |
| Verdict surface taxonomy | stage_1_sect_runbook v1.7 §7 | verbatim |
| Forward routing matrix | stage_1_sect_runbook v1.7 §8 | extended (T.1 verdict-conditional routing) |

### 2.2 Cell Delta Map

| Cell | Delta Class | Notes |
|---|---|---|
| 0 | structural inheritance verbatim | OS preamble; no MEMIT-specific deps differ from prior runbooks |
| 1 | structural inheritance verbatim with engine substitution | Clone target = MEMIT engine repo (per memit-patches-canonical v2.5 anchor SHA) |
| 1.5+ | RE-VERIFIED — MEMIT module introspection | Same structural cell as GRACE/ROME but introspects `memit/` package |
| 2 / 2++ / etc. | structural inheritance with engine path substitutions | MEMIT patch sites per memit-patches v2.5 |
| 3 | APPLICABLE under MEMIT (no longer no-op) | MEMIT consumes layer_stats covariance caches; Cell 3 is the cov-cache integrity gate |
| 4 | structural inheritance verbatim | MEMIT canonical hparams (mom2_update_weight, v_lr, v_num_grad_steps); Llama-3.2-3B layer paths unchanged |
| 5 | REUSABLE — Llama-3.2-3B Checkpoint #1 already exists at NV | First T.1-α-MEMIT execution can READ existing baseline rather than re-capture; cross-session bit-exact gate (C-S220-3) APPLICABLE on second run |
| 6 | structural inheritance | Allowlist `{"cfb-v3-004"}` parity confirmed at S2.22 |
| 7 | structural inheritance | Pre-edit baseline against current model state |
| 8 | REWRITTEN — covariance cache computation from scratch | `/workspace/covariance_caches/` keyed on Llama-3.1-8B; NO entries for Llama-3.2-3B; first-execution cells must compute mom2 from Wikipedia stats |
| 9 / 10 / 11 / 12 / 13 | structural inheritance verbatim | MEMIT edit dispatch + verdict surface + routing |
| 14–17 | DECLARATIVE inheritance | Block C 15-trial loop (verdict-conditional) |
| 18 | APPLICABLE | Cov cache integrity gate verifies fresh computation |
| 19–20 | structural inheritance | NV inventory + manifest extension |

---

## 3. Model Swap — Llama-3.1-8B → Llama-3.2-3B (under MEMIT)

### 3.1 Architecture Comparison (Reused from S2.21 §3.1)

| Property | Llama-3.1-8B | Llama-3.2-3B |
|---|---|---|
| Hidden size | 4096 | 3072 |
| Intermediate size | 14336 | 8192 |
| Number of decoder layers | 32 | 28 |
| Total parameters | 8.03B | 3.21B |
| down_proj shape | Linear(14336, 4096) | Linear(8192, 3072) |
| fp16 weight footprint | 16.06 GiB | 6.42 GiB |
| Tokenizer family | Llama-3 | Llama-3 (parity confirmed S2.22 Cell 6) |

### 3.2 MEMIT Edit Site Mapping

MEMIT canonical L2-L6 layer set per S2.15-D2 D-S215D2-1; cov-cache provenance LOCKED at [2..6] per D-S215D2-BLOCKB-PROVENANCE-1. Layer indices VALID on Llama-3.2-3B (`0 ≤ idx < 28`).

| Layer | 3B validity | Relative depth (3B vs 8B) | Memo |
|---|---|---|---|
| L2 | VALID | 7.1% vs 6.3% | shallow band entry |
| L3 | VALID | 10.7% vs 9.4% | |
| L4 | VALID | 14.3% vs 12.5% | canonical mediation peak (S2.14-D D.1) |
| L5 | VALID | 17.9% vs 15.6% | |
| L6 | VALID | 21.4% vs 18.8% | shallow band exit |

5-layer band shifts marginally deeper in relative depth on 3B (+1–3%) — minor architectural-shape difference; not expected to impact MEMIT applicability.

### 3.3 VRAM Projection (RTX 4090 24 GiB) — MEMIT-Specific

```
═══════════════════════════════════════════════════════════════════
  Component                                       VRAM cost
  ─────────────────────────────────────────────────────────
  Model weights (fp16, 3.21B)                     6.42 GiB
  Activations + gradient accumulation (5-layer)   ~3-4  GiB
  mom2 inverse + workspace                        ~1-2  GiB
  cuBLAS + workspace                              0.50  GiB
  ─────────────────────────────────────────────────────────
  Total under MEMIT canonical hparams:            ~11–13 GiB
  RTX 4090 ceiling:                               24.00 GiB
  HEADROOM:                                       11–13 GiB  ← fits comfortably
═══════════════════════════════════════════════════════════════════
```

**Provenance:** S2.15-D2 D.2 on Llama-3.1-8B at L2-L6 ran at ~14 GiB peak; 3B at same layer set should run ~6 GiB lower (linear-ish scaling with hidden_size² × intermediate_size).

### 3.4 Covariance Cache Compute Cost (NEW LOAD-BEARING for S2.24)

MEMIT's mom2 computation requires per-layer covariance over a corpus (canonical: Wikipedia text statistics with `npos>8192`). Llama-3.1-8B caches at NV (`/workspace/covariance_caches/.../wikipedia_stats/`; ~6.5 GiB across L2-L8 + L17 from S2.18 extension). NO caches for Llama-3.2-3B.

| Cost dimension | Estimate |
|---|---|
| Per-layer cov computation (full corpus) | ~30–60 min (5-layer band L2-L6) |
| Layer set L2-L6 total | ~2.5–5 hours |
| NV storage requirement per cache | ~0.8 GiB per layer (3B intermediate_size × float32 mom2) |
| Total NV addition | ~4 GiB for L2-L6 |

**Operator-side decision pre-S2.24:** confirm whether to compute fresh L2-L6 covariance for Llama-3.2-3B at session entry (additional ~3 hour wall-time) OR reduce scope to single-layer (e.g., L4 mediation peak only; ~30–60 min).

D-S223-COV-SCOPE-1 (PROVISIONAL): full L2-L6 computation matches S2.15-D2 protocol; reduced single-layer would test only L4 PASS/FAIL and lose layer-set discrimination at v1.3 amendment authoring.

---

## 4. Patch Inheritance

| Patch | Llama-3.2-3B Applicability | Defect Class |
|---|---|---|
| P-1 (.upstream_pristine + parent_module substitution) | APPLICABLE | Universal HF transformer with numeric submodule indices |
| P-2 (fp16 cdist; for cov computation backward) | APPLICABLE | Universal fp16-loaded model |
| P-3' + Device-Map | CONDITIONAL — single-GPU dispatch on RTX 4090 sufficient; no multi-GPU sharding | per memit-patches v2.5 §10 |
| P-4 / P-5 / P-6 | APPLICABLE — MEMIT mediation logic patches | per memit-patches v2.5 §1 |
| P-7 (EMPIRICALLY-VALIDATED at S2.8 on 8B) | APPLICABLE — extends to Llama-class | per memit-patches v2.5 §1 |
| Pad-Token | APPLICABLE | Llama-class tokenizer (RATIFIED at S2.22 Cell 5.4 on 3B) |
| Copy-Unmount | APPLICABLE | Bit-exact joint-overlay validated 6× cross-session × 4 layer-ranges (memory KB) |

**Patches NOT applicable** (S2.22 / GRACE-side): P-1-GRACE / P-2-GRACE / F-2 (CONFIGURATION_LAYER) / GRACE adapter unmount mechanism.

### 4.1 Process Constraints (Carry-Forward)

C-S25-15 / C-S26-1/2/3 / C-S28-1 carry forward verbatim from memit-patches v2.5. R1.1/2/3 cell-level gates apply (R1.3 = canonical dry-run gate at Cell 8 equivalent; here Cell 8 is REWRITTEN for fresh cov computation, R1.3 absorbs into post-compute verification gate).

---

## 5. Cross-Session Bit-Exact Discipline — REUSABLE BASELINE

### 5.1 S2.22 Baseline Carry-Forward

`llama_3_2_3b_baselines.json` (Llama-3.2-3B chain Checkpoint #1; 37.8 KB; persisted at S2.22 Cell 5.6) is REUSABLE for S2.24 Cell 5 entry. T.1-α-MEMIT inherits the same per-fact target IDs + per-probe P-values captured at S2.22.

**Implication for Cell 5:** Cell 5 INVERTS from baseline-producer (S2.22 first execution) to **gate-consumer** (S2.24 second execution within Llama-3.2-3B chain). C-S220-3 combined gate (top-1 strict equality + drift `< 1e-5`) APPLICABLE — establishes Llama-3.2-3B chain Checkpoint #2.

### 5.2 Anchor Lineage at S2.24 Entry

```
═══════════════════════════════════════════════════════════════════
  Llama-3.1-8B chain (preserved on NV; not consumed at S2.24):
    Checkpoint #1–#7 (S2.13-C through S2.20)
  
  Llama-3.2-3B chain:
    Checkpoint #1 (S2.22 Cell 5; established under GRACE engine)
    Checkpoint #2 (S2.24 Cell 5; established under MEMIT engine; FIRST C-S220-3 gate)
═══════════════════════════════════════════════════════════════════
```

**Cross-engine consideration:** the baseline JSON is engine-agnostic — captures model state at the model_revision_sha, independent of editor engine. C-S220-3 gate compares model state at consumer time vs producer time; engine swap (GRACE → MEMIT) does not invalidate the gate as long as the model load produces bit-identical activations.

### 5.3 Tokenizer + Allowlist Carry-Forward

| Anchor | Status | S2.24 disposition |
|---|---|---|
| pad_token_id = 128001 | CONFIRMED at S2.22 | inherited verbatim |
| MULTI_TOKEN_ALLOWLIST = `{"cfb-v3-004"}` | CONFIRMED at S2.22 | inherited verbatim |
| Per-fact `target_new_id` mapping | RECORDED in baseline | inherited verbatim |
| Per-fact `target_true_id` (natural top-1) | RECORDED in baseline | available for diagnostic; NOT load-bearing for MEMIT verdict |

---

## 6. Cell Body Authoring Specification

### 6.1 Substring Substitutions (Verbatim Cells)

| Substitution | Pattern |
|---|---|
| Model name | `meta-llama/Llama-3.1-8B` → `meta-llama/Llama-3.2-3B` |
| Revision SHA | inherits S2.22 Cell 5.2 pinned SHA |
| Baseline path | `*_baselines.json` keyed on `llama_3_2_3b` |
| Output paths | `stage_1_sect_*` → `t1_alt_model_3b_memit_*` |
| Cov cache path | `/workspace/covariance_caches/llama_3_1_8b/...` → `/workspace/covariance_caches/llama_3_2_3b/...` |
| Layer paths | UNCHANGED (`model.layers.{2..6}.mlp.down_proj`) |

### 6.2 Cells Requiring Substantive Re-Authoring

| Cell | Re-authoring Scope |
|---|---|
| Cell 1 | engine clone target = MEMIT canonical engine SHA (per memit-patches v2.5); plus snapshot-to-NV per OQ-S222-CELL1-2 (LOAD-BEARING absorption) |
| Cell 1.5+ | MEMIT module introspection (different module surface than GRACE/ROME) |
| Cell 5 | INVERTS — baseline gate-consumer (consume `llama_3_2_3b_baselines.json` from S2.22); FIRST C-S220-3 gate within Llama-3.2-3B chain |
| Cell 8 | REWRITTEN — fresh cov cache computation per §3.4 (S2.15-D2 protocol; ~3 hour wall-time anticipated) |
| Cell 13 | EXTENDED — T.1-α-MEMIT routing matrix per §1.3 |
| Cell 18 | APPLICABLE — verifies fresh cov caches integrity post-Cell-8 computation |

### 6.3 Cell 4 Hyperparameter Inheritance

| Hparam | Value | Provenance |
|---|---|---|
| MEMIT layer set | `[2, 3, 4, 5, 6]` | D-S215D2-1 (PRIMARY band on 8B; carries forward unchanged for T.1-α) |
| `mom2_update_weight` | 15000 | S2.10 PASS configuration |
| `v_lr` | 0.5 | S2.10 PASS configuration |
| `v_num_grad_steps` | 25 | S2.10 PASS configuration |
| `kl_factor` | 0.0625 | canonical |
| Edit dispatch | joint-overlay 5-fact (per S2.14-D D.3 protocol) | carries forward |

### 6.4 v0.2 Codification State at S2.23 Authoring Time

GRACE-side v0.2 codification (recommended pre-S2.23 per S2.22 close §9.1.2) is NOT load-bearing for S2.23 authoring — S2.23 produces a MEMIT-side runbook. GRACE-side artifacts (grace-patches v0.3, t2_grace v0.3, t1_grace_3b v0.2, framework_finding v1.3) can be authored in parallel or post-S2.23 without blocking T.1-α-MEMIT runbook authoring.

**Load-bearing for S2.23 entry:** stage_1_sect_runbook v1.7, memit-patches-canonical v2.5, framework_finding v1.2 (or v1.3 if codified).

---

## 7. Forward Routing Matrix — S2.24 Cell 13

```
S2.24 Cell 13 outcome → S2.25 routing:
═══════════════════════════════════════════════════════════════════
  PASS (calibration corridor met at L2-L6 joint-overlay):
    └── v1.3 amendment scope: ceiling NARROWS to Llama-3.1-8B-specific
        at this scale; framework_finding amends "architectural-
        invariant" claim to "architectural-invariant on Llama-3.1-8B
        at canonical hparams; non-invariant across scale within
        Llama family"
        WS3 implementation guidance: MEMIT viable on Llama-class
        smaller models for fact-knowledge editing
    └── S2.25 = T.1-α-PASS post-routing (open scope)
  
  FAIL with installation (ceiling reproduces; layer-set FAIL with
  same pathology classes as 8B):
    └── v1.3 amendment scope: ceiling generalizes across Llama-class
        scale; tightens v1.0 + v1.1 architectural-invariant claim
    └── S2.25 = T.1-β authoring (alt-architecture: Mistral-7B or
        Qwen-7B); cross-architecture disambiguation
  
  FAIL at environment (cov cache compute OR edit dispatch OOM):
    └── unexpected — projected ~13 GiB peak vs 24 GiB ceiling;
        if observed, hardware migration deliberation OR full-
        precision MEMIT scope reduction
    └── S2.25 = halt for triage
═══════════════════════════════════════════════════════════════════
```

---

## 8. Pre-S2.23 OQ Resolution Slate

### 8.1 NEW OQs Anticipated at S2.24

| ID | Statement |
|---|---|
| OQ-S224-1 | Llama-3.2-3B layer_stats Wikipedia covariance computation: per-layer wall-time on RTX 4090 fp16 (anticipates ~30–60 min/layer; informational anchor for v0.2 codification) |
| OQ-S224-2 | mom2_update_weight=15000 calibration on Llama-3.2-3B: same value as 8B PASS, OR requires re-tuning at smaller scale? PROVISIONAL inheritance pending S2.24 verdict |
| OQ-S224-3 | Joint-overlay 5-fact dispatch peak VRAM at canonical hparams on 3B: empirical confirmation of §3.3 projection (~13 GiB) |
| OQ-S224-COV-SCOPE-1 | D-S223-COV-SCOPE-1 (full L2-L6 vs reduced single-layer) closes empirically at session entry per operator decision |

### 8.2 Carry-Forward from S2.22

| ID | Disposition at S2.23 |
|---|---|
| OQ-S222-CELL1-2 | LOAD-BEARING; v0.2 absorption surface; S2.23 runbook v0.1 should anticipate Cell 1 snapshot mechanism (snapshot MEMIT engine source to `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` at first successful clone) |
| OQ-S222-CELL0-DEPS-1 | Cell 0 expansion absorbed at v0.1 declarative form; transformers 5.7.0 + accelerate + hydra-core + pyyaml + sentencepiece preinstalled assumption FALSIFIED at S2.22 — explicit installation cell required |
| OQ-S222-SURFACE-LABELING-1 | Surface annotation per cell (A=terminal / B=notebook) at v0.1 authoring |
| OQ-S222-CELL-EXEC-VERIFICATION-1 | Patch application cells print explicit acceptance string |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | Resolve before Cell 10/12 verdict at S2.24 — runbook §3.2.2 vs YAML §126 generalization predicate semantic gap |

### 8.3 Carry-Forward from S2.20 (still OPEN)

| ID | S2.23 disposition |
|---|---|
| OQ-S220-MANIFEST-1 | DEFERRED |
| OQ-S220-CFB-PATH-1 | DEFERRED — runbook v0.1 inherits S2.22 path verbatim |

---

## 9. Deliverables — S2.23 Close

### 9.1 Authoring Targets

| ID | Artifact | Length Target |
|---|---|---|
| 1 | `t1_alt_model_3b_memit_runbook v0.1` | ~1500 lines |
| 2 | `session_2_23_summary_block.md` | ~250 lines |

### 9.2 Decisions Anticipated

| ID | Statement |
|---|---|
| D-S223-Q1-1 | Runbook structural inheritance verbatim from stage_1_sect_runbook v1.7 with §6.1 substitutions |
| D-S223-Q2-1 | Cell 5 INVERTS to gate-consumer; first C-S220-3 within Llama-3.2-3B chain |
| D-S223-Q3-1 | Layer set L2-L6 preservation per D-S215D2-1; NOT re-tuning at smaller scale (PROVISIONAL pending S2.24) |
| D-S223-Q4-1 | Cell 8 REWRITTEN — fresh cov computation; protocol per S2.15-D2 |
| D-S223-Q5-1 | Engine source snapshot at Cell 1 absorbing OQ-S222-CELL1-2 |
| D-S223-COV-SCOPE-1 | Full L2-L6 cov computation (PROVISIONAL pending operator confirmation pre-S2.24) |
| D-S223-PATCH-INHERITANCE-1 | All MEMIT patches per memit-patches v2.5 §1 inherited; engine source byte-identical to 8B baseline (verified via patch site line-numbers at Cell 1.0) |

### 9.3 Constraints Anticipated

| ID | Statement |
|---|---|
| C-S223-1 | MEMIT engine SHA pinning at S2.24 Cell 1 entry; documented in Cell 20 manifest extension |
| C-S223-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` post-Cell-1; closes OQ-S222-CELL1-2 |
| C-S223-3 | Cov cache fresh computation gate at Cell 8: per-layer file size + checksum verification per S2.15-D2 PROVENANCE protocol |
| C-S223-4 | Layer-set bound assertion at Cell 4: all of [2..6] within `0 ≤ idx < n_layer=28` |
| C-S223-5 | Per-cell explicit Surface annotation (A vs B); inherits IC-S222-2 absorption surface |

---

## 10. KB Hygiene — Pre-S2.23

### 10.1 Required Uploads

| Document | Rationale |
|---|---|
| `stage_1_sect_runbook v1.7` | LOAD-BEARING for §2.1 structural template |
| `memit-patches-canonical v2.5` | LOAD-BEARING for §4 patch inheritance |
| `framework_finding_memit_ceiling_archival v1.2` (or v1.3 if codified) | LOAD-BEARING for §1.2 routing rationale |
| `session_2_22_summary_block.md` | predecessor session reference |
| `t_branch_decision_document v1.1` | routing rationale at §5'-α |
| `cfb-v3.yaml v1.0` | reference (no execution at S2.23) |
| `probe-set-v3.yaml v1.0` | reference (no execution at S2.23) |
| `llama_3_2_3b_baselines.json` (or NV path reference) | informational; Cell 5 gate-consumer source |

### 10.2 Required Removals

| Document | Rationale |
|---|---|
| `t1_grace_3b_runbook v0.1` (and v0.2 if codified) | T.2 GRACE-side; INAPPLICABLE for MEMIT-side authoring |
| `grace-patches-canonical v0.2` (and v0.3 if codified) | GRACE-side; INAPPLICABLE |
| `t2_grace_runbook v0.2` (and v0.3 if codified) | GRACE-side; INAPPLICABLE |
| `t2_rome_runbook v0.2` | ROME-side; INAPPLICABLE for MEMIT authoring (preserved on NV as forensic record) |
| `rome-patches-canonical v0.2` | ROME-side; INAPPLICABLE |
| `session_2_18_summary_block.md` / `session_2_19_summary_block.md` / `session_2_20_summary_block.md` / `session_2_21_summary_block.md` | predecessor-of-predecessor; load-bearing surfaces absorbed into v1.2 + S2.22 close carry-forward |

---

## 11. Session Arc

```
═══════════════════════════════════════════════════════════════════
  Phase 1: Inheritance verification
     └── Confirm stage_1_sect v1.7 + memit-patches v2.5 + framework v1.2 in KB
  
  Phase 2: Runbook v0.1 declarative authoring
     ├── Cells 0–4: structural inheritance with substitutions (§6.1)
     ├── Cell 1: engine snapshot mechanism per OQ-S222-CELL1-2 absorption
     ├── Cell 5: REWRITTEN — gate-consumer pattern (first C-S220-3 within 3B chain)
     ├── Cell 6: structural inheritance with allowlist carry-forward
     ├── Cell 7: structural inheritance
     ├── Cell 8: REWRITTEN — fresh cov computation per S2.15-D2 protocol
     ├── Cells 9–13: structural inheritance with substitutions; Cell 13 EXTENDED routing matrix
     ├── Cells 14–17: declarative inheritance
     └── Cells 18–20: Cell 18 APPLICABLE; Cells 19–20 structural
  
  Phase 3: Decision + constraint ratification per §9.2 + §9.3
  
  Phase 4: S2.23 close summary authoring per §9.1
═══════════════════════════════════════════════════════════════════
```

---

## 12. Forward Action

| Step | Action | Owner |
|---|---|---|
| 12.1 | Operator confirms KB hygiene per §10 | operator |
| 12.2 | Operator initiates S2.23 with this kickoff | operator |
| 12.3 | Operator decision on D-S223-COV-SCOPE-1 (full L2-L6 vs reduced single-layer) before S2.24 entry | operator |
| 12.4 | Agent authors `t1_alt_model_3b_memit_runbook v0.1` per §6 + §9.1 | agent |
| 12.5 | Agent authors `session_2_23_summary_block.md` per §9.1 | agent |
| 12.6 | Operator endorses S2.23 close artifacts | operator |
| 12.7 | S2.24 = T.1-α-MEMIT execution session | operator + agent |

---

## 13. Specialist Routing — S2.23

| Surface | Primary Specialist | Rationale |
|---|---|---|
| Inheritance map authoring | framework-spec-writer | structural template inheritance |
| Block A cell bodies | memit-specialist | engine + patch state + cov cache + dry-run gate |
| Block B cell bodies | memit-specialist + validation-contract-architect | edit dispatch + verdict surface |
| Block C declarative inheritance | memit-specialist | trial loop body |
| Block-end cells | state-consistency-theorist | NV inventory + manifest |
| Routing matrix | framework-spec-writer + memit-specialist | T.1 verdict-conditional routing per §1.3 / §7 |

aiSecOps-specialist + framework-council remain inactive; reactivated at WS2 (orchestration) + WS3 (implementation) work.

---

**Kickoff status:** READY FOR OPERATOR INITIATION

**Persistence:** `/mnt/user-data/outputs/session_2_23_kickoff.md`
