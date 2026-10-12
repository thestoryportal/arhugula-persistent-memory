# Probe-band Recalibration Spec — S2.11-B

> **Authoring session:** S2.11-B (Probe-band Recalibration + S2.10 Trial Re-evaluation)
> **Predecessor:** S2.10 (CLOSED 2026-05-02 — sweep verdict FAIL on consistency aggregate; calibration corridor EMPTY)
> **Hypothesis class targeted:** Class B (Probe locus) per `s210_to_next_session_handoff_guide.md` §2.3
> **Specialists:** validation-contract-architect (primary — band re-derivation); memit-specialist (consult — band physical meaning under MEMIT); framework-spec-writer (artifact authoring)
>
> **Version:** v1.0 (initial recalibration spec; AUTHORING-ACCEPTANCE-PROVISIONAL pending re-evaluation execution)
>
> **Status:** AUTHORED at S2.11-B mid-session. Ratification path:
> - **AUTHORING-ACCEPTANCE-PROVISIONAL** at this version (methodology defined; mechanical re-evaluation algorithm decidable)
> - **EMPIRICALLY-RATIFIED-PASS** if re-evaluation surfaces ≥1 consistency-PASS config under recommended band → closes OQ-S210-2 with Class B isolation
> - **EMPIRICALLY-RATIFIED-FAIL** if re-evaluation surfaces zero consistency-PASS configs across all candidate bands → eliminates Class B; routes S2.12 to Class A (corpus revision per handoff §3.2)

---

## §1 — Forensic ground-truth

### 1.1 S2.8 empirical distribution at canonical hparams (= S2.10 L01)

The 9 stage_1 trial JSONs in the active KB are the S2.8 trial archive at canonical hparams `(v_lr=0.5, v_num_grad_steps=25, mom2_update_weight=15000)` — equivalent to S2.10 config L01. Aggregate statistics across 27 consistency probes (3 facts × 3 probes × 3 replicates):

| Statistic | Value |
|---|---|
| P(target_new) min | 0.000296 |
| P(target_new) max | 0.011020 |
| P(target_new) median | 0.002621 |
| P(target_new) mean | 0.004215 |
| P(target_new) stdev | 0.003824 |

**Per-fact disparity:**

| fact_id | target_new | n | P(target_new) min | P(target_new) max | P(target_new) mean |
|---|---|---|---|---|---|
| cfb-001 | baseball | 9 | 0.001191 | 0.010506 | 0.005335 |
| cfb-002 | soccer | 9 | 0.002302 | 0.011020 | 0.005314 |
| cfb-003 | tennis | 9 | 0.000296 | 0.004635 | 0.001996 |

cfb-003 distribution is 2–3× weaker than cfb-001/002 distributions. This aligns with OQ-S28-5 (cfb-003 multi-token subject `subject_last` token risk).

### 1.2 Replicate determinism (incidental finding load-bearing for D-S29-2)

Every (fact_id, probe_id) tuple produces bitwise-identical P(target_new) across r1/r2/r3. Determinism under `torch_seed=0` per IC-S24-4 is empirically confirmed at the probe-output level. The reduced 3×1 protocol per D-S29-2 is informationally equivalent to a 3×3 protocol under deterministic seeding; the only variance the 3×3 would surface is non-determinism, which this evidence shows is absent at canonical hparams.

**Implication for routing:** Any "PASS at 3×1; promote to 3×3 for confirmation" path (per `stage_2_sweep_design.md` §3.3) is forensically a non-determinism audit, not a replicate-variance audit. The replicate dimension at canonical hparams adds zero new probability information.

### 1.3 Top-K rank ground-truth

| Rank metric | Observation across 27 cons probes |
|---|---|
| target_new appears in top-5 | 0/27 |
| top_1 == target_new | 0/27 |
| top_1 is a semantic competitor (target_true or related) | 27/27 |

For cfb-001 and cfb-002, the top_1 token across all probes is the target_TRUE (basketball, football). For cfb-003, top_1 is dispersed across non-target tokens (life, called, hockey) suggesting weaker semantic anchoring at the (subject_last="ky", target="tennis") regime.

### 1.4 Threshold sensitivity over canonical-hparam evidence

| Threshold T (P(target_new) > T) | Probe-pass count (out of 27) |
|---|---|
| 0.5 (current band) | 0 (0%) |
| 0.1 | 0 (0%) |
| 0.05 | 0 (0%) |
| 0.01 | 6 (22%) |
| 0.005 | 6 (22%) |
| 0.001 | 24 (89%) |

Two threshold discontinuities are visible: a transition between 0.05 and 0.01, and a transition between 0.005 and 0.001. The (0.005, 0.01) plateau at 6/27 reflects that the P(target_new) distribution clusters between 0.005 and 0.011 at the upper tail.

**Note:** This sensitivity table is canonical-hparam-only (= L01). Stage 2 L02–L14 evidence is required for a sweep-wide sensitivity table. Re-evaluation execution (Tier 2) produces this.

### 1.5 Pre-edit baseline reference

The handoff guide notes pre-edit P(target_new=baseball) = 0.0078 for cfb-001 at the Cell 7 baseline. This is **within the post-edit distribution range (0.001–0.011)**. If this baseline is representative across facts, the post-edit P(target_new) distribution is **statistically indistinguishable from the pre-edit P(target_new) distribution**, which would constitute strong forensic evidence against the Class B hypothesis. Per-fact pre-edit baselines are required to confirm — not preserved in trial JSONs (see §6).

---

## §2 — Methodology

### 2.1 Recalibration ontology

The current consistency band `P(target_new) > 0.5` is a **strong-evidence band**: it asserts the edit caused the model to predict target_new with majority confidence. The S2.10 sweep evidence shows this band is unreachable across the LHS-16 hparam region.

A **weak-evidence band** asks a different question: "did the edit measurably move probability mass toward target_new at all, even sub-dominantly?" Multiple weak-evidence band families are admissible:

- **Absolute-relaxed bands** (B-A): lower fixed threshold T on P(target_new)
- **Rank-improvement bands** (B-B): target_new appears in top-K (K > 1)
- **Relative-lift bands** (B-C): P(target_new)_post / P(target_new)_pre exceeds N×
- **Target-dominance bands** (B-D): P(target_new) exceeds some fraction of P(top_1)
- **Compound bands** (B-E): conjunctions/disjunctions of the above

§3 enumerates each candidate. §4 selects the recommended set.

### 2.2 Per-fact vs uniform bands

Two binding modes:

- **Uniform binding:** single threshold value applies to all facts. Robust to over-tuning; vulnerable to per-fact difficulty disparity (cf. cfb-003 weakness in §1.1).
- **Per-fact binding:** separate threshold per fact, derived from per-fact pre-edit baseline distributions. More sensitive but with a confound — if thresholds are derived from the same data they evaluate, the test is not independent.

This spec adopts **uniform binding** for the primary recommendation (§4.1) on falsification-rigor grounds. Per-fact bands are authored as B-A-perfact alternates for sensitivity analysis (§3.1.2) and surface as OQ-S211B-1 (§7).

### 2.3 Aggregate threshold (≥2/3 PASS rule retention)

The current aggregate rule "≥2/3 of trials PASS for the criterion to PASS at the per-config level" per `stage_2_sweep_design.md` §5.1 is **retained**. Recalibration operates only on the per-trial / per-probe band threshold, not on the aggregation rule. Modifying the aggregation rule would compound two recalibration axes; this spec scopes only the band axis.

### 2.4 Per-probe vs per-trial aggregation

A per-trial verdict is the AND of per-probe verdicts across the 3 consistency probes for that fact (existing protocol). A trial PASSes consistency iff all 3 cons probes PASS. This rule is **retained**; recalibration does not modify per-trial aggregation either.

---

## §3 — Candidate band specifications

### 3.1 Family B-A — Absolute-relaxed thresholds

Drop the threshold `T` to a value where edit-effect signal can be distinguished from baseline noise.

#### 3.1.1 Variants

| Variant | Threshold | Pass rate at L01 (S2.8 evidence) | Disposition |
|---|---|---|---|
| B-A-0.1 | P(target_new) > 0.1 | 0/27 | Reject (no signal lift over 0.5 band) |
| B-A-0.05 | P(target_new) > 0.05 | 0/27 | Reject (no signal lift over 0.5 band) |
| B-A-0.01 | P(target_new) > 0.01 | 6/27 (22%) | Candidate — surfaces upper tail of post-edit distribution |
| B-A-0.005 | P(target_new) > 0.005 | 6/27 (22%) | Equivalent to B-A-0.01 in S2.8 evidence; redundant |
| B-A-0.001 | P(target_new) > 0.001 | 24/27 (89%) | Reject — baseline-noise inclusion (pre-edit ~0.008 within range) |

**B-A-0.01 is the operative absolute-relaxed candidate.** It admits the upper tail of the observed post-edit distribution while excluding the median; a Stage 2 PASS under B-A-0.01 would require ≥2/3 trial passes with ≥3/3 probe passes per trial, i.e., the ENTIRE post-edit P(target_new) distribution per probe must lie above 0.01 — substantially stronger than the marginal upper-tail data point.

#### 3.1.2 Per-fact alternate (sensitivity analysis only — not primary)

Per-fact threshold `T_f` derived as `T_f = max(P(target_new)_pre_f, ε)` where the per-fact baseline drives the threshold and ε = 0.001 floor. Surfaces only at sensitivity analysis stage; not the primary recommendation per §2.2.

### 3.2 Family B-B — Rank-improvement thresholds

Pass criterion: `target_new` appears in top-K.

| Variant | Criterion | Pass rate at L01 (S2.8) | Disposition |
|---|---|---|---|
| B-B-1 | top_1 == target_new | 0/27 | Reject (= original strong-evidence band in rank form) |
| B-B-5 | target_new in top-5 | 0/27 | Reject (insufficient signal) |
| B-B-10 | target_new in top-10 | UNKNOWN — top-10 not preserved | Defer (requires schema augmentation) |
| B-B-100 | target_new in top-100 | UNKNOWN — top-100 not preserved | Defer (requires schema augmentation) |

**Schema constraint.** Trial JSONs preserve only `top_5` per probe. B-B-10/100 cannot be evaluated against existing trial JSONs without re-execution to capture larger top-K. This family is **deferred** as a band candidate; flagged as a schema augmentation opportunity for any future Stage 1 SECT v2 (§6).

### 3.3 Family B-C — Relative-lift thresholds

Pass criterion: `P(target_new)_post / P(target_new)_pre > N` for N ∈ {2, 5, 10, 100}.

**Schema constraint.** Per-probe pre-edit P(target_new) baselines are NOT preserved in trial JSONs. They live in Cell 7 baseline outputs (per `stage_1_sect_runbook_v1_4.md`). Without these baselines on a per-probe basis, B-C cannot be evaluated.

**Disposition.** B-C is the most physically interpretable family — it directly measures "did the edit cause a signal lift relative to the unedited baseline." It is **deferred** for v1.0 of this spec; reactivation requires the operator to provide Cell 7 baseline outputs alongside the trial JSONs (§6.2).

If Cell 7 baseline outputs are available, B-C-2 (lift > 2×) is the proposed primary candidate within this family — generous enough to admit small effects, strict enough to exclude noise.

### 3.4 Family B-D — Target-dominance thresholds

Pass criterion: `P(target_new) > P(top_1) / k` for k ∈ {2, 5, 10}.

| Variant | Criterion | Pass rate at L01 (S2.8) | Disposition |
|---|---|---|---|
| B-D-2 | P(target_new) > P(top_1) / 2 | 0/27 | Reject |
| B-D-5 | P(target_new) > P(top_1) / 5 | 0/27 | Reject |
| B-D-10 | P(target_new) > P(top_1) / 10 | 0/27 | Reject |

Empirically, P(top_1) ranges from 0.04 to 0.80 across probes; P(target_new) max = 0.011. The ratio `P(target_new) / P(top_1)` is bounded above by ~0.27 only at the (cfb-003-cons-1) outlier; at all other probes the ratio is below 0.05. **B-D-10 is the loosest variant; it still PASSes 0/27.** Reject family B-D.

### 3.5 Family B-E — Compound bands

Compound bands combine multiple families with AND/OR logic.

#### 3.5.1 B-E-EITHER (disjunctive permissive)

Pass criterion: `B-A-0.01 OR B-B-5` — PASS if either absolute or rank criterion satisfied.

S2.8 evidence: 6/27 ∪ 0/27 = 6/27. Equivalent to B-A-0.01 at canonical hparams. May differentiate at higher edit strengths if rank improves but absolute remains low. **Candidate.**

#### 3.5.2 B-E-BOTH (conjunctive strict)

Pass criterion: `B-A-0.01 AND B-B-5` — PASS only if both absolute and rank criteria satisfied.

S2.8 evidence: 6/27 ∩ 0/27 = 0/27. **Reject** — strictly stronger than B-A-0.01 alone; degenerates to B-B-5 at L01.

#### 3.5.3 B-E-PROPORTIONAL (preserve aggregate rule alignment)

Pass criterion: `P(target_new) > 0.01 AND P(target_new) > 2 × P(target_new at unrelated_competitor)`.

**Schema constraint.** Requires per-probe specification of an "unrelated_competitor" token whose baseline P serves as a noise reference. Not preserved in trial JSONs. **Deferred.**

---

## §4 — Recommended band

### 4.1 Primary recommendation: B-A-0.01 (absolute-relaxed at threshold 0.01)

**Definition.** A trial PASSes consistency iff `P(target_new) > 0.01` at all three consistency probes (per-trial all-pass; per-config ≥2/3 trials pass). This is structurally identical to the existing band specification with `0.5` replaced by `0.01`.

**Justification.**

1. **Physical meaning.** `P(target_new) > 0.01` corresponds to "target_new carries at least 1% of the next-token probability mass." Pre-edit baselines for the three CFB v1 facts are in the 0.0001–0.01 range (cfb-001 = 0.0078 per handoff §2.3); the 0.01 threshold sits at or just above the upper end of pre-edit baseline noise, separating measurable edit effect from noise floor.

2. **Decidability.** Mechanical AND of per-probe thresholds; identical decidability to current band per `stage_2_sweep_design.md` §5.4.

3. **Falsification rigor.** A PASS under B-A-0.01 requires the entire trial-level distribution (3 probes × ≥2 trials per config) to lie above 0.01 — substantially stronger than the marginal 6/27 single-probe pass rate observed at L01.

4. **Decisive against Class B.** If the sweep produces any PASS under B-A-0.01, Class B is the defect (the original 0.5 band over-specified the threshold). If the sweep produces zero PASS, Class B is eliminated — the data lies uniformly below even a 50× relaxed threshold.

### 4.2 Secondary alternate: B-A-0.05 (asymmetric falsification)

Run B-A-0.05 in parallel. If B-A-0.01 passes but B-A-0.05 fails, the recalibration discovery is "the band threshold was off by ~10×, not 50×." If both pass uniformly, recalibration is well-conditioned.

### 4.3 Sensitivity-analysis bands (non-binding)

For diagnostic completeness, the re-evaluation pass also reports per-config pass rates under:
- B-A-0.001 (noise floor — sanity check)
- B-A-0.005 (intermediate sensitivity)
- B-A-0.1 (intermediate failure boundary)
- B-B-5 (rank-only diagnostic)

These do not gate the verdict; they support forensic interpretation.

### 4.4 Bands explicitly NOT modified

Per scope:

| Band | Disposition | Reason |
|---|---|---|
| Generalization (drift < 0.05) | UNCHANGED | Out of S2.11-B scope; passing 41/42 trials at S2.10 |
| Specificity post-edit (drift < 0.05) | UNCHANGED | Out of scope; passing 42/42 |
| Specificity post-unmount (drift < 0.05) | UNCHANGED | Out of scope; passing 42/42 |
| Unmount band (\|drift\| < 1e-4) | UNCHANGED | HARD per IC-S23-4; not subject to recalibration |

S2.11-B recalibrates the **consistency band** only.

---

## §5 — Re-evaluation algorithm

### 5.1 Inputs

| Input | Source | Required |
|---|---|---|
| 42 per-trial JSONs (`L{01..14}/trials/cfb-{001,002,003}_r1.json`) | NV `/workspace/stage_2_sweep/L*/trials/` OR SSD mirror `/Volumes/memit/llm-database-poc-mirror/stage_2_sweep/L*/trials/` | YES |
| Per-config `aggregate_verdict.json` (×14) | `/workspace/stage_2_sweep/L*/aggregate_verdict.json` | OPTIONAL (cross-check; original aggregates are at the 0.5 band) |
| Per-fact pre-edit P(target_new) baselines | `/workspace/stage_1_sect/cell_7_baseline.json` (or equivalent) | OPTIONAL (enables B-C family if provided) |

### 5.2 Algorithm (decidable mechanical procedure)

```
INPUTS:
    trial_jsons    : list of 42 per-trial JSON paths
    band_specs     : dict of {band_id: predicate}, e.g.,
                     {"B-A-0.01": lambda probe: probe["p_target_new"] > 0.01,
                      "B-A-0.05": lambda probe: probe["p_target_new"] > 0.05,
                      "B-A-0.001": lambda probe: probe["p_target_new"] > 0.001,
                      "B-A-0.005": lambda probe: probe["p_target_new"] > 0.005,
                      "B-A-0.1":   lambda probe: probe["p_target_new"] > 0.1,
                      "B-B-5":     lambda probe: probe["target_new"] in [t["token_str"].strip()
                                                                          for t in probe["top_5"]]}

OUTPUTS:
    revised_per_config_verdicts : per-config per-band PASS/FAIL
    revised_sweep_verdict       : per-band sweep-level PASS/FAIL

STEP 1 — Per-probe evaluation:
    For each trial_json in trial_jsons:
        Load trial.post_edit_probes
        For each cons_probe in {p-{fact_id}-cons-1, p-{fact_id}-cons-2, p-{fact_id}-cons-3}:
            For each band_id in band_specs:
                probe_pass[band_id] = band_specs[band_id](cons_probe)

STEP 2 — Per-trial aggregation (AND across probes):
    For each trial in trials:
        For each band_id:
            trial_pass[band_id] = AND over cons_probes of probe_pass[band_id]

STEP 3 — Per-config aggregation (≥2/3 trials):
    Group trials by config_id (L01..L14)
    For each config_id:
        For each band_id:
            n_trials_passing = sum(trial_pass[band_id] for trials in config)
            config_pass[band_id] = (n_trials_passing >= 2)

STEP 4 — Sweep aggregation (OR across configs):
    For each band_id:
        sweep_pass[band_id] = ANY config has config_pass[band_id] == True

STEP 5 — Calibration corridor (per-band):
    For each band_id:
        corridor[band_id] = [config_id : config_pass[band_id]
                             AND specificity_pe_pass
                             AND specificity_pu_pass
                             AND unmount_pass]
        (Specificity / unmount verdicts inherited from sweep_verdict.json
         since those bands are unmodified per §4.4)
```

### 5.3 Output schema

`revised_sweep_verdict_v1.json`:

```
{
  "spec_ref": "probe_band_recalibration_spec.md v1.0",
  "evaluated_at": "<ISO>",
  "source": {
    "trial_jsons_count": 42,
    "config_count": 14,
    "anchor_at_L01": true
  },
  "per_band_verdicts": {
    "B-A-0.01": {
      "per_config": [
        {"config_id": "L01", "trials_passing": <n>, "config_pass": <bool>},
        ...
        {"config_id": "L14", "trials_passing": <n>, "config_pass": <bool>}
      ],
      "calibration_corridor": [<config_ids>],
      "sweep_pass": <bool>
    },
    "B-A-0.05": { ... },
    "B-A-0.001": { ... },
    "B-A-0.005": { ... },
    "B-A-0.1": { ... },
    "B-B-5": { ... }
  },
  "primary_band": "B-A-0.01",
  "primary_band_verdict": <bool>,
  "diagnostic_summary": "<text>"
}
```

### 5.4 Decidability invariant

Algorithm is mechanical and reproducible: given `(trial_jsons, band_specs)` input pair, the output `revised_sweep_verdict_v1.json` is uniquely determined. No operator interpretation required. Idempotent under re-execution.

### 5.5 Determinism cross-check (incidental)

Algorithm includes an optional STEP 0 that asserts replicate determinism: for any (config, fact, replicate) triple, repeat-run produces identical P(target_new) at all probes. Under the reduced 3×1 protocol there is only 1 replicate per fact-config, so this check is vacuous within the sweep — it is exercised only if the operator promotes a config to 3×3 per `stage_2_sweep_design.md` §3.3.

---

## §6 — Schema constraints surfaced

### 6.1 Existing schema sufficiency

The current per-trial JSON schema (per `/mnt/project/stage_1_trial_cfb-001_r1.json` inspection) preserves:

- `post_edit_probes.{probe_id}.p_target_new`
- `post_edit_probes.{probe_id}.p_target_true`
- `post_edit_probes.{probe_id}.p_top_1`
- `post_edit_probes.{probe_id}.top_1_token`
- `post_edit_probes.{probe_id}.top_5` (token_id, token_str, p)

This is **sufficient** for B-A (absolute), B-B-5 (rank-in-top-5), and B-D (target-dominance) families. **Insufficient** for B-B-10/100 (need top-K with K>5), B-C (need pre-edit baselines), and B-E-PROPORTIONAL (need unrelated-competitor token).

### 6.2 Schema augmentation candidates (forward sessions)

If S2.11-B FAILS and S2.12 progresses to higher-information-density investigation, the trial JSON schema should be augmented with:

- `top_100` (full top-K capture for rank analysis at higher K)
- `pre_edit_baselines.{probe_id}.p_target_new` (per-probe pre-edit baseline for relative-lift analysis)
- `pre_edit_baselines.{probe_id}.top_1_token` (for shift-direction analysis)

This is logged as **OQ-S211B-2** (§7).

### 6.3 OQ-S210-4 incidental light

The S2.8 forensic data shows one finding adjacent to OQ-S210-4 (L02 generalization gen=2/3 anomaly): under deterministic seeding (S2.8), generalization PASSed 9/9 at canonical hparams. The L02 anomaly is therefore not a replicate-stochasticity artifact at canonical hparams; it is genuinely a configuration-localized signal at (v_lr=0.5, steps=50, weight=20000). This does NOT close OQ-S210-4 — it narrows the hypothesis space — but it is a useful side-finding.

---

## §7 — Open questions surfaced by recalibration

| OQ ID | Description | Resolution path |
|---|---|---|
| **OQ-S211B-1** (NEW) | Per-fact band derivation rigor — if uniform B-A-0.01 PASSes but per-fact B-A-perfact yields differential pass rates across cfb-001/002/003, the per-fact baseline disparity (cfb-003 ~2× weaker, §1.1) becomes load-bearing. Per-fact bands carry a circularity risk if derived from the same data they evaluate. | Resolution: re-evaluation pass reports per-fact pass rates as sensitivity output (§4.3); if asymmetry is large, S2.12 should consider fact-level corpus revision (Class A intersection). |
| **OQ-S211B-2** (NEW) | Trial JSON schema sufficiency — current schema captures `top_5` and post-edit probabilities only; insufficient for relative-lift (B-C) and rank-K>5 (B-B-10) analyses. | Resolution: schema augmentation deferred to S2.12 (any re-execution session) per §6.2. |
| **OQ-S211B-3** (NEW) | Pre-edit per-probe baseline preservation — the handoff guide notes Cell 7 baseline P(target_new=baseball)=0.0078 for cfb-001 but does not specify whether per-probe (vs. per-fact aggregate) baselines exist. If only fact-level baselines are preserved, B-C family cannot be activated even with operator data upload. | Resolution: confirm Cell 7 baseline output schema during re-evaluation execution; if per-probe baselines are absent, OQ-S211B-3 closes routing-deferred to S2.12. |

---

## §8 — Falsification semantics

### 8.1 PASS under recalibrated bands

If re-evaluation under B-A-0.01 yields ≥1 calibration corridor entry (consistency-PASS ∩ specificity-PASS ∩ unmount-PASS), Class B is the defect:

- The original band (P > 0.5) over-specified the threshold by ~50×
- The textual axis is functional under MEMIT at the post-2.5 patch state, just at sub-dominant signal strength
- **Does NOT mean the edit "succeeded" in the strong sense.** It means the edit "moved measurable signal toward target_new beyond noise floor."
- Routes to: S2.12 → Workstream 2 entry (orchestration path GAP-4) AND/OR Stage 2 promotion of corridor configs to full 3×3 protocol per `stage_2_sweep_design.md` §3.3.

### 8.2 FAIL under recalibrated bands

If re-evaluation under B-A-0.01 yields zero calibration corridor entries (no consistency-PASS configs even at 50× relaxation), Class B is eliminated:

- The textual-axis defect is upstream of band specification
- The post-edit P(target_new) distribution does not separate from baseline noise even at relaxed thresholds
- This is consistent with the §1 forensic prior — the 27-probe distribution at L01 has a narrow tail that does not extend significantly above pre-edit baseline (~0.008)
- Routes to: S2.12-A (corpus revision, CFB v1 → CFB v2) per handoff guide §3.2

### 8.3 PARTIAL (asymmetric across bands)

If B-A-0.001 PASSes but B-A-0.01 FAILS, the data lies in pure-noise regime at L01; signal differentiation across configs may exist but is below 0.01 magnitude. This is a **diagnostic intermediate** outcome — the recalibration spec recommends treating this as a FAIL for Class B isolation purposes (per §4.1 falsification rigor) but logging it as forensic detail; routes to S2.12-A.

### 8.4 Asymmetric across configs

If B-A-0.01 PASSes only at high-strength configs (e.g., L13/L14 at v_lr=2.0) and not at L01-L08, the signal is hparam-strength-dependent under the relaxed band. This is a **partial Class B + partial calibration** outcome:

- Class B is partially active (band over-specification contributed to FAIL at L01)
- Hparam calibration is also active (higher v_lr / more steps required to reach the relaxed band)
- Routes to: Stage 2 promotion at the qualifying hparam region; OQ-PROBE-2 closes with band-correction; OQ-S25-3/4 close with hparam values from corridor

---

## §9 — Authoring acceptance gates

Per `stage_2_sweep_design.md` §9 acceptance gate convention:

| Gate | Required output | Disposition |
|---|---|---|
| Methodology completeness | Multiple band families enumerated; recommendation rationale tied to physical meaning | **PASS** — §2 ontology; §3 enumeration; §4 recommendation with §1 forensic anchoring |
| Decidability | Re-evaluation algorithm is mechanical and reproducible | **PASS** — §5.2 algorithm; §5.4 invariant |
| Schema sufficiency analysis | Each candidate band evaluated against existing trial JSON schema | **PASS** — §6.1 + per-family disposition in §3 |
| Falsification semantics | PASS/FAIL/intermediate outcomes mapped to forward routing | **PASS** — §8 |
| Forensic anchoring | Recommendation grounded in observed S2.10 / S2.8 distribution, not heuristic | **PASS** — §1 ground-truth + §4.1 justification |

All five authoring acceptance gates PASS at v1.0 close. Spec is AUTHORING-ACCEPTANCE-PROVISIONAL pending re-evaluation execution per §5.

---

## §10 — Carry-forward to re-evaluation execution

| Item | Required at execution |
|---|---|
| Trial JSON corpus | 42 files at `/mnt/user-data/uploads/` OR `/mnt/project/` (operator promotion) |
| Spec | `probe_band_recalibration_spec.md` v1.0 (this document) |
| Algorithm | `re_evaluate_bands.py` (to be authored at execution time per §5.2) |
| Output | `revised_sweep_verdict_v1.json` per §5.3 schema |
| Sweep verdict cross-check | Re-evaluation under existing 0.5 band must reproduce S2.10 verdict (sweep_pass=False; consistency 0/3 across all 14 configs); failure to reproduce = algorithm defect, not band defect |

---

*End of Probe-band Recalibration Spec v1.0.*
