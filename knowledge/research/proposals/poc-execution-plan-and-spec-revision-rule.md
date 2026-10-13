# LLM as Database: Agent Harness Architecture
## Workstream 1 Closing Artifact — POC Execution Plan and Spec-Revision Feedback Rule

> **Workstream:** 1 — Empirical POC Scoping (post-v1.2 sealed spec)
> **Session:** 1.7 — Synthesis (closes Sessions 1.1–1.6)
> **Status:** Draft — pending operator review.
> **Basis:** `write-engine-poc-scope.md` + `memit-compat-proto-1.md` + `memit-drift-proto-1.md` + `epsilon-calib-proto-1.md` + `compaction-probe-calib-proto-1.md` + `judge-calib-proto-1.md`.
> **Reference Framework Document:** `llm-as-database-agent-harness-framework.md`. Spec basis: `llm-as-database-v1_2-integrated-spec.md`.
> **Specialist provenance:** Framework Council (all six specialists). Primary voices per section noted inline.
> **Purpose:** Bridge the empirical workstream to v1.2-point-release spec edits and to Workstream 3 implementation planning. Defines (a) execution sequencing, (b) result-to-spec mapping, (c) decision branches per protocol outcome, (d) the amendment ceremony for v1.2.1 edits, (e) the handoff manifest, (f) risk register.

---

## 1. Unified POC Execution Plan

*Primary voices: MEMIT Specialist (Stage 1–3a sequencing), Validation Contract Architect (Stage 3b/3c gating), Orchestration Comparativist (parallelism envelope).*

### 1.1 Stage Dependency Graph

```
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 0 — Operator-owned preconditions (NOT POC scope; gating)          │
│  • Target model commitment (SC-1..SC-9 verified)                         │
│  • Reference Patch Corpus drafted (≥200 patches × class × ≥1 hop)        │
│  • Probe-Set v1 corpus drafted (joint MEMIT + Validation)                │
│  • ≥1 current_larql_version increment authored (RENAME/BUCKET/COMPUTE    │
│    populated per §22.2)                                                   │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 1 — MEMIT-COMPAT-PROTO-1 (gating; OQ-W2)                           │
│  Pre-flight (PF-1..PF-6) → SECT (3 facts × 3 runs)                       │
│  → OP-1/OP-2/OP-3 (D20 verification) → CFB-3 (locality at N=1)           │
│                                                                            │
│  KILL outcome → D12 revisit (POC halts; spec-revision-pass required)     │
│  PASS or D20-DRIFT → Stage 2 admissible                                  │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 2 — MEMIT-DRIFT-PROTO-1 (sequential after Stage 1; OQ-W1)          │
│  SBC sub-protocol (sub-batch ceiling derivation; runs FIRST)             │
│  → Sweep A (primary, L4 + family-balanced)                               │
│  → Sweep B (L3 sensitivity) ┐                                            │
│  → Sweep C (Structural-only) ├ optional; deferral becomes its own OQ     │
│  → Sweep D (Knowledge-only)  ┘                                           │
│                                                                            │
│  Stage 3 protocol authorship may parallelize with Stage 2 EXECUTION       │
│  per write-engine-poc-scope §6 critical-path note.                       │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                  ┌────────────────┴────────────────┐
                  │                                 │
                  ▼                                 ▼
┌─────────────────────────────┐    ┌─────────────────────────────────────┐
│ STAGE 3 prelude — PROBE_SET │    │ STAGE 3b — COMPACTION-PROBE-CALIB-  │
│ _RATIFICATION ceremony      │    │ PROTO-1 (parallel; OQ-OC3)          │
│ (joint MEMIT + Validation   │    │  Oracle construction → sampling     │
│  attestation under          │    │  sweep → floor validation →         │
│  IC-SCOPE-AUTH-1)           │    │  threshold sensitivity →            │
│                             │    │  CompactionProbeReport v1.3          │
│  Ratifies probe-set v1 hash │    └─────────────────────────────────────┘
│  for downstream consumption │
└─────────────────────────────┘
                  │
                  ├──────────────────┬──────────────────┐
                  ▼                  ▼                  ▼
┌───────────────────────────┐ ┌──────────────────┐ ┌───────────────────┐
│ STAGE 3a — EPSILON-CALIB- │ │ (3b runs in      │ │ STAGE 3c — JUDGE- │
│ PROTO-1 (parallel;        │ │  parallel; see   │ │ CALIB-PROTO-1     │
│ OQ-W-CALIB-1)             │ │  above)          │ │ (parallel;        │
│  Cell stratification →    │ │                  │ │ OQ-V-JUDGE-       │
│  ε measurement →          │ │                  │ │ THRESHOLD)        │
│  BUCKET boundary →        │ │                  │ │  Judge selection  │
│  M-threshold derivation   │ │                  │ │  → eighth Tier 2  │
└───────────────────────────┘ └──────────────────┘ │  sealed corpus    │
                                                    │  authored →       │
                                                    │  threshold sweep  │
                                                    │  → granularity    │
                                                    │  decision rule    │
                                                    └───────────────────┘
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 4 — Consolidation (no new protocol authorship)                     │
│  Bundle Deliverables 1–8 into Deliverable 9 (CALIBRATION_RATIFICATION    │
│  packet path) + Deliverable 10 (per-deployment re-calibration playbook). │
│  Submit packets via three parallel ceremony paths:                       │
│   • CALIBRATION_RATIFICATION (existing; §22.5)                           │
│   • CALIBRATION_RATIFICATION_OC3 (new; proposed Session 1.5)              │
│   • CALIBRATION_RATIFICATION_JUDGE (new; proposed Session 1.6)            │
│                                                                            │
│  POC outputs handed off to Workstream 3 implementation planning.         │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Sequencing Rules (Hard Constraints)

- **C-POC-1 — Stage 1 / Stage 2 sequencing.** Stage 2 MUST NOT open execution until Stage 1 returns `PASS` or `D20-DRIFT`. `D20-FAIL` propagates as a Stage 2 KILL pre-condition (carried from MEMIT-COMPAT-PROTO-1 §6).
- **C-POC-2 — Stage 2 → Stage 3 sequencing.** Stage 3 sub-protocols MUST NOT begin execution until `S_ceiling` and drift threshold values from Stage 2 are committed. (Stage 3 protocol *authorship* may parallelize with Stage 2 *execution*; this distinction is preserved from write-engine-poc-scope §6.)
- **C-POC-3 — Stage 3 internal gating.** Stage 3a, 3b, 3c all gate on the `PROBE_SET_RATIFICATION` ceremony completing as Stage 3's prelude. After ratification, all three sub-protocols MAY run in parallel. The probe-set v1 hash referenced post-ratification is immutable for the calibration epoch.
- **C-POC-4 — SBC-before-Sweep ordering inside Stage 2.** The sub-batch ceiling sub-protocol (SBC-1..SBC-4) MUST complete before the main drift sweep opens. Per MEMIT-DRIFT-PROTO-1 §5: running SBC after means main-sweep patches may exceed `S_ceiling` and contaminate the drift signal.
- **C-POC-5 — Reconciliation gate.** Sample points failing the C-WE-1 5% reconciliation tolerance are discarded, not corrected. Calibration data MUST be sourced from reconciled runs only (per MEMIT-DRIFT-PROTO-1 §7).

### 1.3 Wall-Clock Envelope Estimate

These are estimates, not commitments. Real numbers depend on model size, GPU class, parallelization choice. Numbers assume a 7B–13B parameter target on a single mid-tier GPU (A100/H100-class) unless otherwise noted.

| Phase | Single-GPU estimate | Multi-GPU (≥3) estimate | Dominant cost |
|---|---|---|---|
| Stage 0 (operator) | weeks–months | weeks–months | Probe authorship + corpus sizing |
| Stage 1 | 1–2 weeks | 1–2 weeks | SECT + OP + CFB pre/post |
| Stage 2 | 3–6 weeks | 2–4 weeks | 36 measurement points × ≥3 replicates × 4 sweeps (A primary + B/C/D optional) |
| Stage 3 prelude (probe-set v1 mint) | days | days | Ceremony admission + hash anchor |
| Stage 3a (ε) | 2–4 weeks | 2 weeks | 15 cells × 200 patches × 3–5 replicates × pre/post |
| Stage 3b (compaction probe) | 3–6 weeks | 3 weeks | 7,500-edge corpus × N=10 + M=10 × multi-event sweep grid |
| Stage 3c (judge) | 1–2 weeks | 1 week | Per-cell sweep + adversarial corpus |
| Stage 3 total | **7–13 weeks (sequential)** | **3–4 weeks (parallel)** | Limited by 3b on multi-GPU |
| Stage 4 | 1 week | 1 week | Packet assembly + playbook authorship |
| **POC total (Stage 1 → Stage 4)** | **~12–22 weeks** | **~7–11 weeks** | |

The single-GPU vs. multi-GPU difference is concentrated in Stage 3 (~6–8 weeks of compressible time). Operator should be informed of this tradeoff before committing the schedule.

### 1.4 Resource Requirements

**GPU-hours (estimated):**

| Stage | GPU-hours |
|---|---|
| Stage 1 | 50–100 |
| Stage 2 (Sweep A only) | 400–700 |
| Stage 2 (Sweeps A + B + C + D) | 700–1,200 |
| Stage 3a | 200–400 |
| Stage 3b | 300–600 |
| Stage 3c | 50–100 |
| Stage 4 | minimal (CPU-bound) |
| **Total POC** | **~1,000–2,400 GPU-hours** |

**Human probe-authoring hours (estimated, Stage 0 + ongoing):**

| Artifact | Hours |
|---|---|
| Probe-set v1 (~200 templates × 1.5h) | 300 |
| CFB v1 (1,000 facts, 4-class stratified) | 400–500 |
| Reference Patch Corpus (3,000 patches × 15 cells) | 600–800 |
| Compaction calibration corpus (~10,000 candidates → ~7,500 admitted) | 1,500–2,000 |
| Judge calibration corpus (200 cases × ~30 cells) | 500–700 |
| Adversarial sub-corpora (compaction + judge) | 200–300 |
| **Total human-hours** | **~3,500–4,500** |

These corpus authorship hours assume TGA-authored templates per §21.3. Operator may stagger authorship across Stage 0 / Stage 1 / Stage 2 timelines so that long-pole corpora (compaction, reference patch) are not sequentially blocking.

---

## 2. Per-Protocol Deliverable List with Ratification Anchor

*Primary voices: Graph Data Architect (Tier 1 config field placement), MEMIT Specialist (write-engine config), Validation Contract Architect (probe-side artifacts), Warden (ceremony envelope).*

Each protocol's outputs land in a specific spec location. The mapping is the contract between empirical work and spec edit.

### 2.1 MEMIT-COMPAT-PROTO-1 (Stage 1)

| Deliverable | Lands in | Spec edit class (§4) |
|---|---|---|
| `architecture_profile.json` (PF-6) | Identity anchor referenced by every downstream calibration. Not a Tier 1 field; pinned content-hash at deployment. | A — provisional fill (no spec text change) |
| `causal_trace_concentration_report` (PF-2) | POC artifact only; KILL gate evidence. | A |
| `sect_run_log.json`, `sect_verdict` | Architecture Compatibility Verdict (Deliverable 1 of POC scope). | A |
| `op_verification_report.json` | D20-UPHELD/DRIFT/FAIL verdict; informs §8 D20 safeguard documentation. | A or B (B if DRIFT triggers spec-text qualification) |
| `cfb_v1.json`, `cfb_pre_edit_baseline.json`, `cfb_sect_delta_report.json` | Carried forward to Stage 2 as the frozen regression set (Deliverable 4 of POC scope). | A |
| **Aggregate Architecture Compatibility Verdict** | MEMIT-COMPAT-verdict — feeds the precondition to every downstream protocol. | A on PASS; C on KILL |

### 2.2 MEMIT-DRIFT-PROTO-1 (Stage 2)

| Deliverable | Lands in | Spec edit class |
|---|---|---|
| `N_warn` (point + 25/50/75 percentile interval) | Tier 1 config: `drift_warning_threshold`. NOMINAL → WARNING transition value. | A |
| `N_hard` (point + interval) | Tier 1 config: `drift_hard_threshold`. WARNING → HARD transition. | A |
| `N_critical` (proposed) | Tier 1 config: `drift_critical_threshold` (subject to ratification). HARD → CRITICAL transition. | B (new field — not in v1.2) |
| `S_ceiling` | Tier 1 config: `memit_sub_batch_ceiling`. Replaces provisional 2,000. | A |
| Tier stratification flag | Tier 1 config: `drift_per_tier_counter_required` (boolean); IC-WE-1 sub-counter conditional addition. | B (conditional on stratification trigger firing) |
| Family stratification flag | Tier 1 config: `drift_per_family_counter_required` (boolean); IC-WE-1 sub-counter conditional. | B (conditional) |
| `p95_latency_ratio` envelope | Tier 1 config: `drift_p95_latency_ratio_threshold`. Ratifies or replaces provisional 2.0. | A |
| **Drift Curve Dataset** + **Drift Threshold Table** | Deliverables 2 and 3 of POC scope. | A on PASS; C on no-knee |

### 2.3 EPSILON-CALIB-PROTO-1 (Stage 3a)

| Deliverable | Lands in | Spec edit class |
|---|---|---|
| Per-cell ε (15 cells default, up to 75 with tertiary expansion) | `genesis-seal.json`: `larql_epsilon_table` field (specced at §22.4 as PROVISIONAL; ratification clears flag). | A |
| `M_advisory`, `M_operational`, `M_hard` | `genesis-seal.json`: derived M values + Tier 1 config thresholds (§22.4). | A |
| BUCKET boundary tables (per non-default class) | `IC-MANIFEST-1.bucket_map`. Replaces 0.33/0.66 GS7 illustrative defaults for `attention_weight → declared_importance`; per-class boundaries for other BUCKET transforms. | A (illustrative defaults already PROVISIONAL per §22.7) |
| `epsilon_calibration_report` v1 | Deliverable 6 of POC scope; submitted via existing `CALIBRATION_RATIFICATION` ceremony (§22.5). | A |
| `PROBE_SET_RATIFICATION` ceremony type | New ceremony under IC-SCOPE-AUTH-1 envelope. Warden review required (OQ-W-PROBE-MINT carries forward). | B (new ceremony type — additive amendment) |
| `epsilon_history` audit overlay | New Tier 1 config audit log; cross-epoch comparability protection. | B (new audit log) |

### 2.4 COMPACTION-PROBE-CALIB-PROTO-1 (Stage 3b)

| Deliverable | Lands in | Spec edit class |
|---|---|---|
| SUPPORTING / INCIDENTAL sample rate | Tier 1 config: `compaction_probe_sampling_config.supporting_rate`, `.incidental_rate`. Ratifies or replaces provisional 20% / 10%. | A |
| SUPPORTING / INCIDENTAL floor | Tier 1 config: `.supporting_floor`, `.incidental_floor`. **Candidate values 30 / 15 replace provisional 5 / 3** (significant change; flagged as B). | B (provisional values change is an amendment to §11.14) |
| INCIDENTAL threshold | Tier 1 config: `.incidental_threshold`. Candidate value 0.85 replaces provisional 0.80 (FN-cost-weighted tightening). | B |
| `θ_infra` (uniform + non-uniform bias) | Tier 1 config: `compaction_infrastructure_failure_threshold` + `..._threshold_biased`. NEW fields not in v1.2. | B |
| CompactionProbeReport schema v1.3 | IC-OC-PROBE extension (additive). New fields: `infrastructure_failed_count`, `effective_sample_size`, `failure_id_sidecar_ref`, `infrastructure_failure_bias_check`, `report_classification`, calibration-provenance fields. | B (additive amendment to IC-OC-PROBE) |
| `COMPACTION_PROBE_FAILED` Ledger entry type | New Appendix C entry. | B (new entry type) |
| `CALIBRATION_RATIFICATION_OC3` ceremony type | Parallel to §22.5 ceremony path under existing IC-SCOPE-AUTH-1 envelope. | B (new ceremony type) |
| Sealed sidecar file specification | New IC-OC-PROBE-SIDECAR. C-META1 spirit (operator-signed, append-only, hash-anchored). | B (new IC + new file spec) |

### 2.5 JUDGE-CALIB-PROTO-1 (Stage 3c)

| Deliverable | Lands in | Spec edit class |
|---|---|---|
| `judge_calibration_v1` frozen triple `(judge_model_id, judge_prompt, threshold-by-sub-type)` | §21.4 frozen-at-commit value; per-deployment Tier 2 sealed corpus; not Tier 1 (calibration is per-deployment). | A (closes OQ-V-JUDGE-THRESHOLD; values are empirical per §22.8 non-portable rule) |
| Eighth Tier 2 sealed corpus: `judge-calibration-corpus/` | §13.3 sealed corpora inventory addition; Appendix E amendment. | B (additive corpus) |
| `JUDGE_CALIBRATION_RATIFIED`, `JUDGE_THRESHOLD_DRIFT_DETECTED`, `JUDGE_MODEL_INDEPENDENCE_VIOLATED` Ledger entry types | Appendix C additions. | B (new entry types) |
| `CALIBRATION_RATIFICATION_JUDGE` ceremony type | Parallel to §22.5 ceremony path under IC-SCOPE-AUTH-1. | B (new ceremony type) |
| `granularity_decision_record.json` | Pins per-probe vs. per-domain vs. global default decision per §4.4. | A (closes structural-shape OQ) |
| Five new IC-V-JUDGE-CALIB-{1..5} interface contracts | Appendix B additions. | B (additive ICs) |
| Drift detection / weekly reserved-subset re-judgment policy | New operational invariant; touches IC-V-JUDGE-CALIB-5. | B |

### 2.6 Aggregate

| Spec edit class | Count of POC deliverables landing |
|---|---|
| A (provisional fill — no spec text change) | ~12 |
| B (additive amendment — v1.2.1 point release) | ~14 |
| C (load-bearing assumption invalidation) | conditional on KILL outcomes only |

The bulk of the POC's spec-revision impact is concentrated in Class B. The amendment ceremony (§4) is the load-bearing process for absorbing Class B.

---

## 3. Go / Revise / Kill Decision Tree per Protocol

*All six specialist voices weigh in on outcomes touching their domain. KILL aggregation rules per MEMIT-COMPAT-PROTO-1 §6 govern the categorical kill paths.*

### 3.1 MEMIT-COMPAT-PROTO-1

| Outcome | Trigger | Disposition |
|---|---|---|
| **GO (seal as-is)** | SECT 3/3 L1 + ≥2/3 L2 + 3/3 isolation; OP D20-UPHELD on all 3 facts; CFB delta ≤ 0.5%. | Stage 2 admissible. No spec edit; provisional flags clear at downstream ratifications. |
| **REVISE (targeted)** | SECT EXTENSION_REQUIRED ambiguous; OP `D20-DRIFT` (1–2 neighborhood probes shift); KILL-2/5/6 individually. | Extension protocol authored to disambiguate model-specific vs. implementation-specific cause. Stage 2 may proceed with carry-forward `orthogonal_projection_drift_observed` flag enlarging Stage 2/3 error bars. Class B amendment if D20-DRIFT requires §8 spec-text qualification. |
| **KILL (D12 revisit)** | KILL-1, -3, -4, -7 individually. Any two of KILL-2/5/6 jointly. | POC halts. **Class C — full re-ratification path.** Options: target band redeclaration; model swap; GRACE pivot; architectural redesign. Triggers Workstream 1 re-scoping, not Workstream 1 amendment. |

### 3.2 MEMIT-DRIFT-PROTO-1

| Outcome | Trigger | Disposition |
|---|---|---|
| **GO** | Clean knee with `N_warn` / `N_hard` derivable as point values (or tight intervals); hysteresis `N_hard ≥ 1.5 × N_warn` holds; reconciliation tolerance preserved. | Class A — Tier 1 config fields populated via `CALIBRATION_RATIFICATION` ceremony. |
| **REVISE (targeted)** | Threshold spread `> 1.5×` (POC-scope §4 ambiguity rule) — extension required, ratify ranges instead of points. `DRIFT-NO-HYSTERESIS` extension flag. Tier or family stratification flag fires. | Extension or replicate expansion. Class A for ratifying ranges; Class B if stratification flag fires (new sub-counter required in IC-WE-1). |
| **KILL** | No knee — fidelity degrades approximately linearly from N=1 with no inflection across the 12-point sweep. | **Class C — full re-ratification.** Invalidates §8.7 tier-based drift model. Forces redesign of `drift_state` semantics from tier-based to continuous-budget. Triggers an integrated-spec session analogous to v1.0 → v1.1 transitions. |

### 3.3 EPSILON-CALIB-PROTO-1

| Outcome | Trigger | Disposition |
|---|---|---|
| **GO** | Per-cell ε stable across reference corpus (replicate stddev < 0.15, patch-position effect ≤ ε); chosen M values do not produce false-positive compaction aborts when replayed; BUCKET boundaries derivable per Path A or Path B. | Class A — `larql_epsilon_table`, M values, bucket boundaries populated via existing §22.5 ceremony. |
| **REVISE (targeted)** | Per-class ε split — some calibrate cleanly, others (typically COMPUTE) are unstable. `M_HYSTERESIS_COLLAPSED` flag (`M_hard < 2 × M_advisory`). Cell validity gate failure on a subset. | Ship calibrated classes via §22.7 ratification; flag unstable classes with `calibration_state: UNCALIBRATED`. Operator policy on M hysteresis collapse. Class A for ratifying calibrated subset; cell-by-cell. |
| **KILL** | ε divergence at p50 (not p95) > `Δfidelity_max = 0.05` for one or more transform classes that are non-optional in production manifests. | **Class C — partial re-ratification.** Implies §22's tolerance assumption is mis-scaled and the compaction model needs revisiting. Forces revisit of `Δfidelity_max` itself, not just per-class ε. |

### 3.4 COMPACTION-PROBE-CALIB-PROTO-1

| Outcome | Trigger | Disposition |
|---|---|---|
| **GO** | Clean operating point for SUPPORTING and INCIDENTAL with FN ≤ 5% across stratum sizes ≥ 2× floor; FP ≤ 10% at threshold + 0.02; floors validated; θ_infra empirically grounded. | Class B — additive amendment cluster: floor/threshold updates (§11.14), CompactionProbeReport schema v1.3 (IC-OC-PROBE), new ceremony type, new Ledger entry, sidecar file spec. |
| **REVISE (targeted)** | Provisional INCIDENTAL threshold change 0.80 → 0.85 (FN-cost-weighted tightening); family stratification required (adversarial > 1.5× balanced); θ_infra non-uniform bias indicates systemic measurement issue. | Class B as base; add per-family sub-counter to IC-OC-PROBE if family stratification fires. |
| **KILL** | `PROBE_INSTABILITY_DETECTED` — < 50% Stage A admission rate signals model probe instability is fundamental. | Kicks back to MEMIT-COMPAT-PROTO-1 OP-1 envelope review. **Class C in the worst case** — implies the model's behavioral probe surface is too noisy to support the L2 probe family as designed. May invalidate downstream §21 probe family assumptions. |

### 3.5 JUDGE-CALIB-PROTO-1

| Outcome | Trigger | Disposition |
|---|---|---|
| **GO** | §4.4 hypothesis decision rule produces a unique selected granularity (per-probe or per-domain or global); independence firewall holds; latency budget satisfied; per-cell adversarial floor met. | Class A on triple values + Class B on infrastructure (eighth Tier 2 corpus, three new Ledger entry types, ceremony type, five ICs). Closes OQ-V-JUDGE-THRESHOLD. |
| **REVISE (targeted)** | Indeterminate granularity — corpus expansion invited at ceremony pause; latency-fail → alternate judge candidate selection; partial coverage on self-referential probes (`judgment_v1_coverage: PARTIAL`). | Iteration on judge candidate or corpus; not destructive. PARTIAL coverage forwarded to OQ-V-SELF-REF v2 — not blocking for v1.2.1. |
| **KILL** | Independence firewall fail — judge candidate shares family or weights with target. | Judge-model selection re-opens. **No D12 revisit; no spec-revision pass.** This is a candidate-level failure, not a framework-level failure. The protocol's C-JUDGE-INDEP firewall is doing its job. |

### 3.6 Aggregation Across All Five Protocols

The Workstream 1 outcome is one of:

- **Full GO across all five** → spec edits land as Class A fills + Class B amendment cluster (v1.2.1 point release).
- **GO with REVISE on a subset** → calibrated cells / stable thresholds ship; unstable cells flagged `UNCALIBRATED` per §22.7; partial v1.2.1 release.
- **KILL on Stage 1 or "no knee" on Stage 2** → POC halts; D12 revisit; Workstream 1 re-scopes (this is the explicit kill condition from write-engine-poc-scope §4).
- **KILL on Stage 3** → partial ratification possible; affected layer specs re-evaluated; v1.3 (not v1.2.1) likely.

---

## 4. Spec-Revision Ceremony — POC Outcome to v1.2-Point-Release Edit

*Primary voices: Warden (ceremony envelope authority), State Consistency Theorist (amendment ordering / supersession). Anchored to v1.2 Appendix G amendment record convention.*

POC outcomes route to spec edits via three categories. The category determines the process.

### 4.1 Category A — Provisional Fill (No Spec Text Change)

**When:** A POC outcome populates a field that v1.2 already specced as PROVISIONAL or implementation-phase.

**Process:**
1. Operator submits the calibration packet via the appropriate runtime ceremony:
   - `CALIBRATION_RATIFICATION` (§22.5; existing) for ε / M / bucket boundary fills.
   - `CALIBRATION_RATIFICATION_OC3` (Class B prerequisite — see §4.2) for compaction probe fills.
   - `CALIBRATION_RATIFICATION_JUDGE` (Class B prerequisite) for judge triple.
2. The ceremony populates Tier 1 `genesis-seal.json` fields and clears provisional flags.
3. The spec's next integrated iteration (v1.2.X) records the cleared-flag state, but no new spec text is authored. Appendix G receives no new amendment row for Class A fills.

**Authority:** existing IC-SCOPE-AUTH-1 envelope, existing ceremony types (or new ones whose authoring is itself Category B).

### 4.2 Category B — Named Amendment (v1.2.1 Point Release)

**When:** A POC outcome introduces new fields, new ceremony types, new Ledger entry types, new sealed corpora, or modifies provisional values significantly enough that spec text must change.

**Process — the amendment ceremony for v1.2.1:**

1. **Cluster amendments by domain.** Do NOT author one targeted council session per amendment. POC outcomes naturally cluster:
   - **Cluster B-WE** (Write Engine): `N_critical` Tier 1 field, drift sub-counter additions, `epsilon_history` audit overlay, `PROBE_SET_RATIFICATION` ceremony type. Authoring session: MEMIT Specialist primary, Warden secondary.
   - **Cluster B-OC3** (Compaction): floor/threshold updates to §11.14, CompactionProbeReport schema v1.3, sealed sidecar IC, `COMPACTION_PROBE_FAILED` Ledger entry, `CALIBRATION_RATIFICATION_OC3` ceremony type. Authoring session: Validation Contract Architect primary, MEMIT and Warden secondary.
   - **Cluster B-JUDGE** (Judge): eighth Tier 2 sealed corpus addition, three new Ledger entry types, `CALIBRATION_RATIFICATION_JUDGE` ceremony type, five IC-V-JUDGE-CALIB contracts, drift detection policy. Authoring session: Validation Contract Architect primary, Warden secondary.

2. **Run a targeted council session per cluster.** Each session produces:
   - A draft amendment block for each spec change in the cluster.
   - One row per amendment for Appendix G in the canonical format `Amendment | Ratified in | Applied at | Summary of effect`.
   - Cross-references back to the originating POC ratification packet (each amendment row includes the calibration packet hash).

3. **Assign amendment IDs.** Continue the v1.2 sequence: A15, A16, A17, …. The session-summary skill enforces the assignment is sequential and non-colliding.

4. **Bundle as v1.2.1 minor-version increment.** No new architecture. No load-bearing decision reversed. All amendments either additive or clarifying. Strictly mirrors the v1.1 → v1.2 amendment-only path documented in Appendix G ("No amendment in v1.2 reverses a v1.1 decision or removes a v1.1 interface contract. All v1.2 amendments are either additive or clarifying.").

5. **Single ratification step.** The v1.2.1 spec is ratified by the same operator authority that ratified v1.2. No multi-operator quorum required. The cluster amendments share a single ratification ceremony.

**Constraint — C-POC-6 — Amendment cluster size discipline.** A single targeted council session MUST NOT author more than one cluster's amendments. Mixing clusters (e.g., write-engine + compaction in the same session) loses specialist focus and produces under-reviewed amendments. Three POC-driven clusters → three targeted sessions.

### 4.3 Category C — Load-Bearing Assumption Invalidation

**When:** A POC KILL outcome invalidates a v1.2 load-bearing assumption (e.g., MEMIT works on the target architecture; the drift curve has a knee; the §22 ε tolerance is well-scaled).

**Process — full re-ratification:**

1. **D12 revisit per MEMIT-COMPAT-PROTO-1 §6.** The POC produces a documented finding; the actual D12 revisit happens in a separate workstream re-scoping.
2. **Affected layer specs re-evaluated.** Not amended — re-authored. The §8.7 tier-based drift model, for instance, would be re-designed from a tier-based regime to a continuous-budget regime under "no-knee" KILL.
3. **Trigger an integrated-spec session.** Analogous to v1.0 → v1.1 → v1.2 transitions. Multi-session council arc producing a v1.3 (not v1.2.1) integrated spec. The full spec-writer skill is engaged.
4. **POC ratification packets are NOT submitted.** A ratification packet that would seal an invalidated assumption is rejected at submission.

**Constraint — C-POC-7 — Category C boundary.** A KILL outcome MUST NOT be processed via Category B amendment route. The amendment record convention (Appendix G) explicitly preserves the rule that no v1.2 amendment reverses a v1.1 decision or removes a v1.1 interface contract. A Category C event is a reversal — it requires re-ratification, not amendment.

### 4.4 Routing Decision Rule — IC-WS1-2

```
INTERFACE CONTRACT IC-WS1-2: POC outcome → spec-edit category routing
  From: POC packet (any of 5 protocols)
  To:   Spec maintenance workstream
  What A exposes:
    - Outcome verdict ∈ {GO, REVISE-targeted, KILL-categorical}
    - Affected spec sections (cited inline)
    - Provisional flags affected
    - New mechanism additions (if any)
  Conditions:
    - GO + only provisional fills → Category A
    - GO + new mechanism addition → Category B (cluster amendment)
    - REVISE-targeted that lands within v1.2 mechanism shape → Category A or B per affected sections
    - KILL-categorical that invalidates a v1.2 mechanism → Category C
  Failure behavior:
    - Submission with mixed Category B + Category C content → REJECTED at ingress;
      submitter splits the packet by category.
```

---

## 5. POC-to-Workstream-3 Implementation-Planning Handoff

*Primary voices: Orchestration Comparativist (path-independent component scope), Validation Contract Architect (probe runtime), MEMIT Specialist (Tier 1 config consumption), Warden (Ledger entry emission).*

Workstream 3 is implementation planning for path-independent components — components whose implementations do not depend on the GAP-4 Path A/B/C orchestration selection. The POC produces nine artifact classes that Workstream 3 consumes before path-independent component implementations can be finalized.

### 5.1 Handoff Manifest — Nine Artifact Classes

| # | Artifact | Implementation consumer | Blocking? |
|---|---|---|---|
| 1 | **Calibrated Tier 1 config values** (drift thresholds, S_ceiling, sample rates, floors, judge triple) | Boot-time configuration loader; `genesis-seal.json` schema validator; runtime drift counter; compaction probe runner | Yes — without these, runtime cannot configure |
| 2 | **`architecture_profile.json`** schema + reference instance | Model-loader implementation; consume PF-1..PF-6 fields for tokenizer pin, target-band declaration, covariance file content-hash | Yes — gates model-loader correctness |
| 3 | **Probe-set v1 corpus** with frozen template hashes + judgment dependencies | L2 probe family runtime; probe template commit pipeline; TGA test harness | Yes — gates L2 probe runtime |
| 4 | **`judge_calibration_v1` frozen triple** (per-deployment) | Judge-model invocation path in §21.4 runtime | Yes — gates `judgment_method: judge_model_classification` execution |
| 5 | **Reference Patch Corpus** (≥3,000 patches across 15 cells) | Re-calibration regression fixture; CI / canary-write smoke tests; pre-deployment validation harness | Partially — non-blocking for first deployment, blocking for re-calibration tooling |
| 6 | **CompactionProbeReport schema v1.3** + sealed sidecar file format | IC-OC-PROBE runtime emitter; Ledger entry serializer for `COMPACTION_PROBE_FAILED` / `COMPACTION_ABORTED` / `COMPACTION_PROCEEDED` | Yes — gates compaction probe report emission |
| 7 | **Eight Tier 2 sealed corpora inventory v1.3** (post-judge addition) | Storage tier implementation; corpus author registry; `corpus_init_state` Ledger entry emitter | Yes — gates corpus directory layout |
| 8 | **List of new Ledger entry types** (`COMPACTION_PROBE_FAILED`, `JUDGE_CALIBRATION_RATIFIED`, `JUDGE_THRESHOLD_DRIFT_DETECTED`, `JUDGE_MODEL_INDEPENDENCE_VIOLATED`, `PROBE_SET_v1_INSUFFICIENT_FOR_JUDGE_CALIB`) | Ledger emitter validator; Appendix C lookup table; Ledger replay tooling | Yes — Ledger schema validators reject unknown types |
| 9 | **Three new ceremony types** (`PROBE_SET_RATIFICATION`, `CALIBRATION_RATIFICATION_OC3`, `CALIBRATION_RATIFICATION_JUDGE`) specified | Ceremony engine type registry; CeremonyToken envelope payload validators | Yes — ceremony engine rejects unknown types |
| 10 | **Per-deployment re-calibration playbook** | Operations runbook embedded in harness as a calibration-mode procedure | Non-blocking; recommended before first re-calibration cycle |

### 5.2 What Workstream 3 Can Begin BEFORE Stage 4 Packet Acceptance

Path-independent components that consume schema (not values) can begin implementation during Stage 2 / Stage 3 execution:

- Tier 1 config schema validators (the *shape* of `larql_epsilon_table` is in v1.2 §22.4; values arrive at Stage 4).
- Ledger emitter framework (entry types are additive; framework structure is path-independent).
- Probe template runtime engine (the §21 framework is sealed in v1.2; per-template values arrive at Stage 4).
- CeremonyToken envelope parser (existing IC-SCOPE-AUTH-1 envelope; new ceremony types add payload types but envelope is unchanged).

Components that consume calibrated values MUST wait on Stage 4 packet acceptance:

- `genesis-seal.json` field population.
- Drift counter threshold-comparison logic.
- Compaction probe sampling rate runtime.
- Judge invocation path (specifically the threshold value).

### 5.3 Interface Contract — IC-WS1-1

```
INTERFACE CONTRACT IC-WS1-1: POC packet → §22.5 ceremony ingress
  From: Stage 4 consolidation output (the unified POC packet)
  To:   Three parallel ceremony paths (CALIBRATION_RATIFICATION,
        CALIBRATION_RATIFICATION_OC3, CALIBRATION_RATIFICATION_JUDGE)
  What A exposes:
    - Bundled Deliverables 1–8 with signing CAK metadata block
    - Per-protocol verdict (GO / REVISE / KILL) and aggregated POC verdict
    - architecture_profile_hash anchor (cross-references all sub-packets)
    - probe_set_v1_hash anchor
    - reference_patch_corpus_hash anchor
    - calibration_epoch_id (single ID across the unified packet)
  Conditions:
    - All three sub-packets share the same calibration_epoch_id (ensures
      Stage 3 sub-protocols ran against the same anchor state).
    - Aggregate POC verdict = GO or GO-WITH-REVISE on all five protocols
      (a single KILL routes to Category C, not §22.5 ingress).
  Failure behavior:
    - Sub-packet hash mismatch across the three ceremonies →
      CALIBRATION_PACKET_HASH_DIVERGENCE (SECURITY, sync); both
      ceremonies fail; operator re-bundles.
    - calibration_epoch_id mismatch across sub-packets →
      CALIBRATION_EPOCH_DRIFT (SECURITY, sync); operator re-runs the
      Stage 3 sub-protocol whose epoch drifted.
```

---

## 6. Risks and Mitigations — Top Three

*Each risk is voiced by the specialist with primary domain over the failure mode.*

### 6.1 Risk 1 — Probe-Set v1 Instability (Stage 0 → Stage 1+ exposure)

**Voice:** ✅ Validation Contract Architect (primary), 🔬 MEMIT Specialist (secondary).

**Trigger:** Probe-set v1 produces inconsistent results across replicate runs. Stage 1 SECT or CFB shows replicate stddev exceeding the stability budget. Compaction probe Stage A admission rate falls below 50% (`PROBE_INSTABILITY_DETECTED`). Stage 3a cell validity gate failure on stddev > 0.15.

**Impact:** Catastrophic. Every downstream calibration is anchored on an unstable foundation. Calibration on instability ratifies nothing — the resulting Tier 1 fields are noise, not signal. Worst case: false thresholds clear provisional flags but produce production-incorrect values, surfacing as latent corruption.

**Probability:** Medium. Probe authorship is hard work; the 10/10 stability filter on the compaction protocol expects only 70–85% admission rate. Probe-set v1 is the load-bearing artifact under all five protocols.

**Mitigation:**
- **Probe-set authorship pass is its own Stage 0 sub-phase, with explicit stability validation.** Operator runs CFB v1 pre-edit baseline three times before Stage 1 opens. Replicate stddev across baselines must clear the protocol's stability budget. Failure halts Stage 1 admission; probe-set authorship re-opens.
- **The 10/10 pre-edit / pre-compaction stability filter is non-negotiable per COMPACTION-PROBE-CALIB-PROTO-1 §1.2.** Cannot be relaxed for any reason. < 50% admission triggers kickback to MEMIT-COMPAT-PROTO-1 OP-1 envelope review.
- **Build slack into Stage 0 schedule — budget for one full probe-set authorship re-pass.** Operators who skip this build a calibration on sand.
- **Carry `probe_set_v1_stability_validated` as a Stage 1 entry precondition.** Stage 1 protocol does not open without it.

### 6.2 Risk 2 — MEMIT-COMPAT KILL Invalidates Write-Engine Premise (Stage 1)

**Voice:** 🔬 MEMIT Specialist (primary).

**Trigger:** KILL-1 (causal tracing miss), KILL-3 (L1 storage path broken), KILL-4 (overlay non-isolation), KILL-7 (catastrophic forgetting at N=1), or any two of KILL-2/5/6 jointly.

**Impact:** Catastrophic. POC halts. D12 revisit forced. Options: target band redeclaration (operator policy); model swap (re-run Stage 1 entirely); GRACE pivot (different write technique — major framework change); architectural redesign. Workstream 1 re-scopes; Workstream 3 implementation planning waits on the re-scope.

**Probability:** Medium-low if SC-1..SC-6 selection criteria hold. Higher for less-tested model families. SC-6 (documented MEMIT precedent) is the strongest filter; brand-new architectures without precedent require an OQ-W2-LITERATURE extension that this protocol does not author.

**Mitigation:**
- **Target model selection rigour.** Hard constraints SC-1..SC-6 are non-optional; operational constraints SC-7/8/9 require ≥ 2 of 3. SC-6 specifically: operator MUST identify at least one published or open-source MEMIT implementation against the model family or an architecturally-equivalent sibling before this protocol opens.
- **EXTENSION_REQUIRED disambiguates model-specific from implementation-specific cause** before declaring categorical KILL. This is built into the protocol; operators MUST honor it rather than escalating directly to D12 revisit.
- **Operator may pre-screen with cheap single-edit tests** on multiple candidate models before committing the full POC schedule. A 2-day pre-screen against three candidates costs less than a 12-week POC against the wrong candidate.
- **Two of {KILL-2, KILL-5, KILL-6} jointly** is the only multi-kill aggregation that triggers immediate D12 revisit without further extension. Single instances of those three carry extension as the default disposition — preserve that branch.

### 6.3 Risk 3 — No Knee in Drift Curve (Stage 2)

**Voice:** 🔬 MEMIT Specialist (primary), ⚖️ State Consistency Theorist (secondary — drift_state semantics).

**Trigger:** M1 (CFB pass rate), M2 (perplexity), M3 (intrusion rate) all degrade approximately linearly from N=1 across the 12-point sweep with no inflection point. Threshold derivation rule produces no `N_warn` because the "first-noticeable-degradation" bound is crossed at the smallest tested N (50 edits) and continues degrading proportionally.

**Impact:** Severe. Invalidates §8.7 tier-based drift model (NOMINAL → WARNING → HARD → CRITICAL transitions). Forces redesign of `drift_state` semantics from a tier-based regime to a continuous degradation budget. Cascades: §22 derived M values are also tier-anchored; their derivation rule presumes a knee. This is a Class C event — full re-ratification, not amendment.

**Probability:** Low. Empirical MEMIT literature suggests a knee exists. However, the curve shape is model-specific, and v1.2's tier-based model is an operational simplification that may not survive empirical contact with every model family.

**Mitigation:**
- **Pre-screen with a low-density mini-sweep before committing full Sweep A.** At sample points {200, 1000, 4000, 8000} run a cheap pilot with 1 replicate × 1 patch size to confirm a knee exists, before launching the full Sweep A + B + C + D matrix. The pilot costs ~10% of full Stage 2 GPU-hours; the savings on a no-knee detection is ~90% of Stage 2 cost.
- **If pilot returns "no knee," halt Stage 2 and trigger D12 revisit before sinking the full Stage 2 cost.** This is a designed v1.3 spec-edit cycle — not a wasted POC if caught early.
- **Alternative path: accept "no knee" as a finding and ship a continuous-budget version of `drift_state` in v1.3.** This reframes Class C as Class B-major; Workstream 1 produces a v1.3 spec proposal rather than blocking on D12 revisit.
- **The hysteresis constraint `N_hard ≥ 1.5 × N_warn`** is the secondary signal: if individual thresholds are derivable but hysteresis collapses (`DRIFT-NO-HYSTERESIS` extension flag), that is a softer warning that the curve shape is degrading toward a no-knee regime. Operators should treat `DRIFT-NO-HYSTERESIS` as an early indicator and consider extending Stage 2 with longer runs before declaring success.

---

## 7. Cross-Domain Tensions Surfaced

| Tension | Specialists | Status | Resolution |
|---|---|---|---|
| **T-WS1-1 — Stage parallelism vs. probe-set immutability** | MEMIT Specialist + Validation Contract Architect | ✅ Resolved | Stage 3a, 3b, 3c gate on `PROBE_SET_RATIFICATION` ceremony, not on full Stage 3a output. Probe-set hash immutable for the calibration epoch; all three sub-protocols consume the same ratified hash. |
| **T-WS1-2 — Amendment granularity vs. council session cost** | Warden + Orchestration Comparativist | ✅ Resolved | Cluster amendments by domain (B-WE, B-OC3, B-JUDGE); one targeted council session per cluster; amendment IDs A15+ assigned sequentially. C-POC-6 disciplines cluster size: one cluster per session. |
| **T-WS1-3 — Workstream 3 implementation start vs. POC completion** | Orchestration Comparativist + State Consistency Theorist | 🔶 Partially resolved | Path-independent components consuming schema only may begin during Stage 2 / Stage 3 execution. Components consuming calibrated values wait on Stage 4 packet acceptance. The exact split per component is Workstream 3 territory — deferred as OQ-WS1-3. |
| **T-WS1-4 — Operator-owned vs. POC-owned boundary at Stage 0** | Orchestration Comparativist + MEMIT Specialist | 🔶 Acknowledged | Stage 0 is operator-owned per write-engine-poc-scope §6. Reference patch corpus realism (synthetic vs. agent-output samples) is open as OQ-WS1-2 — operator decision affects Stage 0 prerequisite cost, not POC scope. |

### Pre-Mapped Tension Coverage

Per the framework-council pre-mapped tension routing rule, the following pre-mapped tensions are touched by this synthesis:

- **Pre-T1 (Immutability vs. Mutability Window) — touched.** Ratification ceremonies (existing `CALIBRATION_RATIFICATION` and three new sibling ceremony types) populate Tier 1 `genesis-seal.json` fields post-Genesis-seal. Resolution path inherited from §22.5: provisional flags clear on acceptance; no rewrite of Genesis-sealed fields occurs (the fields were specced as PROVISIONAL precisely to admit this fill-in path). Warden and State Consistency Theorist voiced this resolution above (council framing + §4 Spec-Revision Ceremony). No new Pre-T1 surface; inherited resolution holds.
- **Pre-T2 (Write Volume vs. Edit Locality) — fully addressed.** N_warn / N_hard / S_ceiling derivation is the empirical anchor for the long-standing Pre-T2 resolution. MEMIT Specialist (write-volume concern) and Graph Data Architect (edit-locality concern) both voiced this resolution above (council framing + §1 Execution Plan + §3.2 Drift decision tree). The POC closes the empirical anchor.
- **Pre-T6 (Genesis Completeness vs. Genesis Lock-in) — touched.** Probe-set v1 Genesis anchoring follows the existing minimal-viable-Genesis resolution (mint at Genesis); subsequent probe-set versions enter via `PROBE_SET_RATIFICATION` (write-pipeline path). The eighth Tier 2 sealed corpus (`judge-calibration-corpus/`) is a Tier 2 corpus, not a Genesis modification — extends inventory additively per Pre-T6's existing resolution. Graph Data Architect and MEMIT Specialist positions inherited from prior sessions; no new engagement required.

Pre-T3 (Validator Independence vs. Test Coverage), Pre-T4 (Audit Completeness vs. Write Throughput), and Pre-T5 (Schema Stability vs. Agent Autonomy) are not newly touched by this synthesis — their resolutions inherited from prior sessions hold unchanged.

---

═══════════════════════════════════════════════════
## Session Summary Block — Workstream 1 Closing Synthesis
═══════════════════════════════════════════════════

**Session:** 1.7 — Workstream 1 closing synthesis (closes Sessions 1.1–1.6)
**Status:** Draft — pending operator review.
**Specialist provenance:** Framework Council (all six specialists). Primary voices: MEMIT Specialist (execution sequencing), Validation Contract Architect (probe-side gating), Warden (amendment ceremony authority), State Consistency Theorist (amendment ordering), Graph Data Architect (Tier 1 config field placement), Orchestration Comparativist (Workstream 3 handoff).

### Decisions made

- **D-WS1-1 — Stage execution sequence locked.** Stage 0 (operator preconditions) → Stage 1 (MEMIT-COMPAT-PROTO-1, gating) → Stage 2 (MEMIT-DRIFT-PROTO-1, sequential) → Stage 3 prelude (`PROBE_SET_RATIFICATION` ceremony) → Stage 3a / 3b / 3c (parallel) → Stage 4 (consolidation). All pairwise sequencing constraints carry as C-POC-1..C-POC-5.
- **D-WS1-2 — Stage 3 internal parallelism gated on `PROBE_SET_RATIFICATION`.** All three Stage 3 sub-protocols share the same probe-set v1 hash anchor and `calibration_epoch_id` post-ratification. Authoring of Stage 3 protocols may parallelize with Stage 2 execution per the existing scope §6 critical-path note; *execution* of Stage 3 sub-protocols requires Stage 2 outputs committed.
- **D-WS1-3 — POC outcomes route to spec edits via three categories.** Category A (provisional fill via existing `CALIBRATION_RATIFICATION` and sibling ceremonies — no spec text change); Category B (named amendment cluster A15+ via targeted council sessions for v1.2.1 point release); Category C (D12 revisit / full re-ratification for load-bearing assumption invalidation, producing v1.3 not v1.2.1).
- **D-WS1-4 — Amendment cluster discipline.** Three POC-driven amendment clusters identified: B-WE (write engine), B-OC3 (compaction), B-JUDGE (judge calibration). One targeted council session per cluster; mixing clusters in a single session is prohibited (C-POC-6).
- **D-WS1-5 — Workstream 3 handoff manifest defines nine artifact classes plus a re-calibration playbook.** Path-independent components consuming schema may begin implementation during Stage 2/Stage 3 execution; components consuming calibrated values wait on Stage 4 packet acceptance.
- **D-WS1-6 — Top-three POC risk register defined with per-risk pre-flight or pilot mitigation.** Probe-set v1 instability (Stage 0); MEMIT-COMPAT KILL (Stage 1); no-knee drift curve (Stage 2). Each carries a designed mitigation that is non-optional for operator schedule planning.
- **D-WS1-7 — Wall-clock envelope estimated.** ~7–11 weeks multi-GPU; ~12–22 weeks single-GPU on a 7B–13B target. ~1,000–2,400 GPU-hours total. ~3,500–4,500 human-hours for corpus authorship across Stage 0 and Stage 3. Numbers are estimates, not commitments.

### Constraints established

- **C-POC-1 — Stage 1 / Stage 2 sequencing.** Stage 2 MUST NOT open execution until Stage 1 returns PASS or D20-DRIFT.
- **C-POC-2 — Stage 2 → Stage 3 sequencing.** Stage 3 sub-protocols MUST NOT begin execution until `S_ceiling` and drift threshold values from Stage 2 are committed. Authorship may parallelize with Stage 2 execution.
- **C-POC-3 — Stage 3 internal gating.** Stage 3a, 3b, 3c all gate on `PROBE_SET_RATIFICATION` ceremony completion as Stage 3's prelude.
- **C-POC-4 — SBC-before-Sweep ordering.** Sub-batch ceiling sub-protocol MUST complete before the main drift sweep opens.
- **C-POC-5 — Reconciliation gate.** Sample points failing C-WE-1 5% reconciliation tolerance are discarded, not corrected.
- **C-POC-6 — Amendment cluster size discipline.** A single targeted council session MUST author at most one cluster's amendments. Three clusters → three sessions.
- **C-POC-7 — Category C boundary.** A KILL outcome MUST NOT be processed via Category B amendment route. Category C requires full re-ratification, not amendment.

### Open questions deferred

- **OQ-WS1-1 — Operator target-model commitment** — pending operator decision; gates Stage 1 execution. Inherited from Session 1.1.
- **OQ-WS1-2 — Reference patch corpus realism.** Synthetic-only acceptable, or representative agent-output samples required? Affects Stage 0 prerequisite cost. Inherited from Session 1.1.
- **OQ-WS1-3 — Workstream 3 implementation-start cut per component.** The exact split between schema-only and value-consuming components is Workstream 3 territory; defer to Workstream 3 kickoff session.
- **OQ-WS1-4 — Multi-GPU parallelization in Stage 3.** Wall-clock envelope assumes single-GPU baseline; multi-GPU compression is operator-decision territory. Affects schedule, not protocol shape.
- **OQ-WS1-5 — Operator execution model** — execute end-to-end vs. hand off Stage-by-Stage. Affects required specificity of expected-result shapes. Inherited from Session 1.1.

### Interface contracts defined

- **IC-WS1-1** — POC packet → §22.5 ceremony ingress (consolidates EPSILON-CALIB + COMPACTION-PROBE + JUDGE-CALIB submission packets via shared `calibration_epoch_id` and cross-anchored hashes).
- **IC-WS1-2** — POC outcome → spec-edit category routing (the rule that maps result type to amendment path; rejects mixed Category B + Category C content at submission ingress).

### Cross-domain tensions surfaced

- **T-WS1-1 — Stage parallelism vs. probe-set immutability** (MEMIT + Validation) — ✅ Resolved via Stage 3 prelude `PROBE_SET_RATIFICATION` ceremony.
- **T-WS1-2 — Amendment granularity vs. council session cost** (Warden + Orchestration Comparativist) — ✅ Resolved via three-cluster discipline (C-POC-6).
- **T-WS1-3 — Workstream 3 implementation start vs. POC completion** (Orchestration Comparativist + State Consistency Theorist) — 🔶 Partially resolved (schema-vs-values split principle confirmed; per-component cut deferred as OQ-WS1-3).
- **T-WS1-4 — Operator-owned vs. POC-owned boundary at Stage 0** (Orchestration Comparativist + MEMIT) — 🔶 Acknowledged (operator decision affects cost, not protocol shape).

### Pre-mapped tension coverage

- **Pre-T1 (Immutability vs. Mutability Window)** — touched at ratification populating Tier 1 fields. Resolution inherited from §22.5. Warden + SCT voiced inline (§4 Spec-Revision Ceremony). No new Pre-T1 surface.
- **Pre-T2 (Write Volume vs. Edit Locality)** — fully addressed by POC empirical anchor. MEMIT + Graph Data Architect voiced inline (§1 + §3.2). The POC closes the empirical anchor that v1.0–v1.2 left provisional.
- **Pre-T6 (Genesis Completeness vs. Genesis Lock-in)** — touched at probe-set v1 anchoring + eighth Tier 2 sealed corpus. Inherited resolution holds; no new Pre-T6 surface.

### Spec edits anticipated (preview of v1.2.1 amendment cluster)

| Cluster | Amendments anticipated | Authoring session |
|---|---|---|
| **B-WE (Write Engine)** | `N_critical` Tier 1 field; drift sub-counter additions to IC-WE-1; `epsilon_history` audit overlay; `PROBE_SET_RATIFICATION` ceremony type (closes OQ-W-PROBE-MINT) | MEMIT Specialist (primary) + Warden (secondary) |
| **B-OC3 (Compaction)** | §11.14 floor/threshold updates; CompactionProbeReport schema v1.3 (IC-OC-PROBE extension); sealed sidecar IC; `COMPACTION_PROBE_FAILED` Ledger entry; `CALIBRATION_RATIFICATION_OC3` ceremony type | Validation Contract Architect (primary) + MEMIT + Warden (secondary) |
| **B-JUDGE (Judge Calibration)** | Eighth Tier 2 sealed corpus `judge-calibration-corpus/`; three new Ledger entry types; `CALIBRATION_RATIFICATION_JUDGE` ceremony type; five IC-V-JUDGE-CALIB contracts; drift detection policy | Validation Contract Architect (primary) + Warden (secondary) |

**Estimated v1.2.1 amendment count:** ~14 new amendments (A15–A28). All strictly additive or clarifying. None reverse a v1.2 decision; none remove a v1.2 interface contract.

### Non-Goals

This synthesis does NOT specify:
- Numeric calibration values (those are produced by execution against a committed target model and corpus).
- Stage 0 execution prerequisites beyond what write-engine-poc-scope §6 specifies — Stage 0 is operator-owned.
- Workstream 2 scope (orchestration path selection — GAP-4 family — is a separate workstream).
- Workstream 3 implementation language, framework, or runtime (path-independent components are spec-only at this layer).
- Per-GPU-class wall-clock numbers (estimates assume mid-tier A100/H100; smaller or larger GPUs scale roughly linearly with model parameter count).
- Re-calibration cadence policy (operator-owned per §22.8; OQ-W-CALIB-CADENCE inherited from Session 1.4).

### Next session candidates

- **Stage 0 execution prep (operator-owned, NOT council session):** target model commitment per SC-1..SC-9; probe-set v1 + reference patch corpus authorship sprint; CFB v1 stability validation.
- **Workstream 1 amendment cluster sessions (three sessions, post-Stage 4):**
  1. B-WE cluster — MEMIT Specialist primary + Warden secondary.
  2. B-OC3 cluster — Validation Contract Architect primary + MEMIT + Warden secondary.
  3. B-JUDGE cluster — Validation Contract Architect primary + Warden secondary.
- **Targeted Warden session (pre-Stage 4 acceptable):** review OQ-W-PROBE-MINT — `PROBE_SET_RATIFICATION` ceremony envelope mechanics, joint-attestation field structure under IC-SCOPE-AUTH-1. Inherited from Session 1.4.
- **Targeted Validation + MEMIT session (pre-Stage 4 acceptable):** GAP-15 ownership — Behavioral Probe Agent identity, independence enforcement, pool architecture, prober reliability monitoring. Deployment-blocking status retained until resolved. Inherited from Session 1.5.
- **Workstream 3 kickoff (post-Stage 4 packet acceptance):** path-independent component implementation planning, with the nine-artifact-class handoff manifest as input. Resolves OQ-WS1-3 (per-component schema-vs-values cut).
- **OQ-V-SELF-REF v2 framing session (Validation-domain, v2 scope):** consume the `judgment_v1_coverage: PARTIAL` case set produced by Session 1.6 as input. Frame v2 resolution: in-corpus target-model probing, model-state-aware corpus patterns, ensemble-bypass routes. Inherited from Session 1.6.

═══════════════════════════════════════════════════
*Workstream 1 Closing Synthesis — Sessions 1.1–1.6 consolidated. Awaiting operator review and Stage 0 execution prep before POC opens. Spec-revision feedback rule (D-WS1-3) is the bridge from empirical work to v1.2.1 point-release amendment authorship.*
═══════════════════════════════════════════════════
