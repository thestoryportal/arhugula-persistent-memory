---
name: betaedit-official-repo
description: "Official BetaEdit repo (lbq8942/BetaEdit, IJCAI 2026) cloned to /workspace/external_prior_art/BetaEdit — ships our-exact qwen2.5-3b config; A3 = PORT its solve, not reimplement"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 379d00c4-1e87-4399-8a95-fd542f99e336
---

**What:** official authors' BetaEdit implementation (IJCAI 2026), cloned to `/workspace/external_prior_art/BetaEdit`. Core = `BetaEdit/algs/betaedit/betaedit_main.py`. Ships `configs/llms/qwen2.5-3b.yaml` = our EXACT band[4-8] / `mlp.down_proj` / `subject_last` / wikipedia-cov setup (also qwen2.5-7b, llama3.2-3b), on the same MEMIT primitives as our engine (`compute_z`/`compute_ks`/`get_cov`/`get_module_input_output_at_words`).

**The method = our in-solve AlphaEdit + two additions:** `upd = solve(P@(K·Kᵀ + cache_c + λ1·Σ) + λ2·I,  P@K@residᵀ)` — the **`λ1·Σ` full-covariance leakage penalty** is new — PLUS a τ-periodic **history-aware P-refresh** (`ProjectionUpdater`: recompute P from `(cache_c/step + λ1·Σ)/(λ1+1)` every τ edits). A2's sentinel `K_S·K_Sᵀ` is a **low-rank shadow** of `λ1·Σ` (that's why A2 was PARTIAL); A2b ruled out K_S-*staleness* but BetaEdit refreshes **P** (a different object). See [[match-metric-to-the-claim]] (screen the A3 eval pool to confident-correct so the corruption instrument is clean across seeds).

**A3 = PORT, not reimplement:** extract the solve into our inertness-gated harness (`g6_scale_n.py` / `a2_relbal_sentinels.py` lineage). **Re-tune for our regime** — their `λ1=3000, λ2=10, τ=1000, thresh=0.02`, Qwen-*Instruct*, `mom2=15000` are tuned for gpt2-xl @ 10k edits; `τ=1000` never fires at N=100; we're base-model `5000 / 0.005`. Copy the math, derive λ1/τ. **LAW#5 gate:** BetaEdit at `λ1=0, τ>N, λ2=L2` ≡ our AlphaEdit bit-exactly (advisor-verified vs `betaedit_main.py:265-270`). Pass criterion on the clean metric vs an in-script AlphaEdit baseline.

**Caveats:** NO LICENSE file (all-rights-reserved → port the METHOD into our own code, cite the paper, don't redistribute their code); the runbook's "arXiv 2605.09285" was fabricated (repo cites only IJCAI 2026) → [[verify-external-artifacts-before-effort]]. **Scope:** A1 already shows batch/Genesis eliminates this corruption — A3 only matters for incremental online single-fact writes (operator chose to proceed with A3). Writeup: `CORPUS/16`.
