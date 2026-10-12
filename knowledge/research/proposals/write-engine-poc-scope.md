# Write Engine POC — Scope Document

*Workstream: Empirical POC Scoping (post-v1.2 sealed spec)*
*Session: Write Engine POC scope*
*Primary skill: memit-specialist*

Bounded scope: the write layer of the v1.2 harness — MEMIT, `.vindex` overlay, `.larql` patches, drift state, overlay compaction, fidelity ε. The POC retires Write-Engine-owned items in §18.1 and produces ratification artifacts for the §22 ceremony path.

---

## 1. Exit Criteria — Questions the POC Must Answer

The POC is complete when each of the following has a documented answer with evidence:

- Does MEMIT successfully edit the target model's FFN, with retrieval fidelity measurable through the canonical probe set? (OQ-W2)
- Where does the volume-vs-degradation curve break for this model — i.e., what are the calibrated drift WARNING and HARD thresholds, and is there a knee at all? (OQ-W1)
- What is the recommended MEMIT sub-batch ceiling for this model? (OQ-W1; currently provisional at 2,000)
- For each transform class in the §22 manifest schema (RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT), what is the per-version-hop ε (p95 fidelity delta)? (OQ-W-CALIB-1)
- What `Δfidelity_max` value is empirically supportable for this deployment, and what M values follow from it? (OQ-W-CALIB-1; provisional default 0.05)
- For the `attention_weight → declared_importance` BUCKET transform, do GS7's illustrative 0.33 / 0.66 boundaries match the empirical distribution, or do they need replacement? (D-GS8-B)
- Is the probe-set v1 corpus stable enough to anchor calibration across at least one Genesis update cycle? (OQ-W-PROBE-VERSION, partial)

---

## 2. In-Scope Calibrations

### Retires fully
- **OQ-W1** — drift thresholds (WARNING / HARD / sub-batch).
- **OQ-W2** — MEMIT/target architecture compatibility verdict.
- **OQ-W-CALIB-1** — ε values, M values, bucket boundaries via §22 ratification packet. Closes GAP-1, GAP-2 dependencies.

### Partially informs
- **OQ-OC3** — compaction sampling rates inherit from drift curve shape; the POC produces the W1 numerator. Final OQ-OC3 calibration sits downstream.
- **OQ-W-PROBE-VERSION** — POC ships probe-set v1 with a frozen template hash and `probe_set_version: 1`. Cross-Genesis versioning policy (GAP-48) remains operator-owned.
- **OQ-W8 (residual)** — the probe-set corpus assembled here is foundational for L2 sub-type threshold calibration, but per-sub-type judge thresholds are not set in this POC.

### Not touched
- **OQ-V-JUDGE-THRESHOLD** — validator POC scope.
- **OQ-V-SELF-REF (GAP-49)** — methodological, deferred.
- **OQ-CAKB-BURST (GAP-56)** — workload modeling, security/orchestration scope.
- **T5 / T11 cadences** — operational tuning, post-deployment.
- All Genesis policy / CAK / break-glass / key rotation OQs.
- All orchestration-path OQs (GAP-4 family).

---

## 3. Out of Scope — Operational / Infrastructure

The POC explicitly does not address:

- Orchestrator implementation (LangGraph / SDK / hybrid — GAP-4 path selection).
- Reconciliation Review Queue mechanics, Pruning Agent operation, Dependency Hold lifecycle.
- CAK bootstrap, ceremony authorization, break-glass, key rotation, HSM integration.
- Multi-machine harness, Ledger replication, distributed consensus.
- Network, storage tier, deployment topology decisions.
- Production observability, alerting, notification channels.
- Integration with a live agent layer — the POC uses **synthetic `.larql` patch corpora**, not real Coder/Architect output. Agent-output realism is a downstream concern.
- L2 behavioral judge-model selection, judge-prompt authorship, threshold tuning.
- Constitutional test corpus authoring or constitutional-failure policy.

This list is not exhaustive, but the principle is: anything outside the MEMIT compile path, drift accounting, overlay file lifecycle, fidelity measurement, and probe-set anchoring is out of scope.

---

## 4. Success / Kill / Ambiguous Criteria

### Greenlight (full implementation proceeds)
- **OQ-W2:** MEMIT edits succeed on the target architecture with retrieval fidelity at or above the threshold encoded in the probe-set v1 acceptance criteria; locality holds (existing canonical facts not corrupted at modest N).
- **OQ-W1:** A clear knee exists in the volume-vs-degradation curve. WARNING and HARD threshold values are derivable as point values (or tight intervals) ahead of the catastrophic regime.
- **ε calibration:** Per-class ε values are stable across the reference corpus, and chosen M values do not produce false-positive compaction aborts when replayed against the corpus.

### Kill (forces spec revision pass)
- **OQ-W2 negative:** No measurable in-weight retention on the target architecture, or destructive interference with existing facts at small N. Triggers re-evaluation of the write-engine premise (GRACE alternative, model swap, or architectural pivot).
- **OQ-W1 has no knee:** Fidelity degrades approximately linearly from N=1 with no inflection. Implies there is no "operational regime" — only a continuous degradation budget — which invalidates the tier-based drift model in §8.7. Forces a redesign of `drift_state` semantics.
- **ε divergence:** Per-class ε values exceed `Δfidelity_max = 0.05` at the **p50** (not p95) for one or more transform classes that are non-optional in production manifests. Implies §22's tolerance assumption is mis-scaled and the compaction model needs revisiting.

### Ambiguous (POC extension required)
- **OQ-W2 partial:** MEMIT compiles, but retrieval fidelity sits in 0.7–0.9 — operable but with implications that need validator-side coordination. Extension: bring the validator POC forward to settle joint thresholds.
- **OQ-W1 noisy knee:** Knee exists but only as a wide confidence interval; point thresholds not derivable. Extension: extend the experiment with longer runs or wider corpora; ratify ranges instead of points.
- **Per-class ε split:** Some transform classes calibrate cleanly (e.g., RENAME, DROP), others are unstable (typically COMPUTE). Extension: ship calibrated classes to ratification; flag unstable classes with `calibration_state: UNCALIBRATED` per §22.7 and revisit.
- **Probe-set instability:** Probe-set v1 produces inconsistent results across replicate runs. Extension: probe-set authorship pass before any threshold ratification — calibration on an unstable probe set ratifies nothing.

---

## 5. Deliverables

The POC produces, at minimum:

1. **Architecture Compatibility Verdict** — pass / fail / partial, with raw retrieval-fidelity evidence per IC-WE-1 fields, per OQ-W2.
2. **Drift Curve Dataset** — `(N edges, mean fidelity, p95 fidelity, p95 latency ratio, overlay file count)` tuples spanning the calibrated regime up to and through the catastrophic threshold, anchored at a successful Genesis compile.
3. **Drift Threshold Table** — calibrated WARNING, HARD, and sub-batch ceiling values with confidence intervals; replaces provisional 1,500 / 8,000 / 2,000.
4. **Probe-Set v1 Corpus** — canonical probe set with frozen template hashes, judgment dependencies pinned per §21.5, declared `probe_set_version: 1`. This is the calibration anchor referenced by all subsequent calibrations.
5. **Reference Patch Corpus** — ≥200 patches per transform class for at least one `current_larql_version` hop (per §22.2 precondition). Reusable for re-calibration on architecture refresh.
6. **`epsilon_calibration_report` v1** — schema-conformant per §22.4. Per-transform-class p95 ε for the version hop measured.
7. **Bucket Boundary Table** — calibrated boundaries for `attention_weight → declared_importance`, per D-GS8-B; ratifies or replaces the GS7 0.33 / 0.66 illustrative default.
8. **Compaction Tolerance Evidence** — empirical support for ratifying or replacing `Δfidelity_max = 0.05`, with derived M values per §22.5.
9. **`CALIBRATION_RATIFICATION` Submission Packet** — bundle (1)–(8) in the form expected by the §22.5 ceremony, including signing CAK metadata block.
10. **Per-Deployment Re-Calibration Playbook** — operational document covering how to re-run the calibration on architecture or model refresh. Required because calibrations are non-portable per §22.8.

---

## 6. Rough Sequencing

### Stage 0 — Preconditions (operator-owned, prior to Stage 1)
- Target model committed.
- Reference Patch Corpus drafted (≥200 patches × applicable transform classes × ≥1 version hop). Real or synthetic agent output, but representative.
- Probe-Set v1 Corpus drafted in coordination with `validation-contract-architect`.
- At least one `current_larql_version` increment has been authored, producing a non-empty migration manifest with RENAME, BUCKET, and COMPUTE transforms populated (§22.2).

### Stage 1 — OQ-W2 Architecture Compatibility
- Independent, gating. Negative outcome kills the POC.
- Produces deliverables 1, 4 (probe-set used in earnest for the first time).

### Stage 2 — OQ-W1 Drift / Capacity
- Depends on Stage 1 pass.
- Longest experimental block. Produces deliverables 2, 3.
- Outputs feed Stage 3 (sub-batch ceiling affects ε measurement compile parameters) and OQ-OC3 (downstream).

### Stage 3 — ε / M / Bucket Calibration (§22 operationalization)
- Depends on Stage 1 (compatibility) and Stage 2 (sub-batch ceiling for compile parameters).
- Depends on probe-set v1 stability — re-anchoring fidelity measurement on a moving probe set invalidates the calibration.
- Depends on Stage 0 §22.2 preconditions being met.
- Produces deliverables 6, 7, 8.

### Stage 4 — Consolidation and Submission
- Bundle deliverables 1–8 into deliverable 9 (`CALIBRATION_RATIFICATION` packet).
- Author deliverable 10 (re-calibration playbook).
- Findings handoff.

### Critical-path note
Stages 1 and 2 are strictly sequential. Stage 3 cannot start before Stage 2 — but Stage 3 protocol design can be authored in parallel with Stage 2 execution, since Stage 3 depends on Stage 2's *outputs*, not its protocol shape. Plan for Stage 3 protocol authorship to overlap with Stage 2 runtime.

---

## Session Summary Block — Write Engine POC Scope

**Decisions made:**
- Write Engine POC scope locked to MEMIT compile path, drift accounting, overlay file lifecycle, fidelity ε calibration, probe-set v1 anchoring.
- Three OQs retired in scope: OQ-W1, OQ-W2, OQ-W-CALIB-1 (rolling up GAP-1, GAP-2).
- Three OQs partially informed: OQ-OC3, OQ-W-PROBE-VERSION, OQ-W8 (residual).
- POC uses synthetic `.larql` patch corpora; live-agent integration deferred.
- Output of POC is a §22.5 `CALIBRATION_RATIFICATION` submission packet, not spec-text revision.

**Constraints established:**
- §22.2 preconditions are Stage 0 operator-owned; POC does not produce them.
- Stage 1 (OQ-W2) is gating — negative result kills the POC and forces spec revision.
- Stage 2 → Stage 3 is strictly sequential; Stage 3 protocol authorship can parallelize with Stage 2 execution.
- Probe-set v1 must be stable across the calibration window — instability invalidates threshold ratification.
- Any class that fails to calibrate cleanly ships with `calibration_state: UNCALIBRATED` per §22.7 rather than holding back the packet.

**Open questions deferred (carry-forward to next session or out of POC):**
- Target model commitment status (operator decision, prerequisite for Session 2 protocol).
- Operator execution model (execute end-to-end vs. hand-off) — affects required specificity of expected-result shapes.
- Probe-set v1 authorship boundary with `validation-contract-architect` — joint corpus, separate POC scopes.
- Reference patch corpus realism: synthetic-only acceptable, or does the POC require representative agent-output samples? Affects Stage 0 prerequisite cost.

**Protocols defined this session:**
- None. Scope locked; protocol design begins next session.

**Next session candidate:** Session 2 — `memit-specialist` — OQ-W2 architecture verification protocol. Pre-condition for opening: target model commitment confirmed.
