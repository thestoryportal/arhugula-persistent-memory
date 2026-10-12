## 21. L2 Probe Family and Semantic Assertion Criterion

### 21.1 Purpose

L2 behavioral probes (§8.9 — mandatory for `declared_importance ∈ {CORE, SUPPORTING}`) are generalized from the code-domain-only "generation test" of v1.1 into a domain-agnostic three-member probe family, each producing the same deterministic binary pass/fail outcome required by the Ledger schema (`write_outcome ∈ {success, behavior_fail}`). Source: GAP-9 / v2 GS10.

### 21.2 The Three Probe Sub-Types

**Generation probe** (code-domain edges, `function` / `module` entity types):
Prompt elicits code generation or completion; pass condition is execution-based (test harness returns green). This is the existing §8.9 behavior, preserved verbatim as one member of the family.

**Assertion probe** (non-code `domain_concept` edges asserting positive facts — legal constraints, architectural invariants, business rules stated affirmatively):
Prompt elicits a response in a context where the fact should fire; pass condition is that the response contains the target assertion, verified by one of the three judgment methods (§21.4).

**Constraint probe** (non-code edges asserting prohibitions or invariants — "X must not Y", "Z is required before W"):
Prompt presents an adversarial scenario that would violate the constraint; pass condition is that the response refuses, flags, or correctly applies the constraint.

All three sub-types share the same Ledger contract: binary outcome at probe evaluation time, `write_outcome ∈ {success, behavior_fail}`, storage-pass / behavior-fail never collapsed into success.

### 21.3 Probe Authorship Authority

Probe templates are authored by the **Test Generator Agent (TGA)** as a sub-class of test artifact. This preserves D32–D33 actor-critic independence without a new component and without an independence exemption. TGA's mandate extends:

- From the task specification, emit (i) executable tests for code artifacts, (ii) probe templates for non-code artifacts, (iii) both when a write crosses domains.
- The Coder Agent / Architect Agent writes the `.larql` patch without visibility into either tests or probes.

Option (b) — granting the writing agent an independence exemption — is rejected as puncturing the central invariant. Option (c) — a separate probe-template component — is rejected as requiring a justification TGA already satisfies. The T-TGA-load tension (TGA authority concentration) was Accepted for v1 (GS12) under this allocation.

### 21.4 Semantic Assertion Criterion

Given probe template:

```
P = (elicitation_prompt, target_assertion, judgment_method, threshold)
```

the probe passes iff the model's response to `elicitation_prompt`, evaluated by `judgment_method`, registers `target_assertion` at or above `threshold`. The three permitted judgment methods:

- **`exact_substring`** — target_assertion is a string; pass iff the response contains it (case-sensitive by default; case-insensitive if the template declares so).
- **`structured_field_match`** — target_assertion is a structured object (JSON); the response is parsed against an expected schema and field values; pass iff all required fields match.
- **`judge_model_classification`** — target_assertion is a natural-language specification of the expected content; a designated judge model classifies the response at a declared confidence threshold. Binary classifier output.

For `judge_model_classification`, the judge model, judge prompt, and threshold are part of the probe template and are **versioned and frozen at probe template commit**. A probe's judgment dependencies are immutable once committed — preventing silent drift in what "pass" means.

### 21.5 Spec Block — L2 Probe Family

**What it must do:** Provide a domain-general behavioral verification gate for edges with `declared_importance ∈ {CORE, SUPPORTING}`. Produce a deterministic binary outcome recorded as `write_outcome` in the Ledger.

**Hard constraints:**
- Every L2 probe has exactly three components: `elicitation_prompt`, `expected_behavior_predicate`, `judgment_method`.
- Probe outcome is binary; storage-pass / behavior-fail is a distinct Ledger state, never collapsed into success (preserves §8.9).
- Probe sub-type is declared in the probe template: `{generation | assertion | constraint}`.
- Judge-model dependencies (when `judgment_method = judge_model_classification`) are pinned to specific model versions and frozen at probe template commit.
- Probe templates are TGA-authored.

**Tradeoffs decided:**
- Binary rather than graded outcome — preserves Ledger schema and clean Reflexion-loop semantics; cost is loss of fine-grained confidence for borderline assertion probes.
- Judge-model classification permitted despite introducing a second model — without it, non-trivial non-code facts have no machine-checkable criterion. Mitigated by freezing judge-model and prompt at template commit.
- TGA-authored probes over a separate probe-template component — preserves D32–D33 without new machinery; T-TGA-load concentration Accepted.

**Open questions (deferred):**
- Threshold calibration for `judge_model_classification`: per-probe, per-domain, or global default (OQ-V-JUDGE-THRESHOLD; GAP-9 residual).
- Self-referential probing — handling probes whose judge model is itself subject to `.vindex` writes (OQ-V-SELF-REF; GAP-49 → GS13).

**Interface contract (probe template shape):**

```
probe_template := {
  probe_id,
  probe_sub_type       ∈ {generation, assertion, constraint},
  elicitation_prompt,
  expected_behavior_predicate,
  judgment_method      ∈ {exact_substring, structured_field_match,
                          judge_model_classification},
  judgment_config      (judge_model_id, judge_prompt, threshold — when applicable),
  authored_by          : tga_agent_id,
  template_hash
}
```

### 21.6 Non-Goals

§21 does not specify:
- The calibration of judge-model thresholds (OQ-V-JUDGE-THRESHOLD).
- Probe-template refactoring ceremonies (v2 — tied to TGA-split reconsideration).
- Probe outcomes for edges with `declared_importance = INCIDENTAL` — these are not L2-probed.

---

