const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const site = path.resolve(__dirname, '../../../projects/labviz-spec-v3/receipts/bulk/labviz/site');
const root = path.resolve(__dirname, '../../..');
function bootstrap() {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.join(site, 'data.js'), 'utf8'), context);
  return context;
}
test('Map bootstrap omits the per-run index until a reader requests it', () => {
  assert.equal(bootstrap().window.LAB.index.length, 0);
});
test('Classic deferred index restores source identities and question titles', () => {
  const context = bootstrap();
  const source = path.join(site, 'cards/index.js');
  assert.ok(fs.existsSync(source), 'The classic deferred index was not generated');
  vm.runInNewContext(fs.readFileSync(source, 'utf8'), context);
  const expected = JSON.parse(fs.readFileSync(path.join(site, 'cards/index.json')));
  const keys = ['card_id', 'source', 'field', 'line', 'title', 'chunk', 'has_writes'];
  const select = rows => rows.map(row => keys.map(key => row[key]));
  assert.equal(JSON.stringify(select(context.window.LAB.index)), JSON.stringify(select(expected)));
  assert.ok(context.window.LAB.index.some(row => row.card_id === context.window.LAB.default_run && row.has_writes));
});
test('Map summary counts stay correct before the deferred index loads', () => {
  const lab = bootstrap().window.LAB;
  const original = JSON.parse(fs.readFileSync(path.join(site, 'cards/index.json')));
  assert.ok(lab.index_counts, 'Map counts must not require loading all run rows');
  for (const id of ['exp:C10V-layerpick', 'exp:G6.1', 'corpus:22', 'model:Mistral-7B']) {
    const expected = original.filter(row => 'exp:' + row.experiment === id || row.line === id || row.era === id || row.era === id.replace(/^era:/, '') || row.model === id.replace(/^model:/, '')).length;
    assert.equal(lab.index_counts[id], expected, id);
  }
});
test('Historical template sentences are identified without changing evaluation evidence', () => {
  const lab = bootstrap().window.LAB;
  const original = JSON.parse(fs.readFileSync(path.join(root, 'program/registers/c10_evaluations.json'))).entries;
  const seeded = lab.evaluations.find(entry => entry.id === 'evaluation-0');
  assert.ok(seeded.template_fields?.includes('rules_out'), 'The historical boilerplate must be identifiable to the view');
  assert.ok(seeded.template_fields.includes('question'));
  assert.ok(seeded.template_fields.includes('leaves_open'));
  assert.ok(seeded.template_fields.includes('next_step'));
  for (let i = 0; i < original.length; i++) {
    for (const field of ['question', 'result', 'rules_out', 'leaves_open', 'next_step', 'ref']) {
      assert.equal(lab.evaluations[i][field], original[i][field], 'Source field changed: ' + field);
    }
  }
  const authored = lab.evaluations.find(entry => entry.ref === 'evidence/CORPUS/56');
  assert.equal(JSON.stringify(authored.template_fields), '[]');
  assert.equal(authored.line, 'exp:C10V-layerpick');
});
test('Cited role, label and evaluation rule tables have byte-identical evidence snapshots', () => {
  for (const name of ['gates.json','labels.json','links.json']) {
    const recorded=fs.readFileSync(path.join(root,'code/apps/labviz',name));
    const snapshot=path.join(site,'evidence/code/apps/labviz',name);
    assert.ok(fs.existsSync(snapshot),'Referenced rule table has no snapshot: '+name);
    assert.ok(fs.readFileSync(snapshot).equals(recorded),'Referenced rule table changed: '+name);
  }
});
