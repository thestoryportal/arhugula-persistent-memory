# AGENTS.md — experiments/ (live, re-runnable experiment code)

Local rules for this tree (override the root `AGENTS.md` where more specific). See root for the full guardrails.

## Tracks
`governance/` = CP1–CP3, G1–G3 (2PC, security, validation — design-viability). `scale/` = G6.1 scale-of-N + A1 batch (`g6_scale_n.py`, model-parametrized `g6_scale_n_param.py`, screeners). `track_a/` = cross-entity fixes (sentinels a2, K_S refresh a2b, bias-ablation a7). `track_b/` = scale/quant (B1 via `g6_scale_n_param.py`, B3 `b3_*`). `track_c/` = keying/mechanism (c2, c2b). `deployment/` = E1 + LARQL orchestration. `infra_scripts/` = shared helpers.

## Running
- `export LLMDB_ROOT=/workspace` first. Scripts `os.chdir` into the engine — all paths inside are absolute against `LLMDB_ROOT`, so cwd does not matter, but run from the repo root.
- Inputs: `code/configs/hparams/*.json`, `code/configs/screens/g6_screen_*.json`, `code/configs/probes/b3_probes.json`. Outputs: `results/*.json`, `logs/*.log`.
- Model-parametrized runs (`g6_scale_n_param.py`) take env `MODEL_ID`, `MODEL_REV`, `HPARAMS`, `SCREEN`, `WRITE_MODE` (`sequential|batch|batch_staircase`), and **`RESULT_TAG`** — set `RESULT_TAG` for any non-default model so you don't overwrite the canonical 3B result (`g6_scale_n_batch_result.json`).
- Long runs: launch detached (`setsid bash -c '… python -u … > logs/<n>.log 2>&1' </dev/null & disown`).

## Authoring a new experiment
1. Pre-register the metric + PASS/PARTIAL/FAIL + prediction (in the runbook §8 block and/or `experiments/g6/design/G6_G7_PASS_CRITERIA_DRAFT.md`) BEFORE coding the test. Get an independent review of the test design first (root: advisor→Codex subagent/`/review`).
2. Header: `import os, sys; LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")`; then `ENGINE_ROOT=f"{LLMDB_ROOT}/code/memit/vendor"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)`; `HF_HOME=f"{LLMDB_ROOT}/data/hf_cache"`.
3. Name `experiments/<track><n>_<slug>.py`; write results to `f"{LLMDB_ROOT}/results/<name>_result.json"`, logs to `logs/`.
4. **Run the inertness gate first** (compare your harness path vs the reference engine on a null edit; `|Δexpr|<0.05`). If not inert, HALT — do not trust the science.
5. Engine `../memit/vendor` is read-only on the science path. If you think you must patch it, that is a one-fix-then-halt decision: isolate it, prove inertness, document it.

## Do not
- Re-run or rewrite anything under `../archive/` (frozen, old flat-layout paths).
- Overwrite existing `results/*_result.json` (namespace new outputs).
- Change the `LLMDB_ROOT` convention or hardcode absolute `/workspace/...` in new scripts.
