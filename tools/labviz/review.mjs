/* Run from /private/tmp/labviz-review. This is a self-check, never a review verdict. */
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const SCRATCH = '/private/tmp/labviz-review';
const SITE = join(ROOT, 'results/labviz/site');
const MEASURE = join(ROOT, 'tools/labviz/measure.js');
const ENTRY = pathToFileURL(join(SITE, 'index.html')).href;
const REVIEW = join(ROOT, 'results/labviz/review');
const stamp = new Date().toISOString().replace(/[-:.]/g, '');
const OUT = join(REVIEW, stamp);
const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900, zoom: 1, touch: false },
  { name: 'phone', width: 390, height: 844, zoom: 1, touch: true },
  { name: 'narrow', width: 360, height: 780, zoom: 1, touch: true },
  { name: 'landscape', width: 844, height: 390, zoom: 1, touch: true },
  { name: 'desktop-200pct', width: 1440, height: 900, zoom: 2, touch: false }
];
const FORBIDDEN = ['of 72', 'goal 61', 'reworded', 'made-up', 'C10'];
const LABEL_CLASSES = ['pass', 'lead', 'lead-unreplicated', 'partial', 'tradeoff', 'null', 'underfit', 'control', 'halted-invalid', 'not-labelled', 'not-comparable', 'characterization', 'oracle-measurement', 'not-a-verdict', 'unknown'];
const describeError = error => ({ name: error.name, message: error.message, code: error.code ?? null });

if (resolve(process.cwd()) !== SCRATCH) throw new Error('Run this browser command only from ' + SCRATCH);
if (process.env.npm_config_cache !== join(SCRATCH, 'npm-cache')) throw new Error('npm_config_cache must stay in approved scratch');
if (process.env.PLAYWRIGHT_BROWSERS_PATH !== join(SCRATCH, 'ms-playwright')) throw new Error('PLAYWRIGHT_BROWSERS_PATH must stay in approved scratch');
process.env.TMPDIR = join(SCRATCH, 'test-tmp');
mkdirSync(process.env.TMPDIR, { recursive: true });
mkdirSync(REVIEW, { recursive: true });
mkdirSync(OUT);

const report = {
  kind: 'Lab View design self-check; measurements only; no reviewer verdict',
  entry: ENTRY,
  environment: { node: process.version, platform: process.platform, arch: process.arch, scratch: SCRATCH, tmpdir: process.env.TMPDIR, npm_cache: process.env.npm_config_cache, browser_path: process.env.PLAYWRIGHT_BROWSERS_PATH },
  requested_viewports: VIEWPORTS,
  requested_screens: ['map', 'map-c10-focus', 'line-t-branch', 'line-viability', 'line-f1-conditions', 'line-c10', 'line-d1', 'run-c10v-b-a7', 'run-g6.1', 'compare', 'model-2d', 'model-3d-when-available', 'model-mistral', 'learn', 'evaluations'],
  engines: [],
  summary: null,
  screenshots: [],
  screenshot_checks: []
};

const writeJSON = (path, value) => {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(value, null, 2) + '\n');
};

function cachedChromiumPath() {
  if (process.env.LABVIZ_CHROMIUM_EXECUTABLE) {
    const path = resolve(process.env.LABVIZ_CHROMIUM_EXECUTABLE);
    if (!path.startsWith(join(SCRATCH, 'ms-playwright') + sep)) throw new Error('Chromium executable must be under approved scratch');
    assert.ok(existsSync(path), 'Configured Chromium executable does not exist: ' + path);
    return path;
  }
  const path = join(SCRATCH, 'ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing');
  assert.ok(existsSync(path), 'Provisioned Chromium 1228 executable does not exist: ' + path);
  return path;
}

async function neutralFocus(page) {
  await page.evaluate(() => {
    document.activeElement?.blur();
    document.body.tabIndex = -1; document.body.focus(); document.body.removeAttribute('tabindex');
  });
}

async function waitForChosenRun(page, id) {
  const started = Date.now();
  await page.waitForFunction(target => window.LabView.getState().run === target, id, { timeout: 5000 });
  await settle(page);
  assert.equal((await stateOf(page)).run, id, 'Picker must finish loading the chosen run');
  return Date.now() - started;
}

async function settle(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
}

async function ready(page) {
  await page.waitForFunction(() => window.LabView && typeof window.LabView.getState === 'function', null, { timeout: 5000 });
  await page.addScriptTag({ path: MEASURE });
  await settle(page);
  await neutralFocus(page);
}

async function go(page, state) {
  await page.evaluate(async next => { await window.LabView.setState(next); }, state);
  await settle(page);
  await neutralFocus(page);
}

async function stateOf(page) {
  return page.evaluate(() => ({ ...window.LabView.getState(), hash: location.hash }));
}

async function click(page, selector, actions, method = 'click') {
  const control = page.locator(selector).filter({ visible: true }).first();
  await control.waitFor({ state: 'visible', timeout: 2000 });
  actions.push({ action: method, selector, label: (await control.textContent())?.trim() ?? '', before: await stateOf(page) });
  await control[method]();
  await settle(page);
  actions.at(-1).after = await stateOf(page);
  return control;
}

async function task(name, tasks, work) {
  const record = { name, actions: [], taps: 0, keystrokes: 0, observation: null };
  tasks.push(record);
  try { record.observation = await work(record); }
  catch (error) { record.error = describeError(error); }
  record.taps = record.actions.filter(action => ['click', 'tap'].includes(action.action)).length;
  record.keystrokes = record.actions.filter(action => action.action === 'key').reduce((sum, action) => sum + (action.count ?? 1), 0);
  return record;
}

async function firstView(page) {
  const requests = [];
  const responseReads = [];
  const entries = new Map();
  const requestListener = request => {
    const entry = { url: request.url(), resource_type: request.resourceType(), bytes: null, failure: null };
    requests.push(entry);
    entries.set(request, entry);
    if (entry.url.startsWith('file:')) {
      const path = fileURLToPath(new URL(entry.url));
      if (!path.startsWith(SITE + sep)) throw new Error('First view read outside generated site: ' + path);
      try { entry.bytes = statSync(path).size; }
      catch (error) { entry.file_error = describeError(error); }
    }
  };
  const responseListener = response => {
    if (response.url().startsWith('file:')) return;
    responseReads.push((async () => {
      const entry = entries.get(response.request());
      try { if (entry) entry.bytes = (await response.body()).length; }
      catch (error) { if (entry) entry.body_error = describeError(error); }
    })());
  };
  const failureListener = request => {
    const entry = entries.get(request);
    if (entry) { entry.failure = request.failure(); entry.bytes = 0; }
  };
  page.on('request', requestListener);
  page.on('response', responseListener);
  page.on('requestfailed', failureListener);
  await page.goto(ENTRY, { waitUntil: 'load', timeout: 15000 });
  await ready(page);
  await Promise.all(responseReads);
  page.off('request', requestListener);
  page.off('response', responseListener);
  page.off('requestfailed', failureListener);
  const files = Array.from(new Map(requests.map(entry => [entry.url, entry])).values());
  return { requests, distinct_files: files, first_view_bytes: files.every(file => file.bytes !== null && !file.file_error && !file.body_error) ? files.reduce((sum, file) => sum + file.bytes, 0) : null, known_bytes: files.reduce((sum, file) => sum + (file.bytes ?? 0), 0) };
}

async function fontFixtures(browser) {
  const page = await browser.newPage({ viewport: { width: 500, height: 250 } });
  try {
    await page.setContent('<div id="large-leading" style="font-size:12px;line-height:96px">twelve</div><svg width="100" height="30" viewBox="0 0 200 60"><text id="scaled-svg" x="2" y="24" style="font-size:16px">sixteen</text></svg><svg width="100" height="30" viewBox="0 0 100 30"><text id="unscaled-svg" x="2" y="20" style="font-size:13px">thirteen</text></svg>');
    await page.addScriptTag({ path: MEASURE });
    const sizes = await page.evaluate(() => ['large-leading', 'scaled-svg', 'unscaled-svg'].map(id => window.LabMeasure.renderedFontSize(document.getElementById(id))));
    assert.deepEqual(sizes, [12, 8, 13]);
    const outcomes = sizes.map(size => size >= 13);
    assert.deepEqual(outcomes, [false, false, true]);
    return { sizes_px: sizes, font_fixtures: outcomes, method: 'computed CSS font size and rendered transform matrix; actual browser fixture' };
  } finally { await page.close(); }
}

async function labelFixtures(browser) {
  const page = await browser.newPage({ viewport: { width: 900, height: 900 } });
  try {
    await page.setContent('<main>' + LABEL_CLASSES.map(name => '<span class="label-chip ' + name + '" data-label-class="' + name + '">' + name + '</span>').join(' ') + '</main>');
    await page.addStyleTag({ path: join(SITE, 'style.css') });
    await page.addScriptTag({ path: MEASURE });
    await settle(page);
    const rows = await page.evaluate(() => Array.from(document.querySelectorAll('[data-label-class]'), element => {
      const color = getComputedStyle(element).backgroundColor;
      const rgba = window.LabMeasure.parseColor(color);
      const [r, g, b] = rgba;
      const green = rgba[3] > 0 && g > r * 1.15 && g > b * 1.15;
      return { class: element.dataset.labelClass, color, rgba, green, label: element.textContent.trim() };
    }));
    const result = { rows, green_classes: rows.filter(row => row.green).map(row => row.class), definition: 'opaque background with green channel > 1.15 × red and blue' };
    try { assert.deepEqual(result.green_classes, ['pass']); }
    catch (error) { result.assertion_error = describeError(error); }
    return result;
  } finally { await page.close(); }
}

async function tabMeasurements(page, engine) {
  const expected = await page.evaluate(() => Array.from(document.querySelectorAll('a[href],button,input,select,textarea,summary,[role="button"],[tabindex]')).filter(element => window.LabMeasure.visible(element) && !element.disabled && element.tabIndex >= 0).map(element => window.LabMeasure.address(element)));
  await page.evaluate(() => { document.body.tabIndex = -1; document.body.focus(); document.body.removeAttribute('tabindex'); });
  const visited = [];
  const traversalKey = engine === 'webkit' ? 'Alt+Tab' : 'Tab';
  try {
    for (let index = 0; index < expected.length + 2; index++) {
      await page.keyboard.press(traversalKey);
      visited.push(await page.evaluate(() => {
        const element = document.activeElement;
        const style = getComputedStyle(element);
        const ring = window.LabMeasure.focusRing(element);
        return { element: window.LabMeasure.address(element), name: element.getAttribute('aria-label') || element.textContent.trim().slice(0, 100), outline_width_px: parseFloat(style.outlineWidth), outline_style: style.outlineStyle, outline_offset_px: parseFloat(style.outlineOffset), box_shadow: style.boxShadow, outline_contrast: ring?.contrast ?? null, outline_measurement: ring };
      }));
    }
  } finally { await neutralFocus(page); }
  return { expected, visited, traversal_key: traversalKey, keystrokes: visited.length, unreached: expected.filter(element => !visited.some(stop => stop.element === element)) };
}

async function screenshot(page, engine, viewport, name) {
  const file = engine + '-' + viewport.name + '-' + name + '.png';
  await neutralFocus(page);
  await settle(page);
  const focus = await page.evaluate(() => {
    const skip = document.querySelector('.skip-link:not(:focus)'), rect = skip?.getBoundingClientRect();
    return { active_element: document.activeElement?.tagName ?? null, body_focused: document.activeElement === document.body, skip_link_top_px: rect?.top ?? null, skip_link_bottom_px: rect?.bottom ?? null, skip_link_computed_top: skip ? getComputedStyle(skip).top : null };
  });
  assert.ok(focus.body_focused, 'Screenshot must have neutral body focus');
  assert.ok(focus.skip_link_top_px === null || (focus.skip_link_top_px < 0 && focus.skip_link_bottom_px <= 0 && parseFloat(focus.skip_link_computed_top) < 0), 'Skip link must stay hidden unless focused');
  report.screenshot_checks.push({ file, ...focus });
  await page.screenshot({ path: join(OUT, file), fullPage: true, animations: 'disabled' });
  report.screenshots.push(file);
  return file;
}

function cardsFrom(runs) {
  assert.ok(Array.isArray(runs) && runs.length, 'window.LAB.index must be a non-empty slim index');
  const choose = (name, predicate) => {
    const card = runs.find(predicate);
    assert.ok(card?.card_id, 'Card not found in slim index: ' + name);
    return card;
  };
  const c10v = choose('C10V B·A7', run => run.source === 'results/c10v_layerpick/pass1.json' && run.field.replace(/^\./, '') === 'recipes.B.arms.A7_coined_coined');
  const b0 = choose('C10V B0·A7', run => run.source === 'results/c10v_layerpick/pass1.json' && run.field.replace(/^\./, '') === 'recipes.B0.arms.A7_coined_coined');
  const g6 = choose('G6.1', run => run.source === 'results/g6_scale_n_result.json');
  const oracle = choose('C10W P1 oracle·A7', run => /c10w_oracle\/p1_.*\/eval\.json$/.test(run.source) && run.field.replace(/^\./, '') === 'recipes.oracle_p1.arms.A7_coined_coined');
  const training = runs.find(run => /c10w_oracle\/p1_.*\/train\/A7_coined_coined_s0_r16\.json$/.test(run.source));
  return { c10v, b0, g6, oracle, training };
}

async function tasksFor(page, cards, viewport, engine) {
  const tasks = [];
  const runId = cards.c10v.card_id;
  await task('run → line → map', tasks, async record => {
    await go(page, { view: 'runs', run: runId });
    await click(page, '[data-region="content"] [data-line]', record.actions);
    const afterLine = await stateOf(page);
    const line = afterLine.line;
    await click(page, '[data-map-line][data-focus]', record.actions);
    return { selected_run: runId, line, after_line: afterLine, after_map: await stateOf(page) };
  });
  await task('home → C10 status → shared D1 link', tasks, async record => {
    await go(page, { view: 'map', focus: '' });
    await click(page, '[data-focus="cond:C10"]', record.actions);
    const panel = await page.locator('#connections-panel').innerText();
    const status = page.locator('#connections-panel [data-science-status]').first();
    await status.waitFor({ state: 'visible', timeout: 2000 });
    const c10Status = (await status.textContent())?.trim() ?? '';
    record.observation = { focused_panel: panel, c10_status: c10Status };
    record.status_step = { selector: '#connections-panel [data-science-status]', text: c10Status };
    assert.ok(c10Status && !/\bdraft\b/i.test(c10Status), 'C10 scientific status must be non-empty and not DRAFT');
    await click(page, '#connections-panel [data-shared-with="corpus:22"]', record.actions);
    return { focused_panel: panel, c10_status: c10Status, after_shared_link: await stateOf(page) };
  });
  await task('Runs → Inside the model → Compare keeps selected run', tasks, async record => {
    await go(page, { view: 'runs', run: '', compare: [] });
    await page.locator('#run-search').fill('C10V');
    record.actions.push({ action: 'key', control: '#run-search', text: 'C10V', count: 4 });
    const runSelector = '#run-results [data-run="' + runId + '"]';
    await page.locator(runSelector).first().waitFor({ state: 'attached', timeout: 2000 });
    const closedSummaries = await page.locator(runSelector).first().evaluate(element => {
      const summaries = [];
      for (let ancestor = element.parentElement; ancestor; ancestor = ancestor.parentElement) {
        if (ancestor.tagName === 'DETAILS' && !ancestor.open) summaries.unshift(window.LabMeasure.address(ancestor.querySelector(':scope > summary')));
      }
      return summaries;
    });
    for (const summary of closedSummaries) await click(page, summary, record.actions);
    await click(page, runSelector, record.actions);
    await click(page, 'nav [data-view="model"]', record.actions);
    const model = await page.evaluate(id => {
      const content = document.querySelector('[data-region="content"]');
      return { state_run: window.LabView.getState().run, content_has_id: Boolean(content && (content.querySelector('[data-selected-run="' + id + '"], [data-card-id="' + id + '"]') || content.querySelector('a[href$="' + id + '.json"]'))), hash: location.hash };
    }, runId);
    await click(page, '[data-compare-run="' + runId + '"]', record.actions);
    const compare = await page.evaluate(() => {
      const control = document.querySelector('#compare-left');
      const contentCard = document.querySelector('.compare-grid > article:first-child [data-selected-run]')?.dataset.selectedRun ?? null;
      return { run: window.LabView.getState().run, left: control?.dataset.card || contentCard || control?.value || null, control_card: control?.dataset.card ?? null, content_card: contentCard, hash: location.hash };
    });
    const observed = model.state_run === runId && model.content_has_id && compare.run === runId && compare.left === runId && decodeURIComponent(compare.hash).includes(runId);
    return { selected_run: runId, model, compare, selection_carries: observed };
  });
  await task('wiring animation keeps diagram label visible', tasks, async record => {
    await go(page, { view: 'model', run: runId });
    await click(page, '#animate-wiring', record.actions);
    await page.waitForTimeout(250);
    const label = page.locator('[data-diagram-label="diagram, not recorded activity"]');
    const persists = await label.isVisible();
    return { toggle: await page.locator('#animate-wiring').evaluate(element => ({ checked: element.checked ?? null, pressed: element.getAttribute('aria-pressed') })), text: persists ? await label.innerText() : null, diagram_label_persists: persists };
  });
  for (const [experiment, prefix] of [['C10V-layerpick', 'C10V'], ['C10W-oracle', 'C10W'], ['C10U-mint2', 'C10U'], ['G6.1', 'G6.1'], ['R5', 'R5']]) {
    await task('picker ' + experiment, tasks, async record => {
      await go(page, { view: 'model' });
      await page.locator('#picker-search').fill('');
      const steps = [];
      for (const character of prefix) {
        await page.locator('#picker-search').pressSequentially(character);
        record.actions.push({ action: 'key', key: character, count: 1 });
        await settle(page);
        steps.push(await page.evaluate(() => ({ query: document.querySelector('#picker-search').value, result_ids: Array.from(document.querySelectorAll('#picker-results [data-run]')).filter(window.LabMeasure.visible).map(element => element.dataset.run) })));
      }
      const matches = await page.evaluate(id => {
        const index = new Map(window.LAB.index.map(run => [run.card_id, run]));
        return Array.from(document.querySelectorAll('#picker-results [data-run]')).filter(window.LabMeasure.visible).map((element, position) => ({ id: element.dataset.run, position: position + 1, experiment: index.get(element.dataset.run)?.experiment })).filter(row => row.experiment === id);
      }, experiment);
      if (!matches.length) throw new Error('No picker result for ' + experiment);
      assert.ok(matches[0].position <= 10, 'Experiment must be among the first 10 picker results');
      assert.ok(steps.at(-1).result_ids.length <= 50, 'Picker must show at most 50 results');
      await click(page, '#picker-results [data-run="' + matches[0].id + '"]', record.actions);
      const selectionWaitMs = await waitForChosenRun(page, matches[0].id);
      const afterChoice = await stateOf(page);
      record.actions.at(-1).after = afterChoice;
      return { prefix, after_each_keystroke: steps, results_at_choice: steps.at(-1).result_ids.length, first_experiment_position: matches[0].position, target_run: matches[0].id, selection_wait_ms: selectionWaitMs, after_choice: afterChoice };
    });
  }
  for (const [name, next, key, expected] of [['run', { view: 'runs', run: runId }, 'run', runId], ['line', { view: 'lines', line: 'era:c10' }, 'line', 'era:c10'], ['compare', { view: 'compare', run: runId, compare: [runId, cards.b0.card_id] }, 'compare', [runId, cards.b0.card_id]]]) {
    await task('URL ' + name + ' survives reload', tasks, async () => {
      await go(page, next);
      const before = await stateOf(page);
      await page.reload({ waitUntil: 'load' });
      await ready(page);
      const after = await stateOf(page);
      return { method: 'LabView state selection and actual file reload', key, expected, before, after, hash_has_key: before.hash.includes(key + '='), restored: JSON.stringify(after[key]) === JSON.stringify(expected) && after.view === before.view };
    });
  }
  await task('map and picker by keyboard', tasks, async record => {
    await go(page, { view: 'map', focus: '' });
    await page.locator('[data-focus="cond:C10"]').filter({ visible: true }).first().focus();
    await page.keyboard.press('Enter');
    record.actions.push({ action: 'key', key: 'Enter', control: 'C10 map focus' });
    await settle(page);
    const map = await stateOf(page);
    await go(page, { view: 'model', run: cards.g6.card_id });
    const beforePicker = await stateOf(page);
    await page.locator('#picker-search').fill('');
    await page.locator('#picker-search').pressSequentially('C10V');
    await page.locator('#picker-search').press('ArrowDown');
    const focused = await page.evaluate(() => {
      const search = document.querySelector('#picker-search');
      const option = document.getElementById(search.getAttribute('aria-activedescendant'));
      return { tag: document.activeElement.tagName, active_descendant: option?.id ?? null, run: option?.dataset.run ?? null };
    });
    assert.ok(focused.run && focused.run !== beforePicker.run, 'Keyboard picker must target a different recorded run');
    await page.keyboard.press('Enter');
    record.actions.push({ action: 'key', key: 'C10V, ArrowDown, Enter', count: 6, control: '#picker-search' });
    const selectionWaitMs = await waitForChosenRun(page, focused.run);
    const picker = await stateOf(page), selectionChanged = picker.run !== beforePicker.run;
    assert.ok(selectionChanged, 'Keyboard picker must change the selected run');
    return { map, before_picker: beforePicker, focused_picker_result: focused, selection_wait_ms: selectionWaitMs, selection_changed: selectionChanged, picker };
  });
  for (const slider of ['#training-step', '#event-step']) {
    await task(slider + ' by keyboard' + (viewport.touch ? ' and touch' : ''), tasks, async record => {
      await go(page, { view: 'model', run: (cards.training ?? cards.oracle).card_id });
      const control = page.locator(slider);
      await control.waitFor({ state: 'visible', timeout: 2000 });
      await control.focus();
      await control.press('Home');
      const before = await control.inputValue();
      await control.press('ArrowRight');
      record.actions.push({ action: 'key', key: 'Home, ArrowRight', count: 2, control: slider });
      const after = await control.inputValue();
      let touched = null;
      let beforeTouch = null;
      let touchChanged = null;
      if (viewport.touch) {
        await control.evaluate(element => { element.value = '0'; element.dispatchEvent(new Event('input', { bubbles: true })); });
        await settle(page);
        beforeTouch = await control.inputValue();
        assert.equal(beforeTouch, '0', 'Slider touch baseline must be zero');
        record.actions.push({ action: 'set-control', control: slider, value: beforeTouch, purpose: 'touch baseline' });
        await control.scrollIntoViewIfNeeded();
        const rect = await control.boundingBox();
        assert.ok(rect && rect.width > 0, 'Slider touch target must have a measurable box');
        await page.touchscreen.tap(rect.x + rect.width * 0.75, rect.y + rect.height / 2);
        record.actions.push({ action: 'tap', control: slider, x: rect.x + rect.width * 0.75, y: rect.y + rect.height / 2 });
        await settle(page);
        touched = await control.inputValue();
        touchChanged = touched !== beforeTouch;
        record.observation = { before, after_keyboard: after, before_touch: beforeTouch, after_touch: touched, touch_changed: touchChanged };
        assert.ok(touchChanged, 'Slider touch must change the value from zero');
      }
      return { before, after_keyboard: after, before_touch: beforeTouch, after_touch: touched, touch_changed: touchChanged };
    });
  }
  if (viewport.touch) await task('map and picker by touch', tasks, async record => {
    await go(page, { view: 'map', focus: '' });
    await click(page, '[data-focus="cond:C10"]', record.actions, 'tap');
    const map = await stateOf(page);
    await go(page, { view: 'model', run: cards.g6.card_id });
    const beforePicker = await stateOf(page);
    await page.locator('#picker-search').fill('C10V');
    const target = await page.evaluate(() => Array.from(document.querySelectorAll('#picker-results [data-run]')).find(window.LabMeasure.visible)?.dataset.run);
    assert.ok(target && target !== beforePicker.run, 'Touch picker must target a different recorded run');
    await click(page, '#picker-results [data-run="' + target + '"]', record.actions, 'tap');
    const selectionWaitMs = await waitForChosenRun(page, target);
    const picker = await stateOf(page), selectionChanged = picker.run !== beforePicker.run;
    record.actions.at(-1).after = picker;
    assert.ok(selectionChanged, 'Touch picker must change the selected run');
    return { map, before_picker: beforePicker, target_run: target, selection_wait_ms: selectionWaitMs, selection_changed: selectionChanged, picker };
  });
  return tasks;
}

async function measureViewport(browser, engine, viewport) {
  const context = await browser.newContext({ viewport: { width: viewport.width / viewport.zoom, height: viewport.height / viewport.zoom }, deviceScaleFactor: viewport.zoom, hasTouch: viewport.touch });
  const page = await context.newPage();
  const output = { viewport, zoom_method: viewport.zoom === 2 ? '200% browser-zoom emulation: half CSS viewport and double device scale; native browser zoom is not asserted' : 'native CSS viewport', screens: [], tasks: [], browser_console_errors: [] };
  page.on('pageerror', error => output.browser_console_errors.push(describeError(error)));
  output.failed_requests = [];
  page.on('requestfailed', request => output.failed_requests.push({ url: request.url(), failure: request.failure() }));
  try {
    output.payload = await firstView(page);
    const cards = cardsFrom(await page.evaluate(async () => { await window.LabView.ensureIndex(); return window.LAB.index; }));
    const screens = [
      ['map', { view: 'map', focus: '' }],
      ['map-c10-focus', { view: 'map', focus: 'cond:C10' }],
      ...['t-branch', 'viability', 'f1-conditions', 'c10'].map(era => ['line-' + era, { view: 'lines', line: 'era:' + era }]),
      ['line-d1', { view: 'lines', line: 'corpus:22' }],
      ['run-c10v-b-a7', { view: 'runs', run: cards.c10v.card_id }],
      ['run-g6.1', { view: 'runs', run: cards.g6.card_id }],
      ['compare', { view: 'compare', run: cards.c10v.card_id, compare: [cards.c10v.card_id, cards.b0.card_id] }],
      ['model-mistral', { view: 'model-history', model: 'Mistral-7B' }],
      ['learn', { view: 'learn', learning: 'learn' }],
      ['evaluations', { view: 'learn', learning: 'evaluations' }]
    ];
    for (const [name, state] of screens) {
      const screen = { name, requested_state: state };
      output.screens.push(screen);
      try {
        await go(page, state);
        screen.measurements = await page.evaluate(zoom => window.LabMeasure.measure(zoom), viewport.zoom);
        screen.screenshot = await screenshot(page, engine, viewport, name);
        screen.keyboard = await tabMeasurements(page, engine);
        if (['run-g6.1', 'line-d1', 'model-mistral'].includes(name)) screen.forbidden_words_found = FORBIDDEN.filter(word => screen.measurements.content_text?.toLowerCase().includes(word.toLowerCase()));
      } catch (error) { screen.error = describeError(error); }
    }
    await go(page, { view: 'map', focus: 'cond:C10' });
    await page.addStyleTag({ content: 'html { filter: grayscale(1) !important; }' });
    output.greyscale_screenshot = await screenshot(page, engine, viewport, 'map-c10-greyscale');
    await page.evaluate(() => document.querySelectorAll('style').forEach(style => { if (style.textContent.includes('filter: grayscale(1)')) style.remove(); }));
    output.tasks = await tasksFor(page, cards, viewport, engine);

    const fallbackPage = await context.newPage();
    await fallbackPage.route('https://cdn.jsdelivr.net/**', route => route.abort('blockedbyclient'));
    await fallbackPage.goto(ENTRY, { waitUntil: 'load' });
    await ready(fallbackPage);
    await go(fallbackPage, { view: 'model', run: cards.c10v.card_id });
    await fallbackPage.locator('#show-3d').click();
    await fallbackPage.waitForFunction(() => /unavailable/i.test(document.querySelector('#model-status')?.textContent ?? ''), null, { timeout: 5000 });
    output.screens.push({ name: 'model-2d', cdn: 'deliberately blocked after actually requesting 3D', model_status: await fallbackPage.locator('#model-status').innerText(), fallback_visible: await fallbackPage.locator('#tower-fallback').isVisible(), measurements: await fallbackPage.evaluate(zoom => window.LabMeasure.measure(zoom), viewport.zoom), screenshot: await screenshot(fallbackPage, engine, viewport, 'model-2d'), keyboard: await tabMeasurements(fallbackPage, engine) });
    await fallbackPage.close();

    await go(page, { view: 'model', run: cards.c10v.card_id });
    await page.locator('#show-3d').click();
    try { await page.waitForFunction(() => document.querySelector('#tower canvas') || /unavailable/i.test(document.querySelector('#model-status')?.textContent ?? ''), null, { timeout: 10000 }); }
    catch (error) { output.model_3d_wait_error = describeError(error); }
    const canvas = page.locator('#tower canvas').filter({ visible: true });
    if (await canvas.count()) output.screens.push({ name: 'model-3d', cdn: 'network allowed', measurements: await page.evaluate(zoom => window.LabMeasure.measure(zoom), viewport.zoom), screenshot: await screenshot(page, engine, viewport, 'model-3d'), keyboard: await tabMeasurements(page, engine) });
    else output.screens.push({ name: 'model-3d', status: 'not observed: no visible 3D canvas', message: await page.locator('#tower').innerText(), measurements: null });
    return output;
  } finally { await context.close(); }
}

let playwright;
try {
  playwright = await import(pathToFileURL(join(SCRATCH, 'node_modules/playwright/index.mjs')).href);
  report.environment.playwright = JSON.parse(readFileSync(join(SCRATCH, 'node_modules/playwright/package.json'), 'utf8')).version;
  for (const name of ['chromium', 'webkit']) {
    const engine = { name, status: 'UNVERIFIED', version: null, font_fixture: null, label_fixture: null, viewports: [], error: null };
    report.engines.push(engine);
    let browser;
    try {
      const type = playwright[name];
      const options = { headless: true, timeout: 15000 };
      options.executablePath = name === 'chromium' ? cachedChromiumPath() : join(SCRATCH, 'ms-playwright/webkit-2311/pw_run.sh');
      engine.executable = options.executablePath;
      assert.ok(existsSync(options.executablePath), 'Provisioned browser executable does not exist: ' + options.executablePath);
      browser = await type.launch(options);
      engine.version = browser.version();
      engine.font_fixture = await fontFixtures(browser);
      engine.label_fixture = await labelFixtures(browser);
      for (const viewport of VIEWPORTS) {
        try { engine.viewports.push(await measureViewport(browser, name, viewport)); }
        catch (error) { engine.viewports.push({ viewport, status: 'UNVERIFIED: screen sequence did not complete', error: describeError(error), screens: [], tasks: [] }); }
      }
      engine.status = 'browser launched; observations and errors recorded; no reviewer verdict';
    } catch (error) { engine.error = describeError(error); }
    finally { if (browser) await browser.close(); }
  }
} catch (error) { report.environment_error = describeError(error); }

const screens = report.engines.flatMap(engine => engine.viewports.flatMap(viewport => viewport.screens)).filter(screen => screen.measurements);
if (screens.length) {
  const summaries = screens.map(screen => screen.measurements.summary);
  const minimum = key => {
    const values = summaries.map(summary => summary[key]).filter(value => value !== null && Number.isFinite(value));
    return values.length ? Math.min(...values) : null;
  };
  report.summary = { measured_screens: screens.length, minimum_rendered_font_px: minimum('minimum_rendered_font_px'), minimum_text_contrast: minimum('minimum_text_contrast'), minimum_mark_border_focus_contrast: minimum('minimum_mark_border_focus_contrast'), minimum_target_width_px: minimum('minimum_target_width_px'), minimum_target_height_px: minimum('minimum_target_height_px'), first_view_bytes: report.engines.flatMap(engine => engine.viewports.map(viewport => ({ engine: engine.name, viewport: viewport.viewport.name, bytes: viewport.payload?.first_view_bytes ?? null }))) };
}
const browserAssertions = report.engines.filter(engine => !engine.error && engine.viewports.length === VIEWPORTS.length).map(engine => {
  const observed = engine.viewports.flatMap(viewport => viewport.screens).filter(screen => ['run-g6.1', 'line-d1', 'model-mistral'].includes(screen.name));
  const selections = engine.viewports.flatMap(viewport => viewport.tasks).filter(task => task.name.startsWith('Runs →'));
  const animations = engine.viewports.flatMap(viewport => viewport.tasks).filter(task => task.name.startsWith('wiring animation'));
  const pickers = engine.viewports.flatMap(viewport => viewport.tasks).filter(task => task.name.startsWith('picker '));
  return { engine: engine.name, picker_selection_complete: pickers.length === 5 * VIEWPORTS.length && pickers.every(task => !task.error && task.observation?.target_run && task.observation.after_choice?.run === task.observation.target_run), non_c10_content: observed.length === 3 * VIEWPORTS.length && observed.every(screen => !screen.error && Array.isArray(screen.forbidden_words_found) && screen.forbidden_words_found.length === 0 && screen.measurements?.content_text), selection_carries: selections.length === VIEWPORTS.length && selections.every(task => task.observation?.selection_carries === true), diagram_label_persists: animations.length === VIEWPORTS.length && animations.every(task => task.observation?.diagram_label_persists === true), font_fixtures: engine.font_fixture?.font_fixtures ?? null };
});
const taskErrors = report.engines.flatMap(engine => engine.viewports.flatMap(viewport => viewport.tasks)).filter(task => task.error);
const observationErrors = report.environment_error || report.engines.some(engine => engine.error || engine.viewports.some(viewport => viewport.error || viewport.screens.some(screen => screen.error)));
const proofComplete = !observationErrors && !taskErrors.length && browserAssertions.length === 2 && browserAssertions.every(engine => engine.picker_selection_complete && engine.non_c10_content && engine.selection_carries && engine.diagram_label_persists && JSON.stringify(engine.font_fixtures) === JSON.stringify([false, false, true]));
const proof = { kind: 'actual browser behavior assertions; not a design-review verdict', measure_file: join(OUT, 'measure.json'), complete: proofComplete, non_c10_content: proofComplete, selection_carries: proofComplete, diagram_label_persists: proofComplete, picker_selection_complete: proofComplete, font_fixtures: proofComplete ? browserAssertions[0].font_fixtures : null, task_errors: taskErrors.map(task => ({ name: task.name, error: task.error })), engines: browserAssertions };
writeJSON(join(OUT, 'browser-tests.json'), proof);
writeJSON(join(REVIEW, 'v2-build/browser-tests.json'), proof);
report.browser_assertions = browserAssertions;
writeJSON(join(OUT, 'measure.json'), report);
console.log(JSON.stringify({ measure_file: join(OUT, 'measure.json'), measured_screens: screens.length, screenshots: report.screenshots.length, engines: report.engines.map(engine => ({ name: engine.name, status: engine.status, error: engine.error?.message ?? null })) }));
process.exitCode = observationErrors || taskErrors.length ? 2 : 0;
