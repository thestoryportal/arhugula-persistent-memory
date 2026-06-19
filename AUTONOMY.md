# AUTONOMY — bounded, no-HIL overnight run contract

The autonomy harness lets the repo make **falsification-first** progress unattended, with hard
guardrails so it cannot run wild or corrupt the canonical record. It is **opt-in and
operator-launched** — nothing here runs on its own.

## North Star (never drifts)
**F1 — prove or falsify that the LLM-as-Database spec is implementable, and deliver the
readiness determination.** A clean **FAIL** on a pre-registered falsifier is a SUCCESS for the
run. Optimizer-style "make the number go up" is NOT the goal (see *Fenced units*).

## What it is (thin by design)
`tools/autonomy_driver.py` is a deterministic guardrail loop:

1. **Hard wall-clock stop** — `--budget-min` is a real deadline; the run cannot exceed it.
2. **Preflight hard-gate** — `tools/codex_context_guard.py preflight`; if the pod is NOT-READY
   (engine missing, etc.) it **aborts before any experiment**.
3. **Per-unit loop bound + timeout** — `max_loops` and `timeout_s` per unit; a retry only helps a
   *transient* failure (the driver never loops to chase a different label on a deterministic run).
4. **Deterministic labeling** — PASS / PARTIAL / FAIL / INVALID computed from a **pre-registered
   rule** on the unit's result JSON. No model judgment. (`FAIL` = tested, criteria not met = a
   real negative result. `INVALID` = couldn't evaluate / guard failed = confounded, not a result.)
5. **Gate log** — every model-pull / cov-compute is logged as PRE-APPROVED (standing-auth);
   paid-provider + credential moves are GATED → logged to `logs/autonomy_gates.jsonl` and skipped.
6. **Closeout to STAGING** — findings go to `logs/pending_findings/NN_<unit>.md`. The driver
   **NEVER** writes `CORPUS/*`, the append-only ledger, the runbook, or the checkpoint. **You**
   fold staged findings into the canonical §0.4 record on review.

## What it is NOT
It is **not a scientist**. The agentic discipline — deep-thinking-on-failure, autoresearch,
independent advisor-review — is emitted as an **obligation block** in each staging file for the
review pass (or fulfilled by a model in `--mode agent`). Python does not fake reasoning.
**Self-review by the run model is not independent** — a real review pass uses a *different* model
(`codex exec -m <other>`); otherwise it is a self-consistency check and must not raise confidence.

## The mission (`tools/autonomy_mission.json`)
One **named, pre-registered falsifier** pulled from runbook §0.3:

- **`c2band_falsifier`** — Does editing in the minimum-collinearity band **[8-12]** (C2/`CORPUS/20`)
  reduce cross-entity read corruption vs the default band **[4-8]**, at fixed N=100, **sequential**
  write? (Sequential, not batch: A1/batch already drives corruption to ceiling — `unt_cross_loc`≈98.5%,
  no headroom; sequential baseline ≈54.8% is where C2's mechanism can actually move the metric.)
  Metric: `unt_cross_loc` (paired post-vs-pre JS locality; higher = less corruption), guarded by
  edit-success ≥95 on both arms. **PASS** ≥5pp reduction · **PARTIAL** >1pp · **FAIL** ≤1pp
  (C2 lead falsified for editing) · **INVALID** if a guard fails. Thresholds are fixed before the
  run; adjusting them after seeing results voids pre-registration.
  - Runner: `experiments/track_c/band_corruption_compare.py` (runs `g6_scale_n_param.py` twice).
  - **Cov note:** band [8-12] needs covariance for L9-12 (not cached) — the first run computes them
    (standing-auth: PRE-APPROVED, cov-compute-heavy; hence `timeout_s` is large).

## Launch (operator)
```bash
export LLMDB_ROOT=/workspace
cd /workspace
# Recommended: run detached so an SSH drop doesn't kill it (memory: runpod-durable-experiment-launch)
setsid python -u tools/autonomy_driver.py \
    --mission tools/autonomy_mission.json --budget-min 240 \
    > logs/autonomy_console.log 2>&1 &
# Watch:  tail -f logs/autonomy_console.log
```
On wake: read `logs/autonomy_run_*.md` (summary), the staged `logs/pending_findings/*.md`
(per-unit findings + obligation blocks), and `logs/autonomy_gates.jsonl` (what was gated).

### Dry-run first (no GPU, proves guardrails)
```bash
python tools/autonomy_driver.py --mission tools/autonomy_mission.json --dry-run
```

### Agent mode (full discipline, needs Codex authenticated)
`--mode agent --model <codex-model>` shells `codex exec` per unit so a model fulfils the
deep-thinking / autoresearch / advisor obligations within the wall-clock + loop bounds. Requires
Codex auth (operator-gated). Default is `--mode batch` (runs the unit command directly).

## Fenced units (optimizer — opt-in, NOT in the default mission)
A unit with `"fenced": true` is hyperparameter-optimization (Goodhart-prone: maximizing held-out
accuracy is the *opposite* of falsification). The band-search optimizer lives at
`experiments/track_c/autoresearch_band_search/`. If added to the mission it may **log candidates
only** — a fenced PASS means "candidate worth a pre-registered falsifier", **never a conclusion**.
Keep the default overnight mission pointed at the falsifier.

## Review → canonical (next morning, supervised)
For any staged finding worth keeping, run the full §0.4 close-out yourself: verify the exact
command + numbers reproduce → deep-thinking-on-failure if not PASS → independent (cross-model)
advisor-review → then CORPUS/NN + `00`/`03` + runbook §0.3/§12/§13 + checkpoint + memory.
See `DISCIPLINE.md` §0.4 and §2.
