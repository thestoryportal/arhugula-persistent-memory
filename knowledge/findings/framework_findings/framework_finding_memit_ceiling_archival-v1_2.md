# Framework Finding — MEMIT Ceiling Archival — v1.2

**Status:** ADDITIVE AMENDMENT (v1.0 + v1.1 PERMANENT preserved verbatim)
**Supersedes:** none — additive only
**Carry-forward:** S2.21+ sessions inherit v1.0 + v1.1 + v1.2 conjunction
**Predecessor versions:**
- v1.0 (PERMANENT; ratified S2.18 close 2026-05-05) — rank-1-in-weight class ceiling on Llama-3.1-8B
- v1.1 (ADDITIVE; ratified S2.18 close 2026-05-05) — ROME elimination amendment

---

## §0. Amendment Scope

### §0.1 Statement

v1.2 documents the adapter-mechanism environmental ceiling discovered at S2.20 T.2 GRACE execution. The amendment is **ADDITIVE** — v1.0 + v1.1 integrity preserved verbatim. v1.2 extends the ceiling characterization to include resource-class boundaries that are environment-conditional, distinct from the architectural-invariant ceiling documented in v1.0.

### §0.2 Diff vs Prior Versions

| Surface | v1.0 PERMANENT | v1.1 ADDITIVE | v1.2 ADDITIVE (this) |
|---|---|---|---|
| Class | rank-1-in-weight (MEMIT) | rank-1-in-weight (extended to ROME) | adapter-mechanism (GRACE) |
| Ceiling type | architectural-invariant | architectural-invariant | environmental-conditional |
| Eliminability | not eliminable | not eliminable | eliminable via smaller model OR alternate hardware |
| Verdict status | EMPIRICALLY VALIDATED | EMPIRICALLY VALIDATED | EMPIRICALLY VALIDATED at environmental scope; mechanism scope UNTESTED |

### §0.3 Why Additive

The S2.20 verdict is structurally distinct from S2.10 (MEMIT) and S2.18 (ROME) eliminations:

| Dimension | S2.10 / S2.18 elimination | S2.20 outcome |
|---|---|---|
| Mechanism reachability | Edit dispatch executed; mechanism observed | Edit dispatch did not execute under canonical environment |
| Pathology characterization | Pathology classes empirically captured | UNTESTED |
| Verdict claim | architectural-invariant ceiling | environmental ceiling on canonical hardware |
| Routing implication | Mechanism class eliminated structurally | Mechanism class deferred pending environment relaxation |

v1.2 codifies the asymmetry without retracting v1.0/v1.1 claims.

---

## §1. v1.0 + v1.1 Carry-Forward (Statement Preserved Verbatim)

### §1.1 v1.0 Architectural-Invariant Ceiling (PERMANENT)

The architectural-invariant ceiling on `Llama-3.1-8B × MEMIT × canonical hyperparameters` is empirically validated across seven independent axes per S2.18 close anchor (LOAD-BEARING; permanent post-S2.18):

| Axis | Source Session |
|---|---|
| 1. Hyperparameter sweep (mom2_update_weight, v_lr) bounded at 0.022 | S2.10 |
| 2. Corpus revision bounded at 1.4–3.8e-5 | S2.12-A |
| 3. Target shift bounded | S2.13-C |
| 4. v_lr fine bounded at 7e-7–5e-5 | S2.14-D D.3 |
| 5. Mediation locus L_M=L2 outside canonical band [4..8] | S2.14-D D.1 |
| 6. Layer-set search L2-L6 bounded at 1.5–2.5e-5 | S2.15-D2 |
| 7. ROME canonical hparams (L17 + L2 compute_v 1.06e-2/1.06e-6) | S2.18 |

The seven-axis ceiling is structural (model × {MEMIT, ROME} × hparams). NOT eliminable by Class A/B/C/D corpus/hparam/target/layer-set hypothesis testing NOR by write-engine swap (MEMIT → ROME).

### §1.2 v1.1 ROME Elimination Amendment (PERMANENT)

T.2 ROME ELIMINATED at canonical hyperparameters per S2.18 close (B-FAIL Cell 13). Both load-bearing axes — L17 (ROME paper precedent) AND L2 (S2.14-D D.1 mediation peak) — produce verdict-FAIL on cfb-v3-001 guitar consistency:

| Layer | P(target_new) | Verdict |
|---|---|---|
| L17 | 0.0002 (BOS-collapse) | FAIL |
| L2 | 0.0000 (compute_v non-converge) | FAIL |

ROME elimination at L17 (paper-canonical) AND L2 (S2.14-D mediation-peak) constitutes architectural-invariant ceiling extension to ROME write-engine class.

---

## §2. v1.2 Adapter-Mechanism Environmental Ceiling

### §2.1 Statement

T.2 GRACE on `Llama-3.1-8B × fp16 × RTX 4090 24 GiB × edit-site L17 × full-chain backward × canonical hparams (init_epsilon=1.0, edit_lr=1.0, n_iter=200)` is **NOT EXECUTABLE**. The ceiling is RESOURCE-class (VRAM exhaustion at backward pass activation retention), NOT mechanism-class.

### §2.2 Empirical Surface

| Configuration | VRAM at backward pass | Verdict |
|---|---|---|
| F-1 (`requires_grad_(True)` blanket) | >32 GiB demand | OOM at activation buffer construction |
| F-2 (model.train() only; freeze preserved) | 24.64 GiB allocated | OOM by ~0.6 GiB |
| F-3 (F-2 + `gradient_checkpointing_enable()`) | ~17 GiB projected | CheckpointError — adapter stateful forward incompatible with checkpoint recompute invariant |

### §2.3 Mechanism Scope Untested

Per D-S220-VERDICT-CONDITIONAL-1, the following claims remain UNTESTED at S2.20:

| Claim | Status |
|---|---|
| T.2 GRACE adapter mechanism eliminated at canonical engine + model + hparams | UNTESTED |
| T.2 GRACE narrow-discriminator pathology | UNTESTED |
| T.2 GRACE specificity preservation | UNTESTED |
| T.2 GRACE calibration corridor empirical surface | UNTESTED |
| T.2 GRACE multi-fact codebook scaling | UNTESTED |

### §2.4 Eliminability Conditions

The environmental ceiling is **eliminable** along multiple orthogonal axes:

| Elimination axis | Mechanism | Cost |
|---|---|---|
| Smaller model (T.1-GRACE-3B) | Llama-3.2-3B fits backward chain on RTX 4090 (projected 9.47 GiB allocation) | One-session retry; preserves engine + hparams |
| Alternate hardware (A100 80 GiB) | Original Llama-3.1-8B fits with headroom | Operator-side pod migration |
| Bf16 precision | reduced activation memory; some operations natively support bf16 | Breaks D-S220-CHECKPOINT-7-1 cross-session bit-exact lineage |
| Deeper edit layer (L29 etc.) | fewer downstream layers requiring activation retention | Departs from D-S219-Q3-1 layer corridor specification |

The first elimination path (T.1-GRACE-3B retry) is the S2.21 routing per D-S220-S221-ROUTING-1.

---

## §3. Ceiling Class Taxonomy

### §3.1 Class Distinctions

```
Ceiling class taxonomy at v1.2:
═══════════════════════════════════════════════════════════════════
  
  ARCHITECTURAL_INVARIANT (v1.0 + v1.1)
       │
       ├── Property: not eliminable by class-A/B/C/D hypothesis testing
       │             OR by write-engine swap within rank-1-in-weight class
       │
       ├── Validation: 7 axes (S2.10 / S2.12-A / S2.13-C / S2.14-D D.3 /
       │               S2.14-D D.1 / S2.15-D2 / S2.18)
       │
       └── Coverage: MEMIT + ROME on Llama-3.1-8B at canonical hparams
  
  ENVIRONMENTAL_CONDITIONAL (v1.2 NEW)
       │
       ├── Property: eliminable via smaller model OR alternate hardware
       │             OR precision relaxation OR deeper-layer edit
       │
       ├── Validation: 1 axis (S2.20 — RTX 4090 24 GiB ceiling)
       │
       └── Coverage: GRACE on Llama-3.1-8B at canonical environment
═══════════════════════════════════════════════════════════════════
```

### §3.2 Routing Implications by Ceiling Class

| Ceiling Class | t_branch §5' Routing |
|---|---|
| ARCHITECTURAL_INVARIANT (v1.0 / v1.1) | T-branch hypothesis space narrows; route to T.1 alt-model OR T.3 alt-architecture |
| ENVIRONMENT_CONDITIONAL (v1.2) | Defer mechanism verdict; route to environment-relaxation retry (smaller model / alternate hardware) |

---

## §4. Forward Conditional — S2.21 Verdict-Class Resolution

### §4.1 S2.21 Outcome Matrix

The S2.21 = T.1-GRACE-3B retry resolves the v1.2 environmental-ceiling deferral:

| S2.21 verdict | v1.2 disposition |
|---|---|
| **PASS** (installed edit; calibration corridor met) | Environmental ceiling CONFIRMED as the limiting factor; adapter mechanism viable for smaller models; v1.3 amendment documents ceiling boundary at hardware × model-size axis |
| **FAIL with installation** (narrow-discriminator pathology) | Mechanism-class ceiling EXTENDS to model-class-agnostic adapter elimination; v1.3 amendment merges adapter-mechanism elimination with v1.0 architectural-invariant ceiling |
| **FAIL at environment** (3B also OOMs) | Environmental ceiling propagates to smaller model class; investigate hardware migration OR halt T-branch with stronger environmental caveat |

### §4.2 v1.3 Anticipated Scope

S2.21 verdict triggers v1.3 amendment. The v1.3 amendment is conditional on S2.21 outcome and not pre-specified at v1.2 ratification.

---

## §5. Cross-Reference Map

### §5.1 v1.2 Inheritance from S2.20 Decisions

| v1.2 Section | S2.20 Decision Source |
|---|---|
| §2.1 statement | D-S220-CEILING-ENV-1 |
| §2.2 empirical surface | D-S220-FIX-F-1-RETRACTED + D-S220-FIX-F-2 + D-S220-FIX-F-3 |
| §2.3 mechanism scope | D-S220-VERDICT-CONDITIONAL-1 |
| §2.4 eliminability | D-S220-S221-ROUTING-1 |
| §3.1 taxonomy | A-S220-CELL11+++++++-1/2/3 |
| §4.1 outcome matrix | D-S220-S221-ROUTING-1 |

### §5.2 Forward References

| v1.2 Section | Consumer |
|---|---|
| §2.4 eliminability | S2.21 kickoff scope authoring |
| §3.1 taxonomy | t_branch_decision_document v1.2 (if authored) |
| §4.1 outcome matrix | S2.21 close artifact verdict adjudication |

### §5.3 Sibling Cross-References

| v1.2 Anchor | Sibling Document |
|---|---|
| §2 environmental ceiling | `grace-patches-canonical v0.2 §10` (F-2 + retracted F-1/F-3) |
| §2 environmental ceiling | `t2_grace_runbook v0.2 §3.7` (Cell 13 environmental route) |
| §3 ceiling class taxonomy | t_branch_decision_document v1.1 §5' (routing matrix consumer) |

---

## §6. Document Status

**Authored:** 2026-05-05 (v0.2 codification analog session post-S2.20 close)
**Ratified:** §2 environmental ceiling statement + §3 ceiling class taxonomy + §4 outcome matrix
**v1.0 + v1.1 integrity:** PRESERVED VERBATIM (additive amendment discipline)
**Persistence:** `/mnt/user-data/outputs/framework_finding_memit_ceiling_archival-v1_2.md`
**Successor:** v1.3 (conditional on S2.21 verdict)
