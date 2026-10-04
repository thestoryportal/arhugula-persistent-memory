# Session 2.21 — Summary Block

**Session:** S2.21 — T.1-GRACE-3B Retry Runbook v0.1 Authoring
**Closed:** 2026-05-05
**Mode:** Declarative authoring; pre-empirical
**Predecessor:** S2.20 (T.2 GRACE; ROUTE_A_HALT_ENVIRONMENT_CONDITIONAL)
**Successor:** S2.22 (T.1-GRACE-3B execution on `meta-llama/Llama-3.2-3B`)
**Routing source:** D-S220-S221-ROUTING-1

---

## §1. Verdict

### §1.1 Verdict Class

`AUTHORING_COMPLETE_DECLARATIVE`

### §1.2 Verdict Statement

S2.21 produced `t1_grace_3b_runbook v0.1` (1487 lines; declarative; pre-empirical) per direct structural inheritance from `t2_grace_runbook v0.2`. All inheritance surfaces specified per kickoff §6.1 verbatim-substitution discipline + §6.2 substantive re-authoring at Cells 5/6/8/13/18. The runbook is minimum-viable for S2.22 entry; v0.2 codification anticipated post-S2.22 close per the established v0.1 → v0.2 absorption precedent (~10–24 mid-session cell rewrites typical).

### §1.3 Deliverable Inventory

| ID | Artifact | Length | Status |
|---|---|---|---|
| 1 | `t1_grace_3b_runbook v0.1` | 1487 lines | DECLARATIVE; ratified at S2.21 close |
| 2 | `session_2_21_summary_block.md` | this document | RATIFIED |

---

## §2. Decisions Ratified

### §2.1 Decision Inventory

| ID | Statement (compressed) | Closure |
|---|---|---|
| D-S221-Q1-1 | Runbook structural inheritance verbatim with §6.1 substring substitutions (model name + revision SHA + baseline path + output path prefix); layer paths UNCHANGED (`model.layers.17` / `model.layers.2`) | §1.5 + Cells 0–4 / 9 / 10 / 11 / 11+ / 11++ / 12 / 19–20 |
| D-S221-Q2-1 | Cell 18 INAPPLICABLE per §6.3 (no Llama-3.2-3B covariance caches at NV; GRACE adapter mechanism does not consume covariance caches) | Cell 18 |
| D-S221-Q3-1 | Layer corridor preservation: Layer-A = L17 (60.7% relative depth on 3B vs 53.1% on 8B; +7.6%); Layer-B = L2 (shallow); both within 0 ≤ idx < 28 bound | Cell 4 |
| D-S221-Q4-1 | Fresh baseline capture at Cell 5.5 per §5.2 (Cell 5 REWRITTEN; baseline producer not gate consumer); cross-session bit-exact gate INVERTED for first execution | Cell 5 |
| D-S221-Q5-1 | F-2 dispatch preamble inherited verbatim per `grace-patches-canonical v0.2 §10` (`model.train()` post-constructor; `requires_grad_(True)` NOT invoked; `gradient_checkpointing_enable()` NOT invoked) | Cell 9.5+ + Cell 11.5+ |
| D-S221-CHECKPOINT-1-1 | Checkpoint #1 of Llama-3.2-3B chain ESTABLISHED at S2.22 Cell 5; predecessor chain (Llama-3.1-8B #1–#7) NOT carry-forward across model classes; Llama-3.1-8B chain preserved on NV for any future return | Cell 5.5 / 5.6 (PROVISIONAL pending S2.22 execution) |
| D-S221-VRAM-PROJECTION-1 | Projected allocation under F-2 on RTX 4090 24 GiB: ~9.47 GiB total (model 6.42 + activations L17–L27 ds 2.50 + adapter+Adam 0.05 + workspace 0.50); 14.53 GiB headroom; environmental-3B OOM NOT anticipated but classified as halt for completeness | Cell 9.6 / Cell 11.6 (PROVISIONAL pending empirical confirmation at S2.22) |
| D-S221-CELL13-EXTENDED-1 | Cell 13 routing matrix EXTENDED beyond t2_grace_runbook v0.2 §3.7 to encode v1.2 disposition + v1.3 amendment scope at each route; framework_finding outcome matrix from kickoff §7 absorbed into routing JSON schema | Cell 13 |
| D-S221-CELL3-INHERITANCE-1 | Cell 3 INAPPLICABLE-DEFERRED-BY-MECHANISM inherited verbatim from t2_grace_runbook v0.2 §2.7; D-S219-CELL3-1 precedent extends through T.1-GRACE-3B (cell numbering parity with stage_1_sect_runbook v1.7 / t2_rome_runbook v0.2 preserved) | Cell 3 |

### §2.2 Decision Lifecycle Notes

D-S221-CHECKPOINT-1-1 and D-S221-VRAM-PROJECTION-1 are PROVISIONAL pending S2.22 empirical execution. Resolution pathways:

- D-S221-CHECKPOINT-1-1: RATIFIES at S2.22 Cell 5.5 successful baseline capture; FALSIFIES if Llama-3.2 model load fails (401 GatedRepoError) or layer-set verification fails.
- D-S221-VRAM-PROJECTION-1: RATIFIES at S2.22 Cell 9 / Cell 11 successful edit dispatch (no OOM); FALSIFIES if backward pass exceeds 24 GiB despite 14.53 GiB projected headroom (would trigger environmental-3B halt and route to hardware migration deliberation).

---

## §3. Constraints Established

| ID | Statement | Verification Site |
|---|---|---|
| C-S221-1 | Llama-3.2-3B revision SHA must be pinned at S2.22 Cell 5 entry (prevents floating-tag drift between sessions); SHA recorded in Cell 20 manifest extension | Cell 5.2 |
| C-S221-2 | Tokenizer continuity verification gate: PASS at allowlist parity (`{"cfb-v3-004"}` carries forward from S2.20) OR HARD HALT at MULTI_TOKEN_FAIL on non-allowlist fact; resolution at v0.2 codification with reconstructed allowlist if parity falsified | Cell 6 |
| C-S221-3 | Layer-set validity assertion at Cell 5.3: `n_layer == 28` AND `0 <= 17 < n_layer` AND `0 <= 2 < n_layer` AND `hidden_size == 3072` AND `intermediate_size == 8192`; HARD HALT on any violation (wrong model variant resolved) | Cell 5.3 |
| C-S221-4 | down_proj shape forensic anchor at Cell 8: `Linear(in_features=8192, out_features=3072)`; documents architectural delta vs Llama-3.1-8B `Linear(14336, 4096)`; consequence for adapter value parameter shape (3072,) automatically inherited via `nn.Parameter(torch.zeros(out_features))` in `GRACEAdaptor.__init__` | Cell 8 |
| C-S221-5 | Fresh baseline capture as Llama-3.2-3B chain Checkpoint #1: predecessor chain (Llama-3.1-8B #1–#7) explicitly NOT carry-forward across model classes; cross-session bit-exact gate (C-S220-3) deferred to Checkpoint #2 at any S2.23+ T.1-GRACE-3B re-execution | Cell 5.5 / 5.6 |

### §3.1 Inherited Constraints (Carry-Forward; RATIFIED)

The following constraints carry forward verbatim from `t2_grace_runbook v0.2 §6.1` and `grace-patches-canonical v0.2 §3.1`:

C-GRACE-1, C-GRACE-2, C-GRACE-3, C-GRACE-4, C-GRACE-5-REVISED, C-S220-2, C-F-2-DISPATCH-1, C-PRE-DISPATCH-STATE-1, C-PRE-DISPATCH-AUDIT-1, C-S220-PATCH-AUTHORING-1, C-S220-CELL-HYGIENE-1.

---

## §4. Open Questions

### §4.1 NEW at S2.21 (Closure at S2.22)

| ID | Statement | Closure Path |
|---|---|---|
| OQ-S221-1 | Llama-3.2 tokenizer leading-space convention parity with Llama-3.1: does `tokenizer.encode(" " + target_new, add_special_tokens=False)` produce the same single-token resolution on Llama-3.2 as on Llama-3.1 for cfb-v3 facts? | Cell 6 — RESOLVES informational at allowlist parity confirmed; routes v0.2 codification with reconstructed allowlist if parity falsified |
| OQ-S221-2 | down_proj shape impact on adapter value parameter shape: does `value_shape = 3072` (vs 4096 on 8B) require code-level adjustment in `GRACEAdaptor.__init__`, or does inheritance via `out_features` automatically propagate? | Cell 8 — RESOLVES at successful instantiation; documents at v0.2 codification |
| OQ-S221-3 | `hf_cache` reusability across model classes: does `/workspace/hf_cache` populated at S2.20 for Llama-3.1-8B accept Llama-3.2-3B downloads without conflict, or is per-model cache scoping required? | Cell 5.2 — RESOLVES at successful model load; routes investigation if cache namespace collision surfaces |

### §4.2 Carry-Forward from S2.20 (Not Closed at S2.21)

| ID | Statement | Closure Path |
|---|---|---|
| OQ-S220-MANIFEST-1 | Reproducibility manifest tracks 2 sessions despite 8+ session history; root cause investigation | DEFERRED to S2.22 Cell 0+ pre-execution investigation; runbook v0.1 documents the investigation pattern but does not resolve |
| OQ-S220-CFB-PATH-1 | Corpus path migration to per-engine path (`/workspace/architecture_profile/`) | DEFERRED per operator-side decision; runbook v0.1 inherits S2.20 path verbatim (`/workspace/session_logs/archive/s2_13/cfb-v3.yaml`) |
| OQ-S220-RTX-A100-MIGRATION-1 | Operator-side hardware migration to A100 80 GiB | OPEN; orthogonal to T.1-GRACE-3B retry; RESOLUTION SUBSTANTIVELY ALTERED by S2.22 verdict (Route B → migration de-prioritized; Route A environmental-3B → migration becomes only path forward) |

---

## §5. Interface Contracts Defined

### §5.1 IC-S221-1: Runbook Inheritance Discipline (Cross-Model-Class)

**Contract:** When authoring a parallel-sibling runbook for a NEW target model where the engine class is preserved (here: GRACE_barebones engine; model swap Llama-3.1-8B → Llama-3.2-3B):

1. Direct structural template = the most recent v0.2-codified runbook on the same engine.
2. Cells dispatching against architecture-dependent shapes (down_proj) require shape forensic anchor cells.
3. Cells consuming cross-session reference frames invert from gate-consumer to baseline-producer at first execution; gate role re-engages at second execution within the model-class chain.
4. Predecessor model-class chain bit-exact determinism is preserved as forensic record but does NOT carry forward as a pre-execution gate against the new model class.
5. Cell numbering parity with sibling runbooks is preserved via INAPPLICABLE-DEFERRED placeholders rather than cell renumbering.

**Verification:** `t1_grace_3b_runbook v0.1` Cells 3 (INAPPLICABLE inherited) + Cell 5 (REWRITTEN baseline-producer) + Cell 8 (shape forensic anchor) + Cell 18 (INAPPLICABLE per §6.3).

### §5.2 IC-S221-2: Cross-Model-Class Cross-Session Bit-Exact Discipline

**Contract:** Cross-session bit-exact determinism is scoped to a model-class chain. Distinct model classes start fresh chains:

```
Model-class chain "llama_3_1_8b":
    Checkpoint #1 (S2.13-C) → #7 (S2.20)         [PRESERVED on NV]

Model-class chain "llama_3_2_3b":
    Checkpoint #1 (S2.22 — to-be-established)
    Checkpoint #2 (S2.23+ — first to apply C-S220-3)
```

**Implementation:**
- Reproducibility manifest records `cross_session_checkpoint.model_class_chain` keying.
- Baseline JSON filename keyed on model name (`llama_3_2_3b_baselines.json`).
- C-S220-3 (combined bit-exact gate) applies WITHIN a chain, NOT ACROSS chains.

**Constraint:** A model-class chain is identified by `(model_repo_id, revision_sha)`. Variant changes within the same repo (e.g., a re-pin to a different revision SHA) start a new chain.

### §5.3 IC-S221-3: Routing Outcome Matrix Encoding

**Contract:** Cell 13 routing JSON schema MUST encode three orthogonal facets:

```python
{
    "route": "<ROUTE_B_15_TRIAL | ROUTE_A_HALT_MECHANISM_3B | ROUTE_A_HALT_ENVIRONMENT_3B | ROUTE_C_3_TRIAL_PREVIEW>",
    "v1_2_disposition": "<ENVIRONMENTAL_CEILING_CONFIRMED | MECHANISM_CLASS_ELIMINATION_STRONGER_THAN_V1_0 | ENVIRONMENTAL_CEILING_AT_MODEL_SIZE_INVARIANCE | DEFERRED_PENDING_PREVIEW>",
    "v1_3_amendment_scope": "<...>",
    "s_2_n_plus_1_routing": {"scope": "...", "rationale": "..."}
}
```

**Verification:** Cell 13 at `t1_grace_3b_runbook v0.1 §3.7`; framework_finding v1.2 outcome matrix (kickoff §7) absorbed verbatim into routing logic.

**Carry-forward:** This contract extends to any future T.X retry runbook that consumes a framework finding outcome matrix as the routing source.

---

## §6. Specialist Routing (Session-Level)

| Surface | Primary Specialist | Rationale |
|---|---|---|
| §1 Inheritance map authoring | framework-spec-writer | structural template inheritance discipline |
| §2 Block A cell bodies | memit-specialist | engine + patch state + model load + dry-run gate |
| §3 Block B cell bodies | memit-specialist + validation-contract-architect | edit dispatch + verdict surface |
| §4 Block C declarative inheritance | memit-specialist | trial loop body |
| §5 Block-end cell bodies | state-consistency-theorist | NV inventory + manifest |
| §6 Constraints | framework-spec-writer | constraint codification |
| §7 Verdict surface taxonomy | validation-contract-architect | calibration corridor + pathology classes |
| §8 Forward routing | framework-spec-writer + orchestration-comparativist | successor session adjudication + framework-finding alignment |

aiSecOps-specialist + graph-data-architect + framework-council not invoked at S2.21 (declarative authoring only; no security boundary or schema authoring surface).

---

## §7. Carry-Forward Anchors for S2.22

### §7.1 Load-Bearing State

| Anchor | Status | Carry-forward |
|---|---|---|
| `t1_grace_3b_runbook v0.1` declarative form | RATIFIED | minimum-viable spec for S2.22 execution |
| Patches `{P-1-GRACE, P-2-GRACE, Pad-Token, F-2}` | RATIFIED EMPIRICALLY-VALIDATED at S2.20 | applied at S2.22 Cells 2++ / 2++++ / 5.4 / 9.5+ / 11.5+ |
| `cfb-v3.yaml v1.0` corpus | RATIFIED | consumed at S2.22 Cell 6 |
| `probe-set-v3.yaml v1.0` | RATIFIED | consumed at S2.22 Cell 5.5 + Cell 7 |
| Llama-3.1-8B chain (Checkpoint #1–#7) | PRESERVED on NV | NOT consumed at S2.22; available for any future return |
| Layer corridor (L17 + L2) | RATIFIED | preserved across model swap; both indices valid on Llama-3.2-3B (n_layer = 28) |

### §7.2 Provisional Anchors Pending S2.22

| Anchor | Status | Resolution |
|---|---|---|
| D-S221-CHECKPOINT-1-1 | PROVISIONAL | RATIFIES at S2.22 Cell 5.5 baseline capture |
| D-S221-VRAM-PROJECTION-1 | PROVISIONAL | RATIFIES at S2.22 Cell 9 / Cell 11 successful dispatch (no OOM) |
| OQ-S221-1 / OQ-S221-2 / OQ-S221-3 | OPEN | RESOLVE at S2.22 Cells 6 / 8 / 5.2 respectively |
| OQ-S220-MANIFEST-1 | DEFERRED | investigated at S2.22 Cell 0+ |

### §7.3 Eliminated Hypotheses (S2.20 Carry-Forward)

All S2.20 §11.3 eliminations carry forward unchanged: H-A (FALSIFIED), H-B (CONFIRMED), H-C (FALSIFIED), H-D (CONFIRMED then RECONTEXTUALIZED), H-E (FALSIFIED), H-F (FALSIFIED), H-G (RECONTEXTUALIZED).

---

## §8. KB Hygiene — Pre-S2.22

### §8.1 Required Uploads at S2.22 Entry

| Document | Rationale |
|---|---|
| `t1_grace_3b_runbook v0.1` | LOAD-BEARING; primary execution artifact |
| `grace-patches-canonical v0.2` | LOAD-BEARING; patches applied at Cells 2++ / 2++++ / 9.5+ / 11.5+ |
| `cfb-v3.yaml v1.0` | LOAD-BEARING; corpus consumed at Cells 5.5 / 6 |
| `probe-set-v3.yaml v1.0` | LOAD-BEARING; probe set consumed at Cells 5.5 / 7 |
| `framework_finding_memit_ceiling_archival v1.2` | LOAD-BEARING; routing rationale at Cell 13 |
| `t_branch_decision_document v1.1` | LOAD-BEARING; Route A mechanism vs environmental disambiguation |
| `session_2_21_summary_block.md` | predecessor session reference |

### §8.2 Recommended Removals at S2.22 Entry

| Document | Rationale |
|---|---|
| `t2_grace_runbook v0.1` | superseded by v0.2 |
| `grace-patches-canonical v0.1` | superseded by v0.2 |
| `t2_grace_runbook v0.2` | structural template consumed at S2.21; not load-bearing for S2.22 execution (verbatim cells absorbed into v0.1) |
| `t2_rome_runbook v0.2` / `rome-patches-canonical v0.2` | sibling reference; INAPPLICABLE to T.1-GRACE-3B execution |
| `stage_1_sect_runbook v1.7` / `memit-patches-canonical v2.5` | MEMIT-side; INAPPLICABLE |
| `framework_finding v1.0 / v1.1` | merged into v1.2 carry-forward |
| `session_2_18_summary_block.md` / `session_2_19_summary_block.md` / `session_2_20_summary_block.md` | predecessor-of-predecessor; load-bearing surfaces absorbed into v1.2 + v0.1 carry-forward |

---

## §9. Session Close Posture

### §9.1 Authoring Sequence Executed

```
Phase 1: Inheritance verification                                COMPLETE
  └── Confirmed t2_grace v0.2 + grace-patches v0.2 + framework v1.2 in KB

Phase 2: Runbook v0.1 declarative authoring                      COMPLETE
  ├── §0 + §1: version history + inheritance map
  ├── §2: Block A (Cells 0–8); Cell 5/6/8 substantive re-authoring
  ├── §3: Block B (Cells 9–13); Cell 13 EXTENDED routing matrix
  ├── §4: Block C declarative inheritance
  ├── §5: Block-end (Cells 18–20); Cell 18 INAPPLICABLE
  ├── §6: process constraints (inherited + 5 NEW C-S221-x)
  ├── §7: verdict surface taxonomy (verbatim inheritance)
  ├── §8: forward routing (3-route outcome matrix per kickoff §7)
  └── §9: document status

Phase 3: Decision + constraint ratification                      COMPLETE
  ├── 8 decisions ratified per §2 (D-S221-Q1-1..Q5-1 + Checkpoint + VRAM + Cell13-Extended + Cell3-Inheritance)
  └── 5 constraints ratified per §3 (C-S221-1..5)

Phase 4: S2.21 close summary authoring                            COMPLETE
  └── this document
```

### §9.2 Recovery Cell Inventory

S2.21 is a declarative authoring session; no pod-side execution; no recovery cells authored. All cell bodies in `t1_grace_3b_runbook v0.1` are minimum-viable specifications subject to v0.2 absorption at S2.22 close.

### §9.3 Forward Action

| Step | Action | Owner |
|---|---|---|
| §9.3.1 | Operator endorses S2.21 close artifacts (runbook + summary) | operator |
| §9.3.2 | Operator initiates S2.22 with appropriate kickoff prompt referencing this summary | operator |
| §9.3.3 | Operator confirms KB hygiene per §8 prior to S2.22 entry | operator |
| §9.3.4 | S2.22 = T.1-GRACE-3B execution session: Block A + Block B (+ conditional Block C per Cell 13 routing) | operator + agent |
| §9.3.5 | Post-S2.22 close: v0.2 codification analog session anticipated (parallel to S2.18 / S2.20 absorption precedent) | operator scheduling |

### §9.4 Successor Session Conditional Routing (S2.23 from S2.22)

| S2.22 Cell 13 verdict | S2.23 scope |
|---|---|
| ROUTE_B_15_TRIAL | Block C continuation OR finalization; v1.2 disposition: ENVIRONMENTAL_CEILING_CONFIRMED |
| ROUTE_A_HALT_MECHANISM_3B | T.1 alt-model under MEMIT runbook v0.1 authoring (resumes t_branch §5'-α canonical path); v1.3 amendment: adapter-mechanism architectural-invariant |
| ROUTE_A_HALT_ENVIRONMENT_3B | Hardware migration deliberation OR T-branch halt; v1.3 amendment: model-size invariance ceiling |
| ROUTE_C_3_TRIAL_PREVIEW | 3-trial preview within S2.22 OR S2.23 |

---

**Session 2.21 CLOSED 2026-05-05.**

**Persistence:** `/mnt/user-data/outputs/session_2_21_summary_block.md`
