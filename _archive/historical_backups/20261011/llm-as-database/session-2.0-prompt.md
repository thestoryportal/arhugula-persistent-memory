# Session 2.0 — Target Model Commitment Prompt

> Paste the prompt below into a new chat session **after** the entry note has been read. The prompt assumes the project's revised system prompt is already in place and the curated KB (7 documents) is loaded.

---

```
/memit-specialist

<session_context>
Workstream 1, Session 2.0 — Target Model Commitment.
Closes OQ-WS1-1 (target model commitment, inherited from Session 1.1).
Gates Stage 0 corpus authorship and Stage 1 (MEMIT-COMPAT-PROTO-1) execution.
Output is a recommendation, not a commitment. Operator commits in a follow-up.
</session_context>

<task>
Survey open-weights model candidates against the SC-1..SC-9 selection
criteria from MEMIT-COMPAT-PROTO-1 §1. Produce a structured recommendation
document the operator can review and sign.
</task>

<inputs>
- Selection criteria: project KB, memit-compat-proto-1.md §1.
- Deployment preconditions: project KB, llm-as-database-v1_2-integrated-spec.md
  Appendix A. SC-9 license review uses the overlay redistribution language there.
- Paradigm grounding: project KB, llm-as-database-agent-harness-framework.md.
  Use this for SC-6 — documented MEMIT precedent — to anchor literature search.
- POC staging context: project KB, write-engine-poc-scope.md and
  poc-execution-plan-and-spec-revision-rule.md. These explain why target
  commitment matters and what it gates.
- External catalog site: https://apxml.com/models — an LLM directory with
  filtering by open-weight, parameter count, release date, and provider.
  Use this as a primary candidate-discovery source. The "Open-Weight Models"
  filter and the parameter / context-window columns are aligned with SC-1,
  SC-7, SC-8 evaluation. Do not treat it as the only source — cross-check
  candidate facts (architecture, layer count, tokenizer) against the model
  family's official release notes via web_fetch.
</inputs>

<criteria_summary>
Hard constraints (any failure is categorical reject — stop evaluating that
candidate at the first miss):
- SC-1: Open weights. Full FFN parameter matrices accessible for direct ΔW
  write. API-only models excluded.
- SC-2: Decoder-only transformer with per-layer FFN. MoE excluded from v1.2.
- SC-3: Transformer block depth ≥ 28. Below 28 layers, the L15–L25 target
  band collapses to too few layers for safe distribution.
- SC-4: Tokenizer stability commitment. Tokenizer version, vocab hash, and
  merges hash must be pinnable for the deployment lifetime.
- SC-5: Pre-LN architecture preferred (LLaMA, Gemma, GPT-J yield stable MEMIT
  optimization); post-LN admits the protocol with looser tolerances and a
  flag in the architecture profile.
- SC-6: Documented MEMIT precedent. At least one published or open-source
  MEMIT implementation exists against this model family or an
  architecturally-equivalent sibling.

Operational constraints (≥ 2 of 3 must be satisfied):
- SC-7: Size envelope 7B–70B parameters.
- SC-8: Single-machine inference fit on operator's available GPU memory.
- SC-9: License permits weight-level modification (ΔW write) AND, if
  shipping overlays is intended, redistribution of the resulting .vindex
  artifact.

Canonical source: memit-compat-proto-1.md §1.
</criteria_summary>

<method>
Work in this order:

1. Build a candidate field of 6–8 models. Start with apxml.com/models filtered
   to open-weight; add candidates from web search for "MEMIT implementation
   open-weights LLM" and similar literature-led queries. Lead with SC-6 —
   models without published or open-source MEMIT precedent should be
   explicitly noted as SC-6-fail before any other evaluation.

2. Evaluate each candidate against SC-1..SC-9 with evidence, not assertion.
   Cite sources. For SC-6, cite the specific paper or repository (kmeng01/memit
   on GitHub is the canonical MEMIT reference; family-specific extensions
   should also be cited where they exist). For SC-9, cite the actual license
   text via web_fetch, not a summary.

3. Apply the selection workflow per memit-compat-proto-1.md §1:
   - Any SC-1..SC-6 failure is categorical reject — stop evaluating that
     candidate at the first hard-constraint miss.
   - Operational constraints SC-7..SC-9 are scored, not gated; ≥ 2 of 3
     must hold for admission.

4. Produce a comparison matrix in the format below.

5. Short-list the top 2–3 candidates with rationale.

6. Surface open questions the operator must resolve before commitment.
   At minimum: deployment GPU class for SC-8 sizing; overlay redistribution
   intent for SC-9; production-domain corpus characteristics for downstream
   CFB Domain stratum sizing (CFB-1 in MEMIT-COMPAT-PROTO-1).
</method>

<output_format>
Produce a single markdown document with these sections, in order:

## Candidate Field
Table: candidate name, family, parameter count, layer depth, architecture
(pre-LN / post-LN), release date, primary source.

## Per-Candidate Evaluation
One subsection per candidate. For each candidate, walk SC-1..SC-9 with
cited evidence per row, and end with an admit/reject line. If a candidate
fails an SC-1..SC-6 hard constraint, evaluation stops at that row — do not
fill in subsequent SC rows for rejected candidates.

## Comparison Matrix
Markdown table. Rows = candidates. Columns = SC-1 through SC-9. Cell
values: PASS / FAIL / NOTED (with brief evidence reference). Final
column: ADMIT / REJECT.

## Short-List
Top 2–3 admitted candidates ranked, with one paragraph of rationale each.
Cover: SC-6 strength of precedent; SC-7 sweet-spot positioning;
SC-9 license posture; downstream calibration risk profile.

## Open Questions for Operator
Numbered list. Each question states (a) what the operator must decide,
(b) what the decision affects (which SC and/or which downstream protocol),
(c) what the default behavior is if the operator does not decide.

## Session Summary Block
Standard format per framework-spec-writer skill conventions:
- Decisions made
- Constraints established
- Open questions deferred
- Interface contracts defined
- Next session candidates
</output_format>

<constraints>
- Do NOT evaluate candidates against downstream calibration criteria
  (drift sweep ranges, ε cell counts, compaction probe corpus size,
  judge-model latency, per-cell stratification cost). Those are downstream
  of this commitment.
- Do NOT recommend a closed-API model. SC-1 is categorical.
- Do NOT recommend a Mixture-of-Experts model. SC-2 is categorical for
  v1.2; MoE-MEMIT adaptation is out of POC scope.
- Do NOT skip web search on SC-6. Cite at least one source per candidate
  for MEMIT precedent — paper, GitHub repo, or notebook.
- Do NOT take apxml.com listings at face value for SC-3 (layer depth) or
  SC-5 (pre-LN vs post-LN). Cross-check against the model family's
  technical paper or release notes via web_fetch.
- Do NOT commit on the operator's behalf. The output is a recommendation.
  The session ends when the recommendation is delivered; commitment is
  the operator's separate action.
- The output landing point is architecture_profile.json (PF-6 of
  MEMIT-COMPAT-PROTO-1). Once committed, any field mutation invalidates
  every downstream calibration. Surface this risk to the operator
  before recommendation.
</constraints>

<stopping_rule>
The session is complete when:
- The recommendation document is produced in the format above.
- All open questions for the operator are explicitly named.
- The Session Summary Block records decisions, constraints, deferred
  questions, and the next session candidate (Stage 0 corpus authorship,
  pending operator commitment of one short-listed model).

Do NOT extend into Stage 0 corpus drafting in this session, even if
the operator commits inline. Stage 0 is its own session with its own
KB curation.
</stopping_rule>
```

---

*End of session prompt.*
