#!/usr/bin/python3
"""Static R2O v4/schema-v3 correctness and construction check; no host or product execution."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
FREEZE = HERE / 'shared_disk_clearance_freeze_v4.md'
SCHEMAS = HERE / 'shared_disk_clearance_schemas_v3.json'
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
    example_count = examples_valid(bundle)
    binding_count = invocation_coherence(bundle)
    mandatory_hash_completeness(text, bundle)
    reference_count, observation_count = coherent_examples(text, bundle)
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
    for key in ('invocation', 'executor_invocation', 'intel_invocation', 'existing_admission', 'authorized_payload'):
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
    require(isinstance(manifest, dict) and isinstance(citations, dict) and set(manifest) == set(citations),
            'mandatory hash manifest/source keys mismatch')
    lines = text.splitlines()
    citation_path = 'results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v4.md'
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
            continue  # Stored last-decision proof remains a proof of the earlier commit.
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
    'M12': 'profiles[0]/invocation/sandbox_profile_sha256: additional property',
    'E3': 'invalid example: REQUEST_UNITRequest',
    'E5': 'missing refusal example: REQUEST_UNIT',
    'E4S': 'transition request sequence mismatch: ATTACH_STREAM',
    'E4A': 'authority derived state mismatch: AuthorityRecordStream',
    'E4C': 'invalid example: ActionReceipt',
    'E4N': 'clearance consumption binding mismatch: CONSUME_CLEARANCE',
    'E4F': 'admin fence kind mismatch: INITIALIZE',
    'E4B': 'ReceiptBlob hash mismatch: ReceiptBlob',
}


def damaged_copy(control, freeze, schemas, directory):
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
    schema_path = directory / (control + '.json')
    freeze_path = directory / (control + '.md')
    schema_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    pins = hashes(text, schema_path)
    for name, digest in pins.items():
        text, count = re.subn(r'(\| ' + name + r' pin \| `)[0-9a-f]{64}(`)',
                              lambda m: m[1] + digest + m[2], text)
        require(count == 1, 'mutation copy missing pin row: ' + name)
    freeze_path.write_text(text, encoding='utf-8')
    return freeze_path, schema_path


def mutation_controls(freeze, schemas, controls=None):
    tmp_root = os.environ.get('TMPDIR')
    require(bool(tmp_root) and Path(tmp_root).is_dir(), '$TMPDIR must exist')
    failures = []
    with tempfile.TemporaryDirectory(prefix='r2k-controls-', dir=tmp_root) as tmp:
        for control in controls or tuple('M%d' % i for i in range(1, 13)):
            extra = []
            if control == 'M12':
                # P is read-only; damage only this TMPDIR snapshot.
                profiles = read_json(HERE / 'science_launch_profiles_v1.json')
                science = next(p for p in profiles['profiles'] if p.get('scope') == 'SCIENCE')
                science['invocation']['sandbox_profile_sha256'] = '0' * 64
                profiles['profiles'].remove(science)
                profiles['profiles'].insert(0, science)
                copy_p = Path(tmp) / 'M12-profiles.json'
                copy_p.write_text(json.dumps(profiles), encoding='utf-8')
                copy_f, copy_j = freeze, schemas
                extra = ['--profiles', str(copy_p)]
            else:
                copy_f, copy_j = damaged_copy(control, freeze, schemas, Path(tmp))
            run = subprocess.run(['/usr/bin/python3', '-B', str(Path(__file__).resolve()),
                                  '--freeze', str(copy_f), '--schemas', str(copy_j)] + extra,
                                 capture_output=True, text=True)
            first = run.stderr.splitlines()[0] if run.stderr else '(no error)'
            expected = CONTROL_MESSAGES[control]
            if run.returncode != 1 or expected not in first:
                failures.append(control)
                print('PRECHECK RED %s: expected exit 1 with %r; got exit %d: %s' %
                      (control, expected, run.returncode, first))
            else:
                print('RED %s exit=%d %s' % (control, run.returncode, first))
        require(not failures, 'mutation control expectations unmet: ' + ','.join(failures))



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


def validate_profiles(path, bundle):
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
    if errors:
        for error in errors:
            print('FAIL: ' + error, file=sys.stderr)
        return 1
    print('GREEN profiles: %d LaunchProfile entries, %d not_admitted entries schema-validated, %d not_admitted entries without a J3 schema' %
          (len(profiles['profiles']), validated - len(profiles['profiles']), untyped))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', type=Path, default=FREEZE)
    parser.add_argument('--schemas', type=Path, default=SCHEMAS)
    parser.add_argument('--profiles', type=Path)
    parser.add_argument('--print-hashes', action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    parser.add_argument('--mutation-controls', action='store_true')
    parser.add_argument('--control', choices=tuple(CONTROL_MESSAGES))
    args = parser.parse_args()
    if args.mutation_controls or args.control:
        mutation_controls(args.freeze, args.schemas, [args.control] if args.control else None)
        return 0
    if args.profiles:
        bundle = read_json(args.schemas)
        schema_correctness(bundle)
        return validate_profiles(args.profiles, bundle)
    if args.print_hashes:
        for name, digest in hashes(args.freeze.read_text(encoding='utf-8'), args.schemas).items():
            print(name + ' ' + digest)
        return 0
    definitions, requests, examples, references, lines, _, bindings, observations = check(args.freeze, args.schemas)
    print('GREEN: %d schemas, %d request kinds, %d examples validated, %d hash references recomputed, %d bindings rerendered, %d observations checked' %
          (definitions, requests, examples, references, bindings, observations))
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
