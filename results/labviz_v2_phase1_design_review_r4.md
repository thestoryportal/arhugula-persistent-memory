VERDICT: FIX-FIRST

# Lab View v2 phase 1, fix round 3: decorrelated design review (round 4)

Scope, as the program asked:
- r2 BLOCKING #5 (the skip link in screenshots);
- r2 advisory #9 (the 2D/3D toggle state after a 3D failure);
- a regression spot-check of the 16 criteria that passed in r3.

The reviewer is the same fresh subagent that wrote r3. It has no build context and edited no source file.

## Result in one paragraph

Fix round 3 (`bba6867`) breaks the browser run. `review.mjs` `screenshot()` now calls `window.scrollTo(0, 0)` and asserts `scroll_y === 0` two animation frames later. The site sets `html { scroll-behavior:smooth; }` (`tools/labviz/style.css:3`), so that `scrollTo` animates and the page is still mid-scroll when the assertion runs. Recorded values: 65, 98, 97, 91, 4 and 2 px. The other three viewport runs failed instead on the skip-link page-coordinate assertion, which also follows from the page not reaching the top.

The assertion fails outside the per-screen `try`, so every viewport's screen list is replaced by `[]`:
- all 10 engine/viewport runs ended "UNVERIFIED: screen sequence did not complete";
- `measured_screens` is 0, only 41 of 160 PNGs were written, and the run exited 2;
- `results/labviz/review/v2-build/browser-tests.json` now holds `complete: false`. As a direct result, 4 Python tests fail (`test_v2_12`, `_14`, `_29`, `_30`; they read that file).

The app-side fix for advisory #9 works. The skip-link approach also works when the scroll actually reaches 0: all 41 PNGs that were written are clean. The fix needed is one more harness line.

## Evidence

- **Build.** `.venv/bin/python -B tools/labviz/build.py` exited 0: "1465 cards, 382 surveyed folders/groups", 12.29 s.
- **Browser run.** `results/labviz/review/20261008T121855879Z/`: Chromium 149.0.7827.55 and WebKit 26.5, same cwd and env as r3, run under `nice`. Exit 2.
  - `engines[*].viewports[*].error.message`, Chromium: desktop "Screenshot must start at the top of the page — 65 !== 0"; phone 98; narrow 97; landscape and desktop-200pct "Skip link must stay above the full-page capture unless focused".
  - WebKit: desktop 91, narrow 4, desktop-200pct 2; phone and landscape fail on the skip-link assertion.
  - All 41 `screenshot_checks` that passed have `scroll_y` = 0.
- **Root-cause probe** (`r4probe.mjs`, in scratch): line-c10, map-c10-focus and learn, desktop and phone, both engines. The page is put at scrollY 1,200 (633 on desktop learn), then one of two calls is made, and scrollY is read two frames later.

  | Call | Chromium after 2 frames | WebKit after 2 frames |
  |---|---|---|
  | `window.scrollTo(0, 0)` (what `review.mjs:218` does) | 1199 (from 1200), 632 (from 633) | 1117–1126 (from 1200), 594 (from 633) |
  | `window.scrollTo({ top: 0, left: 0, behavior: 'instant' })` | **0** in 6/6 | **0** in 6/6 |

- **Tests.**
  - Node: `node --test --test-concurrency=1 tools/labviz/test_fix_*.cjs` gave **91 pass, 0 fail**.
  - Python: `Ran 62 tests — FAILED (failures=4)`. The four failures are `test_v2_12_non_C10_content`, `test_v2_14_readability_and_measurement_fixtures`, `test_v2_29_selection_carried_and_restored` and `test_v2_30_animation_is_labelled_diagram`.
  - Each of the four asserts a field of `results/labviz/review/v2-build/browser-tests.json` (`test_labviz.py:518–520`, `:534–535`, `:654`, `:658`). That file is now the honest `complete: false` receipt from the failed run.
  - So these failures follow from the harness defect. They are not app regressions: the same 62 passed in r3 against a complete proof.
  - Runs were serial and at low priority. A GPU job was live, as the program noted.

## Items

| Item | Status | Evidence |
|---|---|---|
| r2 BLOCKING #5: skip link in screenshots | **OPEN** (harness; the fix itself is now the defect) | The pixel scan (`skipscan.cjs`, the same scan as r3) finds **0 of 41** PNGs with the skip-link block. I checked the top 600 px of 12 of them by eye (chromium desktop line-c10 and run-c10v-b-a7, phone compare, narrow line-f1-conditions, landscape evaluations; webkit desktop line-c10 and run-g6.1, phone line-c10, model-mistral and evaluations, narrow line-viability, landscape compare): no "Skip to the view" anywhere. **But** 119 of the 160 screenshots were never taken. The acceptance in r2 and r3 ("all 160 checks at `scroll_y` 0 and no PNG shows it") cannot be met by this run. |
| r2 advisory #9: 3D-failure toggle state | **CLOSED** | Rendered with the CDN blocked (`r4probe.mjs`), Chromium and WebKit, desktop and phone, 4/4: `#show-3d` `aria-pressed="false"`, `#show-2d` `aria-pressed="true"`, the 2D background is the accent `rgb(185,198,255)` and the 3D background is `rgb(36,49,68)`, `#tower` is hidden and `#tower-fallback` is visible. `r4-webkit-phone-3dfail.png` (scratch) shows "2D recorded layers" highlighted under the "3D unavailable … 2D view remains available" message. |
| Regression spot-check of the 16 PASS criteria | **NOT POSSIBLE** from this run | `measure.json` has 0 measured screens and no `summary`, so there are no minima or `keyboard.unreached` counts to compare with r3. The r3 baseline to compare against once the run completes: font minimum 13 px and body 16 px; text contrast 5.42; prose 70.86 characters; 0 phone targets under 44 px; first view 512,835 bytes; 3D canvas height 0.645; picker 50/50; URL restore 30/30; model-2d/model-3d/compare unreached = 0; every other unreached control inside a closed `<details>` (line-c10 420, evaluations 182, map-c10-focus 77). Fix round 3 touched only `model.js:19–20` (two `setAttribute` calls) and `review.mjs`. Neither is likely to move those numbers, but that has to be measured, not assumed. |

## Remaining fix

### BLOCKING

1. **Make the pre-capture scroll instant.**
   - Change: in `tools/labviz/review.mjs:218`, replace `await page.evaluate(() => window.scrollTo(0, 0));` with `await page.evaluate(() => window.scrollTo({ top: 0, left: 0, behavior: 'instant' }));`. This overrides the CSS `scroll-behavior:smooth`; the probe shows scrollY 0 after two frames in 12/12 cases across both engines.
   - Alternatives: make the browser context reduce motion (`browser.newContext({ ..., reducedMotion: 'reduce' })`, which triggers `style.css:236`), or follow the scroll with `await page.waitForFunction(() => window.scrollY === 0)`.
   - Do not change the site's smooth scrolling. It is a reader-facing choice, and reduced-motion users already get `auto`.
   - Also: move the `screenshot(...)` calls for greyscale and model-3d inside their own `try`. A capture assertion should not wipe a whole viewport's measured screens.
   - Then re-run `review.mjs`.
   - Accept when the run exits 0, there are 160 `screenshot_checks` all at `scroll_y` 0, the pixel scan finds 0 of 160, the r3 minima and unreached counts above hold, and the Python suite passes 62/62 again against the refreshed `browser-tests.json`.
