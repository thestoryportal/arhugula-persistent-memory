# workstream-1_5-master-plan.md

Master plan for Workstream 1.5 — the Adversarial Stress-Test Phase. This document is the canonical operational reference for running WS1.5 when its entry gate is reached. It is authored ahead of WS1.5 entry (during Session 2.3 closure / handoff to Session 2.4) so that the seven WS1.5 sessions are derivable from this document at gate time, without requiring contextual reconstruction by a future agent.

This document complements but does not replace:
- `skill-design-decisions-adversarial.md` — governs the 5-skill team's design and tension structure
- `adversarial-skills-starter-descriptions-v2.md` — starter prompts for skill authorship (5 skills + framework-council extension)
- The framework spec v1.2 — the subject of adversarial review

Authored: 2026-04-28 (Session 2.3 closure window)
Authority: operator-ratified at point of incorporation into project KB

---

## 1. Pre-Conditions for WS1.5 Entry

WS1.5 cannot begin until ALL of the following are true. Each precondition has a verification check and a remediation path if not met.

### 1.1 Workstream 1 Stage 4 PASS verdict

**Precondition:** Stage 4 POC packet acceptance session has closed with PASS verdict.

**Verification:** Final session summary block of WS1 reports `STAGE_4_VERDICT: PASS` (or operator-equivalent acceptance language). The POC packet itself is committed to NV at `/workspace/poc_packet/` and mirrored to SSD.

**If not met:** WS1.5 does not begin. If Stage 4 returns CONDITIONAL PASS, operator decides whether to enter WS1.5 with documented Stage-4 conditions held open, or to remediate Stage-4 conditions first. If Stage 4 returns FAIL, WS1.5 is moot — framework returns to WS1 amendment or re-scoping.

### 1.2 Five adversarial skill SKILL.md files exist

**Precondition:** All five adversarial skills are authored and installed at `/mnt/skills/user/{skill-name}/SKILL.md`:
- chaos-engineer
- finops-tokenomics-auditor
- semantic-degradation-analyst
- adversarial-pen-tester
- context-latency-profiler

**Verification:** `ls /mnt/skills/user/{chaos-engineer,finops-tokenomics-auditor,semantic-degradation-analyst,adversarial-pen-tester,context-latency-profiler}/SKILL.md` returns five files, all non-empty, each beginning with the appropriate `# {Skill Name}` heading.

**If not met:** WS1.5 does not begin. Operator authors the missing skills using `adversarial-skills-starter-descriptions-v2.md` Sections 1-5. Each authoring session is approximately 30-60 minutes in the dedicated skill-building project.

### 1.3 framework-council extension authored

**Precondition:** The framework-council SKILL.md has been updated to include the `adversarial-review` session type per Section 6 of `adversarial-skills-starter-descriptions-v2.md`.

**Verification:** `grep -i "adversarial-review" /mnt/skills/user/framework-council/SKILL.md` returns matches, AND the file's session-types or modes section explicitly distinguishes constructive review from adversarial review.

**If not met:** WS1.5 does not begin. Operator runs the Section 6 extension session in the skill-building project. This must occur AFTER Section 1.2's five skills are complete, since the extension references those skills by name.

### 1.4 Project instructions updated for WS1.5 phase

**Precondition:** The framework project's instructions reflect:
- Workstream 1 status changed from "Empirical POC Execution" to "Workstream 1 closed PASS" with closure date and POC packet reference
- New "Workstream 1.5 — Adversarial Stress-Test Phase" status block added with current session indicator
- Five adversarial skills added to "Installed skills" list (with one-line descriptions matching governance doc §3)
- framework-council description updated to note adversarial-review session type

**Verification:** Operator visually confirms the project instructions before pasting any WS1.5 starter prompt.

**If not met:** Operator updates project instructions per §3 of this document.

### 1.5 KB recurated for adversarial review

**Precondition:** The project KB contains documents needed for WS1.5 sessions and excludes documents that are no longer relevant. See §2 for the canonical curated KB.

**Verification:** Operator visually confirms KB composition matches §2 before WS1.5 entry.

**If not met:** Operator performs KB recuration per §2 of this document.

---

## 2. KB Curation for WS1.5

The adversarial review needs different KB content than the constructive WS1 execution sessions did. Specifically, adversarial skills need access to the framework spec, the tension map, the cumulative OQ register, and the POC packet's empirical findings — but they do NOT need execution-specific runbook details, pod operational state, or per-stage runbook deltas.

### 2.1 KB documents to ADD at WS1.5 entry

| Document | Source | Purpose for WS1.5 |
|---|---|---|
| `skill-design-decisions-adversarial.md` | Pre-authored (handoff package) | Governance for the 5-skill team; tension map structure; council integration |
| `workstream-1_5-master-plan.md` (this document) | Pre-authored (handoff package) | Operational reference for the phase |
| `stage-4-poc-packet.md` (or equivalent name) | Generated at WS1 closure | Final POC verdict, empirical findings, residual conditions |
| `cumulative-oq-register.md` | Synthesized at WS1 closure from all OQ-S2x-* backlogs | Single canonical view of all open questions surviving WS1; routes some to WS1.5 review |
| `cumulative-tension-map.md` | Synthesized at WS1 closure from all session tension entries | Pre-existing tensions that adversarial findings will integrate with |

### 2.2 KB documents to RETAIN at WS1.5 entry

| Document | Reason for retention |
|---|---|
| `llm-as-database-v1_2-integrated-spec.md` | The subject of adversarial review; load-bearing |
| `memit-patches-canonical.md` | Adversarial skills reference MEMIT-specific contracts (e.g., chaos-engineer reviewing covariance cache failure modes) |

### 2.3 KB documents to REMOVE at WS1.5 entry

| Document | Reason for removal |
|---|---|
| All `session-2_X-summary-block.md` files (X = 1 through final WS1 session) | Synthesized into stage-4-poc-packet.md and cumulative-oq-register.md; no longer needed individually |
| All `oq-s2X-backlog-vN.md` files | Synthesized into cumulative-oq-register.md |
| All `block-X-execution-plan.md` and `block-X-runpod-notebook.md` files | WS1 execution-specific; WS1.5 does not invoke runtime |
| All `session-2_X-starter-prompt.md` files | Spent; not reference material |
| `reproducibility_manifest.json` | Execution artifact; not load-bearing for spec-time adversarial review (adversarial findings reference spec contracts, not specific image digests) |
| `block-2-3-runbook-deltas.md` and equivalents | WS1 execution detail |
| `architecture-profile-seed.json` | Stage 1 seed; superseded |

### 2.4 Final curated KB at WS1.5 entry

```
Project KB at WS1.5 entry:
├── llm-as-database-v1_2-integrated-spec.md     (retained from WS1)
├── memit-patches-canonical.md                  (retained from WS1)
├── skill-design-decisions-adversarial.md       (added at WS1.5 entry)
├── workstream-1_5-master-plan.md               (added at WS1.5 entry — this doc)
├── stage-4-poc-packet.md                       (added at WS1 closure)
├── cumulative-oq-register.md                   (added at WS1 closure)
└── cumulative-tension-map.md                   (added at WS1 closure)
```

**Total: 7 documents.** Anything else is either WS1 execution carryover (remove) or WS1.5 in-progress artifacts (added during WS1.5 sessions per §6).

### 2.5 KB additions during WS1.5

As WS1.5 sessions complete, their outputs join the KB:

| WS1.5 session | Adds to KB |
|---|---|
| A.1 (kickoff) | `workstream-1_5-session-A_1-summary-block.md` |
| A.2 (chaos) | `chaos-engineer-fmr-register-v1.md` + summary block |
| A.3 (finops) | `finops-cme-register-v1.md` + summary block |
| A.4 (semantic) | `semantic-degradation-dme-register-v1.md` + summary block |
| A.5 (pen-test) | `pen-test-tma-register-v1.md` + summary block |
| A.6 (latency) | `latency-lbe-register-v1.md` + summary block |
| A.7 (synthesis) | `ws1_5-synthesis-output.md` (amendment cluster + tradeoff register) + summary block |

By WS1.5 closure, the KB will have grown to ~14 documents. At WS3 entry, another KB recuration occurs (out of scope for this document).

---

## 3. Project Instructions Update for WS1.5 Entry

The project instructions need targeted updates at WS1.5 entry. The following diff is illustrative; operator adapts to actual instructions text.

### 3.1 Workstream status block updates

**Find this block (or current equivalent at WS1 closure):**
```
- **Workstream 1 — Empirical POC Execution.** Protocol authoring complete (Sessions 1.1-1.7). Block 1 (Kaggle smoke test) PASS in Session 2.2. Block 2 (RunPod activation, HC-2 dry-run) and Block 3 (persistent state architecture) PASS in Session 2.3. Currently in [whatever the current session was] ...
```

**Replace with:**
```
- **Workstream 1 — Empirical POC Execution.** CLOSED PASS at [date] with Stage 4 POC packet acceptance. POC verdict: [PASS / CONDITIONAL PASS / FAIL summary line]. Reference: stage-4-poc-packet.md.
- **Workstream 1.5 — Adversarial Stress-Test Phase.** Active. Currently in [Session A.X — title]; remaining [N] sessions. Reference: workstream-1_5-master-plan.md. Outputs feed spec v1.3 amendment cluster authoring and/or accepted-tradeoff register.
- **Workstream 2 — Orchestration path selection (GAP-4).** Open; [resolution status as of WS1 closure].
- **Workstream 3 — Implementation planning.** Blocked on WS1.5 closure. Path-independent components remain available for early planning per IC-WS1-1.
```

### 3.2 Installed skills updates

**Find the existing "Installed skills" list. Add the following five entries (alphabetically or grouped under an "Adversarial team" subheading per operator preference):**

```
- `adversarial-pen-tester` — hostile actor models, attack surfaces,
  trust-boundary subversion, threat-model amendments to the Warden
  contract; output TMA register
- `chaos-engineer` — component failure modes under unexpected
  combinations, cascade failures, recovery-procedure gaps; output FMR
  register
- `context-latency-profiler` — end-to-end timing, scalability cliffs,
  human-meaningful latency budgets; output LBE register
- `finops-tokenomics-auditor` — cost economics at scale, GPU/token/
  storage cost models, cost-cliff identification; output CME register
- `semantic-degradation-analyst` — polysemantic noise, knowledge
  cluster fracturing, edit interference, long-horizon model coherence;
  output DME register
```

### 3.3 framework-council description update

**Find the existing framework-council entry. Update to note adversarial-review session type:**

```
- `framework-council` — multi-specialist facilitated sessions, cross-
  domain tension mapping; supports two session types: standard
  constructive review (multi-specialist constructive design dialogue)
  and adversarial-review (adversarial findings + constructive
  counterpart dialogue per skill-design-decisions-adversarial.md §5)
```

### 3.4 Reference document update

**Add a line in the appropriate section:**

```
Reference `skill-design-decisions-adversarial.md` for adversarial team
governance. Reference `workstream-1_5-master-plan.md` for the WS1.5
phase structure and per-session scopes.
```

### 3.5 Mode statement update (if relevant)

If the existing "Mode" statement says "Primarily brainstorm and specification. Do not produce runtime implementation code in spec or POC-scoping sessions...", append:

```
Workstream 1.5 sessions are adversarial-review sessions: they produce
structured findings (FMR/CME/DME/TMA/LBE register entries) and tension-
map updates, not implementation code or runtime artifacts. Findings
are handed to framework-spec-writer for amendment authorship; the
adversarial team does not author amendments directly.
```

---

## 4. Per-Session Phase Structure

WS1.5 is a 7-session phase. Each session has a defined scope, primary skill invocations, expected wall time, output artifacts, and blocking relationship with adjacent sessions. Operator may compress (combine A.5 and A.6 if scope is small) or expand (split A.4 if Stage 2 sweep data is rich) per discretion.

### 4.1 Session A.1 — WS1.5 kickoff and target enumeration

**Scope.** Activate the adversarial team in-context. Confirm all 5 skills load. Enumerate the spec sections that warrant adversarial review per axis. Establish the WS1.5 working register (where findings will accumulate). Light session — primarily orientation.

**Primary skill invocations.** None of the adversarial skills (this is orientation, not adversarial review yet). framework-council in standard mode for facilitation.

**Expected wall time.** 30-60 minutes.

**Output artifacts.**
- `workstream-1_5-session-A_1-summary-block.md` — kickoff record
- `ws1_5-target-spec-section-register.md` — list of spec sections targeted by each adversarial axis (e.g., "chaos-engineer reviews §11.8 Transaction Controller, §11.9 Lock/Hold split, §11.12 Pruning Agent"; "context-latency-profiler reviews §10 Authorization Gate cascade, §11.10 escalation phase lock/hold")
- `ws1_5-working-register.md` — empty scaffolding for findings registers (FMR/CME/DME/TMA/LBE) populated in subsequent sessions

**Blocked on.** Pre-conditions §1.1-§1.5 all met.

**Blocks.** Session A.2.

### 4.2 Session A.2 — Chaos Engineer adversarial pass

**Scope.** chaos-engineer reviews failure modes against the target spec sections enumerated in A.1. Files findings as FMR-* entries in the working register. Includes constructive counterpart dialogue (state-consistency-theorist, orchestration-comparativist) per the framework-council adversarial-review session type. Each FMR entry receives one of five canonical responses per skill-design-decisions-adversarial.md §5.2.

**Primary skill invocations.** chaos-engineer (primary), state-consistency-theorist (constructive counterpart), orchestration-comparativist (constructive counterpart for orchestration-coordination failures), framework-council (facilitator in adversarial-review mode).

**Expected wall time.** 2-4 hours (longest of the per-axis sessions because chaos analysis is broad).

**Output artifacts.**
- `chaos-engineer-fmr-register-v1.md` — FMR-1 through FMR-N entries with severity, blast radius, current mitigation, proposed remediation class
- `workstream-1_5-session-A_2-summary-block.md`
- Tension-map updates for any T-ADV-1-vs-* tensions surfaced

**Blocked on.** Session A.1.

**Blocks.** Session A.7 (synthesis depends on A.2-A.6 complete). Does NOT block Sessions A.3-A.6 individually; they can run in any order after A.1.

### 4.3 Session A.3 — FinOps & Tokenomics Auditor adversarial pass

**Scope.** finops-tokenomics-auditor builds cost models for major framework operations and reviews cost-scaling assumptions in the spec. Files CME-* findings. Constructive counterparts: memit-specialist (MEMIT compute cost), orchestration-comparativist (orchestrator overhead cost).

**Primary skill invocations.** finops-tokenomics-auditor (primary), memit-specialist (counterpart), orchestration-comparativist (counterpart), framework-council (facilitator).

**Expected wall time.** 2-3 hours.

**Output artifacts.**
- `finops-cme-register-v1.md` — CME-1 through CME-N with cost formulas, scale projections, cost-cliff identification
- `workstream-1_5-session-A_3-summary-block.md`
- Tension-map updates for any T-ADV-2-vs-* tensions

**Blocked on.** Session A.1. Sessions A.2-A.6 may run in any order; sequencing them in alphabetical order (chaos → finops → semantic → pen-test → latency) is the recommended default but not required.

**Blocks.** Session A.7.

### 4.4 Session A.4 — Semantic Degradation Analyst adversarial pass

**Scope.** semantic-degradation-analyst models polysemantic noise and edit-interference patterns against the spec's per-edit-independence assumptions. Heavy use of Stage 2 drift-sweep data (from WS1) as empirical grounding. Files DME-* findings. Constructive counterparts: memit-specialist (per-edit correctness), graph-data-architect (KNN graph-walk reliability).

**Primary skill invocations.** semantic-degradation-analyst (primary), memit-specialist (counterpart), graph-data-architect (counterpart), framework-council (facilitator).

**Expected wall time.** 2-4 hours (data-heavy if Stage 2 sweep produced rich findings).

**Output artifacts.**
- `semantic-degradation-dme-register-v1.md` — DME-1 through DME-N with degradation curves, breakdown thresholds, monitoring proposals
- `workstream-1_5-session-A_4-summary-block.md`
- Tension-map updates for any T-ADV-3-vs-* tensions

**Special note.** This session's findings may motivate amendments to the .vindex bit-identity contract (OQ-S23-11) or to the spec's edit-rate budget assumptions. If Stage 2 sweep data revealed degradation faster than the spec predicted, this is the session where that finding gets formalized.

**Blocked on.** Session A.1. Stage 2 sweep results from WS1 must be present in cumulative-oq-register or stage-4-poc-packet for grounding.

**Blocks.** Session A.7.

### 4.5 Session A.5 — Adversarial Pen-Tester adversarial pass

**Scope.** adversarial-pen-tester enumerates attack chains against trust assumptions in the Warden contract and validation pipeline. Files TMA-* findings. Constructive counterparts: aisecops-specialist (Warden — primary), validation-contract-architect (validator-pipeline subversion).

**Primary skill invocations.** adversarial-pen-tester (primary), aisecops-specialist (counterpart), validation-contract-architect (counterpart), framework-council (facilitator).

**Expected wall time.** 2-3 hours.

**Output artifacts.**
- `pen-test-tma-register-v1.md` — TMA-1 through TMA-N with attacker capability assumptions, attack chains, current Warden countermeasure status, proposed contract refinements
- `workstream-1_5-session-A_5-summary-block.md`
- Tension-map updates for any T-ADV-4-vs-* tensions

**Caveat.** Per skill governance, this session does NOT produce operational exploit code. TMA entries are conceptual attack chains for spec-amendment input, not attacker tutorials.

**Blocked on.** Session A.1.

**Blocks.** Session A.7.

### 4.6 Session A.6 — Context-Latency Profiler adversarial pass

**Scope.** context-latency-profiler builds latency models for major framework operations. Files LBE-* findings. Constructive counterparts: orchestration-comparativist (coordination overhead), validation-contract-architect (validator-cascade depth).

**Primary skill invocations.** context-latency-profiler (primary), orchestration-comparativist (counterpart), validation-contract-architect (counterpart), framework-council (facilitator).

**Expected wall time.** 2-3 hours.

**Output artifacts.**
- `latency-lbe-register-v1.md` — LBE-1 through LBE-N with step-by-step latency models, p50/p95/p99 estimates, scalability cliffs
- `workstream-1_5-session-A_6-summary-block.md`
- Tension-map updates for any T-ADV-5-vs-* tensions

**Blocked on.** Session A.1.

**Blocks.** Session A.7.

### 4.7 Session A.7 — Synthesis council session

**Scope.** All 5 register outputs (FMR, CME, DME, TMA, LBE) are synthesized into a coherent set of WS1.5 deliverables. Cross-axis tensions resolved per the §6 pre-mapped tension table in skill-design-decisions-adversarial.md. Produces either a spec v1.3 amendment cluster (if findings warrant amendments) OR a consolidated accepted-tradeoff register (if findings are accepted as-is). Most sessions produce a mix of both.

**Primary skill invocations.** framework-council (facilitator), framework-spec-writer (amendment authorship), all 5 adversarial skills (referenced for findings; not driving), all relevant constructive counterparts (referenced for confirmed responses).

**Expected wall time.** 3-5 hours.

**Output artifacts.**
- `ws1_5-synthesis-output.md` — the canonical WS1.5 deliverable, containing:
  - Executive summary (severity-rated finding counts per axis)
  - Cross-axis tension resolutions
  - Spec v1.3 amendment cluster proposals (if applicable; routed to framework-spec-writer for canonical authorship)
  - Accepted-tradeoff register (📋 entries with documented reasoning)
  - V2 deferral register (🔴 entries with v2 routing identifiers)
  - WS3 implementation-planning routing notes (which findings inform WS3 architecture)
- `workstream-1_5-session-A_7-summary-block.md`
- WS1.5 closure verdict: PASS (proceed to WS3) or CONDITIONAL (specific amendments must close before WS3 entry)

**Blocked on.** Sessions A.2 through A.6 all complete with summary blocks committed to KB.

**Blocks.** WS3 entry. WS1.5 closes on this session's completion.

### 4.8 Session sequencing flexibility

Sessions A.2-A.6 are independent of each other and can run in any order, in parallel (different conversations on different days), or compressed (e.g., A.5 and A.6 in a single conversation if scope is small). The default sequencing is alphabetical-by-skill (chaos → finops → semantic → pen-test → latency) for predictability, but operator may resequence if a particular finding from one session demands prioritizing another.

### 4.9 Total estimated wall time

| Component | Lower estimate | Upper estimate |
|---|---|---|
| Session A.1 | 30 min | 60 min |
| Sessions A.2-A.6 | 5 × 2 hr = 10 hr | 5 × 4 hr = 20 hr |
| Session A.7 | 3 hr | 5 hr |
| Inter-session operator review and KB updates | 2 hr | 4 hr |
| **Total wall time** | **~16 hr** | **~30 hr** |

Spread across operator's calendar, this is typically 2-4 weeks at a comfortable session-per-few-days cadence.

---

## 5. Per-Session Starter Prompt Templates

Each WS1.5 session is invoked by pasting a starter prompt at the beginning of a new chat session in the framework project. The starter prompt follows a consistent structure. This section provides templates with placeholders for state that becomes available only at WS1.5 entry time.

### 5.1 Common header (all WS1.5 sessions)

Every WS1.5 session starter prompt begins with:

```
[Skill invocations — varies per session]

<session_context>
Workstream 1.5, Session A.[N] — [Session title]

Predecessor: [Previous WS1.5 session, or "Workstream 1 Stage 4 closure
at <date>" for Session A.1]

Workstream 1 closed PASS at [WS1 closure date]. Stage 4 POC packet
verdict: [verdict]. Reference: stage-4-poc-packet.md.

Workstream 1.5 phase active. This session's scope is per
workstream-1_5-master-plan.md §4.[N].

All operator decisions remain locked from prior workstreams.
Spec subject of review: v1.2 (sealed; the v1.3 amendment cluster, if
any, will be authored at Session A.7 synthesis based on findings from
this session and parallel sessions A.2-A.6).
</session_context>

<task>
[Per-session task — see §5.2 through §5.8 below]
</task>

<inputs>
Required reading (priority order):
[Per-session input list — see templates below]

Skill references:
[Per-session skill paths — see templates below]
</inputs>

<method>
[Per-session method — see templates below]
</method>

<output_format>
[Per-session output spec — see templates below]
</output_format>

<constraints>
- Do NOT author spec amendments directly. Findings are handed to
  framework-spec-writer at Session A.7 synthesis.
- Do NOT produce runtime code, monitoring instrumentation, or
  exploit code (per skill governance).
- Do NOT exceed the per-axis ownership boundary defined in
  skill-design-decisions-adversarial.md §3. Cross-axis observations
  belong in a clearly-marked cross-reference subsection only.
- Do NOT produce findings without severity classification per the
  skill's rubric.
- Maintain calibrated severity discipline — not every finding is
  Critical.
</constraints>

<stopping_rule>
[Per-session stop conditions]
</stopping_rule>
```

### 5.2 Session A.1 starter prompt template

```
/framework-council
/chaos-engineer
/finops-tokenomics-auditor
/semantic-degradation-analyst
/adversarial-pen-tester
/context-latency-profiler

[Common header per §5.1, with session number 1 and title "WS1.5
kickoff and target enumeration"]

<task>
Session A.1 is the WS1.5 kickoff. Three deliverables:

1. Verify all five adversarial skills load correctly. Each skill
   should provide a one-paragraph self-introduction confirming its
   activation triggers, owned axis, output class, and severity rubric
   awareness.

2. Enumerate target spec sections per axis. For each adversarial
   skill, identify which spec v1.2 sections are most relevant to
   that skill's stress axis. Output: target-spec-section register.

3. Establish the WS1.5 working register. Empty scaffolding for FMR,
   CME, DME, TMA, LBE entries that subsequent sessions will populate.
</task>

<inputs>
Required reading (priority order):
- workstream-1_5-master-plan.md (this session's reference)
- skill-design-decisions-adversarial.md (governance)
- llm-as-database-v1_2-integrated-spec.md (subject of review)
- stage-4-poc-packet.md (WS1 closure context)
- cumulative-oq-register.md (residual OQs that may seed adversarial
  findings)
- cumulative-tension-map.md (existing tension structure)

Skill references:
- /mnt/skills/user/framework-council/SKILL.md
- /mnt/skills/user/chaos-engineer/SKILL.md
- /mnt/skills/user/finops-tokenomics-auditor/SKILL.md
- /mnt/skills/user/semantic-degradation-analyst/SKILL.md
- /mnt/skills/user/adversarial-pen-tester/SKILL.md
- /mnt/skills/user/context-latency-profiler/SKILL.md
</inputs>

<method>
Section 1 — Skill activation (~15 min)
Each skill provides a one-paragraph self-introduction.

Section 2 — Target enumeration (~30 min)
For each adversarial axis, identify ~3-7 spec sections most relevant.
Operator confirms or amends.

Section 3 — Working register scaffolding (~15 min)
Produce ws1_5-working-register.md with empty FMR/CME/DME/TMA/LBE
table scaffolds.
</method>

<output_format>
Three artifacts:
1. ws1_5-target-spec-section-register.md (per-axis spec section list)
2. ws1_5-working-register.md (empty register scaffolding)
3. workstream-1_5-session-A_1-summary-block.md (kickoff record)
</output_format>

<stopping_rule>
Session A.1 closes successfully on:
1. All 5 adversarial skills confirmed active
2. Target spec sections enumerated per axis
3. Working register scaffolding committed
4. Session Summary Block emitted

The session does NOT proceed to actual adversarial review. Subsequent
per-axis sessions (A.2-A.6) perform the review.
</stopping_rule>
```

### 5.3 Session A.2 starter prompt template (chaos-engineer)

```
/framework-council adversarial-review §11.8-§11.12 (or per A.1 target
register)
/chaos-engineer
/state-consistency-theorist
/orchestration-comparativist

[Common header per §5.1, session number 2, title "Chaos Engineer
adversarial pass"]

<task>
Session A.2 is the first per-axis adversarial pass. chaos-engineer
reviews the target spec sections identified in Session A.1 for its
axis, files FMR-* findings, and engages constructive counterparts
(state-consistency-theorist, orchestration-comparativist) for
canonical responses per skill-design-decisions-adversarial.md §5.2.

For each FMR entry filed, the constructive counterpart MUST provide
one of:
A. Accept finding; spec amendment required → routed to A.7 synthesis
B. Accept finding; mitigation already in spec → adversarial confirms
C. Accept finding as informational tradeoff → 📋 entry
D. Reject finding as out-of-scope speculation → adversarial withdraws
   or provides additional evidence
E. Defer to v2 → 🔴 entry
</task>

<inputs>
Required reading:
- workstream-1_5-master-plan.md §4.2 (this session's scope)
- ws1_5-target-spec-section-register.md (target sections from A.1)
- ws1_5-working-register.md (where findings accumulate)
- llm-as-database-v1_2-integrated-spec.md (subject)
- skill-design-decisions-adversarial.md §3.1, §6 (chaos-engineer
  ownership and pre-mapped tensions)
- cumulative-oq-register.md (some OQs may seed findings)

Skill references:
- /mnt/skills/user/chaos-engineer/SKILL.md
- /mnt/skills/user/state-consistency-theorist/SKILL.md
- /mnt/skills/user/orchestration-comparativist/SKILL.md
- /mnt/skills/user/framework-council/SKILL.md
</inputs>

<method>
Per chaos-engineer methodology (its SKILL.md §5):
1. Read each target spec section
2. Enumerate implicit assumptions
3. Construct adversarial cases violating assumptions
4. Classify by severity per chaos-engineer rubric
5. Identify current mitigation status
6. File FMR-* entries

Per framework-council adversarial-review session structure:
7. For each FMR, constructive counterpart provides canonical response
8. Tensions logged in cumulative-tension-map.md using T-ADV-1-vs-*
   notation per skill-design-decisions-adversarial.md §6
</method>

<output_format>
1. chaos-engineer-fmr-register-v1.md — full FMR-1 through FMR-N
2. workstream-1_5-session-A_2-summary-block.md
3. cumulative-tension-map.md updates (delta only)
</output_format>

<stopping_rule>
Session A.2 closes when:
1. All target spec sections per A.1 register reviewed by
   chaos-engineer
2. All FMR entries have received a canonical response from
   constructive counterpart(s)
3. Tensions logged
4. Session Summary Block emitted

Halt path: if a Critical FMR is filed and no constructive resolution
emerges, the finding is escalated to a multi-session amendment cluster
under A.7 with explicit deferral notation.
</stopping_rule>
```

### 5.4 Session A.3-A.6 starter prompt templates

Sessions A.3 (finops), A.4 (semantic), A.5 (pen-test), and A.6 (latency) follow the same structural pattern as A.2 with these per-skill substitutions:

| Session | Primary skill | Constructive counterparts | Output register | Tension prefix | Skill ownership reference |
|---|---|---|---|---|---|
| A.3 | finops-tokenomics-auditor | memit-specialist, orchestration-comparativist | finops-cme-register-v1.md | T-ADV-2-vs-* | governance §3.2 |
| A.4 | semantic-degradation-analyst | memit-specialist, graph-data-architect | semantic-degradation-dme-register-v1.md | T-ADV-3-vs-* | governance §3.3 |
| A.5 | adversarial-pen-tester | aisecops-specialist, validation-contract-architect | pen-test-tma-register-v1.md | T-ADV-4-vs-* | governance §3.4 |
| A.6 | context-latency-profiler | orchestration-comparativist, validation-contract-architect | latency-lbe-register-v1.md | T-ADV-5-vs-* | governance §3.5 |

To generate each of these starter prompts, take the A.2 template (§5.3 above) and substitute:
- Skill invocations at the top
- Target axis name in the title and task
- Constructive counterpart skill invocations and references
- Output register filename and entry prefix (CME/DME/TMA/LBE)
- Tension prefix (T-ADV-2-vs-* through T-ADV-5-vs-*)
- Skill ownership section reference (§3.2 through §3.5 of governance)

The session's structural shape (input/method/output/constraints/stop conditions) remains identical across A.2-A.6.

### 5.5 Session A.7 starter prompt template (synthesis)

```
/framework-council
/framework-spec-writer
/chaos-engineer (referenced for FMR review)
/finops-tokenomics-auditor (referenced for CME review)
/semantic-degradation-analyst (referenced for DME review)
/adversarial-pen-tester (referenced for TMA review)
/context-latency-profiler (referenced for LBE review)

[Common header per §5.1, session number 7, title "WS1.5 synthesis
council session"]

<task>
Session A.7 is the WS1.5 closure session. Synthesize all findings from
A.2-A.6 into:

1. Executive summary — finding counts per axis, severity distribution,
   summary verdict.

2. Cross-axis tension resolution — for each pre-mapped tension in
   skill-design-decisions-adversarial.md §6 that surfaced during
   A.2-A.6, document the resolution direction (which axis prevails,
   or how the tension is balanced).

3. Spec v1.3 amendment cluster proposals — for each finding marked
   "Accept; spec amendment required" during A.2-A.6, framework-spec-
   writer drafts the amendment proposal in the framework's standard
   amendment block format. Operator and constructive counterparts
   confirm before inclusion.

4. Accepted-tradeoff register — consolidated 📋 entries with
   documented reasoning.

5. V2 deferral register — consolidated 🔴 entries with v2 routing
   identifiers.

6. WS3 routing notes — which findings inform Workstream 3
   implementation planning (e.g., a Critical FMR may demand a specific
   architectural pattern at WS3 entry).

7. WS1.5 closure verdict:
   - PASS: WS3 entry authorized; no specific amendments gate WS3
   - CONDITIONAL: specific amendments must close before WS3 entry
   - FAIL (rare): WS1.5 surfaced findings invalidating the spec; WS1.5
     extends with a remediation phase before WS3
</task>

<inputs>
Required reading:
- All 5 register files (FMR, CME, DME, TMA, LBE) from A.2-A.6
- All 5 session summary blocks from A.2-A.6
- cumulative-tension-map.md (updated through A.2-A.6)
- skill-design-decisions-adversarial.md §6 (pre-mapped tensions)
- llm-as-database-v1_2-integrated-spec.md (for amendment context)

Skill references:
- /mnt/skills/user/framework-council/SKILL.md (in standard mode for
  cross-team facilitation)
- /mnt/skills/user/framework-spec-writer/SKILL.md (for amendment
  authorship)
- The 5 adversarial skill SKILL.md files (referenced for ownership;
  not driving the synthesis)
</inputs>

<method>
Section 1 — Findings inventory (~30 min)
Tabulate all findings across A.2-A.6 by severity. Count per axis.

Section 2 — Cross-axis tension resolution (~60 min)
For each pre-mapped tension that surfaced, document the resolution.

Section 3 — Amendment cluster authorship (~120-180 min)
framework-spec-writer drafts amendment proposals for each "Accept;
amendment required" finding.

Section 4 — Tradeoff and deferral consolidation (~30 min)
Consolidate 📋 and 🔴 entries.

Section 5 — WS3 routing (~30 min)
Identify findings that inform WS3 architecture.

Section 6 — Closure verdict (~15 min)
PASS / CONDITIONAL / FAIL determination.
</method>

<output_format>
Single canonical artifact:
- ws1_5-synthesis-output.md (executive summary, tension resolutions,
  amendment cluster proposals, tradeoff register, deferral register,
  WS3 routing notes, closure verdict)

Plus standard:
- workstream-1_5-session-A_7-summary-block.md
- WS1.5 closure record (committed to project KB at session close)
</output_format>

<stopping_rule>
Session A.7 closes WS1.5 when:
1. All findings from A.2-A.6 inventoried and dispositioned
2. All pre-mapped tensions that surfaced have a documented resolution
3. Amendment cluster proposals authored (or null if no amendments
   warranted)
4. Closure verdict assigned
5. Session Summary Block emitted
6. KB updated to reflect WS1.5 closure

WS1.5 closes on Session A.7 closure. WS3 entry is gated on the closure
verdict per §7.

Halt path: if synthesis surfaces a finding requiring re-engagement of
an A.2-A.6 skill (e.g., new evidence demands chaos-engineer to revisit
an FMR), session may pause for a focused mini-session and resume.
</stopping_rule>
```

---

## 6. Inter-Session Handoff Convention

Each WS1.5 session ends with a summary block following the framework's standard format (Decisions made / Constraints established / Open questions deferred / Interface contracts defined / Next session candidates). For WS1.5 sessions specifically:

### 6.1 Required summary block contents per session

| Element | Content |
|---|---|
| Session ID | A.[1-7] |
| Adversarial axis | Per session (or "kickoff"/"synthesis" for A.1/A.7) |
| Findings filed count | Number of FMR/CME/DME/TMA/LBE entries produced this session, broken down by severity |
| Findings dispositioned count | How many received a canonical response from constructive counterpart |
| Tensions surfaced | T-ID list of new tensions logged this session |
| Tensions resolved | T-ID list of tensions resolved this session (including any pre-mapped ones from §6 of governance) |
| Spec sections covered | Specific spec section IDs reviewed |
| Spec sections deferred | Sections in the target register but not yet reviewed (forward-routed to a future session if scope expands) |
| Cumulative WS1.5 progress | "Sessions complete: [list]; remaining: [list]" |

### 6.2 Inter-session register synchronization

After each per-axis session (A.2-A.6), the operator commits the produced register file (e.g., chaos-engineer-fmr-register-v1.md) to the project KB before invoking the next session. This ensures subsequent sessions have access to prior findings for cross-axis cross-reference.

The cumulative-tension-map.md is also updated after each session with new T-ADV-* entries.

### 6.3 Session resequencing handling

If operator resequences A.2-A.6 from the default order (chaos → finops → semantic → pen-test → latency), each session's starter prompt must be regenerated to reference the actual prior sessions completed. The structural template (§5.3) is invariant; only the predecessor reference and prior-register references in the inputs change.

### 6.4 Pause and resume

WS1.5 sessions can be paused and resumed within a single session per the same pattern as WS1 sessions (§9 of skill-design-decisions-adversarial.md governance + general framework practice). The working register and tension map are persistent across pauses; an in-flight session resumes by re-loading those documents.

If a session pauses across days, operator runs a brief re-orientation at resume: paste the original starter prompt + the partial register state + "Resume from [last completed step]".

---

## 7. WS1.5 Closure Criteria and WS3 Entry Authorization

### 7.1 WS1.5 closes on Session A.7 emission of:

1. ws1_5-synthesis-output.md committed to KB
2. workstream-1_5-session-A_7-summary-block.md committed to KB
3. WS1.5 closure verdict assigned (PASS / CONDITIONAL / FAIL)
4. KB update reflecting closure (WS1.5 status block in project instructions changed to "CLOSED [verdict] at [date]")

### 7.2 Closure verdict determines WS3 entry

| WS1.5 closure verdict | WS3 entry status |
|---|---|
| PASS | WS3 implementation planning entry authorized immediately |
| CONDITIONAL | WS3 entry blocked until specific amendments listed in synthesis output close. Amendments are authored in a focused remediation phase (typically 1-3 sessions) before WS3 entry. |
| FAIL | WS3 entry blocked indefinitely. Framework returns to WS1 amendment or re-scoping. WS1.5 may re-run after WS1 amendments. |

### 7.3 WS3 routing of WS1.5 outputs

Even on PASS verdict, WS1.5 produces routing notes that inform WS3:

| Finding class | WS3 routing |
|---|---|
| Critical FMR resolved by amendment | WS3 architecture must accommodate the amended contract |
| Critical CME resolved by accepted tradeoff | WS3 budget plan must reflect the tradeoff (e.g., "we accept N$ per million edits per cumulative-tension-map T-ADV-2-vs-MEMIT") |
| DME findings about edit-rate budgets | WS3 implementation must include monitoring per the proposal |
| TMA findings about Warden contract | WS3 Warden component implementation must close the contract refinement |
| LBE findings about latency budgets | WS3 architecture must include the necessary parallelism or fast-paths |

These routing notes become standing requirements for WS3 implementation planning sessions.

### 7.4 Adversarial team posture post-WS1.5

After WS1.5 closes, the adversarial team is NOT decommissioned. It remains available for:

| Reactivation context | Pattern |
|---|---|
| WS3 milestone reviews | Light-touch single-skill sessions targeting the new component (e.g., "chaos-engineer review of the Transaction Controller implementation") |
| Spec v2 planning | Full reactivation if v2 surfaces new architectural questions |
| Production deployment review | Skills can review deployed implementations against the spec |

Per skill-design-decisions-adversarial.md §9.4, an adversarial skill may be retired if it produced zero findings worth amending across WS1.5. Retirement is documented in the governance doc itself with rationale.

---

## 8. Forward-Routing Convention from WS1.5 to WS3

WS1.5 outputs feed WS3 implementation planning through these formal routing channels:

### 8.1 Amendment-derived requirements

Any spec v1.3 amendment authored in A.7 synthesis produces a corresponding WS3 implementation requirement. These are tracked in a register:

```
ws3-implementation-requirements-from-ws1_5.md:
  REQ-WS3-1 — Component X must implement contract Y per amendment A1.3-1
  REQ-WS3-2 — Component Z must include monitoring per amendment A1.3-2
  ...
```

This register becomes a standing input to WS3 implementation planning sessions.

### 8.2 Tradeoff-derived constraints

Accepted tradeoffs (📋 entries) become explicit operational constraints documented for WS3 implementation:

```
ws3-operational-constraints-from-ws1_5.md:
  CON-WS3-1 — Operator accepts $N/million-edit MEMIT compute cost
              (T-ADV-2-vs-MEMIT) — implementation must surface this
              cost transparently in operational dashboards
  CON-WS3-2 — Operator accepts P95 latency of N seconds for
              Coder→Validator→Write cycle (T-ADV-5-vs-VCA) —
              implementation must not regress below this floor
  ...
```

### 8.3 Deferral-derived v2 backlog

V2 deferrals (🔴 entries) become the v2 backlog:

```
v2-backlog-from-ws1_5.md:
  V2-1 — Defer X to v2 per finding [TMA-N]
  V2-2 — Defer Y to v2 per finding [DME-N]
  ...
```

The v2 backlog informs eventual v2 spec planning but does NOT block v1 WS3.

### 8.4 Routing into existing project artifacts

Amendments authored in A.7 may require updates to existing project documents:

| Document | Update path |
|---|---|
| llm-as-database-v1_2-integrated-spec.md | Becomes v1.3 if amendment cluster is non-trivial; otherwise amendments documented as appendix |
| cumulative-tension-map.md | All resolved tensions marked ✅ Resolved with reference to A.7 disposition |
| cumulative-oq-register.md | OQs that motivated adversarial findings closed or routed to v2 |

---

## 9. Operational Failure Modes During WS1.5

The following failure modes are anticipated and documented for operator readiness.

### 9.1 An adversarial skill produces zero findings

**Symptom.** Session A.X completes with empty register file (no FMR/CME/etc. entries).

**Diagnosis.** Either (a) the spec is genuinely robust on this axis, or (b) the skill failed to engage adversarially.

**Resolution.** Operator inspects the session transcript. If (a), document as a positive finding ("chaos-engineer found no Critical or High failure modes in the reviewed sections"). If (b), re-run with a sharper target spec section list.

### 9.2 A constructive counterpart is unable to provide a canonical response

**Symptom.** Adversarial skill files an FMR; constructive counterpart says "I cannot evaluate this without [X data / Y context]."

**Resolution.** The finding is parked with a `pending_constructive_response` flag. Operator either provides the missing context (and re-engages the constructive skill) or routes to A.7 synthesis with the gap noted.

### 9.3 An adversarial finding contradicts an established Stage 4 POC verdict

**Symptom.** A finding asserts something the POC empirically validated (e.g., "this would catastrophically fail" when Stage 1-4 measured no failure).

**Resolution.** Halt the finding. The constructive counterpart confirms the POC verdict supersedes speculative adversarial claims. The finding may be reframed as "POC validated only at small scale; this finding extrapolates to larger scale" — which is valid.

### 9.4 Session A.7 surfaces a Critical finding that requires returning to an earlier session

**Symptom.** Synthesis reveals that, e.g., a chaos finding has implications for the latency model that A.6 didn't see.

**Resolution.** A.7 pauses; operator runs a focused mini-session re-engaging the affected skill. The mini-session's output joins the synthesis. A.7 resumes.

### 9.5 The WS1.5 closure verdict is contested

**Symptom.** Operator and constructive team disagree on PASS vs CONDITIONAL.

**Resolution.** Operator has final authority per the framework's general decision model. The verdict is recorded with explicit operator rationale if it overrides synthesis recommendations. This becomes a documented operator decision in the WS1.5 summary record.

---

## 10. Closure of This Document

This master plan seals at v1.0 upon operator review at WS1.5 entry. It is authored ahead of WS1.5 entry to capture the design while context is fresh; revisions occur only if WS1.5 entry circumstances differ materially from anticipated (e.g., Stage 4 verdict was CONDITIONAL with specific gating amendments, or fewer than 5 adversarial skills were authored).

Subsequent versions follow standard semver: minor versions for refinements within an existing WS1.5 phase structure (e.g., adjusting per-session estimated wall times based on actual WS1.5 experience); major versions for phase-structure changes (e.g., expanding from 7 sessions to 9, or compressing to 5).

This document does NOT prescribe WS3 structure. WS3 has its own master plan, authored at WS3 entry (after WS1.5 closure) with full benefit of WS1.5 outputs as input.

---

## 11. Reference Documents

| Document | Relationship to this master plan |
|---|---|
| skill-design-decisions-adversarial.md | Governs the adversarial team; pre-mapped tensions; skill modification rules |
| skill-design-decisions.md | Governs the constructive team; council session conventions |
| adversarial-skills-starter-descriptions-v2.md | Starter prompts for authoring the 5 skills + framework-council extension |
| llm-as-database-v1_2-integrated-spec.md | Subject of WS1.5 adversarial review |
| stage-4-poc-packet.md | WS1 closure context (authored at WS1 closure, not yet existing at this document's authoring time) |
| cumulative-oq-register.md | OQ context (authored at WS1 closure) |
| cumulative-tension-map.md | Tension structure (synthesized at WS1 closure) |

End of document.
