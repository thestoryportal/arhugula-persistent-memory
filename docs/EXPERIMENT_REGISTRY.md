# Experiment Registry

The navigability spine: every experiment → hypothesis, code, result, evidence doc, status, decision-ID. Machine-readable copy: `docs/experiment_registry.json`. Status flags follow `EXPERIMENT_RUNBOOK.md` §0.4. Resolve any basename with `find . -name <name>`.

| ID | track | hypothesis | script | result | CORPUS | status | decision |
|---|---|---|---|---|---|---|---|
| **CP1** | governance | governed in-pipeline MEMIT write (gate + clean-fail atomicity) | `experiments/governance/cp1_governed_write.py` | `results/cp1_result.json` | CORPUS/07 | PROVEN-FOR-SCOPE |  |
| **CP2** | governance | LARQL query-schema capability (SELECT/DELETE/triple/violates) | `experiments/governance/cp2_query_schema_probe.sh` | `results/cp2_probe_results.txt` | CORPUS/08 | RESOLVED (mixed) |  |
| **CP3** | governance | recipe = MEMIT per D12; band vs C15 | `(analysis)` | `` | CORPUS/09 | D12 CONFIRMED / C15 OPEN |  |
| **G1** | governance | dual-medium 2PC + state ledger + circuit breaker | `experiments/governance/g1_two_phase_commit.py` | `results/g1_result.json` | CORPUS/10 | PROVEN-FOR-SCOPE |  |
| **G2** | governance | Ed25519 security: verify-cannot-forge structural | `experiments/governance/g2_security_layer.py` | `results/g2_result.json` | CORPUS/11 | PROVEN-FOR-SCOPE |  |
| **G3** | governance | deterministic validation pipeline (violates/undeclared) | `experiments/governance/g3_validation_pipeline.py` | `results/g3_result.json` | CORPUS/12 | PROVEN-FOR-SCOPE |  |
| **G6.1** | scale | in-weight store cross-entity-clean at scale (N=100) | `experiments/scale/g6_scale_n.py` | `results/g6_scale_n_result.json` | CORPUS/13 | SPLIT (cross-entity FALSIFIED) | D-G6-1 |
| **A1** | scale | batch (Genesis) write eliminates cross-entity corruption | `experiments/scale/g6_scale_n.py` | `results/g6_scale_n_batch_result.json` | CORPUS/14 | PASS | D-A1-1 |
| **A2** | track_a | in-solve relation-balanced sentinels arrest the decline | `experiments/track_a/a2_relbal_sentinels.py` | `results/a2_relbal_sentinels_result.json` | CORPUS/15 | PARTIAL | D-A2-1 |
| **A2b** | track_a | per-edit K_S refresh reduces corruption (staleness?) | `experiments/track_a/a2b_refresh_ks.py` | `results/a2b_refresh_ks_result.json` | CORPUS/16 | RULED-OUT | D-A2b-1 |
| **A7** | track_b | zeroing attn bias causes the LARQL-style garbage | `experiments/track_a/a7_bias_ablation.py` | `logs/a7_bias_ablation.log` | CORPUS/18 | CAUSAL (sufficient) | D-E1-1 |
| **B1** | scale | A1 batch-clean replicates at larger model (7B) | `experiments/scale/g6_scale_n_param.py` | `results/b1_7b_size_density_result.json` | CORPUS/19 | PARTIAL | D-B1-1 |
| **B1-size-term** | track_b | D1 concentration law's model-size term (3B vs Qwen2.5-7B) | `experiments/track_b/b1_size_dose_response.py` | `results/b1_{3b,7b}_dose_response_result.json` (+`_seeds123`/`_seeds345`) | CORPUS/22 (B1 §) | REPLICATE (law model-general); size threshold UNRESOLVED (instrument noise) | D-B1-2 |
| **B3** | track_b | edits survive real Q4_K_M quantization | `experiments/track_b/b3_run.sh` | `results/b3_quant_survival_result.json` | CORPUS/17 | PASS | D-B3-1 |
| **E1** | deployment | LARQL gguf-to-vindex serves the store on CPU | `experiments/deployment/e1_probe.py` | `results/e1_larql_serve_result.json` | CORPUS/18 | A PASS / B FALSIFIED | D-E1-1 |
| **C2** | track_c | relation-inclusive keying reduces same-relation key collinearity | `experiments/track_c/c2_key_collinearity.py` | `results/c2_result.json` | CORPUS/20 | PRUNED | D-C2-1 |
| **C2b** | track_c | key-collinearity depth map (best band for isolation) | `experiments/track_c/c2b_depth_map.py` | `results/c2b_depth_map_result.json` | CORPUS/20 | mechanism mapped | D-C2-1 |

**Historical / Phase-0–1** (gate-calibration s241/s242, model sweep s243, decouple s245–s252, alt-model t1/t3): frozen in `archive/s_series_scripts/` and `archive/notebooks/`; summarized in `docs/framework_findings/` and `docs/session_summaries/`. Not path-rewritten (target the pre-2026-06-18 flat layout).

**Verification:** all script/result paths above were existence-checked at registry build time; ⚠️ marks any missing artifact.


### D-D1-2 — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤2`** (max unanchored per-relation concentration; anchor before k=3). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log.
