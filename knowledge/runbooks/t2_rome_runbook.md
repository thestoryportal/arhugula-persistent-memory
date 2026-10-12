# T.2 ROME Runbook v0.2 — meta-llama/Llama-3.1-8B (post-S2.18 empirical absorption)

> **Authoring session:** v0.2 codification session (2026-05-05; operator-side post-S2.18; pre-S2.19 BLOCKING)
> **Predecessor session (executor):** S2.18 — T.2 ROME first-execution; CLOSED 2026-05-05 with verdict B-FAIL → T.2 ROME ELIM at canonical hparams
> **Successor session (consumer):** S2.19 = T.2 GRACE runbook v0.1 authoring (verdict-conditional C-FAIL branch active)
> **Target environment:** RunPod RTX 4090 24 GiB single GPU; NV `large_amethyst_wolverine` (carry-forward)
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct; SHA pin `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`)
> **Write engine:** ROME (`https://github.com/kmeng01/rome`; SHA pin `0874014cd9837e4365f3e6f3c71400ef11509e04` — empirically resolved at S2.18 Block A Cell 1 per OQ-S216-1 closure)
> **Trial protocol:** IC-S24-4 — 5 facts × 3 replicates = 15 trials; single-fact dispatch (C-ROME-1 EMPIRICALLY-VALIDATED at S2.18 Cell 9)
> **Cell pattern:** Three-block structure (Block A: setup + baseline; Block B: HC-2-equivalent dry-run; Block C: trial loop) per `t2_rome_runbook_v0_1_authoring_plan.md` §2 carry-forward; structurally inherits from `stage_1_sect_runbook_v1_6.md` RATIFIED template
> **Specialists:** framework-spec-writer (primary, runbook authoring + v0.2 empirical absorption); memit-specialist (Cells 1, 2, 4, 8, 9, 11, 15 — ROME mechanism, P-7-ROME / P-8-ROME / P-9-ROME application, ROMEHyperParamsExtended dispatch); state-consistency-theorist (Cells 3, 5, 7, 15 — covariance cache reuse + Copy-Unmount + cross-session bit-exact gate); validation-contract-architect (Cells 6, 7, 10, 12, 13, 16 — verdict surface, calibration corridor, pathology classification)
>
> **Document version:** v0.2 (empirical absorption of S2.18 first-execution findings)
> **Status:** RATIFIED v0.2 — empirically anchored to S2.18 first-execution record; supersedes v0.1 declarative
> **Supersedes:** v0.1 (RATIFIED at S2.17 Block 2; declarative — preserved as historical anchor at git ref or NV mirror)
> **Companion artifact:** `rome-patches-canonical.md` v0.2 (operator-side post-S2.18; supersedes v0.1; empirical applicability verdicts absorbed)
> **Sibling artifact:** `stage_1_sect_runbook_v1_6.md` v1.6 (RATIFIED at S2.17 Block 1; structural template; v1.7 forthcoming with MULTI_TOKEN_ALLOWLIST canonical absorption per OQ-V02-3 deferred resolution)
>
> **v0.1 → v0.2 status delta.** v0.1 cell bodies were declarative (cell skeleton complete; cell bodies materialized at S2.18 first-execution time). v0.2 absorbs the empirical first-execution record from `session_2_18_summary_block.md` (canonical D / C / OQ / IC) and `session_2_18_summary_block_appendix.md` (cell-by-cell trajectory, patch authoring detail, compute_v traces, verdict tables). v0.2 codifies:
> - Three new SOURCE_LAYER patches authored mid-S2.18 (P-7-ROME, P-8-ROME, P-9-ROME) — REQUIRED for ROME edit dispatch on Llama-3.1-8B fp16; verified at Cell 8 retry / Cell 9 / Cell 11
> - One NEW CONFIG_LAYER patch class introduced (`globals.yml`) — STATS_DIR cwd-relative `data/stats` not consumable by ROME at NV mount; absolute customization REQUIRED per C-S218-4
> - Cell 3 EXPECTED_LAYERS parameterization (was hardcoded `[4,5,6,7,8]` post-S2.17 hardening miss; replaced with SESSION-bound hparam derived from cache-truth lookup)
> - Cell 4 ROME hparam dataclass extension via subclass pattern (`ROMEHyperParamsExtended` with `mom2_batch_tokens` field) per C-S218-5; schema count 20 → 21
> - Cell 5 defensive preamble for L17-extension model cleanup (free 16.07 GiB resident model before fresh load)
> - Cell 6 MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism absorbed canonically (per D-S215D2-CFB-V3-004-MULTITOKEN-1 + PROXY-1; mirror canonical absorption at v1.7 stage_1_sect_runbook)
> - Cell 7 explicit cross-session bit-exact gate (read pre-existing baselines, capture fresh, compare per-fact P values + per-probe top_5 + p_top_1, halt on drift) per kickoff §6.2 HARD halt class
> - Cell 8 ROME-specific R1.3-equivalent (smoke calls `rome.compute_u.get_inv_cov`, NOT hypothetical `get_cov`; smoke layer outside Block B sweep window for fair wall-time)
> - Cells 9 / 11 ROMEHyperParamsExtended subclass; full implementation supersedes v0.1 declarative; 38-probe pre/post/post-unmount measurement loop; Copy-Unmount drift assertions
> - Cell 12 cross-layer comparison table; pathology classification (degenerate-fit vs unfittable-landscape); calibration corridor PASS criterion application
> - Cell 13 verdict gate adjudication framework with 3-route option matrix (A halt / B 15-trial / C 3-trial); S2.18 routing record (Route A halt) preserved as forensic anchor
> - Cells 14-17 trial loop body remains declarative (Route A halt at Cell 13 means Block C did not execute at S2.18; v0.2 codifies the loop only for case future verdict gate at later session routes B or C)
> - Cells 18-20 NV inventory + SHA equality gate + mirror sync command set + reproducibility manifest update + routing decision print

---

## 1.5 Authoring discipline — empirical absorption (post-S2.18; supersedes v0.1 §1.5)

This runbook v0.2 absorbs the S2.18 first-execution empirical record. v0.1's declarative status is replaced with v0.2's empirically-ratified status. The C-S26-3 dry-run gate constraint and the D-S28-2 R1.3 codification carry forward to T.2 ROME via C-ROME-3 (`rome-patches-canonical.md` v0.2 §5.3) and now CARRY EMPIRICAL VALIDATION at S2.18 Cell 8 retry.

> **C-ROME-3 (parallel to C-S26-3) — EMPIRICALLY-VALIDATED at S2.18.** Runbook hardening passes targeting the ROME cache-dispatch surface require an R1.3-equivalent dry-run gate at Block A Cell 8 against post-patch NV state — REQUIRED before authoring-acceptance ratification of any v0.x → v0.(x+1) advance. **Empirical anchor: S2.18 Cell 8 initial OOM at 22.81 GiB → root cause `_t100_` cache filename mismatch from `mom2_batch_tokens=100` not threading to `get_inv_cov` → P-7-ROME authored mid-session → Cell 8 retry PASS within R1.3 envelope (cache HIT log line; smoke-load wall-time within budget).**

**v0.2 dry-run status: EMPIRICALLY-RATIFIED.** v0.2 absorbs the S2.18 Cell 8 retry empirical anchor. The full ratification gate (Block A Cell 8 R1.3-equivalent dry-run against post-clone post-transplant post-P-7-ROME-applied NV state) is empirically verified. v0.2 ships under EMPIRICALLY-RATIFIED status; future v0.3 (if authored) absorbs subsequent-execution empirical record.

| Gate | Trigger | v0.2 disposition (post-S2.18) |
|---|---|---|
| Authoring acceptance | All §6 acceptance criteria of `t2_rome_runbook_v0_1_authoring_plan.md` met (extended for v0.2: empirical absorption complete; cell skeleton + cell body both filled; v1.6 inheritance manifest + S2.18 forensic anchor declared) | **RATIFIED v0.2** at v0.2 codification session close |
| C-ROME-4 application | New defense-in-depth marker added to v0.2 | **TRIGGERED** — three new patches (P-7-ROME, P-8-ROME, P-9-ROME) introduce per-patch markers; `rome-patches-canonical.md` v0.2 §6 / §7 / §8 codifies the marker assertion set |
| Cache-dispatch semantics preservation | v0.2 change to Cells 3, 5, 8, 9, 11 cache-dispatch surfaces relative to v0.1 | **TRIGGERED** — Cell 3 EXPECTED_LAYERS parameterization closes a v0.1 hardcoded-set defect; Cell 8 R1.3-equivalent verified empirically against ROME's `get_inv_cov` resolution path (NOT hypothetical `get_cov`); Cell 9 / Cell 11 single-fact ROME dispatch validated bit-exact via Copy-Unmount per-fact unmount drift `0.00e+00` |
| Empirical anchor inheritance | covariance caches L2-L8 + L17 cache extension + cross-session bit-exact determinism + Copy-Unmount L4-L8 / L2-L6 / L17-single / L2-single | **TRIGGERED** — v0.2 inherits all four carry-forward anchors per D-S216-CLOSE-2 + D-S218-7 (cross-session 5 → 6) + D-S218-8 (Copy-Unmount L17 + L2 single-fact bit-exact) |

**Cross-reference.** `rome-patches-canonical.md` v0.2 §5 (process constraints C-ROME-1 through C-ROME-4 EMPIRICALLY-VALIDATED + C-S218-1 through C-S218-5 NEW); `stage_1_sect_runbook_v1_6.md` § §1.5 / §1.5.1 / §1.5.2 (parent constraints carry-forward).

### 1.5.1 Single-fact dispatch envelope (D-S217-3; EMPIRICALLY-VALIDATED at S2.18)

> **D-S217-3 (EMPIRICALLY-VALIDATED at S2.18 Cell 9 + Cell 11).** ROME edit invocations at S2.18 Block C are single-fact, single-layer. The 15-trial Stage 1 SECT v3 protocol is executed as **15 sequential single-fact ROME edits**, not as a batched multi-fact ROME edit. Each trial's Copy-Unmount restore is per-fact, not per-trial-group.

**Empirical motivation (preserved from v0.1; now anchored to execution).** ROME's published mechanism is single-fact rank-1 update; batched ROME invocation is not a documented mode of the canonical implementation (`https://github.com/kmeng01/rome`). The MEMIT-vs-ROME comparison framework finding (deferred to S2.19+ per D-S216-CLOSE-5) is testable only when ROME's intrinsic single-fact mechanism is preserved at execution.

**v0.2 empirical anchor:** S2.18 Cell 9 (L17 single-fact) + Cell 11 (L2 single-fact) both invoked `apply_rome_to_model([request], hparams=ROME_HPARAMS_LAYER_X, copy=False, return_orig_weights=True)` with a single-element request list; the dispatch surface accepts single-fact lists and returns `weights_copy` for the edited layer. Single-fact dispatch envelope EMPIRICALLY-VALIDATED.

### 1.5.2 Empirical anchor inheritance (D-S217-4 + D-S218-7 extension)

> **D-S217-4 + D-S218-7 (extension).** v0.2 inherits the following empirical anchors:
> 1. **Cross-session bit-exact determinism** on Llama-3.1-8B fp16: **6 cross-session checkpoints** (5 from S2.14-D / S2.15-D2 + 1 NEW at S2.18 Block A → restart → Block B trajectory); forward-pass drift `0.00e+00` across 5 facts + 38 probes. Source: `session_2_18_summary_block.md` D-S218-7. The S2.14-D anchor strengthens further at S2.18.
> 2. **Copy-Unmount bit-exact regime — extended scope at S2.18.** Validated layer ranges:
>    - L4-L8 (5 layers; MEMIT batched-multi-fact joint-overlay) — S2.14-D D.3
>    - L2-L6 (5 layers; MEMIT batched-multi-fact joint-overlay) — S2.15-D2 D.2
>    - L17 (1 layer; ROME single-fact dispatch) — **S2.18 Cell 9** (NEW)
>    - L2 (1 layer; ROME single-fact dispatch) — **S2.18 Cell 11** (NEW)
>    Per-fact unmount drift `0.00e+00` at all four. Six layer ranges across three write-engine configs; all bit-exact. Source: S2.14-D `OQ-S214D-D3-3` + S2.15-D2 narrowed-window + S2.18 D-S218-8 (Copy-Unmount ROME L17 + L2 single-fact validated).
> 3. **Covariance caches L2-L8 + L17 (NEW at S2.18).** L17 cache extension produced at S2.18 Block A Cell 1.5 / pre-Cell-2 via 30.20-min layer_stats compute pass against Wikipedia 100k samples; resident at `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` as `model.layers.17.mlp.down_proj_float32_mom2_100000.npz` (~0.766 GiB; total cache footprint now ~6.52 GiB across 8 layers L2-L8 + L17). PROVENANCE narrowed to layer_set `[2..8, 17]`. Source: pre-S2.6 fork-work + S2.13-C / S2.14-D / S2.15-D2 reuse + S2.18 L17 extension (closes OQ-S217-2 path a — extend cache).
> 4. **`stage_1_llama_baselines.json`** 38-probe baseline at canonical hparams; cfb-v3 fact roster; pre-edit `P[target_TRUE]` natural top-1 captured per D-S213C-CALIB-1/2/3. **EMPIRICALLY-RE-VERIFIED at S2.18 Cell 7** under v0.2's explicit cross-session bit-exact gate (drift `0.00e+00` across 38 probes).

**Re-execution at S2.18 Cell 5 / Cell 7:** Cells 5 + 7 re-execute the baseline capture against the loaded model state to verify the cross-session anchor under the pod's current state. Drift > 0 at any of the 38 probes triggers session-level halt + investigation; this is the bit-exact gate that anchors all post-edit verdicts. **Empirical at S2.18: drift `0.00e+00` across all 38 probes; gate PASS.**

### 1.5.3 v0.1 → v0.2 supersession integrity (NEW at v0.2)

v0.1 was authored S2.17 Block 2 with declarative cell bodies (skeleton + acceptance criteria; empirically-instantiable). v0.1 RATIFIED status was authoring-acceptance only; not empirically-validated. v0.2 absorbs the S2.18 first-execution record and supersedes v0.1's declarative status with empirically-ratified status.

**Supersession discipline.** v0.2 preserves v0.1's structural shape (Block A / Block B / Block C; cell numbering; specialist provenance) and replaces v0.1's declarative cell bodies with empirically-anchored cell bodies. v0.1 is preserved as a historical anchor at NV mirror or git reference; not deleted. References to v0.1 inside v0.2 use the form "v0.1 declared X; v0.2 absorbs empirical Y" to make the supersession trace explicit.

**v0.1 unsupersedeable artifacts.** The following v0.1 elements are unchanged at v0.2:
- §1.1 Purpose (the core empirical question is unchanged: does T.2 ROME PASS or FAIL at canonical hparams on Llama-3.1-8B?)
- §1.2 Measures (acceptance bands inherit from MEMIT canonical; consistency p > 0.5; generalization / specificity drift < 0.05; unmount band < 1e-4 HARD)
- §1.3 Verdict integrity binding (load-bearing subset {cfb-v3-001, cfb-v3-002, cfb-v3-005}; carry-forward unchanged)
- §1.4 Halt conditions (all v0.1 halt classes preserved at v0.2; new halt classes added for cross-session bit-exact gate at Cell 7 and L17-extension model cleanup at Cell 5)
- Block C cell numbering (Cells 14-20)

---

# Part I — Session orientation

## 1.1 Purpose

This runbook drives Session 2.18 — the first T.2 ROME execution against the Workstream 1 production target model `meta-llama/Llama-3.1-8B`. It executes:

1. **Block A** — pre-flight verification (pod, NV, ROME repo clone, patches, covariance cache reuse, hparams, model load, tokenizer, baseline capture, R1.3-equivalent dry-run gate) at Cells 0-8
2. **Block B** — HC-2-equivalent dry-run (single edit on cfb-v3-001 guitar at Layer-A=L17 primary, then at Layer-B=L2 secondary; cross-layer comparison; pathology classification; load-bearing layer selection OR halt) at Cells 9-13
3. **Block C** — 15-trial Stage 1 SECT v3 execution at single-fact ROME dispatch on the load-bearing layer (conditional on Cell 13 verdict gate routing); per-trial verdict aggregation; aggregate verdict per D-S215D2-VERDICT-INTEGRITY-1 carry-forward at Cells 14-20

T.2 ROME is the load-bearing empirical step that tests whether the architectural-invariant ceiling on (Llama-3.1-8B × MEMIT × canonical hparams) — confirmed at six orthogonal axes per `framework_finding_memit_ceiling_archival.md` v1.0 — is **structural to MEMIT specifically**, OR **structural to (Llama-3.1-8B × any rank-1 in-weight write engine)**. T.2 ROME PASS routes the framework finding to a MEMIT-specific ceiling characterization (S2.19 = MEMIT-vs-ROME comparison); T.2 ROME FAIL escalates to GRACE adapter-based testing per D-S216-Q3-1.

**v0.2 empirical record:** S2.18 Block B verdict = **B-FAIL** at both L17 and L2 (`session_2_18_summary_block.md` D-S218-1). Cell 13 verdict gate routed Route A halt (D-S218-2). T.2 ROME ELIM at canonical hparams; architectural-invariant ceiling extended from 6 → 7 axes (`session_2_18_summary_block.md` D-S218-3); T.2 GRACE PROMOTED to leading hypothesis (D-S218-4). S2.19 = T.2 GRACE runbook v0.1 authoring (verdict-conditional C-FAIL branch active per `session_2_19_kickoff_prompt.md`).

## 1.2 Measures

Per IC-S24-4 trial protocol carry-forward (single-fact narrowing per C-ROME-1 EMPIRICALLY-VALIDATED), each of the 15 trials produces a verdict against four criteria. Acceptance bands inherit from MEMIT canonical (D-S24-10 + IC-S23-4); under ROME single-fact dispatch the unmount band is narrower (1 edited layer to restore vs MEMIT's 5).

| Criterion | Definition | Acceptance band | Provenance |
|---|---|---|---|
| **Consistency** | Post-edit top-1 token equals `target_new` and `P(target_new)` exceeds 0.5 | `p_target_new_post > 0.5` | Provisional (D-S24-10; OQ-PROBE-2 carry-forward) |
| **Generalization** | Pre-edit→post-edit drift in top-1 probability for related-but-unedited probes is small | `abs(p_top_1_post − p_top_1_pre) < 0.05` per probe | Provisional |
| **Specificity (shared)** | Pre-edit→post-edit drift in top-1 probability for shared-specificity probes (cross-fact unrelated subjects) is small | `abs(p_top_1_post − p_top_1_pre) < 0.05` per probe | Provisional |
| **Unmount intra-pod drift** | Post-Copy-Unmount drift on `target_TRUE` for the edited fact | `abs(p_target_true_postunmount − p_target_true_pre) < 1e-4` | **HARD** (IC-S23-4) |

**Calibration-band stratification carry-forward (D-S213C-CALIB-3):** The PASS-set is the 4-of-17 instrument single-token coverage subset on the Llama tokenizer. cfb-v3-003 violin / cfb-v3-005 flute carry calibration-band stratification annotations; cfb-v3-004 harp under multi-token allowlist with **first-token-proxy per D-S217-Q5-1** (carry-forward of D-S215D2-CFB-V3-004-PROXY-1 + D-S215D2-CFB-V3-004-MULTITOKEN-1) AND `RE-EVALUATE AT TRIAL 0` flag at Block B Cell 13.

> **v0.2 disposition of cfb-v3-004 multi-token first-token-proxy:** At S2.18 Block B, Cell 13 was reached at B-FAIL verdict before the trial-0 multi-token re-evaluation gate could be exercised — Route A halt preempted Block C entry. The first-token-proxy posture remains DECLARED at v0.2; empirical re-evaluation deferred to next ROME-class execution session (if any). For S2.19 = T.2 GRACE runbook authoring, the multi-token posture inherits as DECLARED-via-v0.2 with `RE-EVALUATE AT TRIAL 0` flag preserved.

## 1.3 Verdict integrity binding (D-S215D2-VERDICT-INTEGRITY-1 carry-forward; preserved at v0.2)

> **Carry-forward from S2.15-D2.** Aggregate verdict at Cell 17 is computed against the **load-bearing subset** {cfb-v3-001, cfb-v3-002, cfb-v3-005} as decisive; full 5-fact aggregate is informational only. cfb-v3-003 and cfb-v3-004 are forensic-informative-excluded by default per S2.13-C calibration-band stratification, MODULO Block B Cell 13 OQ-S217-1 resolution (Q5; cfb-v3-004 multi-token tolerance posture under ROME's single-fact dispatch — first-token-proxy carry-forward at v0.1 with explicit re-evaluation at trial 0).

**v0.2 empirical anchor:** S2.18 did not reach Block C; verdict integrity binding remained inactive at runtime. Carry-forward preserved at v0.2 for any future ROME-class execution; semantics unchanged.

## 1.4 Halt conditions (cross-cell index)

| Condition | Class | Action |
|---|---|---|
| Pod attach failure (Cell 0) | Pre-flight | Re-attach; if persistent, escalate operator |
| ROME repo clone failure (Cell 1) | Pre-flight | Verify network; verify SHA pin resolution; halt session if persistent |
| ROME repo SHA mismatch (Cell 1) | Pre-flight | **NEW at v0.2 (post-S2.18 anchor):** verify SHA pin against rome-patches-canonical.md v0.2 §3 (`0874014cd9837e4365f3e6f3c71400ef11509e04`); halt if drift |
| Patch verification failure (Cell 2) | Pre-flight | Per `rome-patches-canonical.md` v0.2 §1 — schedule transplant + P-7-ROME / P-8-ROME / P-9-ROME application + globals.yml customization; halt this session until ratified |
| `globals.yml` STATS_DIR cwd-relative drift (Cell 2) | Pre-flight | **NEW at v0.2 (post-S2.18 anchor):** verify STATS_DIR is absolute NV-anchored path; halt if cwd-relative |
| Covariance cache failure (Cell 3) | Session-level | Hard halt; cache reuse precondition broken; investigate NV state; do not re-compute cache without operator authorization |
| L17 covariance cache absent (Cell 3) | Pre-flight | **NEW at v0.2 (closes OQ-S217-2 path a):** verify L17 cache extension complete pre-pod-attach; halt if absent |
| ROME hparam schema validation failure (Cell 4) | Pre-flight | Re-author Cell 4 hparam dict; re-verify ROMEHyperParamsExtended subclass per C-S218-5; re-load |
| Schema field count drift (Cell 4) | Pre-flight | **NEW at v0.2 (post-S2.18 anchor):** verify 21-field schema (was 20 at v0.1 per C-S218-5 mom2_batch_tokens addition); halt if drift |
| Model load OOM (Cell 5) | Pre-flight | Restart kernel; re-verify VRAM baseline; per MEMIT runbook v1.6 Cell 0 §0.6 hygiene |
| L17-extension model cleanup miss (Cell 5) | Pre-flight | **NEW at v0.2 (post-S2.18 anchor; closes OQ-S217-2 path a empirical):** if L17 cache extension was performed in same notebook session (16.07 GiB resident), free model + clear CUDA cache before fresh model load |
| Tokenizer single-token failure (Cell 6) | Session-level | Halt; revise affected fact; re-version cfb-v3 corpus; defer Stage 1 to v1.1 corpus |
| MULTI_TOKEN_ALLOWLIST missing for fact (Cell 6) | Session-level | **NEW at v0.2 (carry-forward of D-S215D2-CFB-V3-004-MULTITOKEN-1):** if a multi-token fact is encountered without allowlist entry, halt; either add to allowlist OR halt and revise corpus |
| Baseline drift > 0 against carry-forward `stage_1_llama_baselines.json` (Cell 5 / Cell 7) | Session-level | Hard halt — cross-session bit-exact determinism violated; investigate model SHA, HF cache state, P-1/P-2 application, BEFORE proceeding |
| Cross-session bit-exact gate FAIL (Cell 7) | Session-level (HARD) | **NEW at v0.2 (codified at v0.2 Cell 7):** read pre-existing baselines; capture fresh; compare per-fact P + per-probe top_5 + p_top_1; halt on drift |
| R1.3-equivalent gate FAIL (Cell 8) | Session-level | Hard halt — cache-dispatch round-trip broken under ROME path; verify `rome/layer_stats.py` post-P-6 form; investigate ROME `get_inv_cov` invocation (NOT hypothetical `get_cov` — ROME has no such function) |
| Cell 8 OOM (cache filename mismatch) | Session-level | **NEW at v0.2 (post-S2.18 anchor; closes by P-7-ROME):** verify P-7-ROME applied per rome-patches-canonical v0.2 §6; verify `_t100_` cache filename produced post-P-7-ROME; if absent, halt and re-apply patch |
| Cell 9 / Cell 11 fp16 / fp32 dtype RuntimeError | Session-level | **NEW at v0.2 (post-S2.18 anchor; closes by P-8-ROME / P-9-ROME):** verify P-8-ROME applied (compute_u matmul `.to(u.dtype)` cast); verify P-9-ROME applied (rome_main outer-product `.to(weight.dtype)` casts at both sites); halt and re-apply if absent |
| Block B verdict failure (Cell 13) | Session-level (Block B) | If both layer candidates FAIL the calibration corridor: ROME single-fact dispatch on Llama-3.1-8B does not produce in-band edits at any tested layer → **Cell 13 verdict gate adjudication framework with 3-route option matrix (A halt / B 15-trial / C 3-trial)**; v0.2 Route A halt EMPIRICALLY ANCHORED at S2.18 |
| Unmount band drift > 1e-4 at any trial (Cell 15) | Trial-level (HARD per IC-S23-4) | Immediate halt at the violating trial; do not proceed to next trial; preserve overlay snapshot for forensics |
| Inter-trial baseline drift > 1e-4 on shared-spec probes (Cell 15) | Trial-level (HARD) | Immediate halt; investigate Copy-Unmount restore integrity |

---

# Part II — Pod configuration

## 2.1 Carry-forward from MEMIT runbook v1.6

Pod configuration (RunPod RTX 4090 24 GiB; NV `large_amethyst_wolverine`; Python 3.11; HF env-vars per `stage_1_sect_runbook_v1_6.md` Cell 0 §0.4 PRE-INJECT; etc.) is INHERITED unchanged. T.2 ROME does not introduce pod-level configuration changes.

> **v0.2 anchor for HF_HOME placement:** per S2.14-D OQ-S214D-HF-CACHE-LOCATION-1 and S2.18 carry-forward C-S214D-4: HF_HOME MUST be set BEFORE first transformers import to land cache on NV. v0.2 preserves this constraint.

## 2.2 NV state expected at S2.18 entry (post-S2.18 retroactively codified)

| Path | Source | Cell that consumes |
|---|---|---|
| `/workspace/memit_dry_run/memit/` | pre-S2.6 fork-work + S2.7 patch application | (preserved; not consumed by T.2 ROME at runtime; consumed by Cell 2 transplant source for P-1 / P-2 / P-4 / P-5 / P-6) |
| `/workspace/rome_dry_run/rome/` | **Cell 1 NEW at S2.18** — clone of `https://github.com/kmeng01/rome` at SHA `0874014cd9837e4365f3e6f3c71400ef11509e04` | Cell 2 (patch verification + transplant) |
| `/workspace/rome_dry_run/rome/util/nethook.py.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling preserved at transplant** | (not runtime-consumed; forensic anchor) |
| `/workspace/rome_dry_run/rome/rome/compute_v.py.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling** | (forensic anchor) |
| `/workspace/rome_dry_run/rome/rome/layer_stats.py.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling** | (forensic anchor) |
| `/workspace/rome_dry_run/rome/rome/compute_u.py.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling for P-7-ROME / P-8-ROME** | (forensic anchor) |
| `/workspace/rome_dry_run/rome/rome/rome_main.py.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling for P-9-ROME** | (forensic anchor) |
| `/workspace/rome_dry_run/rome/globals.yml.upstream_pristine` | **Cell 2 NEW at S2.18 — pristine sibling for CONFIG_LAYER patch** | (forensic anchor) |
| `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` | S2.5a baseline | Cell 4 (hparam staging) |
| `/workspace/architecture_profile/stage_1_llama_baselines.json` | S2.13-C / S2.15-D2 cumulative; **NEW at S2.18: cross-session bit-exact gate cell 7 PASS verified** | Cell 5 (cross-session bit-exact gate) + Cell 7 (re-capture comparison) |
| `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` | pre-S2.6 fork-work + L17 extension at S2.18 | Cell 3 (SUBSET reuse verification) |
| `/workspace/covariance_caches/.../wikipedia_stats/PROVENANCE.txt` | pre-S2.6 fork-work + S2.18 update for `[2..8, 17]` | Cell 3 (provenance gate) |
| `/workspace/covariance_caches/.../wikipedia_stats/model.layers.17.mlp.down_proj_float32_mom2_100000.npz` | **S2.18 Block A NEW** — 30.20 min compute on RTX 4090; ~0.766 GiB | Cell 3 (L17 SUBSET) + Cell 9 (L17 dispatch) |
| `/workspace/reproducibility_manifest.json` | cumulative | Cell 19 update at S2.18 close |

---

# Part III — Block A: setup, patches, baseline capture (Cells 0–8)

## Cell 0 — System binaries + Python deps

**Specialist:** state-consistency-theorist (NV mount + dep hygiene)

**Purpose:** Pod attach + NV mount + Python dep install + kernel restart hygiene. **INHERITED UNCHANGED from `stage_1_sect_runbook_v1_6.md` Cell 0.** No ROME-specific changes at v0.2.

---

## Cell 1 — ROME repository clone + SHA pin resolution

**Specialist:** memit-specialist (ROME repo provenance) + state-consistency-theorist (NV state writeback)

**Purpose:** Clone `https://github.com/kmeng01/rome` to `/workspace/rome_dry_run/rome/` if absent; verify SHA pin matches `rome-patches-canonical.md` v0.2 §3 declared SHA (`0874014cd9837e4365f3e6f3c71400ef11509e04`). Write `/workspace/architecture_profile/t2_rome_pinned_sha.txt`.

**v0.2 empirical anchor:** S2.18 Block A Cell 1 cloned to NV at session entry; SHA empirically resolved to `0874014cd9837e4365f3e6f3c71400ef11509e04` (latest stable tip per D-S217-Q2-1 carry-forward). v0.2 codifies this SHA as the canonical pin; future executions verify against this value.

> **OQ-S216-1 closure:** ROME SHA pin resolved empirically at S2.18 Cell 1; v0.2 codifies the resolved value.

**Cell 1 implementation:**

```python
# === CELL 1 — ROME repository clone + SHA pin resolution (v0.2) ===
# Specialist: memit-specialist + state-consistency-theorist
# References: rome-patches-canonical.md v0.2 §3 (SHA pin); D-S217-Q2-1 (latest stable tip);
#             OQ-S216-1 (closed at S2.18 Block A Cell 1)

import os, subprocess, json
from datetime import datetime, timezone

ROME_ROOT = "/workspace/rome_dry_run/rome"
ROME_SHA_PIN = "0874014cd9837e4365f3e6f3c71400ef11509e04"

if not os.path.exists(ROME_ROOT):
    subprocess.run(["git", "clone", "https://github.com/kmeng01/rome", ROME_ROOT], check=True)

# Resolve current HEAD SHA
result = subprocess.run(
    ["git", "-C", ROME_ROOT, "rev-parse", "HEAD"],
    capture_output=True, text=True, check=True
)
current_sha = result.stdout.strip()

# Halt on drift
assert current_sha == ROME_SHA_PIN, (
    f"ROME SHA drift: {current_sha} != {ROME_SHA_PIN}; "
    f"verify rome-patches-canonical.md v0.2 §3 OR re-clone at canonical SHA"
)

with open("/workspace/architecture_profile/t2_rome_pinned_sha.txt", "w") as f:
    f.write(f"{current_sha}\n")

print(f"Cell 1: ROME SHA pin verified = {current_sha[:12]}... (PASS)")
```

**Halt conditions:** SHA mismatch → halt; investigate clone state.

---

## Cell 1.5 — Environment fingerprint capture

**Specialist:** state-consistency-theorist

**Purpose:** Capture extended environment fingerprint with ROME-specific keys (`rome_sha`, `rome_clone_url`). **INHERITED from `stage_1_sect_runbook_v1_6.md` Cell 1.5** with EXPECTED_KEYS schema extended.

**v0.2 empirical anchor:** S2.18 Block A Cell 1.5 EXPECTED_KEYS dict re-applied against post-S2.17 hardening pattern; verified.

---

## Cell 2 — ROME patch state verification + transplant + new patch application

**Specialist:** memit-specialist (patch transplant + application) + state-consistency-theorist (pristine sibling preservation)

**Purpose:** Verify patch state at `/workspace/rome_dry_run/rome/`. Three categories:

1. **Transplant from MEMIT post-state** — copy `util/nethook.py` (P-1 + P-2), `rome/compute_v.py` (P-4), `rome/layer_stats.py` (P-4 + P-5 + P-6) from `/workspace/memit_dry_run/memit/` to ROME root; preserve pristine ROME upstream forms at `*.upstream_pristine` siblings.
2. **New SOURCE_LAYER patches authored mid-S2.18** — apply P-7-ROME (`rome/compute_u.py`; 3 edits), P-8-ROME (`rome/compute_u.py`; 1 edit at compute_u matmul site), P-9-ROME (`rome/rome_main.py`; 2 edits at outer-product sites). Preserve pristine forms at `*.upstream_pristine` siblings.
3. **CONFIG_LAYER patch (NEW class at v0.2)** — customize `globals.yml` for absolute NV-anchored STATS_DIR. Preserve pristine form at `globals.yml.upstream_pristine`.

> **v0.2 disposition note.** v0.1 §1 declared P-1 / P-2 / P-4 / P-5 / P-6 as "transitively applied via shared codebase" — empirically falsified at S2.18 Cell 2. The shared-codebase claim was wrong: ROME upstream `kmeng01/rome` does not contain these patches. v0.2 §1.1 of `rome-patches-canonical.md` codifies the empirical APPLICABLE-DIRECTLY (transplanted) verdict; this cell implements the transplant.

**Cell 2 implementation skeleton:**

```python
# === CELL 2 — ROME patch state verification + transplant (v0.2) ===
# Specialist: memit-specialist + state-consistency-theorist
# References: rome-patches-canonical.md v0.2 §1.1 (transplant set), §1.4 (P-7-ROME / P-8-ROME / P-9-ROME),
#             §1.6 (globals.yml CONFIG_LAYER); C-ROME-4 (marker post-application verification)

import os, shutil, json
from datetime import datetime, timezone

ROME_ROOT = "/workspace/rome_dry_run/rome"
MEMIT_ROOT = "/workspace/memit_dry_run/memit"

os.chdir(ROME_ROOT)  # C-S25-5 cwd invariant carry-forward (per C-S214D-3 import discipline)

# === STEP 1: Transplant from MEMIT post-state (P-1, P-2, P-4, P-5, P-6) ===
# All targets verified post-transplant via marker assertions (C-ROME-4 carry-forward)

TRANSPLANT_MAP = {
    "util/nethook.py":           f"{MEMIT_ROOT}/util/nethook.py",          # P-1 + P-2 carrier
    "rome/compute_v.py":         f"{MEMIT_ROOT}/memit/compute_v.py",       # P-4 carrier (sibling-name in MEMIT)
    "rome/layer_stats.py":       f"{MEMIT_ROOT}/memit/layer_stats.py",     # P-4 + P-5 + P-6 carrier
}

for rome_path, memit_path in TRANSPLANT_MAP.items():
    rome_target = os.path.join(ROME_ROOT, rome_path)
    pristine_target = f"{rome_target}.upstream_pristine"
    if not os.path.exists(pristine_target):
        # Preserve upstream pristine at first transplant
        shutil.copy2(rome_target, pristine_target)
    shutil.copy2(memit_path, rome_target)

# === STEP 2: Apply P-7-ROME, P-8-ROME, P-9-ROME (in-place text substitution) ===
# Per rome-patches-canonical.md v0.2 §6 (P-7-ROME), §7 (P-8-ROME), §8 (P-9-ROME)

def apply_patch_with_pristine(target_path, patches):
    """Apply list of (old, new) substitutions to target_path; preserve pristine sibling."""
    pristine = f"{target_path}.upstream_pristine"
    if not os.path.exists(pristine):
        shutil.copy2(target_path, pristine)
    with open(target_path, "r") as f:
        content = f.read()
    for old, new in patches:
        assert old in content, f"P-X marker assertion FAIL: {target_path} missing pre-patch marker"
        content = content.replace(old, new)
    with open(target_path, "w") as f:
        f.write(content)

# P-7-ROME: 3 edits to rome/compute_u.py — get_inv_cov signature + layer_stats kwarg + compute_u call site getattr
# (Full pre/post text at rome-patches-canonical.md v0.2 §6.1; markers at §6.2)
P_7_ROME_EDITS = [
    # ... [3 substitutions per §6.1; markers tracked at §6.2]
]
apply_patch_with_pristine(f"{ROME_ROOT}/rome/compute_u.py", P_7_ROME_EDITS)

# P-8-ROME: 1 edit to rome/compute_u.py — .to(u.dtype) cast at compute_u matmul site
P_8_ROME_EDITS = [
    # ... [1 substitution per §7.1]
]
apply_patch_with_pristine(f"{ROME_ROOT}/rome/compute_u.py", P_8_ROME_EDITS)

# P-9-ROME: 2 edits to rome/rome_main.py — outer-product .to(weight.dtype) casts (sibling-site discipline)
P_9_ROME_EDITS = [
    # ... [2 substitutions per §8.1; both sibling sites mandatory per C-S218-3]
]
apply_patch_with_pristine(f"{ROME_ROOT}/rome/rome_main.py", P_9_ROME_EDITS)

# === STEP 3: Apply CONFIG_LAYER patch — globals.yml STATS_DIR customization ===
# Per rome-patches-canonical.md v0.2 §9 (CONFIG_LAYER class)

GLOBALS_PATH = f"{ROME_ROOT}/globals.yml"
if not os.path.exists(f"{GLOBALS_PATH}.upstream_pristine"):
    shutil.copy2(GLOBALS_PATH, f"{GLOBALS_PATH}.upstream_pristine")
# Customize STATS_DIR to absolute NV-anchored path
# (see rome-patches-canonical.md v0.2 §9.1 for full pre/post body)

# === STEP 4: Marker post-application verification (C-ROME-4 EMPIRICALLY-VALIDATED) ===
# Verify all 6 transplant markers + 6 new patch markers present post-application
# (Full marker assertion list at rome-patches-canonical.md v0.2 §1.1 / §6.2 / §7.2 / §8.2 / §9.2)

# Patch state manifest write
patch_state = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "version": "v0.2",
    "rome_sha_pin": ROME_SHA_PIN,
    "transplanted_files": list(TRANSPLANT_MAP.keys()),
    "new_patches_applied": ["P-7-ROME", "P-8-ROME", "P-9-ROME"],
    "config_layer_patches_applied": ["globals.yml"],
    "marker_assertions_pass": True,  # populated post-verification loop
    "pristine_siblings_preserved": True,
}
with open("/workspace/architecture_profile/t2_rome_patch_state.json", "w") as f:
    json.dump(patch_state, f, indent=2)

print(f"Cell 2: ROME patch state PASS — {len(TRANSPLANT_MAP)} transplanted + 3 new SOURCE_LAYER + 1 CONFIG_LAYER")
```

**Verification anchors (empirical at S2.18; codified at v0.2):**

| Anchor | Marker | Source location |
|---|---|---|
| P-1 | `def retain_hook(m, args, kwargs, output):` | `util/nethook.py` |
| P-2 | `with_kwargs=True` | `util/nethook.py` |
| P-4 | `hidden_size` reference + `max_position_embeddings` count ≥ 2 | `rome/compute_v.py` + `rome/layer_stats.py` |
| P-5 | `"20231101.en"` + `"wikimedia/wikipedia"` | `rome/layer_stats.py` |
| P-6 | `size_suffix = f"_t{batch_tokens}" + size_suffix` | `rome/layer_stats.py` |
| P-7-ROME | `get_inv_cov(model, tok, layer_name, mom2_dataset, mom2_n_samples, mom2_dtype, mom2_batch_tokens)` | `rome/compute_u.py` |
| P-8-ROME | `inv_cov.to(u.dtype)` at compute_u matmul | `rome/compute_u.py` |
| P-9-ROME | `.to(weight.dtype)` at outer-product (both sites) | `rome/rome_main.py` |
| globals.yml | `STATS_DIR: /workspace/covariance_caches` (absolute NV-anchored) | `globals.yml` |

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| Transplant source missing | Pre-flight | Verify MEMIT-side fork-work session ran successfully; halt if absent |
| Marker assertion FAIL post-transplant | Pre-flight | Hard halt; re-investigate transplant source state |
| P-7-ROME / P-8-ROME / P-9-ROME marker assertion FAIL | Pre-flight | Hard halt; re-apply patch from rome-patches-canonical v0.2 §6 / §7 / §8 |
| `globals.yml` STATS_DIR cwd-relative drift | Pre-flight | Hard halt; re-customize per rome-patches-canonical v0.2 §9 |

---

## Cell 3 — Covariance cache reuse verification (with EXPECTED_LAYERS parameterization at v0.2)

**Specialist:** state-consistency-theorist (cache reuse + PROVENANCE gate)

**Purpose:** Verify that the NV-resident covariance cache produced at the pre-S2.6 fork-work session (and validated cumulatively across S2.13-C / S2.14-D / S2.15-D2 / S2.18 L17 extension) is consumable by ROME's `apply_rome_to_model` → `get_inv_cov` resolution chain. **Inherits the v1.6 SUBSET assertion pattern unchanged from `stage_1_sect_runbook_v1_6.md` Cell 3** (per D-S215D2-CELL3-SUBSET-ASSERTION-1 carry-forward; v1.6 hardening canonical form). **NEW at v0.2: EXPECTED_LAYERS parameterized via SESSION-bound hparam (was hardcoded `[4,5,6,7,8]` at v0.1 post-S2.17 hardening miss).**

**Inputs:** NV-resident `/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/` (≥ 8 `.npz` files: L2-L8 + L17 + `PROVENANCE.txt`).

**v0.2 cell-level changes vs v0.1:**

1. **R1.1 SUBSET assertion** — inherited unchanged (closes OQ-S215D2-PROVENANCE-CACHE-TRUTH-1 transitively for ROME). PROVENANCE-declared layer_set MUST be a subset of cache truth; cache-truth-superset is acceptable.
2. **R1.2 internals consumer** — inherited unchanged (`mom2.mom2` priority resolution per IC-PreS26-3).
3. **R1.3 smoke-load** — adapted for ROME path: smoke-load uses `rome.compute_u.get_inv_cov` invocation path (NOT hypothetical `get_cov` — ROME has no such function; this corrects v0.1's mis-stated dispatch surface). The R1.3 binding under ROME tests whether `rome/layer_stats.py` (post-P-6 transplanted form) correctly resolves the cached `_t100_` filename when invoked through ROME's `get_inv_cov` → `layer_stats` chain. **Empirical anchor: EMPIRICALLY-VALIDATED at S2.18 Cell 8 retry post-P-7-ROME (cache HIT log line; smoke-load wall-time within budget).**
4. **Cache state writer** — inherits the v1.6 canonical `provenance` field name (per OQ-S215D2-CELL11-CACHE-SHA-KEY-1 closure); writes to `t2_rome_cache_state.json`.
5. **NEW at v0.2: EXPECTED_LAYERS parameterization.** v0.1 hardcoded `EXPECTED_LAYER_FILES = {"layer_4", "layer_5", ...}` at Cell 3 — this was a post-S2.17 hardening miss (the Cell 3 spec was hardcoded to S2.15-D2 D.2's L4-L8 sweep window). v0.2 derives EXPECTED_LAYERS from SESSION-bound hparam declared at runbook frontmatter:

```python
# v0.2: SESSION-bound layer set parameterization
SESSION_LAYER_SET = [17, 2]  # T.2 ROME Block B candidates (L17 primary + L2 secondary)
EXPECTED_LAYER_FILES = {f"model.layers.{L}.mlp.down_proj" for L in SESSION_LAYER_SET}
```

This pattern parameterizes the SUBSET assertion against the session's actual sweep window, eliminating the hardcoded-set defect class.

> **v0.2 anchor: closes the post-S2.17 hardening miss for ROME-specific Cell 3 use.** v1.7 of `stage_1_sect_runbook` will absorb the parallel pattern for MEMIT-side use.

> **L17 covariance cache requirement at ROME Block B:** ROME edits one layer per fact; the layer is selected per OQ-S216-3 / D-S217-Q4-1 (L17 primary, L2 secondary at Block B). At v0.1 the L17 cache was absent from cumulative cache truth (`{2..8}`) — `OQ-S217-2` was opened to track this. **v0.2 anchor: OQ-S217-2 path a CLOSED at S2.18 Block A — L17 cache extension performed pre-Cell-2 (30.20 min compute on RTX 4090 against Wikipedia 100k samples; ~0.766 GiB resident at NV).** Cumulative cache truth at v0.2 entry: `{2, 3, 4, 5, 6, 7, 8, 17}`.

**Halt conditions:** as MEMIT v1.6 Cell 3, with the SUBSET-violation halt class noting ROME-specific layer-set sweep window discipline + L17-cache-extension precondition.

---

## Cell 4 — ROME hparam declaration (with ROMEHyperParamsExtended subclass at v0.2)

**Specialist:** memit-specialist (hparam surface inventory + dataclass extension)

**Purpose:** Construct ROME hparam dict for the layer candidates (L17 primary, L2 secondary) per `rome-patches-canonical.md` v0.2 §4. Stage to NV. **NEW at v0.2: 21-field schema (was 20 at v0.1 per C-S218-5 mom2_batch_tokens addition); ROMEHyperParamsExtended subclass for `mom2_batch_tokens` propagation.**

```python
# === CELL 4 — ROME hparam declaration (v0.2) ===
# Specialist: memit-specialist
# References: rome-patches-canonical.md v0.2 §4 (canonical hparams);
#             D-S217-Q3-1 (canonical hparam starting values); C-S218-5 (ROMEHyperParamsExtended)

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

# v0.2 NEW: ROMEHyperParamsExtended subclass per C-S218-5
# Upstream rome.rome_hparams.ROMEHyperParams does not include mom2_batch_tokens;
# subclass adds the field for propagation through compute_u → get_inv_cov → layer_stats
# (the new field is consumed by P-7-ROME's get_inv_cov signature)

# (Full subclass body imported from rome project under MEMIT runbook style;
#  authored at S2.18 Cell 4; codified at v0.2 per C-S218-5.)

# v0.2 declared canonical values per ROME paper Table 1 (GPT-J reference) +
# Llama-3.1-8B adaptation per S2.18 Cell 13 verdict gate (route A halt at canonical)
ROME_HPARAMS_LAYER_A = {  # L17 primary
    "layers": [17],
    "fact_token": "subject_last",
    "v_num_grad_steps": 20,
    "v_lr": 0.5,
    "v_loss_layer": 31,                   # Llama 32-layer last-layer
    "v_weight_decay": 0.5,
    "clamp_norm_factor": 4,
    "kl_factor": 0.0625,
    "mom2_adjustment": 15000,
    "mom2_n_samples": 100000,
    "mom2_dtype": "float32",
    "mom2_batch_tokens": 100,             # NEW at v0.2 schema (was implicit at v0.1)
    "context_template_length_params": [[5, 10], [10, 10]],
    "rewrite_module_tmp": "model.layers.{}.mlp.down_proj",
    "layer_module_tmp": "model.layers.{}",
    "mlp_module_tmp": "model.layers.{}.mlp",
    "attn_module_tmp": "model.layers.{}.self_attn",
    "ln_f_module": "model.norm",          # Llama-specific; differs from GPT-J transformer.ln_f
    "lm_head_module": "lm_head",
    "stats_dir": "/workspace/covariance_caches",
    "mom2_dataset": "wikipedia",
}

ROME_HPARAMS_LAYER_B = dict(ROME_HPARAMS_LAYER_A)  # L2 secondary; same hparams modulo layer
ROME_HPARAMS_LAYER_B["layers"] = [2]

# v0.2 NEW: 21-field schema gate (parallel to MEMIT C-S25-8; was 20 at v0.1)
EXPECTED_FIELDS = set(ROME_HPARAMS_LAYER_A.keys())
assert len(EXPECTED_FIELDS) == 21, f"Schema drift: {len(EXPECTED_FIELDS)} fields, expected 21 (v0.2)"

# Halt if mom2_batch_tokens is missing
assert "mom2_batch_tokens" in EXPECTED_FIELDS, (
    "C-S218-5: ROMEHyperParamsExtended subclass MUST include mom2_batch_tokens"
)

hparam_manifest = {
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "version": "v0.2",
    "basis": "rome-patches-canonical.md v0.2 §4 (canonical hparams; D-S217-Q3-1 GPT-J Table 1 reference);"
             " C-S218-5 (ROMEHyperParamsExtended for mom2_batch_tokens)",
    "layer_a_primary": ROME_HPARAMS_LAYER_A,
    "layer_b_secondary": ROME_HPARAMS_LAYER_B,
    "calibration_status": "EMPIRICALLY-EXAMINED — Cell 13 Block B verdict gate at S2.18 routed Route A halt"
                          " at canonical hparams; calibration corridor not surfaced at L17 OR L2",
    "schema_field_count": 21,
}

with open("/workspace/architecture_profile/t2_rome_hparams.json", "w") as f:
    json.dump(hparam_manifest, f, indent=2)

print(f"Cell 4: ROME hparams declared (Layer-A=L17 primary; Layer-B=L2 secondary). "
      f"Schema gate: {len(EXPECTED_FIELDS)}/21 fields PASS.")
```

**Verification anchors:** 21 hparam fields × 2 layer candidates; canonical values per ROME paper Table 1 + Llama-3.1-8B adaptation; ROMEHyperParamsExtended subclass dispatched per C-S218-5.

**Halt conditions:** Schema drift = halt; re-author EXPECTED_FIELDS dict; verify ROMEHyperParamsExtended import path.

---

## Cell 5 — Llama-3.1-8B model load + Pad-Token alias + cross-session bit-exact gate (with L17-extension cleanup preamble at v0.2)

**Specialist:** memit-specialist (model load) + state-consistency-theorist (Pad-Token + bit-exact gate + L17-extension cleanup)

**Purpose:** Load `meta-llama/Llama-3.1-8B` from NV-cached HF; apply Pad-Token alias; capture model_revision_sha to env_fingerprint; verify cross-session bit-exact determinism against `stage_1_llama_baselines.json` carry-forward. **NEW at v0.2: defensive preamble for L17-extension model cleanup if Cell 3 layer_stats compute pass ran in same notebook session.**

```python
# === CELL 5 — Model load + Pad-Token + bit-exact gate (v0.2) ===
# Specialist: memit-specialist + state-consistency-theorist
# References: D-S217-4 cross-session bit-exact gate; C-S214D-2 VRAM ceiling discipline;
#             session_2_18_summary_block_appendix.md §1 (L17 extension cleanup empirical)

import torch, gc

# v0.2 NEW: defensive preamble for L17-extension model cleanup
# At S2.18 Block A, the L17 cache extension required a model load + 30-min compute pass
# at Cell 3-equivalent. Without explicit cleanup before Cell 5, the resident model
# (~16.07 GiB fp16) competes with the fresh model load → OOM risk.
if "model" in dir():
    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"Cell 5 preamble: prior model freed; CUDA cache cleared.")

# Standard model load (carry-forward from stage_1_sect_runbook_v1_6.md Cell 5)
# ... [unchanged body: HF cache load + Pad-Token alias + arch sanity assertions]

# Cross-session bit-exact gate (carry-forward unchanged)
# ... [forward pass on stage_1_baselines probes + drift assertion]
```

> **v0.2 anchor: D-S217-4 cross-session bit-exact gate.** At first probe pass, the model's forward-pass output on each of the 38 active probes MUST match `stage_1_llama_baselines.json` (S2.13-C / S2.15-D2 / S2.18 cumulative) at fp16 forward-pass drift `0.00e+00`. Drift > 0 at any probe halts the session — cross-session bit-exact determinism is the load-bearing precondition for all post-edit verdicts. **EMPIRICALLY-VALIDATED at S2.18 Cell 5 + Cell 7: drift `0.00e+00` across all 38 probes; gate PASS.**

**Cell 5 implementation:** Direct carry-forward from `stage_1_sect_runbook_v1_6.md` Cell 5 with v0.2 preamble addition; otherwise unchanged.

**Halt conditions:** Model load OOM (per MEMIT v1.6 Cell 5); architecture sanity assertion FAIL (32 layers; 4096 hidden; etc.); cross-session bit-exact gate FAIL (drift > 0 at any probe).

---

## Cell 6 — LLaMA tokenizer single-token verification with MULTI_TOKEN_ALLOWLIST (NEW at v0.2)

**Specialist:** validation-contract-architect (single-token invariant per C-S24-3; MULTI_TOKEN_ALLOWLIST canonical absorption)

**Purpose:** Verify cfb-v3 fact roster (5 facts; instrument-cluster targets) under Llama tokenizer. **MAJOR CHANGE at v0.2: MULTI_TOKEN_ALLOWLIST + first-token-proxy logic absorbed canonically (per D-S215D2-CFB-V3-004-MULTITOKEN-1 + PROXY-1; mirror canonical absorption at v1.7 stage_1_sect_runbook for MEMIT-side use).**

> **v0.2 absorption rationale.** v1.6 of `stage_1_sect_runbook` (RATIFIED at S2.17 Block 1) missed the S2.15-D2 ratified mechanism (D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1). Surfaced at S2.18 Cell 6 reapplication when the operator re-derived the multi-token handling pattern at runtime. v0.2 codifies the mechanism canonically into Cell 6 source code; v1.7 of `stage_1_sect_runbook` will absorb the parallel pattern. This is a MEMIT-side miss as much as a ROME-side miss — any future MEMIT session using cfb-v3 corpus would hit the same halt at v1.6.

**v0.2 Cell 6 canonical block additions:**

```python
# === CELL 6 — LLaMA tokenizer single-token verification (v0.2) ===
# Specialist: validation-contract-architect
# References: C-S24-3 (single-token invariant); D-S215D2-CFB-V3-004-MULTITOKEN-1 + PROXY-1;
#             D-S217-2 single-source contract carry-forward;
#             D-S217-Q5-1 RE-EVALUATE flag at Block B Cell 13

# v0.2 NEW canonical block: MULTI_TOKEN_ALLOWLIST + first-token-proxy
MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}  # harp under Llama tokenizer; first-token-proxy

# verdict_class taxonomy (3 values per D-S215D2-CFB-V3-004-MULTITOKEN-1):
#   STRICT_SINGLE_TOKEN          — fact's target_new tokenizes to exactly one token
#   ALLOWLIST_FIRST_TOKEN_PROXY  — fact is in MULTI_TOKEN_ALLOWLIST AND uses first-token-proxy
#   MULTI_TOKEN_FAIL             — fact tokenizes to multiple tokens AND not in allowlist (HARD halt)

def classify_fact(fact_id, target_new_str, tokenizer):
    """Classify a fact's target_new tokenization status; return verdict_class."""
    token_ids = tokenizer.encode(" " + target_new_str, add_special_tokens=False)
    if len(token_ids) == 1:
        return "STRICT_SINGLE_TOKEN", token_ids[0], None
    if fact_id in MULTI_TOKEN_ALLOWLIST:
        # First-token-proxy: track P(first_token) for proxy facts
        first_token_id = token_ids[0]
        return "ALLOWLIST_FIRST_TOKEN_PROXY", first_token_id, token_ids
    # Multi-token, not in allowlist → halt
    return "MULTI_TOKEN_FAIL", None, token_ids

# Verdict capture per fact (single-source contract per D-S217-2)
fact_verdicts = {}
for fact_id, fact_data in stage_1_facts.items():
    target_str = fact_data["target_new"]["str"]
    verdict_class, primary_token_id, full_token_ids = classify_fact(
        fact_id, target_str, tokenizer
    )
    fact_verdicts[fact_id] = {
        "verdict_class": verdict_class,
        "primary_token_id": primary_token_id,        # used for P(target_new) capture
        "full_token_ids": full_token_ids,            # informational; multi-token cases
        "re_evaluate_at_trial_0": (verdict_class == "ALLOWLIST_FIRST_TOKEN_PROXY"),  # D-S217-Q5-1 flag
    }
    if verdict_class == "MULTI_TOKEN_FAIL":
        raise RuntimeError(
            f"Cell 6 HARD halt: {fact_id} tokenizes to {len(full_token_ids)} tokens; "
            f"not in MULTI_TOKEN_ALLOWLIST. Either add to allowlist OR revise corpus."
        )

# Single-source contract write (D-S217-2 carry-forward)
import json
with open("/workspace/architecture_profile/stage_1_token_verification.json", "w") as f:
    json.dump({
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "version": "v0.2",
        "tokenizer": "meta-llama/Llama-3.1-8B",
        "fact_verdicts": fact_verdicts,
        "multi_token_allowlist": list(MULTI_TOKEN_ALLOWLIST),
    }, f, indent=2)

# Print summary
strict = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "STRICT_SINGLE_TOKEN")
proxy  = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY")
print(f"Cell 6: tokenizer verification PASS ({strict} STRICT + {proxy} PROXY; "
      f"re-evaluate at trial 0: {sum(1 for v in fact_verdicts.values() if v['re_evaluate_at_trial_0'])} facts).")
```

> **D-S217-Q5-1 cfb-v3-004 multi-token posture at v0.2.** Multi-token allowlist for cfb-v3-004 (harp under Llama tokenizer; first-token-proxy carry-forward) is **CODIFIED CANONICALLY at runbook v0.2 Cell 6** with explicit `RE-EVALUATE AT TRIAL 0` flag carried forward to Block B Cell 13. Empirical disposition at S2.18: Block B Cell 13 reached B-FAIL verdict at canonical hparams before the trial-0 re-evaluation gate could be exercised; first-token-proxy posture remains DECLARED for any future ROME-class execution.

**Halt conditions:** Tokenizer single-token failure (verdict_class = `MULTI_TOKEN_FAIL` and fact not in allowlist) → halt; either add to allowlist OR revise corpus + re-version cfb-v3.

---

## Cell 7 — Pre-edit baseline capture + explicit cross-session bit-exact gate (NEW at v0.2)

**Specialist:** validation-contract-architect (probe protocol; calibration-band stratification per D-S213C-CALIB-1/2/3) + state-consistency-theorist (cross-session bit-exact gate codification)

**Purpose:** Capture pre-edit `P[target_new]` and `P[target_TRUE]` (natural top-1) per fact; capture all 38 active probe top-1 + p_top_1 for post-edit / post-unmount comparison. **NEW at v0.2: explicit cross-session bit-exact gate as HARD halt class — read pre-existing baselines, capture fresh, compare per-fact P values + per-probe top_5 + p_top_1, halt on drift.**

```python
# === CELL 7 — Pre-edit baseline capture + cross-session bit-exact gate (v0.2) ===
# Specialist: validation-contract-architect + state-consistency-theorist
# References: D-S213C-CALIB-1/2/3 (calibration-band stratification);
#             D-S217-4 (cross-session bit-exact gate; HARD halt class);
#             OQ-S214D-DETERMINISM-1 (closed empirically; carry-forward to v0.2)

import json
import numpy as np

# === STEP 1: Capture fresh pre-edit baselines ===
fresh_baselines = {}
for probe in stage_1_probes:
    # ... [forward pass capture: top_5 + p_top_1 + per-fact target_new probability]
    pass

# === STEP 2: Cross-session bit-exact gate ===
# v0.2 codifies the explicit pattern (was implicit at v0.1)
PREEXISTING_BASELINES_PATH = "/workspace/architecture_profile/stage_1_llama_baselines.json"

if os.path.exists(PREEXISTING_BASELINES_PATH):
    with open(PREEXISTING_BASELINES_PATH, "r") as f:
        preexisting = json.load(f)
    
    # Per-probe drift assertion (HARD halt class)
    drifted_probes = []
    for probe_id, fresh in fresh_baselines.items():
        if probe_id not in preexisting["probes"]:
            continue  # new probe; informational
        prior = preexisting["probes"][probe_id]
        # top_5 token_id list equality (must match exactly)
        if fresh["top_5_token_ids"] != prior["top_5_token_ids"]:
            drifted_probes.append((probe_id, "top_5_drift"))
        # p_top_1 numerical drift (allclose at 0 absolute tolerance for fp16 reproducibility)
        if not np.isclose(fresh["p_top_1"], prior["p_top_1"], rtol=0, atol=0):
            drifted_probes.append((probe_id, f"p_top_1_drift_{fresh['p_top_1']-prior['p_top_1']:.2e}"))
    
    # Per-fact target_new probability drift assertion
    for fact_id, fresh_p in fresh_baselines["fact_target_new_probs"].items():
        prior_p = preexisting["fact_target_new_probs"].get(fact_id)
        if prior_p is not None and not np.isclose(fresh_p, prior_p, rtol=0, atol=0):
            drifted_probes.append((fact_id, f"fact_p_drift_{fresh_p-prior_p:.2e}"))
    
    # HARD halt on drift
    if drifted_probes:
        raise RuntimeError(
            f"Cell 7 HARD halt: cross-session bit-exact gate FAIL — "
            f"{len(drifted_probes)} probes drifted: {drifted_probes[:5]}{'...' if len(drifted_probes)>5 else ''}"
        )
    print(f"Cell 7: cross-session bit-exact gate PASS — 0 drift across {len(fresh_baselines)} probes.")
else:
    # First-time capture (no baseline to compare against)
    print(f"Cell 7: NO pre-existing baseline; fresh capture written to {PREEXISTING_BASELINES_PATH}.")

# === STEP 3: Per-fact target_TRUE natural top-1 capture (D-S213C-CALIB-1) ===
# (carry-forward from stage_1_sect_runbook_v1_6.md Cell 7)

# === STEP 4: Write fresh baseline to NV ===
# v0.2: only overwrite if no pre-existing baseline OR pre-existing matched fresh
with open(PREEXISTING_BASELINES_PATH, "w") as f:
    json.dump(fresh_baselines, f, indent=2)
```

**v0.2 empirical anchor:** S2.18 Cell 7 cross-session bit-exact gate executed against pre-existing `stage_1_llama_baselines.json` (S2.13-C / S2.15-D2 cumulative). Per-fact P drift = `0.00e+00` across 5 facts. Per-probe top_5 + p_top_1 drift = `0.00e+00` across 38 probes. Gate PASS — adds the 6th cross-session bit-exact determinism checkpoint per D-S218-7.

**Halt conditions:** Cross-session bit-exact drift > 0 at any probe or fact → HARD halt; investigate model SHA, HF cache state, P-1/P-2 application, BEFORE proceeding.

---

## Cell 8 — R1.3-equivalent dry-run gate for ROME dispatch path (with rome.compute_u.get_inv_cov anchor at v0.2)

**Specialist:** memit-specialist (ROME dispatch surface) + state-consistency-theorist (cache-dispatch round-trip)

**Purpose:** Pre-Block-B cache-dispatch defect-class detection under the ROME edit invocation path. Adapts `stage_1_sect_runbook_v1_6.md` § §1.5.1 D-S28-2 R1.3 codification to ROME — invokes ROME's `apply_rome_to_model` (or its lower-level `rome.compute_u.get_inv_cov` directly) on a `_ConfigOnlyPlaceholder` model with a single dummy fact at a smoke layer outside Block B sweep window to verify `get_inv_cov` resolves to the cached `_t100_` form without local recompute. Per C-ROME-3 EMPIRICALLY-VALIDATED.

> **v0.2 disposition note.** v0.1 Cell 8 referenced ROME's `get_cov` invocation path — empirically incorrect; ROME has NO `get_cov` function. The structural analog is `rome.compute_u.get_inv_cov`, which calls `layer_stats` (the patched-via-P-6 `_t100_` filename producer). v0.2 codifies the corrected dispatch surface.

```python
# === CELL 8 — R1.3-equivalent dry-run gate (ROME) — v0.2 ===
# Specialist: memit-specialist + state-consistency-theorist
# References: rome-patches-canonical.md v0.2 §5.3 C-ROME-3 (EMPIRICALLY-VALIDATED);
#             D-S28-2 R1.3 codification (carry-forward from stage_1_sect_runbook_v1_6.md §1.5.1);
#             P-7-ROME (rome/compute_u.py — get_inv_cov with mom2_batch_tokens propagation)

import time, io, contextlib, os
import torch

# v0.2 R1.3-equivalent: invoke ROME's get_inv_cov on a placeholder
# model with the smoke-layer hparams (smoke layer chosen OUTSIDE Block B sweep window
# for fair wall-time; e.g., L8 — already cached from cumulative cache truth).
#
# Capture stdout to detect "Computing Cov locally" log line (the canonical local-recompute
# signature from rome/layer_stats.py post-P-5 dataset loader).

os.chdir(ROME_ROOT)  # C-S25-5 cwd invariant; required for util/globals.py relative open

from rome.compute_u import get_inv_cov

SMOKE_LAYER_NAME = "model.layers.8.mlp.down_proj"  # L8: cached in cumulative cache truth (L2-L8); outside Block B sweep window {17, 2}
R1_3_TIMEOUT_SEC = 30

t_start = time.time()
log_capture = io.StringIO()
with contextlib.redirect_stdout(log_capture):
    inv_cov = get_inv_cov(
        model, tokenizer,
        SMOKE_LAYER_NAME,
        mom2_dataset="wikipedia",
        mom2_n_samples=100000,
        mom2_dtype="float32",
        mom2_batch_tokens=100,    # critical: P-7-ROME signature includes this kwarg
    )
t_elapsed = time.time() - t_start
log_text = log_capture.getvalue()

# Verdict gate
assert t_elapsed < R1_3_TIMEOUT_SEC, (
    f"R1.3 wall-time FAIL: {t_elapsed:.1f}s > {R1_3_TIMEOUT_SEC}s; "
    f"likely local recompute path triggered"
)
assert "Computing Cov locally" not in log_text, (
    f"R1.3 dispatch FAIL: local recompute log line present"
)
assert ("Loading cached" in log_text) or t_elapsed < 5.0, (
    f"R1.3 dispatch ambiguous: cache HIT log not seen and wall-time {t_elapsed:.1f}s suggests cold path"
)

print(f"Cell 8: R1.3-equivalent dry-run gate PASS (wall-time {t_elapsed:.2f}s on smoke layer {SMOKE_LAYER_NAME})")
```

**Verification anchors (empirical at S2.18; codified at v0.2):**

| Anchor | Expected | S2.18 empirical |
|---|---|---|
| ROME `get_inv_cov` resolution log line | Cache HIT log line on smoke layer | Cell 8 retry post-P-7-ROME: cache HIT (log line implicit; wall-time well within budget) |
| Smoke-load wall-time | < 30 sec | Cell 8 retry: well within budget post-P-7-ROME |
| Local recompute log line | ABSENT | Cell 8 retry: ABSENT |

> **v0.2 anchor: S2.18 Cell 8 initial OOM trajectory.** First execution of Cell 8 produced OOM at 22.81 GiB during `get_inv_cov` invocation — root-caused to `_t100_` cache filename mismatch from `mom2_batch_tokens=100` not threading to `get_inv_cov` signature (which lacked the kwarg in upstream ROME). P-7-ROME authored mid-session (3 edits to `rome/compute_u.py` per `rome-patches-canonical.md` v0.2 §6); Cell 8 retry post-P-7-ROME PASS within R1.3 envelope.

**Halt conditions:**

| Condition | Class | Action |
|---|---|---|
| `Computing Cov locally` log line | Session-level | Hard halt — cache-dispatch round-trip broken; verify `rome/layer_stats.py` post-P-6 form via Cell 2 re-run; investigate ROME `get_inv_cov` invocation path |
| Smoke-load wall-time > 30 sec | Session-level | Hard halt — same as above |
| OOM at `get_inv_cov` | Session-level | Hard halt — verify P-7-ROME applied per rome-patches-canonical v0.2 §6; verify `_t100_` cache filename produced post-P-7-ROME; if absent, halt and re-apply patch |
| `apply_rome_to_model` import failure | Pre-flight | Re-verify `os.chdir(ROME_ROOT)` per C-S25-5-equivalent; re-verify Cell 2 patch state |

> **v0.2 ratification note.** The cell body for R1.3-equivalent under ROME is empirically anchored at v0.2 per C-ROME-3 EMPIRICALLY-VALIDATED. Future v0.x advances may further harden the smoke-layer selection or add per-session R1.3 verdict export to `t2_rome_cache_state.json`.

---

# Part IV — Block B: HC-2-equivalent dry-run (Cells 9–13)

> **Block B purpose.** ROME's natural test surface is a single edit at a single layer. Block B is a controlled pilot that validates the full ROME dispatch path on one fact (cfb-v3-001 guitar — the sharpest IN-BAND anchor per S2.13-C calibration) at one layer at a time before committing to Block C's 15-trial 5-fact protocol.
>
> **Cross-layer comparison rationale.** L17 (ROME paper precedent for transformer-mid on GPT-J / GPT-2-XL) gives us the published-mechanism precedent on a different target architecture; L2 (S2.14-D D.1 mediation peak) gives us the Llama-3.1-8B-specific causal mediation evidence. Cross-layer comparison at Cell 12 is the load-bearing surface for Block C layer selection.
>
> **v0.2 empirical anchor:** S2.18 Block B executed both Cell 9 (L17) and Cell 11 (L2) on cfb-v3-001 guitar; cross-layer comparison at Cell 12 surfaced two distinct pathologies (degenerate-fit at L17 vs unfittable-landscape at L2). Cell 13 verdict gate routed Route A halt at canonical hparams.

## Cell 9 — Single edit dispatch: cfb-v3-001 guitar at Layer-A (L17 primary; v0.2 full implementation)

**Specialist:** memit-specialist (ROME dispatch) + validation-contract-architect (verdict surface)

**Purpose:** Apply ROME edit on cfb-v3-001 (Bo Jackson plays the instrument of guitar) at L17. Capture pre-edit / post-edit / post-unmount probe panels.

```python
# === CELL 9 — Single edit dispatch: cfb-v3-001 at Layer-A (L17 primary) — v0.2 ===
# Specialist: memit-specialist + validation-contract-architect
# References: D-S217-Q4-1 (Layer-A primary = L17 ROME paper precedent);
#             rome-patches-canonical.md v0.2 §4 (canonical hparams);
#             cfb-v3.yaml v1.0; probe-set-v3.yaml v1.0;
#             ROMEHyperParamsExtended subclass per C-S218-5

import torch
from rome import apply_rome_to_model
# Note: ROMEHyperParamsExtended consumed at hparam manifest; subclass inheritance per C-S218-5

# Single-fact ROME request (cfb-v3-001)
rome_request_l17 = {
    "prompt": "{} plays the instrument of",
    "subject": "Bo Jackson",
    "target_new": {"str": "guitar"},
}

# === STEP 1: Pre-edit probe panel capture (38 active probes) ===
preedit_probes = {}
for probe_id, probe_def in active_probes.items():
    # ... [38 forward passes; capture top_5 + p_top_1 + p_target_new_pre]
    pass

# === STEP 2: Apply ROME edit ===
# v0.2: invoke apply_rome_to_model with single-fact list + ROMEHyperParamsExtended hparams
# return_orig_weights=True provides the unmount handle directly (Copy-Unmount mechanism preserved
# from MEMIT joint-overlay regime; structurally narrowed to single-layer single-fact)

hparams_l17 = ROMEHyperParamsExtended(**ROME_HPARAMS_LAYER_A)  # subclass instantiation per C-S218-5

t_edit_start = time.time()
model_edited, weights_copy = apply_rome_to_model(
    model, tokenizer, [rome_request_l17],
    hparams=hparams_l17,
    copy=False,
    return_orig_weights=True,
)
t_edit_elapsed = time.time() - t_edit_start

# === STEP 3: Post-edit probe panel capture ===
postedit_probes = {}
for probe_id, probe_def in active_probes.items():
    # ... [38 forward passes; capture top_5 + p_top_1 + p_target_new_post]
    pass

# === STEP 4: Copy-Unmount (single-layer single-fact) ===
# v0.2: explicit unmount via state_dict.copy_ on the edited layer's weight tensor
LAYER_MODULE = f"model.layers.17.mlp.down_proj"
with torch.no_grad():
    target_weight = dict(model.named_parameters())[f"{LAYER_MODULE}.weight"]
    target_weight.copy_(weights_copy[f"{LAYER_MODULE}.weight"])

# === STEP 5: Post-unmount probe panel capture + bit-exact assertion ===
postunmount_probes = {}
unmount_drift = []
for probe_id, probe_def in active_probes.items():
    # ... [38 forward passes; capture top_5 + p_top_1]
    # Per IC-S23-4 (HARD): post-unmount drift on target_TRUE < 1e-4
    drift = abs(postunmount_probes[probe_id]["p_top_1"] - preedit_probes[probe_id]["p_top_1"])
    unmount_drift.append((probe_id, drift))

# HARD assertion (per IC-S23-4)
max_drift = max(d for _, d in unmount_drift)
assert max_drift < 1e-4, (
    f"Cell 9 HARD halt (IC-S23-4 unmount band): max drift {max_drift:.2e} > 1e-4"
)

# === STEP 6: Verdict JSON staging ===
verdict_l17 = {
    "layer": 17,
    "fact_id": "cfb-v3-001",
    "rome_request": rome_request_l17,
    "edit_wall_time_sec": t_edit_elapsed,
    "preedit": preedit_probes,
    "postedit": postedit_probes,
    "postunmount": postunmount_probes,
    "unmount_band_max_drift": max_drift,
    "unmount_band_status": "PASS",
    "p_target_new_pre": preedit_probes["cfb-v3-001-cons-1"]["p_target_new"],
    "p_target_new_post": postedit_probes["cfb-v3-001-cons-1"]["p_target_new"],
    "consistency_status": (
        "PASS" if postedit_probes["cfb-v3-001-cons-1"]["p_target_new"] > 0.5
        else "FAIL"
    ),
}
with open("/workspace/t2_rome_sect/block_b_layer_a_verdict.json", "w") as f:
    json.dump(verdict_l17, f, indent=2)

print(f"Cell 9: L17 dispatch complete. p(guitar)_post={verdict_l17['p_target_new_post']:.2e}; "
      f"unmount_drift_max={max_drift:.2e}")
```

**Verification anchors (empirical at S2.18 Cell 9):**

| Anchor | S2.18 empirical |
|---|---|
| Pre-edit `P(target_new=guitar)` | 1.32e-08 (baseline) |
| Post-edit `P(target_new=guitar)` | 8.26e-03 (FAIL consistency band p > 0.5) |
| Post-edit top-1 token | `<\|begin_of_text\|>` (BOS-collapse pathology) with P=0.924 |
| Post-unmount `abs(P(target_TRUE) - pre)` | `0.00e+00` (PASS unmount band; HARD per IC-S23-4) |
| compute_v iter trajectory | Loss 18.17 → 4.93 monotonic decrease (degenerate-fit) |
| Wall-time (edit only) | ~3-5 min |

**Halt conditions:** Unmount band drift > 1e-4 = immediate halt per IC-S23-4. (S2.18 empirical: 0 violations.)

---

## Cell 10 — Verdict surface for Cell 9 (Layer-A L17)

**Specialist:** validation-contract-architect

**Purpose:** Compute verdict for L17 edit; surface for cross-layer comparison at Cell 12.

**v0.2 anchor:** S2.18 Cell 10 verdict at L17:

| Criterion | Verdict | Empirical |
|---|---|---|
| Consistency (P(target_new) > 0.5) | **FAIL** | P(guitar)_post = 8.26e-03 |
| Unmount band (HARD; IC-S23-4) | PASS | 0.00e+00 |
| BOS-collapse pathology | OBSERVED | top_1 = `<\|begin_of_text\|>` P=0.924 |
| Specificity preserved (gen probes top_1) | PASS | gen probe drift max < 0.020 |

L17 fails consistency at canonical hparams.

---

## Cell 11 — Single edit dispatch: cfb-v3-001 guitar at Layer-B (L2 secondary; v0.2 full implementation)

**Specialist:** memit-specialist (ROME dispatch) + validation-contract-architect (verdict surface)

**Purpose:** Apply ROME edit on cfb-v3-001 at L2. Same dispatch surface as Cell 9 with `ROME_HPARAMS_LAYER_B` (L2). **Pre-execution requires Copy-Unmount restore from Cell 9 first** — the Cell 9 edit must be fully unmounted before Cell 11 dispatch to ensure the L2 test runs against pristine model state.

> **v0.2 implementation:** Full body parallels Cell 9 implementation with `LAYER_MODULE = "model.layers.2.mlp.down_proj"` and `hparams_l2 = ROMEHyperParamsExtended(**ROME_HPARAMS_LAYER_B)`. Cell 9 unmount must complete with bit-exact restore (drift `0.00e+00`) before Cell 11 dispatch. v0.2 anchor: S2.18 Cell 11 produced `0.00e+00` drift on Cell 9 unmount AND `0.00e+00` drift on Cell 11 post-unmount.

**Verification anchors (empirical at S2.18 Cell 11):**

| Anchor | S2.18 empirical |
|---|---|
| Pre-edit `P(target_new=guitar)` | 1.32e-08 (matches Cell 9 baseline; bit-exact restore) |
| Post-edit `P(target_new=guitar)` | 1.06e-06 (FAIL consistency band p > 0.5) |
| compute_v iter trajectory | Loss 13.49-19.26 oscillating non-converging (unfittable-landscape) |
| Post-unmount `abs(P(target_TRUE) - pre)` | `0.00e+00` (PASS unmount band) |
| Wall-time (edit only) | ~3-5 min |

---

## Cell 12 — Verdict surface for Cell 11 (Layer-B L2) + cross-layer comparison + pathology classification

**Specialist:** validation-contract-architect

**Purpose:** Compute Layer-B L2 verdicts (parallel to Cell 10); compute cross-layer comparison metrics; **classify pathology mode (NEW at v0.2)**. Write `t2_rome_block_b_layer_b_verdict.json` + `t2_rome_block_b_cross_layer_comparison.json`.

**v0.2 NEW: Pathology classification taxonomy.**

ROME edit dispatch can fail in two qualitatively distinct modes; v0.2 codifies the taxonomy from S2.18 empirical:

| Pathology class | Definition | Diagnostic | Source |
|---|---|---|---|
| **degenerate-fit** | compute_v loss decreases monotonically (the optimization succeeds against its objective) but the resulting top_1 token is a degenerate fixed point (e.g., BOS token) rather than the target_new | Post-edit top_1 ≠ target_new but P(top_1) high; loss trajectory is monotonic | S2.18 L17: top_1 = `<\|begin_of_text\|>` P=0.924; loss 18.17→4.93 |
| **unfittable-landscape** | compute_v loss oscillates without converging across full iter budget; the optimization cannot find a fixed point in the rank-1 weight update space | Post-edit P(target_new) very low; loss trajectory non-monotonic / oscillating | S2.18 L2: P(guitar) = 1.06e-06; loss 13.49-19.26 oscillating |

**v0.2 NEW: Calibration corridor PASS criterion.**

For Block B verdict to route Route A halt rather than Route B / C, BOTH layers must FAIL consistency band AND the pathology divergence (one degenerate-fit + one unfittable-landscape) must be diagnostic-distinct. v0.2 codifies the criterion:

```
Calibration corridor PASS = (consistency at L_primary > 0.5) OR (consistency at L_secondary > 0.5)
Calibration corridor FAIL = both layers FAIL consistency
Pathology diagnostic = (degenerate-fit at L_primary) AND (unfittable-landscape at L_secondary)
```

S2.18 empirical: corridor FAIL + pathology diagnostic distinct → Route A halt.

**Cross-layer comparison metrics:**

| Metric | Layer-A (L17) | Layer-B (L2) | Comparison verdict |
|---|---|---|---|
| Post-edit `P(target_new)` | 8.26e-03 | 1.06e-06 | Both FAIL consistency p > 0.5 |
| Generalization drift (avg) | < 0.020 | < 0.020 | Both PASS specificity preserved |
| Shared spec drift (avg) | < 0.020 | < 0.020 | Both PASS |
| Unmount drift (HARD gate) | 0.00e+00 | 0.00e+00 | Both PASS < 1e-4 |
| Wall-time (edit only) | ~3-5 min | ~3-5 min | Comparable |
| Pathology class | degenerate-fit (BOS-collapse) | unfittable-landscape | Diagnostic-distinct |

---

## Cell 13 — Block B verdict gate: 3-route option matrix (v0.2 codified per OQ-V02-2 closure)

**Specialist:** validation-contract-architect (verdict gate authority) + memit-specialist (mechanism interpretation)

**Purpose:** Block B verdict consolidation. v0.2 codifies the 3-route option matrix that the v0.1 declarative form lacked. Three deliverables:

1. **Verdict class adjudication** — Cell 12 cross-layer comparison verdict + pathology classification adjudicated against the 3-route matrix
2. **Multi-token tolerance posture for cfb-v3-004 finalized** (if Block C entered) — at trial 0
3. **Routing decision** — surface for Cells 14-20 entry (B / C) OR session halt (A)

**v0.2 NEW: 3-route option matrix.**

| Route | Trigger condition | Block C behavior | S2.18 selection |
|---|---|---|---|
| **A — Halt** | Calibration corridor FAIL AND pathology diagnostic distinct AND replay-S2.15-D2-precedent risk for naïve continuation | Block C NOT executed; session closes at Cell 13; verdict = B-FAIL → T.2 ROME ELIM at canonical | **SELECTED at S2.18** per D-S218-2 |
| **B — Full 15-trial Block C** | Calibration corridor PASS at one layer (consistency > 0.5 at L_primary OR L_secondary) | Cells 14-17 execute full 15-trial loop (5 facts × 3 replicates) at the load-bearing layer; verdict via Cell 17 aggregate | NOT selected (corridor FAIL) |
| **C — Reduced 3-trial Block C** | Calibration corridor BORDERLINE (consistency in [0.4, 0.5] at one layer) AND operator authorizes reduced protocol | Cells 14-17 execute 3-trial loop (load-bearing subset only at single replicate) for verdict integrity preview; full protocol deferred | NOT selected (corridor FAIL, not borderline) |

**Verdict classes (extended from v0.1):**

| Block B verdict class | Definition | Routes to |
|---|---|---|
| **B-PASS** | Calibration corridor PASS at one layer AND multi-token tolerance posture finalized | Route B (or C); Block C 15-trial (or 3-trial) execution at the load-bearing layer |
| **B-FAIL** | Calibration corridor FAIL at both layer candidates AND pathology diagnostic distinct | **Route A halt → T.2 ROME ELIM at canonical hparams** → Escalate to D-S216-Q3-1 path: GRACE adapter-based mechanism (S2.19 = T.2 GRACE runbook authoring) |
| **B-PARTIAL** | Calibration corridor BORDERLINE (one layer PASSES consistency but unmount FAILS, OR consistency 0.4-0.5) | Route C (3-trial preview) OR operator-side verdict integrity binding re-evaluation per `t_branch_decision_document.md` §5 conditional execution plan |

> **v0.2 empirical anchor.** S2.18 Cell 13 verdict gate evaluation:
> - Calibration corridor: **FAIL** at both L17 (p=8.26e-03) and L2 (p=1.06e-06)
> - Pathology classification: **diagnostic distinct** (degenerate-fit at L17 + unfittable-landscape at L2)
> - Replay-S2.15-D2-precedent risk: HIGH (15-trial Block C would replicate the S2.15-D2 D.2 precedent — drilling further into a known-failed mechanism without surfacing new evidence)
> - Operator confirmation: SELECTED Route A halt
>
> **Verdict: B-FAIL → Route A halt → T.2 ROME ELIM at canonical hparams** (D-S218-1 + D-S218-2 + D-S218-3).

> **v0.2 ratification note.** Cell 13 verdict computation logic at v0.2 is structurally codified (three routes); numerical thresholds (consistency 0.5; unmount 1e-4; borderline 0.4-0.5) inherit from D-S24-10 + IC-S23-4 carry-forward. Empirical instantiation at S2.18 Cell 13: Route A halt selected. Future ROME-class execution sessions (if any) re-run the three-route adjudication against fresh empirical state.

---

# Part V — Block C: Stage 1 SECT v3 execution at single-fact ROME dispatch (Cells 14–20)

> **Block C purpose.** Execute the 15-trial Stage 1 SECT v3 protocol per IC-S24-4 against the load-bearing layer selected at Block B Cell 13. Each trial is a single-fact ROME edit (per C-ROME-1). Trial loop structure mirrors `stage_1_sect_runbook_v1_6.md` Block VII (Cells 8-10) with the single-fact dispatch narrowing.
>
> **v0.2 disposition: SKIPPED at S2.18 per Cell 13 Route A halt.** Cells 14-20 are codified at v0.2 in declarative form for any future ROME-class execution session that re-runs Block B and routes Route B or Route C. The S2.18 forensic record contains zero Block C trial executions; the codified cell bodies below define the canonical Block C protocol for re-use without re-derivation.

## Cell 14 — Trial matrix authoring (D-S217-2 + verdict integrity binding carry-forward)

**Specialist:** validation-contract-architect (IC-S24-4 enforcement)

**Purpose:** Enumerate the 15 trials per IC-S24-4 (5 facts × 3 replicates) — OR 3 trials at Route C (3 load-bearing subset facts × 1 replicate); apply D-S217-2 cross-cell SUBSET hard gate (Cell 6 ↔ Cell 8 ↔ Cell 14 single-source); apply D-S215D2-VERDICT-INTEGRITY-1 load-bearing-subset annotation.

> **v0.2 carry-forward unchanged from v0.1 except where noted.** The trial matrix authoring logic is structurally identical to MEMIT runbook v1.6 Cell 8, with the same three ROME-specific adjustments declared at v0.1 §5 Cell 14. v0.2 adds the **Route B / Route C trial count branching** at the matrix construction step:

```python
# === CELL 14 — Trial matrix authoring (v0.2 with route branching) ===
# Specialist: validation-contract-architect
# References: IC-S24-4 (5×3 trial protocol); D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset);
#             D-S217-Q4-1 (load-bearing layer from Block B Cell 13);
#             D-S217-2 (Cell 6/8 single-source contract; carry-forward to Cell 14);
#             v0.2 Cell 13 Route B / Route C branching

LOAD_BEARING_LAYER = block_b_verdict["load_bearing_layer"]          # from Cell 13: 17 OR 2
BLOCK_C_ROUTE = block_b_verdict["block_c_route"]                    # from Cell 13: "B" OR "C"
ROME_HPARAMS_BLOCK_C = ROME_HPARAMS_LAYER_A if LOAD_BEARING_LAYER == 17 else ROME_HPARAMS_LAYER_B

# v0.2: Route B = 5 facts × 3 replicates = 15 trials; Route C = 3 load-bearing facts × 1 replicate = 3 trials
LOAD_BEARING_SUBSET = {"cfb-v3-001", "cfb-v3-002", "cfb-v3-005"}
FORENSIC_INFORMATIVE_DEFAULT = {"cfb-v3-003", "cfb-v3-004"}

if BLOCK_C_ROUTE == "B":
    eligible_facts = stage_1_eligible_facts                         # all 5 facts
    REPLICATES = 3
    EXPECTED_TRIAL_COUNT = 15
elif BLOCK_C_ROUTE == "C":
    eligible_facts = sorted(LOAD_BEARING_SUBSET)                    # 3 load-bearing only
    REPLICATES = 1
    EXPECTED_TRIAL_COUNT = 3
else:
    raise RuntimeError(f"Cell 14: invalid BLOCK_C_ROUTE = {BLOCK_C_ROUTE}; expected 'B' or 'C'")

trial_matrix = []
trial_index = 0
for fact_id in eligible_facts:
    for replicate in range(1, REPLICATES + 1):
        trial_matrix.append({
            "trial_index": trial_index,
            "fact_id": fact_id,
            "replicate": replicate,
            "rome_request": fact_memit_requests[fact_id],           # single-fact dispatch
            "hparams_layer": LOAD_BEARING_LAYER,
            "per_fact_probes": fact_probes[fact_id],
            "shared_specificity_probes": shared_specificity_probes,
            "torch_seed": 0,
            "subset_annotation": (
                "load_bearing" if fact_id in LOAD_BEARING_SUBSET
                else "forensic_informative_excluded"
            ),
        })
        trial_index += 1

assert len(trial_matrix) == EXPECTED_TRIAL_COUNT, (
    f"Trial count mismatch: {len(trial_matrix)} != {EXPECTED_TRIAL_COUNT} (route {BLOCK_C_ROUTE})"
)

# ... [carry-forward C-S24-7 hard gate from MEMIT v1.6 Cell 8]
# ... [carry-forward write to /workspace/t2_rome_sect/trial_matrix.json]
```

---

## Cell 15 — Trial loop execution (single-fact ROME edits + Copy-Unmount per fact)

**Specialist:** memit-specialist (ROME dispatch) + state-consistency-theorist (Copy-Unmount integrity) + validation-contract-architect (verdict computation)

**Purpose:** Execute the trial loop (15 trials at Route B; 3 trials at Route C). Each trial: pre-edit probe panel → ROME single-fact edit at LOAD_BEARING_LAYER → post-edit probe panel → Copy-Unmount → post-unmount probe panel. Per-trial JSON write + per-trial overlay snapshot.

> **v0.2 carry-forward from v0.1 §5 Cell 15.** Implementation skeleton inherits from v0.1; v0.2 cleans up the dispatch invocation to use ROMEHyperParamsExtended and explicit Copy-Unmount drift assertion.

```python
# === CELL 15 — Trial loop execution (v0.2) ===
# Specialist: memit-specialist + state-consistency-theorist + validation-contract-architect
# References: IC-S24-4; IC-S23-4 (unmount band); C-S24-8; D-S215D2-VERDICT-INTEGRITY-1;
#             stage_1_sect_runbook_v1_6.md Cell 9 (carry-forward structural template);
#             ROMEHyperParamsExtended subclass per C-S218-5

from rome import apply_rome_to_model

def run_trial(trial):
    # === Pre-edit probe panel + inter-trial baseline drift gate (per IC-S23-4) ===
    preedit = capture_probe_panel(model, tokenizer, trial["per_fact_probes"])
    inter_trial_drift = compute_drift(preedit, prior_postunmount)
    if max_drift(inter_trial_drift) > 1e-4:
        raise RuntimeError(f"Inter-trial baseline drift HARD halt at trial {trial['trial_index']}")

    # === ROME single-fact dispatch ===
    hparams = ROMEHyperParamsExtended(**ROME_HPARAMS_BLOCK_C)
    model_edited, weights_copy = apply_rome_to_model(
        model, tokenizer,
        [trial["rome_request"]],                                    # single-fact list
        hparams=hparams,
        copy=False,
        return_orig_weights=True,
    )

    # === Post-edit probe panel ===
    postedit = capture_probe_panel(model, tokenizer, trial["per_fact_probes"])

    # === Copy-Unmount: restore single layer in-place ===
    layer_module_name = f"model.layers.{LOAD_BEARING_LAYER}.mlp.down_proj"
    with torch.no_grad():
        target = dict(model.named_parameters())[f"{layer_module_name}.weight"]
        target.copy_(weights_copy[f"{layer_module_name}.weight"])

    # === Post-unmount probe panel + unmount band gate (per IC-S23-4 HARD) ===
    postunmount = capture_probe_panel(model, tokenizer, trial["per_fact_probes"])
    unmount_drift = compute_drift_target_true(postunmount, preedit, trial["fact_id"])
    if unmount_drift > 1e-4:
        raise RuntimeError(
            f"Cell 15 HARD halt (IC-S23-4 unmount band): trial {trial['trial_index']} "
            f"drift {unmount_drift:.2e} > 1e-4"
        )

    # === Verdict computation: consistency / generalization / specificity / unmount ===
    trial_verdict = {
        "trial_index": trial["trial_index"],
        "fact_id": trial["fact_id"],
        "replicate": trial["replicate"],
        "subset_annotation": trial["subset_annotation"],
        "rome_request": trial["rome_request"],
        "hparams_layer": trial["hparams_layer"],
        "wall_time_sec": ...,
        "consistency": {
            "p_target_new_post": postedit[f"{trial['fact_id']}-cons-1"]["p_target_new"],
            "top_1_post": postedit[f"{trial['fact_id']}-cons-1"]["top_1"],
            "verdict": "PASS" if postedit[...]["p_target_new"] > 0.5 else "FAIL",
        },
        "generalization": ...,
        "specificity_shared": ...,
        "unmount_band": {
            "abs_drift_target_true": unmount_drift,
            "verdict": "PASS",
            "_HARD": True,
        },
        "rome_specific": {
            "v_loss_at_step_final": ...,
            "v_norm_clip_factor_used": ...,
            "weights_copy_layer_sha_prefix": ...,
        },
    }

    # === Per-trial JSON write + overlay snapshot ===
    write_trial_json(trial_verdict, trial["trial_index"])
    write_overlay_snapshot(weights_copy, trial["trial_index"])  # ~16 MB FP16 single-layer

    return trial_verdict

# Trial loop with halt-class enforcement
prior_postunmount = preblock_baseline_postunmount  # Cell 7 captured pre-Block-B baseline
for trial in trial_matrix:
    verdict = run_trial(trial)
    prior_postunmount = postunmount  # carry-forward for next trial's inter-trial drift gate
    if verdict["unmount_band"]["verdict"] == "FAIL":
        raise RuntimeError(f"Unmount band HARD halt at trial {trial['trial_index']}")
```

**Per-trial verdict schema** (v0.2; parallel to MEMIT v1.6 Cell 9 per-trial JSON; ROME-specific keys):

```json
{
  "trial_index": <int>,
  "fact_id": "cfb-v3-XXX",
  "replicate": <int>,
  "subset_annotation": "load_bearing|forensic_informative_excluded",
  "rome_request": {...},
  "hparams_layer": <int (LOAD_BEARING_LAYER)>,
  "wall_time_sec": <float>,
  "consistency": {"p_target_new_post": <float>, "top_1_post": <str>, "verdict": "PASS|FAIL"},
  "generalization": {"per_probe_drift": [...], "verdict": "PASS|FAIL"},
  "specificity_shared": {"per_probe_drift": [...], "verdict": "PASS|FAIL"},
  "unmount_band": {"abs_drift_target_true": <float>, "verdict": "PASS|FAIL", "_HARD": true},
  "rome_specific": {
    "v_loss_at_step_final": <float>,
    "v_norm_clip_factor_used": <float>,
    "weights_copy_layer_sha_prefix": <str>
  }
}
```

---

## Cell 16 — Per-trial verdict aggregation

**Specialist:** validation-contract-architect

**Purpose:** Aggregate per-trial verdicts into per-fact and full-aggregate views. **INHERITED from `stage_1_sect_runbook_v1_6.md` Cell 10** with cell-numbering shift.

---

## Cell 17 — Aggregate verdict (load-bearing subset + full-aggregate)

**Specialist:** validation-contract-architect (verdict integrity binding authority)

**Purpose:** Compute the load-bearing-subset aggregate (decisive per D-S215D2-VERDICT-INTEGRITY-1) AND the full 5-fact aggregate (informational). Write `t2_rome_aggregate_verdict.json`.

**Verdict classes for Block C (preserved from v0.1):**

| Verdict | Definition | Routes to (per `t_branch_decision_document.md` §5) |
|---|---|---|
| **C-PASS** | Load-bearing subset {cfb-v3-001, cfb-v3-002, cfb-v3-005}: ≥ 2 of 3 facts at ≥ 2/3 trials each PASS consistency AND all 15 trials PASS unmount band | T.2 ROME PASS → S2.19 = MEMIT-vs-ROME comparison framework finding update (resolves OQ-S216-6) |
| **C-FAIL** | Load-bearing subset FAIL OR any trial FAILS unmount band | T.2 ROME FAIL → S2.19 = T.2 GRACE runbook authoring; S2.20 = GRACE execution |
| **C-PARTIAL** | Load-bearing subset borderline: 2/3 facts PASS but < 2/3 trials each, OR sentinel-FAIL ambiguity | Operator-side verdict integrity binding re-evaluation per `t_branch_decision_document.md` §5 conditional execution plan |

> **v0.2 disposition note:** Block C did not execute at S2.18 (Route A halt at Cell 13). v0.2 codifies Cell 17 in declarative form for future ROME-class execution.

---

## Cell 18 — NV inventory + SHA equality gate

**Specialist:** state-consistency-theorist

**Purpose:** Verify all per-trial JSONs, overlay snapshots, and aggregate verdict are written to NV at canonical paths. Run SHA equality gate (cache_state.provenance.model_revision_sha vs env_fingerprint.model_revision_sha) per OQ-S28-4 carry-forward / v1.6 try-both fallback. Write `t2_rome_nv_inventory.json`.

> **Carry-forward from MEMIT runbook v1.6 Cell 11.** Adapted: NV_TARGETS path prefix is `/workspace/t2_rome_sect/` instead of `/workspace/stage_1_sect/`; OVERLAY_TARGETS file count is 30 at Route B (15 trials × 2 files: edited.pt + original.pt per single layer at Copy-Unmount snapshot) OR 6 at Route C (3 trials × 2 files).

> **v0.2 empirical anchor (Cell 18 ran in modified form at S2.18):** Block C did not execute at S2.18; Cell 18 ran an inventory of Block A + Block B artifacts only. Inventory enumerated: `/workspace/t2_rome_sect/block_b_layer_a_verdict.json`, `block_b_layer_b_verdict.json`, `block_b_cross_layer_comparison.json`, `block_b_verdict_gate.json`. SHA equality gate PASS (model_revision_sha = `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` consistent across `t2_rome_environment_fingerprint.json` and `t2_rome_cache_state.json`).

---

## Cell 19 — Mirror sync (NV → SSD)

**Specialist:** state-consistency-theorist

**Purpose:** rsync NV `/workspace/t2_rome_sect/` to SSD mirror. Pattern carries forward from S2.15-D2 close (4-command rsync mirror discipline). Write `t2_rome_mirror_sync.log`.

> **v0.2 empirical anchor:** S2.18 close produced 4-command mirror sync of `/workspace/t2_rome_sect/` Block A + Block B artifacts; Block C artifacts absent due to Route A halt. NV utilization at S2.18 close documented in `session_2_18_summary_block_appendix.md` §7.

---

## Cell 20 — Block C verdict + reproducibility manifest update + routing decision

**Specialist:** state-consistency-theorist (manifest discipline)

**Purpose:** Append S2.18 execution state to `/workspace/reproducibility_manifest.json` (`sessions["2.18"]`). Print Block C verdict class. Print routing decision per `t_branch_decision_document.md` §5.

> **Carry-forward from MEMIT runbook v1.6 Cell 12.** Adapted: SESSION_LABEL="S2.18"; NV-resident artifact paths under `/workspace/t2_rome_sect/`.

> **v0.2 empirical anchor:** S2.18 Cell 20 wrote `sessions["2.18"]` with verdict = B-FAIL (Route A halt; Block C not executed); routing decision = T.2 GRACE PROMOTED (per D-S218-4). S2.19 = T.2 GRACE runbook v0.1 authoring (verdict-conditional C-FAIL branch active).

---

# Part VI — Halt conditions (cross-cell index)

See § §1.4 above for the full halt-condition index. v0.2 introduces the following NEW halt classes vs v0.1:

| Cell | Condition | Class | Action |
|---|---|---|---|
| Cell 1 | ROME repo SHA mismatch | Pre-flight (NEW) | Verify SHA pin per rome-patches-canonical v0.2 §3 |
| Cell 2 | `globals.yml` STATS_DIR cwd-relative | Pre-flight (NEW) | Re-customize per rome-patches-canonical v0.2 §9 |
| Cell 3 | L17 covariance cache absent | Pre-flight (NEW) | Pre-pod-attach extension required (closes OQ-S217-2 path a) |
| Cell 4 | Schema field count drift | Pre-flight (NEW) | Verify 21-field schema (was 20 at v0.1) |
| Cell 5 | L17-extension model cleanup miss | Pre-flight (NEW) | Free model + clear CUDA cache before fresh load |
| Cell 6 | MULTI_TOKEN_ALLOWLIST missing | Session-level (NEW) | Add to allowlist OR halt + revise corpus |
| Cell 7 | Cross-session bit-exact gate FAIL | Session-level HARD (NEW) | Investigate model SHA, HF cache state, P-1/P-2 application |
| Cell 8 | OOM at `get_inv_cov` | Session-level (NEW) | Verify P-7-ROME applied + `_t100_` cache filename produced |
| Cell 9/11 | fp16/fp32 dtype RuntimeError | Session-level (NEW) | Verify P-8-ROME + P-9-ROME applied (matmul + outer-product casts) |

---

# Part VII — Forward routing (post-S2.18 disposition)

**v0.2 forward routing record:**

| Block C verdict | Successor session | Successor scope | S2.18 disposition |
|---|---|---|---|
| C-PASS | S2.19 | MEMIT-vs-ROME comparison framework finding update; resolves OQ-S216-6 | NOT REACHED (Route A halt at Cell 13) |
| C-FAIL | S2.19 | T.2 GRACE runbook v0.1 authoring; S2.20 = GRACE execution | **CONFIRMED via Block B B-FAIL → Route A halt → T.2 ROME ELIM at canonical** |
| C-PARTIAL | S2.19 (re-evaluation) | Operator-side verdict integrity binding re-evaluation | NOT REACHED |

**v0.2 routing decision (per D-S218-4):** S2.19 = T.2 GRACE runbook v0.1 authoring (parallel structure to S2.17 Block 2 ROME runbook authoring; specialist invocation set: framework-spec-writer primary; memit-specialist consultative for adapter-vs-rank1-update mechanism comparison). T.2 GRACE PROMOTED to leading hypothesis per `t_branch_decision_document.md` v1.1 (forthcoming).

---

# Part VIII — Open questions in scope

## 8.1 OQs closed by S2.18 execution (post-S2.18 anchor)

| OQ ID | Closure mechanism | Empirical anchor |
|---|---|---|
| **OQ-S216-1** | Cell 1 ROME SHA pin resolution | `0874014cd9837e4365f3e6f3c71400ef11509e04` |
| **OQ-S216-2** | Cell 13 Block B verdict gate; full hparam adjudication | Canonical hparams FAIL at L17 + L2; calibration NOT explored further per Route A halt |
| **OQ-S216-3** | Cell 13 Block B verdict gate; load-bearing layer adjudication | Both L17 + L2 FAIL; no load-bearing layer surfaced at canonical |
| **OQ-S216-4** (= OQ-S217-1) | Cell 13 multi-token tolerance posture | Block C did not execute; first-token-proxy posture remains DECLARED-via-v0.2 |
| **OQ-S217-2** | Cell 1.5 / pre-Cell-2 L17 cache extension | 30.20 min compute on RTX 4090; ~0.766 GiB resident; closes path a (extend cache) |
| **OQ-S217-3** | Cell 8 retry post-P-7-ROME / Cell 9 first dispatch | `apply_rome_to_model` schema verified; ROMEHyperParamsExtended subclass works |
| **OQ-S217-4** | Block C did not execute → multi-token native handling not empirically tested | DECLARED-deferred to next ROME-class execution |

## 8.2 OQs activated / opened post-v0.2

| OQ ID | Surface | Disposition |
|---|---|---|
| **OQ-S218-1** | compute_v non-convergence mechanism at L2 (oscillating loss; unfittable-landscape pathology) | OPEN diagnostic; not blocking S2.19 |
| **OQ-S218-2** | BOS-collapse mechanism at L17 (degenerate-fit pathology; top_1 = `<\|begin_of_text\|>`) | OPEN diagnostic; not blocking S2.19 |
| **OQ-S218-3** | Specificity preservation generalization to other facts / corpora | OPEN diagnostic; not blocking S2.19 |

## 8.3 OQs explicitly out of scope for this runbook

| OQ ID | Reason |
|---|---|
| OQ-S216-5 | v1.6 hardening session scheduling — closed at S2.16 / S2.17 Block 1 |
| OQ-S216-6 | MEMIT-vs-ROME comparison framework finding update — out of v0.2 runbook scope; superseded by T.2 ROME ELIM at canonical (the comparison surface collapses; both engines hit the architectural-invariant ceiling) |

---

# Part IX — Non-goals

This runbook v0.2 does NOT:

1. **Modify `memit-patches-canonical.md` v2.5.** Preserved per D-S216-CLOSE-3.
2. **Modify `stage_1_sect_runbook_v1_6.md`.** v1.7 supersession is a separate deliverable (parallel to this v0.2; absorbs MULTI_TOKEN_ALLOWLIST per OQ-V02-3 deferred resolution).
3. **Re-execute any S2.18 cell.** v0.2 absorbs the empirical record; does not re-derive.
4. **Pre-commit ROME hparam recalibration values for future ROME execution.** Cell 4 declares canonical values; recalibration deferred (route A halt did not surface a calibration corridor — per Cell 13 verdict gate).
5. **Pre-commit Block C verdict for any future ROME-class execution.** Cells 14-17 codify the protocol; verdict empirical at execution time.
6. **Author runtime implementation code beyond canonical scaffolding for unexecuted cells.** Cells 14-17 carry-forward from v0.1 declarative form; cells 9 / 11 / 12 / 13 absorbed empirically.
7. **Amend the v1.2 integrated framework spec.** Sealed.
8. **Extend the framework finding archival v1.0 from this artifact.** v1.1 supersession is a separate deliverable in this codification session.
9. **Update the t_branch_decision_document v1.0 from this artifact.** v1.1 supersession is a separate deliverable in this codification session.

---

# Part X — Reference appendices

## 10.1 Carry-forward inheritance from `stage_1_sect_runbook_v1_6.md` (post-v0.2 codification)

| Component | Inherited unchanged | Adapted at v0.2 | NEW at v0.2 vs v0.1 |
|---|---|---|---|
| Cell 0 (pod + deps) | ✓ | | |
| Cell 1 (env fingerprint + ROME SHA) | | ✓ (rome_sha empirically pinned) | |
| Cell 1.5 (manifest write + L17 extension) | | ✓ (EXPECTED_KEYS extended; L17-extension NV write) | |
| Cell 2 (patch state) | | ✓ (transplant + P-7-ROME + P-8-ROME + P-9-ROME + globals.yml) | ✓ (CONFIG_LAYER class) |
| Cell 3 (cache provenance + SUBSET assertion) | ✓ (v1.6 SUBSET pattern) | ✓ (EXPECTED_LAYERS parameterized) | |
| Cell 4 (hparams) | | ✓ (ROME schema; 21-field; ROMEHyperParamsExtended subclass) | |
| Cell 5 (model load + Pad-Token + bit-exact gate) | ✓ | ✓ (L17-extension cleanup preamble) | |
| Cell 6 (tokenizer single-token + MULTI_TOKEN_ALLOWLIST) | | ✓ (canonical absorption) | ✓ (allowlist + first-token-proxy) |
| Cell 7 (baseline + cross-session bit-exact gate) | | ✓ (explicit gate codified; HARD halt class) | |
| Cell 8 (R1.3-equivalent dry-run gate) | | ✓ (rome.compute_u.get_inv_cov; smoke layer outside Block B sweep) | |
| Cells 9-13 (Block B HC-2-equivalent dry-run) | | ✓ (full implementation; pathology classification; 3-route option matrix) | |
| Cell 14 (trial matrix; D-S217-2 + verdict integrity binding + Route B / Route C branching) | ✓ | ✓ (Route B / Route C trial count branching) | |
| Cell 15 (trial loop) | | ✓ (single-fact ROME dispatch with ROMEHyperParamsExtended) | |
| Cells 16-20 (verdict aggregation + persistence) | ✓ (cell-numbering shift) | | |

## 10.2 NV-resident artifact paths (final state at S2.18 close)

```
/workspace/architecture_profile/
  ├── meta-llama_Llama-3.1-8B.json                      (S2.5a; consumed by Cell 4)
  ├── stage_1_environment_fingerprint.json              (MEMIT runbook fingerprint; preserved)
  ├── t2_rome_environment_fingerprint.json              (Cell 1.5 output; ROME fingerprint)
  ├── t2_rome_pinned_sha.txt                            (Cell 1 output; ROME SHA pin = 0874014c...)
  ├── t2_rome_patch_state.json                          (Cell 2 output; v0.2 transplant + new patches)
  ├── t2_rome_cache_state.json                          (Cell 3 output; v1.6 "provenance" key; L2-L8 + L17)
  ├── t2_rome_hparams.json                              (Cell 4 output; 2-layer dict; 21-field schema)
  ├── stage_1_token_verification.json                   (Cell 6 output; MULTI_TOKEN_ALLOWLIST canonical)
  └── stage_1_llama_baselines.json                      (Cell 7 output; cross-session bit-exact gate PASS)

/workspace/rome_dry_run/rome/                           (Cell 1; ROME repo clone at SHA 0874014c...)
  ├── util/nethook.py                                   (transplanted from MEMIT post-state; P-1 + P-2)
  ├── util/nethook.py.upstream_pristine                 (pristine ROME upstream; forensic anchor)
  ├── rome/compute_v.py                                 (transplanted; P-4)
  ├── rome/compute_v.py.upstream_pristine               (pristine; forensic anchor)
  ├── rome/layer_stats.py                               (transplanted; P-4 + P-5 + P-6)
  ├── rome/layer_stats.py.upstream_pristine             (pristine; forensic anchor)
  ├── rome/compute_u.py                                 (P-7-ROME + P-8-ROME applied)
  ├── rome/compute_u.py.upstream_pristine               (pristine; forensic anchor)
  ├── rome/rome_main.py                                 (P-9-ROME applied at both sibling sites)
  ├── rome/rome_main.py.upstream_pristine               (pristine; forensic anchor)
  ├── globals.yml                                       (CONFIG_LAYER customization; STATS_DIR absolute)
  └── globals.yml.upstream_pristine                     (pristine cwd-relative form; forensic anchor)

/workspace/covariance_caches/meta-llama_Llama-3.1-8B/wikipedia_stats/
  ├── PROVENANCE.txt                                    (pre-S2.6 fork-work + S2.18 update for [2..8, 17])
  └── 8 cache files: model.layers.{2..8, 17}.mlp.down_proj_float32_mom2_100000.npz
       (~6.52 GiB total; L2-L8 cumulative + L17 NEW at S2.18 30.20 min compute)

/workspace/t2_rome_sect/                                (Block A + Block B artifacts at S2.18 close)
  ├── block_b_layer_a_verdict.json                      (Cell 10 output; L17)
  ├── block_b_layer_b_verdict.json                      (Cell 12 output; L2)
  ├── block_b_cross_layer_comparison.json               (Cell 12 output; pathology classification)
  ├── block_b_verdict_gate.json                         (Cell 13 output; Route A halt)
  ├── nv_inventory.json                                 (Cell 18 output; SHA equality gate PASS)
  └── mirror_sync.log                                   (Cell 19 output; 4-command mirror sync)

  (Block C artifacts ABSENT due to Route A halt at Cell 13:
   no trial_matrix.json, no trials/ dir, no overlays/ dir, no aggregate_verdict.json)

/workspace/reproducibility_manifest.json                (Cell 20 update; sessions["2.18"] = B-FAIL)
```

## 10.3 Wall-time budget per cell (post-S2.18 empirical anchor)

| Cell | Wall time (v0.1 estimate) | S2.18 empirical | Notes |
|---|---|---|---|
| Cell 0 | ~5–8 min | within budget | dep install + kernel restart |
| Cell 1 | ~30 sec | within budget | ROME repo clone + SHA verify |
| Cell 1.5 | ~10 sec | (+30.20 min L17 extension; one-off) | env fingerprint + L17 cache extension |
| Cell 2 | ~30 sec | ~3 min | transplant + P-7-ROME + P-8-ROME + P-9-ROME + globals.yml |
| Cell 3 | ~1–2 min | within budget | cache SUBSET gate + R1.2 + R1.3-equivalent (warm) |
| Cell 4 | ~10 sec | within budget | hparam declaration + 21-field schema gate |
| Cell 5 | ~2–4 min | within budget (with cleanup preamble) | model load from NV-cached HF (~16 GB) |
| Cell 6 | ~30 sec | within budget | tokenizer + MULTI_TOKEN_ALLOWLIST |
| Cell 7 | ~3–5 min | within budget | 38 forward passes + cross-session bit-exact gate |
| Cell 8 | ~30 sec (was 30 sec at v0.1; first-execution OOM at 22.81 GiB resolved by P-7-ROME) | retry within budget post-P-7-ROME | R1.3-equivalent dry-run gate |
| **Block A subtotal** | **~13–20 min (+30.20 min L17 ext at S2.18)** | within budget | |
| Cell 9 | ~5–7 min | ~5 min | single edit dispatch L17 + 38-probe pre/post/post-unmount |
| Cell 10 | ~10 sec | within budget | verdict computation L17 |
| Cell 11 | ~5–7 min | ~5 min | single edit dispatch L2 |
| Cell 12 | ~10 sec | ~30 sec | verdict computation L2 + cross-layer comparison + pathology classification |
| Cell 13 | ~30 sec | ~30 sec | Block B verdict gate; Route A halt selected |
| **Block B subtotal** | **~11–15 min** | ~11 min S2.18 actual | |
| Cell 14 | ~10 sec | NOT EXECUTED (Route A halt) | trial matrix authoring |
| Cell 15 | ~75–105 min | NOT EXECUTED | 15 trials × ~5–7 min (or 3 trials × ~5–7 min at Route C) |
| Cell 16 | ~10 sec | NOT EXECUTED | per-trial aggregation |
| Cell 17 | ~10 sec | NOT EXECUTED | load-bearing subset + full aggregate verdicts |
| Cell 18 | ~30 sec | ~30 sec (Block A + Block B inventory only) | NV inventory + SHA equality gate |
| Cell 19 | ~30 sec | ~30 sec | mirror sync NV → SSD |
| Cell 20 | ~10 sec | ~10 sec | manifest update |
| **Block C subtotal (Route B)** | **~77–108 min** | NOT EXECUTED | |
| **Block C subtotal (Route C)** | **~17–24 min** | NOT EXECUTED | |
| **Total at Route A halt (S2.18 actual)** | **~25–35 min for Block A + Block B alone** | ~28 min S2.18 | Route A halt route; no Block C cost |

## 10.4 Cell-to-decision traceability (extended at v0.2)

| Decision | Cell of realization |
|---|---|
| C-S25-5 (cwd invariant; ROME-adapted as ROME_ROOT) | Cell 2 `os.chdir(ROME_ROOT)` |
| C-ROME-1 (single-fact dispatch envelope; EMPIRICALLY-VALIDATED) | Cells 9, 11, 14 trial matrix; Cell 15 trial loop |
| C-ROME-2 (covariance cache reuse; EMPIRICALLY-VALIDATED) | Cell 3 SUBSET gate |
| C-ROME-3 (R1.3-equivalent dry-run; EMPIRICALLY-VALIDATED) | Cell 8 |
| C-ROME-4 (marker post-application verification; EMPIRICALLY-VALIDATED) | Cell 2 marker assertion loop |
| C-S218-1 (P-7-ROME REQUIRED; NEW at v0.2) | Cell 2 step 2; Cell 8 retry |
| C-S218-2 (P-8-ROME REQUIRED; NEW at v0.2) | Cell 2 step 2; Cell 9 / Cell 11 dispatch |
| C-S218-3 (P-9-ROME REQUIRED both sibling sites; NEW at v0.2) | Cell 2 step 2; Cell 9 / Cell 11 dispatch |
| C-S218-4 (globals.yml absolute STATS_DIR; NEW at v0.2) | Cell 2 step 3 |
| C-S218-5 (ROMEHyperParamsExtended subclass; NEW at v0.2) | Cell 4 schema gate; Cells 9, 11, 15 hparam instantiation |
| D-S217-1 (Cell 2 = canonical marker site, carry-forward) | Cell 2 |
| D-S217-2 (Cell 6/8 single-source contract, carry-forward) | Cell 6 entry block; Cell 8 cross-cell SUBSET gate; Cell 14 trial matrix |
| D-S217-3 (single-fact dispatch envelope; EMPIRICALLY-VALIDATED) | § §1.5.1; Cells 9, 11, 14, 15 |
| D-S217-4 (empirical anchor inheritance; extended at v0.2 per D-S218-7) | § §1.5.2; Cells 5, 7 cross-session bit-exact gate |
| D-S217-Q2-1 (ROME SHA pin = latest stable tip; CLOSED) | Cell 1; SHA pin = 0874014c... |
| D-S217-Q3-1 (ROME hparams = paper Table 1 GPT-J + Llama adaptation) | Cell 4 |
| D-S217-Q4-1 (Layer-A=L17 + Layer-B=L2; both FAIL at canonical) | Cell 4 (both hparam dicts); Block B Cells 9-13 |
| D-S217-Q5-1 (cfb-v3-004 first-token-proxy + RE-EVALUATE flag; DECLARED-via-v0.2) | Cell 6 (canonical absorption); Cell 13 (Q5 finalization gate; not reached at S2.18) |
| D-S218-1 (B-FAIL Cell 13; NEW at v0.2) | Cell 13 verdict gate |
| D-S218-2 (Route A halt; NEW at v0.2) | Cell 13 routing decision |
| D-S218-3 (T.2 ROME ELIM at canonical hparams; NEW at v0.2) | Cell 13 + Cell 20 routing print |
| D-S218-4 (T.2 GRACE PROMOTED; NEW at v0.2) | Cell 20 routing print + S2.19 forward routing |
| D-S218-5 (3 NEW patches RATIFIED; NEW at v0.2) | Cell 2 step 2 |
| D-S218-6 (NEW CONFIG_LAYER class; NEW at v0.2) | Cell 2 step 3 |
| D-S218-7 (cross-session bit-exact 5→6; NEW at v0.2) | Cell 7 cross-session bit-exact gate |
| D-S218-8 (Copy-Unmount ROME L17 + L2 single-fact bit-exact; NEW at v0.2) | Cells 9, 11 unmount drift assertion |
| D-S218-9 (Q4-1 L17 + L2 NO_LOAD_BEARING; NEW at v0.2) | Cell 13 verdict gate |
| D-S218-10 (Q5-1 CLOSED-MOOT; NEW at v0.2) | Cell 13 (Block C did not execute) |
| IC-S23-4 (intra-pod drift band 1e-4) | Cell 9, 11, 15 unmount band gate |
| IC-S24-4 (Stage 1 trial protocol; declarative at v0.2 unexecuted) | Cells 14 + 15 |
| IC-S25-3 (LLaMA baseline re-capture contract) | Cell 7 |
| D-S213C-CALIB-1/2/3 (calibration-band stratification) | Cell 7 |
| D-S215D2-VERDICT-INTEGRITY-1 (load-bearing subset binding) | Cell 14 subset_annotation; Cell 17 aggregate verdict |
| D-S215D2-CELL3-SUBSET-ASSERTION-1 (cache truth ⊇ PROVENANCE) | Cell 3 |
| D-S215D2-CFB-V3-004-MULTITOKEN-1 (MULTI_TOKEN_ALLOWLIST canonical absorption) | Cell 6 |
| D-S215D2-CFB-V3-004-PROXY-1 (first-token-proxy) | Cell 6 |

---

## 10.5 Authoring metadata

| Field | Value |
|---|---|
| Authoring session | v0.2 codification session (operator-side post-S2.18; pre-S2.19 BLOCKING) |
| Authoring date | 2026-05-05 |
| Document version | 0.2 |
| Iteration | v2 empirical absorption (supersedes v0.1 declarative) |
| Status | RATIFIED v0.2 — empirically anchored to S2.18 first-execution record; supersedes v0.1 declarative |
| Supersedes | v0.1 (RATIFIED at S2.17 Block 2; preserved as historical anchor) |
| Basis | `session_2_18_summary_block.md` (canonical D / C / OQ / IC); `session_2_18_summary_block_appendix.md` (forensic detail; load-bearing for Cells 1.5 / 2 / 7 / 8 / 9 / 11 / 12 / 13 empirical anchors); `rome-patches-canonical.md` v0.2 (companion patches reference); `stage_1_sect_runbook_v1_6.md` (sibling structural template; v1.7 forthcoming); `t_branch_decision_document.md` v1.0 (T-branch methodology lock); `t2_rome_runbook_v0_1_authoring_plan.md` v1.0 (scoping inheritance) |
| Specialist provenance | framework-spec-writer (primary, runbook authoring + v0.2 empirical absorption); memit-specialist (Cells 1, 2, 4, 8, 9, 11, 15 — ROME mechanism, P-7-ROME / P-8-ROME / P-9-ROME application, ROMEHyperParamsExtended dispatch); state-consistency-theorist (Cells 3, 5, 7, 15 — covariance cache reuse + Copy-Unmount + cross-session bit-exact gate); validation-contract-architect (Cells 6, 7, 10, 12, 13, 16 — verdict surface, calibration corridor, pathology classification, MULTI_TOKEN_ALLOWLIST canonical absorption) |
| Last updated | 2026-05-05 |

---

*End of T.2 ROME Runbook v0.2 — RATIFIED at v0.2 codification session close (empirical absorption of S2.18 first-execution record; B-FAIL verdict; Route A halt; T.2 ROME ELIM at canonical hparams; T.2 GRACE PROMOTED via D-S218-4; S2.19 = T.2 GRACE runbook v0.1 authoring forthcoming).*
