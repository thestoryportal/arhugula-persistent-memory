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
| D-D1-1 ⟨D-D1-1@0db8d819⟩ | experiments/track_d/d1_dose_response.py | results/d1_dose_response_result.json | R_pure means k24/36/42 = 51.4/23.6/26.4 (3B, fixed total-N=48); LAW#5 |Δ|=0.0015 |
| D-B1-2 ⟨D-B1-2@0db8d819⟩ | experiments/track_b/b1_size_dose_response.py | results/b1_{3b,7b}_dose_response_seeds123.json | 7B R_pure 58.3/37.5/33.3 vs 3B 65.3/41.7/29.2; 7B seed3 re-run 20.8→70.8 (~50pp run-noise); LAW#5 7B |Δ|=0.0000 |


### D-D1-2 ⟨D-D1-2@e023d8d2⟩ — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (max unanchored per-relation concentration; anchor by k=2; WARNING k=2-3, HARD k=8-10 — REVISED down from k≤2 after the seed-2 across-held-out check). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log. **MIXED-LOAD:** pure-capital fails under +12 other-relation load (mixed clean ceiling k=0; driver=other-relation volume) → vindicates the worse-of(global,per-relation) amendment design; pair k≤1 with a global-volume bound + compaction. **SEED-2 (more-toxic held-out):** corrupts at k=1-2 where seed-3 was clean → ceiling k≤2→k≤1; no per-relation count is universally clean (held-out-dependent SENTINEL, not the causal var). +results/d1_mixedload_smoke_3b_s3.json, results/d1_threshold_lowk_3b_s2.json.

| D-R15-1 | experiments/track_c/r15_constraint_probe.py | results/r15_constraint_probe.json | Tier-0 24/24 (avg p≈0.998); Tier-1 24/24; Tier-2 hand-adj ~11–14/24 flag, ~7/24 silent leak, 2/24 refuse; base 1/24; global-shift 0/4; neutral property-spec 1/24; LAW#5 |Δexpr|=0.0013 |

| D-R9-1 | experiments/track_c/r9_deletion_residue.py | results/r9_deletion_residue.json | write canon 24/24, generalized 19/24; delete-took 12/12; RESIDUE 0/7 (held-out code rank 0→189–27966, p→0); top-5 post=generic filler 6/7; control canon 12/12, held-out 10/12 (2/12 bystander collateral); base 0/24; LAW#5 |Δ|=0.0031 |
| D-C1KVC-1 | experiments/track_d/c1_kvc_grid.py | results/c1_kvc_grid_result.json (+c1_kvc_stats.json) | held-out%: N50{C50 100,C25 99.8,C10 98.0} N100{C100 98.2,C50 96.2,C25 91.7,C10 73.2}; anchors pass; N100_C10 vs clean Δ−0.25 p=0.0009 (JS +0.168 p=0.0001); equal-count refute Δ−0.036 p=0.0038; diff-in-diff N-eff −3.8@C50 vs −24.8@C10; LAW#5 |Δexpr|=0.0008 |
| D-R2-1 | experiments/track_c/r2_reverse_lookup.py | results/r2_reverse_lookup.json | forward-took 24/24; native-reverse ctrl 8/10; reverse base 0/24 → post 0/24; max|ΔP(country)|=0.0003 (max revP 0.0011); LAW#5 |Δexpr|=0.0003 |
| D-R13-1 | experiments/track_c/r13_storage_behavior_split.py | results/r13_storage_behavior_split.json | L1 trained-prompt 24/24; L2 paraphrase P1 2/24,P2 4/24,P3 10/24, any 11/24, all-fail 13/24, mean ~22%; native ctrl L1 10/10,L2-prim 8/10; R9-contrast 79%v22%; LAW#5 |Δexpr|=0.0003 |
| D-R5-1 | experiments/track_c/r5_paraphrase_robustness.py | results/r5_paraphrase_robustness.json (+r5_stats.json) | NOVEL all-3-hit 16/16 mean 100%; PRIOR-single 0/16 mean 25% (revert-to-true 27/36); multi-same 0/16 31%; multi-para 3/16 65%; competitor Fisher p≈0; recipe continuous 13up/0down sign p≈0.0002; L1-took 16/16 all; LAW#5 0.0026 |
| D-R5b-1 | experiments/track_c/r5b_overwrite_prior_edit.py | results/r5b_overwrite_prior_edit.json (+r5b_stats.json) | NOVEL 97.9%/15-16 all-hit; PRIOR 14.6%/0-16; OVERWRITE-EDIT 93.8%/15-16 (v1-resurface 0/3); OVERWRITE vs PRIOR Fisher p<1e-6; vs NOVEL p=1.0; L1 16/16 all; LAW#5 0.0020 |
| D-R1-1 | experiments/track_e/r1_select_readback.py | results/r1_select_readback.json | LANDED read-back 8/8; LEAK SELECT=NULL 6/6 (L2 fires 5/6); GATE-REJECTED NULL 4/4; DROPPED flagged 1/2 (Velloria→Tokyo sig 2.06>thr 2.0 false-recon); LANDED sigs 7.9–10.75 vs DROPPED 0.18/2.06; LAW#5 |Δexpr|=0.0001 |
| D-R1-2 | experiments/track_e/r1_commit_bit_select.py | results/r1_commit_bit_select.json (+r1_commit_bit_ledger.jsonl) | D1 LANDED 8/8; D2 LEAK NULL 6/6 (fires 5/6); D3 REJECTED NULL 4/4 + DROPPED NULL 2/2 via 2PC-abort; D4 Velloria proxy-TRIPLE(2.06)→bit-NULL; D5 chain intact, bypass=[] |
| D-C5-1 | (analysis — spec-read §8.9/8.10/11.2/11.3/11.5/11.14) + tools/(hypergeometric) | results/c5_compaction_probe_power.json; docs/C5_COMPACTION_VERIFY_AUDIT.md | spec MANDATES compaction verify (C-OC3, CORE=1.0 abort); non-CORE sampling FN S=100/10%=0.36; CORE census FN=0; livelock=prediction→C1 |
| D-R11-1 | experiments/track_e/r11_medium_on_read.py (spec-conformance probe; spec-read §7.2/7.4/8.9/11.2/11.3/11.7/26.3) | results/r11_medium_on_read.json | axis-(a) medium/class-on-read & axis-(b) severity-on-read = DERIVABLE-IF-TYPE-RETURNED; read-return shape unspecified (no query-language section); §26.3 provenance_flag is the lone read-result quality field (L4-external only); NOT empirical (documentation echo); NOT promotable |
| D-C10-1 | experiments/track_c/c10_multitoken_value.py (Run1 counterfactual) · c10b_novel_multitoken.py (Runs2+3 novel; engine UNMODIFIED, LAW#5 p-delta+loc gate) | results/c10_multitoken_value.json · c10b_novel_multitoken.json | NOVEL para-full: single 97.2%, coherent-multi 97.2%, INCOHERENT-multi 36.1% (first 70.8%, P(full\|first)=0.51 vs coherent 1.00); incoherent canon-full 95.8% (FITS not GENERALIZES); base 0/24 all; |Δexpr|=0.0003 |Δloc|=0.53; Run1 counterfactual floored 12.5/4.2 | FALSIFIER FIRED; OPEN must-fix for target; cross-family reviewed; NOT promotable |
| D-C6L-1 | experiments/governance/c6_ledger_immutability_redteam.py (reuses real G2 StateLedger/verify_chain; spec-read §13.2/16.1/16.2/16.4/16.5/16.7/27/5) | results/c6_ledger_immutability_redteam.json (+c6_redteam_ledger.jsonl) | K1 rewrite-recompute UNDETECTED (verify_chain INTACT); K2 truncation UNDETECTED; K4 naive-edit DETECTED (control); K5 STH-fix DETECTS K1+K2; K6 finding: (A) no operational-window crypto tamper-evidence (spec-level), (B) §16.5↔§16.2 unreconciled seam. Property-demo+spec-finding; NOT empirical/falsification/promotable |
| D-C1TS-1 | experiments/track_d/c1_scale_city_country_screen.py · c1_truescale_pilot.py · c1_conditioning_diag.py | results/c1_scale_city_country_screen.json · c1_truescale_N2000_diag.json · c1_diag_singletoksubj.log · c1_truescale_substrate_diagnostic.json | screen 2631 native; multi-tok N2000/N100 collapse (ΔW 8900, all-!); single-tok N50/100 clean (held-out 100/86.7%, ΔW 207/294) but expr 42/27%; cost 62min |