# C10Y pre-cast comparison diagnostic — scope (DRAFT, for GPT-6-Astra freeze review)

**Status: DRAFT — NOT FROZEN, NOT AUTHORIZED.** Written 2026-10-09 under D-C10y-zerostep. Nothing here may run until GPT-6-Astra (high) freezes this scope (or an amended version) and the implementation passes review. Thresholds below marked *(proposed)* are drafts for the reviewer to fix or replace **before** any data exists.

## Why
Calibration 4 halted terminally on the zero-step identity check (iii) (prereg `docs/C10Y_DIRECTDW_PREREG.md` §12, Amendment ZERO-STEP-DISPOSITION; diagnostic `architecture_profile/c10y_halt_diagnostic_20261009T023240Z_CALIB4.json`: relative distances 1.6e-4–2.9e-4 at layers 4–8 vs tolerance 1e-4; counts 8/53/13 vs 8/52/12). GPT-6-Astra's ruling (`results/c10y_directdw_calib4/zero_step_ruling_astra.md`, ruling 1 and closing note) leaves three competing explanations open — (R) numerical reassociation/device effects, (K) solve conditioning, (S) an unisolated state/input or implementation discrepancy — and names the cheapest informative follow-up: preserve and compare the **actual** reference pre-cast update, factors and device product **on identical inputs**. This scope is that diagnostic. It distinguishes mechanisms; it does not by itself qualify any redesign (ruling closing note).

## Boundary
- Separate decision ID (proposed `D-C10y-precast`), fresh namespace `results/c10y_precast_diag/<UTC>/`, own halt diagnostic path. Never writes into, resumes, reads around or re-labels calibration 4; no result changes calibration 4's terminal outcome (§12 "No diagnostic result retroactively changes calibration 4").
- Pristine model; no behavioural evaluation (no canonical/held-out/first-token counts — measuring counts would be a calibration retry, which is not authorized). Update-level and weight-level measurements only.
- Engine and harness unmodified; the C10Y driver unmodified. The probe imports the driver's and harness's own solve functions and calls them; any capture uses read-only observation (same discipline as `docs/MATHLAB_PREREG.md` §2.3: original-code-object matching, same-dtype CPU copy then CPU cast, source-unchanged checks). If a needed quantity is a local that cannot be observed read-only, the probe must stop and report rather than re-implement it.
- GPU gate (`tools/c10w_p2_gate.py` `check_fingerprint` + `check_gpu`, fail-closed) and engine fingerprint (`tools/engine_fingerprint.py`, d941a9fb…, `_cov_cpu` 3) before model load. Hard wall-clock cap below; no in-run increase; timeout → INCONCLUSIVE.

## Inputs (identical for both paths)
- Pinned context templates: the calibration's own set (`results/c10y_directdw_calib4/context_templates_calib.json`, SHA-256 9472b663…; verify it equals the C10Q pin c7dabbe7… under the harness's hash method, per prereg §11 Amendment P).
- Targets: calibration 4 did **not** preserve usable targets — `targets_calib.pt` is 1,261 bytes (SHA-256 1d95c75a…), the empty-payload placeholder produced by the record defect. Targets are therefore recomputed **once** in the probe with the harness's own target solve, saved (exclusive write) before any comparison, and **both** paths consume that one saved tensor set. Record that this is a new computation, not calibration 4's targets.
- Arms: A7_coined_coined (the arm whose counts moved) and A1_single as a control. Same fact order, same pinned hparams (`configs/hparams/qwen25_3b_memit_hparams.json`), same covariance caches (hashes recorded).

## Measurements (per layer 4–8, per arm)
1. **Recipe A reference:** the actual pre-cast fp32 ΔW_A as recipe A forms it (`c10e_bandknob.py:205–217`: CPU fp32 solve), captured before the fp16 cast/add.
2. **C10Y zero-step path:** the factors as `c10y_directdw_arms.py` solves them on CPU (`:238–243`), and the product as the driver forms it on the model device (MPS fp32, `:562–563`, `:635`), captured before the fp16 add.
3. **Controls for mechanism:** (a) the same C10Y factors multiplied on **CPU fp32** in recipe A's operation order; (b) the C10Y product formed in CPU float64; (c) recipe A's ΔW recomputed in CPU float64; (d) the CPU repeat floor — recipe A's fp32 solve run twice on the same inputs.
4. For every pair among {ΔW_A, P_MPS, P_CPU32, P_CPU64, ΔW_A64}: relative Frobenius distance (CPU float64), max-abs and quantiles of elementwise differences, the fraction of elements that differ, and the per-column distribution (which output columns / which facts' directions carry the difference).
5. **fp16 realization:** for each candidate update, W0_fp16 + cast(update) using the harness's own merge; report the relative distance of realized weights to recipe A's realized weights and the count of differing fp16 elements; byte-identity yes/no.
6. Condition numbers of the matrices each path inverts (the solve system for recipe A; the factor system for C10Y), CPU float64.

## Pre-registered reading (proposed; reviewer to freeze before data)
Evaluated in order; first match wins.
- **INCONCLUSIVE** — any integrity/provenance failure, missing measurement, non-finite value, timeout, or failed read-only/source-unchanged check. Stop.
- **R (reassociation/device)** — P_CPU32 matches ΔW_A to within the CPU repeat floor (3d) *(proposed: relative Frobenius ≤ max(10 × floor, 1e-7))* **and** its fp16 realization is byte-identical to recipe A's on every layer, **while** P_MPS does not. Interpretation: the identity gap is introduced by forming the product on the device. This would *justify proposing* (not adopting) a later redesign: form the zero-step/merge product on CPU fp32 in recipe A's order. That redesign would need its own amendment, a LAW#5 isolation run against a known-ceiling reference, Astra freeze, and a separate team admission decision for any calibration 5.
- **K (conditioning)** — P_CPU32 does **not** match ΔW_A within the floor, the P_CPU64–ΔW_A64 gap is small *(proposed: ≤ 1e-9 relative)*, and the fp32 gaps scale with the recorded condition numbers. Interpretation: the factored fp32 solve is less accurate than the direct one on this system. No simple fix is licensed; any redesign needs independent justification.
- **S (implementation/state)** — P_CPU64 and ΔW_A64 differ materially *(proposed: > 1e-6 relative)*, or the difference concentrates in specific facts/columns independent of device and precision. Interpretation: the two paths do not compute the same mathematical update; open a bug investigation (one speculative fix after a source read, then halt), no redesign.
- **UNCLASSIFIED** — none of the above. Reported as-is; no follow-on action licensed.

## Spend (bounded; estimates labelled)
| Phase | Seconds | Source |
|---|---:|---|
| Setup: imports, fingerprint, gate, model load, pins | 600 | C10X `CAPS['setup']` (`experiments/track_c/c10x_enginepath_arms.py:36`) |
| Target solve + recipe A capture, 2 arms | 1,360 | ⅔ of C10X `CAPS['A']` = 2,040 s for 3 arms incl. evaluation (no evaluation here) — estimate |
| C10Y factors, device and CPU products, float64 controls, repeat floor, fp16 realizations, comparisons | 300 | new estimate |
| Serialization | 180 | ASTRA attempt-3 `serialization_and_restore` allowance |
| **Sum** | **2,440** | |
| **Cap (sum × 1.15, rounded up to the minute)** | **2,820** | no in-run increase; timeout → INCONCLUSIVE |

Calibration 4's whole run (model load, LAW#3 baseline with evaluation, captures, zero-step check) took about 1,700 s wall-clock (launched 20:32:40, exited 21:01 MDT), report-only cross-check.

## Outputs (staging-only, exclusive writes)
`manifest.json` (all source/input/cache/tokenizer/context hashes, device, versions), `targets.pt` (saved before comparison), `updates_<arm>_L<l>.pt` for each captured/control update, `compare.json` (every statistic above), `reading.json` (the classification, produced by code from the frozen rules), `run.json`, logs. A halt writes the diagnostic JSON with the offending values.

## Explicit non-goals and refusals
No behavioural counts; no tolerance, ε, or count-allowance proposal (refused by ruling 2); no change to (ii)/(iii)/(iii-b)/(iv); no calibration 5; no backfill; no seed or input search; no reuse of calibration 4's empty placeholders as inputs.
