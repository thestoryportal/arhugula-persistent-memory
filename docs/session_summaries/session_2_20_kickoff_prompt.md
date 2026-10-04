# Session 2.20 Kickoff Prompt — T.2 GRACE Stage 1 SECT v3 (Pod-Side Execution)

> **Session:** S2.20
> **Class:** Pod-side execution (Block-and-Cell runbook walk)
> **Predecessor:** S2.19 = T.2 GRACE runbook v0.1 authoring (CLOSED 2026-05-05)
> **2-back predecessor:** S2.18 = T.2 ROME first-execution (CLOSED 2026-05-05; B-FAIL → T.2 ROME ELIMINATED at canonical hparams)
> **Active branch:** Verdict-conditional C-FAIL branch per `t_branch_decision_document.md` v1.1 §5'; T.2 GRACE PROMOTED leading T-branch hypothesis per D-S218-4
> **Workstream:** WS1 (empirical execution)

---

## 1. Session scope and class

### 1.1 Scope statement

Execute `t2_grace_runbook.md` v0.1 cell-by-cell against `meta-llama/Llama-3.1-8B` on a RunPod RTX 4090 24 GiB pod backed by Network Volume storage. Walk Block A pre-flight (Cells 0–8), Block B HC-2-equivalent dry-run (Cells 9–13), Block C 15-trial loop (Cells 14–20; conditional on Cell 13 verdict gate routing).

Verdict surface at Cell 17 (Block C aggregate) + Cell 20 (forward routing decision) resolves T.2 GRACE empirical disposition per `t_branch_decision_document.md` v1.1 §5'.

### 1.2 Session class

| Attribute | Value |
|---|---|
| Class | Pod-side execution |
| Pattern | Block-and-Cell runbook walk |
| Pod-side code execution | YES (operator-driven; agent does not generate runtime implementations) |
| Agent role | Walk operator through runbook cells; surface and triage halts; author session summary block at session close; NO runtime implementation generation |
| Specification authoring scope | None at S2.20 entry; v0.2 codification analog session deferred post-S2.20 if NEW patches surface mid-execution |

### 1.3 Out-of-scope

| Item | Reason |
|---|---|
| Modification of `memit-patches-canonical.md` v2.5 | Preserved unmodified per D-S216-CLOSE-3 |
| Modification of `rome-patches-canonical.md` v0.2 | Preserved post-elimination per `t_branch_decision_document.md` v1.1 §4'.1 |
| Modification of `grace-patches-canonical.md` v0.1 | v0.1 declarative is RATIFIED at S2.19 close; absorption deferred to v0.2 codification analog session post-S2.20 |
| Modification of `t2_grace_runbook.md` v0.1 | Same disposition as v0.1 patches canonical |
| Pre-judgment of verdict | Verdict is empirical via Cell 13 + Cell 17 + Cell 20 |
| Re-execution of T.2 ROME | T.2 ROME ELIMINATED at canonical hparams per S2.18 |
| T.1 / T.3 path activation | Conditional on S2.20 verdict; not in scope at S2.20 |

---

## 2. Predecessor state at session entry

### 2.1 S2.19 deliverables (RATIFIED 2026-05-05)

| File | Lines | Path | Disposition |
|---|---|---|---|
| `grace-patches-canonical.md` v0.1 | 497 | `/mnt/user-data/outputs/grace-patches-canonical.md` | RATIFIED v0.1 declarative |
| `t2_grace_runbook.md` v0.1 | 1489 | `/mnt/user-data/outputs/t2_grace_runbook.md` | RATIFIED v0.1 declarative |
| `session_2_19_summary_block.md` | 223 | `/mnt/user-data/outputs/session_2_19_summary_block.md` | RATIFIED at S2.19 close |

### 2.2 Decisions ratified at S2.19 (carried forward)

| ID | Statement | Cell anchor |
|---|---|---|
| D-S219-Q1-1 | GRACE SHA pin = latest stable tip of `https://github.com/Thartvigsen/GRACE` | Cell 1 |
| D-S219-Q2-1 | Canonical hparams = GRACE paper Table 1 + Llama-3.1-8B adaptation; `GraceHyperParamsExtended` subclass | Cell 4 |
| D-S219-Q3-1 | Adapter placement: Layer-A L17 primary + Layer-B L2 secondary | Cell 4, 9, 11 |
| D-S219-Q4-1 | Unmount = adapter-detach (option (a)); adapter-snapshot-restore (option (c)) fallback if drift > 1e-4 | Cell 9, 11, 15 |
| D-S219-Q5-1 | Multi-token cfb-v3-004: first-token-proxy carry-forward + RE-EVALUATE AT TRIAL 0 flag | Cell 6, 15 |
| D-S219-CELL3-1 | Cell 3 = INAPPLICABLE-DEFERRED-BY-MECHANISM; adapter-pool init verification folded into Cell 8 | Cell 3, 8 |
| D-S219-SIBLING-PARITY-1/-2 | 3 coexisting canonicals + 3 coexisting runbooks | (cross-session discipline) |

### 2.3 Constraints declared at S2.19 (DECLARATIVE; EMPIRICALLY-VALIDATED PENDING at S2.20)

| ID | Statement | Verification cell |
|---|---|---|
| C-GRACE-1 | Single-fact dispatch envelope (no cross-trial codebook state) | Cell 9, 15 |
| C-GRACE-2 | Adapter pool initialization at trial entry (codebook empty, adapter list empty) | Cell 8, 15 |
| C-GRACE-3 | R1.3-equivalent dry-run gate (smoke-load + empty-codebook adapter pool init) | Cell 8 |
| C-GRACE-4 | Marker post-application verification (Pad-Token + any v0.2-absorbed NEW patches) | Cell 2, 5 |
| C-GRACE-5 | Adapter-detach unmount mechanism; bit-exact post-detach forward-pass | Cell 9, 11, 15 |

### 2.4 Carry-forward empirical anchors (LOCKED)

| Anchor | Source | S2.20 expectation |
|---|---|---|
| `meta-llama/Llama-3.1-8B` revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b` | S2.13-C onward | Held; verified at Cell 5 |
| Cross-session bit-exact determinism (6 checkpoints; D-S217-4 + D-S218-7) | S2.18 close | Extended to checkpoint #7 at Cell 5 cross-session bit-exact gate |
| `cfb-v3.yaml` v1.0 (5 facts) + `probe-set-v3.yaml` v1.0 (38 active probes) | S2.13-C | Held verbatim; Cell 6, 7, 14 references |
| IC-S24-4 trial protocol (5 × 3 = 15 trials) | S2.4 series | Held; GRACE multi-fact dispatch semantics may differ — OQ-S219-3 closure at Cell 15 empirical record |
| Acceptance bands (`0.5` cons / `0.05` gen / `0.05` spec / `1e-4` unmount) | D-S24-10 + IC-S23-4 | Held |
| D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset `{cfb-v3-001, cfb-v3-002, cfb-v3-005}` | S2.15-D2 | Held; Cell 17 aggregate gating |
| Pad-Token applicability (engine-agnostic tokenizer-side) | MEMIT v2.5 + ROME v0.2 EMPIRICAL | Cell 5 |
| Copy-Unmount mechanism | MEMIT + ROME EMPIRICAL | INAPPLICABLE under GRACE — replaced by C-GRACE-5 adapter-detach per Q4-1 |
| Covariance caches L2-L8 + L17 (~6.5 GiB on NV) | S2.18 + ceiling Axis 7 anchor | INAPPLICABLE; preserved on NV; Cell 18 SHA equality gate verifies bit-exact preservation |

### 2.5 Open questions activated at S2.20

| OQ | Closure cell |
|---|---|
| OQ-S219-1 — P-1 / P-2 retain-trace applicability under GRACE adapter forward pass | Cell 2 (grep-anchor inspection of `grace/*.py` for `nethook.get_module`) |
| OQ-S219-2 — GRACE CONFIG_LAYER analog (`globals.yml`-equivalent) | Cell 8 (R1.3 dry-run gate initial diagnostic) |
| OQ-S219-3 — GRACE multi-fact dispatch semantics (single-fact-per-trial enforced vs. adapter-accumulation natural) | Cell 15 trial loop empirical record (deferred to v0.2 absorption) |

---

## 3. Mandatory pre-reads (load-bearing for execution)

The agent loads these at session entry. KB hygiene per S2.19 → S2.20 transition reduces the active KB to 8 files:

| # | File | Cells consuming | Load priority |
|---|---|---|---|
| 1 | `t2_grace_runbook.md` v0.1 | All 21 cells | LOAD-BEARING (the runbook itself) |
| 2 | `grace-patches-canonical.md` v0.1 | Cell 1, 2, 4, 5, 8, 9, 11, 15 | LOAD-BEARING (constraint registry + manifest schema) |
| 3 | `session_2_19_summary_block.md` | Cell 0 entry; Cell 20 forward routing | LOAD-BEARING (predecessor close) |
| 4 | `cfb-v3.yaml` | Cell 6, 9, 14 | LOAD-BEARING (corpus) |
| 5 | `probe-set-v3.yaml` | Cell 7, 9, 11, 15 | LOAD-BEARING (probes) |
| 6 | `memit-patches-canonical.md` v2.5 | Cell 2 (P-1 / P-2 transplant source IF OQ-S219-1 = APPLICABLE) | CONDITIONAL (load on Cell 2 demand) |
| 7 | `stage_1_sect_runbook_v1_7.md` | Cell 6 (MULTI_TOKEN_ALLOWLIST inheritance reference) | REFERENCE-ONLY |
| 8 | `t_branch_decision_document_v1_1.md` | Cell 13 routing rationale; Cell 20 forward routing | REFERENCE-ONLY |

### 3.1 Removed at S2.20 entry (preserved on disk)

| File | Reason for removal |
|---|---|
| `session_2_18_summary_block.md` + appendix | S2.18 ROME forensic; carry-forward anchors captured in t2_grace_runbook §1.5.2 + grace-patches-canonical §0 |
| `session_2_17_summary_block.md` | 3-back; superseded |
| `session_v0_2_codification_summary_block.md` | Superseded by S2.19 close |
| `framework_finding_memit_ceiling_archival.md` v1.0 + v1.1 | S2.21+ context, not S2.20-execution-load-bearing |
| `t_branch_decision_document.md` v1.0 | v1.1 supersedes for routing logic |
| `rome-patches-canonical.md` v0.2 | Template-only; inheritance captured in grace-patches-canonical §1.0 + §12 |
| `t2_rome_runbook.md` v0.2 | Template-only; cell-numbering inheritance captured in t2_grace_runbook §10.1 |

---

## 4. Specialist invocation set

| Specialist | Role at S2.20 | Primary cells |
|---|---|---|
| **memit-specialist** | GRACE dispatch authority; hparam surface; mechanism-orthogonality interpretation at Cell 2 patch state + Cell 8 dry-run + Cell 9/11/15 dispatch | 1, 2, 4, 8, 9, 11, 15 |
| **state-consistency-theorist** | Cross-session bit-exact gate; adapter-detach unmount mechanism; covariance cache inapplicability assertion at Cell 3; NV inventory + SHA equality gate at Cell 18 | 3, 5, 7, 15, 18 |
| **validation-contract-architect** | MULTI_TOKEN_ALLOWLIST canonical absorption at Cell 6; verdict_class P-capture wiring at Cell 7; calibration corridor evaluation at Cell 10/12; pathology classification at Cell 12; verdict gate at Cell 13; per-trial verdict adjudication at Cell 16; aggregate verdict at Cell 17 | 6, 7, 10, 12, 13, 14, 16, 17 |
| **framework-spec-writer** | Session summary block at session close; reproducibility manifest update at Cell 20 | (close artifact) + 20 |

### 4.1 Inactive specialists at S2.20

| Specialist | Reason |
|---|---|
| orchestration-comparativist | Write-engine architecture comparison surface is forward-conditional (S2.21 if PASS); not S2.20-execution-load-bearing |
| graph-data-architect | Framework-spec-relevance scoring is forward-conditional; not S2.20-execution-load-bearing |
| aiSecOps-specialist | WS2/WS3 reactivation; inactive at all WS1 sessions |
| framework-council | Multi-specialist facilitated mode is for spec-class sessions; not execution class |

---

## 5. Pod resources + NV state expected at session entry

### 5.1 Pod resources

| Resource | Expectation |
|---|---|
| GPU | RTX 4090 24 GiB (single-card) |
| CUDA | torch ≥ 2.1.0 + transformers ≥ 4.40.0 |
| NV mount | `/workspace/` read+write |
| SSD | `/root/` for mirror sync (Cell 19) |

### 5.2 NV state (verified at Cell 0 entry)

```
/workspace/
├── hf_cache/                                # Llama-3.1-8B fp16 weights cached
│   └── d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/
├── memit_dry_run/memit/                     # MEMIT v2.5 patches state (preserved)
├── rome_dry_run/rome/                       # ROME v0.2 patches state (preserved post-elim)
├── covariance_caches/                       # ~6.5 GiB; INAPPLICABLE for GRACE; SHA-gated at Cell 18
│   └── d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/
│       └── wikipedia_stats/                 # 7 .npz L2-L8 + 1 .npz L17
├── architecture_profile/                    # cumulative; consulted at Cell 4
│   └── d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/profile.json
├── stage_1_sect_d3/                         # S2.14-D outputs (preserved)
├── stage_1_sect/                            # S2.15-D2 outputs (preserved)
├── causal_trace/                            # S2.14-D D.1 mediation map (preserved)
├── cross_session_determinism/               # 6-checkpoint baseline (extended to #7 at Cell 5)
│   └── d04e592bb4f6aa9cfee91e2e20afa771667e1d4b/baseline_logits.pt
├── grace_dry_run/                           # ABSENT at entry; created at Cell 1
└── stage_1_sect_grace/                      # ABSENT at entry; created at Cell 14
```

### 5.3 NV utilization budget

| Metric | S2.18 close | S2.20 budget |
|---|---|---|
| Total NV utilization | ~74% (925.98 / 1259.75 GiB) | Headroom ~333.77 GiB |
| Expected S2.20 delta | Block A: ~10-50 MiB (GRACE clone + manifest); Block B: ~5-10 MiB (block_b_verdict); Block C: ~50-200 MiB (15 per-trial verdicts + adapter-detach traces) | Net delta: ~250 MiB (well within headroom) |

---

## 6. Acceptance criteria

### 6.1 Block A acceptance (Cells 0–8)

| Criterion | Verification |
|---|---|
| GRACE repo cloned at latest stable tip | Cell 1: `GRACE_SHA` recorded to env_fingerprint |
| Environment fingerprint captured | Cell 1.5: `env_fingerprint.json` written |
| Patch state manifest written with OQ-S219-1 closure | Cell 2: `t2_grace_patch_state.json` includes `uses_nethook` field; P-1 / P-2 disposition recorded |
| Cell 3 INAPPLICABLE assertion completes (no NV writes) | Cell 3: structural placeholder execution |
| `GraceHyperParamsExtended` instantiated for Layer-A + Layer-B | Cell 4: `GRACE_HPARAMS_LAYER_A` + `GRACE_HPARAMS_LAYER_B` instantiated; layer-set verified against architecture profile |
| Llama-3.1-8B loaded + Pad-Token applied + cross-session bit-exact gate PASS (checkpoint #7) | Cell 5: `drift == 0.00e+00` against carried baseline |
| MULTI_TOKEN_ALLOWLIST + verdict_class assignment per fact | Cell 6: 4 STRICT_SINGLE_TOKEN + 1 ALLOWLIST_FIRST_TOKEN_PROXY (cfb-v3-004); 0 MULTI_TOKEN_FAIL halts |
| Pre-edit baseline captured | Cell 7: `pre_edit_baseline.json` written |
| R1.3-equivalent dry-run gate PASS + adapter-pool initialization verification PASS | Cell 8: empty-codebook adapter pool produces drift `0.00e+00`; no import-time errors |

### 6.2 Block B acceptance (Cells 9–13)

| Criterion | Verification |
|---|---|
| Single edit dispatch at Layer-A L17 (cfb-v3-001 guitar) | Cell 9: `adapter_pool.codebook_size == 1` post-dispatch |
| Adapter-detach post-Layer-A unmount drift `< 1e-4` | Cell 9: `drift_unmount < 1e-4` (expected `0.00e+00`) |
| Layer-A L17 verdict adjudication | Cell 10: `verdict_layer_a` recorded with cons / spec / pathology |
| Single edit dispatch at Layer-B L2 (cfb-v3-001 guitar) | Cell 11: parallel to Cell 9 with `GRACE_HPARAMS_LAYER_B` |
| Layer-B L2 verdict adjudication + cross-layer comparison | Cell 12: `verdict_layer_b` + `cross_layer_comparison` recorded |
| Cell 13 verdict gate adjudication (3-route option matrix) | Cell 13: `verdict_class` ∈ {B-PASS, B-FAIL, B-PARTIAL}; `block_c_route` ∈ {A, B, C} |

### 6.3 Block C acceptance (Cells 14–20; conditional on Block B Route)

| Route | Block C disposition |
|---|---|
| **Route A** | Block C SKIPPED; session halts at Cell 13; verdict = B-FAIL → T.2 GRACE ELIM at canonical hparams → escalate per `t_branch v1.1 §5'` (FALL BACK TO T.1) |
| **Route B** | Cells 14–17 execute full 15-trial loop (5 facts × 3 replicates); Cell 14 trial matrix; Cell 15 trial loop body; Cell 16 per-trial verdict; Cell 17 aggregate verdict gating per D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset |
| **Route C** | Cells 14–17 execute reduced 3-trial preview (load-bearing subset only at single replicate); aggregate verdict for verdict integrity preview |

| Criterion (Routes B + C) | Verification |
|---|---|
| Cells 18 NV inventory + SHA equality gate | Covariance caches bit-exact preserved |
| Cell 19 mirror sync | `/root/stage_1_sect_grace_mirror/` populated |
| Cell 20 reproducibility manifest update | `reproducibility_manifest.json` `sessions["2.20"]` populated |
| Forward routing decision printed | Cell 20: PASS / FAIL / PARTIAL message printed; routes S2.21 disposition |

### 6.4 Session-level acceptance (mandatory)

| Criterion | Status |
|---|---|
| Session summary block authored at close | `session_2_20_summary_block.md` ≤ ~300L; Decisions / Constraints / OQs / Forward routing |
| All Block A / Block B halts triaged with explicit disposition | Halt-class log per Cell |
| If NEW SOURCE_LAYER or CONFIG_LAYER patches surface mid-execution: documented in session summary as v0.2 absorption candidates | Carry-forward to v0.2 codification analog session |

---

## 7. Halt conditions (cross-cell index)

| Halt class | Trigger | Cell | Disposition |
|---|---|---|---|
| **Cross-session bit-exact drift** | Cell 5 forward-pass drift > 0 against carried baseline | 5 | HALT — investigate before any subsequent cell entry |
| **Patch state miss** | Cell 2 marker assertion FAIL on any APPLICABLE patch | 2 | HALT — patch application failed; investigate before Cell 3 entry |
| **R1.3 dry-run gate FAIL** | Cell 8 GRACE module smoke-load throws import-time or instantiation-time error | 8 | HALT — patches not in place OR GRACE codebase incompatibility; surface NEW patch candidate; investigate before Cell 9 |
| **Empty-codebook drift** | Cell 8 empty-codebook adapter pool produces forward-pass drift > 0 | 8 | HALT — adapter pool instruments forward pass even with empty codebook (mechanism violation); surface NEW patch candidate |
| **Adapter-detach drift** | Cell 9 / Cell 11 / Cell 15 post-detach drift > 1e-4 | 9, 11, 15 | Per-trial halt; fallback to adapter-snapshot-restore (D-S219-Q4-1 option (c)); v0.2 absorption codifies new unmount semantics |
| **Calibration corridor FAIL at both layers** | Cell 13 verdict gate adjudicates B-FAIL | 13 | Route A halt → T.2 GRACE ELIM at canonical hparams → escalate per `t_branch v1.1 §5'` |
| **MULTI_TOKEN_FAIL** | Cell 6 fact tokenizes to multiple tokens AND not in MULTI_TOKEN_ALLOWLIST | 6 | HARD halt per D-V12-MULTITOKEN-1 (inherited from v1.7) |
| **VRAM OOM** | Any cell exceeds 24 GiB VRAM ceiling | any | HALT; per `C-S214D-2`: per-trial `gc.collect() + empty_cache()` OR kernel restart |

---

## 8. Anticipated open questions

### 8.1 OQs scheduled to close at S2.20

| OQ | Closure path |
|---|---|
| OQ-S219-1 | Cell 2 grep-anchor inspection of `grace/*.py` for `nethook.get_module` usage; binary outcome (APPLICABLE / INAPPLICABLE) |
| OQ-S219-2 | Cell 8 R1.3 dry-run gate initial diagnostic; whether GRACE has `globals.yml`-equivalent or other CONFIG_LAYER instance |
| OQ-S219-3 | Cell 15 trial loop empirical record; single-fact-per-trial enforced via codebook reset vs. adapter-accumulation natural to GRACE codebase |

### 8.2 OQ candidates anticipated to surface at S2.20

These are not formal OQs at S2.20 entry; surfacing depends on Block A / Block B empirical record.

| Candidate surface | Likely cell | v0.2 absorption disposition |
|---|---|---|
| Adapter parameter dtype mismatch (fp32 adapter vs. fp16 base model) | Cell 4 / Cell 8 | NEW SOURCE_LAYER patch (analog of P-8-ROME class) |
| Llama architecture-specific instrumentation (RoPE / RMSNorm / GQA) at adapter insertion | Cell 8 / Cell 9 | NEW SOURCE_LAYER patch (analog of P-7 architecture-instrumentation class) |
| Codebook persistence across model reload | Cell 15 | OQ candidate; resolves at v0.2 absorption |
| Gradient flow through frozen base model | Cell 9 / Cell 11 | NEW SOURCE_LAYER patch candidate |

### 8.3 OQ scheduled to remain OPEN post-S2.20

| OQ | Closure window |
|---|---|
| OQ-V11-T-BRANCH-6 (carried) | S2.21 if PASS verdict; resolves comparison framework finding artifact format |

---

## 9. Operator-side commitments

### 9.1 Pod attach + NV state verification

The operator attaches the RunPod pod with NV mount before session entry; verifies `/workspace/` read+write access; verifies expected NV state per Section 5.2.

### 9.2 Mid-execution disposition for NEW patches

If S2.20 surfaces NEW SOURCE_LAYER or CONFIG_LAYER patches mid-execution (parallel to S2.18 P-7-ROME / P-8-ROME / P-9-ROME mid-session surfacing pattern):

| Operator option | Disposition |
|---|---|
| **(a) Author NEW patch in-session** | Patch authored agentically + applied; Cell 2 patch state manifest extended; constraint registry extended at session close summary; v0.2 codification analog session scheduled post-S2.20 to absorb formally |
| **(b) Halt session + author at v0.2 codification analog** | Session halts at the surfacing cell; v0.2 codification analog scheduled before any S2.20 retry |

S2.18 disposition was (a); S2.20 default disposition matches.

### 9.3 Cell 13 Route C authorization

If Cell 13 verdict gate adjudicates BORDERLINE (consistency in `[0.4, 0.5]` at one layer), Route C 3-trial preview requires explicit operator authorization (per `t2_grace_runbook v0.1` Cell 13 disposition matrix). Default disposition: operator authorizes Route C if Cell 12 cross-layer comparison shows one-layer-PASS-borderline + spec / unmount bands PASS at that layer; operator declines Route C and routes Route A halt if verdict integrity uncertainty is HIGH.

### 9.4 cfb-v3-004 RE-EVALUATE flag closure

Cell 15 trial 0 of cfb-v3-004 trial subset surfaces the `P_full > 0.5` / `P_full ≤ 0.5` empirical record. Operator confirms RETIRED / RATIFIED disposition before subsequent cfb-v3-004 trials proceed.

---

## 10. Forward routing post-S2.20

### 10.1 Verdict-conditional successor matrix

```
              S2.20 verdict surface (Cell 17 + Cell 20)
                              │
              ┌───────────────┼───────────────┐
              │               │               │
            PASS            FAIL           PARTIAL
              │               │               │
              ▼               ▼               ▼
   ┌──────────────────┐ ┌──────────────┐ ┌─────────────────┐
   │ Ceiling = rank-1 │ │ Ceiling      │ │ Operator-side   │
   │ -in-weight-class │ │ generalizes  │ │ verdict integ-  │
   │ -mechanism-      │ │ to (model ×  │ │ rity binding    │
   │ specific         │ │ hparams)     │ │ re-evaluation   │
   └─────────┬────────┘ └──────┬───────┘ └────────┬────────┘
             │                 │                  │
             ▼                 ▼                  ▼
   S2.21 = MEMIT-vs-ROME-  S2.21 = T.1 alt-  TBD per operator
   vs-GRACE comparison    model runbook v0.1  disposition
   framework finding      authoring (parallel
   update (resolves       to S2.19; reuses
   OQ-V11-T-BRANCH-6)     MEMIT + cfb-v3 +
                          canonical hparams)
```

### 10.2 v0.2 codification analog session (conditional)

If S2.20 surfaces NEW SOURCE_LAYER or CONFIG_LAYER patches OR adapter-detach unmount fallback (D-S219-Q4-1 option (c)) is exercised:

| Deliverable | Scope |
|---|---|
| `grace-patches-canonical.md` v0.2 | NEW patches absorbed at §6 / §7 / §8 / §9; v0_1_undocumented_findings populated at §2; OQ-S219-1/2/3 closed |
| `t2_grace_runbook.md` v0.2 | Cell bodies revised against empirical record; declarative API placeholders replaced with verified API calls; mid-session NEW patch application cells inserted as needed |
| Possibly `framework_finding_memit_ceiling_archival.md` v1.2 | Axis 8 added if PASS or FAIL produces architectural-invariant ceiling extension to {MEMIT, ROME, GRACE} class |
| Possibly `t_branch_decision_document.md` v1.2 | T.2 GRACE empirical disposition recorded; T.2 MEND / SERAC routing if PASS |

This is forward-conditional and out of scope at S2.20 entry.

### 10.3 Workstream 2 / 3 routing (conditional)

If S2.20 GRACE PASSES, the empirical result is informative for:

| Workstream | Routing implication |
|---|---|
| WS2 (orchestration; GAP-4) | Adapter-based write engines have framework-spec affinity per `grace-patches-canonical v0.1 §12.5` (closer to `.vindex` overlay model than rank-1-update mechanisms); informs orchestrator capability requirements |
| WS3 (implementation planning) | GRACE adapter-pool persistence + State Ledger semantics under adapter mechanism inform `.vindex` overlay implementation choices |

This routing is forward-conditional and informational at S2.20 entry.

---

## 11. Session entry checklist (operator)

| # | Item | Status |
|---|---|---|
| 1 | Pod attached; NV mounted at `/workspace/`; read+write verified | [ ] |
| 2 | KB curated to S2.20 active set (8 files per Section 3) | [ ] |
| 3 | `t2_grace_runbook.md` v0.1 + `grace-patches-canonical.md` v0.1 + `session_2_19_summary_block.md` present in KB | [ ] |
| 4 | NV state per Section 5.2 verified (covariance caches preserved; MEMIT + ROME repos preserved; Llama weights cached) | [ ] |
| 5 | Operator-side disposition for Cell 13 Route C authorization criterion confirmed (per Section 9.3) | [ ] |
| 6 | Operator-side disposition for mid-execution NEW patch surfacing confirmed (per Section 9.2; default option (a)) | [ ] |

---

*End of S2.20 kickoff prompt. S2.20 = T.2 GRACE Stage 1 SECT v3 pod-side execution. Verdict-conditional C-FAIL branch active per `t_branch_decision_document.md` v1.1 §5'. T.2 GRACE PROMOTED leading T-branch hypothesis. Verdict surface at Cell 17 + Cell 20 routes S2.21 disposition (PASS → comparison framework finding update; FAIL → T.1 alt-model runbook authoring; PARTIAL → operator-side re-evaluation).*
