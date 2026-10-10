# LabViz math-lab integration report

Status: **IMPLEMENTED; new integration tests PASS; two existing Python checks FAIL on current source data.** Browser acceptance remains UNVERIFIED.

Built the D-ML-1 forward requirement in `docs/LABVIZ_V2_SPEC.md:1169–1178` after the priority dashboard fixes. The LabViz reader, builder, and interface retain the existing card, citation, classic-script index, and lazy-loading idioms. To find the integration, open the existing LabViz Runs view and search `D-ML-1` or `mathlab_staging`. Static artifacts are regenerated at `results/labviz/site/`; no server or live dashboard was restarted.

## Behavior and source authority

- `tools/labviz/cards.py:78–90,120–122,815–864` reads only canonical `results/mathlab_staging/runs/*/events.jsonl` paths through `tools.mathlab_events.read_events`, then calls the shared `fold`. The entire folded state is retained as an existing typed derived leaf. LabViz adds no MathLab event schema or status file and does not reinterpret producer gate outcomes. Staging sidecar JSON and logs are excluded from generic run-state, score, scale, and latest-log ingestion.
- `tools/labviz/cards.py:307–371` validates reader-bound leaves by rerunning the shared reader, recomputes the shared fold, and verifies byte hashes. The fold operand must be this card's canonical stream, with the exact reader and `.events` path; the shared module must be present in the source hash table. Removed hashes, forged sidecar operands, and another run's operand are rejected. `.events` and `.errors` are reader-result paths, not raw JSONL or physical line references.
- `tools/labviz/cards.py:831–849,866–882` reads staged Markdown only when referenced by a validated event and resolved within the workspace boundary. Absolute and relative producer paths work. Missing, non-Markdown, outside-workspace, traversal, and symlink-escape references stay visible as missing facts. Empty referenced Markdown is still hashed and mirrored. Unreferenced staged text is not copied.
- `tools/labviz/build.py:489–520,581–589` includes MathLab metadata in the existing run index, excludes these cards from score pictures, and mirrors the original event bytes, shared reader/fold source, and cited findings. The original stream and referenced documents remain the authority; generated cards and mirrors are derived snapshots.
- `tools/labviz/app.js:293–298,559–619` shows run purpose, admission receipts separately from experiment-step completion, aggregate PASS/FAIL/INVALID, planned-gate completeness, all stages, progress, gate observations with exact thresholds/comparisons, halt reason and diagnostics, resource history, staged findings, candidate questions, and parse errors. Parse errors precede the stage display. Candidate questions are explicitly **ideas to test**. Text is escaped, and small thresholds are not rounded to zero.
- MathLab Runs, picker, run/model routes, and comparison summaries retain **MATH-PROXY** and **math estimate, not evidence**. A MathLab card has no answer-score headline, applied-write scale, or model score picture. Mixed comparisons retain the proxy boundary. The cheap-stop text requires the shared fold's actual step-3 FAIL stop state; PASS, INVALID, admission-only completion, and a failed substage outside that stop scope do not announce a cheap stop.
- `tools/labviz/README.md:8–20` documents the test commands, entry point, reader-result citations, source authority, and proxy limits.

## Tests first: RED to GREEN

Evidence is preserved in `labviz_integration_evidence_20261009/` next to this report, with byte hashes in `manifest.json`. Source diffs and the pre-integration baseline remain in the proof directory `/private/tmp/labviz-mathlab-d0x3x1mv/` as well.

| Check | RED evidence before implementation/fix | Final evidence |
| --- | --- | --- |
| Shared-reader ingestion, whole folded state, torn final line, malformed middle line, halted run, empty directory and empty stream | `python-red.log`: 9 tests, 9 failures; MathLab stream cards absent and shared-reader calls absent | `python-green.log`: 12 tests OK |
| Production JavaScript renderer, proxy labeling, scope, errors, resources, findings and candidate ideas | `node-red.log`, then `node-ui-red.log`: fixture cards/rendered MathLab UI absent | Included in `all-node-final.log`: all 110 tests pass |
| Workspace finding boundaries and empty document provenance | `python-boundary-red.log`: 11 tests, one failure; empty referenced Markdown missing from source hashes | Included in final 12 Python integration tests |
| Bind fold to the hashed shared module and this run's canonical stream | `python-binding-red.log`: one test, three failing mutation subtests | All three mutations rejected in final Python suite |
| Cheap-stop text must match shared step-3 stop scope | `node-scope-red.log`: 10 tests, nine pass, one fail; admission-purpose step 3 and experiment-purpose step 2 positive controls | All 10 new Node tests pass in final combined suite |

The fixture stream includes 66 gate records and two resource samples, a halted run, producer-shaped gate groups, admission-only completion, calibration PASS/FAIL/INVALID, and successful or partial substages. Tests verify more than 70 reader-bound leaves, mirrored-source validation, exact input preservation, finding boundary cases, escaping, zero MathLab picture calls, and identical fixed-fixture warm-build bytes and mtimes. The Node tests execute the production IIFE with a document adapter; they are not browser layout tests.

Final commands (all run through `PATH=/opt/homebrew/bin:$PATH rtk proxy`):

```sh
env MPLCONFIGDIR=/private/tmp/labviz-mathlab-d0x3x1mv/mpl \
  .venv/bin/python -B -m unittest tools.labviz.test_mathlab

env MPLCONFIGDIR=/private/tmp/labviz-mathlab-d0x3x1mv/mpl \
  TMPDIR=/private/tmp/labviz-review/test-tmp \
  .venv/bin/python -B -m unittest tools.labviz.test_labviz tools.labviz.test_mathlab

node --test --test-reporter=tap tools/labviz/test_*.cjs
```

Final output:

```text
New Python integration suite:
Ran 12 tests in 0.606s
OK

Combined existing + new Python suites:
Ran 74 tests in 267.329s
FAILED (failures=2)

Combined existing + new Node suites:
# tests 110
# pass 110
# fail 0
# cancelled 0
# skipped 0
# todo 0
```

That is **12/12 new Python tests**, **10/10 new Node tests**, **100/100 existing Node tests**, and **60/62 existing Python tests**. The two existing failures were reproduced read-only with the original pre-integration `cards.py` against the same current tables and sources (`baseline-stale-tests.json`):

1. `tools/labviz/test_labviz.py:428`, `test_v2_04_label_transcription`: `INVALID-CONTROLS` is absent from the existing label table. The live source is `results/c10x_enginepath_rerun3/reader.json`, `.arms["I-2"].label`, SHA-256 `b3debe4a85371902e155394e3bd054a3d214cf585a05f614e105296be022bdd9`.
2. `tools/labviz/test_labviz.py:501`, `test_v2_11_context_registry_rules_and_namespaces`: the current registry contains 55 rows; the test expects 54.

Neither the existing tests nor their tables, source records, spec, or registry were changed to make those checks pass. The first combined attempt also used a temporary directory outside the legacy test's documented allowlist; rerunning with the documented `/private/tmp/labviz-review/test-tmp` removed that setup failure and left only the two independently reproduced baseline failures. The entire Python suite is not green.

## Live artifact check

The production builder `.venv/bin/python -B tools/labviz/build.py` exited 0. Its measured run took 25.559524 seconds, reported 746 picture-renderer calls for existing evidence cards, and peak RSS 942,047,232 bytes on Darwin (`live-build.log`). Its printed "2226 cards" describes the existing picture output; the actual final run-card index contains **2348 cards**, including **five MathLab runs**. MathLab cards generate no score pictures. The generated `app.js` matches the final source bytes.

`live-check.json` verifies each real MB stream against the shared reader and fold, validates its card against both workspace and mirrored sources, checks the original event-byte snapshot and cited finding snapshots, and confirms the proxy labels. No producer, notebook, measurement, or model was executed by this check.

| Real run | Events | Purpose | Shared status / outcome | Gates | Stages | Resource samples | Finding refs |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| `dml2_build_acceptance_20261009T175517.460160Z` | 11 | experiment | finished / PASS | 6 | 1 | 1 | 0 |
| `admission_20261009T173935.992389Z` | 5 | admission | finished / INVALID | 1 | 0 | 0 | 1 |
| `acceptance_20261009T172912.342899Z` | 13 | experiment | halted / INVALID | 4 | 1 | 0 | 2 |
| `admission_20261009T040704.898376Z` | 5 | admission | finished / INVALID | 1 | 0 | 0 | 1 |
| `admission_20261009T035911.672726Z` | 4 | admission | finished / INVALID | 0 | 0 | 0 | 1 |

The newly available MB fixture `dml2_build_acceptance_20261009T175517.460160Z` has 11 events and an emitted experiment-step-2 PASS. Its stream SHA-256 is `9d423b33fe3475383b0c7760a4dc943475dcfb33d9496dd2a79bc0ea08b8678e`; its generated card is `run-d1e7bbf27d2b10d1`. This verifies LabViz integration with a real producer artifact; it does not independently establish MathLab measurement acceptance or scientific evidence.

The halted acceptance run keeps its exact diagnostic: `ADMISSION: Build acceptance blocked: /bin/ps permission denied; frozen section 6 forbids dispatch after inventory errors`. Admission receipts remain admission outcomes and do not complete experiment steps. All five streams have zero reader parse errors at this snapshot; the torn/invalid fixtures establish visible error behavior. Five referenced finding documents were checked as exact-byte snapshots.

## Review and verification limits

Criteria review and final implementation review are preserved as `criteria-review.md` and `review.md`. Final bounded review verdict: **PROCEED**. Review initially found an unbound fold-input/source-hash contract; the narrow correction was tested RED then GREEN and independently rechecked. The later stop-scope regression was also tested before its two-line renderer correction and independently rechecked. These were independent same-family fallback reviews with weaker independence. A fresh Claude authentication probe returned `loggedIn: false`; no Claude review is claimed.

Existing Playwright and Chromium were found and probed, with `--disable-gpu`. Chromium launched and then aborted with SIGABRT; cleanup also reported EPERM (`browser-launch.json`). No page could be opened. Browser geometry, screenshots, navigation, accessibility behavior in a browser, and visual acceptance remain **UNVERIFIED**. The Node document adapter and static-source checks do not establish those claims. No server or dashboard restart was attempted.

Fixed-input fixture warm determinism is verified. Full-site warm determinism and performance guarantees are not claimed against a concurrently changing research tree. Emitted PASS outcomes are displayed as math estimates, never promoted to scientific evidence.

## File ownership and protected audit

The LabViz implementation changed only these six source/test files, plus this report, its evidence packet, and generated LabViz artifacts. Counts below compare with captured pre-integration source snapshots (new tests compare with an empty file):

| Owned source/test file | Changed lines | Final SHA-256 |
| --- | --- | --- |
| `tools/labviz/cards.py` | +91 / -6 | `77c9f86fe0bd70871c3127f7c202a4f333791b612e89b847f73b26e2303b7c44` |
| `tools/labviz/build.py` | +6 / -2 | `68b740e1591735d29ac5ddfbf127bb4b077c972e858bce1bbcbb1f06b1cab725` |
| `tools/labviz/app.js` | +86 / -3 | `f6272c36a484394c3b0a436c22c07ab46dff98fd5ae29244238dc96c83efa421` |
| `tools/labviz/README.md` | +6 / -0 | `48c4fff7b58490d8bd867b0127cb709f952d3be55862925f7ae3b45c84214f0e` |
| `tools/labviz/test_mathlab.py` | +344 / -0 | `81989a529c5e3d440e4503f3b3c774c06c3a4f5b7e0a69c29c068c5e4a924482` |
| `tools/labviz/test_mathlab.cjs` | +170 / -0 | `9953b6851461c0c3f62459bf18c5c3c4f906cd1f7ce80a7d654dbd8ce4161366` |

Seventeen protected files were hashed before and after the LabViz phase (`protected_before.json`, `protected_final.json`). The following hashes are unchanged across this phase:

| Protected file | Unchanged SHA-256 |
| --- | --- |
| `tools/dashboard_mathlab.py` | `ba5235dd5ffd13af7f7c04e58dc0fd8b8f76302fc40a89c0247fb52114297fc7` |
| `tools/mathlab_events.py` | `1c0780d42e3cfd794b68ba742fedb0307c2992bd737507cda65bdd8a864d27a5` |
| `docs/MATHLAB_PREREG.md` | `4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507` |

Observed concurrent drift in `tools/dashboard_live.py`, `mathlab/test_mathlab.py`, `tools/mathlab_admit.py`, `tools/mathlab_harvest.py`, and `tools/mathlab_runtime.py` is preserved; their before/after hashes are recorded in `protected_final.json`. This integration did not edit those files, and the audit does not infer the author of their changes or claim that the shared tree stayed unchanged. No producer files, preregistration, or reviewed MathLab dashboard were edited during LabViz integration. Shared fold fixes belong to the earlier priority dashboard phase, documented in `observability_report.md` and `producer_changes_for_mb.md`.

Dependencies remained stdlib plus existing LabViz dependencies. No new packages were installed; no GPU/model/science measurements, commits, git mutations, service restarts, or global memory changes were performed.

Recorded UTC: 2026-10-09T18:51:22.736136+00:00

## 2026-10-09 — stale LabViz tables corrected

**Status: FIXED. Full LabViz Python 74/74 PASS; Node 110/110 PASS; live build PASS.** The two failures recorded in the initial report are now closed by source-backed table updates. No original assertion was weakened.

### Source-backed corrections

`tools/labviz/labels.json:20–21` now includes both exact labels, `INVALID-CONTROLS` and `INVALID-CONTROLS-UNDERFIT`, in the existing `halted-invalid` visual class. All prior mappings compare unchanged. The grouped spec row at `docs/LABVIZ_V2_SPEC.md:497` says in plain words that the control checks and target fit screen failed, explicitly says this is not a process halt, and distinguishes the historical reader label from the erratum with its `CORPUS/58_C10X_ENGINEPATH.md:66–68` citation. The current curated context also exposes that distinction with separate JSON and documentary citations.

The raw authority is unchanged: `results/c10x_enginepath_rerun3/reader.json`, `.arms["I-2"].label` remains `INVALID-CONTROLS`, `.qualifiers` remains `[]`, and file SHA-256 remains `b3debe4a85371902e155394e3bd054a3d214cf585a05f614e105296be022bdd9`. CORPUS/58's erratum separately reports the preregistration-compliant `INVALID-CONTROLS-UNDERFIT`: controls 64/72 and 65/72 miss the 68/72 floor, and independently only 3/24 targets meet fit ≥0.98 against the required 22/24. Neither arm advances; no mechanism or method-family conclusion is added. The pinned scientific reader, historical reading, and CORPUS entry were not edited.

The genuine 55th registry row is **C10X-enginepath**, `docs/EXPERIMENT_REGISTRY.md:61`: step 6/H-11, anchored `D-C10x-enginepath`, CORPUS/58, rerun-3 artifacts and predecessor paths. CORPUS/58 independently documents the same run and process lineage at `:3,43–48`. There are 55 unique registry IDs; the sole prior omission from the 54-entry context table was C10X. `tools/labviz/contexts.json:2025–2088` adds exactly one DRAFT `c10` context, a verbatim registry question, source-backed plain wording, control/fit bar, and separate raw-reader/erratum citations. No single numeric headline is promoted. All prior context entries and other table fields compare unchanged.

The spec's current registry/experiment counts now consistently say 55, including `:290,321,987,1049,1097,1101,1107`. The verified row shape distribution is 36 ten-field, 17 nine-field, one eleven-field, and one twelve-field row. The label row is grouped into an existing class row so the spec remains 1178 lines, the Markdown separator at :503 remains blank, and existing citation line numbers, including :1049, stay valid. All curated citations pass `Program.validate()`.

### Tests first and complete verification

Before table edits, the original two failing checks reproduced in `existing-red.log`: **2 tests, 2 failures**, 27.965s. The checks were then strengthened while the tables stayed unchanged; `strengthened-red.log` records **2 tests, 2 failures**, 23.521s: missing exact label and missing C10X context. The only changed prior expectation is the empirically justified exact row count 54 → 55. Added assertions verify raw bytes/label/empty qualifiers, both exact visual mappings, plain meaning and erratum citation, unique registry IDs, exact registry/table ID equality, C10X source/decision/H-11, result path, DRAFT era, question, raw/erratum citations, and source-path context resolution. Exact label transcription/completeness, PASS-only-green, namespace, ambiguity, unmatched-attempt, and `Program.validate()` assertions remain intact.

The strengthened pair passed after the table edits: **2 tests OK**, 21.699s. After the final same-line spec inventory correction, all LabViz Python and Node suites and the live production entry point were run. Commands used `PATH=/opt/homebrew/bin:$PATH rtk proxy`; Python used `MPLCONFIGDIR=/private/tmp/labviz-stale-0wb6b0eh/mpl`, `TMPDIR=/private/tmp/labviz-review/test-tmp`, and a fresh `PYTHONPYCACHEPREFIX` under the proof directory:

```sh
.venv/bin/python -B -m unittest tools.labviz.test_labviz tools.labviz.test_mathlab
.venv/bin/python -B tools/labviz/build.py
node --test --test-reporter=tap tools/labviz/test_*.cjs
```

```text
Python:
Ran 74 tests in 432.585s
OK

Node:
# tests 110
# pass 110
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 209.80275

Live build:
Lab View picture renderer calls: 722
Lab View: 2229 cards, 454 surveyed folders/groups; results/labviz/site/index.html
Build measurement: 29.603759 seconds; peak RSS 954204160 bytes on darwin
exit_code: 0
```

The builder's printed 2229 count is picture output; the actual generated run-card index contains **2352 cards**, including **six MathLab cards**, at this snapshot. `live-check.json` verifies the generated C10X graph node, era, source line, documentary card `run-ee73a35d571ff89b`, and the card's cited plain-words measure. The label table, context table, spec, registry, CORPUS/58 and raw reader evidence copies are all exact-byte matches to current sources. It verifies the source-bound historical label remains unchanged and validates every curated citation. This is static integration verification, not a new scientific measurement.

### Audit, review and handoff

Only the following four source/test files changed in this follow-up, plus regenerated LabViz output and this report/evidence packet:

| Source/test file | Changed lines | Final SHA-256 |
| --- | --- | --- |
| `tools/labviz/labels.json` | +2 / -0 | `b8d531ed188f4693da6b2fdba790c21ecf7961854e92b95f6099ac3b69ffc44e` |
| `tools/labviz/contexts.json` | +64 / -0 | `d54158a53938b97a3b77f0dd04a7351d909f6ed84c416f11cf0f427554e06156` |
| `tools/labviz/test_labviz.py` | +28 / -1 | `a0f9e029875f6bd1304fd50125385c46262e5fd054c472680d96777a34493358` |
| `docs/LABVIZ_V2_SPEC.md` | +8 / -8 | `c2b70b4af9364bf94dbfcdbd0223b74e5e2dc8c78173084f2f1280fc4a73cabf` |

All **23 captured protected-file hashes remained unchanged**, including the raw C10X reader, CORPUS/58, registry, existing LabViz reader/renderer/builder, shared MathLab contract/dashboard, preregistration and producer/notebook files. This is a bounded file audit, not a claim that the entire shared tree is unchanged. Worktree and branch remained `c10k-route-a` / `worktree-c10k-route-a`.

Both pre-test criteria review and final bounded implementation review returned **PROCEED**. The final review's remaining spec :321 count was corrected and independently rechecked. Review used the same-family fallback with weaker independence after a fresh Claude auth probe returned exit 1, `loggedIn:false`; no Claude review is claimed. Full-suite/build/live-check results above are lead-owned evidence, not independently rerun by those reviewers.

Proof logs, source diffs, review notes and hash receipts are preserved in `labviz_stale_fix_evidence_20261009/` next to this report; byte hashes are in `manifest.json`. The original proof directory is `/private/tmp/labviz-stale-0wb6b0eh/`. The original report prefix is preserved byte for byte, as recorded in `report_append_receipt.json`.

No commits, git mutations, server/dashboard restarts, new dependencies, model/GPU/science execution, scientific artifact edits, or global memory writes occurred. Verification covers CPU fixtures, the Node document adapter and static build/evidence snapshots. Browser acceptance remains UNVERIFIED as previously recorded.

Recorded UTC: 2026-10-09T19:25:49.837643+00:00
