#!/usr/bin/python3
"""Static R2G schema/freeze coverage check; no host or product execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
FREEZE = HERE / 'shared_disk_clearance_freeze_v2.md'
SCHEMAS = HERE / 'shared_disk_clearance_schemas_v1.json'
DRAFT = 'https://json-schema.org/draft/2020-12/schema'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          ValueError('nonfinite JSON number: ' + value)))


def section(text, number):
    match = re.search(r'^## ' + str(number) + r'\. .*\n', text, re.M)
    require(match is not None, 'missing section ' + str(number))
    end = re.search(r'^## ', text[match.end():], re.M)
    return text[match.end():match.end() + end.start()] if end else text[match.end():]


def inventory(text):
    """Read the formal §4 inventory and mapping table, not narrative mentions."""
    documented = {}
    mappings = {}
    entrypoint_kinds = set()
    for part in (section(text, 2), section(text, 4)):
        for line in part.splitlines():
            if not line.startswith('| '):
                continue
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) >= 3:
                literal_list = re.search(r'\b[KA] exactly ([A-Z_, ]+);', cells[2])
                if literal_list:
                    entrypoint_kinds.update(re.findall(r'[A-Z][A-Z_]+',
                                                       literal_list.group(1)))
            if cells[0] in ('type', 'record', 'profile'):
                names = re.findall(r'`([A-Za-z][A-Za-z0-9_]*)`', cells[1])
                require(bool(names), 'empty schema inventory row: ' + line)
                for name in names:
                    require(name not in documented, 'duplicate schema name: ' + name)
                    documented[name] = cells[0]
            elif cells[0] == 'request':
                require(len(cells) == 7, 'malformed request mapping row: ' + line)
                values = [re.fullmatch(r'`([A-Za-z][A-Za-z0-9_]*)`', cell)
                          for cell in cells[1:5]]
                require(all(values), 'mapping names must be single exact tokens')
                kind, request, success, refusal = [match.group(1) for match in values]
                require(kind not in mappings, 'duplicate request kind: ' + kind)
                require(cells[5] in ('internal', 'wire'), 'unknown request channel')
                kinds = re.search(r'; ([A-Z_]+)/([A-Z_]+);', cells[6])
                require(kinds is not None, 'missing response-kind pair for ' + kind)
                mappings[kind] = {'request': request, 'success': success,
                                  'refusal': refusal, 'internal': cells[5] == 'internal',
                                  'success_kind': kinds.group(1),
                                  'refusal_kind': kinds.group(2)}
                for name, category in ((request, 'request'), (success, 'response'),
                                       (refusal, 'response')):
                    require(name not in documented, 'duplicate schema name: ' + name)
                    documented[name] = category
    require(entrypoint_kinds <= set(mappings),
            'entrypoint request kind has no schema: ' +
            str(sorted(entrypoint_kinds - set(mappings))))
    return documented, mappings


def inspect_schema(node, definitions, location='$'):
    require(isinstance(node, dict), 'boolean/untyped schema at ' + location)
    if '$ref' in node:
        target = node['$ref']
        require(target.startswith('#/$defs/'), 'external schema reference: ' + target)
        require(target[8:] in definitions, 'unresolved schema reference: ' + target)
    require(node.get('additionalProperties') is not True,
            'permissive object at ' + location)
    if node.get('type') == 'object':
        require(node.get('additionalProperties') is False,
                'object must be closed at ' + location)
        require(set(node.get('required', [])) == set(node.get('properties', {})),
                'all exact object fields must be required at ' + location)
    for name, prop in node.get('properties', {}).items():
        require(isinstance(prop, dict), 'non-schema field at ' + location + '.' + name)
        if node.get('type') == 'object':
            require(any(key in prop for key in
                        ('type', '$ref', 'oneOf', 'anyOf', 'const', 'enum')),
                    'untyped field at ' + location + '.' + name)
        inspect_schema(prop, definitions, location + '.' + name)
    if 'items' in node:
        inspect_schema(node['items'], definitions, location + '[]')
    for keyword in ('oneOf', 'anyOf', 'allOf'):
        for index, branch in enumerate(node.get(keyword, [])):
            inspect_schema(branch, definitions, location + '/' + keyword + str(index))
    for keyword in ('if', 'then', 'else', 'not'):
        if keyword in node:
            inspect_schema(node[keyword], definitions, location + '/' + keyword)


def hashes(text, schemas):
    result = {'schemas': schemas.read_bytes()}
    data = text.encode('utf-8')
    start = data.index(b'## 2. ')
    result['interface'] = data[start:data.index(b'## 5. ')]
    result['runtime'] = data[start:data.index(b'## 8. ')]
    pins = {}
    for name, payload in result.items():
        run = subprocess.run(['shasum', '-a', '256'], input=payload,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        require(run.returncode == 0, 'shasum failed: ' + run.stderr.decode('utf-8'))
        match = re.fullmatch(rb'([0-9a-f]{64})\s+-\n', run.stdout)
        require(match is not None, 'unexpected shasum output')
        pins[name] = match.group(1).decode('ascii')
        require(pins[name] == hashlib.sha256(payload).hexdigest(),
                'shasum/hashlib disagreement')
    return pins


def check(freeze, schemas, check_pins=True):
    text = freeze.read_text(encoding='utf-8')
    require(len(text.splitlines()) <= 340, 'freeze exceeds 340 lines')
    require(re.findall(r'^## ([1-9])\.', text, re.M) == list('123456789'),
            'freeze must have nine ordered numbered sections')
    bundle = read_json(schemas)
    source_pins = {
        'astra_r2f_verdict.md': '702d0185267f46006a03ff50c4e228a3ef5b0a8f0159b422ae91cec04e267dc6',
        'shared_disk_clearance_freeze_v1.md': '5e044b74f5cdbf3f84331bbeefdb674bd226c1993f03cb611f542783ce703fbf',
        'shared_disk_clearance_contract_v1_1.md': '25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1',
        'integration_r5_completion_table.md': '8f43668d555d02e553e5513ecb1ba3428dd31b1631a0d7d393a7a4012ff4fd81',
    }
    for name, digest in source_pins.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest,
                'source input changed: ' + name)
    gate = HERE.parent.parent / 'tools' / 'c10w_p2_gate.py'
    require(hashlib.sha256(gate.read_bytes()).hexdigest() ==
            'fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26',
            'unchanged gate pin mismatch')
    require(bundle.get('$schema') == DRAFT, 'wrong JSON Schema draft')
    definitions = bundle.get('$defs', {})
    catalog = bundle.get('x-catalog', {})
    named, doc_mappings = inventory(text)
    require(set(definitions) == set(catalog),
            'missing schema or catalog entry: ' + str(sorted(set(definitions) ^ set(catalog))))
    require(set(named) == set(definitions),
            'freeze/schema coverage mismatch: ' + str(sorted(set(named) ^ set(definitions))))
    require(named == catalog, 'schema categories disagree with freeze tables')
    root_refs = [node.get('$ref') for node in bundle.get('oneOf', [])]
    expected_roots = {'#/$defs/' + name for name, category in catalog.items()
                      if category != 'type'}
    require(len(root_refs) == len(set(root_refs)) and set(root_refs) == expected_roots,
            'root union omits/repeats a record/profile/request/response schema')
    mapping = bundle.get('x-response-mapping', {})
    require(set(mapping) == set(doc_mappings), 'request-kind coverage mismatch')
    require(set(definitions['ResponseMapping']['properties']['request_kind']['enum']) ==
            set(mapping), 'request-kind discriminator enum disagrees with mapping')
    request_names = set()
    response_names = set()
    for kind, row in mapping.items():
        for key in ('request', 'success', 'refusal', 'internal',
                    'success_kind', 'refusal_kind'):
            require(key in row and row[key] == doc_mappings[kind][key],
                    'missing/mismatched ' + key + ' mapping for ' + kind)
        request_names.add(row['request'])
        request = definitions[row['request']]
        require(request['properties']['kind'].get('const') == kind,
                'request discriminator mismatch for ' + kind)
        for side in ('success', 'refusal'):
            name = row[side]
            require(name not in response_names, 'response schema reused: ' + name)
            response_names.add(name)
            props = definitions[name]['properties']
            require(props['request_kind'].get('const') == kind,
                    'response request-kind mismatch for ' + kind)
            require(props['kind'].get('const') == row.get(side + '_kind'),
                    'response kind missing/mismatched for ' + kind)
            if side == 'refusal':
                require(row['refusal_kind'] in ('REFUSED', 'HALTED_UNCLEARED'),
                        'invalid refusal kind for ' + kind)
                require(props['grant'] == {'type': 'null'} and
                        props['clearance'] == {'type': 'null'},
                        'refusal includes permission for ' + kind)
    require(request_names == {n for n, c in catalog.items() if c == 'request'},
            'orphan/missing request schema')
    require(response_names == {n for n, c in catalog.items() if c == 'response'},
            'orphan/missing response schema')
    require(definitions['U64']['maximum'] == 18446744073709551615,
            'U64 maximum lost precision')
    for name, value in definitions.items():
        require('C:' in value.get('description', ''), 'schema lacks C clause: ' + name)
        inspect_schema(value, definitions, name)
    require(all('C:' in line or 'C clause' in line
                for line in text.splitlines() if 'PROPOSED' in line),
            'PROPOSED selection lacks C clause on its line')
    require('integration_plan.md' not in text, 'obsolete integration citation remains')
    pins = hashes(text, schemas)
    if check_pins:
        for name, digest in pins.items():
            require(re.search(r'\| ' + name + r' pin \| `' + digest + r'`', text),
                    'missing/stale ' + name + ' pin')
    return len(definitions), len(mapping), len(text.splitlines()), pins


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', type=Path, default=FREEZE)
    parser.add_argument('--schemas', type=Path, default=SCHEMAS)
    parser.add_argument('--print-hashes', action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    if args.print_hashes:
        for name, digest in hashes(args.freeze.read_text(encoding='utf-8'), args.schemas).items():
            print(name + ' ' + digest)
        return 0
    definitions, requests, lines, _ = check(args.freeze, args.schemas)
    print('GREEN: %d schemas, %d request success/refusal mappings, %d freeze lines' %
          (definitions, requests, lines))
    if args.negative_control:
        tmp_root = os.environ.get('TMPDIR')
        require(bool(tmp_root) and Path(tmp_root).is_dir(), '$TMPDIR must exist')
        damaged = read_json(args.schemas)
        removed = 'GrantRecord'
        del damaged['$defs'][removed]
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json',
                                         prefix='r2g-missing-schema-', dir=tmp_root,
                                         delete=False) as copy:
            json.dump(damaged, copy, indent=2)
            copy.write('\n')
            path = copy.name
        run = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()),
                              '--freeze', str(args.freeze), '--schemas', path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        require(run.returncode == 1 and 'missing schema' in run.stderr and
                removed in run.stderr, 'missing-schema negative control did not fail as expected')
        print('RED: removed %s under $TMPDIR; checker exit %d: %s' %
              (removed, run.returncode, run.stderr.strip()))
        print('Negative-copy path: ' + path)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
