VERDICT: FIX-FIRST

# Lab View v2 phase 1, fix round 4: decorrelated design review (round 5)

The reviewer is the same fresh subagent that wrote r3 and r4. It has no build context and edited no source file.

## Result in brief

- **WebKit is fully clean.** All 75 screens are measured. All 80 PNGs were captured at `scroll_y` 0, and none shows the skip link.
- **Chromium still fails the capture check.** On 6 screens in every viewport, Chromium is 2–87 px from the top when the capture check runs, so the run exits 2:
  - 34 Chromium PNGs are missing;
  - 30 Chromium keyboard walks are missing, including `compare`;
  - `browser-tests.json` says `complete: false`, so 4 Python tests fail.
- **The app does not regress.** Every criterion measured in this run holds at its r3 value.
- **Cause:** the site's smooth scrolling leaves an animation running from the Tab walk in Chromium. That animation overrides the instant reset one frame later.
- **Fix:** one harness line. My probe confirms it in both engines, 12/12.

## Evidence

- **Build:** exit 0, "1465 cards, 382 surveyed folders/groups", 11.09 s.
- **Browser run:** `results/labviz/review/20261008T124926101Z/` from commit `a5bb276`.
  - Engines: Chromium 149.0.7827.55 and WebKit 26.5.
  - Exit 2. `measured_screens` 150; 126 of 160 PNGs. 0 console errors, 0 failed requests, 0 task errors.
- **Chromium capture failures:** in each of the 5 Chromium viewports, `screens[name].error` = "Screenshot must start at the top of the page".

  | Screen | Residual scroll (px) |
  |---|---|
  | map-c10-focus | 15–71 |
  | line-viability | 72–87 |
  | line-c10 | 2–8 |
  | run-c10v-b-a7 | 31–72 |
  | compare | 27–41 |
  | learn | 8–12 |

  - The greyscale capture also failed in Chromium phone, narrow, landscape and 200 % (`viewports[].error`, 5–7 px).
  - Each failed capture also skips that screen's `keyboard` walk, which runs after the capture.
  - Fix round 4's local error handling worked: those screens kept their `measurements`, and the viewport kept its tasks.
- **Root-cause probe** (`r5probe.mjs`, scratch, desktop 1440×900). It replays the harness order: state A → 40 Tabs → neutral focus → state B → instant `scrollTo` → two frames.
  - **Chromium, as-is:** `scrollY` is 0 immediately after the reset, then 1, 4 or 5 on the next frame. A 30-frame trace shows `0,1,1,1,…` and `0,4,4,4,…`.
  - **Not cured by:** setting `scroll-behavior:auto` on the element at capture time, or `waitForFunction(scrollY===0)`. The animation started earlier, during the Tab walk.
  - **WebKit, as-is:** 0 everywhere.
  - **Cure:** inject `html { scroll-behavior: auto !important; }` right after load. Result: `scrollY` = 0 after two frames in 6/6 Chromium and 6/6 WebKit cases, even from 435–2,622 px down. A browser context with `reducedMotion: 'reduce'` also gives 6/6, but it also switches off the wiring pulse that a task checks (`style.css:236`), so the style tag is the better fix.
- **Tests.**
  - Node: `test_fix_*.cjs` gives 96 pass, 0 fail.
  - Python: 62 run, FAILED (failures=4): `test_v2_12`, `_14`, `_29`, `_30`. All four read `results/labviz/review/v2-build/browser-tests.json`, which is `complete: false`. Same cause as in r4; this is not an app regression.
  - Runs were serial.

## r2 BLOCKING #5: skip link in screenshots

**OPEN**, because 34 of 160 screenshots were not taken. The screenshots that were taken are clean:
- `screenshot_checks` has 126 entries. All have `scroll_y` = 0, `body_focused` = true, and the skip link entirely above the page (`skip_link_page_bottom_px` ≤ 0).
- The pixel scan (`skipscan.cjs`, as in r3/r4) flagged 15 of 126 PNGs. I checked all 15 flagged spots by eye, plus a crop montage of 12. **None is the skip link.** All are pressed toggles in the accent colour:
  - "2D recorded layers" on every `model-2d` (this also confirms r2 #9 in the harness's own screenshots: 2D is pressed);
  - "Learn" on `learn`.
- **Skip-link PNGs: 0 of 126**, against 98 of 160 in r3.

## Regression check of the 16 applicable criteria (new `measure.json` vs r3)

| # | r3 | r5 | Status |
|---|---|---|---|
| 1 No horizontal scroll at 390/360 | 0 overflow | 0 overflow on all 150 screens | holds |
| 2 Frame | 5 nav items; frame on 150/150 | 5 nav items; breadcrumb, chip and badge on 150/150 | holds |
| 3 Fonts | min 13 / body 16; fixtures `[F,F,T]` | min 13 / body 16; fixtures `[F,F,T]` in both engines | holds |
| 4 Prose | max 70.86 | max 70.86 | holds |
| 5 Contrast | text 5.42; 0 marks without a ≥ 3:1 paint; rings 12.83 | text 5.42; mark/border/focus minimum 1.06 (the same fill-only value as r3); rings 12.83 over 4,179 measured | holds |
| 6 Forbidden words | 0 | 0 hits on run-g6.1, line-d1 and model-mistral; `non_c10_content` true in both engines | holds |
| 7 Tap counts | 2 / 2 | run→line→map 2 taps and home→C10→D1 2 taps, in 10/10 viewports | holds |
| 8 Map focus | holds | measured frame, panel and tasks unchanged; the WebKit greyscale screenshot is present | holds (frame/task evidence) |
| 9 Captions | 320 charts, 0 missing | 320 charts, 0 missing | holds |
| 10 Picker | 50/50 | 50/50 `after_choice.run === target_run`; `picker_selection_complete` true in both engines | holds |
| 11 Landscape 3D | 0.645 | 0.645 in both engines | holds |
| 12 Greyscale | holds | WebKit greyscale present in 5/5 viewports; Chromium greyscale in 1/5 (desktop), missing in 4 | holds on the evidence present; Chromium evidence incomplete |
| 13 Payload | 512,835 bytes | 514,436 bytes (the data grew by 1.6 kB) | holds |
| 14 Targets | 0 under 44 | 0 under 44 at phone and narrow widths | holds |
| 15 URL restore | 30/30 | 30/30 | holds |
| 16 Keyboard/touch | model-2d/model-3d/compare 0 unreached; the rest inside closed `<details>` | model-2d 0/33 and model-3d 0/32 in 10/10 viewports. compare 0/98 in WebKit 5/5; **the Chromium compare walk is missing** (capture failure). Classified by probe on 24 screens (WebKit desktop/phone and Chromium where walked): 2,846 unreached, **all** inside closed `<details>`. `line-c10` is 422/457 (r3: 420/455, two more entries in the data, all in closed `<details>`). Keyboard picker `selection_changed` true 10/10; touch picker true 6/6; sliders pass. | holds on the evidence present; Chromium evidence incomplete for 6 screens |

No criterion regresses. The evidence for #12 and #16 is incomplete in Chromium only because the capture step failed.

## Remaining fix

### BLOCKING

1. **Stop smooth scrolling for the whole harness session, not just at capture.**
   - Change: in `tools/labviz/review.mjs` `ready()` (`:85–90`), right after the `LabView` wait, add `await page.addStyleTag({ content: 'html { scroll-behavior: auto !important; }' });`. `ready()` already runs after the first load, after each URL-reload task and on the fallback page, so every page gets it.
   - Keep the instant `scrollTo` and the `scroll_y === 0` assertion.
   - Do not change `style.css`: the readers' smooth scrolling stays as it is.
   - The probe shows 12/12 resets reach 0 with this tag.
   - Accept when `review.mjs` exits 0 with 160 `screenshot_checks`, all at `scroll_y` 0, 0 skip-link PNGs, Chromium `compare` keyboard unreached = 0, and the Python suite at 62/62 against the refreshed `browser-tests.json`.
