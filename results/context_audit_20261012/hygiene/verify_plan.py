"""Read every output and verify brief coverage, projection and scheduling invariants."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
A = ROOT / 'results/context_audit_20261012'


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
        assert sum(units[u]['minutes'] for u in lane['units']) == lane['total_minutes'] <= 40
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
    return {'synthesis_rows': len(rows), 'units': len(units), 'lanes': len(data['lanes']),
            'waves': len({l['wave'] for l in data['lanes']}), 'exports': len(candidates),
            'all_outputs_reread': len(inventory), 'inventory': inventory}


if __name__ == '__main__':
    result = verify()
    (HERE / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'inventory'}, sort_keys=True))
