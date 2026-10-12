"""Read every output and verify brief coverage, projection and scheduling invariants."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
A = ROOT / 'results/context_audit_20261012'


def verify_restoration(data, here=HERE):
    spec = json.loads((here / 'restoration_spec.json').read_text())
    baseline_path = ROOT / data['restoration_baseline']['path']
    assert hashlib.sha256(baseline_path.read_bytes()).hexdigest() == spec['baseline_sha256']
    baseline = json.loads(baseline_path.read_text())
    old = {u['id']:u for u in baseline['units']}
    units = {u['id']:u for u in data['units']}
    assert len(units) == len(data['units'])
    assert data['restoration_rows'] == spec['rows'], 'coverage differs from frozen restoration spec'
    assert data['restoration_owner_addenda'] == spec['owner_addenda']
    assert data['restoration_sources'] == spec['source_hashes']
    for source, digest in spec['source_hashes'].items():
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest() == digest, ('authority drift',source)
    for ident, original in old.items():
        assert ident in units
        expected = dict(original)
        change = spec['patches'].get(ident, {})
        expected['depends_on'] = list(dict.fromkeys(original['depends_on'] + change.get('depends_on_add', [])))
        assert units[ident] == expected, ('original unit changed outside permitted dependencies',ident)
    assert set(units)-set(old) == {u['id'] for u in spec['units']}
    for before, after in zip(baseline['lanes'], data['lanes']):
        assert before['id']==after['id']
        extra = [u for u in spec['units'] if u.get('append_to_lane')==before['id']]
        expected = dict(before)
        expected['units'] = before['units'] + [u['id'] for u in extra]
        expected['total_minutes'] = before['total_minutes'] + sum(u['minutes'] for u in extra)
        expected['allowlist'] = sorted(set(before['allowlist'] + [p for u in extra for p in u['files']]))
        assert after == expected, ('original lane changed outside append contract',before['id'])
    found = {}
    for item in data['restoration_rows']:
        file, number = item['source'].rsplit(':',1)
        assert 1 <= int(number) <= len((ROOT/file).read_text().splitlines())
        found.setdefault(file,set()).add(int(number))
        assert item['reader'].strip()
        kind = item['disposition'].split()[0]
        assert kind in ('COVERED','NEW','MAESTRO-ONLY','OPERATOR')
        if kind in ('COVERED','NEW'):
            assert item['unit'] in units
            if kind=='COVERED':
                assert item['unit'] in old
                assert isinstance(item['check'],int) and 1 <= item['check'] <= len(old[item['unit']]['checks'])
            else:
                assert item['unit'] not in old
        else:
            assert len(item['disposition'].split()) > 1
    # Derive source coverage from the actual documents, not the spec's counts.
    required = set()
    section = 0
    for number,line in enumerate((A/'PRESERVATION.md').read_text().splitlines(),1):
        if line.startswith('## '):
            section = int(line.split()[1].rstrip('.'))
        if not line.startswith('| '):
            continue
        first = line.split('|')[1].strip()
        if (section==2 and first.startswith('10-')) or (section==3 and first.startswith(('S1/','S3/'))) or (section==4 and first not in ('Worktree (suffix relative to M unless absolute)',)):
            required.add(number)
    assert len(required)==128
    assert required <= found.get('results/context_audit_20261012/PRESERVATION.md',set())
    inside = False
    hypothesis = set()
    for number,line in enumerate((A/'operator_hypothesis_worktree_vs_main.md').read_text().splitlines(),1):
        if line.startswith('## Restoration units'):
            inside=True
        elif inside and line.startswith('## '):
            inside=False
        if inside and line.startswith('- '):
            hypothesis.add(number)
    assert len(hypothesis)==4
    assert hypothesis <= found.get('results/context_audit_20261012/operator_hypothesis_worktree_vs_main.md',set())
    # A second owner cannot quietly take an index or generated destination.
    shared = {'memory_mirror/MEMORY.md','SESSION_BOOTSTRAP.md','SESSION_CHECKPOINT.md',
              'EXPERIMENT_RUNBOOK.md','README.md','PROGRESS.md'}
    for u in data['units']:
        if u['id'] not in old:
            assert not (set(u['source_files']) & shared), ('second generated/index owner',u['id'])
            assert all(not p.endswith('/memory/MEMORY.md') for p in u['source_files'])
    for red, green in [('R-ROOT-RED','R-ROOT-GREEN'),('R-HOOK-RED','R-HOOK-GREEN')]:
        assert units[red]['expected_red'] and red in units[green]['depends_on']
    for ident in ('DG6','DG7','DG-INDEX-PINS'):
        assert 'R-HOOK-GREEN' in units[ident]['depends_on']
    for item in spec['supplemental_exports']:
        unit=units[item['id']]
        assert item['staging_path'] in unit['files']
        assert item['id'] in units['I-CACHE']['depends_on']
        assert unit['wave'] < units['I-CACHE']['wave']
    for ident,duties in spec['owner_addenda'].items():
        brief=(here/'briefs'/(units[ident]['lane']+'.md')).read_text()
        assert all(duty in brief for duty in duties), ('missing shared owner duty',ident)
    mapping=(here/'restoration_map.md').read_text()
    for item in spec['rows']:
        assert item['source'] in mapping and item['reader'].replace('|','&#124;') in mapping
    for ident,change in spec['patches'].items():
        assert ident in mapping and all(dep in mapping for dep in change['depends_on_add'])
    for item in spec['worktree_question']:
        assert item['path'] in mapping and item['status'] in mapping
    assert len(spec['worktree_question'])==7
    assert all(value in mapping for value in spec['final_steps'].values())
    return {'restoration_table_rows':len(required),'hypothesis_bullets':len(hypothesis),
            'restoration_map_rows':len(spec['rows']),'new_units':len(spec['units']),
            'supplemental_exports':len(spec['supplemental_exports']),'baseline_units_preserved':len(old)}


def verify():
    # Every byte is reread; inventories retain hashes so the reviewed bundle is explicit.
    inventory = {}
    for path in sorted(HERE.rglob('*')):
        if path.is_file():
            raw = path.read_bytes()
            raw.decode('utf-8')
            inventory[path.relative_to(HERE).as_posix()] = {
                'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    data = json.loads((HERE / 'lanes.json').read_text())
    units = {u['id']: u for u in data['units']}
    assert len(units) == len(data['units'])
    rows = []
    for line in (A / 'SYNTHESIS.md').read_text().splitlines():
        if line.startswith('| '):
            ident = line.split('|')[1].strip()
            if re.fullmatch(r'(?:C\d+|N\d+|P\d+|D-U\d+[abc]?|I-[A-Z]+[ab]?|E\(n,s\))', ident):
                rows.append(ident)
    assert len(rows) == 119 and set(rows) <= set(units)
    assignment = {}
    for lane in data['lanes']:
        assert lane['requires_dispatch'] is True
        assert lane['kind'] in ('repo', 'host')
        assert sum(units[u]['minutes'] for u in lane['units']) == lane['total_minutes'] <= 36
        expected = {lane['handoff_file']}
        brief = (HERE / 'briefs' / (lane['id'] + '.md')).read_text()
        assert data['content_rules'] in brief and data['planner_finish_rule'] in brief
        for token in ('READY', 'BLOCKED <reason>', 'HANDOFF'):
            assert lane['id'] + ' ' + token in brief
        for ident in lane['units']:
            assert ident not in assignment
            assignment[ident] = lane
            unit = units[ident]
            assert unit['lane'] == lane['id'] and unit['wave'] == lane['wave']
            assert 0 < unit['minutes'] <= 8 and len(unit['checks']) >= 3
            assert unit['finding_ids'] and unit['source'] and unit['deliverable']
            expected.update(unit['files'])
            for path in unit['files']:
                assert not path.startswith('/') and '..' not in Path(path).parts
                assert not any(character in path for character in '*?[')
                assert path in brief
            for check in unit['checks']:
                assert check.replace('<LANE>', lane['id']) in brief
            for row in unit['evidence']:
                source = ROOT / row['audit']
                actual = source.read_text().splitlines()[row['audit_line'] - 1]
                assert row['subject'] in actual, (ident, row['audit'], row['audit_line'])
        assert set(lane['allowlist']) == expected
    assert set(assignment) == set(units)
    for unit in units.values():
        for dep in unit['depends_on']:
            prior = assignment[dep]
            current = assignment[unit['id']]
            assert prior['wave'] < current['wave'] or (
                prior['id'] == current['id'] and current['units'].index(dep) < current['units'].index(unit['id']))
    for left in data['lanes']:
        for right in data['lanes']:
            if left['id'] < right['id'] and left['wave'] == right['wave']:
                assert not (set(left['allowlist']) & set(right['allowlist'])), (left['id'], right['id'])
    notes = [u for u in units.values() if any(path.startswith('memory_mirror/') and Path(path).name != 'MEMORY.md'
             for path in u['source_files'])]
    assert all(u['wave'] < units['I-GIT']['wave'] for u in notes)
    candidates = json.loads((HERE / 'export_candidates.json').read_text())['exports']
    assert len(candidates) == 196
    assert len({e['host_path'] for e in candidates}) == 196
    for item in candidates:
        owner = units[item['id']]
        assert item['staging_path'] in owner['files']
        assert owner['wave'] < units['I-CACHE']['wave']
    assert len((HERE / 'PLAN.md').read_text().splitlines()) <= 120
    assert 'finalize-session' in (HERE / 'host_apply.md').read_text()
    assert len(list((HERE / 'briefs').glob('*.md'))) == len(data['lanes'])
    markdown = (HERE / 'LANES.md').read_text()
    for unit in units.values():
        assert unit['id'] + ' — ' + unit['deliverable'] in markdown
        assert all(check in markdown for check in unit['checks'])
        assert all(path in markdown for path in unit['files'])
    restoration = verify_restoration(data)
    return dict(restoration, **{'synthesis_rows': len(rows), 'units': len(units), 'lanes': len(data['lanes']),
            'waves': len({l['wave'] for l in data['lanes']}), 'exports': len(candidates),
            'all_outputs_reread': len(inventory), 'inventory': inventory})


if __name__ == '__main__':
    result = verify()
    (HERE / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'inventory'}, sort_keys=True))
