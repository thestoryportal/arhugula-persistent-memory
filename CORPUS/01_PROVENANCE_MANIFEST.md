# 01 — PROVENANCE MANIFEST (claim → artifact → numbers)
_Every experiment ID maps to its script, result artifact, and the exact numbers. Council subagents MUST cite from this (path + number) or flag `UNVERIFIABLE`. All paths under `/workspace/`._

| ID | script | result artifact | key numbers (verbatim) |
|---|---|---|---|
| P0-GPTJ | s242_gatecal.py | s242_gatecal_gptj.json | null France: same_entity.pct_locality 99.06, cross 97.88, post_p 0.99254 |
| P0-QWEN7 | s242_gatecal.py | s242_gatecal_qwen.json | null France: same_entity 99.4, cross 96.24 |
| P1-GPTJ | s243_phase1.py | s243_phase1_gptj.json | cellA capital France: same_entity 67.98, cross 98.95, post_p 0.988 |
| P1-QWEN7 | s243_phase1.py | s243_phase1_qwen.json | cellA capital France: same_entity 99.86, cross 99.94 |
| P1-QWEN3 | s243_phase1.py | s243_phase1_qwen3b.json | cellA capital France: same_entity 98.41, cross 99.72, post_p 0.995 |
| R-MEMIT/R-ALPHA | s243h_alphaedit_insolve.py | s243_alphaedit_insolve.json | memit retention 0.333 untouched 78.08; alphaedit retention 1.0 |
| R-TUNE | s243i_alphaedit_tune.py | s243_alphaedit_tune.json | 0.02:{ret1.0,unt73.31} 0.005:{ret1.0,unt80.69,e2expr1.0} 0.001:{ret0,e2expr~0.16} |
| T1.1 | s244a_durability.py | s244_durability.json | thresh0.005; retention 100 @ n=1..33; control 99.83→50.63(n5)→26.7(n10)→18.8(n20)→11.99(n33); ppl 3.744→~3.7 |
| T1.1b | s244b_durability_mitigation.py | s244_durability_mitigation.json | n24 baseline ctrl 22.39; mitigated preserve 99.81 / ctrl 78.38 |
| T1.2 | s244c_novel_insert.py | s244_novel_insert.json | inserts18 expr18 retention33.3 full_records0/6 real_loc99.99 pre_known0 |
| T1.2b | s244e_novel_relkey.py | s244_novel_relkey.json | retention38.9 full_records1/6 real_top1 15/15 |
| T1.2c | s244f_novel_batched.py | s244_novel_batched.json | retention100.0 full_records6/6 real_top1 15/15 |
| T1.3 | s244d_quant.py | s244_quant.json | fp16{ret100,post_p0.98,ppl4.136} q4{ret100,post_p0.957,ppl9.23} n_edits8 |
| T2.1 | s244g_crud.py | s244_crud.json | accumulate: all insert/update/delete ok=true; collateral 94.1–100 |
| T2.2 | s244j_scale.py | s244_scale.json | 12f:{ret100,ctrl99.6} 24f:{100,93.8} 33f:{100,87.5}; ppl 8.42→8.03 |
| T2.3 | s244k_diversity.py | s244_diversity.json | multitoken_capital_expr100 currency100 language100 control_loc79.8 |
| T2.3b | s244l_domain_diversity.py | s244_domain_diversity.json | store2 facts6 expressed5 retention83.3 full1/2 control100 (underpowered) |
| T2.5 | s244h_compaction.py | s244_compaction.json | incremental100 compacted100 n_facts18 PASS |
| T2.6 | s244i_tier_isolation.py | s244_tier_isolation.json | shared{aw100,ac100} isolated{aw100,ac80} |
| A1 | s246_qwen3_cov.py | covariance_caches/_dev_shm_qwen3_model/ | 5 band-layer cov npz (3072²); L4 654s..L8 1006s |
| A2-smoke | s247_qwen3_recipe.py | s247_qwen3_smoke.json | expressed true post_p0.851 same92.82 cross96.22 gate EXPRESSES |
| A2-multi | s248_qwen3_multifact.py | s248_qwen3_multifact.json | edited_retention83.3 control_loc98.75 control_top1 100 same_entity90.48 |
| A4 | s250_qwen3_scale.py | s250_qwen3_scale.json | 4:{100,92.5} 8:{87.5,78.3} 12:{91.7,49.1} 17:{94.1,29.5}; ppl ~23 flat |
| A5 | s251_qwen3_crud_compaction.py | s251_qwen3_crud_compaction.json | crud{ins6,upd5,del6,n6} compaction{incr100,comp100} |
| L-* (LARQL) | (LQL one-shots) | larql_*.log, LARQL_INTEGRATION_ASSESSMENT.md | log-based — see assessment doc for transcripts (run/INFER outputs) |
| L-BRIDGE | s252b_build_vlp_full.py + build_vindex_overlay.py | bridge_full.vlp / packaged.vlp + LQL serve logs | 15360 down-override ops; served France→Berlin 79.07, Japan→Cairo 65.69, Italy→Oslo 81.45, Poland→Nairobi 96.12; controls Athens/Cairo/Beijing; rollback→Paris 81.93 |

## Reproducibility notes
- Editing scripts need **transformers==4.51.0** for Qwen3 (5.x breaks engine nethook; 4.45 lacks Qwen3). Covariance caches durable in `/workspace/covariance_caches/`.
- LARQL artifacts (`.vlp`, vindexes, edited models) live in `/dev/shm/` (tmpfs, EPHEMERAL) — reproducible from scripts. Durable deliverables: scripts, hparams, covariances, `build_vindex_overlay.py`, the CORPUS, the assessment/checkpoint docs.
- LARQL findings are LOG-based (one-shot LQL), transcripts quoted in `LARQL_INTEGRATION_ASSESSMENT.md`. To re-verify: rebuild `/dev/shm/qwen3.vindex` (convert) + re-run the LQL.
| D-D1-1 | experiments/track_d/d1_dose_response.py | results/d1_dose_response_result.json | R_pure means k24/36/42 = 51.4/23.6/26.4 (3B, fixed total-N=48); LAW#5 |Δ|=0.0015 |
| D-B1-2 | experiments/track_b/b1_size_dose_response.py | results/b1_{3b,7b}_dose_response_seeds123.json | 7B R_pure 58.3/37.5/33.3 vs 3B 65.3/41.7/29.2; 7B seed3 re-run 20.8→70.8 (~50pp run-noise); LAW#5 7B |Δ|=0.0000 |


### D-D1-2 — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤2`** (max unanchored per-relation concentration; anchor before k=3). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log.
