# EVIDENCE INDEX — LLM-as-Database Viability + Pre-Dev Validation
_2026-06-17. Master durable map of the whole program. Engine kmeng01/memit @ `5c0c706a…c78770` UNMODIFIED throughout (all workarounds config/harness-level; LAW#5 inertness proven for in-solve work). Model under test: Qwen2.5-3B (CPU-class) + Qwen2.5-7B + GPT-J-6B baselines._

## START HERE
- `SESSION_CHECKPOINT.md` — full running state, resume instructions, every result + decision ID.
- `write_engine_viability_determination_report.md` — the VERDICT (viability determined).
- `write_engine_viability_determination_plan.md` — the determination program. `spec_predev_validation_plan.md` — the pre-dev forward-testing program (Tiers 1–3).
- `framework_finding_v1_10_additive.md` — consolidated finding (calibrated metric + model/size dependence).
- `memory_mirror/` — copy of the agent memory (also at /root/.claude/projects/-root/memory/).

## HEADLINE VERDICT
In-weight, MEMIT-class, multi-field same-entity editing IS viable. Model- & size-dependent: GPT-J fails; Qwen-7B clean at Rung 0; small Qwen-3B (CPU target) reaches reliable multi-field via in-solve AlphaEdit (null-space P + sequential cache_c) + batched compile + preserve-sampling. Edits survive Q4. CRUD + compaction work. Every fix maps to a spec mechanism the spec already specifies (overlay/MEMIT, batched compile §8.3, orthogonal projection §8.2, drift/anchor §9, compaction).

## EXPERIMENT LEDGER (script → result JSON → headline)
| ID | script | result | headline |
|---|---|---|---|
| Gate A | s240_gptj_positive_control.py | s240_gptj_positive_control.json | GPT-J cross-entity clean but same-entity drift 2.48 (non-local) |
| Phase0 v1 | s241_gatecal.py | s241_gatecal_{gptj,qwen}.json | HALT — no clean floor (degenerate stimulus) |
| Phase0 v2 | s242_gatecal.py, s242_screen.py | s242_gatecal_{gptj,qwen}.json, s242_screen_*.json | METRIC CALIBRATED (clean floor both); GPT-J non-local, Qwen-7B local |
| Phase1 | s243_phase1.py | s243_phase1_{gptj,qwen,qwen3b}.json | sequential retention: GPT-J 43% / Qwen-3B 37.5% / Qwen-7B 100% |
| 3B expr smoke | s243b_qwen3b_expr_smoke.py | (log) | Qwen-3B edits express (config valid) |
| mom2 sweep | s243c_qwen3b_mom2_sweep.py | (log) | Qwen-3B mom2_update_weight=5000 (calibrated) |
| Rung1 relsubj | s243d_qwen3b_relsubj.py | s243_phase1_qwen3b_relsubj.json | relation-keying → same-entity 100% but cross-entity bleed |
| Rung3 post-hoc | s243e/f_qwen3b_rung3*.py | s243_rung3_qwen3b.json, s243_rung3seq_*.json | post-hoc projection: inert✓, single-edit benign, sequential 33→50% (insufficient) |
| Hybrid | s243g_qwen3b_hybrid.py | s243_hybrid_qwen3b.json | relkey+post-hoc proj adds nothing to cross-entity |
| In-solve AlphaEdit | s243h_alphaedit_insolve.py | s243_alphaedit_insolve.json | LAW#5 inertness✓; sequential retention 33%→**100%** |
| AlphaEdit tune | s243i_alphaedit_tune.py | s243_alphaedit_tune.json | nullspace_threshold=**0.005**: retention 100% + untouched 80.7% + expr 100% |
| T1.1 durability | s244a_durability.py | s244_durability.json | edited 100% + no forgetting; UN-edited cross-entity collapses 99.8→12% at depth |
| T1.1b preserve-sampling | s244b_durability_mitigation.py | s244_durability_mitigation.json | held-out cross-entity 22%→**78%**, sampled 100% (mitigation generalizes) |
| T1.2 novel insert | s244c_novel_insert.py | s244_novel_insert.json | novel multi-field retention 33%, 0/6 records (FALSIFICATION) |
| T1.2b novel relkey | s244e_novel_relkey.py | s244_novel_relkey.json | relation-keying doesn't fix novel (38.9%) |
| T1.2c novel BATCHED | s244f_novel_batched.py | s244_novel_batched.json | batched/joint compile → **100%, 6/6** (=spec L1 batch compile) |
| T1.3 quantization | s244d_quant.py | s244_quant.json | edits survive Q4: retention 100%→**100%** (ppl rise = crude sim quantizer) |
| T2.1 CRUD | s244g_crud.py | s244_crud.json | INSERT/UPDATE/DELETE all **100%**, collateral ~97% |
| T2.5 compaction | s244h_compaction.py | s244_compaction.json | facts survive recompile: incremental 100% → compacted **100%** (PASS) |
| T2.6 tier isolation | s244i_tier_isolation.py | s244_tier_isolation.json | layer-band tiering HURTS (shared 100% > isolated 80%) → tiering=rollback, not collision-isolation |
| T2.2 scale | s244j_scale.py | s244_scale.json | validated recipe HOLDS: 33-fact store retention 100%, control-loc 87.5% (vs raw 12%), ppl flat; preserve-anchor coverage = the scale knob |
| T2.3 diversity | s244k_diversity.py | s244_diversity.json | multi-token values (New York/Cape Town/...) full-value expr 8/8=100%, control-loc 79.8% — locality NOT a single-token artifact |
| T2.3b domain diversity | s244l_domain_diversity.py | s244_domain_diversity.json | people domain: directional/UNDERPOWERED (only 5/12 screened confident → 2 store entities; 83% retention, controls 100%). People facts too soft for clean screen; multi-token (T2.3) is the strong generality evidence |
| T2.4 LARQL round-trip | external_prior_art/larql (CLI) | larql_read.log, larql_roundtrip.log | LARQL CLI BUILT & functional (deps openssl+cmake+protoc+openblas apt-installed; binary target/release/larql). PROVEN: model→vindex `convert` COMPLETES (browse-level Qwen2.5-0.5B, 116.7K features, on /dev/shm tmpfs + OPENBLAS/OMP/RAYON=8 — fixes for the 3 env blockers: 65-thread BLAS thrash [stime explode/utime~0], network-FS I/O stall, an invalid --down-top-k flag); `link`/`list`/`lql WALK`/`DESCRIBE` queries EXECUTE through LQL. PARTIAL/GAP: browse-level WALK returns noisy multilingual features (NOT a clean "Paris") — clean read needs INFER (inference-level vindex, running). Write→read round-trip (INFER→INSERT INTO EDGES→re-INFER; INSERT "allocates a feature" per README = add-a-neuron model) ARMED via larql_roundtrip.sh, pending inference convert. NOT yet a clean end-to-end proof. |

## VALIDATED WRITE-ENGINE RECIPE (the spec, empirically confirmed)
Qwen2.5-3B, band [4–8], v_loss 35, lm_head=embed_tokens (tied), mom2_update_weight=5000, in-solve AlphaEdit (null-space P from SVD of wikipedia cov, `nullspace_threshold=0.005`, L2=1, sequential `cache_c`), **batched/joint compile per record**, **preserve-sampling** of existing entities for cross-entity at depth, expression gate (post_p>0.5). hparams: `qwen25_3b_memit_hparams.json`. Cov caches: `/workspace/covariance_caches/Qwen_Qwen2.5-3B/`.

## PRIOR ART / RESEARCH (in /workspace)
external_prior_art/{larql,the-mechanism} (Chris Hay; LARQL=spec query+deploy layer); research_and_specs/{gemma4_editing_research, molab_feasibility_report, model_does_not_unpack_memory, llm-knowledge-editing-same-entity-locality}.md; easyedit_assets/ (AlphaEdit/WISE/GRACE refs); easyedit_upstream/ (full clone).

## DECISIONS: D-S242-CAL-1, D-S242-HMODEL-1, D-S243-SEQ-1, D-S243-RUNG-1, D-S243-ALPHAEDIT-1, D-S243-ALPHAEDIT-TUNE-1, D-S244-DURABILITY-1, D-S244-MITIGATION-1, D-S244-NOVEL-1/2/3, D-S244-QUANT-1, D-S244-CRUD-1, D-S244-COMPACT-1, D-S244-TIER-1. (full text in SESSION_CHECKPOINT.md)

## 2026-06-18 (post-B3) — E1 / B1 / C2 + repo reorg
| exp | script | result | CORPUS | status |
|---|---|---|---|---|
| E1 deploy serving | `experiments/deployment/e1_probe.py`, `experiments/track_b/a7_bias_ablation.py` | `results/e1_larql_serve_result.json` | `CORPUS/18` | A PASS (llama.cpp) / B FALSIFIED (LARQL Qwen2.5 bias-drop; A7 causal) |
| B1 size-density | `experiments/scale/g6_scale_n_param.py` | `results/b1_7b_size_density_result.json` | `CORPUS/19` | PARTIAL (7B 91.7%) |
| C2 keying + depth | `experiments/track_c/c2_key_collinearity.py`, `c2b_depth_map.py` | `results/c2_result.json`, `results/c2b_depth_map_result.json` | `CORPUS/20` | PRUNED + L8-12 mechanism |
_Repo reorganized: code→experiments/, configs→configs/, results→results/, logs→logs/, docs→docs/, stale→archive/. Scripts use LLMDB_ROOT. See README.md, REPRODUCIBILITY.md, docs/EXPERIMENT_REGISTRY.md._

## 2026-06-21 — B1 model-size term (D-B1-2)
| exp | script | result | CORPUS | status |
|---|---|---|---|---|
| B1 model-size term | `experiments/track_b/b1_size_dose_response.py` | `results/b1_{3b,7b}_dose_response_result.json` (canonical n=3 = `_seeds123`) | `CORPUS/22` (B1 §) | REPLICATE (concentration law model-general → §8.7 amendment generalizes); size threshold UNRESOLVED (~50pp run-noise) |
_§8.7 structural amendment proposal: `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`. LAW#5 gates PASSED (|Δ|=0.0000–0.0003); 7B VRAM fixes proven inert. Instrument finding: sequential-edit corruption ~50pp run-to-run nondeterministic ([[sequential-edit-run-nondeterminism]])._


### D-D1-2 — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤2`** (max unanchored per-relation concentration; anchor before k=3). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log.
