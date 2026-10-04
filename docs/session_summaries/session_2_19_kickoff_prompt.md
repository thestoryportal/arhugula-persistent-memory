# Session 2.19 Kickoff Prompt — T.2 GRACE Runbook v0.1 Authoring (C-FAIL Branch Active)

> **Session label:** S2.19
> **Session date target:** 2026-05-05+ (operator-side scheduling; this is the v0.2-codification-session-ratified successor)
> **Session class:** Operator-side spec codification + runbook authoring session — NO pod-side execution; NO RunPod attach; NO NV interaction at this session
> **Predecessor session:** v0.2 codification session (CLOSED 2026-05-05; six deliverables RATIFIED — see `session_v0_2_codification_summary_block.md`)
> **2-back predecessor:** S2.18 (T.2 ROME first-execution; CLOSED 2026-05-05 with verdict B-FAIL → T.2 ROME ELIMINATED at canonical hparams)
> **Successor session (target):** S2.20 = T.2 GRACE Stage 1 SECT v3 execution (pod-side; parallel structure to S2.18)
> **Workstream:** WS1 (empirical execution; T-branch entry; T.2 GRACE leading post-ROME-elimination)
> **Verdict-conditional branch:** C-FAIL ACTIVE per `t_branch_decision_document.md` v1.1 §5' empirical resolution (T.2 ROME B-FAIL → escalate to GRACE per v1.0 §5 conditional execution plan)

---

## §1 — Session orientation

### §1.1 Why this session

T.2 ROME ELIMINATED at canonical hparams (S2.18 D-S218-3). The architectural-invariant ceiling on `(Llama-3.1-8B × MEMIT × canonical hparams)` extends to `(Llama-3.1-8B × {MEMIT, ROME} × canonical hparams)` per `framework_finding_memit_ceiling_archival.md` v1.1 §1' Axis 7. T.2 GRACE PROMOTED to leading T-branch hypothesis per D-S218-4 (codified at `t_branch_decision_document.md` v1.1 §1' decision statement amendment).

GRACE is the next test surface because its mechanism is **structurally distinct** from rank-1 in-weight write engines: GRACE adds adapter modules with their own parameters and a routing-layer dispatch; the base model weights are NOT modified in-place. The architectural-invariant ceiling claim does NOT transitively cover GRACE because GRACE does not implement the suspect mechanism class (z-vector update geometry on the base model's MLP down-projection layers). If T.2 GRACE PASSES on Llama-3.1-8B at canonical hparams, the empirical result confirms the ceiling is rank-1-in-weight-class-specific and the framework has a viable adapter-based path forward. If T.2 GRACE FAILS, the suspect locus is `(model × hparams)` independent of write-engine class — falls back to T.1 alt-model testing per v1.1 §5' conditional execution plan.

### §1.2 What this session does

This session authors two parallel canonical artifacts that together unblock S2.20 = T.2 GRACE pod-side execution:

1. **`grace-patches-canonical.md` v0.1** — parallel sibling to `memit-patches-canonical.md` v2.5 (preserved unmodified) and `rome-patches-canonical.md` v0.2 (preserved post-elimination as historical record + carry-forward). Three coexisting write-engine canonicals after this session close.
2. **`t2_grace_runbook.md` v0.1** — parallel sibling to `t2_rome_runbook.md` v0.2 (which inherits structurally from `stage_1_sect_runbook_v1_6.md` / now v1.7). Three-block structure (Block A pre-flight + Block B HC-2-equivalent dry-run + Block C trial loop). Cell-by-cell adaptation per GRACE adapter dispatch surface.

### §1.3 What this session does NOT do

- No pod-side execution. v0.1 ratification is authoring-acceptance-only at S2.19 close; empirical first-execution at S2.20.
- No GRACE empirical pre-judgment. Hparams declared at canonical reference; verdict surface empirical at S2.20 Block B.
- No modification of `memit-patches-canonical.md` v2.5 or `rome-patches-canonical.md` v0.2. Sibling-parity discipline preserved.
- No modification of `framework_finding_memit_ceiling_archival.md` v1.1 or `t_branch_decision_document.md` v1.1. Both are RATIFIED at v0.2 codification session close; this session inherits from them.
- No amendment of the v1.2 integrated framework spec. Sealed.

---

## §2 — Specialists

### §2.1 Active for this session

| Specialist | Role | Cell ranges / sections of primary involvement |
|---|---|---|
| **framework-spec-writer** | Primary; runbook + patches canonical authoring; v0.1 spec format discipline | All sections; structural template inheritance from `t2_rome_runbook.md` v0.2 + sibling-parity from `rome-patches-canonical.md` v0.2 |
| **memit-specialist** | GRACE adapter mechanism specification; hparam surface derivation from GRACE paper Table 1; mechanism-orthogonality argument cross-validation | grace-patches-canonical §1 (patch inventory; MEMIT/ROME inheritance scope); §3 SHA pin; §4 hparams. t2_grace_runbook Cells 1, 2, 4, 8, 9, 11, 15 |
| **state-consistency-theorist** | GRACE unmount mechanism specification (parallel to but structurally distinct from Copy-Unmount); covariance cache inapplicability rationale; cross-session bit-exact determinism inheritance | grace-patches-canonical §5 process constraints (parallel to C-ROME-1..4 / C-S218-1..5). t2_grace_runbook Cells 3, 5, 7, 15 |
| **validation-contract-architect** | Cell 6 / Cell 7 / Cell 9 verdict surface; calibration corridor PASS criterion; pathology classification (degenerate-fit / unfittable-landscape carry-forward from S2.18 ROME taxonomy) | t2_grace_runbook Cells 6, 7, 10, 12, 13, 16. MULTI_TOKEN_ALLOWLIST canonical absorption inheritance from `stage_1_sect_runbook_v1_7.md` §1.5.3 |
| **orchestration-comparativist** | Write-engine architecture comparison surface (foreground at v1.1 GRACE entry); adapter-vs-rank-1-update structural comparison; framework-spec-relevance scoring | grace-patches-canonical §0 purpose + §11 upstream notes vs MEMIT v2.5 + ROME v0.2 |
| **graph-data-architect** | Light-touch; framework-spec-relevance scoring for adapter-based mechanisms (closer to .vindex overlay model than rank-1 update mechanisms) | grace-patches-canonical §0 purpose framing only |

### §2.2 Inactive at this session

`aiSecOps-specialist` (no trust-boundary work in scope; reactivated at Workstream 2 / 3); `framework-council` (single-domain authoring session; no cross-domain tension mapping needed).

---

## §3 — Read order (load-bearing inputs)

The following artifacts MUST be read at session entry. v0.2 codification session deliverables are the primary inputs; v1.0 archival + decision-document-v1.0 are inherited via the v1.1 amendments.

### §3.1 Mandatory pre-read (in order)

1. **`session_v0_2_codification_summary_block.md`** — predecessor session record; §6 deliverables interaction map + §7 forward routing + §8 empirical anchor inheritance summary
2. **`t_branch_decision_document.md` v1.1** — load-bearing for this session's scope; §4'.2 GRACE selection rationale + §4'.3 GRACE entry preconditions + §6' methodology lock for T.2 GRACE
3. **`framework_finding_memit_ceiling_archival.md` v1.1** — §1' ceiling scope extension + §3' hypothesis-class ledger + §4.3'.4 patches carry-forward applicability for GRACE
4. **`rome-patches-canonical.md` v0.2** — sibling-parity template; structural pattern for grace-patches-canonical v0.1 authoring (sections, taxonomy, constraint codification, inventory partitioning)
5. **`t2_rome_runbook.md` v0.2** — structural template; cell-by-cell pattern for t2_grace_runbook v0.1 authoring (Block A/B/C; Cell 13 verdict gate 3-route option matrix; Cell 6 MULTI_TOKEN_ALLOWLIST canonical absorption)

### §3.2 Reference inputs (consulted as needed)

6. **`stage_1_sect_runbook_v1_7.md`** — MEMIT-side parallel sibling; canonical absorption blocks at Cell 6 §1.5.3.1 + Cell 7 §1.5.3.2 + Cell 9 §1.5.3.3 (inheritance pattern for t2_grace_runbook Cell 6 / Cell 7 / Cell 9)
7. **`memit-patches-canonical.md` v2.5** — sibling-parity reference (preserved unmodified; not modified by this session)
8. **`session_2_18_summary_block.md` + `session_2_18_summary_block_appendix.md`** — S2.18 forensic anchor; consulted for the pathology classification taxonomy (degenerate-fit / unfittable-landscape) which is carry-forward to GRACE Cell 12

### §3.3 Operator-side preconditions (before session entry)

- Git references for `https://github.com/Thartvigsen/GRACE` accessible (SHA pin selection at §5 Q1)
- GRACE paper + supplementary accessible for hparam surface derivation (canonical reference values per Table 1 of Hartvigsen et al.)
- Read access to all v0.2 codification deliverables in `/mnt/user-data/outputs/`

---

## §4 — Block structure

S2.19 follows a two-block authoring structure analogous to S2.17 (where Block 1 = stage_1_sect_runbook v1.6 hardening + Block 2 = t2_rome_runbook v0.1 authoring). At S2.19 the two blocks both produce GRACE artifacts:

### §4.1 Block 1 — `grace-patches-canonical.md` v0.1 authoring

**Scope.** Author the parallel sibling patches canonical for GRACE. Inherit structural shape from `rome-patches-canonical.md` v0.2 (15 sections; two-class taxonomy SOURCE_LAYER + CONFIG_LAYER; constraint registry; verification anchors; manifest schema).

**Major content surfaces:**

- **§0 purpose & non-amendment declaration** — declare grace-patches-canonical as parallel sibling; do NOT amend MEMIT v2.5 or ROME v0.2; document scope; framework-spec relevance (graph-data-architect light-touch contribution: adapter-based mechanisms are closer to the .vindex overlay model than rank-1 update mechanisms; this is informative for Workstream 2/3)
- **§1 patch inventory** — partition into:
  - §1.1 SOURCE_LAYER inherited from MEMIT/ROME APPLICABLE-DIRECTLY: Pad-Token (tokenizer-side; engine-agnostic; carry-forward); P-1/P-2 OPEN (whether GRACE adapter forward pass uses any retain-trace pattern; resolved at v0.1 authoring per actual GRACE codebase inspection)
  - §1.2 SOURCE_LAYER INAPPLICABLE: P-4/P-5/P-6/P-7-ROME/P-8-ROME/P-9-ROME (all relate to covariance projection / outer-product / rank-1 update mechanism not used by GRACE); Copy-Unmount (in-place tensor restore — INAPPLICABLE to adapter mechanism)
  - §1.3 SOURCE_LAYER NEW patches surfaced at v0.1 authoring: TBD per actual GRACE codebase inspection (analogous to S2.18 Block A patch authoring at first execution; v0.1 declarative may need v0.2 absorption post-S2.20 first-execution)
  - §1.6 CONFIG_LAYER NEW class instances: globals.yml-equivalent (if GRACE has parallel config-loading idiom; OPEN at v0.1)
- **§3 SHA pin** — resolved at Q1 (operator selects SHA at session entry)
- **§4 canonical hparams** — adapter-rank, routing-threshold, memory-pool-size, learning-rate per GRACE paper Table 1 starting values
- **§5 process constraints** — author C-GRACE-1 through C-GRACE-N analogous to C-ROME-1..4 (single-fact dispatch envelope or multi-fact accumulation envelope; cache reuse if any; R1.3-equivalent dry-run gate; marker post-application verification)
- **§6+ NEW SOURCE_LAYER patches detail** — analogous to §6/§7/§8 in rome-patches-canonical v0.2 (P-7-ROME/P-8-ROME/P-9-ROME detail format)
- **§N CONFIG_LAYER patch detail** — analogous to §9 in rome-patches-canonical v0.2 (globals.yml detail format)

**Acceptance criteria for Block 1 close:**

| Criterion | Verification |
|---|---|
| Sibling-parity preserved | grace-patches-canonical v0.1 does NOT modify memit-patches-canonical v2.5 OR rome-patches-canonical v0.2 |
| Two-class taxonomy adopted | §1 inventory uses SOURCE_LAYER + CONFIG_LAYER per D-V02-6 carry-forward |
| Mechanism-orthogonality argument codified | §0 purpose + §1.2 INAPPLICABLE rationale clearly delineates adapter-mechanism vs rank-1-mechanism boundary |
| All v0.1 patches DECLARATIVE-status flagged | per parallel pattern from rome v0.1 declarative status; v0.2 absorption deferred to post-S2.20 |
| Empirical anchor inheritance recorded | cross-session bit-exact determinism (6 checkpoints) inherited; Pad-Token applicability inherited; Copy-Unmount + covariance caches INAPPLICABLE noted |

### §4.2 Block 2 — `t2_grace_runbook.md` v0.1 authoring

**Scope.** Author the parallel sibling runbook for GRACE. Inherit structural shape from `t2_rome_runbook.md` v0.2 (21 cells; Block A pre-flight + Block B HC-2-equivalent dry-run + Block C trial loop; 3-route Cell 13 verdict gate).

**Major content surfaces:**

- **Frontmatter & §1.5 authoring discipline** — parallel to t2_rome_runbook v0.2; C-S26-3 dry-run gate constraint inherited; C-GRACE-3 R1.3-equivalent dry-run gate ratified
- **§1.5.X anchors** — single-fact dispatch envelope (or batched-edit envelope per GRACE paper); empirical anchor inheritance from S2.18 (cross-session bit-exact 6 checkpoints; cfb-v3.yaml v1.0; probe-set-v3.yaml v1.0; stage_1_llama_baselines.json)
- **Cell 0** — system binaries + Python deps (inherited unchanged from MEMIT v1.7 / ROME v0.2 Cell 0)
- **Cell 1** — GRACE repo clone + SHA pin resolution (parallel to t2_rome v0.2 Cell 1; SHA pin per Q1 resolution)
- **Cell 2** — GRACE patch state verification + transplant (if any) + new SOURCE_LAYER patches application + CONFIG_LAYER patches (if applicable)
- **Cell 3** — covariance cache reuse verification — **INAPPLICABLE for GRACE per t_branch_decision_document v1.1 §6'.3**; Cell 3 either declares INAPPLICABLE-DEFERRED-BY-MECHANISM OR replaces with adapter-pool initialization verification (TBD at authoring; resolved at Q5)
- **Cell 4** — GRACE hparam declaration; adapter-rank, routing-threshold, memory-pool-size, learning-rate per GRACE paper Table 1 + Llama adaptation; ROMEHyperParamsExtended-equivalent subclass for GRACE-specific fields
- **Cell 5** — Llama-3.1-8B model load + Pad-Token alias + cross-session bit-exact gate (INHERITED UNCHANGED from MEMIT v1.7 / ROME v0.2 Cell 5; defensive preamble for any prior model cleanup)
- **Cell 6** — LLaMA tokenizer single-token verification + MULTI_TOKEN_ALLOWLIST canonical absorption (INHERITED via D-V12-MULTITOKEN-1 carry-forward from `stage_1_sect_runbook_v1_7.md` §1.5.3.1; same canonical block; first-token-proxy posture preserved at DECLARED-via-v0.2 with RE-EVALUATE flag)
- **Cell 7** — pre-edit baseline capture + cross-session bit-exact gate (INHERITED from `stage_1_sect_runbook_v1_7.md` Cell 7 §1.5.3.2 verdict_class dispatch wiring; D-S217-4 6-checkpoint anchor + D-V12-MULTITOKEN-1 first-token-proxy P-capture)
- **Cell 8** — R1.3-equivalent dry-run gate for GRACE dispatch path (parallel to t2_rome v0.2 Cell 8; smoke-load uses GRACE adapter init + forward pass, NOT covariance cache resolution since no covariance cache used)
- **Cells 9-13 Block B** — single-fact GRACE edit dispatch (or batched per GRACE paper); cross-layer comparison if applicable (GRACE may not have layer-set candidates equivalent to L17/L2; adapter placement is the analog); pathology classification (degenerate-fit / unfittable-landscape carry-forward from S2.18 ROME taxonomy at t2_rome v0.2 Cell 12); Cell 13 3-route verdict gate (Route A halt / Route B 15-trial / Route C 3-trial preview) inherited unchanged
- **Cells 14-17 Block C** — declarative trial loop (analogous to t2_rome v0.2 Cell 14-17; GRACE multi-fact accumulation semantics may differ from MEMIT batched / ROME single-fact)
- **Cell 15 trial loop body** — GRACE adapter unmount semantics (NOT Copy-Unmount; adapter detach mechanism specified at Q4)
- **Cells 18-20** — NV inventory + SHA equality gate + mirror sync + manifest update + routing decision print (parallel to t2_rome v0.2)

**Acceptance criteria for Block 2 close:**

| Criterion | Verification |
|---|---|
| Cell numbering inherited from t2_rome v0.2 | 21 cells; Block A 0-8, Block B 9-13, Block C 14-20 |
| Sibling-parity preserved | t2_grace_runbook v0.1 does NOT modify t2_rome_runbook v0.2 OR stage_1_sect_runbook_v1_7 |
| MULTI_TOKEN_ALLOWLIST canonical absorption inherited | Cell 6 / Cell 7 / Cell 9 inherits from stage_1_sect_runbook_v1_7 §1.5.3.X via parallel pattern |
| Cell 13 3-route verdict gate inherited | empirically anchored taxonomy from S2.18 codified at t2_rome v0.2 carries forward |
| Adapter unmount semantics specified canonically | Cell 15 trial loop body declares the GRACE-specific unmount mechanism (NOT Copy-Unmount); resolves OQ-V11-T-BRANCH-5 |
| All v0.1 cell bodies DECLARATIVE-status flagged | per parallel pattern from t2_rome v0.1 declarative status; v0.2 absorption deferred to post-S2.20 first-execution |

---

## §5 — Q1-Q5 design questions for ratification at session close

These are the load-bearing operator-resolved questions for v0.1 ratification, parallel to S2.17 Q1-Q5 (which produced D-S217-Q2-1 through D-S217-Q5-1).

### §5.1 Q1 — GRACE SHA pin selection

**Question.** What SHA pin is canonical for GRACE at v0.1?
**Options.** (a) Latest stable tip of `https://github.com/Thartvigsen/GRACE` (parallel to D-S217-Q2-1 ROME selection); (b) GRACE paper supplementary release tag; (c) parent commit of any cited fork.
**Recommendation.** Latest stable tip (option a) — parallel to ROME selection at S2.17.
**Closure ID:** D-S219-Q1-1
**OQ ID:** OQ-V11-T-BRANCH-1 (carry-forward from t_branch_decision_document v1.1 §8'.2)

### §5.2 Q2 — GRACE canonical hparams reference

**Question.** What canonical hparams are declared at v0.1 for `meta-llama/Llama-3.1-8B`?
**Options.** (a) GRACE paper Table 1 starting values verbatim (originally derived against GPT-2-XL / GPT-J reference architectures); (b) GPT-J reference values + Llama-specific calibration sweep at v0.1 authoring; (c) GRACE paper Table 1 + targeted Llama adaptation per architecture differences (32 layers vs GPT-J 28; hidden 4096 vs GPT-J 4096; attention head count differences).
**Recommendation.** Option (c) — minimal Llama adaptation; full calibration deferred to S2.20 Block B Cell 13 verdict gate.
**Closure ID:** D-S219-Q2-1
**OQ ID:** OQ-V11-T-BRANCH-2

### §5.3 Q3 — GRACE adapter placement at Llama-3.1-8B

**Question.** What adapter placement is declared at v0.1?
**Options.** (a) GRACE paper canonical placement (transformer-mid layer per GRACE paper §X) verbatim; (b) Llama-3.1-8B-specific adaptation per architecture (e.g., L15-L17 transformer-mid analog to ROME L17 paper precedent); (c) S2.14-D D.1 mediation peak band L2-L6 (parallel to MEMIT canonical layer set per D-S215D2-1).
**Recommendation.** Two-candidate test surface analogous to D-S217-Q4-1 (which selected L17 primary + L2 secondary for ROME): (b) primary + (c) secondary. Block B at S2.20 tests both.
**Closure ID:** D-S219-Q3-1
**OQ ID:** OQ-V11-T-BRANCH-3

### §5.4 Q4 — GRACE unmount mechanism canonical specification

**Question.** What unmount mechanism is canonical at v0.1?
**Options.** (a) Adapter-detach: remove adapter from routing layer; restore base-model forward-pass behavior (parameters retained but bypassed); (b) Adapter-pop: remove adapter and free its parameters; routing layer restored to no-adapter state; (c) Adapter-snapshot-restore: snapshot adapter state at trial entry; restore at unmount (parallel to Copy-Unmount weight-snapshot pattern but on adapter parameters rather than base weights).
**Recommendation.** Option (a) Adapter-detach for v0.1 (cleanest mechanism; parallel to ROME `weights_copy` return pattern but on routing-layer adapter list). Option (c) considered if adapter-detach produces inter-trial drift > 0 on shared-spec probes (re-evaluate at S2.20 Block B Cell 9).
**Closure ID:** D-S219-Q4-1
**OQ ID:** OQ-V11-T-BRANCH-5

### §5.5 Q5 — Multi-token tolerance posture for cfb-v3-004 under GRACE

**Question.** What multi-token tolerance posture is canonical at v0.1 for cfb-v3-004 (Hakeem Olajuwon plays the instrument of harp; multi-token target_new under Llama tokenizer)?
**Options.** (a) Carry-forward first-token-proxy methodology from D-S215D2-CFB-V3-004-PROXY-1 + D-V12-MULTITOKEN-1 with `RE-EVALUATE AT TRIAL 0` flag (parallel to D-S217-Q5-1 ROME disposition); (b) Strict single-token-only (drop cfb-v3-004 from Stage 1 SECT v3 trial roster for GRACE; reduce trial count from 15 → 12); (c) GRACE-specific multi-token canonical handling (if GRACE paper documents native multi-token target_new dispatch, use that and retire first-token-proxy at v0.1).
**Recommendation.** Option (a) — carry-forward; RE-EVALUATE at S2.20 Block B Cell 9 trial 0 against actual GRACE multi-token dispatch behavior (per t_branch_decision_document v1.1 §6'.2).
**Closure ID:** D-S219-Q5-1
**OQ ID:** OQ-V11-T-BRANCH-4

---

## §6 — Acceptance criteria for session close

### §6.1 Block 1 acceptance (grace-patches-canonical.md v0.1)

| Criterion | Verification mechanism |
|---|---|
| File present in outputs at `/mnt/user-data/outputs/grace-patches-canonical.md` | File system check |
| Frontmatter declares v0.1 RATIFIED status | Section header inspection |
| §0 non-amendment declaration cites memit v2.5 + rome v0.2 preservation | Section content inspection |
| §1 patch inventory partitioned per two-class taxonomy | §1.1-§1.6 subsections present |
| §3 SHA pin recorded per Q1 closure | §3 content inspection |
| §4 canonical hparams declared per Q2 closure | §4 content inspection |
| §5 C-GRACE-1..N constraints declared | §5 process constraints registry |
| §6+ NEW patches detail (if any) authored at v0.1 OR DEFERRED to v0.2 absorption flagged | §6+ content or §0 deferral note |
| §15 authoring metadata complete | metadata table populated |

### §6.2 Block 2 acceptance (t2_grace_runbook.md v0.1)

| Criterion | Verification mechanism |
|---|---|
| File present in outputs at `/mnt/user-data/outputs/t2_grace_runbook.md` | File system check |
| Frontmatter declares v0.1 RATIFIED status (declarative; first-execution at S2.20) | Section header inspection |
| §1.5 authoring discipline carry-forward from t2_rome v0.2 §1.5 | Section structure parallel to ROME |
| Cells 0-20 declared per parallel structure to t2_rome v0.2 | Cell-by-cell inspection |
| Cell 4 ROMEHyperParamsExtended-equivalent for GRACE hparams declared per Q2/Q3 | Cell 4 content inspection |
| Cell 6 MULTI_TOKEN_ALLOWLIST canonical absorption inherited from v1.7 §1.5.3.1 | Cell 6 absorption block present |
| Cell 13 3-route verdict gate inherited from t2_rome v0.2 | Cell 13 content inspection |
| Cell 15 GRACE unmount mechanism specified per Q4 | Cell 15 trial loop body |
| §10 reference appendices complete (carry-forward inheritance + NV path + cell-to-decision traceability + authoring metadata) | §10 sections populated |

### §6.3 Session close artifact

| Criterion | Verification mechanism |
|---|---|
| `session_2_19_summary_block.md` authored at session close | File system check |
| Decisions D-S219-Q1-1 through D-S219-Q5-1 ratified | Decision table inspection |
| Open questions OQ-S219-* (any new at authoring) recorded | OQ table inspection |
| Forward routing to S2.20 declared with entry preconditions | §7 forward routing section present |

---

## §7 — Empirical anchor inheritance at S2.19 entry

The following anchors carry forward to T.2 GRACE entry. Reduced inheritance scope vs T.2 ROME (ROME inherited covariance caches + Copy-Unmount; GRACE does not).

| Anchor | S2.19 inheritance | Source | Notes |
|---|---|---|---|
| Cross-session bit-exact determinism | 6 checkpoints; drift `0.00e+00` | D-S217-4 + D-S218-7 | Held for any GRACE forward pass at canonical hparam regime against same model SHA |
| `meta-llama/Llama-3.1-8B` revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` | LOCKED | S2.13-C through S2.18 cumulative | Held verbatim |
| `cfb-v3.yaml` v1.0 corpus | LOCKED | S2.13-C | Held verbatim |
| `probe-set-v3.yaml` v1.0 (38 active probes) | LOCKED | S2.13-C | Held verbatim |
| IC-S24-4 trial protocol (5 facts × 3 replicates = 15 trials) | LOCKED | S2.4 series | Held; GRACE multi-fact dispatch semantics may differ — re-evaluated at S2.20 Block B |
| Acceptance bands (`0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount) | LOCKED | D-S24-10 + IC-S23-4 | Held; re-evaluate if GRACE adapter dispatch produces different probability surface shapes |
| D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset | LOCKED | S2.15-D2 | Held verbatim |
| MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism | CODIFIED at v1.7 | D-V12-MULTITOKEN-1 | Cell 6 / Cell 7 / Cell 9 absorption inherits via parallel pattern |
| Pad-Token applicability | LIKELY APPLICABLE | memit-patches-canonical v2.5 + rome-patches-canonical v0.2 §1.1 | Engine-agnostic tokenizer-side; carry-forward |
| Copy-Unmount mechanism | INAPPLICABLE | t_branch_decision_document v1.1 §6'.2 | GRACE adapter mechanism does not modify base weights in-place |
| Covariance caches L2-L8 + L17 | INAPPLICABLE | t_branch_decision_document v1.1 §6'.3 | GRACE adapter mechanism does not consume layer_stats |
| Cell 13 3-route verdict gate framework | CODIFIED at t2_rome v0.2 | empirically anchored at S2.18 | Inherited unchanged at t2_grace v0.1 Cell 13 |

---

## §8 — Anticipated open questions at v0.1 authoring

The following OQs are likely to surface during v0.1 authoring; closure paths declared upfront.

| OQ ID | Surface | Closure path |
|---|---|---|
| OQ-V11-T-BRANCH-1 | GRACE SHA pin selection | Q1 resolution at session close |
| OQ-V11-T-BRANCH-2 | GRACE canonical hparams for Llama-3.1-8B | Q2 resolution at session close |
| OQ-V11-T-BRANCH-3 | GRACE adapter placement at Llama-3.1-8B | Q3 resolution at session close |
| OQ-V11-T-BRANCH-4 | Multi-token tolerance posture for cfb-v3-004 under GRACE | Q5 resolution at session close (carry-forward declarative; re-evaluate at S2.20) |
| OQ-V11-T-BRANCH-5 | GRACE unmount mechanism canonical specification | Q4 resolution at session close |
| **OQ-S219-1** (likely NEW) | GRACE adapter mechanism may use retain-trace pattern (P-1 / P-2 carry-forward applicability resolution) | Resolved at v0.1 authoring per actual GRACE codebase inspection at Block 1 §1.1 |
| **OQ-S219-2** (likely NEW) | GRACE may have a CONFIG_LAYER analog (globals.yml-equivalent or similar) | Resolved at v0.1 authoring per actual GRACE repo inspection at Block 1 §1.6 |
| **OQ-S219-3** (likely NEW) | GRACE multi-fact dispatch semantics: single-fact-per-trial OR adapter-accumulation across trials | Resolved at v0.1 authoring per GRACE paper §X / supplementary; declarative at v0.1; empirical at S2.20 Cell 15 |
| **OQ-S219-4** (likely NEW) | GRACE Cell 3 disposition: INAPPLICABLE-DEFERRED-BY-MECHANISM OR replace with adapter-pool initialization verification | Resolved at v0.1 authoring per Q5 disposition |

---

## §9 — Scope guards (operator-side)

Per kickoff §6.1 of the v0.2 codification session: this session is **operator-side spec authoring**. The scope guards below are non-negotiable:

1. **No pod-side execution.** No RunPod attach, no NV interaction, no live tool calls against pod resources. v0.1 is authoring-acceptance only; first-execution at S2.20.
2. **No live GRACE codebase inspection at this session.** Reference GRACE paper + supplementary + repo via static read; do not clone or execute. Empirical patch authoring deferred to S2.20 Block A first-execution (parallel to S2.18 ROME pattern where P-7-ROME / P-8-ROME / P-9-ROME were authored mid-execution).
3. **No modification of v0.2 codification deliverables.** rome-patches-canonical v0.2, t2_rome_runbook v0.2, stage_1_sect_runbook v1.7, framework_finding_memit_ceiling_archival v1.1, t_branch_decision_document v1.1 are RATIFIED; preserved verbatim.
4. **No modification of memit-patches-canonical v2.5.** Sibling-parity discipline preserved.
5. **No amendment of v1.0 PERMANENT artifacts.** framework_finding_memit_ceiling_archival v1.0 + t_branch_decision_document v1.0 inherited via v1.1 amendments only.
6. **Sibling-parity discipline.** grace-patches-canonical v0.1 + t2_grace_runbook v0.1 are parallel siblings; do not amend ROME or MEMIT canonicals; coexist in /mnt/user-data/outputs/ alongside them.
7. **Three coexisting write-engine canonicals after S2.19 close.** memit-patches-canonical v2.5 (preserved unmodified; no further work scheduled) + rome-patches-canonical v0.2 (preserved post-elimination as historical record + carry-forward) + grace-patches-canonical v0.1 (active forward-target).

---

## §10 — Forward routing post-S2.19 close

### §10.1 Immediate next session — S2.20 = T.2 GRACE Stage 1 SECT v3 execution

**Session class:** Pod-side execution session (parallel to S2.18 = T.2 ROME execution).
**Inputs from S2.19:** grace-patches-canonical v0.1 + t2_grace_runbook v0.1 + S2.19 summary block.
**Pod resources:** RunPod RTX 4090 24 GiB; NV `large_amethyst_wolverine`.
**Verdict surface:** Block B Cell 13 3-route option matrix adjudication; Block C trial loop conditional on Cell 13 routing.

### §10.2 Conditional successor sessions per `t_branch_decision_document.md` v1.1 §5'

- **S2.20 GRACE PASS** → ceiling is rank-1-in-weight-class-mechanism-specific; adapter-based mechanism viable on Llama-3.1-8B; S2.21 = MEMIT-vs-ROME-vs-GRACE comparison framework finding update (resolves OQ-V11-T-BRANCH-6); Workstream 2 / 3 implementation planning informed
- **S2.20 GRACE FAIL** → suspect (model × hparams) — ceiling generalizes to adapter mechanisms too → FALL BACK TO T.1 alt model → S2.21 = T.1 alt-model runbook v0.1 authoring (parallel structure to S2.19; reuses MEMIT + cfb-v3 + canonical hparams; alt model = Llama-3.2-3B / Mistral-7B / Qwen-7B)
- **S2.20 PARTIAL** → operator-side verdict integrity binding re-evaluation per t_branch_decision_document v1.0 §5

### §10.3 v0.2 codification analog (post-S2.20)

If S2.20 surfaces empirical patches mid-execution (parallel to S2.18 P-7-ROME / P-8-ROME / P-9-ROME pattern), a v0.2 codification session analog would be scheduled post-S2.20: grace-patches-canonical v0.2 + t2_grace_runbook v0.2 + (potentially) framework_finding_memit_ceiling_archival v1.2 + t_branch_decision_document v1.2. This is forward-conditional and out of scope at S2.19 entry.

---

## §11 — Authoring metadata

| Field | Value |
|---|---|
| Kickoff prompt authoring session | v0.2 codification session (operator-side post-S2.18; this kickoff prompt is authored at session close) |
| Kickoff prompt date | 2026-05-05 |
| Kickoff prompt version | 1.0 (instantiates verdict-conditional template C-FAIL branch from `session_2_19_kickoff_prompt.md` template authored at S2.17) |
| Status | RATIFIED at v0.2 codification session close |
| Predecessor | v0.2 codification session deliverables (D1-D6) |
| Workstream | WS1 |
| Specialist provenance | framework-spec-writer (kickoff prompt authoring); memit-specialist + state-consistency-theorist + orchestration-comparativist + graph-data-architect + validation-contract-architect (consultative for §2 specialist routing + §4 block scope + §5 Q1-Q5 design questions) |

---

*End of S2.19 kickoff prompt — T.2 GRACE runbook v0.1 authoring (C-FAIL branch active per t_branch_decision_document v1.1 §5' empirical resolution; parallel structure to S2.17 Block 2 ROME runbook authoring; sibling-parity discipline preserved across three coexisting write-engine canonicals + runbooks at session close).*
