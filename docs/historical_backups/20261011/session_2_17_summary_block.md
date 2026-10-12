# Session 2.17 Summary Block — v1.6 Hardening + T.2 ROME Runbook v0.1 Authoring

> **Session ID:** S2.17
> **Title:** v1.6 Hardening (INLINE) + T.2 ROME Runbook v0.1 Authoring
> **Predecessor:** S2.16 (Framework Finding Archival + T-Branch Entry Scoping; CLOSED 2026-05-04)
> **Successor:** S2.18 — T.2 ROME Execution (Block A pre-flight + Block B HC-2-equivalent dry-run + Block C 15-trial Stage 1 SECT v3)
> **Status:** **CLOSED** (2026-05-04)
> **Workstream:** WS1 (empirical execution; T-branch entry — T.2 ROME)
> **Session classification:** SCOPING / authoring — no pod-side execution; three deliverable artifacts authored
> **Specialists active:** framework-spec-writer (PRIMARY for Block 1 v1.6 authoring + Block 2 runbook v0.1 authoring + rome-patches-canonical authoring); memit-specialist (PRIMARY for Block 2 ROME mechanism evaluation + patches subset re-derivation + hparam surface inventory + layer-set candidate selection); state-consistency-theorist (secondary; covariance cache reuse verification at Block A Cell 3; Copy-Unmount applicability at ROME single-fact dispatch); validation-contract-architect (occasional; HC-2-equivalent dry-run verdict surface at Block B Cell 13; verdict integrity binding inheritance at Block C Cell 14)

---

## §1 — Verdict

### §1.1 Session deliverables — closed

| # | Block | Artifact | Status | Filename |
|---|---|---|---|---|
| 1 | Block 1 | Stage 1 SECT runbook v1.6 hardening pass | **RATIFIED** | `stage_1_sect_runbook_v1_6.md` |
| 2 | Block 2 | T.2 ROME runbook v0.1 | **RATIFIED v0.1 — declarative; empirical instantiation at S2.18** | `t2_rome_runbook_v0_1.md` |
| 3 | Block 2 | ROME patches canonical v0.1 | **RATIFIED v0.1 — declarative; empirical applicability at S2.18 Block A Cell 2** | `rome-patches-canonical.md` |
| 4 | (close) | This session summary block | **CLOSED** | `session_2_17_summary_block.md` |

### §1.2 Q1-Q5 ratified at S2.17

| Q | Decision | Decision ID |
|---|---|---|
| **Q1** | v1.6 hardening status: INLINE to S2.17 (Block 1) | D-S217-Q1-1 (closed at kickoff per D-S216-Q5-1) |
| **Q2** | ROME SHA pin: latest stable tip (operator-side override semantics; resolved at S2.18 Block A Cell 1 first execution) | D-S217-Q2-1 |
| **Q3** | ROME canonical hparams: ROME paper Table 1 GPT-J reference values at runbook v0.1 (declared starting point); full Llama-3.1-8B calibration at S2.18 Block B Cell 13 | D-S217-Q3-1 |
| **Q4** | Layer candidates at HC-2-equivalent dry-run: BOTH L17 (Layer-A primary; ROME paper precedent for transformer-mid on GPT-J / GPT-2-XL) AND L2 (Layer-B secondary; S2.14-D D.1 mediation peak) | D-S217-Q4-1 |
| **Q5** | cfb-v3-004 multi-token tolerance posture: first-token-proxy carry-forward per D-S215D2-CFB-V3-004-PROXY-1 + explicit `RE-EVALUATE AT TRIAL 0` flag at Block B Cell 13 | D-S217-Q5-1 |

### §1.3 Block 1 verdict — v1.6 hardening RATIFIED

`stage_1_sect_runbook_v1_6.md` ships **RATIFIED** at Block 1 close (not PROVISIONAL). Five carry-forward OQs from S2.15-D2 / S2.13-C closed in canonical single-source form. Ratification posture per `stage_1_sect_runbook_v1_6.md` § §1.5 v1.6 entry: all five edits are documentation discipline, predicate relaxation, or cross-cell field-name reconciliation; **none modify cache-dispatch surface semantics**. The S2.8 architectural-axis empirical anchor + S2.13-C / S2.14-D / S2.15-D2 cumulative pod-side execution discharge the v1.5 PROVISIONAL-pending gate transitively. v1.6 supersedes v1.5 PROVISIONAL.

### §1.4 Block 2 verdict — ROME runbook v0.1 + ROME patches canonical v0.1 RATIFIED

`t2_rome_runbook_v0_1.md` and `rome-patches-canonical.md` v0.1 ship **RATIFIED v0.1** at Block 2 close. Status is **declarative** — cell skeletons complete, structural inheritance from v1.6 explicit, patches inventory + hparams + layer candidates declared. Empirical instantiation at S2.18 Block A first execution. v0.2 absorbs:
- First-execution implementation specifics (Cells 1, 2, 8, 9, 11, 15 cell bodies)
- Block B Cell 13 hparam calibration verdict (full resolution of OQ-S216-2)
- Block B Cell 13 cfb-v3-004 multi-token native handling verdict (full resolution of OQ-S216-4 / OQ-S217-4)
- Any ROME-specific patches surfaced at Cell 2 first execution (currently expected: none)

### §1.5 Risk-budget assessment (Block 1 wall-time vs 60% threshold)

Block 1 (v1.6 hardening) consumed substantially less than 60% of the session budget: surgical edits against v1.5 (~138-line additive delta; ~14 str_replace / view operations; no pod execution). Block 2 proceeded to full-scope authoring as planned. **No deferral to S2.17b was triggered**; both blocks delivered in the single session per the kickoff prompt risk acknowledgement.

---

## §2 — Decisions ratified

### §2.1 Block 1 decisions — v1.6 hardening

| ID | Decision | Closes |
|---|---|---|
| **D-S217-1** | Cell 2 of `stage_1_sect_runbook_v1_6.md` is the canonical and exclusive site for patch-marker assertion. Marker references in Cell 3 / Cell 9 / prose comments are explicitly reclassified as descriptive-only context, not parallel verification sites. Codified at v1.6 § §1.5.2 (companion to C-S28-1 at `memit-patches-canonical.md` v2.5 §10.4) | OQ-S215D2-CELL2-1 |
| **D-S217-2** | Single-source contract for cfb-v3 fact corpus: Cell 6 `stage_1_facts` literal + Cell 8 `fact_memit_requests` literal are the canonical runtime source of truth. `cfb-v3.yaml` v1.0 is reclassified as the documentation mirror. Cell 8 cross-cell SUBSET hard gate validates Cell 6 ↔ Cell 8 (subject, target_new) tuples match exactly. Drift = runbook-authoring violation, not runtime defect | OQ-S213C-10 |
| **D-S217-CELL3-SUBSET-CARRYFORWARD-1** | Cell 3 R1.1 file-set predicate reformed from set-equality to SUBSET assertion per D-S215D2-CELL3-SUBSET-ASSERTION-1 carry-forward. PROVENANCE.txt-declared layer_set is contract-narrowing predicate; cache `.npz` truth is authoritative; cache-truth-superset is acceptable | OQ-S215D2-PROVENANCE-CACHE-TRUTH-1 |
| **D-S217-CELL11-CACHE-FIELD-1** | Cell 3 writer field-name reconciled: `provenance_fields` → `provenance` (canonical). Cell 11 reader gains defensive try-both fallback (`provenance` then `provenance_fields`) for backwards-compat with v1.5-vintage NV state. OQ-S28-4 SHA equality gate now load-bearing rather than silently DEFERRED | OQ-S215D2-CELL11-CACHE-SHA-KEY-1 |
| **D-S217-V12-DOC-REFRESH-1** | Part XI §11.1 OQ-S25-1 closure note filename pattern corrected to post-P-6 form including `_t100_` segment. Part XII §12.2 / §12.3 / §12.5 / §12.6 reference appendices refreshed from CFB v1-era stale-inherited tables to v3 fact set (38 active probes / 15 trials × 30 overlays / cfb-v3-001 through cfb-v3-005 / 95–125 min total wall-time). Closes the dedicated reference-table refresh pass deferred at v1.5 STALE-INHERITED NOTE | OQ-S215D2-V12-2-DOC-DRIFT-1 |

### §2.2 Block 2 decisions — T.2 ROME runbook + patches authoring

| ID | Decision |
|---|---|
| **D-S217-3** | Single-fact dispatch envelope for ROME at S2.18 Block C: 15-trial Stage 1 SECT v3 protocol executed as 15 sequential single-fact ROME edits (no batched multi-fact dispatch). Per-fact Copy-Unmount restore is per-fact, not per-trial-group. Codified at `t2_rome_runbook_v0_1.md` § §1.5.1 (parallel constraint at `rome-patches-canonical.md` v0.1 §4.1 C-ROME-1) |
| **D-S217-4** | v0.1 inherits four empirical anchors without re-execution at S2.17: (1) cross-session bit-exact determinism on Llama-3.1-8B fp16 (5 checkpoints; drift `0.00e+00`); (2) Copy-Unmount bit-exact joint-overlay regime (L4-L8 + L2-L6; structurally narrower under ROME single-fact); (3) covariance caches L2-L8 durable on NV (5.75 GB); (4) `stage_1_llama_baselines.json` 38-probe baseline + cfb-v3 fact roster + per-fact target_TRUE natural top-1 capture. Codified at `t2_rome_runbook_v0_1.md` § §1.5.2 |
| **D-S217-Q1-1** | v1.6 hardening = INLINE to S2.17 Block 1 (closed at kickoff per D-S216-Q5-1) |
| **D-S217-Q2-1** | ROME SHA pin = latest stable tip; operator-side override semantics; resolved at S2.18 Block A Cell 1 first execution. Codified at `rome-patches-canonical.md` v0.1 §2 |
| **D-S217-Q3-1** | ROME canonical hparams at runbook v0.1 = ROME paper Table 1 GPT-J reference values (declared starting point: `v_lr=0.5`, `v_num_grad_steps=20`, `clamp_norm_factor=4`, `kl_factor=0.0625`, `mom2_adjustment=15000`). Full Llama-3.1-8B calibration at S2.18 Block B Cell 13. Codified at `rome-patches-canonical.md` v0.1 §3.1 + `t2_rome_runbook_v0_1.md` Cell 4 |
| **D-S217-Q4-1** | Layer candidates at HC-2-equivalent dry-run (Block B): BOTH L17 (Layer-A primary; ROME paper precedent) AND L2 (Layer-B secondary; S2.14-D D.1 mediation peak). Cross-layer comparison at Cell 12; load-bearing layer for Block C selected at Cell 13. Codified at `rome-patches-canonical.md` v0.1 §3.2 + `t2_rome_runbook_v0_1.md` Cells 9-13 |
| **D-S217-Q5-1** | cfb-v3-004 harp multi-token tolerance posture under ROME single-fact dispatch: first-token-proxy carry-forward per D-S215D2-CFB-V3-004-PROXY-1 + explicit `RE-EVALUATE AT TRIAL 0` flag at Block B Cell 13. Resolves to native multi-token / first-token-proxy / forensic-informative-excluded based on ROME's empirical handling at trial 0 |

### §2.3 Forward-routing decisions

| ID | Decision |
|---|---|
| **D-S217-CLOSE-1** | S2.18 entry locked at T.2 ROME execution per `t2_rome_runbook_v0_1.md` v0.1 three-block structure (Block A pre-flight Cells 0-8 + Block B HC-2-equivalent dry-run Cells 9-13 + Block C 15-trial loop Cells 14-20) |
| **D-S217-CLOSE-2** | `rome-patches-canonical.md` v0.1 is preserved unmodified through S2.18 Block A first execution; v0.2 absorbs empirical applicability verdicts |
| **D-S217-CLOSE-3** | `memit-patches-canonical.md` v2.5 preserved unmodified at S2.17 (consistent with D-S216-CLOSE-3) |
| **D-S217-CLOSE-4** | `stage_1_sect_runbook_v1_6.md` is the basis for S2.18 Block A Cells 0-8 (carry-forward unchanged for Cells 0, 1.5, 5, 6, 7; adapted for Cells 1, 2, 4, 8) and Block C Cells 14, 16, 17, 18, 19, 20 (cell-numbering shift from MEMIT Cells 8, 10, 10, 11, 12, 12) |
| **D-S217-CLOSE-5** | T.2 ROME conditional execution plan locked per `t_branch_decision_document.md` §5: Block C C-PASS ⇒ S2.19 = MEMIT-vs-ROME comparison framework finding update; Block C C-FAIL ⇒ S2.19 = T.2 GRACE runbook authoring + S2.20 = GRACE execution; Block C C-PARTIAL ⇒ operator-side verdict integrity binding re-evaluation |

---

## §3 — Constraints established / maintained

### §3.1 New constraints (Block 2 — ROME canonical)

| Constraint | Source | Status | Applicability |
|---|---|---|---|
| **C-ROME-1** | `rome-patches-canonical.md` v0.1 §4.1 | RATIFIED v0.1 | Single-fact dispatch envelope at S2.18 Block C; no batched multi-fact ROME at runbook v0.1 |
| **C-ROME-2** | `rome-patches-canonical.md` v0.1 §4.2 | RATIFIED v0.1 | Covariance cache reuse from pre-S2.6 fork-work session; SUBSET assertion at Cell 3 |
| **C-ROME-3** | `rome-patches-canonical.md` v0.1 §4.3 | RATIFIED v0.1 | Dry-run gate (R1.3-equivalent) for ROME cache-dispatch surface; parallel to C-S26-3 at MEMIT canonical |
| **C-ROME-4** | `rome-patches-canonical.md` v0.1 §4.4 | DECLARED v0.1 (not yet exercised; no v0.1 markers introduced) | Marker post-application verification; parallel to C-S28-1 at MEMIT canonical |

### §3.2 Constraints maintained (carry-forward; unchanged at S2.17)

| Constraint | Status | S2.17 disposition |
|---|---|---|
| C-S25-5 (cwd invariant at MEMIT_ROOT) | LOCKED | Carry-forward unchanged. Adapted to ROME_ROOT for T.2 ROME |
| C-S26-1 (`mom2_n_samples=100000`, `mom2_dtype=float32`, `batch_tokens=100`) | LOCKED | Carry-forward unchanged. Inherited via covariance cache reuse at C-ROME-2 |
| C-S26-2 (cache-dispatch path explicit batch_tokens propagation via P-7) | LOCKED | Carry-forward unchanged for MEMIT. INAPPLICABLE to ROME (P-7 inapplicable; single-fact dispatch) |
| C-S26-3 (dry-run gate; R1.3 cache-dispatch smoke) | LOCKED | Carry-forward unchanged. Adapted to C-ROME-3 (R1.3-equivalent) for ROME |
| C-S28-1 (defense-in-depth marker post-application verification) | LOCKED | Carry-forward unchanged. Adapted to C-ROME-4 for ROME |
| C-S214D-2 (batched MEMIT N=5 on RTX 4090 24 GiB at VRAM ceiling) | LOCKED | Carry-forward unchanged for MEMIT context. INAPPLICABLE to ROME (single-fact; no VRAM ceiling concern under single-fact dispatch) |

---

## §4 — Open questions

### §4.1 Closed at S2.17

| OQ | Closure | Block |
|---|---|---|
| **OQ-S215D2-CELL2-1** | Closed via `stage_1_sect_runbook_v1_6.md` § §1.5.2 (D-S217-1) | Block 1 |
| **OQ-S215D2-PROVENANCE-CACHE-TRUTH-1** | Closed via Cell 3 R1.1 SUBSET assertion (D-S217-CELL3-SUBSET-CARRYFORWARD-1) | Block 1 |
| **OQ-S215D2-CELL11-CACHE-SHA-KEY-1** | Closed via Cell 3 writer field-name rename + Cell 11 try-both fallback (D-S217-CELL11-CACHE-FIELD-1) | Block 1 |
| **OQ-S215D2-V12-2-DOC-DRIFT-1** | Closed via Part XI §11.1 + Part XII §12.2 / §12.3 / §12.5 / §12.6 refresh (D-S217-V12-DOC-REFRESH-1) | Block 1 |
| **OQ-S213C-10** | Closed via Cell 6 single-source declaration block + Cell 8 cross-cell SUBSET hard gate (D-S217-2) | Block 1 |
| **OQ-S216-5** | v1.6 hardening session scheduling resolved at kickoff (INLINE per D-S216-Q5-1 → D-S217-Q1-1) | (kickoff) |

### §4.2 Closed PARTIALLY at S2.17 — full closure deferred to S2.18

| OQ | Partial closure at S2.17 | Full closure path |
|---|---|---|
| **OQ-S216-1** | ROME SHA pin policy = latest stable tip per D-S217-Q2-1 | Resolved fully at S2.18 Block A Cell 1 first execution (concrete SHA captured to `t2_rome_pinned_sha.txt`) |
| **OQ-S216-2** | ROME canonical hparams declared at v0.1 = ROME paper Table 1 GPT-J reference values per D-S217-Q3-1 | Resolved fully at S2.18 Block B Cell 13 first execution (Llama-3.1-8B-specific calibration verdict) |
| **OQ-S216-3** | Layer-A primary = L17 + Layer-B secondary = L2 declared at v0.1 per D-S217-Q4-1 | Resolved fully at S2.18 Block B Cell 12 cross-layer comparison + Cell 13 load-bearing layer selection |
| **OQ-S216-4** | First-token-proxy carry-forward at v0.1 + RE-EVALUATE AT TRIAL 0 flag per D-S217-Q5-1 | Resolved fully at S2.18 Block B Cell 13 trial 0 (cfb-v3-004 ROME native multi-token handling verdict) |

### §4.3 Opened at S2.17

| OQ | Surface | Closure path |
|---|---|---|
| **OQ-S217-2** | L17 covariance cache availability — current NV cache truth covers L2-L8 (cumulative); L17 is OUTSIDE that range. Block B Layer-A=L17 candidate requires either: (a) extend cache to include L17 (~30 min Wikipedia 100k-sample compute on RTX 4090), OR (b) restrict Block B layer candidate to L2-L8 range and re-author Q4 layer-set candidates | **Operator-side resolution at S2.18 Block A entry, BEFORE pod attach.** Recommended: extend cache to include L17 (preserves L17 ROME paper precedent vs L2 mediation peak comparison surface). Note in `t2_rome_runbook_v0_1.md` § §III Cell 3 |
| **OQ-S217-3** | ROME `apply_rome_to_model` invocation API at the latest stable SHA — v0.1 declared schema (positional + keyword args) may not match if the canonical implementation has API drift. Verified at Cell 8 R1.3-equivalent dry-run gate / Cell 9 first dispatch | Resolved at S2.18 Block A Cell 8 + Block B Cell 9 first execution. v0.2 absorbs the empirically-verified API surface |
| **OQ-S217-4** | ROME multi-token target_new native handling under single-fact dispatch — v0.1 declares first-token-proxy carry-forward; native multi-token may be supported by ROME's mechanism (rank-1 update on single-token v-vector OR token-sequence v-vector — requires empirical verification) | Resolved at S2.18 Block B Cell 13 trial 0. Equivalent to OQ-S216-4 full closure path |

### §4.4 Carry-forward acknowledged

| OQ | Status |
|---|---|
| OQ-S216-6 (MEMIT-vs-ROME comparison framework finding update artifact) | Routes to S2.19 IF S2.18 Block C verdict = C-PASS |
| OQ-S214D-D1-1, OQ-S214D-D1-PREDICATE-1, OQ-S214D-PATH-1, OQ-S214D-CWD-1, OQ-S214D-D3-OOM-1, OQ-S214D-HF-CACHE-LOCATION-1, OQ-S214D-FSTRING-1, OQ-S214D-NV-CACHE-DEDUPE-1, OQ-S214D-D3-OVERLAY-1, OQ-S214D-PATCH-FILE-MAP-1, OQ-S214D-TERMINAL-1, OQ-S214D-TRANSFORMERS-1 | Eliminated as forward concerns post-S2.15-D2 (Class D fully eliminated; T-branch entry locked); not load-bearing for T.2 ROME |

---

## §5 — Empirical anchors (carry-forward to T.2 ROME)

S2.17 produced no new empirical anchors (scoping/authoring session; no pod-side execution). The session inherits and forward-routes the carry-forward anchor inventory from S2.16 §5 + S2.15-D2 §3.2 + §5.

### §5.1 Anchor inheritance summary (per D-S217-4)

| Anchor | Status | T.2 ROME applicability at S2.18 |
|---|---|---|
| Cross-session bit-exact determinism (Llama-3.1-8B fp16 forward-pass drift `0.00e+00`; 5 checkpoints) | LOCKED | INHERITS — same target model; same hparam regime modulo write-engine specifics. Verified at S2.18 Block A Cell 5 / Cell 7 against `stage_1_llama_baselines.json` |
| Copy-Unmount bit-exact joint-overlay regime (L4-L8 + L2-L6; 75/75 + 5/5 layer-restore allclose; per-fact unmount drift `0.00e+00`) | LOCKED | INHERITS — mechanism applicable to ROME single-fact dispatch (PyTorch in-place tensor restore primitive shared across both engines). Structurally narrower under ROME (1 layer per fact, not 5) — strict subset of validated regime |
| Covariance caches L2-L8 (5.75 GB durable on NV; PROVENANCE-narrowed cumulative; ROME consumes same cache structure) | LOCKED | INHERITS for L2-L8 layers. **GAP at L17** per OQ-S217-2 — operator-side cache extension required at S2.18 Block A entry |
| `stage_1_llama_baselines.json` 38-probe baseline at canonical hparams (cfb-v3 fact roster; pre-edit `P[target_TRUE]` natural top-1 captured per D-S213C-CALIB-1/2/3) | LOCKED | INHERITS — same probe set, same fact roster, same target architecture. Cell 7 re-capture verifies bit-exact match |
| `stage_1_token_verification.json` (subject token continuity baseline; multi-token allowlist for cfb-v3-004) | LOCKED (multi-token allowlist subject to RE-EVALUATE AT TRIAL 0 per D-S217-Q5-1) | INHERITS — same Llama tokenizer determinism. cfb-v3-004 multi-token re-evaluated at S2.18 Block B Cell 13 |

### §5.2 New empirical surfaces opened at S2.17 — resolved at S2.18

| Surface | Resolution scope at S2.18 |
|---|---|
| ROME repo SHA pin under "latest stable tip" policy | Cell 1 first execution captures concrete SHA |
| ROME `apply_rome_to_model` API verification | Cell 8 R1.3-equivalent + Cell 9 first dispatch |
| ROME single-fact rank-1 update on Llama-3.1-8B at L17 | Block B Cell 9 |
| ROME single-fact rank-1 update on Llama-3.1-8B at L2 | Block B Cell 11 |
| Cross-layer comparison verdict (load-bearing layer selection) | Block B Cell 12-13 |
| ROME multi-token native handling on cfb-v3-004 | Block B Cell 13 trial 0 |
| 15-trial Stage 1 SECT v3 verdict under ROME single-fact dispatch | Block C Cells 14-17 |

---

## §6 — Interface contracts

### §6.1 New ICs introduced at S2.17

No new interface contracts introduced at S2.17. The session is structural authoring (runbook + patches doc + summary); no new IC-N-M designations are coined.

### §6.2 ICs maintained (carry-forward; unchanged at S2.17)

| IC | Status | T.2 ROME applicability |
|---|---|---|
| IC-S23-4 (intra-pod drift band 1e-4) | LOCKED | Carry-forward to T.2 ROME unmount band gate at Cell 15 |
| IC-S24-3 (CFB v1 ↔ MEMIT input contract) | LOCKED | Carry-forward; ROME consumes same MEMIT-style input format (single fact in a list-of-1) |
| IC-S24-4 (Stage 1 trial protocol — 5 facts × 3 replicates) | LOCKED | Carry-forward; under C-ROME-1 single-fact narrowing applied to dispatch granularity |
| IC-S25-1 (bridge cache provenance contract) | LOCKED | Carry-forward; cache reuse per C-ROME-2 |
| IC-S25-2 (P-4 patch application contract) | LOCKED | Carry-forward; verified at Cell 2 |
| IC-S25-3 (LLaMA baseline re-capture contract) | LOCKED | Carry-forward; Cell 5 / Cell 7 |
| IC-PreS26-2 (post-P-6 cache filename interface) | LOCKED | Carry-forward; ROME `rome/layer_stats.py` post-P-6 verification at Cell 2 |
| IC-PreS26-3 (mom2.mom2 priority resolution) | LOCKED | Carry-forward; Cell 3 R1.2 |

---

## §7 — Predecessor cleanup (S2.16 deliverables retained)

S2.16 deliverables are preserved unchanged at S2.17 close:

- `framework_finding_memit_ceiling_archival.md` v1.0 — PERMANENT empirical record (load-bearing for understanding why T.2 ROME is the test surface; on-demand reference at S2.18+)
- `t_branch_decision_document.md` v1.0 — methodology lock for T.2 ROME (referenced at `t2_rome_runbook_v0_1.md` Part VII forward routing)
- `t2_rome_runbook_v0_1_authoring_plan.md` v1.0 — defines this session's scope (Block 2 acceptance criteria validation)
- `session_2_16_summary_block.md` — predecessor close artifact

`memit-patches-canonical.md` v2.5 is preserved unmodified per D-S216-CLOSE-3 / D-S217-CLOSE-3.

---

## §8 — Forward routing → S2.18

### §8.1 Successor scope

**S2.18 — T.2 ROME execution.** Pod-side execution session against `t2_rome_runbook_v0_1.md` v0.1. Three-block structure:

- **Block A** (Cells 0-8) — pre-flight verification: pod attach + NV mount; ROME repo clone + SHA pin resolution; environment fingerprint capture; ROME patch state verification (closes empirical applicability of `rome-patches-canonical.md` v0.1 §1); covariance cache reuse SUBSET gate; ROME hparam declaration; Llama-3.1-8B model load + Pad-Token + cross-session bit-exact gate; tokenizer single-token verification; pre-edit baseline capture; R1.3-equivalent dry-run gate
- **Block B** (Cells 9-13) — HC-2-equivalent dry-run: cfb-v3-001 guitar at Layer-A=L17 (Cell 9-10); cfb-v3-001 guitar at Layer-B=L2 (Cell 11-12); Block B verdict gate (Cell 13) — load-bearing layer selected for Block C; cfb-v3-004 multi-token finalization; full ROME hparam calibration verdict
- **Block C** (Cells 14-20) — 15-trial Stage 1 SECT v3 execution at single-fact ROME dispatch on the load-bearing layer; per-trial verdict aggregation; aggregate verdict per D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset {cfb-v3-001, cfb-v3-002, cfb-v3-005} decisive; full 5-fact aggregate informational); NV inventory + SHA equality gate; mirror sync NV→SSD; reproducibility manifest update

Wall-time estimate per `t2_rome_runbook_v0_1.md` §10.3: total ~101–143 min (Block A ~13–20 min; Block B ~11–15 min; Block C ~77–108 min).

### §8.2 Pre-S2.18 operator-side dependencies

| Item | Priority | Source | Resolution |
|---|---|---|---|
| 1. Resolve OQ-S217-2 (L17 covariance cache availability): extend cache to include L17 OR restrict layer candidate set to L2-L8 | **REQUIRED — pre-S2.18 dependency** | `t2_rome_runbook_v0_1.md` §III Cell 3 + §VIII §8.2 | Operator-side at S2.18 entry, BEFORE pod attach |
| 2. ROME canonical hparams operator-side review (paper Table 1 GPT-J values declared; Llama-specific calibration scope at Block B Cell 13) | RECOMMENDED | `rome-patches-canonical.md` v0.1 §3.1 | Operator-side review of declared starting values; full resolution at S2.18 Block B Cell 13 |
| 3. ROME repo inspection at `https://github.com/kmeng01/rome` for `apply_rome_to_model` invocation API + post-2022 commit churn assessment | RECOMMENDED | OQ-S217-3 | Operator-side at S2.18 Block A entry; informs Cell 1 SHA pin resolution + Cell 9 dispatch surface |
| 4. KB curation per §10 below | RECOMMENDED | This summary §10 | Operator-side curation before S2.18 entry |

### §8.3 Forward-routing decision tree

```
S2.17 close (THIS SESSION):
  ├── Block 1: stage_1_sect_runbook_v1_6.md RATIFIED
  │   └── Closes 5 carry-forward OQs (CELL2-1, PROVENANCE-CACHE-TRUTH-1,
  │       CELL11-CACHE-SHA-KEY-1, V12-2-DOC-DRIFT-1, S213C-10)
  └── Block 2: t2_rome_runbook_v0_1.md + rome-patches-canonical.md v0.1 RATIFIED
      └── Q1-Q5 ratified; OQ-S217-2/3/4 opened for S2.18 resolution

S2.18 (REQUIRED — T.2 ROME EXECUTION):
  ├── Pre-pod operator dependency: OQ-S217-2 (L17 cache availability) resolved
  ├── Block A: pre-flight + R1.3-equivalent dry-run gate
  │   └── Empirical patch applicability verdicts → rome-patches-canonical.md v0.2
  ├── Block B: HC-2-equivalent dry-run
  │   ├── Resolves OQ-S216-1 (SHA pin), OQ-S216-2 (hparams), OQ-S216-3 (layer),
  │   │   OQ-S216-4/OQ-S217-4 (multi-token), OQ-S217-3 (API)
  │   └── Block B verdict: B-PASS / B-FAIL / B-PARTIAL
  └── Block C: 15-trial Stage 1 SECT v3 (if B-PASS)
      ├── PASS    → S2.19 = MEMIT-vs-ROME comparison framework finding update
      ├── FAIL    → S2.19 = T.2 GRACE runbook v0.1 authoring; S2.20 = GRACE execution
      │             ├── GRACE PASS → S2.21 = adapter-mechanism framework finding
      │             └── GRACE FAIL → fall back to T.1; S2.21 = T.1 alt-model runbook
      └── PARTIAL → operator-side verdict integrity binding re-evaluation
```

### §8.4 Operator decisions at S2.18 kickoff

| Decision | Required by |
|---|---|
| **OQ-S217-2 resolution** — L17 cache availability | Pre-pod-attach (REQUIRED before S2.18 Block A Cell 0 first execution) |
| **Session label confirmation** — `S2.18` to env_fingerprint manifest | Cell 1.5 first execution |
| **Concrete ROME SHA capture** — first execution captures latest stable tip | Cell 1 first execution |
| **R1.3-equivalent dry-run gate disposition** — accept declarative v0.1 OR adapt MEMIT R1.3 pattern at first execution | Cell 8 first execution |
| **Block B verdict adjudication** — B-PASS / B-FAIL / B-PARTIAL classification | Cell 13 |

---

## §9 — Session metadata

| Field | Value |
|---|---|
| Session date | 2026-05-04 |
| Session classification | SCOPING / authoring (no pod-side execution) |
| Session wall-time | Operator-side artifact authoring; no pod time |
| Pod | N/A — session was offline |
| Predecessor close | S2.16 (CLOSED 2026-05-04 — Framework Finding Archival + T-Branch Entry Scoping) |
| Successor entry | S2.18 — T.2 ROME execution |
| Session deliverables | 4 artifacts (v1.6 runbook + v0.1 ROME runbook + v0.1 ROME patches canonical + this summary) |
| Active patches canonical (MEMIT) | `memit-patches-canonical.md` v2.5 (UNCHANGED at S2.17; carry-forward MEMIT canonical) |
| Active patches canonical (ROME) | `rome-patches-canonical.md` v0.1 (NEW at S2.17 Block 2; declarative; v0.2 absorbs S2.18 Block A empirical applicability) |
| Active runbook (MEMIT) | `stage_1_sect_runbook_v1_6.md` RATIFIED at S2.17 Block 1 close (supersedes v1.5 PROVISIONAL) |
| Active runbook (ROME) | `t2_rome_runbook_v0_1.md` RATIFIED v0.1 at S2.17 Block 2 close (declarative; v0.2 absorbs S2.18 first-execution implementation) |
| Active corpus | `cfb-v3.yaml` v1.0 (UNCHANGED) — documentation mirror per D-S217-2 |
| Active probe set | `probe-set-v3.yaml` v1.0 (UNCHANGED) |
| Framework spec | `llm-as-database-v1_2-integrated-spec.md` (sealed; UNCHANGED) |
| MEMIT SHA pin | `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (UNCHANGED; preserved on NV; not consumed by T.2 ROME) |
| ROME SHA pin | TBD (latest stable tip; resolved at S2.18 Block A Cell 1 first execution) |
| Llama-3.1-8B revision SHA | `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` (UNCHANGED) |
| Permanent framework finding | `framework_finding_memit_ceiling_archival.md` v1.0 (preserved; load-bearing for T.2 ROME test design) |

---

## §10 — KB curation recommendations

For S2.18 entry, recommended active KB:

**Add:**
- `stage_1_sect_runbook_v1_6.md` (S2.17 Block 1 deliverable; carry-forward structural template)
- `t2_rome_runbook_v0_1.md` (S2.17 Block 2 deliverable; **load-bearing for S2.18 execution**)
- `rome-patches-canonical.md` v0.1 (S2.17 Block 2 deliverable; **load-bearing for S2.18 Block A Cell 2**)
- `session_2_17_summary_block.md` (this artifact; close artifact)

**Keep:**
- `framework_finding_memit_ceiling_archival.md` v1.0 (PERMANENT empirical context; on-demand reference)
- `t_branch_decision_document.md` v1.0 (decision rationale; methodology lock; referenced at runbook Part VII forward routing)
- `cfb-v3.yaml` v1.0 + `probe-set-v3.yaml` v1.0 (carry-forward canonical artifacts; documentation mirror under D-S217-2)
- `memit-patches-canonical.md` v2.5 (MEMIT canonical; preserved unmodified; on-demand for cross-reference at ROME canonical re-derivation)

**Remove (if S2.18 is the active session):**
- `stage_1_sect_runbook_v1_5.md` (predecessor MEMIT runbook; superseded by v1.6 RATIFIED at S2.17 Block 1 close; load-bearing context now in v1.6)
- `t2_rome_runbook_v0_1_authoring_plan.md` (S2.16 deliverable; defined S2.17 Block 2 scope; superseded by `t2_rome_runbook_v0_1.md` v0.1 itself)
- `session_2_16_summary_block.md` (predecessor session close; load-bearing context now in this S2.17 summary)
- `session_2_17_kickoff_prompt.md` (S2.17 entry prompt; no longer load-bearing)

The KB at S2.18 entry should focus context on: T.2 ROME runbook execution (v0.1 + v1.6 carry-forward), ROME patches reference, framework finding empirical context, and decision rationale.

---

*End of Session 2.17 Summary Block.*
