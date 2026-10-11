# Gap Session 1.1 Summary — MEMIT Specialist
## LLM as Database: Agent Harness Architecture

> **Session:** Gap Session 1 of 6 (Session 1.1 in file naming)
> **Domain:** MEMIT Specialist (primary); Validation Contract Architect (observation)
> **Topic:** GAP-1 — Drift/Compaction Threshold Calibration Framework
> **Baseline:** v1.1 Integrated Specification + Gap Backlog v2.0
> **Status:** Formal deferral confirmed; calibration framework produced

---

## Session Scope

GAP-1 targeted the seven provisionally-specified drift-from-anchor and compaction threshold
values, all marked OQ-W1. The session's objective was to determine what spec work could
accomplish on a formally deferred empirical gap.

**Core finding:** GAP-1 cannot be resolved through specification work. However, the spec can
produce four meaningful deliverables:

1. A classification of each threshold by theoretical footing
2. A calibration protocol — the exact measurement procedure to convert provisional to ratified
3. A formal deferral record with sentinel conditions defining when GAP-1 is "resolved"
4. Three structural relationships between thresholds that are spec requirements, not empirical

---

## Gaps Resolved

None. GAP-1 cannot be resolved without empirical testing against a selected target model.

---

## Gaps Partially Resolved

**GAP-1** — Status upgraded from "empirically blocked / deferred" to **"formally deferred
with calibration framework."**

Produced in this session:

- Threshold Inventory (see below) — each of the seven provisional thresholds classified
  by theoretical footing
- Threshold Calibration Protocol Spec Block — a seven-step ordered measurement protocol
- Formal Deferral Record Spec Block — sentinel conditions defining when GAP-1 is "resolved"
- Three structural relationships identified as spec requirements (not empirical):
  the 50% buffer multiplier, the 97.0% recall criterion, the 2× p95 latency cap

---

## Gaps Deferred

**GAP-1 (formally)** — Deferral rationale: calibration requires (1) target model selection
and (2) completed Genesis compile — both implementation-phase preconditions. Deferral does
not block the spec arc; blocks implementation-phase calibration only. Sentinel conditions
defined in this session close the deferral.

**OQ-W1-R2** (calibration drift across compaction cycles) — Permanent operational concern.
Not a session-closable item; noted as a recurring calibration obligation.

---

## Threshold Inventory — Classification Pass

| Threshold | Spec Value | Classification | Principled Floor/Ceiling? | Calibration Step |
|---|---|---|---|---|
| Drift warning | 1,500 edges | Pure heuristic | No | Step 2 |
| Drift hard trigger | 8,000 edges | Heuristic (ratio-coupled) | No (curve-dependent) | Step 3 |
| Sub-batch ceiling | 2,000 edges | Principled heuristic | Yes — derivable from hidden dimension | Step 1 |
| Overlay file count | 50 files | Heuristic (**wrong spec layer**) | No | Step 5 |
| p95 latency trigger | 2× baseline | Operationally grounded | Yes — industry-standard SLO floor | Step 6 (confirm only) |
| `stale_urgent` ceiling | 1,000 edges | Pure heuristic (deployment-specific) | No | Step 4 (operator-derived) |
| Pruning floor | 24 hours | Architectural constraint | Yes — derivable from cascade latency | Step 7 |

**Key finding on Threshold 4 (Overlay file count):** This threshold is mis-specced at the
MEMIT domain layer. It measures an inference-runtime property, not a parametric memory
property. It should be explicitly flagged as deployment-tunable with no MEMIT-level anchor,
distinct from the other six thresholds.

---

## Threshold Calibration Protocol — Spec Block

### What it must specify

The ordered measurement protocol that converts the provisional threshold set (OQ-W1) into
ratified operational values during implementation phase. "Resolved" for GAP-1 means: all
seven thresholds have been set via this protocol and the resulting values have been recorded
in Tier 1 config with a `VERSION_ADVANCED` Ledger entry referencing the calibration run IDs.

### Hard Constraints

- Calibration MUST be run on the actual target model used in production. Proxy-model
  calibration does not satisfy OQ-W1.
- Calibration MUST be run after Genesis compile is complete, against the post-Genesis
  parametric state.
- At least two independent calibration runs MUST be performed. Threshold values are set to
  the more conservative (lower-triggering) of the two runs.
- Calibration results MUST be recorded as immutable `CALIBRATION_RUN` Ledger entries.
  Thresholds may not be updated without a new calibration run.

### Step-by-Step Protocol

**Step 1 — Sub-batch ceiling (Threshold 3)**

Inject batches of increasing size (500 / 1,000 / 1,500 / 2,000 / 3,000 / 4,000 / 5,000
edges) into the post-Genesis model. After each batch, run the L1 storage probe on a held-out
sample of 100 pre-existing edges not in the batch. Record recall rate of pre-existing edges
per batch size.

*Criterion:* Sub-batch ceiling = largest batch size at which held-out edge recall ≥ 99.5%.
(The 99.5% threshold is a spec requirement matching the behavioral probe pass threshold §8.9.)

*Output:* `calibrated_sub_batch_ceiling` — feeds Step 2 and Step 3.

---

**Step 2 — Drift warning (Threshold 1)**

Execute sequential incremental writes in sub-batches of `calibrated_sub_batch_ceiling` size.
After each sub-batch, run the L1 storage probe on the same held-out 100-edge sample from
Step 1. Continue until recall rate drops below 99.0%.

*Criterion:* Drift warning = **0.5 × (accumulated edge count at 99.0% recall crossing).**
The 50% buffer multiplier is a spec requirement, not operator-configurable.

*Output:* `calibrated_drift_warning`.

---

**Step 3 — Drift hard trigger (Threshold 2)**

Continue sequential writes beyond the drift warning onset until recall drops below 97.0%.

*Criterion:* Drift hard trigger = accumulated edge count at 97.0% recall crossing.
The 97.0% threshold is a spec requirement — 3% false-positive rate on knowledge retrieval
is the defined practical unacceptability boundary.

*Output:* `calibrated_drift_hard_trigger`.

---

**Step 4 — `stale_urgent` backpressure ceiling (Threshold 6)**

This threshold is deployment-specific and depends on Pruning Agent throughput. Operator must:

- (a) Estimate the Pruning Agent's sustainable edge deletion throughput per 24-hour period
  under realistic task load.
- (b) Set the ceiling to no more than 2× that throughput.

*Rationale:* At 2× throughput, the Pruning Agent can clear the backlog within 48 hours
under maximum sustained operation.

*Output:* `calibrated_stale_urgent_ceiling` (operator-derived, not model-derived).

---

**Step 5 — Overlay file count trigger (Threshold 4)**

Mount progressively larger overlay stacks (10 / 20 / 30 / 40 / 50 / 75 / 100 files) against
the inference runtime. Measure p95 inference latency for each stack size using the
Constitutional Test Suite as the probe corpus.

*Criterion:* Overlay file count trigger = stack size at which p95 latency first exceeds
**1.5× the single-overlay baseline.** (Leaves headroom before the 2× hard latency trigger.)

*Output:* `calibrated_overlay_count_trigger`.

---

**Step 6 — p95 inference latency trigger (Threshold 5)**

No separate calibration measurement. Retained at 2× baseline as a deployment-independent SLO
boundary. Confirmed at calibration time by verifying the overlay count trigger (Step 5) fires
before 2× latency is reached under normal operation. If not, overlay count trigger requires
downward revision.

*Output:* `p95_latency_trigger` = 2.0× baseline (confirmed or flagged for revision).

---

**Step 7 — Pruning floor (Threshold 7)**

Measure maximum end-to-end latency of the validation cascade: Tier 2 retry × 3, plus Review
Queue human escalation wait time.

*Criterion:* Pruning floor = **max(24 hours, 2 × maximum cascade latency).**
The 24-hour minimum is retained as an architectural floor regardless of measurement results.

*Output:* `calibrated_pruning_floor`.

---

## Formal Deferral Record — Spec Block

**Status:** FORMALLY DEFERRED — Implementation Phase

**Deferral rationale:** GAP-1 cannot be resolved through specification work. The threshold
values tagged OQ-W1 are properties of a specific target model's FFN architecture under a
specific edit-volume load pattern. No amount of theoretical analysis substitutes for empirical
measurement. This deferral does not block the specification arc — provisional values remain
valid as implementation starting points.

**What the deferral does NOT mean:**

- Does not mean current provisional values are arbitrary — each has a documented rationale.
- Does not mean operators may choose values arbitrarily — values must be set via the
  calibration protocol; values set without a valid `CALIBRATION_RUN` Ledger entry are
  out-of-spec.
- Does not mean the spec is incomplete — the calibration protocol converts provisional to
  ratified.

### GAP-1 Sentinel Conditions (Closing Criteria)

GAP-1 is **RESOLVED** when all five conditions are met:

1. A target model has been selected and its `model_id` is recorded in Tier 1 config.
2. Genesis compile has completed; `IMMUTABLE_ANCHOR` entry exists in the Ledger.
3. At least two `CALIBRATION_RUN` Ledger entries exist, both referencing the same `model_id`
   and the same post-Genesis edge count (within ±5% variance between runs).
4. Tier 1 config has been updated to reflect calibrated values, with a `VERSION_ADVANCED`
   Ledger entry referencing both `CALIBRATION_RUN` entry IDs.
5. Calibrated values have been reviewed and counter-signed by a human operator distinct from
   the operator who ran the calibration.

### What Remains Permanently in the Spec

The structural relationships are spec requirements that do not change based on calibration:

- 50% buffer multiplier for drift warning (Step 2)
- 97.0% recall criterion for hard trigger (Step 3)
- 2× p95 latency cap (Step 6)
- Calibration protocol itself (operators may not deviate without an amended protocol)

**OQ-W1-R2 is a permanent operational concern:** Calibration is not one-time. If calibrated
values drift >20% between compaction cycles, thresholds must be updated and re-ratified.

---

## New Gaps Surfaced

### GAP-29 — Pruning Floor May Be Underspecified

| Field | Value |
|---|---|
| **Domain(s)** | MEMIT Specialist, Validation Contract Architect |
| **Priority** | 🟡 Medium |
| **Status** | Open |

**Description:** The 24-hour Pruning floor (§17.5) may not protect edges still in the
validation cascade under worst-case conditions. If a task escalates to the human review
queue (§9.6 escalation Step 3) and awaits decision for 36–48 hours, a 24-hour floor does
not protect it.

The calibration protocol's Step 7 formula yields:
`Pruning floor = max(24h, 2 × maximum cascade latency)`

Under a 48-hour review queue SLO, this yields a potential floor of **96 hours** — 4× the
current spec value of 24 hours.

**Resolution path:** Validation Contract Architect (GS9) to specify maximum cascade latency
under worst-case retry + review queue conditions. MEMIT Specialist to apply floor formula.
May require upward revision of §17.5.

**Blocks:** Nothing directly. But the 24-hour value should be audited before implementation
begins.

---

## New Tensions Surfaced

None. T13 (Advisory Boundedness vs. Operational Flexibility) was previously identified and
is assigned to GS8. No new cross-domain tensions emerged in this session.

---

## Decisions Made

| ID | Decision |
|---|---|
| **D-GS1_1-A** | The 50% buffer multiplier for drift warning calibration is a **spec requirement**, not operator-configurable. Operators may not reduce it without an amended protocol. |
| **D-GS1_1-B** | The 97.0% held-out recall threshold for drift hard-trigger calibration is a **spec requirement**. Both the criterion and the corpus size (100-edge held-out set) are spec-required. |
| **D-GS1_1-C** | The overlay file count trigger (Threshold 4) is **mis-specced at the MEMIT domain layer**. It is a deployment-runtime property. The spec should explicitly flag it as deployment-tunable with no MEMIT-level anchor. Annotation amendment — not a decision change. |
| **D-GS1_1-D** | Calibration must be performed on the **actual target model**, post-Genesis. Proxy-model calibration does not satisfy OQ-W1. |
| **D-GS1_1-E** | At least **two independent calibration runs** are required. Values are set to the more conservative (lower-triggering) of the two. |
| **D-GS1_1-F** | Calibration is **not a one-time event**. Re-calibration required after each compaction cycle if calibrated values drift >20% between cycles. |

---

## Interface Contracts Defined

**IC-CALIBRATION-1** — Calibration protocol is consumed by Tier 1 config update ceremony.
Threshold fields marked OQ-W1 provisional may not retain provisional values after the first
valid `CALIBRATION_RUN` Ledger entry is written.

**IC-CALIBRATION-2** — Calibration results require human counter-signature by an operator
distinct from the operator who ran the calibration.

---

## New Ledger Entry Types Proposed

### `CALIBRATION_RUN` (GOVERNANCE, synchronous)

```
run_id:                   string    # Unique run identifier
calibration_version:      string    # Protocol version this run follows
model_id:                 string    # Target model (architecture + checkpoint)
post_genesis_edge_count:  int       # Edge count at time of calibration
results: {
  calibrated_sub_batch_ceiling:      int
  calibrated_drift_warning:          int
  calibrated_drift_hard_trigger:     int
  calibrated_stale_urgent_ceiling:   int
  calibrated_overlay_count_trigger:  int
  p95_latency_trigger_confirmed:     bool
  calibrated_pruning_floor:          string   # ISO 8601 duration
}
operator_id:              string
operator_signature:       string
```

---

## Open Questions Carrying Forward

| ID | Question | Blocked By |
|---|---|---|
| OQ-W1-R1 | Held-out recall baseline — must be measured at Genesis, not assumed at 100%. | Implementation phase |
| OQ-W1-R2 | Calibration drift across compaction cycles — permanent operational concern; recurring recalibration obligation. | Ongoing |
| OQ-W1-R3 | T13 dependency: `LARQL_VERSION_LEGACY` hard-block threshold (100 patches) must be revisited against `calibrated_drift_warning` at implementation time. | T13 resolution (GS8) + GAP-1 calibration |

---

## Amendment Recommended

**§17.5 Pruning floor annotation:** Add a note that the 24-hour floor is a minimum and may
require upward revision based on maximum validation cascade latency per calibration Step 7.
No decision change — annotation only. Assigned for inclusion in GS9 Validation Contract
Architect review.

---

## Downstream Unblocking (When GAP-1 Closes)

When the five sentinel conditions are met at implementation phase:

| Downstream Item | Unblocked |
|---|---|
| GAP-9 (compaction verification sample size) | Can be evaluated against actual compaction edge volumes |
| GAP-15 (compaction sample rate detail) | Can be closed or deferred with empirical basis |
| T13 hard-block threshold (100 patches) | Revised against `calibrated_drift_warning` (OQ-W1-R3) |
| Circuit-breaker threshold rationale | Gains empirical grounding |
| Write-budget SLA specification | Becomes possible |

---

## Cross-Domain Observations

**Sub-batch ceiling (Threshold 3) is partially resolvable pre-implementation.** If the target
model *family* is known before the implementation phase, a pre-implementation estimate of the
sub-batch ceiling can be approximated from the model architecture spec (hidden dimension,
layer count). This narrows the uncertainty range before the first calibration run. The MEMIT
Specialist recommends selecting the target model family before the implementation phase begins.

**Overlay file count trigger (Threshold 4) should be re-homed.** It belongs in a future
inference runtime spec section, not the drift-tracking section. Current placement creates
a false impression that it is a MEMIT-level property.

**Pruning floor (Threshold 7) is the most resolvable threshold within spec scope.** It can
be partially specified right now by examining the maximum validation cascade latency — a
property of the validation spec, not the model. GAP-29 captures this obligation.

---

*Gap Session 1.1 Summary — LLM as Database: Agent Harness Architecture*
*MEMIT Specialist — GAP-1 Formal Deferral + Threshold Calibration Framework*
