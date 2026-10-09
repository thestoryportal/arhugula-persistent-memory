"""D-ML-1 fixtures exercise the shared event contract, not a science producer."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tools import mathlab_events
from tools.labviz import build, cards

ROOT = Path(__file__).resolve().parents[2]


def event(run_id, kind, **fields):
    return dict(schema=1, run_id=run_id, ts='2026-10-09T18:00:00Z', type=kind, **fields)


def started(run_id, step=2, purpose='experiment'):
    return event(run_id, 'run_started', step=step, purpose=purpose,
                 title='Reproduce the saved write on CPU', pid=4321,
                 deadline_ts='2026-10-09T18:45:00Z')


def write_stream(root, run_id, events, tail=''):
    path = root/'results/mathlab_staging/runs'/run_id/'events.jsonl'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(e)+'\n' for e in events)+tail)
    return path


def output_fixtures(root):
    """Actual output layout, with recorded-looking data to catch generic ingestion."""
    payloads = {
        'harvest_20261009T184950.056951Z/manifest.json': {
            'tier':'MATH-PROXY', 'decision_id':'D-ML-1',
            'tokenisation':{'parts':{'d-substrings-mint1_s0':{
                'observed':{'rows':[{'label':'RECONSTRUCTED'}]}}}},
            'replay_admission':{'shared_passed':True, 'admitted':[]},
            'delta_norms':{'4':{'delta_norm':12345}},
        },
        'admission_20261009T184919Z.json': {
            'terminal_sources':[{'coordinator':'astra-attempt3',
                                 'path':'results/mathlab/astra_attempt3_terminal.json'}],
            'no_other_coordinator_live_or_pending':True, 'lead':'fixture',
        },
        'harvest_launch_20261009T184919Z.log':'step 1 loss 0.25\nRUN_DONE\n',
        'astra_attempt3_terminal.json':{
            'status':'HALTED-V7', 'coordinator':'astra-attempt3', 'source_outcome':'HALTED',
        },
    }
    files = []
    for family in ('mathlab', 'mathlab_staging'):
        for name, data in payloads.items():
            path = root/'results'/family/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data if isinstance(data,str) else json.dumps(data))
            files.append(path)
    return files


def prepare(root):
    """A real Reader/build fixture, also used by the production-IIFE Node tests."""
    for path in (ROOT/'tools/labviz').glob('*.json'):
        target = root/'tools/labviz'/path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    target = root/'tools/mathlab_events.py'
    shutil.copyfile(ROOT/'tools/mathlab_events.py', target)
    spec = (ROOT/'docs/LABVIZ_V2_SPEC.md').read_text()
    (root/'docs').mkdir()
    (root/'docs/LABVIZ_V2_SPEC.md').write_text(spec[spec.index('## Forward requirement — math lab'):])
    finding = root/'logs/pending_findings/mathlab_fixture.md'
    finding.parent.mkdir(parents=True)
    finding.write_text('# Fixture estimate\nMATH-PROXY — math estimate, not evidence\n<script>not executable</script>\n')
    run = 'halted_fixture'
    stream = [started(run), event(run, 'admission', allowed=True, reasons=[]),
              event(run, 'stage_started', stage='reproduction', plain_words='Repeat the saved calculation', cap_s=2700),
              event(run, 'progress', stage='reproduction', done=3, total=6, unit='arms')]
    for name in ('context', 'law3', 'law5', 'observer-parity', 'budget-reproduction', 'stage-memory-reproduction'):
        stream.append(event(run, 'gate_result', gate_id=name, plain_words='Producer-shaped check '+name,
                            observed=8, bar=8, comparison='>=', passed=True))
    for layer in range(30):
        stream.append(event(run, 'gate_result', gate_id=f'2a-projector-arm-{layer}',
                            plain_words='Projection reproduces the write', observed=1e-7,
                            bar=1e-6, comparison='<=', passed=True))
        stream.append(event(run, 'gate_result', gate_id=f'2a-update-arm-{layer}',
                            plain_words='Write size reproduces the write', observed=1e-7,
                            bar=1e-5, comparison='<=', passed=True))
    stream += [event(run, 'resource_sample', avail_gib=12, floor_gib=8, rss_gib=1.2, cpu_pct=64),
               event(run, 'stage_finished', stage='reproduction', outcome='INVALID', summary='Stopped at the memory floor'),
               event(run, 'resource_sample', avail_gib=7, floor_gib=8, rss_gib=1.5, cpu_pct=0),
               event(run, 'finding_staged', finding_id='estimate-1', tier='MATH-PROXY',
                     summary='The saved math estimate', path=str(finding)),
               event(run, 'candidate_added', candidate_id='idea-1', source='fixture', offline=True,
                     question='Would <img src=x onerror=alert(1)> change the result?'),
               event(run, 'halted', reason='STOPPED-RESOURCE: below the memory floor', diagnostic_path='diagnostic.json')]
    write_stream(root, run, stream)
    run = 'admission_fixture'
    write_stream(root, run, [started(run, step=1, purpose='admission'),
                            event(run, 'admission', allowed=True, reasons=[]),
                            event(run, 'run_finished', outcome='PASS', summary='Admission only; no experiment ran')])
    run = 'torn_fixture'
    write_stream(root, run, [started(run)], '{"type":"run_finished"')
    for outcome in ('PASS', 'FAIL', 'INVALID'):
        run = 'calibration_'+outcome
        write_stream(root, run, [started(run, step=3),
                                event(run, 'gate_result', gate_id='calibration',
                                      plain_words='Aggregate calibration outcome', observed=outcome,
                                      bar='PASS', comparison='meets', passed=outcome=='PASS')])
    write_stream(root, 'empty_fixture', [])
    sidecar = root/'results/mathlab_staging/runs'/run/'admission.json'
    sidecar.write_text(json.dumps({'model':'fake model', 'label':'PASS', 'arm':{'para_full_n':72, 'para_n':72}}))
    output_fixtures(root)
    return stream


class MathLabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='labviz-mathlab-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.stream = prepare(self.root)

    def reader(self):
        reader = cards.Reader(self.root)
        reader.collect()
        return reader

    def card(self, run_id, reader=None):
        reader = reader or self.reader()
        matches = [c for c in reader.cards if c['identity']['name'] ==
                   f'results/mathlab_staging/runs/{run_id}/events.jsonl']
        self.assertEqual(len(matches), 1, 'one MathLab card per canonical event stream')
        return matches[0]

    def test_shared_reader_and_fold_are_the_only_run_state_authority(self):
        with patch.object(mathlab_events, 'read_events', wraps=mathlab_events.read_events) as read, \
             patch.object(mathlab_events, 'fold', wraps=mathlab_events.fold) as fold:
            reader = self.reader()
        self.assertEqual(read.call_count, 7)
        self.assertGreaterEqual(fold.call_count, 7)
        self.assertEqual(len(reader.cards), 7)
        card = self.card('halted_fixture', reader)
        expected = json.loads(cards.encoded(mathlab_events.fold(self.stream)))
        self.assertEqual(card['mathlab']['state']['value'], expected)
        self.assertEqual(card['evidence_status'], 'MATH-PROXY')
        self.assertEqual(card['label']['value'], 'math estimate, not evidence')
        self.assertEqual(len(expected['gates']), 66)
        self.assertEqual(len(expected['resource_samples']), 2)
        self.assertEqual(expected['stages'][0]['outcome'], 'INVALID')
        self.assertTrue(expected['gate_groups']['inertness']['complete'])
        self.assertFalse(expected['gate_groups']['2a']['complete'])
        self.assertFalse(any('admission.json' in name for name in reader.files))
        self.assertEqual(reader.scales['absolute_write_size']['operands'], [])

    def test_both_mathlab_output_families_are_excluded_from_generic_ingestion(self):
        files = output_fixtures(self.root)
        for path in files:
            source = path.relative_to(self.root).as_posix()
            with self.subTest(source=source):
                self.assertFalse(cards.recorded(source))
                if path.suffix == '.json':
                    self.assertEqual(cards.applied_writes(source,json.loads(path.read_text())), [])
        self.assertEqual(cards.recorded_labels(self.root), set())
        self.assertNotIn('RECONSTRUCTED', cards.label_table())
        # Identical payloads outside MathLab must still reach the generic readers.
        control = self.root/'results/ordinary_fixture'
        control.mkdir()
        for path in files[:4]:
            shutil.copyfile(path,control/path.name)
        manifest = control/'manifest.json'
        source = manifest.relative_to(self.root).as_posix()
        self.assertTrue(cards.recorded(source))
        writes = cards.applied_writes(source,json.loads(manifest.read_text()))
        self.assertEqual([item['value'] for item in writes], [12345])
        self.assertEqual(cards.recorded_labels(self.root), {'RECONSTRUCTED'})
        log = control/'harvest_launch_20261009T184919Z.log'
        self.assertEqual(build.parse_log(log.read_text(),log.relative_to(self.root).as_posix())['losses'], [[1,.25]])

    def test_sidecars_never_become_generic_cards_logs_or_scale_operands(self):
        reader = self.reader()
        self.assertEqual(len(reader.cards), 7)
        self.assertTrue(all(cards.mathlab_source(c['identity']['name']) for c in reader.cards))
        self.assertEqual(reader.runs, [])
        self.assertEqual(reader.scales['absolute_write_size']['operands'], [])
        excluded = {p.relative_to(self.root).as_posix() for p in output_fixtures(self.root)}
        self.assertFalse(excluded.intersection(reader.files))
        (self.root/'docs/c10_scoreboard.json').write_text('{"results":[]}')
        legacy = build.collect(self.root)
        self.assertEqual(legacy['runs'], [])
        self.assertEqual(legacy['logs'], [])
        self.assertIsNone(legacy['newest_log'])

    def test_torn_tail_and_invalid_middle_lines_remain_visible(self):
        path = self.root/'results/mathlab_staging/runs/torn_fixture/events.jsonl'
        start = started('torn_fixture')
        path.write_text(json.dumps(start)+'\n{"schema":99}\n'+
                        json.dumps(event('torn_fixture', 'resource_sample', avail_gib=10, floor_gib=8, rss_gib=1, cpu_pct=2))+
                        '\n{"type":"run_finished"')
        card = self.card('torn_fixture')
        errors = card['mathlab']['errors']['value']
        self.assertEqual(len(errors), 2)
        self.assertIn('line 2:', errors[0])
        self.assertIn('line 4: incomplete line', errors[1])
        self.assertEqual(card['mathlab']['state']['value']['status'], 'running')
        self.assertEqual(len(card['events']['timestamped']), 2)
        self.assertTrue(cards.validate_card(json.loads(cards.encoded(card)), self.root))

    def test_admission_receipt_never_completes_an_experiment_step(self):
        state = self.card('admission_fixture')['mathlab']['state']['value']
        self.assertEqual(state['purpose'], 'admission')
        self.assertEqual(state['outcome'], 'PASS')
        self.assertEqual(set(state['steps'].values()), {'not started'})

    def test_aggregate_calibration_retains_all_three_outcomes(self):
        reader = self.reader()
        for outcome, status in [('PASS','running'), ('FAIL','stopped: check failed'), ('INVALID','invalid: no verdict')]:
            state = self.card('calibration_'+outcome, reader)['mathlab']['state']['value']
            self.assertEqual(state['calibration_outcome'], outcome)
            self.assertEqual(state['gate_outcomes']['calibration'], outcome)
            self.assertEqual(state['status'], status)

    def test_legacy_admission_partial_gates_and_substages_keep_fold_scope(self):
        cases = [
            ('legacy_admission', [dict((k,v) for k,v in started('legacy_admission').items() if k!='purpose'),
                                 event('legacy_admission','admission',allowed=True,reasons=[]),
                                 event('legacy_admission','run_finished',outcome='PASS',summary='Receipt')],
             'admission', 'not started'),
            ('substage', [started('substage'),
                          event('substage','stage_started',stage='solve',plain_words='Solve',cap_s=900),
                          event('substage','stage_finished',stage='solve',outcome='PASS',summary='One stage'),
                          event('substage','gate_result',gate_id='law5',plain_words='Identity edit',
                                observed=True,bar=True,comparison='meets',passed=True),
                          event('substage','gate_result',gate_id='2b',plain_words='Proxy scope only',
                                observed=.3,bar=.25,comparison='<=',passed=False)],
             'experiment', 'running'),
            ('step_finished', [started('step_finished'),
                               event('step_finished','run_finished',outcome='PASS',summary='Experiment step complete')],
             'experiment', 'PASS'),
        ]
        for run, stream, purpose, step in cases:
            write_stream(self.root, run, stream)
            state = self.card(run)['mathlab']['state']['value']
            self.assertEqual(state, json.loads(cards.encoded(mathlab_events.fold(stream))))
            self.assertEqual(state['purpose'], purpose)
            self.assertEqual(state['steps']['2'], step)
            if run == 'substage':
                self.assertFalse(state['gate_groups']['inertness']['complete'])
                self.assertEqual(state['status'], 'running')

    def test_empty_directory_has_no_runs_and_empty_stream_has_no_invented_facts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'results/mathlab_staging/runs').mkdir(parents=True)
            self.assertEqual(cards.Reader(root).collect(), [])
        card = self.card('empty_fixture')
        self.assertEqual(card['mathlab']['state']['value']['status'], 'not started')
        self.assertIsNone(card['mathlab']['state']['value']['run_id'])
        self.assertEqual(card['mathlab']['errors']['value'], [])
        self.assertIsNone(card['identity']['date']['value'])

    def test_reader_resolved_leaves_and_fold_roundtrip_are_validated(self):
        card = self.card('halted_fixture')
        self.assertTrue(cards.validate_card(card, self.root))
        self.assertTrue(cards.validate_card(json.loads(cards.encoded(card)), self.root))
        reader_leaves = []
        def visit(value):
            if isinstance(value, dict):
                if 'value' in value and value.get('src',{}).get('reader'):
                    reader_leaves.append(value)
                for key, item in value.items():
                    if key not in ('value','src','sources','built'):
                        visit(item)
            elif isinstance(value, list):
                for item in value:
                    visit(item)
        visit(card)
        self.assertGreater(len(reader_leaves), 70)
        events, errors = mathlab_events.read_events(self.root/card['identity']['name'])
        normalized = {'events':events, 'errors':errors}
        for leaf in reader_leaves:
            self.assertEqual(leaf['src']['reader'], 'mathlab_events.read_events')
            self.assertEqual(cards.resolve(normalized, leaf['src']['path']), leaf['value'])
        self.assertFalse(any(x['src']['file'].endswith('.jsonl') for x in cards.json_leaves(card)))
        for mutation in ('value', 'reader', 'reader-omitted', 'reader-on-json', 'rule', 'stream-path'):
            bad = copy.deepcopy(card)
            operand = bad['mathlab']['state']['inputs'][0]
            if mutation == 'value':
                bad['mathlab']['state']['value']['status'] = 'finished'
            elif mutation == 'reader':
                operand['src']['reader'] = 'unrecognized'
            elif mutation == 'reader-omitted':
                operand['src'].pop('reader')
            elif mutation == 'reader-on-json':
                operand['src'].update(file='tools/labviz/labels.json', path='.', reader='mathlab_events.read_events')
            elif mutation == 'stream-path':
                operand['src']['file'] = 'results/mathlab_staging/runs/halted_fixture/admission.json'
            else:
                bad['mathlab']['state']['rule_src']['file'] = 'tools/labviz/labels.json'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                cards.validate_card(bad, self.root)
        path = self.root/card['identity']['name']
        path.write_text(path.read_text().replace('"schema": 1', '"schema":  1', 1))
        with self.assertRaisesRegex(ValueError, 'source hash changed'):
            cards.validate_card(card, self.root)

    def test_fold_requires_its_hashed_module_and_this_runs_canonical_events(self):
        card = self.card('halted_fixture')
        sidecar = self.root/'results/mathlab_staging/runs/halted_fixture/forged.json'
        changed = copy.deepcopy(self.stream)
        changed[-1]['reason'] = 'Forged halt'
        sidecar.write_text(json.dumps(changed))
        other = 'results/mathlab_staging/runs/admission_fixture/events.jsonl'
        for mutation in ('unhashed-module', 'sidecar', 'other-run'):
            bad = copy.deepcopy(card)
            if mutation == 'unhashed-module':
                bad['sources'] = [s for s in bad['sources'] if s['file']!='tools/mathlab_events.py']
            else:
                file = str(sidecar.relative_to(self.root)) if mutation=='sidecar' else other
                events = changed if mutation=='sidecar' else mathlab_events.read_events(self.root/other)[0]
                operand = {'value':events,'src':{'file':file,'path':'.' if mutation=='sidecar' else '.events'}}
                if mutation=='other-run':
                    operand['src']['reader'] = 'mathlab_events.read_events'
                bad['mathlab']['state']['inputs'] = [operand]
                bad['mathlab']['state']['value'] = json.loads(cards.encoded(mathlab_events.fold(events)))
                bad['sources'].append({'file':file,'sha256':cards.sha(self.root/file)})
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                cards.validate_card(bad, self.root)

    def test_findings_are_referenced_text_with_source_hashes(self):
        card = self.card('halted_fixture')
        finding = card['mathlab']['findings'][0]
        self.assertEqual(finding['event']['value']['tier'], 'MATH-PROXY')
        lines = finding['document']
        self.assertEqual([x['value'] for x in lines],
                         (self.root/'logs/pending_findings/mathlab_fixture.md').read_text().splitlines())
        self.assertEqual(lines[0]['src']['file'], 'logs/pending_findings/mathlab_fixture.md')
        self.assertIn(lines[0]['src']['file'], {x['file'] for x in card['sources']})

    def test_missing_and_outside_workspace_findings_are_explicit(self):
        run = 'finding_errors'
        stream = [started(run)]
        for i, path in enumerate(('logs/pending_findings/missing.md', '/private/tmp/not-a-labviz-finding.md')):
            stream.append(event(run, 'finding_staged', finding_id='f'+str(i), tier='MATH-PROXY', summary='Estimate', path=path))
        write_stream(self.root, run, stream)
        findings = self.card(run)['mathlab']['findings']
        self.assertIn('missing.md', findings[0]['document']['missing'])
        self.assertIn('outside workspace', findings[1]['document']['missing'])

    def test_findings_resolve_workspace_boundaries_and_empty_text_snapshots(self):
        with tempfile.TemporaryDirectory(prefix=self.root.name+'-sibling-',dir=self.root.parent) as tmp:
            outside = Path(tmp)/'outside.md'
            outside.write_text('Outside')
            linked = self.root/'logs/pending_findings/linked.md'
            linked.symlink_to(outside)
            empty = self.root/'logs/pending_findings/empty.md'
            empty.write_text('')
            run = 'reference_boundaries'
            stream = [started(run)]
            refs = [str(outside), str(linked), '../'+Path(tmp).name+'/outside.md', str(empty)]
            for i, ref in enumerate(refs):
                stream.append(event(run,'finding_staged',finding_id='f'+str(i),tier='MATH-PROXY',summary='Estimate',path=ref))
            write_stream(self.root, run, stream)
            reader = self.reader()
            finding = self.card(run, reader)['mathlab']['findings']
            for item in finding[:3]:
                self.assertIn('outside workspace', item['document']['missing'])
            self.assertEqual(finding[3]['document'], [])
            self.assertIn('logs/pending_findings/empty.md',
                          {s['file'] for s in self.card(run, reader)['sources']})
            build.build(self.root)
            self.assertEqual((self.root/'results/labviz/site/evidence/logs/pending_findings/empty.md').read_bytes(), b'')
            self.assertFalse((self.root/'results/labviz/site/evidence/logs/pending_findings/linked.md').exists())

    def test_build_mirrors_only_cited_events_and_findings_and_skips_pictures(self):
        unreferenced = self.root/'logs/pending_findings/unreferenced.md'
        unreferenced.write_text('Unreferenced text')
        inputs = {p:p.read_bytes() for family in ('mathlab', 'mathlab_staging')
                  for p in (self.root/'results'/family).rglob('*') if p.is_file()}
        with patch('tools.labviz.render.card_picture', side_effect=AssertionError('no evidence artwork for math estimates')):
            inventory = build.build(self.root)
        site = self.root/'results/labviz/site'
        index = json.loads((site/'cards/index.json').read_text())
        self.assertEqual(len(index), 7)
        for row in index:
            self.assertEqual(row['mathlab']['tier'], 'MATH-PROXY')
            self.assertEqual(row['label'], 'math estimate, not evidence')
            card = json.loads((site/'cards'/f"{row['card_id']}.json").read_text())
            self.assertTrue(cards.validate_card(card, self.root))
            self.assertTrue(cards.validate_card(card, site/'evidence'))
        evidence = site/'evidence'
        for path, content in inputs.items():
            relative = path.relative_to(self.root)
            if path.name == 'events.jsonl':
                self.assertEqual((evidence/relative).read_bytes(), content)
            else:
                self.assertFalse((evidence/relative).exists())
            self.assertEqual(path.read_bytes(), content)
        note = 'logs/pending_findings/mathlab_fixture.md'
        self.assertEqual((evidence/note).read_bytes(), (self.root/note).read_bytes())
        self.assertFalse((evidence/'logs/pending_findings/unreferenced.md').exists())
        data = (site/'data.js').read_text()
        payload = json.loads(data.removeprefix('window.LAB=').removesuffix(';\n'))
        self.assertEqual(payload['latest_log'], {})
        self.assertEqual(inventory['picture_calls'], 0)
        outputs = lambda: {p.relative_to(site).as_posix():(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns)
                           for p in site.rglob('*') if p.is_file()}
        before = outputs()
        build.build(self.root)
        self.assertEqual(outputs(), before)

    def test_warm_site_replaces_running_harvest_and_retires_generic_mathlab_outputs(self):
        run = 'harvest_fixture'
        initial = [started(run,step=1)]
        path = write_stream(self.root,run,initial)
        build.build(self.root)
        site = self.root/'results/labviz/site'
        index_file = site/'cards/index.json'
        index = json.loads(index_file.read_text())
        row = next(r for r in index if r['source']==path.relative_to(self.root).as_posix())
        self.assertEqual(row['mathlab']['status'], 'running')
        # Seed published artifacts from the old generic reader for both families.
        retired = []
        for i,family in enumerate(('mathlab','mathlab_staging')):
            item = {'card_id':f'run-retired-mathlab-{i}', 'source':f'results/{family}/harvest_launch_20261009T184919Z.log',
                    'chunk':'line-retired-mathlab'}
            retired.append({'card_id':item['card_id'], 'identity':{'name':item['source']}})
            (site/'cards'/f"{item['card_id']}.json").write_text(json.dumps(retired[-1]))
            for suffix in ('.svg','.png'):
                (self.root/'results/labviz/runs'/item['card_id']).with_suffix(suffix).write_bytes(b'obsolete proxy picture')
            index.append(item)
        index_file.write_text(json.dumps(index))
        retired_chunk = site/'cards/line-retired-mathlab.js'
        retired_chunk.write_text('window.LAB_CHUNKS=window.LAB_CHUNKS||{};window.LAB_CHUNKS["line-retired-mathlab"]='+json.dumps(retired)+';\n')
        sidecars = {p:p.read_bytes() for p in output_fixtures(self.root)}
        for source,content in sidecars.items():
            mirror = site/'evidence'/source.relative_to(self.root)
            mirror.parent.mkdir(parents=True,exist_ok=True)
            mirror.write_bytes(content)
        unrelated = site/'cards/run-unrelated.json'
        unrelated.write_text('{"identity":{"name":"results/ordinary/old.json"}}')
        unrelated_mirror = site/'evidence/results/ordinary/old.json'
        unrelated_mirror.parent.mkdir(parents=True)
        unrelated_mirror.write_text('{"preserve":true}')
        completed = initial + [event(run,'gate_result',gate_id='mint-norm-mint1_s'+str(seed),
                                    plain_words='Recorded mint norm comparison',observed={'passed':False},
                                    bar='relative norm difference <= 1e-3; not tensor identity',comparison='meets',passed=False)
                               for seed in range(3)]
        completed += [event(run,'finding_staged',finding_id='harvest-estimate',tier='MATH-PROXY',
                            summary='Operand harvest complete; math analysis pending',path='logs/pending_findings/mathlab_fixture.md'),
                      event(run,'run_finished',outcome='PASS',summary='Operand harvest completed; no behavioural promotion')]
        write_stream(self.root,run,completed)
        with patch('tools.labviz.render.card_picture',side_effect=AssertionError('no proxy artwork')):
            build.build(self.root)
        index = json.loads(index_file.read_text())
        self.assertEqual(len(index), 8)
        self.assertTrue(all(r['source'].endswith('/events.jsonl') for r in index))
        row = next(r for r in index if r['source']==path.relative_to(self.root).as_posix())
        self.assertEqual(row['mathlab']['status'], 'finished')
        card = json.loads((site/'cards'/f"{row['card_id']}.json").read_text())
        state = card['mathlab']['state']['value']
        self.assertEqual(state, json.loads(cards.encoded(mathlab_events.fold(completed))))
        self.assertEqual(state['outcome'], 'PASS')
        self.assertEqual([g['passed'] for g in state['gates']], [False]*3)
        self.assertEqual(card['evidence_status'], 'MATH-PROXY')
        self.assertEqual(card['label']['value'], 'math estimate, not evidence')
        chunk = (site/'cards'/f"{row['chunk']}.js").read_text()
        chunk_cards = json.loads(chunk.split(']=',1)[1].removesuffix(';\n'))
        self.assertEqual(next(c for c in chunk_cards if c['card_id']==card['card_id']), card)
        self.assertTrue(cards.validate_card(card,site/'evidence'))
        self.assertEqual((site/'evidence'/path.relative_to(self.root)).read_bytes(), path.read_bytes())
        self.assertTrue(card['mathlab']['findings'][0]['document'])
        for item in retired:
            self.assertFalse((site/'cards'/f"{item['card_id']}.json").exists())
            for suffix in ('.svg','.png'):
                self.assertFalse((self.root/'results/labviz/runs'/item['card_id']).with_suffix(suffix).exists())
        self.assertFalse(retired_chunk.exists())
        for source,content in sidecars.items():
            self.assertFalse((site/'evidence'/source.relative_to(self.root)).exists())
            self.assertEqual(source.read_bytes(),content)
        self.assertEqual(unrelated.read_text(), '{"identity":{"name":"results/ordinary/old.json"}}')
        self.assertEqual(unrelated_mirror.read_text(), '{"preserve":true}')

    def test_concurrent_appends_keep_card_index_chunk_hash_and_evidence_in_one_snapshot(self):
        for phase in ('reading','publishing'):
            with self.subTest(phase=phase):
                run = 'snapshot_'+phase
                initial = [started(run)]
                path = write_stream(self.root,run,initial)
                initial_bytes = path.read_bytes()
                completed = initial+[event(run,'run_finished',outcome='PASS',summary='Later append')]
                changed = []
                real_read = mathlab_events.read_events
                real_finish = cards.Reader.finish
                def append():
                    if not changed:
                        write_stream(self.root,run,completed)
                        changed.append(True)
                def read_then_append(source):
                    result = real_read(source)
                    if Path(source)==path: append()
                    return result
                def finish_then_append(reader,card):
                    real_finish(reader,card)
                    if card['identity']['name']==path.relative_to(self.root).as_posix(): append()
                hook = patch.object(mathlab_events,'read_events',side_effect=read_then_append) if phase=='reading' else \
                       patch.object(cards.Reader,'finish',new=finish_then_append)
                with hook:
                    build.build(self.root)
                self.assertEqual(changed, [True])
                site = self.root/'results/labviz/site'
                index = json.loads((site/'cards/index.json').read_text())
                row = next(r for r in index if r['source']==path.relative_to(self.root).as_posix())
                card = json.loads((site/'cards'/f"{row['card_id']}.json").read_text())
                expected = completed if phase=='reading' else initial
                state = json.loads(cards.encoded(mathlab_events.fold(expected)))
                self.assertEqual(card['mathlab']['state']['value'], state)
                self.assertEqual(row['mathlab']['status'], state['status'])
                snapshot = (site/'evidence'/path.relative_to(self.root)).read_bytes()
                self.assertEqual(snapshot, path.read_bytes() if phase=='reading' else initial_bytes)
                recorded_hash = next(s['sha256'] for s in card['sources'] if s['file']==row['source'])
                self.assertEqual(recorded_hash, hashlib.sha256(snapshot).hexdigest())
                chunk = (site/'cards'/f"{row['chunk']}.js").read_text()
                chunk_cards = json.loads(chunk.split(']=',1)[1].removesuffix(';\n'))
                self.assertEqual(next(c for c in chunk_cards if c['card_id']==card['card_id']),card)
                self.assertTrue(cards.validate_card(card,site/'evidence'))
                if phase=='publishing':
                    with self.assertRaises(ValueError) as rejection:
                        cards.validate_card(card,self.root)
                    self.assertEqual(str(rejection.exception),
                                     'leaf differs from source '+str(card['mathlab']['state']['inputs'][0]['src']))
                build.build(self.root)
                newer = json.loads((site/'cards'/f"{row['card_id']}.json").read_text())
                self.assertEqual(newer['mathlab']['state']['value']['outcome'], 'PASS')
                self.assertEqual((site/'evidence'/path.relative_to(self.root)).read_bytes(),path.read_bytes())
                self.assertTrue(cards.validate_card(newer,site/'evidence'))

    def test_unstable_capture_fails_after_three_attempts_without_publishing_or_caching(self):
        build.build(self.root)
        site = self.root/'results/labviz'
        outputs = lambda: {p.relative_to(site).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
                           for p in site.rglob('*') if p.is_file()}
        before = outputs()
        run = 'unstable_snapshot'
        path = write_stream(self.root,run,[started(run)])
        source = path.relative_to(self.root).as_posix()
        reader = cards.Reader(self.root)
        attempts = []
        real_read = mathlab_events.read_events
        def always_append(file):
            result = real_read(file)
            if Path(file)==path:
                attempts.append(True)
                with path.open('a') as stream:
                    stream.write(json.dumps(event(run,'run_finished',outcome='PASS',summary='Still appending'))+'\n')
            return result
        with patch.object(mathlab_events,'read_events',side_effect=always_append), \
             patch.object(cards,'Reader',return_value=reader), \
             self.assertRaisesRegex(ValueError, 'event stream changed during snapshot capture'):
            build.build(self.root)
        self.assertEqual(len(attempts), 3)
        self.assertNotIn(source, reader.files)
        self.assertNotIn(source, reader.hashes)
        self.assertNotIn(source, reader.snapshots)
        self.assertEqual(outputs(), before)


if __name__ == '__main__':
    unittest.main()
