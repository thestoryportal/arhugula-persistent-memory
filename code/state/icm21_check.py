"""Read-only validation of the approved ICM v2.1 common wire contracts."""
import argparse
import base64
import binascii
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


CHECK_IDS = frozenset('''C-KEEP C-CONTAINER C-HOLD C-MOVE C-PHASE C-AUDIT-IMPORT
C-QUEUE C-RUN C-MODEL C-WORKTREE C-TOOL C-ROOT C-LEDGER C-REFERENCES C-LABVIZ
C-LANES C-RECORD C-CREATION C-BOUNDARY C-STAGED C-GENERATED C-GRAFT C-AUDIT
C-HANDOFF C-TWINS C-WIRE C-ADMISSION C-LEAN'''.split())
WIRE_TYPES = frozenset('''str id path relpath sha int UTC Status PrdId b64
Finding CheckResult Coverage Exclusion Config Binding Hold Registries RegistryEntry
ReferenceResults ReaderResult ReferenceRow ReferenceManifest Repair RepairSet
CoverageArtifact ByteEdit AuditReport DirtySource WorkspaceRequest WorkspacePolicy
ApprovedRequests LaneScopes LaneScope LaneCapability Admit Deny'''.split())


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def unique(values, reason):
    require(len(values) == len(set(values)), reason)


def decode(value):
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValueError('invalid base64') from error


def validate_schema(value, rule, definitions):
    """Interpret the keyword subset used by the sealed machine schema annex."""
    if '$ref' in rule:
        name = rule['$ref'].removeprefix('#/$defs/')
        require(name in WIRE_TYPES and name in definitions, 'unknown wire type')
        validate_schema(value, definitions[name], definitions)
        if name in ('path', 'relpath'):
            parts = value.split('/')[1:] if name == 'path' else value.split('/')
            require(all(part not in ('', '.', '..') for part in parts),
                    'path is not normalized')
            require(not any(char in value for char in '\x00\r\n'),
                    'invalid path spelling')
        elif name == 'UTC':
            try:
                datetime.fromisoformat(value.removesuffix('Z') + '+00:00')
            except ValueError as error:
                raise ValueError('invalid UTC instant') from error
        elif name == 'b64':
            decode(value)
        validate_semantics(name, value)
        return
    if 'anyOf' in rule:
        for alternative in rule['anyOf']:
            try:
                validate_schema(value, alternative, definitions)
                return
            except ValueError:
                pass
        raise ValueError('no permitted alternative')
    if 'const' in rule:
        require(type(value) is type(rule['const']) and value == rule['const'],
                'invalid constant')
    if 'enum' in rule:
        require(value in rule['enum'], 'unknown enum value')
    kind = rule.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'null': type(None)}
    if kind is not None:
        require(kind in types and type(value) is types[kind], 'invalid field type')
    if kind == 'object':
        properties = rule['properties']
        require(set(rule['required']) <= value.keys(), 'missing field')
        require(value.keys() <= properties.keys(), 'extra field')
        for key, item in value.items():
            validate_schema(item, properties[key], definitions)
    elif kind == 'array':
        require(len(value) >= rule.get('minItems', 0), 'too few items')
        if rule.get('uniqueItems') or rule['items'].get('$ref') == '#/$defs/id':
            unique([json.dumps(x, sort_keys=True) for x in value], 'duplicate item')
        for item in value:
            validate_schema(item, rule['items'], definitions)
        item_name = rule['items'].get('$ref', '').removeprefix('#/$defs/')
        identity = {'ReaderResult': 'registry_id', 'LaneScope': 'lane'}.get(item_name, 'id')
        properties = definitions.get(item_name, {}).get('properties', {})
        if properties.get(identity) == {'$ref': '#/$defs/id'}:
            unique([item[identity] for item in value], 'duplicate collection ID')
    elif kind == 'string':
        require(len(value) >= rule.get('minLength', 0), 'empty string')
        if 'pattern' in rule:
            require(re.fullmatch(rule['pattern'], value) is not None, 'invalid spelling')
    elif kind == 'integer':
        require(value >= rule.get('minimum', 0), 'negative integer')


def validate_argv(argv):
    for argument in argv:
        tokens = re.findall(r'\{([A-Za-z_][A-Za-z0-9_]*)\}', argument)
        require(set(tokens) <= {'root', 'references', 'config', 'policy'},
                'unknown substitution token')


def validate_semantics(name, value):
    if name == 'RegistryEntry':
        require(set(value['check_ids']) <= CHECK_IDS, 'unknown check ID')
        if value['status'] == 'UNVERIFIED':
            require(value['hold_id'] is not None, 'UNVERIFIED registry needs a hold')
            if value['path'].startswith('/'):
                require(value['adapter_argv'] is None, 'UNVERIFIED external adapter')
        if value['adapter_argv'] is not None:
            validate_argv(value['adapter_argv'])
    elif name == 'Registries':
        validate_argv(value['dispatcher'])
        require(bool(value['dispatcher']), 'missing dispatcher')
        entries = value['reader_registry'] + value['loader_registry']
        unique([entry['id'] for entry in entries], 'duplicate registry ID')
    elif name == 'ReferenceResults':
        ids = [reader['registry_id'] for reader in value['readers']]
        require(ids == sorted(ids), 'reader results not in ID order')
    elif name == 'Config':
        require(set(value['required_checks']) <= CHECK_IDS, 'unknown check ID')
        require(value['nightly_utc'] == '02:00:00Z', 'invalid nightly time')
        roots = [value[key] for key in ('canonical_root', 'preservation_root',
                                      'worktree_root', 'tool_root')]
        roots += value['source_roots']
        for i, root in enumerate(roots):
            for other in roots[i + 1:]:
                require(root != other and not root.startswith(other + '/')
                        and not other.startswith(root + '/'), 'nested roots')
        unique([hold['id'] for hold in value['migration_holds']], 'duplicate hold ID')
    elif name == 'ReferenceRow':
        require(value['check_id'] in CHECK_IDS, 'unknown check ID')
        if value['role'] == 'current-reader':
            require(value['repair_path'] is not None, 'unbound current reader')
    elif name == 'Repair':
        require(bool(value['reader_ids']) and bool(value['reference_ids']),
                'unbound repair')
        end = 0
        for edit in value['edits']:
            require(edit['start'] >= end, 'overlapping or unordered byte edits')
            end = edit['end']
    elif name == 'ByteEdit':
        require(value['start'] <= value['end'], 'reversed byte edit')
        require(len(decode(value['before_base64'])) == value['end'] - value['start'],
                'byte edit length mismatch')
    elif name in ('ApprovedRequests', 'RepairSet', 'LaneScopes'):
        field, key = {'ApprovedRequests': ('requests', 'id'),
                      'RepairSet': ('repairs', 'id'),
                      'LaneScopes': ('lanes', 'lane')}[name]
        unique([item[key] for item in value[field]], 'duplicate collection ID')
    elif name == 'WorkspacePolicy':
        unique([item['id'] for item in value['capabilities']], 'duplicate capability ID')
    elif name == 'LaneCapability':
        validate_argv(value['argv'])
    elif name == 'Admit':
        raw = json.dumps(value['request'], sort_keys=True, separators=(',', ':')).encode()
        require(hashlib.sha256(raw).hexdigest() == value['request_sha256'],
                'request digest mismatch')
        require(value['destination'] == value['request']['destination'],
                'admitted destination mismatch')
    elif name == 'AuditReport':
        results, findings = value['check_results'], value['findings']
        ids = [item['id'] for item in results]
        finding_ids = [item['id'] for item in findings]
        unique(ids, 'duplicate check ID')
        unique(finding_ids, 'duplicate finding ID')
        require(set(ids) <= set(value['required_checks']), 'unknown result ID')
        linked = {key for result in results for key in result['findings']}
        require(linked == set(finding_ids), 'dangling or unreferenced finding ID')
        coverage = value['coverage']
        require(set(coverage['checked_registry_ids'])
                <= set(coverage['required_registry_ids']), 'unknown checked registry ID')
        instant = datetime.fromisoformat(value['observed_at'].removesuffix('Z') + '+00:00')
        require(value['check_id'] == instant.strftime('%H%M%S.%fZ-') + value['mode'],
                'check ID and captured UTC instant disagree')
        missing = (set(value['required_checks']) - set(ids)
                   or set(coverage['required_registry_ids'])
                   - set(coverage['checked_registry_ids']))
        statuses = {result['status'] for result in results}
        status = ('FAIL' if 'FAIL' in statuses else
                  'UNVERIFIED' if missing or 'UNVERIFIED' in statuses else 'PASS')
        require(value['overall_status'] == status, 'false audit reduction')


def validate_wire(name, value, schema, fixtures):
    if name == 'ReferenceRow[]':
        require(type(value) is list, 'expected reference array')
        for row in value:
            validate_wire('ReferenceRow', row, schema, fixtures)
        unique([row['id'] for row in value], 'duplicate reference ID')
        targets = {}
        for row in value:
            key = (row['consumer'], row['reference'])
            require(key not in targets or targets[key] == row['final_target'],
                    'ambiguous historical key')
            targets[key] = row['final_target']
        return
    validate_schema(value, {'$ref': '#/$defs/' + name}, schema['$defs'])
    if name == 'ReferenceManifest':
        for key in ('references', 'registries', 'executor', 'repairs', 'coverage'):
            binding = value[key]
            require(binding['path'] in fixtures, 'missing bound fixture')
            require(hashlib.sha256(fixtures[binding['path']]).hexdigest()
                    == binding['sha256'], 'changed binding')


def wire(schema, examples):
    require(type(examples) is dict and set(examples) == {'schema_version', 'fixtures',
                                                       'examples'}, 'invalid examples envelope')
    require(type(examples['schema_version']) is int and examples['schema_version'] == 1,
            'invalid examples version')
    require(type(examples['fixtures']) is dict, 'invalid fixture table')
    fixtures = {}
    for path, record in examples['fixtures'].items():
        validate_schema(path, {'$ref': '#/$defs/path'}, schema['$defs'])
        require(type(record) is dict and set(record) == {'bytes_base64'},
                'invalid fixture record')
        require(type(record['bytes_base64']) is str, 'invalid fixture bytes')
        fixtures[path] = decode(record['bytes_base64'])
    require(type(examples['examples']) is list and bool(examples['examples']),
            'empty examples')
    results = []
    for example in examples['examples']:
        require(type(example) is dict and set(example) == {'id', 'type', 'expected',
                    'layer', 'value', 'rule'}, 'invalid example record')
        for key in ('id', 'type', 'rule'):
            require(type(example[key]) is str and bool(example[key]), 'invalid example field')
        require(example['expected'] in ('PASS', 'FAIL'), 'invalid expected status')
        require(example['layer'] in ('schema', 'semantic'), 'invalid example layer')
        require(example['type'] in WIRE_TYPES or example['type'] == 'ReferenceRow[]',
                'wire type outside approved scope')
        try:
            validate_wire(example['type'], example['value'], schema, fixtures)
            observed, reason = 'PASS', 'Valid wire value'
        except ValueError as error:
            observed, reason = 'FAIL', str(error)
        results.append({'id': example['id'], 'expected': example['expected'],
                        'observed': observed, 'reason': reason})
    unique([item['id'] for item in results], 'duplicate example ID')
    return {'status': 'PASS' if all(item['expected'] == item['observed']
                                  for item in results) else 'FAIL', 'results': results}


def reject_constant(value):
    raise ValueError('invalid JSON constant: ' + value)


def read_json(path):
    return json.loads(path.read_bytes().decode('utf-8'), parse_constant=reject_constant)


def audit_schema():
    package = Path(os.environ['ICM_PACKAGE'])
    binding = read_json(package / 'context.json')['sources']['WIRE-SCHEMAS.json']
    raw = Path(binding['path'].replace('{package}', str(package))).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == binding['sha256'], 'changed wire schema')
    return json.loads(raw)


def active_graft(value):
    def mentions(item):
        if isinstance(item, str):
            return re.search(r'\bgraft\b', item, re.IGNORECASE) is not None
        if isinstance(item, list):
            return any(mentions(child) for child in item)
        if isinstance(item, dict):
            return any(mentions(key) or mentions(child) for key, child in item.items())
        return False

    require(type(value) is dict, 'loader config must be an object')
    return any(mentions(value[key]) for key in ('hooks', 'mcpServers', 'plugins')
               if key in value) or mentions(value.get('search', {}).get('exceptions', [])) \
        or any(mentions(key) and enabled is True
               for key, enabled in value.get('enabledPlugins', {}).items())


def audit(root, mode, config):
    """Inspect registered loader data without executing its commands or adapters."""
    started = time.monotonic_ns()
    instant = datetime.now(timezone.utc)
    schema = audit_schema()
    validate_wire('Config', config, schema, {})
    root = Path(root)
    require(str(root) == config['canonical_root'] and root.is_dir(), 'invalid audit root')
    require(mode in ('session', 'nightly'), 'invalid audit mode')
    coverage = {'inspected': [], 'excluded': [], 'required_registry_ids': [],
                'checked_registry_ids': []}
    findings, results = [], []

    def violation(path, reason):
        identity = str(path) + '\n' + reason
        finding_id = 'F-GRAFT-' + hashlib.sha256(identity.encode()).hexdigest()
        findings.append({'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R9'],
                         'paths': [str(path)], 'evidence': [], 'reason': reason,
                         'previous_finding': None, 'resolution_receipt': None})

    def bound_bytes(path, expected):
        raw = path.read_bytes()
        coverage['inspected'].append(str(path))
        require(hashlib.sha256(raw).hexdigest() == expected, 'changed bound source')
        return raw

    if 'C-GRAFT' in config['required_checks']:
        missing = []
        registry_path = Path(config['registries']['path'])
        try:
            raw = bound_bytes(registry_path, config['registries']['sha256'])
            registry = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
            validate_wire('Registries', registry, schema, {})
            for role in ('reader', 'loader'):
                require(all(entry['role'] == role for entry in registry[role + '_registry']),
                        'registry role mismatch')
        except OSError as error:
            missing.append(str(error))
        except (ValueError, KeyError, TypeError) as error:
            violation(registry_path, str(error))
        else:
            entries = [entry for entry in registry['reader_registry']
                       + registry['loader_registry'] if 'C-GRAFT' in entry['check_ids']]
            coverage['required_registry_ids'] = sorted(entry['id'] for entry in entries)
            if not entries:
                missing.append('No registered Graft loader coverage')
            for entry in entries:
                path = root / entry['path']
                if entry['status'] == 'UNVERIFIED' or entry['source_sha256'] is None:
                    missing.append(entry['id'])
                    continue
                try:
                    raw = bound_bytes(path, entry['source_sha256'])
                    value = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
                    present = active_graft(value)
                except OSError as error:
                    missing.append(entry['id'] + ': ' + str(error))
                except (ValueError, KeyError, TypeError, AttributeError) as error:
                    violation(path, str(error))
                else:
                    coverage['checked_registry_ids'].append(entry['id'])
                    if present:
                        violation(path, 'Active Graft loader or search exception')
        status = 'FAIL' if findings else 'UNVERIFIED' if missing else 'PASS'
        results.append({'id': 'C-GRAFT', 'status': status, 'prd_ids': ['ICM-R9'],
                        'argv': [], 'exit_code': None, 'stdout_sha256': None,
                        'stderr_sha256': None, 'findings': [f['id'] for f in findings],
                        'reason': '; '.join(missing) if missing else
                                  'Active Graft detected' if findings else
                                  'Registered loader data is Graft-free'})
    coverage['inspected'] = sorted(set(coverage['inspected']))
    coverage['checked_registry_ids'].sort()
    statuses = {result['status'] for result in results}
    incomplete = (set(config['required_checks']) - {result['id'] for result in results}
                  or set(coverage['required_registry_ids'])
                  - set(coverage['checked_registry_ids']))
    overall = ('FAIL' if 'FAIL' in statuses else
               'UNVERIFIED' if incomplete or 'UNVERIFIED' in statuses else 'PASS')
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True)
    report = {'schema_version': 1, 'check_id': instant.strftime('%H%M%S.%fZ-') + mode,
              'observed_at': instant.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'root': str(root),
              'source_commit': commit.stdout.decode().strip() if commit.returncode == 0
                               else 'UNVERIFIED',
              'dirty_source_digests': [], 'mode': mode, 'coverage': coverage,
              'required_checks': config['required_checks'], 'check_results': results,
              'findings': findings, 'previous_report': None, 'overall_status': overall,
              'duration_ms': (time.monotonic_ns() - started) // 1000000,
              'reviewed_narrative_paths': [], 'unreviewed_narrative_paths': [str(root)]}
    validate_wire('AuditReport', report, schema, {})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('wire')
    command.add_argument('--root', type=Path, required=True)
    command.add_argument('--schema', type=Path, required=True)
    command.add_argument('--examples', type=Path, required=True)
    args = parser.parse_args()
    try:
        require(args.root.is_absolute() and args.root.is_dir(), 'invalid root')
        result = wire(read_json(args.schema), read_json(args.examples))
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {'status': 'FAIL', 'reason': str(error)}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
