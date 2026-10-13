---
status: in-progress
branch: worktree-c10k-route-a
timestamp: 2026-10-09T23:28:55Z
files_modified:
  - results/mathlab_staging/new1_v2_build_report.md
  - tests/test_new1_geometry.py
  - tests/test_new1_supervisor.py
  - tools/mathlab_events.py
  - tools/new1_geometry.py
  - tools/new1_supervisor.py
---

## Working on: NEW1 terminal durability B2

## 2026-10-09 — Context handoff: NEW1 B2 OPEN (Astra r2)

**Status: FIX-FIRST · B2 NOT RESOLVED · B1/B3 RESOLVED per Astra r2 · shared-contract repair NOT STARTED · no new RED/GREEN run · real geometry NOT RUN · no commits.** This dated section supersedes the previous section's B2 completion claim. Read `results/mathlab_staging/new1_build_astra_r2.md` fully. The earlier 66 NEW1 / 150 shared-consumer GREEN receipts do not cover terminal durability and do not establish B2 acceptance.

Astra's controls expose the missing boundary: `tools/mathlab_events.py:132–134` writes the terminal line before fsync; `:232` accepts a readable PASS as committed. A terminal-fsync timeout returned **STOPPED-DEADLINE**, while `fold()` showed **finished/PASS, all four prediction verdicts and the finding**. Persistent terminal I/O failure combined with failed halt persistence produces the same false completion (`tools/new1_supervisor.py:363–380`). The existing terminal deadline fixture sleeps before append (`tests/test_new1_supervisor.py:510`) and cannot prove durability. B1's 300-s cell deadline, B3's persisted contrasts and the selected-column allocation advisory are resolved in r2.

**Next step for a fresh successor:** reproduce both actual append→fsync failure controls as RED before editing production, then implement the smallest shared event-publication protocol that requires durable terminal commitment. An uncommitted/torn terminal must fold as INCOMPLETE/INVALID, with no PASS, prediction verdicts or NEW1 finding; failed halt persistence must not be required to retract a false PASS. A commit-marker design is explicitly authorized, but merely moving the same readable-before-fsync race into its marker is insufficient. Preserve the pure fold / sole stream authority contract and backward compatibility: existing committed harvest, m2 and m3 streams must retain their recorded outcomes. No implementation design has been selected or applied in this request.

Exact repair surface: `tools/mathlab_events.py`, `tools/new1_supervisor.py`, `tests/test_new1_supervisor.py`, plus necessary shared-contract tests. Existing geometry sources/tests are `tools/new1_geometry.py` and `tests/test_new1_geometry.py`. Keep frozen `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` §6 byte-identical (SHA `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741`): admission, 13-GiB pre-SVD, 300-s waits, 1,800-s total deadline, 6-GiB worker/floor limits, monitoring refusals and persist-before-gate semantics remain binding. Latest user authorization explicitly includes the **SHARED** contract; it supersedes the earlier narrow fold-only repair scope.

Rerun all requested modules: `tools.test_dashboard_mathlab`, `tools.labviz.test_mathlab`, `mathlab.test_mathlab`, `tests.test_new1_supervisor` and `tests.test_new1_geometry`. Use CPU/synthetic fixtures, `TMPDIR=/private/tmp`, a fresh evidence namespace, separate fresh processes for stdlib detector/consumer tests and numerical tests. Preserve r1/r2 reviews and every old failed receipt. No real geometry, model/engine runtime, GPU/MPS, full-shape probe, queue action, dependency installation or commit is authorized. Actual runtime feasibility remains UNVERIFIED.

No B2 implementation, test, tool session or review is in flight. Saved successor state, exact test commands, current source hashes and observed git state are in [handoff_codexmb2_new1_b2_20261009T232855Z.md](handoff_codexmb2_new1_b2_20261009T232855Z.md). Previous evidence remains at `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_independent_fix_r1/`. Worktree/root and branch were reverified; other lanes advanced HEAD to `c1091991544b1936b58bd5f1516b5576143b5de0`. Current `docs/MATHLAB_STEP4_PREREG.md:3` explicitly says **SHELVED** after step-3 calibration FAIL / Astra CONFIRM; do not resume step 4 from the older contingent-draft snapshot.

**Context rule, binding through every handoff:** watch **Context N% left**; before approximately **20%**, stop starting new work, write done / in-flight / exact paths / next step / open risks into the task report, and say so for a fresh successor session. Never approach full-window compaction. Every handoff restates this rule. This session has stopped new work and hands B2 to a fresh successor; do not report NEW1 B2 DONE.

### Exact next-turn sequence

1. Read `AGENTS.md` top context section, `DISCIPLINE.md`, the full r2 review, frozen NEW1 §6 and the latest dated report sections. Verify cwd/root/branch and current source hashes. Do not overwrite concurrent changes or old receipts. Use Graft to inspect the shared symbols/callers before implementation.
2. Start a fresh B2 evidence directory. Write meaningful synthetic controls that fail with current production unchanged: terminal append succeeds but its fsync stalls beyond the supervisor deadline; persistent terminal I/O failure plus inability to persist the halt. Verify RED at the actual write/fsync boundary, rather than sleeping before append or raising only after successful fsync.
3. Fix the shared terminal commitment contract. A readable line alone supplies no proof that its fsync completed. Preserve legacy committed recorded streams and fail closed on new uncommitted/torn terminal events, even if no halt receipt can be persisted. Keep ordinary calibration/admission outcomes meaningful; do not globally hide unrelated gates.
4. Verify the new controls GREEN, positive committed NEW1 publication and recorded harvest/m2/m3 compatibility. Run the required modules below; do not weaken existing assertions. Append a dated B2 repair section with RED/GREEN receipts, exact source delta, limits and no-real-geometry status. Reply NEW1 B2 DONE only after this work is actually complete.

### Exact required test commands

Common environment for every command: `PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1`. Prefix shell invocations with `/opt/homebrew/bin/rtk proxy`; all paths below are relative to the verified worktree root. Use distinct fresh interpreter processes.

```sh
.venv/bin/python -B -m unittest tests.test_new1_supervisor tests.test_new1_geometry -v
.venv/bin/python -B -m unittest tools.test_dashboard_mathlab tools.labviz.test_mathlab -v
PYTHONPATH=/private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/lib/python3.11/site-packages .venv/bin/python -B -m unittest mathlab.test_mathlab -v
```

The local .venv has Python 3.11.16, torch 2.8.0, NumPy 2.4.6, safetensors 0.8.0 and tokenizers 0.21.4 (previously verified). It lacks DuckDB. The existing private/tmp cache supplies DuckDB and was previously used with the explicit PYTHONPATH above; recheck availability, install nothing. MathLab tests use tiny synthetic tensors/tokenizer fixtures and recorded metadata, never a model or real geometry. Keep stdlib detector tests out of a process that already imported torch.

### Preserved evidence and restrictions

- `results/mathlab_staging/new1_build_astra_r1.md`, `results/mathlab_staging/new1_build_astra_r2.md`.
- `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_closeout/`: earlier build evidence.
- `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_independent_fix_r1/`: RED/GREEN logs, before/ snapshots, round-only diff, audit and prior context snapshot. Its B2 completion assertion is superseded by r2 and this handoff.
- No fresh B2 failure reproduction or repair has been performed. No subprocess or reviewer is running. No new source modification has occurred since the latest B2 request.
- The old real launch command is recorded only, remains unexecuted and is not permission to run. Keep frozen caps, pins, prediction definitions and prereg unchanged.
- Other lanes' untracked artifacts and committed progress must be preserved. No git mutations, global state writes or memory updates.

### Observed git state before this handoff

HEAD: `c1091991544b1936b58bd5f1516b5576143b5de0`; root: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`.

Tracked diff before this handoff:
```text
 results/mathlab_staging/new1_v2_build_report.md |  47 ++++++++
 tests/test_new1_geometry.py                     |  36 ++++++
 tests/test_new1_supervisor.py                   | 152 +++++++++++++++++++++++-
 tools/mathlab_events.py                         |  16 +++
 tools/new1_geometry.py                          |   7 +-
 tools/new1_supervisor.py                        |  65 ++++++----
 6 files changed, 292 insertions(+), 31 deletions(-)
```

Staged diff before this handoff: empty (successful command, empty output).

Full status before writing this note (untracked paths belong to multiple lanes):
```text
 M results/mathlab_staging/new1_v2_build_report.md
 M tests/test_new1_geometry.py
 M tests/test_new1_supervisor.py
 M tools/mathlab_events.py
 M tools/new1_geometry.py
 M tools/new1_supervisor.py
?? .ignore
?? external_prior_art
?? results/autoresearch_c10_equivalence_2026-10-06T0815.json
?? results/autoresearch_reaim/
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/HALT.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval_halt.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/eval.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/preflight.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch_entered.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_eval_started.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/train/
?? results/c10w_oracle_logs/attempt1_halted/
?? results/c10w_oracle_logs/p2-a1-s1.gate.20261007T220211.50811.json
?? results/c10w_oracle_logs/p2-a7-rt.gate.20261007T220753.90179.json
?? results/c10w_oracle_logs/p2-a7-s1.gate.20261007T214226.17018.json
?? results/c10w_oracle_logs/p2-canon-s1.gate.20261007T215636.11061.json
?? results/c10w_oracle_logs/p2-eval.gate.20261008T030455.59962.json
?? results/c10w_oracle_logs/p2-read-attempt2.json
?? results/c10w_oracle_logs/p2-shuf-rt.gate.20261007T221517.41222.json
?? results/c10w_oracle_logs/p2-shuf-s1.gate.20261007T214924.63725.json
?? results/c10w_oracle_logs/p2_launch_fingerprint.txt
?? results/c10x_enginepath/
?? results/c10x_enginepath_logs/
?? results/c10x_enginepath_rerun1/
?? results/c10x_enginepath_rerun1_logs/
?? results/c10x_enginepath_rerun2/
?? results/c10x_enginepath_rerun2_logs/
?? results/c10x_enginepath_rerun3/audit_A1_single.pt
?? results/c10x_enginepath_rerun3/audit_A7_coined_coined.pt
?? results/c10y_directdw_calib1/
?? results/c10y_directdw_calib2/
?? results/c10y_directdw_calib3/
?? results/c10y_precast_diag/
?? results/c10z_astra/
?? results/c10z_astra_attempt2/
?? results/c10z_astra_attempt3/halt_p1.json
?? results/c10z_astra_benchmark/20261008T104535Z/heartbeat.json
?? results/c10z_astra_benchmark/20261008T104535Z/run.json
?? results/c10z_astra_benchmark/20261008T104535Z/svd_child.json
?? results/c10z_astra_benchmark/20261008T121345Z/heartbeat.json
?? results/c10z_astra_benchmark/20261008T121345Z/run.json
?? results/c10z_astra_benchmark/20261008T121345Z/svd_child.json
?? results/closeout_fold_20261009T223920Z/
?? results/infranodus_research_arc_2026-10-05/fulltext/
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10.txt.rtf
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10_2.txt.rtf
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1207.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1215.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1217.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1219.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1220.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1222.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1223.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1228.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1230.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1233.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1235.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1238.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1240.json
?? results/infranodus_research_arc_2026-10-05/part2/q10_layer_selection_residual.txt
?? results/infranodus_research_arc_2026-10-05/part2/q11_nullspace_generalization_tradeoff.txt
?? results/infranodus_research_arc_2026-10-05/part2/q12_oov_entity_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q14_rephrase_robustness_weight_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q15_fictional_entity_weight_update.txt
?? results/infranodus_research_arc_2026-10-05/part2/q1_subject_embedding_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q4_key_collinearity_interference.txt
?? results/infranodus_research_arc_2026-10-05/part2/q5_novel_entity_continued_pretraining.txt
?? results/infranodus_research_arc_2026-10-05/part2/q7_frame_vs_subject_recall.txt
?? results/infranodus_research_arc_2026-10-05/part2/q8_editing_overfit_paraphrase.txt
?? results/infranodus_research_arc_2026-10-05/part2/q9_covariance_regularization_editing.txt
?? results/infranodus_research_arc_2026-10-05/segments/
?? results/labviz/
?? results/labviz_codex_brief.md
?? results/labviz_codex_impl.md
?? results/labviz_v2_codex_impl.md
?? results/mathlab/calibration.duckdb
?? results/mathlab/harvest_20261009T184950.056951Z/clean.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_A1_single.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_A2_coherent2.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_mint1_s0.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_mint1_s1.pt
?? results/mathlab/harvest_20261009T184950.056951Z/inloop_mint1_s2.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_A1_single.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_A2_coherent2.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_A7_coined_coined.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_mint1_s0.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_mint1_s1.pt
?? results/mathlab/harvest_20261009T184950.056951Z/postedit_mint1_s2.pt
?? results/mathlab/harvest_20261009T184950.056951Z/weights_A7.pt
?? results/mathlab/harvest_20261009T203705.724371Z/
?? results/mathlab/m2_20261009T192823.926873Z/
?? results/mathlab/m2_20261009T211538.263001Z/
?? results/mathlab/m3_20261009T225557.353172Z/
?? results/mathlab_staging/new1_build_astra_r2.md
?? results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_independent_fix_r1/
?? tools/labviz_serve.sh
```

### Current source hashes

| File | SHA-256 at handoff |
|---|---|
| `tools/mathlab_events.py` | `c14d3e6d58e3895573b0d7c4047d89252c43d050af4191350220c6529c623cab` |
| `tools/new1_supervisor.py` | `5a7b8ea2a86c74d8d57946275ebe1c362a9013c1f89f715405ce1c57019a11e7` |
| `tools/new1_geometry.py` | `ca51ab89d3b2003107fc04da8c8297bb360c58b6751c514a93a5761a7d2e6523` |
| `tests/test_new1_supervisor.py` | `30d49c56add81a7df9696d6907b6f44f3999259bd2587140001890e8d8bf91d2` |
| `tests/test_new1_geometry.py` | `ad79af6e3db8aa6d2aad9b58b3306fa555876353c57fc20b567d5d8447db21eb` |
| `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` | `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741` |
| `docs/MATHLAB_STEP4_PREREG.md` | `ae855d7a69ccb07db477bfac1720cc127881bc2331e37f3ec57aef6d28e1c510` |
| `results/mathlab_staging/new1_build_astra_r2.md` | `04a70224cf2a7816face2622724b6ef25ceeca1b4ac511f532119951bdaa36b7` |
