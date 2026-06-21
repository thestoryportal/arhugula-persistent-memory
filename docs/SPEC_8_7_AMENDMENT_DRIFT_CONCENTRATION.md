# §8.7 Drift-from-Anchor — Proposed Amendment (relation-concentration-conditioned drift)

_Created 2026-06-21. **PROPOSAL** for the operator (spec owner) — not an edit to the governing spec. Derived from Track D1 (`CORPUS/22`, D-D1-1) + B1 model-size term (this loop). Addresses **OQ-W1** (spec line 1298) and the §7.2 "wrong variable" reconciliation. Advisor-vetted framing (2026-06-21): the structural amendment is D1-final; the threshold/size envelope is explicitly OPEN + conservative + tail-risk-flagged._

_**OPERATOR-REVIEWED — APPROVED AS WRITTEN (2026-06-21).** Spec owner approved the structural amendment (per-relation `max_relation_concentration_since_anchor` → worse-of `drift_tier`), the incremental-path scope, the worse-of tier composition, and deferring the numeric values to OQ-W1. The numeric §4 thresholds are now being filled by the lower-variance instrument (`docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md`, D-D1-2)._

---

## 1. The current contract (spec §8.7, verbatim refs)

§8.7 measures drift as **`edge_count_since_anchor`** — a **global, relation-agnostic** cumulative edge count (deletions count as absolute changes). It drives `drift_state.drift_tier ∈ {NOMINAL, WARNING, HARD, CRITICAL}`:
- **WARNING:** 1,500 edges since anchor → schedule compaction.
- **HARD:** 8,000 edges since anchor → suspend writes until compaction.
- §8.8: MEMIT recommended batch 2,000 edges (sub-batched).
- `drift_state` fields (IC-WE-1, D83): `edge_count_since_anchor`, `drift_tier`, `anchor_event_id`, `overlay_file_count`, `p95_latency_ratio`. TC reads it before issuing a write token.
- Counter reconciles with Ledger edge count within 5% (C-WE-1).
- **All thresholds provisional pending OQ-W1** ("Cumulative edit volume degradation threshold (model-specific)… Superset of GAP-1").

## 2. The empirical finding that forces the amendment (D1, `CORPUS/22`)

At **fixed total edit count**, held-out same-relation read corruption is driven by **how concentrated the edits are on a single relation**, NOT by the total edge count:
- Qwen2.5-3B, band [4-8], sequential in-solve AlphaEdit, fixed total-N=48: held-out `capital` top-1 falls as **capital-edit-count** rises (k24→k36→k42: ~65→42→29% on means), while the SAME total-N split across relations stays clean (D1 Phase 2: at equal total edges the diluted store is ~uncorrupted while the concentrated store is ~58pp corrupted).
- **Mechanism (§7.1):** all same-relation facts share a high-variance key direction `k_r` that rides the editable subspace AlphaEdit's null-space `P` cannot protect; concentration on one relation accumulates leakage on that direction.
- A small non-negative **cross-relation term** sits on top (two-variable law), magnitude below single-set resolution.

→ **`edge_count_since_anchor` monitors the wrong variable.** 100 edits concentrated on one relation can corrupt held-out reads while 100 diverse edits do not. The drift counter must track **per-relation edit concentration**, not (only) total edges.

## 3. Proposed structural amendment (D1-final)

**Add a per-relation concentration counter to `drift_state` and drive the drift tier from it (in addition to, not replacing, the global count).**

Proposed `drift_state` field additions (IC-WE-1):
- **`max_relation_concentration_since_anchor`** (int): the maximum, over all relations, of edges applied to a single relation since the last anchor. (Equivalently expose `relation_edge_counts_since_anchor`: a `{relation_id → count}` map; the max drives the tier.)
- **`drift_tier`** is computed as the **worse** of: (a) the existing global `edge_count_since_anchor` tier, and (b) a new **per-relation-concentration tier** keyed on `max_relation_concentration_since_anchor`.

Rationale for keeping BOTH: the global count still bounds aggregate overlay/latency drift (the `overlay_file_count`/`p95_latency_ratio` concerns are real and volume-driven); the per-relation counter captures the read-corruption mechanism the global count misses. The tier is the max (most conservative) of the two. The 5% Ledger reconciliation (C-WE-1) extends naturally: per-relation counts must sum to the global count (a stronger, free integrity check).

**This structural change is independent of the model-size question** (it follows from D1 alone) and is the item the §10 readiness checklist cannot complete without (OQ-W1 reconciliation).

## 4. The threshold values — OPEN, conservative, tail-risk-flagged (B1 size term)

The B1 model-size term (Qwen2.5-3B vs 7B, matched sequential concentration instrument, this loop) was run to decide whether the per-relation-concentration **thresholds** are model-size-invariant (transfer across deployed model) or must scale with size. **The headline result is about the INSTRUMENT, not the model:**

- **The sequential-edit corruption metric is ~50pp run-to-run nondeterministic.** The *same* fixed configuration (same model, entities, edits, harness, seed) gave 7B held-out-capital = **20.8% on one run and 70.8% on a re-run** (k36: 4.2%→41.7%) — a ~50pp swing on a bit-identical config. Mechanism **consistent with GPU/cuBLAS nondeterminism compounding over 24–48 sequential edits, but NOT verified** (the cov is bit-identical from the npz cache so P is stable; the noise most likely enters via `compute_z`/sequential accumulation, not the eigh P-construction). ([[sequential-edit-run-nondeterminism]])
- **The apparent "7B catastrophic collapse" (seed3: 4–21%) was a nondeterministic DRAW, not a real tail mode** — it did NOT reproduce on re-run of the identical config (rebounded to 42–71%). Caught by an advisor-mandated reproducibility re-run; do **not** report it as a deployment tail.
- **The size term is UNRESOLVED — a weak protective lean, within run-noise, cannot be confirmed or excluded.** With the proven-noise seed3 draw removed (and its re-run substituted), 7B leans *higher* (less corrupted) than 3B in **7/8 paired cells, mean +11.5pp** — i.e. the better-supported direction is **size-PROTECTS**, NOT the null and NOT the collapse. But +11.5pp is well below the ~50pp single-config run-noise at n=3, so it **cannot be confirmed**. Do not assert size-invariance (a noise-dominated null) either. The honest statement: *the verdict flips with one seed's noise draw* → unresolved, lean-protective, instrument-noise-limited.
- **The concentration law REPLICATES on 7B** (corruption rises with capital-edit-count on the means, both models; positive control fires; expression 100%) — robust because it is a LARGE effect (~58pp at fixed total-N in D1) that survives the run noise. **This is the real win: the §3 structural amendment (drift = per-relation concentration, not global edge-count) is NOT 3B-specific — it is model-general.** That generality is the F1 input from this loop; the threshold value is the open sub-item.

**→ §8.7 OPERATIONAL GUARDRAIL (3B, set 2026-06-21 via the lower-variance instrument — `docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md`, D-D1-2; DUAL-REVIEWED Opus advisor + gpt-5.5 cross-family, both reviews binding the framing below):**

Qwen2.5-3B, band[4-8], sequential in-solve AlphaEdit, pure-capital staircase. Held-out same-relation top-1 corruption, pooled over randomized edit-ORDERS × 24 held-out, **order-clustered bootstrap** (the Wilson UCB was retired as a *calibrated* bound — the 288 trials are clustered 12 orders × 24 shared entities, not independent; kept only as a descriptive pooled stat):

| per-relation concentration k | pooled mean% | boot-95-upper% | observed-worst-order% | drop-worst-order% |
|---|---|---|---|---|
| 1 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2 | 0.0 | 0.0 | 0.0 | 0.0 |
| 3 | 2.1 | 4.5 | 16.7 | 0.8 |
| 4 | 4.5 | 7.1 | 25.0 | 3.6 |
| 6 | 9.0 | 14.9 | 37.5 | 6.5 |
| 8 | 12.9 | 21.9 | 54.2 | 9.1 |
| 10 | 17.0 | 26.0 | 62.5 | 12.9 |
| 12 | 20.8 | 30.2 | 58.3 | 17.4 |
| 14 | 28.8 | 39.2 | 66.7 | 25.4 |

- **SHIP (the deployable guardrail): max unanchored per-relation concentration `k ≤ 2`; anchor/compact before k=3.** `k≤2` is the largest concentration with **0% corruption across all 24 edit-orders × both process runs** — the only clean, order-robust, process-stable point.
- **SCOPED EMPIRICAL OBSERVATIONS (NOT portable thresholds):** corruption onset k=3 (mean 2.1%, boot-95 4.5%); pooled warning-level (~5%) by k=4; pooled ~20% by k≈10–12. These are **order-dominated** — the leave-one-order-out column shows the single worst order drives almost all of it (k=4: 25% worst vs 3.6% without it). **Do NOT promote k=3–4 / k=10–12 as clean safety thresholds** (both reviewers); they are descriptive.
- **Per-relation count is a fail-closed SENTINEL, not the causal variable.** The driver is edit-set/ORDER geometry (key-collinearity / entity identity), not bare count — confirmed by the order-dominance. Future admission control should condition on edit-set geometry or a post-edit probe; the count is a conservative circuit-breaker only (ties §3.1 / D1 key-collinearity covariate / the field's norm-growth lead D8).
- **SCOPE (binding caveats):** (a) **3B only** — cross-model transfer OPEN (7B sequential noise needs the determinism path, now proven byte-reproducible across processes); (b) **pure-capital = anti-conservative** — real mixed inter-anchor load adds the D1 cross-relation term → true ceiling likely *lower*; mixed-load **untested**; (c) **incremental/inter-anchor path only** (deployment is batch/Genesis, A1-clean — this guardrail governs the A3-parked runtime path); (d) seed-3 held-out (a coarser sweep showed seed-2 more toxic → across-held-out-seed variance undersampled, conservative direction lower). All four push the ceiling *lower*, reinforcing `k≤2`.
- **Instrument finding:** within-process repeats are SD=0 on 3B; the real variance axes are **across-process** (cuBLAS algorithm selection compounding over the sequential chain — determinism fixes it) **and edit-ORDER** (intrinsic, the dominant uncertainty, not GPU noise). The original "50pp run-to-run noise" was 7B-specific + across-process; on 3B the binding uncertainty is edit-order.
- **Recommended next (not blocking the guardrail; all push lower):** mixed-load smoke at k=1–3; repeat low-k with the more-toxic held-out seed; ≥3 held-out seeds; cluster bootstrap already done. Artifacts: `results/d1_threshold_lowk_3b_s3{,_lowextra}.json`, `results/d1_threshold_curve_3b_*.json`, `results/d1_instrument_variance_diagnostic_3b_{nondet,det}.json`; reviews `logs/codex_review_threshold_{,FINAL_}OUT.log`.

1. The per-relation-concentration **operational guardrail is now SET on 3B (`k≤2`, above)** but remains **OPEN for cross-model transfer (OQ-W1)** — **NOT shown to transfer across model size** (the size effect is below the sequential instrument's run noise; needs the determinism path on 7B).
2. Set the per-relation threshold **conservatively** (well below the corruption onset observed on the smallest deployed model). The high run-to-run variance of the *sequential* path is itself an argument for conservatism — but note the deployment path is **batch/Genesis (A1-clean)**, so per-relation drift mainly governs the *incremental/runtime* path (A3-parked).
3. The robust monitorable may need the **key-collinearity of the specific edit set** (the D1 covariate), not just the per-relation count — next refinement (D1 §3.1 / D7).
4. **Compaction is the mitigation**: batch/Genesis re-compile (§8.10, D62) is clean (A1), so a conservative per-relation WARNING should schedule compaction early.
5. **A lower-variance instrument is required to set a quantitative per-relation threshold** — more held-out entities, deterministic-algorithm runs (`torch.use_deterministic_algorithms`), and/or measuring on the batch path; the sequential single-run metric is too noisy (~50pp) for fine threshold calibration. This is the concrete next step the F1 numeric threshold blocks on.

## 5. Honest scope / what is NOT claimed
- Structural amendment (per-relation counter): **promotable** (D1 directional-robust + B1 cross-model replication).
- Quantitative thresholds / a fitted capacity law: **NOT delivered** — 2 model points (3B, 7B) on a ±15–23pp-variance instrument is a **directional size term, underpowered**, not a fitted law (needs ≥3 matched points incl. 8B + more seeds + collinearity covariate). Per [[calibrate-confidence-mechanics-vs-contracts]] / [[pass-label-not-equal-promotable-claim]].
- Size-invariance is **NOT** claimed (a noise-dominated null). Size-protection is **NOT confirmed but is the better-supported lean** (7/8 paired cells favor 7B, mean +11.5pp, after removing the proven-noise seed3 draw) — unresolvable under ~50pp run-noise at n=3. The honest verdict is **UNRESOLVED, lean-protective**; the apparent reversal/collapse was a single non-reproducible noise draw, not a real effect.

## 6. Artifacts / provenance
- D1: `docs/D1_CAPACITY_LAW_PREREG.md`, `results/d1_{predictor_map,concentration_sweep,dose_response}_result.json`, `CORPUS/22`.
- B1: `docs/B1_SIZE_TERM_PREREG.md`, `experiments/track_b/b1_size_dose_response.py`, `results/b1_{3b,7b}_dose_response_result.json` (+ `_seeds123` backups, seeds345/recheck pending).
- Engine `kmeng01/memit` UNMODIFIED (SHA 5c0c706a…); LAW#5 inertness gates PASSED (3B |Δ|=0.0002/0.0003, 7B |Δ|=0.0000/0.0001); harness P-construction via eigh (symmetric-PSD ⇒ identical projector) + bit-exact diagonal-add VRAM rewrite (proven inert).
- Decision `D-B1-2` (size term). Folds into `CORPUS/22` + runbook §0.3/§5.2/§7.2/§8 D1.
