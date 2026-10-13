# T-Branch Decision Document — T.2 ROME ELIMINATED at Canonical; T.2 GRACE PROMOTED (v1.1 amendment of v1.0)

> **Artifact type:** Decision document — load-bearing forward-routing artifact (v1.1 additive amendment of v1.0)
> **Status:** RATIFIED v1.1 — load-bearing; additive amendment of v1.0; v1.0 PERMANENT integrity preserved (decision-record class)
> **Supersedes:** — (additive amendment; v1.0 forward-routing claims preserved verbatim alongside v1.1; v1.0 retained as the load-bearing original record)
> **Authored:** 2026-05-04 (v1.0 within S2.16); 2026-05-05 (v1.1 amendment within v0.2 codification session post-S2.18)
> **Predecessor (v1.0):** `framework_finding_memit_ceiling_archival.md` v1.0 (S2.16 deliverable #1)
> **Predecessor (v1.1):** `framework_finding_memit_ceiling_archival.md` v1.1 (v0.2 codification session deliverable; parallel to this artifact)
> **Successor (v1.0):** `t2_rome_runbook_v0_1_authoring_plan.md` (S2.16 deliverable #3); subsequently superseded by `t2_rome_runbook_v0_1.md` at S2.17, then by `t2_rome_runbook.md` v0.2 at v0.2 codification session
> **Successor (v1.1):** S2.19 = T.2 GRACE runbook v0.1 authoring (verdict-conditional C-FAIL branch active per `session_2_19_kickoff_prompt.md`)
> **Specialist provenance:** memit-specialist (primary; ROME elimination empirical record analysis, GRACE promotion rationale, mechanism comparison rank-1-in-weight vs adapter-based); state-consistency-theorist (secondary; Copy-Unmount inapplicability under GRACE adapter mechanism; cross-session determinism inheritance); orchestration-comparativist (write-engine architecture comparison surface; v1.1 GRACE foreground); graph-data-architect (light-touch; framework-spec-relevance scoring for adapter-based mechanisms — strengthened at v1.1); framework-spec-writer (formalization; v1.0 integrity preservation discipline)
> **Workstream:** WS1 (empirical execution; T.2 ROME closed; T.2 GRACE entry forthcoming at S2.19)

---

## §0 — v1.1 amendment scope and integrity declaration

### §0.1 v1.1 amendment scope

v1.1 is a **strictly additive amendment** of v1.0. The v1.0 decision (T-branch path: T.2 alt write engine; ROME first; escalate to GRACE on FAIL or fall back to T.1 on FAIL+T.1-trigger) is preserved unmodified. v1.1 absorbs the empirical record from S2.18 — the first T.2 ROME execution at canonical hparams against the target model — and makes the following additions:

1. **§1' decision statement updated** for the post-S2.18 routing state: T.2 ROME ELIMINATED at canonical hparams (S2.18 D-S218-3); T.2 GRACE PROMOTED to leading T-branch hypothesis (D-S218-4); v1.0's "ROME first; escalate to GRACE on FAIL" pre-commitment empirically ratified — escalation path activated
2. **§4' write engine selection updated**: T.2 ROME row resolves OPEN → ELIMINATED at canonical; T.2 GRACE row resolves OPEN → PROMOTED active leading hypothesis with S2.19 routing target
3. **§5' conditional execution plan resolved**: the C-FAIL branch (Block C consistency band failure) is the active path post-S2.18; v1.1 records the routing decision and the next-session disposition
4. **§6' methodology lock for T.2 GRACE** (new section parallel to v1.0 §6 ROME methodology lock): inheritance scope reduced relative to ROME because GRACE adapter-based mechanism is structurally distinct from rank-1 in-weight write engines; covariance caches inapplicable; Copy-Unmount inapplicable; subset of patches inapplicable
5. **§8' open questions** — closes v1.0 OQ-S216-1 / OQ-S216-2 / OQ-S216-3 / OQ-S216-4 / OQ-S216-5 (resolved at S2.17 / S2.18); preserves v1.0 OQ-S216-6 dispositional update (resolution context shifted from "if T.2 ROME PASSES" to "T.2 ROME did not PASS at canonical; comparison surface collapses; both engines hit ceiling")
6. **§10' references updated** for v1.1 successor artifacts (rome-patches-canonical v0.2, t2_rome_runbook v0.2, framework_finding_memit_ceiling_archival v1.1, S2.18 summary blocks)

The v1.1 amendment **preserves all v1.0 §1-§11 content verbatim** as load-bearing PERMANENT decision-record. v1.1 surfaces deltas at corresponding section numbers with the suffix `'` (e.g., §1' is the v1.1 amendment to v1.0 §1's decision statement). Where v1.0 made a forward-conditional decision (e.g., "ROME first; escalate to GRACE on FAIL"), v1.1 records the empirical disposition of that decision (T.2 ROME tested; ELIMINATED; escalation activated).

### §0.2 v1.0 integrity preservation

v1.0 is the **original load-bearing decision document** authored at S2.16. v1.0 §1-§11 contain the decision statement, T-branch options surveyed, operator rationale for T.2 over T.1 / T.3, write engine selection (ROME first), conditional execution plan, methodology lock for T.2 ROME, pre-commitment items for runbook authoring, open questions, non-goals, references, and authoring metadata. Each section is decision-record-class — they document the decision made at the v1.0 close; their truth-value as decisions-at-time is not affected by subsequent empirical events.

v1.1 does NOT:
- Edit any v1.0 §1-§11 sentence
- Reverse any v1.0 decision (the decisions remain on record as decisions-at-the-time)
- Withdraw any v1.0 §3 carry-forward preservation argument (the argument was sound at v1.0; the empirical execution of T.2 ROME validated the carry-forward inheritance even though the verdict eliminated the hypothesis)
- Modify any v1.0 reference, decision ID, interface contract, or repository pin

v1.1 layers on top of v1.0 as a parallel artifact. Operators consuming the T-branch decision in successor sessions read both v1.0 (load-bearing original) and v1.1 (amendment additions). The pair `(v1.0, v1.1)` constitutes the complete decision state at v1.1 close.

### §0.3 Reference to v1.0

For all §1-§11 v1.0 content, see `t_branch_decision_document.md` v1.0 (preserved at NV mirror or git reference). v1.1 below references v1.0 sections by number.

---

## §1' — Decision statement amendment (extends v1.0 §1)

**v1.0 decision statement (preserved):**
> T-branch path: T.2 (alt write engine).
> Write engine: ROME first; escalate to GRACE on FAIL or fall back to T.1 on FAIL+T.1-trigger.
> Pre-commitment per D-S215D2-4 confirmed with empirical evidence in hand at S2.16 entry.

**v1.1 amendment:** S2.18 first-execution of T.2 ROME at canonical hparams produced verdict B-FAIL (Cell 13 verdict gate adjudicated as Route A halt; both layer candidates L17 + L2 FAIL the calibration corridor with diagnostic-distinct pathologies). T.2 ROME ELIMINATED at canonical hparams per D-S218-3; the architectural-invariant ceiling extends from `(Llama-3.1-8B × MEMIT × canonical hparams)` to `(Llama-3.1-8B × {MEMIT, ROME} × canonical hparams)` per `framework_finding_memit_ceiling_archival.md` v1.1 §1' (Axis 7 added).

**v1.1 amended decision statement:**
> T-branch path: T.2 (alt write engine) — REMAINS ACTIVE; ROME-side branch closed.
> Write engine: T.2 ROME ELIMINATED at canonical hparams (S2.18); T.2 GRACE PROMOTED to leading T-branch hypothesis (D-S218-4).
> Escalation path activated per v1.0 §5 conditional execution plan C-FAIL branch; T.1 alt model retains as fallback if T.2 GRACE FAILS.

**Empirical anchor.** S2.18 Block B verdict at cfb-v3-001 (Bo Jackson / guitar; sharpest IN-BAND anchor per S2.13-C calibration):
- L17 (ROME paper precedent): post-edit P(guitar) = `8.26e-03`; pathology = degenerate-fit (BOS-collapse on rewrite-shape prompt; post-edit cons-1 top_1 = `<|begin_of_text|>` P=0.924); compute_v loss 18.17→4.93 monotonic decrease
- L2 (S2.14-D D.1 mediation peak): post-edit P(guitar) = `1.06e-06`; pathology = unfittable-landscape; compute_v loss 13.49-19.26 oscillating non-converging across 20 iterations

Both readings well below consistency band `0.5`; both within v1.0 §2 ceiling envelope `[1e-7, 2.2e-2]`. Specificity preserved at both layers (gen probes top_1 unchanged; max P drift < 0.020). Unmount band PASS at both (drift `0.00e+00` per IC-S23-4). The FAIL is decisive on the consistency surface specifically — paralleling the MEMIT FAIL pattern across all six v1.0 axes.

**v1.0 forward-conditional disposition resolved.** v1.0 §5 conditional execution plan declared: "ROME FAIL → Author GRACE runbook v0.1 (S2.19); execute Stage 1 SECT v3 (S2.20)". v1.1 records: this branch is the active forward path post-S2.18. S2.19 = T.2 GRACE runbook v0.1 authoring is the next session per `session_2_19_kickoff_prompt.md` (verdict-conditional C-FAIL branch active).

---

## §4' — Write engine selection amendment (extends v1.0 §4)

**v1.0 §4 ROME first decision (preserved):** ROME selected as first T.2 candidate per memit-specialist meta-recommendation; rationale: closest mechanistic comparison (parent of MEMIT; shared codebase ancestry); lowest patches surface; single-fact / single-layer test surface yields cleanest verdict.

**v1.1 amendment:** S2.18 empirically executed the v1.0 ROME-first commitment. The execution itself confirmed v1.0's carry-forward preservation argument (target model bit-exact, covariance caches reusable, Copy-Unmount mechanism preserved single-fact-narrowed) — but the verdict eliminated ROME as the leading hypothesis. v1.1 records the post-S2.18 candidate matrix:

### §4'.1 Post-S2.18 candidate disposition matrix

| Engine | v1.0 disposition | v1.1 disposition (post-S2.18) | Cost class | Rationale |
|---|---|---|---|---|
| **ROME** | OPEN — leading per memit-specialist meta-recommendation | **ELIMINATED at canonical hparams (S2.18; D-S218-3)** | (closed) | Architectural-invariant ceiling extends to ROME single-fact rank-1 update on Llama-3.1-8B at canonical hparams; both candidate layers L17 + L2 FAIL with diagnostic-distinct pathologies |
| **GRACE** | OPEN — fallback to ROME | **PROMOTED to leading T-branch hypothesis (D-S218-4)** | HIGH (~2-4 sessions; runbook v0.1 authoring + execution + verdict + analysis) | Adapter-based mechanism is orthogonal to rank-1 weight update; ceiling claim does NOT transitively cover GRACE; strongest framework-spec relevance per v1.0 §3.3 carry-forward preservation argument |
| MEND | (deferred at v1.0) | DEFERRED — not currently scheduled | (forward-conditional) | If T.2 GRACE FAILS, MEND may be considered alongside T.1; if T.2 GRACE PASSES, MEND may not be tested |
| SERAC | (deferred at v1.0) | DEFERRED — not currently scheduled | (forward-conditional) | Same as MEND; framework-spec divergent (retrieval-augmented; not pure parametric memory); lower priority |

### §4'.2 GRACE selection rationale (v1.1)

GRACE (General Adapter for Continual Editing) is the leading T.2 candidate post-S2.18 for three reasons:

1. **Mechanism orthogonality.** v1.0 §3.1 argued T.2 over T.1 because the suspect locus is inside MEMIT's z-vector update geometry. S2.18 ROME extension shows the suspect locus is inside the RANK-1 IN-WEIGHT update class — both MEMIT (multi-fact rank-1) and ROME (single-fact rank-1) hit the ceiling. GRACE adapter-based mechanism is structurally distinct: adapters add parameters; routing-layer dispatch consumes them at forward pass; the base model weights are NOT modified in-place. The ceiling claim's structural extension does not cover GRACE because GRACE does not implement the suspect mechanism class.

2. **Framework-spec relevance.** Per v1.0 §3.3 carry-forward preservation argument and §5.3 v1.0 framework-spec implications: adapter-based mechanisms are closer to the `.vindex` overlay model (the framework's canonical parametric-memory architecture). If GRACE PASSES on Llama-3.1-8B at canonical hparams, the empirical result is informative for Workstream 2 / 3 implementation planning — not just for the immediate ceiling-elimination question.

3. **Cost-information ratio.** GRACE is HIGH-cost (~2-4 sessions) but high-information: GRACE PASS resolves both the ceiling question (it's a rank-1-in-weight-class limitation) and the framework-fit question (adapter-based engines are viable on Llama-3.1-8B). GRACE FAIL is the strongest signal for FALL-BACK-TO-T.1 (the ceiling generalizes to adapter mechanisms too; suspect is `(model × hparams)` rather than write-engine class).

### §4'.3 GRACE entry preconditions (v1.1)

For S2.19 = T.2 GRACE runbook v0.1 authoring, the following are pre-committed:

1. **Repository.** `https://github.com/Thartvigsen/GRACE` (per v1.0 §4.1 repo reference; SHA pin selection deferred to S2.19 entry per v0.1 authoring scope).
2. **Sibling-parity discipline.** Author `grace-patches-canonical.md` v0.1 as a parallel sibling to `memit-patches-canonical.md` v2.5 and `rome-patches-canonical.md` v0.2. Do NOT amend either MEMIT or ROME canonical. Three sibling write-engine canonicals coexist post-S2.19: MEMIT v2.5 (preserved; no further work scheduled), ROME v0.2 (preserved post-elimination as historical record + carry-forward for any future re-entry), GRACE v0.1 (active).
3. **Inheritance from MEMIT v2.5 / ROME v0.2.** v1.0 §6.3 empirical anchors carry forward to GRACE with reduced inheritance scope (see §6' below).
4. **Block-and-Cell runbook structure.** `t2_grace_runbook.md` v0.1 inherits the three-block structure (Block A pre-flight + Block B HC-2-equivalent dry-run + Block C trial loop) parallel to t2_rome_runbook v0.1. Block-and-Cell discipline preserved.
5. **GRACE adapter mechanism specification.** GRACE adapter-rank, routing-threshold, memory-pool-size hparams are GRACE-paper-specific; no inheritance from MEMIT/ROME hparam surface. v0.1 authoring derives from GRACE paper / supplementary Table 1.
6. **GRACE unmount mechanism specification.** GRACE adapter modules add parameters rather than modify base weights in-place; Copy-Unmount mechanism (in-place weight tensor restore) is INAPPLICABLE. GRACE unmount = remove adapter from routing layer; restore base model state by detaching adapter. v0.1 authoring derives the canonical unmount semantics per GRACE paper.
7. **Multi-token target tolerance.** D-S215D2-CFB-V3-004-PROXY-1 first-token-proxy methodology may not apply to GRACE; re-evaluate at trial 0.

---

## §5' — Conditional execution plan resolution (extends v1.0 §5)

**v1.0 §5 conditional execution plan (preserved):**

```
S2.16 (this session)  →  S2.17 (T.2 ROME runbook v0.1 authoring + Block B HC-2-equivalent dry-run)
                              ↓
                          S2.18 (T.2 ROME Stage 1 SECT v3 execution)
                              ↓
                         ┌── PASS → ...
                         │
                         ├── FAIL → Author GRACE runbook v0.1 (S2.19); execute Stage 1 SECT v3 (S2.20)
                         │           ├── GRACE PASS  → ...
                         │           └── GRACE FAIL  → FALL BACK TO T.1
                         │
                         └── PARTIAL → ...
```

**v1.1 amendment: empirical resolution of the conditional plan.**

The S2.18 execution resolved the v1.0 plan at the FAIL branch. v1.1 records the empirical trajectory:

```
S2.16 → S2.17 → S2.18 (T.2 ROME execution)
                  ↓
                FAIL — verdict B-FAIL at Cell 13 verdict gate; Route A halt selected
                  ↓
              (v1.0 plan §5 FAIL branch active)
                  ↓
              ┌── v0.2 codification session (this; operator-side; pre-S2.19 BLOCKING)
              │      Deliverables: rome-patches-canonical.md v0.2; t2_rome_runbook.md v0.2;
              │                    stage_1_sect_runbook_v1_7.md (MEMIT-side retroactive miss);
              │                    framework_finding_memit_ceiling_archival.md v1.1 (this artifact's predecessor);
              │                    t_branch_decision_document.md v1.1 (this artifact);
              │                    session_v0_2_codification_summary_block.md (session close)
              │
              └── S2.19 (T.2 GRACE runbook v0.1 authoring)
                    │
                    └── S2.20 (T.2 GRACE Stage 1 SECT v3 execution)
                          ├── GRACE PASS  →  Ceiling is rank-1-in-weight-class-mechanism-specific;
                          │                  adapter-based mechanism viable on Llama-3.1-8B
                          │
                          └── GRACE FAIL  →  Suspect (model × hparams) — ceiling generalizes
                                              to adapter mechanisms too
                                              ⇒ FALL BACK TO T.1 (alt model on Llama-3.2-3B / Mistral-7B)
                                              ⇒ S2.21 = T.1 alt-model runbook v0.1 authoring
```

**Operator disposition.** The C-FAIL branch is the active forward path. v1.1 publication completes the operator-side pre-S2.19 BLOCKING work; S2.19 is unblocked for entry post v0.2 codification session close.

---

## §6' — Methodology lock for T.2 GRACE (NEW at v1.1; parallel to v1.0 §6 ROME methodology lock)

### §6'.1 Locked from carry-forward (held constant from S2.13-C / S2.15-D2 / S2.18)

| Axis | Lock | T.2 GRACE inheritance |
|---|---|---|
| Target model | `meta-llama/Llama-3.1-8B` revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` | YES — bit-exact carry-forward (6 cross-session checkpoints; D-S217-4 + D-S218-7) |
| Stage 1 SECT corpus | `cfb-v3.yaml` v1.0 (5 facts) | YES — held verbatim |
| Probe set | `probe-set-v3.yaml` v1.0 (38 active probes) | YES — held verbatim |
| Trial protocol | IC-S24-4: 5 facts × 3 replicates = 15 trials | YES — held; though GRACE multi-fact dispatch semantics may differ (adapter accumulation vs single-fact-per-trial) |
| Acceptance bands | `0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount | YES — held (re-evaluate if GRACE adapter dispatch produces different probability surface shapes; expected to hold since acceptance bands are model-agnostic) |
| Verdict integrity binding | D-S215D2-VERDICT-INTEGRITY-1: load-bearing subset = {cfb-v3-001, cfb-v3-002, cfb-v3-005} | YES — held verbatim |

### §6'.2 Re-derived at T.2 GRACE entry

| Axis | Re-derivation |
|---|---|
| Engine mechanism | GRACE = adapter-based memory; routing-layer dispatch; key-value adapter blocks. Structurally distinct from MEMIT/ROME rank-1 in-weight mechanism. |
| Layer set | GRACE adapters are inserted at specific layer positions (per GRACE paper canonical placement). For Llama-3.1-8B, candidate placements derived from GRACE paper (originally GPT2-XL / GPT-J reference architectures); Llama-specific adaptation deferred to runbook v0.1 |
| Hparams | GRACE has its own hparam surface: adapter-rank, routing-threshold, memory-pool-size, learning-rate. No inheritance from MEMIT/ROME hparam surface. Reference: GRACE paper Table 1 starting values |
| Multi-token target tolerance | GRACE multi-token handling may differ from MEMIT/ROME; D-S215D2-CFB-V3-004-PROXY-1 first-token-proxy methodology re-evaluated at trial 0 |
| Patches | Re-derive against Llama-3.1-8B + GRACE repo. Patches likely applicable from MEMIT/ROME: P-1, P-2 (nethook retain pattern; if GRACE uses any retain-trace for adapter forward pass — open question for v0.1), Pad-Token (tokenizer-side; engine-agnostic). Patches inapplicable: P-4, P-5, P-6, P-7-ROME, P-8-ROME, P-9-ROME (all relate to covariance / projection / outer-product mechanism not used by GRACE). globals.yml CONFIG_LAYER customization may apply if GRACE shares the same config-loading idiom (open question for v0.1). |
| Unmount mechanism | INAPPLICABLE Copy-Unmount (in-place weight restore). GRACE unmount specification authored fresh at v0.1: detach adapter from routing layer; restore base-model forward-pass behavior |
| Covariance caches | INAPPLICABLE — GRACE adapter mechanism does not consume layer_stats covariance caches |

### §6'.3 Empirical anchors carry-forward

| Anchor | Status | T.2 GRACE inheritance |
|---|---|---|
| Cross-session bit-exact determinism (6 checkpoints; D-S217-4 + D-S218-7) | LOCKED | Inherits — same target model SHA |
| Copy-Unmount bit-exact regime (L4-L8 + L2-L6 + L17 + L2 single-fact) | LOCKED at v1.1 | INAPPLICABLE — adapter-based mechanism does not modify base weights in-place |
| Covariance caches L2-L8 + L17 (~6.5 GB durable on NV) | LOCKED | INAPPLICABLE — adapter mechanism does not consume layer_stats |
| `stage_1_sect_runbook_v1_5/v1.6/v1.7` runbook structure | Reference | T.2 GRACE runbook v0.1 inherits cell structure (Block A / Block B / Block C); cell-by-cell adaptation per GRACE adapter dispatch; multi-token allowlist canonical mechanism inherited via v1.7 absorption |
| `rome-patches-canonical.md` v0.2 sibling-parity pattern | Reference | T.2 GRACE patches canonical follows the same parallel-sibling discipline; does not amend MEMIT or ROME canonical |
| `t2_rome_runbook.md` v0.2 cell structure + 3-route Cell 13 verdict gate framework | Reference | T.2 GRACE runbook v0.1 inherits 3-route option matrix at Block B verdict gate; Cell 13 adjudication framework directly applicable |

---

## §8' — Open questions amendment (extends v1.0 §8)

### §8'.1 v1.0 OQs closed by S2.17 / S2.18

| OQ | v1.0 status | v1.1 closure |
|---|---|---|
| **OQ-S216-1** | OPEN — ROME SHA pin selection | **CLOSED at S2.18 Block A Cell 1; SHA = `0874014cd9837e4365f3e6f3c71400ef11509e04` (latest stable tip per D-S217-Q2-1)** |
| **OQ-S216-2** | OPEN — ROME canonical hparams | **CLOSED at v0.2 codification — canonical hparams per ROME paper Table 1 GPT-J reference values + Llama adaptation; calibration corridor not surfaced at L17 OR L2 per Route A halt** |
| **OQ-S216-3** | OPEN — Layer-set candidates | **CLOSED at S2.17 D-S217-Q4-1: L17 primary + L2 secondary; both tested at Block B; both FAIL** |
| **OQ-S216-4** | OPEN — Multi-token tolerance posture for cfb-v3-004 | **CLOSED at S2.17 D-S217-Q5-1 first-token-proxy carry-forward + RE-EVALUATE flag; subsequently Block C did not execute at S2.18, so RE-EVALUATE not exercised; posture remains DECLARED-via-v0.2** |
| **OQ-S216-5** | OPEN — v1.6 hardening session scheduling | **CLOSED — v1.6 hardening completed at S2.17 Block 1 dedicated session; subsequently superseded by v1.7 at v0.2 codification session per MULTI_TOKEN_ALLOWLIST canonical absorption** |
| **OQ-S216-6** | OPEN — comparison framework finding update | **DISPOSITION SHIFTED — v1.0 framing was "if T.2 ROME PASSES, what artifact captures the MEMIT-vs-ROME comparison framework finding update?" S2.18 verdict B-FAIL means the comparison surface collapses (both engines hit ceiling); the framework finding extension is the v1.1 archival amendment (§4.3' patches table + §1' ceiling scope extension) — closes via amendment rather than via comparison artifact** |

### §8'.2 v1.1 OQs activated / opened

| OQ | Surface | Status | Closure path |
|---|---|---|---|
| **OQ-V11-T-BRANCH-1** | T.2 GRACE runbook v0.1 SHA pin selection | OPEN | Resolved at S2.19 entry |
| **OQ-V11-T-BRANCH-2** | T.2 GRACE canonical hparams for Llama-3.1-8B: inherit GRACE paper reference values OR Llama-specific calibration sweep at runbook v0.1? | OPEN | Resolved at S2.19 / S2.20 HC-2-equivalent dry-run verdict |
| **OQ-V11-T-BRANCH-3** | T.2 GRACE adapter placement at Llama-3.1-8B: inherit GRACE paper canonical placement (e.g., transformer-mid layer) OR Llama-specific adaptation? | OPEN | Resolved at S2.19 runbook v0.1 authoring |
| **OQ-V11-T-BRANCH-4** | T.2 GRACE multi-token tolerance posture for cfb-v3-004 harp | OPEN | Resolved at S2.20 trial 0 of Block B HC-2-equivalent dry-run |
| **OQ-V11-T-BRANCH-5** | T.2 GRACE unmount mechanism canonical specification (parallel to MEMIT/ROME Copy-Unmount discipline) | OPEN | Resolved at S2.19 runbook v0.1 authoring |
| **OQ-V11-T-BRANCH-6** | If T.2 GRACE PASSES, what artifact captures the rank-1-in-weight-vs-adapter comparison framework finding update? | OPEN | Resolved post-S2.20 verdict |

### §8'.3 v1.1 OQs explicitly out of scope

| OQ | Reason |
|---|---|
| OQ-S218-1 / OQ-S218-2 / OQ-S218-3 | ROME-class diagnostic OQs; not load-bearing for T-branch decision document; deferred informational |
| MEND / SERAC entry questions | DEFERRED per §4'.1 candidate matrix; not active hypotheses |

---

## §9' — Non-goals amendment (extends v1.0 §9)

**v1.0 non-goals (preserved):** Does not author the T.2 ROME runbook v0.1; does not commit to specific ROME hparam values; does not author runtime implementation code; does not pre-judge T.2 ROME verdict; does not modify framework spec v1.2; does not foreclose T.1 / T.3 paths.

**v1.1 amendment:** v1.1 also does not:

1. **Modify v1.0 §1-§11.** v1.0 PERMANENT decision-record integrity preserved verbatim.
2. **Author the T.2 GRACE runbook v0.1.** That is the scope of S2.19 = T.2 GRACE runbook v0.1 authoring (forthcoming).
3. **Commit to specific GRACE hparam values.** GRACE hparam surface re-derived at runbook v0.1 authoring per §6'.2.
4. **Pre-judge T.2 GRACE verdict.** The verdict surface at S2.20 is empirical; v1.1 commits to GRACE-as-leading-T-branch hypothesis post-ROME-elimination, not to GRACE PASS or FAIL.
5. **Foreclose T.1 / T.3 paths.** T.1 retains as fallback per §5' if T.2 GRACE FAILS. T.3 remains a multi-session post-WS1 redesign option if both T.2 GRACE and T.1 fail.
6. **Reverse the T.2 ROME elimination.** S2.18 verdict B-FAIL → T.2 ROME ELIMINATED at canonical hparams is a load-bearing empirical record. v1.1 does not propose T.2 ROME re-execution at non-canonical hparams (calibration sweep at L17 / L2 with weakened acceptance bands) within WS1 scope.
7. **Author the framework finding archival v1.1.** That is a parallel deliverable in v0.2 codification session (`framework_finding_memit_ceiling_archival.md` v1.1).

---

## §10' — References amendment (extends v1.0 §10)

### §10.1' — Predecessor artifacts (NEW additions)

- `framework_finding_memit_ceiling_archival.md` v1.1 (v0.2 codification session deliverable; extends v1.0 with Axis 7 + ceiling scope extension to {MEMIT, ROME})
- `session_2_18_summary_block.md` — T.2 ROME execution close artifact; B-FAIL verdict
- `session_2_18_summary_block_appendix.md` — forensic detail (Block A trajectory, patch authoring, compute_v traces, verdict tables)
- `session_2_17_summary_block.md` — v1.6 hardening + T.2 ROME runbook v0.1 authoring close artifact
- `session_2_19_kickoff_prompt.md` — verdict-conditional kickoff template; C-FAIL branch active

### §10.2' — Decision IDs (v1.1 additions)

- D-S218-1 — Cell 13 verdict gate B-FAIL adjudication
- D-S218-2 — Route A halt selection
- D-S218-3 — T.2 ROME ELIMINATED at canonical hparams
- D-S218-4 — T.2 GRACE PROMOTED to leading T-branch hypothesis
- D-S218-7 — Cross-session bit-exact determinism 5 → 6 checkpoint extension
- D-S218-8 — Copy-Unmount validated for ROME single-fact L17 + L2
- D-S218-12 — v1.1 framework finding archival amendment ratified
- D-S218-13 — v1.1 t-branch decision document amendment ratified (this artifact)
- D-V11-T-BRANCH-1 (NEW at v1.1) — T.2 GRACE leading post-ROME-elimination
- D-V11-T-BRANCH-2 (NEW at v1.1) — Sibling-parity discipline preserved for grace-patches-canonical.md v0.1 authoring at S2.19
- D-V11-T-BRANCH-3 (NEW at v1.1) — Mechanism-orthogonality argument: rank-1 in-weight class FAILED at canonical (MEMIT + ROME); adapter-based class is the next test surface

### §10.3' — Repository references (v1.1 additions)

- ROME (now post-elimination historical reference): `https://github.com/kmeng01/rome` SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04` (resolved at S2.18 Block A Cell 1; recorded for any future re-entry)
- GRACE (active forward target): `https://github.com/Thartvigsen/GRACE` (SHA pin selection deferred to S2.19 entry)

### §10.4' — Sibling artifacts (v1.1 additions)

- `rome-patches-canonical.md` v0.2 — ROME patches reference (parallel sibling to MEMIT v2.5; preserved post-elimination as historical record + carry-forward for any future ROME re-entry)
- `t2_rome_runbook.md` v0.2 — ROME runbook (post-S2.18 empirical absorption)
- `stage_1_sect_runbook_v1_7.md` — MEMIT runbook v1.7 (MULTI_TOKEN_ALLOWLIST canonical absorption)
- `grace-patches-canonical.md` v0.1 (forthcoming at S2.19) — GRACE patches reference (parallel sibling to MEMIT v2.5 + ROME v0.2)
- `t2_grace_runbook.md` v0.1 (forthcoming at S2.19) — GRACE runbook (parallel structure to t2_rome_runbook v0.2)

---

## §11' — Authoring metadata (v1.1)

| Field | Value |
|---|---|
| Authoring session | v0.2 codification session (operator-side post-S2.18; pre-S2.19 BLOCKING) |
| Authoring date | 2026-05-05 |
| Document version | 1.1 |
| Iteration | v1.1 additive amendment (preserves v1.0 PERMANENT decision-record integrity) |
| Status | RATIFIED v1.1 — load-bearing; T.2 ROME ELIMINATED at canonical hparams (D-S218-3); T.2 GRACE PROMOTED to leading T-branch hypothesis (D-S218-4); v1.0 §5 conditional execution plan C-FAIL branch active |
| Supersedes | — (additive amendment; v1.0 carry-forward content preserved verbatim alongside v1.1) |
| Basis | v1.0 (S2.16 framework finding archival v1.0 + S2.16 Workstream 1 sessions); + S2.17 ROME runbook v0.1 authoring; + S2.18 T.2 ROME execution; + framework_finding_memit_ceiling_archival.md v1.1 (parallel deliverable in v0.2 codification session) |
| Specialist provenance | memit-specialist (primary; ROME elimination empirical record analysis, GRACE promotion rationale, mechanism comparison rank-1-in-weight vs adapter-based); state-consistency-theorist (secondary; Copy-Unmount inapplicability under GRACE adapter mechanism; cross-session determinism inheritance); orchestration-comparativist (write-engine architecture comparison surface; v1.1 GRACE foreground); graph-data-architect (light-touch; framework-spec-relevance scoring for adapter-based mechanisms); framework-spec-writer (formalization; v1.0 integrity preservation discipline) |
| Last updated | 2026-05-05 |

---

*End of T-Branch Decision Document v1.1 additive amendment of v1.0 — T.2 ROME ELIMINATED at canonical hparams (S2.18 D-S218-3); T.2 GRACE PROMOTED to leading T-branch hypothesis (D-S218-4); v1.0 §5 conditional execution plan C-FAIL branch active; S2.19 = T.2 GRACE runbook v0.1 authoring forthcoming.*
