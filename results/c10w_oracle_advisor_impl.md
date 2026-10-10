Verdict: FIX-FIRST

# D-C10w-oracle: implementation review of build 6e2c168 (oracle measurement, not a route)

Reviewer: Claude Opus 5.5 (independent advisor; not the author). Date: 2026-10-07.
Spec: `docs/C10W_ORACLE_PREREG.md` FROZEN v2.2 (fb1788b; SHA-256 `2baeb4e9…c344`, matches `read.py:20` `PREREG_SHA`).
Build: `experiments/track_c/c10w_oracle_{step0,train,eval,read,selftest}.py` and `tools/run_c10w_stage.sh` at 6e2c168. No build file, spec or tracked file was modified. Every check was model-free: no torch, transformers or MPS was imported.

## The single most important fix

**The LAW#5(ii) zero-adapter check will halt the P1 preflight on every run, before any training starts.** `eval.py:113` applies the null adapter with `weight.add_(delta.to(weight.device, weight.dtype))`. Layers 4–7 of the fp16 eval model contain `-0.0` entries. These are small negative bf16 checkpoint values that underflow when the harness loads the model as fp16 (`c10e_bandknob.py:48`). Under IEEE 754, `-0.0 + (+0.0) = +0.0`, so the zero adapter changes the bytes of those entries, the band SHA-256 no longer matches the base, and `self.assert_base()` at `eval.py:239` raises "LAW#5(iii): band not restored". The P1 preflight therefore HALTs at its LAW#5(ii) step. The fix is under BLOCKING-1.

## BLOCKING

**B1. False HALT of LAW#5(ii) from signed zeros: `eval.py:113`, which trips `eval.py:239`.**
- Evidence: a raw-byte scan of `model-00001-of-00002.safetensors`, reading the `down_proj.weight` tensors of layers 4–8 (stored as BF16, with no `-0.0` in bf16). I converted bf16 to fp32 to fp16 with round-to-nearest-even, which is what torch's CPU cast does. The fp16 tensors then hold `-0.0` entries per layer as follows: L4 21, L5 9, L6 2, L7 4, L8 0. I added `+0.0` and compared SHA-256: the bytes are not identical for L4–L7.
- Failure scenario: the `p1-preflight` stage runs `run_eval`, then `e.null()`, then the zero adapter is applied, then `assert_base()` raises. That is a HALT, `HALT.json` is written in the P1 directory, and `latest_directory("p1")` refuses that directory from then on. No adapter can be trained. A rerun reproduces the HALT deterministically.
- Caveat: I reproduced the conversion with numpy, not the torch/MPS path, because torch was off-limits during the GPU run. When the GPU is free, a one-minute CPU check settles it: `w16=w.to(torch.float16); ((w16+torch.zeros_like(w16)).view(torch.int16)!=w16.view(torch.int16)).sum()` on those five tensors.
- Exact fix (inert for every nonzero delta entry, and leaves bits unchanged where the fp16 delta is zero):
  ```python
  d16 = delta.to(weight.device, weight.dtype)
  with torch.no_grad(): weight.copy_(torch.where(d16 == 0, weight, weight + d16))
  ```
  Also record the band hash before the restore (see A2), so the evidence of the bit-identity check is real.

**B2. G3 equality boundary is wrong for part of the range: `read.py:264`.**
- `round(a,2) >= round(ref,2) - 3` is computed in floating point. For 72 two-decimal values of the closed-form `described_as` A, from 64.01 to 66.99, the arm value at exactly A − 3 fails. Example: A = 64.01 and arm = 61.01 → G3 miss → `PARTIAL-CEILING-LOCALITY-COST` instead of `PASS-CEILING`. The spec's rule (§3:368, "G3 permits equality to A − 3") is violated.
- Historical A values (82.8–99.88 in `results/*.json`) fall outside the affected band, so the practical probability is low, but the rule is exact as written.
- Fix: `"G3": round(a["locality_described_as"]*100) >= round(reference["locality_described_as"]*100) - 300`.
- Verified: `DefectTests.test_G3_equality_passes_across_the_range` fails on the unmodified build ("'G3' unexpectedly found … 64.01") and passes with this fix (48/48).

**B3. No phase-projection refusal before an eval stage: `step0.py:384–388`.**
- The spec (§2.9:314, :316) says "If measurements exceed the applicable phase projection-guard limit, HALT for the existing budget ruling before spending on additional units." `guard_training_unit` (`step0.py:303–313`) runs only before training attempts. The `-eval` branch launches the eval process with no projection check.
- Scenario: preflight takes 85 min. The first four units take 38 min each, so the projection before `p1-shuf` is 85 + 152 + 38 + 190 = 465, which passes. `p1-shuf` then takes 89 min, which is under its 90-min attempt guard, with no retry. The spent-plus-eval projection is 85 + 241 + 190 = 516 > 465, yet `p1-eval` (about 3 h) starts with no recorded budget ruling. The same gap exists for `p2-eval` and `p3-eval`.
- Fix: in the eval branch, before `run_child`, compute `training_projection(phase, proof, completed, {})`. Pass it to `R.check_phase_minutes` with the same authorization or budget lookup that `guard_training_unit` uses.

**B4. HALT and INVALID paths discard the evaluation evidence: `eval.py:359`, `eval.py:433–434`, `step0.py:396–401`.**
- `R.law3(...)` raises before any record is written. `R.validate_phase(...)` runs before `R.write_json(directory/"eval.json", …)`. A validity failure therefore raises and the whole eval record is lost. Example: a positive-control miss with O-A2 at 67/72, which is an INVALID reading the spec expects the reader to produce (§3:331–345; "labels are computed by the reader only", §2.8:287).
- The dispatcher's `HALT.json` and `architecture_profile/c10w_oracle_halt_diagnostic_*.json` contain only the reason string. This violates the CLAUDE.md halt discipline: "write a diagnostic JSON … with full bug state + the offending output". It also violates §2.10, which lists `eval.json` with every readout.
- Only the harness's per-arm print lines survive, in the stage log. Per-prompt rows, probes, MMLU and the U/null evidence are gone, and a 3-hour eval would have to be rerun to diagnose.
- Fix:
  1. In `run_eval`, wrap everything after model load in `try/except`. On an exception, write `eval_halt.json` with the partial record and re-raise. The partial record is `u`, `u_detail`, `stimulus`, `law5_null` and the recipes completed so far, plus the reason.
  2. Write `eval.json` before `validate_phase`.
  3. Let `p1-project` and the reader report `INVALID` through `read_measurement`, which already maps exceptions to INVALID at `read.py:453–455`, instead of raising at `step0.py:390`.

## ADVISORY

- **A1. Trace overhead may trip the 4-h eval guard (`eval.py:293–321`).** `sys.settrace(recipe_trace)` returns the local tracer for every frame, so every Python line in every recipe is traced. That covers all probes, the MMLU-200 pass, mounted re-evaluation and the transformers forward internals. On this venv's Python 3.11.16, a pure-Python workload with this exact tracer shape ran about 11× slower (0.073 s → 0.838 s; `c10w_mut/trace_cost.py`). With a P1 eval estimate of 165–190 min against a 240-min in-process HALT, this is a real budget risk. Fix: in `recipe_trace`, on the `call` event return `recipe_trace` only when `frame.f_code` is `self.original.__code__` or `H.run_recipe.__code__`; otherwise return `None`.
- **A2. The null "after" hash is vacuous (`eval.py:244`).** It is taken after `self.restore()` at `:242`, so it always equals the base. The reader check at `read.py:311` cannot fail on real data; only `eval.py:239` actually tests bit-identity. Fix: capture `self.band_hash()` immediately after the zero application, before the restore, and record that.
- **A3. The trainer may load the model from an unhashed cache (`train.py:149–151`).** `HF_HOME` is set after `from transformers import …`, and huggingface_hub reads it at import. The trainer therefore loads from the shell's `HF_HOME` or `~/.cache/huggingface`, both of which hold Qwen2.5-3B, not from the worktree cache that step 0 hashed. Today the shell's HF_HOME and the worktree's `hf_cache` symlink resolve to the same directory, so this is latent. Fix: set `HF_HOME` (and `HF_HUB_OFFLINE`) before the import.
- **A4. The P1 budget-ruling file is not bound to anything (`step0.py:310–313`).** `authorization_P1.json` raises the P1 limit from `budget_minutes` alone, with no `recorded_by`, `recorded_at` or provenance binding. Require the same identity fields as `require_authorization`.
- **A5. The original suite's launcher-refusal test passes for the wrong reason (`selftest.py:677–689`).** It passes because no step 0 directory exists (`latest_directory("step0")` HALTs), not because P2/P3 lack authorization. Mutant M32, which removes `ensure_authorized` from the dispatcher, survived the original suite. It is killed by the proposed `test_dispatch_refuses_P2_without_authorization_before_creating_phase`.
- **A6. PASS split (b) sets a reference count (`read.py:444–446`).** It sets `reference_count` to the canonical count with status `O-A7-CANON-REFERENCE`, but §3:394 names a reference only for case (a). Reporting it is harmless. Consider `reference_status` = `REPORTED-NOT-REFERENCE` for PASS (b).
- **A7. Mutant M49 survives, with no outcome change.** The trainer's in-process LAW#3 recheck (`train.py:57`) is redundant with the verify-preflight subprocess, which recomputes `law3` from the raw record (`read.py:553`).
- **A8. An 800-step retry starts without a pre-start 90-min projection (`step0.py:372–374`).** The in-run guard (`train.py:212–216`) catches an over-90 attempt after 21 updates, at the cost of one model load. A pre-start check of 2 × the measured 400-step attempt time would avoid that load.
- **A9. Out-of-order stages permanently block a phase directory (`step0.py:396–399`, `read.py:479`).** Running a stage out of order, for example `p1-project` before `p1-eval`, writes `HALT.json` into the P1 directory and permanently blocks it. This is consistent with halt discipline, but worth a line in the operator runbook.
- **A10. The first update does nothing (`train.py:34`).** `learning_rate(0) == 0`, so update 0 is a no-op. This is consistent with "linear warm-up over 20 steps from 0". It is noted only so that "400 updates" is read as 399 effective ones.

## Spec → implementation → test trace (load-bearing items)

| Spec item | Implementation | Test (original or proposed) / mutant |
|---|---|---|
| Entry preflight, forbidden knobs, LLMDB_ROOT (§2.5:192–194) | `read.py:102–106`; called at `step0.py:216,329`, `train.py:138`, `eval.py:340`; `run_c10w_stage.sh:9–13` | `test_entry_preflight_…` |
| Fingerprint at every eval process (§2.7:240) | `step0.py:99–104`, `eval.py:353` | source only; `engine_fingerprint.py` PASS on the worktree (`d941a9fb…`, `_cov_cpu` 3) |
| Seal S1–S6 (§2.3:96–103) | `step0.py:58–86`, frozen-table check `:233–235` | original + proposed `test_each_seal_rule_is_independently_binding` (M36–M38) |
| Stage order: preflight → LAW#3 → train (§2.7:241, §2.8:260,274) | `step0.py:340–344`; trainer cert `train.py:51–68,142`; dispatch `step0.py:359` | `test_entry_preflight_…`; proposed M46 test |
| In-process order U → null → closedform → LAW#3 → oracle (§2.8:277) | `eval.py:357–364`; flags `eval.py:34` | M41 (original); proposed M39 test asserts call order `["U","null","closedform"]` |
| LAW#3 envelope, inclusive (§2.7:241–245) | `read.py:148–154`, `eval.py:224,230,359`, `train.py:57` | `test_law3_envelope_…` (M01–M05) |
| LAW#5(i) strict (§2.7:249) | `eval.py:324`, `read.py:321` | M24 |
| LAW#5(ii) bit-identity, row equality (§2.7:250) | `eval.py:234–244`, `read.py:157–169,308–311` | M40 and M30 (proposed); **B1** |
| LAW#5(iii) restore (§2.7:251) | `eval.py:35,86,280,325`, `read.py:313,319` | M42 (proposed) |
| LAW#5(v) counters (§2.7:253) | `eval.py:37–38,367`, `read.py:314–315` | original |
| LAW#5(vi) nonzero seam (§2.7:254) | `step0.py:137–171` | source only (tensor) |
| Missing adapter → HALT (§2.5:198) | `eval.py:29` | original |
| Adapter hash verified (§2.5:200) | `eval.py:98` | M43 (proposed) |
| Fit gate 456/480, 23/24; one RETRY800 (§2.4:186) | `train.py:37–39,247`; `step0.py:372–375`; `read.py:339` | M31, M48 |
| Matched-pair final steps (§2.2:54) | `step0.py:367–382`, `read.py:345–347` | original "steps" defect |
| 90-min attempt guard (§2.9:316) | `train.py:42–43,160,212–216` | M47 (proposed, fake-torch shim) |
| 40 GB driver bytes, 4-h eval (§2.9:316–318) | `read.py:109–114`; `train.py:159`; `eval.py:78–83` | original |
| Phase projection limits 465/448/327 (§2.9:314) | `step0.py:291–313` before training only | M34 (proposed); **B3** for the eval stage |
| P2/P3 require recorded authorization (§2.8:278,280,285; §8) | `step0.py:316–325,347–348`; `read.py:122–127,517–525,574`; `eval.py:349–352` | M26, M27 (original); M32, M33, M45 (proposed) |
| G1–G7 (§3:349–357, :368) | `read.py:258–272` | M06–M10; **B2** (G3 float) |
| Labels and count bands (§3:359–368) | `read.py:275–281,358–377` | M11–M15, M22 |
| Replication / -UNSTABLE (§3:370) | `read.py:380–394` | M16–M18 |
| Final-label table, P3 trigger (§3:372–384) | `read.py:408–433` | M19, M20 |
| Canonical split and routing (§3:388–397) | `read.py:397–451` | M21, M22 |
| Fresh directories, HALT reuse (§2.10:322; §5) | `read.py:96–99,474–480` | M28 (proposed) |
| Frozen prereg hash (§2.10) | `read.py:486` | M29 (proposed) |

**Engine and harness sources read with line numbers (LAW#4):**
- `c10e_bandknob.py:4`: `HF_HOME` is set before the transformers import at `:11`.
- `c10e_bandknob.py:181–221` (`my_edit`): line 216, which `eval.py:295` traces, is `with torch.no_grad():`, immediately before the fp16 application at `:217`. `upd` is bound at `:211–212`. The trace is read-only.
- `c10e_bandknob.py:415–446` (`run_law5`): sets `_LAW5_DEFAULT_CTX` at `:430` and calls the global `my_edit` at `:433`, so the wrapper delegates there (`eval.py:26`).
- `c10e_bandknob.py:458–509` (`run_recipe`): line 471 is `pre_axes = axes_pre()`, which the build uses only to time setup. The restore at `:473`, the global `my_edit` at `:489`, the hooks at `:494–495` and the final restore at `:506` match the build's assumptions.
- `c10e_bandknob.py:150–160, 162–163, 358–400, 449–455`.
- `memit_main.py:240–284`: the `get_cov` signature matches `eval.py:250`.
- `git diff HEAD -- memit_dry_run` is empty, so the engine is unmodified.

## Evidence

**Selftest (unmodified build, worktree, `.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py`):** `Ran 27 tests … OK — C10W_ORACLE_SELFTEST PASS: 27 tests` (4.7 s).

**Mutation harness:** `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut/mutate.py`. It runs against a mirror root with copied build files and symlinks for everything else. Each exact-string substitution is asserted to match once. Raw results are in `run_pristine.tsv` (original suite) and `run_proposed.tsv` (proposed suite). Both BASELINE rows PASS.

| Mutant | Target | Original suite | Proposed suite |
|---|---|---|---|
| M01 A1/A2 ≥67 | read.py:151 | killed (law3_envelope) | killed |
| M02 para_full lower bound strict | read.py:153 | killed | killed |
| M03 canon upper bound strict | read.py:153 | killed | killed |
| M04 stimulus ≤4 | read.py:149 | killed (stimulus_law5) | killed |
| M05 U leak ≤3 | read.py:150 | killed | killed |
| M06 G1 +2 | read.py:262 | killed (G1_to_G7) | killed |
| M07 G3 strict | read.py:264 | killed | killed |
| M08 G4 training frames +2 | read.py:265 | killed | killed |
| M09 G6 <4 | read.py:267 | killed | killed |
| M10 G7 ≤3 | read.py:271 | killed | killed |
| M11 band(61)=PARTIAL | read.py:276 | **SURVIVED** | killed (same_seed_band_crossing_at_61) |
| M12 FAIL at ≤30 | read.py:280 | killed | killed |
| M13 PAIRING ≥15 | read.py:366 | killed | killed |
| M14 MERGE ≥5 | read.py:369 | killed | killed |
| M15 merge exception ignores gates | read.py:372 | **SURVIVED** | killed (merge_loss_exception_requires_clean_gates) |
| M16 seed gap >16 | read.py:384 | killed | killed |
| M17 same-seed gap >11 | read.py:388 | killed | killed |
| M18 same-seed gate crossing dropped | read.py:390 | killed | killed |
| M19 P3 on LOCALITY-COST | read.py:421 | killed | killed |
| M20 final-label order swapped | read.py:431 | killed | killed |
| M21 canonical gap ≤16 | read.py:401 | killed | killed |
| M22 PASS (b) motivates steps 6–7 | read.py:446 | **SURVIVED** | killed (pass_routing_split_b) |
| M23 positive control 67 | read.py:349 | killed | killed |
| M24 LAW#5(i) ≤ | read.py:321 | killed | killed |
| M25 4-h guard strict | read.py:114 | killed | killed |
| M26 authorized flag dropped | read.py:125 | killed | killed |
| M27 certificate authorization dropped | read.py:574 | killed | killed |
| M28 HALTed directory reused | read.py:479 | **SURVIVED** | killed (latest_directory_refuses_halted_phase) |
| M29 prereg hash unchecked | read.py:486 | **SURVIVED** | killed (load_frozen_rejects_prereg_hash_mismatch) |
| M30 null hash evidence dropped | read.py:311 | **SURVIVED** | killed (null_after_hash_mismatch_invalid) |
| M31 fit gate 455 | read.py:339 | killed | killed |
| M32 dispatcher skips P2/P3 authorization | step0.py:348 | **SURVIVED** | killed (dispatch_refuses_P2_without_authorization…) |
| M33 P3 eligibility dropped | step0.py:324 | **SURVIVED** | killed (P3_entry_requires_scientific_eligibility) |
| M34 no pre-start phase guard | step0.py:370 | **SURVIVED** | killed (dispatch_refuses_training_unit_when_projection_exceeds…) |
| M35 no prior-unit check | step0.py:365 | **SURVIVED** | killed (dispatch_refuses_out_of_order_training_unit) |
| M36 S2c dropped | step0.py:71 | **SURVIVED** | killed (each_seal_rule_is_independently_binding) |
| M37 S3 <0.61 | step0.py:73 | **SURVIVED** | killed (same) |
| M38 synonym list dropped | step0.py:62 | **SURVIVED** | killed (same) |
| M39 eval skips LAW#3 | eval.py:359 | **SURVIVED** | killed (eval_law3_miss_halts_before_any_oracle_recipe) |
| M40 null bit-identity assert dropped | eval.py:239 | **SURVIVED** | killed (null_application_that_changes_band_halts…) |
| M41 null/LAW#3 flags dropped | eval.py:34 | killed | killed |
| M42 entry restore assert dropped | eval.py:35 | **SURVIVED** | killed (oracle_entry_requires_restored_band) |
| M43 adapter hash unverified | eval.py:98 | **SURVIVED** | killed (adapter_hash_verified_before_load) |
| M44 eval skips certificate | eval.py:347 | **SURVIVED** | killed (eval_verifies_preflight_certificate…) |
| M45 eval skips P2 authorization | eval.py:352 | **SURVIVED** | killed (eval_P2_rechecks_authorization) |
| M46 trainer skips certificate | train.py:142 | **SURVIVED** | killed (trainer_verifies_preflight_before_torch) |
| M47 in-run projection guard dropped | train.py:216 | **SURVIVED** | killed (trainer_projection_guard_fires_after_warmup…) |
| M48 warm-up over 10 steps | train.py:34 | **SURVIVED** | killed (warmup_is_linear_over_20_steps) |
| M49 trainer LAW#3 upper bound 19 | train.py:57 | SURVIVED | SURVIVED: redundant with `read.py:553` in the verify-preflight subprocess; no outcome change (A7) |

**Totals:** 49 mutants. Under the original suite, 24 were killed and 25 survived. Under the proposed suite, 48 were killed and 1 survived (M49, not outcome-changing).

**Proposed tests:** `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut/proposed/c10w_oracle_selftest.py`.
- The file is the original suite plus a `ProposedTests` class of 20 tests and a `DefectTests` class, which runs only with `C10W_DEFECTS=1`.
- On the unmodified build: `Ran 47 tests … OK`.
- With `C10W_DEFECTS=1`: B2's test FAILs as intended. With the B2 fix applied in the mirror: `Ran 48 tests … OK`.
- The M47 test injects inert `MagicMock` stand-ins for `torch` and `transformers` into `sys.modules` for that single test and drives `time.monotonic`. It asserts that the HALT fires on the post-warm-up projection, with wall time under 30 min, rather than at the 90-min wall limit.
- B1 has no model-free test: it lives in tensor bit patterns. Its evidence is the raw-byte scan above.

**Scratch:** `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut/`, containing `mutate.py`, `run_pristine.tsv`, `run_proposed.tsv`, `proposed/`, `proposed_tests.py` and `trace_cost.py`. The worktree `git status` is unchanged apart from this file and the pre-existing `README.md` modification.
