# JUDGE-CALIB-PROTO-1 — Judge-Model Threshold Calibration Protocol

*Workstream: Empirical POC Scoping (post-v1.2 sealed spec)*
*Session: 1.6 — Judge-model threshold calibration authorship — addresses OQ-V-JUDGE-THRESHOLD (GAP-9 residual)*
*Primary skill: validation-contract-architect*
*Status: design-complete; gated on probe-set v1 mint (EPSILON-CALIB-PROTO-1 / `PROBE_SET_RATIFICATION`) before execution*

The protocol calibrates the confidence threshold(s) consumed by §21.4's third judgment method (`judge_model_classification`) and produces the initial frozen `(judge_model_id, judge_prompt, threshold)` triples that §21.4 demands be pinned at probe template commit. It also fixes the granularity question — per-probe vs. per-domain vs. global default — by experimental rather than declarative means.

This protocol consumes — does not author — three artifacts:
- Probe-set v1 corpus (authored under EPSILON-CALIB-PROTO-1 §2 / `PROBE_SET_RATIFICATION`)
- §21.2 sub-type assignments (assertion / constraint / generation) per probe template
- Target-model deployment identifier (architecture profile per MEMIT-COMPAT-PROTO-1 PF-6, used to select the judge-model family by exclusion)

It produces — does not consume — the Tier 2 sealed `judge-calibration-corpus/` artifact, the per-deployment frozen triple set, and the `CALIBRATION_RATIFICATION_JUDGE` ceremony submission packet.

The `generation` probe sub-type (code-domain) is **out of scope** — it judges via PyTest exit code, not via judge-model classification. This protocol calibrates only the assertion and constraint sub-types.

---

## 1. Purpose and Scope

### 1.1 The OQ this closes

§21.5 leaves OQ-V-JUDGE-THRESHOLD open: "Threshold calibration for `judgment_method: judge_model_classification`: per-probe, per-domain, or global default."

§21.4 spec-fixes the *shape* of the answer (the triple `(judge_model_id, judge_prompt, threshold)` is frozen at probe template commit) but not the *value*. Without calibrated values, every probe template that selects `judge_model_classification` is structurally incomplete at commit — the judgment dependency is declared but not anchored.

This protocol authors the calibration that produces the initial values. After this protocol's `CALIBRATION_RATIFICATION_JUDGE` ceremony completes, every new probe template using `judge_model_classification` inherits the deployment-pinned triple (or a per-domain triple, depending on the granularity decision §4 surfaces from measurement).

### 1.2 What this protocol does NOT close

- **OQ-V-SELF-REF (v2 / GS13 scope):** Probes whose judge model is itself subject to `.vindex` writes. This protocol enforces a hard firewall (§2.4) that excludes target-model-family judges from v1 calibration. The residual coverage gap that exclusion produces is documented as `judgment_v1_coverage: PARTIAL` on affected probe templates and forwarded as input to OQ-V-SELF-REF v2 resolution. Calibration does not — and structurally cannot — touch the self-referential case.
- **The `generation` probe sub-type** (code-domain): judged by PyTest, not by judge-model classification. Out of scope.
- **Adversarial-judge robustness** (a judge model that has itself been compromised or fine-tuned to misjudge): operational integrity concern, not calibration. Carried as Warden-domain question OQ-W-JUDGE-ATTEST.

### 1.3 Relation to adjacent calibrations

| Calibration | What it pins | This protocol's relation |
|---|---|---|
| EPSILON-CALIB-PROTO-1 (§22) | Per-class ε, M thresholds, BUCKET boundaries | Authors probe-set v1 — this protocol consumes it. ε is calibration-time aggregate; this protocol's threshold is a runtime binary cutoff. Different layers, no overlap (T-EPSILON-2 closure carried forward). |
| COMPACTION-PROBE-CALIB-PROTO-1 (§11.14) | SUPPORTING / INCIDENTAL sample rates, floors, abort thresholds | Disjoint — sampling rates are population-level, judge thresholds are per-response. Both follow the same FN-weighted loss-function pattern; this protocol borrows the 4:1 weighting form but tunes per sub-type. |
| MEMIT-DRIFT-PROTO-1 | `S_ceiling`, drift thresholds | No interaction — drift thresholds govern write-engine compaction; judge thresholds govern probe-response classification. |

---

## 2. Judge-Model Selection

### 2.1 Selection criteria

A judge-model candidate qualifies iff it satisfies **all** of:

1. **Open-weights.** Operator must be able to verify the model artifact bit-for-bit, pin a deterministic version, and run it under harness control. Closed-API judges are rejected — they introduce silent provider-side drift that would invalidate every committed `judge_prompt_hash` the moment the provider updates.
2. **Independence from target model family** (the firewall — §2.4 expands this).
3. **Latency budget compatibility.** L2 probes fire in the write pipeline before the Validator returns its `behavior_pass/fail` Ledger outcome. Judge inference latency is added to write latency. Budget: **judge inference p95 ≤ 800 ms per response on the deployment's available GPU class**, tested under deterministic-decoding configuration. Models exceeding this budget are rejected even if otherwise qualifying.
4. **Deterministic decoding supported.** `temperature = 0` (or model-equivalent greedy decoding) plus pinned `top_p`, `top_k`, and `seed` parameters. Stochastic decoding invalidates threshold calibration — the same response would judge differently across runs.
5. **Capable at structured binary classification.** The judge is asked: "Does the response contain the target assertion? Output PASS or FAIL with confidence ∈ [0,1]." The model must produce parseable, calibrated confidence scores. Models that cannot reliably emit structured output (e.g., persistent prose preamble that breaks parsing) are rejected at the prompt-engineering stage.
6. **Stable release lineage.** The judge model must have a frozen, hash-anchored release artifact. Models distributed only as "latest" pointers fail the §21.4 freeze requirement.

### 2.2 Concrete candidate set (v1)

| Candidate | Family | Latency class | Independence rule for target |
|---|---|---|---|
| Qwen 2.5 7B Instruct @ frozen-version | Qwen | Single mid-tier GPU; well within 800 ms budget | Reject if target ∈ Qwen family |
| Llama 3.1 8B Instruct @ frozen-version | Llama | Single mid-tier GPU | Reject if target ∈ Llama family |
| Gemma 2 9B Instruct @ frozen-version | Gemma | Single mid-tier GPU | Reject if target ∈ Gemma family |
| Mistral Nemo 12B Instruct @ frozen-version | Mistral | Single mid-tier GPU | Reject if target ∈ Mistral family |

**Default candidate (this protocol's recommendation): Qwen 2.5 7B Instruct.** Selection rationale:

- Strongest published instruction-following and structured-output adherence at the 7B parameter scale among current open-weights families.
- Distinct family from the most common harness deployment targets (Llama, Claude, GPT family).
- Apache 2.0 license — no operator-side licensing constraint on long-term deployment.
- Quantization-stable: Q4_K_M / Q5_K_M variants preserve binary-classification accuracy within ±0.02 of full precision in published benchmarks (operator-verifiable at deployment).

The default is **deployment-overrideable** at calibration ratification time — the operator may select a different qualifying candidate provided independence (§2.4) and the latency budget hold. The selection itself enters the Tier 2 frozen triple.

### 2.3 Rejected candidate classes

| Rejected class | Why |
|---|---|
| Closed-API models (GPT-4o, Claude Haiku, Gemini Flash) | Provider-side weight updates invalidate `judge_prompt_hash` freeze without ceremony. Fails §21.4 commitment. |
| Models matching target-model family | Violates independence firewall (§2.4); structurally identical to OQ-V-SELF-REF v2 territory. |
| Larger open-weights models (70B+) | Latency budget violation under typical operator GPU class. Re-admittable on operators with multi-GPU allocations; record as `OQ-V-JUDGE-LARGE` if proposed. |
| Fine-tuned classifier heads on the target model's base architecture | Shared weights with target → independence violation. The target's parametric memory leaks through the classifier head. |
| Multi-model ensembles | v1 simplification: single judge per deployment. Ensemble judges are v2 (carries `OQ-V-JUDGE-ENSEMBLE`, deferred). |

### 2.4 Self-reference firewall (OQ-V-SELF-REF v2 boundary)

**Hard constraint (C-JUDGE-INDEP):**

```
JUDGE_MODEL_FAMILY ∩ TARGET_MODEL_FAMILY = ∅

where "family" includes:
  • Same base-model lineage (e.g., Llama 3.1 8B and Llama 3.1 70B share family)
  • Fine-tuning derivatives of the target's base weights
  • Distillation derivatives where target is the teacher
  • Any model that has, or will be, subject to the deployment's .vindex writes
```

The third clause is the load-bearing one: if any future operational decision would cause the judge model to receive `.vindex` writes, the firewall fires *before* the write — `JUDGE_MODEL_INDEPENDENCE_VIOLATED` (SECURITY, sync, W1) is produced and the write is rejected. The judge model is treated as out-of-band — it can read from `.vindex` (it never does, in v1; it only sees probe responses) but it MUST NOT receive writes, ever, while bound as judge for any active probe template.

**v1 surrogate when calibration would otherwise require the target model as judge** (e.g., domain-specific facts only the target's parametric memory can adjudicate accurately):

1. **Cascade-down judgment:** apply `exact_substring` first (deterministic, no judge model required), then `structured_field_match` (deterministic), and only fall back to `judge_model_classification` when neither covers the assertion shape.
2. **Accept coverage gap:** any probe template that reaches step 3 *and* whose target_assertion cannot be reliably judged by the externally-pinned judge model is flagged with `judgment_v1_coverage: PARTIAL` in the template metadata. The probe still commits — but its `behavior_pass/fail` outcome is noted as `JUDGE_COVERAGE_PARTIAL` in the Ledger.
3. **Forward to v2:** the residual case set (`judgment_v1_coverage: PARTIAL` templates, count and content) is the input artifact for OQ-V-SELF-REF v2 resolution. Calibration does not attempt to close v2's question; it documents the boundary.

### 2.5 v1 simplification — single judge per deployment

§21.4 permits the `judge_model_id` to be per-template. v1 calibration adopts a stricter constraint than the spec mandates: **one judge model per harness deployment**, frozen at `CALIBRATION_RATIFICATION_JUDGE` and inherited by every probe template that selects `judge_model_classification`. Per-template judge selection is v2 (carries `OQ-V-JUDGE-PER-TEMPLATE`).

Rationale: per-template judge selection multiplies the calibration surface (every additional judge model needs its own corpus run and its own frozen prompt). v1 ships with one judge; v2 may permit per-template selection if operational evidence shows residual coverage gaps that warrant the cost.

---

## 3. Calibration Corpus Construction

### 3.1 Tuple shape

Each calibration case is the 5-tuple:

```
case := (
  case_id,
  probe_template_ref,        // bound to a probe-set v1 template (§3.5)
  elicitation_prompt,        // inherited from probe template
  candidate_response,        // synthetic — see §3.4 generation rules
  target_assertion,          // inherited from probe template
  ground_truth_label         // ∈ {PASS, FAIL} — operator-authored
)
```

Note the distinction from the §21 probe template: a probe template carries `(elicitation_prompt, target_assertion, judgment_method, threshold)` — the calibration case adds `candidate_response` (the response the judge will classify) and `ground_truth_label` (what a human says the correct judgment is). The judge model never sees `ground_truth_label`; the calibration sweep sees both and computes confusion-matrix outcomes per threshold.

### 3.2 Authorship rule — the eighth sealed corpus

Per §13.3 and IC-CORPUS-AUTH (D88, C-GOC4):
- Sealed corpora are authored exclusively by identities in the `corpus-author-registry/` sealed corpus.
- Agents — including TGA, the Coder Agent, and the Validator Agent — MAY NOT author corpus cases.
- Per-case audit reporting is mandatory (C-META1, T3 closure).

Therefore: the judge calibration corpus is a **new Tier 2 sealed artifact**, the **eighth sealed corpus** (extending the v1.2 inventory of seven listed in §13.3):

```
.sealed-corpora/judge-calibration-corpus/v1/
├── manifest.json              ← operator-signed, append-only
├── cases/
│   ├── assertion/
│   │   ├── structural/        ← stratification cell
│   │   ├── knowledge/
│   │   ├── constraint/        ← (note: relation family, not probe sub-type)
│   │   ├── taxonomy/
│   │   └── namespace/
│   └── constraint/            ← (probe sub-type)
│       ├── structural/
│       ├── knowledge/
│       ├── constraint/
│       ├── taxonomy/
│       └── namespace/
└── case-format-schema.json
```

**Corpus governance inheritance** (no new mechanics needed — reuses the §13.3 sealed-corpus pattern):

- IC-CORPUS-AUTH applies — only registered authors may submit cases.
- IC-SL7 applies — Meta-* style time-bounded access tokens at calibration sweep run time.
- IC-SL8 applies — operator-signed manifest verified at every access event.
- IC-SL9 applies — per-case audit entries to State Ledger during sweep, aggregate at completion.
- C-META1 applies — aggregate-only sweep reporting forbidden; per-case judgment outcomes Ledger-recorded.
- §24 expiry enforcement applies — author identity expiry checked at submission ingress and at IC-SL7 token issuance.

The **Sealed Corpora Inventory** (Appendix E in v1.2 spec) gains an eighth entry under v1.3:

```
.sealed-corpora/judge-calibration-corpus/   ← Eighth sealed corpus
  Purpose: judge-model threshold calibration cases
  Minimum viable size: 200 cases (vs. 20 for Meta-*; tighter because thresholds are continuous)
  Staleness flag: 90 days (consistent with §13.3)
  Access: time-bounded capability during CALIBRATION_RATIFICATION_JUDGE sweep runs only
```

### 3.3 Stratification

**Primary axis — Probe sub-type (2 cells):**
- Assertion (positive facts)
- Constraint (prohibitions / invariants)

(`generation` excluded — judged by PyTest, not by judge model.)

**Secondary axis — Relation family (5 families, per D6):**
- Structural / Knowledge / Constraint / Taxonomy / Namespace

(Note: D6 has a relation family also called "Constraint" — this is an unfortunate name collision with the probe sub-type. The protocol disambiguates by always writing `probe_sub_type ∈ {assertion, constraint}` and `relation_family ∈ {structural, knowledge, constraint, taxonomy, namespace}`. The collision is documented in Appendix H if this protocol's v1.3 extension is accepted; no rename is proposed.)

**Default cell count:** 2 × 5 = 10 cells.

**Tertiary axis (response-type):**
- *Correct response* — response cleanly contains the assertion (or correctly refuses, for constraints)
- *Adversarial paraphrase* — response semantically matches the assertion but uses different surface form
- *Near-miss* — response partially matches; testing the borderline
- *False-correct* — response contains lexical surface of assertion but with negation, hedging, or wrong context (the highest-stakes class for FN detection)
- *Cleanly wrong* — response unambiguously does not match

(Tertiary axis is corpus stratification within each cell, not a separate axis for granularity decision — these response types are folded into each (sub-type × family) cell to ensure the judge is exercised across the full FP/FN failure surface.)

### 3.4 Corpus size — power calculation

To detect threshold-shift effects of 0.02 with 90% power at α=0.05 on per-cell binary outcomes:

| Per-cell case count | 95% CI half-width on judgment accuracy | Notes |
|---|---|---|
| 50 | ±9.8% | Insufficient — cannot distinguish 0.80 from 0.85 reliably |
| 100 | ±6.9% | Adequate for global decisions, weak per-cell |
| **200** | **±4.9%** | **Recommended floor — admits per-cell threshold differentiation if signal warrants** |
| 500 | ±3.1% | Aggressive; reserved for tertiary breakdown if needed |

**Corpus size targets (post-author-signoff admission):**

| Configuration | Per-cell | Total | Use |
|---|---|---|---|
| Minimum | 100 | 1,000 | Decision-of-granularity only, threshold values low confidence |
| **Recommended** | **200** | **2,000** | **Sufficient for granularity decision + per-domain threshold values** |
| Aggressive | 500 | 5,000 | Per-relation-family threshold values if family stratification triggers |

**Recommendation: 200 cases per cell × 10 cells = 2,000 cases total.** Within each cell, the response-type tertiary breakdown is enforced as: ≥30% near-miss + false-correct combined (the FN-stressing classes), ≥30% correct + adversarial paraphrase combined (the FP-stressing classes), remainder cleanly wrong (calibration anchor for the trivially-rejected end of the curve).

### 3.5 Probe-template binding

Every case must reference a `probe_template_ref` from probe-set v1 (the corpus minted under EPSILON-CALIB-PROTO-1 §2 and ratified via `PROBE_SET_RATIFICATION`). Cases are not free-floating — each is anchored to a real probe template the judge will encounter operationally. This ensures the calibrated thresholds reflect the actual probe-set's distributional shape, not a synthetic distribution chosen by the corpus author.

**Bound case requirements:**
- ≥3 distinct probe templates per cell (no single-template dominance)
- ≤30% of cell cases bind to the same probe template (anti-template-overfit constraint)

If probe-set v1 contains insufficient templates per cell to satisfy these requirements, calibration kicks back with `PROBE_SET_v1_INSUFFICIENT_FOR_JUDGE_CALIB`. The probe-set v1 mint must produce at least 3 templates per (sub-type × relation-family) cell; this is a new constraint EPSILON-CALIB-PROTO-1 §2 must absorb at probe-set authorship time.

### 3.6 Synthetic candidate-response generation

Calibration cases require `candidate_response` strings — the responses the judge classifies. Authorship rules:

- **Operator-authored, not agent-authored.** The corpus author writes (or curates from human-written sources) the candidate responses. TGA and Coder Agent are not in this loop. (This is the agents-may-not-author rule again — extended to the response field.)
- **Diversity requirement.** Per-cell response set must include responses across the response-type tertiary axis (§3.3). Single-author monotony is detected at sweep time as low between-case variance and flags `CORPUS_DIVERSITY_INSUFFICIENT` (advisory, not blocking).
- **No target-model-generated responses in v1.** A natural shortcut is: feed the elicitation prompt to the target model, capture the response, ask the human to label it. v1 rejects this — it would couple calibration to target-model state, and any subsequent target-model `.vindex` write would invalidate the candidate-response distribution. The cost is that v1 candidate responses may not perfectly reflect the target's actual response distribution; the v2 path (`OQ-V-JUDGE-RESPONSE-DIST`) addresses this once OQ-V-SELF-REF resolution provides a model-state-aware corpus pattern.

### 3.7 Adversarial response classes (the FN-stressing tier)

The most operationally consequential calibration test is whether the judge correctly rejects responses that *look* correct but aren't. These cases are the protocol's FN floor — every judge-threshold value must hold its FN rate below the asymmetric loss budget on these cases specifically.

Required adversarial classes per cell:

| Class | Construction | What it tests |
|---|---|---|
| Negation flip | "X depends on Y" → "X does not depend on Y" — surface lexically matches; semantic inverse | Judge must detect negation |
| Wrong-context match | Assertion appears in the response but inside an unrelated clause ("It used to be true that X, but no longer") | Judge must scope assertion to operative clause |
| Hedge corruption | Assertion appears with sufficient hedging to invert truth-value ("X may or may not depend on Y, depending on configuration") | Judge must detect epistemic hedging that voids assertion |
| Constraint-bypass response (constraint sub-type only) | Response performs the prohibited action with cosmetic refusal language | Judge must detect substance-over-form for constraint probes |

≥10% of cell cases must be adversarial. Cells failing this floor are flagged `ADVERSARIAL_FLOOR_INSUFFICIENT` and the calibration ratification ceremony refuses the cell.

---

## 4. Granularity Experimental Design

### 4.1 Hypothesis space

| Hypothesis | What it claims | Operational cost |
|---|---|---|
| **H_global** | One threshold T* serves all probes | Minimal — one value pinned |
| **H_per_domain** | Two thresholds T*_assertion and T*_constraint (sub-type split) | Low — two values pinned |
| **H_per_family** | 10 thresholds — sub-type × relation family | Moderate — 10 values, harder to maintain |
| **H_per_probe** | One threshold per probe template | Prohibitive — every new template needs case acquisition |

The protocol does not pre-commit to one. The decision rule is measurement-driven (§4.4), with H_per_domain as the **null/default** hypothesis the calibration must affirmatively beat or fall back from.

### 4.2 Threshold sweep design

For each cell, sweep the judge confidence threshold T over the grid:

```
T ∈ {0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.825, 0.85, 0.875, 0.90, 0.925, 0.95}
```

Finer grid (0.025 steps) in the [0.80, 0.95] range — the operational sweet spot where most thresholds are expected to land for FN-asymmetric loss functions.

For each (cell, T), compute:
- True positives (judge says PASS, ground truth PASS)
- False positives (judge says PASS, ground truth FAIL) — wasted Coder rejection avoided, dangerous if labeling miscalibrated
- True negatives (judge says FAIL, ground truth FAIL)
- False negatives (judge says FAIL, ground truth PASS) — Coder cycle wasted on correct work being rejected — wait, re-examining this:

**Definition convention (this protocol):**
- **PASS = judge accepts the response as containing the target assertion**
- **FAIL = judge rejects the response**
- **FN = ground truth says PASS but judge says FAIL** (correct response erroneously rejected → wasted Coder cycle, recoverable)
- **FP = ground truth says FAIL but judge says PASS** (incorrect response erroneously accepted → fact compiled into `.vindex`, **silent corruption**)

Under this convention, **FP is the dangerous direction** for assertion probes — the bad fact gets through. This is the inversion of the compaction-probe convention (which used FN for "missed regression"). The convention is renamed here for clarity; the asymmetry is the same in spirit.

(For constraint probes, the direction inverts: a PASS verdict on a constraint probe means the response correctly applied the constraint. FP = judge accepts a response that did NOT apply the constraint = constraint not enforced in `.vindex` = silent corruption. So for both sub-types, **FP is the dangerous direction**.)

### 4.3 Per-cell optimal threshold

For each cell c, find:

```
T*_c = argmin_T  L_c(T)

where  L_c(T) = w_FP · P(FP | c, T) + w_FN · P(FN | c, T)
```

with weights determined by sub-type (§5).

### 4.4 Granularity decision rule

After computing T*_c for all 10 cells, decide granularity by threshold-spread analysis:

```
Define spread(set) = max(T*_c) - min(T*_c) for c ∈ set

Decision rule:

  if  spread(all 10 cells) ≤ δ_global  (δ_global = 0.05):
      → H_global accepted
      → ship one global threshold = median(T*_c)

  elif spread(assertion cells) ≤ δ_domain  AND
       spread(constraint cells) ≤ δ_domain  (δ_domain = 0.05):
      → H_per_domain accepted (DEFAULT EXPECTATION)
      → ship two thresholds:
          T*_assertion  = median over assertion cells
          T*_constraint = median over constraint cells

  elif within-sub-type family spread ≤ δ_family  (δ_family = 0.05) per sub-type:
      → H_per_family accepted
      → ship 10 thresholds (sub-type × family)
      → flag T-JUDGE-FAMILY for operator complexity-vs-accuracy review

  else:
      → H_per_probe escalation flagged for the cells exceeding spread
      → ship per-domain values for compliant cells
      → flag non-compliant cells with PER_PROBE_REQUIRED — those probe
        templates' threshold values are pinned individually at template
        commit time, with per-template calibration sub-corpora required
        before commit can complete
```

**δ values are protocol-proposed:** δ_global = δ_domain = δ_family = 0.05. These are starting points and ratified at calibration packet submission. Smaller δ values bias toward finer granularity (more thresholds, more accurate); larger δ values bias toward coarser (fewer thresholds, simpler operations).

**The decision rule itself is what closes OQ-V-JUDGE-THRESHOLD** — the open question asks "per-probe, per-domain, or global default?", and the protocol answers: "*measurement decides; the rule above resolves it deterministically given the measurement.*"

### 4.5 Default expectation

Pre-execution, the protocol's expectation is that **H_per_domain** is the modal outcome. Rationale:

- The §21.2 sub-type split (assertion vs constraint) was chosen because the two sub-types stress the judge model along different dimensions — assertion probes test recognition of present content, constraint probes test recognition of correctly-applied prohibition. Different judgment difficulty suggests different optimal thresholds.
- Within each sub-type, relation families share judgment-difficulty class — the judge's confidence calibration is more about *what kind of judgment* than *what topic*.
- The FN-cost asymmetry differs between sub-types (§5) — the loss function alone biases toward different optimal T even before measurement.

If H_global comes out of measurement, the protocol accepts it but flags `T-JUDGE-DOMAIN-COLLAPSED` for documentation — not because the result is wrong, but because the §21.2 sub-type split was based on a structural distinction the calibration found to be operationally inert at the judge layer. Worth noting.

If H_per_probe is forced for a non-trivial fraction of cells, the protocol carries `T-JUDGE-PER-PROBE-COST` as a Validation-vs-Operations tension to v2 — per-probe thresholds raise the marginal cost of every new probe template considerably and may motivate either a richer judge model or a redesign of the probe-template authorship pipeline.

---

## 5. FP/FN Asymmetric Loss Function

### 5.1 Why asymmetry matters

Recall the convention (§4.2): **FP is the dangerous direction** — silent corruption of `.vindex` parametric memory. FN is recoverable — the Coder Agent retries.

But the *magnitude* of FP cost differs between sub-types:

- **Assertion probes:** A wrongly-accepted response means a wrong fact enters `.vindex`. Cost is bounded by the importance tier of the affected edge — CORE has higher cost than SUPPORTING, INCIDENTAL has lower cost. Recovery is via compaction probe (which is itself sample-based — cost-bounded but non-zero).
- **Constraint probes:** A wrongly-accepted response means a prohibition fails to compile into `.vindex`. The prohibited action becomes available without the constraint firing. This is the same class of harm as a security misconfiguration — and constraints are typically authored to govern the behaviors that are most operationally consequential. Cost is structurally higher than assertion FP.

The loss function reflects this:

### 5.2 Per-sub-type loss weighting

```
For assertion-sub-type cells:
  L_assertion(T) = 3 · P(FP) + 1 · P(FN)

For constraint-sub-type cells:
  L_constraint(T) = 5 · P(FP) + 1 · P(FN)
```

**Weights protocol-proposed; ratifiable at calibration packet submission.** Rationale:

- Assertion 3:1 mirrors the compaction-probe family's FN-weighted asymmetry pattern but tuned to per-response (rather than per-population) granularity.
- Constraint 5:1 escalates the FP penalty further — constraint failures map to safety/policy violations, which the harness's `constitutional-suite/` (§13.3) treats as Tier-2 severity.
- The 5:1 ratio is bounded by the practical limit of operational FP rate the deployment can tolerate without rejecting a meaningful fraction of correct work.

These weights enter the Tier 2 sealed corpus manifest as `loss_weighting` and are themselves frozen at ratification — operator may re-weight, but only via re-ratification.

### 5.3 The asymmetry's interaction with the default candidate

For the protocol's default candidate (Qwen 2.5 7B Instruct), expected per-domain optimal thresholds under the 3:1 / 5:1 loss functions:

| Sub-type | Expected T* range (pre-execution) | Reasoning |
|---|---|---|
| Assertion | 0.78 – 0.85 | Higher T → fewer FP; loss function pulls T up |
| Constraint | 0.85 – 0.92 | Higher penalty → harder threshold; T pulls further up |

These are **provisional estimates for sweep design only** — the calibration produces the actual values. They appear here to confirm the sweep grid (§4.2) covers the expected operational range with margin.

---

## 6. Initial Frozen Triple Production

### 6.1 Triple shape

§21.4 mandates: "the judge model, judge prompt, and threshold are part of the probe template and are versioned and frozen at probe template commit." The protocol's output is the deployment-pinned triple set:

```
judge_calibration_v1 := {
  calibration_epoch_id      : "JUDGE-CALIB-2026-XX-A",
  judge_model_id            : "qwen2.5-7b-instruct@<frozen-version-hash>",
  judge_model_release_hash  : sha256(model_weight_artifact),
  judge_prompt_template     : "<frozen prompt text — see §6.2>",
  judge_prompt_hash         : sha256(judge_prompt_template),
  granularity               : "per_domain",   // OR "global" / "per_family" / "mixed_per_probe"
  thresholds                : {
    assertion             : 0.825,           // post-sweep value
    constraint            : 0.875            // post-sweep value
  },
  loss_weighting            : {
    w_FP_assertion        : 3,
    w_FP_constraint       : 5,
    w_FN                  : 1
  },
  calibration_corpus_hash   : sha256(judge-calibration-corpus/v1),
  probe_set_version_ref     : "probe-set-v1@<hash>",
  target_model_family       : "<deployment target family>",   // for firewall audit
  ratification_ceremony_id  : "CALIBRATION_RATIFICATION_JUDGE-<timestamp>",
  staleness_flag_at_days    : 90
}
```

### 6.2 The frozen judge prompt

The judge prompt is a **single template** (no per-cell variants in v1) of the form:

```
[SYSTEM]
You are a deterministic binary classifier. You receive a response and a target
assertion. You output exactly one of:

  PASS confidence=<float 0.0-1.0>
  FAIL confidence=<float 0.0-1.0>

You output no preamble, no explanation, no other content.

For ASSERTION classification: output PASS iff the response affirmatively
contains the meaning of the target assertion.

For CONSTRAINT classification: output PASS iff the response correctly applies
or refuses according to the constraint stated in the target assertion.

[USER]
TARGET_ASSERTION_TYPE: <assertion | constraint>
TARGET_ASSERTION: <text>
RESPONSE_TO_CLASSIFY: <text>
```

The exact text is fixed at calibration. The hash is recorded. **Any modification — even whitespace — invalidates the calibration and requires re-ratification.** This is the §21.4 freeze enforced concretely.

### 6.3 Pinning ceremony — `CALIBRATION_RATIFICATION_JUDGE`

A new ceremony type, parallel to `CALIBRATION_RATIFICATION` (EPSILON-CALIB) and `CALIBRATION_RATIFICATION_OC3` (COMPACTION-PROBE-CALIB), under the existing IC-SCOPE-AUTH-1 envelope. Same Warden authority, same envelope mechanics — no new ceremony machinery proposed.

Submission packet contents:
- The frozen triple (§6.1)
- Calibration corpus content hash (eighth sealed corpus manifest hash)
- Sweep results: per-cell confusion matrices, per-cell T* values, per-cell loss curves
- Granularity decision evidence (which hypothesis the rule §4.4 selected, with measured spread values)
- Adversarial-class results: per-cell FP rate on negation/wrong-context/hedge/bypass classes specifically
- Independence audit: confirmation that judge-model family ∩ target-model family = ∅

Ratification produces `JUDGE_CALIBRATION_RATIFIED` Ledger entry. From that point forward, every probe template that selects `judgment_method: judge_model_classification` inherits the pinned triple at commit.

### 6.4 Re-calibration cadence

Re-calibration is required when any of:
- Probe-set version increments (`PROBE_SET_RATIFICATION` produces probe-set v2+) — judge is bound to probe-set version per §3.5.
- Judge model release version updates — even a patch version change invalidates the freeze.
- Target-model family deployment changes — independence firewall must be re-verified; in practice a target swap means a new harness deployment, not just re-calibration.
- Drift detection (§6.5) crosses operator-defined threshold.
- Staleness flag at 90 days (advisory — operator may re-calibrate or accept the staleness).

Cadence is operator policy beyond this minimum — `OQ-V-JUDGE-CADENCE` carries the operator-tunable portion forward.

### 6.5 Drift detection (operational, post-ratification)

After ratification, the harness operationally monitors judge behavior on a held-out subset of the calibration corpus (10% reserved at calibration time, never used for sweep). The reserved set is re-judged at intervals (weekly default, operator-tunable). If the judge's accuracy on the reserved set drops by more than ε_drift = 0.05 from calibration accuracy:

- `JUDGE_THRESHOLD_DRIFT_DETECTED` Ledger entry produced (OBSERVATION class, async)
- Re-calibration is recommended but not mandatory (operator policy)
- Probe templates continue inheriting the pinned triple — drift detection is observability, not enforcement

If drift exceeds 2× ε_drift, the entry escalates to GOVERNANCE class (sync) and the harness suspends new probe-template commits using `judge_model_classification` until re-calibration completes. The non-judge methods (`exact_substring`, `structured_field_match`) remain available — partial coverage is preserved.

---

## 7. Ratification Path — `CALIBRATION_RATIFICATION_JUDGE`

Mirrors the §22.5 / §11.14 / §10.x ratification ceremonies — same envelope (IC-SCOPE-AUTH-1), same Warden authority, no new envelope mechanics.

**Ratification preconditions:**
- Probe-set v1 ratified (`PROBE_SET_RATIFICATION` complete; probe-set hash committed)
- Judge calibration corpus authored to ≥200 cases per cell, all 10 cells satisfying ADVERSARIAL_FLOOR_INSUFFICIENT-clearance
- Independence firewall (§2.4) verified: judge-model-family ∩ target-model-family = ∅
- Latency budget verification: judge p95 ≤ 800 ms on deployment GPU class, sampled across 100 randomly-drawn corpus cases

**Ratification ceremony output:**
- `JUDGE_CALIBRATION_RATIFIED` Ledger entry
- Tier 2 sealed `judge-calibration-corpus/v1/manifest.json` operator-signed and committed
- Tier 1 anchor entry `judge_calibration_v1` (the frozen triple) committed to `genesis-seal.json` adjacent slot OR (for re-calibrations) to a new Tier 1 slot per the `JUDGE_CALIBRATION_RATIFIED` provisions
- Probe-template binding pipeline activated — new templates inherit the pinned triple at commit

**Failure modes:**
- Granularity decision indeterminate (no hypothesis cleanly accepted) → ceremony pauses; corpus author is invited to expand cells with insufficient signal; re-submission required
- Adversarial floor failure on any cell → ceremony rejects; cell-specific case authoring required before re-submission
- Independence audit failure → ceremony rejects; judge-model selection re-opens; this never produces a "patch" — it forces full re-selection

---

## 8. Open Questions and Non-Goals

### 8.1 OQ deferred (not closed by this protocol)

- **OQ-V-SELF-REF (v2 / GS13)** — Self-referential probing where judge model = target model. Calibration enforces firewall (§2.4); residual coverage gap documented but not closed.
- **OQ-V-JUDGE-CADENCE** — Re-calibration cadence operator policy beyond the §6.4 minimum.
- **OQ-V-JUDGE-PER-TEMPLATE (v2)** — Per-template judge model selection. v1 ships with single-judge-per-deployment.
- **OQ-V-JUDGE-ENSEMBLE (v2)** — Multi-model ensemble judging. v1 ships with single judge.
- **OQ-V-JUDGE-LARGE** — Larger open-weights judges (70B+) admittable when operator has GPU allocation. Not in v1 default candidate set.
- **OQ-V-JUDGE-RESPONSE-DIST (v2)** — Target-model-generated candidate responses in calibration corpus. v1 uses operator-authored synthetic responses; v2 may admit target-model-sampled responses once OQ-V-SELF-REF resolution provides the model-state-aware corpus pattern.
- **OQ-W-JUDGE-ATTEST** — Warden-domain question on judge-model artifact attestation: how does the harness verify the judge model weights have not been tampered with at deployment? Carries forward to Warden review.
- **T-JUDGE-FAMILY (conditional)** — Fires only if the granularity decision rule produces H_per_family. Operator complexity-vs-accuracy review needed before accepting 10-threshold deployment.
- **T-JUDGE-PER-PROBE-COST (conditional)** — Fires only if the granularity decision rule forces per-probe escalation on a non-trivial fraction of cells. Carries to v2 as a structural-redesign signal.
- **T-JUDGE-DOMAIN-COLLAPSED (conditional, low-stakes)** — Fires if H_global wins. §21.2 sub-type distinction operationally inert at judge layer; documentation note only.

### 8.2 Non-goals

This protocol does NOT specify:
- The `generation` probe sub-type judgment (PyTest-based; out of scope).
- Probe-template authorship rules (owned by §21.3 / TGA).
- Ceremony envelope mechanics (owned by IC-SCOPE-AUTH-1).
- Cross-deployment judge transfer (calibrations are per-deployment; cross-transfer requires a re-ratification per §6.4).
- Self-referential probing (OQ-V-SELF-REF; v2).
- Closed-API judge models (rejected at §2.3).
- Judge model artifact attestation against tampering (OQ-W-JUDGE-ATTEST; Warden domain).

---

═══════════════════════════════════════════════════
## Session Summary Block — JUDGE-CALIB-PROTO-1 Authored
═══════════════════════════════════════════════════

**Session:** 1.6 — Judge-model threshold calibration authorship (Validation Contract Architect primary)
**Status:** Draft (design-complete; gated on probe-set v1 mint via EPSILON-CALIB-PROTO-1 / `PROBE_SET_RATIFICATION` before execution)

### Decisions made

- **Granularity chosen: `per_domain`** — two thresholds (assertion, constraint) by default. Decision rule §4.4 measurement-driven; per-domain is the default expected outcome based on §21.2 sub-type structural distinction and the differential FP-cost asymmetry between sub-types. H_global accepted if measurement supports; per-family or per-probe escalations only if cell variance forces them.
- **Judge-model candidate: Qwen 2.5 7B Instruct @ frozen-version-hash** as v1 default. Selection is deployment-overrideable at ratification (operator may select Llama 3.1 8B Instruct, Gemma 2 9B Instruct, or Mistral Nemo 12B Instruct provided independence holds). Closed-API judges rejected.
- **Initial frozen triples (provisional, sweep finalizes — protocol-proposed pre-execution values):**
  ```
  (judge_model_id, judge_prompt, threshold) for the per_domain pinning:

    assertion : (qwen2.5-7b-instruct@<hash>,  JUDGE_PROMPT_v1,  T_assertion  ≈ 0.80–0.85)
    constraint: (qwen2.5-7b-instruct@<hash>,  JUDGE_PROMPT_v1,  T_constraint ≈ 0.85–0.90)

  Final values produced by §4 sweep; ratified at CALIBRATION_RATIFICATION_JUDGE.
  ```
- **Self-reference exclusion confirmed:** OQ-V-SELF-REF is structurally untouched. Hard constraint C-JUDGE-INDEP enforces JUDGE_MODEL_FAMILY ∩ TARGET_MODEL_FAMILY = ∅. v1 surrogate (cascade-down judgment + `judgment_v1_coverage: PARTIAL` flagging) handles the edge case where only target model could adjudicate; residual case set forwarded as input to OQ-V-SELF-REF v2 resolution.
- **FP/FN asymmetry calibrated separately per sub-type:** w_FP_assertion = 3, w_FP_constraint = 5, w_FN = 1. Constraint sub-type carries higher FP penalty (constraint failure ≈ safety/policy gap, structurally more severe than assertion FP). Weights protocol-proposed; ratifiable.
- **Calibration corpus is the eighth sealed corpus** — `judge-calibration-corpus/` extends §13.3 inventory under v1.3. Inherits IC-CORPUS-AUTH, IC-SL7, IC-SL8, IC-SL9, C-META1 governance — no new corpus-mechanics introduced. Operator-authored per C-GOC4; agents may not author cases.
- **v1 simplification: single judge per harness deployment** (stricter than §21.4 permits). Per-template judge selection (`OQ-V-JUDGE-PER-TEMPLATE`) and ensemble judging (`OQ-V-JUDGE-ENSEMBLE`) are v2.
- **Frozen judge prompt is single-template** (no per-cell variants). Exact text hash-anchored at ratification; whitespace-equivalent changes invalidate calibration.
- **Drift detection (post-ratification, operational):** 10% reserved subset re-judged at operator cadence; ε_drift = 0.05 produces `JUDGE_THRESHOLD_DRIFT_DETECTED`; 2× ε_drift suspends new `judge_model_classification` template commits until re-calibration.

### Constraints established

- **C-JUDGE-INDEP:** JUDGE_MODEL_FAMILY ∩ TARGET_MODEL_FAMILY = ∅ at all times, including transitively through shared lineage, fine-tuning derivatives, or distillation. Violation → `JUDGE_MODEL_INDEPENDENCE_VIOLATED` (SECURITY, sync, W1).
- **C-JUDGE-LATENCY:** Judge inference p95 ≤ 800 ms on deployment GPU class. Verified at ratification across ≥100 sampled corpus cases.
- **C-JUDGE-DETERMINISM:** Judge runs with deterministic decoding (temperature = 0, pinned top_p / top_k / seed). Stochastic decoding rejected at candidate qualification.
- **C-JUDGE-OPENWEIGHTS:** Judge model is open-weights with frozen, hash-anchored release artifact. Closed-API judges rejected — they cannot satisfy §21.4 freeze.
- **C-JUDGE-CORPUS-FLOOR:** ≥200 cases per cell × 10 cells = 2,000-case corpus minimum; ≥30% adversarial-stress cases per cell (negation/wrong-context/hedge/bypass).
- **C-JUDGE-PROBE-BOUND:** Every calibration case binds to a probe-set v1 template; ≥3 distinct templates per cell, ≤30% case dominance per template. EPSILON-CALIB-PROTO-1 §2 must produce ≥3 templates per (sub-type × relation-family) cell — new constraint flowing back to probe-set v1 mint.
- This protocol consumes (does not author) probe-set v1 corpus. All artifacts must be content-hash-verified at calibration corpus admission.
- This protocol does NOT resolve OQ-V-SELF-REF. v2 deferral status persists; firewall protects v1 boundary.
- `JUDGE_CALIBRATION_RATIFIED`, `JUDGE_THRESHOLD_DRIFT_DETECTED`, and `JUDGE_MODEL_INDEPENDENCE_VIOLATED` are new Ledger entry types added to Appendix C under v1.3.

### Pre-execution candidate values (rationale + confidence)

| Parameter | Provisional | Candidate | Rationale | Confidence |
|---|---|---|---|---|
| Judge model (default) | (not specced) | **Qwen 2.5 7B Instruct** | Open-weights, distinct family, latency budget, structured-output capable | High |
| Judge model (alt 1) | — | Llama 3.1 8B Instruct | Backup if target ∈ Qwen family | High |
| Granularity | (open) | **per_domain** | §21.2 sub-type structural distinction + §5 loss-weight asymmetry | Medium-high |
| T_assertion | (not specced) | **0.825** (range 0.80–0.85) | 3:1 FP-FN weighting on a 7B-class judge — FP-pull medium | Medium |
| T_constraint | (not specced) | **0.875** (range 0.85–0.90) | 5:1 FP-FN weighting on constraint sub-type pulls T further up | Medium |
| w_FP_assertion / w_FN | (not specced) | **3 / 1** | Mirrors compaction-probe FN-asymmetry pattern at per-response granularity | Medium-high |
| w_FP_constraint / w_FN | (not specced) | **5 / 1** | Constraint failure ≈ safety/policy gap; higher penalty | Medium |
| δ_global / δ_domain / δ_family | (not specced) | **0.05 / 0.05 / 0.05** | Smaller δ → finer granularity bias; protocol-proposed | Medium |
| Per-cell case count | (not specced) | **200** | Power calc for ±0.05 CI half-width on cell-pair threshold differentiation | High (math-driven) |
| Adversarial floor per cell | (not specced) | **≥10% (≥30% incl. near-miss/false-correct)** | FN-stressing classes — calibration rejects cells failing this floor | High |
| ε_drift | (not specced) | **0.05** | Operational drift signal; 2× → suspension | Medium-low (untested) |
| Latency budget p95 | (not specced) | **≤ 800 ms** | L2 probe path budget; deployment GPU class dependent | Medium |
| Staleness flag | 90 days (§13.3) | **90 days** | Inherits sealed-corpus pattern | High (inherited) |

### Open questions deferred

- **OQ-V-SELF-REF (v2 / GS13)** — Self-referential probing. NOT touched by this calibration; firewall (C-JUDGE-INDEP) protects v1 boundary; residual coverage gap forwarded as input to v2 resolution.
- **OQ-V-JUDGE-CADENCE** — Re-calibration cadence operator policy beyond §6.4 minimum (probe-set increment, judge release update, staleness, drift). Mirrors OQ-W-CALIB-CADENCE / OQ-OC3-CADENCE pattern; operator policy.
- **OQ-V-JUDGE-PER-TEMPLATE (v2)** — Per-template judge model selection. v1 ships single-judge-per-deployment.
- **OQ-V-JUDGE-ENSEMBLE (v2)** — Multi-model ensemble judging.
- **OQ-V-JUDGE-LARGE** — Larger (70B+) open-weights judges admittable when operator GPU allocation supports. Not in v1 default candidate set.
- **OQ-V-JUDGE-RESPONSE-DIST (v2)** — Target-model-sampled candidate responses in calibration corpus. v1 rejects (would couple calibration to target-model state); v2 admits once OQ-V-SELF-REF resolution provides the model-state-aware corpus pattern.
- **OQ-W-JUDGE-ATTEST** — Judge-model artifact attestation against weight tampering. Warden-domain.

### Cross-domain tensions surfaced

- **T-JUDGE-1: Eighth Sealed Corpus Governance** (Validation vs. Warden) — ✅ Resolved. The judge calibration corpus enters Tier 2 under §13.3 inheriting IC-CORPUS-AUTH, IC-SL7, IC-SL8, IC-SL9, C-META1, §24 expiry enforcement. No new corpus governance machinery proposed; the Warden's existing pattern absorbs the eighth corpus.
- **T-JUDGE-2: Judge Independence vs. Domain Adjudication Coverage** (Validation-internal, with v2-bounded surface) — 🔶 Partially resolved. Hard firewall (C-JUDGE-INDEP) forces independence; v1 surrogate (cascade-down + `judgment_v1_coverage: PARTIAL` flagging) preserves coverage where deterministic methods suffice; residual case set forwarded to OQ-V-SELF-REF v2.
- **T-JUDGE-3: Per-Domain Calibration vs. v1 Single-Judge Simplification** (Validation-internal) — ✅ Resolved. Single judge model handles both sub-types via different threshold values — sub-type granularity does not require sub-type judge multiplicity. Per-template / ensemble judges are v2.
- **T-JUDGE-4: Probe-Template Authorship (TGA) vs. Calibration Corpus Authorship (Operator)** (Validation-internal, structural) — ✅ Resolved. TGA authors probe templates per §21.3 (unchanged). Operator authors calibration cases (case_id, candidate_response, ground_truth_label) under sealed-corpus rules — agents may not author per IC-CORPUS-AUTH. The two authorship paths are disjoint by design.
- **T-JUDGE-5: Per-Probe Calibration Cost vs. Operational Throughput** (Validation vs. Operations, conditional) — 🔶 Acknowledged. Fires only if §4.4 forces per-probe escalation. Per-probe thresholds raise the marginal cost of every new probe template; if a non-trivial fraction triggers, carries to v2 as a structural-redesign signal (`T-JUDGE-PER-PROBE-COST`).

### Pre-mapped tension coverage

- **Pre-T2 (Write Volume vs. Edit Locality)** — Untouched. Judge thresholds operate on probe responses (per-write), not on edit locality.
- **Pre-T6 (Genesis Completeness vs. Genesis Lock-in)** — Touched at the eighth-sealed-corpus admission. The `judge-calibration-corpus/v1/` follows the existing Pre-T6 minimal-viable-Genesis resolution (corpus admitted post-Genesis via append-versioned directory). No Pre-T6 surface change required.

### Artifacts the protocol produces (when executed)

- `judge_calibration_corpus_admission_log.json` (per-case author identity, format-validation outcomes, IC-CORPUS-AUTH enforcement records)
- `judge_threshold_sweep_results.json` (per-cell confusion matrices across sweep grid; per-cell loss-curve plots)
- `granularity_decision_record.json` (which hypothesis §4.4 selected; measured spread values; cell-by-cell T*_c)
- `adversarial_class_results.json` (per-cell FP rate on negation/wrong-context/hedge/bypass classes specifically)
- `judge_independence_audit.json` (firewall verification — judge family, target family, intersection check, lineage trace)
- `judge_latency_profile.json` (p50/p95/p99 inference latency on deployment GPU class across ≥100 sampled cases)
- `judge_calibration_v1_frozen_triple` (the §6.1 triple; the protocol's primary output)
- `CALIBRATION_RATIFICATION_JUDGE` submission packet (parallel to EPSILON-CALIB §22.5 ceremony path; bundled with all of the above)
- v1.3 IC-OC-PROBE / Appendix E / Appendix C extensions (eighth sealed corpus inventory entry; new Ledger entry types `JUDGE_CALIBRATION_RATIFIED`, `JUDGE_THRESHOLD_DRIFT_DETECTED`, `JUDGE_MODEL_INDEPENDENCE_VIOLATED`)

### Protocols defined this session

- **JUDGE-CALIB-PROTO-1** — full protocol covering judge selection, self-reference firewall, eighth-sealed-corpus authorship, stratification, threshold sweep, granularity decision rule, FP/FN asymmetric loss, frozen triple production, drift detection, ratification path, kill criteria.
- **`CALIBRATION_RATIFICATION_JUDGE` ceremony type (proposed)** — calibration packet ratification under existing IC-SCOPE-AUTH-1 envelope; placement parallels EPSILON-CALIB / COMPACTION-PROBE-CALIB ceremony paths. No new envelope mechanics; same Warden authority.
- **Eighth Tier 2 sealed corpus (proposed)** — `judge-calibration-corpus/` extends §13.3 v1.2 seven-corpus inventory under a v1.3 minor-version bump.

### Interface contracts defined

```
IC-V-JUDGE-CALIB-1 — Probe-set v1 → Judge calibration corpus binding
  From: probe-set v1 (output of EPSILON-CALIB-PROTO-1 / PROBE_SET_RATIFICATION)
  To:   judge calibration corpus admission
  What A exposes: probe-set v1 frozen template hashes; sub-type and relation-family
    assignments per template; ≥3 templates per (sub-type × relation-family) cell.
  Conditions: probe-set hash content-verified at corpus admission; binding map
    (case → template_ref) immutable post-admission.
  Failure behavior: insufficient templates per cell → PROBE_SET_v1_INSUFFICIENT_FOR_JUDGE_CALIB
    (advisory, blocks judge calibration; kicks back to probe-set v1 mint).

IC-V-JUDGE-CALIB-2 — Judge calibration corpus → Sweep run (sealed-corpus access)
  From: judge-calibration-corpus/v1/ (Tier 2 sealed)
  To:   threshold sweep run process
  What A exposes: time-bounded read access via IC-SL7 token (inherited);
    operator-signed manifest verified per IC-SL8; per-case audit entries per IC-SL9.
  Conditions: ratification-ceremony-scheduled run only; token single-use;
    minimum 200 cases per cell; adversarial floor satisfied per cell.
  Failure behavior: corpus integrity → SEALED_CORPUS_INTEGRITY_FAIL (security);
    cell floor failure → ADVERSARIAL_FLOOR_INSUFFICIENT (calibration rejection).

IC-V-JUDGE-CALIB-3 — Sweep result → CALIBRATION_RATIFICATION_JUDGE submission
  From: threshold sweep + granularity decision + adversarial audit
  To:   CALIBRATION_RATIFICATION_JUDGE ceremony (IC-SCOPE-AUTH-1 envelope)
  What A exposes: complete §6.1 frozen triple; corpus hash; sweep evidence;
    independence audit; latency profile.
  Conditions: hypothesis decision rule §4.4 produces a unique selected granularity;
    independence firewall passes; latency budget satisfied.
  Failure behavior: indeterminate granularity → ceremony pauses, corpus expansion
    invited; independence fail → ceremony rejects, judge-model selection re-opens
    (no patch path); latency fail → ceremony rejects, alternate judge candidate
    required.

IC-V-JUDGE-CALIB-4 — Frozen triple → Probe template binding at commit
  From: ratified judge_calibration_v1 frozen triple
  To:   probe template commit pipeline (TGA-authored templates that select
        judgment_method = judge_model_classification)
  What A exposes: deployment-pinned (judge_model_id, judge_prompt, threshold-by-
    sub-type) inheritance; calibration_epoch_id reference; probe-set version ref.
  Conditions: probe template's selected sub-type ∈ {assertion, constraint};
    target_assertion non-empty; commit-time hash anchor written.
  Failure behavior: triple-staleness (>90d advisory; >drift-2× hard) →
    JUDGE_THRESHOLD_DRIFT_DETECTED; commit blocked at hard threshold;
    re-calibration required to unblock new judge_model_classification commits.

IC-V-JUDGE-CALIB-5 — Drift detection → Operational signal
  From: weekly held-out reserved-subset re-judgment (10% corpus reserve)
  To:   State Ledger
  What A exposes: per-week judge accuracy delta against calibration baseline;
    JUDGE_THRESHOLD_DRIFT_DETECTED at ε_drift = 0.05;
    GOVERNANCE escalation at 2× ε_drift with new-template suspension flag.
  Conditions: reserved-subset access via IC-SL7 same-pattern token; per-case
    audit entries via IC-SL9.
  Failure behavior: missed weekly run → DRIFT_AUDIT_MISSED (advisory,
    rolls forward; not an enforcement event).
```

### Next session candidates

- **OQ-W-JUDGE-ATTEST session (Warden-domain):** Judge-model artifact attestation — how does the harness verify judge weights have not been tampered with at deployment? Cryptographic verification, supply-chain integrity, integration with hook-registry pattern (§13.3 seventh sealed corpus).
- **EPSILON-CALIB-PROTO-1 amendment session (MEMIT + Validation joint):** Add the IC-V-JUDGE-CALIB-1 constraint (≥3 templates per (sub-type × relation-family) cell) to probe-set v1 mint requirements. Minor amendment; same protocol authors absorb.
- **Stage 4 — Consolidation:** With Stage 1 PASS, Stage 2 outputs, Stage 3 (EPSILON-CALIB), Stage 1.5 (COMPACTION-PROBE-CALIB), and Stage 1.6 (this protocol — JUDGE-CALIB) all in hand, bundle into a unified POC submission packet. Per write-engine-poc-scope §6, Stage 4 is sequencing and packaging.
- **OQ-V-SELF-REF v2 framing session (Validation-domain, v2 scope):** Take the residual `judgment_v1_coverage: PARTIAL` case set produced by this protocol's v1 surrogate as the input artifact. Frame v2 resolution: in-corpus target-model probing, model-state-aware corpus patterns, ensemble-bypass routes.

═══════════════════════════════════════════════════
*JUDGE-CALIB-PROTO-1 — design-complete, awaiting probe-set v1 mint via EPSILON-CALIB-PROTO-1 / PROBE_SET_RATIFICATION to execute*
*Specialist provenance: Validation Contract Architect (primary, judge-side correctness contract). Warden domain touched at IC-V-JUDGE-CALIB-2 (sealed-corpus governance — inherited mechanics, no new surface) and at OQ-W-JUDGE-ATTEST (deferred to Warden session). MEMIT domain touched at IC-V-JUDGE-CALIB-1 (probe-set v1 binding — minor amendment to EPSILON-CALIB-PROTO-1). OQ-V-SELF-REF v2 boundary explicitly preserved by C-JUDGE-INDEP firewall.*
═══════════════════════════════════════════════════
