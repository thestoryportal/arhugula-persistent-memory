# C10Y pre-cast comparison diagnostic — scope (FROZEN v2)

**Status: FROZEN v2 (2026-10-09) — GPT-6-Astra high FREEZE, `results/c10y_directdw_calib4/precast_scope_astra_r2.md` (no BLOCKING). Freeze approves the scope only: implementation review is still required before any run, and nothing here authorizes corrective execution, calibration 5 or stage-1.** History: v1 written 2026-10-09 under D-C10y-zerostep (SHA-256 f666bd01…); v2 folds GPT-6-Astra (high) review `results/c10y_directdw_calib4/precast_scope_astra.md` (FIX-FIRST, 4 BLOCKING + ADVISORY; fold log §Fold log). Nothing here may run until GPT-6-Astra freezes this scope and the implementation passes review. The classification below is threshold-free (BLOCKING 3); no numerical magnitude threshold is proposed.

## Why
Calibration 4 halted terminally on the zero-step identity check (iii) (prereg `docs/C10Y_DIRECTDW_PREREG.md` §12, Amendment ZERO-STEP-DISPOSITION; diagnostic `architecture_profile/c10y_halt_diagnostic_20261009T023240Z_CALIB4.json`: relative distances 1.6e-4–2.9e-4 at layers 4–8 vs tolerance 1e-4; counts 8/53/13 vs 8/52/12). GPT-6-Astra's ruling (`results/c10y_directdw_calib4/zero_step_ruling_astra.md`, ruling 1 and closing note) leaves three competing explanations open — (R) numerical reassociation/device effects, (K) solve conditioning, (S) an unisolated state/input or implementation discrepancy — and names the cheapest informative follow-up: preserve and compare the **actual** reference pre-cast update, factors and device product **on identical inputs**. This scope is that diagnostic. It localizes device-product effects and records evidence bearing on reassociation, conditioning and implementation/state discrepancies; these mechanisms need not be mutually exclusive. It does not by itself qualify any redesign (ruling closing note).

## Boundary
- Separate decision ID (proposed `D-C10y-precast`), fresh namespace `results/c10y_precast_diag/<UTC>/`, own halt diagnostic path. Never writes into, resumes, reads around or re-labels calibration 4; no result changes calibration 4's terminal outcome (§12 "No diagnostic result retroactively changes calibration 4").
- Pristine model; no behavioural evaluation (no canonical/held-out/first-token counts — measuring counts would be a calibration retry, which is not authorized). Update-level and weight-level measurements only.
- Engine and harness unmodified; the C10Y driver unmodified. The probe imports the driver's and harness's own solve functions and calls them; any capture uses read-only observation (same discipline as `docs/MATHLAB_PREREG.md` §2.3: original-code-object matching, same-dtype CPU copy then CPU cast, source-unchanged checks). If a needed quantity is a local that cannot be observed read-only, the probe must stop and report rather than re-implement it.
- GPU gate (`tools/c10w_p2_gate.py` `check_fingerprint` + `check_gpu`, fail-closed) and engine fingerprint (`tools/engine_fingerprint.py`, d941a9fb…, `_cov_cpu` 3) before model load. Hard wall-clock cap below; no in-run increase; timeout → INCONCLUSIVE. The probe takes exclusive ownership of its output directory (refuses an existing directory), records the gate and fingerprint results immediately before model load, and runs under an external deadline that covers setup through cleanup (the supervisor, not the worker, enforces it).

## Inputs (identical for both paths)
- Pinned context templates: the calibration's own set (`results/c10y_directdw_calib4/context_templates_calib.json`, SHA-256 9472b663…; verify it equals the C10Q pin c7dabbe7… under the harness's hash method, per prereg §11 Amendment P).
- Targets: calibration 4 did **not** preserve usable targets — `targets_calib.pt` is 1,261 bytes (SHA-256 1d95c75a…), the empty-payload placeholder produced by the record defect. Targets are therefore recomputed **once** in the probe with the harness's own target solve, saved (exclusive write) before any comparison, and **both** paths consume that one saved tensor set. Record that this is a new computation, not calibration 4's targets.
- Arms: A7_coined_coined (the arm whose counts moved) and A1_single as a control. Same fact order, same pinned hparams (`configs/hparams/qwen25_3b_memit_hparams.json`), same covariance caches (hashes recorded).

**Per-layer identical-input contract (BLOCKING 1).** For each arm, restore and verify the same pristine weights, initialize a fresh zero cache, and use one saved projector set and one saved target set. Pin request order, tokenized batches, padding, lookup indices, context cache and operative harness globals.

At each layer preserve the actual pre-layer state identity, K, cur, allocated residual R, P, cache C, L2, assembled solve matrix and right-hand sides from both original paths. Record dtype, shape, orientation and tensor-byte hashes. Compare corresponding operands exactly before attributing output differences to arithmetic. All controlled arithmetic variants consume the same saved recipe-A operand packet; no variant's update feeds subsequent layer inputs. Separately record any disagreement in C10Y's native capture path.

Prove observer coverage and tensor/weight inertness with observer-off/on controls; source identity alone is insufficient. Restore weights, hooks, globals and caches between arms and on failure. No behavioral evaluation is introduced.

Targets remain a **NEW COMPUTATION**: recomputed once, saved before any comparison (calibration 4's `targets_calib.pt`, 1,261 bytes, SHA-256 1d95c75a…, is the empty-payload placeholder of the persistence defect).

## Measurements (per layer 4–8, per arm)
1. **Recipe A reference:** the actual pre-cast fp32 ΔW_A as recipe A forms it (`c10e_bandknob.py:205–217`: CPU fp32 solve), captured before the fp16 cast/add.
2. **C10Y zero-step path:** the factors as `c10y_directdw_arms.py` solves them on CPU (`:238–243`), and the product as the driver forms it on the model device (MPS fp32, `:562–563`, `:635`), captured before the fp16 add.
3. **Controls.** Preserve M32, Q32 = P32 @ K32, B32 = Q32 @ R32.T, the actual direct solution, and the actual factor solution X32. Measure separately:
   (a) CPU-fp32 R32 @ X32.T, with the same factors and parenthesization as the MPS product;
   (b) CPU-float64 multiplication of promoted, already-solved fp32 factors;
   (c) genuine CPU-float64 direct and factored solves from the same saved operands, promoted before assembly, followed by their respective products;
   (d) float64 solves of the saved assembled fp32 systems, to distinguish assembly rounding from solve/product effects;
   (e) exact-input repeats of the direct solve, factor solve, CPU product and MPS product.
   Controls (b) and (c) are distinct artifacts. Explicit diagnostic-only arithmetic is permitted for these controls; it never substitutes for capturing the original reference or modifies the engine, harness or driver.
4. For every pair among the captured updates and the controls of measurement 3: relative Frobenius distance (CPU float64), max-abs and quantiles of elementwise differences, the fraction of elements that differ, and the per-column distribution over weight coordinates (update columns are weight coordinates, not fact IDs; no attribution of differences to facts is claimed).
5. **fp16 realization:** for each candidate update, W0_fp16 + cast(update) using the harness's own merge; report the relative distance of realized weights to recipe A's realized weights and the count of differing fp16 elements; byte-identity yes/no. Preserve both realized weights and realized updates `W_post − W0`, with the subtraction performed after CPU promotion. Freeze the cast/add device and order for each control. A float64 realization must not silently pass through a helper that first demotes the update to fp32 (`stored_weight`, `c10y_directdw_arms.py:287–289`, contains an explicit `.float()`).
6. Record the condition-number norm and computation method. Both paths should use the same coefficient matrix M; preserve and compare their actual matrices. Report normalized residuals for both solves against their respective saved systems, and errors relative to the float64 controls. Condition numbers are explanatory measurements, not causal verdicts.

## Pre-registered reading (threshold-free; BLOCKING 3)
All distances, repeat floors, precision changes and conditioning measurements are descriptive. No numerical magnitude threshold establishes K or S.

Evaluate in order:

- **INCONCLUSIVE:** required capture, source identity, observer validation, persistence, finiteness, resource or deadline requirements fail.
- **R:** corresponding native operands and states agree; repeats are byte-stable; CPU-fp32 multiplication of the saved C10Y factors produces recipe-A-identical realized fp16 weights in all ten arm/layer cells; MPS multiplication of those same factors produces different realized weights in at least one A7 cell. Report every cell, including A1. Interpretation: changing product device is sufficient to remove the observed weight mismatch on these newly computed inputs. This establishes neither calibration-4 causation nor an exclusive explanation of all pre-cast differences.
- **K:** reserved; not emitted by this scope. Precision convergence, residuals and conditioning may support a conditioning hypothesis, but do not uniquely identify it. Such cases are UNCLASSIFIED with the measurements attached.
- **S:** complete, validated traces directly demonstrate a discrepancy in operative inputs, state, orientation or implemented formula. A faithfully captured discrepancy is evidence; missing or untrustworthy capture is INCONCLUSIVE. Numerical distance or concentration alone cannot trigger S. An S outcome may propose a separately reviewed investigation; this measurement scope authorizes no corrective execution.
- **UNCLASSIFIED:** all remaining cases, including unresolved CPU reassociation/conditioning and mixed mechanisms.

Only R may justify proposing a CPU-fp32 product redesign. Adoption requires its own amendment, LAW#5 isolation against the required reference, implementation review and separate team admission. No label authorizes a fix, calibration 5 or stage-1 dispatch.

This classification is independent of calibration 4's observed distances. It intentionally accepts more UNCLASSIFIED outcomes; an automatic positive K verdict would need an additional, independently justified conditioning test before freeze.

## Spend (bounded; estimates labelled)
| Phase | Seconds | Source |
|---|---:|---|
| Setup: imports, fingerprint, gate, model load, pins | 600 | C10X `CAPS['setup']` (`experiments/track_c/c10x_enginepath_arms.py:36`) |
| Target solve + recipe A capture, 2 arms | 1,360 | estimate, feasibility **UNVERIFIED**: ⅔ of C10X `CAPS['A']` (2,040 s for 3 arms incl. evaluation, `c10x_enginepath_arms.py:36`). Reconciliation: C10X lists target solving separately (`CAPS['targets']` 3,600 s for 216 solves, `UNIT_PLAN` :55 ≈ 16.7 s/solve), so the 48 target solves here (24 facts × 2 arms) alone project ≈ 800 s, leaving ≈ 560 s for the two recipe-A captures without evaluation |
| C10Y factors, device and CPU products, float64 controls, repeat floor, fp16 realizations, comparisons | 300 | new estimate, feasibility **UNVERIFIED** — genuine float64 direct/factored solves (control c, d), repeats (e) and conditioning calculations at the band's matrix size may exceed it; the 2,820 s hard cap stands and a timeout is INCONCLUSIVE |
| Serialization | 180 | ASTRA attempt-3 `serialization_and_restore` allowance |
| **Sum** | **2,440** | |
| **Cap (sum × 1.15, rounded up to the minute)** | **2,820** | no in-run increase; timeout → INCONCLUSIVE |

Calibration 4's whole run (model load, LAW#3 baseline with evaluation, captures, zero-step check) took about 1,700 s wall-clock (launched 20:32:40, exited 21:01 MDT), report-only cross-check.

## Outputs (staging-only, exclusive writes)
`manifest.json` (all source/input/cache/tokenizer/context hashes, device, versions), `targets.pt` (saved before comparison), per-layer operand packets `operands_<arm>_L<l>.pt`, `updates_<arm>_L<l>.pt` for each captured/control update, `compare.json` (every statistic above), `reading.json` (the classification, produced by code from the frozen rules), `run.json`, logs. A halt writes the diagnostic JSON with the offending values.

Persist each completed target, operand packet, factor, update and computed gate input using exclusive durable phase writes before evaluating its dependent gate. Flush/fsync records; never rely on successful function return or final serialization to retain partial work. Record incomplete and NOT-RUN phases explicitly. The supervisor preserves committed artifacts and writes a fresh terminal diagnostic on timeout. Forced-halt, interrupted-phase and overwrite-refusal tests must demonstrate retained values, unchanged gate outcomes and cleanup before implementation approval.

## Explicit non-goals and refusals
No behavioural counts; no tolerance, ε, or count-allowance proposal (refused by ruling 2); no change to (ii)/(iii)/(iii-b)/(iv); no calibration 5; no backfill; no seed or input search; no reuse of calibration 4's empty placeholders as inputs.


## Fold log (v1 → v2; review `results/c10y_directdw_calib4/precast_scope_astra.md`)
| Item | Disposition | Where |
|---|---|---|
| BLOCKING 1 — per-layer identical-input contract | Astra's text appended verbatim after the Inputs list; NEW COMPUTATION label retained | §Inputs |
| BLOCKING 2 — controls conflate product precision, solve precision and order | Measurement 3 replaced verbatim by controls (a)–(e); measurement 6 replaced verbatim; measurement 5 amended verbatim incl. the `stored_weight` `.float()` demotion trap (`c10y_directdw_arms.py:287–289`) | §Measurements 3, 5, 6 |
| BLOCKING 3 — magnitude thresholds as causal classifiers | All three proposed thresholds removed; threshold-free ordered classification INCONCLUSIVE / R / K-reserved / S / UNCLASSIFIED adopted verbatim; line 6 wording replaced verbatim | §Pre-registered reading; §Why |
| BLOCKING 4 — persist-before-gate incomplete | Astra's text appended verbatim; per-layer operand packets added to the output list | §Outputs |
| ADVISORY — "one speculative fix" | Replaced: an S outcome may propose a separately reviewed investigation; no corrective execution authorized | §Pre-registered reading (S) |
| ADVISORY — cap arithmetic / 1,360 s estimate | 2,820 s hard cap kept; 1,360 s reconciled against `c10x_enginepath_arms.py:36` CAPS and :55 UNIT_PLAN; feasibility stated UNVERIFIED | §Spend |
| ADVISORY — GPU / namespace | Exclusive directory ownership, gate results recorded immediately before model load, external deadline setup→cleanup | §Boundary |
| ADVISORY — column interpretation | Fact-attribution claim dropped; columns described as weight coordinates | §Measurements 4 |

Freeze note (round-2 advisory): the fold log's "verbatim" means substantively verbatim, with typography (two apostrophes at line 21) and a citation addition (the `stored_weight` `.float()` explanation at line 38).
