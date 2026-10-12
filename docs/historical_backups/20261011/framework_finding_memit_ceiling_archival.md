# Framework Finding — Architectural-Invariant MEMIT Ceiling on Llama-3.1-8B at Canonical Hparams

> **Artifact type:** Framework finding archival — permanent meta-conclusion
> **Status:** RATIFIED — load-bearing
> **Authored:** 2026-05-04 (within S2.16)
> **Basis:** Workstream 1 Sessions S2.10, S2.11-B, S2.12-A, S2.13-C, S2.14-D, S2.15-D2
> **Specialist provenance:** memit-specialist (primary; mechanism identification, ROME / GRACE forward routing); state-consistency-theorist (secondary; Copy-Unmount bit-exact joint-overlay carry-forward); validation-contract-architect (verdict surface across hypothesis classes; consistency band enforcement); framework-spec-writer (formalization)
> **Workstream:** WS1 (empirical execution)
> **Successor:** S2.16 T-branch decision document (`t_branch_decision_document.md`)

---

## §1 — Finding statement

The architectural-invariant ceiling on `(meta-llama/Llama-3.1-8B × MEMIT × canonical hparams)` is **structural** and **not eliminable** by any axis within hypothesis classes A (corpus structure), B (probe structure), C (target neighborhood), or D (layer-set selection). Across SIX orthogonal axes of empirical variation, MEMIT's `z`-vector update geometry converges to avg `P[target_new]` magnitudes in the range `1e-7` to `2.2e-2` — well below the consistency band `0.5` required for an edit-success verdict per IC-S24-4 / cfb-v3.yaml v1.0 acceptance criteria.

Generalization, specificity (post-edit and post-unmount), and the unmount band (HARD; IC-S23-4) hold at every axis. Only the consistency surface fails. The ceiling is therefore not an artifact of the verification pipeline, the cache-dispatch path, the Copy-Unmount regime, or the bit-exact reproducibility infrastructure; it is a property of MEMIT's optimization geometry on this target model at canonical hparams.

The optimization-geometry magnitudes — z-error L2-norm `3.14–4.22` and per-layer upd-norm `0.32–0.67` — are essentially identical across layer-set re-selection (`L4-L8` S2.13-C reference vs `L2-L6` S2.15-D2 corrected window). Cluster-level fact-independence of these magnitudes confirms the ceiling is structural to the `(model × write engine × hparams)` combination, not to any specific class of input variation.

The only remaining hypothesis class that has not yet been empirically eliminated is **T-branch** — change one of the three load-bearing parameters of the combination: `(T.1 alt model)`, `(T.2 alt write engine)`, or `(T.3 alt parametric memory architecture)`.

---

## §2 — Empirical record across six orthogonal axes

### §2.1 Axis index

| Axis | Session | Variation held against canonical hparams | Ceiling reading (avg `P[target_new]` at v* convergence) | Verdict |
|---|---|---|---|---|
| 1 — Hparam surface | S2.10 | LHS-16 reduced grid: `v_lr ∈ [0.1, 2.0]`, `v_num_grad_steps ∈ [25, 200]`, `mom2_update_weight ∈ [5000, 25000]` | `0.022` max | FAIL — no calibration corridor |
| 2 — Probe structure (Class B) | S2.11-B | Probe family substitution under fixed cfb corpus | (verdict-decisive at probe surface) | FAIL → B ELIMINATED |
| 3 — Corpus structure (Class A) | S2.12-A | cfb-v2 sport-relation neighborhood; subject regime variation | `1.4e-5` to `3.8e-5` | FAIL → A ELIMINATED |
| 4 — Target neighborhood (Class C) | S2.13-C | cfb-v3 instrument-class targets; cluster-shift completeness PASS-set 4-of-17 on Llama tokenizer | calibration-band stratification (in-band-3 / at-floor-1 / sub-noise-2) | FAIL → C ELIMINATED |
| 5 — Layer-set mediation (Class D.1) | S2.14-D | Causal trace per-fact mediation; `L_M` values L5/L2/L6/L3/L3 across 5 cfb-v2 facts | mediation peak `L_M=L2` outside MEMIT canonical `[4..8]` | NEAR-MISS → resolved as ceiling-not-locus at S2.15-D2 |
| 6 — Batched MEMIT (Class D.3) | S2.14-D | `N=5` simultaneous edits at canonical hparams; single batched trial vs serial baseline | `7e-7` to `5e-5` | FAIL → D.3 ELIMINATED at Trial 0 OOM |
| 7 — Layer-set narrowed window (Class D.2) | S2.15-D2 | `hparams.layers` narrowed `[4,5,6,7,8] → [2,3,4,5,6]` per D.1 mediation peak alignment | `1.5e-5` to `2.5e-5` | FAIL → D.2 ELIMINATED |

The axis index above lists seven empirical reference points across the four hypothesis classes plus the canonical hparam baseline. Class D produced three sub-classes (D.1, D.2, D.3); each is recorded as a separate axis because each tests a distinct mechanism within the layer-set hypothesis space.

### §2.2 Axis 1 — Hparam sweep (S2.10)

LHS-16 reduced grid established the canonical hparam surface as the maximal-effort baseline. Provisional values `v_lr=0.5`, `mom2_update_weight=15000`, `v_num_grad_steps=25` were ratified as canonical by sweep verdict; the `0.022` max reading came from the best LHS-16 trial and remains the highest avg `P[target_new]` recorded across any axis. No calibration corridor existed at PASS criterion (`P[target_new] ≥ 0.5` consistency band).

S2.10 settled the canonical hparam surface against which all subsequent class-elimination axes were tested. No further hparam-level variation is in scope at any later session under D-S25-3 / D-S25-4 / D-S29-1.

### §2.3 Axis 2 — Probe structure (S2.11-B; Class B ELIMINATED)

Class B tested whether the probe family used to evaluate edit success was inducing the FAIL verdict — i.e., whether a different probe set might reveal edit success that the original probe family obscured. Verdict FAIL on the probe surface eliminated B as a candidate cause. Probe-set-v3.yaml v1.0 ratified at S2.13-C as the canonical probe family carrying forward; 38 active probes durable across all subsequent sessions.

### §2.4 Axis 3 — Corpus structure (S2.12-A; Class A ELIMINATED)

Class A tested whether the corpus structure of the original Stage 2 sweep facts was inducing the FAIL verdict. cfb-v2 sport-relation corpus with subject regime variation produced ceiling readings `1.4e-5` to `3.8e-5`. Class A ELIMINATED. cfb-v3.yaml v1.0 (5 facts: Bo Jackson / Tiger Woods / Deion Sanders / Hakeem Olajuwon / Lindsey Vonn) ratified at S2.13-C as the canonical corpus carrying forward.

### §2.5 Axis 4 — Target neighborhood (S2.13-C; Class C ELIMINATED)

Class C tested whether the target-token neighborhood structure (specifically: target token cluster-shift completeness against the natural top-1 calibration band) was inducing the FAIL verdict. cfb-v3 instrument-class targets enabled cluster-shift away from the original sport-relation neighborhood. Cluster-shift completeness verdict PASS at the PASS-set 4-of-17 instrument single-token coverage on the Llama tokenizer. Calibration-band stratification (D-S213C-CALIB-3) revealed three regimes:

| Calibration band | Facts | Behavior |
|---|---|---|
| **IN-BAND** `[0.0001, 0.05]` | cfb-v3-001 guitar (`P=0.0005`); cfb-v3-002 piano (`P=0.0003`) | Pre-edit `P[target_new]` measurable; edit-lift expected if mechanism functional |
| **AT-FLOOR** | cfb-v3-005 flute (sentinel; `P=0.0000`) | At natural floor; edit-lift required to clear floor |
| **SUB-NOISE** | cfb-v3-003 violin; cfb-v3-004 harp | Sub-noise pre-edit; verdict integrity only on load-bearing subset |

Class C ELIMINATED. cfb-v3.yaml v1.0 ratified as canonical.

### §2.6 Axis 5 — Layer-set mediation (S2.14-D D.1; NEAR-MISS resolved at S2.15-D2)

Class D.1 tested whether the canonical MEMIT layer set `[4,5,6,7,8]` was misaligned with the actual mediation locus for cfb-v2 facts on Llama-3.1-8B. Causal trace per-fact mediation map identified `L_M` values L5/L2/L6/L3/L3 across 5 cfb-v2 facts, with mediation band peak at L2-L5 (one step or more below MEMIT `[4..8]` for 4 of 5 facts). Tiger Woods (`P_clean=0.926`) was the sharpest anchor at `L_M=L2`, `IE=0.7058` — single-layer L2 MLP patch alone restores 70% of corruption recovery.

Verdict at S2.14-D: NEAR-MISS. The mediation peak misalignment was a load-bearing candidate explanation for the ceiling. The verdict-predicate cascade `v0.1` was too coarse to distinguish near-miss (`|L_M - MEMIT_center| ≤ 4`) from far-miss (`> 4`); OQ-S214D-D1-PREDICATE-1 surfaced for `v0.2` predicate refinement.

Resolution at S2.15-D2: the narrowed window `L2-L6` was constructed to test D.1 directly. D.2 FAIL at L2-L6 with optimization-geometry magnitudes essentially identical to L4-L8 reference confirms that the mediation peak misalignment was not the locus. D.1 NEAR-MISS resolved as ceiling-not-locus. OQ-S214D-D1-PREDICATE-1 eliminated as forward concern; predicate-cascade refinement no longer load-bearing for Class D verdict.

### §2.7 Axis 6 — Batched MEMIT (S2.14-D D.3; ELIMINATED at Trial 0 OOM)

Class D.3 tested whether batched MEMIT `N=5` simultaneous-edit dispatch was inducing the FAIL verdict — i.e., whether the optimization geometry of a batched edit differs from serial single-edit dispatch in a way that recovers consistency. Single batched trial executed at `N=5` on RTX 4090 24 GiB; ceiling readings `7e-7` to `5e-5`. Trial 0 OOM (constraint C-S214D-2: batched MEMIT `N=5` on RTX 4090 24 GiB at VRAM ceiling). D.3 ELIMINATED.

The Copy-Unmount bit-exact joint-5-fact-overlay regime was empirically validated at S2.14-D D.3: 5/5 layers `allclose_match=True`; per-fact unmount drift `0.00e+00`. First IC-S23-4 validation under joint-edit regime. OQ-S214D-D3-3 closed empirically. This is a load-bearing carry-forward anchor: any T-branch successor that retains the target model and uses an in-place tensor restore mechanism inherits this validation.

### §2.8 Axis 7 — Layer-set narrowed window (S2.15-D2 D.2; ELIMINATED)

Class D.2 tested whether narrowing the canonical layer set from `[4,5,6,7,8]` to `[2,3,4,5,6]` — better aligning MEMIT dispatch to the D.1 mediation peak band — recovers edit success. Stage 1 SECT v3 narrowed-window execution: 15 trials (5 facts × 3 replicates); verdict-integrity-decisive on 3-fact load-bearing subset (cfb-v3-001 guitar / cfb-v3-002 piano / cfb-v3-005 flute sentinel) per D-S213C-VERDICT-3 carry-forward.

| Aggregate criterion | Load-bearing subset (decisive) | Full 5-fact aggregate (informational) |
|---|---|---|
| **Consistency** | **0/3 facts pass** | 0/5 facts pass |
| Generalization | 3/3 facts pass | 5/5 facts pass |
| Specificity (post-edit) | 3/3 facts pass | 5/5 facts pass |
| Specificity (post-unmount) | 3/3 facts pass | 5/5 facts pass |
| **Unmount (HARD; IC-S23-4)** | **9/9 trials pass** | **15/15 trials pass** |
| **Stage 1 verdict** | **FAIL** | **FAIL** |

Sentinel cfb-v3-005 (Lindsey Vonn / flute) consistency `0/3` is the strongest possible class-elimination signal per cfb-v3.yaml v1.0 acceptance criteria. Per-trial z-error magnitudes `3.14-4.22` and per-layer upd-norm magnitudes `0.32-0.67` at L2-L6 are essentially identical to L4-L8 historical reference. Class D FULLY ELIMINATED.

The Copy-Unmount bit-exact joint-overlay regime was extended from L4-L8 to L2-L6 at S2.15-D2: 75/75 layer-restore allclose; 30/30 trial unmount drift `0.00e+00`. Cross-session bit-exact determinism on Llama-3.1-8B fp16 forward-pass confirmed across 5 cross-session checkpoints (Block A → kernel restart → Block B → S2.14-D anchor → cfb-v3.yaml v1.0 lock baseline). OQ-S214D-DETERMINISM-1 closed empirically. Both anchors are load-bearing carry-forward to T-branch.

---

## §3 — Hypothesis-class ledger — final

| Class | Description | Status | Eliminated at |
|---|---|---|---|
| A | Corpus structure (sport-relation cfb-v2 → instrument-class cfb-v3) | ELIMINATED | S2.12-A |
| B | Probe structure (probe family ratification) | ELIMINATED | S2.11-B |
| C | Target neighborhood (cluster-shift completeness; calibration-band stratification) | ELIMINATED | S2.13-C |
| D | Layer-set selection | **FULLY ELIMINATED** | **S2.15-D2** |
| D.1 | Mediation map locus (causal trace) | NEAR-MISS resolved as ceiling-not-locus | S2.15-D2 |
| D.2 | Narrowed window L2-L6 | ELIMINATED (FAIL at corrected window) | S2.15-D2 |
| D.3 | Batched MEMIT N=5 | ELIMINATED (FAIL + OOM ceiling) | S2.14-D |
| **T** | **T-branch — model × write engine × architecture** | **OPEN — only remaining hypothesis class** | — |
| T.1 | Alt model (Llama-3.2-3B / Mistral-7B / etc.) | OPEN | — |
| T.2 | Alt write engine (ROME / GRACE / MEND / SERAC) | OPEN — leading per D-S215D2-4 | — |
| T.3 | Alt parametric memory architecture | OPEN — out of WS1 scope per project instructions | — |

---

## §4 — Load-bearing carry-forward anchors

These anchors are empirical results that the architectural-invariant ceiling does not invalidate. They are load-bearing for any successor session — including T-branch sessions — that operates within their applicability scope.

### §4.1 Cross-session bit-exact determinism (Llama-3.1-8B fp16)

| Property | Value |
|---|---|
| Forward-pass drift | `0.00e+00` |
| Verified at | 5 cross-session checkpoints (Block A capture → kernel restart → Block B Cell 5 → S2.14-D anchor → cfb-v3.yaml v1.0 lock baseline) |
| Hparam regime | Canonical (`v_lr=0.5`, `mom2_update_weight=15000`, `v_num_grad_steps=25`, `fact_token=subject_last`) |
| Carry-forward applicability | Any T-branch session retaining `meta-llama/Llama-3.1-8B` revision `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` |
| Closed-by | OQ-S214D-DETERMINISM-1 |

### §4.2 Copy-Unmount bit-exact joint-overlay regime

| Property | Value |
|---|---|
| Mechanism | Per-layer in-place tensor restore via Copy-Unmount under joint-multi-fact-overlay regime |
| Layer sets validated | `L4-L8` (S2.14-D D.3) AND `L2-L6` (S2.15-D2 D.2) |
| Per-layer allclose | 75/75 PASS at S2.15-D2 (15 trials × 5 layers); 5/5 at S2.14-D D.3 |
| Per-trial unmount drift | `0.00e+00` across 15+1 trials |
| Carry-forward applicability | Any T-branch session that retains the target model AND uses a write-engine mechanism allowing in-place tensor restore. T.2 ROME: yes (sibling of MEMIT in same repo; nethook patterns identical). T.2 GRACE: no (adapter-based; different dispatch surface). T.1 alt model: re-derivation per architecture |
| Closed-by | IC-S23-4 (HARD); OQ-S214D-D3-3 |

### §4.3 Active patches canonical (`memit-patches-canonical.md` v2.5)

| Patch | Description | T.2 ROME applicability | T.2 GRACE applicability |
|---|---|---|---|
| P-1 | nethook trace-context | Likely | Different dispatch surface; minimal reuse |
| P-2 | nethook get-trace | Likely | Different dispatch surface; minimal reuse |
| P-4 | config-attribute resolution | Likely | Re-derive |
| P-5 | dataset-loader pad-token interaction | Likely | Re-derive |
| P-6 | post-cache filename canonicalization (`_t100_` segment) | Inapplicable — single-fact dispatch; no batch_tokens propagation surface | Inapplicable |
| P-7 | cache-dispatch explicit `batch_tokens` propagation | Inapplicable — same reason | Inapplicable |
| Pad-Token | Tokenizer pad-token coverage | Likely | Likely |
| Copy-Unmount | In-place tensor restore | Likely (mechanism applicable) | Inapplicable (adapter mechanism) |

ROME shares the MEMIT codebase ancestry under SHA pin `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (parent commit). Patches P-1, P-2, P-4, P-5, Pad-Token, Copy-Unmount carry forward to T.2 ROME with high confidence; P-6 and P-7 are MEMIT-multi-fact-specific and inapplicable.

### §4.4 Ratified runbook

`stage_1_sect_runbook_v1_5.md` EMPIRICALLY-RATIFIED at S2.15-D2 close per D-S215D2-CLOSE-2. Cache-dispatch architectural axis fully validated at L2-L6 (R1.3 PASS at 5.23s; 15/15 unmount drift `0.00`); textual axis FAIL recapitulates S2.13-C; layer-set narrowed-window axis FAIL eliminates D.2 sub-class. Optional v1.6 hardening pass deferred per D-S215D2-3; only required if successor session reuses Stage 1 SECT runbook structurally (likely for T.2 ROME; minimal for T.2 GRACE).

### §4.5 Ratified canonical fact and probe artifacts

| Artifact | Status | Carry-forward |
|---|---|---|
| `cfb-v3.yaml` v1.0 (5 facts) | LOCKED | Carry-forward to T-branch under D-S213C-VERDICT-3 |
| `probe-set-v3.yaml` v1.0 (38 active probes) | LOCKED | Carry-forward to T-branch under D-S213C-VERDICT-3 |
| `stage_1_token_verification.json` | TOLERATED-MULTITOKEN allowlist (cfb-v3-004 harp; first-token-proxy methodology) | Re-validate per write engine multi-token handling |
| `stage_1_llama_baselines.json` | 38 probes; first-token-proxy per D-S215D2-CFB-V3-004-PROXY-1 | Re-validate at trial 0 for write-engine-specific drift |

---

## §5 — Scope of the finding

### §5.1 What this finding claims

1. The architectural-invariant ceiling on `(meta-llama/Llama-3.1-8B × MEMIT × canonical hparams)` is structural across six orthogonal axes of empirical variation within hypothesis classes A, B, C, D.
2. Hypothesis classes A, B, C, and D are fully eliminated as candidate explanations for the ceiling.
3. The optimization-geometry magnitudes (z-error, upd-norm) are stable across layer-set re-selection and across fact-cluster variation, indicating the ceiling is structural to the `(model × write engine × hparams)` combination.
4. Generalization, specificity, and unmount surfaces are not implicated in the FAIL verdict; only the consistency surface fails.
5. T-branch (model × write engine × architecture) is the only remaining hypothesis class.

### §5.2 What this finding does not claim

1. **Not a claim about MEMIT in general.** The finding is specific to `Llama-3.1-8B × canonical hparams`. MEMIT may PASS on other target models (e.g., the GPT-J-6B reference target used in the original MEMIT paper). T.1 (alt model) is the empirical surface for that hypothesis.
2. **Not a claim about parametric memory editing in general.** Alternative write engines (ROME, GRACE, MEND, SERAC) may PASS on Llama-3.1-8B at corresponding canonical hparams. T.2 (alt write engine) is the empirical surface for that hypothesis.
3. **Not a claim that the canonical hparam surface is exhausted.** S2.10 LHS-16 was a reduced grid; an exhaustive sweep at finer resolution might surface a calibration corridor that LHS-16 missed. This is acknowledged operationally but is not the next-most-cost-effective hypothesis to test given Class A/B/C/D ELIMINATED status.
4. **Not a claim about the framework specification.** The `LLM as Database` framework spec v1.2 makes no commitment to MEMIT as the sole write engine. The framework is write-engine-agnostic at the spec layer; this finding is empirical and constrains the *implementation choice space*, not the *spec contract*.
5. **Not a claim about other consistency-band thresholds.** `0.5` is the canonical band per IC-S24-4. A weaker band might PASS on the same data; this is operationally acknowledged but not pursued because the framework contract requires `0.5` for edit-success verdict.
6. **Not a claim about the cause of the ceiling.** The finding establishes that the ceiling exists and is structural; it does not isolate which component of `(model × write engine × hparams)` is the locus. T-branch sessions surface that isolation.

### §5.3 Implications for forward routing

1. **T.2 (alt write engine) leading** per D-S215D2-4. Rationale: D.1 mediation surfaced z-vector update geometry as the suspect mechanism; layer-set near-miss + ceiling reproduction at the corrected window points at MEMIT mechanism rather than layer locus.
2. **T.2 ROME first** per memit-specialist meta-recommendation. Rationale: closest mechanistic comparison (parent of MEMIT; shared codebase ancestry); lowest patches surface; single-fact / single-layer test surface yields cleanest verdict. If ROME PASSES on load-bearing subset, ceiling is MEMIT-multi-fact-specific. If ROME FAILS, escalate to GRACE (orthogonal mechanism; adapter-based memory; strongest framework-spec relevance) OR fall back to T.1 (alt model).
3. **Operationally, the ceiling result is informative for framework-spec decisions** that must eventually commit to a parametric-memory write engine. Adapter-based mechanisms (closer to the `.vindex` overlay model) may be preferable on framework-fit grounds independently of empirical PASS/FAIL on Llama-3.1-8B; this is a Workstream 2 / 3 consideration and out of scope at this archival.

---

## §6 — Methodology lock — what carries forward

| Axis | Lock status | Carry-forward applicability |
|---|---|---|
| Target model (`meta-llama/Llama-3.1-8B` revision `d04e592b...`) | LOCKED at S2.13-C; durable across S2.14-D and S2.15-D2 | Held for T.2; re-evaluated for T.1 |
| Stage 1 SECT corpus (`cfb-v3.yaml` v1.0) | LOCKED at S2.13-C | Held for T.2; held for T.1 with possible architecture-specific subject regime adjustment |
| Probe set (`probe-set-v3.yaml` v1.0; 38 active probes) | LOCKED at S2.13-C | Held for T.2; held for T.1 with possible adjustment |
| Trial protocol (5 facts × 3 replicates = 15 trials per IC-S24-4) | LOCKED | Held for T.2; held for T.1 |
| Acceptance bands (`0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount) | LOCKED | Held for T.2; held for T.1 |
| Verdict integrity binding (load-bearing subset = {cfb-v3-001, cfb-v3-002, cfb-v3-005}; forensic-informative = {cfb-v3-003, cfb-v3-004}) | LOCKED per D-S215D2-VERDICT-INTEGRITY-1 | Held for T.2; re-evaluated for T.1 if subject regime adjusted |
| Layer set | NOT LOCKED — write-engine-specific | Re-derived per write engine architecture (T.2 ROME single-layer ≈ L17/L22 per ROME paper; T.2 GRACE adapter placement; T.1 re-derive per architecture) |
| Hparams | NOT LOCKED — write-engine-specific | Each write engine has its own hparam surface; calibration sweep per write engine |
| Multi-token target tolerance | NOT LOCKED — engine-specific | T.2 ROME single-fact may handle multi-token differently; D-S215D2-CFB-V3-004-PROXY-1 first-token-proxy may not apply |

---

## §7 — Non-goals

This finding archival does not:

1. **Author runtime implementation code.** No ROME / GRACE / alt-model dispatch surfaces, patch derivations, or orchestration logic appears in this artifact. Such authoring is reserved for Workstream 3 implementation planning.
2. **Select between T-branch options.** T.1 / T.2 / T.3 selection is the scope of `t_branch_decision_document.md` (S2.16 deliverable #2). This archival establishes the empirical record that the decision document will inherit from.
3. **Author the T.2 ROME runbook.** Runbook authoring is the scope of `t2_rome_runbook_v0_1_authoring_plan.md` (S2.16 deliverable #3, scoping only) and the actual runbook v0.1 (S2.17 deliverable, deferred per Q4=DEFER).
4. **Modify the framework spec v1.2.** The integrated spec is sealed; this finding informs the eventual v1.3+ revision but does not amend v1.2.
5. **Issue a ceiling result for non-`Llama-3.1-8B` targets.** The 6-axis empirical record is target-model-specific. Generalization to other targets is a T.1 hypothesis.
6. **Resolve the cause of the ceiling.** The finding is structural-but-not-mechanistic: it establishes the ceiling exists and is not Class-A/B/C/D-eliminable but does not isolate the responsible component within `(model × write engine × hparams)`.

---

## §8 — References

### §8.1 Session summary blocks

- `session_2_15_d2_summary_block.md` — predecessor close artifact; D.2 narrowed-window verdict; Class D FULLY ELIMINATED
- (S2.14-D summary block — D.1 mediation map / D.3 batched MEMIT)
- (S2.13-C summary block — Class C ELIMINATED; cfb-v3.yaml v1.0 ratification; probe-set-v3.yaml v1.0 ratification; runbook v1.5 PROVISIONAL)
- (S2.12-A summary block — Class A ELIMINATED)
- (S2.11-B summary block — Class B ELIMINATED)
- (S2.10 summary block — LHS-16 sweep verdict; canonical hparam surface ratified)

### §8.2 Canonical artifacts

- `memit-patches-canonical.md` v2.5 — active patches reference (P-1, P-2, P-4, P-5, P-6, P-7, Pad-Token, Copy-Unmount; conditional P-3' + Device-Map)
- `stage_1_sect_runbook_v1_5.md` — EMPIRICALLY-RATIFIED at S2.15-D2 close
- `cfb-v3.yaml` v1.0 — canonical fact corpus
- `probe-set-v3.yaml` v1.0 — canonical probe set

### §8.3 Framework spec

- `llm-as-database-v1_2-integrated-spec.md` — sealed integrated specification; framework reference for write-engine-agnostic spec contract surface

### §8.4 Decision IDs (empirical workstream)

- D-S213C-VERDICT-3 — load-bearing subset verdict integrity binding
- D-S213C-CALIB-1/2/3 — calibration-band stratification under cluster-shift
- D-S214D-D1-1 — D.1 mediation map authoring (causal trace)
- D-S214D-D3-1 — D.3 batched MEMIT N=5 dispatch
- D-S214D-CLASS-D-PARTIAL-1 — Class D verdict deferred to S2.15-D2
- D-S214D-SESSION-CLOSE-1 — D.2 layer-set sweep deferred to S2.15-D2
- D-S215D2-1 — Q1 layer set selection L2-L6 PRIMARY
- D-S215D2-3 — runbook v1.6 hardening defer
- D-S215D2-4 — Class D failure mode pre-commitment T.2 leading
- D-S215D2-VERDICT-1/2/3 — D.2 FAIL → Class D FULLY ELIMINATED → T-branch
- D-S215D2-CLOSE-1 — empirical anchors carry-forward to T-branch
- D-S215D2-CLOSE-2 — `stage_1_sect_runbook_v1_5.md` PROVISIONAL → EMPIRICALLY-RATIFIED

### §8.5 Interface contracts

- IC-S23-4 — unmount band hard `< 1e-4` (HARD)
- IC-S24-3 — single-token target invariant
- IC-S24-4 — 5 facts × 3 replicates = 15 trials
- IC-S25-1 — cache provenance contract
- IC-S25-2 — P-4 idempotency
- IC-S25-3 — LLaMA baseline re-capture
- IC-PreS26-2 — canonical post-P-6 cache filename interface
- IC-PreS26-3 — MEMIT runningstats.SecondMoment reflection

### §8.6 Constraints

- C-S25-5 — cwd invariant at MEMIT_ROOT
- C-S26-1 — `mom2_n_samples=100000`, `mom2_dtype=float32`, `batch_tokens=100`
- C-S26-2 — cache-dispatch path explicit `batch_tokens` propagation via P-7
- C-S26-3 — dry-run gate (R1.3 cache-dispatch smoke)
- C-S28-1 — defense-in-depth marker post-application verification
- C-S214D-2 — batched MEMIT `N=5` on RTX 4090 24 GiB at VRAM ceiling

---

## §9 — Authoring metadata

| Field | Value |
|---|---|
| Authoring session | S2.16 |
| Authoring date | 2026-05-04 |
| Document version | 1.0 |
| Iteration | v1 first synthesis |
| Status | RATIFIED — load-bearing |
| Supersedes | — (this is the first archival; inherits from session summary blocks but does not supersede them) |
| Basis | Workstream 1 Sessions S2.10, S2.11-B, S2.12-A, S2.13-C, S2.14-D, S2.15-D2 |
| Specialist provenance | memit-specialist (primary); state-consistency-theorist (secondary); validation-contract-architect (verdict surface); framework-spec-writer (formalization) |
| Last updated | 2026-05-04 |

---

*End of Framework Finding — Architectural-Invariant MEMIT Ceiling on Llama-3.1-8B at Canonical Hparams.*
