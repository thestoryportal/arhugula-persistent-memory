---
name: repo-reorganized-llmdb-root
description: 2026-06-18 the /workspace repo was reorganized from flat-root scatter into a clean tree; scripts now use LLMDB_ROOT (default /workspace); files are NOT at root anymore
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4fe3a83d-4803-44dd-9256-cb8cb1a6a3db
---

On 2026-06-18 the scattered `/workspace` repo (~370 loose root files) was reorganized to publication grade. **Files are no longer at the flat root** — look in the new tree:
- **`experiments/<track>/`** — live scripts: `governance/` (cp1-g3), `scale/` (g6_*), `track_a/` (a0-a7), `track_b/` (b1/b3), `track_c/` (c2*), `deployment/` (e1, larql_*), `infra_scripts/`.
- **`configs/`** — `hparams/` (qwen25_3b/7b, qwen3_06b, llama32_3b memit hparams + yaml), `screens/` (g6_screen_*), `probes/` (b3_probes.json).
- **`results/`** (all `*_result.json`, ledgers, b3_pred_*), **`logs/`** (all `*.log`/`.flag`), **`docs/`** (framework_findings/, session_summaries/, runbooks/, HYPOTHESIS_REGISTER, design notes), **`archive/`** (frozen s-series scripts, notebooks, stale subdirs).

**Path convention:** live scripts begin `LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")` and reference `f"{LLMDB_ROOT}/configs/..."`, `f"{LLMDB_ROOT}/results/..."`. `.sh` use `$LLMDB_ROOT`. To re-run from elsewhere set `LLMDB_ROOT`.

**STAYED at root (unmoved, referenced via LLMDB_ROOT default):** the canonical docs (CLAUDE.md, EXPERIMENT_RUNBOOK.md, SESSION_CHECKPOINT.md, SESSION_BOOTSTRAP.md, EVIDENCE_INDEX.md, CORPUS/, research_and_specs/, memory_mirror/), all infra (`hf_cache/`, `memit_dry_run/`, `external_prior_art/`, `covariance_caches/`, `llama_cpp_src/`, model artifacts, `*.gguf`, `b3_q4km.vindex/`), and `stage_1_sect/` + `architecture_profile/` + `reproducibility_manifest.json` (kept for evidence provenance, cited 130+×).

**Entry points for a fresh researcher:** `README.md` → `REPRODUCIBILITY.md` → `docs/EXPERIMENT_REGISTRY.md` (maps every experiment ID → script/config/result/log/CORPUS doc/status). CORPUS docs cite artifacts by basename (resolve via the registry or `find`). Frozen s-series scripts in `archive/` were NOT path-rewritten (they target the old flat layout). Pre-reorg snapshot + rollback at `/root/migration_backup/` (manifest, hashes, tar, migration_map.tsv). See [[experiment-runbook-is-canonical]], [[durable-artifact-path-collision]].
