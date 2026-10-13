# Session 2.1 — GPU Procurement Research Prompt

> Paste the prompt below into a new chat session **after** the entry note has been read. The prompt assumes the project's revised system prompt is in place and the curated KB (10 documents) is loaded.

---

```
/memit-specialist

<session_context>
Workstream 1, Session 2.1 — GPU Procurement Research.
Closes OQ-WS1-4 (multi-GPU parallelization decision; inherited from Session 1.7).
Unblocks Stage 0 corpus authorship and Stage 1 (MEMIT-COMPAT-PROTO-1) execution.

Inherits from Session 2.0:
  - Production target: LLaMA 3.1 8B (~16GB FP16 model weight footprint).
  - Calibration baseline: GPT-J 6B (~12GB FP16). Sequential or coexistent loading.
  - Migration cost: ~40 GPU-hours for second covariance precomputation pass when
    transitioning from GPT-J to LLaMA 3.1 8B.

Operator's current machine: 2020 Intel 16GB MacBook Pro. Cannot run any
candidate locally. This session evaluates cloud GPU procurement and the
alternative of an Apple Silicon upgrade.

Output is a recommendation, not a procurement commitment. Operator commits
in a follow-up.
</session_context>

<task>
Survey GPU procurement options across three modalities — free-tier cloud,
paid cloud rental, and self-hosted Apple Silicon — against the criteria
defined below. Produce a structured recommendation document the operator
can review and use to make a procurement decision.
</task>

<inputs>
- Per-stage GPU-hour estimates and wall-clock envelope: project KB,
  poc-execution-plan-and-spec-revision-rule.md §1.3 (~1,000-2,400 GPU-hours
  total; 7-11 weeks multi-GPU, 12-22 weeks single-GPU on a 7B-13B target).
- Per-stage memory profile: project KB, the four protocol documents
  (memit-compat-proto-1, memit-drift-proto-1, epsilon-calib-proto-1,
  compaction-probe-calib-proto-1, judge-calib-proto-1).
- Target model VRAM requirements: project KB, the target model
  recommendation document. Production target LLaMA 3.1 8B (~16GB FP16);
  calibration baseline GPT-J 6B (~12GB FP16). Plan for ~1.5× VRAM
  during MEMIT covariance precomputation per memit-compat-proto-1 §PF-5.
- Deployment preconditions: project KB, llm-as-database-v1_2-integrated-spec.md
  Appendix A. Single OS user owning harness process; filesystem readable
  only by harness user; persistent storage required for architecture_profile.json
  hash anchor and .vindex overlays across sessions.
- Judge inference latency budget: project KB, judge-calib-proto-1.md §2.1
  — p95 ≤ 800ms per response on deployment GPU class. This binds
  candidate GPU classes against Stage 3c viability.
</inputs>

<criteria_summary>
Define and apply criteria in this structure. Lead with HC-2 (toolchain
compatibility) — any failure is categorical reject, parallel to how SC-6
led the target model selection in Session 2.0.

Hard constraints (any failure is categorical reject — stop evaluating
that candidate at the first miss):

- HC-1: Sufficient memory to load the larger of {LLaMA 3.1 8B, GPT-J 6B}
  in FP16 plus 1.5× headroom for MEMIT covariance precomputation.
  Floor: 24GB VRAM or unified memory comfortably; 16GB VRAM is the
  hard minimum and only fits with FP16 quantization tricks.
- HC-2: MEMIT toolchain compatibility. Either CUDA-capable (NVIDIA) or
  documented MEMIT/ROME/EasyEdit precedent on the platform's compute
  backend. Apple Silicon's PyTorch MPS and MLX backends currently have
  zero published MEMIT precedent — flag this explicitly. AMD ROCm has
  partial precedent and should be evaluated case-by-case.
- HC-3: Persistent storage for architecture_profile.json hash anchor
  and .vindex overlays across sessions. Free-tier providers that wipe
  state between sessions are operationally impractical for the multi-week
  POC unless paired with a separate persistent storage backend.
- HC-4: Tenant isolation per Appendix A — single OS user owning the
  harness process; filesystem privacy. Single-tenant bare-metal or
  isolated container strongly preferred over shared-tenant notebook
  environments. Document the audit posture per provider.
- HC-5: Reproducibility. Pinned environment image, deterministic
  decoding support, ability to reproduce runs across sessions. Evaluate
  against provider environment-versioning posture.

Operational constraints (≥ 3 of 5 must be satisfied for admission):

- OC-1: Cost envelope. Total cost across the POC GPU-hour budget
  (~1,000-2,400 hours) must be tractable for the operator. Calculate
  total POC cost per candidate at both the low and high estimates;
  flag candidates over $5K total at the high estimate.
- OC-2: Wall-clock support. Provider supports continuous long-running
  jobs without forced pre-emption. Stage 2 sweep is 36+ measurement
  points × ≥3 replicates and benefits from uninterrupted runs.
- OC-3: Multi-GPU scaling availability. Stage 3 sub-protocols can run
  in parallel post-PROBE_SET_RATIFICATION; multi-GPU compresses Stage 3
  from ~7-13 weeks sequential to ~3-4 weeks parallel.
- OC-4: Judge inference latency on candidate GPU class. Per JUDGE-CALIB-
  PROTO-1 §2.1, p95 ≤ 800ms per response under deterministic decoding.
  This binds the GPU class for Stage 3c — sub-mid-tier GPUs may fail.
- OC-5: Egress and storage cost predictability. Some providers charge
  high egress fees that compound over the POC. Flag any provider whose
  egress structure could materially change total cost.

Apple Silicon-specific evaluation (in addition to the above):

- AS-1: MEMIT toolchain port effort. Estimate the work required to run
  kmeng01/memit or EasyEdit against PyTorch MPS or MLX. Cite any
  community ports, GitHub issues, or known successful runs of MEMIT
  derivatives on Apple Silicon.
- AS-2: Numerical precision on covariance precomputation. PF-5 in
  MEMIT-COMPAT-PROTO-1 escalates to KILL-2 on covariance divergence or
  NaNs. MPS backend has a history of FP precision differences with CUDA;
  surface this risk specifically.
- AS-3: Total-cost-of-ownership comparison. Compare upfront cost of an
  Apple Silicon machine sufficient for the POC against equivalent cloud
  rental for the same wall-clock and GPU-hour budget. Include resale
  value and post-POC use considerations.
</criteria_summary>

<method>
Work in this order:

1. **Build a free-tier cloud candidate field of 4-6 providers.** Google
   Colab (free tier and Pro), Kaggle, Lightning AI free tier, Hugging
   Face Spaces with GPU, and any other current free-GPU offerings.
   For each, document: GPU class offered free, session time limits,
   weekly hour caps, persistent storage status, eligibility constraints
   (.edu, region, account history).

2. **Build a paid cloud candidate field of 6-8 providers.** RunPod,
   Lambda Labs, Vast.ai, CoreWeave, Together.ai, Modal, Paperspace,
   AWS/GCP/Azure on-demand, plus any other current relevant offerings.
   Cover the price range. For each, document: available GPU classes,
   spot-vs-on-demand pricing, persistent storage offering, audit posture
   (single-tenant vs shared, ToS introspection language), egress cost.

3. **Build an Apple Silicon candidate field.** Use web search to verify
   the current (post-knowledge-cutoff) Mac lineup. As of last known
   state: Mac Studio with M3 Ultra (up to 192GB unified), Mac Studio
   with M4 Max (up to 128GB), MacBook Pro 14"/16" with M4 Pro/Max (up
   to 128GB unified). Verify current configurations, prices, and
   release status via web search.

4. **Evaluate each candidate against HC-1..HC-5.** Cite sources. For
   HC-2 specifically, cite the MEMIT toolchain compatibility evidence —
   for cloud GPU this is "CUDA capable" with version reference; for
   Apple Silicon this is the documented (or absent) MEMIT-on-MPS or
   MEMIT-on-MLX evidence.

5. **Apply admission rules.** Any HC-1..HC-5 failure rejects categorically.
   Operational constraints OC-1..OC-5 are scored; ≥ 3 of 5 must hold
   for admission. Document each candidate's score with evidence.

6. **For Apple Silicon candidates that survive HC-1..HC-5, evaluate
   AS-1, AS-2, AS-3.** Estimate toolchain port effort in weeks and
   GPU-hours-equivalent. Estimate covariance precomputation risk
   qualitatively (low/medium/high) with evidence. Compute TCO comparison
   against the closest cloud-rental equivalent.

7. **Produce comparison matrices** (one per modality, plus a unified
   short-list table).

8. **Short-list 3-5 candidates spanning the modalities** with rationale.
   Cover at least one free-tier option (for pre-flight smoke testing
   of toolchain), at least one paid cloud option (for the bulk of the
   POC), and Apple Silicon if it survives admission.

9. **Surface open questions for the operator** — at minimum: total
   POC budget envelope; preferred audit posture; Apple Silicon
   long-term post-POC use case; multi-GPU vs. single-GPU schedule
   preference.
</method>

<output_format>
Produce a single markdown document with these sections, in order:

## Bottom Line Up Front
Three-sentence summary: which modality and which candidate(s) the
recommendation favors, why, and what the operator must decide before
procurement.

## Candidate Field
Three sub-sections — free-tier cloud, paid cloud, Apple Silicon — each
with a brief table of name, key spec (VRAM/unified memory, GPU class),
release date or current pricing, primary source.

## Per-Candidate Evaluation
Sub-sections per candidate. For each: HC-1..HC-5 verdicts with cited
evidence, OC-1..OC-5 scores, and admit/reject line. For Apple Silicon
admits: also AS-1..AS-3 evaluation.

## Comparison Matrix
One unified markdown table. Rows = candidates. Columns = HC-1..HC-5,
OC-1..OC-5, total-POC-cost-estimate, ADMIT/REJECT.

## Short-List
3-5 candidates ranked, with one paragraph of rationale each. Identify
the recommended primary, recommended secondary, and any free-tier
candidate suitable for pre-flight smoke testing of toolchain.

## Open Questions for Operator
Numbered list. Each question states (a) what the operator must decide,
(b) what the decision affects, (c) what the default behavior is if
the operator does not decide.

## Apple Silicon Long-Term Note
A separate sub-section if Apple Silicon is rejected for the POC but
might be reconsidered post-POC for v2 or for ongoing harness operation.
This is operator-relevant information that doesn't fit cleanly in
the recommendation itself.

## Session Summary Block
Standard format per framework-spec-writer skill conventions:
Decisions made / Constraints established / Open questions deferred /
Interface contracts defined (if any) / Next session candidates.
</output_format>

<constraints>
- Do NOT rely on training data for pricing or availability. Pricing
  changes weekly and Apple's lineup may have shifted. Web-search every
  candidate before scoring.
- Do NOT recommend a free-tier provider as the primary POC venue. Free
  tiers are useful for pre-flight smoke testing, not for the multi-week
  full POC execution. Stage 2 alone is 3-6 weeks of continuous runtime.
- Do NOT default Apple Silicon to "no" on AS-1 without doing the
  literature search. There may be community ports of MEMIT to MPS or
  MLX. If there are none, that finding itself is a citable verdict
  parallel to how SC-6 rejected Falcon in Session 2.0.
- Do NOT default Apple Silicon to "yes" on memory grounds alone.
  Unified memory headroom does not substitute for documented toolchain
  precedent.
- Do NOT recommend a specific spot-vs-on-demand procurement strategy
  in this session. That's an operational decision for the procurement
  follow-up, not the recommendation. Just surface the spot vs. on-demand
  distinction with cost implications.
- Do NOT commit on the operator's behalf. The output is a recommendation.
  The session ends when the recommendation is delivered; commitment
  happens in a follow-up.
- Surface any provider whose ToS includes telemetry, tenant-workload
  introspection, or model-output logging. These are HC-4 audit-posture
  failures regardless of how attractive the pricing looks.
</constraints>

<stopping_rule>
The session is complete when:
- The recommendation document is produced in the format above.
- All open questions for the operator are explicitly named.
- The Session Summary Block records decisions, constraints, deferred
  questions, and the next session candidate (architecture_profile.json
  drafting session, pending operator procurement decision).

Do NOT extend into procurement-commitment work or architecture_profile.json
drafting in this session. Both are downstream of this recommendation.
</stopping_rule>
```

---

*End of session prompt.*
