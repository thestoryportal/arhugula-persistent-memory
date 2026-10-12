# C10J AnyEdit Reset - Stage 0 Diagnostic

**Decision-ID:** `D-C10j-anyedit-reset`
**Date:** 2026-06-27
**Status:** `HALTED` for local runner construction from the reused C10h path
pending a route decision or separate upstream-environment addendum.
**Prereg:** `docs/C10J_ANYEDIT_RESET_PREREG.md`

## Purpose

This document records the Stage-0 checks required before authoring any new
C10J AnyEdit runner. It is not a CORPUS finding and is not promoted evidence for
or against the LLM-as-Database spec.

## EVIDENCE-SHOWS

### 1. Preregistration and advisor gate passed for Stage 0 only

- Mechanical prereg gate passed:
  `python3 tools/experiment_gate.py check-prereg docs/C10J_ANYEDIT_RESET_PREREG.md`
- First Claude advisor pass returned `FIX-FIRST`:
  `logs/claude_c10j_anyedit_reset_prereg_review.md`
- Revised prereg advisor pass returned `PROCEED` for Stage-0 actions only:
  `logs/claude_c10j_anyedit_reset_prereg_review_v2.md`

### 2. Upstream source was located, but direct smoke is not runnable in the current environment

Artifact: `logs/c10j_anyedit_upstream_feasibility.log`

- Repository: `https://github.com/jianghoucheng/AnyEdit.git`
- Commit: `057a77f185f7ffb55818f6bd9add37f43bb447e7`
- Current environment:
  - Python `3.11.10`
  - torch `2.4.1+cu124`
  - transformers `4.51.0`
- Upstream hparams inventory contains Qwen2.5-7B and Llama3-8B configs, not a
  Qwen2.5-3B config.
- `python3 -m experiments.evaluate_uns --help` failed before CLI display with:
  `ModuleNotFoundError: No module named 'nltk'`.

This is a feasibility diagnostic only. It does not test AnyEdit behavior.

### 3. Cheapest default-window local control probe failed

Artifact: `results/c10j_anyedit_window50_controls.json`
Log: `logs/c10j_anyedit_window50_controls.log`

The result path is C10J-namespaced, and `find results -maxdepth 1` shows a
separate existing `results/c10h_anyedit_window50_controls.json`; this Stage-0
run wrote `results/c10j_anyedit_window50_controls.json` and did not reuse the
canonical C10h output path.

Declared provenance deviation: the reused harness still stamps the internal
`decision_id` as `D-C10h-anyedit-window50-controls` and the log says C10h. This
is another reason to treat the artifact as diagnostic-only.

Declared method boundary: this run did **not** execute the official upstream
AnyEdit experiment runner. It used the repo-local `experiments/track_c/c10h_anyedit_pilot.py`
harness, which implements local ARE-style multi-token target construction and a
layer update path on top of the local MEMIT hparams/engine primitives. Therefore
the manipulated condition was the local C10h AnyEdit/ARE transplant at
`window_size=50`, not a source-faithful upstream AnyEdit run.

Frozen control gate:

```text
CONTROL_RECOVERY_PASS iff A1_single and A2_coherent2 held-out para_full >= 80
under AnyEdit window_size=50
```

Saved verdict:

```json
{
  "label": "CONTROL_RECOVERY_FAIL",
  "baseline_controls": {
    "A1_single_para_full": 97.2,
    "A2_coherent2_para_full": 94.4
  },
  "anyedit_window50_controls": {
    "A1_single_para_full": 0.0,
    "A2_coherent2_para_full": 0.0,
    "control_min_para_full": 0.0
  },
  "licensed_claim": "stops A7 under this local upstream-window transplant condition"
}
```

Arm summary:

| Arm | Recipe | Canon full | Held-out `para_full` | Locality |
|---|---:|---:|---:|---:|
| A1 | local MEMIT reference | 100.0 | 97.2 | 89.66 |
| A2 | local MEMIT reference | 100.0 | 94.4 | 93.85 |
| A1 | AnyEdit window=50 diagnostic | 25.0 | 0.0 | 99.88 |
| A2 | AnyEdit window=50 diagnostic | 8.3 | 0.0 | 99.88 |

Failure signature: near-perfect locality (`99.88`) with weak canonical fit
(`25.0` / `8.3`) and zero held-out behavior (`para_full=0.0` / `0.0`). This is
consistent with an edit that barely applied under the local integration path,
not evidence that official upstream AnyEdit is ineffective.

LAW#5 inertness passed in the reused harness:

```text
|Δexpr|=0.0001 |Δloc|=0.58 -> INERT
```

### 4. Experiment-gate refused stats

Artifact: `logs/experiment_gate/c10j_anyedit_window50_controls_stats.json`

`python3 tools/experiment_gate.py check-result results/c10j_anyedit_window50_controls.json`
returned `BLOCKED` because the JSON is aggregate-only and lacks per-unit arrays.
The refusal is correct and blocks any completion, promotion, or CORPUS claim.
The catastrophic aggregate failure is still sufficient to stop escalation under
the preregistered easy-control licensing rule.

## I-INFER

The default-window local C10h AnyEdit/ARE transplant did not recover A1/A2
behavior. Therefore, under the C10J prereg, a hard A7 run is not licensed and a
new local C10J active-parity runner should not be authored from this failed
path.

The observed failure does not prove official AnyEdit is ineffective. It only
shows that this local upstream-window transplant path failed the preregistered
easy-control licensing gate in the current Qwen2.5-3B / transformers 4.51.0
environment.

Because AnyEdit is optional for F1 unless the spec is amended, the official
upstream-environment route is a costed choice, not the default next step. The
bounded-hybrid / side-store route remains the already-supported F1 route for
project-coined multi-word semantic values unless the operator explicitly wants
to spend on general in-weight multi-token storage.

## Decision

- `A7_LICENSED_FOR_ADDENDUM`: **NO**
- New local C10J runner construction from the reused C10h path: **HALT**
- CORPUS promotion: **NO**
- Next valid routes:
  1. build a separate official-upstream environment attempt matching upstream
     dependencies/model envelope as closely as feasible, with its own addendum;
  2. test another method family under the same easy-control licensing discipline;
  3. return to the bounded-hybrid / side-store route for project-coined
     multi-word semantic values.

## Follow-Up Requirements

If any future AnyEdit run is attempted:

- emit per-unit records following `tools/STATS_LOGGING_CONVENTION.md`;
- use a C10J-native `decision_id` in saved JSON;
- declare upstream deviations before interpretation;
- pass active A1/A2 behavior before any hard C10 arm;
- run Claude advisor again before an A7 addendum.
