reviewer: Claude advisor subagent, model Opus 5.5

# Advisor review: `docs/C10S_SOLVEFEAS_PREREG.md` v1 DRAFT (D-C10s-solvefeas)

Date 2026-10-06. Review only. No model was loaded and nothing ran on the GPU. All numbers below were recomputed from `results/c10s_sharedz_r2/inject.json` (`rows[*].shared_solve.history`, `loss_at_stop`, `frame_fit`) and `results/c10s_sharedz_r2/inertness.json` (`checks.*.solve` / `full_solve_record`) with model-free Python.

**Verdict: FIX-FIRST**

The single change (25 to 50 steps, one budget for every solve) is the right design, and 50 is supported by the recorded trajectories. Four things need fixing first. Two of the readings claim more than the record can show. The plan in §5 would leave some solves at 25 steps without anyone noticing. The arm would run under step 1's identity and halt path. And the "every solve's budget is recorded" validity addition can't be met for the engine solves as the code stands.

---

## What the record shows (the facts these items rest on)

- **None of the 24 shared solves were stopped by the loss rule.** All 24 have `stopped_by: "budget"`, `loss_evals` 25, `adam_steps` 24, and 20–22 clamp hits. Each `delta_norm` equals `max_norm` to 0.01.
- **The KL and weight-decay terms put a floor under the stopping rule.** Once the solve is on the clamp, weight decay is fixed at `0.5·0.75/‖target_init‖` (`compute_z.py:154-156`), about 0.0049–0.0064. At evaluation 25 the KL term was 0.0375–0.2144. KL + wd was below 0.05 for only **2 of 24** solves (Zorbland 0.0498, Skornwell 0.0436). For the other 22, the stop at `compute_z.py:164` cannot fire unless KL falls, so most solves will run all 50 evaluations.
- **Late slopes for the seven underfit facts.** Ratio of mean NLL per evaluation at the stop (last one / geometric mean of last three):

  | Fact | Last ratio | Last-3 ratio |
  |---|---|---|
  | Oxbarrow | 0.62 | 0.58 |
  | Zephquin | 0.54 | 0.57 |
  | Fluvane | 0.68 | 0.63 |
  | Marsduq | 0.75 | 0.66 |
  | Drennik | 0.83 | 0.63 |
  | Crulpane | 0.82 | 0.63 |
  | Skornwell | 0.86 | 0.87 |

  All seven reach their minimum NLL at the last evaluation, so all were still falling. The factor each one's worst frame still has to drop, taking −ln(0.98) as the target, is 8.4× for Oxbarrow, 5.1× for Marsduq, 4.9× for Drennik, 3.6× for Zephquin, 3.3× for Crulpane, 2.1× for Fluvane and 1.1× for Skornwell.
- **The well-fit facts slow down near the bottom.** Once mean NLL reaches about 0.01, the per-evaluation ratio rises to about 0.85–0.95 (Trannak 0.981 over the last three, Quenby 0.93, Lurmaxen 0.89). Some are not monotone: Brinduun's minimum was at evaluation 22 and rose after that, and Vythorn rose at the last evaluation.
- **T2 settles just above the line.** Among the passing facts, T2 ends at 0.981–0.990. Ten passing entries sit in [0.98, 0.985): Mophgar, Trannak, Yastovel, Lurmaxen, Wombryne and Thelby on T2, Fluvane on CANON, and three others.
- **The canonical engine solves are borderline at 25 steps.** The inertness canonical solve on Zorbland stopped by `loss<0.05` at **evaluation 25 of 25** (loss 0.0468; `inertness.json` `checks.ii_single.solve`). The triplicate twin stopped at evaluation 24. The heterogeneous (iv) solve ran out of budget. The canonical solves in cell 1 have no recorded stop reason, because the engine's printout is suppressed by `quiet()` (`c10s_sharedz_arms.py:417-418, 423-424`).
- **The context templates differ between processes.** They are sampled without a seed (`c10s_sharedz_arms.py:584-585`; `memit_main.py:304-322`). So the new run's solves will not replay CORPUS/51's first 25 evaluations.
- **`v_num_grad_steps` enters the loop in only two places:** the loop bound (`compute_z.py:108`) and the final break (`:167`). The driver's copy is the same (`c10s_sharedz_arms.py:244, :287`). So, in the same process, a 50-step solve's state at evaluation 25 is exactly the state a 25-step solve would return. A solve that stops by loss at or before evaluation 25 returns the same z under either budget.

---

## Items

### 1. BLOCKING: the readings in §0 and §3 claim more than the record can show. Add a same-run comparison at evaluation 25 and classify each underfit entry.

**Problem (a).** §0 says "A pass of the fit gate says the budget was the binding constraint." That doesn't follow. Templates are unseeded per process, so the 50-step run solves on a different context draw from CORPUS/51. A pass could come from an easier draw. The reverse also holds: with 10 passing entries sitting within 0.005 of the threshold, a harder draw could fail at 50 because of entries that were not underfit in CORPUS/51.

**Problem (b).** §3 says UNDERFIT-AT-50 means "the budget alone does not repair the fit." That is honest only if the underfit entries had stopped improving by evaluation 50. If they are still falling at 50, as all seven were at 25, the right reading is "still limited by the budget at 50; inconclusive about (a)", not "points at (b) or (c)".

**Problem (c).** If a solve stops on the loss rule with a frame below 0.98, the budget was not what limited it. The engine's averaged objective counted the solve as done. That is a third case, and it is distinct from (a), (b) and (c). (The stopping rule ends a solve when the mean NLL over all prompts plus KL plus weight decay is below 0.05. One frame can sit near NLL 0.06, fit about 0.94, while the mean passes.)

**Fix (record).** In `compute_z_shared`, record `nll_each` at every evaluation. That is 18 floats × 50 evaluations × 24 facts, which is negligible. Also record `frame_fit_at_eval25`, computed from the evaluation at `it == 24`. As shown above, this is exactly the 25-step fit in this process on these templates. Snapshot `delta` at `it == 24` as well, so the 25-step shared z exists if the reader needs it.

**Fix (readings, put in the reader per the CORPUS/50 Q2 lesson).** Leave the gate unchanged: still any frame below 0.98 at stop. Add these descriptors:

- **Budget binding (in-run)** means the fit at evaluation 25 fails in this run and the fit at stop passes. Only this supports "the budget was the binding constraint". If the fit passes at both 25 and 50 in-run, the record should say "fit passes; the budget was not shown to bind (this process's 25-step fit also passes)".
- **Each entry below 0.98 at stop is classified, in this precedence:**
  - `OBJECTIVE-STOPPED`: `stopped_by == "loss<0.05"`.
  - `PLATEAUED`: proposed rule is that the entry's frame fit changed by less than 0.002 between evaluations 40 and 50. The program should freeze this number before the run.
  - `STILL-DESCENDING`: everything else.
- **UNDERFIT-AT-50 wording:**
  - "Budget alone does not repair the fit; not separated between (b) and (c)" only if every underfit entry is PLATEAUED.
  - "Still limited by the budget at 50; inconclusive about (a)" if any entry is STILL-DESCENDING.
  - "Objective satisfied with a frame below 0.98; not the budget" for OBJECTIVE-STOPPED entries.
  - Every case routes to step 2. A further budget extension would need its own ruling.
- **Per-entry comparison.** For each entry, print the fit at evaluation 25 in this run beside CORPUS/51's fit. The record can then show whether an UNDERFIT-AT-50 comes from the seven original facts or from entries that passed before.

### 2. BLOCKING: §5's single environment variable does not reach every solve, and several paths would stay at 25 steps without anyone noticing.

These are the points the 50-step settings must reach, and what happens if each one is missed:

| # | Where | Current code | If missed |
|---|---|---|---|
| a | Driver's `hp`, used by the canonical, shared and twin solves in cell 1 | Imported from `c10l_covgeom_p6_zinject.py:25`, which reads the hard-coded `H.HP_BASE` (`c10e_bandknob.py:30`, not an env var). The driver imports it by name at `c10s_sharedz_arms.py:115`. | **All of cell 1 stays at 25 steps**, while the harness pass runs 50 if only `HP_CANDIDATE` is changed. Fix: in the driver, right after the imports, rebind `hp = MEMITHyperParams.from_json(<selected path>)` and assert `hp.layers == p6.hp.layers` and `hp.layers[-1] == Z_LAYER`. Do not edit `p6` or `H.HP_BASE`. |
| b | Inertness `hp` | `c10s_sharedz_inertness.py:35` takes `A.hp` | Follows (a) automatically if the rebinding happens at driver module level. Assert it. |
| c | Harness pass (`run_recipe` → `my_edit` → engine `compute_z` for A1, A2 and the reference A7, plus `run_law5`) | With `C10_RECIPES=candidate`, only `run_recipe(CANDIDATE_NAME, HP_BAND)` runs (`c10e_bandknob.py:582`). `HP_BAND` comes from `HP_CANDIDATE`, **hard-coded** at `c10s_sharedz_arms.py:105` to the 25-step file. `HP_BASE` is not used in the pass. | **The pass stays at 25 steps.** Set `HP_CANDIDATE` from the selected path before `import c10e_bandknob` at `:114`. That import is where `HP_BAND` is read. |
| d | Inertness/driver binding | `require_inertness` (`:570-581`) compares only source-file hashes. | **An inertness record made at 25 steps would certify a 50-step run**: both settings files are in the hashed set, so the hashes match either way. Fix: record `hparams_path`, `hparams_sha256` and `v_num_grad_steps` in `inertness.json`. Halt if they differ from the driver's. |
| e | `second` stage | Re-checks source hashes only (`:642-644`) | **A second process launched without the variable solves at 25 steps.** Fix: halt unless the effective hparams sha equals the one in `run.json`. |
| f | Records | `"hparams": H.HP_BASE` at `c10s_sharedz_arms.py:474` (inject.json), `:610` (run.json), `c10s_sharedz_inertness.py:171` | Every record would name the 25-step file. Fix: write the effective path, sha and `v_num_grad_steps`. |

**Positive control (cheap; it shows the setting actually reached the solves).**
- Assert that every shared solve's `loss_evals` is at most `hp.v_num_grad_steps` and that at least one is greater than 25.
- In inertness, (ii) and (iii) on Zorbland stopped by loss at evaluations 25 and 24. At 50 steps they will return the same z as at 25 and will not exercise evaluations 26–50. Only (iv) does. Assert `checks.iv_heterogeneous.full_solve_record.loss_evals > 25`, and record that (ii) and (iii) never left the 25-step range.

**Preferred form.** Use a closed selector, for example `C10S_ARM ∈ {sharedz, solvefeas}`, that maps to one frozen record: `{decision_id, prereg, hparams, halt_path, default OUT_DIR}`. This is better than a free path variable because it cannot produce a mixed state, such as the new settings under the old prereg. With the selector unset, behaviour must be bit-identical to `1169794`, as §5 already requires.

### 3. BLOCKING: the arm runs under step 1's identity, and a halt would overwrite step 1's provenance file.

- `DECISION_ID = "D-C10s-sharedz"` (`c10s_sharedz_arms.py:51`).
- `PREREG` is fixed to `docs/C10S_SHARED_Z_PREREG.md` (`:108`).
- `HALT_PATH` is `architecture_profile/c10s_sharedz_halt_diagnostic.json` (`:52`). That file is the step-1 HALT diagnostic cited by CORPUS/51 at 0d422ad. Any halt in this arm would overwrite it.
- `docs/C10S_SOLVEFEAS_PREREG.md` is not in `SOURCE_FILES` (`:139-142`). §5 adds only the new settings file.

**Fix:**
- Under the solvefeas selector: decision ID `D-C10s-solvefeas`, prereg `docs/C10S_SOLVEFEAS_PREREG.md`, and halt path `architecture_profile/c10s_solvefeas_halt_diagnostic.json`.
- Add both the new prereg and `qwen25_3b_memit_hparams_steps50.json` to `SOURCE_FILES`.
- The parent prereg stays hashed, since §1 inherits it.
- Make the `OUT_DIR` default `results/c10s_solvefeas/` under the selector.

### 4. BLOCKING: §2's "effective `v_num_grad_steps` of every solve" can't be met for the engine solves, and it is the evidence that question (2)'s comparability rests on.

**Problem.** §2 says "the solve diagnostics already record `loss_evals`". That is true only for the shared solves. The canonical, twin and harness solves (A1, A2, reference A7) go through the unmodified engine with its output suppressed (`quiet()`; `recording_compute_z` at `:487-492` captures only z). Nothing records how many evaluations they ran.

**Why it matters.** The engine solves are borderline at 25 steps (Zorbland stopped at evaluation 25 of 25). This count is what shows which canonical and reference targets actually changed under the new budget, and so how far the reference can have moved away from CORPUS/44–51.

**Fix (no engine edit).** Around each `_engine_compute_z` call, in cell 1 and inside `recording_compute_z`, add a read-only forward hook on `block` that counts the forward passes made during the call, in the style of `CaptureTargetInit`. `compute_z` makes exactly one forward per evaluation (`compute_z.py:108-122`), so the count equals the number of evaluations. Record it per solve. A count of 25 or less means "this z is identical to the 25-step z in this process". A count above 25 means "changed by the budget". Report, per arm, how many of the 24 targets changed.

### 5. ADVISORY: 50 is the right N, but §1's justification is wrong in detail and the cost argument is false.

- "Roughly halved per step at the stop" holds for Oxbarrow (0.62) and Zephquin (0.54) only. Drennik (0.83), Crulpane (0.82) and Skornwell (0.86) were slower.
- The stronger justification:
  - Straight-line extrapolation of each fact's last-three slope reaches the worst-frame target in about 3–5 more evaluations: Oxbarrow ≈ 4–5, Marsduq ≈ 4–5, Drennik ≈ 3.5, Zephquin ≈ 2.5, Crulpane ≈ 2.5.
  - Allowing for the slowdown the well-fit facts show (about 0.85–0.95 per evaluation once mean NLL is near 0.01), the estimate becomes about 10–15.
  - So 25 more steps give about twice the needed headroom. Keep 50.
  - A larger N, say 100, only guards against the STILL-DESCENDING case that item 1 now reports honestly. It would also change more canonical and reference targets (see item 4). I would not raise it.
- Delete "(the stopping rule ends a solve early)". KL + wd was 0.05 or more for 22 of 24 shared solves at evaluation 25, so expect almost every shared solve, and probably most canonical ones, to run all 50.
- §4 costs: cell 1 took 1750 s at 25 steps. Re-estimate cell 1 at about 50–60 min and the pass at about 45–60 min, not 35. The pass's 72 engine solves plus `run_law5` all double too.

### 6. ADVISORY: one budget everywhere is the fair design. Change the response to an envelope miss.

- Using the same budget for the canonical, twin and shared solves is required. Canonical at 25 against shared at 50 would mix up the phrasing variable with the budget. The twin is only a rounding null if it matches the shared solve's batch shape and budget.
- A1, A2 and the reference A7 cannot be split anyway: `run_recipe` applies one `hp` per recipe (`c10e_bandknob.py:458-489`). The ≥ 10 paired gain needs the same-run reference at the same budget.
- What breaks with CORPUS/44–51 is limited to targets whose engine solve needed more than 25 evaluations. Item 4 measures that.
- **Fix to §2's first bullet.** The [5, 18]/72 and [5, 10]/24 envelope is the spread of the 25-step baseline (`c10m_diag_read.py:13`). If the 50-step reference lands outside it, that is a measured effect of the budget on the program's baseline, not a harness defect. Label it **REFERENCE-SHIFT**: halt the comparison, record it as a finding with item 4's count of changed targets, assign no label to the shared arm, and do not call it "INVALID, not a finding".
- Keep A1 and A2 ≥ 68 as validity checks.
- State as a limit that PARTIAL's "> 18" threshold comes from the 25-step envelope.

### 7. ADVISORY: the fit gate is fragile near the threshold. Report on it; do not change it.

- Ten passing entries sit in [0.98, 0.985), and late NLL is not always monotone (Brinduun, Vythorn).
- The engine returns the last iterate, not the best one. So a fact that passed at 25 can dip below 0.98 at evaluation 50 through oscillation alone.
- The frozen gate stands. The reader should print the number of entries in [0.975, 0.985] and, for each new failing entry, its evaluation-25 fit (item 1). That keeps such a dip from being read as a frame result.

### 8. ADVISORY: §0 and §3 wording on frames.

- Rephrase "points at (b) or (c) without separating them" to "consistent with (b), (c) or the averaged objective; not separated". The third option is item 1's OBJECTIVE-STOPPED case.
- State in §3 that "fit" is still the parent's teacher-forced context-average diagnostic. Neither a pass nor a fail is a statement about full-sequence frame reads (CORPUS/51 F-S4/F-S5).
- Nothing else in the draft claims too much about frames.

### 9. ADVISORY (optional, cheap): a two-by-two comparison inside one process.

- With item 1's `delta` snapshot at evaluation 25, the 25-step shared z costs nothing. Running the canonical engine solve a second time at the 25-step settings costs a 7-row solve per fact.
- Injecting all four targets (canonical and shared, at 25 and at 50) gives the budget effect on each target in the same process and on the same templates. It would replace the comparison with CORPUS/51's 51/69, which is confounded by the different templates.
- These would be readouts only, with no gate.

---

**BLOCKING summary:** (1) the readings claim too much: add an evaluation-25 fit from the same run and classify each underfit entry as objective-stopped, plateaued or still-descending. (2) The settings variable does not reach the driver's `hp` (p6 import), the hard-coded `HP_CANDIDATE`, the inertness/driver binding or the `second` stage, and the records name the 25-step file: rebind, bind and assert, with a positive control showing more than 25 evaluations. (3) The decision ID, prereg and halt path are step 1's, so a halt would overwrite CORPUS/51's diagnostic: use per-arm identity and hash the new prereg. (4) The engine solves record no evaluation count: add a read-only forward-count hook so the reference shift can be attributed.
