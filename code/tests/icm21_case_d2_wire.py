"""ReaderControls D2 wire parser case."""
import copy
import json

from icm21_fixtures import D2_POSITIVE, HEADER, digest, put, sealed


class D2WireParserCase:
    def test_d2_wire_parser(self):
        self.require_file('code/state/icm21_check.py', 'D2-only MapBinding parser')
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        examples['examples'] = [x for x in examples['examples'] if x['type'] == 'LabvizMoves']
        self.assertEqual(len(examples['examples']), 2)
        positive = copy.deepcopy(examples['examples'][0])
        positive['value'] = json.loads(D2_POSITIVE['map'])
        positive['expected'] = 'PASS'
        examples['examples'] = [positive]
        for name, data in D2_POSITIVE['inputs'].items():
            put(self.scratch, name, data)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        for spelling in ('/foreign/path-map.tsv', '_index/wrong.tsv', '../path-map.tsv'):
            candidate = copy.deepcopy(examples)
            candidate['examples'][0]['value']['derived_from']['sealed']['path'] = spelling
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            original = (self.scratch / name).read_bytes()
            (self.scratch / name).write_bytes(original + b'changed')
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            (self.scratch / name).write_bytes(original)
        for change in (lambda v: v.update(extra=True),
                       lambda v: v.update(about='wrong identity'),
                       lambda v: v.update(moves=[]),
                       lambda v: v['derived_from']['sealed'].update(extra=True),
                       lambda v: v['derived_from']['sealed'].update(sha256='short')):
            candidate = copy.deepcopy(examples)
            change(candidate['examples'][0]['value'])
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            source = self.scratch / name
            parked = source.with_name(source.name + '.parked')
            source.rename(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.symlink_to(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.unlink()
            parked.rename(source)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        # Only LabvizMoves changes: ordinary Binding must remain absolute.
        ordinary = copy.deepcopy(examples)
        ordinary['examples'][0].update(type='Binding', value={'path': '_index/path-map.tsv',
                                                             'sha256': digest(HEADER)})
        self.assertEqual(self.wire(self.scratch, ordinary).returncode, 1)
