VERDICT: FIX-FIRST

# Lab View v2 phase 1, fix round 2: decorrelated design review (round 3)

Reviewer: a fresh subagent with no build context. Every verdict below comes from this reviewer's own browser run, its screenshots and its probes. The builder's report was read only to know what was claimed. No source file was edited.

**Summary.**
- All 16 applicable acceptance criteria now PASS. Criterion 17 is N/A.
- r2 BLOCKING items 1–4 are CLOSED.
- r2 BLOCKING item 5 (the skip link in screenshots) is only half closed:
  - The app is correct. The unfocused skip link sits above the viewport in all 160 capture checks.
  - The screenshots are not. A pixel scan flagged 98 of the 160 PNGs; in 11 of the 12 flags checked by eye, "Skip to the view" is drawn over the content.
  - The cause is in the harness: `fullPage` capture of a scrolled page draws the `position:fixed` link at `scrollY − 150` in the image.
- The remaining fix is one harness line. The verdict stays FIX-FIRST only because r2's written acceptance for item 5 ("none of the 160 PNGs shows 'Skip to the view'") is not met.
- No app-side criterion fails.

## Evidence

- **Build.** `.venv/bin/python -B tools/labviz/build.py` exited 0: "1465 cards, 382 surveyed folders/groups", 10.41 s, peak RSS 833 MB.
- **Fresh browser run.** `results/labviz/review/20261008T114734498Z/`, made by `tools/labviz/review.mjs`, exited 0.
  - Engines: Chromium 149.0.7827.55 and WebKit 26.5. Both launched.
  - Coverage: 150 measured screens and 160 PNGs.
  - Errors: 0 console errors, 0 failed requests, 0 task errors and 0 screen errors in all 10 engine/viewport runs.
  - Proof file: `measure.json` is 172 MB. `results/labviz/review/v2-build/browser-tests.json` now points at this run, with `complete: true` and `task_errors: []`.
  - Path notation below: `E/V/screen` means `engines[name=E].viewports[viewport.name=V].screens[name=screen]`.
- **Reviewer probes** (scratch only, not in the repo):
  1. `probe.mjs`: for every `keyboard.unreached` control (desktop and phone, both engines), it checks in a live page whether the control sits inside a closed `<details>`.
  2. `skipscan.cjs`: a pixel scan of all 160 PNGs for the skip link's accent block (rgb 185,198,255) at the left edge. 12 of the flagged spots were checked by eye in a crop montage.
  3. `rowprobe.mjs`: opens the first run group on `line-c10` and `line-d1` and reads its rows.
- **Screenshots read directly.** Tall pages were tiled with ffmpeg.
  - Chromium desktop: map, map-c10-focus, line-c10 (whole page), run-c10v-b-a7 (tiles 0–2), model-2d, evaluations.
  - Chromium phone: map, line-d1, compare, map-c10-greyscale.
  - WebKit phone: run-g6.1, model-2d, learn.
  - Chromium landscape: model-3d.
  - WebKit desktop: map-c10-greyscale (the board tile).
- **Tests.**
  - Node: `node --test --test-concurrency=1 tools/labviz/test_fix_*.cjs` gave **87 pass, 0 fail**.
  - Python: `python -B -m unittest tools.labviz.test_labviz` gave **`Ran 62 tests in 115.921s — OK`**.
  - Process check before running Python: the only matches were two Codex build sessions, whose prompt text contains `run_c10w`. There was no GPU experiment process. All runs were serial.

## 17 acceptance criteria (spec §4A.4)

| # | Verdict | Evidence |
|---|---|---|
| 1 Home at 390/360: map and status strip, no horizontal scroll | **PASS** | `*/phone/map` `layout.scroll_width` = 390/390 and `*/narrow/map` = 360/360 in both engines. `chromium-phone-map.png` shows the status strip and the "Spec layers · Column 1 of 7" drill-down. |
| 2 Same five-item nav, breadcrumb, context chip and evidence badge on every page | **PASS** | `measurements.frame.navigation` has exactly 5 items on all 150 screens: Map, Science lines, Runs, Inside the model, Learn. Breadcrumb, context and `evidence_tier` are present on all 150. The frame matches each view. Examples from WebKit phone: `line-d1` shows "Map›D1 capacity law"; `run-g6.1` shows "Map›scale›G6.1›Selected run" / "Editing and serving viability · G6.1"; `model-mistral` shows "Map›Mistral-7B". Screenshots agree (`chromium-desktop-run-c10v-b-a7.png`, `webkit-phone-learn.png`). |
| 3 No text < 13 px; body ≥ 16 px, at every width and 200 % | **PASS** | No screen has `minimum_rendered_font_px` < 13. No screen has `body_rendered_font_px` < 16. Font fixtures give `[false,false,true]` in both engines. |
| 4 Prose ≤ 72 characters | **PASS** | The largest `maximum_prose_characters` across 150 screens is 70.86. |
| 5 Composited contrast | **PASS** | `summary.minimum_text_contrast` = 5.42. Every painted mark has at least one ≥ 3:1 paint: 0 elements have all paints below 3. Sub-3 fills such as `.g-cell chosen` (1.06) and `.fact-cell hit-0` (1.09) all carry a ≥ 3:1 outside edge. The summary's 1.06 is a fill-only value. Focus rings measured on screen: 4,253, minimum 12.83:1. |
| 6 G6.1, D1 and Mistral content free of forbidden words | **PASS** | 0 forbidden-word hits in `content_text` for `run-g6.1`, `line-d1` and `model-mistral`, in both engines at all sizes. `browser_assertions[*].non_c10_content` = true. G6.1 reads "33.3% edited-relation top-1 correctness vs truth at N=100; recorded baseline 100%" (`webkit-phone-run-g6.1.png`). D1 leads with its own question and its measure "held-out same-relation read corruption vs concentration" (`chromium-phone-line-d1.png`). |
| 7 Tap counts | **PASS** | `tasks["run → line → map"]`: 2 taps in 10/10 runs (line then map; `after_map.focus` = `exp:C10V-layerpick`). `tasks["home → C10 status → shared D1 link"]`: 2 taps in 10/10 runs. Status: "⛔ FALSIFIER FIRED 2026-06-25 (D-C10-1, CORPUS/35) — OPEN MUST-FIX…". The shared link is "Qwen2.5-3B · shared with D1" (`after_shared_link` = `model:Qwen2.5-3B`). |
| 8 Map focus on C10 | **PASS** | `chromium-desktop-map-c10-focus.png` and `webkit-desktop-map-c10-greyscale.png`, board tile: C10 is "focused"; §8.9, A7, D-C10* decisions, CORPUS 18/41/42 and Qwen2.5-3B are "● connected"; the rest are "not on this line's path" with a dashed hatch. The panel lists "Shared with other lines" with "Qwen2.5-3B · shared with D1" first. |
| 9 Every chart has a caption and a visible "does not mean" line | **PASS** | 320 measured charts, 0 missing a caption or caveat (`measurements.charts`). Confirmed in screenshots: run fact grid, written layers, side effects (`chromium-phone-compare.png`); timeline (`chromium-desktop-line-c10.png`); map; and the static wiring (`chromium-landscape-model-3d.png`). |
| 10 Picker | **PASS** | 50/50 picker tasks have no error, and `after_choice.run === target_run` in all 50. `first_experiment_position` = 1 everywhere. Keystrokes: 4 for C10V, C10W, C10U and G6.1; 2 for R5. 1 tap each. The longest list at any keystroke is 50. Results narrow on every key (C10W: 50→50→46→18). `selection_wait_ms` runs 8–283 ms. `browser_assertions[*].picker_selection_complete` = true. |
| 11 Landscape 3D canvas ≤ 70 %, controls visible | **PASS** | `*/landscape/model-3d` `layout.canvases[0].height_fraction` = 0.645 in both engines. `chromium-landscape-model-3d.png` shows the 2D/3D toggles and "Open a layer" directly above the canvas. Layer labels are HTML overlays. |
| 12 Coloured state also carried by text or pattern (greyscale) | **PASS** | `chromium-phone-map-c10-greyscale.png` and `webkit-desktop-map-c10-greyscale.png`: the states read "focused", "● connected" and "not on this line's path", with a hatched, dashed border. Run pictures print "3/3 · C ✓", "· written" and ✓/✕. The configured band is a dashed outline (`webkit-phone-model-2d.png`). |
| 13 First-view payload ≤ 1 MB | **PASS** | `summary.first_view_bytes` = 512,835 in all 10 runs. |
| 14 Targets ≥ 44×44 at phone widths | **PASS** | 0 targets below 44 px at phone or narrow width in either engine. `summary.minimum_target_width_px` and `minimum_target_height_px` are both 44. |
| 15 URL state survives reload | **PASS** | `tasks["URL run/line/compare survives reload"]`: `restored` = true and `hash_has_key` = true in 30/30 runs. |
| 16 Keyboard and touch | **PASS** | **Tab reach:** `*/model-2d`, `*/model-3d` and `*/compare` now have 0 unreached controls (r2: 19/15/48). The probe classified all remaining unreached controls on desktop and phone, in both engines, as inside closed `<details>` (e.g. line-c10 420/420, evaluations 182/182, map-c10-focus 77/77, run-c10v-b-a7 4/4); none is reachable but missed. **Rings:** every visited control has a 3 px solid outline; the on-screen minimum is 12.83:1. **Map and picker by keyboard:** `selection_changed` = true, starting from G6.1 and choosing C10V with ArrowDown/Enter. **Picker by touch:** `selection_changed` = true. **Sliders:** keyboard 0→1; touch 0→29/30 (`#training-step`) and 0→358–363 (`#event-step`). |
| 17 Replay/sandbox banners | **N/A** | Phase 3/4. |

## r2 BLOCKING items

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Picker uses up to 50 Tab stops | **CLOSED** | Criterion 16 row: model-2d, model-3d and compare have 0 unreached controls. The keyboard task picks with ArrowDown/Enter (`focused_picker_result.active_descendant` is set). |
| 2 | Harness picker race | **CLOSED** | 50/50 picker tasks are error-free, with `after_choice.run === target_run`. Every task records its wait (8–283 ms). The run exited 0. The three r2 Chromium `TimeoutError`s did not recur. |
| 3 | Line-page length | **CLOSED** | `line-c10` is 3,063 px desktop and 4,019 px narrow (target ≤ 6,000 / ≤ 10,000; r2: 20,766 / 28,202). Others, desktop/narrow: `line-f1-conditions` 3,043/4,048, `line-viability` 2,962/3,976, `line-d1` 2,431/3,138. `chromium-desktop-line-c10.png` shows the experiment groups closed with counts and best binding label; "40 more experiment groups", "17 more document links", "67 dated source snapshots" and "46 sourced decisions" are all collapsed. Opened rows read in words, for example "recipe B · A7 coined/coined · binding · NULL" and "2026-10-08 03:32 UTC" (rowprobe). |
| 4 | Raw Markdown and repeated paragraph in run-row titles | **CLOSED** | 0 `**` and 0 backticks in `content_text` on every line, run and model-mistral screen. D1 rows read "D1 · DILUTED trajectory" / "D1 · CONCENTRATED trajectory" (rowprobe). |
| 5 | Skip link left in measurements and screenshots | **OPEN (harness only)** | **Measurements: closed.** All 160 `screenshot_checks` show `body_focused` = true and the skip link's `rect.bottom` ≤ −99.66. No skip-link text node lies inside the viewport on any screen. **Screenshots: open.** The pixel scan flagged 98 of 160 PNGs. 11 of the 12 flags checked by eye are the skip link; the 12th, `*-learn` at y=610, is the pressed "Learn" toggle. Examples: `chromium-desktop-map-c10-focus.png` (y≈863, over "Multi-token value robustness"), `chromium-desktop-line-c10.png`, `chromium-desktop-model-2d.png` (over the "Inside the model" heading), `webkit-phone-learn.png`, `webkit-phone-model-2d.png` and `chromium-landscape-model-3d.png`. The scan skips the top 180 px, so the true count is higher: `chromium-phone-line-d1.png` shows it over the nav. **Cause:** `.skip-link` is `position:fixed; top:-100px; translateY(-100%)` (`style.css:193–194`). After the Tab walk, the page is left scrolled. Playwright's `fullPage` capture then draws the fixed element at document y = `scrollY − 150`. The capture check in `review.mjs` `screenshot()` tests `getBoundingClientRect().top < 0`, which is viewport-relative, so it cannot see this. A reader in a real viewport never sees the link. |

## r2 ADVISORY items (6–16)

| # | Status | Evidence |
|---|---|---|
| 6 nav count | CLOSED | `frame.navigation` has 5 items on all screens. |
| 7 Learn "61/72" | CLOSED | `webkit-phone-learn.png`: "the line's bar: 61 of 72". |
| 8 Learn era slugs | CLOSED | Learn `content_text`: "All eras / Multi-token value robustness / F1 readiness conditions / …". |
| 9 3D fallback leaves 3D pressed | **OPEN** | `webkit-phone-model-2d.png` and `chromium-desktop-model-2d.png`: "3D structure" is still highlighted (pressed) while "3D unavailable (WebGL or CDN) … 2D view remains available" shows. Cause: `model.js:144` catches the error and calls `fallback()` (`model.js:16–20`), which never resets the toggles. So the `.catch` added at `app.js:695` never runs. |
| 10 Compare links touch | CLOSED | `chromium-phone-compare.png`: "Left run data" and "Right run data" are spaced. |
| 11 Source citations run together | CLOSED for citations | Each source is on its own line (`chromium-desktop-run-c10v-b-a7.png`). The one remaining phone `clipped_text_nodes` is a table header, not a citation (see A2). |
| 12 Phone nav overflow | CLOSED | No nav scroll overflow at phone or narrow width. The fifth label is "Learn". |
| 13 Landscape map scrolls sideways | CLOSED | `*/landscape/map` `scroll_width` = 844/844, with no scrolling descendants. |
| 14 Raw status line | CLOSED | The strip leads with a plain summary ("Step 6: two engine changes … Step 7 …") before the log line. |
| 15 Stale proof file | CLOSED | `v2-build/browser-tests.json` points at `20261008T114734498Z`, `complete: true`. |
| 16 Picker tasks reselect the current run | CLOSED | Keyboard and touch tasks go from G6.1 to C10V with `selection_changed` = true. |

## Remaining fixes

### BLOCKING

1. **Skip link drawn into full-page screenshots** (r2 #5, harness only).
   - Change: in `tools/labviz/review.mjs` `screenshot()` (around `:215–229`), add `await page.evaluate(() => window.scrollTo(0, 0)); await settle(page);` after `neutralFocus(page)` and before `page.screenshot(...)`.
   - Change: make the capture check document-relative. Assert `rect.bottom + window.scrollY <= 0`, not the viewport `rect.top`. Record `scroll_y` in `screenshot_checks`.
   - Accept when `scroll_y` = 0 in all 160 checks and no PNG shows "Skip to the view".
   - Re-running the browser script is enough to close this. No app change and no new criterion review are needed.

### ADVISORY

- **A1. 3D fallback toggle state** (r2 #9, still open).
  - Change: in `tools/labviz/model.js` `fallback()` (`:16–20`), add `document.getElementById('show-3d')?.setAttribute('aria-pressed','false'); document.getElementById('show-2d')?.setAttribute('aria-pressed','true');`.
  - Alternative: rethrow at the end of the `catch` at `:144`, so that the handler at `app.js:695` runs.
  - Reason: as it stands, the pressed state tells a screen reader that 3D is showing.
- **A2. Phone run table overflows by 6 px.**
  - The table at `#view-content > section:nth-of-type(6) > div:nth-of-type(2)` is 330/324 wide, and its "Margin / repeat" header (`th:nth-of-type(7)`) is clipped. This is the `run-c10v-b-a7` phone/narrow `clipped_text_nodes` = 1.
  - Change: let the header wrap (`white-space:normal`), or reduce the cell padding at ≤ 400 px.
- **A3. Inline controls touching with no gap.**
  - Where: "Framing review: draft" next to "Data for this view" (`chromium-desktop-line-c10.png`, `chromium-phone-line-d1.png`); "Explore this era" next to "Data for this view" (`webkit-phone-learn.png`); and "Data for this view Original source Save SVG" (`webkit-phone-run-g6.1.png`, Source record panel).
  - Change: put each group in a flex row with `gap: 8px 12px`, like the `.run-actions` row used in Compare.
- **A4. Empty expander.**
  - `line-d1` shows "+ 0 dated source snapshots" (`chromium-phone-line-d1.png`).
  - Change: when the count is 0, render the "not recorded" sentence and no `<details>`.
- **A5. Map focus page length and orientation.**
  - `map-c10-focus` is 10,181 px on desktop, because five fully expanded derived chains come before the board.
  - The phone drill-down opens on "Spec layers", where every node is "not on this line's path" (`chromium-phone-map-c10-greyscale.png`).
  - A derived self-link "C10 → C10" is listed.
  - Changes: fold derived chains after 2; open the drill-down on the column that holds the focused node; drop self-links.
- **A6. D1 run group rows.**
  - One row still uses a truncated CORPUS paragraph as its title ("Spec §8.7 models drift as edge_count_since_anchor — …").
  - Several rows read the same "D1 · DILUTED trajectory".
  - Change: give every `corpus:22` card the short display title, plus a distinguishing seed/ordering/relation suffix.
- **A7. Focus-ring coverage in the harness.**
  - 12,228 visited rings are off-screen and unmeasured (`outline_measurement.limitations`: "Offset focus ring sample is outside the viewport").
  - Change: in `tabMeasurements()`, call `scrollIntoView({block:'center'})` before measuring each ring.
  - The 4,253 rings that were measured are all at least 12.83:1, so this is a harness gap, not an app defect.
- **A8. Criterion 7 path.**
  - "Open this run's science line" lands on the experiment page (`line` = `exp:C10V-layerpick`), not on the era line `era:c10`.
  - This counts as the run's line, but a breadcrumb step "Multi-token value robustness" between the experiment and Map would make the science line explicit.
