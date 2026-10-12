# C10 ANYEDIT PILOT - PRE-REGISTRATION

**Decision-ID:** `D-C10h-anyedit-pilot` - **Date:** 2026-06-26 - **Class:** FALSIFIER-resolver / AnyEdit feasibility pilot (can-fail; NOT promotable).
**Parent:** `D-C10-1` (`CORPUS/35_C10_MULTI_TOKEN_VALUE.md`), `D-C10b-residual` (`CORPUS/36_C10_RESIDUAL_COINED_VALUES.md`), `D-C10e-bandknob` (`CORPUS/37_C10_BANDKNOB.md`), `D-C10f-band412` (`CORPUS/38_C10_BAND412.md`), `D-C10g-strengthlayers` (`CORPUS/39_C10_STRENGTH_LAYER_SWEEP.md`), and AnyEdit viability/audit docs (`docs/C10_ANYEDIT_VIABILITY_AUDIT.md`, `docs/C10_ANYEDIT_TOKEN_ALIGNMENT_GATE.md`).
**E2e-map cell:** spec Section 8 write engine / Section 8.9 L2 behavioral firing for Layer-4 `domain_concept`; fixed deployment target = `local Intel CPU + batch writes`.
**Scope:** Qwen2.5-3B / HF-fp16 / capital relation / NOVEL insert / same 24-subject C10 residual setup where possible / one seed / local `transformers==4.51.0` / harness-side AnyEdit ARE target-vector/window transplant / local MEMIT-AlphaEdit engine primitives unchanged.

## 0. Question

C10 showed that the fixed-target in-weight path expresses single-token and prior-coherent multi-token values robustly, but fails project-coined multi-word semantic values. The hard A7 coined-coined class is the binding value class for this pilot: `CORPUS/36` measured A7 held-out paraphrase full-sequence at `19.4%`, and `CORPUS/37-39` found no behavioral rescue from later band, widened band, or bounded strength/layer-count MEMIT knobs.

The remaining practical rescue hypothesis is AnyEdit-style autoregressive per-token/window editing: instead of optimizing only a first-value-token anchored edit and relying on the model to realize the continuation, optimize target vectors across the target value tokens/windows.

This pilot asks:

**Can a harness-side AnyEdit small-window transplant materially rescue A7 held-out paraphrase full-sequence readout while preserving A1/A2 controls, locality, token alignment, and LAW#5 inertness?**

This is not C10 closure. It is a feasibility pilot for whether AnyEdit deserves replication and deployment-path follow-up.

## 1. Prior Gates Incorporated

1. `docs/C10_ANYEDIT_VIABILITY_AUDIT.md` found the official LLM AnyEdit target is `jianghoucheng/AnyEdit`; upstream as-is is not comparable because it assumes older dependencies and A100-class headroom. The local test must be a harness-side transplant preserving local MEMIT primitives.
2. The viability audit found upstream `window_size=50` creates only one window for current A7 values (`4-6` Qwen2.5 tokens, mean `5.5`), so it cannot be the primary per-token C10 test.
3. `docs/C10_ANYEDIT_TOKEN_ALIGNMENT_GATE.md` resolved the prior advisor FIX-FIRST item: current A7 stimuli pass answer-vs-continuation suffix alignment `24/24` with leading-space answers. The harness must still enforce this as a hard pre-edit abort gate for every request.
4. This prereg treats advisor/research outputs as design input only. AnyEdit is not evidence until a valid run clears the frozen gates below.

## 2. Arms And Conditions

### Arms

- **A1 single:** single-token positive control.
- **A2 coherent2:** prior-coherent two-token positive control.
- **A7 coined-coined:** hard project-coined multi-word semantic treatment; binding arm.

### Conditions

0. **Same-run local MEMIT reference:** baseline local MEMIT/AlphaEdit recipe: `configs/hparams/qwen25_3b_memit_hparams.json` with layers `[4,5,6,7,8]`, on the same A1/A2/A7 stimuli and evaluator. This is mandatory for any lead label because it is the delta comparator. If implementation cost prevents this, the run may only be labeled `INVALID/HALTED` or `WINDOW_DIAGNOSTIC_ONLY`; it may not make rescue, behavioral-lead, or no-material-rescue claims.
1. **PRIMARY AnyEdit small-window:** `window_size=1`, `overlap=0`. This is the only primary test of the per-token/window rescue hypothesis because it creates multiple target vectors/windows for every A7 value.
2. **DIAGNOSTIC AnyEdit default-window:** `window_size=50`, `overlap=0`, only if cheap after the primary path exists. This condition is explicitly diagnostic-only because it creates one window for A7 and therefore does not test per-token rescue.

No `window_size=2` fallback is licensed by this prereg. If `window_size=1` cannot be implemented in one clean harness-side fix, halt and write the diagnostic; do not switch to another window after seeing results without a prereg addendum.

## 3. Required Implementation Boundaries

- Do not edit `memit_dry_run/memit` science-path primitives.
- Do not downgrade pinned local dependencies.
- Put AnyEdit-only fields such as `window_size`, `overlap`, `nullspace_threshold`, and `L2` in a harness-side wrapper/config, not in the strict local MEMIT hparams schema.
- Preserve the local path convention: `LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")`.
- Emit result JSON under a namespaced path, expected `results/c10h_anyedit_pilot.json`, and logs under `logs/c10h_anyedit_pilot.log`.

## 4. Binding Metric

The binding metric is **A7 held-out paraphrase full-sequence exact match** (`para_full`) across three held-out paraphrases (`72` trials for N=24).

Full-sequence exact match is the database-style read criterion: a project-coined semantic value is usable only if the complete value is returned, not merely its first token.

## 5. Secondary Metrics And Diagnostics

Report, per condition and arm:

- `canon_full`, `canon_first`;
- `para_full`, `para_first`, `para_any_full`;
- exact counts: `canon_full_hits/24`, `para_full_hits/72`, `para_first_hits/72`;
- `P(full|first)`;
- teacher-forced continuation per-token accuracy;
- target token length and decoded target text;
- number of windows, window boundaries, boundary-crossing tokens, selected `lookup_idxs`, target-vector count;
- per-window continuation success where available;
- edit delta norms by edited layer/window;
- locality/bystander probe, including at minimum the existing C10-style collateral prompt and a JS/locality score if available;
- context-reliance diagnostic:
  - held-out paraphrase alone;
  - canonical prompt;
  - held-out paraphrase with a canonical/context prefix if implemented.

Context-prefix success is diagnostic only. It cannot substitute for held-out paraphrase-alone `para_full`.

## 6. Frozen Validity And Abort Rules

The run is **INVALID/HALTED** if any of these fail before result interpretation:

1. **Token-alignment gate fails.** For every request in every arm and condition, the harness must emit:
   - standalone answer token IDs;
   - `question + answer` continuation suffix token IDs of the same length;
   - decoded answer text and decoded suffix text;
   - window boundaries for every planned `window_size`;
   - `lookup_idxs` derived from those windows.

   The harness must use leading-space answers. Abort if any answer IDs differ from the continuation suffix IDs, if decoded text is malformed, or if the primary `window_size=1` condition creates only one A7 window.

2. **LAW#5 AnyEdit inertness fails.** Before any A7 evidence is trusted, an AnyEdit-specific identity/no-op path must produce near-zero expression change and stable locality. The harness must report the same style of `delta_expr` / `delta_loc` diagnostics used by prior C10 harnesses, or halt with a written diagnostic explaining why no meaningful inertness analog exists.

   Frozen inertness thresholds:
   - `abs(delta_expr) <= 0.01`;
   - `abs(delta_loc) <= 3.0` on the existing C10 locality score scale;
   - no parameter tensor may change in a pure no-op pipeline path;
   - for an identity/null edit path, all reported edited-layer delta norms must be finite and the output/locality thresholds above must hold.

   If the harness uses a different locality scale, it must halt and write a prereg addendum before any pilot run.

3. **Engine boundary is crossed.** If the transplant requires changing `memit_dry_run/memit` primitives, replacing local MEMIT/AlphaEdit solve behavior, or downgrading dependencies, halt.

4. **One-fix-then-halt rule is exceeded.** If a hparam/module mismatch cannot be resolved by one clean harness-side wrapper/fix, halt and write the diagnostic rather than iterating toward green.

5. **Same-run reference is invalid.** The same-run MEMIT reference must reproduce the known A7 failure envelope (`A7.para_full <= 35%`) and keep A1/A2 controls at `para_full >= 80%`. If it fails this sanity check, the AnyEdit comparison is invalid; report the diagnostic.

6. **Primary window-count invariant fails.** For `window_size=1`, every request must satisfy `target_vector_count == answer_token_count`, each window must cover exactly one answer token, and `len(lookup_idxs) == answer_token_count`. This must hold for A1, A2, and A7; for A7 it must also imply more than one target vector for every request.

Primary AnyEdit A1/A2 controls below `para_full >= 80%` are not invalid. They are valid evidence of tradeoff/over-editing and cannot support rescue.

## 7. Frozen Outcome Rules

Let `K` be the primary AnyEdit `window_size=1` condition. Let `B` be the same-run MEMIT reference. If `B` is absent or invalid, the run cannot receive a lead or rescue label.

Candidate-level labels:

- **USABILITY_RESCUE_LEAD_NOT_CLOSURE:** `K.A7.para_full >= 85%`, `min(K.A1.para_full, K.A2.para_full) >= 80%`, `K.A7.para_full - B.A7.para_full >= 20pp`, and locality is not materially worse than the same-run reference. This is a lead only, not C10 closure.
- **BEHAVIORAL_LEAD_NOT_CLOSURE:** `K.A7.para_full >= 40%`, `K.A7.para_full - B.A7.para_full >= 20pp`, `min(K.A1.para_full, K.A2.para_full) >= 80%`, and locality is not materially worse than the same-run reference.
- **CONTEXT_DEPENDENT_NON_RESCUE:** context-prefix diagnostic succeeds but held-out paraphrase-alone `K.A7.para_full < 40%` or misses the relevant lead threshold.
- **WINDOW_DIAGNOSTIC_ONLY:** any `window_size=50` result, positive or negative. It may inform mechanism but cannot establish per-token C10 rescue.
- **TRADEOFF_NOT_CLEAN_RESCUE:** A7 improves but A1/A2 controls fall below `para_full >= 80%` or locality materially worsens.
- **WINDOW_BOUNDARY_NON_RESCUE:** apparent gains concentrate on within-window or boundary artifacts while full-sequence held-out `para_full` remains below `40%`.
- **NO_MATERIAL_ANYEDIT_RESCUE:** primary `K.A7.para_full < 40%` and no valid clean-control `>=20pp` same-run delta.
- **INVALID/HALTED:** any validity/abort rule fires.

No result below `A7.para_full >= 85%` can be called C10 closure. No canonical-only, context-prefix-only, first-token-only, or `window_size=50` result can be called a behavioral rescue.

For outcome labels, "locality is not materially worse" means both:

- A7 C10-style locality score is no more than `5.0` points below same-run baseline (`K.A7.locality >= B.A7.locality - 5.0`) when the existing C10 locality score is used;
- any exact-match bystander/collateral metric added by the harness drops by no more than `10pp` vs same-run baseline.

If either locality metric is unavailable, the run cannot receive a lead label.

## 8. Licensed Claims

If negative, this rules out only this scoped harness-side AnyEdit small-window pilot on Qwen2.5-3B / A7 / N=24 / one seed / capital relation / HF-fp16. It does not prove the AnyEdit family impossible, does not prove MEMIT-family editing impossible, and does not update the deployment recipe.

If positive, it is a lead only. Before any C10 closure or deployment claim, it needs at minimum: replication, Q4_K_M survival, broader value-class checks beyond A7, and a larger/model-size or relation transfer check.

## 9. Fork After A Valid Pilot

- If **USABILITY_RESCUE_LEAD_NOT_CLOSURE** or **BEHAVIORAL_LEAD_NOT_CLOSURE**, replicate before promotion and then test Q4_K_M survival of multi-token values.
- If **CONTEXT_DEPENDENT_NON_RESCUE** or **WINDOW_BOUNDARY_NON_RESCUE**, treat fixed-window AnyEdit as insufficient for behavioral readout; the targeted next research lead is muKE/AnyEdit++-style dependency/window handling, not another unbounded hparam sweep.
- If **TRADEOFF_NOT_CLEAN_RESCUE**, SUIT/locality-preserving editing is the cleaner fallback lead.
- If **NO_MATERIAL_ANYEDIT_RESCUE** or **INVALID/HALTED**, the production-safe C10 alternative remains accept-as-bounded: keep in-weight CORE values to single-token / prior-coherent / verified classes, and route project-coined multi-word semantic values through index/side-store/Git-backed mechanisms.
