# LabViz stale-table fix — independent final review

**Final verdict: PROCEED.** The initial single spec-count inconsistency is now RESOLVED, as independently confirmed in the delta note below. The label and context corrections are source-faithful, and the test changes strengthen rather than weaken the existing checks.

**Most important next action:** change the remaining current registry-count claim at `docs/LABVIZ_V2_SPEC.md:321` from 54 rows to 55 rows. Keep the line in place so downstream citations do not move. Then finish the root-owned full-suite/build/report gates; this review does not infer their outcomes.

This is an independent same-family fallback with weaker independence, not Claude cross-family review. The parent reports a fresh Claude authentication probe returned exit 1/loggedIn:false. The reusable advisor prompt and CORPUS/58 were read in full. No tests, builder, server, producer, notebook, model or GPU code were run by this review; the independent checks below use stdlib file reads only.

## B1 — Remaining current spec count

`docs/LABVIZ_V2_SPEC.md:321` still describes `docs/EXPERIMENT_REGISTRY.md` as having 54 rows. Its program-wide context row is a present-tense inventory claim, not a historical result or CORPUS/54 reference. The independently counted registry now contains 55 rows. This is the only remaining relevant 54-row claim found in the spec; the other retained 54 occurrences are source line numbers, times or CORPUS identifiers. Correct this one field to make the requested count/table/spec update consistent.

## Findings supporting the implementation

1. **Historical label and documentary correction remain distinct.** Independently verified raw reader SHA-256 `b3debe4a85371902e155394e3bd054a3d214cf585a05f614e105296be022bdd9`. `results/c10x_enginepath_rerun3/reader.json:1` still has I-2 label INVALID-CONTROLS, qualifiers [], eligible false, and process reader status VALID. `CORPUS/58_C10X_ENGINEPATH.md:66–68` separately requires INVALID-CONTROLS-UNDERFIT while preserving that historical reader output. `tools/labviz/labels.json:20–21` adds both exact strings to the existing halted-invalid visual class; no prior key or mapping was changed. The grouped spec row at `docs/LABVIZ_V2_SPEC.md:497` says this is a visual class, explicitly distinguishes raw reader from erratum, cites CORPUS/58, and states not a process halt. That matches the arm-versus-process distinction at `CORPUS/58_C10X_ENGINEPATH.md:12` and the erratum's independent fit qualifier. No scientific label, qualifier, result or reader code was rewritten.

2. **The 55th context is genuine.** Exactly one registry row at `docs/EXPERIMENT_REGISTRY.md:61` names C10X-enginepath, step 6/H-11, D-C10x-enginepath, CORPUS/58 and rerun3 plus predecessor paths. CORPUS/58 :3 and :43–48 independently document that decision and process lineage. The new `tools/labviz/contexts.json:2025–2088` entry is the only added context; all previous entries compare equal to baseline. It stays DRAFT in era c10, copies the registry question, explains the raw/erratum distinction with separate JSON and documentary citations, and uses the correct control/fit bar from CORPUS/58 :66. It introduces no promoted numeric headline. Every new text citation was independently checked against its exact source line; every quote is present.

3. **Registry counts are empirically supported.** Independent stdlib line counting found **55 rows**, with field-shape distribution **36 ten-field, 17 nine-field, one eleven-field, one twelve-field**. C10X is uniquely at :61. The other spec changes correctly update 54 to 55 and 16 to 17 at the relevant inventory passages (`docs/LABVIZ_V2_SPEC.md:290`, `:987`, `:1049`, `:1097`, `:1101`, `:1107`). The spec remains 1178 lines, line 503 remains blank and the widely cited headline-missing quote at :1049 remains intact.

4. **Assertions are preserved and strengthened.** The exact label table/spec equality, recorded-label completeness and PASS-only-green assertions remain unchanged (`tools/labviz/test_labviz.py:424–429`). Added checks at :430–439 bind the raw hash, raw label and empty qualifiers, both visual mappings, plain meaning, not-process-halt qualifier and erratum citation. The sole changed existing registry assertion is exact 54 to empirically verified exact 55 (`:511`). Added checks at :512–528 require uniqueness, exact registry/table ID equality, C10X source line, CORPUS/decision/H-11, result path, DRAFT era, question identity, explicit raw/erratum citations and source-path context resolution. Existing namespace, ambiguity, unmatched-attempt and Program.validate checks remain. No skip, looser bound or weakened predicate was added.

5. **Scope is narrow.** Actual diffs comprise the two label entries, one context, relevant spec wording/counts, and stronger checks in the existing test file. The protected_before.json hash comparison returned **no drift**. No reader, renderer, builder, dashboard, shared event contract or MB producer changed within the inspected protected scope.

## Evidence boundary

Inspected existing-red.log: two selected tests ran and both failed. Inspected strengthened-red.log: the strengthened pair also both failed before table edits. These are supplied saved logs, not independently rerun test results. Root-owned targeted/full Python and Node suites, live build, dated report append and final handoff remain outside this read-only review's verified scope. No browser or scientific acceptance is claimed.

Resolve B1, then a narrow read-only confirmation suffices; no unchanged-state broad re-review is needed.

## Final narrow delta — B1 RESOLVED; PROCEED

Independently re-read `docs/LABVIZ_V2_SPEC.md:321`: it now says 55 registry rows. A read-only assertion confirms no remaining current-count phrases 54 rows / 54 registry / 54 experiment in the spec, 1178 total lines, and the blank separator at :503 preserved. This closes the only review finding.

**PROCEED** with the root-owned full Python/Node suite, live build and dated report closeout. The parent reports the strengthened targeted pair passed before this final same-line documentation correction; this reviewer did not run or infer full-suite/build results. No outstanding issue remains in the inspected four-file change. No source file was edited by this reviewer; only this review artifact was updated.
