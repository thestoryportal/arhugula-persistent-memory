# LLM as Database: Agent Harness Architecture
## Skill Friction Log v1.0 — aiSecOps-specialist

> **Scope:** Post-session friction analysis for `aiSecOps-specialist` (The Warden)
> **Session analyzed:** Session 3 — Threat Modeling: Write Layer Access Control
> **Evidence sources:**
> - `transcript-session-3-security.md` (full session transcript)
> - `threat-modeling-write-layer-access-control.md` (session summary)
> - `gap-backlog-v1.md` (19 gaps extracted from the integrated spec)
> - `tension-map-v1.md` (12 tensions from Session 7 cross-domain synthesis)
> - `skill-design-decisions.md` (ownership boundaries and pre-mapped tensions)
> - `/mnt/skills/user/aisecops-specialist/SKILL.md` (skill definition)
>
> **Method:** Evidence-first. Friction entries are only raised where (a) a specific failure is
> directly traceable in the session transcript, or (b) a gap or tension document explicitly
> identifies Session 3 as the point of origin and the Warden's domain as the responsible
> owner. No friction is invented from general inference.
>
> **Total entries:** 12 (5 High confidence, 7 Medium confidence)
> **Entry format:** SKILL-FRICTION-[N] per `framework-spec-writer` SKILL.md conventions

---

## Friction Entries — High Confidence

---

### SKILL-FRICTION-1

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Format Failure
Evidence:   SKILL.md §Operating Mode, Phase 1; session transcript structure (lines 22–56).
            The transcript shows the skill moved from the user's invocation directly to
            "Session 3 — AISecOps Specialist: The Warden / Scope: Write layer threat
            model…" with zero probing questions. Phase 1 of the skill definition is:
            "Before producing spec output, ask probing questions to map the trust surface."
            Six named questions are listed. None were asked.
Description: The Socratic Inquiry phase was entirely bypassed. The user's directive
             "Start with the threat model" was treated as an instruction to skip Phase 1
             entirely. The Phase 1 questions exist because they surface attack surface
             information that shapes every subsequent spec block — specifically, questions
             about how many agents have write authority, whether humans are in the loop,
             and where .vindex files live outside the harness. Without answers to these,
             the threat model must either assume or leave gaps. In Session 3, the skill
             assumed answers (the agent roster was inferred from prior session docs) rather
             than confirming them. This is architecturally acceptable in this case because
             Sessions 1 and 2 documents were uploaded and the context was rich. However,
             the Phase 1 bypass also meant no probing questions were surfaced as open
             questions in the session summary — which would have been the appropriate
             compensating behavior when inquiry is skipped by user direction.
Confidence: High — directly evidenced by transcript structure.
Proposed fix: Add a Phase 1 bypass protocol to SKILL.md: "If the user explicitly bypasses
              inquiry (e.g., 'start with the threat model'), do not silently skip Phase 1.
              Instead, (a) note in the session preamble that inquiry is being bypassed per
              user direction, (b) log each unanswered Phase 1 question as an OQ-S[N] item
              in the session summary's Open Questions section, and (c) mark each as
              'not yet confirmed — assumed from prior session documents' or equivalent.
              A skipped question is a deferred question, not a closed one."
```

---

### SKILL-FRICTION-2

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Question
Evidence:   D27 in session transcript (line 299): "expires after 30 minutes" — no analysis
            of whether 30 minutes is achievable for a Genesis compile of up to 10,000 edges
            internally sub-batched at 2,000. TENSION-T7 in tension-map-v1.md (lines 246–276)
            directly documents the revision: "a large Genesis patch running on GPU could
            easily exceed 30 minutes. A TTL expiry mid-compile produces an indeterminate
            state." T7 required Session 7 to change the model to admission-time TTL (10 min
            at admission, then compile proceeds independent of token state).
Description: The schema migration authorization token's 30-minute TTL was specced as
             a fixed expiration window without the Warden asking: "Is this window achievable
             given the maximum expected Genesis compile duration?" The MEMIT Specialist had
             already specced (by Session 2) a 10,000-edge hard cap with internal 2,000-edge
             sub-batching. The Warden had access to these figures via the uploaded Session 2
             document but did not interrogate whether a 10,000-edge MEMIT compile can
             complete in 30 minutes. This created a latent timing conflict that was only
             caught when the State Consistency Theorist examined the 2PC interaction in
             Session 5 and escalated it to the full council in Session 7 (T7). The Warden
             should have asked this question or flagged it as input required from the
             MEMIT Specialist before finalizing D27.
Confidence: High — D27 is directly in the transcript; T7 directly traces to D27 and
            documents the corrective action required.
Proposed fix: Add to SKILL.md §Useful Framing Questions: "Is the schema migration
              authorization token's TTL achievable given the maximum expected Genesis compile
              duration? What is the largest `.larql` patch the Architect Agent is expected to
              produce, and has the MEMIT Specialist confirmed a compile-time estimate for that
              patch size? A TTL that expires mid-compile creates an indeterminate 2PC state
              that the State Consistency Theorist must resolve." Also add to the Spec Output
              Checklist: "[ ] Schema migration token TTL cross-checked against MEMIT
              Specialist's compile-time estimate for maximum Architect Agent patch size."
```

---

### SKILL-FRICTION-3

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Tension Attribution
Evidence:   TENSION-T11 in tension-map-v1.md (lines 384–420): "The Warden had specced a
            separate, cryptographically immutable audit trail (D28) as a security artifact.
            The State Consistency Theorist had separately specced a State Ledger…These were
            two append-only Merkle-chain integrity logs doing substantially overlapping work."
            Pre-T4 in skill-design-decisions.md (line 108): "Audit completeness vs. write
            throughput — Warden vs. State Consistency Theorist + MEMIT Specialist" is a
            pre-mapped structural tension baked into the skill team. Session 3's IC15 defines
            "Write Engine → Audit Log" but produces no interface contract between the Audit
            Log and the State Ledger.
Description: T11 was a foreseeable tension. Pre-T4 in the skill team's pre-mapped tension
             list identifies "Audit completeness vs. write throughput — Warden vs. State
             Consistency Theorist + MEMIT Specialist" as a structural conflict to be expected.
             The Warden specced the audit trail as a complete, standalone, append-only
             Merkle-chain artifact in Session 3 — which is exactly the description of the
             State Ledger that would be specced in Session 5. By not asking "How does this
             audit trail interact with the State Ledger the State Consistency Theorist will
             spec?" and not producing an interface contract between the two, the Warden left
             a structural overlap that required a Session 7 architectural merge. The SKILL.md
             Spec Output Checklist explicitly says "Interface contracts with MEMIT Specialist,
             Validation layer, and State Ledger defined" — the State Ledger contract was not
             produced. This is the most consequential tension the skill was positioned to
             pre-empt and did not.
Confidence: High — T11 body text explicitly names D28 as the source of the conflict;
            Pre-T4 is documented in skill-design-decisions.md as a pre-mapped tension the
            skill team was expected to hold.
Proposed fix: Add to SKILL.md §Operating Mode, Phase 2 under Spec Synthesis: "Before
              finalizing the audit trail spec block, produce a preliminary interface contract
              between the Audit Trail and the State Ledger, even if the State Consistency
              Theorist has not yet run. The preliminary contract should declare: (a) which
              events are audit-trail-owned vs. ledger-owned, (b) whether the audit trail and
              ledger are the same artifact or separate artifacts, and (c) what the storage
              delineation is. Mark this contract 'REQUIRES STATE CONSISTENCY INPUT in
              Session 5.' Producing a stub contract prevents a parallel-spec duplication
              in Session 5 from going undetected until Session 7."
```

---

### SKILL-FRICTION-4

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   D28 in session transcript (line 451): "Audit trail is a mandatory, append-only
            security artifact. Canonical record format defined (12 required fields). Stored
            outside .vindex layer." The Audit Trail spec block (lines 326–370) defines 12
            fields and retention policy but specifies storage only as "outside the .vindex
            layer" and "separate from the State Ledger." No storage format (JSONL vs. DB),
            no file path, and no integrity mechanism for the audit trail itself is specified.
            TENSION-T11 traces the Session 7 merge requirement directly to this gap: the
            Unified Ledger resolution mandates "one append-only JSONL file at
            <harness_root>/.state-ledger/ledger.jsonl" with Merkle-chain-lite integrity —
            architecture that had to be invented in Session 7 because Session 3 left storage
            unspecified.
Description: The audit trail spec block defines what to record (12-field canonical format)
             and how long to retain it (project lifetime; indefinite for integrity violations)
             but does not specify where or in what format. "Stored outside the .vindex layer"
             is a security boundary description, not a storage spec. The absence of a
             format and path meant the State Consistency Theorist in Session 5 independently
             specced a Merkle-chain JSONL State Ledger with identical architectural
             properties, producing the T11 duplication. Had the Warden specced a concrete
             storage architecture (even as a placeholder: "append-only JSONL file at a
             harness-root path, with Merkle-chain-lite integrity, outside Git and outside
             .vindex"), the State Consistency Theorist would have had a surface to interface
             with rather than a second independent implementation.
Confidence: High — T11 directly traces the need for the Unified Ledger to the gap between
            D28's abstract "stored outside .vindex" and a concrete storage architecture.
Proposed fix: Add to SKILL.md §Audit Trail Requirements: "The audit trail spec block MUST
              specify: (a) storage format (append-only JSONL strongly recommended for
              portability and queryability; alternatives require explicit rationale), (b) file
              system location relative to harness root — outside both Git and .vindex,
              (c) integrity mechanism for the audit trail file itself (not just the records
              within it), and (d) whether this is a standalone file or shares infrastructure
              with the State Ledger. If storage architecture cannot be resolved in this
              session, produce an OQ-S[N] item explicitly requesting State Consistency
              Theorist input on storage design in Session 5."
```

---

### SKILL-FRICTION-5

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   C17 in session transcript (line 76): "Write Scope Definitions are not modifiable
            by any agent at runtime. Scope changes require out-of-band human review event."
            Write Scope Definitions spec block (lines 213–268): "Scope definitions are
            security artifacts. They must be versioned, signed, and stored outside the
            harness's mutable layer." No storage path, file format, or governance mechanism
            is specified beyond "outside mutable layer." TENSION-T4 in tension-map-v1.md
            (lines 136–170) documents the resulting conflict: "Write Scope Definitions
            (Warden's domain) needed to be agent-runtime-immutable but operator-updatable"
            was one of four patterns from three sessions that each had "no unified governance
            model." T4's resolution required creating the three-tier .harness/ model
            (Tier 1 immutable anchor, Tier 2 sealed artifacts, Tier 3 anchored Git config)
            in Session 7.
Description: The Write Scope Definitions spec block correctly identifies that scope
             definitions are security artifacts and must be versioned, signed, and stored
             outside the mutable layer. However, it does not specify *where* they are stored
             or *how* the version-locking and signing are implemented. This left the storage
             question open for every session that followed. When the State Consistency
             Theorist (Session 5) specced Git-committed anchored artifacts, and the
             Orchestration Comparativist (Session 6) specced agent YAML as Git-committed
             operational config, there was no Warden-supplied storage contract to resolve
             against — leading to T4's fragmented governance pattern. Speccing "stored in
             a Warden-managed, operator-signed, versioned directory at .harness/
             write-scope-definitions/" in Session 3 would have given subsequent specialists
             a concrete target.
Confidence: High — T4 body text explicitly names Write Scope Definitions as one of the
            four fragmented storage patterns that required the Session 7 resolution.
Proposed fix: Add to SKILL.md §Write Scope Design: "Write Scope Definition storage must
              be specified to the level of: (a) physical location (named path relative to
              harness root, outside .vindex and outside agent process write permissions),
              (b) governance format (versioned directory, operator-signed manifest, or
              equivalent), (c) integrity mechanism (hash-sealed at version creation),
              and (d) update ceremony requirements (what constitutes a signed update event).
              'Stored outside the mutable layer' is a security boundary description, not
              a storage spec. A storage spec is required before this block is complete."
```

---

## Friction Entries — Medium Confidence

---

### SKILL-FRICTION-6

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Cross-Domain Implication
Evidence:   OQ-S2 in session summary (line 108): "Token revocation mechanism for
            compromised agent identity mid-session. → Needs operational spec before
            production deployment." No session routing, no cross-domain flag, no interface
            contract stub. TENSION-T5 in tension-map-v1.md (lines 174–208) documents the
            resulting Session 7 architecture: agent suspension model, governance-state
            binding (tokens carry hash-bindings to Write Scope Definition and Agent YAML),
            Orchestrator signing key dual-store. T5 is framed as "Warden vs. Orchestration
            Comparativist" — a conflict that required both specialists to resolve.
Description: OQ-S2 was recognized as open in Session 3 but routed as a generic operational
             deferral rather than as a cross-domain interface question requiring Orchestration
             Comparativist input. Token revocation mid-session is not purely operational: it
             requires the Orchestrator to maintain an in-memory suspended-agents set, which
             is an architectural decision. The Warden should have routed OQ-S2 explicitly to
             "INPUT REQUIRED: Session 6 (Orchestration)" and produced a preliminary interface
             contract stub: "Gate ← Orchestrator: revocation signal for suspended agent.
             Behavior: Gate rejects all tokens from suspended agent regardless of TTL state."
             Without this routing, T5 had to be surfaced from scratch in Session 7, requiring
             significant architecture (the suspension model, governance-state binding, and
             dual-store key anchor) to be worked out under cross-domain conflict rather than
             planned ahead.
Confidence: Medium — T5 directly traces to OQ-S2, but some of T5's resolution required
            Orchestration input that could not have been fully anticipated in Session 3.
Proposed fix: Add to SKILL.md §Key Risks: "Token revocation is not an operational concern
              alone — it has direct Orchestration implications. If an agent's token is
              revoked, the Orchestrator must define: (a) does suspension take effect
              immediately or at the next token presentation?, (b) what happens to an
              operation that is mid-2PC when suspension is declared?, and (c) how does
              the Gate receive the suspension signal? Any OQ regarding token revocation
              must be routed explicitly to Session 6 (Orchestration Comparativist) with
              an interface contract stub defining the revocation signal and Gate behavior."
```

---

### SKILL-FRICTION-7

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Tension Attribution
Evidence:   TENSION-T4 in tension-map-v1.md (lines 136–170): the four fragmented storage
            patterns included "The Warden specced a permanently immutable Genesis seal
            (D49, dual-store), [and] the State Consistency Theorist specced path-
            classification as an anchored Git artifact (D76)." Upstream cause: neither
            the Warden in Session 3 nor the other specialists in Sessions 4–6 asked
            how their respective storage governance patterns would be unified. Pre-T5 in
            skill-design-decisions.md (line 109): "Schema stability vs. agent autonomy in
            patch generation" is listed as a pre-mapped structural tension, which has a
            configuration governance dimension that the Warden should have surfaced.
Description: T4 (Configuration Authority Fragmentation) was not foreseeable in full — it
             required Session 5 and 6 outputs to materialize. However, the Warden in Session
             3 specced the Genesis seal and Write Scope Definitions without asking: "How
             will these storage artifacts be governed alongside other harness configuration?"
             A Warden operating with cross-domain awareness would have recognized that
             immutable anchor artifacts, versioned operational config, and agent-runtime
             security artifacts are three different governance tiers and would have produced
             a preliminary note flagging this as an open cross-domain question — even without
             knowing Session 5's or Session 6's specific outputs. The Warden's pre-mapped
             role as "trust boundary owner across all components" implies awareness that
             configuration governance is a trust question, not just an operational one.
Confidence: Medium — T4 required multi-session input to fully materialize; the Warden
            could not have produced T4's resolution alone, but could have pre-surfaced
            the structural conflict.
Proposed fix: Add to SKILL.md §Operating Mode, Phase 2: "Before finalizing any spec block
              that establishes a new storage artifact (seal, scope definition, audit trail,
              configuration file), flag it with a cross-domain note: 'Storage governance
              for this artifact must be unified with all other harness configuration
              artifacts in a Session 5–6 synthesis. Preliminary storage pattern: [type].
              Routing: State Consistency Theorist (Session 5) and Orchestration
              Comparativist (Session 6) must confirm that this pattern is compatible with
              the broader harness configuration governance model.'"
```

---

### SKILL-FRICTION-8

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Backlog Attribution
Evidence:   GAP-3 in gap-backlog-v1.md (lines 99–137): "The spec notes [the .larql format
            version mismatch concern] because the `.larql` format is the interface through
            which all agents author writes. A version mismatch between an agent's
            YAML-defined expectations and the current schema is not currently covered by
            the Gate's pre-checks (§10.2 lists seven pre-checks; schema version is not
            among them). Security note (Warden): If the Gate's pre-check list does not
            include a schema version check, an attacker who can replay a patch authored
            under an older schema version might bypass Validator checks added in the newer
            version." The security note in GAP-3 is attributed to the Warden but was
            produced by the council in Session 7, not by the Warden in Session 3. The
            Patch Authorization Gate spec block (lines 157–209) lists three checks
            (Identity, Scope, Integrity) with no mention of schema version verification.
Description: Schema version verification of .larql patches is a Gate concern with a
             direct security implication: a patch authored under a prior schema version
             could bypass Validator checks added to newer versions — a replay-variant attack.
             The Warden's SKILL.md Spec Output Checklist includes "Prompt injection vector
             analysis complete for write-authorized agents" and "Threat model completed for
             all five primary threats." Schema version replay falls within the spirit of
             Threat 2 (supply chain attack via tampered patch) and the prompt injection
             vector concern. GAP-3 is rated Critical (blocks 3+ other gaps) and required
             the council to add the Warden's security note in Session 7. This note should
             have been a Session 3 output, either as a Gate pre-check or as an OQ-S[N]
             item. The gap is attributable to the Warden because the Gate pre-check list
             is exclusively the Warden's spec domain.
Confidence: Medium — GAP-3's security note is attributed to "Warden" in the gap backlog
            but was produced in Session 7, not Session 3, confirming a Session 3 miss.
Proposed fix: Add to SKILL.md §Patch Authorization Gate (or the five primary threats
              section): "Threat 6 (Schema Version Replay): A patch authored under an older
              .larql schema version may bypass Validator checks added in newer versions if
              the Gate does not verify schema version compliance. The Gate pre-check list
              MUST include a schema version check OR an explicit OQ-S[N] must be produced
              noting that .larql schema versioning is required before the Gate pre-check
              list can be finalized." Add to the Spec Output Checklist: "[ ] Gate
              pre-check list addresses .larql schema version verification or explicitly
              defers it as a named open question."
```

---

### SKILL-FRICTION-9

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Backlog Attribution
Evidence:   OQ-S4 in session summary (line 118): "Scope version management across long-
            running projects where agent capabilities evolve. → Operational concern;
            deferred to orchestration session." GAP-5 in gap-backlog-v1.md (lines 177–207),
            rated 🟠 High priority: "The Write Scope Definition update ceremony for
            long-running projects is only partially addressed (OQ-S4, §18.2). What is not
            defined is the behavior when a scope update occurs while there are active
            in-flight invocation tokens or open Write Locks." GAP-5 blocks: complete token
            lifecycle spec and long-running project governance spec.
Description: OQ-S4 was classified as an "operational concern" and deferred to the
             Orchestration session. GAP-5 shows this classification was incorrect: scope
             version management during in-flight operations is a security-bearing question
             because a scope update mid-flight creates a window where the agent briefly
             operates under either more or less authority than intended (the old token carries
             the old scope hash; the Gate will reject it as an "infrastructure failure" and
             re-issue — but the agent's in-progress work was authorized under the old scope).
             This is not an operational edge case; it is a trust boundary condition the
             Warden must characterize. Routing it to "orchestration" without flagging its
             security implications meant the Orchestration session addressed it as a
             scheduling concern rather than a trust scope concern, leaving GAP-5 open.
Confidence: Medium — GAP-5 is directly traceable to OQ-S4's misclassification;
            inferred from gap backlog rather than directly evidenced in transcript text.
Proposed fix: Revise §Key Risks in SKILL.md: "Scope changes during live operations are
              a security event, not an operational configuration update. Add to the Key
              Risks list: 'Scope update during in-flight operation: if a Write Scope
              Definition is updated while an agent holds an active token within its TTL
              window, the Gate will reject the token. This creates a window where the
              agent has started work under a scope that is no longer active. The Warden
              must spec: (a) whether the Orchestrator must drain in-flight operations
              before accepting a scope update, (b) whether the agent's partially-completed
              work is rolled back or held pending re-authorization, and (c) what Ledger
              entry is produced for a scope-update token rejection.' Any OQ about scope
              version management must be routed to Orchestration AND flagged as requiring
              Warden input on the security boundary."
```

---

### SKILL-FRICTION-10

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Question
Evidence:   The five-threat model in the transcript (lines 100–150) covers: Unauthorized
            Write (Threat 1), Patch Injection (Threat 2), Prompt Injection via Knowledge
            Poisoning (Threat 3), Cascading Corruption (Threat 4), Rollback Evasion
            (Threat 5). No threat covers human or external-tool Git commits outside the
            harness pipeline. TENSION-T10 in tension-map-v1.md (lines 349–380): "Out-of-
            Band Git Commit Handling — State Consistency Theorist vs. Warden. The Warden
            could not allow auto-compilation of catch-up patches generated from
            unauthenticated state changes; every write to the parametric layer requires
            human-authorized, Validator-verified content." T10 is framed as a Warden
            concern that required the Warden's participation to resolve but was not
            surfaced until Session 7.
Description: The Warden's threat model covers agent-originating threats and supply-chain
             attacks on agent-generated patches. It does not cover a sixth attack class:
             an external actor (human with repo access, CI system, automated script) writing
             to the Git repository outside the harness pipeline. This creates an unauthenticated
             state change: the Git layer has facts the parametric layer does not, and the
             harness has no record of who authorized the change. T10 required the Warden
             to rule that "no auto-compilation of catch-up patches from unauthenticated state
             changes" — a position that is clearly within the Warden's domain and could have
             been established as Threat 6 in Session 3. Instead, the State Consistency
             Theorist detected the issue when speccing reconciliation and had to escalate it
             as a cross-domain conflict.
Confidence: Medium — T10 is documented as a Warden-relevant conflict in Session 7, but
            it emerged from State Consistency session work, not from a direct Session 3
            evidence trail.
Proposed fix: Add to SKILL.md §Threat Model: "Threat 6 — Out-of-Band State Injection
              (Git Write Outside Harness): A human operator, CI system, or external tool
              commits directly to the project's Git repository without using the harness
              pipeline. The commit changes code state without a corresponding .larql patch
              or Ledger entry. If the harness detects this and auto-generates a catch-up
              patch, it is executing an unauthorized parametric write (no agent token, no
              Gate check, no Validator review). Defense: Out-of-band Git commits MUST
              NOT trigger automatic parametric writes. Catch-up patches generated from
              out-of-band commits require explicit human review and the standard
              authorization pipeline before reaching the write engine. The Warden must
              produce an OQ-S[N] for this threat class if the State Consistency Theorist
              has not yet specced reconciliation behavior."
```

---

### SKILL-FRICTION-11

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Cross-Domain Implication
Evidence:   TENSION-T3 in tension-map-v1.md (lines 103–130): "Meta-* Audit Completeness
            vs. Corpus Integrity — Warden vs. Validation Contract Architect. The Warden
            needed complete audit visibility into Meta-Validator and Meta-TGA health
            monitoring behavior — specifically, the ability to audit individual test case
            outcomes, not just aggregate health scores." The Session 3 Audit Trail spec
            block (lines 326–370) defines 12 mandatory fields covering write events and
            gate rejections. It does not mention periodic health monitoring events
            (Meta-Validator runs, behavioral probes, Meta-TGA runs). The per-case audit
            requirement for Meta-* runs was a Warden requirement that first appeared in
            Session 7.
Description: The audit trail spec in Session 3 correctly addressed write events and
             gate rejections. It did not address whether health monitoring events —
             Meta-Validator runs, behavioral probes, Meta-TGA health score computations —
             are auditable events. This left a gap that only became visible in Session 7
             when the Warden needed per-case (not aggregate-only) audit records from
             Meta-* runs for forensic purposes. Had the Warden asked in Session 3 "What
             does the audit trail look like for periodic health monitoring runs?", this
             requirement would have been surfaced before the Validation Contract Architect
             specced the Meta-Validator mechanism in Session 4. Instead, T3 required a
             Session 7 negotiation to add per-case audit reporting as a requirement on
             top of an already-specced health monitoring system.
Confidence: Medium — T3 directly documents the Warden's per-case audit requirement;
            the absence from Session 3's audit spec is inferred from the audit trail
            block's 12-field format, which covers only write events.
Proposed fix: Add to SKILL.md §Audit Trail Requirements: "The audit trail specification
              MUST address not only write events and gate rejections, but also periodic
              health monitoring events. Specifically: any system component that runs
              periodic behavioral verification (Meta-Validator, behavioral probe, Meta-TGA,
              or equivalent) is a security-auditable event. The Warden must specify: (a)
              whether health monitoring run results are per-case records or aggregate-only,
              (b) whether a health monitoring run that produces only an aggregate score
              satisfies the Warden's forensic investigation requirements, and (c) where
              health monitoring audit records are stored. Aggregate-only health scores
              prevent forensic investigation of individual test case failures."
```

---

### SKILL-FRICTION-12

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   Genesis Bootstrapping Security spec block (lines 277–323): Step 1 describes
            a human reviewer inspecting the Architect Agent's output patch. Step 2 describes
            the schema migration authorization token. Step 3 describes the post-Genesis
            snapshot seal. No step or sub-clause describes what happens if the human
            reviewer rejects the patch at Step 1. The error path (re-invoke Architect Agent?
            halt project initialization? log rejection as security event?) is entirely
            absent. No OQ-S[N] item covers it.
Description: The Genesis Security Protocol specced the happy path (human reviews → approves
             → token issued → compile proceeds → snapshot sealed) but contains no error
             path specification. If the human reviewer at Step 1 determines the patch is
             corrupted, includes injected facts, or is otherwise unacceptable, the protocol
             provides no guidance on: (a) what system state the harness is in at the point
             of rejection (Genesis not yet started — clean; or has something already been
             written?), (b) whether the Architect Agent is re-invoked and with what
             correction context, (c) whether the rejected patch hash is logged as a
             security event in the audit trail, and (d) how many rejection cycles are
             permitted before the Genesis process is abandoned and escalated. For the
             highest-risk operation in the entire harness (the Warden's own characterization),
             the error path omission is significant. This likely requires low effort to
             address but was not flagged as an open question.
Confidence: Medium — directly evidenced by the absence of error-path language in the
            spec block; impact inferred from the block's own statement that Genesis
            bootstrapping is "the most critical security moment in the entire harness
            lifecycle."
Proposed fix: Add to SKILL.md §Genesis Security Protocol template: "For every step in
              the Genesis Security Protocol, an error path MUST be specified alongside
              the happy path. Step 1 error path minimum requirements: (a) state of the
              system on rejection (was anything written? Is a cleanup required?), (b)
              re-invocation protocol for the Architect Agent (what correction context is
              provided?), (c) whether the rejected patch hash is logged as a security
              incident, (d) maximum number of rejection-and-retry cycles before escalation
              to human halt decision. If any of these cannot be resolved in the session,
              produce an OQ-S[N] item explicitly deferring the error path design."
```

---

## Proposed SKILL.md Changes — Summary

The following changes to `/mnt/skills/user/aisecops-specialist/SKILL.md` are proposed based on
the 12 friction entries above. Each change is scoped to the minimum modification that prevents
the specific documented friction without altering the skill's ownership scope, voice, or
pre-mapped tension responsibilities (per `skill-design-decisions.md` §Skill Modification Rules).

| Entry | Section to modify | Change type |
|-------|------------------|-------------|
| SF-1 | §Operating Mode, Phase 1 | Add Phase 1 bypass protocol with OQ logging requirement |
| SF-2 | §Useful Framing Questions + Spec Output Checklist | Add TTL feasibility question and MEMIT cross-check item |
| SF-3 | §Operating Mode, Phase 2 | Add stub interface contract requirement for audit trail ↔ State Ledger |
| SF-4 | §Audit Trail Requirements | Add storage format, file path, and integrity mechanism as required fields |
| SF-5 | §Write Scope Design | Add storage path and governance mechanism as required spec fields |
| SF-6 | §Key Risks | Add token revocation as Orchestration-routing cross-domain risk |
| SF-7 | §Operating Mode, Phase 2 | Add storage governance cross-domain note for all new storage artifacts |
| SF-8 | §Patch Authorization Gate (new threat) + Spec Output Checklist | Add Threat 6 (schema version replay) and Gate pre-check item |
| SF-9 | §Key Risks | Add scope update during in-flight operation as security-bearing concern |
| SF-10 | §Threat Model | Add Threat 6 (out-of-band Git write) as a named attack class |
| SF-11 | §Audit Trail Requirements | Add health monitoring event audit coverage as a required spec topic |
| SF-12 | §Genesis Security Protocol template | Add error path specification as mandatory alongside happy path |

**Before implementing:** per `skill-design-decisions.md` §Skill Modification Rules, all
changes must be documented in `skill-refinement-log-v1.md` with rationale before reinstalling.
Changes SF-3, SF-8, and SF-10 touch interface contract definitions and require a council
interface contract review after modification.

---

## Performance Pattern Summary

The `aiSecOps-specialist` skill performed strongly within its core domain. The threat model was
thorough, concrete, and well-grounded in the specific harness architecture. The Patch
Authorization Gate, Write Scope Definitions, Genesis Security Protocol, and Audit Trail spec
blocks were all substantially correct and required no architectural revision in Sessions 4–6.
The session's interface contracts (IC10–IC16) were consistently well-formed and consumed
without conflict by downstream sessions. The skill's systematic weakness is not what it
produces within its domain — it is what it fails to flag at the domain's edges. Specifically,
the skill consistently under-specifies the physical storage architecture of the security
artifacts it introduces (audit trail, Write Scope Definitions, Genesis seal) — producing
ownership claims ("stored outside mutable layer") without storage contracts, which left
Sessions 5–7 to discover fragmented governance patterns. Equally, the skill treats several
cross-domain questions (token revocation, scope version management, out-of-band Git writes)
as operational deferrals rather than routing them explicitly to the sessions that need to
answer them — a pattern that caused multiple tensions to surface in Session 7 rather than
being pre-empted during their originating sessions. The skill knows its boundaries but does
not reliably pass information across them.

---

*Skill Friction Log v1.0 — 12 entries across 6 friction types*
*5 High confidence (directly evidenced in transcript)*
*7 Medium confidence (inferred from gap backlog or tension map)*
*Proposed fixes: 12 SKILL.md changes identified, all within existing ownership scope*
*Modification prerequisites: `skill-refinement-log-v1.md` entry required before reinstall*
*Council IC review required for: SF-3, SF-8, SF-10*
