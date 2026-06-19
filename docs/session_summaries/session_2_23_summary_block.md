═══════════════════════════════════════════════════════════════════
# Session 2.23 — Summary Block
# T.1-α-MEMIT Runbook v0.1 Authoring
═══════════════════════════════════════════════════════════════════

**Session:** S2.23
**Type:** Authoring (declarative runbook; no pod execution)
**Predecessor:** S2.22 (T.1-GRACE-3B; ROUTE_A_HALT_MECHANISM_3B; NARROW_BY_DESIGN)
**Successor:** S2.24 (T.1-α-MEMIT execution)
**Routing source:** D-S222-S223-ROUTING-1
**Closed:** 2026-05-05
**Specialist set:** memit-specialist (primary), validation-contract-architect (Block B verdict surface), state-consistency-theorist (Block-end), framework-spec-writer (inheritance map + routing matrix)

---

## §1. Session Outcome

S2.23 produced `t1_alt_model_3b_memit_runbook v0.1` — a NEW declarative runbook for running MEMIT against `meta-llama/Llama-3.2-3B` at canonical hyperparameters, by structural inheritance from `stage_1_sect_runbook v1.7` with the base model swapped 8B → 3B and the covariance-cache computation re-authored from scratch. The runbook tests whether the v1.0 + v1.1 architectural-invariant ceiling generalizes across Llama-class scale or is Llama-3.1-8B-specific at this scale.

All three load-bearing inputs were confirmed present in the KB at session entry: `stage_1_sect_runbook v1.7`, `memit-patches-canonical v2.5`, `framework_finding_memit_ceiling_archival v1.2`. The `llama_3_2_3b_baselines.json` (S2.22 Checkpoint #1) was inspected and confirmed engine-agnostic and consistent with the kickoff's Cell 5 gate-consumer inversion.

---

## §2. Deliverables Produced

| ID | Artifact | Length | Status |
|---|---|---|---|
| 1 | `t1_alt_model_3b_memit_runbook v0.1` | 875 lines | DECLARATIVE — ready for S2.24 |
| 2 | `session_2_23_summary_block.md` | this artifact | close artifact |

The runbook contains all 21 cells (0–20, including 1.5), the inheritance map (§I), architecture-swap reference (§II), patch-inheritance matrix (§III), four-block cell decomposition (§IV–VII), halt-condition cross-index (§VIII), forward routing matrix (§IX), OQ slate (§X), decision/constraint registry (§XI), non-goals (§XII), and reference appendices (§XIII).

---

## §3. Decisions Ratified

| ID | Statement |
|---|---|
| D-S223-Q1-1 | Runbook structural inheritance verbatim from `stage_1_sect_runbook v1.7` with §6.1 substitutions |
| D-S223-Q2-1 | Cell 5 INVERTS to gate-consumer; first `C-S220-3` within Llama-3.2-3B chain (Checkpoint #2 under MEMIT) |
| D-S223-Q3-1 | Layer set `[2..6]` preserved per `D-S215D2-1`; NOT re-tuned at smaller scale (PROVISIONAL pending S2.24) |
| D-S223-Q4-1 | Cell 8 REWRITTEN — fresh cov computation; protocol per S2.15-D2 |
| D-S223-Q5-1 | Engine source snapshot at Cell 1 absorbing `OQ-S222-CELL1-2` |
| D-S223-COV-SCOPE-1 | Full L2-L6 cov computation (PROVISIONAL pending operator confirmation pre-S2.24; runbook defaults to full scope) |
| D-S223-PATCH-INHERITANCE-1 | All MEMIT patches per `memit-patches v2.5` §1 inherited; engine source byte-identical to 8B baseline (verified via patch-site line numbers at Cell 1.0) |

---

## §4. Constraints Established

| ID | Statement |
|---|---|
| C-S223-1 | MEMIT engine SHA pinning at Cell 1 entry; documented in Cell 20 manifest extension |
| C-S223-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` post-Cell-1; closes `OQ-S222-CELL1-2` |
| C-S223-3 | Cov-cache fresh-computation gate at Cell 8: per-layer file size + checksum per S2.15-D2 PROVENANCE protocol |
| C-S223-4 | Layer-set bound assertion at Cell 4: all of `[2..6]` within `0 ≤ idx < n_layer = 28` |
| C-S223-5 | Per-cell explicit Surface annotation (A vs B); inherits IC-S222-2 absorption surface |

---

## §5. Key Authoring Findings

§5.1 **The Cell 5 inversion is cross-engine.** The S2.22 baseline JSON was captured under the GRACE engine but is engine-agnostic — it records pre-edit forward-pass probabilities at the pinned model SHA, independent of editor. The `C-S220-3` gate at Cell 5 validly compares MEMIT-time model load against GRACE-time capture; the gate tests whether the model load is bit-identical across the engine swap. A FAIL would signal a cross-engine determinism break, not a baseline error. This was confirmed by direct inspection of the 38-probe baseline panel.

§5.2 **Cell 8 is the cost center and the structural pivot from GRACE.** MEMIT consumes per-layer covariance caches that GRACE did not. The 8B caches on NV are keyed on the 8B architecture and are useless for 3B, so Cell 8 is rewritten to compute fresh caches (~3 hour wall-time, ~4 GiB NV addition for L2-L6). P-5/P-6/P-7 are prerequisites: P-5 modernizes the dataset loader, P-6/P-7 construct the `_t100_` filename segment that makes the cache edit-time-visible. Without that segment the later edit-time lookup misses and falls back to a full-`npos` compute that OOMs.

§5.3 **Copy-Unmount is back in scope.** Under GRACE the runbook used adapter-detach (Copy-Unmount INAPPLICABLE). Under MEMIT the joint-overlay weight edit is reversed by bit-exact Copy-Unmount, inherited verbatim at Cell 11/15 with the IC-S23-4 HARD gate (drift `< 1e-4`).

§5.4 **Multi-token surface unchanged from S2.22.** cfb-v3-004 (`harp` → `[4960, 79]`) is the sole multi-token target; `MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}` carries forward verbatim. The four STRICT facts preserve cross-session bit-exact determinism at Cell 15 (the §1.5.3.3 absorption block does not execute for them).

§5.5 **VRAM headroom is comfortable.** Projected ~11–13 GiB peak vs 24 GiB ceiling (S2.22 GRACE-3B demonstrated 6.47 GiB; MEMIT adds cov-compute and edit-dispatch overhead). FAIL-at-environment is therefore the least likely of the three verdict routes.

---

## §6. Open Questions

### §6.1 Anticipated to OPEN at S2.24

| ID | Statement | Closes when |
|---|---|---|
| OQ-S224-1 | Per-layer cov-compute wall-time on RTX 4090 fp16 | Cell 8 execution |
| OQ-S224-2 | `mom2_update_weight=15000` correctly calibrated at 3B, or re-tune? | S2.24 verdict |
| OQ-S224-3 | Joint-overlay 5-fact dispatch peak VRAM (~13 GiB projection) | Cell 9/15 execution |
| OQ-S224-COV-SCOPE-1 | Full L2-L6 vs reduced single-layer scope | S2.24 entry (operator) |

### §6.2 Carried forward from S2.22

| ID | Disposition |
|---|---|
| OQ-S222-CELL1-2 | ABSORBED (Cell 1 snapshot; `C-S223-2`) |
| OQ-S222-CELL0-DEPS-1 | ABSORBED (Cell 0 explicit install) |
| OQ-S222-SURFACE-LABELING-1 | ABSORBED (per-cell annotation; `C-S223-5`) |
| OQ-S222-CELL-EXEC-VERIFICATION-1 | ABSORBED (acceptance strings) |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | CARRIED — must resolve before Cell 10/13 verdict at S2.24 |

### §6.3 Carried forward from S2.20 (still OPEN)

| ID | Disposition |
|---|---|
| OQ-S220-MANIFEST-1 | DEFERRED |
| OQ-S220-CFB-PATH-1 | DEFERRED (inherits S2.22 path verbatim) |

---

## §7. Forward Routing — S2.24

S2.24 is the T.1-α-MEMIT execution session. The Cell 13 verdict routes S2.25:

| S2.24 verdict | S2.25 scope | Framework finding implication |
|---|---|---|
| PASS | T.1-α-PASS post-routing (open scope); v1.3 amendment NARROWS ceiling to Llama-3.1-8B-specific at scale; WS3 permits MEMIT on smaller Llama | Architectural-invariant claim narrows |
| FAIL with installation | T.1-β alt-architecture authoring (Mistral-7B or Qwen-7B) | Ceiling generalizes across Llama-class scale |
| FAIL at environment | halt for triage (hardware migration / precision deliberation) | Orthogonal blocker |

### §7.1 Operator action required pre-S2.24

| Step | Action |
|---|---|
| 1 | Confirm `D-S223-COV-SCOPE-1` (full L2-L6 vs reduced single-layer) before Cell 8 |
| 2 | Resolve `OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1` (runbook §3.2.2 vs YAML §126 predicate gap) before Cell 10/13 verdict |
| 3 | Confirm NV headroom for ~4 GiB cov-cache addition |

---

## §8. KB Hygiene — Pre-S2.24 Entry

### §8.1 Load-bearing for S2.24 execution

| Document | Rationale |
|---|---|
| `t1_alt_model_3b_memit_runbook v0.1` | the runbook under execution |
| `memit-patches-canonical v2.5` | patch application at Cells 1.5/2 |
| `cfb-v3.yaml v1.0` | corpus reference |
| `probe-set-v3.yaml v1.0` | probe reference |
| `llama_3_2_3b_baselines.json` | Cell 5 gate-consumer source |
| `session_2_23_summary_block.md` | predecessor reference |

### §8.2 Recommended removals at S2.24 entry

| Document | Rationale |
|---|---|
| `framework_finding v1.2` | routing rationale absorbed; re-upload on demand for v1.3 authoring |
| `t_branch_decision_document v1.1` | routing rationale absorbed into this runbook |
| GRACE-side artifacts (already removed at S2.23 per kickoff §10.2) | INAPPLICABLE for MEMIT execution |

---

## §9. Mirror Sync (Operator-Side)

Per two-tier storage discipline (D-S210-6), sync S2.23 authoring outputs from `/mnt/user-data/outputs/` to the durable archive tier at `/Volumes/memit/llm-database-poc-mirror/` via rsync (direct TCP `-e` flag; excludes for `hf_cache`; SHA-256 spot-check post-sync). Artifacts to sync: `t1_alt_model_3b_memit_runbook_v0_1.md`, `session_2_23_summary_block.md`.

---

## §10. Session Close Posture

S2.23 is an authoring session; no pod state changed, no NV writes occurred, no verdict was rendered. The runbook is declarative and forward-compatible against S2.24 execution. The architectural-invariant ceiling claim (v1.0 + v1.1) is untouched — T.1-α exists to test its scale-generalization, and that test is an S2.24 execution outcome, not an S2.23 authoring outcome.

═══════════════════════════════════════════════════════════════════
**Session 2.23 CLOSED 2026-05-05.**
**Persistence:** `/mnt/user-data/outputs/session_2_23_summary_block.md`
═══════════════════════════════════════════════════════════════════
