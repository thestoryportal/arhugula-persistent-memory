# Codex MB handoff — 2026-10-09

**BINDING CONTEXT RULE:** watch `Context N% left`. Before approximately **20%**, stop starting new work, write **done / in flight / exact paths / next step / risks** into the task report, and say so in the reply so MAESTRO can start a fresh successor. **Every handoff restates this rule.** MAESTRO invoked this stop; step-4 drafting is paused. No commits, computation, run control or live-file writes are authorized by this handoff.

Worktree root: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch `worktree-c10k-route-a`. Paths below are relative to that root. Preserve other sessions' work and operator commits. Shell commands must use `/opt/homebrew/bin/rtk proxy`.

## Done: builds and diagnosis

- **Steps 1–3:** model-free admission, CPU supervision, harvest observer/persistence, exact solve reproduction, two frozen retrospective proxies, marimo notebooks and provenance index. Main code: `tools/mathlab_{admit,runtime,harvest,cpu_runner}.py`, `tools/run_mathlab_{harvest,cpu}.sh`, `mathlab/{core,fixtures,index}.py`, `mathlab/m2_solve_repro.py`, `mathlab/m3_calibration.py`, `mathlab/test_mathlab.py`, `mathlab/test_index.py`. Shared `tools/mathlab_events.py` was used, never edited. Full history/evidence: **`results/mathlab_staging/build_report.md`** (SHA below).
- **D-ML-2 / prereg §14:** test-first deadline increase to **6540 s** for step 2, **SVD reserve 5 GiB**, solve reserve **9 GiB**; step 3 **1800 s**, index **300 s** unchanged. MAESTRO's full-shape CPU evidence: `results/mathlab_staging/peak_{svd,solve}_full.{json,txt}`; projector **78.95 s / 4.61 GiB**, solve **146.13 s / 8.08 GiB**. Real runner+uv fixture notebooks passed outside the sandbox. These are tooling measurements, not production-feasibility proof.
- **Producer contract + harvest persistence:** standalone admission purpose does not start experiments under `fold()`; real experiment runs attach. Partial captures persist exclusively+fsync before coverage failure/state cleanup, retain occurrence identities, and enter diagnostic-only halt records, never analysis. Evidence directories: `results/mathlab_staging/producer_contract_20261009T181053.740818Z/` and `harvest_persistence_20261009T183202.046125Z/`.
- **Mint norm diagnosis:** `results/mathlab_staging/mint_norm_diagnosis.md`; supporting audit `mint_norm_diagnosis_20261009T193234.646267Z/`. Leading cause: historical native fp32 pre-cast norm versus observer-recomputed fp64 norm. Fresh A1/A7 had the same drift; saved A7 reductions reproduce approximately .0019→.0060. Mint-specific attribution was an inference because its original native norms/full updates were unavailable. This led to frozen **D-ML-3 / §15**, not a relaxed 1e-3 bar.
- **D-ML-3 implementation:** persist the same observed unchanged `H.my_edit` returned `delta_norm` as `n_native`, plus producer Torch version/CPU threads. Historical comparison uses fp64 subtraction/division; missing/nonfinite fail closed. fp64 `upd_norm` remains diagnostic for historical agreement and unchanged gate-2a reference. Evidence: `results/mathlab_staging/dml3_impl_20261009T195833.138642Z/`.
- **D-ML-3 reviewer fix:** collect scalar map/producer metadata **before coverage validation**, including zero captures. Duplicate captures retain operands without ambiguous occurrence scalars; final returned layer-map values persist separately as `returned.l<layer>.n_native`. Both raw stores survive fsync failure; HALT unchanged. Evidence: `results/mathlab_staging/dml3_review_fix_20261009T202255.869402Z/` (`red_behavior.txt`, `green_targeted.txt`, `checks.json`, `implementation.diff`, `final_verification.json`, `context_save.md`). **7 behavioral RED failures → 7 targeted PASS; full MathLab 77, dashboard 53, DuckDB 1, strict marimo PASS.** Independent final review **GO**: `results/mathlab_staging/dml3_impl_astra_r2.md`.

## Current live state: read-only snapshot

- **Harvest 2 PASS; all three mint arms ADMITTED.** Checked terminal PASS event at **21:14:57 UTC** and manifest `replay_admission` at lines **71257–71268**. Operands: **`results/mathlab/harvest_20261009T203705.724371Z/`**. Run/events/admission: **`results/mathlab_staging/runs/harvest_20261009T203702Z_6589/`**. Manifest SHA **`ef72e0adf4d6da5c3272c57a4189b919226dbf290615773d36af9bc746df0731`**.
- **Step 2 on harvest 2 RUNNING at the latest read, 22:11:10 UTC.** Run: **`results/mathlab_staging/runs/m2_20261009T211535Z_57196/`**; output: **`results/mathlab/m2_20261009T211538.263001Z/`**; log: **`results/mathlab/m2_h2_launch_20261009T211535Z.log`**. Completion manifest was not present at the preceding listing. Do not stop, restart, edit or otherwise control it.
- **Step 3 QUEUED**, per MAESTRO; no H2 calibration PASS is established by this note. It must consume only the completed H2 reproduction source chain. Its future exact output/run pins remain pending.
- **Harvest 1 remains separate and invalid for mint calibration:** `results/mathlab/harvest_20261009T184950.056951Z/`, manifest SHA **`bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e`**. Its earlier A1/A2/A7-only reproduction is `results/mathlab/m2_20261009T192823.926873Z/`, run `results/mathlab_staging/runs/m2_20261009T192821Z_82233/`. Never backfill/relabel/merge its rejected mint records or original `results/c10u_mint2/r3/` records.

## Checked identity pins

These hashes were read at handoff; reverify before future work. SHA-256 is over full file bytes.

| File | SHA-256 |
|---|---|
| `docs/MATHLAB_PREREG.md` | `85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8` |
| `tools/mathlab_runtime.py` | `416b597c1309f7dcabb065749e05da9ce28743b1d16c9791ae1eed527a4a72c5` |
| `tools/mathlab_harvest.py` | `c2df98cd599ebbce43409fce0d96b4051929beaa6ad475c0284381367614e348` |
| `mathlab/core.py` | `127bae6d3899db1faae88de56afe31487305355e8dc7b64d80e7b74d9034eb80` |
| `mathlab/test_mathlab.py` | `2b111cd5751f1d1115d2186d8c7d5ac59be329e9700dcefc3c60029ee5a1da76` |
| `tools/mathlab_events.py` | `1c0780d42e3cfd794b68ba742fedb0307c2992bd737507cda65bdd8a864d27a5` |
| `tools/mathlab_cpu_runner.py` | `77ee421368f917283d2aeeea43239c38c482c05924e47942b1de32a155577d31` |
| `tools/run_mathlab_cpu.sh` | `a79e0dedd366c7721f8a9e84214f63f52d293ae8f38740068874f4e0256b8007` |
| `results/mathlab_staging/build_report.md` | `5e1626da6e26044d8bddd95d9422753a06d65daa820ae598e0bffca68544b9de` |
| `results/mathlab_staging/mint_norm_diagnosis.md` | `e9ec9d9a412348f0c8cedbcef7d1a2e33aa06bd52d41ac9ccfdf0aaec4346f24` |
| `docs/MATHLAB_STEP4_PREREG.md` — unfinished draft | `9da5d4b8c9fe532b2b55c79b9d7f453a9d6c2d07a95d87edd307fc2e7ec1799b` |

## Verification commands / runtime notes

**Reference commands only; none rerun for this handoff.** Existing `.venv` serves MathLab/dashboard tests. Real DuckDB/marimo uses the already resolved uv environment below; probe availability rather than installing globally. Use writable **`TMPDIR=/private/tmp`** to avoid marimo temporary-directory exceptions. Every numerical check uses CPU, empty CUDA visibility, eight threads and disabled bytecode writes.

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest mathlab.test_mathlab -v
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_dashboard_mathlab -v
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 /private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m unittest mathlab.test_index -v
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 /private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m marimo check --strict mathlab/m2_solve_repro.py mathlab/m3_calibration.py
/opt/homebrew/bin/rtk proxy bash -n tools/run_mathlab_cpu.sh tools/run_mathlab_harvest.sh
```

Headless acceptance means the **real admission + runner + PEP723/uv path**, not direct Python notebook execution. The runner delegates `nice -n 10 /opt/homebrew/bin/timeout -k 30 <deadline_s> uv run --script <notebook>`; m2=6540, m3=1800. Earlier sandbox process/network denials were cleared by MAESTRO outside it; PyPI resolved torch 2.8.0, marimo 0.25.1, DuckDB 1.5.6. Do not claim a direct cached fixture run proves this live boundary. Graft CLI needs `env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin`; do not upgrade tools mid-task.

## Step 4: started, unfinished; successor work only

**Text exists:** `docs/MATHLAB_STEP4_PREREG.md`, DRAFT v1 / NOT FROZEN / NOT RUN. It was written just before interruption; **final source/citation validation and post-draft review were NOT completed**. Do not announce `STEP4 DRAFT DONE`, execute it, or treat its proposed spending caps as measured feasibility. No notebook/runner extension, numeric computation, InfraNodus request, queue change or tests were performed.

Read first: `docs/MATHLAB_PREREG.md` §0, §4.3, §5, §7, §8 (and binding §14/15); `results/mathlab_staging/infranodus_trial/SUMMARY.md`; `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` (current DRAFT v2, style only). Preserve operator intent verbatim from the draft. Step-3 H2 FAIL/INVALID **shelves step 4**; even PASS leaves prospective queue utility unverified.

Design notes already folded: candidate source/novelty audit; ≤12 sealed cards; three fixed original-anchor diagnostics (raw layer transfer contribution, collateral self/cross terms, all-subject heterogeneity); ≤6 units; proposed 1800-s complete-cycle cap including waits/indexing. Calibration applies only to **original anchors**, not new interventions, scalar envelopes or geometry. The shadow list orders **anchor-support groups**, never inferred research-question benefit; novel interventions remain uncalibrated. Actual reorder/prune also needs separately demonstrated prospective utility. GPU entry still needs an independent complete prereg, **formal Astra FREEZE**, operator budget/placement and normal admission. Current runner permits only m2/m3; shared events already support step 4 and `candidate_added`.

The existing `/root/mathlab_build_review` agent gave pre-criteria **PROCEED for contingent DRAFT only** under advisor-review; Claude auth was freshly unavailable (`loggedIn=false`), so this is same-family fallback/weaker independence, not formal FREEZE. Its main correction: distinguish anchor-evidence eligibility from proposed-intervention calibration; no score-gap or diagnostic-magnitude ranking of question quality. Agent transcript carries the advice; no final draft review artifact was written. The reviewer is not doing a continuing compute/edit task.

**Next step:** a fresh successor should reverify files/live disposition, inspect the unfinished draft and its citations, finish textual review only if MAESTRO directs, and keep all future freeze/build/execution gates explicit. Do not auto-wait/launch on a timer. **Risks/traps:** fixed norm contract versus fp64 diagnostic; duplicate returned-map attribution; source/harvest mixing; stale `Next` prose; receipt/substage mistaken for completion; DuckDB mistaken for authority; InfraNodus known-result restatements (all three trial questions); calibration transferred to new families/questions; CPU-only bypassing admission; proposal PASS mistaken for behavioral evidence. `events.jsonl` + validated `fold()` remains sole run-state authority. No pending MB-owned processes; H2 step 2 belongs to MAESTRO and stays untouched.

**Context rule restated:** before approximately 20%, stop new work, record done/in-flight/exact paths/next step/risks in the report, tell MAESTRO, and hand off to a fresh successor. Every later handoff must repeat it. This handoff is the requested closeout; Codex MB stops here.
