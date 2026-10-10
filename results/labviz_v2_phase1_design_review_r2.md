VERDICT: FIX-FIRST

# Lab View v2 phase 1, fix round 1: decorrelated design review (round 2)

Reviewer: a fresh subagent with no build context. Judged from new measurements and screenshots only. No source file was edited.

## Evidence

- **Fresh browser run** at `results/labviz/review/20261008T102337237Z/`, made by this reviewer with `tools/labviz/review.mjs`.
  - Both engines launched with no error: Chromium 149.0.7827.55 and WebKit 26.5.
  - It covers 150 measured screens (2 engines × 5 viewports × 15 screens), 160 PNGs and 15 scripted tasks per engine and viewport.
  - Console errors: none. Failed requests: none.
  - Paths below are written `E/V/screen`, meaning `engines[name=E].viewports[viewport.name=V].screens[name=screen]`.
- **Screenshots read directly.** Tall pages were cut into tiles with ffmpeg in scratch. I looked at:
  - map, map-c10-focus and map-c10-greyscale (chromium desktop, chromium and webkit phone, webkit narrow);
  - line-c10 (desktop, four tiles from 0 to 15,800 px) and line-d1 (phone);
  - run-c10v-b-a7 (desktop), run-g6.1 (webkit phone) and compare (chromium phone);
  - model-2d (webkit phone) and model-3d (chromium landscape);
  - evaluations (desktop) and learn (webkit phone).
- **An independent picker probe** (a scratch Playwright script, phone 390×844, both engines). It typed each prefix, tapped the first matching result and polled `LabView.getState().run`. Results:

  | Engine | C10W-oracle | C10U-mint2 | G6.1 |
  |---|---|---|---|
  | Chromium | target selected after 421 ms | 139 ms | 68 ms |
  | WebKit | 456 ms | 133 ms | 75 ms |

  In every case `line` was updated to the chosen experiment.
- **Python suite:** `Ran 58 tests in 163.699s — OK`. Run after checking that no `c10w_p2_gate` process was present. The `run_c10w_p2_stage.sh p2-eval` stage was already running, not starting.
- **Builder's claims:** `results/labviz_v2_codex_impl.md` § "Fix round 1". The builder states that browser acceptance was UNVERIFIED on its side. This review is the first post-fix browser measurement.

## 17 acceptance criteria (spec §4A.4)

| # | Verdict | Evidence |
|---|---|---|
| 1 Home at 390/360: map and status strip, no horizontal scroll | **PASS** | `*/phone/map` `layout.scroll_width` is 390/390 and `*/narrow/map` is 360/360, in both engines. `chromium-phone-map.png` and `webkit-narrow-map.png` show the status strip and the "Spec layers · Column 1 of 7" drill-down. |
| 2 Same five-item nav, breadcrumb, context chip and evidence badge on every page | **PASS** | All four are present on all 150 screens (`measurements.frame`), and the frame now matches the view: `learn`/`evaluations` show breadcrumb `Map›Learn & evaluations` and chip `Learn & evaluations · all eras`; `model-mistral` shows `Map›Mistral-7B` / `Mistral-7B · model history`; `map-c10-focus` shows `Map›C10` / `C10`; `line-d1` shows `D1 capacity law`. `frame.navigation` has 6 entries, but that is a harness artifact: `measure.js:269` selects `nav [data-view]`, which also matches the breadcrumb's "Map" button. `index.html` top-nav has exactly five buttons. |
| 3 No text < 13 px; body ≥ 16 px; every width and 200 % | **PASS** | `minimum_rendered_font_px` = 13 on all 1× screens and 26 at 200 %. `body_rendered_font_px` is 17 on desktop/landscape and 16 on phone/narrow. Font fixtures give `[false,false,true]` in both engines. |
| 4 Prose ≤ 72 characters | **PASS** | `maximum_prose_characters` peaks at 70.86 in Chromium and 68.0 in WebKit (69.73 at Chromium 200 %). |
| 5 Composited contrast (text ≥ 4.5; marks, rings, borders ≥ 3) | **PASS** | Minimum text contrast is 5.42 (`run-c10v-b-a7`). `.write-mark` is now 3.31. Every mark fill below 3:1 has a ≥ 3:1 outside edge (`.fact-cell hit-0` fill 1.09 / outside 7.50; `.g-cell` 2.47 / 7.44; `.margin-mark` 2.50 / 8.94; `.write-track` 1.14 / 10.89). A per-element scan found zero sub-3 marks without such an edge. The focus ring is at least 12.83 on every visited control. The summary's 1.06 is a fill-only value. |
| 6 G6.1, D1 and Mistral content free of forbidden words; captions in own era's terms | **PASS** | 0 forbidden-word hits in `content_text` for `run-g6.1`, `line-d1` and `model-mistral` (both engines, all sizes). D1 now leads with "D1 decides the monitored variable: at a FIXED total edit count N …" plus its measure ("held-out same-relation read corruption vs concentration", `CORPUS/22…:6`). G6.1 headline: "33.3% edited-relation top-1 correctness vs truth at N=100; recorded baseline 100%" (`webkit-phone-run-g6.1.png`). Mistral uses the T-branch ceiling framing. |
| 7 Tap counts: run → line 1, map 2; Home → C10 status → D1-shared link ≤ 4 | **PASS** | `tasks["run → line → map"]` takes 2 taps (lines, then map) in 10/10 runs. `tasks["home → C10 status → shared D1 link"]` takes 2 taps in 10/10 runs. Its `c10_status` is "⛔ FALSIFIER FIRED 2026-06-25 (D-C10-1, CORPUS/35) — OPEN MUST-FIX for the fixed target.", and the link followed is "Qwen2.5-3B · shared with D1" (`[data-shared-with="corpus:22"]`). |
| 8 Map focus on C10 highlights its nodes, dims the rest, lists shared links | **PASS** | `chromium-desktop-map-c10-focus.png`: C10 experiments, D-C10* decisions, CORPUS 42–47 and models carry "● connected"; C1–C9, spec sections and layers say "not on this line's path" with a dashed hatch. The panel sits above the board and lists "Shared with other lines" with a D1-shared item first. |
| 9 Every chart has a caption and a "does not mean" line, both visible | **PASS** | 320 measured charts across all screens, engines and sizes; 0 lack a caption or a caveat, and every caveat starts "Does not mean". The Compare top caveat now has the lead. The phone map caption now describes the drill-down. |
| 10 Picker: per-keystroke filtering, ≤ 6 chars to top 10, 1 tap, ≤ 50 shown | **PASS (app)** / harness evidence defective | Keystrokes are 4/4/4/4/2, `first_experiment_position` is 1, the largest list is 50, and taps are 1 in every completed run. **But** `measure.json` records 3 Chromium `TimeoutError`s on `picker C10U-mint2` (desktop, phone, narrow: "element is not stable … detached from the DOM"). It also records `after_choice.run` ≠ the target in 13/50 picker tasks (C10W in 8/10, C10U in Chromium landscape and 200 %). The independent probe above shows the app selects the tapped run within ~0.4 s. The harness `click()` reads state after 2 animation frames, before async `chooseRun → loadCard` finishes (the C10W card is 362 KB). The late re-render then detaches the next task's results. The app passes; the evidence must be re-made (fix B2). |
| 11 Landscape 844×390: 3D canvas ≤ 70 % of the height, controls visible | **PASS** | `*/landscape/model-3d` `canvases[0].height_fraction` = 0.645 in both engines. `chromium-landscape-model-3d.png` shows the 2D/3D toggles and the "Open a layer" select directly above the canvas. The tooltip is one line and labels are thinned to every 4th layer. |
| 12 Every coloured state also carried by text or pattern (greyscale) | **PASS** | `chromium-desktop-map-c10-greyscale.png` and `webkit-phone-map-c10-greyscale.png`: connected and dimmed nodes now differ by words ("● connected" vs "not on this line's path") and by a dashed, hatched border. `chromium-desktop-run-c10v-b-a7.png`: fact cells print "3/3", "C ✓"; side effects print ✓/✕; write bars print "· written"; the configured band is a dashed outline. Label chips are text. |
| 13 First-view payload ≤ 1 MB | **PASS** | `summary.first_view_bytes` = 496,617 in all 10 engine/viewport runs: index.html 11,144 + style.css 18,196 + data.js 375,604 + app.js 91,673. |
| 14 Every target ≥ 44×44 at phone widths | **PASS** | 0 targets below 44 px at phone or narrow width in either engine. The WebKit selects `#map-preset`, `#learn-era` and `#layer-pick` are now 47 px tall (were 23). |
| 15 URL state survives reload | **PASS** | `tasks["URL run/line/compare survives reload"]`: `restored` = true and `hash_has_key` = true in 30/30 runs. |
| 16 Every control reachable by Tab with a visible ring; map, picker and slider by keyboard and touch | **FAIL** | (a) `*/model-2d` keyboard: 19 of 33 expected controls unreached, 16 of them outside closed `<details>`: `#show-2d`, `#show-3d`, `#layer-pick`, `#animate-wiring`, `#event-step`, the four `#view-content > div:nth-of-type(5) > button`s, and section data links. `model-3d`: 15 unreached outside details. `compare`: 48 unreached, all outside details. Cause: `#picker-search` renders up to 50 `#picker-results` buttons on focus (`app.js:677`). Each is its own Tab stop, so a keyboard user must press Tab 21–50 extra times to get past the picker, and the harness budget (`expected.length + 2`, `review.mjs:183`) runs out inside the list (`visited` ends at `#picker-results > button:nth-of-type(21)` / `(50)`). (b) Other screens: unreached controls are only children of closed `<details>`, which is correct. WebKit now walks with Alt+Tab. (c) Rings: every visited control has a 3 px solid ring at 12.83:1. (d) Map by keyboard and touch, and sliders by keyboard and touch (`touch_changed: true`, 0 → 30 / 0 → 362) all pass. The keyboard and touch picker steps re-select the already-current run `run-f87efa71907dc8eb`, so they do not prove a change (advisory). |
| 17 Replay/sandbox banners | **N/A** | Phase 3/4; no such view exists. |

## Prior BLOCKING items (from `labviz_v2_phase1_design_review.md`)

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Frame shows a stale context | **CLOSED** | Criterion 2 row above. |
| 2 | Chromium prose measure | **CLOSED** | Maximum 70.86 characters (was 75.02). |
| 3 | `.write-mark` contrast | **CLOSED** | 3.31:1 (was 2.84). |
| 4 | D1 caption | **CLOSED** | Criterion 6 row above. |
| 5 | C10 status and shared-D1 path | **CLOSED** | Criterion 7 row: the status is the F1 cell from `docs/F1_DETERMINATION.md:71`; "Framing review: draft" is shown separately; the D1-shared button comes first; the path takes 2 taps. |
| 6 | Greyscale map state | **CLOSED** | Criterion 12 row above. |
| 7 | WebKit select targets | **CLOSED** | 47 px tall. |
| 8 | Keyboard/touch coverage (harness) | **PARTLY OPEN** | Closed: (a) model views are now measured; (b) WebKit Alt+Tab works; (c) slider touch is reset and changes. **Open:** (a) is measured but not demonstrated, because the picker consumes the Tab budget (criterion 16). (d) Blur-before-screenshot does not work: the skip link "Skip to the view" still covers content in `chromium-desktop-map-c10-focus.png` (over "Framing review: draft"), `chromium-desktop-line-c10.png`, `chromium-desktop-evaluations.png`, `chromium-landscape-model-3d.png`, `webkit-phone-model-2d.png`, `webkit-phone-map-c10-greyscale.png` and `webkit-phone-learn.png`. In `measure.json` the skip link is inside the viewport during measurement on compare, evaluations, learn, line-viability, map-c10-focus and run-c10v-b-a7 in both engines. Those are the screens measured after a screen whose Tab cycle wrapped back to the skip link. |
| 9 | Phone horizontal overflow on line-viability | **CLOSED** | `*/phone|narrow/line-viability` scroll_width is 390/390 and 360/360. |
| 10 | Page length and IA | **PARTLY OPEN** | See below. |

**Closed under item 10:**
- Evaluations: 1,082 px desktop / 2,134 px narrow, was 26,458 / 36,653. Four collapsed era groups with counts, shown in `chromium-desktop-evaluations.png`.
- Map focus: the panel is above the board and derived links fold after 5 rows ("19 more derived document links").

**Still open under item 10:** the line pages remain flat, long lists.

| Screen | Before (desktop / phone / narrow) | Now (desktop / phone / narrow) |
|---|---|---|
| `line-c10` | 23,593 / 28,886 / 31,421 px | 20,766 / 25,765 / 28,202 px (about −12 %) |
| `line-f1-conditions` | not given | 9,402 / 14,732 / 15,679 px |
| `line-viability` | not given | 8,122 / 12,077 / 12,229 px |
| `line-d1` | not given | 4,442 / 8,856 / 9,619 px |

Problems seen in the screenshots:
- `chromium-desktop-line-c10.png`, y ≈ 2,800–9,000: after the 24-card experiment grid, "Recorded runs in this line" lists 50 uncollapsed `run-row` buttons (`app.js:303` `rows.slice(0,50)`). Their titles are just "C10V-layerpick" / "C10U-mint2". The only things that tell them apart are raw ISO timestamps and raw field paths such as `recipes.B.delta_norms.A7_coined_coined` and `law5.floor.behavior_count_deltas`, which spec line 395 named as a v1 defect.
- `line-c10` then shows a timeline that repeats about 50 of the same runs (50 "Date and source for this observation" links in `content_text`), each under a full ISO timestamp heading.
- On `chromium-phone-line-d1.png` every D1 run row's bold title is the whole CORPUS/22 paragraph in raw Markdown (`**global, relation-agnostic**`, backticks). That paragraph is repeated row after row: 144 `**` and 48 backticks in `chromium/desktop/line-d1` `content_text`. The cause is `runRow()` (`app.js:281`), which renders `entry.title` without `docText()`.

## Remaining fixes

### BLOCKING

1. **Picker is up to 50 Tab stops (criterion 16).**
   - `tools/labviz/app.js:495–505`: make the picker a single Tab stop. Render the results with `tabindex="-1"` and `role="option"` inside `role="listbox"`. In `#picker-search`, ArrowDown/ArrowUp move `aria-activedescendant` (or roving focus) and Enter picks; Escape clears.
   - Adjust `map and picker by keyboard` (`review.mjs:320–323`) to press ArrowDown instead of Tab/Alt+Tab before Enter.
   - Accept when `*/model-2d`, `*/model-3d` and `*/compare` `keyboard.unreached` contain only `details`-nested controls.
2. **Harness picker race (criterion 10 evidence).**
   - `tools/labviz/review.mjs:296`: after `click(...)`, run `await page.waitForFunction(id => window.LabView.getState().run === id, matches[0].id, { timeout: 5000 })` before recording `after_choice`. Record the wait in ms and fail the task if the target is not reached.
   - Re-run until all 50 picker tasks are error-free with `after_choice.run === matches[0].id`.
3. **Line-page length (prior #10, §4A.1 spec lines 336/344).**
   - `app.js:303`: replace the flat `rows.slice(0,50).map(runRow)` with runs grouped by experiment in collapsed `<details>` (summary: experiment name + count + best binding label). Inside each group, show 5 rows, then "Search all N in Runs".
   - Put the dated observation timeline (`scienceTimeline`) inside a closed `<details>` with a count.
   - Row secondary text should name the arm and recipe in words (e.g. "recipe B · A7 coined/coined · binding · NULL"), not raw field paths. Show dates as `2026-10-08 03:32 UTC`.
   - Target: `line-c10` ≤ 6,000 px desktop and ≤ 10,000 px narrow.
4. **Raw Markdown and repeated paragraph in run-row titles (D1/F1/T-branch).**
   - `app.js:281` `runRow()`: wrap the title in `docText(...)`.
   - In the card build (`tools/labviz/cards.py`, title for `corpus:22` trajectory cards), give D1 cards a short title (e.g. "D1 · DILUTED trajectory" / "D1 · CONCENTRATED trajectory") rather than the whole CORPUS/22 paragraph.
   - Accept when `*/line-d1`, `line-f1-conditions` and `line-t-branch` `content_text` contain no `**` or backticks.
5. **Skip link left focused in measurements and screenshots (prior #8d).**
   - `review.mjs` `tabMeasurements()` (around `:178–190`): end with `await page.evaluate(() => document.activeElement?.blur())`.
   - In `screenshot()` (`:195–199`), after the blur assert `document.activeElement === document.body` and record `active_element` in the report. If the skip link still renders, also check it with `.skip-link:not(:focus)` computed `top` before capture.
   - Accept when no `html > body > a` text node has `rect.top ≥ 0` in any screen and none of the 160 PNGs shows "Skip to the view".

### ADVISORY

6. `measure.js:269`: count only `.top-nav [data-view]` for criterion 2 (currently 6 items because the breadcrumb's "Map" is matched).
7. **Learn card shows a bare "61/72"** under C10 (`webkit-phone-learn.png`; `contexts.json` era `bar: "61/72"`). On its own it reads like a result. Label it "the line's bar: 61 of 72", or drop it, since the measure line already says "goal 61".
8. **Learn era select shows raw slugs** (`content_text`: "All eras c10 f1-conditions t-branch viability"). Use `eraLabel()` for the option text.
9. **Model 2D fallback with 3D unavailable** (`webkit-phone-model-2d.png`): `#show-3d` stays `aria-pressed="true"` while "3D unavailable … 2D view remains available" shows. In the `enhanceModel().catch` handler (`app.js:666`), reset `#show-3d` to false and `#show-2d` to true.
10. **Compare data links touch each other:** "Left run dataRight run data" (`chromium-phone-compare.png`). Add a gap or put them in a `.run-actions` row.
11. **Run-page source citations run together** without a separator: `…para_full_nresults/c10v_layerpick/run.json…` beside the NULL chip in `chromium-desktop-run-c10v-b-a7.png`, and phone `clipped_text_nodes` = 1 on `run-c10v-b-a7`. Wrap each source in its own block or add a separator.
12. **Phone nav overflows its box:** `html > body > header > nav` scroll_width 362 vs client 358 (phone) and 338 vs 328 (narrow); "Learn & evaluations" touches the button edge. Allow the label to wrap or shorten it to "Learn".
13. **Landscape map board** scrolls sideways inside `#map-board` (scroll_width 994 vs 775 at 844 px; Evidence and Models columns are off-screen). Use the phone drill-down below about 1,000 px.
14. **Status strip** still prints the raw log line ("A1_single canon=100.0 para=100.0 … kl 1.99579 ppl 21.755->19.84"). The last log line is allowed, but a one-line plain summary in front of it would help.
15. **Stale proof file:** `results/labviz/review/v2-build/browser-tests.json` still points `measure_file` at the pre-fix `20261008T084543647Z` run. The fresh run wrote its own copy in `20261008T102337237Z/`. Make `review.mjs` update one canonical location, or delete the stale pointer.
16. **Picker keyboard/touch tasks** pick the already-selected run (`run-f87efa71907dc8eb`). Start them from a different run so the change is observable.
