# 00 — MASTER EVIDENCE LEDGER (single source of truth)
_All numbers verified against the result JSONs in `/workspace/` on 2026-06-18. Status ∈ {PROVEN, PARTIAL, NEGATIVE/clarifying, UNTESTED}. "Engine" = kmeng01/memit, UNMODIFIED throughout; all workarounds are config/harness-level or our-own-code; LARQL UNMODIFIED (used via its CLI/LQL only)._

## Metric (the measurement instrument)
Same-entity %-locality = mean(1 − JS/ln2) over same-entity OTHER-attribute next-token distributions (behavioral-deviation; ground-truth-free). Expression gate: post-edit top-1 prob > 0.5. Cross-entity JS = the lineage's Neighborhood-Success control.

## PHASE 0 — metric calibration (`s242_*`)
| ID | model | result (null-edit floor) | status |
|---|---|---|---|
| P0-GPTJ | GPT-J-6B | clean floor: France null edit same-entity **99.06%**, cross **97.88%** (re-asserts near-certain token ≈ no-op) | PROVEN: metric calibrated |
| P0-QWEN7 | Qwen2.5-7B | clean floor: same-entity **99.4%**, cross **96.24%** | PROVEN: metric calibrated |
_(v1 calibration HALTed on degenerate stimulus; v2 centrality-matched stimulus gave clean floors → metric trustworthy. Decision D-S242-CAL-1.)_

## PHASE 1 — baseline + model/size dependence (`s243_phase1_*`, single-edit "Cell A", capital→Cairo)
| ID | model | France capital edit: same-entity loc / cross loc | status |
|---|---|---|---|
| P1-GPTJ | GPT-J-6B | **67.98%** / 98.95% — same-entity NON-LOCAL | NEGATIVE: GPT-J fails same-entity |
| P1-QWEN7 | Qwen2.5-7B | **99.86%** / 99.94% — clean | PROVEN: Qwen-7B clean at Rung 0 |
| P1-QWEN3 | Qwen2.5-3B | **98.41%** / 99.72% single-edit clean | PROVEN single-edit; (sequential fails → see Tier-1) |
_Decision D-S242-HMODEL-1: same-entity locality is model- AND size-dependent (contra "model-general failure" prior)._

## RECIPE DEVELOPMENT — sequential multi-field on Qwen2.5-3B (`s243_alphaedit_*`)
| ID | method | edit-1 retention after edit-2 | untouched-attr loc | status |
|---|---|---|---|---|
| R-MEMIT | stock MEMIT in-solve | **33.3%** | 78.08% | baseline (sequential clobber) |
| R-ALPHA | in-solve AlphaEdit (null-space P + cache_c) | **100%** | ~74–81% | PROVEN: fixes clobber (LAW#5 inertness proven) |
| R-TUNE | AlphaEdit threshold sweep | 0.02→100%/73.31% · **0.005→100%/80.69%/expr100%** · 0.001→0%/16%(over-constrained) | — | PROVEN: `nullspace_threshold=0.005` optimal |
_Decisions D-S243-ALPHAEDIT-1, -TUNE-1._

## TIER 1 — concept-critical (`s244_*`, Qwen2.5-3B unless noted)
| ID | test | result | status |
|---|---|---|---|
| T1.1 | durability at depth (33-edit stream) | edited-fact cumulative retention **100% throughout**; perplexity flat 3.74; BUT un-edited control cross-entity loc collapses **99.83%→11.99%** | PARTIAL: retention+no-forgetting PROVEN; cross-entity-at-depth FALSIFIED |
| T1.1b | preserve-sampling mitigation | at 24 edits: baseline control **22.39%** → mitigated preserve **99.81%** / held-out control **78.38%** | PROVEN: preserve-sampling fixes cross-entity (generalizes); coverage knob |
| T1.2 | novel-entity insert (sequential) | expressed 18/18; novel multi-field retention **33.3%**, full-records **0/6**; real entities preserved 99.99% | NEGATIVE: novel sequential insert clobbers |
| T1.2b | novel insert + relation-keying | retention **38.9%**, full-records 1/6 | NEGATIVE: relation-keying doesn't fix novel |
| T1.2c | novel insert BATCHED (joint solve) | retention **100%**, full-records **6/6**, real preserved 15/15 | PROVEN: batched compile fixes novel (= spec L1-buffered batch compile) |
| T1.3 | quantization survival | fp16 ret 100%/post_p 0.98/ppl 4.14 → 4-bit roundtrip ret **100%**/post_p 0.957/ppl 9.23 | PROVEN edits survive Q4 (ppl rise = crude sim quantizer; real Q4_K untested) |

## TIER 2 — operations + scale + structure (`s244_*`, Qwen2.5-3B)
| ID | test | result | status |
|---|---|---|---|
| T2.1 | CRUD | INSERT 6/6, UPDATE 6/6, DELETE(revert) 6/6 (both cache modes); other-facts preserved 94–100% | PROVEN |
| T2.2 | scale (store growth) | 12 facts ret 100%/ctrl 99.6% · 24→100%/93.8% · 33→100%/87.5%; ppl flat ~8 | PROVEN: retention holds; control-loc = coverage knob |
| T2.3 | value diversity (multi-token) | multi-token capital full-value expr **8/8**; control-loc 79.8% | PROVEN: not a single-token artifact |
| T2.3b | entity-domain diversity (people) | store=2, retention 83.3%, control 100% | UNDERPOWERED (only 2/12 screened; suggestive not decisive) |
| T2.5 | compaction-regression | incremental 100% → compacted (batch-recompile) **100%** | PROVEN: facts survive recompile |
| T2.6 | tier isolation (disjoint layer bands) | shared-band STABLE 100→**100** under churn; isolated-band 100→**80** | NEGATIVE/clarifying: layer-band tiering HURTS; protection = cache_c+preserve in SHARED band |

## QWEN3-0.6B RE-VALIDATION (deployment-servable model; `s247–s251`, transformers 4.51)
| ID | test | result | status |
|---|---|---|---|
| A1 | recipe port (covariances+hparams) | band [4-8] covariances computed; engine works under tf 4.51 | PROVEN enabler |
| A2 | recipe smoke + multi-fact | smoke: expressed post_p **0.851**, same 92.82%, cross 96.22%. multi-fact (6): edited **83.3% (5/6)**, control top1 **100%**, control-loc 98.75%, same-entity 90.48% | PROVEN: recipe transfers, no recalibration; clean locality |
| A4 | scale | 4→100%/92.5% · 8→87.5%/78.3% · 12→91.7%/49.1% · 17→**94.1%/29.5%**; ppl flat ~23 | PROVEN: scale transfers; control-loc coverage-knob (0.6B collides faster than 3B) |
| A5 | CRUD + compaction | INSERT 6/6, UPDATE 5/6, DELETE 6/6; compaction 100%→100% | PROVEN: tiers transfer to deployment model |

## LARQL INTEGRATION (log-based evidence; see `LARQL_INTEGRATION_ASSESSMENT.md`)
| ID | finding | evidence | status |
|---|---|---|---|
| L-CPU | LARQL CPU inference correct | Qwen3-0.6B `run "capital of France"` → "**Paris**…" coherent; `INFER`→Paris 65.6%; CPU unit tests 14/14 | PROVEN: deployment-CPU backend works |
| L-BIAS | Qwen2.5 garbage = extraction drops attn bias | vindex `family:qwen2`, weight_manifest **0 bias tensors**; Qwen3 (no bias, qk-norm) serves clean | PROVEN root-cause (Qwen2.5-specific extraction bug) |
| L-COMPOSE | native in-weight install (COMPOSE) immature | gate_scale=30 default corrupts; ALPHA=0.3 installs but bleeds cross-entity (no preserve-sampling) | NEGATIVE: LARQL native in-weight write not clean |
| L-COMPACT | native MEMIT consolidation blocked | "No edge metadata available for MEMIT solve" persists even with BEGIN PATCH+relation+COMPOSE | NEGATIVE: COMPACT metadata flow incomplete (LARQL gap) |
| L-VERIFY | ROUTE VERIFY fixes KNN cross-entity bleed | baseline Italy/Spain→Berlin(bleed) → with ROUTE VERIFY → Italy→Rome, Spain→Madrid, France keeps Berlin | PROVEN: no-code collision fix (retrieval/L1 path) |
| L-ROLL | rollback by frozen base | serve base alone → France→Paris (original); base unmodified | PROVEN: governance-by-construction (file-level) |
| L-COMPILE | COMPILE bakes overlay→weights | "Down overrides baked: N"; bakes whatever the overlay holds | PROVEN mechanism |
| **L-BRIDGE** | **decoupled bridge: clean+in-weight+governed, no LARQL code** | our clean edited down_proj → `.vlp` (15360 down-overrides, full band) → `APPLY` on frozen base → `COMPILE` → serves **France→Berlin 79%, Japan→Cairo, Italy→Oslo, Poland→Nairobi; controls Greece/Egypt/China preserved; rollback→Paris** | PROVEN end-to-end on Qwen3-0.6B |

## CP1 — GOVERNED IN-PIPELINE MEMIT WRITE (`cp1_governed_write.py`, 2026-06-18; full detail in `07_CP1_*`)
| ID | test | result | status |
|---|---|---|---|
| CP1-POS | authorized patch → in-step GPU compile → APPLY+COMPILE on frozen base → probe → ledger | COMMITTED; probe France→**Berlin** ✓; compile **1.1s**; **15360** down-overrides; PREPARED+COMMITTED emitted | PROVEN (scope: parametric) |
| CP1-GATE | gate rejects bad-sig/tampered-hash/out-of-scope/replay/expired | **5/5 hard-rejected** (`TOKEN_SIGNATURE_INVALID`,`INTEGRITY_HASH_MISMATCH`,`SCOPE_RELATION_FORBIDDEN`,`TOKEN_REPLAY`,`TOKEN_EXPIRED`); none compiled/committed | PROVEN: Gate enforces §10.2 (5 checks) |
| CP1-ATOM | compile throws mid-step (the n8n question) | mid_compile + mid_mount: **FAILED, PREPARED kept, NO COMMITTED, frozen base unchanged**, WRITE_FAILED forensic | PROVEN: clean-fail atomicity (parametric) |
| CP1-DET | determinism (C-OR2 non-reasoning) | within-process overlay hash identical; **cross-process NOT bit-reproducible** (GPU FP; attn-backward in compute_z) | PROVEN (governance sense); cross-proc repro = non-requirement |
| CP1-LEDGER | hash-chained State Ledger | 19 entries, chain intact | PROVEN |
_Scope: PARAMETRIC-ONLY. Dual-medium 2PC→G1; L1 SELECT probe→CP2 (behavioral stand-in used); asymmetric signing→G2; batch/multi-minute compile duration→G6. Engine UNMODIFIED; governance is our-own-code through the Gate (closes the C16 out-of-band-bridge gap)._

## CP2 — LARQL QUERY-SCHEMA CAPABILITY (`cp2_query_schema_probe.sh`, 2026-06-18; detail in `08_CP2_*`)
| ID | probe | result | status |
|---|---|---|---|
| CP2-SELECT | L1 SELECT read-back of a written edge (§8.9) | `SELECT FROM EDGES` returns **weight-derived feature rows**, not triples; **positive control: native France→Paris NOT readable either** (DESCRIBE→"no edges"); Paris never surfaces | ❌ L1 SELECT-probe NOT provided by LARQL (feature-introspection, not a triple store) — needs OUR schema-layer triple index |
| CP2-DELETE | DELETE FROM EDGES (§8.5) | "Deleted 1 features (patch overlay)"; subsequent SELECT confirms removal | ✅ works (feature-level) |
| CP2-TRIPLE | entity→relation→target model | `INSERT INTO EDGES (entity,relation,target) VALUES(...)` first-class; **installs to KNN store, not MEMIT** | ⚠️ vocabulary present; store feature/KNN-keyed (consistent w/ L-COMPOSE) |
| CP2-FAMILIES | 5 relation families (D6) | `SHOW RELATIONS` → **24,469 emergent decompiler labels** (morphological/economics/…), none are the 5 families | ❌ schema-mapping gap (LARQL relation space is emergent) |
| CP2-VIOLATES | violates hard-reject (C6/C9) | `INSERT … "violates" …` → **ACCEPTED** ("France —[violates]→ Berlin") | ❌ not enforced by LARQL (Validator's job) |
_Net: verbs EXIST + execute (not INFER-only); DELETE works; but L1-triple-readback, 5 families, and violates-rejection are SCHEMA/VALIDATION-LAYER contracts LARQL doesn't provide → concretely-scoped build items (→ schema layer / G3), NOT LARQL modifications. Back-fills CP1's deferred L1 probe: behavioral stand-in was correct; true L1 = our triple index._

## CP3 — MEMIT-COMPLIANCE OF THE RECIPE (analysis, 2026-06-18; detail in `09_CP3_*`)
| ID | claim | basis | status |
|---|---|---|---|
| CP3-D12 | recipe = "MEMIT" per D12 (ROME/GRACE/FT excluded) | engine = kmeng01/memit reference; our code = closed-form down_proj solve `solve(A,B)` w/ null-space `Pi` (not gradient FT; `compute_z` optimizes target vector). **D20 spine:** stock MEMIT has NO orthogonal projection → literal-MEMIT fails D20 → spec's "MEMIT" = family-with-safeguards = our recipe. Null-space step is spec-MANDATED, not deviating. preserve-sampling/batched = standard MEMIT usage | ✅ **CONFIRMED** (method-class; satisfies BOTH D20 safeguards) |
| CP3-C15 | edit band per C15 (L15-25/32-layer, middle-to-late) | our band **[4-8]** for 0.6B(28L) AND 3B(36L); C15 scaled ≈ L13-22(28L)/L17-28(36L) → **[4-8] is early under any reading**. C15 stated declaratively (NOT provisional). Passed locality = supporting, not vindicating | ❌ **OPEN DIVERGENCE** — small-model band calibration vs C15 (→ OQ-W2/G5/G6); spec may need small-model recalibration |
_Net: D12 method-class CONFIRMED (null-space projection is D20-mandated, not an excluded extension); C15 layer-band is a real unresolved divergence, logged not defended-away._

## G1 — DUAL-MEDIUM 2PC + STATE LEDGER + TC + CIRCUIT BREAKER (`g1_two_phase_commit.py`, 2026-06-18; detail in `10_G1_*`)
| ID | test | result | status |
|---|---|---|---|
| G1-HAPPY | git FIRST → vindex SECOND (D46) → COMMITTED binds git↔overlay | real APPLY+COMPILE; served "Berlin"; pair logged | ✅ |
| G1-D46 | git-first fails → vindex never attempted (Weights-ahead unreachable) | ABORTED, vindex untouched, active unchanged | ✅ |
| G1-COMP | C-TC2 asymmetry: Structural auto git-revert (≤3); Layer4 PARK + HIL (≤5, no auto-revert) | both hold; operator-confirm reverts parked Layer4 | ✅ |
| G1-ROLLBACK | COMMITTED → dual rollback → base serves original | git reverted + pointer→base; base serves "Paris" | ✅ |
| G1-DIVERGE | out-of-band git commit (§11.13) + vindex-pointer flip → DIVERGED → trip | both detected + tripped; sanctioned park does NOT false-trip | ✅ |
| G1-CIRCUIT | 3-consec trip → READ_ONLY → reject → both reset-precondition arms gate → resume | all hold | ✅ |
| G1-TPC4 | fabricated COMMITTED-without-PREPARED is DETECTED (not just avoided) | detector flags bypass, not legit | ✅ |
_Scope: dual-medium 2PC machinery PROVEN. Caveats: failure-path compensation reverts GIT ONLY (vindex written 2nd; vindex reversal shown separately by rollback); divergence detection ASYMMETRIC (git=real content, vindex=pointer-metadata not artifact re-hash → G2/G6); reset = precondition-stub for IC-TC-RESET ceremony (→ G2); PREPARED-timeout + cross-task-trip deferred. Engine/git UNMODIFIED._

## KNOWN GAPS (NOT yet evidenced — the council's audit targets)
- **G1 Governance/consistency**: ✅ **2PC + State Ledger (Git↔.vindex pairing) + Transaction Controller (C-TC2) + circuit breaker PROVEN-FOR-SCOPE (2026-06-18, `10_G1_*`).** Remaining: content-level vindex integrity (→G2/G6), full signed reset ceremony (→G2), PREPARED-timeout + cross-task trip.
- **G2 Security**: ✅ **PROVEN-FOR-SCOPE (2026-06-18, `g2_security_layer.py`, `11_G2_*`).** REAL Ed25519: verify-cannot-forge is STRUCTURAL (T-NO-PRIVKEY: no private key reachable from Gate/CeremonyVerifier — retires CP1's HMAC), content-level overlay integrity (signature over re-hashed bytes defeats the metadata-rewrite that fooled G1's pointer check), CAK CeremonyToken verifier (IC-TC-RESET §20.3 with airtight structural exclusion — replaces G1's reset stub), + per-patch edge-cap, agent suspension, naive ledger-tamper detection. 9/9 tests. Remaining: key CUSTODY (offline/HSM, v2/ops), anchored-head ledger IMMUTABILITY (current = naive-tamper detection only), full multi-dimension blast-radius, real boot integration, audit_category enforcement.
- **G3 Validation pipeline**: ✅ **PROVEN-FOR-SCOPE (2026-06-18, `g3_validation_pipeline.py`, `12_G3_*`).** Deterministic schema/static validator delivers the two CP2-surfaced contracts: `violates`/undeclared-relation rejection vs the real §7.3 five families BEFORE MEMIT (C5/C6/C9), + the §8.9 storage-probe SPLIT (triple-SELECT expressibility LARQL lacked + storage-pass/behavior-fail reconciliation). Plus §9 invariants: actor-critic identity-collision rejection, fail-fast cascade, code_pass_patch_fail disposition (§9.7), injection hard-reject-never-retry (§9.8 C29), bounded never-discard retry control-plane (§9.5/9.6), signed-PASS handoff refusing forged/unsigned PASS (§9.9, G3→CP1). 8/8. Caveats: storage-truth rides on a BEHAVIORAL signal (index = intent/expressibility only); Reflexion = control-plane only (LLM fix stubbed); independence = identity-collision tested (sequencing-D33 construction-asserted); only STATIC level fully real; determinism = documented property not a finding.
- **G4 Query schema**: only `INFER`/`run` (generation) tested. Full `SELECT`/`DESCRIBE`/`DELETE FROM EDGES`, triple model, deletion semantics — **UNTESTED.**
- **G5 Operator hardware**: pod Linux-CPU proxy only; **operator Intel CPU UNTESTED** (D1).
- **G6 Scale/efficiency**: **G6.1 SCALE-OF-N DONE (2026-06-18, `13_G6_1_*`, `g6_scale_n.py`) — SPLIT, first empirical falsifier.** Qwen2.5-3B in-solve AlphaEdit, N=100 (50 entities × 2 fields), sequential. ✅ **Write-side PASS:** 98% retention @ N=100, **apply-expression 100% through record 100** (cache_c-strangling did not fire), within-entity 95.6%, global 98.4%. ❌ **Cross-entity consistency FAIL:** held-out top-1 correctness on the edited relation collapses **100→91.7→58.3→41.7%** (baseline→N26→N50→N100) — genuine read corruption (stable==correct), relation-SPECIFIC (continent control 100% stable), scale-amplifying. **Falsifies "cross-entity-clean at scale" for subject-keyed AlphaEdit; SCOPES the prior "VALIDATED" to same-entity-only.** Next falsifier: entity-aware in-solve projection at scale. STILL UNTESTED: larger Qwen3, real-GGUF-Q4_K, overlay size-at-scale (volume-gated).
- **G7 Multi-token values** partially express (Spain "Hanoi"→"H"); **multi-token robustness UNTESTED.**

## ⭐ 2026-06-18 (post-B3) — E1 / B1 / C2 (deployment + size-density + keying mechanism)
| ID | claim | result | status |
|---|---|---|---|
| **E1-A** | edited Q4_K_M store serves correct recall on CPU at acceptable tok/s | llama.cpp `-ngl 0`: edited 100% / native 97.4%; ~8–13 tok/s prompt-eval (pod CPU proxy) | ✅ **PASS** (`18_E1_*`) |
| **E1-B** | LARQL `gguf-to-vindex` is the serving substrate for Qwen2.5-3B | vindex loads only after a vocab-config fix (151643→151936), then serves GARBAGE — 0/108 attn biases extracted. **A7 causal ablation: zeroing q/k/v bias in HF alone → garbage** (proven sufficient cause). | ❌ **FALSIFIED** — LARQL-side bias-drop (not the store); model-family split (Qwen2.5 edit-validated vs Qwen3 LARQL-servable). D-E1-1 ⟨D-E1-1@55708623⟩ |
| **B1** | A1 batch-clean (cross-entity) replicates at larger model (Qwen2.5-7B) | write-side 100%/100%, inertness INERT; held-out edited-rel top-1 **100%(N=0)→91.7%(N=100, 11/12)**; continent control 100% stable | 🟡 **PARTIAL** — not the flat-100% of 3B; small residual at 7B (one probe). Scopes A1 to 3B/N≤100. Directional size-density (confounded). D-B1-1 ⟨D-B1-1@2ebae54e⟩ (`19_B1_*`) |
| **C2** | relation-inclusive keying reduces same-relation key collinearity (root-cause fix) | relation keying makes keys MORE collinear (0.93–0.99). Depth map: separability U-shaped, **min L8–12 (0.20–0.42)**, max late L24–28 (0.88–0.91) | ⛔ **PRUNED** + mechanism mapped. C15 tension (L15-25 = worst isolation zone); new lead band [8-12]. D-C2-1 ⟨D-C2-1@e2eff6af⟩ (`20_C2_*`) |
_Net: CPU deployment loop CLOSED via llama.cpp (E1-A); LARQL serving bias-architecture-gated (E1-B, causally grounded by A7). A1 batch-clean largely-but-not-perfectly size-robust (B1). Cross-entity bleed = a measured layer-resolved key-collinearity phenomenon, minimal at L8-12 (C2)._

## ⭐ 2026-06-20 — D1 capacity law (concentration-vs-dilution drift variable, `22_D1_CAPACITY_LAW`, D-D1-1 ⟨D-D1-1@0db8d819⟩)
| ID | test | result | status |
|---|---|---|---|
| D1-P1 | predictor map (no-edit `compute_ks`, Qwen2.5-3B) | covariate (same-rel cross-ent collinearity @[4-8]) capital 0.436 > language 0.412 > continent 0.333; D7 dissociation 1.71→2.38 | covariate ranking set; D7 basis-rotation weak-moderate (relation-clustering falls, not entity rising) |
| D1-P2 | CONCENTRATED 50 capital vs DILUTED 17cap+17lang+16cont, FIXED total-N=50, band[4-8] seq, 4 seeds×2 orderings, LAW#5 ✓ (|Δ|=0.0007), fixed disjoint 12-entity held-out | held-out capital @ equal total-N: CONC mean 52.1% vs DIL 83.3%, **concentrated more corrupted 4/4 seeds** (gaps 50/16.7/41.7pp); 2 CONFIRM+1 PARTIAL; seed3 INVALID (continent under-expr 81.2%) | **PARTIAL aggregate; ROBUST directional: global `edge_count_since_anchor` (§8.7) INSUFFICIENT → drift must be relation-concentration-aware** (OQ-W1/§7.2). NOT settled = two-variable law (concentration + smaller cross-relation term); thresholds/size-term UNSET. **Dual-reviewed** (Opus + gpt-5.5 `FIX-FIRST` applied); independence CLOSED (directional). NEXT: high-cardinality replication + B1 size term. |

## ⭐ 2026-06-20 — C2-band falsifier (sequential band [4-8] vs [8-12], `21_C2BAND_*`, D-C2band-1 ⟨D-C2band-1@c6fb6103⟩)
| ID | test | result | status |
|---|---|---|---|
| C2-band | low-collinearity band [8-12] vs [4-8], sequential N=100, Qwen2.5-3B, 1 seed | cross-entity JS loc 67.68→86.41 (+18.73pp); within-entity JS 95.48→**77.77** (−17.71); global 97.34→98.40; held-out same-rel top-1 7/12→10/12 (Fisher p≈0.37, n.s.); retention 98→96 | **PASS (mechanical) — NOT PROMOTED to PROVEN: a REAL direction-specific redistribution (within-loc FALL + expr 100% rule out under-editing), underpowered (1 seed); within-entity top-1 cost & mechanism UNMEASURED.** Not a recipe change (batch already clean). De-confounders queued. |

## ⭐ 2026-06-21 — B1 model-size term (D1 concentration law × model size, `22` B1-§, D-B1-2 ⟨D-B1-2@0db8d819⟩)

| sub | setup | result (verbatim) | verdict |
|---|---|---|---|
| B1-replicate | D1 dose-response ported to **Qwen2.5-7B** (intermediate 18944) vs matched in-session 3B; band[4-8] seq; LAW#5 gates ✓ (3B |Δ|=0.0002/0.0003, 7B |Δ|=0.0000/0.0001); engine UNMODIFIED | held-out capital R_pure means 7B k24/36/42 = 58.3/37.5/33.3 vs 3B 65.3/41.7/29.2; **monotone on means both models, expr 100%, pos-control fires** | **REPLICATE — concentration law is MODEL-GENERAL → §8.7 per-relation-concentration amendment generalizes across size (the win)** |
| B1-size | paired (same shuffles), 7B−3B | mean −2.3pp (noise-dominated); **after removing a proven-noise seed3 draw: 7B less-corrupted in 7/8 cells, +11.5pp** | **UNRESOLVED, weak protective lean** — ≪ run-noise at n=3; NOT size-invariance, NOT size-worsens |
| B1-instrument | 7B seed3 re-run, IDENTICAL config | k24 **20.8%→70.8%**, k36 4.2%→41.7% | **~50pp run-to-run nondeterminism**; the apparent '7B collapse' (4–21%) was a NON-REPRODUCIBLE noise draw, NOT a tail mode (advisor-mandated re-run). Single-run absolutes unreliable → noisy sequential instrument can't set the numeric §8.7 threshold |

_§8.7 structural amendment WRITTEN as operator proposal (`docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`): `max_relation_concentration_since_anchor` drives drift_tier worse-of vs global edge-count; numeric threshold OPEN (needs lower-variance instrument). Harness VRAM fixes (eigh-for-P, diagonal-add, del-Pi, expandable_segments) proven inert. Dual advisor pass. Memories [[sequential-edit-run-nondeterminism]], [[wide-intermediate-7b-editing-vram]], [[calibrate-symmetrically-unresolved-is-a-verdict]]._


### D-D1-2 ⟨D-D1-2@e023d8d2⟩ — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (max unanchored per-relation concentration; anchor by k=2; WARNING k=2-3, HARD k=8-10 — REVISED down from k≤2 after the seed-2 across-held-out check). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log. **MIXED-LOAD:** pure-capital fails under +12 other-relation load (mixed clean ceiling k=0; driver=other-relation volume) → vindicates the worse-of(global,per-relation) amendment design; pair k≤1 with a global-volume bound + compaction. **SEED-2 (more-toxic held-out):** corrupts at k=1-2 where seed-3 was clean → ceiling k≤2→k≤1; no per-relation count is universally clean (held-out-dependent SENTINEL, not the causal var). +results/d1_mixedload_smoke_3b_s3.json, results/d1_threshold_lowk_3b_s2.json.
