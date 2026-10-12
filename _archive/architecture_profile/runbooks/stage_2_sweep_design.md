# Stage 2 Sweep Design — Llama-3.1-8B MEMIT Hparam Calibration

> **Authoring session:** S2.9 (Combined v1.4 hardening + Stage 2 sweep design)
> **Predecessor:** Stage 1 SECT v1.3 execution at S2.8 — VERDICT FAIL on consistency aggregate (0/9 trials; provisional band; calibration scope)
> **Consumer session(s):** S2.10+ Stage 2 sweep execution (multi-config; per-config Stage-1-form trial protocol)
> **Target environment:** RunPod RTX 4090 24 GiB (sm_89); NV `large_amethyst_wolverine`
> **Target model:** `meta-llama/Llama-3.1-8B` (FP16; revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`)
> **Active patch state:** P-1, P-2, P-4, P-5, P-6, P-7 + Pad-Token + Copy-Unmount (per `memit-patches-canonical.md` v2.4.1; conditional P-3', Device-Map not active)
> **Specialists:** memit-specialist (primary — hparam space scoping); validation-contract-architect (success criteria authoring; band review per OQ-PROBE-2); state-consistency-theorist (NV/SSD partitioning per OQ-S28-6); framework-spec-writer (this artifact)
>
> **Version:** v1.0 (initial Stage 2 design; PROVISIONAL pending S2.10 entry decision)
>
> **Status:** AUTHORED at S2.9 close. Ratification path:
> - **PROVISIONAL** at S2.9 close (this version)
> - **RATIFIED-EMPIRICALLY** when at least one sweep configuration achieves Stage 1 PASS verdict against post-v1.4 NV state (Stage 2 PASS criterion per §5)
> - **DEFECTIVE-IN-FIELD** if first execution of the selected reduction strategy surfaces sweep-design defects (e.g., bound mis-scoping, configuration encoding error)

---

## 1. Sweep matrix dimensions

The Stage 2 sweep targets three MEMIT hparams that are jointly responsible for edit-strength under the Stage 1 trial protocol. Each dimension is anchored to the S2.8 empirical forensic signal (per `session_2_8_summary_block.md` §8.3, §8.4):

| Hparam | S2.8 value | Sweep levels (4-level; 64-config full grid) | Anchor |
|---|---|---|---|
| `v_lr` | `0.5` | `0.5` / `1.0` / `1.5` / `2.0` | Loss trajectories converge to `P(target_new) ≈ 1e-5` at step 25 with no plateau; >10⁴× lift needed to clear the 0.5 consistency band threshold. Higher learning rate is the direct lever to compress the trajectory into the available step budget. |
| `v_num_grad_steps` | `25` | `25` / `50` / `100` / `200` | Loss still descending at step 25 (no plateau observed in S2.8 trial JSONs). Larger step budget allows the optimizer to reach the threshold without changing other hparams. Geometric scaling (×2 / ×4 / ×8) chosen for log-spaced wall-time scaling. |
| `mom2_update_weight` | `15000` | `15000` / `17500` / `20000` / `25000` | upd_norm magnitudes 0.27–0.77 at edit layers vs orig_norm ~88 (< 1% relative). FFN write under-powers the consistency target. Linear scaling between bounds chosen because the relationship between this weight and the resulting upd_norm magnitude is approximately linear (per MEMIT solve form `Δ = K K^T (mom2 + λI)^{-1}`); geometric scaling would over-explore the high end. |

**Layers fixed at `[4, 5, 6, 7, 8]`** per Llama-3.1-8B reference hparams (`meta-llama/Llama-3.1-8B.json`). Layer-set sweep is OUT OF SCOPE for Stage 2 — it is a corpus-level decision (`fact_token = subject_last`, mid-band layer choice) that would require fact-locality probing distinct from this calibration sweep.

**Other hparams fixed at S2.8 values** (`clamp_norm_factor=0.75`, `kl_factor=0.0625`, `v_loss_layer=31`, `v_weight_decay=0.5`, `mom2_n_samples=100000`, `fact_token="subject_last"`). Stage 2 calibrates the three jointly-edit-strength hparams only; secondary hparams remain at upstream-MEMIT defaults.

**Full grid cardinality:** 4 × 4 × 4 = **64 configurations**.

---

## 2. Reduction strategy selection

### 2.1 Decision

**Latin Hypercube Sampling at n=16** is selected as the Stage 2 reduction strategy. Justification:

| Strategy | Configs | Wall-time @ 9-trial protocol | Statistical informativeness | Verdict |
|---|---|---|---|---|
| Full grid | 64 | ~34 hr | Maximal — every (v_lr, v_num_grad_steps, mom2_update_weight) corner explored | REJECTED — operationally costly; the dominant signal in S2.8 (monotone loss-trajectory shape, near-linear upd_norm scaling) suggests the response surface is smooth and near-additive, making corner exhaustion over-investment. |
| **Latin hypercube n=16** | **16** | **~8.5 hr** | High — every level of each hparam appears exactly 4 times; main-effect estimates statistically identifiable; interaction effects partially identifiable | **SELECTED** |
| One-at-a-time (OAT) | 10 | ~5.3 hr | Low — main effects only; cannot detect hparam interactions | REJECTED — the hparams are not orthogonal in their effect on edit strength (e.g., higher `v_lr` may require fewer steps to reach the same trajectory point, or may overshoot at high `mom2_update_weight`). OAT misses interaction structure that drives the PASS/FAIL boundary. |
| Bayesian optimization (sequential) | ~10–15 (variable) | ~5–8 hr; sequential | High under good prior; risk of getting stuck in local optima with no PASS configs | REJECTED for v1.0 — the empirical prior at S2.9 is a clear failure boundary at S2.8 settings but no successful PASS observation; sequential acquisition without an anchor PASS is exploratory in a regime where exploitation has nothing to exploit. Reconsidered for v1.1 if Stage 2 sweep produces a PASS anchor. |

### 2.2 LHS construction

The 16-point LHS is constructed by partitioning each dimension into 4 strata (matching the 4-level grid) and drawing one configuration from each (stratum index, stratum index, stratum index) Latin-square slice such that each stratum appears exactly 4 times across the 16 points.

A canonical LHS-16 plan derived from the 4×4×4 grid:

| Config ID | `v_lr` | `v_num_grad_steps` | `mom2_update_weight` |
|---|---|---|---|
| L01 | 0.5 | 25 | 15000 |
| L02 | 0.5 | 50 | 20000 |
| L03 | 0.5 | 100 | 25000 |
| L04 | 0.5 | 200 | 17500 |
| L05 | 1.0 | 25 | 20000 |
| L06 | 1.0 | 50 | 15000 |
| L07 | 1.0 | 100 | 17500 |
| L08 | 1.0 | 200 | 25000 |
| L09 | 1.5 | 25 | 25000 |
| L10 | 1.5 | 50 | 17500 |
| L11 | 1.5 | 100 | 15000 |
| L12 | 1.5 | 200 | 20000 |
| L13 | 2.0 | 25 | 17500 |
| L14 | 2.0 | 50 | 25000 |
| L15 | 2.0 | 100 | 20000 |
| L16 | 2.0 | 200 | 15000 |

Each level of each hparam appears exactly 4 times (stratification preserved). Configurations are intended to be executed in the order listed but may be permuted by the operator without affecting the sweep's statistical properties.

**Anchor inclusion.** L01 (the S2.8 baseline configuration) is retained in the LHS plan as the negative-control anchor; if Stage 2 v2 execution reproduces the S2.8 0/9 consistency FAIL at L01, the architectural-axis anchor inheritance from S2.8 is empirically re-confirmed within Stage 2.

### 2.3 Tradeoffs accepted

| Cost | Benefit |
|---|---|
| 75% reduction in corner coverage vs. full grid | 4× reduction in wall-time; 4× reduction in NV pressure; preserves main-effect identifiability |
| LHS does not guarantee corner inclusion (e.g., the (2.0, 200, 25000) "all-strong" corner is not in this plan; (1.5, 200, 25000) at L08 is the closest neighbor) | The S2.8 forensic signal points to a monotone direction in (strength × budget) space; corners are unlikely to be where the PASS boundary lies. If sweep results contradict this, an LHS-supplement at v1.1 can target specific corners. |
| Interaction-effect estimates have lower power than full grid | Acceptable for v1.0; promotion path to full grid OR Bayesian optimization at v1.1 if v1.0 produces an inconclusive result |

---

## 3. Per-configuration trial protocol

### 3.1 Decision

**Reduced trial protocol — 3 facts × 1 replicate = 3 trials per configuration** is selected for Stage 2 sweep v1.0.

| Option | Trials per config | Wall-time per config @ Stage 1 amortized rate | Total wall-time (16 configs) |
|---|---|---|---|
| Full Stage 1 form (3 × 3) | 9 | ~3 min (S2.8 amortized; cache-hit warm) | ~48 min × 16 = **~13 hr** |
| **Reduced (3 × 1)** | **3** | **~1 min (cache-hit warm; 1 cold-start trial)** | **~5–8 hr (incl. 1 cold start per config)** |
| Single-fact (1 × 1) | 1 | ~30 s | ~10 min total | REJECTED — single-fact trials cannot identify orthographic / fact-locality variance per OQ-S28-5 (cfb-003 multi-token subject risk). |

### 3.2 Rationale

The reduced 3 × 1 protocol is selected because:

1. **Replicate variance was zero at S2.8.** All three replicates of every fact produced identical verdicts and identical loss trajectories (torch_seed=0; deterministic per `IC-S24-4` trial protocol). The replicate dimension contributes no new information at the consistency axis under deterministic seeding. Replicates' value is in detecting non-determinism — already absent at S2.8.
2. **Fact dimension carries informativeness.** All three fact_ids (`cfb-001`, `cfb-002`, `cfb-003`) are retained because they exercise distinct subject-token regimes: cfb-001 (`Michael Jordan`) and cfb-002 (`Lionel Messi`) are 2-token subjects; cfb-003 (`Wayne Gretzky`) is a 5-token subject anchored to a low-information `subject_last` token (per OQ-S28-5). Per-fact verdict spread is informative for the PASS-boundary location.
3. **Cost ratio.** 3× wall-time savings per config; 16-config sweep fits within a single multi-hour session envelope rather than spanning multiple days.

### 3.3 Promotion path to full Stage 1 form

If a Stage 2 v1.0 configuration achieves the Stage 2 PASS criterion (per §5) on the reduced protocol, that configuration is promoted to a full Stage 1 SECT v2 execution — 3 facts × 3 replicates = 9 trials — to confirm replicate consistency before declaring the configuration the calibrated Stage 1 hparam set. This is a separate execution session (S2.11 candidate or later).

---

## 4. NV/SSD overlay artifact partitioning (OQ-S28-6 closure)

### 4.1 Per-configuration overlay artifact footprint

| Artifact class | Per-trial size | Per-config (3 trials) | Per-sweep (16 configs) |
|---|---|---|---|
| `edited.pt` (overlay) | ~550 MB (5 layers × ~110 MB FP16 down_proj) | ~1.65 GB | ~26 GB |
| `original.pt` (overlay) | ~550 MB | ~1.65 GB | ~26 GB |
| Trial verdict JSON | ~50 KB | ~150 KB | ~2 MB |
| Per-config aggregate JSON | ~5 KB | ~5 KB | ~80 KB |
| **Total per-sweep overlay footprint** | — | **~3.3 GB / config** | **~52 GB / sweep** |

NV pre-sweep target utilization (post-S2.8 hygiene): ~53% (47 GB free of 100 GB quota). 52 GB sweep footprint exceeds free space by 5 GB; sustained NV hosting of the full sweep is infeasible.

### 4.2 Partitioning policy

**Per-configuration overlay artifacts MUST migrate to SSD mirror after per-config verdict emission.** NV retains only:

| NV-resident (durable) | SSD-resident (after per-config close) |
|---|---|
| Per-trial verdict JSON (×3 per config) | `edited.pt` (×3 per config) |
| Per-config aggregate JSON | `original.pt` (×3 per config) |
| Sweep aggregate JSON (final) | Per-config NV partition fully reclaimed after migration |
| Reproducibility manifest entry | — |

**Migration trigger.** After each configuration's Cell 11 NV inventory verification PASS (using v1.4 form including the SHA equality gate per OQ-S28-4), the operator runs an `rsync` from `/workspace/stage_1_sect/overlays/<config_id>/` to the SSD mirror, then `rm -rf` the NV-side overlay directory. Trial verdict JSONs and aggregate JSONs remain on NV.

**NV residency budget per sweep:** ~3.3 GB peak (one config in flight) + ~80 KB persistent (verdict + aggregate JSONs across all 16 configs). Drops to ~3.3 GB peak vs. ~52 GB sustained — well within the post-hygiene NV envelope.

### 4.3 Cross-medium consistency

Per `D-S24-14` (NV write discipline + SSD mirror sync convention) and `IC-S25-1` (bridge cache provenance contract — archived not deleted):

| Constraint | Stage 2 sweep binding |
|---|---|
| NV is canonical for verdict JSONs | Verdict JSONs MUST remain on NV until reproducibility manifest update completes for the sweep |
| SSD mirror is durable for overlays | Overlays MUST be present on SSD before NV deletion; rsync must complete with non-zero copy and zero error before `rm -rf` proceeds |
| Recovery on SSD-side loss | Operator may re-execute any specific configuration against the same Stage 1 SECT v2 runbook; overlay reproduction is deterministic given (config, fact, replicate, torch_seed) |

### 4.4 Closure of OQ-S28-6

OQ-S28-6 (NV utilization sustainability for Stage 2 sweep) is CLOSED by §4.2 and §4.3 above. The NV/SSD partitioning policy makes Stage 2 sweep operationally feasible at any LHS reduction strategy; the policy is independent of the specific sweep cardinality.

---

## 5. Stage 2 PASS criteria

### 5.1 Per-configuration verdict

Each Stage 2 configuration produces a per-configuration verdict against the four Stage 1 acceptance criteria (per `IC-S24-4` and `aggregate_verdict.json` schema), evaluated under the reduced 3-trial protocol:

| Criterion | Threshold | Notes |
|---|---|---|
| Consistency | ≥ 2/3 PASS | Provisional band per `D-S24-10`; PROVISIONAL retained from Stage 1 |
| Generalization | ≥ 2/3 PASS | Provisional band; flag at `< 0.05` drift threshold |
| Specificity (post-edit) | ≥ 2/3 PASS | Provisional band; flag at `< 0.05` drift threshold |
| Specificity (post-unmount) | ≥ 2/3 PASS | Provisional band |
| Unmount band | 3/3 PASS at `\|drift\| < 1e-4` | HARD per `IC-S23-4`; not subject to recalibration |

A configuration's per-config verdict is PASS iff ALL FIVE criteria PASS at their reduced-trial thresholds.

### 5.2 Stage 2 sweep PASS criterion

**Primary.** The sweep PASSes iff **at least one configuration** in the LHS-16 plan achieves a per-config PASS verdict per §5.1.

**Sweep verdict file:** `/workspace/stage_2_sweep/sweep_verdict.json` (analogous to Stage 1 `aggregate_verdict.json`; one entry per configuration plus an aggregate `sweep_pass` boolean).

### 5.3 Secondary: per-config trade-off curve (optional analysis)

A secondary analysis (not gating sweep PASS) characterizes the configurations that PASS consistency but FAIL specificity bleed (drift ≥ 0.05 from baseline). This identifies the "calibration corridor" — the (v_lr, v_num_grad_steps, mom2_update_weight) sub-region where edit strength is sufficient for consistency without bleeding specificity. The corridor anchors S2.11+ refinement (e.g., LHS-supplement around the corridor; or full-Stage-1-form re-execution of the corridor configurations).

### 5.4 Decidability requirement

Per the kickoff §2.4 authoring acceptance gate:

> Stage 2 PASS criterion is decidable from sweep output JSONs (no operator interpretation required).

The §5.1 + §5.2 criteria are mechanical: each per-config verdict is a deterministic AND of five threshold predicates against the per-config aggregate JSON; the sweep verdict is a deterministic OR over per-config verdicts. No operator interpretation is required.

---

## 6. Wall-time and cost projection

### 6.1 Per-configuration wall-time breakdown

| Phase | Wall time per config |
|---|---|
| Cell 0 + 0-VERIFY + 0.6 + 0.7 (one-time per pod lifecycle) | 0 (amortized across sweep) |
| Cells 1–8 (pre-flight; per-config because hparams change at Cell 4) | ~3–4 min |
| Cell 9 trial loop (3 trials × ~15s warm; 1 cold-start trial at ~32s) | ~1 min |
| Cells 10–11 (verdict + NV inventory) | ~30 s |
| Cell 11.5 (overlay migration to SSD; OQ-S28-6 partitioning) | ~30 s |
| **Per-config total** | **~5 min** |

### 6.2 Sweep wall-time projection

| Strategy | Configs | Per-config wall-time | Sweep total |
|---|---|---|---|
| LHS-16 with reduced 3×1 protocol (selected) | 16 | ~5 min | **~80 min (~1.5 hr)** |
| LHS-16 with full Stage 1 form (3×3) | 16 | ~13 min | ~3.5 hr |
| Full grid (64) with reduced 3×1 protocol | 64 | ~5 min | ~5.5 hr |
| Full grid (64) with full Stage 1 form (3×3) | 64 | ~13 min | ~14 hr |

The selected configuration (LHS-16 with reduced 3×1 protocol; ~1.5 hr wall-time) fits within a single multi-hour session envelope.

### 6.3 Cost projection

RTX 4090 RunPod pricing reference (operator-side; not authoritative): ~$0.40–$0.60 / GPU-hr. Sweep cost @ 1.5 hr ≈ $0.60–$0.90 per sweep execution. Includes ~30 min envelope for orphan-kernel recovery + NV hygiene per S2.8 forensic anchor.

---

## 7. Schedule integration

### 7.1 Single-session execution feasibility

The selected LHS-16 + reduced-trial-protocol + ~1.5 hr wall-time fits within a single Workstream 1 session. Sweep execution can be a single-session deliverable (S2.10 if Candidate B selected) or part of a combined session that also produces sweep-result analysis.

### 7.2 Multi-session split (optional)

If the operator prefers to bound per-session wall-time more tightly, the sweep splits cleanly along the LHS row index:

| Session | Configurations | Wall-time |
|---|---|---|
| S2.10a | L01–L08 (first 8 LHS configs) | ~40 min |
| S2.10b | L09–L16 (second 8 LHS configs) | ~40 min |
| Aggregate | — | ~80 min total + per-session orientation overhead |

No structural reason to split unless the operator schedule demands shorter sessions. Default recommendation: single-session execution.

### 7.3 Operator schedule input — DEFERRED

Operator schedule fit is OUT OF SCOPE for this design document. Schedule integration is operator-side per the project instructions ("Schedule tracking for Workstream 1 is operator-side, not encoded in any project KB artifact").

---

## 8. Probe band posture (provisional retention)

Per kickoff §2.3, all probe bands ratified at S2.8 are RETAINED for Stage 2:

| Band | Status | Retention rationale |
|---|---|---|
| Consistency `P(target_new) > 0.5` post-edit | Provisional (D-S24-10); FAILED uniformly at S2.8 | OQ-PROBE-2 closure path is hparam-side calibration, NOT band recalibration. The S2.8 forensic signal (loss converges to 1e-5 vs. 0.5 threshold) shows the gap is in edit strength, not in band threshold appropriateness. |
| Generalization drift `< 0.05` from baseline | Provisional (D-S24-10); PASSED 9/9 at S2.8 | RETAIN; flag for re-evaluation at Stage 2 PASS configs (higher edit strength may produce drift > 0.05 → specificity bleed signal per §5.3). |
| Shared-specificity drift `< 0.05` from baseline | Provisional (D-S24-10); PASSED 9/9 at S2.8 | RETAIN; same flag as generalization. |
| Unmount band `\|drift\| < 1e-4` | HARD per IC-S23-4; PASSED 9/9 at S2.8 at `\|drift\|=0.00` | RETAIN; HARD band; not subject to recalibration. Sweep will not produce drift > 0 unless P-7 + Copy-Unmount semantics regress, which is unrelated to the calibration sweep dimensions. |

OQ-PROBE-2 closure is BLOCKED on Stage 2 sweep PASS — bands cannot be ratified until at least one config produces a workable PASS configuration that the bands correctly classify. Stage 2 v1.0 is the empirical step toward OQ-PROBE-2 closure.

---

## 9. Authoring acceptance gates — disposition at S2.9 close

Per kickoff §2.4 authoring acceptance gates:

| Gate | Required output | Disposition at S2.9 |
|---|---|---|
| Sweep matrix completeness | All 3 dimensions specified with explicit level values; 64-config full grid enumerated OR reduction strategy explicitly defined | **PASS** — §1 enumerates 4 levels per dimension; §2 specifies LHS-16 with explicit per-config table |
| Reduction strategy decidability | Selection rationale tied to wall-time budget AND statistical informativeness | **PASS** — §2.1 provides four-way comparison; §2.3 documents tradeoffs accepted |
| Success criteria definition | Stage 2 PASS criterion is decidable from sweep output JSONs | **PASS** — §5.1 + §5.2 define mechanical AND-of-thresholds + OR-over-configs predicates; §5.4 explicitly confirms decidability |
| NV/SSD partitioning closure | OQ-S28-6 explicitly closed; per-config artifact retention policy documented | **PASS** — §4.2 + §4.3 + §4.4 close OQ-S28-6 |
| Wall-time / cost projection | Per-config + per-strategy + total wall-time documented | **PASS** — §6.1 + §6.2 + §6.3 |

All five authoring acceptance gates PASS at S2.9 close. v1.0 is RATIFIED for authoring acceptance; empirical ratification is gated on Stage 2 execution (S2.10 candidate B) or selection of a reduced-config sub-sweep (S2.10 candidate A).

---

## 10. Open questions

### 10.1 New OQs surfaced at v1.0 authoring

| OQ ID | Description | Resolution path |
|---|---|---|
| **OQ-S29-1** (NEW) | LHS-16 plan corner-coverage gap. The all-strong corner (v_lr=2.0, steps=200, weight=25000) is not in the LHS plan; if the plan converges to a near-PASS region near that corner, an LHS-supplement targeting the corner is needed. | Empirical at Stage 2 sweep close — analyze sweep results' direction-of-improvement; if it points toward an unexplored corner, author LHS-supplement at v1.1. |
| **OQ-S29-2** (NEW) | Specificity bleed under stronger edit settings. Generalization + specificity 9/9 at S2.8 baseline does not guarantee the bands hold at Stage 2 PASS configurations. | Empirical at sweep close — §5.3 secondary analysis identifies the calibration corridor; if no corridor exists (i.e., all consistency-PASS configs fail specificity), corpus-level intervention is needed (OQ-S28-5 routing; probe-set v1.2 corpus revision). |
| **OQ-S29-3** (NEW) | Replicate determinism under different `v_lr` levels. S2.8 confirmed determinism at v_lr=0.5 with torch_seed=0; sweep configs at v_lr=2.0 may surface non-determinism via numerical instability in the v-update step. | Empirical at sweep close — if any per-config trial shows non-zero replicate variance under torch_seed=0 + identical hparams, the reduced 3×1 protocol's assumption of replicate equivalence breaks for that config; promotion path requires full 3×3 form for that config. |

### 10.2 OQs activated by Stage 2 design

| OQ ID | S2.9 disposition | Resolution path |
|---|---|---|
| OQ-S25-3 (`mom2_update_weight=15000` provisional) | ACTIVATED — Stage 2 sweep dimension | Closes via Stage 2 PASS configuration's `mom2_update_weight` value |
| OQ-S25-4 (`v_lr=0.5` provisional) | ACTIVATED — Stage 2 sweep dimension | Closes via Stage 2 PASS configuration's `v_lr` value |
| OQ-PROBE-2 (band calibration) | ACTIVATED — bands retained PROVISIONAL pending Stage 2 PASS | Closes when a PASS config validates band correctness; or surfaces band recalibration need if no config PASSes |

### 10.3 OQs explicitly out of scope for v1.0

| OQ ID | Description | Routing |
|---|---|---|
| OQ-S28-5 (cfb-003 multi-token subject orthographic risk) | Probe-set v1.2 / corpus revision scope; not blocking Stage 2 sweep | Post-Stage-2 corpus revision session (S2.10 Candidate C if selected) |
| Layer-set selection (`layers = [4,5,6,7,8]`) | Fixed at upstream-MEMIT default; not in Stage 2 sweep | Stage 3+ if sweep results warrant |
| Subject token regime (multi-token vs. single-token) | Corpus design scope per `cfb-v1.yaml` | Out of v1.0; revisited if OQ-S28-5 escalates |

---

## 11. Non-goals (explicit)

This sweep design v1.0 deliberately does NOT:

- **Authorize a runtime sweep execution implementation.** Stage 2 sweep execution is a future session deliverable; this document defines the design parameters (matrix, strategy, criteria, partitioning) without prescribing a specific runtime executor (per project mode: spec/brainstorm sessions do not produce runtime code).
- **Recalibrate probe bands.** Per §8, OQ-PROBE-2 closure path is hparam-side; bands are retained as-is for Stage 2.
- **Sweep MEMIT layer selection.** Layer set fixed at `[4,5,6,7,8]`; sweep targets only the three jointly-edit-strength hparams.
- **Address corpus design.** OQ-S28-5 and probe-set v1.2 are routed to corpus-level sessions, not this calibration sweep.
- **Replace Stage 1 SECT v2 execution.** Stage 1 SECT v2 against post-v1.4 NV state is a separate session. A Stage 2 PASS configuration is promoted via Stage 1 SECT v2 (full 3×3 form) before being declared the calibrated Stage 1 hparam set.
- **Define multi-corpus sweeps.** Stage 2 v1.0 sweep is bound to `cfb-v1.yaml v1.1 stage_1_eligible_facts` (cfb-001, cfb-002, cfb-003). Multi-corpus calibration is a Stage 3+ scope.

---

## 12. Carry-forward to S2.10 entry

| Item | State at S2.10 entry |
|---|---|
| Stage 2 sweep design | v1.0 RATIFIED for authoring acceptance |
| Sweep matrix | LHS-16 plan in §2.2 |
| Per-config trial protocol | Reduced 3×1 (§3) |
| PASS criteria | §5.1 + §5.2 |
| NV/SSD partitioning | §4.2 (operator-side per-config rsync + delete) |
| OQ-S28-6 | CLOSED (per §4.4) |
| Active OQs forwarded | OQ-S29-1, OQ-S29-2, OQ-S29-3 (sweep-execution scope); OQ-S25-3, OQ-S25-4, OQ-PROBE-2 (calibration scope; resolution path through Stage 2 sweep) |
| Predecessor runbook | `stage_1_sect_runbook.md v1.4` (PROVISIONAL per §1.5) |
| Active patches | P-1, P-2, P-4, P-5, P-6, P-7 + Pad-Token + Copy-Unmount (per `memit-patches-canonical.md v2.4.1` or v2.5 if C-S28-1 ratified at S2.9) |

---

*End of Stage 2 Sweep Design v1.0.*
