# EPSILON-CALIB-PROTO-1 — Per-Transform-Class ε / M / Bucket Calibration Protocol

*Workstream: Empirical POC Scoping (post-v1.2 sealed spec)*
*Session: Stage 3 protocol authorship — addresses OQ-W-CALIB-1, GAP-1, GAP-2, GAP-48 (residual)*
*Primary skills: memit-specialist + validation-contract-architect (joint)*
*Status: design-complete; gated on MEMIT-COMPAT-PROTO-1 PASS + MEMIT-DRIFT-PROTO-1 outputs (`S_ceiling`, drift thresholds) before execution*

The protocol operationalizes §22 (`larql_fidelity_calibration`). §22 ratifies the structure (D-GS8-A); this protocol authors the execution design. It produces the `epsilon_calibration_report` artifact consumable by the `CALIBRATION_RATIFICATION` ceremony (§20 / §22.5), including per-cell ε values, derived M thresholds for the T13 three-tier model, and bucket boundary tables for non-default BUCKET transforms (D-GS8-B).

This protocol consumes — does not author — five artifacts from prior protocols:
- `architecture_profile.json` (MEMIT-COMPAT-PROTO-1 PF-6)
- `S_ceiling` (MEMIT-DRIFT-PROTO-1 SBC)
- Probe-set v1 corpus with frozen template hashes (MEMIT-COMPAT-PROTO-1 + Validation collaboration)
- Reference Patch Corpus (≥200 patches per class-hop per §22.2; Stage 0 operator-owned)
- TGA Health Score record at probe authorship (§9.4 L4 / IC-V-TGA2)

---

## 1. Calibration Cell Cut — Transform-Class Stratification

### 1.1 The Cut Chosen

Calibration cells are stratified along three nested axes:

**Primary axis — Transform class (5 classes, fixed by §22.4):**
- `RENAME` — entity / relation / target rename
- `BUCKET` — continuous attribute discretization
- `COMPUTE` — derived field replacement
- `DROP` — deprecated edge removal
- `DEFAULT_INSERT` — new mandatory field default insertion

**Secondary axis — Importance tier (3 tiers, mirrors §8.9 / §9.4 L2 cascade):**
- `CORE`
- `SUPPORTING`
- `INCIDENTAL`

**Tertiary axis — Relation family (5 families per D6, conditional on empirical trigger):**
- `Structural` / `Knowledge` / `Constraint` / `Taxonomy` / `Namespace`
- Tertiary stratification engages **only if** post-primary calibration shows family deviation outside the band `ε(family-pure) / ε(family-balanced) ∉ [0.8, 1.25]`. Mirrors MEMIT-DRIFT-PROTO-1 §6 stratification trigger.

**Default cell count:** 5 × 3 = 15 cells. Tertiary trigger doubles a subset; full tertiary expansion would yield 5 × 3 × 5 = 75 cells (worst-case, not expected default).

### 1.2 Rejected Cuts

The following candidate axes were considered and rejected:

| Candidate axis | Rejection rationale |
|---|---|
| Edit volume (per-patch edge count) | Conflates transform-class fidelity with patch-size locality — already controlled by `S_ceiling` from MEMIT-DRIFT-PROTO-1 SBC. Calibrating both simultaneously confounds the signal. |
| Probe sub-type (Generation / Assertion / Constraint per §21) | Probe sub-type is a response-scoring axis, not a transform axis. Patches with the same transform may bind to probes of different sub-types; sub-stratifying ε on scoring axis scatters per-class signal. |

### 1.3 Per-Cell Reference Patch Requirement

- Minimum 200 patches per cell per version hop measured (§22.2 floor, applied per-cell).
- Default corpus size at primary stratification: 15 × 200 = 3,000 patches per version hop.
- Tertiary expansion adds patches only for cells that triggered family stratification.

---

## 2. Probe-Set v1 Authorship and Binding

### 2.1 Probe Authorship Authority

Probe templates are TGA-authored per §21.3 — preserved unchanged. This protocol does not modify §21.3. TGA authority over probe template authorship is uncontested by this calibration.

### 2.2 Probe-to-Patch Binding

Each reference patch in the calibration corpus carries one or more **bound probes** drawn from probe-set v1. The binding is established at Stage 0 corpus authorship and is content-hashed into the corpus identity.

**Binding contract:**
```
patch_probe_binding := {
  patch_id,
  bound_probes: [{
    probe_template_hash,
    elicitation_prompt_ref,
    expected_behavior_predicate,
    judgment_method ∈ {exact_substring, structured_field_match,
                       judge_model_classification},
    judgment_config (judge_model_id, judge_prompt, threshold — per §21.4)
  }, ...]
}
```

A patch with zero bound probes is unscoreable for fidelity and is excluded from calibration. A cell with fewer than 200 bound-probe-coverage patches fails §22.2 precondition and the protocol does not execute for that cell.

### 2.3 Per-Patch Fidelity Score

For each patch, fidelity is a scalar computed from the bound probe's judgment method:

| Judgment method (§21.4) | Per-probe fidelity scalar | Range |
|---|---|---|
| `exact_substring` | 1.0 if substring present, 0.0 otherwise | {0, 1} |
| `structured_field_match` | fraction of required fields matching expected values | [0, 1] |
| `judge_model_classification` | judge model confidence at the declared threshold | [0, 1] |

If a patch carries multiple bound probes, per-patch fidelity = arithmetic mean across bound probes. **Mixing judgment methods within a calibration cell is permitted** — ε aggregates per-patch fidelity scalars regardless of how each was scored, because the migration translation does not depend on judgment method.

---

## 3. Per-Class ε Measurement Protocol

Operationalizes §22.3 step-by-step. Each cell is calibrated independently.

### 3.1 Procedure (per cell, per version hop)

**Step 0 — Cell admission check.**
- ≥ 200 reference patches with valid probe bindings present.
- `architecture_profile.json` and `S_ceiling` from upstream protocols present and content-hash-verified.
- TGA Health Score at probe-template authorship ≥ 95% (or operator-acknowledged below-threshold flag for cell).

**Step 1 — Pre-translation compile.**
- Compile reference patches at `source_version` through MEMIT.
- Patch order randomized per replicate; seed logged.
- Single-patch size enforced ≤ `S_ceiling` from MEMIT-DRIFT-PROTO-1 SBC.
- Per replicate: run all bound probes; record per-probe response. Score per-probe fidelity per §2.3. Compute per-patch fidelity = mean across patch's bound probes.

**Step 2 — Replication for baseline.**
- ≥ 3 replicates per patch (5 strongly preferred).
- Different sampling seeds per replicate (model response generation).
- Fresh anchor between replicates — no inherited drift.
- Per-patch baseline fidelity = mean across replicates.

**Step 3 — Apply migration manifest translation.**
- Translate each reference patch via the `larql_migration_manifest` translator. Translation is read-only against Tier 1 manifest artifact (per IC-MANIFEST handoff).
- Translated patches retain their probe bindings (the bound probes remain valid post-translation; if a translation breaks a probe, that patch is excluded from the cell with reason `PROBE_BINDING_BROKEN_BY_TRANSLATION` — counts toward fidelity loss qualitatively but is not aggregated into ε).

**Step 4 — Post-translation compile.**
- Same as Step 1, applied to translated patches. Same patch-order randomization protocol. Fresh anchor.

**Step 5 — Replication for post-translation.**
- Same as Step 2, applied to translated patches.

**Step 6 — Per-patch fidelity delta.**
```
per_patch_delta = baseline_fidelity_mean − post_translation_fidelity_mean
```
Per-patch deltas may be negative (post-translation fidelity exceeded baseline) — these are recorded but treated as zero-delta for ε aggregation (negative deltas indicate improvement, not loss).

**Step 7 — Cell aggregation.**
- Across all per-patch deltas in the cell, compute mean, p50, p95, p99.
- **Cell ε = p95** (per §22.3 step 4).
- p99 reported as tail-watch indicator; not threshold-deriving.

### 3.2 Cell Validity Gate

A cell's ε is **valid** for ratification if:
1. ≥ 200 patches contributed valid baseline-and-post deltas (excluding `PROBE_BINDING_BROKEN_BY_TRANSLATION` patches).
2. Replicate-to-replicate per-patch standard deviation < 0.15 fidelity points across the cell median (probe-noise stability).
3. Patch-position effect across replicates does not exceed cell ε (i.e., randomization successfully factored position into noise).

A cell failing any validity gate ships in the report with `calibration_state: UNCALIBRATED` per §22.7. Operator may invoke an extension protocol (out of v1 scope) or re-author the probe-set / corpus.

---

## 4. Probe-Set Versioning Governance (OQ-W-PROBE-VERSION / GAP-48)

### 4.1 The Comparability Problem

ε values are only algebraically valid within the probe-set epoch they were calibrated against (§22.4 `calibrated_against_probe_set_version` field). If the probe set evolves, historical ε values lose comparability with new ones, breaking T13 M-threshold consumption.

### 4.2 Three-Layer Governance

**Layer 1 — Strict epoch isolation (mandatory floor):**
- `probe_set_version` is a Tier 1 config field in `genesis-seal.json`.
- Every `epsilon_calibration_report` carries `calibrated_against_probe_set_version: N`.
- Cross-epoch ε comparison emits `STALE_PROBE_VERSION` advisory in dry-run reports.
- The Tier 1 `larql_epsilon_table` is keyed by `(probe_set_version, transform_class, importance_tier)` — never overwritten across versions.

**Layer 2 — `PROBE_SET_RATIFICATION` ceremony (governance):**
- New ceremony type under IC-SCOPE-AUTH-1 envelope (§20).
- Submission requires joint MEMIT + Validation attestation in the ceremony envelope:
  - Validation attestation: probe templates conform to §21.3 TGA authorship; TGA Health Score at template authorship is recorded.
  - MEMIT attestation: a re-calibration cycle (§3) has been executed against the new probe set, producing fresh ε values.
- On acceptance:
  - `probe_set_version` increments.
  - All currently-active ε values are flagged `STALE_PROBE_VERSION`.
  - Re-calibration SLO clock starts (operator-owned policy; suggested default 30 days).
  - Tier 1 config update is atomic — `probe_set_version`, `larql_epsilon_table`, derived M table, bucket boundary table all advance under the same ceremony envelope.

**Layer 3 — `epsilon_history` audit overlay:**
- Tier 1 `genesis-seal.json` retains an `epsilon_history` field with per-epoch calibrations.
- Comparisons across epochs are not blocked but are flagged as advisory only.

### 4.3 Authorship Boundary

- TGA authors probe templates per §21.3 (unchanged).
- Probe-set version *mint* — freezing the set under a new identity — requires the `PROBE_SET_RATIFICATION` ceremony and is **not** a TGA-only act. Single-domain mint authority would let either side break the other's contract.
- Operator owns probe-set evolution cadence per §22.8.

---

## 5. BUCKET Boundary Derivation (D-GS8-B Operationalization)

### 5.1 Two Derivation Paths

For non-default BUCKET transforms (i.e., not `attention_weight → declared_importance`):

**Path A — Quantile-Based Default (operator-free):**
1. Compute empirical CDF of source values across the reference corpus.
2. For a K-bucket transform, set candidate boundaries at quantiles `1/K, 2/K, ..., (K-1)/K`.
3. Run §3 calibration with these candidate boundaries.
4. Accept if cell ε ≤ `Δfidelity_max`. Otherwise iterate with adjusted quantiles (e.g., 0.40 / 0.70 instead of 0.33 / 0.66) up to operator-set iteration cap.

**Path B — Operator-Declared (domain-knowledge override):**
1. Operator declares boundaries from domain knowledge.
2. Run §3 calibration against declared boundaries.
3. Accept if cell ε ≤ `Δfidelity_max`. Otherwise reject and require operator revision — **the protocol does not modify operator-declared boundaries on its own.**

### 5.2 Default Selection Rule

Path A is the default. Path B is invoked when the operator explicitly declares boundaries in the calibration submission. Both paths terminate in `CALIBRATION_RATIFICATION` (§22.5) — the protocol does not grant boundary authority to anyone outside that ceremony.

### 5.3 Failure Disposition

A BUCKET transform that fails to find boundaries with cell ε ≤ `Δfidelity_max` after both paths is flagged `BUCKET_UNCALIBRATED` and ships with `calibration_state: UNCALIBRATED` per §22.7. Non-blocking; advisory only. The rest of the calibration packet proceeds.

### 5.4 GS7 Default Preservation

`attention_weight → declared_importance` retains the GS7 illustrative defaults (0.33 / 0.66) as Path A starting points, with the same §22.6 validation requirement. If Path A succeeds at these starting boundaries, no change. If not, Path A iterates; if iteration fails, Path B is the operator override route.

---

## 6. M-Threshold Derivation (T13 Three-Tier Model Operationalization)

### 6.1 Canonical M Derivation

Given calibrated cell ε and `Δfidelity_max` (provisional default 0.05; ratified at calibration time per §22.4):

```
M_advisory    = floor(0.5 × Δfidelity_max / ε)
M_operational = floor(1.0 × Δfidelity_max / ε)
M_hard        = floor(2.0 × Δfidelity_max / ε)
```

The 0.5× / 1.0× / 2.0× multipliers are protocol-proposed, not spec-fixed. Mirrors hysteresis pattern of MEMIT-DRIFT-PROTO-1 §4 (`N_hard ≥ 1.5 × N_warn`). Ratification of these multipliers is part of the calibration packet submission.

### 6.2 Hysteresis Constraint (mandatory)

```
M_hard ≥ 2 × M_advisory
```

If integer-floor operations collapse the hysteresis gap (e.g., very small ε pushes M_advisory and M_hard within 1 of each other), the cell is flagged `M_HYSTERESIS_COLLAPSED`. Operator policy applies — same disposition as MEMIT-DRIFT-PROTO-1's `DRIFT-NO-HYSTERESIS` flag. This is an extension trigger, not a kill.

### 6.3 Operational Layer Boundary

M values gate **batch composition** during migration operations — how many class-c transforms can sit in a single migration before hitting advisory / pause / hard limits. M values do **not** gate L2 probe outcomes. A single L2 probe always emits binary `{success, behavior_fail}` per §21.5.

The ε that drives M derivation is the same ε that informs probe-template threshold authorship for `judgment_method: judge_model_classification` (§21.4) — but the runtime probe outcome remains binary. ε never appears in `write_outcome`; it appears only in calibration-time threshold setting and migration-time batch composition.

### 6.4 Sub-Batch Ceiling Boundary (vs. MEMIT-DRIFT-PROTO-1)

`S_ceiling` (Stage 2) and M values (Stage 3) are independent constraints on different operational axes:

- `S_ceiling` — single-patch size cap for compile fidelity (axis: edges per patch).
- M — per-class transform count cap in a migration batch (axis: transforms per class per batch).

A migration batch must satisfy both: `patch_size ≤ S_ceiling` AND `transforms_per_class ≤ M_operational`. **Conjunction, not disjunction.**

---

## 7. Ratification Artifact — `epsilon_calibration_report` Shape

### 7.1 Required Fields

```
epsilon_calibration_report := {
  report_id,
  protocol_version: "EPSILON-CALIB-PROTO-1",
  
  # Provenance
  calibrated_against_probe_set_version: N,
  calibrated_against_reference_corpus_hash,
  calibrated_against_architecture_profile_hash,    # MEMIT-COMPAT-PROTO-1 PF-6
  calibrated_against_S_ceiling,                    # MEMIT-DRIFT-PROTO-1 SBC
  
  # TGA / Validation provenance (T-EPSILON-3)
  tga_probe_authorship_evidence: [{
    probe_template_hash,
    tga_run_id,
    authored_at
  }, ...],
  tga_health_score_at_calibration,                 # IC-V-TGA2 record reference
  
  # Per-cell ε
  per_cell_calibration: [{
    transform_class ∈ {RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT},
    importance_tier ∈ {CORE, SUPPORTING, INCIDENTAL},
    relation_family_stratified: bool,              # tertiary trigger fired?
    relation_family_breakdown: [...] | null,       # populated only if tertiary
    n_patches,
    n_replicates,
    fidelity_stats: { mean, p50, p95, p99 },
    epsilon: <p95 fidelity delta>,                 # = p95 of fidelity_stats
    derived_M: { advisory, operational, hard },
    hysteresis_status ∈ {OK, COLLAPSED},
    calibration_state ∈ {CALIBRATED, UNCALIBRATED},
    cell_validity_gate_pass: bool
  }, ...],
  
  # BUCKET boundary tables (D-GS8-B)
  bucket_boundary_table: [{
    bucket_transform_id,
    derivation_path ∈ {QUANTILE_DEFAULT, OPERATOR_DECLARED},
    boundaries: [...],
    cell_epsilon,
    calibration_state ∈ {CALIBRATED, UNCALIBRATED}
  }, ...],
  
  # Tolerance and multipliers
  compaction_tolerance_used: 0.05,                 # Δfidelity_max
  m_multipliers_used: { advisory: 0.5, operational: 1.0, hard: 2.0 },
  
  # Stratification flags
  family_stratification_flags: [{
    cell_id, trigger_reason,
    family_pure_epsilon, family_balanced_epsilon, ratio
  }, ...],
  
  # Submission metadata
  signing_metadata: {
    timestamp,
    signing_CAK,
    ceremony_envelope_ref                           # IC-SCOPE-AUTH-1
  }
}
```

### 7.2 Submission Path

- Ceremony type: `CALIBRATION_RATIFICATION` per §20 / IC-SCOPE-AUTH-1 envelope.
- On acceptance, Tier 1 `genesis-seal.json` populates:
  - `larql_epsilon_table` — keyed by `(probe_set_version, transform_class, importance_tier)`.
  - `compaction_tolerance` — `Δfidelity_max` value used.
  - `derived_M_table` — keyed identically to ε table; per-cell `(advisory, operational, hard)`.
  - `bucket_boundary_table` — keyed by `bucket_transform_id`.
- Provisional flags on T13 thresholds and IC-MANIFEST-1 `bucket_map` clear in the spec's next integrated iteration.
- `epsilon_history` Tier 1 field appends the new epoch — historical epochs preserved per §4.2 Layer 3.

### 7.3 Linkage to Adjacent Protocols

| Upstream input | Source protocol | Protocol field consumed |
|---|---|---|
| `architecture_profile.json` hash | MEMIT-COMPAT-PROTO-1 PF-6 | `calibrated_against_architecture_profile_hash` |
| `S_ceiling` | MEMIT-DRIFT-PROTO-1 SBC | Step 1 / Step 4 single-patch size enforcement |
| Probe-set v1 corpus | MEMIT-COMPAT-PROTO-1 + Validation | §2 probe-to-patch binding |
| Reference Patch Corpus | Stage 0 (operator) | Cell admission §3.1 Step 0 |
| TGA Health Score | §9.4 L4 / IC-V-TGA2 | `tga_health_score_at_calibration` |

---

## 8. Kill Criteria and Extension Triggers

| Code | Trigger | Source | Severity | Disposition |
|---|---|---|---|---|
| **EPSILON-KILL-1** | ε for any non-optional transform class exceeds `Δfidelity_max` at the **p50** (not p95) | §3 cell aggregation | Categorical | §22 tolerance assumption is mis-scaled; spec-revision pass required |
| **EPSILON-KILL-2** | More than 50% of cells fail the cell validity gate (§3.2) | §3.2 | Categorical | Probe-set v1 or reference corpus is unstable; re-author before ratification |
| **EPSILON-EXT-1** | A subset of transform classes calibrate cleanly; others (typically COMPUTE) are unstable | §3.2 per-cell | Extension | Ship calibrated cells; flag unstable cells `UNCALIBRATED` per §22.7 |
| **EPSILON-EXT-2** | Tertiary stratification triggers for ≥ 3 cells (family-specific drift is widespread) | §1.1 trigger | Extension | Expand family-stratified corpus and re-run; calibration packet ships with stratified table |
| **EPSILON-EXT-3** | `M_HYSTERESIS_COLLAPSED` for one or more cells | §6.2 | Extension | Operator policy — adjust multipliers or accept collapsed regime; not blocking |
| **EPSILON-EXT-4** | `BUCKET_UNCALIBRATED` for one or more BUCKET transforms after both Path A and Path B exhausted | §5.3 | Extension | Ship affected BUCKETs with `UNCALIBRATED` flag; operator policy on whether to use them in production |

---

## 9. Open Questions Carried Forward

- **OQ-W-PROBE-MINT** — `PROBE_SET_RATIFICATION` ceremony type placement under IC-SCOPE-AUTH-1 (§20). This protocol proposes the ceremony type and joint-attestation requirement; Warden review of the IC-SCOPE-AUTH-1 envelope addition is deferred to the next Warden-domain session. Does not block this protocol's authorship; does block production deployment of probe-set version increments. (T-EPSILON-3 partial closure.)
- **OQ-W-MULT** — M-threshold multipliers (0.5 / 1.0 / 2.0) are protocol-proposed; ratification is part of the calibration packet submission. Operator may tune at calibration time.
- **OQ-W-CRITICAL-CARRY** — Inherited from MEMIT-DRIFT-PROTO-1: the CRITICAL boundary is referenced in the drift_tier enum but is protocol-authored not spec-fixed. M_hard alignment with N_critical is left to operator policy at the calibration packet level.
- **OQ-W-CALIB-CADENCE** — Re-calibration cadence after `probe_set_version` increment. §4.2 Layer 2 suggests 30-day default SLO; operator policy is owned externally per §22.8.
- **OQ-V-JUDGE-THRESHOLD** — Carried from §21. NOT resolved by this protocol. ε informs threshold authorship guidance but does not specify per-probe judge thresholds. Remains scoped to validation POC.

---

## 10. Non-Goals

§EPSILON-CALIB-PROTO-1 does not specify:
- Numeric ε / M / bucket boundary values — those are produced by execution against a committed target model and corpus, ratified via §22.5.
- Probe template authorship rules — owned by §21.3 (TGA authority).
- Ceremony envelope mechanics — owned by §20 / IC-SCOPE-AUTH-1.
- Cross-model ε transfer — calibrations are per-deployment, per §22.8.
- Reference Patch Corpus authorship rules — Stage 0 operator-owned.
- Automated re-calibration triggers — operator policy per §22.8.
- L2 probe judge thresholds (OQ-V-JUDGE-THRESHOLD) — validation POC scope.

---

═══════════════════════════════════════════════════
## Session Summary Block — EPSILON-CALIB-PROTO-1 Authored
═══════════════════════════════════════════════════

**Session:** 1.4 — Stage 3 protocol authorship (joint MEMIT + Validation Contract Architect)
**Status:** Draft (design-complete; gated on Stage 1 PASS + Stage 2 outputs before execution)

### Decisions made

- Stage 3 protocol formally named **EPSILON-CALIB-PROTO-1**. Ten components: cell cut, probe-set authorship, ε measurement, probe-set versioning, BUCKET boundary derivation, M-threshold derivation, ratification artifact shape, kill criteria, open questions, non-goals.
- **Transform-class cut chosen:** primary by transform class (5: RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT — fixed by §22.4), secondary by importance tier (3: CORE, SUPPORTING, INCIDENTAL — mirrors §8.9 / §9.4 cascade), tertiary by relation family (5; conditional on family-deviation trigger ε(family-pure) / ε(family-balanced) ∉ [0.8, 1.25]). Default cell count 15; tertiary expansion up to 75.
- **Rejected sub-cuts:** edit volume (conflates with `S_ceiling`), probe sub-type (scoring axis, not transform axis).
- **Probe-set authorship rule:** TGA authors individual probe templates per §21.3 (unchanged). Probe-set *version* mint requires `PROBE_SET_RATIFICATION` ceremony with joint MEMIT + Validation attestation in the IC-SCOPE-AUTH-1 envelope. Single-domain mint authority rejected — would let either side break the other's contract.
- **Per-patch fidelity scoring rule:** scalar from bound probe's judgment method (binary {0,1} for exact_substring; [0,1] for structured_field_match and judge_model_classification). Mixing methods within a cell permitted; mean across bound probes when multiple.
- **Replication:** ≥ 3 replicates per patch per pre/post phase (5 strongly preferred). Patch order randomized within each replicate; seed logged. Fresh anchor between replicates — no inherited drift (mirrors MEMIT-DRIFT-PROTO-1 §5 SBC hygiene).
- **Cell ε derivation:** p95 of per-patch fidelity deltas across the cell. Mean, p50, p99 reported; p99 is tail-watch only.
- **Cell validity gate:** ≥ 200 valid patch contributions, replicate stddev < 0.15, patch-position effect ≤ ε. Failure ships cell as `calibration_state: UNCALIBRATED`.
- **BUCKET derivation paths:** Path A (quantile-default, operator-free) is the default; Path B (operator-declared) is the override route. Both terminate in `CALIBRATION_RATIFICATION`. GS7 0.33/0.66 retained as Path A starting points for `attention_weight → declared_importance`.
- **M-threshold canonical derivation:** `M_advisory = floor(0.5 × Δfidelity_max / ε)`, `M_operational = floor(1.0 × Δfidelity_max / ε)`, `M_hard = floor(2.0 × Δfidelity_max / ε)`. Multipliers protocol-proposed; ratification at calibration packet submission.
- **Hysteresis constraint:** `M_hard ≥ 2 × M_advisory`. Collapse triggers `M_HYSTERESIS_COLLAPSED` flag, operator policy applies. Not a kill.
- **Probe-set versioning governance:** three-layer model — strict epoch isolation (mandatory floor), `PROBE_SET_RATIFICATION` ceremony (governance), `epsilon_history` audit overlay. ε values comparable only within a single probe-set epoch.
- **Independence from `S_ceiling`:** M and `S_ceiling` are conjunction-bound, not interchangeable. Migration batches must satisfy both.

### Constraints established

- This protocol consumes (does not author) `architecture_profile.json` (PF-6), `S_ceiling` (SBC), probe-set v1 corpus, Reference Patch Corpus, TGA Health Score record. All five must be content-hash-verified at Step 0 cell admission.
- `PROBE_SET_RATIFICATION` is a new ceremony type proposed by this protocol. IC-SCOPE-AUTH-1 envelope addition is a Warden-domain concern carried as OQ-W-PROBE-MINT — does not block this protocol's authorship; does block production probe-set version increments.
- ε is a calibration-time aggregate, never a runtime evaluation. Runtime L2 probes remain binary `{success, behavior_fail}` per §21.5. ε never appears in `write_outcome`. (T-EPSILON-1 closure.)
- Per-class ε (§22) and per-probe judge thresholds (§21.4 / OQ-V-JUDGE-THRESHOLD) are different layers with different runtime touchpoints. ε does not resolve OQ-V-JUDGE-THRESHOLD. (T-EPSILON-2 closure.)
- Stage 3 cannot open execution until Stage 2 outputs (`S_ceiling`, drift thresholds) are committed. Stage 1 PASS verdict is a precondition (carried from MEMIT-COMPAT-PROTO-1 §6 KILL aggregation rules).
- Protocol-proposed values (M multipliers, BUCKET starting quantiles, replication count floor of 3, validity-gate stddev threshold 0.15) are flagged for ratification at calibration packet submission — not spec-fixed.

### Open questions deferred

- **OQ-W-PROBE-MINT** — `PROBE_SET_RATIFICATION` ceremony type placement under IC-SCOPE-AUTH-1. Warden domain review needed before production deployment of probe-set increments. (T-EPSILON-3 partial residual.)
- **OQ-W-MULT** — M multipliers (0.5 / 1.0 / 2.0) operator-tunable at ratification time.
- **OQ-W-CRITICAL-CARRY** — M_hard alignment with N_critical (MEMIT-DRIFT-PROTO-1 carry-forward) — operator policy at packet level.
- **OQ-W-CALIB-CADENCE** — Re-calibration cadence after `probe_set_version` increment; 30-day default SLO suggested, operator-owned per §22.8.
- **OQ-V-JUDGE-THRESHOLD** — Per-probe judge threshold calibration (§21 carry-forward) — NOT resolved by this protocol; remains scoped to validation POC.

### Cross-domain tensions surfaced

- **T-EPSILON-1: Continuous ε vs. Binary L2 Outcome** (MEMIT vs. Validation) — ✅ Resolved. ε is calibration-time aggregate; runtime probe outcomes remain binary per §21.5. ε informs threshold authorship; never appears in `write_outcome`.
- **T-EPSILON-2: Per-Class ε vs. Per-Probe Judge Threshold** (MEMIT vs. Validation) — ✅ Resolved. Different layers, different runtime touchpoints. ε does not resolve OQ-V-JUDGE-THRESHOLD.
- **T-EPSILON-3: Probe-Set Version Mint Authority** (Validation vs. MEMIT — improvised) — 🔶 Partially resolved. Joint-attestation `PROBE_SET_RATIFICATION` ceremony specified; IC-SCOPE-AUTH-1 envelope mechanics carried forward as OQ-W-PROBE-MINT for Warden review.
- **T-EPSILON-4: M-Threshold vs. Drift Sub-Batch Ceiling** (MEMIT-internal Stage 2 vs. Stage 3) — ✅ Resolved. Independent constraints on different axes (patch size vs. per-class transform count); migration batches satisfy both via conjunction.

### Pre-mapped tension coverage

- **Pre-T2 (Write Volume vs. Edit Locality)** — Touched by M-threshold derivation. Primary resolution path (per-batch edge ceiling, per-session write budget) remains in MEMIT-DRIFT-PROTO-1's `S_ceiling` and drift thresholds. Graph Data Architect's Pre-T2 voice is engaged in MEMIT-DRIFT-PROTO-1; deferred from this protocol with stated reason. M values operate at a complementary granularity (per-class per-batch).
- **Pre-T6 (Genesis Completeness vs. Genesis Lock-in)** — Touched by probe-set v1 Genesis anchoring. Probe-set v1 follows existing Pre-T6 minimal-viable-Genesis resolution. Subsequent probe-set versions enter via `PROBE_SET_RATIFICATION` (write-pipeline path), not Genesis modification. Graph Data Architect and Warden positions inherited from prior sessions; no new engagement required on this protocol.

### Artifacts the protocol produces (when executed)

- Per-cell calibration runs with replicate logs and patch-position seed records
- `epsilon_calibration_report` v1 per §7.1 (Deliverable 6 of POC scope)
- BUCKET boundary tables per §5 (Deliverable 7)
- Compaction tolerance evidence and derived M table per §6 (Deliverable 8)
- `CALIBRATION_RATIFICATION` submission packet bundling all of the above with signing CAK metadata (Deliverable 9 — final POC submission to §22.5 ceremony path)

### Protocols defined this session

- **EPSILON-CALIB-PROTO-1** — full protocol covering cell stratification, ε measurement, probe-set versioning governance, BUCKET boundary derivation, M-threshold derivation, ratification artifact shape, kill criteria.
- **`PROBE_SET_RATIFICATION` ceremony type (proposed)** — joint MEMIT + Validation attestation under IC-SCOPE-AUTH-1; placement subject to Warden review (OQ-W-PROBE-MINT).

### Next session candidates

- **Warden-domain session:** Review OQ-W-PROBE-MINT — `PROBE_SET_RATIFICATION` ceremony envelope mechanics, joint-attestation field structure under IC-SCOPE-AUTH-1.
- **Validation POC session:** Address OQ-V-JUDGE-THRESHOLD per-probe judge threshold calibration — operates on probe-set v1 already authored by this Stage.
- **Stage 4 — Consolidation:** Bundle Deliverables 1–8 into the `CALIBRATION_RATIFICATION` submission packet (Deliverable 9) and author the per-deployment re-calibration playbook (Deliverable 10). Per write-engine-poc-scope §6, Stage 4 is sequencing and packaging — no new protocol authorship.

═══════════════════════════════════════════════════
*EPSILON-CALIB-PROTO-1 — design-complete, awaiting Stage 1 PASS + Stage 2 outputs to execute*
*Specialist provenance: MEMIT Specialist (primary, write-engine domain) + Validation Contract Architect (primary, probe-set and binary-outcome contract). Graph Data Architect and Warden domains touched at Pre-T2 / Pre-T6 / OQ-W-PROBE-MINT — engagement deferred with stated reason.*
═══════════════════════════════════════════════════
