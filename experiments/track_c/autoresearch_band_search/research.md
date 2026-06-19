# Research: Band-[8–12] cross-entity isolation search (Qwen2.5-3B, sequential path)

## Goal
Find the edit **band** (which transformer layers MEMIT writes into) — and secondarily `mom2_update_weight` — that **maximizes held-out same-relation top-1 (cross-entity read isolation)** on the **sequential** editing path at N=100 on Qwen2.5-3B, beating the current band-[4-8] baseline, **without** sacrificing edit retention or expression. This operationalizes the `CORPUS/20` (C2b) finding that same-relation key collinearity is minimal at L8–12, so editing there *should* reduce the cross-entity corruption that collapses 100→41.7% on the sequential path (`CORPUS/13`).

## Success Metric
- **Metric:** `metric_value` from `evaluate.py` = held-out edited-relation **EXACT** top-1 % (exact match, not the lenient prefix-match `correct()` — the NEW-3 confound).
- **Target:** > the measured [4-8] baseline; stretch goal → approach the batch path's clean level (`CORPUS/14`).
- **Direction:** maximize

## Constraints
- **Max iterations:** 12  _(each new band triggers a one-time covariance computation — expensive; spend the budget deliberately)_
- **Evaluator:** `python evaluate.py`  _(prints JSON to stdout)_
- **Keep policy:** score_improvement
- **Guard (MUST stay true — else the experiment is INVALID and is reverted regardless of metric):** `evaluate.py` reports `"valid": true`, i.e. **retention ≥ 95% AND apply-time expression ≥ 95%**. This blocks the obvious cheat (a band that "looks isolated" only because the edits never took).
- **Noise runs:** 1  _(single seed — a known confound; see the verification rule below)_
- **Min delta:** 1.0  (percentage points)

## Current Approach (baseline)
Band **[4-8]** (the program's default). Sequential cross-entity collapses **100 → 41.7%** with N (`CORPUS/13`, `CORPUS/20`); the **batch** path eliminates it at 3B (`CORPUS/14`) but the **sequential/incremental** path is unsolved (A3 parked). C2b depth map: same-relation subject-key collinearity is min at **L8-12 (cos 0.20-0.42)**, max in late layers — hence the [8-12] hypothesis. **[4-8] covariance is cached** (use it to validate `evaluate.py` reproduces the baseline); **[8-12] is not** (computed on first eval).

## Search Space
- **Allowed changes:** `config.json` only — `layers` (any subset of 2..32) and `mom2_update_weight`. Start at `[8,9,10,11,12]`; explore neighbouring bands ([8-11], [9-12], [8-12]+thresh, mid-vs-mid-late).
- **Forbidden changes:** `run_edit.py`, `evaluate.py`, the screen file (`configs/screens/g6_screen_qwen3b.json`), the held-out entity set, the EXACT-match metric, the engine (`memit_dry_run/memit`), and the guard thresholds. **Do not weaken the metric or the guard to make a band "win".**

## Context & References
`CORPUS/20` (C2b depth map) · `CORPUS/13` (G6.1 sequential collapse) · `CORPUS/14` (A1 batch-clean) · `docs/HYPOTHESIS_REGISTER_2026-06-18.md` C2/D2. The engine inertness gate (LAW#5) runs inside `run_edit.py` each iteration.

---

## ⚠️ CRITICAL — this loop OPTIMIZES; our program FALSIFIES (read before trusting any winner)
This autoresearch loop is an **optimizer** (hill-climb a metric, keep-if-better) — the **opposite** of this program's falsification-first discipline. **Its output is hypothesis-generation, NOT evidence.** A winning band is a **candidate**, never a result. Before any winner is believed or written down:
1. **Re-run with PRE-REGISTERED pass criteria** set *before* the confirmation run (not the loop's moving target).
2. Confirm the **engine inertness gate** passed (already in `run_edit.py`).
3. **Multiple seeds** — this loop is single-seed, a confound.
4. **`advisor()` review** of the candidate and its metric.
5. Verify it isn't **gaming the guard** (e.g. barely clearing 95% retention while the metric balloons).

**Goodhart's law applies:** the loop *will* find configs that game the metric. The EXACT-match metric + retention/expression guard + frozen held-out set are defenses, not guarantees. **NEVER write a loop winner into `CORPUS/` as a finding** — only into the hypothesis register as a lead for a proper, pre-registered experiment (a band-[8-12] confirmation run). The loop *proposes*; the program's discipline *disposes*.

## History
<!-- Auto-maintained by the agent. Do not edit manually. -->
| # | Change | Metric (exact %) | Valid | Result | Timestamp |
|---|--------|------------------|-------|--------|-----------|
| 0 | Baseline band [4-8] | TBD (run to establish) | TBD | -- | -- |
