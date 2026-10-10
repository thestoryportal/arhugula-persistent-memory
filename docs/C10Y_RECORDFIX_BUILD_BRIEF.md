# C10Y record-only persistence correction — build brief (D-C10y-zerostep)

Status: build brief, 2026-10-09. Builder: Codex session `codexy` (built C10Y). Reviewer: GPT-6-Astra (high) implementation review. Lead: program session.

## Authority (binding)
- Prereg `docs/C10Y_DIRECTDW_PREREG.md` §12 "Amendment ZERO-STEP-DISPOSITION — 2026-10-09" (Decision ID D-C10y-zerostep), "Persistence correction" block.
- GPT-6-Astra team ruling `results/c10y_directdw_calib4/zero_step_ruling_astra.md`, ruling 3 (read it in full). Where this brief and the ruling disagree, the ruling wins.
- This is a **record-only** correction. It authorizes **no** calibration 5 and no stage-1 dispatch, and it is necessary but **not sufficient** for any future admission.

## The defect (confirmed, all four calibrations)
`law5_calib.json`, `ledger_calib.json`, `overlap_audit_calib.json` and `step0_calib.json` contain `{}\n` in calib1–calib4 (same SHA-256 `ca3d163b…`). Causal chain (`experiments/track_c/c10y_directdw_arms.py`, read it with `cat -n` before editing — LAW#4):
- the calibration caller initialises `prefix={}` (~:1359) and replaces it only when `instrument_prefix` returns (~:1365–1366);
- `instrument_prefix` accumulates `ledger`, `targets`, `target_audits`, `checks`, `law5`, `step0` as locals (~:2498–2501) and raises on a gate failure before returning;
- `persist_prefix` (~:1303–1315) then writes `prefix.get(key, {})` — manufacturing empty placeholders and losing the baseline rows, the (ii) capture floor/distances, the partial ledger, the overlap audit and any parity records, plus the offending gate inputs.

## What to build
1. Persist **already computed** records and the offending gate inputs **before** each validating gate, using immutable phase records (one exclusively created file per completed phase, or an equivalent explicit partial-record scheme). Do **not** permanently freeze an early incomplete aggregate under the final record names.
2. Use the existing exclusive durable-write primitives (`write_json` / `save_tensors`, ~:124–132: `open('x')`, flush, fsync; `EXISTING-ARTIFACT` refusal).
3. Every record a halted run did not reach is written with an explicit status — `NOT-RUN` or `INCOMPLETE` plus the phase that halted — **never** `{}` and never a value that reads as passed.
4. Preserve offending inputs and the gate outcome exactly; cleanup/restore behaviour unchanged.
5. Apply to the calibration path and to the stage paths that share `persist_prefix` / `instrument_prefix`.

## Out of scope (refuse)
No recomputation of solves, no new numerical diagnostics (the pre-cast comparison is a separate, unfrozen scope: `docs/C10Y_PRECAST_DIAG_SCOPE.md`), no changes to any gate, tolerance, statistic, count rule or threshold, no historical backfill of calib1–4, no edits to the prereg, no GPU, no model load, no commits.

## Tests (write first; `experiments/track_c/c10y_directdw_selftest.py` style)
- Forced halt at each gate that can fire inside `instrument_prefix` (at least: LAW#3 baseline, (ii) capture floor, (iii) zero-step identity, (iii-b), the memory floor): the run directory then holds loadable records whose values are identical to what was computed before the halt, the offending gate inputs, and explicit NOT-RUN/INCOMPLETE markers for unreached phases; the halt code and diagnostic are unchanged.
- Overwrite refusal: a pre-existing artifact of any of these names makes the write halt with `EXISTING-ARTIFACT`; nothing is overwritten.
- Success path: a fixture run that passes all gates produces the same final records (names, schema, values) as before the change, apart from the added phase records.
- Cleanup: weights/hooks/caches restored after every forced halt exactly as before.
- The full existing selftest suite still passes; report its counts before and after.

## Acceptance
All tests above pass; diff confined to persistence/serialization and its tests; no numeric code path changed (state how you verified that, e.g. a diff-scope check plus an unchanged-output fixture comparison); a short report at `results/c10y_directdw_calib4/recordfix_build_report.md` with a requirement → test → implementation table keyed to ruling 3, full test output, and every deviation.

## Bad output looks like
- Still writing `{}` (or `[]`, `null`) for a phase that did not run.
- Catching the gate exception to "finish" the phase, or reordering so a gate runs after its record is overwritten.
- Recomputing distances or adding new statistics "while you are there".
- Writing the final `ledger_calib.json` early and then appending to it (mutable record).
- Backfilling calib1–4 from logs.
