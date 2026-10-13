## 22. `larql_fidelity_calibration` Protocol

### 22.1 Purpose

Several T13 thresholds and IC-MANIFEST-1 bucket-map boundaries depend on a per-transform-class fidelity coefficient ε that cannot be set a priori. The `larql_fidelity_calibration` protocol (D-GS8-A, v2 GS8) defines the measurement procedure that produces an `epsilon_calibration_report` artifact consumable by the genesis-seal update ceremony. Protocol structure is ratified; numeric ε outputs are implementation-phase per OQ-W1 / OQ-W-CALIB-1 / GAP-1 / GAP-2 / GAP-48.

### 22.2 Preconditions

- At least one full `current_larql_version` increment has occurred, producing a non-empty migration manifest with at least one RENAME, one BUCKET, and one COMPUTE transform type populated.
- A reference patch corpus representative of production agent output exists (minimum 200 patches per transform class per version hop measured).

### 22.3 Procedure (per transform class, per version hop)

1. Select reference patches at `source_version`. Compile through MEMIT to produce baseline parametric encoding; record per-patch retrieval fidelity via canonical probe set (probe set defined at Genesis; versioning per OQ-W-PROBE-VERSION / GAP-48).
2. Apply migration manifest translation to the same reference patches. Compile the translated patches through MEMIT. Record per-patch retrieval fidelity via the same probe set.
3. Compute per-patch fidelity delta. Aggregate mean, p50, p95, p99 across the class-hop combination.
4. The class-hop ε value = p95 of fidelity delta. (p95 chosen over mean to bound worst-case compaction batches.)

### 22.4 Output Artifact — `epsilon_calibration_report`

Required fields:
- Per transform class (RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT): per-hop ε values.
- Corpus statistics (patch count per class-hop).
- `calibrated_against_probe_set_version` field — records the canonical probe-set version the calibration was run against (D-GS8-A / GAP-48 resolution). Historical ε values are comparable only within a single probe-set-version epoch.
- Compaction tolerance assumption used for M derivation (provisional default: `Δfidelity_max = 0.05`; ratified at calibration time).
- Timestamp and signing CAK.

### 22.5 Ratification Path

The calibration artifact is submitted via a `CALIBRATION_RATIFICATION` ceremony (ceremony_type per §20 / IC-SCOPE-AUTH-1). On acceptance, Tier 1 `genesis-seal.json` fields `larql_epsilon_table`, `compaction_tolerance`, and derived M values are populated, and the provisional flags on T13 thresholds and IC-MANIFEST-1 `bucket_map` are cleared in the spec's next integrated iteration.

### 22.6 Bucket Boundary Determination (D-GS8-B)

Bucket boundaries for any BUCKET transform class are calibrated by the same protocol, producing a per-transform-class optimal boundary table rather than a fixed global default. The GS7 illustrative values (0.33 / 0.66) are retained as provisional illustrative defaults for the `attention_weight → declared_importance` bucket only; other BUCKET transforms ratify their own boundaries at calibration time.

### 22.7 Interface Contract Delta

`IC-MANIFEST-1` `bucket_map` field description:
- Boundaries remain PROVISIONAL until a `CALIBRATION_RATIFICATION` ceremony is accepted for the transform class the bucket serves.
- Manifest entries authored prior to first calibration carry `calibration_state: UNCALIBRATED` and flag accordingly in dry-run reports (non-blocking; advisory only until first calibration lands).

### 22.8 Non-Goals

§22 does not specify:
- Numeric ε values, M values, or bucket boundaries — implementation-phase per OQ-W-CALIB-1.
- Automated re-calibration triggers — operator-owned cadence.
- Cross-model ε transfer — a calibration is per-deployment, not portable.

---

