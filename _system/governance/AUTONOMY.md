# AUTONOMY — bounded, no-HIL overnight run contract

The autonomy harness lets the repo make **falsification-first** progress unattended, with hard
guardrails so it cannot run wild or corrupt the canonical record. It is **opt-in and
operator-launched** — nothing here runs on its own.

## North Star (never drifts)
**F1 — prove or falsify that the LLM-as-Database spec is implementable, and deliver the
readiness determination.** A clean **FAIL** on a pre-registered falsifier is a SUCCESS for the
run. Optimizer-style "make the number go up" is NOT the goal (see *Fenced units*).

## What it is (thin by design)
`code/lab/runners/autonomy_driver.py` is a deterministic guardrail loop:

1. **Hard wall-clock stop** — `--budget-min` is a real deadline; the run cannot exceed it.
2. **Preflight hard-gate** — `code/agents/codex_context_guard.py preflight`; if the pod is NOT-READY
   (engine missing, etc.) it **aborts before any experiment**.
3. **Per-unit loop bound + timeout** — `max_loops` and `timeout_s` per unit; a retry only helps a
   *transient* failure (the driver never loops to chase a different label on a deterministic run).
4. **Deterministic labeling** — PASS / PARTIAL / FAIL / INVALID computed from a **pre-registered
   rule** on the unit's result JSON. No model judgment. (`FAIL` = tested, criteria not met = a
   real negative result. `INVALID` = couldn't evaluate / guard failed = confounded, not a result.)
5. **Gate log** — every model-pull / cov-compute is logged as PRE-APPROVED (standing-auth);
   paid-provider + credential moves are GATED → logged to `logs/autonomy_gates.jsonl` and skipped.
6. **Closeout to STAGING** — findings go to `experiments/ml/reviews/pending_findings/NN_<unit>.md`. The driver
   **NEVER** writes `evidence/CORPUS/*`, the append-only ledger, the runbook, or the checkpoint. At the supervised fold-in, the close-out is gated by `python3 code/gates/closeout_check.py <D-ID>` (must be ✅ ALL GREEN — DISCIPLINE §1.1). **You**
   fold staged findings into the canonical §0.4 record on review.

## What it is NOT
It is **not a scientist**. The agentic discipline — deep-thinking-on-failure and
independent advisor-review — is emitted as an **obligation block** in each staging file for the
review pass (or fulfilled by a model in `--mode agent`). Python does not fake reasoning.
**Self-review by the run model is not independent** — a real review pass uses a *different* model
(`codex exec -m <other>`); otherwise it is a self-consistency check and must not raise confidence.

## The mission (`code/lab/runners/autonomy_mission.json`)
One **named, pre-registered falsifier** pulled from runbook §0.3.

> **⚠ STALE (2026-06-21): the bundled `c2band_falsifier` mission is DONE** — folded in as `D-C2band-1` (`evidence/CORPUS/21`, mechanical PASS-not-promoted). **Re-point `code/lab/runners/autonomy_mission.json` to a current §0.3 falsifier before any launch.** The strongest current candidate is the **compaction-at-scale cleanliness** falsifier (hypothesis **D20**, B3N condition 3: does the batch/compaction path stay clean at **N≥2,000**, where MEMIT sub-batching engages?) — but it **needs a runner + pre-registered rule authored first** (no runner exists yet). Until a fresh mission + runner are pre-registered, the loop has nothing valid to run. The description below is retained as the **worked example** of a well-formed mission.

- **`c2band_falsifier`** *(DONE — example only)* — Does editing in the minimum-collinearity band **[8-12]** (C2/`evidence/CORPUS/20`)
  reduce cross-entity read corruption vs the default band **[4-8]**, at fixed N=100, **sequential**
  write? (Sequential, not batch: A1/batch already drives corruption to ceiling — `unt_cross_loc`≈98.5%,
  no headroom; sequential baseline ≈54.8% is where C2's mechanism can actually move the metric.)
  Metric: `unt_cross_loc` (paired post-vs-pre JS locality; higher = less corruption), guarded by
  edit-success ≥95 on both arms. **PASS** ≥5pp reduction · **PARTIAL** >1pp · **FAIL** ≤1pp
  (C2 lead falsified for editing) · **INVALID** if a guard fails. Thresholds are fixed before the
  run; adjusting them after seeing results voids pre-registration.
  - Runner: `code/lab/track_c/band_corruption_compare.py` (runs `g6_scale_n_param.py` twice).
  - **Cov note:** band [8-12] needs covariance for L9-12 (not cached) — the first run computes them
    (standing-auth: PRE-APPROVED, cov-compute-heavy; hence `timeout_s` is large).

## Launch (operator)
```bash
cd <repo root>   # in a worktree: the worktree root
export LLMDB_ROOT=$PWD
# Recommended: run detached so closing the terminal doesn't kill it (macOS has no setsid)
nohup .venv/bin/python -u code/lab/runners/autonomy_driver.py \
    --mission code/lab/runners/autonomy_mission.json --budget-min 240 \
    > logs/autonomy_console.log 2>&1 &
# Watch:  tail -f logs/autonomy_console.log
```
On wake: read `logs/autonomy_run_*.md` (summary), the staged `experiments/ml/reviews/pending_findings/*.md`
(per-unit findings + obligation blocks), and `logs/autonomy_gates.jsonl` (what was gated).

### Dry-run first (no GPU, proves guardrails)
```bash
python code/lab/runners/autonomy_driver.py --mission code/lab/runners/autonomy_mission.json --dry-run
```

### Agent mode (full discipline, needs Claude subscription auth)
`--mode agent` attempts an independent cross-family review of each reviewable staged finding
when more than 45 s of the wall-clock budget remain. A skipped review (45 s or less left) or an
`UNAVAILABLE` review (advisor missing, timed out, or failed) leaves the independent-review
obligation open.
The default advisor is Claude via `code/agents/claude_advisor.sh` (`--advisor claude`;
claude.ai subscription auth). `--advisor codex --model <codex-model>` shells `codex exec` as
the fallback and needs Codex auth (operator-gated). Default is `--mode batch` (runs the unit
command directly).

## Fenced units (optimizer — opt-in, NOT in the default mission)
A unit with `"fenced": true` is optimizer-style search (Goodhart-prone: maximizing held-out
accuracy is the *opposite* of falsification). If added to the mission it may **log candidates
only** — a fenced PASS means "candidate worth a pre-registered falsifier", **never a conclusion**.
Keep the default overnight mission pointed at the falsifier.

### Autoresearch is not run by this driver
Karpathy's `autoresearch` loop runs as its own operator-launched Claude Code session, exactly as the
macOS fork directs: `bash code/lab/track_c/autoresearch_c10/launch.sh`. How we use it, its fence
and its deviations: `experiments/c10r/design/AUTORESEARCH.md` (D-C10r-rulings-1, D-C10r-impl-1). The vendored
`tools/autoresearch-skill/` loop this section used to describe was never present in this checkout
and is retired, as is `code/lab/track_c/autoresearch_band_search/`. The fence is unchanged: a
loop "win" is a lead for the hypothesis register, never `evidence/CORPUS/`.

## Review → canonical (next morning, supervised)
For any staged finding worth keeping, run the full §0.4 close-out yourself: verify the exact
command + numbers reproduce → deep-thinking-on-failure if not PASS → independent (cross-model)
advisor-review → then evidence/CORPUS/NN + `00`/`03` + runbook §0.3/§12/§13 + checkpoint + memory.
See `_system/governance/DISCIPLINE.md` §0.4 and §2.

---

# Rules moved from the pre-v2 `CLAUDE.md` and `AGENTS.md`
Moved verbatim by lane 5a. The root `CLAUDE.md` now only routes here.

## Appendix — the `autonomy_driver.py` unattended harness (opt-in, operator-launched only; distinct from standing delegation)

The repo can make bounded falsification-first progress **unattended**, but **nothing runs on its own** — it is **opt-in and operator-launched**. The real harness is **`code/lab/runners/autonomy_driver.py`**, fully specified in **`_system/governance/AUTONOMY.md`** (hard wall-clock stop, preflight gate, deterministic pre-registered labeling, STAGING-only output — it never writes `evidence/CORPUS/`/ledger/runbook/checkpoint; the operator folds staged findings in through the §0.4 close-out gate). The mission is one pre-registered falsifier from §0.3 (`code/lab/runners/autonomy_mission.json` — **re-point it to a current §0.3 falsifier before launch; the bundled `c2band_falsifier` is STALE/DONE (D-C2band-1)**). When this regime runs, the LAWs + halt + close-out gate in `_system/governance/DISCIPLINE.md` still apply unchanged. The "terse / no-relay / make-all-calls-yourself / kickoff+summary_block" defaults belong to this regime only — in interactive mode, legible reasoning + HIL gates replace them.

## Autonomous (no-HIL) runs — `_system/governance/AUTONOMY.md` + `code/lab/runners/autonomy_driver.py`
For bounded unattended overnight progress. **Opt-in, operator-launched** — nothing runs on its own. This harness is separate from MAESTRO's standing delegation, under which the orchestrated team keeps working within authorized scope.
- **Driver** = thin deterministic guardrails: hard wall-clock (`--budget-min`), **preflight hard-gate**, per-unit `max_loops`/`timeout_s`, **pre-registered deterministic PASS/PARTIAL/FAIL/INVALID** from the result JSON (no model judgment), gate-log (`logs/autonomy_gates.jsonl`), and **closeout to STAGING** (`experiments/ml/reviews/pending_findings/NN_<unit>.md`). **At supervised fold-in (when a staged finding is promoted to evidence/CORPUS/ledger/runbook), the close-out is NOT done until `python3 code/gates/closeout_check.py <D-ID>` is ✅ ALL GREEN** (binding gate, DISCIPLINE §1.1 — mechanical, not operator-verified).
- **The driver NEVER writes `evidence/CORPUS/*`, the ledger, the runbook, or the checkpoint.** Unattended findings are staged; the operator folds them into the canonical §0.4 record on supervised review. The `.codex/hooks/` (pre_tool_use_policy / stop_gate) are intended to enforce this; runtime enforcement is UNVERIFIED until current paths and invocation are qualified. STAGING-only remains mandatory regardless of hook availability.
- **Mission** (`code/lab/runners/autonomy_mission.json`) points at **one named pre-registered FALSIFIER** from §0.3. The bundled mission (`c2band_falsifier`) is **STALE** — that falsifier is done (D-C2band-1); re-point it to a live §0.3 falsifier before any launch. Optimizer/sweep units must be `fenced:true` (candidate-log only, never a conclusion) — see DISCIPLINE §3.1.
- **`--mode agent`** appends an advisory independent review per reviewable staged finding. Default backend is Claude via `code/agents/claude_advisor.sh` for Codex-led work (`--advisor claude`; claude.ai Max subscription auth, no API key); `--advisor codex` remains fallback/secondary. Default `--mode batch` runs the unit command directly.
- Launch + review instructions: `_system/governance/AUTONOMY.md`. Bounds & rationale: `_system/governance/DISCIPLINE.md` §3.1.
