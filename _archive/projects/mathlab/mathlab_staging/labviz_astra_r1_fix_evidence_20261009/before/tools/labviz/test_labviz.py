"""Brief-derived regression tests. Run with .venv/bin/python -B -m unittest."""
import importlib
import json
from pathlib import Path
import re
import sys
import tempfile
import time
import unittest
import copy
import hashlib
import subprocess
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TEST_PROOF = Path(tempfile.mkdtemp(prefix='labviz-cpu-proof-'))


def recorded_log_prefix(content, expected_sha256):
    prefix=b''
    for line in content.splitlines(keepends=True):
        prefix+=line
        if hashlib.sha256(prefix).hexdigest()==expected_sha256:
            return prefix
    raise ValueError('No log prefix matches its recorded SHA-256')


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images, self.ids, self.links = [], set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'img':
            self.images.append(a['src'])
        if tag == 'a':
            self.links.append(a.get('href', ''))


class LabViewTests(unittest.TestCase):
    def builder(self):
        self.assertTrue((ROOT / 'tools/labviz/build.py').exists(), 'builder not implemented')
        return importlib.import_module('tools.labviz.build')

    def test_builder_is_present(self):
        self.builder()

    def test_whole_history_older_arm_fact_and_depth_records(self):
        b = self.builder()
        examples = {
            'c2band_compare_result.json': ('arms_raw.base', 'arms_raw.band812'),
            'c2b_depth_map_result.json': ('numeric_key_table',),
            'r1_select_readback.json': ('detail.LANDED', 'detail.DROPPED'),
            'r9_deletion_residue.json': ('secrets',),
            'd1_concentration_sweep_result.json': ('CONCENTRATED.trajectory', 'DILUTED.trajectory'),
        }
        for name, fields in examples.items():
            source = 'results/' + name
            runs = b.parse_record(json.loads((ROOT / source).read_text()), source, ROOT)
            self.assertTrue(runs, name)
            for field in fields:
                self.assertTrue(any(r['field'] == field for r in runs), (name, field))
            self.assertTrue(all(r['score'] is None for r in runs), name)
        arms = b.parse_record({'arms_raw': {'base': {'expression': 100.0, 'band': [4, 5]}}}, 'fixture.json')
        self.assertEqual(arms[0]['measurements'][0], ['expression', 100.0])
        self.assertEqual(arms[0]['band'], [4, 5])

    def test_binding_count_and_zero_are_preserved(self):
        b = self.builder()
        r = b.parse_record({'arm': {'para_full_binding_n': 0, 'para_full_n': 12,
                                   'para_n': 72, 'canon_full_n': 4, 'canon_n': 24}}, 'x.json')[0]
        self.assertEqual(r['score'], 0)
        self.assertEqual(r['out_of'], 72)

    def test_missing_and_percent_only_counts(self):
        b = self.builder()
        r = b.parse_record({'arms': {'A': {'para_full': 95.8}}}, 'old.json')[0]
        self.assertIsNone(r['score'])
        self.assertIsNone(r['out_of'])
        self.assertIsNone(r['grid'])
        self.assertEqual(r['percent'], 95.8)
        self.assertEqual(r['model'], 'model not recorded')

    def test_real_supported_schemas(self):
        b = self.builder()
        examples = {
            'legacy': 'results/c10_multitoken_value.json',
            'recipes': 'results/c10e_bandknob.json',
            'mint': 'results/c10u_mint2/r3/F_r0_mint1_s2.json',
            'reader': 'results/c10u_mint2/r3_read_after_v2.json',
            'retained': 'results/g6_scale_n_batch_result.json',
            'per-unit': 'results/c1_kvc_grid_result.json',
            'training': str(next(ROOT.glob('results/c10w_oracle/*/train/*.json')).relative_to(ROOT)),
            'numeric-arms': 'results/a2b_refresh_ks_result.json',
        }
        for schema, source in examples.items():
            with self.subTest(schema=schema):
                data = json.loads((ROOT / source).read_text())
                runs = b.parse_record(data, source)
                self.assertTrue(runs, source)
                self.assertTrue(all(r['source'] == source for r in runs))
        mint = b.parse_record(json.loads((ROOT / examples['mint']).read_text()), examples['mint'])[0]
        self.assertEqual((mint['score'], mint['out_of']), (40, 72))
        self.assertEqual(len(mint['grid']), 24)
        self.assertIn('teacher', mint['grid_label'].lower())
        train = b.parse_record(json.loads((ROOT / examples['training']).read_text()), examples['training'])[0]
        self.assertTrue(train['losses'])

    def test_exact_grid_has_unknown_cells(self):
        b = self.builder()
        rows = [{'subject': str(i), 'para_full_hits': [True, False, None]} for i in range(24)]
        r = b.parse_record({'arms': {'A': {'para_full_n': 24, 'para_n': 72}},
                            'detail': {'A': rows}}, 'x.json')[0]
        self.assertEqual(r['grid'][0], [True, False, None])
        self.assertIn('free', r['grid_label'].lower())

    def test_no_probability_invented_from_teacher_forced_hits(self):
        b = self.builder()
        r = b.parse_record({'arm': {'para_full_n': 1, 'para_n': 72, 'extra': {
            'per_position_teacher_forced': {'0': {'hits': 30, 'n': 72}}}}}, 'x.json')[0]
        self.assertEqual(r['curves'], [])

    def test_generic_facts_keep_recorded_boolean_outcomes(self):
        b = self.builder()
        r = b.parse_record({'records': [{'entity': 'A', 'retained_at_end': True},
                                        {'entity': 'B', 'retained_at_end': False}]}, 'x.json')[0]
        self.assertEqual(r['outcomes']['values'], [[True], [False]])
        self.assertEqual(r['outcomes']['columns'], ['retained_at_end'])

    def test_older_per_run_and_injection_tables(self):
        b = self.builder()
        source = 'results/b1_7b_dose_response_result.json'
        runs = b.parse_record(json.loads((ROOT / source).read_text()), source)
        self.assertEqual(len([r for r in runs if r['field'].startswith('per_run[')]), 9)
        self.assertTrue(all(r['model'] == 'Qwen2.5-7B' for r in runs))
        source = 'results/c10s_solvefeas/inject.json'
        runs = b.parse_record(json.loads((ROOT / source).read_text()), source)
        self.assertTrue(any(r['field'] == 'rows' for r in runs))

    def test_layer_sizes_match_only_their_arm(self):
        b = self.builder()
        d = {'recipes': {'R': {'arms': {'A': {'para_full_n': 1}, 'B': {'para_full_n': 2}},
              'delta_norms': {'A': {'4': {'delta_norm': 3.0}}, 'B': {'8': {'delta_norm': 9.0}}}}}}
        runs = b.parse_record(d, 'x.json')
        self.assertEqual(runs[0]['writes'], {'4': 3.0})
        self.assertEqual(runs[1]['writes'], {'8': 9.0})

    def test_primary_mint_arm_has_its_recorded_write_sizes(self):
        b = self.builder()
        source = 'results/c10u_mint2/r3/F_r0_mint1_s2.json'
        data = json.loads((ROOT / source).read_text())
        r = b.parse_record(data, source)[0]
        self.assertEqual(r['writes']['4'], data['recipe']['delta_norms']['candidate']['4']['delta_norm'])

    def test_model_metadata_is_source_bound(self):
        b = self.builder()
        r = b.parse_record({'model': 'Qwen/Qwen2.5-7B', 'config': {'band': [8, 12]},
                            'arms': {'A': {'para_full_n': 5}}}, 'x.json')[0]
        self.assertEqual(r['model'], 'Qwen2.5-7B')
        self.assertEqual(r['band'], [8, 12])
        self.assertEqual(r['layers'], 28)
        self.assertEqual(r['layer_source'], 'CORPUS/19_B1_SIZE_DENSITY.md:11')
        r = b.parse_record({'S7': {'model': 'GPT-6-Astra'}, 'arms': {'A': {'para_full_n': 5}}}, 'x.json')[0]
        self.assertEqual(r['model'], 'model not recorded')

    def test_explicit_model_name_outside_catalog_is_retained(self):
        b = self.builder()
        r = b.parse_record({'model': 'AnotherRecordedModel', 'num_hidden_layers': 4,
                            'config': {'band': [1,3]}, 'arm': {'para_full_n': 1}}, 'x.json')[0]
        self.assertEqual(r['model'], 'AnotherRecordedModel')
        self.assertEqual(r['layers'], 4)
        self.assertEqual(r['band'], [1,3])

    def test_log_counts_loss_and_terminal_status(self):
        b = self.builder()
        text = 'step 10 loss 2.25\n A1_single n: canon 24/24 para 0/72 L1 0/12 L3 30/30 ppl 21.0->22.0\nRUN_DONE\n'
        log = b.parse_log(text, 'results/x/behavior.log')
        self.assertEqual(log['losses'], [[10, 2.25]])
        self.assertEqual(log['observations'][0]['score'], 0)
        self.assertFalse(log['running'])

    def test_evaluations_come_from_scoreboard(self):
        b = self.builder()
        s = json.loads((ROOT / 'docs/c10_scoreboard.json').read_text())
        e = b.seed_evaluations(s)
        self.assertEqual(len(e['entries']), len(s['results']))
        for row, entry in zip(s['results'], e['entries']):
            self.assertEqual(entry['source_result'], row)
            for field in ('question', 'result', 'rules_out', 'leaves_open', 'next_step'):
                self.assertTrue(entry[field])

    def test_every_results_folder_and_corpus_header_is_surveyed(self):
        b = self.builder()
        inventory = b.collect(ROOT)
        expected = {str(p.relative_to(ROOT)) for p in (ROOT / 'results').iterdir()
                    if p.is_dir() and p.name != 'labviz'}
        self.assertTrue(expected <= set(inventory['survey']))
        self.assertEqual(len(inventory['scoreboard']['results']), len(inventory['history']))
        self.assertEqual(len(list((ROOT / 'CORPUS').glob('[0-9][0-9]_*.md'))), len(inventory['corpus']))
        self.assertTrue(all('model' in r for r in inventory['runs']))
        self.assertTrue(any(r['model'] == 'Qwen2.5-7B' for r in inventory['runs']))

    def test_earlier_model_branches_have_dated_source_cards(self):
        inv = self.builder().collect(ROOT)
        notes = [r for r in inv['runs'] if r['schema'] == 'historical model note']
        self.assertTrue({'Llama-3.1-8B','Llama-3.2-3B','Mistral-7B'} <= {r['model'] for r in notes})
        self.assertTrue(all(r['date'] == '2026-06-15' for r in notes))
        self.assertTrue(all(r['score'] is None for r in notes))

    def test_runs_use_recorded_time_within_the_same_day(self):
        b = self.builder()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'docs').mkdir(); (root/'results').mkdir(); (root/'CORPUS').mkdir()
            (root/'docs/c10_scoreboard.json').write_text(json.dumps({'results': [], 'brief': 'Test'}))
            for name,hour in [('z-old.json','01'),('a-new.json','20')]:
                (root/'results'/name).write_text(json.dumps({'when_utc': f'2026-10-07T{hour}:00:00+00:00',
                    'arm': {'para_full_n': 1, 'para_n': 72}}))
            self.assertEqual(b.collect(root)['runs'][0]['source'],'results/a-new.json')

    def test_phone_css_contract(self):
        b = self.builder()
        css = (ROOT / 'tools/labviz/style.css').read_text()
        self.assertIn('box-sizing: border-box', css)
        self.assertIn('max-width: 100%', css)
        self.assertIn('min-width: 0', css)
        self.assertIn('overflow-wrap: anywhere', css)
        self.assertIn('min-height: 44px', css)
        element_rules = re.sub(r'@media[^\{]+', '', css)
        for value in re.findall(r'min-width:\s*(\d+)px', element_rules):
            self.assertLessEqual(int(value), 390)

    def test_build_round_trip_idempotent_missing_fields_and_source_safety(self):
        b = self.builder()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir(); (root / 'results/old').mkdir(parents=True)
            (root / 'CORPUS').mkdir()
            board = {'brief': 'Test', 'goal': 61, 'out_of': 72,
                     'results': [{'date': '2026-06-25', 'name': 'Old', 'best': 1,
                                  'score': '1 of 72', 'kind': 'write', 'verdict': 'Partial', 'ref': 'CORPUS/06'}], 'queue': []}
            (root / 'docs/c10_scoreboard.json').write_text(json.dumps(board))
            source = root / 'results/old/run.json'
            source.write_text(json.dumps({'model': 'Qwen/Qwen2.5-3B', 'arm': {'para_full_n': 1, 'para_n': 72}}))
            (root / 'CORPUS/06_TEST.md').write_text('# Test\n_Date 2026-06-25._\n## VERDICT — PARTIAL\n')
            (root / 'docs/c10_evaluations.json').write_text(json.dumps(b.seed_evaluations(json.loads((root / 'docs/c10_scoreboard.json').read_text()))))
            before = source.read_bytes()
            b.build(root)
            site = root / 'results/labviz/site'
            html = (site / 'index.html').read_text(); page = Page(); page.feed(html); page.close()
            self.assertIn('not recorded for this run', html)
            self.assertTrue({'now', 'runs', 'model', 'models', 'history', 'learn', 'evaluations'} <= page.ids)
            self.assertTrue(page.images)
            for src in page.images:
                self.assertTrue((site / src).exists(), src)
            for link in page.links:
                if link.startswith('#run-'):
                    self.assertIn(link[1:], page.ids)
            imgs = list((root / 'results/labviz/runs').glob('*.svg'))
            self.assertTrue(imgs)
            self.assertTrue(all(p.with_suffix('.png').exists() for p in imgs))
            saved = {p.name: p.read_bytes() for p in imgs}
            outputs=lambda: {p.relative_to(root).as_posix():(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns)
                             for p in (root/'results/labviz').rglob('*') if p.is_file()}
            warm_before=outputs(); started=time.perf_counter()
            warm_inventory=b.build(root)
            elapsed=time.perf_counter()-started; warm_after=outputs()
            self.assertEqual(warm_before,warm_after)
            self.assertEqual(warm_inventory['picture_calls'],0)
            proof=TEST_PROOF/'warm-fixture-check.json'
            proof.parent.mkdir(parents=True,exist_ok=True)
            proof.write_text(json.dumps({'kind':'Controlled small fixture; current production builder; no live sources',
                                         'changed_outputs':[],'picture_calls':0,'outputs_checked':len(warm_before),
                                         'identical_bytes':True,'unchanged_mtimes':True,'elapsed_seconds':elapsed},indent=2)+'\n')
            self.assertEqual(html, (site / 'index.html').read_text())
            self.assertEqual(saved, {p.name: p.read_bytes() for p in imgs})
            self.assertEqual(before, source.read_bytes())
            efile = root / 'docs/c10_evaluations.json'
            e = json.loads(efile.read_text()); e['entries'][0]['next_step'] = 'Operator update'
            efile.write_text(json.dumps(e)); b.build(root)
            self.assertIn('Operator update', (site / 'index.html').read_text())

    def test_no_science_imports(self):
        b = self.builder()
        for p in (ROOT / 'tools/labviz').glob('*.py'):
            self.assertNotRegex(p.read_text(), r'(?m)^\s*(?:from|import)\s+(?:torch|transformers|experiments|memit_dry_run)\b')

    def test_saved_picture_text_does_not_clip_at_right_edge(self):
        b = self.builder()
        from tools.labviz.render import image
        import matplotlib.image as mpimg
        with tempfile.TemporaryDirectory() as tmp:
            r = b.parse_record({'arm': {'para_full_n': 1, 'para_n': 72}}, 'results/c10u/test.json')[0]
            r['title'] = 'Give a name one or two new vocabulary words · one new word · block F · replicate 0 · seed 2'
            out = Path(tmp) / 'run'; image(r,out)
            pixels = mpimg.imread(out.with_suffix('.png'))
            self.assertLess(float(pixels[:, -5:, :3].max()), .7, 'text touches/crosses the right image edge')

    def test_saved_picture_title_and_score_do_not_overlap(self):
        b = self.builder()
        from tools.labviz.render import image
        import xml.etree.ElementTree as ET
        with tempfile.TemporaryDirectory() as tmp:
            r = b.parse_record({'arm': {'para_full_n': 1, 'para_n': 72}}, 'results/c10u/test.json')[0]
            r['title'] = 'Give a name one or two new vocabulary words · one new word · block F · replicate 0 · seed 2'
            out = Path(tmp) / 'run'; image(r, out)
            headings = []
            for e in ET.parse(out.with_suffix('.svg')).iter('{http://www.w3.org/2000/svg}text'):
                if e.text == '1 of 72 reworded answers':
                    self.assertGreaterEqual(float(e.get('y')) - max(headings), 12)
                    break
                match = re.search(r'translate\([^ ]+ ([^)]+)\)', e.get('transform', ''))
                if match:
                    headings.append(float(match[1]))
            else:
                self.fail('score text was not saved')


class LabViewV2Tests(unittest.TestCase):
    """The numbered contract in labviz_v2_codex_brief.md, independently asserted."""
    _reader = None

    def api(self):
        self.assertTrue((ROOT/'tools/labviz/cards.py').is_file(), 'v2 typed recorded reader is not implemented')
        return importlib.import_module('tools.labviz.cards')

    def reader(self):
        api = self.api()
        if self.__class__._reader is None:
            self.__class__._reader = api.Reader(ROOT)
            self.__class__._reader.collect()
        return self.__class__._reader

    def card(self, source, field):
        return self.reader().find(source, field)

    def v(self, leaf):
        return leaf['value']

    def test_v2_01_leaf_integrity_and_jq_cross_check(self):
        a=self.api(); r=self.reader()
        snapshots=[]
        for card in r.cards:
            try:
                a.validate_card(card, ROOT, r.scales)
            except ValueError as error:
                live='results/c10w_oracle/p2_20261008T034226_086980Z/p2-eval.log'
                self.assertEqual(str(error),'source hash changed: '+live)
                changed=[s for s in card['sources'] if hashlib.sha256((ROOT/s['file']).read_bytes()).hexdigest()!=s['sha256']]
                self.assertEqual([s['file'] for s in changed],[live])
                prior=recorded_log_prefix((ROOT/live).read_bytes(),changed[0]['sha256'])
                with tempfile.TemporaryDirectory() as tmp:
                    snapshot=Path(tmp)
                    for item in card['sources']:
                        destination=snapshot/item['file']; destination.parent.mkdir(parents=True,exist_ok=True)
                        if item['file']==live: destination.write_bytes(prior)
                        else: destination.symlink_to(ROOT/item['file'])
                    a.validate_card(card,snapshot,r.scales)
                receipt=TEST_PROOF/'validation-snapshots'/changed[0]['sha256']/Path(live).name
                receipt.parent.mkdir(parents=True,exist_ok=True); receipt.write_bytes(prior)
                snapshots.append({'card_id':card['card_id'],'source':live,'sha256':changed[0]['sha256'],
                                  'fixture':receipt.as_posix(),
                                  'kind':'SHA-exact earlier log prefix; original live file untouched; production rejection preserved'})
        proof=TEST_PROOF/'live-log-validation.json'
        proof.write_text(json.dumps({'snapshots':snapshots,'production_validator_unchanged':True},indent=2)+'\n')
        leaves=[]
        for card in r.cards:
            leaves.extend(a.json_leaves(card))
        by_source={}
        for leaf in leaves:
            by_source.setdefault(leaf['src']['file'],[]).append(leaf)
        samples=[items[0] for items in by_source.values()]
        samples += [leaf for leaf in leaves if '[' in leaf['src']['path']][:60]
        self.assertGreaterEqual(len(samples),50)
        verified=[]
        for leaf in samples:
            p=subprocess.run(['/usr/bin/jq','-c',leaf['src']['path'],str(ROOT/leaf['src']['file'])],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr); self.assertTrue(p.stdout.strip())
            self.assertEqual(json.loads(p.stdout),leaf['value'])
            verified.append(leaf)
        proof=TEST_PROOF/'jq-leaves.json'
        proof.parent.mkdir(parents=True,exist_ok=True)
        proof.write_text(json.dumps(verified,indent=2)+'\n')

    def test_v2_02_written_layers_and_full_precision(self):
        self.api()
        b0=self.card('results/c10v_layerpick/pass1.json','recipes.B0.arms.A7_coined_coined')
        b=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        self.assertEqual({x['layer'] for x in b0['per_layer'] if self.v(x['written'])},{8})
        self.assertEqual(self.v(b0['parts']['band']),[4,5,6,7,8])
        self.assertEqual({x['layer'] for x in b['per_layer'] if self.v(x['written'])},set(range(4,9)))
        self.assertEqual(self.v(next(x['write_size'] for x in b['per_layer'] if x['layer']==8)),16.31455421447754)

    def test_v2_03_roles_badges_and_wrong_reader(self):
        a=self.api()
        source='results/c10v_layerpick/pass1.json'
        c=self.card(source,'recipes.B.arms.A7_coined_coined')
        self.assertEqual((self.v(c['headline']['hits']),self.v(c['headline']['out_of']),self.v(c['headline']['program_goal']),self.v(c['label'])),(12,72,61,'NULL'))
        for field,role in [('recipes.B.arms.A1_single','control'),('recipes.A.arms.A7_coined_coined','reference'),('recipes.Bshuf.arms.A7_coined_coined','shuffled-control')]:
            c=self.card(source,field); self.assertEqual(self.v(c['identity']['role']),role)
            self.assertNotIn('program_goal',c['headline'])
        w=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json','recipes.oracle_p1.arms.A7_coined_coined')
        self.assertEqual(self.v(w['headline']['hits']),70); self.assertIsNone(self.v(w['label']))
        self.assertEqual(self.v(w['interim_label']),'PARTIAL-CEILING-LOCALITY-COST')
        self.assertIn('ORACLE MEASUREMENT',self.v(w['oracle_class']))
        u=self.card('results/c10u_mint2/r3/F_r0_mint1_s0.json','arm')
        replica=self.card('results/c10u_mint2/r3/F_r1_mint1_s0.json','arm')
        self.assertEqual(self.v(u['label']),'LEAD'); self.assertIsNone(self.v(replica['label']))
        self.assertIn('replica of mint1_s0',self.v(replica['replica_note']))
        identity=dict(family='c10v_layerpick',recipe='B',arm='A7_coined_coined',seed=None,replicate=None,sha256='a')
        self.assertTrue(a.join_matches(identity,identity))
        for key in identity:
            bad={**identity,key:'wrong'}; self.assertFalse(a.join_matches(identity,bad),key)
        self.assertEqual(a.label_class('NEW-UNKNOWN'), 'unknown')
        r5=self.card('results/r5_paraphrase_robustness.json','arms.NOVEL_single')
        self.assertEqual(self.v(r5['label']),'CHARACTERIZATION'); self.assertNotIn('program_goal',r5['headline'])
        g=self.card('results/g6_scale_n_result.json','records')
        self.assertEqual(self.v(g['context']['status_now']),'SPLIT (cross-entity FALSIFIED)')
        self.assertNotIn('program_goal',g['headline'])

    def test_v2_04_label_transcription(self):
        a=self.api()
        self.assertEqual(json.loads((ROOT/'tools/labviz/labels.json').read_text()),a.labels_from_spec(ROOT))
        for label in a.recorded_labels(ROOT):
            self.assertIn(label,a.label_table())
        self.assertTrue(all(k.startswith('PASS') for k,v in a.label_table().items() if v=='pass'))
        source=ROOT/'results/c10x_enginepath_rerun3/reader.json'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),'b3debe4a85371902e155394e3bd054a3d214cf585a05f614e105296be022bdd9')
        arm=json.loads(source.read_text())['arms']['I-2']
        self.assertEqual(arm['label'],'INVALID-CONTROLS'); self.assertEqual(arm['qualifiers'],[])
        self.assertEqual(a.label_class(arm['label']),'halted-invalid')
        self.assertEqual(a.label_class('INVALID-CONTROLS-UNDERFIT'),'halted-invalid')
        row=next(line for line in (ROOT/'docs/LABVIZ_V2_SPEC.md').read_text().splitlines() if line.startswith('  | ') and '`INVALID-CONTROLS`' in line)
        self.assertIn('control checks failed and the target failed the fit screen',row)
        self.assertIn('not a process halt',row)
        self.assertIn('CORPUS/58_C10X_ENGINEPATH.md:66–68',row)

    def test_v2_05_every_recorded_gate_and_boundaries(self):
        a=self.api(); counts={'c10v_layerpick':0,'c10u_mint2':0,'c10w_oracle':0}
        for c in self.reader().cards:
            if c['identity']['field'] not in ('arm', 'recipes.B.arms.A7_coined_coined','recipes.B0.arms.A7_coined_coined','recipes.Bshuf.arms.A7_coined_coined','recipes.oracle_p1.arms.A7_coined_coined'): continue
            for g in c.get('gates',[]):
                if self.v(g.get('passed',{'value':None})) is not None:
                    self.assertTrue(a.gate_consistent(g),g)
                    counts[c['identity']['family']]+=1
        self.assertEqual(counts,{'c10v_layerpick':15,'c10u_mint2':49,'c10w_oracle':7})
        c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        g=next(g for g in c['gates'] if g['name']=='described_as')
        self.assertEqual(self.v(g['observed']),86.17); self.assertEqual(self.v(g['reference_line']),87.0); self.assertFalse(self.v(g['passed']))
        for value,want in [(87,True),(86.99,False)]: self.assertEqual(a.rule_outcome(value,87,'≥'),want)
        for value,want in [(4,True),(5,False)]: self.assertEqual(a.rule_outcome(value,4,'≤'),want)
        bad=copy.deepcopy(g); bad['passed']['value']=True; self.assertFalse(a.gate_consistent(bad))
        for value in [None,float('nan'),float('inf')]:
            row=a.gauge_fixture(value,90,True); self.assertNotIn('reference_line',row); self.assertNotIn('passed',row)
        for value in [None,float('nan'),float('inf')]:
            row=a.gauge_fixture(86,value,False); self.assertNotIn('reference_line',row); self.assertNotIn('passed',row)
        for field in ['recipes.closedform.arms.A7_coined_coined','recipes.oracle_canon_s0.arms.A7_canon']:
            w=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json',field)
            self.assertTrue(any('reference_line' in g for g in w['gates']))
            self.assertTrue(all(g['judgement']!='recorded' for g in w['gates']))

    def test_v2_06_fact_strips_and_missing_cells(self):
        a=self.api(); c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        self.assertEqual(len(c['per_fact']),24); self.assertEqual(self.v(c['per_fact'][0]['rewordings_hit']),[True,True,True])
        u=self.card('results/c10u_mint2/r3/F_r0_mint1_s0.json','arm')
        self.assertEqual(u['per_fact'][0]['hit_kind'],'teacher-forced')
        self.assertIsNone(a.strip_cell({'value':None}))

    def test_v2_07_stimulus_role_order_and_hash(self):
        a=self.api(); r=self.reader()
        c=self.card('results/c10e_bandknob.json','recipes.baseline.arms.A7_coined_coined')
        self.assertEqual(self.v(c['stimulus']['questions']),["{}'s capital city is called","If you visit {}, its capital city is","The main city and seat of government of {} is"])
        c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        self.assertEqual(self.v(c['stimulus']['canonical']),'The capital of {} is the city of')
        table=json.loads((ROOT/'tools/labviz/stimulus.json').read_text())
        self.assertTrue(a.transcription_valid(table,ROOT))
        bad=copy.deepcopy(table); entries=bad['c10_harness']['entries']; entries[1]['text'],entries[2]['text']=entries[2]['text'],entries[1]['text']
        self.assertFalse(a.transcription_valid(bad,ROOT))
        self.assertIsNone(a.transcribed_stimulus({'identity':{'source_sha256':{'experiments/track_c/c10e_bandknob.py':'wrong'}}},ROOT)['canonical']['value'])
        w=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json','recipes.oracle_p1.arms.A7_coined_coined')
        self.assertTrue(a.generated_order_valid(w))

    def test_v2_08_layer_map_uses_B_reading(self):
        self.api(); c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined'); m=c['layer_map']
        self.assertEqual((len(self.v(m['G_table'])),len(self.v(m['G_table'])[0])),(24,5))
        self.assertEqual(len(self.v(m['margins'])),24); self.assertEqual(len(self.v(m['repeat_margins'])),24)
        self.assertTrue(self.v(m['map_reproduced']))
        self.assertEqual(self.v(m['spearman']),-0.3162875387734472)
        self.assertEqual(m['spearman']['src']['path'],'.readings.B.spearman_G_edge')

    def test_v2_09_training_has_only_recorded_steps(self):
        self.api(); cards=[c for c in self.reader().cards if c.get('training')]
        self.assertGreaterEqual(len(cards),10)
        for c in cards:
            self.assertEqual(len(self.v(c['training']['losses'])),40); self.assertEqual(len(self.v(c['training']['step_seconds'])),400)
            self.assertEqual([x['step'] for x in self.v(c['training']['losses'])],list(range(10,401,10)))
            self.assertNotIn('step_answers',c['training'])

    def test_v2_10_untouched_basis_and_written_modules(self):
        self.api(); w=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json','recipes.oracle_p1.arms.A7_coined_coined')
        self.assertEqual(self.v(w['parts']['untouched_basis']),"the 434 base tensors were hash-verified frozen during adapter training; the evaluated model has the adapter's ΔW merged into down_proj 4–8; `base_band_hash` = `final_band_hash` shows the base was restored after evaluation")
        self.assertEqual({x['layer'] for x in w['per_layer'] if self.v(x['written'])},set(range(4,9)))
        v=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        self.assertEqual(self.v(v['parts']['untouched_basis']),'by design (the engine writes only down_proj)')

    def test_v2_11_context_registry_rules_and_namespaces(self):
        self.api(); p=self.reader().program
        self.assertEqual(len(p.registry),55)
        self.assertEqual(len({row['id'] for row in p.registry}),55)
        self.assertEqual(set(p.tables['experiments']),{row['id'] for row in p.registry})
        row=next(x for x in p.registry if x['id']=='C10X-enginepath')
        self.assertEqual(row['line'],61); self.assertEqual(row['corpus'],['58'])
        self.assertEqual(row['decision'],'D-C10x-enginepath'); self.assertEqual(row['hypothesis'],['H-11'])
        self.assertIn('results/c10x_enginepath_rerun3/',row['results'])
        entry=p.tables['experiments'][row['id']]
        self.assertEqual(entry['era'],'c10'); self.assertEqual(entry['status'],'DRAFT')
        self.assertEqual(entry['question'],row['question'])
        self.assertIn('The reader recorded INVALID-CONTROLS; the erratum reports INVALID-CONTROLS-UNDERFIT.',entry['measure'])
        self.assertIn({'file':'results/c10x_enginepath_rerun3/reader.json','path':'.arms["I-2"].label','value':'INVALID-CONTROLS'},entry['citations']['measure'])
        self.assertTrue(any(c['file']=='CORPUS/58_C10X_ENGINEPATH.md' and c['line']==66 and 'INVALID-CONTROLS-UNDERFIT' in c['quote'] for c in entry['citations']['measure']))
        context=p.context('results/c10x_enginepath_rerun3/reader.json',{})
        self.assertEqual(context['matched_by'],'registry_path')
        self.assertEqual(context['experiment']['node_id'],'exp:C10X-enginepath')
        self.assertEqual(context['era']['node_id'],'era:c10')
        self.assertEqual(context['status_now']['value'],row['status'])
        self.assertEqual(next(x for x in p.registry if x['id']=='C10U-mint2')['decision'],'D-C10u-mint2')
        self.assertTrue({'exp:A7','hyp:A:A7','arm:A7_coined_coined','track:track_e','runbook-track:E'} <= {n['node_id'] for n in p.graph['nodes']})
        p.validate()
        from tools.labviz.cards import resolve
        for node in p.graph['nodes']:
            src=node.get('src',{})
            if 'path' in src:
                self.assertTrue(src['path'].startswith('.'))
                resolve(json.loads((ROOT/src['file']).read_text()),src['path'])
        from tools.labviz.context import expand_braces, decision_ids
        self.assertEqual(expand_braces('results/x{,_a,_b}.json'),['results/x.json','results/x_a.json','results/x_b.json'])
        self.assertEqual(decision_ids('D-ID ROUTING-BLOCKED-UNDERFIT D-C10u-mint2'),['D-C10u-mint2'])
        ctx=p.context('results/c10u_mint2/r2/F_r0_mint1_s0.json',{'decision_id':'D-C10u-mint2'})
        self.assertIn('attempt not named',ctx['match_note']['value'])

    def test_v2_12_non_C10_content(self):
        self.api(); f=ROOT/'results/labviz/review/v2-build/browser-tests.json'
        self.assertTrue(f.exists(),'browser non-C10 checks not recorded')
        self.assertTrue(json.loads(f.read_text())['non_c10_content'])

    def test_v2_13_focus_map_expected_chain(self):
        self.api(); p=self.reader().program
        reached=p.focus('cond:C10'); self.assertIn('spec:§8.9',reached)
        line=(ROOT/'docs/SPEC_EXPERIMENT_OVERLAY.md').read_text().splitlines()[21]
        from tools.labviz.context import decision_ids
        self.assertTrue({'dec:'+d for d in decision_ids(line)} <= reached)
        self.assertIn('era:t-branch',p.focus('model:Mistral-7B'))

    def test_v2_14_readability_and_measurement_fixtures(self):
        self.api(); css=(ROOT/'tools/labviz/style.css').read_text()
        for size in re.findall(r'font-size:\s*([\d.]+)px',css): self.assertGreaterEqual(float(size),13)
        self.assertNotIn('fillText',(ROOT/'tools/labviz/model.js').read_text())
        f=ROOT/'results/labviz/review/v2-build/browser-tests.json'; self.assertTrue(f.exists(),'rendered text fixtures have not run')
        self.assertEqual(json.loads(f.read_text())['font_fixtures'],[False,False,True])

    def test_v2_15_payload_and_classic_scripts(self):
        self.api(); site=ROOT/'results/labviz/site'
        html=(site/'index.html').read_text(); self.assertNotIn('type="module"',html)
        self.assertLessEqual(sum((site/name).stat().st_size for name in ['index.html','style.css','app.js','model.js','data.js']),1000000)
        self.assertTrue(list((site/'cards').glob('*.js')))

    def test_v2_16_ingestion_boundary(self):
        a=self.api()
        for path,data in [('results/replays/a.json',{}),('results/sandbox/a.json',{}),('results/c10x/telemetry/a.json',{}),('results/a.json',{'evidence_status':'NOT EVIDENCE: replay'}),('results/a.json',{'evidence_status':'EXPLORATORY: sandbox'})]: self.assertFalse(a.recorded(path,data))
        self.assertTrue(a.recorded('results/a.json',{'arm':{'para_full_n':0}}))

    def test_v2_17_links_phase_scoped(self):
        a=self.api(); a.validate_links(ROOT)
        p1=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json','recipes.oracle_p1.arms.A7_coined_coined')
        self.assertIsNotNone(p1['plain_words']['question']['value'])
        for source in ('results/c10w_oracle/p2_20261008T034226_086980Z/eval.json',
                       'results/c10w_oracle/p1_20261007T223707_598959Z-other/eval.json'):
            card={'identity':{'name':source}}
            self.reader().evaluation(card)
            for leaf in card['plain_words'].values():
                self.assertIsNone(leaf['value'])
                self.assertEqual(leaf['missing'],'no plain-words evaluation linked yet')

    def test_v2_18_compare_subject_join_and_refusals(self):
        a=self.api(); c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        shuffled=copy.deepcopy(c); shuffled['per_fact'].reverse()
        self.assertTrue(a.compare(c,shuffled)['eligible'])
        for kind in ['answer','templates','population','scoring']:
            bad=copy.deepcopy(c)
            if kind=='answer': bad['per_fact'][0]['answer']['value']='changed'
            if kind=='templates': bad['stimulus']['questions']['value']=['changed']
            if kind=='population': bad['per_fact'].pop()
            if kind=='scoring': bad['per_fact'][0]['hit_kind']='teacher-forced'
            self.assertFalse(a.compare(c,bad)['eligible'],kind)

    def test_v2_19_build_safety_and_round_trip(self):
        a=self.api(); self.assertEqual(hashlib.sha256((ROOT/'tools/labviz_serve.sh').read_bytes()).hexdigest(),'c90afb9ce1bd8c3b54af95f4534f055404587a0105045e931ee34d6cb9a05a4b')
        for path in (ROOT/'tools/labviz').glob('*.py'):
            if path.name=='test_labviz.py': continue
            self.assertNotRegex(path.read_text(),r'\b(subprocess|multiprocessing|os\.system)\b')
        self.assertTrue(Path(tempfile.gettempdir()).is_relative_to('/private/tmp/labviz-review/test-tmp'))

    def test_v2_20_derivations_population_and_mutations(self):
        a=self.api(); r=self.reader(); c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        self.assertEqual(c['scale']['max']['value'],113.7967300415039)
        for part in ['configured','condition']:
            bad=copy.deepcopy(c)
            leaf=bad['per_layer'][0]['configured'] if part=='configured' else bad['context']['condition']
            leaf['inputs'].pop()
            with self.assertRaises(ValueError): a.validate_card(bad,ROOT,r.scales)
        bad=copy.deepcopy(c); bad['scale']['max']['value']=1
        with self.assertRaises(ValueError): a.validate_card(bad,ROOT,r.scales)
        bad=copy.deepcopy(r.scales); bad['absolute_write_size']['operands'].pop()
        with self.assertRaises(ValueError): a.validate_population(r.cards,bad,ROOT)

    def test_v2_21_write_kinds_separate(self):
        a=self.api()
        for src,data in [('results/x/step0_offline.json',{'per_layer':{'4':{'dW_fro':999}}}),('results/x/inject.json',{'delta_norms':{'A7':{'4':{'delta_norm':999}}}})]: self.assertEqual(a.applied_writes(src,data),[])

    def test_v2_22_hparams_and_model_revision_bindings(self):
        a=self.api(); record=json.loads((ROOT/'results/c10v_layerpick/pass1.json').read_text())
        parts=a.bound_parts(record,ROOT); self.assertEqual(parts['structure']['layers']['value'],36)
        record['identity']['source_sha256']['configs/hparams/qwen25_3b_memit_hparams.json']='wrong'
        self.assertIsNone(a.bound_parts(record,ROOT)['written_module']['value'])
        record['model']['revision']='wrong'; self.assertIsNone(a.bound_parts(record,ROOT)['structure']['layers']['value'])

    def test_v2_23_picker_newest_with_writes(self):
        a=self.api(); c=self.card('results/c10v_layerpick/pass1.json','recipes.B.arms.A7_coined_coined')
        old=copy.deepcopy(c); old['card_id']='old'; old['identity']['date']['value']='2026-01-01'
        new=copy.deepcopy(c); new['card_id']='new'; new['identity']['date']['value']='2026-10-08'
        empty=copy.deepcopy(new); empty['card_id']='empty'; empty['identity']['date']['value']='2026-10-09'; empty['per_layer']=[]
        self.assertEqual(a.newest_written([old,empty,new]),'new')

    def test_v2_24_events_utc_and_untimestamped(self):
        a=self.api()
        events=[{'at':'2026-10-07T22:00:00-06:00','source':'b','index':1},{'at':'2026-10-08T04:00:00Z','source':'a','index':2},{'source':'c','index':10},{'source':'c','index':2}]
        timed,untimed=a.order_events(events)
        self.assertEqual([x['source'] for x in timed],['a','b']); self.assertEqual([x['index'] for x in untimed],[2,10])
        w=self.card('results/c10w_oracle/p1_20261007T223707_598959Z/eval.json','recipes.oracle_p1.arms.A7_coined_coined')
        self.assertTrue(any(e['name']=='STAGE_EXIT=0' for e in w['events']['untimed']))
        self.assertTrue(any(e['name']=='training loss' for e in w['events']['untimed']))

    def test_v2_25_warm_rebuild_skips_pictures(self):
        self.api(); f=ROOT/'results/labviz/review/fix-round1/warm-fixture-check.json'
        self.assertTrue(f.exists(),'warm unchanged-input check has not run')
        info=json.loads(f.read_text()); self.assertEqual(info['changed_outputs'],[]); self.assertEqual(info['picture_calls'],0)

    def test_v2_26_non_C10_records(self):
        self.api(); g=self.card('results/g6_scale_n_result.json','records'); self.assertEqual(len(g['records']),100); self.assertEqual(len(g['rungs']),3)
        for row in g['records']:
            self.assertTrue({'entity','field','expressed_at_apply','retained_at_end'} <= set(row))
        for arm in ['NOVEL_single','PRIOR_single','PRIOR_multi_same','PRIOR_multi_para']:
            c=self.card('results/r5_paraphrase_robustness.json','arms.'+arm)
            self.assertIsNotNone(c['headline']['rate']['value']); self.assertEqual(len(c['per_fact']),16)
            self.assertTrue(all('generated_text' in f for f in c['per_fact']))

    def test_v2_27_saved_picture_metadata(self):
        self.api(); from tools.labviz.render import picture_readable
        self.assertFalse(picture_readable({'width_px':561,'text_px':[6*110/72]},600))
        self.assertTrue(picture_readable({'width_px':561,'text_px':[9*110/72]},600))
        manifest=json.loads((ROOT/'results/labviz/images_manifest.json').read_text())
        self.assertTrue(manifest)
        for item in manifest.values(): self.assertTrue(picture_readable(item,600))

    def test_v2_28_D1_documentary_context(self):
        self.api(); rows=[c for c in self.reader().cards if re.match(r'results/d1_[^/]*\.json$',c['identity']['name'])]
        self.assertTrue(rows)
        named=0
        for c in rows:
            name=Path(c['identity']['name']).name
            if name.startswith('d1_concentration_sweep_result') or name=='d1_predictor_map_result.json':
                named+=1; self.assertEqual(c['context']['corpus']['node_id'],'corpus:22'); self.assertEqual(c['context']['decision']['node_id'],'dec:D-D1-1')
                self.assertIsNone(c['context']['experiment']['value'])
            else: self.assertIsNone(c['context']['experiment']['value'])
        self.assertGreaterEqual(named,5)

    def test_v2_29_selection_carried_and_restored(self):
        self.api(); f=ROOT/'results/labviz/review/v2-build/browser-tests.json'; self.assertTrue(f.exists(),'selection browser test has not run')
        self.assertTrue(json.loads(f.read_text())['selection_carries'])

    def test_v2_30_animation_is_labelled_diagram(self):
        self.api(); f=ROOT/'results/labviz/review/v2-build/browser-tests.json'; self.assertTrue(f.exists(),'animation browser test has not run')
        self.assertTrue(json.loads(f.read_text())['diagram_label_persists'])

    def test_fix_31_D1_graph_framing_preserves_its_document_sources(self):
        node=next(n for n in self.reader().program.graph['nodes'] if n['node_id']=='corpus:22')
        self.assertIn('FIXED total edit count N',node['question']['value'])
        self.assertEqual(node['description'],node['question'])
        self.assertEqual(node['measure']['value'],'held-out same-relation read corruption vs concentration')
        self.assertEqual(node['short_label']['value'],'D1 CAPACITY LAW')
        for key in ('question','short_label'):
            leaf=node[key]; citation=leaf['src']
            line=(ROOT/citation['file']).read_text().splitlines()[citation['line']-1]
            self.assertIn(citation['quote'],line)
            self.assertIn(leaf['value'],citation['quote'])
        self.assertEqual(node['framing_status']['value'],'DRAFT')

    def test_fix_32_C10_science_status_is_separate_from_draft_framing(self):
        program=self.reader().program
        node=next(n for n in program.graph['nodes'] if n['node_id']=='cond:C10')
        condition=next(n for n in program.conditions if n['id']=='C10')
        self.assertEqual(node['status']['value'],condition['status'])
        self.assertNotEqual(node['status']['value'],'DRAFT')
        self.assertEqual(node['status']['src']['file'],'docs/F1_DETERMINATION.md')
        self.assertEqual(node['status']['src'],node['citations']['status'])
        self.assertEqual(node['framing_status']['value'],'DRAFT')

    def test_fix_33_G6_headlines_keep_rung_specific_truth_percentages(self):
        original=json.loads((ROOT/'results/g6_scale_n_result.json').read_text())
        for i,rung in enumerate(original['rungs']):
            card=self.card('results/g6_scale_n_result.json',f'rungs[{i}]')
            result=card['headline']['heldout_top1']
            self.assertEqual(result['value'],rung['heldout_top1']['edited_rel']['top1_correct_vs_truth'])
            self.assertEqual(result['unit'],'percent')
            self.assertEqual(card['headline']['rung_n']['value'],rung['n'])
            self.assertIsNone(card['headline']['hits']['value'])
            self.assertIsNone(card['headline']['out_of']['value'])
            self.assertNotIn('program_goal',card['headline'])

    def test_fix_34_bootstrap_defers_the_classic_index_and_preserves_evaluations(self):
        site=ROOT/'results/labviz/site'
        script=(site/'data.js').read_text()
        self.assertTrue(script.startswith('window.LAB='))
        payload=json.JSONDecoder().raw_decode(script[len('window.LAB='):])[0]
        self.assertEqual(payload['index'],[])
        self.assertEqual(payload['index_src'],'cards/index.js')
        self.assertTrue((site/payload['index_src']).is_file())
        rows=json.loads((site/'cards/index.json').read_text())
        for identity in ('exp:G6.1','exp:C10V-layerpick','corpus:22'):
            expected=sum(row['line']==identity or 'exp:'+str(row['experiment'])==identity for row in rows)
            self.assertEqual(payload['index_counts'][identity],expected)
        original=json.loads((ROOT/'docs/c10_evaluations.json').read_text())['entries']
        for recorded,display in zip(original,payload['evaluations']):
            for key in recorded:
                self.assertEqual(display[key],recorded[key])
        self.assertEqual(len(payload['evaluations']),len(original))
        self.assertIn('rules_out',payload['evaluations'][0]['template_fields'])

    def test_fix_35_log_snapshot_requires_the_exact_recorded_hash(self):
        prior=b'old line\nSTAGE_EXIT=2\n'
        digest=hashlib.sha256(prior).hexdigest()
        self.assertEqual(recorded_log_prefix(prior+b'new live line\n',digest),prior)
        with self.assertRaisesRegex(ValueError,'No log prefix matches'):
            recorded_log_prefix(b'changed line\nSTAGE_EXIT=2\nnew live line\n',digest)

    def test_fix_round2_D1_trajectory_titles_preserve_the_cited_question(self):
        reader=self.api().Reader(ROOT)
        source='results/d1_concentration_sweep_result.json'
        runs=importlib.import_module('tools.labviz.build').parse_record(reader.read(source),source,ROOT)
        original=json.dumps(reader.read(source),sort_keys=True)
        for branch in ('DILUTED','CONCENTRATED'):
            card=reader.make(next(row for row in runs if row['field']==branch+'.trajectory'))
            title=card['identity'].get('display_title',{})
            self.assertEqual(title.get('value'),f'D1 · {branch} trajectory')
            self.assertEqual(title['src'],{'file':'tools/labviz/contexts.json','path':f'.corpus_eras["22"].display_titles["{branch}"]'})
            self.assertIn('FIXED total edit count N',card['context']['question']['value'])
            self.assertEqual(card['context']['question']['src']['file'],'tools/labviz/contexts.json')
            self.assertEqual(card['context']['question']['src']['path'],'.corpus_eras["22"].question')
            table=json.loads((ROOT/'tools/labviz/contexts.json').read_text())['corpus_eras']['22']
            self.assertEqual(card['context']['question']['value'],table['question'])
            self.assertEqual(table['citations']['question']['file'],'CORPUS/22_D1_CAPACITY_LAW.md')
            self.assertIn('FIXED total edit count N',table['citations']['question']['quote'])
            reader.finish(card)
            self.assertTrue(self.api().validate_card(card,ROOT,reader.scales))
            changed=copy.deepcopy(card);changed['identity']['display_title']['value']='D1 · wrong trajectory'
            with self.assertRaisesRegex(ValueError,'leaf differs from source'):
                self.api().validate_card(changed,ROOT,reader.scales)
        self.assertEqual(json.dumps(reader.read(source),sort_keys=True),original)

    def test_fix_round2_index_retains_recipe_and_arm_for_human_run_rows(self):
        rows=json.loads((ROOT/'results/labviz/site/cards/index.json').read_text())
        row=next(row for row in rows if row['source']=='results/c10v_layerpick/pass1.json' and row['field']=='recipes.B.arms.A7_coined_coined')
        self.assertEqual(row.get('recipe'),'B')
        self.assertEqual(row.get('arm'),'A7_coined_coined')

    def test_fix_round2_D1_index_uses_the_short_trajectory_title(self):
        rows=json.loads((ROOT/'results/labviz/site/cards/index.json').read_text())
        for branch in ('DILUTED','CONCENTRATED'):
            row=next(row for row in rows if row['source']=='results/d1_concentration_sweep_result.json' and row['field']==branch+'.trajectory')
            self.assertEqual(row['title'],f'D1 · {branch} trajectory')

    def test_fix_round2_index_recipe_and_arm_are_text_or_missing(self):
        rows=json.loads((ROOT/'results/labviz/site/cards/index.json').read_text())
        for row in rows:
            for key in ('recipe','arm'):
                self.assertTrue(row.get(key) is None or isinstance(row[key],str),(row['card_id'],key,row.get(key)))
        zero=next(row for row in rows if row['source']=='results/d20_subbatch_sweep_result_ord2.json' and row['field'].startswith('arms[0].'))
        self.assertEqual(zero['arm'],'0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
