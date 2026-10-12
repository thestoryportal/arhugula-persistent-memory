#!/usr/bin/env python3
"""Compare JSON meaning, independent of serialization; no version inference."""
import csv
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
WANTED = {'aggregate_verdict.json', 'stage_2_sweep_verdict.json',
          'reproducibility_manifest.json', 'llm-as-database/reproducibility_manifest.json'}


def flatten(value, pointer=''):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from flatten(child, pointer + '/' + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flatten(child, pointer + '/' + str(index))
    else:
        yield pointer, value


def main():
    with (OUT / 'candidates_refined.tsv').open() as f:
        candidates = {r['inventory_row']: r for r in csv.DictReader(f, delimiter='\t') if r['path'] in WANTED}
    with (OUT / 'program_json_diffs.jsonl').open('w') as output, (OUT / 'matches.tsv').open() as matches:
        for row in csv.DictReader(matches, delimiter='\t'):
            if row['inventory_row'] not in candidates:
                continue
            backup = Path('/Volumes/backups') / candidates[row['inventory_row']]['path']
            target = Path(row['repo_or_mirror_path'])
            if max(backup.stat().st_size, target.stat().st_size) > 200 * 1024:
                raise ValueError('Use bounded ranges for large JSON')
            a = json.loads(backup.read_text())
            b = json.loads(target.read_text())
            aa, bb = dict(flatten(a)), dict(flatten(b))
            changed = [{'key': k, 'backup': aa[k], 'counterpart': bb[k]} for k in sorted(aa.keys() & bb.keys()) if aa[k] != bb[k]]
            item = {'backup': str(backup), 'counterpart': str(target),
                    'backup_only_keys': sorted(aa.keys() - bb.keys()),
                    'counterpart_only_keys': sorted(bb.keys() - aa.keys()),
                    'changed_leaves': changed,
                    'equal_leaves': sum(aa[k] == bb[k] for k in aa.keys() & bb.keys()),
                    'parsed_objects_equal': a == b,
                    'backup_top_keys': list(a), 'counterpart_top_keys': list(b)}
            output.write(json.dumps(item) + '\n')
            print(backup.name, 'equal leaves', item['equal_leaves'], 'changed', len(changed), 'JSON equal', a == b)


if __name__ == '__main__':
    main()
