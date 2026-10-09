'use strict';

// Production cards and IIFE; this document adapter does not measure browser layout.
const assert = require('node:assert/strict');
const { test } = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '../..');
const fixture = [
  'import json, tempfile',
  'from pathlib import Path',
  'from tools.labviz.test_mathlab import prepare, started, event, write_stream',
  'from tools.labviz.cards import Reader',
  'with tempfile.TemporaryDirectory() as tmp:',
  '    root = Path(tmp)',
  '    prepare(root)',
  "    run = 'finding_errors'",
  "    write_stream(root, run, [started(run), event(run, 'finding_staged', finding_id='bad',",
  "        tier='MATH-PROXY', summary='Estimate', path='logs/pending_findings/missing.md')])",
  "    for purpose,step in [('admission',3),('experiment',2)]:",
  "        run='calibration_scope_'+purpose",
  "        write_stream(root,run,[started(run,step=step,purpose=purpose),",
  "            event(run,'gate_result',gate_id='calibration',plain_words='Calibration',",
  "                observed='FAIL',bar='PASS',comparison='meets',passed=False)])",
  '    print(json.dumps(Reader(root).collect()))',
].join('\n');
const generated = spawnSync(path.join(root, '.venv/bin/python'), ['-B', '-c', fixture], { cwd:root, encoding:'utf8' });
assert.equal(generated.status, 0, generated.stderr);
const recordedCards = JSON.parse(generated.stdout);
const card = name => {
  const found = recordedCards.find(c => c.identity.name === 'results/mathlab_staging/runs/'+name+'/events.jsonl');
  assert.ok(found, 'canonical MathLab stream must become a card: '+name);
  return found;
};
const plain = html => String(html).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');

function element() {
  const attrs = new Map();
  return {
    innerHTML:'', textContent:'', dataset:{}, style:{}, children:[], value:'',
    setAttribute(k,v) { attrs.set(k,String(v)); }, getAttribute(k) { return attrs.get(k); },
    removeAttribute(k) { attrs.delete(k); }, addEventListener() {}, querySelectorAll() { return []; },
    append(n) { this.children.push(n); }, after() {}, focus() {}, scrollIntoView() {},
  };
}

function app() {
  const elements = new Map(), get = id => {
    if (!elements.has(id)) elements.set(id,element());
    return elements.get(id);
  };
  const document = {
    getElementById:get, querySelectorAll:() => [], addEventListener() {},
    createElement:element, head:element(),
  };
  const index = recordedCards.map(c => ({
    card_id:c.card_id, source:c.identity.name, field:c.identity.field, line:'mathlab:D-ML-1',
    experiment:'D-ML-1', title:c.context.question?.value, label:c.label.value,
    mathlab:c.mathlab ? {tier:c.evidence_status, status:c.mathlab.state.value.status,
                        purpose:c.mathlab.state.value.purpose, run_id:c.mathlab.state.value.run_id} : undefined,
  }));
  const window = { LAB:{index, graph:{nodes:[],edges:[]}}, addEventListener() {} };
  const location = {hash:''}, history = {replaceState(_s,_t,hash) { location.hash=hash; }};
  const expose = 'window.testMathlab={frame,renderRun,renderRuns,renderModel,renderCompare,runRow,pickerResults,set:next=>{state={...initial,...next}},seed:c=>cards.set(c.card_id,c)};';
  const source = fs.readFileSync(path.join(__dirname,'app.js'),'utf8')
    .replace('state=readURL(); renderStatus(); fire(render());', expose);
  vm.runInNewContext(source, {window, document, location, history, URLSearchParams,
    requestAnimationFrame() {}, matchMedia:() => ({matches:false}), queueMicrotask, console});
  recordedCards.forEach(c => window.testMathlab.seed(c));
  return {api:window.testMathlab, get, html:() => get('view-content').innerHTML, index};
}

test('run view pins the proxy label and renders full stages, gate thresholds, resources and halt', () => {
  const c = card('halted_fixture'), r = app();
  r.api.set({view:'run',run:c.card_id}); r.api.frame(c); r.api.renderRun(c);
  assert.match(r.get('evidence-badge').textContent, /MATH-PROXY/);
  assert.match(r.html(), /math estimate, not evidence/);
  for (const term of ['reproduction','Repeat the saved calculation','2700','STOPPED-RESOURCE',
                       'diagnostic.json','Resource samples','Available GiB','RSS GiB','CPU %','Progress','3','6']) {
    assert.ok(plain(r.html()).includes(term), term);
  }
  for (const gate of c.mathlab.state.value.gates) assert.ok(r.html().includes(gate.gate_id), gate.gate_id);
  assert.match(r.html(), /0\.000001|1e-6/);
  assert.match(r.html(), /observer-parity/);
  assert.match(plain(r.html()), /2a.*incomplete/i);
  assert.doesNotMatch(r.html(), /Save SVG|Save PNG|class="score"|<h3>Side effects<\/h3>|<h3>Written layers<\/h3>/);
});

test('admission PASS remains a receipt with all experiment steps not started', () => {
  const r = app(); r.api.renderRun(card('admission_fixture'));
  assert.match(plain(r.html()), /Admission only/i);
  assert.equal((plain(r.html()).match(/not started/g) || []).length, 4);
  assert.doesNotMatch(plain(r.html()), /Step [1-4].*completed/i);
});

test('calibration PASS, FAIL, INVALID render as folded and only FAIL gets cheap-stop text', () => {
  for (const outcome of ['PASS','FAIL','INVALID']) {
    const r = app(); r.api.renderRun(card('calibration_'+outcome));
    assert.ok(plain(r.html()).includes(outcome));
    assert.equal(/\bcheap(?:ly)?\b/i.test(plain(r.html())), outcome === 'FAIL', outcome);
    if (outcome === 'INVALID') assert.match(plain(r.html()), /invalid: no verdict/);
  }
});

test('a calibration gate outside the folded stop scope never tells the operator to stop', () => {
  for (const name of ['calibration_scope_admission','calibration_scope_experiment']) {
    const c=card(name), r=app(); r.api.renderRun(c);
    assert.equal(c.mathlab.state.value.status, 'running');
    assert.equal(c.mathlab.state.value.steps['3'], 'not started');
    assert.doesNotMatch(plain(r.html()), /\bcheap(?:ly)?\b/i);
  }
});

test('parse errors are visible before the stage view and preserve the torn-tail line', () => {
  const r = app(); r.api.renderRun(card('torn_fixture'));
  assert.match(r.html(), /role="alert"/);
  assert.match(plain(r.html()), /line 2: incomplete line/);
  assert.ok(r.html().indexOf('Parse errors') < r.html().indexOf('Stages'));
});

test('finding text and candidate ideas are escaped and retain proxy limits', () => {
  const r = app(); r.api.renderRun(card('halted_fixture'));
  assert.match(r.html(), /MATH-PROXY/);
  assert.match(plain(r.html()), /Candidate questions.*ideas to test/i);
  assert.match(r.html(), /&lt;script&gt;not executable&lt;\/script&gt;/);
  assert.match(r.html(), /&lt;img src=x onerror=alert\(1\)&gt;/);
  assert.match(r.html(), /evidence\/logs\/pending_findings\/mathlab_fixture\.md/);
  assert.doesNotMatch(r.html(), /<script>|<img src=x/);
});

test('missing referenced findings show their read problem', () => {
  const r = app(); r.api.renderRun(card('finding_errors'));
  assert.match(plain(r.html()), /missing\.md/);
  assert.match(plain(r.html()), /read|missing/i);
});

test('direct model and mixed compare routes retain the proxy boundary', () => {
  const c = card('halted_fixture'), r = app();
  r.api.set({view:'model',run:c.card_id}); r.api.frame(c); r.api.renderModel(c);
  assert.match(r.html(), /math estimate, not evidence/);
  assert.doesNotMatch(r.html(), /show-3d|Static wiring|Inside the model/);
  const evidence = {card_id:'ordinary',identity:{name:'results/ordinary.json'},context:{},
                    headline:{hits:{value:1},out_of:{value:72}},label:{value:null},per_fact:[],per_layer:[],sources:[]};
  r.api.seed(evidence); r.api.set({view:'compare',compare:[evidence.card_id,c.card_id]});
  r.api.renderCompare(evidence,c); r.api.frame(evidence);
  assert.match(r.get('evidence-badge').textContent, /MATH-PROXY/);
  assert.match(r.html(), /math estimate, not evidence/);
  assert.match(plain(r.html()), /not comparable/);
});

test('Runs and picker rows show proxy tier, label, folded scope and status', () => {
  const c = card('admission_fixture'), r = app();
  const row = r.api.runRow(r.index.find(x => x.card_id === c.card_id));
  assert.match(row, /MATH-PROXY/); assert.match(row, /math estimate, not evidence/);
  assert.match(row, /admission/); assert.match(row, /finished/);
  r.api.set({view:'runs'}); r.api.renderRuns(); r.api.frame();
  assert.match(r.get('evidence-badge').textContent, /MATH-PROXY/);
  assert.match(r.get('run-results').innerHTML, /MATH-PROXY/);
  r.api.pickerResults('admission_fixture');
  assert.match(r.get('picker-results').innerHTML, /MATH-PROXY/);
});

test('empty event stream shows unknown facts without fabricating success', () => {
  const r = app(); r.api.renderRun(card('empty_fixture'));
  assert.match(plain(r.html()), /not started/);
  assert.match(plain(r.html()), /not recorded/);
  assert.doesNotMatch(r.html(), /class="score"|Save SVG|Save PNG|>PASS</);
});
