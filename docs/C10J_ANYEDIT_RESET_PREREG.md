# C10J AnyEdit Reset - Preregistration

**Decision-ID:** `D-C10j-anyedit-reset`
**Date:** 2026-06-27
**Class:** method-port faithfulness / C10 reset gate; can-fail; not promotable.
**Decision gate:** `docs/C10_ANYEDIT_RESET_DECISION_GATE.md`
**E2e-map cell:** Section 8 write engine and Section 8.9 L2 behavioral firing for Layer-4 `domain_concept`; fixed deployment target = `local Intel CPU + batch writes`.
**Scope:** Qwen2.5-3B / HF-fp16 / local `transformers==4.51.0` / official `jianghoucheng/AnyEdit` source-faithfulness check / novel-insert A1-A2 easy controls only / no hard A7 licensed in this prereg.

## Hypothesis

A fresh, source-faithful AnyEdit reset can only become C10 evidence if it first
recovers active A1/A2 easy-control behavior under a documented upstream-equivalent
method-port packet. Token alignment, no-op inertness, and canonical fit are
necessary but not sufficient.

This prereg tests the falsifiable claim:

> The AnyEdit reset harness can produce a source-faithful active A1/A2 edit trace
> and recover held-out full-sequence behavior on A1/A2 without damaging locality.

This advances C10 by deciding whether an A7 hard-case pilot is licensed. It does
not test A7 and cannot rescue or falsify C10 by itself.

## F1 Decision Meaning

- **If PASS:** AnyEdit becomes licensed for a separate A7 prereg addendum. F1 is
  unchanged until A7 is tested.
- **If FAIL/HALTED:** this local reset does not currently justify hard-case spend.
  F1 remains compatible with the bounded-hybrid route: project-coined multi-word
  semantic values route through Git / `.vindex` / index / side-store rather than
  relying on direct in-weight serving.
- **If INVALID:** no science update; diagnose the method port only.

## Bias Boundary

Prior C10h results are used only as known failure modes:

- local transplant control collapse is possible;
- no-op and token gates are not active edit parity;
- hard A7 must not run before A1/A2 recover.

Prior C10h numbers do not set success thresholds, implementation choices, or
interpretation. Thresholds below are chosen from the easy-control licensing rule
in the reset decision gate and experiment-gate method-port checklist.

## Stage Covered By This Prereg

This prereg covers **Stage 0 and Stage 1 only**:

0. verify the external repo before effort: confirm `jianghoucheng/AnyEdit` is
   reachable, record commit, and confirm the path is the LLM AnyEdit path, not
   an image-editing name collision;
1. run the cheapest control probe before any new runner: A1/A2 only with the
   existing C10h harness under upstream/default `window_size=50`, namespaced to
   `c10j`, to test whether the documented control collapse is just the
   small-window setting;
2. attempt a direct upstream A1/A2 smoke/feasibility anchor in a throwaway
   environment, or write a diagnostic explaining the precise dependency/model
   incompatibility that prevents it;
3. only after 0-2, construct or wrap an A1/A2-only active parity runner;
4. emit a method-port packet;
5. run A1/A2 controls;
6. audit the packet with `tools/experiment_gate.py audit-method-port`;
7. run Claude advisor before any A7 addendum.

No A7, A6, coined-coined, or other hard C10 arm is licensed by this prereg.

## Binding Metric

Primary binding metric: A1 and A2 held-out paraphrase full-sequence exact match
(`para_full`) after the AnyEdit reset edit.

Passing threshold:

- `A1.para_full >= 80%`
- `A2.para_full >= 80%`

Full-sequence exact match is the read-correctness metric. Canonical prompt fit,
first-token accuracy, target probability, and delta norms are diagnostics only.

## PASS / PARTIAL / FAIL / INVALID Thresholds

- **PASS - A7_LICENSED_FOR_ADDENDUM:** all of the following hold:
  - A1 and A2 `para_full >= 80%`;
  - A1 and A2 are each within `15pp` of the same-run local MEMIT reference
    `para_full`;
  - active trace packet passes `tools/experiment_gate.py audit-method-port`;
  - locality is not materially worse than the same-run local MEMIT reference;
  - LAW#5 / no-op inertness passes;
  - all upstream deviations are declared before interpretation;
  - Claude advisor returns `PROCEED` or `FIX-FIRST` items are resolved before A7.
- **PARTIAL - PORT_ACTIVE_BUT_NOT_LICENSED:** active trace is nonzero and
  source-faithful enough to diagnose, but A1 or A2 misses `80%`, locality is
  materially worse, or advisor returns unresolved `FIX-FIRST`.
- **FAIL - EASY_CONTROLS_NOT_RECOVERED:** A1/A2 behavior stays below threshold
  after one localized fix, or the source-faithful implementation cannot produce
  viable easy-control behavior.
- **INVALID/HALTED:** missing saved JSON, missing method-port packet, engine
  primitive edits, failed token-alignment/inertness gate, aggregate-only result,
  undeclared upstream deviation, or any hard A7 run attempted before PASS.

## Power / MDE

This is a licensing/engineering gate, not a promotion-quality reliability claim.
The planned sample is the existing A1/A2 easy-control suite with held-out
paraphrases. These controls must be recorded as **novel inserts** rather than
counterfactual updates over pretrained priors. If any easy-control item is an
update over a known prior, or if either A1/A2 result lands in `[80%, 90%)`, rerun
that easy-control gate once under the same prereg before licensing A7.

A single seed/order can support a scoped diagnostic pass/fail for hard-case
licensing, not a broad AnyEdit reliability claim.

No power calculation is binding for Stage 1 because the criterion is a high
absolute easy-control floor (`>=80%`) plus trace faithfulness, not an estimated
small effect. If Stage 1 passes and an A7 addendum is drafted, that addendum must
run `tools/power.py` or explicitly justify why only a scoped pilot is being run.

## Confounders And Controls

| Confounder | How it fakes a result | Control |
|---|---|---|
| Method-port drift | Local hybrid is mistaken for upstream AnyEdit behavior | Required method-port packet: upstream commit, hparams, deviations, active trace, controls, thresholds |
| Token/no-op false parity | Alignment and inertness pass while active update is wrong | Active A1/A2 trace with target norms, delta/update norms, logit deltas, and behavior |
| Canonical-only fit | Trained prompt improves while held-out read fails | Binding metric is held-out `para_full`; canonical fit diagnostic only |
| Under-editing vs locality | Weak edit looks safe because nothing changed | Require behavior floor plus nonzero finite update/delta norms |
| Over-editing/control collapse | Hard-case gain would be bought by destroying easy controls | A7 not licensed unless A1/A2 pass first |
| Undeclared hparam/module mismatch | Compatibility patch changes method semantics | Deviations declared before run; one localized fix maximum |
| Denominator/survivorship | Failed controls disappear from metrics | Report attempted, edited, evaluated, and retained denominators |
| Context reliance | Prefix/canonical context carries answer | Not in Stage 1 claim; if logged, diagnostic only |
| Window-size false cause | A1/A2 collapse is caused by `window_size=1`, not method-port drift | Stage-0 A1/A2-only default-window probe under `window_size=50` before new runner |

Any open preregistered confound caps the result at PARTIAL or INVALID.

## LAW / Inertness Gates

- Do not edit `memit_dry_run/memit` science-path primitives.
- Do not downgrade pinned dependencies.
- Run the standard engine/source fingerprint checks used by the local MEMIT
  harness before any evidence-bearing run.
- Run AnyEdit no-op/identity inertness before interpreting A1/A2 behavior.
- Inertness pass requires finite reported layer deltas and:
  - `abs(delta_expr) <= 0.01`;
  - `abs(delta_loc) <= 3.0` on the pinned C10 locality score scale;
  - no parameter tensor changes in a pure no-op pipeline path.
- If the failing boundary is unclear, use debug-mantra: reproduce, trace,
  hypothesize, one fix, rerun same gate, halt.

One-fix boundary: one localized harness-side compatibility fix is allowed after
the first active A1/A2 failure. A second distinct fix requires a prereg addendum
and Claude advisor review.

## Method-Port Faithfulness

Required upstream record:

- upstream repository: `jianghoucheng/AnyEdit`;
- upstream commit: to be recorded from the checked-out source before run;
- upstream method: `AlphaEdit_ARE` / AnyEdit autoregressive target construction;
- upstream hparams: model, layers, window size, overlap, nullspace threshold,
  L2/clamp/cov settings, target module names, and any Qwen-specific hparams.

Required declared deviations:

- local model is Qwen2.5-3B under `transformers==4.51.0`;
- local hparam/module names may differ from upstream Qwen configs;
- local run must preserve local MEMIT/AlphaEdit primitives and LAW#5;
- any use of `model.embed_tokens` or other target-module compatibility override
  must be declared and justified before interpretation;
- any deviation from upstream `window_size` is not licensed in Stage 1 unless
  explicitly declared as an easy-control diagnostic.

Required active trace fields:

- token IDs: standalone answer IDs and `question + answer` continuation suffix IDs;
- answer/loss masks;
- lookup/edit positions;
- target hidden-state norms and target probability traces;
- per-layer delta norms;
- per-layer update norms;
- projector ranks or null-space dimensions where applicable;
- pre/post target-token logit deltas;
- canonical and held-out A1/A2 behavior;
- locality/bystander behavior.

Required behavior thresholds:

- A1 `para_full >= 80%`;
- A2 `para_full >= 80%`;
- each of A1 and A2 no more than `15pp` below the same-run local MEMIT reference
  `para_full`;
- locality no more than `5.0` points below same-run local MEMIT reference on the
  existing C10 locality score scale.

Required packet:

- `logs/c10j_anyedit_reset_method_port_packet.json`

The hard-case flag must remain:

```json
{"hard_case_licensed": false}
```

until this prereg receives PASS and a separate A7 addendum exists.

## Planned Artifacts

- Prereg: `docs/C10J_ANYEDIT_RESET_PREREG.md`
- Decision gate: `docs/C10_ANYEDIT_RESET_DECISION_GATE.md`
- Runner: `experiments/track_c/c10j_anyedit_reset_controls.py`
- Stage-0 default-window result JSON: `results/c10j_anyedit_window50_controls.json`
- Stage-0 upstream-feasibility log: `logs/c10j_anyedit_upstream_feasibility.log`
- Result JSON: `results/c10j_anyedit_reset_controls.json`
- Log: `logs/c10j_anyedit_reset_controls.log`
- Method-port packet: `logs/c10j_anyedit_reset_method_port_packet.json`
- Experiment-gate stats/audit outputs: `logs/experiment_gate/`
- Advisor output: `logs/claude_c10j_anyedit_reset_prereg_review.md`

All paths are namespaced `c10j` and must not overwrite C10h artifacts.

## Advisor / Cross-Family Review

Required review points:

1. Claude advisor review of this prereg before harness authoring.
2. Claude advisor review after any Stage 1 failure/stall that would require a
   second fix or an approach change.
3. Claude advisor review before any A7 addendum.
4. Claude advisor review before any verdict/CORPUS write if a later A7 run occurs.

Review is input, not evidence. Saved artifacts and preregistered criteria bind.

## Abort Criteria

Abort and write a diagnostic if any of the following occur:

- official AnyEdit source/commit cannot be recorded;
- source read reveals this is not the LLM AnyEdit path;
- Stage-0 default-window probe or upstream-feasibility attempt is skipped without
  a written rationale and Claude advisor acceptance;
- local harness must edit `memit_dry_run/memit`;
- no-op/inertness fails;
- active trace is missing required fields;
- A1/A2 result is aggregate-only;
- method-port packet fails audit and cannot be fixed by one localized change;
- A1/A2 controls fail after one localized fix;
- any hard A7 run is attempted before this prereg passes and an A7 addendum exists.

## Next Fork

- **PASS:** draft an A7 addendum with held-out full-sequence as binding metric,
  first-token and `P(full|first)` diagnostics, context-prefix/window-boundary
  diagnostics, locality/bystanders, power/MDE statement, Claude advisor review,
  and experiment-gate bundle requirements.
- **FAIL/HALTED:** stop the local AnyEdit reset route and choose explicitly among:
  official environment/upstream runner investment; muKE/AnyEdit++/SUIT as a new
  preregistered method lead; or bounded hybrid / side-store routing for
  project-coined multi-word semantic values.
