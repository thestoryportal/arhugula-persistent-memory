/validation-contract-architect
/framework-spec-writer (secondary)
/graph-data-architect (tertiary, for CFB ontology if needed)

<session_context>
Workstream 1, Session 2.4 — CFB v1 Corpus Authorship and Probe-Set v1 Authorship.

Predecessor: Session 2.3 closed PASS on 2026-04-28 with HC-2 verdict locked,
RunPod NV provisioned and bit-identity-verified across 2 across-teardown
cycles, reproducibility manifest finalized, and rsync mirror configured to
external SSD. The Session 2.3 Summary Block is the canonical input to this
session.

Session 2.4 is the FIRST text/spec authoring session in the post-Block-3
workstream. No GPU pod is required for this session — corpus and probe
authorship are pure spec work that does not invoke MEMIT or load any model.

All operator decisions remain locked from Sessions 2.1, 2.2, and 2.3:
  - Production target: LLaMA 3.1 8B (target model commitment in Session 2.5)
  - Calibration baseline: GPT-J 6B (HC-2 PASS verified)
  - Primary venue: RunPod Secure Cloud RTX 4090 on-demand at $0.69/hr
  - Persistent state: NV `large_amethyst_wolverine` + SSD `memit` mirror
  - MEMIT pin: SHA 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b
  - Joint version pin: transformers 4.45.2 + accelerate 0.34.2 + huggingface_hub 0.25.2
  - Container image: runpod/pytorch@sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5
  - HC-2 acceptance band (amended per OQ-S23-3): drift_p_basketball_postunmount_intrapod < 1e-4

The session ends with CFB v1 corpus committed to NV at /workspace/cfb_baseline/
and probe-set v1 committed to NV at /workspace/architecture_profile/probes/
(or equivalent canonical location), Session Summary Block emitted, and
artifacts rsync'd to SSD mirror.
</session_context>

<task>
Author two related deliverables that together prepare Stage 1 SECT execution:

1. **CFB v1 corpus.** A College Football Basketball ground-truth corpus
   defining the facts that Stage 1 will edit into the model. The corpus
   structure must satisfy MEMIT input requirements (subject + prompt +
   target_new + target_true) AND the framework's broader requirements for
   reproducibility, traceability, and probe coverage.

2. **Probe-set v1.** A set of validation queries that exercise the
   MEMIT-edited model post-edit. Probes must distinguish edit success from
   collateral damage, and provide measurable signals on consistency,
   robustness, and generalization.

The session is collaborative spec work. Claude inhabits the Validation
Contract Architect skill (with framework-spec-writer for canonical artifact
structure and graph-data-architect for ontological clarification when
relevant). The operator drives design decisions; Claude facilitates,
surfaces design tensions, and produces formal artifacts.

Key decisions to be made in this session:
  - CFB v1 fact granularity: player-level facts? team-level? mixed?
  - CFB v1 fact count: how many facts is "Stage 1-sized"?
    (3 facts × 3 runs = 9 trials per Stage 1; corpus must enable this)
  - Subject distribution: same subject (Michael Jordan) repeatedly,
    or distinct subjects per fact?
  - Probe categories: consistency probes (paraphrase robustness),
    generalization probes (related but unedited facts), specificity probes
    (unrelated facts, must remain unchanged), unmount probes (post-unmount
    parity with pre-edit baseline)
  - Probe count per category
  - Token-id discipline (per OQ-S23-6): each probe expected output must
    be sourced from actual model output, not predicted; this requires
    a probe authorship workflow that captures token IDs from the live
    model on the calibration baseline (GPT-J 6B)
  - OQ-S23-14 disposition: clean up the duplicate notebook at /workspace/
    root, or retain it as forensic evidence
</task>

<inputs>
Required reading (priority order):
- session-2_3-summary-block.md: Session 2.3 closure record; canonical input
  for Session 2.4 and downstream
- reproducibility_manifest.json: pinned-version record; informs probe
  authorship by establishing the calibration baseline anchors
- oq-s23-backlog-v2.md: 14 deferred OQs; OQ-S23-6 (token-id discipline) and
  OQ-S23-14 (duplicate notebook) directly apply to this session
- llm-as-database-v1_2-integrated-spec.md: framework specification for CFB
  corpus and probe structure requirements

Optional / reference:
- block-2-runpod-notebook.md: shows the canonical fact format used in HC-2
  ("Michael Jordan plays the sport of" subject/prompt/target_new/target_true)
- memit-patches-canonical.md: MEMIT input format constraints
- block-2-3-runbook-deltas.md: runbook authorship constraints inherited from
  Session 2.3 (token-id source discipline, image preconditions, etc.)

Skill references:
- /mnt/skills/user/validation-contract-architect/SKILL.md
- /mnt/skills/user/framework-spec-writer/SKILL.md
- /mnt/skills/user/graph-data-architect/SKILL.md
</inputs>

<corpus_v1_requirements>
CFB v1 must satisfy the following at session close:

1. **MEMIT input compliance.** Each fact must be expressible as:
   {prompt, subject, target_new, target_true} with prompt containing
   "{}" placeholder for subject substitution.

2. **Stage 1 sizing.** Corpus must support 3 facts × 3 runs (9 trials).
   Minimum 3 facts; recommended 5-10 facts for Stage 2 sweep flexibility.

3. **Subject diversity.** At least 2 distinct subjects across the corpus
   to test cross-subject generalization in probe-set v1.

4. **Domain coherence.** "CFB" defines the corpus topic boundary
   (College Football Basketball — a curated overlap of NCAA football and
   NCAA basketball, OR a deliberately wider sports domain TBD). The
   operator decides the topical boundary in this session.

5. **Probe pairability.** Each fact in CFB v1 must have at least one
   matching probe in probe-set v1 of each probe category (consistency,
   generalization, specificity, unmount).

6. **Reproducibility provenance.** Each fact must record:
   - Source citation (Wikipedia article URL, sports reference URL, etc.)
   - Author timestamp
   - Subject token IDs at GPT-J 6B (per OQ-S23-6 discipline)
   - target_new and target_true token IDs at GPT-J 6B
   - Pre-edit P(target_true) measured on calibration baseline
   - Pre-edit P(target_new) measured on calibration baseline

7. **Format.** YAML or JSON canonical form; must round-trip parse without
   loss; must be diff-friendly for version control.
</corpus_v1_requirements>

<probe_set_v1_requirements>
Probe-set v1 must satisfy the following at session close:

1. **Four probe categories with explicit purpose:**
   - **Consistency probes.** Paraphrase the edited fact's prompt;
     post-edit model should give same target_new with high probability.
     Tests robustness to surface form variation.
   - **Generalization probes.** Related but unedited facts in the same
     subject's domain; post-edit model should NOT have changed these.
     Tests collateral damage radius.
   - **Specificity probes.** Unrelated facts (different subject, different
     domain); post-edit model must NOT have changed these. Tests
     edit isolation.
   - **Unmount probes.** Post-unmount parity check; same prompts as
     pre-edit baseline; values must match within 1e-4 (per
     OQ-S23-3 amended HC-2 band).

2. **Per-fact coverage.** For each fact in CFB v1, at minimum:
   - 2 consistency probes (paraphrase variants)
   - 2 generalization probes (related but unedited)
   - 2 specificity probes (unrelated)
   - 1 unmount probe (pre-edit baseline value at exact prompt)

3. **Token-id discipline (OQ-S23-6).** Each probe expected output must
   be sourced from actual model output on calibration baseline
   (GPT-J 6B). Predicted/derived values are not acceptable. The
   probe authorship workflow must specify HOW these values are captured;
   actual capture is deferred to Stage 1 prep (Session 2.5) or done
   as a sub-task in this session if a quick GPT-J 6B inference cell
   is run on a temporary pod.

4. **Reproducibility provenance.** Each probe must record:
   - Probe ID (unique, traceable)
   - Linked fact ID (which CFB v1 fact it pairs with)
   - Probe category
   - Expected output (top-1 token, top-5 distribution if relevant)
   - Acceptance band (drift tolerance)
   - Author timestamp

5. **Format.** Same YAML/JSON canonical form as CFB v1.
</probe_set_v1_requirements>

<method>
Section 1 — Foundational design questions (Socratic, ~30-45 min)

Claude (as Validation Contract Architect) facilitates a structured
conversation surfacing design decisions. Suggested order:

1.1 Topic boundary: What is "CFB" for this corpus?
   - Strict College Football + College Basketball overlap (athletes
     who played both)?
   - Broader sports facts where the model has measurable prior?
   - Other domain (operator's call)?

1.2 Fact count: 3? 5? 10? Trade-offs with Stage 2 sweep flexibility.

1.3 Subject distribution: How many distinct subjects?
   - Same subject repeatedly (Michael Jordan all 5 facts) tests
     intra-subject edit consistency
   - Distinct subjects per fact tests cross-subject generalization
   - Mixed strategy possible

1.4 Fact format: prompt template choice. The HC-2 fact uses
   "Michael Jordan plays the sport of"; CFB v1 may follow this
   pattern or use different templates.

1.5 Probe count per category per fact: minimum 2 consistency, 2
   generalization, 2 specificity, 1 unmount = 7 probes/fact.
   For 5 facts: 35 probes. Adjust as operator preferences emerge.

1.6 Token-id capture workflow: how/when are GPT-J 6B token IDs
   captured for the CFB v1 facts and probe-set v1 expected outputs?
   Options:
   - Spin up a temporary low-tier pod in this session (~$0.20)
     and run a token-id capture cell.
   - Defer to Session 2.5 prep (Stage 1 prep cluster).
   - Author CFB v1 + probe-set v1 with placeholders, fill at
     Session 2.5 prep.

Section 2 — CFB v1 corpus authorship (~30 min)

Based on Section 1 decisions, Claude drafts CFB v1 in canonical YAML/JSON
format. Operator reviews and iterates. Output structure:

  cfb_v1:
    metadata:
      version: "1.0"
      authored_at: "2026-04-XX..."
      author: "operator + Claude (Validation Contract Architect)"
      domain: "<as decided in 1.1>"
      target_model_baseline: "EleutherAI/gpt-j-6B (revision float16)"
    facts:
      - id: "cfb-001"
        subject: "<subject>"
        prompt: "<prompt template with subject placeholder>"
        target_new: "<new target>"
        target_true: "<original target>"
        source_citation: "<URL>"
        token_ids: { ... }   # placeholder if deferred per 1.6
        baseline_probabilities: { ... }   # placeholder if deferred
      - id: "cfb-002"
        ...

Section 3 — Probe-set v1 authorship (~30 min)

Pair each CFB v1 fact with probes per probe_set_v1_requirements §2.
Output structure:

  probe_set_v1:
    metadata:
      version: "1.0"
      authored_at: "..."
      author: "..."
      paired_corpus: "cfb_v1"
    probes:
      - id: "p-cfb-001-consistency-1"
        linked_fact_id: "cfb-001"
        category: "consistency"
        prompt: "<paraphrase of cfb-001 prompt>"
        expected_top_1_post_edit: "<token>"
        expected_top_1_post_unmount: "<token>"
        acceptance_band: "..."
      - id: "p-cfb-001-generalization-1"
        ...

Section 4 — OQ-S23-14 disposition (~5 min)

Operator decides: remove, migrate, or retain the duplicate notebook at
/workspace/llm-as-database-agent-context-smoke-test.ipynb. If remove or
migrate, session includes a small command to execute on next pod
deployment.

Section 5 — Deferred token-id capture decision (~5 min)

If operator chose to capture token IDs in this session: agent specifies
the capture procedure (a small Python script run on a temporary pod). If
deferred: agent annotates CFB v1 and probe-set v1 with placeholder fields
and explicit "fill at Session 2.5" markers.

Section 6 — Artifact persistence and Session Summary Block (~10 min)

Three options for artifact persistence:
  A. Save artifacts to project KB only (no NV write this session;
     they propagate to NV at next pod deployment)
  B. Spin up a temporary low-tier pod for ~$0.20, write artifacts to
     /workspace/cfb_baseline/ and /workspace/architecture_profile/probes/,
     rsync to SSD, terminate
  C. Save artifacts to project KB AND write to MBP local archive AND
     defer NV write to next pod deployment

Operator selects. Default recommendation: A (lowest cost, simplest;
NV write happens at Session 2.5 prep when a pod will be spun up anyway).

Session Summary Block emitted in standard format: Decisions made /
Constraints established / Open questions deferred / Interface contracts
defined / Next session candidates.
</method>

<output_format>
Two primary artifacts:

1. cfb-v1.yaml (or cfb-v1.json) — canonical corpus
2. probe-set-v1.yaml (or probe-set-v1.json) — canonical probe set

Plus standard session deliverables:

3. session-2_4-summary-block.md — closure record

If operator selects Method §6 option B (NV write):
4. NV writes via SSH-pipe-from-MBP per OQ-S23-19 discipline

If Section 5 capture in-session:
5. token-id-capture-results.json — measured token IDs and baseline
   probabilities
</output_format>

<constraints>
- Do NOT invoke MEMIT or load any model in this session. CFB v1 and
  probe-set v1 are spec deliverables, not execution artifacts.
- Do NOT default to assuming a GPU pod is available. The session can
  complete entirely without GPU resources unless §6 option B is chosen.
- Do NOT skip the token-id source discipline (OQ-S23-6). If token IDs
  are placeholder, they must be EXPLICITLY marked as such with a
  forward-routing tag pointing to Session 2.5 prep.
- Do NOT exceed Session 2.4 budget envelope. Target wall time: 90 min
  conversation + 30 min artifact authorship. Cost: $0 (no pod) to
  ~$0.50 (temporary pod for token-id capture).
- Do NOT begin Stage 1 SECT execution. That is Session 2.6+ scope.
- Do NOT commit to LLaMA 3.1 8B target model decisions. That is
  Session 2.5 scope.
- If Section 1 design questions surface tensions that require
  framework-council scope, surface as a deferred OQ rather than
  resolving in-session.
- If a verification step surfaces an environment incompatibility,
  surface as an open question. Do not work around silently.
</constraints>

<stopping_rule>
Session 2.4 closes successfully on ALL of:
1. CFB v1 corpus authored, validated, and persisted (KB, NV, or both
   per §6 selection)
2. Probe-set v1 authored, validated, and persisted (same persistence
   target)
3. OQ-S23-14 disposition decided (remove / migrate / retain)
4. Token-id discipline either captured in-session or marked deferred
   with explicit Session 2.5 fill obligation
5. Session Summary Block emitted

Halt path: if any design decision in Section 1 requires Council scope
(multi-specialist tension), session can pause and re-route to a
framework-council sub-session before resuming.

The session does NOT proceed to:
- Stage 1 SECT execution
- LLaMA 3.1 8B target model commitment (Session 2.5)
- Stage 1 runbook authorship (Session 2.5)
- Token-id capture is OPTIONAL in-session (defer to 2.5 if convenient)
</stopping_rule>

# Session 2.4 — Orientation for Next Agent

## 1. Purpose

This session authors the corpus and probe-set that Stage 1 SECT execution
will use. It is the first session post-Block-3 and the first non-execution
session in the workstream. The session establishes specification ground
truth that Sessions 2.5+ will operationalize.

## 2. Read Order for Next Agent

| Priority | Document | Purpose |
|---|---|---|
| 1 | session-2_3-summary-block.md | Closure record from prior session; locked decisions |
| 2 | reproducibility_manifest.json | Pinned versions; calibration baseline anchors |
| 3 | oq-s23-backlog-v2.md | OQ-S23-6 (token-id discipline) and OQ-S23-14 (notebook cleanup) apply directly |
| 4 | llm-as-database-v1_2-integrated-spec.md | Framework spec for corpus/probe requirements |
| 5 | block-2-runpod-notebook.md (optional) | Reference fact format from HC-2 |

## 3. State at Session Start

| Element | Value |
|---|---|
| HC-2 verdict | PASS (locked from Session 2.3) |
| Calibration baseline model | GPT-J 6B float16, SHA `b71ae8bc...` |
| Production target model | LLaMA 3.1 8B (commitment deferred to Session 2.5) |
| NV state | Detached (operator may have terminated pod from Session 2.3) |
| Reproducibility manifest | Finalized at NV `/workspace/reproducibility_manifest.json` |
| Sync mirror | `/Volumes/memit/llm-database-poc-mirror/` |

## 4. Forward Pointers

After Session 2.4 closes, the immediate downstream sessions are:

| Session | Topic | Blocked on |
|---|---|---|
| 2.5 | Stage 1 SECT execution prep + LLaMA 3.1 8B target model commitment | Session 2.4 closure |
| 2.6 | Stage 1 SECT execution (3 facts × 3 runs) | Session 2.5 closure |

OQ-S23-6 (token-id source discipline) closes at Session 2.5 prep if
deferred from this session, OR closes here if captured in-session.

OQ-S23-14 (duplicate notebook disposition) closes here.

All other OQ-S23-* entries route to Session 2.5+ as documented in the
v2 backlog.

## 5. Critical Operator Behaviors to Preserve

| Behavior | Source |
|---|---|
| Operator drives design decisions; Claude facilitates | Session 2.4 collaborative authorship pattern |
| Each probe expected output sourced from actual model, not predicted | OQ-S23-6 token-id source discipline |
| Artifacts use canonical YAML/JSON; round-trip parseable | Reproducibility provenance |
| Spec work; no MEMIT invocation; no model loading | Session 2.4 scope boundary |
| Defer GPU-bound work to Session 2.5+ | Cost discipline |
