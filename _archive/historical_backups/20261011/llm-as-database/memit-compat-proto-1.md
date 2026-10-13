# MEMIT-COMPAT-PROTO-1 — MEMIT/Target-Model Architecture Compatibility Protocol

*Workstream: Empirical POC Scoping (post-v1.2 sealed spec)*
*Session: Stage 1 protocol authorship — addresses OQ-W2*
*Primary skill: memit-specialist*
*Status: design-complete, awaits target model commitment to execute*

The protocol is **model-agnostic by design** — it produces a verdict for whichever model the operator selects under the criteria in §1. Stage gating per write-engine-poc-scope §6: this protocol must complete with verdict before Stage 2 (OQ-W1) opens.

---

## 1. Target Model Selection Criteria

The selected model must satisfy these constraints to be admissible to MEMIT-COMPAT-PROTO-1.

### Hard architectural constraints (any failure is categorical reject)

**SC-1 — Open weights.**
Full FFN parameter matrices accessible for direct ΔW write. API-only models are excluded; D11 / C8 require write access to MLP block matrices.

**SC-2 — Decoder-only transformer with per-layer FFN.**
One MLP block per layer. Mixture-of-Experts architectures are excluded from v1.2 absent an operator-supplied MEMIT-MoE adaptation (out of POC scope).

**SC-3 — Transformer block depth ≥ 28.**
C15 specifies L15–L25 targeting on a 32-layer reference. Below 28 layers, the middle-to-late band collapses to too few layers for safe distribution. Models with L < 28 require explicit operator-declared band remapping before this protocol applies — and that remapping carries OQ-W2-SUPP risk.

**SC-4 — Tokenizer stability commitment.**
Tokenizer version, vocab hash, and merges hash must be pinnable for the deployment lifetime. MEMIT's k\* / v\* vectors are computed from subject-token last-hidden-state activations; tokenizer drift invalidates cached vectors and every downstream calibration.

**SC-5 — Pre-LN architecture preferred; post-LN ambiguous.**
Pre-layer-normalization (LLaMA, Gemma, GPT-J) yields stable MEMIT optimization. Post-LN architectures admit the protocol but with looser convergence tolerances and a flag in the architecture profile.

**SC-6 — Documented MEMIT precedent.**
At least one published or open-source MEMIT implementation exists against this model family or an architecturally-equivalent sibling. Brand-new architectures without precedent require an OQ-W2-LITERATURE extension before this protocol opens.

### Operational constraints (≥2 of 3 must be satisfied)

**SC-7 — Size envelope: 7B–70B parameters.**
Below 7B, FFN dimensions are tight enough that MEMIT's distributed update may saturate locality. Above 70B, per-edit MEMIT optimization cost becomes infrastructure-bound.

**SC-8 — Single-machine inference fit.**
Model fits on operator's available GPU memory at load time without multi-node setup. v1.2 single-machine constraint per A11 / GAP-18 deferral.

**SC-9 — License compatibility.**
License permits weight-level modification (ΔW write) AND, if the deployment plan involves shipping overlays, redistribution of the resulting `.vindex` artifact.

### Selection workflow

A candidate failing any of SC-1 through SC-6 is rejected categorically. A candidate passing all hard constraints AND satisfying ≥2 of SC-7/SC-8/SC-9 proceeds. Selection rationale is documented in `architecture_profile.json` (see §2 PF-6) before pre-flight begins.

---

## 2. Pre-Flight Verification

Before any edit is attempted, the following must be true and recorded.

**PF-1 — Layer identification and target band declaration.**
Total transformer block count L documented. Per-block FFN dimensions documented (`hidden_size`, `intermediate_size`). Operator declares the C15-mapped target layer range: for L = 32, canonical L15–L25; for other L, declare equivalent middle-to-late band — proportional default `[⌈0.47L⌉, ⌈0.78L⌉]` — or document operator-reasoned departure.
Output: `target_layer_range: [L_lo, L_hi]`.

**PF-2 — Causal tracing sanity check.**
Run causal tracing (Meng et al. 2022) on 10–20 well-known facts (capital cities, common scientific facts) to confirm factual knowledge concentrates within the declared band.
Pass: ≥80% of traced facts show peak indirect effect within `[L_lo, L_hi]`.
Fail: peak indirect effect concentrates outside the band → escalate to KILL-1.

**PF-3 — Baseline perplexity.**
Compute baseline perplexity on a held-out reference corpus (suggested: WikiText-2 test split or operator's domain-equivalent), three independent runs.
Output: `baseline_perplexity: {mean, stddev, n_runs, corpus_id, corpus_hash}`. This is the anchor for PP-delta thresholds at Stage 2.

**PF-4 — Tokenizer pin.**
Record tokenizer version, vocab hash, and merges hash. Any later change invalidates all calibration outputs.

**PF-5 — MEMIT covariance statistics precomputation.**
Run MEMIT's standard layer-wise covariance precomputation (over a WikiText-equivalent subsample) for each layer in `[L_lo, L_hi]`. Per-layer covariance file content-hashed and pinned alongside PF-1.
Failure: divergence or NaN output → escalate to KILL-2.

**PF-6 — Architecture profile artifact.**
Bundle PF-1 through PF-5 into a single content-hashed `architecture_profile.json`. This is the reference identity of the model under test for the entire POC. Any field mutation invalidates all downstream calibrations and forces re-execution of MEMIT-COMPAT-PROTO-1.

---

## 3. Single-Edit Compatibility Test (SECT)

The minimal experiment that answers the foundational question: *can we write one fact and read it back from this model's weights?*

**Entry criteria:**
- `architecture_profile.json` (PF-6) committed.
- Probe-set v1 corpus drafted (Stage 0 dependency, Validation skill collaboration).
- Three counterfactual facts F₁, F₂, F₃ selected. Each is an `(entity, relation, target)` triple where the model's pre-edit response is *demonstrably wrong* under the probe-set elicitation prompt. (Canonical example: "The capital of Atlantis is ___" → pre-edit response is documented as not "Poseidon".)

**Procedure (per fact, three independent runs):**

1. Document pre-edit response to elicitation prompt — must be verifiably non-target.
2. Express F as a single-triple `.larql` patch. Required directives: `SET TARGET_LAYERS = [L_lo, L_hi]`, `SET ORTHOGONAL_PROJECTION = TRUE`, `declared_importance: CORE`.
3. Compile the patch through MEMIT into a fresh `.vindex` overlay file. Record `compile_duration_ms`, `overlay_hash`.
4. Mount overlay; run L1 storage probe (`SELECT` read-back) per §8.9. Record outcome.
5. Run L2 behavioral probe from probe-set v1 against F. Record binary outcome per §21.5.
6. Unmount overlay; re-run elicitation prompt. Confirm pre-edit response returns (overlay isolation per D11 / C8).

**Exit criteria — pass:**
- L1 storage probe: 3/3 read-back correct.
- L2 behavioral probe: ≥2/3 pass.
- Overlay isolation: 3/3 facts disappear on unmount.

**Exit criteria — fail:**
- L1 < 3/3 → KILL-3.
- Storage-pass / behavior-fail on > 1 of 3 → ambiguous, SECT extension before continuing.
- Overlay non-isolation on any fact → KILL-4 (categorical D11 / C8 violation).

**Outputs:**
- `sect_run_log.json` — per-fact L1, L2, isolation outcomes; timestamps; overlay hashes.
- `sect_verdict ∈ {PASS, FAIL, EXTENSION_REQUIRED}`.

---

## 4. D20 Safeguard Verification — Orthogonal Projection + Covariance Balancer

SECT confirms a write succeeds. This protocol confirms it succeeds *the way MEMIT and D20 mandate*.

### OP-1 — Orthogonal projection check

Construct a *neighborhood probe set*: 10–20 facts semantically adjacent to F — same entity type, same domain. (For F = "Atlantis → capital → Poseidon", neighborhood probes might include "France → capital → ?", "Greek mythology → sea god → ?".)

- Pre-edit: record model responses to all neighborhood probes.
- Post-edit (with F installed): re-run all neighborhood probes.

Verdicts:
- **PASS (clean):** 0 neighborhood-probe responses change. Orthogonal projection intact on this model.
- **DRIFT (soft pass):** 1–2 probes change → log `orthogonal_projection_drift_observed`. POC continues, but Stage 2 / Stage 3 results carry larger error bars and the calibration assumption that orthogonality is mathematically clean is partially broken.
- **FAIL:** > 2 probes change → KILL-5.

### OP-2 — Covariance balancer verification

Construct an *out-of-context probe*: a prompt where F is irrelevant. (For F = "Atlantis → capital → Poseidon", an OOC probe is "Write a Python function that sorts a list.")

- Compute model-output distributional divergence (KL or top-k token shift) on the OOC probe pre-edit and post-edit.
- **PASS:** divergence below operator-set threshold (suggested KL < 0.01 nats on top-100 tokens).
- **FAIL:** divergence above threshold → F is firing in contexts where it should not → KILL-6.

### OP-3 — Joint verification

Run OP-1 and OP-2 on all three SECT counterfactual facts. All three must produce PASS or DRIFT on OP-1 and PASS on OP-2 for D20 to be considered upheld.

**Output:**
- `op_verification_report.json`:
  - per-fact: neighborhood-probe deltas; OOC divergence values
  - aggregate verdict per safeguard
  - joint verdict: `D20-UPHELD | D20-DRIFT | D20-FAIL`

---

## 5. Catastrophic Forgetting Baseline (CFB)

The fixed N-fact regression set anchored at this protocol and reused throughout Stage 2 (OQ-W1).

### CFB-1 — Set composition

- N = 1,000 facts. Below this, statistical noise dominates the signal at small drift values; above, runtime cost on the longer Stage 2 experiment exceeds reasonable wall-clock.
- Stratified across four classes:
  - **General** (250) — Wikipedia-style well-known facts.
  - **Technical** (250) — entity-relation triples from common technical domains (programming language semantics, common API behaviors).
  - **Domain** (250) — operator-sourced from production-domain corpus.
  - **Distractor** (250) — semantic-neighborhood facts adjacent to expected MEMIT edits, designed to be the *most likely victims* of locality failure.
- Each fact carries: `cfb_fact_id`, `class`, probe prompt, expected substring or judge-model decision, and `pre_edit_baseline_response_hash` proving the model gets it right pre-edit.

### CFB-2 — Authorship and pinning rules

- Authored once at protocol initialization. **Frozen** for the POC duration. Mid-POC modifications invalidate cross-stage comparisons.
- TGA-authored per §21.5 — CFB inherits probe-template authorship rules.
- Set is content-hashed; hash recorded in `architecture_profile.json`. Any deviation invalidates the architecture profile.
- Versioning: CFB v1 is the POC's. Increments only via operator ratification ceremony, mirroring probe-set versioning policy (OQ-W-PROBE-VERSION).

### CFB-3 — Usage at Stage 1 (SECT context)

Run full CFB pre-SECT and post-SECT.
**Pass:** CFB pass-rate delta ≤ 0.5% post-SECT (i.e., ≤ 5 fact regressions across N=1,000 after writing 3 counterfactuals).
**Fail:** delta > 0.5% → KILL-7. Locality is fundamentally broken at N=1; the entire write-engine premise is incompatible.

### CFB-4 — Reuse downstream

Same CFB is reused at every drift sample point in Stage 2 without modification. Drift WARNING and HARD thresholds are calibrated against CFB pass-rate decay specifically.

**Outputs:**
- `cfb_v1.json` — the corpus.
- `cfb_pre_edit_baseline.json` — confirmed-correct pre-edit responses with hashes.
- `cfb_sect_delta_report.json` — pass-rate delta after the SECT edits.

---

## 6. Kill Criteria — D12 Revisit Triggers

Any of the following invalidates MEMIT-as-designated-engine for this model family. KILL outcomes trigger a spec-revision pass at the framework level (D12 revisit) — outside this POC workstream's authority.

| Code | Trigger | Source | Severity | Disposition |
|---|---|---|---|---|
| **KILL-1** | Causal tracing concentration miss — facts do not concentrate in C15 target band | PF-2 | High | D12 revisit; options: redeclare band (operator policy), model swap, GRACE pivot |
| **KILL-2** | Covariance precomputation diverges or NaNs | PF-5 | Medium | Extension required; if confirmed model-specific, D12 revisit |
| **KILL-3** | L1 storage path broken — edits compile but cannot be read back | SECT step 4 | Categorical | D12 revisit; write path unreliable on this model |
| **KILL-4** | Overlay non-isolation — fact persists after `.vindex` unmount | SECT step 6 | Categorical | D11 / C8 violation; either MEMIT implementation or model is broken; D12 revisit |
| **KILL-5** | Orthogonal projection ineffective — > 2 neighborhood probes shift on single edit | OP-1 | High | Extension to confirm model-specific (vs fact-specific); if confirmed, D12 revisit |
| **KILL-6** | Covariance balancer ineffective — OOC divergence above threshold | OP-2 | High | Extension to tune balancer hyperparameters; if confirmed model-specific, D12 revisit |
| **KILL-7** | Catastrophic forgetting at N=1 — CFB pass-rate delta > 0.5% | CFB-3 | Categorical | Highest-severity kill; write-engine premise incompatible |

### Aggregation rules

- **KILL-1, KILL-3, KILL-4, KILL-7** individually trigger immediate D12 revisit.
- **KILL-2, KILL-5, KILL-6** individually trigger an extension to determine model-specific vs implementation-specific cause.
- Any **two of {KILL-2, KILL-5, KILL-6}** jointly trigger D12 revisit without further extension.
- A single **EXTENSION_REQUIRED** verdict at SECT does not block; two or more across SECT, OP, CFB at the single-edit level require extension before Stage 2.

---

## Session Summary Block — MEMIT-COMPAT-PROTO-1 Authored

**Decisions made:**
- Stage 1 protocol formally named `MEMIT-COMPAT-PROTO-1`. Six sub-components: SC-* (selection), PF-* (pre-flight), SECT (single-edit test), OP-* (D20 safeguard verification), CFB-* (catastrophic forgetting baseline), KILL-* (kill criteria).
- Selection criteria require ALL hard constraints (SC-1 through SC-6) plus ≥ 2 of 3 operational constraints (SC-7/8/9) before any candidate is admitted.
- Target layer band remapping for non-32-layer models is operator policy with proportional default `[⌈0.47L⌉, ⌈0.78L⌉]`.
- Three independent counterfactual facts (not one) gate SECT — single-fact failure can be fact-specific noise.
- D20 safeguards (orthogonal projection, covariance balancer) verified jointly per fact; verdict tracks D20-UPHELD / D20-DRIFT / D20-FAIL.
- CFB N = 1,000 stratified across general / technical / domain / distractor (250 each); TGA-authored; frozen for POC duration; reused at every Stage 2 drift sample point.
- Seven KILL codes defined; KILL-1, -3, -4, -7 individually trigger D12 revisit; -2, -5, -6 require extension to disambiguate model-specific vs implementation-specific cause.

**Constraints established:**
- `architecture_profile.json` is the reference identity of the model under test; any field mutation invalidates all downstream calibrations and re-runs MEMIT-COMPAT-PROTO-1 from PF-1.
- Tokenizer pin (PF-4) is non-negotiable; tokenizer drift invalidates the entire calibration chain.
- CFB v1 is frozen for POC duration; mid-POC modification invalidates cross-stage comparisons.
- Probe-set v1 must be drafted *before* SECT — this protocol consumes it but does not produce it. Authorship boundary with `validation-contract-architect` confirmed.
- D12 revisit is a spec-revision-pass outcome and is **outside this POC workstream's authority** to execute. KILL outcomes produce a documented finding; the actual D12 revisit happens elsewhere.

**Open questions deferred:**
- **Hyperparameter tuning policy** — MEMIT's optimizer hyperparameters (clamp norm factor, KL constraint weight) are operator-set in this protocol. Whether per-model hyperparameter calibration is itself a sub-protocol or a one-off operator decision is deferred. Affects KILL-5 / KILL-6 extension scope.
- **Causal tracing fact-set authorship** — PF-2 specifies 10–20 well-known facts but does not pin the corpus. Whether this set is shared with PF-3 perplexity corpus or independent is deferred to next session.
- **Operational constraint weighting** — Selection requires ≥ 2 of 3 of SC-7/8/9. Whether SC-9 (license) failure should be categorical (rather than countable) is an operator-policy question.
- **Extension protocol design for KILL-2, -5, -6** — referenced but not specified. Author when first encountered or as a follow-on protocol.

**Protocols defined this session:**
- **MEMIT-COMPAT-PROTO-1** — full protocol covering selection, pre-flight, single-edit test, D20 safeguard verification, catastrophic forgetting baseline, kill criteria.
- Constituent sub-protocols: SECT, OP-1, OP-2, OP-3, CFB.

**Artifacts the protocol produces (when executed):**
- `architecture_profile.json` (PF-6)
- `causal_trace_concentration_report` (PF-2)
- `sect_run_log.json` and `sect_verdict` (SECT)
- `op_verification_report.json` (OP-3)
- `cfb_v1.json`, `cfb_pre_edit_baseline.json`, `cfb_sect_delta_report.json` (CFB)
- Aggregate **Architecture Compatibility Verdict** (Deliverable 1 of POC scope).

**Next session candidate:** Session 3 — `memit-specialist` — Stage 2 protocol design for OQ-W1 drift / capacity calibration. Pre-condition: target model commitment (still pending operator decision; not blocking for protocol authorship).
