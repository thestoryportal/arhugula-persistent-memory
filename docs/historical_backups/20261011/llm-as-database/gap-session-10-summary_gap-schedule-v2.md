# Gap Session 10 of 12 — Summary

**Session:** Gap Resolution 10 / 12
**Specialists convened:** MEMIT Specialist, Validation Contract Architect, State Consistency Theorist
**Baseline:** v1.1 Integrated Spec
**Gaps addressed:** GAP-9 (behavioral probe generalization), GAP-11 (Layer 4 external document provenance)

---

## Session Framing

Both gaps concern what the write engine can verify about facts after they have been written. GAP-9 asks whether the L2 inference probe — specified in code-flavored language — extends to non-code Layer 4 facts. GAP-11 asks whether the harness can detect when the authoritative source of a Layer 4 fact has drifted out from under it, given the Pruning Agent only monitors Git.

The Validation Contract Architect owns probe semantics. The MEMIT Specialist owns what is recoverable from the parametric layer after a write. The State Consistency Theorist owns the question of whether an external-source-drift signal should be treated as an out-of-band event analogous to an out-of-band Git commit.

---

## GAP-9 Resolution — Behavioral Probe Generalization

### L2 Probe Family (Domain-Agnostic Reformulation)

The L2 probe is redefined as a **structured inference elicitation** with three deterministic components: an elicitation prompt, an expected-behavior predicate, and a deterministic pass/fail judgment. The code-domain "generation test" becomes one member of a probe family rather than the canonical form.

Three probe sub-types are introduced:

- **Generation probe** (code-domain edges, `function`/`module` entity types): prompt elicits code generation or completion; pass condition is execution-based (test harness returns green). This is the existing §8.9 behavior.
- **Assertion probe** (non-code `domain_concept` edges asserting positive facts — legal constraints, architectural invariants, business rules stated affirmatively): prompt elicits a response in a context where the fact should fire; pass condition is that the response contains the target assertion, verified by structured field match or judge-model binary classification at a declared confidence threshold.
- **Constraint probe** (non-code edges asserting prohibitions or invariants — "X must not Y", "Z is required before W"): prompt presents an adversarial scenario that would violate the constraint; pass condition is that the response refuses, flags, or correctly applies the constraint.

All three sub-types share the same pass/fail contract: deterministic binary outcome at probe evaluation time, recorded as `write_outcome ∈ {success, behavior_fail}` per §8.9.

### Actor-Critic Independence for Probe Authorship

**Resolved: Option (a)** — probe templates are authored by the Test Generator Agent (TGA) as a sub-class of test artifact. This preserves D32–D33 without introducing a new component or an independence exemption.

Rationale: the invariant under D32–D33 is that the agent writing the artifact-under-verification cannot also write the verifier. A probe template is a verifier. The TGA already reads the task specification only and never the Coder Agent's output; extending its mandate to probe templates keeps the independence boundary intact. Introducing a separate probe-template component (option c) would require justifying why TGA cannot cover the case, which it can. Granting the writing agent an independence exemption (option b) would puncture the central invariant of the validation architecture and is rejected.

TGA's mandate is therefore: from the task specification, emit (i) executable tests for code artifacts, (ii) probe templates for non-code artifacts, (iii) both when a write crosses domains. The Coder Agent (or Architect Agent, for L4) writes the `.larql` patch without visibility into either.

### Concrete Verifiable Criterion (Non-Code)

The following is specified as a minimum-viable non-code pass criterion:

**Semantic Assertion Criterion.** Given probe template `P = (elicitation_prompt, target_assertion, judgment_method, threshold)`, the probe passes iff the model's response to `elicitation_prompt`, evaluated by `judgment_method`, registers `target_assertion` at or above `threshold`. `judgment_method` is one of: `exact_substring`, `structured_field_match`, `judge_model_classification`. For `judge_model_classification`, the judge model, prompt, and threshold are part of the probe template and are themselves versioned — a probe's judgment dependencies are immutable once the probe template is committed, preventing silent drift in what "pass" means.

### Spec Blocks

```
### L2 Probe Family — Spec Block
What it must do:
  Provide a domain-general behavioral verification gate for edges with
  declared_importance ∈ {CORE, SUPPORTING}. Produce a deterministic binary
  outcome recorded as write_outcome in the Ledger.

Hard constraints:
  - Every L2 probe has exactly three components: elicitation_prompt,
    expected_behavior_predicate, judgment_method.
  - Probe outcome is binary; storage-pass / behavior-fail is a distinct
    Ledger state, never collapsed into success (preserves §8.9).
  - Probe sub-type is declared in the probe template:
    {generation | assertion | constraint}.
  - Judge-model dependencies (when judgment_method = judge_model_classification)
    are pinned to specific model versions and frozen at probe template commit.

Tradeoffs decided:
  - Probe outcome is deterministic binary rather than graded: preserves the
    existing Ledger schema and the clean fail/retry semantics of the Reflexion
    loop, at the cost of losing fine-grained confidence signal for borderline
    assertion probes.
  - Judge-model classification is permitted despite introducing a second model:
    without it, non-trivial non-code facts have no machine-checkable criterion.
    Mitigated by freezing judge model and prompt at template commit.

Open questions (deferred):
  - Threshold calibration for judge_model_classification: per-probe, per-domain,
    or global default.
  - Handling probes whose judge model is itself subject to .vindex writes
    (self-referential probing).

Interface contract:
  probe_template := {
    probe_id,
    probe_sub_type ∈ {generation, assertion, constraint},
    elicitation_prompt,
    expected_behavior_predicate,
    judgment_method ∈ {exact_substring, structured_field_match, judge_model_classification},
    judgment_config (judge_model_id, judge_prompt, threshold — when applicable),
    authored_by: tga_agent_id,
    template_hash
  }
  probe_outcome := {pass, behavior_fail} — written to Ledger entry for
  the corresponding write.
```

```
### Probe Authorship Authority — Spec Block
What it must enforce:
  The agent authoring a write artifact cannot also author its verifier.

Hard constraints:
  - Probe templates for all probe sub-types are authored by TGA.
  - TGA reads task specification only; never reads the .larql patch under
    verification (extends D33 to probe templates).
  - Coder Agent and Architect Agent MUST NOT author probe templates.
  - No independence exemption is granted to any writing agent.

Tradeoffs decided:
  - Extending TGA's mandate rather than creating a separate probe-template
    component: simpler architecture, same independence guarantee.

Open questions (deferred):
  - Does TGA need a distinct persona or mode for non-code probe generation,
    given the different skill profile from test generation?

Interface contract:
  tga_output := {
    test_artifacts: [test_cases],      // for code writes
    probe_templates: [probe_template], // for non-code writes or L2 gates
    authored_by: tga_agent_id,
    source_task_spec_hash
  }
```

---

## GAP-11 Resolution — Layer 4 External Document Provenance

### Decision: Provenance Is Tracked

The harness **tracks external document provenance for all Layer 4 writes** that cite an external source. This is mandatory, not advisory: without it, the Ledger's audit trail cannot answer the question "what was the authoritative state of the world when this fact was written?", which is a foundational guarantee of the framework.

### Provenance Record Structure

The provenance record is a required metadata block in the `.larql` patch for any L4 write citing an external source, and is copied verbatim into the Ledger entry. Layer 4 writes with no external citation (purely architect-authored domain knowledge) are permitted and carry `external_source_uri: null` with an `internal_authority` field instead.

**Required fields:**
- `external_source_uri` — canonical URI of the source document at time of write.
- `source_hash_at_write` — hash of the retrieved content at write time.
- `hash_algorithm` — default `sha256`; explicit to permit future migration.
- `write_timestamp` — ISO 8601 UTC.

**Additional fields (required):**
- `retrieval_method ∈ {direct_fetch, archival_snapshot, human_supplied}`.
- `source_type ∈ {web_document, specification, api_reference, legal_text, academic_publication, other}`.
- `content_snapshot_ref` — pointer to a locally archived copy of the source content at write time. Local archival is mandatory when `retrieval_method = direct_fetch`; this is the only mechanism that guarantees the harness can still audit the written fact when the external source disappears.
- `source_authority_declared` — free-text attribution of who or what entity the source represents (used for human review, not machine logic).

### Drift Detection and Response

**Monitoring mechanism: Provenance Monitor** — a new component, distinct from the Pruning Agent. Rationale from the State Consistency Theorist: the Pruning Agent's invariant is that Git is its ground truth. Conflating external-source monitoring with Pruning Agent responsibilities would blur that invariant and create a component with two sources of truth. The Provenance Monitor has exactly one job: periodically re-fetch external sources listed in Ledger provenance records, compute the hash, and compare to `source_hash_at_write`.

**Trigger conditions:**
- Scheduled sweep (default: weekly; per-source override via `source_type` policy table).
- Manual trigger from human reviewer.
- On Ledger read for any L4 edge whose last provenance check exceeds a staleness window.

**Drift outcomes** (written as Ledger entries, never as automatic patches):
- `content_changed` — source retrieved, hash differs from `source_hash_at_write`.
- `source_unavailable` — source cannot be retrieved (HTTP error, domain gone, paywalled, etc.).
- `hash_mismatch` — source retrieved but content is corrupt or truncated relative to a sanity check.

All three outcomes produce a Ledger entry with `entry_type = external_source_drift`, `requires_human_review = true`, and a link back to the affected edge(s). **The drift entry is advisory with respect to the existing edge** — the fact in `.vindex` is not rolled back, deleted, or modified by the Provenance Monitor. The fact may still be correct; drift only signals that the authoritative basis for the fact can no longer be confirmed automatically.

**Human review path:** drifted edges appear in a pending-review queue. The reviewer chooses one of:
- `confirm` — fact remains valid despite source drift; Ledger records reviewer identity, timestamp, and `new_source_hash` if applicable. This extends the edge's provenance record with a successor entry rather than overwriting.
- `re-verify` — triggers a new validator cascade with the current source content as input; may produce a new write that replaces the edge.
- `retire` — routes to standard pruning pipeline for deletion.

### No Auto-Compile Applies

**Confirmed: `no auto-compile` (§11.13) extends to detected external source changes.** The Provenance Monitor never authors `.larql` patches. Its output is exclusively Ledger advisory entries. The same rationale that blocks the Pruning Agent from auto-compiling out-of-band Git commits applies here: external source drift is, categorically, an out-of-band event — the harness did not cause it, cannot validate it under its own trust model without human review, and must not silently rewrite its knowledge graph in response.

This extends §11.13's scope: "out-of-band changes" now formally includes external source drift, not only out-of-band Git commits.

### Spec Blocks

```
### Provenance Record (Layer 4) — Spec Block
What it must represent:
  The authoritative basis for a Layer 4 fact at the moment of write, sufficient
  to detect later drift and to support human re-verification.

Hard constraints:
  - Every L4 write citing an external source MUST carry a complete provenance
    record in its .larql patch metadata.
  - Provenance record is copied verbatim into the Ledger entry; the Ledger is
    the canonical historical record.
  - When retrieval_method = direct_fetch, a local content snapshot is mandatory.
  - Hash algorithm is declared explicitly per record (no global constant).
  - L4 writes without external citation MUST carry internal_authority instead;
    external_source_uri = null is not a silent omission.

Tradeoffs decided:
  - Local snapshot mandatory for direct_fetch: storage cost accepted in exchange
    for auditability when sources disappear.
  - Advisory-only drift entries: preserves the "no auto-compile" invariant, at
    the cost of accumulating review backlog for high-churn sources.

Open questions (deferred):
  - Retention policy for content snapshots (indefinite vs. tiered).
  - Handling of sources behind authentication (credentials in provenance record?).
  - Granularity of drift detection for large documents (whole-document hash vs.
    section-level).

Interface contract:
  provenance_record := {
    external_source_uri: string | null,
    source_hash_at_write: string | null,
    hash_algorithm: string,                   // default "sha256"
    write_timestamp: ISO8601,
    retrieval_method: {direct_fetch, archival_snapshot, human_supplied},
    source_type: {web_document, specification, api_reference, legal_text,
                  academic_publication, other},
    content_snapshot_ref: string | null,
    source_authority_declared: string,
    internal_authority: string | null          // required iff external_source_uri = null
  }
```

```
### Provenance Monitor — Spec Block
What it must do:
  Periodically re-verify external sources cited in Ledger provenance records.
  Emit advisory Ledger entries when drift is detected. Never modify .vindex
  directly, never author .larql patches.

Hard constraints:
  - Distinct component from the Pruning Agent (different ground truth domain).
  - Output is exclusively Ledger entries with entry_type = external_source_drift.
  - requires_human_review = true on every drift entry.
  - Drift never triggers automatic rollback, deletion, or rewrite of the affected
    edge (extends §11.13 no-auto-compile scope).
  - Monitor runs on schedule, on manual trigger, and on Ledger read for stale
    provenance.

Tradeoffs decided:
  - Separate component rather than Pruning Agent extension: preserves the Pruning
    Agent's single-ground-truth invariant (Git). Cost: one more component to
    operate.
  - Whole-source hash default: simple and unambiguous. Section-level detection
    deferred as an optimization.

Open questions (deferred):
  - Default staleness window per source_type.
  - Rate-limiting and politeness budget for scheduled sweeps against external
    hosts.
  - Behavior when a source's canonical URI redirects (follow vs. flag).

Interface contract:
  drift_entry := {
    entry_type: "external_source_drift",
    edge_ids: [edge_id],
    drift_type: {content_changed, source_unavailable, hash_mismatch},
    detection_timestamp: ISO8601,
    new_source_hash: string | null,           // null for source_unavailable
    requires_human_review: true,
    monitor_component_id: string
  }
  human_review_outcome := {confirm, re-verify, retire}
```

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-9** — L2 probe generalized to a three-member probe family (generation, assertion, constraint) with a shared deterministic pass/fail contract. Probe template authorship assigned to TGA as a sub-class of test artifact, preserving D32–D33 independence without exemption. Semantic Assertion Criterion specified as the minimum-viable non-code pass criterion with three judgment methods, including pinned-version judge-model classification.
- **GAP-11** — Provenance tracking for Layer 4 external-sourced facts is mandatory. Provenance record structure specified with required fields including local content snapshot for direct-fetch retrievals. New component introduced: the Provenance Monitor, distinct from the Pruning Agent. Drift detection produces advisory-only Ledger entries requiring human review; never triggers automatic rewrite. §11.13 no-auto-compile scope extended to external source drift.

**GAPS PARTIALLY RESOLVED:** none.

**GAPS DEFERRED:**
- Threshold calibration strategy for `judge_model_classification` (per-probe vs. per-domain vs. global) — deferred to a future validation-tuning session.
- Retention policy for provenance content snapshots — deferred; storage-cost analysis required.
- Handling of authenticated external sources (credentials and provenance) — deferred; intersects the Warden's threat model and is better addressed with AISecOps present.
- Section-level vs. whole-document drift detection granularity — deferred as a Provenance Monitor optimization.

**NEW GAPS SURFACED:**
- **GAP-13 (new)** — Self-referential probing: when the judge model used by a `judge_model_classification` probe is itself subject to `.vindex` writes, probe outcomes may drift silently. No mechanism currently isolates judge-model state from the write stream it verifies.
- **GAP-14 (new)** — TGA skill-profile divergence: TGA's mandate now spans executable test generation and non-code probe template authorship. Whether a single agent role can cover both without quality degradation is unverified.
- **GAP-15 (new)** — Provenance record lifecycle for L4 writes that cite an external source which is itself later re-verified: the relationship between the original provenance record and the successor record (extend, replace, chain) is specified narratively but not formally.

**NEW TENSIONS SURFACED:**
- **T-PM-vs-PA** — Provenance Monitor and Pruning Agent both generate advisory entries flagged `requires_human_review`. A single edge can accumulate advisories from both components (Git-side staleness and external-source drift) without a defined merge/priority order in the human review queue. Ownership: State Consistency Theorist (queue semantics) and Warden (review-path integrity) — to be reconciled in a future session.
- **T-TGA-load** — TGA is now the sole author of executable tests, probe templates (three sub-types), and the only agent permitted to read task specifications for verification-artifact generation. The Actor-Critic independence guarantee concentrates verification authority in a single role, raising a single-point-of-failure concern the Validation Contract Architect flagged but did not resolve here.

---

*End of Gap Session 10 Summary. Baseline for Session 11: v1.1 integrated spec + GS5–GS10 resolutions. New gaps (GAP-13, GAP-14, GAP-15) and tensions (T-PM-vs-PA, T-TGA-load) added to the backlog.*
