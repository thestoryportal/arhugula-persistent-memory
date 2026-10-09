# LabViz MathLab integration — postimplementation review

**Final verdict: PROCEED.** B1 below was initially FIX-FIRST and is now RESOLVED by the narrow validator correction and independent recheck recorded at the end. The initial findings are preserved for audit.

This is independent same-family fallback review with weaker independence; Claude authentication was reported unavailable. It is not cross-family Claude review. Scope: source diff against the supplied baseline, the forward requirement and criteria packet, new fixture tests, and two small provenance mutation probes. No main build, existing suite, browser, science code, model or GPU was run.

## B1 — BLOCKING: mathlab-fold input and rule-source hash are not fully bound

`tools/labviz/cards.py:341` only checks that rule_src.file equals tools/mathlab_events.py. It does not require that file in the card's hash table, nor bind the fold input to this card's canonical events stream. The general input checker (`:315–340`) permits ordinary hashed JSON leaves; it only requires the shared-reader tag when the source path already happens to be canonical MathLab JSONL. The final hash loop (`:366`) verifies only entries present in card.sources.

Two independent temporary-fixture mutations both returned True from validate_card:

1. Remove tools/mathlab_events.py from card.sources while retaining rule_src. **MISSING_FOLD_HASH_ACCEPTED=True.** The claimed rule source is now unverified.
2. Write an ordinary sidecar JSON containing copied events with a changed halt reason, substitute it as the mathlab-fold operand using a normal JSON src leaf without reader, recompute the derived state and add the sidecar hash. **SIDECAR_FOLD_OPERAND_ACCEPTED=True.** The original eventstream remains in the card's other citations, while displayed state now derives from an invented sidecar. All supplied ordinary validation tests still pass.

This defeats the explicit criteria that the fold has only reader-resolved event operands and that its source identity/hash are binding. It does not show that the normal builder currently emits corrupted cards: the builder at `:821–822` uses the right input and source. It shows that the promised validator does not enforce that invariant.

**Minimal required fix:** for mathlab-fold, require exactly one input with src.reader=mathlab_events.read_events, src.path=.events, and src.file equal to the card's identity.name, with that name passing mathlab_source. Require rule_src.file=tools/mathlab_events.py and its presence in the source hash table. Keep the existing input re-read, recomputation and hash comparisons. Add RED negative fixtures for removed fold hash, substituted sidecar operand and a different canonical run's operand, then verify canonical card/root and mirror roundtrips remain valid.

## What the reviewed implementation already establishes

- The source reader consumes only the canonical event path pattern and calls the shared read_events; its cache contains the shared validated events and errors, with source paths normalized for the mirror (`tools/labviz/cards.py:78–90`). Fold is called through a named derived operation and JSON serialization canonicalizes integer step keys (`:120–122`). Interpretation remains in the shared module.
- MathLab staging sidecars are excluded from generic recorded JSON/log scans and applied-write population (`tools/labviz/cards.py:135`, `:434–451`, `:792`). The new card has no score headline or per-layer writes and is always labelled MATH-PROXY (`:842–858`). The builder skips score-picture generation (`tools/labviz/build.py:511`) and mirrors original JSONL, the fold source and cited Markdown (`:581–589`).
- Findings resolve against the workspace boundary before reading; outside, missing and symlink-escape cases remain explicit missing leaves. Referenced empty Markdown is included in source hashes and mirrors (`tools/labviz/cards.py:824–840`, `:863`). Unreferenced text is not mirrored by the new path.
- The production IIFE renders scope, experiment steps, stages, gates with observed values/thresholds/shared outcomes, halt, progress, resource samples, staged text and candidate ideas (`tools/labviz/app.js:559–619`). Parse errors appear before stages. Event and finding text are HTML-escaped. Model URLs route to the MathLab view; mixed comparison avoids answer-score comparison (`:625`, `:651–666`). Frame, Runs and picker labels retain the proxy boundary (`:164–168`, `:294–296`).
- Admission-only completion, aggregate PASS/FAIL/INVALID, partial inertness and successful substages use the shared folded state; no independent JS gate verdict is introduced. In particular, aggregate INVALID remains no verdict rather than cheap-stop FAIL.

## Independent verification and limits

- New Python suite: `.venv/bin/python -B -m unittest tools.labviz.test_mathlab` with temporary MPLCONFIGDIR — **11 tests OK**. Its builds are under temporary fixture roots, not the production generated site.
- New Node suite: `/opt/homebrew/bin/node --test tools/labviz/test_mathlab.cjs` — **9 tests passed**. It executes the production IIFE through a document adapter, not a real browser.
- The Python suite verifies 66 gates and two resource samples, malformed middle/torn-tail records, more than 70 reader-bound leaves, mirrored-source validation, missing/outside/symlink finding boundaries, zero score-picture calls and fixed-input warm-build bytes/mtimes.
- Protected-file hashes were compared with protected_before.json; the command result is recorded in the review conversation. No repository file was edited by this reviewer. No dashboard/producer code was imported by the tests except the shared stdlib event module; science producers were not executed.
- Browser layout/navigation, live serving, GPU behavior and scientific validity remain **UNVERIFIED**. Existing-suite and real-acceptance checks are being handled by the lead; this review makes no independent claim about those results.

Resolve B1 with a narrow test-first validator correction, then re-review that delta only.

## B1 delta re-review — RESOLVED; final PROCEED

Inspected `tools/labviz/cards.py:337–343`: mathlab-fold now requires one input with the exact `.events` reader leaf from this card's canonical identity.name, validates the canonical stream path, and requires both the exact tools/mathlab_events.py rule source and its membership in the source hash table. Existing source rereads, derived-state recomputation and byte-hash verification remain in place. This closes both demonstrated bypasses and the related cross-run substitution.

Inspected `tools/labviz/test_mathlab.py:241–262`: negative fixtures cover absent fold hash, recomputed forged sidecar events, and another canonical run's events. The saved python-binding-red.log records **three subtest failures before the fix**. Independently reran the new Python suite after the correction: **12 tests OK**, including source and evidence-mirror roundtrips and fixture-only builds. The unchanged Node suite's prior independent result remains **9 tests passed**; no unchanged renderer rerun was needed.

Protected-scope clarification from the prior hash comparison: mathlab/test_mathlab.py, tools/mathlab_admit.py and tools/mathlab_runtime.py changed concurrently relative to protected_before.json; authorship was not inferred. Dashboard and shared event-module hashes matched. This reviewer edited none of them.

**No outstanding BLOCKING issue in this bounded integration review.** Hand off the integration with MATH-PROXY limits intact. Browser/live-serving, model/GPU and science acceptance remain UNVERIFIED; parent-owned existing-suite/live-acceptance results are separate from this review. Only this review artifact was updated.

## Final renderer-only delta — PROCEED

Inspected `tools/labviz/app.js:582–583`: cheap-stop prose now requires the shared aggregate outcome FAIL, the shared step-3 state FAIL, and the shared overall status stopped: check failed. It therefore describes the fold's actual stop decision; it does not create an independent gate outcome. Inspected the production-IIFE regression at `tools/labviz/test_mathlab.cjs:107–113`, using admission-purpose step 3 and experiment-purpose step 2 fixtures. Both folded states stay running with step 3 unstarted, and neither rendered view may announce a cheap stop.

Independently ran only the two affected Node tests with --test-name-pattern='calibration PASS|outside the folded stop scope': **2 passed, 0 failed**. This also preserves the normal step-3 PASS/FAIL/INVALID positive/negative controls. The saved node-scope-red.log shows the new regression failed before the correction. No unchanged contract or broad suite was rerun.

Final bounded review verdict remains **PROCEED**, with no outstanding integration blocker. Do not describe the entire repository test suite as green: the lead reports 74 Python tests with two independently reproduced pre-integration failures (existing label-table drift and registry-count drift), plus 110/110 Node tests. Those broader baseline diagnostics and live-check.json acceptance results are lead-owned evidence, not independently rerun by this narrow review. Browser acceptance remains UNVERIFIED; the lead reports the fresh Chromium probe aborted. Only this review file was appended.
