VERDICT: PASS

# Lab View v2 phase 1, fix round 5: decorrelated design review (round 6)

The reviewer is the same fresh subagent that wrote r3–r5. It has no build context and edited no source file.

**Verdict:** PASS. The browser run completed with no errors. All 16 applicable acceptance criteria pass, and every one matches or beats its r3 value. r2 BLOCKING #5 is closed: none of the 160 screenshots shows the skip link. r2 advisory #9 stays closed. The canonical proof file says `complete: true`.

## Evidence

- **Build** (commit `1cf4e96`): `.venv/bin/python -B tools/labviz/build.py` exited 0: "1465 cards, 382 surveyed folders/groups", 9.45 s.
- **Browser run:** `results/labviz/review/20261008T130913325Z/`, run with the same cwd and env as r3. **Exit 0.**
  - Engines: Chromium 149.0.7827.55 and WebKit 26.5.
  - Coverage: 150 measured screens, **160 of 160 PNGs**.
  - Errors: 0 viewport or screen errors, 0 task errors, 0 console errors, 0 failed requests.
- **Canonical proof:** `results/labviz/review/v2-build/browser-tests.json` has `complete: true`. Its `measure_file` points at this run. In both engines, `browser_assertions` has `picker_selection_complete`, `non_c10_content`, `selection_carries` and `diagram_label_persists` all true, and font fixtures `[false,false,true]`.
- **Tests,** run serially:
  - Node: `test_fix_*.cjs` gives **100 pass, 0 fail**.
  - Python: `tools.labviz.test_labviz` gives **`Ran 62 tests in 115.098s — OK`**. The four proof-dependent tests that failed in r4 and r5 now pass.

## r2 BLOCKING #5: skip link in screenshots

**CLOSED.**
- `screenshot_checks`: 160 entries. All have `scroll_y` = 0 and `body_focused` = true. None has the skip link inside the page (`skip_link_page_bottom_px` > 0 in 0 cases).
- The measurements show no skip-link text inside the viewport on any of the 150 screens.
- The pixel scan of all 160 PNGs (`skipscan.cjs`, as in r3–r5) flagged 20 spots. All 20 are pressed toggles in the accent colour:
  - "2D recorded layers" on every `model-2d`;
  - "Learn" on every `learn`.
- I checked 12 of those flagged spots in a crop montage, covering every Chromium model-2d and learn flag plus two WebKit flags. None is the skip link.
- I also looked at the top 1,100 px of 6 Chromium screenshots that showed the link in r3 or failed in r5: `desktop-map-c10-focus`, `phone-line-viability`, `narrow-run-c10v-b-a7`, `landscape-compare`, `phone-learn` and `phone-map-c10-greyscale`. All six are clean.
- **Skip-link PNGs: 0 of 160** (r3: 98 of 160).

## r2 advisory #9: 3D-failure toggle state

**Still CLOSED.** In every `model-2d` screenshot, taken with the CDN blocked, "2D recorded layers" is the pressed toggle and "3D structure" is not (flag crops above). This agrees with the r4 rendered probe.

## Full regression check (r6 vs r3)

| # | r3 | r6 | Status |
|---|---|---|---|
| 1 No horizontal scroll | 0 overflow | `scroll_width` ≤ width on 150/150 screens; phone map 390/390, narrow map 360/360 | PASS |
| 2 Frame | 5 nav items; frame on 150/150 | 5 nav items (Map, Science lines, Runs, Inside the model, Learn); breadcrumb, chip and badge on 150/150 | PASS |
| 3 Font sizes | min 13; body 16 | `minimum_rendered_font_px` 13; body ≥ 16; fixtures `[F,F,T]` in both engines | PASS |
| 4 Prose | max 70.86 | max 70.86 | PASS |
| 5 Contrast | text 5.42; 0 marks without a ≥ 3:1 paint; rings ≥ 12.83 (4,253 measured) | text 5.42; 0 marks without a ≥ 3:1 paint; rings ≥ **11.29** over **16,480** measured | PASS |
| 6 Forbidden words | 0 | 0 on run-g6.1, line-d1 and model-mistral, both engines, all sizes | PASS |
| 7 Tap counts | 2 / 2 | run→line→map 2 taps and home→C10→D1 2 taps, 10/10 | PASS |
| 8 Map focus | PASS | frame and panel unchanged; `chromium-phone-map-c10-greyscale.png` shows the C10 panel above the board | PASS |
| 9 Captions | 320 charts, 0 missing | 320 charts, 0 missing | PASS |
| 10 Picker | 50/50 | 50/50 with no error and `after_choice.run === target_run`; first position 1; ≤ 50 shown | PASS |
| 11 Landscape 3D | 0.645 | 0.645 in both engines | PASS |
| 12 Greyscale | PASS | `map-c10-greyscale` captured in 10/10 engine/size runs (r5: 6/10) | PASS |
| 13 Payload | 512,835 bytes | 514,436 bytes (data grew by 1.6 kB) | PASS |
| 14 Targets | 0 under 44 | 0 under 44 at phone and narrow widths; summary minimum 44×44 | PASS |
| 15 URL restore | 30/30 | 30/30 (restored and hash key present) | PASS |
| 16 Keyboard/touch | model-2d/model-3d/compare 0 unreached; rest inside closed `<details>` | See below | PASS |

**Criterion 16 detail:**
- **Unreached controls:** model-2d 0/33, model-3d 0/32 and compare 0/98 in all 10 engine/size runs (r5 lacked Chromium compare).
- **Probe:** it classified 32 screens (both engines, desktop and phone): 4,164 unreached controls, **all** inside closed `<details>`, 0 inside open ones.
- **Count changes:** `line-c10` is 422/457 against r3's 420/455, two more data entries, both in closed `<details>`. evaluations 182/198 and map-c10-focus 77 are unchanged.
- **Picker and sliders:** keyboard picker `selection_changed` true 10/10; touch picker 6/6; sliders move by keyboard 10/10 and by touch 6/6.

The focus-ring minimum moved from 12.83 to 11.29 only because far more rings are on screen when measured. `#event-step` now gets measured: `rgb(255,211,143)` on `rgb(25,35,49)` is 11.29:1, well above 3:1. This is better measurement coverage, not a regression.

## Remaining items (ADVISORY only, carried from r3; none blocks)

These are r3 A2–A8, unchanged and non-blocking:
- the phone run table overflows by 6 px and clips "Margin / repeat";
- some inline controls touch with no gap;
- `line-d1` shows an empty "0 dated source snapshots" expander;
- the map-c10-focus page is long and its phone drill-down opens on a column with nothing connected;
- D1 group rows have duplicate titles;
- harness ring coverage (now much improved: 16,480 measured);
- the criterion-7 path lands on the experiment page, not the era line.
