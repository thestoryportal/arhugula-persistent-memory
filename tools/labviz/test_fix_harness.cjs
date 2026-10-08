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
  const attributes = new Map();
  const { style: customStyle, rect: customRect, ...extra } = overrides;
  const rect = { x: 20, y: 20, width: 100, height: 44, left: 20, right: 120, top: 20, bottom: 64, ...customRect };
  const node = {
    id, tagName: tag, parentElement: parent, children: [], namespaceURI: 'http://www.w3.org/1999/xhtml',
    textContent: id, dataset: {}, tabIndex: ['A', 'BUTTON', 'INPUT', 'SELECT'].includes(tag) ? 0 : -1,
    scrollWidth: rect.width, clientWidth: rect.width, disabled: false,
    style: { display: 'block', visibility: 'visible', opacity: '1', backgroundColor: 'rgb(16, 23, 33)', backgroundImage: 'none', color: 'rgb(255, 255, 255)', fontSize: '16px', transform: 'none', zoom: '1', overflowX: 'visible', overflowY: 'visible', outlineWidth: '3px', outlineStyle: 'solid', outlineColor: 'rgb(255, 211, 143)', outlineOffset: '4px', boxShadow: 'none', borderTopWidth: '0px', borderRightWidth: '0px', borderBottomWidth: '0px', borderLeftWidth: '0px', ...customStyle },
    getBoundingClientRect: () => rect,
    getAttribute(name) { return name === 'class' ? (this.className || '') : attributes.get(name) ?? null; },
    setAttribute(name, value) { attributes.set(name,String(value)); },
    removeAttribute(name) { attributes.delete(name); }, dispatchEvent() {},
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
      if (selector.startsWith('nav ') || selector.startsWith('.top-nav ') || selector.startsWith('p, ') || selector === '[data-chart]' || selector === 'canvas') return [];
      return interactive();
    },
    querySelector(selector) {
      if (selector === '.skip-link:not(:focus)') return nodes.find(node=>node.className==='skip-link'&&!node.focused) || null;
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
  const context = vm.createContext({ document, innerWidth: width, innerHeight: 844, devicePixelRatio: 1, scrollX: 0, scrollY: 0, scrollTo(position,top) { const target=typeof position==='object'?position:{left:position,top};context.scrollX=target.left;context.scrollY=target.top; }, location: { href: 'file:///fixture/index.html', hash: '' }, NodeFilter: { SHOW_TEXT: 4 }, getComputedStyle: node => node.style, requestAnimationFrame: work => work(), Event: class Event {} });
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
    async waitForFunction(fn, value) { const result = await this.evaluate(fn, value); assert.ok(result, 'Fixture wait condition did not hold'); },
    async addScriptTag() {}, async addStyleTag() {}, async on() {}, async off() {}, async route() { dom.document.fallback = true; }, async goto() {}, async close() {},
    async screenshot(options) { captures.push({ name: path.basename(options.path), focused: dom.document.activeElement !== dom.document.body && dom.document.activeElement.focused === true }); },
    keyboard: { async press(key) {
      if (key === 'Enter') return;
      if (!['Tab','Alt+Tab'].includes(key)) return;
      const controls = dom.interactive().filter(node => node.tabIndex>=0&&(key === 'Alt+Tab' || node.tagName === 'INPUT' || node.tagName === 'SELECT'));
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

test('Tab measurement leaves neutral focus for the next measured screen', async () => {
  const runtime=reviewRuntime(), dom=observationDOM([element('skip-link','A'),element('next','BUTTON')]);
  await runtime.fns.tabMeasurements(pageFixture(dom),'webkit');
  assert.equal(dom.document.activeElement,dom.document.body);
  assert.equal(dom.nodes.some(node=>node.focused),false);
});

test('Screenshot records neutral focus and verifies the hidden skip link', async () => {
  const runtime=reviewRuntime(), skip=element('skip-link','A',null,{className:'skip-link',style:{top:'-100px'},rect:{top:-100,bottom:-56}});
  const dom=observationDOM([skip]);skip.focus();
  await runtime.fns.screenshot(pageFixture(dom),'chromium',{name:'phone'},'map');
  const checks=vm.runInContext('report.screenshot_checks',runtime.context);
  assert.equal(checks?.[0]?.active_element,'BODY');
  assert.equal(checks[0].skip_link_top_px,-100);
});

test('Screenshot rejects a skip link still covering content after focus is cleared', async () => {
  const runtime=reviewRuntime(), skip=element('skip-link','A',null,{className:'skip-link',style:{top:'10px'}});
  const dom=observationDOM([skip]),page=pageFixture(dom);
  await assert.rejects(runtime.fns.screenshot(page,'chromium',{name:'phone'},'map'),/skip link/i);
  assert.equal(page.captures.length,0);
});

for (const engine of ['chromium','webkit']) test('Full-page capture settles scroll after a Tab walk in '+engine, async () => {
  const runtime=reviewRuntime(), skip=element('skip-link','A',null,{className:'skip-link',style:{top:'-100px'},rect:{top:-150,bottom:-100}});
  const dom=observationDOM([skip,element('last-control','INPUT')]),page=pageFixture(dom),press=page.keyboard.press,capture=page.screenshot;
  page.keyboard.press=async key=>{await press(key);dom.context.scrollY=960;};
  let pendingFrames=0,resets=0;
  dom.context.scrollTo=(position,top)=>{const target=typeof position==='object'?position:{left:position,top};assert.equal(target.left,0);assert.equal(target.top,0);resets++;pendingFrames=2;};
  dom.context.requestAnimationFrame=callback=>{if(pendingFrames>0&&--pendingFrames===0)dom.context.scrollY=0;callback();};
  page.screenshot=async options=>{
    assert.equal(options.fullPage,true);await capture(options);
    Object.assign(page.captures.at(-1),{scroll_y:dom.context.scrollY,skip_link_page_bottom_px:skip.getBoundingClientRect().bottom+dom.context.scrollY});
  };
  const tabs=await runtime.fns.tabMeasurements(page,engine);
  assert.ok(tabs.visited.length>0);assert.equal(dom.context.scrollY,960);
  assert.equal(dom.document.activeElement,dom.document.body);
  await runtime.fns.screenshot(page,engine,{name:'phone'},'model-2d');
  assert.equal(page.captures[0].scroll_y,0,'A scrolled full-page image would include the fixed skip link');
  assert.ok(page.captures[0].skip_link_page_bottom_px<=0);
  assert.equal(resets,1);assert.equal(pendingFrames,0);
  const checks=vm.runInContext('report.screenshot_checks',runtime.context);
  assert.equal(checks[0].scroll_y,0);assert.equal(checks[0].skip_link_page_top_px,-150);assert.equal(checks[0].skip_link_page_bottom_px,-100);
});

test('Full-page capture rejects a viewport-hidden skip link inside the document image', async () => {
  const runtime=reviewRuntime(), skip=element('skip-link','A',null,{className:'skip-link',style:{top:'-100px'},rect:{top:-150,bottom:-100}});
  const dom=observationDOM([skip]),page=pageFixture(dom);
  dom.context.scrollY=960;dom.context.scrollTo=()=>{};
  await assert.rejects(runtime.fns.screenshot(page,'chromium',{name:'phone'},'map'),/skip link.*full-page/i);
  assert.equal(page.captures.length,0);
});

for (const engine of ['chromium','webkit']) test('Screenshot overrides smooth scrolling after a Tab walk in '+engine, async () => {
  const stylesheet=fs.readFileSync(path.join(__dirname,'style.css'),'utf8');
  assert.match(stylesheet,/html\s*\{[^}]*scroll-behavior\s*:\s*smooth\b/);
  const runtime=reviewRuntime(),skip=element('skip-link','A',null,{className:'skip-link',style:{top:'-100px'},rect:{top:-150,bottom:-100}});
  const dom=observationDOM([skip,element('last-control','INPUT')]),page=pageFixture(dom),press=page.keyboard.press,capture=page.screenshot;
  let destination=null;
  dom.context.scrollTo=(position,top)=>{
    const target=typeof position==='object'?position:{left:position,top};
    if(target.behavior==='instant'){dom.context.scrollX=target.left;dom.context.scrollY=target.top;destination=null;}
    else destination=target;
  };
  dom.context.requestAnimationFrame=callback=>{if(destination)dom.context.scrollY+=(destination.top-dom.context.scrollY)*.1;callback();};
  dom.context.scrollY=1200;
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.evaluate(async()=>{await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));});
  assert.ok(dom.context.scrollY>0,'Positive control: CSS smooth scrolling is still moving after two frames');
  page.keyboard.press=async key=>{await press(key);dom.context.scrollY=1200;};
  page.screenshot=async options=>{assert.equal(dom.context.scrollY,0,'Capture must override the smooth scroll');await capture(options);};
  await runtime.fns.tabMeasurements(page,engine);
  assert.equal(dom.context.scrollY,1200);assert.equal(dom.document.activeElement,dom.document.body);
  await runtime.fns.screenshot(page,engine,{name:'phone'},'map-c10-greyscale');
  assert.equal(page.captures.length,1);
  const checks=vm.runInContext('report.screenshot_checks',runtime.context);
  assert.equal(checks[0].scroll_y,0);assert.ok(checks[0].skip_link_page_bottom_px<=0);
});

// Only the browser IO boundary is delayed: tasksFor and its observations are real.
function delayedPickerPage({stuck=false}={}) {
  const search=element('picker-search','INPUT');
  const dom=observationDOM([search]),page=pageFixture(dom),baseLocator=page.locator;
  const rows=['C10V-layerpick','C10W-oracle','C10U-mint2','G6.1','R5'].map((experiment,i)=>({card_id:'chosen-'+i,experiment}));
  dom.context.LAB={index:rows};
  let options=[],pending=null,searchFocused=false,mapFocused=false;
  const baseQueryAll=dom.document.querySelectorAll.bind(dom.document);
  dom.document.querySelectorAll=selector=>selector==='#picker-results [data-run]'?options:baseQueryAll(selector);
  dom.document.getElementById=id=>id==='picker-search'?search:options.find(option=>option.id===id) || null;
  function filter() {
    if(pending)throw new Error('Picker result detached by an unfinished prior selection');
    options=rows.filter(row=>row.experiment.startsWith(search.value)).map(row=>element('picker-option-'+row.card_id,'BUTTON',null,{dataset:{run:row.card_id}}));
  }
  function choose(id) {
    if(stuck){pending=Promise.resolve();return;}
    pending=new Promise(resolve=>setImmediate(()=>{page.state.run=id;page.state.line='exp:'+rows.find(row=>row.card_id===id).experiment;pending=null;resolve();}));
  }
  page.waitForFunction=async(fn,value)=>{
    if(pending)await pending;
    const result=await page.evaluate(fn,value);
    if(!result){const error=new Error('Chosen run did not finish loading');error.name='TimeoutError';throw error;}
  };
  page.locator=selector=>{
    const base=baseLocator(selector);
    if(selector==='[data-focus="cond:C10"]')return {...base,filter(){return this;},first(){return this;},focus:async()=>{mapFocused=true;searchFocused=false;}};
    if(selector==='#picker-search')return {...base,
      fill:async value=>{search.value=value;searchFocused=true;filter();},
      pressSequentially:async value=>{search.value+=value;searchFocused=true;filter();},
      press:async key=>{if(key==='ArrowDown'){search.setAttribute('aria-activedescendant',options[0]?.id);return;}throw new Error('Picker must use arrows rather than '+key);}
    };
    if(selector.startsWith('#picker-results [data-run'))return {...base,
      filter(){return this;},first(){return this;},waitFor:async()=>{},
      textContent:async()=>options[0]?.textContent,
      click:async()=>choose(options[0]?.dataset.run),tap:async()=>choose(options[0]?.dataset.run)
    };
    return base;
  };
  page.keyboard.press=async key=>{
    assert.equal(key,'Enter');
    if(mapFocused){page.state.focus='cond:C10';mapFocused=false;}
    else if(searchFocused)choose(options.find(option=>option.id===search.getAttribute('aria-activedescendant'))?.dataset.run);
  };
  return page;
}

test('All picker tasks wait for delayed selection before reading or filtering the next list', async () => {
  const runtime=reviewRuntime();selectTask(runtime,'picker ');
  const tasks=await runtime.fns.tasksFor(delayedPickerPage(),{c10v:{card_id:'starting-run'},b0:{card_id:'other-start'},oracle:{card_id:'oracle'}},{touch:false},'chromium');
  assert.equal(tasks.length,5);
  for(let i=0;i<tasks.length;i++){
    assert.equal(tasks[i].error,undefined,tasks[i].name);
    assert.equal(tasks[i].observation?.after_choice.run,'chosen-'+i);
    assert.equal(tasks[i].observation?.target_run,'chosen-'+i);
    assert.ok(Number.isFinite(tasks[i].observation?.selection_wait_ms));
  }
});

test('A picker load timeout fails the task instead of recording a stale run as success', async () => {
  const runtime=reviewRuntime();selectTask(runtime,'picker C10V');
  const tasks=await runtime.fns.tasksFor(delayedPickerPage({stuck:true}),{c10v:{card_id:'starting-run'},b0:{card_id:'other-start'},oracle:{card_id:'oracle'}},{touch:false},'chromium');
  assert.equal(tasks[0].error?.name,'TimeoutError');
});

for(const [engine,touch] of [['chromium',false],['webkit',false],['webkit',true]]) test(engine+' picker '+(touch?'touch':'keyboard')+' demonstrates a changed run',async()=>{
  const runtime=reviewRuntime();selectTask(runtime,touch?'map and picker by touch':'map and picker by keyboard');
  const tasks=await runtime.fns.tasksFor(delayedPickerPage(),{c10v:{card_id:'chosen-0'},b0:{card_id:'b0'},g6:{card_id:'other-start'},oracle:{card_id:'oracle'}},{touch},engine);
  assert.equal(tasks[0].error,undefined);
  assert.equal(tasks[0].observation?.before_picker?.run,'other-start');
  assert.equal(tasks[0].observation?.picker.run,'chosen-0');
  assert.equal(tasks[0].observation?.selection_changed,true);
});

test('Frame measurement counts only the five top-level destinations',()=>{
  const destinations=['map','lines','runs','model','learn'].map(view=>element(view,'BUTTON',null,{dataset:{view}}));
  const breadcrumb=element('crumb','BUTTON',null,{dataset:{view:'map'}});
  const dom=observationDOM([...destinations,breadcrumb]),base=dom.document.querySelectorAll.bind(dom.document);
  dom.document.querySelectorAll=selector=>selector==='.top-nav [data-view]'?destinations:selector==='nav [data-view]'?[...destinations,breadcrumb]:base(selector);
  assert.deepEqual(plain(dom.api.measure().frame.navigation.map(node=>node.view)),['map','lines','runs','model','learn']);
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

// Round 2: the canonical proof pointer must follow the latest completed review.
for (const taskFails of [false,true]) test('runner refreshes dated and canonical proof for ' + (taskFails ? 'a failed picker' : 'successful tasks'), async () => {
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
    fixtureViewport: async (_browser, _engine, viewport) => ({ viewport, payload: { first_view_bytes: 123 }, screens: ['run-g6.1', 'line-d1', 'model-mistral'].map(name => ({ name, forbidden_words_found: [], measurements: { content_text: 'Controlled content', summary: fixtureSummary } })), tasks: [{ name: 'Runs → selected run', observation: { selection_carries: true } }, { name: 'wiring animation fixture', observation: { diagram_label_persists: true } }, ...Array.from({length:5},(_,i)=>({name:'picker fixture-'+i,observation:{target_run:'chosen-'+i,after_choice:{run:'chosen-'+i}},...(taskFails&&i===0?{error:{name:'TimeoutError',message:'Chosen run did not finish loading'}}:{})}))] })
  }, true, 'fontFixtures = fixtureFont; labelFixtures = fixtureLabels; measureViewport = fixtureViewport;');
  await runtime.done;
  const proof = writes.find(write => write.target.endsWith('/browser-tests.json'));
  const measurement = writes.find(write => write.target.endsWith('/measure.json'));
  assert.ok(proof && measurement);
  assert.equal(proof.target, path.join(path.dirname(measurement.target), 'browser-tests.json'));
  assert.equal(proof.content.measure_file, measurement.target);
  const latest=writes.find(write => write.target === path.join(ROOT, 'results/labviz/review/v2-build/browser-tests.json'));
  assert.ok(latest);assert.equal(latest.content.measure_file,measurement.target);
  assert.equal(latest.content.complete,!taskFails);assert.equal(latest.content.non_c10_content,!taskFails);
  assert.equal(runtime.context.process.exitCode,taskFails?2:0);
});

function modelViewportFixture() {
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
    const page = pageFixture(dom); page.closed=false;page.close=async()=>{page.closed=true;};pages.push(page);return page;
  }, async close() { this.closed=true; } };
  return {context,pages};
}

// Break: model fallback/canvas screenshots omit keyboard observations.
test('both 2D fallback and 3D model screens contain actual keyboard measurements', async () => {
  const runtime = reviewRuntime();
  vm.runInContext('tasksFor = async () => [];', runtime.context);
  const {context,pages}=modelViewportFixture();
  const result = await runtime.fns.measureViewport({ newContext: async () => context }, 'webkit', { name: 'phone', width: 390, height: 844, zoom: 1, touch: true });
  const models = result.screens.filter(row => ['model-2d', 'model-3d'].includes(row.name));
  assert.deepEqual(plain(models.map(row => row.name)), ['model-2d', 'model-3d']);
  for (const screen of models) {
    assert.ok(screen.keyboard, screen.name + ' keyboard observations missing');
    assert.deepEqual(plain(screen.keyboard.unreached), []);
  }
  assert.equal(pages.flatMap(page => page.captures).some(capture => capture.focused), false);
});

for (const name of ['map-c10-greyscale','model-2d','model-3d']) test('Capture failure preserves measured screens for '+name, async () => {
  const runtime=reviewRuntime();vm.runInContext('tasksFor = async () => [];',runtime.context);
  const {context,pages}=modelViewportFixture(),newPage=context.newPage.bind(context);
  context.newPage=async()=>{
    const page=await newPage(),capture=page.screenshot;
    page.screenshot=async options=>{if(path.basename(options.path).endsWith('-'+name+'.png'))assert.fail('Synthetic capture assertion for '+name);await capture(options);};
    return page;
  };
  const output=await runtime.fns.measureViewport({newContext:async()=>context},'webkit',{name:'phone',width:390,height:844,zoom:1,touch:true});
  assert.equal(output.screens.length,15);assert.ok(output.screens.every(screen=>screen.measurements));
  const error=name==='map-c10-greyscale'?output.error:output.screens.find(screen=>screen.name===name)?.error;
  assert.equal(error?.name,'AssertionError');assert.ok(error.message.includes(name));
  assert.equal(context.closed,true);assert.equal(pages[1].closed,true);
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
