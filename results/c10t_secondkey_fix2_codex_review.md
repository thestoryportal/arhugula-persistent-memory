# D-C10t-secondkey — fix-2 review

**Verdict: PROCEED.** No blocking finding in the four dtype-placement edits. The fresh rerun plan is correct, with the selection comparison described below completed before `first`.

Reviewed the working-tree diff against HEAD, arms/read/step0, the reachable harness and engine dtype paths, the frozen preregistration, the published step-0 artifact, and the halt diagnostic/log. This is a review of the C10 write-path candidate toward F1, not a scientific verdict or readiness change.

## 1. MPS fix completeness

The diff contains exactly four replacements of `.detach().double().cpu()` with `.detach().cpu().double()` in `experiments/track_c/c10t_secondkey_arms.py:326,403,419,439`. An exact source comparison confirmed that reversing those four replacements reproduces HEAD byte for byte.

- `key_stats`: the input is now CPU before widening; its remaining `.double()` at line 338 operates on a CPU boolean mask derived from the CPU Gram matrix.
- `Collector.cur`: both direct and held-out representations move to CPU before widening. `Collector.solve` does the same for the diagnostic target copy.
- Step 0: `sentence_keys` returns CPU tensors (line 59); covariance moves to CPU before the SVD (lines 69–70). Thus `K`, `U`, `S`, `coords`, and `PK` are CPU at every widening in lines 77,85,87. Cross-template representations move to CPU in lines 111,117 before the cosine's `.double()` calls at line 120.
- The reader imports no torch. The reachable harness widens distributions already moved to CPU (`c10e_bandknob.py:84–85,105,325`); its projectors and solve are CPU. The engine's float64 solve also moves operands to CPU first (`memit/memit_main.py:191–203`). The covariance collector's optional float64 default is not reached: the frozen hparams specify `mom2_dtype="float32"`.

No remaining float64-on-MPS path was found in this scoped pass-1/pass-2 call chain.

## 2. Gate and label numbers

The edits change where widening occurs, with no arithmetic between transfer and conversion. For these fp16/fp32 representations, CPU transfer preserves values and float64 widening is exact; the subsequent diagnostic arithmetic remains CPU float64.

The four sites produce key-geometry and residual readouts. `Collector.solve` returns the original engine `z` unchanged (line 440), and `Collector.keys` returns the original `K` (line 451). These diagnostic copies do not enter the edit solve, mutate weights, or replace behavioral predictions. The reader checks diagnostic presence/population, while gate and label values come from the unchanged behavioral counts, locality probes, fit telemetry, write norms, and frozen selection rules (`read.py:269–389`). No threshold or gate-feeding numerical calculation changed.

This establishes preservation of the computation by inspection; it does not assert identical outcomes across fresh stochastic processes. The original MPS path halted before producing these readouts.

## 3. Fresh rerun and selection comparison

Use a fresh `OUT_DIR=results/c10t_secondkey_r2` for step 0 and `first`. Leave `POSITIONS` unset or point it explicitly at that directory's `step0.json`. Do not reuse the halted run's controls, marker, identity, or partial work.

This is necessary: `require_sources` rejects the old step-0 identity before model import (`arms.py:549`). The only mismatched pinned source is arms.py: recorded SHA-256 `5fbc37a7e9518cd1f66b299c7ae801f35f999983686cf28cf3657c2e40005aac`, current `897131ab5757c580012f1d81dcf8a993f7602d8df8c3c061159976708674a456`. The halted directory also contains `run.json`, so `first` refuses it. It contains neither `pass1.json` nor `pass2.json`.

Before `first`, compare parsed scientific contents against `results/c10t_secondkey/step0.json`: the ordered fact/value/token population, complete `selection`, ordered candidate-arm names, and ordered request payloads/digests. The published selection is READY, B10 only, with nonwritable counts surprisal 0 / leverage 15 and pre-/post-admission agreement 15. Its 48-request digest is `fbea3436ea41ad3f47a3f399a5b25ebdd035b3292242018c17ed3b70fff3d05d`. Record the comparison and any differences. A changed scientific selection or request payload warrants HALT before the write pass; do not silently accept or reselect it.

**A raw byte difference alone is not a halt reason across the two step-0 files.** The new source hash, UUID, timestamp, timing, and sampled contexts can differ; JSON formatting/key order can also differ without changing a selection. Compare normalized selection/request contents, not whole-file bytes. Within the new run, however, the published positions file must remain byte-identical across passes: the existing positions-file SHA-256 checks stay binding (`arms.py:568–569`; `read.py:455–458`).

## Verification

All **53/53** existing model-free selftests passed, with exit 0 and `C10T_SECONDKEY_SELFTEST_DONE`. The reviewed modules and selftest were compiled directly from current source in memory, with bytecode writes disabled. The published step-0 artifact also passed `step0_validity` with no problems. No torch/model/harness runtime was imported, and no accelerator experiment or rerun was performed; accelerator execution remains unverified by this review.
