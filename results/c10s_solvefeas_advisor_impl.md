reviewer: Claude advisor subagent, model Opus 5.5

# Advisor implementation review: D-C10s-solvefeas (prereg v2; Codex report `results/c10s_solvefeas_codex_impl.md`)

Date 2026-10-06. This is a review only. I loaded no model and ran nothing on the GPU. I read the working-tree diff against HEAD for the four driver/reader files, plus the new settings file. HEAD's copies of those four files are byte-identical to `1169794` (`git diff 1169794 HEAD` is empty for them).

I ran two model-free checks:
- The 1169794 reader (`git show 1169794:…/c10s_sharedz_read.py`) and the new reader, both on `results/c10s_sharedz_r2`. Both exit 0 with **identical** output, ending in `cell 1 outcome: UNDERFIT`.
- `diff` of the settings files. The only change is line 6, `"v_num_grad_steps": 25 → 50`.

I took the 28/28 selftest result from the coordinator's run and did not rerun it.

**Verdict: FIX-FIRST.** There is one BLOCKING item, and its fix is one line. Everything else is implemented as v2 specifies. Once item 1 is fixed (plus one selftest case for it), this can proceed without another full review.

---

## (1) My four v1 BLOCKING items, as v2 specifies them

**a. The evaluation-25 snapshot is the 25-step state, taken before the update.** Implemented correctly.
- At `c10s_sharedz_arms.py:368-370`, the snapshot is taken when `it + 1 == 25`. That point is after the forward pass and loss for evaluation 25, and before the stop check, `loss.backward()`, `opt.step()` and the clamp.
- So `delta` there has had 24 Adam updates plus the clamp applied after the 24th. That is exactly what a 25-step solve returns: the engine breaks at `it == N-1` without updating (`compute_z.py:164-168`).
- `nll_each` comes from that same evaluation, so the snapshot's `frame_fit` equals the 25-step solve's fit at stop.
- If the solve stops on the loss rule before evaluation 25, the snapshot is taken after the loop (`:393-396`) and marked `carried_forward`. That state is the same under both budgets. Correct.
- `_target_25 = target_init + delta25`, the same arithmetic as `:180`. It is injected only on the held-out templates (`:544-546`) and recorded with no gate.

**b. Closed `C10S_ARM` selector with its own identity.** Implemented, with one gap (item 1 below).
- `Arm` NamedTuple and `_ARMS` at `c10s_sharedz_read.py:52-77`. Each arm carries its Decision-ID, prereg, halt path (`architecture_profile/c10s_solvefeas_halt_diagnostic.json`), settings file, step count and output directory.
- `DECISION_ID`, `HALT_PATH` and `PREREG` are rebound from the selected arm at `arms.py:100-108,127`.
- Both preregs and `qwen25_3b_memit_hparams_steps50.json` join `SOURCE_FILES` for solvefeas only (`:163-168`).
- `results/c10s_solvefeas/` does not exist yet, so nothing will be overwritten there.

**c. The 50-step settings reach every solve.** Implemented.

| Route | Evidence | Status |
|---|---|---|
| Driver `hp`, used by the canonical, shared and twin solves | Rebound at `:146`, `assert hp.v_num_grad_steps == ARM.steps` at `:147`. The shared solve is at `:445`, canonical and twin at `:510,:517`. | OK |
| Inertness | `H, hp, Z_LAYER = A.H, A.hp, A.Z_LAYER` (`inertness.py:35`) runs after the driver module finishes importing, so it picks up the rebound `hp`. Engine solves go through `A.engine_solve` (`:55`). LAW#5 (v) runs inside `count_nested_engine_solves` (`:208`). | OK |
| `HP_CANDIDATE` set before the harness import | Set at `:126`. `import c10e_bandknob as H` happens at `:135`. `HP_BAND` is read at import (`c10e_bandknob.py:31`). Asserted at `:148`. | OK |
| Harness A1 / A2 / reference A7 / `run_law5` | `run_recipe(CANDIDATE_NAME, HP_BAND)` (`c10e_bandknob.py:582`). Every engine call goes through `recording_compute_z → engine_solve`, which asserts the step count (`:216`). | OK |
| LAW#5 engine path (`apply_memit_to_model → execute_memit → compute_z`) | `memit_main.compute_z` is rebound while the call runs (`:228-241`). `memit_main.py:129` calls the module-level `compute_z` by name and positionally, so the rebinding takes effect. The engine cache path is unused (`cache_template` defaults to None, `memit_main.py:32,106-113`). | OK |
| Bound across processes | `require_settings` checks arm, path, sha and step count (`:695-700`, reader `SETTINGS_KEYS` at `:49`). It is applied to the inertness record and its identity (`:709-710`), and in the second stage to `run`, `IDENTITY`, `pass1` and its identity (`:784-785,:796-797`). | OK |
| Arm swap between first and second stage | A sharedz `second` run against a solvefeas `OUT_DIR` skips `require_settings`. It still halts in `provenance_mismatches`, because the recorded source set has two extra files. | Caught |
| Every record names the settings | `"hparams": HP_PATH` replaces `H.HP_BASE` (`:573,:749`, `inertness.py:171`). `RECORD_SETTINGS` is stamped into dumps, identities, shared diagnostics and halt records. | OK |

**d. Engine forward counting and the positive control.** Implemented.
- `CountForwards` is a root-module forward hook that returns `None` (`:198-209`).
- `compute_z` calls `model(**input_tok)` once per evaluation (`compute_z.py:108-122`), so the count equals `loss_evals`. A count outside `[1, steps]` halts (`:221`).
- The positive control (`solve_budget`, reader `:137-152`) requires some solve with more than 25 evaluations. It is applied in cell 1 (`:587`), in each pass (`:671`, and `validity` at reader `:400-415`) and in the second process (`:817`).
- **Scope note:** the shared solves meet this control on their own, because they always run to budget at 50 (v1). So the control proves the setting reached the shared solver. For the engine-side solves, the guarantee is the hard check `hparams.v_num_grad_steps == ARM.steps` in `engine_solve` (`:216`). That is sound, but see item 3.

## (2) Reader classification and labels against v2 §3

These match v2 §3 exactly.

- **Classes** (`underfit_class`, reader `:98-105`):
  - `objective-stopped` when `stopped_by == "loss<0.05"`. This takes precedence, including a loss stop at evaluation 50.
  - `plateaued` when `|fit50 − fit40| < 0.002`, using `history[39]` and `history[49]`.
  - `still-descending` otherwise, including exactly 0.002.
- **Labels** (`:127`):
  - UNDERFIT-AT-50 when the fit gate fails at stop.
  - Else FIT-PASSES-AT-25 when the gate passes at evaluation 25.
  - Else BUDGET-BINDING. This matches v2: the gate passes at stop and some entry was below 0.98 at evaluation 25.
  - Evaluation 25 uses `min(25, n)` for solves that stopped on the loss rule earlier.
- **Precedence in cell 1** (`solvefeas_cell1_outcome`, `:155-161`): budget INVALID, then UNDERFIT-AT-50, then NOISE-NON-DISCRIMINATING, then the screen. This matches A2 and v2.
- **REFERENCE-SHIFT** (`:179-181`):
  - Inclusive bounds: para [5, 18] and canon [5, 10].
  - `validity` drops the envelope reasons for solvefeas only (`:430,:432`). A1/A2 ≥ 68 and every other validity check stay first.
  - The driver then persists `outcome: REFERENCE-SHIFT` in the pass and in `run.json`, and halts to the solvefeas halt path (`:684-691`).
  - In the second process it becomes a permanent named outcome, and the reader accepts it (`:459-465,:481-519`).
  - This is "HALT + record + report", not INVALID, as v2 specifies.

## (3) Behaviour with `C10S_ARM` unset compared with `1169794`

The numerical path is identical. Evidence:
1. The AST equality test of `compute_z_shared`'s default path (`selftest.py:693-732`).
2. `engine_solve` and `count_nested_engine_solves` return or yield without hooks for sharedz (`:214-215,:230-232`).
3. `RECORD_SETTINGS = {}`, so dumps and dicts are unchanged.
4. For sharedz, `HP_PATH` equals the old `H.HP_BASE` string.
5. The rebound `hp` loads the same file as P6's.
6. The reader produces identical output on `results/c10s_sharedz_r2` (above).

A rerun of step 1 would therefore follow CORPUS/51's code path. It would **not** reproduce CORPUS/51's identity, because the source digest changes with the edited files and the context templates are unseeded. Those differences are expected and do not affect correctness.

The only structural change on the default path: `import c10s_sharedz_read as R` (`:98`) now runs outside the initialization halt boundary, so a failed import raises without a diagnostic. This has no effect on results.

---

## Items

### 1. BLOCKING: an invalid `C10S_ARM` value writes to step 1's halt file

**Problem.** The module-level defaults are still `DECISION_ID = "D-C10s-sharedz"` (`:53`) and `HALT_PATH = …/c10s_sharedz_halt_diagnostic.json` (`:54`). On an unknown selector, `halt(str(e))` at `:102` runs before they are rebound at `:103-104`.

So a mistyped arm writes over the git-tracked step-1 HALT diagnostic that CORPUS/51 cites (0d422ad). Examples: `C10S_ARM=solveFeas`, or `solvefeas ` with a trailing space. The inertness script imports the driver, so the same path is reachable from there. v2 §4 says "the step-1 halt file must never be written by this arm".

**Fix.** Replace `:101-102` with:

```python
except ValueError as e:
    raise SystemExit(f"HALT: {e}")
```

so nothing is written. Alternatively, set `HALT_PATH` to a neutral `architecture_profile/c10s_arm_selector_halt_diagnostic.json` before `select_arm`. Add a selftest that runs the selector block with `C10S_ARM=bogus` and asserts the step-1 halt file's mtime and bytes are unchanged.

### 2. ADVISORY: save cell 1's data before the reader rules can raise

`solvefeas_reading` and `underfit_class` raise `ValueError` on an inconsistent history (reader `:103,:113-115`). They are called inside `injection_cell` (`:586`), before `dump(inject.json)` (`:761`). If one raises, about an hour of cell-1 results reaches the top-level `halt` with no `inject.json`.

Fix: wrap the three solvefeas computations at `:585-588` in `try/except ValueError`, and call `halt(..., partial_inject=out-without-tensors)`. Or dump `inject.json` with outcome `PENDING` first. Given the data, this is unlikely to trigger: budget-stopped solves always have `loss_evals == 50`.

### 3. ADVISORY: use explicit halts instead of `assert` on the budget checks, and record observed values rather than the arm's stamp

The checks at `:147`, `:148` and `:216` are `assert`s, which `python -O` removes.

Separately, the `v_num_grad_steps` written into each engine-solve record and shared diagnostic is `ARM_RECORD`'s constant, not a value read from the `hparams` object actually used. The reader's `settings_mismatches` therefore compares a stamp against a stamp.

Fix:
- Replace the three asserts with `if …: halt(…)`.
- In `engine_solve` and in `compute_z_shared`'s diag, record `"v_num_grad_steps": hparams.v_num_grad_steps`. Put it after `**ARM_RECORD`, so the observed value overrides the stamp and a mismatch becomes visible to `solve_budget`.
- Add the same guard at the top of `compute_z_shared`, solvefeas only.

### 4. ADVISORY: report how many engine targets the budget changed

v1 item 4 asked for this count so that the reference move, and any REFERENCE-SHIFT, could be traced to specific targets. A target whose engine count is 25 or less is identical to its 25-step version in this process. The counts are recorded, but nothing reports them.

Fix: in the reader, print the number of solves with `loss_evals > 25` out of the total, broken down by `role` (canonical, noise twin, harness). For the harness, break it down per arm using `extra.engine_solves`, especially reference A7. Print this beside any REFERENCE-SHIFT disposition. Readout only.

### 5. ADVISORY: `still-descending` also covers fits that got worse

The class is "otherwise" (v2 §3), so a frame whose fit fell by 0.002 or more between evaluations 40 and 50 is called still-descending. Its qualification text, "the budget is not exhausted as an explanation", then misdescribes it. Late NLL was not monotone in CORPUS/51 (Brinduun, Vythorn).

Fix: keep the frozen class. Record the signed `fit50 − fit40` per failing entry and print "(fit fell)" when it is negative. Readout only, no change to the label.

### 6. ADVISORY: the inertness record carries engine counts but no budget check

`rec["engine_solves"]` is recorded (`inertness.py:174`), but `solve_budget` is not applied there. Also, (ii) and (iii) on Zorbland will probably stop on the loss rule at about evaluation 25, so only (iv) exercises evaluations 26 to 50.

Fix: record `R.solve_budget(A.ENGINE_SOLVES, {"iv": iv_diag}, A.ARM_RECORD)` and `iv.full_solve_record.loss_evals` in the inertness record. This can be recorded only; the run-level controls already gate.

---

**BLOCKING summary:** (1) An invalid `C10S_ARM` value halts while `HALT_PATH` is still step 1's (`arms.py:53-54,:101-102`), which overwrites the CORPUS/51-cited `architecture_profile/c10s_sharedz_halt_diagnostic.json`. Fix: `raise SystemExit` without writing (or use a neutral halt path), plus a selftest.
