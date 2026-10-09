import hashlib, json, sys
from pathlib import Path
root = Path.cwd()
sys.path.insert(0,str(root))
from tools import mathlab_events
from tools.labviz import cards
proof = Path(__file__).resolve().parent
site = root/'results/labviz/site'
evidence = site/'evidence'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
index = json.loads((site/'cards/index.json').read_text())
mathrows = [r for r in index if r['source'].startswith(('results/mathlab/','results/mathlab_staging/'))]
assert all(cards.mathlab_source(r['source']) and r['mathlab']['tier']=='MATH-PROXY' for r in mathrows)
assert 'RECONSTRUCTED' not in cards.label_table()
assert 'RECONSTRUCTED' not in cards.recorded_labels(root)
summary = {'total_cards':len(index),'mathlab_cards':len(mathrows),'runs':[],'checks':[]}
for row in mathrows:
    card = json.loads((site/'cards'/(row['card_id']+'.json')).read_text())
    assert card['evidence_status']=='MATH-PROXY'
    assert card['label']['value']=='math estimate, not evidence'
    assert cards.validate_card(card,evidence)
    state = card['mathlab']['state']['value']
    assert row['mathlab']['status']==state['status']
    script = (site/'cards'/(row['chunk']+'.js')).read_text()
    chunk = json.loads(script.split(']=',1)[1].removesuffix(';\n'))
    assert next(c for c in chunk if c['card_id']==card['card_id'])==card
    mirrored = cards.source_data(evidence,row['source'])
    mirrored_events, mirrored_errors = mirrored['events'], mirrored['errors']
    assert state==json.loads(cards.encoded(mathlab_events.fold(mirrored_events)))
    assert mirrored_errors==card['mathlab']['errors']['value']
    source_hash = next(s['sha256'] for s in card['sources'] if s['file']==row['source'])
    assert source_hash==sha(evidence/row['source'])
    live_events, live_errors = mathlab_events.read_events(root/row['source'])
    live_state = json.loads(cards.encoded(mathlab_events.fold(live_events)))
    item = {'run_id':state['run_id'],'card_id':card['card_id'],'status':state['status'],
            'outcome':state['outcome'],'purpose':state['purpose'],'steps':state['steps'],
            'source':row['source'],'snapshot_sha256':source_hash,'events':len(mirrored_events),
            'parse_errors':mirrored_errors,'current_live_status':live_state['status'],
            'current_live_events':len(live_events),'current_live_sha256':sha(root/row['source'])}
    if state['run_id']=='harvest_20261009T184932Z_95961':
        assert state==live_state and not live_errors
        assert state['status']=='finished' and state['outcome']=='PASS'
        assert source_hash==sha(root/row['source'])
        norm_gates = {g['gate_id']:g for g in state['gates'] if g['gate_id'].startswith('mint-norm-')}
        required = {'mint-norm-mint1_s'+str(i) for i in range(3)}
        assert set(norm_gates)==required
        assert all(g['passed'] is False and state['gate_outcomes'][name]=='FAIL' for name,g in norm_gates.items())
        assert all(g['observed']['passed'] is False for g in norm_gates.values())
        assert all(g['bar']=='relative norm difference <= 1e-3; not tensor identity' for g in norm_gates.values())
        assert len(card['mathlab']['findings'])==1
        finding = card['mathlab']['findings'][0]
        assert finding['event']['value']['tier']=='MATH-PROXY'
        assert finding['name']=='logs/pending_findings/10_mathlab_harvest_20261009T192601.184026Z.md'
        assert [line['value'] for line in finding['document']]==(root/finding['name']).read_text().splitlines()
        assert (evidence/finding['name']).read_bytes()==(root/finding['name']).read_bytes()
        item.update(norm_outcomes={n:state['gate_outcomes'][n] for n in sorted(required)},
                    derived_eligible_mint_arms=0,
                    norm_threshold=next(iter(norm_gates.values()))['bar'],
                    finding=finding['name'],finding_sha256=sha(root/finding['name']))
    summary['runs'].append(item)
assert any(r['run_id']=='harvest_20261009T184932Z_95961' for r in summary['runs'])
assert any(r['run_id']=='m2_20261009T192821Z_82233' for r in summary['runs'])
# No obsolete generic MathLab publication or uncited sidecar remains served.
for path in (site/'cards').glob('run-*.json'):
    c=json.loads(path.read_text())
    name=c.get('identity',{}).get('name','')
    if name.startswith(('results/mathlab/','results/mathlab_staging/')):
        assert cards.mathlab_source(name) and 'mathlab' in c, str(path)
for path in (evidence/'results/mathlab').rglob('*'):
    assert not path.is_file(), str(path)
for path in (evidence/'results/mathlab_staging').rglob('*'):
    if path.is_file(): assert cards.mathlab_source(path.relative_to(evidence).as_posix()), str(path)
summary['checks']=['all MathLab index rows are canonical MATH-PROXY streams',
                   'card/index/chunk/mirrored-reader-fold agree for every MathLab run',
                   'harvest terminal PASS and all three norm failures retain exact thresholds',
                   'zero replay-eligible mint arms derived from required failed checks',
                   'staged finding and shared reader/fold module snapshots hash correctly',
                   'no RECONSTRUCTED verdict label or generic MathLab publication remains']
(proof/'live-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
