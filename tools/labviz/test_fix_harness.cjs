/* Node observation-layer fixtures only: no browser, screenshots, or science execution. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { fileURLToPath, pathToFileURL } = require('node:url');
const test = require('node:test');

const ROOT = path.resolve(__dirname, '../..');
const SCRATCH = '/private/tmp/labviz-review';
const reviewPath = path.join(__dirname, 'review.mjs');
const measureSource = fs.readFileSync(path.join(__dirname, 'measure.js'), 'utf8');
const plain = value => JSON.parse(JSON.stringify(value));

function reviewRuntime(extra = {}, full = false, setup = '') {
  // Only module loading and filesystem/browser boundaries are substituted.
  // Every assertion below executes the production function, not source matching.
  let source = fs.readFileSync(reviewPath, 'utf8').replace(/^import .*;\n/gm, '').replace('import.meta.url', 'reviewModuleUrl');
  if (!full) source = source.slice(0, source.indexOf('\nlet playwright;'));
  else source = source.replace("import(pathToFileURL(join(SCRATCH, 'node_modules/playwright/index.mjs')).href)", 'importPlaywright()').replace('\nlet playwright;', '\n' + setup + '\nlet playwright;');
  const context = vm.createContext({
    assert: { ...assert, deepEqual: (actual, expected, message) => assert.deepEqual(plain(actual), plain(expected), message) }, ...path, fileURLToPath, pathToFileURL,
    existsSync: fs.existsSync, readdirSync: fs.readdirSync, statSync: fs.statSync,
    readFileSync: fs.readFileSync, mkdirSync() {}, writeFileSync() {},
    reviewModuleUrl: pathToFileURL(reviewPath).href, URL,
    process: { cwd: () => SCRATCH, env: { npm_config_cache: path.join(SCRATCH, 'npm-cache'), PLAYWRIGHT_BROWSERS_PATH: path.join(SCRATCH, 'ms-playwright') }, version: 'Node fixture', platform: 'darwin', arch: 'arm64' },
    console: { log() {} }, ...extra
  });
  if (full) return { context, done: vm.runInContext('(async () => {\n' + source + '\nglobalThis.observedReport = report;\n})()', context) };
  vm.runInContext(source + '\nglobalThis.reviewFns = { cachedChromiumPath, labelFixtures, tabMeasurements, screenshot, tasksFor, measureViewport };', context);
  return { context, fns: context.reviewFns };
}

function element(id, tag = 'DIV', parent = null, overrides = {}) {
  const { style: customStyle, rect: customRect, ...extra } = overrides;
  const rect = { x: 20, y: 20, width: 100, height: 44, left: 20, right: 120, top: 20, bottom: 64, ...customRect };
  const node = {
    id, tagName: tag, parentElement: parent, children: [], namespaceURI: 'http://www.w3.org/1999/xhtml',
    textContent: id, dataset: {}, tabIndex: ['A', 'BUTTON', 'INPUT', 'SELECT'].includes(tag) ? 0 : -1,
    scrollWidth: rect.width, clientWidth: rect.width, disabled: false,
    style: { display: 'block', visibility: 'visible', opacity: '1', backgroundColor: 'rgb(16, 23, 33)', backgroundImage: 'none', color: 'rgb(255, 255, 255)', fontSize: '16px', transform: 'none', zoom: '1', overflowX: 'visible', overflowY: 'visible', outlineWidth: '3px', outlineStyle: 'solid', outlineColor: 'rgb(255, 211, 143)', outlineOffset: '4px', boxShadow: 'none', borderTopWidth: '0px', borderRightWidth: '0px', borderBottomWidth: '0px', borderLeftWidth: '0px', ...customStyle },
    getBoundingClientRect: () => rect,
    getAttribute(name) { return name === 'class' ? (this.className || '') : null; },
    removeAttribute() {}, dispatchEvent() {},
    matches(selector) {
      if (selector === ':focus') return Boolean(this.focused);
      return selector.split(',').some(part => part.trim().startsWith('.') && (this.className || '').split(' ').includes(part.trim().slice(1)));
    },
    closest(selector) { for (let row = this; row; row = row.parentElement) if (row.matches(selector)) return row; return null; },
    ...extra
  };
  if (parent) parent.children.push(node);
  return node;
}

function observationDOM(nodes = [], width = 390, hit = null) {
  const html = element('root', 'HTML', null, { rect: { x: 0, y: 0, left: 0, top: 0, right: width, bottom: 844, width, height: 844 } });
  const body = element('body', 'BODY', html);
  for (const node of nodes) if (!node.parentElement) { node.parentElement = body; body.children.push(node); }
  const all = [html, body, ...nodes];
  const interactive = () => nodes.filter(node => ['A', 'BUTTON', 'INPUT', 'SELECT', 'SUMMARY'].includes(node.tagName));
  const document = {
    body, documentElement: html, activeElement: body, fonts: { ready: Promise.resolve() },
    createTreeWalker: () => ({ nextNode: () => null }),
    createRange: () => ({ selectNodeContents() {}, getBoundingClientRect: () => ({ width: 0, height: 0 }) }),
    createElement: () => ({ getContext: () => ({ measureText: () => ({ width: 8 }) }) }),
    querySelectorAll(selector) {
      if (selector === '*') return all;
      if (selector === 'style') return [];
      if (selector === '[data-label-class]') return nodes.filter(node => node.dataset.labelClass);
      if (selector.startsWith('nav ') || selector.startsWith('p, ') || selector === '[data-chart]' || selector === 'canvas') return [];
      return interactive();
    },
    querySelector(selector) {
      if (selector === '#tower canvas') return this.canvas || null;
      if (selector === '#model-status') return { textContent: this.fallback ? '3D unavailable' : '3D available' };
      if (selector.startsWith('#')) return nodes.find(node => '#' + node.id === selector) || null;
      return null;
    },
    elementsFromPoint(x, y) { return [hit ? hit(x, y) : body, html].filter(Boolean); },
    elementFromPoint(x, y) { return this.elementsFromPoint(x, y)[0]; }
  };
  function focus(node) { if (document.activeElement) document.activeElement.focused = false; document.activeElement = node; node.focused = true; }
  for (const node of all) { node.focus = () => focus(node); node.blur = () => { node.focused = false; document.activeElement = body; }; }
  const context = vm.createContext({ document, innerWidth: width, innerHeight: 844, devicePixelRatio: 1, location: { href: 'file:///fixture/index.html', hash: '' }, NodeFilter: { SHOW_TEXT: 4 }, getComputedStyle: node => node.style, requestAnimationFrame: work => work(), Event: class Event {} });
  vm.runInContext(measureSource, context);
  context.window = context;
  return { context, document, nodes, interactive, api: context.LabMeasure };
}

function pageFixture(dom, { status = 'BLOCKING: write contract remains open', staleShared = false, touchChanges = true } = {}) {
  const state = { view: 'map', run: '', focus: '', line: '', compare: [] };
  dom.context.LabView = { getState: () => ({ ...state }), setState: async next => Object.assign(state, next), ensureIndex: async () => dom.context.LAB?.index || [] };
  let traversalIndex = -1;
  const captures = [];
  const touchBefore = [];
  const page = {
    captures, touchBefore, state,
    async evaluate(fn, value) { dom.context.argument = value; return vm.runInContext('(' + fn.toString() + ')(argument)', dom.context); },
    async waitForFunction(fn) { const result = await this.evaluate(fn); assert.ok(result, 'Fixture wait condition did not hold'); },
    async addScriptTag() {}, async addStyleTag() {}, async on() {}, async off() {}, async route() { dom.document.fallback = true; }, async goto() {}, async close() {},
    async screenshot(options) { captures.push({ name: path.basename(options.path), focused: dom.document.activeElement.focused === true }); },
    keyboard: { async press(key) {
      if (key === 'Enter') return;
      const controls = dom.interactive().filter(node => key === 'Alt+Tab' || node.tagName === 'INPUT' || node.tagName === 'SELECT');
      if (dom.document.activeElement === dom.document.body) traversalIndex = -1;
      if (controls.length) { traversalIndex = (traversalIndex + 1) % controls.length; controls[traversalIndex].focus(); }
    } },
    touchscreen: { async tap(x) {
      const slider = dom.nodes.find(node => node.type === 'range');
      touchBefore.push(slider.value);
      if (touchChanges) slider.value = String(Math.round((x - 20) / 100 * Number(slider.max)));
    } },
    locator(selector) {
      const matching = dom.nodes.find(node => '#' + node.id === selector);
      const validShared = selector === '#connections-panel [data-shared-with="corpus:22"]';
      const legacyShared = staleShared && selector === '#connections-panel [data-shared="layer:write-engine"]';
      const exists = matching || validShared || legacyShared || ['#connections-panel', '#connections-panel [data-science-status]', '[data-focus="cond:C10"]', '#show-3d', '#model-status', '#tower-fallback', '#tower canvas'].includes(selector);
      const control = {
        filter() { return this; }, first() { return this; },
        async waitFor() { if (!exists) throw new Error('No fixture control: ' + selector); },
        async textContent() { return selector.includes('data-science-status') ? status : selector; },
        async innerText() { return selector === '#connections-panel' ? 'C10\nStatus now\n' + status + '\nshared with D1' : status; },
        async click() { if (selector.includes('data-focus')) state.focus = 'cond:C10'; if (validShared || legacyShared) state.focus = 'model:Qwen2.5-3B'; },
        async tap() { return this.click(); },
        async isVisible() { return Boolean(exists); }, async count() { return exists ? 1 : 0; },
        async focus() { matching?.focus(); },
        async inputValue() { return matching.value; },
        async press(key) { if (key === 'Home') matching.value = '0'; if (key === 'ArrowRight') matching.value = String(Number(matching.value) + 1); },
        async evaluate(fn) { assert.ok(matching, 'Fixture element required for evaluate'); dom.context.fixtureElement = matching; return vm.runInContext('(' + fn.toString() + ')(fixtureElement)', dom.context); },
        async scrollIntoViewIfNeeded() {},
        async boundingBox() { return matching.getBoundingClientRect(); }
      };
      return control;
    }
  };
  return page;
}

function selectTask(runtime, prefix) {
  runtime.context.taskPrefix = prefix;
  vm.runInContext('const fixtureTask = task; task = (name, tasks, work) => name.startsWith(taskPrefix) ? fixtureTask(name, tasks, work) : Promise.resolve(null);', runtime.context);
}

// Break: accepting the misspelled layer selector loses the actual D1 path.
test('home task follows a rendered shared-D1 link and records science status', async () => {
  const runtime = reviewRuntime(); selectTask(runtime, 'home →');
  const page = pageFixture(observationDOM());
  const tasks = await runtime.fns.tasksFor(page, { c10v: { card_id: 'fixture-run' }, oracle: { card_id: 'fixture-oracle' }, b0: { card_id: 'fixture-control' } }, { touch: false }, 'chromium');
  assert.equal(tasks[0].error, undefined);
  assert.equal(tasks[0].observation.c10_status, 'BLOCKING: write contract remains open');
  assert.equal(tasks[0].actions[1].selector, '#connections-panel [data-shared-with="corpus:22"]');
  assert.equal(tasks[0].taps, 2);
  assert.equal(tasks[0].observation.after_shared_link.focus, 'model:Qwen2.5-3B');
});

// Break: treating an absent or framing-review DRAFT value as scientific status.
for (const status of ['', 'DRAFT']) test('home task rejects scientific status ' + JSON.stringify(status), async () => {
  const runtime = reviewRuntime(); selectTask(runtime, 'home →');
  const tasks = await runtime.fns.tasksFor(pageFixture(observationDOM(), { status, staleShared: true }), { c10v: { card_id: 'fixture-run' }, oracle: { card_id: 'fixture-oracle' }, b0: { card_id: 'fixture-control' } }, { touch: false }, 'chromium');
  assert.match(tasks[0].error?.message || '', /C10 scientific status/);
  assert.equal(tasks[0].observation.c10_status, status);
  assert.equal(tasks[0].taps, 1);
});

// Break: plain Tab in macOS WebKit visits form inputs but skips links/buttons.
test('WebKit keyboard measurement walks links and buttons with Alt+Tab', async () => {
  const runtime = reviewRuntime();
  const dom = observationDOM([element('link', 'A'), element('button', 'BUTTON'), element('input', 'INPUT')]);
  const result = await runtime.fns.tabMeasurements(pageFixture(dom), 'webkit');
  assert.deepEqual(plain(result.unreached), []);
  assert.deepEqual(plain(result.expected), ['#link', '#button', '#input']);
  assert.equal(result.traversal_key, 'Alt+Tab');
});

// Break: a screenshot after keyboard coverage leaves the skip link over content.
for (const name of ['map', 'map-c10-greyscale']) test('screenshot blurs focus for ' + name, async () => {
  const runtime = reviewRuntime();
  const dom = observationDOM([element('skip-link', 'A')]); dom.nodes[0].focus();
  const page = pageFixture(dom);
  await runtime.fns.screenshot(page, 'chromium', { name: 'phone' }, name);
  assert.equal(page.captures[0].focused, false);
});

// Break: the touch result can equal the keyboard result without exercising a new value.
for (const touchChanges of [true, false]) test('slider touch from zero ' + (touchChanges ? 'changes' : 'must fail when unchanged'), async () => {
  const runtime = reviewRuntime(); selectTask(runtime, '#training-step');
  const slider = element('training-step', 'INPUT', null, { type: 'range', value: '0', min: '0', max: '4' });
  const page = pageFixture(observationDOM([slider]), { touchChanges });
  const tasks = await runtime.fns.tasksFor(page, { c10v: { card_id: 'fixture-run' }, oracle: { card_id: 'fixture-oracle' }, b0: { card_id: 'fixture-control' } }, { touch: true }, 'webkit');
  assert.deepEqual(page.touchBefore, ['0']);
  if (touchChanges) {
    assert.equal(tasks[0].error, undefined);
    assert.equal(tasks[0].observation.before_touch, '0');
    assert.equal(tasks[0].observation.after_touch, '3');
    assert.equal(tasks[0].observation.touch_changed, true);
  } else assert.match(tasks[0].error?.message || '', /touch.*change/i);
});

// Break: an about:blank file stylesheet leaves all labels transparent; a non-awaited style load has the same failure.
test('label fixture waits for addStyleTag before observing computed backgrounds', async () => {
  const runtime = reviewRuntime();
  const dom = observationDOM();
  const page = pageFixture(dom);
  page.setContent = async html => {
    for (const [, name] of html.matchAll(/data-label-class="([^"]+)"/g)) dom.nodes.push(element(name, 'SPAN', null, { dataset: { labelClass: name }, style: { backgroundColor: 'rgba(0, 0, 0, 0)' } }));
  };
  page.addStyleTag = async ({ path: stylePath }) => {
    assert.equal(stylePath, path.join(ROOT, 'results/labviz/site/style.css'));
    await new Promise(resolve => setImmediate(resolve));
    for (const node of dom.nodes) node.style.backgroundColor = node.dataset.labelClass === 'pass' ? 'rgb(24, 83, 52)' : 'rgb(55, 60, 70)';
  };
  const result = await runtime.fns.labelFixtures({ newPage: async () => page });
  assert.deepEqual(plain(result.green_classes), ['pass']);
  assert.equal(result.assertion_error, undefined);
});

// Break: only a cached headless shell or the package's stale default executable is chosen.
test('runner explicitly selects provisioned Chromium 1228 and WebKit', async () => {
  const chromium = path.join(SCRATCH, 'ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing');
  const webkit = path.join(SCRATCH, 'ms-playwright/webkit-2311/pw_run.sh');
  const stale = path.join(SCRATCH, 'ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell');
  const type = executable => ({ executablePath: () => executable, launch: async () => { throw new Error('Controlled fixture stops before browser launch'); } });
  const runtime = reviewRuntime({
    existsSync: target => [path.join(SCRATCH, 'ms-playwright'), chromium, webkit, stale].includes(target),
    readdirSync: () => ['chromium_headless_shell-1243', 'chromium-1228', 'webkit-2311'],
    readFileSync: target => String(target).endsWith('package.json') ? '{"version":"fixture"}' : fs.readFileSync(target, 'utf8'),
    importPlaywright: async () => ({ chromium: type(stale), webkit: type(path.join(SCRATCH, 'ms-playwright/webkit-9999/pw_run.sh')) })
  }, true);
  await runtime.done;
  assert.equal(runtime.context.observedReport.engines[0].executable, chromium);
  assert.equal(runtime.context.observedReport.engines[1].executable, webkit);
});

// Break: a later review silently replaces the proof cited by the historical Phase-1 report.
test('successful runner writes browser proof only in its fresh namespace', async () => {
  const writes = [];
  const browser = { version: () => 'fixture only', close: async () => {} };
  const type = { executablePath: () => 'unused stale default', launch: async () => browser };
  const fixtureSummary = { minimum_rendered_font_px: 16, minimum_text_contrast: 5, minimum_mark_border_focus_contrast: 4, minimum_target_width_px: 44, minimum_target_height_px: 44 };
  const runtime = reviewRuntime({
    existsSync: () => true,
    writeFileSync: (target, content) => writes.push({ target, content: JSON.parse(content) }),
    readFileSync: target => String(target).endsWith('package.json') ? '{"version":"fixture"}' : fs.readFileSync(target, 'utf8'),
    importPlaywright: async () => ({ chromium: type, webkit: type }),
    fixtureFont: async () => ({ font_fixtures: [false, false, true] }),
    fixtureLabels: async () => ({ green_classes: ['pass'] }),
    fixtureViewport: async (_browser, _engine, viewport) => ({ viewport, payload: { first_view_bytes: 123 }, screens: ['run-g6.1', 'line-d1', 'model-mistral'].map(name => ({ name, forbidden_words_found: [], measurements: { content_text: 'Controlled content', summary: fixtureSummary } })), tasks: [{ name: 'Runs → selected run', observation: { selection_carries: true } }, { name: 'wiring animation fixture', observation: { diagram_label_persists: true } }] })
  }, true, 'fontFixtures = fixtureFont; labelFixtures = fixtureLabels; measureViewport = fixtureViewport;');
  await runtime.done;
  const proof = writes.find(write => write.target.endsWith('/browser-tests.json'));
  const measurement = writes.find(write => write.target.endsWith('/measure.json'));
  assert.ok(proof && measurement);
  assert.equal(proof.target, path.join(path.dirname(measurement.target), 'browser-tests.json'));
  assert.equal(proof.content.measure_file, measurement.target);
  assert.equal(writes.some(write => write.target === path.join(ROOT, 'results/labviz/review/v2-build/browser-tests.json')), false);
});

// Break: model fallback/canvas screenshots omit keyboard observations.
test('both 2D fallback and 3D model screens contain actual keyboard measurements', async () => {
  const runtime = reviewRuntime();
  vm.runInContext('tasksFor = async () => [];', runtime.context);
  const index = [
    { card_id: 'b', source: 'results/c10v_layerpick/pass1.json', field: 'recipes.B.arms.A7_coined_coined' },
    { card_id: 'b0', source: 'results/c10v_layerpick/pass1.json', field: 'recipes.B0.arms.A7_coined_coined' },
    { card_id: 'g6', source: 'results/g6_scale_n_result.json', field: '' },
    { card_id: 'oracle', source: 'results/c10w_oracle/p1_fixture/eval.json', field: 'recipes.oracle_p1.arms.A7_coined_coined' }
  ];
  const pages = [];
  const context = { async newPage() {
    const dom = observationDOM([element('show-2d', 'BUTTON'), element('show-3d', 'BUTTON')]);
    dom.context.LAB = { index }; dom.document.canvas = element('canvas', 'CANVAS');
    const page = pageFixture(dom); pages.push(page); return page;
  }, async close() {} };
  const result = await runtime.fns.measureViewport({ newContext: async () => context }, 'webkit', { name: 'phone', width: 390, height: 844, zoom: 1, touch: true });
  const models = result.screens.filter(row => ['model-2d', 'model-3d'].includes(row.name));
  assert.deepEqual(plain(models.map(row => row.name)), ['model-2d', 'model-3d']);
  for (const screen of models) {
    assert.ok(screen.keyboard, screen.name + ' keyboard observations missing');
    assert.deepEqual(plain(screen.keyboard.unreached), []);
  }
  assert.equal(pages.flatMap(page => page.captures).some(capture => capture.focused), false);
});

// Break: reading the empty Map bootstrap index prevents every viewport screen sequence.
// Loading it during first-view capture also wrongly charges it to the initial Map payload.
test('lazy card index loads after first-view payload measurement', async () => {
  const runtime = reviewRuntime({ statSync: () => ({ size: 100 }) });
  vm.runInContext('tasksFor = async () => [];', runtime.context);
  const index = [
    { card_id: 'b', source: 'results/c10v_layerpick/pass1.json', field: 'recipes.B.arms.A7_coined_coined' },
    { card_id: 'b0', source: 'results/c10v_layerpick/pass1.json', field: 'recipes.B0.arms.A7_coined_coined' },
    { card_id: 'g6', source: 'results/g6_scale_n_result.json', field: '' },
    { card_id: 'oracle', source: 'results/c10w_oracle/p1_fixture/eval.json', field: 'recipes.oracle_p1.arms.A7_coined_coined' }
  ];
  const requests = [];
  const context = { async newPage() {
    const dom = observationDOM([element('show-2d', 'BUTTON'), element('show-3d', 'BUTTON')]);
    dom.context.LAB = { index: [] }; dom.document.canvas = element('canvas', 'CANVAS');
    const page = pageFixture(dom);
    const listeners = new Map();
    page.on = (name, listener) => { if (!listeners.has(name)) listeners.set(name, new Set()); listeners.get(name).add(listener); };
    page.off = (name, listener) => listeners.get(name)?.delete(listener);
    const emit = file => {
      requests.push(file);
      const request = { url: () => pathToFileURL(path.join(ROOT, 'results/labviz/site', file)).href, resourceType: () => file.endsWith('.html') ? 'document' : file.endsWith('.css') ? 'stylesheet' : 'script' };
      for (const listener of listeners.get('request') || []) listener(request);
    };
    page.goto = async () => {
      assert.equal(dom.context.LAB.index.length, 0, 'First-view navigation must retain the empty lazy Map bootstrap');
      for (const file of ['index.html', 'style.css', 'data.js', 'app.js']) emit(file);
    };
    dom.context.LabView.ensureIndex = async () => {
      await new Promise(resolve => setImmediate(resolve));
      emit('cards/index.js');
      dom.context.LAB.index = index;
      return index;
    };
    return page;
  }, async close() {} };
  let result;
  await assert.doesNotReject(async () => { result = await runtime.fns.measureViewport({ newContext: async () => context }, 'webkit', { name: 'phone', width: 390, height: 844, zoom: 1, touch: true }); });
  assert.deepEqual(plain(result.payload.requests.map(row => path.basename(new URL(row.url).pathname))), ['index.html', 'style.css', 'data.js', 'app.js']);
  assert.equal(result.payload.first_view_bytes, 400);
  assert.equal(result.screens.find(row => row.name === 'run-c10v-b-a7').requested_state.run, 'b');
  assert.deepEqual(requests.slice(0, 5), ['index.html', 'style.css', 'data.js', 'app.js', 'cards/index.js']);
});

// Break: border-on-identical-fill reports a fake 1:1 interior edge.
test('identical border/fill excludes only the interior contrast and keeps outside edge', () => {
  const button = element('active', 'BUTTON', null, { style: { backgroundColor: 'rgb(185, 198, 255)', borderTopWidth: '2px', borderTopStyle: 'solid', borderTopColor: 'rgb(185, 198, 255)' } });
  const dom = observationDOM([button]);
  const paint = dom.api.measure().paint;
  assert.equal(paint.some(row => row.kind === 'border-top'), false);
  assert.ok(paint.find(row => row.kind === 'border-top-outside')?.contrast > 3);
});

// Break: skipping every interior border would conceal a distinct low-contrast border.
test('distinct interior border contrast remains observable', () => {
  const button = element('bordered', 'BUTTON', null, { style: { backgroundColor: 'rgb(185, 198, 255)', borderTopWidth: '2px', borderTopStyle: 'solid', borderTopColor: 'rgb(180, 190, 245)' } });
  const paint = observationDOM([button]).api.measure().paint;
  assert.ok(paint.find(row => row.kind === 'border-top')?.contrast < 1.2);
  assert.ok(paint.find(row => row.kind === 'border-top-outside')?.contrast > 3);
});

// Break: the offset ring is compared to the focused button's own fill.
test('offset focus ring samples backdrop outside the focused control', () => {
  const button = element('active', 'BUTTON', null, { style: { backgroundColor: 'rgb(185, 198, 255)' } });
  const dom = observationDOM([button]); button.focus();
  const ring = dom.api.measure().paint.find(row => row.kind === 'focus-ring');
  assert.ok(ring.contrast > 12, 'Offset ring must see the dark page backdrop');
  assert.deepEqual(plain(ring.background), [16, 23, 33, 1]);
});

// Break: using parent backdrop alone misses a neighboring active button under the ring.
for (const matte of [false, true]) test('focus ring ' + (matte ? 'composites its matte over a neighbor' : 'detects a neighbor without a matte'), () => {
  const button = element('focus', 'BUTTON', null, { style: { backgroundColor: matte ? 'rgb(185, 198, 255)' : 'rgb(16, 23, 33)', outlineOffset: '2px', boxShadow: matte ? 'rgb(16, 23, 33) 0px 0px 0px 6px' : 'none' } });
  const neighbor = element('neighbor', 'BUTTON', null, { style: { backgroundColor: 'rgb(185, 198, 255)' } });
  const dom = observationDOM([button, neighbor], 390, () => neighbor); button.focus();
  const ring = dom.api.measure().paint.find(row => row.kind === 'focus-ring');
  assert.ok(matte ? ring.contrast > 12 : ring.contrast < 1.2);
});

// Break: opaque-only ring math overstates contrast for a translucent outline.
test('translucent offset ring is composited against the actual backdrop', () => {
  const button = element('focus', 'BUTTON', null, { style: { backgroundColor: 'rgb(185, 198, 255)', outlineColor: 'rgba(255, 211, 143, 0.5)' } });
  const dom = observationDOM([button]); button.focus();
  const ring = dom.api.measure().paint.find(row => row.kind === 'focus-ring');
  assert.deepEqual(plain(ring.foreground), [135.5, 117, 88, 1]);
  assert.ok(ring.contrast > 3 && ring.contrast < 5);
});

// Break: a within-viewport box containing a long unbroken label escapes target-only overflow checks.
test('overflow names visible descendants and separates expected table scrolling', () => {
  const long = element('long-language-measure', 'SPAN', null, { scrollWidth: 391, clientWidth: 328, textContent: 'C2b_depth_map_subject_keying.language_cos_by_layer' });
  const table = element('table-wrap', 'DIV', null, { className: 'table-wrap', scrollWidth: 600, clientWidth: 328, style: { overflowX: 'auto' } });
  const cell = element('table-cell', 'TD', table, { scrollWidth: 600, clientWidth: 100 });
  const hidden = element('hidden', 'DIV', null, { scrollWidth: 500, clientWidth: 100, style: { display: 'none' } });
  const dom = observationDOM([long, table, cell, hidden], 360);
  const rows = dom.api.measure().layout.scrolling_descendants || [];
  assert.deepEqual(plain(rows.map(row => row.element)), ['#long-language-measure', '#table-wrap', '#table-cell']);
  assert.equal(rows[0].contributes_to_root_overflow, true);
  assert.equal(rows[0].expected_table_scroll, false);
  assert.equal(rows[1].expected_table_scroll, true);
  assert.equal(rows[2].expected_table_scroll, true);
  assert.equal(rows[2].contributes_to_root_overflow, false);
});
