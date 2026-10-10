# C10Y calibration 4 — ZERO_STEP-IDENTITY halt: diagnosis (2026-10-08 ~21:20 MDT)

**Verdict: PROPERTY of the frozen check (iii), not a code bug.** The driver computes exactly what prereg :130 specifies. The frozen tolerance and exact-count rule assume a recomputation that reproduces recipe A bit for bit. The zero-step path is algebraically equal to recipe A but numerically different, and nothing in the code can make it bit-identical. Diagnosis only; no fix was applied and nothing was launched.

## What halted
- Run: `results/c10y_directdw_calib4/` (launched 20:32:40, halted 21:00:57). Diagnostic: `architecture_profile/c10y_halt_diagnostic_20261009T023240Z_CALIB4.json`, phase `instrument_prefix`, code ZERO_STEP-IDENTITY.
- The memory floor held. Recipe A passed LAW#3 in this process: A7 canon 8/24, para 12/72, first 52; A1 70, A2 71 (`logs/stage_calib.log`). LAW#5 standing was INERT. The capture-solve check (ii) passed, because the run reached (iii).
- Zero-step A7 merged counts were canon 8, para_full **13**, para_first **53**, against reference 8 / 12 / 52, so `counts_equal` was false. Directed distance to recipe A's realized write was 2.83e-4, 2.30e-4, 2.93e-4, 2.24e-4 and 1.60e-4 at layers 4–8.

## The rule and the code (LAW#4)
- Prereg :129 (ii): run the original `my_edit` twice; floor = largest per-layer `‖ΔW_a − ΔW_b‖_F/‖ΔW_a‖_F`; tolerance = max(10 × floor, 1e-4), taken from the C10V rule. Prereg :130 (iii): the zero-step merge must give weights "within (ii)'s tolerance of recipe A's" and **identical** canon_full_n / para_full_n / para_first_n. None of Amendments T (§9), C (§10, :718, :739) or P (§11) changes (iii).
- Code: `c10y_directdw_arms.py:2630` sets `tolerance=max(10*floor,1e-4)`. The floor is the distance between two runs of the same deterministic `my_edit`, effectively 0, so tolerance = 1e-4. `:2656` computes `_directed_distance` (`:1762`: relative Frobenius in CPU float64) between recipe A's realized write `references[arm]` and the zero-step realized write. `:2657` compares counts with the in-process recipe A metrics (`:2643`). `:2667` halts on either test.
- Reference path (recipe A, `c10e_bandknob.py:205–217`): CPU fp32 `upd = solve(M, P·K·rᵀ)ᵀ`, then `W_fp16 += upd.to(device, fp16)`.
- Zero-step path: `factor_solve` (`c10y:238–243`) solves `X = solve(M, P·K)` on the CPU in fp32 and sets B = Xᵀ, A(0) = r. The Writer moves A and B to MPS in fp32 (`:562–563`) and merges `W_fp16 += to_like(A@B, W)` (`:635`): an MPS fp32 matmul, then fp16. In exact arithmetic r·Xᵀ = upd, which is all the prereg asserts (prereg :45 already says the implementation "does not assert bit-exact factorisation or exact preservation of the quantised deployed update"). In floating point the two paths solve different right-hand sides of an ill-conditioned M and multiply on different devices.

## Why not a bug
- The conversions are safe. `to_like` (`:194–196`) moves device first, then dtype. `cpu64` (`:189–191`) is detach→cpu→double. The two CPU-side `.float().cpu()` calls in `factor_solve` do not change dtype. The known torch 2.8 MPS offset-view hazard (combined MPS→CPU device+dtype change) does not occur.
- The contexts are the same: recipe A and the zero-step run share one process, one pinned template set and one restored W0. A zero ΔW initialisation cannot apply, because A(0) = R by design (prereg :47).
- Signed zero is irrelevant: these are value differences on ~0.1–0.5 % of elements, not −0/+0 byte flips.

## Quantitative check (CPU only, real weights)
`results/c10y_directdw_calib4/fp16_realize.py` uses the real Qwen2.5-3B `down_proj` 4–8 weights (fp16, read straight from the safetensors shards, no model load). It adds a rank-24 update at A7 recipe A's per-layer write norms (`results/c10x_enginepath_rerun3/pass1.json` `write_norms_float64`), realized two ways that differ only before the fp16 cast:

| fp32 pre-cast relative difference | realized fp16 directed distance (L4–L8) | elements changed |
|---|---|---|
| 1e-7 (pure fp32 reassociation) | 1.4–2.1e-5 | ≤0.01 % |
| 1e-6 | 4.1–5.8e-5 | 0.03–0.05 % |
| 1e-5 | 1.3–1.9e-4 | 0.3–0.5 % |

The observed 1.6–2.9e-4 corresponds to a pre-cast difference of roughly 1–3e-5. That is the expected size of two fp32 solves of an ill-conditioned M with different right-hand sides, plus an MPS-vs-CPU matmul (rough bound cond(M)·ε₃₂). fp16 rounding then turns it into ~1e-4-scale realized distances, on a fraction of a percent of weights. A ±1 change on one borderline held-out prompt (para_full and para_first each +1, consistent with a single prompt flipping to a full hit) is then an expected outcome. This simulates the mechanism; it does not measure this run's fp32 difference. That difference was not recorded (see record defect). Running the factors on the CPU would need the model, which this diagnosis did not load.

**So the frozen (iii) asks for something this solve path cannot deliver.** A floor measured by repeating an identical deterministic computation (0) says nothing about an algebraically equivalent but different computation. Exact count identity cannot survive the fp16 rounding flips on a borderline prompt. Note that the reference write itself carries fp32 solve error of the same order. Check (iii-b) (executed loop, the same merge at `:635`) would face the same issue.

## Record defect (separate, record-only)
`law5_calib.json`, `ledger_calib.json`, `overlap_audit_calib.json` and `step0_calib.json` are each 3 bytes, `{}\n`, which is why they share SHA-256 ca3d163b…. All four calibrations (calib1–4) show the same. Cause: `calibration_main` initialises `prefix={}` (`:1359`); `instrument_prefix` raises Halt before returning (`:1366`); `persist_prefix` (`:1302–1315`) then writes `prefix.get(key, {})` placeholders. Everything built inside `instrument_prefix` is lost on any halt: the LAW#3/V4 record, the (ii) floor/tolerance/distances, the ledger, step0, and the per-prompt recipe A rows. As a result this diagnosis cannot name the flipped prompt or its margin. It is the same class as ASTRA's lost `dstats` (CLAUDE.md halt rule: keep the offending output). Fix: persist each record as it is created, or attach it to the Halt detail. That is record-only and needs a regression test like ASTRA ruling 5.

## Options for the team (none applied; each needs a dated amendment + Astra review; pre-register before any re-run)
There is no "one fix" in code that is honest: making the zero-step merge bit-identical (e.g. merging the captured `reference_update`) would make check (iii) vacuous, because it is meant to validate the A@B merge path.
1. **Recommended: a precision-floor amendment to (iii)/(iii-b).** Replace the repeat floor with a path-precision floor measured the same way every run: the realized distance between recipe A's fp32-solve write and the same update solved in float64 on the CPU and realized through the identical fp16 add. Tolerance = max(10 × that floor, 1e-4). Replace exact count identity with: every per-prompt hit difference must lie on a prompt whose recipe A margin is below a pre-registered ε, with |Δcount| ≤ 1 per metric. Alternatively, defer count identity to the train–deploy parity check (iv), which already compares merged against forward. The ε and the ±1 must be frozen by Astra before any new data, given that one failure has been observed.
2. Compare at fp32 (planned), not realized fp16: `‖A@B − upd‖/‖upd‖` ≤ k·cond(M)·ε₃₂, recorded per layer, with the realized-count check handled by (iv) parity. Cleaner numerically, but further from the "merged weights" wording.
3. Accept ZERO_STEP-IDENTITY as stage-1 calibration's terminal outcome for this design. That stops step 7 before any candidate.
Whichever option is chosen, also fix the record defect before the re-run (record-only, regression-tested).

## Process notes
- Re-run rule D-C10w-p2rerun: any continuation is a fresh calibration (calib5, fresh namespace). calib4 is kept as data and never read around.
- Escalation history: calibration 3's authorization returned a further **memory-floor** halt to the operator. That class is resolved: this run passed the floor with 34.45 GiB available. ZERO_STEP-IDENTITY is a different halt class: a frozen instrument rule, with decision owner the team via Astra under the operator's delegation ("All questions are to be decided with the team").


## Reviewer qualification (GPT-6-Astra, 2026-10-09 — `zero_step_ruling_astra.md` ruling 1; appended, original text unchanged)
- Verdict stands as PROPERTY of the implemented comparison with no demonstrated causal arithmetic bug; the persistence defect is a separate, confirmed bug.
- "Cannot pass by construction" is withdrawn: non-bit-exact arithmetic can still meet a finite tolerance and identical discrete outputs. Prereg :45 disclaims bit-exactness, but :47 promises zero-step reduction and :129–131 define its empirical acceptance criteria — this is an unfulfilled requirement, not a proof of impossibility.
- `fp16_realize.py` uses random factors and injected perturbations with real pristine weights and C10X-borrowed norms; it illustrates rounding amplification and does NOT measure calibration 4's fp32 gap, condition number, changed-element fraction or prompt margins.
- Net +1/+1 does not establish a single changed prompt (gains and losses may cancel); "borderline" and "expected" are hypotheses.
- The repeat floor and capture distances were lost (empty records); reaching (iii) supports that (ii) passed under the inspected control flow but does not recover those measurements.
- Competing explanations remain: numerical reassociation/device effects (plausible, not established), solve conditioning, and an unisolated state/input or implementation discrepancy.
- Disposition: option 3 — calibration 4 is terminal HALTED / ZERO_STEP-IDENTITY (D-C10y-zerostep); no calibration 5 is authorized by this ruling.
