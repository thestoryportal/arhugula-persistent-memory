# COMPACTION-PROBE-CALIB-PROTO-1 — Compaction Probe Sampling Rate Calibration Protocol

*Workstream: Empirical POC Scoping (post-v1.2 sealed spec)*
*Session: 1.5 — Compaction probe calibration authorship — addresses OQ-OC3*
*Primary skill: validation-contract-architect (joint touch: memit-specialist for compaction-side semantics)*
*Status: design-complete; gated on MEMIT-COMPAT-PROTO-1 PASS verdict and MEMIT-DRIFT-PROTO-1 outputs (`S_ceiling`, drift thresholds) before execution*

The protocol calibrates the §11.14 SUPPORTING and INCIDENTAL sampling rates and floors against a real model on a controlled corpus, producing values that populate the `compaction_probe_sampling_config` block in Tier 1 config and the IC-OC-PROBE struct fields. It also tests whether the 95% / 80% abort thresholds survive empirical scrutiny.

The CORE 1.0 threshold and 100% sampling rate are **not in scope** — they are spec-fixed by C-OC3 and not provisional.

This protocol consumes — does not author — three artifacts:
- `architecture_profile.json` (MEMIT-COMPAT-PROTO-1 PF-6)
- `S_ceiling` and drift thresholds (MEMIT-DRIFT-PROTO-1)
- Probe-set v1 corpus with frozen template hashes (MEMIT-COMPAT-PROTO-1 + Validation collaboration)

It produces — does not consume — the §11.14 sampling rate / floor / threshold values that feed Tier 1 config and IC-OC-PROBE.

---

## 1. Ground-Truth Oracle — Establishing What "Compaction Caused Regression" Means

### 1.1 The core problem

Sampling-based detection has two natural ways to be wrong:
- **False negative (missed regression):** the population contains regressions, the sample misses them, compaction proceeds, knowledge graph silently degrades. This is the dangerous direction.
- **False positive (spurious abort):** the population is clean, sampling noise produces apparent failures, compaction aborts, expensive work is wasted and re-attempted.

To measure either, the protocol must know the **true** post-compaction regression status of every edge in a calibration corpus — the ground truth against which sampling-based decisions are scored. This is the oracle.

### 1.2 Oracle construction — three-stage qualifying probe

```
[ Calibration corpus admission ]
        ↓
[ Stage A: pre-compaction stability filter ]
  Each candidate edge probed N=10 times pre-compaction.
  Edge admitted iff pass rate = 10/10 across all 10 runs.
  Stochastically passing edges (e.g. 7/10) are EXCLUDED from corpus —
  their post-compaction failures cannot be attributed to compaction.
        ↓
[ Stage B: compaction event ]
  Standard production compaction run (full MEMIT re-compile, 2PC).
  Compaction is the same procedure as production — no calibration-only paths.
        ↓
[ Stage C: post-compaction full-population probe ]
  Every admitted edge probed M=10 times post-compaction.
  Edge labelled REGRESSED iff post-compaction pass rate ≤ 5/10.
  Edge labelled SURVIVED iff post-compaction pass rate ≥ 9/10.
  Edges in 6/10–8/10 band labelled UNCERTAIN — excluded from the
  oracle's regression label, reported as a separate diagnostic
  (uncertain rate is a calibration health signal, not a per-edge label).
```

Stage A's 10/10 stability filter eliminates probe noise from masquerading as compaction-caused regression. Stage C's two-band labelling separates "cleanly regressed" (action-relevant) from "noisily ambiguous" (excluded from rate calc, but counted as a corpus health signal — high uncertain rate signals probe instability and invalidates the calibration run).

### 1.3 Why probe stability matters

If the calibration corpus admits edges that pass pre-compaction probes only 7/10 times, then a 6/10 post-compaction probe rate looks like regression but is actually within pre-existing probe noise. This contaminates the regression rate and inflates measured false-negative rates — calibration converges on rates that are conservative for the wrong reason.

Stage A's strict filter is non-negotiable for valid calibration. The cost is corpus shrinkage: empirically, ~70–85% of candidate edges survive 10/10 stability filtering on a healthy MEMIT-compatible model. The protocol expects ~30% of candidate edges to be filtered out at Stage A; if more than 50% are filtered, the model's probe stability itself is suspect and a `PROBE_INSTABILITY_DETECTED` flag is raised — calibration halts, kicks back to MEMIT-COMPAT-PROTO-1 OP-1 envelope review.

### 1.4 Corpus size for 1% resolution

To measure pass-rate differences at 1% resolution within a stratum requires ≥100 cleanly-labelled edges in that stratum (and meaningfully more for confidence intervals at the 1% level — Clopper-Pearson 95% CI half-width on n=100, p=0.95 is roughly ±4.3%; on n=500 it's roughly ±2%; on n=1000 it's roughly ±1.4%).

**Stratification cells:** 3 importance tiers (CORE, SUPPORTING, INCIDENTAL) × 5 relation families (D6) = 15 cells.

**Corpus size targets (post-Stage A admission):**

| Cell density | Edges per cell | Total | 95% CI half-width on p=0.95 |
|---|---|---|---|
| Minimum (1% gross resolution) | 100 | 1,500 | ±4.3% |
| Recommended (sub-1% on key cells) | 500 | 7,500 | ±2.0% |
| Aggressive (publication-grade) | 1,000 | 15,000 | ±1.4% |

**Recommendation:** 500 edges per cell post-Stage A → 7,500-edge realistic-mix corpus. Adversarial corpus (§3.3) is sized at 100 edges per affected cell — adversarial corpora are designed for stress-testing specific failure topologies, not high-resolution rate measurement.

To land 500 admitted edges per cell, the candidate corpus must be sized with ~30% over-provision: ~10,000–11,000 candidate edges submitted to Stage A.

### 1.5 What the oracle does not establish

- **Does not establish** whether SUPPORTING or INCIDENTAL probes are equally informative as CORE probes. That is a probe-design question, scoped to the L2 Probe Family work in §21 and out of scope here.
- **Does not establish** whether the calibration is portable across model architectures. Calibrations are per-deployment per §22.8; this protocol inherits that constraint.
- **Does not produce** ε values or M thresholds — those are EPSILON-CALIB-PROTO-1's job. This protocol produces sampling rates and floors only.

---

## 2. Sampling Sweep — Rate-vs-Recall under Realistic and Adversarial Mixes

### 2.1 The decision function under test

For each stratum (tier × family), the operational abort decision at compaction time is:

```
sample = uniform_random_subset(stratum_population, k = max(rate × |stratum|, floor))
sample_pass_rate = passed(sample) / |sample|
decide(stratum) = PROCEED  if sample_pass_rate ≥ threshold
decide(stratum) = ABORT    otherwise
overall_decision = ABORT if any stratum aborts; else PROCEED
```

The calibration measures, for each (rate, floor, threshold) configuration, the joint distribution of `decide()` against the oracle's true population pass rate.

### 2.2 Sweep axes

**Axis 1 — Sampling rate (per-tier, separate sweeps):**

| Tier | Sweep range | Step |
|---|---|---|
| SUPPORTING | 5%, 10%, 15%, 20%, 25%, 33%, 50%, 75%, 100% | 9 points |
| INCIDENTAL | 3%, 5%, 8%, 10%, 15%, 20%, 33%, 50%, 100% | 9 points |

100% is the oracle reference; everything below it carries some miss probability.

**Axis 2 — Floor:**

| Tier | Floor sweep | Step |
|---|---|---|
| SUPPORTING | 5, 10, 15, 20, 25, 30, 40, 50 | 8 points |
| INCIDENTAL | 3, 5, 8, 10, 15, 20, 30 | 7 points |

Floor sweep is meaningful only for stratum sizes where the floor is binding (i.e., rate × |stratum| < floor). Per-cell evaluation conditions on stratum size — see §3 floor validation.

**Axis 3 — Threshold (sensitivity sweep):**

| Tier | Threshold sweep |
|---|---|
| SUPPORTING | 0.90, 0.92, 0.95, 0.97, 0.99 |
| INCIDENTAL | 0.70, 0.75, 0.80, 0.85, 0.90 |

The 95% / 80% spec values sit in the middle of each range.

**Axis 4 — Population pass rate (synthetic injection):**

To measure `decide()` behaviour against known population truths, the protocol takes the labelled corpus from §1 and synthetically perturbs the population pass rate by re-labelling a controlled fraction of edges as REGRESSED. Range:

| Population pass rate | Purpose |
|---|---|
| 1.00 | Baseline — no regressions; measures false-positive abort rate |
| 0.99, 0.97, 0.95 | Boundary region for SUPPORTING — measures discrimination near threshold |
| 0.90, 0.85, 0.80 | Boundary region for INCIDENTAL — measures discrimination near threshold |
| 0.70, 0.50 | Catastrophic regime — should always abort |

### 2.3 Realistic-mix corpus

Regressions distributed across the corpus with two independent sources:
- **Empirical-emulating distribution:** regression probability for each edge is set proportional to that edge's pre-compaction probe stability margin (edges that passed 10/10 with high judge confidence regress less; edges that passed 10/10 marginally regress more). Probability calibrated such that overall corpus regression rate matches observed compaction noise from MEMIT-COMPAT-PROTO-1 baseline runs.
- **Random uniform overlay:** a small fixed fraction (1–2%) of edges across the corpus are labelled REGRESSED uniformly at random, regardless of stability margin. This represents the "compaction occasionally breaks something for no obvious reason" failure mode.

The realistic-mix corpus is the primary measurement substrate. Recall and false-negative rate curves for §6 deliverables are produced from this corpus.

### 2.4 Adversarial corpus — clustered regression mode

Stratified random sampling within a cell is provably effective against uniform regression distribution. Its known failure mode is **regression clustering** — when regressions concentrate in a small structural region of the cell, sampling miss probability rises sharply.

Adversarial corpus design — three deliberate clustering modes:

| Mode | Clustering pattern | Tests |
|---|---|---|
| **Family-clustered** | All regressions land in one relation family within a tier (e.g., all SUPPORTING regressions are in the Knowledge family) | Whether tertiary stratification (per-family sub-sampling) is necessary |
| **Neighborhood-clustered** | All regressions land in one polysemantic cluster (entities sharing dense embedding-space neighborhood) | Whether intra-stratum random sampling protects against locality-correlated failures |
| **Recency-clustered** | All regressions land in edges written most recently before compaction (i.e., last 10% of edits to anchor) | Whether recency-aware sampling is required, or random uniform suffices |

Each adversarial corpus is sized at 100 edges per affected cell (smaller than realistic-mix; clustering experiments are stress tests, not high-resolution rate measurements).

Per-mode regression injection rate: 5% of stratum population, all concentrated in the cluster.

Sweep rates and floors against each adversarial corpus identical to §2.2. Comparison rule:

```
miss_rate(adversarial, mode) / miss_rate(realistic, equivalent population pass rate)
  ≤ 1.5 → cluster-mode tolerable; current sampling design protects
  ∈ [1.5, 3.0] → cluster-mode marginal; flag for tertiary stratification
  > 3.0 → cluster-mode dangerous; tertiary stratification mandatory or
          rate increase required
```

The 1.5× and 3.0× bands are protocol-proposed; ratification at calibration packet submission.

### 2.5 Replication and noise control

- **Per-configuration runs:** 500 independent random samplings of the corpus per (rate, floor, threshold, population pass rate) cell. Sufficient to compute miss-rate at 0.2% resolution (1/500).
- **Compaction event:** the compaction itself (§1.2 Stage B) runs once per corpus; replicated random sampling operates over the post-compaction labels. The compaction event is not re-replicated — that would be MEMIT-DRIFT-PROTO-1's job, not this protocol's.
- **Independent corpus replicates:** 3 independent realistic-mix corpora are constructed from disjoint candidate edge pools, each running through the full compaction → label cycle. This separates within-corpus sampling noise from across-corpus generalization variance. Cross-corpus disagreement > 5% on key rate-vs-recall points triggers `CALIBRATION_NON_REPRODUCIBLE` flag.

### 2.6 Output — rate-vs-recall curves

For each tier, two plot families:

**Family 1 — Realistic-mix discrimination curves**
For each (population pass rate, threshold) pair, plot:
- x-axis: sampling rate
- y-axis: P(correct decision) decomposed into:
  - P(PROCEED | population should proceed)  ← 1 − false-positive abort rate
  - P(ABORT  | population should abort)     ← 1 − false-negative miss rate

**Family 2 — Adversarial-vs-realistic miss rate ratio**
For each clustering mode, plot:
- x-axis: sampling rate
- y-axis: miss_rate(adversarial) / miss_rate(realistic)
- Marker at the 1.5× and 3.0× band boundaries

Acceptable miss rate ceiling is set at 5% in §4 (false-negative rate ≤ 0.05 at the operational threshold). The smallest sampling rate at which both Family 1 and Family 2 satisfy the ceiling becomes the recommended rate for that tier.

---

## 3. Floor Validation — Small-Stratum Behaviour

### 3.1 Why floors exist

For small strata (e.g., a SUPPORTING/Constraint cell with only 18 edges in the compacted overlay), 20% sampling = 3.6 edges. Below ~5 samples, the sample pass rate cannot meaningfully discriminate 95% from 80% — both are within sampling noise. The floor enforces a minimum sample size when rate-based sampling would fall below a discrimination threshold.

The current spec floors (5 for SUPPORTING, 3 for INCIDENTAL) are placeholder values that the calibration must validate.

### 3.2 Floor binding zones

The floor is binding when `floor > rate × |stratum|`. Define the binding zone for each (rate, floor) pair as the range of stratum sizes where the floor is the active sample-size determinant.

For SUPPORTING at rate 20%, floor 5: binding zone is `|stratum| ≤ 25`.
For SUPPORTING at rate 20%, floor 30: binding zone is `|stratum| ≤ 150`.
For INCIDENTAL at rate 10%, floor 3: binding zone is `|stratum| ≤ 30`.
For INCIDENTAL at rate 10%, floor 15: binding zone is `|stratum| ≤ 150`.

Real-world strata frequently land in binding zones. Production traffic concentration in a few high-volume relation families means rare-family cells routinely have stratum sizes in the 10–100 range.

### 3.3 Floor sweep design

For each (tier, floor) candidate value, sweep:
- Stratum size: 8, 12, 16, 20, 25, 30, 50, 75, 100 edges
- Population pass rate: 1.00, 0.95, 0.90, 0.80, 0.70 (per tier-relevant range)
- Single regression case: |stratum| − 1 SURVIVED, 1 REGRESSED (worst-case detection)

For each (floor, stratum size, population pass rate), compute via Monte Carlo (10,000 samplings):
- P(correct PROCEED | should proceed)
- P(correct ABORT | should abort)
- P(detect | exactly 1 regression in stratum) — the worst-case detection rate

### 3.4 Floor-acceptance rule

A floor is acceptable for a tier if, at the corresponding rate-tier threshold:
- P(false-negative abort) ≤ 5% across all stratum sizes ≥ 2 × floor
- Worst-case single-regression detection rate ≥ 50% across all binding-zone stratum sizes
- P(false-positive abort | true rate = threshold + 0.02) ≤ 10%

The 50% single-regression detection floor is deliberately permissive — at floor sample sizes, perfect detection is mathematically infeasible. The bar is "meaningful discrimination," not "perfect coverage." Operators who require higher detection on small strata can either raise the floor or escalate the stratum to CORE (which guarantees 100% sampling).

### 3.5 Expected floor outcome (protocol-proposed pre-execution estimates)

The candidate values pre-protocol:

| Tier | Spec floor | Power-derived target | Protocol-proposed candidate |
|---|---|---|---|
| SUPPORTING | 5 | ~30 (95% vs 80% discrimination at α=0.05, β=0.20) | **Sweep recommends 30; final value set at calibration** |
| INCIDENTAL | 3 | ~18 (80% vs 50% discrimination at α=0.05, β=0.20) | **Sweep recommends 15; final value set at calibration** |

The calibration sweep validates or replaces these candidates. If the empirical sweep produces a floor recommendation outside ±20% of the candidate, the protocol records `FLOOR_CANDIDATE_DIVERGED` for operator review — divergence may indicate either probe-noise issues (return to §1.3 instability check) or genuine deployment-specific variance.

---

## 4. Abort-Threshold Sensitivity — Does 95% / 80% Survive?

### 4.1 The threshold calibration question

The 95% / 80% thresholds are inherited from spec §11.14 and are provisional. The calibration must answer:

1. At empirically measured optimal sampling rates, do thresholds at 95% / 80% produce acceptable false-negative rates (≤ 5%) and acceptable false-positive rates (≤ 10%)?
2. If not, what threshold value satisfies both bounds simultaneously?
3. Do thresholds need to be tier × family stratified, or are tier-only thresholds sufficient?

### 4.2 Sensitivity sweep

Already enumerated as Axis 3 in §2.2. Each (rate, floor, threshold) cell from §2.2 produces both false-positive and false-negative rates from the realistic-mix corpus.

For each tier, find the threshold T* that minimizes:

```
loss(T) = w_FN × P(false_negative | T) + w_FP × P(false_positive | T)
```

with `w_FN = 4` and `w_FP = 1` — false negatives are the dangerous direction (silent knowledge corruption) and weighted four times more heavily than false positives (wasted compaction work). The 4:1 weighting is protocol-proposed; ratification at calibration packet submission.

If the optimal T* differs from the spec threshold by more than ±0.03 (e.g., SUPPORTING comes out at 0.92 or 0.98 rather than 0.95), the protocol flags `THRESHOLD_DIVERGED` and the calibration packet carries both the spec value and the empirical value — operator decides which to ratify.

### 4.3 Family-stratified threshold question

If adversarial-corpus testing in §2.4 returns family-clustering sensitivity > 1.5× for any (tier, family) pair, the recommendation may be to apply a tighter threshold for that specific family rather than tightening the entire tier. The protocol records family-by-family loss curves to support this decision, but the default recommendation is tier-level thresholds — family stratification is a complexity that should be paid for only when measurement demands it.

### 4.4 Pre-execution candidate dispositions

The empirical work will produce final values. Pre-execution, the protocol's expected outcomes:

- **SUPPORTING 95% threshold:** likely survives. The 95% level is far enough from the realistic measured pass rate (expected: 0.97–0.99 at well-tuned compaction) that discrimination is achievable at moderate sample sizes.
- **INCIDENTAL 80% threshold:** at higher risk. The 80% level is closer to the typical pass rate (expected: 0.85–0.92), and discrimination requires larger samples. Calibration may recommend tightening to 0.85.
- **CORE 1.0 (out of scope, spec-fixed by C-OC3):** untouched.

These are pre-execution conjectures, not commitments. The empirical sweep may invert them.

---

## 5. CompactionProbeReport Field Population

### 5.1 Spec contract from IC-OC-PROBE (current state)

IC-OC-PROBE specifies the report struct must carry:
- Stratified sampling outcomes (CORE / SUPPORTING / INCIDENTAL)
- Abort thresholds applied
- Random seed (reproducibility)
- CORE failure IDs individually listed
- SUPPORTING / INCIDENTAL failure IDs individually listed iff ≤10, summary-logged otherwise

This protocol extends — does not contradict — that contract.

### 5.2 Field population specification

The CompactionProbeReport struct is grouped into five sections.

**Section A — Identity & Reproducibility**

| Field | Type | Source | Purpose |
|---|---|---|---|
| `report_id` | UUID | TC-issued at probe start | Ledger primary key |
| `compaction_event_id` | UUID | TC compaction state | Foreign key to compaction event chain |
| `compaction_anchor_event_id` | UUID | from `drift_state.anchor_event_id` | Ties report to the anchor whose successor compaction is being verified |
| `random_seed` | int64 | sampling-time generated | Reproducibility of stratified sample selection |
| `probe_set_version` | string | from §22 / EPSILON-CALIB | Semantic compatibility of probe authorship |
| `epsilon_calibration_id` | UUID | from §22 calibration packet | Which ε regime's thresholds applied |
| `sampling_calibration_id` | UUID | from this protocol's output | Which OQ-OC3 calibration epoch produced the rates / floors used |
| `prober_agent_id` | string | TC-recorded | Which Behavioral Probe Agent ran the probes (touches GAP-15) |
| `judge_model_ids` | list[string] | per-probe-binding | Judge model(s) used in `judge_model_classification` mode |
| `start_timestamp`, `end_timestamp` | ISO-8601 | TC-recorded | Wall-clock span |

**Section B — Per-Stratum Outcome (one entry per stratum cell)**

| Field | Type | Purpose |
|---|---|---|
| `tier` | enum {CORE, SUPPORTING, INCIDENTAL} | Importance tier |
| `relation_family` | enum {Structural, Knowledge, Constraint, Taxonomy, Namespace} \| null | Family stratification (null when family-stratified config disabled) |
| `population_size` | int | Total edges in this stratum in compacted overlay |
| `sample_size` | int | Edges actually probed |
| `floor_engaged` | bool | True iff configured floor was the active sample-size determinant |
| `passed_count` | int | Probes returning success per §21.4 judgment |
| `failed_count` | int | Probes returning behavior_fail per §21.4 judgment |
| `infrastructure_failed_count` | int | Probes that errored — see Section D |
| `effective_sample_size` | int | `sample_size − infrastructure_failed_count` (denominator for pass rate) |
| `pass_rate` | float [0, 1] | `passed_count / effective_sample_size` |
| `threshold_applied` | float [0, 1] | Configured threshold for this stratum |
| `decision` | enum {PROCEED, ABORT} | Stratum-level decision |
| `failure_ids_listing_mode` | enum {INDIVIDUAL, SUMMARY, MIXED} | Per IC-OC-PROBE rule |
| `failure_ids` | list[edge_id] | Individual mode (always for CORE; SUPPORTING / INCIDENTAL when failure count ≤ 10) |
| `failure_summary` | object \| null | Summary mode — breakdown by sub-attributes (relation type, schema version, recency band) when individual listing suppressed |
| `failure_id_sidecar_ref` | URI \| null | Sealed sidecar file reference holding full failure ID list when suppressed in main payload (resolves audit-completeness vs. ledger-payload-size tension) |

**Section C — Aggregate Decision**

| Field | Type | Purpose |
|---|---|---|
| `overall_decision` | enum {PROCEED, ABORT} | True iff every stratum decided PROCEED |
| `aborting_strata` | list[stratum_key] | Which strata's failures triggered abort (empty if overall decision is PROCEED) |
| `report_classification` | enum {COMPACTION_PROCEEDED, COMPACTION_ABORTED, COMPACTION_PROBE_FAILED} | Determines which Ledger event type is emitted — see §6 separation rules |

**Section D — Infrastructure Failure Accounting**

| Field | Type | Purpose |
|---|---|---|
| `total_probes_attempted` | int | Sum of sample_size across all strata |
| `total_infrastructure_failures` | int | Sum of infrastructure_failed_count across all strata |
| `infrastructure_failure_rate` | float [0, 1] | `total_infrastructure_failures / total_probes_attempted` |
| `infrastructure_failure_threshold` | float [0, 1] | Configured threshold above which the entire run reclassifies as COMPACTION_PROBE_FAILED |
| `infrastructure_failure_breakdown` | object | Counts by failure category (timeout / judge_unreachable / sandbox_error / token_budget_exceeded / other) |
| `infrastructure_failure_bias_check` | object | Per §6.4 — flags whether infra failures are uniform across tiers/families or systematically biased |

**Section E — Calibration Provenance & Audit Trail**

| Field | Type | Purpose |
|---|---|---|
| `sampling_config_snapshot` | object | The (rate, floor, threshold) values applied per tier, captured at probe start (immutable) |
| `tier_1_config_hash` | SHA-256 | Hash of the active Tier 1 config block governing sampling |
| `meta_validator_health_at_probe_time` | float \| NOT_COMPUTED | Latest Meta-Validator Health Score per IC-V-TGA2 (audit cross-linkage) |
| `tga_health_at_probe_time` | float \| NOT_COMPUTED | Latest TGA Health Score (audit cross-linkage) |
| `notes` | string \| null | Operator-extensible audit notes; default null |

### 5.3 Audit-completeness reconciliation with C-META1

C-META1 forbids aggregate-only Meta-Validator audit reports. Compaction probe reports are **not** Meta-Validator runs, but they share the audit-completeness principle. The §11.14 spec language ("summary-logged unless ≤10 IDs") creates a tension: large-failure runs would have aggregate-only ledger entries.

**Resolution:** the `failure_id_sidecar_ref` field. When a stratum's failure list exceeds 10 IDs, the main ledger payload carries the summary; the full per-edge failure list is written to a sealed sidecar file (operator-signed, append-only, hash-anchored in the main ledger entry). This preserves ledger payload size discipline while keeping per-case data accessible for Warden post-hoc audit.

The sidecar is co-classified with the COMPACTION_ABORTED ledger entry — same retention schedule, same integrity anchor. The sidecar is not optional. Without it, Warden audit visibility on aborted compactions degrades to summaries-only — unacceptable per the C-META1 spirit even though the literal C-META1 scope is Meta-Validator.

### 5.4 What the report does NOT carry

Explicit non-fields (commonly proposed, deliberately rejected):

| Field | Why excluded |
|---|---|
| `proposed_remediation` | Probe report is descriptive, not prescriptive. Remediation is operator policy. |
| `compaction_retry_recommendation` | Same as above. Retry decisions live in TC, not in the probe report. |
| `judge_model_confidence_distribution` | Per-probe judge confidence is captured in §21 probe records, not duplicated here. |
| `historical_compaction_pass_rates` | Cross-event temporal data is the Ledger's job, not a single report's. |
| `epsilon_value_per_stratum` | ε is a calibration aggregate, never a runtime value (T-EPSILON-1, EPSILON-CALIB-PROTO-1). Including ε here would re-open T-EPSILON-1. |

### 5.5 Backward compatibility with IC-OC-PROBE

IC-OC-PROBE in v1.2 spec specifies struct fields at coarse granularity (sampling rates, abort thresholds, random seed, failure listing rule). The §5.2 specification adds fields without modifying any v1.2 fields. The report extension is a v1.3 contract amendment, not a breaking change. Existing v1.2 consumers reading the report receive a struct with all v1.2 fields populated identically; new fields are additive.

If the v1.2 IC-OC-PROBE consumers cannot tolerate unknown additional fields, the calibration packet ratification ceremony (parallel to §22.5) must include a Tier 1 config flag `compaction_report_schema_version` controlling field emission. Default to v1.3 (full population); operators can pin to v1.2 (subset) for a migration window. Carried as OQ-V-OC-REPORT-VER.

---

## 6. Separation from MEMIT Compatibility — COMPACTION_PROBE_FAILED vs COMPACTION_ABORTED

### 6.1 The two distinct failure modes

These two failure modes carry different operator implications:

| Event | What it means | What operator does |
|---|---|---|
| `COMPACTION_ABORTED` | Probes ran successfully; aggregate pass rates fell below abort thresholds | Investigate compaction itself — likely MEMIT compatibility regression, drift threshold miscalibration, or pathological edge population. Re-run requires fix. |
| `COMPACTION_PROBE_FAILED` | Probe infrastructure failed too many probes for the pass-rate measurement to be trustworthy | Investigate probe infrastructure — judge model availability, sandbox health, network. Compaction state is unknown — neither proven good nor proven bad. Re-run probe (not compaction). |

Conflating them is dangerous in both directions:
- If COMPACTION_PROBE_FAILED is logged as COMPACTION_ABORTED, operator wastes effort fixing MEMIT when probe infrastructure is the actual problem. Over time, operators become desensitized to "abort" events ("oh, that's just probe flakiness") — and miss the real ones.
- If COMPACTION_ABORTED is logged as COMPACTION_PROBE_FAILED, a real regression appears as a transient infrastructure issue. Operator re-runs probes (which may complete the second time but on a different sample, masking the original signal). Real regressions get re-classified as flaky tests.

### 6.2 The classification rule

**Inputs** (from §5.2 Section D):
- `total_probes_attempted` = N
- `total_infrastructure_failures` = F
- `infrastructure_failure_rate` = F / N
- `infrastructure_failure_threshold` = θ_infra (Tier 1 config; protocol-proposed candidate **0.05**)

**Classification:**

```
if infrastructure_failure_rate > θ_infra:
    report_classification = COMPACTION_PROBE_FAILED
    overall_decision = ABORT_INDETERMINATE
elif overall_decision == ABORT (per §5.2 Section C aggregation):
    report_classification = COMPACTION_ABORTED
else:
    report_classification = COMPACTION_PROCEEDED
```

Critically: when infrastructure_failure_rate exceeds threshold, the per-stratum pass-rate computation is *not* used to determine overall decision. Even if the (low-power) measured pass rates would otherwise produce PROCEED, the entire run is marked PROBE_FAILED — because we don't trust the measurement.

### 6.3 Threshold for θ_infra

A 5% infrastructure failure rate means 1 in 20 probes errored. At that level:
- Aggregate pass-rate measurements still have 95% of their intended sample size
- Statistical power is mildly degraded but not destroyed
- The operator can still distinguish "compaction broken" from "probe flaky"

A 10% threshold is the upper bound of tolerability; above 10%, the sample's effective size drops sharply. A 2% threshold is overly strict — judge model rate-limits and transient timeouts can briefly elevate failures above 2% without indicating systemic infrastructure breakdown.

**Protocol-proposed candidate:** θ_infra = 0.05 (5%). Calibration sweep includes θ_infra ∈ {0.02, 0.05, 0.08, 0.10} to verify.

### 6.4 Bias check — are infrastructure failures random?

A subtle hazard: if infrastructure failures correlate with edge difficulty (complex edges time out, simple edges complete), the surviving probe sample is biased toward easy edges. Pass rates measured on a biased sample overestimate the true population pass rate — false-negative aborts increase silently.

The bias check (§5.2 Section D `infrastructure_failure_bias_check` field) computes:

```
For each (tier, family) cell:
  expected_infra_failure_rate = total_infra_failures / total_probes
  observed_infra_failure_rate_in_cell = cell_infra_failures / cell_probes
  z_score = (observed − expected) / sqrt(expected × (1 − expected) / cell_probes)

  if any cell has |z_score| > 2.0:
    bias_check_flag = NON_UNIFORM
  else:
    bias_check_flag = UNIFORM
```

Bias result reported in the CompactionProbeReport. Two policy paths:

| Bias result | Threshold rule |
|---|---|
| UNIFORM | Standard θ_infra = 0.05 applies |
| NON_UNIFORM | Tighter θ_infra applies (protocol-proposed: 0.02). Above this, classify as COMPACTION_PROBE_FAILED rather than risk silently biased pass rates. |

The bias-aware threshold is protocol-proposed; ratification at calibration packet submission. Carried as OQ-V-OC-INFRA-BIAS.

### 6.5 The contract with MEMIT-COMPAT-PROTO-1

MEMIT-COMPAT-PROTO-1 produces a PASS / D20-DRIFT / D20-FAIL verdict on baseline MEMIT compatibility for the deployment. Its concerns are:
- Can MEMIT execute writes on this model architecture at all?
- Does the architecture profile match the compatibility envelope?
- Are baseline operating points within tolerance?

These concerns are **upstream of compaction-time probing**. MEMIT-COMPAT-PROTO-1 KILL conditions short-circuit Stage 2 and Stage 3 protocols, including this one. If MEMIT-COMPAT-PROTO-1 returns D20-FAIL, this protocol does not execute — there is no point calibrating compaction probe rates on a model that fails baseline compatibility.

The COMPACTION_PROBE_FAILED event class is **not** an indicator that MEMIT compatibility regressed. It is an indicator that the probe machinery (judge models, sandbox, scheduler) is failing. These two diagnostic paths are independent:

```
[ Pre-deployment ]
    MEMIT-COMPAT-PROTO-1 →  PASS / D20-DRIFT / D20-FAIL
                            (architecture-level, not probe-level)
        ↓ if PASS or D20-DRIFT (operator-accepted)
[ This protocol ]
    COMPACTION-PROBE-CALIB-PROTO-1 →  sampling rates, floors, thresholds
        ↓ ratified
[ Operational ]
    Per-compaction-event probe → classification:
        COMPACTION_PROCEEDED         (normal path)
        COMPACTION_ABORTED           (compaction-side failure, route to MEMIT review)
        COMPACTION_PROBE_FAILED      (probe-side failure, route to infrastructure review)
```

The three runtime classifications are mutually exclusive. A single compaction event produces exactly one Ledger entry of these three types.

### 6.6 What this protocol leaves to GAP-15

GAP-15 (compaction verification ownership, Validation + MEMIT) — the question of *who runs the Behavioral Probe* and how its independence from the MEMIT execution path is enforced — is **not resolved** by this protocol. This protocol assumes the Behavioral Probe Agent exists as a distinct process, has its own identity (`prober_agent_id` in §5.2), and runs the probes independently of the Coder Agent and MEMIT layer.

GAP-15's resolution determines whether `prober_agent_id` is a single agent, a pool, or a meta-prober that itself has reliability monitoring. That work is for a separate session jointly between Validation and MEMIT skills. The deployment-blocking status flagged in the validation-contract-architect skill remains; this protocol's completion does not retire it.

The empirical implications for this protocol: GAP-15's eventual resolution may add fields to `Section A — Identity & Reproducibility` (e.g., `prober_pool_membership`, `prober_independence_attestation`). The §5.2 schema is forward-extensible to accommodate that addition under the v1.3 → v1.4 minor version increment path.

---

## 7. Calibrated Outputs — Mapping to Tier 1 Config and IC-OC-PROBE

The protocol's calibrated values land as follows:

| Calibrated output | Lands in |
|---|---|
| SUPPORTING sampling rate | Tier 1 config: `compaction_supporting_sample_rate`. Replaces provisional 20%. |
| SUPPORTING floor | Tier 1 config: `compaction_supporting_floor`. Replaces provisional 5. |
| SUPPORTING abort threshold | Tier 1 config: `compaction_supporting_threshold`. Validates or replaces 0.95. |
| INCIDENTAL sampling rate | Tier 1 config: `compaction_incidental_sample_rate`. Replaces provisional 10%. |
| INCIDENTAL floor | Tier 1 config: `compaction_incidental_floor`. Replaces provisional 3. |
| INCIDENTAL abort threshold | Tier 1 config: `compaction_incidental_threshold`. Validates or replaces 0.80. |
| Infrastructure failure threshold | Tier 1 config: `compaction_probe_infra_failure_threshold`. New field; protocol-proposed 0.05. |
| Infrastructure-bias-aware threshold | Tier 1 config: `compaction_probe_infra_failure_threshold_biased`. New field; protocol-proposed 0.02. |
| Family stratification flag | Tier 1 config: `compaction_per_family_sampling_required`. Boolean; triggers per-family sub-stratification in IC-OC-PROBE if true. |
| Calibration epoch ID | Tier 1 config: `compaction_sampling_calibration_id`. Identifies the calibration packet that produced these values. |

CORE values (`100% sample`, `1.0 threshold`) are **not in this table** — they are spec-fixed by C-OC3.

---

## 8. Pre-Execution Candidate Values & Rationale

The empirical sweep produces final values. Pre-execution, the protocol's candidate values, rationale, and confidence:

| Parameter | Spec / provisional | Protocol-proposed candidate | Rationale | Confidence pre-sweep |
|---|---|---|---|---|
| SUPPORTING sample rate | 20% | **20%** (retained) | At populations ≥150, 20% gives ≥30 samples — adequate power. Below 150, floor takes over. Sweep may recommend 15% if floor adjustment compensates. | Medium-high |
| SUPPORTING floor | 5 | **30** | Power calc: discriminating p=0.95 from p=0.85 at α=0.05, β=0.20 needs n≈30. Spec floor of 5 cannot discriminate at this level. | High (math-driven) |
| SUPPORTING threshold | 0.95 | **0.95** (retained) | Distance from typical compaction pass rate (0.97–0.99) gives discrimination margin. Sweep tests 0.92 and 0.97 for sensitivity. | Medium-high |
| INCIDENTAL sample rate | 10% | **10%** (retained) | At populations ≥200, 10% gives ≥20 samples. Below 200, floor takes over. | Medium |
| INCIDENTAL floor | 3 | **15** | Power calc: discriminating p=0.80 from p=0.65 at α=0.05, β=0.20 needs n≈18. Floor of 3 cannot discriminate. | High (math-driven) |
| INCIDENTAL threshold | 0.80 | **0.85** (tightened) | Typical INCIDENTAL pass rate (0.85–0.92) sits close to 0.80; insufficient discrimination margin. Tightening to 0.85 trades higher false-positive rate for lower false-negative rate (FN-cost-weighted at 4×, this is favourable). Sweep validates. | Medium |
| Infrastructure failure threshold (uniform) | (not specced) | **0.05** | Below 5%, sample power preserved; above 5%, biased sample risk rises. | Medium |
| Infrastructure failure threshold (biased) | (not specced) | **0.02** | When infra failures are non-uniform, even small absolute failure rates produce substantial sample bias. Tighter threshold protects against silent pass-rate inflation. | Medium-low (untested) |
| Family stratification flag | (not specced) | **conditional** — engages iff adversarial-corpus family-clustering miss-rate ratio > 1.5× | Avoids paying complexity cost unless empirically justified. Mirrors EPSILON-CALIB-PROTO-1 §1.1 family-deviation trigger pattern. | Medium |

Confidence levels reflect pre-execution belief. The sweep produces final ratifiable values.

---

## 9. Kill Criteria & Non-Goals

### 9.1 Kill criteria

The protocol does not produce ratifiable calibration outputs if any of the following hold:

- **Stage A admission rate < 50%** — model probe stability is too low; calibration would converge on values protecting against probe noise rather than compaction regression. Kicks back to MEMIT-COMPAT-PROTO-1 OP-1.
- **Stage C uncertain rate > 15%** — too many edges fall in the 6/10–8/10 ambiguous band; oracle is unreliable. Same kickback.
- **Cross-corpus disagreement > 5%** on key rate-vs-recall points — calibration is non-reproducible; either probe set or compaction itself is unstable. Flags `CALIBRATION_NON_REPRODUCIBLE`.
- **Adversarial miss-rate ratio > 3.0×** at all swept rates for any cluster mode — clustering vulnerability is severe enough that no rate-based sampling can protect against it. Tertiary stratification or alternative sampling design (e.g., non-random adversary-aware sampling) required before re-run.
- **MEMIT-COMPAT-PROTO-1 verdict is D20-FAIL** — upstream KILL propagates, this protocol does not execute.
- **MEMIT-DRIFT-PROTO-1 outputs unavailable** — `S_ceiling` and drift thresholds are required to size compaction events realistically; their absence makes calibration unrepresentative.

### 9.2 Non-goals

This protocol does not specify:

- CORE sampling rate or threshold (spec-fixed by C-OC3)
- Probe template authorship rules (owned by §21.3, TGA authority)
- ε numeric values, M thresholds, BUCKET boundaries (owned by EPSILON-CALIB-PROTO-1)
- The Behavioral Probe Agent's identity, independence, or pool architecture (GAP-15, separate session)
- Cross-deployment portability of calibrated values (per §22.8, calibrations are per-deployment)
- Compaction trigger threshold values themselves (owned by MEMIT-DRIFT-PROTO-1 outputs)
- Re-calibration cadence (operator policy, OQ-W-CALIB-CADENCE pattern applies)
- Per-judge-model thresholds (§21.4, OQ-V-JUDGE-THRESHOLD)

---

═══════════════════════════════════════════════════
## Session Summary Block — COMPACTION-PROBE-CALIB-PROTO-1 Authored
═══════════════════════════════════════════════════

**Session:** 1.5 — OQ-OC3 calibration protocol authorship (validation-contract-architect primary, memit-specialist secondary)
**Status:** Draft (design-complete; gated on MEMIT-COMPAT-PROTO-1 PASS + MEMIT-DRIFT-PROTO-1 outputs before execution)

### Decisions made

- Stage 1.5 protocol formally named **COMPACTION-PROBE-CALIB-PROTO-1**. Eight components: ground-truth oracle, sampling sweep, floor validation, abort-threshold sensitivity, CompactionProbeReport population, COMPACTION_PROBE_FAILED vs COMPACTION_ABORTED separation, calibrated-output mapping, pre-execution candidate values.
- **Ground-truth oracle:** three-stage qualifying probe — Stage A pre-compaction stability filter (10/10 admission), Stage B compaction event, Stage C post-compaction full-population probe with two-band labelling (REGRESSED ≤5/10, SURVIVED ≥9/10, UNCERTAIN excluded). 10/10 stability filter is non-negotiable; admission rate <50% triggers kickback to MEMIT-COMPAT-PROTO-1 OP-1.
- **Corpus size:** 7,500-edge realistic-mix corpus (500 edges per cell across 15 cells = 3 tiers × 5 families) for sub-1% rate resolution. Adversarial corpora at 100 edges per affected cell across three clustering modes (family, neighborhood, recency).
- **Sampling sweep:** 9-point rate sweep per tier, 8-point floor sweep per tier, 5-point threshold sweep per tier, 9-point synthetic population pass rate sweep. 500 random samplings per configuration; 3 independent corpus replicates with 5% cross-corpus disagreement ceiling.
- **Adversarial bands:** miss_rate(adversarial) / miss_rate(realistic) ≤1.5× tolerable, [1.5, 3.0] flag for tertiary stratification, >3.0× mandatory tertiary stratification.
- **Floor-acceptance rule:** P(false-negative abort) ≤5% across stratum sizes ≥2× floor; worst-case single-regression detection rate ≥50% in binding zone; P(false-positive abort) ≤10% at threshold + 0.02.
- **Threshold loss function:** loss(T) = 4 × P(FN) + 1 × P(FP). FN weighted four times higher than FP given silent-knowledge-corruption asymmetry. 4:1 weighting protocol-proposed; ratifiable.
- **CompactionProbeReport extension:** Five-section schema (Identity, Per-Stratum Outcome, Aggregate Decision, Infrastructure Failure Accounting, Calibration Provenance). Adds `infrastructure_failed_count`, `effective_sample_size`, `failure_id_sidecar_ref`, `infrastructure_failure_bias_check`, `report_classification` enum, calibration-provenance fields.
- **C-META1 spirit reconciliation:** sealed sidecar file (operator-signed, append-only, hash-anchored in main ledger entry) carries full per-edge failure ID list when stratum failure count exceeds 10. Main payload retains summary; sidecar retains audit completeness. Backward-compatible v1.3 IC-OC-PROBE extension.
- **Classification rule (PROBE_FAILED vs ABORTED):** infrastructure_failure_rate > θ_infra → COMPACTION_PROBE_FAILED (overrides per-stratum decision). Else aggregate per-stratum decision: any ABORT → COMPACTION_ABORTED; else COMPACTION_PROCEEDED. Mutually exclusive runtime classifications.
- **Bias check:** per-cell z-score on infra failure rate against expected; |z| > 2.0 → NON_UNIFORM bias flag → tighter θ_infra (0.02 vs 0.05). Protects against systemic biased sample (complex edges timing out → easy-edge-only effective sample inflates pass rates).
- **Independence from MEMIT-COMPAT-PROTO-1:** PROBE_FAILED is a probe-infrastructure event, distinct from MEMIT-COMPAT-PROTO-1's architecture-level verdict. The two diagnostic paths are independent and never conflated. MEMIT-COMPAT D20-FAIL propagates as KILL upstream of this protocol.

### Constraints established

- This protocol consumes (does not author) `architecture_profile.json`, probe-set v1 corpus, MEMIT-DRIFT-PROTO-1 `S_ceiling` and drift thresholds. All artifacts must be content-hash-verified at calibration corpus admission.
- 10/10 pre-compaction stability filter is non-negotiable for valid calibration. <50% Stage A admission triggers kickback.
- CORE sampling rate (100%) and threshold (1.0) are spec-fixed (C-OC3) and excluded from calibration scope. The calibration cannot weaken CORE.
- Infrastructure failure classification overrides per-stratum aggregation when triggered. Even if aggregate would be PROCEED, high infrastructure failure rate produces COMPACTION_PROBE_FAILED — measurement trustworthiness gates the decision.
- COMPACTION_ABORTED and COMPACTION_PROBE_FAILED are mutually exclusive runtime Ledger event classifications. A single compaction event produces exactly one of these (or COMPACTION_PROCEEDED).
- IC-OC-PROBE extension is additive (v1.2 → v1.3 minor version). Ratification ceremony (parallel to §22.5) controls config flag for backward emission.
- MEMIT-COMPAT-PROTO-1 PASS / D20-DRIFT verdict required to proceed; D20-FAIL → KILL.
- MEMIT-DRIFT-PROTO-1 outputs (`S_ceiling`, drift thresholds) required to size compaction events representatively.
- This protocol does NOT resolve GAP-15 (compaction verification ownership). GAP-15 deployment-blocking status persists independently.

### Pre-execution candidate values (rationale + confidence)

| Parameter | Provisional | Candidate | Rationale | Confidence |
|---|---|---|---|---|
| SUPPORTING sample rate | 20% | **20%** | Adequate at populations ≥150; floor handles smaller | Medium-high |
| SUPPORTING floor | 5 | **30** | Power calc for 0.95 vs 0.85 discrimination | High (math-driven) |
| SUPPORTING threshold | 0.95 | **0.95** | Adequate margin from typical pass rate; sweep validates | Medium-high |
| INCIDENTAL sample rate | 10% | **10%** | Adequate at populations ≥200; floor handles smaller | Medium |
| INCIDENTAL floor | 3 | **15** | Power calc for 0.80 vs 0.65 discrimination | High (math-driven) |
| INCIDENTAL threshold | 0.80 | **0.85** | Insufficient margin at 0.80; FN-cost-weighted tightening favourable | Medium |
| θ_infra (uniform bias) | (not specced) | **0.05** | Sample power preserved below 5%; risk above | Medium |
| θ_infra (non-uniform bias) | (not specced) | **0.02** | Biased samples need tighter threshold | Medium-low (untested) |
| Family stratification | (not specced) | **conditional** on adversarial >1.5× | Pay complexity cost only when justified | Medium |

### Open questions deferred

- **OQ-V-OC-REPORT-VER** — Tier 1 config flag `compaction_report_schema_version` controlling v1.2 vs v1.3 IC-OC-PROBE field emission for migration window. Operator-tunable; rotation policy operator-owned.
- **OQ-V-OC-INFRA-BIAS** — Bias-aware infrastructure failure threshold (0.02) is protocol-proposed and untested pre-execution. Calibration sweep includes θ_infra ∈ {0.02, 0.05, 0.08, 0.10} but bias correlation with edge difficulty is empirical territory.
- **OQ-OC3-WEIGHT** — Loss function weighting w_FN = 4, w_FP = 1 is protocol-proposed. Operator policy on FN/FP cost ratio belongs to deployment-specific risk posture.
- **OQ-OC3-CADENCE** — Re-calibration cadence after model architecture changes or significant drift threshold updates. Mirrors OQ-W-CALIB-CADENCE pattern; operator policy.

### Cross-domain tensions surfaced

- **T-OC3-1: Aggregate vs. Per-Case Audit** (Validation vs. Warden) — ✅ Resolved. Sealed sidecar file pattern preserves Ledger payload size discipline while keeping per-case data accessible. Backward-compatible v1.3 extension. C-META1 spirit honoured though literal C-META1 scope is Meta-Validator.
- **T-OC3-2: Probe Failure vs. Compaction Failure** (Validation vs. MEMIT) — ✅ Resolved. COMPACTION_PROBE_FAILED and COMPACTION_ABORTED are mutually exclusive runtime classifications with infrastructure failure rate as discriminator. Bias check (NON_UNIFORM tightens threshold to 0.02) protects against silently biased samples masking the distinction.
- **T-OC3-3: GAP-15 Ownership** (Validation + MEMIT, deferred) — 🔴 Not resolved. Behavioral Probe Agent identity, independence enforcement, and pool architecture out of scope. `prober_agent_id` field reserved in §5.2 Section A; GAP-15 resolution may add forward-extensible fields under v1.3 → v1.4. Deployment-blocking status persists.
- **T-OC3-4: Floor Tightening vs. Production Tail Strata** (Validation-internal) — 🔶 Acknowledged. Raising floors from 5→30 (SUPPORTING) and 3→15 (INCIDENTAL) significantly increases probe cost on small strata. For low-volume relation families, floor-driven sample sizes may equal or exceed population — effectively forcing 100% sampling on tail cells. The cost is real but the alternative is silent pass-rate misclassification on small strata. Sweep produces empirical floor values; operator can negotiate complexity vs cost at ratification.

### Pre-mapped tension coverage

- **Pre-T2 (Write Volume vs. Edit Locality)** — Touched by `S_ceiling` consumption from MEMIT-DRIFT-PROTO-1. Compaction event size is bounded by `S_ceiling`; calibration corpus sizing assumes compaction events sized to operational expectations. No new Pre-T2 surface.
- **Pre-T6 (Genesis Completeness vs. Genesis Lock-in)** — Untouched. Compaction does not modify Genesis-tier edges (C-OC1).

### Artifacts the protocol produces (when executed)

- `calibration_corpus_admission_log.json` (Stage A admission outcomes — counts, rejection reasons, instability indicators)
- `oracle_label_log.json` (Stage C per-edge labels — REGRESSED / SURVIVED / UNCERTAIN with confidence)
- `sampling_sweep_results.json` (per-configuration miss-rate, false-positive-rate, false-negative-rate matrices)
- `floor_validation_report.json` (per-floor binding-zone behaviour, single-regression detection rates)
- `threshold_sensitivity_report.json` (per-threshold loss curves, optimal T* per tier)
- `adversarial_corpus_results.json` (per-clustering-mode miss-rate ratios, family-stratification trigger flags)
- `compaction_sampling_calibration_report.json` v1 — final calibrated values for SUPPORTING / INCIDENTAL sample rates, floors, thresholds; θ_infra (uniform and biased); family stratification flag; calibration epoch ID
- `CompactionProbeReport` schema v1.3 specification document (extension to IC-OC-PROBE)
- `CALIBRATION_RATIFICATION_OC3` submission packet (parallel to EPSILON-CALIB §22.5 ceremony path)

### Protocols defined this session

- **COMPACTION-PROBE-CALIB-PROTO-1** — full protocol covering oracle construction, sampling sweep, floor validation, threshold sensitivity, CompactionProbeReport population, PROBE_FAILED vs ABORTED separation, calibrated-output mapping.
- **`CALIBRATION_RATIFICATION_OC3` ceremony type (proposed)** — calibration packet ratification under existing IC-SCOPE-AUTH-1 envelope; placement parallels EPSILON-CALIB-PROTO-1 ceremony path. No new envelope mechanics; same Warden authority.

### Next session candidates

- **GAP-15 session (Validation + MEMIT joint):** Resolve compaction verification ownership — Behavioral Probe Agent identity, independence enforcement from MEMIT execution path, pool architecture, prober reliability monitoring. Deployment-blocking status retained until resolved. Carries forward `prober_agent_id` schema slot reserved in §5.2.
- **IC-OC-PROBE v1.3 ratification session (Warden + Validation joint):** Author the v1.2 → v1.3 schema migration ceremony, OQ-V-OC-REPORT-VER config flag mechanics, sealed-sidecar file specification (signing authority, retention coupling, hash-anchor pattern).
- **Stage 4 — Consolidation:** With Stage 1 PASS, Stage 2 outputs, Stage 3 (EPSILON-CALIB) outputs, and Stage 1.5 (this protocol) outputs all in hand, bundle into a unified POC submission packet. Per write-engine-poc-scope §6, Stage 4 is sequencing and packaging.

═══════════════════════════════════════════════════
*COMPACTION-PROBE-CALIB-PROTO-1 — design-complete, awaiting MEMIT-COMPAT-PROTO-1 PASS + MEMIT-DRIFT-PROTO-1 outputs to execute*
*Specialist provenance: Validation Contract Architect (primary, probe-side correctness contract) + MEMIT Specialist (secondary, compaction-side semantics). GAP-15 ownership question explicitly deferred to separate session; deployment-blocking status retained.*
═══════════════════════════════════════════════════
