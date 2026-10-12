# v2 Spec Synthesis — Opening Prompt
## Step 3.1: Compile the v2 Integrated Spec

**Model:** Opus 4.6 | **Web Search:** ✗ | **Deep Research:** ✗
**Skill:** `framework-council`

---

```
Full Council — v2 Spec Synthesis.

You are operating inside the LLM as Database: Agent Harness Architecture
specification project. The KB contains all reference documents. This session
produces the v2 integrated spec document: `llm-as-database-v1_2-integrated-spec.md`

─── BASELINE ────────────────────────────────────────────────────────────────

The active spec baseline is `llm-as-database-v1_1-integrated-spec.md`. This
document is the v1.1 spec. The v2 spec supersedes it — do not produce an
appendix or patch document. Produce a complete, self-contained integrated
spec where every section reflects the current resolved state.

─── RESOLUTION RECORD ───────────────────────────────────────────────────────

The authoritative record of all decisions made since v1.1 is:

  gap-backlog-v5.md   — all 60 gaps with resolution status and session refs
  tension-map-v5.md   — all 25 tensions with current status

Use these as the canonical reference for what has been resolved and what
remains open or deferred. Where the backlog cites a session for a spec block
(e.g., "IC-SCOPE-RECONCILE from GS5 v3"), the full spec block is in the
corresponding session summary in the KB. Pull from those summaries when
assembling section content.

─── AMENDMENT OBLIGATIONS ───────────────────────────────────────────────────

The following amendments were ratified and are outstanding in v1.1 — they
must be applied in the v2 spec:

A1-REVISED  §11.8.1  TC compensation bounded to reversal-only (C-CRC-3)
A2-GS2      §11.8.1  Precondition check error handling; CIRCUIT_RESET_REJECTED
A3          IC-TC-RESET  CeremonyToken / CAK authorization for circuit reset
A4          §14.3    SCOPE_HASH_MISMATCH threshold 3 → 2; SCOPE_MISMATCH_ESCALATED
A5          §10.9    Ceremony authorization verification against CAK before SCOPE_UPDATED
A6          §10.9    Rate limit check precedes signature verification
A7          Appendix C  GS3 batch Ledger entry additions
A7b         Appendix C  GS4 CeremonyToken-model entries; deprecated-entry markers
A8          Appendix C  Circuit breaker cross-category rationale annotation
A9          IC-MANIFEST-1  ceremony_token_id replaces ratification_signature
A10         §13.2    ceremony_authorization_key_anchor in genesis-seal.json
A11         Deployment guidance  v1 CAK backup custodian clarification
A12         §11.8.1 IC-TC-RESET  Genesis-trip Hold-release precondition branch
A12-IC-CORPUS-AUTH  expires_at predicate at submission ingress
A13-IC-SL7  contains_expired_author_cases response field
A14-Appendix-C  CONSTITUTIONAL_FAILURE field pair (invariant_statement +
              failure_assertion_message)

─── MAJOR STRUCTURAL ADDITIONS ──────────────────────────────────────────────

The following components exist in session summaries and gap session outputs
but are not yet in v1.1. Each requires a new or substantially rewritten
section in v2:

§10.9.1   Scope Registry Reconciliation on Orchestrator Restart (GAP-25 / GS5 v3)
§10.9.2   Scope Propagation Bound — 5-second ceiling; DIVERGED_STATE trigger
§11.8.1.1 Bounded Compensation Under READ_ONLY (A1-REVISED)
§11.8.1.2 Reset Ceremony Under Orchestrator Degradation (GAP-24 / GS5 v3)
§11.8     State machine addenda: BURST_SUSPENDED state (GAP-41 / GS10);
          TRUST_ROOT_LOST terminal state (GAP-42 / GS10) — transition rules
§13.2     ceremony_authorization_key_anchor (A10); corpus_author_bootstrap_identity
          replacing corpus_author_identities (GAP-8 / GS8 v3)
§13.3     corpus-author-registry/ (Tier 2, sixth sealed corpus — GAP-8 / GS8 v3);
          hook-registry/v1 (Tier 2, seventh sealed corpus — GAP-54 / GS11)
§13.5     Boot-time verification step 3a: CAK anchor semantic verification
          (GS5 v3 — note: GS5 v3 calls these D99/D100 locally; see D-number collision
          warning above); RATE_LIMIT_RETENTION_CONFLICT boot check (GAP-46 / GS11)
§14.3     Aggregate SCOPE_HASH_MISMATCH detection (GAP-38 / GS12);
          scope_mismatch_aggregate_threshold_n + _window_seconds (Tier 1)
§16.2     W3 scope consolidation: C-W3-1 two-admission-criteria policy (GAP-29b / GS10);
          IC-W3-POLICY-1; three ratified W3 carve-outs beyond INTEGRITY_VIOLATION_EMERGENCY
§16.4     §16.4 documentation: entry-count bounds for full verification (GAP-53 / GS11)
New §     Ceremony Authorization — IC-SCOPE-AUTH-1: the unified ceremony authorization
          umbrella covering all four ceremony types (MANIFEST_RATIFICATION, HOLD_RELEASE,
          SCOPE_UPDATE, CIRCUIT_RESET) via CeremonyToken envelope. Full interface contract
          is in v2 GS4 summary (now in KB). This section is NOT in v1.1 — v1.1 has only
          the older IC-SCOPE-UPDATE single-ceremony model. Pull the full IC-SCOPE-AUTH-1
          spec block, including ceremony_type discriminator, CAK verification requirement,
          replay rejection logic, and failure behavior, from v2 GS4 summary.
New §     CAK bootstrap tool model: IC-BOOT-1, dual-root signing, C-BOOT-5 (GAP-40 / GS10)
New §     Per-CAK burst limit: N=5/10min, BURST_SUSPENDED, IC-CAKB-1 (GAP-41 / GS10)
New §     Break-glass emergency channel: second Tier 1 anchor, M≥3 quorum,
          TRUST_ROOT_LOST, IC-BG-1, OQ-S-CAK-1 partially addressed (GAP-42 / GS10)
New §     larql_fidelity_calibration protocol: per-transform-class measurement of ε
          coefficient, calibration run structure, output record format with
          calibrated_against_probe_set_version field (D-GS8-A / v2 GS8 + GAP-48 / GS13).
          Full spec block is in v2 GS8 summary (now in KB). Pull from there — do not
          mark this provisional-only; the protocol structure is ratified even though
          numeric outputs are implementation-phase.
New §     L2 probe family: three-member domain-agnostic probe protocol (Generation probe,
          Assertion probe, Constraint probe), Semantic Assertion Criterion with three
          judgment methods (string containment, embedding similarity, pinned-version
          judge-model classification), TGA authorship authority (GAP-9 / v2 GS10 + GS13).
          Full spec block is in v2 GS10 summary (now in KB). Pull from there.
New §     Corpus author registry expiry enforcement: two-point check (submission ingress
          + IC-SL7 token issuance); EXPIRED_AUTHOR_PRESENT advisory flag on Meta-*
          Health Score results; no mid-run revocation; C-CORPUS-EXP1/2
          (v2 GS9 — note: v2 GS9 calls these D99/D100 locally; entirely different
          decisions from v3 GS5's D99/D100 and v3 GS9's D99/D100 — see D-number
          collision warning above). Full spec block in v2 GS9 summary (now in KB).
New §     Q5 weak-check: CONSTITUTIONAL_FAILURE Ledger entry gains
          invariant_statement + failure_assertion_message field pair; no runtime
          block on mismatch; C-CONSTITUTIONAL-Q5 (v2 GS9 D100 local — see D-number
          collision warning). Full spec block in v2 GS9 summary (now in KB).
New §     External document provenance for Layer 4 facts: mandatory provenance block,
          advisory-only staleness, Pruning Agent external_source_audit, IC-EXT-PROV1/2
          (GAP-11 / GS9 v3)
New §     Ledger retention policy: two-tier governance (7y Tier 1 floor + 90d Tier 3
          active period), ledger-archive/v1 format, IC-RETENTION1/2 (GAP-12 / GS9 v3)
Appendix C  All outstanding Ledger entry type additions — running total exceeds 50
            new types across GS3 through GS12. Pull from gap-backlog-v5.md and session
            summaries; apply deprecation markers for HOLD_RELEASE_SIGNATURE_INVALID and
            HOLD_RELEASE_REPLAY_REJECTED per A7b.

─── DEFERRED / PROVISIONAL ITEMS ────────────────────────────────────────────

The following items remain explicitly deferred to v2 implementation-phase
or future spec work. Mark each with: "Implementation-time decision (OQ-[ref])"
or "Deferred to v3 (OQ-[ref])" as appropriate:

- GAP-1 / GAP-2: all threshold values tied to empirical calibration
  (drift thresholds, MEMIT sub-batch ceiling, ε coefficient, M in T13's
  three-tier model). Mark all as provisional. The calibration protocol
  structure itself (D-GS8-A) is ratified and should appear as a full spec
  block (see Major Structural Additions above — pull from v2 GS8 summary).
  Only the numeric outputs of that protocol are implementation-phase.
- GAP-4 path specs: three conditional spec blocks (Path A/B/C) — each
  marked "activates on operator selection of Path [X]". Include GAP-56
  burst-limit density check, GAP-57 non-universal binary deployment note,
  and GAP-58 state-machine behavior per path.
- GAP-13: Genesis automation (secondary LLM reviewer as human-review
  proxy) — v3 scope. Human review mandatory in v2.
- GAP-17: Voluntary Write Lock release — v3 scope.
- GAP-18: Multi-machine Ledger replication — v3 scope.
- GAP-19: OOK + CAK key rotation — v3 scope. Include dependency map.
- GAP-27 resolution: scope_update_min_interval_seconds placed at Tier 3
  Anchored Git Config (rate-limits.json); dual-layer rate limit
  (per-ceremony-initiator primary + per-affected-agent-id secondary).
- OQ-SC3: Stale Layer 4 fact reconciliation workflow — mark as open,
  implementation-time decision per GS13 outcome.
- T15: CAK availability v2 path documented (OQ-S-CAK-2 m-of-n). Note
  that GAP-42 break-glass partially addresses OQ-S-CAK-1.
- T16: Batch Genesis Hold release — v3 scope (T16 not resolved).

─── COUNCIL TASKS ───────────────────────────────────────────────────────────

1. Produce `llm-as-database-v1_2-integrated-spec.md` as a complete,
   self-contained document. Use the standard integrated spec block format
   from the original Session 7 output (available in KB).

2. Where v1.1 spec blocks have been superseded by gap session resolutions,
   REPLACE them — do not append or annotate. The v2 spec must be readable
   without reference to v1.1.

3. Where v1.1 spec blocks remain valid and unchanged, carry them forward
   verbatim. Do not paraphrase working spec text.

4. For each new section or substantially rewritten section, note the source
   session and decision ID in a parenthetical: e.g., "(D103, GS9 v3)" at
   the end of the relevant spec block or sub-block.

5. Produce an updated Appendix C covering all Ledger entry types —
   original v1.1 types plus all additions from GS1 through GS13.
   Mark deprecated entries per A7b.

6. Produce an updated tension map summary at the end of the document
   (Appendix F or equivalent) showing all 25 tensions and their v2 status,
   drawn from tension-map-v5.md.

7. At the end of the synthesis, explicitly list any decisions where
   the council identified an inconsistency between session outputs that
   was not resolved in any gap session. Flag these as INCON-[N] items
   requiring a follow-on targeted session before the spec can be sealed.

─── KNOWN DECISION NUMBERING COLLISION ──────────────────────────────────────

Decision IDs (D-numbers) were assigned locally per session across non-sequential
runs of v1, v2, and v3 schedules. Known collision range: D89–D103. When citing
decisions in the v2 spec, use session reference + content description rather than
D-number alone where ambiguity exists. The spec-writer skill (framework-spec-writer)
can assist with traceability; invoke it if needed for the Appendix C population pass.

─── FORMAT ──────────────────────────────────────────────────────────────────

Standard integrated spec block format (from Session 7 / v1.1):

### [Component] — Spec Block
What it must do / represent / enforce / guarantee:
Hard constraints:
Tradeoffs decided:
Open questions (deferred):
Interface contract:

Section numbering: continue from v1.1 where sections exist; assign new
numbers for new sections in sequence. Do not renumber existing sections.

─── FINAL INSTRUCTION ───────────────────────────────────────────────────────

Invoke the framework-council skill. Begin with a brief synthesis plan —
which sections you will write in which order — so the structure can be
confirmed before drafting begins. Then produce the full spec document
section by section, pausing at natural boundaries (major numbered sections)
to confirm before continuing.
```
