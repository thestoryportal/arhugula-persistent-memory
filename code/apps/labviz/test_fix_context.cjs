const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const { execFileSync } = require('node:child_process');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { test } = require('node:test');

const ROOT = resolve(__dirname, '../..');
const SITE = resolve(ROOT, 'results/labviz/site');
const readJSON = file => JSON.parse(readFileSync(file, 'utf8'));
const context = readJSON(resolve(SITE, 'context.json'));
const index = readJSON(resolve(SITE, 'cards/index.json'));
const node = id => context.graph.nodes.find(item => item.node_id === id);
const hash = file => createHash('sha256').update(readFileSync(file)).digest('hex');

function sourced(leaf) {
  assert.ok(leaf && Object.hasOwn(leaf, 'value'), 'consumer receives a typed leaf');
  assert.ok(leaf.src, 'consumer receives a source citation');
  const file = resolve(ROOT, leaf.src.file);
  if (Object.hasOwn(leaf.src, 'path')) {
    const actual = JSON.parse(execFileSync('/opt/homebrew/bin/rtk', ['proxy', 'jq', leaf.src.path, file], { encoding: 'utf8' }));
    assert.deepEqual(leaf.value, actual, 'JSON leaf retains its exact source value');
  } else {
    const line = readFileSync(file, 'utf8').split(/\r?\n/)[leaf.src.line - 1];
    assert.ok(line?.includes(leaf.src.quote), 'document quote occurs verbatim at its cited line');
    assert.ok(leaf.src.quote.includes(leaf.value), 'document value occurs verbatim in its quote');
  }
}

// Catches the missing graph framing that made the line renderer use generic text.
test('D1 line receives its frozen deciding question as a verbatim documentary leaf', () => {
  const question = '**D1 decides the monitored variable:** at a FIXED total edit count N, does held-out same-relation read corruption depend on the **concentration** of edits on one relation, or on **N** itself?';
  assert.equal(node('corpus:22').question?.value, question);
  assert.deepEqual(node('corpus:22').description, node('corpus:22').question);
  sourced(node('corpus:22').question);
  assert.equal(node('corpus:22').question.src.file, 'CORPUS/22_D1_CAPACITY_LAW.md');
  assert.equal(node('corpus:22').question.src.line, 6);
});

// Catches using the era's generic measure rather than D1's concentration contrast.
test('D1 line measure describes its own concentration contrast and preserves its citations', () => {
  const d1 = node('corpus:22');
  assert.equal(d1.measure?.value, 'held-out same-relation read corruption vs concentration');
  sourced(d1.measure);
  assert.equal(d1.measure.src.path, '.corpus_eras["22"].line_measure');
  const citations = context.contexts.corpus_eras['22'].citations.line_measure;
  assert.ok(citations.some(item => item.line === 6 && item.quote.includes('**concentration**')));
  assert.ok(citations.some(item => item.line === 11 && item.quote.includes('held-out `capital` top-1')));
  for (const citation of citations) {
    const line = readFileSync(resolve(ROOT, citation.file), 'utf8').split(/\r?\n/)[citation.line - 1];
    assert.ok(line.includes(citation.quote));
  }
});

// Catches the absent C10 status and the substitution of DRAFT as science status.
test('C10 focus receives the actual science status cell separately from framing review', () => {
  const c10 = node('cond:C10');
  assert.ok(c10.status?.value?.includes('OPEN MUST-FIX for the fixed target.'));
  assert.notEqual(c10.status.value, 'DRAFT');
  sourced(c10.status);
  assert.equal(c10.status.src.file, 'docs/F1_DETERMINATION.md');
  assert.equal(c10.status.src.quote, c10.status.value, 'the complete current-status cell is retained');
  assert.deepEqual(c10.citations.status, c10.status.src);
  assert.equal(c10.framing_status.value, 'DRAFT');
  sourced(c10.framing_status);
  assert.equal(hash(resolve(SITE, 'evidence', c10.status.src.file)), hash(resolve(ROOT, c10.status.src.file)), 'the builder copied the status source unchanged');
});

// Catches replacing the long documentary title or dropping its source to shorten UI text.
test('D1 has a source-bound short label while its original title and quote stay intact', () => {
  const d1 = node('corpus:22');
  assert.equal(d1.short_label?.value, 'D1 CAPACITY LAW');
  sourced(d1.short_label);
  assert.equal(d1.label, '22 — D1 CAPACITY LAW: global total-edge-count is INSUFFICIENT; drift must be relation-concentration-aware');
  assert.equal(d1.src.quote, d1.label);
  assert.equal(d1.framing_status.value, 'DRAFT');
  sourced(d1.framing_status);
  assert.ok(node('layer:Write Engine'), 'documentary node identity keeps its case');
  assert.equal(node('layer:write-engine'), undefined);
});

// Catches losing the recorded heldout_top1 result or inventing a count/goal from a percentage.
test('G6.1 rung cards expose their recorded edited-relation truth percentages and baseline', () => {
  const expected = [
    { field: 'rungs[0]', n: 26, percent: 91.7 },
    { field: 'rungs[1]', n: 50, percent: 50 },
    { field: 'rungs[2]', n: 100, percent: 33.3 },
  ];
  for (const row of expected) {
    const summary = index.find(item => item.source === 'results/g6_scale_n_result.json' && item.field === row.field);
    assert.ok(summary, row.field + ' has a generated card');
    const card = readJSON(resolve(SITE, 'cards', summary.card_id + '.json'));
    assert.equal(card.headline.heldout_top1?.value, row.percent, row.field + ' keeps the real rung value');
    assert.equal(card.headline.heldout_top1.unit, 'percent');
    assert.equal(card.headline.heldout_top1.plain, 'edited-relation top-1 correctness vs truth');
    assert.equal(card.headline.heldout_top1.src.path, '.' + row.field + '.heldout_top1.edited_rel.top1_correct_vs_truth');
    assert.equal(card.headline.rung_n.value, row.n);
    assert.equal(card.headline.heldout_baseline_top1.value, 100);
    for (const leaf of [card.headline.heldout_top1, card.headline.rung_n, card.headline.heldout_baseline_top1]) sourced(leaf);
    assert.equal(card.headline.hits.value, null);
    assert.equal(card.headline.out_of.value, null);
    assert.equal(card.headline.program_goal, undefined);
    const source = card.sources.find(item => item.file === 'results/g6_scale_n_result.json');
    assert.equal(source.sha256, hash(resolve(ROOT, source.file)));
  }
});

// Catches source-cleaning or accidentally promoting curated framing during this UI fix.
test('every curated entry stays DRAFT and documentary source text stays verbatim', () => {
  function check(value) {
    if (Array.isArray(value)) return value.forEach(check);
    if (!value || typeof value !== 'object') return;
    if (Object.hasOwn(value, 'status')) assert.equal(value.status, 'DRAFT');
    if (value.file && value.line) {
      const line = readFileSync(resolve(ROOT, value.file), 'utf8').split(/\r?\n/)[value.line - 1];
      assert.ok(line.includes(value.quote), 'Stale documentary citation: ' + value.file + ':' + value.line + ' — ' + value.quote);
    }
    Object.values(value).forEach(check);
  }
  check(context.contexts);
  const card = readJSON(resolve(SITE, 'cards/run-44acd672174bfa71.json'));
  sourced(card.context.question);
  sourced(card.context.status_now);
  assert.ok(card.context.status_now.value.includes('SPLIT'));
});
