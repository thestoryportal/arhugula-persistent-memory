# Session 2.18 Summary Block — T.2 ROME Execution

**Workstream:** WS1 — Empirical POC Execution
**Session label:** `2.18 — T.2 ROME Execution`
**Predecessor:** S2.17 (v1.6 hardening + T.2 ROME runbook v0.1 authoring) CLOSED 2026-05-04
**Successor:** S2.19 (verdict-conditional; C-FAIL branch instantiation per `session_2_19_kickoff_prompt.md` §5)
**Status:** CLOSED 2026-05-05
**Specialist invocation set (active):** memit-specialist (primary), state-consistency-theorist (secondary), validation-contract-architect (verdict adjudication), framework-spec-writer (artifact authoring)
**Pod-side execution platform:** RunPod RTX 4090 24 GiB; NV `large_amethyst_wolverine` mounted at `/workspace`
**Model:** `meta-llama/Llama-3.1-8B` fp16; revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`
**ROME repo SHA:** `0874014cd9837e4365f3e6f3c71400ef11509e04` (latest stable tip per D-S217-Q2-1)

---

## Headline verdict

`B-FAIL` adjudicated at Cell 13 verdict gate. **T.2 ROME hypothesis ELIMINATED at canonical hparams.** The architectural-invariant ceiling first established for MEMIT (S2.15-D2 6-axis) extends to ROME at the two operator-selected candidate layers (L17 ROME paper precedent + L2 S2.14-D D.1 mediation peak). 7th axis added to the framework finding archival. Routes per `t_branch_decision_document.md` v1.0 §5 C-FAIL path to S2.19 = GRACE runbook v0.1 authoring.

---

## Detailed forensic record

Full forensic record is in companion artifact `session_2_18_summary_block_appendix.md`:
- Block A pre-flight cell-by-cell trajectory + halt classes
- All patch SHAs + edit anchors (P-7-ROME, P-8-ROME, P-9-ROME, `globals.yml`)
- compute_v iter-by-iter trajectories at L17 + L2
- 38-probe pre-edit baselines + cross-session bit-exact comparison
- Block B verdict surfaces (per-probe pre / post-edit / post-unmount)
- Mirror sync command record
- v0.2 codification deliverable specifications (rome-patches-canonical.md, t2_rome_runbook, stage_1_sect_runbook v1.7)

The primary block below is the canonical D / C / OQ / IC record and routing.

---

```
═══════════════════════════════════════════════════
SESSION 2.18 — T.2 ROME Execution
PRIMARY OUTPUTS:
  1. Block A pre-flight COMPLETE (Cells 0-8; L17 covariance extension)
  2. Three NEW source-layer patches AUTHORED + RATIFIED:
     P-7-ROME (rome/compute_u.py — batch_tokens propagation)
     P-8-ROME (rome/compute_u.py — precision coercion at matmul)
     P-9-ROME (rome/rome_main.py — precision coercion at outer-product)
  3. NEW config-layer patch class introduced:
     globals.yml (per-repo absolute NV STATS_DIR customization)
  4. Block B Cells 9-13 COMPLETE; both candidate layers tested
  5. T.2 ROME ELIMINATED at canonical hparams — 7th axis on
     architectural-invariant ceiling
  6. Cross-session bit-exact determinism checkpoint count 5→6;
     Copy-Unmount bit-exact validated for ROME single-layer dispatch
  7. Block C SKIPPED per Cell 13 verdict gate (Route A: HALT)
  8. Routes to S2.19 = GRACE runbook v0.1 authoring
═══════════════════════════════════════════════════

DECISIONS MADE
───────────────────────────────────────────────────
D-S218-1.   Block B verdict adjudicated B-FAIL at Cell 13. cfb-v3-001
            (Bo Jackson / guitar) fails consistency criterion
            P(target_new_post) > 0.5 at both candidate layers L17
            (post-edit P=0.0002; pathology BOS-collapse) and L2
            (post-edit P=0.0000; pathology compute_v non-convergence).

D-S218-2.   Route (A) HALT path selected at Cell 13 verdict gate over
            Route (B) full 15-trial Block C and Route (C) 3-trial
            subset. Block C 15-trial would replicate S2.15-D2 D.2
            precedent of 15 FAILs at structurally-identical
            calibration corridor; no verdict change expected.

D-S218-3.   T.2 ROME hypothesis ELIMINATED at canonical hparams
            (ROME paper Table 1 GPT-J reference values per
            D-S217-Q3-1). Extends architectural-invariant ceiling
            axis count from 6 to 7. Updates t_branch_decision_document
            §5 status: T.2 ROME from OPEN to ELIMINATED.

D-S218-4.   T.2 GRACE PROMOTED to active leading T-branch hypothesis
            for S2.19 routing. Pre-commitment from D-S215D2-4
            empirically reaffirmed by ROME ELIM at S2.18.

D-S218-5.   Three NEW source-layer patches RATIFIED for v0.2
            rome-patches-canonical.md codification:
            P-7-ROME (rome/compute_u.py; 3 surgical edits;
              threads mom2_batch_tokens through get_inv_cov →
              layer_stats; closes upstream defect of cache MISS
              path producing _mom2_100000.npz instead of post-P-6
              _mom2_t100_100000.npz);
            P-8-ROME (rome/compute_u.py; 1 surgical edit;
              .to(u.dtype) cast on get_inv_cov return value at
              matmul site; closes upstream defect of fp32 inv_cov
              @ fp16 cur_repr matmul on fp16 base models);
            P-9-ROME (rome/rome_main.py; 2 surgical edits at
              execute_rome L117 and apply_rome_to_model L43;
              .to(weight.dtype) cast on both operands at
              outer-product sites; closes upstream defect of
              fp16 left_vector @ fp32 right_vector matmul).

D-S218-6.   NEW config-layer patch class introduced. ROME-side
            globals.yml customized from upstream cwd-relative
            "data/stats" to absolute NV-anchored
            "/workspace/covariance_caches"; pristine backed up at
            globals.yml.upstream_pristine. Parallel to MEMIT pre-S2.6
            fork-work customization, but applied to a structurally
            different schema (4 paths vs 5; no KV_DIR). v0.2
            patches doc must introduce CONFIG_LAYER patch class
            distinct from SOURCE_LAYER patch class.

D-S218-7.   Cross-session bit-exact determinism checkpoint count
            incremented 5 → 6. Llama-3.1-8B fp16 forward-pass
            drift = 0.00e+00 across 5 facts + 38 probes vs
            pre-S2.18 backup. OQ-S214D-DETERMINISM-1 empirical
            anchor strengthened.

D-S218-8.   Copy-Unmount bit-exact mechanism EMPIRICALLY-VALIDATED
            for ROME single-layer dispatch at L17 (drift_max =
            0.00e+00) and L2 (drift_max = 0.00e+00). Extends
            S2.14-D MEMIT joint-5-fact-overlay validation (4-layer
            band L4-L8) and S2.15-D2 narrowed L2-L6 band
            validation to ROME single-fact single-layer regime.
            Six layer ranges across three write-engine
            configurations all bit-exact.

D-S218-9.   Q4-1 (load-bearing layer selection L17 vs L2) CLOSED
            with value NO_LOAD_BEARING_LAYER. Both candidate
            layers fail consistency criterion. L17 fails via
            wrong-direction (BOS collapse on rewrite-shape
            prompt); L2 fails via compute_v non-convergence
            (oscillating loss; landscape unfittable). Different
            mechanisms, same outcome.

D-S218-10.  Q5-1 (cfb-v3-004 multi-token RE-EVALUATE at Trial 0)
            CLOSED-MOOT. Single-token cfb-v3-001 failed at both
            layers; multi-token first-token-proxy semantics for
            cfb-v3-004 would not succeed where strong single-token
            failed. MULTI_TOKEN_ALLOWLIST mechanism remains
            structurally valid for v0.2 codification (D-S215D2-
            CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1
            carry-forward unchanged).

D-S218-11.  v0.2 codification deliverables MANDATORY for clean
            S2.19 entry:
            - rome-patches-canonical.md v0.1 → v0.2 (8 source
              patches + 1 config patch + 8 v0_1_undocumented_findings)
            - t2_rome_runbook.md v0.1 → v0.2 (multiple cell-level
              notebook adaptations absorbed canonically)
            - stage_1_sect_runbook v1.6 → v1.7 (MULTI_TOKEN_
              ALLOWLIST canonical absorption; retroactive miss for
              MEMIT-side too).

D-S218-12.  framework_finding_memit_ceiling_archival.md v1.0 →
            v1.1 RECOMMENDED. Extend axis count 6→7; add T.2 ROME
            ELIM record; preserve v1.0 PERMANENT framework finding
            integrity.

D-S218-13.  t_branch_decision_document.md v1.0 → v1.1 RECOMMENDED.
            Record T.2 ROME ELIM at canonical hparams; promote
            T.2 GRACE to leading hypothesis with active routing
            target status.

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C-ROME-1.   Single-fact dispatch envelope. ROME edit dispatch via
            apply_rome_to_model MUST be invoked with requests
            list of length exactly 1 per dispatch. EMPIRICALLY-
            VALIDATED at S2.18 Cell 9 + Cell 11 (status change
            from DECLARED at v0.1 to EMPIRICALLY-VALIDATED at v0.2).

C-ROME-2.   Covariance cache reuse. ROME dispatch MUST consume the
            same covariance cache structure as MEMIT sibling at
            STATS_DIR. EMPIRICALLY-VALIDATED at S2.18 Cell 8 + 9
            + 11 — three layers (L4 smoke + L17 + L2) hit cache
            with post-P-6 _t100_ filename form. Status change
            DECLARED → EMPIRICALLY-VALIDATED.

C-ROME-3.   R1.3-equivalent dry-run gate. ROME dispatch path MUST
            be smoke-tested via direct get_inv_cov call before
            apply_rome_to_model invocation. EMPIRICALLY-VALIDATED
            at S2.18 Cell 8 (post-P-7-ROME). Status change
            DECLARED → EMPIRICALLY-VALIDATED. v0.2 codification:
            Cell 8 implementation supersedes v0.1 declarative
            scaffolding.

C-ROME-4.   Marker post-application verification. After patch
            application, marker strings MUST be verified present
            in the post-write source via re-read. EMPIRICALLY-
            VALIDATED at S2.18 P-7-ROME (3 markers), P-8-ROME
            (1 marker), P-9-ROME (2 markers; both call sites).
            Status change DECLARED → EMPIRICALLY-VALIDATED.

C-S218-1.   P-7-ROME application is REQUIRED for ROME edit
            dispatch on any base model with covariance cache
            constructed via post-P-6 batch_tokens=100 form.
            Without this patch, get_inv_cov constructs cache
            filename without _t100_ segment, hits HTTP 404 from
            upstream, falls back to local mom2 compute, OOMs
            with model resident.

C-S218-2.   P-8-ROME application is REQUIRED for ROME edit
            dispatch on any base model loaded in fp16 (or any
            non-fp32 dtype). Without this patch, the matmul at
            compute_u.py line 120 fails with dtype mismatch
            RuntimeError (fp32 inv_cov @ fp16 cur_repr).

C-S218-3.   P-9-ROME application is REQUIRED for ROME edit
            dispatch on any base model loaded in fp16. Without
            this patch, the outer-product at rome_main.py line
            117 (execute_rome) fails with dtype mismatch
            RuntimeError (fp16 left_vector @ fp32 right_vector
            from compute_v's Adam optimization buffer).

C-S218-4.   globals.yml MUST be customized on a per-repo basis
            to point STATS_DIR (and HPARAMS_DIR / RESULTS_DIR /
            DATA_DIR for completeness) at absolute NV-anchored
            paths matching the project's covariance cache
            directory layout. Cwd-relative defaults
            ("data/stats") MUST NOT be left in place for
            offline cache-hit dispatch. v0.2 codification:
            CONFIG_LAYER patch class distinct from SOURCE_LAYER.

C-S218-5.   ROMEHyperParams dataclass extension is REQUIRED to
            propagate mom2_batch_tokens to compute_u call site
            via getattr. Either subclass (ROMEHyperParamsExtended
            with mom2_batch_tokens field) or post-instantiation
            attribute assignment. Upstream 19-field dataclass
            schema (v0.2 verified count: 19) does not include
            this MEMIT-extended field.

═══════════════════════════════════════════════════
OPEN QUESTIONS
═══════════════════════════════════════════════════

CLOSED at S2.18:
───────────────────────────────────────────────────
OQ-S217-2   CLOSED at Block A pre-flight via path (a):
            extend covariance cache to include L17. 30.20 min
            wall-time, 0.766 GiB durable, IC-PreS26-3 schema
            verified.

OQ-S217-3   CLOSED with two independent verification anchors:
            apply_rome_to_model in-kernel signature matches
            pre-pod inspection: (model, tok, requests, hparams,
            copy=False, return_orig_weights=False).

OQ-S217-Q4-1 CLOSED via D-S218-9 with value NO_LOAD_BEARING_LAYER.

OQ-S217-Q5-1 CLOSED-MOOT via D-S218-10. MULTI_TOKEN_ALLOWLIST
            mechanism remains structurally valid for v0.2 even
            though Block C 15-trial was skipped.

OQ-S216-1   CLOSED at Block A pre-flight Cell 1: ROME SHA pin
            0874014cd9837e4365f3e6f3c71400ef11509e04.

OQ-S216-2   CLOSED — FAIL at canonical hparams. compute_v at
            L17 monotonically converged to ceiling 1.06e-02; at
            L2 non-converged. Both far below threshold. Mechanism
            failure is architectural, not numerical; hparam
            recalibration not indicated.

OQ-S214D-DETERMINISM-1 EMPIRICAL ANCHOR STRENGTHENED. Status
            unchanged (was CLOSED-EMPIRICAL post-S2.14-D);
            checkpoint count 5→6 at S2.18.

NEW OPEN at S2.18 (deferred to S2.19+ or operator-side):
───────────────────────────────────────────────────
OQ-S218-1   compute_v non-convergence mechanism at L2. Why does
            L2 oscillate (loss 14.5-19.3 across 20 iters; final
            P(target_new) 1.06e-06 below initial 1.32e-08
            random-baseline regime) while L17 monotonically
            decreases (loss 18.17→4.93; final 1.06e-02)?
            Diagnostic interest only — does not block S2.19
            routing. Deferred to optional S2.20+ post-mortem
            or to v1.1 framework finding archival authoring
            context. Routes to memit-specialist + Mediation
            Map Theorist (if invoked).

OQ-S218-2   BOS collapse mechanism at L17. Why does L17 wrong-
            direction edit collapse cons-1 + unmount-1 top-1 to
            <|begin_of_text|> with P=0.89 specifically? Tokenizer
            specificity? Llama-3.1-8B prompt-frame interaction?
            Llama embedding norm at BOS post-edit? Diagnostic
            interest only — does not block S2.19 routing.

OQ-S218-3   Specificity preservation generalization. cfb-v3-001
            specificity (Auburn / Alabama / Heisman year top-1
            preserved at both L17 and L2) carries forward, but
            unverified across cfb-v3-002 / 003 / 004 / 005.
            Block C 15-trial would have characterized this;
            skipped per D-S218-2. Routes diagnostic interest;
            does not block. v1.1 framework finding archival
            authoring may revisit.

OQ-S218-V0-2-CODIFICATION  v0.2 codification deliverable authoring
            (operator-side post-session). MANDATORY per D-S218-11
            for clean S2.19 entry. Three substantive deliverables:
            rome-patches-canonical.md v0.2; t2_rome_runbook v0.2;
            stage_1_sect_runbook v1.7. NOT a runtime blocker but
            IS a structural blocker for S2.19 GRACE runbook
            authoring (sibling-pattern from finalized v0.2 ROME
            structure).

CARRY-FORWARD UNCHANGED FROM PRIOR SESSIONS:
───────────────────────────────────────────────────
OQ-S214D-D1-1, OQ-S214D-D1-PREDICATE-1, OQ-S214D-PATH-1,
OQ-S214D-CWD-1, OQ-S214D-D3-OOM-1, OQ-S214D-HF-CACHE-LOCATION-1,
OQ-S214D-FSTRING-1, OQ-S214D-NV-CACHE-DEDUPE-1, OQ-S214D-D3-
OVERLAY-1, OQ-S214D-PATCH-FILE-MAP-1, OQ-S214D-TERMINAL-1,
OQ-S214D-TRANSFORMERS-1 — all REMAIN OPEN as forward concerns;
S2.18 did not interact with these.

OQ-S213C-10 CLOSED at S2.17 Block 1 (v1.6 RATIFIED) —
unchanged; informational reference only.

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
(no new interface contracts at S2.18)

S2.18 interacted with the following carry-forward IC anchors;
status of each is unchanged:
- IC-S23-4 (unmount band drift_max < 1e-4 hard gate):
  EMPIRICALLY-VALIDATED for ROME single-layer dispatch at L17
  and L2; drift_max = 0.00e+00 at both layers. Validation
  scope extends from MEMIT joint-5-fact-overlay (S2.14-D D.3,
  S2.15-D2 D.2) to ROME single-fact single-layer (S2.18 Cell
  9 + 11). Six layer ranges across three write-engine
  configurations all bit-exact.
- IC-S24-3 (single-token verdict invariant; first-token-proxy
  for cfb-v3-004 multi-token allowlist): MULTI_TOKEN_ALLOWLIST
  reapplication required notebook-side at S2.18 Cell 6 (v1.6
  hardening miss; v1.7 codification mandated per D-S218-11).
- IC-S25-3 (Stage 1 SECT pre-edit reference baseline): cross-
  session bit-exact gate added at S2.18 Cell 7 (notebook-side;
  v0.2 t2_rome_runbook codification mandated). Baseline
  artifact stage_1_llama_baselines.json bit-equivalent across
  S2.13-C / S2.14-D / S2.15-D2 / S2.18 capture under canonical
  hparams.
- IC-PreS26-2 (post-P-6 _t100_ covariance cache filename form):
  EMPIRICALLY-VALIDATED for ROME dispatch via P-7-ROME at
  S2.18 Cell 8 retry. Cache HIT confirmed at L4 (smoke), L17
  (Block B Layer-A), L2 (Block B Layer-B).
- IC-PreS26-3 (covariance cache schema; (14336,14336) float32
  PSD): EMPIRICALLY-VALIDATED for L17 cache extension at
  S2.18 Block A pre-flight.

═══════════════════════════════════════════════════
INPUT REQUIRED FOR NEXT SESSION
═══════════════════════════════════════════════════
S2.19 routing (operator-confirmed at Cell 13 verdict gate):
B-FAIL → S2.19 = GRACE runbook v0.1 authoring per
t_branch_decision_document.md v1.0 §5 C-FAIL path. Branch
instantiation from session_2_19_kickoff_prompt.md §5
(C-FAIL branch).

Pre-S2.19 BLOCKING dependencies (operator-side; per D-S218-11):

  1. v0.2 rome-patches-canonical.md authoring.
     Inputs: t2_rome_patch_state.json (8 source-layer entries +
     1 config-layer entry + 8 v0_1_undocumented_findings); P-7-
     ROME / P-8-ROME / P-9-ROME application records; pristine
     SHA backups at /workspace/rome_dry_run/rome/{rome,util}/
     *.upstream_pristine. Recategorize P-7 from INAPPLICABLE
     (v0.1) to APPLICABLE-WITH-MODIFICATION (v0.2; via P-7-
     ROME on rome/compute_u.py rather than memit/memit_main.py).
     Add P-8-ROME and P-9-ROME as NEW patch entries.

  2. v0.2 t2_rome_runbook.md authoring.
     Inputs: notebook-side cell adaptations from S2.18
     execution. Substantive adaptations to absorb canonically:
     Cell 3 EXPECTED_LAYERS parameterization via SESSION-bound
     hparam; Cell 4 schema count fix (20→21); Cell 5 defensive
     preamble for L17-extension model cleanup; Cell 6 MULTI_
     TOKEN_ALLOWLIST + first-token-proxy logic (also needed
     v1.7 MEMIT-side); Cell 7 explicit cross-session bit-exact
     gate; Cell 8 ROME-specific R1.3-equivalent (smoke calls
     get_inv_cov, not hypothetical get_cov); Cell 9 hparam
     subclass pattern (ROMEHyperParamsExtended) for mom2_batch
     _tokens propagation; Cell 13 verdict gate adjudication
     framework with three-route option matrix.

  3. v1.7 stage_1_sect_runbook.md authoring (retroactive miss
     codification for MEMIT side). Inputs: D-S215D2-CFB-V3-
     004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1 ratified
     at S2.15-D2 close; v1.6 Cell 6 absorbed at S2.17 Block 1
     ratification but did NOT include MULTI_TOKEN_ALLOWLIST
     mechanism. Notebook-side reapplication at S2.18 Cell 6
     surfaced this miss. v1.7 must absorb the allowlist
     declaration + first-token-proxy capture logic + RE-
     EVALUATE flag wiring at Cell 13 canonically.

Pre-S2.19 RECOMMENDED dependencies (operator-side; per D-S218-12,
D-S218-13):

  4. v1.1 framework_finding_memit_ceiling_archival.md authoring.
     Extend axis count 6 → 7; add Axis 7 = "write engine ROME
     at L17 + L2 (S2.18 empirical)"; preserve v1.0 PERMANENT
     framework finding integrity. Status: ROME ELIM is now
     load-bearing for the framework-level claim.

  5. v1.1 t_branch_decision_document.md authoring. Update §5
     T.2 ROME from OPEN to ELIMINATED at canonical hparams;
     promote T.2 GRACE to active leading hypothesis with
     S2.19 routing target status.

S2.19 entry artifact: session_2_19_kickoff_prompt.md
(C-FAIL branch instantiation; verdict-conditional template
authored at S2.17 close).

S2.19 anticipated scope: parallel structure to S2.17 Block 2
(ROME runbook v0.1 authoring). Author grace-patches-canonical.md
v0.1 + grace_runbook v0.1; declarative; schema-faithful; SHA-
pinned to a chosen GRACE upstream commit; 5 carry-forward OQs
projected.

S2.20 anticipated scope: GRACE pod-side execution (parallel
to S2.18 ROME execution). Sufficient compute headroom on
RTX 4090 24 GiB for adapter-based mechanism (memory profile
likely lower than ROME's compute_v Adam buffers).

═══════════════════════════════════════════════════
```

---

## Specialist provenance

- **memit-specialist (primary):** ROME edit dispatch architecture analysis; precision boundary diagnosis (P-8-ROME + P-9-ROME); compute_v trajectory interpretation at L17 + L2; T.2 ROME ELIM verdict reasoning; T-branch matrix update.
- **state-consistency-theorist (secondary):** Cross-session bit-exact determinism gate authoring (Cell 7 v0.2 codification); Copy-Unmount mechanism validation under ROME single-fact regime; NV state discipline (Cell 18-20 inventory + manifest).
- **validation-contract-architect (verdict adjudication):** Cell 13 verdict gate formalization; calibration corridor PASS criterion application; routing option trade-space (A / B / C); MULTI_TOKEN_ALLOWLIST first-token-proxy verdict logic at Cell 6.
- **framework-spec-writer (artifact authoring):** This summary block + companion appendix.

Carry-forward specialist invocation rationale: WS1 active subset (memit-specialist primary, state-consistency-theorist secondary, validation-contract-architect occasional, framework-spec-writer for artifact authoring) per project instructions. Other skills (graph-data-architect, aiSecOps-specialist, orchestration-comparativist, framework-council) remained dormant — appropriate for execution-focused session.

---

## Non-goals

This session summary block does NOT:

- Author v0.2 codification deliverables. Those are operator-side post-session work (per D-S218-11).
- Make architectural decisions about T.2 GRACE strategy or T.2 GRACE candidate commit selection. Those are S2.19 scope.
- Resolve OQ-S218-1 (compute_v non-convergence mechanism at L2) or OQ-S218-2 (BOS collapse mechanism at L17). Those are diagnostic-interest open questions; not verdict-blockers.
- Verify Block C 15-trial trial-to-trial variance characterization. Block C SKIPPED per D-S218-2 routing decision.
- Update framework_finding_memit_ceiling_archival.md or t_branch_decision_document.md inline. Those are RECOMMENDED operator-side authoring per D-S218-12 / D-S218-13.

---

## Carry-forward to v0.2 codification (post-session operator-side work)

Three substantive deliverables MUST be authored before S2.19 entry to preserve sibling-pattern parity between ROME (v0.2) and GRACE (v0.1 to be authored at S2.19):

1. **rome-patches-canonical.md v0.2** — supersedes v0.1 declarative. 8 source-layer + 1 config-layer = 9 patches in inventory; 8 v0_1_undocumented_findings entries; recategorization of P-7 from INAPPLICABLE → APPLICABLE-WITH-MODIFICATION; introduction of CONFIG_LAYER patch class.

2. **t2_rome_runbook.md v0.2** — supersedes v0.1 declarative. Multiple cell-level notebook adaptations absorbed canonically (per OQ-S218-V0-2-CODIFICATION enumeration above).

3. **stage_1_sect_runbook.md v1.7** — supersedes v1.6. MULTI_TOKEN_ALLOWLIST canonical absorption; retroactive miss for MEMIT-side too (v1.6 ratification at S2.17 Block 1 did not include the S2.15-D2 ratified mechanism; surfaced at S2.18 Cell 6 reapplication).

Two RECOMMENDED authoring tasks for framework finding integrity:

4. **framework_finding_memit_ceiling_archival.md v1.1** — extend axis count 6→7; add Axis 7 = ROME L17 + L2.

5. **t_branch_decision_document.md v1.1** — record T.2 ROME ELIM; promote T.2 GRACE to leading hypothesis.

Post-authoring KB curation: ADD the five new authored documents; KEEP the v1.0 PERMANENT framework finding archival as historical anchor; REMOVE no documents (additive update; v1.0 → v1.1 supersession is non-destructive).
