#!/usr/bin/python3
"""Static R2W D15 correctness, recorded reachability and construction check; no host or product execution."""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import copy
import shlex


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / 'shared_disk_clearance_freeze_v10.md'
SCHEMAS = HERE / 'shared_disk_clearance_schemas_v9.json'
PROFILES = HERE / 'science_launch_profiles_v7.json'
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


def finite_float(token):
    value = float(token)
    require(math.isfinite(value), 'nonfinite JSON number: ' + token)
    return value


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object, parse_float=finite_float,
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
        require(node.get('additionalProperties') is False or
                'propertyNames' in node and isinstance(node.get('additionalProperties'), dict),
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
    if isinstance(node.get('additionalProperties'), dict):
        inspect_schema(node['additionalProperties'], definitions, location + '/additionalProperties')
    if 'items' in node:
        inspect_schema(node['items'], definitions, location + '[]')
    for keyword in ('oneOf', 'anyOf', 'allOf'):
        for index, branch in enumerate(node.get(keyword, [])):
            inspect_schema(branch, definitions, location + '/' + keyword + str(index))
    for keyword in ('if', 'then', 'else', 'not', 'propertyNames'):
        if keyword in node:
            inspect_schema(node[keyword], definitions, location + '/' + keyword)


def hashes(text, schemas):
    result = {'schemas': schemas.read_bytes(), 'inventory': (HERE / 'science_launch_inventory_v8.md').read_bytes()}
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
    require(len(text.splitlines()) <= 360, 'freeze exceeds 360 lines')
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
    schema_correctness(bundle)
    root_refs = [node.get('$ref') for node in bundle.get('oneOf', [])]
    expected_roots = {'#/$defs/' + name for name, category in catalog.items()
                      if category != 'type'}
    covered_roots = set(root_refs)
    pending_roots = list(root_refs)
    while pending_roots:
        ref = pending_roots.pop()
        require(isinstance(ref, str) and ref.startswith('#/$defs/') and
                ref[8:] in definitions, 'unresolved root schema reference')
        node = definitions[ref[8:]]
        # shared_disk_clearance_schemas_v3.json:1425-1437: FencingReceipt is a pure union of three named variants.
        if (set(node) <= {'description', 'oneOf'} and 'oneOf' in node and
                all(set(branch) == {'$ref'} for branch in node['oneOf'])):
            for branch in node['oneOf']:
                require(set(branch) == {'$ref'}, 'root alias must use exact references')
                child = branch['$ref']
                require(child not in covered_roots, 'root union repeats a variant')
                covered_roots.add(child)
                pending_roots.append(child)
    require(len(root_refs) == len(set(root_refs)) and covered_roots == expected_roots,
            'root union omits/repeats a record/profile/request/response schema')
    mapping = bundle.get('x-response-mapping', {})
    require(set(mapping) == set(doc_mappings), 'request-kind coverage mismatch')
    independent_mapping(text, bundle)
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
    required_r3(bundle)
    example_count = examples_valid(bundle)
    binding_count = invocation_coherence(bundle)
    mandatory_hash_completeness(text, bundle)
    reference_count, observation_count = coherent_examples(text, bundle)
    round8_checks(None, bundle, text)
    round9_checks(None, bundle, text)
    round10_checks(None, bundle, text)
    pins = hashes(text, schemas)
    if check_pins:
        for name, digest in pins.items():
            require(re.search(r'\| ' + name + r' pin \| `' + digest + r'`', text),
                    'missing/stale ' + name + ' pin')
    return len(definitions), len(mapping), example_count, reference_count, len(text.splitlines()), pins, binding_count, observation_count




JSON_TYPES = {'null', 'boolean', 'object', 'array', 'number', 'integer', 'string'}
ANNOTATIONS = {'$schema', '$id', 'description', 'x-catalog', 'x-response-mapping',
               'x-fencing-mapping', 'x-construction'}
VALIDATOR_KEYWORDS = ANNOTATIONS | {
    '$defs', '$ref', 'type', 'const', 'enum', 'oneOf', 'anyOf', 'allOf',
    'properties', 'required', 'additionalProperties', 'items', 'if', 'then',
    'else', 'not', 'pattern', 'minimum', 'maximum', 'minLength', 'maxLength',
    'minItems', 'maxItems', 'propertyNames', 'minProperties', 'maxProperties'}


def json_equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    return a == b


def schema_correctness(bundle):
    """Draft keyword shape checks, limited to the enumerated supported vocabulary."""
    seen = set()
    def walk(node, location):
        require(isinstance(node, dict), 'non-object schema at ' + location)
        seen.update(node)
        require(set(node) <= VALIDATOR_KEYWORDS,
                'unsupported schema keyword at ' + location + ': ' +
                str(sorted(set(node) - VALIDATOR_KEYWORDS)))
        for key, value in node.items():
            bad = 'malformed ' + key + ' at ' + location
            if key in ('$schema', '$id', '$ref', 'description', 'pattern'):
                require(isinstance(value, str), bad)
                if key == 'pattern':
                    try:
                        re.compile(value)
                    except re.error as error:
                        raise ValueError(bad + ': ' + str(error)) from error
            elif key == 'type':
                types = value if isinstance(value, list) else [value]
                require(bool(types) and all(isinstance(t, str) and t in JSON_TYPES
                                           for t in types) and len(types) == len(set(types)), bad)
            elif key == 'required':
                require(isinstance(value, list) and all(isinstance(x, str) for x in value)
                        and len(value) == len(set(value)), bad)
            elif key == 'enum':
                require(isinstance(value, list) and bool(value), bad)
                require(not any(json_equal(x, y) for i, x in enumerate(value)
                                for y in value[:i]), bad)
            elif key in ('minimum', 'maximum'):
                require(isinstance(value, (int, float)) and not isinstance(value, bool) and
                        (not isinstance(value, float) or math.isfinite(value)), bad)
            elif key in ('minLength', 'maxLength', 'minItems', 'maxItems', 'minProperties', 'maxProperties'):
                require(type(value) is int and value >= 0, bad)
            elif key in ('properties', '$defs'):
                require(isinstance(value, dict), bad)
                for name, child in value.items():
                    walk(child, name if key == '$defs' else location + '.' + name)
            elif key in ('oneOf', 'anyOf', 'allOf'):
                require(isinstance(value, list) and bool(value), bad)
                for i, child in enumerate(value):
                    walk(child, location + '/' + key + str(i))
            elif key in ('items', 'if', 'then', 'else', 'not', 'propertyNames'):
                walk(value, location + '/' + key)
            elif key == 'additionalProperties':
                require(isinstance(value, (bool, dict)), bad)
                if isinstance(value, dict):
                    walk(value, location + '/' + key)
            elif key.startswith('x-'):
                require(location == '$' and isinstance(value, dict), bad)
            # const accepts any JSON value; $id/$schema/description are annotations.
    for name, node in bundle['$defs'].items():
        require(isinstance(node, dict) and any(k in node for k in
                ('type', '$ref', 'const', 'enum', 'oneOf', 'anyOf', 'allOf')),
                'schema lacks assertion: ' + name)
    walk(bundle, '$')
    return seen


def ssh_request_kinds(text):
    """Independent §3 table parser; does not consult inventory() or §4."""
    kinds = set()
    for line in section(text, 3).splitlines():
        if not line.startswith('| '):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if cells[0].startswith('R2_'):
            require(len(cells) == 3 and re.fullmatch(r'R2_[A-Z_]+_V1', cells[0])
                    and re.fullmatch(r'[A-Z][A-Z_]+', cells[1]),
                    'malformed SSH request table row: ' + line)
            require(cells[1] not in kinds, 'duplicate SSH request kind: ' + cells[1])
            kinds.add(cells[1])
    require(bool(kinds), 'empty SSH request-kind table')
    return kinds


def independent_mapping(text, bundle):
    mapping = bundle['x-response-mapping']
    # MAESTRO's corrected C2: noninternal also includes local IPC (F4:64).
    for kind in sorted(ssh_request_kinds(text)):
        require(kind in mapping and mapping[kind].get('internal') is False,
                'SSH request kind missing/non-wire: ' + kind)
    transitions = bundle['x-construction']['transitions']
    require(set(transitions) == set(mapping), 'transition request-kind coverage mismatch')
    for kind, row in mapping.items():
        require(type(row['internal']) is bool, 'mapping internal flag must be boolean: ' + kind)
        for key in ('request', 'success', 'refusal'):
            name = row[key]
            category = 'request' if key == 'request' else 'response'
            require(name in bundle['$defs'] and bundle['x-catalog'].get(name) == category,
                    'missing request/response schema or catalog row: ' + kind + '/' + key)
            require({'$ref': '#/$defs/' + name} in bundle['oneOf'],
                    'request/response absent from root union: ' + kind + '/' + key)
        require(all(k in transitions[kind] for k in
                    ('before', 'after', 'receipt', 'request', 'success')),
                'incomplete transition entry: ' + kind)


def instance_valid(value, schema, definitions, depth=0):
    """Every recognized assertion is evaluated; unknown keywords cannot pass."""
    require(depth < 256, 'schema validation reference depth exceeded')
    require(not (set(schema) - VALIDATOR_KEYWORDS), 'unsupported validation keyword')
    if '$ref' in schema:
        ref = schema['$ref']
        if not instance_valid(value, definitions[ref[8:]], definitions, depth + 1):
            return False
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        matches = {'null': value is None, 'boolean': isinstance(value, bool),
                   'object': isinstance(value, dict), 'array': isinstance(value, list),
                   'string': isinstance(value, str),
                   'number': isinstance(value, (int, float)) and not isinstance(value, bool),
                   'integer': (isinstance(value, int) and not isinstance(value, bool)) or
                              (isinstance(value, float) and value.is_integer())}
        if not any(matches[t] for t in types):
            return False
    if 'const' in schema and not json_equal(value, schema['const']):
        return False
    if 'enum' in schema and not any(json_equal(value, x) for x in schema['enum']):
        return False
    for key in ('oneOf', 'anyOf', 'allOf'):
        if key in schema:
            valid = [instance_valid(value, branch, definitions, depth + 1)
                     for branch in schema[key]]
            if (key == 'oneOf' and sum(valid) != 1 or
                    key == 'anyOf' and not any(valid) or key == 'allOf' and not all(valid)):
                return False
    if 'not' in schema and instance_valid(value, schema['not'], definitions, depth + 1):
        return False
    if 'if' in schema:
        branch = 'then' if instance_valid(value, schema['if'], definitions, depth + 1) else 'else'
        if branch in schema and not instance_valid(value, schema[branch], definitions, depth + 1):
            return False
    if isinstance(value, dict):
        if not schema.get('minProperties', 0) <= len(value) <= schema.get('maxProperties', len(value)):
            return False
        if 'propertyNames' in schema and not all(instance_valid(k, schema['propertyNames'], definitions, depth + 1) for k in value):
            return False
        if not set(schema.get('required', [])) <= value.keys():
            return False
        properties = schema.get('properties', {})
        for name, child in value.items():
            if name in properties:
                if not instance_valid(child, properties[name], definitions, depth + 1):
                    return False
            elif 'additionalProperties' in schema:
                additional = schema['additionalProperties']
                if additional is False:
                    return False
                if isinstance(additional, dict) and not instance_valid(
                        child, additional, definitions, depth + 1):
                    return False
    if isinstance(value, list):
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value)):
            return False
        if 'items' in schema and not all(instance_valid(x, schema['items'], definitions, depth + 1)
                                        for x in value):
            return False
    if isinstance(value, str):
        if not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value)):
            return False
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum']:
            return False
        if 'maximum' in schema and value > schema['maximum']:
            return False
    # ANNOTATIONS and $defs are explicitly recognized metadata, not assertions.
    return True


def examples_valid(bundle):
    examples = bundle['x-construction']['examples']
    require(isinstance(examples, dict) and bool(examples), 'missing construction examples')
    for kind, row in bundle['x-response-mapping'].items():
        for side in ('success', 'refusal'):
            require(any(isinstance(e, dict) and e.get('schema_name') == row[side]
                        for e in examples.values()), 'missing ' + side + ' example: ' + kind)
    for name, example in examples.items():
        require(isinstance(example, dict) and set(example) == {'schema_name', 'instance'}
                and example['schema_name'] in bundle['$defs'], 'invalid example metadata: ' + name)
        require(instance_valid(example['instance'], bundle['$defs'][example['schema_name']],
                               bundle['$defs']), 'invalid example: ' + name)
    return len(examples)



def transition_rules(text):
    """Parse F4:219-231's exhaustive state-edge table independently of examples."""
    rules = {'science': set(), 'transfer': set()}
    active = False
    domain = 'science'
    for line in section(text, 4).splitlines():
        if line.startswith('| Legal transition set'):
            active = True
            continue
        if not active:
            continue
        if not line.startswith('|'):
            break
        cells = [x.strip() for x in line.strip('|').split('|')]
        if '→' not in cells[0]:
            continue
        if cells[0].startswith('transfer=null'):
            domain = 'transfer'
        for clause in cells[0].split(';'):
            tokens = [x.strip().replace('fresh ', '') for x in clause.split('→')]
            choices = []
            for token in tokens:
                if token in ('No science record', 'transfer=null', 'null'):
                    choices.append([None])
                else:
                    require(re.fullmatch(r'[A-Z_]+(?:/[A-Z_]+)*', token) is not None,
                            'unparsed legal transition token: ' + token)
                    choices.append(token.split('/'))
            for left, right in zip(choices, choices[1:]):
                rules[domain].update((a, b) for a in left for b in right)
    require(all(rules.values()), 'missing exhaustive legal transition table')
    return rules


def digest_json(value, authority=False):
    if authority:
        # shared_disk_clearance_freeze_v4.md:324: no nested hash exceptions.
        value = {k: v for k, v in value.items() if k != 'last_decision'}
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()



def invocation_templates(profile):
    for key in ('invocation', 'broker_invocation', 'executor_invocation', 'intel_invocation', 'existing_admission', 'authorized_payload'):
        if isinstance(profile.get(key), dict):
            yield '/' + key, profile[key]
    for i, child in enumerate(profile.get('children', [])):
        yield '/children/%d/invocation' % i, child['invocation']


def template_names(template):
    return {token['$bind'] for token in template['argv'] +
            [e['value'] for e in template['environment']] if isinstance(token, dict)}


def profile_declarations(profile, name):
    # shared_disk_clearance_freeze_v4.md:158-161: exact owning union, no implicit supplier.
    declarations = profile['bindings']
    by_name = {d['name']: d for d in declarations}
    used = set().union(*(template_names(t) for _, t in invocation_templates(profile)))
    require(len(by_name) == len(declarations) and set(by_name) == used,
            'profile declaration names mismatch: ' + name)
    return by_name


def invocation_coherence(bundle):
    examples = bundle['x-construction']['examples']
    profiles = {}
    sources = {}
    for name, e in examples.items():
        v = e['instance']
        if isinstance(v, dict):
            sources[(e['schema_name'], digest_json(v))] = v
            if e['schema_name'] in ('LaunchProfile', 'UnitProfile'):
                profile_declarations(v, name)
                profiles[(e['schema_name'], digest_json(v))] = v
    count = 0
    for name, e in examples.items():
        if e['schema_name'] != 'InvocationBinding':
            continue
        count += 1
        binding = e['instance']
        key = (binding['profile_type'], binding['profile_sha256'])
        require(key in profiles, 'invocation owning profile unresolved: ' + name)
        profile = profiles[key]
        templates = dict(invocation_templates(profile))
        require(binding['template_path'] in templates, 'invocation template unresolved: ' + name)
        template = templates[binding['template_path']]
        declarations = profile_declarations(profile, name)
        bound = {v['name']: v for v in binding['bound_values']}
        require(len(bound) == len(binding['bound_values']) and set(bound) == template_names(template),
                'invocation bound names mismatch: ' + name)
        values = {}
        for field, v in bound.items():
            declared = declarations[field]
            if v['source_record'] == 'SELF':
                require(v['source_field'] == '' and v['source_record_sha256'] == key[1],
                        'invocation SELF binding mismatch: ' + name + '/' + field)
                selected = key[1]
            else:
                source_key = (v['source_record'], v['source_record_sha256'])
                require(source_key in sources, 'invocation source record unresolved: ' + name + '/' + field)
                source = sources[source_key]
                require(digest_json(source) == v['source_record_sha256'],
                        'invocation source hash mismatch: ' + name + '/' + field)
                try:
                    selected = pointer(source, v['source_field'])
                except ValueError as error:
                    raise ValueError('invocation source pointer unresolved: ' + name + '/' + field + ': ' + str(error)) from error
                if v['source_record'] == 'ScienceLaunchContextRecord':
                    require(source['launch_profile_sha256'] == key[1],
                            'science context owning profile mismatch: ' + name)
                    expected_names = {d['name'] for d in declarations.values() if d['source_field'].startswith('/values/')}
                    require(set(source['values']) == expected_names and
                            (not v['source_field'].startswith('/values/') or v['source_field'] == '/values/' + field),
                            'science context values mismatch: ' + name + '/' + field)
            require(all(v[k] == declared[k] for k in ('name', 'source_record', 'source_field')),
                    'invocation declaration binding mismatch: ' + name + '/' + field)
            require(isinstance(selected, str) and bool(selected) and selected == v['value'],
                    'invocation bound value mismatch: ' + name + '/' + field)
            values[field] = selected
        def render(token):
            return values[token['$bind']] if isinstance(token, dict) else token
        argv = [render(token) for token in template['argv']]
        environment = sorted([{'name': e['name'], 'value': render(e['value'])}
                              for e in template['environment']], key=lambda e: e['name'])
        require(len({e['name'] for e in environment}) == len(environment),
                'invocation environment duplicate name: ' + name)
        # shared_disk_clearance_freeze_v4.md:159: compare arrays reconstructed from sources, then hash them.
        for field, rendered in (('argv', argv), ('environment', environment)):
            require(binding['rendered_' + field] == rendered,
                    'invocation rendered ' + field + ' mismatch: ' + name)
            require(binding['rendered_' + field + '_sha256'] == digest_json(rendered),
                    'invocation rendered ' + field + ' hash mismatch: ' + name)
        require(sum(len(s.encode('utf-8')) for s in argv) <= 16384,
                'invocation argv byte ceiling exceeded: ' + name)
    return count


def mandatory_hash_completeness(text, bundle):
    # shared_disk_clearance_freeze_v4.md:162: recurse schemas, independently of listed references.
    c = bundle['x-construction']
    definitions = bundle['$defs']
    manifest, citations = c['mandatory_hash_fields'], c['mandatory_hash_sources']
    expected = freeze_hash_obligations(text, definitions)
    for name, paths in expected.items():
        missing = set(paths) - set(manifest.get(name, []))
        require(not missing, 'mandatory hash manifest omission: ' + name + ' ' + str(sorted(missing)))
    require(set(manifest) == set(expected), 'mandatory hash manifest schema set mismatch')
    require(isinstance(manifest, dict) and isinstance(citations, dict) and set(manifest) == set(citations),
            'mandatory hash manifest/source keys mismatch')
    lines = text.splitlines()
    citation_path = 'results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md'
    for name, paths in manifest.items():
        require(name in definitions and isinstance(paths, list) and all(isinstance(p, str) for p in paths)
                and len(paths) == len(set(paths)), 'malformed mandatory hash manifest: ' + name)
        match = re.fullmatch(re.escape(citation_path) + r':([1-9][0-9]*)', citations[name])
        require(match is not None and int(match[1]) <= len(lines) and bool(lines[int(match[1]) - 1].strip()),
                'mandatory hash source citation unresolved: ' + name)
    targets = [(r['target_type'], r['target_name'], r['target_pointer']) for r in c['hash_references']]
    require(len(targets) == len(set(targets)), 'duplicate mandatory hash reference target')
    targets = set(targets)
    mandatory = set()
    def visit(value, schema, example, prefix, depth=0):
        require(depth < 256, 'mandatory hash schema depth exceeded')
        if '$ref' in schema:
            name = schema['$ref'][8:]
            for path in manifest.get(name, []):
                require(path.startswith('/'), 'invalid mandatory hash pointer: ' + name)
                try:
                    carried = pointer(value, path)
                except ValueError as error:
                    if str(error).startswith('unresolved JSON pointer:'):
                        continue
                    raise
                if carried is not None:
                    target = ('example', example, prefix + path)
                    mandatory.add(target)
                    require(target in targets, 'mandatory hash reference missing: example/' + example + prefix + path)
            visit(value, definitions[name], example, prefix, depth + 1)
        if isinstance(value, dict):
            for key, child in value.items():
                nested = schema.get('properties', {}).get(key, schema.get('additionalProperties'))
                if isinstance(nested, dict):
                    visit(child, nested, example, prefix + '/' + key.replace('~', '~0').replace('/', '~1'), depth + 1)
        if isinstance(value, list) and 'items' in schema:
            for i, child in enumerate(value):
                visit(child, schema['items'], example, prefix + '/' + str(i), depth + 1)
        for keyword in ('oneOf', 'anyOf', 'allOf'):
            for branch in schema.get(keyword, []):
                if instance_valid(value, branch, definitions):
                    visit(value, branch, example, prefix, depth + 1)
        if 'if' in schema:
            branch = 'then' if instance_valid(value, schema['if'], definitions) else 'else'
            if branch in schema:
                visit(value, schema[branch], example, prefix, depth + 1)
    for name, e in c['examples'].items():
        visit(e['instance'], {'$ref': '#/$defs/' + e['schema_name']}, name, '')
    return len(mandatory)



def observation_revisions(bundle):
    # shared_disk_clearance_freeze_v4.md:94,98-99,102,113,163-181,246:
    # observed precommit pair and ledger are distinct from each resulting pair.
    c = bundle['x-construction']
    examples = c['examples']
    refs = {(r['target_type'], r['target_name'], r['target_pointer']): r for r in c['hash_references']}
    by_digest = {digest_json(e['instance']): e['instance'] for e in examples.values()}
    observation_names = {digest_json(e['instance']): n for n, e in examples.items() if e['schema_name'] == 'ObservationRecord'}
    checked = set()
    def check_observation(observation, before, label):
        label = observation_names.get(digest_json(observation), label)
        epoch, sequence = (before.get('authority_epoch'), before.get('sequence'))
        require((observation['observed_authority_epoch'], observation['observed_sequence']) == (epoch, sequence),
                'observation precommit revision mismatch: ' + label)
        if before.get('record_type') == 'AuthorityRecord':
            require(observation['host_id'] == before['m3_host_id'] and observation['boot_id'] == before['m3_boot_id'],
                    'observation precommit host/boot mismatch: ' + label)
            require(observation['observed_ledger_generation'] == before['ledger_generation'],
                    'observation precommit ledger mismatch: ' + label)
            pending = {s['launch_id'] for s in before['science'] if s['state'] in ('PENDING', 'CLEARED')}
            target = observation['observed_pending_launch_id']
            require(target is None or target in pending, 'observation precommit pending launch mismatch: ' + label)
            require(not pending or target in pending, 'observation precommit pending launch missing: ' + label)
        checked.add(digest_json(observation))
    # Use the independently named transition precommit endpoint, never infer it from the proof.
    for kind, tr in c['transitions'].items():
        before = construction_value(bundle, tr.get('before_type', 'example'), tr['before'])
        after = construction_value(bundle, tr.get('after_type', 'example'), tr['after'])
        if kind == 'QUERY':
            require(before == after, 'QUERY revision changed')
            response = examples[bundle['x-response-mapping']['QUERY']['success']]['instance']
            check_observation(response['body']['observation'], before, 'QUERYSuccessResponse/body/observation')
            continue  # Stored last-decision proof belongs to its earlier commit.
        check_observation(after['observations'], before, tr['after'] + '/observations')
        request = construction_value(bundle, 'example', tr['request'])
        if kind == 'REGISTER_SCIENCE':
            pending_receipt = by_digest.get(before['last_decision'], {})
            r = refs.get(('example', next((n for n, e in examples.items() if e['instance'] == pending_receipt), ''), '/before_state_sha256'))
            require(r is not None and pending_receipt.get('operation') == 'REGISTER_SCIENCE',
                    'science PENDING publication lacks precommit reference')
            initial = pointer(construction_value(bundle, r['source_type'], r['source_name']), r['source_pointer'])
            require(initial['authority_epoch'] == request['authority_epoch'] and initial['sequence'] == request['sequence']
                    and before['sequence'] == initial['sequence'] + 1,
                    'science PENDING publication revision mismatch')
            check_observation(before['observations'], initial, tr['before'] + '/observations')
        if kind in ('INITIALIZE', 'RECONCILE', 'QUIESCE', 'REOPEN', 'SHUTDOWN'):
            approval = by_digest.get(request['body']['approval_receipt'], {})
            require((approval.get('observed_authority_epoch'), approval.get('observed_sequence')) ==
                    (before.get('authority_epoch'), before.get('sequence')),
                    'admin approval observed pair mismatch: ' + kind)
            proposed = after['authority_epoch'] if kind in ('INITIALIZE', 'RECONCILE') else None
            require(approval.get('proposed_epoch') == proposed and
                    (kind not in ('INITIALIZE', 'RECONCILE') or proposed != before.get('authority_epoch')),
                    'admin approval proposed epoch mismatch: ' + kind)
    # Every receipt with linked authority endpoints binds both complete revision pairs.
    for name, e in examples.items():
        v = e['instance']
        if not isinstance(v, dict) or v.get('before_state_sha256') is None or v.get('after_state_sha256') is None:
            continue
        endpoints = []
        for field in ('before_state_sha256', 'after_state_sha256'):
            r = refs.get(('example', name, '/' + field))
            require(r is not None, 'receipt revision lacks endpoint reference: ' + name)
            endpoints.append(pointer(construction_value(bundle, r['source_type'], r['source_name']), r['source_pointer']))
        before, after = endpoints
        if after.get('record_type') != 'AuthorityRecord':
            # F4:176's disable-all and J3 phase_rule's consume control proof are nonauthority.
            continue
        require((v.get('observed_authority_epoch'), v.get('observed_sequence')) ==
                (before.get('authority_epoch'), before.get('sequence')), 'receipt observed pair mismatch: ' + name)
        result_keys = ('authority_epoch', 'sequence') if v['record_type'] == 'ActionReceipt' else ('resulting_authority_epoch', 'resulting_sequence')
        require(tuple(v.get(k) for k in result_keys) == (after['authority_epoch'], after['sequence']),
                'receipt resulting pair mismatch: ' + name)
        if before.get('record_type') == 'AuthorityRecord':
            if v.get('kind') in ('REFUSED', 'HALTED_UNCLEARED'):
                require(before == after, 'refusal changes linked revision: ' + name)
            elif before['authority_epoch'] == after['authority_epoch']:
                require(after['sequence'] == before['sequence'] + 1, 'receipt revision must advance exactly once: ' + name)
            else:
                require(v.get('operation') == 'RECONCILE' and after['sequence'] == 1,
                        'replacement revision mismatch: ' + name)
        else:
            require(v.get('operation') == 'INITIALIZE' and after['sequence'] == 1,
                    'initialization revision mismatch: ' + name)
    return len(checked)


def coherent_examples(text, bundle):
    c = bundle['x-construction']
    examples = c['examples']
    refs = c['hash_references']
    require(isinstance(refs, list) and bool(refs), 'missing construction hash references')
    # shared_disk_clearance_schemas_v3.json:10531-10532 defines the separately
    # projected synthetic artifact; F4:316 still pins the full deployed file.
    external = construction_value(bundle, 'schema', 'external_schema_artifact')
    require(c['external_schema_artifact_sha256'] == digest_json(external),
            'external schema artifact hash mismatch')
    targets = {}
    for ref in refs:
        fields = {'target_type', 'target_name', 'target_pointer', 'source_type',
                  'source_name', 'source_pointer', 'hash_mode'}
        require(isinstance(ref, dict) and set(ref) == fields and
                all(isinstance(x, str) for x in ref.values()), 'malformed hash reference')
        key = (ref['target_type'], ref['target_name'], ref['target_pointer'])
        require(key not in targets, 'duplicate hash reference target: ' + str(key))
        targets[key] = ref
        actual = pointer(construction_value(bundle, key[0], key[1]), key[2])
        require(actual == reference_hash(bundle, ref),
                'hash reference mismatch: ' + key[0] + '/' + key[1] + key[2])
    observation_count = observation_revisions(bundle)
    # Field-level dependency graph: authority projections intentionally do not
    # depend on /last_decision, as required by F4:324; every other cycle fails.
    edges = {}
    for key, ref in targets.items():
        source = (ref['source_type'], ref['source_name'])
        prefix = ref['source_pointer']
        edges[key] = [other for other in targets if other[:2] == source
                      and (other[2] == prefix or other[2].startswith(prefix + '/'))
                      and not (ref['hash_mode'] == 'authority' and
                               (other[2] == '/last_decision' or
                                other[2].startswith('/last_decision/')))]
    visiting, finished = set(), set()
    def visit(key):
        require(key not in visiting, 'cyclic construction hash dependency: ' + str(key))
        if key in finished:
            return
        visiting.add(key)
        for child in edges[key]:
            visit(child)
        visiting.remove(key)
        finished.add(key)
    for key in edges:
        visit(key)
    def blobs(value, location):
        # shared_disk_clearance_freeze_v4.md:74: canonical_utf8 must itself
        # parse as one named immutable record and match the blob's digest.
        if isinstance(value, dict):
            if 'canonical_utf8' in value:
                raw = value['canonical_utf8']
                require(value['sha256'] == hashlib.sha256(raw.encode('utf-8')).hexdigest(),
                        'ReceiptBlob hash mismatch: ' + location)
                record = json.loads(raw, object_pairs_hook=unique_object, parse_float=finite_float,
                                    parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite blob JSON')))
                require(isinstance(record, dict) and record.get('record_type') in bundle['$defs'],
                        'ReceiptBlob unknown record: ' + location)
                require(canonical(record) == raw and instance_valid(record,
                        bundle['$defs'][record['record_type']], bundle['$defs']),
                        'ReceiptBlob noncanonical/invalid record: ' + location)
                blobs(record, location + '/parsed')
            for key, child in value.items():
                blobs(child, location + '/' + key)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                blobs(child, location + '/' + str(i))
    for name, example in examples.items():
        blobs(example['instance'], name)
    for name, artifact in c['artifacts'].items():
        require(isinstance(artifact, dict), 'malformed construction artifact: ' + name)
        if 'utf8' in artifact:
            require(isinstance(artifact['utf8'], str) and artifact.get('sha256') ==
                    hashlib.sha256(artifact['utf8'].encode('utf-8')).hexdigest(),
                    'artifact raw-byte hash mismatch: ' + name)
    pairs = {}
    for name, example in examples.items():
        value = example['instance']
        if not isinstance(value, dict):
            continue
        if value.get('outcome') == 'COMMITTED':
            # shared_disk_clearance_freeze_v4.md:71,74: successful durable
            # actions bind both complete state snapshots before acknowledgment.
            require(all(isinstance(value.get(k), str) and re.fullmatch('[0-9a-f]{64}', value[k])
                        for k in ('before_state_sha256', 'after_state_sha256')),
                    'COMMITTED receipt lacks before/after hashes: ' + name)
        if value.get('record_type') == 'AuthorityRecord':
            observation = value['observations']
            # shared_disk_clearance_freeze_v4.md:94,163: host/boot revalidate.
            for key, observed in (('m3_host_id', 'host_id'), ('m3_boot_id', 'boot_id')):
                require(value[key] == observation[observed],
                        'authority observation binding mismatch: ' + name + '/' + key)
            states = {x['state'] for x in value['science']}
            transfer = value['transfer']
            unresolved = 'UNRESOLVED' in states or transfer and transfer['state'] == 'UNRESOLVED'
            # shared_disk_clearance_freeze_v4.md:234: unresolved forces recovery;
            # otherwise derive running/pending/open, retaining explicit recovery.
            expected = ('RECOVERY_REQUIRED' if unresolved else 'SCIENCE_RUNNING' if 'RUNNING' in states
                        else 'SCIENCE_PENDING' if states else 'OPEN')
            require(value['authority_state'] == expected or
                    not unresolved and value['authority_state'] == 'RECOVERY_REQUIRED',
                    'authority derived state mismatch: ' + name)
        fields = ('before_state_sha256', 'after_state_sha256')
        if any(value.get(field) is not None for field in fields):
            endpoints = []
            for field in fields:
                ref = targets.get(('example', name, '/' + field))
                require(ref is not None, 'receipt state hash lacks reference: ' + name + '/' + field)
                endpoints.append(pointer(construction_value(bundle, ref['source_type'],
                                                           ref['source_name']), ref['source_pointer']))
            require(all(isinstance(v, dict) for v in endpoints),
                    'receipt state projection must be object: ' + name)
            before, after = endpoints
            pairs[name] = (before, after)
            if before.get('sequence') is not None and after.get('sequence') is not None:
                if value.get('kind') in ('REFUSED', 'HALTED_UNCLEARED'):
                    require(before == after, 'refusal changes linked state: ' + name)
                elif before.get('authority_epoch') != after.get('authority_epoch'):
                    # shared_disk_clearance_freeze_v4.md:285: replacement uses
                    # a new epoch; shared_disk_clearance_freeze_v4.md:163 restarts sequence at 1.
                    require(value.get('operation') == 'RECONCILE' and after['sequence'] == 1,
                            'invalid epoch transition: ' + name)
                else:
                    require(after['sequence'] == before['sequence'] + 1,
                            'receipt revision must advance exactly once: ' + name)
                for key in ('authority_epoch', 'sequence'):
                    if key in value:
                        require(value[key] == after[key], 'receipt after binding mismatch: ' + name + '/' + key)
    rules = transition_rules(text)
    by_digest = {digest_json(e['instance']): (name, e['instance']) for name, e in examples.items()}
    # shared_disk_clearance_freeze_v4.md:189-191: reconciliation must agree
    # with its selected fence; missing history retains unresolved exclusion.
    for name, example in examples.items():
        value = example['instance']
        if example['schema_name'] != 'ReconciliationReceipt':
            continue
        fence = by_digest.get(value['fence_receipt'], ('', {}))[1]
        require(fence.get('record_type') == 'FencingReceipt' and
                fence.get('kind') == value['fencing_kind'],
                'reconciliation fence binding mismatch: ' + name)
        if value['fencing_kind'] == 'NO_PRIOR_AUTHORITY':
            require(value['prior_authority_sha256'] is None and value['all_history_accounted'] is True
                    and value['retained_unresolved_ids'] == [], 'invalid no-prior reconciliation: ' + name)
        elif value['fencing_kind'] == 'MISSING_HISTORY':
            require(value['prior_authority_sha256'] is None and value['all_history_accounted'] is False
                    and bool(value['retained_unresolved_ids']), 'missing history loses exclusion: ' + name)
        else:
            require(value['prior_authority_sha256'] is not None, 'prior writer reconciliation lacks history: ' + name)
    def check_edges(before, after, receipt, name, request=None):
        if before.get('record_type') != 'AuthorityRecord' or after.get('record_type') != 'AuthorityRecord':
            return
        left, right = before['transfer'], after['transfer']
        a, b = left['state'] if left else None, right['state'] if right else None
        require(a == b or (a, b) in rules['transfer'],
                'illegal transfer transition: ' + name + '/' + str(a) + '->' + str(b))
        if a == 'GRANTED' and b == 'ACTIVE':
            # shared_disk_clearance_freeze_v4.md:225,240: coordinator consumes
            # the enrolled executor's exact one-use allowance before ACTIVE.
            require(request is not None and request['kind'] == 'CONSUME_UNIT' and
                    receipt.get('record_type') == 'ConsumeUnitReceipt' and
                    receipt['actor'] == request['body']['actor'] and
                    receipt['actor']['role'] == 'COORDINATOR' and
                    receipt['subject'] == request['body']['executor'] == right['executor'] and
                    receipt['committed_elapsed'] < left['consume_by_elapsed'],
                    'unit consumption actor/expiry mismatch: ' + name)
            for key in ('job_id', 'unit_id', 'allowance_nonce', 'allowance_sequence', 'unit_profile_sha256'):
                require(left[key] == right[key] == receipt[key] == request['body'][key],
                        'unit consumption binding mismatch: ' + name + '/' + key)
            require(receipt['sandbox_profile_sha256'] == request['body']['sandbox_profile_sha256'] ==
                    right['executor']['sandbox_profile_sha256'] and
                    receipt['enrollment_receipt'] == request['body']['enrollment_receipt'],
                    'unit consumption enrollment/profile mismatch: ' + name)
        if b in ('PAUSED', 'COMPLETED', 'CANCELLED'):
            # shared_disk_clearance_freeze_v4.md:212-215,226-229,231: closure
            # and checkpoint are durable proof, not an unbound digest.
            require(by_digest.get(right['closure_receipt'], ('', {}))[1].get('record_type') ==
                    'ClosureReceipt', 'terminal/paused transfer lacks closure: ' + name)
        if a == 'PAUSED' and b == 'GRANTED':
            # shared_disk_clearance_freeze_v4.md:230: fresh unit/nonce and
            # explicit resume approval; archived old unit may not be reused.
            require(left['unit_id'] != right['unit_id'] and
                    left['allowance_nonce'] != right['allowance_nonce'] and not after['science'] and
                    any(by_digest.get(h, ('', {}))[1].get('record_type') == 'ResumeApprovalRecord'
                        for h in receipt.get('input_receipts', [])), 'invalid fresh resume: ' + name)
        old = {x['launch_id']: x for x in before['science']}
        new = {x['launch_id']: x for x in after['science']}
        require(len(old) == len(before['science']) and len(new) == len(after['science']),
                'duplicate live science launch: ' + name)
        for launch in old.keys() | new.keys():
            a = old[launch]['state'] if launch in old else None
            b = new[launch]['state'] if launch in new else None
            if a == 'CLEARED' and b == 'RUNNING':
                # shared_disk_clearance_freeze_v4.md:222: exact launch/nonce/
                # sequence, same clearance and now strictly below expiry.
                clearance = old[launch]['clearance']
                body = request['body'] if request is not None else {}
                require(request is not None and request['kind'] == 'CONSUME_CLEARANCE' and
                        body.get('launch_id') == launch and
                        body.get('clearance_nonce') == clearance['nonce'] and
                        body.get('clearance_sequence') == clearance['sequence'] == before['sequence'] and
                        new[launch]['clearance'] == clearance and
                        clearance['issued_elapsed'] <= receipt['entry_elapsed'] <=
                        receipt['completed_elapsed'] < clearance['consume_by_elapsed'],
                        'clearance consumption binding mismatch: ' + name)
                proof_hash = new[launch]['consume_receipt']
                proof = by_digest.get(proof_hash, ('', {}))[1]
                require(proof_hash in receipt['input_receipts'] and
                        proof.get('record_type') == 'ActionReceipt' and
                        proof.get('operation') == 'CONSUME_CLEARANCE' and
                        proof.get('outcome') == 'COMMITTED' and
                        proof.get('authority_epoch') == before['authority_epoch'] and
                        proof.get('sequence') == after['sequence'],
                        'clearance consumption lacks one-use control proof: ' + name)
            if b is None and a is not None:
                # shared_disk_clearance_freeze_v4.md:223: terminal receipt/archive
                # removes the live entry atomically; validate the terminal proof.
                require(request is not None and request['kind'] == 'RELEASE_SCIENCE' and
                        request['body']['launch_id'] == launch and
                        (a, request['body']['target_state']) in rules['science'] and
                        request['body']['closure_receipt'] in receipt.get('input_receipts', []) and
                        by_digest.get(request['body']['closure_receipt'], ('', {}))[1].get('record_type') ==
                        'ClosureReceipt', 'science archive lacks closure proof: ' + name)
            else:
                require(a == b or (a, b) in rules['science'],
                        'illegal science transition: ' + name + '/' + str(a) + '->' + str(b))
        a, b = before['authority_state'], after['authority_state']
        # shared_disk_clearance_freeze_v4.md:234: same state, any->recovery,
        # derived pending/running/open, recovery release only through reconciliation.
        allowed = {( 'OPEN', 'SCIENCE_PENDING'), ('SCIENCE_PENDING', 'SCIENCE_RUNNING'),
                   ('SCIENCE_RUNNING', 'SCIENCE_PENDING'), ('SCIENCE_PENDING', 'OPEN'),
                   ('SCIENCE_RUNNING', 'OPEN')}
        require(a == b or b == 'RECOVERY_REQUIRED' or (a, b) in allowed or
                a == 'RECOVERY_REQUIRED' and receipt.get('operation') == 'REOPEN',
                'illegal authority transition: ' + name)
        if a == 'RECOVERY_REQUIRED' and b != a:
            require(request is not None and request['body'].get('reconciliation_receipt') in by_digest,
                    'recovery release lacks reconciliation: ' + name)
            reconciliation = by_digest[request['body']['reconciliation_receipt']][1]
            require(reconciliation.get('record_type') == 'ReconciliationReceipt' and
                    reconciliation['new_authority_epoch'] == after['authority_epoch'],
                    'recovery reconciliation epoch mismatch: ' + name)
    for kind, tr in c['transitions'].items():
        row = bundle['x-response-mapping'][kind]
        before = construction_value(bundle, tr.get('before_type', 'example'), tr['before'])
        after = construction_value(bundle, tr.get('after_type', 'example'), tr['after'])
        receipt = construction_value(bundle, 'example', tr['receipt'])
        request = construction_value(bundle, 'example', tr['request'])
        success = construction_value(bundle, 'example', tr['success'])
        for key in ('request', 'success'):
            require(examples[tr[key]]['schema_name'] == row[key], 'transition schema mapping mismatch: ' + kind)
        require(request['kind'] == kind, 'transition request kind mismatch: ' + kind)
        if kind in ('INITIALIZE', 'QUIESCE', 'RECONCILE', 'REOPEN', 'SHUTDOWN'):
            # shared_disk_clearance_freeze_v4.md:186-191,196: operation-specific
            # fencing variants and immutable MAESTRO administration approval.
            # shared_disk_clearance_freeze_v4.md:98,163 separates the observed pair.
            body = request['body']
            approval = by_digest.get(body['approval_receipt'], ('', {}))[1]
            require(approval.get('record_type') == 'MaestroApprovalReceipt' and
                    approval.get('operation') == kind and
                    approval.get('request_nonce') == request['request_nonce'] and
                    approval.get('observed_sequence') == (None if kind == 'INITIALIZE' else request['sequence']) and
                    approval.get('observed_authority_epoch') == (None if kind == 'INITIALIZE' else request['authority_epoch']),
                    'admin approval binding mismatch: ' + kind)
            if body['fence_receipt'] is not None:
                fence = by_digest.get(body['fence_receipt'], ('', {}))[1]
                permitted = ({'NO_PRIOR_AUTHORITY', 'MISSING_HISTORY'} if kind == 'INITIALIZE'
                             else {'PRIOR_WRITER_CEASED', 'MISSING_HISTORY'})
                require(fence.get('record_type') == 'FencingReceipt' and fence.get('kind') in permitted,
                        'admin fence kind mismatch: ' + kind)
            else:
                require(kind == 'QUIESCE', 'admin operation lacks fence: ' + kind)
            if body['reconciliation_receipt'] is not None:
                reconciliation = by_digest.get(body['reconciliation_receipt'], ('', {}))[1]
                require(reconciliation.get('record_type') == 'ReconciliationReceipt' and
                        reconciliation.get('fence_receipt') == body['fence_receipt'],
                        'admin reconciliation binding mismatch: ' + kind)
                if kind in ('INITIALIZE', 'RECONCILE', 'REOPEN'):
                    require(reconciliation['new_authority_epoch'] == after['authority_epoch'],
                            'admin reconciliation epoch mismatch: ' + kind)
        observed = before
        if request['sequence'] != before['sequence']:
            # shared_disk_clearance_freeze_v4.md:221-222,246: REGISTER_SCIENCE
            # durably publishes PENDING first; clearance is its second transition.
            prior = [(n, a, b) for n, (a, b) in pairs.items()
                     if examples[n]['instance'].get('request_nonce') == request['request_nonce']
                     and examples[n]['instance'].get('operation') == 'REGISTER_SCIENCE'
                     and a.get('sequence') == request['sequence'] and b == before]
            require(kind == 'REGISTER_SCIENCE' and len(prior) == 1,
                    'transition request sequence mismatch: ' + kind)
            observed = prior[0][1]
            check_edges(observed, before, examples[prior[0][0]]['instance'], prior[0][0], request)
        require(request['authority_epoch'] == observed['authority_epoch'],
                'transition request epoch mismatch: ' + kind)
        for key in ('authority_epoch', 'sequence'):
            require(success[key] == after[key], 'transition success ' + key + ' mismatch: ' + kind)
        require(success['request_nonce'] == request['request_nonce'], 'transition success nonce mismatch: ' + kind)
        require(success['m3_host_id'] == after['m3_host_id'] and success['m3_boot_id'] == after['m3_boot_id'],
                'transition success host/boot mismatch: ' + kind)
        require(success['decision_receipt'] == digest_json(receipt), 'transition receipt link mismatch: ' + kind)
        if kind == 'QUERY':
            # shared_disk_clearance_freeze_v4.md:74: read-only, current last_decision.
            require(before == after and success['decision_receipt'] == after['last_decision'] and
                    success['grant'] is None and success['clearance'] is None,
                    'QUERY changes state or permission')
        else:
            require(receipt.get('request_nonce') == request['request_nonce'],
                    'transition receipt nonce mismatch: ' + kind)
            require(receipt['before_state_sha256'] == digest_json(before, before.get('record_type') == 'AuthorityRecord')
                    and receipt['after_state_sha256'] == digest_json(after, after.get('record_type') == 'AuthorityRecord'),
                    'transition receipt state mismatch: ' + kind)
            require(after['last_decision'] == digest_json(receipt), 'transition last decision mismatch: ' + kind)
            if kind == 'INITIALIZE':
                # shared_disk_clearance_freeze_v4.md:187-188,285: absent-store
                # control is not authority; initialization stays RECOVERY_REQUIRED.
                require(before.get('record_type') is None and after['authority_state'] == 'RECOVERY_REQUIRED',
                        'initialization infers OPEN authority')
            check_edges(before, after, receipt, kind, request)
        for example in examples.values():
            if example['schema_name'] != row['refusal']:
                continue
            refusal = example['instance']
            for key in ('request_nonce', 'authority_epoch', 'sequence'):
                require(refusal[key] == request[key], 'refusal request binding mismatch: ' + kind + '/' + key)
            record = by_digest.get(refusal['decision_receipt'], ('', {}))[1]
            require(record.get('record_type') == 'DecisionReceipt' and
                    record.get('request_nonce') == request['request_nonce'] and
                    record.get('kind') == refusal['kind'] and
                    refusal['body']['decision'] == refusal['decision_receipt'],
                    'refusal receipt binding mismatch: ' + kind)
    # Also enforce state edges for every linked receipt, not just table successes.
    for name, (before, after) in pairs.items():
        receipt = examples[name]['instance']
        request = next((construction_value(bundle, 'example', tr['request'])
                        for kind, tr in c['transitions'].items()
                        if kind != 'QUERY' and tr['receipt'] == name), None)
        check_edges(before, after, receipt, name, request)
    return len(refs), observation_count


def canonical(value):
    # shared_disk_clearance_freeze_v4.md:324: UTF-8 key order, literal UTF-8,
    # decimal integers, lowercase \u00xx controls, no insignificant whitespace.
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        value.encode('utf-8')  # Reject unpaired surrogates.
        return '"' + ''.join('\\"' if c == '"' else '\\\\' if c == '\\'
                             else '\\u%04x' % ord(c) if ord(c) < 32 else c
                             for c in value) + '"'
    if isinstance(value, list):
        return '[' + ','.join(canonical(v) for v in value) + ']'
    require(isinstance(value, dict), 'canonical JSON requires integer-only JSON')
    return '{' + ','.join(canonical(k) + ':' + canonical(value[k])
                          for k in sorted(value, key=lambda k: k.encode('utf-8'))) + '}'


def pointer(value, path):
    require(isinstance(path, str) and (not path or path.startswith('/')),
            'invalid JSON pointer: ' + str(path))
    for token in path.split('/')[1:]:
        require(re.search(r'~(?![01])', token) is None, 'invalid JSON pointer escape')
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            require(re.fullmatch(r'0|[1-9][0-9]*', token) is not None,
                    'invalid JSON pointer array index')
            index = int(token)
            require(index < len(value), 'unresolved JSON pointer: ' + path)
            value = value[index]
        else:
            require(isinstance(value, dict) and token in value,
                    'unresolved JSON pointer: ' + path)
            value = value[token]
    return value


def construction_value(bundle, category, name):
    c = bundle['x-construction']
    if category == 'schema':
        require(name == 'external_schema_artifact', 'unknown schema artifact: ' + name)
        return {k: v for k, v in bundle.items() if k != 'x-construction'}
    require(category in ('example', 'artifact', 'state'), 'unknown reference type: ' + category)
    table = c[{'example': 'examples', 'artifact': 'artifacts', 'state': 'states'}[category]]
    require(name in table, 'unresolved construction reference: ' + category + '/' + name)
    return table[name]['instance'] if category == 'example' else table[name]


def reference_hash(bundle, ref):
    value = pointer(construction_value(bundle, ref['source_type'], ref['source_name']),
                    ref['source_pointer'])
    mode = ref['hash_mode']
    if mode == 'authority':
        # shared_disk_clearance_freeze_v4.md:324: omit only last_decision.
        require(isinstance(value, dict) and value.get('record_type') == 'AuthorityRecord',
                'authority projection requires AuthorityRecord')
        value = {k: v for k, v in value.items() if k != 'last_decision'}
    require(mode in ('raw', 'canonical', 'authority'), 'unknown hash mode: ' + mode)
    if mode == 'raw':
        require(isinstance(value, str), 'raw hash source must be UTF-8 text')
        payload = value.encode('utf-8')
    else:
        payload = canonical(value).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def reseal_construction(bundle):
    """Rebase all synthetic dependent hashes and serialized blobs for mutation isolation."""
    c = bundle['x-construction']
    c['external_schema_artifact_sha256'] = hashlib.sha256(canonical(
        construction_value(bundle, 'schema', 'external_schema_artifact')).encode()).hexdigest()
    for _ in range(len(c['hash_references']) + 1):
        changed = False
        for ref in c['hash_references']:
            value = construction_value(bundle, ref['target_type'], ref['target_name'])
            parent_path, token = ref['target_pointer'].rsplit('/', 1)
            parent = pointer(value, parent_path)
            token = token.replace('~1', '/').replace('~0', '~')
            key = int(token) if isinstance(parent, list) else token
            digest = reference_hash(bundle, ref)
            # Rebuild redundant serialized bytes when rebasing canonical sources;
            # controls must not leave stale artifact/ReceiptBlob payloads behind.
            if ref['hash_mode'] in ('canonical', 'authority') and key == 'sha256':
                source = pointer(construction_value(bundle, ref['source_type'], ref['source_name']),
                                 ref['source_pointer'])
                if ref['hash_mode'] == 'authority':
                    source = {k: v for k, v in source.items() if k != 'last_decision'}
                serialized = canonical(source)
                if isinstance(parent, dict) and 'utf8' in parent:
                    parent['utf8'] = serialized
                if isinstance(parent, dict) and 'canonical_utf8' in parent:
                    parent['canonical_utf8'] = serialized
            if parent[key] != digest:

                parent[key] = digest
                changed = True
        if not changed:
            return
    raise ValueError('construction reseal did not converge')


CONTROL_MESSAGES = {
    'M1': 'schema lacks assertion: Hash',
    'M2': 'SSH request kind missing/non-wire: REQUEST_UNIT',
    'M3': 'missing/mismatched success mapping for REQUEST_UNIT',
    'M4': 'hash reference mismatch: example/Process/executable_sha256',
    'M5': 'missing schema or catalog entry:',
    'M6': 'malformed required at GrantRecord',
    'M7': 'invocation source pointer unresolved: InvocationBindingExecutor/job_id',
    'M8': 'invocation rendered argv mismatch: InvocationBindingExecutor',
    'M9': 'invocation declaration binding mismatch: InvocationBinding/job_id',
    'M10': 'mandatory hash reference missing: example/InvocationBindingExecutor/profile_sha256',
    'M11': 'observation precommit revision mismatch: ObservationRecordScienceCleared',
    'M12': 'profiles[0]/authorized_payload/sandbox_profile_sha256: additional property',
    'R1': 'R1 guard composition mismatch',
    'R2': 'R2 P2 inner launcher must be CHILD_ONLY',
    'R3': 'R3 science child role permits non-science authority',
    'R4': 'R4 P3 replication Git profile missing',
    'R6Q': 'observation precommit revision mismatch: QUERYSuccessResponse/body/observation',
    'R6H': 'mandatory hash manifest omission: CheckpointRecord',
    'E3': 'invalid example: REQUEST_UNITRequest',
    'E5': 'missing refusal example: REQUEST_UNIT',
    'E4S': 'transition request sequence mismatch: ATTACH_STREAM',
    'E4A': 'authority derived state mismatch: AuthorityRecordStream',
    'E4C': 'invalid example: ActionReceipt',
    'E4N': 'clearance consumption binding mismatch: CONSUME_CLEARANCE',
    'E4F': 'admin fence kind mismatch: INITIALIZE',
    'E4B': 'ReceiptBlob hash mismatch: ReceiptBlob',
}


def damaged_copy(control, freeze, schemas):
    bundle = read_json(schemas)
    text = freeze.read_text(encoding='utf-8')
    c = bundle['x-construction']
    if control in ('M7', 'M8', 'M9', 'M10', 'M11'):
        binding = c['examples']['InvocationBindingExecutor']['instance']
        if control == 'M7':
            binding['bound_values'][0]['source_field'] = '/transfer/not_a_field'
        elif control == 'M8':
            binding['rendered_argv'][0] = 'executor-mutated'
        elif control == 'M9':
            next(d for d in c['examples']['UnitProfile']['instance']['bindings'] if d['name'] == 'job_id')['source_field'] = '/transfer/unit_id'
        elif control == 'M10':
            refs = c['hash_references']
            c['hash_references'] = [r for r in refs if (r['target_type'], r['target_name'], r['target_pointer']) !=
                                    ('example', 'InvocationBindingExecutor', '/profile_sha256')]
            require(len(refs) - len(c['hash_references']) == 1, 'M10 must drop exactly one binding')
        else:
            observation = c['examples']['ObservationRecordScienceCleared']['instance']
            original = canonical(observation)
            revision = c['examples'][c['transitions']['REGISTER_SCIENCE']['after']]['instance']['sequence']
            def damage(value):
                if isinstance(value, dict):
                    if canonical(value) == original:
                        value['observed_sequence'] = revision
                    for child in value.values():
                        damage(child)
                elif isinstance(value, list):
                    for child in value:
                        damage(child)
            damage(c['examples'])
        reseal_construction(bundle)
    elif control == 'M1':
        bundle['$defs']['Hash'] = {'description': 'C:47'}
    elif control == 'M2':
        row = bundle['x-response-mapping'].pop('REQUEST_UNIT')
        names = {row[k] for k in ('request', 'success', 'refusal')}
        for name in names:
            del bundle['$defs'][name]
            del bundle['x-catalog'][name]
        bundle['oneOf'] = [r for r in bundle['oneOf'] if r['$ref'][8:] not in names]
        kinds = bundle['$defs']['ResponseMapping']['properties']['request_kind']['enum']
        kinds.remove('REQUEST_UNIT')
        mappings_schema = bundle['$defs']['ConsumerInterfaceProfile']['properties']['mappings']
        mappings_schema['minItems'] = mappings_schema['maxItems'] = len(kinds)
        removed = {n for n, e in c['examples'].items() if e['schema_name'] in names or
                   isinstance(e['instance'], dict) and
                   e['instance'].get('request_kind') == 'REQUEST_UNIT'}
        c['examples'] = {n: e for n, e in c['examples'].items() if n not in removed}
        for example in c['examples'].values():
            instance = example['instance']
            if isinstance(instance, dict) and example['schema_name'] == 'ConsumerInterfaceProfile':
                instance['mappings'] = [m for m in instance['mappings']
                                        if m['request_kind'] != 'REQUEST_UNIT']
        del c['transitions']['REQUEST_UNIT']
        c['hash_references'] = [r for r in c['hash_references']
                                if r['source_name'] not in removed | names
                                and r['target_name'] not in removed | names]
        # Remove only §4's formal mapping row. §3 remains independently intact.
        text, count = re.subn(r'^\| request \| `REQUEST_UNIT` .*\n', '', text, flags=re.M)
        require(count == 1, 'M2 must remove exactly one §4 mapping row')
        reseal_construction(bundle)
    elif control == 'M3':
        row = bundle['x-response-mapping']['REQUEST_UNIT']
        row['success'], row['refusal'] = row['refusal'], row['success']
    elif control == 'M4':
        c['examples']['Process']['instance']['executable_sha256'] = '0' * 64
    elif control == 'E4B':
        c['examples']['ReceiptBlob']['instance']['canonical_utf8'] = 'null'
    elif control == 'E4F':
        for ref in c['hash_references']:
            if ref['target_name'] == 'INITIALIZERequest' and ref['target_pointer'] == '/body/fence_receipt':
                ref['source_name'] = 'PriorWriterCeasedFencingReceipt'
        reseal_construction(bundle)
    elif control == 'E4N':
        c['examples']['CONSUME_CLEARANCERequest']['instance']['body']['clearance_nonce'] = '0' * 32
    elif control == 'E4S':
        c['examples']['ATTACH_STREAMRequest']['instance']['sequence'] = 99
    elif control == 'E4A':
        c['examples']['AuthorityRecordStream']['instance']['authority_state'] = 'SCIENCE_RUNNING'
        reseal_construction(bundle)
    elif control == 'E4C':
        c['examples']['ActionReceipt']['instance']['before_state_sha256'] = None
        c['hash_references'] = [r for r in c['hash_references']
                                if not (r['target_name'] == 'ActionReceipt' and
                                        r['target_pointer'] == '/before_state_sha256')]
        reseal_construction(bundle)
    elif control == 'M5':
        del bundle['$defs']['GrantRecord']
    elif control == 'M6':
        bundle['$defs']['GrantRecord']['required'] = 'x'
    elif control == 'E3':
        c['examples']['REQUEST_UNITRequest']['instance']['kind'] = 'QUERY'
    elif control == 'E5':
        del c['examples']['REQUEST_UNITRefusalResponse']
        c['hash_references'] = [r for r in c['hash_references']
                                if r['target_name'] != 'REQUEST_UNITRefusalResponse'
                                and r['source_name'] != 'REQUEST_UNITRefusalResponse']
    else:
        raise ValueError('unknown mutation control: ' + control)
    schema_path = MemoryPath(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n')
    return sealed_memory(text, schema_path)


class MemoryPath:
    def __init__(self, text):
        self.text = text
    def read_text(self, encoding='utf-8'):
        return self.text
    def read_bytes(self):
        return self.text.encode('utf-8')


def sealed_memory(text, schema_path):
    for name, digest in hashes(text, schema_path).items():
        text, count = re.subn(r'(\| ' + name + r' pin \| `)[0-9a-f]{64}(`)',
                             lambda m: m[1] + digest + m[2], text)
        require(count == 1, 'mutation missing pin row: ' + name)
    return MemoryPath(text), schema_path


def mutation_controls(freeze, schemas, controls=None):
    # Every branch uses fresh in-memory JSON; no directory, file, or subprocess checker.
    check(freeze, schemas)
    validate_profiles(PROFILES, read_json(schemas), freeze.read_text())
    failures = []
    selected = controls or tuple(CONTROL_MESSAGES)
    for control in selected:
        expected = CONTROL_MESSAGES[control]
        if control in ('R1', 'R2', 'R3', 'R4', 'R6Q', 'R6H', 'M12'):
            bundle = read_json(schemas)
            profiles = read_json(PROFILES)
            if control == 'R1':
                profiles['profiles'][0]['invocation'] = copy.deepcopy(profiles['profiles'][0]['authorized_payload'])
            elif control == 'R2':
                q = next(q for q in profiles['profiles'] if Path(q['entrypoint']).name == 'run_c10w_stage.sh' and 'p2-shuf-s1' in q['authorized_payload']['argv'])
                q['admission_scope'] = 'TOP_LEVEL'
            elif control == 'R3':
                bundle['$defs']['ScienceChildProfile']['oneOf'][0]['properties']['role'] = {'$ref': '#/$defs/Role'}
            elif control == 'R4':
                q = next(q for q in profiles['profiles'] if Path(q['entrypoint']).name == 'c10w_oracle_step0.py' and 'p3-shuf-s0' in q['authorized_payload']['argv'])
                q['children'] = [ch for ch in q['children'] if ch.get('trace_site') != 'science-replication']
            elif control == 'R6Q':
                observation = bundle['x-construction']['examples']['QUERYSuccessResponse']['instance']['body']['observation']
                require(observation['observed_sequence'] == 3, 'QUERY positive control not sequence 3')
                observation['observed_sequence'] = 4
            elif control == 'R6H':
                c = bundle['x-construction']
                c['mandatory_hash_fields']['CheckpointRecord'].remove('/policy_sha256')
                refs = c['hash_references']
                c['hash_references'] = [r for r in refs if (r['target_type'], r['target_name'], r['target_pointer']) != ('example', 'CheckpointRecord', '/policy_sha256')]
                require(len(refs) - len(c['hash_references']) == 1, 'R6H must remove one root reference')
            elif control == 'M12':
                profiles['profiles'][0]['authorized_payload']['sandbox_profile_sha256'] = '0' * 64
            copy_f, copy_j = sealed_memory(freeze.read_text(), MemoryPath(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n'))
        else:
            copy_f, copy_j = damaged_copy(control, freeze, schemas)
            profiles = None
        try:
            if control in ('R1', 'R2', 'R4'):
                REQUIRED_CHECKS[control](profiles, bundle)
            elif control == 'M12':
                validate_profiles(MemoryPath(json.dumps(profiles)), bundle, copy_f.read_text())
            else:
                check(copy_f, copy_j)
        except ValueError as error:
            actual = str(error)
            if expected in actual:
                print('RED %s: exit 1: %s' % (control, actual))
            else:
                failures.append(control)
                print('WRONG RED %s: expected %r; got %s' % (control, expected, actual))
        else:
            failures.append(control)
            print('UNEXPECTED GREEN ' + control)
    require(not failures, 'mutation control expectations unmet: ' + ','.join(failures))
    print('GREEN mutation controls: %d intended RED, zero filesystem writes' % len(selected))


def instance_errors(value, schema, definitions, location):
    """Explain each failed assertion using the same validator as construction examples."""
    if instance_valid(value, schema, definitions):
        return []
    if '$ref' in schema:
        return instance_errors(value, definitions[schema['$ref'][8:]], definitions, location)
    errors = []
    for keyword in ('oneOf', 'anyOf'):
        if keyword in schema:
            branches = schema[keyword]
            # Select a discriminated object shape before reporting nested failures.
            candidates = [b for b in branches if isinstance(value, dict) and
                          all(k in value and json_equal(value[k], p['const'])
                              for k, p in b.get('properties', {}).items() if 'const' in p)]
            if len(candidates) != 1:
                candidates = branches
            alternatives = [instance_errors(value, b, definitions, location) for b in candidates]
            best = min(alternatives, key=len)
            errors.extend(best or [location + ': ' + keyword + ' has wrong number of matching shapes'])
    for branch in schema.get('allOf', []):
        errors.extend(instance_errors(value, branch, definitions, location))
    if 'if' in schema:
        branch = 'then' if instance_valid(value, schema['if'], definitions) else 'else'
        if branch in schema:
            errors.extend(instance_errors(value, schema[branch], definitions, location))
    if 'type' in schema and not instance_valid(value, {'type': schema['type']}, definitions):
        return errors + [location + ': expected type ' + str(schema['type'])]
    for keyword in ('const', 'enum', 'pattern', 'minimum', 'maximum', 'minLength', 'maxLength',
                    'minItems', 'maxItems', 'minProperties', 'maxProperties', 'not'):
        if keyword in schema and not instance_valid(value, {keyword: schema[keyword]}, definitions):
            errors.append(location + ': violates ' + keyword)
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(location + '/' + key + ': required field missing')
        properties = schema.get('properties', {})
        for key, child in value.items():
            path = location + '/' + key.replace('~', '~0').replace('/', '~1')
            if 'propertyNames' in schema:
                errors.extend(instance_errors(key, schema['propertyNames'], definitions, path + '/name'))
            nested = properties.get(key, schema.get('additionalProperties'))
            if nested is False:
                errors.append(path + ': additional property')
            elif isinstance(nested, dict):
                errors.extend(instance_errors(child, nested, definitions, path))
    if isinstance(value, list) and 'items' in schema:
        for i, child in enumerate(value):
            errors.extend(instance_errors(child, schema['items'], definitions, location + '/' + str(i)))
    return list(dict.fromkeys(errors)) or [location + ': schema assertion failed']


def validate_profiles(path, bundle, text):
    profiles = read_json(path)
    require(isinstance(profiles, dict), 'profiles document must be an object')
    definitions = bundle['$defs']
    errors = []
    validated, untyped = 0, 0
    for category in ('profiles', 'not_admitted'):
        entries = profiles.get(category)
        require(isinstance(entries, list), category + ' must be an array')
        for i, entry in enumerate(entries):
            location = category + '[%d]' % i
            if not isinstance(entry, dict):
                errors.append(location + ': expected object')
                continue
            name = 'LaunchProfile' if category == 'profiles' else next(
                (entry[k] for k in ('schema_name', 'record_type', 'schema') if
                 isinstance(entry.get(k), str) and entry[k] in definitions), None)
            if name is None:
                untyped += 1
                continue
            validated += 1
            errors.extend(instance_errors(entry, definitions[name], definitions, location))
    require(not errors, errors[0] if errors else '')
    production_coherence(profiles, bundle, text)
    require(re.search(r'\| profiles pin \| `' + hashlib.sha256(path.read_bytes()).hexdigest() + r'`', text), 'missing/stale profiles pin')
    print('GREEN profiles: %d LaunchProfile entries, %d not_admitted entries schema-validated, %d not_admitted entries explicit refusals checked' %
          (len(profiles['profiles']), validated - len(profiles['profiles']), untyped))
    return 0


def freeze_hash_obligations(text, definitions):
    """Read normative record-reference pointers from F5, never the supplied manifest."""
    obligations = {}
    for line in section(text, 4).splitlines():
        if not line.startswith('| hash obligation |'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        names = re.findall(r'`([A-Za-z][A-Za-z0-9_]*)`', cells[1])
        paths = re.findall(r'`(/[^`]*)`', cells[2])
        require(names and paths, 'malformed freeze hash obligation')
        for name in names:
            require(name in definitions and name not in obligations, 'duplicate/unknown freeze hash obligation: ' + name)
            expanded = []
            for path in paths:
                if path.endswith('/*'):
                    prefix = path[:-2]
                    sizes = []
                    def bounds(schema, tokens):
                        if '$ref' in schema:
                            bounds(definitions[schema['$ref'][8:]], tokens)
                        if not tokens and schema.get('type') == 'array':
                            require(type(schema.get('maxItems')) is int, 'unbounded freeze hash array: ' + name + path)
                            sizes.append(schema['maxItems'])
                        if tokens and tokens[0] in schema.get('properties', {}):
                            bounds(schema['properties'][tokens[0]], tokens[1:])
                        for keyword in ('oneOf', 'anyOf', 'allOf'):
                            for branch in schema.get(keyword, []):
                                bounds(branch, tokens)
                    bounds(definitions[name], prefix[1:].split('/'))
                    require(sizes and len(set(sizes)) == 1, 'unresolved freeze hash array: ' + name + path)
                    expanded.extend(prefix + '/' + str(i) for i in range(sizes[0]))
                else:
                    expanded.append(path)
            obligations[name] = expanded
    require(obligations and '/policy_sha256' in obligations.get('CheckpointRecord', []),
            'freeze mandatory hash obligations missing')
    return obligations


def refusal_matches(refusal, entrypoint, argv):
    """DR D1 preserves variant-specific LATE_BOUND_ARGV refusals."""
    if refusal['entrypoint'] != entrypoint:
        return False
    variant = refusal.get('variant')
    if not variant:
        return True
    tokens = [] if variant == 'ordinary' else variant.replace(':', ' ').split()
    # Payloads name the script once, before its ordered CLI arguments.
    if entrypoint not in argv:
        return False
    return argv[argv.index(entrypoint) + 1:] == tokens


SCIENCE_ROLES = {'SCIENCE_PAYLOAD', 'SCIENCE_CHILD'}
GUARD_ARGV = ['science-guard', '--launch-id', {'$bind': 'launch_id'}, '--launch-profile', {'$bind': 'self_sha256'}]


def required_r1(profiles, bundle):
    for i, p in enumerate(profiles['profiles']):
        if p['scope'] != 'SCIENCE':
            continue
        require(p['invocation']['argv'] == GUARD_ARGV and p['invocation']['executable_path'].endswith('/bin/r2-m3')
                and p['invocation'] != p['authorized_payload'], 'R1 guard composition mismatch: profile %d' % i)
        declarations = profile_declarations(p, 'production/%d' % i)
        require(declarations.get('launch_id') == {'name': 'launch_id', 'source_record': 'ScienceLaunchContextRecord', 'source_field': '/launch_id'}
                and declarations.get('self_sha256') == {'name': 'self_sha256', 'source_record': 'SELF', 'source_field': ''},
                'R1 guard launch-context declarations missing: profile %d' % i)
    c = profiles.get('x-construction', {})
    require(c.get('status') == 'SYNTHETIC_BINDING_VECTORS_NOT_RUN_AUTHORITY', 'R1 production binding receipts missing')
    merged = copy.deepcopy(bundle)
    merged['x-construction']['examples'].update(c.get('examples', {}))
    for i, p in enumerate(profiles['profiles']):
        if p['scope'] != 'SCIENCE':
            continue
        name = 'ProductionLaunchProfile%03d' % i
        examples = c['examples']
        require(examples.get(name) == {'schema_name': 'LaunchProfile', 'instance': p}, 'R1 production receipt owning profile mismatch: ' + name)
        own = digest_json(p)
        receipts = [e['instance'] for e in examples.values() if e['schema_name'] == 'InvocationBinding' and e['instance']['profile_sha256'] == own]
        require({r['template_path'] for r in receipts} == {path for path, _ in invocation_templates(p)},
                'R1 production template receipt coverage mismatch: ' + name)
    invocation_coherence(merged)


def p2_stage(profile):
    return next((a for a in profile['authorized_payload']['argv'] if isinstance(a, str) and a.startswith('p2-')), None)


def required_r2(profiles, bundle):
    for i, profile in enumerate(profiles['profiles']):
        if Path(profile['entrypoint']).name == 'run_c10w_stage.sh' and p2_stage(profile):
            parent = profile.get('admission_parent') or {}
            require(profile.get('admission_scope') == 'CHILD_ONLY' and parent.get('entrypoint', '').endswith('/tools/run_c10w_p2_stage.sh'),
                    'R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile %d' % i)
    for i, p in enumerate(profiles['profiles']):
        base = Path(p['entrypoint']).name
        stage = p2_stage(p)
        if base == 'run_c10w_stage.sh' and stage:
            require(p.get('admission_scope') == 'CHILD_ONLY' and p.get('admission_parent', {}).get('entrypoint', '').endswith('/tools/run_c10w_p2_stage.sh'),
                    'R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile %d' % i)
        if base == 'c10w_oracle_step0.py' and stage:
            require(p.get('admission_scope') == 'CHILD_ONLY' and p.get('admission_parent', {}).get('entrypoint', '').endswith('/tools/run_c10w_stage.sh'),
                    'R2 P2 dispatcher must be CHILD_ONLY under inner stage: profile %d' % i)
        require(p.get('admission_scope') in ('TOP_LEVEL', 'CHILD_ONLY'), 'R2 admission scope missing: profile %d' % i)
        require((p['admission_scope'] == 'TOP_LEVEL') == (p.get('admission_parent') is None), 'R2 parent applicability mismatch: profile %d' % i)
        require(isinstance(p.get('admission_citation'), str) and re.search(r':\d+', p['admission_citation']), 'R2 admission evidence missing: profile %d' % i)
        if p['existing_admission'] and p['existing_admission']['executable_path'] == '/usr/bin/true':
            require(p['admission_scope'] == 'TOP_LEVEL' and p['admission_parent'] is None, 'R2 no-op child admission bypass: profile %d' % i)
            no_gate_sources = {
                'c10u_mint2_wordlist.py': 'science_launch_inventory_v4.md:153',
                'c10w_oracle_train.py': 'science_launch_inventory_v4.md:157',
                'c10w_oracle_eval.py': 'science_launch_inventory_v4.md:159',
                'c10w_oracle_step0.py': 'c10w_oracle_step0.py:436',
                'run_c10w_stage.sh': 'run_c10w_stage.sh:3',
                'c10w_p2_rerun.py': 'c10w_p2_rerun.py:295',
            }
            require(base in no_gate_sources and no_gate_sources[base] in p['admission_citation'], 'R2 unsupported no-op admission evidence: profile %d' % i)
        if base == 'run_c10w_p2_stage.sh':
            require(p['admission_scope'] == 'CHILD_ONLY' and p['admission_parent']['entrypoint'].endswith('/tools/run_c10w_p2.sh'), 'R2 P2 single-coordinator restriction missing')
            gate = p['existing_admission']
            require(gate and gate['argv'][1].endswith('/tools/c10w_p2_gate.py') and gate['argv'][2] == stage, 'R2 P2 gate mismatch')
        if p['admission_scope'] == 'CHILD_ONLY':
            parent = p['admission_parent']
            matches = [q for q in profiles['profiles'] if q['entrypoint'] == parent['entrypoint'] and q['authorized_payload']['argv'] == parent['payload_argv']]
            if matches:
                require(len(matches) == 1, 'R2 ambiguous parent recipe')
                require(any(ch['invocation'] == p['authorized_payload'] for ch in matches[0]['children']), 'R2 child absent from declared parent')
            else:
                require(any(refusal_matches(r, parent['entrypoint'], parent['payload_argv']) for r in profiles['not_admitted']), 'R2 missing unprofiled-parent refusal')


def required_r3(bundle):
    definitions = bundle['$defs']
    variants = definitions['ScienceChildProfile']['oneOf']
    require(len(variants)==2, 'R9 R1 helper/science recipe variants missing')
    child = variants[0]
    helper = variants[1]['properties']
    require(helper['role'].get('const')=='ADMISSION_HELPER' and helper['registration_authority'].get('const')=='C:115' and helper['enrollment'].get('const')=='PRE_RELEASE_REQUIRED', 'R9 R1 helper schema permits A1 authority')
    roles = child['properties']['role'].get('enum', [])
    require(set(roles) == SCIENCE_ROLES, 'R3 science child role permits non-science authority')
    require(child['properties']['enrollment'].get('const') == 'DECLARED_AT_ROOT_ADMISSION', 'R3 science registration exemption not restricted')
    require('AUTHORITY_WRITE' not in child['properties']['capability_kinds']['items'].get('enum', []), 'R3 science child permits AUTHORITY_WRITE')
    examples = bundle['x-construction']['examples']
    payload = copy.deepcopy(examples['Process']['instance'])
    payload['role'] = 'SCIENCE_PAYLOAD'
    payload.pop('sandbox_profile_sha256', None)
    payload['science_invocation_profile_sha256'] = digest_json(examples['LaunchProfileScience']['instance']['authorized_payload'])
    require(instance_valid(payload, definitions['Process'], definitions), 'R3 unsandboxed science Process cannot be represented')
    for role in definitions['Role']['enum']:
        if role in SCIENCE_ROLES:
            continue
        candidate = copy.deepcopy(payload)
        candidate['role'] = role
        require(not instance_valid(candidate, definitions['Process'], definitions), 'R3 non-science Process lost sandbox requirement: ' + role)
    for e in examples.values():
        if e['schema_name'] == 'Process' and e['instance']['role'] in SCIENCE_ROLES:
            proc = e['instance']
            require('sandbox_profile_sha256' not in proc and any(e2['schema_name'] == 'ScienceInvocationProfile' and digest_json(e2['instance']) == proc.get('science_invocation_profile_sha256') for e2 in examples.values()), 'R3 science Process profile reference unresolved')


def needs_replication(profile):
    base = Path(profile['entrypoint']).name
    argv = profile['authorized_payload']['argv']
    return base == 'c10w_oracle_train.py' or base == 'c10w_oracle_eval.py' and 'P3' in argv or base in ('c10w_oracle_step0.py', 'run_c10w_stage.sh') and any(isinstance(a, str) and a.startswith('p3-') for a in argv)


def required_r4(profiles, bundle):
    for i, p in enumerate(profiles['profiles']):
        if p['scope'] != 'SCIENCE':continue
        if needs_replication(p):
            candidates=[ch for ch in p['children'] if ch.get('origin')=='SCIENCE' and ch.get('trace_site')=='science-replication']
            require(len(candidates)==1, 'R4 P3 replication Git profile missing: profile %d operand family' % i)
            environment={e['name']:e['value'] for e in candidates[0]['invocation']['environment']}
            require(environment.get('HF_HUB_OFFLINE')=='1' and 'LLMDB_DEVICE' not in environment,'R4 replication environment mismatch')
            require({'name':'replication_adapter_family','source_record':'ScienceLaunchContextRecord','source_field':'/values/replication_adapter_family'} in p['bindings'],'R4 replication adapter binding missing')
        for ch in p['children']:
            if ch['role']=='ADMISSION_HELPER':
                require(ch['enrollment']=='PRE_RELEASE_REQUIRED' and ch['registration_authority']=='C:115','R9 R1 admission helper requires full pre-release registration')
            else:
                require(ch['enrollment']=='DECLARED_AT_ROOT_ADMISSION','R4 science child registration is not declared at root admission')


REQUIRED_CHECKS = {'R1': required_r1, 'R2': required_r2, 'R4': required_r4}


def production_coherence(profiles, bundle, text):
    round8_checks(profiles, bundle, text)
    round9_checks(profiles, bundle, text)
    round10_checks(profiles, bundle, text)
    required_r4(profiles, bundle)
    required_r1(profiles, bundle)
    required_r2(profiles, bundle)
    required_r3(bundle)
    merged = copy.deepcopy(bundle)
    merged['x-construction']['examples'].update(profiles['x-construction']['examples'])
    examples_valid(merged)
    bindings = invocation_coherence(merged)
    merged['x-construction']['hash_references'].extend(profiles['x-construction'].get('hash_references', []))
    coherent_examples(text, merged)
    for p in profiles['profiles']:
        for path, template in invocation_templates(p):
            require(len({e['name'] for e in template['environment']}) == len(template['environment']), 'duplicate production environment: ' + path)
            if path not in ('/invocation', '/broker_invocation'):
                require(hashlib.sha256(Path(template['executable_path']).read_bytes()).hexdigest() == template['executable_sha256'], 'production executable identity mismatch: ' + template['executable_path'])
                for dependency in template['dependencies']:
                    require(hashlib.sha256(Path(dependency['path']).read_bytes()).hexdigest() == dependency['sha256'], 'production dependency identity mismatch: ' + dependency['path'])
        for ch in p['children']:
            require(ch['role'] in set(SCIENCE_ROLES) | {'ADMISSION_HELPER'} and 'AUTHORITY_WRITE' not in ch['capability_kinds'], 'science child role/capability mismatch')
    denied = []
    for refusal in profiles['not_admitted']:
        require(all(isinstance(refusal.get(field), str) and refusal[field] for field in ('entrypoint', 'sha256', 'reason', 'citation', 'what_would_admit')), 'incomplete production refusal metadata')
        require(instance_valid(refusal['entrypoint'], bundle['$defs']['Path'], bundle['$defs']) and instance_valid(refusal['sha256'], bundle['$defs']['Hash'], bundle['$defs']), 'invalid production refusal identity')
        require(not refusal['reason'].startswith('RETIRED_NOT_ADMITTED:'), 'R5 unsound retirement rationale remains')
        if refusal['reason'].startswith('NOT_ADMITTED_NO_PROFILE:'):
            require('r2_round7_decisions.md' in refusal['citation'], 'R5 refusal lacks DR D1 citation')
        denied.append(refusal)
    for p in profiles['profiles']:
        for ch in p['children']:
            inv = ch['invocation']
            require(p.get('composition_refusal') or not any(refusal_matches(r, r['entrypoint'], inv['argv']) if r['entrypoint'] in inv['argv'] else refusal_matches(r, inv['executable_path'], inv['argv']) for r in denied), 'R5 parent declares refused launcher; parent not admitted')
    print('GREEN production coherence: R1-R4, D1 refusals, %d binding vectors rerendered; native behavior UNVERIFIED' % bindings)


# Round-8 checks are separate from the preserved round-7 controls.
A1_AUTHORITY = 'D-R2C-A1'
GAPS = {'SHORT_LIVED_CHILD', 'REPARENTED_ORPHAN', 'MISSED_EVENTS', 'OBSERVER_RESTART', 'UNEXPECTED_DESCENDANT'}
BROKER_ARGV = ['science-launch-broker', '--launch-id', {'$bind': 'launch_id'}, '--nonce', {'$bind': 'delegation_nonce'}, '--launch-profile', {'$bind': 'self_sha256'}]


def r8_examples(profiles, bundle):
    examples = dict(bundle['x-construction']['examples'])
    if profiles is not None:
        examples.update(profiles['x-construction']['examples'])
    return examples


def r8_r1(profiles, bundle, text):
    examples = r8_examples(profiles, bundle)
    enrollments = [e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceEnrollmentRecord']
    require(enrollments, 'R8 R1 science descendant declaration lacks A1 authority; D3 does not satisfy C:115')
    for r in enrollments:
        if r['kind'] == 'ROOT':
            require(r['registration_authority'] == 'C:115' and r['pre_release_registered'] is True and r['process'] is not None,
                    'R8 R1 root lacks full pre-release registration')
        elif r['kind'] == 'DESCENDANT':
            require(r['registration_authority'] == A1_AUTHORITY and r['enrollment'] == 'DECLARED_AT_ROOT_ADMISSION',
                    'R8 R1 science descendant authority must be A1, not C:115')
    gaps = [e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceObservationGapRecord']
    require({r['gap'] for r in gaps} == GAPS, 'R8 R1 observation gap coverage missing')
    for r in gaps:
        require(r['disposition'] == 'UNRESOLVED' and r['exclusion_retained'] is True and r['terminal_release'] is False,
                'R8 R1 observation gap must retain UNRESOLVED with no terminal release')
    for p in ([] if profiles is None else profiles['profiles']):
        for child in p['children']:
            require(child.get('registration_authority') == ('C:115' if child['role']=='ADMISSION_HELPER' else A1_AUTHORITY),
                    'R8 R1 science descendant authority must be A1, not C:115')
    for i, p in enumerate([] if profiles is None else profiles['profiles']):
        group = [e['instance'] for n, e in examples.items() if n.startswith('ProductionLaunchProfile%03d' % i) and e['schema_name'] == 'ScienceEnrollmentRecord']
        roots = [r for r in group if r['kind'] == 'ROOT']
        children = [r for r in group if r['kind'] in ('DESCENDANT','ADMISSION_HELPER')]
        bindings = [e['instance'] for n, e in examples.items() if n.startswith('ProductionLaunchProfile%03dBinding' % i) and e['schema_name'] == 'InvocationBinding']
        child_hashes = {digest_json(r) for r in bindings if r['template_path'].startswith('/children/')}
        root_hashes = {digest_json(r) for r in bindings if r['template_path'] == '/authorized_payload'}
        require(len(roots) == 1 and {r['recipe_binding_sha256'] for r in roots} == root_hashes,
                'R8 R1 missing or wrong root pre-release registration recipe')
        require(len(children) == len(p['children']) and {r['recipe_binding_sha256'] for r in children} == child_hashes,
                'R8 R1 incomplete descendant declaration')
    d8 = (HERE / 'r2_round8_decisions.md').read_text()
    amended = d8.split('**Amended text.**')[1].split('**Consequence for this round.**')[0]
    ruling = '**Operator ruling,' + d8.split('**Operator ruling,')[1].split('**Amended text.**')[0]
    require(' '.join(amended.split()) in ' '.join(text.split()) and ' '.join(ruling.split()) in ' '.join(text.split()),
            'R8 R1 freeze must quote approved amended text and operator ruling exactly')
    require('D-R2C-A1' in text and 'may already have executed' in text and 'NOTE_FORK' in text and 'Gate 2' in text,
            'R8 R1 amendment/observation/commissioning boundary missing')


def r8_r2(profiles, bundle, text):
    definitions = bundle['$defs']
    science = definitions['LaunchProfile']['oneOf'][0]
    require(science['properties']['invocation'] == {'$ref': '#/$defs/InvocationProfile'},
            'R8 R2 guard must use ordinary InvocationProfile with GUARD sandbox')
    examples = r8_examples(profiles, bundle)
    sandboxes = {digest_json(e['instance']): e['instance'] for e in examples.values() if e['schema_name'] == 'SandboxProfile'}
    owners = [e['instance'] for e in bundle['x-construction']['examples'].values() if e['schema_name'] == 'LaunchProfile' and e['instance']['scope'] == 'SCIENCE']
    if profiles is not None:
        owners += profiles['profiles']
    for p in owners:
        sandbox = sandboxes.get(p['invocation'].get('sandbox_profile_sha256'))
        require(sandbox and sandbox['role'] == 'GUARD' and sandbox['exec_paths'] == [] and sandbox['deny_fork_exec'] is True,
                'R8 R2 guard sandbox must deny fork/exec and have empty exec_paths')
        broker = p.get('broker_invocation')
        require(broker and broker.get('role') == 'SCIENCE_LAUNCH_BROKER' and broker.get('argv') == BROKER_ARGV,
                'R8 R2 delegation requires provisioned science launch broker')
        require(broker.get('capability_kinds') == ['SPAWN'] and 'sandbox_profile_sha256' not in broker,
                'R8 R2 broker cannot hold authority-write or bulk-write capability')
    delegations = [e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceDelegationRecord']
    require(delegations, 'R8 R2 delegation requires provisioned science launch broker')
    for r in delegations:
        require(r.get('broker') is not None and r['broker']['role'] == 'SCIENCE_LAUNCH_BROKER',
                'R8 R2 delegation requires provisioned science launch broker')
        require(r['broker_pre_release_registered'] and r['parent_without_guard_restrictions'] and r['authenticated'] and r['single_use'],
                'R8 R2 delegation authentication/bootstrap missing')
        require(r['sequence'] == ['SUSPENDED_ADMISSION', 'REGISTER_ADMISSION', 'RELEASE_ADMISSION', 'WAIT_SUCCESS', 'SUSPENDED_PAYLOAD', 'REGISTER_PAYLOAD', 'RELEASE_PAYLOAD'],
                'R8 R2 broker sequence must wait for successful admission')
        require(r['failed_admission'] == 'EXCLUSION_UNTIL_EXPLICIT_CANCELLATION' and r['missing_broker'] == 'REFUSE',
                'R8 R2 failure must refuse and preserve exclusion')


def r8_r3(profiles, bundle, text):
    if profiles is None:
        return
    ordered = sorted(enumerate(profiles['profiles']), key=lambda item: Path(item[1]['entrypoint']).name != 'c10w_oracle_eval.py' or 'P2' not in item[1]['authorized_payload']['argv'])
    for i, p in ordered:
        base = Path(p['entrypoint']).name
        payload = p['authorized_payload']['argv']
        restricted = base == 'c10w_oracle_train.py' or (base == 'c10w_oracle_eval.py' and 'P2' in payload)
        require(not restricted or (p['admission_scope'] == 'CHILD_ONLY' and p['existing_admission'] is None and
                p['admission_parent']['entrypoint'].endswith('/tools/run_c10w_p2.sh')),
                'R8 R3 direct P2 trainer/evaluator bypasses coordinator admission: profile %d' % i)
        if p['admission_scope'] == 'TOP_LEVEL' and p['existing_admission']['executable_path'] == '/usr/bin/true':
            audit = profiles['x-construction'].get('root_admission_audit', {}).get(str(i))
            require(audit and audit.get('caller_record') and audit['source_chain'] and audit['scope'] == 'ALL_REACHING_PRODUCTION_CHAINS',
                    'R8 R3 no-op admission lacks complete launch-chain audit: profile %d' % i)
            for citation in audit['source_chain']:
                path, line = citation.rsplit(':', 1)
                source = ROOT / path
                require(source.is_file() and 0 < int(line) <= len(source.read_text().splitlines()),
                        'R8 R3 source chain citation unresolved: ' + citation)


def r8_admission_receipt(p, examples, bundle):
    own = digest_json(p)
    bindings = [e['instance'] for e in examples.values() if e['schema_name'] == 'InvocationBinding' and e['instance']['profile_sha256'] == own]
    require({r['template_path'] for r in bindings} == {path for path, _ in invocation_templates(p)} and len(bindings) == len(list(invocation_templates(p))),
            'R8 R4 admission aggregate must include every unique InvocationBinding')
    receipt = copy.deepcopy(bundle['x-construction']['examples']['ActionReceipt']['instance'])
    receipt['operation'] = 'REGISTER_SCIENCE_ROOT_ADMISSION'
    receipt['input_receipts'] = [own] + [digest_json(r) for r in bindings]
    require(instance_valid(receipt, bundle['$defs']['ActionReceipt'], bundle['$defs']),
            'R8 R4 root admission receipt exceeds frozen input_receipts bound: needs %d' % len(receipt['input_receipts']))
    require(len(canonical(receipt).encode('utf-8')) <= 262144, 'R8 R4 admission receipt exceeds 262144-byte file bound')
    blob = {'sha256': digest_json(receipt), 'canonical_utf8': canonical(receipt)}
    require(instance_valid(blob, bundle['$defs']['ReceiptBlob'], bundle['$defs']) and len(blob['canonical_utf8'].encode('utf-8')) <= 8192,
            'R8 R4 admission ReceiptBlob exceeds 8192 UTF-8 bytes')
    return receipt


def r8_r4(profiles, bundle, text):
    if profiles is None:
        require(bundle['$defs']['ActionReceipt']['properties']['input_receipts']['maxItems'] == 64,
                'R8 R4 root admission input_receipts bound must be 64')
        return
    examples = r8_examples(profiles, bundle)
    sizes = []
    all_sizes = []
    for i, p in enumerate(profiles['profiles']):
        group = {n: e for n, e in examples.items() if n.startswith('ProductionLaunchProfile%03d' % i)}
        # CHILD_ONLY recipes are also built: turning a route off cannot hide an overflow.
        receipt = r8_admission_receipt(p, group, bundle)
        all_sizes.append((len(receipt['input_receipts']), len(canonical(receipt).encode('utf-8'))))
        if p['admission_scope'] == 'TOP_LEVEL':
            sizes.append((len(receipt['input_receipts']), len(canonical(receipt).encode('utf-8'))))
    require(bundle['$defs']['ActionReceipt']['properties']['input_receipts']['maxItems'] == 64,
            'R8 R4 root admission input_receipts bound must be 64')
    require(sizes, 'R8 R4 no production TOP_LEVEL admission aggregate constructed')
    print('GREEN admission aggregates: %d TOP_LEVEL, %d total; max TOP_LEVEL %d input receipts, %d UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file' %
          (len(sizes), len(profiles['profiles']), max(v[0] for v in sizes), max(v[1] for v in sizes)))

    print('GREEN all aggregate maxima: %d input receipts / %d UTF-8 bytes; frozen bounds 64 / 8192 / 262144' % (max(v[0] for v in all_sizes),max(v[1] for v in all_sizes)))


def operand_matches(kind, value):
    if not isinstance(value, str):
        return False
    return {'PID': bool(re.fullmatch(r'[1-9][0-9]*', value)), 'PATH': value.startswith('/'),
            'DIRECTORY': value.startswith('/'), 'HASH': bool(re.fullmatch(r'[0-9a-f]{64}', value)),
            'TOKEN': bool(value) and not value.startswith('--')}[kind]


def structured_refusal_matches(refusal, entrypoint, argv):
    if refusal['entrypoint'] != entrypoint:
        return False
    variant = refusal.get('variant')
    if variant is None:
        return True
    if not isinstance(variant, dict) or entrypoint not in argv:
        return False
    suffix = argv[argv.index(entrypoint) + 1:]
    tokens = variant['tokens']
    slots = variant['required_operands']
    if len(suffix) != len(tokens) + len(slots) or suffix[:len(tokens)] != tokens:
        return False
    return all(operand_matches(slot['kind'], value) for slot, value in zip(slots, suffix[len(tokens):]))


SOURCE_REFUSAL_CASES = [
    ('tools/run_c10w_p2.sh', 'ordinary', ['123', '/source-valid/predecessor.log'], 'tools/run_c10w_p2.sh:9', '<predecessor pid> <predecessor log>'),
    ('tools/run_c10w_p2.sh', '--reattempt-eval', ['--reattempt-eval', str(ROOT / 'results/c10w_oracle/p2_20261008T034226_086980Z')], 'tools/run_c10w_p2.sh:17', 'belongs to another P2 directory'),
    ('tools/run_c10w_p2_stage.sh', 'p2-eval --reattempt', ['p2-eval', '--reattempt', str(ROOT / 'results/c10w_oracle/p2_20261008T034226_086980Z')], 'tools/run_c10w_p2_stage.sh:12', 'p2-eval --reattempt <P2 directory>'),
]


def r8_r5(profiles, bundle, text):
    if profiles is None:
        return
    for relative, name, args, citation, source_text in SOURCE_REFUSAL_CASES:
        source, line = citation.rsplit(':', 1)
        require(source_text in (ROOT / source).read_text().splitlines()[int(line)-1], 'R8 R5 source-valid control citation drift: ' + citation)
        entry = str(ROOT / relative)
        refusal = next((r for r in profiles['not_admitted'] if r['entrypoint'] == entry and (r.get('variant', {}).get('name') if isinstance(r.get('variant'), dict) else r.get('variant')) == name), None)
        require(refusal and refusal_matches(refusal, entry, [entry] + args),
                'R8 R5 refusal misses source-valid required operands: ' + name)
        require(not refusal_matches(refusal, entry, [entry] + args[:-1]), 'R8 R5 refusal accepts invalid arity: ' + name)
    for r in profiles['not_admitted']:
        if 'variant' in r:
            require(instance_valid(r['variant'], bundle['$defs'].get('RefusalVariant', {}), bundle['$defs']),
                    'R8 R5 malformed structured refusal variant')
    for p in profiles['profiles']:
        parent = p.get('admission_parent')
        if parent and parent['entrypoint'].endswith('/tools/run_c10w_p2.sh'):
            argv = parent['payload_argv']
            require(len(argv) == 3 and (argv[1] == '--reattempt-eval' and operand_matches('DIRECTORY', argv[2]) or
                    operand_matches('PID', argv[1]) and operand_matches('PATH', argv[2])),
                    'R8 R5 impossible coordinator parent argv: required operands missing')
    # Propagation exercises actual source-valid argv at the real production checker boundary.
    for relative, name, args, _, _ in SOURCE_REFUSAL_CASES:
        entry = str(ROOT / relative)
        try:
            refused_descendants([{'invocation': {'executable_path': '/bin/bash', 'argv': [entry] + args}}], profiles['not_admitted'])
        except ValueError as error:
            require('R5 parent declares refused launcher' in str(error), 'R8 R5 wrong propagation failure')
        else:
            raise ValueError('R8 R5 source-valid descendant refusal failed to propagate: ' + name)


def refused_descendants(children, denied):
    for ch in children:
        inv = ch['invocation']
        require(not any(refusal_matches(r, r['entrypoint'], inv['argv']) if r['entrypoint'] in inv['argv'] else refusal_matches(r, inv['executable_path'], inv['argv']) for r in denied),
                'R5 parent declares refused launcher; parent not admitted')


def r8_r6(profiles, bundle, text):
    examples = r8_examples(profiles, bundle)
    contexts = {digest_json(e['instance']): e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceLaunchContextRecord'}
    owners = [bundle['x-construction']['examples']['LaunchProfileScience']['instance']] if profiles is None else profiles['profiles']
    for i, p in enumerate(owners):
        examples = bundle['x-construction']['examples'] if profiles is None else {n: e for n, e in profiles['x-construction']['examples'].items() if n.startswith('ProductionLaunchProfile%03d' % i)}
        own = digest_json(p)
        bindings = [e['instance'] for e in examples.values() if e['schema_name'] == 'InvocationBinding' and e['instance']['profile_sha256'] == own]
        hashes = {r.get('launch_context_sha256') for r in bindings}
        require(len(hashes) == 1 and None not in hashes, 'R8 R6 production bindings lack one authenticated launch context')
        context_hash = next(iter(hashes))
        context = contexts.get(context_hash)
        require(context and context['launch_profile_sha256'] == own and context.get('context_mac'), 'R8 R6 launch context identity unresolved')
        for r in bindings:
            require(all(v['source_record_sha256'] == context_hash for v in r['bound_values'] if v['source_record'] == 'ScienceLaunchContextRecord'),
                    'R8 R6 cross-context substitution in production tree')
        records = [e['instance'] for e in examples.values() if e['schema_name'] in ('ScienceEnrollmentRecord', 'ScienceDelegationRecord') and e['instance']['launch_profile_sha256'] == own]
        require(records and all(r['launch_context_sha256'] == context_hash for r in records), 'R8 R6 delegation/enrollment cross-context identity')
        delegation = next(r for r in records if r['record_type'] == 'ScienceDelegationRecord')
        require(delegation['delegation_nonce'] == context['values']['delegation_nonce'] and delegation['broker']['host_id'] == context['host_id'] and delegation['broker']['boot_id'] == context['boot_id'],
                'R8 R6 broker delegation launch/nonce/host/boot mismatch')


refusal_matches = structured_refusal_matches

ROUND8_CHECKS = {'R1': r8_r1, 'R2': r8_r2, 'R3': r8_r3, 'R4': r8_r4, 'R5': r8_r5, 'R6': r8_r6}


def round8_checks(profiles, bundle, text):
    for fn in ROUND8_CHECKS.values():
        fn(profiles, bundle, text)
    print('GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED')


R8_CONTROL_MESSAGES = {
    'R8R1A': 'R8 R1 science descendant authority must be A1, not C:115',
    'R8R1B': 'R8 R1 root lacks full pre-release registration',
    'R8R1C': 'R8 R1 observation gap must retain UNRESOLVED with no terminal release',
    'R8R2A': 'R8 R2 guard sandbox must deny fork/exec and have empty exec_paths',
    'R8R2D': 'R8 R2 guard sandbox must deny fork/exec and have empty exec_paths',
    'R8R2B': 'R8 R2 delegation requires provisioned science launch broker',
    'R8R2C': 'R8 R2 broker cannot hold authority-write or bulk-write capability',
    'R8R3': 'R8 R3 direct P2 trainer/evaluator bypasses coordinator admission',
    'R8R4': 'R8 R4 root admission receipt exceeds frozen input_receipts bound: needs 65',
    'R8R5': 'R8 R5 refusal misses source-valid required operands: ordinary',
    'R8R6': 'R8 R6 cross-context substitution in production tree',
}


def r8_damaged(control, profiles, bundle):
    examples = profiles['x-construction']['examples']
    all_examples = r8_examples(profiles, bundle)
    if control == 'R8R1A':
        r = next(e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceEnrollmentRecord' and e['instance']['kind'] == 'DESCENDANT')
        r['registration_authority'] = 'C:115'
    elif control == 'R8R1B':
        r = next(e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceEnrollmentRecord' and e['instance']['kind'] == 'ROOT')
        r['pre_release_registered'] = False
    elif control == 'R8R1C':
        r = next(e['instance'] for e in bundle['x-construction']['examples'].values() if e['schema_name'] == 'ScienceObservationGapRecord')
        r['disposition'] = 'CLEARED'
    elif control in ('R8R2A', 'R8R2D'):
        r = bundle['x-construction']['examples']['SandboxProfileGuard']['instance']
        prior = digest_json(r)
        if control == 'R8R2A':
            r['exec_paths'] = ['/bin/bash']
        else:
            r['deny_fork_exec'] = False
        # Change only one assertion; the separate deny_fork_exec=false control also runs below.
        changed = digest_json(r)
        for e in all_examples.values():
            if e['schema_name'] == 'LaunchProfile' and e['instance']['scope'] == 'SCIENCE':
                require(e['instance']['invocation']['sandbox_profile_sha256'] == prior, 'R8R2A positive guard identity drift')
                e['instance']['invocation']['sandbox_profile_sha256'] = changed
        for p in profiles['profiles']:
            p['invocation']['sandbox_profile_sha256'] = changed
    elif control == 'R8R2B':
        r = next(e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceDelegationRecord')
        r['broker'] = None
    elif control == 'R8R2C':
        profiles['profiles'][0]['broker_invocation']['capability_kinds'].append('AUTHORITY_WRITE')
    elif control == 'R8R3':
        q = next(p for p in profiles['profiles'] if Path(p['entrypoint']).name == 'c10w_oracle_eval.py' and 'P2' in p['authorized_payload']['argv'])
        q['admission_scope'] = 'TOP_LEVEL'
        q['admission_parent'] = None
        q['existing_admission'] = copy.deepcopy(profiles['profiles'][0]['existing_admission'])
    elif control == 'R8R4':
        # A real 64-binding tree needs 65 input hashes with its owning profile.
        q = profiles['profiles'][0]
        q['children'] = [{'role': 'SCIENCE_CHILD', 'origin': 'SCIENCE', 'trace_site': 'MUTATION_RECEIPT_BOUND', 'invocation': copy.deepcopy(q['existing_admission']), 'enrollment': 'DECLARED_AT_ROOT_ADMISSION', 'registration_authority': A1_AUTHORITY, 'capability_kinds': []} for _ in range(60)]
        require(instance_valid(q, bundle['$defs']['LaunchProfile'], bundle['$defs']), 'R8R4 owner must remain schema-valid')
        own = digest_json(q)
        examples['ProductionLaunchProfile000']['instance'] = q
        ctx = examples['ProductionLaunchProfile000Context']['instance']
        ctx['launch_profile_sha256'] = own
        group = {}
        for i, (path, template) in enumerate(invocation_templates(q)):
            record = copy.deepcopy(examples['ProductionLaunchProfile000Binding000']['instance'])
            record['binding_id'] = hashlib.sha256(('65 control %d' % i).encode()).hexdigest()[:32]
            record['profile_sha256'], record['template_path'] = own, path
            group['Binding%03d' % i] = {'schema_name': 'InvocationBinding', 'instance': record}
        require(len(group) == 64, 'R8R4 must construct exactly 64 bindings')
        return group, q
    elif control == 'R8R5':
        r = next(r for r in profiles['not_admitted'] if r['entrypoint'].endswith('/tools/run_c10w_p2.sh') and r.get('variant', {}).get('name') == 'ordinary')
        r['variant']['required_operands'].pop()
    elif control == 'R8R6':
        original = examples['ProductionLaunchProfile001Context']['instance']
        other = copy.deepcopy(original)
        other['context_id'] = hashlib.sha256(b'round8 second context').hexdigest()[:32]
        other['launch_id'] = hashlib.sha256(b'round8 second launch').hexdigest()[:32]
        other['values']['phase_directory'] += '/second-launch'
        other['context_mac'] = hashlib.sha256(canonical({k: v for k, v in other.items() if k != 'context_mac'}).encode()).hexdigest()
        require(instance_valid(other, bundle['$defs']['ScienceLaunchContextRecord'], bundle['$defs']), 'R8R6 second context must be schema-valid')
        require(other['launch_id'] != original['launch_id'] and other['values']['phase_directory'] != original['values']['phase_directory'], 'R8R6 second launch must differ in ID/directory')
        examples['ProductionLaunchProfile001OtherContext'] = {'schema_name': 'ScienceLaunchContextRecord', 'instance': other}
        binding = next(e['instance'] for n, e in examples.items() if n.startswith('ProductionLaunchProfile001Binding') and e['instance']['template_path'] == '/authorized_payload')
        field = next(v for v in binding['bound_values'] if v['name'] == 'phase_directory')
        old_value = field['value']
        field['source_record_sha256'] = digest_json(other)
        field['value'] = other['values']['phase_directory']
        binding['rendered_argv'] = [field['value'] if a == old_value else a for a in binding['rendered_argv']]
        binding['rendered_argv_sha256'] = digest_json(binding['rendered_argv'])
        examples['ProductionLaunchProfile001RootEnrollment']['instance']['recipe_binding_sha256'] = digest_json(binding)
        examples['ProductionLaunchProfile001Delegation']['instance']['payload_binding_sha256'] = digest_json(binding)
        # Guard/context stamp intentionally unchanged. Every pre-R8 local check must pass.
        require(instance_valid(binding, bundle['$defs']['InvocationBinding'], bundle['$defs']), 'R8R6 payload binding must remain schema-valid')
        merged = copy.deepcopy(bundle)
        merged['x-construction']['examples'].update(examples)
        examples_valid(merged)
        invocation_coherence(merged)
    else:
        raise ValueError('unknown round8 control: ' + control)
    return None


LEGACY_CONTROL_MESSAGES = dict(CONTROL_MESSAGES)
legacy_mutation_controls = mutation_controls


def round8_mutation_controls(freeze, schemas, controls=None):
    old = [c for c in (controls or LEGACY_CONTROL_MESSAGES) if c in LEGACY_CONTROL_MESSAGES]
    if old:
        # Preserve the exact 26 old controls and their expected error substrings.
        legacy_mutation_controls(freeze, schemas, old)
    selected = [c for c in (controls or R8_CONTROL_MESSAGES) if c in R8_CONTROL_MESSAGES]
    failures = []
    for control in selected:
        bundle = read_json(schemas)
        profiles = read_json(PROFILES)
        special = r8_damaged(control, profiles, bundle)
        profile_path = MemoryPath(json.dumps(profiles, indent=2, ensure_ascii=False) + '\n')
        text = re.sub(r'(\| profiles pin \| `)[0-9a-f]{64}(`)', lambda m: m[1] + hashlib.sha256(profile_path.read_bytes()).hexdigest() + m[2], freeze.read_text())
        copy_f, copy_j = sealed_memory(text, MemoryPath(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n'))
        try:
            if control == 'R8R4':
                group, owner = special
                r8_admission_receipt(owner, group, bundle)
            elif control == 'R8R6':
                # Execute the repinned packet: default and all local reconstruction checks have passed.
                validate_profiles(profile_path, bundle, copy_f.read_text())
            else:
                ROUND8_CHECKS['R' + control[3]](profiles, bundle, copy_f.read_text())
        except ValueError as error:
            actual = str(error)
            if R8_CONTROL_MESSAGES[control] in actual:
                print('RED %s: exit 1: %s' % (control, actual))
            else:
                failures.append(control)
                print('WRONG RED %s: expected %r; got %s' % (control, R8_CONTROL_MESSAGES[control], actual))
        else:
            failures.append(control)
            print('UNEXPECTED GREEN ' + control)
    require(not failures, 'round8 mutation control expectations unmet: ' + ','.join(failures))
    print('GREEN mutation controls: %d intended RED (%d old + %d round8), zero filesystem writes' % (len(old) + len(selected), len(old), len(selected)))


CONTROL_MESSAGES.update(R8_CONTROL_MESSAGES)
mutation_controls = round8_mutation_controls


# Round 9: D10-D12; sources are read only; mutations never touch the filesystem.
ADMISSION_REASON = 'NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED:'

def r9_r1(profiles, bundle, text):
    definitions=bundle['$defs']
    helper_process=[v for v in definitions['Process']['oneOf'] if v['properties']['role'].get('const')=='ADMISSION_HELPER']
    require('ADMISSION_HELPER' in definitions['Role']['enum'] and len(helper_process)==1, 'R9 R1 ADMISSION_HELPER Process role missing')
    props=helper_process[0]['properties']
    require(props['registration_authority'].get('const')=='C:115' and props['pre_release_registered'].get('const') is True and props.get('sandbox_profile_sha256',{}).get('$ref')=='#/$defs/Hash', 'R9 R1 helper Process must retain C:115 pre-release registration and sandbox')
    examples = r8_examples(profiles, bundle)
    owners = [e['instance'] for e in examples.values() if e['schema_name'] == 'LaunchProfile' and e['instance']['scope'] == 'SCIENCE']
    if profiles is not None: owners += profiles['profiles']
    owners.sort(key=lambda p: not any(any(isinstance(v,str) and v.endswith('/c10w_p2_gate.py') for v in c['invocation']['argv']) for c in p['children']))
    for p in owners:
        gate_present = any(any(isinstance(v,str) and v.endswith('/c10w_p2_gate.py') for v in c['invocation']['argv']) for c in p['children'])
        helpers = [ch for ch in p['children'] if ch['role']=='ADMISSION_HELPER' or (gate_present and ch.get('origin')=='ADMISSION')]
        for ch in helpers:
            require(ch.get('role') == 'ADMISSION_HELPER' and ch.get('registration_authority') == 'C:115' and ch.get('enrollment') == 'PRE_RELEASE_REQUIRED',
                    'R9 R1 admission/helper carries A1 authority or science role: ' + p['entrypoint'])
        gate = p.get('existing_admission') or {}
        affected = helpers or (gate and gate['executable_path'] != '/usr/bin/true')
        if affected:
            require(p.get('composition_refusal', '').startswith(ADMISSION_REASON),
                    'R9 R1 admission-spawned helper composition not refused: ' + p['entrypoint'])
        require(not gate or ('registration_authority' not in gate and 'enrollment' not in gate),
                'R9 R1 admission carries A1 authority')
    def walk(v):
        if isinstance(v, dict):
            if v.get('role') == 'ADMISSION_HELPER' or v.get('kind') == 'ADMISSION_HELPER':
                require(v.get('registration_authority') == 'C:115' and v.get('enrollment') != 'DECLARED_AT_ROOT_ADMISSION',
                        'R9 R1 admission/helper carries A1 authority or science role')
            for child in v.values(): walk(child)
        elif isinstance(v, list):
            for child in v: walk(child)
    walk(examples)
    if profiles is not None:
        audit = profiles['x-construction'].get('admission_source_audit', {})
        gate = 'tools/c10w_p2_gate.py'
        require(gate in audit and audit[gate]['spawn_lines'] == [63, 69, 75, 79], 'R9 R1 admission source spawn audit missing')
        src = (ROOT / gate).read_text().splitlines()
        require(all(term in src[line-1] for line, term in [(63,'subprocess.run'),(69,'engine_fingerprint.py'),(75,'/bin/ps'),(79,'/usr/bin/env')]), 'R9 R1 admission spawn citation changed')
        require(audit[gate]['sha256'] == hashlib.sha256((ROOT/gate).read_bytes()).hexdigest(), 'R9 R1 admission source pin changed')
        for p in profiles['profiles']:
            if p.get('composition_refusal'):
                require(any(r['entrypoint'] == p['entrypoint'] and r.get('payload_argv') == p['authorized_payload']['argv'] and r['reason'] == p['composition_refusal'] for r in profiles['not_admitted']), 'R9 R1 composition refusal record missing')


def caller_search(entrypoint):
    # Literal basename search intentionally includes non-call hits for explicit classification.
    return ['/usr/bin/grep', '-R', '-n', '-F', '--include=*.py', '--include=*.sh', '--', Path(entrypoint).name, 'experiments', 'tools', 'mathlab', 'architecture_profile', 'visualization', '.claude', '.codex']


def caller_hits(command):
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    require(run.returncode in (0, 1) and not run.stderr, 'R9 R2 caller grep failed: ' + run.stderr)
    return sorted(run.stdout.splitlines())


def r9_r2(profiles, bundle, text):
    if profiles is None: return
    ordered=sorted(enumerate(profiles['profiles']), key=lambda item: not (Path(item[1]['entrypoint']).name=='c10w_oracle_eval.py' and any(v in item[1]['authorized_payload']['argv'] for v in ('P1','P3'))))
    for i, p in ordered:
        if Path(p['entrypoint']).name == 'c10w_oracle_eval.py' and any(v in p['authorized_payload']['argv'] for v in ('P1','P3')):
            require(p['admission_scope'] == 'CHILD_ONLY' and p['existing_admission'] is None and p['admission_parent']['entrypoint'].endswith('/experiments/track_c/c10w_oracle_step0.py'),
                    'R9 R2 direct P1/P3 evaluator bypasses dispatcher projection: profile %d' % i)
        if p['admission_scope'] != 'TOP_LEVEL' or p['existing_admission']['executable_path'] != '/usr/bin/true': continue
        audit = profiles['x-construction'].get('root_admission_audit', {}).get(str(i), {})
        record = audit.get('caller_record', {})
        command = caller_search(p['entrypoint'])
        require(record.get('grep_argv') == command and record.get('grep_command') == ' '.join(shlex.quote(v) for v in command), 'R9 R2 no-op lacks exact caller grep: profile %d' % i)
        require(record.get('hits') == caller_hits(command), 'R9 R2 caller hit set differs: profile %d' % i)
        require('outer_obligations' not in audit and len(record.get('classifications', [])) == len(record['hits']), 'R9 R2 unsupported empty-obligation claim or incomplete caller classification')
        for hit, item in zip(record['hits'], record['classifications']):
            require(item.get('hit') == hit and item.get('kind') in ('CALLER','NON_CALL') and item.get('explanation'), 'R9 R2 missing caller classification')
            require(item.get('checks') is not None and item.get('direct_route_preserves_all') is True, 'R9 R2 caller obligation skipped by direct no-op')
            if item['kind'] == 'CALLER': require(item['checks'], 'R9 R2 caller checks require cited record')
            for check in item['checks']:
                require(check.get('explanation') and check.get('citations'), 'R9 R2 missing caller check citations')
                for citation in check['citations']:
                    path, line = citation.rsplit(':',1)
                    require(0 < int(line) <= len((ROOT/path).read_text().splitlines()), 'R9 R2 caller check citation unresolved')
        pins = record.get('source_pins', {})
        require(set(pins) == {h.split(':',1)[0] for h in record['hits']}, 'R9 R2 caller source pins incomplete')
        for path, digest in pins.items(): require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, 'R9 R2 caller source pin changed: ' + path)


def r9_r3(profiles, bundle, text):
    examples = r8_examples(profiles, bundle)
    bindings = {}
    for name, e in examples.items():
        if e['schema_name'] == 'InvocationBinding': bindings.setdefault(digest_json(e['instance']), []).append((name,e['instance']))
    owners = {digest_json(e['instance']): e['instance'] for e in examples.values() if e['schema_name'] == 'LaunchProfile'}
    contexts = {digest_json(e['instance']): e['instance'] for e in examples.values() if e['schema_name'] == 'ScienceLaunchContextRecord'}
    production_owners = {} if profiles is None else {digest_json(e['instance']): n for n,e in profiles['x-construction']['examples'].items() if e['schema_name']=='LaunchProfile'}
    def resolve(r, field, template):
        value = r[field]
        owner = owners.get(r['launch_profile_sha256'])
        require(owner is not None, 'R9 R3 delegation reference owning profile unresolved')
        if value is None:
            require(template == '/existing_admission' and owner['existing_admission'] is None, 'R9 R3 delegation reference illegally null')
            return None
        matches = bindings.get(value, [])
        require(len(matches) == 1, 'R9 R3 delegation reference does not resolve uniquely: ' + field)
        name, binding = matches[0]
        require(binding['profile_type'] == 'LaunchProfile' and binding['profile_sha256'] == r['launch_profile_sha256'] and binding.get('launch_context_sha256') == r['launch_context_sha256'] and binding['template_path'] == template,
                'R9 R3 delegation reference foreign profile/context/template: ' + field)
        if profiles is not None:
            own_name = production_owners.get(r['launch_profile_sha256'])
            if own_name is not None:
                require(name.startswith(own_name+'Binding'), 'R9 R3 delegation reference foreign profile tree: ' + field)
            else:
                require(name in bundle['x-construction']['examples'], 'R9 R3 delegation reference foreign fixture tree: ' + field)
        return binding
    def process_identity(process, binding, owner, context):
        if process is None: return
        require(binding is not None and context is not None, 'R9 R3 process binding/context unresolved')
        template = dict(invocation_templates(owner))[binding['template_path']]
        key = 'broker_invocation_profile_sha256' if process['role']=='SCIENCE_LAUNCH_BROKER' else 'science_invocation_profile_sha256'
        require(process['executable_sha256'] == template['executable_sha256'] and process['argv_sha256'] == binding['rendered_argv_sha256'] and process.get(key) == digest_json(template) and process['host_id']==context['host_id'] and process['boot_id']==context['boot_id'], 'R9 R3 process identity disagrees with invocation binding')
    for name,e in examples.items():
        r=e['instance']
        if e['schema_name'] not in ('ScienceDelegationRecord','ScienceEnrollmentRecord'): continue
        owner=owners.get(r['launch_profile_sha256']); context=contexts.get(r['launch_context_sha256'])
        require(owner and context and context['launch_profile_sha256']==r['launch_profile_sha256'], 'R9 R3 delegation reference owning context unresolved')
        if e['schema_name']=='ScienceDelegationRecord':
            fields=[k for k in r if k.endswith('_binding_sha256')]
            require(set(fields) == {'admission_binding_sha256','payload_binding_sha256'}, 'R9 R3 delegation reference has unmapped binding field')
            for field in fields: resolve(r,field,{'admission_binding_sha256':'/existing_admission','payload_binding_sha256':'/authorized_payload'}[field])
            matches=[b for rows in bindings.values() for _,b in rows if b['profile_sha256']==r['launch_profile_sha256'] and b['template_path']=='/broker_invocation' and b.get('launch_context_sha256')==r['launch_context_sha256']]
            require(len(matches)==1,'R9 R3 broker binding ambiguous')
            process_identity(r['broker'],matches[0],owner,context)
        else:
            rows=bindings.get(r['recipe_binding_sha256'],[])
            require(len(rows)==1,'R9 R3 enrollment binding unresolved')
            binding=rows[0][1]
            require(binding['profile_sha256']==r['launch_profile_sha256'] and binding.get('launch_context_sha256')==r['launch_context_sha256'], 'R9 R3 enrollment binding foreign launch')
            require((binding['template_path']=='/authorized_payload') if r['kind']=='ROOT' else binding['template_path'].startswith('/children/'), 'R9 R3 enrollment template mismatch')
            process_identity(r.get('process',r.get('observed_process')),binding,owner,context)


ROUND9_CHECKS = {'R1': r9_r1, 'R2': r9_r2, 'R3': r9_r3}

def round9_checks(profiles, bundle, text):
    for fn in ROUND9_CHECKS.values(): fn(profiles,bundle,text)
    print('GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities')


def foreign_delegation(profiles, field):
    examples=profiles['x-construction']['examples']
    foreign=examples['ProductionLaunchProfile003Delegation']['instance']
    examples['ProductionLaunchProfile000Delegation']['instance'][field]=foreign[field] if foreign[field] is not None else foreign['payload_binding_sha256']


R9_CONTROL_MESSAGES = {
    'R9R1A': 'R9 R1 admission/helper carries A1 authority or science role',
    'R9R1B': 'R9 R1 admission/helper carries A1 authority or science role',
    'R9R1C': 'R9 R1 admission-spawned helper composition not refused',
    'R9R2A': 'R9 R2 direct P1/P3 evaluator bypasses dispatcher projection',
    'R9R2B': 'R9 R2 direct P1/P3 evaluator bypasses dispatcher projection',
    'R9R2C': 'R9 R2 caller hit set differs',
    'R9R3A': 'R9 R3 delegation reference foreign profile/context/template: payload_binding_sha256',
    'R9R3B': 'R9 R3 delegation reference foreign profile/context/template: admission_binding_sha256',
    'R9R3C': 'R9 R3 process identity disagrees with invocation binding',
}

round8_controls = mutation_controls

def round9_mutation_controls(freeze, schemas, controls=None):
    old=[c for c in (controls or CONTROL_MESSAGES) if c not in R9_CONTROL_MESSAGES]
    if old: round8_controls(freeze,schemas,old)
    selected=[c for c in (controls or R9_CONTROL_MESSAGES) if c in R9_CONTROL_MESSAGES]
    for control in selected:
        profiles=read_json(PROFILES);bundle=read_json(schemas);examples=profiles['x-construction']['examples']
        if control in ('R9R1A','R9R1B'):
            p=next(p for p in profiles['profiles'] if any(ch['role']=='ADMISSION_HELPER' for ch in p['children']))
            ch=next(ch for ch in p['children'] if ch['role']=='ADMISSION_HELPER')
            if control=='R9R1A': ch['registration_authority']=A1_AUTHORITY;ch['enrollment']='DECLARED_AT_ROOT_ADMISSION'
            else: ch['role']='SCIENCE_CHILD';ch['registration_authority']=A1_AUTHORITY;ch['enrollment']='DECLARED_AT_ROOT_ADMISSION'
        elif control=='R9R1C':
            p=next(p for p in profiles['profiles'] if (p.get('composition_refusal') or '').startswith(ADMISSION_REASON));p.pop('composition_refusal')
        elif control in ('R9R2A','R9R2B'):
            phase='P1' if control=='R9R2A' else 'P3'
            p=next(p for p in profiles['profiles'] if Path(p['entrypoint']).name=='c10w_oracle_eval.py' and phase in p['authorized_payload']['argv'])
            p.update(admission_scope='TOP_LEVEL',admission_parent=None,existing_admission=copy.deepcopy(profiles['profiles'][0]['existing_admission']))
        elif control=='R9R2C':
            audit=next(a for a in profiles['x-construction']['root_admission_audit'].values() if a.get('caller_record',{}).get('hits'))
            audit['caller_record']['hits'].pop()
        elif control in ('R9R3A','R9R3B'): foreign_delegation(profiles,'payload_binding_sha256' if control=='R9R3A' else 'admission_binding_sha256')
        else: examples['ProductionLaunchProfile000RootEnrollment']['instance']['process']['argv_sha256']=hashlib.sha256(b'wrong-process-argv').hexdigest()
        path=MemoryPath(json.dumps(profiles,indent=2,ensure_ascii=False)+'\n')
        text=re.sub(r'(\| profiles pin \| `)[0-9a-f]{64}(`)',lambda m:m[1]+hashlib.sha256(path.read_bytes()).hexdigest()+m[2],freeze.read_text())
        try:
            if control.startswith('R9R3'):
                copy_f,copy_j=sealed_memory(text,MemoryPath(json.dumps(bundle,indent=2,ensure_ascii=False)+'\n'))
                check(copy_f,copy_j)
                validate_profiles(path,bundle,copy_f.read_text())
            else: ROUND9_CHECKS[control[2:4]](profiles,bundle,text)
        except ValueError as error:
            require(R9_CONTROL_MESSAGES[control] in str(error),'WRONG RED '+control+': '+str(error))
            print('RED %s: exit 1: %s'%(control,error))
        else: raise ValueError('UNEXPECTED GREEN '+control)
    print('GREEN mutation controls: %d intended RED (%d preserved + %d round9), zero filesystem writes'%(len(old)+len(selected),len(old),len(selected)))

mutation_controls=round9_mutation_controls
CONTROL_MESSAGES.update(R9_CONTROL_MESSAGES)


# Round 10: D13 origin-sensitive occurrences and reproducible recorded trace.

def trace_hits(command):
    require(isinstance(command,list) and command[:3]==['/usr/bin/grep','-n','-E'] and len(command)==6 and command[3]=='--', 'R10 trace command must be fixed read-only grep')
    require(command[-1] in {p.relative_to(ROOT).as_posix() for p in ROOT.glob('tools/*.py')} | {p.relative_to(ROOT).as_posix() for p in ROOT.glob('experiments/track_c/*.py')}, 'R10 trace source outside pinned scope')
    run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    require(run.returncode in (0,1) and not run.stderr, 'R10 recorded grep failed: '+run.stderr)
    return sorted(run.stdout.splitlines())


def trace_selector(inv, selector):
    return (selector['executable'] is None or inv['executable_path']==selector['executable']) and all(
        token in inv['argv'] for token in selector['argv_contains']) and all(
        any(isinstance(v,dict) and v.get('$bind','').startswith(prefix) for v in inv['argv']) for prefix in selector['bind_prefixes'])


def admission_roots(p, trace):
    root=trace['root']
    return [(path,inv) for path,inv in invocation_templates(p) if (path=='/existing_admission' or path.startswith('/children/')) and trace_selector(inv,root['selector'])]


def traced_occurrences(p, trace):
    roots=admission_roots(p,trace)
    if not roots:return []
    stages={inv['argv'][-1] for _,inv in roots}
    require(stages<=set(trace['supported_stages']), 'R10 unreviewed admission stage requires revised trace')
    application=next((a for a in trace['applications'] if a['entrypoint']==p['entrypoint'] and a['payload_argv']==p['authorized_payload']['argv']),None)
    require(application is not None, 'R10 admission origin has no recorded application')
    expected=[]
    for site in trace['process_sites']:
        if not r11_site_reachable(site, stages):continue
        family=site['id'] in (V_SITE,T_SITE)
        matched=[(n,ch) for n,ch in enumerate(p['children']) if ch.get('trace_site')==site['id'] and trace_selector(ch['invocation'],site['selector'])]
        require(matched,'R10 '+site['id']+' admission recipe missing: '+p['entrypoint'])
        admission=[(n,ch) for n,ch in matched if ch.get('origin')=='ADMISSION']
        if family:
            require(len(admission)==1,'R10 '+site['id']+' admission-origin occurrence missing/merged: '+p['entrypoint'])
            pass  # Family digests are checked after authority/origin assertions below.
        else:
            recipes={canonical(ch['invocation']) for _,ch in matched}
            require({hashlib.sha256(r.encode()).hexdigest() for r in recipes}==set(application['recipes'][site['id']]), 'R10 recorded admission recipe set mismatch: '+site['id'])
            for recipe in recipes:
                require(len([ch for _,ch in admission if canonical(ch['invocation'])==recipe])==1,'R10 '+site['id']+' admission-origin occurrence missing/merged: '+p['entrypoint'])
        for n,ch in admission:
            path='/children/%d'%n
            require(ch.get('role')=='ADMISSION_HELPER' and ch.get('registration_authority')=='C:115' and ch.get('enrollment')=='PRE_RELEASE_REQUIRED', 'R10 '+site['id']+' admission-origin carries A1/science authority: '+path)
            if site['shared_science']:
                science=[c for _,c in matched if c.get('origin')=='SCIENCE']
                require(science,'R10 '+site['id']+' origins merged/science occurrence missing')
                require(all(c['role']=='SCIENCE_CHILD' and c['registration_authority']==A1_AUTHORITY and c['enrollment']=='DECLARED_AT_ROOT_ADMISSION' for c in science), 'R10 shared science occurrence lost A1')
            expected.append(path)
        if family:
            require([digest_json(ch) for _,ch in admission]==application.get('operand_families',{}).get(site['id']), 'R10 recorded admission operand family mismatch: '+site['id'])
    require(len(expected)==len(set(expected)),'R10 admission occurrence serves multiple trace sites')
    require(set(expected)=={'/children/%d'%n for n,ch in enumerate(p['children']) if ch.get('origin')=='ADMISSION'}, 'R10 untraced admission occurrence')
    return expected


def round10_checks(profiles,bundle,text):
    round11_checks(profiles,bundle,text)
    trace=(profiles or bundle)['x-construction'].get('admission_trace')
    require(isinstance(trace,dict),'R10 admission transitive trace missing')
    require(trace.get('claim')=='RECORDED_QUERIES_ONLY_NOT_COMPLETE_CALL_GRAPH','R10 trace lexical limit missing')
    queries=trace['queries'];require(queries and len({q['id'] for q in queries})==len(queries),'R10 trace queries missing/duplicate')
    for q in queries:
        require(trace_hits(q['command'])==q['hits'],'R10 recomputed trace hit-set mismatch: '+q['id'])
        require(hashlib.sha256((ROOT/q['command'][-1]).read_bytes()).hexdigest()==q['sha256'],'R10 trace source pin mismatch: '+q['id'])
    byid={q['id']:q for q in queries}
    for site in trace['process_sites']:
        q=byid[site['query']]
        require(any(int(h.split(':',1)[0])==site['line'] for h in q['hits']), 'R10 reached process start absent from hit list: '+site['id'])
        require(q['command'][4]==r'subprocess\.|os\.(exec|spawn|system|popen)|Popen' or site['kind']=='ADMISSION_ROOT', 'R10 process-start query pattern changed')
        require(site['edges'] and all(edge in byid for edge in site['edges']), 'R10 process site call edge missing: '+site['id'])
    require(trace==bundle['x-construction'].get('admission_trace'),'R10 production/schema trace disagreement')
    require('D13' in text and 'RECORDED_QUERIES_ONLY_NOT_COMPLETE_CALL_GRAPH' in text,'R10 freeze origin/lexical boundary missing')
    for q in queries:
        require(shlex.join(q['command']) in text and json.dumps(q['hits'],ensure_ascii=False) in text,'R10 freeze command/hit record missing: '+q['id'])
    owners=(profiles['profiles'] if profiles else [e['instance'] for e in bundle['x-construction']['examples'].values() if e['schema_name']=='LaunchProfile' and e['instance']['scope']=='SCIENCE'])
    count=0
    for p in owners:
        paths=traced_occurrences(p,trace);count+=len(paths)
        if paths:
            require(p.get('composition_refusal','').startswith(ADMISSION_REASON),'R10 admission composition refusal missing')
    if profiles:
        require(len([p for p in owners if admission_roots(p,trace)])==len(trace['applications']), 'R10 admission application coverage changed')
        for i,p in enumerate(owners):
            prefix='ProductionLaunchProfile%03d'%i
            for n,ch in enumerate(p['children']):
                if ch.get('origin')!='ADMISSION':continue
                enrollment=profiles['x-construction']['examples'][prefix+'Descendant%d'%n]['instance']
                require(enrollment['kind']=='ADMISSION_HELPER' and enrollment['registration_authority']=='C:115' and enrollment['enrollment']=='PRE_RELEASE_REQUIRED','R10 admission enrollment carries science authority')
    round12_checks(profiles,bundle,text)
    print('GREEN D13 trace: %d recorded queries, %d admission-origin occurrences derived; recorded queries only, no complete call graph or native proof'%(len(queries),count))


def test_first_branch(profiles,branch):
    # Legacy defect probes run before any successor subjects exist.
    affected=[p for p in profiles['profiles'] if p.get('existing_admission') and any(isinstance(v,str) and v.endswith('/c10w_p2_gate.py') for v in p['existing_admission']['argv'])]
    require(affected,'R10 legacy positive control lacks gate admission')
    for p in affected:
        candidates=[ch for ch in p['children'] if ('verify-preflight' in ch['invocation']['argv'] if branch=='verify-preflight' else ch['invocation']['executable_path']=='/usr/bin/git' and any(isinstance(v,dict) and v.get('$bind','').startswith('p2_adapter_relative_') for v in ch['invocation']['argv']))]
        if candidates:
            require(any(ch.get('origin')=='ADMISSION' and ch['role']=='ADMISSION_HELPER' and ch['registration_authority']=='C:115' for ch in candidates),'R10 '+branch+' admission-origin misclassified SCIENCE_CHILD/DECLARED_AT_ROOT_ADMISSION/D-R2C-A1')
    require(any(('verify-preflight' in ch['invocation']['argv'] if branch=='verify-preflight' else ch['invocation']['executable_path']=='/usr/bin/git') for p in affected for ch in p['children']), 'R10 legacy branch recipe missing')


R10_CONTROL_MESSAGES={
 'R10A':'R10 verify-preflight admission-origin carries A1/science authority',
 'R10B':'R10 git-ls-files admission-origin carries A1/science authority',
 'R10C':'R10 recomputed trace hit-set mismatch: starts-train',
 'R10D':'R10 verify-preflight admission-origin occurrence missing/merged',
}
round9_controls=mutation_controls

def round10_mutation_controls(freeze,schemas,controls=None):
    old=[c for c in (controls or CONTROL_MESSAGES) if c not in R10_CONTROL_MESSAGES]
    if old:round9_controls(freeze,schemas,old)
    selected=[c for c in (controls or R10_CONTROL_MESSAGES) if c in R10_CONTROL_MESSAGES]
    for control in selected:
        profiles=read_json(PROFILES);bundle=read_json(schemas)
        if control=='R10C':
            q=next(q for q in profiles['x-construction']['admission_trace']['queries'] if q['id']=='starts-train')
            q['hits']=[h for h in q['hits'] if not h.startswith('65:')]
        else:
            site='git-ls-files' if control=='R10B' else 'verify-preflight'
            p=next(p for p in profiles['profiles'] if any(ch.get('origin')=='ADMISSION' and ch.get('trace_site')==site for ch in p['children']))
            ch=next(ch for ch in p['children'] if ch.get('origin')=='ADMISSION' and ch.get('trace_site')==site)
            if control=='R10D':
                science=next(c for c in p['children'] if c.get('origin')=='SCIENCE' and c['invocation']==ch['invocation'])
                science['origin']='ADMISSION_AND_SCIENCE';p['children'].remove(ch)
            else:ch.update(role='SCIENCE_CHILD',registration_authority=A1_AUTHORITY,enrollment='DECLARED_AT_ROOT_ADMISSION')
        try:round10_checks(profiles,bundle,freeze.read_text())
        except ValueError as error:
            require(R10_CONTROL_MESSAGES[control] in str(error),'WRONG RED '+control+': '+str(error));print('RED %s: exit 1: %s'%(control,error))
        else:raise ValueError('UNEXPECTED GREEN '+control)
    print('GREEN mutation controls: %d intended RED (%d preserved + %d D13), zero filesystem writes'%(len(old)+len(selected),len(old),len(selected)))

mutation_controls=round10_mutation_controls
CONTROL_MESSAGES.update(R10_CONTROL_MESSAGES)

def r11_counterexample(profiles,bundle):
    # Execute only the cited pure branch bodies; all IO/process boundaries are fixtures.
    from types import SimpleNamespace
    first,count=r11_source_domain();trace=profiles['x-construction']['admission_trace']
    p=next(p for p in profiles['profiles'] if any(inv['argv'][-1] not in (first,'p2-eval') for _,inv in admission_roots(p,trace)))
    require(any(inv['argv'][-1].startswith('p2-') for _,inv in admission_roots(p,trace)), 'R11B fixture lacks P2 argv')
    root=ROOT/'results/c10w_oracle/fixture-only';p1=root/'p1';p2=root/'p2';evaluation=root/'evaluation';authorization=root/'authorization'
    digest=hashlib.sha256(b'R11B passing linked fixture').hexdigest()
    proof={'phase':'P3','status':'PASS','law3':True,'law5_null':True,'fingerprint':True,'step0_sha256':digest,'provenance':{'pinned':digest},
           'evaluation':{'path':str(evaluation),'sha256':digest},'p1_directory':str(p1),'authorization':{'path':str(authorization),'sha256':digest},'authorized_projection_minutes':1,
           'law3_counts':{'A1':68,'A2':68,'para_full':5,'canon_full':5,'para_first':42,'u_para_full':0,'stimulus':[0,0,0,0]},
           'law5_standing':{'ok':True,'expr_delta':0,'loc_delta':0},'null_evidence':{'base_hash':digest,'after_hash':digest,'u_hit_probe_sha256':digest,'zero_hit_probe_sha256':digest,'ppl_delta':0,'described_as':100.}}
    evidence={k:v for k,v in proof.items() if k not in ('phase','p1_directory','authorization','authorized_projection_minutes')}
    record={'phase':'P2','p1_eval_sha256':digest,'authorization':proof['authorization'],'authorized_projection_minutes':1,
            'step0_directory':str(root/'step0'),'provenance':proof['provenance'],
            'train_records':[{'status':'PASS','adapter':{'path':str(p2/('adapter%d'%i)),'sha256':digest}} for i in range(count)]}
    values={str(evaluation):{'provenance':proof['provenance']},str(authorization):{'authorized':True},str(p2/'eval.json'):record,str(p1/'eval.json'):{},str(p1/'verdict.json'):{}}
    probes=[]
    def verify_ref(ref):require(ref.get('sha256')==digest and ref['path'] in values or ref.get('sha256')==digest and ref['path'].startswith(str(p2/'adapter')), 'R11B fixture linked prerequisite failed')
    def authorization_ok(phase,auth,eval_hash,verdict_hash,minutes):require(phase in ('P2','P3') and auth=={'authorized':True} and eval_hash==verdict_hash==digest and minutes==1,'R11B fixture authorization failed')
    ns={'Path':Path,'ROOT':ROOT,'require':require,'verify_ref':verify_ref,'load_json':lambda path:values[str(path)],
        'sha_file':lambda path:digest,'preflight_evidence':lambda raw:evidence,'require_authorization':authorization_ok,
        'latest_directory':lambda phase:p2,'load_frozen':lambda path:{'provenance':proof['provenance']},'frozen_provenance':lambda frozen:frozen['provenance'],
        'verify_linked_train':lambda tr:require(tr['status']=='PASS','R11B fixture training failed'),
        'validate_phase':lambda rec:require(rec['phase']=='P2' and len(rec['train_records'])==count,'R11B fixture replication failed'),
        'read_measurement':lambda phases:{'status':'INCOMPLETE','p3_required':True}}
    def run(argv,**kwargs):
        if argv[0]=='/usr/bin/git':probes.append(argv);return SimpleNamespace(returncode=1,stdout='',stderr='')
        require(argv[-1]=='verify-preflight','R11B unexpected fixture process')
        ns['verify_preflight_certificate'](json.loads(kwargs['input']))
        return SimpleNamespace(returncode=0,stdout='{"ok":true}',stderr='')
    ns['subprocess']=SimpleNamespace(run=run)
    wanted={'verify_preflight_certificate','authorized_phase_entry','replication_for','require_untracked_adapter','adapter_is_tracked'}
    tree=ast.parse((ROOT/'experiments/track_c/c10w_oracle_read.py').read_text())
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    require({n.name for n in nodes}==wanted,'R11B pinned branch functions missing')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<R11B pinned reader bodies>','exec'),ns)
    training={'R':SimpleNamespace(**ns),'subprocess':SimpleNamespace(run=run),'json':json}
    tree=ast.parse((ROOT/'experiments/track_c/c10w_oracle_train.py').read_text())
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='require_training_preflight')
    exec(compile(ast.Module(body=[node],type_ignores=[]),'<R11B pinned training body>','exec'),training)
    training['require_training_preflight'](proof,digest,proof['provenance'])
    require(len(probes)==count,'R11B P2 argv/P3 certificate did not reach Git with passing prerequisites')
    print('R11B fixture: P2 argv %s; P3 certificate; linked/evidence/authorization prerequisites PASS; %d mocked Git probes, no file writes or real Git/verifier launches; source reads/path resolution occur'%(admission_roots(p,trace)[0][1]['argv'][-1],len(probes)))
    missing=next(ch for ch in p['children'] if ch.get('origin')=='ADMISSION' and ch.get('trace_site')=='git-ls-files')
    p['children'].remove(missing)


# Round 11: D14 certificate-selected reachability, independent of argv stage.
def r11_source_domain():
    tree=ast.parse((ROOT/'experiments/track_c/c10w_oracle_read.py').read_text())
    assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    stages=ast.literal_eval(assignments['TRAIN_STAGES'])['P2']
    units=assignments['TRAIN_UNITS']
    count=next(len(v.elts) for k,v in zip(units.keys,units.values) if ast.literal_eval(k)=='P2')
    return stages[0],count


def r11_site_reachable(site,stages):
    kind=site.get('selector_kind')
    require(kind in ('argv_stage','loaded_data','unconditional'),'R11 process site selector kind missing: '+site['id'])
    if kind=='loaded_data':
        require(not site.get('stages'),'R11 loaded_data site filtered by argv stage: '+site['id'])
        excluded={s for e in site.get('exclusions',[]) for s in e['stages']}
        return bool(stages-excluded)
    if kind=='unconditional':
        require(not site.get('stages'),'R11 unconditional site filtered by argv stage: '+site['id'])
        return True
    return bool(stages.intersection(site['stages']))


def r11_selectors(trace):
    git=next(s for s in trace['process_sites'] if s['id']=='git-ls-files')
    require(git.get('selector_kind')=='loaded_data' and not git.get('stages'), 'R11 loaded_data site filtered by argv stage: git-ls-files')
    for site in trace['process_sites']:
        if site['id']=='git-ls-files':
            require(site.get('selector_kind')=='loaded_data' and not site.get('stages'),
                    'R11 loaded_data site filtered by argv stage: git-ls-files')
        r11_site_reachable(site,set(trace['supported_stages']))


def r11_exclusion(trace):
    first,_=r11_source_domain()
    site=next(s for s in trace['process_sites'] if s['id']=='git-ls-files')
    exclusions=site.get('exclusions',[])
    require(len(exclusions)==1 and exclusions[0].get('stages')==[first], 'R11 first-stage exclusion unpinned: stage domain')
    pin=exclusions[0].get('enforcing_line',{})
    line=(ROOT/'tools/c10w_p2_gate.py').read_text().splitlines()[102]
    require(pin.get('path')=='tools/c10w_p2_gate.py' and pin.get('line')==103 and
            pin.get('text')==line and pin.get('sha256')==hashlib.sha256(line.encode()).hexdigest() and
            'phase="P2"' in line, 'R11 first-stage exclusion unpinned: gate:103')
    require(site.get('selector_field')=='certificate.phase','R11 loaded_data selector field missing')
    return first


def r11_reachability(profiles,bundle):
    trace=(profiles or bundle)['x-construction']['admission_trace'];first,_=r11_source_domain()
    owners=profiles['profiles'] if profiles else [e['instance'] for e in bundle['x-construction']['examples'].values() if e['schema_name']=='LaunchProfile' and e['instance']['scope']=='SCIENCE']
    for p in owners:
        roots=admission_roots(p,trace)
        if not roots:continue
        stages={inv['argv'][-1] for _,inv in roots}
        if stages=={first}:continue
        candidates=[ch for ch in p['children'] if ch.get('origin')=='ADMISSION' and ch.get('trace_site')==V_SITE]
        require(len(candidates)==1, 'R11 reachable admission occurrence missing: verifier-descendant Git, '+','.join(sorted(stages)))
        application=next(a for a in trace['applications'] if a['entrypoint']==p['entrypoint'] and a['payload_argv']==p['authorized_payload']['argv'])
        require(application.get('routes',{}).get(V_SITE)==['verifier-p3'],'R11 reachable admission route coverage missing')
        if 'p2-eval' in stages:
            require(application.get('routes',{}).get(T_SITE)==['gate-phase-trains'],'R11 reachable admission route coverage missing')
            require(len([ch for ch in p['children'] if ch.get('origin')=='ADMISSION' and ch.get('trace_site')==T_SITE])==1,'R11 reachable admission route coverage missing')
        require(p.get('composition_refusal','').startswith(ADMISSION_REASON),'R11 composition refusal missing')


def round11_checks(profiles,bundle,text):
    trace=(profiles or bundle)['x-construction']['admission_trace']
    r11_selectors(trace);r11_exclusion(trace);r11_reachability(profiles,bundle)
    site=next(s for s in trace['process_sites'] if s['id']=='git-ls-files')
    routes={r['id']:r for source in (site,r12_site(trace,T_SITE)) for r in source.get('routes',[])}
    require(set(routes)=={'verifier-p3','gate-phase-trains'},'R11 Git routes missing')
    expected=['tools/c10w_p2_gate.py:101,104–105','experiments/track_c/c10w_oracle_train.py:51–66',
              'experiments/track_c/c10w_oracle_read.py:588,531–539,538,542,550,139–140,133']
    require(routes['verifier-p3'].get('citations')==expected and routes['verifier-p3'].get('selector_kind')=='loaded_data','R11 verifier descendant route citations missing')
    require(routes['gate-phase-trains'].get('citations')==['tools/c10w_p2_gate.py:128','experiments/track_c/c10w_oracle_read.py:520,139–140,133'] and routes['gate-phase-trains'].get('selector_kind')=='argv_stage','R11 direct Git route citations missing')
    require('D14' in text and 'gate:103' in text,'R11 freeze exclusion/reachability rule missing')


R11_CONTROL_MESSAGES={
 'R11A':'R11 loaded_data site filtered by argv stage: git-ls-files',
 'R11B':'R11 reachable admission occurrence missing: verifier-descendant Git',
 'R11C':'R11 first-stage exclusion unpinned: gate:103',
}
round10_controls=mutation_controls


def round11_mutation_controls(freeze,schemas,controls=None):
    old=[c for c in (controls or CONTROL_MESSAGES) if c not in R11_CONTROL_MESSAGES]
    if old:round10_controls(freeze,schemas,old)
    selected=[c for c in (controls or R11_CONTROL_MESSAGES) if c in R11_CONTROL_MESSAGES]
    for control in selected:
        profiles=read_json(PROFILES);bundle=read_json(schemas)
        site=next(s for s in profiles['x-construction']['admission_trace']['process_sites'] if s['id']=='git-ls-files')
        if control=='R11A':site['stages']=['p2-eval']
        elif control=='R11B':
            r11_counterexample(profiles,bundle)
        else:site['exclusions'][0]['enforcing_line'].pop('sha256')
        # Both recorded copies agree: each control isolates its own semantic defect.
        bundle['x-construction']['admission_trace']=copy.deepcopy(profiles['x-construction']['admission_trace'])
        try:round11_checks(profiles,bundle,freeze.read_text())
        except ValueError as error:
            require(R11_CONTROL_MESSAGES[control] in str(error),'WRONG RED '+control+': '+str(error));print('RED %s: exit 1: %s'%(control,error))
        else:raise ValueError('UNEXPECTED GREEN '+control)
    print('GREEN mutation controls: %d intended RED (%d preserved + %d D14), zero filesystem writes'%(len(old)+len(selected),len(old),len(selected)))

mutation_controls=round11_mutation_controls
CONTROL_MESSAGES.update(R11_CONTROL_MESSAGES)

# Round 12: D15 pre-spawn cardinality and operand-source proof.
OPERAND_REASON = 'NOT_ADMITTED_OPERAND_DOMAIN_UNENUMERATED:'
READER_SOURCE = 'experiments/track_c/c10w_oracle_read.py'
V_SITE = 'git-ls-files'
T_SITE = 'git-phase-trains'


def r12_pin(path, number):
    line = (ROOT / path).read_text().splitlines()[number - 1]
    return {'path': path, 'line': number, 'text': line,
            'sha256': hashlib.sha256(line.encode()).hexdigest()}


def r12_pins_valid(pins, message):
    require(isinstance(pins, list) and pins, message)
    for pin in pins:
        require(isinstance(pin, dict) and isinstance(pin.get('path'), str)
                and type(pin.get('line')) is int and pin['line'] > 0, message)
        require(pin == r12_pin(pin['path'], pin['line']), message)


def r12_site(trace, name):
    matches = [s for s in trace['process_sites'] if s['id'] == name]
    require(len(matches) == 1, 'R12 process site missing/duplicate: ' + name)
    return matches[0]


# Inserted into K9: exact metadata expected from pinned pre-spawn source.
def r12_metadata():
    gate='tools/c10w_p2_gate.py'; train='experiments/track_c/c10w_oracle_train.py'
    step='experiments/track_c/c10w_oracle_step0.py'; shell='tools/run_c10w_p2_stage.sh'
    dispatch='tools/run_c10w_stage.sh'; read=READER_SOURCE
    def pins(path,*lines):return [r12_pin(path,n) for n in lines]
    def constant(maximum,path,*lines):return {'kind':'pinned_constant','maximum':maximum,'enforcing_lines':pins(path,*lines)}
    def literal(path,*lines):return {'kind':'pinned_literal','enforcing_lines':pins(path,*lines)}
    def loaded(record,field,path,lines,constraints):
        return {'kind':'loaded_data','record':record,'field':field,'read_lines':pins(path,*lines),'pre_spawn_constraints':constraints}
    vcount={'kind':'loaded_data','record':'latest_directory("p2")/eval.json','field':'train_records','selection_lines':pins(read,543,549)}
    vsource=loaded('latest_directory("p2")/eval.json','train_records[*].adapter.path',read,(543,549,550),pins(read,70,71,72,73,74,132,133,525,526,527,528,550))
    tsource=loaded('train/<tag>_{400,800}.json (last existing file)','adapter.path',read,(516,517,518,519,520),pins(read,70,71,72,73,74,132,133,518,519,520))
    result={
      V_SITE:(vcount,vsource),
      T_SITE:(constant(6,read,28,29,30,515),tsource),
      'gate-root':(constant(1,shell,22),loaded('shell arguments','S; EXTRA',shell,(8,9,10,12,13,22),pins(shell,9,12,13,22))),
      'fingerprint':(constant(1,gate,70),literal(gate,70)),
      'ps':(constant(1,gate,75),literal(gate,75)),
      'env':(constant(1,gate,79),literal(gate,79)),
      'tmux-exec':(constant(1,gate,79),loaded('process environment','PATH selects tmux executable',gate,(79,),pins(gate,79))),
      'verify-preflight':(constant(1,train,65),literal(train,65,66)),
      'science-replication':(vcount,vsource),
      'science-disk-records':({'kind':'loaded_data','record':'disk_state latest phase eval.json records','field':'phases[*].train_records','selection_lines':pins(read,593,596,597,599,604,607)},
          loaded('disk_state latest phase eval.json records','phases[*].train_records[*].adapter.path',read,(593,596,597,599,604,607,608),pins(read,70,71,72,73,74,132,133,600,601,602,606,608))),
      'science-fingerprint':(constant(1,step,101),literal(step,100,101,102)),
      'science-shell-dispatch':(constant(1,shell,34),loaded('shell arguments','S',shell,(8,9,34),pins(shell,9,26,34))),
      'science-python-dispatch':(constant(1,dispatch,15),loaded('shell arguments','argv[1]',dispatch,(15,),pins(dispatch,9,10,11,14,15))),
      'science-train-child':(constant(3,step,398,399,401,405,407,409),loaded('dispatch stage and disk-selected training records','directory; step0; unit; steps',step,(376,382,388,393,394,398,401,409,305,306),pins(step,296,397,400,407,408))),
      'science-eval-child':(constant(1,step,411,415),loaded('dispatch stage and disk-selected phase','phase; directory; step0',step,(376,382,411,415),pins(step,296,413,414))),
      'science-read-child':(constant(1,step,357),literal(step,357)),
      'science-shell-dirname-p2':(constant(1,shell,7),literal(shell,7)),
      'science-shell-dirname-dispatch':(constant(1,dispatch,7),literal(dispatch,7)),
      'science-shell-mkdir':(constant(1,shell,20),literal(shell,8,20)),
      'science-shell-date':(constant(1,shell,24),literal(shell,24)),
    }
    for phase,maximum in [('p1',5),('p2',6),('p3',4)]:
        result['science-phase-trains-'+phase]=(constant(maximum,read,28,29,30,515),tsource)
    return result


def r12_validate_metadata(site, count, source):
    expected=r12_metadata()
    require(site in expected,'R12 process site has no source mapping: '+site)
    require((count,source)==expected[site],'R12 occurrence/site differs from exact pinned pre-spawn metadata: '+site)
    for value in (count,source):
        for key in ('enforcing_lines','selection_lines','read_lines','pre_spawn_constraints'):
            if key in value:r12_pins_valid(value[key],'R12 process metadata pin mismatch: '+site)


def r12_counts(trace):
    v = r12_site(trace, V_SITE)
    # The round-11 representation is six indexed bindings, with no pre-spawn bound.
    require(v.get('count', {}).get('kind') == 'loaded_data',
            'R12 loaded_data count represented by an unpinned constant: verifier-p3')
    count = v['count']
    require(set(count) == {'kind', 'record', 'field', 'selection_lines'}
            and count['record'] == 'latest_directory("p2")/eval.json'
            and count['field'] == 'train_records',
            'R12 verifier count must come from eval.json train_records without a bound')
    r12_pins_valid(count['selection_lines'], 'R12 verifier count source unpinned')
    require(count['selection_lines'] == [r12_pin(READER_SOURCE, 543), r12_pin(READER_SOURCE, 549)],
            'R12 verifier count source differs from pinned pre-spawn loop')
    t = r12_site(trace, T_SITE)
    bound = t.get('count', {})
    require(bound.get('kind') == 'pinned_constant' and bound.get('maximum') == r11_source_domain()[1],
            'R12 count bound unpinned: gate-phase-trains')
    r12_pins_valid(bound.get('enforcing_lines'), 'R12 count bound unpinned: gate-phase-trains')
    require(bound['enforcing_lines'] == [r12_pin(READER_SOURCE, n) for n in (28, 29, 30, 515)],
            'R12 count bound unpinned: gate-phase-trains')
    for site in trace['process_sites']:
        c = site.get('count', {})
        require(c.get('kind') in ('pinned_constant', 'loaded_data'),
                'R12 process site count kind missing: ' + site['id'])
        if c['kind'] == 'pinned_constant':
            require(type(c.get('maximum')) is int and c['maximum'] > 0,
                    'R12 constant count missing: ' + site['id'])
            r12_pins_valid(c.get('enforcing_lines'), 'R12 count bound unpinned: ' + site['id'])
        else:
            require(not any(k in c for k in ('maximum', 'constant', 'bound', 'recipes')),
                    'R12 loaded_data count represented by an unpinned constant: ' + site['id'])
            require(c.get('record') and c.get('field'), 'R12 loaded count source missing: ' + site['id'])
            r12_pins_valid(c.get('selection_lines'), 'R12 loaded count source unpinned: ' + site['id'])


def r12_route_equality(profiles, bundle):
    trace = (profiles or bundle)['x-construction']['admission_trace']
    owners = profiles['profiles'] if profiles else [e['instance'] for e in bundle['x-construction']['examples'].values()
              if e['schema_name'] == 'LaunchProfile' and e['instance']['scope'] == 'SCIENCE']
    for p in owners:
        roots = admission_roots(p, trace)
        if not any(inv['argv'][-1] == 'p2-eval' for _, inv in roots):
            continue
        application = next(a for a in trace['applications'] if a['entrypoint'] == p['entrypoint']
                           and a['payload_argv'] == p['authorized_payload']['argv'])
        # A single recipe set labelled with both routes is exactly V11 F2.
        require(T_SITE in application.get('operand_families', {})
                and V_SITE in application.get('operand_families', {}),
                'R12 routes merged without pinned pre-spawn operand equality: profile 38')
        v = [ch for ch in p['children'] if ch.get('origin') == 'ADMISSION' and ch.get('trace_site') == V_SITE]
        t = [ch for ch in p['children'] if ch.get('origin') == 'ADMISSION' and ch.get('trace_site') == T_SITE]
        require(len(v) == len(t) == 1 and canonical(v[0]['invocation']) != canonical(t[0]['invocation']),
                'R12 routes merged without pinned pre-spawn operand equality: profile 38')
        require(v[0].get('operand_source') != t[0].get('operand_source'),
                'R12 routes merged without pinned pre-spawn operand equality: profile 38')
        require(set(application['operand_families'][V_SITE]).isdisjoint(application['operand_families'][T_SITE]),
                'R12 routes merged without pinned pre-spawn operand equality: profile 38')


def r12_operand_sources(trace):
    expected = {
        V_SITE: ('latest_directory("p2")/eval.json', 'train_records[*].adapter.path', (543, 549, 550)),
        T_SITE: ('train/<tag>_{400,800}.json (last existing file)', 'adapter.path', (516, 517, 518, 519, 520)),
    }
    for site in trace['process_sites']:
        source = site.get('operand_source', {})
        require(source.get('kind') in ('pinned_literal', 'loaded_data'),
                'R12 process site operand source kind missing: ' + site['id'])
        if source['kind'] == 'pinned_literal':
            r12_pins_valid(source.get('enforcing_lines'), 'R12 literal operands unpinned: ' + site['id'])
        else:
            require(source.get('record') and source.get('field'), 'R12 loaded operand record/field missing: ' + site['id'])
            r12_pins_valid(source.get('read_lines'), 'R12 loaded operands unpinned: ' + site['id'])
            r12_pins_valid(source.get('pre_spawn_constraints'), 'R12 operand constraints unpinned: ' + site['id'])
        if site['id'] in expected:
            record, field, numbers = expected[site['id']]
            require(source.get('kind') == 'loaded_data' and source.get('record') == record and source.get('field') == field,
                    'R12 independent operand source mismatch: ' + site['id'])
            require(source['read_lines'] == [r12_pin(READER_SOURCE, n) for n in numbers],
                    'R12 independent operand selection unpinned: ' + site['id'])
            constraints = source['pre_spawn_constraints']
            require(all(r12_pin(READER_SOURCE, n) in constraints for n in (132, 133)),
                    'R12 Git ROOT/-- constraints unpinned: ' + site['id'])


def round12_checks(profiles, bundle, text):
    trace = (profiles or bundle)['x-construction']['admission_trace']
    r12_counts(trace)
    r12_route_equality(profiles, bundle)
    r12_operand_sources(trace)
    require('D15' in text and OPERAND_REASON in text, 'R12 freeze D15 refusal missing')
    owners = profiles['profiles'] if profiles else [e['instance'] for e in bundle['x-construction']['examples'].values()
              if e['schema_name'] == 'LaunchProfile' and e['instance']['scope'] == 'SCIENCE']
    totals = {origin: {'count': {'pinned_constant': 0, 'loaded_data': 0},
                       'operand_source': {'pinned_literal': 0, 'loaded_data': 0}}
              for origin in ('ADMISSION', 'SCIENCE')}
    for p in owners:
        for child in p['children']:
            origin = child.get('origin')
            require(origin in totals, 'R12 process origin missing')
            site = child['trace_site']
            for field, kinds in (('count', ('pinned_constant', 'loaded_data')),
                                 ('operand_source', ('pinned_literal', 'loaded_data'))):
                value = child.get(field, {})
                require(value.get('kind') in kinds, 'R12 occurrence ' + field + ' kind missing: ' + site)
                totals[origin][field][value['kind']] += 1
            loaded = child['count']['kind'] == 'loaded_data' or child['operand_source']['kind'] == 'loaded_data'
            if loaded:
                require(child.get('occurrence_form') == 'OPERAND_FAMILY_NOT_ENUMERATED',
                        'R12 loaded-data occurrence represented as bound recipes: ' + site)
                require(OPERAND_REASON + site in p.get('composition_refusal', ''),
                        'R12 uncovered operand domain not refused: ' + site)
            if origin == 'SCIENCE':
                require(child['registration_authority'] == A1_AUTHORITY and child['enrollment'] == 'DECLARED_AT_ROOT_ADMISSION',
                        'R12 science occurrence lost A1 authority: ' + site)
            else:
                require(child['registration_authority'] == 'C:115' and child['enrollment'] == 'PRE_RELEASE_REQUIRED',
                        'R12 admission occurrence carries science authority: ' + site)
                require(p.get('composition_refusal', '').startswith(ADMISSION_REASON),
                        'R12 admission helper refusal lost')
            if site in (V_SITE, T_SITE):
                source_site = r12_site(trace, site)
                require(child['count'] == source_site['count'] and child['operand_source'] == source_site['operand_source'],
                        'R12 occurrence differs from pinned count/operand source: ' + site)
    for site in trace['process_sites']:
        r12_validate_metadata(site['id'],site['count'],site['operand_source'])
    for p in owners:
        for child in p['children']:
            r12_validate_metadata(child['trace_site'],child['count'],child['operand_source'])
    for origin, counts in totals.items():
        print('GREEN D15 %s sites: count pinned_constant=%d loaded_data=%d; operand-source pinned_literal=%d loaded_data=%d' %
              (origin, counts['count']['pinned_constant'], counts['count']['loaded_data'],
               counts['operand_source']['pinned_literal'], counts['operand_source']['loaded_data']))


def r12_fixture(control):
    """Pinned branch bodies, in-memory disk/reference mocks; no writes or real children."""
    from types import SimpleNamespace
    from unittest.mock import patch
    wanted = {'verify_preflight_certificate', 'authorized_phase_entry', 'replication_for',
              'verify_linked_train', 'require_untracked_adapter', 'adapter_is_tracked',
              'phase_trains', 'train_tag', 'train_identity', 'validate_phase'}
    tree = ast.parse((ROOT / READER_SOURCE).read_text())
    bodies = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    require({n.name for n in bodies} == wanted, 'R12 fixture pinned reader bodies missing')
    names = {'CLASS', 'DECISION_ID', 'MODEL_ID', 'MODEL_REV', 'BAND', 'TEMPLATE_SHA', 'PREREG_SHA',
             'A1', 'A2', 'A7', 'SHUF', 'CANON_ARM', 'RECIPES', 'TRAIN_UNITS'}
    constants = [n for n in tree.body if isinstance(n, ast.Assign)
                 and {x.id for t in n.targets for x in ast.walk(t) if isinstance(x, ast.Name)} <= names]
    ns = {'Path': Path, 'ROOT': ROOT, 'require': require}
    exec(compile(ast.Module(body=constants, type_ignores=[]), '<R12 pinned constants>', 'exec'), ns)
    exec(compile(ast.Module(body=bodies, type_ignores=[]), '<R12 pinned reader bodies>', 'exec'), ns)
    root = ROOT / 'results/c10w_oracle/fixture-only'; p1 = root / 'p1'; p2 = root / 'p2'
    evaluation = root / 'evaluation'; authorization = root / 'authorization'
    sha = hashlib.sha256(b'R12 valid evidence fixture').hexdigest()
    provenance = {k: sha for k in ('train_inputs', 'trainer_source', 'mmlu200', 'templates', 'prereg')}
    provenance.update(templates=ns['TEMPLATE_SHA'], prereg=ns['PREREG_SHA'])
    proof = {'phase': 'P3', 'status': 'PASS', 'law3': True, 'law5_null': True, 'fingerprint': True,
             'step0_sha256': sha, 'provenance': provenance, 'p1_directory': str(p1),
             'evaluation': {'path': str(evaluation), 'sha256': sha},
             'authorization': {'path': str(authorization), 'sha256': sha}, 'authorized_projection_minutes': 1,
             'law3_counts': {'A1': 68, 'A2': 68, 'para_full': 5, 'canon_full': 5, 'para_first': 42,
                             'u_para_full': 0, 'stimulus': [0, 0, 0, 0]},
             'law5_standing': {'ok': True, 'expr_delta': 0, 'loc_delta': 0},
             'null_evidence': {'base_hash': sha, 'after_hash': sha, 'u_hit_probe_sha256': sha,
                              'zero_hit_probe_sha256': sha, 'ppl_delta': 0, 'described_as': 100.}}
    evidence = {k: v for k, v in proof.items() if k not in ('phase', 'p1_directory', 'authorization', 'authorized_projection_minutes')}
    values = {str(evaluation): {'provenance': provenance}, str(authorization): {'authorized': True},
              str(p1 / 'eval.json'): {}, str(p1 / 'verdict.json'): {}}
    references = {str(path): sha for path in (evaluation, authorization, p1 / 'eval.json', p1 / 'verdict.json')}
    units = ns['TRAIN_UNITS']['P2']
    count = 7 if control == 'R12A' else len(units)
    linked = []
    for index in range(count):
        unit = units[index % len(units)]
        adapter = p2 / ('earlier_adapter_%d' % index)
        adapter_sha = hashlib.sha256(('adapter bytes %d' % index).encode()).hexdigest()
        original = {'arm': unit[0], 'seed': unit[1], 'rank': unit[2], 'retrain': unit[3],
                    'status': 'PASS', 'adapter': {'path': str(adapter), 'sha256': adapter_sha}}
        path = p2 / ('linked_attempt_%d.json' % index)
        values[str(path)] = original
        references[str(path)] = digest_json(original)
        references[str(adapter)] = adapter_sha
        linked.append(dict(original, record_file={'path': str(path), 'sha256': references[str(path)]}))
    band_hash = {str(n): sha for n in ns['BAND']}
    def arm():
        return {'extra': {'mmlu': {'correct': [], 'correct_to_wrong': 0, 'wrong_to_correct': 0},
                          'cross_score': {}, 'cross_detail': {}}, 'para_full_n': 68}
    recipes = {}
    for name, arms in dict(closedform=(ns['A1'], ns['A2'], ns['A7']), **ns['RECIPES']['P2']).items():
        recipes[name] = {'band': list(ns['BAND']), 'restored': True, 'band_after_hash': band_hash,
                         'law5_gate': {'ok': True, 'expr_delta': 0, 'loc_delta': 0},
                         'arms': {key: arm() for key in arms}, 'detail': {key: {} for key in arms}}
    record = {'class': ns['CLASS'], 'decision_id': ns['DECISION_ID'], 'status': 'PASS', 'phase': 'P2',
              'p1_eval_sha256': sha, 'authorization': proof['authorization'], 'authorized_projection_minutes': 1,
              'step0_directory': str(root / 'step0'), 'provenance': provenance, 'train_records': linked,
              'environment': {'model_id': ns['MODEL_ID'], 'model_revision': ns['MODEL_REV'],
                              'layers': list(ns['BAND']), 'dtype': 'float16', 'device': 'mps'},
              'validity': {k: True for k in ('fingerprint', 'seal', 'instrument', 'hashes', 'entry', 'seam')},
              'wall_seconds': 1, 'sampled_peak_driver_bytes': 1,
              'u': {k: arm() for k in (ns['A1'], ns['A2'], ns['A7'], ns['SHUF'])},
              'stimulus': {k: [] for k in (ns['A1'], ns['A2'], ns['A7'], ns['SHUF'])},
              'u_detail': {k: {} for k in (ns['A1'], ns['A2'], ns['A7'], ns['SHUF'])},
              'law5_null': dict(ok=True, weights_identical=True, counts_identical=True, probes_identical=True,
                                ppl_delta=0, described_as=100., arm={}, rows={}, base_hash=band_hash, after_hash=band_hash),
              'delegation_identity': True, 'base_band_hash': band_hash, 'final_band_hash': band_hash,
              'zero_adapter_hits': 1, 'expected_zero_hits': 1,
              'trained_oracle_hits': len(units), 'expected_trained_hits': len(units), 'recipes': recipes}
    values[str(p2 / 'eval.json')] = record
    probes = []; boundaries = []
    def verify_ref(ref):
        require(ref.get('path') in references and references[ref['path']] == ref.get('sha256'),
                'R12 fixture linked/reference prerequisite failed')
    def authorization_ok(phase, auth, eval_sha, verdict_sha, minutes):
        require(phase in ('P2', 'P3') and auth == {'authorized': True} and eval_sha == verdict_sha == sha
                and minutes == 1, 'R12 fixture authorization prerequisite failed')
    ns.update(verify_ref=verify_ref, load_json=lambda path: values[str(path)], sha_file=lambda path: sha,
              preflight_evidence=lambda raw: evidence, require_authorization=authorization_ok,
              latest_directory=lambda phase: p2, load_frozen=lambda path: {'provenance': provenance},
              frozen_provenance=lambda frozen: frozen['provenance'],
              read_measurement=lambda phases: {'status': 'INCOMPLETE', 'p3_required': True})
    for name in ('finite', 'validate_arm', 'check_eval_seconds', 'check_driver_bytes', 'compare_null', 'law3', 'verify_prompt_count'):
        ns[name] = lambda *args, **kwargs: None
    pinned_validator = ns['validate_phase']
    def validator(rec):
        boundaries.append(('validate_phase', len(probes)))
        if control == 'R12A':
            pinned_validator(rec)
        else:
            require(rec['phase'] == 'P2' and len(rec['train_records']) == len(units), 'R12B fixture replication invalid')
    ns['validate_phase'] = validator
    def run(argv, **kwargs):
        if argv[0] == '/usr/bin/git':
            require(argv[:4] == ['/usr/bin/git', 'ls-files', '--error-unmatch', '--'], 'R12 fixture wrong Git command')
            probes.append(argv[-1]); return SimpleNamespace(returncode=1, stdout='', stderr='')
        require(argv[-1] == 'verify-preflight', 'R12 fixture unexpected real-child recipe')
        ns['verify_preflight_certificate'](json.loads(kwargs['input']))
        return SimpleNamespace(returncode=0, stdout='{"ok":true}', stderr='')
    ns['subprocess'] = SimpleNamespace(run=run)
    training = {'R': SimpleNamespace(**ns), 'subprocess': SimpleNamespace(run=run), 'json': json}
    tree = ast.parse((ROOT / 'experiments/track_c/c10w_oracle_train.py').read_text())
    body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'require_training_preflight')
    exec(compile(ast.Module(body=[body], type_ignores=[]), '<R12 pinned training body>', 'exec'), training)
    if control == 'R12A':
        try:
            training['require_training_preflight'](proof, sha, provenance)
        except ValueError as error:
            require(str(error) == 'INVALID-INCOMPLETE: matched training units', 'R12A wrong validation failure: ' + str(error))
        else:
            raise ValueError('R12A expected pinned validate_phase to reject seven units')
        require(len(probes) == len(set(probes)) == 7 and boundaries == [('validate_phase', 7)],
                'R12A must reach seven distinct Git probes before validation failure')
        print('R12A fixture: P2 argv/P3 certificate; upstream/link prerequisites PASS; seven distinct mocked Git probes before pinned validate_phase:333 raises; no writes or real Git/verifier launches; source reads/path resolution occur')
    else:
        training['require_training_preflight'](proof, sha, provenance)
        earlier = set(probes); probes.clear()
        selected = set()
        for index, unit in enumerate(units):
            path = p2 / 'train' / (ns['train_tag'](unit, 800) + '.json')
            adapter = p2 / ('later_adapter_%d' % index)
            adapter_sha = hashlib.sha256(('later adapter %d' % index).encode()).hexdigest()
            values[str(path)] = {'status': 'PASS', 'adapter': {'path': str(adapter), 'sha256': adapter_sha}}
            references[str(adapter)] = adapter_sha; selected.add(str(path))
        with patch.object(Path, 'is_file', lambda path: str(path) in selected):
            ns['phase_trains'](p2, 'P2')
        later = set(probes)
        require(len(earlier) == len(later) == len(units) and earlier.isdisjoint(later),
                'R12B independent routes must probe different operand sets')
        print('R12B fixture: profile 38 p2-eval; eval.json earlier linked adapters versus last-existing train/*.json later adapters; %d + %d disjoint mocked Git operands; no writes or real Git/verifier launches; source reads/path resolution occur' % (len(earlier), len(later)))


R12_CONTROL_MESSAGES = {
    'R12A': 'R12 loaded_data count represented by an unpinned constant: verifier-p3',
    'R12B': 'R12 routes merged without pinned pre-spawn operand equality: profile 38',
    'R12C': 'R12 count bound unpinned: gate-phase-trains',
}
round11_controls = mutation_controls


def round12_mutation_controls(freeze, schemas, controls=None):
    old = [c for c in (controls or CONTROL_MESSAGES) if c not in R12_CONTROL_MESSAGES]
    if old:
        round11_controls(freeze, schemas, old)
    selected = [c for c in (controls or R12_CONTROL_MESSAGES) if c in R12_CONTROL_MESSAGES]
    for control in selected:
        profiles = read_json(PROFILES)
        bundle = read_json(schemas)
        # First prove that the exact baseline passes, then mutate only this defect.
        round12_checks(profiles, bundle, freeze.read_text())
        trace = profiles['x-construction']['admission_trace']
        if control == 'R12A':
            r12_fixture(control)
            r12_site(trace, V_SITE)['count'] = {'kind': 'pinned_constant', 'maximum': r11_source_domain()[1],
                                               'enforcing_lines': [r12_pin(READER_SOURCE, n) for n in (28, 29, 30)]}
        elif control == 'R12B':
            r12_fixture(control)
            p = profiles['profiles'][38]
            v = next(ch for ch in p['children'] if ch.get('origin') == 'ADMISSION' and ch['trace_site'] == V_SITE)
            t = next(ch for ch in p['children'] if ch.get('origin') == 'ADMISSION' and ch['trace_site'] == T_SITE)
            t['invocation'] = copy.deepcopy(v['invocation'])
            t['operand_source'] = copy.deepcopy(v['operand_source'])
        else:
            r12_site(trace, T_SITE)['count']['enforcing_lines'][-1].pop('sha256')
        bundle['x-construction']['admission_trace'] = copy.deepcopy(trace)
        try:
            round12_checks(profiles, bundle, freeze.read_text())
        except ValueError as error:
            require(R12_CONTROL_MESSAGES[control] in str(error), 'WRONG RED ' + control + ': ' + str(error))
            print('RED %s: exit 1: %s' % (control, error))
        else:
            raise ValueError('UNEXPECTED GREEN ' + control)
    print('GREEN mutation controls: %d intended RED (%d preserved + %d D15), zero filesystem writes' %
          (len(old) + len(selected), len(old), len(selected)))


mutation_controls = round12_mutation_controls
CONTROL_MESSAGES.update(R12_CONTROL_MESSAGES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', type=Path, default=FREEZE)
    parser.add_argument('--schemas', type=Path, default=SCHEMAS)
    parser.add_argument('--profiles', type=Path)
    parser.add_argument('--required-check', choices=('R1', 'R2', 'R3', 'R4'))
    parser.add_argument('--round8-check', choices=tuple(ROUND8_CHECKS))
    parser.add_argument('--round12-check', choices=('counts', 'route-equality', 'operand-sources', 'all'))
    parser.add_argument('--round12-fixture', choices=('R12A', 'R12B'))
    parser.add_argument('--round11-check', choices=('reachability','selectors','exclusion'))
    parser.add_argument('--round9-check', choices=tuple(ROUND9_CHECKS))
    parser.add_argument('--test-first-branch', choices=('verify-preflight','git-ls-files'))
    parser.add_argument('--foreign-binding', choices=('admission_binding_sha256','payload_binding_sha256'))
    parser.add_argument('--print-hashes', action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    parser.add_argument('--mutation-controls', action='store_true')
    parser.add_argument('--control', choices=tuple(CONTROL_MESSAGES))
    args = parser.parse_args()
    if args.round12_fixture:
        r12_fixture(args.round12_fixture); return 0
    if args.round12_check:
        profiles = read_json(args.profiles) if args.profiles else None
        bundle = read_json(args.schemas); trace = (profiles or bundle)['x-construction']['admission_trace']
        if args.round12_check == 'counts': r12_counts(trace)
        elif args.round12_check == 'route-equality': r12_route_equality(profiles, bundle)
        elif args.round12_check == 'operand-sources': r12_operand_sources(trace)
        else: round12_checks(profiles, bundle, args.freeze.read_text())
        print('GREEN D15 ' + args.round12_check); return 0
    if args.round11_check:
        profiles=read_json(args.profiles) if args.profiles else None
        bundle=read_json(args.schemas);trace=(profiles or bundle)['x-construction']['admission_trace']
        if args.round11_check=='reachability':r11_reachability(profiles,bundle)
        elif args.round11_check=='selectors':r11_selectors(trace)
        else:r11_exclusion(trace)
        print('GREEN D14 '+args.round11_check);return 0
    if args.test_first_branch:
        test_first_branch(read_json(args.profiles),args.test_first_branch)
        return 0
    if args.round9_check:
        profiles=read_json(args.profiles or PROFILES)
        if args.foreign_binding: foreign_delegation(profiles,args.foreign_binding)
        ROUND9_CHECKS[args.round9_check](profiles,read_json(args.schemas),args.freeze.read_text())
        print('GREEN round9 '+args.round9_check)
        return 0
    if args.round8_check:
        ROUND8_CHECKS[args.round8_check](read_json(args.profiles or PROFILES), read_json(args.schemas), args.freeze.read_text())
        print('GREEN round 8 ' + args.round8_check)
        return 0
    if args.required_check:
        bundle = read_json(args.schemas)
        if args.required_check == 'R3':
            required_r3(bundle)
        else:
            REQUIRED_CHECKS[args.required_check](read_json(args.profiles), bundle)
        print('GREEN ' + args.required_check)
        return 0
    if args.mutation_controls or args.control:
        mutation_controls(args.freeze, args.schemas, [args.control] if args.control else None)
        return 0
    if args.profiles:
        check(args.freeze, args.schemas)
        return validate_profiles(args.profiles, read_json(args.schemas), args.freeze.read_text())
    if args.print_hashes:
        for name, digest in hashes(args.freeze.read_text(encoding='utf-8'), args.schemas).items():
            print(name + ' ' + digest)
        return 0
    definitions, requests, examples, references, lines, _, bindings, observations = check(args.freeze, args.schemas)
    print('GREEN: %d schemas, %d request kinds, %d examples validated, %d hash references recomputed, %d bindings rerendered, %d observations checked' %
          (definitions, requests, examples, references, bindings, observations))
    if args.negative_control:
        mutation_controls(args.freeze, args.schemas, ['M5'])
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
